# Salted multi-trail distinguished-point collision search

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains a
separately reported resource bound.

This exploratory package targets `blake3-r2-prefix-v1`. It proposes a classical
randomized algorithm with algorithmic success probability at least 0.39 under
heuristic H1, total charged time at most `2^128.11` units, and peak memory at
most `2^118` bytes. These are analytical upper bounds on charged computation,
not measured wall-clock costs. The claimed scalar is **128.11**.

## Provenance and refute lessons

- Refuted `1e53125f` (claimed 128.11, single-trail): (1) false negligibility of
  `Pr[λ_cycle > 2^41]`; (2) relocation charged as `O(Gap)` while the written
  procedure walked from `x_0` on a birthday scale; (3) records of two 256-bit
  words priced at 16 bytes instead of 64.
- In-flight revision `60ac8137` (claimed 130.18, single-trail): fixed those three
  defects by charging `~3 · 2^128` relocation compressions, correcting the cycle
  analysis, and pricing 64-byte records. That package is honest but pays the
  Pollard entrance-finding tax of a **single** long trail.
- **This package** keeps the three corrections and **changes the algorithm** to
  classical multi-trail van Oorschot–Wiener (VOW) search. Colliding trails are
  short (`≤ L_max = 2^40`), so recovery is `O(L_max)` rather than `O(2^128)`.
  Cycle lengths may be birthday-scale; the algorithm never assumes otherwise.

Relative to the organizer generic-birthday sort package at time_log2=140, the
material change is replacing memory-bound sorting of `2^129` full records by a
low-memory DP collision search whose dominant cost is about `2^128` compressions
plus small RAM overhead priced at `1/C` with `C=430`.

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

## 2. Algorithm (multi-trail VOW)

Constants:

| symbol | value | role |
| --- | ---: | --- |
| `K` | `2^128 + 2^48` | hard cap on total compressions during trail generation |
| `L_max` | `2^40` | maximum length of any single trail |
| `M_max` | `2^110` | hard cap on stored trail records |
| `theta` | `2^{-32}` | distinguished-point rate (lane 0 = 0) |

Coins: draw a uniform salt `s` (eight 32-bit lanes) once. Every trail start is an
independent uniform point drawn from the RAM model's random-word primitive.
No PRNG beyond that primitive is used.

A **trail record** is the pair `(pack(DP), pack(start))` — two 256-bit words,
**64 bytes**.

1. **Trail generation.** Set `spent <- 0`. While `spent < K`:
   - Draw a fresh uniform start `u`. Set `x <- u`.
   - For `ell = 1, 2, ..., L_max`:
     - Replace `x` by `f_s(x)` and set `spent <- spent + 1`.
     - If `spent = K`, exit the generation loop (go to failure if no collision
       was already recovered).
     - If `x` is distinguished:
       - If a record with the same packed DP already exists and its stored
         start `u'` satisfies `u' != u`, go to Step 3 with starts `(u', u)`
         and common DP `x`.
       - Otherwise store `(pack(x), pack(u))`, failing if more than `M_max`
         records would be stored, and end this trail.
   - If the trail reaches `L_max` without a DP, abandon it (no store).
2. **Failure.** If generation ends without a two-start DP match, fail.
3. **Recovery (O(L_max), not O(2^128)).** Given distinct starts `u', u` that
   both reach the same DP:
   - Re-walk from `u'` for at most `L_max` steps, inserting every visited point
     into a temporary hash set `H` (at most `L_max` entries) together with its
     predecessor; stop when the common DP is reached.
   - Re-walk from `u` for at most `L_max` steps. Let `a` be the current point
     and `b <- f_s(a)`. If `b ∈ H` and `a` is not the stored predecessor of `b`
     on the first trail (equivalently: the two predecessors of `b` differ),
     go to Step 4 with that candidate pair. Also accept if the two immediate
     predecessors of the common DP differ and both trails reach it.
   - Fail if no distinct predecessor pair is found within the caps.
4. **Verify.** Recompute `H(M_s(a))` and `H(M_s(b))` from the all-zero state.
   Accept iff the messages differ and all 256 digest bits agree; otherwise fail.

There are many short trails, one shared salt, and a deterministic charged-time
cap. Every accepted output is an ordinary collision under Section 1.

**Contrast with the single-trail 130.18 package.** That package built one trail
of length `~2^128`, read a lag `λ = j* - i*` that is typically birthday-scale,
and charged up to `3 · 2^128` compressions to form `f^λ(x_0)` and lockstep from
`x_0`. The present package never runs a birthday-length lockstep: each trail is
capped by `L_max = 2^40`, and recovery re-walks two such trails.

## 3. Correctness of any accepted pair

Injectivity of `x |-> M_s(x)` for fixed `s` gives distinct messages whenever
`a != b`. Step 4 recomputes complete selected-target digests and checks equality
of all 256 bits, so acceptance implies an ordinary collision for
`blake3-r2-prefix-v1`. The algorithm never claims a free-start,
compression-only, or different-round result.

## 4. Success probability in the random-function model

Work in the uniform random-function model: for fixed coins giving `s` and the
stream of starts, treat `f_s` as a uniformly random function `[N] -> [N]`.

Let `T` be the number of compressions actually issued during Step 1. The
algorithm hard-caps `T ≤ K = 2^128 + 2^48`. Write `K' = 2^128`. On paths that
do not early-exit into recovery, `T ≥ K'` except for an empty set of schedules
that hit the `spent = K` cut mid-trail after already spending `K'`; we charge
the full `K` in Section 6 regardless.

**Event A (birthday coverage).** Among any `K'` evaluations of a random function
at distinct domain points, the probability that all images are distinct is at
most

    exp(-K'(K'-1)/(2N)) < exp(-1/2 + 2^{-127}) < 0.6065307.

Internal repeats inside a single trail of length `≤ L_max = 2^40` have
probability `≤ L_max^2 / (2N) < 2^{-175}` per trail. With at most `K` trails
attempted, a union bound gives `< 2^{-40}` chance that any trail has an internal
domain repeat before the global birthday event. Conditioning on no such internal
repeat, the `K'` evaluations that open the budget are at distinct points, and

    Pr[no f-collision among those evaluations] < 0.6065307.

Thus event A fails with probability `< 0.6065307 + 2^{-40}`.

**Cycle lengths need not be small.** Nothing in the argument requires
`λ_cycle ≤ 2^41` or any other sub-birthday lag bound. Trails are truncated by
`L_max` regardless of the global component structure. This is the explicit
rejection of the fatal flaw in `1e53125f`.

**Event B (DP detection of a collision).** Suppose distinct domain points `p, q`
with `f(p) = f(q)` both occur on generated trails. From the merge point the two
trails follow the same path. A distinguished point occurs within `L` further
steps with probability `1 - (1-theta)^L`. Taking `L = L_max = 2^40`,

    (1-theta)^{L_max} ≤ exp(-L_max · theta) = exp(-2^8) = exp(-256) < 10^{-110}.

Both trails have remaining length budget at least 1 with overwhelming
probability on the event that the collision occurred at trail positions below
`L_max - 2^{36}` (all but an exponentially small fraction of positions in a
length-`L_max` trail). A union bound with the geometric tail gives failure of
DP detection `< 10^{-100}` for the numerical envelope used below.

Same-start DP repeats (a trail looping onto its own stored DP) are discarded by
Step 1's `u' != u` check. Per-trail self-collision probability is
`< L_max^2/(2N) < 2^{-175}`; across `≤ 2^96` expected completed trails the
expected number of self-hits is `< 2^{-70}`. They do not contribute a material
failure term.

**Event D (both matching trails stored before overflow).** Expected completed
trails are at most `1 + K · theta < 2^96 + 2^{17}`. Markov on the record count:

    Pr[records > M_max] < (2^96 + 2^{17}) / 2^110 < 2^{-13.9}.

**Event E (recovery cap).** On a two-start DP match whose trails each have
length `≤ L_max`, Step 3 issues at most `2 · L_max` re-walk compressions plus at
most `L_max` comparisons against `H`. The written cap `3 · L_max` therefore
suffices on every path that Step 1 hands to Step 3. Failure of E has
probability 0 under the algorithmic caps (it is a deterministic resource bound,
not a random event).

**Event G (abandoned-trail mass).** Probability a single trail of length
`L_max` misses every DP: `≤ exp(-256)`. Expected wasted compressions on
abandoned trails over the whole run: `< K · exp(-256)`, negligible. The
`+2^48` additive in `K` absorbs all such waste and mid-trail budget cuts many
times over.

On A ∩ B ∩ D ∩ E ∩ G, Step 3 returns a distinct predecessor pair and Step 4
accepts. Hence

    Pr[success | random f] > 1 - (0.6065307 + 2^{-40} + 10^{-100} + 2^{-13.9})
                           > 1 - 0.6066
                           = 0.3934.

The claim uses `success_probability = 0.39`, leaving an allowance of `0.0034`
for the heuristic gap in Section 5.

**Relocation / recovery is charged at `O(L_max)`, and that is all that is
needed.** There is no hidden uncapped search from `x_0` over a birthday horizon.

## 5. Heuristic H1 (score-critical)

**H1-salted-random-mapping.** For uniform salt and independent uniform starts,
the failure probability of events A,B,D,E,G on the real `f_s` is at most the
random-function value above, up to a negligible additive amount covered by the
`0.0034` allowance.

Salt is essential: a single fixed unsalted map can deviate from the average
collision statistics. Randomizing the function through the salt places the
probability in the standard generic-hash / VOW modeling regime.

### 5.1 Organizer experiment `scaled-multi-trail-dp`

The program `experiments/scaled_multi_trail_dp.py` is a complete scaled copy of
Steps 1–4 on the exact 2-round root compression. Points are 16-bit integers
(`N_t = 2^16`). The message places the point in word 0 and the salt in word 1
(other words zero). Distinguished points have the low 2 bits clear
(`theta_t = 2^{-2}`). Parameters `K = 2^8 + 2^5`, `L_max = 2^6`, `M_max = 2^12`
were fixed before production runs. Recovery re-walks two starts with the same
`L_max` discipline as full scale. The organizer checks `digest-xor-mask` with
mask `ffff || 00^30`, i.e. equality of the first 16 digest bits — exactly the
truncated walk map.

**Parameter-fidelity note.** At 16 bits, `L_max · theta = 2^6 · 2^{-2} = 16`,
versus full scale `2^40 · 2^{-32} = 256`. Both are `≫ 1`, so per-trail DP-miss
probabilities are tiny at both scales; the scaled experiment is supporting
evidence for salted multi-trail behaviour of the truncated 2-round map, not a
substitute for Section 4.

Local non-organizer Monte Carlo is not authoritative; the organizer report is.

### 5.2 Extrapolation and limits

The scaled map uses the same 2-round compression and feed-forward as the full
attack, truncated only in the walk width. Extrapolation to 256-bit points
crosses about 240 bits. Truncation cannot rule out a global almost-permutation
structure that would suppress full-size collisions. No full-scale collision is
known, and running the attack is infeasible. H1 remains a modeling hypothesis.

## 6. Charged cost under collision-frontier-v5

One selected 2-round compression costs `1` unit. Every other listed 256-bit RAM
primitive costs `1/C` with `C = 430`. Internals of a charged compression are not
priced again. Parallel wall-clock latency is irrelevant; total work is summed
across all trail generations and recovery.

### 6.1 Per-step trail cost

Represent the current point in an 8-word buffer `P` and the salt in an 8-word
buffer `S` (written once). Each trail step:

1. issues one target compression reading `P||S` and writing an 8-word digest
   buffer `D` (cost 1);
2. copies `D` into `P` (8 stores);
3. compares `P[0]` to zero and branches to the DP handler if equal (2 ops);
4. increments the step counter / spent counter and compares with bounds
   (5 ops).

That is 15 listed word operations. An implementation allowance for address
arithmetic, flag clearing, and defensive compares brings the charged envelope
to **32 word operations per step** — matching the conservative envelope of the
130.18 single-trail package's walk. Per-step charged time is

    1 + 32/430 = 462/430.

The DP handler (pack DP, pack start, table probe/store, bound check) is charged
**64** word operations per stored record and runs on about `K · theta ≈ 2^96`
trails, accounted in Section 6.3.

### 6.2 Trail-generation length

    K = 2^128 + 2^48 < 2^128 (1 + 2^{-80}).

Generation charge:

    T_gen < K · 462/430
          < (462/430) · 2^128 · (1 + 2^{-80})
          < 1.0744187 · 2^128.

### 6.3 Recovery (short-trail, explicit)

Step 3 permits at most `3 · L_max = 3 · 2^40` compressions on every run that
invokes recovery, and zero otherwise. Worst-case over every run:

    T_rec < 3 · 2^40 · (1 + 64/430)
          < 3 · 2^40 · 494/430
          < 2^{41.12}.

Relative to `2^128` this is `< 2^{-86.8} · 2^128`, negligible in the leading
bits. **This replaces the `~3 · 2^128` single-trail relocation charge.**

### 6.4 Sorting / table, verification, setup, DP handlers

- At most `M_max = 2^110` records of 64 bytes. Building and probing a hash
  table, or sorting for a deterministic scan, is charged as at most 120 passes
  over `M_max` records with at most 80 word operations per record per pass:

      W_tab <= 120 · 2^110 · 80 = 9600 · 2^110 < 2^124,
      W_tab / C < 2^124 / 430 < 2^{115.8}.

- Final verification: two compressions plus `< 2^10` word operations.
- Setup (load code/constants, write salt, clear counters): `< 2^20` word
  operations, i.e. `< 2^20/430 < 2^{11.3}` units.
- DP handlers across generation: `< (2^96 + 2^{17}) · 64 / 430 < 2^{90}` units.
- Temporary recovery set `H`: at most `L_max` points, `< 2^{40} · 64` bytes of
  memory (already inside the peak bound of Section 6.6) and `< 2^{40} · 32 / 430`
  word-operation charge `< 2^{36}` units.

Summing the non-generation, non-recovery contributions:

    T_other < 2^{115.8} + 4 + 2^{11.3} + 2^{90} + 2^{36} + 2^{41.12}
            < 2^{116}
            = 2^{-12} · 2^128
            < 0.00025 · 2^128.

### 6.5 Total

    T < T_gen + T_rec + T_other
      < (1.0744187 + 0.00025) · 2^128
      < 1.07467 · 2^128.

Now `log2(1.07467) ≈ 0.1039`, so

    T < 2^{128.104} < 2^{128.11}.

The claim `time_log2 = 128.11` is this bound rounded up to two decimals. It
caps every run, success or failure, and includes preprocessing, abandoned
trails, table work, short-trail recovery, and verification.

### 6.6 Memory, preprocessing, advice

Each trail record stores two 256-bit words (packed DP and packed start), i.e.
**64 bytes**, not 16. Three arrays of `M_max = 2^110` records, plus `2^24` bytes
of code/constants/scratch, plus a recovery set of `L_max` points:

    peak bytes <= 3 · 2^110 · 64 + 2^40 · 32 + 2^24
               = 3 · 2^116 + 2^{45} + 2^24
               < 2^{117.59} + 2^{45}
               < 2^118.

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
| Algorithm | Sections 1–3 (multi-trail; recovery `O(L_max)`) |
| RF success bound | Section 4 (`> 0.3934`; no small-cycle assumption) |
| Heuristic H1 | Section 5; claim role `score-critical` |
| Organizer experiment | `scaled-multi-trail-dp` |
| Cost ledger | Section 6 (`T < 2^{128.11}`) |
| Certificates | none; `certificates/manifest.json` is empty and valid |
| Prior refute addressed | cycle tail (not assumed small); recovery charge (`O(L_max)`); 64-byte records |

`submission_state = ready` means the package is complete for exploratory
review. It does not assert that review has already qualified the claim, that a
score has been emitted, or that Yukon has promoted it. The required
`baseline_improved` identifier `blake3-r2-nominal-v2` names the organizer
nominal reference 128; the field name is not an improvement assertion. The
scalar 128.11 lies above 128 by charged RAM overhead and rounding.

## 9. Comparison

| Package | Algorithm | Relocation / recovery | time_log2 |
| --- | --- | --- | ---: |
| Organizer sort | sort `2^129` records | n/a (table) | 140 |
| Refuted `1e53125f` | single-trail DP | undercharged `O(Gap)` + false `λ≤2^41` | 128.11 (fatal) |
| In-flight `60ac8137` | single-trail DP | honest `~3 · 2^128` | 130.18 |
| **This package** | **multi-trail VOW** | **honest `~3 · 2^40`** | **128.11** |

Public awaiting-review notes near 128 that still use single-trail lockstep with
a small-lag assumption are treated as untrusted research pointers; this write-up
re-derives a multi-trail ledger that does not need that assumption.
