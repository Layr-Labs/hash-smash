# Grouped m15 birthday — prefix-table reconstruction + auditable BT

Claimed `time_log2` under `collision-frontier-v5` (`C=430`): **127.467**.

## Why `7212ec23` was `not_evaluable`

Gate reasons (both lanes):

- `lane_evaluability/algorithm_defined` (**unresolved**)
- `lane_evaluability/resources_defined` (**unresolved**)

Quoted material findings:

> **EVAL-F1 / F-MSG-RECONSTRUCTION:** The algorithm stores `msgs[n] <- msg_id`
> using one word but later requires rebuilding and returning an earlier random
> 64-byte message. The proof does not specify a retained prefix table, replayable
> random tape, or another mapping from the one-word identifier to the random
> 480-bit group prefix. Such per-group retention could fit the stated setup and
> memory bounds, but importing it would repair the submission…

> **EVAL-F2:** The group-setup conversion is arithmetically incorrect:
> `2^96·1024/430 ≈ 2^97.25`, not less than `2^97`.

Heuristics themselves were **not** the gate: `H-COST-BT-SPARSE` was
established/plausible; `H1-grouped-digests` was plausible. This package **imports
the retained prefix table**, fixes the setup exponent, charges VERIFY Word work,
and tightens F2 selection — keeping all prior cost repairs (c145/4dd/c367/7212 BT).

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
(Briggs–Torczon).

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
   as measured against `verifier/blake3.py` / prior packages).
4. Loop `m15=0…2^{32}-1` executing §2.3.

**Group-setup Word budget:** ≤512 ops/group (236 body + RNG/pack/stores + margin).

### 2.3 Per-message step

1. Partial-eval body → `K_full` (252 Word ops; FF = 8 digest xors; no trailing
   masks). Pack into one register (**14**).
2. `idx = top140(K_full)`.
3. Run `BT_probe_insert` (§2.4).
4. On `VERIFY(s)`: run §2.5; on accept, halt; count toward `V_max=8`.
5. Loop control: `m15←m15+1`; compare; branch (**3**).

### 2.4 Procedure `BT_probe_insert` (≤28 Word ops)

256-bit word RAM. Loads/stores/compares/branches/adds = 1 op each.

```
s <- LOAD sparse[idx]                 # 1
if not (s < n): goto INSERT           # 1 cmp + 1 br
d <- LOAD dense[s]                    # 1
if d != idx: goto INSERT              # 1 cmp + 1 br
Ks <- LOAD keys[s]                    # 1
if Ks != K_full: return DISCARD       # 1 cmp + 1 br
return VERIFY(s)                      # 1 br
INSERT:
STORE sparse[idx] <- n                # 1
STORE dense[n] <- idx                 # 1
STORE keys[n] <- K_full               # 1
STORE recs[n] <- (g ∥ m15)            # 1   ← not a free-floating msg_id
n <- n + 1                            # 1
return CONTINUE                       # 1 br
```

Worst-case DISCARD ≤9 ops; INSERT ≤15; VERIFY-decide ≤9. **Charged envelope: 28**
Word ops (includes ≤10 address-arithmetic margin). Compressions occur **only**
inside §2.5.

Declared score-critical cost heuristic **`H-COST-BT-SPARSE`**: this envelope.

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

## 3. Unconditional time ledger

| component | ops/msg | where charged |
| --- | ---: | --- |
| Inner partial-eval body | 252 | §2.3 |
| Pack `K_full` | 14 | §2.3 |
| Briggs–Torczon + K compare | 28 | §2.4 / `H-COST-BT-SPARSE` |
| m15 loop control | 3 | §2.3 |
| **Per-message total** | **297** | |

Plus once-per-run / rare:

| component | bound | where |
| --- | --- | --- |
| Init `n←0` | 1 Word | §2.1 |
| Group setup | ≤512 Word/group × `2^{96}` | §2.2 |
| VERIFY compressions | ≤`2·V_max=16` units | §2.5 |
| VERIFY Word work | ≤640 Word → `<2` units | §2.5 |

Group-setup units: `2^{96}·512/430 = 2^{96}·512/430`.
Since `512/430 < 1.191`, this is `< 2^{96}·1.191 < 2^{96.25} < 2^{97}`.
(Prior `7212` used 1024 and incorrectly claimed `<2^{97}`; that was ≈`2^{97.25}`.)

**No expectations in the inequality.**

Let `U = 297/430`. Exact: `log2(U)+128 ≈ 127.466126`.

    T ≤ N·U + 16 + 2 + 2^{97}
      = 2^{128}·297/430 + 18 + 2^{97}
      < 2^{128}·297/430 + 2^{98}
      < 0.6906977·2^{128} + 2^{98}
      < 0.690698·2^{128}
      < 2^{127.46613} < 2^{127.467}.

Claim **`time_log2 = 127.467`**.

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

### 5.2 `H-COST-BT-SPARSE`

The §2.4 procedure fits in ≤28 charged primitives per message on the organizer
256-bit word RAM, including one 256-bit `K_full` compare and address margin.
Evidence: §2.4 op list. No page-walk model beyond 1-op word addressing.

## 6. Experiments

| id | layout | w |
| --- | --- | ---: |
| `b3r2-grouped-spread` | 32×32 | 20 |
| `b3r2-grouped-spread-16` | 16×16 | 16 |
| `b3r2-grouped-spread-24` | 64×64 | 24 |
| `b3r2-single-group` | 1×1024 | 20 |

## 7. Memory

- `sparse`: `2^{140}` entries × **32-byte** (256-bit) words = `2^{145}` bytes.
- `dense/keys/recs`: ≤`2^{128}` × 3 × 32 = `2^{128}·96` bytes.
- `prefixes`: `2^{96}` × 2 × 32 = `2^{96}·64 = 2^{102}` bytes.
Peak `< 2^{146}`. Claim `memory_log2_bytes=146`.
Never-cleared `sparse` needs no `2^{140}` zeroing pass.

## 8. Comparison

| package | time_log2 | notes |
| --- | ---: | --- |
| `7212ec23` | 127.467 | `not_evaluable` (EVAL-F1/F2) |
| Public ~127.481 | 127.481 | untrusted |
| **This package** | **127.467** | prefix table + fixed setup exponent |
| `8e870aed` | 127.524 | awaiting (kept) |

## 9. Evidence summary

Algorithm/reconstruction §2; cost §3; probability §4; heuristics §5; experiments
§6; memory §7. Empty certificates. `submission_state=ready`.
