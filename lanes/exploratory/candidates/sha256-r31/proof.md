# SHA-256, 31 prefix rounds: unconditional collision construction

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains
a separately reported resource bound.

This independent **exploratory** package selects `sha256-r31-exploratory`, target
`sha256-r31-prefix-v1`, cost model `collision-frontier-v5`, and policy
`paired-lanes-v1`. It submits a complete analytic algorithm, not an already
computed collision. Readiness requests review; it does not assert an AI outcome,
mathematical proof certification, human acceptance, or promotion.

The algorithm uses a birthday table with a fresh pairwise-universal tabulation
hash and a hard traversal cap. Its probability proof is distribution-free for
the fixed target hash. No ideal-hash, random-oracle, differential,
round-independence, or experimental-extrapolation premise is used. The required
`baseline_improved` value `sha256-r31-nominal-v2` only identifies the organizer's
nominal display reference; it is not an established attack, qualified baseline,
or security bound. The submitted scalar is 132, below the organizer package's
136, with every charged phase bounded below.

## 1. Exact message and complete-hash definition

Write BE_k(v) for the k-byte big-endian encoding of integer v. Set

    q = 2^129,  D = 2^512,  N = 2^256.

A sampled message is

    m(x,y) = BE_32(x) || BE_32(y),  0 <= x,y < 2^256.

This injectively identifies the D messages of exactly 64 bytes. Their 512-bit
length is less than 2^64. The message is hashed with the complete target's
padding, fixed IV, feed-forward, and full output, as follows.

Block 0 contains the original 64 message bytes. Block 1 is byte 0x80, then 55
zero bytes, then BE_8(512). In two 256-bit words block 1 is (2^255,512).
Initialize the eight 32-bit chaining words once, in this order:

    6a09e667 bb67ae85 3c6ef372 a54ff53a
    510e527f 9b05688c 1f83d9ab 5be0cd19

For EACH block, parse its 16 consecutive big-endian 32-bit words as
W[0],...,W[15]. All additions below are modulo 2^32; NOT and rotations operate
on 32 bits. Define

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
t=0,...,30 with simultaneous updates:

    T1 = h + S1(e) + Ch(e,f,g) + K[t] + W[t]
    T2 = S0(a) + Maj(a,b,c)
    (a,b,c,d,e,f,g,h) = (T1+T2, a, b, c, d+T1, e, f, g).

After round 30 add all eight working words to the corresponding incoming
chaining words. The result is the next block's incoming state; do not reset the
IV between blocks. After block 1 concatenate BE_4 of all eight state words in
standard order. This 32-byte output is H(m), interpreted as one 256-bit integer
d in the same big-endian order. Equality of d is equality of the full digest.

The model supplies one selected-round compression, including expansion and
feed-forward, at one unit. H uses two such units. Message handling, packing,
table operations, randomness, and control flow are charged separately below;
the primitive's internal rounds are not charged twice.

## 2. Fresh tabulation family

Let B=2^132. A bucket index is a 132-bit integer. Before sampling messages,
generate 16 tables T_0,...,T_15, each with 2^16 entries. Every entry is obtained
by drawing a fresh independent uniform 256-bit RAM word and retaining its low
132 bits. This setup therefore uses exactly 2^20 random words. It is regenerated
on every algorithm execution and is not nonuniform advice.

Split a digest d into its 16 consecutive 16-bit chunks d_0,...,d_15 in a fixed
big-endian order and define

    h(d) = T_0[d_0] XOR T_1[d_1] XOR ... XOR T_15[d_15].

For distinct digests d and e, choose any chunk position j where d_j != e_j.
Condition on every table entry except T_j[d_j]. The remaining entry is uniform
and independent, so h(d) XOR h(e) is uniform on 132 bits. Consequently

    Pr_h[h(d)=h(e)] = 2^-132

for every fixed distinct pair. Only this pairwise collision property is used;
the proof does not claim that SHA-256 outputs are uniform.

## 3. Concrete capped RAM algorithm

Every RAM word is 256 bits (32 bytes). Allocate B one-word bucket heads and set
all of them to the zero sentinel. Allocate space for q four-word records. Record
indices run from 1 through q so zero remains the sentinel. A record is

    (digest, x, y, next_record_index).

No object headers, pointers outside these word indices, allocator metadata, or
hidden storage are used. Maintain a counter `probes`, initially zero. Then:

1. Generate the fresh tabulation family and clear every bucket head.
2. For i=1,...,q, draw fresh independent uniform words x and y, compute
   d=H(m(x,y)), and set p to the head of bucket h(d).
3. While p is nonzero:
   - if `probes` equals K=2^128, return FAIL; otherwise increment `probes`;
   - load record p;
   - if its digest equals d and either message word differs, copy both messages,
     recompute both complete hashes from the fixed IV, require distinctness and
     full-digest equality, and return the pair;
   - otherwise follow the stored next index.
4. If the chain ends, store (d,x,y,old_head) in record i and make i the new head.
5. Return FAIL if all q samples are processed without returning a pair.

Every execution has fixed allocation bounds, processes at most q iid samples,
and performs at most K record probes. For probability analysis, couple its lazy
draws to a length-q iid sequence by appending unused independent pairs after any
early return; those unused variables cost nothing because the algorithm never
reads them. Duplicate copies of one message never count as a collision. A
returned pair is always distinct and is verified against the exact complete
target. All failed runs, setup, table clearing, actual random draws, and cap
handling are included in the cost.

## 4. Distribution-free collision probability

For each of the N possible digest values z, let p_z be the fraction of the D
64-byte messages mapping to z under fixed deterministic H. Independent uniform
messages induce independent samples from p. This statement does not assume that
p itself is uniform.

For a probability vector p, let e_q(p) be the q-th elementary symmetric sum.
The probability that q output samples all differ is q! e_q(p). To see where
this is maximized, fix all coordinates except two, a and b. With r denoting the
other coordinates,

    e_q(p) = e_q(r) + (a+b)e_(q-1)(r) + ab e_(q-2)(r).

All coefficients are nonnegative. The probability simplex is compact and e_q
is continuous, so a maximizer exists. Among all maximizers choose one minimizing
the continuous quantity sum_z p_z^2. If two coordinates a,b differ, averaging
them preserves a+b and increases ab. It therefore cannot decrease e_q; a strict
increase would contradict maximality. The averaged vector is consequently also
a maximizer, but its sum of squared coordinates is smaller by (a-b)^2/2, a
contradiction. Thus every coordinate of this chosen maximizer equals 1/N.
Hence, for every fixed target H,

    Pr(no repeated digest)
      <= product_(j=0)^(q-1) (1-j/N)
      <= exp(-q(q-1)/(2N)).

Here q(q-1)/(2N)=2-2^-128>3/2. The exponential series gives

    exp(3/2) > 1 + 3/2 + (3/2)^2/2 + (3/2)^3/6
             = 67/16 > 4,

so exp(-3/2)<1/4 and therefore the probability C of at least one repeated
digest is greater than 3/4.

Let R be the event that an original 512-bit message repeats. A union bound gives

    Pr(R) <= binomial(q,2)/D < 2^-255.

On the complement of R, before the algorithm returns a collision, every
nonterminal record probe is between two distinct messages with distinct
digests. For each such unordered sample pair, the tabulation lemma bounds the
probability of sharing a bucket by 2^-132. Let V count all such distinct-digest
bucket-sharing pairs among the q samples. Linearity of expectation, without
independence between pairs, yields

    E[V] <= binomial(q,2)/B < 2^125.

Markov's inequality therefore gives

    Pr(V >= K) < 2^125 / 2^128 = 1/8.

If C occurs while neither R nor V>=K occurs, fewer than K nonterminal probes can
precede the first distinct-message equal-digest pair. Its terminal probe is
therefore among the K permitted probes, so it is found before the cap. A union
bound thus proves

    Pr(success) >= Pr(C) - Pr(R) - Pr(V>=K)
                > 3/4 - 2^-255 - 1/8
                = 5/8 - 2^-255
                > 3/5 = 0.60.

This proves the declared `success_probability: 0.6` for one fully charged
execution. The probability is about algorithmic coins, not confidence in this
argument, an AI review, or a reviewer decision.

## 5. Auditable resource implementation

These are worst-case bounds for every random tape. Each selected compression
costs one unit. Every other permitted 256-bit load/store, addition/subtraction,
Boolean operation, shift, comparison, branch, or random-word draw costs 1/2140
target-compression units.

For auditability, call one source-level RAM action a core operation. Even when
its operands and result require explicit memory traffic and its instruction is
fetched from stored code, charge at most eight primitive word operations per
core operation. The bounds below apply that factor before pricing by 1/2140.

### 5.1 Per-sample and traversal bounds

For each processed sample, excluding chain traversal, at most 8192 ordinary
operations cover all of the following:

- two random-word draws and loop control;
- packing the 64-byte message, fixed padding access, IV/state transfer, and
  dispatch of two separately charged compression calls;
- extraction of 16 digest chunks, 16 addressed table reads, XOR accumulation,
  and the bucket-head read;
- four-word record addressing and insertion, index arithmetic, branches,
  instruction fetches, spills, and unused slack.

This is more than 1024 core operations per generated record. Direct tabulation
needs fewer than 16 chunk extractions, 16 table-address calculations, 16 table
loads, 16 XORs, and a bounded loop shell; the remaining allowance dominates
message-interface and insertion work.

One record probe costs at most 1024 ordinary operations. This is
128 core operations for addressing, four field loads, digest and message
comparisons, counter handling, next-index handling, branches, fetches, spills,
and slack. There are at most K=2^128 such probes.

Final verification occurs at most once and costs at most four additional
compression calls and 8192 ordinary operations, including message/digest
comparisons and output stores.

### 5.2 Setup and preprocessing

Clearing one bucket needs at most eight core operations: address handling, the
sentinel store, counter update, bound comparison, branches, and slack. Including
the factor of eight, clearing all B buckets costs at most

    64B = 2^138 ordinary operations.

Generating and storing each of the 2^20 tabulation entries needs at most 16 core
operations, including a random draw, mask, address operations, loop handling,
fetches, and spills, for at most 2^27 ordinary operations. Loading fixed code,
constants, IV, scratch, and array bases costs less than 2^30 further ordinary
operations. Thus setup costs less than

    (2^138 + 2^27 + 2^30)/2140 < 2^128

target-compression units. It is included in total time, and
`preprocessing_log2: 128` is a conservative upper bound rather than a separate
discount.

### 5.3 Total time

Separating supplied compression calls from ordinary operations gives

| Phase | Compression calls | Ordinary operations |
| --- | ---: | ---: |
| Fixed setup and bucket clearing | 0 | at most 2^138 + 2^27 + 2^30 |
| Generate, hash, and insert up to q records | 2q | at most 8192q |
| All chain probes | 0 | at most 1024K = 2^138 |
| Final verification/output | at most 4 | at most 8192 |

With q=2^129 and K=2^128,

    H_calls <= 2q+4,
    W <= 8192q + 2*2^138 + 2^30 + 2^27 + 8192
      < (9/8 + 1/4096) * 2^142.

Since 2140>2048=2^11,

    T = H_calls + W/2140
      < 2^130 + 4 + (9/8 + 1/4096)*2^131
      < 2^132.

This proves `time_log2: 132`. The bound charges the full q-sample execution even
when a collision would be found early. It also charges all cap visits, failed
runs, randomness, initialization, and verification; no expected running-time
discount is used.

### 5.4 Peak storage and address width

The bucket array contains exactly B words, or 2^137 bytes. The four-word record
array contains 4q words, or 2^136 bytes. The tabulation family contains 2^20
words, or 2^25 bytes. Fixed code, constants, scratch, message buffers, saved
output, counters, and state occupy less than 2^20 bytes. Therefore

    M < 2^137 + 2^136 + 2^25 + 2^20 < 2^138 bytes.

This proves `memory_log2_bytes: 138`. Bucket indices are 132 bits; record indices
are at most 129 bits; byte addresses are below 2^138. All fit in one 256-bit RAM
word without wraparound. The algorithm assumes the abstract model's memory,
not physical feasibility on a present machine.

`nonuniform_advice_log2_bytes: 0` is the schema's one-byte upper bound; actual
nonuniform advice is zero bytes. Public fixed code, the SHA-256 specification,
IV, and constants are uniform specification data, and their storage and setup
remain charged. The optional legacy `data_log2` field is omitted because it is
not a scored or reviewed resource and the schema recommends omitting it in new
claims.

## 6. Evidence, scope, and limitations

The heuristic list is empty. Sections 1-5 derive correctness, probability, and
resource bounds only from the exact target and the organizer's RAM/randomness
model. The tabulation tables and messages use fresh independent random words,
as the model permits. No empirical claim or property of SHA-256's observed
distribution enters the proof.

The certificate manifest is valid and empty. There is no experiment manifest or
participant executable. Finite experiments cannot execute the astronomical
abstract construction and would add no support to its all-distributions
argument. All analytic evidence needed for review is included here.

This is a generic, astronomically expensive theoretical collision construction,
not a practical attack, a differential result, a measured execution, or a new
security claim about 31-round SHA-256. The improvement is resource accounting:
pairwise-universal bucketing plus a probabilistically budgeted traversal cap
removes the baseline merge sort's 129 full passes. An exploratory AI
qualification would remain distinct from mathematical proof, human acceptance,
and successful manual promotion.

## 7. Starting package and independent revision

The starting candidate was the organizer's score-136 package at repository
commit `86f1102ff2d6873db29d992599412ae9eb23bda2`. This revision retains its exact
complete-hash definition, iid 512-bit message sampling, distribution-free
birthday lemma, distinct-input accounting, and memory scale. It independently
replaces the two-array merge sort with the fresh tabulation construction above.
No unpromoted solver package, certificate, differential characteristic, measured
search, or historical-work estimate is incorporated.
