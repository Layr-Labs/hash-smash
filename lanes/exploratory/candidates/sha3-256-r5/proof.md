# Five-round SHA3-256 collisions: blind trail search, exact 2-round connector, brute force

## 1. Claim

Target `sha3-256-r5-prefix-v1`, exploratory lane, ordinary collisions, cost model
`collision-frontier-v5` (one 5-round Keccak-f[1600] permutation = 1 unit, every
other 256-bit word-RAM primitive = 1/1355 unit).

The algorithm below outputs two distinct 135-byte messages with equal 256-bit
digests with probability at least 0.5, using at most 2^42.91 units of total
computation (preprocessing included), at most 2^30.59 bytes of memory, and no
nonuniform advice. The scalar claimed is `time_log2 = 42.91`.

The attack follows the framework of Guo, Liao, Liu, Liu, Qiao and Song (Practical
collision attacks against round-reduced SHA-3, IACR ePrint 2019/147): a connector
that deterministically reaches the input difference of a 3-round differential
trail, followed by brute force over the connector's solution space. What is new
here, and what makes the construction cheap and fully accounted:

- The trail is re-derived inside the algorithm by an exhaustive blind search
  (Section 4) instead of being taken from the paper.
- The connecting stage is solved as one exact constraint program (Section 5).
  In the hold-out measurement of Section 5.6, 11 of 30 random choices
  succeed within 1.6e+12 retired instructions each (about a minute on one
  core). The paper reports 428.8 core-hours for its connecting stage.
- Everything works in the byte domain of the profile. The paper's own SHA3-256
  collision uses 1084-bit messages and is not a valid witness here (Section 11).

All costs are bounded in Section 9. Measured quantities come with their
measurement method. The two heuristic premises are stated in Section 8 and listed
in `claim.json` with their evidence. Eleven verified collision certificates produced
by this construction are included (Section 10). One of them comes from an
end-to-end run of exactly the claimed algorithm.

## 2. Exact target

Messages are byte strings. The algorithm only outputs messages of exactly 135
bytes. SHA3 padding appends the delimited suffix 0x06 and the final bit of
pad10*1. For a 135-byte message both fall in block byte 135, which becomes 0x86,
so the padded message is exactly one 136-byte block

    P(M) = M || 0x86.

Bit i of the block is bit (i mod 8) of byte floor(i/8) (Keccak bit order). The
state is 25 lanes A[x,y] of 64 bits, lane index x+5y, bit z of a lane being bit z
of its little-endian integer. The initial state is zero. The 17 block lanes are
XORed into lanes 0..16; the capacity lanes 17..24 stay zero. Then rounds
i = 0,1,2,3,4 of Keccak-f[1600] are applied, in this order:

    theta: C[x] = XOR_y A[x,y];  D[x] = C[x-1] XOR rot(C[x+1],1);  A[x,y] ^= D[x]
    rho, pi: B[y, 2x+3y] = rot(A[x,y], r[x,y])
    chi:   A[x,y] = B[x,y] XOR (NOT B[x+1,y] AND B[x+2,y])
    iota:  A[0,0] ^= RC[i]

with RC[0..4] = 0x1, 0x8082, 0x800000000000808a, 0x8000000080008000, 0x808b and
the standard rho offsets r[x,y] (rows y = 0..4, columns x = 0..4):

    0 1 62 28 27 / 36 44 6 55 20 / 3 10 43 25 39 / 41 45 15 21 8 / 18 2 61 56 14.

These are the first five rounds with the original first-round constants, which is
the profile's prefix convention, not Keccak-p's last-round convention. The digest
is the first 32 bytes of the resulting state, which are lanes 0..3 of plane y=0.
There is no feed-forward and no further permutation, since 32 < 136. Every hash in
this document is this function, with one permutation call per message. This is the
organizer's `verifier/keccak.py:sha3_256(m, rounds=5)`, and every certificate
checks against it.

A first-round input state x in the algorithm is the padded block P(M) placed in
the rate, with zero capacity. Exactly 520 state bits are pinned: the 512
capacity bits (value 0) and block byte 135 (value 0x86). The remaining 1080 bits
are the message bits. Conversely, every state with the pinned bits set this way
is P(M) for exactly one 135-byte message M.

## 3. Notation and the attack frame

L = pi o rho o theta is linear and invertible, and round i is iota_i o chi o L.
For a message pair, alpha_i is the XOR difference of the states entering round i
and beta_i = L(alpha_i) is the difference entering chi in round i. iota does not
change differences. chi acts independently on the 320 rows (y,z), 5 bits each. For
a row input difference d and output difference e, DDT(d,e) is the number of row
values v with chi(v) XOR chi(v XOR d) = e, and the weight is w(d,e) = 5 - log2 DDT(d,e).

**Fact 3.1.** For fixed (d,e) the solution set V(d,e) = {v : chi(v) XOR chi(v XOR d) = e}
is either empty or an affine subspace of GF(2)^5 of dimension 5 - w(d,e). The
reason is that chi(v) XOR chi(v XOR d) is an affine function of v for fixed d,
since chi has algebraic degree 2.

The attack uses a pair (M, M') with M' = M XOR Delta. Its differences evolve as:

- Rounds 0 and 1 (the connector): the 2-round connector of Section 5 outputs an
  affine set S of first-round states such that for every x in S the pair
  (x, x XOR alpha_0) has difference exactly alpha_2 after round 1 (Theorem 5.1).
- Rounds 2, 3, 4 (the trail): from alpha_2 the pair follows the trail
  beta_2 -> alpha_3 -> beta_3 -> alpha_4 -> beta_4 -> alpha_5 probabilistically.
  The digest condition is that alpha_5 vanishes on lanes 0..3 of plane 0.

The trail (Section 4) has beta_2 -> alpha_3 of weight w2 = 24 and beta_3 -> alpha_4
of weight 19. Summing over every alpha_4 compatible with beta_3, the exact
probability that the digest difference vanishes given alpha_3 is
P34 = 2^-13.219.

## 4. Phase A: blind trail search (deterministic, one-time)

The search follows the trail requirements of Guo et al. (Sect. 5.3 and App. C of
2019/147):
- alpha_3 and alpha_4 lie in the column-parity (CP) kernel;
- the trail starts from a light alpha_3, of Hamming weight "say 10" in the
  paper's words;
- the digest difference must vanish;
- the connector must be able to absorb the chi_1 conditions implied by alpha_2.

It is exhaustive over a stated finite space and uses no information about any
particular trail.

**A1 (enumeration).** Enumerate every nonzero state alpha_3 in the CP-kernel
with Hamming weight at most 10, up to rotation along z. Kernel means every column
(x,z) holds an even number of active bits, here 2 or 4. A depth-first generator
adds whole columns. It is complete for a structural reason: chi acts within a
slice, so a kernel alpha_4 compatible with beta_3 = L(alpha_3) = pi rho (alpha_3)
exists only if every active slice of beta_3 has at least two active rows. A slice
with a single active row produces an odd column after chi.

The generator therefore always extends the configuration with a column that puts
a bit into the smallest such "lonely" slice in a new row. Every column that could
do so is tried. Once no lonely slice remains, any further column is tried. This
reaches every valid configuration. Duplicates and rotations are removed by a
canonical form, the lexicographically least rotation. The run yields
7,945,960 rotation classes.

Each class is then tested exactly, slice by slice. The test asks whether outputs
can be chosen for the active rows of beta_3, each compatible by DDT, so that
alpha_4 is in the kernel and beta_4 = pi rho (alpha_4) has no active row in plane
y = 0. On the trail that last condition means no difference reaches the digest
lanes. 485 classes survive.

**A2 (connector feasibility).** For each survivor, CP-SAT decides whether some
beta_2 compatible with alpha_3 gives connector load w1 <= 140. Here
w1 = sum over active rows of alpha_2 = L^-1(beta_2) of min_d w(d, row).

The encoding is exact:
- gamma = rho^-1 pi^-1 (beta_2) and P is its column parity.
- alpha_2 = gamma XOR d, where d flips whole columns and satisfies the linear
  system (I + E) d = E P, with E(P)[x,z] = P[x-1,z] XOR P[x+1,z-1]. This is
  theta^-1 written in column form.
- Each row weight is a table lookup.

Results: 484 survivors are proved infeasible and exactly one is feasible.
For comparison, the minimum w1 per survivor, computed separately, is
127 for that one and at least 185 for every other. So any threshold
in [127, 184] yields the same unique output, and the choice of 140 is not
tuned to the answer.

**A3 (forward probability).** For the feasible core, P34 is computed exactly by
enumerating all 2^19 alpha_4 compatible with beta_3 and summing
P(beta_3 -> alpha_4) * P(digest difference 0 | beta_4 = L(alpha_4)) =
2^-13.219.

**Output.** A minimal-w1 beta_2 for that core gives the trail below. Nonzero
lanes are written as index:hex, the hex being the 64-bit lane integer:

    beta_2 = 0:0000000000000001 2:0000000000000004 5:0000000000000004 6:0000000000000004 7:0000000000000004 8:0000000000020000 10:2000000000000000 12:0000000000200000 15:2000000000000000 18:0000000000020000 20:0000000000200001 22:0000000000200000 24:0000000000000001
    beta_3 = 0:0000000000000001 2:0000000000000001 3:0000004000000000 7:0000000000000001 9:0000000000040000 11:0000000000000100 14:0000000000040000 20:0000000000000001 21:0000000000000100 23:0000004000000000
    beta_4 = 5:0000000010000004 6:0000004000000000 10:0000008000000000 11:0000000000000040 14:0000000000040000 16:0000001000000000 17:0000000000040000 19:0100000040000000 20:4000000000000000 22:0200000000000000 24:0000010000000400

with w1 = 127 (alpha_2 has 59 active rows), w2 = 24, w(beta_3) = 19, and no
active beta_4 row in plane 0. This is exactly Trail core No. 3 of Guo et al.,
with the same rotation and the same beta_2. A blind exhaustive search over the
paper's own criteria returns the paper's trail as the unique usable one, which
also explains why the paper used it for both SHA3-224 and SHA3-256.

## 5. Phase B: the 2-round connector (randomized)

Let alpha_2 = L^-1(beta_2).

**B1 (random beta_1).** For each of the 59 active rows of alpha_2, draw with fresh
independent coins one input difference of maximal DDT entry to that row's output
difference, uniformly among the maximizers. This gives beta_1, with weight
w1 = 127, and alpha_1 = L^-1(beta_1). Every such choice is a valid differential for
chi_1. The choice only affects whether the next step succeeds.

**B2 (model).** The unknowns are a choice per chi_0 row s = (y,z) of an option
(d_s, A_s), where:
- d_s is an input difference with DDT(d_s, alpha_1[s]) > 0, or d_s = 0 when
  alpha_1[s] = 0;
- A_s is a maximal affine subset of V(d_s, alpha_1[s]) (Fact 3.1) on which every
  output combination u . chi(v) required below is affine.

The required combinations come from the 127 chi_1 conditions. These are the
linear equations defining V(beta_1[t], alpha_2[t]) for each active chi_1 row t,
each a linear form in chi_1 inputs. Through L each becomes a linear form in chi_0
outputs, and each chi_0 row s contributes one mask u.

This is Guo et al.'s non-full linearization (their Sect. 4.2), applied to
exactly the combinations needed rather than to individual output bits.

**Difference constraints.** beta_0 = L(alpha_0) with alpha_0 zero on the 520
pinned bits (Section 2). In column form, with c the column parity of alpha_0 and
E as in A2:
- at the rho/pi image of each pinned bit, beta_0 = E(c);
- on each column, the free bits of beta_0 have parity c XOR (#free mod 2) E(c).

**Value constraints.** On the product of the A_s the whole value system is
linear, because every quantity entering a chi_1 condition is affine there:
- 520 pinned-bit equations Linv[k] . y = t_k, where y = L(x);
- y_s in A_s for every row s;
- the 127 chi_1 conditions.

A *relation* is a combination of pinned equations and chi_1 conditions that is
constant on every A_s. The system is consistent iff every relation has the right
constant, and each consistent independent relation adds one degree of freedom.

Two families of relations are structural and are modelled with a reward:
- 200 column pairs of pinned bits. Their sum passes theta unchanged and lands on
  one input bit of two chi_0 rows.
- The 127 single chi_1 conditions. Each touches 11 chi_0 output bits that are
  often constant on their sets.

Any other violated relation found after a solve becomes an exact
conditional-parity cut: "if every touched row keeps the touched mask constant,
the constants must sum to the right value". The model is then solved again.

**Objective.** The objective is DF_est = 1080 - 127 - sum_s (5 - dim A_s) + #relations,
which equals the realized degrees of freedom when the model is exact. Solving
stops once DF_est >= 45.

**B3 (realization).** The chosen options give a linear system over x. It is
solved by Gaussian elimination. Its solution set is S = x0 + span(B), with
DF = dim S, together with alpha_0 = L^-1(beta_0). An attempt succeeds iff the
system is consistent and DF >= 41. Otherwise a new attempt starts from B1
with fresh coins.

Each attempt runs as a child process with one solver thread, at most 30 solve
rounds and a 60 s wall-clock limit per solve. A watchdog reads the child's
hardware retired-instruction counter (`proc_pid_rusage`, `ri_instructions`) about
every 10 ms and kills the child once it exceeds the budget I_B = 1.60e+12
instructions. A killed attempt counts as a failure. At most K = 3 attempts are
made.

**Theorem 5.1.** For every x in S, the pair (x, x XOR alpha_0) consists of the
padded blocks of two distinct 135-byte messages and has state difference alpha_2
after round 1.

*Proof.* Both states satisfy the 520 pinned-bit equations: x by construction, and
x XOR alpha_0 because alpha_0 vanishes on pinned bits. So both are P(M) for
135-byte messages, distinct since alpha_0 != 0.

In round 0, y = L(x) has y_s in A_s, a subset of V(d_s, alpha_1[s]), for every row,
so chi_0 maps the input difference beta_0 to alpha_1 exactly. iota does not change
differences, so round 1 receives alpha_1 and beta_1 = L(alpha_1).

On S every chi_0 output combination used by a chi_1 condition is affine (choice of
A_s), so each chi_1 condition is a linear equation in x, and these equations hold
on S. They state exactly that every active chi_1 row input lies in
V(beta_1[t], alpha_2[t]). Hence the chi_1 output difference is alpha_2. []

Random sampling checks this on every space used (64 elements each, 0 misses),
and so does the C brute force, which re-checks alpha_2 after round 1 on one pair in
2^20. Over all runs in Section 8 that is 660,480 checks with 0 failures.

**B4 (measured connector statistics).** Section 5.6 holds the data.

### 5.6 Connector measurements

There were two batches with disjoint seeds. The hold-out batch was run only
after the budget had been fixed, so its success rate is not tuned on the data
that certifies it.

- **Batch 1** (9 attempts, seeds 43..51) ran
  without the budget, under `/usr/bin/time -l`. It was used only to choose I_B.
  - Outcomes: INFEASIBLE: 2, SUCCESS: 6, time-cap: 1.
  - Largest attempt: 1.762e+12 instructions.
- **Hold-out batch** (30 attempts with fresh seeds) ran under the exact
  algorithm: watchdog, budget I_B, and success criterion DF >= 41.
  - Outcomes: BUDGET: 12, INFEASIBLE: 7, SUCCESS: 11.
  - Realized DF of the successes: [48, 50, 50, 51, 51, 52, 52, 54, 54, 59, 60].
  - The largest watchdog overhead was 7.63e+08 instructions.

From the hold-out batch only, the Clopper-Pearson 95% lower bound on the
per-attempt success rate is r_L = 0.221. With K = 3 attempts, P(some
attempt succeeds) >= 1 - (1 - r_L)^K = 0.5274.

## 6. Phase C: brute force

Take the space S from the first successful attempt. If alpha_0 is in span(B),
drop a basis vector that it uses, so each unordered pair appears once. Keep
40 basis vectors. Enumerate x over x0 + span of those vectors in Gray-code order, one
basis XOR per step. Stop after N = 2^39.6 pairs. For each x, evaluate the 5-round
permutation on x and on x XOR alpha_0 and compare the 256 digest bits.

On equality, output M = x[0..134] and M' = (x XOR alpha_0)[0..134], after
recomputing both complete hashes from Section 2 and checking M != M'.

Any output is an ordinary collision of the exact target (Theorem 5.1 and the
final check). Nothing is free-start, truncated or compression-only.

## 7. Correctness of the output

By Theorem 5.1, any returned pair consists of distinct 135-byte messages under
the exact padding, rounds 0..4, zero IV and full 256-bit digest of the profile.
The final explicit recomputation ensures that a returned pair is a collision.

## 8. Success probability

The algorithm's coins are the beta_1 draws in B1. Phase A is deterministic.
Within an attempt, the outcome can also depend on solver timing, because of the
wall-clock limits. Each attempt is therefore treated as a randomized procedure
whose success rate is measured under exactly these limits (Section 5.6).

Success requires a successful connector attempt within K, and then at least one
colliding pair among the N enumerated pairs.

**Connector.** P(some attempt succeeds within K = 3) >= 0.5274, from the
hold-out success rate (heuristic H2).

**Brute force (heuristic H1).** For the pairs (x, x XOR alpha_0) with x in a
connector space, the events "this pair collides" have probability p each and
behave as independent trials. Here p is the product of the round-2 probability
2^-24 and P34.

The following table supports H1: every complete enumeration made for this
work, by C code that counts, per pair, the alpha_3 hits after round 2 and the
full digest collisions. Spaces D and E come from a variant where some round-2
conditions are made linear and absorbed into the space, so their round-2 weight
is 24 - k.

| Run | Space | Pairs | Round-2 weight | alpha_3 hits | expected | ratio | collisions |
|---|---|---|---|---|---|---|---|
| A | space from the published characteristic after a 2-bit repair | 2^36 | 24 | 4136 | 4096 | 1.0098 | 1 |
| B | same characteristic, second connector seed | 2^36 | 24 | 4134 | 4096 | 1.0093 | 0 |
| C | from-scratch characteristic (beta_1 seed 3), 38-dimensional subspace | 2^38 | 24 | 16226 | 16384 | 0.9904 | 2 |
| D | beta_1 seed 4, 8 round-2 conditions absorbed into the space | 2^32 | 16 | 65255 | 65536 | 0.9957 | 11 |
| E | beta_1 seed 4, 11 round-2 conditions absorbed into the space | 2^30 | 13 | 130620 | 131072 | 0.9966 | 8 |
| F | exact Phase B space (hold-out seed 100, early stop), 38-dimensional subspace: end-to-end trial of the claimed pipeline | 2^38 | 24 | 16265 | 16384 | 0.9927 | 1 |

Pooled over all runs:
- alpha_3 hits 236636 against 237568 expected, ratio 0.9961.
- 23 collisions among those alpha_3 hits, so P34 is estimated at
  9.720e-05 = 2^-13.329.
- The exact Garwood 95% interval is [2^-13.986, 2^-12.743]. It
  contains the exact Markov value 2^-13.219 of Section 3.

All collisions were verified with the organizer's function. The round-2 hit rate
matches its expected weight to within 1% in every space, including the absorbed
ones (pooled: 0.39%). That is consistent with the round-2
conditions acting as independent fair coins on these spaces.

**Conservative value.** Take the 95% lower bounds on both factors: the round-2
factor at 1.96 sigma below the pooled count, R2_L = 0.9921, and P34_L. Then

    p_L = 2^-24 * 0.9921 * 2^-13.986 = 2^-37.998.

With N = 2^39.6, the expected number of collisions is N p_L = 3.036.
Under the Poisson approximation,
P(brute force succeeds) >= 1 - exp(-3.036) = 0.9520.
The space has 2^(DF-1) >= 2^40 pairs, which is enough.

Overall: P(success) >= 0.5274 * 0.9520 = 0.5020 >= 0.5 = the claimed value.
K and N were chosen jointly to minimize the worst-case total of Section 9 subject
to this bound.
This is the algorithm's success probability, not confidence in the argument.

## 9. Cost in the word-RAM model

### 9.1 Accounting rules

1. Each evaluation of the selected 5-round permutation costs 1 unit (cost model).
2. Code written for this attack (trail generator, brute force) is charged by an
   explicit operation count. Each counted step has an explicit upper bound on
   256-bit word-RAM primitives, independent of compiler and CPU.
3. Black-box software (the CP-SAT solver and the Python driver) is charged
   through the hardware count of retired instructions of the process
   (`/usr/bin/time -l`, Apple M4 Pro), times CMAX = 1024 primitives per
   instruction.

**Why 1024 suffices (rule 3).** On ARM64, loads and stores move at most 512 bits:
at most 2 words, so 2 primitives. Integer ALU, shift and compare instructions,
branches and conditional selects are each at most 3 primitives. The primitive set
has no multiply, divide or floating point, so those are emulated:
- 64x64 multiply, schoolbook with 8-bit table lookups (64 lookup/shift/add
  steps): <= 256;
- 64-bit divide by restoring shift-subtract: <= 320;
- IEEE double add, multiply or FMA, by mantissa multiply plus align, normalize
  and round: <= 500;
- double divide or square root, by digit recurrence: <= 450;
- 128-bit SIMD instructions act on at most 2 double, 4 single or 16 byte lanes;
  each listed case stays <= 1024;
- CRC32: <= 256.

**Charged phases.** Memory traffic, hashing and the solver's search are all
included, because they are counted in retired instructions or in the explicit
per-step bounds. The only uncharged items are operating-system work and
page-table effects, which the abstract RAM does not model. System time was 1.0%
and 1.7% of user time in the two Phase A runs.

### 9.2 Phase A1: trail generator (algorithmic count)

The generator's counters for the complete run:
- 5.864e+09 search nodes, at <= 600 primitives each (lonely-slice scan
  over 64 slices plus loop control);
- 1.078e+10 candidate trials, at <= 40;
- 2.364e+10 bit insertions or removals, at <= 25 each (3 table lookups,
  3 counter updates);
- 4.224e+09 canonical-form rotations, at <= 300 each (10 index
  updates, insertion sort of 10, compare);
- 6.600e+07 canonicalized configurations, at <= 200 each for
  hashing and lookup in a 2^26-entry table at load <= 0.12;
- 8.874e+06 forward row scans, at <= 500;
- 3.561e+07 forward combinations, at <= 30;
- 2^24 primitives to initialize the table.

Total: A1 <= 5.826e+12 primitives = 2^32.00 units. As a cross-check the
hardware count for the same run is 5.724e+12 instructions, matching the
algorithmic bound to within 1.8%. The run took 306 CPU-seconds.

### 9.3 Phase A2+A3: screen (rule 3)

One process covers all 485 survivors (single solver thread) and the
exact P34 of the feasible one. It retired 3.454e+12 instructions:
A2+A3 <= 3.454e+12 * 1024 / 1355 = 2^41.25 units.

### 9.4 Phase B: connector (rule 3)

Per attempt, the child retires at most I_B plus the instructions executed
between the last poll and the kill. The polling interval is nominally 10 ms but
can stretch under scheduler load, so a margin of 5% of I_B is charged
(8.0e+10 instructions). At <= 4.5 GHz x 10 instructions/cycle that covers
gaps of up to 1.8 s. Measured overshoot at the last poll
before a kill: max 1.26e+08 over 12 killed attempts. The watchdog's own count is at most 7.63e+08.
B <= K * (I_B + 8.0e+10 + 7.63e+08) * 1024 / 1355
  = 3 * 1.681e+12 * 1024 / 1355 = 2^41.79 units.

### 9.5 Phase C: brute force (rules 1 and 2)

Per pair:
- 2 permutation calls;
- at most 256 other primitives: a Gray-code index from a byte table (<= 20); x
  XOR basis vector over the 7 words of the 1600-bit state (load, XOR and store:
  21); forming x XOR alpha_0 (21); the digest compare, which is word 0 (4); and
  call and loop overhead (<= 50).

For N = 2^39.6 pairs plus the final 2-message check:
C <= 2^39.6 * (2 + 256/1355) + 2 + 4096/1355 = 2^40.73 units.

### 9.6 Total

| Phase | Units |
|---|---|
| A1 trail generator | 2^32.00 |
| A2+A3 trail screen | 2^41.25 |
| B connector (K attempts, worst case) | 2^41.79 |
| C brute force | 2^40.73 |
| **Total** | **2^42.91** |

So `time_log2 = 42.91` (rounded up). Phase A (`preprocessing_log2 =
41.25`) is included in the total. This is a worst-case bound for the
stated algorithm, not an expected cost and not a cost conditional on lucky
trials. Phase B is charged for all K attempts and Phase C for all N pairs.

## 10. Evidence

**Certificates.** `certificates/manifest.json` lists eleven collision witnesses
for this exact target, each a pair of 135-byte messages verified with
`sha3_256(m, rounds=5)`. None of them collides at 6 rounds.
- One (exact-pipeline-holdout100-11) comes from run F: the space of a hold-out
  Phase B attempt produced by the exact claimed algorithm, enumerated as in
  Phase C.
- Two (scratch-seed3-*) come from the from-scratch space of run C. Its trail is
  the output of Phase A; its beta_1 is a random draw; its connector is Phase B
  without early stopping.
- Eight come from runs D and E.

These certificates show the construction works. They do not establish its
probability, which rests on Section 8.

**Measurements.** The tables in Sections 5.6 and 8 and the counters in Section 9
are the complete measurement record. No run was dropped. Every enumeration
listed was run to completion, and every collision found is counted.

## 11. Relation to the published attack and limitations

**The published witness.** Guo et al.'s SHA3-256 pair (their Table 17) is a
5-round collision of this permutation. Its block byte 135 is 0xEE, though: it
fixes only 4 padding bits and its messages are 1084 bits long. No byte string
pads to that block, so it is not a witness for this profile.

**The published characteristic.** Their characteristic forces block bit 1083
to 1 through its chi_0 conditions, while byte 135 = 0x86 has that bit 0, so it
cannot be reused here. The construction above derives a new first-round
characteristic (beta_1, beta_0) for each attempt.

**Limitations:**
- H1 and H2 are empirical. H1 is supported by 23 collisions and 236636 round-2
  hits across 6 spaces. H2 is supported by 30 hold-out attempts.
- The CP-SAT cost is charged through a hardware instruction count times a
  worst-case emulation factor. That is conservative, but not an analytic
  operation count of the solver's algorithm.
- The trail space of Phase A (Hamming weight <= 10, kernel alpha_3 and alpha_4,
  no digest-plane activity) follows the paper's documented criteria. A wider
  space could contain cheaper trails. This affects only optimality, not validity.
