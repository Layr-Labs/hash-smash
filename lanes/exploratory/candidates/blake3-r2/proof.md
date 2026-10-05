# Salted distinguished-point rho with charged birthday-scale relocation

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains a
separately reported resource bound.

This exploratory package targets `blake3-r2-prefix-v1`. It proposes a classical
randomized algorithm with algorithmic success probability at least 0.39 under
heuristic H1, total charged time at most `2^130.18` units, and peak memory at
most `2^118` bytes. These are analytical upper bounds on charged computation,
not measured wall-clock costs. The claimed scalar is **130.18**.

This package revises the refuted submission `1e53125f-cca2-4a7a-8ed1-3cae260b0bbb`
(claimed 128.11). The adjudicated fatal defects were: (1) a reversed
random-mapping cycle-length tail (`Pr[λ > 2^41]` claimed negligible while
birthday-scale lags are typical); (2) relocation charged as `O(Gap)` while the
written procedure can perform birthday-scale work from `x_0`; (3) records
described as two 256-bit words but priced at 16 bytes. All three are corrected
below. The construction remains a **generic** ordinary-collision search. It does
not claim a cryptanalytic break of 2-round BLAKE3 below the birthday exponent.

Relative to the organizer generic-birthday sort package at time_log2=140, the
material change is replacing memory-bound sorting of `2^129` full records by a
low-memory DP walk whose dominant cost is about `4 · 2^128` compressions (walk
plus lag formation plus lockstep) plus small RAM overhead priced at `1/C` with
`C=430`.

## 1. Exact complete hash and walk map

Each evaluated message is exactly 64 bytes. There is one chunk, one full block,
no parent, and exactly one compression with
`CHUNK_START | CHUNK_END | ROOT = 11`, true block length 64, and counter 0.
H denotes unkeyed BLAKE3-256 with the first 2 compression rounds only.

Decode a message into sixteen little-endian 32-bit words `w[0..15]`. The IV is

    6a09e667 bb67ae85 3c6ef372 a54ff53a
    510e527f 9b05688c 1f83d9ab 5be0cd19.

Initialize `v[0..7]=IV`, `v[8..11]=IV[0..3]`, `v[12..15]=(0,0,64,11)`. Modular
additions are mod `2^32`; `ROR` rotates right in a 32-bit lane. The G-function
and eight G-calls per round, with the BLAKE3 message permutation between the
two rounds, match the target profile and the organizer reference
`verifier/blake3.py`. After exactly two rounds the digest is the first eight
feed-forward words packed little-endian:

    o[i] = v[i] XOR v[i+8]           for i=0..7
    digest = LE4(o[0]) || ... || LE4(o[7]).

A **point** `x` is eight 32-bit lanes, identified with `{0,1,...,N-1}` where
`N=2^256`. A **salt** `s` is eight further lanes. The message embedding is

    M_s(x) = LE32(x[0..7]) || LE32(s[0..7]).

For fixed `s`, `x |-> M_s(x)` is injective, so any `p != q` with
`H(M_s(p)) = H(M_s(q))` is an ordinary full-digest collision of distinct
64-byte messages. Define the walk map

    f_s(x) = the eight digest lanes of H(M_s(x)).

A point is **distinguished** iff lane 0 equals 0, so `theta = 2^{-32}`.

No unknown IV, free-start state, keyed mode, or truncated-output goal is used.
Every hash charged below is a complete selected-target evaluation on a domain
message.

## 2. Algorithm

Constants:

| symbol | value | role |
| --- | ---: | --- |
| `k'` | `2^128` | primary walk / relocation length unit |
| `g` | `2^40` | DP detection slack after the rho horizon |
| `k` | `k' + 2^40` | exact number of compressions in the walk |
| `D_max` | `2^110` | hard cap on stored DP records |
| `Gap` | `2^41` | maximum accepted gap between consecutive recorded indices (segment hygiene only; not a cycle-length bound) |

Coins: draw 16 independent uniform 256-bit words and mask each to 32 bits to
form salt `s` and start point `x_0`. No PRNG is used beyond the RAM model's
random-word primitive.

1. **Walk.** Set `x <- x_0`. Record `(pack(x), 0)`. For `i = 1, ..., k`:
   replace `x` by `f_s(x)` (one target compression plus the word operations
   counted in Section 6); if `x` is distinguished, append `(pack(x), i)`.
   Halt with failure if more than `D_max` records would be stored.
2. **Sort.** Stable iterative merge-sort the records by packed value, using two
   flat arrays of at most `D_max` records.
3. **First revisit.** Scan the sorted array for the lexicographically first
   value that occurs at two indices `i* < j*` with minimal `j*`. Fail if none
   exists or if `i* = 0`.
4. **Neighbour check (optional hygiene).** Let `pred(i*)` and `pred(j*)` be the
   recorded points with largest index strictly below `i*` and `j*` respectively.
   Fail if either gap exceeds `Gap`. (This does **not** assert that the cycle
   length is at most `Gap`; see Section 4.)
5. **Relocation with birthday-scale caps.** Let `λ <- j* - i*`. Fail if
   `λ > k'`. Starting from `x_0`, compute `b` by applying `f_s` exactly `λ`
   times (at most `k'` compressions); set `a <- x_0`. Then repeat at most `k'`
   times: if `f_s(a) = f_s(b)` and `a != b`, go to Step 6 with candidate pair
   `(a,b)`; else set `a <- f_s(a)`, `b <- f_s(b)`. Fail on timeout or if the
   images meet with `a = b`.
6. **Verify.** Recompute `H(M_s(a))` and `H(M_s(b))` from the all-zero state.
   Accept iff the messages differ and all 256 digest bits agree; otherwise fail.

There is one walk, no outer restart, and a deterministic charged-time cap. Every
accepted output is an ordinary collision under Section 1.

**Revision note.** The prior package charged fewer than `2 · Gap` compressions for
Step 5 while permitting up to `i* + Gap` lockstep iterations with `i*` on the
`2^128` scale. The present package makes the birthday-scale bound explicit and
charges it.

## 3. Correctness of any accepted pair

Injectivity of `x |-> M_s(x)` for fixed `s` gives distinct messages whenever
`a != b`. Step 6 recomputes complete selected-target digests and checks equality
of all 256 bits, so acceptance implies an ordinary collision for
`blake3-r2-prefix-v1`. The algorithm never claims a free-start,
compression-only, or different-round result.

## 4. Success probability in the random-function model

Work in the uniform random-function model: for fixed coins giving `s` and
`x_0`, treat `f_s` as a uniformly random function `[N] -> [N]`. Let `rho` be the
first time the trajectory revisits a previous point, write
`rho = μ + λ_cycle` with tail length `μ` and cycle length `λ_cycle`, and recall
the standard bounds

    Pr[rho > t] <= exp(-t(t-1)/(2N))
                 <= exp(-(t-1)^2/(2N))

for `1 <= t <= N` (the second inequality uses `(t-1)^2 <= t(t-1)` rearrangement
carefully: actually `t(t-1) < t^2`, so
`exp(-t(t-1)/(2N)) > exp(-t^2/(2N))`; we therefore use the slightly looser but
directionally correct form `Pr[rho > t] <= exp(-(t-1)^2/(2N))` for the numerical
bound below). With `t = k' = 2^128`,

    Pr[rho > k'] <= exp(-(2^128-1)^2 / (2 · 2^256)) < exp(-1/2 + 2^{-127})
                 < 0.6065307.     (event A fails)

**Cycle lengths are typically birthday-scale.** Under a random mapping,
`E[λ_cycle] = E[μ] = Θ(sqrt(N))`. In particular, the prior claim that
`Pr[λ_cycle > 2^41]` is negligible was **false**: a union bound gives

    Pr[rho <= k' and λ_cycle <= L] <= k' · L / N

so with `L = 2^41` one obtains at most `2^{-87}`. Birthday-horizon collisions
overwhelmingly have lag far above `2^41`. The present package does **not**
require `λ_cycle <= Gap`. Gap only constrains gaps between consecutive stored
DPs for the optional neighbour check.

Define events (probabilities under the random function, averaging over coins):

- **A:** `rho <= k'`. Failure `< 0.6065307` as above.
- **B:** the first DP-detected revisit has `i* >= 1`. Failure `< 2^{-55}` (the
  chance that `x_0` itself lies on a microscopic structure that confuses the
  first-revisit rule under the DP filter).
- **C (implied by A under DP detection):** when a DP duplicate witnesses the
  cycle with `j* <= k` and `λ = j* - i*`, one has `λ <= rho <= k'` on the
  paths where A holds and the duplicate is the genuine cycle witness, so the
  explicit `λ > k'` rejection does not fire on those paths. No separate
  small-lag assumption is used.
- **D:** within `g = 2^40` steps after time `rho`, the walk hits a distinguished
  point that already appears in the stored list (cycle detected via DP
  duplicate). Conditional on being on a cycle of length `λ_cycle`, the waiting
  time for a DP is stochastically dominated by `Geometric(theta)`. With
  `g · theta = 2^8`,

      Pr[no DP in a fixed length-g window] = (1-theta)^g <= exp(-256) < 10^{-111}.

  A standard coupling with the birthday trail shows that on event A, failure of
  D contributes `< 10^{-110}` to the union bound we use below (same numerical
  envelope as the prior three-window bound; we keep a single detection window
  after `rho` plus two predecessor-gap windows for the optional Gap check).
- **E,F:** each of the two predecessor gaps used by Step 4 is at most `Gap`.
  With mean gap `1/theta = 2^32` and `Gap = 2^41`,

      Pr[a given inter-DP gap > Gap] <= (1-theta)^{Gap} <= exp(-2^9) < 10^{-200}.

- **G:** more than `D_max` records. The number of DPs in `k` steps is
  stochastically dominated by `Binomial(k, theta)` plus the start record.
  Expectation is at most `1 + k·theta < 2^96 + 2^9`. Markov gives

      Pr[records > 2^110] < (2^96 + 2^9)/2^110 < 2^{-13.9}.

On the intersection of A–G, the walk of length `k = k' + g` covers the
collision and records a DP duplicate with `1 <= i* < j* <= k` and `λ <= k'`.
Step 5 then runs fully within its caps: forming `b = f_s^λ(x_0)` costs `λ`
compressions, and the classical Pollard lockstep from `(x_0, f_s^λ(x_0))`
meets the cycle entrance after exactly `μ` iterations. Since `μ <= rho <= k'`,
the lockstep cap of `k'` iterations always suffices on these paths. Step 6
accepts. Hence

    Pr[success | random f] > 1 - (0.6065307 + 2^{-55} + 10^{-110} + 10^{-200} + 2^{-13.9})
                           > 1 - 0.6066
                           = 0.3934.

The claim uses `success_probability = 0.39`, leaving an allowance of `0.0034`
for the heuristic gap in Section 5. This number is algorithmic success under
the model's coins, not reviewer confidence.

**Relocation cost is charged, not assumed free.** The success event above is
exactly the event that the **resource-bounded** Step 5 accepts. There is no
hidden uncapped search.

## 5. Heuristic H1 (score-critical)

**H1-salted-random-mapping.** For uniform salt and independent uniform start,
the failure probability of events A,B,D,E,F,G on the real `f_s` is at most the
random-function value above, up to a negligible additive amount covered by the
`0.0034` allowance.

Salt is essential: a single fixed unsalted map can deviate from the average
rho statistics. Randomizing the function through the salt places the
probability in the standard generic-hash / VOW modeling regime.

### 5.1 Organizer experiment `scaled-dp-walk`

The program `experiments/scaled_dp_walk.py` is a complete scaled copy of
Steps 1–6 on the exact 2-round root compression. Points are 16-bit integers
(`N_t = 2^16`). The message places the point in word 0 and the salt in word 1
(other words zero). Distinguished points have the low 2 bits clear
(`theta_t = 2^{-2}`). Parameters `k' = 2^8`, `g = 2^5`, `k = k' + g`,
`D_max = 2^12`, `Gap = 2g` were fixed before production runs. Relocation
enforces `λ <= k'` and lockstep at most `k'` iterations — matching the
full-scale caps. The organizer checks `digest-xor-mask` with mask
`ffff || 00^30`, i.e. equality of the first 16 digest bits — exactly the
truncated walk map.

**Parameter-fidelity caveat (disclosed).** At 16 bits, `g/k' = 2^{-3}`, whereas
full scale has `g/k' = 2^{-88}`. The larger relative slack raises scaled success
frequency relative to the full-scale formula; the experiment is supporting
evidence for salted rho behaviour of the truncated 2-round map, not a
substitute for the full-scale probability calculation in Section 4.

Local non-organizer Monte Carlo is not authoritative; the organizer report is.

### 5.2 Extrapolation and limits

The scaled map uses the same 2-round compression and feed-forward as the full
attack, truncated only in the walk width. Extrapolation to 256-bit points
crosses about 240 bits. Truncation cannot rule out a global almost-permutation
structure that would suppress full-size collisions. No full-scale collision is
known, and running the attack is infeasible. H1 remains a modeling hypothesis.

Evidence references: `experiment:scaled-dp-walk` and this section together with
Sections 1–4 and 7.

## 6. Charged cost under collision-frontier-v5

One selected 2-round compression costs `1` unit. Every other listed 256-bit RAM
primitive costs `1/C` with `C = 430`. Internals of a charged compression are not
priced again. Parallel wall-clock latency is irrelevant; total work is summed.

### 6.1 Per-step walk cost

Represent the point in an 8-word buffer `P` and the salt in an 8-word buffer
`S` (written once). Each walk step:

1. issues one target compression reading `P||S` and writing an 8-word digest
   buffer `D` (cost 1);
2. copies `D` into `P` (8 stores);
3. compares `P[0]` to zero and branches to the DP handler if equal (2 ops);
4. increments the step counter and compares it to `k` with a branch (3 ops).

That is 13 listed word operations. An implementation allowance for address
arithmetic, flag clearing, and an extra defensive compare brings the charged
envelope to **32 word operations per step**. Per-step charged time is

    1 + 32/430 = 462/430.

The DP handler (pack, store record, bound check) is charged **64** word
operations per recorded DP and runs on about `k·theta ≈ 2^96` steps, already
covered in Section 6.3.

### 6.2 Walk length

    k = 2^128 + 2^40 < 2^128 (1 + 2^{-88}).

Walk charge:

    T_walk < k · 462/430
           < (462/430) · 2^128 · (1 + 2^{-88})
           < 1.0744187 · 2^128.

### 6.3 Relocation (birthday-scale, explicit)

Step 5 permits at most `k'` compressions to form `b` and at most `k'` lockstep
iterations, each lockstep iteration issuing two compressions. Worst-case over
every run (success or failure), using the written caps and `λ <= k` before the
`λ > k'` rejection on paths that somehow produce a huge lag from the finite
walk:

    #compressions_reloc <= λ + 2 · k'  <= k + 2 · k'  < 3 · 2^128 + 2^40.

Each relocation compression is paired with an envelope of **64** accompanying
word operations (copy, compare, branch, counter), matching the prior package's
reloc envelope:

    T_reloc < (3 · 2^128 + 2^40) · (1 + 64/430)
            < (3 · 2^128 + 2^40) · 494/430
            < 3.44652 · 2^128.

(The slightly tighter reading that rejects `λ > k'` before forming `b`, so that
`#compressions_reloc <= 3 · k'` on every continuing path, yields the same
leading coefficient up to `2^{-88}` relative terms.)

### 6.4 Sorting, verification, setup

- At most `D_max = 2^110` records. At most 120 merge passes, each writing every
  record, with at most 80 word operations per record per pass:

      W_sort <= 120 · 2^110 · 80 = 9600 · 2^110 < 2^14 · 2^110 = 2^124,
      W_sort / C < 2^124 / 430 < 2^{115.8}.

- Final verification: two compressions plus `< 2^10` word operations.
- Setup (load code/constants, write salt, clear counters): `< 2^20` word
  operations, i.e. `< 2^20/430 < 2^{11.3}` units.
- DP handlers across the walk: `< (2^96 + 2^9) · 64 / 430 < 2^{90}` units.

Summing the non-walk, non-reloc contributions:

    T_other < 2^{115.8} + 4 + 2^{11.3} + 2^{90}
            < 2^{116}
            = 2^{-12} · 2^128
            < 0.00025 · 2^128.

### 6.5 Total

    T < T_walk + T_reloc + T_other
      < (1.0744187 + 3.44652 + 0.00025) · 2^128
      < 4.52119 · 2^128.

Now `2^{2.176} ≈ 4.521` and `log2(4.52119) ≈ 2.176`, so

    T < 2^{130.176} < 2^{130.18}.

The claim `time_log2 = 130.18` is this bound rounded up to two decimals. It
caps every run, success or failure, and includes preprocessing, failed DP
checks, sorting, birthday-scale relocation, and verification.

This matches the independent cost-role reconstruction on the prior (undercharged)
package once relocation is priced honestly (~130.18).

### 6.6 Memory, preprocessing, advice

Each record stores two 256-bit words (packed point and index), i.e. **64 bytes**,
not 16. Three arrays of `D_max = 2^110` records, plus `2^24` bytes of
code/constants/scratch:

    peak bytes <= 3 · 2^110 · 64 + 2^24
               = 3 · 2^116 + 2^24
               < 2^{117.59} + 2^24
               < 2^118.

Expected use is far lower (`~2^96` records). Claim
`memory_log2_bytes = 118`.

**Revision note.** The prior package described two 256-bit words but priced 16
bytes per record. That understatement is removed; `D_max` is lowered from
`2^112` to `2^110` so the corrected 64-byte records still fit under `2^118`.

Preprocessing (setup) is `< 2^{12}` units after `/C` pricing; claim
`preprocessing_log2 = 12`. It is included in `T`. Nonuniform advice is zero;
the schema field is `0` meaning at most one byte of advice capacity.

## 7. Structural remarks (not used for a sub-birthday claim)

With the fixed IV and flags, the state after a single round determines the
sixteen message words in the natural algebraic sense of the G-sequence (each
message word enters once as an additive input). A collision of complete digests
therefore requires a nonzero intermediate difference that cancels through the
second round and the feed-forward fold. The naive lane-complement trick fails
modular addition (`NOT c + NOT d = NOT(c+d) - 1`). No usable differential
characteristic yielding a proven sub-birthday ordinary collision was obtained.
This package therefore remains at the generic birthday regime.

## 8. Evidence summary and interpretation

| Item | Content |
| --- | --- |
| Algorithm | Sections 1–3 (relocation caps explicit) |
| RF success bound | Section 4 (`> 0.3934`; no small-cycle assumption) |
| Heuristic H1 | Section 5; claim role `score-critical` |
| Organizer experiment | `scaled-dp-walk` (manifest + program; capped relocation) |
| Cost ledger | Section 6 (`T < 2^{130.18}`) |
| Certificates | none; `certificates/manifest.json` is empty and valid |
| Prior refute addressed | cycle tail; relocation charge; 64-byte records |

`submission_state = ready` means the package is complete for exploratory
review. It does not assert that review has already qualified the claim, that a
score has been emitted, or that Yukon has promoted it. The required
`baseline_improved` identifier `blake3-r2-nominal-v2` names the organizer
nominal reference 128; the field name is not an improvement assertion. The
scalar 130.18 lies above 128 by charged RAM overhead, birthday-scale
relocation, and rounding.

## 9. Comparison to the sort-based 140 package and the refuted 128.11 attempt

The previous ready package stored `n = 2^129` triples and merge-sorted them,
paying roughly `129 · Θ(n)` word operations. With `C = 430` that overhead
dominated and produced `time_log2 = 140`.

The refuted 128.11 attempt replaced the sort by a DP rho walk but (i) treated
`λ_cycle > 2^41` as negligible, (ii) charged `O(Gap)` relocation despite an
algorithm that can walk from `x_0` for `~μ` steps, and (iii) priced 64-byte
records at 16 bytes. The present package keeps the DP walk, charges
`~3 · 2^128` relocation compressions honestly, corrects the probability
events, and prices memory correctly, yielding **130.18** — still about 9.8
bits below 140.
