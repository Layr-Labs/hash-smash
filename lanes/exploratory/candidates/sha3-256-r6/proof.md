# SHA3-256 prefix rounds 0–5: unconditional 32-bit radix-sort birthday (tightened)

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

Relative to the prior local 32-bit radix package at 128.34 (awaiting review
as `25f61e1`), this package keeps the same algorithm and probability proof
and only tightens ordinary-operation envelopes:

- omit redundant initial zeroing of the Q-record arrays (every Src slot is
  fully overwritten during generate; every Dst slot is overwritten on the
  first scatter pass);
- reduce the per-record per-pass radix spare (40 → 30);
- reduce generate and scan envelopes (88 → 72 and 28 → 20).

Same `Q`, same 8-pass 32-bit LSD radix, empty heuristics. No distinguished-
point method and no random-function heuristic.

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
These are precisely the padded rate block XORed into the all-zero state.
Lanes 17 through 24 remain the zero capacity portion.

Apply exactly the first six Keccak-f[1600] rounds, indices 0 through 5.
For each round use the following stages; within a stage assignments are
simultaneous, and each stage reads the preceding one. Subscripts x,y are
modulo 5. All lane arithmetic is on 64 bits, with NOT64 and rot64 restricted
to those bits, not the entire 256-bit RAM word.

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

**Generate.** Initialize fixed code/constants/workspace. Do **not** bulk-zero
the Q-record arrays: every Src[i] is fully written below, and the first
scatter pass writes every Dst slot exactly once (Cnt sums to Q). For
i = 0,...,Q-1 draw fresh independent uniform 256-bit words u_i, v_i,
compute d_i = H(u_i,v_i), and store (d_i, u_i, v_i) in Src[i]. Charge all
2Q random draws and all hashes, including unsuccessful samples.

**LSD 32-bit radix sort.** Digests are unsigned 256-bit words. For pass
k = 0,1,...,7, sort Src stably by the 32-bit digit

    digit(d,k) = (d >> (32*k)) AND (2^32 - 1)

using counting sort into Dst, then swap the roles of Src and Dst (pointer
swap of the two array bases; no element copy). Explicitly:

1. Zero Cnt[0 .. 2^32 - 1] (2^32 stores).
2. For i = 0..Q-1: let g = digit(Src[i].digest, k); Cnt[g] = Cnt[g] + 1.
3. Pos[0] = 0; for g = 0..2^32 - 2: Pos[g+1] = Pos[g] + Cnt[g]
   (exclusive prefix sum over 2^32 entries).
4. For i = 0..Q-1: let g = digit(Src[i].digest, k); let j = Pos[g];
   copy all three words of Src[i] into Dst[j]; Pos[g] = j + 1.
5. Swap the Src/Dst base pointers.

After 8 passes the final Src is sorted by full unsigned digest.
Every pass is a complete stable counting sort, so equal-digest classes
become contiguous. Eight passes cover all 256 digest bits (8 * 32 = 256).

**Scan.** Scan adjacent records of the final Src. When two digest words
agree, compare both message words. If the messages are identical, continue.
If they differ, recompute H for both from fresh all-zero states, check full
digest equality, and output the two 64-byte messages.
On verification failure output failure; this branch is unreachable under
exact RAM semantics. If the scan ends without a witness, output failure.
There is one complete batch and no restart or amplification.

Sorting preserves every record and makes each equal-digest class contiguous.
If a class contains distinct messages, some adjacent messages differ:
otherwise transitivity of equality would make the whole class one message.
Thus the algorithm succeeds exactly when its sample contains distinct
messages with equal target digests.

## 3. Unconditional success for this fixed function

The only randomness is the 2Q independent uniform RAM words. H remains the
fixed function in Section 1. For each of its N possible digest values y let

    p_y = |{m in D : H(m)=y}| / 2^512.

Some p_y may be zero, and no balance assumption is made. Independent uniform
messages produce independent outputs with this common distribution p.

Here is the full finite-distribution bound. For q <= N let e_q(p) denote the
sum of products of probabilities over all q-element subsets of coordinates.
The probability of all q sampled outputs being distinct is q! e_q(p).
Hold all coordinates except a,b fixed, and keep a+b fixed. Then

    e_q(p) = a*b*e_(q-2)(rest) + (a+b)*e_(q-1)(rest) + e_q(rest),

where e_0=1 and impossible-size coefficients are zero.
All coefficients are nonnegative, so replacing a,b by their mean cannot
decrease e_q. Among maximizers of e_q on the compact simplex, choose one
minimizing sum p_i^2. If two coordinates differ, averaging them does not
decrease e_q and strictly decreases the sum of squares, a contradiction.
Therefore the uniform vector maximizes e_q.

Let E be the event that some two sampled digests agree. Then

    Pr(not E) <= product_(j=0)^(Q-1) (1-j/N) <= exp(-Q*(Q-1)/(2*N)).

With the stated Q,

    Q*(Q-1)/(2*N) = 0.494316245 > -ln(0.61) = 0.4942963218,

so Pr(E) >= 1 - exp(-0.494316245) > 0.390012 > 0.39.

Let R be the event that any two sampled messages are equal. Then
Pr(R) <= binomial(Q,2)/2^512 < 2^{-256}. Hence

    Pr(success) >= Pr(E) - Pr(R) > 0.390012 - 2^{-256} > 0.39.

The JSON reports 0.39. No random-oracle, balance, or differential heuristic
is used. The heuristic list is empty.

## 4. 256-bit RAM implementation and complete charged time

Instruction budgets are counts of ordinary word operations at 1/1626 each
(C = 1626 for sha3-256-r6). Permutation calls cost 1 each; their internal
round operations are not double-counted in the ordinary budgets.

All actual scalars fit in a word: Q, indices, digits < 2^32, Pos/Cnt entries
(<= Q), and addresses below 2^136. Address record i as base+(i<<1)+i with
offsets 0,1,2. Each record uses three individual loads/stores.

### 4.1 Per-phase ordinary-operation envelopes

**H wrapper (per call, excluding the permutation unit).**
25 zero stores, eight lane extractions from (u,v), two padding stores,
dispatch, four output-lane loads, three shifts/ORs, and call bookkeeping:
at most 56 ordinary primitives. The permutation itself is one target unit.

**Generate one record.** Two random-word draws, one H wrapper (56), three
record stores, loop index update and branch: at most **72** ordinary
primitives (56+2+3+5 with spare), plus one permutation unit.

**One radix pass, per record (histogram).** Extract digit (shift+AND = 2),
load Cnt[g], add 1, store (3), loop control (3): at most 8.
**One radix pass, per record (scatter).** Extract digit (2), load Pos[g] (1),
three-word load (3), three-word store (3), Pos[g]+=1 (2), address arithmetic
(6), loop control (3): at most 20. Combined itemized bound: 28.
Add a spare of 2: **30 ordinary primitives per record per pass**.

**Per-pass O(1) on the 2^32 tables.** Zero Cnt (2^32 stores), exclusive
prefix sum (<= 3 * 2^32), pointer swap (4): at most 4 * 2^32 per pass.
Over 8 passes: at most `8 * 4 * 2^32 = 2^37` operations.

**Adjacent scan per pair.** Two digest loads, compare, branch, optional
message compares, loop control: at most **20** ordinary primitives.
Bound by 20 Q.

**No bulk zero of Src/Dst.** As stated in Section 2, generate and the first
scatter overwrite every record slot, so the previous 6Q zeroing charge is
removed.

**Fixed code load.** At most 2^30 charged operations for a 2^24-byte fixed
code/constants area.

### 4.2 Totals

| Phase | Permutation calls (cost 1) | Ordinary ops (cost 1/1626) |
| --- | ---: | ---: |
| Load fixed code/constants; init fixed workspace | 0 | 2^30 |
| Draw, construct, hash and store every message | Q | 72 Q |
| 8 radix passes, per-record work | 0 | 8 * 30 Q = 240 Q |
| 8 radix passes, O(1) count/prefix/swap on 2^32 tables | 0 | 2^37 |
| Scan all adjacent pairs | 0 | 20 Q |
| Recompute both witness hashes; verify; emit | at most 2 | 2^14 |

Summing:

    W <= (72 + 240 + 20) Q + 2^30 + 2^37 + 2^14
       = 332 Q + 138512711680.

    H_calls <= Q + 2
    T = H_calls + W/1626
      <= Q + 2 + 332 Q / 1626 + 138512711680/1626
       = Q (1 + 332/1626) + 2 + 85186169.54...
       = Q (1958/1626) + 85186171.54...
       = Q (979/813) + 85186171.54...

Now 979/813 < 1.20419, and with Q < 2^127.99176:

    T < 1.20419 * Q + 85186172
      < 1.20419 * 2^127.99176 + 2^27
      < 2^128.2599.

Using the exact integer Q:

    T <= Q + 2 + 332*Q/1626 + 138512711680/1626
       < 1.204182 * Q + 85186172
       < 2^128.25981.

The claimed scalar **128.26** is a strict upward rounding
(`2^128.25981 < 2^128.26`).

Preprocessing is only the fixed-code load (record arrays are not bulk-zeroed),
already in T:

    P <= 2^30 / 1626 < 2^20 < 2^30.

The retained `preprocessing_log2: 30` is a loose independent upper bound.

No earlier search chooses messages, coins, collisions, or advice. These are
worst-case bounds for one run, hence also bound expected time.

## 5. Memory, data and interpretation of the claim

Each array occupies 3Q words = 96Q bytes. Both arrays total 192Q bytes.
Cnt and Pos use `2 * 2^32` words = `2^38` bytes. Fixed area: 2^24 bytes.

    M <= 192 Q + 2^38 + 2^24 < 2^136 bytes.

JSON meanings:

* `time_log2: 128.26` means T <= 2^{128.26} target-compression units.
* `memory_log2_bytes: 136` means M <= 2^{136} peak bytes.
* `data_log2: 128` means at most Q+2 < 2^{128} hash evaluations.
* `preprocessing_log2: 30` means P < 2^{30} setup units, already in T.
* `success_probability: 0.39` is a proved one-batch lower bound.
* `nonuniform_advice_log2_bytes: 0` bounds advice by 2^0 bytes (actual 0).

No improvement over an established attack is claimed. Compared with the
128.34 package, the same 8-pass 32-bit radix algorithm is retained; only
ordinary-operation envelopes were tightened as in Section 4.

## 6. Evidence, heuristic disclosures and limitations

All needed evidence is the analytic argument in Sections 1–5. Heuristics are
empty. No experiment or certificate is claimed. This is an analytic upper
bound, not a measured practical attack.

Literature context (not a numeric premise): no classical ordinary-collision
attack on six-round SHA3-256 below birthday is used here. Awaiting-review
distinguished-point packages near the nominal 128 display value typically
declare a random-function heuristic; this package does not use that method
and does not treat those scores as baselines.

`ready` means complete and available for review. Exploratory qualification
is `plausible_not_refuted`; neither AI outcome is mathematical proof.

## 7. Provenance

This package revises the local unconditional 32-bit radix claim at
time_log2 128.34 (`25f61e1`, awaiting review) in the same editable path.
Hash definition, Q, radix width/pass count, probability proof, and C=1626
pricing are retained. Envelope changes: remove record-array zeroing; per-pass
30 (was 40); generate 72 (was 88); scan 20 (was 28). Fresh ordinary review is
required; no inherited qualification is asserted.
