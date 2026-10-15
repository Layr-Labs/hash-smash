# Six-round SHA3-256: generic memoryless rho collision search, scalar cost 130.38

## 1. Claim

Target `sha3-256-r6-prefix-v1`: complete SHA3-256 sponge (zero IV, rate 136 bytes, suffix 0x06 with pad10*1, rounds 0..5 of Keccak-f[1600] in every permutation call, full 256-bit digest). We claim an ordinary collision algorithm with total time T < 2^130.38 target compressions, memory < 2^16 bytes, no preprocessing or advice, and success probability > 0.39 under one declared heuristic (H_random, the standard random-mapping model). This is the classical Pollard-rho / Floyd memoryless birthday attack. It uses no structure of Keccak. It is submitted because its scalar score 130.38 + max(0, 16 - 20) = 130.38 is far below the current incumbent's 248.67 (time 122.67 plus memory term 146 - 20 = 126).

## 2. Iteration map

For a 256-bit word x let enc(x) be its 32-byte little-endian encoding, a valid message (32 < 136 bytes, so it is absorbed as a single padded block: byte 32 is 0x06, byte 135 is 0x80). Define f(x) = H(enc(x)), interpreting the 32-byte digest as a 256-bit little-endian word. One evaluation of f is one six-round permutation call plus at most 64 other word operations (storing x into the four first rate lanes, XORing two padding constants, zeroing the remaining 21 lanes by stores from a constant zero word, reading the four output lanes, one 256-bit pack, plus the loop's comparison, branch and register moves).

If f(t) = f(h) with t != h, then enc(t) != enc(h) and H(enc(t)) = H(enc(h)) on all 256 bits: an ordinary collision of the complete hash.

## 3. Algorithm (Floyd)

```
x0 <- uniform random 256-bit word
t <- f(x0); h <- f(f(x0)); n <- 3
while t != h:                       # phase 1, cycle detection
    t <- f(t); h <- f(f(h)); n <- n + 3
    if n > 3*2^128: halt failure
t <- x0                             # phase 2, tail location
loop:
    ft <- f(t); fh <- f(h)
    if ft == fh: exit loop
    t <- ft; h <- fh
if t == h: halt failure             # x0 was on the cycle (mu = 0)
output enc(t), enc(h)
```

Write x_i = f^i(x0), mu the tail length, lambda the cycle length, L = mu + lambda the number of distinct values before the first repeat. Phase 1 stops at the first i >= 1 with x_i = x_{2i}, i.e. the least i >= mu that is a multiple of lambda; such i <= mu + lambda = L. Phase 1 therefore uses at most 3L evaluations and does not hit its cap when L <= 2^128. In phase 2 the tortoise runs x_0, x_1, ... and the hare x_i, x_{i+1}, ...; since i is a multiple of lambda, x_j and x_{j+i} first coincide at j = mu. The loop exits at j = mu - 1 with t = x_{mu-1}, h = x_{mu-1+i}, f(t) = f(h) = x_mu. If mu >= 1, t is on the tail and h is on the cycle, so t != h: a valid collision. Phase 2 uses 2 mu <= 2L evaluations.

## 4. Success probability

Success iff L <= 2^128 and mu >= 1. Under H_random (claim.json), with N = 2^256 and k = 2^128:

Pr[L <= k] >= 1 - prod_{i=1}^{k-1}(1 - i/N) >= 1 - exp(-k(k-1)/(2N)) = 1 - exp(-(1 - 2^-128)/2) >= 0.393469.

Given L = l, mu = 0 iff the repeated value x_l equals x_0, probability 1/l; and Pr[L = l] <= l/N, so Pr[mu = 0 and L <= k] <= sum_{l <= k} (l/N)(1/l) = k/N = 2^-128. Hence success >= 0.393469 - 2^-128 > 0.39.

## 5. Time

Evaluations: at most 3k in phase 1 (cap) plus 2 mu <= 2k in phase 2, total <= 5 * 2^128. Each evaluation is one permutation call (1 unit) plus at most 64 word operations at 1/1626 each (reference_operation_cost of sha3-256-r6). Setup (random word, two initial evaluations' bookkeeping, output) is under 64 further operations. Total, counting failures (the bound covers a failing run, which stops at the cap):

T <= 5 * 2^128 * (1 + 64/1626) + 64/1626 < 5.1968 * 2^128 = 2^130.3776 <= 2^130.38.

All work is sequential on one processor; parallelization (van Oorschot-Wiener distinguished points) would not reduce total work and is not used.

## 6. Memory

The 25-lane (200-byte) Keccak state, the 136-byte block buffer, the words x0, t, h, ft, fh (160 bytes), the counter, and straight-line code for the six-round permutation and the loop (well below 32 KiB). Total below 2^16 bytes, so memory_log2_bytes = 16 and the memory term max(0, 16 - 20) is 0.

## 7. Evidence and limits

Experiment `rho-reduced` runs this exact algorithm on the 16-bit truncation of f (complete six-round digests, only bits 0..15 kept for the iteration), and the organizer verifies each returned pair agrees on those 16 bits with distinct messages. A local run gave 40/40 successes with mean 812 evaluations, matching the random-mapping prediction (about 2.5 * sqrt(pi * 2^16 / 2) ~ 800). No 256-bit collision is observed or claimed; the heuristic is the standard random-mapping model, extrapolated from 16 to 256 bits. The result is generic and makes no cryptanalytic claim about six-round Keccak.
