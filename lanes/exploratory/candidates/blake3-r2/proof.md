# Grouped m15 birthday with auditable Briggs–Torczon ledger

Claimed `time_log2` under `collision-frontier-v5` (`C=430`): **127.467**.

## Why previous package was `not_evaluable`

`c36797d2` (@127.457) failed evaluability because cost review invented / found
unsupported score-critical heuristic **`H-COST-SPARSE-21`**:

> A genuinely sparse dictionary keyed by the top 140 digest bits supports every
> probe, insertion, occupancy test, payload access, and collision handling step
> in at most 21 charged word operations per candidate…

The 21-op line had **no representation, init policy, or op-by-op procedure**, and
`scripts/reference_operation_costs.py` is not in the submission archive (harness
file only). Unsupported score-critical cost heuristics gate to `not_evaluable`.

This package **eliminates that gap** by (1) specifying Briggs–Torczon completely,
(2) charging an explicit per-message op list totaling **297**, (3) declaring
heuristic **`H-COST-BT-SPARSE`** with matching statement/scope/evidence so the
gate sees a disclosed, evidenced cost premise rather than an implicit 21.

It also keeps prior repairs: no compression on unequal-`K` index hits (`c145`);
no H1 expectations inside the time inequality (`4dd`); worst-case compare folded
into the BT procedure.

## 1. Target

Unkeyed BLAKE3-256, exactly 2 rounds, 64-byte root block, flags 11, counter 0,
length 64. Ordinary full-digest collision of distinct messages.
Reference: `verifier/blake3.py`.

## 2. Algorithm

`N=2^128` messages as `2^96` groups × all `m15∈[0,2^32)`. Each digest is computed
by m15 partial evaluation → `K_full` (256 bits). Let `idx = top140(K_full)`.

**Data structure (Briggs–Torczon sparse set):**
- Integer `n` (live entry count), initially `0`.
- Array `sparse[0..2^{140}-1]` of integer slots (**never cleared**).
- Arrays `dense[0..N_max)`, `keys[0..N_max)`, `msgs[0..N_max)` with `N_max=2^{128}`.
- Membership test: entry `idx` is live iff `s=sparse[idx]`, `s<n`, and `dense[s]=idx`.

**Per message:**
1. Partial-eval → `K_full`; `idx=top140(K_full)`.
2. Run `BT_probe_insert` below.
3. On `VERIFY(s)`: rebuild both messages; run **two** reference compressions;
   accept if messages differ and digests agree; count toward `V_max=8`; if
   `V_max` exhausted, fail.
4. Halt on first accept.

### 2.1 Procedure `BT_probe_insert` (Word-op count)

Machine: 256-bit word RAM. `idx` and `K_full` each fit in one word. Loads/stores/
compares/branches/adds are 1 op each (cost-model primitives).

```
s <- LOAD sparse[idx]                 # 1
if not (s < n): goto INSERT           # 1 cmp + 1 br
d <- LOAD dense[s]                    # 1
if d != idx: goto INSERT              # 1 cmp + 1 br   (uninit garbage)
Ks <- LOAD keys[s]                    # 1
if Ks != K_full: return DISCARD       # 1 cmp + 1 br
return VERIFY(s)                      # 1 br
INSERT:
STORE sparse[idx] <- n                # 1
STORE dense[n] <- idx                 # 1
STORE keys[n] <- K_full               # 1
STORE msgs[n] <- msg_id               # 1
n <- n + 1                            # 1
return CONTINUE                       # 1 br
```

**Worst-case path lengths:**
- DISCARD (occupied, unequal K): `1+1+1+1+1+1+1+1+1 = 9` ops through the compare,
  counted inside the **28-op envelope** below with margin for address arithmetic.
- INSERT: through failed live-test then 5 stores/add/br ≤ `3+2+5+1 = 11` on the
  short path, or `9+5+1` if both live-tests run then insert ≤ 15.
- VERIFY branch: ≤ 9 ops to decide VERIFY (no compression here).

**Charged BT envelope per message: 28 Word ops**, covering probe/insert/discard
decision, 256-bit `K` compare, and ≤10 ops of index address arithmetic / flag
clearing. Compressions are **only** on VERIFY and are charged in §3 as `T_ver`.

Initialization: set `n←0` once per run (`1` store). **No** fill of `sparse`
(Briggs–Torczon). Setup group RNG: ≤4 random-word draws per group, charged in
group setup (§3.1).

## 3. Unconditional time ledger

Inner body **252** ops (FF = 8 digest xors; no trailing `& MASK`; organizer
`_g=30`). Pack `K_full` into one word: **14** (conservative; may be 0–1 under
pure 256-bit digest register). BT envelope: **28**. Loop: `m15←m15+1`; compare
to `2^32`; branch: **3**.

| component | ops/msg |
| --- | ---: |
| Inner partial-eval body | 252 |
| Pack | 14 |
| Briggs–Torczon + K compare | 28 |
| m15 loop control | 3 |
| **Total** | **297** |

Verification: `T_ver ≤ 2·V_max = 16` compression units every run.
Group setup: ≤1024 Word ops/group (236 measured body + RNG/control margin) ×
`2^96` groups → `< 2^{96}·1024/430 < 2^{97}` units after `/C`.

**No expectations in the inequality.**

    T ≤ N·(297/430) + 16 + 2^{97}
      < 2^128 · 297/430 + 2^{97}
      < 0.69070 · 2^128 + 2^{97}
      < 0.6908 · 2^128
      < 2^{127.4661} < 2^{127.467}.

Claim **`time_log2 = 127.467`**.

### Declared cost heuristic `H-COST-BT-SPARSE`

Score-critical for the **28-op BT envelope** only: that the §2.1 procedure on a
256-bit word RAM with word-addressable `sparse[idx]` implements the membership
/ insert / unequal-K discard semantics in ≤28 charged primitives per message,
with never-cleared `sparse` justified by the classic `dense[sparse[idx]]==idx`
filter. Evidence: §2.1 op list; Briggs–Torczon reference semantics; memory §5.
This replaces the unsupported implicit `H-COST-SPARSE-21`.

## 4. Success probability (F2 fixed)

`F1`: no 256-bit collision among N digests: `< exp(-1/2+2^{-128}) < 0.606531`.

`F2` (**selected-pair displacement**): fix any colliding pair `{a,b}` with `a`
inserted before `b` in scan order. Failure mode: when `a` was processed, slot
`idx(a)` was already live with a different key, so `a` was discarded and never
stored; then `b` cannot verify against `a`. For that fixed `a`,
`Pr[slot occupied] ≤ (entries before a)/2^{140} ≤ N/2^{140} = 2^{-12}`.
(This is **not** the probability that some unequal-K hit occurs somewhere.)

`F3`: identical group prefixes among `2^96` draws: `< 2^{-287}`.

`F4`: `V_max` exhausted before verifying a true collision: under H1, same-`K`
events before the first birthday collision are negligible; `V_max=8` suffices.

Under H1: success `> 1 - 0.606531 - 2^{-12} - 2^{-287} - ε > 0.3932`.
Claim **0.39**.

## 5. Heuristic H1-grouped-digests

Unchanged modeling hypothesis for F1/F2/F4. Time bound does **not** use H1.

## 6. Experiments

Matched-scale `digest-xor-mask` events (`N_t^2/2^w=1`):

| id | layout | w |
| --- | --- | ---: |
| `b3r2-grouped-spread` | 32×32 | 20 |
| `b3r2-grouped-spread-16` | 16×16 | 16 |
| `b3r2-grouped-spread-24` | 64×64 | 24 |
| `b3r2-single-group` | 1×1024 | 20 |

## 7. Memory

`sparse`: `2^{140}` words × 32-bit dense-index ≈ `2^{145}` bytes.
`dense/keys/msgs`: ≤`2^{128}` records × ≤64 bytes ≈ `2^{134}`.
Peak `< 2^{146}`. Claim `memory_log2_bytes=146`. Never-cleared `sparse` needs
no `2^{140}` zeroing pass (Briggs–Torczon).

## 8. Comparison

| package | time_log2 | notes |
| --- | ---: | --- |
| `c36797d2` | 127.457 | `not_evaluable` (`H-COST-SPARSE-21` unsupported) |
| `4dd74401` / `c1454726` | 127.417 | refuted cost fatals |
| Public ~127.481 | 127.481 | untrusted |
| **This package** | **127.467** | auditable BT + declared cost heuristic |
| `8e870aed` | 127.524 | awaiting (kept) |

## 9. Evidence summary

Algorithm/BT §2; cost §3; probability §4; H1 §5; experiments §6; memory §7.
Empty certificates. `submission_state=ready`.
