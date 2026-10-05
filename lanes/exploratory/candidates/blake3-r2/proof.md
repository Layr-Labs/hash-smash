# Grouped partial-evaluation birthday search (verification-accounted)

The scalar below is `time_log2` under `collision-frontier-v5` with `C = 430`.
Claimed scalar: **127.417**.

## Refute lesson from `c1454726`

Failed `c1454726` (same 287-ops candidate ledger) was refuted on
**`lane_cost/F-COST-VERIFY-OMITTED`** (adjudicator **confirmed**):

> The algorithm explicitly performs two charged target compressions for each
> repeated 140-bit table key, but the submitted total-time formula includes only
> 287 word operations per generated message and no verification term.

The defect was **not** the dropped FF `& MASK` or the dropped spare. It was an
ambiguous "on a key match, re-verify" that judges read as charging **two full
compressions on every 140-bit index collision** (~`2^115` encounters under H1 →
~`2^116` omitted units).

**This package repairs that** by separating three events and charging each:

| event | action | charged cost |
| --- | --- | --- |
| empty 140-bit slot | insert `(K_full, msg)` | in 21-op table allowance |
| occupied slot, **`K_full` differs** | discard (F2 displacement) | Word compares only (no compression) |
| occupied slot, **`K_full` equal** | rebuild msgs + **2** reference compressions; accept/fail | ≤ `2·V_max` compression units |

Here `K_full` is the full **256-bit** digest from the partial evaluator. A
140-bit index hit alone never triggers a target compression.

## 1. Target

Unkeyed BLAKE3-256, 2 rounds, 64-byte root messages, flags 11. Ordinary
full-digest collision. Reference `verifier/blake3.py`.

## 2. Algorithm

Constants: `N=2^128` messages as `2^96` groups × `2^32` values of `m15`;
sparse-set index uses the top **140** bits of `K_full`; `V_max=8`.

1. For each group: fix uniform `m0..m14`; for each `m15`:
   - compute digest by m15 partial evaluation → `K_full` (256 bits);
   - let `idx = top140(K_full)`;
   - **if slot `idx` empty:** store `(K_full, message)`; continue;
   - **if slot occupied with `K_stored ≠ K_full`:** discard this message
     (compare at most eight 32-bit words / one 256-bit compare); continue;
   - **if `K_stored = K_full`:** regenerate both messages from stored ids;
     recompute both digests with **two full reference compressions**;
     if messages differ and digests agree, **accept** and halt;
     count one verification toward `V_max`; if `V_max` exhausted, **fail**.
2. If the scan ends without accept, fail.

Partial evaluator bit-exact vs `blake3(msg,2)` on large random samples.

## 3. Why verification is O(1) in the charged cap

Under H1, digests are uniform. The first time `K_full` repeats is a birthday
collision on 256 bits. Expected number of same-`K_full` events in a full scan
is `≈ N(N-1)/2^{257} < 1`. The algorithm **halts on first successful verify**,
so the number of compression-verify calls on a successful path is **1** (two
compressions). On failure paths it is 0. The hard cap `V_max=8` makes the
resource bound **heuristic-free** even for pathological maps: at most 16
target-compression units for verification on every run.

False 140-bit collisions do **not** invoke compressions—only Word compares.

## 4. Word-op candidate ledger (unchanged 287) + verify term

Counting: `reference_operation_costs.py` convention; organizer `_g` = 30.
Inner body **252** (FF = 8 xors; no trailing `& MASK`—lanes already masked by G).
Pack **14** + sparse-set probe/insert **21** = **35**. No spare.
Per-message candidate ops: **287**.

Index-hit full-`K` compares: ≤ 8 Word ops each. Expected index hits
`≲ N·N/2^{140} = 2^{116}`; compare charge
`< 2^{116}·8/430 = 2^{-12}·8/430·2^{128} < 10^{-5}·2^{128}`.

Verification: `T_ver ≤ 2·V_max = 16` compression units.

    T < 2^128 · 287/430 + 10^{-5}·2^128 + 16
      < (0.66744186 + 0.00001)·2^128 + 16
      < 0.66746·2^128
      < 2^{127.4168} < 2^{127.417}.

Claim **`time_log2 = 127.417`**.

### Fallbacks

| variant | ops/msg + verify | time_log2 |
| --- | --- | ---: |
| **This claim** | 287 + ≤16 | **127.417** |
| Keep FF `& MASK` (inner 260), no spare | 295 + ≤16 | 127.457 |
| Restore spare (`8e870aed` ledger) | 309 + ≤16 | ≈127.524 |
| Reload 27 constants | 314 + ≤16 | ≈127.546 |

Public ~247-op inner body still rejected (undercounts `_g=30`).

## 5. Success probability

`F1` no 256-bit collision: `<0.606531`.
`F2` displacement (index collision, different `K_full`): `≤ N·2^{-140}=2^{-12}`.
`F3` identical prefixes: `<2^{-287}`.
`F4` `V_max` exhausted before a true collision is verified: under H1, same-`K`
events before the first true birthday collision are negligible; `V_max=8`
leaves huge margin. Under H1: success `>0.3932`. Claim **0.39**.

## 6. Heuristic H1-grouped-digests

Unchanged score-critical modeling hypothesis for F1/F2/F4. Organizer matched-scale
mask experiments at `w∈{16,20,24}` plus single-group stress (Section 7).

## 7. Experiments

| id | layout | w | N_t^2/2^w |
| --- | --- | ---: | ---: |
| `b3r2-grouped-spread` | 32×32 | 20 | 1 |
| `b3r2-grouped-spread-16` | 16×16 | 16 | 1 |
| `b3r2-grouped-spread-24` | 64×64 | 24 | 1 |
| `b3r2-single-group` | 1×1024 | 20 | 1 |

## 8. Memory / preprocessing / advice

Memory `<2^{146}`; `preprocessing_log2=0`; advice 0.

## 9. Comparison

| package | time_log2 | notes |
| --- | ---: | --- |
| `c1454726` (refuted) | 127.417 | omitted verify term / ambiguous key-match |
| `8e870aed` | 127.524 | awaiting review |
| Public ~127.481 | 127.481 | untrusted 247-op inner |
| **This package** | **127.417** | verify capped + full-K vs index clarified |

## 10. Evidence summary

Algorithm §2–3; cost §4 (including `F-COST-VERIFY-OMITTED` repair); probability §5;
H1 §6; experiments §7. Empty certificate manifest. `submission_state=ready`.
