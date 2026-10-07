# Certified five-round SHA3-256 collisions: blind trail search, byte-aligned 2-round connector, 3-round trail

This package claims an ordinary-collision algorithm for `sha3-256-r5-prefix-v1` with total charged
time at most 2^44.6 target-permutation units under `collision-frontier-v5`, peak memory at most
2^31 bytes, and success probability 1. The algorithm is a fixed deterministic program. It was
executed in full, and its output, two colliding pairs of distinct 135-byte messages, is in
`certificates/` as two `hash-collision-witness-v2` certificates that the organizer verifier checks.
The time bound charges every CPU-second spent on producing the pairs: the trail search, all
connector and brute-force runs including aborted and unproductive ones, development and diagnostic
runs, and replay and verification. That work is measured as CPU time and converted to word-RAM
primitives with an explicit ceiling (Section 7), and a factor-2.2 margin is added.

The construction follows Guo, Liao, Liu, Liu, Qiao and Song, "Practical Collision Attacks against
Round-Reduced SHA-3", Journal of Cryptology 33 (2020) 228-270, IACR ePrint 2019/147 (GLL+20): a
2-round connector for rounds 0-1 and a 3-round differential for rounds 2-4. Three things are new
here:
- the trail core is re-derived by a blind, capped search using only the paper's published
  thresholds, rather than copied;
- the connector is re-engineered for byte-aligned messages (8 fixed padding bits instead of 4),
  where the paper's procedure, as written, fails (Section 5.2);
- real byte-aligned collisions were produced.

This package supersedes our earlier heuristic package for this track (time_log2 56.35, no
certificate). Its literal connector Step 1 does not work as written (Section 5.2).

## 1. Exact target

H is `verifier/keccak.py:sha3_256(data, 5)`: the full SHA3-256 sponge (rate 1088, capacity 512,
all-zero initial state, domain suffix 0x06, pad10*1) with prefix rounds 0..4 of Keccak-f[1600] on
every absorbed block. The digest is the first 32 bytes of the state. Lane index x+5y, little-endian
lanes; state bit (x,y,z) is bit z of lane x+5y. A 135-byte message pads to the single block
m || 0x86, so absorbed bits 1080..1087 are 0,1,1,0,0,0,0,1 (LSB first) and bits 1088..1599 are 0:
c+p = 520 fixed bits, 1080 free bits. Each round is R = iota o chi o pi o rho o theta. L = pi o rho
o theta is GF(2)-linear and invertible. Following GLL+20: alpha_i is the difference entering round
i, beta_i = L(alpha_i) the difference entering chi of round i, and each 5-bit row of a chi input is
one S-box. DDT is the 32x32 S-box difference table. The weight of a chi transition is
w = 5 - log2 DDT per active row. An ordinary collision is a pair of distinct byte strings with equal
256-bit digests.

## 2. Certificates (the output of the executed program)

| id | M1 (hex, 135 bytes) / M2 | digest (5 rounds) |
| --- | --- | --- |
| collision-a | 5c3ddb2364c4fff44cf1d31facc9ec6f0f9d19a5dff5d2bd857cf04e210f470e8b8b9591118f1e2c62116aca2329d9152f44db357af47f0aa4db373a514e3ac851812b4df7565abe619c3027967ea35276dfbf45acaec92fe0ff1e73f1d5e8df36da11cc42af086e8f16ac3513db781795b1a462b6f93711b567a0c7bb6814b4ff1d413328f5e7 / 0cfd64f03b85490a41917ba506870503519e518f02afcf6408323ea8aa71143b2639d668f6249bfdcb2384963dc4eafd0004a81a22e0fd00de3f80c5e6b4845e1b28eab52ee2a99c3eb0bd4ada8c5b4d691707910552729c5595d219e852b3493c407572a099c182b9b8059acab7ff394d0cc744be55fc3f0ba7366ad33a478cf1c6ec12969e87 | 830bcb0d018bd9555849f1d04b0921d709a6529d7ef6caab9b5bd632d5ece797 |
| collision-b | d79fa5b1bcbb4ecadd6a556efff67c5e48c13d50c4e3011264d32ba17f4c4f94c65cddf86ca295950f5749dfb79bfdc68a8ada3df18a1b03d4c09db259b9011589da660d7f30bdeddda41062a5fbd8a77465ac11ad48338666d15f02f111994674d6b07e44aeaae9e6b2a1ad453c87c7dc86b0f23e1ce31d88603044ce5bda1f48a1db25bb2e78 / 911baaa0b6562c36d6220aa2949bd811834696c097de18a082dc85a84085d0d94c2f40585c11200ec747e91abc7f156e8c01e233aa85dbf922b6f1b96fda6ecd0018c7fa2818f3acadc9f491b2312427daed984cc10e477099f5e2cfa3b4c1bb51477ec22e0fb4c347f6720362cb302e5f9d9df5f9ff1dc68fa4868266c7e9ce5056f426a52a16 | 11f6251f376488ce7b2f8607fe71a1887f2fb16c010d3c6a9276ac0706825259 |

Each pair has the message difference Delta = alpha0 of its connector space (570 and 542 differing
bits). Both pairs collide under `sha3_256(m, 5)`, and their full 24-round SHA3-256 digests differ.
The checker reports `certificates_verified: 2`. The correctness of the output therefore does not
depend on any argument in this document; Sections 3-6 describe the program that produced it, and
Section 7 charges its cost.

## 3. The program (overview)

The program P is fixed and deterministic. Its only randomness is xoshiro256** expanded from fixed
seeds written in its text, so it has no algorithmic coins.

1. Trail search (Section 4). Enumerate trail cores (beta2, beta3) with the procedure and thresholds
   of GLL+20 App. C.2 and select the core minimizing w1. The output is the core used below.
2. Connector + brute force, run A (Section 5, 6): seed 101, streams 0..11, wall cap 7200 s, stop at
   the first verified collision (this run produced collision-b).
3. Connector + brute force, run B: seed 202, streams 0..8, wall cap 600 s (this run produced
   collision-a).
4. Output both verified pairs.

Steps 2 and 3 are listed in the order they were executed. Both are charged in full, including
run A's whole execution: it ran until it was stopped after 10,276 s, past its cap, while one
thread finished a 2^43-message space. Step 3 is not needed for a collision once step 2 has
succeeded, but it was run and is charged. Section 9 gives the expected cost of fresh runs as
context; the claim does not rely on it.

## 4. Step 1: blind trail-core search (GLL+20 Sect. 5.3, App. C.2)

The search uses no knowledge of the paper's trail cores. Its inputs are the paper's published
thresholds: KeccakTools 3-round core weight at most 60 ("aMaxWeight 60"), light beta3 ("low
Hamming weight, say 10"), forward cap C1 <= 2^36, backward cap C2 <= 2^35, #AS(alpha2) <= 110 and
w2 + w3 + w4^d <= 55 (requirement (3)).

Stage A (light beta3). The output is every beta3, up to translation in z, such that
alpha3 = L^-1(beta3) lies in the column-parity kernel, some alpha4 compatible with beta3 lies in the
kernel, HW(alpha3) <= 10, and the KeccakTools 3-round core weight
KW = w_rev(alpha3) + w(beta3) + min over in-kernel alpha4 of w(L(alpha4)) is at most 60.
Kernel at alpha3 is a per-column parity condition. Kernel at alpha4 is a per-slice condition: in
each slice, the chi outputs of the active rows of beta3 must be choosable to XOR to zero. The
generator is a depth-first search started from each of the 25 points of slice 0 (every core has a
translate with a point in slice 0). While some alpha3 column is odd, or some beta3 slice cannot
reach XOR zero, it branches on adding one point to the first such column or slice. Its prunes are
sound: points + max(#odd columns, #infeasible slices) <= 10, and
2 rows(alpha3) + 2 rows(beta3) + 4 <= 60, a lower bound on KW. KW is computed exactly at every
feasible node, and results are kept up to z-rotation. Validation against KeccakTools'
`TrailCoreInKernelAtC`:
- at weight 40, the generator returns exactly the KeccakTools cores whose exact weight is <= 40;
- at weight 60, every core that KeccakTools produced before stalling is in its output.
The search stops at the first feasible set on each path, so a core that strictly contains a smaller
feasible core (for example, a union of two separate structures) is not generated. Completeness of
the enumeration is not needed for this claim: the search is charged for what it executed, and its
output is the core used.
KeccakTools itself would need about 7e3 core-hours at weight 60, extrapolated from measured runs at
weights 36 (151 s) and 40 (1,134 s); those runs are charged as exploratory work (Section 7).

Stage A output: 3,486 cores (GLL+20 report "more than 3000"), 1.96e8 search nodes, 152.7 CPU-s.
For stages B and C the cores are sorted by KW, then by their canonical lanes as text.

Stage B (forward, App. C.2 step 2). For each core with C1 = prod |compatible outputs| <= 2^36,
enumerate every alpha4 compatible with beta3 and compute beta4 = L(alpha4). A digest collision is
possible from beta4 iff every active row of beta4 in plane y = 0 can reach output 0x10 (output bits
0..3 zero). Keep beta3 iff some beta4 allows it. The search also computes
P_fwd = sum over alpha4 of P(beta3 -> alpha4) * prod DDT(row, 0x10)/32, the multi-trail
probability of a digest collision given alpha3 (that is, 2^-(w3 + w4^d)).

Stage C (backward, App. C.2 step 3). For each kept core with C2 <= 2^35, enumerate every beta2
compatible with alpha3 (each active row of alpha3 takes every din with DDT(din, dout) > 0) and
compute alpha2 = L^-1(beta2). For #AS(alpha2) <= 110, record w1 (the minimum reverse weight of
alpha2) and w2 = w(beta2 -> alpha3).

Selection: among candidates satisfying requirement (3), take the minimum w1, breaking ties by
#AS(alpha2). w1 is the number of linear conditions the connector must impose on round 1 (Eq. 7
below). The paper's requirement (2), TDF > w1 + w2 + w3 + w4^d, rejects every SHA3-256 core,
including the one GLL+20 used (124 < 170), so the selection is by minimum w1, as GLL+20 effectively
did.

Results:

| quantity | value |
| --- | --- |
| cores from stage A (KW <= 60, HW(alpha3) <= 10) | 3,486 |
| forward-compatible | 956 |
| with some beta2 giving #AS(alpha2) <= 110 | 48 (all satisfy requirement (3)) |
| selected (rank 1934 of 3,486 in the fixed order) | #AS(alpha2) = 59, w1 = 127, w2 = 24, w3 + w4^d = 13.22 |
| runner-up | #AS(alpha2) = 81, w1 = 187 |

The selected core is GLL+20 trail core No. 3 (their Tables 5 and 9), bit for bit, in the same
z-orientation. Display: rows y = 0..4, columns x = 0..4, 16 hex digits per lane, most significant
digit first, '-' = 0.

    beta2 (10 active rows, w2 = 24)
    ---------------1|----------------|---------------4|----------------|----------------
    ---------------4|---------------4|---------------4|-----------2----|----------------
    2---------------|----------------|----------2-----|----------------|----------------
    2---------------|----------------|----------------|-----------2----|----------------
    ----------2----1|----------------|----------2-----|----------------|---------------1
    beta3 (9 active rows, w3 = 19)
    ---------------1|----------------|---------------1|------4---------|----------------
    ----------------|----------------|---------------1|----------------|-----------4----
    ----------------|-------------1--|----------------|----------------|-----------4----
    ----------------|----------------|----------------|----------------|----------------
    ---------------1|-------------1--|----------------|------4---------|----------------

The runner-up is useless for this connector: it imposes 187 round-1 conditions on about 136 free
variables. Measured cost of the search: Section 7.

The multi-trail value 13.22 for rounds 3-4 was also confirmed by simulation: random state pairs with
difference alpha3 collide on the digest after rounds 3-4 with probability 2^-13.22 (3,512 of
33,554,432).

## 5. Steps 2-3: the byte-aligned 2-round connector

### 5.1 Setting
The unknown is x = L(S0), the chi input of round 0 for the first message. The connector outputs an
affine space of x such that every message M in it satisfies R2(M) + R2(M + Delta) = alpha2 =
L^-1(beta2) deterministically. Here Delta = alpha0 = L^-1(beta0), y = chi(x), and
z = L(y + RC0) is the chi input of round 1. All systems are incremental, fully row-reduced GF(2)
systems over 1600 variables plus a right-hand side.

### 5.2 Why the literal GLL+20 procedure fails for p = 8
GLL+20 build E_M from Eq. 2 (the value conditions V(din, dout) of every active round-0 S-box) and
Eq. 3 (the fixed initial bits), after choosing beta0 by the target difference algorithm, which they
say "always" finds a compatible beta0. We implemented that procedure and validated the code on the
published 1084-bit pair. With 520 fixed bits, the Eq. 2 + Eq. 3 system was inconsistent on every
try. The cause is structural:
- the span of Eq. 3 contains 200 two-bit relations x_(j,3) = x_(j',4) + c (196 for p = 4). They
  come from capacity columns with two fixed bits, after rho and pi.
- these relations link bit 3 of one S-box to bit 4 of another, forming 120 paths through planes
  P2 -> P0 -> P3 -> P1 (-> P4) (where a path continues into P4).
- V(din, dout) almost always pins or relates bits 3 and 4, so each path imposes value conditions.
  The paper's own published pair has 58 such dependencies among its Eq. 2 + Eq. 3 rows, all
  consistent.
- meanwhile the difference system E_Delta is fully determined after about 57 of about 300 active
  S-boxes, so later S-boxes cannot be chosen to satisfy their paths.
We also found that #AS(alpha1) must be pushed well below its typical value of about 310 to leave
enough degrees of freedom. The connector below is GLL+20's design, with these points fixed.

### 5.3 Connector algorithm (as executed)
Setup: L and L^-1 as matrices; the DDT and the V(din, dout) affine subspaces; all 2451 affine
subspaces of GF(2)^5 with their linear outputs. For every subspace W and output mask U, a table
cand[W][U] lists the largest affine subspaces of W on which all outputs in U are affine. This is
generic non-full linearization; it contains the choices of the paper's Observations 3 and 4. The
200 link relations are computed by reducing unit vectors against Eq. 3.

1a. beta1. For each of the 59 active rows of alpha2, the options are the din maximizing
    DDT(din, dout). Start from a uniform choice, then hill-climb: pick a random row, move to the din
    minimizing #AS(alpha1 = L^-1(beta1)), with uniform tie-breaks. Stop at #AS(alpha1) <= 268, or
    restart after 177 non-improving moves. The B rows are the 127 V(din, dout) equations on z,
    pulled back to y through L, with L(RC0) folded into the right-hand side. U_j is the y-support
    of those rows on S-box j.
1b. Difference phase, path-aware. E_Delta starts with: alpha0 = 0 on the 520 fixed bits, and
    beta0 = 0 on rows where alpha1 = 0. Paths are processed in random order. For each path, a
    depth-first search chooses, for every active S-box, a 2-dimensional affine subset (or a
    1-dimensional one while an E_Delta budget remains) of {din : DDT(din, dout) > 0} that meets
    the current implied hull. Candidates are ordered by the mean weight of their members. The
    search requires every din combination allowed by the link difference equalities to be
    value-consistent along the path, checked by a dynamic program over the link bits. A fallback
    pass requires only existence. Search budgets: 4000 nodes per try, 8 tries.
    Value phase. E_M starts with Eq. 3. S-boxes are processed in increasing index. Each takes a din
    in the hull of E_Delta whose V(din, dout) meets the hull of E_M, preferring maximal DDT; its 5
    difference bits go into E_Delta and its V equations (Eq. 2) into E_M. Any failure returns to 1a.
1d. Linearization (Algs. 1-3). For each S-box with U_j != 0, compute the exact implied hull W of the
    current system on its 5 bits. If the marked outputs are affine on W, nothing is added; this is
    an exact preProcess that also captures implications created during the pass. Otherwise add a
    uniformly chosen member of cand[W][U_j]; this can never be inconsistent, because the subspace
    lies in the projection W. Then substitute the resulting affine expressions of the marked y bits
    into the 127 B rows (Eq. 7). A row reducing to 0 = 1 is a failure. Per (beta1, beta0):
    64 attempts; if any succeeds, continue up to 16,384 attempts in total.
1e. Every success with DF >= 14 becomes a space. x0 and a basis come from the row-reduced system,
    mapped through L^-1 to a message M0, basis vectors w_k (17 lanes) and Delta. Every space is
    checked on 64 random members for the fixed bits and for R2(M) + R2(M + Delta) = alpha2.
    Delta always lies in the span of the w_k.

Parameters (both runs): p = 8, #AS(alpha1) <= 268, 64 / 16384 attempts, minimum DF 14, max-DDT din,
budget margin 10. Each stream is seeded by xoshiro256** from SEED * 1000 + stream.

### 5.4 Measured connector behaviour (p = 8)
Typical spaces have DF 17-22. DF >= 33 occurred (DF 43 in run A). Run B made 244,948 linearization
attempts in total (60,219 consistent). Every one of the roughly 265,000 emitted spaces passed the
64-member check.

## 6. Brute force and verification
Each space is enumerated in Gray-code order (2^DF messages; a halved mode that visits each pair once
exists but was not used in the charged runs). Per message: rounds 0-1 and L of round 2, unrolled,
then a check that each of the 10 active rows of beta2 lies in V(din, dout) of the beta2 -> alpha3
transition. Survivors (rate 2^-24) run both messages through all 5 rounds and compare the first 256
bits; a match is written out with its digest. Measured survivor counts match 2^-24 (run B: 4,592
observed, 4,527 expected).

## 7. Cost accounting under collision-frontier-v5

### 7.1 Measured CPU time (all work, upper bounds)
All runs used one Apple M4 Pro (8 performance + 4 efficiency cores). CPU time is rusage user + sys
where recorded. Where rusage was lost, the bound is (number of threads) x (wall time).

| item | CPU seconds (upper bound) | basis |
| --- | ---: | --- |
| run A (seed 101, 12 workers + 1 monitor thread, stopped at 10,276 s) | 133,588 | 13 threads x 10,276 s wall |
| run B (seed 202, 9 workers) | 3,126 | rusage |
| replay of run B's stream 3 (reproduces collision-a) | 246 | rusage |
| brute-force replays on collision-a's spaces | 342 | rusage |
| connector development and diagnostics (p = 4/8 tests, analyses, simulations) | 14,400 | estimate, 4 h (H2) |
| trail search, executed procedure: stage A | 153 | rusage |
| trail search: stages B/C, part 2 (2,131 cores) | 20,442 | rusage |
| trail search: stages B/C, part 1 (1,355 cores, 3 threads, rusage lost) | 22,401 | 3 threads x 7,467 s wall |
| trail search, exploratory (KeccakTools runs, generator development) | 14,400 | itemized about 10,500 s; charged 4 h (H2) |
| verification of both pairs (organizer Python) | 360 | estimate, 0.1 h |
| total | 209,458 | = 58.2 core-hours |

Charged budget: 128 core-hours, a factor 2.2 above the 58.2 core-hour total. The margin covers any
error in the two estimated items, and in the stopped-run bounds, by a wide factor.

### 7.2 From CPU time to v5 units (ceiling H1)
Under v5, a five-round permutation costs 1 unit and any other 256-bit word-RAM primitive (load,
store, add, bitwise, shift/rotate, compare, branch, random word) costs 1/1355 unit.
H1: one CPU core-hour on this machine executes at most 2^48 primitives. Evidence: the hardware
counters of the three instrumented runs, which cover every code path we used (connector + brute
force, trail stage A, trail stages B/C):

| run | instructions retired | CPU s | instructions per CPU-s | IPC |
| --- | ---: | ---: | ---: | ---: |
| replay (connector + BF) | 3.431e12 | 245.6 | 1.40e10 | 5.3 |
| trail stage A | 1.855e12 | 152.7 | 1.21e10 | 4.5 |
| trail stages B/C, part 2 | 2.828e14 | 20,441.9 | 1.38e10 | 5.1 |

An AArch64 instruction performs at most 3 v5 primitives: an integer or 64/128-bit vector operation
counts as at most one 256-bit primitive; a three-input vector op (EOR3/BCAX) counts as 2; a
load/store pair with address writeback counts as 2. The highest rate, 1.40e10 x 3 = 4.2e10
primitives per CPU-second, gives 1.5e14 = 2^47.1 per core-hour, 1.9x below 2^48. The
uninstrumented runs execute the same binaries on the same workloads. The efficiency cores in run A
are slower, which only lowers their rate. Permutation evaluations performed inside this CPU time are
charged through their primitives. Separately, every full five-round evaluation is also charged
1 unit: at most 2 per filter survivor plus verification, in total < 2^18 calls.

Total: T <= 128 core-hours x 2^48 / 1355 + 2^18 = 2^(7 + 48 - 10.404) + 2^18
= 2^44.596 + 2^18 < 2^44.6 units. The claim is time_log2 = 44.6.
Preprocessing (the trail search, executed and exploratory, about 16 core-hours, x2) is about 2^42.6
units, included in T.

### 7.3 Memory and advice
- peak resident memory: trail stage A hash table 868 MB; KeccakTools runs at most 182 MB plus a
  44 MB cache; connector run A under 100 MB across 12 threads.
- saved connector spaces (386 MB on disk) are diagnostic output, not needed by the program.
- declared memory_log2_bytes = 31 (2 GiB), an upper bound including code.
- nonuniform advice: the program text (two seeds, caps, thresholds, the round constants), under
  64 KB; declared 16. The trail core is not advice: it is computed in step 1, and that computation
  is charged.

## 8. Success probability
P is deterministic. It uses no random coins; its PRNG is part of the program text. It was executed,
and both output pairs are certified. Its success probability is therefore 1, and its charged time
is the measured cost of that execution, bounded above in Section 7. The cost model's note that a
seeded experiment does not establish ideal random coins concerns claims about randomized
algorithms. This claim does not rest on any probabilistic premise about fresh coins; the output
pair is checked directly by the verifier.

## 9. Context: expected cost for fresh seeds (not claimed)
Run B succeeded at 403.6 s wall, using 3,126 CPU-s for 9 streams to its cap; its stream 3 alone
regenerates collision-a in 246 CPU-s. Run A needed about 24-34 core-hours for its single
collision. Over both runs, about 47,500 distinct pairs reached the exact alpha3 after round 2, and
2 distinct collisions resulted. That is fewer than the about 4.9 expected from the measured
2^-13.22, which happens with probability about 13% under a Poisson model.
- run A alone had none until its last space;
- survivors matched random pairs in every statistic we tested.
The shortfall is unexplained. A fresh run of this program would cost, on our evidence, 1-35
core-hours of connector work plus the 12 core-hour trail search. The claim does not depend on this.

## 10. Relation to GLL+20 and to our earlier package
- GLL+20 Table 17 prints a five-round SHA3-256 collision of 1084-bit messages (byte 135 = 0xEE).
  We verified it with the organizer permutation (digest 65017c2e8b6040b4...). It lies outside this
  target's byte-string domain and is not used.
- Trail core No. 3 is recovered by step 1, not copied; its rank in the search order is reported.
- The connector differs from GLL+20 in four places, each needed for p = 8 (Section 5.2):
  - path-aware difference subsets;
  - the interleaved value phase;
  - the #AS(alpha1) hill-climb;
  - exact implied-hull preProcess with generic minimal linearizing subspaces.
- Our earlier pending package for this track (time_log2 56.35, heuristic, no certificate) followed
  the paper's procedure literally, and its Step 1 does not work as written. This package replaces it.
- GLL+20's own connector took 428.8 core-hours (p = 4, DF 37). Ours produced p = 8 spaces of DF 28-43
  in minutes of CPU, because of the changes above.

## 11. Declared heuristics
H1 (score-critical): the ceiling of 2^48 primitives per core-hour for the uninstrumented 90% of the
charged CPU time. Evidence: Section 7.2, the hardware counters, and the instruction-to-primitive
bound.
H2 (supporting): the estimated items of Section 7.1 (development 4 h, trail exploratory 4 h,
verification 0.1 h). They are 14% of the total, and the 2.2x budget would absorb them even if
they were 9 times larger.
No heuristic affects correctness or success: the output is verified.
