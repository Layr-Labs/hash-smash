# 5-round SHA3-256: v18 with a cheaper counted match step, E stage 1 with D1[0] in registers, a bitsliced T2 leaf and its omitted development charged, time 2^33.7208

Exploratory claim. **v19 is Meganpark980320's v18 (f1eb6445; its v17 168a1b3a) with the changes of Section U and nothing
else.** v18 is rubenmarcus's v15 (91f1424d) with five accounting changes (Section V, v18's text); v15 is winglock's v14
(f1cedf6b, with Th0rgal). Everything from Section V on is v18's text, edited only where a number or program changes;
each such place is marked "(v19)" (earlier marks "(v16)", "(v17)", "(v18)" are v18's). The algorithm's computation,
its success studies and its output are v15's: v19 computes the same trail, the same T3 keys, matches and decisions,
the same B', connector and E outputs, and every R5 and R6 run is a complete run of v19.

## U. What v19 changes (three cheaper counted programs, two development items added; no new heuristic, cap, constant or run of the algorithm)

| Change | Where | v18 | v19 | Evidence |
| --- | --- | --- | --- | --- |
| U.1 Match step | P, T3 (2.1) | 83 per match (run index and end test, the match counter loaded, incremented and stored with its cap test, 14 loads, two popcounts, five masked sum stages) | 62 per match; A's 7 words and the match counter with its M_CAP test move to once per (a, block): 11, inside the 2^6 sort-and-merge bound per half vector per block (37 + 11 = 48) | r5-mitm-1 trial 2: every per_a counts exactly 11 and every match_step exactly 62 on every level-64 match of the output core in 4 seed-picked blocks; AS, decision and counter equal the plain evaluation |
| U.2 E stage 1 | E (2.4) | 75,386 per block of 256 Gray steps | 69,242: the 24 words of D1[0] stay in registers | r5-count trials 0, 2, 4, 6: every step's count equals the new formula, every step's words equal the plain evaluation |
| U.3 T2 leaf | P, T2 (2.1) | 166 per leaf with its Gray step (32 lookups of a 1024-entry table) | 56: a bitsliced test of ALLOW (22) and the same 2-word Gray step (at most 34) | r5-count trials 1, 3, 5, 7: the test equals ALLOW on all 32 row values, then 64 leaves equal the plain test, each at most 56 |
| U.4 D15 completed | 0.1, V.3 | the T1/T2 run that wrote cores.bin (the input of every native T3 run of D15) is not charged | charged at the counted prices of the submitted programs: 2^26.5335 units | v15's Appendix A (cores.py, export.py) |
| U.5 D19 | 0.1 | - | every run we made for v19 except executions of the organizer's harness: 2^28.9135 units | U.5 |

Result: algorithm 2^31.4335 -> 2^31.3507; development 2^33.5070 -> 2^33.4106; total 2^33.8145 -> **2^33.7207, claimed
33.7208**; preprocessing 33.64 -> 33.53. Success probability 0.40 with v15's evidence (R6 44/48, R5 46/48), unchanged:
each change computes the same values in the same order, and no cap, constant or rule changes, so every R5 and R6 run is
a complete run of v19 (Lemma 6c, U.6). For comparison: v18 with U.4 alone would be 2^33.8365; v19's program changes
alone (without U.4 and D19) give 2^33.6579.

Credits first. v19 is **Meganpark980320's v18** (f1eb6445; its v17 168a1b3a) with the changes in this table and nothing
else; v18 is **rubenmarcus's v15** (91f1424d) with five accounting changes (Section V); v15 is winglock's v14
(f1cedf6b, with **Th0rgal**). The T3 meet-in-the-middle (with the zero-block half-sum match of **Subflatus3**'s
9bccf245), the counted fast exhaustive search, D15 and R6 are v15's; the counted T3 programs, B' at its true cost, the
run-free caps, the unrolled E blocks and the repriced development are v17's and v18's; the zero-advice framing is
Th0rgal's 7deb1595 (with Subflatus3 and rubenmarcus). Co-authors of v19: Meganpark980320, rubenmarcus, Th0rgal and
Subflatus3. Only the items of this section are new; Sections V and 0-8 keep v18's text, with "(v19)" marking each place
where a number or program changes.

### U.1 Match step: 62 per match, 11 per (a, block) (match_step and per_a in r5.py)

v18's match step (V.1) costs 83: run index and end test 4; the match counter loaded, incremented and stored, and its
cap test, 5; A's and B's 7 plane words loaded and XORed 21; the active-row word 4 and the folded tail 6; a SWAR popcount
of each, 10 + 10, and their sum 1; five masked horizontal stages 20; the test 2. In T3 the matches of a half vector a in
a block are one run of equal keys of half B after the merge. v19 computes the same AS and decision with two counted
pieces:
- per_a, once per (a, block) whose run is not empty: A's 7 words loaded once and kept in registers over the run, and
  the match counter (kept in a register for the whole of T3) advanced by the run length (a subtraction of the run's end
  and start, and an addition) with the M_CAP test: 7 + 2 + 2 = **11**. It is charged inside the bound of 2.1 for one
  half vector in one block (2^6), of which V.1 uses 37 (key extraction 3, two radix passes of 14, the merge step 6);
  37 + 11 = 48 <= 64, so P's sort-and-merge term is unchanged.
- match_step, per match: run index and end test 4; B's 7 loads and 7 XORs with A's registers 14; active-row word 4
  and folded tail 6; the first SWAR stage of each word 3 + 3; the second stage of both words and their sum 9 (4-bit
  fields at most 4 + 4); bytes 4 (masked; at most 16); 16-bit fields 4 (masked; at most 32); four unmasked
  shift-and-add stages by 16, 32, 64 and 128 bits 8 (no field exceeds 16 x 32 = 512 < 2^16, so no carry crosses a
  field); the final mask 1; the test 2: **62**. The step has a single path.

The cap: v18 raises CapReached at the first match that takes the counter above M_CAP; v19's per_a raises it before
the run whose matches would take the counter above M_CAP, that is at the same (a, block) run. CapReached means no
output, so P's output and its stopping rule are unchanged. (mitm_core, the Python driver, keeps v15's per-match test,
which r5-count trials 8 and 9 exercise.) Registers: A's 7 words, the counter and the step's temporaries, far below 64.

Evidence: r5-mitm-1 trial 2 (the organizer seed picks 4 blocks of the output core at level 64): every per_a counts
exactly 11 and every match_step exactly 62. For every match, AS and the decision equal the plain evaluation, and the
counter equals the number of matches. Our prototype proto_match.py checked all 49,060 level-64 matches of the output
core (the 30 with AS < 64 included) and 344 level-32 matches (folded keys) against v18's match_step and the plain
evaluation. r5-count trial 10 still checks the 49,060 matches and 30 evaluations through the plain driver.

Price: P's matches 2^24 x (62 + 2^11) = 2^24.6390 units (v18 2^24.6532). D15's matches are priced at 62 by the rule
of V.3 (U.6).

### U.2 E stage 1 with D1[0] in registers (fes_step in r5.py)

In the recursion of 2.4, D1[b1] is read and written only at steps whose lowest set bit is b1. So D1[0] (colex rank 0)
is touched only at odd steps, and at every odd step. v19 keeps its 24 words in registers for the whole space. They are
loaded once after the setup, and those 24 loads lie inside the setup bound of 2^16 units, which is about 18,000 units
above what the setup uses (2.4). At an odd step the D1 update needs no load and no store, which saves 2 per equation
when the step has two or more set bits. When the step has one set bit, F's update needs no load, which saves 1 per
equation. A step therefore counts 29 + 2 x (positions from the block index) plus a vector term. At even steps the
vector term is 24 x (2, 5, 8, 11), as in v18; at odd steps it is 24 x (1, 3, 6, 9), for 1 to 4 set bits. Per block of
256 steps:
- 128 odd steps at most 245 and 128 even steps at most 293;
- 2 x (4 + 24 + 56 + 56) = 280 for the positions taken from the block index;
- the prologue, at most 98.

That gives 128 x 245 + 128 x 293 + 280 + 98 = **69,242 primitives per block** (v18 75,386), 270.48 per step;
per space 2^16 x 69,242 = 2^32.08 primitives.

Registers: F 24, D1[0] 24, at most 5 temporaries and the control values (2.4: at most 16 besides F), at most 64, the
model's limit. The words computed and their order are v18's (Lemma 4 unchanged).

Stage 2 (a pair of the pass word) may spill and restore the 48 register words. That is at most 96 primitives per
stage-2 pair, inside 2.4's 2^11 primitives per pair. Those 2^11 cover at most 32 basis additions of 7 words (448), the
second message (14), the 256-bit comparison and the output, all far below 2^11 - 96.

Evidence: r5-count trials 0, 2, 4, 6 run two blocks (511 steps). They check every step's count against this formula
and every step's words against the plain evaluation. Our build check check_e1.py ran v19's fes_step next to v18's on
the same state for 2 x 1,023 steps. F, the pass words and every derivative vector were equal at every step. The counts
differed by exactly 24 x 2 or 24 x 1 at odd steps and by 0 at even steps (24.0 per step on average).

The same block price applies, by the rule of V.3, to G2's 530 and C's 768 E spaces. Each space saves 2^16 x 6,144 =
402,653,184 primitives.

### U.3 T2 leaf: a bitsliced test (t2_leaf in r5.py)

ALLOW = {q : DDT[q][0] + DDT[q][16] > 0} = {0, 16, 20, 21, 24, 26, 28, 29, 30, 31}. With x0..x4 the bits of q,
ALLOW(q) = x4 (x2 OR NOT x0)(x3 OR NOT x1) OR NOT (x4 OR x3 OR x2 OR x1 OR x0); r5-count checks this on all 32 values.

v19 keeps the 64 digest-plane rows of L(alpha4) bitsliced. Bits x0..x3 of the 64 rows sit in the four 64-bit lanes of
word 0, and bit x4 in lane 0 of word 1. Knuth's Algorithm H updates them with the same 2-word XOR per Gray step (gstep,
v15's counted step, at most 34).

A leaf costs **22**:
- the leaf counter and its cap test, 3;
- three lane shifts, 3;
- the 12 gates of the formula;
- the mask of lane 0 and its test, 3;
- the store of a kept leaf, 1.

v18's leaf took 32 table lookups, up to 132. A leaf with its step costs **56** (v18: 166). The leaf is allowed iff all
64 rows are allowed, which is exactly v18's decision, so C1, P45 > 0 and the 467 kept cores are unchanged.

Evidence:
- r5-count trials 1, 3, 5, 7: t2_leaf on each of the 32 row values (in all 64 rows) equals ALLOW. Then, for 64 leaves
  of the output core's walk from a seed-picked point, the decision equals the plain test, the bitsliced words equal
  L(alpha4), and each leaf with its step counts at most 56.
- Our walk of the first 300,000 leaves of the output core (t2walk.py): the leaf counted 21, or 22 when kept (104 kept);
  the step counted 26, 31 or 34; the final state equalled L(alpha4); and sampled decisions equalled the plain test.
- proto_t2.py compared 80,000 leaves with v18's t2_leaf.

Price: P's T2 C1 x 56 = 2^26.0135 units (v18 2^27.5812).

### U.4 D15 completed: the T1/T2 run behind cores.bin

v15's Appendix A shows two steps before T3. cores.py ran T1 (lane_dfs from the 25 lanes, N1 = 8,674,833 nodes) and T2
(p45pos on all 1741 cores). export.py then wrote cores.bin: the rows, compatible differences and their L^-1 images of
the 467 kept cores. cores.bin is the input of every native T3 run that D15 charges: the stopped contiguous run, the
layout comparison and the certified run.

v15's D15 itemization (0.1) does not list that run, and v17 and v18 reprice only the listed items. v19 charges it at
the counted prices of the submitted programs: N1 x 2^12 + C1 x 56 + 2^32 (the export, at P's setup bound) primitives =
**2^26.5335 units**. At v18's T2 price it would be 2^27.7783, and v18 with it would be 33.84.

### U.5 Our development (D19) and every run we made for v19

Rule. D19 charges every run we made for v19 at the counted prices of the submitted programs, with stated bounds where a
count is not exact. It does so whether or not the run fixed a number; none of them did. The one exception is the
organizer's own harness. Local executions of experiments/runner.py, and the certificate check of
scripts/local_tracks.py, run the shipped experiments exactly as every review does and re-derive logged results. They
are verification, as in v15's 0.1, so they are listed and priced, not charged.

| D19 item | What it computed | Price (log2 units) |
| --- | --- | --- |
| contig.c (013c9764...), run by run_contig.sh (061da374...), log contig.log (8f36ff6e...), 2026-10-08T08:09:00Z-08:09:21Z | feasibility count for an idea not adopted (U.7): on 4 sample kept cores, the T3 matches of v15's final layout (equal to MT6: 49,060, 18,965, 10,838, 19,211) and of v15's contiguous layout at every level, with a bit-0 popcount filter on every match | 28.7901: 6,607,302,743 matches x (62 + 31) + 71 x 2^11 + 4 x (2 x 9^5 x (96 + 329 x 2^6) + 329 x 2^17) + 2^32 primitives. As a cross-check, the run retired 336,207,352,387 machine instructions in all (2^27.90 units), below the charge |
| export_cores.py (768f76be...), output cores_sample.bin (bc22aa99...) | T1 for the lanes of the 4 sample cores, and their core tables | 22.8155: 4 x 348,343 nodes x 2^12 + 2^32 |
| prototypes proto_match.py (5356dcb9...), proto_e1.py (440f94bc...), proto_t2.py (4b3120c2...); build checks check_e1.py (43702c79...), t2walk.py (4aee89e5...) | the checks quoted in U.1-U.3 | 21.9577 (bounds per step, leaf, match and setup; ledger_v19.py) |
| p45meter.py (9e251739...), output p45meter.json (780a7348...) | an accounting run: T1 from all 25 lanes, then p45pos with counters on all 1741 cores (1,181,844 calls, 3,412,138 options, 6,731,804 row checks), to price the trail experiments of our local organizer runs | 24.8392: N1 x 2^12 + those events at 64, 32, 64 primitives + 1741 x 2^17 + 2^32 |
| **D19** | | **28.9135** |

Listed, priced, not charged (verification): two local organizer runs, both with Python 3.12 in place of Docker. The
runner executes every experiment twice and compares the outputs byte for byte.
- In our build session, r5-count and r5-mitm-1 on the public seed: 11 of 11 and 3 of 3 PASS (runner report_sha256 8d396f29...).
- All 16 experiments on the public seed, 2026-10-08T13:17:06Z-13:19:27Z, each execution through a meter that records
  B''s counter and the connector's work units (runner report_sha256 aa362d94..., meter file 83adfb86...). Every experiment passed:
  - r5-trail-0..3: 4 of 4;
  - r5-count: 11 of 11;
  - r5-mitm-0, r5-mitm-1: 1 of 1 and 3 of 3;
  - r5-bpfull: trials 0-2 PASS, with 7 of 24 connector attempts accepted and verified;
  - r5-R-0..7: 16 full collisions.

  Each execution took at most 6.8 CPU-s and 87 MB.

We priced these runs like D19:
- B' at its true cost from the metered counters (WK + WK.d, which covers Base, candidates, attempts and coins);
- connector attempts at the algorithm's price;
- T1 at 2^12 per node;
- the trail experiments' pruned P45 search as counted by p45meter.py;
- stated bounds for the rest (E windows at counted E prices, facts() 2^30, module tables 2^32 per execution).

The runs come to 2^27.9777 and 2^25.3189 units; the certificate check is 2^9.65. Charged, the claim would be 33.76.
None of these runs, and no D19 run, fixed a constant, cap or rule that v19's algorithm reads. The prototypes and the build checks tested program text (which 0.1 does not charge; D19 charges them anyway); both organizer runs executed the shipped experiments on the final experiment file (r5.py 97815b2c...).

Analysis scripts that compute no target function are not runs: ledger.py, scenarios.py, scenarios2.py, krule.py,
ledger19.py, and ledger_v19.py (whose output is U.8).

### U.6 What v19 reuses from v15-v18, after re-checking it

We re-checked each accounting step that v19 reuses before reusing it.

- **B' at its true cost (V.5).** r5.py's tallies equal the stated prices: Aff.copy subtracts n x (253 - 2w), for a
  true 3 + 2w per entry instead of 256. Aff.add adds 4w per set entry and subtracts 505 per entry, for a true 7 + 4w
  on set entries instead of 512. Here w = (n + 256) // 256 = 7 or 11 words for the n = 1600 and 2570 entry tables, so
  true <= WK at every event. This is faithful counting of the same execution, and we reuse it. We did not re-derive C's
  48 or G2's 10 B' runs ourselves; their true costs are v17's (V.5). r5-bpfull trial 0 reports a whole R5 B' run's
  true cost on every review: ours gave 2,573,293,728 primitives for run 21, whose WK cost of 16,241,153,777 equals the
  log.
- **E blocks (V.7).** We re-counted 75,386 = 256 x 293 + 280 + 98 from fes_step; v19 starts from it (U.2).
- **Counted T3 steps (V.1).** We re-counted hv_step 96 and match_step 83; v19 replaces the match step (U.1).
- **Caps (V.2).** The three inequalities of v13's rule hold as stated, and no R5 or R6 run reaches X_MAX, S2CAP or
  B_TRUE (V.2, V.5). We reuse them unchanged.
- **D15 at counted prices (V.3).** We recomputed it term by term from v15's published numbers (rounded charges
  +0.005 in log2, stated match counts at their smallest rounding), which reproduces 2^32.3521. At v19's match step the
  three items become 2^31.4988 (contiguous run), 2^29.1769 (layouts) and 2^28.1652 (certified run). The fourth item
  (2^28.9858) is unchanged. With U.4, D15 is 2^32.0899. We found one omission (U.4) and added it.
- **G2 and C (V.5, V.7).** Our ledger recomputes C from its published counts. For G2's non-E part it takes the larger
  of the value implied by v18's published G2 (at its upper rounding) and the sum of its components (B' 2^27.8176 true,
  2,176 attempts at the 2^18 cap, 10 x S): 2^28.2825. This reproduces v18's total as 2^33.8147 (published 2^33.8145).

Inherited premises, disclosed and unchanged:
- A1 is uncharged (V.6); charged, the claim would be 40.99.
- v17's B' re-derivations are listed, not charged; charged at their true cost on v19's ledger, the claim would be 34.30.
- v17's own development is charged as D16 at its stated bound of 2^27.
- Development is priced at the counted prices of the submitted programs. This is the rule of v14, v15 and v17; v19
  applies it to D15's matches, to U.4, and to G2's and C's E spaces.

### U.7 Considered and not adopted

- **S2CAP = 2^11** (8 x the 256 stage-2 pairs expected per space) would give 33.65. We did not adopt it, because we
  chose it after the R5 and R6 maxima (308, 315) were known, so no rule fixed it before every run that could inform it.
- **K from an analytic rule** (44 or 50 spaces), with a new pre-registered success study that would leave C uncharged
  (about 33.0). Not adopted, for the same reason: C, R5 and R6 had run before the rule was written.
- **An exact re-count of v15's contiguous run with a cheap popcount filter** (about 33.5 with this package). Not
  adopted: it would need a new full run of that layout. Only the feasibility run of U.5 was made, and it is charged.

### U.8 Ledger (log2 units; exact rationals, rate 1355; ledger_v19.py)

| Term | v18 | v19 |
| --- | --- | --- |
| P | 29.0537 | 28.6592 (T2 27.5812 -> 26.0135; matches 24.6532 -> 24.6390; rest unchanged) |
| B' | 29.0000 | 29.0000 |
| Connector | 29.4539 | 29.4539 |
| E stage 1 / stage 2 | 28.3829 / 29.3970 | 28.2602 / 29.3970 |
| S, bases, E setup, output | as v18 | as v18 |
| **Algorithm** | 31.4335 | **31.3507** |
| G2 | 31.1003 | 30.9994 |
| C | 31.9977 | 31.9189 |
| D15 | 32.3521 | 32.0899 (contiguous run 31.4988, layouts 29.1769, certified run 28.1652, rest 28.9858, T1/T2 export 26.5335) |
| D16 / D19 | 27 / - | 27 / 28.9135 |
| **Total** | 33.8145 -> 33.82 | **33.7207 -> 33.7208** |
| Preprocessing (P, B', S, development) | 33.6315 -> 33.64 | 33.5279 -> 33.53 |

Sensitivities (not claimed):

| Change | Total |
| --- | --- |
| match step at 83 | 33.83 |
| E at 75,386 per block | 33.77 |
| T2 at 166 | 33.75 |
| all three program changes undone (v18 with U.4 and D19) | 33.89 |
| D19 doubled | 33.78 |
| our local organizer runs charged | 33.76 |
| S2CAP 2^11 (not adopted) | 33.65 |
| D15 doubled | 34.13 |
| v17's B' re-derivations charged | 34.30 |
| A1 charged | 40.99 |

## V. What v17 and v18 change (accounting of v15's own computation; no new heuristic; v18's text and numbers, superseded where Section U says so)

| Change | Where | v15 | v17 | Evidence |
| --- | --- | --- | --- | --- |
| Counted half-vector step with all keys | P, T3 (2.1) | 2^7 per half vector + 2^11 per half vector per level for keys (bounds) | 96 primitives per half vector, all 127 keys of the 7 levels included (counted) | r5-mitm-1 trial 1: both full half tables of the output core (118,096 counted steps) |
| Counted match step | P, T3 (2.1) | 2^9 per match (bound) | 83 per match (counted; one path below the cap) | r5-mitm-1 trial 2: every level-64 match of the output core in 4 seed-picked blocks |
| B' at its true cost | B' (2.2) | every "row" event at 256 primitives, including Aff's table update (2 events = 512 per table entry) and copy (256 per entry) | those two sites at their true word cost (V.5); a true-cost budget B_TRUE = 2^29 units by the run-free cap rule; v14's counter, CCAP and B_BUDGET unchanged | r5-bpfull trial 0 reports the true cost of a whole B' run; Section V.5 table |
| Caps | 2.3, 2.4, 2.6 | X_MAX = 2^23, S2CAP = 2^24 | X_MAX = 2^20, S2CAP = 2^21 (run-free rule, V.2) | largest R5/R6 attempt 190,240 work units, stage-2 count 315 |
| E stage 1 by unrolled blocks (v18) | E (2.4) | every Gray step at its longest path, 364 (74 of it control: the lowest set bits of the step index by a comparison tree, their ranks) | 256 steps per block as straight-line code: positions below bit 8 are program constants, those from the block index are computed once per block (at most 98); a block costs at most 75,386 = 256 x 293 + 280 + 98 (294.48 per step) | r5-count trials 0, 2, 4, 6: two blocks (511 steps), every step's count equals its formula, the prologue at most 98 |
| Development | 0.1 | G2 2^31.8877, C 2^33.2426, D15 2^34.6617 | G2 2^31.1003, C 2^31.9977 (their B' at true cost, V.5; their E spaces at v18's E, V.7), D15 2^32.3521 (V.3), D16 2^27 | V.3, V.5, V.7 |

Result: algorithm 2^33.9407 -> 2^31.4335; development 2^35.2659 -> 2^33.5070; total 2^35.7504 -> **2^33.8145, claimed
33.82** (v17: 33.93); preprocessing 33.64. Success probability 0.40 with v15's evidence (R6 44/48, R5 46/48), unchanged.

### V.1 The counted T3 programs (hv_step, match_step in r5.py)

**Half vectors with all keys.** Every key of every level is a linear function of the half vector (the block's row
fields folded into 26 bits by XOR with rotation; at 64 blocks the 25-bit field itself), so the key of a sum is the sum
of the keys. hv_step therefore tabulates, with each half vector, all 127 keys of the 7 levels (9 keys of 26 bits per
256-bit word: 15 key words), stepping them by the same mixed-radix Gray XOR as the 7 plane words of the vector. One
step: Knuth's Algorithm H control (as T2's counted gstep), the choice and weight loads, the w2 update, 22 words
loaded, XORed and stored (the stored entry), and the focus-pointer updates: **96 primitives** on the longest path,
counted with r5.py's W operators (load, st count 1, test 2). The per-row difference tables cost at most 10 rows x 32
differences x (22 words + 7 x 320 x 6 primitives of key folds) per core, below 2^31 primitives over all 467 cores; P's
setup bound is raised from 2^31 to 2^32 primitives to cover it. The sort-and-merge price per half vector per block
(2^6) includes extracting the key from its key word (3; two radix passes of 14 and the merge step of 6: 37 < 2^6).
The keys are exactly v15's keys (r5-mitm-1 trial 1 compares all 22 words with to_planes and mkey of v15's halves() at
sampled steps of both full tables of the output core), so match sets, counts (7,251,935 in the native run),
evaluations and P's output are v15's (Lemma P unchanged); the table order does not affect P's output.

**Match step.** alpha2 = LA(a) + LB(b) in 7 plane words (bit x of rows 0..255 in P_x; tail rows of planes 0..3 in T,
of plane 4 in T2). One match: bucket-run index (load, add, end test), the match counter and its M_CAP test, 14 loads
and 7 XORs, the active-row word P_0 | ... | P_4 and the folded tail, a SWAR popcount of both, and the test AS < nb:
**83 primitives**, counted; the step has a single path below the cap. r5-mitm-1 trial 2 checks AS and the decision
against the plain evaluation on every level-64 match of the output core in 4 seed-picked blocks; v15's r5-count
trial 10 still checks all 49,060 matches and the 30 evaluations of that level. The full evaluation keeps 2^11.

### V.2 Caps by v13's run-free rule

v13 set X_MAX and S2CAP by a rule that used no run: each the largest power of two whose charged term stays within a
reference term (v14's T3 batch term, 2^43 primitives). v15 removed that term and kept the caps. v17 re-applies the
rule with the term that replaced it, v15's P charge (2^40.43 primitives), rounded down to 2^40:
- X_MAX: 2^13 x (X x 96 + 2^15 x 2^9 + 2^22) <= 2^40 holds for X = 2^20, not 2^21;
- S2CAP: 96 x S x (2 x 1355 + 2^11) <= 2^40 holds for S = 2^21, not 2^22;
- B_TRUE (V.5): B_TRUE x 1355 <= 2^40 holds for 2^29 units, not 2^30.
No number is computed from a run. None binds in any run we know of: the largest connector attempt is 189,224 work
units in R5 and 190,240 in R6 (2^20 = 1,048,576); the largest stage-2 count is 308 (R5) and 315 (R6) against 2^21
(256 expected per space: 2^32 pairs, 24 equations); the largest true B' cost of a run is 2^27.972 units in R5 and
2^28.2709 in R6 (V.5) against 2^29. Hence every R5 and R6 run is a complete run of v17 with the same output (Lemma 6c),
and the success evidence carries over unchanged. A binding cap only fails an attempt, ends a space or ends B''s
search; it never makes a cost bound wrong.

### V.3 D15 at v17's T3 prices (H2)

The rule is v14's and v15's: development is charged at the counted prices of the submitted programs (v15 used it to
price v14's G2 and C at v15's counted E). Applied to v15's own D15, whose cost is almost entirely T3 work, it changes
two prices: a match (2^9 -> 83) and the keys (2^7 + 2^11 per level per half vector -> 96 or, for a run with more
keys, 30 + 3 x (7 + key words)). **Every input below is a number v15 published (its proof 0.1); we reconstruct no
D15 workload.** Where v15 gives a rounded charge we take it rounded up (+0.005 in log2), and where it gives a match
count we take its smallest rounding (4.25 x 10^10 -> 4.245 x 10^10); both choices can only raise the result.

| D15 item (v15's 0.1) | v15 log2 units | v17: v15's charge minus the stated savings | v17 log2 units |
| --- | --- | --- | --- |
| stopped contiguous-block run, levels nb = 1, 2, 4, 5, 8, 10, 16, 20, 32, 40 (all divisors of 320 up to 40; the tenth level charged complete) | 34.33 | 2^34.335 x 1355 - 429 x (4.245 + 1.145) x 10^10 (the matches v15 states for its last two levels, each now 83 instead of 512) - HV x (2^7 + 10 x 2^11 - 99) (keys of 10 levels, 16 key words) | 31.8496 |
| comparison of six layouts at nb = 64 | 32.00 | 2^32.005 x 1355 - 429 x 1.115 x 10^10 (contiguous-layout matches, v15: 1.12 x 10^10) | 29.5384 |
| certified native run (fixed M_CAP) | 29.61 | exact: HV x 96 + 127 x HV x 2^6 + 127 x 467 x 2^17 + 7,251,935 x 83 + 30 x 2^11 | 28.1657 |
| count-only recounts, Python T3 re-runs, stage-1 development, driver self-test | 27.40, 25.06, 19.36, 28.24 | kept, each rounded up | 28.9858 (sum) |
| **D15** | **34.6617** | | **32.3521** |

D16 (our development for v16/v17, charged at a stated bound of **2^27 units**): Python checks of the counted programs
on the output core and local executions of the organizer experiments. None fixed a number: the step prices are counted
from program text, the caps come from the rule. The B' re-derivations of V.5 are listed there.

### V.4 Ledger

| Term | v15 | v17 (log2 units) |
| --- | --- | --- |
| P | 30.0286 | 29.0537 (half vectors incl. all keys 21.7151; keys term 28.9375 -> 0; matches 25.5959 -> 24.6532; setup 2^32 primitives) |
| B' | 32.0000 | 29.0000 (B_TRUE) |
| Connector | 32.2180 | 29.4539 |
| E stage 1 | 28.6887 | 28.3829 (v18, V.7) |
| E stage 2 | 32.3970 | 29.3970 |
| S, bases, E setup, output | as v15 | as v15 |
| **Algorithm** | 33.9407 | **31.4335** |
| G2 | 31.8877 | 31.1003 (its B' 2^30.4349 -> 2^27.8175; 530 E spaces at v18's E) |
| C | 33.2426 | 31.9977 (its B' 2^32.5422 -> 2^29.9498; 768 E spaces at v18's E) |
| D15 | 34.6617 | 32.3521 |
| D16 | - | 27 |
| **Total** | 35.7504 -> 35.76 | **33.8145 -> 33.82** |
| Preprocessing (P, B', S, development) | 35.4430 -> 35.45 | 33.6315 -> 33.64 |

Sensitivities (not claimed; every one below v15's 35.76): E stage 1 at v17's 364 per step 33.9248; B' at v15's 2^32 budget
(no B_TRUE) 34.1350; G2 and C B' at WK prices 34.3990; D15 doubled 34.2612; B_TRUE, G2/C B' repricing and the E change all undone
34.6249.

### V.5 B' at its true cost

B''s counter WK charges 256 primitives per "row" event, and its budget (B_BUDGET = 2^32 units), candidate cap (CCAP)
and every logged B' cost of v14's studies are in WK's units. Profiling whole B' runs (R5 runs 21, 24, 42) shows that 98.8%
of WK's cost is row events and that two sites make about 86% of the row events:
- Aff.add's table update `s.T = [t ^ af if t & pb else t for t in T]`, charged 2 row events (512 primitives) per
  table entry. pb is a single bit, so the test reads one word of the entry: loop control 3, load 1, AND 1, test 2
  (7 per entry); only an entry whose bit is set is XORed with af: w loads, w XORs, w stores and w loads of af (4w,
  w = 7 words for the 1600-entry tables of 1,601-bit rows, 11 for the 2,570-entry tables of 2,571-bit rows).
- Aff.copy, charged one row event (256) per entry: loop control 3 and the entry's w loads and w stores (3 + 2w).
Every other site keeps WK's price. Both true prices are below WK's at every event (at most 51 < 512 and 25 < 256),
so the true cost of any B' execution is at most its WK cost.

r5.py now keeps, next to WK's counter, the exact difference between the true cost and WK's cost at these two sites
(WK.d; it counts the set entries of every update). WK's counter, CCAP and B_BUDGET act exactly as in v14 and v15, so
B''s execution and output are unchanged. The algorithm adds one budget on the true cost, **B_TRUE = 2^29 units**
(the rule of V.2), over all of its B' calls; B' fails if the true cost exceeds it. The algorithm's B' term is
therefore 2^29 units plus one update (no update's true cost exceeds its WK cost, below 2^13 units).

Every B' run that enters a number of this claim was re-derived from its label with the experiment file's code (the
advice, rounds and (c, j) of every run reproduce the logs; WK costs equal the logs up to a constant setup term counted
outside bprime in the logged figures: C's total differs by 435,644,112 primitives (0.005%), G2's runs by 11,182,080
each; we add these differences at WK's price; the constants of v13's runs are v13's: R = 16, DMIN = 40,
weights 1, 0.25, 1, 1, which are the only differences between v13's and v14's B' code):

| Runs | Count | WK cost (logged = re-derived) | True cost | Ratio |
| --- | --- | --- | --- | --- |
| C (v14's pre-registration C, labels "hashsmash sha3-256-r5 v11 C B-prime run k") | 48 of 48 | 8,469,206,995,669 primitives re-derived; logged total 8,469,642,639,781 | 1,404,774,725,208 primitives; the logged total minus our re-derived WK sum is added at WK's price | 0.166 |
| G2: v6 run and pre-registration A (labels of v13's BRUNS) | 1 + 9 | 2^30.4349 units (each run's logged cost; our re-derivations miss a constant 11,182,080 primitives of setup per run, added at WK's price) | 2^27.8175 units | |
| R5 (all rounds of each run) | 39 of 48 re-derived | every logged run at most 2^28.73 units, below B_TRUE | largest re-derived 2^27.972 units | |
| R6 (all rounds of each run) | 39 of 48 re-derived, including the only two runs logged above 2^29 (runs 23: 2^29.61, and 28: 2^29.05) | largest 2^29.6107 units (run 23) | run 23: 2^28.2709, run 28: 2^27.0369 units | |

So C's B' costs 2^29.9498 units instead of 2^32.5422 and G2's B' 2^27.8175 instead of 2^30.4349. No R5 or R6 run
reaches B_TRUE: a run's true cost is at most its logged WK cost, which is below 2^29 for every run except R6 runs 23 and
28, and those two were re-derived at 2^28.27 and 2^27.04 units. Each is a complete run of v17. r5-bpfull trial 0 (a whole B' run of R5 picked by the organizer
seed) reports the true cost next to the logged WK cost. These re-derivations fix no number (B_TRUE comes from the rule;
the prices from program text): like v14's re-derivations of R5 they are listed, not charged. If they were charged,
at their true cost (about 2^32.7 units in all) the total would be 34.44, at WK's price (about 2^34.3) 35.13; both are
below 35.76.

### V.7 E stage 1 as unrolled blocks (v18)

v15's counted stage 1 charges every one of the 2^24 Gray steps at its longest path, 364 primitives per 256 pairs: 264
for the derivative vectors (per equation at most 4 loads, 4 XORs and 3 stores), 26 for the pass test, and 74 of
control, mostly finding the up to four lowest set bits of the step index i by a comparison tree and the colex ranks
that address the derivative vectors. That control depends only on i, not on the data. v18's stage 1 is the same
recursion, in the same Gray order, computing the same words (so Lemma 4 and every output are unchanged), written as
blocks of 256 steps of straight-line code: in step r of a block (i = 256 B + r) the set bits of i below bit 8 are
those of r, constants of that step's code, and their ranks are constants. The set bits taken from B (only when r has
fewer than four set bits) and their partial ranks are computed once per block by a prologue (pro in r5.py: the
comparison tree on B, at most 4 x 16 primitives, and 16 load-and-add pairs for the partial-rank table: at most 98).
A step then costs its counter and end test (3), one load and one add for each position taken from B (2 per
position), the vectors (24 x 2, 5, 8 or 11 for 1 to 4 positions) and the test (26). Over the 256 steps of a block
(r = 0 takes all four positions from B, the 8 values of r with one set bit take three, the 28 with two take two, the
56 with three take one): at most 256 x 293 + 2 x (4 + 24 + 56 + 56) + 98 = **75,386 primitives per block**, 294.48
per step, against 364. Per space: 2^16 blocks x 75,386 = 2^32.20 primitives. r5-count trials 0, 2, 4, 6 now run two
blocks (outer coordinates 0..8, 511 steps, the second block's prologue and its steps with a position from B
included) and check, besides the plain-evaluation equalities of v15, that every step's count equals 29 + 2 x (positions
from B) + 24 x (2, 5, 8, 11) and that the prologue counts at most 98.

The same price applies, by the rule of V.3, to the E spaces of the charged development: G2's 530 and C's 768 spaces
(each saves 2^24 x 364 - 2^16 x 75,386 = 1,166,409,728 primitives).

### V.6 A1 (v7's design study) stays uncharged, as in v13, v14 and v15

A1 (v7's design study: a connector without steering, annealers, backtracking and benchmarks; 10,432 CPU-s) produced
the text of B''s D2u and M2 phases. The cost model charges construction, preprocessing and advice, including any search
omitted from the submitted program: work whose result the attack uses. No result of A1 is an input of the algorithm:
B' reads only P's trail and the fixed bits, its constants are fixed by rule or by charged runs (G2, C; 0.2), and its
whole computation is charged every time it runs (here at its true cost). A1's outputs were comparisons between program
designs; replacing them by any other way of writing the same program text would not change any count, cap, constant
or output of the algorithm. Charging the research that led to a program's text would charge every package for its
authors' experiments; the lineage's packages that qualified (v8 at 40.26, v13, v14, v15) all treat A1 this way. The
claim if A1 were charged at 2^38 primitives per core-second is 40.98 (0.1).

Credits for v17: the base is rubenmarcus's v15 (91f1424d); everything not listed in this section is theirs or, through
v15, winglock's (v8, v13, v14), Th0rgal's and Subflatus3's, as credited in Section 8. In Sections 0-8, "our" and "we"
mean the v15 authors unless marked (v16) or (v17).

---

(v15's text follows; it is v15's proof with the v16/v17 edits marked.)

## 0. Claim, summary, changes

| Field | Value | Basis |
| --- | --- | --- |
| time_log2 (v19) | 33.7208 | v19: 2^33.7207 (Section U.8); v18: 2^33.8145 (Section V). v15's basis was 2^35.7504, rounded up: the algorithm, 2^33.9407 (Section 6), plus the charged development: v14's G2 (2^31.8877) and C (2^33.2426), priced at v15's counted programs as v14's rule prescribes, and our own development D15 (2^34.6617) (Section 0.1) |
| success_probability | 0.40 | R6 (pre-registered, 48 complete runs of v15): 44 successes, one-sided 95% Clopper-Pearson bound 0.8193; R5 (v14's, 48 runs that are complete runs of v15): 46 successes, bound 0.874 (Section 5) |
| preprocessing_log2 (v19) | 33.53 | P, B', S and the charged development: v19 2^33.5279, v18 2^33.6315 (v15 2^35.4430) |
| memory_log2_bytes | 30 | largest phase about 2^28 bytes (Section 7) |
| nonuniform_advice_log2_bytes | 0 | the algorithm computes its trail and its connector advice; development is charged as preprocessing |

Board when this was written (2026-10-08): v8 113fc836 promoted at 40.26; lowest pending claim v14 f1cedf6b at 37.05.

What the two changes are worth, term by term (log2 units; Section 6): P 33.65 -> 30.03; E stage 1 32.76 -> 28.69;
v14's E setup (96 x 2^24 primitives, 2^20.18 units) is replaced by the fast exhaustive search's setup (96 x 2^16
units, 2^22.59; larger, and negligible). The algorithm goes from
2^35.0558 to 2^33.9407; its remaining large terms are v14's caps (B' 2^32, connector 2^32.22, stage 2 2^32.40), which
v15 keeps unchanged (2.6). v14's charged development G2 and C consists mostly of E on 530 and 768 spaces; priced at
v15's E (as v14 priced it at v14's E), it falls from 2^35.28 and 2^35.91 to 2^31.89 and 2^33.24. Our own development
(D15, 2^34.66) is charged in full; most of it is one abandoned run of an earlier block layout of T3.

Sensitivities (not claimed; Section 0.1): G2 and C at v14's prices instead of v15's: 37.13, which is not below v14's
37.05; so the improvement rests on pricing development at the submitted programs' counted prices, which is v14's own
rule (H2). Without our development D15: 34.83. D15 at twice its charge: 36.31. All of v14's uncharged items charged
as in v14's table: see 0.1.

### 0.1 Development: what is charged, and why (H2)

Rule (v14's, unchanged). The cost model counts all construction, preprocessing and advice, including any search
omitted from the submitted program. Every target-specific run whose result fixed a number that the algorithm reads,
or whose plan would have changed such a number on another outcome, is charged as preprocessing, at the counted prices
of the submitted programs (the prices of the claim). Runs that only produced program text, or only measured the
success of the algorithm as submitted, fix no number; they are disclosed with the claim they would give. Where only CPU
time is known, a sensitivity uses 2^38 primitives per core-second (v14's rate).

Charged:

| Id | Runs | What they fixed | Price | log2 units |
| --- | --- | --- | --- | --- |
| G2 | v14's G2: the v6 run (B' 2^27.12 units by its exact counters, 1,024 connector attempts, E on 512 spaces); pre-registration A (9 B' runs, 2^30.28 units, 9 x 128 attempts); pre-registration B (E on 18 spaces) | K = 96, CCAP = 2^26 units, B_BUDGET = 2^32 units, A_ADV = 2^11, A_MAX = 2^13 (v10) | as in v14 (each attempt at its cap then, 2^18 x 96 + 2^24 + 2^22 primitives; each advice's S at 2^31 primitives), each space at v15's E: bases 2^24 primitives, setup 2^16 units, 2^24 steps of 364 primitives, 2^11 stage-2 pairs (2^22.13 units per space) | 31.8877 |
| C | v14's pre-registration C (48 runs of v13's algorithm to E's first 16 spaces) | its rule would have raised K had its bound been below 0.40 | B' at its exact WK counts (8,469,642,639,781 primitives), 9,097 attempts at their 2^18 cap, 48 x S, 768 spaces at v15's E; these spaces were computed by fes.c, which is v15's stage 1 | 33.2426 |
| D15 | ours, listed below | the block layout of T3 (contiguous rows replaced by row (y, z) in block (z + 13 y) mod 64) and M_CAP | P's prices of 2.1 per half vector, key, entry and block; 2^9 primitives per match and 2^11 per full evaluation (the bounds of 2.1 without the evaluation when none was made); B' and connector at v14's prices | 34.6617 |

D15 itemised (log2 units): the first native T3 run, with contiguous blocks of 320/nb rows (levels nb = 1 to 40), stopped
during its tenth level and charged with that level complete (4.25 x 10^10 matches there, counted afterwards without
enumeration; 1.15 x 10^10 at its ninth level): 34.33; the comparison of six block layouts on 8 cores at nb = 64 (the
contiguous layout charged complete, 1.12 x 10^10 matches, counted afterwards): 32.00; the certified native run (2.1),
which fixed M_CAP: 29.61; the count-only measurements just mentioned: 27.40; Python re-runs of T3 for checks: at most
25.06; development and checks of the counted stage 1: at most 19.36; the driver's self-test (a replay of R5 run 4):
28.24. Total 34.6617.

Charged development: 2^31.8877 + 2^33.2426 + 2^34.6617 = 2^35.2659 units, all of it preprocessing. (v19: G2 2^30.9994, C 2^31.9189, D15 2^32.0899 with the T1/T2 export of U.4, D16 2^27, D19 2^28.9135: 2^33.4106; Sections U.4, U.5, U.8.)

Why G2 and C are priced at v15's E. This is v14's rule: "at the counted prices of the submitted programs", justified
in v14 by "the search that G2 performed, if added to the submitted program, would run on the program's own counted
routines". v14 applied it by pricing G2's spaces at v14's counted E rather than at the v8 enumerator they ran. v15's
counted E computes the same function of the space (Lemma 4), so the same rule prices them at v15's E. For C the case is
stronger: its 768 spaces were enumerated by fes.c, whose stage 1 is v15's counted stage 1. At v14's prices the claim
would be 37.13 (with G2's spaces at the v8 enumerator that the v6 run actually ran, as in v14's sensitivity: 39.94).

Not charged (each fixes no number of v15; claim if charged, with the price named):

| Id | Runs | Why nothing is fixed | Claim if charged |
| --- | --- | --- | --- |
| A1 | v7's design study that produced B''s code (10,432 CPU-s) | code, not a number; the code is charged every time it runs | 40.98 (2^38 primitives per core-second) |
| A2 | v13's B' tuning (at most 1,559 CPU-s) | v14 and v15 use none of its constants | 38.44 (same rate) |
| R5 | v14's success study (48 runs) | its plan fixed every constant before any run | 36.23 (v15's prices) |
| R6 | our success study (48 runs, Section 4.7) | its plan fixed every constant before any run; its only rule is whether to claim | 36.44 (v15's prices) |
| C' | v14's parallel session (at most 12,537 CPU-s) | its plan fixed the values before its runs | 41.24 (2^38 per core-second) |
| D | v14's pre-registration D | it measured v13's success | at most 36.93 (v14's prices) |
| A3, A4 | v7's abandoned plan and B' run (at most 535.6 CPU-s) | nothing | 37.28 |
| B | v14's native T3 passes and v7's P run | nothing: v15's P computes its output itself | 36.52 (3 runs at v14's P price) |
| local | organizer-experiment runs on our machine (Section 4.6) | re-derivations of logged results | - |

### 0.2 Where every number of v15 comes from

The numbers of B', the connector and the driver are v14's, with v14's origins (v14's Section 0.2): B''s constants are
values no run chose; CCAP, B_BUDGET, K, A_ADV, A_MAX come from G2 (charged) and K was kept by C's rule (charged);
connector DMIN = 33 is the least DF for which E's 32-dimensional window and beta exist; X_MAX, S2CAP and B''s budget
satisfy v13's cap rule (2.6). New numbers:

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

sha3-256-r5-prefix-v1 is FIPS 202 SHA3-256 restricted to rounds 0-4 of Keccak-f[1600]: rate 1088, capacity 512, zero
initial state, suffix 0x06 with pad10*1, digest = lanes 0..3 after the 5 rounds. Round i maps A to chi(L(A)) xor
RC[i], with L = pi o rho o theta. State bit (x,y,z) has index 64(x+5y)+z. chi acts on the 320 rows (y,z) by chi5(v)_i
= v_i xor (NOT v_{i+1}) v_{i+2}. All messages are exactly 135 bytes: A0 = M || 0x86 || 0^512, so the 520 bits F =
1080..1599 are fixed (1081, 1082, 1087 are 1). For a pair, alpha_i is the difference entering round i, beta_i =
L(alpha_i) the difference entering chi. DDT[d][o] = #{v : chi5(v) xor chi5(v xor d) = o}; V(d,o) = {v : chi5(v) xor
chi5(v xor d) = o} is an affine set of dimension log2 DDT[d][o], so a row transition is w = 5 - log2 DDT affine
equations on one message's row value. x = L(A0) is the first message's round-0 chi input.

Cost model (collision-frontier-v5): one 5-round permutation is 1 unit; every other primitive on 256-bit words (load,
store, add/sub, AND/OR/XOR/NOT, shift or rotation, comparison, conditional branch, fresh random word) is 1/1355 unit.
Our counted programs count every executed load, store, operation, comparison and branch as one primitive; shift
amounts, masks and constant addresses are instruction fields; values live in at most 64 registers (the bound is
stated per program). A 256-bit word holds one bit of each of 256 pairs (or leaves): bitslicing.

## 2. The algorithm and its charges

Phases: trail search P (2.1), advice program B' (2.2), setup S and connector (2.3), enumeration E (2.4), driver
(2.5). Section 6 lists every term, the cap that enforces it and its price.

### 2.1 Trail search P (deterministic; T1 and T2 as in v14, T3 by meet-in-the-middle)

P outputs the 2-round in-kernel core alpha3 and the beta2 that minimise w1 (then w2, then the earlier core, then the
least choice vector: v14's order).

T1 (cores), unchanged: a candidate alpha3 is a set of at most 10 bits whose alpha-columns and beta-columns (columns of
pi o rho of each bit) all hold an even number of bits; depth-first search from bit (lane, z = 0) for each of the 25
lanes; at a node let c be the smallest odd alpha-column, else the smallest odd beta-column; if none, record the core in
canonical form (least sorted bit list over the 64 z-translations), else, below 10 bits, branch on each bit of c not
yet in the set. N1 = 8,674,833 nodes, 1741 cores. Price: 2^12 per node (as in v8: at most 2^9 per node outside the
17,100 core events, a core event at most 2^15, and N1 x 2^9 + 17,100 x 2^15 < N1 x 2^12).

T2 (forward), unchanged: for each core, beta3 = pi o rho(alpha3); the C1 leaves alpha4 compatible with beta3 are
visited in reflected mixed-radix Gray order (Knuth's Algorithm H over the rows of beta3); the 64 digest-plane rows of
L(alpha4) are kept as 32 row pairs (10-bit fields of 2 words) and updated by XOR. A leaf is allowed iff every
digest-plane row q has DDT[q][0] + DDT[q][16] > 0 (32 lookups of one 1024-entry table); the core is kept iff some leaf
is allowed, which is P45 > 0 (Section 3). C1 = 1,639,088,128 leaves; 467 kept cores. (v19: the rows are kept bitsliced and the leaf is a 12-gate test of ALLOW, 56 with its step, Section U.3.) v18's counted price (r5-count) was 166
primitives per leaf on its longest path; v19's is 56 (U.3).

T3 (backward) by meet-in-the-middle on zero blocks of alpha2 (new in v15; replaces v14's exhaustive batches).

- Halves. For a kept core with rows j = 0..n-1 of alpha3 ((y, z) order) and the m_j input differences compatible with
  row j's output difference (ascending), alpha2 = L^-1(beta2) = sum_j L^-1(d_j at row j) is linear in the choices.
  Rows 0..h-1 form half A and rows h..n-1 half B, h the least value that minimises |A| + |B| (|A| = m_0 ... m_{h-1});
  for the 392 cores with ten 9-fold rows, |A| = |B| = 9^5. The half vectors LA(a), LB(b) (alpha2's 320 rows of 5
  bits), their w2 parts and choice vectors are tabulated in mixed-radix Gray order (one XOR of a 10-word difference
  vector each). HV = sum over kept cores of |A| + |B| = 48,592,224 (organizer-recomputed by r5-trail-0..3).
- Levels. A level is a block count nb in (1, 2, 4, 8, 16, 32, 64): row (y, z) of alpha2 lies in block ((z + 13 y) mod
  64) mod nb, so each level refines the previous one and at nb = 64 every block has 5 rows, one in each plane y, at 5
  distinct slices. The key of a half vector on block t is its block's row values (5 bits each, rows in increasing
  64 y + z) written at bit offsets 0, 5, 10, ... reduced mod 26 with wrap-around and XORed (a linear fold into 26 bits;
  exact, with no fold, for nb = 64). Equal block contents give equal keys.
- Matching. For each core and block, both key lists are sorted (two radix passes of 13 bits) and merged. Every pair
  (a, b) with equal keys is a match: alpha2 = LA(a) + LB(b), AS = its number of active rows; if AS <= nb - 1 the leaf
  is evaluated in full (w1 = sum of the least weights of alpha2's active rows, w2 = w2(a) + w2(b), choice vector) and
  the least (w1, w2, choice) of the core is kept. A global counter of matches raises CapReached above M_CAP = 2^24 (2.6).
- Certification. After a level over all kept cores in T2's order, let W* be the least w1 found (ties: least w2, then
  the earlier core, then the least choice vector). If W* <= 2 nb - 1, P outputs that leaf and stops; otherwise the next
  level runs. If no level certifies, P outputs nothing (the algorithm fails).

Lemma P (certification gives v14's output). At level nb every leaf with AS(alpha2) <= nb - 1 is found: its nb - 1 or
fewer active rows miss some block, on which LA(a) = LB(b), so the keys agree. Every leaf not found has AS >= nb, so
w1 >= 2 AS >= 2 nb > W* (no nonzero chi5 DDT entry exceeds 8 of 32, so every active row of alpha2 costs at least 2).
Hence W* is the least w1 over all leaves of all kept cores, and every leaf with w1 = W* is found (its AS <= W*/2 < nb),
so the tie-break among them is exact. This is the output of v14's T3 (which visits all 1.38 x 10^12 leaves): the least
(w1, w2), then the earlier core, then the least choice vector.

Native run (mitm2.c, Appendix A; P's T3 on the 467 kept cores exported by the experiment file's T1, T2 and
core_tables). Levels 1, 2, 4, 8, 16, 32 find no leaf with AS <= nb - 1. Level 64 evaluates 30 matches, all on core 17
of T2's order (core No. 349 of T1's list), and certifies W* = 127 <= 127: w2 = 24, choice (0, 0, 3, 0, 0, 0, 0, 0, 3,
1), whose beta2 is BETA2 of Section 3. That is v14's trail (GLL+20 core No. 3), found exactly. Matches per level:
20,490, 40,849, 81,791, 165,085, 329,494, 818,094 and 5,796,132 (7,251,935 in all, 2.31 times below M_CAP). The run
took 370 s on 5 threads (250 CPU-s user, 46 s system, 233 MB). The per-core log (matches and evaluations of every core
at every level) has SHA-256 given in Appendix A; r5.py holds its level-64 column (MT6).

The block layout matters for the cost, not for correctness: an earlier run with contiguous blocks (rows 5t..5t+4 of
one plane, so a block's rows share theta's column effect) produced 1.15 x 10^10 matches at nb = 32 alone and was
stopped. That run and the small comparison that chose the slice stride 13 are charged as development (0.1, D15).

Python form (r5.py): halves, mkey, mitm_core with the M_CAP check in plain sight, and trail_search (T1, T2, then the
levels). It makes exactly the native program's decisions: on core 17 at level 64 and on core 0 at all seven levels it
reproduced the native match and evaluation counts, and the organizer checks it on the output core (r5-count trial 10),
on seed-picked cores (r5-mitm-0, r5-mitm-1) and as P's driver on a sub-problem with its cap (r5-count trials 8, 9).

```python
    M[0] += 1
    if M[0] > mcap:
     raise CapReached()
```

with mcap = M_CAP = 2^24 in algorithm(); CapReached makes algorithm() return without output.

Prices of T3 (bounds, not counted; in units of primitives on 256-bit words):
- a half vector: 2^7 (10 loads, 10 XORs and 10 stores of the 10-word vector, the w2 and Gray updates);
- all keys of one half vector at one level: 2^11 (each of the 320 row fields is extracted once, with a load, a shift
  and a mask, and shifted and XORed into its block's key: at most 6 x 320 = 1,920, plus at most 64 key stores);
- one half vector in one block: 2^6 (two radix passes of 14 primitives each and the merge step, at most 6; with the key extraction 37, V.1; v19: plus per_a, 11, once per (a, block) of half A, 37 + 11 = 48 < 2^6, Section U.1);
- one block of one core at one level: 2^17 (the 2^13-entry count arrays of both halves, cleared and prefix-summed in
  both passes: 4 x 2^13 x 4);
- one match: 2^12 (alpha2: 20 loads and 10 XORs; AS: per word a fold of each 5-bit field into its low bit and a
  shift-and-add count, at most 32 per word, plus the comparison: below 2^9; the full evaluation when AS <= nb - 1:
  w1 over the 320 row fields by table lookup, w2, the lexicographic comparison: below 2^11). (v16: 83 counted below the evaluation; v19: 62 per match plus 11 per (a, block) inside the 2^6 sort-and-merge price, Section U.1.)

P's charge: T1 + T2 + HV x 2^7 + 7 x HV x 2^11 + 127 x HV x 2^6 + 127 x 467 x 2^17 + M_CAP x 2^12 + setup (DDT, L^-1
by elimination, the row-difference vectors of every kept core: below 2^31) = 2^40.43 primitives = 2^30.03 units
(v14: 2^33.65). The level and block counts are fixed by the program (all seven levels are charged although P stops at
the seventh), HV is organizer-recomputed, and the only data-dependent count, the matches, is charged at its cap.

Premise P (inside H1; success only, since every cost term of P is a fixed count or a cap): P outputs the trail of
Section 3 within M_CAP. Its evidence: the native run above, which certifies itself by Lemma P; its agreement with
v14's two exhaustive T3 passes over all 5,679,328,446 batches (same trail, unique); the organizer checks just listed.
If P certified nothing or hit its cap, it would output nothing: the cost bound holds either way.

### 2.2 Advice program B' (budget 2^32 units, at most 2^26 units per candidate; constants no run chose)

B' (experiment file, rand_min_beta1 to bprime) is v6's program with a budget and a per-candidate cap. Its only inputs
are P's trail and the fixed bits F. For candidate c = 0, 1, ... (each abandoned once its own cost exceeds CCAP = 2^26
units; B' then moves to c + 1):
- beta1_c: in each of the 59 rows of alpha2, a uniformly chosen input difference of least weight (50 rows have exactly
  one, 9 have 4 or 5); then the round-1 conditions, the linearisation table and the link and candidate tables.
- attempts j = 0, 1, ... with no limit (B_R = 2^62 in r5.py is never reached): D2u gives the rows of alpha1 =
  L^-1(beta1_c), in DSATUR order, affine sets of compatible differences on which the fixed-bit link conditions are
  uniform, trying candidates in uniformly permuted order sorted by an unweighted key (KW = MW = LB = PREF = 1); M2
  picks, row by row, (d, W) with forward checking on one value system (x, fixed bits, row equations, the 127 round-1
  conditions). An attempt is accepted iff it is consistent with DF >= DMIN = 33 and 64 sampled points pass (both
  messages padded, block difference L^-1(beta0), exact 2-round difference alpha2).
- B' stops at the first accepted attempt and outputs (beta1_c, beta0). A candidate with no accepted attempt ends at
  CCAP.

v13 had R = 16 attempts per candidate, DMIN = 40 and weights (1, 0.25, 1, 1), all chosen by development runs (A2).
v14 replaces them by the values above (0.2), and the R5 study measures the algorithm with them (4.2). Nothing else in
the experiment file's algorithm changes.

Every operation is counted by class: row (one operation on an integer of at most 2585 bits = 11 words: 256
primitives), small (8), Keccak-f call (5 units), SHA-256 compression (2 units), 2-round evaluation (1 unit). The class
WK raises BudgetExceeded on the first counter update that takes B''s cost above B_BUDGET = 2^32 units or the current
candidate's cost above CCAP; so B' spends at most 2^32 units plus one update and a candidate at most 2^26 units plus
one update (the largest update inside B' is below 2^13 units). r5-bpfull executes bprime() whole: from the label of
R5 run 21, 24 or 42 (picked by the seed; these are the R5 runs whose advice came from candidate 0 with B' below
2^23.7 units) its counted cost equals the R5 log and its output the logged advice; and on R5 run 2's label with a
2^22-unit budget and a 2^21-unit candidate cap, candidate 0 stops 0.68 units above 2^21, candidate 1 starts, and B'
stops with no output 188.1 units above 2^22. In R5, 90 of 141 candidates ended at CCAP (with no attempt limit every
candidate that is not accepted ends there) and every run's B' cost, all advice rounds together, was at most 2^28.73
units, so B''s budget never acted.
Coins: fresh 256-bit words in the algorithm (counted as 32
primitives each); in our runs, Coins(SHA-256(label || "beta1" || c)) and Coins(SHA-256(label || "att" || c || j))
(Section 4.1). WK's 2 units per SHA-256 compression is below the 3.3 units of a 64-round compression at the organizer's
sha256-r32 price; a run makes at most 2 compressions per attempt or candidate, and an attempt counts at least 302
units, so our runs' counts are within 0.9% of their true cost. The claimed algorithm draws fresh words and computes no
SHA-256; algorithm(label) in the experiment file derives its coins from a label with SHA-256 and SHAKE-256 only so
that runs can be reproduced, and WK charges those calls. Restart: when an
advice is discarded (2.3), B' resumes at the next candidate under the same budget; the connector's work is charged to
its own term.

### 2.3 Setup S and the connector (unchanged v5 attempt)

S builds L and L^-1 as row forms, alpha2 = L^-1(beta2), alpha1' = L^-1(beta1'), the 127 round-1 conditions (equations
of V(beta1'_r, alpha2_r) on z = L(chi(x) + RC0)), and the linearisation table. One attempt (attempt() in the
experiment file) keeps two echelon systems with undo, E_D on delta (the unknown beta0) and E_M on x, with one shared
counter of work units (a reduction call or a row addition, at most 96 primitives). D1: E_D gets (L^-1 delta)_j = 0 for
j in F, and delta_r = 0 on the inactive rows of alpha1'. D2: in a uniform order of the active rows, the first
uniformly permuted affine set of compatible differences that contains beta0'_r and is consistent. M1: E_M gets the
fixed bits. M2: per row, the first d (beta0'_r first, then by DDT) consistent with E_D and with x_r in V(d,
alpha1'_r). M3: linearise each row with masks on an affine W. M4: add the 127 round-1 conditions. M5: accept iff
consistent and DF = 1600 - rank(E_M) >= 33; above X_MAX = 2^20 work units (2.6; v16, v15: 2^23) the attempt fails. An attempt costs at
most 2^26.86 primitives (2^20 x 96 + 2^15 coin words x 2^9 + 2^22) and draws at most 22,150 coin words.

Advice rounds (v10 caps): run attempts on the current advice until K = 96 are accepted; if A_ADV = 2^11 attempts give
fewer, discard it and resume B' at its next candidate. At most A_MAX = 2^13 attempts in all, so at most 4 advice
rounds.

### 2.4 Enumeration E (stage 1 by bitsliced fast exhaustive search, counted)

Space and window (unchanged): V = solutions of E_M, beta = beta0; offset v0 = the solution with all free variables 0;
b_i = (solution with free variable i set) + v0, kept if independent of beta and the earlier ones; W = span of the first
32 kept b_i. E tests the 2^32 pairs (x, x + beta), x = v0 + sum over the set bits j of the coordinate c of b_j.

Stage 1 tests the 24 round-2 equations (EQS, a basis of the equations of V(beta2_r, alpha3_r) on the 10 rows of beta2,
checked by eqs_ok) on the first message's round-2 input u = L(chi(L(chi(x) + RC0)) + RC1). Let f(c) in GF(2)^24 be the
residual bits (bit k set iff equation k fails). Round 0's output has degree <= 2 in c, round 1's <= 4 and L is linear,
so f has degree <= 4 in c: this is exact, with no assumption.

Layout (v14's): coordinates 0..7 are inner (bit p of a 256-bit word is inner point p); coordinates 8..31 are outer and
run in reflected binary Gray order over 2^24 steps, step i flipping outer coordinate ctz(i). For each equation k, the
word F_k(y) (bit p = f_k at outer point y and inner point p) is a polynomial of degree <= 4 in the 24 outer variables
with 256-bit word coefficients.

Stage 1 is the derivative recursion of fast exhaustive search (Bouillaguet, Chen, Cheng, Chou, Niederhagen, Shamir,
Yang, CHES 2010) on these 24 words at once. State: F (24 words, in registers) and the derivative vectors D1[a], D2[a,b],
D3[a,b,c] (in memory) and the constants D4[a,b,c,d], each a vector of 24 words, indexed by colex ranks. Step i: with
b1 < b2 < b3 < b4 the positions of the lowest (up to four) set bits of i, D3[b1 b2 b3] ^= D4[b1 b2 b3 b4], D2[b1 b2] ^=
D3[b1 b2 b3], D1[b1] ^= D2[b1 b2], F ^= D1[b1], each level only as far as i has set bits. The pass word is NOT(F_0 OR
... OR F_23); its pairs go to stage 2.

Setup (fes_setup in r5.py; fes.c builds the same state, Appendix B): f at the 41,449 coordinates of weight <= 4 (all
32 variables), their Moebius transform (the algebraic normal form of f, exact since deg f <= 4), the 256-bit truth
tables of the inner monomials of every outer monomial, and the initial derivative vectors D_w[K] = (d_K F)(gray(K - 1))
for w < 4 and D4[K] = d_K F (a constant). Bound per space: the 41,449 evaluations at 1 unit each (two rounds and L, the
price of a 2-round evaluation in B''s counter class) plus at most 2^23 primitives (617,089 XORs of the Moebius transform,
at most 41,449 x 24 x 3 for the truth tables, 19,024 vector XORs of at most 72 for the derivatives, ranks), below
2^16 units.

Counted step (fes_step in r5.py; W operators, load(), st() count 1, test() 2). Control, at most 74: the step counter
and its end test (3); up to four lowest set bits of i, each by an isolation (2), a comparison tree over the 24
positions (at most 5 tests, 10) and the position into a register (1), with a clearing (1) after each of the first
three and an end test (2) before each of the last three; the rank arithmetic (a table load and an add per level) and
the shifts to vector offsets (at most 10). Vectors, at most 264: per equation at most 4 loads, 4 XORs and 3 stores.
Test, 26: the OR of the 24 words, its complement (the pass word) and the test. (v18: the steps run as unrolled blocks of 256 at most 75,386 primitives per block, Section V.7; v19: 69,242 with D1[0] in registers, Section U.2; v15's per-step count follows.) The longest path is 364 primitives per
256 pairs (1.42 per pair), counted by r5-count on paths that include four lowest bits at depth-5 positions; every step
is charged at 364 (v14's batch program: 6,112). Registers: the 24 words of F, at most 5 temporaries and the control
values, at most 40 (v19: also the 24 words of D1[0], at most 64, Section U.2).

Stage 2 (unchanged rule): for each pair of the pass word, form x and x + beta (at most 32 basis additions), both
complete 5-round digests (2 units), compare 256 bits and output the pair (bytes 0..134 of L^-1(x) and L^-1(x + beta))
if equal; at most 2 units + 2^11 primitives per pair. At most S2CAP = 2^21 (v16; v15: 2^24) stage-2 pairs per space (2.6; then E stops
on that space); the largest count in the 1,236 spaces of R5 is 308.

Lemma 4 (E is v14's E). For every space, at every outer Gray point, stage 1 computes F_k = the 24 equation words of the
plain evaluation at the 256 inner points: the recursion is an identity for polynomials of degree <= 4 [BCC+10], and
the setup computes the exact ANF. These are the complements of the words of v14's counted e_batch at the same batch
(which marks satisfied equations; both are the plain evaluation). So the pass words, their order (outer Gray order, then inner point), stage 2 and the output are those of
v14's E, and E outputs a pair on a space iff the window holds a colliding pair and the stage-2 cap does not bind.
fes.c (Appendix B) is this stage 1 in native code: it ran every E of R5, C, D (v14) and R6 (Section 4.7), each space
self-checked against direct evaluation of all 256 inner points at 64 checkpoints, all passed. r5-count trials 0, 2, 4,
6 check the counted fes_step against e_plain after every step of a 2^8-point outer window. The Python e_window of the
replays tests the same 2^32 pairs in natural order (Lemma 4 of v14), which changes at most which pair is output.

### 2.5 Main loop and correctness

Run P (trail_search, 2.1; fail on CapReached or if no level certifies). Base S from P's output.
Advice rounds (2.2, 2.3) until K = 96 accepted spaces of one advice, or until B''s budget or A_MAX is
exhausted (then fail). Run E on the K spaces in order and halt with the first output; if there is none, fail.
algorithm() in the experiment file is this driver with every cap (its P is trail_search, its E the plain
evaluation e_window, Lemma 4).
Lemma 1 (outputs are collisions): for x in V, A0 = L^-1(x) satisfies the fixed-bit equations, and so does A0 +
L^-1(beta), since E_D forces (L^-1 beta)_j = 0 on F; beta != 0; E compares the true 256-bit digests. Lemma 2 (used only
for the probability): for x in V the difference after round 1 is alpha2. Lemma 3: beta is not in W, so the 2^32
pairs of a space are distinct.

### 2.6 Caps

(v16, v17) X_MAX = 2^20, S2CAP = 2^21 and B_TRUE = 2^29 units by v13's rule re-anchored at 2^40 primitives (Section V.2). v15's text:


Two counts can only be observed by running and enter the time through a cap: the work units of a connector attempt
(X_MAX = 2^23) and E's stage-2 pairs per space (S2CAP = 2^24). These are v14's values, set in v13 by a rule that used
no run (each the largest power of two whose charged term stays within 2^43 primitives, v14's T3 batch term rounded
down); B''s budget of 2^32 units (chosen in v10 from G2's runs, charged) also satisfies that rule. v15's P no longer has that term; v15 keeps the
values unchanged, so that every run of R5 is also a complete run of v15 (Lemma 6) and no cap is re-chosen after
seeing R5 (in R5 the largest attempt used 189,224 work units and the largest stage-2 count was 308). v14's F_CAP is
gone with v14's T3. P's match counter has the new cap M_CAP = 2^24: the least power of two at least twice the total
of P's native run (7,251,935); that run is charged as development (0.1, D15).

## 3. Exact facts (P's output; recomputed by facts() in every B' and connector experiment)

alpha3 = bits {0, 130, 450, 529, 701, 789, 1021, 1169, 1280, 1429}; nonzero lanes of beta2 in hex 0:1 2:4 5:4 6:4 7:4
8:20000 10:2000000000000000 12:200000 15:2000000000000000 18:20000 20:200001 22:200000 24:1. alpha3 and beta3 =
L(alpha3) are in the CP kernel (10 bits each); beta2 -> alpha3 on the same 10 rows, w2 = 24 (row 66 weight 4, rows 256
and 277 weight 3, the rest 2); alpha2 = L^-1(beta2) has 59 active rows and w1 = 127; C2 = 3^20 for this core. P45 =
sum over the 2^19 alpha4 compatible with beta3 of Pr[beta3 -> alpha4] x prod over nonzero digest-plane rows q of
L(alpha4) of (DDT[q][0] + DDT[q][16])/32 = 55/2^19 = 2^-13.2186 (192 nonzero terms); with w2, p_M = 2^-37.2186 per
pair. Advice facts, for each advice used: beta1' -> alpha2 has weight 127 on the 59 rows; beta0' is compatible with
alpha1' on every row and zero on its inactive rows; alpha0' = L^-1(beta0') is nonzero and zero on F.
v15's P certifies this trail at its level of 64 blocks (2.1; r5-count trial 10 rechecks it on every review).

## 4. Executed evidence (none of it is the claimed cost)

### 4.1 Coins, run selection, premise R, every run made since v11

Coins of our runs. A labelled run uses Coins(SHA-256(label || "beta1" || c)) for B''s candidate c,
Coins(SHA-256(label || "att" || c || j)) for its attempt j, and, for connector attempt i on the advice of candidate c,
seed_i = SHA-256(label || "conn" || (c + 1) as 4 little-endian bytes || i as 8 little-endian bytes) with words
SHAKE-256(seed_i || k) (class Coins). The index map is the algorithm's own: Fisher-Yates index j = (low 64 bits) mod
(i+1). In the claimed algorithm every coin is a fresh uniform 256-bit word; the only difference is SHAKE-256 output in
place of fresh words.

Premise R (stated inside H1): the label-seeded coins act as fresh coins, and the 48 runs of each pre-registered study
(R5, v14's; R6, ours, 4.7) are an unselected sample of the algorithm's runs. Under premise R the 48 success
indicators of a study are independent Bernoulli(p) draws; distinct labels by themselves only give distinct SHAKE-256
streams. Support for R5 (v14's text; R6's is in 4.7):
- The labels "hashsmash sha3-256-r5 R5 run k", k = 0..47, the plan, the driver, the analysis and every file of the
  computation were hashed at 2026-10-07T20:27:28Z, before any run (Appendix D; a first commit at 20:27:03Z was
  replaced before any run, only to change the launcher's start gate; the launch wrapper and the watchdog, which
  compute nothing, were written after the commit and before the launch).
- All 48 runs were started and completed (exit code 0, empty error files); none was stopped, excluded or repeated;
  every result is in the table of 4.3 and the ledger of Appendix D.
- The plan has one outcome-dependent rule: claim 0.40 if the bound is at least 0.40, else nothing from R5. A bound
  computed by a rule fixed in advance keeps its coverage whatever is then done with it: Pr[the claim is made and the
  true success is below it] <= Pr[the bound exceeds the true success] <= 0.05. It has no rule that changes a constant.
- The organizer's seeds pick which logged successes r5-R-0..7 replay and which earlier attempts are re-run; a
  holdout nonce changes them. They do not enter any bound.

Every run made since v11 (2026-10-07; times UTC; v14's list). In v14 only R5 entered the bound; in v15 R6 and R5 do.
C and G2's runs are charged (0.1); the rest are listed so that nothing is selected away.
- Pre-registration C (16:57:43Z-17:16:03Z, 48 runs), its smoke-test run 999 (16:55:34Z) and pre-registration D
  (17:53:22Z-17:58:42Z, 31 runs): v13's evidence for v13's tuned B' (4.4). C is charged.
- C' (a parallel session of ours): plan prereg/plan.md hashed at 16:58:33Z (SHA-256
  7fde45cf25f6555cab68dfef679adce25cd5fad6ab64cdc9ca4a2cb6da063b8b), which states "B' constants of v11, fixed by
  rule with no run: no attempt limit per candidate ..., DMIN = 33 ..., D2u ordering unweighted (all weights 1)",
  os.urandom seeds and a native E. 14 runs started 16:58:42Z-17:14:54Z; 4 finished (its runs 2, 5, 7, 9), each with a
  collision (at its spaces 2, 3, 11 and 4); the other 10 were left unfinished when it was abandoned at 17:18Z
  (prereg/runs.jsonl, SHA-256 2f63dd3bae4e21cbd736529cd3fbfcb7fd469dfba1bd92825b3e8d97236eecd3). Before it, the same
  session made 3 test runs of the variant from 16:52:22Z (test_log.jsonl, SHA-256
  38093c7f3809938e984eb15d164a1e7106ef27b7b33f5aba71d0320c666f4d9f) whose native E was not a working form of E
  (0.05-0.11 round-2 passes per space against about 256 expected); none had an output. C' chose no constant (its plan
  predates its runs) and enters no bound; R5's plan names it.
- Runs made for v13 (after 20:00Z): local organizer-experiment runs and a certificate check, no new outcome.
- The R5 study: 48 runs, 20:45:12Z-21:23:48Z (4.2). Before its plan, its driver was run once, as a self-test that
  re-derived v11 pre-registration C's run 5 positive space with v11's constants (no R5 outcome).
- Runs made for v14 (2026-10-07T21:43Z-22:20Z), all re-derivations of logged R5 runs with no new outcome: a replay
  of all 48 runs with the experiment file's code (each advice re-derived from its label with the logged DF and hash;
  connector attempts 0..i re-run with the logged status, DF and work count; 46 collisions re-found at the logged
  coordinates; for runs 6 and 31 all attempts up to the 96th acceptance); whole B' runs of the 15 R5 runs whose
  advice came from candidate 0 (each with the logged cost and advice); timing and memory measurements of the
  replays; local organizer-experiment runs (4.6).

Every run made for v15 (2026-10-08; times UTC):
- D15 (charged, 0.1): the first native T3 run with contiguous blocks (stopped in its tenth level); the comparison of
  six block layouts on 8 cores; the certified native run of P (2.1, Appendix A); count-only recounts of the stopped
  runs' match totals (used only to charge them); Python re-runs of T3 on single cores for the checks of 2.1;
  development and checks of the counted stage 1; the driver's self-test (a replay of R5 run 4 that reproduced R5's
  logged advice and collision).
- R6 (Section 4.7): plan and code hashed at 00:19:33Z, 48 runs started from 00:19:45Z, all reported.
- Local organizer-experiment runs (4.6) and the certificate check: re-derivations, no new outcome. (v19: every run made for v19, with hashes, is in Section U.5.)

### 4.2 The R5 study (48 complete runs of v14's algorithm)

Plan (Appendix D, verbatim; plan.txt, SHA-256 7ffaf34f4001a449a6775fa3f204f7c93a0be60c69e45588d320aae1d382574b),
hashed at 2026-10-07T20:27:28Z with the driver r5run.py, the experiment file (r5v13.py, byte-identical to v13's
experiments/r5.py), the analysis analyze.py, the launchers, the enumerator fes (the binary of C, Appendix B) and its
libraries (commit.txt, Appendix D). R5 is algorithm() of that file with B''s three settings replaced by the values of
2.2 (r5run.py sets them before the run: B_R = 2^62, B_DMIN = 33, KW = MW = LB = PREF = 1); this is v14's experiment
file, whose algorithm differs from v13's only in these constants. Per run, as algorithm() does it: B' with its budget
and candidate cap from candidate 0, the connector rule (attempts until 96 accepted, or discard the advice after 2^11
attempts and resume B'), then E on the accepted spaces in order up to the first output, with fes (exact over the
2^32 window, self-check against direct evaluation at 64 points) and stage 2 by complete 5-round digests on at most
S2CAP pairs. P's output is the trail of Section 3 (premise P). Launch: at 20:38:41Z; a run started only when fewer
than 11 processes were busy and the 1-minute load average was below 12, at most 10 runs at a time, nice 10. A
watchdog written before the launch (watchdog.py, SHA-256
c0f03d92bf1f653c4268ebd06721189666d647e99ff74d7c1085e6b6df186b4d; it pauses and resumes our processes to keep the
machine at 12 or fewer busy processes, which cannot change a deterministic run's result) paused two runs for 10 s
each (watchdog.log). The first run started at 20:45:12Z and the last ended at 21:23:48Z; all 48 exit codes are 0
and all error files are empty. Python CPU time 12,150 s in all (plus fes).

Results (every run; table of 4.3; ledger in Appendix D):
- 46 of 48 runs output a collision; runs 6 and 31 had none in their 96 spaces. Every collision was verified by
  complete digests, and again by our replay with the experiment file (4.1).
- B': 141 candidates; 51 accepted (DF 33-76), 90 ended at CCAP; B' cost per run 2^23.19 to 2^28.73 units.
- Connector: 51 advice rounds, 15,323 attempts, 4,674 accepted (0.305); 96 accepted within 96-557 attempts on every
  kept advice. Runs 9, 17 and 47 discarded their first advice at A_ADV (65, 0 and 1 accepted in 2,048 attempts), and
  B' resumed at the next candidate, as the algorithm does. Largest attempt 189,224 work units (X_MAX = 2^23).
- E: 1,236 spaces enumerated, all self-checks passed, round-2 passes per space 200-308 (mean 255.75; 2^32 x 2^-24 =
  256 expected); the stage-2 cap never bound. First positive space at index 1-89.
- Analysis (analyze.py, fixed in the plan): 46 of 48, one-sided 95% Clopper-Pearson lower bound 0.8746; claim rule:
  0.40 (analysis.json, SHA-256 25e283c8b53d9725830e263daf9fa69c433859b47f30b7a9e1dcb7d95a96d2b3).

### 4.3 Per-run table of the R5 study

From the result files ("attempts", "accepted": connector attempts and acceptances per advice round; "spaces": E's
spaces enumerated up to the first output; B' log2 units over all rounds of the run):

| k | candidates | (c, j) per round | DF | B' log2 units | attempts | accepted | spaces | first positive space | success |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0, 25 | 46 | 24.74 | 128 | 96 | 14 | 14 | yes |
| 1 | 4 | 3, 17 | 45 | 27.78 | 238 | 96 | 75 | 75 | yes |
| 2 | 3 | 2, 41 | 40 | 27.47 | 96 | 96 | 44 | 44 | yes |
| 3 | 7 | 6, 12 | 37 | 28.67 | 441 | 96 | 22 | 22 | yes |
| 4 | 4 | 3, 37 | 41 | 27.92 | 96 | 96 | 1 | 1 | yes |
| 5 | 7 | 6, 23 | 44 | 28.72 | 122 | 96 | 27 | 27 | yes |
| 6 | 4 | 3, 22 | 52 | 27.79 | 452 | 96 | 96 | none in 96 | no |
| 7 | 3 | 2, 19 | 46 | 27.31 | 557 | 96 | 5 | 5 | yes |
| 8 | 2 | 1, 46 | 42 | 26.88 | 110 | 96 | 8 | 8 | yes |
| 9 | 4 | 0, 18; 3, 37 | 38, 37 | 27.69 | 2048 + 239 | 65 + 96 | 26 | 26 | yes |
| 10 | 4 | 3, 24 | 35 | 27.85 | 176 | 96 | 1 | 1 | yes |
| 11 | 3 | 2, 11 | 40 | 27.19 | 425 | 96 | 25 | 25 | yes |
| 12 | 3 | 2, 1 | 38 | 27.08 | 173 | 96 | 42 | 42 | yes |
| 13 | 1 | 0, 30 | 51 | 25.03 | 145 | 96 | 29 | 29 | yes |
| 14 | 4 | 3, 16 | 45 | 27.76 | 191 | 96 | 7 | 7 | yes |
| 15 | 5 | 4, 6 | 51 | 28.15 | 124 | 96 | 12 | 12 | yes |
| 16 | 1 | 0, 16 | 59 | 24.55 | 137 | 96 | 18 | 18 | yes |
| 17 | 3 | 0, 29; 2, 11 | 33, 34 | 27.33 | 2048 + 260 | 0 + 96 | 6 | 6 | yes |
| 18 | 7 | 6, 9 | 51 | 28.66 | 96 | 96 | 62 | 62 | yes |
| 19 | 4 | 3, 6 | 67 | 27.70 | 153 | 96 | 48 | 48 | yes |
| 20 | 1 | 0, 42 | 44 | 25.63 | 138 | 96 | 1 | 1 | yes |
| 21 | 1 | 0, 3 | 49 | 23.51 | 206 | 96 | 1 | 1 | yes |
| 22 | 5 | 4, 10 | 47 | 28.12 | 419 | 96 | 20 | 20 | yes |
| 23 | 3 | 2, 4 | 36 | 27.14 | 120 | 96 | 8 | 8 | yes |
| 24 | 1 | 0, 2 | 38 | 23.20 | 215 | 96 | 10 | 10 | yes |
| 25 | 1 | 0, 5 | 50 | 23.67 | 147 | 96 | 27 | 27 | yes |
| 26 | 4 | 3, 22 | 76 | 27.79 | 339 | 96 | 22 | 22 | yes |
| 27 | 2 | 1, 29 | 35 | 26.91 | 154 | 96 | 5 | 5 | yes |
| 28 | 2 | 1, 21 | 47 | 26.62 | 195 | 96 | 13 | 13 | yes |
| 29 | 1 | 0, 18 | 38 | 24.84 | 142 | 96 | 86 | 86 | yes |
| 30 | 2 | 1, 2 | 51 | 26.16 | 122 | 96 | 14 | 14 | yes |
| 31 | 1 | 0, 18 | 40 | 25.52 | 181 | 96 | 96 | none in 96 | no |
| 32 | 3 | 2, 49 | 59 | 27.49 | 113 | 96 | 69 | 69 | yes |
| 33 | 4 | 3, 0 | 33 | 27.63 | 96 | 96 | 89 | 89 | yes |
| 34 | 1 | 0, 9 | 39 | 24.59 | 121 | 96 | 17 | 17 | yes |
| 35 | 2 | 1, 17 | 50 | 26.52 | 119 | 96 | 18 | 18 | yes |
| 36 | 2 | 1, 8 | 42 | 26.36 | 96 | 96 | 10 | 10 | yes |
| 37 | 1 | 0, 10 | 49 | 24.06 | 115 | 96 | 53 | 53 | yes |
| 38 | 2 | 1, 19 | 54 | 26.64 | 136 | 96 | 10 | 10 | yes |
| 39 | 1 | 0, 7 | 40 | 23.83 | 242 | 96 | 18 | 18 | yes |
| 40 | 6 | 5, 60 | 59 | 28.58 | 200 | 96 | 34 | 34 | yes |
| 41 | 1 | 0, 46 | 46 | 25.80 | 349 | 96 | 1 | 1 | yes |
| 42 | 1 | 0, 3 | 41 | 23.21 | 191 | 96 | 2 | 2 | yes |
| 43 | 1 | 0, 4 | 35 | 23.60 | 96 | 96 | 13 | 13 | yes |
| 44 | 5 | 4, 2 | 53 | 28.05 | 117 | 96 | 1 | 1 | yes |
| 45 | 2 | 1, 28 | 37 | 26.75 | 182 | 96 | 1 | 1 | yes |
| 46 | 5 | 4, 25 | 38 | 28.16 | 96 | 96 | 23 | 23 | yes |
| 47 | 6 | 4, 2; 5, 18 | 34, 57 | 28.22 | 2048 + 173 | 1 + 96 | 6 | 6 | yes |

### 4.4 Earlier runs: pre-registrations C and D, G2's runs

Pre-registrations C and D measured v13's algorithm (tuned B': R = 16, DMIN = 40, weights 1, 0.25, 1, 1) on 48
pre-registered runs: C (plan prereg_c/plan.txt, SHA-256 4e1edbd45e4b0dfb10de7a67f432805e30d54eef073caba197d26ace7142b666,
hashed with its driver, analysis and enumerator at 16:55:25Z) ran B', the connector rule and E on the first 16 spaces
of runs k = 0..47 (16:57:43Z-17:16:03Z; 328 candidates, 48 advices, 768 spaces, 23 positive in 18 runs); D (plan
3a3bc8119b38b5eaa969a4a803db9b0c9d59c08b363ebaecc88816aeb21ba46c, hashed at 17:53:16Z) completed the other 30 runs and
run 999 (818 spaces). 46 of 48 succeeded (47 of 49 with run 999), the same count as R5. Both plans are in Appendix C.
C's rule would have raised K had its bound been below 0.40, so C is charged (0.1): its 48 B' runs at their exact WK
counts (8,469,642,639,781 primitives), its 9,097 connector attempts at their 2^18 cap, 48 x S and 768 spaces at the
counted E, 2^35.9149 units. D fixed no number. Neither enters Section 5.

G2 (charged, 0.1): the v6 run (one advice, 14 positive spaces in the first 512 accepted) and pre-registrations A
(nine B' runs under v8's program, 65 candidates) and B (18 spaces of A's advices). v10 chose K, CCAP, B_BUDGET,
A_ADV and A_MAX from them. None enters Section 5.

### 4.5 Certificates

16 certificates (distinct 135-byte messages, equal complete 5-round digests), the most intake accepts: r5-v6-000038,
whose first message r5-count uses; R5's collisions of runs 0-5, 7 and 35 (run 35's replay exceeds the experiment
sandbox's memory); and the collisions of the first seven successful R6 runs in k order (k = 1, k = 2, k = 3, k = 4, k = 5, k = 6, k = 7), id
r6-R6-k<k>-<coordinate>. Each is that run's logged output. v14's certificates of R5 runs 8-14 are not repeated (their
runs are in the r5-R replay strata).

### 4.6 Organizer experiments

r5.py holds the reference algorithm and all experiments (one file, 62,095 bytes; the organizer's limit is 16
experiments and 64 KiB of source). r5-R-* return real collisions. The other experiments check programs and counts and
return sentinels: PASS (00^135, 01 || 00^134), FAIL (00^135, 02 || 00^134).

| id | trials | PASS means | local result (public seed; nonces v15-nonce-1, v15-nonce-2) |
| --- | --- | --- | --- |
| r5-trail-0..3 | 1 each | P's structural counts of the group (T1 nodes per lane; cores, C1, P45 > 0, C2, half vectors HV) equal the log | 4 of 4 on every seed |
| r5-count | 11 | counted E stage 1 (fes_setup, fes_step) against e_plain at every step of a 2^8-point outer window and its longest path 364 (v18: two unrolled blocks, V.7; trials 0, 2, 4, 6); T2's counted leaf (1, 3, 5, 7; v19: the bitsliced leaf on all 32 row values, then 64 leaves, at most 56, U.3; v19's stage-1 counts per U.2); P's driver on the sub-problem [core 874, core 1136] with all levels (8) and its cap (9); T3's certifying level on the output core: 49,060 matches, 30 evaluations, the trail of Section 3 (10) | 11 of 11 on every seed |
| r5-mitm-1 (v16 additions) | 3 | as r5-mitm-0 (0); the counted half-vector step over both half tables of the output core (1) and the counted match step on 4 seed-picked level-64 blocks of it (2), proof V.1 (v19: per_a exactly 11 and match_step exactly 62, U.1) | 3 of 3 on our seeds (about 6 CPU-s) |
| r5-mitm-0, r5-mitm-1 | 1 each | T3's level of 64 blocks on a seed-picked kept core (re-derived by T1 from its lane and the mask LANEM): match count = the native log MT6, no evaluation | 2 of 2 on every seed |
| r5-bpfull | 3, then 24 connector attempts | v14's: whole B' of a seed-picked R5 run from its label (logged cost and advice), both B' caps acting, the R5 table's 46 of 48 and its bound, attempts with organizer coins accepted and verified | 3 of 3 on every seed; attempts accepted and verified: 7, 6 and 12 of 24 (descriptive) |
| r5-R-0..7 | 2 each | v14's replay of two seed-picked R5 successes of the stratum (the 45 successes other than run 35, position mod 8): advice re-derived from the label, logged connector statuses re-run, E's 2^12-coordinate window returns the logged collision | 16 full collisions on every seed |

Over a review the seeds re-derive 16 of the 45 replayable successes (v14: 20 with 10 strata; the organizer's limit of
16 experiments made room for r5-mitm-0, 1 by merging v14's 10 strata into 8); any logged success that is not an output
of the algorithm at its logged place would be caught with probability at least 1/3 for that run (2 picks among at most
6), and the certificates are checked by intake. r5-mitm-0, 1 audit 2 of the 467 per-core match counts per review
(each wrong count caught with probability about 2/467 per review); the output core, whose count and trail matter for
the certification, is checked on every review (r5-count trial 10).

Local runs (our check, not organizer evidence): experiments/runner.py with Python 3.12 in place of Docker (the same
request and environment; each experiment executed twice with byte-identical output, as the runner requires), on the
public seed and on the nonces "v15-nonce-1" and "v15-nonce-2", written down before the runs. All 16 experiments passed on all three seeds. (v19: v19's experiment file passed all 16 on the public seed, Section U.5.) Per experiment at most 11.8 CPU-s, 13.2 s wall and 93 MB on our machine, which was shared with other work; v14's own experiments (r5-bpfull, r5-R-*) take 6.4 to 11.8 CPU-s here, against at most 5.7 CPU-s that v14 reported for its machine, and ours are r5-count 10.8, r5-trail 4.3 to 8.6, r5-mitm 1.9 to 3.2.

### 4.7 The R6 study (ours: 48 complete runs of v15's algorithm)

Plan (Appendix E, verbatim; plan.txt, SHA-256 9c7659c3acf661348f3d8e031cb28bb16bc309614f0a9763cdb9a2e4c22e5e7c),
hashed at 2026-10-08T00:19:33Z with the driver r6run.py, the experiment file r5v14.py (byte-identical to v14's
experiments/r5.py, whose B', S, connector and driver v15 keeps unchanged), fes.c and the binary fes, P's native T3
mitm2.c, the analysis analyze.py, the launcher run_all.py and the organizer verifier's keccak.py (commit.txt, Appendix
E). All files were made read-only at the commit. Labels "hashsmash sha3-256-r5 R6 run k", k = 0..47; coins derived from
the label exactly as algorithm(label) does. Before the plan, the driver was run once as a self-test on the label of R5
run 4; it reproduced R5's logged advice and collision (no R6 outcome; charged in D15). The launcher started run 0 at
00:19:45Z, at most 5 runs at a time with nice 10, and the last run ended at 2026-10-08T02:10:55Z. All 48 exit codes are 0 and all error files are empty. Python CPU time
18,994 s in all, plus 2,493 s in fes. Premise R for R6: the labels, plan and every file of the computation were
hashed and made read-only before any run; every run is reported (table below, Appendix E); the plan's only
outcome-dependent rule is whether to claim, which keeps the bound's coverage; no constant was changed after any run.

Results (every run; table below; ledger in Appendix E):
- 44 of 48 runs output a collision; runs 0, 29, 30, 45 had no output in their 96 spaces. Every collision was verified by the analysis with the experiment
  file's digest and with the organizer verifier (sha3_256(m, 5)).
- B': 162 candidates in all; B' cost per run 2^22.62 to 2^29.61 units (budget 2^32).
- Connector: 58 advice rounds, 33,131 attempts, 4,844 accepted; run 10 discarded an advice with 1 accepted in 2,048 attempts; run 11 discarded an advice with 53 accepted in 2,048 attempts; run 12 discarded an advice with 0 accepted in 2,048 attempts; run 18 discarded an advice with 66 accepted in 2,048 attempts; run 23 discarded an advice with 1 accepted in 2,048 attempts; run 27 discarded an advice with 64 accepted in 2,048 attempts; run 33 discarded an advice with 2 accepted in 2,048 attempts; run 34 discarded an advice with 46 accepted in 2,048 attempts; run 34 discarded an advice with 0 accepted in 2,048 attempts; run 45 discarded an advice with 3 accepted in 2,048 attempts. Largest attempt 190,240 work units
  (X_MAX = 2^23).
- E: 1,408 spaces enumerated, all self-checks passed; round-2 passes per space 210-315 (256 expected); the
  stage-2 cap never bound. First positive space at index 1-78.
- Analysis (analyze.py, fixed in the plan): 44 of 48, one-sided 95% Clopper-Pearson lower bound 0.8193; claim rule:
  0.40 is supported (analysis.json, SHA-256 35c979811047ee5fea6d2759d6abce254f68e72b95f4fbe5ba138cba9a15d162).

Per-run table (from the result files; "attempts", "accepted": connector attempts and acceptances per advice round;
"spaces": E's spaces enumerated up to the first output; B' log2 units over all rounds):

| k | candidates | (c, j) per round | DF | B' log2 units | attempts | accepted | spaces | first positive space | success |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 4 | 3, 26 | 35 | 27.91 | 394 | 96 | 96 | none in 96 | no (none-in-K) |
| 1 | 1 | 0, 2 | 44 | 23.48 | 187 | 96 | 9 | 9 | yes |
| 2 | 5 | 4, 0 | 46 | 28.04 | 148 | 96 | 12 | 12 | yes |
| 3 | 1 | 0, 1 | 55 | 23.15 | 148 | 96 | 19 | 19 | yes |
| 4 | 1 | 0, 0 | 34 | 22.62 | 178 | 96 | 4 | 4 | yes |
| 5 | 1 | 0, 22 | 45 | 25.68 | 135 | 96 | 22 | 22 | yes |
| 6 | 6 | 5, 27 | 40 | 28.53 | 96 | 96 | 10 | 10 | yes |
| 7 | 2 | 1, 45 | 40 | 26.89 | 113 | 96 | 1 | 1 | yes |
| 8 | 2 | 1, 14 | 42 | 26.43 | 111 | 96 | 14 | 14 | yes |
| 9 | 3 | 2, 1 | 38 | 27.08 | 123 | 96 | 14 | 14 | yes |
| 10 | 3 | 0, 12; 2, 26 | 34, 48 | 26.98 | 2048 + 315 | 1 + 96 | 34 | 34 | yes |
| 11 | 6 | 3, 8; 5, 4 | 34, 40 | 28.20 | 2048 + 207 | 53 + 96 | 10 | 10 | yes |
| 12 | 3 | 0, 33; 2, 8 | 33, 33 | 26.97 | 2048 + 359 | 0 + 96 | 49 | 49 | yes |
| 13 | 2 | 1, 7 | 37 | 26.35 | 128 | 96 | 37 | 37 | yes |
| 14 | 4 | 3, 19 | 39 | 27.77 | 304 | 96 | 34 | 34 | yes |
| 15 | 2 | 1, 9 | 41 | 26.52 | 176 | 96 | 60 | 60 | yes |
| 16 | 1 | 0, 23 | 55 | 24.79 | 263 | 96 | 37 | 37 | yes |
| 17 | 1 | 0, 5 | 34 | 24.22 | 412 | 96 | 7 | 7 | yes |
| 18 | 3 | 1, 27; 2, 14 | 35, 45 | 27.20 | 2048 + 139 | 66 + 96 | 14 | 14 | yes |
| 19 | 3 | 2, 21 | 42 | 27.36 | 96 | 96 | 8 | 8 | yes |
| 20 | 1 | 0, 55 | 51 | 25.77 | 204 | 96 | 15 | 15 | yes |
| 21 | 6 | 5, 4 | 36 | 28.39 | 329 | 96 | 11 | 11 | yes |
| 22 | 4 | 3, 4 | 33 | 27.69 | 911 | 96 | 2 | 2 | yes |
| 23 | 13 | 10, 10; 12, 31 | 34, 41 | 29.61 | 2048 + 139 | 1 + 96 | 32 | 32 | yes |
| 24 | 4 | 3, 13 | 42 | 27.75 | 144 | 96 | 20 | 20 | yes |
| 25 | 1 | 0, 0 | 42 | 23.02 | 484 | 96 | 30 | 30 | yes |
| 26 | 3 | 2, 23 | 33 | 27.36 | 1221 | 96 | 4 | 4 | yes |
| 27 | 7 | 3, 1; 6, 6 | 39, 41 | 28.44 | 2048 + 124 | 64 + 96 | 45 | 45 | yes |
| 28 | 9 | 8, 9 | 45 | 29.05 | 347 | 96 | 9 | 9 | yes |
| 29 | 3 | 2, 45 | 50 | 27.42 | 163 | 96 | 96 | none in 96 | no (none-in-K) |
| 30 | 2 | 1, 33 | 58 | 26.73 | 471 | 96 | 96 | none in 96 | no (none-in-K) |
| 31 | 1 | 0, 11 | 35 | 25.04 | 677 | 96 | 1 | 1 | yes |
| 32 | 2 | 1, 0 | 39 | 26.15 | 112 | 96 | 5 | 5 | yes |
| 33 | 7 | 1, 4; 6, 2 | 36, 33 | 28.42 | 2048 + 897 | 2 + 96 | 78 | 78 | yes |
| 34 | 8 | 2, 13; 4, 1; 7, 5 | 34, 33, 60 | 28.49 | 2048 + 2048 + 96 | 46 + 0 + 96 | 53 | 53 | yes |
| 35 | 2 | 1, 27 | 39 | 26.73 | 96 | 96 | 23 | 23 | yes |
| 36 | 6 | 5, 4 | 62 | 28.37 | 113 | 96 | 46 | 46 | yes |
| 37 | 4 | 3, 2 | 40 | 27.67 | 158 | 96 | 9 | 9 | yes |
| 38 | 2 | 1, 5 | 44 | 26.25 | 263 | 96 | 74 | 74 | yes |
| 39 | 1 | 0, 2 | 35 | 23.34 | 120 | 96 | 11 | 11 | yes |
| 40 | 1 | 0, 25 | 38 | 25.46 | 188 | 96 | 19 | 19 | yes |
| 41 | 4 | 3, 7 | 39 | 27.79 | 96 | 96 | 4 | 4 | yes |
| 42 | 6 | 5, 9 | 33 | 28.39 | 448 | 96 | 32 | 32 | yes |
| 43 | 1 | 0, 10 | 43 | 24.21 | 96 | 96 | 49 | 49 | yes |
| 44 | 2 | 1, 7 | 44 | 26.30 | 174 | 96 | 18 | 18 | yes |
| 45 | 4 | 0, 17; 3, 10 | 33, 50 | 27.54 | 2048 + 222 | 3 + 96 | 96 | none in 96 | no (none-in-K) |
| 46 | 2 | 1, 32 | 46 | 26.66 | 118 | 96 | 32 | 32 | yes |
| 47 | 2 | 1, 9 | 37 | 26.41 | 208 | 96 | 7 | 7 | yes |

## 5. Success probability (end to end, over the algorithm's own coins)

The probability space is the algorithm's coins: B' candidate coins and connector coins. The target is fixed, and P
and E are deterministic. A run of the algorithm is therefore a function of its coins, and p = Pr[the algorithm
outputs a collision].

Lemma 6 (complete runs; v17). (c) Each R5 and R6 run is also a complete run of v17: v17 differs from v15 only in the B' true-cost tally and its budget B_TRUE = 2^29 units, which no R5 or R6 run reached (largest true B' cost 2^28.2709 units, Section V.5; WK's counter and caps act as in v15), in the programs that compute P's T3 (same keys, matches, decisions and output: r5-mitm-1 trials 1, 2), whose output is a constant of every run, and in the caps X_MAX = 2^20 and S2CAP = 2^21, which no R5 or R6 run reached (largest attempt 190,240 work units, largest stage-2 count 315). An attempt or a space that stays below a cap behaves identically under either cap, so each run's output is v16's. (v18, v19) v18's unrolled E blocks (V.7: the same stage-1 words in the same Gray order, Lemma 4) and v19's three program changes (U.1: the same AS, decisions and match counts, CapReached at the same (a, block) run, so the same output of P; U.2: the same stage-1 words in the same order; U.3: the same leaf decisions, so the same 467 kept cores) compute the same values in the same order, with the same caps, constants and rules; so each R5 and R6 run is also a complete run of v18 and of v19, with the same output (r5-count trials 0-7 and r5-mitm-1 trial 2 check each change against the plain evaluation). Parts (a) and (b) are v15's:

Lemma 6 (complete runs). (a) Each R6 run is v15's algorithm executed with label-derived coins: r6run.py makes
algorithm()'s calls in algorithm()'s order (bprime, Setup, attempt, E per space) from the code of v14's experiment
file, whose B', S, connector and driver v15 keeps byte for byte; P's output is the certified trail (2.1); E on a space
is fes (v15's stage 1, Lemma 4) and stage 2 by complete digests in fes's order with at most S2CAP pairs. In R6 B''s budget never acted (at most 2^29.61 units per run), no attempt reached X_MAX (largest 190,240 work units), A_MAX never acted (at most 4192 attempts in a run), every fes self-check passed and the stage-2 cap never bound (at most 315 pairs).
(b) Each R5 run is also a complete run of v15: v14's Lemma 6 shows it is a complete run of v14's algorithm, and v15
differs from v14 only in P and E's stage 1, which compute v14's outputs (Lemma P, Lemma 4), and in the caps F_CAP
(gone) and M_CAP (P's native run stays 2.31 times below it); P's output is a constant of every run. So R5's success
indicators are v15's.

Heuristics (claim.json):
- H1-end-to-end-success: p >= 0.40, under premise R (the label-seeded coins act as fresh coins, and the runs of the
  pre-registered studies are unselected samples of the algorithm's runs) and premise P (2.1). Support: R6, our
  pre-registration (Section 4.7, Appendix E): 44 of 48 runs succeed, one-sided 95% Clopper-Pearson lower bound
  0.8193; by its plan's rule this supports the claim 0.40. R5 (v14's pre-registration, 4.2): 46 of 48, bound 0.8746.
  The two studies are not pooled for the bound; each alone supports 0.40.
- H2-development-ledger: the charged development (G2 and C at v15's prices, and D15) contains every target-specific
  run whose result fixed, or under its plan could have changed, a number that v15's algorithm reads (0.1, 0.2). (v19: G2, C, D15 with the T1/T2 export, D16 and D19, at the counted prices of v19's programs, Sections U.4, U.5, U.8.)

So Pr[success] >= 0.40 with confidence at least 95% under either study. Every cap of Section 6 holds without H1.

Consistency (descriptive; no bound uses it): R6 found 44 positive spaces in 1,408 enumerated spaces (0.031 per
space; E stops at the first output); R5 found 46 in 1,236 (0.037); the trail predicts 0.0265 (1 - exp(-256 x
2^-13.2186)), and a run succeeds with probability 0.924 at that rate.

## 6. Time (collision-frontier-v5: one 5-round permutation = 1 unit, other primitives 1/1355)

| Term | Cap, enforced by | Count and price | log2 units |
| --- | --- | --- | --- |
| P: T1 | exact count N1 (organizer-recomputed) | 8,674,833 nodes x 2^12 (bound per node, as in v8) | 24.6443 |
| P: T2 (v19) | exact count C1 (organizer-recomputed) | 1,639,088,128 leaves x 56 (counted, U.3; v18: 166) | 26.0135 (v18: 27.5812) |
| P: T3 half vectors (v16) | exact count HV (organizer-recomputed) | 48,592,224 x 96 (counted hv_step, all 127 keys included) | 21.7151 |
| P: T3 keys (v16) | inside hv_step | 0 (v15: 7 x HV x 2^11, 28.9375) | - |
| P: T3 sort and merge | 127 blocks over the levels (fixed) | 127 x HV x 2^6 (bound) | 28.1188 |
| P: T3 block setup | 127 blocks x 467 cores (fixed) | 127 x 467 x 2^17 (bound) | 22.4519 |
| P: T3 matches (v19) | M_CAP = 2^24 (2.6) | 2^24 x (62 counted, U.1 + 2^11 evaluation bound); per (a, block) 11 inside the sort-and-merge bound | 24.6390 (v18: 24.6532) |
| P: setup (v16) | | 2^32 primitives (bound; includes hv_step's tables) | 21.5959 |
| B' (v17) | true-cost budget B_TRUE (V.5), re-checked on every update; WK's B_BUDGET and CCAP as v15 | 2^29 units + one update (< 2^13 units) | 29.0000 (v15: 32.0000) |
| S | at most 4 advice rounds | 4 x 2^31 primitives | 22.5959 |
| Connector (v16) | X_MAX = 2^20 work units per attempt, A_MAX = 2^13 attempts | 2^13 x (2^20 x 96 + 2^15 x 2^9 + 2^22) primitives | 29.4539 |
| Bases | K = 96 spaces | 96 x 2^24 primitives | 20.1809 |
| E setup | K = 96 spaces | 96 x 2^16 units (bound: 41,449 evaluations at 1 unit + 2^23 primitives) | 22.5850 |
| E stage 1 (v19) | 2^16 blocks of 256 steps per space | 96 x 2^16 x 69,242 primitives (counted per block, U.2; v18: 75,386) | 28.2602 (v18: 28.3829; v15: 28.6887) |
| E stage 2 (v16) | S2CAP = 2^21 per space | 96 x 2^21 x (2 units + 2^11 primitives) | 29.3970 |
| Output | one pair | 2^22 primitives | 11.5959 |
| Algorithm (v19) | | | 31.3507 (v18: 31.4335; v15: 33.9407) |
| Development G2 (v14's; v6 run, pre-registrations A and B) (v17) | exact counters and caps (0.1) | counted prices of the submitted programs; B' at its true cost (V.5); E at v19's E (U.2) | 30.9994 (v18: 31.1003; v15: 31.8877) |
| Development C (v14's pre-registration C) (v17) | exact counters and caps (0.1) | counted prices of the submitted programs; B' at its true cost (V.5); E at v19's E (U.2) | 31.9189 (v18: 31.9977; v15: 33.2426) |
| Development D15 (v15's) | counts of v15's runs (0.1) | v19: at v19's counted prices, with the T1/T2 export of U.4; v17: at v17's counted T3 prices (Section V.3); v15: P's bounds of 2.1 | 32.0899 (v18: 32.3521; v15: 34.6617) |
| Development D16 (v16/v17) and D19 (v19) | D16: v17's runs (Section V.3); D19: every run made for v19 except the organizer's harness (U.5) | D16 stated bound; D19 counted prices and stated bounds | D16 27.0000; D19 28.9135 |
| Total T (v19) | | | 33.7207 -> 33.7208 (v18: 33.8145 -> 33.82; v15: 35.7504 -> 35.76) |

Every term of the algorithm is a cap, a fixed count or an organizer-recomputed count, times a counted longest path
or a stated bound; no expected value is used, and no count taken only from our runs enters except through a cap
(M_CAP). Preprocessing (P + B' + S + development) = 2^35.4430, claimed 35.45 (v19: 2^33.5279, claimed 33.53). The exact sums are in rationals (the
script that produced this table reproduces v14's 2^35.0558 and 2^37.0488 from v14's terms).

Sensitivity (not the claim): every bound of T3 four times larger: 35.82; the E setup bound four times larger: 35.76;
E stage 1 at 2 x 364: 35.77; G2 and C at v14's prices: 37.13; D15 doubled: 36.31; D15 omitted: 34.83.

## 7. Memory

P: per core, the two half tables (at most 2 x 9^5 vectors of 320 bytes, 38 MB, plus keys and indices); the native run
peaked at 233 MB with 5 cores in flight. B' at most 113.5 MB (v14), connector under 2^23 bytes. E: the derivative
vectors (24 + 276 + 2,024 + 10,626 vectors of 24 words of 32 bytes, 10 MB) and, during setup, the ANF table of fes.c
(41,449 x 768 bytes, 32 MB). Before E starts, algorithm() keeps the echelon system of each of the K accepted spaces
(about 31 MB in all). Declared 2^30 bytes, more than 4 x the largest phase.

## 8. Not claimed; credits

Not claimed: any improvement on [GLL+20] beyond the byte-aligned (p = 8) adaptation, B', the counted programs and the
accounting. The certificates show that the construction works; they are not the claimed cost.

(v19: v19 is Meganpark980320's v18 with the changes of Section U, whose credits come first; co-authors Meganpark980320, rubenmarcus, Th0rgal, Subflatus3. v15's text follows.) This package is winglock's v14 (f1cedf6b, with Th0rgal as co-author), with two of its phases replaced. Everything not
named as new in Section 0 is theirs: the construction, B', the connector, the driver, the caps, the R5 study and its
replay experiments, every certificate of R5 and v6, fes.c and most of the experiment file and of this proof's text. The
new parts are T3 by meet-in-the-middle on zero blocks (2.1), the counted fast exhaustive search for E's stage 1 (2.4),
the repricing of the charged development at v15's programs (0.1), our development ledger D15, and the R6 study (4.7).

Credits: [GLL+20] for the connector and linearisation framework and the 5-round trail core that P re-derives; Dinur,
Dunkelman, Shamir (FSE 2012) for the target-difference algorithm; Qiao, Song, Liu, Guo (EUROCRYPT 2017) for
linearisation; Daemen, Van Assche (FSE 2012) and KeccakTools for in-kernel trail cores; Bouillaguet, Chen, Cheng, Chou,
Niederhagen, Shamir, Yang (CHES 2010) [BCC+10] for fast exhaustive search, used by v14's evidence enumerator fes.c and
now by the counted E. winglock (v8 113fc836, v13 7f16e461, v14 f1cedf6b) and Th0rgal (7deb1595, with Subflatus3 and
rubenmarcus) for the zero-advice framing and the whole algorithm this package modifies; Subflatus3 (9bccf245) also
used fast exhaustive search inside E (on the round-1 input, at 429 primitives per pair) and enumerated the output
core's leaves with AS(alpha2) <= 63 by a half-sum match on 5-row blocks, an idea close to our T3; GordoAR (e3ce0518,
bc0f7b56, ed433634) for re-sizing work on the same lineage; hybridnoise (ef4a0c66) and jagnani73 (654cb3d2) as
credited by v14. baseline_improved is the required nominal reference ID, not a claim of dominance.

## Appendix A. Trail search P as run (T1 and T2 in the experiment file; T3 in C)

These programs are our evidence for premise P (2.1); the algorithm's P is trail_search in r5.py. T1 and T2 ran as the
experiment file's lane_dfs and p45pos (cores.py: 1741 cores, 467 kept, sum C2 = 1,379,275,399,350, the counts that
r5-trail-0..3 recompute); export.py wrote, for every kept core in T2's order, its rows and, for every compatible input
difference of every row, the row values of L^-1 of that difference (core_tables), and the tables MINW and WT2
(cores.bin, SHA-256 a3a10277c3cd2fd0eb6cf82eb509ca57907b1597e37a8a8057db584c53a9a9b9). mitm2.c is T3 (2.1); its header
comment is the one of the earlier contiguous-block program mitm.c (D15), while its blocks and levels are those of
set_level, which are the ones of 2.1 and of r5.py. Built with clang -O3 -mcpu=apple-m4 and run as `mitm2 cores.bin 5`
(5 threads, 370 s, 296 CPU-s, 233 MB). Its output mitm2.log (3,277 lines: per core and level the half-vector entries,
matches and evaluations, per level the totals and the best leaf, then "CERTIFIED at level 6 (nb 64)") has SHA-256
e0430adb40d7f166ed1625494d02283a285092c33a608175a76371b74bbdbebc. SHA-256 of the sources: cores.py
7e77b07d0514846a4be75e0fc58a3ecd69b7fedc6b8b14aaa63e4c9fcd213bd5, export.py
d3e5256998b947b6265eab09b4b4d63025f8dea9cea0b3cfe63146d46a5e897c, mitm2.c
7a2ba2db66cf57ec664c623af8ed922067829d3f2a25c850d8d2f6a842b47d7f (the file hashed in R6's commit record, Appendix E).
v14's native T3 (trail3b, two exhaustive passes over all batches; v14's Appendix A) found the same trail.

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

fes.c (SHA-256 9a023ce614609bb9c27ba94683a6dc340f7a1324a3550ca4ba3f45775ae30de4, hashed in the plan of C) is an
exact form of E's stage 1 for evidence runs: f(c), the 24 residual bits at window coordinate c, has degree <= 4 in c
(round 0's output has degree <= 2, round 1's <= 4, and L is linear), so its algebraic normal form is the Moebius
transform of its values on the 41,449 coordinates of weight <= 4 with no assumption; coordinates 0..7 are bitsliced
and 8..31 enumerated by the degree-4 derivative recursion of fast exhaustive search. Every pass is printed;
espace.stage2 (Python, the experiment file's Linv_map and digest5) then compares complete digests. The driver
prereg_c.py (51ba941c...) calls the experiment file's bprime, Setup, attempt and enum_basis. The R5 study ran the
same binary (SHA-256 6d1110190325ed04bccc56eee4b2844e1a0f3d95f17e9cce0984a3d5c01835c3) with the same espace.py, from its
driver r5run.py.

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

v15: fes.c is also the native form of v15's counted stage 1 (2.4): it computes the same derivative recursion over the
same Gray order, with the inner 256 points in four 64-bit words per equation. R6 ran a binary built from this source
with clang -O3 -mcpu=apple-m4 (SHA-256 93eff750b3529c2d54a48f5368f6c19f3d8ff70b935cbf380d13b4b564199a86) and the
stage 2 of r6run.py (Appendix E).

## Appendix C. The plans of pre-registrations C and D (verbatim)

C's plan refers to the three heuristics H1-H3 of the v11 draft. C and D measured v13's algorithm; v14 charges C
(0.1) and uses neither for its bound.

prereg_c/plan.txt (SHA-256 4e1edbd45e4b0dfb10de7a67f432805e30d54eef073caba197d26ace7142b666):

```text
Pre-registration C for hashsmash sha3-256-r5 v11 (written before any run of C; its SHA-256 and UTC time are
recorded in prereg_c/commit.txt before run_c.sh starts).

Purpose: measure, with fresh labels and no decision rule about submitting, the three averages that the success
probability of the v11 algorithm needs (H1, H2, H3 of v11), over the algorithm's own randomness.

Runs: k = 0..47, all of them, started by tools/run_c.sh (12 at a time); none is stopped, excluded or repeated;
every result file runs/<k>.json and runlog.txt is reported.  Labels: B' "hashsmash sha3-256-r5 v11 C B-prime run
<k>", connector "hashsmash sha3-256-r5 v11 C conn run <k>".  Coins: the experiment file's Coins and run_seed
(SHA-256 seeds, SHAKE-256 words).

Per run (tools/prereg_c.py): B' of the experiment file (budget 2^32 units, candidate cap 2^26 units, all
candidates and attempts logged with counted costs); the connector rule of algorithm() (attempts until 96 accepted
or 2^11 attempts, then discard); E on the first 16 accepted spaces of a kept advice over the whole 2^32 window
(tools/fes.c, exact: degree-4 interpolation on the 41,449 points of weight <= 4 and fast exhaustive search, with a
self-check against direct evaluation at 64 checkpoints), stage 2 by complete 5-round digests (tools/espace.py).
fes.c was checked before this plan against the v6 and v8 logs: v6 spaces 0 and 1 give 271 and 276 round-2
passes; v6 positives 38, 126, 462 and the three v8 positives are found at their recorded coordinates.

Analysis (tools/analyze_c.py, fixed now): joint 95% confidence by Bonferroni (alpha 0.02 for H1's mean, 0.015
for H2, 0.015 for H3); H2 pooled with pre-registration A (9 runs, 65 candidates); H1 with the Kish design
effect under the dispersion premise v0 = 1, switched to v0 = 3 by the code if the chi-square homogeneity test
of per-advice positive counts has p < 0.01 or the within-advice second moment exceeds 2 s-hat^2.
Use: K = 96 (v10's value) if the success bound at the confidence bounds is >= 0.40 at K = 96; otherwise the
least multiple of 8 up to 512 for which it is (the claimed time then grows).  There is no rule about submitting
that depends on the outcome; the package states whatever the analysis gives.
```

prereg_d/plan.txt (SHA-256 3a3bc8119b38b5eaa969a4a803db9b0c9d59c08b363ebaecc88816aeb21ba46c):

```text
Pre-registration D for hashsmash sha3-256-r5 v11 (written before any run of D; its SHA-256 and UTC time are recorded
in prereg_d/commit.txt before tools/run_d.sh starts).

Purpose: measure the v11 algorithm's success probability end to end, with no premise about how s(a) varies across
advices.  Each of the 48 runs of pre-registration C is a complete run of the algorithm up to E: B' under its budget and
candidate cap gave an advice, the connector rule kept it with 96 accepted spaces (no run was discarded).  The
algorithm succeeds on such a run iff E outputs a pair on one of these 96 spaces.  C enumerated the first 16; D
enumerates the rest, in order, stopping at the first space with an output, as the algorithm's E does.

Runs: the 30 runs of C with no positive space among their first 16 (k = 0 1 2 3 4 8 9 10 11 12 13 16 17 19 22 23
26 28 29 31 32 34 35 36 37 38 39 41 45 46) and run 999 (the smoke test of C's driver, made after C's plan with
label k = 999 and outside C's sample; 0 positive spaces in 16), started by tools/run_d.sh (12 at a time); none is
stopped, excluded or repeated; every file prereg_d/runs/<k>.json, err_<k>.txt and runlog.txt is reported.  The other
18 runs of C already succeeded (a positive space among the first 16) and are not re-run.

Per run (tools/prereg_d.py): re-derive the advice from its label (bprime started at the logged accepting candidate;
must reproduce C's advice hash) and each accepted connector attempt from run_seed(conn label, i) (must reproduce C's
status, DF and work count); E (tools/fes and espace.stage2, the files of C, unchanged) on accepted spaces 17..96 in
order until the first output.  Before this plan the driver was checked only with --check on run 0's space No. 1,
which C had already enumerated (265 round-2 passes, no output; reproduced), so no new outcome was seen.

Analysis (tools/analyze_d.py, fixed now): x = number of the 48 runs k = 0..47 that succeed; p_L = one-sided 95%
Clopper-Pearson lower bound on x / 48; p_L' the same on the 49 runs with run 999 added.  A run with a missing file or
an error counts as a failure.  Use: K stays 96 (no constant changes).  The claimed success probability is 0.40 if
min(p_L, p_L') >= 0.40, else min(p_L, p_L') rounded down to two decimals; the package reports the result in every
case.  There is no rule about submitting or withholding that depends on the outcome.
```

## Appendix D. The R5 study: plan, commit record and per-run ledger (verbatim)

plan.txt (SHA-256 7ffaf34f4001a449a6775fa3f204f7c93a0be60c69e45588d320aae1d382574b):

```text
Pre-registration R5 for hashsmash sha3-256-r5 (written before any run of R5; its SHA-256 and UTC time are recorded in
commit.txt together with the SHA-256 of every file it names; a first commit at 20:27:03Z was replaced before any
run, only to change the launcher's start gate).

Purpose: measure, end to end, the success probability of the R5 algorithm over its own coins. R5 is v13's algorithm
(algorithm() of r5v13.py, byte-identical to v13's experiments/r5.py) with B''s six tuned constants replaced by values
that no run selected:
- no attempt limit per candidate (B_R = 2^62, never reached): a candidate ends at its accepted attempt or at its cap
  CCAP = 2^26 units;
- B''s DMIN = 33, the connector's value, which is the least DF for which E's window and beta exist;
- the D2u ordering weights KW = MW = LB = PREF = 1 (unweighted).
Every other constant is v13's: K = 96, CCAP = 2^26 units, B_BUDGET = 2^32 units, A_ADV = 2^11, A_MAX = 2^13,
X_MAX = 2^23, S2CAP = 2^24, F_CAP = 2^30. P's output is the trail of v13's proof Section 3 (P is deterministic).

Runs: k = 0..47, label "hashsmash sha3-256-r5 R5 run <k>" (B' candidate and attempt coins and connector coins derived
from the label exactly as algorithm(label) does). Each run is r5run.py <k>: B' with its budget and candidate cap, the
connector rule (attempts until 96 accepted or A_ADV, then discard and resume B'), then E on the accepted spaces in
order, stopping at the first output, as algorithm() does. E on a space is fes (exact over the 2^32 window, self-check
at 64 points; Lemma 4 of the proof makes it E's function of the space) with stage 2 by complete 5-round digests on at
most S2CAP pairs. Launch: run_all.sh (at most 10 runs at a time, nice 10; a new run starts only when fewer than 11
processes on the machine are busy and the 1-minute load average is below 12). Every run is started and completed; none is stopped, excluded or repeated. If the machine
crashes, run_all.sh is started again and runs only the k without a result file (runs are deterministic functions of
their labels, so a restarted run has the same result); any restart is reported.

Analysis (analyze.py, fixed now): s = number of the 48 runs that output a collision; p0 = one-sided 95%
Clopper-Pearson lower bound for s of 48. Claim rule for any package built on R5: success 0.40 if p0 >= 0.40;
otherwise R5 is not claimed. Every run is reported in a per-run table whatever the outcome. This study changes no
constant of R5.

Known before this plan: a parallel session's plan C' of 2026-10-07T16:58Z ran the same B' configuration with
os.urandom seeds and a native E; 14 runs started, 4 finished (each with a collision) and 10 were left unfinished.
Those runs are not part of this sample. The only run made with this driver before this plan is its self-test, which
re-derived v11 pre-registration C's run 5 positive space with v11's constants (collision at 0x2b32ba84; no R5
constant was set).
```

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

Other files of the study (SHA-256): the superseded commit record commit_superseded_2027Z.txt 2bf5e4857146647c0e44bad6f973f25424fcb21774a5ad249b41f648fabfabc0;
launch_all.sh 09f13f6412477c3714a4f1c6afc9bbaa2a2f9224aedb7c388e8cb31684e92d81 and watchdog.py c0f03d92bf1f653c4268ebd06721189666d647e99ff74d7c1085e6b6df186b4d (written after the commit and
before the launch; operational only); launch.txt d94e657b34494a858f30825290954268cbb5b246133c7bb20fa7cf6e0bb9c68b; runlog.txt f6bdce33e5630716205f81a1c01b3f7d6a241d876c8ac2d467c843b66fd77c87;
watchdog.log 953f8bd7cbc95bce03c35a254d1bac7e9ce3535ba57372dbe44b58fdf73dcd26; finished.txt 877ed57ab0381cbac6dd62dab1481a34f4e2cc0d4059ecdee44681970bb7cc91; analysis.json
25e283c8b53d9725830e263daf9fa69c433859b47f30b7a9e1dcb7d95a96d2b3; the 48 result files runs/0.json .. runs/47.json concatenated in k order
9bbeffce00b293c110f53493b51327877d3c640016b9ec7471774e98f1884185 (each file's own SHA-256 is in its ledger line).

Per-run ledger (one JSON object per run, derived from the result files; SHA-256 of the text below, with a final
newline, c08a5834a3b1d5fab1b67e49017c5940e45fa93a48f9b54700366c73017c513e). Fields: candidates; per advice round (c, j, DF, advice hash prefix, B''s exact WK
count in 1/1355 units, connector attempts, accepted, kept); spaces enumerated and their round-2 pass counts in order;
fes self-checks; whether the stage-2 cap bound; largest connector attempt in work units; first positive space; the
output coordinate and the SHA-256 of the output pair (message a || message b); Python CPU seconds.

```text
{"k":0,"file_sha256":"8fa1ef8f4fd841ec0b13f8bc2cc9831a1d991b2114be17759f69e414c07c6df0","candidates":1,"rounds":[{"c":0,"j":25,"DF":46,"advice_sha256_16":"280945655e1ee829","bprime_wk":38074812258,"attempts":128,"accepted":96,"kept":true}],"spaces":14,"passes":[240,243,232,254,259,214,274,243,258,261,243,265,273,254],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":169059,"first_positive":14,"success":true,"coordinate":"0x666ad35a","pair_sha256":"9790baf7d8718ff77202382597cb25d4f8bf4ea143f029b24ad665e669e97e9d","cpu_s":17.9}
{"k":1,"file_sha256":"f485643ce92a49689ac14860b14a7cabf964e20b8c604e8899d16e353b5ca65d","candidates":4,"rounds":[{"c":3,"j":17,"DF":45,"advice_sha256_16":"3e77c8b3006fc433","bprime_wk":312337330281,"attempts":238,"accepted":96,"kept":true}],"spaces":75,"passes":[252,246,261,252,248,253,239,275,269,240,262,227,252,268,251,239,235,241,245,244,242,266,255,232,234,251,274,247,235,251,242,262,263,253,255,282,233,235,258,269,254,253,281,268,263,268,256,242,262,255,267,232,268,255,238,235,299,264,303,261,277,238,247,259,305,240,238,241,261,257,271,273,246,245,259],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":158726,"first_positive":75,"success":true,"coordinate":"0x583943c6","pair_sha256":"cef3599bb02542bf9906ef63e3b886ded8f2f4eb62a59e62a74b97f0fa2670d8","cpu_s":115.2}
{"k":2,"file_sha256":"73a80a83c838ca43f42e724cf936920e2f90c51fc283d47ed0531e98c5fb4221","candidates":3,"rounds":[{"c":2,"j":41,"DF":40,"advice_sha256_16":"fcc740d15e2c123c","bprime_wk":251078095236,"attempts":96,"accepted":96,"kept":true}],"spaces":44,"passes":[222,253,251,229,242,246,269,254,267,238,278,229,258,238,290,263,282,253,265,251,274,261,241,249,270,268,253,262,232,242,255,282,267,262,272,257,241,295,225,246,227,277,237,249],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":180277,"first_positive":44,"success":true,"coordinate":"0xeb9478a8","pair_sha256":"3c8e4adc35fcb4852724c22995864b5a219b9133c20efab84b319c161a94b230","cpu_s":245.6}
{"k":3,"file_sha256":"2f52e9bb31af72c93f3f7f9394e1fe96e60076bd0e3bccb0e8b30da14f6df713","candidates":7,"rounds":[{"c":6,"j":12,"DF":37,"advice_sha256_16":"2582f7e5e1ee05a3","bprime_wk":578328306529,"attempts":441,"accepted":96,"kept":true}],"spaces":22,"passes":[257,249,255,240,262,247,263,265,262,233,293,236,255,248,238,247,294,266,244,261,233,263],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":162093,"first_positive":22,"success":true,"coordinate":"0x2bed516e","pair_sha256":"63f2680f2788a88c3f3d96f80db5b4b068a8c8e9d3e6dbf5c5766646f50f908c","cpu_s":806.9}
{"k":4,"file_sha256":"3fbcb7090b2dd3bb7baf192150ce196f1e2d586f0cd100cd4489a0c5233b7e32","candidates":4,"rounds":[{"c":3,"j":37,"DF":41,"advice_sha256_16":"990540e7f5ee7f2e","bprime_wk":343020384242,"attempts":96,"accepted":96,"kept":true}],"spaces":1,"passes":[253],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":155543,"first_positive":1,"success":true,"coordinate":"0x809f225b","pair_sha256":"12586fc0e3f70e7817c88e93a1769fd64599d63887f2aca7864fae50f66fd8e1","cpu_s":389.0}
{"k":5,"file_sha256":"3c79f927df5b3a0ff010edc0dd4f47dfb78945db9a2a5983bfb6977dc1296ec7","candidates":7,"rounds":[{"c":6,"j":23,"DF":44,"advice_sha256_16":"0ed8a41be7b8d0f2","bprime_wk":599657552824,"attempts":122,"accepted":96,"kept":true}],"spaces":27,"passes":[258,260,247,268,247,266,247,245,232,242,262,256,263,267,252,271,267,240,257,251,257,260,262,264,252,255,260],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":160667,"first_positive":27,"success":true,"coordinate":"0xb046f6d2","pair_sha256":"06bd06bef66154b161109e475793f800f4a93471b103d812a058749657d6dba9","cpu_s":799.3}
{"k":6,"file_sha256":"f03afbf368c1cf62fc621e7dfabb790e4ed9534e330065a247644ddb64ca9670","candidates":4,"rounds":[{"c":3,"j":22,"DF":52,"advice_sha256_16":"a66cd4311a4614e7","bprime_wk":313594643595,"attempts":452,"accepted":96,"kept":true}],"spaces":96,"passes":[282,268,252,255,268,266,245,254,233,241,279,279,219,252,250,250,261,264,256,248,244,218,237,266,235,236,265,248,251,266,237,268,234,227,250,248,260,272,259,255,280,252,245,261,253,261,283,262,268,259,247,267,256,242,249,259,263,252,265,200,251,266,249,233,235,255,255,283,225,273,239,289,247,263,265,256,293,277,247,233,236,242,276,242,239,273,242,237,274,229,268,248,257,259,246,243],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":159967,"first_positive":null,"success":false,"cpu_s":577.8}
{"k":7,"file_sha256":"d611f95aafa759448853d2e69349140a04ca4fcb6afd0cbc900f36d6cc47af5b","candidates":3,"rounds":[{"c":2,"j":19,"DF":46,"advice_sha256_16":"c0a660ea8ca083fb","bprime_wk":225008224082,"attempts":557,"accepted":96,"kept":true}],"spaces":5,"passes":[282,256,256,249,254],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":172832,"first_positive":5,"success":true,"coordinate":"0xb29f36d1","pair_sha256":"c650e07bd8a9c29ab47cd7a79974dc08a04d37c59a05829a1e61a6079b45b4db","cpu_s":393.7}
{"k":8,"file_sha256":"eab8ceba3524ef5ab9df2d2945d10a282911fb0541472dadcbac449d88eeef60","candidates":2,"rounds":[{"c":1,"j":46,"DF":42,"advice_sha256_16":"86143858d2186b3e","bprime_wk":167812154154,"attempts":110,"accepted":96,"kept":true}],"spaces":8,"passes":[279,235,301,259,246,236,256,254],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":170670,"first_positive":8,"success":true,"coordinate":"0x49b7c1aa","pair_sha256":"7e6c2481e01f8ba67b93c3916ed3bfa9ad69a92f133b8cf9b203aec6ba97acbd","cpu_s":192.2}
{"k":9,"file_sha256":"dfe861dbf8745df906558449225b8083c3bcef1c0b13b012c21a036d990946a6","candidates":4,"rounds":[{"c":0,"j":18,"DF":38,"advice_sha256_16":"084ea8d296fc5738","bprime_wk":40954994054,"attempts":2048,"accepted":65,"kept":false},{"c":3,"j":37,"DF":37,"advice_sha256_16":"0bb3d38f1b42a976","bprime_wk":251622426462,"attempts":239,"accepted":96,"kept":true}],"spaces":26,"passes":[246,248,242,246,251,251,251,266,243,258,238,246,265,269,250,234,263,247,238,264,239,266,238,247,254,240],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":173127,"first_positive":26,"success":true,"coordinate":"0xea0802ec","pair_sha256":"e665b1b063910547586545a660972bfd9a68faa53e87cb9b46bc099ac96ae026","cpu_s":308.1}
{"k":10,"file_sha256":"806069b5dd52cea93a5815000585bca028407d40399fd71ec6411e7b7db7bea6","candidates":4,"rounds":[{"c":3,"j":24,"DF":35,"advice_sha256_16":"150f8e0160df3ae2","bprime_wk":327621245214,"attempts":176,"accepted":96,"kept":true}],"spaces":1,"passes":[253],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":165466,"first_positive":1,"success":true,"coordinate":"0x18794793","pair_sha256":"7a156f9cfc4ea84dd1c1da10a46d7ed5ca977e4bb510ac27f02dbc8a68c5a520","cpu_s":585.9}
{"k":11,"file_sha256":"08122e68e1e9755965b97b3ad5460c20cdf3ee4423905bd93887ec0981044edc","candidates":3,"rounds":[{"c":2,"j":11,"DF":40,"advice_sha256_16":"dfd46d98c5bac015","bprime_wk":207393917721,"attempts":425,"accepted":96,"kept":true}],"spaces":25,"passes":[231,266,246,269,270,223,243,247,242,271,266,251,302,244,226,268,279,243,247,280,260,259,234,265,284],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":166768,"first_positive":25,"success":true,"coordinate":"0x24cde90d","pair_sha256":"9b4b72563b26a43939c64fa1a13602381b925eea1ab0f2e8fd8d96ed946c1901","cpu_s":77.4}
{"k":12,"file_sha256":"f7bc4fe75d8e7b79a7db053de2e16c648fe9710408f431da4f09b0d34c1d25a1","candidates":3,"rounds":[{"c":2,"j":1,"DF":38,"advice_sha256_16":"47aaaf1baf7ff3e9","bprime_wk":192180288756,"attempts":173,"accepted":96,"kept":true}],"spaces":42,"passes":[238,253,255,285,242,287,226,247,251,285,265,278,243,273,271,254,274,264,250,260,278,231,233,251,258,273,270,251,276,279,267,282,237,265,273,244,264,259,250,251,248,250],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":172687,"first_positive":42,"success":true,"coordinate":"0x8c2e14b6","pair_sha256":"9b18bfce3758e2b5e5616b510015b172ebfd006740ad399a859909a50e7177a9","cpu_s":225.7}
{"k":13,"file_sha256":"36373c25a87f3910859b787b76cf5e8ef96c4f0fc6865e0cdfa7bac61d10b235","candidates":1,"rounds":[{"c":0,"j":30,"DF":51,"advice_sha256_16":"8525d2214e680d20","bprime_wk":46500147486,"attempts":145,"accepted":96,"kept":true}],"spaces":29,"passes":[284,235,239,241,250,249,252,267,270,280,262,233,255,262,257,245,280,256,262,269,259,255,255,283,226,246,261,258,274],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":150197,"first_positive":29,"success":true,"coordinate":"0xb78632c1","pair_sha256":"6666fedb64a3c018c93173754d80ff7148bf5a5ac7f94aa33702bbccb57dd49c","cpu_s":24.4}
{"k":14,"file_sha256":"f497860587819887895984e81567f85d5026569e79213f1dd88fe1bb355eb92a","candidates":4,"rounds":[{"c":3,"j":16,"DF":45,"advice_sha256_16":"e8f4d11f7e68145f","bprime_wk":309025389420,"attempts":191,"accepted":96,"kept":true}],"spaces":7,"passes":[262,253,265,267,240,259,241],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":171880,"first_positive":7,"success":true,"coordinate":"0x2fd52b7c","pair_sha256":"af194024ce73148dcd738fec4667c43d205e4fcfb49293b0153571eba2b22b01","cpu_s":421.6}
{"k":15,"file_sha256":"ac5b8c14273a1db0cd67eee2f36473374167481ff38edebbe8d17ca22176e9fc","candidates":5,"rounds":[{"c":4,"j":6,"DF":51,"advice_sha256_16":"0f79c3f921bf1079","bprime_wk":403494575287,"attempts":124,"accepted":96,"kept":true}],"spaces":12,"passes":[252,248,246,267,279,267,235,250,272,244,232,254],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":171019,"first_positive":12,"success":true,"coordinate":"0xf798b773","pair_sha256":"9bfb43265ce31e91cfc0a77b96882beab53461e88ebff5b114d97328c8a10950","cpu_s":278.1}
{"k":16,"file_sha256":"905e52e68c94959aa869f392606a0bec9af20e9cefde3b549592db4bdd72610c","candidates":1,"rounds":[{"c":0,"j":16,"DF":59,"advice_sha256_16":"e555cc23f6c334fc","bprime_wk":33239383121,"attempts":137,"accepted":96,"kept":true}],"spaces":18,"passes":[272,285,244,235,261,238,248,249,240,276,273,280,252,249,266,268,270,250],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":169904,"first_positive":18,"success":true,"coordinate":"0xfd207a79","pair_sha256":"d93bce4aaa25c92552cfeecefdf0a2b66b7dd1285ba8cba4dac914276dd666bb","cpu_s":18.3}
{"k":17,"file_sha256":"e7007a7bf08887e55d4c25e402371682a3cde835876e2e2f528529065cdbcac1","candidates":3,"rounds":[{"c":0,"j":29,"DF":33,"advice_sha256_16":"e8437f477f92fd1a","bprime_wk":77092244681,"attempts":2048,"accepted":0,"kept":false},{"c":2,"j":11,"DF":34,"advice_sha256_16":"4c655d9b3d5148e9","bprime_wk":151180478561,"attempts":260,"accepted":96,"kept":true}],"spaces":6,"passes":[258,264,251,271,276,221],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":182357,"first_positive":6,"success":true,"coordinate":"0xf802f1a0","pair_sha256":"60fab94516deda7de4a5f169d41e7166f38f10dff70487a846a5da3703c68f61","cpu_s":137.4}
{"k":18,"file_sha256":"81ef2bcb468e4a7ba358cc3883af56d7882041293e0de29af1651147332989ca","candidates":7,"rounds":[{"c":6,"j":9,"DF":51,"advice_sha256_16":"faeeaff303a4bc16","bprime_wk":574144202201,"attempts":96,"accepted":96,"kept":true}],"spaces":62,"passes":[233,252,267,242,246,262,244,293,250,274,293,257,254,264,252,289,276,216,266,266,247,218,223,247,244,283,278,264,232,247,235,278,266,292,259,275,247,245,237,255,276,223,243,252,236,246,269,294,264,232,261,267,275,221,271,256,264,252,272,251,273,267],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":151924,"first_positive":62,"success":true,"coordinate":"0x9a5263fe","pair_sha256":"141ee6a1b7d78e902bc4b35b4454f8f8f4fb2030900b93e2e31b71d3471c4259","cpu_s":682.6}
{"k":19,"file_sha256":"cbd905e4148068641dc1c2b134142b993a563f6eefaeb2950041dcf9d99bc1fa","candidates":4,"rounds":[{"c":3,"j":6,"DF":67,"advice_sha256_16":"e825a2f1d8233c5b","bprime_wk":295807253548,"attempts":153,"accepted":96,"kept":true}],"spaces":48,"passes":[257,253,232,276,256,261,275,291,259,239,244,239,252,261,270,240,280,262,267,280,234,246,264,238,274,274,251,264,266,262,253,252,238,255,272,231,274,246,262,257,238,240,224,253,253,229,233,272],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":157812,"first_positive":48,"success":true,"coordinate":"0x1d43683a","pair_sha256":"aa0ed22edfcd7faf33f7dddb57ca5ef7afb7231744b67dfc6cd5c122277a0bdc","cpu_s":259.2}
{"k":20,"file_sha256":"48d3030ca0ee16fcdb69db7519afc6d1f5b8f14a53d2712cc298d530d73a6a42","candidates":1,"rounds":[{"c":0,"j":42,"DF":44,"advice_sha256_16":"779e8a13a798fff0","bprime_wk":70134455323,"attempts":138,"accepted":96,"kept":true}],"spaces":1,"passes":[248],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":150376,"first_positive":1,"success":true,"coordinate":"0xdc7d40cd","pair_sha256":"52474a896f0d52686380c2c3b6b56db4520a9a8a40a6bc6997cc3af165181852","cpu_s":22.4}
{"k":21,"file_sha256":"52348f87ec4998255ea1f7ff7ed828217ab1b5c43bc5508139ab402790610350","candidates":1,"rounds":[{"c":0,"j":3,"DF":49,"advice_sha256_16":"76a6a0b06305286a","bprime_wk":16241153777,"attempts":206,"accepted":96,"kept":true}],"spaces":1,"passes":[240],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":145190,"first_positive":1,"success":true,"coordinate":"0x18c48859","pair_sha256":"a0a8f20cf4ea8c4499b3f216759b955c54868fdcf31f3c35beab64206a798b65","cpu_s":10.6}
{"k":22,"file_sha256":"90bb393d3411fafff857e78ee20b3a3f24bf2700d607a1b1718096cd370768e7","candidates":5,"rounds":[{"c":4,"j":10,"DF":47,"advice_sha256_16":"307b89e477e629a7","bprime_wk":394934128877,"attempts":419,"accepted":96,"kept":true}],"spaces":20,"passes":[254,254,269,253,248,250,228,262,264,268,257,246,247,255,276,249,236,250,262,242],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":155808,"first_positive":20,"success":true,"coordinate":"0xedac52b","pair_sha256":"211619b1de35f06434b832cdaedba2ef951dcb121ecfa184ee29adb217b06ad6","cpu_s":811.7}
{"k":23,"file_sha256":"b7a31881c49fc15275df14c01ef59951ac6c7dfa2e1d53560ca3d8f4941abd93","candidates":3,"rounds":[{"c":2,"j":4,"DF":36,"advice_sha256_16":"ed6b47add7f42842","bprime_wk":200506769832,"attempts":120,"accepted":96,"kept":true}],"spaces":8,"passes":[272,259,253,246,254,243,262,291],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":189059,"first_positive":8,"success":true,"coordinate":"0x4c97b04d","pair_sha256":"bc098599327e16a9e58301f5a52c1bf1edde958ed3867ae4a5c1af82d17b541d","cpu_s":227.6}
{"k":24,"file_sha256":"64ed2d76e0d1f8bec7785b342ce98c0af1513ae5053a4045d38f64369c27e3c2","candidates":1,"rounds":[{"c":0,"j":2,"DF":38,"advice_sha256_16":"c512e5d242700b34","bprime_wk":13054253838,"attempts":215,"accepted":96,"kept":true}],"spaces":10,"passes":[256,259,272,272,232,281,235,245,247,232],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":180653,"first_positive":10,"success":true,"coordinate":"0xd37d80d0","pair_sha256":"26633a06f988d5382655357b6e36ac12a46d8effb1e56b31b5377b5a7747e040","cpu_s":13.6}
{"k":25,"file_sha256":"3d81b91a491a912cc2de0408f0f7c51a83fc12665cf1b5178f29894ace4f8180","candidates":1,"rounds":[{"c":0,"j":5,"DF":50,"advice_sha256_16":"0bc2399f10895341","bprime_wk":18097029411,"attempts":147,"accepted":96,"kept":true}],"spaces":27,"passes":[254,258,256,256,249,266,269,251,253,261,250,249,249,254,250,264,279,229,267,255,278,267,239,256,259,272,250],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":163758,"first_positive":27,"success":true,"coordinate":"0x32e5b851","pair_sha256":"f0ad4c091ec5fee0cbe0f0a947979b187898f10e7e7d6c16ac59da2b0b14c716","cpu_s":17.7}
{"k":26,"file_sha256":"d753c7d46d0c2b2c2ae138897f9d5f5bb4ac3f4722fbb0abae4b4fbcc4cef2be","candidates":4,"rounds":[{"c":3,"j":22,"DF":76,"advice_sha256_16":"b2bf1e43951643a3","bprime_wk":314294025988,"attempts":339,"accepted":96,"kept":true}],"spaces":22,"passes":[252,222,247,263,241,272,249,278,276,273,240,258,245,229,254,266,240,242,263,247,257,245],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":141284,"first_positive":22,"success":true,"coordinate":"0x2ddd6f8c","pair_sha256":"bd9be57c03c3c3c12465de0b54331bee766ba009e048dca77db48a195dfb1c12","cpu_s":613.5}
{"k":27,"file_sha256":"c4bcbeae9630a3cfa1892cbba702c68b472d745664bbb384afd9380f49439e73","candidates":2,"rounds":[{"c":1,"j":29,"DF":35,"advice_sha256_16":"f1f0e642722eb6c1","bprime_wk":170544972982,"attempts":154,"accepted":96,"kept":true}],"spaces":5,"passes":[241,242,271,263,296],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":183028,"first_positive":5,"success":true,"coordinate":"0x9d691e84","pair_sha256":"ef451682763b429038ade5a5ab8073e32bbc5a53ed8b1f82501f306496bba266","cpu_s":219.0}
{"k":28,"file_sha256":"1d137a7c51c9282738b11b0cce10c472ed034baa190df357500b8833ddb9596b","candidates":2,"rounds":[{"c":1,"j":21,"DF":47,"advice_sha256_16":"c4d9ae4a6e956874","bprime_wk":139927868687,"attempts":195,"accepted":96,"kept":true}],"spaces":13,"passes":[253,267,228,271,248,245,269,251,247,271,254,250,245],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":169261,"first_positive":13,"success":true,"coordinate":"0xb692bd00","pair_sha256":"fea11aa78821859ff963da34f1ed82acf65a953d91c6c7b6a5299e09e03e5f4a","cpu_s":48.5}
{"k":29,"file_sha256":"52a9912c0a1fcaa16287d021d24295035cd4b62a3dafb63b2590cecbb4009060","candidates":1,"rounds":[{"c":0,"j":18,"DF":38,"advice_sha256_16":"080af7ab45188e38","bprime_wk":40805517088,"attempts":142,"accepted":96,"kept":true}],"spaces":86,"passes":[265,243,254,258,235,283,232,214,241,243,268,235,232,231,280,252,232,224,255,248,242,248,252,241,288,236,249,277,257,263,239,252,269,250,276,246,273,268,236,257,283,242,275,257,257,245,280,275,230,246,257,233,262,277,271,206,261,248,242,270,238,265,249,248,262,271,267,222,265,241,290,284,250,264,242,260,266,254,250,265,248,283,275,270,272,253],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":156593,"first_positive":86,"success":true,"coordinate":"0x8a033888","pair_sha256":"2da2bb4d2daa786c1cb9d903abbe46573cda5bba55451aa252acddb8ef0d9a20","cpu_s":40.3}
{"k":30,"file_sha256":"f8f1215f84e944edaa72db6d16d69b27238cb6b3d30bebe81c38a3fb0a4bdd7a","candidates":2,"rounds":[{"c":1,"j":2,"DF":51,"advice_sha256_16":"0886a4cd8c109dfb","bprime_wk":101712554082,"attempts":122,"accepted":96,"kept":true}],"spaces":14,"passes":[248,274,228,259,242,252,254,250,276,247,269,263,266,230],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":154824,"first_positive":14,"success":true,"coordinate":"0x7677e6d5","pair_sha256":"9848ec7bfcabce7e808d6f68218568f9c191ea9b3e679dbf3c009491292b729c","cpu_s":200.9}
{"k":31,"file_sha256":"bde3e12b2fd8cb89394d4b79b261832aa244f0d95b23ff9d6b63e87201958984","candidates":1,"rounds":[{"c":0,"j":18,"DF":40,"advice_sha256_16":"90e806abff67dd73","bprime_wk":65385934933,"attempts":181,"accepted":96,"kept":true}],"spaces":96,"passes":[297,249,250,274,244,259,255,260,242,251,282,249,308,231,278,254,242,246,226,229,278,266,241,258,238,242,270,256,256,245,248,244,266,274,257,252,272,266,266,227,289,237,245,291,301,229,227,261,267,269,242,268,277,256,295,265,275,252,255,253,250,279,253,242,253,246,245,254,258,263,278,238,287,254,275,248,264,268,229,242,262,256,262,250,241,293,222,283,260,236,276,253,264,256,262,239],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":182799,"first_positive":null,"success":false,"cpu_s":48.1}
{"k":32,"file_sha256":"81814ecaee495de0407c70a0516ecf82e9e722878b0428ba8084bf651bd32010","candidates":3,"rounds":[{"c":2,"j":49,"DF":59,"advice_sha256_16":"f0aacc181f17e5f2","bprime_wk":255263864595,"attempts":113,"accepted":96,"kept":true}],"spaces":69,"passes":[248,246,277,238,222,279,246,241,274,254,250,246,281,237,230,261,268,258,239,238,283,273,250,230,288,262,251,276,266,282,251,267,265,262,226,256,268,295,285,249,253,267,270,261,267,256,261,279,261,260,257,279,254,265,286,282,260,255,272,263,240,266,230,267,271,298,279,222,252],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":174374,"first_positive":69,"success":true,"coordinate":"0x7ee68969","pair_sha256":"fc09481a5284ea183889a00d7a9db55440172b390dc591f2157edb83cc37e58b","cpu_s":445.9}
{"k":33,"file_sha256":"fd5220669294ec8b9d0a4b60845bbb856fa5dd40befbd2984deb31dc0d008349","candidates":4,"rounds":[{"c":3,"j":0,"DF":33,"advice_sha256_16":"06cbae2481d762d4","bprime_wk":281425137060,"attempts":96,"accepted":96,"kept":true}],"spaces":89,"passes":[282,256,238,251,264,238,269,246,265,273,262,254,227,244,278,273,256,242,254,252,272,239,271,264,260,250,245,261,294,246,251,226,254,237,262,231,274,275,277,253,248,241,243,250,233,261,238,251,232,224,213,245,253,257,254,246,241,250,250,247,271,247,262,263,244,272,256,261,267,287,243,242,254,251,249,270,253,240,273,269,235,232,275,241,270,253,263,271,232],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":174985,"first_positive":89,"success":true,"coordinate":"0x6de67ec4","pair_sha256":"10b5a22fca2345ca8040578417014049f3f223b726cc07c306e8523e5ee4c55d","cpu_s":451.5}
{"k":34,"file_sha256":"61890e4957637e4587e549c72f55ec6c4fa9554b5dbd0242df253e91670e3065","candidates":1,"rounds":[{"c":0,"j":9,"DF":39,"advice_sha256_16":"80224146e6c5ad7d","bprime_wk":34267480602,"attempts":121,"accepted":96,"kept":true}],"spaces":17,"passes":[235,261,237,269,255,266,265,278,254,229,243,252,258,262,269,248,237],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":169150,"first_positive":17,"success":true,"coordinate":"0x5c9dc6b0","pair_sha256":"ff07535ef3c39e48a4736e5a2c97bcc31bd23400caccc87b6a19b3a9a91c788a","cpu_s":18.4}
{"k":35,"file_sha256":"d7b319ec8a3c90e873f1d41392bd957e9e2e96d75741afecc94bb0d892235e1f","candidates":2,"rounds":[{"c":1,"j":17,"DF":50,"advice_sha256_16":"d729790d79918f57","bprime_wk":130539795895,"attempts":119,"accepted":96,"kept":true}],"spaces":18,"passes":[240,247,213,237,279,247,247,249,255,275,233,252,251,268,256,246,273,231],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":159671,"first_positive":18,"success":true,"coordinate":"0x5268c733","pair_sha256":"c22b7cdf49d76a3c71adba18be69f2254427c7e142ea59e557c314ac04903573","cpu_s":42.0}
{"k":36,"file_sha256":"3603e35ca4fc807371293c729fa8e22b9583cbbe87c87e6ad0fa082290f89127","candidates":2,"rounds":[{"c":1,"j":8,"DF":42,"advice_sha256_16":"939a664bfd2456cc","bprime_wk":116965248146,"attempts":96,"accepted":96,"kept":true}],"spaces":10,"passes":[266,248,260,278,246,255,256,251,254,241],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":175091,"first_positive":10,"success":true,"coordinate":"0x9c81d199","pair_sha256":"ec370eba500ebe99215b1b97e2af06c08d33930dbe400cfee930aa4b73476a3a","cpu_s":206.9}
{"k":37,"file_sha256":"612e67e05d789e2ee0f9c97ee6fd92aa68f3089c4e6ea521783fde54ce642549","candidates":1,"rounds":[{"c":0,"j":10,"DF":49,"advice_sha256_16":"6588bac5e87ef9ee","bprime_wk":23668632583,"attempts":115,"accepted":96,"kept":true}],"spaces":53,"passes":[239,237,264,262,271,218,223,265,277,267,206,275,282,262,258,251,253,274,260,261,255,249,258,261,260,240,256,264,266,273,255,241,238,250,288,264,251,250,281,270,279,241,281,292,229,251,257,262,249,285,275,221,272],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":183729,"first_positive":53,"success":true,"coordinate":"0x136a479b","pair_sha256":"1a550fb76906946679ea7a99289213a4a086a716f933f98b3423e564ec7a43a0","cpu_s":25.9}
{"k":38,"file_sha256":"ecb36361dcc89e1d4e7e6fb6533372fea70268e2d5ff6187831c8bef16e93dee","candidates":2,"rounds":[{"c":1,"j":19,"DF":54,"advice_sha256_16":"b88715e46286f374","bprime_wk":142182257663,"attempts":136,"accepted":96,"kept":true}],"spaces":10,"passes":[228,255,257,267,274,272,263,258,259,250],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":143571,"first_positive":10,"success":true,"coordinate":"0x4fcaba49","pair_sha256":"63b8222073c805c9b00d99c87372473aa5e7f99635d8017e538fd70bf3aada45","cpu_s":219.5}
{"k":39,"file_sha256":"d8f4c15c64359426ed5a58bab2ac17a4f3a02f9092bde341902cae4e996d13ce","candidates":1,"rounds":[{"c":0,"j":7,"DF":40,"advice_sha256_16":"f44365f8536ce4d4","bprime_wk":20177747396,"attempts":242,"accepted":96,"kept":true}],"spaces":18,"passes":[258,279,245,251,254,287,270,214,248,244,258,253,253,229,248,248,254,258],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":180978,"first_positive":18,"success":true,"coordinate":"0xefa3368e","pair_sha256":"7e87c7aade0e30bc840322cd6d6142beaa6a038f7b09bcd1c90e74f61815e86f","cpu_s":20.1}
{"k":40,"file_sha256":"be0478e710916bc13886aa6eb5630fece8432ca32d5349e649dbba087f293fda","candidates":6,"rounds":[{"c":5,"j":60,"DF":59,"advice_sha256_16":"5ad68acd639f683c","bprime_wk":541898590494,"attempts":200,"accepted":96,"kept":true}],"spaces":34,"passes":[255,257,307,272,247,251,217,273,267,255,266,245,268,287,233,261,259,262,280,234,259,277,241,274,275,250,251,226,241,236,267,289,251,251],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":177677,"first_positive":34,"success":true,"coordinate":"0x4ef55bf4","pair_sha256":"78871e4218d3c3ae5b5c5da555ec1e3870fdbf4bb8b202529f3c27d4b83c22a5","cpu_s":180.4}
{"k":41,"file_sha256":"6bf0cd8306d133048f6cc718af29d3db9863b06b02b1ce1c5d5f890e72a4cd7d","candidates":1,"rounds":[{"c":0,"j":46,"DF":46,"advice_sha256_16":"94f6adda90602420","bprime_wk":79341484558,"attempts":349,"accepted":96,"kept":true}],"spaces":1,"passes":[285],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":189224,"first_positive":1,"success":true,"coordinate":"0xed7a8466","pair_sha256":"0b1dab5303216b4e1dae1ebab0660c544e82ea3656448db078cef4c5f548787d","cpu_s":36.1}
{"k":42,"file_sha256":"50cab7b8eb8eb41316b60cf485549c200012bc9c2e40d5e35c09d4936cd88afe","candidates":1,"rounds":[{"c":0,"j":3,"DF":41,"advice_sha256_16":"16eea1c45f2d5de2","bprime_wk":13145128283,"attempts":191,"accepted":96,"kept":true}],"spaces":2,"passes":[234,245],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":149231,"first_positive":2,"success":true,"coordinate":"0x87fe5ef6","pair_sha256":"fe9113444fa950bdf11f59993ff2b46744c1d1d35e7c2acd1a3f8cdb798f5e78","cpu_s":10.9}
{"k":43,"file_sha256":"2adb605a1e4b4298b6c4a8c6f36f3c5a7cb1b03a2f2c2ff741209989d6c99c98","candidates":1,"rounds":[{"c":0,"j":4,"DF":35,"advice_sha256_16":"ef3d7a787676e3c5","bprime_wk":17261581360,"attempts":96,"accepted":96,"kept":true}],"spaces":13,"passes":[281,270,232,269,242,260,240,246,275,240,236,261,232],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":171725,"first_positive":13,"success":true,"coordinate":"0xb113a784","pair_sha256":"5fc8460f157b99ad344f84adf0fb72dbe0c6bfe3acaf97c480f9c6801c0dd042","cpu_s":12.4}
{"k":44,"file_sha256":"b0ee344f4897ff153b97c82e8739892a06965dcdf89c5887e0ddee25f15e4a65","candidates":5,"rounds":[{"c":4,"j":2,"DF":53,"advice_sha256_16":"4f6dc8abb4410242","bprime_wk":375519444704,"attempts":117,"accepted":96,"kept":true}],"spaces":1,"passes":[248],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":158889,"first_positive":1,"success":true,"coordinate":"0xca7141d7","pair_sha256":"d85549a7777e2b6ed4d8d94cf02fd418dbbca9b5f0b6925425594c9b4df2f321","cpu_s":268.6}
{"k":45,"file_sha256":"0937e7a81ef8afd205ff8692b88c63a11788b72d1340b053e0bfa26f0a6c58b0","candidates":2,"rounds":[{"c":1,"j":28,"DF":37,"advice_sha256_16":"61673a9db5e52775","bprime_wk":152553772122,"attempts":182,"accepted":96,"kept":true}],"spaces":1,"passes":[260],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":165802,"first_positive":1,"success":true,"coordinate":"0xbd1a064f","pair_sha256":"6657af21acd6e0daa465748e5e80cb3113c081ad2b2d7a310739276ce148f651","cpu_s":221.0}
{"k":46,"file_sha256":"ebe8889cbc4040971cce416996135bf322ffb4752e672e7793547ee72dc802e8","candidates":5,"rounds":[{"c":4,"j":25,"DF":38,"advice_sha256_16":"a5133030b527d4ff","bprime_wk":406851160974,"attempts":96,"accepted":96,"kept":true}],"spaces":23,"passes":[291,263,255,246,252,244,267,237,285,264,264,257,236,253,261,265,278,221,265,259,256,285,250],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":181510,"first_positive":23,"success":true,"coordinate":"0xd8e38715","pair_sha256":"15235ad44a92e2254f850e81263fddd2d41779f2b387648fddee6baff5099aba","cpu_s":560.8}
{"k":47,"file_sha256":"1cd3fa50765d74708f4a195bac3cf1dda7bc9c53579b2c960568f0771727ab6a","candidates":6,"rounds":[{"c":4,"j":2,"DF":34,"advice_sha256_16":"f23cf80cb8fe925b","bprime_wk":379453154095,"attempts":2048,"accepted":1,"kept":false},{"c":5,"j":18,"DF":57,"advice_sha256_16":"a0c0d48e3d81f87a","bprime_wk":43936069583,"attempts":173,"accepted":96,"kept":true}],"spaces":6,"passes":[232,241,252,240,266,277],"selfcheck_ok":true,"s2cap_bound":false,"max_attempt_work":180855,"first_positive":6,"success":true,"coordinate":"0x1ac2c743","pair_sha256":"1d72f7077eae20ca917e06d585cb803859012e17a2917a9468d7068b719e6315","cpu_s":599.2}
```

## Appendix E. The R6 study: plan, commit record, driver, analysis, launcher and per-run ledger (verbatim)

plan.txt:

```text
Pre-registration R6 for hashsmash sha3-256-r5 (v15). Written before any run of R6. Its SHA-256 and UTC time are
recorded in commit.txt together with the SHA-256 of every file it names.

Purpose: measure, end to end and independently of v14's R5 study, the success probability over the algorithm's own
coins of the v15 algorithm. v15 is v14's algorithm (B' with B_BUDGET = 2^32 units and CCAP = 2^26 units, no attempt
limit per candidate, DMIN = 33, unweighted D2u; connector X_MAX = 2^23; driver K = 96, A_ADV = 2^11, A_MAX = 2^13;
stage 2 with S2CAP = 2^24) with two phases replaced by programs that compute the same outputs:
- P: T3 by meet-in-the-middle on zero blocks of alpha2 (mitm2.c). Its native run (before this plan) certified the
  trail of v14's proof Section 3 (w1 = 127, w2 = 24, core 17 of T2's order) at its level of 64 blocks. P is
  deterministic, so every run uses that trail (constants ALPHA3_BITS and BETA2 of the experiment file).
- E: stage 1 is the bitsliced degree-4 fast exhaustive search, exactly the function computed by fes.c (the binary
  fes, built from fes.c with clang -O3), followed by stage 2 by complete 5-round digests in fes's output order, at
  most S2CAP pairs per space.
B', S, the connector and the driver are the code of r5v14.py (byte-identical to v14's experiments/r5.py), called
by r6run.py in algorithm()'s order.

Runs: k = 0..47, label "hashsmash sha3-256-r5 R6 run <k>"; all coins are derived from the label exactly as
algorithm(label) does. Each run is `python3 r6run.py "<label>" results/<k>.json`; launcher run_all.py (at most 5
runs at a time, nice 10, increasing k). Every run is reported. No run is stopped, excluded or repeated. A run that
exits abnormally, or whose result file is missing or malformed, counts as a failure.

Analysis (analyze.py, fixed now): a run succeeds iff it outputs two distinct 135-byte messages with equal complete
5-round SHA3-256 digests, checked with the experiment file's digest and with the organizer verifier
(organizer_keccak.py = verifier/keccak.py, sha3_256(m, 5)). Report the count x of 48 and the one-sided 95%
Clopper-Pearson lower bound. Claim rule: the v15 package may claim success probability 0.40 on R6 if the bound is
at least 0.40 (x >= 26); otherwise R6 supports no claim and that is reported. No rule changes any constant of the
algorithm. R5 (v14's study) is reported beside R6 as separate evidence; the two are not pooled for the bound.

Self-test made before this plan (not part of R6, no new outcome): r6run.py on the label of R5 run 4 reproduced
R5's logged advice (c = 3, j = 37, DF 41, advice hash 990540e7f5ee7f2e) and the logged collision at space 1,
coordinate 809f225b.
```

commit.txt (SHA-256 446a29920246ac5c796fb510aa7447765b6841ed4b43d9e5887e473e430329c2):

```text
R6 commit record
utc 2026-10-08T00:19:33Z
9c7659c3acf661348f3d8e031cb28bb16bc309614f0a9763cdb9a2e4c22e5e7c  plan.txt
0ae6ea6628e27337a06d12076746442ca3638b48cc44a1318dba6c25d11c143f  r6run.py
0be4334dfc215f181b8cae5332c87551971bbd60617c28b0f50e18737e9d7ef4  r5v14.py
9a023ce614609bb9c27ba94683a6dc340f7a1324a3550ca4ba3f45775ae30de4  fes.c
93eff750b3529c2d54a48f5368f6c19f3d8ff70b935cbf380d13b4b564199a86  fes
7a2ba2db66cf57ec664c623af8ed922067829d3f2a25c850d8d2f6a842b47d7f  mitm2.c
e31fcfd247866de2993f01c7c95b23e6ccd52d6ea65c7e3e49070188114a0862  analyze.py
56d9360b3f6d28e74d227a910e1f92be689c7caf10b5ee34f75987ac9d198e46  run_all.py
95ce77dff0476301c05057e01296f3e3507c4926423257540cfc3e5fd36ee0ae  organizer_keccak.py
```

r6run.py:

```python
"""R6 driver: one complete run of the v15 algorithm with label-derived coins (plan.txt).
Usage: python3 r6run.py <label> <outfile.json>
Calls, in algorithm()'s order, the experiment file's bprime, Setup, attempt and enum_basis; E on a space is the
binary fes (exact stage 1 over the 2^32 window; Appendix B) followed by stage 2 (complete 5-round digests of both
messages, in fes's output order, at most S2CAP pairs).  P's output is the trail of proof Section 3 (the output of
the MITM trail search, certified by its run).  The run stops at its first output."""
import sys, json, time, subprocess, hashlib, resource
sys.setrecursionlimit(100000)
import r5v14 as R

FES = "./fes"

def e_space(info, st):
    v0, basis = R.enum_basis(info["EM"], info["beta0"], 32)
    lines = [" ".join("%016x" % w for w in R.lanes(v)) for v in [v0] + basis]
    p = subprocess.run([FES], input="\n".join(lines) + "\n", capture_output=True, text=True)
    out = p.stdout.split("\n")
    summ = [l for l in out if l.startswith("summary")]
    passes = [int(l.split()[1], 16) for l in out if l.startswith("pass ")]
    ok = p.returncode == 0 and len(summ) == 1 and "selfcheck=ok" in summ[0]
    found = None
    for n, c in enumerate(passes):
        if n >= R.S2CAP:
            break
        x = v0
        for j in range(32):
            if (c >> j) & 1:
                x ^= basis[j]
        A, B = R.Linv_map(x), R.Linv_map(x ^ info["beta0"])
        if R.digest5(A) == R.digest5(B):
            found = (c, R.message(A).hex(), R.message(B).hex())
            break
    return ok, len(passes), found

def run(label):
    t0 = time.time()
    rec = {"label": label.decode(), "rounds": [], "spaces": [], "result": None}
    base, OB = R.Base(R.ALPHA3_BITS, R.BETA2), R.own_bits()
    left, c, att = R.B_BUDGET, 0, 0
    while att < R.A_MAX:
        h = R.WK.cost()
        r = R.bprime(base, OB, label, left, None, c)
        if r is None:
            rec["result"] = "bprime-budget"
            return rec
        left -= R.WK.cost() - h
        rd = {"c": r[2], "j": r[3], "DF": r[4], "bp_units": (R.WK.cost() - h) / 1355,
              "advice": hashlib.sha256((hex(r[0]) + hex(r[1])).encode()).hexdigest()[:16], "status": ""}
        c = r[2] + 1
        st = R.Setup(base, r[0], r[1])
        spaces = []
        for i in range(R.A_ADV):
            att += 1
            status, info = R.attempt(st, R.Coins(R.run_seed(label + b"conn" + c.to_bytes(4, "little"), i)))
            rd["status"] += "A" if status == "ok" else str(R.STATUS[status])
            rd["max_xors"] = max(rd.get("max_xors", 0), info["xors"])
            if status == "ok":
                spaces.append(info)
            if len(spaces) == R.K_SPACES or att == R.A_MAX:
                break
        rd["accepted"] = len(spaces)
        rec["rounds"].append(rd)
        if len(spaces) == R.K_SPACES:
            for k, info in enumerate(spaces):
                ok, npass, found = e_space(info, st)
                rec["spaces"].append({"k": k, "DF": info["DF"], "selfcheck": ok, "passes": npass,
                                      "hit": found is not None})
                if not ok:
                    rec["result"] = "selfcheck-fail"
                    return rec
                if found:
                    rec["result"] = "collision"
                    rec["output"] = {"space": k + 1, "coord": "%08x" % found[0], "m1": found[1], "m2": found[2]}
                    return rec
            rec["result"] = "none-in-K"
            return rec
    rec["result"] = "a_max"
    return rec

if __name__ == "__main__":
    label = sys.argv[1].encode()
    t0 = time.time()
    rec = run(label)
    ru = resource.getrusage(resource.RUSAGE_SELF)
    ruc = resource.getrusage(resource.RUSAGE_CHILDREN)
    rec["cpu_python_s"] = ru.ru_utime + ru.ru_stime
    rec["cpu_fes_s"] = ruc.ru_utime + ruc.ru_stime
    rec["wall_s"] = time.time() - t0
    rec["wk_units_total"] = R.WK.cost() / 1355
    json.dump(rec, open(sys.argv[2], "w"), indent=1)
    print(rec["result"], rec.get("output", {}).get("space"))
```

analyze.py:

```python
"""R6 analysis (fixed in the plan): reads results/k.json for k = 0..47; a run succeeds iff its result is
"collision" and both messages are distinct 135-byte strings with equal complete 5-round SHA3-256 digests
(rechecked here with the experiment file's digest).  Missing or malformed result files count as failures.
Prints the count, the one-sided 95% Clopper-Pearson lower bound and the claim rule's outcome."""
import json, math, sys
sys.setrecursionlimit(10000)
import r5v14 as R
import organizer_keccak

def cp_lower(x, n):
    lo, hi = 0.0, 1.0
    for _ in range(100):
        m = (lo + hi) / 2
        if sum(math.comb(n, i) * m ** i * (1 - m) ** (n - i) for i in range(x, n + 1)) < 0.05:
            lo = m
        else:
            hi = m
    return lo

def ok(rec):
    if rec.get("result") != "collision":
        return False
    a, b = bytes.fromhex(rec["output"]["m1"]), bytes.fromhex(rec["output"]["m2"])
    def dig(m):
        return R.digest5(int.from_bytes(m + b"\x86" + bytes(64), "little"))
    return (len(a) == len(b) == 135 and a != b and dig(a) == dig(b)
            and organizer_keccak.sha3_256(a, 5) == organizer_keccak.sha3_256(b, 5))

rows, succ = [], 0
for k in range(48):
    try:
        rec = json.load(open("results/%d.json" % k))
        s = ok(rec)
    except Exception:
        rec, s = {}, False
    succ += s
    rows.append({"k": k, "success": s, "result": rec.get("result"), "space": rec.get("output", {}).get("space")})
lb = cp_lower(succ, 48)
out = {"runs": 48, "successes": succ, "cp95_lower": lb, "claim_0.40_supported": lb >= 0.40, "rows": rows}
json.dump(out, open("analysis.json", "w"), indent=1)
print(succ, "of 48; one-sided 95% CP lower bound", round(lb, 4), "; claim 0.40 supported:", lb >= 0.40)
```

run_all.py:

```python
"""R6 launcher (fixed in the plan): runs k = 0..47 in increasing k, at most 5 at a time, each as
nice -n 10 python3 r6run.py "hashsmash sha3-256-r5 R6 run <k>" results/<k>.json, stdout/stderr to logs/<k>.*.
No run is stopped, excluded or repeated."""
import subprocess, os, time
os.makedirs("results", exist_ok=True); os.makedirs("logs", exist_ok=True)
procs, k = {}, 0
log = open("launch.log", "a")
while k < 48 or procs:
    while k < 48 and len(procs) < 5:
        o, e = open("logs/%d.out" % k, "w"), open("logs/%d.err" % k, "w")
        procs[k] = subprocess.Popen(["nice", "-n", "10", "python3", "r6run.py", "hashsmash sha3-256-r5 R6 run %d" % k,
                                     "results/%d.json" % k], stdout=o, stderr=e)
        log.write("%s start %d\n" % (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), k)); log.flush()
        k += 1
    for j, p in list(procs.items()):
        if p.poll() is not None:
            log.write("%s end %d rc %d\n" % (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), j, p.returncode)); log.flush()
            del procs[j]
    time.sleep(2)
log.write("%s all done\n" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
```

Per-run ledger (k, result, output coordinate, SHA-256 of results/k.json); launch.log SHA-256 ed8292923f2d931bbb6724ecc20e2da3b39c4ef2374e0591709e430bc37dbf17; analysis.json SHA-256 35c979811047ee5fea6d2759d6abce254f68e72b95f4fbe5ba138cba9a15d162:

```text
0 none-in-K - a84aa30d96d1ab023bf1301ad4db1a4529845ff64bb3e85a1ef342c36a07921d
1 collision 733dc3d4 4822c1e11f5d860c605c78d1ed8268af5e74c259fd2d08c50f7c0cb4b9b333fb
2 collision aeb1ace2 f6e72cd110cb40b604f6aad02dc36a3e30bdc5b3caa833252e7659ea5ab235ae
3 collision 9f192bb6 a15c38ff624fc3f984cd7f3f927ae0e042dc5d945a5e3e2ea2639d9ff711592f
4 collision f3dd4cdf 5da9c63bebd6f9d0cc32f9297480b7809d00baaa8ed951c498b22555576367c0
5 collision b6021820 f627e11d04843d740b78bc4e125f9e7d6068d0c1281bfd27f5cb7ede8e62c72a
6 collision 5aa44394 6422e511b00a7f403327acc9d73d19e5ed77a33ddddc6d40a5922fd11095da70
7 collision 22221082 6f1f8c87c08d5350fc5e2060a2cc8823514a81d0fd36c97b281ad2afb46f3247
8 collision da6e0cfe 57c6a567d71757c6f9e48d1c175a5c4e40835eddd8985b5bc9fc1ece28b07027
9 collision c3d64ae2 465d6491e7fa4d47b5609c8104706a3e673a560f209895376142fb0e8d7489e1
10 collision c3a04f0c 36a4fb52888dea117082866811769db82ac48bff28a251e215ed492571eab1eb
11 collision ca1e3e01 43c320a866b4d99d039123953cc3b61139b78d696b83f95112db767d0bbc4bf5
12 collision 41ec9bbd a5b3165e10b69720cae193defbb383392bdae3c5133bc2fd7ce184e296b8b35d
13 collision 2d49b6a5 f2851e658c987b43ac9f731c6d5533616ba3ca3b412ce843c0285100bdc7c232
14 collision f49e4560 4e8690c39fb4f2b2bc218ee2cb790a19bb21e5395672113eb9a6a56e5d4946fb
15 collision 379f9b2a 19d10cb1c934a2da246de55675d4dd19346ab8c0a87add109484ea6af83e80a5
16 collision f5736e5f bbb5f7760d562bb75f770b254dbceea42a2b72cf3dc4c47debfe5cbaf0cccb92
17 collision 0e5db5e4 e23da358f7f85478a8c822ba8fe4c7a76c222b51e5f14c0d6f9ebd9a8ac07d8c
18 collision 792508e9 f82e1453ff943062b065a973d33ff12fbfc4fbd96592b0ab2109aba6f0f3c5e4
19 collision 6715b085 4b20e9084e4d2baab807c2f988f30e2267a3cae8a29cb53668608c87a490e1fa
20 collision 96f56a4d 3dbc0a07659f1dbffd2332a04c129ab75036bb69fe6a049f49bc17c44c08c349
21 collision c577495b 69228c4addd403a5ede7dcc98698ce3e87685f544701846d074803904bc90be6
22 collision c3d944ad e50ea677268ec276d6c4172a94a547cf2a44392da23eee068aecc06182128748
23 collision ebc5894d 2814d456fcc74d59733c10bbd0e2e0482ed479e6c0c0b6a0864943bf4001bc73
24 collision d2801e58 2400fa1caab6f627fe892f65d2bff41119c1ee012b62b30ddd8c6c1f2c7d019b
25 collision 0fa14f06 aacff4de352af232ea5e1ba8076afdc08680d02dfc5e03f9573b452ca0879fc0
26 collision 5fafb237 3426eb60dbdc80aba79890ebc47c4d4b47dd28fb603991f4951c4ece76bf4192
27 collision 2f03107c ffa8c593d26a2e5c291f8094b8739e4b5f4471dab8d94ebb610ad73a7282d46d
28 collision 69da8cfa 465e78731bb2c76379eac7daa2d23788386b54bcdf0e31c06976e811d81ae1c9
29 none-in-K - 84d54cde2c744b9b46d091ccd2ecc161d44215eba47e83e2cddde4179e2d6064
30 none-in-K - 04a599c4a533d4c91af9ff90c739849e29b919a3070988b615842b4517c99570
31 collision 40b61df1 87ec1f75f0acd2fde9f4fe24ff6800bf96e8a7a8f2021625ab0e81e2f6d9ac5d
32 collision 96e0a49f a0ce8908b0ccbeb9b241ca1ed34826875e1d38695120a4f3816d0bf79b780ed4
33 collision 30fda680 6ded5e58002d359459eba1c1b89478b737a6e75277743d145b41d3ec5e1ed104
34 collision 53086d2a ce1936749fc79c9d485013183afa97358d484a05fbd477b4435f9d76b699efcb
35 collision a8b48eb3 3a12557a5fbb1d930e8039a821a40768e7d816950e8ebd0352e7d196678cf86e
36 collision 2a9b0523 4b0193e32bfebbdbcec5a37b8a14b21a16f0c5235a56cf54afeea619dcfd6e43
37 collision 954a987d 7446e4a27da48f7e0b915d2ebfef66a9fafcb71cead658198f3e52a1cbe83f8a
38 collision fe494614 2eed0cfb3b02877846222df370835b64c844cf8624343ed71602161fca9c0085
39 collision b71c6547 824cd748b618223bf9df7525f8304e12a7d4dd3e86aa9fca07c7d2467ad83e8e
40 collision ab9e046c bd645536e56b7bff5f84afe4416a7954cebc5e624f3f0c8b6ff225bf46fde04c
41 collision a16efce5 fea81d90d21e8fb4f686fae3cfb8db4aca1be5a3fd13171a8e96d0c49282ece1
42 collision 4fe16868 f83afb2240ac0b729e41c4ccc9f7e379f85ba5506f6d433f258edf1fc48134b7
43 collision 9cd474ef c847e451ed83ac182a1c3f8982d94f442d65281695a010ba2af8e2dcef210857
44 collision 41cc1562 5bfb4a18fcb69808421a8492175acfe2674f83b3d63b2da62f19f97d858444f3
45 none-in-K - 5e286c1d122053a5ba1c416a44cfbc36ce33364df323a312dd87c2ccbd5bd558
46 collision 30e8e5e2 24701c7cb905fbdecc2c28242d294752e60622ed49caa63841a375f4e67d75e5
47 collision 5056934e 3dbcf6b99075f6e1ed5791d29f01d09347660fbd936a75e1eb1dec623b6bd092
```
