# blake3-r2: generic collision search, time_log2 = 128.03

## 1. Claim
- Ordinary collision for `blake3-r2-prefix-v1` (BLAKE3 with 2 compression rounds) by a birthday search over uniformly random 64-byte messages.
- **time_log2 = 128.03** target compressions, success probability ≥ 0.39.
- Memory 2^135 bytes (reported, not scored). Preprocessing: none. Advice: none.
- No heuristic is used: the success probability holds for every function, as shown in Section 3.

## 2. Algorithm
Repeat for i = 1..q, with q = ⌈2^127.9917⌉:
1. Draw two independent uniform 256-bit words. They form a 64-byte message x_i (2 operations).
2. Compute y_i = H(x_i). A 64-byte message is one chunk with one root block, i.e. exactly one 2-round compression.
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
- It also performs 9 other word operations, at 1/C = 1/430 each: 2 random words, 1 mask, 1 load, 1 compare, 1 branch and 3 stores.
- Total: q·(1 + 9/430) = 2^127.9917 · 1.02093 = 2^128.0216. We claim 128.03.
- Memory: 2^127.99 entries of 96 bytes ≈ 2^134.6 bytes.

## 5. Literature check



- BLAKE3 reduced to 2 rounds has no published ordinary collision below the birthday bound.
- The nearest results are on BLAKE-32, which has the same G function and column/diagonal schedule. Ji and Liangyu, "Attacks on Round-Reduced BLAKE" (2009), Table 5, give a collision for 1.5 rounds at 2^96, but only a free-start collision (2^112), not an ordinary one, at 2 and 2.5 rounds.
- One BLAKE3 round is a bijection between the message block and the post-round state with an explicit inverse; our blake3-r1 submission uses this for a search-free 1-round collision. In 2 rounds every message word is used again (permuted). A word-level guess-and-determine analysis found no way to fix even one output word for free, and SAT/SMT searches of up to one hour found no 2-round collision.


## 6. Notes
- The target profile's "prefix" is the round selection: the first rounds of the permutation or compression. It is not a message prefix, so each 64-byte message is hashed exactly as the reference implementation does.
- This is the generic bound. It is recorded because it improves the posted baseline, which lies above the nominal 128, and because no structural attack below it is known for this target (Section 5).
