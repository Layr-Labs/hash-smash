# sha3-256-r6: generic collision search, time_log2 = 128.0

## 1. Claim
- Ordinary collision for `sha3-256-r6-prefix-v1` (SHA3-256 with 6 Keccak-f rounds) by a birthday search over uniformly random 64-byte messages.
- **time_log2 = 128.0** target compressions, success probability ≥ 0.39.
- Memory 2^135 bytes (reported, not scored). Preprocessing: none. Advice: none.
- No heuristic is used: the success probability holds for every function, as shown in Section 3.

## 2. Algorithm
Repeat for i = 1..q, with q = ⌈2^127.9917⌉:
1. Draw two independent uniform 256-bit words. They form a 64-byte message x_i (2 operations).
2. Compute y_i = H(x_i). A 64-byte message is shorter than the 136-byte rate, so hashing it is exactly one 6-round permutation.
3. Look up y_i in a hash table indexed by its low bits: 1 mask, 1 load, 1 compare, 1 branch.
4. Store (y_i, x_i): 3 stores.
5. If an earlier x_j ≠ x_i has y_j = y_i, output (x_j, x_i).

## 3. Success probability (no randomness assumption on H)
- **Inputs.** The x_i are uniform on {0,1}^512. The probability that two inputs coincide is at most q²/2^513 < 2^−256.
- **Outputs.** For any fixed function H, each y_i = H(x_i) is an independent sample from some distribution p on {0,1}^256.
- **Uniform is the worst case.** The probability that q independent samples are pairwise distinct is a Schur-concave function of p, so it is largest when p is uniform. Hence
  Pr[some y_i = y_j] ≥ 1 − ∏_{k<q}(1 − k/2^256) ≥ 1 − exp(−q(q−1)/2^257).
- **Choice of q.** With q = 2^127.9917 the bound equals 0.39. Subtracting the < 2^−256 chance of equal inputs leaves ≥ 0.39 − 2^−256, and one extra step restores it.
- So the stated success probability does not rest on H behaving randomly. A non-uniform H only helps.

## 4. Cost (collision-frontier-v5)
- Each step evaluates H once: one target compression for a 64-byte message.
- It also performs 9 other word operations, at 1/C = 1/1626 each: 2 random words, 1 mask, 1 load, 1 compare, 1 branch and 3 stores.
- Total: q·(1 + 9/1626) = 2^127.9917 · 1.00554 = 2^127.9997. We claim 128.0.
- Memory: 2^127.99 entries of 96 bytes ≈ 2^134.6 bytes.

## 5. Literature check



- No classical collision attack on 6-round SHA3-256 below the birthday bound is published.
- Guo, Liu, Song and Tu (ASIACRYPT 2022) note that the colliding 4-round trails exceed the bound for SHA3-224/256, and give only quantum 6-round attacks for them.
- Tu, Song, Wu, Guo, Weng and Xing (2026) report 6-round SHA3-256 near collisions, 6 digest bits apart, and a practical 6-round SHAKE128 (d=160) collision. A near collision is not a collision.


## 6. Notes
- The target profile's "prefix" is the round selection: the first rounds of the permutation or compression. It is not a message prefix, so each 64-byte message is hashed exactly as the reference implementation does.
- This is the generic bound. It is recorded because it improves the posted baseline, which lies above the nominal 128, and because no structural attack below it is known for this target (Section 5).
