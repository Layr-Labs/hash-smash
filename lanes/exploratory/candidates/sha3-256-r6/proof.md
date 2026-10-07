# sha3-256-r6: generic birthday search with an exact, fixed-work radix-sort ledger (time_log2 = 128.17)

## Claim

| field | value |
|---|---|
| target | `sha3-256-r6-prefix-v1` (SHA3-256 with 6 prefix rounds), ordinary collision of the complete 256-bit digest |
| time_log2 | **128.17** (computed bound 128.1224; the claim also covers 50 uncounted operations per trial: 128.1626) |
| success_probability | 0.39 (proved lower bound 0.39347, no heuristic) |
| memory_log2_bytes | 136 (computed 135.585) |
| preprocessing_log2 | 0 |
| nonuniform_advice_log2_bytes | 0 |
| heuristics | none |

No cryptanalytic weakness of SHA3-256 with 6 prefix rounds is used. This is the textbook birthday attack. What this package adds is a complete ledger: every operation of a fixed-work program is charged, and the success probability is proved for this specific function.

## Cost model

`collision-frontier-v5`: one 6-round Keccak-f[1600] permutation call costs one unit; every other primitive 256-bit word-RAM operation costs 1/C with C = 1626 (`reference_operation_costs.sha3-256-r6`). Primitive operations are load, store, add/sub mod 2^256, AND/OR/XOR/NOT, shift/rotate, compare, conditional branch, and one independent uniform random 256-bit word. Work is summed over all processors.

## Message domain and one evaluation

Every message is a 64-byte string M = A || B with A, B uniform 256-bit words, so both members of the output pair are honest byte strings in the domain.

The 64-byte message M = A || B (A, B are 256-bit words) is one SHA3-256 block (64 < 136 bytes). The sponge state (1600 bits, held in 7 words) is set to zero, A and B are written into its first two words, the padding bytes 0x06 (byte 64) and 0x80 (byte 135) are XORed in, the 6-round permutation is applied once, and the digest is the first 256-bit word of the state.

## The algorithm (fixed work on every tape)

Parameters: q = 2^128 trials, N = 2^256 digests. Arrays R and S each hold q records (K, A, B) of three 256-bit words. CNT is an array of 2^64 counters.

1. **Generate.** For i = 0..q−1: draw A_i, B_i; compute K_i = H(A_i || B_i); store (K_i, A_i, B_i) at R[i].
2. **Sort.** LSD radix sort of R by the 256-bit key K, in 4 passes on the 64-bit digits of K (least significant first). Each pass:
   - (a) zero CNT;
   - (b) count: for each record, extract the digit with one shift and one AND, and increment CNT[digit];
   - (c) exclusive prefix sum over CNT;
   - (d) scatter each record to S at position CNT[digit]++;
   - (e) swap R and S.
   LSD radix sort with a stable scatter is correct for any key multiset; its work does not depend on the data.
3. **Scan.** For i = 1..q−1: if K_i = K_{i−1} and (A_i, B_i) ≠ (A_{i−1}, B_{i−1}), output the two messages and stop; otherwise continue. If the scan ends without output, report failure.

The program has no data-dependent loop bound. The only data-dependent branch, the equal-key test, costs a bounded number of extra operations per record, and that worst case is charged.

## Ledger

Per trial in step 1:

| operation | ops |
|---|---:|
| two independent uniform random 256-bit words A, B | 2 |
| zero the 7 state words | 7 |
| write A and B into the state | 2 |
| load the two padding constants and XOR them in | 4 |
| load the 256-bit digest word | 1 |
| store the record (K, A, B) and advance the write address | 4 |
| loop control (increment, compare, branch) | 3 |
| **step 1 total** | **23** |

Per record per sort pass:
- counting: load K, shift, AND, address add, load counter, increment, store counter, loop control 3, giving 10;
- scatter: load K, A, B (3), extract digit (2), address add, load/increment/store counter (3), destination address (2), store K, A, B (3), loop control (3), giving 17.

Over 4 passes that is 4 × 27 = **108**.

Per record in step 3 (worst case, equal key): load key, compare, branch, load the four message words, two compares, branch, loop control 3, giving **13**.

Total per trial: 23 + 108 + 13 = **144** word operations.

Fixed per-pass work: zeroing the counters (store plus loop control, 4 per counter) and the prefix sum (load, add, store plus loop control, 6 per counter) over 2^64 counters, 10 × 2^64 per pass, 40 × 2^64 = 2^69.32 in all; plus at most 64 operations of set-up.

Total charged time:

    T = q · 1 + (q · 144 + 40 · 2^64 + 64) / 1626
      = 2^128 · (1 + 144/1626) + 2^58.65
      = 2^128.1224.

The claim 128.17 also bounds 2^128 · (1 + 194/1626) = 2^128.1626. That leaves room for 50 further operations per trial, if a reviewer counts any line above more strictly.

## Success probability (proved, for this fixed function)

Let H be the fixed target. The digests K_i = H(M_i) are i.i.d. with some distribution p on the N values, because the M_i are i.i.d. uniform.
- The probability that q i.i.d. draws from p are pairwise distinct is a Schur-concave symmetric function of p. It is therefore maximised by the uniform distribution (Munford 1977, "A note on the uniformity assumption in the birthday problem").
- For uniform p it equals ∏_(i<q)(1 − i/N) ≤ exp(−q(q−1)/(2N)).
- With q = 2^128 and N = 2^256, q(q−1)/(2N) = 1/2 − 2^−129.

So Pr[some K_i = K_j, i ≠ j] ≥ 1 − exp(−1/2 + 2^−129) ≥ 0.393469.

An equal key with equal messages is not a collision. Equal messages require (A_i, B_i) = (A_j, B_j) for some i ≠ j, which has probability at most q²/2^513 = 2^−257.

After sorting, any two equal keys with distinct messages lie in a run of equal keys. That run contains an adjacent pair with distinct messages unless all its messages are equal. So the scan outputs a valid collision whenever one exists among the trials.

Therefore Pr[success] ≥ 0.393469 − 2^−257 > 0.3934 ≥ 0.39. No assumption about H is used.

## Memory

R and S hold 2 · 2^128 · 3 · 32 bytes; CNT holds 2^64 · 32 bytes. The total is 2^135.585 bytes. Memory is reported only; it is not scored.

## Scope and limitations

- The attack is generic and gives no evidence about the cryptanalytic strength of the target.
- The ledger is a conservative, explicit operation count, not a measurement.
- No certificate is supplied, because a collision at this cost is infeasible.

## Prior work

The birthday paradox and radix sort are textbook methods. Other solvers have also submitted generic birthday packages for this track. This ledger and text are our own.
