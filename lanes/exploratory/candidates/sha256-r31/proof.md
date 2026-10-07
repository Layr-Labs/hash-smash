# sha256-r31-exploratory: v6 chain (in-algorithm characteristic search + local-search family + SWAR online)

Cost model collision-frontier-v5, C = 2140. Logarithms base 2, costs in units. **Claim: 2^33.47 units at success
probability 0.40** (ledger 2^33.4645, rounded up) under one declared cost premise, **P1** (Section 4, heuristic H-P1):
the seven search-model constants fixed as literals in [LLW24]'s public search program (Peace9911/sha_2_attack@6a9f35fd)
are public algorithm text, used without charging their original discovery and declared as 2^3 bytes of advice. All
seven are quantities of the published characteristic, which the r31 record 50592e75 (jungjipdo; PR #467, merged
2026-10-07) uses in full without time charge (its H1, plausible in all four lanes; declared as 2^9 bytes of advice).
**With P1 charged** (the allowance of our unsubmitted v5): **41.45** at the measured solver price 6, **42.03** at price
9. Our gate G0 showed the constants are load-bearing. Every other phase runs inside the algorithm under a budget
enforced in its code and is charged at that budget. The programs and raw logs are not part of this submission.
Everything the claim uses is stated here (Appendices A-C), and the organizer experiment `v6-pairs-and-swar-batch`
re-checks the 92 pairs and the SWAR count.

## 1. Algorithm (one run = `chain OUTDIR budgets.txt KEY`)

| # | phase | program | what it computes |
|---:|---|---|---|
| G | P-model generation | `cgen` (C port of our r31 `cfind.py`, itself from [LLW24]'s `correct_dc_model_31_256.py`; byte-identical output) | STP model: local collision dW5..9, dW16, dW18; 8_14 caps h=0, K=20, HW(dE5)<=7, HW(dE6)<=4, HW(s0(dW6)-diff)<=9, HW(dE7)<=8, HW(dE8)<=14 |
| P | characteristic search | STP 2.4.1 + CryptoMiniSat 5.14.7, one call, default seed | signed characteristic (A-weight 20; differs from the published one in its A, E and W rows) |
| C1 | rows + model M | `cglue char` | signed rows, modular differences; model M (USCMig f94a3f75) with full hints |
| S | exact sets | `sets` (15 threads, one pass over 2^32) | V7, V8, G16 lists; \|V6\| = 2^23 |
| M | base starting point | STP+CMS, one call | A1..A4, E3..E12 of one SP (3,072 table tuples) |
| C3 | parse | `cglue sp` | SP words |
| L | local search | `ls2` (USCMig's move set: flip A5..A8, E5..E12, derive A1..A4), BFS, 64 expansions, 2 completions per SP | 384 SPs, 4,048,896 tuples |
| A | tables + rate model + N | `tabm` | per-SP tables (tuples, completions, G16); q_model = T x 2^-9 x 2^-32 x p20 with p20 from 2^22 seeded samples; **N = 2/q_model = 3,510,010,448 trials** (rounded up to a multiple of 7) |
| O | online | `v6on`: 7-lane SWAR batches; lane l's message word i = bits [36l, 36l+32) of 256-bit random word i (AES-128-CTR under the run's key); key = CV1[0] into the full 2^32-bit bitmap; scalar hit path (key match, tuple, W6, step-20 tests); capped completion (E13, W14, W15); every candidate re-hashed from the IV | first verified pair, or failure at N |

Charged program for O: the counted SWAR batch, 2,235 primitives per 7 trials = 0.149199 units/trial (rand 16, load
47, add 263, and 792, or 246, xor 308, shift 543, cmp 7, branch 13; 55 of 64 registers): 16 RAND and 16 masks, the
schedule, 31 rounds with each K_t loaded, 9 IV loads, word-0 feed-forward, 7 lane extracts, 7 x 7 bitmap-probe ops,
6 control. The organizer experiment runs this exact batch (Section 6). `v6on` evaluates the same lanes natively; in
development the keys were identical on 16.8M trials and 1.05M full chaining values equalled the official verifier.

## 2. Term table (exact)

| term | basis | units | log2 |
|---|---|---:|---:|
| P characteristic search | (3.19635e12 budget + 5e9 overshoot) instr x 6 | 8.976e9 | 33.063 |
| L local search | (3.91776e11 + 5e9) x 5 | 9.271e8 | 29.788 |
| S exact sets | (1.94462e11 + 7.5e10) x 5 | 6.296e8 | 29.230 |
| M base SP | (2.12008e11 + 5e9) x 6 | 6.084e8 | 29.181 |
| O online | N/7 = 501,430,064 batches x 2,235 ops | 5.237e8 | 28.964 |
| A tables, rate model | (1.83976e10 + 5e9) x 5 | 5.467e7 | 25.704 |
| C3, C1, G | (5.03e7 / 6.82e7 / 5.86e8 + 5e9 each) x 17 / 12 / 5 | 8.16e7 | 26.28 |
| H hit path at caps | keys <= 3,304,416 (1 unit + 512 ops each), tuples <= 13,239,742 (512), W6 <= 29,946 (1,024 + 2 x 64 x 128), <= 64 completion calls (each <= 64 x 2^16 x 160 + 2^16 x 160 + 64 x 256 ops + 35 units) | 2.789e7 | 24.733 |
| O0 online setup | 8.21524e9 x 5 (checked in-process) | 1.919e7 | 24.194 |
| D driver + watchdog | 1e9 x 10 | 4.673e6 | 22.156 |
| B bitmap build, R replay | | 2.3e4 | 14.5 |
| **total (claim 33.47)** | | **1.18525e10** | **33.4645** |
| *sensitivity: + P1 allowance (premise P1 charged)* | 64 calls x 1,800 CPU-s x 9.2e9 instr/CPU-s = 1.05984e15 instr x 6 | +2.9715e12 | *41.4401 -> 41.45* |
| *same, solver price 9 (P, M and P1)* | | | *42.0247 -> 42.03* |

- Budgets: max(1.05, max/min + 0.03) x min over the two pre-freeze runs E0'/E0'' of the same binary (larger factors
  for tiny phases), frozen before the evidence (Appendix B). The watchdog kills a phase once its retired-instruction
  count exceeds the budget; a kill is a failed run (Appendix C).
- Overshoot: the watchdog sleeps at most headroom / (5e10 instr/s x threads), clamped to 1..100 ms, so a phase can
  pass its budget only by its rate times (the 1 ms floor + the OS wake-up delay). We charge 100 ms at 5e10 instr/s per
  thread (5e9 instructions; 7.5e10 for the 15-thread S), which covers a wake-up delay of up to 99 ms. 5e10 is above
  the hardware maximum of one thread on this machine (4.6e10). Only a killed (failed) run can overshoot.
- Prices (ops of the cost model per retired AArch64 instruction; jungjipdo's per-form table `a64ops_jj`, credited):
  solver 6 = 1.15 x 4.843, measured on the exact P and M models (an instrumented build with identical output; 99.62%
  of PC samples in the measured library). The P1 sensitivity rows use the same price. Our C phases: price
  measured per phase with coverage, 1.15 x (ops + 4 x uncovered)/plain, rounded up to 0.5, floor 5.
- Memory: chain max RSS 1,328,742,400 B = 2^30.31 (2^29 B key bitmap + tables + solver), claimed 2^30.4.

## 3. Evidence (pre-registered, PREREG2, before the root seed existed)

- **Freeze.** The SHA-256 list of every program, source, budget and price file and of the solver binary and library
  (Appendix B) was written and its own hash recorded before the root seed was drawn (15:09:55.626 / .687 / .707Z).
  Keys: key_i = first 16 bytes of SHA-256("v6f2-r31|" + ROOT + "|" + i), ROOT = 902e2ee5...e3ba854f (Appendix B).
- **E-C** (full chain, key_0 = 5c53e73e...): every phase within budget (P 3.04626e12 of 3.19635e12; all margins >=
  4.8%, Appendix B); every prefix output byte-identical to E0'/E0'' (third and fourth observation); online: verified
  collision after 882,018,046 trials.
- **E-S stage 1** (100 online runs on the E-C prefix, keys 1..100, sequential, frozen cap N): **k = 91 of 100**;
  one-sided 99.5% Clopper-Pearson lower bound **0.8108 >= 0.40 -> claim 0.40** (stage 2 not run). Stops: 91 found,
  9 reached the cap N, 0 hit-path cap aborts. Trials 152,222,675,885 = 2^37.147; realised rate 91/trials = 2^-30.640
  vs the in-algorithm model q = 2^-30.709; predicted success 0.877 (realised rate) / 0.865 (model). Success times vs
  the exponential law truncated at N: KS D = 0.124 (5% critical value 0.143). Per-run table: Appendix A.
- **Interruption (disclosed).** A machine reboot at ~16:11Z killed run 85 after runs 1..84 had finished (k = 78/84,
  already above the rule's k >= 54, so resuming could not be outcome-selected). Before resuming we re-hashed every
  frozen file and wrote and hashed a resume note and script; keys 85..100 then ran exactly as pre-registered (run 85
  restarted from scratch; its partial output is kept). The resume note says all frozen files were equal; that is
  inaccurate in one point: the development log DEVLOG.md had been appended to after the freeze (append-only; its frozen
  2,130-byte prefix unchanged; it changes no program, budget, price or constant). We restored it to the frozen prefix
  and moved the appended notes to a separate post-freeze log. Every program, source, budget, price and solver file
  was equal. In the evidence-cost sensitivity the interrupted attempt is charged as a full extra run.
- **E-V**: all 92 pairs (E-C + 91 E-S) checked with the official verifier `digest(.., 'sha256', 31)`: 92 OK,
  92 distinct digests, 92 distinct M0; one difference family DW5..9 = (00000ffa, 001f77ef, b00fb5fa, d800f100,
  00008004) (the in-algorithm characteristic's); every M0 word random (no counter or fixed word).
- Development checks (disclosed): solver price measurement, SWAR equivalence (2.4M batches), prefix determinism (5
  identical runs), gate G0 (Section 4, P1).

## 4. Premises (each decided explicitly)

| # | premise | decision |
|---|---|---|
| P1 | [LLW24]'s 7 search-model constants (HW(dW16)=17, HW(dW18)=2, HW(dE12)=HW(dE14)=2, dE13=0, support HW(dE11\|dE12)=5, message weight 48) | **adopted as a declared cost premise: not charged in time, declared as 2^3 bytes of nonuniform advice** (H-P1, Section 5). Reasons: (i) precedent: the r31 record 50592e75 (jungjipdo; PR #467, merged 2026-10-07) uses the entire published characteristic without time charge (its H1-public-characteristic, plausible in all four lanes; declared as 2^9 bytes of advice); all seven constants are quantities of that characteristic (provenance below), so they carry strictly less information than it; (ii) they are fixed literals of [LLW24]'s public, pinned search program, not search output; (iii) that program also fixes signed A and E patterns, which our generator drops, so only the seven weights are inherited; our search output 8_14 (A-weight 20) differs from the published characteristic in its A, E and W rows, and everything downstream (P, S, M, L, A, O) is our own measured, budgeted, in-chain work. Disclosed against it: gate G0 (two P calls without the six weight constants; dE13=0 kept as a structural requirement of model M and the completion) failed (G0a: dense characteristic, \|V6\| = 2^8, model M UNSAT after 1.0e13 instructions; G0b: nothing in 1.2e13), so the constants are load-bearing (without them no usable characteristic within budget); all seven equal quantities of the published characteristic; our v5 (never submitted) charged an allowance for them. **P1 charged** on v5's basis (64 calls x 1,800 CPU-s x 9.2e9 instr/CPU-s, solver price 6): **41.45**; price 9: **42.03**; price 25: 43.50; v5's own 1 op/instruction: 38.89. |
| P2 | the 8_14 caps, NEXP, J, T11, MCS, rate seed fixed in development | adopt, disclosed (zero-advice precedent: our 113fc836, Th0rgal 7deb1595). Selection disclosed: development produced 15 SAT characteristics, of which model M was SAT for 3 (all with P >= 3.04e12 instructions); 8_14 was chosen after seeing that downstream result, and the default solver seed re-derives it deterministically. Sensitivities: the 2 earlier M-SAT configurations run in-chain first 35.03; whole development ledger charged (2^40.52 at price 9 + this build's solver runs at 9) 40.72 |
| P3 | published characteristic free | not used beyond the seven quantities of P1: our own search P runs in-chain and is charged in full |
| P4 | solver price | 6 (measured on the charged models x 1.15); 4.843 -> 33.22; 9 -> 33.96; 25 -> 35.30 |
| P5 | C prices | measured per phase (floor 5); all C phases at price >= 9 -> 33.62 |
| P6 | Python generator at 256/instruction | not needed: byte-identical C ports |
| P7 | SWAR price while the evidence runs use the native evaluator | adopt after the equivalence checks (tekkac, Th0rgal precedent) and the organizer experiment |
| P8 | budget kill = failure, charged at budget + overshoot | adopt |
| P9 | E-S runs not charged | adopt (they feed no constant); E-C chain + 101 online attempts (incl. the interrupted one) charged at caps: 36.20 |
| P10 | N_f | 2 (cap 2/q), not chosen from evidence; N = 4/q -> 33.53 |
| P11 | first blocks | 16 AES-CTR words per 7-trial batch, no counter or shared prefix |

P1 provenance (checkable). In Peace9911/sha_2_attack@6a9f35fd, `find_dc/correct_dc_model_31_256.py`, the constants
are literals: HW(dW18) = 2 (line 71), HW(dW16) = 17 (78), HW(dE14) = 2 (156), HW(dE12) = 2 (163), HW(dE13) = 0 (170),
HW(dE11 | dE12) = 5 (184), total HW(dW0..dW30) = 48 (193). The same file also fixes signed patterns for A5..A10 (`aa`,
line 126) and E8..E14 (`ee`, line 99); our generator sets both to empty (marked r31v6), so only the seven weights are
inherited. In the published characteristic (cell table of 50592e75's proof, Section 5) the signed cells give exactly
these seven values: HW(dW16) = 17, HW(dW18) = 2, HW(dE12) = 2, dE13 = 0, HW(dE14) = 2, HW(dE11 | dE12) = 5, and
6+5+10+6+2+17+2 = 48 signed W cells (rows 5, 6, 7, 8, 9, 16, 18).

## 5. Heuristics (minimal set)

- **H-SUCC.** One run of the frozen chain outputs a verified 31-step collision with probability >= 0.40. Support:
  E-S (one-sided 99.5% Clopper-Pearson, Appendix A) + E-C; the prefix is deterministic (identical outputs in 5 runs)
  and every cap/budget abort is a failure inside the measured rate. Model value 1 - e^-2 = 0.86. Scope: the reference
  machine (Apple M5 Pro) and the frozen binaries and solver library of Appendix B.
- **H-P1 (cost premise P1; score-critical for the time claim, not for success).** The seven [LLW24] search-model
  constants of P1 are public algorithm text (literals of the pinned public search program and quantities of the
  published characteristic; provenance in Section 4) that the algorithm may use without charging their original
  discovery. They are seven integers, not a characteristic, collision, message word, chaining value or state value;
  declared as 2^3 bytes of advice. Same form as 50592e75's H1-public-characteristic (plausible in all four lanes),
  which uses the whole published characteristic. Our characteristic and all downstream work are computed and charged
  in-chain (Sections 1-3). Claim 33.47 under H-P1; with P1 charged 41.45 (price 6) / 42.03 (price 9); a charge of T
  units gives 1.18525e10 + T. Limitations: G0 shows the constants are load-bearing; all seven are quantities of the
  published characteristic; our unsubmitted v5 charged them.
- Premise inside H-SUCC (not a separate heuristic): AES-128-CTR under the run's fresh random key implements the
  random-word primitive (16 words per 7-trial batch, charged).
- Not heuristics: prices (measurements on the charged programs), SWAR count (exact; organizer-recomputed), caps and
  budgets (enforced in code, charged at the cap).

## 6. Certificates and experiment

- `certificates/`: 16 (the format's maximum: E-C and the first 15 E-S successes in key order) of the 92 verified
  31-step collisions (two-block messages M0||M1, M0||M1'), all equal under the official verifier.
- `experiments/v6check.py` (`v6-pairs-and-swar-batch`, stdlib only): trial t < 92 returns pair t (E-C, then the 91
  E-S successes in key order; t < 16 are the certificates); every trial runs the counted SWAR batch on 16 random
  words derived from the organizer seed and compares all 7 lanes' key and full CV with a scalar 31-step compression.
  Local run: 92/92 pairs collide under the official verifier; 256/256 trials report 2,235 ops (the categories of
  Section 1) and 7/7 lanes equal; byte-identical output on repeat; 0.33 s. It makes no probability or cost inference.

## 7. Credits and co-authors

Co-authors: USCMig (f94a3f75: move set, model M, completions), jagnani73 (654cb3d2: fresh block per trial, flat
charge, global caps), Th0rgal (7deb1595, f310d44f: zero-advice pattern with our 113fc836; SWAR online), tekkac (7x36
SWAR packing), jungjipdo (replay-chain framing, per-form price table `a64ops_jj`; 50592e75 is the precedent for
premise P1). Also credited: Peace9911 sha_2_attack (model generator); cryptanalysis [LLW24] (Li, Liu, Wang,
EUROCRYPT 2024), [LLWDS24], [MNS13].

## Appendix A. E-S per-run table (keys from the root seed; trials until the verified pair, or N = 3,510,010,448)

| runs | run key-prefix trials ("cap" = no pair at N) |
|---|---|
| 1-5 | 1 c51adda6 254218846; 2 d5dfe69a 2074927778; 3 ff99994f 2073181838; 4 032bd356 1742230098; 5 50a7f9ab 3510010448 cap |
| 6-10 | 6 857f9dc2 605039183; 7 621ed952 3009451298; 8 80cdf175 2663756158; 9 8752d0e9 2326783543; 10 d1d10f2e 1052054934 |
| 11-15 | 11 3b83e677 1381071097; 12 d9f2e502 1322939576; 13 e9dbf655 674859703; 14 27fb132a 3510010448 cap; 15 8644e875 2277215647 |
| 16-20 | 16 2116f153 3510010448 cap; 17 92ee8a15 1007560162; 18 24c29427 1744502578; 19 ae603e70 2161639949; 20 5afe5d49 3326531369 |
| 21-25 | 21 6a87b8f1 2247104804; 22 e1010907 925947141; 23 ac883bd2 374595634; 24 056de318 2220894074; 25 9dcddd0a 520067814 |
| 26-30 | 26 cc1fbf79 1394288924; 27 a9d94ecf 801117107; 28 c3019f9f 2047996552; 29 db484890 3510010448 cap; 30 a1b05128 65950290 |
| 31-35 | 31 b83a3ba4 2037082054; 32 ec5add7f 437920868; 33 10a461cd 964819905; 34 436dd19e 903359947; 35 0d6b4773 745270050 |
| 36-40 | 36 d31ac7f9 3510010448 cap; 37 d45b8cdf 459363233; 38 134a2a09 958413575; 39 a9836981 1781964576; 40 f0fcd4e2 1471501556 |
| 41-45 | 41 7807456b 542992989; 42 ad206191 384431887; 43 b991f92c 2537312932; 44 9e17ccec 2010053577; 45 08ea25c3 2132386788 |
| 46-50 | 46 828a376c 1771778533; 47 e11fece4 2172852668; 48 c6f74413 421798370; 49 650ecbae 1329787074; 50 08506cfe 415382296 |
| 51-55 | 51 2c9b21e7 1687203567; 52 d24d9350 411156893; 53 4425e557 3267339516; 54 91c9c5f9 539104174; 55 6bc730ab 2648254378 |
| 56-60 | 56 60c82e0d 3382589350; 57 555eaee7 1138243946; 58 4b7d72f6 403694403; 59 be0cd59d 1788724322; 60 5b75f627 74544645 |
| 61-65 | 61 724f58d2 2375148888; 62 30f0e684 687475817; 63 931fe8d4 1074926972; 64 ea3066f0 1097793102; 65 d8877713 477193549 |
| 66-70 | 66 6a98673e 2950602669; 67 849b33b1 163266243; 68 6959ed69 1040064907; 69 33521b79 3510010448 cap; 70 bca32756 2253640088 |
| 71-75 | 71 90f02f7a 314926717; 72 af1468a3 1314107998; 73 a9878b2d 1577247280; 74 a8ea458d 54598831; 75 8c7a2359 2458097257 |
| 76-80 | 76 075be96e 413606543; 77 c8acb931 451013283; 78 e7be279f 2853321506; 79 c7841675 307683026; 80 1aec3f88 1382603215 |
| 81-85 | 81 398fb668 188297732; 82 8b368e74 450332001; 83 867971a6 877741837; 84 c4872965 498068473; 85 7180a096 2425177286 |
| 86-90 | 86 953e9c74 794079818; 87 f1c38825 1025623417; 88 feec4ece 2639048496; 89 2bfe1b2b 1695287545; 90 2e9ace80 498754725 |
| 91-95 | 91 c7f97557 386012907; 92 9dc701e5 305099032; 93 d77e4f8f 3510010448 cap; 94 171c1c87 337321376; 95 a8ca057a 373021467 |
| 96-100 | 96 6ed3ede9 2681207991; 97 e61905c2 3510010448 cap; 98 54757d77 3510010448 cap; 99 e21e1ee2 1365552314; 100 1b939fe9 1729383376 |

Totals: 100 runs, 91 pairs, 9 at the cap, 152,222,675,885 trials. E-C (key_0 = 5c53e73e): pair after 882,018,046.

## Appendix B. Freeze: hashes, root, budgets, E-C phase counts

Root seed ROOT = 902e2ee52c3e77204d81ac9d2175531b9bc6777640a74729eee2a864e3ba854f (drawn after the list below; the
list's own SHA-256 b6980f247c165e29538a905629dbe86f63eb2e42d07f952c5dfe7e5b630cc9c1 was recorded first).

| phase | budget (instr) | E-C count | margin |
|---|---:|---:|---:|
| G | 586,409,547 | 530,203,429 | 10.6% |
| P | 3,196,350,460,056 | 3,046,261,305,716 | 4.9% |
| C1 | 68,220,138 | 46,560,749 | 46.5% |
| S | 194,462,096,505 | 184,983,444,778 | 5.1% |
| M | 212,007,838,847 | 201,526,400,899 | 5.2% |
| C3 | 50,341,469 | 34,261,503 | 46.9% |
| L | 391,775,959,990 | 372,950,532,423 | 5.0% |
| A | 18,397,566,054 | 17,532,801,005 | 4.9% |
| OSETUP | 8,215,242,484 | (checked in-process) | |
| DRV | 1,000,000,000 | 136,202,944 | |

Frozen SHA-256 list (first 16 hex digits; paths relative to the build root; the last two are the solver binary and
library):

e3fbcb4460c0f5f9 PREREG2.md; 725d3da9e9cdbc26 DEVPLAN.md; a5a4a473d433e953 DEVLOG.md; f6b9576028b43b88 es_run2.sh;
1686837d52c38762 chain; 893f81e61c819254 cgen; 3c7b5190fb0e24af cglue; 8d164f19b554ebc7 sets; a3cbf8161a1c6c76 ls2;
083acbdd1c1ca18e tabm; 4e1c34b26d0bacc6 v6on; 4749585488a84c38 src/chain.c; 4c75b1babf329018 src/cgen.c;
8cde995f502bc609 src/cglue.c; c0f306fa7ee8c9f4 src/sets.c; af212da0b3a170a1 src/ls2.c; c5d12e3830e713cc src/tabm.c;
18d568797f7c57ff src/v6on.c; 25a184af5d5a643f src/v6aes.h; b7584e005ee3cc99 src/v6io.h; 25f0dfd2f3becaca src/r31.h;
6d523b77ce8fd9ea src/swar31.py; f6a2ebcd444e37df src/swar_vm.py; 676cd7569c25f6e3 src/ledger2.py; a45db0ddad484c6d
src/cp.py; bf8edaa4bfa5e94e src/seeds2.py; 86a443c90747a088 src/vpair.py; 7bc384346b97609e src/pricetab.py;
67fb75810984bece frozen2/budgets.txt; f680e8570c52a7b3 frozen2/prices.json; 69d82a04485b03a9 pc/prices_c.json;
d6f546f13d3c1366 bin/stp_simple; 58a9dbe719a134ad lib/libstp.2.4.dylib

## Appendix C. Enforcement

- `chain` forks each phase and the child execv's the phase binary directly (no shell, no grandchild outside the
  count). The parent reads the child's retired instructions with proc_pid_rusage(RUSAGE_INFO_V4).ri_instructions
  (kernel instructions included), sleeps t = the largest integer in [1, 100] ms with t x 5e10/1000 x threads <=
  headroom, and kills with SIGKILL as soon as the count exceeds the budget; a kill ends the run as a failure. The
  driver also caps its own instructions (DRV). `v6on` checks its setup count against OSETUP in-process, and the
  online loop stops at N trials; the hit path stops at its caps (key matches 3,304,416, tuple tests 13,239,742, W6
  passes 29,946, 64 completion calls), and a cap stop is a failure.
- Every output pair is re-hashed from the IV before it is written; E-V re-checked all 92 with the official verifier.
