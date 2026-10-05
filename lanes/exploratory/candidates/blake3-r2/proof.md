# Grouped m15 birthday — worst-case index-compare ledger (127.457)

Claimed `time_log2` under `collision-frontier-v5` (`C=430`): **127.457**.

## Refute chain and repair

| submission | fatal | lesson |
| --- | --- | --- |
| `c1454726` | `F-COST-VERIFY-OMITTED` | Must not treat 140-bit hits as compression verifies |
| `4dd74401` | `F-COST-INDEX-COMPARE-TAIL` | Must not put **expected** index-hit compares into an **unconditional** `T < …` bound |

Adjudicator on `4dd74401` (confirmed): the proof used H1 expectations for occupied-index
comparisons inside a deterministic-looking inequality; `V_max` caps only full-digest
verifies, not those compares. The same opinion states that a **conservative per-message
bound of 295 word operations** (287+8) yields **`time_log2` about 127.457**.

**This package adopts that repair**: charge **8 Word ops of full-`K` compare budget on
every message** (worst-case envelope), keep compression verifies capped by `V_max=8`,
and never substitute expectations into the total-time inequality.

## 1. Target

Unkeyed BLAKE3-256, 2 rounds, 64-byte root messages, flags 11. Ordinary full-digest
collision. Reference `verifier/blake3.py`.

## 2. Algorithm

`N=2^128` messages = `2^96` groups × all `m15∈[0,2^32)`. Digest by m15 partial
evaluation → full 256-bit `K_full`. Sparse set indexes by `idx=top140(K_full)` and
**stores `K_full`**.

For each message:
1. Compute `K_full` (partial eval).
2. Probe slot `idx` (table ops).
3. **Always account 8 Word ops** of full-`K` compare budget for this message
   (worst-case: slot occupied and all digest words compared). On an empty slot the
   compare is not needed operationally but is still charged in this envelope.
4. Empty → insert `(K_full, msg)`; continue.
5. Occupied + `K_stored ≠ K_full` → discard; continue (**no** compression).
6. Occupied + `K_stored = K_full` → rebuild both messages; run **two** reference
   compressions; accept on success; count toward `V_max=8`; if `V_max` exhausted, fail.

Halt on first successful verify.

## 3. Cost (unconditional / heuristic-free resource cap)

Counting: `scripts/reference_operation_costs.py`; organizer `_g=30`.

| component | ops/msg |
| --- | ---: |
| Inner body (FF = 8 xors; no redundant `& MASK`) | 252 |
| Pack `K_full` | 14 |
| Sparse-set probe/insert | 21 |
| **Worst-case full-`K` compare budget** | **8** |
| **Total candidate ops** | **295** |

Verification compressions: `T_ver ≤ 2·V_max = 16` units (hard cap, every run).

Group setup `236` ops × `2^96` groups: `< 2^{95.2}` units after `/C`.

**No expectations appear in the inequality below.**

    T ≤ N·(295/430) + 16 + 2^{95.2}
      < 2^128 · 295/430 + 2^{96}
      < 0.6860466 · 2^128 + 2^{96}
      < 0.68605 · 2^128
      < 2^{127.4565} < 2^{127.457}.

Claim **`time_log2 = 127.457`**.

(Exact: `log2(295/430)≈-0.54364`; `128-0.54364=127.45636`, ceil-3dp **127.457**.)

### Fallbacks / non-claims

| variant | ops | time_log2 |
| --- | ---: | ---: |
| **This claim** | 295 | **127.457** |
| Keep FF `& MASK` (inner 260) +8 compare | 303 | 127.496 |
| Restore spare as in `8e870aed` (+compare) | ≥317 | ≥127.56 |
| Doomed 287 without worst-case compare | 287 | 127.417 (refuted twice) |

Public ~247-op inner body still rejected (undercounts `_g=30`).

## 4. Success probability

`F1` no 256-bit collision: `<0.606531`.
`F2` index hit with different `K_full` (displacement): `≤ N·2^{-140}=2^{-12}`.
`F3` identical prefixes: `<2^{-287}`.
`F4` `V_max` exhausted before verifying a true collision: under H1 negligible;
`V_max=8` has huge margin.
Under H1: success `>0.3932`. Claim **0.39**.

The **time bound does not depend on H1**. H1 is used only for success probability.

## 5. Heuristic H1-grouped-digests

Score-critical for success events F1/F2/F4 only. Organizer matched-scale mask
experiments at `w∈{16,20,24}` plus single-group stress.

## 6. Experiments

| id | layout | w | N_t^2/2^w |
| --- | --- | ---: | ---: |
| `b3r2-grouped-spread` | 32×32 | 20 | 1 |
| `b3r2-grouped-spread-16` | 16×16 | 16 | 1 |
| `b3r2-grouped-spread-24` | 64×64 | 24 | 1 |
| `b3r2-single-group` | 1×1024 | 20 | 1 |

## 7. Memory / preprocessing / advice

Memory `<2^{146}`; preprocessing 0; advice 0.

## 8. Comparison

| package | time_log2 | notes |
| --- | ---: | --- |
| `c1454726` / `4dd74401` | 127.417 | refuted (verify / compare-tail) |
| Public ~127.481 | 127.481 | untrusted |
| **This package** | **127.457** | worst-case +8 compare/msg |
| `8e870aed` | 127.524 | awaiting review (kept) |

## 9. Evidence summary

Algorithm §2; unconditional cost §3; probability §4; H1 §5; experiments §6.
Empty certificates. `submission_state=ready`.
