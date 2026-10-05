# SHA3-256 prefix rounds 0–5: unconditional 32-bit radix (visible spare, 128.2465)

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is reported only.

Selected lane: exploratory. Target: `sha3-256-r6-prefix-v1`.
Total charged time ≤ 2^128.2465, peak memory ≤ 2^136 bytes, success probability ≥ 0.39.
Proposed scalar: **128.2465**. Generic analytic construction; not a cryptanalytic
advance. `baseline_improved: sha3-256-r6-nominal-v2` is the required nominal
identifier only; nominal 128 is not an established attack.

**Board context.** Zero-spare 128.24 was refuted. Awaiting-review tickets including
**128.2473** (`59b3a6e2`) are left alone. This package keeps **visible spare on
every hot path** (gen **65**=+1, per-pass **29**=+1, scan **17**=+1) while
tightening to **128.2465**. Empty heuristics. DP v2 closed: sha3r6 n=32 @ k0=1.10
was 0.3875&lt;0.39 — no DP submit.

## 1. Exact complete hash and legal messages

Let `Q = ceil(9943 * 2^128 / 10000)` and `N = 2^256`. Numerically
`Q = 338342757429489101165234520331412045824`.
Messages: 64-byte `LE32(u)||LE32(v)` (`|D|=2^512`).

SHA3-256: rate 1088, capacity 512, all-zero IV, suffix `0x06`+pad10*1, prefix
rounds 0..5, full 256-bit digest. One absorption.

H(u,v): zero 25 lanes; load u,v into A[0..7]; A[8]=0x06;
A[16]=0x8000000000000000; six Keccak-f rounds (standard rho, RC[0..5]); return
`d=A[0]|(A[1]<<64)|(A[2]<<128)|(A[3]<<192)`. One permutation = 1 unit;
other word ops = 1/1626.

## 2. Algorithm

Src/Dst: Q records of `(digest,u,v)`. Cnt/Pos length `2^32`.
Generate without bulk-zeroing arrays (full overwrite). LSD 32-bit radix, 8
passes. Adjacent scan; recompute H on distinct equal-digest messages.

## 3. Unconditional success

Schur/averaging: `Q(Q-1)/(2N)=0.494316245 > -ln(0.61)` ⇒ `Pr(E)>0.390012`.
`Pr(R)<2^{-256}`. Success > 0.39. Heuristics empty.

## 4. Cost (C=1626) — visible spare

**H wrapper:** ≤56 ordinary ops.
**Generate:** 2 rand + 56 wrapper + 3 stores + loop/spare → **65**
(vs itemized ~64: **+1 spare**; vs awaiting 128.2473's 66: −1).
**Radix per record/pass:** 28 itemized + **1 spare = 29**.
**Scan per pair:** **17** (vs tight 16: **+1 spare**).
**Tables:** ≤2^37. **Fixed load:** 2^30. No Src/Dst bulk zero.

| Phase | Perms | Ordinary ops |
| --- | ---: | ---: |
| Fixed load | 0 | 2^30 |
| Generate | Q | 65 Q |
| 8×29/record | 0 | 232 Q |
| Table O(1) | 0 | 2^37 |
| Scan | 0 | 17 Q |
| Verify | ≤2 | 2^14 |

    W ≤ 314 Q + 138512711680
    T ≤ Q + 2 + 314Q/1626 + 138512711680/1626
      < 2^128.246483

Exact: `log2 T ≈ 128.246483 < 128.2465`. Claim **128.2465**.

Wcoef **314** vs refuted 304 (+10 spare total) and vs awaiting 315 (−1).

`preprocessing_log2: 30` (fixed load only).

## 5. Memory

`M ≤ 192Q + 2^38 + 2^24 < 2^136`.

## 6. Limitations / DP close-out

Analytic birthday bound only. Spare intentional after 128.24 refutation.
DP v2 complete: sha3r6 n=32 collision_rate **0.3875** at k0=1.10 (gate fail);
sha3r24 n=32 was **0.4375** (control only). No H-RF DP package. PERM6 is not a
v5 discount (still 1 unit/permutation, C=1626).

## 7. Provenance

Tightens awaiting-review 128.2473 with continued visible spare on all three hot
paths. Fresh review required. Leaves awaiting-review tickets untouched.
