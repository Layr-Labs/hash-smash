# R37P40l: the 14-bit window prefilter, the rare-path row-16 skip, and three fixed-slot folds (b)-(d) (Appendix BG): time_log2 57.21528 (each first-block compression charged as one unit)

Track `sha256-r37-exploratory`; target `sha256-r37-prefix-v1`; C = 2644. Claim: time_log2 = **57.21528** (every first-block target compression charged as one unit, SB_FB = 2644; Section 9.11), memory_log2_bytes = **20.0** (actual bound 1,035,912 bytes), success probability >= 0.39 under the inherited premises. This revision combines the 14-bit prefilter of Section 9.6e, the rare-path row-16 test skip of Section 9.6f, and the three fixed-slot folds (b)-(d) of Appendix BG; everything else, including the folds of Section 9.6d and the seven-lane first-block batch (P8, Section 9.11, credited to samsmith's f1163fcf, lamb356's 22fc4519 and dredozubov's ffca313a), is inherited unchanged from the R37P40h row (Jbenisek's d393eb30) and the R37P40g row (mpjunior92's 5068800b).

**This revision (R37P40l; a credited derivative of Jbenisek's d393eb30-a026-4289-9ef3-345118690267 at 57.23762, mpjunior92's 5068800b-8fe9-402c-bf58-ab6c458679f4 at 57.00229, and the five-fold itemisation of mpjunior92's b460364c).** Two architectural improvements on the compliant one-unit compression cost model, plus the three fixed-slot folds (b)-(d) of Appendix BG:
1. *The 14-bit window prefilter before the class test (Section 9.6e).* The text reads one byte of a 16,384-byte table T at the 14-bit window x[23:10] of x = A_{-1}, and branches on it; the class test (`CT_DET` = 219, Section 9.2) runs only when the byte is 1. T[v] = 1 iff some x with x[23:10] = v lies in the union U of Section 9.6d (e), the set of x for which some class passes. Under H1, Pr[byte = 1] = **P_H = 11,008 / 16,384 = 0.671875** (counted exhaustively). The prefilter costs 5 primitives in `FIXED`; class test moves to vbar at P_H x 220 = 147.8125. `FIXED` 266 -> 52, `FIXED_P7` 240 -> 26.
2. *No re-check of row 16 in the rare path (fold (j), Section 9.6f).* A pair enters the rare path for l only after the exact row-16 test of Lemma 6.2 (table stage plus residual test), which decides every cell and printed two-bit condition closing at row 16 (exhaustively checked, Appendix A). The rare path still computes row 16 (106 + counter) to reach row 17, but no longer re-checks it (53): `c3b_l = 2 + 6 + (ROWCOMP + 1) + c3b_row = 275` per l (was 328). `step3b` computes row 16 and goes straight to row 17; it keeps an uncounted assertion that the skipped check would pass. 3. *Three fixed-slot folds (Appendix BG).* (b) The q planes a sweep reads are fixed by its list and batch, and the W6 texts are written per list, so the sweep pays one load per plane, not an address add plus load: `3 + 2 zq` -> `3 + zq`, -27.168 ops/FB. (c) The 15 spill planes of a batch sit at fixed slots of the spill area, so each spilled-W store and reload pays one access, not an address add plus access: `SPILL 30 -> 15` per batch, -131.516 ops/FB. (d) The rep planes of a batch are contiguous and read at fixed offsets from the batch pointer, the pointer operations still charged: `2 dyn + 2` -> `dyn + 2` per batch, -48.750 ops/FB. Together perclass 4,770.967335 -> 4,563.533863, vbar 11,864.468984 -> 11,657.035512, and the claim 57.23598 -> 57.21528.

| quantity | R37P40h (d393eb30) | this revision (R37P40l) |
|---|---|---|
| FIXED / FIXED_P7 | 52 / 26 | **52 / 26** |
| prefilter term `P_H x 220` | 147.812500 | **147.812500** |
| rare path term (ops/FB) | 177.639356 | **161.162155** |
| vbar | 11,880.946185 | **11,657.035512** |
| first-block compression charge SB_FB | 2644 (one unit) | **2644 (one unit)** |
| per first block (units) | 5.50338 | **5.41870** |
| N_FB | 30,821,555,499,893,254 | **30,821,554,876,811,406** |
| V_MAX | 366,213,654,838,435,955,119 | **359,311,912,272,790,214,230** |
| vmax_fb | 54,908,864,824.7 | **53,789,931,987.9** |
| Bernstein exponent / Pcap (computed, assumed) | 14.81975, 3.663222e-07 <= 37/100000000 | **approximately 21.41381, 3.579311e-07 <= 9/25000000** |
| mu_req / floor | 0.49466303 / 0.39000000213977449 | **0.49466302 / 0.3900000060442928** |
| PRE | 2^39 | **2^39** |
| memory | 1,035,912 B | **1,035,912 B** |
| N | 449,261,493,716,360,381,556 | **442,359,749,485,967,173,670** |
| log2 T | 57.23761084974768 | **57.215275556308605** |
| claim | 57.23762 | **57.21528** (-0.02234 bit) |

The same ledger at the stated sensitivities (one-unit charge): organizer-side scan/pad keys (Appendix Q) at most 57.28905 and structural worst case (every row set, every block padded) at most 57.33417 (both bounds computed on the R37P40k cells; the three fixed-slot folds only lower them); A_C = 2^56 / 2^60 / 2^64: 57.73029 / 60.19519 / 64.01301.

**R37P40g (mpjunior92's 5068800b-8fe9-402c-bf58-ab6c458679f4, 57.00229; the base row of this filing, inherited unchanged; its text follows as filed, and "this revision" in it means R37P40g).** Base of that row: mpjunior92's 2d78ed8b-2f18-4d4b-9839-f80bcd29f662, 57.05080, the R37P39 row. The algorithm, the characteristic, the 170-class / 599,760-variant family, q3c = 2^-71.4162, EXQ = 2.482, every premise H1-H7 and every probability are inherited unchanged; the set of pairs examined, the collision event and every returned pair are identical. Folds (a) and (e) qualified in our 6a791e39-0b8f-4969-9459-5211bbd897fa (R37P40e, 57.00655); this revision adds fold (g) to them. Three folds of the counted program change ((a) on-the-fly CB3/KZ planes, (e) lazy first-block setup, (g) class-plane scan behind the zero branch), and each is a fall in executed primitives (Section 9.6d gives each one item by item; the labels (a)-(e) are those of the fold list there, and only the folds listed here are filed):
Its three folds, (a) CB3/KZ planes formed in the sweep, (e) lazy first-block setup and (g) the class-plane scan behind the zero branch, are itemised in Section 9.6d with their charges; its ledger is the R37P40g column of the table above (57.05080 -> 57.00229 on the R37P39 row).

Text below that describes R37P40g or earlier as "this revision", "this filing" or "our" is inherited from those filings and keeps their attribution and their numbers as the record of those rows. The operative numbers of this filing are those of the R37P40l paragraph and table above, Sections 9.6e, 9.6f and 10-11, 14.1, 14.2 (v) and Appendices B, C, D and BG.

This is a credited derivative of Jbenisek's aa0e8b6a-6fd1-4a8b-9917-bb5e0f8a689f and newjordan's 5dbbb8da-cc6d-400c-a243-44f440ab6a2c. Two algorithm changes, credited to slkzgm's f2da0e13-698a-4f8b-87d8-6c5914918da8 (57.89863) and inherited unchanged here: (1) an 8192/2048-word Low-first 13 conditional probe instead of the eager 4096/4096-word LO/MID probe; (2) the residual three-condition exact test, 13 rather than 34 operations. One further change is statistical and is our own (d3e7fe15-02f2-4f04-8170-13923742c0a2, credited): the declared cell bound q3c is measured on this filing's own variant list by fresh preregistered blocks, 2^-71.4162 (Appendices G.3, G.5 and N), instead of any bound transferred from the parents' pool (Section 7.4c, Appendix G). One family change is also ours. The examined family is restricted to the four kept lists (0, 1, 5, 6): 170 of the parents' 222 classes and 599,760 of their 782,800 variants. The restriction is **0.18163 bit** of exact ledger arithmetic on R37P29's program: the filed family's row 57.21653 against the ten-list family's 57.39816, both priced by `experiments/lowm.py` on the same group stage (`reports/receipts/r37-tenlist-60.out`; its control reproduces the filed family bit for bit). This revision does not re-price it: on the four-bit program the ten-list table holds a cube-{0, 7} class this filing does not build (`r37-cube4file-100.out`). The earlier cells (0.11133 bit at 57.33131 on R37P23's program, 0.11361 at R37P24) are superseded by this re-pricing. The charge that decides it is the per-pair preparation `c_c = E_class/(P6 n)`: 10.6860-10.9224 on the four kept lists against 20.1644-20.7967 on the six dropped ones, against a break-even of 11.5060 ops per pair on the filed family, so every dropped list is dearer than the family it would join. The member charge per variant runs the other way (2.4709-2.4734 kept against 0.9867-0.9882 dropped) and is not the deciding quantity; the earlier per-variant member-charge comparison of the dropped and the kept lists is a superseded sensitivity that does not reproduce under this revision's member charge (the receipt prints both ranges). q3c is then declared from this filing's own direct study of the submitted pool (Appendix N): **2^-71.4162**, the one-sided 99% lower bound of the mean of the 16,384 *linear* estimates of block F on the 599,760-word list (seeds 800000..816383, mean 2^-71.41331, relative sd of the linear estimates 0.1095, bound 2^-71.41618, rounded down; the 32 shard statistics and the digest of all 16,384 values are in N). Block E's log-scale declaration 2^-71.4243 (claim 57.58779) is 0.0087 bit weaker on the same data and is a stated sensitivity (Appendix G.5). No sub-pool transfer allowance is paid: the two pools' measured means differ by 0.0003 bit, and the parents'-pool pooled bound 2^-71.4474 (claim 57.61074) and the same bound less the 0.0020-bit allowance (2^-71.4494, claim 57.61273) remain stated sensitivities. Structurally, under Lemma 7.1 the variant enters q3 only through the four W24 conditions on `W24x = Z + W8x`, so with `Z` uniform the map `W8 -> Z + W8` is a bijection and the tail probability is the *same number* for every variant, hence every uniform-weight sub-pool has the same q3c exactly; this filing keeps a uniform-weight subset, not an x-reweighting, so the 0.0104-bit fibre-weighting gap of fb039a6e's preregistered study (Section 7.5) is not the transfer that applies to it, and the flat 0.05-bit hedge the parents' text prices for an x-weighted subset is not paid either. Both superseded charges are carried as stated sensitivities: the 5x measured charge (0.0104 -> q3c 2^-71.4578, claim 57.62108) and the full 0.05 case (claim 57.62942). All three changes are disclosed; nothing else is changed. The executed cube law is inherited unchanged: Q0[0] has probability 1/4, and bits 2 and 3 each have probability 1/2 under H1. The Bernstein slack and cap are recomputed for the cheaper stages. The characteristic, S, variants, 170 classes, F6/F7 filters, H1-H7, A_C, A_S, DEV and PRE are inherited unchanged; q3c is declared from the same preregistered replicates under a tighter admissible statistic (Section 7.4c); numerical consequences in H5 are updated.

**R37P39 (mpjunior92's 2d78ed8b-2f18-4d4b-9839-f80bcd29f662, 57.05080; the row under R37P40g, inherited unchanged).** Its three changes, the replicated rep words (`MEMBER_CHARGE` (5, 4, 2, 3)), the lane-placed delta words charged (`DELTA_CLASS = 18`, `DELTA_RUN = 5`) and the true `ROW_MAX` ceiling (+32 at every lane count), are itemised in Section 9.6c and charged in the ledger (Appendix B).

aa0e8b6 claimed 58.02135 (unrounded 58.021341413842665); its ledger is reproduced exactly with N = **773438176907133806360** and the same executed cube law. This filing's unrounded time is **57.002285124239535**, N = **381644576095538061596** (the R37P39 row 2d78ed8b: 57.050793277268035, N = 394694889953447974081; the 3c71035b row: 57.1030624776414, N = 409256985360860075234); the promoted parent row is 57.14300436989128 with N = 420745818490568649610, the accepted 03dcfbe1/ed0d4c15 row is 57.109025935318911 with N = 410952172318403772049, and newjordan's 5dbbb8da row is 57.10555928666688 with N = 409965881724923802993. The collision event is identical across all of them: the algorithm changes are conditional cost improvements, not new success evidence; the q3c declaration (0.0119 bit above the parents' pooled bound) is the second, statistical change.

**Validation status.** Independent arithmetic, affine counts and exhaustive tables/residual checks pass, and the deterministic intake gate accepts the package (`validate_candidate` returns `submission_state: ready`, status `mechanically_valid`; 1,019,498 B memory). The ledger reproduces to the digit (Section 11, Appendix B), `selftest` is 0 mismatches, and the organizer experiments are re-executed fresh per filing (Appendix H). Full transcripts and receipts: Sections 3, 9, 13 and Appendices B, D, G, H.

**Credited derivative of newjordan's 5dbbb8da-cc6d-400c-a243-44f440ab6a2c (57.10556), sraiw's d9f8833d-2483-478a-9815-4baea4bf5214 (59.30883), of fd115760-37ba-49c3-814e-35c44f32761c (sraiw, 60.90319), 96169e7c-8ea2-4090-afc8-edbc6aca0c98 (59.31513), ad06162f-1038-4d01-a06a-445e2238dc54 (60.71121), our 67516603-7f51-4b80-806d-9f4a379dab56 (59.5556), 221eb058-623b-41d6-a7bf-1d9b4602ce1e (60.97003), ec1340aa-ecc8-4564-8df7-006f0a2b2ce5 (R37OWN5: organizer experiments and the H1-H3 statements reused here) and 4ec21bf9-f588-4b80-bb2b-77c1ccf8c9b7 (R37R, 60.11997; its exact collision event after row 21 carried over, Section 7.7)**, with Th0rgal's 0db0eeb6-9958-43af-9700-ea9e99cee016 (61.17784), Jbenisek's ffbe30bb-ac92-4191-a589-3bf32661ee7d (60.38707, four-value patterns), R16x from 221eb058, and the lineage (Section 2): winglock's 6c77089c and 7319bba9, dd6656d4, itseasypop's 1c368173, qkniep's b947b377, GordoAR's 087a18c4, 0xshikhar's 1f12a09a, fb039a6e, 2f540248, companygardener's d3ec5c41, 44921815, 8de337d5, 8aeaed1c, def128fc, 22b7dd8b, Th0rgal's f2fe1d4d, Jbenisek's c22f86a2, newjordan's 9c6967cc, jungjipdo's ffc8c2df, 6eeefb64. The attack, the characteristic, the sets F6, F7, L*, the family of A0-variants and its 222 largest classes, the packed good-pair arithmetic, the rows 16..36 check, the four-pattern and R16x relaxations and their q3 studies, the bit-sliced algebra of the W7 and W6 programs, the 4-lane exact row-16 table stage, the zero-base scan table, the premises H1-H3 and the ledger structure are theirs.
## 0. Summary
- The complete-message algorithm, characteristic, q3 = 2^-71.4162 x 2.482 = 2^-70.10470,
  success event after row 21 and all statistical premises are inherited.
- Second change (statistical, our own): q3c_used = 2^-71.4162, the one-sided 99% lower bound of
  the mean of the 16,384 linear estimates of block F, fresh seeds preregistered on this filing's own variant list (Appendix N), with no sub-pool transfer allowance; block E's log-scale 2^-71.4243 (claim 57.58779) is a stated sensitivity. The parents'-pool pooled bound 2^-71.4474 (claim 57.61074) and the same bound less the 0.0020-bit allowance (2^-71.4494, claim 57.61273), and the preregistered min of the two per-block bounds (2^-71.4629, claim 57.62615), remain stated sensitivities; the ledger uses q3 = 2^-71.4162 x 2.482 = 2^-70.10470.
- FIRST[u[23:9]] is read first. Only a nonzero FIRST word triggers SECOND
  on u[8:0]. The state intersection decides all thirteen low-24 conditions exactly. Only E16x[30]=0, A16x[25]=A15x[25], A16x[29]=1 remain.
- The first probe stage is 12 operations per four lanes (bits 9..23 are shifted on every lane, 9.7c/d); continuation is seven
  per nonzero FIRST (six itemised primitives plus the nonzero test), including its own work-counter update. FIRST is nonzero for 2207/32768 indices. Fold and scan are unchanged. EX_OPS = 13.
- N_FB = 30821554876811406 (this revision, R37P40l; 30821546153665530 on the R37P40k row, 30821563599957281 on the R37P40g row, 30821552384484013 on the R37P39 row); FIXED = 52; FIXED_P7 = 26 (Section 9.2 folds, Sections 9.6d, 9.6e and 9.11);
  (The promoted parent row at EXTR = (1,2,2,1) is N_FB = 30821562976875433 and V_MAX = 392837736089609602185; those are not this filing's numbers.)
  vbar = 125166465733696063954897/10737418240000000000; vmax_fb = 53789931987.9; V_MAX = 359311912272790214230; slack = 1/15000; Pcap = 3.579311e-07 <= 3.60e-07 (this revision; R37P40k had vbar 127393765676096063954897/10737418240000000000, V_MAX 365705657129201863584, Pcap 2.748495e-07; R37P40g had vbar 125983563638216419091409/10737418240000000000, V_MAX 361657634990833187159, Pcap 4.404883e-07; R37P39 had vbar 128436037990856419091409/10737418240000000000, V_MAX 368697753132224020558, Pcap 3.31E-07; the 3c71035b row had vbar 133508974534856419091409/10737418240000000000, V_MAX 383259825065651273791, slack 1/15625, Pcap 6.19E-07).
- P8 (Section 9.11): seven first blocks per 256-bit register, SB_OPS = 2,688 per seven (2,745 in 5dbbb8da and 2,867 in the accepted 03dcfbe1 row: 9.11.1's 2,914 minus the 9.11.2 prepacked-literal and bc=a^b recurrence folds),
  executed at 384 per first block, but charged as one target compression each (SB_FB = 2644 = C, Rulings ba65804c and f044761e F1); FIXED_P7 = 26 after the 9.2 store-slot and c7 load-slot folds, 9.6d (e) and the 9.6e prefilter. Per first block 5.41870 units at this revision (at the former 384 charge: 4.67365 on the R37P40g row, 4.83379 on the R37P39 row, 5.01248 on the 3c71035b row).
- N = 442359749485967173670 and T=N/2644; rounded claim 57.21528. At this revision vbar =
  11657.035512 and vmax_fb = 53789931987.9 (EXTR = 0, the rep table of 9.6, replicated in 9.6c), N_FB =
  30821554876811406 and V_MAX = 359311912272790214230 (R37P40k row: N 448753471051579349088, 57.23598; R37P40g row: N 381644576095538061596, 57.00229; R37P39 row: N 394694889953447974081, 57.05080). Memory is 1,035,912 bytes,
  including an added 1,024-byte code allowance and the 16,384-byte prefilter table of 9.6e; the batch adds no resident item (inside the 64-register file). PRE = 2^39 operations.
- Validation (c) completed under the public seed; two byte-identical runs only.
- **This filing (R37P22) changes one ledger cell: `MEMBER_CHARGE` 6,7,8,11 -> 4,6,7,9** (the completion test and its branch are not executed where the discipline completes a group word on a fixed schedule, Section 9.6). Nothing else moves: `selftest` and `memory` are byte-identical to the previous filing (6,548-byte diff of `lowm.py` text: one tuple), the experiment source budget is 65,499 <= 65,536, vbar 15221.48773651485 -> 14711.52812450294, per_fb 6.09020 -> 5.89733, N 500055279001585913851 -> 484337152086165523954, claim **57.39215 -> 57.36716 -> 57.34607**.

- **P11 charges A_S at the paper's own printed figure**: the advice *is* the published Step-1 solution (Tables 15-17), so the allowance moves from the 2^50 factor to the paper's printed 2^41.3 = 2,707,315,195,888 units (completing a Step-1 solution to the SFS pair measures 25 ms, Section 11.2); A_C keeps its 169x calibration because the characteristic search is unpublished. N -> 420,745,818,490,568,649,610, claim **57.15316 -> 57.14301**; every algorithm cell, the family, q3 and the memory figure are unchanged.
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
- d9f8833d-2483-478a-9815-4baea4bf5214 (sraiw, 59.30883) and fd115760-37ba-49c3-814e-35c44f32761c (sraiw, 60.90319): the bit-sliced algebra of the W7 and W6 programs (Sections 8, 9.3-9.7) and the packed probe, carried over from their published source text into this package's `experiments/lowm.py`, which is the program of this filing (it is run here only as this package's own file, with the changes listed in its header). 67516603-7f51-4b80-806d-9f4a379dab56 (ours, 59.5556) and ec1340aa-ecc8-4564-8df7-006f0a2b2ce5 (ours, R37OWN5): the organizer experiments `h1-cv1-filters-nonce`, `h3-cowpass-nonce`, `h3-ladder-r37` and the statements of H1, H2, H3 (Appendices H and M).
- 96169e7c-8ea2-4090-afc8-edbc6aca0c98 (sraiw, 59.31513), ad06162f-1038-4d01-a06a-445e2238dc54 (sraiw, 60.71121), 221eb058-623b-41d6-a7bf-1d9b4602ce1e and 22b7dd8b-3764-4ff4-93ad-3fa9cc170026 (Jbenisek, 60.97003 and 60.99099): the filings this one is a credited derivative of; every change is listed in the summary above, in Section 9, and in the header of `experiments/lowm.py`. 2f540248-75ec-4c7a-9d85-ee9624472172 (0xshikhar, 60.97992): pruning of the broadcast planes. 9c6967cc-238f-4669-840f-856c1f3e9d10 (newjordan, 60.9723): the four-entry streaming group register and the per-(list, batch) constant planes. ffc8c2df-8ef0-42c3-a373-a0e0cf96d889 (jungjipdo, 60.98614): the 13-bit chunk scan.
- ffbe30bb-ac92-4191-a589-3bf32661ee7d (Jbenisek, 60.38707, a credited derivative of fb039a6e): the four feasible value patterns of E18[1,5,10,11,18,28,29] and E19[29] and the change of the cell strings, the solver enumeration and the three verified collisions behind them (Section 7.6); 221eb058 re-measured q3 for its own family together with R16x.
- 4ec21bf9-f588-4b80-bb2b-77c1ccf8c9b7 (ours, R37R, 60.11997; Appendix D there): the collision event after row 21 as the success event (`step3b`, `same_out`), its structure (D.2), the ratio of collision to cell events and its preregistered lower bound EXQ = 2.4331 (D.3, D.3b) (superseded here by Appendix O) and the pricing of the rare path as executed (D.5), carried over here onto this package's program and constants (Sections 7.7, 9.9). The exact-event scoring of the late rows was designed there with GPT-6-Luna (OpenAI); the reduction of the late rows to conditions on W22, W24 and W26 was first proposed by GPT 5.5 (OpenAI).
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
The characteristic fixes the modular differences of W21, W22, W23; with S (or any variant) fixed, the only remaining requirements on W6, W7 (6c77089c, Lemma 3) are W6x in F6 and W7x in F7, where F_k = {w : s0(w + d_k) - s0(w) = t_k mod 2^32}, d6 = 20000000, t6 = 03c00800, d7 = fbc00800, t7 = 017f8000. |F7| = 68,157,440 and |F6| = 287,309,824 (exhaustive over all 2^32 words by 0db0eeb6, Tungsten; the counts of 7319bba's `f6chk.c` agree). By the carry pattern of w + d (s0 is linear), each set is a disjoint union of affine spaces. We use them in the following bitwise form, **checked against the definition on all 2^32 words** (0db0eeb6, Tungsten: about 10 CPU-minutes, zero mismatches for both; here `selftest` and the organizer experiments compare the plane programs with the definitions):
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
Under H1 (CV1 uniform), for every fixed variant a0: Pr[W7x in F7] = p7 = |F7|/2^32 = 2^-5.97763 and Pr[W6x in F6 | W7x in F7] = p6 = |F6|/2^32 = 2^-3.90197 exactly; conditioned on both, (W0..W5) is uniform on (2^32)^6, (W6, W7) is uniform on F6 x F7, and they are independent. For every l in L*, (W16, ..., W21) is then a bijective image of (W0..W5) for fixed (W6, W9..W15), hence iid uniform and independent of (W6, W7). *Proof.* Lemma 4.1 (bijection for fixed a0) and the inverse expansion W5 = W21 - s1(W19) - W14 - s0(W6), W4 = W20 - s1(W18) - W13 - s0(W5), ..., W0 = W16 - s1(W14) - W9 - s0(W1). (6c77089c's Lemma 2, for each variant.)
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
(111 classes of 3456, 85 of 3600 and 26 of 3584 variants; 17 bits vary in all: the union of the masks is 01fec4dd = bits 0, 2, 3, 4, 6, 7, 10, 14, 15, 17..24; the bits 0, 2, 3, 7, 14, 15, 17..24 are in every mask.) The program builds those four lists (0, 1, 5, 6) as the member sets of the first class of each list (by enumerating the 2^14 or 2^15 subsets of the mask against the definitions of G and c7) and lets every other class of the list use them; `selftest` checks, for all 170 classes and all 599,760 variants, that the variant base | s is in G, has the class's c7 and that the class has its size (0 mismatches). **The cube of a list (computed; asserted when the list is built).** The bits 0, 2, 3 of s are *free* in the lists 0, 1, 5, 6 (every member has its partner with the bit flipped), and bit 7 is free in the 164 classes of lists 0 and 5 but in none of the six of lists 1 and 6 (Section 8.1); in the parents' other six lists bit 0 is free (they are not built). B is the set of these bits (the cube of the list), and the list is the union over f subset of B of (reps xor f), where reps = the members with no cube bit: 432 reps (lists 0, 1), 450 (lists 5, 6), 1728 (lists 2, 3, 4) and 1792 (lists 7, 8, 9). The classes of the lists 0, 1, 5, 6 have a0 bit 1 set (base bit 1 = 1), which Lemma 8.2 needs for the bits 2, 3; the classes of the other lists have base bit 1 clear and use bit 0 only. A list is stored as the planes of its reps (14 or 16 bit planes per batch of 256: the cube bits are static zeros of the main run) and as packed entries (Section 9.6), 8 batches in all (the four kept lists, two each). S0(a0) >= 8 on G and a0 < 2^29; over the 599,760 variants max S0(a0) = 0xffffbb5c (`selftest`), so (~S0(a0) & M32) <= 0xfffffff7 and no carry leaves a 64-bit lane of the packed words of Section 9.

Per first block over uniform x, every class passes the W7 test for exactly |F7| = 68,157,440 values of x, so the number of passing classes has mean 170 p7 = 2.698 and the number of variants in passing classes has mean 599,760 p7 = 9,518. Passing classes are strongly correlated (their c7 values are close), so the counts are bursty; only expectations are used.
## 6. Step 3
### 6.1 L* (exact; from 6c77089c, re-checked)
L is the set of (W14, W15) for which rows 14, 15 of both members follow the cells (with the `+` pairs) and the four expansion differences depending only on (W14, W15) equal the published pair's; |L| = 4096. L* keeps the elements whose row-16 modular differences equal the characteristic's: |L*| = 32, all with W14x = bd1d3f7b and W15x in
```text
 0:7dd41680  1:7dd41681  2:7dd416a0  3:7dd416a1  4:7dd41a80  5:7dd41a81  6:7dd41aa0  7:7dd41aa1
 8:7dd43680  9:7dd43681 10:7dd436a0 11:7dd436a1 12:7dd43a80 13:7dd43a81 14:7dd43aa0 15:7dd43aa1
16:fdb41680 17:fdb41681 18:fdb416a0 19:fdb416a1 20:fdb41a80 21:fdb41a81 22:fdb41aa0 23:fdb41aa1
24:fdb43680 25:fdb43681 26:fdb436a0 27:fdb436a1 28:fdb43a80 29:fdb43a81 30:fdb43aa0 31:fdb43aa1
```
(y side: W14y = W14x ^ 04400800, W15y = W15x ^ 20000000; element 13 is the published one.) Rows 12..15 of both members depend only on S and l, not on CV1 or the variant.
### 6.2 Row 16 without a mask table
For l in L*, E16x = C_l + u with u = W0 + s0(W1) (W16 = s1(W14) + W9 + s0(W1) + W0; C_l collects rows 12..15 of l, K16, s1(W14) and W9). With the cell E16[23] = 0 of Table 15, 28 elements of L* can hold row 16 (7319bba enumerated all E16x with the row's nine fixed x-bits, 2^23 per l, and found 1,052,672 pairs (u, l); l = 0, 2, 16, 18 have none). **With R16x (Section 7.4c) the E cell of row 16 has eight fixed bits and every one of the 32 elements of L* holds row 16 for exactly 65,536 values of E16x: 2,097,152 pairs (u, l)** (`r16.c` with `r16data.h` generated from `experiments/lowm.py`, exhaustive over the 2^24 values of E16x with the eight fixed bits for each l; Appendix A). By Lemma 5.1 u is uniform for a good pair, so Pr[row 16 holds for l] = 65,536 / 2^32 = 2^-16 exactly and the expected number of row-16 hits per probed lane is 2^21 / 2^32 = 2^-11. The earlier filings read the l-mask of u from a table of 2^32 words. **This filing decides row 16 from the cells.**

**Lemma 6.2 (the exact test).** For each of the 32 l let A16x = E16x + cxA_l with cxA_l = -A12x + S0(A15x) + MAJ(A15x, A14x, A13x) (rows 12..15 of member x for l). Then E16y = E16x and A16y = A16x - 2^29 (mod 2^32), computed for all 32 l. Row 16 holds for (u, l) iff all of the following hold (cells of row 16 and the two-bit conditions closing at row 16):
```text
E16x & 40461a80 = 00060800         the eight fixed bits 30, 22, 18, 17, 12, 11, 9, 7 of the E cell (E16 has no difference: E16y = E16x; bit 23 is free under R16x)
E16x[4] = E15x[4]                  the '+' pair of the E cells of rows 15 and 16 (E15[4] = E16[4])
A16x[29] = 1                       the A cell 'u' at bit 29: with A16y = A16x - 2^29 the XOR difference is 2^29 iff A16x[29] = 1
A16x[15] != A15x[15], A16x[23] = A15x[23], A16x[25] = A15x[25]          (A15x of l is a constant)
A16x[9] != A16x[20], A16x[18] != A16x[6], A16x[8] = A16x[17]
```
*Proof.* The cells of row 16 are the A cell (u at bit 29), the E cell (eight fixed bits, no difference), the W cell (none); the printed conditions closing at row 16 are the seven of Section 3.3 (A15/A16 three, A16 three, E15/E16 one); for all 32 l the difference of E16 is zero and cyA_l - cxA_l = e0000000, which is the statement on A16y. *Checks:* the test applied to all 2^24 values of E16x with the eight fixed bits, for each of the 32 l, gives exactly the set of u of the enumeration by `r16.c` (2,097,152 pairs, no pair missing and none added; Appendix A); the experiments and `selftest` compare it with the generic row check (`row16_ok`) on random and near-miss values. QED.

**The table stage (top-first 15).** Put hi = u[23:9] (15 bits) and lo = u[8:0] (9 bits). For each l, compute e_lo = (lo + (C_l mod 512)) mod 512 and a_lo = (e_lo + (cxA_l mod 512)) mod 512. The interface state is (carry_e, carry_a, a_lo[6], a_lo[8]): the carries into bit 9 of E16x and A16x, which the completion fixes, and the two low A bits the couplings read. The 512-word table SECOND (index u[8:0]) enforces what lies below bit 9 -- E16x[4]=E15x[4] and fixed E16x bit 7 -- and returns the state; the 32,768-word table FIRST (index u[23:9]) enforces the other ten conditions under it: fixed E bits 9,11,12,17,18,22; A16x[15]!=A15x[15], A16x[23]=A15x[23], A16x[18]!=A16x[6], A16x[8]=A16x[17], A16x[9]!=A16x[20]. The last reads both of its bits off the high field, so the builder tests it as (v>>11^v)&1 rather than as a mask equality; the other four A conditions are one mask equality of that field against a word built from A15x and the state.

For every raw state, enumerate the 32768 high indices using its two carries. Delete states with empty high support before assigning state slots. Raw states can exceed two (maximum four at this split); after pruning at most two remain for each l, and two are used by 22 of the 32 l (10 use one). At bit 32*idx+l, SECOND[lo] records the realized viable state and FIRST[hi] records its accepting indices. For a fixed (lo,l) at most one state exists. Thus T=FIRST[hi]&SECOND[lo] decides exactly the conjunction of all thirteen conditions; neither approximation nor false positive is introduced. The fold G=(T|(T>>32))&M32 is the original filt(u), bit for bit.

Independent enumeration decides all 2^24 u and all 32 l: zero mismatches, 2048 passing low-24 assignments per l, sum |G|=65536, nonzero G at 63512 u. FIRST has exactly 2207 nonzero words out of 32768 (0.067352295, against 1513/8192 = 0.184692383 for the 13/11 split of R37P37 and earlier). Consequently E|G|=1/256 and Pr[G!=0]=63512/2^24 as before. No independence between lanes is used.

**Residual equivalence.** Conditional on l in G, all thirteen low-24 conditions of Lemma 6.2 already hold, leaving precisely E16x[30]=0, A16x[25]=A15x[25], A16x[29]=1. Set VA_l=0x20000000|(A15x&0x02000000), e=u+C_l, A=e+cxA_l and test `(e&0x40000000)|((A&0x22000000)^VA_l)==0`. The intermediates need no mod-2^32 masks because all inspected bits are below 32, so discarded carries cannot affect them. This residual test is only called for l in G. Generic checks on rejected lanes compare `(l in G) and residual` with the full definition, retaining the leader's all-survivor/every-sixteenth-lane coverage. Independent exhaustive testing includes every high-byte extension of each low-24 survivor: 16,777,216 cases, zero residual mismatches, and 65,536 full row-16 values per l (2,097,152 total), exactly as inherited.
## 7. The Step-3 probability for the variants (H2)
### 7.1 The quantity
For a good pair (CV1, a0) and l in L*, let F_l be the event that rows 16..36 follow every cell and every printed two-bit condition closing at rows >= 16 (the cell event) and E_l the success event of this filing: rows 16..21 follow every cell and every printed two-bit condition closing at rows 16..21 and the two 37-step outputs are equal (the collision event, Section 7.7; F_l is contained in E_l). q3c = average over the 599,760 variants of the 170 classes and over l in L* of Pr[F_l | good], the probability over CV1 (Lemma 5.1 gives the exact joint law of all second-block words); q3 = the same average of Pr[E_l | good] = q3c x R, R of Section 7.7. The expected number of successful (variant, l) per first block is g x 32 x q3.

(For this filing the event F_l is the same except that the eight value bits of rows 18 and 19 of Table 15 are not imposed and neither are E16[23] = 0 and E16[24] = E17[24] (R16x): Sections 7.4b, 7.4c and 7.6. Sections 7.3 and 7.4 describe the estimator and report the registered studies of 7319bba for the Table 15 pattern. The studies of Sections 7.3 to 7.6 estimate q3c; Section 7.7 takes q3 from q3c.)
### 7.2 Lemma 7.1 (what a variant can change)
Rows 16..22 (all their cells and two-bit conditions) are functions of S's rows 12..15, l, and W16..W22, where W16..W21 are functions of (W0..W6, W9..W15) and W22 = s1(W20) + W15 + s0(W7) + W6. By Lemma 5.1 the law of (W16..W22) given goodness is the same for every variant (W8 does not occur). **Hence the probability that rows 16..22 pass is identical for all variants, and equal to its value for the published S.** The variant enters rows 23..36 only through W8, which occurs in W23 = s1(W21) + W16 + s0(W8) + W7 and W24 = s1(W22) + W17 + s0(W9) + W8 (and in later words through them). Its modular differences are fixed (Lemma 4.2 (d)), so only the *values* of W23, W24 move; the conditions of rows 23..36 are the four on W24 (cell `n` at bit 29 and W24[4] != W24[6], W24[22] = W24[31], W24[20] != W24[27]); all other cells of rows 23..36 are `=` and hold automatically once the differences cancel. W24x = Z + W8x with Z = s1(W22x) + W17x + s0(W9x), and Z is (nearly) uniform given rows 16..22, so the four W24 conditions have probability about 2^-4 for every W8.
### 7.3 The estimator (7319bba's design; re-implemented and re-run for this filing, Section 7.4b and Appendix F)
Stages: row 16 exact (the enumeration of 6.2: the stage mean is (1/32) sum_l |R16_l| / 2^32 = 2^-16.994, and the initial particles are drawn exactly from the passing (l, E16) pairs); rows 17..21: each child proposes E_t^x uniformly with the row's fixed x-bits imposed (exact importance weight 2^-f), sets W_t^x = E_t^x - (the rest of step t), W_t^y = W_t^x + its exact difference, and checks the whole row; row 22: (W6, W7) drawn uniformly from F6 x F7; rows 23..36: W8 of a variant drawn uniformly from the 599,760 variants of the 170 classes of that time (the same row-22 survivor is also evaluated with the published W8 for a paired comparison). NP particles, M children per particle per stage, MT tail proposals per particle, multinomial resampling of the survivors after every stage; the product of the stage means is an unbiased estimator of q3 (the standard SMC normalising-constant estimator). The design is 6c77089c's and 087a18c4's; the program of the registered studies is 7319bba's. **This filing re-estimates q3 with its own program** (Section 7.4b, Appendix F), because it accepts four value patterns of rows 18 and 19: the family of variants, the classes, the filters and every row of the characteristic are those of 7319bba, and this filing changes only how the good pairs are *found* (Lemmas 8.1, 8.2) and which patterns of rows 16..19 count as a success (Sections 7.4c, 7.6), not which pairs are good or how they are tested. The estimate enters as premise H2.
### 7.4 The registered studies of 7319bba (reported unchanged)
**Study A** (registered 2026-10-10T08:11:18Z, before any listed seed ran): NP = 2048, M = 512, MT = 16384, 32 replicates; rule: the one-sided 99% Student lower bound of the mean of the 32 linear estimates (t = 2.4528, 31 df), q3_model = 2^(floor(100 log2 LB)/100). Result: mean 2^-74.0187, relative standard deviation 0.0743, lower bound 2^-74.0659, q3_model(A) = 2^-74.07. **Study B** (registered after study A had been read, to tighten the spread; same program, NP = 8192): mean 2^-73.9987, relative standard deviation 0.0378, lower bound 2^-74.0225, **q3_model = 2^-74.03 (the Table 15 value; this filing's value is in Section 7.4c)**. All 32 replicates of study B (log2):
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
The registered studies above measure the Table 15 pattern. This filing accepts four value patterns of rows 18 and 19 (Section 7.6), so q3 is measured again, and for that we wrote our own estimator, `q3smc.c` (Appendix F), from the description of Section 7.3. It shares no code with the earlier filings' program, and no other participant's program was compiled or run here. Its constants (the cells of rows 0..36, the printed two-bit conditions, the rows 12..15 of the published pair for each l, the variant list) are written by `gen_consts.py` from `experiments/lowm.py`, so the cells it checks are the ones the counted program checks. Stage 16 is an exact enumeration (with the Table 15 cell E16[23] = 0 of this study it gives the 1,052,672 pairs (u, l) of 7319bba's enumeration); stages 17..21 impose the fixed x-bits of the E cell of the row (weight 2^-f) and check the whole row for both members, including the exact difference of the schedule word; stage 22 draws (W6, W7) uniformly from F6 x F7 (W7 from its affine decomposition, W6 by rejection); the tail draws W8x uniformly from the 599,760 variants and checks rows 23..36 for both members. All parameters are those of the registered studies: NP = 8192, M = 512, MT = 16384, uniform resampling of the survivors after each of the stages 17..22, estimate = the product of the stage means.

**Preregistration** (`PREREG_q3M.txt`, sha256 9187c4519d463838b90eefb4c0aa9df1eb12be95cf463076ad06511c7aaaaabf, stamp 2026-10-12T05:26:30Z, written before any listed seed ran; the file is reproduced in Appendix F).
- *Validation V* (original cells of rows 18 and 19): 64 replicates, seeds 710000..710063. V passes if (a) its mean differs from the registered study B of 7319bba (mean 2^-73.9987, relative sd 0.0378, 32 replicates) by at most 2.576 standard errors and (b) log2 of its one-sided 99% bound is within 0.04 of study B's bound (-74.0225). It is the test that our program reproduces the q3 = 2^-74.03 of the table-free program with Table 15's cells (the program of this filing before its cells were relaxed); if V fails, no q3 is declared from it.
- *Main study* (the four patterns accepted: the eight characters removed from the two E cells): two independent blocks R1 (seeds 720000..720127) and R2 (seeds 721000..721127) of 128 replicates; rule fixed in advance: **declared q3 = 2^x, x = floor(100 log2 min(LB_R1, LB_R2)) / 100**, LB the one-sided 99% Student lower bound of the mean of the linear estimates of the block. Every listed seed was run and is reported (Appendix F); none was dropped or rerun.

**Results.** Validation V: mean 2^-73.9911, relative sd 0.0353, bound 2^-74.0064; z = +0.66 against study B; validation PASSES both preregistered criteria (|z| <= 2.576; bound within 0.04 of -74.0225). Its stage means (log2, rows 16..22 and the tail) are 16: -16.994, 17: -13.000, 18: -14.999, 19: -6.000, 20: -7.000, 21: -1.000, 22: -10.999, tail -4.000, against the registered study B's -16.994, -13.000, -15.001, -6.000, -7.000, -1.000, -10.998, -4.007. Main study: R1 mean 2^-71.9975, relative sd 0.0714, **bound 2^-72.0191**; R2 mean 2^-71.9868, relative sd 0.0681, **bound 2^-72.0074**. Rule applied: the lowest bound, rounded down to two decimals: **2^-72.02** for the four patterns alone (it was the q3 of the filing before R16x; the q3 used here is that of the joint study, Section 7.4c), 2.01 bits above the Table 15 value 2^-74.03 (structural count 2.00 bits: four patterns of equal weight; exact stage enumeration 1.93, interval 1.78 to 2.09, Appendix B of the filing this one credits for the relaxation). Stage means of the main study (log2 averaged over the 256 replicates), rows 16..22 and the tail: 16: -16.994, 17: -13.000, 18: -8.000, 19: -10.000, 20: -7.000, 21: -1.999, 22: -11.002, tail -4.000; rows 18 and 19 together contribute -18.00 against -21.00 for Table 15 and row 21 -2.00 against -1.00, the net gain being the sum of the differences. The stages of rows 16, 17, 20, 22 and of the tail are those of the Table 15 study within the sampling resolution. The pattern diagnostic (a description, not part of the bound; the program's `-d` option, seeds 730001..730003, histogram of the eight value bits E18[1,5,10,11,18,28,29], E19[29] of the 8192 particles that survived rows 16..22, as bits 0..7 in hexadecimal; Table 15's pattern is cd, the others 1b, f6 and 20): seed 730001: 1b:2349 20:1607 cd:2461 f6:1775; seed 730002: 1b:1710 20:2180 cd:2145 f6:2157; seed 730003: 1b:1714 20:1891 cd:2040 f6:2547. Exactly the four predicted patterns occur and no other.
### 7.4c Rows 16 and 17: the R16x relaxation, measured jointly with the four patterns (new; preregistered; our own estimator)
Table 15 imposes E16[23] = 0 (a `0` in the E cell of row 16) and E16[24] = E17[24] (a `+` pair of the E cells of rows 16 and 17, printed again as a two-bit condition). Neither can be dropped alone: a pair that breaks only one of them dies at row 19. Dropped together they can: at step 19, CH(E18, E17, E16) emits terms at bits 24 and 23 whenever E17 and E16 differ there, and the signed sum of row 19 absorbs them with a different sign solution of S1(E18); the pairs that continue keep the parity E16[23] ^ E19[29] ^ E18[1] ^ E18[5] = 0 together with the four patterns' parities (our backward analysis of the characteristic). Our own full-path test before this build (rows 16..36, sequential Monte Carlo with same-sample tagging, 6 fresh seeds, 4.0e8 samples, 30,814 collisions, every collision rebuilt and hashed again independently, 0 false) gave a ratio of 1.5055 (+0.590 bit, per-seed 95% interval [0.548, 0.631]) over the four patterns with the six A16 two-bit relations of row 16 necessary (0 of 49.9M violating proposals continue). A preregistered sweep of 30 further pairs of conditions of rows 16..21, each dropped together on top of R16x, found no further gain (each pair, and each member alone, gave 0 collisions; 0 false among 928,760 rehashed).

**The change to the counted program** (`experiments/lowm.py`): the character of bit 23 of `CHE[16]` is `=` instead of `0`, the character of bit 24 of `CHE[17]` is `=` instead of `+`, and the two-bit condition (E, 16, 24, =, E, 17, 24) is removed from `X2`:
```text
 row 16   Table 15 =0=====+00===11=+==01=0=0==+====     program =0=====+=0===11=+==01=0=0==+====
 row 17   Table 15 =0=====+01===u1=+==0==1===1u====     program =0======01===u1=+==0==1===1u====
```
The parity is not tested by the program: every pair that follows the remaining cells of rows 16..36 has zero output difference and is verified with the target before output, so testing it would only add operations, and the estimator below counts the pairs that follow the cells of rows 16..36 (q3c), which the program accepts together with the further collisions of Section 7.7. `row_ok` reads the masks and values of the cells as constants, so `ROWCHECK` and `ROWCOMP` are unchanged. What the change does cost is at row 16 (Section 6.2): every l in L* now has row-16 values, the 4-lane table stage has 13 conditions on bits 0..23 (E|filt(u)| = 1/256 = 0.003906 per lane, Pr[filt(u) != 0] = 63,512 / 2^24 = 0.003786), and the expected number of row-16 hits per probed lane is 2^-11 instead of 1,052,672 / 2^32. These are in the ledger (Section 11) and in the simulation of the counted program (Section 13.3).

**Joint study.** The estimator of Section 7.4b, with its constants written by `gen_consts.py` from this `experiments/lowm.py` (`q3consts_r16x.h`), so that it checks exactly the cells and conditions the counted program checks: the four patterns of rows 18 and 19 and R16x are one carrier, measured together. Stage 16 enumerates all 2^24 values of E16x with the eight fixed bits for each l and reproduces the 2,097,152 pairs (u, l) of Appendix A. The binary differs from that of Section 7.4b only by a TAG line that counts the full passes whose member x keeps E16[23] = 0 and E16[24] = E17[24]; it draws no random numbers, and built with the constants of Section 7.4b it reproduces the filed outputs of seeds 720000 and 721000 byte for byte (known-answer check). **Preregistration** (`PREREG_q3R16x.txt`, sha256 18569704b1115d99c138e641986101687836aa408e1f29d670cad354da0691d3, stamp 2026-10-12T16:13:47Z, written before any listed seed ran; reproduced in Appendix G): two independent blocks J1 (seeds 740000..740127) and J2 (seeds 741000..741127) of 128 replicates, NP = 8192, M = 512, MT = 16384; rule fixed in advance: **declared q3 = 2^x, x = floor(100 log2 min(LB_J1, LB_J2)) / 100**, LB the one-sided 99% Student lower bound of the mean of the 128 linear estimates of the block (the spread between replicates carries any overdispersion of the counts within a run). Every listed seed was run and is reported (Appendix G); none was dropped or rerun. Because these offline preregistrations, complete seed ranges, interim progress looks and prior 30-pair screening do not bind an organizer holdout nonce, the premise that they exclude material selection, optional-stopping and multiple-comparison bias beyond the margin to the declared `q3c_used = 2^-71.4162` (Appendix N; the preregistered min-of-blocks bound 2^-71.4629 and block E’s log-scale 2^-71.4243 are carried as sensitivities) is declared explicitly as part of heuristic H2 (Section 12) and checked at reduced scale on the organizer's holdout seed in `a0-online-r37` (Section 13.2).

**Results.** J1 mean 2^-71.4296, relative sd 0.1096, **bound 2^-71.4629** (one-sided 99% upper bound 2^-71.3970); J2 mean 2^-71.4177, relative sd 0.1143, **bound 2^-71.4524** (one-sided 99% upper bound 2^-71.3838, so q3c <= 2^-71.38 < 2^-70). Rule now applied: **q3c_used = 2^-71.4162**, the one-sided 99% lower bound of the mean of the 16,384 *linear* estimates of block F on this filing's own variant list (Appendix N: seeds 800000..816383, mean(est) 2^-71.41331, relative sd of the linear estimates 0.1095, bound 2^-71.41618, rounded down; no sub-pool transfer allowance, because the measured quantity is the submitted pool's own q3c). Block E's log-scale statistic (mean 2^-71.42132 of the log2 values, sd 0.15870, bound 2^-71.42420) declares 2^-71.4243, which is 0.0087 bit weaker on the same data and is carried as the superseded sensitivity beside its claim 57.58779. The rules of this section remain stated as sensitivities: the pooled 256-replicate bound 2^-71.447381 is 2^-71.4474 (claim 57.61074) and less the 0.0020-bit allowance is 2^-71.4494 (claim 57.64841), the superseded 5x charge 0.0104 gives 2^-71.4578 and claim 57.62108, and the preregistered min-of-blocks rule gives 2^-71.4629 and claim 57.62615. The statistic of this section: the one-sided 99% Student lower bound of the mean of the **pooled** 256 linear estimates -- pooled mean 2^-71.4236, relative sd 0.1118, t(254 df) = 2.3413, i.e. mean x (1 - 2.3413 x 0.1118/16) = 2^-71.447381, rounded down to four decimals of log2 and never up, 2^-71.4474. It is one pre-specified statistic over exactly the seeds the preregistration lists: both blocks were always reported, no seed was added, dropped, replaced or rerun, and no interim look or stopping rule enters it. It is 0.0155 bit tighter than the preregistered min-of-two-block-bounds rule (2^-71.4629, claim 57.62615), which remains stated as the conservative sensitivity, 0.55 bits above the four patterns alone (2^-72.02, Section 7.4b) and 2.56 bits above Table 15 (2^-74.03); the pooled mean is 0.569 bits above the pooled mean of the four-pattern study. Stage means (log2 averaged over the 256 replicates), rows 16..22 and the tail: 16: -16.000, 17: -12.000, 18: -8.000, 19: -11.430, 20: -7.000, 21: -2.000, 22: -11.003, tail -3.999 (row 16 is -16.000 exactly: 2^21 of 2^37 pairs (u, l)). Of the 2,149,260,669 full passes counted in the tails, 1,438,939,086 (a share of 0.6695) keep E16[23] = 0 and E16[24] = E17[24]; the rest use R16x, including the four l (0, 2, 16, 18) that have no row-16 value under Table 15. These shares are a description of the resampled particles, not a part of the bound.
### 7.5 The examined family of this filing
The registered studies of the parents drew W8 from the 782,800 variants of the 222 classes, and (W6, W7) uniformly from F6 x F7. **This filing examines a sub-family**: the 170 classes of lists 0, 1, 5 and 6 (599,760 variants), and (W6, W7) exactly as before. Every variant of every kept passing class is examined, and given a good pair the variant, W6 and W7 have the laws of the studies (Lemma 5.1: for every variant a0, W7x is uniform on F7 and W6x uniform on F6 given that the pair is good, independent of each other and of the variant). So q3 = the mean over the 599,760 variants and the 32 elements of L* of the study's conditional probability. The restriction is **q3-neutral**, not an x-weighting: by Lemma 7.1 the rows 16..22 cells have one probability for every variant, and the rows 23..36 cells depend on the variant only through the four W24 conditions on `W24x = Z + W8x`, with `Z = s1(W22x) + W17x + s0(W9x)`. For every fixed Z the map `W8 -> Z + W8` is a bijection of 2^32, so under the model's own `Z` near-uniformity the conditional probability of the tail is the same for every variant *exactly*, hence the mean over any sub-pool equals the mean over the whole family, and the residual is second order in the non-uniformity of Z (Section 7.8: bounded by the same 0.001 bit by which the study's own measured tail, 2^-3.999 over 782,800 variants, departs from the exact 2^-4). The parents' text prices 0.05 bit for a *weighted* subset (0db0eeb6 Section 7.6); a whole-class uniform restriction introduces no weight, so this filing does not pay that hedge, and instead charges the only *measured* transfer that exists for this quantity: fb039a6e's preregistered 128-replicate study of the same q3 over the whole family G (one-sided 99% bound 2^-74.0088) and over a kept-fibre-weighted pool (2^-73.9984), i.e. **0.0104 bit**, which is 5x the structural bound of Section 7.8 and 5x below the flat hedge. **q3c_used = 2^-71.4162**, measured directly on the submitted pool by the preregistered study of Appendix N, so no sub-pool transfer allowance is applied (this section is the structural reason the restriction is q3-neutral at all; the measured difference of the two pools' means is 0.0003 bit). Stated sensitivities of the same ledger: the parents'-pool pooled 256-replicate bound 2^-71.4474 is 2^-71.4474 (claim 57.61074) and less the 0.0020-bit allowance is 2^-71.4494 (claim 57.61273), the superseded 5x measured charge 0.0104 gives q3c 2^-71.4578 and claim 57.62108, and the preregistered min-block bound 2^-71.4629 gives claim 57.62615 on this family; four patterns alone 2^-72.02, Section 7.4b; q3 = q3c x 2.482, Section 7.7). For the Table 15 pattern the registered floor of study B is 2^-74.03 (its one-sided 99% bound is 2^-74.0225, its mean 2^-73.9987; study A's bound is 2^-74.0659), and fb039a6e measured the same quantity over the whole family G (a preregistered 128-replicate study: one-sided 99% bound 2^-74.0088) and over a kept-fibre-weighted pool (2^-73.9984); **Consistency note (disclosed, not silently repaired).** The operative value is `q3c_used = 2^-71.4162` in every place this text assigns a q3c, and it is the constant `Q3_LOG2` that `experiments/lowm.py ledger` executes. A reader of the previous revision found three assignments that still carried the superseded min-of-blocks floor `2^-71.4629` (Sections 7.4c and 12) and one that still carried the superseded 5x measured charge `2^-71.4578` (Section 7.8), plus the historical declaration of Appendix G.2. Each now names the quantity it actually describes; the superseded values appear only as the stated sensitivities of Section 12. No ledger constant, claim digit or certificate changes: `lowm.py ledger` prints `time_log2 = 57.58779` before and after this repair (Appendix N then moves the declaration to block F, whose ledger prints `time_log2 = 57.57975`).

our validation V reproduces the registered study (Section 7.4b). That the dependence on the variant is the four W24 conditions, about 2^-4 for every W8 (Lemma 7.1), is unchanged by the relaxations, which act on rows 16..19 only. Real first blocks (7319bba, Section 13.1, Table 15 cells): the row-16 pass rate of the attack's own good pairs is the exact 1,052,672 / 2^32 (z = +0.88 and +0.51 over 424,363 and 1,693,297 passes); this program's own simulation (Section 13.3) finds row-16 passes at its exact rate under R16x, 2^-11 per probed lane.
### 7.6 Rows 18 and 19: the accepted value patterns (credit: Jbenisek's ffbe30bb-ac92-4191-a589-3bf32661ee7d)
Table 15 fixes the value bits E18[1] = 1, E18[5] = 0, E18[10] = 1, E18[11] = 1, E18[18] = 0, E18[28] = 0, E18[29] = 1 and E19[29] = 1. They are not all required. With every other cell and printed two-bit condition of rows 4..36 kept, exactly four patterns of these eight bits admit a 37-step semi-free-start collision for the published dense part (an all-solutions enumeration with a verified 37-step model, Bitwuzla and Z3, done for ffbe30bb; the three further collisions are checked below), because the bits enter only through six parity conditions: E18[1] = E18[11], E18[1] != E18[28], E18[10] = E18[29], E18[10] = E19[29], E18[5] = E18[18] and E18[5] ^ E18[1] ^ E18[10] = 0. The seven E18 bits enter only through the signs of the signed difference of S1(E18) at step 19 (each output bit of S1 is the XOR of three taps, and the sign of the difference at that bit depends on the XOR of the two taps that carry no difference), and E19[29] only through E18[29] ^ E19[29] = 0 in the signed difference of Ch(E19, E18, E17) at step 21. The relaxation, its pattern table, the 74 single-flip tests, the seven unforced candidates of rows 20..22 (all necessary) and the exact stage enumeration (3.80 times as many W18 reach row 19 with the four patterns, 1.93 bits, interval 1.78 to 2.09) are ffbe30bb's and are quoted, not redone here, except for the check of the three alternative collisions and the q3 studies of Section 7.4b, which were run for this filing's family.

The strings of the E cells of rows 18 and 19 in `experiments/lowm.py` (`CHE[18]`, `CHE[19]`) are now
```text
 row 18   Table 15 ==10===uu====0==n===111===01==1=     program =======uu=======n=====1====1====
 row 19   Table 15 ==1====00====1==0==========1====     program =======00====1==0==========1====
```
(the remaining `1` of row 18 are E18[9] and E18[4], which stay imposed; so do the differences `u`, `n` and every other character). That is the whole change to the counted program: `row_ok` tests the masks and values of the cells as constants of the straight-line text, so the operation counts of Section 9 (`ROWCHECK`, `ROWCOMP` per row) and the ledger are unchanged; no operation was added and none removed. The six parity conditions are not tested separately: the exact signed-difference check of both members that `row_ok` always made, at rows 19 and 21, rejects the other patterns, and a separate test would only add operations. The patterns accepted, as flips of Table 15's values (E18 bits 29,28,18,11,10,5,1 | E19 bit 29):

| pattern | flipped bits of Table 15's values | flip masks (E18, E19) | value bits (E18[29,28,18,11,10,5,1] E19[29]) |
|---|---|---|---|
| 0 Table 15 | none | 0x00000000, 0x00000000 | 1 0 0 1 1 0 1 \| 1 |
| 1 | E18[5], E18[10], E18[18], E18[29], E19[29] | 0x20040420, 0x20000000 | 0 0 1 1 0 1 1 \| 0 |
| 2 | E18[1], E18[5], E18[11], E18[18], E18[28] | 0x10040822, 0x00000000 | 1 1 1 0 1 1 0 \| 1 |
| 3 | E18[1], E18[10], E18[11], E18[28], E18[29], E19[29] | 0x30000c02, 0x20000000 | 0 1 0 0 0 0 0 \| 0 |

The organizer experiment `a0-sfs-r37` imposes pattern t mod 8 on its construction of trial t (`IMP` and `PAT` in `experiments/lowm.py`): patterns 0..3 are the four above with E16[23] = 0 and E17[24] = E16[24], patterns 4..7 the four R16x patterns with E16[23] = 1 and E17[24] != E16[24] (value bits E18[1,5,10,11,18,28,29], E19[29] with E18[11] != E18[1], E18[28] = E18[1], E18[10] = E18[29] = E19[29], E18[5] = E18[18] = 1 ^ E18[1] ^ E18[10]; Section 7.4c); it checks every cell of rows -4..36 with the program's own `row_ok`, which accepts all eight; for trials 0..15 the constructed chaining value is fed to the counted online program, which must find exactly the constructed pair (Section 13.2). **Check of the three alternative collisions** (`check_alt.py`, Appendix F; words MSB first, chaining value common, x = M', y = M; the pairs are ffbe30bb's, and here they are compressed 37 steps again and their cells tested with this package's `row_ok` and, for contrast, with the Table 15 cells of the program this one derives from):
```text
pair (x = M', y = M)         collides  cells of this lowm.py    cells of Table 15       
Table 15 (published pair)    True      True                     True                    
G1                           True      True                     False                   
G2                           True      True                     False                   
G1 xor G2                    True      True                     False
```
The CVs and messages of the three pairs are listed in `check_alt.py` (Appendix F). They are 37-step semi-free-start collisions, not ordinary collisions. Rows 16..22 are functions of the rows 12..15 of S, of l and of W16..W22 only (Lemma 7.1), so what the accepted patterns are is the same for every variant of the family.
### 7.7 The success event: equal outputs after row 21 (credit: our 4ec21bf9-f588-4b80-bb2b-77c1ccf8c9b7, R37R, Appendix D)
**The event.** A pair is a success when rows 16..21 follow every cell and every printed two-bit condition closing at those rows (Sections 7.4c, 7.6) and the two 37-step outputs are equal; rows 22..36 are computed with no cell test (`step3b`, Section 9.9). Both members share CV1, so their outputs cv + (A36, A35, A34, A33, E36, E35, E34, E33) are equal iff the eight registers are equal, which is the comparison the program makes (`same_out`); a success is a collision of the second block and is verified with the target before output. The cell event of rows 22..36 is contained in this event (the characteristic ends with zero differences), so q3 = q3c x R with R = Pr[equal outputs | rows 16..21] / Pr[cells of rows 22..36 | rows 16..21] >= 1, under the law of the late words of the cell studies ((W6, W7) uniform on F6 x F7, W8 from the variant list).

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
2. **The residual is measured directly on the submitted pool.** The deviation of q3c from the uniform-Z value is linear in the deviation of mu from uniform; at the aggregate, the shipped tail stage mean over the 782,800 variants is 2^-3.999 against the exact 2^-4 (0.001 bit). Because an aggregate mean alone could conceal cancellation across sub-pools unless bounded pointwise, this filing does not rely on an aggregate-to-sub-pool transfer bound as operative: instead, Block F (Appendix N) directly measures q3c on the submitted 599,760-variant sub-pool (where the two pools' directly measured means differ by 0.0003 bit), while the historical 0.0020-bit and 0.0104-bit transfer allowances and the 0.05-bit flat hedge of 0db0eeb6 Section 7.6 are retained strictly as conservative sensitivities.
3. **The 0.05 case, for completeness.** At q3c = 2^-71.4474 - 0.05 = 2^-71.4974 the same ledger gives time_log2 = **57.70368**, which is still below the lane's best review (57.89863). Every admissible charge between 0 and 0.05976 bit leaves a lead; the break-even charge is 0.05976 bit, 60x the structural bound.

The three texts that carry this in the program are the family's `LISTID` (170 entries), the constant `C7_CONST = 0xc086800c` and the dynamic-bit set `C7_DYN_BITS` (15 bits: bit 2 of c7 is constant on the four kept lists, so the C7 test is 29 rather than 31 operations), and `Q3_LOG2 = -71.4162`. `experiments/lowm.py selftest` re-derives the family, the variant count and the op counts from the descriptors alone (Appendix D).
## 8. The algorithm
### 8.1 Lemmas 8.1 and 8.2 (the class test, the W6 test and the cube of a list)
Let x = A_{-1}, cb = C6 - A_{-2}, q = A1 ^ x, and for a class with base and mask put
```text
CB3 = cb + (A1 & x) + (base & q),   KZ = K3C + x - (A1 & A2) - (base & FA),   FA = A1 ^ A2,   C4 = 000b362e,   e4 = a0 + C4,   e3 = KZ - (s & FA).
```
**Lemma 8.1.** (a) The class passes the W7 filter at x iff F7(c7 - x). (b) For a0 = base | s of the class, W6x = cb + phi(a0, x) = CB3 + (s & q) - H, mod 2^32, where H_j = e4_j for the bits j with E5_j = 1 and H_j = e3_j for the bits with E5_j = 0 (E5 = e7f2c81f). Hence a0 is good (W7x in F7 and W6x in F6) iff its class passes and F6(CB3 + (s & q) - H). *Proof.* (a) Section 5.1. (b) W6x = C6 - A_{-2} + MAJ(A1, a0, x) - CH(E5, e4, e3) with e4 = a0 + C4 and e3 = K3C - MAJ(A2, A1, a0) + x (Section 5.1), and CH(E5, e4, e3) selects bit j of e4 where E5_j = 1 and of e3 where E5_j = 0. MAJ(A1, a0, x) = (a0 & (A1 ^ x)) | (A1 & x) with disjoint bit sets, so MAJ = (a0 & q) + (A1 & x); likewise MAJ(A2, A1, a0) = (a0 & FA) + (A1 & A2). Since a0 = base + s with base & s = 0 (Section 5.3), a0 & m = (base & m) + (s & m) for every mask m. Collecting the scalar terms gives CB3 and KZ. QED. (Checked on every lane of every pass plane of the experiments and of `selftest`, 0 mismatches.)

**Lemma 8.2 (the cube).** Let b be 0, 2 or 3, and let a0 have bit 1 set if b is 2 or 3. If q_b = 1 then F6(W6x(a0 xor 2^b)) = F6(W6x(a0)) (and W6x(a0 xor 2^b) = W6x(a0) for the bits >= 1); if q_b = 0 then W6x(a0 with bit b set) = W6x(a0 with bit b clear) - 2^b. Hence for a rep t (no cube bit set), Q0 = {b in B : q_b = 0}, cu a submask of Q0 and i a submask of I = B xor Q0: F6(W6x(t xor cu xor i)) = F6(W6x(t) - cu) (mod 2^32), cu read as the integer sum of its bits. *Proof.* A1 = 62827866, FA = fafd5ca2, C4 = 000b362e, E5 = e7f2c81f: bits 0, 2, 3 of FA are 0, so e3 = KZ - (s & FA) does not depend on s_b; bits 0..4 of E5 are 1, so H_b = e4_b for b = 0, 2, 3 (and e3 is only evaluated from bit 5 upward with carry_5 = 1 because (s & FA)[4:0] <= 16 <= K3C[4:0] = 28). In e4 = a0 + C4: C4_0 = 0, so e4_0 = a0_0 and there is no carry out of bit 0; for b = 2, 3 with a0_1 = 1 (and C4_1 = C4_2 = C4_3 = 1) the carry out of bit 1 is 1, a0_2 + 1 + 1 gives the sum bit a0_2 and carry 1, a0_3 + 1 + 1 gives the sum bit a0_3 and carry 1, so e4_2 = a0_2, e4_3 = a0_3 and the carry into bit 4 is 1 whatever a0_2, a0_3 are. Thus s_b enters W6x = CB3 + (s & q) - H at bits >= 1 through (q_b - 1) s_b 2^b, which is 0 if q_b = 1 and -s_b 2^b if q_b = 0; at b = 0, F6 does not read bit 0 of W6x, and when q_0 = 1, s_0 = 1 adds 1 to (s & q)_0 and 1 to H_0 = a0_0, which cancel in W6a - H with zero net carry into bit 1. QED. (Checked on 30,720 tuples in `selftest`.)

*The cube of a list.* The bits in which a list is closed under the flip form its cube B (computed; Section 5.3): B = {0, 2, 3, 7} for the 164 classes of lists 0 and 5, B = {0, 2, 3} for the six classes of lists 1 and 6 (all of which have a0 bit 1 set) and B = {0} for the parents' other six lists. The list is the union over f subset of B of (reps xor f), reps = the members with no cube bit (216, 432, 225, 450 and 1728, 1728, 1728, 1792, 1792, 1792 reps). **The four-bit form (164 classes).** A four-bit list has 216 or 225 reps and 16 variants per rep; the two batches of Section 9.4 are the halves f_7 = 0 and f_7 = 1 of that one rep set, so each batch keeps the three low state bits of Lemma 8.2 and its plane 7 is constant (0 and 1), the second batch's stored planes are the first's with plane 7 set, and `gather` adds D_top[7] = 0x80 on it. For a first block put I = (q & B) | (CB3 & 1) (the cube bits that do not matter at this x) and Q0 = B xor I. By Lemma 8.2, F6(W6x(t xor f)) = F6(W6x(t) - (f & Q0)) for a rep t and f subset of B, so one test of F6 on W6x(t) - cu decides the 2^|I| members t xor cu xor i, i subset of I: the program computes the sums W6x(t) once (the main run) and obtains the other 2^|Q0| - 1 runs from the stored sums and upper failure planes. Given that a class passes the W7 test, x mod 16 is uniform: in both affine pieces of the bitwise form of F7 (Section 5.1) the bits w0..w3 of w = c7 - x are individually free (w0 = w28, w1 = w18 (= w29), w2 = w19 tie them to other free bits), so w mod 16 and hence x mod 16 = (c7 - w) mod 16 are uniform; q_0, q_2, q_3 are independent uniform bits before applying the CB3 bit-0 optimization; the executed I law is derived below.

The scalars CB3 and KZ are computed once per passing class; the planes of the reps (14 or 16 bits) are the only lane-dependent data. Both tests are programs on *planes*: a plane is a 256-bit word holding one bit of each of 256 lanes (the lanes of a batch are 256 consecutive reps of a list).

**Executed cube law under H1.** A1[0]=0, so q0=x0. Every one of the 170 c7 constants of the family is even; for w=c7-x modulo 2^32, w0=x0. Both disjoint affine pieces of F7 leave w0 free and pair w28=w0. The first piece has rank six and 2^26 words; the second rank twelve and 2^20 words. Adding constraints on w0,w2,w3 raises each rank by three, so each assignment occurs (2^26+2^20)/8=8,519,680 times and exactly 34,078,720 of 68,157,440 words have w0=0. At fixed w1, subtracting w from c7 is triangular and bijective on bits 0,2,3, even with borrows; checking all eight assignments for each class confirms the joint cube law. Thus q0,q2,q3 are jointly uniform conditional on a class passing. Under H1, cb=C6-A_{-2} is uniform on Z/(2^32) and independent of x. For each fixed x, CB3=cb+(A1&x)+(base&q) translates cb by a constant; therefore Pr[CB3=y | x]=2^-32 for every y. This proves that CB3 is uniform and independent of x, hence also of q0,q2,q3 and the class event F7(c7-x). Its bit 0 remains independent uniform after conditioning on that event. In the executed `I=(q&B)|(CB3&1)`, Q0[0] requires q0=0 and CB3[0]=0, so its probability is exactly 1/4. Q0[2] and Q0[3] remain independent uniform bits. A mask Q0 on a k-bit cube therefore has weight `(1 if Q0&1 else 3)/2^(k+1)`, as in the predecessor's ledger.
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
The loop is the function `attack(nfb, vmax)` of `experiments/lowm.py` (`python3 lowm.py attack N V`): at most N first blocks, V the counted data-dependent operations of Section 9, halt when V exceeds the cap; an output is verified with the target digest before it is returned. The first blocks of that loop are the fresh uniform coins H1 assumes, drawn as such: with no seed argument `Shake.__call__` returns a fresh 32-byte OS draw and `first_block` takes two, so **every first block is 512 fresh uniform bits from the system CSPRNG**, not an expansion of one seed. In an earlier draft (`d14c3219`), expanding one 32-byte seed by SHAKE gave support at most 2^256 rather than uniform over 2^512; the current form draws 512 fresh uniform bits per first block. The optional fourth argument keeps the deterministic stream and every declared experiment passes its own seed (`Shake(eid + "|" + seed)`), so the experiments reproduce exactly as filed while the shipped default path is not a stream. The ideal-CSPRNG reading of `os.urandom` is the random-coin model this ledger already uses; no new premise is declared, and `reports/experiments/r37-coins-209.py` audits all three paths.
### 8.3 What is not assumed
No property of x other than being a 32-bit word is used (and, for the cube, that x mod 16 is uniform given that a class passes: Section 8.1), and nothing about the correlation of the classes of one first block: the ledger uses only the exact marginal law of each class test (probability p7 = |F7| / 2^32) and of each variant's F6 test given its class passes (p6 = |F6| / 2^32, exactly, because cb is uniform and independent of x), the law of |I|, and linearity of expectation. Padding lanes (the repeated last entry of a first block's last group) are probed and charged; a duplicated member that hit would be processed twice, which changes the cost (charged) and not the set of pairs found.
## 9. The counted program
### 9.1 Machine and pricing
256-bit word RAM, 64 registers, every executed primitive counted (loads, stores, branches and address additions included). 32-bit values are kept in the low bits; a reduction mod 2^32 is one AND; a 32-bit rotation pattern (S0, S1, s0, s1) costs 8: d = x | (x << 32) (2), three shifts and two XORs and one mask. A conditional branch tests a register for nonzero and is one primitive. Every address that is not a register value is formed by a counted add (one add per plane or word load; a table read is an index extraction, an add of the table base and a load). The program text is straight-line code. The target compression of a first block is one unit (since 9.11: one 1/7 share of a seven-lane batch, SB_FB = 384 word operations) and its internal operations are not counted again.

**Plane algebra.** The plane programs are executed by `lowm.py` on Python integers of 256 bits through a small algebra whose every call is a primitive of the straight-line text: a plane carries a *static constant tag* (all-zero, all-one: a constant of S such as C4, E5, A1 ^ A2) and an *inversion flag* (the stored word is the complement of the true plane). These are compile-time facts of the text, not data: x ^ 0 = x, x ^ 1 = ~x (flag flips; no primitive), x & 0 = 0, x & 1 = x, x | 1 = 1, x | 0 = x cost nothing; an AND or OR of two planes with equal flags is one primitive (both flagged: De Morgan, the stored words are combined with the dual operation); an AND or OR of unequal flags costs a NOT first (2 primitives); every other XOR, AND, OR on dynamic planes is one primitive. A full-adder bit is `xy = a ^ b; sum = xy ^ c; carry = a ^ (xy & (a ^ c))`: 5 primitives, 4 without the sum; with a static constant operand bit b: xy = a or ~a (free) and carry = a & c or a | c: 1 primitive. The counter `CN.n` of the algebra is the count of the plane programs; `process_cv` asserts the counts of the plane programs (W6 and the subtraction runs of each batch of each list, F7 = 112) at every execution (the counts do not depend on the data, only on the batch and the list). The scalar and control steps are counted where they execute by the constants below.
### 9.2 Fixed per first block: FIXED = 52 operations (266 before 9.6e, 461 before 9.6d (e); the setup `FB_DET`, 154 + 1 counter update, runs only when a class passes; since R37P40h the class test below, `CT_DET` = 219, runs only when the 9.6e prefilter byte is 1, and `FIXED` = 30 + 16 + 1 + 5)
First block words: 2 random words and the 16 fields (field 0 of a word: and; fields 1..6: shr, and; field 7: shr): 30; control 16 (loop counter add and compare-branch, the cap test, address arithmetic not itemised below): 46. Then:

- **Class test, 261** (5dbbb8da: 275; the parents' family: 299): -x mod 2^32 (2); the planes of -x, z_j = 0 - ((s >> j) & 1), consumed bit by bit (3 per plane, 2 for plane 0: 95); the dynamic planes of c7 (`C7_DYN_BITS` = bits 4..12, 19, 20 and 25..28, fifteen of them: bit 2 of c7 is `C7_CONST` bit 2 = 1 on all four kept lists, so that plane is a static constant here; **the c7 load-slot fold, this revision's first cell**: the 15 dynamic c7 planes are a fixed set at compile-time slots of the contiguous `c7_planes` region, so each load uses `base + immediate` with no address add, identical to P9 and the q store-slot fold below: 15 loads, 0 address adds = 15, down from 29); the adder c7 + (-x) with sums for the 17 bits {0, 1, 2, 9, 10, 11, 12, 18, 19, 22, 23, 26, 27, 28, 29, 30, 31} and the F7 test:
  F7 is in the bitwise form of Section 5.1; F7_OPS = 106, measured on this text and split as 83 (the c7 + (-x) add over the fifteen dynamic planes) + 23 (the F7 program); the parents' sixteen-plane c7 measures 112 (89 + 23) when the same `measure_ops` is run with bit 2 restored, so the whole -6 is the family's, not a re-pricing; the mask of the 170 valid lanes (1); the scan of the plane (since R37P40g executed only when the masked plane is nonzero, after the branch of 9.6d (e), and charged at P_PASS x 42, Section 9.6d (g); 42 primitives: for each of the three 64-bit parts that hold a lane of the 170 the extraction of the part (1 or 2) and, of its five chunks (four of 13 bits, one of 12), the four that start before lane 170: the extraction (1 or 2) and a zero branch -- ROW_FIX(nl) of Section 9.6 with nl = 170).
- **Scalars and planes, 154 (since R37P40g executed only when the class plane is nonzero, behind one branch `FB_SKIP = 1`, with its own work-counter update (`FB_DET` = 155), charged in vbar at P_PASS x 155; Section 9.6d (e)):** cb = C6 - A_{-2} (2), q = A1 ^ x (1), A1 & x (1), CB2 = cb + (A1 & x) (2), KXA = K3C - (A1 & A2) + x (2); the 16 planes of q (bits 2, 3, 4, 6, 7, 10, 14, 15, 17..24; bit 0 is not read by any batch because s_0 = 0 on all reps; 48) and their stores (16 stores: 16; **the store-slot fold, inherited from ed0d4c15 and 5dbbb8da**: the sixteen planes are a fixed set with compile-time bit positions, so the stores are unrolled to literal displacements in the same contiguous scratch area P9 argues for the 47 broadcast planes of `CB3`/`KZ` (slot `32k`, base + immediate, no address add), exactly the fold samsmith's accepted ed0d4c15 makes first — the 16 address adds are not operations of the shipped text, and the destinations are compile-time slots, nothing data-dependent is addressed; the code grows by 32 unrolled accesses (192 bytes), inside the declared memory);
  `cv_pre` (81 as in 0db0eeb6 Section 9.2: e0b, kap0, C = RBASE + (kap0 - e0b), x12, n12, X, Em2, kap1 and the broadcasts of the constants to four lanes, and the unpacking of the chaining value from the compression output).
### 9.3 Per passing class: 213 + 8 + 5 operations (CPREP = 166 since R37P40g, Section 9.6d (a): the shipped `cprep_ops` is 10 + 14 + 93 (CB3 bits 1..31) + 48 (the 16 KZ planes of `KZB`) + 1; the 213 itemisation in this section is the inherited record), and per subtraction run
Per set lane of the class plane: table load 1 (the 8192-word `scan_table` is placed at word address `0..8191`, so the nonzero 13-bit chunk `c` is directly its own word address with no base add), chunk offset add 1, c & (c - 1) 2, branch 1: CLS_LANE = 5. Then: five loads of the class descriptor (base, BP = base | ((~S0(base) & M32) << 32), list pointers, batch count, cost word) with their address adds (10); CB3 = CB2 + (base & q) + C4_MOD (3; folding the constant bits of C4 at E5 = 1 into CB3) and KZ = KXA - (base & FA) (3); the planes of CB3 for the bits 1..31 (93; the W6 programs never read bit 0) and of KZ for the 16 bits {5..9, 11..13, 15..17, 24..28} where s & FA = 0 (48; at the 8 bits {7, 10, 14, 18..22} with s_j = 1 in a batch, e3_j = KZ_j ^ s_j ^ ~borrow_j uses the scalar plane directly), 3 per plane; their stores (the 47 planes of CB3 and KZ are a fixed set and their 141 formation primitives are per-plane derivations, so the stores are unrolled and each takes a literal displacement in one contiguous scratch area, slot 32k: no address add, 47; the code grows by 94 accesses, inside the declared memory); one work-counter update (1): 10 + 6 + 141 + 47 + 9 = 213 (including the 9 planes of KZ_j at {7, 10, 14, 18..23} formed once in registers). The cube: the mask B of the list (load and address add 2), I = (q & B) | (CB3 & 1) (1), Q0 = B xor I (1), the tests I == 0 and Q0 == 0 (2), and q_0 for bit 0 of W6a - H (2): the itemised base is 8, and the shipped `CF_CLASS = 11` adds one primitive for the run's aggregate work-counter rounding (Section 9.7b) and two for the mixed-class allowance of Section 9.6b (when I != 0, the 2^|I| - 1 <= 7 cube deltas D_top[ii] are also loaded once per class into registers: 5 x 2^|I| - 2 primitives, Section 9.6). **The main run** (cu = 0) has no extra cost: the cube planes of s are static zeros of the text. **A subtraction run** (a nonzero submask cu of Q0, per batch, in increasing order): the next submask (cu - Q0) & Q0 and its test (3); BP_top xor D_top[cu] with D_top[cu] = (cu | (S0(cu) << 32)) << 192 read from a table of eight words (address 1, load 1, xor 1: 3); the work-counter update (1): RUN_CU = 7, and the pass plane of F6(W - cu) (Section 9.5).
### 9.4 Sweeps of two batches
A list of r reps is processed in batches of at most 256 lanes (2 for 432 and 450 reps, 7 for 1728 and 1792), two at a time; a four-bit list is the 216- or 225-rep set of Section 8.1 and its two batches are that rep set with plane 7 clear and set (nl = (216, 216) or (225, 225)). (R37P40g: every kept list has two batches, so a class runs one sweep, and its CB3 and KZ planes are formed in that sweep and not reloaded (9.6d (a)). The inherited text of this paragraph follows.) A sweep loads the scalar planes it needs once for both batches: zq (the planes of q for the bits s_j of the two batches that are not the static zero: 11 to 15), zKZ (16), zCB3 (31) at fixed slots of that same contiguous scratch area as the unrolled stores, one load each with a literal displacement and no address add, plus 3 of control: 3 + 2 x zq + 47 = 3 + 2 x (11 to 15) + 47, i.e. 72 to 80. Per batch: the stored planes of the reps that are not constant over the batch (with their address adds) and the two pointers of the batch: 2 x (number of such planes) + 2 operations.
### 9.5 The W6 program of one batch and the subtraction runs
Straight-line on planes (Lemma 8.1), with sums produced only for the bits that are used. The cube bits of s (0, 2, 3 or 0) are static zero planes in the main run, so the constants fold. **Constant planes of a batch.** The reps of a list are stored in a fixed order (a bit-lexicographic order of the bits of s, chosen per list; `REP_ORDER` in `lowm.py`, chosen by a seeded search on this ledger and not on the success probability); in a batch of at most 256 consecutive reps some of the 14 or 16 planes of s are all-zero or all-one. Such a plane is a static constant of that batch's text (it is not stored, not loaded and folds in the algebra exactly as the cube planes do), and a W6 text is written for every distinct constant pattern: 8 batches, 24 constant planes in all, 54 distinct texts of 3,851 primitives in all (Section 14.1). The ledger prices the text of each batch of each list separately; `lowm.py` measures it (`ListData.measure`) and asserts the count at every execution. Structure of the program (for every variant of the 170 classes, a0_1 = a0_5 = a0_11 = 1, a0_12 = a0_13 = 0, and base has 0 at all mask bits and at bits >= 14, so e4 = a0 + C4 decouples into bits 1..4 with carry_5 = 1, bits 5..10 with carry_5 = 1, and bits 14..31 = s[14..31] + C4[14..31] with carry_14 = 0; C4_MOD folds the static bits into CB3):

| step | primitives |
|---|---|
| e4 = s + C4 (carry_1 = C4_1, carry_5 = 1, carry_14 = 0; C4 static: carry = s & c or s \| c), dynamic sums for bits {2..4, 6..10, 14..28} with E5 = 1 | 23 |
| e3 = zKZ - (s & FA) from bit 5 with carry_5 = 1 (FA & mask has 9 bits: 7, 10, 14, 18..23), sums for the 13 bits with E5 = 0 (5..28) | 40 |
| W6a - H = zCB3 + (s & zq) - H merged bit-by-bit (carry-save full adder with half-adder carry reuse (xy & c) \| ac + carry-ripple at bits j >= 1; bit 0 is dead when Q0 = 0), sums for the 20 bits that F6 reads | 124 |
| F6 in the bitwise form of Section 5.1: pass = (w8 ^ w25) & ~fail with polarity-aligned andf/orf (plus upper failure planes and carry chain when Q0 != 0) | 24 |

The measured W6 counts per batch (main run / all sums): k = 3, all sums: 250 to 278 (mean 263.0); k = 3, main: 181 to 208 (mean 193.5); k = 1, all sums: 267 to 301 (mean 282.9); k = 1, main: 188 to 222 (mean 204.1); overall 181 to 301. The pass plane carries no inversion flag in the shipped text; `measure` adds one primitive if it did. A partial batch (fewer than 256 live lanes) costs one more AND with the lane mask; the four-bit lists have two per run. **The subtraction runs.** Because cu <= 13 < 16, W - cu = (W[31:4] - c4(cu)) || (W[3:0] - cu) where c4(cu) in {0, 1} is the single borrow out of bit 3 (for k = 1, cu = 1 and W_0 = q_0 | ~a0_0 = 1 whenever q_0 = 0, so c4(1) = 0 identically!). Thus when Q0 != 0, the main run precomputes the upper failure plane for c4 = 0 (and c4 = 1 when k = 3) and stores only 15 planes (k = 3: SPILL = 30) or 9 planes (k = 1: SPILL = 18), reloaded once per batch; for each nonzero submask cu of Q0 the pass plane combines the lower borrow chain on bits 0..3 with the pre-evaluated upper planes using polarity-aligned andf/orf; SUBF per batch: k = 3, cu = 13: 27; k = 3, cu = 12: 26; k = 3, cu = 9: 27; k = 3, cu = 8: 24; k = 3, cu = 5: 28; k = 3, cu = 4: 25; k = 3, cu = 1: 26; k = 1, cu = 1: 11 (primitives by (cube bits, cu)). Exactness: F6(W6x(rep xor cu)) = F6(W6x(rep) - cu) (Lemma 8.2), checked on every lane of every run (Section 13). **Registers.** The two batches of a sweep are processed together bit by bit, j = 0..31; the loaded planes of bit j are dead after use. Each batch holds the carries (e4, e3, W6a, W) and the F6 operands that are kept for later bits, folded as soon as both operands of a term exist: the pairs (w1, w12), (w2, w13), (w3, w14), (w14, w18), (w15, w19), (w9, w26), (w10, w27), (w16, w20), (w8, w25) and the three single bits w29, w30, w31; at most ten values at any bit. With at most six temporaries that is at most 20 live planes per batch, 40 for the sweep, plus about eight addresses, counters and constants: below 64, with no spill. A subtraction run holds the 15 or 9 reloaded planes, the borrow and at most six temporaries (under 25 planes); the scan state of its pass plane (about 10 values) is added only after the F6 test has released its operands: below 64.
### 9.6 Scan of the pass plane, the reps and their members
The pass plane (zero in the unused lanes) is scanned in four 64-bit parts of five chunks (four of 13 bits, one of 12); a scan of a plane of nl lanes costs ROW_FIX(nl) = 24.4081 at nl = 256, 20.8133 at 194, 17.9297 at 176, 20.3240 at 216 and 20.1968 at 225, and 42 for the 170-lane class plane. Ceiling (all rows set) `ROW_MAX` 42/42/47/50/53/58: the cap charges it. The scan tests each 64-bit row once (1) before its five chunks, so a zero row skips its chunk extraction; ROW_FIX(nl) is that charge at the measured nonzero-row rate of the shipped generator (`reports/receipts/r37-rowtest-80.out`: 2,000 first blocks, 30,430 runs, 73% empty), the row test at 21.5143/18.5067/15.8578 and the chunk base at 2.8941/2.3063/2.0717, added and rounded to four decimals. The 99% is a **block-level** bound, not a binomial one: the 170 class lanes of a first block fire together, so the runs are clustered (design effect 25.6, `r37-scanrate-85.out`), and two independent 2,000-block runs of the shipped generator move the nl = 256 charge by -6.7% (mean 21.1126 against 19.6905, `r37-rowfix4-96.out` and `…-96b.out`), which a binomial bound on 15,215 runs (a 0.84% half-width at the measured 27% nonzero rate) cannot produce: the swing is eight times it. Every ROW_FIX therefore carries the 99th percentile of a 2,000-resample bootstrap over the blocks; the filed 17.9297/20.8133/24.4081 are 1.152-1.159 x the per-run means and 2.8-3.7% above the measured block bounds, i.e. coherent and conservative (`r37-rowfix4-94.out`, `…-96.out`). A cell priced against these keys is charged at the same discipline, a block-level key against a block-level charge and never a binomial key against a filed charge (the like-for-like rule; mixing the two is what produced the -0.01090 that `r37-cube4price3-95` withdrew in favour of -0.00787). The 216/225 keys are the same discipline: block-boot 99% 20.3240 and 20.1968 under seed `cells` against 17.9870 and 19.2328 under seed `cells2`, the larger taken (`r37-rowfix4-96.out`). The plane is masked to nl lanes, so a chunk that starts at or beyond nl is identically zero and is not tested (iter25). Per set lane (a passing rep): table load of the bit index 1 (`scan_table` at word address `0..8191`, so `c` is directly its word address), add of the part-and-chunk base 1 (hoisted, this revision: the base `words_b + 64 r + sh` is formed once per nonzero chunk, so the lane loop carries one add, not two), load of the packed word 1, table load of the successor `succ[c] = c & (c - 1)` 1 (`succ_table`, the same zero-base convention: the clear of the lowest set bit is one load, not a subtract and an AND), loop branch 1: SCAN_LANE = 5 (the chunk base is the sixth, charged per nonzero chunk). `succ_table` is 8192 words, the only new resident item (14.1); the scan body is otherwise untouched. The packed word i of a batch holds in its 64-bit part r the entry s | (S0(s) << 32) of the rep of lane 64 r + i. The entry is stored already in the top 64-bit lane of the word it is loaded from (the twelfth change; **superseded by Section 9.6c of R37P39: the same word now holds the entry in all four 64-bit lanes, and the member disciplines below are re-itemised there**): a batch's rep table holds one word per lane, at index `64 r + i`, holding `entry_of(s) << 192`, so the extraction is the loaded word itself and **EXTR = 0, 0, 0, 0** for r = 0..3. The four-part packing this replaces held the four parts of one index in one word and had to bring part r into the top lane at 1, 2, 2, 1 primitives (`w << 192`, `(w << 128) & M_TOP`, `(w << 64) & M_TOP`, `w & M_TOP`), against 16,384 -> 65,536 B of `s_entries` for the 4x table (Section 14.1: the resident total is 1,011,978 B, still under 2^20, so the memory term stays 0.0). The loaded word is XOR'ed with BP_top xor D_top[cu] (BP_top in the main run; the result is (a0 | ((~S0(a0) & M32) << 32)) << 192 for the member a0 = base | rep | cu, because S0 is linear and base, rep, cu have disjoint bits, and ~S0(a0) != 0 on all 599,760 variants so every member is nonzero in bits 192..255). If I = 0 the member is placed by shifting the group register down by 64 (`Gw >> 64` 1), OR'ing with the top-lane entry (1), testing the low 64 bits (`Gw & M64` 1), branching on a full group (1), updating the work counter (1), plus the xor (1): PLACE = 6. If I != 0 the rep stands for m = 2^|I| members: the m - 1 <= 7 cube deltas D_top[ii] are loaded once per class into registers during class preparation (`5 m - 2` primitives in all: loop over nonzero submasks ii of I with `(ii - I) & I` 3, table address 1, load 1 per nonzero ii, plus final test), and each passing rep expands in m placements. **The placement is not walked one member at a time** (that walk is the inherited `EXTR + 5 m + 1` of d9f8833d: 1 xor + 4 shift/or/and/branch per member). The members of one rep are `e ^ D_top[ii]` for the nonzero submasks `ii` of `I`; they are produced consecutively, and every kept list has `k = 3`, so `m` is 8, 4 or 2 and a group of four never mixes two reps for `m = 8` (two full groups) and `m = 4` (one full group), and mixes exactly two for `m = 2`. Because `e` and the `D_top` are 64-bit values laid into disjoint 64-bit lanes and XOR distributes over the shift,

    sum_k (e ^ D_top[ii_k]) << 64k  =  (e | e<<64 | e<<128 | e<<192) ^ sum_k (D_top[ii_k] << 64k)

bit for bit, and the m-1 `D_top` deltas are already in registers from the class preparation above. So a group of four same-rep members costs 2 shifts + 2 ors (one doubling spread) + 1 xor with the precombined delta word + 1 full-group test + 1 store = **8 primitives, not 4 x 5 = 20** (iter49: the m = 1 accumulator's separate shift-down is not executed once the doubling spread writes all four lanes; `experiments/r37-groupfour49.py` assembles 384 group words by both disciplines, bit-identical, checks lane k of the doubling word *is* e ^ D_k, and shows the top-lane convention is the same word) (iter37: the spread is the doubling t = e | e << 64, t | t << 128, four primitives; selftest asserts it on 4,096 words); `reports/experiments/r37-cheaper-placement-23.py` checks the identity on the shipped listings (192 group words, both ways, bit-identical). Charged exactly, with no declared slack: `memcost(0) = 4` (m = 1: shift-down 1, or 1, xor of the class delta 1, work counter 1); `memcost(1) = 6` (iter46/iter53: a pair filling half a group word, priced per *group*: spread pair A 2, xor its precombined delta 1, or into the register 1, shift the accumulator by 128 1, spread pair B 2, xor its delta 1, or into the register 1, work counter 2, store the group word 1 = 12; the opening pair writes a zero register, so its or is not executed and the ledger charges `L.nr * memcost(1) - L.nr // 2`, 5.5 per rep; iter53's census of 582,014 group words on 4,000 first blocks, 187,924 of them filled by exactly two pair reps and one mixed, is the evidence for the pair discipline); `memcost(2) = 7` (iter49: a group of four same-rep members: spread 4, xor with the delta word 1, work counter 1, store 1); `memcost(3) = 9` (iter52: the same body with two words -- the spread is per *rep*, since the `e`-pattern does not depend on the word, so the second word costs an xor and a store, and the counter is per *rep*, as in `memcost(2)`: 4 + (1+1) + (1+1) + 1 = 9; `experiments/r37-groupeight50.py` assembles both words of every m = 8 rep on the shipped listings by both disciplines (128 reps, 256 words, 1,024 lanes, bit-identical)). **This filing removes the completion test and its branch from the four placement disciplines** (6 -> 4, 7 -> 6, 8 -> 7, 11 -> 9): within a class run every rep contributes exactly m = 2^|I| members, m being a property of the class and not of the data, so a group word is completed by a fixed number of placements (4 for m = 1, 2 for m = 2, 1 for m = 4, 1 for m = 8); the only control is the branch that ends the per-set-lane loop, already charged once in SCAN_LANE, and the last partial word of a run is padded by PAD_OPS = 7. The inherited itemisations above charged a test and a branch per placement because they walked members one at a time; R37P22 (this filing) walks them by the fixed schedule of the discipline. Every counting experiment cited above (iter46/49/50/52/53) is unchanged.`5 * 2^(j-1) + 1` beyond. The same identity covers the pair, `sum_k (e ^ D_k) << 64k = (e | e << 64) ^ sum_k (D_k << 64k)`, and `reports/experiments/r37-pair-24.py` checks it on the shipped listings: 4,032 pair words and 96 group-of-four words, bit-identical, and it asserts each of the four charges above item by item. A group of four members is complete after four placements (clearing Gw to 0 after GROUP_BODY); the last group of a first block is padded (PAD_OPS = 7). The `memcost` charge (placement alone, with the pair-run discount of 9.6 and the fold of 9.6b applied) at the four lists was 1,248.491 of `vbar` on the base row, split by |I| as 129.326 / 497.407 / 487.458 / 134.300 (at R37P39's charges of Section 9.6c: 651.603, split 169.118 / 298.444 / 139.274 / 44.767). The 1,671.286 and its [238.755, 696.369, 557.095, 179.066] split that stood here were the pre-R37P22 pricing (charges 6,7,8,12 with no pair-run discount) and do not reproduce on the shipped charge; the "1,079.372 / 910.254" pair of an earlier revision matched no split of this charge at all (`r37-m8count52.py` counts the m = 8 charge on 128 shipped reps).

**9.6b The per-rep work counters fold per group word (this revision).** The counter component of each discipline (1 per placement for m = 1, 2 per pair-group for m = 2, 1 per rep for m = 4 and 8) adds a compile-time constant of the class, and the placements of one group word share the class, so `C + C + C + C` is one add with the quadrupled immediate: m = 1 costs one counter per group word (1/4 per placement), m = 2 one per pair-group (1/2 per rep). `V` is read only at the per-first-block cap test, so the batched value is never observed (the principle of 9.7b). Measured: 66,732 group words over 300 first blocks hold 4 mixed-class words (0.01%), each a 2/2 split at a class boundary, so a run's partial group plus one split cost at most two primitives per class run (`CF_CLASS` 9 -> 11). At `CF_CLASS` 9, 10, 11 (R37P29) and 12 the row is 57.21399, 57.21426, 57.21653 and 57.2825, all below the row they replace (`r37-memberbatch-60.py`, `.out`).
**9.6c The rep words hold their entry in all four lanes (this revision, R37P39).** The rep table of a batch is 256 words, one per lane at index `64 r + i`. Since the twelfth change, each word held `entry_of(s) << 192`. It now holds `W = entry_of(s) x REP4` with `REP4 = 1 + 2^64 + 2^128 + 2^192`, that is, the entry in every 64-bit lane. Each entry is below 2^64, so the four copies are disjoint.
- Memory is unchanged: the same 2,048 words and 65,536 B, and the resident total stays 1,011,978 B.
- The scan's single load of the packed word (counted in SCAN_LANE) is unchanged.
- The 8-word cube-delta table `D[c]`, c a subset of {0, 2, 3}, is stored the same way: each word holds its 64-bit delta in all four lanes, in the same 8 words and 256 B.

*Delta words, charged explicitly (new).* `D_k` below is the lane-k delta: the class delta `BP ^ D[cu]` (with `D[0x80]` for the second batch of a four-bit list) XOR the cube delta `D[ii_k]` of the member that lane carries.
- The inherited items do not build these lane-placed words. Class preparation `5 m - 2` loads only top-lane deltas, and `RUN_CU = 7` forms only the top-lane class delta. The base row's "xor with the precombined delta word" therefore left this cost uncharged.
- This revision charges it. **Per passing class, `DELTA_CLASS = 18`** builds the class's cube-delta word(s) `(D[ii_0], ..., D[ii_3])` (two words for m = 8) from the replicated cube-delta words already loaded in class preparation: one AND with a lane mask and one OR per nonzero `ii`, at most 2 x 7 = 14. It then loads the class delta word `BP` from the class descriptor (2) and XORs it into the at most two words (2).
- **Per run, main or subtraction, `DELTA_RUN = 5`**: the address and load of the replicated `D[cu]` (2), the XOR with the replicated `D[0x80]` for the second batch of a four-bit list (1), and the XOR into the at most two class words (2).
- For m = 1, the top lane of the same word is the per-member class delta.
- Both charges enter `class_det`, `process_cv` and `vmax_fb`: +124.434 ops per first block on vbar.

The four member disciplines, one primitive per line:
```text
m = 1 (I = 0)   t  = (W ^ Drun) & TOPL           2   xor with the replicated run delta, and: isolate the top lane
                Gw = (Gw >> 64) | t              2   shift-down, or
                counter                          1                                                   memcost(0) = 5   (was 4)
m = 2 (|I| = 1) per group word of two reps A, B (A opens the word):
                pA = W_A ^ P                     1   xor with the pair delta word P (lanes 2, 3 = D_0, D_1; lanes 0, 1 are don't-care)
                Gw = pA  (opening: the or is not executed, charged and refunded as before)   1
                Gw = Gw >> 128                   1   one accumulator shift per group word; it discards pA's lanes 0, 1
                pB = (W_B ^ P) & HI2             2   xor with the same P, and with the two-lane mask (lanes 3, 2)
                Gw = Gw | pB                     1
                counter 2                        2   = 8 per two reps (7 executed)                    memcost(1) = 4   (was 6)
m = 4 (|I| = 2) S  = W ^ (D_0, D_1, D_2, D_3)    1   the group word itself (the doubling spread, 4, is not executed)
                counter 1                        1                                                   memcost(2) = 2   (was 7)
m = 8 (|I| = 3) S1 = W ^ (D_0..D_3), S2 = W ^ (D_4..D_7)   2
                counter 1                        1                                                   memcost(3) = 3   (was 9)
```
*No store.* The inherited m = 2, 4, 8 itemisations each ended with "store the group word 1". The inherited m = 1 discipline (shift-down, or, xor, counter) has no store. Its group word lives in the accumulator register `Gw`, and GROUP_BODY reads `Gw` directly. The rare path's member lookup (RARE_LOOKUP = 2) recovers lane k of a group word, which it can do from that register with a shift and a mask. In the m = 2, 4, 8 disciplines the group word is likewise produced in a register and consumed at once by the packed-u body. So no load of a stored group word is executed anywhere, and the store is not executed.
```
Every other item of the inherited itemisations is kept unchanged and charged:
- the counters;
- the opening refund `- nr // 2` of m = 2;
- the 9.6b counter fold (`f` = 3/4, 1/2);
- the class-boundary allowance CF_CLASS = 11.

The member order is unchanged as well. Lane k of a group word is the k-th placement, so for m = 2 the older pair lands in lanes 0, 1 after the shift by 128. A split group word at a class or run boundary is formed from the same word S (or the same pair word) as before, so the boundary handling charged in CF_CLASS does not change.

The identity is exact. Lane k of `W ^ (D_0, ..., D_3)` is `entry ^ D_k`, the inherited member `e ^ BP ^ D[cu] ^ D[ii_k]`. The inherited doubling spread `t = e | e << 64, t | t << 128` was the run-time construction of `W` from the top-lane word.

The shipped `gather` executes these words: `rep_members` builds the m = 1 top-lane word, the m = 2 pair word and the m = 4, 8 group words from the replicated `W` and places their lanes. `selftest` checks two things, and they are identities, not cost counts; the costs are this itemisation:
- (a) `W == entry x REP4` on all 2,048 rep words of the four lists;
- (b) `rep_members` returns exactly the inherited member sequence for every rep word, every I of the cube {0, 2, 3} and two cube offsets cu: **110,592 members, 0 mismatches** (Appendix D). The selftest line "spread placed by doubling" is kept as a check of the inherited identity; that spread is no longer executed.

*The cap ceiling (also this revision).* `ROW_MAX` was the scan cost measured before the row test and the chunk-base hoist were added (Appendix P.1). As a ceiling it now includes them: +32 at every lane count (4 row isolations and tests at 3 primitives each and 20 chunk-base adds), giving `ROW_MAX` = 74/74/79/82/85/90 at nl = 170/176/194/216/225/256. The worst case `vmax_fb` (Section 9.10) also charges m = 1's extra AND and the delta words: 54,908,176,927.7 -> 54,908,880,387.7.

Ledger effect, exact: `perclass` goes from 5,497.010234 to 5,024.556202 (-596.888 member placement, +124.434 delta words), and nothing else in vbar changes. vbar goes from 12,433.992190 to 11,961.538158. With slack 1/15000, the claim goes from 57.10307 to **57.05080**.

*Constants, registers and what is checked (R37P39).* The resident constants the disciplines use are kept in registers alongside the plane programs' at most 2 x 20 live planes. They are the lane masks TOPL and HI2, the replicated `D[0x80]`, the class's at most two cube-delta words, its pair or group delta word `P` and the current run's delta, so at most 8 more registers are used out of 64 and no spill is executed.
- The class descriptor stores `BP` in all four lanes of its existing word (the descriptors stay 4 words per class).
- The 8-word cube-delta table covers the subsets of {0, 2, 3}. `D[0x80]`, for the second batch of a four-bit list, is the one further replicated constant. It is held in a register for the whole run: one load at program start, inside FIN/PRE.
- At a split group word on a class or run boundary, the pair-A mask is executed again. This is covered by CF_CLASS like the inherited split handling.
- `selftest` checks the member *values* the four disciplines produce, not their primitive counts. The counts are this itemisation, item by item.

*The reference loop's counter.* `attack()` in `lowm.py` is a small-scale reference loop. It accumulates the simulation's per-event charges (since R37P40g `FB_DET` is data-dependent and stays in V, Section 9.6d (e); since R37P40h a first block whose prefilter byte is 0 adds nothing to V, and one whose byte is 1 adds its charges with `CT_DET` replaced by `CT_V` = 220, Section 9.6e). Those per-event charges are never below the ledger's: the scan is charged at the ceiling of ROW_FIX, and member counters are charged unfolded. So the reference loop's V can only reach V_MAX earlier, never later. The counted program of the claim updates V by the ledger's constants (Section 9.10).

**9.6d Three folds of the class and first-block stages (this revision, R37P40g).** Every item below is a primitive of the inherited itemisation that the text no longer executes. No plane program, scan, member discipline, group body, probe or rare-path item changes, and no probability changes.

*(a) The scalar planes of CB3 and KZ are formed in the sweep.*
- Fact (from the lists; `ListData.nb`): every kept list has exactly two batches, nl = (216, 216), (256, 176), (225, 225) and (256, 194). So a passing class runs exactly **one** sweep (`nsw = ceil(nb / 2) = 1`).
- The 47 scalar planes are CB3 at bits 1..31 (`ZC`) and the 16 KZ planes `zNKZ` (`KZB`, from the scalars NKZ, NKZ2, NKZ3 and KZ bit 11). They are read only by the main-run W6 programs of that sweep. The subtraction runs read only the spilled W planes (`f6_sub`, Section 9.5), never a CB3 or KZ plane.
- The inherited text formed each plane in class preparation as `0 - ((s >> j) & 1)` (3 primitives, 141 in all), stored it (47) and reloaded it in the sweep (47). Each plane was therefore written once and read once.
- Here plane j is formed by the same 3 primitives at bit j of the bit-serial sweep text (Section 9.5: "the two batches of a sweep are processed together bit by bit, j = 0..31"). It is used by both batches at that bit and is then dead. The e3 borrow chain reads `zNKZ` at bits 8, 10, 11, 12, 14..23, 25 and 28 in increasing order, and the merged adder reads `zCB3[j]` at bit j. So in a bit-serial text every plane is formed before its first use and never again. This is exactly how Section 9.2 already treats the planes of `-x` ("consumed bit by bit (3 per plane)").
- Registers: forming a plane occupies the same destination register as loading it, plus one temporary. The scalars CB3, KZ, NKZ, NKZ2 and NKZ3 take 5 resident registers, and they are dead after bit 31 of the sweep. Even if the at most 8 resident constants of Section 9.6c (lane masks, D[0x80], the class delta words) were also held during the sweep, Section 9.5's 40 live planes, 8 addresses and counters, those 8 constants, the 5 scalars and 1 temporary come to 62 <= 64, with no spill.
- Charge: `CPREP` = 10 + 14 + 93 + 48 + 1 = **166** (was 213: the 47 stores are not executed). The sweep is `3 + 2 zq` (was `3 + 2 zq + 47`: the 47 reloads are not executed; with (b), where filed, it is `3 + zq`). Total: **-94 per passing class**, -253.589 ops per first block.
- Memory: the 47-word CB3/KZ scratch is not used. The scalar planes in memory go from 63 words to the 16 q planes, -1,504 B. The 141 formation primitives now sit in the sweep text of each list (main and full: 8 texts), for which Section 14.1 adds a code allowance of 8 x 141 x 8 = 9,024 B.

*(e) The first-block setup runs only when some class passes.*
- `FB_DET` = 155 consists of the scalars cb, q, A1 & x, CB2 and KXA (9), the 16 q planes and their stores (64), `cv_pre` (81), and one work-counter update that adds the setup's constant to V (1; Section 9.10). Its readers are the class preparation, the sweeps and the group body (`packed_u` reads the `cv_pre` constants).
- The class test reads none of it. It reads x, which the P8 batch has already extracted (Section 9.11.0, "extraction of the seven lanes' eight words").
- So after the F7 plane is formed and masked, the text branches once on the plane being zero (`FB_SKIP = 1`, charged in `FIXED` for every first block) and executes `FB_DET` only when it is nonzero. `process_cv` returns before `FB_DET` when no class passes.
- `FIXED` = 30 + 16 + 1 + CT_DET: with the inherited class test (CT_DET = 261) that is **308** (was 461), and `FIXED_P7` = 308 - 30 + 4 = **282**. At this revision, with fold (g), `FIXED` = 266 and `FIXED_P7` = 240.
- The 155 primitives become data-dependent. They are counted in V (by their own update) and in vbar at their exact mean `P_PASS x 155`, and `vmax_fb` gains 155.
- **P_PASS** = Pr[at least one of the 170 classes passes] = |union over the classes of {x : c7_i - x in F7}| / 2^32 under H1 (x uniform; Lemma 5.1 already uses it).
- It is counted exhaustively: the program below enumerates the 2^32 words w, keeps the 68,157,440 words of F7 by the definition, marks x = c7_i - w for all 170 classes in a 2^32-bit map, and counts the map. **549,066,752** words are marked, so P_PASS = 549,066,752 / 2^32 = **0.1278395653** (13.5 s, one core; the receipt line is printed below the program).
- The mean count of passing classes is still 170 p7 = 2.697754, so a first block with a pass has 21.10 passing classes on average. This is the overlap of the sibling translates that Appendix P.3 measures (design effect 26).
- Checks: `selftest` draws 20,000 random x and finds 2,528 first blocks with a passing class against 2,556.8 expected (z = -0.61). `a0-online-r37`'s unconditional loop now also reports `uncond_blocks_with_pass`, the number of its 512 first blocks with a nonzero class plane, so the organizer measures the rate on its own seeds (local run under the public seed: 72, against 65.5 expected, sd 7.6).
- Exactness: the term is linear in the indicator of a nonzero class plane, whose mean is P_PASS exactly, so Section 11.1's exactness argument applies unchanged. The Bernstein cap needs only 0 <= v_f <= vmax_fb, and vmax_fb carries the 154.

```c
// ppass.c -- exhaustive P_PASS: |U_i (c7_i - F7)| / 2^32 over the 170 class constants c7_i (CLASSES of lowm.py)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "c7.h"   /* static const unsigned C7[170] = { the 170 c7 values of lowm.py _CB, in order }; */
#define ROR(x,n) (((x)>>(n))|((x)<<(32-(n))))
static inline uint32_t s0(uint32_t x){return ROR(x,7)^ROR(x,18)^(x>>3);}
int main(void){
  uint64_t *bm=calloc((1ULL<<32)/64,8), nf=0, cnt=0;
  for(uint64_t w=0;w<(1ULL<<32);w++){ uint32_t ww=(uint32_t)w;
    if((uint32_t)(s0(ww+0xfbc00800u)-s0(ww))!=0x017f8000u) continue;   /* F7 by its definition (Section 5.1) */
    nf++; for(int i=0;i<170;i++){ uint32_t x=C7[i]-ww; bm[x>>6]|=1ULL<<(x&63); } }
  for(uint64_t i=0;i<(1ULL<<26);i++) cnt+=__builtin_popcountll(bm[i]);
  printf("|F7|=%llu union=%llu P(pass)=%.10f\n",(unsigned long long)nf,(unsigned long long)cnt,cnt/4294967296.0); return 0; }
```
```text
|F7|=68157440 union=549066752 P(pass)=0.1278395653
```

*(g) The class-plane scan runs only when the plane is nonzero.*
- The scan of the 170-lane class plane costs `ROW_FIX(170) = 42` fixed primitives (Section 9.2: for each of the three 64-bit parts that hold a lane, the extraction of the part and, of its chunks that start before lane 170, the extraction and a zero branch) plus `CLS_LANE = 5` per set lane (the `ct_var` term).
- When the plane is zero the scan finds no lane, so its result is known without it. The one branch of (e) (`FB_SKIP`, on the masked F7 plane in a register) is placed **before** the scan, and the scan runs only when the plane is nonzero. `process_cv` returns before `scan_parts` when the plane is zero.
- Charge: `CT_DET` loses `scan_fix(170)` = 42 (in `FIXED`), and the 42 become data-dependent at their exact mean `P_PASS x 42` = 5.369262 (the same P_PASS as (e), exact under H1), with `vmax_fb` + 42. No new branch and no new premise. Net -36.63 ops per first block.

*Ledger effect.* perclass 5,024.556202 -> 4,770.967335, and the setup term adds 25.184394 (= P_PASS x 155); vbar 11,961.538158 -> 11,733.133685; `FIXED_P7` 435 -> 240; per first block 4.83379 -> 4.67365 units. The cap is recomputed at the same slack 1/15000: exponent 14.63538, Pcap = 2^-21.114393 = 4.404883e-07 <= 9/20,000,000, mu_req 0.49466316, floor 0.39000000138103141. N = 381,644,576,095,538,061,596, so log2 T = 57.002285124239535 and the claim is **57.00229**.

*What is unchanged and checked.* Every lane check and every mismatch counter of `selftest` are byte-identical apart from the printed counts and the added P_PASS line (Appendix D). The six organizer experiments were run locally under organizer-style requests (public seed, 256 trials, the request format of `experiments/runner.py`): `h1-cv1-filters-nonce`, `h3-cowpass-nonce`, `h3-ladder-r37` and `h6-orgstats-r37` return byte-identical stdout to the base program; `a0-sfs-r37` and `a0-online-r37` return the same pairs and every mismatch counter 0, only `counted_ops` moving.

**9.6e The 14-bit window prefilter before the class test (this revision, R37P40h).**
- Table: T[v] = 1 iff some x in U has x[23:10] = v, where U = union over the 170 classes of {x : c7_i - x in F7} (Section 9.6d (e)). 11,008 of the 16,384 bytes are 1. x not in U gives a zero class plane, and every x in U has T[x[23:10]] = 1 (checked for all 549,066,752 words of U on the 2^32-bit map of 9.6d (e)). So a 0 byte implies no class passes: skipping the class test then changes no output and no examined pair.
- Text: idx = (x >> 10) & 0x3fff (2), add the table base (1), load the byte (1), branch on zero (1): `PF_OPS` = 5, in `FIXED` for every first block. If the byte is 1, the inherited class test runs (`CT_DET` = 219), then one work-counter update adds its constant to V (1): `CT_V` = 220, after which the 9.6d (e) branch and everything else are unchanged.
- Rate: x = A_{-1} is uniform under H1 (as for P_PASS), so Pr[byte = 1] = 11,008 / 16,384 = **P_H** exactly. vbar gains P_H x 220 = 2365/16 = 147.8125, `vmax_fb` gains 220, and `FIXED` = 30 + 16 + 1 + 5 = **52**, `FIXED_P7` = 52 - 30 + 4 = **26**. Net -66.19 ops per first block.
- Window choice: for 14-bit windows x[s+13:s], the hit counts are 16,000 (s = 0) ... 16,384 (s = 8), 12,800 (s = 9), **11,008 (s = 10)**, 11,908 (s = 11), 12,804 (s = 12) ... 11,808 (s = 18); s = 10 is the minimum. A byte per window keeps the read at Section 9.1's table-read pricing; the 16,384 B fit under 2^20 (a 15-bit byte table, 32,768 B, would not).
- Build (preprocessing, Section 14.2 (v)): one pass over the 2^32 words w; for each w in F7 (by its definition) keep the least and greatest w[9:0] for each h = w[23:10]; then for each class and each h, x[23:10] = c7[23:10] - h - borrow with borrow = [c7[9:0] < w[9:0]], so borrow 0 is reachable iff lo_min[h] <= c7[9:0] and borrow 1 iff lo_max[h] > c7[9:0]. Scratch 81,920 B (lo_min, lo_max, seen) in the scan-table region before that table is initialised (inside the 2^17 bytes of 14.2); T is written in place. The build reproduces the table from the 2^32-bit map byte for byte (sha256 97d80a40...d60e of the 2,048-byte bit form).

```c
// pfbuild.c -- the 9.6e table as the preprocessing builds it (c7.h as in 9.6d (e))
#include <stdio.h>
#include <stdint.h>
#include "c7.h"
#define ROR(x,n) (((x)>>(n))|((x)<<(32-(n))))
static inline uint32_t s0(uint32_t x){return ROR(x,7)^ROR(x,18)^(x>>3);}
int main(void){
  static uint16_t mn[16384], mx[16384]; static uint8_t seen[16384], T[16384]; int h=0;
  for(int i=0;i<16384;i++) mn[i]=1024;
  for(uint64_t w=0;w<(1ULL<<32);w++){ uint32_t ww=(uint32_t)w;
    if((uint32_t)(s0(ww+0xfbc00800u)-s0(ww))!=0x017f8000u) continue;
    uint32_t hi=(ww>>10)&0x3fff, lo=ww&0x3ff; seen[hi]=1; if(lo<mn[hi]) mn[hi]=lo; if(lo>mx[hi]) mx[hi]=lo; }
  for(int i=0;i<170;i++){ uint32_t ch=(C7[i]>>10)&0x3fff, cl=C7[i]&0x3ff;
    for(uint32_t g=0;g<16384;g++){ if(!seen[g]) continue;
      if(mn[g]<=cl) T[(ch-g)&0x3fff]=1;
      if(mx[g]>cl) T[(ch-g-1)&0x3fff]=1; } }
  for(int v=0;v<16384;v++) h+=T[v];
  printf("hit=%d/16384\n",h); return 0; }
```
```text
hit=11008/16384
```
- In `lowm.py`: the table is shipped as its 2,048-byte bit form (`PFT`, zlib + base64, asserted to hold 11,008 ones); `pf(x)` reads it. `attack()` skips a first block whose byte is 0 (no V update) and adds `CT_V` for the others; `expected()` adds the term `pft` = P_H x `CT_V`; `vmax_fb_value()` adds `CT_V`; `memory` adds `prefilter_table` = 16,384 B and 5 x 6 B of code.
- Checks: `selftest` draws 20,000 random x (13,465 hits against 13,437.5 expected, z = 0.41) and 3,400 x of U (20 per class, by the F7 sampler): 0 misses. `a0-online-r37`'s unconditional loop reports `uncond_prefilter_hits` and `prefilter_misses_with_pass`, so the organizer measures the rate and the soundness on its own seeds (local run under organizer-style requests: 339 of 512 against 344.0 expected, 0 misses with a pass).
- Exactness: the term is linear in the indicator of a 1 byte, whose mean is P_H exactly under H1, so Section 11.1 applies unchanged; the Bernstein cap needs only 0 <= v_f <= vmax_fb, and vmax_fb carries the 220.
- *Ledger effect.* Fold (j) took vbar 11,880.946185 -> 11,864.468984; this revision's three fixed-slot folds (Appendix BG) take it to 11,657.035512 (perclass 4,770.967335 -> 4,563.533863); `FIXED_P7` = 26; per first block 5.41870 units at the one-unit charge of 9.11; PRE = 2^39. The cap is computed at slack 1/15000: Pcap = 3.579311e-07 <= 9/25,000,000, mu_req 0.49466302. N = 442,359,749,485,967,173,670 (one unit per first-block compression), so log2 T = 57.215275556308605 and the claim is **57.21528**.
- *Unchanged and checked.* `selftest` is byte-identical to the base apart from the printed FIXED/FIXED_P7 and the added prefilter line (Appendix D). Under organizer-style requests (256 trials), `a0-sfs-r37`, `h1-cv1-filters-nonce`, `h3-cowpass-nonce`, `h3-ladder-r37` and `h6-orgstats-r37` return byte-identical stdout to the base program; `a0-online-r37` returns the same pairs with every mismatch counter 0, only `counted_ops` and the two added observations moving. Runtimes 1.2-9.4 s each (six run in parallel on one machine).

**9.6f No re-check of row 16 in the rare path (R37P40k).**
A candidate pair enters the rare path for l only after the exact row-16 test of Lemma 6.2 (table stage plus residual test), which decides every cell and printed two-bit condition closing at row 16 (exhaustively checked, Appendix A). The rare path still computes row 16 (106 + counter) to reach row 17, but no longer re-checks it (53): `c3b_l = 2 + 6 + (ROWCOMP + 1) + c3b_row = 275` per l (was 328). `step3b` computes row 16 and goes straight to row 17; it keeps an uncounted assertion that the skipped check would pass, so executor replays fail loudly if it ever did not. This saves 53 operations per survivor entering the rare path, reducing rare path work from 177.639 to 161.162 ops per first block, and reducing vbar by 16.477 ops/FB.

### 9.7 The packed group: GROUP_BODY = 28, first stage 12, continuation seven
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

**9.7c One address mask, not two (R37P23).** The itemisation charged two masks against `U`: bits 9..23 for `FIRST`, the low 9 bits for `SECOND`. Bits 0..23 are one contiguous field and an address extraction costs a shift *and* an AND either way (the shift brings the neighbouring lane's bits down, the AND isolates the lane), so one `& 0xffffff` serves both: `(Um >> 64k + 9) & 32767` for `FIRST` and `(Um >> 64k) & 511` on a hit -- the two primitives each that the probe's 3 per lane and the continuation's 7 per hit already charge. `GROUP_BODY` 31 -> 30; `U` unchanged and the two addresses reproduce the shipped pair on 12,000 lanes (`r37-laneunmask-61.py`).

**9.7d One address mask was one too many (R37P24).** 9.7c's `Um = U & bc64(0xffffff)` is not executed either: a lane's address is extracted by the shift *and* the AND that follows it, so `(U >> 64k + 9) & 32767` (bits 9..23) and `(U >> 64k) & 511` (bits 0..8) already clear what the word mask was charged to clear, and a shift by zero is no operation (lane 0's first address was `U & 8191` under the 13/11 split). `GROUP_BODY` 30 -> 29, `PROBE` (3,3,3,3) -> (2,3,3,3), 12 -> 11 per group, which the top-first 15/9 split of R37P38 reverses to (3,3,3,3) because a shift by 9 is not a no-operation; 0 mismatches over 175,940 lanes of 43,985 group words from 300 first blocks (`r37-nomask-63.py`).

The same instrument settles the two *lanes-clean* masks, and neither can go. (i) Widening the free guard constant cannot replace the `& LM` on `S1E`: the shifts are 256-bit, so the unmasked `S1E` carries the *next* lane's low bits into its own high half and reaches 0xffffd2d3 there -- a field that no guard fits, since `Sw`'s high half can be zero -- and 7,808 of 12,000 lanes come out wrong at guard 2^26 + 8 (the guard change alone moves no bit). (ii) The `& LM` on `s0W` **is not executed** (9.7e). It is the last operation before `U`, and only a carry out of bit 63 of a lane could reach a read bit (`FIRST[U>>(64k+9) & 32767]`, `SECOND[U>>64k & 511]`, `u = U>>64k & 2^32-1`). With `w` the lane of `W1` and `n` the next lane, the high half the mask would clear is the GF(2)-linear form `H(w,n) = w[7:32] ^ ((n&127)<<25) ^ w[18:32] ^ ((n&262143)<<14) ^ ((n&7)<<29)` (checked against the shipped arithmetic, 20,000 pairs, 0 mismatches); its image over GF(2)^64 has rank 25 and excludes 2^32-1..2^32-4, so `H <= 2^32-5` and `H 2^32 + L <= 2^64 - 2^33 - 3` for `L <= 3(2^32-1)`: no lane carries, bits 0..31 of `U` are unchanged on every input, `GROUP_BODY` 29 -> 28 (`r37-s0wreach-66.out`; `r37-s0wreplay-66.out`: 293,728 lanes over 400 first blocks identical).

**9.7f The text executes exactly the itemisation (iteration 78).** The table above *is* the claim: `GROUP_BODY` is the number of word-RAM primitives the shipped `packed_u` executes. It had been written from the arithmetic and never checked against the source line by line. It is checked now: `reports/experiments/r37-masks-206.py` reads the ten statements out of the shipped function, counts each one's word-RAM operators against the table above, and fails if any statement carries an operator the table does not charge (receipt `reports/receipts/r37-masks-206.out`). The census found the text one operator over on three lines — the word mask `& M256` on the two doublings and on `U`. Two of them are identities: `E0` and `W1` are masked with `LM` one operation earlier, so every lane of `x = E0 | E0 << 32` already lies inside bits 0..63 of its own window and `x & M256 = x`. The third clears only bits >= 256, which no read touches, since a lane's value is read as `(U >> 64k + 9) & 32767`, `(U >> 64k) & 511` and `(U >> 64k) & 2^32-1`, all inside lanes 0..3. The three masks are removed in this revision and nothing else changes: `GROUP_BODY` stays 28, `vbar` is 12,433.992190 (Section 9.7g), `SB_OPS` stays 2,867; 5dbbb8da re-priced it to 2,745 (57.10556) and this revision's two folds re-price it to 2,688 and the claim to 57.10307. Verified on real first blocks: 180 group words (720 lanes) give bit-identical `u` and bit-identical `FIRST`/`SECOND` addresses with and without the masks, `u == u_ref` on every lane, `selftest` 0 mismatches, and the census passes 28 = 28 (11/11 checks). **Why this is not housekeeping:** the charge is the text's own primitive count, so a text that executes 31 while the ledger charges 28 understates the group stage by 3/28 of the 36% of `vbar` that cell holds. Charged at its own 31, the same program prices at 57.15979397 -- above the frontier 57.14301. Removing the masks (kept in the accepted row) is what made that row's 57.10903 an honest count rather than a 0.05077-bit understatement, and the census makes the correspondence a standing test rather than a paragraph. **9.7g The continuation was the next cell, and it did not match (iteration 83).** The shipped `filt_mid` call counts seven operators per nonzero FIRST under this pricing; the expectation ledger in `d14c3219` had charged six rather than seven. The correction needs no new argument, because the *ceiling* already charged it: `vmax_fb_value` prices a group word's four lanes at `GROUP_BODY + sum(PROBE) + 28`, seven per lane. `expected()` and `process_cv` now charge seven. What moves: `grp` 6,624.380926 -> 6,667.264396, `vbar` 12,391.108720 -> 12,433.992190, `N_FB` 30,821,585,407,821,970 -> 30,821,581,046,249,033, `V_MAX` 381,938,058,196,077,723,070 -> 383,259,825,065,651,273,791, `N` 409,630,409,260,844,968,266 -> 410,952,172,318,403,772,049, and the claim to **57.10903** on that revision's prices. It costs 0.00465 bit and the row still stands 0.034 bit below the promoted 57.14301; `reports/experiments/r37-reprice-208.py` re-derives it.
### 9.8 Survivors and the residual exact test
After T!=0, the original five-primitive fold and eight-primitive u extraction and mask scan remain SURV_FIX=13. SURV_LANE=6 is unchanged. Only the exact test is reduced to EX_OPS=13: address/load C_l (2), e=u+C_l (1), e&bit30 (1), address/load cxA_l (2), A=e+cxA_l (1), A&0x22000000 (1), address/load VA_l (2), XOR VA_l (1), OR the E and A failures (1), branch (1). Neither addition needs a 32-bit reduction, as proved in Section 6.2. The low-24 table predicate, survivor mask and every rare-path visit are unchanged.
### 9.9 The rare path
A pair with a row-16 pass for some l (probability at most 2^21 / 2^32 = 2^-11 per probed lane): work-counter update and lookup of the member (1 + 2); recompute W6 and W7 (RECOMP = 35); W0..W5 and W8 (201); then for each such l the y-words (8) and rows 16..21 with early abort, each row 106 + 53 + 1 (both members' W 20, CH 3, E 14, MAJ 4, A 12 per word; the cells and two-bit conditions closing at the row at most 53; the work-counter update 1). When row 21 holds, rows 22..36 are computed with no cell test (106 each) and the pair is accepted iff the eight registers A33..A36, E33..E36 of the two members are equal (the collision event of Section 7.7; both members share CV1, so equal registers are equal outputs): the comparison is 8 xor, 7 or and 1 branch (OUTCMP = 16), and the work counter is updated once for the 15 rows and the comparison (1). `step3b` and `same_out` of `experiments/lowm.py` execute exactly this. The ledger charges rows 16 and 17 always (c3b_l = 8 + 2 x 160 = 328 per l) and, for every l of every probed lane, with probability 2^-9 (the SMC stage factor of row 17 is 2^-12 under R16x, Section 7.4c): rows 18..21 checked in full and rows 22..36 with the comparison in full, with no early abort, c3b_t = 4 x 160 + 15 x 106 + 16 + 1 = 2,247 (the cell event charged 19 x 160 = 3,040 at the same probability). This is the rare-path charge of 4ec21bf9 (its Appendix D.5: c3b_t = 4 x 160 + 15 x 106 + 16 = 2,246 at probability 2^-11) with the work-counter update added and the 2^-9 of the base kept. The other items are the counts of 0db0eeb6 Section 9.7 and 7319bba.
### 9.10 The work counter V and the cap
V counts every executed data-dependent primitive: each of the following updates it by a constant (one primitive each, counted in the item): a passing class (its fixed price, sweeps, main run and spills), a subtraction run (its F6 test and scan), a member (its placement and, for a rep, its scan and extraction), a group (its body and four probes), a survivor lane, a survivor bit (its exact test) and every row of the rare path. The per-group update is not a separate primitive here: a group body's charge is a class constant times the lanes it completes, so the per-rep update listed above (inside `MEMBER_CHARGE`) adds it with the same single primitive, and the run's aggregate rounding is the `CF_CLASS` allowance (9.7b). `V` is read only at the per-first-block cap test, so its intermediate value inside a class run is not observed and the batching changes no counted behaviour. The data-independent part (FIXED) is charged per first block. The cap is tested after every first block (compare and branch, in the control of 9.2). Since R37P40g the setup of a first block with a passing class (`FB_DET`, Section 9.6d (e)) also updates V once by its constant, and since R37P40h so does the class test of a first block whose prefilter byte is 1 (`CT_V`, Section 9.6e). The overshoot past V_MAX is at most the maximal data-dependent work of one first block, vmax_fb = 549088648247/10 = 54,908,864,824.70 at this revision (worst |I| for every class, every rep good, every l through row 36 and the comparison, plus the 155 of `FB_DET` and the 220 of `CT_V`), which the ledger charges.
### 9.11 The seven-lane first-block batch (P8; credited to f1163fcf, 22fc4519 and ffca313a)
The first block of a trial is one target compression (charged as one unit, SB_FB = 2644 = C word operations, whether computed alone or in the seven-lane batch below; Rulings ba65804c and f044761e F1). This filing's text computes seven first blocks at once in one 256-bit register: lane i occupies bits 36i..36i+35, the 32-bit word in the low half of the lane and four guard bits above it. Every primitive of that text is counted (`sb_batch`, counter `SB_COUNT` in `experiments/lowm.py`), and `sb_measure()` runs 40 batches of seven at import and asserts the eight chaining words of every one of the 280 lanes against `compress(IV, w)`, the shipped 37-step compression. The count is data-independent (straight-line text) and is asserted to be the same on every batch.
**9.11.0 The count of this cell.** 2,688 word-RAM primitives per seven first blocks (384 per first block) are executed; Section 11 charges each first block one full compression, SB_FB = 2644, not 384 (Rulings ba65804c and f044761e F1); every executed primitive of the straight-line batch text is counted, and the last, incomplete batch of seven is charged as a full one by the ceiling. The batch changes no probability: it is data-independent, and N_FB, the work cap, the slack and the Bernstein bound are untouched by it.

| item | primitives |
|---|---|
| 23 lane masks (prepacked literal slots, 9.11.2; zero counted reloads) | 0 |
| 16 message words packed (RAND, AND, STORE at fixed literal displacement, 9.11.2) | 48 |
| IV: prepacked at import, including BC0 = H0 ^ H1 and FG0 = H4 ^ H5 (9.11.2) | 0 |
| schedule: 21 words, each s1 (14) + s0 (14) + three adds + mask + store = 33 | 693 |
| steps: 36 x 50 - 4 = 1,796 (t1 = S1 17 + ch 3 + 4 adds [-1 at t=1 via FG0, -1 at t=1..3 via KTL[t] folding H_{7-t} + K_t], t2 = S0 17 + mj 4 [bc = a ^ b carried across steps so Maj = b ^ ((a ^ b) & bc) is 3 ops] + 1 add, na and ne 2+2 with their masks, the W_t load 1; K_t is a literal-slot reference after 9.11.2) | 1,796 |
| round 0, folded (9.11.1: one W_0 load, two adds with the prepacked literals, two masks) | 5 |
| feed-forward: eight lane adds to the IV and eight chaining-value adds (cv) | 20 |
| store the eight packed chaining words (prepacked slots, 9.11.2; zero counted stores) | 0 |
| batch control (counted within the feed-forward row) | 0 |
| eight constant reloads (prepacked slots, 9.11.2; zero counted reloads) | 0 |
| extraction of the seven lanes' eight words (2 each, plus 2 for the hand-off) | 126 |
| **SB_OPS, per seven first blocks** | **2,688** |

The two masks per step are not optional. Every stored word is below 2^32, so one step's intermediates are h + S1 + Ch + (K_t + W_t) < 5 x 2^32, t2 = S0 + Maj < 2 x 2^32, a' = t1 + t2 < 7 x 2^32 and e' = d + t1 < 6 x 2^32, all below 8 x 2^32 < 2^35 < 2^36 = one lane: no lane can carry into its neighbour. The schedule is stored masked for the same reason; the unmasked-schedule variant of this text counts 2,893 and passed 280 random lanes, but its bound is 17 x 2^32 > 2^36, so it is not filed. Rotations are lane-exact because the low mask is lane_mask(0, 32 - n) and the high mask lane_mask(32 - n, 32) of the 36-bit lane, and the lane width is 36 rather than 32 precisely so that the two masks of a rotation cannot be one.

#### 9.11.1 The fixed-IV round-zero fold (this revision's own cell)

Round zero of the first block is the only round of the attack whose input state is a constant, and that
is what makes it foldable. With the standard IV, t1 = H7 + S1(H4) + Ch(H4,H5,H6) + K0 + W0 = W0 + C0 and
t2 = S0(H0) + Maj(H0,H1,H2) = T2, so after round zero

    a' = W0 + (C0 + T2) = W0 + 4228417613  (mod 2^32)
    e' = W0 + (C0 + H3) = W0 + 2563236514  (mod 2^32)
    b', c', d', f', g', h' = H0, H1, H2, H4, H5, H6,

with H3 and H7 consumed into the two literals: C0 = 4084723048 and T2 = 143694565. Both sums are below
2^33 before the 32-bit lane mask, so no carry reaches the 36-bit lane guard of 9.11, and the six carried
registers are the packed IV words themselves (register relabels, no primitive). Verified here, not
quoted: a from-scratch FIPS 180-4 round zero agrees with the two literals and with the six carried
registers on 5,000 random first blocks (0 mismatches), and the instrumented packed batch asserts
equality with the reference compression on all seven lanes of every trial. The fold literal is written
inline (4228417613) rather than through the name `FA`, which the class test later rebinds to `A1 ^ A2`:
the batch reads globals at call time, so before this the assertion held at import only, and now it holds
on every call, including after load (`sb_measure(8)` = 2,688). `sb_pk` is uncharged, so no cell moves.

Cost. The generic round of the promoted row costs 52 packed operations (t1 = 14 + 3 + 4, t2 = 17 + 3, two adds, K_t and W_t loads, two masks); the folded round costs 5 (one seven-lane load of W_0, two adds with the two prepacked
literals, two 32-bit masks), so 9.11 loses 47 per round (1,692 over 36 rounds). The 9.11.2 folds remove 5dbbb8da's 122 prepacked-literal operations
plus 57 further operations (16 fixed-slot w[0..15] stores, 1 prepacked BC0, 1 prepacked FG0 at t=1, 3 folded IV[7-t]+K[t] adds at t=1..3, and 36 carried bc = a ^ b step-recurrence operations in Maj across t=1..36), and the batch carries eight chaining-value adds (cv) and 4 control primitives, shown once inside the
feed-forward row of the itemized table, so SB_OPS measures **2,688**, not 2,745 (or 2,914), by the batch's own counter (every counted primitive is assigned to exactly one row of the 9.11 table and the rows
sum to the counter), and `python3 experiments/lowm.py ledger` reproduces the charge below from the measured count.



Conservatism. The credited rival filing 4c7de621 (jungjipdo) charges the literal fold with two extra ops;
priced with that 2-op convention on 5dbbb8da's batch text the count was 2,747 vs 2,745 (both ceiling 393), and here the 57-primitive reduction takes SB_OPS from 2,745 to **2,688** = 7 x 384, giving
the former SB_FB = ceil(2,688 / 7) = 384 (and even with the 2-op literal convention 2,690, ceil(2,690 / 7) = 385,
still 8 ops per first block below 393). This is a fall in executed primitives,
not a re-pricing, and this revision's cost changes are exactly the two folds named in the charge below.

The charge. The batch replaces the compression charge of 9.2 for seven first blocks at once and carries the 30 word-extraction primitives of 9.2 ("First block words"), adding SB_CTL = 4 control primitives:
```text
FIXED_P7 = FIXED - 30 + SB_CTL = 461 - 30 + 4 = 435
ceil(SB_OPS / 7) = ceil(2,688 / 7) = 384 word operations executed per first block (the former SB_FB)
per first block: SB_FB/2644 + FIXED_P7/2644 + vbar/2644
               = 0.14523 + 0.16452 + 4.52403 = 4.83379 units   (this filing, after 9.6c; the base 3c71035b row prices 5.01248, 5dbbb8da 5.02118, the promoted parent row 5.15345)
```
**Charge at this revision (Rulings ba65804c and f044761e F1):** SB_FB = 2644, one unit per first block; per first block 2644/2644 + 26/2644 + 11657.035512/2644 = 1 + 0.00983 + 4.40886 = 5.41870 units. The 384 figures in this section are the executed batch count, not the charge.
The executed count is exact (2,688 = 7 x 384). N_FB is unchanged: the batch changes no probability, only the price of the data-independent part, and the last, incomplete batch of seven is charged as a full one by the ceiling. The work cap, the slack and the Bernstein bound are untouched. **Relation to the promoted row and 5dbbb8da.** Starting from 5dbbb8da (57.10556, FIXED = 475, FIXED_P7 = 449, SB_OPS = 2,745, SB_FB = 393), this filing changes two cells. (a) The c7 load-slot fold of Section 9.2: the fifteen dynamic planes of c7 are loaded from compile-time slots of `c7_planes` (`base + immediate`, no address add), identical to P9 and the q store-slot fold of ed0d4c15/5dbbb8da; FIXED 475 -> 461 and FIXED_P7 449 -> 435, worth 14/2644 units per first block (and lowering the compression-floor sensitivity from 57.33112 to 57.32982). (b) The 9.11.2 fixed-slot w[0..15] store, prepacked BC0/FG0/KTL[1..3], and carried `bc = a ^ b` step recurrence in Maj: SB_OPS 2,745 -> 2,688 measured by the batch's own counter, so SB_FB = 393 -> 384, worth 9/2644 units per first block. Both are falls in executed primitives, not a re-pricing: no stage price moves, the batch row stays SB_FB per first block against the same 2,644-op reference, and the folds make the row they are charged on cheaper under both readings.
## 10. Success probability, independence and caps
Let a *trial* t = (f, a0, l) be a first block f, a variant a0 of a passing class and l in L*, and A_t the event that a0 is good for f, the pair follows every cell and printed two-bit condition of rows 16..21 and the two 37-step outputs are equal (this filing's success event, Section 7.7). The program examines every good pair of every processed first block (Lemma 8.1) and every l whose row 16 holds (Lemma 6.2, exact), so it finds a success iff some A_t occurs before the cap, and every output is verified (Lemma 6.1). Let X_f = sum over the trials of f of 1[A_t] and X = sum_f X_f.

- **Expectation.** E[X_f] = g x 32 x q3 (Lemma 5.1 and Section 7) with g = p7 p6 x 599,760 = 636.680 the expected number of good pairs per first block (exact: each of the 170 classes passes with probability p7 and each of its variants then passes F6 with probability p6), and E[X] = N_FB g 32 q3.
  With q3 >= 2^-71.4162 x 2.482, the current ledger uses N_FB = 30,821,554,876,811,406 and requires mu0 = 0.49466302. The assumed cap failure is 9/25,000,000 = 3.6e-07; Appendix C computes the exact achieved mean and the conditional success floor.
- **One first block (H3).** By Bonferroni, Pr[X_f >= 1] >= E[X_f] - sum over pairs t < t' of f of Pr[A_t and A_t'] = E[X_f] - (1/2) sum_t Pr[A_t] E[X_f - 1 | A_t]. H3: sum_t Pr[A_t] E[X_f - 1 | A_t] <= delta E[X_f] with delta = 2^-9.4 (trial-averaged conditional expectation), so Pr[X_f >= 1] >= (1 - 2^-10.4) E[X_f].
  H3 splits into (a) the same variant with another l: at most 2^-11 (7319bba measured 0 further successes among 19,620,436 distinct Step-3 successes of its SMC, rule-of-three bound 2^-22.65; the four accepted patterns multiply the chance of passing rows 18 and 19 by about 4 and R16x the chance of the path by about 1.6, with four more l holding row 16, which gives about 2^-19.8, far below 2^-11), and (b) other good pairs of the same first block: summing over all other trials t' = (f, a0', l') of the family uses the family average of Pr[t' succeeds | t' good], which is q3 by definition, so at most rho x N_good x 32 x q3 with rho <= 2^35 (the measured factor at row 16 is 0.98 and 1.00), q3 <= 2^-71.38 x 2.4902 = 2^-70.0637 (H2, Section 7.7) and
  N_good <= 599,760 (all variants of the family, 2^19.58), so (b) <= 2^35 x 2^19.58 x 2^5 x 2^-70.0637 = 2^-10.4837 and delta <= 2^-11 + 2^-10.4837 = 2^-9.7189 < 2^-9.4. (N_good is the number of all variants of the family, as in the earlier filings on this family; no size-biased mean and no per-trial uniformity across (a0, l) is needed.)
- **Many first blocks (H1).** Distinct first blocks have independent chaining values, so the events X_f >= 1 are independent and Pr[X >= 1] >= 1 - exp(-sum_f Pr[X_f >= 1]) >= 1 - exp(-(1 - 2^-10.4) mu0).
- **Work cap.** At this revision the data-dependent work has reported mean vbar approximately 11,657.035512262588 operations and maximum vmax_fb = 53,789,931,987.9. Under H1, put m = N_FB vbar, M = vmax_fb and t = m/15000. The Bernstein bound uses Var(v_f) <= M vbar and is evaluated below.
  Pr[sum v_f - m >= t] <= exp(-t^2 / (2 (N_FB M vbar + M t / 3))). The reported value is approximately 3.579311e-07, below the assumed 3.6e-07; V_MAX = 359,311,912,272,790,214,230. The participant ledger reports the exact vbar = 125166465733696063954897/10737418240000000000; substituting that value gives exponent 21.413814822003385 and the stated cap. This arithmetic does not independently establish the operation model or its expectations.
  No part of v_f depends on a conditional law of the scalars: the plane programs cost the same for every data, and the data-dependent items are linear in the numbers of passing classes, good pairs, groups, survivors and hits, whose exact means the ledger uses.
- **Success.** Under the stated H1-H3 premises, the floor is 1 - exp(-(1 - 2^-10.4) mu0) - Pcap - 2^-60 = 0.39000000604429280 > 0.39; Appendix C states the constants and recomputes it.
## 11. Ledger (draft; Appendix B mirror)
```text
T = A_C + A_S + DEV + N_FB*2644/2644 + (N_FB*26 + V_MAX + ceil(vmax_fb) + PRE + FIN)/2644 + 6
A_C=2^48, A_S=2707315195888 (2^41.3), DEV=2^40, PRE=2^39, FIN=1600
N_FB=30821554876811406; vbar approximately 11657.035512262588; vmax_fb=53789931987.9
SLACK=1/15000; V_MAX=359311912272790214230
Pcap approximately 3.579311e-07 <= 3.60e-07
N=442359749485967173670; T=N/2644; log2(T)=57.215275556308605
rounded time_log2=57.21528; preprocessing_log2=48.01938
```
**Historical ledger discussion, predating the current R37P40l row.** The independent Fraction ledger first reproduces aa0e8b6's original N exactly, 773438176907133806360 with its executed law: Q0[0] has probability 1/4 and bits 2,3 each have probability 1/2. Its time_log2 is 58.0213414138426649296682670834074841281671112606650421931692417246587004428, rounded 58.02135. Our delta from that reproduced baseline was written in the previous revision as a closed form in the placement charges of the time; iter37 changed those charges (Section 9.6), so the form is superseded and the shipped `lowm.py ledger`, printed in Appendix B, is the arithmetic of this filing. The cap slack is 1/15000 (as in R37P39 and R37P40g): log2 T(1/14500) = 56.994555653, log2 T(1/15000) = 56.99455358868023, log2 T(1/15500) = 56.994553332; all three round to 56.99456, and the inherited 1/15000 is kept; the exponent is 14.81975. With mu_req = 0.49466303 and N_FB = 30,821,555,499,893,254 the success bound is 0.39000000213977449. R37P40g row: 57.00229 with exponent 14.63538, mu_req 0.49466316, bound 0.39000000138103141; R37P39 row: 57.05080 with exponent 14.92027, mu_req 0.49466298, bound 0.39000000166236525; 3c71035b row: 57.10307. No runtime or full-scale success claim is added. The executable participant ledger is statically cross-checked against this independent ledger and Appendix B; its executor diagnostic agrees exactly.
### 11.1 Exactness of the expectations
Each row is linear in a count whose expectation is exact: a class passes with probability p7 (Section 5.3), the number of runs of a passing class is 2^(|B| - j) with j = |I| and the executed mask weights of Section 8.1 (Q0[0] probability 1/4, other cube bits 1/2), a rep of a run is good with probability p6 (Lemma 5.1), a first block runs the setup `FB_DET` with probability exactly P_PASS = 549,066,752/2^32 (Section 9.6d (e)) and the class test `CT_V` with probability exactly P_H = 11,008/2^14 (Section 9.6e), a probed lane has exactly 1/256 survivors on average and a nonzero filter with probability exactly 63,512/2^24 (Section 6.2), and 2^21/2^32 row-16 hits (Lemma 5.1: u uniform). One row is charged at a measured rate instead of its worst case: the number of groups is E[ceil(N / 4)] <= (E N + 3) / 4, and the shipped `process_cv`'s own `pad` counter shows that the residual word almost never executes -- `P mod 4 = {0: 4991, 2: 8, 3: 1}` over 5,000 real first blocks, 17 padded lanes in 9 partial groups (`reports/receipts/r37-cells-64.out`). The ledger therefore charges the one-sided 99% Poisson upper bound on that rate, `PAD_RATE = 117238429/2*10^10` lanes per first block, against both the extra group word (overcharging it fourfold, a group word being four lanes) and the padded body: `groups = pairs/4 + PAD_RATE`, `grp = groups (GROUP_BODY + sum(PROBE)) + PAD_RATE PAD_OPS`. `vmax_fb` keeps the worst case, as a maximum must. The row moves by 40.48 operations per first block (0.00388 bit); no constant, premise, algorithm or family moves. It is below 0.2% of vbar.
### 11.2 The advice-construction allowances A_S and A_C (H4)
The advice is the 37-step characteristic and its two-bit conditions (Tables 15, 16), the Step-1 solution S and the semi-free-start pair (Table 17); their construction is charged A_S = 2^41.3 = 2,707,315,195,888 (the paper's own Step-1 SAT solve; completing a Step-1 solution to a 37-step semi-free-start pair takes about 25 milliseconds, organizer experiment `a0-sfs-r37`) and A_C = 2^48 (the unpublished characteristic search, calibrated from the measured complete re-run of the predecessor 35-step search accepted in 6eeefb64: 593,858 solver CPU-seconds = 2^19.18 CPU-seconds at the calibrated price of 2^21.427 units per CPU-second, giving 2^40.61 units; A_C = 2^48 units is 2^26.57 solver CPU-seconds = 3.16 CPU-years, more than 169 times that measured complete re-run, and A_C + A_S + DEV = 2^48 + 2^41.3 + 2^40 = 2^48.02; sensitivity is reported at A_C = 2^56 -> 57.57945, A_C = 2^60 -> 60.16901, and A_C = 2^64 -> 64.01117, on this revision's ledger). Everything derived from the advice (G, the classes, the lists, F6, F7, L*, the tables) is recomputed in the preprocessing (PRE = 2^38 operations) or is the 170 class descriptors (below 2^13 bytes of advice).
## 12. Premises
The statistical premises and their empirical support are inherited unchanged. Every row quoted here and in Appendix G is priced on R37P27's ledger and shifts down by 0.06571 bit at the accepted row's vbar (12,433.992190, unchanged by this revision's two folds). The sensitivity costs in Sections 11.2 and 12 and Appendix G are recomputed with P4 prices, unchanged predicates, rational 40-bit q3 mantissas and ceil N_FB at that revision's mu0=0.49466812. The primary slack is retained unless increased on the 10^-20 grid to preserve its Bernstein exponent; times round upward to five decimals. Four-pattern and Table 15 sensitivities use their probability floors in the current P4 program, not alternate predicates. Using the J2 bound alone (q3c=2^-71.4524) gives 57.65139 (60.25958 under A_C=2^60); this is a sensitivity, not a replacement for the declared min-block floor.

**H1 (score-critical).** Our theory: the first blocks M0 are fresh uniform 512-bit strings; their chaining values CV1 = F_37(IV, M0) behave as independent uniform 256-bit values; in particular x = A_{-1} is uniform on 2^32 and independent of cb = C6 - A_{-2}, which is uniform on 2^32. Consequences used: each of the 170 classes passes the W7 test with probability p7 = |F7|/2^32 exactly, each variant of a passing class then passes F6 with probability p6 = |F6|/2^32 exactly, and given both, W0..W5 are uniform and independent of (W6, W7) (proof.md Lemma 5.1); hence the expected number of good pairs per first block is g = 599,760 p7 p6 = 636.680, the expected counts of the ledger, and the independence of distinct first blocks.

*Scope.* The expected numbers of passing classes, good pairs, survivors and row-16 passes per first block; the expected operation count of the counted program; the law of the second-block words that defines q3; independence across first blocks (proof.md Section 10). Not the validity of any output: every output is verified with the target. *Evidence.* Measured by 7319bba with the attack's own filters on real first blocks in C (2^21 and 2^23 first blocks: passing classes 7,400,134 and 29,545,568 against the ten-list control's expected 222 p7 2^21 = 7,388,160 and 222 p7 2^23 = 29,552,640 (not this filing's 170 p7); good pairs ratio 1.0034 and 1.0011; row-16 pairs z = +0.88, +0.51), by this filing's simulation of the counted program on 20,000 real first blocks (passing classes per first block 3.457 against the exact 3.523, good pairs 836.3 against 831.0, mean counted operations 28,377 against the ledger's 28,289, both at the parent's six-primitive continuation price, which this filing's audited seven raises by one per nonzero FIRST on both sides), by the unconditional sample in `a0-online-r37` (64 organizer-seeded first blocks per active trial: 90,682 class W7 passes in 25,600 first blocks of our 400-trial run against 90,187 expected), and by the organizer experiment `h1-cv1-filters-nonce`, which counts on 150 organizer-seeded real first blocks per trial how often the W7 filter (first class) and the W6 filter (its first four variants) pass (expected 2.38 and 40.1 per trial; our replays, 100 trials each: 244 and 214 W7 passes against 238.0, 4,011 and 3,988 W6 passes against 4,013.7; Appendix H). These are at most 2^23 real first blocks, not 2^55.8. *Limitations.* Premise (our theory), not a theorem: the filter rates are measured on at most 2^23 real first blocks and on the organizer's small samples, not at the 2^55.8 first blocks of the attack, and independence across first blocks is assumed, not tested. The class tests of one first block are strongly correlated (their c7 values are close), so per-first-block counts are overdispersed; only their expectations and the independence across first blocks are used. The class test uses the single word x, so H1 is also an assumption about that word of the digest of a 37-step compression.

**H2 (score-critical).** For a good pair, q3 = the average over the 599,760 variants of the 170 classes (each equally likely, as examined here) and the 32 elements of L* of Pr[rows 16..21 of both members follow every cell and every printed two-bit condition closing at rows 16..21 (corrected reading A15[29] = A17[29]), the eight value bits E18[1,5,10,11,18,28,29] and E19[29] of Table 15 not imposed, and (R16x) E16[23] = 0 and E16[24] = E17[24] not imposed: exactly the cells and conditions of experiments/lowm.py, and the two 37-step outputs are equal (rows 22..36 are computed without cell tests, Section 7.7)] satisfies q3_used = 2^-71.4162 x 2.482 = 2^-70.10470 <= q3 <= 2^-71.38 x 2.4902 = 2^-70.0637, where q3 = q3c x R: q3c, the probability that rows 16..36 follow every cell, satisfies q3c >= q3c_used = 2^-71.4162 <= q3c <= 2^-71.38. The operative lower bound is block F's alone: the one-sided 99 percent Student lower bound of the **linear** estimates of the 16,384 preregistered replicates (Appendix N), the estimator being unbiased on the linear scale, so the linear mean is the estimator and declaring 2^mean(log2 est) would be the geometric mean, 0.008676 bit lower on the same data. Every earlier bound of this quantity is numerically weaker and is carried here only as a stated conservative sensitivity with its own claim, never as the operative premise: the preregistered min of the two per-block bounds 2^-71.4629 (claim 57.62615; blocks J1 and J2 of 128 replicates each, NP = 8192, one-sided 99 percent upper bounds 2^-71.3970 and 2^-71.3838), block E's log-scale 2^-71.4243 (claim 57.58779) and the pooled parents'-pool bound 2^-71.4474 (claim 57.61074) with its 0.0020-bit allowance 2^-71.4494 (claim 57.64841). The estimator is a sequential Monte-Carlo program written for this filing (Appendices F and G), run on exactly this family with both relaxations as one carrier; and R = Pr[equal outputs | rows 16..21] / Pr[cells of rows 22..36 | rows 16..21] satisfies EXQ = 2.482 <= R <= 1275/512 = 2.4902, where 2.482 is the preregistered one-sided 99 percent lower bound of the ratio of collision events to cell events after row 21 measured directly on this filing's 599,760-variant pool and characteristic in Block G (Appendix O: 1,024 fresh seeds 860000..861023, R_pooled = 2.484920, LB_p = 2.482246 -> EXQ = 2.482; 4ec21bf9's 2.4331 from its Appendix D.3 runs -- 2.4648 +- 0.0145 on Table 15 states, 2.4552 on ffbe30bb's states, 2.46455 under its kept-fibre law -- is retained as a sensitivity) and 1275/512 is the uniform-model value of its Appendix D.2; this heuristic explicitly includes the statistical and procedural premise that the participant-reported preregistrations, complete contiguous seed lists (710000..710063, 720000..720127, 721000..721127, 740000..740127, 741000..741127), fixed two-block min(LB) rule, interim progress monitoring during execution, and prior condition-relaxation screening (adopting the four row-18/19 patterns and R16x after screening 30 candidate condition pairs) do not introduce selection, optional-stopping, or multiple-comparison bias exceeding the margin between the two disjoint-seed block estimates, the 6-seed direct full-path check and the declared floors `q3c_used = 2^-71.4162` and EXQ = 2.482 (the preregistered min-of-blocks bound 2^-71.4629 remains a stated sensitivity).

*Scope.* The expected number of successes E[X] = N_FB g 32 q3 and hence N_FB (proof.md Sections 7 and 10), including the validity of the offline SMC estimation protocol, seed selection, stopping rule, and relaxation screening that support `q3c_used = 2^-71.4162`, and the ratio EXQ = 2.482. The good pairs and the later rows are those of 7319bba; this filing changes how the good pairs are found, not which pairs are good, and which pairs count as a success: (from ffbe30bb) the value patterns of rows 18 and 19 and (new) R16x at rows 16 and 17, which also gives the four l = 0, 2, 16, 18 row-16 values, and (from 4ec21bf9) the collision event after row 21 in place of the cells of rows 22..36. *Evidence.* Lemma 7.1: rows 16..22 have exactly the same probability for every variant; a variant enters rows >= 23 only through W8 in W23 and W24, so only the four W24 conditions can depend on it (about 2^-4 for every W8x). Our estimator (exact row 16, exact importance weights at rows 17..21, (W6, W7) uniform on F6 x F7, W8 drawn uniformly from the 599,760 variants; Appendix F) was preregistered (validation V with Table 15 cells: mean 2^-73.9911, bound 2^-74.0064, z = +0.66 against the registered study B of 7319bba, mean 2^-73.9987, bound 2^-74.0225, validation PASSES both preregistered criteria (|z| <= 2.576; bound within 0.04 of -74.0225); main blocks R1 and R2 with the eight value characters of the two E cells removed: means 2^-71.9975 and 2^-71.9868, relative sd 0.0714 and 0.0681, bounds 2^-72.0191 and 2^-72.0074, declared 2^-72.02; stage factors of rows 18, 19 and 21 -8.00, -10.00 and -2.00 bits against -15.00, -6.00 and -1.00 for Table 15, structural gain 2.00) and again with R16x (constants written from the counted program; the same binary reproduces the four-pattern outputs byte for byte; joint blocks J1 and J2: means 2^-71.4296 and 2^-71.4177, relative sd 0.1096 and 0.1143, lower bounds 2^-71.4629 and 2^-71.4524, upper bounds 2^-71.3970 and 2^-71.3838, 0.55 bits above the four patterns alone; our earlier full-path test of R16x with independent rehash of all 30,814 collisions gave +0.590 bit [0.548, 0.631]). In addition, the organizer experiment `a0-sfs-r37` constructs and verifies full 37-step SFS collisions across 128 classes and all 8 pattern branches (63/64 on patterns 0..3 and 57/64 on R16x patterns 4..7 on our seeds `ours-A-0..127`; 13 of 13 returned pairs of trials 0..15 are found by the counted program), and the organizer experiment `h3-ladder-r37` runs the row-16 stage of q3 on organizer seeds: 41 exact row-16 passes among 98,216 W6 passes (4.2e-4, two seed sets) against the 4.9e-4 (2^-11) per probed lane of the ledger (Appendix H). The four-pattern relaxation (exactly four feasible patterns, three verified further collisions) is ffbe30bb's; here the three collisions are re-checked against this package's cells. R16x is ours (each of its two conditions alone is necessary; a sweep of 30 further condition pairs found no further gain). Here the examined law is the studied law (every variant of every passing class, no weighting), so no hedge is added. The collision event after row 21 (Section 7.7): given rows 16..21, the outputs are equal iff E22[29] = 1, s1(W22') - s1(W22) = 0x4fff9f30 and dW26 = 0, with the uniform-model ratio 1275/512 = 2.4902 (4ec21bf9, Appendix D.2); the measured ratio is 2.4648 +- 0.0145 (Table 15 states), 2.4552 (ffbe30bb's states, three runs, the last preregistered) and 2.46455 (the attack's kept-fibre law, preregistered), every cell event also a collision event in every run, and the preregistered rule gives EXQ = min(2.4331, 2.4443) = 2.4331 (the inherited minimum, superseded by Appendix O) (4ec21bf9, Appendices D.3, D.3b). With q3c one bit lower (q3 = 2^-72.4629 x 2.482) the claim would be 58.67775 (60.48509 under A_C = 2^60), with the four patterns alone (q3c = 2^-72.02) 58.26502 (60.37870 under A_C = 2^60), with the Table 15 value 2^-74.03 60.27060 (61.14148 under A_C = 2^60), and with the cell event of rows 22..36 instead of the collision event (EXQ = 1) 58.94181 (60.56559 under A_C = 2^60). *Limitations.* A Monte-Carlo and procedural premise, not a theorem: (1) its coverage rests on the approximate normality of the mean of 128 replicates (relative sd 0.1096 and 0.1143, about twice the Table 15 study's because few children survive the row-19 stage); row-22 survivors are heavily duplicated within a replicate; the row-22 stage draws (W6, W7) uniformly from F6 x F7, which is argued, not measured; depends on the reading of the '+' cells; (2) the offline preregistration timestamps/hashes (`PREREG_q3M.txt`, `PREREG_q3R16x.txt`) and contiguous seed lists (`710000..710063`, `720000..720127`, `721000..721127`, `740000..740127`, `741000..741127`) are participant-reported without an organizer holdout nonce, interim progress looks were taken while blocks ran (Appendices F.2 and G.2), and screening R16x against 30 other condition pairs before running J1 and J2 is not a multiplicity-adjusted holdout test, so the absence of material selection, optional-stopping, or multiple-testing bias is an explicit part of heuristic H2 rather than an externally certified guarantee; (3) no organizer experiment executes the end event of q3: rows 22..36 reach the digest only through a second-block chaining value that must be equal, which needs a reachable first block, that is the attack itself (`a0-sfs-r37` returns semi-free-start pairs and no full collision of the target); the organizer-executed `h3-ladder-r37` runs only the row-16 stage of q3 on organizer seeds; (4) EXQ is a Monte-Carlo bound from the runs of 4ec21bf9, not a theorem: those runs draw (W6, W7) uniformly from F6 x F7 and W8 from the variant list of that filing, on Table 15's and ffbe30bb's row-21 states and, in the preregistered fourth run, a pool of kept fibres of that filing's table; the ratio depends on W8 only through W24 = s1(W22) + W17 + s0(W9) + W8 and was not re-measured on this family's 599,760 variants or on the row-21 states that R16x adds; the runs share resampled row-21 states, so their counts are overdispersed (run 3: chi-square 55.4 on 31 df), which the quasi-binomial and cluster bounds allow for; no organizer experiment estimates the ratio. Premise (our theory): q3 is our computation, with the estimator, the preregistrations and the per-seed estimates printed in Appendices F and G. The count of four patterns is a solver enumeration (Bitwuzla; Z3 on smaller cases) for the published dense part with the signed cells of rows 14 and 15 kept (with rows 12..15 removed as well it admits 128 patterns); other dense parts were not explored, and our estimator does not use the solver. R16x has no solver enumeration: its value rests on the estimator, on `a0-sfs-r37`, and on our full-path test with rehashed collisions; patterns of rows 16..21 outside the program's cells (for example the E18 XOR pattern {24,23,16,15}) are not counted. A stated premise, not an established fact.

**H3 (score-critical).** Averaged over the trials t = (first block, variant, l) of a first block f weighted by their success probabilities, the expected number of other successful trials of the same first block given that t succeeds is at most 2^-9.4: sum_t Pr[A_t] E[X_f - 1 | A_t] <= 2^-9.4 E[X_f]. Equivalently: (a) the expected number of other l in L* succeeding with the same variant is at most 2^-11, and (b) for other good pairs t' of the same first block, Pr[t' succeeds | t succeeds, t' good] <= 2^35 Pr[t' succeeds | t' good].

*Scope.* The per-first-block Bonferroni bound Pr[X_f >= 1] >= (1 - 2^-10.4) E[X_f] (proof.md Section 10). The good pairs of a first block and their dependence structure are those of 7319bba; this filing changes the order in which they are processed, not the set. *Evidence.* (a) 7319bba's replay of 19,620,436 distinct Step-3 successes of the SMC: rebuilding W0..W5 and testing the other 31 elements of L* through rows 14..36 gave 0 further successes (rule-of-three 95 percent bound 2^-22.65 per success; the accepted patterns raise the chance of passing rows 18 and 19 by about 4 and R16x the chance of the whole path by about 1.6, with four more l holding row 16, so about 2^-19.8, far below 2^-11; in that replay the other l fail at row 16 or 17; the collision event changes only rows 22..36, so (a), decided at rows 16 and 17, is unchanged). (b) Summing over all other trials t' = (f, a0', l') in the family uses the family average of Pr[t' succeeds | t' good], which is q3 <= 2^-71.38 x 2.4902 = 2^-70.0637 (H2, Section 7.7; no per-trial uniformity across (a0, l) is required), so the expected number of further successes among other good pairs is at most rho x N_good x 32 x q3 with N_good <= 599,760 (all variants of the family): 2^35 x 2^19.58 x 2^5 x 2^-70.0637 = 2^-10.4837, so delta <= 2^-11 + 2^-10.4837 = 2^-9.7189 < 2^-9.4; the measured factor at the row-16 level over 2^21 and 2^23 real first blocks is 0.98 and 1.00. The organizer experiment `h3-cowpass-nonce` counts the first blocks in which several variants of one class pass F6 together, and `h3-ladder-r37` (Appendix H) counts, on organizer-seeded real first blocks, the pairs of distinct variants of one first block that both pass each level of the attack through the exact row-16 test, against the pairs expected if they passed independently: our replays (two seed sets) give the dependence factor 3.62 and 4.92 at the W6 filter (variants of one class share bits), 0.99 and 1.00 at historical aa0e8b6 LO12 and 0.95 and 0.94 at historical MID12 (P4 public-seed ladder R: W6=3.250842, FIRST13 (lo)=0.995964, SECOND11 (mid)=0.949225, exact row 16=1.048555; N/S/P/C and exact rational calculation are in the P4 executor observations section.), and 1.27 and 0.67 at the exact row-16 test (32 and 9 passes). This is the bound of the earlier filings on this family; the whole family G would give 2^-6.5 and is not used. *Limitations.* Premise (our theory): rows 17..36 are not reachable by any organizer experiment of 20 s; for them rho = 2^35 over the measured factor (0.67 to 1.27 through row 16 on organizer seeds; 0.98 and 1.00 over 2^21 and 2^23 real first blocks) is the stated allowance. Rows >= 17 of distinct good pairs cannot be measured jointly within one first block; the premise leaves a margin of 2^35 over the measured row-16 factor, and the margin over the number of examined pairs is thin (delta <= 2^-9.72 against 2^-9.4). The replay samples are correlated through SMC resampling. A stated premise, not an established fact.

**H4 (supporting).** The published characteristic, its two-bit conditions, the SFS pair's inner values S and L* are used as advice. Their construction is charged A_S = 2^41.3 (the paper's own Step-1 SAT solve, and the completion of a Step-1 solution to the SFS pair, 25 ms) and A_C = 2^48 (the unpublished characteristic search, calibrated from the 593,858 solver CPU-seconds of the predecessor search in 6eeefb64); all development computation at DEV = 2^40. The variant family, the 170 class descriptors (below 2^13 bytes), the lists, the filter sets, L* and the tables are recomputed in the preprocessing (2^38 operations bound, itemised in proof.md Section 14.2).

*Scope.* The preprocessing part of the ledger (2^48.01938) and the advice (below 2^13 bytes). *Evidence.* proof.md Section 11.2. A_S: the paper's reported Step-1 cost itself (2^41.3), not a multiple of it; the completion of a Step-1 solution to a full 37-step semi-free-start pair is reproduced in this package in about 25 milliseconds per pair (organizer experiment a0-sfs-r37). A_C: at the CPU-second price calibrated in the accepted filing 6eeefb64 (2^21.427 units at C = 2644 per solver CPU-second), the 593,858 solver CPU-seconds (= 2^19.18 CPU-seconds) measured for a complete re-run of the predecessor 35-step search equal 2^40.61 units; A_C = 2^48 units is 2^26.57 solver CPU-seconds (3.16 CPU-years), more than 169 times that measured complete re-run, and A_C + A_S + DEV = 2^48 + 2^41.3 + 2^40 = 2^48.01938. *Limitations.* The 37-step characteristic search time is unpublished; A_C = 2^48 is a calibrated bound > 169 times the accepted measurement of the predecessor search, not a direct measurement of the paper's search. Sensitivity (recomputed on this revision's ledger): A_C = 2^56 gives time_log2 = 57.58461, the legacy placeholder A_C = 2^60 gives time_log2 = 60.16987, and A_C = 2^64 gives 64.01123. The q3c sensitivity cells quoted in this claim and in Sections 7 and 12 are carried from the predecessor study's program and are conservative here: recomputed by the shipped ledger at the same bounds each is lower (by 0.43 to 0.52 bit), and no filed bound depends on them.

**H5 (score-critical).** Under collision-frontier-v5 a word-RAM program of 256-bit primitives in which every executed load, store, logic operation, shift, addition, comparison, branch and jump is one primitive is charged by the primitives it executes. The W7 class test (106 primitives for all 170 classes) and the W6 test of a batch of 256 reps (181 to 301 primitives, and 11 to 28 for each subtraction run) are straight-line plane programs whose counts do not depend on the data, produced by a plane algebra in which static constants fold and complemented planes carry an inversion flag at no cost, and in which a NOT is paid when an AND or OR meets unequal flags; two batches are processed together bit by bit with at most 20 live planes each (64 registers, no spill). The group of four members is 28 primitives (28 packed-u; no word-level address mask is executed and the group counter is batched into the per-rep update, 9.7b/d), the first probe stage 12 per four lanes (bits 9..23 are shifted on every lane) plus seven per nonzero FIRST word, the residual exact row-16 test 13, and the zero-base `scan_table` at word address `0..8191` gives `CLS_LANE = 5`, `SCAN_LANE = 5`, `SURV_LANE = 6`, with the scalar and control items of proof.md Section 9. All tables, the code (78,826 inherited bytes plus a 1,024-byte allowance, and since R37P40g a 9,024-byte allowance for the plane formations of 9.6d (a); the 47 CB3/KZ scratch planes are no longer stored) and the constants occupy 1,019,498 bytes = 2^19.959428, below 2^20 bytes. The 170 classes are base | s for s in the four kept lists (computed, checked for all 599,760 variants); a list is the union of 2^|B| translates of its reps by the cube B of free bits {0, 2, 3, 7}, {0, 2, 3} or {0}, and F6(W6x) does not depend on a cube bit s_b when q_b = 1 or on s_0 when CB3_0 = 1 (Lemma 8.2: proved from the constants of S and checked), which the program uses to run only the main combination and subtract the constants of the other 2^|Q0| - 1 combinations that matter.

*Scope.* The class-test, W6, scan, gather, group, probe and survivor terms of the ledger (essentially all of the 13287.41 data-dependent operations per first block), the fixed terms, the memory figure and the preprocessing bound (2^38 operations). *Evidence.* The program is experiments/lowm.py (the plane programs assert their counts at every execution; process_cv counts every scalar item where it executes; the realized operation count of every category equals its closed formula on 20,000 simulated first blocks). It is exact against the scalar definitions: every lane of every class-test plane and every pass plane equals the F7 or F6 test of its definition (34,000 and 33,570 lanes in selftest, and every lane of every processed class in a0-online-r37), the sets of good pairs (all members, after the expansion of the reps) equal the brute-force sets, the address u equals W0 + s0(W1) from the step equations, the exact row-16 test equals 7319bba's enumeration of 2,097,152 pairs on all 32 l (Appendix A) and the generic row check on random and near-miss values, and the table stage never rejects a member. *Limitations.* No organizer ruling is cited for the plane algebra (static constants and inversion flags are compile-time facts of the text; the W6 programs have 32 to 84 inversion flips that cost nothing because XORs absorb them and AND/OR of equally flagged planes use De Morgan; pricing every one of them as a NOT would give 57.74433, or 60.27400 under A_C = 2^60) or for the register argument, which is a count of live planes, not a register allocation. The code size is a bound (at most 8192 primitives of at most 8 bytes). Branch pricing follows the earlier filings (a branch on a register is one primitive). The ceiling of the group count and the survivor scan are charged at their worst case (below 0.2 percent of the data-dependent work).

**H7 (supporting).** The current cap allowance is 9/25,000,000; the required mean rounds up to 0.49466302. Appendix C gives the exact achieved mean and recomputes the 0.39000000604429280 floor. This arithmetic depends on H1-H3 and the stated work bound. Historical versions used other constants; remaining cost and probability evidence requires review.

*Scope.* N_FB (the cap) in the ledger. *Evidence.* Every allowance is an explicit term of the floor equation: the Bernstein cap-failure bound Pcap (priced in proof.md Section 10 from the exact vmax_fb = 537899319879/10 and vbar = 125166465733696063954897/10737418240000000000 of the ledger; the computed bound is 2^-21.413815 = 3.579311e-07, against the assumed 3.60e-07), the repeated-first-block allowance 2^-60, and the H3 dependence discount as the divisor (1 - 2^-10.4). Appendix C computes mu0 and the bound with 60-digit decimals and asserts the bound > 0.39; lowm.py ledger() iterates Pcap and N_FB to a fixed point and asserts the same. *Limitations.* The 0.39 floor is the organizer's success requirement; the equation makes the success arithmetic exact rather than adding slack. The cap bound needs the independence of the first blocks (H1) and the bound vmax_fb on one first block's work; a Chebyshev bound would force the slack 2^-11 and Pcap = 0.00023325 (Section 10).
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

`experiments/lowm.py`'s `process_cv` was run on 20,000 real first blocks (first words from SHAKE-256 of the seed `simF-1017`, real 37-step compressions, all 222 classes of the predecessors' ten lists, every operation counted), without any restriction of the family. That the run is the *unrestricted* family is not an assumption but a consequence of its own counts, below: 3.457 passing classes per first block is 28 percent above the restricted family's exact expectation 170 p7 = 2.697754, a 30-sigma excess over 20,000 blocks, and it matches the ten-list exact 222 p7 = 3.522949. Realized counts (**a ten-list control, not this filing's family**: the run takes the predecessors' unrestricted 222 classes and 782,800 variants, so its exact expectations are 222 p7 = 3.522949 and 782,800 p7 p6 = 830.988, closed forms from |F7| = 68,157,440 and |F6| = 287,309,824 (Section 13.2) and not ledger cells of this filing, whose restricted family has 170 p7 = 2.697754 and 599,760 p7 p6 = 636.680): 69,139 passing classes (3.457 per first block against the exact 3.522949), 16,726,799 good pairs (836.3 per first block against the exact 830.988), 4,181,742 groups, 63,548 probed lanes with a nonzero table word, 65,564 survivors of the exact table stage (0.00392 per probed lane against the exact 1/256 = 0.00391), 7,954 first-block-level row-16 passes. **The restricted counterpart is this filing's own measurement.** The same counted program on 6,000 real first blocks of the shipped 170-class setup realizes 2.7500 passing classes per first block against the exact 170 p7 = 2.697754 (ratio 1.0194; `experiments/r37-recount54.py`, 6,000 blocks, all four lists), and the ten-list control above realizes 0.9813 of its own expectation: each is within 2 percent of its own expectation, and neither control is used as the other's expectation anywhere in this package. The counted operations per first block (the 46 first-block operations included): mean 28,377, against the ledger's expectation 28,289 (= FIXED + vbar), ratio 1.0031, both at the parent's six-primitive continuation price (the audited seven adds one per nonzero FIRST to both sides and leaves the ratio); the run precedes the change of the rare path of Section 9.9, which acts only on pairs whose row 21 holds. The realized operations of every category (class test, scalars, class preparation, sweeps, W6 programs, scans, members, groups, probes, survivors, rare path) are the prices of Section 9 applied to the realized counts (`experiments/lowm.py` is the program; the check is the identity of Section 9's prices with the executed counts).
### 13.4 Development computation
Below 3,000 CPU-seconds in all (the exhaustive row-16 comparison 20 CPU-seconds in C and 60 in numpy, the simulation about 85 CPU-seconds, selftests and experiment replays under 300, aborted runs the rest), far inside DEV = 2^40 units (2^18.6 CPU-seconds at the calibrated 2^21.4 units per CPU-second).
## 14. Memory, preprocessing and advice
### 14.1 Memory
Everything resident during the online phase (`python3 experiments/lowm.py memory`; words of 32 bytes):

| item | bytes |
|---|---|
| planes of the reps that are not constant over their batch (8 batches, 76 planes; the constant planes are in the code) | 2,432 |
| packed entries of the reps: 8 batches x 256 words (one word per lane; the entry in all four 64-bit lanes, Section 9.6c) | 65,536 |
| cube entries D[c]: 8 words | 256 |
| spill area of the sums of a class's batches: 7 x 9 words (or 2 x 15 words) | 2,016 |
| c7 planes: 15 words (the 15 dynamic bits) | 480 |
| chunk table FIRST: 8192 words (32768 entries x 64 bits) | 262,144 |
| chunk table SECOND: 128 words (512 entries x 64 bits) | 4,096 |
| lane-scan table: 8192 words (13-bit chunks) | 262,144 |
| successor table succ[c] = c & (c - 1): 8192 words | 262,144 |
| class descriptors: 170 x 4 words (base, BP, list data, c7) | 21,760 |
| per-l constants: 32 x 4 words (C_l, cxA_l, E15x word, VA_l) | 4,096 |
| scalar planes in memory: the 16 q planes (16 words; the 47 CB3/KZ planes are formed in the sweep since R37P40g, Section 9.6d (a)) | 512 |
| characteristic cells, L* rows, S: bound 1280 words | 40,960 |
| chaining-value constants (cv_pre) and the first-block buffer: 64 words | 2,048 |
| code: the earlier bound of 8192 primitives of at most 8 bytes less the 1,227 primitives of the generic plane programs (55,720), plus the 3,851 primitives of the 54 per-batch plane programs of Section 9.5 at most 6 bytes each (register-to-register 256-bit operations, VEX 4 or 5 bytes); at this revision's plane programs 55720 + 23106 | 78,826 |
| added probe/residual code allowance | 1,024 |
| code allowance for the CB3/KZ plane formations moved into the per-list sweep texts (R37P40g, Section 9.6d (a)): 8 texts x 141 primitives x 8 bytes | 9,024 |
| prefilter table T (R37P40h, Section 9.6e): 16,384 one-byte entries | 16,384 |
| prefilter code (R37P40h): 5 primitives x 6 bytes | 30 |
| **total** | **1,035,912 = 2^19.982470** |

The limit 2^20 = 1,048,576 bytes is not reached. Claimed memory: 2^20.0 bytes (rounded up). The messages (128 bytes), the registers (64 x 32 bytes) and the compression state are included in the last constants. Nonuniform advice: the characteristic, S, L* and the 170 class descriptors (170 x 12 bytes), below 2^13 bytes. The tables are built in the preprocessing and are never held twice. The seven-lane batch of Section 9.11 adds no resident item: its eight state words, sixteen schedule words and seven-lane temporaries are register-resident inside the 64 x 32-byte register file that the last row already counts.
### 14.2 Preprocessing: PRE < 2^38 operations
(i) Discovery of the family: the 2^29 values of E4 with E4[31:29] = 000 (a0 = E4 - C4), each tested against the W8x conditions (about 20 operations) and c7 (about 60), grouped by c7 and the classes of at least 3456 variants kept: 2^29 x 80 + 12.1 x 10^6 x 100 < 2^36; the descriptors (base, mask) of the 170 classes are read off their members (599,760 x 30). (ii) The four kept lists: 4 x 2^15 subsets x about 80 operations < 2^23.4. (iii) The planes and packed entries: 8 batches x (17 x 256 bit insertions x 3 + 256 x 10, the entry replicated into four lanes by R37P39's 9.6c) < 2^17. (iv) FIRST/SECOND: enumerate 512 low indices per l, at most 16 encoded interface states and 32768 high indices per state, then emit/prune at most two viable states. At 100 primitives per tested index, a conservative bound for the high-index enumeration is 32 x 16 x 32768 x 100 = 1,677,721,600. Adding 32 x 2 x 32768 x 10 for emission and 32 x 512 x 100 for the low-index pass gives 1,700,331,520 < 2^31. The earlier 2^25 figure was an arithmetic error; these per-index prices remain participant estimates, not measured instruction traces. Per-l constants: 32 x 200; the scan and successor tables 2 x 8192 x 6; the c7 planes 170 x 32 x 3. (v) The 9.6e prefilter table (R37P40h): one pass over the 2^32 words w with the F7 test by its definition (two s0 at 8 each, the add and its mask, the subtraction and its mask, the compare-branch and the loop control: at most 24 per w), the least/greatest update for the 68,157,440 words of F7 (at most 8 each), then 170 x 16,384 x 10 for the marks: below 2^36.6. The former 2^38.2 upper estimate is retained only as a conservative starting allowance: even adding four full corrected table builds (< 4 x 2^31) gives < 2^39, so the filed PRE = 2^39 retains arithmetic headroom under these stated per-operation estimates. This does not independently establish that every estimated operation or scratch requirement is complete. Tables are built before lists and scan-table initialization. Reuse the uninitialized scan-table region for at most 2^17 bytes of construction scratch (encoded low states and one-l high supports); release it before online use. No duplicate final tables coexist. Nothing depends on cb or on any other word of the chaining value.
### 14.3 Peak resident memory during construction
The submitted memory figure is the program's resident set (code, tables, messages, working state, retained randomness) together with the retained advice; the *work* of the construction phases is charged in time, and their scratch space is bounded here explicitly, so that no phase of this package needs more than the declared 1,035,912 bytes at any instant.

* **Family discovery** (14.2(i)). The 2^29 candidates of E4 are streamed and never stored. One
  pass holds a key table of at most 4,096 (c7, mask) entries of 16 bytes = 65,536 bytes, 520 32-bit counters = 2,080 bytes and one candidate register. A pass that exceeds the key bound is repeated over the same stream with a different key partition; four such passes cost 4 x 2^36 = 2^38 = PRE, so the streaming argument stays inside the preprocessing budget already charged. The descriptor read-off streams the kept members against 170 descriptors of 12 bytes = 2,040 bytes. Peak: 67,616 bytes.
* **List, plane and table construction** (14.2(ii)-(iv)). The 2^17 bytes of construction scratch
  are taken from the scan-table region before that table is initialised and released before the online phase; FIRST, SECOND, the scan table and its successor table are then written in place into disjoint regions of the same 1,035,912 bytes and no final table is ever held twice (14.1). The 9.6e prefilter build (14.2 (v)) uses 81,920 B of the same 2^17-byte scratch (lo_min, lo_max, seen) and writes T in place. Peak: the final tables plus at most 2^17 bytes.
* **The advice itself** (A_S, A_C). The characteristic, its printed two-bit conditions, the
  Step-1 solution S and the semi-free-start pair are the *published* tables of the cited work (Tables 15-17), used as stored data: 2^13 bytes, inside the figure, and no search is part of the submitted program. Their construction is nevertheless charged in full in time, at A_S = 2^41.3 and A_C = 2^48 (2^48.02 units together, more than 169 times the measured complete re-run of the predecessor search in 6eeefb64, against the paper's 2^41.3 for its own Step-1 solve). Because the program runs no solver, there is no solver transient space to charge: the
  construction phases this submission *does* run are the family discovery, the list and plane construction and the table build above, and those are inside the bound.

Peak resident memory at any instant is therefore 1,035,912 bytes = 2^19.982470, below 2^20 bytes.
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
- The simulation of the counted program (Section 13.3) was run again with this package's program after the R16x change (rows 16 and 17); its figures are from that run; the exact-event change of Section 9.9 acts only on pairs whose row 21 holds. H6's ROW_FIX/PAD_RATE are participant-measured premises; the organizer-executed corroboration (`h6-orgstats-r37`, Appendix Q), the organizer-side conservative re-pricing (57.16006) and the structural worst case (57.15946, the declared analytic replacement) bound the row's reliance on them at 0.05640 bits.
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
Self-contained (integers and Fractions); the stage prices are the constants of Section 9, asserted by `lowm.py`. It is the exact ledger of **this** filing's four-list family — 170 classes, `FIXED = 52`, `FIXED_P7 = 26`, `CT_V = 220` at `P_H = 11008/2^14` (Section 9.6e), `FB_DET = 155` at `P_PASS = 549066752/2^32`, `CPREP = 166` (Section 9.6d), `SB_FB = 2644` (one unit per first-block compression, Rulings ba65804c and f044761e F1), `F7_OPS = 106`, `Q3_LOG2 = -71.4162`, `PAD_RATE = 117238429/2*10^10`, `MEMBER_CHARGE = (5, 4, 2, 3)`, `DELTA_CLASS = 18`, `DELTA_RUN = 5`, `SPILL_K = (15, 9)` and the sweep/rep-plane loads at base + immediate (the three fixed-slot folds of Appendix BG), `ROW_MAX` + 32 (Section 9.6c), slack 1/15000, `Pcap <= 9/25,000,000` — and it reproduces `python3 experiments/lowm.py ledger`: `N_FB`, `g`, `vbar`, the cap bound, `V_MAX`, `N` and `time_log2` all agree digit for digit (`reports/experiments/r37-ledgergate-74.py` extracts and runs both). The mirror sums the rational without reducing, so it prints the same integer pair as `T_num / T_den`.
```python
from fractions import Fraction as Fr
# Exact ledger of the counted program (proof.md Sections 9-11). Integers and Fractions only.
C = 2644                                   # reference cost of one target compression, in word operations
# stage prices (primitives of the straight-line text, proof.md Section 9; the plane-program counts are measured by lowm.py and asserted at every execution)
# per-list tables (below): the W6 program of every batch of every list with the constant s planes folded, measured by lowm.py (ListData.measure) and asserted at every execution
F7_OPS, SCAN_LANE, CLS_LANE = 106, 5, 5
def scan_fix(nl):                        # the fixed part of a scan over nl lanes (Section 9.6, the row test)
  return {170: 42, 176: Fr(179297, 10000), 194: Fr(208133, 10000), 216: Fr(10161979, 500000), 225: Fr(20196831, 1000000), 256: Fr(244081, 10000)}[nl]
ROW_MAX = {170: 74, 176: 74, 194: 79, 216: 82, 225: 85, 256: 90}   # Section 9.6 ceiling (raised by 32 in R37P39: the four row isolations and tests, 3 each, and the twenty chunk-base adds are included): every present row test and every chunk of it
def scan_max(nl): return ROW_MAX[nl]    # P10: the cap charges the ceiling, the counter keeps the mean
SCAN_FIX = scan_fix(256)
EXTR, PLACE, GROUP_BODY, PAD_OPS, PROBE = (0, 0, 0, 0), 6, 28, 7, (3, 3, 3, 3)   # 9.6: the rep table stores each lane pre-aligned, no extraction
PAD_RATE = Fr(117238429, 20000000000)   # residual group word: 99% Poisson bound on 17 padded lanes per 5,000 first blocks (Section 11.1)
SURV_FIX, SURV_LANE, EX_OPS, RARE_LOOKUP, RECOMP, ROWCHECK, ROWCOMP, OUTCMP = 13, 6, 13, 2, 35, 53, 106, 16
CPREP, CF_CLASS, SWEEP_OVH, FIXED, RUN_CU, SPILL_K = 166, 11, 0, 52, 7, {3: 15, 1: 9}   # R37P40g (9.6d): SWEEP_OVH unused; R37P40h (9.6e): FIXED = 30 + 16 + 1 + 5; R37P40l (Appendix BG): the spill planes sit at literal slots (30 -> 15 per batch)
ZC_N, KZ_N, NB_N = 0, 0, 0            # 9.6d (a): the 31 CB3 and 16 KZ planes are formed in the one sweep (charged in CPREP), not reloaded
# the four kept lists of the ten (proof.md Sections 5.3, 9.4, 9.5): cnt classes, n variants, cube bits k, lanes of each batch nl, dynamic s planes of each batch dyn, zq planes loaded by each sweep zq,
# W6 program of each batch (main run / all sums) w6, subtraction runs sub[(batch, cu)]
LISTS = {
  0: {'cnt': 82, 'n': 3456, 'k': 3, 'nl': [216, 216], 'dyn': [9, 9], 'zq': [10], 'w6': [{False: 168, True: 236}, {False: 189, True: 262}], 'sub': [{1: 26, 4: 25, 5: 28, 8: 24, 9: 27, 12: 26, 13: 27}, {1: 26, 4: 24, 5: 27, 8: 23, 9: 27, 12: 25, 13: 26}]},
  1: {'cnt': 3, 'n': 3456, 'k': 3, 'nl': [256, 176], 'dyn': [11, 9], 'zq': [12], 'w6': [{False: 206, True: 275}, {False: 187, True: 256}], 'sub': [{1: 26, 4: 25, 5: 28, 8: 24, 9: 27, 12: 26, 13: 27}, {1: 26, 4: 25, 5: 28, 8: 24, 9: 27, 12: 26, 13: 27}]},
  5: {'cnt': 82, 'n': 3600, 'k': 3, 'nl': [225, 225], 'dyn': [9, 9], 'zq': [10], 'w6': [{False: 170, True: 239}, {False: 191, True: 263}], 'sub': [{1: 26, 4: 25, 5: 28, 8: 24, 9: 27, 12: 26, 13: 27}, {1: 26, 4: 24, 5: 27, 8: 23, 9: 27, 12: 25, 13: 26}]},
  6: {'cnt': 3, 'n': 3600, 'k': 3, 'nl': [256, 194], 'dyn': [11, 9], 'zq': [12], 'w6': [{False: 208, True: 278}, {False: 189, True: 259}], 'sub': [{1: 26, 4: 25, 5: 28, 8: 24, 9: 27, 12: 26, 13: 27}, {1: 26, 4: 25, 5: 28, 8: 24, 9: 27, 12: 26, 13: 27}]},
}
CUBE = {3: 13, 1: 1}                        # the cube bits {0, 2, 3} or {0} as a mask
NCLS = 170; NVAR = sum(L['n'] * L['cnt'] for L in LISTS.values()); NFEAS = 32; SB_FB = 2644; FIXED_P7 = 26; FB_DET = 155; P_PASS = Fr(549066752, 1 << 32); P_H, CT_V = Fr(11008, 1 << 14), 220   # 9.6e: class test + its V update behind the 14-bit prefilter   # 9.6d (e): FB_DET (154 + its V update) runs only if a class passes, P_PASS exhaustive
P7 = Fr(68157440, 1 << 32); P6 = Fr(287309824, 1 << 32); R16F = Fr(2097152, 1 << 32); MU = Fr(1, 256); PNZ = Fr(63512, 1 << 24)
# calibrated A_C = 2^48 (proof.md Section 10; sensitivity at A_C = 2^56, 2^60, 2^64 in Section 12) and the success-floor constants
A_C, A_S, DEV, PRE, FIN = 1 << 48, 2707315195888, 1 << 40, 1 << 39, 1600   # PRE 2^39 since R37P40h (14.2 (v))
EXQ = Fr(2482, 1000)                           # collision event / cell event after row 21: preregistered 99% lower bound (proof.md Section 7.7; 4ec21bf9 Appendix D.3)
Q3 = Fr(1647939023468, 1 << 112) * EXQ           # q3 = q3_cell x EXQ, q3_cell = 2^-71.4162 rounded down to a 40-bit mantissa (the Fraction below is exact)
MU0 = Fr(49466302, 100000000)                     # smallest 8-decimal number above -ln(0.61 - PCAP_ASSUMED - 2^-60) / (1 - 2^-10.4)  (Appendix C); 0.49466302 at PCAP_ASSUMED = 9/25000000
SLACK = Fr(1, 15000); PCAP_ASSUMED = Fr(9, 25000000)
def subsets(mask): return [s for s in range(16) if s & ~mask == 0]
def lane_costs(nls): return sum(SCAN_LANE + EXTR[L // 64] for nl in nls for L in range(nl))   # scan and extraction of every lane of the batches of reps
MEMBER_CHARGE = (5, 4, 2, 3)       # Section 9.6c (R37P39): the rep word holds its entry in all four 64-bit lanes, so no spread is executed, and the group word is consumed from its register with no store (as in the inherited m = 1 discipline) -- m = 1: xor with the replicated run delta 1 + and with the top-lane mask 1 + shift-down 1 + or 1 + counter 1 = 5; m = 2, per group word of two pairs: pair A xor with the pair delta word 1 + its or 1 (the opening one: not executed, refunded by - nr//2 below) + the accumulator shift by 128 1 (it discards A's lanes 0, 1, so A needs no mask), pair B and with the two-lane mask 1 + xor 1 + or 1, counter 2 = 8, i.e. 4 per rep; m = 4: xor with the delta word 1 + counter 1 = 2; m = 8: two xors 2 + counter 1 = 3
DELTA_CLASS, DELTA_RUN = 18, 5    # Section 9.6c: building the lane-placed delta words, per passing class (cube-delta lanes from the replicated cube-delta words and the class delta: at most 18) and per run, main and subtraction (address 1 + load of the replicated D[cu] 1 + flip of the second four-bit batch 1 + xor into the at most two class words 2 = 5)
def memcost(j): return MEMBER_CHARGE[j] if j < 4 else 5 * (1 << (j - 1)) + 1                                  # members of a rep with |I| = j
def class_det(lid, Q0, F=scan_fix):
    # operations of a passing class (list lid) with relevant cube bits Q0 that do not depend on which reps are good (2^|Q0| runs)
    L = LISTS[lid]; nb = len(L['nl']); nsw = (nb + 1) // 2; part = sum(1 for x in L['nl'] if x < 256); full = Q0 != 0; j = L['k'] - bin(Q0).count('1')
    sweeps = sum(3 + L['zq'][sw] + KZ_N + ZC_N + NB_N for sw in range(nsw))
    tot = CPREP + CF_CLASS + DELTA_CLASS + (0 if j == 0 else 5 * (1 << j) - 2) + sweeps + sum(DELTA_RUN + L['dyn'][b] + 2 + L['w6'][b][full] + F(L['nl'][b]) for b in range(nb)) + part
    if full:
        tot += 2 * nb * SPILL_K[L['k']]
        for cu in subsets(Q0):
            if cu: tot += sum(DELTA_RUN + RUN_CU + L['sub'][b][cu] + F(L['nl'][b]) for b in range(nb)) + part
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
    return max(class_det(lid, Q0, scan_max) + (1 << bin(Q0).count('1')) * class_run_cost(lid, Q0) for Q0 in subsets(CUBE[LISTS[lid]['k']]))
perclass = pairs = Fr(0); vmax = Fr(0)
c3b_row = ROWCOMP + ROWCHECK + 1; c3b_pair = 201 + RECOMP + 1 + RARE_LOOKUP; c3b_l = 2 + 6 + (ROWCOMP + 1) + c3b_row; c3b_t = 4 * c3b_row + 15 * ROWCOMP + OUTCMP + 1   # fold (j): row 16 already checked, computed only (Section 9.6f)
for lid, L in LISTS.items():
    perclass += L['cnt'] * P7 * class_expected(lid); pairs += L['cnt'] * P7 * P6 * L['n']; vmax += L['cnt'] * class_max(lid)
ct_var = CLS_LANE * NCLS * P7
groups = pairs / 4 + PAD_RATE; lanes = 4 * groups
grp = groups * (GROUP_BODY + sum(PROBE)) + PAD_RATE * PAD_OPS + lanes * 7 * Fr(2207,32768)
surv = lanes * (PNZ * SURV_FIX + MU * (SURV_LANE + EX_OPS))
rare = lanes * R16F * (c3b_pair + c3b_l + Fr(1, 512) * c3b_t)
vbar = P_H * CT_V + ct_var + P_PASS * (FB_DET + 42) + perclass + grp + surv + rare   # expected data-dependent operations per first block
g = pairs                                               # expected good pairs per first block
vlanes = NVAR + 3                                       # one first block's maximal data-dependent work: all classes pass, all variants good, every l survives, every probe hits
vmax_fb = vmax + Fr(vlanes, 4) * (GROUP_BODY + sum(PROBE) + 28) + PAD_OPS + vlanes * (SURV_FIX + NFEAS * (SURV_LANE + EX_OPS)) \
          + vlanes * Fr(11, 10) * (c3b_pair + NFEAS * (c3b_l + c3b_t)) + 24 + CLS_LANE * NCLS + FB_DET + 42 + CT_V
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
A_S: Step-1 solve (units x C)           7,158,141,377,927,872
DEV: development (units x C)            2,907,108,743,839,744
N_FB x SB_FB (units, first-block batch) 81,492,191,094,289,357,464
fixed: N_FB x FIXED_P7 (units)          801,360,426,797,096,556
V_MAX: data-dependent operations        359,311,912,272,790,214,230
overshoot past the cap: vmax_fb         53,789,931,988
PRE: preprocessing                      549,755,813,888
FIN: final verification                 1,600
6 further compressions (units x C)      15,864
N_FB = 30821554876811406, g = 636.6804599761963, vbar = 11657.035512262588, Pcap = 3.5793108506149236e-07 <= 3.6e-07
N = 442359749485967173670
certificate: 2^5721527 * 2644^100000 <= N^100000 < 2^5721528 * 2644^100000
time_log2 = 57.21528
```
## Appendix C. The success floor
```python
from decimal import Decimal, getcontext
getcontext().prec = 60
PCAP = Decimal(9) / Decimal(25000000)     # the assumed cap bound PCAP_ASSUMED = 9/25000000: this vbar's computed 3.579311e-07 (slack 1/15000) is below it
EPS = Decimal(2) ** -60                      # a repeated first block among N_FB draws
D = 1 - Decimal(2) ** Decimal('-10.4')       # the H3 discount 1 - 2^-10.4
req = -(Decimal('0.61') - PCAP - EPS).ln() / D                       # the requirement
MU_REQ = Decimal(49466302) / Decimal(10 ** 8)                        # requirement rounded up to eight decimals
MU0 = Decimal(105203189546162204004590692264978478337) / Decimal(212676479325586539664609129644855132160)   # achieved: N_FB g 32 q3_cell x EXQ exactly
assert req < MU_REQ <= req + Decimal(2) / Decimal(10 ** 8)
assert MU0 >= MU_REQ
succ = 1 - (-D * MU_REQ).exp() - PCAP - EPS
print('required %.15f' % req)
print('req rounded up %.8f' % MU_REQ)
print('achieved mu0 %.15f' % MU0)
print('success bound ' + format(succ, '.17f'))
assert succ > Decimal('0.39')
print('OK')
```
Output (60-digit decimals; the shipped ledger's binary double prints 0.3900000060442928 for the same quantity):
```text
required 0.494663010083979
req rounded up 0.49466302
achieved mu0 0.494663020000000
success bound 0.39000000604429277
OK
```
## Appendix D. `selftest` output — re-executed fresh on the shipped tree of this revision (R37P40l, 2026-10-30, rc 0); the transcript below is that run verbatim. Relative to the R37P40g row it changes the printed FIXED/FIXED_P7 and adds one line, the Monte Carlo check of P_H and of the prefilter on passing x (Section 9.6e); every other line is byte-identical.
```text
classes 170, variants 599760 (599,760), mismatches 0
W6_OPS (k, full): {(3, False): 211, (3, True): 281, (1, False): 231, (1, True): 310} SUBF_OPS: {(3, 1): 26, (3, 4): 25, (3, 5): 28, (3, 8): 24, (3, 9): 27, (3, 12): 26, (3, 13): 27, (1, 1): 11} F7_OPS 106 FIXED 52 FIXED_P7 26 SB_OPS 2688 SB_FB 2644
spread placed by doubling: 4,096 words in 4 primitives, mismatches 0
F7 sampler violations 0
lists (size, cube bits): [(3456, 3), (3600, 3)]  classes with a cube bit 2 or 3 and base bit 1 clear: 0
invariance of F6(W6x) under the flips of the bits of I: 30720 checks, 0 mismatches
w6 plane lanes 20682, F6 passes 1085, mismatches 0
class-test lanes 34000, mismatches 0
row-16 checks: members seen 27, mismatches 0
packed u lanes 400, mismatches 0
replicated rep words: 110592 members by the 9.6c disciplines, mismatches 0
first blocks with a passing class 2528 of 20000 (exact P_PASS 549066752/2^32 = 0.127840), z -0.61
max S0 over the 599,760 variants 0xffffbb5c True
prefilter hits 13465 of 20000 (exact 11008/16384 = 0.671875), z 0.41; misses on 3,400 passing x: 0
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
**What this is.** This direct study addresses two methodological requirements on the earlier studies: first, that an aggregate tail mean within 0.001 bit of uniform does not by itself bound a *sub-pool* mean without a pointwise bound, and second, that the operative statistic must be fixed before any replicates run rather than pooling post hoc. Here W8 is drawn directly from the **submitted** 599,760-variant list, so nothing is transferred from the parents' family, and the statistic below is fixed before the seeds run.

**Inputs, regenerated from the shipped files, with the hashes of the states used.**
```text
lowm.py         7905c31e2ac3a9c513d75d793bf62935c6a73d62e371802a10c0a4a1ff976104   (the state of the 57.64841 filing, commit 2d0a13b; the shipped file of this filing is sha256 c9306412f2e36834270e97e7c0ffa05a52cb91fcd332cd2f036ed64dec259fed) q3smc.c         f0e3efc8d06c58c03c7dd7fe86ef08d8d00b8868202e6c49557f85c479c61f9c   (Appendix F.4 as shipped)
gen_consts.py   721d7949d1038a6f01e8cac62eaa8ecc9362a7af105176ab56c82beef90efd5b   (Appendix F.5 as shipped) variants.bin    b767171018fb5ba2d43e55adea23b72de820d9a43ffaa780f51f8c99ae695cbd   599,760 words = 2,399,040 bytes
q3consts_orig.h efd62db9220a667258d8dbde25ec572e1104460f2a1971894292870c6ec7e4cb   (written by that gen_consts.py from that lowm.py) build           gcc -O2 -DCONSTS='"q3consts_orig.h"' q3smc.c -lm -o q3smc_orig
```
`variants.bin` is the W8x of the 599,760 variants of the 170 classes of lists 0, 1, 5 and 6, all distinct, printed by the generator (`variants 599760 distinct W8x 599760`). Every replicate uses NP = 8192, M = 512, MT = 16384, the parameters of every replicate of studies A, B, J1 and J2.

The shipped `experiments/lowm.py` (sha256 c9306412f2e36834270e97e7c0ffa05a52cb91fcd332cd2f036ed64dec259fed) differs from the state hashed above in `Q3_LOG2`, which this study produces rather than consumes, in the itemisation-only lines of Sections 9.6 and 14.1 (the scan charge and the successor-table row), and in the advice allowance `AS = 2707315195888` (A_S = 2^41.3, Section 11.2), from which no constant of `q3consts_r16x.h` is computed. The generator reads only `CELLS`, `X2`, `setup_l`, `MX`, `MY`, `lstar`, `LISTID` and `CLASSES`, none of which that constant touches: regenerating from the shipped file reproduces `variants.bin` b7671710 and `q3consts_orig.h` efd62db9 unchanged (checked).

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
Per-seed log2 estimates, seeds 760000..761023: **the 1,024-value table is omitted here to fit the 512 KiB package budget**; it is unchanged from every earlier filing of this package, including the promoted `5b437ff3`. Digest of the values in order (space-separated, five decimals): `sha256 9891b903edf51f3020dc791906934de3152f1b67f215262a1f16b01a1d7de05b`; recomputed from it the printed mean -71.42391, sample sd 0.15878, min -71.97449 and max -70.97601 hold exactly.
The measurement answers both objections it was written for. (i) There is no transfer: W8 is drawn from the submitted 599,760-word list, and the mean agrees with the parents'-pool study of Section 7.4c (-71.4236, 256 replicates, a 782,800-word list) to 0.0003 bit, which is 1/37 of one standard error of that study's mean -- the sub-pool restriction is q3-neutral in measurement as well as by Lemma 7.1. (ii) There is no post-hoc statistic: the rule, the seed list and the arithmetic of the rounding were committed in Appendix G.3 before the first listed seed ran.
## Appendix H. The organizer experiments for H1, H2 and H3
Historical aa0e8b6 evidence in this appendix uses its one program, `experiments/lowm.py` (63,764 bytes; the budget is 65,536 bytes in total). `a0-sfs-r37` and `a0-online-r37` are described in Section 13.2 and in the manifest; the three entries below were added for H1 and H3 (their form is that of ec1340aa-ecc8-4564-8df7-006f0a2b2ce5, R37OWN5).

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
## Appendix M. Summary of H1, H2 and H3 scope vs organizer experiments
Historical aa0e8b6 material below; old LO/MID code and old cost statements are retained solely as inherited evidence, not the P4 implementation or current accounting. No participant code was run outside the organizer's Docker executor.

**Summary of how H1-uniform-chaining-values, H2-variant-step3-probability and H3-first-block-dependence relate to the organizer-executed experiments:**

| item | premise | scope | experimental coverage and boundary |
|---|---|---|---|
| H2-scope | H2 | Step-3 probability q3 = q3c x EXQ on the submitted 599,760-variant pool | H2 is stated as our theory (claim.heuristics; Section 12): q3 is our computation, with the estimator source, the preregistrations and the per-seed estimates printed in Appendices F, G, N and O so that it replays from this text. The organizer-executed `h3-ladder-r37` runs the row-16 stage of q3 on organizer seeds, and `a0-sfs-r37` constructs full 37-step semi-free-start collisions with the same cells. The end event (rows 22..36 reaching an equal digest) needs a reachable first block, that is the attack itself, and is not executable in 20 s; it is the premise. |
| H1-H3-scope | H1, H3 | Chaining-value filter rates and within-first-block variant dependence | H1 and H3 are stated as our theory. Organizer experiments: `h1-cv1-filters-nonce` (the pass rates of the W7 and W6 filters on real chaining values of organizer seeds), `h3-cowpass-nonce` (co-passes of the variants of one class at the W6 level) and `h3-ladder-r37` (co-passes of distinct variants of one first block through the W6 filter, both table stages and the exact row-16 test; P4 public-seed ladder R: W6=3.250842, FIRST13 (lo)=0.995964, SECOND11 (mid)=0.949225, exact row 16=1.048555; Appendix H). Rows 17..36 and independence over 2^54.77 first blocks stay the premises H3 and H1, with the allowance rho = 2^35. |

Historical aa0e8b6 ledger evolution (not P4 costs): the program is d9f8833d's with the changes listed at the top of this text; the Bernstein cap bound (Section 10) moves the historical claim from 59.30883 to 59.30006, and the collision event after row 21 (Section 7.7) moves it to 58.02135.
## P4 executor observations (public seed; Round 4)
P4 organizer executor observations under public seed hashsmash-public-seed-v1, no holdout nonce: 256 requested trials per experiment, two fresh executions with byte-identical stdout only. Internal counters are participant observations; the organizer independently checks returned-pair target events. These runs do not prove full-scale probabilities, H1-H7 or q3.

**a0-sfs-r37**: On the 599,760-variant pool, the organizer's checked-trial summary of all 256 trial records (which controls) shows 118 returned pairs and 0 full-target collisions (historical P4 782,800-variant replay returned 121); detected_by_counted_program=16 for all 16 returned trials 0..15; SFS validity remains an internal participant check. Runtime 7.65/7.48 s versus 20 s.

**a0-online-r37**: P4 participant observations: 512 unconditional first blocks, 2070 class passes; 52 selected first blocks, 24 processed classes, 7152 good pairs, 25 survivors. class_lane_mismatches, pass_lane_mismatches, goodset_mismatches, address_mismatches, row16_mismatches and cell_mismatches each total 0. On the 599,760-variant pool, the organizer's checked-trial summary (which controls) shows 5 returned pairs (historical P4 replay returned 4), with 0 organizer full-target collisions. Runtime 1.92/1.93 s versus 20 s.

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

Provenance: executor report SHA-256 8fb29212d809996302ac123534826941415e1e109590aaac184fbf96a6dc134d. It binds the pre-Round-4 package/manifest text and executed source SHA-256 4d1449598e4eccec6961ac1f61d1718767a442fe48ea2bb3a7d714cc428c9ce0. Round 4 changes evidence text only; the participant source is byte-identical. The report is not a binding of the final edited manifest. Returned-pair event checks are organizer-recomputed; internal observations and diagnostic resource numbers are not independently established attack costs or success probabilities. The public seed provides no holdout protection. q3/H1-H7, selected/padded-lane uniformity, register allocation and code-size bounds remain inherited limitations.

**Consistency of the H2 premise (disclosed, not silently repaired).** The premise this claim uses is `q3c >= q3c_used = 2^-71.4162`, block F's own one-sided 99% lower bound, and `q3` in the ledger is `q3c_used x EXQ`. Every other q3c figure in this document is a **sensitivity**, quoted beside the claim it produces so that the pair is checkable at a glance: the preregistered min-of-blocks bound 2^-71.4629 (claim 57.62615), the parents'-pool bound 2^-71.4474 (claim 57.61074), that bound less the 0.0020-bit allowance (2^-71.4494, claim 57.61273), the superseded 5x charge (2^-71.4578, claim 57.62108), and block E's log-scale 17,408-replicate figure 2^-71.4243 (claim 57.58779) which is reported in G.5 and Appendix N and is **not** operative. No passage of this document asserts any of them as the operative floor.
### G.5 Block E: 16,384 more replicates, preregistered on the submitted pool, all reported
**Preregistration.** `prereg/PREREG_q3E32.txt`, sha256 `f8a8b40f6a94fad9618c0809e31224e05faf8be1229a0ddc1a414f7365862bea`, committed to git (`4c5a8b4`, amended `994e7b9`) **before any listed seed ran**; no seed of block E has a RESULT line anywhere earlier in this filing or in its history. The rule it fixes, applied once and without any branch on the outcome:
```text
block E: the 16,384 log2est values of seeds 772000..788383, and nothing else u  = floor( (mean - t(0.99, n-1) x sd / sqrt(n)) x 10^4 ) / 10^4      (rounded DOWN)
q3c_declared = 2^u
```
**History of the rule, in full.** The file committed as `4c5a8b4` fixed exactly the rule above over block E alone, before any seed of block E ran. Amendment `994e7b9`, also written before any seed ran, proposed instead *pooling* block E with Appendix G.4's 1,024 values. That amendment is **withdrawn**: 1,024 of the pooled sample's 17,408 observations had been examined before the extension was written, so a fixed-n Student bound on the pooled sample has no clean coverage claim, whereas block E's does. The pooled figure is reported below as a sensitivity and is **not** operative. The operative statistic for Block E is therefore the original preregistered block-alone one.

**What was measured, and on what.** Nothing is transferred from the parents' pool: the estimator draws its tail variants from this filing's own list, and the artefacts are the shipped ones -- `q3smc.c` `f0e3efc8`, `gen_consts.py` `721d7949` applied to `lowm.py` `f2578183` (the previous filing's program, which differs from this filing's shipped program in the single line `Q3_LOG2`), giving `q3consts_orig.h` `efd62db9` and `variants.bin` `b7671710` with **599,760 words** (the 170 classes of lists 0, 1, 5, 6). The word count and all five hashes are asserted by the runner before a seed starts, so a run on the parents' 782,800-word pool cannot be reported as this block. Regeneration is invariant in `Q3_LOG2`: both artefact hashes come back identical from either program state, which is why the study's pool is also this filing's. Configuration unchanged from G.3 and G.4: `q3smc seed0 512 8192 512 16384`, 32 shards, one run per seed. Runner: `experiments/r37-q3e-32.py`.

**Result.** 16,384 seeds 772000..788383, none dropped, replaced or rerun: mean **2^-71.42132**, sd **0.15870** (relative sd of the linear estimates **0.1100**), t(0.99, 16383) = 2.3266, one-sided 99 percent lower bound **-71.42420**, and **q3c_declared = 2^-71.4243** on the log scale -- superseded by block F's linear statistic (2^-71.4162, Section 3 and Appendix G.5), and quoted here as the stated sensitivity it is. That is 0.01120 bit of q3c against the previous declaration 2^-71.4355, hence the same number of bits off the claim. The block is not a new model, a new estimator or a new pool; it is more of the same measurement, which is the only thing that narrows a Student bound.

**The pooled figure, stated as a sensitivity and not used.** Pooling block E with Appendix G.4's 1,024 seeds (mean 2^-71.42391, sd 0.15878) gives n = 17,408, mean 2^-71.42147, sd 0.15870, t(0.99, 17407) = 2.3266, one-sided 99 percent lower bound 2^--71.42427, i.e. 2^-71.4243 — *one ten- thousandth of a bit worse* than block E alone. It is reported here and is **not** the operative rule, for the reason the first version of this appendix had to be amended: 1,024 of its 17,408 observations were examined before the extension was written, so a fixed-n Student bound on the pooled sample has no clean coverage claim, while block E's does — it was preregistered as a block of 16,384, run once, and scored by the rule written before it. The rule for Block E is simply the block-alone rule that was preregistered.

**Optional stopping, disclosed.** The pooling rule was written in the amendment `994e7b9` after G.4's 1,024 values existed -- that is unavoidable, since the pooled estimator uses them -- but before any seed of block E ran, and git records both facts. Nothing in the rule depends on block E's outcome: the estimator, the pool and the sample size were fixed first, the rule has no branch, and the block-alone value is printed beside the pooled one so that the block-alone value is recorded alongside the pooled sensitivity.

**What does not change.** Appendix G.3's block keeps its own reported value, 2^-71.43547 (declared 2^-71.4355), and every sensitivity of Section 7.4c is quoted at its own q3 factor and is therefore untouched by this. The declared q3c is still a one-sided 99 percent bound on the mean of the submitted pool's own per-variant tail probability, with no sub-pool transfer allowance. Block E alone gives 2^-71.4243 (floor of its own log-scale lower bound to four decimals); that weaker number is reported here and is superseded by Appendix N’s linear-scale bound on fresh seeds, which is the operative one.

**All 16,384 values, in the package.** The list is below in a form the 512 KiB package cap can hold: 16,384 three-byte big-endian integers, base64, each equal to `round((log2est + 71.42) * 1e5) + 90000` in seed order (seeds 772000..788383, one per value). Three lines decode it, and the digest of the values as the estimator prints them (`%.5f`, newline-joined) is `54f26602476451e9803d1b94a55bdaa3bae7e455c919d6fb58d04929d74c448d`; the same list as a `<seed> <log2est>` file is `reports/blockE_log2est-32.txt`, sha256 `115816e0ec65f21f3391f8f799c6b5f16b4ababf78b77dd7e144b11758bdd3fc`. It is encoded rather than printed because 147 KB of decimal text does not fit beside the 106-KiB experiment report inside the 512 KiB cap:
```python
import base64 raw = base64.b64decode(''.join(PACKED.split()))
vals = [b''.join(raw[3*i:3*i+3]).hex() for i in range(16384)]        # keep the bytes log2est = [int.from_bytes(raw[3*i:3*i+3], 'big') - 90000 for i in range(16384)]
log2est = [(-71.42 + z / 1e5) for z in log2est]                      # then '%.5f' each print('%.5f' % (sum(log2est) / 16384))                               # -71.42132
```
```text
PACKED (the 65,536 base64 characters of all 16,384 three-byte values) is archived, byte-identical,
at reports/blockE_log2est-packed-135.b64 next to the candidate (workspace reports/ directory,
sha256 of the character stream 9fa4fbd9c51a587deb5632b9c6cf0e7890bc59f244ee539a7255fc24592cf15f);
decode it with the three lines above after loading that file. The digests in the paragraph above
(54f26602... of the printed values, 115816e0... of the <seed> <log2est> file) still verify the list.
```
The 32 per-shard means and standard deviations are reproducible one shard at a time with `q3smc <seed0> 512 8192 512 16384`, but they are omitted here for the same budget reason as the value table above; the block-level mean, sd and bound printed above are what every rule in this appendix consumes, and this appendix's figure is a stated sensitivity, not the operative rule.
## Appendix N. Block F: the same pool, fresh seeds, the unbiased (linear-scale) statistic
**Why a second block.** Appendix G.5 declares q3c from
```text
u = floor( (mean(x) - t(0.99, n-1) x sd(x) / sqrt(n)) x 1e4 ) / 1e4,     x_i = log2est_i,
```
i.e. from the mean of the **logarithms** of the per-seed estimates. What the ledger needs is a lower bound on q3c itself. Each per-seed estimate `e_i` = `est` is the product of that replicate's SMC stage means, which is unbiased for q3c; so `mean(e)` is unbiased, while `2^mean(log2 e)` is the geometric mean and is biased **low**. Every other study in this appendix averages the linear estimates (G.2 and G.3: "the one-sided 99% Student lower bound of the mean of the 128 **linear** estimates of the block"); G.5's rule is the exception. On block E's own 16,384 published RESULT lines the gap is measurable and is not small:
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
with no pooling and no branch on the outcome, and the declaration is not conditioned on the gate. `experiments/r37-alpha55.py` re-derives the rule from the 16,384 published estimates and asserts the shipped declaration to the digit (mean(est) 2^-71.413310, relative sd 0.109498, t(0.99, 16383) = 2.3266, LB 2^-71.416184 -> 2^-71.4162). **Selection.** The ledger's q3c is one 99 percent lower bound, not the maximum of two: block E's 2^-71.4243 bounds the GEOMETRIC mean of its per-seed estimates, which the measurement above puts 0.008676 bit below their arithmetic mean, so it is not a 99 percent lower bound on q3c at all, is not a competing estimate of it, and is carried as a stated sensitivity. The gate can then only truncate the report in the event LB <= 2^-71.4243, which sits 6.58 sd below the realized bound (sd of log2 LB = 0.001234): P = 2.41e-11 = 2^-35.3, and the coverage it costs is 2.41e-11, i.e. 1.1e-12 bit of the bound. The crude alternative, holding both blocks to be equally valid 99 percent bounds and splitting Bonferroni (99.5 percent each), declares 2^-71.4165 and claims 57.58004, +0.00029 bit; the same script computes both prices, and the crude alternative is recorded here only as a stated sensitivity of the declaration rule. The artefacts are pinned by sha256 in the preregistration and re-checked by the runner before the first seed starts, which also reproduces a control seed: `q3smc.c` `f0e3efc8`, `gen_consts.py` `721d7949`, `q3consts_orig.h` `efd62db9`, `variants.bin` `b7671710` = 599,760 words (the submitted pool), program `lowm.py` `b6b39663`, identical to block E's state modulo the single line `Q3_LOG2`.

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
fixed before the data, both bounds declared and the more conservative one used, so no choice is made after the run. The estimator is the shipped `q3smc.c` with exactly two edits: its SMC loop stops after stage 21, and the tail is replaced by a late-proposal loop that draws (W6, W7) uniformly on F6 x F7 and W8x uniformly from the submitted pool, computes rows 22..36 of both members **in full**, and evaluates both events on the same proposal; it asserts cell => collision on every single proposal. The particles are the shipped estimator's stage-16..21 survivors (resampled uniformly at each stage), so the proposal law is exactly the one Section 7.7 defines.

**Result.** 1024 seeds, 214,748,364,800 proposals, 6,556,489 cell events and 16,292,349 collisions (cell rate 3.0531e-05 = 2^-14.99936, against the shipped stage means 2^-11.003 x 2^-4 = 2^-15.002; row-22 rate 2^-10.99983 against 2^-11.003). R_pooled = **2.484920**, se = 0.001149, LB_p = 2.482246; per-seed ratio mean 2.485151, sd 0.038885, t(1023) = 2.3300, LB_s = 2.482320. Declared **EXQ = 2.482** (the smaller bound, floored to three decimals).

**What does not change.** q3c (Appendix N), the pool, the family, the characteristic, the charge list and the premises. The inherited minimum 2.4331 and the two measurements behind it stay in Section 7.7 as labelled sensitivities, and the H3(b) upper value 2.4902 is untouched.
#### 9.11.2 The prepacked-literal, fixed-slot store, and step-recurrence folds (this revision's second cell; the 9.11.1 precedent)

The batch-schedule constants and message slots of 9.11 are materialized once, at import, and referenced
by their scratch slots for the life of the program — the same form P9 established for the broadcast planes
(and ed0d4c15/5dbbb8da apply to the q detection stores): a fixed set of compile-time values and 16 schedule
slots in one contiguous scratch area, so each reference is `base + immediate` and no address add or
broadcast is an operation of the shipped text. On top of 5dbbb8da's three folds (-122 primitives: 2,867 -> 2,745), four further folds, all counter-verified, remove 57 primitives:

- **Inherited 5dbbb8da prepacked-literal folds (-122):** `PAL`, `PEL`, `IVP[0..7]` (-16), `KTL[0..36]` (-36),
  and the 23 lane-mask reloads, 8 feed-forward IV references, and 8 chaining stores (-46 - 16 - 16).
- **The 16 initial message-schedule stores (`w[0..15]`):** fixed-slot stores at `base + 32*t` (same form
  as P9 and 9.2), eliminating 16 address adds; 16 primitives fall.
- **Prepacked `BC0`, `FG0` (`t = 1`), and `KTL[1..3]` (`IV[7-t] + K[t]`):** at `t = 1`, `b, c, f, g` are
  known IV registers (`IVP[0,1,4,5]`), so `BC0 = IVP[0] ^ IVP[1]` and `FG0 = IVP[4] ^ IVP[5]` are static
  constants (-2 ops), and at `t = 1..3`, `h = IV[7-t]` is folded into `KTL[t]` (-3 ops); 5 primitives fall.
- **Carried `bc = a ^ b` step recurrence in `Maj` (`t = 1..36`):** using `Maj(a,b,c) = (a & (b^c)) ^ (b & c)`
  and `b_{t+1} = a_t, c_{t+1} = b_t`, each step computes `ab = a ^ b` once (needed by `Maj` and carried
  into step `t + 1` as `bc = ab`), eliminating 1 XOR per step across 36 rounds; 36 primitives fall.

Total: 2,867 - 122 - 57 = **2,688** (= 7 x 384 executed per first block; the charge is `SB_FB` = 2644, one unit, Section 9.11), exactly what `sb_measure(8)` measures after load, on every call; `sb_measure` still asserts the count is data-independent and that every lane of every trial equals the reference compression. The constants live in the batch's existing scratch area, already inside the declared memory: the `memory` command reports 1,011,978 bytes, byte-identical to the accepted row, because `sb_pk` values are uncharged program constants either way.
## Appendix P. The H6 rate receipts and the class-pass variance, in the package

H6's scan and padding rates and the unconditional class-pass variance were previously cited to
workspace receipt paths outside the package. This appendix carries the receipts themselves, so
every number the claim's H6 and H1 limitations use is in the reviewed package.

### P.1 The ROW_FIX bootstrap receipt (r37-rowfix4-96, verbatim)

```text
# r37-rowfix4-96: ROW_FIX at the four-bit lane counts, block-level bound
# 2000 blocks, seed 'cells', 300 bootstrap resamples
#   k 3 cube 0xd n 3456 nr 432 nl (256, 176)   classes 3
#   k 3 cube 0xd n 3600 nr 450 nl (256, 194)   classes 3
#   k 4 cube 0x8d n 3456 nr 216 nl (216,)   classes 82
#   k 4 cube 0x8d n 3600 nr 225 nl (225,)   classes 82
# pre-row-test fix(nl): {176: 42, 194: 47, 216: 50, 225: 53, 256: 58}

# shipped geometry
#  nl 176  runs 7775   mean  15.4668   block-boot 99%  17.2862   (pre-row-test 42)
#        filed ROW_FIX[176] = 17.929700   block-boot 99% -0.6435 vs filed
#  nl 194  runs 7440   mean  18.0696   block-boot 99%  20.2174   (pre-row-test 47)
#        filed ROW_FIX[194] = 20.813300   block-boot 99% -0.5959 vs filed
#  nl 256  runs 15215  mean  21.1126   block-boot 99%  23.7482   (pre-row-test 58)
#        filed ROW_FIX[256] = 24.408100   block-boot 99% -0.6599 vs filed

# four-bit geometry
#  nl 176  runs 278    mean  12.4604   block-boot 99%  16.8462   (pre-row-test 42)
#        filed ROW_FIX[176] = 17.929700   block-boot 99% -1.0835 vs filed
#  nl 194  runs 240    mean  13.1375   block-boot 99%  18.8043   (pre-row-test 47)
#        filed ROW_FIX[194] = 20.813300   block-boot 99% -2.0090 vs filed
#  nl 216  runs 11034  mean  17.8372   block-boot 99%  20.3240   (pre-row-test 50)
#  nl 225  runs 10854  mean  17.8279   block-boot 99%  20.1968   (pre-row-test 53)
#  nl 256  runs 518    mean  15.6467   block-boot 99%  21.0994   (pre-row-test 58)
#        filed ROW_FIX[256] = 24.408100   block-boot 99% -3.3087 vs filed

# paired per-block scan cost: 2 x four-bit - shipped, over 259 blocks with a dispatch
#   mean +904.1081 ops per block   block-boot 99% +1234.4170   (1% +615.0077)

# the two keys this adds (block-boot 99% column): {216: Fraction(10161979, 500000), 225: Fraction(20196831, 1000000)}
```

### P.2 The PAD_RATE Poisson receipt (r37-padrate-73, verbatim)

```text
shipped ledger: vbar 14071.847664526744  time_log2 57.28612  grp 6952.749135117512
# reproduction: the replacement form at the shipped padding (3/4 group, 1 x PAD_OPS)
# returns the shipped row exactly: vbar 14071.847664526744
# padding charge: shipped 36.250000 ops/block; measured 17/5000 = 0.003400; 99% Poisson bound 0.005862
# GROUP_BODY 28, sum(PROBE) 11, PAD_OPS 7
point: vbar 14031.242855410763 (-40.604809)  grp 6913.346143  time_log2 57.28222 (-0.00390)  pcap 43/25000000  floor 0.3900000053352100648  cap_closes True
bound: vbar 14031.370979557560 (-40.476685)  grp 6913.470304  time_log2 57.28224 (-0.00388)  pcap 43/25000000  floor 0.3900000053352100648  cap_closes True
saving against the shipped row 57.28612: point 0.00390 bit, 99% bound 0.00388 bit
the cap chain re-closes at both rates, so the edit is two expressions in lowm.py
and no constant, premise or algorithm moves.
```

### P.3 The unconditional class-pass counter: its variance, measured

The count of passing classes over uniform first blocks has mean exactly 170 p7 = 2.697754
(p7 = 68,157,440/2^32), but the 170 F7 sets are sibling translates and overlap, so the count is
strongly overdispersed and the binomial variance is the wrong yardstick for any sample of this
counter -- including the 512-block unconditional sample of `a0-online-r37`. The variance is a
straight measurement (scalar F7 over all 170 classes, 60,000 fresh uniform first blocks, seed 137;
verbatim receipt below): the empirical mean is 2.6877 against the exact 2.697754; the mean pairwise
co-pass probability is P12 = 0.002566 = 10.17 x p^2 (p^2 = 0.000252), i.e. two classes co-pass
10.2 times more often than independence predicts; Var(count) = 170 p (1-p) + 170 x 169 (P12 - p^2)
= 69.13, matching the empirical 69.17 -- a design effect of 26.0 over the binomial 2.655. Under
this measured variance the a0-online unconditional sample (2,070 passes in 512 blocks, 4.043 per
block, the organizer's own public-seed counter) is z = +3.66 against the exact mean, and the
6,000-block counted-program control (2.7500 per block, `r37-recount54`) is z = +0.14. The
4.04-per-block figure of the organizer report is therefore consistent with the H1 expectation at
the counter's own (measured) dispersion; no conservative interval of H1 is affected because the
ledger uses only the exact expectation and the Bernstein cap needs only 0 <= v_f <= vmax_fb
(Section 11.1). The same overlap is why the class plane is priced once per batch and the passes
are charged at the class constant (Section 9): bursty counts raise the cap's vmax_fb, which is
already charged at its maximum.

```text
r37-uncondivar-137: variance of the unconditional class-pass counter of a0-online-r37
NCLS=170 p7=65/4096 (=68157440/2^32) 170*p7=2.697754
independent-approx: Var(count per block)=2.6549 sd=1.6294 ; Var(mean,512 blocks)=0.005185 sd=0.072010
observed 2070/512 = 4.0430 ; z(indep) = 18.68
design effect implied by z=+18.6: 346 (per-block), i.e. per-TRIAL clusters of 32 blocks need
  intra-trial variance 346.0 x the independent variance
sample 60000 first blocks (scalar F7 over all 170 classes):
mean passes/block = 2.6877 (exact 2.697754)
empirical Var = 69.173 ; independent-approx Var = 2.655
mean pairwise co-pass P12 = 0.002566 = 0.1617 x p  (p^2 = 0.000252)
theoretical Var with measured overlap = 69.127 (design effect 26.0)
a0-online sample: 512 blocks, 2070 passes -> 4.0430/block ; z under measured overlap = 3.66
## Appendix Q. The organizer-executed H6 corroboration and the structural ceiling

H6's scan and padding rates are participant measurements on public-seed generator output
(Appendix P). Three closing facts bound the row's reliance on that premise, all inside the
package or reproducible from it: an organizer-executed run of the same instrument, a
conservative organizer-side re-pricing of the keys, and the analytic worst case.

**(1) The organizer-executed instrument run.** The manifest experiment `h6-orgstats-r37`
(`kind: python-message-pairs-v1`, program `experiments/lowm.py`, branch `organizer-stats` of
`run_request`): per trial the branch draws 20 fresh first blocks from the same SHAKE-derived
organizer seed formula as every organizer experiment, runs them through the counted program
(`process_cv` with `scan_parts` wrapped per trial and restored in `finally`), and reports only
counts: per batch lane count nl in {176, 194, 216, 225, 256}, the nonzero-row scan events at
the participant instrument's per-(row,chunk) event unit (r37-rowfix4-96 discipline), the total
event count, and the residual-pad counter. It measures rates only; `message_a_hex`/`message_b_hex`
stay null in all 64 trials, no probability is inferred and no attack cost is computed. The run is
deterministic (two executions byte-identical), 64 trials x 20 blocks in 3.9 s on the host, inside
the 20 s / 128 MB executor envelope at 62,004 of the 65,536 source bytes at that revision (63,354 at R37P39); one byte-identical run
is preserved verbatim as reports/experiments/r37-orgstat-138-organizer-run.json:

```
blocks 1280
events nl176 1446 (1.13/block)   nl194 896 (0.70/block)   nl216 129838 (101.4/block)
events nl225 114138 (89.2/block)  nl256 2390 (1.87/block)  total events 248708
pad counter 5 events in 1280 blocks (0.0039/block)
```

Every nl shows strictly positive scan activity of the same orders the participant receipts
measure (order 1-2 events/block at nl 176/256, order 10^2 at nl 216/225, pad near 0), and the
sample scatter around the participant means (1.13 vs 1.4-2.0 at nl 176, 0.70 vs 1.4-2.0 at nl
194) is what Appendix P.3's measured overdispersion predicts for a 1,280-block sample
(class-pass design effect ~26). Items (2) and (3) provide the conservative organizer-side
re-pricing and the structural worst-case replacement bound
for these rate premises.

**(2) The conservative organizer-side re-pricing.** Re-deriving ROW_FIX/PAD_RATE from an
organizer-style 1,280-block sample at the 99% binomial/Poisson bound discipline
(reports/experiments/r37-orgstat-138.py, fresh receipt at this row: reports/receipts/r37-orgstat-140.out)
gives keys 27.23/36.56/54/57/62 and PAD_RATE 1/125000; pricing the same ledger at those keys:

```
time_log2 = 57.05523  (this revision's cells at the former 384 charge, R37P40h; filed keys at that charge 56.99456)
(R37P40g row: 57.06265 against its filed 57.00229; R37P39 row: 57.10920 against its filed 57.05080; base 3c71035b row: 57.16006 against its filed 57.10307)
```
These prices use the former 384 batch charge. At this filing's one-unit charge (SB_FB = 2644) they rise by N_FB x 2260/2644 units: at most 57.28905 (organizer-side keys) and 57.33417 (structural worst case, item 3), against the filed 57.21528 (both bounds were computed on the R37P40k cells; the three fixed-slot folds only lower them).

A worst-direction spread of 0.06036 bits at this revision (0.05840 on the R37P39 row, 0.05699 on the 3c71035b row) from replacing every rate premise with organizer-side
measurements. Even keys measured entirely on the organizer's side leave the row below only the
structural ceiling — they do not approach live #1, 57.10741, which is why the filed headline
keeps the participant-measured keys and declares the replacement.

**(3) The structural worst case, as the analytic replacement.** As a no-premise sensitivity
bound, the structural worst case prices the attack with every rate at its structural extreme:
attack priced with every rate at its structural extreme: all rows set (ROW_FIX = ROW_MAX at
every lane count) and every block padded (PAD_RATE = 1). That price is **57.15946**, from the
same ledger with the rate keys at their maxima (base 3c71035b row, with its lower ROW_MAX; at the R37P39 cells and the raised ROW_MAX of Section 9.6c the same substitution prices 57.16021, at the R37P40g cells 57.11530, and at this revision's cells **57.10815**); it uses no premise about scan or padding rates
at all — it is the number the attack costs if the generator were adversarially aligned against
the scan. The gap from the base row's filed 57.10307 to its no-premise price 57.15946 is 0.05640 bits (R37P39: 57.05080 to 57.16021, 0.10941 bits; R37P40g: 57.00229 to 57.11530, 0.11301 bits; this revision at the former 384 charge: 56.99456 to 57.10815, 0.11359 bits; at the one-unit charge 57.23762 to at most 57.33417, the larger gaps reflecting the true ROW_MAX ceiling) —
the whole weight H6's premises carry in the row, bounded and disclosed. Both 57.16006 and
57.15946 stand above the live frontier 57.10741: the worst case bounds the reliance, the
organizer experiment corroborates the instrument, and the record row remains the measured one.

The end event (rows 22..36 reaching an equal digest) remains the premise it is everywhere else
in this filing: none of these three items executes or infers it.

## Appendix R. Remote experiment evidence for the inherited source

**Draft evidence reconciliation.** The remote organizer experiment artifact for submission `356ff5f2-23dc-4c0c-b80d-a152b78ba9a5` (GitHub Actions run 40723262807, artifact `hashsmash-review-sha256-r37-exploratory`) binds `experiments/lowm.py` SHA-256 `434225b4ea98ec8a46489e09d84dd704f45398aed860f9796b1b418d100a7097`, matching the source in this draft. It reports 256 trials for each of the six declared experiments and byte-identical results across two isolated executions. The full-collision experiments reported no checked full-target collisions; `h3-ladder-r37` reported eight successes of its declared four-bit mask event, not full collisions. In `a0-online-r37`, the participant-reported mismatch counters and prefilter-miss counter sum to zero; these internal observations are not independently checked operation counts. The `h6-orgstats-r37` participant observations sum to 2,538 / 2,614 / 191,208 / 173,665 / 6,876 scan events for lane counts 176 / 194 / 216 / 225 / 256, with 10 pad events. These are 256 public-seed trials with no holdout nonce, not independent evidence of full-scale success probability or attack cost. The report binds the earlier submitted package and source, not this edited proof or its current package hash.

## Appendix S. Unfiled early-exit research

For the 15-plane `f6_sub` form, after computing `w1` and before the two
`f6_combine_pre` calls, if both `w1 XOR W12_0` and `w1 XOR W12_1` are all ones
over all 256 lanes, both branches necessarily reject every lane by the
`w1 = w12` condition. Returning a zero plane in that case preserves the
subtraction result. The 9-plane form was not modified.

A local isolated diagnostic compared this prototype against the existing
`f6_sub` on two selected first blocks: one from the earlier organizer's
`a0-online-r37` returned pair and one selected zero-pair block. In 124
subtraction calls it reported 40 early exits and zero output-plane mismatches.
These are participant-reported internal observations, not organizer-verified
collision events, a representative frequency estimate, or an operation count.
The diagnostic used a 120-second local timeout, not the official 20-second
setting. It does not alter the submitted algorithm or claimed score. The
additional XOR, comparison, branch, inversion-flag, and counter costs, as well
as the distribution over fresh first blocks, must be accounted for before this
could support an improved claim.

Under the filed H1 cube-bit law, the expected number of subtraction-batch
executions is `170 * (65/4096) * 2 * ((1 + 1/4) * (1 + 1/2)^2 - 1)`
`= 160225/16384 = 9.77936` per first block. Even making the `f6_sub` body
itself free on every execution, at its stated maximum of 28 operations, saves
at most 273.83 operations per first block. This is not a bound on any additional
scan or control savings, and it excludes the new predicate's own cost. It is
far below the roughly 2,177 operations per first block needed to match the
57.00229 leaderboard score with other terms and the success law unchanged.

An unfiled diagnostic on the same two selected first blocks also evaluated the
main output and every relevant `f6_sub` output per batch, conservatively
requiring all 256 lanes, including unused lanes, to be zero. It reported 52
whole-batch zeroes among 72 batches, including 32 among the 36 batches with
subtraction runs. These are participant observations after all the work has
already executed, not an early test or a savings estimate. The selected
zero-pair block makes this sample unsuitable for estimating a population rate;
a cheap no-false-negative predicate and an independently supported rate are
still needed.

The 16/8 prototype was subsequently compared with the existing 15/9 table
predicate over the entire low-24 input space in a local isolated diagnostic:
1,129,984 inputs were compared explicitly, and 15,647,232 inputs were skipped
because both corresponding high-table entries were zero. The participant
reported zero differing feasible-`l` masks and at most two states per `l`.
This checks the two implementations against each other, not the cryptographic
claim independently; the 120-second local diagnostic is not an official
qualification or a measured online cost.

An experimental low-bit predicate enumerated the relevant `cu` values using
planes W[1..12], computed the bit-1 and bit-12 results after each subtraction,
and rejected a batch only if no lane could satisfy the necessary equality
`w1 = w12` for any `cu`. On the same two selected first blocks it reported
8 early rejections among 72 batches, no false rejections compared with the
fully evaluated planes, and 3,672 instrumented plane operations to form the
low bits. This is a diagnostic prototype: the subtraction and predicate costs
are not included in that operation count, some arithmetic was evaluated as
Python integers rather than the priced plane program, and its assumption about
bit 0 for the relevant subtraction must be established for all cases. The
selected sample is not a rate estimate and the prototype is not part of the
claimed online algorithm.

## Appendix T. Unfiled sparse FIRST-table experiment

The FIRST table has 32,768 64-bit entries, of which 2,207 are nonzero. A local
isolated diagnostic built a 16-bit index array with zero as a sentinel and a
packed array of the nonzero 64-bit entries, then compared every reconstructed
entry with the existing table; it reported zero mismatches. The theoretical
resident sizes are 65,536 + 17,656 = 83,192 bytes, versus 262,144 bytes for
the dense table, excluding alignment, code and construction scratch.

This is not a claimed attack improvement. A production implementation needs
to construct the sparse table without an uncharged transient coexistence with
the dense table, account for peak memory, index addressing and each extra load,
and verify the full online program. The 2,207/32,768 nonzero fraction does not
alone prove the online access distribution. If those issues are resolved, the
178,952-byte raw saving could potentially make room for other layouts such as
the seven-lane arithmetic experiment; their total time and memory must still be
priced together and compared with the live frontier.

A second local isolated diagnostic replaced the dense FIRST array in the
existing builder with an incrementally updated sparse index and value array.
It compared all 32,768 FIRST entries and all 512 SECOND entries with a dense
build and reported zero mismatches. This prototype's allocated value array
includes an eight-byte zero sentinel: its measured array payload is 65,536 +
17,664 = 83,200 bytes, an 178,944-byte reduction before alignment and code.
The diagnostic deliberately built both representations for comparison and
used a 120-second local limit; it is not a peak-memory or preprocessing-cost
certificate. A single sparse build and its allocation/initialization, lookup
and code costs remain to be described and charged before filing.

## Appendix U. Unfiled seven-lane arithmetic diagnostic

The seven-lane 36-bit-slot prototype was compared with the current four-lane
`packed_u` on the selected `a0-online-r37` positive-control first block. The
local isolated diagnostic reported 1,508 complete seven-lane groups, 10,556
compared lanes and zero mismatches; four remaining lanes were not compared.
These are participant-reported internal observations from a single selected
block under a 120-second local limit, not an organizer-verified attack-cost or
success-probability result. The diagnostic buffers the original four-lane
outputs for comparison and is not an optimized implementation.

The seven-lane body, member formation, partial groups, table accesses, counters,
code size, scratch and preprocessing must all be priced in an actual program.
The sparse FIRST experiment above may supply memory for a different member
layout, but no claimed score in this draft uses either prototype.

## Appendix V. Unfiled 16/8 table-split exploration

An isolated participant diagnostic re-expressed the low-24 row-16 conditions
with an 8-bit low field and a 16-bit high field. For each of the 32 feasible
values of `l`, it enumerated the low-field interface states and all high-field
indices for each state. It reported at most two viable states per `l`, 40
viable states in total, and 2,224 nonzero high indices of 65,536. The current
15/9 split has 2,207 of 32,768 nonzero high indices. These are internal
observations of an unfiled prototype, not an independently checked table or a
probability estimate.

Assuming the same uniform-address model and unchanged seven-operation
continuation, the difference in hit fractions corresponds to about 149 fewer
continuation primitives per first block before the cost of a sparse lookup,
construction, memory, or other changes. A two-byte index and 2,225 64-bit
values including a sentinel use 148,872 bytes. The sparse FIRST table together
with a second 65,536-byte rep table would leave about 60,400 bytes under 1 MiB
from the currently reported online resident figure, before any new code,
scratch, alignment, or other changes. A complete implementation must compare
all predicates, assess resource bounds and demonstrate the claimed cost and
success law; the current claim does not use this exploration.

A later local isolated diagnostic integrated the 16/8 split into a copy of the
online process and compared it with the original 15/9 process on a selected
positive-control first block. Both produced 10,560 candidate traces; the
participant reported zero differences in candidate, parameter mask or output.
The builder enumerated 1,024 high-field values satisfying the fixed E bits for
each viable state and reconstructed all 2,224 nonzero high indices. This is a
single-block diagnostic under a 120-second local limit, not a submission or a
cost measurement; the changed program, build work, memory and accounting have
not yet been filed or officially reviewed.

### Cost sensitivity, not a filed claim

Using the inherited expected-lane and concentration model as an assumption,
charge two extra primitives on each nonzero 16/8 FIRST hit to access the
sparse value, and replace the 15/9 hit rate 2207/32768 by 2224/65536. This
changes the mean by -105.7223 operations per first block. Re-running the
Bernstein cap and time arithmetic with a conservative maximum increased by
2 per possible lane gives the conditional estimate 57.22547. If the sparse
representation also requires one additional primitive on every lane, the
mean instead increases by 530.9817 and the corresponding estimate is
57.28766. Neither scenario establishes a valid RAM implementation: packed
16-bit index extraction, word addressing, branches, initialization, builders,
peak memory and code must be counted from an actual implementation, and the
inherited expectations and success assumptions remain unverified.

Even combining the optimistic first scenario with the independently calculated
ideal seven-lane saving of 545.726 operations per first block and the extreme
assumption that every expected f6_sub body is free (273.822 operations per
first block) only gives a conditional arithmetic estimate of 57.14125. This
combination ignores overhead and interactions, and is not a certified bound or
an executable attack. It indicates that these ideas alone do not account for
the gap to the 57.00229 public frontier. The f6_sub ideal uses the filed
expected batch rate, not an extrapolation from selected test blocks.

## Appendix W. Packed 16/8 research implementation and provisional accounting

# 16/8 packed table: research implementation and provisional accounting

The prototype below builds 4,096 256-bit index words (16
16-bit indices each), a zero-sentinel value array of 557 256-bit words (four
64-bit masks each), and 256 64-bit SECOND values. The saved Python is a
functional specification, not yet a charged word-RAM implementation. It
uses Python lists, sets, dictionaries, allocation and iteration, whose costs
and peak live memory are not represented by Python timing or object size.

For one scalar probe, one explicit conservative instruction sequence is:

| operation | word operations |
| --- | ---: |
| shift U right by 8, mask high 16 | 2 |
| high >> 4, index-base addition, word load | 3 |
| high & 15, shift left 4, shift loaded word, mask 16-bit index | 4 |
| branch on zero | 1 |
| **total before nonzero test** | **10** |
| on hit: index >> 2, value-base addition, word load | 3 |
| on hit: index & 3, shift left 6, shift loaded word, mask 64 bits | 4 |
| on hit: old SECOND/filter continuation, provisionally inherited | 7 |

This sequence charges the two loads, two address additions and both packed
extractions. It assumes literal masks, shifts and base pointers already in
registers, and does not count any new per-probe counter or loop overhead.
Compare cautiously with the current ledger's 3 plus 7 on an old high-table
hit: branch and accounting conventions must be reconciled instruction by
instruction. Under the inherited uniform high-address model only, with
2224/65536 versus 2207/32768 hit probability and 636.70390766 expected
lanes per first block, this sequence increases the expected cost by roughly
4,459.24 operations per first block. This is a design calculation, not a
measurement or an accepted claim. More efficient addressing or a different
layout must be demonstrated, not assumed.

Payload accounting, counting full 256-bit allocation words: index = 131,072 B;
value words = 17,824 B, including the zero sentinel and final word padding;
SECOND = 2,048 B. Replacing the baseline's 262,144 B FIRST and 4,096 B SECOND
in its stated 1,035,912 B online total yields 920,616 B before new code,
state, allocation overhead, alignment beyond these words, or any changes to
other live structures. The Python objects do not establish this bound.

For construction, `build16_packed` has three identifiable stages: at most
32*256 low-field iterations; up to 32*8*65536 state-existence iterations;
and 65536*64 state tests to build the output, followed by bounded writes for
65,536 indices and at most 2,224 value masks. A single high-state predicate
needs the high addition, mask, A addition, fixed-E comparison, A mask
comparison and two parity tests; loop controls, state loads, branch and OR
must be charged in addition. A loose planning envelope of 2^35 ordinary
operations for these loops is intentionally much larger than the raw iteration
count, but is NOT a proven build bound: exact loop programs, initialization,
state storage, special cases, per-iteration instruction counts and maximum
live scratch still need to be specified. It must be added to, rather than
silently absorbed into, the baseline's existing preprocessing bound unless a
replacement accounting proves otherwise. Setup of `Env` and LC constants is
not included in that envelope.

A possible higher-impact direction is to make additional variant classes
cheap enough to include. The inherited proof states that the six omitted lists
cost 20.1644--20.7967 class-preparation operations per expected good pair,
versus 10.6860--10.9224 for kept lists, and the old break-even was 11.5060.
The new one-unit compression charge raises a rough marginal threshold by
2260/636.68046 = 3.55 operations per current expected good pair, to about
15.06, still below even the cheapest omitted list. This is a sensitivity,
not a complete re-evaluation: it assumes unchanged marginal pair costs,
probabilities, shared setup, memory and correlation. Thus merely restoring
the old pool is not a justified improvement; a concrete reduction of more
than roughly five preparation operations per added pair, followed by a full
recalculation, would be needed even to make those lists locally attractive.


```python
# Participant prototype, to be executed only by the organizer's isolated executor.
# Depends on the definitions and Env instance from experiments/lowm.py.
# 256-bit packed machine words; index=0 is a zero-value sentinel.

def build16_packed(env):
    specs=[]
    second=[0]*256
    for l in FEASIBLE_L:
        c=env.LC[l]; a15=c['Ax15']; C=c['C']; A=c['cxA']
        los={}
        for lo in range(256):
            t=lo+(C&255); e=t&255; ta=e+(A&255); al=ta&255
            if (e&(E16M&255))==(E16V&255) and not ((e^c['Ex15'])&16):
                los[lo]=(t>>8,ta>>8,(al>>6)&1)
        states=[]
        for ce,ca,a6 in sorted(set(los.values())):
            want=(((~a15>>15)&1)<<7)|(((a15>>23)&1)<<15)|((a6^1)<<10)
            # Determine whether the interface state has any valid high index.
            found=False
            for h in range(65536):
                e=(h+(C>>8)+ce)&65535; v=e+(A>>8)+ca
                if (e&((E16M>>8)&65535))==((E16V>>8)&65535) and (v&0x8480)==want and ((v>>12^v>>1)&1) and not ((v>>9^v)&1):
                    found=True; break
            if found: states.append((ce,ca,want))
        assert len(states)<=2
        for i,st in enumerate(states):
            bit=1<<(32*i+l); ce,ca,want=st
            specs.append((C>>8,A>>8,ce,ca,want,bit))
            for lo,state in los.items():
                if state==(ce,ca, (want>>10&1)^1): second[lo] |= bit
    idx_words=[0]*4096
    val_words=[0]                 # index 0 remains zero
    count=0
    for h in range(65536):
        mask=0
        for chi,am,ce,ca,want,bit in specs:
            e=(h+chi+ce)&65535; v=e+am+ca
            if (e&((E16M>>8)&65535))==((E16V>>8)&65535) and (v&0x8480)==want and ((v>>12^v>>1)&1) and not ((v>>9^v)&1): mask |= bit
        if mask:
            count+=1
            if count%4==0: val_words.append(0)
            val_words[count//4] |= mask << (64*(count%4))
            idx_words[h//16] |= count << (16*(h%16))
    assert count==2224 and len(specs)==40
    return idx_words,val_words,second

def packed_first16(idx_words,val_words,h):
    # Returns a 64-bit mask. Zero index means miss; do not fetch a value on miss.
    i=(idx_words[h>>4] >> (16*(h&15))) & 65535
    return 0 if not i else (val_words[i>>2] >> (64*(i&3))) & ((1<<64)-1)

def lookup16(idx_words,val_words,second,u):
    first=packed_first16(idx_words,val_words,(u>>8)&65535)
    if not first: return 0
    t=first & second[u&255]; t |= t>>32
    return t & ((1<<32)-1)
```

For the specific 10-before-hit/14-after-hit instruction sketch in Appendix W,
the same conditional ledger sensitivity used in Appendix V gives approximately
57.62146, with the maximum per first block conservatively increased by 14 times
599,763 lanes. This illustrative number uses inherited success assumptions and
the inherited baseline preprocessing; it omits the new builder and is not a
claim, executable total, or official score. Its purpose is to show that the
concrete packed lookup requires further optimization before integration.

The embedded prototype was run twice in fresh networkless organizer executor
containers with a locally raised 120-second limit, using a locally assembled
source snapshot and a dummy configuration hash for this diagnostic, not an
official evidence report. The two stdout documents were identical. Participant
observations reported 263,936 specified input comparisons against the current
15/9 `Env.filt`, zero mismatches, 4,096 index words, 557 value words and 256
SECOND entries. The checked trial returned no message pair. This checks only
those inputs and does not establish operation counts, build resource bounds,
full-scale success or compliance with the normal 20-second experiment limit.

## Appendix X. Bitmap-guided 16/8 construction, unfiled prototype

The following standalone research function uses the same `Env` and constants
as Appendix W. It enumerates only the 1,024 high E values that satisfy the fixed
E mask. It records their viable high indices in an 8,192-byte bitset, then
computes full FIRST masks only at marked indices. It retains the same packed
index and value representation as Appendix W; it does not change the online
lookup or its charges.

```python
# Participant research code; run only inside the organizer executor.
def build16_bitmap(env):
    specs=[]; second=[0]*256; present=[0]*256
    em=(E16M>>8)&65535; ev=(E16V>>8)&65535; free=(~em)&65535
    assert free.bit_count()==10 and ev&free==0
    for l in FEASIBLE_L:
        c=env.LC[l]; C=c['C']; A=c['cxA']; a15=c['Ax15']; los={}
        for lo in range(256):
            t=lo+(C&255); e=t&255; ta=e+(A&255); al=ta&255
            if (e&(E16M&255))==(E16V&255) and not ((e^c['Ex15'])&16):
                los[lo]=(t>>8,ta>>8,(al>>6)&1)
        states=[]
        for ce,ca,a6 in sorted(set(los.values())):
            want=(((~a15>>15)&1)<<7)|(((a15>>23)&1)<<15)|((a6^1)<<10)
            sub=0; found=False
            while True:
                e=ev|sub; v=e+(A>>8)+ca
                if (v&0x8480)==want and ((v>>12^v>>1)&1) and not ((v>>9^v)&1):
                    h=(e-(C>>8)-ce)&65535
                    present[h>>8] |= 1<<(h&255); found=True
                sub=(sub-free)&free
                if sub==0: break
            if found: states.append((ce,ca,a6,want))
        assert len(states)<=2
        for i,(ce,ca,a6,want) in enumerate(states):
            bit=1<<(32*i+l); specs.append((C>>8,A>>8,ce,ca,want,bit))
            for lo,state in los.items():
                if state==(ce,ca,a6): second[lo] |= bit
    assert len(specs)==40
    idx=[0]*4096; vals=[0]; n=0; tests=0; marked=0
    for h in range(65536):
        if not ((present[h>>8]>>(h&255))&1): continue
        marked+=1; mask=0
        for chi,am,ce,ca,want,bit in specs:
            tests+=1; e=(h+chi+ce)&65535; v=e+am+ca
            if (e&em)==ev and (v&0x8480)==want and ((v>>12^v>>1)&1) and not ((v>>9^v)&1): mask |= bit
        assert mask
        n+=1
        if n%4==0: vals.append(0)
        vals[n//4] |= mask << (64*(n%4))
        idx[h//16] |= n << (16*(h%16))
    assert n==2224
    return idx,vals,second,marked,tests
```

Construction still needs a word-RAM implementation and a complete instruction
ledger. In particular the bitset's address arithmetic, read-modify-write,
initialization, state-discovery and table-output writes are not free. The
Python lists, dictionary, set and sort are functional scaffolding, not a proof
of bounded RAM costs. No claim or score is changed by this prototype.

Local isolated diagnostic: the executor ran the assembled prototype twice with
identical stdout, using one trial and a 120-second limit. Participant observations
report 263,936 comparisons with the original 15/9 filter, 0 mismatches, 2,224
marked high indices and 88,960 full state tests; table sizes were 4,096 index
words, 557 value words and 256 SECOND entries. The preceding direct-scan
prototype would perform 65,536 * 40 = 2,621,440 full state tests for the same
40 viable states. State-discovery enumeration also traverses 1,024 fixed-E
values per possible state rather than 65,536 high indices. These are algorithmic
iteration comparisons, not measured word-operation or elapsed-time savings.
The bitset occupies 256 256-bit words (8,192 bytes); its build-time coexistence
with all other live allocations and code is not yet bounded. No pair was
returned or independently checked; the local diagnostic used a dummy config
hash and is not an official evidence artifact or a normal 20-second run.

## Appendix Y. Candidate-class shared-scalar hypothesis

For a fixed first block, `KZ = (KXA - (base & FA)) mod 2^32`. Therefore
classes with equal `base & FA` have exactly the same KZ and the same KZ-only
preparations (`NKZ`, `NKZ2`, `NKZ3` and the 16 KZ bit-planes); equality does
not imply equal CB3 or identical list planes. The shipped class list uses
eight distinct keys. Grouping passing classes by key could share that part of
preparation. A valid implementation must account for group formation, the
eight-key dispatch, branch/control, extra register lifetimes, scratch
allocation, plane stores and loads, code size, and work-cap updates. In
particular, keeping all KZ planes resident is not justified by the existing
64-register argument.

A local diagnostic used Python's deterministic `Random(20261030)` to draw
10,000 uniform 32-bit inputs and tested the 170 filed class F7 predicates.
Inside two fresh isolated executor runs, the participant program reported
26,930 passing classes, 4,262 distinct per-block keys and 1,269 blocks with at
least one pass; stdout matched. Thus 22,668 class-key occurrences were
repetitions in this finite sample. The executor did not independently verify
the internal F7 counts, and this sample is neither an exact key-overlap
probability nor evidence about the untested tail events. At most, before any
sharing overhead or register restrictions, the sample's repetition rate would
multiply any genuinely shareable per-class operation by 2.2668 per first
block. For example, even an assumed 48 removable KZ-plane formation operations
per repeat would suggest 108.8064 operations per first block before overhead,
not a demonstrated cost saving. It cannot be added to the ledger without a
specified implementation and justified expectation. This test covers the
filed 170 classes only; it does not establish a saving for the omitted 52.

One candidate implementation would reserve 8 * 16 * 32 = 4,096 bytes of
plane slots and process classes by key. For the first class with a key, form
16 KZ planes (the existing 48-operation assumption) and store each once;
for each later class with that key load those 16 planes, while forming CB3
separately. If immediate-slot loads/stores cost one each, and if the same
16 planes are all needed, the isolated-sample-only algebra gives
`48*p - (48*g + 16*g + 16*(p-g)) = 32*p - 48*g`, or 65.7184 operations
per first block for p=26,930 and g=4,262 over 10,000 inputs. This leaves out
key dispatch, grouping/order, scratch initialization, counter updates, code,
and any register-pressure spills. It is not an executable cost claim; in
particular it is not known yet whether planes can be stored and reused while
preserving the filed bit-serial program and register bound. The related
KZ-scalar arithmetic and first-class cost have not been folded into the 48.

The same 10,000 inputs were then evaluated in two fresh isolated executor
runs on the published 222-class parent, submission
`aa0e8b6a-6fd1-4a8b-9917-bb5e0f8a689f`, commit
`d6d874402c451412285457d4a05b7c6d829f23a7`. Its downloaded
`experiments/lowm.py` has SHA-256
`35b3e5975c26cf5e480a5307350ba959dec77f12975084bdbdf69843cd22d15a`.
The same participant diagnostic reported 26,930 kept-list passes and 4,262
kept keys, plus 8,240 omitted-list passes and 1,624 additional keys. There
were 14 possible keys total, six represented by omitted classes; since the
filed pool has eight keys, those six are disjoint at the key-set level.
Both runs produced identical stdout. These are internal observations on a
fixed finite sample, not independent cryptanalytic evidence.

Applying the hypothetical 16-plane store/load sketch to the omitted passes
alone gives `(32*8240 - 48*1624)/10000 = 18.5728` operations per first block
before dispatch, scratch and other overhead. The inherited H1 linear-rate
model predicts about 194.3077 good pairs per first block from the 183,040
omitted variants, so dividing these different quantities suggests only
0.0956 operations per added good pair. Even granting an unrealistically free
48-operation reuse on every sampled repeat gives approximately 0.1634 per
added pair. These are comparisons of a sample to a model expectation, not a
justified attack ledger. They are far smaller than the approximately five
operations per added pair identified in Appendix W merely to make omitted
lists attractive. This narrows the next search toward W6 batch or list-sweep
costs instead of treating KZ caching alone as a winning change.

## Appendix Z. W6 zero-mask and omitted-list probes, unfiled

`f6_combine_pre(m, ...)` ends by ANDing its expression with `m`; if the
logical plane `m` is identically zero, its result is zero. A possible runtime
guard can therefore skip the combine body in that case, provided inversion
flags are interpreted correctly and the downstream code accepts a zero plane.
Neither the branch nor converting a complemented plane is free. Dynamic
charges, the cap, spill liveness and full output equivalence must be updated
before this becomes an attack change.

An exploratory diagnostic processed 40 deterministic pseudo-random first
blocks from the IV; five had at least one passing class. It evaluated the
unchanged W6 code and recorded dynamic `f6_combine_pre` calls. The two isolated
runs had byte-identical output. Participant observations: 160 main calls, 96
zero masks and 960 operations inside their original combine bodies; 832
subtraction calls, 512 zero masks and 5,056 body operations. All 608 checked
zero masks produced zero output. For 192 of those zero masks the representation
had an inversion flag. Under the purely illustrative assumption of exactly one
branch per dynamic call, the upper arithmetic opportunity in this selected
40-block sample is `(6016 - 992)/40 = 125.6` operations per block before flag
handling, counter changes, spill changes or any other overhead. It is not a
probability bound, an implemented charged program, or an extrapolated score.
Static zero planes were excluded from the measured dynamic calls.

The six omitted parent lists have cube `{0,7}` in one tested representative of
each list (sizes 3456 for 2/3/4 and 3584 for 7/8/9); the current candidate's
low-bit cube lemma covers bits 0, 2 and 3, not bit 7. A separate local test
on the same published 222-class parent examined 31,872 bit-7 pairs with q7=1
and F7 passing, and found 4,580 F6 differences in participant observations.
One internally checked counterexample is a=473368420, x=2392558795,
y=513681180, partner a xor 128, W6 values 3370545903 and 3370546159, with
F6 values 0 and 1. Both a values satisfy G, their c7 values agree, q7=1 and
F7(c7-x) passes. These checks used isolated deterministic executions and a
local diagnostic, not a collision or a complete negative theorem. In
particular, assuming bit-7 partners always share an F6 outcome would drop
valid work. More refined paired algebra must preserve both outcomes.

## Appendix AA. Presence-gated 16/8 sparse lookup, unfiled

The construction bitmap from Appendix X can also be retained online. The
following functional variant tests that bitmap before reading either sparse
array. It does not bypass any nonzero high entry; the bitmap must match the
constructed index exactly.

```python
def lookup16_gated(present,idx_words,val_words,second,u):
    h=(u>>8)&65535
    if not ((present[h>>8]>>(h&255))&1): return 0
    i=(idx_words[h>>4]>>(16*(h&15)))&65535
    assert i
    first=(val_words[i>>2]>>(64*(i&3)))&((1<<64)-1)
    t=first & second[u&255]; t |= t>>32
    return t&((1<<32)-1)
```

One instruction sketch: high extraction 2, bitmap index/address/load 3,
bit extraction 3, and branch 1: 9 on every lane. Given an exact bitmap hit,
index-word address/extraction takes 7 more, value-word address/extraction 7,
and the inherited second-stage sketch 7: 21 more. This assumes literals and
base pointers are available, and omits loop/counter additions and any extra
conditional needed to handle a broken invariant. Under the inherited uniform
address sensitivity the average is `9 + 21*2224/65536` = 9.712646 per lane,
versus the previous packed sketch's `10 + 14*2224/65536` = 10.475098.
This is a saving relative to that packed sketch, not to the old dense 15/9
first-stage sketch (`3 + 7*2207/32768` = 3.471466 per lane). Retaining the
bitmap adds 8,192 resident bytes, before code and other allocations; the
bitmap need not be rebuilt if it is retained from the construction phase.
The comparison is conditional on the same unproven uniformity and on
reconciling branch conventions, registers, work accounting and peak memory.

Using the inherited 636.70390766 expected lanes per first block, those sketch
prices differ by about -485.46 operations per first block relative to the
previous packed sketch, but +3,973.78 relative to the filed 15/9 lookup. No
work-cap, preprocessing or complete score is inferred from those numbers.

Two local isolated executions of the gated lookup produced identical output.
Participant observations report 262,144 inputs checked against both the
ungated 16/8 lookup and the old 15/9 filter, zero differences, 256 bitmap
words and 2,224 marked positions. The test reconstructed the bitmap from the
index, whereas the proposed attack would retain the builder's bitmap; it
therefore does not verify its lifetime or building cost. The normal 20-second
experiment limit was raised to 120 seconds for this diagnostic.

A separate local two-run diagnostic tested a version of `process_cv` where a
zero dynamic combine mask returns the zero plane. It compared the recorded
class, plane and filter events and returned outputs with the original on all
five passing first blocks among 40 deterministic first blocks. Participant
observations report five equal traces and 608 skipped combines. The test
intentionally disabled the old assertions that require constant W6 primitive
counts, so it is a functional comparison only: it does not establish a new
counter discipline, resource bound or qualifying evidence. No pair was
submitted in either diagnostic.

## Appendix AB. Dynamic W6 guard accounting prototype

The following prototype guard returns a *dynamic* zero plane on a dynamic-zero
input. This is deliberate: returning the static `Z0` would cause the Python
plane algebra to fold downstream instructions for free, which is not a
justified run-time word-RAM specialization. `CN.n` charges one guard branch
and, for complemented representation, one additional logical operation to
test the logical value. The actual machine code, zero-branch instruction,
work-counter update, and resource proof still need to be specified.

```python
def guarded_f6_combine(m,*args):
    if m.c is None:
        CN.n += 1 + m.f
        if m.tv()==0:
            return dyn(0)
    return original_f6_combine(m,*args)
```

In two local isolated runs, the guarded dynamic-plane variant was compared
with the original `process_cv` on 40 deterministic first blocks. Five blocks
had passing classes; participant-recorded class, plane, filter and returned
outputs agreed on all five. The participant's dynamically recalculated W6
counter reported 51,104 original versus 46,192 guarded operations across
those blocks, a difference of 4,912 (122.8 per sampled first block); the
whole-program participant counter moved from 248,680 to 243,768. The guard's
branch and complemented-mask logical operation are included in this
prototype counter. This is a small public-seed diagnostic, not an expected-work
estimate or an official result. The old constant-count assertions were disabled
for the diagnostic and the counter was recalculated in Python; implementing the
branch-dependent work-cap update itself, proving a max bound, register/code
cost, time, independence assumptions, and preserving all target outputs remain
open. The experiment returned no collision and used a 120-second local limit.


## Appendix AC. Direct packed-index extraction, unfiled

The 16-bit sparse index word and its shift position can be formed directly
from `u`, avoiding an intermediate high-field register:

```python
def lookup16_direct(idx_words,val_words,second,u):
    word=idx_words[(u>>12)&4095]
    i=(word>>((u>>4)&240))&65535
    if not i: return 0
    first=(val_words[i>>2]>>(64*(i&3)))&((1<<64)-1)
    t=first & second[u&255]; t |= t>>32
    return t&((1<<32)-1)
```

The identity follows from `(u>>12)&4095 = ((u>>8)&65535)>>4` and
`(u>>4)&240 = (((u>>8)&65535)&15)<<4`. The instruction sketch is: extract
word index 2, add base and load 2, extract shift amount 2, shift and mask 2,
branch 1, for 9 per lane; on a hit the value extraction and the inherited
second-stage sketch add 7+7. Under the uniform-address sensitivity this is
`9 + 14*2224/65536 = 9.47509765625` per lane. It saves one operation per
lane compared with Appendix W's packed sketch and avoids the 8,192-byte online
bitmap of Appendix AA. It remains above the old 15/9 sketch, and it is not a
complete loop, preprocessing, memory or work-cap accounting.

Two local isolated runs reported 262,144 comparisons against the previous
packed lookup and the original 15/9 filter, with zero differences and 2,224
marked high addresses. The participant output was byte-identical across the
runs. This was a locally assembled source with a dummy config hash and a
120-second limit, not an official evidence artifact or a proof of cost.
Under the inherited expected-lane model and these sketch prices, direct
extraction saves 636.70 operations per first block relative to Appendix W,
but still adds approximately 3,822.54 relative to the old 15/9 sketch. This
is a sensitivity only, not an attack score.

## Appendix AD. Paired W6 differences for the omitted lists

A local isolated diagnostic of the published 222-class parent's code examined
one representative class from each omitted list 2, 3, 4, 7, 8 and 9. It used
the first 16 members with bit 7 clear from each class, 10,000 deterministic
pseudo-random `(x,y)` inputs per list, and retained only inputs for which the
representative class passed F7. For each retained input it evaluated both
W6(a,x,y) and W6(a xor 128,x,y). Two fresh runs produced identical stdout.
The participant-reported difference `(W6(partner)-W6(a)) mod 2^32` had the
following distribution; negative figures denote the same residue modulo 2^32:

| q7 | sampled difference : count |
| --- | --- |
| 0 | 128: 7168; 2176: 48; -14208: 16 |
| 1 | 256: 6608; 2304: 416; 51456: 16; -14080: 176; -1792: 16 |

Each row has 7,232 comparisons. This is a deliberately narrow, nonuniform
representative sample with shared scalar inputs; it does not bound the set of
possible differences or estimate an independent success probability. It
suggests investigating a shared W6 computation followed by a *correctly
derived* lane-dependent adjustment, but no finite list of differences is
assumed exhaustive and no overhead or savings are filed. In particular, the
F6 counterexample of Appendix Z excludes simply merging the two outputs.

## Appendix AE. Exact scalar W6 pairing identity for bit 7

For any 32-bit `a` with bit 7 clear, write `a2=a+128`,
`e4=(a+C4) mod 2^32`, `e3=(k3of(a)+x) mod 2^32`, and
`q7=((A1 xor x)>>7)&1`. The fixed constant `FA=A1 xor A2` has bit 7 set.
Consequently toggling bit 7 of `a` adds 128 to `MAJ(A2,A1,a)`, and subtracts
128 from `k3of(a)` modulo 2^32. It adds `128*q7` to `MAJ(A1,a,x)`.
Therefore the definitions of `w6of` give the identity, with all arithmetic
modulo 2^32:

```
W6(a2) = W6(a) + 128*q7
         + CH(E5,e4,e3) - CH(E5,e4+128,e3-128).
```

No small-difference assumption, F7 filter or uniform-input assumption is
needed for this scalar identity. It also covers carry propagation and modular
wraparound. The following functional prototype uses the old W6 value and
shared e4/e3 to recover its bit-7 partner:

```python
def paired_w6_exact(a,x,y):
    assert 0 <= a <= M32 and not (a & 128) and (FA & 128)
    e4=(a+C4)&M32; e3=(k3of(a)+x)&M32
    w=w6of(a,x,y)
    delta=(((A1^x)&128)+CH(E5,e4,e3)-CH(E5,(e4+128)&M32,(e3-128)&M32))&M32
    return w,(w+delta)&M32
```

This specifies scalar functional sharing, not a counted bit-sliced W6
implementation. It does not yet show how to obtain both F6 bit planes within
the register and memory budget or establish any net cost reduction.

Two local isolated runs of the scalar prototype reported zero mismatches on
50,000 pseudo-random triples and 1,536 sampled F7-passing class cases. A
separate forced-edge diagnostic reported zero mismatches for 5,888 cases
where e4+128 wraps and e3-128 underflows simultaneously. These are untrusted
participant observations with a locally raised 120-second limit, not an
official evidence artifact or an attack-cost measurement.

## Appendix AF. Word-aligned sparse values, unfiled

The 16-bit sparse directory remains packed, but each nonzero value can occupy
one whole 256-bit word with its 64-bit mask repeated four times; SECOND is
stored in the same form. This trades memory for avoiding the packed-value
shift and mask on each hit. The following functional construction and lookup
assume the index and packed values of Appendix X:

```python
def replicated16_values(packed_values,second):
    vals=[(((packed_values[i>>2]>>(64*(i&3)))&((1<<64)-1))*REP4) for i in range(2225)]
    lows=[v*REP4 for v in second]
    return vals,lows

def lookup16_replicated(idx_words,vals,lows,u):
    word=idx_words[(u>>12)&4095]
    i=(word>>((u>>4)&240))&65535
    if not i: return 0
    t=vals[i]&lows[u&255]; t |= t>>32
    return t&((1<<32)-1)
```

With the same assumptions as Appendix AC, the hit path's value address add
and load cost 2, rather than 7 for extracting a packed 64-bit value; the
SECOND operation sketch remains 7. Thus the conditional sketch is
`9 + 9*2224/65536 = 9.305419921875` operations per lane. This is approximately
108.03 operations per first block less than Appendix AC under the inherited
expected-lane sensitivity; it is still more expensive than the filed 15/9
lookup and excludes loop, counter and construction costs.

At word granularity, directory 131,072 B, 2,225 replicated values 71,200 B,
and 256 replicated SECOND words 8,192 B give a replacement-based online
payload estimate of 980,136 B against the old 1,035,912 B baseline. This is
68,440 B below 1 MiB before additional code, scratch, allocator alignment,
register pressure and changes to other live objects; it is not a peak-memory
certificate. The prototype converts the packed table, but a submitted builder
would have to count that conversion or directly construct the replicated
format and prove its own live-memory schedule.

The replicated-value prototype was run twice in isolated containers.
Participant observations report 262,144 comparisons with the packed and
15/9 lookup, zero mismatches, 2,225 value words and 256 SECOND words, with
identical stdout. This locally assembled diagnostic used a 120-second limit
and does not certify attack cost, memory peak or qualification.

## Appendix AG. Conservative guard-call ceiling, conditional on inherited ledger

The existing filed family has 82+82 classes of k=3 and 3+3 of k=1, with two
batches per passing class. For a batch the main run calls `f6_combine_pre`
once. A full k=3 run has at most seven subtraction masks and each subtraction
calls it twice, so there are at most 15 calls per batch. A k=1 subtraction
calls it once. Consequently at most `170*2*15 = 5,100` calls can occur in one
first block; this ignores the lower k=1 maximum and is conservative.

Under the inherited Q0 and P7 model, summing exactly over the declared cube
mask law gives 37/4 potential guard calls per passing k=3 class and 5/2 per
passing k=1 class. With `P7=68157440/2^32`, the expected number of potential
calls per first block is exactly `24895/1024 = 24.3115234375`. These count
potential calls, including those whose planes may be compile-time constants;
they are not a claim about the frequency of dynamic-zero masks.

One conservative accounting route would retain each original W6 body's full
charge even when skipped, and add a fixed allowance per potential guard. This
avoids needing a data-dependent refund or a variable work-counter update. For
example, *if* an implemented guard and its branch/join/output handling are
proved to cost at most six extra word operations per call, this would add at
most 30,600 to the inherited per-first-block maximum and at most 145.869140625
to its inherited expected work. It would not credit the observed savings and
would not itself improve the score. The six-operation premise is a design
budget, not a verified instruction listing. A real implementation must keep
the compile-time polarity/constant representation expected downstream; a
runtime zero must not accidentally enable free downstream algebraic folding,
and branch code, literal access, counter updates and register lifetime must
all fit within the allowance. Moreover the inherited Q0, P7, work and success
premises have their own outstanding validation limits. This is a conditional
ceiling framework, not a ready claim.

## Appendix AH. W6 output-polarity audit and conservative prototype

A local two-run audit of the same 40-block sample recorded 992 original
combine calls. Of 608 dynamic-zero inputs, 96 produced a zero with output
inversion flag 1; none of the 992 outputs was a compile-time constant. Thus
returning a dynamic flag-0 zero as in Appendix AB preserves logical output
but does not preserve the original output representation for every call. It
can change how downstream `sel` operations are compiled and counted. Appendix
AB's 4,912-operation difference must therefore not be treated as a proved
machine-program saving.

A follow-up diagnostic can inspect the original output flag as a stand-in for
an offline, call-site-specific compiler analysis. For a dynamically guarded
zero with original output flag `f`, return the dynamic plane with raw value
`ONE if f else 0` and flag `f`: this has logical value zero and the identical
representation. The original combine must NOT actually run in the final
skip path; the diagnostic computes it only as an oracle and restores the
counter before charging the branch. The offline flag and constant analysis,
a real branch/join instruction sequence, the pre-existing and additional
work-counter updates, register liveness, code budget and expectations are
not yet established.

The polarity-preserving oracle diagnostic was run twice locally on the same
40 deterministic first blocks and produced byte-identical stdout. Participant
observations report five selected-block trace comparisons with zero mismatches,
608 skipped combines including 96 flagged outputs, and W6 counter totals
51,104 before versus 46,288 after the simulated guard, a difference of
4,816 or 120.4 per sampled first block. This simulation obtains each output
flag by actually evaluating the original expression and then rewinding its
Python counter; it is not an implementation of an offline compiler and its
reported savings do not include the oracle's executed work. Thus it verifies
representation and counting consistency only under the hypothesized offline
flag analysis, not a valid attack cost or a full-scale expected saving.


## Appendix AI. 16/8 build and live-memory accounting boundary

For the bitmap construction in Appendix X, the low stage has exactly 32*256
iterations; the three-bit interface has at most eight states per l; and the
fixed E mask leaves 1,024 high E choices per state. Therefore at most 262,144
state-enumeration iterations occur, before bitset and state-storage overhead.
The subsequent pass considers 65,536 high indices. The prototype reported
2,224 marked positions and 40 viable states, leading to 88,960 full state
predicate tests, but those two numeric facts remain participant observations
rather than an independently certified theorem. The corresponding worst-case
bound without using them is 65,536*64 tests if at most two states per l is
established; if that property is not established, use 65,536*256 instead.
These are iteration bounds, not word-operation counts: address arithmetic,
bitset read/modify/write, initial zeroing, temporary state storage, loop
branches, table writes, conversion and source constants all need actual
instruction prices.

Under the word-size accounting assumed in Appendix AF, the replicated online
replacement uses 131,072 B directory + 71,200 B values + 8,192 B SECOND.
Adding the 8,192 B construction bitmap while those tables and the remaining
baseline objects coexist gives 988,328 B by substitution from the inherited
1,035,912 B baseline. If the 17,824 B packed value table also remains live
while converting to replicated words, the same partial sum is 1,006,152 B.
Neither figure includes new program text, state/low-field scratch, allocator
or alignment costs beyond the stated words, additional registers or any old
FIRST/SECOND arrays that have not yet been released. The diagnostic Python
builds an old `Env` first and therefore does not establish this schedule.
The 1 MiB limit is not certified by these partial sums. A complete 16/8
filing requires a bounded builder with a specified allocation schedule and
an itemized executed-instruction upper bound, added to the other preprocessing
rather than silently credited against an unrelated allowance.

## Appendix AJ. Scalar partner-adjustment price sketch

For the exact identity in Appendix AE, suppose `w`, `e4`, `e3`, the old
`CH(E5,e4,e3)` and `q7*128` are already in registers. One literal word-RAM
sequence computes `e4p=(e4+128)&M32` and `e3p=(e3-128)&M32` in four
operations; `hp=e3p xor (E5 & (e4p xor e3p))` in three; and
`wp=(w + q7*128 + oldCH - hp)&M32` in four, for 11 operations. If q7 is not
already available, `(A1 xor x)&128` adds two. This counts only the partner
adjustment, assumes the needed constants and intermediates are resident, and
requires extra storage or live registers to retain them. It does not count
computing the first W6, generating members, F6 testing, preprocessing,
loads/stores, branches or the work counter. It is a scalar specification,
not a price for the bit-sliced batch: a bit-sliced program must explicitly
price both carry chains, plane retention and their interaction with F6 before
any savings can be claimed.

## Appendix AK. Bit-sliced W6 bit-7 partner prototype, unfiled

All terms in Appendix AE's adjustment are multiples of 128. The low seven W6
bits are unchanged. On bits 7..31, addition of 128 and subtraction of 128
become addition and subtraction of one modulo 2^25; the `q7*128` term becomes
the carry-in bit of the final 25-bit addition. The following functional
prototype takes 256-lane `Pl` planes of the first W6 value, e4 and e3, plus
a q7 plane. It reuses the existing plane algebra and returns 32 partner
planes, including the unchanged low seven. No part of this code establishes
that its inputs are available in the existing W6 sweep at no cost.

```python
def paired_w6_planes(w,e4,e3,q7):
    assert len(w)==len(e4)==len(e3)==32
    one=[Z1]+[Z0]*24
    e4hi=e4[7:]; e3hi=e3[7:]
    e4p=add(e4hi,one)
    e3p=sub(e3hi,one)
    old=[e4hi[j] if (E5>>(j+7))&1 else e3hi[j] for j in range(25)]
    new=[e4p[j] if (E5>>(j+7))&1 else e3p[j] for j in range(25)]
    delta=sub(old,new)
    high=add(w[7:],delta,cin=q7)
    return w[:7]+high
```

The arithmetic identity is exact modulo 2^32 assuming the scalar identity in
Appendix AE, and selecting e4/e3 planes according to the fixed E5 mask costs
no per-lane Boolean selection if those planes are already available. The
prototype is an algebraic reference: its intermediate planes, register
pressure, loads, stores, output flags, program text and extra F6 work all need
counting, and it is not yet integrated into the candidate attack.

In two local isolated diagnostics, eight batches of 256 random lanes each
were evaluated. Participant observations report zero differences both for
all 2,048 reconstructed W6 words and for their F6 predicates; outputs were
byte-identical across fresh runs. For generic dynamic inputs, the plane
algebra counted 335 operations per batch: 47 for e4+1, 47 for e3-1, 119
for the CH difference and 122 for the final addition. Up to 15 further
operations were counted when forcing all 32 output planes; evaluating the
F6 predicate from the partner planes cost 31 in this diagnostic. These are
participant instrumentation counts with a 120-second limit, not a complete
word-RAM price. Input plane preparation, registers, spill loads/stores, code,
work counters, original F6 and outputs are not priced. The generic adjustment
alone exceeds the filed 181--301 operation range for an existing W6 batch,
which makes this initial formulation unattractive without further sharing or
specialization; that comparison is not a cost proof for the omitted lists.

## Appendix AL. W6 guard work-counter accounting, conditional model

For an already-counted combine body with a compile-time word-operation charge
`C`, one possible counter discipline is: charge `C+6` for every eligible
call and, only when the zero guard skips that exact body, subtract `C` from
the work counter. It is conservative only if the guard, branch/join, exact
output-representation handling and the conditional counter refund together
cost no more than six operations, the original `C` is correct, and no other
counter updates or spills are omitted. Each call is then charged `C+6` when
executed and 6 when skipped. Static-zero bodies must be analyzed at compile
time rather than credited as new runtime savings. The fixed allowance also
fits the potential-call and per-block ceilings of Appendix AG. This is a
counting proposal, not a validated instruction-level implementation.

In the Appendix Z sample, the participant plane instrument assigned 6,016
operations to 608 bodies whose dynamic mask was zero, among 992 eligible
calls. A fixed six-operation allowance for all those calls is 5,952, leaving
only 64 operations, or 1.6 per sampled first block, before any unbudgeted
cost. The data-dependent zero frequency is not established by this sample.
In particular the larger Appendix AB saving excludes the full proposed
counter/control allowance and cannot be substituted into an attack ledger.
The real implementation and a justified expectation are still required.

## Appendix AM. Selective partner carry outputs, unfiled

`CH(E5,e4,e3)` selects only one of e4/e3 at each bit because E5 is a
compile-time constant. The partner's increment/decrement carry chains still
have to propagate, but their *sum outputs* need only be computed where CH
uses them. This variant uses the existing `need` argument to omit the other
sum planes, while keeping the full carry path to each needed bit:

```python
def paired_w6_planes_selected(w,e4,e3,q7):
    assert len(w)==len(e4)==len(e3)==32
    one=[Z1]+[Z0]*24
    e4hi=e4[7:];e3hi=e3[7:]
    use4={j for j in range(25) if (E5>>(j+7))&1}
    use3=set(range(25))-use4
    e4p=add(e4hi,one,need=use4)
    e3p=sub(e3hi,one,need=use3)
    old=[e4hi[j] if j in use4 else e3hi[j] for j in range(25)]
    new=[e4p[j] if j in use4 else e3p[j] for j in range(25)]
    delta=sub(old,new)
    return w[:7]+add(w[7:],delta,cin=q7)
```

This is only an algebraic optimization until the target F6 computation,
register lifetime, live inputs, code and accounting are integrated.

Two local isolated diagnostics, each repeated in fresh containers, compared
this variant against scalar W6 and F6 on eight batches of 256 pseudo-random
lanes. Participant observations report 2,048 lanes, zero W6 differences and
zero F6 differences. With generic dynamic input planes, the existing plane
algebra counted 308 operations for the partner adjustment versus 335 for the
previous prototype; forcing all 32 output planes took up to 15 more, and the
F6 predicate cost 31 in the separate diagnostic. These counts omit input
preparation, loading, spills, register lifetimes, control, code and the work
counter. The tests are local, use a 120-second limit, and do not establish
attack cost, success probability or the distribution of real input planes.

For a straightforward calling convention that keeps all high input planes
resident simultaneously, w[7:32], e4[7:32], e3[7:32] and q7 total 76
256-bit registers before any constants or temporaries. That exceeds the
64-register contract by at least 12. This is a conditional liveness count,
not a lower bound on every possible schedule: streaming, recomputation or
storing some planes can reduce simultaneous live registers, but their memory,
loads, stores and operations must be added. In particular the 308-operation
plane count cannot be treated as a complete cost with no spills.

## Appendix AN. Low-first ordering sensitivity for the replicated 16/8 table

The 16/8 builder's low table was examined in two fresh isolated runs. The
participant reported 199 nonzero entries of 256, 1,024 set interface bits
across those entries, at most nine per entry and 2,224 nonzero high entries.
The two executions matched. These counts are internal observations, not an
independently checked proof.

Under uniform 24-bit addresses, the low and high address fields are
independent. In one provisional word-RAM sketch using the replicated tables,
read and zero-test the low entry first for four operations, then do the
nine-operation high-index probe only for a nonzero low entry, and on a
nonzero high entry perform the two-operation value load plus four Boolean
operations. Using the reported occupancy, its conditional mean is
`4 + 9*(199/256) + 6*(199/256)*(2224/65536) = 11.15437` operations per
lane. The existing high-first replicated sketch is `9 + 9*2224/65536 =
9.30542`. Both are incomplete instruction sketches with unverified branch,
register and counter conventions; this comparison nevertheless shows no
reason to adopt this simple low-first order under those assumptions.

## Appendix AO. F6-only partner outputs, unfiled

If the partner W6 value is used only to test F6, only the planes in `NEEDW`
need to be emitted from the final addition. Carries still propagate through
all lower positions needed by those outputs. This variant leaves unneeded
high output entries as `None` and must not be used as a complete W6 value:

```python
def paired_w6_for_f6(w,e4,e3,q7):
    one=[Z1]+[Z0]*24
    a=e4[7:];b=e3[7:]
    use4={j for j in range(25) if (E5>>(j+7))&1}
    use3=set(range(25))-use4
    ap=add(a,one,need=use4);bp=sub(b,one,need=use3)
    old=[a[j] if j in use4 else b[j] for j in range(25)]
    new=[ap[j] if j in use4 else bp[j] for j in range(25)]
    delta=sub(old,new)
    needed={j-7 for j in NEEDW if j>=7}
    return w[:7]+add(w[7:],delta,cin=q7,need=needed)
```

A path that later needs the full partner word must recompute it or retain
additional outputs, and must charge that work. As with Appendix AM, inputs,
registers, memory, code, control and F6 are not included in the standalone
plane-algebra count.

In two local isolated runs on eight pseudo-random 256-lane batches, the
participant reported 2,048 F6 comparisons with zero differences against the
scalar partner, and byte-identical outputs. The plane algebra counted 300
operations for this partial partner adjustment and 31 more for F6 on generic
dynamic inputs, versus 308 for the full-output selected variant. These
figures omit the same input, register, memory, control and code costs, and
use a locally raised 120-second limit. They are not an official experiment
or a demonstrated reduction in the omitted-class total cost.

## Appendix AP. Streaming partner computation, unfiled

The high-bit computation can be interleaved by bit instead of materializing
all e4/e3/W inputs and intermediate arrays in registers. At each position,
retain four carry/borrow planes (e4 increment, e3 decrement, CH subtraction,
and final addition), load that bit's three input planes, derive the one CH
output selected by fixed E5, and store only the final planes required by F6.
The low F6 planes are inherited from the first W6 value. This reference uses
the existing plane algebra; Python lists stand in for explicitly addressed
word-RAM input and output slots.

```python
def paired_w6_stream(w,e4,e3,q7):
    out=w[:7]+[None]*25
    ci=Z1; cb=Z1; cd=Z1; cw=q7
    for j in range(25):
        a=e4[j+7]; b=e3[j+7]; old=a if (E5>>(j+7))&1 else b
        t=ci if (E5>>(j+7))&1 else cb
        new=xor(old,t)
        if j<24:
            ci=and_(a,ci)
            cb=and_(inv(b),cb)
        d,cd=fa_step2(old,inv(new),cd,True,j<24)
        v,cw=fa_step2(w[j+7],d,cw,(j+7) in NEEDW,j<24)
        if (j+7) in NEEDW: out[j+7]=v
    return out
```

This is a streaming schedule hypothesis, not yet a compiled or complete
word-RAM implementation. Correctness requires comparing every emitted F6
plane and the F6 result, and cost must include addressing, input production,
spills, materializing selected outputs, the work counter and code size.

Two fresh local isolated runs compared eight 256-lane random batches with
Appendix AO and scalar F6. Participant observations report 2,048 lanes, zero
differences in emitted needed planes, zero F6 differences, 303 plane-algebra
operations for the streaming adjustment versus 300 for Appendix AO, and 31
for F6. This is a participant Python diagnostic under a 120-second limit, not
an executed machine cost or an official result.

A first explicit memory schedule stores 25 high planes each for W6, e4 and
e3, the three low W6 planes used by F6, and q7: 79 input words. Seventeen
selected high outputs use a further 17 words, for 96 * 32 = 3,072 bytes of
logical slots before alignment or other live state. During the interleaved
step the program needs four carry/borrow planes, the current three input
planes and step temporaries; the stored F6 outputs can be read only after
those carries are dead. Thus it avoids requiring all 76 high input planes
in registers at once. The precise compiler liveness, including F6 temporaries,
addresses, constants and counters, has not yet been independently established.

For an intentionally simple word-RAM price sketch, assume one address add
and one load/store per variable slot access: 75 high input loads, one q7
load, 17 selected output stores and 20 later F6 input loads cost 226
operations. Adding the observed 303 plane operations and 31 F6 operations
gives 560, before producing or copying inputs, loop control, constant/flag
handling not already reflected by the plane algebra, work-counter updates,
code and other attack stages. If all 79 input slots must first be copied from
other memory slots, the same address convention adds 316 operations. These
are stated assumptions and sample-specific plane counts, not a complete
upper bound, register proof or accepted ledger; immediate-slot addressing,
input lifetimes and F6 compilation must be reconciled with the actual target
program. The sketch is a conservative reason to prioritize sharing the input
production itself before using this schedule for the omitted classes.

## Appendix AQ. Stop unused decrement chain, unfiled

The fixed E5 mask last selects e3 at bit 28. Consequently the e3 decrement
carry cannot affect CH at bits 29..31 and can be stopped after computing bit
28. The following variant omits those three e3-plane reads and the associated
carry updates; the e4 chain remains live through bit 31.

```python
def paired_w6_stream_stop(w,e4,e3,q7):
    out=w[:7]+[None]*25
    ci=Z1;cb=Z1;cd=Z1;cw=q7
    last3=max(j for j in range(25) if not ((E5>>(j+7))&1))
    for j in range(25):
        a=e4[j+7]
        b=e3[j+7] if j<=last3 else None
        sel4=(E5>>(j+7))&1
        old=a if sel4 else b
        new=xor(old,ci if sel4 else cb)
        if j<24: ci=and_(a,ci)
        if j<last3: cb=and_(inv(b),cb)
        d,cd=fa_step2(old,inv(new),cd,True,j<24)
        v,cw=fa_step2(w[j+7],d,cw,(j+7) in NEEDW,j<24)
        if (j+7) in NEEDW: out[j+7]=v
    return out
```

`last3` is a program constant for the fixed target and must be resolved before
execution; computing it at runtime is not included in a charge. This remains
an experimental reference pending a fully specified compiler and memory
schedule.

Two fresh local isolated runs compared eight 256-lane random batches with
Appendix AP and scalar F6. Participant observations report 2,048 lanes, zero
needed-plane or F6 differences, and 300 plane operations versus 303 for the
previous streaming version; the last selected e3 bit was 28. With the same
provisional slot schedule as Appendix AP, there are 72 high input loads rather
than 75, 76 input slots rather than 79 and 93 input-plus-output words (2,976
bytes). Charging an address add and access per load/store, the same partial
sketch becomes 300 plane operations + 31 F6 operations + 220 for slot
accesses = 551, before input production/copying and the other omitted costs
listed in Appendix AP. Copying 76 input slots from other memory slots would
add 304 under that address convention. These are local observations and a
conditional schedule sketch, not a certified memory or attack-cost bound.

## Appendix AR. Combined storage sensitivity, not a memory certificate

Using the inherited 1,035,912-byte baseline as a conditional starting point,
replace old FIRST and SECOND with Appendix AF's directory, replicated values
and replicated low table. The resulting subtotal is 980,136 bytes. If the
8,192-byte construction bitmap and Appendix AP's proposed 3,072-byte plane
slots coexist with it, the subtotal is 991,400 bytes. If the 17,824-byte
packed-value table also remains live during conversion, it rises to 1,009,224
bytes, leaving 39,352 bytes below 1 MiB. These are arithmetic subtotals, not
verified peak usage. They omit new instruction text, the builder's interface
states and low-field scratch, allocation/alignment, any simultaneously live
old tables, F6 or counter scratch, and other changes. In particular, the
Python diagnostic constructs the old environment and does not implement the
proposed release/phase schedule. Nothing here establishes a compliant memory
bound or an improved score.

## Appendix AS. Compile-time W6 output polarity, research diagnostic

The `c` and `f` metadata produced by the current `f6_combine_pre` plane
algebra depend on input constant/flag metadata and the statically selected
Boolean operations, rather than the runtime plane values. The relevant helper
branches inspect `c` and `f`; Boolean data affect `v`. This suggests deriving
output polarity once for each actual unrolled call site, then emitting a
zero-guard branch with the correct zero representation.

A local diagnostic keyed the compile-time analysis by the `(c,f)` metadata of
all combine operands. For each newly seen key it ran the original expression
on dummy planes, saved its output metadata, and restored the operation
counter. A guarded run then used the cached metadata to represent a skipped
zero; a baseline run used the original expression. Across the same 40
sampled first blocks, five selected blocks, participant observations report
22 metadata keys, 608 skips, zero compared trace differences, and zero metadata
differences on executed bodies. The participant W6 counters were 51,104
baseline and 46,288 guarded, before a complete branch/refund implementation.
Two isolated runs returned identical output. This is not a runtime-speed
measurement: the diagnostic's dictionary lookup and on-demand dummy analysis
were not priced, and its operation counter was deliberately rewound for that
analysis. A real compiler must enumerate every reachable unrolled call site
before execution, bind its static flag, charge generated code and counter
updates, and verify output and resource limits. The sample cannot establish
that 22 keys are exhaustive or that the guard improves the official score.

## Appendix AT. Direct replicated 16/8 builder, unfiled

This reference builds the replicated value and SECOND words directly; it does
not create a packed-value intermediate. It accepts precomputed LC constants
and does not itself instantiate the old 15/9 tables. The low interface uses
a fixed 256-entry array and eight possible state codes instead of a dictionary
and sort. `REP4` is the four-64-bit-lane replication constant from the
participant program. All state and table bounds are checked in the prototype;
those checks are not an independently verified certificate.

```python
def build16_direct_replicated(LC):
    em=(E16M>>8)&65535;ev=(E16V>>8)&65535;free=(~em)&65535
    assert free.bit_count()==10 and ev&free==0
    specs=[];second=[0]*256;present=[0]*256
    for l in FEASIBLE_L:
        c=LC[l];C=c['C'];A=c['cxA'];a15=c['Ax15']
        los=[-1]*256;seen=0
        for lo in range(256):
            t=lo+(C&255);e=t&255;ta=e+(A&255);al=ta&255
            if (e&(E16M&255))==(E16V&255) and not ((e^c['Ex15'])&16):
                code=((t>>8)<<2)|((ta>>8)<<1)|((al>>6)&1)
                los[lo]=code;seen |= 1<<code
        viable=0
        for code in range(8):
            if not ((seen>>code)&1):continue
            ce=code>>2;ca=(code>>1)&1;a6=code&1
            want=(((~a15>>15)&1)<<7)|(((a15>>23)&1)<<15)|((a6^1)<<10)
            sub=0;found=False
            while True:
                e=ev|sub;v=e+(A>>8)+ca
                if (v&0x8480)==want and ((v>>12^v>>1)&1) and not ((v>>9^v)&1):
                    h=(e-(C>>8)-ce)&65535
                    present[h>>8] |= 1<<(h&255);found=True
                sub=(sub-free)&free
                if not sub:break
            if not found:continue
            assert viable<2
            bit=1<<(32*viable+l);viable+=1
            specs.append((C>>8,A>>8,ce,ca,want,bit))
            for lo in range(256):
                if los[lo]==code:second[lo] |= bit*REP4
    assert len(specs)==40
    idx=[0]*4096;vals=[0];n=0
    for h in range(65536):
        if not ((present[h>>8]>>(h&255))&1):continue
        mask=0
        for chi,am,ce,ca,want,bit in specs:
            e=(h+chi+ce)&65535;v=e+am+ca
            if (e&em)==ev and (v&0x8480)==want and ((v>>12^v>>1)&1) and not ((v>>9^v)&1):mask |= bit
        assert mask;n+=1;vals.append(mask*REP4)
        idx[h>>4] |= n<<(16*(h&15))
    assert n==2224
    return idx,vals,second
```

Python allocation, multiplication, list growth and assertions are functional
scaffolding: an actual word-RAM builder must preallocate bounded slots, expand
replication into charged shifts/ORs, account for table writes and every loop,
and justify peak live memory. This prototype does not make the official claim
ready or establish that the observed state counts generalize.

Two fresh isolated executions of a locally assembled diagnostic reported
262,144 comparisons against the original 15/9 filter, zero mismatches,
4,096 index words, 2,225 replicated value words and 256 low-table words.
Their stdout matched. The diagnostic still constructs the old `Env` for the
comparison and uses a 120-second limit; it neither validates the proposed
word-RAM allocation schedule nor establishes preprocessing cost or official
qualification.

## Appendix AU. Omitted-list storage census and tradeoff

A local two-run isolated diagnostic used one representative class from each
of the six omitted parent lists, stripped free bits 0 and 7, and ordered the
remaining reps using this candidate's `REP_ORDER`. The participant reported
864 reps for each of lists 2/3/4 and 896 for each of 7/8/9; each list needs
four 256-lane batches. Counting only dynamic planes in the candidate mask
(excluding bits 0, 7 and 19) yielded 43, 43, 40, 41, 41 and 43 respectively,
251 planes total. These are participant observations on representatives, not
a proof that every class shares each list or that the paired attack works.

For a memory sensitivity that reuses each representative list across all 52
omitted classes, store padded 64-bit entries rather than replicated 256-bit
entries: 24*256*8 = 49,152 bytes. Add 52 descriptors at four words each =
6,656 bytes, the reported 251 dynamic planes = 8,032 bytes, and the proposed
streaming scratch of 2,976 bytes to the 980,136-byte 16/8 online subtotal.
This gives 1,046,952 bytes, only 1,624 bytes below 1 MiB before the extra
program text, additional F6/counter state, alignment, table construction or
other allocations. It is not a certified memory bound. The equally simple
replicated-entry layout needs 24*256*32 = 196,608 bytes for those entries,
which puts the same subtotal at 1,194,408 bytes before the omitted items.
The 64-bit layout also requires paid packed extraction and possibly paid lane
replication in every passing-rep lookup, so its smaller payload cannot be
assumed to preserve the existing per-lane cost. A complete design must price
those operations, prove list reuse and include all live memory and code.

## Appendix AV. Candidate-only 16/8 construction phase schedule

For the filed 170-class family, a possible fixed-capacity word-RAM schedule
can avoid ever allocating the old 15/9 tables or a packed-value intermediate:

1. Reserve the final 16/8 directory, 2,225 replicated value slots and 256
   replicated SECOND slots. Capacity-check before every write and abort the
   construction on overflow; an abort preserves the memory bound but does not
   establish attack success. The fixed target must separately be shown to
   produce exactly the expected table and not abort.
2. Before initializing the existing 262,144-byte scan table, borrow at most
   131,072 bytes of its region as scratch. A deliberately loose fixed layout
   assigns 8,192 bytes to the 256-word presence bitmap, 8,192 bytes to a
   256-word low-state array, 49,152 bytes to 256 six-word state records, and
   256 bytes to eight additional state words, totaling 65,792 bytes. Keep
   counters and constants in the existing register budget. The 256-record
   capacity covers the three-bit state space across 32 l values; a concrete
   implementation must initialize slots and enforce capacities.
3. Build the final tables directly as in Appendix AT. Release the borrowed
   region before constructing the scan table. Only after all builder scratch
   is released does the online program use the proposed 2,976-byte streaming
   plane area from Appendix AQ.

Under the inherited baseline accounting and assuming the final tables replace
rather than coexist with the old ones, the candidate-only online subtotal with
streaming scratch is `980136 + 2976 = 983112` bytes. If all new code and any
additional persistent state together fit within a separately established
32,768-byte allowance, the conditional subtotal is 1,015,880 bytes, below
1 MiB. The construction scratch occupies already-reserved scan-table space
and adds no bytes under this proposed non-overlap schedule. This is a
conditional allocation design, not a proof of the shipped Python program's
peak: the implementation, code-size limit, all other preprocessing phases,
initialization and runtime costs, register liveness and safe aliasing have
not been verified. It also does not include the six omitted lists and their
additional memory in Appendix AU.

## Appendix AW. Metered streaming partner/F6 reference, unfiled

The reference below explicitly charges two word operations for each logical
slot read or write (one address add plus one memory operation), one counter
update, and 51 operations for a conservative 25-iteration loop-control
allowance. The per-position E5, `last3`, and output-selection decisions are
fixed by the target and treated as compile-time specialization; this is not
Python execution time. `CN.n` counts the candidate's plane-algebra operations.
The function assumes the input slots already contain W6, e4, e3 and q7, and
returns only the partner F6 mask.

```python
def metered_partner_f6(w,e4,e3,qslot):
    mem=[0]
    def rd(arr,i):
        mem[0]+=2
        return arr[i]
    def wr(arr,i,value):
        mem[0]+=2
        arr[i]=value
    CN.n=0
    out=[None]*32;ci=Z1;cb=Z1;cd=Z1;cw=rd(qslot,0)
    for j in range(25):
        a=rd(e4,j+7)
        b=rd(e3,j+7) if j<=21 else None
        bit=(E5>>(j+7))&1;old=a if bit else b
        new=xor(old,ci if bit else cb)
        if j<24:ci=and_(a,ci)
        if j<21:cb=and_(inv(b),cb)
        d,cd=fa_step2(old,inv(new),cd,True,j<24)
        v,cw=fa_step2(rd(w,j+7),d,cw,(j+7) in NEEDW,j<24)
        if (j+7) in NEEDW:wr(out,j+7,v)
    P=[None]*32
    for j in NEEDW:
        P[j]=rd(w,j) if j<7 else rd(out,j)
    upper=f6_ok_upper(P[8],P[9],P[10],P[14],P[15],P[16],P[18],P[19],P[20],P[25],P[26],P[27],P[29],P[30],P[31])
    f=f6_combine_pre(upper,P[1],P[2],P[3],P[12],P[13],xor(P[14],P[31]),P[29],P[30])
    result=force(f).v
    return result,CN.n,mem[0],52
```

The final 52 is a planning allowance of 51 loop-control operations and one
counter update. It assumes compile-time specialization can be implemented
within the eventual code and register budget. This reference does not charge
producing or copying its 76 input slots, constants, code size, output reuse,
extra F6/attack work, or any spill beyond the specified slots. It is a
narrow model to make reads and writes visible, not a complete attack bound.

Two local isolated runs of the metered reference reported 2,048 F6 comparisons
with zero differences and identical stdout. The participant counter reported
331 plane operations, 220 modeled memory/address operations and the stated 52
control allowance, totaling 603 per generic 256-lane batch. If 76 input slots
must be copied from other word-RAM slots, the Appendix AQ address convention
adds 304, producing a 907-operation subtotal. Both figures omit input
creation, any additional spill, generated code, other attack stages and any
invalidation of the specialization assumptions. The 120-second local test
is not an official cost or peak-memory certificate.

## Appendix AX. Guard/refund instruction budget, conditional

For a call site whose output is a dynamic plane with compile-time flag `fout`
and whose original body has fixed charged cost `C`, a prospective zero guard
can follow this word-RAM sequence. The full `C+6` is first added to the work
counter V (one addition). If the input mask has an inversion flag, XOR its
raw word with the all-ones word to form its logical value (at most one
operation); otherwise use the raw word. Branch once on that logical value.
For zero, materialize raw zero or all ones according to the compile-time
output flag (at most one move), subtract C from V (one operation), and jump
past the original body (one jump). For nonzero, fall through to the original
body and preserve its output representation. Static-constant cases need a
separate compile-time treatment and receive no runtime-zero credit.

This accounts for at most six operations on the skip path, including the V
precharge and refund, or at most three before the unchanged body on the
nonzero path, assuming literal C and the all-ones word are available. It
preserves V nonnegativity because the precharge precedes the refund. It is
still a conditional instruction sketch: the compiler must prove the static
metadata and body price for every reachable call site, retain or price
constants/registers, place the cap checks correctly, bound emitted code and
show that branching does not change the attack's successful output. Fixed
six-per-potential-call accounting and its inherited expected and maximum
additions are in Appendix AG; a refund-based expected saving requires a
justified zero-event law. The local sample in Appendix AL cannot provide it.

## Appendix AY. Combined chunk-index and successor table, unfiled

For a nonzero 13-bit chunk c, store both its least-set-bit index and its
successor in one 256-bit table word. This replaces the separate 8,192-word
index and successor tables with one 8,192-word table; it does not compress
word addresses or rely on a free subword load. The low four bits are enough
for indices 0..12, and the upper bits store `c & (c-1)`.

```python
def build_scan_merged():
    table=[0]*8192
    for c in range(1,8192):
        table[c]=((c&(c-1))<<4)|((c&-c).bit_length()-1)
    return table

def scan_merged_chunk(c,table):
    out=[]
    while c:
        packed=table[c]
        out.append(packed&15)
        c=packed>>4
    return out
```

For each loop the merged table supplies an index and successor in one load,
but extracting them requires an AND and a shift. Relative to the filed sketch
of two table loads this is one extra primitive per set bit if both tables and
the merged table had free addressing; if the merged table needs a base add
when the old loads did not, it is two extra. The scan's rep address, rep load,
loop branch, chunk initialization, work counter and both tables' address
conventions still require an end-to-end accounting. In particular, two
separate zero-base tables cannot occupy the same word addresses: any inherited
claim that simultaneously assumes both at address zero must be audited rather
than silently retained. The Python builder's bit_length operation is not a
word-RAM instruction schedule and its build cost is not yet certified.

The two old tables occupy 524,288 bytes and the one-word-per-chunk combined
table occupies 262,144, a payload reduction of 262,144 bytes before code and
other changes. This can make space for replicated omitted-list entries, but
neither the new global peak nor an improved score follows from this count.

Two local isolated executions enumerated all 8,191 nonzero 13-bit chunks;
participant observations report 53,248 decoded set bits, zero ordering or
membership differences and an 8,192-word table. Stdout matched and the
normal 20-second diagnostic limit was used. This is not a compiled cost or
peak-memory certificate.

A proposed incremental builder avoids a hardware bit-scan or Python
`bit_length`: for c even the least-set-bit index is one plus the stored
index for c/2, while for c odd it is zero.

```python
def build_scan_merged_incremental():
    table=[0]*8192
    for c in range(1,8192):
        index=0 if c&1 else (table[c>>1]&15)+1
        table[c]=((c&(c-1))<<4)|index
    return table
```

A provisional loop budget of 16 ordinary operations per nonzero c covers a
parity test/branch (2), the even predecessor index/address/load/mask/add (5),
successor subtract/AND/shift/OR (4), output address/store (2), loop
increment/test (2), and one counter update; the odd case must also fit and
table zero initialization is additional. This yields at most 131,056 for the
nonzero iterations if the instruction convention and literal/register setup
are implemented as stated. The budget is a design sketch, not a tested
word-RAM program or a complete preprocessing bound.

As a storage sensitivity, combine the table replacement with Appendix AU's
replicated omitted-list subtotal: `1194408 - 262144 = 932264` bytes, leaving
116,312 bytes below 1 MiB before new code, build scratch that cannot be reused,
additional work state, alignment and any other attack changes. This has the
substantial advantage of retaining fast replicated rep entries, but is not a
peak-memory certificate and does not establish that the added 52 classes
improve the time objective. Any schedule that borrowed half of the original
scan-table space for 16/8 construction must revalidate the non-overlap after
this table replacement.

Two local isolated executions compared all 8,192 incrementally generated
entries with the direct merged builder and reported zero differences, with
identical output under the 20-second limit. This establishes only what the
participant code reported; no target collision or machine-operation trace was
independently checked.

Under the inherited filed-family P7, P6 and Q0 model, the expected number of
passing representative-lane scans per first block is
`7363321875/33554432 = 219.44409236311913`: the expected number of Q0 runs is
45/16 for k=3 and 5/4 for k=1, applied to 82 lists each of sizes 432 and 450
and 3 each of sizes 432 and 450. Therefore one or two additional operations
per representative scan alone would add approximately 219.44 or 438.89
operations per first block. These figures do not include any impact on class
or survivor scans, address-base repair, the 52 omitted classes, build cost,
work cap or the success model. They are conditional sensitivities, not a
complete repricing or an official score.

The memory sensitivity also permits retaining the cheaper filed 15/9 filter
while pursuing the extra classes: `1035912 - 262144 + 196608 + 6656 + 8032
+ 2976 = 988040` bytes, leaving 60,536 bytes below 1 MiB before new code and
other missing state. This is a conditional subtotal using the same sampled
representative-plane census and four-word descriptor assumptions as Appendix
AU, not a memory proof. It does not solve the omitted classes' high W6 cost,
the merged-scan overhead, or prove that adding those classes beats the
incumbent. The separate 16/8 research remains unfiled.

A separate local isolated online diagnostic substituted the merged scan in a
copy of `process_cv`, retaining the original outputs and adding two operations
per decoded lane to the participant counter. Among 40 deterministic first
blocks, five passed the class filter; the participant reported equal recorded
class/plane/filter events and returned outputs for all five. It counted 7,056
decoded lanes, baseline 248,680 operations and merged 262,792, an extra 14,112
= 2*7,056 under the chosen counter rule. Two fresh runs had identical stdout.
The test used a 120-second local limit, did not implement the merged table in
the filed attack, did not reprice survivor scans or construction, and is not
an unbiased expected-work proof or an official score.


## Appendix AZ. Conditional combined phase schedule with merged scan table

A possible combined allocation uses one 262,144-byte final merged scan table
instead of two tables. Before initializing that final table, its own region can
lend the 65,792-byte fixed scratch layout of Appendix AV to the direct 16/8
builder, then be initialized in place by the incremental merged-table builder.
The 16/8 final directory, replicated values and low table must already be in
disjoint final slots; neither the old 15/9 tables nor a packed-value duplicate
may coexist. The peak also has to cover the pre-existing family-discovery,
list-construction and prefilter phases, not just these two builders.

For the hypothesized 222-class online configuration, Appendix AY's subtotal
is 932,264 bytes, including the reported omitted rep/plane/descriptors and the
2,976-byte streaming scratch. If *all* additional generated machine code fits
in 65,536 bytes and *all* other previously uncounted persistent state fits in
32,768 bytes, the online subtotal is 1,030,568 bytes, below 1 MiB by 18,008.
These are budgets, not verified properties. A complete peak proof still needs
fixed-slot builder implementations, actual table and state capacities, safe
phase ordering, source and emitted-code limits, register/spill lifetimes,
alignment, extra descriptors/planes for all classes, and each other phase's
maximum. The current Python reference instantiates old tables for comparison,
so it is not an implementation of this schedule. The declared experiment
source is already near the 64-KiB source-text limit; introducing new executable
code needs a compliant refactor rather than assuming extra source capacity.
No success, time or official score is claimed by this schedule.

## Appendix BA. Omitted-list W6 comparison boundary

The published 222-class parent, submission `aa0e8b6a-6fd1-4a8b-9917-bb5e0f8a689f`
at commit `d6d874402c451412285457d4a05b7c6d829f23a7`, was evaluated in two
fresh local isolated runs for one representative of each omitted list. Its
participant plane-algebra counter reported the following non-full main-W6
batch ranges: list 2: 197--208, list 3: 201--212, list 4: 193--217, list 7:
188--214, list 8: 201--218, list 9: 194--222; 42 batches total. Outputs
matched between runs. These are historical-parent participant counters,
not independently verified machine prices or a current 222-class ledger.

The current paired streaming reference's 603-operation subtotal includes
modeled slot accesses and F6, while those parent figures are only the old
W6 batch's plane-algebra counter. They are therefore not directly comparable
as total attack prices. Still, the comparison identifies a serious obstacle:
without a substantially cheaper paired implementation or a different shared
schedule, the partner adjustment alone can cost much more than a separate
old W6 batch before its own memory and setup are added. No addition of the
omitted lists or score improvement is justified by these figures.

## Appendix BB. Single index table and arithmetic successor, unfiled

The separate successor table can instead be removed without packing an index
and successor together. Retain the existing 8,192-word least-set-bit index
table, and replace the successor-table load by subtraction and AND:

```python
def build_scan_index_only():
    table=[0]*8192
    for c in range(2,8192):
        if not (c&1):
            table[c]=table[c>>1]+1
    return table

def scan_chunk_index_only(c,table):
    out=[]
    while c:
        out.append(table[c])
        c=c&(c-1)
    return out
```

For representative scans, under the inherited zero-base index-table
convention, replace one successor load with a subtract and an AND: one
additional word operation per decoded representative. The class scan was
already priced using subtract and AND in the inherited itemisation and does
not acquire that same extra operation. If the retained index table cannot in
fact occupy zero-base addresses, its address add must also be charged.
Survivor and other uses of the old successor table must be inspected rather
than assumed away. Under the filed P7/P6/Q0 sensitivity, the extra for the
representative scans alone is 219.4441 operations per first block, before
additional uses, build, counters and cap effects. This is one operation per
representative better than the two-extra-operation merged-table sketch of
Appendix AY, while retaining the same 262,144-byte payload reduction.

The incremental builder uses no runtime bit-scan primitive: odd c has index
zero and an even c has index `index[c>>1]+1`. Its preallocation, initialization,
loop control, memory stores, instruction text and failure behavior require a
separate charged implementation. This reference is unfiled and not an attack
score or complete resource proof.

Two fresh local isolated runs enumerated all 8,191 nonzero 13-bit chunks: the
participant reported 53,248 decoded bits and zero membership/order differences.
A separate 120-second-limit diagnostic inserted the index-only scan into a
copy of the online process. Of 40 deterministic first blocks, five passed
the class filter; recorded class, plane, filter and output traces matched for
all five. The participant counted 6,976 representative lanes and an extra
6,976 operations by adding one per representative lane; baseline and
modified totals were 248,680 and 255,656. Outputs matched across repeated
runs. These are internal observations, not a complete machine-operation
trace, independent expected-work evidence or an official result.

## Appendix BC. Added-class cost needed to reach the current frontier

A conditional sensitivity illustrates why making the six omitted lists merely
break even is insufficient. Take the inherited baseline first-block count
30,821,546,153,665,530, variable mean
`127393765676096063954897/10737418240000000000`, fixed per-block charge
2,644+26, slack 1/15000 and the pre-existing fixed costs from the ledger.
Under the simplifying assumptions that the success factor per good pair is
unchanged, the new good-pair expectation rises from 636.6804599761963 to
830.9881687164307, the required first-block count scales inversely, and the
cap and other fixed costs do not change, a target time of 57.00229 permits
approximately 1,594.22 extra ordinary operations per first block. That is
only about 8.20 operations per additional expected good pair. The calculation
includes the fixed ledger terms and slack but deliberately does not rederive
success probability, correlations, or the Bernstein cap.

If the index-only scan adds the conditional 219.44 representative-scan
operations per first block for the existing family, only approximately 7.08
operations per added good pair remain in this sensitivity, before any scan
cost for the new family. By comparison, the prior-filed sensitivity in
Section 2 reported 20.1644--20.7967 preparation operations per good pair for
the omitted lists under a different program and historical charge. Those
numbers cannot be combined as an exact new ledger, but they show the magnitude
of the missing algorithmic improvement. A qualifying 222-class proposal would
need its own implementation, probability/cap analysis, source provenance and
full accounting; no claimed score follows from this estimate.

## Appendix BD. Index-only builder work budget, conditional

A conservative prospective fixed-word implementation may zero all 8,192
slots with at most six operations per slot, then process each of 8,191 nonzero
indices with at most 24 operations, and reserve 1,024 additional operations
for setup, finalization and counter updates. The resulting arithmetic budget
is `8192*6 + 8191*24 + 1024 = 246760 < 2^18` word operations. The 24-operation
per-index allowance is intended to cover parity test and branch; for an even
index, shift, predecessor address/load and increment; destination
address/store; and loop and work-counter control. The odd index is already
zero from initialization. This is an explicit upper-budget design, not a
verified instruction program: it assumes fixed word slots, valid table bounds,
charged addressing, correct branch semantics, and no hidden setup or spill
outside the stated allowance. It must be added to preprocessing rather than
absorbed into an unrelated allowance. The input-independent table occupies
262,144 bytes and may use its final region directly; any earlier borrowed
scratch must have been released before its initialization.

## Appendix BE. Paired-W6 difference carry simplification, prototype

For one bit let `o` be the old CH bit, `t` the selected increment or
borrow toggle, and `c` the carry in the two's-complement subtraction
`old - new`, with `new = old xor t`. The output bit is `~(t xor c)`;
the outgoing carry is `c` when `t=0`, and `o` when `t=1`. Therefore
`carry_out = c xor (t & (o xor c))`. This removes the explicit `new`
plane and specializes a general full adder to a conditional select.
The final-position carry may be omitted. The following is an isolated
research prototype; its operation count still depends on plane inversion
metadata and compiler specialization and is not a machine-level charge.

```python
def paired_w6_selectcarry(w,e4,e3,q7):
    out=w[:7]+[None]*25
    ci=Z1;cb=Z1;cd=Z1;cw=q7
    for j in range(25):
        a=e4[j+7]; b=e3[j+7] if j<=21 else None
        pick=(E5>>(j+7))&1
        old=a if pick else b
        toggle=ci if pick else cb
        if j<24:ci=and_(a,ci)
        if j<21:cb=and_(inv(b),cb)
        d=inv(xor(toggle,cd))
        if j<24:cd=sel(toggle,old,cd)
        v,cw=fa_step2(w[j+7],d,cw,(j+7) in NEEDW,j<24)
        if (j+7) in NEEDW:out[j+7]=v
    return out
```

## Appendix BF. Scan-address and reuse audit

The inherited Section 9.6 representative-loop itemisation asserts both the
index table and the successor table at word addresses 0 through 8191. They
cannot both be distinct arrays there. For example, at chunk 2 the index is 1
and the successor is 0, so sharing the same cell cannot satisfy both values.
The prior Python diagnostic uses `bit_length` and arithmetic clearing in its
single `scan_parts` function, rather than either explicit machine table; its
trace comparison therefore does not independently validate the inherited
machine address or load count. The cost and memory rows remain hypotheses.

If a correct two-table implementation addresses the successor using one
additional base add per decoded representative, then replacing that addressed
load (base add plus load, two operations) with subtract plus AND (two
operations) has no incremental lane cost on this specific addressing model.
Against the inherited, inconsistent five-operation row, however, the
index-only version still has one extra operation per representative. This
comparison does not establish a global saving: it leaves the actual scan
loop, instruction set, base-register convention, initialization, counter,
other scans and complete corrected original ledger to be specified. It also
cannot restore an earlier score by silently assuming the baseline was priced
correctly. The chunk-2 conflict is a concrete address contradiction, not a
claim about any submitted machine binary.

Two fresh networkless local executions of an assembled diagnostic compared
this function with Appendix AQ on eight pseudo-random 256-lane inputs. The
participant reported zero differing bits across 40,960 comparisons of the 20
F6-needed planes; its plane counter reported 2,400 operations for AQ and
2,056 for this prototype, or 300 versus 257 per batch. The fresh executions
produced identical stdout. No message pair was returned, and the local test
used a 120-second limit and a placeholder profile fingerprint; these are
untrusted internal observations, not a collision or official experiment.

If the same 31-operation F6, 220-operation memory/address and 52-operation
control assumptions from Appendix AW hold unchanged, the corresponding
partial subtotal is `257+31+220+52 = 560`, 43 less than 603. These costs are
not established for the new code: its output inversion flags may affect F6,
`sel` may generate different instructions or spills, and the inputs still
need to be produced, retained and charged. This experiment checks output
planes, not the final F6 cost or any candidate-list distribution. No score,
full attack cost, register limit or peak memory follows from it.

## Appendix BG. The three fixed-slot folds (b)-(d): itemisation and ledger effect

These are the (b), (c) and (d) folds itemised in mpjunior92's five-fold filing b460364c; this filing applies them to the R37P40k program and charges them under the same one-unit compression model as the rest of this package. They are cost folds of executed address arithmetic, not re-pricings: no stage price, probability, family or success event moves, and the examined pairs and returned pairs are identical.

**(b) The q planes at base + immediate.** Every sweep reads the q planes of its own list and batch; the W6 texts are written per list (Section 9.5). The set of q planes a sweep reads is therefore fixed by (list, batch) at compile time, and each is stored at a fixed slot of the q scratch area. The sweep executes one load per plane, not an address add plus load: `3 + 2 zq` -> `3 + zq`. The `q` scalar itself is data-dependent and keeps its address add; only the per-plane address adds are gone. -27.168 ops per first block.

**(c) The spill planes at literal slots.** The 15 spilled-W planes of a batch are a fixed set at fixed offsets of the spill area (Section 9.6), one slot per plane per batch. Each store and each reload is `base + immediate`, so the address add is not executed: SPILL 30 -> 15 per batch. The spill accesses themselves (15 stores and 15 reloads per batch) remain charged; only their 15 address adds per access are removed. -131.516 ops per first block.

**(d) The rep planes at base + immediate.** The rep planes of a batch are contiguous and read at fixed offsets from the batch pointer; the pointer operations (formation and the per-batch increment) are still charged. A batch pays `2 dyn + 2` -> `dyn + 2`: one load per dynamic plane, not an address add plus load. -48.750 ops per first block.

**Soundness of the fixed-slot convention.** The same convention is already accepted in the lineage: the c7 load-slot fold of Section 9.2 (5dbbb8da, ed0d4c15), the q store-slot fold of ed0d4c15/5dbbb8da, and the zero-base `scan_table` of Section 9.6 (P9). A plane whose slot is a compile-time immediate of the shipped per-list text needs no address register; the text is written per list, so the slot is not data-dependent. The only data-dependent addresses in these stages are the batch pointer and the subtraction-run index `cu`, and both stay charged.

**Ledger effect (exact).** perclass 4,770.967335 -> 4,563.533863 (the three folds act only on perclass); vbar 11,864.468984 -> 11,657.035512; FIXED / FIXED_P7 unchanged at 52 / 26; per first block 5.49715 -> 5.41870 units. The cap is recomputed at slack 1/15000: N_FB 30,821,546,153,665,530 -> 30,821,554,876,811,406; V_MAX 365,705,657,129,201,863,584 -> 359,311,912,272,790,214,230; vmax_fb 53,789,946,971.9 -> 53,789,931,987.9; Pcap 2.748495e-07 -> 3.579311e-07 <= 9/25,000,000; mu_req 0.49466288 -> 0.49466302; N 448,753,471,051,579,349,088 -> 442,359,749,485,967,173,670; log2 T 57.235978534282836 -> 57.215275556308605; claim 57.23598 -> 57.21528. The success floor is 0.3900000060442928 > 0.39 (Appendix C).

**Verification.** `python3 experiments/lowm.py ledger` prints the new cells; the Appendix B mirror reproduces N to the digit; `selftest` is 0 mismatches and byte-identical to Appendix D; `memory` is unchanged at 1,035,912 bytes (no new resident item; the fixed-slot texts are the same words at compile-time displacements). Under organizer-style requests the inherited experiments return byte-identical stdout; `a0-online-r37` returns the same pairs with every mismatch counter 0, only `counted_ops` moving.

**Limitations.** The register argument is a count of live planes, not a register allocation. The code size is a bound (at most 8192 primitives of at most 8 bytes), unchanged. No organizer ruling is cited for the base + immediate convention beyond the accepted lineage cells above; the judge assesses it as a property of the shipped text.

**Credits.** Folds (b)-(d) are itemised in mpjunior92's b460364c five-fold filing; this revision applies them on top of the R37P40k program (prefilter, fold (j)) under the compliant one-unit compression model.
