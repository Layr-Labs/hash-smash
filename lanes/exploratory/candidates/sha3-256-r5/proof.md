# 5-round SHA3-256: every phase inside the algorithm under a hard cap, time 2^34.14

Exploratory claim, with Th0rgal as co-author: Th0rgal 7deb1595 (with Subflatus3 and rubenmarcus) introduced on this
track the zero-advice framing used here. The algorithm runs every phase itself (trail search P, advice program B',
connector, enumeration E); each stops at a hard cap written into its code, and the claimed time is the sum of the
caps times counted prices. The algorithm reads nothing published. [GLL+20] = J. Guo, G. Liao, G. Liu, M. Liu, K.
Qiao, L. Song, "Practical Collision Attacks against Round-Reduced SHA-3", J. Cryptology 33 (2020), ePrint 2019/147.

## 0. Claim, summary, changes

| Field | Value | Basis |
| --- | --- | --- |
| time_log2 | 34.14 | sum of the phase charges, 2^34.1359, rounded up (Section 6) |
| success_probability | 0.40 | >= 0.67 under H1-H3 (Section 5) |
| preprocessing_log2 | 33.40 | P, B' and S: 2^33.3994, rounded up |
| memory_log2_bytes | 30 | largest phase about 2^28 bytes (Section 7) |
| nonuniform_advice_log2_bytes | 0 | the algorithm computes its trail and its connector advice |

Summary: P finds the trail (organizer-recomputed counts times counted worst-case prices; the one count the organizer
cannot recompute, P's number of full evaluations, enters only through its cap F_CAP = 2^22), B' builds the connector
advice (budget 2^32 units, at most 2^26 units per candidate), the v5 connector makes K = 96 affine spaces, and E tests
2^32 pairs per space, 256 pairs per 256-bit word, at 6,112 counted primitives per 256 pairs. Success uses s0 = 0.013
from the pre-registered v6 run (H1) and B' and connector rates from nine pre-registered B' runs (H2, H3), with v8's
evidence; H2 no longer assumes a per-candidate cost (it is a cap now).

What changed from v8 (40.26, on the board), and why each change is honest:

| Item | v8 | v10 | Why |
| --- | --- | --- | --- |
| E, per 256 pairs | 256 x 594 (one pair per word, worst early-abort path) | 6,112: bitsliced, every path | the same 2^32 pairs and the same 24 equations, now 256 pairs per 256-bit word (2.4); r5-count checks every equation word against a plain evaluation |
| P's charge | 2 x (exact counts x per-item price bounds), T3 leaf priced 2^9 | exact counts x counted prices, T3 in bitsliced batches at 1,583 primitives per batch of up to 256 leaves, every batch charged in full; full evaluations at F_CAP = 2^22 | P is deterministic; the batch, group and leaf counts are recomputed by r5-trail-0..3 and the prices by r5-count |
| B' | budget 2^34 units; per-candidate cost <= 2^26.85 units assumed in H2 | budget 2^32 units; per-candidate cap CCAP = 2^26 units in the WK counter | H2 becomes a rate only; every logged candidate (largest 2^25.848 units) is below the cap |
| K; connector caps | 128; 2^12 attempts per advice, 2^16 in all | 96; A_ADV = 2^11, A_MAX = 2^13 | trades E against success under v8's H1: the claim needs s >= 0.0060, 2.2 times below s0 (v8: 3.3) |
| Time | 40.26 | 34.14 | |

A v9 draft (34.40, never submitted) charged T3's second stage only on 1.5 times a batch count taken from our native
run, and two of its counted prices were one primitive below the longest path; review found both, and v10 removes the
first and corrects the second.

Nothing that enters the success probability changed except the caps above: E's output on a space is the same function
of the space as in v6 and v8 (Lemma 4), P's output is the same trail (Section 2.1), and the advice and connector
programs are v8's (the experiment file differs from v8 only in the caps B_BUDGET, CCAP, K, A_ADV, A_MAX, in the control
flow of bprime and algorithm() that enforces them, and in omitting docstrings and comments). No logged run reached a
cap. The claimed 0.40 needs s >= 0.0060 per space (2.2 times below s0) and, at s = s0, q >= 0.0258 per B' candidate
(2.9 times below q_c0).

Development runs (not charged, unchanged from v8). B' has six design constants: R = 16 attempts per candidate, DMIN
= 40, and the D2u ordering weights KW = 1.0, MW = 0.25, LB = 1.0, PREF = 1.0. Development runs on 2026-10-06 before
09:01Z (75 processes, 1,559 CPU-s) chose them; some used the published [GLL+20] difference as a test case. Uncharged
v5 runs also set the connector's DMIN = 33 (the least DF for which E's window exists) and its 2^18 work-unit cap
(charged in full, never bound: largest of 1,152 attempts 179,180). The algorithm reads no output of development runs
except these numbers, and every success rate used here comes from runs made after they were fixed. 7deb1595 used this
framing (zero advice, development uncharged and disclosed). Sensitivity (not the claim; 2^38 primitives per
core-second): charging the 1,559 CPU-s of B' development adds 2^38.20 units (T = 2^38.29, still below 40.26 and
42.19); v7's whole development ledger (12,527 CPU-s) gives T = 2^41.22. The new constants of v9 and v10 (batch layouts
of E and T3, CCAP, K, A_ADV, A_MAX, B_BUDGET) only change cost or caps; they were set by counting and by the bound of
Section 5, with no new run. The two native runs of P (2.1, Appendix A; 7,598 and 11,823 CPU-s) are executions of P,
whose cost is charged in full.

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
slot p. A batch (t3_batch in r5_trail.py, counted):

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

Counts of T3. Every count in P's charge except F (the number of full evaluations) is recomputed by the organizer
(batches and groups by r5-trail-0..3, prices by r5-count). F depends on T3's decisions and enters only through
F_CAP. We ran the batch program natively (trail3b, Appendix A) in two passes over all 5,679,328,446 batches. Pass 1 runs
every core from T = infinity and gives each core's exact minimum (the global minimum 127 is core No. 349, the 18th
kept core; the running minima before it are 287, 274, 263); its F = 1,896,302 is an upper bound on the algorithm's F,
because at every batch the algorithm's T is at most pass 1's. Pass 2 runs core i from T = the minimum over the cores
before it, which is exactly the algorithm's T, and counts F = 770. Both passes output the trail of Section 3 (w1 =
127, w2 = 24, unique). Stated premise (a deterministic fact, not a probability): P outputs the trail of Section 3 with
F <= F_CAP = 4,194,304 (2.2 times pass 1's bound, 5,447 times pass 2's count). The organizer cannot re-run the
minimisation (1.4 x 10^12 leaves); Appendix A gives the commands, sources, CPU times and the SHA-256 of both per-core
logs, r5-trail-0..3 recompute every count that is not a T3 decision, r5-count executes the batch program against a
plain evaluation, and Section 3 checks w1 = 127. If F exceeded F_CAP, P would stop without output: the cost bound
holds either way.

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
units above 2^22). All 65 candidates of the nine pre-registered B' runs cost at most 2^25.848 units and every run at
most 2^28.22 units, so they are runs of the capped 2^32-unit program as well.
Coins: fresh 256-bit words in the algorithm (counted as 32
primitives each); in our runs, Coins(SHA-256(label || "beta1" || c)) and Coins(SHA-256(label || "att" || c || j))
(Section 4.1). WK's 2 units per SHA-256 compression is below the 3.3 units of a 64-round compression at the organizer's
sha256-r32 price; a run makes at most 2 compressions per attempt or candidate, and an attempt counts at least 302
units, so our runs' counts are within 0.9% of their true cost. The algorithm computes no SHA-256. Restart: when an
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
run of Section 4 (bf.cpp, bf8.cpp, the Python e_window) is a run of this E for the purpose of H1.

### 2.5 Main loop and correctness

Run P. Base S. Advice rounds (2.2, 2.3) until K = 96 accepted spaces of one advice, or until B''s budget or A_MAX is
exhausted (then fail). Run E on the K spaces in order and halt with the first output; if there is none, fail.
algorithm() in the experiment file is this driver with every cap (its E is the plain evaluation e_window, Lemma 4).
Lemma 1 (outputs are collisions): for x in V, A0 = L^-1(x) satisfies the fixed-bit equations, and so does A0 +
L^-1(beta), since E_D forces (L^-1 beta)_j = 0 on F; beta != 0; E compares the true 256-bit digests. Lemma 2 (used only
for the probability): for x in V the difference after round 1 is alpha2. Lemma 3: beta is not in W, so the 2^32
pairs of a space are distinct.

## 3. Exact facts (recomputed before the connector trials of every r5_connector experiment)

alpha3 = bits {0, 130, 450, 529, 701, 789, 1021, 1169, 1280, 1429}; nonzero lanes of beta2 in hex 0:1 2:4 5:4 6:4 7:4
8:20000 10:2000000000000000 12:200000 15:2000000000000000 18:20000 20:200001 22:200000 24:1. alpha3 and beta3 =
L(alpha3) are in the CP kernel (10 bits each); beta2 -> alpha3 on the same 10 rows, w2 = 24 (row 66 weight 4, rows 256
and 277 weight 3, the rest 2); alpha2 = L^-1(beta2) has 59 active rows and w1 = 127; C2 = 3^20 for this core. P45 =
sum over the 2^19 alpha4 compatible with beta3 of Pr[beta3 -> alpha4] x prod over nonzero digest-plane rows q of
L(alpha4) of (DDT[q][0] + DDT[q][16])/32 = 55/2^19 = 2^-13.2186 (192 nonzero terms); with w2, p_M = 2^-37.2186 per
pair. Advice facts, for each advice used: beta1' -> alpha2 has weight 127 on the 59 rows; beta0' is compatible with
alpha1' on every row and zero on its inactive rows; alpha0' = L^-1(beta0') is nonzero and zero on F.

## 4. Executed evidence (none of it is the claimed cost)

### 4.1 Coins in our runs

Attempt i of a labelled run uses seed_i = SHA-256(label || i as 8 little-endian bytes) and words SHAKE-256(seed_i
|| k) (class Coins); B' runs use the seeds of 2.2. In the algorithm every coin is a fresh uniform 256-bit word;
Fisher-Yates index j = (low 64 bits) mod (i+1).

### 4.2 Runs after the constants were fixed (unchanged from v8)

| Run | Pre-registered | Used for |
| --- | --- | --- |
| B' with LABEL_B = "hashsmash sha3-256-r5 v6 B-prime advice run 1" | 2026-10-06T09:01Z | the advice of the v6 run (k = 0 below) |
| v6 full-scale run, LABEL = "hashsmash sha3-256-r5 v6 run" | 09:19Z | s0 (H1): 14 of the first 512 accepted spaces |
| Pre-registration A: B' runs k = 0..8 + 128 connector attempts each | 15:29:17Z (sha256 fcfd7d64...) | H2, H3 |
| Pre-registration B: E check on 2 spaces per advice + 2 v6 spaces | after A (sha256 2f2deebf...) | support for H1 across advice |

The v6 full-scale run: 960 of 1024 attempts accepted; the first 512 accepted spaces, enumerated over their 2^32
windows, gave 132,138 round-2 passes (1.008 x expected, variance/mean 1.02, at most 301 per space) and 14 collisions.
s-hat = 0.0273; one-sided 99% Clopper-Pearson lower bound 0.0133; s0 = 0.013. r5-den-0..2 re-run all 538 attempt
indices up to the 512th acceptance (the whole denominator); r5-replay re-derives the 14 positives. Its decision rule
(submit only if s0 >= 0.002) is disclosed; this is H1's outcome-selection premise. A fault of the C++ E (bf.cpp in the
v6 run, bf8.cpp in 4.3) could only lose positives and lower s-hat: every positive is replayed at its coordinate by the
Python E (r5-replay, r5-replay8) and the denominator is re-run (r5-den).

Pre-registration A (r5c.py, bprun.py, cnrun.py hashed before the runs; up to docstrings, r5c.py's algorithm functions
are AST-identical to v8's experiment file, except that Setup takes the advice as arguments, e_window has the stage-2
cap and algorithm(), which no run used, has the budget correction of v8; v10's file changes only the caps B_BUDGET,
CCAP, K, A_ADV and A_MAX and the control flow of bprime and algorithm() that enforces them, and no pre-registered run
reached a cap). Nine B' runs started together; none was stopped, excluded or repeated.
Costs are exact counts. Neither pre-registration had a rule about submitting.

| k | label | c, j | DF | attempts | B' cost (log2 units) | largest candidate | CPU-s | connector accepted / 128 | conn. DF | 99% CP lower |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | LABEL_B | 5, 9 | 41 | 90 | 27.118 | 25.542 | 41.6 | 120 | 40-42 | 0.868 |
| 1 | fresh run 1 | 0, 2 | 42 | 3 | 23.445 | 23.445 | 3.4 | 105 | 39-42 | 0.727 |
| 2 | fresh run 2 | 14, 5 | 42 | 230 | 28.218 | 25.612 | 84.0 | 68 | 40-42 | 0.425 |
| 3 | fresh run 3 | 9, 10 | 49 | 155 | 26.961 | 25.226 | 39.6 | 93 | 42-48 | 0.624 |
| 4 | fresh run 4 | 11, 2 | 66 | 179 | 27.764 | 25.848 | 63.4 | 104 | 65-67 | 0.719 |
| 5 | fresh run 5 | 2, 11 | 40 | 44 | 26.201 | 24.940 | 21.7 | 83 | 39-40 | 0.542 |
| 6 | fresh run 6 | 7, 6 | 47 | 119 | 27.735 | 25.617 | 61.6 | 58 | 39-45 | 0.349 |
| 7 | fresh run 7 | 6, 10 | 50 | 107 | 27.167 | 25.403 | 43.5 | 68 | 48-51 | 0.425 |
| 8 | fresh run 8 | 2, 4 | 41 | 37 | 24.685 | 24.315 | 8.3 | 45 | 39-42 | 0.255 |

"fresh run k" = "hashsmash sha3-256-r5 v8 B-prime fresh run k"; connector label "hashsmash sha3-256-r5 v8 conn run k". k
= 0 reproduces the v6 advice bit for bit. Totals: 65 candidates, 9 accepted (q_c-hat = 0.138, one-sided 95% CP lower
bound q_c0 = 0.0742); largest candidate c_max = 2^25.848 units; largest B' run 2^28.218 units, 2^3.8 below the v10
budget; 744 of 1,152 connector attempts accepted, all verified (Lemmas 1-2 on two solutions); largest attempt 179,180
work units and 4,460 coin words. Every advice is "good" (99% CP lower bound >= 0.10), so f_up = one-sided 95% CP upper
bound of 0/9 = 0.2831. B' failure bound at the v10 budget: every candidate
stops at CCAP plus one update, so n = floor(2^32 / (2^26 + 2^13)) = 63 candidates fit, and (1 - q_c0 (1 - f_up))^63 = 0.0320 (v8: 142 candidates, 0.00043).

### 4.3 Pre-registration B: E check (unchanged from v8)

bf8 enumerated the full 2^32 window of the first 2 accepted spaces of each advice k = 0..8, and of v6 spaces 0 and 1
(20 spaces, 2^36.3 pairs).

| Advice k | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | v6 spaces |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| round-2 passes (2 spaces; 512 expected) | 506 | 542 | 533 | 562 | 576 | 526 | 514 | 502 | 499 | 547 (= 271 + 276, as in v6) |
| collisions | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |

Pooled over the 18 v8 spaces: 4,760 round-2 passes vs 4,608 expected (ratio 1.033, inside the pre-registered 99%
interval [0.994, 1.072] but 2.2 Poisson standard deviations above 1; advice 4 alone is 2.8 above); at most 307 per
space; the stage-2 cap never bound. Three collisions (advice 4 twice, both in its first space, attempt 0; advice 7
once); r5-replay8 re-derives the advice from its label, re-runs the connector attempt and replays all three. At the v6
rate (0.027 per space) three or more collisions in the 16 spaces of fresh advice has probability about 0.01, and two in
one of 18 spaces about 0.007. So rates may vary between advices and spaces more than an independent-pair model
predicts; s (H1) counts spaces with at least one collision. As pre-registered, these spaces do not enter s0.

### 4.4 Certificates

16 certificates (distinct 135-byte messages, equal complete 5-round digests): the 3 collisions of 4.3
(r5-v8-r4-000000-13c3cc2f, r5-v8-r4-000000-9707a665, r5-v8-r7-000002-1e5fa912: run k, attempt, window coordinate) and
13 of the 14 v6 collisions (r5-v6-<attempt>; attempt 462 is left out by the 16-certificate limit and replayed by
r5-replay).

### 4.5 Organizer experiments

r5_connector.py: reference algorithm and experiments; r5_trail.py: P recount and the counted programs. PASS returns
the sentinel (00^135, 01 || 00^134), whose digest XOR is the declared mask value; FAIL returns (00^135, 02 || 00^134).
The evidence is the organizer's execution of the visible code.

| id | trials | PASS means | local public-seed result |
| --- | --- | --- | --- |
| r5-bp-0..4 | 2 per advice, then 32 connector attempts per advice | B' re-derives advice k from its label (candidate setup row count, the accepting attempt's status, DF and row count, advice hash); one other logged attempt of that candidate matches; an organizer-seeded attempt is accepted and verified | 18 of 18 B' checks; 196 of 288 attempts |
| r5-bpfull | 2 | B' run k = 1 executed whole under its budget and CCAP: same output, counted cost equal to the logged one; with a 2^22-unit budget and a 2^21-unit candidate cap, candidate 0 stops within one update above 2^21, candidate 1 starts, and B' stops with no output within one update above 2^22 | 2 of 2 |
| r5-den-0..2 | 180, 180, 178 | v6 attempt i accepted with the logged DF (FAIL: rejected as logged) | 512 PASS of 538 |
| r5-replay | 14 | full collision: v6 positive replayed | 14 collisions |
| r5-replay8 | 3 | full collision: v8 E-check positive replayed | 3 collisions |
| r5-trail-0..3 | 1 each | P's counts of the group (T1 nodes per lane; cores, C1, P45 > 0, C2, T3 batches and groups) equal the log | 4 of 4 |
| r5-count | 24 | E batch (trials 0, 3, ...): a seeded space with the certificate's x at a seeded slot; every one of the 24 equation words equals a plain evaluation (one third of the 256 pairs per trial), the slot passes, count 6,072 + control 40. T3 batch (1, 4, ...): the output core, a seeded group and outer Gray position, four batches at seeded thresholds: AS of every slot and the pass word equal a plain evaluation, the maintained base equals L^-1 of the outer rows, count with the Gray step <= 1,583; longest paths, measured on every such trial: the comparison over all 513 tau classes 74, the batch over all 513 tau classes (synthetic group) 1,539, the Gray step's longest branch 44, and 1,539 + 44 = 1,583. T2 leaf (2, 5, ...): three leaves of the output core from a seeded Gray position; decision and maintained digest-plane words equal a plain evaluation, count <= 166 | 24 of 24 |

Local run of the organizer runner (experiments/runner.py with a local Python 3.9 executor in place of Docker, public
seed, each program run twice; identical results): every success count in the table, at most 8.0 CPU-s and 90 MB per
experiment (r5-bp-0); the r5-trail parts at most 7.4 CPU-s, r5-bpfull 6.3 CPU-s, r5-count 2.9 CPU-s. Source texts
64,866 bytes.

## 5. Success probability

Theorem (under H1-H3). Pr[the algorithm outputs a collision] >= 0.67. The heuristics (mirrored in claim.json, as in
v8) enter only the success probability; no cost cap depends on them:
- H1-space-success: for each advice B' can output, per accepted space E outputs a pair with probability >= s0 = 0.013
  (a bound per advice, not an average over advices: (e) needs s >= 0.0060 for the final advice). Evidence 4.2 (v6 run,
  14 of 512; r5-den-0..2, r5-replay, r5-bp-0) and 4.3 (9 advices, round-2 rate 1.033 x the trail value, 3 collisions,
  r5-replay8); by Lemma 4 these are runs of v10's E. Premises: E depends on the advice only through alpha2 (Markov);
  seeded coins act as fresh; the v6 decision rule (disclosed) did not bias s-hat beyond the 99% bound. Limits: s0 is
  measured on one advice; 4.3 shows more variation between advices and spaces than an independent-pair model predicts
  (all of it upward).
- H2-bprime-runs: B' candidates are independent, each yields an accepted advice within its cap CCAP = 2^26 units with
  probability >= q_c0 = 0.0742, so (b) <= 0.0320. Evidence 4.2 (all 65 logged candidates ended below the cap),
  r5-bp-0..4 and r5-bpfull. v8's per-candidate cost premise is now the cap of 2.2. The claim needs q >= 0.0258 (at s =
  s0).
- H3-connector-acceptance: a B' advice has connector acceptance q >= 0.10 except with probability <= f_up = 0.2831 (0
  of 9 bad; 45-120 of 128 accepted; 288 organizer-seeded attempts in r5-bp-0..4).

Failure needs one of:
- (a) P stops at a cap. Every count of P except F is exact and its counter never binds; F <= F_CAP is the
  deterministic premise of 2.1 (pass 2: 770; pass 1, an upper bound: 1,896,302; F_CAP = 4,194,304). 0 under it.
- (b) B' exhausts 2^32 units before a good advice (connector acceptance q >= 0.10): <= 0.0320 (H2; restarts included).
- (c) More than 3 advice rounds: <= f_up^4 = 0.0065 (H3).
- (d) A good advice gives fewer than 96 accepted attempts in 2^11: Chernoff with mean >= 204.8, exp(-28.9) < 2^-41.
- (e) E outputs nothing on the 96 spaces of the final advice: (1 - s0)^96 = 0.2848 (H1; the spaces are i.i.d. given
  the advice, because the attempts use independent coins).
- (f) Coin map: each Fisher-Yates index is within (i+1)/2^64 of uniform; with at most 2^38.4 coin words in B' and 2^29.5
  in the connector, all on lists of fewer than 2^12 elements, the total variation is below 2^-13.

So Pr[success] >= 1 - 0.0320 - 0.0065 - 2^-41 - 0.2848 - 2^-13 > 0.67. The claim 0.40 holds for any s >= 0.0060, 2.2
times below s0, and (at s = s0) for any q >= 0.0258, 2.9 times below q_c0. At s-hat = 0.0273 the bound is 0.89.

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
Van Assche (FSE 2012) and KeccakTools for in-kernel trail cores. Th0rgal 7deb1595 (with Subflatus3 and rubenmarcus): the
zero-advice framing with every phase inside a capped algorithm and development disclosed (used here), and the
early-abort order of the round-2 rows that v8's E used (v10's bitsliced E evaluates all 24 equations); Th0rgal is a
co-author of this package. None of 7deb1595's code, data or certificates is used. hybridnoise's note (ef4a0c66) showed
that an own-beta1 byte-aligned connector can work; jagnani73 (654cb3d2) taught us fresh coins, hard caps and
organizer experiments. baseline_improved is the required nominal reference ID, not a claim of dominance.

## Appendix A. Trail search P as run (C++17; shared helpers kc.h)

Run as `trail1c 10 > cores; trail2c < cores > t2; trail3b U 15 u_inf < t2 > pass1; trail3b U 15 u_seq < t2 > pass2`,
where u_inf holds 2^30 for every kept core and u_seq the running minimum of the pass-1 minima of the earlier cores
(Section 2.1). T1 and T2 are v8's programs (their caps are v8's and never bind; P is charged its exact counts). T2's
charged form is the counted Gray program of r5_trail.py (same leaves, same decision P45 > 0); trail2c also prints
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

## Appendix B. E as run in our evidence (bf8.cpp)

bf8.cpp (sha256 480ad1a16d6f790561ac2ee5808d5ca226b6283510c9ec7208673ba6d33593fc, fixed in pre-registration B; uses kc.h
of Appendix A) is a multithreaded C++ form of v8's E used only for the E check of 4.3; its source is left out for
length. It tests the same pairs and predicate as v10's E (Lemma 4): on v6 spaces 0 and 1 its stage-2 counts equal the
v6 E's (271, 276), and its three collisions are replayed from their labels by r5-replay8.
