# A low-memory distinguished-point walk for SHA-256 r37 collisions

## 1. Claim and scope

This package specifies a classical randomized algorithm for the exact
`sha256-r37-prefix-v1` target in the exploratory lane. On every random tape its
total charged time is below `2^128.15` target-compression units and its peak
memory is below `2^20` bytes. Under one declared premise, `RM-WALK` (Section 5),
it returns two distinct complete messages with equal full 256-bit digests with
probability greater than `0.4249`, which exceeds the required `0.39` by 0.0349.

The method is the textbook one: a Pollard-rho walk whose repeat is detected with
sparse distinguished points (van Oorschot and Wiener). No cryptanalytic property
of SHA-256 is used, no novelty is claimed, and nothing here is specific to 37
rounds except the target being hashed. The walk stores an 8192-entry table, so
its memory stays below `2^20` bytes; that is its whole purpose. The scalar
projection is `128.15 + max(0, 20 - 20) = 128.15`.

The required `baseline_improved` value `sha256-r37-nominal-v2` names the
organizer's nominal reference (display value 128). This construction does not
beat that value and does not claim to. No collision witness is supplied: a full
run is far beyond feasible computation. The success bound depends on
`RM-WALK`, which is a heuristic, not a theorem (Sections 5 and 10).

## 2. Messages and the iteration family

Write `H` for the complete `sha256-r37` hash of a byte string: the standard
fixed IV, FIPS 180-4 padding, indices 0 through 36 of the standard schedule and
round constants on every padded block, wordwise feed-forward, and big-endian
serialization of all eight chaining words. Every message used here is 48 bytes,

```
m(x, r) = BE32(x) || BE16(r),   x in {0,1}^256,  r in {0,1}^128,
```

where BEk is k bytes big-endian. Its bit length 384 satisfies the domain. The
padded message is exactly one block. Its sixteen 32-bit words are `x` (W0..W7,
most significant first), `r` (W8..W11), `0x80000000` (W12, the `0x80` byte),
`0, 0` (W13, W14, the zero bytes and the high half of the length) and `384`
(W15). There is no second block. One call of the priced primitive on this
block from the IV, followed by serialization, is `H(m(x, r))`.

For each `r` define `f_r(x) = H(m(x, r))`, read back as a 256-bit integer. Then
`f_r` maps `{0,1}^256` to itself. If `x != y` and `f_r(x) = f_r(y)`, then
`m(x, r)` and `m(y, r)` are distinct messages with equal full digests: an
ordinary collision of the exact target. Nothing is truncated and no chaining
value is chosen.

The algorithm draws `r` once, uniformly, and draws a uniform start `x_0`. The
walk is `x_{t+1} = f_r(x_t)`. Let `rho` be the first index with
`x_rho in {x_0, ..., x_{rho-1}}`, let `mu < rho` be the index with
`x_mu = x_rho`, and let `lambda = rho - mu >= 1`. Then `x_0, ..., x_{rho-1}`
are distinct and `x_t = x_{t-lambda}` for every `t >= rho`. If `mu >= 1`, the
pair `(x_{mu-1}, x_{rho-1})` has distinct entries (two different indices below
`rho`) and equal images `x_mu = x_rho`. If `mu = 0` the start lies on its own
cycle and gives no collision.

A value `x` is *distinguished* (a DP) when its top 116 bits are zero, i.e.
`x < 2^140`: the three most significant words are zero and the fourth is below
`2^12`. The DP fraction is exactly `theta = 2^-116`.

## 3. Algorithm

Fixed parameters: `k = 68 * 2^122 = (17/16) * 2^128`, `L = 2^120`,
`TCAP = k + L`, table capacity `K = 2^13`. The table holds pairs
`(value, index)` of 256-bit words in insertion order, which is increasing index
order. This is inert pseudocode, not an experiment program.

```
r  = RANDOM256() AND (2^128 - 1);   x0 = RANDOM256()
table = []; x = x0; t = 0
loop:                                           # walk
    if x < 2^140:                               # DP test
        if some table entry j has value x: s = index(j); goto found
        if len(table) == K: return FAILURE      # overflow
        append (x, t)
    if t == TCAP: return FAILURE
    x = f_r(x); t = t + 1
found:
    lam = t - s
    (vp, sp) = entry before j in the table, or (x0, 0) if j is the first entry
    tau = sp + lam
    if tau >= s:
        j* = last table entry with index <= tau  (scanning forward from j)
        (base, steps) = (value(j*), tau - index(j*))
    else:
        (base, steps) = (vp, lam)
    if steps > 2L: return FAILURE
    A = vp; B = f_r applied steps times to base     # B-preparation
    if A == B: return FAILURE
    repeat at most L times:                         # lockstep
        if f_r(A) == f_r(B):
            recompute H(m(A,r)) and H(m(B,r)) from the IV
            return (m(A,r), m(B,r)) if A != B and the digests agree, else FAILURE
        A = f_r(A); B = f_r(B)
    return FAILURE
```

The lockstep keeps `f_r(A)` and `f_r(B)` from the comparison as the next `A` and
`B`, so each iteration makes exactly two target calls. No step restarts, retries
or amplifies. Every exit is bounded by an explicit counter.

## 4. Deterministic correctness

Fix `r` and `x_0`, so `rho`, `mu` and `lambda` are fixed.

**Lemma 1 (detection).** If the cycle `x_mu, ..., x_{rho-1}` contains a DP, let
`s` be the smallest DP index with `s >= mu`. Provided no earlier exit (table
overflow or the step limit) occurs, the walk detects at `t = s + lambda`, with
table entry index `s`, so `lam = lambda`. If the cycle contains no DP, no
detection ever happens and the walk ends at `TCAP` with FAILURE.
*Proof.* Values at indices below `rho` are distinct, so no stored value recurs
before index `rho`. A DP value stored at index `u` recurs first at `u + lambda`
if `u >= mu` and never if `u < mu`. The first recurrence over all stored DPs is
therefore at `s + lambda`. Every DP at index below `s + lambda` that is not a
recurrence was stored there, so the lookup finds the entry of index `s`.

**Lemma 2 (bracket).** Let `s'` be `sp`, the index of the entry preceding `s`
(or 0 for the anchor `x_0`). If `mu >= 1` then `s' < mu`. If `mu = 0` then
`s' = 0 = mu` and the algorithm returns FAILURE at the `A == B` test.
*Proof.* A stored entry with index in `[mu, s)` would be a DP at index at least
`mu` smaller than `s`, contradicting the choice of `s`. If no entry precedes
`s`, `s' = 0`, which is below `mu` exactly when `mu >= 1`. If `mu = 0`, then
`A = x_0` and `B = x_lambda = x_0`.

**Lemma 3 (preparation).** `B = x_{s'+lambda}`.
*Proof.* If `tau = s' + lambda >= s`, the entry `j*` is a stored DP with index
in `[s, tau]` (the entry of index `s` qualifies), and walking `tau - index(j*)`
steps from its value reaches index `tau`. Every DP index in `[s, tau]` is
stored, since `tau < mu + lambda = rho` when `s' < mu`. If `tau < s`, walking
`lambda` steps from `x_{s'}` reaches index `s' + lambda`.

**Lemma 4 (output).** If `mu >= 1`, the lockstep stops at its iteration
`q = mu - s' - 1 >= 0` with `A = x_{mu-1}` and `B = x_{rho-1}`, and returns two
distinct messages with equal full digests.
*Proof.* At iteration q, `A = x_{s'+q}` and `B = x_{s'+lambda+q}`. Their images
agree exactly when `s' + q + 1 >= mu`. The first such q is `mu - s' - 1`. Then
`A != B` because both indices are below `rho` and differ by `lambda >= 1`, so
`m(A, r) != m(B, r)`, while `H(m(A, r)) = f_r(A) = f_r(B) = H(m(B, r))`. The
final recomputation repeats the check from the IV and cannot fail after a true
match.

**Lemma 5 (counters).** Call a run a maximal block of consecutive non-DP
values among `x_0, ..., x_{rho-1}`. Suppose `rho <= k`, `mu >= 1`, the cycle
contains a DP, every run has length below `L`, and at most `K` DPs occur among
`x_0, ..., x_{rho-1}`. Then no counter or capacity check fails, so the
algorithm succeeds.
*Proof.* The values `x_mu, ..., x_{s-1}` lie within one run, so `s - mu < L` and
detection happens at `t = rho + (s - mu) < k + L = TCAP`. Stored entries are
distinct first-lap DPs, at most K of them, so the table never overflows before
detection. Lockstep needs `mu - s' <= s - s' <= L` iterations, because the
values strictly between `s'` and `s` lie within one run (as do `x_0, ..., x_{s-1}`
when `s' = 0` is the anchor). In the case `tau < s`, preparation needs
`lambda < s - s' <= L` steps. In the case `tau >= s`, let `n` be the next DP
index after `index(j*)`. If `n < rho`, it is stored and exceeds `tau`, so
`steps < n - index(j*) <= L`. Otherwise the next DP occurrence is the detection
index `s + lambda`, so
`steps < (rho - 1 - index(j*)) + 1 + (s - mu) < L + L = 2L`.

## 5. The declared premise RM-WALK

**Statement.** Draw `r` uniformly from `{0,1}^128` and `x_0` uniformly from
`{0,1}^256`, independently, and run the walk of the fixed target's `f_r`. The
probability of the success event of Lemma 5 is at least its value when `f_r` is
replaced by a uniformly random function on `{0,1}^256` that is independent of
`x_0`. The claim tolerates a shortfall: Section 6 bounds the ideal value above
`0.4249`, so the claim survives if the real probability is at least the ideal
value minus `0.0349` (about 8% relative).

**Why the suffix r is drawn fresh.** A single fixed map has one functional
graph, and its cycle and tail lengths are not concentrated: different maps give
noticeably different probabilities over the start point alone. Drawing `r`
makes the success probability an average over `2^128` maps `f_r`. If `H` behaved
as a uniformly random function on 48-byte messages, these maps would be
independent uniformly random functions, `RM-WALK` would hold exactly, and the
average would concentrate at the ideal value. The premise is the usual
random-mapping assumption of generic collision search, applied to this
averaged family rather than to one map.

**Known structure.** For each fixed `r`, the first sixteen rounds act
bijectively on `x`. From the fixed IV, the state after round 7 determines W0..W7
uniquely: the state words give `a_5..a_8` and `e_5..e_8`, and each relation
`e_{t+1} = a_{t+1} - T2(a_t, a_{t-1}, a_{t-2}) + a_{t-3}` recovers one earlier
`a`, after which each `W_t` follows from its round equation. Rounds 8..15 use
the fixed words W8..W15, so each is a fixed permutation of the state. A
16-round analogue of `f_r` would therefore be a permutation plus a constant
feed-forward: it has no collisions at all, and this walk would always end with
`mu = 0`. The 21 further rounds use the expanded words W16..W36, which depend on
`x` through the message schedule and break that bijectivity. No property is
known to the author that makes the 37-round map injective or permutation-like.
This structure is why `RM-WALK` is declared rather than assumed silently.

**Evidence.** Section 8 runs a scaled analogue of this algorithm on 12-, 14-
and 16-bit truncations of the real 37-round digest, with the same fresh-suffix
randomization and a slightly smaller budget ratio, `k / 2^(n/2) = 65/64`. The organizer
recomputes every returned event. The truncations test the random-mapping
statistics of the target's digest bits and the implementation. They cannot test
the full-width bijectivity risk above: truncating any map, permutation or not,
gives a map that behaves like a random one. That risk rests on the structural
argument alone.

## 6. Success probability under RM-WALK

Replace `f_r` by a uniformly random function and sample it lazily: each new
argument receives a fresh uniform value. With `Z_0, Z_1, ...` iid uniform on
`{0,1}^256` and `N = 2^256`, the walk satisfies `x_t = Z_t` for all `t <= rho`,
where `rho` is the first repeat index of the Z sequence. Every event of Lemma 5
is an event of this Z sequence. Failure is bounded by five terms.

1. *Late repeat.* `rho > k` means `Z_0, ..., Z_k` are distinct, with probability
   `prod_{j=1..k} (1 - j/N) <= exp(-k(k+1)/(2N)) < exp(-x)`, where
   `x = k^2/(2N) = 289/512`. Since `e^x` exceeds its degree-11 Taylor sum `S`,
   this term is below `1/S < 0.568672`.
2. *Start on the cycle.* `P(rho = t, mu = 0) <= P(Z_t = Z_0) = 1/N`, so
   `P(mu = 0, rho <= k) <= k/N = 17 * 2^-132 < 2^-127`.
3. *Cycle without a DP.* Given `rho = t`, the values `Z_0, ..., Z_{t-1}` are a
   uniformly random sequence of distinct values, and `mu` is uniform on
   `{0, ..., t-1}` independently of them, because the repeat `Z_t` is uniform
   over the `t` earlier values. A fixed set of `l` positions holds no DP with
   probability at most `(1 - theta)^l`, since sampling without replacement only
   lowers it. Averaging over `lambda = l` uniform on `{1, ..., t}` gives at most
   `(1/t) * sum_{l>=1} (1 - theta)^l < 1/(theta t)`. Hence
   `P(no DP on cycle, rho <= k) <= P(rho <= t0) + 1/(theta t0)` for any `t0`.
   With `t0 = 2^124`, `P(rho <= t0) <= t0(t0+1)/(2N) = 2^-9 + 2^-133` and
   `1/(theta t0) = 2^-8`, so this term is below `0.0058594`.
4. *Long run.* A run of length at least L inside `Z_0, ..., Z_{k-1}` starts at
   position 0 or right after a DP, and is followed by L non-DP values. Hence its
   probability is at most `(1 + k theta)(1 - theta)^L <= 4353 * e^-16`, using
   `k theta = 4352` and `theta L = 16`. Bounding `e^16` below by its degree-59
   Taylor sum gives a value below `0.00048987`. When `rho <= k`, the first-lap
   runs lie inside this prefix.
5. *Table overflow.* The DPs among `Z_0, ..., Z_{k-1}` are binomial with mean
   `k theta = 4352`. By Markov's inequality on `2^X`, at least `K + 1 = 8193` of
   them has probability at most `(1 + theta)^k / 2^8193 <= e^4352 / 2^8193`,
   and `e^4352 < 3^4352 < 2^6898` makes this below `2^-1295`.

Summing, failure is below `0.568672 + 2^-127 + 0.0058594 + 0.00048987 + 2^-1295`,
so success exceeds `0.42497 > 0.39`. Every comparison above was verified
in exact rational arithmetic; the only analytic inputs are the series
lower bounds `e^y > sum_{i<m} y^i/i!` for `y > 0`. The bound is
over the algorithm's fresh coins `(r, x_0)` for the fixed target, as required
by the cost model, with `RM-WALK` transferring the ideal-function calculation.

## 7. Time accounting

**Machine model.** Classical 256-bit word RAM, as in `collision-frontier-v5`.
There is a fixed register file of 32 words, counted in memory below. Every
executed instruction is one primitive: a load, a store, an addition or
subtraction, a bitwise operation, a shift, a comparison, a conditional branch,
or a random word. A comparison and the branch on its result count as two
primitives. Unconditional jumps are branches on a fixed true condition and also
count one. One call of the priced primitive covers the schedule expansion
through W36, rounds 0..36 and the feed-forward of one block, at cost 1. Its
interface reads 8 chaining words and 16 block words from fixed memory regions
and writes 8 result words, one 32-bit value per RAM word. Those 32 accesses and
the call and return branches are charged separately: 34 primitives per call.
Each ordinary primitive costs `1/C` with `C = 2644`.

**One walk step**, worst case, with the current x as eight words in registers:

| Work | Primitives |
| --- | ---: |
| DP test: three word-is-zero tests, one shift and test of the fourth word | 9 |
| Step-limit test against TCAP | 2 |
| Primitive call: interface accesses, call and return | 34 |
| Copy the 8 result words to registers and to block words W0..W7 | 16 |
| Index increment and loop branch | 2 |
| Total, charged as 64 | 63 |

The IV region and block words W8..W15 are written once per run, because `r`
is fixed for the run, and the primitive does not modify its input regions.
A preparation step is the same step without the DP test, also charged 64.

**One lockstep iteration**: two primitive calls (68), loading and comparing
the two 8-word results (32), copying both results back to the two block regions
(16), and the iteration counter and branches (3). That is 119, charged as 160.

**DP events.** A DP is packed into one word with 7 shifts and 7 ORs. The table
is scanned linearly; each entry costs a load, comparison, branch, pointer
update, end test and branch, so 6 primitives. An insertion costs a few stores
and pointer updates. Each event is charged `6K + 64`. There are at most `K + 1`
events, because the `(K+1)`-th insertion attempt fails. Locating `s'` and `j*`
scans at most `2K` further entries, charged `12K`, and unpacking `base` into
eight words costs 24.

**Fixed work.** Loading the program and constants takes at most `2^13` words
at 6 primitives each (load, store, two pointer updates, end test, branch), which
is 49,152. Everything else happens once per run and is charged at most `2^12`:
drawing `r` and `x_0`, setting the constant regions, the arithmetic after
detection, unpacking `vp` into `A`, switching between the two lockstep block
buffers, and the final recomputation's marshaling. Both together are charged
`2^16` primitives.

**Totals.** Primitive calls are bounded by the walk (`TCAP`), preparation (`2L`),
lockstep (`2L`) and final check (2):

```
H <= k + 5L + 2
W <= 64 (TCAP + 1) + (K + 1)(6K + 64) + 12K + 24 + 64 * 2L + 160 L + 2^16
T  = H + W / 2644
```

With `k = 68 * 2^122` and `L = 2^120`, `T / 2^128 = 1.1082699...` and
`log2 T = 128.14831`. The claim `time_log2 = 128.15` is rounded up, and
`T^100 < 2^12815` was checked in exact integer arithmetic. These bounds hold on
every random tape: there is no expected-time tail and no restart loop.
Preprocessing, the program and constant loading, is at most
`2^16 / 2644 < 25 < 2^5` units and is already inside T; it is reported as
`preprocessing_log2 = 5`.

## 8. Experimental evidence

Three declared `python-message-pairs-v1` experiments (`rhodp-n12`, `rhodp-n14`,
`rhodp-n16`) run a scaled analogue of the algorithm of Section 3 on the real
target, with the walk state reduced to n bits. Each organizer trial derives, from its seed, a 32-byte
template, a 16-byte suffix R and a start value. The walk iterates
`g(x) = top n bits of H(enc(x) || R)` on n-bit values, where `enc(x)` flips bits
of the template according to x (bit i of x goes to bit `i div 8` of word
`i mod 8`), so every walk step evaluates the full 37-round digest of a 48-byte
message. The experiments use the budget ratio `k = (65/64) * 2^(n/2)`. They
were designed when the full attack used that ratio; the final attack uses the
larger `17/16`, so the experiments test a slightly stricter budget:

| Experiment | n | k | DP bits | L | K | Ideal success |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `rhodp-n12` | 12 | 65 | 1 | 32 | 256 | 0.375 |
| `rhodp-n14` | 14 | 130 | 1 | 32 | 256 | 0.388 |
| `rhodp-n16` | 16 | 260 | 2 | 64 | 512 | 0.384 |

The scaled analogue differs from the full attack in four ways:

- The walk is cut off at k rather than `k + L`, so any trial that succeeds
  under that cut-off also succeeds under the full rule on the same coins.
- Distinguished points are dense (`theta` is 1/2 or 1/4), so a walk stores
  about 32 to 65 of them instead of about 4352. Only `theta L = 16` and the
  table's headroom are preserved.
- x changes only the two lowest bits of each message word W0..W7, over a
  seed-dependent random template, rather than all 256 bits.
- The iteration reads only the top n bits of digest word 0.

The ideal rates were computed by the author by simulating the same scaled
rules on lazily sampled ideal random functions: 200,000 runs per width with
Python's `random.Random(20261025)`, giving a standard error of about 0.0011.
That simulator is not part of the package; an independent advisory re-simulation
agreed within its error. The decision rule is fixed in advance. Fewer than
78 (n12), 81 (n14) or 80 (n16) successes out of 256 counts against `RM-WALK` for
these truncations, or reveals a defect in the implementation. These are exact
binomial cut-offs at the one-sided 1% level for each experiment, not corrected
for testing three widths. The organizer checks each returned pair as a `digest-xor-mask`
event on the top n digest bits, using its own target implementation, so a wrong
hash implementation in the program would produce failed checks rather than
successes.

**Local rehearsal (disclosed, not official).** Before submission the author
ran these experiments through the organizer's `run_experiments` executor in
Docker with the public seed, the pinned limits and the organizer's own event
check. The isolation flags were unchanged, but the platform was swapped to the
arm64 build of the same Python 3.12.12 release, because emulating the pinned
amd64 image on the author's machine exceeded the 20-second timeout. The two
fresh runs per experiment were byte-identical. Results: `rhodp-n12` 98/256
(0.383), `rhodp-n14` 96/256 (0.375), `rhodp-n16` 103/256 (0.402), with no
repeated pairs. All three are above their cut-offs and within one standard
deviation (about 0.030) of their ideal rates. They show no visible trend with
width, though three points at this precision cannot rule one out. A sample of
256 cannot resolve a shortfall as small as the 0.0349 tolerance of Section 5;
it can exclude only much larger departures. An earlier
rehearsal of a variant using 32-byte messages and no suffix gave 104, 99 and
107. Section 5 explains why the fresh-suffix family replaced it; the
change was made for the analysis, not for its counts. The official
remote report supersedes these numbers. Python integers are
platform-independent, so it is expected to reproduce them.

**Scope of this evidence.** It is a finite sample at widths 12 to 16 under
public, SHAKE-derived seeds. Independence between trials is itself heuristic.
It supports the random-mapping statistics of truncated r37 digests and the
correctness of the algorithm's control flow. The extrapolation to 256 bits is
the premise itself, not a consequence of the data.

## 9. Memory, code and advice

| Item | Bytes, at most |
| --- | ---: |
| DP table: 8192 entries of two 32-byte words | 524,288 |
| Program and public constants (IV, 37 round constants, masks) | 262,144 |
| Registers, primitive interface regions, two block buffers, counters, output | 65,536 |
| Total | 851,968 |

`851,968 < 2^20`, so `memory_log2_bytes = 20` and the scalar memory term is
zero. The allowances are generous: the program is a few hundred instructions
and the scratch area is under 100 words. Indices are below `2^130` and fit a
word. No random tape is stored; `r` and `x_0` are the only random words drawn.
The program is uniform: it uses only public profile constants and the fixed
parameters stated here. There is no target-dependent advice and no precomputed
collision. `nonuniform_advice_log2_bytes = 0` is an upper bound of one byte,
covering zero.

## 10. Limitations and sensitivity

- `RM-WALK` is a heuristic. If the 37-round map were permutation-like for most
  suffixes, the walk would end with `mu = 0` and fail. Section 5 explains why
  that is not expected, but it is not proved, and Section 8 cannot test it.
- The time bound uses the register-machine accounting of Section 7. Under a
  coarser lowering, at most 8 primitives per elementary statement (512 per step
  and 1280 per lockstep iteration), the same algorithm bounds at
  `log2 T = 128.370`. If memory traffic inside the priced compression were also
  charged, at an allowance of 200 primitives per call, the bound is `128.251`.
  Both stay below `2^128.37`.
- Success is a probability over fresh coins, above 0.4249 under the premise.
  It meets the 0.39 requirement as long as the real probability falls short of
  the ideal-function value by less than 0.0349. The experiments of Section 8
  cannot resolve a shortfall that small. The algorithm does not retry; a larger
  shortfall would need a larger budget k, at roughly 0.04 bit of time per extra
  0.02 of success near this point.
- No witness, executed full search, novelty or improvement over the nominal
  reference is claimed.

## 11. Sources

- NIST FIPS 180-4, Sections 5.1.1, 5.3.3 and 6.2.2: padding, IV, schedule and
  feed-forward. The organizer profile fixes the reduction to 37 rounds.
- J. M. Pollard, "A Monte Carlo method for factorization", BIT 15 (1975): the
  rho walk on a function's graph.
- P. C. van Oorschot and M. J. Wiener, "Parallel collision search with
  cryptanalytic applications", Journal of Cryptology 12 (1999): distinguished
  points for low-memory collision search.
- P. Flajolet and A. M. Odlyzko, "Random mapping statistics", EUROCRYPT '89:
  the tail and cycle statistics behind the random-mapping premise.

These are context only. Every step needed to assess the claim is given above.
