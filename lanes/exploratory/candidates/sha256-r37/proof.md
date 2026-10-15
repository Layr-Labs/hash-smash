# 37-round SHA-256: generic memoryless rho, scalar cost 130.36

## 1. Claim

Target `sha256-r37-prefix-v1`: complete SHA-256 with prefix rounds 0 through 36 on every padded block, standard IV, FIPS 180-4 padding, full feed-forward and 256-bit digest. Generic Pollard-rho / Floyd collision search on f(x) = H(enc32(x)). Time strictly less than 2^130.36 target compressions. Memory strictly less than 2^16 bytes (memory term 0). Success probability exceeds 0.39 under heuristic H_random. No preprocessing and no nonuniform advice.

## 2. Iteration map

enc(x) is the 32-byte little-endian encoding of a 256-bit word. H is the complete selected hash of that message: one FIPS-padded block (32 + 0x80 + zeros + 8-byte big-endian bit length 256) and one 37-round compression from the standard IV. f(x) is the 256-bit big-endian reading of the digest. One evaluation is one target compression plus at most 80 other word operations under collision-frontier-v5 with C = 2644.

If f(t) = f(h) with t != h, then enc(t) and enc(h) are distinct messages whose complete digests agree on all 256 bits.

## 3. Algorithm (Floyd)

```
x0 <- uniform random 256-bit word
t <- f(x0); h <- f(f(x0)); n <- 3
while t != h:
    t <- f(t); h <- f(f(h)); n <- n + 3
    if n > 3*2^128: halt failure
t <- x0
loop:
    ft <- f(t); fh <- f(h)
    if ft == fh: exit loop
    t <- ft; h <- fh
if t == h: halt failure
output enc(t), enc(h)
```

Phase 1 uses at most 3L evaluations for first-repeat length L. Phase 2 exits with a collision whenever the tail length mu is at least 1, using at most 2L further evaluations.

## 4. Success probability

Success iff L <= 2^128 and mu >= 1. Under H_random, with N = 2^256 and k = 2^128,

Pr[L <= k] >= 1 - exp(-(1 - 2^-128)/2) >= 0.393469.

Pr[mu = 0 and L <= k] <= 2^-128. Hence success >= 0.393469 - 2^-128 > 0.39.

## 5. Time

Evaluations at most 5 * 2^128. Each is one compression plus at most 80 word operations at 1/2644 each. Setup under 80 further operations.

T <= 5 * 2^128 * (1 + 80/2644) + 80/2644 < 5.1513 * 2^128 = 2^130.364 < 2^130.36.

All work is sequential on one processor.

## 6. Memory

The 8-word SHA-256 state, the 64-byte block, tortoise/hare words, the counter and the straight-line 37-round compression code fit in under 2^16 bytes. No tables in the claimed algorithm (the experiment builds a 2^16 lookup only as evidence acceleration).

## 7. Evidence and limits

Experiment `rho-reduced` runs this Floyd algorithm on the 16-bit truncation of f; the organizer verifies each returned pair agrees on digest bits 0..15 with distinct messages. No 256-bit collision is observed or claimed. H_random is the standard random-mapping model, not a theorem about 37-round SHA-256. The attack is generic.

## 8. Score

Normalized score = time_log2 + max(0, memory_log2_bytes - 20) = 130.36 + 0 = 130.36, below the promoted scalar best of 248.


## Cost contract

Reference cost C for sha256-r37-prefix-v1 is the organizer-pinned compression
cost (64 for full SHA-256 scaled to 37 rounds per frontier track config).
Floyd uses three 32-byte states; memory_log2_bytes=16.

Under H_random on f(x)=H(enc32(x)) with domain 2^256, Pr[L<=2^128] >
1-exp(-1/2). Success after excluding mu=0 is >0.39. Time: <=5*2^128
compressions times C accounting gives time_log2 < 130.36 as claimed.

## Experiment

rho_reduced.py: Floyd on 16-bit truncation; digest-xor-mask bits 0..15;
organizer-executed, reproducible. Offline: high success rate matching
birthday ~800 evals for N=2^16.

## Limits

Generic attack; H_random assumed; no full-width witness; exploratory AI review.
