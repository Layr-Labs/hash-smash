# SHA-256 r31 exploratory: generic one-block birthday with validated sparse dictionary

Declared scalar under `collision-frontier-v5`: `time_log2 = 128.060215`, with
`memory_log2_bytes = 198`, `preprocessing_log2 = 8.936605`, and
`success_probability = 0.39`. This exploratory package for
`sha256-r31-exploratory` / `sha256-r31-prefix-v1` is a complete analytic RAM
algorithm, not a computed collision. `ready` requests review; it does not assert
an AI outcome or human acceptance.

The construction is unconditional and distribution-free for this fixed hash.
No ideal-hash, random-oracle, differential, round-independence, or
experimental-extrapolation premise is used. The required `baseline_improved`
value `sha256-r31-nominal-v2` is organizer display metadata only; this package
does not claim improvement over that reference as an established attack.

Relative to the organizer birthday baseline (`time_log2 = 136`, merge-sorted
64-byte two-block samples), two accounting changes remove the dominant overhead:

1. **One padded block per sample.** Exactly 36-byte messages pad under FIPS
   180-4 to a single 64-byte block, so each sample costs one selected-round
   compression rather than two.
2. **Exact linear-work duplicate detection.** A two-level Briggs–Torczon
   validated sparse direct-address dictionary replaces comparison sorting,
   eliminating the `log2(n)` merge-pass factor. Memory is reported under v5 and
   does not affect the scalar.

A prior envelope that charged only 88 ordinary operations per sample was
refuted. This package adopts a carefully itemized **104 ordinary ops/sample**
ledger (58 generation + 38 table + 8 control), matching the accounting that
already passed AI screening on the public peer package `3458d67` (commit
`f14d875`).

## 1. Exact message and complete-hash definition

Write BE_k(v) for the k-byte big-endian encoding of integer v. Set

    n = ceil(9943 * 2^128 / 10000)
      = 338342757429489114221633372169407132651,

D = 2^288, and Q = 2^256. For independent uniform 256-bit words u,t set
w = t AND (2^32 - 1) and form the 36-byte message

    m(u,w) = BE_32(u) || BE_4(w).

This injectively identifies D = 2^288 messages of exactly 36 bytes. Their bit
length L = 288 satisfies L < 2^64 and L <= 447, so FIPS 180-4 padding yields
exactly one 512-bit block:

    BE32(u) || BE4(w) || 0x80 || (19 zero bytes) || BE_8(288).

Decode this single block as sixteen big-endian 32-bit words W[0..15] held in
separate RAM words:

    W[j] = (u >> (32 * (7 - j))) AND (2^32 - 1),  j = 0..7;
    W[8] = w;
    W[9] = 0x80000000;
    W[10..14] = 0;
    W[15] = 288.

Initialize the working state once with the standard IV:

    a = 0x6a09e667, b = 0xbb67ae85, c = 0x3c6ef372, d = 0xa54ff53a,
    e = 0x510e527f, f = 0x9b05688c, g = 0x1f83d9ab, h = 0x5be0cd19.

All additions below are modulo 2^32; NOT and rotations operate on 32 bits.
Define

    s0(z) = ROTR32(z,7) XOR ROTR32(z,18) XOR (z >> 3)
    s1(z) = ROTR32(z,17) XOR ROTR32(z,19) XOR (z >> 10)
    S0(z) = ROTR32(z,2) XOR ROTR32(z,13) XOR ROTR32(z,22)
    S1(z) = ROTR32(z,6) XOR ROTR32(z,11) XOR ROTR32(z,25)
    Ch(e,f,g) = (e AND f) XOR ((NOT e) AND g)
    Maj(a,b,c) = (a AND b) XOR (a AND c) XOR (b AND c)
    W[t] = W[t-16] + s0(W[t-15]) + W[t-7] + s1(W[t-2]),
        for t = 16,...,30.

The constants K[0],...,K[30] are, in hexadecimal and original index order,

    428a2f98 71374491 b5c0fbcf e9b5dba5 3956c25b 59f111f1 923f82a4 ab1c5ed5
    d807aa98 12835b01 243185be 550c7dc3 72be5d74 80deb1fe 9bdc06a7 c19bf174
    e49b69c1 efbe4786 0fc19dc6 240ca1cc 2de92c6f 4a7484aa 5cb0a9dc 76f988da
    983e5152 a831c66d b00327c8 bf597fc7 c6e00bf3 d5a79147 06ca6351

Copy the incoming chaining words into (a,b,c,d,e,f,g,h), then execute exactly
t = 0,...,30 with simultaneous updates:

    T1 = h + S1(e) + Ch(e,f,g) + K[t] + W[t]
    T2 = S0(a) + Maj(a,b,c)
    (a,b,c,d,e,f,g,h) = (T1+T2, a, b, c, d+T1, e, f, g).

After round 30 apply Davies–Meyer feed-forward: add all eight working words to
the corresponding IV words. The complete digest is the 256-bit integer

    d = (a'<<224)|(b'<<192)|(c'<<160)|(d'<<128)|(e'<<96)|(f'<<64)|(g'<<32)|h'

in standard big-endian word order. Equality of d is equality of the full digest.

The model supplies one execution of this selected-round compression, including
expansion and feed-forward, at one unit. Message handling and state/byte
serialization are charged separately below as ordinary word operations.

Outside that compression primitive, generation uses **58 ordinary word
operations**: two fresh random words (2); u extraction (8 ANDs, 7 shifts and
8 stores = 23); w extraction and store (2); seven zero/constant padding stores
(7); two call/return transfers (2); digest packing (8 loads, 7 shifts and
7 ORs = 22). Total: 2+23+2+7+2+22 = 58.

## 2. Concrete RAM algorithm and stopping rule

Every RAM word is 256 bits (32 bytes). Draw precisely 2n fresh words through the
model's independent uniform random-word primitive, two per message. There is no
finite seed, deterministic PRNG expansion, or precomputed advice. The high 224
bits of the second word are discarded, not reused as uncharged coins.

### 2.1 Two-level validated sparse direct-address dictionary

Split a digest d into a 192-bit prefix h = floor(d / 2^64) and a 64-bit suffix
l = d mod 2^64. Reserve:

- T1[0..2^192-1]: top-level sparse map from prefix to block index;
- block arena B of at most n blocks of 2^64 words each;
- back1[0..n-1], back[0..n-1], fwd[0..2n-1];
- counters count1 = count = 0.

Do not initialize T1, B, or the record arrays; their initial contents may be
arbitrary fixed words. All reserved cells are counted in the memory bound.
Briggs–Torczon validation (dense back-pointers) makes every access correct for
arbitrary initial sparse contents, so no clearing pass is required.

For each of at most n samples:

1. Generate (u,w), prepare the complete-hash block, and compute d.
2. Load x = T1[h]. If x < count1 and back1[x] = h, let b = x. Otherwise let
   b = count1, increment count1, set back1[b] = h and T1[h] = b.
3. Load r = B[b*2^64 + l]. If r < count and back[r] = d, load (u',w') from
   fwd[2r], fwd[2r+1]. If u = u' and w = w', continue (repeated input).
   Otherwise recompute both complete hashes, test full digest equality and
   message inequality, output the collision and halt. On a failed check halt
   with failure.
4. Otherwise store r = count in B[b*2^64 + l], store back[count] = d,
   fwd[2count] = u, fwd[2count+1] = w, increment count, and continue.

After n samples, halt with failure. There is one batch, no restart, no
unpriced sorting, no probing chain, and no compressed-digest comparison.
The final check consumes at most two target evaluations, already charged.

For an unseen prefix h, a passing validation x < count1 and back1[x] = h would
mean the dense array already contains h, a contradiction. Therefore its first
access allocates exactly one fresh block. Later accesses to h return that block.
The same argument at level two says that passing r < count and back[r] = d is
possible exactly when d was inserted. Blocks are never reassigned, and different
low digits occupy different cells. Hence every distinct-message digest collision
among the samples is found. Repeated identical messages alone are rejected.
This invariant holds for every initial memory contents and every fixed target
function.

### 2.2 Main loop summary

Initialize fixed program state and counters. Run the n-sample loop above. A
returned pair is always distinct and has identical complete target hashes,
confirmed by recomputation. FAIL has no claimed output relation. There are no
restarts or other amplification.

## 3. Distribution-free birthday lemma

For each of the Q possible digest values y let p_y be the fraction of the D
36-byte messages mapping to y under the fixed deterministic H. Retain zero
entries. Independent uniform messages induce independent output samples from
this same p, because H is applied separately to independent inputs. This says
nothing about whether p is uniform or SHA-256 behaves like a random function.

For a probability vector p let e_n(p) be the elementary symmetric sum of degree
n. The probability that n samples all differ is n! e_n(p). Among maximizers of
e_n on the simplex, choose one minimizing sum_y p_y^2. If two coordinates a,b
differ, averaging them preserves a+b, increases ab, and cannot decrease e_n,
but strictly decreases the sum of squares — a contradiction. Therefore the
maximizer is uniform (including distributions with zero coordinates), and for
every p,

    Pr(all digests distinct) <= n! binomial(Q,n)/Q^n
      = product_(j=0)^(n-1) (1 - j/Q)
      <= exp(-n(n-1)/(2Q)).

No independence-of-collision-events assumption or structural property of H is
used.

## 4. Algorithmic success and repeated inputs

Let C mean that some sampled digest repeats and R that some original message
repeats. The event C minus R guarantees two distinct messages with equal full
digests, which the algorithm finds. Without assuming independence of C and R,

    Pr(success) >= Pr(C) - Pr(R)
      >= 1 - exp(-n(n-1)/(2Q)) - n(n-1)/(2D).

For our n, n(n-1)/(2Q) > 0.494316244 > 0.4943. The exact rational degree-six
alternating-series upper bound on exp(-0.4943) with x = 4943/10000 is

    1 - x + x^2/2 - x^3/6 + x^4/24 - x^5/120 + x^6/720 < 0.6099992.

It follows that an output pair occurs with probability greater than 0.3900008.
A repeated input pair has total probability at most binomial(n,2)/2^288 < 2^-33.
Subtracting this event is safe even though some repetitions also contain useful
collisions. Hence

    Pr(success) > 0.3900008 - 2^-33 > 0.39.

`success_probability: 0.39` is a lower bound on algorithmic success under its
fresh coins, not equality with actual success, confidence in this proof, or
confidence in an AI review. The entire n-sample construction is paid on failed
runs too. There are no restarts beyond the single fully charged execution.

## 5. Auditable resource implementation

These are worst-case bounds for every random tape in the specified classical
256-bit word RAM. Each selected compression costs one unit. Every other word
load, store, arithmetic/Boolean operation, shift, comparison, branch, and random
word costs 1/2140 target-compression units. Ordinary-operation counts below are
unpriced counts W; compression calls are counted separately as H.

### 5.1 Per-sample instruction budget (104 ordinary ops)

A core scalar operation is charged at the model's word-operation weight.
Address arithmetic is counted. The generation ledger (section 1) uses 58
ordinary operations.

The longest insert-path table count is 37 operations:

| Table work | Word operations |
| --- | ---: |
| Split full d into h,l | 2 |
| T1 address, load, range comparison and branch | 4 |
| back1 address, load, equality comparison and branch | 4 |
| Allocate: copy b, increment count1, back1 address/store, T1 store | 5 |
| Block address: shift and two adds, load, range comparison and branch | 6 |
| back address, load, equality comparison and branch | 4 |
| Insert: block store; back address/store; fwd shift/add/store, add/store; count increment | 9 |
| Sample-loop increment, comparison and branch | 3 |
| Total | 37 |

On a known prefix, allocation's five operations are replaced by one copy.
For an already present digest, record recovery uses one shift, one base add,
two loads and one address add (5), two message-word comparisons, one AND and
one branch (4). This replaces the nine insert operations. Even charging one
additional control transfer yields a table cap of **38**. Range checks always
short-circuit before loading an invalid dense index.

The per-sample cap is therefore **104 ordinary operations**: 58 generation
plus 38 table operations, with **8** further operations for base/mask loads
and control transfers. It is a deterministic path bound, including repeated
samples. Compression internals are not included in this 104; they are paid by
the separate one-unit compression charge.

Final verification happens at most once: two hashes through the same wrapper,
full digest/message comparisons and output stores cost less than 2^14 ordinary
operations, plus two compression calls.

### 5.2 Code, setup, peak storage

Reserve at most 2^17 words for uniform code, public constants and fixed
workspace, including the target primitive's implementation. Straight-line
fixed-coordinate primitive code and the displayed wrapper/table loops use
fewer than 2^14 native instructions, each encoded in at most four words;
working states and counters use fewer than 2^12 more words. This fits in the
reserve. Load/clear that reserve with at most eight operations per word,
including address and loop work: **2^20 ordinary operations**. Declared
`preprocessing_log2: 8.936605` is the corresponding bound in
target-compression units:

    P = 2^20 / 2140,  log2(P) = 8.93660491871149 < 8.936605.

The large table and record arrays are reserved but not cleared, exactly as
proved by the sparse validation invariant. Setup is included in total time.

Memory map (public bases are word addresses; all intervals are disjoint):

| Region | Word count | Starting word address |
| --- | ---: | ---: |
| Uniform code/constants/fixed workspace | 2^17 | 0 |
| back1 | n | 2^128 |
| back | n | 2^129 |
| fwd | 2n | 2^130 |
| Block arena | n * 2^64 | 2^192 |
| T1 | 2^192 | 2^194 |

The arena ends below 2^193; T1 ends at 2^194 + 2^192 < 2^195. Even the
corresponding byte addresses are below 2^200, so either byte or word address
capacity remains well below the 256-bit limit. All counters, indices, n and
comparison values fit in one word.

All reserved memory, including uncleared cells, is counted:

    M = 32 * (2^192 + n*2^64 + 4*n + 2^17) < 2^198 bytes.

The inequality follows from n < 0.9943 * 2^128 + 1: the two dominant terms
total less than 1.9943 * 2^192 + 2^64, leaving much more than 4n + 2^17 below
2^193 words. This proves `memory_log2_bytes: 198`. Memory is required and
reviewed but contributes nothing to the scalar under v5.

### 5.3 Total time

| Phase | Compression calls (cost 1) | Ordinary ops (cost 1/2140) |
| --- | ---: | ---: |
| Fixed setup | 0 | 2^20 |
| Process all n samples | n | 104 n |
| Final verification | at most 2 | 2^14 |

Thus

    H = n + 2,
    W = 104 * n + 2^20 + 2^14,
    T = H + W / 2140,
    log2(T) = 128.0602149915648 < 128.060215.

The declared `time_log2: 128.060215` is a tight upper bound on this
reconstructed value. All setup is inside T. Preprocessing is included in T;
verification work is accounted in H and W. Total work is summed across all
processors; no wall-clock normalization, partial free computation, unpriced
advice, external oracle, restart, or reused target-dependent table is involved.
Actual nonuniform advice is zero; its required nonnegative log bound 0
conservatively allows at most one byte.

## 6. Evidence, scope, and limitations

The heuristic list is empty because sections 1–5 derive correctness, probability
and resources from the explicit target and model primitives. Fresh independent
random words are part of the organizer's model. No ideal SHA-256 behavior is
required.

The certificate manifest is valid and empty. There is no experiment manifest or
executable candidate source. This is an astronomically expensive theoretical RAM
construction, not a measured run, practical attack, or new SHA-256 security
result. Any eventual selected-lane AI qualification remains distinct from
mathematical proof or human acceptance.

## 7. Source and accounting revision

This package revises the organizer's SHA-256 r31 birthday baseline by (i) using
36-byte one-block messages and (ii) replacing merge sort with a validated
two-level sparse direct-address dictionary. The distribution-free probability
argument is retained with n calibrated to the required success probability 0.39.

A previous HashSmash submission on this track (`8be32cc`) used the same
algorithm but claimed an 88 ordinary-ops/sample envelope and `time_log2 = 128.05`.
That envelope was refuted by paired review. The present package adopts the
itemized 104-op ledger (58 generation + 38 table + 8 control) that already
passed AI screening on peer submission `3458d67` (commit `f14d875`, claimed
score 128.060215, awaiting human review). The former baseline declaration was
136 at v5; the explicit counts now support 128.060215. This is a new package
requiring fresh ordinary review.
