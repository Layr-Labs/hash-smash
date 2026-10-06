# 5-round SHA3-256: byte-aligned connector, self-generated charged advice, pre-registered run

This is an exploratory claim. The claimed time is a hard cap of the specified algorithm, valid
on every run. No published pair, difference or message value is used: the advice is the output
of our own deterministic program B', which an organizer experiment re-derives from its label at
the logged operation counts. The algorithm was executed at full scale with that advice in a
pre-registered run (5.3): 14 collisions of 135-byte messages in 14 of 512 spaces. All 14 ship as
certificates, and an organizer experiment re-derives all 14 with E's own tests. [GLL+20] = J.
Guo, G. Liao, G. Liu, M. Liu, K. Qiao, L. Song, "Practical Collision Attacks against
Round-Reduced SHA-3", J. Cryptology 33 (2020) 228-270, ePrint 2019/147.

## 0. Claim, summary, changes, checklist

| Field | Value | Basis |
| --- | --- | --- |
| time_log2 | 45.33 | hard cap 2^45.328, rounded up (Section 7) |
| success_probability | 0.40 | > 0.9987 under H2 and H3 (Section 6) |
| memory_log2_bytes | 36 | Section 8; the algorithm itself uses < 2^23 bytes |
| preprocessing_log2 | 45.08 | 32 x P (2^43.937) + all other advice work as machine capacity (2^44.206) + S |
| nonuniform_advice_log2_bytes | 9.3 | trail core (214 bytes) + beta1', beta0' (400 bytes) = 614 bytes |

Summary. (1) The advice is the trail core output by our search P and the pair (beta1', beta0')
output by our program B' (Section 2). (2) Both are charged in full: P at 32 x its exact
leaf-count cost (2^43.94, 8 x the measured CPU time of all its runs); all other advice work, B'
included, as the whole capacity of the one 15-core machine it ran on, every core for the whole
6,600 s window that contains it, at 2^38 primitives per core-second (H1): 2^44.206. No process
log enters the charge. (3) The connector of v5 is unchanged except that it reads beta1', beta0'
instead of the published differences: byte-aligned 135-byte messages, a target-difference phase
steered to beta0', non-full linearisation, at most 2^18 work units per attempt. (4) E searches
K = 512 accepted spaces, 2^32 pairs each, with a full 256-bit digest test; attempts use
independent coins, so the spaces are i.i.d. (5) Heuristics: H1 (machine capacity over the advice
window), H2 (per-space output probability s0 = 0.013), H3 (per-attempt acceptance q0 = 0.05).
The run-selection premise is stated inside H2 and H3 and bounded by compute (5.3). (6) Organizer
experiments re-run every logged attempt of the full-scale run up to its 512th accepted one and
re-derive every collision.

Changes since 189a63b2 (rated not_evaluable). Each finding of its dossier is answered below.

| 189a63b2 finding | this package |
| --- | --- |
| H1 unsupported: the advice was the published pair, charged from historical single-core times of an unpublished CPU; no operation trace; target-compression calls inside opaque CPU time; factor-2 coverage of unreported runs | The published pair is gone. B' (2.2) counts its work exactly by class (2^27.12 units), and r5-advice re-derives the advice from the label alone at the logged counts. The charge does not sum process logs: every core of our one machine is charged for the whole window that contains all advice work other than P (2^44.206, 2^17 x B''s exact count). Calls worth more than 1/1355 per primitive (Keccak-f, SHA-256, 5-round evaluations) are separated by measured maximal rates (2.3). P's factor 32 also covers its prototypes |
| H2 unsupported: the 21/768 count was participant-reported; replays of hard-coded successes do not check the denominator | New pre-registered run with the new advice (5.3). r5-den-0..5 re-run all 538 logged attempt indices up to the 512th accepted one (the whole denominator; nothing sampled, nothing seed-dependent), r5-replay re-derives every positive (numerator). Run selection is bounded by compute (5.3) |
| H3: 8/256 organizer trials, margin 1.37 | With the new advice about 94% of attempts are accepted. r5-connector and r5-conn-b run 128 organizer-seeded attempts; q0 = 0.05, and Pr[123 of 128 or more if q <= 0.05] < 2^-504 |
| Undeclared run-selection premise (rated unsupported); heuristics_disclosed unresolved | The premise is written into H2 and H3, with every full-scale and advice run listed (5.4); choosing the run among alternatives would have needed work on at least 2^49.7 labels, 2^50.7 units even at one SHA-256 call each (5.3). Connector parameters tuned in v5 were non-binding (2.3) |
| r5-connector's host check is vacuous | Inherent to digest-only host events; every scope says so. The host also counts FAIL rows, so each experiment yields two organizer-counted numbers |

Checklist: (1) messages of 135 bytes, padded block M || 0x86 || 0^512 (1); (2) trail facts w1 =
127, w2 = 24, C2 = 3^20, P45 = 55/2^19 (3.1); (3) advice facts (3.2), recomputed before every
organizer experiment except r5-advice*; (4) per attempt at most 2^18 work units and 22,150 coin
words (4.1, 7); (5) success > 0.9987 (6); (6) time 2^43.937 + 2^44.206 + 2^42.674 + 2^31.06 +
small = 2^45.328 (7).

## 1. Target, messages, notation

sha3-256-r5-prefix-v1 is FIPS 202 SHA3-256 restricted to rounds 0-4 of Keccak-f[1600]: rate
1088, capacity 512, zero initial state, suffix 01 with pad10*1 (byte 0x06), digest = first 32
bytes squeezed (lanes 0..3). Round i maps A to chi(L(A)) xor RC[i], with L = pi o rho o theta.
State bit (x,y,z) has index 64(x+5y)+z; block byte j is lane floor(j/8), bits 8(j mod 8)..+7.
chi acts on the 320 rows (y,z) by chi5(v)_i = v_i xor (NOT v_{i+1}) v_{i+2}, indices mod 5.

All messages are exactly 135 bytes. The initial state is A0 = M || 0x86 || 0^512; one
permutation is applied and the digest is lanes 0..3 of its output. The fixed set F = bits
1080..1599 (520 bits) holds constants: bits 1081, 1082 and 1087 are 1, the rest 0.

For a pair of states, alpha_i is the difference entering round i (alpha_0 is the block
difference), beta_i = L(alpha_i) the difference entering chi, and chi maps beta_i to
alpha_{i+1}. DDT[d][o] = #{v : chi5(v) xor chi5(v xor d) = o}; a row transition d -> o has
weight 5 - log2 DDT[d][o]. x = L(A0) is the first message's round-0 chi input; the second has x
xor beta0. A linear form over x is a 1601-bit vector whose bit 1600 is the constant. Row facts,
checked exhaustively over all (d, o): R1. V(d,o) = {v : chi5(v) xor chi5(v xor d) = o} is an
affine subspace of dimension log2 DDT[d][o] when nonempty, so a transition is exactly w affine
equations on one message's row value. R2. The least weight into a nonzero o is 2, and 3 when o
has at least 3 bits and is not three cyclically consecutive bits.

## 2. Advice and its charged construction

The advice is (alpha3, beta2) from P and (beta1', beta0') from B': 214 + 400 = 614 bytes. The
cost model charges all construction of advice, including runs left out of the submitted program.

### 2.1 Trail core: search P (charged at 32 x P)

P outputs the 2-round in-kernel core alpha3 and the beta2 that minimise w1; its C++ source is
inert text in the experiment file (INERT_SOURCES). T1 (cores): a candidate alpha3 is a set of at
most 10 bits whose alpha-columns and beta-columns (columns of pi o rho of each bit) all hold an
even number of bits; depth-first search from each of the 25 bits with z = 0; at a node, let c be
the smallest odd alpha-column, else the smallest odd beta-column; if none, record the core in
canonical form (smallest sorted bit list over the 64 z-translations), else, below 10 bits,
branch on each bit of c not yet in the set. T2 (forward): beta3 = pi o rho(alpha3); enumerate
every alpha4 compatible with beta3, accumulate P45 (3.1) and keep cores with P45 > 0. T3
(backward): for each kept core enumerate every beta2 compatible with alpha3 in reflected
mixed-radix Gray order, maintaining alpha2 = L^-1(beta2) incrementally, and compute w1 (R2) only
when 2 AS(alpha2) does not exceed the best w1 so far. Output: least w1; ties to the smaller w2,
then the smaller choice vector.

| Stage | Executed run |
| --- | --- |
| T1 | 8,674,833 nodes; 1741 cores (8 of 6 bits, 139 of 8, 1594 of 10) |
| T2 | sum C1 = 1,639,088,128 leaves; 467 cores have P45 > 0 |
| T3 | sum C2 = 1,379,275,399,350 leaves |
| Output | w1 = 127, reached by exactly one core and one beta2 (w2 = 24); next best w1 = 263. This is core No. 3 of [GLL+20] (weights 127-24-19) |

P is charged at 32 x (C2 x 2^9 + C1 x 2^12 + nodes x 2^12 + 2^31) primitives = 2^43.937 units
(prices in 7). The factor 32 makes the charge independent of how closely P resembles any other
tooling; the accepted precedent 654cb3d2 charged a re-run search with the same margin. It also
covers every run of P: T1 once, T2 twice and T3 once in full, 10,260 CPU-s in all by
/usr/bin/time (2^40.92 units at the rate of 2.3), after the three programs were written and
tested within ten minutes; 32 x P is 8 x the measured time of all of them. P ran before the
window of 2.3.

### 2.2 Connector advice: program B'

B' is a deterministic program (the functions from rand_min_beta1 to b_attempt of the experiment
file, with the constants KW, MW, LB, PREF). Its only inputs are P's trail and the fixed bits F;
it reads no published value. With LABEL_B = "hashsmash sha3-256-r5 v6 B-prime advice run 1", for
candidate c = 0, 1, ...:
- beta1_c: in each of the 59 rows of alpha2 a uniform input difference of least weight (50 rows
  have exactly one, 9 have 4 or 5), coins Coins(SHA-256(LABEL_B || "beta1" || c)). Then the
  round-1 conditions, the linearisation table (4.2), and the link and candidate tables below.
- attempts j < R = 16, coins Coins(SHA-256(LABEL_B || "att" || c || j)):
  - D2u: rows of alpha1 = L^-1(beta1_c) in DSATUR order. Each gets an affine set of compatible
    differences on which the fixed-bit "link" conditions are uniform, so they become linear in
    the difference. Almost every value-phase dependency comes from two rows that share a
    fixed-bit column, and this removes it before the value phase.
  - M2: rows in DSATUR order. Each gets (d in its set, W) with W from the linearisation table.
    Forward checking runs on one value system: x, the fixed bits, the row equations, and the 127
    round-1 conditions through auxiliary variables (one per basis mask of a row).
  - Accept iff consistent and DF >= DMIN = 40, and 64 sampled points of the space pass: both
    messages padded, block difference L^-1(beta0), exact 2-round difference alpha2.
- Stop at the first accepted attempt; the advice is (beta1_c, beta0).

Every operation is counted by class: row (one operation on an integer of at most 2585 bits, 256
primitives), small (one word operation, 8 primitives), keccak (one Keccak-f[1600] call of the
coin stream, 5 units), sha256 (one compression, 2 units) and r2 (one 2-round evaluation in the
verification, 1 unit).

The run. It was pre-registered (program hash, label, R = 16, DMIN = 40, stop rule) and run once,
single process, under /usr/bin/time -l on an Apple M5 Pro core, Python 3.12.

| Quantity | Value |
| --- | --- |
| candidates, attempts | 6 (c = 0..5), 90: 41 failed in D2u, 40 in M2, 8 with DF < 40, 1 accepted |
| output | c = 5, j = 9: DF = 41, 64 of 64 points verified |
| counters | row 762,402,397; small 179,345,238; keccak 127,472; sha256 186; r2 128 |
| exact cost | 196,609,775,536 primitives + 637,860 units = 2^27.12 units |
| measured | 35.57 CPU-s; 600,255,935,980 instructions retired; 131,886,521,816 cycles; peak 42 MB |

r5-advice re-runs candidate 5 and its attempt 9 from LABEL_B alone, must reproduce BETA1A,
BETA0A, DF 41 and the logged row counts of the candidate setup (9,455,652) and of the attempt
(23,444,127), and audits 4 other logged attempts; r5-advice-log audits one logged attempt of
each of candidates 4, 3, 2 (with their setup counts). Our local organizer-format run of both
matched all 8 (5.6). For comparison only: beta1' agrees with the published beta1 of [GLL+20] in
the 50 rows with a single least-weight choice and differs in the other 9; beta0' shares 17 of
its 310 active rows with the published beta0.

### 2.3 Charge of all other advice work: machine capacity over a window (H1)

Everything that produced or shaped (beta1', beta0') ran on one machine, an Apple M5 Pro with 15
cores (5 performance, 10 efficiency) and 48 GiB, inside the window [07:30Z, 09:20Z] of
2026-10-06 (6,600 s): the study of the connector without the published pair, the 75 development
processes of B' (among them every run that used a published difference as a test case), B'
itself (09:01:21Z-09:02:07Z; the advice was final then), the steering check of the v5 attempt
with the new advice (1,000 attempts, 941 accepted, DF 40-42), and the abandoned h23 plan (5.4).
The window opens before the organizer's review run of 189a63b2 (20261006T073301Z), whose outcome
started this work (its first file is dated 07:47:39Z), and closes after the pre-registration of
the full-scale run (09:19:04Z). We charge every core for the whole window, busy or not, and add
1,000 core-seconds for the organizer-format re-runs of B' made after the window (they only
reproduce the advice; under 500 CPU-s in all):

    (15 x 6,600 + 1,000) core-seconds x 2^38 / 1355 = 100,000 x 2^27.60 = 2^44.206 units.

Rate. One core-second of this machine is at most 2^38 primitives of the 256-bit word RAM. No
core decodes more than 10 instructions per cycle or reaches 5 GHz, so at most 2^35.54
instructions per second, and an ordinary ARM64 scalar or NEON instruction touches at most 512
bits (2 primitives; we allow 4): 2^37.54. B' measured 2^33.97 instructions per CPU-second (4.55
per cycle at 3.72 GHz). The ARMv8 SHA-3 instructions (EOR3, RAX1, XAR, BCAX) are two operations
on 128 bits each; the SHA-2 instructions used by hashlib's SHA-256 do more and are covered by
the separation below. None of this work used the GPU or SME.

Separation. A 5-round permutation costs 1 unit, and we price a Keccak-f[1600] call at 5 units
and a SHA-256 compression at 2 units (about 2,100 32-bit operations), so such calls cannot be
divided by 1355. Their maximal rates on one core of this machine, measured with bulk inputs so
that call overhead is minimal (Python 3.12 hashlib), and with our fastest native code:

| Work inside one core-second | Max rate per CPU-s | Units per CPU-s |
| --- | --- | --- |
| Keccak-f[1600] calls (SHAKE-256, SHA3-256 in hashlib) | 2^22.3 | 2^24.6 |
| SHA-256 compressions (hashlib, SHA-2 instructions) | 2^25.2 | 2^26.2 |
| 5-round evaluations, bit-sliced Python | 2^19.4 | 2^19.4 |
| 5-round evaluations, C++ E, one thread (run only after the window) | 2^25.2 pairs x 3.19 units | 2^26.9 |
| any other instructions | 2^35.54 x 4 primitives | 2^27.14 |

Every row is below the 2^27.60 units charged per core-second, so for any mix of calls and other
work the charge covers max(call price, primitive price). This includes the Keccak-f calls of all
coin streams, the 4,660 logged 2-round checks and the bit-sliced benchmarks.

Cross-checks (not the charge). (a) r5-advice re-derives B''s exact count, 2^27.12 units; the
charge is 2^17.09 times that, and B' is the same kind of single-threaded Python process as the
development runs. (b) Our per-process ledger of the window is far below the capacity charged:

| Category | Processes; time source | CPU-s |
| --- | --- | --- |
| Study: connector without steering, annealers, backtracking, benchmarks | per-trial logs 6,802 s; allowances for unlogged outputs 3,630 s | 10,432 |
| Development of B', with the steering check | 75: 15 by /usr/bin/time, 29 per-attempt logs + 5 s, 4 crashed at start, 23 terminal-only bounds | 1,559 |
| h23 plan (published advice; abandoned) | organizer-format emulations 177 s; development allowance | 500 |
| B' | 1, by /usr/bin/time -l | 35.6 |
| Total | | 12,527 |

The 100,000 core-seconds charged are 8.0 x this total. Charging 4 x the ledger instead would
give time_log2 44.96; the window charge is larger and depends on no entry of it.

Design parameters. The connector's DMIN = 33 and X_max = 2^18 come from v5 runs with the
published pair, before the window and not charged. Both were non-binding in the pre-registered
run: every accepted attempt had DF 40-42 and all 64 rejections failed in M4, so any DMIN <= 40
gives the same run, and the largest attempt used 166,277 of the 262,144 work units allowed. The
value 33 is also the least DMIN for which E's window and beta exist (4.4). So neither carries
information from the published pair. B''s own parameters (R = 16, DMIN = 40, KW, MW, LB, PREF)
were set by runs inside the window and are charged with it.

## 3. Exact facts (recomputed by every organizer experiment except r5-advice*)

### 3.1 The trail core (output of P)

alpha3 = bits {0, 130, 450, 529, 701, 789, 1021, 1169, 1280, 1429}. Nonzero lanes in hex:

    alpha3: 0:1 2:4 7:4 8:20000 10:2000000000000000 12:200000 15:2000000000000000 18:20000
            20:1 22:200000
    beta2:  0:1 2:4 5:4 6:4 7:4 8:20000 10:2000000000000000 12:200000 15:2000000000000000
            18:20000 20:200001 22:200000 24:1

| Quantity | Value |
| --- | --- |
| alpha3, beta3 = L(alpha3) | 10 bits each, both in the CP kernel |
| beta2 -> alpha3 | the same 10 rows, every row compatible, w2 = 24 |
| alpha2 = L^-1(beta2) | 114 bits, 59 active rows, w1 = 127 (sum of least weights, R2) |
| C2 = # beta2 compatible with alpha3 | 3^20 = 3,486,784,401 |
| P45 (below) | 55/2^19 = 2^-13.2186, from 192 nonzero terms of 2^19 |

The digest is bits x = 0..3 of the 64 rows of plane y = 0. For such a row with input difference
d, PZ[d] = (DDT[d][0] + DDT[d][0x10])/32. The Markov value P45 is the sum over alpha4 in prod_r
{o : DDT[d_r][o] > 0} (rows of beta3) of prod_r DDT[d_r][o_r]/32 x prod over nonzero plane-0
rows q of L(alpha4) of PZ[q]. With w2, p_M = 2^-37.2186 per pair. No claimed number uses it.

### 3.2 The advice (output of B')

| Quantity | Value |
| --- | --- |
| beta1' (BETA1A) | 68 bits, on the 59 rows of alpha2, every row of least weight: beta1' -> alpha2 has weight 127 |
| alpha1' = L^-1(beta1') | 310 active rows |
| beta0' (BETA0A) | compatible with alpha1' on every row, zero on its inactive rows; transitions 44 of DDT 8, 189 of DDT 4, 77 of DDT 2 (weight 963) |
| alpha0' = L^-1(beta0') | nonzero and zero on all 520 fixed bits, so both messages are padded |
| round-1 conditions | 127 (rows of alpha2), on 315 rows of chi(x); linearisation table 3,145 entries |

## 4. Algorithm

### 4.1 Parameters and coins

At most A_max = 2^16 connector attempts; at most K = 512 enumerated spaces; at most X_max = 2^18
work units per attempt (4.3); acceptance DF >= 33; 2^32 pairs per space.

Coins are independent uniform 256-bit words, drawn fresh. Every random choice is a uniform
permutation by Fisher-Yates: for i = n-1 down to 1, j = (low 64 bits of one fresh word) mod
(i+1), swap positions i and j. Lists have at most 310 elements, so each index is within 2^-55.6
of uniform. An attempt draws at most 22,150 words (from the list sizes: 20,449 in D2, 930 in M2,
771 in M3), so a whole run is within 2^-25 of exact uniform permutations in total variation;
Section 6 subtracts this. Target and advice are fixed. The algorithm uses no seed expansion; our
runs and the experiments expand seeds as Section 5 states.

### 4.2 Setup S

S computes L and L^-1 as 1600 row forms each; alpha2 = L^-1(beta2) and alpha1' = L^-1(beta1');
the 127 round-1 conditions: for each of the 59 rows of alpha2, the equations of V(beta1'_r,
alpha2_r) (R1) on z = L(chi(x) xor RC0), each a sum over round-0 rows r of a 5-bit mask applied
to row r of chi(x) (M_r = the masks of row r); the equations of all 2,451 affine subsets of
GF(2)^5 and E's 10 row tests; and the linearisation table: for every row with nonempty M_r and
every set S_r that M3 can meet (V(d, alpha1'_r) for every compatible d, or all 32 values for an
inactive row), either S_r itself if every mask is affine on S_r, or the list of all
largest-dimension affine W in S_r on which every mask is affine.

### 4.3 One connector attempt (`attempt()`, unchanged from v5)

Two echelon systems over GF(2) with undo: E_D on delta (the unknown beta0) and E_M on x. One
counter shared by both counts work units: one call of the reduction routine, or one row addition
inside it. Above X_max the attempt fails.
- D1. E_D gets (L^-1 delta)_j = 0 for j in F, and delta_r = 0 for every row r where alpha1' is
  0.
- D2. Draw a uniform order Q of the 310 active rows. For each r in Q, with o = alpha1'_r and
  rv = beta0'_r, try k = 2, 1, 0: permute uniformly the k-dimensional affine subsets of {d :
  DDT[d][o] > 0} and keep those that contain rv; take the first U whose equations (delta_r in U)
  are consistent with E_D and add them. If no k works, fail.
- M1. E_M gets (L^-1 x)_j = F_j for j in F.
- M2. For each r in Q, order U_r by a uniform permutation, then stably by DDT[d][o] descending,
  then stably with d = rv first; take the first d with delta_r = d consistent with E_D and x_r
  in V(d,o) consistent with E_M; add both, set beta0_r = d. If none, fail.
- M3. Linearise, rows in index order: S_r = V(beta0_r, alpha1'_r) (all 32 values if inactive);
  if its table entry is S_r, W_r = S_r; else permute the listed W uniformly and take the first
  that E_M implies, failing that the first consistent with E_M (adding it); if none, fail. On
  W_r each mask of M_r is an explicit affine form in x_r.
- M4. Substitute these forms into the 127 round-1 conditions and add them to E_M; fail if
  inconsistent.
- M5. DF = 1600 - rank(E_M). Accept iff DF >= 33, output (E_M, beta0).

### 4.4 Space and enumeration E

V = solutions of E_M, beta = beta0. Basis: the offset v0 is the solution with all free variables
0; b_i = (solution with free variable i set) xor v0, free variables in increasing order; add
beta, then b_1, b_2, ..., keeping each vector independent of those before; W = span of the first
32 kept b_i (it exists since DF >= 33). Enumerate x in v0 + W in Gray-code order. For each x,
compute u = L(chi(L(chi(x) xor RC0)) xor RC1) and test the 10 rows of beta2: u_r in V(beta2_r,
alpha3_r). If all pass, compute both complete 5-round digests of A0 = L^-1(x) and A0' = L^-1(x
xor beta); if all 256 bits are equal, output (bytes 0..134 of A0, of A0') and halt.

### 4.5 Main loop and correctness

Run S. For a = 1..A_max: run attempt a; if accepted, run E on its space and halt with E's output
if any; if E has run K times, halt with failure. After A_max attempts, halt with failure. Lemma
1 (outputs are collisions). For x in V, A0 = L^-1(x) satisfies the fixed-bit equations, and so
does A0 xor L^-1(beta) since E_D forces (L^-1 beta)_j = 0 on F: both are padded 135-byte
messages; beta != 0 (its rows are compatible with nonzero alpha1' rows); E compares the true
256-bit digests. Lemma 2 (two rounds, used only for the probability). For x in V the difference
after round 0 is alpha1' (R1 on active rows, zero elsewhere); each mask of M_r equals its affine
form on V, so the 127 conditions hold and the difference after round 1 is alpha2. Lemma 3. beta
is not in W, so the 2^32 pairs {x, x xor beta} of one space are distinct.

## 5. Executed runs (evidence; none of them is the claimed cost)

### 5.1 Coins in our runs

Attempt i of a labelled run uses seed_i = SHA-256(L || i as 8 little-endian bytes) and the words
SHAKE-256(seed_i || k), k = 0, 1, ..., through the coin map of 4.1 (class Coins).

### 5.2 Pre-registration

Before any attempt with L = "hashsmash sha3-256-r5 v6 run", we fixed (SHA-256 of the plan
bfab1ee9c59f91de...): Phase A = attempts 0..1023, all logged; Phase B = the first 512 accepted
attempts, each enumerated over exactly its specified 2^32-pair window by the C++ E (bf.cpp with
kc.h, Appendix A; the binary of v5); H2 statistic I_k = [E outputs a pair in space k], s0 =
one-sided 99% Clopper-Pearson lower bound; decision K = 512 if s0 >= 0.002; no stopping,
exclusion or re-run. K = 512 and A_max = 2^16 were fixed in the plan; the run decided only
whether this package is submitted, and it produced no advice.

### 5.3 The full-scale run

Phase A: 960 of 1024 attempts accepted, 64 failed in M4; DF 40 (227), 41 (558), 42 (175). The
largest attempt used 166,277 work units (cap 262,144) and at most 4,103 coin words. The 512th
accepted attempt is index 537.

| Quantity (Phase B) | Value |
| --- | --- |
| pairs | 512 x 2^32 = 2^41 |
| round-2 passes | 132,138 (1.008 x the 2^-24 expectation); per-space variance/mean 1.02 |
| spaces where E outputs a pair | 14 of 512; 14 collisions in total |
| s-hat; two-sided 95% interval | 0.0273; [0.0150, 0.0455] |
| one-sided 99% Clopper-Pearson lower bound | 0.0133, so s0 = 0.013 |
| the same at confidence 1 - 0.01/2^20 | 0.0036 |

The Markov-Poisson value per space is 1 - exp(-2^32 p_M) = 0.0265 (context only).

What the organizer re-executes. r5-den-0 .. r5-den-5 re-run all 538 attempts up to the 512th
accepted one and compare each with the shipped log (512 accepted, 26 rejected), and r5-replay
re-derives all 14 positives with the Python E at their recorded 32-bit coordinates, hence inside
their windows. A fault of the C++ E could only have lost positives, so 14/512 is a lower bound
for the specified E on this fixed, pre-registered population whatever the C++ E did.

Run selection. If s were at most 0.0010 (all that the claim needs), a label whose first 512
accepted spaces contain 14 or more positive spaces would occur with probability at most
2^-50.79. Whether a label qualifies depends only on its own coins, which nothing reveals before
work is done on that label, so any procedure that ends with a qualifying label with probability
1/2 works on at least 2^49.79 labels in expectation. Even at one SHA-256 call (2 units) per
label that is 2^50.7 units, more than the claimed time; and a label shows a positive only after
a 2^32-pair window of it is searched, so the realistic cost is at least 2^81.7 pair evaluations,
2^40 times this whole run (2^41 pairs, 2.9 h on the 15 cores). The 2^20 correction in the table
is an illustration only.

### 5.4 Cross-checks and the list of runs

- The shipped program re-ran all 1024 Phase-A attempts: status, DF, work units, coin words and a
  hash of (E_M, beta0) are identical to the log.
- C++ E against the Python E of the experiment file: all 132,138 round-2 passes the C++ E
  reported in the 512 windows were confirmed by the Python E (same pass, same digest-difference
  weight, coordinate inside the window); on one 2^12 window per space around its first pass, the
  Python E found exactly the passes of the C++ E (512 in total).
- Windows of different spaces: in 406 pairs of spaces from 29 test attempts, no two windows
  intersect, although all spaces share beta0'.
- Runs with the B' advice: the steering check of 2.3 (no E), this run, its cross-checks, and
  organizer-format runs of the experiments. This is the only full-scale run with this advice,
  and the only B' run with LABEL_B. No advice candidate was ever tested for collisions.
- Abandoned plan: before B' we pre-registered and ran locally, in organizer format, an
  experiment plan for the published advice (h23 in 2.3). It was dropped because that advice
  could not be charged credibly; none of its results is used here, and its compute is inside the
  window of 2.3.

### 5.5 Certificates

Collision r5-v6-<i> (i zero-padded to 6 digits) is the one E outputs in the space of attempt i.
All 14, as attempt index (DF): 38 (41), 126 (41), 128 (40), 184 (42), 205 (40), 210 (40), 232
(41), 246 (41), 253 (40), 275 (42), 317 (41), 327 (41), 390 (40), 462 (41). The coordinates are
the list REPLAYS of the experiment file. All 14 ship as certificates, with digests in the
certificate manifest; r5-replay replays all 14. Each is a pair of distinct 135-byte messages
with equal complete 5-round digests (organizer reference sha3_256(m, rounds=5)).

### 5.6 Organizer experiments (experiments/r5_connector.py)

The file is the reference implementation of the coin map, S, one attempt, E restricted to a
window, and B'. Except r5-advice*, each experiment first recomputes the facts of Section 3 and
returns no pair if one differs. A PASS row returns the sentinel (00^135, 01 || 00^134), whose
5-round digest XOR is the declared mask value; a FAIL row returns (00^135, 02 || 00^134), which
fails it. So the host counts successes = PASS and returned_pairs = PASS + FAIL; the host check
of a sentinel is vacuous, and the evidence is the organizer's execution of the visible code.

| id | trials used | what PASS means | local public-seed result |
| --- | --- | --- | --- |
| r5-advice | 0-4 | B' re-derives the advice (trial 0) or an audited attempt matches its log | 5 PASS of 5 returned |
| r5-advice-log | 0-2 | an attempt of candidate 4, 3 or 2 matches its log | 3 PASS of 3 returned |
| r5-connector, r5-conn-b | 0-63 each | one attempt with the trial's seed is accepted and passes Lemmas 1-2 | 63 PASS of 64 returned; 60 PASS of 64 returned |
| r5-den-0 .. r5-den-5 | 90k .. 90k+89 (k = 5: 450-537); no seed used | attempt i of L is accepted with the logged DF (FAIL: rejected as logged; no pair: log wrong); together all 538 indices | 512 PASS of 538 returned (80/90, 84/90, 87/90, 87/90, 88/90, 86/88; no mismatch) |
| r5-replay | 0-13 | full collision: the replayed attempt, basis and Python E reproduce the recorded pair | 14 full collisions |

Each experiment took at most 5.9 s of CPU locally (Python 3.12 and 3.9, each run twice with
identical output). With two non-public nonces in place of the public seed, r5-connector and
r5-conn-b gave 59 and 59, and 61 and 63, PASS of 64; every other experiment exactly as with the
public seed. The r5-den experiments were pre-registered (program hash and per-part predictions)
before their first run.

## 6. Success probability

Theorem (under H2 and H3). Pr[the algorithm outputs a collision] > 0.9987.

Proof. With exact uniform permutations the attempts are i.i.d.: each uses fresh coins on the
fixed target and advice. Let q = Pr[an attempt is accepted] and s = Pr[E outputs a pair |
accepted]. The accepted attempts of an unbounded sequence form an i.i.d. sequence of spaces,
each of which makes E output a pair with probability s. The algorithm fails only if (i) fewer
than K of its A_max attempts are accepted, or (ii) E outputs nothing on the first K accepted
spaces.
- (i): under H3 (q >= 0.05) the mean is at least 3,276.8; by Chernoff, Pr[(i)] <= exp(-(3276.8 -
  512)^2 / (2 x 3276.8)) < 2^-1600.
- (ii): under H2 (s >= s0), Pr[(ii)] = (1 - s)^K <= (1 - 0.013)^512 = 0.0012.

The coin map differs from exact uniform permutations by at most 2^-25 (4.1). So Pr[success] >=
1 - 0.0012 - 2^-1600 - 2^-25 > 0.9987. The claim 0.40 holds for any s >= 0.0010 (K = 512), a
factor 13 below s0. The probability space is the algorithm's coins for the fixed target and
advice; the proof needs no premise about costs, order of events or collisions within a space.

## 7. Time (collision-frontier-v5: one 5-round permutation = 1 unit, other primitives 1/1355)

| Term | Count and price | log2 units |
| --- | --- | --- |
| Trail core: 32 x P | 32 x (1,379,275,399,350 x 2^9 + 1,639,088,128 x 2^12 + 8,674,833 x 2^12 + 2^31) primitives | 43.937 |
| All advice work other than P (H1) | (15 cores x 6,600 s + 1,000) core-seconds, at 2^38 / 1355 each | 44.206 |
| Setup S | <= 2^31 primitives (counted: 2^26.8) | 20.6 |
| Connector | 2^16 attempts x 2^25.46 primitives | 31.06 |
| Bases of enumerated spaces | 512 x 2^24 primitives | 22.60 |
| Enumeration E | 512 x 2^32 pairs x (3 + 256/1355) | 42.674 |
| Total T | sum | 45.328 -> 45.33 |

Every term is a cap on every run. Preprocessing (advice plus S) is 2^45.078, claimed 45.08.
Prices: a T3 leaf of P is at most 512 primitives (5 planes x (5 XOR, 4 OR, popcount <= 24, add,
shift, compare, branch) plus a Gray step amortised over >= 9 leaves); a T2 leaf or T1 node at
most 2^12. A connector attempt is at most 2^25.46 primitives: 2^18 work units x 96 (a row
addition is 7 + 7 loads, 7 XOR and 7 stores of 256-bit words, a leading-bit search of <= 50 and
a pivot lookup), 2^15 coin words x 2^9, and 2^22 for row extraction, table lookups and forms. A
pair in E is 3 units + 256 primitives: the first message's two rounds plus a third L count as
one permutation and both full digests as two more, whether or not the 10-row test passes; the
256 primitives cover the Gray XOR, the row tests and the 256-bit compare. B''s exact counts
price a row operation at 256 primitives and a small one at 8. Sensitivity: charging the H1
window twice gives 45.88; charging the process ledger at 4 x instead of the window would give
44.96.

## 8. Memory

The algorithm: L and L^-1 row forms 643 KB; E_D and E_M at most 322 KB each; tables under 2 MB;
E holds 32 basis states and 2 messages; advice 614 bytes; code under 1 MB: under 2^23 bytes. The
advice runs measured peaks of 42 MB (B') and 4.1 MB (P); all advice work ran on one machine with
48 GiB (2^35.6 bytes) of memory, which bounds it whatever ran concurrently. Declared
memory_log2_bytes = 36.

## 9. Declared heuristics (mirrored in claim.json)

- H1-advice-cost (score-critical). All advice work other than P ran on one 15-core machine
  inside the 6,600 s window of 2.3; one core-second of it is at most 2^38 primitives, and every
  call priced above 1/1355 per primitive runs below 2^27.60 units per core-second (separation,
  2.3). Charge: every core for the whole window, plus 1,000 core-seconds for later re-runs of
  B', 2^44.206 units. Evidence: the hardware bound 2^37.54, B''s measured 2^33.97 instructions
  per second, the measured call rates, r5-advice (B''s exact count, 2^27.12, re-derived by the
  organizer) and the ledger (12,527 CPU-s, 1/8.0 of the charge). Limits: the window endpoints
  and the core count are our statements; the organizer can check the review-run time and B''s
  count. Sensitivity: twice the window gives 45.88.
- H2-space-success (score-critical). For one attempt with fresh coins, conditioned on
  acceptance, E outputs a pair with probability at least s0 = 0.013. Evidence: the
  pre-registered run, 14 of 512 spaces (5.3); r5-replay re-derives every positive and r5-den-0
  .. r5-den-5 the whole denominator. Sampling premise: SHAKE-256-expanded coins from distinct
  seeds give the same q and s as fresh coins. Run-selection premise: this run and its analysis
  were fixed in advance (5.2, 5.4); choosing it among alternatives would have needed work on at
  least 2^49.79 labels: 2^50.7 units even at one SHA-256 call each, and realistically 2^81.7
  pair evaluations (5.3). Limits: few spaces contain collisions, so the interval is wide; all
  spaces share the fixed advice.
- H3-attempt-success (score-critical). One attempt with fresh coins is accepted with probability
  at least q0 = 0.05. Evidence: 123 of 128 organizer-seeded attempts (r5-connector, r5-conn-b;
  one-sided 99.9% lower bound 0.877; Pr[123 of 128 or more if q <= 0.05] < 2^-504) and Phase A's
  960 of 1024. Premises as for H2; the organizer seeds are not ours to choose. Limits: the seeds
  are public and the harness draws no inference.

## 10. Not claimed; credits

Not claimed: any improvement on the method of [GLL+20] beyond the byte-aligned (p = 8)
adaptation, the B' difference/value phases, and the accounting. The time is a hard cap; the
certificates show that the construction works and are not the claimed cost. Credits: [GLL+20]
for the connector and linearisation framework and the 5-round trail core that P re-derives;
Dinur, Dunkelman, Shamir (FSE 2012) for the target-difference algorithm; Qiao, Song, Liu, Guo
(EUROCRYPT 2017) for linearisation; Daemen, Van Assche (FSE 2012) and KeccakTools for in-kernel
trail cores. hybridnoise's public note (package ef4a0c66 on this track) showed that an own-beta1
byte-aligned connector can work; none of its code, data or certificates is used. jagnani73's
accepted package 654cb3d2 taught us to charge advice searches with a margin and to use fresh
coins, hard caps and organizer experiments; none of its constructions is reused.
baseline_improved is the required nominal reference ID, not a claim of dominance.

## Appendix A. Source of the multithreaded E of the full-scale run (C++17)

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

`bf.cpp`:

```cpp
// Brute-force stage: enumerate x in x0 + span(basis) (basis excludes beta0), pair (x, x^beta0).
// Stage 1: round-2 conditions on message 1 (beta2 -> alpha3 rows). Stage 2: full 5-round digests of both.
// Usage: bf spacefile nthreads [dimlimit]
#include "kc.h"
#include <thread>
#include <atomic>
#include <mutex>
static St X0,B0; static std::vector<St> BS; static int D;
static int crow_y[16],crow_z[16];static uint32_t cmask[16];static int ncr=0;
static std::mutex mu; static std::atomic<unsigned long long> s1tot(0),coll(0),evals(0);
static inline void chiRC(St&s,int r){chi(s);s.a[0]^=RC[r];}
static void run(int tid,int nth,int dim){
  // thread handles cosets indexed by top bits: split dim into low part L and high part H with 2^H >= nth
  int H=0;while((1<<H)<nth)H++; if(H>dim)H=dim; int Lw=dim-H;
  for(unsigned hc=tid;hc<(1u<<H);hc+=nth){
    St x=X0; for(int b=0;b<H;b++)if((hc>>b)&1)xr(x,BS[Lw+b]);
    unsigned long long n=1ULL<<Lw, s1=0;
    for(unsigned long long i=0;i<n;i++){
      if(i){int j=__builtin_ctzll(i);xr(x,BS[j]);}
      St s=x; chiRC(s,0); Lmap(s); chiRC(s,1); Lmap(s);
      bool ok=true;
      for(int k=0;k<ncr&&ok;k++){int v=rowval(s,crow_y[k],crow_z[k]);if(!((cmask[k]>>v)&1))ok=false;}
      if(!ok)continue;
      s1++;
      St a=x,b=x;xr(b,B0);
      chiRC(a,0);chiRC(b,0);
      for(int r=1;r<5;r++){Lmap(a);chiRC(a,r);Lmap(b);chiRC(b,r);}
      int dw=0;for(int l=0;l<4;l++)dw+=__builtin_popcountll(a.a[l]^b.a[l]);
      std::lock_guard<std::mutex> g(mu);
      printf("S1 dw=%d x=",dw);for(int l=0;l<25;l++)printf("%016llx",(unsigned long long)x.a[l]);printf("\n");
      if(dw==0){coll++;printf("COLLISION\n");}
      fflush(stdout);
    }
    s1tot+=s1;evals+=n;
  }
}
static void rd(FILE*f,St&s){for(int l=0;l<25;l++){unsigned long long v;if(fscanf(f,"%llx",&v)!=1){fprintf(stderr,"parse\n");exit(1);}s.a[l]=v;}}
int main(int argc,char**argv){
  initDDT();
  FILE*f=fopen(argv[1],"r");rd(f,B0);rd(f,X0);int inD;fscanf(f,"%d %d",&D,&inD);BS.resize(D);for(int i=0;i<D;i++)rd(f,BS[i]);fclose(f);
  int nth=argc>2?atoi(argv[2]):4;int dim=argc>3?atoi(argv[3]):D;if(dim>D)dim=D;
  // core No.3 alpha3 (canonical) and beta2 rows
  int a3bits[10]={0,130,450,529,701,789,1021,1169,1280,1429};St a3;zero(a3);for(int b:a3bits)flip(a3,b);
  St b2;zero(b2);const u64 B2[25]={0x1,0,0x4,0,0,0x4,0x4,0x4,0x20000,0,0x2000000000000000ULL,0,0x200000,0,0,0x2000000000000000ULL,0,0,0x20000,0,0x200001,0,0x200000,0,0x1};
  for(int l=0;l<25;l++)b2.a[l]=B2[l];
  for(int y=0;y<5;y++)for(int z=0;z<64;z++){int d=rowval(b2,y,z);if(!d)continue;int o=rowval(a3,y,z);uint32_t m=0;for(int v=0;v<32;v++)if((chi5(v)^chi5(v^d))==o)m|=1u<<v;crow_y[ncr]=y;crow_z[ncr]=z;cmask[ncr]=m;ncr++;}
  // sanity: alpha3 rows outside beta2 rows must be zero
  fprintf(stderr,"rows=%d dim=%d\n",ncr,dim);
  std::vector<std::thread> th;for(int t=0;t<nth;t++)th.emplace_back(run,t,nth,dim);for(auto&t:th)t.join();
  fprintf(stderr,"DONE evals=%llu stage1=%llu collisions=%llu\n",(unsigned long long)evals,(unsigned long long)s1tot,(unsigned long long)coll);
  printf("DONE evals=%llu stage1=%llu collisions=%llu\n",(unsigned long long)evals,(unsigned long long)s1tot,(unsigned long long)coll);
}
```
