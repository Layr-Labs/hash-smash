# SHA-256, 31 prefix rounds: single-block birthday collision construction

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains a
separately reported resource bound.

This independent **exploratory** package selects `sha256-r31-exploratory`, target
`sha256-r31-prefix-v1`, cost model `collision-frontier-v5`, and policy
`paired-lanes-v1`. It submits a complete analytic algorithm, not an already
computed collision. Readiness requests review; it does not assert an AI outcome
or human acceptance. The full argument also addresses the rigorous review
obligations.

The algorithm is an unconditional birthday construction for this fixed hash with
a distribution-free probability bound. It combines **single-block messages** (so
every hash is exactly one reduced compression) with a **validated sparse
direct-address detector** that needs no initialization pass and no sorting, so the
charged work per sample is small. No ideal-hash, random-oracle, differential,
round-independence, or experimental-extrapolation premise is used. The required
`baseline_improved` value `sha256-r31-nominal-v2` only identifies the organizer's
nominal display reference; it is not an established attack, qualified baseline,
or security bound. This package does not claim improvement over that reference.
Its declared scalar is 128.05, with all bounds explained below.

## 1. Exact message and complete-hash definition

The target profile admits every finite byte string with bit length below 2^64.
Choose the following subset. Write BE_k(v) for the k-byte big-endian encoding of
integer v. Set

    z in [0, 2^288),   m(z) = BE_36(z),

so every message is exactly 36 bytes, and z -> m(z) is a bijection onto the
2^288 distinct 36-byte strings. Let D = 2^288 be that message count and let
N = 2^256 be the digest count.

A 36-byte message is padded by FIPS 180-4 into **exactly one** 512-bit block:
append the byte 0x80, append zero bytes until the length is 56 modulo 64 (here
36 + 1 = 37, so 19 zero bytes), then append the 64-bit big-endian original bit
length 288. The single padded block is

    message bytes 0..35, byte 0x80, 19 zero bytes, then BE_8(288).

Parsed as sixteen big-endian 32-bit words W[0],...,W[15], words W[0],...,W[8] are
the nine big-endian words of the 36 message bytes, W[9] = 0x80000000, W[10] =
... = W[14] = 0, and W[15] = 288. There is no second block.

Hash this block with the complete target's rules. All additions below are modulo
2^32; NOT and rotations operate on 32 bits. Define

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

Initialize the eight 32-bit chaining words once, in this order:

    6a09e667 bb67ae85 3c6ef372 a54ff53a
    510e527f 9b05688c 1f83d9ab 5be0cd19

Copy them into (a,b,c,d,e,f,g,h) and execute exactly t = 0,...,30 with
simultaneous updates:

    T1 = h + S1(e) + Ch(e,f,g) + K[t] + W[t]
    T2 = S0(a) + Maj(a,b,c)
    (a,b,c,d,e,f,g,h) = (T1+T2, a, b, c, d+T1, e, f, g).

After round 30 add all eight working words to the corresponding incoming
chaining words (here the fixed IV). Concatenate BE_4 of all eight state words in
standard order. This 32-byte output is H(m(z)); interpret it as one 256-bit
integer d(z) in the same big-endian order. Equality of d is equality of the full
digest. Because the message pads to one block, the model charges exactly one
selected-round target compression for H(m(z)): expansion, the 31 rounds and the
feed-forward are inside that single unit, and there is no second block.

Every one of the D messages is a valid target input, so two distinct messages
with equal H are an ordinary complete-message collision of this profile, not a
compression-only, free-start, or truncated-output artifact. The block contains
only rounds 0 through 30 of the standard schedule at their original indices, so
no round range, IV, padding rule, or output width is changed.

## 2. Concrete RAM algorithm and stopping rule

Every RAM word is 256 bits (32 bytes). Fix

    n = ceil(9943 * 2^128 / 10000) = 338342757429489114221633372169407132651.

Use the model's independent uniform random-word primitive; there is no finite
seed, deterministic PRNG expansion, or precomputed advice.

Sampling. For each i = 0,...,n-1 draw two fresh independent uniform 256-bit
words, retain 288 of their bits to obtain a fresh uniform z_i in [0, 2^288),
form the single padded block of section 1, compute d_i = H(m(z_i)), and reduce
d_i to one 256-bit word. Generate every sample on the same execution; there are
no restarts.

Detector. Write a digest key k as (P, X) with P = k >> 64 (the high 192 bits) and
X = k mod 2^64 (the low 64 bits). Maintain:

- a level-1 block table `L` of 2^192 word cells (never initialized);
- a list of lazily allocated blocks `Blk[b]`, each a 2^64-cell array, with
  `BP[b]` the 192-bit prefix that owns block b, and a block counter `nb`;
- a dense digest array `Dd` of n words, a dense message array `Dm` of n
  two-word messages (a 288-bit message needs two 256-bit cells), and a counter c.

For each sampled digest k with message m, membership is decided by:

    b = L[P]
    exists = (b < nb) and (BP[b] == P)
    if exists:
        j = Blk[b][X]
        if (j < c) and (Dd[j] == k):
            if Dm[j] != m:                       # distinct messages -> collision
                recompute H(m) and H(Dm[j]); verify full equality and message
                inequality; output both messages and halt
            else:
                skip (same message drawn twice; not a collision)
            continue
    # absent: insert
    if not exists:
        b = nb; BP[b] = P; Blk[b] = <fresh 2^64-cell block>; L[P] = b; nb = nb + 1
    Blk[b][X] = c; Dd[c] = k; Dm[c] = m; c = c + 1

The algorithm returns only a verified pair or, if all n samples are processed
without a distinct-message digest repeat, FAIL. There are no restarts or
amplification passes; the single fully charged execution is paid whether it
succeeds or fails.

Exactness of the detector (unconditional). Claim: membership returns PRESENT for
a freshly sampled key k if and only if k was inserted by an earlier sample.
- If k was inserted, then at insertion some block b with BP[b] = P and L[P] = b
  was allocated and Blk[b][X] was set to the dense index j with Dd[j] = k. Later
  insertions never change Blk[b][X] for the same (P,X) (a later duplicate would
  be caught as PRESENT, not re-inserted), so the test succeeds.
- Conversely, PRESENT requires Dd[j] = k for some dense index j < c. The dense
  array holds exactly the distinct digests of earlier samples, and every inserted
  digest is distinct (we halt at the first distinct-message repeat and skip
  repeated messages), so k was inserted.
No initialization is required. For an uninitialized L[P], the test `b < nb` may
pass and `BP[b] == P` is then read from a block index that has been initialized
(all indices below nb have BP set), so it equals P only for the genuine block of
P; a false positive is therefore impossible, and no clearing pass is charged.

Correctness. Whenever two of the n sampled messages have equal digests, the later
one triggers PRESENT, the distinct-message branch, the recomputation check, and a
halt with an ordinary collision. A returned pair is always distinct and has equal
complete hashes, confirmed by recomputation. Repeated copies of a single message
never count as success. FAIL has no claimed output relation.

Address-space feasibility. All structures are addressed by word-cell indices
below 2^256. The block table `L` uses 2^192 cells; at most n = 2^128 blocks are
allocated, each of 2^64 cells, so the blocks use at most 2^192 cells; the owner
list and dense arrays use at most 4 * 2^128 = 2^130 further cells, and code uses
2^21. Hence the algorithm touches at most 2^193 + 2^130 + 2^21 < 2^194 cells, well
below 2^256, and every cell address fits in one 256-bit word and never wraps.

## 3. Distribution-free birthday lemma

For each of the N possible digest values u let p_u be the fraction of the D
messages mapping to u under the fixed deterministic H. Retain zero entries.
Independent uniform messages induce independent output samples from this same p,
because H is applied separately to independent inputs. This says nothing about
whether p is uniform or SHA-256 behaves like a random function.

For a probability vector p let e_n(p) be the sum of products over all its
n-element coordinate subsets. The probability that n samples all differ is
n! e_n(p), since each unordered n-element set contributes its n! possible
orders. We prove that e_n(p) is maximized by the uniform vector.

The N-coordinate probability simplex is compact and e_n is continuous. Among its
maximizers choose one minimizing sum_u p_u^2; that choice exists by compactness.
If two coordinates a,b differ, call the other N-2 coordinates r. Splitting
subsets by which of these two coordinates they contain gives

    e_n(p) = e_n(r) + (a+b)e_(n-1)(r) + ab e_(n-2)(r).

Here e_0=1 and e_j=0 outside the available subset sizes. Every coefficient is
nonnegative. Averaging a,b preserves a+b and increases ab by (a-b)^2/4, so it
cannot decrease e_n. The result must still be a maximizer (a strict increase
would contradict maximality), but its sum of squared coordinates is strictly
smaller, a contradiction. Therefore all coordinates of that maximizer equal 1/N.
This proves the bound for every p, regardless of the actual hash's bias.

Since 2 <= n <= N, the probability of no repeated digest is at most

    n! binomial(N,n)/N^n
      = product_(j=0)^(n-1) (1-j/N)
      <= exp(-n(n-1)/(2N)).

The final inequality uses 1-u <= exp(-u) term by term and sums j/N. No
independence-of-collision-events assumption or structural property of H is used.

## 4. Algorithmic success probability and repeated inputs

Let C mean that some sampled digest repeats and R that some original message
repeats. The event C minus R guarantees two distinct messages with equal full
digests, which the algorithm finds. Without assuming independence of C and R,

    Pr(success) >= Pr(C) - Pr(R)
      >= 1 - exp(-n(n-1)/(2N)) - n(n-1)/(2D).

For two different positions the chance of equal 288-bit messages is exactly
1/D = 2^-288. The union bound over the binomial(n,2) position pairs gives the
repeated-input term n(n-1)/(2D).

With the chosen n, N = 2^256 and D = 2^288,

    n(n-1)/(2N) = 0.494316245... ,
    n(n-1)/(2D) = 2^-33.xxx < 2^-32.

For an elementary rational certification, let x = 0.494316245. The positive
exponential series gives the lower bound

    e^x > 1 + x + x^2/2 + x^3/6 + x^4/24 + x^5/120 + x^6/720 + x^7/5040
        + x^8/40320 > 1.639376,

so e^(-x) < 1/1.639376 < 0.60999 and hence 1 - e^(-x) > 0.39001. Therefore

    Pr(success) > 0.39001 - 2^-32 > 0.39.

The declared `success_probability: 0.39` is a lower bound on the algorithm's
success event under its fresh coins, not equality with actual success, confidence
in this proof, or confidence in an AI review. It meets the model minimum 0.39.
The entire n-sample construction is paid on failed runs too; there are no
restarts to account for beyond the single fully charged execution.

The digest distribution p is arbitrary; sections 3-4 never assume it is uniform
and never assume the message-to-digest map behaves like a random function. The
only randomness is the model's fresh independent uniform coins, which the
construction consumes directly and which the cost model prices.

## 5. Auditable resource implementation

These are worst-case bounds for every random tape in the specified classical
256-bit word RAM. Each selected compression costs one unit. Every other word
load, store, arithmetic/Boolean operation, shift, comparison, branch, and random
word costs 1/2140 target-compression units (the SHA-256 r31 reference operation
cost C = 2140 from `collision-frontier-v5`).

A core scalar action (an assignment, comparison, branch, address computation, or
load/store of a scalar) is charged through the eight-operation allowance: up to
four instruction-word fetches, two operand loads, the operation, and a result
store. Instruction fetch and operand access are thus charged explicitly, not
assumed free; a bare word load or store is one such action. The per-sample table
below counts, for each phase, the number of scalar actions and charges each at the
allowance of eight operations, so the per-sample bound is the sum over its phases.

| Phase | Scalar actions | Charged ordinary operations |
| --- | ---: | ---: |
| Draw two fresh random words | 1 | 8 |
| Form the 36-byte message (mask/truncate) and lay out nine block words | 1 | 8 |
| Copy the eight fixed IV words into working state | 1 | 8 |
| Dispatch the one compression call and read the 256-bit digest | 1 | 8 |
| Split the digest into prefix P and suffix X and form the block address | 1 | 8 |
| Level-1 probe (load L[P], test b < nb, load BP[b], compare) | 1 | 8 |
| Level-2 probe (load cell, test j < c, load Dd[j], compare) | 1 | 8 |
| Insert stores (block cell, Dd, Dm, counter) with amortized block allocation | 1 | 8 |
| Loop control | 1 | 8 |
| Total per sample, rounded upward | 9 | 72 |

The compression itself is one target-compression unit and is not in the table.
Thus at most 72 ordinary operations per sample. Fixed setup and program loading
cost at most 2^20 ordinary operations. Final verification is performed at most
once: two hashes through the same single-block wrapper, full-digest and message
comparisons, and output stores cost fewer than 2^14 ordinary operations plus two
compression calls. Hence H_calls <= n + 2 and

    W <= 72 n + 2^20 + 2^14.

Peak storage. The block table L has 2^192 cells = 2^197 bytes. At most n blocks
are allocated, each 2^64 cells = 2^69 bytes, giving at most 2^197 bytes. The
owner-prefix list `BP` and the dense arrays `Dd` (n words) and `Dm` (2n words)
use at most 3n + n = 4 * 2^128 words = 2^134 bytes. Code and fixed workspace add
2^20 bytes. Therefore

    M <= 2^197 + 2^197 + 2^134 + 2^20 < 2^198 bytes,

so the declared `memory_log2_bytes` is 199 (a conservative bound). Memory
contributes nothing to the scalar and is reported fully; it is far beyond any
physical machine, and all cells lie below 2^194 as shown in section 2.

Total time and auxiliary fields. With C = 2140,

    T = H_calls + W/2140
      <= (n + 2) + (72 n + 2^20 + 2^14)/2140
       = (1 + 72/2140) n + 2 + 497.7
       = 1.033645 n + 499.7
       < 2^128.0396  for the chosen n.

The declared `time_log2: 128.05` exceeds the reconstructed 2^128.0396. The
declared `preprocessing_log2: 8.94` is a conservative bound on the fixed setup in
target-compression units: fewer than 2^20 ordinary operations, i.e. fewer than
2^20/2140 = 489.99 < 2^8.94 units, and setup is already inside T. All setup, all
samples, every probe, every insertion and the verification are inside T; no phase
is omitted, and the compression internals are not charged twice. The optional
legacy `data_log2` field is omitted. `nonuniform_advice_log2_bytes: 0` is a
one-byte upper bound, as required by the nonnegative logarithmic schema; actual
nonuniform advice is zero bytes.

## 6. Evidence, scope, and limitations

The heuristic list is empty because sections 1-5 derive correctness, probability
and resources from the explicit target and model primitives. The detector's
exactness is a deterministic invariant unrelated to the digest distribution.
Fresh independent random words are part of the organizer's model, not an
empirical claim about a seeded program; there is no random-oracle or ideal-hash
assumption. The probability bound is distribution-free over every digest
distribution of the fixed hash.

The certificate manifest is valid and empty. There is no experiment manifest or
executable candidate source. A finite toy experiment adds no premise to the
all-distributions lemma and cannot establish this full-scale execution's success
or cost. All necessary analytic evidence is included here, without external-link
dependence or participant-code execution.

This is an astronomically expensive theoretical RAM construction, not a measured
run, practical attack, or new SHA-256 security result. It is an accounting-level
improvement over the organizer's baseline package, not a new cryptanalytic
advance and not a structural weakness of the 31-round compression. Any eventual
selected-lane AI qualification remains distinct from mathematical proof or human
acceptance, and scalar improvement is not Pareto dominance.

## 7. Source and accounting revision

This package revises the organizer's exploratory SHA-256 r31 baseline in
`lanes/exploratory/candidates/sha256-r31/`. It retains the baseline's
distribution-free birthday lemma, complete single-block definition and full
feed-forward/digest, and changes three things: messages are 36 bytes so each hash
is one block instead of two; the detector is a two-level validated direct-address
table (sparse-set invariant, addressable below 2^194 cells) instead of a
comparison merge sort, removing all per-sample comparison and clearing work; and
the sample count is the exact minimum n for success probability at least 0.39.
This is a new package requiring fresh ordinary review, not a replay of an earlier
qualification or a new cryptanalytic algorithm.
