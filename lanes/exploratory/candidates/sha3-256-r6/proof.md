# SHA3-256 prefix rounds 0–5: unconditional 3-pass key-index radix birthday (128.13)

The scalar is `time_log2` under `collision-frontier-v5` (C = 1626); memory is reported only.
Lane: exploratory. Target: `sha3-256-r6-prefix-v1`. Attack: ordinary collision.
Total charged time < 2^128.1240 ≤ 2^128.13. Peak memory < 2^135.58 ≤ 2^136 bytes. Success probability > 0.39.
Heuristics: **none**. This is a generic birthday construction and does not advance cryptanalysis.
`baseline_improved: sha3-256-r6-nominal-v2` is the required identifier only.
This package is self-contained. Every procedure the bound depends on is stated below.

## 1. Target function and messages

`N = 2^256`, `Q = ceil(9943·2^128/10000) = 338342757429489101165234520331412045824 < 2^128`.
A message is 64 bytes, viewed as two 256-bit words (u, v) whose 64-bit little-endian lanes fill
A[0..7]. So `|D| = 2^512`.
H(u, v): state A[0..24] = 0. XOR the eight message lanes into A[0..7]. A[8] ^= 0x06, A[16] ^= 0x8000000000000000
(SHA3 suffix 0x06 and pad10*1 inside the 1088-bit rate; one block, all-zero IV, capacity 512). Apply Keccak-f[1600]
rounds 0..5 (standard θ ρ π χ ι, RC[0..5]). Output d = A[0] | A[1]<<64 | A[2]<<128 | A[3]<<192, the full 256 bits.
Cost: one permutation call = 1 unit. Wrapper (zeroing, loads, pad, packing) ≤ 56 ordinary ops.

## 2. Algorithm (exact)

Digits of d: digit0 = bits 0..85, digit1 = bits 86..170, digit2 = bits 171..255 (widths 86/85/85, sizes
B0 = 2^86, B1 = B2 = 2^85). Arrays: Msg[0..Q-1] of (u, v); Src, Dst[0..Q-1] of pairs (d, i);
Cnt0[0..B0-1], Cnt1[0..B1-1], Cnt2[0..B2-1], one word each.

```
INIT:     Cnt0, Cnt1, Cnt2 <- 0
GENERATE: for i in 0..Q-1:
              u <- rand256(); v <- rand256(); d <- H(u,v)
              Msg[i] <- (u,v); Src[i] <- (d,i)
              for p in 0..2 (unrolled): Cnt_p[digit_p(d)] += 1          # fused histograms
PREFIX:   for p in 0..2: s <- 0; for j: t <- Cnt_p[j]; Cnt_p[j] <- s; s <- s+t   # exclusive prefix sums
for pass p in 0..2:                                                  # LSD order
    for i in 0..Q-1: (d,x) <- Src[i]; k <- digit_p(d); Dst[Cnt_p[k]] <- (d,x); Cnt_p[k] += 1
    swap(Src, Dst)
SCAN: for i in 0..Q-2:
    if Src[i].d == Src[i+1].d:
        a <- Src[i].x; b <- Src[i+1].x
        if Msg[a] != Msg[b]: recompute H(Msg[a]), H(Msg[b]); if equal output (Msg[a], Msg[b]); halt
output FAIL
```

The histogram for every pass depends only on the multiset of digests, which is fixed after GENERATE. So
computing all three histograms during generation gives exactly the counts a separate per-pass
histogram would give. A stable scatter does not change that multiset.

Correctness: each pass is a stable counting sort on one digit. By the standard LSD invariant, after pass p
the pairs are sorted by the low (86 + 85p) bits of d. After pass 2 they are sorted by all 256 bits. Every
index 0..Q-1 appears exactly once throughout, since a counting sort permutes. If two generated messages
are distinct but share a digest, all records with that digest form one contiguous run, and some adjacent
pair in the run has distinct messages, so SCAN finds it. Output is recomputed and verified. The algorithm
never outputs a non-collision, and its only failure mode is FAIL.

## 3. Success probability (unconditional, over the algorithm's coins)

Probability space: the 2Q independent uniform 256-bit words drawn by rand256. H is a fixed function, and
no assumption on H is used. Let E be the event that some i<j has H(m_i) = H(m_j), and R the event that some
i<j has m_i = m_j. The m_i are iid uniform on {0,1}^512. The probability that Q iid samples from an output
distribution contain a repeated value is Schur-convex in that distribution. H induces output probabilities
|H^-1(y)|/2^512, which average 2^-256, so the uniform-output case (every preimage size 2^256) is the
minimum. Hence `Pr(E) ≥ 1 - Π_{k<Q}(1 - k/N) ≥ 1-exp(-Q(Q-1)/(2N))`, where Q(Q-1)/(2N) = 0.494316245 > -ln(0.61),
so Pr(E) > 0.390012. Pr(R) ≤ Q^2/2^513 < 2^-256. SCAN succeeds on E \ R, so success > 0.39.

## 4. Cost ledger (ordinary ops; itemized → charged with visible spare)

| Hot path | itemized | charged | spare |
|---|---:|---:|---:|
| Generate / record: 2 rand + 56 wrapper + 4 stores (Msg 2, Src 2) + 3 loop/index + 3×6 fused histogram (shift, mask, addr, load, add, store) | 83 | **86** | +3 |
| Scatter / record / pass: 2 loads, shift, mask, addr, load Cnt, addr Dst, 2 stores, inc, store Cnt, 3 loop | 14 | **17** | +3 |
| Scan / adjacent pair (worst path): load d, compare, branch, reg move, 2 idx loads, 4 Msg loads, 2 compares, combine, branch, 3 loop | 17 | **19** | +2 |

Cold paths, fully charged:
- INIT + PREFIX: 3 tables ≤ 2^86 entries, ≤ 8 ops/entry (zero store + loop, then load/store/add + loop), < 2^91. Charged **2^92**.
- Fixed setup 2^30; verification 2 permutations + 2^14 ops.

    Wcoef = 86 + 3·17 + 19 = 156
    W ≤ 156·Q + 2^92 + 2^30 + 2^14
    T ≤ Q + 2 + W/1626
    log2 T ≈ 128.123923 < 128.13

Without any spare (Wcoef 148) the bound would be about 128.1175. The claim keeps 8 ops/record of
visible spare on hot paths and leaves ≈ 0.006 bits of rounding margin.

## 5. Memory

Msg: 64Q bytes. Src + Dst: 2·64Q bytes. Cnt tables: (2^86 + 2^85 + 2^85) = 2^87 words · 32 bytes = 2^92. Code/state 2^24.
Total ≈ 192Q + 2^92 ≈ 2^135.577 < 2^136. Every index (< 2^128), count (≤ Q) and address (< 2^136) fits in a
256-bit word.

## 6. Why the structure is legitimate

(a) Moving (digest, index) pairs instead of full (digest, u, v) records is standard key-index sorting.
The messages are written once, read only on the rare equal-digest path, and every access is charged.
(b) Histogram fusion is exact, since the counts depend only on the digest multiset (§2). (c) Three passes
of 85/86-bit digits keep the count-table work at 2^92 ops, about 2^-46 of the main term. Two passes would
need 2^128-entry tables costing ≈ 0.014 bits, which is why it was not chosen. Extracting a digit is one
shift plus one mask on the 256-bit word RAM, whatever the width. Every cost is H-independent: no hash
table, chain, or probe sequence whose length could depend on H.

## 7. Limitations

Analytic birthday bound only. No heuristic, no experiment, and no certificate (empty manifest).
Not an established attack.
