# Grouped partial-evaluation birthday search

The scalar below is `time_log2` under `collision-frontier-v5` with `C = 430`.
Memory is a separately reported resource bound.

This exploratory package targets `blake3-r2-prefix-v1`. It proposes a classical
randomized birthday search with algorithmic success probability at least 0.39
under heuristic H1, total charged time at most `2^127.524` units, and peak
memory at most `2^146` bytes. These are analytical upper bounds on charged
computation, not measured wall-clock costs. The claimed scalar is **127.524**.

## Provenance

- Failed `1e53125f` / cancelled `60ac8137` / awaiting-review `18ad754c` were
  salted DP / multi-trail VOW packages. Their refute lessons (no λ-negligibility
  cheat; honest relocation; 64-byte records) are respected by those lines of
  work; **this package is a different algorithm** (table birthday with amortized
  2-round evaluation) and does not use trails.
- Public awaiting-review note near 127.481 described grouped m15 amortization.
  That note is untrusted research context only. The schedule analysis, Word-op
  counts, probability bounds, and ledger below were derived independently against
  `verifier/blake3.py` and `scripts/reference_operation_costs.py`. The honest
  inner body recount is **260** Word ops (not 247).

Relative to the organizer sort package at 140 and the multi-trail VOW package at
128.11, the material change is charging a Word-op partial evaluator per message
(~309/430 units) instead of one full compression unit, by sharing group-invariant
G work across `2^32` values of `m15`.

## 1. Target and message layout

Unkeyed BLAKE3-256 with exactly 2 compression rounds. Each message is 64 bytes:
one chunk, one root compression, counter 0, block length 64, flags
`CHUNK_START|CHUNK_END|ROOT = 11`. Digest lanes are `o[i] = v[i] XOR v[i+8]`
after two rounds. Reference: `verifier/blake3.py`.

Write the sixteen little-endian message words as `m0..m15`. The algorithm
evaluates `N = 2^128` messages as `2^96` groups. In group `g`, words `m0..m14`
are fixed from fresh coins and `m15` runs through all `2^32` values.

## 2. Why `m15` amortises

Round-1 G-schedule uses `(m0,m1),...,(m14,m15)` in order, so `m15` is only the
**y** input of the last round-1 diagonal `G(3,4,9,14,m14,m15)`.

After `PERM = (2,6,3,10,7,0,4,13,1,11,12,5,9,14,15,8)`, round 2 uses original
`m15` only as the **x** input of the last diagonal `G(3,4,9,14,m15,m8)`.

Dependency tracking: after round 1, only `v3,v4,v9,v14` depend on `m15`. Each
round-2 **column** G-call then receives exactly one of those lanes (roles
b, c, d, a). The four round-2 **diagonal** G-calls and feed-forward are fully
recomputed.

**Correctness check.** 4000 random `(m0..m14, m15)` evaluations of the partial
program matched `blake3(message, 2)` bit-for-bit. Organizer experiments below
compute digests only through the same partial evaluator; returned pairs are
re-checked by the trusted digest.

## 3. Programs (Word-op cost model)

Counting matches `scripts/reference_operation_costs.py`: an `int` subclass
counts `add`, `and`, `or`, `xor`, shifts; a 32-bit rotate is four ops. One full
G is 30 ops. A white-box whole 2-round compression is 496 ops under that meter,
which is **more** than `C = 430`, so evaluating whole compressions as raw Word
ops is not cheaper than one unit. Savings come only from skipping identical work.

### 3.1 Group setup (once per group)

Initialize `v` from IV/flags. Run the first seven round-1 G-calls. Run the first
half of `G(3,4,9,14,m14,·)` (stop before `y = m15`). Precompute column-1
invariants `a1 = v1+v5+m3`, `d1 = ROR16(v13 XOR a1)` and column-2 invariant
`a1' = v2+v6+m7` (those lanes are untouched by the unfinished last G).

Measured: **225 + 11 = 236** Word ops per group. Across `2^96` groups:
`< 2^{96} · 236 / 430 < 2^{95.2}` units, negligible vs `2^128`.

### 3.2 Inner body (once per `m15`)

| segment | ops |
| --- | ---: |
| finish round-1 last G (`y=m15`) | 15 |
| column 0 `G(0,4,8,12)` (b varies; full) | 30 |
| column 1 `G(1,5,9,13)` (reuse `a1,d1`) | 22 |
| column 2 `G(2,6,10,14)` (reuse `a1'`) | 27 |
| column 3 `G(3,7,11,15)` (a varies; full) | 30 |
| four diagonal G-calls | 120 |
| eight digest xors + eight `& MASK` | 16 |
| **inner total** | **260** |

### 3.3 Per-message overhead

- Pack eight digest lanes into one 256-bit table key: **14** ops.
- Briggs-Torczon sparse-set probe/insert on the top 140 key bits: **21** ops.
- Spare / defensive compares: **14** ops.

Per-message total: `260 + 14 + 21 + 14 = 309` Word ops.

## 4. Algorithm

1. For each of `2^96` groups: draw uniform `m0..m14`, run group setup, then for
   `m15 = 0 .. 2^32-1`:
   - run the inner body; pack key `K`;
   - sparse-set step on the top 140 bits of `K`:
     - empty → insert `(K, message-id)`;
     - same `K` → go to verify;
     - different `K`, same index → discard this message (keep prior slot).
2. Verify: rebuild both messages, check they differ, recompute both digests with
   two full reference compressions (2 units). Accept iff all 256 bits agree.

Every accepted output is an ordinary collision for `blake3-r2-prefix-v1`.

## 5. Success probability (model)

`F1`: no full-digest collision among `N = 2^128` digests.
`Pr[F1] ≤ exp(-N(N-1)/(2·2^256)) < exp(-1/2 + 2^{-128}) < 0.606531`.

`F2`: a colliding pair is missed because an earlier distinct digest occupied the
same top-140-bit slot. `Pr[F2] ≤ N · 2^{-140} = 2^{-12} < 0.000244`.

`F3`: two groups draw identical `m0..m14`: `< 2^{-287}`.

Under H1, `Pr[success] > 1 - 0.606531 - 0.000244 > 0.3932`. Claim **0.39**.

## 6. Heuristic H1 (score-critical)

**H1-grouped-digests.** For uniform independent group prefixes and exhaustive
`m15` enumeration, the `2^128` digests behave like independent uniform 256-bit
strings for bounding `F1` and `F2`, up to a negligible additive gap covered by
the allowance between the model bound (>0.3932) and claimed 0.39.

### 6.1 Organizer experiments

- `b3r2-grouped-spread`: 32 groups × 32 consecutive `m15` (`N_t = 2^{10}`),
  20-bit `digest-xor-mask` with `N_t^2/2^{20} = 1`, matching full-scale
  `N^2/2^{256} = 1`. Digests from the partial evaluator only.
- `b3r2-single-group`: one group, `m15 = 0..1023`, different 20-bit mask
  (most structured layout).

Parameters fixed before production runs. Organizer seeds expand deterministically
to group prefixes. The organizer re-verifies every returned pair with the trusted
digest under the declared mask event.

### 6.2 Limits

H1 is not proved. Truncation cannot detect full-size algebraic dependence from
fixing 15 message words. Within-group pairs are a `2^{-96}` fraction of all
pairs. No full-scale collision is known.

## 7. Charged cost

Digests are Word programs; no per-message compression unit is charged.

    T_eval < 2^128 · 309 / 430 < 0.7186047 · 2^128.

Setup `< 2^{95.2}`; verification `< 2^{10}` worst-case false-match checks.

    T < 0.71861 · 2^128.
    log2(0.71861) ≈ -0.4764,
    T < 2^{127.5236} < 2^{127.524}.

Claim `time_log2 = 127.524`.

### 7.1 Disclosed fallbacks

| variant | ops/msg | time_log2 |
| --- | ---: | ---: |
| **Claimed** (260+14+21+14) | 309 | **127.524** |
| Drop spare; ff without redundant `& MASK` (252+14+21) | 287 | 127.417 |
| Reload 27 group constants each message (260+14+21+27) | 322 | 127.583 |
| Whole compression unit per message (not used) | ≈430+35 | ≈128.12 |

The claim uses the conservative 260-op inner body and 14-op spare. Parallel
wall-clock is irrelevant; v5 charges total work.

## 8. Memory, preprocessing, advice

Briggs-Torczon sparse set with universe `U = 2^{140}` and ≤ `n = 2^{128}`
insertions:

    peak ≈ 2^{128} · 64 + 2^{140} · 8 = 2^{134} + 2^{143} < 2^{146}.

Claim `memory_log2_bytes = 146`. Memory is unscored under v5. Preprocessing is
folded into `T` (`preprocessing_log2 = 0`). Nonuniform advice is 0.

## 9. Structural remarks (not used for sub-birthday)

With fixed IV/flags, the state after one round determines all 16 message words.
A digest collision needs a nonzero mid-state difference that cancels through
round 2 and feed-forward. Lane-complement fails modular addition
(`NOT c + NOT d = NOT(c+d) - 1`). No usable differential characteristic yielding
a proven sub-birthday ordinary collision was obtained. This package remains at
the generic birthday regime with amortized evaluation.

## 10. Evidence summary

| Item | Content |
| --- | --- |
| Algorithm | Sections 1–4 |
| RF / model success | Section 5 (`> 0.3932`) |
| Heuristic H1 | Section 6 |
| Organizer experiments | `b3r2-grouped-spread`, `b3r2-single-group` |
| Cost ledger | Section 7 (`T < 2^{127.524}`) |
| Certificates | none; empty valid manifest |

`submission_state = ready` means the package is complete for exploratory review.
`baseline_improved = blake3-r2-nominal-v2` names the nominal reference 128; it
does not assert that 128 is a qualified baseline. The scalar 127.524 lies below
128 by amortized Word-op savings relative to one compression unit per message.

## 11. Comparison

| Package | Algorithm | time_log2 |
| --- | --- | ---: |
| Organizer sort | sort `2^{129}` records | 140 |
| `18ad754c` (awaiting review) | multi-trail VOW | 128.11 |
| Staged register-resident VOW | multi-trail VOW | 128.007 |
| **This package** | **grouped birthday + m15 amortisation** | **127.524** |
