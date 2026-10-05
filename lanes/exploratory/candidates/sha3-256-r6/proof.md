# SHA3-256 prefix rounds 0–5: unconditional 32-bit radix birthday (conservative spare)

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
separately reported resource bound and does not affect the score.

Selected lane: exploratory. Target: `sha3-256-r6-prefix-v1`.
This finite classical algorithm has total charged time at most 2^128.26,
peak memory at most 2^136 bytes, and success probability at least 0.39.
The proposed scalar is **128.26**. It is a generic analytic construction
with infeasible resource use, not a claimed cryptanalytic advance over any
established attack. The required `baseline_improved` identifier
`sha3-256-r6-nominal-v2` identifies the organizer's nominal reference only.
That nominal display value 128 is not an established attack, qualified
baseline, or security bound; this package does not claim to improve it.

**Relation to prior local packages.** Itemized zero-spare envelopes at
`time_log2 = 128.24` (tickets `8082380`, `6af5e49`) were **refuted** under
paired OpenAI review (`paired:openai:gpt-5.6-sol`). This package restores
conservative ordinary-operation spare on the same 8-pass 32-bit LSD radix
algorithm (generate 72, per-record per-pass 30, scan 20; still no bulk zero of
record arrays) and claims **128.26**. Empty heuristics. Awaiting-review
ticket `25f61e1` at 128.34 is a separate earlier archive and is not modified
here.

## 1. Exact complete hash and legal messages

Let
`Q = ceil(9943 * 2^128 / 10000)`
and `N = 2^256`. Numerically
`Q = 338342757429489101165234520331412045824`,
so `2^127.99175 < Q < 2^127.99176`. The input family D is all 64-byte
strings, so `|D| = 2^512`. Every message has legal bit length 512 < 2^64.
Represent a message by two 256-bit words u,v and serialize it as
LE32(u) || LE32(v), where LE32 writes exactly 32 little-endian bytes,
including zero bytes. This is a bijection from pairs of words onto D.

The selected complete hash has a 1600-bit state, rate 1088 bits (136 bytes),
capacity 512, the all-zero initial state, and full 256-bit output.
Each such message's entire padded input is exactly one 136-byte block:

    LE32(u) || LE32(v) || 06 || (00 repeated 70 times) || 80

This is the SHA3 domain suffix 01 and pad10*1, using delimited suffix 0x06.
There is exactly one absorption permutation, no extra squeezing permutation,
and no Davies-Meyer feed-forward.

The complete subroutine H(u,v) is as follows. Store the state as 25 lanes,
each in the low 64 bits of a separate RAM word; upper bits are zero.
The lane index is x+5y for 0 <= x,y < 5, in little-endian lane order.
Set all 25 lanes A to zero, then for j = 0,1,2,3 set

    A[j]   = (u >> (64*j)) AND (2^64-1)
    A[j+4] = (v >> (64*j)) AND (2^64-1).

Set A[8] = 0x06 and A[16] = 0x8000000000000000.
Lanes 17 through 24 remain the zero capacity portion.

Apply exactly the first six Keccak-f[1600] rounds, indices 0 through 5:

    C[x] = A[x,0] XOR A[x,1] XOR A[x,2] XOR A[x,3] XOR A[x,4]
    D[x] = C[x-1] XOR rot64(C[x+1],1)
    T[x,y] = A[x,y] XOR D[x]
    B[y,2*x+3*y] = rot64(T[x,y],rho[x,y])
    Anew[x,y] = B[x,y] XOR ((NOT64 B[x+1,y]) AND B[x+2,y])
    A = Anew
    A[0,0] = A[0,0] XOR RC[round]

The rho offsets, listed in x+5y order, are

    0, 1,62,28,27, 36,44, 6,55,20, 3,10,43,25,39,
    41,45,15,21, 8, 18, 2,61,56,14.

Use these six RC constants in this order:

    0x0000000000000001, 0x0000000000008082,
    0x800000000000808A, 0x8000000080008000,
    0x000000000000808B, 0x0000000080000001.

Return

    d = A[0] OR (A[1] << 64) OR (A[2] << 128) OR (A[3] << 192).

LE32(d) is exactly the first 32 squeeze bytes, hence the full target digest.
The six-round transformation costs one selected-target sponge permutation
under collision-frontier-v5; surrounding construction operations are charged
separately as ordinary word operations at 1/1626 each.

## 2. Algorithm, data structures and stopping rule

Use two arrays Src and Dst of Q records each. Each record is exactly three
RAM words (digest, u, v), or 96 bytes. No previous collision or
input-specific advice is supplied.

Also allocate count and prefix arrays Cnt[0 .. 2^32 - 1] and
Pos[0 .. 2^32 - 1], each of `2^32` words.

**Generate.** Initialize fixed code/constants/workspace. Do not bulk-zero the
Q-record arrays: every Src[i] is fully written below, and the first scatter
pass writes every Dst slot exactly once (Cnt sums to Q). For i = 0,...,Q-1
draw fresh independent uniform 256-bit words u_i, v_i, compute
d_i = H(u_i,v_i), and store (d_i, u_i, v_i) in Src[i]. Charge all 2Q random
draws and all hashes, including unsuccessful samples.

**LSD 32-bit radix sort.** Digests are unsigned 256-bit words. For pass
k = 0,1,...,7, sort Src stably by the 32-bit digit

    digit(d,k) = (d >> (32*k)) AND (2^32 - 1)

using counting sort into Dst, then swap Src/Dst base pointers:

1. Zero Cnt[0 .. 2^32 - 1] (2^32 stores).
2. For i = 0..Q-1: let g = digit(Src[i].digest, k); Cnt[g] = Cnt[g] + 1.
3. Pos[0] = 0; for g = 0..2^32 - 2: Pos[g+1] = Pos[g] + Cnt[g].
4. For i = 0..Q-1: let g = digit(Src[i].digest, k); let j = Pos[g];
   copy all three words of Src[i] into Dst[j]; Pos[g] = j + 1.
5. Swap the Src/Dst base pointers.

After 8 passes the final Src is sorted by full unsigned digest.
Equal-digest classes are contiguous. Eight passes cover all 256 bits.

**Scan.** Scan adjacent records of the final Src. When two digest words
agree, compare both message words. If the messages are identical, continue.
If they differ, recompute H for both from fresh all-zero states, check full
digest equality, and output the two 64-byte messages.
On verification failure output failure. If the scan ends without a witness,
output failure. One complete batch; no restart.

The algorithm succeeds exactly when the sample contains distinct messages
with equal target digests.

## 3. Unconditional success for this fixed function

The only randomness is the 2Q independent uniform RAM words. For each digest
value y let p_y = |{m in D : H(m)=y}| / 2^512. Independent uniform messages
yield i.i.d. outputs with law p.

For q <= N let e_q(p) be the sum of products of probabilities over
q-element subsets. The probability that q sampled outputs are pairwise
distinct is q! e_q(p). Averaging any two coordinates at fixed sum cannot
decrease e_q. Among maximizers of e_q, one minimizing sum p_i^2 must be
uniform. Hence uniform digests maximize Pr(all distinct), and

    Pr(not E) <= product_(j=0)^(Q-1) (1-j/N) <= exp(-Q*(Q-1)/(2*N)),

where E is the event of some digest collision.

Direct evaluation with the stated Q gives

    Q*(Q-1)/(2*N) = 0.494316245 > -ln(0.61) = 0.4942963218,

so Pr(E) >= 1 - exp(-0.494316245) > 0.390012 > 0.39.

Repeated messages: Pr(R) <= binomial(Q,2)/2^512 < 2^{-256}. Hence

    Pr(success) >= Pr(E) - Pr(R) > 0.390012 - 2^{-256} > 0.39.

The JSON reports the weaker lower bound 0.39. No random-oracle or differential
heuristic is used. Heuristics are empty.

## 4. 256-bit RAM implementation and complete charged time

Ordinary word operations cost 1/1626 each (C = 1626). Permutation calls cost
1; internal round ops are not double-counted.

### 4.1 Conservative envelopes (spare restored)

**H wrapper (excluding the permutation unit):** 25 zero stores, eight lane
extractions, two padding stores, dispatch, four output loads, three
shifts/ORs, bookkeeping: **56** ordinary primitives.

**Generate one record:** 2 random draws + 56 wrapper + 3 record stores +
loop control with spare: at most **72** ordinary primitives, plus one
permutation. (The refuted 128.24 package used 64; spare is restored here.)

**One radix pass, histogram, per record:** digit extract (2), Cnt
load/add/store (3), loop (3) = 8.
**One radix pass, scatter, per record:** digit extract (2), Pos load (1),
3-word load (3), 3-word store (3), Pos+=1 (2), address arithmetic (6),
loop (3) = 20.
Itemized subtotal 28; **plus spare 2 → 30** ordinary primitives per record
per pass. (The refuted package used 28 with no spare.)

**Per-pass O(1) on 2^32 tables:** zero Cnt (2^32) + prefix (<= 3·2^32) +
swap (4) <= 4·2^32. Over 8 passes: **2^37**.

**Adjacent scan per pair:** at most **20** ordinary primitives (restored
from 16). Bound by 20Q.

**No bulk zero of Src/Dst** (Section 2).
**Fixed code load:** at most 2^30.

### 4.2 Totals

| Phase | Perms | Ordinary ops |
| --- | ---: | ---: |
| Fixed code/constants load | 0 | 2^30 |
| Generate/hash/store | Q | 72 Q |
| 8 radix passes × 30/record | 0 | 240 Q |
| 8× table O(1) on 2^32 | 0 | 2^37 |
| Adjacent scan | 0 | 20 Q |
| Verify/emit | ≤2 | 2^14 |

    W <= (72 + 240 + 20) Q + 2^30 + 2^37 + 2^14
       = 332 Q + 138512711680.

    H_calls <= Q + 2
    T <= Q + 2 + 332 Q / 1626 + 138512711680/1626
       = Q (1 + 332/1626) + 2 + 85186169.54...
       = Q (1958/1626) + 85186171.54...
       = Q (979/813) + 85186171.54...

Now 979/813 < 1.20419, and with Q < 2^127.99176:

    T < 1.20419 * Q + 85186172
      < 1.20419 * 2^127.99176 + 2^27
      < 2^128.2599.

Exact integer check with the stated Q:

    T <= Q + 2 + 332*Q/1626 + 138512711680/1626
       < 1.204182 * Q + 85186172
       < 2^128.25981.

The claimed scalar **128.26** is a strict upward rounding
(`2^128.25981 < 2^128.26`).

Preprocessing is only the fixed-code load:

    P <= 2^30 / 1626 < 2^20 < 2^30.

Retained `preprocessing_log2: 30` is a loose upper bound already inside T.

## 5. Memory, data and interpretation of the claim

    M <= 192 Q + 2^38 + 2^24 < 2^136 bytes.

JSON meanings:

* `time_log2: 128.26` — T <= 2^{128.26} target-compression units.
* `memory_log2_bytes: 136` — M <= 2^{136} peak bytes.
* `data_log2: 128` — at most Q+2 < 2^{128} hash evaluations.
* `preprocessing_log2: 30` — P < 2^{30}, already in T.
* `success_probability: 0.39` — proved one-batch lower bound.
* `nonuniform_advice_log2_bytes: 0` — advice upper bound 2^0 (actual 0).

No improvement over an established attack is claimed.

## 6. Evidence, heuristic disclosures and limitations

All evidence is the analytic argument above. Heuristics are empty. No
experiment or certificate is claimed. This is an analytic upper bound, not
a measured practical attack. The zero-spare 128.24 accounting was rejected on
paired review; this package intentionally retains spare in generate, radix,
and scan envelopes rather than re-arguing the itemized minimum.

## 7. Provenance

Restores conservative spare relative to the refuted 128.24 itemized package,
on the same 8-pass 32-bit radix / Q / Schur birthday line as earlier local
work (including cancelled `e3e14fe` at 128.26). Fresh review required; no
inherited qualification asserted. Does not cancel or alter awaiting-review
`25f61e1` at 128.34.
