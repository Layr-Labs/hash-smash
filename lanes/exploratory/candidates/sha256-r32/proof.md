# SHA-256, first 32 rounds: exploratory distinguished-point birthday search

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
separately reported resource bound.

This package is bound to `sha256-r32-exploratory`, target profile
`sha256-r32-prefix-v1`, and cost model `collision-frontier-v5`. It gives a
classical probabilistic algorithm with worst-case charged time below
`2^128.02`, peak memory below `2^112` bytes, and algorithmic success
probability at least `0.39` under one explicitly declared score-critical
heuristic. It is a generic birthday construction; no full-scale execution,
concrete collision certificate, differential weakness, or improvement over an
established attack is claimed. All necessary arguments appear below.

The required identifier `sha256-r32-nominal-v2` names an organizer display
reference (nominal exponent 128 for 256-bit targets), not an established
attack, qualified baseline, or security bound. The claimed scalar `128.02`
sits just above that number only because every instruction is charged.
Readiness is a request for review, not a claim of AI qualification or
acceptance.

Method: P. C. van Oorschot and M. J. Wiener, "Parallel Collision Search with
Cryptanalytic Applications", Journal of Cryptology 12(1):1-28, 1999,
single-processor distinguished-point (DP) search. Prior HashSmash packages
apply the same generic method to sibling targets (for example the
`sha3-256-r6-exploratory` DP package at 128.014 and the `sha256-r32`
DP tickets at 128.01-128.02). This package redoes only the
target-specific parts for 32-round SHA-256: message map and padding,
per-step operation count at `C=2224`, and total `log2`. It adopts no
unpromoted solver file; any resemblance to concurrent tickets is convergence
on the textbook method.

## 1. Exact complete-message target

The attack uses only messages of exactly 32 bytes, a subset of the profile's
finite-byte-string domain with bit length less than `2^64`. For a 256-bit
word `x`, define `msg(x) = BE32(x)`: exactly 32 bytes, most significant byte
first, including zeros. This map is injective. Padding under FIPS 180-4 for a
256-bit (32-byte) message is deterministic and fits in the same block:

- Parse the 32-byte message as eight big-endian 32-bit words `W[0..7]`.
- Set `W[8] = 0x80000000`, `W[9..14] = 0`, `W[15] = 0x100` (bit length 256).
- The single 64-byte block `B = W[0..15]` is processed once from the fixed IV.

The eight-word initial state, in order, is
`(6a09e667, bb67ae85, 3c6ef372, a54ff53a, 510e527f, 9b05688c, 1f83d9ab,
5be0cd19)`. Compression `C32(S,B)` is exactly the 32-round function of
Section 1 of the organizer baseline: sixteen input words, expansion
`W[t] = W[t-16] + sigma0(W[t-15]) + W[t-7] + sigma1(W[t-2])` for `t=16..31`
with the standard `sigma0/sigma1/Sigma0/Sigma1/Ch/Maj` and constants `K[0..31]`
at original indices, 32 steps
`T1 = h + Sigma1(e) + Ch(e,f,g) + K[t] + W[t]`,
`T2 = Sigma0(a) + Maj(a,b,c)`,
`(a,b,c,d,e,f,g,h) = (T1+T2, a, b, c, d+T1, e, f, g)`,
then componentwise feed-forward `S + (a..h)` modulo `2^32`. Full
specification, constants, and rotation definitions are retained from the
baseline and the target profile; nothing is renumbered, truncated, or given a
chosen IV. Define `H(x)` as the concatenation, in state order and big-endian
encoding, of all eight words of `C32(IV,B(x))`. This is the full 256-bit
digest of the complete 32-byte message. Thus `H` is exactly the fixed-IV,
first-32-round, padded complete hash required by `sha256-r32-prefix-v1`.

Define `f(x)` as the 256-bit integer value of `H(x)` in big-endian order.
Then `BE32(f(x))` is exactly the digest bytes of `msg(x)`. Since `msg` is
injective, any `x != x'` with `f(x) = f(x')` yields two distinct 32-byte
messages with byte-for-byte equal complete hashes: an ordinary collision.
There is no second block, no chosen IV, no free-start state, no truncation,
and no near-collision substitute.

Reference: `verifier/hash_functions.py:digest(m, "sha256", 32)`. The
construction above agrees with it by definition; Section 4 checks the
message-to-block packing explicitly.

## 2. Distinguished-point algorithm

A selected `C32` compression costs one target-compression unit. Each other
primitive 256-bit word operation (load/store, add/sub mod `2^256`,
AND/OR/XOR/NOT, shift/rotation, comparison, conditional branch, independent
uniform random word) costs `1/C` with `C = 2224` for `sha256-r32` under v5.
Instruction fetch is not a model primitive and is not separately charged;
every data-word operation listed below is charged.

Registers: `H0..H7` hold chaining words and `W0..W15` hold block words as
dedicated registers. The `COMP32` call replaces `H` by the 32-step
compression with feed-forward, costs 1 unit, and is charged 1 extra ordinary
operation to issue. We conservatively assume it may overwrite `W0..W15` (an
in-place schedule), so IV/padding words are rewritten every evaluation. This
matches `docs/RESCORING.md`, which counts data-word operations including
message expansion and feed-forward and excludes memory traffic and
serialization from the reference normalization. All attack memory traffic
remains charged below as explicit loads/stores where stated; the reference
normalization exclusion does not remove attack work.

Constants: `theta = 2^-32`. A point is distinguished (DP) iff its low 32
output bits (word `H7`) are zero. Maximum chain length `L = 2^40`.
Evaluation budget `K0 = 65300 * 2^112`. Record cap `Dcap = 2^98`.
All counters fit a 256-bit word.

```
CHAIN(start):
  x = start  # 256-bit word
  for j = 0..L-1:
    y = f(x)            # 1 COMP32 + per-evaluation wrapper below
    if y.low32 == 0: return (DP=y, start=start, len=j+1)
    x = y
  return ABANDONED       # chain gave up, counted in budget

Main (one run, no restart):
  setup fixed IV/padding registers, table base, budget counter (<=16 ops)
  total_evals = 0
  stored = 0
  loop:
    if total_evals >= K0 or stored >= Dcap: break
    s = UniformWord()              # fresh independent coins
    total_evals += 1
    (res, chain_evals) = walk from s up to L steps, testing DP after each step
    total_evals += chain_evals - 1  # first evaluation already counted above
    if res is ABANDONED: continue   # budget already charged
    # res is a DP triple (dp, start, len)
    lookup dp in table (depth-224 structure below)
    if dp already stored with (start0, len0):
      RELOCATE the two chains from start and start0 to their merge point
      let (a,b) be the two distinct predecessors (Section 3)
      OUTPUT: recompute H(msg(a)), H(msg(b)) by two full reference digests,
        check a != b and digests equal on all 256 bits, emit (msg(a),msg(b))
        and halt with success
      else (same chain / same start collision): discard current DP and continue
    else:
      store (dp -> (start,len)) if stored < Dcap, stored += 1, continue
  halt with FAIL
```

Per evaluation wrapper (unrolled accounting, charged every step): 8 IV-word
writes, 8 padding-word writes (`W8..W15`), 1 call issue, 8 moves `H -> W0..W7`
(the next message words are exactly the eight output words), and a DP test
after every evaluation (compare `W7/H7` with 0 plus branch). That is 27
operations plus amortized loop control `3/16` per evaluation when the walk
loop is unrolled 16 times, for `435/16 = 27.1875` ordinary operations per
evaluation. Block control (counter, bound test, jump) is the `3/16`.

`CHAIN` control beyond evaluations: budget test, one `RAND`, walk setup and
abandon handling, at most 19 operations per chain. `DPFOUND` (lookup/insert):
depth-224 binary structure on the 224 high DP bits, at most
`23 + 224*17 + 9 = 3840` operations per DP-terminated chain (loads,
compares, branches, stores). `RELOCATE`: re-walk at most two length-`L`
segments, charged as evaluations (each `1 + 80/2224` units to cover walk
overhead generously). `OUTPUT`: two whole reference digests (2 units) plus
at most 300 ordinary operations for comparisons, distinctness check, and
writing at most 64 message bytes plus serialization.

The table holds at most `Dcap = 2^98` entries. Each entry is
`(dp:1 word, start:1 word, len:1 word)` plus hash-bucket linkage charged in
the memory bound. No unbounded allocation, no recursion, no uncharged
library sort. The run always charges every evaluation including failures and
abandoned chains; there is no success-amplification outside this run.

## 3. Correctness

Each `f` evaluation is exactly one complete single-block hash by Section 1.
`msg` injectivity means any distinct-predecessor equality under `f` is an
ordinary collision. The walk follows deterministic iteration of `f`:
`x_{k+1} = f(x_k)`. If two stored chains share a DP value, re-walking both
from their starts reaches the first index where they agree; the immediate
predecessors at that index are distinct inputs with equal `f`-images unless
the two chains are the same chain (same start and overlapping suffix), in
which case the pair is discarded and the search continues. Standard
van Oorschot-Wiener analysis: contact (two evaluations landing on the same
value) with no bad event yields, through `RELOCATE`, two distinct
predecessors. `OUTPUT` recomputes both complete digests from the fixed IV
and requires message inequality and full 256-bit digest equality before
returning. Every successful return therefore satisfies the exact profile's
ordinary-collision relation. Conversely, on the good event of Section 6 the
algorithm returns. All resource bounds below hold for every coin choice
without any heuristic.

## 4. Message packing check (analytic, not an organizer experiment)

For all 32-byte inputs, `W[0..7]` are the message words, `W[8]=0x80000000`,
`W[9..14]=0`, `W[15]=0x100`. Bit length 256 is `0x100`, stored big-endian in
the last word. Total padded length is exactly one 64-byte block. No second
block, no length-overflow branch, no variable-length loop is needed. This is
stated so the cost reviewer can verify the 8+8 wrapper count: eight message
moves and eight fixed padding writes per evaluation.

## 5. Charged time

`H_calls` counts `COMP32` calls; `W` counts ordinary operations. Compression
internals are inside `H_calls` and never also in `W`.

- Fixed setup: at most 16 ordinary operations (below one unit, included).
- Main evaluations: at most `K0 + L + 2` `COMP32` calls. Reason: at most
  `K0` budgeted evaluations, plus boundary completion of the final chain
  (at most `L`), plus 2 for `OUTPUT`. Each carries at most 27.1875 ordinary
  wrapper operations.
- Per-chain control: number of chains is deterministically bounded by
  `Dcap + K0/L < 2^98 + 65300*2^72 < 2^99` (DP terminations at most the
  record cap; abandoned chains at most budget divided by `L`). At most 19
  operations each, so below `19 * 2^99 < 2^104` operations.
- `DPFOUND`: runs only on DP-terminated chains (at most `Dcap`), at most
  3840 operations each, so below `3840 * 2^98 < 2^110` operations.
- `RELOCATE`: at most `2L = 2^41` evaluations, charged as
  `3 * 2^40 * (1 + 80/2224)` units generously (covers walk plus control).
  This is below `2^43` units.
- `OUTPUT`: 2 units plus 300 operations, at most once.

Hence on every choice of coins:

```
H_calls <= K0 + L + 2
W <= K0*27.1875 + 2^110 + 2^104 + 300 + 16
T = H_calls + W/2224
  <= K0*(1 + 27.1875/2224) + (L + 2) + (2^110 + 2^104 + 316)/2224
```

With `K0 = 65300 * 2^112`, `log2(K0) = 127.99479537...`,
`1 + 27.1875/2224 = 1.01222459...`, `log2(1.01222459...) = 0.01752943...`,
so `log2(K0 * 1.01222459...) = 128.01232480...`. The additive remainder is
below `2^100` units, i.e. below a factor `1 + 2^-28` on the leading term.
Therefore for every run:

```
T < K0 * 1.0122246 * (1 + 2^-28) < 2^128.0124 < 2^128.02.
```

Concretely `T <= 2^128.0124` in target-compression units; the submitted
`time_log2 = 128.02` retains more than `0.007` bits of slack. This prices
phase counts (hashing plus all table, control, relocation, and verification
work), preprocessing, failed trials, randomness, and the required success
budget. There is one finite run, so no restart or expected-time truncation
assumption. The bound uses `C = 2224` from `collision-frontier-v5` for
`sha256-r32`.

Sensitivity (all still below the organizer 136 baseline):

| reading | per-eval charge | bound |
| --- | --- | --- |
| claimed | 27.1875 ops | 2^128.0124 -> claim 128.02 |
| 35 ops per eval (extra loads) | 35 | about 2^128.017 |
| 80 ops per eval (paranoid traffic) | 80 | about 2^128.037 |
| whole compression per message (rejects wrapper detail) | C=2224 as 1 unit + 0 | about 2^128.00 + small |
| merge-sort birthday at 2 blocks | - | 2^136 (baseline) |

Even at 80 ordinary operations per evaluation the bound stays below 128.04,
far below 136. The scalar is an accounting result, not a weakness of SHA-256.

## 6. Success probability under H-RF

Probability space: fresh independent uniform 256-bit words from the RAM
primitive (one per chain start; walk steps are deterministic given starts).
The hash is fixed. Only this section uses heuristic H-RF: fresh `f`
evaluations behave as independent uniform values on `{0,1}^256` for
first-contact and bad-event estimates. Resource bounds and correctness need
no heuristic.

Let `N = 2^256`. Consider the first `K0` evaluations in order. Under H-RF the
contact probability (some two evaluations agree) satisfies the standard
birthday lower bound:

```
Pr[contact in K0] >= 1 - exp(-K0*(K0-1)/(2N)).
```

With `K0 = 65300 * 2^112`, `K0^2/(2N) = 65300^2/2^33 = 0.49640540...`,
which exceeds `-ln(0.61) = 0.49429632...`. Hence
`Pr[contact] >= 1 - exp(-0.4963...) > 0.39128`.

Bad events (all bounded under H-RF except where stated exactly):

- `B1`: a chain start lands on a previously visited point. At most
  `K0^2/(2N)`-style union bound gives `< 4.63e-10`; more directly the number
  of starts is below `2^99`, so `Pr[B1] < 2^99 * K0/N < 2^-44`. We charge
  the loose `4.63e-10`.
- `B2`: first contact involves a start or the current chain's own cycle
  (no distinct-predecessor pair). Same order as `B1`, `< 2.32e-10`.
- `B3`: a run of `L/2` consecutive non-DP outputs when a DP was overdue in a
  way that forces abandonment of the contacting chain. Under H-RF,
  `(1-theta)^{L/2} = (1-2^-32)^{2^39} < exp(-2^7) = 2^-184.5`. Summed over at
  most `2^99` chains this is below `2^-85`. We charge `2^-88` conservatively.
- `B4`: record cap overflow (more DPs than `Dcap`). Expected DPs are
  `K0*theta = 65300*2^80 < 2^96`. By Markov/Chernoff the overflow beyond
  `2^98` is below `2^-97`. We charge a loose `2^-90`.

Total bad-event mass is below `7.0e-10 < 2^-30`. Therefore:

```
Pr[success] >= 0.39128 - 7.0e-10 > 0.39127 > 0.39.
```

The declared `0.39` keeps more than `0.0012` of allowance. Input repeats are
included in the contact analysis (equal inputs give equal outputs and are
resolved by `RELOCATE`/discard logic, never counted as collisions). The
`0.39` figure is an algorithmic success lower bound under H-RF, not
confidence in the proof or in any review.

## 7. Memory, preprocessing, advice

Peak storage (deterministic layout, cap `Dcap = 2^98`):

- Table: at most `2^98` entries of `(dp, start, len)` = 3 words = 96 bytes
  each, i.e. below `96 * 2^98 < 2^105` bytes, plus bucket headers below
  `2^100` bytes. Even with a factor-16 hash-table slack this is below
  `2^109` bytes.
- Walk scratch, counters, IV/padding registers, message buffers, and
  verification state: below `2^20` bytes.
- Code and constants (loops over pseudocode, no unrolling of `K0` or `L`;
  all 32 round constants and eight IV words): below `2^20` bytes.

Accordingly `M < 2^110` bytes comfortably; the submitted
`memory_log2_bytes = 112` retains more than two bits of slack. Memory is
reported only under v5 and does not affect the scalar.

`preprocessing_log2 = 0`: fixed setup is at most 16 ordinary operations,
cost `16/2224 < 1` unit, already inside `T`. No offline search. Array
allocation means choosing address intervals, not invoking an uncharged
allocator; table writes during the walk are charged per chain above.

No nonuniform advice is used, so actual size is zero bytes. The schema
requires a finite nonnegative logarithm; `nonuniform_advice_log2_bytes = 0`
means a conservative upper bound of one byte, not the literal logarithm of
zero and not permission to hide uniform code. Uniform code is charged in `M`
and its initialization in `T`.

No `data_log2` is declared (optional legacy metadata). If counted as bytes
of complete padded inputs, at most `K0 + L + 2 < 2^129` evaluations of at
most 64 bytes each fit below `2^135` bytes; this is already charged in `T`
and needs no separate bound.

## 8. Heuristic, evidence, and limitations

`heuristics` contains exactly one entry `H-RF` (score-critical, success bound
only). Statement, role, scope, extrapolation, evidence references
(`proof:6`, `proof:7`), and limitations are in `claim.json` and elaborated
here. Cryptanalysis and cost depend on no other heuristic: no ideal-hash
balance beyond contact statistics, no differential-trail independence, no
seed expansion, no empirical extrapolation from small cases is used for the
bound. The certificate manifest is valid and empty. No experiment manifest
or program is supplied because no empirical premise beyond the stated
analytic heuristic is used; `not_requested` is therefore the correct
experiments status. A reduced toy run would not strengthen the full-size
contact arithmetic and is not substituted for it.

Limitations: H-RF is a model of a fixed function, tested here only by
analytic comparison to textbook DP behavior, not by organizer-executed
scaled runs. The margin above 0.39 is about 0.0012; a contact shortfall
`delta` would need about `2.4*delta` more bits of budget. Memory (up to
`2^112` bytes) far exceeds a rho walk's and rules out any Pareto claim.
Abstract resources are enormous but fit the stated RAM and message domains.
This is a constant-factor accounting improvement (single block, no sort),
not a cryptanalytic weakness of SHA-256. Exploratory `plausible_not_refuted`
is neither proof nor human acceptance.

## 9. Source and accounting note

This is an independent DP accounting package for `sha256-r32-prefix-v1`. The
complete-hash definition follows the organizer baseline; the four-word
records, merge sort, `q=2^129`, and scalar 136 are replaced by the
single-block DP construction above. It needs fresh review and inherits no
earlier qualification. The per-evaluation count (27.1875) and total
(`2^128.0124`, claim `128.02`) are the tightest bounds supported here under
v5 prices; the judge checks the bound and does not automatically tighten it.
If a reorg changes scoring policy, the preserved-score rule applies.

## 10. Commands

```sh
yukon setup --track sha256-r32-exploratory
python3 scripts/local_tracks.py show sha256-r32-exploratory
python3 scripts/local_tracks.py check sha256-r32-exploratory
```

`check` reports `mechanically_valid`, `ready`, `certificates_verified: 0`.
No provider key is used locally; remote judging supplies review credentials
in its isolated job. No participant command is executed on the host.
