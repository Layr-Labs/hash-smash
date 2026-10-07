# 5-round SHA3-256: every phase inside one capped algorithm, an untuned advice program, its development charged, time 2^37.05

Exploratory claim, with Th0rgal as co-author: Th0rgal 7deb1595 (with Subflatus3 and rubenmarcus) introduced on this
track the zero-advice framing used here. The algorithm runs every phase itself (trail search P, advice program B',
connector, enumeration E). The algorithm's time is a sum of terms, each an exact count or a hard cap times a counted
price. Only the data-dependent counts carry a cap in the code: B''s budget and candidate cap, the connector's work
and attempt caps, E's stage-2 cap and P's cap F_CAP on full evaluations. P's T1 nodes, T2 leaves and T3 batches are
exact counts of a deterministic search, which the organizer recomputes. The algorithm reads nothing published.
Target-specific development is charged as preprocessing: every run whose result fixed, or under its plan could have
changed, a number that the algorithm reads is part of the claimed time (Section 0.1, heuristic H2). [GLL+20] = J.
Guo, G. Liao, G. Liu, M. Liu, K. Qiao, L. Song, "Practical Collision Attacks against Round-Reduced SHA-3", J.
Cryptology 33 (2020), ePrint 2019/147.

## 0. Claim, summary, changes

| Field | Value | Basis |
| --- | --- | --- |
| time_log2 | 37.05 | 2^37.0488, rounded up: the algorithm, 2^35.0558 (Section 6), plus the charged development, 2^35.2782 for the runs that sized K and the caps (G2) and 2^35.9149 for pre-registration C, whose plan could have raised K (Section 0.1) |
| success_probability | 0.40 | >= 0.874: one-sided 95% Clopper-Pearson bound from 46 successes in 48 complete runs of this algorithm (the R5 study, pre-registered; Section 5) |
| preprocessing_log2 | 36.86 | P, B', S and the charged development: 2^36.8544, rounded up |
| memory_log2_bytes | 30 | largest phase about 2^28 bytes (Section 7) |
| nonuniform_advice_log2_bytes | 0 | the algorithm computes its trail and its connector advice; development is charged as preprocessing |

Summary: P finds the trail. Its charge is organizer-recomputed counts times counted worst-case prices. The one count
the organizer cannot recompute at full scale is F, P's number of full evaluations. F enters only through its cap
F_CAP = 2^30, which the code of P checks, and Lemma P bounds it by a logged count 566 times below the cap. B' builds
the connector advice (budget 2^32 units, at most 2^26 units per candidate) with constants that no run chose: no
attempt limit per candidate, DMIN = 33 and unweighted ordering. The v5 connector makes K = 96 affine spaces, and E
tests 2^32 pairs per space at 6,112 counted primitives per 256 pairs. The success probability is measured end to
end on 48 complete runs of this algorithm from pre-registered labels (the R5 study: plan and code hashed before any
run, every run reported; 46 succeed). The premises are that these label-seeded runs behave like runs with fresh
coins (premise R, Section 4.1) and that P outputs the trail of Section 3 within F_CAP (premise P, 2.1); both are
inside H1. H2 states the development ledger (0.1).

What changed from v13 (38.52; review run 37683599756, plausible_not_refuted, no fatal finding) and why. v14 is v13's
algorithm with B''s six tuned constants replaced by values that no run chose. The success evidence is the R5 study
of exactly this algorithm. So B''s tuning runs (A2) fix no number of v14 and are no longer charged; pre-registration
C, whose rule could have raised K, is now charged.

| Review finding on v13 | v14 |
| --- | --- |
| F-COST-PREPROCESS-LEDGER (cost, material): the line between charged and uncharged development is score-dominant, and its premise was in prose, not in claim.heuristics | Declared as H2-development-ledger: the rule, every run with what it fixed, every exclusion with the claim it would give (0.1), and the origin of every number in B' and the connector (0.2) |
| F-EVAL-A2-AUDITABILITY (material): A2's 1,559 CPU-s rests on lost per-process logs | A2's six constants are gone; A2 fixes no number of v14 and enters only as a disclosed sensitivity |
| F-PROB-LEDGER-01, F-EXP-01, F-EVAL-H1-AUDIT-SCOPE (material): the count, the timing and the failures rested on files outside the package; replays never checked a positive space's place in its run | R5's plan and commit record (verbatim) and a per-run ledger with the SHA-256 of every result file are in Appendix D. r5.py holds every run's advice, accepting attempt, space index and connector status string. r5-R-0..9 re-derive 20 seed-picked successes per review from their labels, re-run the accepting attempt and up to 23 seed-picked earlier attempts against the logged statuses (which fixes the space's index <= 96), and return the collisions; r5-bpfull re-runs one whole B' from its label and recomputes 46 of 48 and the bound; 15 R5 collisions are certificates |
| F-P-FULL-SCALE-01, F-EXP-02 (material), F-EVAL-IMPLICIT-PREMISES (minor): P's full-scale premise was not declared | Stated inside H1 as premise P, with its evidence (2.1, Appendix A, r5-count, r5-trail-0..3) and its scope (success only; the cost is capped) |
| F-SUCCESS-EXTRAPOLATION (material): premise R is still needed | Unchanged in kind (4.1). The sentence "distinct labels, so independent" is corrected: under premise R the 48 outcomes are independent Bernoulli(p) draws; distinct labels only give distinct SHAKE-256 streams |
| advisory: K = 96 was kept on C's outcome | C is charged at counted prices (2^35.9149) |
| advisory: "P 2^33.65 units" was rounded down | 2^33.652 |

v13's changes are kept: F_CAP, X_MAX and S2CAP from the rule of 2.6, G2 charged, one end-to-end heuristic with every
other run listed, algorithm() running P with its F_CAP check in plain sight.

### 0.1 Development: what is charged, and why (H2)

Rule. The cost model counts all construction, preprocessing and advice, including any search omitted from the
submitted program. We apply it as follows: every target-specific run whose result fixed a number that the algorithm
reads, or whose plan would have changed such a number on another outcome, is charged as preprocessing, at the counted
prices of the submitted programs (the prices of the claim). Runs that only produced program text, or only measured
the success of the algorithm as submitted, fix no number; they are disclosed with the claim they would give. Where
only CPU time is known, a sensitivity uses 2^38 primitives per core-second (2^27.596 units per CPU-s): above this
machine's peak (at most 10 instructions per cycle under 5 GHz, at most 512 bits, 2 primitives, per scalar or NEON
instruction; we allow 4, giving 2^37.54) and above the measured maximal rates of Keccak-f (2^24.6 units per CPU-s),
SHA-256 (2^26.2) and our fastest 5-round code (2^26.9) (v7's proof, 2.3; v7's ledger states that none of this work
used the GPU or SME). For comparison, B' itself runs at about 2^22 units per CPU-s (r5-bpfull's runs).

Charged:

| Id | Runs | What they fixed | Price | log2 units |
| --- | --- | --- | --- | --- |
| G2 | the v6 run (B' 2^27.12 units by its exact counters, 1,024 connector attempts, E on 512 spaces); pre-registration A (9 B' runs, 2^30.28 units by their exact counters, 9 x 128 attempts); pre-registration B (E on 18 spaces) | K = 96, CCAP = 2^26 units, B_BUDGET = 2^32 units, A_ADV = 2^11, A_MAX = 2^13: v10 chose them from the v6 run's per-space rate and A's candidate costs | each attempt at its cap then (2^18 x 96 + 2^24 + 2^22 primitives), each space at the counted E of 2.4 (bases, setup, 2^24 batches of 6,112, 2^11 stage-2 pairs), each advice's S at 2^31 primitives | 35.2782 |
| C | pre-registration C (2026-10-07, 48 runs of v13's algorithm up to E's first 16 spaces; 4.4) | its plan's rule would have raised K above 96 had its bound been below 0.40; K stayed 96 | B' at its exact WK counts (8,469,642,639,781 primitives, 2^32.54 units), 9,097 attempts at their 2^18 cap, 48 x S, 768 spaces at the counted E | 35.9149 |

Charged development: 2^35.2782 + 2^35.9149 = 2^36.6314 units, all of it preprocessing.

Not charged (each fixes no number of v14):

| Id | Runs | Why nothing is fixed | Claim if charged |
| --- | --- | --- | --- |
| A1 | v7's design study: connector without steering, annealers, backtracking, benchmarks; 10,432 CPU-s | it produced B''s code (the D2u and M2 phases, DSATUR order), which the algorithm executes and is charged for in full every time it runs; no number of B' or the connector comes from it (0.2) | 41.04 (2^38 primitives per core-second) |
| A2 | 75 development processes of B' (2026-10-06, at most 1,559 CPU-s, v7's ledger) | they fixed v13's six B' constants (R = 16, DMIN = 40, KW, MW, LB, PREF); v14 uses none of them (2.2) | 38.74 |
| R5 | the R5 study: 48 runs of v14's algorithm (4.2) | its plan fixed every constant before any run and changes none; its only rule is whether to claim (0.40 if its bound is at least 0.40) | 37.88 (counted prices: B' 2^32.82 units by its exact counters, 15,323 attempts at the X_MAX price, 51 x S, 1,236 spaces at the counted E) |
| C' | a parallel session's runs of the same B' variant (2026-10-07, 14 runs started 16:58:42Z, 4 finished, abandoned; 3 test runs; 4.1) | its plan, hashed at 16:58:33Z before its runs, already fixed the three values "by rule with no run"; its outcomes changed none of them, and it enters no bound | 41.29 (at most 12,537 CPU-s at 2^38 primitives per core-second) |
| D | pre-registration D: completion of C's runs (4.4) | it measured v13's success; no constant | 37.58 |
| A3, A4 | v7's abandoned h23 plan (at most 500 CPU-s); v7's B' run (35.6 CPU-s), whose advice is not used | nothing | 37.87 |
| B | native runs of P: v7's (10,260 CPU-s), pass 1 (7,598 CPU-s) and pass 2 (11,823 CPU-s) of Appendix A | nothing: P computes the same output inside the algorithm and is charged for it there; pass 1's count is the evidence for premise P | 37.42 (each at P's counted price, F at 2^30) |
| G1 | v5 connector runs with the published pair | they used DMIN = 33, which analysis fixes: 33 is the least DF for which E's 32-dimensional window and beta exist (2.4), so no smaller threshold can work and a larger one only rejects spaces that E can use; their 2^18 work cap is replaced by X_MAX from the rule of 2.6 | - |

Everything in this table except A1 and C', at the prices given: 39.51. Pricing G2's 530 spaces at the enumerator they
actually ran (v8's E, 594 primitives per pair) instead of the counted E, which computes the same outputs (Lemma 4):
40.01. The claim stays at or below 38.51 for up to 1,228 CPU-s of further development at 2^38 primitives per
core-second.

### 0.2 Where every number of B' and the connector comes from

B''s code takes as input only P's trail (alpha3, beta2) and the fixed bits F. It reads no output of any development
run. The numbers in B', the connector, the driver and E:

| Number | Where | Origin |
| --- | --- | --- |
| no attempt limit per candidate (B_R = 2^62, never reached); DMIN = 33; D2u weights KW = MW = LB = PREF = 1 | B' | no run: a candidate ends at its first accepted attempt or at its cap; 33 is the connector's DMIN (G1 row above); weight 1 is the unweighted order. Written as "fixed by rule with no run" in C''s plan (16:58:33Z) and again in R5's plan (20:27:28Z), both before any of their runs |
| CCAP = 2^26 units, B_BUDGET = 2^32 units | B' | G2 (charged) |
| least-weight input difference per row of alpha2 (largest DDT entry) | B' | analysis: it gives the least weight of beta1 -> alpha2 (127) |
| WT[d] = 5 - log2 max DDT[d]; COST = WT + linearisation loss; M2 orders by 5 - log2 abs(W), then by the rank added | B' | analysis: the number of affine equations that each choice adds |
| affine-set dimensions 2, 1, 0, largest first | B', connector | structure: every affine subset of a row's 5-bit value set that the DDT allows |
| 64 sampled points in B''s verify | B' | a self-check of the produced space. No check failed in any R5 run (all 51 attempts that reached DF >= 33 passed it), so any positive number gives the same runs; its cost is counted in WK |
| K = 96, A_ADV = 2^11, A_MAX = 2^13 | driver | G2 (charged); K kept by C's rule (charged) |
| connector DMIN = 33 | connector | analysis: the least DF for which E's window and beta exist, so the least threshold that can work (G1's runs used it) |
| X_MAX = 2^23, S2CAP = 2^24, F_CAP = 2^30 | connector, E, P | the rule of 2.6, no run |
| 32-dimensional window (2^32 pairs per space) | E | v3's design by analysis: 2^32 x p_M = 2^32 x 2^-37.22 gives s = 0.0265 per space |
| E's batch layout (6,112 per batch), T3's batch layout and every counted price | E, P | counting, no run |
| cores of at most 10 bits; order by least w1, then w2 | P | [GLL+20] and in-kernel trail practice (KeccakTools); v8's threshold rule (2.1) |
| 256-bit coin words from 4,096-byte SHAKE-256 blocks | Coins | implementation of fresh words for reproducible runs; the claimed algorithm draws fresh words |

So the only target-specific machine work that shaped the program and is not charged is A1, which produced code, not
a number. R5 measures this code's success with constants that no run chose: 46 of 48, the same count as v13's tuned
B' in C and D.

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

### 2.1 Trail search P (deterministic; exact counts x counted prices)

P outputs the 2-round in-kernel core alpha3 and the beta2 that minimise w1.

T1 (cores), unchanged: a candidate alpha3 is a set of at most 10 bits whose alpha-columns and beta-columns (columns of
pi o rho of each bit) all hold an even number of bits; depth-first search from bit (lane, z = 0) for each of the 25
lanes; at a node let c be the smallest odd alpha-column, else the smallest odd beta-column; if none, record the core in
canonical form (least sorted bit list over the 64 z-translations), else, below 10 bits, branch on each bit of c not
yet in the set. N1 = 8,674,833 nodes, 1741 cores. Price: 2^12 per node (as in v8: at most 2^9 per node outside the
17,100 core events, a core event at most 2^15, and N1 x 2^9 + 17,100 x 2^15 < N1 x 2^12).

T2 (forward): for each core, beta3 = pi o rho(alpha3); the C1 leaves alpha4 compatible with beta3 are visited in
reflected mixed-radix Gray order (Knuth's Algorithm H over the rows of beta3); the 64 digest-plane rows of L(alpha4)
are kept as 32 row pairs (10-bit fields of 2 words) and updated by XOR. A leaf is allowed iff every digest-plane row q
has DDT[q][0] + DDT[q][16] > 0 (32 lookups of one 1024-entry table); the core is kept iff some leaf is allowed, which
is P45 > 0 (every term of P45 is >= 0; Section 3). C1 = 1,639,088,128 leaves; 467 kept cores. Counted price (r5-count):
166 primitives per leaf on its longest path (132 for a kept leaf, 34 for the longest Gray step; leaf counter
tested against C1).

T3 (backward, in batches). For each kept core, in T2 order, the beta2 compatible with alpha3 (C2 =
1,379,275,399,350 leaves in all) are visited in batches. With m_j the fan-in of row j of alpha3 (rows in (y, z)
order, input differences ascending), rows 0..k-1 in full and g values of row k are the slots of a batch (k, g largest
with m_0...m_{k-1} g <= 256; 243 slots for the 9-fan-in cores); row k's values fall into G = ceil(m_k / g) groups; the
outer rows k+1..n-1 run in Algorithm H order, the group slowest. That makes 5,679,328,446 batches in 1411 groups
(r5-trail-0..3 recompute both). Per group (a bound, not counted: 2^27 primitives; each of the 107 x 2^15 table
indices takes 11 primitives for both tables, 3 loads, 6 operations and 2 stores, 2^25.2 in all, and the
transposition and ACT less than 2^20): the slots' alpha2 contributions transposed into 1600 words (bit p = slot p), ACT[r][v] = the activity word of
row r of alpha2 when the base row value is v, and for each triple of rows t (rows 3t..3t+2, t < 106; rows 318, 319)
two tables TS[t], TC[t] of 2^15 words: bit p is bit 0, resp. bit 1, of the number of active rows of the triple in
slot p. A batch (t3_batch in r5.py, counted):

- batch counter, tested against the exact count 5,679,328,446 (cap constants are instruction fields); tau = floor(T /
  2), T the least w1 found so far (over all cores);
- for each of the 107 triples, its 15-bit field of the 7 packed base words selects TS[t], TC[t] (two loads); full
  adders (5 primitives each) give AS, the number of active rows of alpha2, in bitsliced binary (9 words); pass = the
  valid slots with AS <= tau (comparison with the bits of tau, at most 74 primitives);
- every slot in pass is evaluated in full (w1, w2, lexicographic update of the best; counter capped at F_CAP = 2^30;
  a bound, not counted: at most 2^13 primitives each for its 7 packed words, 107 triple-weight lookups, w2 from the
  selection and the comparison);
- the Gray step of Algorithm H (memory arrays, 7 delta loads and XORs).

A leaf is evaluated in full iff 2 AS(alpha2) <= T, which is v8's rule, with T read at the start of each batch; so T3
outputs the exact minimum (least w1, then w2, then the choice vector, then the earlier core). Counted price: 1,583
primitives per batch, charged on every batch: the batch is straight-line code except the comparison, and its longest
path, 1,539 at tau = 0, is measured by r5-count over all 513 tau classes; the Gray step's longest branch is 44.
Registers: at most 34 in a batch (the 7 base words, at most two pending words per weight level, tau, temporaries).

P in the experiment file (new in v11). trail_search() is P's driver and algorithm() calls it first: T1 is lane_dfs
over the 25 lanes, T2 keeps the cores with p45pos (P45 > 0), in T1's sorted order, and T3 is t3_core per kept core
from the running minimum T of the earlier cores. t3_core takes exactly the decisions of the batch program (same
batches, slots, threshold B = min(T, best w1 of the core) read at the batch start, rule 2 AS <= B, order (w1, w2,
choice vector), earlier core on ties); it computes AS with plain integer code where t3_batch is the counted
bitsliced form (as e_window is to e_batch). Its full-evaluation counter carries the cap in plain sight:

```python
F[0] += 1
if F[0] > fcap:
  raise CapReached()
```

with fcap = F_CAP = 2^30 in algorithm() (2.6); CapReached makes algorithm() return without output. Base(a3b, b2) is built
from P's output (the experiments use P's logged output, the constants ALPHA3_BITS and BETA2 of Section 3).
Premise P (inside H1; it concerns success only, since every cost term of P is an exact count or a cap): P outputs
the trail of Section 3 within F_CAP. Its evidence is the rest of this section, Appendix A, r5-count trials 24-27 and
r5-trail-0..3.

Counts of T3. Every count in P's charge except F is recomputed by the organizer (batches and groups by r5-trail-0..3,
prices by r5-count). F depends on T3's decisions and enters only through F_CAP. Native runs (trail3b, Appendix A)
went over all 5,679,328,446 batches twice. Pass 1 runs every core from T = infinity and gives each core's exact
minimum (the global minimum 127 is core No. 349, the 18th kept core) with F = 1,896,302. Pass 2 runs core i from T =
the minimum over the cores before it, which is exactly the algorithm's T, and counts F = 770. Both passes output the
trail of Section 3 (w1 = 127, w2 = 24, unique).

Lemma P (pass 1 bounds the algorithm's F). Within a core, both runs visit the same batches and slots in the same
order; let B_alg and B_1 be the thresholds at a batch start (B_1 = the least w1 evaluated so far in the core, B_alg =
min(T, the same for the algorithm)). Then B_alg <= B_1 at every batch, so the algorithm evaluates a subset of the
slots that pass 1 evaluates (a slot is evaluated iff 2 AS <= B), and F_alg <= 1,896,302 for any order of the cores.
Proof: every active row of alpha2 costs at least 2 (no nonzero chi5 DDT entry exceeds 8 of 32), so w1(slot) >= 2
AS(slot). Let the slot w* give B_1. If the algorithm evaluated w*, B_alg <= w1(w*) = B_1. If not, then 2 AS(w*) >
B_alg at w*'s batch, and B_alg never increases, so now B_alg < 2 AS(w*) <= w1(w*) = B_1. Before any evaluation, B_1 =
infinity. So the premise on F rests on pass 1's count, 566 times below F_CAP.

trail3b has no cap check; with 770 evaluations against a cap of 1,073,741,824 a check could not have acted. Organizer
check of the same decisions on sub-problems (r5-count trials 24-27, executing the algorithm's t3_core and
trail_search): core No. 1136 from T = 2^30 gives (w1, w2, choice) = (372, 18, 2.4.7.0.4.0) with
F = 517, and from T = 127 no evaluation, exactly the native pass-1 and pass-2 lines; trail_search on the sub-problem
[core 874, core 1136] outputs core 874's native pass-1 trail (w1 = 320, w2 = 23, same beta2) with F = 425; with the cap
lowered to 100, t3_core raises CapReached at F = 101. Deterministic premise (not a probability; the earliest one in
the success argument): P outputs the trail of Section 3 with F <= F_CAP = 1,073,741,824 (566 times pass 1's bound,
1,394,469 times pass 2's count). The organizer cannot re-run the whole minimisation (1.4 x 10^12 leaves); Appendix A gives the
commands, sources, CPU times and the SHA-256 of both per-core logs, and Section 3 checks w1 = 127. If F exceeded
F_CAP, P would stop without output: the cost bound holds either way.

P's charge: T1 + T2 + T3 batches + full evaluations at F_CAP + group setup + setup (DDT, L^-1 by elimination,
per-core tables: below 2^31) = 18,285,619,395,298 primitives = 2^33.652 units. No factor 2: every count is exact and
organizer-recomputed or a cap, and every price is the longest counted path or a stated bound.

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
consistent and DF = 1600 - rank(E_M) >= 33; above X_MAX = 2^23 work units (2.6) the attempt fails. An attempt costs at
most 2^29.62 primitives (2^23 x 96 + 2^15 coin words x 2^9 + 2^22) and draws at most 22,150 coin words.

Advice rounds (v10 caps): run attempts on the current advice until K = 96 are accepted; if A_ADV = 2^11 attempts give
fewer, discard it and resume B' at its next candidate. At most A_MAX = 2^13 attempts in all, so at most 4 advice
rounds.

### 2.4 Enumeration E (bitsliced, counted)

Space and window (unchanged): V = solutions of E_M, beta = beta0; offset v0 = the solution with all free variables 0;
b_i = (solution with free variable i set) + v0, kept if independent of beta and the earlier ones; W = span of the first
32 kept b_i. E tests the 2^32 pairs (x, x + beta), x in v0 + W.

Batches: coordinates 8..31 of x run in Gray order over 2^24 batches; within a batch the 256 values of coordinates 0..7
are the 256 bit positions of every word (pair p of the batch has x = base + sum over j < 8 with bit j of p of b_j).

Per space (e_setup, at most 2^24 primitives): Pat (1600 words: bit p of word i is bit i of the inner part of pair p);
round-0 tables TP[z][h][v] (16 words) for the row pairs (2h, z), (2h+1, z), h = 0, 1, and base row values v (10 bits):
the 5 words of chi(row 2h) + chi(row 2h+1), then the 5 + 5 words of each row (iota included), and T4[z][v] (row (4,
z)); the base and b_8..b_31 packed as three 16-bit fields per slice z (12 words).

Stage 1 of a batch (e_batch, counted): pass 1, slice by slice (slice 63 first for its parities): three field
extractions and 15 table loads give the parity words P01, P23 and the row-4 words; C[x][z] = P01 + P23 + a4 (the column
parities of the round-0 output a); D[x][z] = C[x-1][z] + C[x+1][z-1]; for each of the 659 bits of a that the 24
equations need, t = a + D is stored (a from its table entry). Pass 2, slice by slice: the 659 needed bits of e = L(a)
(one load each), chi and iota on the 276 needed bits of the round-1 output b, the 51 needed column parities of b and
21 needed bits of b stored. Round 2: the 26 needed bits of u = L(b) (3 loads, 2 XOR each), the 24 equations of the 10
rows of beta2 (EQS, a basis of the equations of V(beta2_r, alpha3_r), checked by eqs_ok), pass = their AND; one
test. Count: 6,072 primitives, then the batch control (counter, 5-level comparison tree for the next Gray coordinate,
12 loads and XORs of the packed delta, loop test): 40. So E costs exactly 6,112 primitives per 256 pairs on every
path (23.875 per pair). Registers: at most 55 (pass 2: the 12 base words, at most 25 e and 16 b words of a slice).

Stage 2 (unchanged rule): for each pair of the pass word, form x and x + beta (at most 32 basis additions), both
complete 5-round digests (2 units), compare 256 bits and output the pair (bytes 0..134 of L^-1(x) and L^-1(x + beta))
if equal; at most 2 units + 2^11 primitives per pair. At most S2CAP = 2^24 stage-2 pairs per space (2.6; then E stops
on that space); the largest count in the 1,236 spaces of R5 is 308 (in the 1,586 spaces of C and D, 314; 256
expected).

Lemma 4 (E is v8's E). For every space, the set of tested pairs (v0 + W, all 2^32) and the stage-1 predicate (the 24
equations, equivalently u_r in V(beta2_r, alpha3_r) on the 10 rows) are those of v6 and v8; r5-count checks every
equation word of the counted program against a plain evaluation (85 or 86 of the 256 pairs per trial, residues
alternating), and a passing pair (the first message of certificate r5-v6-000038 placed at a seeded slot) passes. E outputs a pair on a space iff the window holds a
colliding pair and the stage-2 cap does not bind; the order of testing changes only which pair is output. So every E
run of Section 4 (fes.c of the R5 study and of pre-registrations C and D, Appendix B; the Python e_window of r5-R-*)
is a run of this E for the purpose of H1.

### 2.5 Main loop and correctness

Run P (trail_search, 2.1; fail on CapReached). Base S from P's output.
Advice rounds (2.2, 2.3) until K = 96 accepted spaces of one advice, or until B''s budget or A_MAX is
exhausted (then fail). Run E on the K spaces in order and halt with the first output; if there is none, fail.
algorithm() in the experiment file is this driver with every cap (its P is trail_search, its E the plain
evaluation e_window, Lemma 4).
Lemma 1 (outputs are collisions): for x in V, A0 = L^-1(x) satisfies the fixed-bit equations, and so does A0 +
L^-1(beta), since E_D forces (L^-1 beta)_j = 0 on F; beta != 0; E compares the true 256-bit digests. Lemma 2 (used only
for the probability): for x in V the difference after round 1 is alpha2. Lemma 3: beta is not in W, so the 2^32
pairs of a space are distinct.

### 2.6 Caps set by one rule

Three counts can only be observed by running: P's full evaluations F, the work units of a connector attempt, and E's
stage-2 pairs per space. Each has a hard cap in the code and is charged at its cap. v13 sets the three caps by one rule
that uses no run: each is the largest power of two whose charged term stays within 2^43 primitives, which is T3's
batch term (5,679,328,446 x 1,583 = 2^43.03 primitives) rounded down to a power of two. With the other factors of each
term fixed (2^13 primitives per full evaluation; A_MAX = 2^13 attempts of at most 96 X_MAX + 2^24 + 2^22 primitives;
K = 96 spaces of S2CAP pairs at 2 units + 2^11 primitives each), the rule gives F_CAP = 2^30, X_MAX = 2^23 and S2CAP =
2^24. B''s budget, 2^32 units = 2^42.40 primitives, also satisfies it. v11's caps were 2^22 (sized from pass 1's
count), 2^18 (from v5 runs, G1) and 2^11. The R5 study ran with v13's caps, and none acted in it (largest attempt
189,224 work units, largest stage-2 count 308; F = 770 in the algorithm's order). The three terms now cost
2^32.60, 2^32.22 and 2^32.40 units instead of 2^24.60, 2^28.06 and 2^19.40; this adds 0.063 bits to the total.

## 3. Exact facts (P's output; recomputed by facts() in every B' and connector experiment)

alpha3 = bits {0, 130, 450, 529, 701, 789, 1021, 1169, 1280, 1429}; nonzero lanes of beta2 in hex 0:1 2:4 5:4 6:4 7:4
8:20000 10:2000000000000000 12:200000 15:2000000000000000 18:20000 20:200001 22:200000 24:1. alpha3 and beta3 =
L(alpha3) are in the CP kernel (10 bits each); beta2 -> alpha3 on the same 10 rows, w2 = 24 (row 66 weight 4, rows 256
and 277 weight 3, the rest 2); alpha2 = L^-1(beta2) has 59 active rows and w1 = 127; C2 = 3^20 for this core. P45 =
sum over the 2^19 alpha4 compatible with beta3 of Pr[beta3 -> alpha4] x prod over nonzero digest-plane rows q of
L(alpha4) of (DDT[q][0] + DDT[q][16])/32 = 55/2^19 = 2^-13.2186 (192 nonzero terms); with w2, p_M = 2^-37.2186 per
pair. Advice facts, for each advice used: beta1' -> alpha2 has weight 127 on the 59 rows; beta0' is compatible with
alpha1' on every row and zero on its inactive rows; alpha0' = L^-1(beta0') is nonzero and zero on F.

## 4. Executed evidence (none of it is the claimed cost)

### 4.1 Coins, run selection, premise R, every run made since v11

Coins of our runs. A labelled run uses Coins(SHA-256(label || "beta1" || c)) for B''s candidate c,
Coins(SHA-256(label || "att" || c || j)) for its attempt j, and, for connector attempt i on the advice of candidate c,
seed_i = SHA-256(label || "conn" || (c + 1) as 4 little-endian bytes || i as 8 little-endian bytes) with words
SHAKE-256(seed_i || k) (class Coins). The index map is the algorithm's own: Fisher-Yates index j = (low 64 bits) mod
(i+1). In the claimed algorithm every coin is a fresh uniform 256-bit word; the only difference is SHAKE-256 output in
place of fresh words.

Premise R (stated inside H1): the label-seeded coins act as fresh coins, and the 48 runs of the R5 study are an
unselected sample of the algorithm's runs. Under premise R the 48 success indicators are independent Bernoulli(p)
draws; distinct labels by themselves only give distinct SHAKE-256 streams. Support:
- The labels "hashsmash sha3-256-r5 R5 run k", k = 0..47, the plan, the driver, the analysis and every file of the
  computation were hashed at 2026-10-07T20:27:28Z, before any run (Appendix D; a first commit at 20:27:03Z was
  replaced before any run, only to change the launcher's start gate; the launch wrapper and the watchdog, which
  compute nothing, were written after the commit and before the launch).
- All 48 runs were started and completed (exit code 0, empty error files); none was stopped, excluded or repeated;
  every result is in the table of 4.3 and the ledger of Appendix D.
- The plan has one outcome-dependent rule: claim 0.40 if the bound is at least 0.40, else nothing from R5. A bound
  computed by a rule fixed in advance keeps its coverage whatever is then done with it: Pr[the claim is made and the
  true success is below it] <= Pr[the bound exceeds the true success] <= 0.05. It has no rule that changes a constant.
- The organizer's seeds pick which logged successes r5-R-0..9 replay and which earlier attempts are re-run; a
  holdout nonce changes them. They do not enter any bound.

Every run made since v11 (2026-10-07; times UTC). Only R5 enters the bound; C and G2's runs are charged (0.1); the
rest are listed so that nothing is selected away.
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

16 certificates (distinct 135-byte messages, equal complete 5-round digests): 15 collisions of the R5 study, one per
run (id r5-R5-k<k>-<coordinate>, runs 0-5, 7-14 and 35; run 35's replay exceeds the experiment sandbox's memory, so
its collision is a certificate), and r5-v6-000038, whose first message r5-count uses. Each R5 certificate is that
run's logged output, the pair at the coordinate in r5.py's table RUNS.

### 4.6 Organizer experiments

r5.py holds the reference algorithm and all experiments (one file, 64,366 bytes). r5-R-* return real collisions.
The other 6 experiments check programs and counts and return sentinels: PASS (00^135, 01 || 00^134), FAIL (00^135, 02
|| 00^134).

| id | trials | PASS means | local result (public seed; nonces v14-nonce-1, v14-nonce-2) |
| --- | --- | --- | --- |
| r5-trail-0..3 | 1 each | P's counts of the group (T1 nodes per lane; cores, C1, P45 > 0, C2, T3 batches and groups) equal the log | 4 of 4 on every seed |
| r5-count | 28 | counted programs of E, T3, T2 against plain evaluations and their longest paths (trials 0-23); P on sub-problems and its cap (24-27, 2.1) | 28 of 28 on every seed |
| r5-bpfull | 3, then 24 connector attempts | trial 0: whole B' of a seed-picked R5 run (21, 24 or 42) from its label: logged cost and advice, facts of Section 3; trial 1: both caps act (2^22-unit budget, 2^21-unit candidate cap); trial 2: the table RUNS has 48 runs and 46 successes, and the bound is >= 0.40; trials 3-26: an attempt with organizer coins on trial 0's advice is accepted and verified (Lemmas 1-2) | 3 of 3 on every seed; attempts accepted and verified: 7, 10 and 13 of 24 (30 of 72; descriptive, no bound uses this rate; R5's label-seeded rate 0.305) |
| r5-R-0..9 | 2 each | the seeds pick two successes of the stratum (the 45 successes other than run 35, position mod 10); for each: B' re-derives the advice from its label (DF, hash, facts of Section 3); the status string has idx accepted attempts, idx <= 96, ending at attempt i; attempt i and min(i, 23) seed-picked earlier attempts are re-run with the run's coins and give the logged statuses, attempt i with the logged DF; E's 2^12-coordinate window returns the collision at the logged coordinate | 20 full collisions on every seed |

Over a review the seeds re-derive 20 of the 45 replayable successes; any logged success that is not an output of the
algorithm at its logged place would be caught with probability at least 2/5 for that run (2 picks among at most 5),
and the 15 certificates are checked by intake.

Local runs (our check, not organizer evidence): experiments/runner.py with Python 3.12 in place of Docker, each
experiment executed twice by the runner with byte-identical output, on the public seed and on the nonces
"v14-nonce-1" and "v14-nonce-2", written down before the runs. Per experiment at most 5.7 CPU-s and 94 MB (three
seeds in parallel). Over the three seeds r5-R-0..9 replayed 37 distinct successes of the 45, each giving its logged collision. A first local pass
(2026-10-07T22:07Z) on an earlier layout of the same experiments (the trail groups merged in pairs, 12 strata) also
passed everything; the layout was changed only to keep every experiment near v13's tested run times.

## 5. Success probability (end to end, over the algorithm's own coins)

The probability space is the algorithm's coins: B' candidate coins and connector coins. The target is fixed, and P
and E are deterministic. A run of the algorithm is therefore a function of its coins, and p = Pr[the algorithm
outputs a collision].

Lemma 6 (each R5 run is a complete run of the algorithm). For every k, the R5 record is the algorithm's execution
with the label-derived coins:
- P's output is the trail of Section 3 (premise P, 2.1).
- B' started at candidate 0 with the full budget; its cost over all rounds of a run was at most 2^28.73 units, so its
  budget never acted. CCAP acted as specified (90 candidates).
- The connector rule ran as specified: 48 advices kept with 96 accepted within 96-557 attempts; 3 advices discarded at
  A_ADV with B' resumed at the next candidate; at most 2,308 attempts in a run, so A_MAX never acted; no attempt
  reached X_MAX (largest 189,224 work units).
- E ran on the accepted spaces in order and stopped at its first output. fes is E on each space by Lemma 4 (all
  1,236 self-checks passed), and the stage-2 cap never bound (at most 308 pairs).
- r5run.py makes algorithm()'s calls in algorithm()'s order (bprime, Setup, attempt, E per space), with E as fes and
  espace.stage2; the experiment file it loads is byte-identical to v13's experiments/r5.py, and its three settings
  are v14's constants.
So "success" in the table of 4.3 is the algorithm's success on those coins. The runs use the algorithm's own index
map, so they differ from the algorithm only in using SHAKE-256 words in place of fresh words (premise R).

Heuristics (claim.json):
- H1-end-to-end-success: p >= p0 = 0.874, under premise R (4.1) and premise P (2.1). Support: 46 of the 48 R5 runs
  succeed. Under premise R the 48 outcomes are independent Bernoulli(p) draws, and the one-sided 95% Clopper-Pearson
  lower bound (exact binomial tail) is 0.8746. The organizer re-derives 20 seed-picked successes per review
  (r5-R-0..9), recomputes the count and the bound from the table (r5-bpfull trial 2) and checks 15 collisions as
  certificates; every run, failures included, is in the table of 4.3 and the ledger of Appendix D.
- H2-development-ledger: the charged development (G2 and C) contains every target-specific run whose result fixed,
  or under its plan could have changed, a number that the algorithm reads (0.1, 0.2).

So Pr[success] >= 0.874 >= 0.40, with confidence 95%. The claimed 0.40 follows the rule of R5's plan. It would still
be the 95% bound with as few as 26 successes in 48, that is, 20 more failures than observed. Every cap of Section 6
holds without H1.

Consistency (descriptive; no bound uses it):
- R5 found 46 positive spaces in 1,236 enumerated spaces, 0.037 per space (E stops at the first output, so this is
  the maximum-likelihood rate). C found 23 in 768 (0.0299) with v13's B'.
- The trail predicts 1 - exp(-256 x 2^-13.2186) = 0.0265 per space: about 256 round-2 passes per space, each reaching
  alpha3 and then colliding with probability P45. At 0.0265 per space a run succeeds with probability 0.924; 46 of 48
  = 0.958 were observed.
- v13's tuned B' gave the same count, 46 of 48, in C and D.

## 6. Time (collision-frontier-v5: one 5-round permutation = 1 unit, other primitives 1/1355)

| Term | Cap, enforced by | Count and price | log2 units |
| --- | --- | --- | --- |
| P: T1 | exact count N1 (organizer-recomputed) | 8,674,833 nodes x 2^12 (bound per node, as in v8) | 24.6443 |
| P: T2 | exact count C1 (organizer-recomputed) | 1,639,088,128 leaves x 166 (counted) | 27.5812 |
| P: T3 batches | batch counter at the exact count (organizer-recomputed) | 5,679,328,446 batches x 1,583 (counted, every batch) | 32.6274 |
| P: T3 full evaluations | F_CAP = 2^30 (2.6) | 2^30 x 2^13 (bound, not counted) | 32.5959 |
| P: T3 group setup | 1411 groups (organizer-recomputed) | 1411 x 2^27 (bound, not counted; derived 2^25.2) | 27.0584 |
| P: setup |  | 2^31 primitives (bound) | 20.5959 |
| B' | WK counter, re-checked on every update | 2^32 units + one update (< 2^13 units) | 32.0000 |
| S | at most 4 advice rounds | 4 x 2^31 primitives | 22.5959 |
| Connector | X_MAX = 2^23 work units per attempt (2.6), A_MAX = 2^13 attempts | 2^13 x (2^23 x 96 + 2^15 x 2^9 + 2^22) primitives | 32.2180 |
| Bases | K = 96 spaces | 96 x 2^24 primitives | 20.1809 |
| E setup | K = 96 spaces | 96 x 2^24 primitives (bound, not counted; derived about 2^23.1) | 20.1809 |
| E stage 1 | 2^24 batches per space | 96 x 2^24 x 6,112 primitives (counted, every path) | 32.7583 |
| E stage 2 | S2CAP = 2^24 per space (2.6) | 96 x 2^24 x (2 units + 2^11 primitives) | 32.3970 |
| Output | one pair | 2^22 primitives | 11.5959 |
| Algorithm | | | 35.0558 |
| Development G2 (v6 run, pre-registrations A and B) | exact counters and caps (0.1) | counted prices of the submitted programs | 35.2782 |
| Development C (pre-registration C) | exact counters and caps (0.1) | counted prices of the submitted programs | 35.9149 |
| Total T | | | 37.0488 -> 37.05 |

K = 96 is v10's value, chosen from the runs of G2 (charged, 0.1) and kept by the rule of pre-registration C (charged,
0.1); R5 measured the success at K = 96 (Section 5).

Every term of the algorithm is a cap or an exact count, times the longest counted path or a stated bound; no expected
value is used, and no count taken only from our runs enters except through a cap (F_CAP). The development terms are exact
counters or caps at counted prices (G2, C). Preprocessing (P + B' + S + development) = 2^36.8544, claimed 36.86.
Sensitivity (not the claim): with v8's prices for P (2 x its v8 bound) T would be 2^40.10; with v8's E (594 per pair)
2^38.20; with the three uncounted setup bounds 4 times larger 2^37.05; the development sensitivities are in 0.1.

## 7. Memory

Measured peaks: P 7.5 MB (trail3b, both passes; the counted program's triple tables would take 2 x 2^15 x 107 words =
224 MB per group), B' at most 113.5 MB (pre-registration A's run 2; 113 MB in the replay of R5 run 35), connector under 2^23 bytes; E's tables 2 x 64 x 1024 x 16 words = 67
MB per space plus Pat. Before E starts, algorithm() keeps the echelon system of each of the K accepted spaces (about
31 MB in all). Declared 2^30 bytes, more than 4 x the largest phase.

## 8. Not claimed; credits

Not claimed: any improvement on [GLL+20] beyond the byte-aligned (p = 8) adaptation, B', the bitsliced counted E and T3
and the accounting. The certificates show that the construction works; they are not the claimed cost. Credits:
[GLL+20] for the connector and linearisation framework and the 5-round trail core that P re-derives; Dinur, Dunkelman,
Shamir (FSE 2012) for the target-difference algorithm; Qiao, Song, Liu, Guo (EUROCRYPT 2017) for linearisation; Daemen,
Van Assche (FSE 2012) and KeccakTools for in-kernel trail cores;
Bouillaguet, Chen, Cheng, Chou, Niederhagen, Shamir, Yang (CHES 2010) for the fast exhaustive search of our evidence
enumerator fes.c. Th0rgal 7deb1595 (with Subflatus3 and rubenmarcus): the
zero-advice framing with every phase inside a capped algorithm (used here; v13 and v14 charge the development that
7deb1595 and our v8-v11 disclosed without charge), and the
early-abort order of the round-2 rows that v8's E used (v10's bitsliced E evaluates all 24 equations); Th0rgal is a
co-author of this package. None of 7deb1595's code, data or certificates is used. hybridnoise's note (ef4a0c66) showed
that an own-beta1 byte-aligned connector can work; jagnani73 (654cb3d2) taught us fresh coins, hard caps and
organizer experiments. Subflatus3 (04395e26, d2df1a56) and GordoAR (bc0f7b56) also cap T3's full evaluations at 2^30; our F_CAP check
dates from v10 and its value here comes from the rule of 2.6. No code, data or text of theirs is used. baseline_improved is the required nominal reference ID, not a claim of dominance.

## Appendix A. Trail search P as run (C++17; shared helpers kc.h)

These native programs are our evidence for the premise of 2.1 (the algorithm's P is trail_search in r5.py).
Run as `trail1c 10 > cores; trail2c < cores > t2; trail3b U 15 u_inf < t2 > pass1; trail3b U 15 u_seq < t2 > pass2`,
where u_inf holds 2^30 for every kept core and u_seq the running minimum of the pass-1 minima of the earlier cores
(Section 2.1). T1 and T2 are v8's programs (their caps are v8's and never bind; P is charged its exact counts). T2's
charged form is the counted Gray program of r5.py (same leaves, same decision P45 > 0); trail2c also prints
P45. trail3b is the batch form of T3 with the decisions of t3_batch (scalar AS per slot; a slot is evaluated in full
iff 2 AS <= B, B fixed at the batch start). Pass 2 ran the listed file; its per-core prefix counters (lng=) were used
by the v9 draft and are not used by v10. Pass 1 ran an earlier form (trail3b.cpp sha256 b6cddee6...) without the
prefix counters that stops adding a slot's AS once 2 AS > B (the same decisions). Pass 1: 775 s on 15 threads (7,598
CPU-s, 7.5 MB); pass 2: 1,071 s (11,823 CPU-s, 6.9 MB); both output core 349, w1 = 127, w2 = 24 and the beta2 of
Section 3, and both count 5,679,328,446 batches and 1,379,275,399,350 leaves (F = 1,896,302 and 770). SHA-256 of the
per-core logs: pass 1 4efc3ee04fa5f179..., pass 2 6da403d1c0663d41...; u_seq 601a26855ff33b51.... SHA-256 of the
sources: kc.h c6d9edec..., trail1c.cpp 264297b5..., trail2c.cpp a67dc713..., trail3b.cpp (listed) e467e4aa....

`kc.h`:

```cpp
// Keccak-f[1600] helpers shared by the v4 programs. Bit index i = 64*(x+5y)+z.
#pragma once
#include <cstdint>
#include <cstring>
#include <cstdio>
#include <vector>
#include <algorithm>
typedef uint64_t u64;
struct St { u64 a[25]; };
static const int RHO[25] = {0,1,62,28,27,36,44,6,55,20,3,10,43,25,39,41,45,15,21,8,18,2,61,56,14};
static const u64 RC[5] = {0x1ULL,0x8082ULL,0x800000000000808AULL,0x8000000080008000ULL,0x808BULL};
static inline u64 rol(u64 v,int n){n&=63;return n?((v<<n)|(v>>(64-n))):v;}
static inline void zero(St&s){memset(s.a,0,sizeof s.a);}
static inline void xr(St&d,const St&s){for(int i=0;i<25;i++)d.a[i]^=s.a[i];}
static inline int getbit(const St&s,int i){return (s.a[i>>6]>>(i&63))&1;}
static inline void flip(St&s,int i){s.a[i>>6]^=1ULL<<(i&63);}
static inline bool isz(const St&s){u64 o=0;for(int i=0;i<25;i++)o|=s.a[i];return !o;}
static void theta(St&s){u64 C[5],D[5];for(int x=0;x<5;x++)C[x]=s.a[x]^s.a[x+5]^s.a[x+10]^s.a[x+15]^s.a[x+20];
 for(int x=0;x<5;x++)D[x]=C[(x+4)%5]^rol(C[(x+1)%5],1);for(int i=0;i<25;i++)s.a[i]^=D[i%5];}
static void rhopi(St&s){St b;for(int x=0;x<5;x++)for(int y=0;y<5;y++)b.a[y+5*((2*x+3*y)%5)]=rol(s.a[x+5*y],RHO[x+5*y]);s=b;}
static void Lmap(St&s){theta(s);rhopi(s);}
static void chi(St&s){St b;for(int y=0;y<5;y++)for(int x=0;x<5;x++)b.a[x+5*y]=s.a[x+5*y]^((~s.a[(x+1)%5+5*y])&s.a[(x+2)%5+5*y]);s=b;}
static void rnd(St&s,int r){Lmap(s);chi(s);s.a[0]^=RC[r];}
static inline int rowval(const St&s,int y,int z){int v=0;for(int x=0;x<5;x++)v|=((s.a[x+5*y]>>z)&1)<<x;return v;}
static inline void setrow(St&s,int y,int z,int v){for(int x=0;x<5;x++){u64 m=1ULL<<z;if((v>>x)&1)s.a[x+5*y]|=m;else s.a[x+5*y]&=~m;}}
static int chi5(int v){int o=0;for(int i=0;i<5;i++){int b=((v>>i)&1)^((1^((v>>((i+1)%5))&1))&((v>>((i+2)%5))&1));o|=b<<i;}return o;}
static int DDT[32][32];
static void initDDT(){memset(DDT,0,sizeof DDT);for(int d=0;d<32;d++)for(int v=0;v<32;v++)DDT[d][chi5(v)^chi5(v^d)]++;}
static inline int lg2(int v){int k=0;while((1<<k)<v)k++;return k;}
// L^{-1} images of unit vectors, computed by Gaussian elimination once.
static St LINV[1600];
static void initLinv(){
  // M rows: for each output bit j, which input bits. We invert by solving L(x)=e_j via columns.
  static St col[1600]; for(int i=0;i<1600;i++){zero(col[i]);flip(col[i],i);Lmap(col[i]);}
  // Build augmented matrix A (1600x1600) with rows = output bits, row j has bit i iff L(e_i)_j=1.
  std::vector<St> A(1600),B(1600);
  for(int j=0;j<1600;j++){zero(A[j]);zero(B[j]);flip(B[j],j);}
  for(int i=0;i<1600;i++)for(int j=0;j<1600;j++)if(getbit(col[i],j))flip(A[j],i);
  for(int c=0;c<1600;c++){int p=-1;for(int r=c;r<1600;r++)if(getbit(A[r],c)){p=r;break;}
    std::swap(A[c],A[p]);std::swap(B[c],B[p]);
    for(int r=0;r<1600;r++)if(r!=c&&getbit(A[r],c)){xr(A[r],A[c]);xr(B[r],B[c]);}}
  // Now A=I, B = M^{-1} rows: (L^{-1} s)_c = <B[c], s>. LINV[j] = L^{-1}(e_j): bit c set iff B[c] has bit j.
  for(int j=0;j<1600;j++)zero(LINV[j]);
  for(int c=0;c<1600;c++)for(int j=0;j<1600;j++)if(getbit(B[c],j))flip(LINV[j],c);
}
static St Linv(const St&s){St o;zero(o);for(int j=0;j<1600;j++)if(getbit(s,j))xr(o,LINV[j]);return o;}
```

`trail1c.cpp`:

```cpp
// Stage T1: enumerate connected in-kernel 2-round cores (alpha3 and beta3 = pi.rho(alpha3) both in the
// CP kernel, |alpha3| <= KMAX bits), dedupe by z-translation, compute forward data (C1, P45) and C2.
#include "kc.h"
#include <set>
#include <cmath>
static int KMAX = 10;
// alpha3 bit (x,y,z) -> beta3 bit (y, 2x+3y, z+rho)
static inline int fwdbit(int i){int l=i>>6,z=i&63,x=l%5,y=l/5;int X=y,Y=(2*x+3*y)%5;return 64*(X+5*Y)+((z+RHO[l])&63);}
static int BWD[1600];
static inline int colA(int i){int l=i>>6;return (l%5)*64+(i&63);} // column (x,z) of an alpha3 bit
static inline int colB(int i){int j=fwdbit(i);int l=j>>6;return (l%5)*64+(j&63);}
static std::set<std::vector<int>> found;
static unsigned long long nodes=0;
static int cntA[320],cntB[320];
static std::vector<int> cur;
static std::vector<int> canon(const std::vector<int>&b){
  std::vector<int> best;
  for(int t=0;t<64;t++){std::vector<int> v;for(int i:b){int l=i>>6,z=i&63;v.push_back(64*l+((z-t)&63));}
    std::sort(v.begin(),v.end());if(best.empty()||v<best)best=v;}
  return best;
}
static bool inset(int i){for(int j:cur)if(j==i)return true;return false;}
static void add(int i){cur.push_back(i);cntA[colA(i)]++;cntB[colB(i)]++;}
static void rem(){int i=cur.back();cur.pop_back();cntA[colA(i)]--;cntB[colB(i)]--;}
static const unsigned long long CAP1=17349666ULL; // 2 x the 8,674,833 nodes of the executed run (budget of P)
static void dfs(){
  if(++nodes>CAP1){fprintf(stderr,"P budget exhausted in T1\n");exit(2);}
  // first unbalanced column in deterministic order: alpha-view columns 0..319 then beta-view 0..319
  int ca=-1,cb=-1;
  for(int i:cur){if(cntA[colA(i)]&1){if(ca<0||colA(i)<ca)ca=colA(i);} }
  if(ca<0)for(int i:cur){if(cntB[colB(i)]&1){if(cb<0||colB(i)<cb)cb=colB(i);} }
  if(ca<0&&cb<0){found.insert(canon(cur));return;}
  if((int)cur.size()>=KMAX)return;
  if(ca>=0){int x=ca/64,z=ca%64;for(int y=0;y<5;y++){int i=64*(x+5*y)+z;if(inset(i))continue;add(i);dfs();rem();}}
  else{int X=cb/64,Z=cb%64;for(int Y=0;Y<5;Y++){int j=64*(X+5*Y)+Z;int i=BWD[j];if(inset(i))continue;add(i);dfs();rem();}}
}
int main(int argc,char**argv){
  if(argc>1)KMAX=atoi(argv[1]);
  initDDT();
  for(int i=0;i<1600;i++)BWD[fwdbit(i)]=i;
  memset(cntA,0,sizeof cntA);memset(cntB,0,sizeof cntB);
  for(int l=0;l<25;l++){unsigned long long n0=nodes;add(64*l);dfs();rem();fprintf(stderr,"lane %d nodes %llu\n",l,nodes-n0);}
  fprintf(stderr,"T1 nodes=%llu cores=%zu\n",nodes,found.size());
  // output each core: bits of alpha3
  for(auto&c:found){printf("%zu",c.size());for(int i:c)printf(" %d",i);printf("\n");}
}
```

`trail2c.cpp`:

```cpp
// Stage T2: forward extension. For each core from T1: beta3 = pi.rho(alpha3); C1 = #alpha4 compatible;
// P45 = sum over all compatible alpha4 of Pr(beta3->alpha4) * Pr(zero 256-bit digest difference | beta4 = L(alpha4)).
// C2 = #beta2 compatible with alpha3. Output one line per core.
#include "kc.h"
#include <cmath>
static double PZ[32];
struct Row{int y,z,d;};
static std::vector<Row> rows;
static std::vector<std::vector<std::pair<int,St>>> outs; // per row: (o, L(row o))
static std::vector<std::vector<double>> pr;
static double P45; static unsigned long long leaves;
static unsigned long long allleaves=0; static const unsigned long long CAP2=3278176256ULL; // 2 x sum C1 (budget of P)
static void fdfs(size_t k,const St&b4,double p){
  if(k==rows.size()){leaves++;if(++allleaves>CAP2){fprintf(stderr,"P budget exhausted in T2\n");exit(2);}double q=p;
    for(int z=0;z<64&&q>0;z++){int d=0;for(int x=0;x<5;x++)d|=((b4.a[x]>>z)&1)<<x;if(d)q*=PZ[d];}
    P45+=q;return;}
  for(size_t j=0;j<outs[k].size();j++){St n=b4;xr(n,outs[k][j].second);fdfs(k+1,n,p*pr[k][j]);}
}
int main(int argc,char**argv){
  double c1max=argc>1?atof(argv[1]):30;
  initDDT();
  for(int d=0;d<32;d++)PZ[d]=(DDT[d][0]+DDT[d][0x10])/32.0;
  char line[4096];int idx=0;unsigned long long totleaves=0;
  while(fgets(line,sizeof line,stdin)){
    int n;char*p=line;int off;sscanf(p,"%d%n",&n,&off);p+=off;St a3;zero(a3);
    for(int k=0;k<n;k++){int b;sscanf(p,"%d%n",&b,&off);p+=off;flip(a3,b);}
    St b3=a3;rhopi(b3);
    rows.clear();outs.clear();pr.clear();
    double lc1=0,lc2=0;int w3=0;
    for(int y=0;y<5;y++)for(int z=0;z<64;z++){int d=rowval(b3,y,z);if(!d)continue;rows.push_back({y,z,d});
      std::vector<std::pair<int,St>> v;std::vector<double> q;int mw=99;
      for(int o=0;o<32;o++)if(DDT[d][o]){St s;zero(s);setrow(s,y,z,o);Lmap(s);v.push_back({o,s});q.push_back(DDT[d][o]/32.0);mw=std::min(mw,5-lg2(DDT[d][o]));}
      lc1+=log2((double)v.size());outs.push_back(v);pr.push_back(q);}
    int nra=0;
    for(int y=0;y<5;y++)for(int z=0;z<64;z++){int o=rowval(a3,y,z);if(!o)continue;nra++;int c=0;for(int d=0;d<32;d++)if(DDT[d][o])c++;lc2+=log2((double)c);}
    // w3 lower bound: weight of beta3 (determined by beta3):
    for(auto&r:rows){int dd=r.d;int k=0;for(int o=0;o<32;o++)if(DDT[dd][o])k++;w3+=lg2(k);} // weight of any transition = log2(#outputs)
    P45=-1;leaves=0;
    if(lc1<=c1max){P45=0;St z0;zero(z0);fdfs(0,z0,1.0);totleaves+=leaves;}
    printf("%d n=%d ASb3=%zu w3=%d C1=%.3f C2=%.3f ASa3=%d logP45=%.4f",idx,n,rows.size(),w3,lc1,lc2,nra,P45>0?log2(P45):(P45<0?999.0:-999.0));
    printf(" |%s",line);
    idx++;
  }
  fprintf(stderr,"T2 total leaves=%llu\n",totleaves);
}
```

`trail3b.cpp`:

```cpp
// Stage T3 in batch form (v9). For each kept core (T2 order), the beta2 leaves are visited in batches:
// inner rows 0..k-1 of alpha3 in full and a group of g values of row k form the slots of a batch (one bit
// position per slot in the counted bitsliced program); the outer rows k+1..n-1 run in reflected mixed-radix
// Gray order, the group index slowest. A batch's threshold B = min(T, best w1 so far) is fixed at the batch
// start; a slot is evaluated in full iff 2*AS(alpha2) <= B. Output: least w1, then w2, then choice vector.
// This native program computes AS per slot with scalar code (same decisions as the bitsliced program).
// Modes:  trail3b P nth < t2      (shared global best across threads; finds the minimum)
//         trail3b U nth ufile < t2 (core i starts with T = U_i from ufile, no sharing; F_i is then an upper
//                                   bound for the sequential algorithm's F_i by monotonicity)
#include "kc.h"
#include <thread>
#include <mutex>
#include <atomic>
#include <map>
struct Core{int idx;St a3;};
static std::vector<Core> cores;
static std::vector<int> Ustart;
static std::atomic<int> nextc(0);
static std::mutex mu;
static std::atomic<int> gbest(1<<30);
static bool shared_mode=true;
static std::atomic<unsigned long long> totleaves(0),totbatches(0),totfull(0);
static const int NR=8; static const int RP[NR]={66,96,129,162,192,225,258,288};
struct Res{int idx,w1,w2;unsigned long long leaves,batches,full,lng[NR];std::vector<int> sel;St b2;int k,g,G;};
static std::vector<Res> results;
static inline int w1of(const St&s){
  int w=0;
  for(int y=0;y<5;y++){u64 v[5]={s.a[5*y],s.a[5*y+1],s.a[5*y+2],s.a[5*y+3],s.a[5*y+4]};
    u64 nz=v[0]|v[1]|v[2]|v[3]|v[4];
    u64 b0=0,b1=0,b2=0;
    for(int k=0;k<5;k++){u64 c=b0&v[k];b0^=v[k];u64 c2b=b1&c;b1^=c;b2|=c2b;}
    u64 ge3=b2|(b1&b0);
    u64 cons=0;for(int i=0;i<5;i++)cons|=v[i]&v[(i+1)%5]&v[(i+2)%5]&~v[(i+3)%5]&~v[(i+4)%5];
    w+=2*__builtin_popcountll(nz)+__builtin_popcountll(ge3&~cons);}
  return w;
}
static inline int asof(const St&s){int n=0;for(int y=0;y<5;y++)n+=__builtin_popcountll(s.a[5*y]|s.a[5*y+1]|s.a[5*y+2]|s.a[5*y+3]|s.a[5*y+4]);return n;}
static void work(){
  for(;;){int ci=nextc++;if(ci>=(int)cores.size())return;Core&c=cores[ci];
    std::vector<int> ry,rz,ro;for(int y=0;y<5;y++)for(int z=0;z<64;z++){int o=rowval(c.a3,y,z);if(o){ry.push_back(y);rz.push_back(z);ro.push_back(o);}}
    int n=ry.size();std::vector<std::vector<int>> ins(n);std::vector<std::vector<St>> LI(n,std::vector<St>(32));
    for(int j=0;j<n;j++){for(int d=0;d<32;d++)if(DDT[d][ro[j]])ins[j].push_back(d);
      for(int v=0;v<32;v++){St s;zero(s);setrow(s,ry[j],rz[j],v);LI[j][v]=Linv(s);}}
    int WT[32][32];for(int d=0;d<32;d++)for(int oo=0;oo<32;oo++)WT[d][oo]=DDT[d][oo]?5-lg2(DDT[d][oo]):99;
    // inner configuration
    int P=1,k=0;while(k<n&&P*(int)ins[k].size()<=256){P*=ins[k].size();k++;}
    int g=1,G=1;if(k<n){g=std::min((int)ins[k].size(),256/P);G=(ins[k].size()+g-1)/g;}
    int T=shared_mode?(1<<30):Ustart[ci];
    int bw1=1<<30,bw2=1<<30;std::vector<int> bestsel;St bestb2;zero(bestb2);
    unsigned long long leaves=0,batches=0,full=0,lng[NR]={0};
    int no=n-k-1; if(no<0)no=0;           // outer digits: rows k+1..n-1
    for(int gam=0;gam<G;gam++){
      // slots of this group
      std::vector<St> IV;std::vector<std::vector<int>> SI;std::vector<int> SW2;
      int gl=(k<n)?std::min(g,(int)ins[k].size()-gam*g):1;
      for(int s=0;s<P*gl;s++){int r=s;std::vector<int> idx(k+1,0);St v;zero(v);int w2=0;
        for(int j=0;j<k;j++){int m=ins[j].size();idx[j]=r%m;r/=m;xr(v,LI[j][ins[j][idx[j]]]);w2+=WT[ins[j][idx[j]]][ro[j]];}
        if(k<n){idx[k]=gam*g+r;xr(v,LI[k][ins[k][idx[k]]]);w2+=WT[ins[k][idx[k]]][ro[k]];}
        IV.push_back(v);SI.push_back(idx);SW2.push_back(w2);}
      // outer Gray (Knuth Algorithm H) over rows k+1..n-1
      std::vector<int> a(no+1,0),f(no+1),o(no+1,1),mm(no+1);for(int j=0;j<=no;j++){f[j]=j;mm[j]=j<no?(int)ins[k+1+j].size():2;}
      St base;zero(base);int w2o=0;for(int j=0;j<no;j++){xr(base,LI[k+1+j][ins[k+1+j][0]]);w2o+=WT[ins[k+1+j][0]][ro[k+1+j]];}
      for(;;){
        batches++;leaves+=IV.size();
        int B=std::min(T,bw1);if(shared_mode)B=std::min(B,gbest.load());
        // decisions of the batch (threshold fixed at batch start)
        static thread_local std::vector<int> pass;pass.clear();
        int minpre[NR];for(int q=0;q<NR;q++)minpre[q]=1<<30;
        for(size_t s=0;s<IV.size();s++){const St&l=IV[s];int as=0;u64 nz[5];
          for(int y=0;y<5;y++){int b=5*y;nz[y]=(base.a[b]^l.a[b])|(base.a[b+1]^l.a[b+1])|(base.a[b+2]^l.a[b+2])|(base.a[b+3]^l.a[b+3])|(base.a[b+4]^l.a[b+4]);as+=__builtin_popcountll(nz[y]);}
          if(2*as<=B)pass.push_back(s);
          for(int q=0;q<NR;q++){int R=RP[q],c=0;for(int y=0;y<5;y++){int lo=64*y;if(R>=lo+64)c+=__builtin_popcountll(nz[y]);else if(R>lo)c+=__builtin_popcountll(nz[y]&((1ULL<<(R-lo))-1));}
            if(c<minpre[q])minpre[q]=c;}}
        for(int q=0;q<NR;q++)if(2*minpre[q]<=B)lng[q]++;
        for(int s:pass){St t=base;xr(t,IV[s]);full++;int w1=w1of(t);int w2=w2o+SW2[s];
          std::vector<int> sel(n);for(int j=0;j<=k&&j<n;j++)sel[j]=SI[s][j];for(int j=0;j<no;j++)sel[k+1+j]=a[j];
          if(shared_mode){int gg=gbest.load();while(w1<gg&&!gbest.compare_exchange_weak(gg,w1));}
          if(w1<bw1||(w1==bw1&&(w2<bw2||(w2==bw2&&sel<bestsel)))){bw1=w1;bw2=w2;bestsel=sel;}
        }
        int j=f[0];f[0]=0;if(j==no)break;
        int old=ins[k+1+j][a[j]];a[j]+=o[j];int nw=ins[k+1+j][a[j]];
        xr(base,LI[k+1+j][old^nw]);w2o+=WT[nw][ro[k+1+j]]-WT[old][ro[k+1+j]];
        if(a[j]==0||a[j]==mm[j]-1){o[j]=-o[j];f[j]=f[j+1];f[j+1]=j+1;}
      }
    }
    Res R;for(int q=0;q<NR;q++)R.lng[q]=lng[q];R.idx=c.idx;R.w1=bw1;R.w2=bw2;R.leaves=leaves;R.batches=batches;R.full=full;R.sel=bestsel;R.k=k;R.g=g;R.G=G;
    zero(R.b2);if(!bestsel.empty())for(int j=0;j<n;j++)setrow(R.b2,ry[j],rz[j],ins[j][bestsel[j]]);
    totleaves+=leaves;totbatches+=batches;totfull+=full;
    std::lock_guard<std::mutex> gd(mu);results.push_back(R);
    printf("%d ci=%d T0=%d k=%d g=%d G=%d batches=%llu leaves=%llu full=%llu w1=%d w2=%d lng=",c.idx,ci,shared_mode?-1:Ustart[ci],k,g,G,batches,leaves,full,bw1==(1<<30)?-1:bw1,bw2==(1<<30)?-1:bw2);
    for(int q=0;q<NR;q++)printf("%llu%s",lng[q],q<NR-1?",":"");
    if(!bestsel.empty()){printf(" sel=");for(int v:bestsel)printf("%d.",v);printf(" b2=");for(int i=0;i<25;i++)printf("%016llx%s",(unsigned long long)R.b2.a[i],i<24?",":"");}
    printf("\n");fflush(stdout);
  }
}
int main(int argc,char**argv){
  shared_mode=argv[1][0]=='P';int nth=atoi(argv[2]);
  initDDT();initLinv();
  char line[8192];
  while(fgets(line,sizeof line,stdin)){
    int idx;double lp;char*q=strstr(line,"logP45=");sscanf(line,"%d",&idx);sscanf(q+7,"%lf",&lp);if(lp<-900||lp>900)continue;
    char*p=strchr(line,'|')+1;int n,off;sscanf(p,"%d%n",&n,&off);p+=off;St a3;zero(a3);
    for(int k=0;k<n;k++){int b;sscanf(p,"%d%n",&b,&off);p+=off;flip(a3,b);}
    cores.push_back({idx,a3});
  }
  if(!shared_mode){FILE*fu=fopen(argv[3],"r");int v;while(fscanf(fu,"%d",&v)==1)Ustart.push_back(v);fclose(fu);
    if(Ustart.size()!=cores.size()){fprintf(stderr,"U size mismatch\n");return 1;}}
  // optional subset: env CORES="i,j,..." (positions)
  fprintf(stderr,"T3b cores=%zu\n",cores.size());
  std::vector<std::thread> th;for(int t=0;t<nth;t++)th.emplace_back(work);for(auto&t:th)t.join();
  fprintf(stderr,"T3b total batches=%llu leaves=%llu full=%llu\n",(unsigned long long)totbatches,(unsigned long long)totleaves,(unsigned long long)totfull);
  // global best
  const Res*b=nullptr;for(auto&r:results){if(r.sel.empty())continue;
    if(!b||r.w1<b->w1||(r.w1==b->w1&&(r.w2<b->w2||(r.w2==b->w2&&r.idx<b->idx))))b=&r;}
  if(b){fprintf(stderr,"BEST core %d w1=%d w2=%d b2=",b->idx,b->w1,b->w2);for(int i=0;i<25;i++)fprintf(stderr,"%016llx%s",(unsigned long long)b->b2.a[i],i<24?",":"\n");}
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
