# SHA-256, 32 prefix rounds: unconditional collision construction (radix-sort accounting)

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains
a separately reported resource bound.

This independent **exploratory** package selects `sha256-r32-exploratory`, target
`sha256-r32-prefix-v1`, cost model `collision-frontier-v5`, and policy
`paired-lanes-v1`. It submits a complete analytic algorithm, not an already
computed collision. Readiness requests review; it does not assert an AI outcome
or human acceptance. The full argument also addresses the rigorous review obligations.

The algorithm uses a large birthday table with a distribution-free proof for
this fixed hash. No ideal-hash, random-oracle, differential, round-independence,
or experimental-extrapolation premise is used. The required `baseline_improved`
value `sha256-r32-nominal-v2` only identifies the organizer's nominal display
reference; it is not an established attack, qualified baseline, or security
bound. This package does not claim improvement over that reference. Its declared
scalar is 131.6, with all bounds explained below.

The only substantive difference from the organizer's prior conservative baseline
package (which declared 136) is that the collision-detection step sorts the
record array with a **two-pass least-significant-digit radix (counting) sort**
on the 256-bit digest, rather than a `log2(q)`-pass comparison merge sort. The
cost model charges memory as a reported metric only with no scalar contribution,
so the radix bucket arrays are fully charged in memory and in time but do not
affect the score through memory. Replacing the sort removes the dominant
`log2(q)` factor from the ordinary-operation ledger; the message definition, the
distribution-free probability proof, and the success lower bound are retained
verbatim.

## 1. Exact message and complete-hash definition

Write BE_k(v) for the k-byte big-endian encoding of integer v. Set q = 2^129,
D = 2^512, and N = 2^256. A sampled message is

    m(x,y) = BE_32(x) || BE_32(y),  0 <= x,y < 2^256.

This injectively identifies the D messages of exactly 64 bytes. Their 512-bit
length is less than 2^64. The message is hashed with the complete target's
padding, fixed IV, feed-forward, and full output, as follows.

Block 0 contains the original 64 message bytes. Block 1 is byte 0x80, then 55
zero bytes, then BE_8(512). In two 256-bit words block 1 is (2^255,512).
Initialize the eight 32-bit chaining words once, in this order:

    6a09e667 bb67ae85 3c6ef372 a54ff53a
    510e527f 9b05688c 1f83d9ab 5be0cd19

For EACH of the two blocks, parse its 16 consecutive big-endian 32-bit words
as W[0],...,W[15]. All additions below are modulo 2^32; NOT and rotations
operate on 32 bits. Define

    s0(z) = ROTR32(z,7) XOR ROTR32(z,18) XOR (z >> 3)
    s1(z) = ROTR32(z,17) XOR ROTR32(z,19) XOR (z >> 10)
    S0(z) = ROTR32(z,2) XOR ROTR32(z,13) XOR ROTR32(z,22)
    S1(z) = ROTR32(z,6) XOR ROTR32(z,11) XOR ROTR32(z,25)
    Ch(e,f,g) = (e AND f) XOR ((NOT e) AND g)
    Maj(a,b,c) = (a AND b) XOR (a AND c) XOR (b AND c)
    W[t] = W[t-16] + s0(W[t-15]) + W[t-7] + s1(W[t-2]),
        for t = 16,...,31.

The constants K[0],...,K[31] are, in hexadecimal and original index order,

    428a2f98 71374491 b5c0fbcf e9b5dba5 3956c25b 59f111f1 923f82a4 ab1c5ed5
    d807aa98 12835b01 243185be 550c7dc3 72be5d74 80deb1fe 9bdc06a7 c19bf174
    e49b69c1 efbe4786 0fc19dc6 240ca1cc 2de92c6f 4a7484aa 5cb0a9dc 76f988da
    983e5152 a831c66d b00327c8 bf597fc7 c6e00bf3 d5a79147 06ca6351 14292967

Copy the incoming chaining words into (a,b,c,d,e,f,g,h), then execute exactly
t = 0,...,31 with simultaneous updates:

    T1 = h + S1(e) + Ch(e,f,g) + K[t] + W[t]
    T2 = S0(a) + Maj(a,b,c)
    (a,b,c,d,e,f,g,h) = (T1+T2, a, b, c, d+T1, e, f, g).

After round 31 add all eight working words to the corresponding incoming
chaining words. The result is the next block's incoming state; do not reset the
IV between blocks. After block 1 concatenate BE_4 of all eight state words in
standard order. This 32-byte output is H(m); interpret it as one 256-bit integer
d in the same big-endian order. Equality of d is equality of the full digest.

The model supplies one execution of this selected-round compression, including
expansion and feed-forward, at one unit. H uses two such units. Its message
handling and state/byte serialization are charged separately below; the internal
32 rounds are not charged a second time. A wrapper can unpack a 256-bit word
into eight 32-bit words using shifts/masks and pack the final state by shifts/ORs.
These interface operations are included even if the compression primitive
already accepts packed blocks and states.

## 2. Concrete RAM algorithm and stopping rule

Every RAM word is 256 bits (32 bytes). Draw precisely 2q fresh words through the
model's independent uniform random-word primitive, two per message. There is no
finite seed, deterministic PRNG expansion, or precomputed advice.

A record is exactly three words (digest,x,y); the last two retain the original
message. There are no object headers, per-record pointers, or hidden storage.
One array A of q contiguous records holds the sample; a second array B of q
records is the radix-sort scratch destination. Record i has word address
base+(i+i+i): multiplication is not an assumed primitive. All counters, code,
constants and scratch occupy the fixed separate space charged in section 5.

1. Initialize the fixed program state. For i = 0,...,q-1 draw independent uniform
   words x,y, compute H(m(x,y)) using the fixed IV and both padded blocks, and
   store (H(m(x,y)),x,y) in A[i]. Generate the entire table on every execution.
2. Sort the q records by their unsigned 256-bit `digest` field using the
   two-pass least-significant-digit radix sort of section 2.1. The sort is
   stable and groups all records that share a digest into a contiguous run.
3. Scan the sorted array from index 1 to q-1, comparing each record with its
   predecessor. At the first equal digest with either message word different,
   copy both messages into the fixed output buffer. Recompute both complete H
   values from the fixed IV, check full equality and message inequality, and
   return the two original messages. Return FAIL if this final check fails
   (impossible in the specified exact RAM) or the scan ends without a pair.
   There are no restarts or other amplification.

### 2.1 Two-pass radix (counting) sort on the 256-bit digest

Split the 256-bit digest key of each record into two 128-bit digits: digit 0 is
the low 128 bits and digit 1 is the high 128 bits. The sort performs two stable
counting-sort passes, digit 0 first, then digit 1. Each pass uses a count array
`cnt` of exactly R = 2^128 words, allocated and fully charged. Memory is a
reported metric with no scalar contribution, so the 2^128-word count array and
the second record array are permitted and are charged below in both the time and
memory ledgers.

A single pass, reading source base S and writing destination base T for the
current digit `g` (a shift of 0 or 128 followed by a 128-bit mask):

    for b = 0 .. R-1:            # zero the count array
        cnt[b] = 0
    for i = 0 .. q-1:            # count occurrences of each digit value
        d = (S[i].digest >> g) AND (2^128 - 1)
        cnt[d] = cnt[d] + 1
    acc = 0                      # exclusive prefix sums -> bucket start offsets
    for b = 0 .. R-1:
        t = cnt[b]; cnt[b] = acc; acc = acc + t
    for i = 0 .. q-1:            # stable scatter into destination
        d = (S[i].digest >> g) AND (2^128 - 1)
        pos = cnt[d]; cnt[d] = pos + 1
        copy all three words of S[i] to T[pos]

Pass 1 reads A, writes B. Pass 2 reads B, writes A. After both passes A holds
the records in nondecreasing `digest` order: least-significant-digit radix sort
with a stable per-digit counting sort is a standard, deterministic,
distribution-free sorting algorithm, and two 128-bit digits cover the full
256-bit key. Stability of each pass guarantees that records equal on the current
and all lower digits keep their relative order, so the final array is totally
ordered by the 256-bit digest. No comparison, hash table, recursion, or
variable-length operation is used.

Because the sort only reorders whole three-word records, every record keeps its
own (digest,x,y). All records sharing a digest are therefore contiguous after
the sort. If such a group contains two distinct messages, some adjacent pair in
the group has equal digest and unequal message, so the scan in step 3 finds an
ordinary collision whenever one exists among the samples. A returned pair is
always distinct and has identical complete target hashes, confirmed by
recomputation. Repeated copies of a single message never count as success. FAIL
has no claimed output relation.

## 3. Distribution-free birthday lemma

For each of the N possible digest values z let p_z be the fraction of the D
64-byte messages mapping to z under the fixed deterministic H. Retain zero
entries. Independent uniform messages induce independent output samples from
this same p, because H is applied separately to independent inputs. This says
nothing about whether p is uniform or SHA-256 behaves like a random function.

For a probability vector p let e_q(p) be the sum of products over all its
q-element coordinate subsets. The probability that q samples all differ is
q! e_q(p), since each unordered q-element set contributes its q! possible orders.
We now prove that e_q(p) is maximized by the uniform vector.

The N-coordinate probability simplex is compact and e_q is continuous. Among
its maximizers choose one minimizing sum_z p_z^2; that choice exists by
compactness. If two coordinates a,b differ, call the other N-2 coordinates r.
Splitting subsets by which of these two coordinates they contain gives

    e_q(p) = e_q(r) + (a+b)e_(q-1)(r) + ab e_(q-2)(r).

Here e_0=1 and e_j=0 outside the available subset sizes. Every coefficient is
nonnegative. Averaging a,b preserves a+b and increases ab by (a-b)^2/4, so it
cannot decrease e_q. The result must still be a maximizer (a strict increase
would contradict maximality), but its sum of squared coordinates is strictly
smaller, a contradiction. Therefore all coordinates of that maximizer equal
1/N. This proves the bound for every p, regardless of the actual hash's bias.

Since 2 <= q <= N, the probability of no repeated digest is at most

    q! binomial(N,q)/N^q
      = product_(j=0)^(q-1) (1-j/N)
      <= exp(-q(q-1)/(2N)).

The final inequality uses 1-u <= exp(-u) term by term and sums j/N. No
independence-of-collision-events assumption or structural property of H is used.

## 4. Algorithmic success and repeated inputs

Let C mean that some sampled digest repeats and R that some original message
repeats. The event C minus R guarantees two distinct messages with equal full
digests, which the algorithm finds. Without assuming independence of C and R,

    Pr(success) >= Pr(C) - Pr(R)
      >= 1 - exp(-q(q-1)/(2N)) - q(q-1)/(2D).

For two different positions the chance of equal 512-bit messages is exactly
1/D. The union bound over binomial(q,2) position pairs gives the repeated-input
term. There is no rejection sampling or uncharged sampling without replacement.

For our parameters q(q-1)/(2N)=2-2^-128>1 and
q(q-1)/(2D)=2^-255-2^-384<2^-255. For an elementary rational certification of
the declared decimal, exp(1)>1+1+1/2+1/6=8/3, so exp(-1)<3/8, hence
exp(-(2-2^-128))<exp(-1)<3/8. Thus

    Pr(success) > 5/8 - 2^-255 > 3/5 = 0.60 > 0.39,

where 2^-255<1/40=5/8-3/5. `success_probability: 0.6` is a lower bound on
algorithmic success under its fresh coins, not equality with actual success,
confidence in this proof, or confidence in an AI review. The entire q-sample
construction and the sort are paid on failed runs too. There are no restarts to
account for beyond the single fully charged execution.

## 5. Auditable resource implementation

These are worst-case bounds for every random tape in the specified classical
256-bit word RAM. Each selected compression costs one unit. Every other word
load, store, arithmetic/Boolean operation, shift, comparison, branch, and random
word costs 1/2224 target-compression units. In the instruction budgets below,
ordinary-operation counts are unpriced counts W, not target-compression units.
Compression calls are counted separately as H_calls; their expansion and round
internals are not included in W. Constants and bytes are retained below.

### 5.1 Instruction and interface budgets

A core scalar operation (two-operand arithmetic/comparison, assignment, branch,
or load/store) can be implemented with at most eight charged operations even
when scalar operands/results live in scratch: up to four instruction-word
fetches, two operand loads, the operation, and a result store. Thus instruction
fetches are charged explicitly as well. Constants fit that allowance. Address
calculation is itself counted as core work; base+3*i uses three additions. A
record copy uses three addressed loads and three addressed stores. Loops,
branches and addressing are not free.

**Generation wrapper.** The generation wrapper uses at most 200 ordinary core
operations per message, plus two random-word instructions and dispatch of two
compression calls. A direct wrapper uses at most 32 shifts/masks to unpack the
first block, 24 shifts/ORs to pack the final digest, and 144 further operations
for IV/state copies, access to the already initialized padding block, record
addressing/stores and loop control. Fetching and dispatching the two random-word
instructions and two compression calls can each be allowed eight operations.
This is at most 8*200+8*4<2048 ordinary operations per sampled message. The two
compression calls themselves cost two additional target-compression units.

**Radix pass, per record.** In each counting-sort pass, a record contributes to
the count loop and to the scatter loop. The count step reads the digest, forms
the digit by one shift and one mask, and increments one count word: with the
eight-operation allowance and address arithmetic this is at most 64 charged
operations. The scatter step reforms the digit, loads and writes back the bucket
cursor, and copies three words (three loads, three stores): at most 128 charged
operations including address arithmetic, bounds tests and loop control. A pass
therefore charges at most 192 operations per record for the two record-indexed
loops, which we round up to **512 per record per pass** to absorb all spills,
instruction fetches and loop bookkeeping. With two passes this is at most 1024
ordinary operations per record over the whole sort.

**Count-array handling.** Zeroing the count array and computing its exclusive
prefix sums touch R = 2^128 words per pass. Allow 16 charged operations per
count word (two loop iterations, each a load, an add, a store, address and
control, inside the eight-operation allowance): at most 16*2^128 operations per
pass, i.e. at most 2^133 operations for the two passes, charged as a fixed cost
independent of q. Because q = 2^129, this fixed count-array cost equals at most
2^133 = 16q ordinary operations, which section 5.3 folds into the per-record
envelope with ample slack.

**Scan.** Each scan position needs at most 64 core operations (six field loads,
bounded address calculations, equality tests, branches and index updates). Its
cap of 2048 charged operations per record includes copying a prospective output
pair.

**Final verification.** Final verification happens at most once; two hashes
through the same wrapper, full digest/message comparisons and output stores cost
less than 8192 ordinary operations, plus four compression calls. The possible
final FAIL path is within the same cap.

### 5.2 Code, setup, peak storage, and address width

All large loops are bounded loops, not unrolled code. The fixed program can be
laid out in fewer than 4096 instruction slots, each allowed four full 256-bit
words for opcode and operands, allocating 2^19 bytes for code. The radix count
and scatter bodies use at most a few hundred core-instruction slots; the wrapper
200, scan 64, and initialization, loop shells and final checks fit in the
remaining slots. Each such instruction includes its operand addresses in its
at-most-four-word encoding; instruction fetch and operand access are charged in
the execution budgets above, rather than assumed free. No compiler, runtime,
big-integer library, allocator or operating system is used by the RAM algorithm.

Allocate at most 4096 additional words (2^17 bytes) for IV, all 32 constants
even if internal to the primitive, message/padding buffers, unpacked block
words, eight-word input/output states, indices, saved records, counters and
output. These listed objects require fewer than 256 words; the larger cap covers
all spills and even unused schedule positions. A loader may read/write every
code/constant word, initialize all fixed scratch, and establish array base
addresses in fewer than 2^20 ordinary operations. The declared
`preprocessing_log2: 20` remains a conservative bound in target-compression
units: the actual setup costs less than 2^20/2224. Setup is included in total
time. No message-dependent setup, precomputed search or stored collision is
omitted.

The two record arrays occupy exactly 6q words = 192q bytes. The count array of
each pass holds R = 2^128 words = 2^133 bytes and is reused across the two
passes. Large arrays are not assumed zero: generation fills A, each scatter pass
fills its entire destination before any read from it, and every count pass
explicitly zeroes its R words first. Fixed code, constants and scratch occupy
less than 2^20 bytes together. Randomness is retained only in the message fields
and constant-size copies; there is no stored random tape. Thus peak memory on
every execution is

    M <= 192q + 2^133 + 2^20 < 512q = 2^138 bytes,

since 2^133 = 16q < 320q. This proves `memory_log2_bytes: 138`. All indices,
byte/word addresses and counter bounds are below 2^138, far below 2^256, so
address and counter arithmetic never wraps. D and N are proof notation, not RAM
operands; the algorithm stores q, which fits in one word and can be formed by a
shift.

### 5.3 Total time and auxiliary claim fields

Including setup, all trials, both radix passes, the count-array handling,
scanning and verification, the following separates compression calls from every
other charged operation:

| Phase | Compression calls, at cost 1 each | Ordinary operations, at cost 1/2224 each |
| --- | ---: | ---: |
| Fixed setup | 0 | 2^20 |
| Generate all q records | 2q | 2048q |
| Two radix passes (record-indexed loops) | 0 | 1024q |
| Two radix passes (count-array zero + prefix) | 0 | 2^133 |
| Scan | 0 | 2048q |
| Final verification and output | at most 4 | 8192 |

Thus H_calls <= 2q+4 and, using 2^133 = 16q,

    W <= (2048 + 1024 + 16 + 2048)q + 2^20 + 8192 = 5136q + 1056768.

With C = 2224, v5 gives

    T = H_calls + W/2224
      <= (2 + 5136/2224)q + 4 + 1056768/2224
       = (2 + 2.309353) q + (small)
       < 4.32 q
       < 2^2.111 * 2^129 = 2^131.111  for q = 2^129.

The declared `time_log2: 131.6` is a conservative upper bound on this value with
more than 0.48 bits of slack; the reconstructed bound above is strictly below
2^131.12. 2 + 5136/2224 is approximately 4.309 = 2^2.1075; 4.32 < 2^2.111, and
2^2.111 * 2^129 = 2^131.111 < 2^131.6. The dominant former cost — a
`log2(q)`-pass comparison merge sort charging about 129*2048q operations — is
replaced by the constant two-pass radix cost, which is what lowers the scalar.
All setup is inside T. This reconstructs the phase counts, rather than dividing
the old rounded scalar by C or discounting hash calls.

`nonuniform_advice_log2_bytes: 0` is a one-byte upper bound, as required by the
nonnegative logarithmic schema. Actual nonuniform advice is zero bytes. Public
fixed code, IV and SHA-256 constants are uniform specification data, but their
storage and initialization are still charged. No favorable seed, cached
collision, hidden preprocessing or target-dependent advice is supplied.

## 6. Evidence, scope, and limitations

The heuristic list is empty because sections 1-5 derive correctness, probability
and resources from the explicit target and model primitives. Fresh independent
random words are part of the organizer's model, not an empirical claim about a
short seeded program. No ideal SHA-256 behavior is required. The radix sort is a
textbook deterministic algorithm; its correctness does not depend on any
distribution of the digests, only on stability of the per-digit counting sort.

The certificate manifest is valid and empty. There is no experiment manifest or
executable candidate source. A finite toy experiment adds no premise to the
all-distributions lemma and cannot establish this full-scale execution's success
or cost. All necessary analytic evidence is included here, without external-link
dependence or participant-code execution. This is an astronomically expensive
theoretical RAM construction, not a measured run, practical attack, or new
SHA-256 security result. Any eventual selected-lane AI qualification remains
distinct from mathematical proof or human acceptance.

## 7. Source and accounting revision

This is an accounting revision of the organizer's conservative SHA-256 r31
baseline package that declared 136 under v5 with a comparison merge sort. Its
complete-hash definition, three-word records, distribution-free probability
proof, success lower bound and memory bound are retained verbatim. The single
change is the collision-detection step: a two-pass least-significant-digit radix
(counting) sort on the 256-bit digest replaces the `log2(q)`-pass merge sort,
removing the dominant `log2(q)` factor from the ordinary-operation ledger. The
count arrays are fully charged in both the time and memory ledgers; memory is a
reported metric only and does not affect the scalar. This is a new package
requiring fresh ordinary review, not a replay of an earlier qualification or a
new cryptanalytic algorithm.
