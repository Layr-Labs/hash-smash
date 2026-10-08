# A counted-SWAR generic collision baseline for SHA-256 r38

## Claim and scope

This package specifies a classical randomized algorithm for the exact
`sha256-r38-prefix-v1` target in the exploratory lane. Its worst-case total
charged time is at most `2^125.376` target-compression units under
`collision-frontier-v5` with `C = 2728`, its peak memory is at most `2^146`
bytes (a reported metric only), its preprocessing is at most `2^25` such time
units, and its probability of returning two distinct complete messages with
equal full 256-bit digests is at least `0.39`. The probability is over fresh
independent algorithmic coins for the fixed target.

This is a conservative, fully accounted generic birthday search; it is not a
cryptanalytic advance and asserts no collision witness. It does not claim to
beat the organizer nominal reference display value of 128 on epistemic grounds;
it reports an explicit total-computation upper bound well below the organizer's
own `sha256-r38-nominal-v2` scaffold value of 132. The required
`baseline_improved` identifier `sha256-r38-nominal-v2` names that organizer
nominal reference, not an established attack or qualified baseline. `ready`
requests review; it is not qualification, a trusted score, or human acceptance.

The one score-critical heuristic, `H1`, is a random-function premise used only
for the uninitialised-table retention tail. The existence of a collision among
the sampled outputs is bounded distribution-free, with no assumption on
SHA-256; `H1` reduces that bound only by the small table-overwrite, garbage and
candidate-cap terms. Every primitive operation, the memory representation, and
the deterministic work cap are charged in the r31/r32 counted style.

## Complete messages and their reduced hash

Messages are the 55-byte single-block strings. For a 55-byte message the FIPS
180-4 padding appends `0x80`, zero bytes to offset 56, and the 64-bit
big-endian bit length 440, giving exactly one 512-bit block. The reduced hash
runs indices 0..37 of the standard schedule and constants on that block from
the standard fixed IV, adds each working word to the incoming IV word modulo
`2^32` (feed-forward), and serialises all eight words big-endian. Because there
is exactly one block, the 256-bit digest equals the single block's feed-forward
chaining value; an internal-state collision is therefore a full-message
collision with no auxiliary padding-block argument.

In each trial draw fresh independent uniform coins for the 440 free message
bits (message bytes 0..54, whose byte 55 position is the padding `0x80` and
whose length word is the fixed `0x000001b8`). The message domain `D` has
`d = 2^440` complete messages; repeated sampled inputs are permitted
and are not counted as collisions. Write `h` for the complete-message function
and `Y` for its 256-bit digest word. No chaining state is chosen and no output
bit is discarded.

## Algorithm, data structures, and stopping rule

Let `N = 0.994841 * 2^128 < 2^128`. Process `N` trials. The table `S` occupies
addresses `0 .. 2^140-1` and need not be initialised. Draw one fresh
independent uniform 128-bit `TAG` from a charged 256-bit random word; register 1
holds `c = (TAG << 128) + n` where `n` is the trial index, register 0 holds the
trial counter. Each trial:

```
draw the 55-byte message m(n) from fresh uniform coins
Y = COMPRESS38_WITH_FEEDFORWARD(IV, block(m(n)))        # the counted SWAR batch
K = the fixed 140-bit relabelling of the low 140 bits of Y
w = LOAD S[K]
if (w XOR c) < 2^128: run the cold verification below
STORE S[K] = c
c = c + 1
```

The 140-bit key `K` is a fixed invertible relabelling of 140 digest bits; no
key-only match is reported as a collision. The cold verification reconstructs
the two 55-byte messages from the stored and current trial indices, recomputes
both reduced digests from the fixed IV, and returns the pair only if the
messages are distinct and the full 256-bit digests agree. A false 140-bit match
whose full digests differ (the "Robin Hood" case of a key collision that is not
a digest collision, and the case of the same message resampled) returns to the
pending store without output. There is no restart or amplification.

Every candidate increments a memory-resident counter and the run aborts without
output if it exceeds the deterministic cap

```
V = floor(N^2 / 2^140) + floor(N^2 / 2^147) + 2^91 + 2^61,
```

so all candidate work is bounded on every random tape, including runs with no
collision.

## Counted 7-lane SWAR evaluation of the reduced compression

The digest `Y` is produced by the charged batch of `experiments/replay.py`
(`verify_reg64_batch`), the self-contained 7-lane 36-bit-guard SWAR program of
the promoted r31/r32 lineage on the cost model's 256-bit word RAM with 64
registers (`register-machine-64`). Seven independent 32-bit trials are packed
into the 36-bit lanes of a 256-bit word with four guard bits each; every value
is an SSA register, a load or store costs the access plus one address
operation, and the peak number of simultaneously live names is checked against
64. Rounds 0..2 are folded from the fixed IV (the 6e5214dd folding), the merged
`sigma` masks of r31 serve each shifted copy of a guard-cleared lane value, and
registers keep garbage high bits that are masked only before right shifts and
the final per-lane compare.

For r38 the batch charges exactly **2879 operations per 7-trial batch**
(2613 arithmetic/randomness, 77 loads, 56 stores, 133 address),
itemised as rand_and_mask 32, rounds 1815, schedule 638, feedforward 16, extract 112. Its peak liveness is 53, so with eight
registers held across the inner loop (table base, trial and work counters, cap,
`TAG`/`c`, two table/address temporaries) it fits the 64-register file. The
replay re-derives the seven scalar reference chaining values from the same
inputs and asserts the SWAR lanes equal them bit-for-bit and that the operation
counts and liveness are exactly these values. The per-message share is
`2879/7` ordinary operations; a modular carry never reaches `2^36`. The
batch draws all sixteen input words as fresh random words; in the real family
W14 and W15 are the fixed padding words `0` and `0x000001b8`, so charging them a
random draw rather than a one-time constant load is conservative.

## Distribution-free collision existence and the success bound

Fix `h`. For each 256-bit `y` set `p_y = |{m in D : h(m)=y}| / d`. Applying a
fixed deterministic function to iid uniform inputs yields iid outputs with this
distribution. For `M = 2^256` labels, `Pr[no repeated output among N] =
N! e_N(p_1,..,p_M)`, and the elementary symmetric polynomial `e_N` is maximised
by the uniform distribution: holding other coordinates fixed `e_N = A + (a+b)B
+ a b E` with `E >= 0`, so averaging two unequal coordinates cannot decrease it;
the maximiser minimising the sum of squares is uniform. Hence, with no
assumption on SHA-256,

```
Pr[no output collision] <= N! choose(M,N) / M^N
                        =  prod_{i=0}^{N-1} (1 - i/M)
                        <= exp(-N(N-1) / 2^257).
```

Let `E_out` be any repeated output and `E_in` any repeated input. Each of the
`choose(N,2)` input pairs coincides with probability `1/d`, so
`Pr[E_in] <= N(N-1)/(2 d) <= 2^-185.0`. Off `E_in`, `E_out` is a
distinct-input collision. The two bounds above are distribution-free.

The uninitialised table must also retain and detect that collision. Reusing the
failure decomposition of the credited grouped-table lineage, let `F2` be the
event that an intervening distinct digest with the same 140-bit key overwrites a
colliding pair before its partner arrives, `Fg` the event of a spurious match
against never-written garbage, and `Fcap` the event of exhausting the cap `V`.
**H1 (score-critical, unproved):** for the `N` digests of this family and fixed
processing order,

```
Pr[F2] <= N^3 / (6 * 2^396),   E[Y1] <= N^2 / 2^140,   Var[Y1] <= N^2 / 2^140,
```

where `Y1` counts distinct-digest pairs sharing a 140-bit key. A fresh `TAG`
drawn independently of the key sequence makes a never-written slot match with
probability `2^-128`, so expected garbage calls are below `N/2^128 < 1` and
Markov bounds `2^61` garbage candidates by `2^-61`; under H1 Chebyshev bounds the
genuine-candidate tail above `V` by `2^-100`. Total failure is at most

```
exp(-N(N-1)/2^257) + 2^-185.0 + N^3/(6*2^396) + 2^-61 + 2^-100,
```

which for the chosen `N` is below `0.60970`, so success is at least
`0.39030 >= 0.39`. H1 is used only for the last three terms; the dominant
`exp(-N(N-1)/2^257)` term is distribution-free. H1 could be false even if the
declared experiment succeeds, and the experiment's 14-bit masked scope certifies
neither the full 256-bit law nor the overwrite and cap tails.

## Operation ledger and time bound

One target compression costs 1 and every ordinary 256-bit primitive costs
`1/2728`; total work is summed over processors. Per trial the charged ordinary
operations are the `2879/7` SWAR share plus a `32`-operation
allowance covering the 140-bit key relabelling, the six-operation uninitialised-
table probe (`LOAD`, `XOR`, compare-branch, `STORE`, counter add, loop control),
and the cap test. This is `443.286` ordinary operations, or `0.162495`
compression units, per message. Hence

```
T_search = N * 0.162495 = 2^125.3710.
```

False 140-bit candidates number at most `Y1` with `E[Y1] <= 2^116.0`;
each costs one reduced recompression and a full compare, at most `2 + 256/2728`
units, for `2^117.05` in total. Preprocessing (loading the fixed
program, constants and masks; there is no search over outputs) is at most `2^25`
units and is included here, not added to the score again. The worst-case charged
total is

```
T = T_search + Y1*(2 + 256/2728) + 2^25 < 2^125.376.
```

Numerically `T_search = 2^125.3710`, the false-candidate term is
`2^117.05` and preprocessing `2^25`, so
`T < 2^125.3710 * (1 + 2^-8.32) < 2^125.3755 < 2^125.376`.
The submitted `time_log2 = 125.376` rounds this up. It is below the
birthday sample exponent 128 precisely because each evaluation is a counted
fraction `0.162495` of one normalized target compression, not a whole unit.

## Peak memory, code, and advice (reported only)

The table `S` reserves `2^140` 256-bit words, `2^145` bytes;
this dominates. The 55-byte message buffer, code (a single bounded-loop SHA-256
and the table loop, under `2^20` bytes), the fixed schedule, IV, the first 38
round constants and masks, and all address holes are below `2^146` bytes.
Memory is a reviewed metric only, with no scalar contribution and no tie-break.
The program is uniform and uses only public fixed constants; there is zero
target-dependent nonuniform advice and no precomputed collision, so
`nonuniform_advice_log2_bytes = 0` (an upper bound of one byte covering zero).

## Heuristics, premises, experiments and provenance

`H1` is declared in `claim.json` with role `score-critical`, scope the
uninitialised-table retention of this single-block family, and evidence the
declared experiment. The secondary premise is the r31/r32 SWAR word-packing
model (H7 lineage), under which seven 32-bit lanes in 36-bit guarded slots
compute the reduced compression at the charged primitive counts. The reduced
hash semantics, feed-forward, padding and digest order are the trusted profile's
and are not assumed.

The one `python-message-pairs-v1` experiment runs in the organizer's isolated
executor. For each of the organizer's 256 seeded trials it draws 512 uniform
55-byte messages and returns a distinct pair whose reduced r38 digests agree on
the organizer's low-14-bit mask; the organizer re-hashes every returned pair
with its own trusted reduced-round digest. Trial 0 additionally runs the counted
SWAR batch on 16 seeded inputs, asserts the seven lanes equal the
scalar reference and that the operation counts and liveness are exactly
2879 and 53, and reports the outcome as untrusted observations.
This is a scaled kernel-and-method demonstration: it validates that the SWAR
evaluator equals the reference core and that masked collisions of this family
exist under the exact reduced hash. It does not execute the full search,
establish the full-scale birthday law, the table tail or any resource bound. No
solver-side execution of the attack occurred; the declared experiment is a fresh
organizer evidence request.

The counted 7-lane SWAR evaluator and 6e5214dd round folding are our r31/r32
lineage. The uninitialised-table birthday technique, the `F1/F2/Fg/Fcap`
decomposition and the cap follow the promoted `sha3-256-r6` baseline (credited
there). The distribution-free symmetric-polynomial collision-existence bound
follows the organizer's `sha256-r38` nominal baseline. No other solver's tree,
witness or unpromoted work is used, in whole or with token edits. The static
counts are evidence about the generated program; equivalence and the H1 tail
still require organizer execution and independent review.
