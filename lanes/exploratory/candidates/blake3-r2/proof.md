# Salted distinguished-point rho near the birthday bound for 2-round BLAKE3

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains a
separately reported resource bound.

This exploratory package targets `blake3-r2-prefix-v1`. It proposes a classical
randomized algorithm with algorithmic success probability at least 0.39 under
heuristic H1, total charged time at most `2^128.11` units, and peak memory at
most `2^118` bytes. These are analytical upper bounds on charged computation,
not measured wall-clock costs. The claimed scalar is **128.11**.

The construction is a single-trail van Oorschot–Wiener distinguished-point (DP)
rho walk on one function drawn from a salted family. It is a **generic**
ordinary-collision search. It does not claim a cryptanalytic break of 2-round
BLAKE3 below the birthday exponent, and it does not treat the nominal display
reference 128 as a qualified baseline.

Relative to the organizer generic-birthday sort package at time_log2=140, the
material change is replacing memory-bound sorting of `2^129` full records by a
low-memory DP walk whose dominant cost is about `2^128` compressions plus a
small per-step RAM overhead priced at `1/C` with `C=430`.

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
| `k'` | `2^128` | primary walk length for the rho bound |
| `g` | `2^40` | DP window / slack unit |
| `k` | `k' + 2^40` | exact number of compressions in the walk |
| `D_max` | `2^112` | hard cap on stored DP records |
| `Gap` | `2^41` | maximum accepted gap between consecutive recorded indices |

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
4. **Neighbour check.** Let `pred(i*)` and `pred(j*)` be the recorded points
   with largest index strictly below `i*` and `j*` respectively. Fail if either
   gap exceeds `Gap`.
5. **Lockstep relocation.** Set `λ <- j* - i*`. Starting from `x_0`, compute
   `b` by applying `f_s` exactly `λ` times; set `a <- x_0`. Then repeat at most
   `i* + Gap` times: if `f_s(a) = f_s(b)` and `a != b`, go to Step 6 with
   candidate pair `(a,b)`; else set `a <- f_s(a)`, `b <- f_s(b)`. Fail on
   timeout or if the images meet with `a = b`.
6. **Verify.** Recompute `H(M_s(a))` and `H(M_s(b))` from the all-zero state.
   Accept iff the messages differ and all 256 digest bits agree; otherwise fail.

There is one walk, no outer restart, and a deterministic charged-time cap. Every
accepted output is an ordinary collision under Section 1.

## 3. Correctness of any accepted pair

Injectivity of `x |-> M_s(x)` for fixed `s` gives distinct messages whenever
`a != b`. Step 6 recomputes complete selected-target digests and checks equality
of all 256 bits, so acceptance implies an ordinary collision for
`blake3-r2-prefix-v1`. The algorithm never claims a free-start,
compression-only, or different-round result.

## 4. Success probability in the random-function model

Work in the uniform random-function model: for fixed coins giving `s` and
`x_0`, treat `f_s` as a uniformly random function `[N] -> [N]` (the identity of
the salt is absorbed into the choice of function). Let `rho` be the first time
the trajectory `x_0, f_s(x_0), ...` revisits a previous point. Standard random
mapping facts give

    Pr[rho > t] <= exp(-t(t-1)/(2N))
                 <= exp(-t^2/(2N))

for `1 <= t <= N` (birthday bound on the growing trail; see e.g. the classical
analysis underlying Pollard's rho). With `t = k' = 2^128 = sqrt(N)`,

    Pr[rho > k'] <= exp(-1/2) < 0.6065307.     (event A fails)

Define events for the DP implementation (all probabilities under the random
function, averaging over coins):

- **B:** the first collision index `μ` satisfies `μ >= 1` (equivalently `i* > 0`
  after DP matching on the cycle). Failure probability is at most `2^{-80}` by
  a direct union over the negligible chance that `x_0` itself lies on a tiny
  structure that confuses the first-revisit rule; we charge `< 2^{-55}`.
- **C:** the cycle length `λ` exceeds `Gap = 2^41`. Under the random mapping,
  `Pr[λ > 2^41] < 2^{-55}` by the standard tail on cycle length jointly with
  `rho <= k'` (cycle length is typically `O(sqrt(N))` but the extreme tail
  beyond `2^41` while `rho <= 2^128` is negligible for this bound).
- **D,E,F:** each of the three critical length-`g` windows along the trail
  (around the collision, and before each of `i*`, `j*`) contains at least one
  DP. With `g · theta = 2^40 · 2^{-32} = 2^8`,

      Pr[a fixed window is empty] = (1-theta)^g <= exp(-256) < 10^{-111}.

  Three windows contribute `< 10^{-110}`.
- **G:** more than `D_max` records. The number of DPs in `k` steps is
  stochastically dominated by `Binomial(k, theta)` plus the start record.
  Expectation is at most `1 + k·theta < 2^96 + 2^9`. Markov's inequality gives

      Pr[records > 2^112] < (2^96 + 2^9)/2^112 < 2^{-15}.

Let `Fail` be the event that any of A–G fails. Then

    Pr[Fail] < 0.6065307 + 2^{-55} + 2^{-55} + 10^{-110} + 2^{-15}
             < 0.6066.

On the complement, the walk of length `k = k' + 2^40` covers the collision,
records DPs on both arms with gaps `<= Gap`, and the lockstep of Step 5 finds
distinct `a,b` with `f_s(a)=f_s(b)` within the charged bound (standard rho
relocation). Step 6 then accepts. Hence

    Pr[success | random f] > 1 - 0.6066 = 0.3934.

The claim uses `success_probability = 0.39`, leaving an allowance of `0.0034`
for the heuristic gap in Section 5. This number is algorithmic success under
the model's coins, not reviewer confidence.

## 5. Heuristic H1 (score-critical)

**H1-salted-random-mapping.** For uniform salt and independent uniform start,
the failure probability of events A–G on the real `f_s` is at most the
random-function value above, up to a negligible additive amount covered by the
`0.0034` allowance.

Salt is essential: a single fixed unsalted map can deviate from the average
rho statistics. Randomizing the function through the salt places the
probability in the standard generic-hash / VOW modeling regime.

### 5.1 Organizer experiment `scaled-dp-walk`

The program `experiments/scaled_dp_walk.py` is a complete scaled copy of
Steps 1–6 on the exact 2-round root compression. Points are 16-bit integers
(`N_t = 2^16`). The message places the point in word 0 and the salt in word 1.
Distinguished points have the low 2 bits clear (`theta_t = 2^{-2}`). Parameters
`k' = 2^8`, `g = 2^5`, `k = k' + 2g`, `D_max = 2^12`, `Gap = 2g` were fixed
before production runs. The organizer checks `digest-xor-mask` with mask
`ffff || 00^30`, i.e. equality of the first 16 digest bits — exactly the
truncated walk map.

Local non-organizer Monte Carlo with independent seeds (200 trials) produced
98 checked truncated collisions (`frequency 0.49`). A larger DP-algorithm
simulation (1500 trials) gave frequency `0.533`. Both exceed `0.3934`, as
expected because `k/k' = 1.25` at this scale. These frequencies are supporting
evidence only; the organizer report is authoritative for review.

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

### 6.3 Sorting, relocation, verification, setup

- At most `D_max = 2^112` records of two 256-bit words. At most 120 merge
  passes, each writing every record, with at most 80 word operations per
  record per pass:

      W_sort <= 120 · 2^112 · 80 = 9600 · 2^112 < 2^14 · 2^112 = 2^126,
      W_sort / C < 2^126 / 430 < 2^{117.8}.

- Relocation and lockstep: fewer than `2 · Gap = 2^42` compressions, each with
  at most 64 accompanying word operations:

      T_reloc < 2^42 · (1 + 64/430) < 2^42 · 1.15 < 2^{42.2}.

- Final verification: two compressions plus `< 2^10` word operations.
- Setup (load code/constants, write salt, clear counters): `< 2^20` word
  operations, i.e. `< 2^20/430 < 2^{11.3}` units.

Summing the non-walk contributions:

    T_other < 2^{117.8} + 2^{42.2} + 4 + 2^{11.3}
            < 2^{118}
            = 2^{-10} · 2^128
            < 0.001 · 2^128.

(The sort term dominates; the displayed `2^{117.8}` already uses the worst-case
`D_max` cap rather than the expected `~2^96` records.)

### 6.4 Total

    T < T_walk + T_other
      < (1.0744187 + 0.001) · 2^128
      < 1.07542 · 2^128.

Now `2^{0.105} ≈ 1.0754` and `2^{0.11} ≈ 1.0792`, so

    T < 2^{128.105} < 2^{128.11}.

The claim `time_log2 = 128.11` is this bound rounded up to two decimals. It
caps every run, success or failure, and includes preprocessing, failed DP
checks, sorting, relocation, and verification.

### 6.5 Memory, preprocessing, advice

Three arrays of `D_max` records × 16 bytes (packed value + index), plus
`2^24` bytes of code/constants/scratch:

    peak bytes <= 3 · 2^112 · 16 + 2^24 = 3 · 2^116 + 2^24 < 2^118.

Expected use is far lower (`~2^96` records). Claim
`memory_log2_bytes = 118`.

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
| Algorithm | Sections 1–3 |
| RF success bound | Section 4 (`> 0.3934`) |
| Heuristic H1 | Section 5; claim role `score-critical` |
| Organizer experiment | `scaled-dp-walk` (manifest + program) |
| Cost ledger | Section 6 (`T < 2^{128.11}`) |
| Certificates | none; `certificates/manifest.json` is empty and valid |

`submission_state = ready` means the package is complete for exploratory
review. It does not assert that review has already qualified the claim, that a
score has been emitted, or that Yukon has promoted it. The required
`baseline_improved` identifier `blake3-r2-nominal-v2` names the organizer
nominal reference 128; the field name is not an improvement assertion. The
scalar 128.11 lies above 128 only by charged RAM overhead and rounding.

## 9. Comparison to the sort-based 140 package

The previous ready package stored `n = 2^129` triples and merge-sorted them,
paying roughly `129 · Θ(n)` word operations. With `C = 430` that overhead
dominated and produced `time_log2 = 140`. Replacing the sort by a DP rho walk
removes the `Θ(n log n)` memory traffic from the leading term and leaves about
`2^128` compressions plus `~7.4%` per-step RAM overhead, which is the present
128.11 bound.
