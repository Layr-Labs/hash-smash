# SHA-256, 31 prefix rounds: unconditional collision construction

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains
a separately reported resource bound.

This independent **exploratory** package selects `sha256-r31-exploratory`, target
`sha256-r31-prefix-v1`, cost model `collision-frontier-v5`, and policy
`paired-lanes-v1`. It submits a complete analytic algorithm, not an already
computed collision. Readiness requests review; it does not assert an AI outcome
or human acceptance. The full argument also addresses the rigorous review obligations.

The algorithm uses a large birthday table with a distribution-free proof for
this fixed hash. No ideal-hash, random-oracle, differential, round-independence,
or experimental-extrapolation premise is used. The required `baseline_improved`
value `sha256-r31-nominal-v2` only identifies the organizer's nominal display
reference; it is not an established attack, qualified baseline, or security
bound. This package does not claim improvement over that reference. Its declared
scalar is 130.18, with all bounds explained below.

## 1. Exact message and complete-hash definition

Write BE_k(v) for the k-byte big-endian encoding of integer v. Set q = 2^128,
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
chaining words. The result is the next block's incoming state; do not reset the
IV between blocks. After block 1 concatenate BE_4 of all eight state words in
standard order. This 32-byte output is H(m); interpret it as one 256-bit integer
d in the same big-endian order. Equality of d is equality of the full digest.

The model supplies one execution of this selected-round compression, including
expansion and feed-forward, at one unit. H uses two such units. Its message
handling and state/byte serialization are charged separately below; the internal
31 rounds are not charged a second time. A wrapper can unpack a 256-bit word
into eight 32-bit words using shifts/masks and pack the final state by shifts/ORs.
These interface operations are included even if the compression primitive
already accepts packed blocks and states.

## 2. Concrete RAM algorithm and stopping rule

Every RAM word is 256 bits (32 bytes). Draw precisely 2q fresh words through the
model's independent uniform random-word primitive, two per message. There is no
finite seed, deterministic PRNG expansion, or precomputed advice.

A record is exactly three words (digest,x,y); the last two retain the original
message. There are no object headers, per-record pointers, or hidden storage.
Arrays A and B each contain q contiguous records. Record i has word address
base+(i+i+i): multiplication is not an assumed primitive. A separate array of
q words holds radix counts and offsets. All counters, code, constants and
scratch occupy the fixed separate space charged in section 5.

1. Initialize the fixed program state. For i = 0,...,q-1 draw independent uniform
   words x,y, compute H(m(x,y)) using the fixed IV and both padded blocks, and
   store (H(m(x,y)),x,y) in A[i]. Generate the entire table on every execution.
2. Sort by the digest using two stable least-significant-digit radix passes with
   128-bit digits: first the low digest half, then the high digest half. A pass
   uses `digit=(digest >> shift) AND (2^128-1)` with shift zero or 128. It first zeros all count words,
   counts the q input digits, replaces counts by exclusive prefix offsets, and
   scans the input in increasing index order. Each record is written to the
   position in its digit's offset word, after which that offset is incremented.
   Swap the input/output bases after every pass. There is no hash table,
   recursion, comparison sort, node allocation, or unbounded key operation.
3. Scan the digest-sorted array while retaining the first record of the current
   equal-digest group. If a later record in that group differs in x or y, copy
   the two messages into the fixed output buffer. Recompute both complete H
   values from the fixed IV, check full equality and message inequality, and
   return the two original messages. Return FAIL if this final check fails
   (impossible in the specified exact RAM) or the scan ends without a pair.
   There are no restarts or other amplification.

Each radix scatter is stable because records are read in increasing input order
and each digit's offset is incremented after use. The first pass sorts by the
low half. Stability of the second pass preserves that ordering within each high
half, so the result is sorted by the complete 256-bit digest. Every pass writes
all q destination records before that array becomes a source, so neither large
array needs a hidden clearing pass. The two passes leave the final result in A.

All records sharing a digest are contiguous. Comparing every member of a group
with its first record finds a distinct message whenever the group contains one;
repeated copies of only one message never count. Thus the scan finds an ordinary
collision whenever one exists among the samples. A returned pair is always
distinct and has identical complete target hashes, confirmed by recomputation.
FAIL has no claimed output relation.

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

For our parameters

    a = q(q-1)/(2N) = 1/2 - 2^-129 > 499/1000,
    q(q-1)/(2D) = 2^-257 - 2^-385 < 2^-257 < 1/1000.

The positive Taylor terms give

    exp(499/1000)
      > 1 + 499/1000 + (499/1000)^2/2 + (499/1000)^3/6
      = 9865254499/6000000000
      > 1000/609.

Therefore exp(-a)<609/1000, and

    Pr(success) > 1 - 609/1000 - 1/1000 = 0.39.

`success_probability: 0.39` is a lower bound on
algorithmic success under its fresh coins, not equality with actual success,
confidence in this proof, or confidence in an AI review. The entire q-sample
construction and every sorting pass are paid on failed runs too. There are no
restarts to account for beyond the single fully charged execution.

## 5. Auditable resource implementation

These are worst-case bounds for every random tape in the specified classical
256-bit word RAM. Each selected compression costs one unit. Every other word
load, store, arithmetic/Boolean operation, shift, comparison, branch, and random
word costs 1/2140 target-compression units. In the instruction budgets below,
ordinary-operation counts are unpriced counts W, not target-compression units.
Compression calls are counted separately as H_calls; their expansion and round
internals are not included in W. Constants and bytes are retained below.

### 5.1 Instruction and interface budgets

A core scalar operation (two-operand arithmetic/comparison, assignment, branch,
or load/store) can be implemented with at most eight charged operations even
when scalar operands/results live in scratch: up to four instruction-word
fetches, two operand loads, the operation, and a result store. Thus instruction
fetches are charged explicitly as well. Constants fit that allowance. Address calculation is itself counted as
core work; base+3*i uses three additions. A record copy uses three addressed
loads and three addressed stores. Loops, branches and addressing are not free.

Across the counting and scatter scans of one radix pass, the following padded
bounds cover one input record:

| Work per record per radix pass | Maximum core operations |
| --- | ---: |
| Both loop tests, branches and index updates | 12 |
| Source, destination and bucket address calculations | 14 |
| Two digit extractions and bucket load/update/store operations | 14 |
| Load and copy the three-word record | 8 |
| Base/shift access, scalar assignments and scratch bookkeeping | 16 |
| Total | 64 |

There is no recursion, variable-length comparison, or node allocation. Operand
reloads/spills fit the eight-operation allowance. Zeroing and prefixing one
bucket consume at most 16 core operations together, including both loop
shells; pass setup, base swaps, shift updates and exits consume fewer than 128
more. After applying the eight-operation core allowance, one complete radix
pass therefore costs at most

    512q + 128q + 1024 = 640q + 2^10

ordinary operations. Both passes cost at most `1280q + 2^11` ordinary
operations.

The generation wrapper uses at most 200 ordinary core operations per message,
plus two random-word instructions and dispatch of two compression calls. A
direct wrapper uses at most 32 shifts/masks to unpack the first block, 24 shifts/ORs to pack the final
digest, and 144 further operations for IV/state copies, access to the already
initialized padding block, record addressing/stores and loop control. Transfers
of primitive input/output state and scalar scratch are covered by the eight-operation
allowance. Fetching and dispatching the two random-word instructions and two
compression calls can each be allowed eight operations. This is at most
8*200+8*4<2048 ordinary operations per sampled message. The two compression
calls themselves cost two additional target-compression units. Random draws,
call dispatch, operand transfer and instruction fetches remain inside W.
The second block is a fixed scratch constant; a packed-block interface costs
no more. Expansion and 31 rounds are inside each compression's unit cost.

Each scan position needs at most 64 core operations (six field loads, bounded
address calculations, equality tests, branches and index updates). Its cap of
2048 charged operations includes copying a prospective output pair. Final
verification happens at most once; two hashes through the same wrapper, full
digest/message comparisons and output stores cost less than 8192 ordinary
operations, plus four compression calls.
The possible final FAIL path is within the same cap.

### 5.2 Code, setup, peak storage, and address width

All large loops are bounded loops, not unrolled code. The fixed program can be
laid out in fewer than 4096 instruction slots, each allowed four full 256-bit
words for opcode and operands, allocating 2^19 bytes for code. The radix loops
use at most 192 core-instruction slots, the wrapper 200, scan 64, and
initialization, loop shells and final checks fit in the remaining 3640 slots.
Each such instruction includes its operand addresses in its at-most-four-word
encoding; instruction fetch and operand access are charged in the execution
budgets above, rather than assumed free. No compiler,
runtime, big-integer library, allocator or operating system is used by the RAM
algorithm. The full compression specification fixes its supplied primitive;
its internals need not be implemented a second time in the attack program.

Allocate q words (32q bytes) for radix counts/offsets and at most 4096
additional words (2^17 bytes) for IV, all 31 constants even if internal to the
primitive, message/padding buffers, unpacked block words, eight-word
input/output states, indices, saved records, counters and output. The latter
objects require fewer than 256 words; the larger cap covers all spills and even
unused schedule positions. Radix counts are zeroed inside every charged pass.
A loader may read/write every code/constant word, initialize all fixed scratch,
and establish array base addresses in fewer than 2^20 ordinary operations. The declared
`preprocessing_log2: 9` follows in target-compression units because the actual
setup costs less than 2^20/2140 < 2^9. Setup is included in total
time. No message-dependent
setup, precomputed search or stored collision is omitted.

The two arrays occupy exactly 6q words=192q bytes. Large arrays are not assumed
zero: generation fills A and each radix pass fills its entire destination
before any read from it. Outside the two record arrays, the radix array, fixed
code, constants and scratch occupy less than 32q+2^20 bytes together. Output
already fits scratch. Randomness is retained only
in the message fields and constant-size copies; there is no stored random tape.
Thus peak memory on every execution is

    M <= 224q + 2^20 < 256q = 2^136 bytes.

This proves `memory_log2_bytes: 136`. All indices, byte/word addresses and
counter bounds are below 2^136, far below 2^256, so address and counter
arithmetic never wraps. D and N are proof notation, not RAM operands; the
algorithm stores q, which fits in one word and can be formed by a shift.

### 5.3 Total time and auxiliary claim fields

Including setup, all trials, both radix passes, scanning and verification,
the following separates compression calls from every other charged operation:

| Phase | Compression calls, at cost 1 each | Ordinary operations, at cost 1/2140 each |
| --- | ---: | ---: |
| Fixed setup | 0 | 2^20 |
| Generate all q records | 2q | 2048q |
| Both radix passes | 0 | 1280q + 2^11 |
| Scan | 0 | 2048q |
| Final verification and output | at most 4 | 8192 |

Thus H_calls <= 2q+4 and

    W <= 5376q + 2^20 + 2^13 + 2^11.

These ordinary caps retain spare allowance from the explicit instruction
budgets; they do not count the compression internals. With C=2140, v5 gives

    T = H_calls + W/2140
      <= (2 + 5376/2140)q
         + 4 + (2^20 + 2^13 + 2^11)/2140
       < 2^2.18 q = 2^130.18,  for q=2^128.

The coefficient is exactly 2414/535 < 4.513, the constant term is less than
2^9, and 4.513 + 2^-119 < 2^2.18. This proves the submitted
`time_log2: 130.18`. All setup is inside T. This reconstructs the phase counts,
rather than dividing the old rounded scalar by C or discounting hash calls.

To fix units for the otherwise untyped data field, `data_log2: 136` bounds
**bytes of complete padded input presented to hashing**, including final
verification. At most q+2 complete 64-byte messages are evaluated and 2q+4
compression calls process 128(q+2) padded bytes, less than 256q=2^136 bytes.
Original message data is only 64(q+2) bytes. No external message corpus is
required. The same numeric cap also upper-bounds counts of messages,
compressions and random words. Sort copies are internal traffic, fully charged
in T, rather than acquired input data; all retained data is charged in M.

`nonuniform_advice_log2_bytes: 0` is a one-byte upper bound, as required by the
nonnegative logarithmic schema. Actual nonuniform advice is zero bytes. Public
fixed code, IV and SHA-256 constants are uniform specification data, but their
storage and initialization are still charged. No favorable seed, cached
collision, hidden preprocessing or target-dependent advice is supplied.

## 6. Evidence, scope, and limitations

The heuristic list is empty because sections 1-5 derive correctness,
probability and resources from the explicit target and model primitives. Fresh
independent random words are part of the organizer's model, not an empirical
claim about a short seeded program. No ideal SHA-256 behavior is required.

The certificate manifest is valid and empty. There is no experiment manifest
or executable candidate source. A finite toy experiment adds no premise to
the all-distributions lemma and cannot establish this full-scale execution's
success or cost. All necessary analytic evidence is included here, without
external-link dependence or participant-code execution. This is an
astronomically expensive theoretical RAM construction, not a measured run,
practical attack, or new SHA-256 security result. Any eventual selected-lane AI
qualification remains distinct from mathematical proof or human acceptance.

## 7. Source and accounting revision

This is an algorithmic accounting revision of the organizer's SHA-256 r31 package
`35a8a47f2601b035331d7db4b6275f5c36b1d1be00e379f5e58d54e5328696a8`
in production base `0455d2b52f4f920fe5c3a6af8c71592a824e6a57`.
Its complete-hash definition, three-word records and distribution-free
probability lemma are retained. This revision uses the smallest power-of-two
sample count meeting the 0.39 threshold and replaces comparison sorting by two
stable 128-bit radix passes. The resulting unconditional v5 bound is 130.18 rather
than 136. This is a new package requiring fresh ordinary review, not a replay
of an earlier qualification or a new differential cryptanalytic algorithm.
