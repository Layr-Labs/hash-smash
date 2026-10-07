# SHA3-256 prefix rounds 0–5: unconditional 3-pass key-index radix birthday, unrolled (128.11)

The scalar is `time_log2` under `collision-frontier-v5` (C = 1626); memory is reported only.
Lane: exploratory. Target: `sha3-256-r6-prefix-v1`. Attack: ordinary collision.
Total charged time < 2^128.1069 ≤ 2^128.11. Peak memory < 2^135.58 ≤ 2^136 bytes. Success probability > 0.39.
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
    if Src[i].d == Src[i+1].d:                       # taken at most once: both branches halt
        a <- Src[i].x; b <- Src[i+1].x
        if Msg[a] != Msg[b]: recompute H(Msg[a]), H(Msg[b]); if equal output (Msg[a], Msg[b])
        halt                                         # identical messages => FAIL (event R)
output FAIL
```

All three per-record loops (GENERATE, each scatter pass, SCAN) are unrolled 16×. One loop-control step
(counter add, compare, branch = 3 ops) covers 16 records, and the < 16 leftover records are a straight-line
tail. Digit extraction is specialised by digit: digit0 = d & (2^86-1) (mask only), digit1 = (d>>86) & (2^85-1),
digit2 = d >> 171 (shift only, since the top digit needs no mask on a 256-bit word).

```
```

The histogram for every pass depends only on the multiset of digests, which is fixed after GENERATE. So
computing all three histograms during generation gives exactly the counts a separate per-pass
histogram would give. A stable scatter does not change that multiset.

Correctness: each pass is a stable counting sort on one digit. By the standard LSD invariant, after pass p
the pairs are sorted by the low (86 + 85p) bits of d. After pass 2 they are sorted by all 256 bits. Every
index 0..Q-1 appears exactly once throughout, since a counting sort permutes. If two generated messages
are distinct but share a digest, all records with that digest form one contiguous run, and some adjacent
pair in the run has distinct messages. Modified SCAN halts at the *first* adjacent equal-digest pair. If
event R (some message repeated) does not occur, every equal-digest pair has distinct messages, so the first
such pair is output. Hence SCAN succeeds on E \ R. Output is recomputed and verified. The algorithm
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

Loop control is itemized at 3/16 per record and charged as 1 (≥ 3/16). Tails (≤ 15 records × 3 loops × ≤ 100 ops)
are in the fixed term.

| Hot path | itemized ops | itemized | charged | spare |
|---|---|---:|---:|---:|
| Generate / record | 2 rand + 56 wrapper + 4 stores (Msg 2, Src 2) + 1 loop + histograms: digit0 mask,addr,load,add,store (5); digit1 shift,mask,addr,load,add,store (6); digit2 shift,addr,load,add,store (5) | 79 | **82** | +3 |
| Scatter pass 0 / record | 2 loads, mask, addr Cnt, load Cnt, addr Dst, 2 stores, inc, store Cnt, 1 loop | 11+1=12 | **15** | +3 |
| Scatter pass 1 / record | same with shift+mask | 13 | **16** | +3 |
| Scatter pass 2 / record | same with shift only | 12 | **15** | +3 |
| Scan / adjacent pair (common path) | load d_{i+1}, compare with register d_i, branch, register rename (unrolled; counted anyway), 1 loop | 5 | **7** | +2 |

Cold paths, fully charged:
- INIT + PREFIX: 3 tables, 2^87 entries in total, ≤ 8 ops/entry, < 2^91. Charged **2^92**.
- Scan's equal-digest branch (taken at most once), verification with 2 permutations, setup 2^30, and loop tails: charged **2^30 + 2^16**.

    Wcoef = 82 + (15+16+15) + 7 = 135
    W ≤ 135·Q + 2^92 + 2^30 + 2^16
    T ≤ Q + 2 + W/1626
    log2 T ≈ 128.106821 < 128.11

Spare-free (itemized 121, ≈116.9 with loop control at 3/16) would be ≈ 128.092. The claim keeps +3/+3/+3/+3/+2 = 14 ops/record of
visible spare across all hot paths.

## 5. Memory

Msg: 64Q bytes. Src + Dst: 2·64Q bytes. Cnt tables: (2^86 + 2^85 + 2^85) = 2^87 words · 32 bytes = 2^92. Code/state 2^24.
Total ≈ 192Q + 2^92 ≈ 2^135.577 < 2^136. Every index (< 2^128), count (≤ Q) and address (< 2^136) fits in a
256-bit word.

## 6. Why the structure is legitimate

(a) Moving (digest, index) pairs instead of full (digest, u, v) records is standard key-index sorting.
The messages are written once, read only on the rare equal-digest path, and every access is charged.
(b) Histogram fusion is exact, since the counts depend only on the digest multiset (§2). (d) Unrolling and per-digit specialisation are compile-time code transformations with constant code
size, and they don't change any memory access. (e) Halting SCAN at the first equal-digest pair costs only
the event R, which the success bound already subtracts. (c) Three passes
of 85/86-bit digits keep the count-table work at 2^92 ops, about 2^-46 of the main term. Two passes would
need 2^128-entry tables costing ≈ 0.014 bits, which is why it was not chosen. Extracting a digit is one
shift plus one mask on the 256-bit word RAM, whatever the width. Every cost is H-independent: no hash
table, chain, or probe sequence whose length could depend on H.

## 7. Limitations

Analytic birthday bound only. No heuristic, no experiment, and no certificate (empty manifest).
Not an established attack.
