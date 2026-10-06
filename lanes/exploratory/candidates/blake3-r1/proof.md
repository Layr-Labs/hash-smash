# Meet-in-the-middle second preimage for 1-round BLAKE3 (blake3-r1)

The scalar below is `time_log2` under `collision-frontier-v5`.
Memory is a separately reported bound. This package targets
blake3-r1-prefix-v1 with a classical meet-in-the-middle second-preimage
construction. The claimed scalar is 80.

One heuristic premise is declared in claim.json. H-MITM-UNIFORM
(score-critical) states that the two 128-bit digest-half key maps behave
uniformly over uniform 64-bit half inputs. It rests on offline
full-distinctness counts plus two organizer-executed experiments. Every
operation count below is a syntactic bound over displayed fixed-bound
loops; no wall-clock observation and no SAT solver enters the ledger.

## 1. Exact complete hash and the half split

Each message is exactly 64 bytes (512 bits, below 2^64), decoded into
sixteen little-endian 32-bit words w[0..15]. Unkeyed BLAKE3-256 with 1
prefix round in every compression. On 64-byte messages there is one chunk,
one full block, no parent, exactly one compression with
CHUNK_START | CHUNK_END | ROOT = 11, true block length 64, chunk counter 0,
root-output counter 0, standard IV 6a09e667 bb67ae85 3c6ef372 a54ff53a
510e527f 9b05688c 1f83d9ab 5be0cd19, and state
v[0..7]=IV, v[8..11]=IV[0..3], v[12..15]=(0,0,64,11).

One round applies eight G calls in fixed order. The first four (column
round) consume w[0..7]; the last four (diagonal round) consume w[8..15]:
G(0,5,10,15,w8,w9) writes v[0],v[5],v[10],v[15];
G(1,6,11,12,w10,w11) writes v[1],v[6],v[11],v[12];
G(2,7,8,13,w12,w13) writes v[2],v[7],v[8],v[13];
G(3,4,9,14,w14,w15) writes v[3],v[4],v[9],v[14].
Digest word o[i]=v[i] XOR v[i+8] for i=0..7. Hence, with w[0..7] fixed so
the column-round output is constant, digest half H1=(o0,o2,o5,o7) depends
only on (w8,w9,w12,w13), and digest half H2=(o1,o3,o4,o6) depends only on
(w10,w11,w14,w15). The write sets are disjoint, verifiable against
verifier/blake3.py, and confirmed by randomized flip tests (flipping one
half's words leaves the other half's digest words unchanged). This is the
ordinary complete-message hash with a restricted 64-byte domain.

## 2. Algorithm

Target T = blake3-r1 of 64 zero bytes, fixed. The algorithm draws its
coins as stated below; at most four attempts, stopping at the first
success. Probability space: the attempt prefix C (eight 32-bit words)
drawn fresh uniform per attempt from the RAM model's random-word
primitive; the target T and the function are fixed. Within one attempt,
with C fixed, all table and probe sets below are EXHAUSTIVE over their
64-bit half-input domains (no sampling, no replacement draws), so no
duplicate-draw statistics enter. Per attempt:

1. Draw fresh uniform C for w[0..7]. The column-round state S is then
   fixed for this attempt.
2. Half H1: enumerate ALL 2^64 pairs (w8,w9); for each compute the
   diagonal G pair and store key LA=(v0,v5,v10,v15) with payload (w8,w9)
   in a table; sort the table by key. Then enumerate ALL 2^64 pairs
   (w12,w13); for each compute (v2,v7,v8,v13) and probe lookup key
   K=(T0^v8,T5^v13,T2^v2,T7^v7); keep the first probe that hits a stored
   LA. A hit yields (w8,w9,w12,w13) with H1 equal to T's half.
3. Half H2: same structure exhaustively over all (w10,w11) tabled with
   key LB=(v1,v6,v11,v12) and all (w14,w15) probes with lookup key
   (T1^v9,T6^v14,T3^v3,T4^v4) in the same component order.
4. Assemble M* from this attempt's C and the four recovered half words.
   Recompute the complete blake3-r1 digest from the standard IV, check
   M* != zeros and all 256 digest bits equal T. Return (zeros, M*) on
   success; otherwise draw a fresh C and continue, or fail after four
   attempts (32 fresh prefix coins followed by exhaustive joins).

One batch of at most four attempts over fresh coins, no restart beyond
the fixed attempt loop, at most one final verification per attempt. Prior exploratory measurements
(single-bit screening, cascade statistics) guided the choice of this
split; they perform no work in the claimed construction and need no
charging. All executed work is counted in Section 5.

## 3. Correctness of any returned pair

Table keys are exact 128-bit G-output words; the join condition is
precisely v0^v8=T0, v2^v10=T2, v5^v13=T5, v7^v15=T7 for H1 (and the mirror
set for H2), i.e. half-digest equality with T. Both halves matching gives
full 256-bit digest equality. Messages are 64 bytes, hence in the profile
domain; distinctness is explicitly rechecked, and the final recomputation
uses the complete hash of Section 1. Any returned pair is an ordinary
collision (a second preimage of T). The certificate entry
blake3-r1-collision-01 carries one such pair, found during preliminary
research with a SAT solver and retained here solely as an existence
witness; the scored construction is the MITM of Section 2, whose analysis
does not depend on how the witness was found.

## 4. Success probability at least 0.39 over fresh prefix coins

Fix nothing: C is drawn fresh uniform per attempt (eight 32-bit coins),
and the analysis below is over those coins for the fixed target and
function. Within one attempt, table and probe sets are exhaustive, so no
sampling duplicates exist at all: the left table holds every 2^64
half-input's key (distinct up to key-space collisions of expectation
below one, negligible against the margin), and all 2^64 probes are tried.
Under H-MITM-UNIFORM, for coin-random C the 2^64 table keys and the 2^64
probe keys behave as uniform draws over the 128-bit key space, giving
expected hits E = 2^64 * 2^64 / 2^128 = 1 per half. The hit count is
Binomial(2^64, ~2^-64); P[half succeeds] = 1-(1-2^-64)^(2^64) >
1-1/e-2^-64 > 0.63, using (1-1/n)^n < 1/e. The two halves run over
disjoint message and state words with S fixed by the same C, so their
success events are treated as independent (structural disjointness of
Section 1); P[attempt succeeds] > 0.63^2 = 0.397. Retries over fresh C
values can only add probability: P[overall] >= P[first attempt] > 0.39,
with no cross-attempt independence needed. The submitted
success_probability is 0.39, a floor over the algorithm's own fresh coins
given the uniformity premise. This number is algorithmic success, not
reviewer confidence.

## 5. Fully charged RAM cost in v5 units (single consistent ledger)

One selected compression costs one unit; every other 256-bit word
operation costs 1/222. The construction evaluates only G fragments, never
a full compression, so all units below come from word operations at
1/222. Caps below count displayed instructions at full price first, then
apply the single division by 222 once.

Per half per attempt, with N=2^64 exhaustive iterations (counter-driven,
no sampling; the only coins per attempt are the eight prefix words, eight
random-word primitives at 1/222, negligible and included):
- Left table: N iterations, each two G evaluations (cap 2^8
  word-ops per G: 8 additions, 8 XORs, 8 rotations, loads, stores, and
  address arithmetic) plus key packing and table store (cap 2^6):
  N * 2^10 = 2^74 word-ops at full price.
- Sort of N entries: at most N * 64 comparisons and moves, cap 2^5
  word-ops each: 2^64 * 2^6 * 2^5 = 2^75 word-ops.
- Right probes: N iterations, each two G evaluations
  plus one hash-bucket probe (cap 2^8): N * 2^10 = 2^74 word-ops.
- Per half below 2^74 + 2^75 + 2^74 < 2^76 word-ops. Two halves below
  2^77. Four attempts below 2^79. Final verifications below 2^20.
  Total word-ops W < 2^79 + 2^20 < 2^80.
- Charged units U = W / 222 < 2^80 / 128 = 2^73, using 222 > 128.
  Submitted time_log2 = 80 and preprocessing_log2 = 80 are both loose
  caps over this one ledger (actual total below 2^73 units); their
  equality is shared headroom, not an equation. Table construction is the
  dominant phase and is included, not omitted.

Peak memory: one table at a time holds N entries of 16-byte key plus
8-byte payload, capped at 32 bytes per entry with allocator slack:
2^64 * 2^5 = 2^69 bytes. Code, constants, G scratch, and output add
below 2^20 bytes. Total below 2^69 + 2^20 < 2^70. Submitted
memory_log2_bytes = 72 (4x headroom). Memory is metric-only under v5.

Claim fields: time_log2=80 bounds total charged time; memory_log2_bytes=72
bounds peak bytes; preprocessing_log2=80 bounds the table-building phases
(included in the total, not omitted); nonuniform_advice_log2_bytes=0: no
external advice exists; the recovered pair is algorithm output found by
the counted search, and the manifest is verification evidence, not advice.
success_probability=0.39 proved in Section 4 given the premise of
Section 6. No data_log2 is claimed.

## 6. Heuristic disclosure

H-MITM-UNIFORM (score-critical): over the algorithm's fresh uniform
prefix coins C, the exhaustive H1 table keys and probe keys behave as
uniform draws over the 128-bit key space (marginally uniform per key
with pairwise match rate 2^-128 across the disjoint table/probe input
sets), and likewise for H2, so the Section 4 coin-probability occupancy
analysis holds. Scope: exact G-fragment maps of Section 1 indexed by
coin-random C. Evidence: offline multi-C full-distinctness counts
(64/64 random prefixes with 4096/4096 distinct keys on both halves, plus
65536/65536 over 2^16 samples at fixed C) in proof lines below, plus
organizer experiment half-uniformity (256 trials drawing a random C each
then 512 seeded samples reporting distinct counts, the same C-coin
distribution as the algorithm) and truncated-differential-demo (live
last-round diffusion signal). Extrapolation: sampled distinctness plus
ARX avalanche generalize to full-domain uniformity across random C;
cross-half independence follows from the disjoint variable sets of
Section 1. Limitations: uniformity is measured, not proved; a hidden
structural bias correlated across C could lower hit rates. The property
concerns the fixed hash function under coin-distributed prefixes and is
machine-independent; no timing, solver, or hardware premise is used.

## 7. Evidence

Certificates: manifest entry blake3-r1-collision-01, organizer-verified
(distinct 64-byte messages, recomputed digests equal expected); provenance
disclosed in Section 3. Experiment half-uniformity replays the witness
(full-collision event) and reports seeded distinctness statistics for both
halves. Experiment truncated-differential-demo emits seeded word-9
MSB-difference pairs against a full-digest mask with offline rate 0.4993,
confirming last-round diffusion under organizer execution. Offline counts:
multi-C half-key distinctness 4096/4096 per half on all 64/64 random
prefixes (seed 31337), 65536/65536 per half over 2^16 samples at fixed C
(seed 2026); cascade rates 0.4993/0.2508/0.1255/0.0625 over 2^18 samples
(seed 555); split-independence flip tests passed. No full-scale 2^64
execution is asserted or needed for the analytic ledger.

## 8. Reference and readiness

baseline_improved blake3-r1-nominal-v2 names the organizer nominal display
128: not an established attack, baseline, or bound. This candidate's bound
80 sits below 128 and below the promoted best 149 under the same v5 model;
no Pareto claim beyond the scalar is made. submission_state=ready means
complete for review, not qualified, scored, or promoted. Exploratory lane
only.
