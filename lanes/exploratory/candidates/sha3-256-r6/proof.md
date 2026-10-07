# SHA3-256 prefix rounds 0–5: unconditional 128-bit-digit 2-pass radix birthday (128.14)

The scalar is `time_log2` under `collision-frontier-v5` (C = 1626); memory is reported only.
Lane: exploratory. Target: `sha3-256-r6-prefix-v1`. Attack: ordinary collision.
Total charged time < 2^128.1305 ≤ 2^128.14. Peak memory < 2^136 bytes. Success probability > 0.39.
Heuristics: **none**. This is a generic birthday construction and does not advance cryptanalysis.
`baseline_improved: sha3-256-r6-nominal-v2` is the required identifier only.

This package is self-contained. Every procedure the bound depends on is spelled out below.

## 1. Target function and messages

`N = 2^256`, `Q = ceil(9943·2^128/10000) = 338342757429489101165234520331412045824`.
A message is 64 bytes `LE64(u0)||…||LE64(u7)`. Equivalently it is the pair (u, v) of two 256-bit words, so `|D| = 2^512`.
H(u, v): state A[0..24] = 0. XOR the eight message lanes into A[0..7]. A[8] ^= 0x06, A[16] ^= 0x8000000000000000
(SHA3 suffix plus pad10*1 within the 1088-bit rate, single block). Apply Keccak-f[1600] rounds 0..5
(standard θ ρ π χ ι, RC[0..5]). Output d = A[0] | A[1]<<64 | A[2]<<128 | A[3]<<192, the full 256 bits.
Cost: one permutation call = 1 unit. Wrapper (zeroing, loads, pad, packing) ≤ 56 ordinary ops.

## 2. Algorithm (exact)

Arrays: Src[0..Q-1], Dst[0..Q-1] of 3-word records (d, u, v); Cnt[0..2^128-1], one word each.

```
GENERATE: for i in 0..Q-1: u <- rand256(); v <- rand256(); d <- H(u,v); Src[i] <- (d,u,v)
for pass p in 0..1:                      # LSD, digit p = bits 128p..128p+127 of d
    for j in 0..2^128-1: Cnt[j] <- 0
    for i in 0..Q-1: k <- (Src[i].d >> 128p) & (2^128-1); Cnt[k] += 1          # histogram
    s <- 0; for j in 0..2^128-1: t <- Cnt[j]; Cnt[j] <- s; s <- s+t            # exclusive prefix sum
    for i in 0..Q-1: k <- digit_p(Src[i].d); Dst[Cnt[k]] <- Src[i]; Cnt[k] += 1  # stable scatter
    swap(Src, Dst)
SCAN: for i in 0..Q-2:
    if Src[i].d == Src[i+1].d and (Src[i].u,Src[i].v) != (Src[i+1].u,Src[i+1].v):
        recompute H on both, check equality, output both messages, halt
output FAIL
```

Correctness: a stable counting sort by 2 consecutive 128-bit digits from least to most significant sorts by
the full 256-bit d (standard LSD invariant: after pass p the records are sorted by the low 128(p+1) bits).
So any two records with equal digests and distinct messages end up in one run of equal digests. Within
a run that contains at least two distinct messages, some adjacent pair is distinct, so SCAN finds it.
The output is recomputed and checked, so any output is a genuine ordinary collision. The algorithm never
outputs a wrong answer. Its only failure mode is FAIL.

## 3. Success probability (unconditional, over the algorithm's coins)

Probability space: the 2Q fresh uniform words. H is fixed, and no assumption on H is used.
Let E be the event that some pair i<j has H(m_i) = H(m_j), and R the event that some pair has m_i = m_j.
Schur-convexity/averaging: for any fixed H: {0,1}^512 -> {0,1}^256, the probability that Q uniform inputs
contain an output collision is a Schur-convex function of the output distribution. So it is minimized
when every digest has exactly 2^256 preimages, i.e. the uniform-output case. Any imbalance in H only
helps the attacker. Balanced bound: `Pr(E) ≥ 1-exp(-Q(Q-1)/(2N))`, with Q(Q-1)/(2N) = 0.494316245 > -ln(0.61),
so Pr(E) > 0.390012. Pr(R) ≤ Q^2/2^513 < 2^-256. Success ≥ Pr(E)-Pr(R) > 0.39.

## 4. Cost ledger (ordinary ops; itemized minimum → charged with visible spare)

| Item | itemized | charged | spare |
|---|---:|---:|---:|
| Generate / record: 2 rand + 56 wrapper + 3 stores + 3 loop/index | 64 | **66** | +2 |
| Histogram / record / pass: load d, shift, mask, addr, load Cnt, add, store, loop | 8 | | |
| Scatter / record / pass: 3 loads, shift, mask, addr, load Cnt, 2 addr, 3 stores, inc, store Cnt, 3 loop | 20 | | |
| Per record per pass (hist+scatter) | 28 | **32** | +4 |
| Scan / adjacent pair: 3 loads ×2 lanes compare, branch, loop | 16 | **18** | +2 |
| Tables / pass: zero 2^128 (≤3 ops/entry) + prefix sum 2^128 (≤5 ops/entry) | 2^131 | | |
| Both passes of table work | | **2^132** | |
| Fixed setup | | 2^30 | |
| Verify (2 perms + 2^14 ops) | | | |

    Wcoef = 66 + 2·32 + 18 = 148
    W ≤ 148·Q + 2^132 + 2^30 + 2^14
    T ≤ Q + 2 + W/1626
    log2 T ≈ 128.130459 < 128.14

The table term 2^132/1626 ≈ 2^121.33 is about 2^-6.7 of Q, and it is included in the total above. The claim keeps 8 ops/record of visible spare.

## 5. Memory

Src+Dst: 2·96·Q bytes < 2^136 (192Q ≈ 2^135.6). Cnt: 2^128 words · 32 bytes = 2^133 bytes. Code/state: 2^24.
Total: 192Q + 2^133 + 2^24 ≈ 2^135.80 < 2^136. Cnt indices (<2^128) and all addresses (<2^136) fit in one 256-bit word, and counts ≤ Q < 2^129 fit in one word. `preprocessing_log2: 30` covers the fixed setup only.

## 6. Why fewer passes is legitimate

The word RAM has 256-bit words, so extracting a 64-bit digit is one shift and one mask, the same cost
as a 32-bit digit. Under v5 the only effect of a wider digit is the larger counting table: 2^128 entries
per pass, zeroed and prefix-summed with every op charged (2^132 ops ≈ 2^121.3 units). A single pass would need 2^256 entries and is infeasible, so 2 passes is the minimum. The structural gain comes from cutting the
number of passes from 8 (50b542cf) to 4 (bda7eb9e) to 2 over Q records, not from trimming per-operation counts.

## 7. Limitations

Analytic birthday bound only. No heuristic, no experiment, and no certificate (empty manifest).
Not an established attack.
