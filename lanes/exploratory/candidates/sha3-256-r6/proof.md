# SHA3-256 prefix rounds 0–5: distinguished-point collision search (K0=1.10·2^128)

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is reported only.

Selected lane: exploratory. Target: `sha3-256-r6-prefix-v1`.
Total charged time ≤ 2^128.21, peak memory ≤ 2^120 bytes, success probability ≥ 0.39
under heuristic **H-RF**. Proposed scalar: **128.21**.

This is a generic van Oorschot–Wiener distinguished-point (DP) ordinary-collision
search. It is not a cryptanalytic differential advance. `baseline_improved:
sha3-256-r6-nominal-v2` is the required nominal identifier only; nominal 128 is
not an established attack. Awaiting-review unconditional **128.2465** is left
alone; this package is an independent structural claim.

## 1. Exact target and step map

SHA3-256 with prefix rounds 0..5: rate 1088, capacity 512, IV zero, suffix `0x06`
+ pad10*1, full 256-bit digest. One absorption of a 32-byte message.

Define `msg(x)` as the 32-byte little-endian encoding of the 256-bit word `x`.
Define `f(x) = SHA3-256-r6(msg(x))` interpreted as a 256-bit word. One evaluation
of `f` issues exactly one selected-round sponge permutation (1 time unit) plus
ordinary word operations itemized in Section 7.

## 2. Machine model

Classical probabilistic 256-bit word RAM per `collision-frontier-v5`.
Reference cost C = 1626 for `sha3-256-r6`. Parallelism charges total work.

## 3. Parameters

| Symbol | Value |
|--------|-------|
| N | 2^256 |
| K0 | 1.10 · 2^128 |
| θ | 2^-32 (distinguished: low 32 bits zero) |
| L | 2^40 (max chain length ≈ 16/θ order) |
| w | 40 ordinary ops per `f`-evaluation (visible spare) |

K0 is **inflated** above the birthday-scale factor ≈0.9944 because truncated
sha3-r6 RF-calibration at 0.9944 missed empirical rate 0.39 (Section 9).

## 4. Algorithm (single processor)

Maintain a dictionary of distinguished points. While fewer than K0 evaluations:

1. Draw a uniform random start `s`.
2. Walk `x ← f(x)` from `s` for at most L steps, counting evaluations.
3. On a distinguished point `y`: if `y` is new, store `(start, length)`; if `y`
   repeats a prior record, **RELOCATE** (length-align then lockstep) to obtain
   predecessors `(a,b)`. If `a ≠ b` and `f(a)=f(b)`, output `(msg(a), msg(b))`.

Halt with failure if the budget is exhausted without a collision.

## 5. Output correctness (unconditional)

RELOCATE returns distinct predecessors of a common image under `f` when a
nontrivial meeting exists. Verifying `f(a)=f(b)` with `a≠b` yields an ordinary
collision of the selected target on distinct 32-byte messages. No heuristic.

## 6. Success probability under H-RF

**Heuristic H-RF** (claim.json): unevaluated queries to `f` behave as a random
function.

Under H-RF, the probability of at least one trailing collision among K0
distinct-image evaluations is at least

    1 - exp(-K0(K0-1)/(2N)) ≈ 1 - exp(-1.10²/2) ≈ 0.4539 > 0.39,

after standard DP bad-event deductions of the van Oorschot–Wiener shape (same
start collision, fruitless cycles, etc.) which are O(K0·θ·K0/N) and smaller
order terms at these parameters; a 0.01 absolute margin remains above 0.39.
Formal claim: **success probability ≥ 0.39 under H-RF**.

H-RF is score-critical and unproven. Section 9 gives truncated supporting
experiments at k0_factor=1.10.

## 7. Time bound (unconditional)

Per `f`-evaluation ordinary ops (visible spare; tight sketch ≈35):

| Step | Spare claim |
|------|------------:|
| Rebuild/absorb 32-byte x + suffix/pad | 28 |
| Pack digest word | 6 |
| DP test + loop/index | 6 |
| **Total w** | **40** |

PERM6 itself costs 1 unit (not in w).

    T ≤ K0 · (1 + w/C) = 1.10 · 2^128 · (1 + 40/1626)
      ⇒ log2 T ≈ 128.17256

Additive DP-table and RELOCATE extras are ≪ 2^-20 relative to K0 at these
parameters (dictionary ops O(1) amortized per DP; ≤3L evaluations for one
relocate). Claim **128.21** includes explicit margin above 128.17256
(approximately +2% on the ordinary envelope, then round up).

`preprocessing_log2: 20` covers code/constants load only.

## 8. Memory

DP dictionary stores O(K0·θ) ≈ 1.10·2^96 records of O(1) words each, plus
O(L) scratch for relocate — bounded by **2^120** bytes with margin.
`memory_log2_bytes: 120`. Memory is unscored.

## 9. Evidence for H-RF (truncated DP campaigns)

Preregistered script `research/dp_preregister_n32_rfcal.py` (research tree;
methodology mirrored here). Predicate: collision found within
`ceil(k0_factor · 2^{n/2})` evaluations on n-bit truncations of `f`.

### 9.1 Stress at inflated factor (Gate A — pass)

sha3r6, n=32, t=8, trials=120:

| k0_factor | base_seed | collision_rate | ≥0.39 |
|----------:|----------:|---------------:|:-----:|
| 1.10 | 301100 | **0.4000** | yes |
| 1.12 | 301120 | **0.4333** | yes |
| 1.14 | 301140 | **0.3917** | yes |

### 9.2 Birthday-scale calibration (fail → inflate K0)

At k0_factor=0.9944, sha3r6 collision rates for n∈{20,24,28,32} were all
**below** 0.39 (0.335, 0.355, 0.350, 0.375). Therefore this package does **not**
claim K0≈0.9944·2^128; it uses **1.10·2^128**.

### 9.3 Sensitivity

H-RF affects only success probability. If truncated rates near K0 fell short by
a small δ, restoring 0.39 would require a modest K0 increase; the claimed
128.21 still has ledger margin under the live unconditional 128.2465 at w=40.

## 10. Literature / limitations

No classical ordinary-collision attack on **SHA3-256 with 6 rounds** below
birthday is claimed or cited as a dependency (Guo et al. 2022 classical 6-round
result is for SHAKE128; SHA3-256-r6 classical below birthday is not established
in that line). This package is generic DP under H-RF.

Exploratory qualification only (`plausible_not_refuted`). Heuristic may be
refuted by better experiments or analysis.

## 11. Provenance

Structural alternative to exhausted unconditional radix spare
(gen65/pp29/scan17 @ 128.2465). Forbidden zero-spare paths not used.
