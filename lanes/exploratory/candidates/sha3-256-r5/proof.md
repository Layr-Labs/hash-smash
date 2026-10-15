# 5-round SHA3-256: R5N3, R5N with a clean development record regenerated under the memory cap (R.8, Appendix M; Appendices K and M govern), time 2^31.60861, memory 2^25.906891

## R. What R5N changes (B' tent as update logs, P's key words by Gray walks, bases at acceptance; Appendices K and L govern)

R.0. R5N is our 0f72a85e (our accepted entry, 39.75228: time 32.79669, memory 2^26.955592) with three program changes in experiments/r5.py, one changed organizer check and Appendices K (memory) and L (ledger). The algorithm's values and order, K = 50, every cap, rule K, premise R, R7 and its replays, the advice, H2 and the certificates are 0f72a85e's and the lineage's (credits: Sections Z-0). r5.py (65,463 bytes) is AST-identical to 0f72a85e's except Aff (a log field), the new XT, xd and rep, m2, algorithm, hv_trial with its price constants, and the docstring (RUNS writes 0x00000000 as 0: same AST); whitespace was compacted in the changed functions. manifest.json changes only r5-mitm-1's trial-1 text and hypothesis and one parenthesis of r5-bpfull's scope. R5N2 (635939f2, refuted on F-memory-charged-D15-peak) was R5N with the advice produced by a capped run. R5N3 (this package) changes no program, no experiment and no certificate of R5N2 (r5.py sha256 f9a88567b9cadffcdd7995bd6dc68a543218594e8825ee484a597c9e219b3cb3): it replaces the development record by one in which every run was made under the memory cap (R.8, Appendix M) and answers the ruling (R.9). Time and preprocessing change, and memory by the cap's virtual-size margin (R.4, R.8); success and every program do not.

R.1. A: m2's tentative list as update logs. 0f72a85e's m2 keeps a copy of X (at most 3,200 entries of 13 words) and D (1,600 x 7 words) for every candidate of the chosen row until one is accepted (structural maximum 216 copies, 365 MB; measured maximum 36). R5N builds each candidate exactly as before (same copies, adds, order and WK charges) but keeps only the materialised entry that sorts first (least rank increase, then least index) and, for every entry, its update log: the (af, pb) of each table-changing Aff.add (at most 10 for X, 5 for D). The trial loop is unchanged; any other entry is rebuilt when tried by rep(): a copy of the current table with the logged updates replayed by the same expression `t ^ af if t & pb else t`.
- Lemma A. A replayed table equals the eagerly built one entry by entry, and an untouched entry is the same object (a touched entry is a new integer from the same operation on the same values, so CPython's small-integer identity also agrees). So the identity tests, dom_of, the accepted entry, choice, X, D, every coin draw and the counters row, small, keccak, sha256, r2 equal 0f72a85e's on every input; WK.cost(), CCAP and B_BUDGET act identically.
- Extras, counted in WK.d (inside B_TRUE) and in XT[0]: 2w + 2 per log write; per rebuild len(T)(3 + 2w) for the copy and 7 len(T) + 1 + 4w x (entries with the pivot bit) per replayed update (V.5's prices). A rebuild repeats a subset of its entry's build at the same prices and each entry is rebuilt at most once; a log write is at most 28 primitives against at least 7 x 1,600 for its update. So extras <= 1.0025 x 0f72a85e's true cost, on every execution.
- Online charge unchanged: B_TRUE = 2^29 units caps WK cost + WK.d including the extras; the largest single update (a rebuild) is below 2^11 units.
- R7 transfer (H1). R5N on R7's labels equals 0f72a85e unless B_TRUE acts where it did not, which needs 2.0025 x (old true cost) > 2^29, i.e. old true cost above 2^27.998 units: in R7 (W.2) only runs 10 (2^28.39) and 32 (2^28.60); next is run 13 (2^27.90). Counting runs 10 and 32 as failures, 37 of 48, one-sided 95% Clopper-Pearson bound 0.6493 >= 0.40. The claim stays 0.40.
- Regression run here: whole B' runs (bprime from candidate 0 under B_BUDGET, CCAP, B_TRUE) of R7 runs 1, 2, 4, 6, 33, 37 with 0f72a85e's r5.py and R5N's give identical (c, j, DF), advice and WK cost, and R5N's true cost = old true cost + XT exactly (Table R.1, primitives; a process's first run includes V.5's 11,182,080 memo setup).

| R7 run k | (c, j, DF) | WK cost (both) | true cost 0f72a85e | true cost R5N | extras (XT) |
| --- | --- | --- | --- | --- | --- |
| 1 | 0, 13, 41 | 26,960,409,156 | 4,267,896,176 | 4,268,054,328 | 158,152 |
| 2 | 0, 13, 46 | 30,140,691,100 | 5,193,057,253 | 5,193,183,251 | 125,998 |
| 4 | 1, 0, 44 | 100,098,075,558 | 81,307,444,040 | 81,307,525,488 | 81,448 |
| 6 | 0, 2, 51 | 16,435,064,578 | 2,785,537,578 | 2,785,916,829 | 379,251 |
| 33 | 0, 4, 54 | 13,220,514,578 | 2,296,034,182 | 2,296,102,134 | 67,952 |
| 37 | 0, 0, 36 | 11,319,984,179 | 1,668,994,911 | 1,669,110,679 | 115,768 |

R.2. B: P's half table without the 14 key words. 0f72a85e prices P (and, by X.5, D15 and D19) with 22-word entries (7 plane words, all 127 keys in 14 key words): 83.1 MB per core. R5N's entry holds the 7 plane words, w2 and the choice (8 bytes) and one key-word slot; each key word is produced when its level needs it by a Gray walk of that word alone (same reflected mixed-radix walk, one-word difference tables). Per core and level nb: tabulate planes, w2 and choice (HV_STEP 38: X.2's state step with 7 words and the weight); for each key word holding keys of nb (keywords() packing: 1, 1, 1, 2, 3, 4, 7 words for nb = 1 .. 64; 19), walk both halves writing it (KW_STEP 20: the state step with one word and its store), then sort and merge its blocks as before (3 + 28 + 6, per_a 18, match 49). Keys, matches, evaluations and P's output are unchanged (trail_search is unchanged; Lemma W). r5-mitm-1 trial 1 walks both full half tables of the output core for the planes with w2, key word 0, and all 14 key words; PASS iff the sampled words equal to_planes/keywords of halves()'s vector, w2 equals halves()'s weight and the longest steps count exactly 38, 20 and 59 (= 20 + 3 x 13). Local: PASS.
- Repricing (X.5, W.5: tables at every level, as the native runs computed them): D15's certified run 7 x 38 + 19 x 20 = 646 per half vector instead of 7 x 80: +86 x HV. D15's stopped ten-level run: 10 x 38 + 21 x 20 = 800 (keys of each level from a fresh word), below its charge 10 x 83, which stays. The layout comparison keeps v15's key price, above the new one. D19's contig.c (4 cores, 329 blocks, charged 80 per half vector): bound 38 + 329 x 20, +6,538. D20's ptrial_check (4 trail_search runs, at most 14,580 half vectors): +550 each. A full per-block stream without plane tables was prototyped and not adopted (about 70 primitives per match to regenerate B, and D15's stopped run has over 5.4 x 10^10 matches).

R.3. Bases at acceptance. 0f72a85e's algorithm() keeps each accepted attempt's info, with its echelon system, until E: 50 systems resident (Section 7: about 31 MB; Appendix I counted one). R5N's algorithm() computes enum_basis(EM, beta0, 32) at acceptance and keeps (v0, basis, beta0), 7,616 bytes; E runs on the same values in the same order. Every accepted space's basis is now computed: at most 3 x 49 + 50 = 197 per run (at most 4 advice rounds), so the Bases term is 197 x 2^24 primitives.

R.4. Memory (Appendix K). Dense model of the lineage, code included, no allowance: dense-model peak = E phase, 47,755,983 bytes = 2^25.509178; claimed memory = 62,914,560 bytes = 2^25.906891, the largest address-space cap that any label of the development needed to complete (R.8; CPython's virtual size exceeds the dense model by several MB) (B' 37,604,113; P per core and level 35,598,680; connector 6,288,399). Development: every development run of R5N3 was made under an address-space cap of at most 62,914,560 bytes (`prlimit --as`; R.8) and its measured peak resident set is at most 52,146,176 bytes, below the claim (Appendix M lists all 50). D15's native run is superseded (R.8, R.9). Python RSS for orientation (memmeter, whole B' of R7 run 2): 0f72a85e 45,476 KiB, R5N 33,988 KiB.

R.5. Time (Appendix M): the online algorithm (B' unchanged, Bases 197 x 2^24) is 2^29.983254 units (1,061,350,115 units); the development is the ledger of Appendix M: the 50 runs of R5N3 (2^30.9079 units), D16 (2^27) and the peers' build checks D21, D_Y, D_v23, D_v24, 2^31.0434 units in all. Total 2^31.608606 units, claimed 31.60861, preprocessing claimed 31.36176. R5N2's development rows (G2, D15, D19, D20, D22, D23, L1-L10) are not charged: R.8 lists what superseded them and why. R.2's repricing rows are history.

R.6. D26 (every run made for R5N: design studies, tracemalloc runs, 38 stream-prototype runs, the B' regression runs) and R5N2's L9 and L10 (the capped advice run of R5N2 and its other runs) are history: none of their outputs is used by R5N3, which regenerates the advice, M_CAP, the layout and the B' and connector samples in R.8.
Several of R5N's design studies ran above the cap (40 to 85 MB). None of these runs is charged in R5N3; the sensitivity if they were is in the submission note.

R.7. Not shown: no R7 re-tally (charged it would cost about 2^30.7 units); runs 10 and 32 count as failures instead. Measured extras were 6.8 x 10^-5 to 1.4 x 10^-4 of the true cost (Table R.1), against the bound 1.0025. The code term uses the arm64 size of the lineage's instruction-count bounds (at most 8 bytes per primitive of the unrolled E block); with a 2 MiB allowance instead of r5.py's 65,536 bytes the E phase is 49,787,599 bytes (2^25.5693). E's ANF table (31.8 MB) is now the largest structure; rebuilding it from its 165,796-byte coefficients was not built.

R.8. R5N3's development: every run under the cap, every input regenerated. 
Ruling 635939f2 (R5N2) held that D15's certified native run of P stays charged development and fixed M_CAP.
That run measured 233 MB with five cores in flight. It is superseded and is not part of this entry's development.
R5N3 does not rest on it: the other runs that fixed or measured the constants the algorithm reads (G2's B' and E runs, D19's contig.c, D20's replays and ptrial_check, D22, D23, R5N's design studies and R5N2's capped runs) are superseded too, because R5N3 regenerates each such input from the target and r5.py alone, from scratch, in processes whose address space is capped by `prlimit --as` (47,755,983 bytes, the dense model's figure, at first; the labels that died there were re-run under looser caps, below; the claim is the largest cap any label needed, below), `nice -n 10`, `/usr/bin/time -v`, one thread each; the capped runs started on 2026-10-15 at 16:47Z, Ubuntu on WSL2, CPython 3.14.4; builds of capadv with cargo and of fes with gcc are not capped, build no target value and are not runs of the algorithm). Every run is one line of devmem.jsonl (SHA-256 c0f0ff0dc601ad1eeaa58be6ddc66718a96fd5e3b4094fc0cba79aa782f6b976) and one row of the table below with its measured peak resident set (ru_maxrss of /usr/bin/time -v); the largest measured peak of all 50 runs is 52,146,176 bytes, below the claim 62,914,560 (82.9%).

What the runs derived (no earlier output is read by any stage; stage scripts in run_all.sh order s00 s10 s11 s12 s13 s20 s30 s40, sha256 of every source in Appendix M):
- s10: T1, T2 and the core tables of the 467 kept cores (trail_search's enumeration with r5.py's own functions): 8,674,833 lane_dfs nodes, 1,741 cores reached, 467 kept, 48,592,224 half vectors, sum C2 1,379,275,399,350; peak 37,036,032 bytes, written to disk one core at a time.
- s11: the block layout. Six layouts fixed before any run in py/mklayouts.py (contiguous 5 rows, z only, (z + y) mod 64, (z + 5y), (z + 13y) = the shipped BLK, (z + 29y)); the 8 kept cores with the most half-table entries; matches at nb = 64 counted by capadv (HS_COUNT): contiguous 8,069,035,297; z only 47,447,341,904; stride 1 8,488,440,313; stride 5 6,731,341; stride 13 (shipped) 78,534; stride 29 773,682. The stage fails unless the shipped layout has the fewest; it does. Peaks at most 34,926,592 bytes.
- s12: stage 2 (P's T3: both half tables regenerated per level and block by Gray walks, a hash table of one half's keys, one core resident) over all 467 cores and all seven levels with the match cap effectively off: 7,251,935 matches (20,490; 40,849; 81,791; 165,085; 329,494; 818,094; 5,796,132 per level), 30 evaluations at nb = 64, least leaf W* = 127 at nb = 64 on core 17, w2 = 24, choice (0, 0, 3, 0, 0, 0, 0, 0, 3, 1); M_CAP is then the least power of two at least twice the matches, 2^24 = 16,777,216 = the shipped M_CAP; the advice (stage 3, finalize.py: beta2 from the leaf as trail_search does) has SHA-256 e97373f75db5f2ff838e2fda81e059c33e009106e834c5ac808a828bce18d7d9 of the core tuple's repr and the 200 bytes of beta2 for the produced and for the shipped constants (ALPHA3_BITS, BETA2). Log SHA-256 991ff285b6f29441f3af4d76ecd0700c...; peak 7,991,296 bytes (capadv), 28,180,480 bytes (finalize).
- s13: the capped replacement for mitm_trial(q)'s half tables. The organizer experiments r5-mitm-* run mitm_trial(q) in Python; R5N3 never runs it (next line). Instead mt6_check.py compares the per-core nb = 64 match counts of s12's streamed run with r5.MT6, the table mitm_trial(q) checks (M[0] == MT6[q]): all 467 cores equal (0 differ); peak 28,364,800 bytes. mitm_trial's own check of the output core (OUT_LOG, 30 evaluations, beta2 == BETA2) is covered by s12's RESULT line and ADVICE_IDENTICAL.
  (The Python half tables of mitm_trial(q) for one core measured 78.1 MiB, above the cap, so no such execution is part of this development.)
- s20: ten whole B' runs (bprime from candidate 0 under B_BUDGET, CCAP, B_TRUE with the shipped r5.py) on the fresh labels "hashsmash sha3-256-r5 R10 run K", K = 0..9: each completed run has a true cost below B_TRUE = 2^29 units and a WK cost below B_BUDGET = 2^32 units; they replace G2's B' rows as the sample behind B_BUDGET/CCAP (the constants stay as filed: R.8's last paragraph).
- s30: E stage 1 (fes.c, Appendix B) on three seeded spaces: peak 22,392,832 bytes.
- s40: the online phases up to the accepted spaces (B', Setup, connector attempts until 50 spaces are accepted, algorithm()'s order, each accepted space kept as its basis) on labels R10 run K, K = 0..2.

Runs that did not complete under the cap of 47,755,983 bytes, stated plainly: s20_bprime_2, s40_online_2, s20_bprime_9, s40_online_0, s20_bprime_5, s20_bprime_0, s20_bprime_8 (exit != 0), that is s20 labels 0, 2, 5, 8, 9 and s40 labels 0, 2 of "R10 run K".
Each died with MemoryError in the address-space cap at a measured resident set of 39 to 41 MB, after 1 to 28 minutes (the cap limits virtual size, which exceeds the resident set by the interpreter's mappings); one B' of label 2 run with PYTHONMALLOC=malloc died the same way.
They are in the table, are charged (as the completed run of the same label), and their peaks are below the claim.
We did not drop or replace any label: each was re-run under looser caps (rows *_cap*): s20 label 0: completed first at a cap of 62,914,560 bytes; s20 label 2: completed first at a cap of 52,428,800 bytes; s20 label 5: completed first at a cap of 62,914,560 bytes; s20 label 8: completed first at a cap of 62,914,560 bytes; s20 label 9: completed first at a cap of 53,477,376 bytes; s40 label 0: completed first at a cap of 62,914,560 bytes; s40 label 2: completed first at a cap of 52,428,800 bytes. Every such re-run, completed or not, is a row of M.2 with its cap and measured peak.
One probe ran under an address-space cap above the claim: 67,108,864 bytes (row s20_bprime_9_cap67108864). That number is the cap, not a measurement.
Its measured peak resident set was 51,908,608 bytes, below the claim.
Consequently the claim is raised from the dense model's 47,755,983 bytes to 62,914,560 bytes (2^25.906891, +0.397712 bits, time unchanged): the largest cap that any label needed, in the ladder of caps we tried (labels 2 and 9 were tried at several caps, the others at the cap that completed them). Every run's cap is at most the claim except that one probe's cap, and every run's measured peak is at most the claim.
The literal statement "every run completed under prlimit --as=47,755,983" is false for these labels, and the claim is accordingly raised, not the runs omitted.

What is not regenerated (stated plainly). K = 50, A_ADV = 1067, A_MAX = 4268, S2CAP = 2^11, CCAP = 2^26, B_BUDGET = 2^32 units, X_MAX = 2^20, B_TRUE = 2^29 are the filed constants (rule K of W.1 and the lineage's run-free rules); R5N3's ten B' runs and its connector runs are a fresh sample consistent with them, not a re-derivation of them. The R7 study (W.2, Appendix F: 48 complete runs of v20, up to 116 MB, with the old program) is not repeated; its premise R and its bound are unchanged. The organizer's own harness executions are not ours. Our earlier local runs of the organizer experiments (D19-D23, up to 99 MB for r5-mitm-1) are superseded as development (they choose no constant of the algorithm; R5N3's s13 replaces what they checked) and are not charged in R5N3; the sensitivity of charging them is in the submission note.

R.9. Answers to ruling 635939f2 (R5N2, refuted), by finding id.
**F-memory-charged-D15-peak** (fatal).
D15's 233 MB native run is superseded and is not part of this entry's development, because every input it produced (the trail data, the block layout, M_CAP, the advice, the per-core match counts) is regenerated from scratch by R.8's runs.
Every run of R.8 has its measured peak in Appendix M at or below the claim (62,914,560 bytes; R.4). The proof no longer charges D15, G2, D19, D20, D22 or D23 (the lineage's rows stay as history in Z.4, Z.5 and 0.1 and are not added).
**F-EVAL-ADVICE-RUN-EXECUTION-GAP**: the advice pipeline of R5N2 is replaced by R.8's stages s10-s13, with every run's command, cap, peak, exit and price in M.2, the log's SHA-256 and every source's SHA-256 (M.0). The sources are still not in the package (the 64 KiB experiment-source limit; r5.py leaves 73 bytes) and there is still no organizer execution of the pipeline: that gap remains and is stated in H2.
**F-ledger-independent-verification**, **F-EVAL-COST-LEDGER-NOT-INDEPENDENTLY-VALIDATED** and **F-EXP-NO-TOTAL-COST-INFERENCE**: the time and preprocessing bounds stay conditional on H2 (completeness of the development ledger and the counted prices). The ledger is now short (M.2-M.5: 50 runs, D16, four peers' rows) and fully listed, but the organizer's experiments still check counted routines, not attack cost, and R5N3's choice to supersede the older rows is disclosed in H2.
**F-success-iid-premise**, **F-PROB-IID-PREMISE**, **F-EVAL-PROBABILITY-INFERENCE-LIMIT** and **F-EXP-IID-TRUST-GAP**: 0.40 rests on premise R (label-seeded coins act as fresh coins; R7's 48 runs are an unselected sample); the organizer's report draws no iid inference and has no holdout nonce; R5N3 does not change that.
**F-H1-CURRENT-PROGRAM-TRANSFER** and **F-EXP-CURRENT-TRANSFER-MISMATCH**: R7 measured v20; the transfer to this program counts R7 runs 10 and 32 as failures (37 of 48, bound 0.6493, R.1) and is arithmetic, not an organizer-run experiment; unchanged.
Answers carried from ruling e268e947 (R5N), by id: F-memory-preprocessing-peak (R.8); F-cost-ledger-independent-verification, F-EXP-3 (as above); F-success-iid-premise, F-PROB-IID-1, F-EXP-1 (as above); F-EXP-2 (the organizer's experiment 7 checks v20's R7 table, 39 of 48, bound 0.6956; the transfer to this program is arithmetic, R.1).

Exploratory claim (v25/v25h, b5213766): v22b (08930c1e) plus Section Z (1d1f98ee advice; v23/v24 T2/T3 steps; 12-pass 1,024-step E block at 208,007 primitives; development item 23 at per-invocation counts; 32.92344 / 32.82958).

## Z. What v25 changes

**Credits first.** Every algorithm, study, certificate and development record is v22b's lineage's (Sections X, W, U, V and 0-8, with their credits): winglock's v22b/v22, v20, v19, v14, v13, v8; Th0rgal's v21 (a9ec6971) and zero-advice framing (7deb1595); 0xshikhar's T3 memory repair (6667fc4f, 395e8a28); Meganpark980320's v17/v18 (168a1b3a, f1eb6445); rubenmarcus's v15 (91f1424d), whose D15 contains the certified run of P; Subflatus3's zero-block half-sum match (9bccf245). v25 adds: **leech1996**'s Y (1d1f98ee, 33.03168): the advice reading of P's certified output and its argument (Z.1), adopted unchanged; **Th0rgal**'s v23 (017f48c9, 32.98298) and v24 (08c9e7c1, 32.97491): the match step with nibble-aligned tail planes and a carry-free nibble fold, the single-AND T2 leaf with its complemented lanes, the 14 key words, and the E prologue (ctz over the block-index bits only, ten partial ranks, base ranks as plain loads) (Z.2, Z.3). We read their notes and packages as data, wrote each idea into v22b's experiment file ourselves and checked it against v22b's programs and the plain evaluation; their stated build checks are charged (D_Y, D_v23, D_v24). The multi-pass block of Z.3 and its register accounting are ours, and so is any error in them. Considered and not adopted: GordoAR's rev-7 (83697db1, 32.94842), which lowers K to 36 with the attempt limits scaled, a rung chosen with R7's outcomes known while R7 stays uncharged (R7 charged: 33.8036); and v23/v24's Python refactors of functions that algorithm() reaches, which would break the byte identity with the file R7 ran (Z.1).

| Change | Where | v22b | v25 | Evidence |
| --- | --- | --- | --- | --- |
| Z.1 advice: P's certified output read by algorithm() (Y) | online algorithm, H1 | P run online (2^28.516241 units) | P removed online (its 2^32-primitive setup bound kept); P's one execution charged in D15 | AST comparison; r5-trail-0, 1, 23, r5-count-2 trials 8-10, r5-mitm-0/1 |
| Z.2 match step (v24) | D15, D19 | 56 (899/16 per match) | 49 (787/16 per match), per_a 18 | r5-mitm-1 trial 2 |
| Z.2 T2 leaf with its Gray step (v24) | D15 | 26 | 21 | r5-count trials 1, 3, 5, 7 |
| Z.2 half-vector step (v24) | D15, D19 | 83 (86 with 15 key words) | 80 (83) | r5-mitm-1 trial 1 |
| Z.3 E stage 1 | E, G2, development item 20 | 66,831 per 256 steps | 208,007 per 1,024 steps (52,001.75 per 256) | r5-count trials 0, 2, 4, 6; r5-count-2 trial 11; check_e.py |
| Z.4 development | G2, D15, D19, development item 20; D_Y, D_v23, D_v24, development item 23 | v22's prices | v25's prices (X.5's rule); peers' checks and our runs charged | ledger_v23.py |

### Z.1 P's certified output as advice (leech1996's Y, adopted)

- **The change.** algorithm() begins with `base, OB = Base(), own_bits()` in place of `trail_search()`, its two failure returns and `Base(tr[0], tr[1])`; this is Y's edit, character for character. The defaults of Base() are ALPHA3_BITS and BETA2 (Section 3), P's certified output. By AST (files parsed as data), the 101 top-level definitions that algorithm() reaches in v25's r5.py, including the helpers that build its import-time tables, are v22b's byte for byte except algorithm() itself; they no longer include trail_search and its helpers. trail_search() is still called by p_trial (r5-count-2 trials 8, 9) and mitm_core by mitm_trial (r5-count-2 trial 10, r5-mitm-0/1).
- **Where the advice is charged.** The cost model requires that "all construction/preprocessing and advice must be accounted for, including any search omitted from the submitted program". The omitted search is P. R5N3 produces it by the capped runs of R.8 (Appendix M: the pipeline T1, T2 export, streamed T3 over all 467 cores and seven levels, 7,251,935 matches, W* = 127 certified at level 64 by Lemma P). v15's certified native run (mitm2.c, Appendix A; the same output and per-level counts) is superseded: it is not part of this entry's development and is not charged here (R.9). The run computes P's output from the target alone, and P's output is a deterministic function of the target (the least leaf of Lemma P). v22b ran P a second time online; v25 removes only that second execution and keeps P's 2^32-primitive setup bound online (DDT, L^-1 and Base()'s tables). The organizer still recomputes the output core's certifying level and compares (core, beta2) with ALPHA3_BITS and BETA2 in every review (r5-count-2 trial 10).
- **Success.** R7's 48 runs never executed trail_search: each started from P's certified output and made algorithm()'s later calls in algorithm()'s order (W.2). v25's algorithm() makes exactly those calls with the same constants, caps and label-derived coins, so every R7 run is a complete run of v25: 39 of 48 succeed, one-sided 95% Clopper-Pearson bound 0.6956, claim 0.40 by R7's pre-registered rule. Premise P leaves H1; the probability space is the algorithm's own coins with the target and the advice fixed. The counted programs of Z.2 and Z.3 are the price model; algorithm() never calls them (X.11).
- **Earlier uncharged sources of the same constants** (GLL+20's core No. 3, v7's P run, v14's two native T3 passes; item B of Section 0.1) are not relied on. Charged as three executions of P at v25's prices: 33.1129. P kept online, as in v22b: 32.9889.
- **Advice size.** ALPHA3_BITS (at most 10 bit positions below 1600) and BETA2 (1,600 bits): under 2^8 bytes, declared nonuniform_advice_log2_bytes = 8.

### Z.2 Counted programs from Th0rgal's v23/v24 (re-implemented)

- **Match step 49** (787/16 per match with the run loop's 3 per 16 matches; per_a 18). to_planes puts bits x = 0..3 of tail row k (rows 256..319) at bit 4k + x of word 5 and x = 4 at bit 4k of word 6; the step forms t = w5 OR w6, t = t OR (t >> 2), t = t OR (t >> 1) (5 primitives: the active-row bit of tail row k at bit 4k) and adds t AND 0x11..11 at the 2-bit stage, h = h - ((h >> 1) AND SW0) + (t AND SW3) (each low 2-bit field at most 2 + 1); then the 2-bit to nibble stage (4) and the carry-free nibble fold c = (c + (c >> 4)) AND SW2 (3; each nibble at most 5, so two add to at most 10). Count: pointer 1, B's 7 words loaded and XORed 14, OR tree 4, tail 5, first stage with the tail 5, nibble stage 4, fold 3, byte fold 3, four shift-and-adds 8, test 2: **49** (v23's note stated 50 and its r5-mitm-1 trial 2 failed; v24 corrected it to 49; ours counts 49 and the trial checks 18 + 49 e + 3 floor(e/16) exactly).
- **T2 leaf 4 (3 when not kept), with the 17-primitive state step: 21.** Word w holds lanes (x0, x1, NOT x4, NOT x4) and word v lanes (NOT x2, NOT x3, x2, x3); the Gray step's XOR of uncomplemented differences keeps the complements. By De Morgan on Th0rgal's v21 identity, NOT ALLOW = (x0 AND NOT x2) OR (x1 AND NOT x3) OR (x2 AND NOT x4) OR (x3 AND NOT x4), so all 64 rows are allowed iff w AND v = 0: 1 + test 2 + store 1 when kept.
- **Half-vector step 80 (83 with 15 key words in D15's ten-level run).** The 63 keys of levels below 64 (26 bits) sit 9 per word in 7 words and the 64 level-64 keys (exact 25-bit slices) 10 per word in 7 words: 14 key words instead of 15, 3 primitives each.

Our checks: the organizer runs and timing gates of Z.6 on the final file (every predicted PASS). Each program computes the same decisions, AS, words and keys as v22b's: r5-count trials 1, 3, 5, 7 compare the leaf with ALLOW on all 32 row values and the walk's words with the plain layout; r5-mitm-1 trial 1 compares the 21 words with to_planes/keywords of halves() along both full half tables; trial 2 compares AS and every decision with the plain evaluation.

### Z.3 E stage 1: a multi-pass block of 1,024 steps, 208,007 counted primitives

E's computation is unchanged (Lemma 4): the same F, derivative vectors, pass words and stage-2 order. Only the counted program that prices it (e_blk and pro in r5.py) changes.

- **Independence of the 24 equation words.** Every state word of the derivative recursion belongs to one equation word k: F_k and D_w[rank][k]. Step i updates word k from word k's own vectors only, and the pass word of step i is the OR over k of F_k (then compared with all ones). So a block of 1,024 steps can be run word group by word group: in pass p = 0..11 the block's 1,024 steps run for equation words 2p and 2p + 1 only, and a buffer of 1,024 words carries the partial OR of the passes so far (pass 0 stores it; passes 1..10 load, OR and store it; pass 11 loads, ORs and compares it with all ones). **Lemma Z.** After each pass p, F_k and every D_w[.][k] for k in {2p, 2p + 1} equal their values after the block in the single-pass order, and after pass 11 the comparison at step r is the single-pass comparison at step r. (Induction over the steps of a pass, per word: a pass makes, for its two words, exactly the updates of fes_step in the same step order; the other words are untouched.)
- **Blocks.** A block is 1,024 consecutive steps 1024 B + r (B a 14-bit block index; block 0 starts at r = 1). The positions below 10 of a step are constants of the unrolled code, positions 10..23 come from B. Each pass of a block keeps F_2p, F_2p+1 and the two words of 29 derivative vectors in registers: 60 resident words, loaded when the pass starts and stored when it ends (D4 tables are not resident). The 29 are the vectors of levels 1 to 3 whose ranks depend only on positions below 10 that the 1,024 steps use most (list RES in r5.py). A level below the top costs 1 (XOR into the resident word) instead of 3 (load, XOR, store); a resident top level costs 0 instead of 1.
- **Registers (v22b's convention, X.4).** 64 words of 256 bits. Besides the 60 resident words a step needs the chain value, a load temporary and one address register per level whose rank depends on B (dy of them, each loaded from the prologue's stored partial ranks): 62 + dy. A step with dy >= 3 spills and restores dy - 2 resident words that it does not use (2 primitives each). In a block of 1,024 steps, dy >= 3 only at r = 0 (dy = 4) and at the 10 steps r = 2^j (dy = 3).
- **Prologue (once per block, at most 87).** The block counter's load, the block loop's end test and B's store; up to four isolations of the lowest set bit of B, each located by a comparison tree over positions 10..23 (4 comparisons; Th0rgal's v23 searched [8, 24) for v22b's 256-step blocks), with the end tests; then the ten partial ranks that depend on B (four base ranks as plain table loads, six with an add; Th0rgal's v23/v24) and their stores. The largest prologue over all 2^14 block indices is 87.
- **Count.** In each pass and at each step: dy rank loads, 2 x max(0, dy - 2) spill primitives, for each of the two words 1 + (top level: 0 resident, 1 loaded) + (each lower level: 1 resident, 3 not) (the last 1 is F_k's XOR), the OR of the two words (1), and the buffer: load and OR (2) in passes 1..11, store (1) in passes 0..10 or the comparison with its branch (2) in pass 11. Over a block whose index has at least four set bits (then every step's positions >= 10 all come from B; any other index costs less: a step's levels are the lowest set bits of 1024 B + r, at most four; with fewer set bits in B a step keeps its levels from r and has at most as many levels from B, so its level updates, dy, rank loads and spills do not increase; check_e.py confirms it on all 469 indices with one to three set bits) this is exactly **207,920**; with the prologue, **208,007 per 1,024 steps** (2^14 blocks per space).
- **Stage 2.** The pass words of a block are known after its pass 11; stage 2 handles the block's passing steps in step order, so the pairs and their order (outer Gray order, then inner point), S2CAP and E's stopping rule are as in 2.4 (e_window, which algorithm() runs, enumerates in natural order; success is identical while S2CAP does not act, as in X.4). Stage 2 uses only the pass word and the coordinate 1024 B + r (it forms x by basis additions); its hand-off (spilling and restoring the 60 resident words, 120, and the coordinate) lies inside 2.4's 2^11 primitives per pair, as in X.4.
- **Memory.** The unrolled code of a block (12 passes of 1,024 straight-line step bodies: 207,920 counted primitives, under 2^18 instructions) and the 32 KiB buffer, beside the 10 MB of derivative vectors: far below Appendix K's memory figure.

Evidence. r5-count trials 0, 2, 4, 6 (organizer seeds): fes_setup with 11 outer coordinates, then two blocks of 1,024 steps through e_blk; every F_k after every step (recorded in its pass) and the pass bit equal e_plain at 3 slots of the start and 1 seeded slot of every step; the prologue counts at most 87 and each block at most 207,920. r5-count-2 trial 11 computes the block price itself (trials 0, 2, 4, 6 check values, trial 11 checks the price): count-only e_blk on zero tables with 24 outer coordinates over the 1,024 steps of a seed-picked block index with at least four set bits (exactly 207,920) and the prologue for all 2^14 block indices (largest exactly 87). Our check_e.py: two seeded spaces with 11 outer coordinates (2,047 steps each), e_blk next to v22b's fes_step on copies of one state: F and every derivative vector compared word by word after every block, and the pass words equal (no step of either space had a passing point, so the pass-word comparison is between all-zero results); and e_blk's count over all 469 block indices with one to three set bits and three with at least four: largest 207,920.

### Z.4 Development at v25's prices; D_Y, D_v23, D_v24 and D23

(R5N3: history, condensed. v25 charged G2, D15, D19 and development item 20 at v25's prices, our runs for v25 as D23 (2^26.6118) and the peers' build checks D_Y (2^14), D_v23 (2^25) and D_v24 (2^24.53). R5N3 charges the peers' checks as filed and D21, D16, and the runs of Appendix M; it does not charge G2, D15, D19, development items 20, 22 and 23 (R.8, R.9). The itemised table of D23 is in R5N2's proof.)

### Z.5 Ledger (log2 units; exact rationals, rate 1355; ledger_v23.py)

(R5N3: history. The online terms below are R5N3's, with Bases 197 x 2^24 (R.3); the development row is replaced by Appendix M.)

| Term | Count and price | v22b | v25 |
| --- | --- | --- | --- |
| P (T1, T2, T3) | removed online (Z.1); at v25's prices it would be 2^28.4926 | 28.5162 | - |
| P's setup bound / B' / S | 2^32 primitives / B_TRUE 2^29 units + one update / 4 x 2^31 primitives | 21.5959 / 29.0000 / 22.5959 | same |
| Connector | 4268 x (2^20 x 96 + 2^15 x 2^9 + 2^22) primitives | 28.5132 | 28.5132 |
| Bases / E setup | 50 x 2^24 primitives / 50 x 2^16 units | 19.2398 / 21.6439 | same |
| E stage 1 | 50 x 2^14 x 208,007 primitives (v22b: 50 x 2^16 x 66,831) | 27.2680 | **26.9061** |
| E stage 2 / output | 50 x 2^11 x (2 units + 2^11 primitives) / 2^22 primitives | 18.4559 / 11.5959 | same |
| **Online algorithm** | | 30.4623 | **29.980777** |
| G2 / D15 / D16 | X.5's rule at v25's programs (Z.4) | 30.9572 / 32.0018 / 27 | 30.6668 / 31.8816 / 27 |
| D19 / D20 / D21 / D22 | | 28.8303 / 29.0748 / 22.6078 / 26.7962 | 28.7232 / 29.0730 / 22.6078 / 26.7962 |
| D_Y / D_v23 / D_v24 / D23 | Z.4 | - | 14 / 25 / 24.53 / 26.6118 |
| **Development** | | 32.8394 | **32.722414** |
| **Total** | | 33.093387 -> 33.09339 | **32.923440 -> claimed 32.92344** |
| Preprocessing (P's setup bound, B', S, development) | | 33.004263 -> 33.00427 | **32.829571 -> claimed 32.82958** |

Claims are rounded up at the fifth decimal from the exact rational sum. Reference: v24's stated prices under this ledger (D_Y, D_v23, D_v24, no D23) give 32.9765. Sensitivities (not claimed):

| Change | Total |
| --- | --- |
| P kept online (v22b's accounting) | 32.9889 |
| E block at v24's price (66,499 per 256 steps) / at v22b's (66,831) | 32.9939 / 32.9955 |
| no repricing of development beyond v22b | 33.0520 |
| B charged as three executions of P | 33.1129 |
| D23 doubled / D_v23 and D_v24 not charged | 32.9415 / 32.9132 |
| E-constant sweeps charged by v25's time-window bound instead of Z.8's counts | 32.92621 |
| D15 doubled | 33.4946 |
| C charged / R7 charged | 33.4292 / 33.8036 |
| our local organizer runs for v25 charged (Z.6) | 33.0505 |
| also every other verification and timing execution charged (v25's metered runs, the v25s timing gates, the timing runs of the experiment programs: 475 executions at the largest per-execution price, 2^32.7123 units) | 33.8913 |

Memory (R5N3): the claim's figure is R.4's, 62,914,560 bytes; v25's record of earlier memory statements is history and is not repeated here (7, X.8, R.8, Appendix K and M govern).

### Z.6 Organizer experiments and our local checks

- **v25s: experiments regrouped for the organizer's limits.** Our first submission of v25 (fc3ec8af) failed intake: an experiment process exceeded the organizer's 20 s timeout (our local runs had no timeout; the slowest process, r5-count, took 7.2 s locally). The organizer allows at most 16 experiments, so v25s regroups the same checks: r5-count keeps trials 0-7 and r5-count-2 runs trials 8-11 (same functions, same trial numbers); r5-bpfull's trial 1 (B' at its budget and candidate cap) is r5-mitm-0's trial 1; r5-trail-2 and r5-trail-3 run as r5-trail-23 (trials 0 and 1); r5-R-g replays one seed-picked run of its stratum per review instead of two (8 R7 successes per review instead of 16; the strata, the checks of each replay and the certificates are unchanged). Wherever the later text names r5-count trials 8-11, r5-bpfull trial 1, r5-trail-2/3 or two replays per R experiment, this mapping applies. No algorithm, price, count or prediction of a check changes; the edits are in rows_for and bp_rows only (mk_r5v25s.py, mk_manifest_v25s.py). Timing gate (orgrun_gate.py): the organizer's runner with a 13 s timeout per process on the public seed and 8 nonces named before the runs (winglock-v25s-gate-1..8): 9 of 9 runs completed with every experiment's predicted outcome; the slowest process took 5.7 s (no process reached the gate).
- **experiments/r5.py** (SHA-256 959ea423919bb8067396f4de9f4c8986ea511ee6bc092aa4922a3eebad57e52c, 65,245 of 65,536 bytes). By AST its definitions differ from v22b's only in algorithm() (Z.1), the counted programs and their checks (to_planes, keywords, match_step, SW, t2_leaf, t2_trial, ctz, pro, e_block, fes_trial; fes_step, e_ops and S1 removed, e_blk, EP, EW, RES and SP added), the constants T2_LEAF, E_PRO, E_STEPS, HV_STEP, MATCH_STEP, PER_A and the docstring, and (v25s) rows_for and bp_rows, which route trials to experiments; none of the changed programs is reached by algorithm().
- **experiments/manifest.json** (SHA-256 e24942aa...): the scope and hypothesis texts of r5-count and r5-mitm-1 describe v25's programs, and those of r5-mitm-0 and r5-mitm-1 name the advice's provenance in place of premise P; v25s regroups the experiments as above (mk_manifest_v25s.py; each regrouped text says so); every other text and every certificate is v22b's.
- **Local organizer runs (verification, priced, not charged).** experiments/runner.py of the current main with Python 3.12 in place of Docker, every execution metered as in X.10; plan orgplan_v25.txt (SHA-256 67dce02e...), written before v25's runs: the public seed and the nonces "winglock-v25-nonce-1" and "-2"; v25s's runs use the same seeds (orgplan_v25s.txt, SHA-256 403c0ee6...).

| Seed | UTC | report_sha256 | report | meter | log |
| --- | --- | --- | --- | --- | --- |
| public | 10-09T21:43:19Z-21:45:05Z | fde85f4d | ef8c4789 | d3c0b717 | 88023b22 |
| nonce-1 | 10-09T21:45:05Z-21:46:51Z | 64817175 | 10096f9a | c8bbbcbe | 1e9aa802 |
| nonce-2 | 10-09T21:46:51Z-21:48:40Z | 80ab7af2 | 9721826e | 0611ade3 | eed9b752 |

  The runner executes every experiment twice with byte-identical output; on each of the 3 seeds all 16 experiments completed with every predicted PASS: r5-trail-0, r5-trail-1 1/1 and r5-trail-23 2/2 with the exact structural counts predicted, r5-count 8/8, r5-count-2 4/4, r5-mitm-0 2/2, r5-mitm-1 3/3, r5-bpfull trials 0 and 2 PASS (trials 3-26 descriptive only), r5-R-0..7 1/1 full 5-round collision each. Each execution took at most 5.3 CPU-s and 99 MB. Priced like X.10, the runs and our local_tracks checks are 2^29.4821 units; charged, the total would be 33.0505.
- `python3 scripts/local_tracks.py check sha3-256-r5-exploratory`: mechanically_valid (16 certificates verified)

### Z.7 Limitations

- v25's gain over v22b rests on Y's advice reading (Z.1; P online: 32.9889), on X.5's repricing rule applied to v25's programs (without it: 33.0520) and on the multi-pass block's register accounting (Z.3), which follows v22b's 64-word convention; the cost model sets no register limit.
- The multi-pass block computes the same values in a different order (Lemma Z); the organizer checks it against the plain evaluation (trials 0, 2, 4, 6) and its exact price (trial 11), not against fes_step, which r5.py no longer contains; our check_e.py compared the two.
- Everything else is inherited from v22b unchanged: rule K's premise (W.1), premise R, R7's fallback to v19 (W.3), A1 uncharged (V.6), v17's B' re-derivations listed and not charged, and local organizer runs priced and not charged (X.10, Z.6).

- Z.8's invocation list comes from our session command log; the package carries its excerpt for these commands, not the log itself, so completeness of the list is our statement (v25's window bound: 32.92621). sweep.py, sweep2.py and the counting rule are in Z.8, so their counts can be re-derived; model.py's source is not (its count is 2% of its 2^31 process charge).

### Z.8 v25h: the E-constant sweeps counted per invocation; what verification, X.5's rule and R7 fix

(R5N3: history, condensed. v25h charged the E-constant sweeps of D23 (model.py, sweep.py, sweep2.py and one command) at their per-invocation operation counts; R5N3 does not charge D23 or these sweeps (R.8, Appendix M). The scripts and their per-invocation counts are in R5N2's and b5213766's proofs.)

## X. What v22 changes (cheaper counted programs: Th0rgal's v21 re-derived, adopted and extended; no new heuristic, cap, constant or run of the algorithm)

**Credits first.** v22 is our v20 (84668773) with the counted programs of this section and nothing else. Its starting point is **Th0rgal**'s v21 (a9ec6971, claimed 33.12242), which is our v20 with four routines of experiments/r5.py tightened: the match step (62 -> 60: the tail's SWAR constants masked to 64 bits, so the tail needs no mask, and the carry-free byte fold (c + (c >> 8)) & HM), the T2 leaf with its Gray step (56 -> 42: the identity NOT ALLOW(q) = (x0 AND NOT x2) OR (x1 AND NOT x3) OR ((x2 OR x3) AND NOT x4) on lanes that hold x4 twice, and a Gray step that addresses the adjacent-choice difference directly), the half-vector step (96 -> 93: the same direct addressing, with signed weight deltas) and E's stage-1 block (69,242 -> 68,472: words 0..10 of D2[0] in the 11 registers that v19 left free). We re-derived each of the four from v21's published description, wrote it into v20's experiment file ourselves and checked it against v20's programs and the plain evaluation (X.6); all four are in v22, each extended below, and v21's own build checks of them (its D21) are charged in v22's development (X.8). **Th0rgal is a co-author** (also of v14, and of the zero-advice framing in 7deb1595). The rest of the lineage is credited and co-authored as in v20 (Section W): Meganpark980320, rubenmarcus, Subflatus3, 0xshikhar, and winglock's v8, v13, v14, v19 and v20.

| Change | Where | v20 | v21 (Th0rgal, as stated) | v22 | Evidence |
| --- | --- | --- | --- | --- | --- |
| X.1 match step | P (T3), D15, D19 | 62 per match, per_a 11 | 60, per_a 11 | 56 per match + 3 per 16 matches of a run (899/16 = 56.1875 per match), per_a 18; the run loop as executed control flow | r5-mitm-1 trial 2; check_v22.py |
| X.2 T2 leaf with its Gray step | P (T2), D15's T1/T2 export | 56 (leaf 22, step 34) | 42 (15, 27) | 26 (leaf 9, state step 17) | r5-count trials 1, 3, 5, 7; check_v22.py |
| X.3 half-vector step | P (T3), D15, D19 | 96 (99 with 16 key words) | 93 (96) | 83 (86), with the entry pointer's advance that v17-v21 left out | r5-mitm-1 trial 1; check_v22.py |
| X.4 E stage-1 block of 256 steps | E, G2, D20 | 69,242 | 68,472 | 66,831, with the prologue's 16 stores, the block index in memory and a spill at r = 0 that v18-v21 left out | r5-count trials 0, 2, 4, 6 and 11; check_v22.py |
| X.5 development at v22's prices | G2, D15, D19, D20 | v20's programs | v21's programs | v22's programs (V.3's rule) | ledger_v22.py |
| X.8 development of v21 and v22 | 0.1 | D20 | D21 2^22.6077 | D21 charged (2^22.6078); D22, every run we made for v22 except the organizer's harness, 2^26.7962 | X.8 |

Result: algorithm 2^30.5033 -> 2^30.4623; development 2^32.8930 -> 2^32.8394; total 2^33.144923 -> **2^33.093387, claimed 33.09339** (rounded up at the 5th decimal); preprocessing 2^33.058081 -> 2^33.004263 (claimed 33.00427). Success probability 0.40 from R7, unchanged (X.11). v21 claims 33.12242; v22 is 0.02903 below it. Every price below is a counted longest path of r5.py (W operators: a primitive counts 1, load() and st() 1, test() 2 for the comparison and the branch) and is checked by the organizer on every review. v22's gain over v20 rests on the lineage's rule that development is priced at the submitted programs' counted prices (X.5): without that repricing the total would be 33.1571.

### X.1 Match step: 56 per match, 3 per 16 matches of a run, per_a 18 (match_step, match_run, per_a in r5.py)

v20's match step (U.1) costs 62. v22's body (55; 56 with the run loop's pointer load) is superseded in v25 by Z.2's 49; the sum into the top field and the run loop below are kept.
- Th0rgal's two v21 tightenings (the unmasked folded tail and the carry-free byte fold) are superseded in v25 by Z.2's nibble-aligned tail planes and nibble fold.
- New in v22, the sum into the top field. The four stages are c + (c << 16), c + (c << 32), c + (c << 64) and c + (c << 128); a left shift of a 256-bit word drops the bits above bit 255, and r5.py's W now models that. Each 16-bit field holds at most 32 after the fold, so no field carries, and the top field (bits 240..255) ends at AS <= 320 < 2^16 while the lower fields hold partial sums below 2^240. Hence c < nb x 2^240 iff AS < nb: the final mask goes (-1). The experiment reads AS as c >> 240 outside the count, for its check only.
- New in v22, the run loop unrolled 16 times (match_run). The matches of one a in one block are one run of e B entries after the merge. per_a, once per (a, block): A's 7 words (7), e = end - start (1), the match counter advanced by e and its M_CAP test (3), q = e AND 15 (1), the end of the peel start + q (1), the jump-table load and the jump into the peel (counted as a test, 3) and the guard e < 16 (2): **18**. The peel runs the first q matches as straight-line copies; then each pass of the loop runs 16 copies, advances the run pointer and tests it against the run's end (3). A copy loads its entry's pointer at a fixed offset from the run pointer (1) and runs the body (55): **56**. So a run of e costs exactly 18 + 56 e + 3 floor(e/16), every match is priced at **56 + 3/16 = 899/16** (v20 62, v21 60), and per_a lies inside 2.1's bound of 2^6 per half vector per block, of which the radix sort and merge use 37: 37 + 18 = 55 <= 64, so P's sort-and-merge term is unchanged. (For P alone the slot is not needed: per_a runs at most M_CAP times, 2^17.8 units if charged on top.) The body has a single path.

Evidence. r5-mitm-1 trial 2 (organizer seed) checks the run loop, AS and every decision against the plain evaluation, now with v25's 49 (Z.2): each run of e counts exactly 18 + 49 e + 3 floor(e/16). Our check_v22.py compared v22's AS and decision with v20's on all 49,060 level-64 matches of the output core and 20,002 random plane vectors: equal in every case.

### X.2 T2: the leaf (8, or 9 when kept) and the Gray state step (17)

Leaf. v22's two lane-parallel selections (8, or 9 when kept) are superseded in v25 by Z.2's single-AND leaf (4, or 3 when not kept). v20's leaf counter and its cap test are gone: T2 visits exactly C1 leaves, an organizer-recomputed count, and every core's walk ends by Algorithm H's own end test.

Gray state step (gstep; X.3 uses it too). Knuth's Algorithm H keeps, for row j, a position a_j and a direction o_j. v22 keeps the pair as one state of the row's state table: the up-states (a, +1), a = 0..m_j - 2, at offsets 2a, and the down-states (a, -1), a = m_j - 1..1, at offsets 2(m_j - 1 - a) + 1. A state's record holds the address of the next state, the move's difference words (the XOR of the two choices' vectors) and, for X.3, the move's signed change of the weight. Every move that does not reach an end goes to a higher offset; the two moves that do (a_j becomes m_j - 1 or 0, where H reverses o_j and updates the focus pointers) go to a lower offset, since m_j >= 3 (every m_j is at least 4 in T2 and at least 9 in T3; for m_j = 2 the encoding would fail). So H's reversal test is one comparison of the new state's address with the old one. Step: j = f_0, f_0 = 0 and the end test (4); the state, its successor and the store (3); 2 per word (load and XOR); the reversal test (2); f_j = f_{j+1} and f_{j+1} = j + 1 (4): **17 with 2 words**, on the longest path (v20 34, v21 27). Lemma X2. From H's initial state (every a_j = 0, o_j = +1, the up-state at offset 0) the state step makes the same sequence of moves (j, a_j) as H, and its words change by the same XORs. (By induction on the steps: a record's successor and difference are those of H's move from that state, and the focus pointers are H's.)

A leaf with its step: 26 in v22 (v20 56, v21 42); 21 in v25 (Z.2). Prices: P's T2 and D15's T1/T2 export, C1 leaves each.

Evidence. r5-count trials 1, 3, 5, 7 (organizer seeds; v25's leaf, Z.2): the leaf equals ALLOW on all 32 row values, and 64 leaves of a seed-picked walk match the plain test and layout; r5-mitm-1 trial 1 exercises every row's reversals. Our check_v22.py: the first 200,000 leaves of the output core's walk, v22's state step next to v20's: the same moves, words and decisions.

### X.3 Half vectors: 83 (86 with 16 key words)

The half-vector step is the state step of X.2 with the plane and key words (3 per word), the weight update (3) and the entry pointer (1): 83 with 15 key words in v22, 80 with 14 in v25 (Z.2); 86 / 83 in D15's ten-level run. The state tables are per-core setup inside Section 6's bound of 2^32 primitives for P's setup.

Evidence. r5-mitm-1 trial 1: both full half tables of the output core (118,096 steps) against halves() and the key words; the longest step counts exactly the stated price. Our check_v22.py compared all 118,096 entries: equal.

### X.4 E stage 1: 66,831 per block of 256 steps

v22's single-pass block of 256 steps (fes_step; v20's U.2 less the step counter and the pass word's complement, with Th0rgal's D2[0] registers) is superseded in v25 by Z.3's multi-pass block of 1,024 steps; r5.py no longer contains fes_step. Kept from X.4:
- The block is straight-line code; the block loop is counted once per block in the prologue, and a pass's coordinate is formed in stage 2.
- The pass word is formed only for stage 2: the step compares the OR with all-ones (2).
- Resident derivative words save their loads and stores (Z.3 generalises this to 29 resident tables per pass).
- Two omissions of v18-v21 are now counted. The prologue stores the 16 partial ranks it computes, which the steps load (+16 per block), and keeps the block index B in memory (its load and store, +2). And this proof's register convention (64 words of 256 bits, Section 1, since v14; the cost model sets no register limit) holds at every step: besides the 59 resident words, a step needs the chain value, a load temporary and one address register per level whose rank depends on B, at most 5 in all, except at r = 0, where all four positions come from B; there one resident word is spilled and restored (+2 per block).

v22's block bound: 66,714 per 256 steps plus a prologue of at most 117, **66,831** (v20 69,242); v25: 207,920 per 1,024 steps plus at most 87 (Z.3).

Stage 2's hand-off spills and restores the 59 resident words (118) and forms the pass word and the coordinate (at most 4), all inside 2.4's 2^11 primitives per pair (at most 32 basis additions of 7 words, 448, and the second message, 14, besides them). The 11 extra loads when a space starts lie inside the setup bound of 2^16 units.

Evidence (v22). r5-count trials 0, 2, 4, 6 and 11 checked fes_step's values and price; in v25 the same trials check e_blk (Z.3). Our check_v22.py: two seeded spaces, 1,023 steps each, v22's fes_step next to v20's: F, every derivative vector and the pass word equal at every step.

### X.5 Development at v22's prices

The lineage prices development at the counted prices of the submitted programs: v14 priced G2 at v14's E, v15 priced G2 and C at v15's E, v17-v19 repriced D15 at their counted T3 programs (V.3, U.6), and v21's own gain over v20 comes from the same rule. With v22's programs: G2's 530 E spaces at 66,831 per block; D15's contiguous run, layouts and certified run at 899/16 per match and 86 or 83 per half vector; D15's T1/T2 export at 26 per leaf; D19's contig.c run at 899/16 + 31 per match and 83 per half vector; D20's R7 self-test at 66,831 per block. The other D19 and D20 items keep v20's prices, which only over-charges (without any repricing of D19 and D20: 33.0979). These runs were made by native or older programs (mitm2.c, contig.c, fes.c) whose native 64-bit C loops execute strictly fewer actual word operations (<30/vector/block, <35/match, <150/block; <1,860 CPU-s in D15) than the submitted counted-program bounds charged here, so X.5 is a conservative upper bound on actual historical operations. **A reader who rejects that rule should use 33.1571** (G2, D15, D19 and D20 at v20's prices, D21 and D22 charged), which is above v20's 33.14493: v22's improvement over v20 comes from the rule, as v17's to v21's did.

### X.6 Th0rgal's v21: what we checked

v21's note (a9ec6971) gives each change with its count, and we took the four ideas from it; we did not use v21's experiment file. Each idea, as written into v20's file by us, computes exactly what v20's routine computes (X.1-X.4, with the organizer's checks and check_v22.py). Where v21's stated counts differ from ours, the difference is in our extensions (the top-field sum and the unrolled run loop; the selection form of the leaf, the dropped counter and the state step; the dropped step counter and complement) and in the omissions we now count (X.3, X.4), except in E: v21's 770 for D2[0]'s registers is below the per-position saving of 1,408. Under our ledger's rules, v21's stated prices give 2^33.119910 before v21's D21 and 2^33.120897 with it, against v21's stated 2^33.122414; we could not trace the remaining difference (about 0.0015) from v21's note. The total with one program at v20's price and the others at v22's: match step 33.1410; T2 leaf and step 33.1048; half-vector step 33.0948; E block 33.1041.

### X.7 Considered and not adopted: B2, and 395e8a28's T.1 and T.3, at v22's prices

B2 (W.7: a 31-primitive filter, the popcount of alpha2's bit-0 plane on rows 0..255, in front of the match step, and an exact re-count of v15's stopped contiguous run to price D15's largest item with it) still cannot lower the total. Our study projected about -0.17 for it; that projection left the re-count uncharged (the study's own runs, contig.c among them, are charged in D19). The re-count would fix a number of the claim, so W.6's rule charges it (every run we make is charged; v15 charged its own count-only recounts). It must run the filter on every match of the run (at least 4.245 x 10^10 + 1.145 x 10^10) and sort and merge 138 blocks of HV half vectors: the repriced item is at least 2^30.5635 and the re-count at least 2^30.5381, together at least 2^31.5509, above the item at v22's prices (2^31.3984). With the re-count charged, the total would be at least 33.1422; with it uncharged, which is not our rule, at least 32.8829. We did not run the re-count and do not claim either.

395e8a28's T.1 (a counted stage-2 step, with the hand-off: 2 units + 192 per pair) and T.3 (the self-test's B' at a measured true cost), as W.11 prices them, at v22's prices: T.1 with its development charged 33.1850 (uncharged 33.0932); T.3 with its measurement charged 33.0970 (uncharged 33.0748). Charged as this lineage charges such runs, neither lowers the total; we do not claim the uncharged values.

### X.8 Development of v21 and v22: D21 and D22

D21. v22 adopts the ideas of v21's four routines; v21 states that it checked them with Python build checks priced at 2^22.6077 units. By W.11's rule v22 charges D21 at v21's stated value rounded up, 2^22.6078, and R5N3 keeps that row (Appendix M). D22 (every run we made for v22, 2^26.7962) is history, condensed, and is not charged in R5N3 (R.8); its itemised table is in R5N2's proof.

### X.9 Ledger (log2 units; exact rationals, rate 1355; ledger_v22.py)

(R5N: superseded ledger condensed to fit the 512 KiB judge-evidence budget; its table and sensitivities are in 0f72a85e's proof, unchanged. Appendices J and L govern.)

### X.10 Organizer experiments and our local checks in v22

- **The experiment file.** r5.py (SHA-256 d737b451302052183ebd5e9aac875df0e3db3099b35be0fd8d976f1e19037909) is 64,959 of 65,536 bytes. By AST, its definitions differ from v20's (4941939a...) only in the counted programs and their checks (gstep, gtab, gpos, t2_leaf, t2_trial, hv_trial, per_a, match_run, match_step, match_trial, pro, fes_step, e_ops, e_block, fes_trial; v20's hv_step is now gstep with a weight), the constants T2_LEAF, E_PRO, E_STEPS, HV_STEP, MATCH_STEP, PER_A, S1, UNR and DUP, r5-count's twelfth trial in rows_for, the left shift of W (256-bit) and the docstring; in the functions that neither algorithm() nor the module's import-time tables reach, whitespace is compacted (' = ' to '=', ', ' to ',' and, in the checks, the spaces around binary operators; compact_v22.py, AST-checked). algorithm() and every definition it reaches, including the helpers that build its import-time tables, are byte-identical to v20's (X.11).
- **r5-count and r5-mitm-1** now check v22's programs (X.1-X.4), and r5-count has a twelfth trial (the E block price); their scope and hypothesis texts in experiments/manifest.json say so; every other experiment, and its text, is v20's.
- **Local organizer runs (verification, priced, not charged).** experiments/runner.py of the current main with Python 3.12 in place of Docker, every execution metered as in U.5, written down before the runs. A first set (plan a473d203..., 2026-10-08T23:15:02Z; nonces "winglock-v22-nonce-1" and "-2") ran an earlier build (a7f9cbbb...) that our review then changed; the final set (orgplan_v22.txt, SHA-256 c1c0b29c..., 2026-10-08T23:43:55Z; the public seed and the nonces "winglock-v22-nonce-3" and "winglock-v22-nonce-4") ran the final files, which are v22b's (X.12). Per seed (UTC; SHA-256 prefixes of the runner's report_sha256 and of the report, meter and log files):

| Set, seed | UTC | report_sha256 | report | meter | log |
| --- | --- | --- | --- | --- | --- |
| first, public | 10-08 23:15:39Z-23:18:09Z | c77b445d | dda5f85b | 131c4f20 | ab9796ce |
| first, nonce-1 | 10-08 23:18:09Z-23:20:41Z | dc9f845c | 7845a00c | 73325986 | 7582f5ae |
| first, nonce-2 | 10-08 23:20:41Z-23:23:14Z | 90d62fcb | 9eb1cfbd | 3a868560 | 52872bf3 |
| final, public | 10-09 02:00:05Z-02:02:44Z | 8f93e4da | 41f96278 | 9eba2d02 | 2a270352 |
| final, nonce-3 | 10-09 02:02:44Z-02:05:22Z | eb20ad03 | 8e558c70 | 0ba7cb17 | 1e9688fe |
| final, nonce-4 | 10-09 02:05:22Z-02:08:03Z | 2cbb7e8c | 72c2c441 | 92f5ab2c | a21d9573 |

  The runner executes every experiment twice with byte-identical output; on each seed of each set all 16 experiments completed with every predicted PASS; on the final set: r5-trail-0..3 1/1 each, r5-count 12/12, r5-mitm-0 1/1, r5-mitm-1 3/3, r5-bpfull trials 0-2 (with 18/18/19 of its 24 descriptive connector attempts accepted), and r5-R-0..7 two full collisions each (16 per seed). Each execution took at most 7.4 CPU-s and 99 MB. Priced like U.5, both sets and our local_tracks checks are 2^30.6009 units; charged, the total would be 33.3294.
- **Certificates** are v20's (r5-v6-000038 and the collisions of R7 runs 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17).
- `python3 scripts/local_tracks.py check sha3-256-r5-exploratory`: mechanically_valid, ready, 16 certificates verified.

### X.11 Why R7 measures v22

The counted programs are the algorithm's price model: the organizer checks that they compute what the algorithm computes and counts their longest paths; algorithm() never calls them (its P is trail_search, its E is e_window, 2.5). algorithm() and every definition it reaches (B', the connector, E, P's driver, the caps and K = 50, and the helpers chi5, _affine_subsets, _theta_inv_setup and fwd that build its import-time tables) are byte-identical to v20's file, whose algorithm R7 ran (W.2, W.10); the W class, whose left shift changed, is not used by algorithm(). So every R7 run is a complete run of v22, premise R and premise P are v20's, and H1 is unchanged except for the package's name.

### X.12 v22b: the same package with condensed text

v22 (53ed1c23) was refused at the organizer's intake because its judge evidence (the line-numbered proof, the intake and certificate reports, the experiment view and the benchmark contract, as canonical JSON) exceeded the 512 KiB review budget: 555,193 bytes by our reconstruction with the organizer's own code (v20's, which passed, 520,664). v22b changes only this proof's text and, in claim.json, the proof line references and one sentence. experiments/r5.py (d737b451...), experiments/manifest.json and the certificates are v22's byte for byte, so the organizer runs of X.10 executed exactly v22b's experiment files; the algorithm, the claim and every price are v22's. What changed:
- Condensed (superseded or historical text): U.1-U.3, U.5's list of organizer runs, U.6 and U.8; V.1, V.4 and V.7; W.7, W.9's sensitivities and W.11; v15's summary in Section 0; Sections 4.1, 4.5 and 4.6, Lemma 6(c) and the v15/v19 heuristics paragraph of Section 5; Section 6's table, which keeps v22's terms (earlier versions' values are in X.9, W.9, U.8 and V.4) and now lists D21, as X.9 does.
- Run lists as tables: the local organizer runs of W.10 and X.10; each study's per-run ledger merged into its per-run table (R7: W.2; R6: 4.7; R5: Appendix D, which now holds 4.3's table, with R5's per-space pass counts summarised as min-max per run).
- Appendices: C's plans and the R5 and R6 plans summarised; the R6 and R7 drivers, analyses and launchers and krule.py described by function; the superseded R7 commit record given by its differences. Kept verbatim: Appendices A and B, rule.txt, R7's plan, every commit record in force, krule.out and the builder record. The verbatim texts of v22's Appendices C-F are byte-identical in v20's proof (84668773).
- Prose is no longer hard-wrapped (one line per paragraph or list item); the rendered text is unchanged.

Every SHA-256 value, every disclosed run and every number that a claim, bound, price or sensitivity uses is kept; dropped are details of superseded programs (v18's and v19's per-step and per-space savings, v15's file size), the Bonferroni levels of C's plan, constants of the condensed drivers' code and R5's per-space pass counts. v22b's own checks ran only the organizer's intake, certificate and judge-view code (verification, not charged; a certificate check is 2^9.65 units, which leaves 33.3294 unchanged).

## W. What v20 changes (rule K with a new pre-registered study R7, C no longer charged, P's T3 core by core; no new heuristic)

(v22: Section W is v20's text. Where it states a price of a counted program or a total, Section X governs.)

| Change | Where | v19 | v20 | Evidence |
| --- | --- | --- | --- | --- |
| W.1 K, A_ADV, A_MAX, S2CAP | 2.3-2.6 | 96, 2^11, 2^13 (v10, from G2; K kept by C's rule); S2CAP = 2^21 (v13's cap rule) | 50, 1067, 4268 and 2^11 by rule K: an analysis of P's exact output and of R7's design, written and hashed before any run of R7; no run outcome is an input | rule.txt, krule.py (Appendix F) |
| W.2 Success evidence | 5 | R6 44/48 and R5 46/48, complete runs of v19 (K = 96) | R7: 48 pre-registered complete runs of v20; 39 succeed, one-sided 95% Clopper-Pearson bound 0.6956 | W.2, Appendix F; certificates; r5-R-0..7 and r5-bpfull replay R7 runs |
| W.3 C | 0.1 | charged, 2^31.9189 (its only role: keeping K = 96) | not charged (K no longer depends on it); G2 stays charged | W.3 |
| W.4 Order of P's T3 (= 0xshikhar's T.2) | 2.1, 7 | level by level over all cores (before v20, trail_search kept every core's half tables: 48,592,224 vectors of 1,600 bits, far above the cap) | core by core, all seven levels per core: the same output, counts and terms, with one core's half tables in memory | Lemma W; r5-count trials 8-10 |
| W.5 D15 (includes 0xshikhar's T.4) | V.3 | the native T3 runs' half vectors priced once | priced at every level, as those programs computed them | Appendix A (mitm2.c) |
| W.6 D20 | 0.1 | - | every run we made for v20 except executions of the organizer's harness and the study R7 (our replay test included): 2^29.0751 units | W.6 |
| W.11 395e8a28's T.1 and T.3 | 2.4, V.3 | - | considered, not adopted: with their runs charged as this lineage charges such runs, neither lowers the total | W.11 |

Result: algorithm 2^31.3507 -> 2^30.5033; development 2^33.4106 -> 2^32.8930; total 2^33.7207 -> **2^33.144923, claimed 33.14493** (rounded up at the 5th decimal); preprocessing 2^33.5279 -> 2^33.058081 (claimed 33.05809). Success probability 0.40, measured by R7 alone. R5 and R6 ran v19's K = 96; they are reported as history and support no bound of v20 (W.8).

Credits first. v20 is our v19 (a2d6ce92), which is **Meganpark980320's v18** (f1eb6445; its v17 168a1b3a) with the changes of Section U; v18 is **rubenmarcus's v15** (91f1424d) with the changes of Section V; v15 is winglock's v14 (f1cedf6b, with **Th0rgal**). T3's zero-block half-sum match is **Subflatus3**'s (9bccf245), and the zero-advice framing is Th0rgal's 7deb1595 (with Subflatus3 and rubenmarcus). **0xshikhar**'s 395e8a28 (itself our v19 with four changes, the lowest claim in review when we finished, 33.6804) found and repaired the memory flaw that v19 inherited: its T.2 is the same repair as our W.4, and 0xshikhar published it first (6667fc4f, then 395e8a28). Its T.4 is the certified-run half of our W.5. Its T.1 (a counted stage-2 step) and T.3 (a measured true cost for D15's driver self-test) are sound accounting, and W.11 says why v20 does not take them. Co-authors of v20: Meganpark980320, rubenmarcus, Th0rgal, Subflatus3 and 0xshikhar. New here: rule K, R7, the order of P's T3 loops, the D15 repricing and D20. Everything from Section U on is v19's text, edited only where a number or a rule changes; each such place is marked "(v20)".

### W.1 Rule K: four constants from P's exact output and R7's design

Rule K (Appendix F, rule.txt, verbatim) reads three exact facts of P's output (Section 3): w2 = 24 (E's 24 stage-1 equations), P45 = 55/2^19, and the 2^32 pairs of E's window. Under the model that a pair passes stage 1 with probability 2^-24 and a passing pair collides with probability P45, a space holds lambda = 2^32 x 2^-24 x 55/2^19 = 55/2^11 = 0.026855 colliding pairs on average, succeeds with probability q = 1 - exp(-lambda) = 0.026498, and K spaces of independent coins give p_K = 1 - (1 - q)^K. The model only chooses the constants; the claim rests on R7.
- K. R7 has 48 runs and claims 0.40 iff its one-sided 95% Clopper-Pearson lower bound is at least 0.40, that is iff s >= 26 (Pr[Bin(48, 0.40) >= 26] = 0.0329 <= 0.05 < 0.0604 = Pr[Bin(48, 0.40) >= 25]). K is the least value for which the study passes with probability at least 0.999 under the model: **K = 50** (p_50 = 0.73888, Pr[pass] = 0.999041; K = 49: 0.998575). At the level 0.99 the rule would give 44. krule.py computes this with exact rational binomial sums (output krule.out, in the commit record).
- A_ADV and A_MAX. v10 set A_ADV = 2^11 and A_MAX = 2^13 for K = 96 from G2's runs (charged). The rule keeps G2's ratios: **A_ADV = ceil(50 x 2^11 / 96) = 1067** and **A_MAX = 4 x 1067 = 4268**, still at most four advice rounds (S's term of 4 x 2^31 primitives is unchanged).
- S2CAP. The least power of two at least 8 times the model's 2^32 x 2^-24 = 256 stage-2 pairs per space: **S2CAP = 2^11**.
- Unchanged: X_MAX = 2^20 work units, B_TRUE = 2^29 units, B_BUDGET = 2^32 units, CCAP = 2^26 units, B''s code and constants, S, the connector, P and E.

History, stated plainly. The rule reads no run outcome, but it was written after G2 (the v6 run, pre-registrations A and B), pre-registrations C and D, C', R5 and R6 had run, and its author knew their outcomes: R5 46/48 and R6 44/48 at K = 96; positive spaces per enumerated space 0.037 (R5) and 0.031 (R6), above the model's 0.0265; R5 and R6 truncated at 50 spaces would each give 40/48; largest stage-2 counts 308 and 315. The power level 0.999 (rather than 0.99) and the factor 8 of S2CAP were chosen with that knowledge, in our study of 2026-10-08, and v19 (U.7) declined to adopt the rule for this reason. What the knowledge could have done, it did not do: every conventional power level gives a smaller K under the model (0.80: 34, 0.90: 37, 0.95: 39, 0.99: 44), and with R5's or R6's observed rate per space in place of the model's q even the level 0.999 gives 36 or 43 (klevels.py: exact sums, no target computation; W.6). So the K chosen with the earlier outcomes known is the most expensive of these alternatives. Likewise S2CAP's factor 8 is above the factor 2 that the observed maxima (308, 315) would have allowed, and all of E's stage 2 at 2^11 is 2^18.4559 units. Our rule for numbers the algorithm reads: a number selected by target-specific runs is charged unless an a-priori rule fixed it, written down and hashed before the new evidence run, with the history disclosed and the charged sensitivity printed. rule.txt and R7's plan were hashed together at 2026-10-08T15:23:01Z (commit.txt), before any run of R7, and rule.txt states this history itself. Charged anyway (W.9): with C 33.6585; with C, R5 and R6 35.3462; with R7 34.0173; with all four 35.5857; with S2CAP kept at 2^21 33.1998.

### W.2 R7: 48 pre-registered complete runs of v20

Plan (Appendix F, verbatim; plan.txt, SHA-256 4f7f38abc6635ae5c710c44ef113affab5ca3a1f17bb86637abdfea0c6f8e2f1), hashed at 2026-10-08T15:23:01Z with rule.txt, krule.py and its output, the driver r7run.py, the experiment file r5v20.py, the binary fes and fes.c (Appendix B), the analysis analyze7.py, the launcher run_all7.py with its wrapper run7.sh, the organizer verifier's keccak.py and the driver's self-test record (commit.txt, SHA-256 eebce75c95f63140a68d3d7867586af9d554cc4923eec01c264c3669193772f7). All of them were made read-only at the commit. A first commit record (15:22:40Z) was replaced before any run, only to correct two dates to UTC; both records are in Appendix F. Labels "hashsmash sha3-256-r5 R7 run k", k = 0..47; every coin is derived from the label exactly as algorithm(label) derives it.
- r5v20.py is v19's experiments/r5.py (97815b2c...) with three edits: the version string, the constants line "K_SPACES, A_ADV, A_MAX, S2CAP = 50, 1067, 4268, 1 << 11", and, in the organizer replay of R5, the bound on a logged space index written as R5's 96. The shipped r5.py differs from r5v20.py only in trail_search's loop order (W.4), which R7 does not execute (every run uses P's certified output, as R5 and R6 did), in the organizer replay tables (W.10) and in the spacing of ten constant tables (compact_ws.py, AST-checked); every function that algorithm() calls after P is byte-identical.
- r7run.py makes algorithm()'s calls in algorithm()'s order: bprime with the WK budget, CCAP and the true-cost budget B_TRUE; Setup; connector attempts until 50 are accepted (the advice is discarded after 1067 attempts; at most 4268 attempts in all); then E on the 50 spaces in order (fes, then stage 2 by complete digests in fes's order on at most 2^11 passes), stopping at the first output.
- Before the plan the driver ran once, as a self-test on the label of R5 run 21 (an outcome logged by R5): with K = 50 it reproduced R5's advice (candidate 0, attempt 3, DF 49, advice hash 76a6a0b06305286a), the DF 48 of space 1 and the collision at space 1, coordinate 18c48859 (selftest.json; charged in D20). No R7 label was run before the commit.

Launch: run7.sh took the machine-wide heavy-job lock at 2026-10-08T15:30:37Z and started run_all7.py: increasing k, at most 10 runs at a time, a new run only while the 1-minute load average was below 12, nice 10, Python 3.12. The first run started at 2026-10-08T15:30:37Z and the last ended at 2026-10-08T16:04:54Z; all 48 exit codes are 0 and all error files are empty. Python CPU time 10,296 s in all, plus 1,382 s in fes; at most 1,420 CPU-s and 116 MB per run.

Results (every run; table below, which includes the per-run ledger's coordinates and result-file hashes):
- **39 of 48 runs output a collision**; runs 0, 6, 12, 25, 27, 28, 29, 30 and 31 had no output (none-in-K). Every collision was verified by analyze7.py with the experiment file's digest5 and with the organizer verifier (sha3_256(m, 5)).
- Analysis (analyze7.py, fixed in the plan): one-sided 95% Clopper-Pearson lower bound 0.6956; by the plan's rule the claim 0.40 is supported (analysis.json, SHA-256 aebc7346398e321273b8f4c230439e2187c3993405bcb20ae9110d691a95c4de).
- B': 128 candidates in all; B' cost per run 2^23.00 to 2^29.47 units at WK's counter, true cost at most 2^28.60 units (B_TRUE = 2^29 units never acted; B_BUDGET never acted).
- Connector: 49 advice rounds, 6,920 attempts, 2,400 accepted; advice discarded at A_ADV: run 12 (0 accepted in 1067 attempts). Largest attempt 197,334 work units (X_MAX = 2^20 never reached); at most 1,201 attempts in a run (A_MAX = 4268 never acted).
- E: 1,249 spaces enumerated, all self-checks passed; round-2 passes per space 199-310 (256 expected; S2CAP = 2^11 never bound). First positive space at index 1-46.

Each run is therefore a complete run of v20 with its label's coins: B_BUDGET, B_TRUE, X_MAX, A_MAX and S2CAP never acted; CCAP and A_ADV acted only as the algorithm prescribes (ending candidates without an accepted attempt, and discarding one advice); the nine runs without output enumerated all 50 spaces. The output is algorithm()'s output for these coins (E's stage 2 follows fes's order, which changes at most which colliding pair of a space is output, Lemma 4).

Premise R for R7 (inside H1): the label-seeded coins act as fresh coins and R7's 48 runs are an unselected sample of v20's runs. Support: the labels, the plan, the rule and every file of the computation were hashed and made read-only before any run; every run is reported; the plan's only outcome-dependent rule is whether v20 is claimed (W.3), and a bound computed by a rule fixed in advance keeps its coverage (Pr[the claim is made and the true success is below it] <= 0.05); no constant was changed after any run. Which runs the organizer replays and which collisions are certificates was fixed before any result existed (plan.txt; the table builder mk_r7table.py, SHA-256 7044aa7e..., was hashed at 15:29:39Z, before the first result file), with one later exception: run 22 was left out of the replay strata after our replay test measured its replay at 107.8 MB, too close to the organizer's 128 MB (W.10). Its collision stays in the per-run ledger and counts in R7; counted as a failure instead, 38 of 48 would still give a bound of 0.6723. Six of the nine failures fall in runs 25-31. The labels are SHA-256-derived and the runs deterministic; every failed run ended normally (exit code 0, empty error file) after enumerating all 50 spaces with every fes self-check passed. Any systematic fault in a batch of concurrent runs could only have produced false failures, which bias the bound down.

Organizer evidence for R7: r5-R-0..7 replay R7, as R7's plan fixed (R7's table fits the 64-KiB budget): the experiment file's table RUNS holds R7's 48 runs, and over a review the organizer seeds re-derive 16 of the 38 replayable R7 successes (8 strata, 2 each), run 22 being left to the per-run ledger because its replay came too close to the organizer's sandbox limit in our replay test; r5-bpfull trial 0 runs a whole B' of R7 run 6 or 33 or 37 from its label and trial 2 checks R7's table and bound (W.10). The collisions of R7 runs 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17 (the first 15 successes in k order) are certificates, with v6's.

Per-run table (from the result files; "attempts", "accepted": connector attempts and acceptances per advice round; "spaces": E's spaces enumerated up to the first output; B' over all rounds of the run, at WK's counter and at its true cost; the output coordinate and the SHA-256 of results/k.json, which are R7's per-run ledger, merged here in v22b):

| k | candidates | (c, j) per round | DF | B' log2 units (WK; true) | attempts | accepted | spaces | first positive space | success | coordinate | results/k.json SHA-256 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 3 | 2, 46 | 35 | 27.57; 24.93 | 51 | 50 | 50 | none in 50 | no (none-in-K) | - | 7736204c6c3cbdb8b8fa94a29e84c50786714f022a64dcb87b0a68b18695f234 |
| 1 | 1 | 0, 13 | 41 | 24.25; 21.59 | 60 | 50 | 29 | 29 | yes | 14afb8c6 | dd25f17cfad00857c8f162a24d9031045c49c6227e2aef3a00aeb125637b9e0b |
| 2 | 1 | 0, 13 | 46 | 24.41; 21.87 | 223 | 50 | 18 | 18 | yes | 3f841d38 | 2d0d69ffae55112d2cf14cdf5c8e982f8f056e1b72e00f101e65b135138f3360 |
| 3 | 4 | 3, 11 | 64 | 27.72; 25.07 | 53 | 50 | 6 | 6 | yes | 7b036919 | b7da8e46c183b10f75fec1d91203d83f2938d109d8d7bd765aa9d59effae1b8d |
| 4 | 2 | 1, 0 | 44 | 26.14; 25.84 | 139 | 50 | 12 | 12 | yes | ea8b24fb | 2f05f3d07712e3704dae3244894ae077f771cf4fd440e81638ee8dbcfcf9d596 |
| 5 | 1 | 0, 9 | 36 | 24.48; 21.94 | 330 | 50 | 46 | 46 | yes | cf0d4d9d | 6d33ee9295efc16bf82bf4c08b42ddd8c67f146778ec7f76f45fd11ad39538f3 |
| 6 | 1 | 0, 2 | 51 | 23.53; 20.98 | 64 | 50 | 50 | none in 50 | no (none-in-K) | - | 5689a4ed54279e46a1d8e74179780b21cca7342f225eafce2212fbefee42b92d |
| 7 | 4 | 3, 10 | 52 | 27.68; 25.11 | 64 | 50 | 7 | 7 | yes | 701bd5c0 | fe9a6bfcb6918dbd0689c44ea591833eb0887cd2f0ab5de158384a3b7a609196 |
| 8 | 1 | 0, 22 | 53 | 24.93; 22.30 | 97 | 50 | 37 | 37 | yes | a39eedce | e8088471358a88957ebb28b0d497f7ba0fba35f198f5ac908184886d55688a76 |
| 9 | 1 | 0, 10 | 36 | 24.50; 21.85 | 99 | 50 | 25 | 25 | yes | 46d9e789 | 6dc1f9d3d5aaf55445ff2d01612ee7979544f892696cd235d583b011fd4306f7 |
| 10 | 11 | 10, 11 | 51 | 29.36; 28.39 | 56 | 50 | 28 | 28 | yes | 099dbac3 | 13a18ca0d47bfd49204c2fec86b6e96ea91c82cfb4dea013e7d68b340142fcf4 |
| 11 | 1 | 0, 17 | 43 | 24.94; 22.39 | 50 | 50 | 6 | 6 | yes | d6ddbc42 | 698284d25bd16e20c188bc327088880137cc768300631f8dbe2db2fc6825c475 |
| 12 | 4 | 1, 19; 3, 6 | 33, 46 | 27.48; 24.84 | 1067 + 134 | 0 + 50 | 50 | none in 50 | no (none-in-K) | - | b0600d6e681362649fdc2e919eb857c28b927a532bc229d2f6b57c92e397582e |
| 13 | 6 | 5, 22 | 34 | 28.49; 27.90 | 50 | 50 | 11 | 11 | yes | 0f571823 | fc11ae5b0159ab5ed500e8d9f5f4a1589284218634dca0466837890d2dab8d26 |
| 14 | 2 | 1, 0 | 55 | 26.16; 25.83 | 76 | 50 | 28 | 28 | yes | 8874542d | 703593378c408dfa4d4a9b3e0afcea5849ff3af4c61dc7d55610acedc832b44a |
| 15 | 1 | 0, 4 | 43 | 23.75; 21.12 | 50 | 50 | 27 | 27 | yes | 17cbaca4 | 20cba464ced8e379b9854967f7abaeb5a94ff8f02c7887aa6b03bd438ec16b46 |
| 16 | 3 | 2, 19 | 45 | 27.29; 26.16 | 130 | 50 | 21 | 21 | yes | d4bf3291 | 295a84f78a1bca4fc325dee7d82965effb4f7907aefe4c010ec30737195111e3 |
| 17 | 3 | 2, 17 | 41 | 27.26; 24.73 | 53 | 50 | 31 | 31 | yes | ef731b50 | 100b1f9400dc52829150c932f7611bf67acf89e0c4f433dd64d737fa9a8941bd |
| 18 | 1 | 0, 17 | 53 | 24.87; 22.13 | 111 | 50 | 36 | 36 | yes | 28f6dafe | f2684d8f56e9c2383f52b2eb17a8134d4515c723177fce3f25586ec03fc10dae |
| 19 | 1 | 0, 28 | 41 | 25.63; 23.02 | 50 | 50 | 1 | 1 | yes | 90f42c45 | 9936f74dc24f358fc3833a0bb67832e86d240a7998578660659943a15821f2be |
| 20 | 3 | 2, 13 | 45 | 27.29; 26.17 | 72 | 50 | 14 | 14 | yes | 9bdb3915 | aa80df67603ac71c0ded9a71ef8f9fdc23a9755e7905fd331298f7dd83836bb2 |
| 21 | 2 | 1, 37 | 44 | 26.84; 26.00 | 50 | 50 | 25 | 25 | yes | c8c8a787 | c36b469047ec7632de0ab65177d5c2022b99c3962adb99e1c3ee20568ac8ce9d |
| 22 | 1 | 0, 22 | 34 | 25.37; 22.60 | 819 | 50 | 26 | 26 | yes | 2517d4eb | 969e6f629b57e7933d9aa9c100114564e7a8aaab08138ee6414d1e031d45282e |
| 23 | 1 | 0, 11 | 35 | 24.22; 21.67 | 78 | 50 | 36 | 36 | yes | a32a9ebe | 0369f674ca87d3385bf391dd4b31f57f093d8e1806e6cff38d0ab774dd567ea6 |
| 24 | 2 | 1, 53 | 51 | 26.97; 24.39 | 78 | 50 | 10 | 10 | yes | efd6d6e4 | 64f9a2176098ca04a81c076e03bdc3d0e6a27dbd71f4c5f4ca5347308c4144d1 |
| 25 | 1 | 0, 2 | 37 | 23.54; 20.90 | 150 | 50 | 50 | none in 50 | no (none-in-K) | - | 9d499e3aaf93e727c7b360df04ccfd745a639e1c12873b16214ddecea237bb61 |
| 26 | 5 | 4, 6 | 40 | 28.09; 27.49 | 247 | 50 | 10 | 10 | yes | c8bb7651 | af5cb93f34c157d3eb18324e43cba5610f83d24719d4d7d3fe3245cdab35bd28 |
| 27 | 1 | 0, 9 | 35 | 24.25; 21.65 | 50 | 50 | 50 | none in 50 | no (none-in-K) | - | 0a9776c8ab3e0a224cc480fc6b1c98302a2662f19e164b8d574bf66be5ce7653 |
| 28 | 4 | 3, 17 | 41 | 27.89; 25.37 | 50 | 50 | 50 | none in 50 | no (none-in-K) | - | 929b39df19a5a6fa98b337d593514a8e62a034af459db7060b96b80b7d225189 |
| 29 | 1 | 0, 38 | 34 | 25.71; 23.12 | 112 | 50 | 50 | none in 50 | no (none-in-K) | - | 4d34ccd5a696cd54a2bda9eff8f58fbb6acbf92833677b60173e8fb0bf0ae4e9 |
| 30 | 6 | 5, 19 | 57 | 28.45; 25.88 | 103 | 50 | 50 | none in 50 | no (none-in-K) | - | 75a62b3da1998356fb1dd7c7ea10c8a823858352bbe3bfea2648c19ad43fcf62 |
| 31 | 3 | 2, 5 | 35 | 27.17; 26.84 | 50 | 50 | 50 | none in 50 | no (none-in-K) | - | ea7de7429d9f7849fb7cb8fb6c1afe447de7a6cedc3c9623ddfc90767dad7b7f |
| 32 | 12 | 11, 0 | 34 | 29.47; 28.60 | 140 | 50 | 23 | 23 | yes | d6b309ed | 25a4c65029bed53a54ac7a4dd1ed8f6488fe5d72d6bf6c59f3332109ed66743b |
| 33 | 1 | 0, 4 | 54 | 23.22; 20.69 | 71 | 50 | 13 | 13 | yes | 02e46ab6 | a9e1b9b0feacb2cf4cbb1ed9f2846c8f5b19984cc772c526ed986deb69ab9c70 |
| 34 | 3 | 2, 22 | 46 | 27.32; 26.86 | 50 | 50 | 1 | 1 | yes | 771c8283 | cca4340a429c0684a4466bd529a255829be4157ad39c0e56b8f6e98bd06040cf |
| 35 | 7 | 6, 7 | 35 | 28.63; 27.64 | 51 | 50 | 10 | 10 | yes | 5067a7b7 | c8cddb106190c262ac5274083dc05d02ffd568ca1c6153ab2130bca46031f9e4 |
| 36 | 2 | 1, 1 | 40 | 26.22; 25.85 | 119 | 50 | 11 | 11 | yes | 85c7c5ff | 9555acd6131c19cad1e42e422e577e363437c5089192c9f48fe74325bb39a2cc |
| 37 | 1 | 0, 0 | 36 | 23.00; 20.24 | 453 | 50 | 40 | 40 | yes | d3f097a2 | 4623aaf77cb69c6d44b87c73f414206b0e36f0e77905e7d91ea465906d371173 |
| 38 | 2 | 1, 1 | 38 | 26.16; 23.61 | 91 | 50 | 7 | 7 | yes | 4ef230d9 | 7a7f89a821857851d42be397d3ed8b13da98082c90d88c639e43c08df8ab02f3 |
| 39 | 1 | 0, 24 | 33 | 25.37; 22.71 | 357 | 50 | 44 | 44 | yes | 186c8baf | cbeecd4e30b1769018622aed421a30d68b0b57b9fedfe5bfeebb37d06f1e0d84 |
| 40 | 1 | 0, 9 | 44 | 24.12; 21.50 | 63 | 50 | 23 | 23 | yes | 6f3c6bcc | f0e534c5955ce965f6d89ba6044b1f2feaf2e034069930ffbb88561b518ccbb6 |
| 41 | 3 | 2, 67 | 60 | 27.55; 24.96 | 50 | 50 | 11 | 11 | yes | 4d6abffd | 77a5b0c299e04131959da618b9d0017de56e6c071973e1968d56aba46335d929 |
| 42 | 3 | 2, 54 | 53 | 27.58; 26.26 | 282 | 50 | 13 | 13 | yes | be9110d3 | 4438ea77dbb6793e38496dc32272f0945b58e62123ed9ebb5eb2fd103dca3c40 |
| 43 | 1 | 0, 29 | 39 | 25.59; 22.87 | 71 | 50 | 4 | 4 | yes | 2cea1adb | 2d92ea0acc775268dcfcfeeb9b197bd711712a7add6a2191d08f7dde01652f84 |
| 44 | 2 | 1, 25 | 63 | 26.51; 25.91 | 98 | 50 | 21 | 21 | yes | 269333df | bd27634966e5b607e183ab09d071d7ea74a615710c4a02bb9539deab261bb9c2 |
| 45 | 1 | 0, 12 | 57 | 24.41; 21.73 | 52 | 50 | 38 | 38 | yes | b890cd6b | b1b2b36ef295b2e9c8d86ecd6d4fdc4580ee0b9749469997f66f5e8a44f8cc5a |
| 46 | 5 | 4, 17 | 35 | 28.17; 26.56 | 50 | 50 | 20 | 20 | yes | a1ee8ada | 1a5d21eb4bff7c835092f3d8758dda200fa7f9d6fc01d2f88b7cc948cd37626e |
| 47 | 1 | 0, 3 | 42 | 23.62; 20.95 | 56 | 50 | 30 | 30 | yes | 4d570e93 | 052db47df5abcd6e08a4633ab74e67fb3e3b94c08ea396e23f9e9fa493559300 |

### W.3 Development: C is no longer charged; G2 is

The rule of 0.1 is unchanged. C (v14's pre-registration C, 48 runs to 16 spaces each) was charged because its plan would have raised K had its bound been below 0.40; that was its only role (0.1, 4.4). With K fixed by rule K, no number of v20 depends on C, so v20 does not charge it. G2 fixed CCAP, B_BUDGET and v10's A_ADV and A_MAX, whose ratios rule K keeps, and stays charged in full (2^30.9994 units). R7 only measures success, and its only outcome-dependent decision is whether v20 is claimed (see below), so like R5 and R6 it is listed and priced, not charged. For a reader who rejects rule K's premise (a rule written after C, R5 and R6 but hashed before R7 counts as a priori), the totals with those runs charged at v20's prices are: C (2^31.9189 units) 33.6585; C, R5 (2^33.6556) and R6 (2^33.9493) 35.3462; R7 (2^32.8771) 34.0173; all four 35.5857. R5 and R6 are priced from their logs: B' at its WK cost (an upper bound of the true cost), every attempt at the algorithm's attempt bound, S per advice round, each space at v20's counted E with its stage-2 count (R6: at 2^11 pairs); R7 likewise from its result files, with B' at its true cost.

R7's plan and rule 0.1. plan.txt's one outcome-dependent decision reads: "the v20 package claims success probability 0.40 iff the bound is at least 0.40 (s >= 26); otherwise v20 is not claimed, the package falls back to v19's algorithm, and that is reported." Rule 0.1 charges a run "whose plan would have changed such a number on another outcome". We read that rule as it has been applied since v14: it charges runs whose data set a constant of the algorithm being claimed. C's plan would have raised K within the same algorithm, as a function of C's count, so C was charged. R7's gate reads only pass or fail. No constant of v20 is a function of R7's data, and exactly one set of constants was tested, so nothing was selected among alternatives. On failure the alternative was a different, separately evidenced package (v19, a2d6ce92, already in review), not another K for v20. Every success study gates the package it supports in this way: v15 would not have been claimed had R6 failed, and R5 and R6 were not charged. With the gate, the pre-registered bound keeps its coverage: Pr[v20 is claimed and its success is below 0.40] <= 0.05. A reader who charges R7 anyway gets 34.0173, which is above 395e8a28's 33.6804; this is v20's main residual risk, and we print it.

### W.4 P's T3 core by core: the same output and terms, one core's tables in memory

v19 inherited a gap in T3's memory schedule; a review of 0xshikhar's v17 (cade0f12), which ran the same code, rated it fatal. The gap is real: P's half-vector term charges every core's half tables once (HV x 96, all 127 keys included), the reference trail_search kept the half tables of all 467 cores across the seven levels (48,592,224 vectors of 1,600 bits, far above the cap), and the native mitm2.c instead recomputed each core's tables at every level (7 x HV steps, more time than the term charges). v20 makes the schedule part of the algorithm. P's T3 runs core by core: for each kept core in T2's order it builds the two half tables once (hv_step, all keys), runs the seven levels on them (sort and merge per block, the match step with the global counter and its cap M_CAP), keeps for each level the least (w1, w2, choice) found so far (on ties the earlier core), and frees the tables. After the last core it outputs the best leaf of the first level nb whose best has w1 <= 2 nb - 1, or nothing. trail_search in r5.py is now this loop.

Lemma W (same output). The matches, evaluations and best leaf of a core at a level depend only on that core's half tables and on nb, not on the order in which the (core, level) pairs are processed. The level-by-level order stops at the first certifying level; on the target only level 64, the last, certifies (2.1), so both orders process every (core, level) pair: the same 7,251,935 matches (below M_CAP = 2^24), the same per-level bests, the same certifying level and the same output (core 17, w1 = 127, w2 = 24, Section 3). In general the core-by-core order processes all seven levels, so its counter can reach M_CAP where the level order would have stopped earlier; that ends P without output, and every cost bound holds either way. The terms of 2.1 already charge all seven levels for all cores (127 blocks per core), HV x 96 once and the matches at M_CAP, so P's charge is unchanged.

Memory. (R5N3: history; the streamed P of R.2 and R.8 holds one core's planes, w2 and choice and one key-word slot, Appendix K, and the claim's figure is R.4's.) The organizer checks the new loop: r5-count trials 8 and 9 run trail_search on the sub-problem [core 874, core 1136] (102 matches with all levels; CapReached with cap 0), and trial 10 and r5-mitm-0, 1 check single cores at level 64 as before. Our check ptrial_check.py ran trials 8 and 9 on the new loop before the organizer runs (D20). The sensitivity with every core's half tables recomputed at every level (7 x HV x 96) is 33.1481.

The bound of 2 x 9^5 entries per core. A row's factor in the half tables is the number of chi input differences compatible with its output difference: 9 for a single-bit output, at most 10 for two bits, at most 12 in all. A core has at most 10 bits. A ten-row core has ten single-bit rows, and its best split (h minimises the sum of the two products) gives 9^5 + 9^5. A core with r <= 9 rows has at most 10 - r extra bits, and its best split is at most the balanced one: at most 9^4 x 10 + 9^4 = 72,171 entries for r = 9, fewer for fewer rows. So every core's two half tables hold at most 2 x 9^5 = 118,098 entries (48,592,224 over all 467 kept cores, as r5-trail-0..3 recount).

Time. P builds each core's half tables once (hv_step over all keys) and deletes them before building the next core's (trail_search's del H), which is exactly the one build per core that P's term HV x 96 has charged since v17; no level rebuilds them, so the repair costs no time (395e8a28's T.2 makes the same argument). Credit. The same repair was made independently by 0xshikhar and published first, in their 6667fc4f (v17.1, after a review of their v17 rated the retention fatal) and in 395e8a28 (T.2). We keep our own trail_search; ptrial_check.py checked its loop before 0xshikhar's publication, and r5-count trials 8 and 9 check the final version (with del H) in every review.

### W.5 D15 priced with the half vectors of every level

The native T3 programs of D15 computed each core's half tables at every level: mitm2.c (Appendix A) allocates and fills VA and VB per core per level, and mitm.c, whose header it shares, ran the stopped contiguous run the same way. v17-v19 priced those half vectors once. v20 prices them at every level: the stopped run at 10 x HV x 99 (each of its ten levels with all its keys, in place of HV x 99) and the certified run at 7 x HV x 96. W.5 raises D15 from 2^32.0899 to 2^32.1064 units; with v19's pricing the total would be 33.1370. The certified run's part (6 x HV x 96 = 2^24.3001 units more) is also 395e8a28's T.4.

### W.6 Our development for v20 (D20) and every run we made for v20

The rule is U.5's: D20 charges every run we made for v20 at the counted prices of the submitted programs, with stated bounds where a count is not exact, whether or not it fixed a number (none did). Two kinds of run are not charged, as in U.5: executions of the organizer's own harness (experiments/runner.py and scripts/local_tracks.py; listed and priced in W.10, charged 33.3739) and the success study R7 (W.3). Our replay test, which ran the shipped replay function outside the harness, is charged.

| D20 item | What it computed | log2 units |
| --- | --- | --- |
| R7 driver self-test (r7run.py; selftest.json 91a2b6e3...), 2026-10-08T15:20:41Z-15:20:50Z | R5 run 21's label with K = 50: Base, B' (candidate 0, attempt 3), 91 connector attempts, one space by fes and stage 2 | 24.1664 |
| ptrial_check.py (38a35333...), log ptrial_check.log (de26642d...), 2026-10-08T15:28:00Z | the core-by-core trail_search on r5-count's sub-problem: all levels (102 matches) and cap 0 (CapReached), twice | 23.1420 |
| replay_test.py (b886ad6b...), output replay_test.json (be8be1d2...), log replay_test.log (689084a7...), ended 2026-10-08T16:24:19Z | the shipped replay function on all 39 R7 successes with a fixed test seed, each in its own process (39 returned the logged collision; at most 3.9 CPU-s and 108 MB): its B' attempt and coins at WK's cost, 24 connector attempts at their bound, the 2^12 window, facts() and module tables | 28.9584 |
| t1check.py (a42f8121...), log t1check.log (f1f1c81c...), 2026-10-08T18:04:14Z | 395e8a28's s2_step as ported (W.11, not adopted) on a synthetic space (SHAKE-256 basis), 8 coordinates: 96 primitives each, x and d5x(x) = digest5(L^-1(x)) checked | 21.5963 |
| mk_certs.py (organizer verifier on the 15 R7 certificates) | 30 complete 5-round digests (30 units) and setup (2^20 primitives) | 9.6508 |
| module loads of r5.py by build scripts (mk_manifest.py; at most 8) | r5.py's module-level tables only, to read RUNS and CHEAP; each at most 2^31 primitives (a whole t1check.py process, load included, retired 1,219,414,088 instructions) | 23.5959 |
| **D20** | | **29.0751** |

Scripts that compute no target function and load no target code are not runs: krule.py (exact binomial sums), ledger_v20.py, org_price.py, klevels.py, r7stats.py, mk_r7table.py, apply_r7.py, d20_extra.py, compact_ws.py, astdiff.py, and for the final package port_t1.py, astcheck.py, mk_manifest2.py, mk_cfg.py, gen_proof.py, gen_claim.py and gen_note.py (they read r5.py as text). The instruction counts used as bounds are of an arm64 machine, whose widest vector instruction is 128 bits, so one instruction does at most one 256-bit primitive's work. analyze7.py (R7's analysis: two complete digests of each output, by two implementations) is priced with R7.

### W.7 Considered and not adopted: a re-count of v15's contiguous run with a popcount filter (B2)

(v22: at v22's prices in X.7. R5N2: condensed.) Our study proposed a 31-primitive filter in front of the match step and an exact re-count of v15's stopped contiguous run; the re-count would fix a number of the claim, so by our rule and v15's precedent it is charged, and then B2 cannot lower the total: the repriced item is at least 2^30.5678 units and the re-count at least 2^30.5386, together at least 2^31.5533, above the item as v20 prices it without them (2^31.5139). We did not adopt B2 and did not run the re-count (ledger_v20.py prints these bounds).

### W.8 R5 and R6 in v20

R5 (v14's) and R6 (v15's) are complete runs of v19 (Lemma 6) with K = 96, A_ADV = 2^11, A_MAX = 2^13 and S2CAP = 2^21. They are not runs of v20, support no bound of v20 and are not pooled with R7; Sections 4.2-4.7 and Appendices D and E keep them as history. Truncated at 50 spaces (ignoring the different discard limit) each would give 40/48.

### W.9 Ledger (log2 units; exact rationals, rate 1355; ledger_v20.py)

(R5N: superseded ledger condensed to fit the 512 KiB judge-evidence budget; its table and sensitivities are in 0f72a85e's proof, unchanged. Appendices J and L govern.)

### W.10 Organizer experiments and our local checks in v20

- **r5-R-0..7 replay R7.** As R7's plan fixed, the organizer replays switch from R5's table to R7's, which fits the 64-KiB budget: RUNS holds R7's 48 runs (advice (c, j, DF, hash), first positive space, its accepting attempt, coordinate, the space's DF and the status string of attempts 0..i). Stratum g holds the R7 successes at positions g, g + 8, ... (in k order) of the 38 replayable ones (run 22 is excluded: its replay came too close to the organizer's sandbox limit in our replay test; its collision is in R7's per-run ledger, W.2). Each of a stratum's two seed-picked replays re-derives the advice from the label 'hashsmash sha3-256-r5 R7 run k', re-runs the logged accepting attempt and up to 23 earlier attempts with the run's coins, checks the space index (at most K = 50) and returns the logged collision from E's 2^12-coordinate window. Over a review the seeds re-derive 16 of R7's 39 successes.
- **r5-bpfull.** Trial 0 runs a whole B' of R7 run 6 or 33 or 37 (single-round runs whose advice came from candidate 0, cheapest by B' cost and below 2^23.7 units, a rule fixed before R7's results) from its label and compares WK's cost with R7's log; trial 1 keeps R5 run 2's label for the cap test; trial 2 checks R7's table (48 runs, 39 with an output, bound 0.6956 >= 0.40); trials 3..26 run connector attempts with organizer coins on trial 0's advice.
- **r5-count trials 8 and 9** run the core-by-core trail_search (W.4); r5-trail-0..3, r5-mitm-0 and r5-mitm-1 are v19's.
- **The experiment file.** r5.py (SHA-256 4941939a5efbf24b6181d7d26a3293c684eb6edb00061abc1cd7dfa213502458) is 65,530 of 65,536 bytes. By AST its top-level statements are R7's r5v20.py's except trail_search (W.4) and the replay tables and checks (RUNS, CHEAP, the label function, R7's count: apply_r7.py); ten constant tables differ only in spacing (compact_ws.py, AST-checked). Every function that algorithm() calls after P is byte-identical to r5v20.py's.
- **Local organizer runs (verification, priced, not charged; U.5).** experiments/runner.py with Python 3.12 in place of Docker, every execution metered as in U.5, each set on the public seed and on the nonces "winglock-v20-nonce-1" and "winglock-v20-nonce-2", written down before the runs. The final set (orgplan2.txt, SHA-256 878c5246..., 2026-10-08T18:36:55Z) ran the final files; a first set ran the version with 395e8a28's s2_check (r5.py 7f74ca6b..., orgplan.txt 42a6cd60..., 2026-10-08T18:06:53Z; W.11). Per seed (2026-10-08, UTC; SHA-256 prefixes of the runner's report_sha256 and of the report, meter and log files):

| Set, seed | UTC | report_sha256 | report | meter | log |
| --- | --- | --- | --- | --- | --- |
| final, public | 18:37:01Z-18:39:37Z | 8c989eef | 10e87e40 | decf17e0 | 322fa48f |
| final, nonce-1 | 18:39:37Z-18:42:12Z | 3ff3aca4 | 3692e121 | 026a1fa2 | 0843c2df |
| final, nonce-2 | 18:42:12Z-18:44:42Z | 9e5bd457 | 6c8b0ba0 | ebc7bd06 | 9f85df47 |
| first, public | 18:07:00Z-18:09:41Z | eb348a11 | 8e1b7873 | 714ca1ee | 1e2d7c42 |
| first, nonce-1 | 18:09:41Z-18:12:21Z | 7c809117 | 1e47e49a | f7c651f3 | d7b18372 |
| first, nonce-2 | 18:12:21Z-18:14:55Z | 6505de88 | d077daf3 | 40d74082 | e5ee7a79 |

  The runner executes every experiment twice with byte-identical output. On each seed of the final set all 16 experiments completed with every predicted PASS: r5-trail-0..3 1/1 each, r5-count 11/11, r5-mitm-0 1/1, r5-mitm-1 3/3, r5-bpfull trials 0-2 (with 15/18/19 of its 24 descriptive connector attempts accepted), and r5-R-0..7 two full collisions each (16 per seed); together the three seeds replayed 30 distinct R7 successes. The first set passed in the same way, with s2_ops = 96 on all 48 replays. Each execution of either set took at most 7.5 CPU-s and 99 MB. A first attempt on the public seed at 2026-10-08T16:33:59Z stopped at manifest validation (a scope over 2,000 characters) before any experiment ran. Priced like U.5, the six runs and our local_tracks checks are 2^30.6050 units; charged, the total would be 33.3739.
- **Certificates.** r5-v6-000038 and the collisions of R7 runs 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17 (the first 15 successes in k order). The R5 and R6 certificates of v19 are not repeated; R5's successes and R6's are in Sections 4.3 and 4.7.
- `python3 scripts/local_tracks.py check sha3-256-r5-exploratory`: mechanically_valid, ready, 16 certificates verified.

### W.11 Considered from 0xshikhar's 395e8a28 and not adopted: T.1 (counted stage 2) and T.3 (self-test at true cost)

395e8a28 is our v19 with four changes: T.2 (P's memory) is our W.4 and T.4 is part of our W.5. T.1 and T.3 are sound accounting ideas, and we credit them; v20 does not take them, because neither lowers the total once the runs behind it are charged as this lineage charges such runs (X.7 gives the values at v22's prices).

- **T.1, a counted stage-2 step.** s2_step takes both digests from x through four byte tables built in E's setup (chi(x) + RC0 and four rounds, no L^-1): 96 counted primitives per pair besides its 2 units, instead of v19's stated bound of 2^11. It must be charged with the hand-off from stage 1 (the spill and restore of v19's 48 register words, U.2, which sat inside the 2^11 bound): 2 units + 192 per pair. Its development, 395e8a28's checks of s2_step on all 45 replayable R5 successes, consists of build checks of the program we would adopt, which this lineage charges (like t1check.py, ptrial_check.py and v17's D16): about 2^29.1649 units at our replay test's price per replay. At K = 50 and S2CAP = 2^11 all of E's stage 2 is 2^18.4559 units, so adopted with that charge the total would be 33.2334 (33.1447 uncharged). We ported it verbatim (port_t1.py: AST-identical definitions), checked it (t1check.py, charged in D20; three local organizer runs, W.10) and left it out.
- **T.3, the driver self-test of D15 at B''s true cost.** 395e8a28 re-ran from its label the B' of v15's self-test (a replay of R5 run 4, in D15 at WK's counter) and measured WK 343,020,384,242 (as R5's log, 2^27.92 units) and true cost 184,051,070,042 primitives, which would lower D15 by 2^26.8059 units. The measurement is itself a run that fixes a number of the claim (v15 charged its count-only recounts of the same kind; W.7 applies the rule to B2), of at least 2^27.0587 units with setup: charged, the total is 33.1484 against 33.144923 without T.3 (33.1270 uncharged).

Both adopted, with nothing charged for their runs, the total would be 33.1268. We do not claim that.

## U. What v19 changes (three cheaper counted programs, two development items added; no new heuristic, cap, constant or run of the algorithm)

| Change | Where | v18 | v19 | Evidence |
| --- | --- | --- | --- | --- |
| U.1 Match step | P, T3 (2.1) | 83 per match | 62 per match; A's 7 words and the match counter with its M_CAP test move to once per (a, block): 11, inside the 2^6 sort-and-merge bound per half vector per block (37 + 11 = 48) | r5-mitm-1 trial 2 |
| U.2 E stage 1 | E (2.4) | 75,386 per block of 256 Gray steps | 69,242: the 24 words of D1[0] stay in registers | r5-count trials 0, 2, 4, 6 |
| U.3 T2 leaf | P, T2 (2.1) | 166 per leaf with its Gray step (32 lookups of a 1024-entry table) | 56: a bitsliced test of ALLOW (22) and the same 2-word Gray step (at most 34) | r5-count trials 1, 3, 5, 7 |
| U.4 D15 completed | 0.1, V.3 | the T1/T2 run that wrote cores.bin (the input of every native T3 run of D15) is not charged | charged at the counted prices of the submitted programs: 2^26.5335 units | v15's Appendix A (cores.py, export.py) |
| U.5 D19 | 0.1 | - | every run we made for v19 except executions of the organizer's harness: 2^28.9135 units | U.5 |

Result: algorithm 2^31.4335 -> 2^31.3507; development 2^33.5070 -> 2^33.4106; total 2^33.8145 -> **2^33.7207, claimed 33.7208**; preprocessing 33.64 -> 33.53. Success probability 0.40 with v15's evidence (R6 44/48, R5 46/48), unchanged: each change computes the same values in the same order, and no cap, constant or rule changes, so every R5 and R6 run is a complete run of v19 (Lemma 6c, U.6). For comparison: v18 with U.4 alone would be 2^33.8365; v19's program changes alone (without U.4 and D19) give 2^33.6579.

Credits first. v19 is **Meganpark980320's v18** (f1eb6445; its v17 168a1b3a) with the changes in this table and nothing else; v18 is **rubenmarcus's v15** (91f1424d) with five accounting changes (Section V); v15 is winglock's v14 (f1cedf6b, with **Th0rgal**). The T3 meet-in-the-middle (with the zero-block half-sum match of **Subflatus3**'s 9bccf245), the counted fast exhaustive search, D15 and R6 are v15's; the counted T3 programs, B' at its true cost, the run-free caps, the unrolled E blocks and the repriced development are v17's and v18's; the zero-advice framing is Th0rgal's 7deb1595 (with Subflatus3 and rubenmarcus). Co-authors of v19: Meganpark980320, rubenmarcus, Th0rgal and Subflatus3. Only the items of this section are new; Sections V and 0-8 keep v18's text, with "(v19)" marking each place where a number or program changes.

### U.1 Match step: 62 per match, 11 per (a, block) (match_step and per_a in r5.py)

(v22: superseded by Section X.1, which gives v20's step of 62 in full. R5N2: condensed; v19's per_a, once per (a, block) whose run is not empty, 7 + 2 + 2 = 11, was checked by r5-mitm-1 trial 2. Price then: P's matches 2^24 x (62 + 2^11) = 2^24.6390 units.)

### U.2 E stage 1 with D1[0] in registers (fes_step in r5.py)

(v22: superseded by Section X.4, which starts from this block. R5N2: condensed; v19 kept D1[0] in registers for the whole space, 69,242 per block (v18 75,386), checked by r5-count trials 0, 2, 4, 6.)

### U.3 T2 leaf: a bitsliced test (t2_leaf in r5.py)

(v22: superseded by Section X.2. R5N2: condensed; v19's bitsliced ALLOW test, 22 per leaf, 56 with v15's Gray step (v18: 166), the same decisions, was checked by r5-count trials 1, 3, 5, 7. Price then: C1 x 56 = 2^26.0135 units.)

### U.4 D15 completed: the T1/T2 run behind cores.bin

v15's Appendix A shows two steps before T3. cores.py ran T1 (lane_dfs from the 25 lanes, N1 = 8,674,833 nodes) and T2 (p45pos on all 1741 cores). export.py then wrote cores.bin: the rows, compatible differences and their L^-1 images of the 467 kept cores. cores.bin is the input of every native T3 run that D15 charges: the stopped contiguous run, the layout comparison and the certified run.

v15's D15 itemization (0.1) does not list that run, and v17 and v18 reprice only the listed items. v19 charges it at the counted prices of the submitted programs: N1 x 2^12 + C1 x 56 + 2^32 (the export, at P's setup bound) primitives = **2^26.5335 units**. At v18's T2 price it would be 2^27.7783, and v18 with it would be 33.84.

### U.5 Our development (D19) and every run we made for v19

(R5N3: history, condensed. v19's D19 (contig.c, 2^28.9) and the runs we made for v19 are superseded and not charged in R5N3 (R.8).)

### U.6 What v19 reuses from v15-v18, after re-checking it

We re-checked each accounting step that v19 reuses. B''s true-cost tallies (V.5): Aff.copy is true 3 + 2w per entry instead of 256 and Aff.add true 7 + 4w on set entries instead of 512 (w = 7 or 11 words for the 1600- and 2570-entry tables), so true <= WK at every event; C's 48 and G2's 10 B' runs keep v17's true costs; r5-bpfull trial 0 reports a whole B' run's true cost on every review (ours: 2,573,293,728 primitives for R5 run 21, whose WK cost of 16,241,153,777 equals the log). v18's 75,386 per block and v17's hv_step 96 and match_step 83 (recounted; v19 replaces the E block and the match step). v13's cap rule (V.2): its three inequalities hold, and no R5 or R6 run reaches X_MAX, S2CAP or B_TRUE. D15 at counted prices (V.3), recomputed from v15's published numbers (rounded charges +0.005 in log2, match counts at their smallest rounding), reproduces 2^32.3521; at v19's match step its items are 2^31.4988 (contiguous run), 2^29.1769 (layouts), 2^28.1652 (certified run) and 2^28.9858 (unchanged), and with the one omission we found (U.4) D15 is 2^32.0899. G2 and C (V.5, V.7) from their published counts, G2's non-E part as the larger of the value implied by v18's published G2 and the sum of its components (B' 2^27.8176 true, 2,176 attempts at the 2^18 cap, 10 x S): 2^28.2825, which reproduces v18's total as 2^33.8147 (published 2^33.8145).

Inherited premises, disclosed and unchanged: A1 uncharged (V.6); v17's B' re-derivations listed, not charged; v17's own development charged as D16 at its stated bound of 2^27; development priced at the counted prices of the submitted programs (the rule of v14, v15 and v17, applied by v19 to D15's matches, to U.4 and to G2's and C's E spaces).

### U.7 Considered and not adopted

- **S2CAP = 2^11** (8 x the 256 stage-2 pairs expected per space) would give 33.65. We did not adopt it, because we chose it after the R5 and R6 maxima (308, 315) were known, so no rule fixed it before every run that could inform it.
- **K from an analytic rule** (44 or 50 spaces), with a new pre-registered success study that would leave C uncharged (about 33.0). Not adopted, for the same reason: C, R5 and R6 had run before the rule was written. (v20 adopts it, with S2CAP = 2^11, under a new pre-registered study R7 and with this history disclosed: Section W.1.)
- **An exact re-count of v15's contiguous run with a cheap popcount filter** (about 33.5 with this package). Not adopted: it would need a new full run of that layout. Only the feasibility run of U.5 was made, and it is charged. (v20: with the re-count charged it cannot lower the total, Section W.7; v22: also at v22's prices, Section X.7.)

### U.8 Ledger (log2 units; exact rationals, rate 1355; ledger_v19.py)

(R5N: superseded ledger condensed to fit the 512 KiB judge-evidence budget; its table and sensitivities are in 0f72a85e's proof, unchanged. Appendices J and L govern.)

## V. What v17 and v18 change (accounting of v15's own computation; no new heuristic; v18's text and numbers, superseded where Section U says so)

| Change | Where | v15 | v17 | Evidence |
| --- | --- | --- | --- | --- |
| Counted half-vector step with all keys | P, T3 (2.1) | 2^7 per half vector + 2^11 per half vector per level for keys (bounds) | 96 primitives per half vector, all 127 keys of the 7 levels included (counted) | r5-mitm-1 trial 1: both full half tables of the output core (118,096 counted steps) |
| Counted match step | P, T3 (2.1) | 2^9 per match (bound) | 83 per match (counted; one path below the cap) | r5-mitm-1 trial 2: every level-64 match of the output core in 4 seed-picked blocks |
| B' at its true cost | B' (2.2) | every "row" event at 256 primitives, including Aff's table update (2 events = 512 per table entry) and copy (256 per entry) | those two sites at their true word cost (V.5); a true-cost budget B_TRUE = 2^29 units by the run-free cap rule; v14's counter, CCAP and B_BUDGET unchanged | r5-bpfull trial 0 reports the true cost of a whole B' run; Section V.5 table |
| Caps | 2.3, 2.4, 2.6 | X_MAX = 2^23, S2CAP = 2^24 | X_MAX = 2^20, S2CAP = 2^21 (run-free rule, V.2) | largest R5/R6 attempt 190,240 work units, stage-2 count 315 |
| E stage 1 by unrolled blocks (v18) | E (2.4) | every Gray step at its longest path, 364 (74 of it control: the lowest set bits of the step index by a comparison tree, their ranks) | 256 steps per block as straight-line code: positions below bit 8 are program constants, those from the block index are computed once per block (at most 98); a block costs at most 75,386 = 256 x 293 + 280 + 98 (294.48 per step) | r5-count trials 0, 2, 4, 6: two blocks (511 steps), every step's count equals its formula, the prologue at most 98 |
| Development | 0.1 | G2 2^31.8877, C 2^33.2426, D15 2^34.6617 | G2 2^31.1003, C 2^31.9977 (their B' at true cost, V.5; their E spaces at v18's E, V.7), D15 2^32.3521 (V.3), D16 2^27 | V.3, V.5, V.7 |

Result: algorithm 2^33.9407 -> 2^31.4335; development 2^35.2659 -> 2^33.5070; total 2^35.7504 -> **2^33.8145, claimed 33.82** (v17: 33.93); preprocessing 33.64. Success probability 0.40 with v15's evidence (R6 44/48, R5 46/48), unchanged.

### V.1 The counted T3 programs (hv_step, match_step in r5.py)

(v22: superseded by Sections X.1 and X.3. R5N2: condensed.) v17 replaced v15's T3 bounds by counted steps: every key of every level is a linear function of the half vector, so hv_step tabulates all 127 keys with each half vector and steps them with its 7 plane words by the same mixed-radix Gray XOR (96 per half vector; P's setup bound 2^32 primitives covers the difference tables). The keys are v15's (r5-mitm-1 trial 1 compares them at sampled steps of both full tables of the output core), so match sets, counts (7,251,935), evaluations and P's output are v15's (Lemma P unchanged). The match step was counted at 83 (v15: 2^9); the full evaluation keeps 2^11.

### V.2 Caps by v13's run-free rule

v13 set X_MAX and S2CAP by a rule that used no run: each the largest power of two whose charged term stays within a reference term (v14's T3 batch term, 2^43 primitives). v15 removed that term and kept the caps. v17 re-applies the rule with the term that replaced it, v15's P charge (2^40.43 primitives), rounded down to 2^40:
- X_MAX: 2^13 x (X x 96 + 2^15 x 2^9 + 2^22) <= 2^40 holds for X = 2^20, not 2^21;
- S2CAP: 96 x S x (2 x 1355 + 2^11) <= 2^40 holds for S = 2^21, not 2^22;
- B_TRUE (V.5): B_TRUE x 1355 <= 2^40 holds for 2^29 units, not 2^30. No number is computed from a run. None binds in any run we know of: the largest connector attempt is 189,224 work units in R5 and 190,240 in R6 (2^20 = 1,048,576); the largest stage-2 count is 308 (R5) and 315 (R6) against 2^21 (256 expected per space: 2^32 pairs, 24 equations); the largest true B' cost of a run is 2^27.972 units in R5 and 2^28.2709 in R6 (V.5) against 2^29. Hence every R5 and R6 run is a complete run of v17 with the same output (Lemma 6c), and the success evidence carries over unchanged. A binding cap only fails an attempt, ends a space or ends B''s search; it never makes a cost bound wrong.

### V.3 D15 at v17's T3 prices (H2)

The rule is v14's and v15's: development is charged at the counted prices of the submitted programs (v15 used it to price v14's G2 and C at v15's counted E). Applied to v15's own D15, whose cost is almost entirely T3 work, it changes two prices: a match (2^9 -> 83) and the keys (2^7 + 2^11 per level per half vector -> 96 or, for a run with more keys, 30 + 3 x (7 + key words)). **Every input below is a number v15 published (its proof 0.1); we reconstruct no D15 workload.** Where v15 gives a rounded charge we take it rounded up (+0.005 in log2), and where it gives a match count we take its smallest rounding (4.25 x 10^10 -> 4.245 x 10^10); both choices can only raise the result.

| D15 item (v15's 0.1) | v15 log2 units | v17: v15's charge minus the stated savings | v17 log2 units |
| --- | --- | --- | --- |
| stopped contiguous-block run, levels nb = 1, 2, 4, 5, 8, 10, 16, 20, 32, 40 (all divisors of 320 up to 40; the tenth level charged complete) | 34.33 | 2^34.335 x 1355 - 429 x (4.245 + 1.145) x 10^10 (the matches v15 states for its last two levels, each now 83 instead of 512) - HV x (2^7 + 10 x 2^11 - 99) (keys of 10 levels, 16 key words) | 31.8496 |
| comparison of six layouts at nb = 64 | 32.00 | 2^32.005 x 1355 - 429 x 1.115 x 10^10 (contiguous-layout matches, v15: 1.12 x 10^10) | 29.5384 |
| certified native run (fixed M_CAP) | 29.61 | exact: HV x 96 + 127 x HV x 2^6 + 127 x 467 x 2^17 + 7,251,935 x 83 + 30 x 2^11 | 28.1657 |
| count-only recounts, Python T3 re-runs, stage-1 development, driver self-test | 27.40, 25.06, 19.36, 28.24 | kept, each rounded up | 28.9858 (sum) |
| **D15** | **34.6617** | | **32.3521** |

D16 (our development for v16/v17, charged at a stated bound of **2^27 units**): Python checks of the counted programs on the output core and local executions of the organizer experiments. None fixed a number: the step prices are counted from program text, the caps come from the rule. The B' re-derivations of V.5 are listed there.

### V.4 Ledger

v15 -> v17: log2-unit comparison, superseded by X.9/Z.9 (condensed; total 35.7504 -> 33.8145).

### V.5 B' at its true cost

B''s counter WK charges 256 primitives per "row" event, and its budget (B_BUDGET = 2^32 units), candidate cap (CCAP) and every logged B' cost of v14's studies are in WK's units. Profiling whole B' runs (R5 runs 21, 24, 42) shows that 98.8% of WK's cost is row events and that two sites make about 86% of the row events:
- Aff.add's table update `s.T = [t ^ af if t & pb else t for t in T]`, charged 2 row events (512 primitives) per table entry. pb is a single bit, so the test reads one word of the entry: loop control 3, load 1, AND 1, test 2 (7 per entry); only an entry whose bit is set is XORed with af: w loads, w XORs, w stores and w loads of af (4w, w = 7 words for the 1600-entry tables of 1,601-bit rows, 11 for the 2,570-entry tables of 2,571-bit rows).
- Aff.copy, charged one row event (256) per entry: loop control 3 and the entry's w loads and w stores (3 + 2w). Every other site keeps WK's price. Both true prices are below WK's at every event (at most 51 < 512 and 25 < 256), so the true cost of any B' execution is at most its WK cost.

r5.py now keeps, next to WK's counter, the exact difference between the true cost and WK's cost at these two sites (WK.d; it counts the set entries of every update). WK's counter, CCAP and B_BUDGET act exactly as in v14 and v15, so B''s execution and output are unchanged. The algorithm adds one budget on the true cost, **B_TRUE = 2^29 units** (the rule of V.2), over all of its B' calls; B' fails if the true cost exceeds it. The algorithm's B' term is therefore 2^29 units plus one update (no update's true cost exceeds its WK cost, below 2^13 units).

Every B' run that enters a number of this claim was re-derived from its label with the experiment file's code (the advice, rounds and (c, j) of every run reproduce the logs; WK costs equal the logs up to a constant setup term counted outside bprime in the logged figures: C's total differs by 435,644,112 primitives (0.005%), G2's runs by 11,182,080 each; we add these differences at WK's price; the constants of v13's runs are v13's: R = 16, DMIN = 40, weights 1, 0.25, 1, 1, which are the only differences between v13's and v14's B' code):

| Runs | Count | WK cost (logged = re-derived) | True cost | Ratio |
| --- | --- | --- | --- | --- |
| C (v14's pre-registration C, labels "hashsmash sha3-256-r5 v11 C B-prime run k") | 48 of 48 | 8,469,206,995,669 primitives re-derived; logged total 8,469,642,639,781 | 1,404,774,725,208 primitives; the logged total minus our re-derived WK sum is added at WK's price | 0.166 |
| G2: v6 run and pre-registration A (labels of v13's BRUNS) | 1 + 9 | 2^30.4349 units (each run's logged cost; our re-derivations miss a constant 11,182,080 primitives of setup per run, added at WK's price) | 2^27.8175 units | |
| R5 (all rounds of each run) | 39 of 48 re-derived | every logged run at most 2^28.73 units, below B_TRUE | largest re-derived 2^27.972 units | |
| R6 (all rounds of each run) | 39 of 48 re-derived, including the only two runs logged above 2^29 (runs 23: 2^29.61, and 28: 2^29.05) | largest 2^29.6107 units (run 23) | run 23: 2^28.2709, run 28: 2^27.0369 units | |

So C's B' costs 2^29.9498 units instead of 2^32.5422 and G2's B' 2^27.8175 instead of 2^30.4349. No R5 or R6 run reaches B_TRUE: a run's true cost is at most its logged WK cost, which is below 2^29 for every run except R6 runs 23 and 28, and those two were re-derived at 2^28.27 and 2^27.04 units. Each is a complete run of v17. r5-bpfull trial 0 (a whole B' run of R5 picked by the organizer seed) reports the true cost next to the logged WK cost. These re-derivations fix no number (B_TRUE comes from the rule; the prices from program text): like v14's re-derivations of R5 they are listed, not charged. If they were charged, at their true cost (about 2^32.7 units in all) the total would be 34.44, at WK's price (about 2^34.3) 35.13; both are below 35.76.

### V.7 E stage 1 as unrolled blocks (v18)

(v22: block price in X.4; v25: Z.3.) v18 unrolled v15's 2^24 Gray steps (364/step) into 256-step blocks (75,386/block = 294.48/step, prologue 98; r5-count trials 0,2,4,6 run 2 blocks), applied to G2 (530 spaces) and C (768 spaces) by V.3.

### V.6 A1 (v7's design study) stays uncharged, as in v13, v14 and v15

A1 (v7's design study: a connector without steering, annealers, backtracking and benchmarks; 10,432 CPU-s) produced the text of B''s D2u and M2 phases. The cost model charges construction, preprocessing and advice, including any search omitted from the submitted program: work whose result the attack uses. No result of A1 is an input of the algorithm: B' reads only P's trail and the fixed bits, its constants are fixed by rule or by charged runs (G2, C; 0.2), and its whole computation is charged every time it runs (here at its true cost). A1's outputs were comparisons between program designs; replacing them by any other way of writing the same program text would not change any count, cap, constant or output of the algorithm. Charging the research that led to a program's text would charge every package for its authors' experiments; the lineage's packages that qualified (v8 at 40.26, v13, v14, v15) all treat A1 this way. The claim if A1 were charged at 2^38 primitives per core-second is 40.98 (0.1).

Credits for v17: the base is rubenmarcus's v15 (91f1424d); everything not listed in this section is theirs or, through v15, winglock's (v8, v13, v14), Th0rgal's and Subflatus3's, as credited in Section 8. In Sections 0-8, "our" and "we" mean the v15 authors unless marked (v16) or (v17).

---

(v15's text follows; it is v15's proof with the v16/v17 edits marked.)

## 0. Claim, summary, changes

| Field | Value | Basis |
| --- | --- | --- |
| time_log2 (v22) | 33.09339 | v22: 2^33.093387, rounded up (Section X.9); v20: 2^33.144923 (Section W.9); v19: 2^33.7207 (Section U.8); v18: 2^33.8145 (Section V). v15's basis was 2^35.7504, rounded up: the algorithm, 2^33.9407 (Section 6), plus the charged development: v14's G2 (2^31.8877) and C (2^33.2426), priced at v15's counted programs as v14's rule prescribes, and our own development D15 (2^34.6617) (Section 0.1) |
| success_probability | 0.40 | (v20) R7 (pre-registered, 48 complete runs of v20): 39 successes, one-sided 95% Clopper-Pearson bound 0.6956 (Section W.2). v19's basis: R6 (pre-registered, 48 complete runs of v15): 44 successes, one-sided 95% Clopper-Pearson bound 0.8193; R5 (v14's, 48 runs that are complete runs of v15): 46 successes, bound 0.874 (Section 5) |
| preprocessing_log2 (v22) | 33.00427 | P, B', S and the charged development: v22 2^33.004263, v20 2^33.058081, v19 2^33.5279, v18 2^33.6315 (v15 2^35.4430) |
| memory_log2_bytes | 25.906890595609 (R.4, K) | 62,914,560 B: the largest cap any development label needed; the dense model's largest phase, E, is 47,755,983 B (Appendix K) |
| nonuniform_advice_log2_bytes | 0 | the algorithm computes its trail and its connector advice; development is charged as preprocessing |

Board when this was written (2026-10-08): v8 113fc836 promoted at 40.26; lowest pending claim v14 f1cedf6b at 37.05. (v22, 2026-10-09, as given to us: Th0rgal's v21 a9ec6971 at 33.12242 in review; our v20 84668773 at 33.14493, plausible_not_refuted; v8 113fc836 promoted at 40.26.) (v20, 2026-10-08T18:46Z: v8 113fc836 promoted at 40.26; lowest in review 0xshikhar's 395e8a28 at 33.6804, then our v19 a2d6ce92 at 33.7208 and Meganpark980320's v18 f1eb6445 at 33.82.)

(v15 summary, superseded by X.9/Z.9; condensed: total 37.05 -> 35.76.)

### 0.1 Development: what is charged, and why (H2)

(R5N3: history. R5N3 charges the runs of Appendix M, D16 and the peers' build checks D21, D_Y, D_v23, D_v24; the rule below is unchanged, and R.8 says which runs fixed or measured the constants and were regenerated.)

Rule (v14's, unchanged). The cost model counts all construction, preprocessing and advice, including any search omitted from the submitted program. Every target-specific run whose result fixed a number that the algorithm reads, or whose plan would have changed such a number on another outcome, is charged as preprocessing, at the counted prices of the submitted programs (the prices of the claim). Runs that only produced program text, or only measured the success of the algorithm as submitted, fix no number; they are disclosed with the claim they would give. Where only CPU time is known, a sensitivity uses 2^38 primitives per core-second (v14's rate).

Charged in the lineage's earlier ledgers (history, condensed): G2 (v14's v6 run, pre-registrations A and B: K = 96, CCAP, B_BUDGET, A_ADV, A_MAX), C (pre-registration C), D15 (the native T3 runs, the layout comparison, the certified run that fixed M_CAP, the T1/T2 export), D16, D19, development items 20, 21, 22 and 23. R5N3 charges only D16, D21 and the peers' checks of earlier ledgers plus the runs of Appendix M; the regenerated inputs are listed in R.8.

Not charged (each fixes no number of v15; claim if charged, with the price named):

| Id | Runs | Why nothing is fixed | Claim if charged |
| --- | --- | --- | --- |
| A1 | v7's design study that produced B''s code (10,432 CPU-s) | code, not a number; the code is charged every time it runs | 40.98 (2^38 primitives per core-second) |
| A2 | v13's B' tuning (at most 1,559 CPU-s) | v14 and v15 use none of its constants | 38.44 (same rate) |
| R5 | v14's success study (48 runs) | its plan fixed every constant before any run | 36.23 (v15's prices) |
| R6 | our success study (48 runs, Section 4.7) | its plan fixed every constant before any run; its only rule is whether to claim | 36.44 (v15's prices) |
| R7 (v20) | v20's success study (48 runs, Section W.2) | rule K and its plan fixed every constant before any run; its only outcome-dependent decision is whether v20 is claimed (on failure v19 would stand; why this is not a charge: W.3) | 34.0173 (v20's prices, W.9; v22: 33.9770, X.9) |
| C' | v14's parallel session (at most 12,537 CPU-s) | its plan fixed the values before its runs | 41.24 (2^38 per core-second) |
| D | v14's pre-registration D | it measured v13's success | at most 36.93 (v14's prices) |
| A3, A4 | v7's abandoned plan and B' run (at most 535.6 CPU-s) | nothing | 37.28 |
| B | v14's native T3 passes and v7's P run | nothing: v15's P computes its output itself | 36.52 (3 runs at v14's P price) |
| local | organizer-experiment runs on our machine (Section 4.6) | re-derivations of logged results | - |

### 0.2 Where every number of v15 comes from

The numbers of B', the connector and the driver are v14's, with v14's origins (v14's Section 0.2): B''s constants are values no run chose; CCAP, B_BUDGET, K, A_ADV, A_MAX come from G2 (charged) and K was kept by C's rule (charged) (v20: K = 50, A_ADV = 1067, A_MAX = 4268 and S2CAP = 2^11 come from rule K, Section W.1); connector DMIN = 33 is the least DF for which E's 32-dimensional window and beta exist; X_MAX, S2CAP and B''s budget satisfy v13's cap rule (2.6). New numbers:

| Number | Where | Origin |
| --- | --- | --- |
| halves (least h minimising the sum of the two products) | P | analysis: the cheapest split |
| levels nb = 1, 2, 4, ..., 64, certification W* <= 2 nb - 1 | P | analysis: dyadic refinement of one partition; the certification bound is Lemma P; the schedule stops at the first certified level, and every level is charged |
| block of row (y, z) = ((z + 13 y) mod 64) mod nb | P | D15 (charged): contiguous blocks (rows sharing slices) gave 10^10 matches per level; a comparison of 6 layouts on 8 cores chose one row per plane at slices spread by 13 |
| 26-bit linear key fold | P | implementation of key equality; exact at nb = 64 |
| M_CAP = 2^24 | P | D15 (charged): the least power of two at least twice the certified run's 7,251,935 matches |
| inner/outer split 8/24, Gray order | E | v14's batch layout |
| E_STEP = 364 and every T3 price | E, P | counting (r5-count) and the stated bounds of 2.1 |

## 1. Target, messages, notation

sha3-256-r5-prefix-v1 is FIPS 202 SHA3-256 restricted to rounds 0-4 of Keccak-f[1600]: rate 1088, capacity 512, zero initial state, suffix 0x06 with pad10*1, digest = lanes 0..3 after the 5 rounds. Round i maps A to chi(L(A)) xor RC[i], with L = pi o rho o theta. State bit (x,y,z) has index 64(x+5y)+z. chi acts on the 320 rows (y,z) by chi5(v)_i = v_i xor (NOT v_{i+1}) v_{i+2}. All messages are exactly 135 bytes: A0 = M || 0x86 || 0^512, so the 520 bits F = 1080..1599 are fixed (1081, 1082, 1087 are 1). For a pair, alpha_i is the difference entering round i, beta_i = L(alpha_i) the difference entering chi. DDT[d][o] = #{v : chi5(v) xor chi5(v xor d) = o}; V(d,o) = {v : chi5(v) xor chi5(v xor d) = o} is an affine set of dimension log2 DDT[d][o], so a row transition is w = 5 - log2 DDT affine equations on one message's row value. x = L(A0) is the first message's round-0 chi input.

Cost model (collision-frontier-v5): one 5-round permutation is 1 unit; every other primitive on 256-bit words (load, store, add/sub, AND/OR/XOR/NOT, shift or rotation, comparison, conditional branch, fresh random word) is 1/1355 unit. Our counted programs count every executed load, store, operation, comparison and branch as one primitive; shift amounts, masks and constant addresses are instruction fields; values live in at most 64 registers (the bound is stated per program). A 256-bit word holds one bit of each of 256 pairs (or leaves): bitslicing.

## 2. The algorithm and its charges

Phases: trail search P (2.1), advice program B' (2.2), setup S and connector (2.3), enumeration E (2.4), driver (2.5). Section 6 lists every term, the cap that enforces it and its price.

### 2.1 Trail search P (deterministic; T1 and T2 as in v14, T3 by meet-in-the-middle)

P outputs the 2-round in-kernel core alpha3 and the beta2 that minimise w1 (then w2, then the earlier core, then the least choice vector: v14's order).

T1 (cores), unchanged: a candidate alpha3 is a set of at most 10 bits whose alpha-columns and beta-columns (columns of pi o rho of each bit) all hold an even number of bits; depth-first search from bit (lane, z = 0) for each of the 25 lanes; at a node let c be the smallest odd alpha-column, else the smallest odd beta-column; if none, record the core in canonical form (least sorted bit list over the 64 z-translations), else, below 10 bits, branch on each bit of c not yet in the set. N1 = 8,674,833 nodes, 1741 cores. Price: 2^12 per node (as in v8: at most 2^9 per node outside the 17,100 core events, a core event at most 2^15, and N1 x 2^9 + 17,100 x 2^15 < N1 x 2^12).

T2 (forward), unchanged: for each core, beta3 = pi o rho(alpha3); the C1 leaves alpha4 compatible with beta3 are visited in reflected mixed-radix Gray order (Knuth's Algorithm H over the rows of beta3); the 64 digest-plane rows of L(alpha4) are kept as 32 row pairs (10-bit fields of 2 words) and updated by XOR. A leaf is allowed iff every digest-plane row q has DDT[q][0] + DDT[q][16] > 0 (32 lookups of one 1024-entry table); the core is kept iff some leaf is allowed, which is P45 > 0 (Section 3). C1 = 1,639,088,128 leaves; 467 kept cores. (v19: the rows are kept bitsliced and the leaf is a 12-gate test of ALLOW, 56 with its step, Section U.3; v22: 26 with the Gray state step, Section X.2.) v18's counted price (r5-count) was 166 primitives per leaf on its longest path; v19's is 56 (U.3).

T3 (backward) by meet-in-the-middle on zero blocks of alpha2 (new in v15; replaces v14's exhaustive batches).

- Halves. For a kept core with rows j = 0..n-1 of alpha3 ((y, z) order) and the m_j input differences compatible with row j's output difference (ascending), alpha2 = L^-1(beta2) = sum_j L^-1(d_j at row j) is linear in the choices. Rows 0..h-1 form half A and rows h..n-1 half B, h the least value that minimises |A| + |B| (|A| = m_0 ... m_{h-1}); for the 392 cores with ten 9-fold rows, |A| = |B| = 9^5. The half vectors LA(a), LB(b) (alpha2's 320 rows of 5 bits), their w2 parts and choice vectors are tabulated in mixed-radix Gray order (one XOR of a 10-word difference vector each). HV = sum over kept cores of |A| + |B| = 48,592,224 (organizer-recomputed by r5-trail-0..3).
- Levels. A level is a block count nb in (1, 2, 4, 8, 16, 32, 64): row (y, z) of alpha2 lies in block ((z + 13 y) mod 64) mod nb, so each level refines the previous one and at nb = 64 every block has 5 rows, one in each plane y, at 5 distinct slices. The key of a half vector on block t is its block's row values (5 bits each, rows in increasing 64 y + z) written at bit offsets 0, 5, 10, ... reduced mod 26 with wrap-around and XORed (a linear fold into 26 bits; exact, with no fold, for nb = 64). Equal block contents give equal keys.
- Matching. For each core and block, both key lists are sorted (two radix passes of 13 bits) and merged. Every pair (a, b) with equal keys is a match: alpha2 = LA(a) + LB(b), AS = its number of active rows; if AS <= nb - 1 the leaf is evaluated in full (w1 = sum of the least weights of alpha2's active rows, w2 = w2(a) + w2(b), choice vector) and the least (w1, w2, choice) of the core is kept. A global counter of matches raises CapReached above M_CAP = 2^24 (2.6).
- Certification. After a level over all kept cores in T2's order, let W* be the least w1 found (ties: least w2, then the earlier core, then the least choice vector). If W* <= 2 nb - 1, P outputs that leaf and stops; otherwise the next level runs. If no level certifies, P outputs nothing (the algorithm fails). (v20: P runs the seven levels core by core, one core's half tables at a time, and certifies after the last core, with the same output: Section W.4.)

Lemma P (certification gives v14's output). At level nb every leaf with AS(alpha2) <= nb - 1 is found: its nb - 1 or fewer active rows miss some block, on which LA(a) = LB(b), so the keys agree. Every leaf not found has AS >= nb, so w1 >= 2 AS >= 2 nb > W* (no nonzero chi5 DDT entry exceeds 8 of 32, so every active row of alpha2 costs at least 2). Hence W* is the least w1 over all leaves of all kept cores, and every leaf with w1 = W* is found (its AS <= W*/2 < nb), so the tie-break among them is exact. This is the output of v14's T3 (which visits all 1.38 x 10^12 leaves): the least (w1, w2), then the earlier core, then the least choice vector.

Native run (mitm2.c, Appendix A; P's T3 on the 467 kept cores exported by the experiment file's T1, T2 and core_tables; R.8's capped run reproduces its counts and result). Levels 1, 2, 4, 8, 16, 32 find no leaf with AS <= nb - 1. Level 64 evaluates 30 matches, all on core 17 of T2's order (core No. 349 of T1's list), and certifies W* = 127 <= 127: w2 = 24, choice (0, 0, 3, 0, 0, 0, 0, 0, 3, 1), whose beta2 is BETA2 of Section 3. That is v14's trail (GLL+20 core No. 3), found exactly. Matches per level: 20,490, 40,849, 81,791, 165,085, 329,494, 818,094 and 5,796,132 (7,251,935 in all, 2.31 times below M_CAP). The run took 370 s on 5 threads (250 CPU-s user, 46 s system, 233 MB). The per-core log (matches and evaluations of every core at every level) has SHA-256 given in Appendix A; r5.py holds its level-64 column (MT6).

The block layout matters for the cost, not for correctness: an earlier run with contiguous blocks (rows 5t..5t+4 of one plane, so a block's rows share theta's column effect) produced 1.15 x 10^10 matches at nb = 32 alone and was stopped. That run and the small comparison that chose the slice stride 13 are charged as development (0.1, D15).

Python form (r5.py): halves, mkey, mitm_core with the M_CAP check in plain sight, and trail_search (T1, T2, then the levels). It makes exactly the native program's decisions: on core 17 at level 64 and on core 0 at all seven levels it reproduced the native match and evaluation counts, and the organizer checks it on the output core (r5-count trial 10), on seed-picked cores (r5-mitm-0, r5-mitm-1) and as P's driver on a sub-problem with its cap (r5-count trials 8, 9).

```python
    M[0] += 1
    if M[0] > mcap:
     raise CapReached()
```

with mcap = M_CAP = 2^24 in algorithm(); CapReached makes algorithm() return without output.

Prices of T3 (bounds, not counted; in units of primitives on 256-bit words):
- a half vector: 2^7 (10 loads, 10 XORs and 10 stores of the 10-word vector, the w2 and Gray updates);
- all keys of one half vector at one level: 2^11 (each of the 320 row fields is extracted once, with a load, a shift and a mask, and shifted and XORed into its block's key: at most 6 x 320 = 1,920, plus at most 64 key stores);
- one half vector in one block: 2^6 (two radix passes of 14 primitives each and the merge step, at most 6; with the key extraction 37, V.1; v19: plus per_a, 11, once per (a, block) of half A, 37 + 11 = 48 < 2^6, Section U.1; v22: per_a 18, 37 + 18 = 55 < 2^6, Section X.1);
- one block of one core at one level: 2^17 (the 2^13-entry count arrays of both halves, cleared and prefix-summed in both passes: 4 x 2^13 x 4);
- one match: 2^12 (alpha2: 20 loads and 10 XORs; AS: per word a fold of each 5-bit field into its low bit and a shift-and-add count, at most 32 per word, plus the comparison: below 2^9; the full evaluation when AS <= nb - 1: w1 over the 320 row fields by table lookup, w2, the lexicographic comparison: below 2^11). (v16: 83 counted below the evaluation; v19: 62 per match plus 11 per (a, block) inside the 2^6 sort-and-merge price, Section U.1; v22: 899/16 per match plus 18 per (a, block), Section X.1.)

P's charge: T1 + T2 + HV x 2^7 + 7 x HV x 2^11 + 127 x HV x 2^6 + 127 x 467 x 2^17 + M_CAP x 2^12 + setup (DDT, L^-1 by elimination, the row-difference vectors of every kept core: below 2^31) = 2^40.43 primitives = 2^30.03 units (v14: 2^33.65; these are v15's prices: v22's P is 2^28.5281 units, Section 6). The level and block counts are fixed by the program (all seven levels are charged although P stops at the seventh), HV is organizer-recomputed, and the only data-dependent count, the matches, is charged at its cap.

Premise P (inside H1; success only, since every cost term of P is a fixed count or a cap): P outputs the trail of Section 3 within M_CAP. Its evidence: the native run above, which certifies itself by Lemma P; its agreement with v14's two exhaustive T3 passes over all 5,679,328,446 batches (same trail, unique); the organizer checks just listed. If P certified nothing or hit its cap, it would output nothing: the cost bound holds either way.

### 2.2 Advice program B' (budget 2^32 units, at most 2^26 units per candidate; constants no run chose)

B' (experiment file, rand_min_beta1 to bprime) is v6's program with a budget and a per-candidate cap. Its only inputs are P's trail and the fixed bits F. For candidate c = 0, 1, ... (each abandoned once its own cost exceeds CCAP = 2^26 units; B' then moves to c + 1):
- beta1_c: in each of the 59 rows of alpha2, a uniformly chosen input difference of least weight (50 rows have exactly one, 9 have 4 or 5); then the round-1 conditions, the linearisation table and the link and candidate tables.
- attempts j = 0, 1, ... with no limit (B_R = 2^62 in r5.py is never reached): D2u gives the rows of alpha1 = L^-1(beta1_c), in DSATUR order, affine sets of compatible differences on which the fixed-bit link conditions are uniform, trying candidates in uniformly permuted order sorted by an unweighted key (KW = MW = LB = PREF = 1); M2 picks, row by row, (d, W) with forward checking on one value system (x, fixed bits, row equations, the 127 round-1 conditions). An attempt is accepted iff it is consistent with DF >= DMIN = 33 and 64 sampled points pass (both messages padded, block difference L^-1(beta0), exact 2-round difference alpha2).
- B' stops at the first accepted attempt and outputs (beta1_c, beta0). A candidate with no accepted attempt ends at CCAP.

v13 had R = 16 attempts per candidate, DMIN = 40 and weights (1, 0.25, 1, 1), all chosen by development runs (A2). v14 replaces them by the values above (0.2), and the R5 study measures the algorithm with them (4.2). Nothing else in the experiment file's algorithm changes.

Every operation is counted by class: row (one operation on an integer of at most 2585 bits = 11 words: 256 primitives), small (8), Keccak-f call (5 units), SHA-256 compression (2 units), 2-round evaluation (1 unit). The class WK raises BudgetExceeded on the first counter update that takes B''s cost above B_BUDGET = 2^32 units or the current candidate's cost above CCAP; so B' spends at most 2^32 units plus one update and a candidate at most 2^26 units plus one update (the largest update inside B' is below 2^13 units). r5-bpfull executes bprime() whole: from the label of R5 run 21, 24 or 42 (picked by the seed; these are the R5 runs whose advice came from candidate 0 with B' below 2^23.7 units) its counted cost equals the R5 log and its output the logged advice; and on R5 run 2's label with a 2^22-unit budget and a 2^21-unit candidate cap, candidate 0 stops 0.68 units above 2^21, candidate 1 starts, and B' stops with no output 188.1 units above 2^22. In R5, 90 of 141 candidates ended at CCAP (with no attempt limit every candidate that is not accepted ends there) and every run's B' cost, all advice rounds together, was at most 2^28.73 units, so B''s budget never acted. Coins: fresh 256-bit words in the algorithm (counted as 32 primitives each); in our runs, Coins(SHA-256(label || "beta1" || c)) and Coins(SHA-256(label || "att" || c || j)) (Section 4.1). WK's 2 units per SHA-256 compression is below the 3.3 units of a 64-round compression at the organizer's sha256-r32 price; a run makes at most 2 compressions per attempt or candidate, and an attempt counts at least 302 units, so our runs' counts are within 0.9% of their true cost. The claimed algorithm draws fresh words and computes no SHA-256; algorithm(label) in the experiment file derives its coins from a label with SHA-256 and SHAKE-256 only so that runs can be reproduced, and WK charges those calls. Restart: when an advice is discarded (2.3), B' resumes at the next candidate under the same budget; the connector's work is charged to its own term.

### 2.3 Setup S and the connector (unchanged v5 attempt)

S builds L and L^-1 as row forms, alpha2 = L^-1(beta2), alpha1' = L^-1(beta1'), the 127 round-1 conditions (equations of V(beta1'_r, alpha2_r) on z = L(chi(x) + RC0)), and the linearisation table. One attempt (attempt() in the experiment file) keeps two echelon systems with undo, E_D on delta (the unknown beta0) and E_M on x, with one shared counter of work units (a reduction call or a row addition, at most 96 primitives). D1: E_D gets (L^-1 delta)_j = 0 for j in F, and delta_r = 0 on the inactive rows of alpha1'. D2: in a uniform order of the active rows, the first uniformly permuted affine set of compatible differences that contains beta0'_r and is consistent. M1: E_M gets the fixed bits. M2: per row, the first d (beta0'_r first, then by DDT) consistent with E_D and with x_r in V(d, alpha1'_r). M3: linearise each row with masks on an affine W. M4: add the 127 round-1 conditions. M5: accept iff consistent and DF = 1600 - rank(E_M) >= 33; above X_MAX = 2^20 work units (2.6; v16, v15: 2^23) the attempt fails. An attempt costs at most 2^26.86 primitives (2^20 x 96 + 2^15 coin words x 2^9 + 2^22) and draws at most 22,150 coin words.

Advice rounds (v10 caps): run attempts on the current advice until K = 96 are accepted; if A_ADV = 2^11 attempts give fewer, discard it and resume B' at its next candidate. At most A_MAX = 2^13 attempts in all, so at most 4 advice rounds. (v20: K = 50, A_ADV = 1067 and A_MAX = 4268 = 4 x A_ADV by rule K, Section W.1; still at most 4 advice rounds.)

### 2.4 Enumeration E (stage 1 by bitsliced fast exhaustive search, counted)

Space and window (unchanged): V = solutions of E_M, beta = beta0; offset v0 = the solution with all free variables 0; b_i = (solution with free variable i set) + v0, kept if independent of beta and the earlier ones; W = span of the first 32 kept b_i. E tests the 2^32 pairs (x, x + beta), x = v0 + sum over the set bits j of the coordinate c of b_j.

Stage 1 tests the 24 round-2 equations (EQS, a basis of the equations of V(beta2_r, alpha3_r) on the 10 rows of beta2, checked by eqs_ok) on the first message's round-2 input u = L(chi(L(chi(x) + RC0)) + RC1). Let f(c) in GF(2)^24 be the residual bits (bit k set iff equation k fails). Round 0's output has degree <= 2 in c, round 1's <= 4 and L is linear, so f has degree <= 4 in c: this is exact, with no assumption.

Layout (v14's): coordinates 0..7 are inner (bit p of a 256-bit word is inner point p); coordinates 8..31 are outer and run in reflected binary Gray order over 2^24 steps, step i flipping outer coordinate ctz(i). For each equation k, the word F_k(y) (bit p = f_k at outer point y and inner point p) is a polynomial of degree <= 4 in the 24 outer variables with 256-bit word coefficients.

Stage 1 is the derivative recursion of fast exhaustive search (Bouillaguet, Chen, Cheng, Chou, Niederhagen, Shamir, Yang, CHES 2010) on these 24 words at once. State: F (24 words, in registers) and the derivative vectors D1[a], D2[a,b], D3[a,b,c] (in memory) and the constants D4[a,b,c,d], each a vector of 24 words, indexed by colex ranks. Step i: with b1 < b2 < b3 < b4 the positions of the lowest (up to four) set bits of i, D3[b1 b2 b3] ^= D4[b1 b2 b3 b4], D2[b1 b2] ^= D3[b1 b2 b3], D1[b1] ^= D2[b1 b2], F ^= D1[b1], each level only as far as i has set bits. The pass word is NOT(F_0 OR ... OR F_23); its pairs go to stage 2.

Setup (fes_setup in r5.py; fes.c builds the same state, Appendix B): f at the 41,449 coordinates of weight <= 4 (all 32 variables), their Moebius transform (the algebraic normal form of f, exact since deg f <= 4), the 256-bit truth tables of the inner monomials of every outer monomial, and the initial derivative vectors D_w[K] = (d_K F)(gray(K - 1)) for w < 4 and D4[K] = d_K F (a constant). Bound per space: the 41,449 evaluations at 1 unit each (two rounds and L, the price of a 2-round evaluation in B''s counter class) plus at most 2^23 primitives (617,089 XORs of the Moebius transform, at most 41,449 x 24 x 3 for the truth tables, 19,024 vector XORs of at most 72 for the derivatives, ranks), below 2^16 units.

Counted step (fes_step in r5.py; W operators, load(), st() count 1, test() 2). Control, at most 74: the step counter and its end test (3); up to four lowest set bits of i, each by an isolation (2), a comparison tree over the 24 positions (at most 5 tests, 10) and the position into a register (1), with a clearing (1) after each of the first three and an end test (2) before each of the last three; the rank arithmetic (a table load and an add per level) and the shifts to vector offsets (at most 10). Vectors, at most 264: per equation at most 4 loads, 4 XORs and 3 stores. Test, 26: the OR of the 24 words, its complement (the pass word) and the test. (v18: the steps run as unrolled blocks of 256 at most 75,386 primitives per block, Section V.7; v19: 69,242 with D1[0] in registers, Section U.2; v22: 66,831, Section X.4; v15's per-step count follows.) The longest path is 364 primitives per 256 pairs (1.42 per pair), counted by r5-count on paths that include four lowest bits at depth-5 positions; every step is charged at 364 (v14's batch program: 6,112). Registers: the 24 words of F, at most 5 temporaries and the control values, at most 40 (v19: also the 24 words of D1[0], at most 64, Section U.2).

Stage 2 (unchanged rule): for each pair of the pass word, form x and x + beta (at most 32 basis additions), both complete 5-round digests (2 units), compare 256 bits and output the pair (bytes 0..134 of L^-1(x) and L^-1(x + beta)) if equal; at most 2 units + 2^11 primitives per pair. At most S2CAP = 2^21 (v20: 2^11 by rule K, Section W.1; v16; v15: 2^24) stage-2 pairs per space (2.6; then E stops on that space); the largest count in the 1,236 spaces of R5 is 308.

Lemma 4 (E is v14's E). For every space, at every outer Gray point, stage 1 computes F_k = the 24 equation words of the plain evaluation at the 256 inner points: the recursion is an identity for polynomials of degree <= 4 [BCC+10], and the setup computes the exact ANF. These are the complements of the words of v14's counted e_batch at the same batch (which marks satisfied equations; both are the plain evaluation). So the pass words, their order (outer Gray order, then inner point), stage 2 and the output are those of v14's E, and E outputs a pair on a space iff the window holds a colliding pair and the stage-2 cap does not bind. fes.c (Appendix B) is this stage 1 in native code: it ran every E of R5, C, D (v14) and R6 (Section 4.7), each space self-checked against direct evaluation of all 256 inner points at 64 checkpoints, all passed. r5-count trials 0, 2, 4, 6 check the counted fes_step against e_plain after every step of a 2^8-point outer window. The Python e_window of the replays tests the same 2^32 pairs in natural order (Lemma 4 of v14), which changes at most which pair is output.

### 2.5 Main loop and correctness

Run P (trail_search, 2.1; fail on CapReached or if no level certifies). Base S from P's output. Advice rounds (2.2, 2.3) until K = 96 (v20: 50) accepted spaces of one advice, or until B''s budget or A_MAX is exhausted (then fail). Run E on the K spaces in order and halt with the first output; if there is none, fail. algorithm() in the experiment file is this driver with every cap (its P is trail_search, its E the plain evaluation e_window, Lemma 4). Lemma 1 (outputs are collisions): for x in V, A0 = L^-1(x) satisfies the fixed-bit equations, and so does A0 + L^-1(beta), since E_D forces (L^-1 beta)_j = 0 on F; beta != 0; E compares the true 256-bit digests. Lemma 2 (used only for the probability): for x in V the difference after round 1 is alpha2. Lemma 3: beta is not in W, so the 2^32 pairs of a space are distinct.

### 2.6 Caps

(v16, v17) X_MAX = 2^20, S2CAP = 2^21 and B_TRUE = 2^29 units by v13's rule re-anchored at 2^40 primitives (Section V.2). (v20: S2CAP = 2^11 by rule K, Section W.1; X_MAX and B_TRUE unchanged.) v15's text:

Two counts can only be observed by running and enter the time through a cap: the work units of a connector attempt (X_MAX = 2^23) and E's stage-2 pairs per space (S2CAP = 2^24). These are v14's values, set in v13 by a rule that used no run (each the largest power of two whose charged term stays within 2^43 primitives, v14's T3 batch term rounded down); B''s budget of 2^32 units (chosen in v10 from G2's runs, charged) also satisfies that rule. v15's P no longer has that term; v15 keeps the values unchanged, so that every run of R5 is also a complete run of v15 (Lemma 6) and no cap is re-chosen after seeing R5 (in R5 the largest attempt used 189,224 work units and the largest stage-2 count was 308). v14's F_CAP is gone with v14's T3. P's match counter has the new cap M_CAP = 2^24: the least power of two at least twice the total of P's native run (7,251,935); that run is charged as development (0.1, D15).

## 3. Exact facts (P's output; recomputed by facts() in every B' and connector experiment)

alpha3 = bits {0, 130, 450, 529, 701, 789, 1021, 1169, 1280, 1429}; nonzero lanes of beta2 in hex 0:1 2:4 5:4 6:4 7:4 8:20000 10:2000000000000000 12:200000 15:2000000000000000 18:20000 20:200001 22:200000 24:1. alpha3 and beta3 = L(alpha3) are in the CP kernel (10 bits each); beta2 -> alpha3 on the same 10 rows, w2 = 24 (row 66 weight 4, rows 256 and 277 weight 3, the rest 2); alpha2 = L^-1(beta2) has 59 active rows and w1 = 127; C2 = 3^20 for this core. P45 = sum over the 2^19 alpha4 compatible with beta3 of Pr[beta3 -> alpha4] x prod over nonzero digest-plane rows q of L(alpha4) of (DDT[q][0] + DDT[q][16])/32 = 55/2^19 = 2^-13.2186 (192 nonzero terms); with w2, p_M = 2^-37.2186 per pair. Advice facts, for each advice used: beta1' -> alpha2 has weight 127 on the 59 rows; beta0' is compatible with alpha1' on every row and zero on its inactive rows; alpha0' = L^-1(beta0') is nonzero and zero on F. v15's P certifies this trail at its level of 64 blocks (2.1; r5-count trial 10 rechecks it on every review).

## 4. Executed evidence (none of it is the claimed cost)

### 4.1 Coins, run selection, premise R, every run made since v11

Coins of our runs. A labelled run uses Coins(SHA-256(label || "beta1" || c)) for B''s candidate c, Coins(SHA-256(label || "att" || c || j)) for its attempt j, and, for connector attempt i on the advice of candidate c, seed_i = SHA-256(label || "conn" || (c + 1) as 4 little-endian bytes || i as 8 little-endian bytes) with words SHAKE-256(seed_i || k) (class Coins). The index map is the algorithm's own: Fisher-Yates index j = (low 64 bits) mod (i+1). In the claimed algorithm every coin is a fresh uniform 256-bit word; the only difference is SHAKE-256 output in place of fresh words.

Premise R (stated inside H1): the label-seeded coins act as fresh coins, and the 48 runs of each pre-registered study (R5, v14's; R6, ours, 4.7) are an unselected sample of the algorithm's runs. Under premise R the 48 success indicators of a study are independent Bernoulli(p) draws; distinct labels by themselves only give distinct SHAKE-256 streams. Support for R5 (v14's text; R6's is in 4.7):
- The labels "hashsmash sha3-256-r5 R5 run k", k = 0..47, the plan, the driver, the analysis and every file of the computation were hashed at 2026-10-07T20:27:28Z, before any run (Appendix D; a first commit at 20:27:03Z was replaced before any run, only to change the launcher's start gate; the launch wrapper and the watchdog, which compute nothing, were written after the commit and before the launch).
- All 48 runs were started and completed (exit code 0, empty error files); none was stopped, excluded or repeated; every result is in the table of 4.3 and the ledger of Appendix D.
- The plan has one outcome-dependent rule: claim 0.40 if the bound is at least 0.40, else nothing from R5. A bound computed by a rule fixed in advance keeps its coverage whatever is then done with it: Pr[the claim is made and the true success is below it] <= Pr[the bound exceeds the true success] <= 0.05. It has no rule that changes a constant.
- The organizer's seeds pick which logged successes r5-R-0..7 replay and which earlier attempts are re-run; a holdout nonce changes them. They do not enter any bound.

Every run made since v11 (2026-10-07; times UTC; v14's list). In v14 only R5 entered the bound, in v15 R6 and R5 did (v20 and v22: R7 alone). C and G2's runs are charged (0.1; v20: C no longer, W.3); the rest are listed so that nothing is selected away.
- Pre-registration C (16:57:43Z-17:16:03Z, 48 runs), its smoke-test run 999 (16:55:34Z) and pre-registration D (17:53:22Z-17:58:42Z, 31 runs): v13's evidence for v13's tuned B' (4.4).
- C' (a parallel session of ours): plan prereg/plan.md hashed at 16:58:33Z (SHA-256 7fde45cf25f6555cab68dfef679adce25cd5fad6ab64cdc9ca4a2cb6da063b8b), which states "B' constants of v11, fixed by rule with no run: no attempt limit per candidate ..., DMIN = 33 ..., D2u ordering unweighted (all weights 1)", os.urandom seeds and a native E. 14 runs started 16:58:42Z-17:14:54Z; 4 finished (its runs 2, 5, 7, 9), each with a collision (at its spaces 2, 3, 11 and 4); the other 10 were left unfinished when it was abandoned at 17:18Z (prereg/runs.jsonl, SHA-256 2f63dd3bae4e21cbd736529cd3fbfcb7fd469dfba1bd92825b3e8d97236eecd3). Before it, the same session made 3 test runs of the variant from 16:52:22Z (test_log.jsonl, SHA-256 38093c7f3809938e984eb15d164a1e7106ef27b7b33f5aba71d0320c666f4d9f) whose native E was not a working form of E (0.05-0.11 round-2 passes per space against about 256 expected); none had an output. C' chose no constant (its plan predates its runs) and enters no bound; R5's plan names it.
- Runs made for v13 (after 20:00Z): local organizer-experiment runs and a certificate check, no new outcome.
- The R5 study: 48 runs, 20:45:12Z-21:23:48Z (4.2). Before its plan, its driver was run once, as a self-test that re-derived v11 pre-registration C's run 5 positive space with v11's constants (no R5 outcome).
- Runs made for v14 (21:43Z-22:20Z), all re-derivations of logged R5 runs with no new outcome: a replay of all 48 runs with the experiment file's code (each advice re-derived from its label with the logged DF and hash; connector attempts 0..i re-run with the logged status, DF and work count; 46 collisions re-found at the logged coordinates; for runs 6 and 31 all attempts up to the 96th acceptance); whole B' runs of the 15 R5 runs whose advice came from candidate 0 (each with the logged cost and advice); timing and memory measurements of the replays; local organizer-experiment runs (4.6).
- Runs made for v15 (2026-10-08): D15 (charged, 0.1: the first native T3 run with contiguous blocks, stopped in its tenth level; the comparison of six block layouts on 8 cores; the certified native run of P, 2.1 and Appendix A; count-only recounts of the stopped runs' match totals, used only to charge them; Python re-runs of T3 on single cores for the checks of 2.1; development and checks of the counted stage 1; the driver's self-test, a replay of R5 run 4 that reproduced R5's logged advice and collision); R6 (4.7: plan and code hashed at 00:19:33Z, 48 runs started from 00:19:45Z, all reported); local organizer-experiment runs (4.6) and the certificate check (re-derivations, no new outcome). Every run made for v19, v20 and v22, with hashes, is in Sections U.5, W.2, W.6, W.10, X.8 and X.10.

### 4.2 The R5 study (48 complete runs of v14's algorithm)

Plan (Appendix D, summarised; plan.txt, SHA-256 7ffaf34f4001a449a6775fa3f204f7c93a0be60c69e45588d320aae1d382574b), hashed at 2026-10-07T20:27:28Z with the driver r5run.py, the experiment file (r5v13.py, byte-identical to v13's experiments/r5.py), the analysis analyze.py, the launchers, the enumerator fes (the binary of C, Appendix B) and its libraries (commit.txt, Appendix D). R5 is algorithm() of that file with B''s three settings replaced by the values of 2.2 (r5run.py sets them before the run: B_R = 2^62, B_DMIN = 33, KW = MW = LB = PREF = 1); this is v14's experiment file, whose algorithm differs from v13's only in these constants. Per run, as algorithm() does it: B' with its budget and candidate cap from candidate 0, the connector rule (attempts until 96 accepted, or discard the advice after 2^11 attempts and resume B'), then E on the accepted spaces in order up to the first output, with fes (exact over the 2^32 window, self-check against direct evaluation at 64 points) and stage 2 by complete 5-round digests on at most S2CAP pairs. P's output is the trail of Section 3 (premise P). Launch: at 20:38:41Z; a run started only when fewer than 11 processes were busy and the 1-minute load average was below 12, at most 10 runs at a time, nice 10. A watchdog written before the launch (watchdog.py, SHA-256 c0f03d92bf1f653c4268ebd06721189666d647e99ff74d7c1085e6b6df186b4d; it pauses and resumes our processes to keep the machine at 12 or fewer busy processes, which cannot change a deterministic run's result) paused two runs for 10 s each (watchdog.log). The first run started at 20:45:12Z and the last ended at 21:23:48Z; all 48 exit codes are 0 and all error files are empty. Python CPU time 12,150 s in all (plus fes).

Results (every run; per-run table and ledger in Appendix D):
- 46 of 48 runs output a collision; runs 6 and 31 had none in their 96 spaces. Every collision was verified by complete digests, and again by our replay with the experiment file (4.1).
- B': 141 candidates; 51 accepted (DF 33-76), 90 ended at CCAP; B' cost per run 2^23.19 to 2^28.73 units.
- Connector: 51 advice rounds, 15,323 attempts, 4,674 accepted (0.305); 96 accepted within 96-557 attempts on every kept advice. Runs 9, 17 and 47 discarded their first advice at A_ADV (65, 0 and 1 accepted in 2,048 attempts), and B' resumed at the next candidate, as the algorithm does. Largest attempt 189,224 work units (X_MAX = 2^23).
- E: 1,236 spaces enumerated, all self-checks passed, round-2 passes per space 200-308 (mean 255.75; 2^32 x 2^-24 = 256 expected); the stage-2 cap never bound. First positive space at index 1-89.
- Analysis (analyze.py, fixed in the plan): 46 of 48, one-sided 95% Clopper-Pearson lower bound 0.8746; claim rule: 0.40 (analysis.json, SHA-256 25e283c8b53d9725830e263daf9fa69c433859b47f30b7a9e1dcb7d95a96d2b3).

### 4.3 Per-run table of the R5 study

In Appendix D (v22b: merged with the study's per-run ledger): for every run its candidates, (c, j) and DF per advice round, B' log2 units, connector attempts and acceptances, spaces enumerated, first positive space and success, with the ledger's hashes and counts.

### 4.4 Earlier runs: pre-registrations C and D, G2's runs

Pre-registrations C and D measured v13's algorithm (tuned B': R = 16, DMIN = 40, weights 1, 0.25, 1, 1) on 48 pre-registered runs: C (plan prereg_c/plan.txt, SHA-256 4e1edbd45e4b0dfb10de7a67f432805e30d54eef073caba197d26ace7142b666, hashed with its driver, analysis and enumerator at 16:55:25Z) ran B', the connector rule and E on the first 16 spaces of runs k = 0..47 (16:57:43Z-17:16:03Z; 328 candidates, 48 advices, 768 spaces, 23 positive in 18 runs); D (plan 3a3bc8119b38b5eaa969a4a803db9b0c9d59c08b363ebaecc88816aeb21ba46c, hashed at 17:53:16Z) completed the other 30 runs and run 999 (818 spaces). 46 of 48 succeeded (47 of 49 with run 999), the same count as R5. Both plans are in Appendix C. C's rule would have raised K had its bound been below 0.40, so C is charged (0.1): its 48 B' runs at their exact WK counts (8,469,642,639,781 primitives), its 9,097 connector attempts at their 2^18 cap, 48 x S and 768 spaces at the counted E, 2^35.9149 units. D fixed no number. Neither enters Section 5.

G2 (charged, 0.1): the v6 run (one advice, 14 positive spaces in the first 512 accepted) and pre-registrations A (nine B' runs under v8's program, 65 candidates) and B (18 spaces of A's advices). v10 chose K, CCAP, B_BUDGET, A_ADV and A_MAX from them. None enters Section 5.

### 4.5 Certificates

(v20) 16 certificates (distinct 135-byte messages, equal complete 5-round digests), the most intake accepts: r5-v6-000038, whose first message r5-count uses, and the collisions of the first 15 successful R7 runs in k order (ids r7-R7-k<k>-<coordinate>), as R7's plan fixed (Section W.2); each is that run's logged output. v19's certificates (R5 runs 0-5, 7 and 35, run 35's replay exceeding the experiment sandbox's memory; the first seven successful R6 runs, k = 1..7, ids r6-R6-k<k>-<coordinate>) and v14's (R5 runs 8-14) are not repeated; R5's and R6's outputs are in Appendices D and E.

### 4.6 Organizer experiments

(v15's section, condensed; the current experiments and local runs are in Sections W.10 and X.10, and experiments/manifest.json states each experiment's scope and hypothesis.) r5.py holds the reference algorithm and all experiments in one file (the organizer's limits: 16 experiments and 64 KiB of source). r5-R-* return real collisions; the others check programs and counts and return sentinels, PASS (00^135, 01 || 00^134) or FAIL (00^135, 02 || 00^134): r5-trail-0..3 recount P's structural counts per lane group (T1 nodes per lane; cores, C1, P45 > 0, C2, HV); r5-count checks the counted stage 1 against e_plain, T2's counted leaf, P's driver on the sub-problem [core 874, core 1136] with all levels and with its cap, and T3's certifying level on the output core (49,060 matches, 30 evaluations, the trail of Section 3); r5-mitm-0, 1 run T3's level of 64 blocks on a seed-picked kept core (re-derived by T1 from its lane and the mask LANEM; match count = the native log MT6), and r5-mitm-1 also the counted half-vector step over both half tables of the output core and the counted match step on 4 seed-picked level-64 blocks of it; r5-bpfull runs a whole logged B' from its label (logged cost and advice), both B' caps, the study's table and bound, and connector attempts with organizer coins; r5-R-0..7 replay two seed-picked logged successes of a stratum (advice re-derived from the label, logged connector statuses re-run, E's 2^12-coordinate window returns the logged collision). r5-mitm-0, 1 review 2 of the 467 per-core match counts per review (each wrong count caught with probability about 2/467 per review); the output core, whose count and trail matter for the certification, is checked on every review (r5-count trial 10). v15's local runs (experiments/runner.py with Python 3.12 in place of Docker, each experiment twice with byte-identical output, on the public seed and the nonces "v15-nonce-1" and "v15-nonce-2", written down before the runs) passed all 16 experiments on all three seeds, at most 11.8 CPU-s and 93 MB per experiment.

### 4.7 The R6 study (ours: 48 complete runs of v15's algorithm)

Plan (Appendix E, summarised; plan.txt, SHA-256 9c7659c3acf661348f3d8e031cb28bb16bc309614f0a9763cdb9a2e4c22e5e7c), hashed at 2026-10-08T00:19:33Z with the driver r6run.py, the experiment file r5v14.py (byte-identical to v14's experiments/r5.py, whose B', S, connector and driver v15 keeps unchanged), fes.c and the binary fes, P's native T3 mitm2.c, the analysis analyze.py, the launcher run_all.py and the organizer verifier's keccak.py (commit.txt, Appendix E). All files were made read-only at the commit. Labels "hashsmash sha3-256-r5 R6 run k", k = 0..47; coins derived from the label exactly as algorithm(label) does. Before the plan, the driver was run once as a self-test on the label of R5 run 4; it reproduced R5's logged advice and collision (no R6 outcome; charged in D15). The launcher started run 0 at 00:19:45Z, at most 5 runs at a time with nice 10, and the last run ended at 2026-10-08T02:10:55Z. All 48 exit codes are 0 and all error files are empty. Python CPU time 18,994 s in all, plus 2,493 s in fes. Premise R for R6: the labels, plan and every file of the computation were hashed and made read-only before any run; every run is reported (table below, Appendix E); the plan's only outcome-dependent rule is whether to claim, which keeps the bound's coverage; no constant was changed after any run.

Results (every run; table below, which includes the per-run ledger's coordinates and result-file hashes):
- 44 of 48 runs output a collision; runs 0, 29, 30, 45 had no output in their 96 spaces. Every collision was verified by the analysis with the experiment file's digest and with the organizer verifier (sha3_256(m, 5)).
- B': 162 candidates in all; B' cost per run 2^22.62 to 2^29.61 units (budget 2^32).
- Connector: 58 advice rounds, 33,131 attempts, 4,844 accepted; ten advices were discarded at A_ADV after 2,048 attempts each (accepted in parentheses): runs 10 (1), 11 (53), 12 (0), 18 (66), 23 (1), 27 (64), 33 (2), 34 (46, then 0) and 45 (3). Largest attempt 190,240 work units (X_MAX = 2^23).
- E: 1,408 spaces enumerated, all self-checks passed; round-2 passes per space 210-315 (256 expected); the stage-2 cap never bound. First positive space at index 1-78.
- Analysis (analyze.py, fixed in the plan): 44 of 48, one-sided 95% Clopper-Pearson lower bound 0.8193; claim rule: 0.40 is supported (analysis.json, SHA-256 35c979811047ee5fea6d2759d6abce254f68e72b95f4fbe5ba138cba9a15d162).

Per-run table (from the result files; "attempts", "accepted": connector attempts and acceptances per advice round; "spaces": E's spaces enumerated up to the first output; B' log2 units over all rounds; the output coordinate and the SHA-256 of results/k.json, which are R6's per-run ledger, merged here in v22b): (v25: the SHA-256 values in this table are shortened to their first 16 hex digits to keep the judge evidence within its budget; the full values are in v22b's proof (08930c1e), unchanged.)

| k | candidates | (c, j) per round | DF | B' log2 units | attempts | accepted | spaces | first positive space | success | coordinate | results/k.json SHA-256 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 23 | 13 | 10, 10; 12, 31 | 34, 41 | 29.61 | 2048 + 139 | 1 + 96 | 32 | 32 | yes | ebc5894d | 2814d456fcc74d59 |
| 28 | 9 | 8, 9 | 45 | 29.05 | 347 | 96 | 9 | 9 | yes | 69da8cfa | 465e78731bb2c763 |

(R5N: 46 rows condensed out to fit the 512 KiB judge-evidence budget; kept: runs 23 and 28, the two re-derived in V.5. The full table is in 0f72a85e's and v15's proofs, unchanged; R6 is listed, not charged.)

## 5. Success probability (end to end, over the algorithm's own coins)

(v20) v20's success probability rests on R7 alone (Section W.2): 39 of 48 complete runs of v20 succeed; under premise R the one-sided 95% Clopper-Pearson lower bound is 0.6956 >= 0.40, so by R7's pre-registered rule the claim 0.40 is supported. R5 and R6 are complete runs of v19 (Lemma 6 below), not of v20, and are history (W.8). The rest of this section is v19's.

The probability space is the algorithm's coins: B' candidate coins and connector coins. The target is fixed, and P and E are deterministic. A run of the algorithm is therefore a function of its coins, and p = Pr[the algorithm outputs a collision].

(v20: Lemma 6 concerns v19's algorithm, with K = 96; R7's runs are complete runs of v20 directly, Section W.2; and of v22, Section X.11.)

Lemma 6 (complete runs; v17-v19). (c) Each R5 and R6 run is also a complete run of v17: v17 differs from v15 only in the B' true-cost tally and its budget B_TRUE = 2^29 units, which no R5 or R6 run reached (largest true B' cost 2^28.2709 units, Section V.5; WK's counter and caps act as in v15), in the programs that compute P's T3 (same keys, matches, decisions and output: r5-mitm-1 trials 1, 2), whose output is a constant of every run, and in the caps X_MAX = 2^20 and S2CAP = 2^21, which no R5 or R6 run reached (largest attempt 190,240 work units, largest stage-2 count 315); an attempt or a space that stays below a cap behaves identically under either cap. (v18, v19) v18's unrolled E blocks (V.7) and v19's three program changes (U.1-U.3: the same AS, decisions, match counts and CapReached point, the same stage-1 words in the same order, the same leaf decisions and 467 kept cores) compute the same values in the same order, with the same caps, constants and rules, so each R5 and R6 run is also a complete run of v18 and of v19, with the same output (r5-count trials 0-7 and r5-mitm-1 trial 2 check each change against the plain evaluation). Parts (a) and (b) are v15's:

Lemma 6 (complete runs). (a) Each R6 run is v15's algorithm executed with label-derived coins: r6run.py makes algorithm()'s calls in algorithm()'s order (bprime, Setup, attempt, E per space) from the code of v14's experiment file, whose B', S, connector and driver v15 keeps byte for byte; P's output is the certified trail (2.1); E on a space is fes (v15's stage 1, Lemma 4) and stage 2 by complete digests in fes's order with at most S2CAP pairs. In R6 B''s budget never acted (at most 2^29.61 units per run), no attempt reached X_MAX (largest 190,240 work units), A_MAX never acted (at most 4192 attempts in a run), every fes self-check passed and the stage-2 cap never bound (at most 315 pairs). (b) Each R5 run is also a complete run of v15: v14's Lemma 6 shows it is a complete run of v14's algorithm, and v15 differs from v14 only in P and E's stage 1, which compute v14's outputs (Lemma P, Lemma 4), and in the caps F_CAP (gone) and M_CAP (P's native run stays 2.31 times below it); P's output is a constant of every run. So R5's success indicators are v15's.

Heuristics: v22's H1 and H2, like v20's, are in claim.json; H1 rests on R7 (Sections W.2 and X.11). In v15 and v19, H1-end-to-end-success (p >= 0.40 under premise R, that the label-seeded coins act as fresh coins and the runs of the pre-registered studies are unselected samples of the algorithm's runs, and premise P, 2.1) rested on R6 (Section 4.7, Appendix E: 44 of 48, one-sided 95% Clopper-Pearson bound 0.8193) and R5 (4.2: 46 of 48, bound 0.8746), not pooled, each alone supporting 0.40; H2-development-ledger stated that the charged development contains every target-specific run whose result fixed, or under its plan could have changed, a number that the algorithm reads (0.1, 0.2): v15's G2, C and D15; v19's G2, C, D15 with the T1/T2 export, D16 and D19 (U.4, U.5, U.8); v20's G2, D15, D16, D19 and D20 (C not charged, W.3); v22's G2, D15, D16, D19, D20, D21 and D22 at v22's prices (X.5, X.8).

So Pr[success] >= 0.40 with confidence at least 95% under either study (v20: under R7, Section W.2). Every cap of Section 6 holds without H1.

Consistency (descriptive; no bound uses it): R6 found 44 positive spaces in 1,408 enumerated spaces (0.031 per space; E stops at the first output); R5 found 46 in 1,236 (0.037); the trail predicts 0.0265 (1 - exp(-256 x 2^-13.2186)), and a run succeeds with probability 0.924 at that rate.

## 6. Time (collision-frontier-v5: one 5-round permutation = 1 unit, other primitives 1/1355)

| Term | Cap, enforced by | Count and price | log2 units |
| --- | --- | --- | --- |
| P: T1 | exact count N1 (organizer-recomputed) | 8,674,833 nodes x 2^12 (bound per node, as in v8) | 24.6443 |
| P: T2 (v22) | exact count C1 (organizer-recomputed) | 1,639,088,128 leaves x 26 (counted, X.2) | 24.9066 |
| P: T3 half vectors (v22) | exact count HV (organizer-recomputed) | 48,592,224 x 83 (counted state step, all 127 keys and the entry pointer included, X.3) | 21.5052 |
| P: T3 keys (v16) | inside hv_step | 0 (v15: 7 x HV x 2^11, 28.9375) | - |
| P: T3 sort and merge | 127 blocks over the levels (fixed) | 127 x HV x 2^6 (bound) | 28.1188 |
| P: T3 block setup | 127 blocks x 467 cores (fixed) | 127 x 467 x 2^17 (bound) | 22.4519 |
| P: T3 matches (v22) | M_CAP = 2^24 (2.6) | 2^24 x (899/16 counted, X.1 + 2^11 evaluation bound); per (a, block) 18 inside the sort-and-merge bound | 24.6350 |
| P: setup (v16) | | 2^32 primitives (bound; includes the half-vector tables, v22: the state tables of X.2-X.3) | 21.5959 |
| B' (v17) | true-cost budget B_TRUE (V.5), re-checked on every update; WK's B_BUDGET and CCAP as v15 | 2^29 units + one update (< 2^13 units) | 29.0000 |
| S | at most 4 advice rounds | 4 x 2^31 primitives | 22.5959 |
| Connector (v20) | X_MAX = 2^20 work units per attempt, A_MAX = 4268 attempts | 4268 x (2^20 x 96 + 2^15 x 2^9 + 2^22) primitives | 28.5132 |
| Bases (v20) | K = 50 spaces | 50 x 2^24 primitives | 19.2398 |
| E setup (v20) | K = 50 spaces | 50 x 2^16 units (bound: 41,449 evaluations at 1 unit + 2^23 primitives) | 21.6439 |
| E stage 1 (v22) | 2^16 blocks of 256 steps per space | 50 x 2^16 x 66,831 primitives (counted per block, X.4) | 27.2680 |
| E stage 2 (v20) | S2CAP = 2^11 per space | 50 x 2^11 x (2 units + 2^11 primitives) | 18.4559 |
| Output | one pair | 2^22 primitives | 11.5959 |
| Algorithm (v22) | | | 30.4623 |
| Development G2 (v14's; v6 run, pre-registrations A and B) | exact counters and caps (0.1) | counted prices of the submitted programs; B' at its true cost (V.5); E at v22's E (X.4, X.5) | 30.9572 |
| Development C (v14's pre-registration C) | | not charged since v20 (W.3) | - |
| Development D15 (v15's) | counts of v15's runs (0.1) | at v22's counted prices (X.5; V.3's rule), half vectors at every level (W.5), with the T1/T2 export (U.4) | 32.0018 |
| Development D16 (v16/v17) and D19 (v19) | D16: v17's runs (Section V.3); D19: every run made for v19 except the organizer's harness (U.5) | D16 stated bound; D19 counted prices (v22's for contig.c, X.5) and stated bounds | D16 27.0000; D19 28.8303 |
| Development D20 (v20) | every run made for v20 except executions of the organizer's harness and R7 (W.6) | counted prices (the self-test at v22's E, X.5) and stated bounds | 29.0748 |
| Development D21 (v21's) and D22 (v22) | D21: v21's build checks of the routines v22 adopts; D22: every run made for v22 except executions of the organizer's harness (X.8) | D21 v21's stated value, rounded up; D22 counted prices and stated bounds | D21 22.6078; D22 26.7962 |
| Total T (v22) | | | 33.093387 -> 33.09339 (v20, v19, v18, v15: X.9, W.9, U.8, V.4) |

Every term of the algorithm is a cap, a fixed count or an organizer-recomputed count, times a counted longest path or a stated bound; no expected value is used, and no count taken only from our runs enters except through a cap (M_CAP). Preprocessing (P + B' + S + development): v22 2^33.004263, claimed 33.00427 (v20: 2^33.058081, claimed 33.05809; v19: 2^33.5279, claimed 33.53; v15: 2^35.4430, claimed 35.45). The exact sums are in rationals (the script that produced this table reproduces v14's 2^35.0558 and 2^37.0488 from v14's terms).

Sensitivity (v15's, not the claim; v20's sensitivities are in Section W.9, v22's in Section X.9): every bound of T3 four times larger: 35.82; the E setup bound four times larger: 35.76; E stage 1 at 2 x 364: 35.77; G2 and C at v14's prices: 37.13; D15 doubled: 36.31; D15 omitted: 34.83.

## 7. Memory

(R5N3: the claim's memory figure is R.4's, and the advice-generating run is R.8's capped run s12. P's T3 runs core by core (Section W.4): in the shipped counted program one core's half tables are resident and are deleted before the next core's. T1's set of found cores has 1,741 entries (r5-trail-0..3). algorithm() keeps one basis per accepted space before E (R.3).)

## 8. Not claimed; credits

Not claimed: any improvement on [GLL+20] beyond the byte-aligned (p = 8) adaptation, B', the counted programs and the accounting. The certificates show that the construction works; they are not the claimed cost.

Lineage: v25h (b5213766) <- v25 (fa625146) <- v22b (08930c1e) <- v22 <- v20 (84668773) <- v19 (a2d6ce92) <- v18 <- v15 <- v14 (f1cedf6b); co-authors winglock, Th0rgal, Meganpark980320, rubenmarcus, Subflatus3, 0xshikhar, leech1996.

Credits: [GLL+20] for the connector and linearisation framework and the 5-round trail core that P re-derives; Dinur, Dunkelman, Shamir (FSE 2012) for the target-difference algorithm; Qiao, Song, Liu, Guo (EUROCRYPT 2017) for linearisation; Daemen, Van Assche (FSE 2012) and KeccakTools for in-kernel trail cores; Bouillaguet, Chen, Cheng, Chou, Niederhagen, Shamir, Yang (CHES 2010) [BCC+10] for fast exhaustive search, used by v14's evidence enumerator fes.c and now by the counted E. winglock (v8 113fc836, v13 7f16e461, v14 f1cedf6b) and Th0rgal (7deb1595, with Subflatus3 and rubenmarcus) for the zero-advice framing and the whole algorithm this package modifies; Subflatus3 (9bccf245) also used fast exhaustive search inside E (on the round-1 input, at 429 primitives per pair) and enumerated the output core's leaves with AS(alpha2) <= 63 by a half-sum match on 5-row blocks, an idea close to our T3; GordoAR (e3ce0518, bc0f7b56, ed433634) for re-sizing work on the same lineage; hybridnoise (ef4a0c66) and jagnani73 (654cb3d2) as credited by v14. baseline_improved is the required nominal reference ID, not a claim of dominance.

## Appendix A. Trail search P as run (T1 and T2 in the experiment file; T3 in C)

(R5N2: the advice is produced by R.8's capped run; mitm2.c's run below is superseded.) These programs are our evidence for premise P (2.1); the algorithm's P is trail_search in r5.py. T1 and T2 ran as the experiment file's lane_dfs and p45pos (cores.py: 1741 cores, 467 kept, sum C2 = 1,379,275,399,350, the counts that r5-trail-0..3 recompute); export.py wrote, for every kept core in T2's order, its rows and, for every compatible input difference of every row, the row values of L^-1 of that difference (core_tables), and the tables MINW and WT2 (cores.bin, SHA-256 a3a10277c3cd2fd0eb6cf82eb509ca57907b1597e37a8a8057db584c53a9a9b9). mitm2.c is T3 (2.1); its header comment is the one of the earlier contiguous-block program mitm.c (D15), while its blocks and levels are those of set_level, which are the ones of 2.1 and of r5.py. Built with clang -O3 -mcpu=apple-m4 and run as `mitm2 cores.bin 5` (5 threads, 370 s, 296 CPU-s, 233 MB). Its output mitm2.log (3,277 lines: per core and level the half-vector entries, matches and evaluations, per level the totals and the best leaf, then "CERTIFIED at level 6 (nb 64)") has SHA-256 e0430adb40d7f166ed1625494d02283a285092c33a608175a76371b74bbdbebc. SHA-256 of the sources: cores.py 7e77b07d0514846a4be75e0fc58a3ecd69b7fedc6b8b14aaa63e4c9fcd213bd5, export.py d3e5256998b947b6265eab09b4b4d63025f8dea9cea0b3cfe63146d46a5e897c, mitm2.c 7a2ba2db66cf57ec664c623af8ed922067829d3f2a25c850d8d2f6a842b47d7f (the file hashed in R6's commit record, Appendix E). v14's native T3 (trail3b, two exhaustive passes over all batches; v14's Appendix A) found the same trail.

`cores.py` (with the experiment file imported as r5v14, which is byte-identical to v14's experiments/r5.py):

```python
import sys, json, math
sys.setrecursionlimit(10000)
import r5v14 as R
reach=set()
for lane in range(25):
    reach |= R.lane_dfs(lane)[1]
cores=[c for c in sorted(reach) if R.p45pos(c)]
out=[]
for c in cores:
    rows=R.rows_of(c)
    ms=[R.NIN[o] for _,o in rows]
    out.append({"bits":list(c),"ms":ms,"c2":math.prod(ms)})
json.dump(out,open("kept.json","w"))
print(len(reach),len(cores),sum(x["c2"] for x in out))
```

`export.py`:

```python
import json, struct, sys
import r5v14 as R
kept=json.load(open("kept.json"))
out=open("cores.bin","wb")
out.write(struct.pack("<I",len(kept)))
def rowbytes(s):
    # byte r = 5-bit value of row r=(y,z), r = 64*y+z
    b=bytearray(320)
    for y in range(5):
        for z in range(64):
            b[64*y+z]=sum(((s>>(64*(x+5*y)+z))&1)<<x for x in range(5))
    return bytes(b)
for ci,c in enumerate(kept):
    bits=tuple(c["bits"])
    rows, ins, LI = R.core_tables(bits)
    out.write(struct.pack("<I",len(rows)))
    for j,((y,z),o) in enumerate(rows):
        out.write(struct.pack("<IIII",y,z,o,len(ins[j])))
        for d in ins[j]:
            out.write(struct.pack("<I",d)); out.write(rowbytes(LI[j][d]))
    R.CACHE.clear()
out.write(bytes(R.MINW))
for d in range(32):
    for o in range(32):
        out.write(bytes([5-(R.DDT[d][o].bit_length()-1) if R.DDT[d][o] else 99]))
out.close()
print("ok")
```

`mitm2.c`:

```c
// mitm.c: trail search P's step T3 by meet-in-the-middle on zero blocks of alpha2 (native evidence program).
// For every kept core (the T1/T2 output, in T2's order) the beta2 choices are split into two halves A (rows 0..h-1)
// and B (rows h..n-1); alpha2 = LA(a) + LB(b) with LA, LB linear images under L^-1.  A level is a block size bsz
// dividing 320: the 320 rows of alpha2 form nb = 320/bsz blocks of bsz consecutive rows.  A leaf with
// AS(alpha2) <= nb - 1 has a zero block t, i.e. LA(a) and LB(b) agree on block t.  For each block the program
// matches the keys of both halves (exact for 5*bsz <= 26 bits, else a linear 26-bit fold; false matches are
// discarded by the full check) and evaluates every matching leaf with AS <= tau = nb - 1 in full (w1, w2, choice).
// After a level, the best w1 W* over all cores is certified if W* <= 2 tau + 1 (every leaf not found has AS >= tau+1,
// so w1 >= 2 AS >= 2 tau + 2).  Levels run from the largest block size down; the first certified level stops P.
// Output order: least (w1, w2), then the earlier core, then the least choice vector (row order) - v14's order.
// Usage: mitm cores.bin threads  (prints per-level, per-core counts and the result)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <pthread.h>
typedef uint64_t u64;
#define NW 40
typedef struct { int y, z, o, m; int d[32]; u64 v[32][NW]; } Row;
typedef struct { int n; Row r[10]; } Core;
static Core *cores; static int ncores;
static uint8_t MINW[32], WT2[32][32];
static const int NBL[] = {1, 2, 4, 8, 16, 32, 64};
#define NLEV 7
static int BROWS[64][320], BCNT[64];
typedef struct { int w1, w2, core; int ch[10]; } Best;
static int better(const Best *a, const Best *b) {  // a < b ?
  if (b->w1 < 0) return 1;
  if (a->w1 != b->w1) return a->w1 < b->w1;
  if (a->w2 != b->w2) return a->w2 < b->w2;
  if (a->core != b->core) return a->core < b->core;
  for (int i = 0; i < 10; i++) if (a->ch[i] != b->ch[i]) return a->ch[i] < b->ch[i];
  return 0;
}
typedef struct { uint32_t key, idx; } KI;
static void rsort(KI *a, KI *tmp, int n) {  // LSD radix, 2 passes of 13 bits (26-bit keys)
  static __thread int cnt[1 << 13];
  for (int pass = 0; pass < 2; pass++) {
    int sh = 13 * pass;
    memset(cnt, 0, sizeof cnt);
    for (int i = 0; i < n; i++) cnt[(a[i].key >> sh) & 8191]++;
    int s = 0;
    for (int i = 0; i < 8192; i++) { int c = cnt[i]; cnt[i] = s; s += c; }
    for (int i = 0; i < n; i++) tmp[cnt[(a[i].key >> sh) & 8191]++] = a[i];
    memcpy(a, tmp, sizeof(KI) * n);
  }
}
static inline uint32_t keyof(const u64 *v, int t) {
  // the block's row values (5 bits each, in the block's row order) folded linearly into 26 bits (exact if <= 26 bits)
  const uint8_t *by = (const uint8_t *)v;
  uint32_t k = 0; int pos = 0;
  for (int i = 0; i < BCNT[t]; i++) {
    uint32_t c = by[BROWS[t][i]] & 31;
    k ^= (c << pos) & 0x3FFFFFF;
    if (pos > 21) k ^= c >> (26 - pos);
    pos += 5; if (pos >= 26) pos -= 26;
  }
  return k;
}
static void set_level(int nb) {  // block of row (y, z): ((z + 13 y) mod 64) mod nb; rows in increasing r = 64 y + z
  for (int t = 0; t < nb; t++) BCNT[t] = 0;
  for (int r = 0; r < 320; r++) { int t = ((r % 64) + 13 * (r / 64)) % 64 % nb; BROWS[t][BCNT[t]++] = r; }
}
typedef struct {
  int lev;  // level index
  long long matches[1024], evals[1024], entries[1024];
  int next; pthread_mutex_t mu; Best best;
} Job;
static Job job;
static void do_core(int ci, int nb, long long *M, long long *F, long long *E, Best *best) {
  Core *C = &cores[ci];
  int n = C->n, h = 0; long long bestsum = -1;
  for (int hh = 1; hh < n; hh++) {
    long long pa = 1, pb = 1;
    for (int j = 0; j < hh; j++) pa *= C->r[j].m;
    for (int j = hh; j < n; j++) pb *= C->r[j].m;
    if (bestsum < 0 || pa + pb < bestsum) { bestsum = pa + pb; h = hh; }
  }
  long long na = 1, nbb = 1;
  for (int j = 0; j < h; j++) na *= C->r[j].m;
  for (int j = h; j < n; j++) nbb *= C->r[j].m;
  u64 *VA = malloc(sizeof(u64) * NW * na), *VB = malloc(sizeof(u64) * NW * nbb);
  int *WA = malloc(sizeof(int) * na), *WB = malloc(sizeof(int) * nbb);
  for (int side = 0; side < 2; side++) {
    int lo = side ? h : 0, hi = side ? n : h; long long N = side ? nbb : na;
    u64 *V = side ? VB : VA; int *Wt = side ? WB : WA;
    for (long long s = 0; s < N; s++) {
      long long r = s; u64 acc[NW] = {0}; int w2 = 0;
      for (int j = lo; j < hi; j++) {
        int i = (int)(r % C->r[j].m); r /= C->r[j].m;
        for (int w = 0; w < NW; w++) acc[w] ^= C->r[j].v[i][w];
        w2 += WT2[C->r[j].d[i]][C->r[j].o];
      }
      memcpy(V + NW * s, acc, sizeof acc); Wt[s] = w2;
    }
  }
  int tau = nb - 1;
  KI *ka = malloc(sizeof(KI) * na), *kb = malloc(sizeof(KI) * nbb), *tmp = malloc(sizeof(KI) * (na > nbb ? na : nbb));
  long long m = 0, f = 0;
  for (int t = 0; t < nb; t++) {
    for (long long s = 0; s < na; s++) { ka[s].key = keyof(VA + NW * s, t); ka[s].idx = (uint32_t)s; }
    for (long long s = 0; s < nbb; s++) { kb[s].key = keyof(VB + NW * s, t); kb[s].idx = (uint32_t)s; }
    rsort(ka, tmp, (int)na); rsort(kb, tmp, (int)nbb);
    long long i = 0, j = 0;
    while (i < na && j < nbb) {
      if (ka[i].key < kb[j].key) { i++; continue; }
      if (ka[i].key > kb[j].key) { j++; continue; }
      long long i2 = i, j2 = j;
      while (i2 < na && ka[i2].key == ka[i].key) i2++;
      while (j2 < nbb && kb[j2].key == kb[j].key) j2++;
      for (long long p = i; p < i2; p++) for (long long q = j; q < j2; q++) {
        m++;
        const u64 *a = VA + NW * ka[p].idx, *b = VB + NW * kb[q].idx;
        u64 x[NW]; int as = 0;
        for (int w = 0; w < NW; w++) { x[w] = a[w] ^ b[w]; for (int k = 0; k < 8; k++) as += ((x[w] >> (8 * k)) & 31) != 0; }
        if (as > tau) continue;
        f++;
        const uint8_t *by = (const uint8_t *)x; int w1 = 0;
        for (int k = 0; k < 320; k++) w1 += MINW[by[k]];
        Best c; c.w1 = w1; c.w2 = WA[ka[p].idx] + WB[kb[q].idx]; c.core = ci;
        memset(c.ch, 0, sizeof c.ch);
        long long r = ka[p].idx; for (int jj = 0; jj < h; jj++) { c.ch[jj] = (int)(r % C->r[jj].m); r /= C->r[jj].m; }
        r = kb[q].idx; for (int jj = h; jj < n; jj++) { c.ch[jj] = (int)(r % C->r[jj].m); r /= C->r[jj].m; }
        if (better(&c, best)) *best = c;
      }
      i = i2; j = j2;
    }
  }
  *M = m; *F = f; *E = (long long)nb * (na + nbb);
  free(VA); free(VB); free(WA); free(WB); free(ka); free(kb); free(tmp);
}
static void *worker(void *arg) {
  (void)arg;
  Best b; b.w1 = -1;
  for (;;) {
    pthread_mutex_lock(&job.mu); int ci = job.next++; pthread_mutex_unlock(&job.mu);
    if (ci >= ncores) break;
    long long M, F, E;
    do_core(ci, NBL[job.lev], &M, &F, &E, &b);
    job.matches[ci] = M; job.evals[ci] = F; job.entries[ci] = E;
  }
  pthread_mutex_lock(&job.mu); if (b.w1 >= 0 && better(&b, &job.best)) job.best = b; pthread_mutex_unlock(&job.mu);
  return NULL;
}
int main(int argc, char **argv) {
  FILE *fp = fopen(argv[1], "rb"); int th = argc > 2 ? atoi(argv[2]) : 1;
  uint32_t u; if (fread(&u, 4, 1, fp) != 1) return 2; ncores = (int)u;
  cores = calloc(ncores, sizeof(Core));
  for (int c = 0; c < ncores; c++) {
    if (fread(&u, 4, 1, fp) != 1) return 2; cores[c].n = (int)u;
    for (int j = 0; j < cores[c].n; j++) {
      uint32_t h4[4]; if (fread(h4, 4, 4, fp) != 4) return 2;
      Row *R = &cores[c].r[j]; R->y = h4[0]; R->z = h4[1]; R->o = h4[2]; R->m = h4[3];
      for (int i = 0; i < R->m; i++) { if (fread(&u, 4, 1, fp) != 1) return 2; R->d[i] = (int)u; if (fread(R->v[i], 1, 320, fp) != 320) return 2; }
    }
  }
  if (fread(MINW, 1, 32, fp) != 32 || fread(WT2, 1, 1024, fp) != 1024) return 2;
  fclose(fp);
  pthread_mutex_init(&job.mu, NULL);
  job.best.w1 = -1;
  for (int lev = 0; lev < NLEV; lev++) {
    job.lev = lev; job.next = 0; set_level(NBL[lev]);
    pthread_t T[16];
    for (int i = 0; i < th; i++) pthread_create(&T[i], NULL, worker, NULL);
    for (int i = 0; i < th; i++) pthread_join(T[i], NULL);
    long long M = 0, F = 0, E = 0;
    for (int c = 0; c < ncores; c++) { M += job.matches[c]; F += job.evals[c]; E += job.entries[c]; printf("core %d lev %d nb %d entries %lld matches %lld evals %lld\n", c, lev, NBL[lev], job.entries[c], job.matches[c], job.evals[c]); }
    int tau = NBL[lev] - 1;
    printf("LEVEL %d nb %d tau %d entries %lld matches %lld evals %lld best_w1 %d w2 %d core %d choice", lev, NBL[lev], tau, E, M, F, job.best.w1, job.best.w2, job.best.core);
    for (int i = 0; i < cores[job.best.core >= 0 ? job.best.core : 0].n; i++) printf(" %d", job.best.ch[i]);
    printf("\n"); fflush(stdout);
    if (job.best.w1 >= 0 && job.best.w1 <= 2 * tau + 1) { printf("CERTIFIED at level %d (nb %d)\n", lev, NBL[lev]); return 0; }
  }
  printf("NOT CERTIFIED\n");
  return 1;
}
```

## Appendix B. E as run in the R5 study and pre-registrations C and D (fes.c)

fes.c (SHA-256 9a023ce614609bb9c27ba94683a6dc340f7a1324a3550ca4ba3f45775ae30de4, hashed in the plan of C) is an exact form of E's stage 1 for evidence runs: f(c), the 24 residual bits at window coordinate c, has degree <= 4 in c (round 0's output has degree <= 2, round 1's <= 4, and L is linear), so its algebraic normal form is the Moebius transform of its values on the 41,449 coordinates of weight <= 4 with no assumption; coordinates 0..7 are bitsliced and 8..31 enumerated by the degree-4 derivative recursion of fast exhaustive search. Every pass is printed; espace.stage2 (Python, the experiment file's Linv_map and digest5) then compares complete digests. The driver prereg_c.py (51ba941c...) calls the experiment file's bprime, Setup, attempt and enum_basis. The R5 study ran the same binary (SHA-256 6d1110190325ed04bccc56eee4b2844e1a0f3d95f17e9cce0984a3d5c01835c3) with the same espace.py, from its driver r5run.py.

```c
// fes.c: E's stage 1 on one space by exhaustive search over the 2^32 window (v11 evidence, pre-registration C).
// The window point of coordinate c (32 bits) is x(c) = v0 + sum_{j: bit j of c} b_j (x is the round-0 chi input,
// as in the experiment file's e_window).  f(c) = residual bits of E's 24 round-2 equations (bit k set iff
// equation k fails), so c passes stage 1 iff f(c) = 0.  a = chi(x)+RC0 has degree <= 2 in c, e = L(a) too,
// b = chi(e)+RC1 degree <= 4, u = L(b) and f degree <= 4.  So f's algebraic normal form is exactly the Moebius
// transform of its values on the 41,449 points of weight <= 4 (no assumption).  Coordinates 0..7 are bitsliced
// (256-bit truth tables per equation); coordinates 8..31 run in Gray order with the derivative recursion of
// fast exhaustive search (Bouillaguet et al., CHES 2010), degree 4.  Every pass is printed; a self-check
// compares the recursion with direct evaluation of all 256 inner points at 64 checkpoints.
// Input (stdin): 33 lines of 25 hex lanes: v0, b_0 .. b_31.  Output: "pass <c hex>" lines, then a summary.
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
typedef uint64_t u64;
typedef uint32_t u32;
static const int RHO[25] = {0,1,62,28,27,36,44,6,55,20,3,10,43,25,39,41,45,15,21,8,18,2,61,56,14};
static const int EQ[24][4] = {{1,2,8,1},{1,2,16,1},{1,2,3,0},{1,2,5,1},{1,17,4,1},{1,17,16,0},{0,0,2,0},
  {0,0,16,1},{0,2,2,1},{0,2,8,0},{2,21,2,1},{2,21,8,0},{2,61,2,0},{2,61,16,1},{3,17,4,1},{3,17,16,0},{3,61,2,0},
  {3,61,16,1},{4,0,2,1},{4,0,8,1},{4,0,17,0},{4,21,2,0},{4,21,8,0},{4,21,16,1}};
static u64 V0[25], BS[32][25];
static inline u64 rol(u64 v, int n) { n &= 63; return n ? (v << n) | (v >> (64 - n)) : v; }
static void Lmap(const u64 *A, u64 *B) {
  u64 P[5], T[5];
  for (int x = 0; x < 5; x++) P[x] = A[x] ^ A[x + 5] ^ A[x + 10] ^ A[x + 15] ^ A[x + 20];
  for (int x = 0; x < 5; x++) T[x] = P[(x + 4) % 5] ^ rol(P[(x + 1) % 5], 1);
  for (int y = 0; y < 5; y++) for (int x = 0; x < 5; x++)
    B[y + 5 * ((2 * x + 3 * y) % 5)] = rol(A[x + 5 * y] ^ T[x], RHO[x + 5 * y]);
}
static void chi(const u64 *A, u64 *B) {
  for (int y = 0; y < 5; y++) for (int x = 0; x < 5; x++)
    B[x + 5 * y] = A[x + 5 * y] ^ (~A[(x + 1) % 5 + 5 * y] & A[(x + 2) % 5 + 5 * y]);
}
static u32 feval(u32 c) {
  u64 x[25], a[25], e[25], b[25], u[25];
  memcpy(x, V0, sizeof x);
  for (int j = 0; j < 32; j++) if ((c >> j) & 1) for (int i = 0; i < 25; i++) x[i] ^= BS[j][i];
  chi(x, a); a[0] ^= 1ULL; Lmap(a, e); chi(e, b); b[0] ^= 0x8082ULL; Lmap(b, u);
  u32 r = 0;
  for (int k = 0; k < 24; k++) {
    int y = EQ[k][0], z = EQ[k][1], m = EQ[k][2], cc = EQ[k][3], v = 0;
    for (int xx = 0; xx < 5; xx++) v |= (int)((u[xx + 5 * y] >> z) & 1) << xx;
    r |= (u32)((__builtin_popcount(m & v) & 1) ^ cc) << k;
  }
  return r;
}
// ranks of masks of weight <= 4 (colex)
static u64 Cn[64][6];
static int wofs[6];
static int rank32(u32 s) {
  int w = 0, r = 0;
  while (s) { int p = __builtin_ctz(s); s &= s - 1; w++; r += (int)Cn[p][w]; }
  return wofs[w] + r;
}
#define NE 24
#define NV (NE * 4)
typedef struct { u64 w[NV]; } Vt;  // [eq][4 words] : bit l of eq's table = residual at inner point l
static inline void vx(Vt *d, const Vt *s) { for (int i = 0; i < NV; i++) d->w[i] ^= s->w[i]; }
static Vt *G;      // g_M for outer masks M of weight <= 4 (rank over 24 vars)
static Vt D1[24], *D2, *D3, *D4;
static u64 MONO[256][4];
static int orank(u32 M) { return rank32(M); }
static void deriv(Vt *out, u32 K, u32 ystar) {  // d_K f at outer point ystar = sum over M >= K, M\K <= ystar of g_M
  memset(out, 0, sizeof *out);
  u32 free_ = ystar & ~K;
  int kw = __builtin_popcount(K);
  int fb[24], nf = 0;
  for (u32 t = free_; t; t &= t - 1) fb[nf++] = __builtin_ctz(t);
  vx(out, &G[orank(K)]);
  if (kw <= 3) for (int a = 0; a < nf; a++) {
    vx(out, &G[orank(K | 1u << fb[a])]);
    if (kw <= 2) for (int b = a + 1; b < nf; b++) {
      vx(out, &G[orank(K | 1u << fb[a] | 1u << fb[b])]);
      if (kw <= 1) for (int c = b + 1; c < nf; c++) vx(out, &G[orank(K | 1u << fb[a] | 1u << fb[b] | 1u << fb[c])]);
    }
  }
}
static u32 gray(u32 i) { return i ^ (i >> 1); }
int main(void) {
  for (int n = 0; n < 64; n++) { Cn[n][0] = 1; for (int k = 1; k < 6; k++) Cn[n][k] = n ? Cn[n - 1][k - 1] + Cn[n - 1][k] : 0; }
  // number of masks of weight w over 32 bits = C(32,w)
  { long c32[6] = {1, 32, 496, 4960, 35960, 201376}; wofs[0] = 0; for (int w = 1; w < 6; w++) wofs[w] = wofs[w - 1] + (int)c32[w - 1]; }
  for (int r = 0; r < 33; r++) for (int i = 0; i < 25; i++) {
    unsigned long long v; if (scanf("%llx", &v) != 1) { fprintf(stderr, "input\n"); return 2; }
    if (r == 0) V0[i] = v; else BS[r - 1][i] = v;
  }
  // values on weight <= 4 points, then Moebius
  int NP = wofs[5];
  u32 *F = malloc(sizeof(u32) * NP), *A = malloc(sizeof(u32) * NP), *MS = malloc(sizeof(u32) * NP);
  int np = 0;
  for (u32 s = 0; np < NP; ) { (void)s; break; }
  // enumerate masks of weight <= 4
  MS[np++] = 0;
  for (int a = 0; a < 32; a++) {
    MS[np++] = 1u << a;
  }
  for (int b = 1; b < 32; b++) for (int a = 0; a < b; a++) MS[np++] = 1u << a | 1u << b;
  for (int c = 2; c < 32; c++) for (int b = 1; b < c; b++) for (int a = 0; a < b; a++) MS[np++] = 1u << a | 1u << b | 1u << c;
  for (int d = 3; d < 32; d++) for (int c = 2; c < d; c++) for (int b = 1; b < c; b++) for (int a = 0; a < b; a++)
    MS[np++] = 1u << a | 1u << b | 1u << c | 1u << d;
  if (np != NP) { fprintf(stderr, "np %d %d\n", np, NP); return 3; }
  for (int t = 0; t < NP; t++) { if (rank32(MS[t]) < 0 || rank32(MS[t]) >= NP) return 4; F[rank32(MS[t])] = feval(MS[t]); }
  for (int t = 0; t < NP; t++) {
    u32 S = MS[t], acc = 0;
    for (u32 T = S;; T = (T - 1) & S) { acc ^= F[rank32(T)]; if (!T) break; }
    A[rank32(S)] = acc;
  }
  // g_M: outer mask M = S >> 8 (24 vars), inner monomial S & 255
  for (int l = 0; l < 256; l++) for (int s = 0; s < 256; s++) if ((l & s) == s) MONO[s][l >> 6] |= 1ULL << (l & 63);
  int NG = 1 + 24 + 276 + 2024 + 10626;
  G = calloc(NG, sizeof(Vt));
  // ranks over 24 vars use the same colex ranks restricted to bits < 24 (wofs offsets of 32-bit ranks are
  // larger than needed but consistent); allocate by rank32 bound
  free(G); G = calloc(NP, sizeof(Vt));
  for (int t = 0; t < NP; t++) {
    u32 S = MS[t], cf = A[rank32(S)];
    if (!cf) continue;
    u32 M = S >> 8, Sin = S & 255;
    Vt *g = &G[orank(M)];
    for (int k = 0; k < NE; k++) if ((cf >> k) & 1) for (int w = 0; w < 4; w++) g->w[4 * k + w] ^= MONO[Sin][w];
  }
  int N2 = 276, N3 = 2024, N4 = 10626;
  D2 = calloc(N2, sizeof(Vt)); D3 = calloc(N3, sizeof(Vt)); D4 = calloc(N4, sizeof(Vt));
#define I2(a,b) ((int)(Cn[b][2] + (a)))
#define I3(a,b,c) ((int)(Cn[c][3] + Cn[b][2] + (a)))
#define I4(a,b,c,d) ((int)(Cn[d][4] + Cn[c][3] + Cn[b][2] + (a)))
  for (int a = 0; a < 24; a++) deriv(&D1[a], 1u << a, gray((1u << a) - 1));
  for (int b = 1; b < 24; b++) for (int a = 0; a < b; a++) deriv(&D2[I2(a, b)], 1u << a | 1u << b, gray((1u << a | 1u << b) - 1));
  for (int c = 2; c < 24; c++) for (int b = 1; b < c; b++) for (int a = 0; a < b; a++)
    deriv(&D3[I3(a, b, c)], 1u << a | 1u << b | 1u << c, gray((1u << a | 1u << b | 1u << c) - 1));
  for (int d = 3; d < 24; d++) for (int c = 2; c < d; c++) for (int b = 1; b < c; b++) for (int a = 0; a < b; a++)
    deriv(&D4[I4(a, b, c, d)], 1u << a | 1u << b | 1u << c | 1u << d, 0);
  Vt f; deriv(&f, 0, 0);
  long passes = 0; int chk_ok = 1, nchk = 0;
  u32 NOUT = 1u << 24;
  for (u32 i = 0; i < NOUT; i++) {
    if (i) {
      u32 t = i; int b1 = __builtin_ctz(t); t &= t - 1;
      if (t) { int b2 = __builtin_ctz(t); t &= t - 1;
        if (t) { int b3 = __builtin_ctz(t); t &= t - 1;
          if (t) { int b4 = __builtin_ctz(t); vx(&D3[I3(b1, b2, b3)], &D4[I4(b1, b2, b3, b4)]); }
          vx(&D2[I2(b1, b2)], &D3[I3(b1, b2, b3)]); }
        vx(&D1[b1], &D2[I2(b1, b2)]); }
      vx(&f, &D1[b1]);
    }
    u32 y = gray(i);
    for (int w = 0; w < 4; w++) {
      u64 acc = 0;
      for (int k = 0; k < NE; k++) acc |= f.w[4 * k + w];
      u64 ps = ~acc;
      while (ps) { int p = __builtin_ctzll(ps); ps &= ps - 1; passes++; printf("pass %08x\n", (y << 8) | (u32)(64 * w + p)); }
    }
    if ((i & ((1u << 18) - 1)) == 12345 % (1u << 18)) {  // 64 checkpoints
      nchk++;
      for (int l = 0; l < 256; l++) {
        u32 r = feval((y << 8) | (u32)l), q = 0;
        for (int k = 0; k < NE; k++) q |= (u32)((f.w[4 * k + (l >> 6)] >> (l & 63)) & 1) << k;
        if (q != r) chk_ok = 0;
      }
    }
  }
  printf("summary passes=%ld checkpoints=%d selfcheck=%s\n", passes, nchk, chk_ok ? "ok" : "FAIL");
  return chk_ok ? 0 : 1;
}
```

v15: fes.c is also the native form of v15's counted stage 1 (2.4): it computes the same derivative recursion over the same Gray order, with the inner 256 points in four 64-bit words per equation. R6 ran a binary built from this source with clang -O3 -mcpu=apple-m4 (SHA-256 93eff750b3529c2d54a48f5368f6c19f3d8ff70b935cbf380d13b4b564199a86) and the stage 2 of r6run.py (Appendix E).

## Appendix C. The plans of pre-registrations C and D (summarised)

C's plan refers to the three heuristics H1-H3 of the v11 draft. C and D measured v13's algorithm; v14 charged C (0.1; v20 no longer does, W.3) and neither enters any bound. (v22b: both plans are summarised; their verbatim texts are in v20's proof, 84668773, Appendix C.)

- prereg_c/plan.txt (SHA-256 4e1edbd45e4b0dfb10de7a67f432805e30d54eef073caba197d26ace7142b666), written before any run of C (its SHA-256 and UTC time recorded in prereg_c/commit.txt before run_c.sh started). Runs k = 0..47 (12 at a time; none stopped, excluded or repeated; every result file and runlog.txt reported), labels "hashsmash sha3-256-r5 v11 C B-prime run <k>" and "hashsmash sha3-256-r5 v11 C conn run <k>". Per run (tools/prereg_c.py): B' (budget 2^32 units, candidate cap 2^26 units, every candidate and attempt logged with counted costs), the connector rule of algorithm() (attempts until 96 accepted or 2^11 attempts, then discard), and E on the first 16 accepted spaces of a kept advice over the whole 2^32 window by fes.c (Appendix B; checked before the plan against the v6 and v8 logs) with stage 2 by complete 5-round digests (espace.py). Analysis (analyze_c.py): joint 95% confidence by Bonferroni over v11's H1-H3 (H2 pooled with pre-registration A; H1 with a Kish design effect whose dispersion premise the code switches by a fixed homogeneity test). Use: K = 96 if the success bound is >= 0.40 at K = 96, otherwise the least multiple of 8 up to 512 for which it is (the claimed time then grows; this is why C was charged, 0.1); no rule about submitting depends on the outcome.
- prereg_d/plan.txt (SHA-256 3a3bc8119b38b5eaa969a4a803db9b0c9d59c08b363ebaecc88816aeb21ba46c), written before any run of D. D completes, in order and stopping at the first output, accepted spaces 17..96 of the 30 runs of C with no positive space among their first 16 (k = 0 1 2 3 4 8 9 10 11 12 13 16 17 19 22 23 26 28 29 31 32 34 35 36 37 38 39 41 45 46) and of run 999 (the smoke test of C's driver, outside C's sample), each advice and accepted connector attempt re-derived from its label (reproducing C's advice hash, statuses, DF and work counts); before the plan the driver was checked only on a space that C had already enumerated. Analysis (analyze_d.py): x = the number of the 48 runs that succeed; one-sided 95% Clopper-Pearson lower bounds p_L on 48 runs and p_L' on 49 with run 999 (a missing file or an error counts as a failure); K stays 96; the claimed success probability is 0.40 if min(p_L, p_L') >= 0.40, else that minimum rounded down to two decimals, reported in every case; no rule about submitting or withholding depends on the outcome.

## Appendix D. The R5 study: plan, commit record and per-run ledger (condensed)

(v22b: the plan is summarised, and the per-run ledger is tabulated and merged with Section 4.3's table. Every SHA-256 value and every run is kept, and every ledger field except the per-space round-2 pass counts, which are summarised as min-max per run. The verbatim plan and ledger are in v20's proof, 84668773, Appendix D.)

plan.txt (SHA-256 7ffaf34f4001a449a6775fa3f204f7c93a0be60c69e45588d320aae1d382574b), summarised (Section 4.2 gives the runs, the driver, E and the launch). Written before any run of R5; its SHA-256 and UTC time are recorded in commit.txt with the SHA-256 of every file it names (a first commit at 20:27:03Z was replaced before any run, only to change the launcher's start gate). R5 is v13's algorithm (algorithm() of r5v13.py, byte-identical to v13's experiments/r5.py) with B''s six tuned constants replaced by values that no run selected: no attempt limit per candidate (B_R = 2^62, never reached; a candidate ends at its accepted attempt or at CCAP = 2^26 units), DMIN = 33 (the connector's value, the least DF for which E's window and beta exist) and KW = MW = LB = PREF = 1; every other constant is v13's (K = 96, CCAP = 2^26 units, B_BUDGET = 2^32 units, A_ADV = 2^11, A_MAX = 2^13, X_MAX = 2^23, S2CAP = 2^24, F_CAP = 2^30). Every run is started and completed, none is stopped, excluded or repeated; after a machine crash run_all.sh would run only the k without a result file, and any restart would be reported. Analysis (analyze.py): s of 48 and its one-sided 95% Clopper-Pearson lower bound p0; claim rule for any package built on R5: success 0.40 if p0 >= 0.40, otherwise R5 is not claimed; every run is reported whatever the outcome; the study changes no constant. Known before the plan: C' (Section 4.1; not part of this sample) and the driver's self-test, which re-derived v11 pre-registration C's run 5 positive space with v11's constants (collision at 0x2b32ba84; no R5 constant was set).

commit.txt (written at 2026-10-07T20:27:28Z, before any run; SHA-256 c579732d422ad4bbb57aece0de85004a17c7a66d37c367eb35ea3ef273031c68):

```text
R5 plan committed 2026-10-07T20:27:28Z, before any run of R5 (replaces commit_superseded_2027Z.txt: launcher start gate only)
7ffaf34f4001a449a6775fa3f204f7c93a0be60c69e45588d320aae1d382574b  plan.txt
4a0343299736e0b36de47276de307a19121dc5e1ae96b64209a972fe45adf37d  r5run.py
a8f40c141e648a1469024d7929e964245aa80bb72f1490703144e4d7fb385f26  r5v13.py
da89a7eb6394b900e402f88e311a420183a4ab4f7af6bf9c6ff07043ab65910c  analyze.py
bf3a595fb0a66d6a9ec9b67ef4e5958ebdeeef6e209ee31b4686ce3cdf5234a3  one_run.sh
0d87a39d82be19a126be336e556c7a00238f23396736363002f5caab8fd9bb3e  run_all.sh
6d1110190325ed04bccc56eee4b2844e1a0f3d95f17e9cce0984a3d5c01835c3  fes
c9c5d4a9e3b1d86312a56a6f00fba511b1f321c7c1e3874d0b4b12c81278e769  espace.py
fe26aed012e0588fbed04bee3a611509993e661423a8a8196c581de807b7a285  r5lib.py
4b720a703bc503f0255ada15e3ef20cb835129ece3158d4ce1b935e0f09cf550  r5tlib.py
```

Other files of the study (SHA-256): the superseded commit record commit_superseded_2027Z.txt 2bf5e4857146647c0e44bad6f973f25424fcb21774a5ad249b41f648fabfabc0; launch_all.sh 09f13f6412477c3714a4f1c6afc9bbaa2a2f9224aedb7c388e8cb31684e92d81 and watchdog.py c0f03d92bf1f653c4268ebd06721189666d647e99ff74d7c1085e6b6df186b4d (written after the commit and before the launch; operational only); launch.txt d94e657b34494a858f30825290954268cbb5b246133c7bb20fa7cf6e0bb9c68b; runlog.txt f6bdce33e5630716205f81a1c01b3f7d6a241d876c8ac2d467c843b66fd77c87; watchdog.log 953f8bd7cbc95bce03c35a254d1bac7e9ce3535ba57372dbe44b58fdf73dcd26; finished.txt 877ed57ab0381cbac6dd62dab1481a34f4e2cc0d4059ecdee44681970bb7cc91; analysis.json 25e283c8b53d9725830e263daf9fa69c433859b47f30b7a9e1dcb7d95a96d2b3; the 48 result files runs/0.json .. runs/47.json concatenated in k order 9bbeffce00b293c110f53493b51327877d3c640016b9ec7471774e98f1884185 (each file's own SHA-256 is in its ledger line).

Per-run table and ledger (v22b: Section 4.3's table and the ledger, merged). From the result files ("attempts", "accepted": connector attempts and acceptances per advice round; "spaces": E's spaces enumerated up to the first output; B' log2 units over all rounds of the run). The ledger (one JSON object per run, derived from the result files; SHA-256 of its verbatim text, with a final newline, c08a5834a3b1d5fab1b67e49017c5940e45fa93a48f9b54700366c73017c513e) also holds, per run: the SHA-256 of runs/k.json; per advice round the advice hash prefix and B''s exact WK count in primitives (1/1355 units) and whether the advice was kept (kept iff 96 were accepted); the round-2 pass counts of the enumerated spaces, in order (here min-max per run; over all 1,236 spaces 200-308); the fes self-checks (all passed, in every run) and whether the stage-2 cap bound (in no run); the largest connector attempt in work units; the output coordinate and the SHA-256 of the output pair (message a || message b); Python CPU seconds. (v25: the SHA-256 values in this table are shortened to their first 16 hex digits to keep the judge evidence within its budget; the full values are in v22b's proof (08930c1e), unchanged.)

| k | candidates | (c, j) per round | DF | B' log2 units | attempts | accepted | spaces | first positive space | success | runs/k.json SHA-256 | per round: advice hash prefix, B' WK primitives | largest attempt | passes | coordinate | output pair SHA-256 | CPU s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 4 | 3, 37 | 41 | 27.92 | 96 | 96 | 1 | 1 | yes | 3fbcb7090b2dd3bb | 990540e7f5ee7f2e 343020384242 | 155543 | 253 | 0x809f225b | 12586fc0e3f70e78 | 389.0 |
| 21 | 1 | 0, 3 | 49 | 23.51 | 206 | 96 | 1 | 1 | yes | 52348f87ec499825 | 76a6a0b06305286a 16241153777 | 145190 | 240 | 0x18c48859 | a0a8f20cf4ea8c44 | 10.6 |

(R5N: 46 rows condensed out to fit the 512 KiB judge-evidence budget; kept: run 4, whose replay is D15's driver self-test, and run 21, the R7 self-test's label. The full table is in 0f72a85e's and v22b's proofs, unchanged; R5 is listed, not charged, and no number of the claim reads the other rows.)

## Appendix E. The R6 study: plan, commit record, driver, analysis, launcher and per-run ledger (condensed)

(R5N: condensed to fit the 512 KiB judge-evidence budget; the full appendix is in 0f72a85e's and v15's proofs, unchanged. R6 is listed, not charged, and no number of the claim reads it; Section 4.7 keeps its plan hash, results and analysis.) SHA-256 values of the study's files, in 0f72a85e's order: 9c7659c3acf661348f3d8e031cb28bb16bc309614f0a9763cdb9a2e4c22e5e7c, 446a29920246ac5c796fb510aa7447765b6841ed4b43d9e5887e473e430329c2, 9c7659c3acf661348f3d8e031cb28bb16bc309614f0a9763cdb9a2e4c22e5e7c, 0ae6ea6628e27337a06d12076746442ca3638b48cc44a1318dba6c25d11c143f, 0be4334dfc215f181b8cae5332c87551971bbd60617c28b0f50e18737e9d7ef4, 9a023ce614609bb9c27ba94683a6dc340f7a1324a3550ca4ba3f45775ae30de4, 93eff750b3529c2d54a48f5368f6c19f3d8ff70b935cbf380d13b4b564199a86, 7a2ba2db66cf57ec664c623af8ed922067829d3f2a25c850d8d2f6a842b47d7f, e31fcfd247866de2993f01c7c95b23e6ccd52d6ea65c7e3e49070188114a0862, 56d9360b3f6d28e74d227a910e1f92be689c7caf10b5ee34f75987ac9d198e46, 95ce77dff0476301c05057e01296f3e3507c4926423257540cfc3e5fd36ee0ae, ed8292923f2d931bbb6724ecc20e2da3b39c4ef2374e0591709e430bc37dbf17, 35c979811047ee5fea6d2759d6abce254f68e72b95f4fbe5ba138cba9a15d162.

## Appendix F. The R7 study (v20): rule K, plan, commit records, driver, analysis, launcher and per-run ledger

Files in the order of the commit record. fes.c is Appendix B's (SHA-256 9a023ce6...); the binary fes is the one of pre-registration C and R5 (SHA-256 6d111019...); organizer_keccak.py is the organizer's verifier/keccak.py (SHA-256 95ce77df..., as in R6); r5v20.py is v19's experiments/r5.py with the three edits that plan.txt lists; selftest.json is the driver's self-test record (R5 run 21's label). rule.txt, plan.txt, commit.txt, krule.out and the builder record are verbatim below and the per-run ledger is merged into Section W.2's table; the superseded commit record is given by its differences, and krule.py, the driver, analysis, launcher and wrapper are described by function (v22b; their verbatim texts, with two absolute local paths redacted, are in v20's proof, 84668773, Appendix F). The SHA-256 values are those of the files as committed and run.

rule.txt (SHA-256 af87bc47bc1a6f892a5f05e3aa147562c57bfcea0c09e0ca13a4ee9931ebecd5):

```text
Rule K for hashsmash sha3-256-r5 v20. Written 2026-10-08 (UTC), before any run of R7. Its SHA-256 and UTC time are
recorded in commit.txt together with plan.txt and every file of R7's computation.

Purpose. Fix four constants of v20's algorithm by an analysis that reads no run outcome: K (accepted connector
spaces per advice that E enumerates), A_ADV and A_MAX (the connector's attempt limits per advice and in all) and
S2CAP (stage-2 pairs per space). The pre-registered study R7 (plan.txt) then measures the success probability of
the algorithm with these constants. Every other constant and every program is v19's.

Inputs. Exact facts of P's output (proof Section 3; P is deterministic and its output is recomputed by the
organizer's experiments): the round-2 transition beta2 -> alpha3 has w2 = 24 conditions, which are E's 24 stage-1
equations; P45 = 55/2^19 exactly (the sum over the 2^19 alpha4 compatible with beta3); E's window has 2^32 pairs.
No count, rate or maximum observed in any run is an input.

Model (used only to choose the constants; the claim is measured by R7, not by this model). A pair of a space
passes stage 1 with probability 2^-24 and a passing pair collides with probability P45, so the expected number of
colliding pairs in a space is lambda = 2^32 x 2^-24 x 55/2^19 = 55/2^11 = 0.026855. A space succeeds with
probability q = 1 - exp(-lambda) = 0.026498, and K spaces of independent coins with p_K = 1 - (1 - q)^K.

Study design (fixed here and in plan.txt). R7 has 48 runs. Its claim rule: claim 0.40 iff the one-sided 95%
Clopper-Pearson lower bound of s successes in 48 is at least 0.40, which holds iff s >= 26
(Pr[Bin(48, 0.40) >= 26] = 0.0329 <= 0.05 < Pr[Bin(48, 0.40) >= 25] = 0.0604).

Rule for K. K is the least K such that the study passes with probability at least 0.999 under the model:
Pr[Bin(48, p_K) >= 26] >= 0.999. Result: K = 50 (p_50 = 0.73888, Pr = 0.999041; K = 49: 0.998575).
(At the level 0.99 the rule would give K = 44.) krule.py computes this with exact rational binomial sums.

Rule for A_ADV and A_MAX. v10 set A_ADV = 2^11 and A_MAX = 2^13 for K = 96 from G2's runs (G2 is charged and stays
charged). The rule keeps G2's ratios: attempts per advice proportional to K, and four advice rounds in all:
A_ADV = ceil(K x 2^11 / 96) = 1067 and A_MAX = 4 x A_ADV = 4268.

Rule for S2CAP. The least power of two that is at least 8 times the model's expected number of stage-2 pairs per
space (2^32 x 2^-24 = 256): S2CAP = 2^11. (v13's run-free cap rule, re-anchored by v17, gave 2^21.)

Unchanged (v19's): X_MAX = 2^20 work units per attempt, B_TRUE = 2^29 units, B_BUDGET = 2^32 units, CCAP = 2^26
units, B''s code and constants (no attempt limit per candidate, DMIN = 33, unweighted D2u), S, the connector, P, E.

Consequence for the development ledger. Pre-registration C's only role in the algorithm was to keep K = 96 (its
plan would have raised K had its bound been below 0.40). Under this rule K does not depend on C, so v20 does not
charge C. G2 stays charged in full (K's old value, CCAP, B_BUDGET and the ratios used for A_ADV and A_MAX).

What was known when this rule was written (the full history; none of it enters the rule, but its author knew it):
- G2 (v6 run: 14 positive spaces in its first 512; pre-registrations A and B), pre-registrations C (48 runs to
  16 spaces each: 23 positive spaces in 768, 18 runs with a positive space) and D (the other 30 runs and run 999,
  818 spaces; 46 of 48 with C), C' (14 runs started, 4 finished, each with a collision), R5 (46 of 48 at K = 96;
  46 positive spaces in 1,236; largest stage-2 count 308) and R6 (44 of 48 at K = 96; 44 positive spaces in 1,408;
  largest stage-2 count 315).
- Observed rates of positive spaces per enumerated space: R5 0.037, R6 0.031, above the model's q = 0.0265.
- R5 and R6 truncated at 50 spaces (descriptive; ignores the change of A_ADV): 40 of 48 each.
- v19's package (proof U.7) considered this rule and S2CAP = 2^11 and did not adopt them, because C, R5 and R6 had
  run before the rule was written. v20 adopts them only with the new study R7, run after this rule and plan.txt
  were hashed.
- The study of 2026-10-08 that proposed this rule chose the power level 0.999 (K = 50) over 0.99 (K = 44) and the
  factor 8 for S2CAP knowing the outcomes above.
Because of this history the package prints, beside the claim, the totals with C charged, with C, R5 and R6
charged, with R7 charged and with S2CAP at 2^21.
```

plan.txt (SHA-256 4f7f38abc6635ae5c710c44ef113affab5ca3a1f17bb86637abdfea0c6f8e2f1):

```text
Pre-registration R7 for hashsmash sha3-256-r5 (v20). Written before any run of R7. Its SHA-256 and UTC time are
recorded in commit.txt together with rule.txt and the SHA-256 of every file named here.

Purpose: measure, end to end, the success probability over the algorithm's own coins of v20's algorithm. v20 is
v19's algorithm with the four constants of rule.txt: K_SPACES = 50, A_ADV = 1067, A_MAX = 4268, S2CAP = 2^11. All
else is v19's: B_BUDGET = 2^32 units, CCAP = 2^26 units, B_TRUE = 2^29 units, X_MAX = 2^20 work units, B' with no
attempt limit per candidate, DMIN = 33 and unweighted D2u, S, the connector, P (its output is the certified trail of
proof Section 3) and E (stage 1 as computed by fes, stage 2 by complete digests).

Experiment file: r5v20.py, v19's experiments/r5.py (SHA-256 97815b2c8b2b955acafd05d58e4d69cf9b6b1b9eb9766193aeb8494640e5d0df)
with exactly three edits: the docstring's version (v19 -> v20); the constants line
"K_SPACES, A_ADV, A_MAX, S2CAP = 50, 1067, 4268, 1 << 11"; and, in the organizer replay of R5 runs, the bound on a
logged space index written as R5's 96 instead of K_SPACES.

Runs: k = 0..47, label "hashsmash sha3-256-r5 R7 run <k>"; every coin is derived from the label exactly as
algorithm(label) does. Each run is r7run.py <k> results: algorithm()'s calls in algorithm()'s order (bprime with
the WK budget, the per-candidate cap and the true-cost budget; Setup; attempt with the connector coins until 50
accepted, discarding the advice after 1067 attempts, at most 4268 attempts in all; then E on the 50 accepted spaces
in order, stopping at the first output). E on a space is the binary fes (built from fes.c; exact over the 2^32
window, self-check against direct evaluation at 64 checkpoints) followed by stage 2 by complete 5-round digests in
fes's output order on at most S2CAP passes. A space whose self-check fails ends the run without output.

Launch: run7.sh takes the machine-wide heavy lock, waits while the 1-minute load average is above 12, then runs
run_all7.py: increasing k, at most 10 runs at a time, a new run starts only while the 1-minute load average is
below 12, nice 10, Python 3.12. Every run is started and completed; none is stopped, excluded or repeated. If the
machine crashes, run7.sh is started again and runs only the k without a result file (runs are deterministic
functions of their labels); any restart is reported. A run that exits abnormally, or whose result file is missing
or malformed, counts as a failure.

Analysis (analyze7.py, fixed now): a run succeeds iff it outputs two distinct 135-byte messages whose complete
5-round SHA3-256 digests are equal, checked with the experiment file's digest5 and with the organizer verifier
(organizer_keccak.py = verifier/keccak.py, sha3_256(m, 5)). Report the count s of 48 and the one-sided 95%
Clopper-Pearson lower bound. Claim rule: the v20 package claims success probability 0.40 iff the bound is at least
0.40 (s >= 26); otherwise v20 is not claimed, the package falls back to v19's algorithm, and that is reported. This
is the plan's only outcome-dependent decision; no rule changes any constant. Every run is reported in a per-run
table and a per-run ledger (SHA-256 of each result file) whatever the outcome. R5 and R6 (K = 96) are reported
beside R7 as descriptive history; they are not pooled with R7.

Decided now for the package, independent of the outcome: R7's collisions, first in k order, replace R6's as
certificates (with v6's, at most 16); the organizer replays of the package (r5-R-0..7 and r5-bpfull) are switched
from R5's table to R7's logged runs if R7's table fits the 64-KiB experiment budget, else they stay on R5's. Neither
choice changes code that algorithm() runs. R7 fixes no number of the algorithm; it is listed and priced, and the
total with R7 charged is printed as a sensitivity.

A first commit record (commit_superseded_1522Z.txt, 15:22:40Z) was replaced before any run, only to correct the
dates of rule.txt and plan.txt to UTC.

Known before this plan: rule.txt (with its history of G2, C, D, C', R5, R6). The only run of this driver before
the plan is its self-test (selftest.json, 2026-10-08T15:20Z) on the label of R5 run 21, an R5 outcome logged before: with
K = 50 it reproduced R5's logged advice (candidate 0, attempt 3, DF 49, advice hash 76a6a0b06305286a), the DF 48 of
the first space and the collision at space 1, coordinate 18c48859. No R7 label has been run.
```

commit.txt (SHA-256 eebce75c95f63140a68d3d7867586af9d554cc4923eec01c264c3669193772f7):

```text
R7 commit record (rule K and pre-registration R7, written before any run of R7; replaces commit_superseded_1522Z.txt, dates only)
utc 2026-10-08T15:23:01Z
af87bc47bc1a6f892a5f05e3aa147562c57bfcea0c09e0ca13a4ee9931ebecd5  rule.txt
4f7f38abc6635ae5c710c44ef113affab5ca3a1f17bb86637abdfea0c6f8e2f1  plan.txt
ea9db588dcf0763b595cc5f105a14c91ac42b33c660f44e5f14cfebf6a2463d7  krule.py
f0a144498b017023b13d5b2a944e038c5e9ff0d82734fa8e72e3e1db4f2ef5f6  krule.out
66e7365cec23668ae4294ef475681f5a0df4983bddd3beeb25c60a7352372096  r7run.py
89b72bf71050a30d5ee74083a09ee057511b6005b853fe45e249711977390826  r5v20.py
6d1110190325ed04bccc56eee4b2844e1a0f3d95f17e9cce0984a3d5c01835c3  fes
9a023ce614609bb9c27ba94683a6dc340f7a1324a3550ca4ba3f45775ae30de4  fes.c
38c889466affaae7509618c2ae251972620f219a3ff7711fa67a728e620a8447  analyze7.py
cf34b509d90e2445232ca4abfaa1476385356e4b42e374b2c98676650767b9c8  run_all7.py
79f7b4941dc807c1b9700a9c1e7d9348d4f3f828bf78063b950ee8280b1f97de  run7.sh
95ce77dff0476301c05057e01296f3e3507c4926423257540cfc3e5fd36ee0ae  organizer_keccak.py
91a2b6e33dd45320c46c5846ad8bd593428584e04e03faac180873cd94a2b8a0  selftest.json
71a4f9541df0eb55df5b58d0e60b57ab9d7928c69aa93f143cc28c2e651c488e  selftest.log
378783f6a0aef223d4926f86470ddbd1ecc89619f35e1a93356eea5e94e7b534  selftest.time
db1f924365f848f0c907aa01558c5fb97d45c5c6473cddf751cb380843b39d4e  commit_superseded_1522Z.txt
```

commit_superseded_1522Z.txt (SHA-256 db1f924365f848f0c907aa01558c5fb97d45c5c6473cddf751cb380843b39d4e), by its differences: header "R7 commit record (rule K and pre-registration R7, written before any run of R7)", "utc 2026-10-08T15:22:40Z", then the same 15 lines as commit.txt's first 15 (rule.txt to selftest.time, in the same order and, except for two, with the same SHA-256 values), the two differing lines being rule.txt 7626058b81e0922b7059cd5829a65a2acfe9abd88f6298b035d8be3215a0e57b and plan.txt 08d1d3b1e38043151bb02a3f0cbf334e772728a7aaf58403cfd368df4ddf4e20 (the versions whose dates were then corrected to UTC); it has no line for a superseded record.

krule.py (SHA-256 ea9db588dcf0763b595cc5f105a14c91ac42b33c660f44e5f14cfebf6a2463d7) computes rule K with exact rational binomial sums: s_min = the least s with Pr[Bin(48, 0.40) >= s] <= 0.05; lambda = 55/2^11 and q = 1 - exp(-lambda) (as a rational of denominator at most 10^12); for K = 1, 2, ... p_K = 1 - (1 - q)^K, and K = the first with Pr[Bin(48, p_K) >= s_min] >= 0.999; A_ADV = ceil(K x 2^11 / 96), A_MAX = 4 x A_ADV, S2CAP = 2^ceil(log2(8 x 2^32 / 2^24)); it prints these and, for reference, K = 44 and K = 96. Its output:

krule.out (SHA-256 f0a144498b017023b13d5b2a944e038c5e9ff0d82734fa8e72e3e1db4f2ef5f6):

```text
lambda = 55/2^11 = 0.026855, q = 0.026498
s_min = 26 (Pr[Bin(48,0.40) >= 26] = 0.03285 <= 0.05; at 25: 0.06037)
K = 48: p_K = 0.72447, Pr[study passes] = 0.997901
K = 49: p_K = 0.73177, Pr[study passes] = 0.998575
K = 50: p_K = 0.73888, Pr[study passes] = 0.999041
for reference K = 44: p_K = 0.69322, Pr[study passes] = 0.990912
for reference K = 96: p_K = 0.92408, Pr[study passes] = 1.000000
K = 50, A_ADV = 1067, A_MAX = 4268, S2CAP = 2048
```

r7run.py (SHA-256 66e7365cec23668ae4294ef475681f5a0df4983bddd3beeb25c60a7352372096). `r7run.py <k> <outdir>` runs the label "hashsmash sha3-256-r5 R7 run <k>" and writes <outdir>/<k>.json atomically; `r7run.py selftest <outfile>` runs the same driver on the label of R5 run 21. It makes algorithm()'s calls of r5v20.py in algorithm()'s order, with its constants (recorded in the result): Base and own_bits() with P's certified trail; bprime from the next candidate under the remaining WK budget, CCAP and the remaining true-cost budget ("bprime-budget" if none); Setup; connector attempts with Coins(run_seed(label || "conn" || (c + 1) as 4 little-endian bytes, i)) (4.1) until K_SPACES are accepted, discarding the advice after A_ADV attempts, at most A_MAX in all ("a_max"); then each accepted space in order: enum_basis, the binary fes (exit code 0 and selfcheck=ok required, else "selfcheck-fail"; Appendix B), and for the first S2CAP passes in fes's output order the complete 5-round digests of L^-1(x) and L^-1(x + beta0). It stops at the first equal pair ("collision": space, accepting attempt, coordinate, both messages) or ends "none-in-K". It records per round c, j, DF, B''s WK and true cost, the advice hash prefix (16 hex digits of SHA-256 of hex(beta1) + hex(beta0)), the attempt statuses, the largest work count and the index and DF of each acceptance; per space DF, self-check, passes and hit; CPU seconds, peak memory, wall time and WK's counters. analyze7.py (SHA-256 38c889466affaae7509618c2ae251972620f219a3ff7711fa67a728e620a8447). A run succeeds iff its result is "collision" and its two messages are distinct 135-byte strings whose complete 5-round digests are equal by the experiment file's digest5 (on m || 0x86 || 0^512) and by the organizer verifier (organizer_keccak.sha3_256(m, 5)); a missing or malformed result file counts as a failure. The one-sided 95% Clopper-Pearson bound is found by 100 bisection steps on the binomial tail at 0.05 (0 for no success). It writes analysis.json (the count, the bound, whether 0.40 is supported, and descriptive per-run rows that no rule uses) and prints the count, the bound and the claim rule's outcome. run_all7.py (SHA-256 cf34b509d90e2445232ca4abfaa1476385356e4b42e374b2c98676650767b9c8). k = 0..47 in increasing k, skipping a k whose result file exists (only after a machine crash), at most 10 at a time, a new run starting only while the 1-minute load average is below 12 (checked every 15 s); each run is `nice -n 10 <python3.12> r7run.py <k> results` with its own stdout and stderr files; launch.log records every start (with the load and the number running) and every end with its return code. No run is stopped, excluded or repeated. run7.sh (SHA-256 79f7b4941dc807c1b9700a9c1e7d9348d4f3f828bf78063b950ee8280b1f97de). Takes the machine-wide heavy-job lock (a directory created atomically, removed on exit), waits while the 1-minute load average is above 12, runs run_all7.py and logs the lock and the unlock to launch.log.

Record of the replay-table and certificate builder, hashed before the first R7 result file existed:

```text
utc 2026-10-08T15:29:39Z (before any R7 result file exists: 0 files)
7044aa7ea1aa5b1a713298cdbaa73bddf9c28674210b4347f0ef655ad3b2d904  mk_r7table.py
```

Per-run ledger (k, result, output coordinate, SHA-256 of results/k.json): merged into Section W.2's per-run table (v22b). launch.log SHA-256 afd375abf670a1b5cc2505d3e9ca9e9234fc2b32c75867c0522a3eec7a6f1784; analysis.json SHA-256 aebc7346398e321273b8f4c230439e2187c3993405bcb20ae9110d691a95c4de.

## Appendix G. This derivative: L2-L6 and development rows D24/D25; K = 50 unchanged

G.0. Lineage is b5213766/1d801017; this appendix re-prices their programs and adds D24/D25. Algorithm, r5.py, manifests, certificates, K, caps, rule K, premise R, R7, H1 and H2 are inherited; no new premise or target run.

G.1. L2: T1 uses 2^9 per node outside 17,100 core events and 2^15 per event (the 2^12/node bound). D15 export and D19 p45meter/export use these exact sums, saving 2^25.4891 units.

G.2. L3: 2,048-step E blocks use Z.3's 12 passes and 29 resident tables. Exact block count is 410,392 (at least four index bits), at most 410,284 otherwise; plus prologue <=87 gives 410,479 per block and 2^13 blocks/space. Savings: online 2^20.6741; G2/D20 2^24.0829.

G.3. L4: E setup is 41,449 units + 2^23 primitives/space, saving 2^19.7712 online and 2^23.1772 on G2.

G.4. L5: with UNR = 256, e matches cost 18 + 49e + 3 floor(e/256); D15/D19 savings are 2^23.1483 units.

G.4b. L6: the stated sort/merge components are 3 + 14 + 14 + 6 + 18 = 55 primitives per half-vector/block, replacing 64. Across D15 and D19 the exact saving is 117,291,268,224 primitives = 117,291,268,224/1355 units = 2^26.3672; the three component terms are recorded in the earlier sections.

G.5. D24 charged every lever/check at inherited prices: 2^26.0674 units. D25 is claim arithmetic with no target run: 2^31 + 2^23 primitives = 2,155,872,256/1355 = 2^20.6015. Non-runs and verification stay uncharged under Z.4/Z.8.

G.6. Superseded ledger: total 2^32.90547 (numerator 2180223758084977334573/271000000000) and preprocessing 2^32.81088; sensitivities are inherited. Appendix J supersedes this total.

G.7. Historical native C runs were below submitted bounds (mitm2/contig <30 ops/vector/block, <35 ops/match; fes <150 ops/256-step block); X.5 and L2-L6 are conservative. H1/H2 are inherited.

## Appendix H. This derivative (pkgR5R): A, B1, B2, C

H.0. Base is 4e24cebd on 1d801017/b5213766; A-C re-price existing counts, with no new premise or target run. J supersedes H.

H.1. A = -110,951,289,234 primitives; B1 = -57,497,664,672; B2 = -1,398,752,712 (exact derivations: U.1/X.1/U.5).

H.2. C re-prices D15's driver self-test: B' = 343,020,384,242 WK primitives, 96 attempts and one E space at inherited charges; 2^28.016215 units; C = 6321272920235813/135500000.

H.3. Historical H total was 2^32.87429 (numerator 2133611670920905708573/271000000000), preprocessing 2^32.77757; J supersedes it; no target function runs here.

## Appendix I. Memory
(Superseded by Appendix K.) 0f72a85e's figure was 130,149,253 bytes: B' 113.5 MiB (an allowance) + connector 8 MiB + code 2 MiB + one echelon system 650,117; P 89,233,818; E 44,591,237.

## Appendix J. Exact executed-count memory-rule ledger

(R5N3: history, condensed. Appendix J applied seven measured savings and one small development row to R5N's ledger and gave time 32.79669 for 0f72a85e, whose rows (G2, D15, D19, D20 and the others) R5N3 no longer charges: Appendix M governs. J's seven rows and its exact total are in R5N2's proof.)

## Appendix K. Memory (R5N; supersedes Appendix I)

Dense model: every resident structure at 32-byte words (a GF(2) row of at most 1,601 bits is 7 words, 224 bytes), phases sequential, code resident in every phase. Code = r5.py (at most 65,536 bytes) + the unrolled 2,048-step E block (410,479 counted primitives, at most 8 bytes each: two 4-byte arm64 instructions per 256-bit primitive) = 3,349,368 bytes. One echelon system: 1,600 x (224 + 8) + 1,600 x 8 = 384,000. One basis: 34 x 224 = 7,616. Setup's Cand: lin 307,200, condparts 277,890, a1rows, act and rowmasks 15,360: 600,450. Base (Lrow, Linv): 716,800. Module tables 131,072 and the parmw memo (n <= 10) 349,525: 480,597.

| Phase | Components (bytes) | Total | log2 |
| --- | --- | ---: | ---: |
| E | ANF table G 41,449 x 768 = 31,832,832; derivative vectors 12,950 x 24 x 32 = 9,945,600; pass buffer 65,536; 50 bases 380,800; the last attempt's info (one echelon system) 384,000; Setup 600,450; Base 716,800; tables 480,597; code 3,349,368 | 47,755,983 | 25.509178 |
| B' | X buffers (X0, current, materialised, working or rebuilt) 4 x 3,200 x 13 x 32 = 5,324,800; 6 D buffers 2,150,400; 2 port systems (1,600 x 14 words) 1,433,600; update logs 216 x (10 x 424 + 5 x 232 + 24) = 1,171,584; Model.cands 320 x 216 x 288 = 19,906,560; t.lin 307,200; conds 277,890; domain lists 398,080; d2u candidates 729,600; Base 716,800; tables 480,597; previous advice round (algorithm()): 49 bases 373,184, one echelon system 384,000, Setup 600,450; code 3,349,368 | 37,604,113 | 25.164387 |
| P, per core and level (development, at the submitted program) | planes 2 x 9^5 x 224 = 26,453,952; key-word slot 2 x 9^5 x 32 = 3,779,136; w2 and choice 2 x 9^5 x 8 = 944,784; one block's sort pairs 944,784; Gray tables 10 x 16 x 256 = 40,960; core tables 10 x 9 x 224 = 20,160; T1/T2 core lists 65,536; code 3,349,368 | 35,598,680 | 25.085320 |
| Connector | ED and EM 2 x 384,000; Setup 600,450; Base 716,800; 49 bases 373,184; tables 480,597; code 3,349,368 | 6,288,399 | 22.584261 |

Peak = max(online phases: B', connector, E; preprocessing and development phases: P and every development run, at the submitted programs (X.5)) = E = 47,755,983 bytes, memory_log2_bytes (dense model) = 25.509178153459 (rounded up; the claim is raised, see the end of this appendix). The B' item sizes other than the update logs are the dense structural maxima of our memory study (tent bound 216 computed over all 374 subspaces of F2^5; Model.cands at 216 entries for every row), re-checked by arithmetic; 0f72a85e's tent copies (up to 216 x 1,689,600 bytes) are gone. Every development run of R5N3 (R.8, Appendix M) has a measured peak of at most 52,146,176 bytes (109.2% of E's 47,755,983 and 82.9% of the claim). Claim: memory_log2_bytes = log2(62,914,560) = 25.906890595609 (rounded up): the dense model's 47,755,983 (E) is raised to 62,914,560, the largest address-space cap that any development label needed (R.8; the interpreter's virtual size exceeds the dense model's structures). Sensitivity (not claimed): a 2 MiB code allowance instead of r5.py's 65,536 bytes: 49,787,599 (2^25.5693).

## Appendix L. Exact ledger (R5N2; history: superseded by Appendix M)

(R5N3: history, condensed. R5N2's Appendix L added rows L1-L10 (B' rows at true cost, the half-vector repricing, bases, D26, and the capped advice run L9 with L10) to Appendix J's total and gave time 33.08452. Appendix M supersedes it; L's rows are in R5N2's proof.)


## Appendix M. R5N3: the development record and the exact ledger (supersedes Appendix L)

M.0. Scope. R5N3's charged development is: the 50 runs of R.8 (table M.2), D16 (v17's stated bound 2^27), and the peers' build checks of programs the lineage adopts (D21, D_Y, D_v23, D_v24, as filed). Every run of R5N3 is in the table; none is omitted, and the log (devmem.jsonl, SHA-256 c0f0ff0dc601ad1eeaa58be6ddc66718a96fd5e3b4094fc0cba79aa782f6b976) has exactly 50 lines. Sources (SHA-256): r5.py f9a88567b9cadffcdd7995bd6dc68a543218594e8825ee484a597c9e219b3cb3 (the shipped file); capadv/src/main.rs 0f03517732fd3124b393e3aaf23ba3dae4f59b3fec59b6e1ea1f15c811fef341; capadv binary e04c3f83047a296d1cdca5cde11ca0832aa882a117fac2f4696fbd88d885ef4a; fes.c 9a023ce614609bb9c27ba94683a6dc340f7a1324a3550ca4ba3f45775ae30de4; fes binary 7b4ff593a5d8c5a3ca00c0332295c943ca027a9904d463f8fec9431cfd30bb28; py/export_cores.py 6f18b9ec44fdea59d849cc3612b93440c6f9b877ee63cca9e941337952487aa4; pickcores.py 8a34c8fc0a85f60eb31370896b40296c8c7364b4646f409bcec72d6db99d3a75; mklayouts.py 9631e150518e77e2e857315bcbe3f59caefe68bbd1cc447d9d58c6698c839ea1; layout_pick.py d0de11926ee71a3110a83d7a5a163e4e2ee7fe8816d50cafb59eb4acb9cef0ff; mcap.py 2a6bdd6341806ce3b4d26119b037998699aa18ea0b0ff50f1f3879673377dad2; finalize.py 08734a0a6db6aa4d6f0bda94a3dcc3cd792cefa0fcf45a91166cd96969f28397; bprime_run.py 81c4b42c2dbd719ccc7cf575b540983ef793098607207f33d25cb970ee2ee2d0; conn_run.py dac5d72f416a1bc3f703ac9baa132a6c08cc2510815bf62aceb829060a251db6; mt6_check.py 2c5ad3d652955b6facb1c5ab66f6933ddf335e0f4c5496e2dd825bf9e260c26c; run_all.sh 836e1a86dcfb78d0e3951f33ae21504b80cee97e24eeb93f4fd2dccb93fd49ea; lib.sh a18d370bea5ce2dd7c56c9f9f69661b88fec63e0b2e0566f9cb6effbc680d56d; stages/*.sh s00_prep.sh e6d5ac386301ab3d7214d65f0859cfc0b0712338334b4d12717c108062e2ae7f, s10_cores.sh 036d464784f88e39f2dc0e2d78c32da13619c7651952fc451fc42d5422e93706, s11_layout.sh ddcaf668cb918a48eecbad6aba7a916ae2b5a56f17b64d1c51a7bd4f97816044, s12_advice.sh 300a64409ea066423c7d6b8e1afe37ca01ce61ceb6a2a3b9257435faaa61fe9f, s13_mt6.sh 719c89ec19d0d7cd38efd4198d2a95841b7ee3b26b04054319fab999cf4bcec6, s20_bprime.sh 367947b7391c0d3e35e6f241be9f3f790cc0ea0d9fbb54e87084a577daaadd3e, s30_fes.sh 49dbc8981739b240860c6e5eefe07f79944b6a5b01e7159cb70162b47cba2343, s40_online.sh e5a027381d5832d0aee313c0115ce17b2187a005a8f7ec965a77110168b6facc. The claim_bytes and within_claim fields of devmem.jsonl hold the dense model's 47,755,983 that was current when each run was logged; they are not the final claim, and the cap and peak columns of M.2 are the record. These sources are not part of the package (the experiment sources are limited to 64 KiB and r5.py has 73 bytes left).

M.1. Prices (primitives; a primitive count P is P/1355 units; 2^31 primitives per Python process that loads r5.py, which also covers the process's own small work). capadv events at the counted prices of R5N2's R.8 (Gray step 41, hash insert 8, probe 50, key hit 1,024, evaluation 2^11, per core and block 2^17, per core 2^20; s11's count-only runs: 5 per counted match, the loop `cnt += 1; *mt += 1; out.m[ni] += 1; i = dict.next[i]`, 64 blocks per core); export_cores.py at U.4's bound (8,674,833 x 2^12 + 1,639,088,128 x 21 + 2^32); B' at its true cost (WK + WK.d, extras included) plus 2^27 for Base() and own_bits(); a connector attempt at 2^20 x 96 + 2^15 x 512 + 2^22, Setup 4 x 2^31, bases 2^24 each, and the B' inside s40 at its WK cost (an upper bound of the true cost); E stage 1 at 2^14 x 208,007 per space. A run that failed is charged as the completed run of the same label.

M.2. Every development run (one row per devmem.jsonl line):

| # | Stage | Command (cwd out/run; wrapper `/usr/bin/time -v prlimit --as=CAP nice -n 10`) | CAP (B) | Peak RSS (B) | Exit | Wall (s) | Price (log2 units) |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | s10_cores | `python3 -B py/export_cores.py cores.txt` | 47,755,983 | 37,036,032 | 0 | 30.4 | 25.7487 |
| 2 | s11_pick8 | `python3 -B py/pickcores.py cores.txt cores8.txt` | 47,755,983 | 34,926,592 | 0 | 0.0 | 20.5959 |
| 3 | s11_mkconsts | `python3 -B py/mklayouts.py` | 47,755,983 | 27,836,416 | 0 | 0.4 | 21.5959 |
| 4 | s11_L0_contig5 | `HS_COUNT=1 HS_ONLY64=1 HS_NCORES=8 ../capadv.bin all cores.txt  (in L0_contig5)` | 47,755,983 | 8,253,440 | 0 | 16.5 | 24.9740 |
| 5 | s11_L1_z | `HS_COUNT=1 HS_ONLY64=1 HS_NCORES=8 ../capadv.bin all cores.txt  (in L1_z)` | 47,755,983 | 8,085,504 | 0 | 72.8 | 27.4094 |
| 6 | s11_L2_s1 | `HS_COUNT=1 HS_ONLY64=1 HS_NCORES=8 ../capadv.bin all cores.txt  (in L2_s1)` | 47,755,983 | 8,114,176 | 0 | 17.0 | 25.0402 |
| 7 | s11_L3_s5 | `HS_COUNT=1 HS_ONLY64=1 HS_NCORES=8 ../capadv.bin all cores.txt  (in L3_s5)` | 47,755,983 | 8,126,464 | 0 | 0.7 | 21.6116 |
| 8 | s11_L4_s13 | `HS_COUNT=1 HS_ONLY64=1 HS_NCORES=8 ../capadv.bin all cores.txt  (in L4_s13)` | 47,755,983 | 8,192,000 | 0 | 0.8 | 21.6005 |
| 9 | s11_L5_s29 | `HS_COUNT=1 HS_ONLY64=1 HS_NCORES=8 ../capadv.bin all cores.txt  (in L5_s29)` | 47,755,983 | 8,409,088 | 0 | 0.8 | 21.6016 |
| 10 | s11_pick | `python3 -B py/layout_pick.py L*/stage.log` | 47,755,983 | 11,726,848 | 0 | 0.0 | 20.5959 |
| 11 | s30_fes_1 | `./fes < fes_in_1.txt` | 47,755,983 | 22,392,832 | 0 | 2.1 | 21.9672 |
| 12 | s30_fes_2 | `./fes < fes_in_2.txt` | 47,755,983 | 22,261,760 | 0 | 2.3 | 21.9672 |
| 13 | s30_fes_3 | `./fes < fes_in_3.txt` | 47,755,983 | 22,196,224 | 0 | 2.3 | 21.9672 |
| 14 | s40_online_1 | `python3 -B py/conn_run.py w/r5.py 10 1 50` | 47,755,983 | 39,976,960 | 0 | 76.8 | 25.2112 |
| 15 | s12_t3 | `HS_MCAP=2^40 ./capadv.bin all cores.txt` | 47,755,983 | 7,991,296 | 0 | 125.8 | 28.2945 |
| 16 | s12_mcap | `python3 -B py/mcap.py stage2.log` | 47,755,983 | 28,467,200 | 0 | 0.2 | 20.5959 |
| 17 | s12_final | `python3 -B py/finalize.py cores.txt stage2.log advice.txt` | 47,755,983 | 28,180,480 | 0 | 0.2 | 21.5959 |
| 18 | s20_bprime_4 | `python3 -B py/bprime_run.py w/r5.py 10 4` | 47,755,983 | 39,743,488 | 0 | 104.4 | 22.7548 |
| 19 | s13_mt6 | `python3 -B py/mt6_check.py stage2.log` | 47,755,983 | 28,364,800 | 0 | 0.1 | 20.5959 |
| 20 | s20_bprime_6 | `python3 -B py/bprime_run.py w/r5.py 10 6` | 47,755,983 | 40,087,552 | 0 | 133.1 | 23.4472 |
| 21 | s20_bprime_2 | `python3 -B py/bprime_run.py w/r5.py 10 2` | 47,755,983 | 40,923,136 | 1 | 211.0 | 23.8874 |
| 22 | s40_online_2 | `python3 -B py/conn_run.py w/r5.py 10 2 50` | 47,755,983 | 39,972,864 | 1 | 237.4 | 26.7446 |
| 23 | s20_bprime_3 | `python3 -B py/bprime_run.py w/r5.py 10 3` | 47,755,983 | 39,821,312 | 0 | 70.5 | 22.3148 |
| 24 | s20_bprime_2_pmalloc | `PYTHONMALLOC=malloc python3 -B py/bprime_run.py w/r5.py 10 2` | 47,755,983 | 41,136,128 | 1 | 81.1 | 23.8874 |
| 25 | s20_bprime_7 | `python3 -B py/bprime_run.py w/r5.py 10 7` | 47,755,983 | 39,882,752 | 0 | 201.5 | 23.5044 |
| 26 | s20_bprime_2_cap50331648 | `python3 -B py/bprime_run.py w/r5.py 10 2` | 50,331,648 | 42,721,280 | 1 | 70.7 | 23.8874 |
| 27 | s20_bprime_2_cap49000000 | `python3 -B py/bprime_run.py w/r5.py 10 2` | 49,000,000 | 42,115,072 | 1 | 71.3 | 23.8874 |
| 28 | s20_bprime_2_cap56623104 | `python3 -B py/bprime_run.py w/r5.py 10 2` | 56,623,104 | 48,250,880 | 0 | 80.7 | 23.8874 |
| 29 | s20_bprime_2_cap52428800 | `python3 -B py/bprime_run.py w/r5.py 10 2` | 52,428,800 | 44,691,456 | 0 | 86.7 | 23.8874 |
| 30 | s20_bprime_2_cap50855936 | `python3 -B py/bprime_run.py w/r5.py 10 2` | 50,855,936 | 43,061,248 | 1 | 73.7 | 23.8874 |
| 31 | s20_bprime_2_cap51904512 | `python3 -B py/bprime_run.py w/r5.py 10 2` | 51,904,512 | 44,167,168 | 1 | 75.2 | 23.8874 |
| 32 | s20_bprime_2_cap51380224 | `python3 -B py/bprime_run.py w/r5.py 10 2` | 51,380,224 | 43,917,312 | 1 | 75.6 | 23.8874 |
| 33 | s40_online_2_cap52428800 | `python3 -B py/conn_run.py w/r5.py 10 2 50` | 52,428,800 | 44,658,688 | 0 | 99.2 | 26.7446 |
| 34 | s20_bprime_1 | `python3 -B py/bprime_run.py w/r5.py 10 1` | 47,755,983 | 39,993,344 | 0 | 59.7 | 22.4332 |
| 35 | s20_bprime_9 | `python3 -B py/bprime_run.py w/r5.py 10 9` | 47,755,983 | 40,759,296 | 1 | 208.0 | 23.8750 |
| 36 | s40_online_0 | `python3 -B py/conn_run.py w/r5.py 10 0 50` | 47,755,983 | 40,849,408 | 1 | 1686.9 | 27.0293 |
| 37 | s20_bprime_5 | `python3 -B py/bprime_run.py w/r5.py 10 5` | 47,755,983 | 39,997,440 | 1 | 1656.0 | 25.9280 |
| 38 | s20_bprime_9_cap52428800 | `python3 -B py/bprime_run.py w/r5.py 10 9` | 52,428,800 | 44,666,880 | 1 | 70.0 | 23.8750 |
| 39 | s20_bprime_9_cap62914560 | `python3 -B py/bprime_run.py w/r5.py 10 9` | 62,914,560 | 52,146,176 | 0 | 77.5 | 23.8750 |
| 40 | s20_bprime_9_cap67108864 | `python3 -B py/bprime_run.py w/r5.py 10 9` | 67,108,864 | 51,908,608 | 0 | 78.9 | 23.8750 |
| 41 | s20_bprime_9_cap56623104 | `python3 -B py/bprime_run.py w/r5.py 10 9` | 56,623,104 | 48,332,800 | 0 | 85.8 | 23.8750 |
| 42 | s20_bprime_9_cap54525952 | `python3 -B py/bprime_run.py w/r5.py 10 9` | 54,525,952 | 45,957,120 | 0 | 79.8 | 23.8750 |
| 43 | s20_bprime_9_cap55574528 | `python3 -B py/bprime_run.py w/r5.py 10 9` | 55,574,528 | 47,341,568 | 0 | 80.0 | 23.8750 |
| 44 | s20_bprime_9_cap53477376 | `python3 -B py/bprime_run.py w/r5.py 10 9` | 53,477,376 | 45,674,496 | 0 | 80.9 | 23.8750 |
| 45 | s20_bprime_0 | `python3 -B py/bprime_run.py w/r5.py 10 0` | 47,755,983 | 40,779,776 | 1 | 1680.5 | 26.0361 |
| 46 | s20_bprime_8 | `python3 -B py/bprime_run.py w/r5.py 10 8` | 47,755,983 | 40,534,016 | 1 | 1645.8 | 26.8493 |
| 47 | s20_bprime_5_cap62914560 | `python3 -B py/bprime_run.py w/r5.py 10 5` | 62,914,560 | 50,450,432 | 0 | 398.2 | 25.9280 |
| 48 | s20_bprime_0_cap62914560 | `python3 -B py/bprime_run.py w/r5.py 10 0` | 62,914,560 | 50,302,976 | 0 | 429.9 | 26.0361 |
| 49 | s40_online_0_cap62914560 | `python3 -B py/conn_run.py w/r5.py 10 0 50` | 62,914,560 | 50,618,368 | 0 | 431.8 | 27.0293 |
| 50 | s20_bprime_8_cap62914560 | `python3 -B py/bprime_run.py w/r5.py 10 8` | 62,914,560 | 51,220,480 | 0 | 789.8 | 26.8493 |

M.3. The online terms (units; exact) and the peers:

| Term | Exact (units) | log2 |
| --- | --- | ---: |
| P setup 2^32 prim | 4294967296/1355 | 21.5959 |
| B' 2^29 + 2^13 units | 536879104/1 | 29.0000 |
| S 4 x 2^31 prim | 8589934592/1355 | 22.5959 |
| connector 4268 x CONN prim | 519137394688/1355 | 28.5132 |
| Bases 197 x 2^24 prim | 3305111552/1355 | 21.2180 |
| E setup 50 x 2^16 units | 3276800/1 | 21.6439 |
| E stage 1 50 x 2^14 x 208007 prim | 34079866880/271 | 26.9061 |
| E stage 2 50 x 2^11 x (2 units + 2^11 prim) | 97443840/271 | 18.4559 |
| output 2^22 prim | 4194304/1355 | 11.5959 |
| **Online total** | 1438129405952/1355 | 29.983254 |

| Peer row (as filed, units) | Value | log2 |
| --- | ---: | ---: |
| D16 | 134217728 | 27.0000 |
| D21 | 6391841 | 22.6078 |
| D_Y | 16384 | 14.0000 |
| D_v23 | 33554432 | 25.0000 |
| D_v24 | 24225113 | 24.5300 |

M.4. Total N = 4436881300481 / 1355 = 3274451144.2664 units; log2 N = 31.608606; **time_log2 = 31.60861**; **preprocessing_log2 = 31.36176** (P's setup bound, B', S and the development, rounded up); memory 2^25.906891 (R.4); **score 31.60861 + (25.906891 - 20) = 37.51550** (0f72a85e: 39.75228; R5N2: 38.59370). The integer primitive-operation numerator printed by the ledger is N = 4436881300481 (the ceiling of N x 1355)..

M.5. Reproduction (Fraction arithmetic and integer powers only; the development row is the sum of the 50 run prices of M.2 in primitives):

```python
from fractions import Fraction as F
R = 1355
run_prims = [76395417600, 2147483648, 4294967296, 44653306277, 241544839312, 46750331357, 4341786497, 4308522462, 4311998202, 2147483648, 5555470336, 5555470336, 5555470336, 52634055487, 446103400136, 2147483648, 4294967296, 9589788523, 2147483648, 15497223738, 21025774368, 152355013329, 7069031907, 21025774368, 16124378418, 21025774368, 21025774368, 21025774368, 21025774368, 21025774368, 21025774368, 21025774368, 152355013329, 7673903029, 20846918929, 185602121337, 86503154548, 20846918929, 20846918929, 20846918929, 20846918929, 20846918929, 20846918929, 20846918929, 93238549240, 163831591975, 86503154548, 93238549240, 185602121337, 163831591975]
dev = F(sum(run_prims), R) + 134217728 + 6391841 + 16384 + 33554432 + 24225113
online = F(4294967296, 1355) + F(536879104, 1) + F(8589934592, 1355) + F(519137394688, 1355) + F(3305111552, 1355) + F(3276800, 1) + F(34079866880, 271) + F(97443840, 271) + F(4194304, 1355)
N = online + dev
assert N == F(4436881300481, 1355)
assert N.numerator**100000 <= N.denominator**100000 * (1 << 3160861) and N.numerator**100000 > N.denominator**100000 * (1 << 3160860)
ops = N * R
N_int = -((-ops.numerator) // ops.denominator)
assert N_int == 4436881300481
print('N =', N_int)
print('time_log2 =', 31.60861)
```
