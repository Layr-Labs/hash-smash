# 5-round SHA3-256: every phase inside the algorithm under a hard cap, time 2^40.26

Exploratory claim, with Th0rgal as co-author: Th0rgal 7deb1595 (with Subflatus3 and rubenmarcus) introduced on this
track the zero-advice framing and the early-abort row order used in E. The algorithm runs every phase itself (trail
search P, advice program B', connector, enumeration E); each stops at a hard budget written into its code, and the
claimed time is the sum of the budgets. The algorithm reads nothing published. [GLL+20] = J. Guo, G. Liao, G. Liu, M.
Liu, K. Qiao, L. Song, "Practical Collision Attacks against Round-Reduced SHA-3", J. Cryptology 33 (2020), ePrint
2019/147.

## 0. Claim, summary, changes

| Field | Value | Basis |
| --- | --- | --- |
| time_log2 | 40.26 | sum of the phase budgets, 2^40.2557, rounded up (Section 6) |
| success_probability | 0.40 | >= 0.81 under H1-H3 (Section 5) |
| preprocessing_log2 | 39.97 | budgets of P, B' and S: 2^39.9601, rounded up |
| memory_log2_bytes | 30 | largest measured peak of any phase 113.5 MB (Section 7) |
| nonuniform_advice_log2_bytes | 0 | the algorithm computes its trail and its connector advice |

Summary: P finds the trail (budget 2 x its counted bound), B' builds the connector advice (budget 2^34 units), the v5
connector makes K = 128 affine spaces, and E tests 2^32 pairs per space at <= 594 counted primitives each. Success
uses s0 = 0.013 from the pre-registered v6 run (H1) and B'/connector rates from nine B' runs under a new
pre-registration (H2, H3).

How v8 charges differently from v7 (45.33), and why:

| Item | v7 | v8 |
| --- | --- | --- |
| Framing | 614 bytes of advice, built outside the algorithm | no advice: P and B' are phases of the algorithm |
| Trail search P | 32 x its count (2^43.94) | 2 x its counted bound (2^39.94): exact node and leaf counts (organizer-recomputed, capped by counters) x per-item price bounds (T3 leaf: counted program) |
| B' and its development | all advice work as the capacity of one machine over a 6,600 s window (2^44.21) | B' at its budget 2^34; development runs are not charged (below) |
| E per pair | 3 units + 256 primitives, both digests for every pair | worst-case path of the counted early-abort program, 594 primitives; digests only for round-2 passes, at most 2^11 per space |
| Spaces | K = 512 | K = 128, with a restart rule for weak advice |

Development runs (not charged). B' has six design constants: R = 16 attempts per candidate, DMIN = 40, and the D2u
ordering weights KW = 1.0, MW = 0.25, LB = 1.0, PREF = 1.0. Development runs on 2026-10-06 before 09:01Z (75
processes, 1,559 CPU-s with the steering check in v7's ledger) chose them; some used the published [GLL+20] difference
as a test case. Uncharged v5 runs (with the published pair) also set the connector's DMIN = 33 and its 2^18 work-unit
cap. Neither carries information: 33 is the least DF for which E's 32-dimensional window and beta exist, and the cap is
charged in full and never bound (largest of 1,152 v8 attempts: 179,180). These are the only constants fixed by
uncharged runs. B''s structure, its budget and every cap were set by analysis and are charged in full; P's rules (cores
of at most 10 bits, least w1) follow [GLL+20] and in-kernel trail practice; trail2c's C1 filter (c1max = 30) never
applies (largest log2 C1 is 20). v7 said the opposite about the six B' constants (that they "were set by runs inside
the window and are charged with it"); v8 reverses that statement. Reason: the algorithm reads no output of the
development runs except these six numbers, and every success rate used here comes from runs made after they were
fixed: the v6 full-scale run (pre-registered 09:19Z, after the B' run of 09:01Z) and pre-registrations A and B
(Section 4). 7deb1595 used this framing (zero advice, development uncharged and disclosed) and was rated
plausible_not_refuted. Sensitivity (not the claim; 2^38 primitives per core-second as in v7): charging the 1,559 CPU-s
of B' development gives T = 2^40.57, v7's whole development ledger (12,527 CPU-s) 2^41.81, and v7's machine-capacity
window (2^44.21) 2^44.30.

## 1. Target, messages, notation

sha3-256-r5-prefix-v1 is FIPS 202 SHA3-256 restricted to rounds 0-4 of Keccak-f[1600]: rate 1088, capacity 512, zero
initial state, suffix 0x06 with pad10*1, digest = lanes 0..3 after the 5 rounds. Round i maps A to chi(L(A)) xor
RC[i], with L = pi o rho o theta. State bit (x,y,z) has index 64(x+5y)+z. chi acts on the 320 rows (y,z) by chi5(v)_i
= v_i xor (NOT v_{i+1}) v_{i+2}. All messages are exactly 135 bytes: A0 = M || 0x86 || 0^512, so the 520 bits F =
1080..1599 are fixed (1081, 1082, 1087 are 1). For a pair, alpha_i is the difference entering round i, beta_i =
L(alpha_i) the difference entering chi. DDT[d][o] = #{v : chi5(v) xor chi5(v xor d) = o}; V(d,o) = {v : chi5(v) xor
chi5(v xor d) = o} is an affine set of dimension log2 DDT[d][o], so a row transition is w = 5 - log2 DDT affine
equations on one message's row value. x = L(A0) is the first message's round-0 chi input.

## 2. The algorithm and its budgets

Phases: trail search P (2.1), advice program B' (2.2), setup S and connector (2.3), enumeration E (2.4), driver
(2.5). Section 6 lists every hard cap, how the code enforces it, and its charge.

### 2.1 Trail search P (budget 2 x its counted bound)

P outputs the 2-round in-kernel core alpha3 and the beta2 that minimise w1. T1 (cores): a candidate alpha3 is a set of
at most 10 bits whose alpha-columns and beta-columns (columns of pi o rho of each bit) all hold an even number of
bits; depth-first search from bit (lane, z = 0) for each of the 25 lanes; at a node let c be the smallest odd
alpha-column, else the smallest odd beta-column; if none, record the core in canonical form (least sorted bit list
over the 64 z-translations), else, below 10 bits, branch on each bit of c not yet in the set. T2 (forward): beta3 = pi
o rho(alpha3); enumerate every alpha4 compatible with beta3 (C1 leaves), accumulate P45 (Section 3) and keep the cores
with P45 > 0. T3 (backward): for each kept core enumerate every beta2 compatible with alpha3 (C2 leaves) in reflected
mixed-radix Gray order with alpha2 = L^-1(beta2) maintained incrementally; compute w1 only when 2 AS(alpha2) does not
exceed the best w1 so far. Output: least w1, ties to the smaller w2, then the smaller choice vector.

| Stage | Count | Budget (2 x) | Organizer recomputation |
| --- | --- | --- | --- |
| T1 | N1 = 8,674,833 nodes; 1741 cores; 17,100 core events | 17,349,666 nodes | r5-trail-0..3: every node, per lane, and the core set |
| T2 | C1 = 1,639,088,128 leaves; 467 cores with P45 > 0 | 3,278,176,256 leaves | C1 per core, and P45 > 0 decided exactly per core |
| T3 | C2 = 1,379,275,399,350 leaves | 2,758,550,798,700 leaves | C2 per kept core (T3 visits exactly C2 leaves per core) |
| Output | w1 = 127 by one core and one beta2 (w2 = 24): core No. 3 of [GLL+20] | | facts of Section 3 |

Prices (word RAM, Appendix A); the counts are exact, the prices are per-item upper bounds. A T3 leaf costs at most
2^9 primitives. r5-ecount (trials 90-91) executes a counted form of one pass of T3's loop: the step counters and
threshold, m0 = 9 leaves on the longest path that does not compute w1 in full (per plane 5 loads, 5 XOR, 4 OR, a
17-operation popcount, add, shift, comparison and branch: 35), and the Gray step on its longest branch (25 loads and
25 XOR into alpha2, the Gray-state and w2 updates): 1,750 primitives, 194.5 per leaf. 9 is the smallest row-0 fan-in,
so every Gray step is amortised over at least 9 leaves. The 545 leaves on which w1 is computed in full cost at most
2^12 each. A T2 leaf costs at most 2^12: 64 row extractions with their loads, test and loop step (at most 30 each);
every probability factor is a power of two (DDT entries of chi are powers of two), so each of at most 64 products is
an exponent addition (at most 9 primitives with the table load); one floating-point addition (at most 2^8 emulated);
its share of the recursion (at most 60, since every node has at least 4 children); in all at most 2,812. A T1 node
costs at most 2^9 outside the 17,100 core events; a core event (canonical form over 64 translations, set insertion)
costs at most 2^15, and N1 x 2^9 + 17,100 x 2^15 < N1 x 2^12. Setup (DDT, L^-1 by elimination, per-core tables) is
below 2^31. So P's counted bound is

    C2 x 2^9 + C1 x 2^12 + N1 x 2^12 + 2^31 = 712,940,389,039,104 primitives = 2^38.937 units,

and its budget is twice that: 1,425,880,778,078,208 primitives = 2^39.937 units. In Appendix A, T1 stops above 2 N1
nodes, T2 above 2 C1 leaves, T3 above 2 C2 leaves. The capped T1 and T2 reproduce the October 6 outputs byte for byte;
the capped T3 reproduces the output core's line (w1, w2, leaves, beta2) on a subset of 8 kept cores (the uncapped T3
ran once, 10,181 CPU-s). r5-trail-0..3 (a partition of the cores) reproduce N1, 1741, C1, 467 and C2 exactly; the T3
minimisation itself (1.4 x 10^12 leaves) is not re-executed, and Section 3 checks w1 = 127. Context (not the charge):
the shipped T3 on the output core alone (3^20 leaves) retires 62.5 ARM64 instructions per leaf and reproduces its line.
If every price of P were doubled, T would be 2^41.11.

### 2.2 Advice program B' (budget 2^34 units)

B' (experiment file, rand_min_beta1 to bprime) is v6's program with a budget in place of v6's 400-candidate limit. Its
only inputs are P's trail and the fixed bits F. For candidate c = 0, 1, ...:
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
WK raises BudgetExceeded on the first counter update that takes B''s cost above 2^34 units, so B' spends at most 2^34
units plus one update (the largest update inside B' is below 2^13 units). r5-bpfull executes bprime() whole: run k = 1
from its label (counted cost equal to the logged 15,477,633,191/1355 units, same output), and with a 2^20-unit budget
(stops with no output, 100.4 units above the budget). Coins: fresh 256-bit words in the algorithm (counted as 32
primitives each); in our runs, Coins(SHA-256(label || "beta1" || c)) and Coins(SHA-256(label || "att" || c || j))
(Section 4.1). WK's 2 units per SHA-256 compression is below the 3.3 units of a 64-round compression at the organizer's
sha256-r32 price (2,224 primitives per 32 rounds); a run makes at most 2 compressions per attempt or candidate, and an
attempt counts at least 302 units (copying the 1,600-entry difference space; attempts of a candidate whose round-1
system is inconsistent stop at once, and its setup counts at least 2^18 units), so our runs' counts are within 0.9% of
their true cost. The algorithm computes no SHA-256. Restart: when an advice is discarded (2.3), B' resumes at the next
candidate under the same budget; the connector's work is charged to its own term, not to B''s budget.

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

Advice rounds: run attempts on the current advice until K = 128 are accepted; if 2^12 attempts give fewer, discard it
and resume B'. At most A_max = 2^16 attempts in all, so at most 16 advice rounds.

### 2.4 Enumeration E (early-abort stage 1, counted)

Space and window: V = solutions of E_M, beta = beta0; offset v0 = the solution with all free variables 0; b_i =
(solution with free variable i set) + v0, kept if independent of beta and the earlier ones; W = span of the first 32
kept b_i. E enumerates x in v0 + W in Gray order (2^32 pairs (x, x + beta)).

Stage 1, per pair: x ^= b_j (25 loads, 25 XOR); round 0 (chi, iota) on x into 25 fresh registers; round 1 in full;
then the 24 equations of the 10 rows of beta2 (u_r in V(beta2_r, alpha3_r), u = L(round-1 output)) in this order: row
(1,2) (= row 66, weight 4), then row (1,17) (= row 81), then the other 8 rows (EQS in r5_trail.py). This row order is
the early-abort order of Th0rgal 7deb1595. Each equation uses only the bits of u it needs: bit u[X,Y,z] is bit 0 of
b[i] >> k xor C[xs-1] >> k xor C[xs+1] >> (k-1), where (xs, ys) = (3(Y - 3X) mod 5, X) is the rho-pi source lane i, k
= z - rho_i, and the column parities C of the round-1 output b are computed on first use. The pair stops at the first
failing equation.

Count (r5_trail.py, organizer-executed as r5-ecount). The counted program uses the organizer convention: every
XOR/AND/OR/NOT, shift, load, comparison and conditional branch is one primitive, and a 64-bit rotation by r != 0 is
((v << r) | (v >> (64 - r))) & M (4 primitives). Register use: x (25), the round values (25, written into registers
freed by their sources), D or C (5), 5 rotation outputs, 2 temporaries and M: at most 63 of the 64 registers, so the
only loads are the 25 basis lanes. Exit k (first failing equation) costs COST[k] = 384, 400, 418, 427, ..., 593
primitives (24 = all pass: 593). The Gray loop is unrolled by 16; each block boundary costs 15 (counter, m & -m, a
5-level comparison tree, loop test). So every pair costs at most 593 + 15/16 < 594 primitives, which is the charge
(expected 398.625 with uniform round-2 rows; context only).

Our own count vs 671. 7deb1595 reports 671 primitives per pair with this row order (962 without early abort),
including 150 loads and stores. Ours is lower because the state stays in registers (only the 25 basis lanes are
loaded), round 0 needs no theta, chi takes 3 primitives per lane (the mask after chi is redundant on reduced
operands), and round 2 computes only the bits the tested equations use. We charge our worst case, 594.

Stage 2: if all 24 equations hold, form x + beta and both complete 5-round digests (round 0 of the first message is
reused; 2 units and at most 2^7 primitives), compare all 256 bits, and output the pair (bytes 0..134 of L^-1(x) and
L^-1(x + beta)) if they are equal. At most S2CAP = 2^11 stage-2 pairs per space (then E stops on that space); the
largest observed is 307 (256 expected). Our runs used bf8.cpp (Appendix B), checked against the counted program.

### 2.5 Main loop and correctness

Run P (stop if its budget is exhausted). Base S. Advice rounds (2.2, 2.3) until K = 128 accepted spaces of one advice,
or until B''s budget or A_max is exhausted (then fail). Run E on the K spaces in order and halt with the first output;
if there is none, fail. algorithm() in the experiment file is this driver with every cap (corrected in this version:
after a discarded advice, B''s budget resumes without the connector's coin work, which the earlier driver counted
against it; no run used algorithm()). Lemma 1 (outputs are collisions): for x in V, A0 = L^-1(x) satisfies the fixed-bit
equations, and so does A0 + L^-1(beta), since E_D forces (L^-1 beta)_j = 0 on F; beta != 0; E compares the true 256-bit
digests. Lemma 2 (used only for the probability): for x in V the difference after round 1 is alpha2. Lemma 3: beta is
not in W, so the 2^32 pairs of a space are distinct.

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

### 4.2 Runs after the constants were fixed

| Run | Pre-registered | Used for |
| --- | --- | --- |
| B' with LABEL_B = "hashsmash sha3-256-r5 v6 B-prime advice run 1" | 2026-10-06T09:01Z | the advice of the v6 run (k = 0 below) |
| v6 full-scale run, LABEL = "hashsmash sha3-256-r5 v6 run" | 09:19Z | s0 (H1): 14 of the first 512 accepted spaces |
| Pre-registration A: B' runs k = 0..8 + 128 connector attempts each | 15:29:17Z (sha256 fcfd7d64...) | H2, H3 |
| Pre-registration B: E check on 2 spaces per advice + 2 v6 spaces | after A (sha256 2f2deebf...) | support for H1 across advice |

The v6 full-scale run (as in v7): 960 of 1024 attempts accepted; the first 512 accepted spaces, enumerated over their
2^32 windows, gave 132,138 round-2 passes (1.008 x expected, variance/mean 1.02, at most 301 per space) and 14
collisions. s-hat = 0.0273; one-sided 99% Clopper-Pearson lower bound 0.0133; s0 = 0.013. r5-den-0..2 re-run all 538
attempt indices up to the 512th acceptance (the whole denominator); r5-replay re-derives the 14 positives. Its decision
rule (submit only if s0 >= 0.002) is disclosed; this is H1's outcome-selection premise. As in v7, a fault of the C++ E
(bf.cpp in the v6 run, bf8.cpp in 4.3) could only lose positives and lower s-hat: every positive is replayed at its
coordinate by the Python E (r5-replay, r5-replay8) and the denominator is re-run (r5-den).

Pre-registration A (r5c.py, bprun.py, cnrun.py hashed before the runs; up to docstrings, r5c.py's algorithm functions
are AST-identical to the experiment file's, except that Setup takes the advice as arguments, e_window has the stage-2
cap and algorithm(), which no run used, has the budget correction of 2.5). Nine B' runs started together; none was
stopped, excluded or repeated. Costs are exact counts. Pre-registration A's only other rule: if an advice failed
facts() or an accepted attempt failed verify_space, this would be reported and the package not built until understood
(neither happened). Neither pre-registration had a rule about submitting.

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
= 0 reproduces the v6 advice bit for bit at the v6 B'-only counts (row 762,306,397, small 174,005,590; 2^27.118 units;
v7's table, 762,402,397 and 179,345,238, also counted the base setup Base and own_bits). Totals: 65 candidates, 9
accepted (q_c-hat = 0.138, one-sided 95% CP lower bound q_c0 = 0.0742); largest candidate c_max = 2^25.848 units;
largest B' run 2^28.218 units, 2^5.8 below the budget; 744 of 1,152 connector attempts accepted, all 744 verified
(Lemmas 1-2 on two solutions); largest attempt 179,180 work units and 4,460 coin words. Every advice is "good" (99% CP
lower bound >= 0.10), so f_up = one-sided 95% CP upper bound of 0/9 = 0.2831. Pre-registered B' failure bound: n =
floor(2^34 / (2 c_max)) = 142 candidates fit the budget, and (1 - q_c0 (1 - f_up))^142 = 0.00043.

### 4.3 Pre-registration B: E check

bf8 enumerated the full 2^32 window of the first 2 accepted spaces of each advice k = 0..8, and of v6 spaces 0 and 1
(20 spaces, 2^36.3 pairs).

| Advice k | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | v6 spaces |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| round-2 passes (2 spaces; 512 expected) | 506 | 542 | 533 | 562 | 576 | 526 | 514 | 502 | 499 | 547 (= 271 + 276, as in v6) |
| collisions | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 |

Pooled over the 18 v8 spaces: 4,760 round-2 passes vs 4,608 expected (ratio 1.033, inside the pre-registered 99%
interval [0.994, 1.072] but 2.2 Poisson standard deviations above 1; advice 4 alone is 2.8 above); at most 307 per
space; the stage-2 cap never bound; mean stage-1 count 398.625 per pair in every space. Three collisions (advice 4
twice, both in its first space, attempt 0; advice 7 once); r5-replay8 re-derives the advice from its label, re-runs the
connector attempt and replays all three. At the v6 rate (0.027 per space) three or more collisions in the 16 spaces of
fresh advice has probability about 0.01, and two in one of 18 spaces about 0.007. So rates may vary between advices
and spaces more than an independent-pair model predicts; s (H1) counts spaces with at least one collision, so a second
collision in a space does not change it. As pre-registered, these spaces do not enter s0.

### 4.4 Certificates

16 certificates (distinct 135-byte messages, equal complete 5-round digests): the 3 collisions of 4.3
(r5-v8-r4-000000-13c3cc2f, r5-v8-r4-000000-9707a665, r5-v8-r7-000002-1e5fa912: run k, attempt, window coordinate) and
13 of the 14 v6 collisions (r5-v6-<attempt>; attempt 462 is left out by the 16-certificate limit and replayed by
r5-replay).

### 4.5 Organizer experiments

r5_connector.py: reference algorithm and experiments; r5_trail.py: P recount and E count. PASS returns the sentinel
(00^135, 01 || 00^134), whose digest XOR is the declared mask value; FAIL returns (00^135, 02 || 00^134). The evidence
is the organizer's execution of the visible code.

| id | trials | PASS means | local public-seed result |
| --- | --- | --- | --- |
| r5-bp-0..4 | 2 per advice, then 32 connector attempts per advice | B' re-derives advice k from its label (candidate setup row count, the accepting attempt's status, DF and row count, advice hash); one other logged attempt of that candidate matches; an organizer-seeded attempt is accepted and verified | 18 of 18 B' checks; 196 of 288 attempts (187 with a random nonce) |
| r5-bpfull | 2 | B' run k = 1 executed whole under its budget: same output, counted cost equal to the logged one; with a 2^20-unit budget B' stops after one update | 2 of 2 |
| r5-den-0..2 | 180, 180, 178 | v6 attempt i accepted with the logged DF (FAIL: rejected as logged) | 512 PASS of 538 |
| r5-replay | 14 | full collision: v6 positive replayed | 14 collisions |
| r5-replay8 | 3 | full collision: v8 E-check positive replayed | 3 collisions |
| r5-trail-0..3 | 1 each | P's counts of the group equal the log | 4 of 4 |
| r5-ecount | 92 | counted stage 1 equals a plain evaluation and COST[exit] (64 seeded states, 25 forced exits, block control 15); one counted T3 pass (9 leaves + Gray step) equals a plain evaluation and costs 1,750 <= 9 x 512 | 92 of 92 |

Local runs of the organizer runner (Python 3.12 and 3.9, each program run twice; identical results): at most 6.0
CPU-s and 1.4 x 10^11 instructions under 3.12 (7.6 CPU-s under 3.9) and 96 MB per experiment; the four r5-trail parts
at most 3.4 CPU-s each. With a random nonce in place of the public seed only the connector counts change (187 of 288).

## 5. Success probability

Theorem (under H1-H3). Pr[the algorithm outputs a collision] >= 0.81. The heuristics (mirrored in claim.json) enter
only the success probability; no cost cap depends on them:
- H1-space-success: for each advice B' can output, per accepted space E outputs a pair with probability >= s0 = 0.013
  (a bound per advice, not an average over advices: (e) needs s >= 0.0040 for the final advice). Evidence 4.2 (v6 run,
  14 of 512; r5-den-0..2, r5-replay, r5-bp-0) and 4.3 (9 advices, round-2 rate 1.033 x the trail value, 3 collisions,
  r5-replay8). Premises: E depends on the advice only through alpha2 (Markov); seeded coins act as fresh; the v6
  decision rule (disclosed) did not bias s-hat beyond the 99% bound. Limits: s0 is measured on one advice; 4.3 shows
  more variation between advices and spaces than an independent-pair model predicts (all of it upward).
- H2-bprime-runs: B' candidates are independent, each accepted with probability >= q_c0 = 0.0742 at a cost <= 2^26.85
  units (2 x the largest of 65), so (b) <= 0.00043. Evidence 4.2, r5-bp-0..4 and r5-bpfull (the budget counter and one
  whole run executed). Limit: the per-candidate cost is bounded by observation, not by a cap; a Markov bound from the
  mean run cost gives 0.0084 instead.
- H3-connector-acceptance: a B' advice has connector acceptance q >= 0.10 except with probability <= f_up = 0.2831 (0
  of 9 bad; 45-120 of 128 accepted; 288 organizer-seeded attempts in r5-bp-0..4).

Failure needs one of:
- (a) P exhausts its budget: impossible, since P is deterministic and its node and leaf counts are half their caps.
- (b) B' exhausts 2^34 units before a good advice (connector acceptance q >= 0.10): <= 0.00043 (H2; this includes the
  restarts).
- (c) More than 15 advice rounds: <= f_up^16 < 2^-29 (H3).
- (d) A good advice gives fewer than 128 accepted attempts in 2^12: Chernoff with mean >= 409.6, < 2^-139.
- (e) E outputs nothing on the 128 spaces of the final advice: (1 - s0)^128 = 0.1873 (H1; the spaces are i.i.d. given
  the advice, because the attempts use independent coins).
- (f) Coin map: each Fisher-Yates index is within (i+1)/2^64 of uniform; with at most 2^39.4 coin words in B' (32
  counted primitives each under 2^34 units) and 2^30.5 in the connector, all on lists of fewer than 2^12 elements, the
  total variation is below 2^-12.

So Pr[success] >= 1 - 0.00043 - 2^-29 - 2^-139 - 0.1873 - 2^-12 > 0.81. The claim 0.40 holds for any s >= 0.0040, 3.3
times below s0. At s-hat = 0.0273 the bound is 0.97.

## 6. Time (collision-frontier-v5: one 5-round permutation = 1 unit, other primitives 1/1355)

| Term | Hard cap, enforced by | Count and price | log2 units |
| --- | --- | --- | --- |
| P | node and leaf counters at 2 x the exact counts (Appendix A) | 2 x 712,940,389,039,104 primitives (counted bound) | 39.9367 |
| B' | WK counter, re-checked on every update | 2^34 units + one update (< 2^13 units) | 34.0000 |
| S | at most 16 advice rounds | 16 x 2^31 primitives | 24.5959 |
| Connector | 2^18 work units per attempt, A_max = 2^16 attempts | 2^16 x (2^18 x 96 + 2^15 x 2^9 + 2^22) primitives | 31.0554 |
| Bases | K = 128 spaces | 128 x 2^24 primitives | 20.5959 |
| E stage 1 | 2^32-pair window, worst-case path | 128 x 2^32 x 594 primitives | 37.8102 |
| E stage 2 | S2CAP = 2^11 per space | 128 x 2^11 x (2 units + 2^7 primitives) | 19.0666 |
| Output | one pair | 2^22 primitives | 11.60 |
| Total T | | | 40.2557 -> 40.26 |

Every term is a cap that holds on every run; no expected value is used. Preprocessing (P + B' + S) = 2^39.9601,
claimed 39.97. Sensitivity (not the claim): the 64-register model lets E load only the 25 basis lanes; at 671 primitives
per pair (7deb1595's count) T = 2^40.29, with 150 further loads and stores per pair (744) 2^40.33. Context only: the
measured central cost (P at its count, B' at the mean of the nine runs, about 160 attempts, E at 398.625 + 15/16 per
pair) is about 2^39.3.

## 7. Memory

Measured peaks: P 4.1 MB (T3), B' at most 113.5 MB (run 2; 42-83 MB in the others), connector and reference code under
2^23 bytes; E keeps 25 lanes and 32 basis vectors. Before E starts, algorithm() keeps the echelon system of each of the
K accepted spaces (at most 1,600 forms of 1,601 bits each, about 41 MB in all; the bases alone would be 128 x 33 x 200
bytes). Declared 2^30 bytes, 9 x the largest measured peak.

## 8. Not claimed; credits

Not claimed: any improvement on [GLL+20] beyond the byte-aligned (p = 8) adaptation, B', the counted early-abort E and
the accounting. The certificates show that the construction works; they are not the claimed cost. Credits: [GLL+20]
for the connector and linearisation framework and the 5-round trail core that P re-derives; Dinur, Dunkelman, Shamir
(FSE 2012) for the target-difference algorithm; Qiao, Song, Liu, Guo (EUROCRYPT 2017) for linearisation; Daemen, Van
Assche (FSE 2012) and KeccakTools for in-kernel trail cores. Th0rgal 7deb1595 (with Subflatus3 and rubenmarcus): the
zero-advice framing with every phase inside a capped algorithm and development disclosed, and the early-abort order of
the round-2 rows (row 66, then row 81); Th0rgal is a co-author of this package. None of 7deb1595's code, data or
certificates is used. hybridnoise's note (ef4a0c66) showed that an own-beta1 byte-aligned connector can work;
jagnani73 (654cb3d2) taught us fresh coins, hard caps and organizer experiments. baseline_improved is the required
nominal reference ID, not a claim of dominance.

## Appendix A. Trail search P with its budget counters (C++17; shared helpers kc.h)

Run as `trail1c 10 > cores; trail2c < cores > t2; trail3c 12 < t2 > t3` (T3 reads the cores with P45 > 0).

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

`trail3c.cpp`:

```cpp
// Stage T3: backward extension. For each core with P45 > 0 (lines of T2 output), enumerate every beta2
// compatible with alpha3 (row-wise, all compatible input differences) in reflected mixed-radix Gray order,
// keep alpha2 = L^{-1}(beta2) incrementally, and compute w1 = sum over rows of minrev(alpha2 row).
// Exact minimum of (w1, w2, beta2 lanes lexicographic) per core. Pruning: w1 >= 2*AS(alpha2).
#include "kc.h"
#include <thread>
#include <mutex>
#include <atomic>
struct Core{int idx;St a3;double p45;};
static std::vector<Core> cores;
static std::atomic<int> nextc(0);
static std::mutex mu;
static std::atomic<unsigned long long> totleaves(0),totfull(0);
static std::atomic<int> gbest(1<<30);
static std::atomic<unsigned long long> gleaves(0); static const unsigned long long CAP3=2758550798700ULL; // 2 x sum C2 (budget of P)
static inline int w1of(const St&s){
  int w=0;
  for(int y=0;y<5;y++){u64 a0=s.a[5*y],a1=s.a[5*y+1],a2=s.a[5*y+2],a3=s.a[5*y+3],a4=s.a[5*y+4];
    u64 nz=a0|a1|a2|a3|a4;
    // ge3: at least 3 of 5 bits set
    u64 s1=a0^a1, c1=a0&a1; u64 s2=s1^a2, c2=(s1&a2)|c1; // count of a0..a2 = s2 + 2*c2? (c1,c2 not disjoint-safe) recompute properly below
    (void)s2;(void)c2;
    // exact bit-sliced counter
    u64 b0=0,b1=0,b2=0; u64 v[5]={a0,a1,a2,a3,a4};
    for(int k=0;k<5;k++){u64 c=b0&v[k];b0^=v[k];u64 c2b=b1&c;b1^=c;b2|=c2b;}
    u64 ge3=b2|(b1&b0); // count>=3 : 4,5 -> b2 ; 3 -> b1&b0
    u64 cons=0;for(int i=0;i<5;i++)cons|=v[i]&v[(i+1)%5]&v[(i+2)%5]&~v[(i+3)%5]&~v[(i+4)%5];
    w+=2*__builtin_popcountll(nz)+__builtin_popcountll(ge3&~cons);}
  return w;
}
static inline int asof(const St&s){int n=0;for(int y=0;y<5;y++)n+=__builtin_popcountll(s.a[5*y]|s.a[5*y+1]|s.a[5*y+2]|s.a[5*y+3]|s.a[5*y+4]);return n;}
static void work(){
  for(;;){int ci=nextc++;if(ci>=(int)cores.size())return;Core&c=cores[ci];
    // rows of alpha3
    std::vector<int> ry,rz,ro;for(int y=0;y<5;y++)for(int z=0;z<64;z++){int o=rowval(c.a3,y,z);if(o){ry.push_back(y);rz.push_back(z);ro.push_back(o);}}
    int n=ry.size();std::vector<std::vector<int>> ins(n);std::vector<std::vector<St>> LI(n,std::vector<St>(32));
    for(int j=0;j<n;j++){for(int d=0;d<32;d++)if(DDT[d][ro[j]])ins[j].push_back(d);
      for(int v=0;v<32;v++){St s;zero(s);setrow(s,ry[j],rz[j],v);LI[j][v]=Linv(s);}}
    // Knuth Algorithm H over rows 1..n-1; row 0 enumerated innermost.
    int WT[32][32];for(int d=0;d<32;d++)for(int oo=0;oo<32;oo++)WT[d][oo]=DDT[d][oo]?5-lg2(DDT[d][oo]):99;
    int n1=n-1;std::vector<int> a(n1+1,0),f(n1+1),o(n1+1,1),m(n1+1);for(int j=0;j<=n1;j++){f[j]=j;m[j]=j<n1?(int)ins[j+1].size():2;}
    St al;zero(al);for(int j=1;j<n;j++)xr(al,LI[j][ins[j][0]]);
    int w2o=0;for(int j=1;j<n;j++)w2o+=WT[ins[j][0]][ro[j]];
    int m0=ins[0].size();std::vector<St> L0(m0);std::vector<int> w0(m0);for(int k=0;k<m0;k++){L0[k]=LI[0][ins[0][k]];w0[k]=WT[ins[0][k]][ro[0]];}
    int bw1=1<<30,bw2=1<<30;unsigned long long leaves=0,full=0,nbest=0;int bas=0;
    std::vector<int> bestsel;
    for(;;){
      leaves+=m0;if((gleaves+=m0)>CAP3){fprintf(stderr,"P budget exhausted in T3\n");exit(2);}
      int T=std::min(bw1,gbest.load());
      for(int k=0;k<m0;k++){const St&l0=L0[k];
        int as=0,y=0;
        for(;y<5;y++){int b=5*y;as+=__builtin_popcountll((al.a[b]^l0.a[b])|(al.a[b+1]^l0.a[b+1])|(al.a[b+2]^l0.a[b+2])|(al.a[b+3]^l0.a[b+3])|(al.a[b+4]^l0.a[b+4]));if(2*as>T)break;}
        if(y<5)continue;
        St t=al;xr(t,l0);full++;int w1=w1of(t);int w2=w2o+w0[k];
        {int g=gbest.load();while(w1<g&&!gbest.compare_exchange_weak(g,w1));}
        std::vector<int> sel;sel.push_back(k);for(int j=0;j<n1;j++)sel.push_back(a[j]);
        if(w1<bw1||(w1==bw1&&w2<bw2)){bw1=w1;bw2=w2;bestsel=sel;nbest=1;bas=as;T=std::min(bw1,gbest.load());}
        else if(w1==bw1&&w2==bw2){nbest++;if(sel<bestsel)bestsel=sel;}
      }
      int j=f[0];f[0]=0;if(j==n1)break;
      int old=ins[j+1][a[j]];a[j]+=o[j];int nw=ins[j+1][a[j]];
      xr(al,LI[j+1][old^nw]);w2o+=WT[nw][ro[j+1]]-WT[old][ro[j+1]];
      if(a[j]==0||a[j]==m[j]-1){o[j]=-o[j];f[j]=f[j+1];f[j+1]=j+1;}
    }
    if(bestsel.empty()){totleaves+=leaves;std::lock_guard<std::mutex> g(mu);printf("%d w1>%d pruned leaves=%llu logP45=%.4f\n",c.idx,gbest.load(),leaves,log2(c.p45));fflush(stdout);continue;}
    St b2;zero(b2);for(int j=0;j<n;j++)setrow(b2,ry[j],rz[j],ins[j][bestsel[j]]);
    totleaves+=leaves;totfull+=full;
    std::lock_guard<std::mutex> g(mu);
    printf("%d w1=%d w2=%d AS2=%d nbest=%llu leaves=%llu full=%llu logP45=%.4f b2=",c.idx,bw1,bw2,bas,nbest,leaves,full,log2(c.p45));
    for(int i=0;i<25;i++)printf("%016llx%s",(unsigned long long)b2.a[i],i<24?",":"\n");fflush(stdout);
  }
}
int main(int argc,char**argv){
  int nth=argc>1?atoi(argv[1]):12;
  initDDT();initLinv();
  char line[8192];
  while(fgets(line,sizeof line,stdin)){
    int idx;double lp;char*q=strstr(line,"logP45=");sscanf(line,"%d",&idx);sscanf(q+7,"%lf",&lp);if(lp<-900||lp>900)continue;
    char*p=strchr(line,'|')+1;int n,off;sscanf(p,"%d%n",&n,&off);p+=off;St a3;zero(a3);
    for(int k=0;k<n;k++){int b;sscanf(p,"%d%n",&b,&off);p+=off;flip(a3,b);}
    cores.push_back({idx,a3,pow(2.0,lp)});
  }
  fprintf(stderr,"T3 cores=%zu\n",cores.size());
  std::vector<std::thread> th;for(int t=0;t<nth;t++)th.emplace_back(work);for(auto&t:th)t.join();
  fprintf(stderr,"T3 total leaves=%llu full=%llu\n",(unsigned long long)totleaves,(unsigned long long)totfull);
}
```

## Appendix B. E as run in our evidence (bf8.cpp)

bf8.cpp (sha256 480ad1a16d6f790561ac2ee5808d5ca226b6283510c9ec7208673ba6d33593fc, fixed in pre-registration B; uses kc.h
of Appendix A) is a multithreaded C++ form of E (2.4) used only for the E check of 4.3; its source is left out for
length. Ties to the counted program: equal exit histograms on a 2^14 window; on v6 spaces 0 and 1 its stage-2 counts
equal the v6 E's (271, 276); its three collisions are replayed from their labels by r5-replay8.
