# SHA3-256 prefix rounds 0–5: DP collision search (K0=1.10·2^128, w=36)

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is reported only.

Lane: exploratory. Target: `sha3-256-r6-prefix-v1`.
Charged time ≤ 2^128.18, memory ≤ 2^120 bytes, success ≥ 0.39 under **H-RF**.
Proposed scalar: **128.18**.

Revision of validating `4d2e7fb3` @ 128.21: **same K0 and H-RF evidence**, tighter
ordinary-op claim **w=36** (+4 spare over frozen tight ≤32). Generic DP only.

## 1. Exact target and step map

SHA3-256 prefix rounds 0..5; rate 1088; capacity 512; IV zero; suffix `0x06`+pad.
`msg(x)` = 32-byte LE encoding of 256-bit word `x`.
`f(x) = SHA3-256-r6(msg(x))` as a 256-bit word. One `f` = one perm unit + w ordinary ops.

## 2. Machine model

collision-frontier-v5; C=1626; total work across processors.

## 3. Parameters

| Symbol | Value |
|--------|-------|
| K0 | 1.10 · 2^128 |
| θ | 2^-32 |
| L | 2^40 |
| w | **36** (was 40) |

## 4. Algorithm

Single-processor van Oorschot–Wiener DP search with RELOCATE on repeated
distinguished points (same as prior 128.21 package). Budget K0 evaluations.

## 5. Output correctness (unconditional)

RELOCATE + verify `f(a)=f(b)`, `a≠b` ⇒ ordinary collision. No heuristic.

## 6. Success probability under H-RF

Under H-RF, contact among K0 evaluations yields

    1 - exp(-K0(K0-1)/(2N)) ≈ 1 - exp(-1.10²/2) ≈ 0.4539 > 0.39

after standard DP bad-event deductions with margin. **≥0.39 under H-RF.**
Same probability argument as 128.21; w change does not affect Pr.

## 7. Time bound — frozen opcount w=36

Tight envelope ≤32 ordinary ops/eval (overwrite absorb 12, load 4, pad 2,
pack 4, DP test 3, loop 4, contingency 3). Claimed **w=36** = tight + **4 spare**.

    T ≤ K0 · (1 + 36/1626) = 1.10 · 2^128 · (1 + 36/1626)
      ⇒ log2 T ≈ 128.169097 < 128.18

Dictionary/RELOCATE extras ≪ main term. Claim **128.18**.
`preprocessing_log2: 20`.

## 8. Memory

≤ 2^120 bytes (`memory_log2_bytes: 120`). Unscored.

## 9. Evidence for H-RF (unchanged tables)

Preregistered truncated DP campaigns (`research/dp_n32_rfcal_preregister.json`).

### Stress @ k0=1.10 family (sha3r6 n=32, trials=120)

| k0 | base_seed | collision_rate | ≥0.39 |
|---:|----------:|---------------:|:-----:|
| 1.10 | 301100 | **0.4000** | yes |
| 1.12 | 301120 | **0.4333** | yes |
| 1.14 | 301140 | **0.3917** | yes |

### RF@0.9944 sha3r6 — failed (reason K0 stays 1.10·2^128)

n=20..32 all coll&lt;0.39 (0.335, 0.355, 0.350, 0.375).

No new collision trials this revision — opcount-only change.

## 10. Limitations

H-RF unproven; truncated ≠ full-n. Exploratory only. No invented 6-round
SHA3-256 classical differential.

## 11. Provenance

Replaces validating 128.21 (w=40) with w=36 spare-preserving tighten.
Leaves awaiting radix tickets alone.
