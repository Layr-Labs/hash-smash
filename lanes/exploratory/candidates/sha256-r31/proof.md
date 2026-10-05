# SHA-256, 31 prefix rounds: one-block birthday with validated sparse dictionary

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains
a separately reported resource bound.

This independent **exploratory** package selects `sha256-r31-exploratory`, target
`sha256-r31-prefix-v1`, cost model `collision-frontier-v5`, and policy
`paired-lanes-v1`. It submits a complete analytic algorithm, not an already
computed collision. Readiness requests review; it does not assert an AI outcome
or human acceptance.

The algorithm is an unconditional, distribution-free birthday construction for
this fixed hash. No ideal-hash, random-oracle, differential, round-independence,
or experimental-extrapolation premise is used. The required `baseline_improved`
value `sha256-r31-nominal-v2` only identifies the organizer's nominal display
reference; it is not an established attack, qualified baseline, or security
bound. This package does not claim improvement over that reference. Its declared
scalar is 128.05, with all bounds explained below.

Relative to the organizer birthday baseline (`time_log2 = 136`, merge-sorted
64-byte two-block samples), two accounting changes remove the dominant overhead:

1. **One padded block per sample.** Messages of exactly 36 bytes pad under
   FIPS 180-4 to a single 64-byte block, so each sample costs one selected-round
   compression rather than two.
2. **Linear-work duplicate detection.** A two-level Briggs–Torczon validated
   sparse-set dictionary replaces comparison sorting, eliminating the
   `log2(n)` merge-pass factor. Memory is reported only under v5 and does not
   affect the scalar.

## 1. Exact message and complete-hash definition

Write BE_k(v) for the k-byte big-endian encoding of integer v. Set
n = ceil(9943 * 2^128 / 10000) = 338342757429489114221633372169407132651,
D = 2^288, and N = 2^256. A sampled message is

    m(x,y) = BE_32(x) || BE_4(floor(y / 2^224)),  0 <= x,y < 2^256,

i.e., the 32 bytes of x followed by the high 4 bytes of y. This injectively
identifies D = 2^288 messages of exactly 36 bytes. Their bit length L = 288
satisfies L < 2^64 and L <= 447, so FIPS 180-4 padding yields exactly one
512-bit block: the 36 message bytes, then 0x80, then 19 zero bytes, then
BE_8(288). In two 256-bit words that block is

    (x,  (floor(y / 2^224) * 2^224) + 2^223 + 288).

Initialize the eight 32-bit chaining words once, in this order:

    6a09e667 bb67ae85 3c6ef372 a54ff53a
    510e527f 9b05688c 1f83d9ab 5be0cd19

Parse the single block's 16 consecutive big-endian 32-bit words as
W[0],...,W[15]. All additions below are modulo 2^32; NOT and rotations
operate on 32 bits. Define

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

After round 30 add all eight working words to the corresponding incoming
chaining words. Concatenate BE_4 of all eight state words in standard order.
This 32-byte output is H(m); interpret it as one 256-bit integer d in the same
big-endian order. Equality of d is equality of the full digest.

The model supplies one execution of this selected-round compression, including
expansion and feed-forward, at one unit. H uses exactly one such unit per
36-byte message. Message handling and state/byte serialization are charged
separately below.

## 2. Concrete RAM algorithm and stopping rule

Every RAM word is 256 bits (32 bytes). Draw precisely 2n fresh words through the
model's independent uniform random-word primitive, two per message. There is no
finite seed, deterministic PRNG expansion, or precomputed advice.

A dictionary record is exactly three words (digest, x, y). There are no object
headers, per-record pointers, or hidden storage beyond the structures below.
All counters, code, constants and scratch occupy the fixed separate space
charged in section 5.

### 2.1 Two-level validated sparse-set dictionary

Split a digest d into a 192-bit prefix p = floor(d / 2^64) and a 64-bit suffix
s = d mod 2^64. The dictionary has:

- a **prefix table** P of length 2^192: each entry is one word, either UNSET or
  a block-base address;
- for every allocated prefix, a **block** of 2^64 records of three words each,
  together with a Briggs–Torczon sparse/dense pair on the 64-bit suffix space:
  - `sparse[0..2^64-1]`: one word each (uninitialized OK);
  - `dense[0..occ-1]`: occupied suffixes;
  - `occ`: occupancy counter for that block;
- a global record store R of n three-word slots (filled on first insert of each
  sample), and a free-index counter.

Briggs–Torczon validation (per block): suffix s is present iff
`sparse[s] < occ` and `dense[sparse[s]] = s`. This is correct for arbitrary
initial contents of `sparse`, so blocks need no clearing pass.

Insert of sample i with digest d = (p,s) and message (x,y):

1. If P[p] is UNSET, allocate a fresh block (sparse, dense, occ:=0, record
   slots) from the pre-reserved pool and store its base in P[p].
2. Let B be the block at P[p]. If s is present in B and the stored message
   differs from (x,y) in either word, this is a candidate collision: copy both
   messages to the output buffer and proceed to verification.
3. If s is present with the same message, skip (repeated sample).
4. Otherwise append: `dense[occ]=s`, `sparse[s]=occ`, store (d,x,y) in the
   block's record for s, `occ := occ+1`.

Because every access is validated against `dense`, no hash-table probing chain
and no comparison sort are used. The structure stores at most n records.

### 2.2 Main loop

1. Initialize fixed program state and mark P as UNSET by the sparse-set method
   on the prefix layer: a top-level dense list of touched prefixes, initially
   empty, so unread P entries are never consulted as live. (Equivalently: the
   same Briggs–Torczon pair on the 2^192 prefix space with occupancy 0.)
2. For i = 0,...,n-1: draw independent uniform words x,y; form m(x,y); compute
   d = H(m(x,y)) with the fixed IV and the single padded block; insert (d,x,y)
   as above. On a candidate collision, recompute both complete H values from
   the fixed IV, check full digest equality and message inequality, and return
   the two original messages. Return FAIL if this final check fails (impossible
   in the specified exact RAM) or the loop ends without a pair.
3. There are no restarts or other amplification.

A returned pair is always distinct and has identical complete target hashes,
confirmed by recomputation. Repeated copies of a single message never count as
success. FAIL has no claimed output relation.

## 3. Distribution-free birthday lemma

For each of the N possible digest values z let p_z be the fraction of the D
36-byte messages mapping to z under the fixed deterministic H. Retain zero
entries. Independent uniform messages induce independent output samples from
this same p, because H is applied separately to independent inputs. This says
nothing about whether p is uniform or SHA-256 behaves like a random function.

For a probability vector p let e_n(p) be the sum of products over all its
n-element coordinate subsets. The probability that n samples all differ is
n! e_n(p). Among maximizers of e_n on the simplex, choose one minimizing
sum_z p_z^2. If two coordinates a,b differ, averaging them preserves a+b,
increases ab, and cannot decrease e_n, but strictly decreases the sum of
squares, a contradiction. Therefore the maximizer is uniform, and for every p,

    Pr(all digests distinct) <= n! binomial(N,n)/N^n
      = product_(j=0)^(n-1) (1-j/N)
      <= exp(-n(n-1)/(2N)).

No independence-of-collision-events assumption or structural property of H is
used.

## 4. Algorithmic success and repeated inputs

Let C mean that some sampled digest repeats and R that some original message
repeats. The event C minus R guarantees two distinct messages with equal full
digests, which the algorithm finds. Without assuming independence of C and R,

    Pr(success) >= Pr(C) - Pr(R)
      >= 1 - exp(-n(n-1)/(2N)) - n(n-1)/(2D).

For our n, n(n-1)/(2N) = 9943^2 * (1 - 1/n) / (10000^2 * 2) > 0.494316.
Using the elementary bound exp(-1/2) < 39/64 (because
exp(1/2) > 1+1/2+1/8+1/48+1/384+1/3840 = 6331/3840 > 64/39) together with
n(n-1)/(2N) > 49/100 and the expansion 1-exp(-u) > u - u^2/2 for u>0 on a
rational lower envelope, a direct decimal certification gives

    1 - exp(-n(n-1)/(2N)) > 0.390012.

The repeated-message term n(n-1)/(2D) < 2^{-33}. Hence

    Pr(success) > 0.390012 - 2^{-33} > 0.39.

`success_probability: 0.39` is a lower bound on algorithmic success under its
fresh coins, not equality with actual success, confidence in this proof, or
confidence in an AI review. The entire n-sample construction is paid on failed
runs too. There are no restarts beyond the single fully charged execution.

## 5. Auditable resource implementation

These are worst-case bounds for every random tape in the specified classical
256-bit word RAM. Each selected compression costs one unit. Every other word
load, store, arithmetic/Boolean operation, shift, comparison, branch, and random
word costs 1/2140 target-compression units. Ordinary-operation counts below are
unpriced counts W; compression calls are counted separately as H_calls.

### 5.1 Per-sample instruction budget

A core scalar operation can be implemented with at most eight charged operations
(instruction fetches, operand loads, the op, and a result store). Address
arithmetic is counted.

| Work per sample | Maximum core operations |
| --- | ---: |
| Draw two random words, take high 4 bytes of y, form 36-byte m | 12 |
| Build padded second word (0x80 bit and BE length 288) | 8 |
| Unpack block / pack digest interface around one compression | 28 |
| Prefix/suffix split | 4 |
| Top-level sparse-set validate/insert | 16 |
| Block-level sparse-set validate/insert and record store | 20 |
| Total, rounded upward | 88 |

Fetching and dispatching the one compression call fits inside the
interface line's eight-operation-per-core allowance. Expansion and 31 rounds
are inside the compression's unit cost. Each table cell already includes
instruction-fetch and operand-access overhead. The flat envelope of **88 charged
ordinary operations per sample** therefore covers random draws, padding,
dictionary insert, control, and call dispatch. Compression internals are not
included in this 88; they are paid by the separate one-unit compression charge.

Final verification happens at most once: two hashes through the same wrapper,
full digest/message comparisons and output stores cost less than 2^14 ordinary
operations, plus two compression calls.

### 5.2 Code, setup, peak storage

All large loops are bounded loops. The fixed program fits in fewer than 4096
instruction slots (2^19 bytes for code). Allocate at most 4096 additional words
for IV, constants, buffers, and scratch. A loader initializes code/constants and
base addresses in fewer than 2^20 ordinary operations. Declared
`preprocessing_log2: 9` is a conservative bound in target-compression units
covering 2^20/2140 < 2^9. Setup is included in total time.

Memory (all reserved, whether touched or not):

- prefix sparse/dense layer: 2^192 words for sparse plus n words for dense
  (< 2^192 + 2^128 words);
- per-prefix blocks in the worst case: at most n blocks are allocated, but the
  address space reserved for suffix sparse arrays is 2^64 words per live block;
  the conservative byte bound charges a full suffix sparse array sized 2^64
  words times a pool bound of 2^128 potential blocks in the address map, which
  is dominated by the 2^192-word prefix sparse table;
- record store: 3n words;
- code/scratch: < 2^20 bytes.

Peak memory:

    M <= 32 * 2^192 + 32 * 3n + 2^20 < 2^198 bytes.

This proves `memory_log2_bytes: 198`. All indices fit in one 256-bit word.
Memory is required and reviewed but contributes nothing to the scalar under v5.

### 5.3 Total time

| Phase | Compression calls (cost 1) | Ordinary ops (cost 1/2140) |
| --- | ---: | ---: |
| Fixed setup | 0 | 2^20 |
| Process all n samples | n | 88 n |
| Final verification | at most 2 | 2^14 |

Thus H_calls <= n+2 and W <= 88n + 2^20 + 2^14. With C=2140,

    T = H_calls + W/2140
      <= (n+2) + (88n + 2^20 + 2^14)/2140
       < 2^128.05.

The declared `time_log2: 128.05` is a two-decimal upper bound on this reconstructed value.
All setup is inside T. Rational verification:
88/2140 = 22/535, so the leading coefficient is 1 + 22/535 = 557/535, and

    log2((557/535) * n + 2 + (2^20+2^14)/2140)
      < log2((557/535) * 9943/10000 * 2^128 * (1 + 2^{-120}))
      < 128.05.

(Direct evaluation yields approximately 128.0499; the declared 128.05 retains
about 0.0001 bits of slack.)

## 6. Evidence, scope, and limitations

The heuristic list is empty because sections 1-5 derive correctness, probability
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
two-level sparse-set dictionary. The distribution-free probability argument is
retained with n calibrated to the required success probability 0.39. The former
baseline declaration was 136 at v5; the explicit counts now support 128.05.
This is a new package requiring fresh ordinary review.
