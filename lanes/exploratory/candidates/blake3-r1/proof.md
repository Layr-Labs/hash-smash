# BLAKE3, 1 prefix round: exploratory distinguished-point birthday search

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
separately reported resource bound.

This package is bound to `blake3-r1-exploratory`, target profile
`blake3-r1-prefix-v1`, and cost model `collision-frontier-v5`. It gives a
classical probabilistic algorithm with worst-case charged time below
`2^128.3`, peak memory below `2^112` bytes, and algorithmic success
probability at least `0.39` under one explicitly declared score-critical
heuristic. It is a generic birthday construction; no full-scale execution,
concrete collision certificate, differential weakness, or improvement over an
established attack is claimed. All necessary arguments appear below.

The required identifier `blake3-r1-nominal-v2` names an organizer display
reference (nominal exponent 128 for 256-bit targets), not an established
attack, qualified baseline, or security bound. The claimed scalar `128.3`
sits just above that number only because every instruction is charged.
Readiness is a request for review, not a claim of AI qualification or
acceptance.

Method: P. C. van Oorschot and M. J. Wiener, "Parallel Collision Search with
Cryptanalytic Applications", Journal of Cryptology 12(1):1-28, 1999,
single-processor distinguished-point (DP) search. This is an independent
generic package for the 1-round BLAKE3 target; it adopts no unpromoted solver
file. Deterministic 1-round collision tickets with scores near 0-4 are noted
as untrusted awaiting-review work and are not used here; this package is a
reviewable generic fallback that improves the promoted 149 baseline by
removing the sort.

## 1. Exact complete-message target

The attack uses only messages of exactly 32 bytes, a subset of the profile's
finite-byte-string domain with bit length below `2^64`. For a 256-bit word
`x`, define `msg(x) = LE32(x)`: exactly 32 bytes, least significant byte
first, including zeros. This map is injective.

For a 32-byte input, BLAKE3 uses one chunk with one block. Per
`verifier/blake3.py:blake3(m, 1)` and the target profile: chunk counter 0,
block words from `struct.unpack("<16I", msg.ljust(64, b"\0"))` (eight message
words followed by eight zero words for loading; true block length encoded
separately as 32), chaining value `cv = IV`, flags
`CHUNK_START|CHUNK_END|ROOT = 11`, block length 32, root counter 0. The
eight-word IV is
`(6a09e667, bb67ae85, 3c6ef372, a54ff53a, 510e527f, 9b05688c, 1f83d9ab,
5be0cd19)`. Compression state is
`v[0..7]=cv`, `v[8..11]=IV[0..3]`, `v[12..15]=(counter_low, counter_high,
block_len, flags)=(0,0,32,11)`. Exactly the first 1 round is executed with the
standard eight `G` calls per round and the BLAKE3 message permutation between
rounds (vacuous for one round). Output is `o[i]=v[i]^v[i+8]` and
`o[i+8]=v[i+8]^cv[i]` for `i=0..7`; the digest is the first 32
little-endian bytes `LE4(o[0])||...||LE4(o[7])`. This retains the ordinary
hash's flags, counter, length encoding, and feed-forward, rather than a
free-start or compression-only substitute.

Define `f(x)` as the 256-bit integer value of that digest in little-endian
order. Since `msg` is injective, any `x != x'` with `f(x)=f(x')` yields two
distinct 32-byte messages with byte-for-byte equal complete hashes: an
ordinary collision. There is exactly one chunk/parent/root compression per
evaluation, charged as one unit per the v5 rule that BLAKE3 must charge all
such compressions. No second chunk, parent node, key, derivation flag, or
truncation is involved on this domain.

## 2. Distinguished-point algorithm

A selected 1-round BLAKE3 compression (chunk/parent/root) costs one
target-compression unit. Each other primitive 256-bit word operation costs
`1/C` with `C = 222` for `blake3-r1` under v5. Instruction fetch is not a
model primitive and is not separately charged; every data-word operation
below is charged.

Registers hold chaining words, block words, counter/length/flags, and walk
control. The `COMP1` call runs the 1-round compression with feed-forward,
costs 1 unit, and is charged 1 extra ordinary operation to issue. We assume
it may overwrite block registers, so IV, message, padding-zero, counter,
length, and flag words are rewritten every evaluation.

Constants: `theta = 2^-32`. A point is distinguished iff its low 32 digest
bits are zero. Maximum chain length `L = 2^40`. Evaluation budget
`K0 = 65300 * 2^112`. Record cap `Dcap = 2^98`.

```
Main (one run, no restart):
  setup fixed IV/counter/length/flags registers, table base, budget (<=16 ops)
  total_evals = 0; stored = 0
  loop:
    if total_evals >= K0 or stored >= Dcap: break
    s = UniformWord()
    total_evals += 1
    walk from s up to L steps, testing DP after each f step
    charge every step (section 5); on abandon continue
    on DP triple (dp,start,len): lookup dp in table
    if dp already stored with (start0,len0):
      RELOCATE both chains to merge point, let (a,b) be distinct predecessors
      OUTPUT: recompute blake3(msg(a),1), blake3(msg(b),1), check a != b and
        full 256-bit equality, emit pair and halt with success
      else discard and continue
    else store if stored < Dcap and continue
  halt with FAIL
```

Per-evaluation wrapper (conservative, charged every step): 8 IV writes, 16
block-word writes (8 message + 8 zero-fill), 4 state words
(counter low/high, length, flags), 1 call issue, 8 moves of digest words to
next-message registers, DP test (compare + branch), plus amortized loop
control. Total at most 40 ordinary operations per evaluation. Block control
is included. This is a cap, not a measured count; sensitivity in Section 5
shows robustness to larger caps.

`CHAIN` control beyond evaluations: at most 19 operations per chain.
`DPFOUND`: depth-224 structure on high DP bits, at most 3840 operations per
DP-terminated chain. `RELOCATE`: at most `2L` evaluations, charged as
evaluations. `OUTPUT`: two whole reference digests (2 units) plus at most
300 ordinary operations. Table holds at most `Dcap` entries of
`(dp,start,len)`. No unbounded allocation, no recursion, no library sort.
Every evaluation including failures is charged; no restart or external
amplification.

## 3. Correctness

Each `f` evaluation is exactly one complete single-chunk single-block hash
by Section 1. `msg` injectivity means any distinct-predecessor equality
under `f` is an ordinary collision. The walk follows deterministic iteration
of `f`. If two stored chains share a DP, re-walking both from starts reaches
the first agreement index; its immediate predecessors are distinct inputs
with equal images unless the chains coincide, in which case the pair is
discarded. On the good event of Section 6 the algorithm returns. `OUTPUT`
recomputes both complete digests and requires message inequality and full
256-bit equality. Every successful return satisfies the exact profile's
ordinary-collision relation. All resource bounds hold for every coin choice
without any heuristic.

## 4. Message packing check

For 32-byte inputs, block words `w[0..7]` are the message words,
`w[8..15]=0` for loading, with true length 32 encoded in state (not as data).
Counter is 0, flags 11. Total padded extent is one 64-byte block in one
chunk. No second block, parent, or length-overflow branch is needed. This
justifies the 16+8+4 wrapper count as a cap.

## 5. Charged time

`H_calls` counts `COMP1` calls; `W` counts ordinary operations.

- Fixed setup: at most 16 operations.
- Main evaluations: at most `K0 + L + 2` calls (budget plus final-chain
  completion plus 2 for `OUTPUT`), each with at most 40 wrapper operations.
- Chains: deterministically below `Dcap + K0/L < 2^99`, at most 19 ops each,
  below `2^104` total.
- `DPFOUND`: only on DP chains (at most `Dcap`), at most 3840 each, below
  `2^110` total.
- `RELOCATE`: at most `2^41` evaluations, charged as evaluations, below
  `2^43` units generously.
- `OUTPUT`: 2 units + 300 ops, at most once.

Hence:

```
H_calls <= K0 + L + 2
W <= K0*40 + 2^110 + 2^104 + 316
T = H_calls + W/222
  <= K0*(1 + 40/222) + small
```

With `K0 = 65300 * 2^112`, `log2(K0)=127.99479537...`,
`1+40/222=1.18018018...`, `log2=0.238997...`, so
`log2(K0*1.18018018...)=128.23380250...`. The additive remainder is below
`2^100` units (factor below `1+2^-28`). Therefore for every run:

```
T < 2^128.234 < 2^128.3.
```

The submitted `time_log2 = 128.3` retains more than `0.06` bits of slack.
This prices hashing plus all table, control, relocation, and verification
work, preprocessing, failed trials, randomness, and the success budget. One
finite run only.

Sensitivity (all far below 149):

| reading | per-eval | bound |
| --- | --- | --- |
| claimed | 40 | 2^128.234 -> 128.3 |
| 50 per eval | 50 | about 2^128.288 |
| 80 per eval | 80 | about 2^128.42 |
| merge-sort birthday | - | 2^149 (baseline) |

## 6. Success probability under H-RF

Probability space: fresh independent uniform words (one per chain start).
Only this section uses H-RF: fresh `f` evaluations behave as independent
uniform values for contact estimates.

Let `N=2^256`. For the first `K0` evaluations, under H-RF:

```
Pr[contact] >= 1 - exp(-K0*(K0-1)/(2N)).
```

`K0^2/(2N)=0.49640540... > -ln(0.61)=0.49429632...`, so
`Pr[contact] > 0.39128`. Bad events (`B1` start on visited point,
`B2` self-cycle, `B3` long non-DP run, `B4` cap overflow) total below
`7.0e-10` by the same counting as the SHA-256 DP package (starts below
`2^99`, expected DPs below `2^96` vs cap `2^98`, `(1-2^-32)^{2^39}`
exponentially small). Hence `Pr[success] > 0.39127 > 0.39`. The declared
`0.39` keeps `>0.0012` allowance. Input repeats are included, never counted
as collisions. This is an algorithmic bound under H-RF, not confidence in
review.

## 7. Memory, preprocessing, advice

Peak storage with cap `Dcap`: at most `2^98` entries of 3 words (96 bytes)
below `2^105` bytes plus buckets/scratch/code/constants below `2^20` bytes
each. Thus `M < 2^110`; submitted `memory_log2_bytes = 112` keeps slack.
Memory is reported only. Preprocessing is at most 16 ops (`<1` unit, inside
`T`); submitted 0. No advice is used; submitted 0 means at most one byte by
schema convention, with zero actual advice. No `data_log2` is declared
(optional legacy); at most `K0+L+2 < 2^129` evaluations are already charged
in `T`.

## 8. Heuristic, evidence, and limitations

One heuristic `H-RF` (score-critical, success bound only), with statement,
scope, extrapolation, evidence `proof:6,proof:7`, and limitations in
`claim.json` and here. No other heuristic is used. No experiment manifest is
declared because no empirical premise beyond analytic H-RF is used;
`not_requested` is correct. A toy masked run would not strengthen the
contact arithmetic and is not substituted. Certificate manifest is valid and
empty. Limitations: H-RF is unproved for fixed 1-round BLAKE3 with margin
~0.0012; memory is large (no Pareto claim); abstract cost is enormous but
fits the RAM domain. This is accounting, not a weakness of BLAKE3.
Exploratory `plausible_not_refuted` is neither proof nor human acceptance.
Deterministic 1-round collisions near 0-4 remain untrusted until manually
reviewed and promoted; this generic package does not assert them.

## 9. Source note

Independent DP accounting for `blake3-r1-prefix-v1`. The baseline's records,
merge sort, `n=2^129`, and scalar 149 are replaced by the DP construction.
Needs fresh review; inherits no qualification.

## 10. Commands

```sh
yukon setup --track blake3-r1-exploratory
python3 scripts/local_tracks.py show blake3-r1-exploratory
python3 scripts/local_tracks.py check blake3-r1-exploratory
```

`check` gives `mechanically_valid`, `ready`, `certificates_verified: 0`.
No provider key is used locally; remote judging supplies review credentials.
No participant command runs on the host.
