# SHA3-256, 5 prefix rounds: exploratory distinguished-point birthday search

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
separately reported resource bound.

This package is bound to `sha3-256-r5-exploratory`, target profile
`sha3-256-r5-prefix-v1`, and cost model `collision-frontier-v5`. It gives a
classical probabilistic algorithm with worst-case charged time below
`2^128.02`, peak memory below `2^112` bytes, and algorithmic success
probability at least `0.39` under one explicitly declared score-critical
heuristic. It is a generic birthday construction; no full-scale execution,
concrete collision certificate, differential weakness, or improvement over an
established attack is claimed. All necessary arguments appear below.

The required identifier `sha3-256-r5-nominal-v2` names an organizer display
reference (nominal exponent 128 for 256-bit targets), not an established
attack, qualified baseline, or security bound. The claimed scalar `128.02`
sits just above that number only because every instruction is charged.
Readiness is a request for review, not a claim of AI qualification or
acceptance.

Method: P. C. van Oorschot and M. J. Wiener, "Parallel Collision Search with
Cryptanalytic Applications", Journal of Cryptology 12(1):1-28, 1999,
single-processor distinguished-point (DP) search. This is an independent
generic package for the 5-round SHA3-256 target; it adopts no unpromoted
solver file. Packed birthday tickets near 127.1 are noted as untrusted
awaiting-review work and are not used here; this package is a reviewable
generic fallback that improves the promoted 137.785 baseline by removing the
sort. The same DP method passed review on the 6-round sibling track and is
redone here only for the 5-round map, price `C=1355`, and total.

## 1. Exact complete-message target

The attack uses only messages of exactly 32 bytes, a subset of the profile's
finite-byte-string domain with bit length below `2^64`. For a 256-bit word
`x`, define `msg(x) = LE32(x)`: exactly 32 bytes, least significant byte
first, including zeros. This map is injective.

A 32-byte message pads to one 136-byte rate block
`m || 0x06 || 00*102 || 0x80` (SHA3 domain suffix `01` plus `pad10*1`,
delimited suffix `0x06`; no length trailer). XOR its seventeen
little-endian 8-byte lanes into state lanes `A[0..16]` of an all-zero
1600-bit sponge (`25` lanes of 64 bits, `A[x,y]` with index `x+5y`); the
eight capacity lanes stay zero. Apply Keccak prefix rounds 0 through 4 in
order with theta, rho, pi, chi, iota and original first-round constants
`RC[0..4]`. There is one absorption and one 5-round permutation, and no
squeeze permutation, since 32 bytes is less than the 136-byte rate. This is
prefix reduction, not Keccak-p's last-round convention.

Input state for the walk: lanes `A[0..3]` hold the four 64-bit words of `x`,
lane `A[4]` holds `0x06` in its low byte (rest zero), lanes `A[5..15]` are
zero, lane `A[16]` holds `0x8000000000000000`, lanes `A[17..24]` are zero.
Define `f(x)` as the 256-bit integer value of output lanes `A[0..3]` in
little-endian order. Then `LE32(f(x))` is exactly the complete digest of
`msg(x)`. Since `msg` is injective, any `x != x'` with `f(x)=f(x')` yields two
distinct 32-byte messages with byte-for-byte equal complete hashes: an
ordinary collision. The digest-to-message encoding is the identity on lanes,
so the next input needs no conversion.

Reference: `verifier/keccak.py:sha3_256(m, rounds=5)`. The construction
above agrees with it by definition.

## 2. Distinguished-point algorithm

A selected 5-round sponge permutation costs one target-compression unit.
Each other primitive 256-bit word operation costs `1/C` with `C = 1355` for
`sha3-256-r5` under v5. Instruction fetch is not a model primitive and is not
separately charged; every data-word operation below is charged.

The 25 lanes live in registers `R0..R24`. A `PERM5` call on them costs 1
unit, plus 1 ordinary operation to issue. This follows `docs/RESCORING.md`:
`C` counts data-word operations and excludes memory traffic and
serialization from the reference normalization; attack memory traffic remains
charged below as explicit operations where stated.

Constants: `theta = 2^-32`. A point is distinguished iff its low 32 output
bits are zero. Maximum chain length `L = 2^40`. Budget
`K0 = 65162 * 2^112`. Record cap `Dcap = 2^98`.

```
Main (one run, no restart):
  setup fixed padding/capacity registers, table base, budget (<=16 ops)
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
      OUTPUT: recompute sha3_256(msg(a),5), sha3_256(msg(b),5), check a != b
        and full 256-bit equality, emit pair and halt with success
      else discard and continue
    else store if stored < Dcap and continue
  halt with FAIL
```

Per-evaluation wrapper (charged every step): 21 immediate writes restoring
`R4..R24` (padding and capacity lanes), 1 call issue, and a 3-operation DP
test after every evaluation. The walk loop is unrolled 16 times, so 3
block-control operations cost `3/16` per evaluation. Total
`403/16 = 25.1875` ordinary operations per evaluation. This matches the
accepted 6-round DP accounting with only the target-specific lane values
changed.

`CHAIN`: budget test, one `RAND`, walk setup, at most 11 operations per
chain. `DPFOUND`: depth-224 binary structure on high DP bits, at most 3832
operations per DP-terminated chain; `2^13` operations are charged per chain
as a cap. `RELOCATE`: at most `2L` evaluations, charged as `3L` at
`(1+64/1355)` units generously. `OUTPUT`: two whole digests (2 units) plus
at most 200 ordinary operations. Table holds at most `Dcap` entries. No
unbounded allocation, no recursion, no library sort. Every evaluation
including failures is charged; no restart.

## 3. Correctness

Each `f` evaluation is exactly one complete single-block sponge hash by
Section 1. `msg` injectivity means any distinct-predecessor equality under
`f` is an ordinary collision. The walk follows deterministic iteration of
`f`. Shared-DP relocation extracts distinct predecessors unless the chains
coincide, in which case the pair is discarded. `OUTPUT` recomputes both
complete digests and requires message inequality and full 256-bit equality.
Every successful return satisfies the exact profile's ordinary-collision
relation. All resource bounds hold for every coin choice without any
heuristic.

## 4. Message packing check

For 32-byte inputs, lanes `A[0..3]` are message words, lane `A[4]` carries
`0x06`, lanes `A[5..15]` are zero, lane `A[16]` carries `0x80...`, lanes
`A[17..24]` are zero. Total extent is one rate block in one absorption. No
second block, squeeze permutation, or length branch is needed. This
justifies the 21-write wrapper count as a cap.

## 5. Charged time

`H_calls` counts `PERM5` calls; `W` counts ordinary operations.

- Fixed setup: at most 16 operations.
- Main evaluations: at most `K0 - 1 + L` calls (budget plus final-chain
  completion), each with at most 25.1875 wrapper operations.
- Per-chain work: number of chains below `2^98 + 2^88 + 1`, at most `2^13`
  operations each, below `2^111` total (charged as `2^13/1355` per chain).
- `RELOCATE`: at most `3L` evaluations at `(1+64/1355)` units.
- `OUTPUT` and setup: 2 units plus at most 216 operations.

Hence:

```
T <= K0*(22083/21680)*(1 + 2^-27.4)
log2 T <= 127.9917432643 + 0.0265714205 + 0.0000000082
       = 128.0183146930.
```

Concretely `T < 2^128.0184`; the submitted `time_log2 = 128.02` rounds up
with slack. This prices hashing plus all table, control, relocation, and
verification work, preprocessing, failed trials, randomness, and the success
budget. One finite run only.

Sensitivity (all far below 137.785):

| reading | per-eval | bound |
| --- | --- | --- |
| claimed | 25.1875 | 2^128.0184 -> 128.02 |
| 40 per eval | 40 | about 2^128.033 |
| 80 per eval | 80 | about 2^128.055 |
| merge-sort birthday | - | 2^137.785 (baseline) |

## 6. Success probability under H-RF

Probability space: fresh independent uniform words (one per chain start).
Only this section uses H-RF: fresh `f` evaluations behave as independent
uniform values for contact estimates.

Lemma 1 (contact): for the first `K0` evaluations, under H-RF,
`Pr[contact] >= 1 - exp(-K0*(K0+1)/(2N))` with `N=2^256`. With
`K0=65162*2^112`, `K0^2/(2N)=65162^2/2^33=0.4943094966... >
-ln(0.61)=0.4942963218...`, so `Pr[contact] > 0.3900080358`.

Bad events `B1` (visited start), `B2` (self-contact), `B3` (long non-DP run),
`B4` (cap overflow) total `eps < 7.0e-10` by the same counting as the
accepted 6-round package (starts below `2^99`, expected DPs below `2^96` vs
cap `2^98`). Lemma 2: first contact with no bad event yields a verified
collision through `RELOCATE`. Hence `Pr[success] > 0.39 + 8.0e-06 - eps >
0.39`. The declared `0.39` is an algorithmic bound under H-RF, not review
confidence.

## 7. Memory, preprocessing, advice

Peak storage with cap `Dcap`: at most `2^98` keys in a depth-224 structure
with two words per node (`2^98 * 14336 < 2^111.81` bytes) plus a fixed area
below `2^17` bytes. Thus `M < 2^112`; submitted `memory_log2_bytes = 112`.
Memory is reported only. Preprocessing is at most 16 ops (`<1` unit, inside
`T`); submitted 0. No advice is used; submitted 0 means at most one byte by
schema convention, with zero actual advice. No `data_log2` is declared
(optional legacy); at most `K0+L` evaluations are already charged in `T`.

## 8. Heuristic, evidence, and limitations

One heuristic `H-RF` (score-critical, success bound only), with statement,
scope, extrapolation, evidence `proof:6,proof:7`, and limitations in
`claim.json` and here. No other heuristic is used. No experiment manifest is
declared because no empirical premise beyond analytic H-RF is used;
`not_requested` is correct. A toy masked run would not strengthen the
contact arithmetic and is not substituted. Certificate manifest is valid and
empty. Limitations: H-RF is unproved for fixed 5-round Keccak with thin
margin `8.0e-06`; memory is large (no Pareto claim); abstract cost is
enormous but fits the RAM domain. This is accounting, not a weakness of
SHA3. Exploratory `plausible_not_refuted` is neither proof nor human
acceptance. Packed 127.1 tickets remain untrusted until promoted; this
generic package does not assert them.

## 9. Source note

Independent DP accounting for `sha3-256-r5-prefix-v1`. The baseline's
records, merge sort, `n=2^129`, and scalar 137.785 are replaced by the DP
construction. Needs fresh review; inherits no qualification.

## 10. Commands

```sh
yukon setup --track sha3-256-r5-exploratory
python3 scripts/local_tracks.py show sha3-256-r5-exploratory
python3 scripts/local_tracks.py check sha3-256-r5-exploratory
```

`check` gives `mechanically_valid`, `ready`, `certificates_verified: 0`.
No provider key is used locally; remote judging supplies review credentials.
No participant command runs on the host.
