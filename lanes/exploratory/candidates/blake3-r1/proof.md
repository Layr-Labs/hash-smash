# SAT second-preimage collision for 1-round BLAKE3 (blake3-r1)

The scalar below is `time_log2` under `collision-frontier-v5`.
Memory is a separately reported bound. This package targets
blake3-r1-prefix-v1 with a deterministic construction and a
machine-checked collision witness. The claimed scalar is 37.

Two heuristic premises are declared in claim.json. H-SAT-TIME
(score-critical) bounds the one-time SAT preprocessing in v5 units from
one observed Z3 run plus an explicit machine-operation cap. H-SAT-MEM
(supporting) bounds the preprocessing peak memory from the observed peak
plus headroom. The witness correctness and success probability use no
heuristic: they rest on the organizer-recomputed certificate and the
organizer-executed witness experiment.

## 1. Exact complete hash

Each message is exactly 64 bytes (512 bits, below 2^64). Decode into
sixteen little-endian 32-bit words w[0..15]. Unkeyed BLAKE3-256 with 1
prefix round in every compression. On 64-byte messages there is one chunk,
one full block, no parent, exactly one compression with
CHUNK_START | CHUNK_END | ROOT = 11, true block length 64, chunk counter 0,
root-output counter 0.

IV is 6a09e667 bb67ae85 3c6ef372 a54ff53a 510e527f 9b05688c 1f83d9ab
5be0cd19. State v[0..7]=IV, v[8..11]=IV[0..3], v[12..15]=(0,0,64,11).
G(a,b,c,d,x,y): v[a]=v[a]+v[b]+x; v[d]=ROR(v[d] XOR v[a],16);
v[c]=v[c]+v[d]; v[b]=ROR(v[b] XOR v[c],12); v[a]=v[a]+v[b]+y;
v[d]=ROR(v[d] XOR v[a],8); v[c]=v[c]+v[d]; v[b]=ROR(v[b] XOR v[c],7), all
adds modulo 2^32. One round calls the eight G in column-then-diagonal order
with the message words exactly as in verifier/blake3.py; no later rounds.
Output o[i]=v[i] XOR v[i+8], o[i+8]=v[i+8] XOR IV[i] for i=0..7; digest is
LE4(o[0])..LE4(o[7]). This is the ordinary complete-message hash, not a
free-start, compression-only, truncated, or different-round object. The
profile permits longer messages; this algorithm generates only 64-byte
messages, so the one-root-compression description covers every hash it
evaluates.

## 2. Algorithm

Preprocessing (once): fix target T = blake3-r1 of 64 zero bytes. Encode one
1-round compression as 32-bit bitvectors (Z3 5.1.0): 16 variable message
words m[0..15], same IV, same v[12..15], same G order, same feed-forward and
packing as Section 1 (cross-checked on a random input against
verifier/blake3.py: exact match). Constrain all eight digest words equal to
T and OR(m[i] != 0) for distinctness. Z3 reports SAT; the model bytes B are
stored. Observed wall: 2.6 s single-core, peak resident under 1 GiB.

Online (deterministic): output fixed A = 64 zero bytes and B from
certificates/msg_a.bin and certificates/msg_b.bin. Recompute both complete
blake3-r1 hashes from the all-zero state, check A != B bytewise and both
digests equal on all 256 bits and equal manifest expected_digest
e9174a9264d9445b72d2a0015ca2283f497c0ecb5d9ee4b2020d61c608c9ba88.
Return the pair if verified, else fail. One batch, no restart, at most two
hash evaluations plus comparisons and output.

## 3. Correctness of the returned collision

The encoding replicates the reference: identical constants, state layout, G
sequence, feed-forward, and packing, confirmed by the random-input match.
The solver model therefore satisfies the digest equation, and the
independent Python recomputation plus the organizer certificate check
confirm it. A != B holds by the OR-constraint and is rechecked. Both
messages are 64 bytes, hence in the profile domain. The final check
establishes distinct messages with equal full 256-bit digests: an ordinary
collision. Certificates carry the witness; experiment
fixed-collision-witness replays the same pair under organizer execution.

## 4. Success probability 1.0

The online algorithm is deterministic with no random coins: it always
outputs the same stored pair and the verification branch always succeeds
(organizer certificate check passed). Hence algorithmic success probability
is 1.0, above required 0.39. This is algorithmic success, not reviewer
confidence, and uses no sampling or heuristic.

## 5. Fully charged RAM cost in v5 units (single consistent ledger)

One selected compression costs one unit; every other 256-bit word operation
costs 1/222. This ledger charges preprocessing, message handling, both
hashes, verification, code, and retained state. For a strict upper bound,
word operations are charged at full price (the 1/222 discount is foregone).

Preprocessing cap: observed wall 2.6 s is below 2^2 s. Any modern single
CPU retires below 2^34 primitive operations per second (16.4e9/s cap above
a 4 GHz core at few ops per cycle, with OS/Python overhead absorbed).
Hence the fixed Z3 instance costs below 2^2 * 2^34 = 2^36 full-price units.
This conversion (wall time via generic CPU cap) is heuristic H-SAT-TIME;
the cap is deliberately loose (no C discount, 4 s ceiling over 2.6 s
observed, 16.4e9/s ceiling over typical ~3-4e9/s throughput).

Online cap: 2 target compressions plus message packing, comparisons,
addressing, and output: below 2^17 full-price units (under 131072 word
operations; the loop bodies need only hundreds).

Fixed storage (code, IV constants, driver text, verification scratch)
below 2^20 bytes, initialized once; included in the preprocessing cap.

Total: T <= 2^36 + 2^17 + 2 < 2^37, because 2^36 + 2^17 + 2 < 2 * 2^36.
Submitted time_log2 = 37. Preprocessing alone is <= 2^36 < 2^37, so
preprocessing_log2 = 37 is also a valid upper bound. Both bounds use the
same ledger; no second accounting is introduced.

Peak memory: preprocessing resident below 2^30 bytes observed (< 1 GiB);
messages, code, and scratch below 2^20 bytes; total below 2^31. Submitted
memory_log2_bytes = 32 (4 GiB ceiling, more than 2x headroom). Memory is
metric-only under v5. The observed-peak extrapolation is heuristic
H-SAT-MEM.

Claim fields: time_log2=37 bounds total charged time; memory_log2_bytes=32
bounds peak bytes; preprocessing_log2=37 bounds the one-time SAT search
(included in T, not omitted); nonuniform_advice_log2_bytes=0: no external
advice exists; A and B are outputs of the charged preprocessing retained in
charged memory, and the manifest is verification evidence, not advice.
success_probability=1.0 proved in Section 4. No data_log2 is claimed.

## 6. Heuristic disclosures

H-SAT-TIME (score-critical): the fixed Z3 5.1.0 instance for target T
terminates within 2^36 full-price v5 units. Scope: exact 16-word bitvector
encoding of Section 1, fixed zero target, stated solver version, modern
CPU. Evidence: Sections 2 and 5 plus experiment fixed-collision-witness
(which confirms the witness, not the runtime). Extrapolation: one 2.6 s
observation generalized by the 2^2 s ceiling and 2^34 ops/s machine cap
with the C discount foregone. Limitations: solver-version and
machine-dependent; wall-to-ops conversion is a generic cap, not an analytic
solver bound; reruns may vary but stay orders of magnitude inside the cap.

H-SAT-MEM (supporting): the same instance peaks within 2^32 bytes. Scope
as above. Evidence: Sections 2 and 5. Extrapolation: sub-1-GiB observed
peak with 4x headroom. Limitations: machine and allocator dependent;
memory does not affect the scalar.

## 7. Evidence

Certificates: manifest entry blake3-r1-collision-01, organizer-verified
(distinct 64-byte messages, recomputed digests equal expected). Experiment
fixed-collision-witness replays the pair under organizer execution with a
full-collision event check. No full-scale statistical trial is needed for a
deterministic witness; the runtime heuristic is disclosed in Section 6 with
its limits.

## 8. Reference and readiness

baseline_improved blake3-r1-nominal-v2 names the organizer nominal display
128: not an established attack, baseline, or bound. This candidate's bound
37 sits below 128 under the same v5 model; no Pareto claim beyond the
scalar is made. submission_state=ready means complete for review, not
qualified, scored, or promoted. Exploratory lane only.
