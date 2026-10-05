# Grouped m15 birthday — BT-envelope counter absorb + partial-eval meter (127.432)

Claimed `time_log2` under `collision-frontier-v5` (`C=430`): **127.432**.

This package is the same algorithm family as validating `9551ae18` (@**127.437**,
291 ops/msg) with two honest changes:

1. **Documented overcharge removal / loop absorb.** The mandatory
   `(g∥m15) ← (g∥m15)+1` counter update is charged inside the existing
   **24-op** `H-COST-BT-SPARSE` envelope (edge-margin reallocation). Per-message
   dominant total becomes **290 = 252 + 14 + 24**. Outer unroll control remains
   **3/256** in `T`. The BT envelope does **not** drop below the defendable 24.
2. **Partial-eval count evidence.** Declares score-critical
   `H-COST-PARTIAL-EVAL` with a segment-metered 252-op inner body under organizer
   Word accounting (`scripts/reference_operation_costs.py` convention;
   organizer `_g=30`), plus experiment `b3r2-partial-eval-meter`.

It does **not** shrink BT below 24, does **not** revive `c36797d2`'s unsupported
`H-COST-SPARSE-21`, does **not** claim pack=0, and does **not** adopt the public
247 `_g` undercount. Briggs–Torczon, `prefixes[g]`, VERIFY reconstruction, and
the unconditional (no-expectation) ledger are unchanged in strength from the
c1a7 / 03e49 / 9551 repair lineage.

## Lineage (what this retains)

| prior id | defect | repair kept here |
| --- | --- | --- |
| `c1454726` | `F-COST-VERIFY-OMITTED` | compressions only on equal `K_full`; `V_max=8` |
| `4dd74401` | `F-COST-INDEX-COMPARE-TAIL` | no expectations inside `T`; worst-case compare in BT |
| `c36797d2` | `H-COST-SPARSE-21` unsupported | explicit BT + declared `H-COST-BT-SPARSE` @**24** (not 21) |
| `7212ec23` | EVAL-F1/F2 (msg reconstruct / setup exponent) | `prefixes[g]` + ≤512 Word/group |
| `03e49dc5` | live @127.467 / 297 / BT-28 | retained in AR ladder |
| `c1a7e1b9` | review @127.447 / 293 / BT-24 | retained; new `H-COST-PARTIAL-EVAL` obligation addressed here |
| `9551ae18` | validating @127.437 / 291 / loop amort | this package undercuts by envelope absorb; adds PE meter |

## Hardening against paired-review failure patterns

### Against `4dd74401` — F-COST-INDEX-COMPARE-TAIL
Every index-hit path that compares keys is charged as a **worst-case** Word-op
path inside the 24-op BT envelope (§2.4). The time bound `T` uses **no**
H1-expectation substitution for compare frequency. Unequal-`K` discards cost
Word ops only; they never become compression units via an expectation.

### Against `c1454726` — F-COST-VERIFY-OMITTED
Target compressions occur **only** on equal `K_full` (§2.5). Each VERIFY rebuilds
both messages from `prefixes[g]` / `recs[s]`, then runs **two** reference
compressions. Cap `V_max=8` ⇒ ≤16 compression units. VERIFY Word work ≤640 ⇒
`<2` units after `/C`. Ledger lines are explicit in §3.

### Against `c36797d2` — not_evaluable / H-COST-SPARSE-21
We do **not** claim a 21-op sparse dictionary. Membership is the written
Briggs–Torczon filter `dense[sparse[idx]]==idx ∧ sparse[idx]<n`, with
never-cleared `sparse[]` of 256-bit words. Declared score-critical cost
heuristic `H-COST-BT-SPARSE` covers the **24-op** envelope. Path table +
address/edge margin are in §2.4. This undercut does **not** trim BT below 24.

### Against `7212ec23` — algorithm_defined / resources_defined / F-MSG-RECONSTRUCTION
Retained `prefixes[g]` table (two 256-bit words packing `m0..m14` per group).
Live records store `recs[s]=(g∥m15)`. VERIFY (§2.5) rebuilds both 64-byte
messages before rehash. Group-setup budget ≤512 Word/group ⇒ `<2^{97}` units.
Memory layout for sparse/dense/keys/recs/prefixes is stated in §7.

### Against `F-COST-PARTIAL-COUNT-EVIDENCE` / `H-COST-PARTIAL-EVAL` (new on c1a7)
Section §2.6 gives the organizer-Word segment ledger for the 252-op inner body.
Experiment `b3r2-partial-eval-meter` implements the same Word meter, checks
segment identity on every message, and checks digests against an inlined
2-round compress bit-identical to `verifier/blake3.py`. Heuristic
`H-COST-PARTIAL-EVAL` is declared in `claim.json`.

Every score-critical heuristic is **declared** (claim.json), **implemented**
(§2), and **covered by the cost ledger** (§3).

## 1. Target

Unkeyed BLAKE3-256, exactly 2 rounds, 64-byte root block, flags 11, counter 0,
length 64. Ordinary full-digest collision of distinct messages.
Reference: `verifier/blake3.py`.

## 2. Algorithm (fully specified)

`N=2^{128}` messages as `G=2^{96}` groups × all `m15∈[0,2^{32})`.

### 2.1 Persistent state

- `n ∈ {0,…,N}` live BT count; initially `0` (one store at run start).
- `sparse[0..2^{140})` — array of **256-bit** words (**never cleared**).
- `dense[0..N)`, `keys[0..N)`, `recs[0..N)` — parallel arrays of 256-bit words.
- **`prefixes[0..G)`** — retained group-prefix table. Entry `prefixes[g]` is
  **two** 256-bit words packing the fifteen 32-bit words `m0..m14` (480 bits) for
  group `g`. Written once at group setup; read only on VERIFY.

Membership: `idx` is live iff `s=sparse[idx]`, `s<n`, and `dense[s]=idx`
(Briggs–Torczon). Same filter as `03e49dc5` / `c1a7e1b9` / `9551ae18`.

Record layout for live slot `s`:
- `dense[s] = idx` (140-bit index, zero-padded in a 256-bit word),
- `keys[s] = K_full` (full 256-bit digest),
- `recs[s] = (g ∥ m15)` with `g` a 96-bit group id in the high bits and `m15` a
  32-bit word in the low bits (fits in one 256-bit word).

### 2.2 Group setup (once per group `g`)

1. Draw 15 uniform random 32-bit words `m0..m14` (or equivalently draw two
   256-bit random words and truncate/pack). Charge ≤20 Word ops for RNG/packing.
2. `STORE prefixes[g][0], prefixes[g][1]` with the packed prefix (**2 stores**).
3. Run the fixed partial-evaluation setup body for `m0..m14` (**≤236 Word ops**,
   organizer-metered; matches prior packages and §2.6 setup count).
4. Set `m15 ← 0` / initialize live counter register `(g∥m15)`. Enter the
   256-way unrolled per-message loop (§2.3).

**Group-setup Word budget:** ≤512 ops/group (236 body + RNG/pack/stores + margin).

### 2.3 Per-message step (inside 256-way unroll)

1. Partial-eval body → eight 32-bit digest lanes (**252** Word ops; FF = 8 digest
   xors; no trailing masks; organizer `_g=30`). Metered exactly in §2.6: 252.
2. Pack lanes into one 256-bit register `K_full` (**14** = 7 shifts + 7 ORs).
   Metered exactly: 14.
3. `idx = top140(K_full)` (shift/mask charged inside the BT address/edge margin).
4. Run `BT_probe_insert` (§2.4) — envelope **24**, which **includes** the
   counter update `(g∥m15) ← (g∥m15)+1` that always follows the probe/insert
   (see §2.4 edge accounting).
5. On `VERIFY(s)`: run §2.5; on accept, halt; count toward `V_max=8`.

**Outer control (every 256 unrolled copies):** compare block counter; branch;
increment block counter (**3** ops per 256 messages = **3/256** per message).
After `2^{32}` messages the group ends (exact trip count).

### 2.4 Procedure `BT_probe_insert` (≤24 Word ops, includes counter)

256-bit word RAM. Loads/stores/compares/branches/adds = 1 op each.
Membership uses the standard Briggs–Torczon filter
`dense[sparse[idx]]==idx ∧ sparse[idx]<n` — **not** an undeclared “sparse
dictionary of 21 ops” (`c367`).

```
s <- LOAD sparse[idx]                 # 1
if not (s < n): goto INSERT           # 1 cmp + 1 br
d <- LOAD dense[s]                    # 1
if d != idx: goto INSERT              # 1 cmp + 1 br
Ks <- LOAD keys[s]                    # 1
if Ks != K_full: goto AFTER           # 1 cmp + 1 br
return VERIFY(s)                      # 1 br  (VERIFY path; counter still updated after return handling)
INSERT:
STORE sparse[idx] <- n                # 1
STORE dense[n] <- idx                 # 1
STORE keys[n] <- K_full               # 1
STORE recs[n] <- (g ∥ m15)            # 1  (register already live)
n <- n + 1                            # 1
AFTER:
(g ∥ m15) <- (g ∥ m15) + 1            # 1  (always; low 32 bits)
return CONTINUE                       # 1 br
```

**Path primitives (including the always-taken counter add, excluding VERIFY body):**

| path | count | breakdown |
| --- | ---: | --- |
| DISCARD (live, unequal `K`) | 10 | 3 loads + 3 cmp + 3 br + 1 counter-add (+ return br shared below) |
| INSERT via empty (`s≥n`) | 10 | load+cmp+br + 4 stores + n-add + counter-add |
| INSERT via stale (`s<n`, `dense≠idx`) | **13** | load+cmp+br + load+cmp+br + 4 stores + n-add + counter-add |
| VERIFY-decide then counter | 10 | same through equal-`K` branch + counter after VERIFY returns CONTINUE |

Worst path primitives among non-VERIFY hot paths = **13** (INSERT via stale,
including counter).

**Address-arithmetic charge:** each array access may need a `base+index`
addition. The INSERT-via-stale path touches at most **six** distinct address
computations after reusing materialized `idx` and `n`. Charge **≤6**.

**Edge / packing margin:** ≤**5** ops covering flag materialization /
branch-delay slots / spare compare reorder / return-branch accounting.
Forming `(g∥m15)` is **not** an extra charge: that register is the live
per-message counter; its `+1` is the explicit counter line above.

**Charged envelope: 13 + 6 + 5 = 24 Word ops.** Same numeric floor as
`c1a7e1b9` / `9551ae18`. The change vs `9551ae18` is only that the previously
separate `+1` loop line is now inside this envelope (edge margin 6→5 to make
room for the counter primitive already listed in the path table).

Compressions occur **only** inside §2.5. Declared score-critical cost
heuristic **`H-COST-BT-SPARSE`**: this 24-op envelope.

**Explicit non-claim vs `c367`:** we do **not** assert an unsupported
`H-COST-SPARSE-21`. Representation, init policy, membership filter, and
op-by-op procedure are fully written above and ledger-covered by the 24-op
line in §3.

### 2.5 VERIFY(s) — reconstruction via prefix table

Let `rec = LOAD recs[s]` (**1**). Parse `g* = high96(rec)`, `m15* = low32(rec)`
(**2** masks/shifts).

**Rebuild stored message `M*`:**
1. `p0 ← LOAD prefixes[g*][0]`; `p1 ← LOAD prefixes[g*][1]` (**2**).
2. Unpack fifteen 32-bit words `m0..m14` from `(p0,p1)` into a 16-word buffer and
   set word 15 to `m15*` (**≤20** stores/shifts).

**Rebuild current message `M`:** same unpack from `prefixes[g]` (already in
registers from this group's setup, or reload ≤2 loads) + current `m15` (**≤20**).

Then:
- If `M == M*` as 64-byte strings, return CONTINUE (not a distinct-message
  collision) — **≤16** word compares.
- Else run **two** reference compressions (`verifier/blake3.py`); compare digests
  (**1** word compare). If equal, **accept** and return witness `(M,M*)`.
- Increment verification counter; if counter > `V_max=8`, **fail**.

**VERIFY Word ops (non-compression), worst case per attempt:** ≤80.
Across ≤8 attempts: ≤640 Word ops → ≤640/430 < 2 compression-units after `/C`.

### 2.6 Partial-eval Word meter (H-COST-PARTIAL-EVAL evidence)

Convention (identical to `scripts/reference_operation_costs.py`):
- Machine: classical 256-bit word RAM.
- Each of `+`, `&`, `|`, `^`, `<<`, `>>` on a `Word` counts **1**.
- `_ror(v,n)` expands to `(v>>n)|(v<<(32-n))&MASK` — four ops (two shifts, OR, AND).
- No native 32-bit rotate is assumed.
- Under this meter, organizer `blake3._compress` / `_g` costs **30** per full G
  and **430** for a full 2-round compress (`C=430`).

Per-message body after group setup (FF xor-only, no trailing `& MASK`):

| segment | ops | notes |
| --- | ---: | --- |
| `r1_finish` | **15** | second half of last R1 G with `m15` (`_g` second half) |
| `r2_col0_full` | **30** | full G on permuted `(m0,m1)` |
| `r2_col1_partial` | **22** | restore invariant `(a1,d1)` + continue second half |
| `r2_col2_partial` | **27** | restore invariant `a1c2` + continue second half |
| `r2_col3_full` | **30** | full G |
| `r2_diagonals` | **120** | four full G (`4×30`) |
| `ff` | **8** | eight `v[i]^v[i+8]` (no trailing masks) |
| **Inner total** | **252** | |

Identity: `15+30+22+27+30+120+8 = 252`.

Group-setup body under the same meter is **236** Word ops (charged inside the
≤512/group budget of §2.2).

Bit-exactness: for every metered message in experiment
`b3r2-partial-eval-meter`, the body's digest equals the inlined 2-round root
compress (same schedule/IV/flags as `verifier/blake3.py`). Segment counts are
deterministic (identical on every message).

**Explicit non-claim:** we do **not** use public 247 (undercounts `_g` as 29 on
several segments). Fallback if FF `& MASK` required: `ff=16` → inner **260** →
dominant 298 → `time_log2=127.472` (not this package).

Declared score-critical cost heuristic **`H-COST-PARTIAL-EVAL`**: this 252-op
body under the organizer Word convention above.

## 3. Unconditional time ledger

| component | ops/msg | where charged |
| --- | ---: | --- |
| Inner partial-eval body | **252** | §2.3 / §2.6 / `H-COST-PARTIAL-EVAL` |
| Pack `K_full` | 14 | §2.3 (7 shl + 7 OR, exact) |
| Briggs–Torczon + K compare + counter | **24** | §2.4 / `H-COST-BT-SPARSE` |
| **Per-message dominant** | **290** | |
| Outer unroll control | **3/256** | §2.3 (written in `T`) |

Plus once-per-run / rare:

| component | bound | where |
| --- | --- | --- |
| Init `n←0` | 1 Word | §2.1 |
| Group setup | ≤512 Word/group × `2^{96}` | §2.2 |
| VERIFY compressions | ≤`2·V_max=16` units | §2.5 |
| VERIFY Word work | ≤640 Word → `<2` units | §2.5 |

Group-setup units: `2^{96}·512/430`.
Since `512/430 < 1.191`, this is `< 2^{96}·1.191 < 2^{96.25} < 2^{97}`.

**No expectations in the inequality.** Index-hit compares are worst-case inside
the 24-op BT line, not H1-expected counts (`4dd` repair).

Let `U = (290 + 3/256)/430`. Exact dominant:
`log2((290+3/256)/430)+128 ≈ 127.431774`.

    T ≤ N·U + 16 + 2 + 2^{97}
      = 2^{128}·(290 + 3/256)/430 + 18 + 2^{97}
      < 2^{128}·(290 + 3/256)/430 + 2^{98}
      < 0.674446·2^{128}
      < 2^{127.43178} < 2^{127.432}.

Claim **`time_log2 = 127.432`**.

### Delta vs validating `9551ae18`

| item | 9551 (validating) | this package |
| --- | ---: | ---: |
| Inner (FF xor-only, `_g=30`) | 252 | **252** (now segment-metered) |
| Pack `K_full` | 14 | 14 |
| BT + K compare envelope | 24 | **24** (includes counter) |
| Separate loop increment | 1 | **0** (absorbed into BT envelope) |
| **Per-message dominant** | **291** | **290** |
| `time_log2` | 127.437 | **127.432** |
| `H-COST-PARTIAL-EVAL` | undeclared | **declared + metered** |

Haircut source: documented edge-margin reallocation absorbing the counter into
the existing 24-op BT envelope. Not from undercounting VERIFY, index-compare
tail, pack, inner `_g`, or BT below 24.

## 4. Success probability

`F1`: no 256-bit collision among N digests: `< e^{-1/2+2^{-128}} < 0.606531`.

`F2` (**earliest-completing pair displacement**): Let `E` be the event that at
least one unordered colliding pair exists. On `E`, let `(a*,b*)` be the unique
ordered pair with `pos(a*)<pos(b*)`, `digest(a*)=digest(b*)`, minimizing
`(pos(b*), pos(a*))` lexicographically (the collision that completes earliest in
scan order). `F2` is the event that when `a*` was inserted, `idx(a*)` was already
live with a **different** key, so `a*` was discarded. At that moment `<N` entries
exist, so under H1 (uniform independent digests ⇒ uniform independent `idx`)
`Pr[F2 | E] ≤ N/2^{140} = 2^{-12}`. The collision-conditioning that defines
`(a*,b*)` couples `digest(a*)` with `digest(b*)` but does not, under H1, couple
`idx(a*)` to the keys of **unrelated** prior live entries beyond this bound.
(Declared inside `H1-grouped-digests` scope.)

`F3`: identical prefixes among `2^{96}` draws: `< 2^{-287}`.

`F4`: `V_max` exhausted before a true verify: under H1, same-`K` events before the
first birthday collision are negligible; `V_max=8` suffices.

Under H1: success `> 1 - 0.606531 - 2^{-12} - 2^{-287} - ε > 0.3932`.
Claim **0.39**.

## 5. Heuristics (all score-critical ones declared)

### 5.1 `H1-grouped-digests`

Unchanged modeling hypothesis for F1 / F2-conditioning / F4. Time bound does
**not** use H1. Experiments are matched-scale consistency checks only — they do
**not** rigorously establish full-scale 256-bit iid behavior (acknowledged).

Matched-scale load identity used by all four H1 experiments:

    N_t^2 / 2^w = 1 = N^2 / 2^{256}.

### 5.2 `H-COST-BT-SPARSE`

The §2.4 procedure (including the always-taken counter update) fits in ≤**24**
charged primitives per message on the organizer 256-bit word RAM, including one
256-bit `K_full` compare and address/edge margin. Evidence: §2.4 op list + path
table. No page-walk model beyond 1-op word addressing.
**Numeric floor unchanged from `c1a7e1b9` / `9551ae18` — not a trim below 24.**

Fallback if a future judge demands the prior padded 28-op envelope without
counter absorb: restore 28+separate-loop accounting → 297 ops →
`time_log2=127.467` (already in flight as `03e49dc5`).

### 5.3 `H-COST-PARTIAL-EVAL`

The §2.3 / §2.6 body costs exactly **252** Word ops under organizer accounting
with `_g=30` and FF xor-only. Evidence: segment table §2.6; experiment
`b3r2-partial-eval-meter` (meter source + digest bit-exactness checks).
Observation op counts are harness-untrusted; the adjudicated content is the
analytic ledger plus readable meter.

## 6. Experiments

| id | layout | role |
| --- | --- | --- |
| `b3r2-grouped-spread` | 32×32, w=20 | H1 consistency |
| `b3r2-grouped-spread-16` | 16×16, w=16 | H1 cross-scale |
| `b3r2-grouped-spread-24` | 64×64, w=24 | H1 cross-scale |
| `b3r2-single-group` | 1×1024, w=20 | H1 structured stress |
| `b3r2-partial-eval-meter` | 32×32, w=20 + Word meter | **H-COST-PARTIAL-EVAL** evidence |

## 7. Memory

- `sparse`: `2^{140}` entries × **32-byte** (256-bit) words = `2^{145}` bytes.
- `dense/keys/recs`: ≤`2^{128}` × 3 × 32 = `2^{128}·96` bytes.
- `prefixes`: `2^{96}` × 2 × 32 = `2^{96}·64 = 2^{102}` bytes.
Peak `< 2^{146}`. Claim `memory_log2_bytes=146`.
Never-cleared `sparse` needs no `2^{140}` zeroing pass.

## 8. Comparison

| package | time_log2 | notes |
| --- | ---: | --- |
| `c36797d2` | 127.417 | `not_evaluable` (`H-COST-SPARSE-21`) — abandoned |
| `7212ec23` | 127.467 | `not_evaluable` (EVAL-F1/F2) |
| `03e49dc5` | 127.467 | awaiting review (kept; BT-28) |
| `c1a7e1b9` | 127.447 | in review (kept; BT-24; PE obligation) |
| `9551ae18` | 127.437 | validating (kept; loop amort) |
| **This package** | **127.432** | counter absorb into BT-24; PE meter added |
| `8e870aed` | 127.524 | awaiting (kept) |
| `18ad754c` | 128.11 | awaiting (kept) |

## 9. What we refuse to claim

- **287 / 127.417** via 21-op sparse (`c367` `not_evaluable`) — abandoned.
- **Further BT trim below 24** without new microbenchmark evidence — refused.
- **Pack=0 / ~127.397** without a separate register-digest evaluability writeup —
  not this package.
- **Public 247-style inner** — undercounts organizer `_g` (30→29).
- Expectation-for-worst-case index hits inside `T` (`4dd` fatal).
- Skipping VERIFY rehash on equal-`K_full` (`c145` fatal).
- Omitting `prefixes[g]` / message reconstruction (`7212` EVAL-F1).
- Undeclared partial-eval op counts without Word-meter evidence.

## 10. Evidence summary

Algorithm/reconstruction §2; BT path table §2.4; partial-eval meter §2.6; cost
§3; probability §4; heuristics §5; experiments §6; memory §7. Empty certificates.
Failure-pattern hardening stated in the preamble.
`submission_state=ready`.
