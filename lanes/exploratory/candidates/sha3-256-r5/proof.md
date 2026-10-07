# 5-round SHA3-256: every phase inside the algorithm under a hard cap, time 2^34.14

Exploratory claim, with Th0rgal as co-author: Th0rgal 7deb1595 (with Subflatus3 and rubenmarcus) introduced on this
track the zero-advice framing used here. The algorithm runs every phase itself (trail search P, advice program B',
connector, enumeration E). The claimed time is a sum of terms, each an exact count or a hard cap times a counted
price. Only the data-dependent counts carry a cap in the code: B''s budget and candidate cap, the connector's work
and attempt caps, E's stage-2 cap and P's cap F_CAP on full evaluations. P's T1 nodes, T2 leaves and T3 batches are
exact counts of a deterministic search, which the organizer recomputes. The algorithm reads nothing published. [GLL+20] = J. Guo, G. Liao, G. Liu, M. Liu, K.
Qiao, L. Song, "Practical Collision Attacks against Round-Reduced SHA-3", J. Cryptology 33 (2020), ePrint 2019/147.

## 0. Claim, summary, changes

| Field | Value | Basis |
| --- | --- | --- |
| time_log2 | 34.14 | sum of the phase charges, 2^34.1359, rounded up (Section 6; unchanged from v10) |
| success_probability | 0.40 | >= 0.874: one-sided 95% Clopper-Pearson bound from 46 successes in 48 complete runs of the algorithm (pre-registrations C and D; 0.877 with the one extra run, 47 of 49; Section 5) |
| preprocessing_log2 | 33.40 | P, B' and S: 2^33.3994, rounded up |
| memory_log2_bytes | 30 | largest phase about 2^28 bytes (Section 7) |
| nonuniform_advice_log2_bytes | 0 | the algorithm computes its trail and its connector advice |

Summary: P finds the trail. Its charge is organizer-recomputed counts times counted worst-case prices. The one count
the organizer cannot recompute at full scale is F, P's number of full evaluations. F enters only through its cap
F_CAP = 2^22, which the code of P checks, and Lemma P bounds it by a logged count 2.2 times below the cap. B' builds
the connector advice (budget 2^32 units, at most 2^26 units per candidate). The v5 connector makes K = 96 affine
spaces, and E tests 2^32 pairs per space at 6,112 counted primitives per 256 pairs. The success probability is
measured end to end, on complete runs of the algorithm from pre-registered labels: pre-registration C ran B', the
connector rule and E on the first 16 spaces of 48 fresh runs, and pre-registration D finished E on the remaining
spaces of every run that had no output yet. The only premise is that these label-seeded runs behave like runs with
fresh coins (premise R, Section 4.1).

What changed from v10 (34.14, rated not_evaluable) and why. The algorithm, its caps and its cost are v10's.

| Review finding on v10 | v11 |
| --- | --- |
| H1 was a pointwise bound for every advice B' can output, measured on one advice (14 of 512) plus 2 spaces per fresh advice; H2 and H3 were pointwise per-candidate and per-round bounds from aggregate counts | One heuristic, H1-end-to-end: the success probability itself, an average over all of the algorithm's coins, bounded from 48 complete runs (Section 5). No per-advice, per-candidate or dispersion premise is used |
| The v6 run had a submit-if-threshold rule; public-seed and historically selected runs were treated as representative of fresh coins (H4, unsupported) | v6, pre-registration B and pre-registration A are not used for any bound. The bound uses only pre-registrations C and D: fresh labels, plan and code hashed before any run, every run reported, no submit or withhold rule. Every other run made during v11, including one smoke test and a parallel session's abandoned variant runs, is listed in 4.1, and the bound is also given with the smoke test included. Premise R is stated inside H1 with its support |
| algorithm() started from hard-coded BETA2/ALPHA3 and never invoked P; no F_CAP check was visible | algorithm() now runs P (trail_search, with the check `if F[0] > fcap: raise CapReached` in t3_core) and builds Base from P's output; r5-count runs P on sub-problems and reproduces the native per-core lines (output and F), and shows the cap stopping P; Lemma P (2.1) makes the premise on F rest on pass 1's logged count |
| Component experiments used fixed sentinels | r5-C-0..4 return real collisions. Trial 0 of each re-derives a positive space of C from its labels (B', connector attempts 0..i, E); trial 1 does the same for the success of a run completed by D (B', the accepting attempt i, E). The other 11 experiments still return sentinels: they check programs and counts, not outputs |

Development runs (not charged, unchanged from v8 and v10). B' has six design constants: R = 16 attempts per candidate,
DMIN = 40, and the D2u ordering weights KW = 1.0, MW = 0.25, LB = 1.0, PREF = 1.0. Development runs on 2026-10-06
before 09:01Z (75 processes, 1,559 CPU-s) chose them; some used the published [GLL+20] difference as a test case.
Uncharged v5 runs also set the connector's DMIN = 33 (the least DF for which E's window exists) and its 2^18 work-unit
cap (charged in full, never bound: largest of 10,249 logged attempts 187,040). The algorithm reads no output of
development runs except these numbers, and every rate used here comes from runs made after they were fixed. 7deb1595
used this framing (zero advice, development uncharged and disclosed). Sensitivity (not the claim; 2^38 primitives per
core-second): charging the 1,559 CPU-s of B' development gives T = 2^38.29, still below the lowest listed score,
39.05; v7's whole development ledger (12,527 CPU-s) gives T = 2^41.22. The constants of v9-v11 (batch layouts of E and
T3, CCAP, K, A_ADV, A_MAX, B_BUDGET) only change cost or caps and were set by counting, with no run. The native runs
of P (2.1, Appendix A) are executions of P, whose cost is charged in full. Pre-registrations C and D are evidence
about the algorithm's randomness, not part of the algorithm, and changed no constant of it (K stayed 96). Their
compute is disclosed, not charged: C about 3,100 CPU-s of Python and 768 enumerations of about 2.5 s; D 496 CPU-s of
Python and 818 enumerations.

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
- every slot in pass is evaluated in full (w1, w2, lexicographic update of the best; counter capped at F_CAP = 2^22;
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

with fcap = F_CAP = 2^22 in algorithm(); CapReached makes algorithm() return without output. Base(a3b, b2) is built
from P's output (the experiments use P's logged output, the constants ALPHA3_BITS and BETA2 of Section 3).

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
infinity. So the premise on F rests on pass 1's count, 2.2 times below F_CAP.

trail3b has no cap check; with 770 evaluations against a cap of 4,194,304 a check could not have acted. Organizer
check of the same decisions on sub-problems (r5-count trials 24-27, executing the algorithm's t3_core and
trail_search): core No. 1136 from T = 2^30 gives (w1, w2, choice) = (372, 18, 2.4.7.0.4.0) with
F = 517, and from T = 127 no evaluation, exactly the native pass-1 and pass-2 lines; trail_search on the sub-problem
[core 874, core 1136] outputs core 874's native pass-1 trail (w1 = 320, w2 = 23, same beta2) with F = 425; with the cap
lowered to 100, t3_core raises CapReached at F = 101. Deterministic premise (not a probability; the earliest one in
the success argument): P outputs the trail of Section 3 with F <= F_CAP = 4,194,304 (2.2 times pass 1's bound, 5,447
times pass 2's count). The organizer cannot re-run the whole minimisation (1.4 x 10^12 leaves); Appendix A gives the
commands, sources, CPU times and the SHA-256 of both per-core logs, and Section 3 checks w1 = 127. If F exceeded
F_CAP, P would stop without output: the cost bound holds either way.

P's charge: T1 + T2 + T3 batches + full evaluations at F_CAP + group setup + setup (DDT, L^-1 by elimination,
per-core tables: below 2^31) = 9,523,886,111,458 primitives = 2^32.711 units. No factor 2: every count is exact and
organizer-recomputed or a cap, and every price is the longest counted path or a stated bound.

### 2.2 Advice program B' (budget 2^32 units, at most 2^26 units per candidate)

B' (experiment file, rand_min_beta1 to bprime) is v6's program with a budget and a per-candidate cap. Its only inputs
are P's trail and the fixed bits F. For candidate c = 0, 1, ... (each abandoned once its own cost exceeds CCAP = 2^26
units; B' then moves to c + 1):
- beta1_c: in each of the 59 rows of alpha2, a uniformly chosen input difference of least weight (50 rows have exactly
  one, 9 have 4 or 5); then the round-1 conditions, the linearisation table and the link and candidate tables.
- attempts j < R = 16: D2u gives the rows of alpha1 = L^-1(beta1_c), in DSATUR order, affine sets of compatible
  differences on which the fixed-bit link conditions are uniform; M2 picks, row by row, (d, W) with forward checking
  on one value system (x, fixed bits, row equations, the 127 round-1 conditions). An attempt is accepted iff it is
  consistent with DF >= DMIN = 40 and 64 sampled points pass (both messages padded, block difference L^-1(beta0),
  exact 2-round difference alpha2).
- B' stops at the first accepted attempt and outputs (beta1_c, beta0).

Every operation is counted by class: row (one operation on an integer of at most 2585 bits = 11 words: 256
primitives), small (8), Keccak-f call (5 units), SHA-256 compression (2 units), 2-round evaluation (1 unit). The class
WK raises BudgetExceeded on the first counter update that takes B''s cost above B_BUDGET = 2^32 units or the current
candidate's cost above CCAP; so B' spends at most 2^32 units plus one update and a candidate at most 2^26 units plus
one update (the largest update inside B' is below 2^13 units). r5-bpfull executes bprime() whole: run k = 1 from its
label (counted cost equal to the logged 15,477,633,191/1355 units, same output), and with a 2^22-unit budget and a
2^21-unit candidate cap (candidate 0 stops 33.1 units above 2^21, candidate 1 starts, B' stops with no output 264.0
units above 2^22). All 65 candidates of pre-registration A cost at most 2^25.848 units and every run at most 2^28.22
units, so they are runs of the capped 2^32-unit program as well; in pre-registration C (4.2) the shipped caps acted
(2 of 328 candidates stopped at CCAP).
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
consistent and DF = 1600 - rank(E_M) >= 33; above 2^18 work units the attempt fails. An attempt costs at most 2^25.46
primitives (2^18 x 96 + 2^15 coin words x 2^9 + 2^22) and draws at most 22,150 coin words.

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
if equal; at most 2 units + 2^11 primitives per pair. At most S2CAP = 2^11 stage-2 pairs per space (then E stops on
that space); the largest observed is 307 (256 expected).

Lemma 4 (E is v8's E). For every space, the set of tested pairs (v0 + W, all 2^32) and the stage-1 predicate (the 24
equations, equivalently u_r in V(beta2_r, alpha3_r) on the 10 rows) are those of v6 and v8; r5-count checks every
equation word of the counted program against a plain evaluation (85 or 86 of the 256 pairs per trial, residues
alternating), and a passing pair (the first message of certificate r5-v6-000038 placed at a seeded slot) passes. E outputs a pair on a space iff the window holds a
colliding pair and the stage-2 cap does not bind; the order of testing changes only which pair is output. So every E
run of Section 4 (fes.c of pre-registrations C and D, Appendix B; the Python e_window of r5-C-*) is a run of this E for
the purpose of H1.

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

### 4.1 Coins, run selection, premise R, every run made during v11

Coins of our runs. Attempt i of a labelled connector run uses seed_i = SHA-256(label || i as 8 little-endian bytes)
and words SHAKE-256(seed_i || k) (class Coins); B' runs use Coins(SHA-256(label || "beta1" || c)) and
Coins(SHA-256(label || "att" || c || j)). The index map is the algorithm's own: Fisher-Yates index j = (low 64 bits)
mod (i+1). In the claimed algorithm every coin is a fresh uniform 256-bit word; the only difference is SHAKE-256
output in place of fresh words.

Premise R (stated inside H1): the label-seeded coins act as fresh coins, and the 48 runs of pre-registration C, which
D completes, are an unselected sample of the algorithm's runs. Support:
- Labels "hashsmash sha3-256-r5 v11 C B-prime run k" and "... C conn run k", k = 0..47, were written in C's plan; the
  plan, driver, analysis and enumerator were hashed before any run (4.2), and so was D's plan (4.3).
- Every run of C was started, none was stopped, excluded or repeated, and every result is reported (table of 4.3).
- Neither plan has a rule to submit or withhold that depends on the outcome. C's only outcome-dependent choice was K,
  which could only grow; it stayed 96. D's plan fixed the claimed success as 0.40 if its bound is at least 0.40,
  else the bound. A bound computed by a rule fixed in advance keeps its coverage whatever is then done with it:
  Pr[the claim is made and the true success is below it] <= Pr[the bound exceeds the true success] <= 0.05.
- The production seed is the organizer's public seed, which we did not choose. It only picks which logged
  successes r5-C-0..4 replay; it does not enter any bound.
- Our local experiment runs with the public seed and with nonces fixed before running give the same deterministic
  results (4.6).

Every run made during v11 (2026-10-07; times UTC). Only C and D enter the bound; the rest are listed so that nothing
is selected away.
- Pre-registration C: runs k = 0..47, 16:57:43Z-17:16:03Z (4.2).
- Run 999 (smoke test of C's driver, labels "... C B-prime run 999" and "... C conn run 999"): 16:55:34Z-16:56:09Z,
  after C's plan was hashed and outside C's sample. One candidate, advice (c, j) = (0, 0), DF 40, kept; 0 positive
  spaces among its first 16. D completed it (first output at space 23). The bound is given with it included (Section
  5). File devcheck/999.json, SHA-256 364f1abeba9454663dc48130e4e729137d82d48dc76b973c479272e5d93940f7.
- Pre-registration D: 31 runs, 17:53:22Z-17:58:42Z, and one check of its driver at 17:52:05Z on run 0's space No. 1,
  which C had already enumerated (4.3).
- A parallel session of ours wrote a different plan at 16:58:33Z, which we call C' here to avoid the name clash
  (prereg/plan.md, SHA-256 7fde45cf25f6555cab68dfef679adce25cd5fad6ab64cdc9ca4a2cb6da063b8b). It ran a variant
  that is not the claimed algorithm: B' with no attempt limit per candidate, DMIN 33 and unweighted D2u ordering,
  os.urandom seeds and a native E. 14 runs started 16:58:42Z-17:14:54Z. 4 finished (its runs 2, 5, 7, 9), each
  with a collision (at its spaces 2, 3, 11 and 4). The runner ended at 17:18Z with the other 10 unfinished
  (prereg/runs.jsonl, SHA-256 2f63dd3bae4e21cbd736529cd3fbfcb7fd469dfba1bd92825b3e8d97236eecd3). C' was abandoned. It
  fixed no constant and enters no bound.
- The same session made 3 test runs of that variant, starting 16:52:22Z (test_log.jsonl, SHA-256
  38093c7f3809938e984eb15d164a1e7106ef27b7b33f5aba71d0320c666f4d9f). Each kept an advice and ran its E on 96
  spaces with no output. But that E reported 0.05-0.11 round-2 passes per space on average, against about 256
  expected (258-274 in C'), so it was not a working form of E; we have not established why. These runs are not runs
  of the claimed algorithm and enter no bound.
- Re-derivations, no new outcome: the parallel session's check of its native E on v6 spaces 0, 1 and 38 (271,
  276 and 227 round-2 passes, and v6's collision in space 38); its replay of 2 of C''s finished runs; our local
  organizer-experiment runs (4.6) and our reviewers' runs of them with other nonces.

### 4.2 Pre-registration C (48 fresh runs up to E's first 16 spaces)

C's plan (Appendix C, verbatim; prereg_c/plan.txt, SHA-256
4e1edbd45e4b0dfb10de7a67f432805e30d54eef073caba197d26ace7142b666) and the SHA-256 of the driver tools/prereg_c.py
(51ba941c39a6e5a67e8ced0ea9a0686391b1f2794024822fce586fb234b0ea7e), the analysis tools/analyze_c.py
(277ff73227ff24e1d813956e133c8fdad418580114d19ecb60409be6f34a12f7), the enumerator fes.c
(9a023ce614609bb9c27ba94683a6dc340f7a1324a3550ca4ba3f45775ae30de4) and its binary
(6d1110190325ed04bccc56eee4b2844e1a0f3d95f17e9cce0984a3d5c01835c3), the experiment-file library r5lib.py
(fe26aed012e0588fbed04bee3a611509993e661423a8a8196c581de807b7a285), espace.py
(c9c5d4a9e3b1d86312a56a6f00fba511b1f321c7c1e3874d0b4b12c81278e769) and the launcher run_c.sh
(b1939a541633a38b78487c9edfe48819c90d274a250981a830bcfc09d4895e45) were written down at 2026-10-07T16:55:25Z,
before any run. Per run, as the algorithm does it: B' (budget 2^32 units, candidate cap 2^26 units, every candidate
and attempt logged with its counted cost); the connector rule (attempts until 96 accepted or 2^11, then discard); for
a kept advice, E on its first 16 accepted spaces over the whole 2^32 window (fes.c, Appendix B), stage 2 by complete
5-round digests, S2CAP recorded. The first launch, at 16:56:15Z, failed in the shell before any run started (macOS
xargs could not build its -I command line; runs/ empty, no run log). The launcher was changed to call one_c.sh and
nothing else changed (run_c.sh 5bfea119e8b2f61a8cc520b1f61481eb5cf182340adfed531f30e30af1b08aba, one_c.sh
9f2dbb66478010f9f23ee9c0dff24b1bb4807bf0464231b168493bd995b2b380). The 48 runs ran 16:57:43Z-17:16:03Z. Run log
prereg_c/runlog.txt afa31086c4575625d3bed565d3e00f075b3e517c1d89344a1b7487b4531ca3a3; result files runs/*.json
concatenated in name order 08294bcd433e41e7bdd7d0775c997220a260f4b76564d87ad70e2a79853b9f24; analysis output
b6fa4d8f8c82c3e9834a958ed826e890d90f08362316a1aa1b58bdf56b0da135 (all in prereg_c/commit.txt).

Results (every run; per run in the table of 4.3): 48 runs, 328 candidates (2 stopped at CCAP), 48 advices, none
discarded (96 accepted within 96-917 attempts); B' cost per run 2^22.59-2^28.81 units; 768 spaces enumerated, 23
positive (23 collisions, none two in one space), in 18 runs; round-2 passes per space mean 256.51 (2^32 x 2^-24 =
256), maximum 314 < S2CAP = 2,048; all 768 enumerations passed fes's self-check, and all 23 collisions were verified
by complete digests (15 are certificates). C's planned analysis combined three averages with a dispersion premise; it
kept K = 96 and gave 0.478. v11 no longer uses that argument, because D measures the success itself.

Before C's plan, fes.c was checked against the logs of earlier runs: v6 spaces 0 and 1 give 271 and 276 round-2
passes (the v6 log), v8 advice 4 space 0 gives 307 and both of its collisions, and v6 positives 38, 126, 462 and v8
advice 7's positive are found at their recorded coordinates; on every tested window the pass set equals the Python
e_window's.

### 4.3 Pre-registration D (completes every run of C to its end) and the per-run table

D was planned after C's results were known, to measure the success probability without any premise about how the
per-space rate varies between advices. Its outcome was not known. Moving from C's planned analysis to D's selects
or drops no run, and the claimed value is 0.40 under either (C's analysis gave 0.478). Plan (Appendix C, verbatim;
prereg_d/plan.txt, SHA-256 3a3bc8119b38b5eaa969a4a803db9b0c9d59c08b363ebaecc88816aeb21ba46c), driver tools/prereg_d.py
(89d503bb0daaa7ed96f4b9c43577e767d34d339c456d48212ea83d442056d1d0), analysis tools/analyze_d.py
(49b282b5401a07d25d7091413be6c782c9e0c57d11831f300d5d8e47832d32c8), launchers one_d.sh
(5b1be567c089f2039a418b72d25ed015bf77c18fa459e99258020a6a45578933) and run_d.sh
(c94192d12119c86d52d75239b6b736b4f1c4b307f7b4e816143b37d710d701b7), with the unchanged files of C, were hashed at
2026-10-07T17:53:16Z, before any run of D. For each of the 30 runs of C without a positive space among its first 16,
and for run 999, D re-derives the advice from its label (bprime started at the logged accepting candidate; C's advice
hash reproduced in every run) and each accepted connector attempt (C's logged status, DF and work count reproduced),
then runs E on accepted spaces 17, 18, ... in order and stops at the first output, as the algorithm's E does. The
other 18 runs of C already had an output. All 31 ran, 17:53:22Z-17:58:42Z, all with exit code 0 and empty error
files. Run log 3dff546cb68bd6ab6ffc9a9ae87f06e63f4867cabc8734adca63c26063de45fe; result files concatenated
25e9a5bb6b7aee42be480e2efbab1c69fabf98bd669536ab2d78649432681425; analysis output
90ad41c744cf5f473f9b936d8b9cc9ad5f9cbf9f9501847eb1d762b9e3469509 (prereg_d/commit.txt).

Results: 28 of the 30 runs output a collision within their 96 spaces, and run 999 at its space 23. Runs 22 and 26
had none in 96. So 46 of the 48 runs of C succeed, and 47 of 49 with run 999. D enumerated 818 spaces; all passed
fes's self-check, the stage-2 cap never bound (largest round-2 pass count over C and D: 314), and every output was
verified by complete digests. Our replay of all 29 outputs with the experiment file's r5-C trial-1 code returned 29
full collisions (devcheck_d/).

Per-run table of C and D (from the result files; "attempts to 96": connector attempts until the 96th acceptance;
"success": E outputs a pair on one of the 96 spaces):

| k | candidates | (c, j) | DF | B' log2 units | attempts to 96 | round-2 passes, spaces 1-16 | positive in 1-16 | D: spaces enumerated | first positive space | success |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 4 | 3, 12 | 41 | 26.14 | 96 | 4277 | 0 | 4 | 20 | yes |
| 1 | 10 | 9, 6 | 72 | 27.71 | 122 | 4184 | 0 | 57 | 73 | yes |
| 2 | 9 | 8, 1 | 50 | 27.36 | 917 | 4102 | 0 | 50 | 66 | yes |
| 3 | 5 | 4, 1 | 45 | 26.74 | 251 | 4129 | 0 | 43 | 59 | yes |
| 4 | 5 | 4, 6 | 51 | 26.60 | 501 | 4041 | 0 | 34 | 50 | yes |
| 5 | 7 | 6, 2 | 41 | 26.94 | 120 | 4069 | 2 | - | 2 | yes |
| 6 | 1 | 0, 0 | 41 | 22.59 | 415 | 4028 | 1 | - | 2 | yes |
| 7 | 5 | 4, 6 | 88 | 25.74 | 105 | 4093 | 1 | - | 5 | yes |
| 8 | 6 | 5, 1 | 40 | 26.51 | 117 | 4060 | 0 | 11 | 27 | yes |
| 9 | 9 | 8, 5 | 55 | 27.54 | 114 | 4135 | 0 | 8 | 24 | yes |
| 10 | 18 | 17, 6 | 52 | 28.44 | 104 | 4034 | 0 | 16 | 32 | yes |
| 11 | 12 | 11, 2 | 56 | 27.75 | 96 | 4076 | 0 | 36 | 52 | yes |
| 12 | 16 | 15, 12 | 52 | 28.06 | 106 | 4174 | 0 | 20 | 36 | yes |
| 13 | 1 | 0, 7 | 57 | 23.89 | 293 | 3981 | 0 | 11 | 27 | yes |
| 14 | 13 | 12, 4 | 55 | 27.40 | 245 | 4102 | 1 | - | 1 | yes |
| 15 | 3 | 2, 10 | 49 | 26.19 | 240 | 4058 | 1 | - | 11 | yes |
| 16 | 4 | 3, 13 | 45 | 26.12 | 114 | 4115 | 0 | 22 | 38 | yes |
| 17 | 2 | 1, 0 | 58 | 25.29 | 159 | 4150 | 0 | 6 | 22 | yes |
| 18 | 1 | 0, 5 | 49 | 23.37 | 96 | 4038 | 1 | - | 3 | yes |
| 19 | 1 | 0, 7 | 61 | 24.00 | 113 | 4059 | 0 | 23 | 39 | yes |
| 20 | 9 | 8, 12 | 52 | 26.96 | 96 | 4012 | 2 | - | 6 | yes |
| 21 | 4 | 3, 3 | 50 | 24.94 | 114 | 4062 | 1 | - | 3 | yes |
| 22 | 2 | 1, 6 | 43 | 25.66 | 109 | 4064 | 0 | 80 | none in 96 | no |
| 23 | 3 | 2, 3 | 43 | 26.52 | 145 | 4053 | 0 | 3 | 19 | yes |
| 24 | 16 | 15, 4 | 57 | 28.34 | 228 | 4157 | 1 | - | 14 | yes |
| 25 | 2 | 1, 4 | 55 | 25.92 | 111 | 4198 | 1 | - | 10 | yes |
| 26 | 16 | 15, 5 | 63 | 27.41 | 152 | 4217 | 0 | 80 | none in 96 | no |
| 27 | 13 | 12, 2 | 59 | 28.34 | 96 | 4057 | 2 | - | 2 | yes |
| 28 | 12 | 11, 4 | 57 | 27.40 | 112 | 4028 | 0 | 6 | 22 | yes |
| 29 | 3 | 2, 15 | 40 | 26.29 | 205 | 4033 | 0 | 11 | 27 | yes |
| 30 | 1 | 0, 8 | 44 | 24.62 | 233 | 4111 | 2 | - | 8 | yes |
| 31 | 9 | 8, 7 | 43 | 27.62 | 96 | 4144 | 0 | 22 | 38 | yes |
| 32 | 10 | 9, 5 | 50 | 27.65 | 213 | 4151 | 0 | 14 | 30 | yes |
| 33 | 6 | 5, 11 | 49 | 26.98 | 114 | 4154 | 2 | - | 2 | yes |
| 34 | 4 | 3, 15 | 57 | 26.61 | 179 | 4128 | 0 | 38 | 54 | yes |
| 35 | 4 | 3, 0 | 46 | 25.32 | 117 | 4149 | 0 | 23 | 39 | yes |
| 36 | 4 | 3, 1 | 44 | 25.75 | 119 | 4023 | 0 | 13 | 29 | yes |
| 37 | 13 | 12, 7 | 61 | 27.77 | 406 | 4100 | 0 | 59 | 75 | yes |
| 38 | 1 | 0, 13 | 50 | 24.97 | 216 | 3991 | 0 | 25 | 41 | yes |
| 39 | 3 | 2, 3 | 57 | 25.33 | 96 | 4043 | 0 | 4 | 20 | yes |
| 40 | 3 | 2, 1 | 40 | 26.04 | 215 | 4099 | 1 | - | 11 | yes |
| 41 | 12 | 11, 11 | 42 | 28.00 | 214 | 4169 | 0 | 61 | 77 | yes |
| 42 | 7 | 6, 15 | 41 | 27.02 | 153 | 4191 | 1 | - | 15 | yes |
| 43 | 8 | 7, 4 | 40 | 27.49 | 534 | 4120 | 1 | - | 11 | yes |
| 44 | 3 | 2, 2 | 62 | 23.51 | 174 | 4119 | 1 | - | 5 | yes |
| 45 | 23 | 22, 11 | 43 | 28.81 | 119 | 4118 | 0 | 10 | 26 | yes |
| 46 | 4 | 3, 9 | 46 | 26.11 | 96 | 4182 | 0 | 21 | 37 | yes |
| 47 | 1 | 0, 12 | 48 | 24.17 | 111 | 4221 | 1 | - | 11 | yes |
| 999 (smoke test, not in C) | 1 | 0, 0 | 40 | 22.57 | 135 | 4068 | 0 | 7 | 23 | yes |

### 4.4 Earlier runs, not used for any bound

Pre-registration A (2026-10-06T15:29:17Z, sha256 fcfd7d64...): nine B' runs under the program of v8 (k = 0 used
the v6 label LABEL_B = "hashsmash sha3-256-r5 v6 B-prime advice run 1", whose outcome was already known; k = 1..8
"hashsmash sha3-256-r5 v8 B-prime fresh run k"), started together, none stopped or repeated: 65 candidates, 9
accepted, every candidate at most 2^25.848 units (below CCAP) and every run at most 2^28.218 units. v11's B' and
connector functions are AST-identical to v10's (only Base's arguments, facts() reading st.beta2 and algorithm()
changed), and C ran v10's file itself. r5-bp-0..4 re-derive A's advices from their labels and run connector attempts
with organizer-seeded coins; r5-bpfull runs B' run 1 whole and shows both caps acting. A enters no bound.

| k | c, j | DF | B' cost (log2 units) | connector accepted / 128 |
| --- | --- | --- | --- | --- |
| 0 | 5, 9 | 41 | 27.118 | 120 |
| 1 | 0, 2 | 42 | 23.445 | 105 |
| 2 | 14, 5 | 42 | 28.218 | 68 |
| 3 | 9, 10 | 49 | 26.961 | 93 |
| 4 | 11, 2 | 66 | 27.764 | 104 |
| 5 | 2, 11 | 40 | 26.201 | 83 |
| 6 | 7, 6 | 47 | 27.735 | 58 |
| 7 | 6, 10 | 50 | 27.167 | 68 |
| 8 | 2, 4 | 41 | 24.685 | 45 |

The v6 run (one advice, 14 positive spaces of the first 512 accepted, 132,138 round-2 passes, 1.008 x expected; it
had the decision rule "submit only if s0 >= 0.002") and pre-registration B (18 spaces of the nine A advices: 4,760
round-2 passes, 1.033 x expected; 3 collisions in 2 spaces) are consistent with C (v6: 0.0273 positive spaces per
space against C's 0.0299; B: 2 positive spaces of 18, probability 0.10 at C's rate). Neither enters Section 5; their
organizer replays (v10's r5-den, r5-replay, r5-replay8) are replaced by r5-C-0..4.

### 4.5 Certificates

16 certificates (distinct 135-byte messages, equal complete 5-round digests): 15 collisions of pre-registration C, in
(k, attempt) order (id r5-v11-c<k>-<attempt>-<coordinate>), and r5-v6-000038, whose first message r5-count uses.

### 4.6 Organizer experiments

r5.py holds the reference algorithm and all experiments (one file, 64,561 bytes). r5-C-* return real collisions. The
other 11 experiments check programs and counts and return sentinels: PASS (00^135, 01 || 00^134), FAIL (00^135, 02
|| 00^134).

| id | trials | PASS means | local public-seed result |
| --- | --- | --- | --- |
| r5-bp-0..4 | 2 per advice, then 32 connector attempts per advice | B' re-derives advice k of A from its label (candidate setup, accepting attempt, advice hash); one other logged attempt matches; an attempt with organizer-seeded coins is accepted and verified (Lemmas 1-2) | 18 of 18 B' checks; 196 of 288 attempts (descriptive; no bound uses this rate) |
| r5-bpfull | 2 | B' run 1 of A executed whole under its budget and CCAP: same output, counted cost equal to the log; with a 2^22-unit budget and a 2^21-unit candidate cap both caps act | 2 of 2 |
| r5-trail-0..3 | 1 each | P's counts of the group (T1 nodes per lane; cores, C1, P45 > 0, C2, T3 batches and groups) equal the log | 4 of 4 |
| r5-count | 28 | counted programs of E, T3, T2 against plain evaluations and their longest paths (trials 0-23, as in v10); P on sub-problems and its cap (24-27, 2.1) | 28 of 28 |
| r5-C-0..4 | 2 each | trial 0: the seed picks a positive space of C in the stratum; B' re-derives the advice from its label (hash, facts of Section 3), connector attempts 0..i are re-run and their status string matches the log's hash, and E's 2^12-coordinate window returns the collision at the logged coordinate. Trial 1: the seed picks a run completed by D; same, with only the accepting attempt i re-run (logged DF and work count) | 10 collisions (5 of C, 5 of D) |

The seeds pick which logged successes are replayed. In production the seed is the organizer's public seed, which is
known in advance, so the replays show that the picked spaces are outputs of the algorithm from their labels; they are
not a random audit.

Local runs (our check, not organizer evidence): experiments/runner.py with Python 3.12 in place of Docker, each
experiment executed twice by the runner with byte-identical output, on the public seed and on the nonces
"v11-nonce-1" .. "v11-nonce-4", which we wrote down before the first such runs. Every seed gives 18 of 18 B' checks,
2 of 2 (r5-bpfull), 4 of 4 (r5-trail), 28 of 28 (r5-count) and 10 full collisions (r5-C-0..4). Connector attempts
with seeded coins accepted: 196, 184, 181, 185 and 185 of 288 (descriptive). Over the five seeds, r5-C audited 16 of
C's 23 positive spaces and 18 of the 29 outputs of D, and each replayed; our replay of all 29 outputs of D with the
same trial-1 code returned 29 full collisions. Per experiment at most 9.7 CPU-s and 97 MB, measured with the five
seed runs in parallel on a shared machine (load about 47 on 15 cores, where wall time reached 19.5 s); the heaviest
experiments are r5-bp-0 and r5-C-0 (single-threaded).

## 5. Success probability (end to end, over the algorithm's own coins)

The probability space is the algorithm's coins: B' candidate coins and connector coins. The target is fixed, and P
and E are deterministic. A run of the algorithm is therefore a function of its coins, and p = Pr[the algorithm
outputs a collision].

Lemma 6 (each run of C, completed by D, is a complete run of the algorithm). For every k, the records of C and D are
the algorithm's execution with the label-derived coins:
- P's output is the trail of Section 3 (the deterministic premise of 2.1).
- B' started at candidate 0 with the full budget and gave an advice after at most 2^28.81 units, so its budget never
  acted.
- The connector rule kept that first advice: 96 accepted within at most 917 < 2^11 attempts, so neither A_ADV nor
  A_MAX acted.
- E ran on the 96 accepted spaces in order, stopping at its first output. fes is E on each space by Lemma 4, and the
  stage-2 cap never bound.
So "success" in the table of 4.3 is the algorithm's success on those coins. Our runs use the algorithm's own index
map, so they differ from the algorithm only in using SHAKE-256 words in place of fresh words (premise R).

Heuristic (claim.json):
- H1-end-to-end-success: p >= p0 = 0.874, under premise R of 4.1. Support: 46 of the 48 runs of C succeed. The runs
  use distinct labels, so their outcomes are independent, and the one-sided 95% Clopper-Pearson lower bound (exact
  binomial tail) is 0.8746. With run 999 included, 47 of 49 succeed and the bound is 0.8770. The organizer checks
  sampled successes of C and D through the replays r5-C-0..4 (4.6); every run, failures included, is in the table of
  4.3.

So Pr[success] >= 0.874 >= 0.40, with confidence 95%. The claimed 0.40 follows the rule of D's plan. It would still
be the 95% bound with as few as 26 successes in 48, that is, 20 more failures than observed. Every cap of Section 6
holds without H1.

Consistency (descriptive; no bound uses it):
- C found 23 positive spaces in 768, or 0.0299 per space.
- The trail predicts 1 - exp(-256 x 2^-13.2186) = 0.0265 per space: about 256 round-2 passes per space, each reaching
  alpha3 and then colliding with probability P45.
- If every advice had s = 0.0299, a run would succeed with probability 1 - (1 - 0.0299)^96 = 0.946. 46 of 48 = 0.958
  were observed.
- B' accepted 48 of 328 candidates, and no advice was discarded.

## 6. Time (collision-frontier-v5: one 5-round permutation = 1 unit, other primitives 1/1355)

| Term | Cap, enforced by | Count and price | log2 units |
| --- | --- | --- | --- |
| P: T1 | exact count N1 (organizer-recomputed) | 8,674,833 nodes x 2^12 (bound per node, as in v8) | 24.6443 |
| P: T2 | exact count C1 (organizer-recomputed) | 1,639,088,128 leaves x 166 (counted) | 27.5812 |
| P: T3 batches | batch counter at the exact count (organizer-recomputed) | 5,679,328,446 batches x 1,583 (counted, every batch) | 32.6274 |
| P: T3 full evaluations | F_CAP = 2^22 | 2^22 x 2^13 (bound, not counted) | 24.5959 |
| P: T3 group setup | 1411 groups (organizer-recomputed) | 1411 x 2^27 (bound, not counted; derived 2^25.2) | 27.0584 |
| P: setup |  | 2^31 primitives (bound) | 20.5959 |
| B' | WK counter, re-checked on every update | 2^32 units + one update (< 2^13 units) | 32.0000 |
| S | at most 4 advice rounds | 4 x 2^31 primitives | 22.5959 |
| Connector | 2^18 work units per attempt, A_MAX = 2^13 attempts | 2^13 x (2^18 x 96 + 2^15 x 2^9 + 2^22) primitives | 28.0554 |
| Bases | K = 96 spaces | 96 x 2^24 primitives | 20.1809 |
| E setup | K = 96 spaces | 96 x 2^24 primitives (bound, not counted; derived about 2^23.1) | 20.1809 |
| E stage 1 | 2^24 batches per space | 96 x 2^24 x 6,112 primitives (counted, every path) | 32.7583 |
| E stage 2 | S2CAP = 2^11 per space | 96 x 2^11 x (2 units + 2^11 primitives) | 19.3970 |
| Output | one pair | 2^22 primitives | 11.5959 |
| Total T | | | 34.1359 -> 34.14 |

K = 96 is v10's value, kept by the rule of pre-registration C (4.2); D measured the success at K = 96 (Section 5).

Every term is a cap or an exact count, times the longest counted path or a stated bound; no expected value is used,
and no count taken only from our runs enters except through a cap (F_CAP). Preprocessing (P + B' + S) = 2^33.3994,
claimed 33.40. Sensitivity (not the claim): with v8's prices for P (2 x its v8 bound) T would be 2^39.95; with v8's E
(594 per pair) 2^37.49; with the three uncounted setup bounds 4 times larger 2^34.17; charging B''s development
(Section 0) 2^38.29.

## 7. Memory

Measured peaks: P 7.5 MB (trail3b, both passes; the counted program's triple tables would take 2 x 2^15 x 107 words =
224 MB per group), B' at most 113.5 MB (run 2), connector under 2^23 bytes; E's tables 2 x 64 x 1024 x 16 words = 67
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
zero-advice framing with every phase inside a capped algorithm and development disclosed (used here), and the
early-abort order of the round-2 rows that v8's E used (v10's bitsliced E evaluates all 24 equations); Th0rgal is a
co-author of this package. None of 7deb1595's code, data or certificates is used. hybridnoise's note (ef4a0c66) showed
that an own-beta1 byte-aligned connector can work; jagnani73 (654cb3d2) taught us fresh coins, hard caps and
organizer experiments. baseline_improved is the required nominal reference ID, not a claim of dominance.

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

## Appendix B. E as run in pre-registrations C and D (fes.c)

fes.c (SHA-256 9a023ce614609bb9c27ba94683a6dc340f7a1324a3550ca4ba3f45775ae30de4, hashed in the plan of C) is an
exact form of E's stage 1 for evidence runs: f(c), the 24 residual bits at window coordinate c, has degree <= 4 in c
(round 0's output has degree <= 2, round 1's <= 4, and L is linear), so its algebraic normal form is the Moebius
transform of its values on the 41,449 coordinates of weight <= 4 with no assumption; coordinates 0..7 are bitsliced
and 8..31 enumerated by the degree-4 derivative recursion of fast exhaustive search. Every pass is printed;
espace.stage2 (Python, the experiment file's Linv_map and digest5) then compares complete digests. The driver
prereg_c.py (51ba941c...) calls the experiment file's bprime, Setup, attempt and enum_basis.

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

C's plan refers to the three heuristics H1-H3 of the v11 draft. Its runs are used as planned, but its analysis
is superseded by D's end-to-end measurement (4.2, Section 5).

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
