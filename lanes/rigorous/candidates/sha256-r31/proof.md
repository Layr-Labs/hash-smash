# SHA-256, 31 prefix rounds: unconditional collision construction

This independent **rigorous** package selects `sha256-r31-rigorous`, target
`sha256-r31-prefix-v1`, cost model `collision-frontier-v3`, and policy
`paired-lanes-v1`. It submits a complete analytic algorithm, not an already
computed collision. Readiness requests review; it does not assert an AI outcome
or human acceptance. The same mathematical obligations support exploratory review.

The algorithm uses a large birthday table with a distribution-free proof for
this fixed hash. No ideal-hash, random-oracle, differential, round-independence,
or experimental-extrapolation premise is used. The required `baseline_improved`
value `sha256-r31-nominal-v2` only identifies the organizer's nominal display
reference; it is not an established attack, qualified baseline, or security
bound. This package does not claim improvement over that reference. Its declared
scalar is 148 + 138 = 286, with all bounds explained below.

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
base+(i+i+i): multiplication is not an assumed primitive. All counters, code,
constants and scratch occupy the fixed separate space charged in section 5.

1. Initialize the fixed program state. For i = 0,...,q-1 draw independent uniform
   words x,y, compute H(m(x,y)) using the fixed IV and both padded blocks, and
   store (H(m(x,y)),x,y) in A[i]. Generate the entire table on every execution.
2. Sort triples lexicographically by (digest,x,y) using the bottom-up merge sort
   below. `lex_le` compares at most three pairs of unsigned 256-bit fields and
   returns true on equality. No hash table or unbounded-string comparison is used.
3. Scan the sorted array from index 1 to q-1, comparing each record with its
   predecessor. At the first equal digest with either message word different,
   copy both messages into the fixed output buffer. Recompute both complete H
   values from the fixed IV, check full equality and message inequality, and
   return the two original messages. Return FAIL if this final check fails
   (impossible in the specified exact RAM) or the scan ends without a pair.
   There are no restarts or other amplification.

The merge procedure uses word-address bases L and R. All scalar assignments,
address calculations, loads, stores, comparisons and branches are charged.

    L = A; R = B; width = 1
    while width < q:
        start = 0
        while start < q:
            middle = start + width; end = middle + width
            i = start; j = middle; k = start
            while k < end:
                if i == middle: take = right
                else if j == end: take = left
                else if lex_le(L[i], L[j]): take = left
                else: take = right
                if take == left:
                    R[k] = L[i]; i = i + 1
                else:
                    R[k] = L[j]; j = j + 1
                k = k + 1
            start = end
        swap L and R by exchanging their base-address words
        width = width + width

Since q is a power of two, all run lengths divide q and no middle/end index
exceeds q. Each pass writes its complete destination before that array becomes
a source. No uninitialized B record is read; large arrays need no hidden
clearing pass. Exactly 129 passes each emit q records. Inductively each pass
merges sorted runs into sorted runs twice as long. Starting with singleton
runs, the final L contains the same record multiset in sorted order.

All records sharing a digest are contiguous, and messages within such a group
are sorted. If a group contains two distinct messages there is an adjacent
unequal-message pair. Thus the scan finds an ordinary collision whenever one
exists among the samples. A returned pair is always distinct and has identical
complete target hashes, confirmed by recomputation. Repeated copies of a single
message never count as success. FAIL has no claimed output relation.

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
the declared decimal, exp(1)>1+1+1/2+1/6=8/3, so exp(-1)<3/8. Hence

    Pr(success) > 5/8 - 2^-255 > 3/5 = 0.60 > 0.39,

where 2^-255<1/40=5/8-3/5. `success_probability: 0.6` is a lower bound on
algorithmic success under its fresh coins, not equality with actual success,
confidence in this proof, or confidence in an AI review. The entire q-sample
construction and every sorting pass are paid on failed runs too. There are no
restarts to account for beyond the single fully charged execution.

## 5. Auditable resource implementation

These are worst-case bounds for every random tape in the specified classical
256-bit word RAM. Each selected compression costs one unit. Every other word
load, store, arithmetic/Boolean operation, shift, comparison, branch, and random
word costs one. Constants and bytes are retained in the bounds below.

### 5.1 Instruction and interface budgets

A core scalar operation (two-operand arithmetic/comparison, assignment, branch,
or load/store) can be implemented with at most eight charged operations even
when scalar operands/results live in scratch: up to four instruction-word
fetches, two operand loads, the operation, and a result store. Thus instruction
fetches are charged explicitly as well. Constants fit that allowance. Address calculation is itself counted as
core work; base+3*i uses three additions. A record copy uses three addressed
loads and three addressed stores. Loops, branches and addressing are not free.

The following deliberately padded bounds cover a single merge emission,
including potential work on both branch paths even though only one runs:

| Work per emitted record | Maximum core operations |
| --- | ---: |
| Output-loop and source-bound tests and branches | 12 |
| Two source addresses, destination address, and field offsets | 18 |
| Load both triples and write the selected triple, including copies | 18 |
| Lexicographic comparisons of three fields, with branches | 18 |
| Source selection, index increments, and loop-back branch | 18 |
| Other scalar assignments and fixed scratch bookkeeping | 24 |
| Total, rounded upward | 128 |

There is no recursion, variable-length comparison, or node allocation. Operand
reloads/spills fit the eight-operation allowance. Each run's initialization,
end handling and start update consume at most 64 more core operations; there
are q/(2*width)<=q/2 runs per pass. Pass tests, base swaps, width updates and
exit cost at most 64 more core operations per pass. Even charging the final
exit again, the pass cost is at most

    8*(128q + 64(q/2) + 64) <= 2048q.

The generation wrapper uses at most 200 core operations per message, plus two
random-word instructions and two compression calls. A direct wrapper uses at
most 32 shifts/masks to unpack the first block, 24 shifts/ORs to pack the final
digest, and 144 further operations for IV/state copies, access to the already
initialized padding block, record addressing/stores and loop control. Transfers
of primitive input/output state and scalar scratch are covered by the eight-operation
allowance. Fetching and dispatching the two random-word instructions and two
compression calls can each be allowed eight operations. This is at most
8*200+8*4<2048 charged operations per sampled message.
The second block is a fixed scratch constant; a packed-block interface costs
no more. Expansion and 31 rounds are inside each compression's unit cost.

Each scan position needs at most 64 core operations (six field loads, bounded
address calculations, equality tests, branches and index updates). Its cap of
2048 charged operations includes copying a prospective output pair. Final
verification happens at most once; two hashes through the same wrapper, full
digest/message comparisons and output stores cost less than 8192 operations.
The possible final FAIL path is within the same cap.

### 5.2 Code, setup, peak storage, and address width

All large loops are bounded loops, not unrolled code. The fixed program can be
laid out in fewer than 4096 instruction slots, each allowed four full 256-bit
words for opcode and operands, allocating 2^19 bytes for code. The merge body
uses at most 128 core-instruction slots, the wrapper 200, scan 64, and
initialization, loop shells and final checks fit in the remaining 3704 slots.
Each such instruction includes its operand addresses in its at-most-four-word
encoding; instruction fetch and operand access are charged in the execution
budgets above, rather than assumed free. No compiler,
runtime, big-integer library, allocator or operating system is used by the RAM
algorithm. The full compression specification fixes its supplied primitive;
its internals need not be implemented a second time in the attack program.

Allocate at most 4096 additional words (2^17 bytes) for IV, all 31 constants
even if internal to the primitive, message/padding buffers, unpacked block
words, eight-word input/output states, indices, saved records, counters and
output. These listed objects require fewer than 256 words; the larger cap
covers all spills and even unused schedule positions. A loader may read/write
every code/constant word, initialize all fixed scratch, and establish array
base addresses in fewer than 2^20 charged instructions. This is the declared
`preprocessing_log2: 20`, also included in total time. No message-dependent
setup, precomputed search or stored collision is omitted.

The two arrays occupy exactly 6q words=192q bytes. Large arrays are not assumed
zero: generation fills A and each merge pass fills its entire destination
before any read from it. Fixed code, constants and scratch occupy less than
2^20 bytes together. Output already fits scratch. Randomness is retained only
in the message fields and constant-size copies; there is no stored random tape.
Thus peak memory on every execution is

    M <= 192q + 2^20 < 512q = 2^138 bytes.

This proves `memory_log2_bytes: 138`. All indices, byte/word addresses and
counter bounds are below 2^138, far below 2^256, so address and counter
arithmetic never wraps. D and N are proof notation, not RAM operands; the
algorithm stores q, which fits in one word and can be formed by a shift.

### 5.3 Total time and auxiliary claim fields

Including setup, all trials, all 129 merge passes, scanning and verification,

    T <= 2^20 + 2048q + 129*2048q + 2048q + 8192
       = 2^20 + 131*2048q + 8192
       < 2^19*q = 2^148 charged units.

This proves `time_log2: 148` in the model's `target-compressions` unit, which
also charges every ordinary primitive operation. The submitted upper bounds
rather than the sharper internal ledger define scalar 286. Setup is inside T.

To fix units for the otherwise untyped data field, `data_log2: 137` bounds
**bytes of complete padded input presented to hashing**, including final
verification. At most q+2 complete 64-byte messages are evaluated and 2q+4
compression calls process 128(q+2) padded bytes, less than 256q=2^137 bytes.
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
