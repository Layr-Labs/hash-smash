# 5-round SHA3-256: a byte-aligned connector on the published GLL+20 difference, with charged advice and a pre-registered fresh-coin measurement

This is an exploratory claim. The claimed time is a hard cap of the specified algorithm, valid
on every run, and the charged construction of the advice dominates it. The algorithm of Section 4
was executed at full scale in a pre-registered run (5.2). Every attempt in that run has its own
seed, so the samples are independent. The run found 21 collisions of 135-byte messages, in
21 of 768 spaces. The first 16 ship as certificates, and an organizer experiment
re-derives all 21 with E's own tests.
[GLL+20] = J. Guo, G. Liao, G. Liu, M. Liu, K. Qiao, L. Song, "Practical Collision Attacks
against Round-Reduced SHA-3", J. Cryptology 33 (2020) 228-270, ePrint 2019/147.

## 0. Claim, summary, changes, checklist

| Field | Value | Basis |
| --- | --- | --- |
| time_log2 | 49.35 | hard cap 2^49.341, rounded up (Section 7) |
| success_probability | 0.40 | > 0.9791 under H2 and H3 (Section 6) |
| memory_log2_bytes | 65 | Section 8; the algorithm itself uses < 2^23 bytes |
| preprocessing_log2 | 49.34 | advice steps (b)+(c), 2^49.300 (H1), plus 32 x P for step (a), 2^43.94 |
| nonuniform_advice_log2_bytes | 8.1 | the published pair, 2 x 1084 bits = 271 bytes |

Summary. (1) The advice is the published SHA3-256 colliding pair of [GLL+20] (Table 17); the
algorithm reads four differences from it (Section 2). (2) The advice's construction is charged in
full: its trail search, step (a), at 32 x the exact cost of our executed search P, which returns
the advice's trail core bit for bit; its connector and brute-force runs, steps (b) and (c), at
twice their published single-core times at 2^38 primitives per core-second (H1). (3) The
connector works on byte-aligned 135-byte messages (p = 8 fixed padding bits, zero capacity): a
target-difference value phase steered toward the published round-0 difference, then the
non-full linearisation of [GLL+20], hard-capped at 2^18 work units (2^25.46 primitives) per
attempt. (4) E searches up to K = 256 accepted spaces, 2^32 pairs each, with a full 256-bit
digest test; attempts use independent coins, so the spaces are i.i.d. (5) Heuristics: H1 (advice
construction time); H2 (per-space output probability s0 = 0.015, the one-sided 99%
Clopper-Pearson bound of the pre-registered run, with no Markov value or clustering allowance);
H3 (per-attempt acceptance q0 = 0.02; 99.9% bound 2.74% from 32,768 attempts).

Changes since v4. A committee simulation reviewed v4. Each of its material findings, and each
premise it rated unsupported, is answered below.

| v4 finding | Fix |
| --- | --- |
| Implicit premise: seeded MT19937 streams give i.i.d. samples (unsupported) | New pre-registered run (5.2). Attempt i has its own seed SHA-256(label \|\| i), expanded by SHAKE-256 through the specified coin map, so samples are independent by construction. The remaining premise, that the XOF behaves as fresh coins, is stated inside H2 and H3. Cross-checks: os.urandom seeds, homogeneity tests, the 14 v4 streams (5.3) |
| H2 rested on a 1/19 Markov-clustering allowance, pooled per-pair rates, and development spaces outside the window | H2 is the per-space Bernoulli count in the specified regime (768 spaces, each exactly the 2^32 window), and s0 is its 99% lower bound. Markov values are context only (5.4). Development spaces are not used |
| H2's "contains a collision" is not the event E detects | H2 now reads "E, run on the space, outputs a pair" |
| H2 and H3 conditioned on the past; space test; disjointness tested only up to 160 | The space test is removed. Spaces from independent attempts are i.i.d., so success follows exactly from two single-attempt probabilities (6). Repeated pairs across spaces do not affect the bound |
| H1 memory clause unsupported | Removed. memory_log2_bytes = 65 follows from H1's own time bound at <= 32 bytes per primitive (8) |
| H1 accounting: P replaces the authors' GPU-assisted trail search | The accounting reading is stated in Section 2. Step (a) is charged at 32 x P, the margin of accepted precedent 654cb3d2 for the same kind of charge |
| H1's conversion ignores popcount, bit-scan, multiply and 512-bit instructions | The rate is raised from 2^36 to 2^38 per core-second: 2^35.22 micro-operations/s x 6.9 primitives each (2) |
| The attack used P's unverifiable output (hard-coded BETA2) | The algorithm reads alpha2 and alpha3 from the advice pair. P is only the charged surrogate for step (a). The organizer facts check that P's reported output equals the advice's trail |
| P and C++ E sources not shipped; denominators unverifiable | Both are embedded as inert text in the experiment file. r5-replay runs the shipped Python E around every recorded collision. The two E implementations agree (5.3) |
| r5-connector: vacuous host check, 160 trials | 256 trials, and the vacuity is stated in the manifest and in 5.6 |
| Replay MT states not tied to (seed, index); lin_options outside the work counter; code's coin map differs from the specification | Each replay derives its seed from (label, i) inside the trial. The linearisation table is built and charged in setup S (4.3, 7). The code implements the specified coin map (class Coins) |
| Inconsistencies; reviewer-directed wording | Harmonised. No text instructs the reader to run anything |

Checklist (each item can be re-derived from this file or the experiment source): (1) messages of
135 bytes, padded block M || 0x86 || 0^512, 520 fixed state bits (1); (2) the advice's trail has
w1 = 127, w2 = 24, AS(alpha2) = 59, C1 = 2^19, C2 = 3^20, P45 = 55/2^19 with 192 nonzero terms
(3); (3) per attempt at most 2^18 work units and 21,930 coin words, 2^25.46 primitives (4.4, 7);
(4) success 1 - 2^-175.5 - (1 - 0.015)^256 - 2^-25 > 0.9791 (6); (5) time 2^49.300 + 2^43.937 + 2^41.673 + 2^30.06 + small = 2^49.341 (7).

## 1. Target, messages, notation

sha3-256-r5-prefix-v1 is FIPS 202 SHA3-256 restricted to rounds 0-4 of Keccak-f[1600] in every
permutation call. It has rate 1088, capacity 512 and a zero initial state; the suffix is 01 with
pad10*1 (delimited byte 0x06); the digest is the first 32 bytes squeezed (lanes 0..3).

Round i maps A to chi(L(A)) xor RC[i], with L = pi o rho o theta. State bit (x,y,z) has index
64(x+5y)+z. Block byte j is lane floor(j/8), bits 8(j mod 8)..8(j mod 8)+7. chi acts on the 320
rows (y,z) by chi5(v)_i = v_i xor (NOT v_{i+1}) v_{i+2}, indices mod 5.

All messages are exactly 135 bytes. The initial state is A0 = M || 0x86 || 0^512, one
permutation is applied, and the digest is lanes 0..3 of its output. The fixed set F = bits
1080..1599 (520 bits) holds constants: bits 1081, 1082 and 1087 are 1, and the rest are 0. The
1084-bit messages of [GLL+20] fix only 4 bits (1084..1087), so they are not valid inputs here.

For a pair of states, alpha_i is the difference entering round i (alpha_0 is the block
difference), beta_i = L(alpha_i) is the difference entering chi, and chi maps beta_i to
alpha_{i+1}. DDT[d][o] = #{v : chi5(v) xor chi5(v xor d) = o}, and a row transition d -> o has
weight w = 5 - log2 DDT[d][o]. x = L(A0) is the first message's round-0 chi input; the second
message has x xor beta0. A linear form over x is a 1601-bit vector, whose bit 1600 is the
constant.

Row facts, checked exhaustively over all 32 x 32 pairs (d, o):
- R1. V(d,o) = {v : chi5(v) xor chi5(v xor d) = o} is an affine subspace of dimension
  log2 DDT[d][o] whenever DDT[d][o] > 0. A transition is therefore exactly w affine equations on
  one message's row value.
- R2. The least weight of a transition into a nonzero o is 2. It is 3 when o has at least 3 bits
  and is not exactly three cyclically consecutive bits.

## 2. Advice, its construction, and how it is charged

Published inputs:
- G1 ([GLL+20] Table 17): a 5-round SHA3-256 colliding pair of 1084-bit messages, listed in the
  experiment source (PUB_M1, PUB_M2). This is the advice: 2 x 1084 bits = 271 bytes.
- G2 ([GLL+20] Table 6, SHA3-256 row): trail core No. 3; connector time Tc = 428.8 h;
  brute-force time Tb = 45.6 h; DF = 37. The table's footnote says the times are for "one CPU
  core", except for one 6-round row that used three GPUs. Their Section 5.4 places the GPU in the
  trail search, and in the brute force for lower-probability trails.
- G3 ([GLL+20] Tables 5 and 9): core No. 3 has weights 127-24-19 and is the core they used.

What the algorithm reads. With A1, A2 the published states and s_r(A) the state after round r:
beta0_pub = L(A1) xor L(A2); beta1_pub = L(s_0(A1)) xor L(s_0(A2)); alpha2 = s_1(A1) xor s_1(A2);
alpha3 = s_2(A1) xor s_2(A2). No other part of the algorithm depends on [GLL+20].

Accounting. The cost model charges all construction of the advice, including any search left out
of the submitted program. [GLL+20] produced the pair in three steps:
- (a) a GPU-assisted trail search, whose time is not published, which output core No. 3, i.e.
  alpha2, alpha3 and the later rounds;
- (b) one connector run given core No. 3, which chose beta1 and produced a message space;
- (c) one brute-force run in that space.

The pair, and hence all four differences, is the output of (a), (b) and (c) run with their
coins. We charge:
- Step (a): our deterministic search P (4.2), executed once, outputs core No. 3 bit for bit. Its
  exact leaf counts give 2^38.94 units. We charge 32 times that, 2^43.94, so that the charge does
  not depend on how closely P resembles the authors' tooling. The accepted precedent 654cb3d2
  charged its re-run characteristic search with a margin of about 32.
- Steps (b) and (c): twice their published sum, 2 x 474.4 core-hours = 3,415,680 core-seconds,
  at no more than 2^38 primitives per core-second (H1). This is 2^59.70 primitives = 2^49.300
  units. The factor 2 covers unreported preliminary runs and machine differences.

Why 2^38 per core-second: 2^38 = 5 x 10^9 cycles/s x 8 micro-operations per cycle x 6.9. No x86
core sold up to 2019 exceeds 5.0 GHz or retires more than 8 micro-operations per cycle. In GF(2)
elimination and Keccak, a micro-operation is a load, store or ALU operation on at most 512 bits,
possibly fused with one load: at most 4 primitives. Popcount, bit-scan and multiply cost at most
2^7 primitives each, so the average stays below 6.9 while fewer than 1 in 45 micro-operations is
one of them; these workloads are dominated by XOR row operations. Calibration: [GLL+20] report
2^21-2^22 Keccak-f[1600] evaluations per second per core, i.e. 2^34.7 primitives per second at
271 primitives per round, 9.8 times below 2^38.

## 3. Exact facts (recomputed by both organizer experiments before any trial)

### 3.1 The advice's trail core (core No. 3)

alpha3 = bits {0, 130, 450, 529, 701, 789, 1021, 1169, 1280, 1429}. Nonzero lanes, in hex, with
bit z = 2^z:

    alpha3: 0:1 2:4 7:4 8:20000 10:2000000000000000 12:200000 15:2000000000000000 18:20000
            20:1 22:200000
    beta3:  0:1 2:1 3:4000000000 7:1 9:40000 11:100 14:40000 20:1 21:100 23:4000000000
    beta2:  0:1 2:4 5:4 6:4 7:4 8:20000 10:2000000000000000 12:200000 15:2000000000000000
            18:20000 20:200001 22:200000 24:1

| Quantity | Value |
| --- | --- |
| alpha3 | 10 bits and 10 active rows, in the CP kernel |
| beta3 = L(alpha3) | 10 bits and 9 active rows, in the CP kernel |
| beta2 -> alpha3 | same 10 rows, every row compatible, w2 = 24 |
| alpha2 = L^-1(beta2) | 114 bits and 59 active rows; w1 = 127 (sum of least weights, R2) |
| C1 = # alpha4 compatible with beta3 | 2^19 |
| C2 = # beta2 compatible with alpha3 | 3^20 = 3,486,784,401 |

The experiments compute alpha2 and alpha3 from the advice pair and check that they equal these
constants, which are P's reported output (5.1). The published pair's 5-round digests are equal.
alpha1_pub = L^-1(beta1_pub) has 318 active rows, whose round-0 transitions are 75 of DDT 2, 156
of DDT 4 and 87 of DDT 8. beta1_pub -> alpha2 has weight 127.

### 3.2 Rounds 3-4 to a zero digest difference (context only)

The digest is bits x = 0..3 of the 64 rows of plane y = 0. For such a row with input difference
d, PZ[d] = (DDT[d][0] + DDT[d][0x10])/32 is the probability of zero output difference on
x = 0..3. Under the Markov model

    P45 = sum over alpha4 in prod_r {o : DDT[d_r][o] > 0} of
          prod_r DDT[d_r][o_r]/32 x prod over nonzero plane-0 rows q of L(alpha4) of PZ[q].

The sum has 2^19 terms (9 rows of beta3), of which exactly 192 are nonzero, and P45 = 55/2^19 =
2^-13.2186. With w2, p_M = 2^-37.2186 per pair. No claimed number uses this Markov value.

### 3.3 Why the published difference cannot be reused unchanged

Take the fixed-bit equations together with the round-0 equations x_r in V(beta0_pub,r,
alpha1_pub,r) (R1). With the published p = 4 fixed values there are 1458 equations of rank 1400,
consistent. With the p = 8 values of Section 1 there are 1462 equations of rank 1403 and one
contradiction. A byte-aligned connector must therefore change beta0. Ours keeps beta1_pub and
steers beta0 toward beta0_pub (4.4).

## 4. Algorithm

### 4.1 Parameters and coins

Parameters: at most A_max = 2^15 connector attempts; at most K = 256 enumerated spaces; a
per-attempt cap of X_max = 2^18 work units (4.4); acceptance threshold DF >= 33; 2^32 pairs per
space.

Coins are independent uniform 256-bit words, drawn fresh by the algorithm. Every random choice is
a uniform random permutation of a list by Fisher-Yates: for i = n-1 down to 1, j = (low 64 bits
of one fresh word) mod (i+1), and positions i and j are swapped. Lists have at most 318 elements,
so each index is within 318/2^64 < 2^-55.6 of uniform. An attempt makes at most 21,930 draws,
counted from the list sizes (20,063 in D2, 954 in M2, 913 in M3), so a whole run is within 2^-25
of exact uniform permutations in total variation; Section 6 subtracts this. The target and the
advice are fixed. The algorithm uses no stored pair, seed expansion or counter; our runs and the
experiments expand seeds, as Section 5 states.

### 4.2 Phase P: trail-core search (the charged surrogate for step (a); run once)

P's output is not an input of the algorithm (Section 2); P is specified so that its charge is well
defined, and its C++ source is embedded as inert text in the experiment file.
- T1 (2-round in-kernel cores): a candidate alpha3 is a set of at most 10 bits whose
  alpha-columns (x,z) and beta-columns (columns of pi o rho of each bit) all hold an even number
  of bits. Depth-first search from each of the 25 bits with z = 0. At a node, let c be the
  smallest odd alpha-column, else the smallest odd beta-column. If none exists, the node is a
  core: record it in canonical form (the smallest sorted bit list over the 64 z-translations).
  Otherwise, if the node has fewer than 10 bits, branch on each bit of column c not yet in the
  set (for a beta-column, the pi o rho preimages).
- T2 (forward): beta3 = pi o rho(alpha3); enumerate every alpha4 compatible with beta3,
  accumulate P45 (3.2), and keep the cores with P45 > 0.
- T3 (backward): for each kept core, enumerate every beta2 compatible with alpha3 in reflected
  mixed-radix Gray order, maintaining alpha2 = L^-1(beta2) incrementally; compute w1 (R2) only
  when 2 AS(alpha2) does not exceed the best w1 so far (w1 >= 2 AS, so no improving leaf is
  skipped).
- Output: the (core, beta2) with the least w1; ties go to the smaller w2, then to the
  lexicographically smaller choice vector.

### 4.3 Setup S

Setup S computes:
- L and L^-1 as 1600 row forms each.
- The four differences of Section 2, and alpha1 = L^-1(beta1_pub), which has 318 active rows.
- The 127 round-1 conditions. For each of the 59 active rows of alpha2, they are the equations of
  V(beta1_pub row, alpha2 row) (R1) on the round-1 chi input z = L(chi(x) xor RC0). Each
  condition is a sum, over round-0 rows r, of a 5-bit mask applied to row r of chi(x). M_r is the
  set of masks that occur for row r.
- The equations of all 2,451 affine subsets of GF(2)^5, and the 10 row tests of E.
- The linearisation table. For each of the 320 rows with nonempty M_r, and each set S_r that M3
  can meet (V(d, alpha1_r) for every compatible d, or all 32 values for an inactive row), the
  entry is either S_r itself, if every mask of M_r is affine on S_r, or the list of all
  largest-dimension affine W in S_r on which every mask is affine. The table has 3,183 entries
  and takes 517,621 inner steps of at most 64 primitives each.

### 4.4 One connector attempt

An attempt uses two echelon systems over GF(2), with undo: E_D on delta (the unknown beta0) and
E_M on x. One counter, shared by both systems, counts work units. A work unit is one call of the
reduction routine, or one row addition (an XOR of two stored forms) inside it. If the counter
exceeds X_max = 2^18, the attempt stops and fails. The reference implementation is `attempt()`
in experiments/r5_connector.py.

- D1. E_D receives (L^-1 delta)_j = 0 for j in F, and delta_r = 0 (5 equations) for every row r
  where alpha1 is zero.
- D2. Draw a uniformly random order Q of the 318 active rows. For each row r in Q, with
  o = alpha1_r and rv = (beta0_pub)_r, try k = 2, 1, 0 in turn. Permute uniformly the
  k-dimensional affine subsets of {d : DDT[d][o] > 0}, and keep those that contain rv. Take the
  first subset U whose equations (delta_r in U) are consistent with E_D, and add them. If no k
  works, fail.
- M1. E_M receives (L^-1 x)_j = F_j for j in F.
- M2. For each r in Q, order the elements of U_r by a uniform permutation, then stably by
  DDT[d][o] descending, then stably with d = rv first. Take the first d for which delta_r = d is
  consistent with E_D and x_r in V(d,o) (R1) is consistent with E_M. Add both and set
  beta0_r = d. If no d works, fail.
- M3. Linearise, rows in index order. Let S_r = V(beta0_r, alpha1_r) for active rows and all 32
  values otherwise, and look up its table entry. If the entry is S_r itself, W_r = S_r.
  Otherwise permute the listed W uniformly; take the first W whose equations E_M already
  implies, failing that the first consistent with E_M (adding its equations); if none, fail.
  On W_r each mask of M_r is an explicit affine form in x_r.
- M4. Substitute these forms into the 127 round-1 conditions and add them to E_M. If they are
  inconsistent, fail.
- M5. DF = 1600 - rank(E_M). Accept iff DF >= 33, and output (E_M, beta0).

This differs from [GLL+20] Algorithms 1-3 and Section 4.6 in three ways: beta1 is fixed to
beta1_pub, the difference phase is steered toward beta0_pub, and linearisation is per occurring
mask.

### 4.5 Space and enumeration E

Let V be the solutions of E_M (dimension DF), and let beta = beta0.

Basis. The offset v0 is the solution with all free variables 0. b_i = (solution with free
variable i set) xor v0, with free variables in increasing order. Add beta, then b_1, b_2, ...,
keeping each vector that is independent of those added before. W is the span of the first 32
kept b_i; it exists because DF >= 33.

Enumeration and test. Enumerate x in v0 + W in Gray-code order (one 7-word XOR per step). For
each x, compute the first message's round-2 chi input u = L(chi(L(chi(x) xor RC0)) xor RC1), and
test the 10 active rows of beta2: u_r in V(beta2_r, alpha3_r). If all 10 pass, compute both
complete 5-round digests of A0 = L^-1(x) and A0' = L^-1(x xor beta). If all 256 bits are equal,
output (bytes 0..134 of A0, bytes 0..134 of A0') and halt.

### 4.6 Main loop

Run S. For a = 1..A_max: run attempt a; if it is accepted, run E on its space and halt with E's
output if there is one; if E has now run K times, halt with failure. After A_max attempts, halt
with failure. Phase P is charged as preprocessing (Section 2); nothing in the loop reads its
output.

### 4.7 Correctness

Lemma 1 (outputs are collisions). For x in V, A0 = L^-1(x) satisfies the fixed-bit equations of
E_M. A0' = A0 xor L^-1(beta) does too, because E_D forces (L^-1 beta)_j = 0 on F. Both are
therefore padded 135-byte messages. beta != 0, since its 318 rows are compatible with nonzero
alpha1 rows. E outputs only after comparing the true 256-bit digests.

Lemma 2 (two rounds). For x in V, the pair has difference alpha1 after round 0: active rows
satisfy x_r in V(beta_r, alpha1_r) (R1), and inactive rows have zero difference. Each mask of M_r
equals its affine form on V, so the 127 round-1 conditions hold exactly and the difference after
round 1 is alpha2. This lemma is needed only for the probability.

Lemma 3 (distinct pairs within a space). beta is not in W, so the 2^32 unordered pairs
{x, x xor beta} of one space are distinct. Pairs of different spaces may coincide; Section 6 does
not need them to be distinct.

## 5. Executed runs (evidence)

### 5.1 Phase P

| Stage | Result |
| --- | --- |
| T1 | 8,674,833 nodes; 1741 cores (8 of 6 bits, 139 of 8, 1594 of 10) |
| T2 | C1 per core is 2^12 (8 cores), 2^15 (2), 2^16 (137), 2^18 (14), 2^19 (58) or 2^20 (1522); sum C1 = 1,639,088,128 leaves; 467 cores have P45 > 0 |
| T3 | C2 per kept core is 3^12 (1), 3^14 (1), 3^16 (47), 100 x 3^12 (1), 3^18 (9), 10 x 3^16 (16) or 3^20 (392); sum C2 = 1,379,275,399,350 leaves |

The least w1 is 127, reached by exactly one core and one beta2 (w2 = 24). That result equals the
advice's trail (3.1) bit for bit, at the same z-offset. The next best core has w1 = 263. The
machine also counted 7.95 x 10^13 retired instructions and a 4.1 MB peak; neither is used for
charging.

### 5.2 The pre-registered fresh-coin run

Before the run, we recorded a plan (constant PREREG of the experiment file, SHA-256 a881367e...).
It fixed the label, the seed rule, the attempt count, the number of spaces, the statistics and
the confidence levels, with no stopping, exclusion or re-run.
- Seeds: attempt i used seed_i = SHA-256(L || i as 8 little-endian bytes), with
  L = "hashsmash sha3-256-r5 v5 run".
- Coins: the words SHAKE-256(seed_i || k), k = 0, 1, ..., fed through the coin map of 4.1
  (class Coins of the experiment file, which is the code that ran).

Phase A covered attempts i = 0..32767: 992 accepted (3.03%; one-sided 99.9% Clopper-Pearson
lower bound 2.74%), 31,416 failed in M2, 300 in M4, and 60 had DF < 33. Accepted DF: 33 (247),
34 (405), 35 (245), 36 (83), 37 (9), 38 (2), 39 (1). The largest attempt used 165,608 work units
(cap 262,144) and at most 4,423 coin words. Over 32 consecutive blocks of 1024 attempts the
acceptance counts give chi-square 23.9 on 31 df (p = 0.82).

Phase B took the first 768 accepted attempts (indices up to 24,973) and ran E on each over
exactly its specified 2^32-pair window. E here is the multithreaded C++ program embedded in the
experiment file, with the tests of 4.5; 5.3 checks it against the Python E.

| Quantity | Value |
| --- | --- |
| pairs | 768 x 2^32 = 2^41.58 |
| round-2 passes | 197,291 (1.003 x the 2^-24 expectation); per-space variance/mean 1.05 |
| spaces where E outputs a pair | 21 of 768; 21 collisions in total |
| s-hat; two-sided 95% interval | 0.0273; [0.0170, 0.0415] |
| one-sided 99% Clopper-Pearson lower bound | 0.01548, so s0 = 0.015 |

Each of these 21 spaces contains exactly one collision (5.5 lists them).

### 5.3 Cross-checks

| Check | Result |
| --- | --- |
| acceptance with seeds from os.urandom(32) | 256 of 8,192 (3.13%); against the main run, chi-square 0.21 (p = 0.65) |
| organizer-style local r5-connector run (public seed, all 256 trial seeds) | 8 of 256 accepted and verified |
| v4 MT19937 streams (101-108 x 700, 201-206 x 1500; 490 of 14,600) | per-stream counts 23 26 23 28 21 34 23 29 53 45 45 47 42 51: chi-square 10.66 on 13 df (p = 0.64). All three coin sources together: chi-square 3.60 on 2 df (p = 0.17) |
| v4 full-scale run (160 spaces of 2^32 pairs, MT coins) | 1 space with a collision; consistent with s-hat; not used for H2 |
| C++ E against Python E | all 197,291 round-2 passes that the C++ E reported in 768 spaces were confirmed by the Python E (same pass, same digest-difference weight, coordinate inside the window); on 768 windows of 2^12 around them, the Python E found exactly the same passes as the C++ E (768 in total) |

### 5.4 Context: the Markov model (not used for any claimed number)

The Markov-Poisson value per space is 1 - exp(-2^32 p_M) = 0.0265 (3.2); s-hat is 1.03
times that, with the wide interval of 5.2. The round-2 pass rate matches 2^-24 (5.2), so any
deviation from the model lies in rounds 3-4 or in clustering inside a space. H2 is stated in
terms of the measured event, so the model does not enter the claim.

### 5.5 Certificates

Collision r5-v5-<i> (i zero-padded to 6 digits) is the one E outputs in the space of attempt i.
All 21, as attempt index (DF), are: 943 (33), 2190 (35), 2704 (33), 3183 (33), 5732 (34), 7904
(35), 9726 (34), 9919 (35), 11032 (34), 13359 (36), 13690 (36), 14402 (36), 15238 (37), 16169
(34), 17854 (34), 19236 (34), 19326 (35), 20272 (36), 20737 (34), 21826 (36), 22852 (36). The
recorded coordinates are the list REPLAYS of the experiment file. The first 16 ship as
certificates (the schema maximum), with digests in the certificate manifest; r5-replay replays
all 21. Each is a pair of distinct 135-byte messages with equal complete 5-round digests
(organizer reference sha3_256(m, rounds=5)).

### 5.6 Organizer experiments

experiments/r5_connector.py is the reference implementation of the coin map, S, one attempt, and
E restricted to a window. It serves two declared experiments. Each first recomputes every fact of
Section 3, including the check that P's reported output equals the advice's trail, and returns no
pair if any fact differs.

r5-connector. Each of the 256 organizer trials runs one attempt whose coin words are the SHAKE-256
expansion of the trial's organizer seed. If the attempt is accepted, two points of its space are
checked against Lemmas 1-2: valid distinct 135-byte messages, block difference L^-1(beta0), and
difference alpha2 after rounds 0-1. A passing trial returns a fixed sentinel pair (00^135,
01 || 00^134) whose 5-round digest XOR is the declared mask value; any other outcome returns no
pair. The host check of the sentinel is vacuous (no 5-round digest predicate can see a 2-round
difference): the evidence is the organizer's execution of the visible checking code. The host
count of returned pairs equals the number of accepted, verified attempts: 7.8 expected at 3.03%,
at least 5.1 under H3. Our local run with the public seed returned 8 of 256, using 6 s of CPU
(Python 3.12) and 21 MB.

r5-replay. For each recorded collision the trial recomputes seed_i from (L, i), runs that attempt again,
rebuilds the basis of 4.5, runs the Python E on the 2^12 aligned coordinates that contain the
recorded one, and returns E's output if it is the recorded point. The host checks that the pair
is a full collision. This ties each collision to an attempt() space and to E's own tests; it
does not measure the rate (5.2 does).

## 6. Success probability

Theorem (under H2 and H3). Pr[the algorithm outputs a collision] > 0.9791.

Proof. With exact uniform permutations, attempts are i.i.d.: each uses its own fresh coins on the
fixed target and advice. Let q = Pr[an attempt is accepted] and s = Pr[E outputs a pair |
accepted]. The number of accepted attempts among A_max is Binomial(A_max, q). In an unbounded
sequence of attempts, the accepted ones form an i.i.d. sequence of spaces, each of which makes E
output a pair with probability s.

The algorithm fails only if (i) fewer than K of its A_max attempts are accepted, or (ii) E outputs
nothing on the first K accepted spaces.
- (i): under H3 (q >= 0.02) the mean count is at least 655.4. By Chernoff,
  Pr[(i)] <= exp(-(655.4 - 256)^2 / (2 x 655.4)) = 2^-175.5.
- (ii): under H2 (s >= s0), Pr[(ii)] = (1 - s)^K <= (1 - 0.015)^256 = 0.0209.

The coin map differs from exact uniform permutations by at most 2^-25 (4.1). So
Pr[success] >= 1 - 0.0209 - 2^-175.5 - 2^-25 > 0.9791. The claim is 0.40, which holds for
any s >= 0.0020 (K = 256), a factor 7.5 below s0 and 14 below s-hat.

The proof needs no assumption about attempt costs, the order of events, or collisions within a
space. The probability space is the algorithm's coins, for the fixed target and fixed advice.

## 7. Time (collision-frontier-v5: one 5-round permutation = 1 unit, other primitives 1/1355)

| Term | Count and price | log2 units |
| --- | --- | --- |
| Advice, steps (b)+(c) (H1) | 3,415,680 core-s x 2^38 / 1355 | 49.300 |
| Advice, step (a): 32 x P | 32 x (1,379,275,399,350 x 2^9 + 1,639,088,128 x 2^12 + 8,674,833 x 2^12 + 2^31) primitives | 43.937 |
| Setup S | <= 2^31 primitives | 20.6 |
| Connector | 2^15 attempts x 2^25.46 primitives | 30.06 |
| Bases of enumerated spaces | 256 x 2^24 primitives | 21.60 |
| Enumeration E | 256 x 2^32 pairs x (3 + 256/1355) | 41.673 |
| Total T | sum | 49.341 -> 49.35 |

Every term is a cap on every run: attempts, work per attempt, enumerated spaces and pairs per
space are all bounded. Preprocessing (advice plus S) is 2^49.334, claimed 49.34. Prices:
- P: a T3 leaf is at most 512 primitives (5 planes x (5 XOR, 4 OR, popcount <= 24, add, shift,
  compare, branch), plus a Gray step amortised over >= 9 leaves; the 545 full w1 evaluations of
  about 1000 each fit in the margin). A T2 leaf or T1 node is at most 2^12 (a 25-lane copy and
  XOR, 64 row extractions and bookkeeping; or parity scans and 64 translations x a sort of 10).
- Setup S (<= 2^31): 3,200 evaluations of L or L^-1 (<= 2^12 each), the theta^-1 matrix, 2,451
  annihilators (<= 2^11 each) and the linearisation table (517,621 steps x 64).
- Connector attempt (<= 2^25.46): 2^18 work units x 96 (a row addition is 7 + 7 loads, 7 XOR and
  7 stores of 256-bit words, a leading-bit search of <= 50 and a pivot lookup; a call costs
  less); 2^15 coin draws x 2^9 (a fresh word, a 64-bit shift-and-subtract reduction, a swap);
  2^22 for row extraction, table lookups and building forms.
- Pair in E (3 units + 256 primitives): the first message's two rounds plus a third L count as
  one permutation and both full digests as two more, whether or not the 10-row test passes; the
  256 primitives cover the Gray XOR, the 10 row tests and the 256-bit compare.

Sensitivity: 2^37 or 2^39 primitives per core-second gives 48.39 or 50.33. Slack
factor 1 instead of 2 also gives 48.39. All non-advice terms x 8 gives 49.61.

## 8. Memory

The algorithm: L and L^-1 row forms 643 KB (2 x 1600 x 201 bytes); E_D and E_M at most 322 KB
each; tables (DDT, affine subsets and their equations, linearisation table) under 2 MB; E holds
32 basis states and 2 messages; advice 271 bytes; code under 1 MB; P (charged as preprocessing)
4.1 MB measured. No space is stored after its enumeration. Total under 2^23 bytes.

The cost model's memory also includes the advice. The runs that produced it report no memory,
but a computation of T primitives touches at most 32 T bytes. H1's time bound for steps (b)+(c)
is 2^59.70 primitives (P is far smaller), so those runs used at most 2^64.70 bytes. Declared:
memory_log2_bytes = 65. This uses no premise beyond H1; memory is not scored.

## 9. Declared heuristics (mirrored in claim.json)

- H1-advice-cost (score-critical). Statement: the connector and brute-force runs that produced
  the advice took at most 2 x (Tc + Tb) = 948.8 single-core hours, and one such core-second is at
  most 2^38 word-RAM primitives. Evidence: G2 (published single-core timings of the runs that
  produced the pair) and the hardware bound of Section 2 (5.0 GHz x 8 micro-operations per cycle
  x 6.9 primitives); calibration 2^34.7 primitives per second from the authors' Keccak rate.
  Limits: the CPU is unpublished; Tc and Tb are single reported runs; preliminary runs are
  covered only by the factor 2.
- H2-space-success (score-critical). Statement: for one attempt with fresh coins, conditioned on
  acceptance, E run on its space outputs a pair with probability at least s0 = 0.015.
  Evidence: in the pre-registered run (5.2), E output a pair in 21 of 768 accepted
  spaces, each with exactly its specified 2^32-pair window; the one-sided 99% Clopper-Pearson
  lower bound is 0.01548 >= s0. The samples are independent because every attempt has its own
  SHA-256-derived seed. Sampling premise: SHAKE-256-expanded coins from distinct seeds give the
  same q and s as fresh coins (a difference would distinguish SHAKE-256 from random); the
  acceptance rate agrees with os.urandom seeds (5.3). Limits: few spaces contain collisions, so
  the interval is wide and s0 is its lower end; all spaces share the published round-1
  difference, which is part of the fixed advice. Sensitivity: the claimed 0.40 needs only
  s >= 0.0020.
- H3-attempt-success (score-critical). Statement: one attempt with fresh coins is accepted with
  probability at least q0 = 0.02. Evidence: 992 of 32,768 in the pre-registered run (99.9% lower
  bound 2.74%); cross-checks 256 of 8,192 with os.urandom seeds, 490 of 14,600 in v4, and 8 of
  256 with organizer seeds; the homogeneity tests pass (5.2, 5.3). Sampling premise: as for H2.
  Limits: the margin is a factor of 1.37 against the 99.9% bound. The rate depends on the fixed
  advice: with a random beta1, our connector accepted 0 of 18,000 attempts.

## 10. Not claimed; credits

Not claimed: any improvement on the method of [GLL+20] beyond the byte-aligned (p = 8)
adaptation and the accounting. The time is a hard cap. The certificates show that the
construction works; they are not the claimed cost. Credits: [GLL+20] for the trail core, the
connector framework and the published pair; Dinur, Dunkelman, Shamir (FSE 2012) for the target
difference algorithm; Qiao, Song, Liu, Guo (EUROCRYPT 2017) for linearisation; Daemen, Van Assche
(FSE 2012) and KeccakTools for in-kernel trail cores. The public note of jagnani73's accepted
SHA-256 package 654cb3d2 taught us to charge advice at published run times with a margin, and to
use fresh coins, hard caps and organizer experiments; none of its constructions is reused.
hybridnoise's byte-aligned package on this track (ef4a0c66) uses its own beta1 search; none of
its code, data or certificates is used. baseline_improved is the required nominal reference ID,
not a claim of dominance.
