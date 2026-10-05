# SHA-256, 32 prefix rounds: one-block birthday search with two radix passes

## 1. Scope and claim

This package selects `sha256-r32-exploratory`, target
`sha256-r32-prefix-v1`, cost model `collision-frontier-v5`, and review policy
`paired-lanes-v1`. The submitted scalar is `time_log2: 129.724`, an upper bound
on total charged computation in selected-target compression equivalents. Peak
memory is bounded by `2^136` bytes. This is an analytic classical RAM algorithm,
not an executed search or a supplied collision.

The construction replaces the checkout's two-block messages and 129-pass merge
sort with one-block complete messages and two stable 128-bit radix passes. All
large count-array initialization and prefix-sum work is paid. It uses no
ideal-hash premise, random oracle, cryptanalytic differential, experimental
extrapolation, nonuniform advice, or short-seed expansion.

The required `baseline_improved: sha256-r32-nominal-v2` is a nominal-reference
identifier, not an assertion that the exponent 128 is an executable, accepted,
or improved baseline. The scalar here is greater than 128. Readiness requests
review; it does not assert qualification, mathematical verification, human
acceptance, or promotion.

## 2. Messages and the exact complete hash

Let R = 2^128, q = R+1, N = 2^256, and D = 2^440. BE_k(v) denotes the
k-byte big-endian representation of v. Independently sample x uniformly from
[0,2^256) and y uniformly from [0,2^184), and define

    m(x,y) = BE_32(x) || BE_23(y).

These D distinct messages have exactly 55 bytes and bit length 440 < 2^64.
Sampling uses two fresh independent uniform 256-bit word primitives per message;
the second draw is masked with 2^184-1 to obtain y. Every y has exactly 2^72
preimages under this mask, so the resulting message is exactly uniform over D.
Each pair of draws is independent of every other pair. No duplicate-rejection
loop, seeded PRNG, or uncharged random source is used.

FIPS 180-4 padding yields exactly one 64-byte block:

    BE_32(x) || BE_23(y) || 0x80 || BE_8(440).

In two packed 256-bit words this block is

    (x, (y << 72) OR (0x80 << 64) OR 440).

The three fields in the second word occupy disjoint bits. This is padding of the
original 55-byte message, not a pre-padded message supplied as original input.
There is no second block. Initialize once with the fixed standard IV, in order:

    6a09e667 bb67ae85 3c6ef372 a54ff53a
    510e527f 9b05688c 1f83d9ab 5be0cd19

Parse the padded block into sixteen big-endian 32-bit words W[0],...,W[15].
Execute the following standard SHA-256 schedule and round formulas at precisely
indices t = 0,...,31. All additions are modulo 2^32, and rotations and NOT
operate on 32-bit words:

    s0(z) = ROTR32(z,7) XOR ROTR32(z,18) XOR (z >> 3)
    s1(z) = ROTR32(z,17) XOR ROTR32(z,19) XOR (z >> 10)
    S0(z) = ROTR32(z,2) XOR ROTR32(z,13) XOR ROTR32(z,22)
    S1(z) = ROTR32(z,6) XOR ROTR32(z,11) XOR ROTR32(z,25)
    Ch(e,f,g) = (e AND f) XOR ((NOT e) AND g)
    Maj(a,b,c) = (a AND b) XOR (a AND c) XOR (b AND c)
    W[t] = W[t-16] + s0(W[t-15]) + W[t-7] + s1(W[t-2]), t=16,...,31
    T1 = h + S1(e) + Ch(e,f,g) + K[t] + W[t]
    T2 = S0(a) + Maj(a,b,c)
    (a,b,c,d,e,f,g,h) = (T1+T2, a, b, c, d+T1, e, f, g)

The constants are the original K[0] through K[31], without renumbering:

    428a2f98 71374491 b5c0fbcf e9b5dba5 3956c25b 59f111f1 923f82a4 ab1c5ed5
    d807aa98 12835b01 243185be 550c7dc3 72be5d74 80deb1fe 9bdc06a7 c19bf174
    e49b69c1 efbe4786 0fc19dc6 240ca1cc 2de92c6f 4a7484aa 5cb0a9dc 76f988da
    983e5152 a831c66d b00327c8 bf597fc7 c6e00bf3 d5a79147 06ca6351 14292967

Start (a,b,c,d,e,f,g,h) at the IV. After round 31, add all eight final working
words to the corresponding IV words modulo 2^32. Concatenate their BE_4 encodings
in standard order. Call this complete 32-byte hash H(m) and its unsigned
big-endian 256-bit value d. Full equality of d is equality of all output words.
The selected compression primitive includes message expansion, the 32 rounds,
and full feed-forward and costs one unit. Interface work is charged separately;
compression internals are not also charged as word operations.

## 3. Explicit RAM algorithm

Each RAM word contains 256 bits. Each record contains exactly three words
(d,x,y). Allocate two arrays A and B, each holding q records, and a count array C
holding R words. A record's address is base+(i+i+i), not an assumed free multiply.
All field offsets, pointer arithmetic, loads, stores, comparisons, branches,
and counter updates are charged in section 6. Arrays have no object headers,
per-record pointers, runtime, or allocator. Fixed scratch and code are separately
bounded. Contiguous uninitialized storage is permitted, but no read of
uninitialized data occurs; this algorithm explicitly writes every used entry.

First generate all q independent messages, compute each complete one-block H,
and fill A with (d,x,y). Do not stop early or reuse a table from another run.
Next sort by all 256 bits of d using the following stable LSD radix pass, first
with shift s=0 and then s=128. The radix mask is R-1.

    L = A; U = B
    for s in [0,128]:
        for r = 0,...,R-1:
            C[r] = 0
        for i = 0,...,q-1:
            r = (L[i].d >> s) AND (R-1)
            C[r] = C[r] + 1
        total = 0
        for r = 0,...,R-1:
            count = C[r]
            C[r] = total
            total = total + count
        for i = 0,...,q-1:
            r = (L[i].d >> s) AND (R-1)
            j = C[r]
            U[j] = L[i]              # copy all three fields
            C[r] = j + 1
        swap L and U

The prefix sum equals q. For each digit, its positions occupy a disjoint interval
of length equal to its frequency. Scattering fills that interval in source order,
so each pass is stable and is a permutation of the records. Every destination
position is written exactly once before that destination becomes a source.
Resetting C on both passes is explicitly paid. Stable sorting first by the low
128 bits and then by the high 128 bits sorts by the complete unsigned digest.

Finally scan adjacent records in L. For an equal digest and an unequal message
(i.e. x differs or y differs), copy the two original messages into fixed scratch,
recompute their complete hashes independently from the fixed IV, and check
message inequality and full hash equality. Return the two 55-byte originals only
if these checks pass; otherwise return FAIL. If no adjacent pair qualifies,
return FAIL. There are no restarts. At most one prospective pair is rehashed.

All records having the same digest are contiguous. Although messages within
such a group need not be sorted, a group with at least two distinct messages
must have some adjacent unequal messages: otherwise transitivity of adjacent
message equality would make the entire group identical. Thus the scan detects
any distinct-message collision present among the samples. The final check
cannot fail in the specified exact RAM, and a returned result is always an
ordinary collision for the exact complete target. Repeated copies of the same
message alone never count as success.

## 4. Distribution-free probability argument

For each of the N possible digest values z, let p_z be the fraction of our D
allowed messages whose fixed deterministic H equals z. Retain zero coordinates.
The independently sampled input messages induce independent output samples
from p; no assertion that p is uniform is needed.

Let e_q(p) be the sum of products over all q-element coordinate subsets. The
probability of all q sampled outputs differing is q! e_q(p). To bound e_q, choose
a maximizer on the compact probability simplex, and among all maximizers choose
one minimizing the sum of squared coordinates. Both choices exist. If two
coordinates a,b differ, and the other coordinates form vector v, then

    e_q(p) = e_q(v) + (a+b)e_(q-1)(v) + ab e_(q-2)(v).

Here e_0=1, and e_j=0 for an impossible subset size. All coefficients are
nonnegative. Averaging a,b preserves their sum and increases their product, so
cannot decrease e_q. It remains a maximizer, but strictly decreases the sum of
squared coordinates, a contradiction. Hence a maximizing vector is uniform and
for every fixed H,

    Pr(no repeated digest) <= q! binomial(N,q) / N^q
       = product_(j=0)^(q-1) (1-j/N)
       <= exp(-q(q-1)/(2N)).

This uses 2 <= q <= N and 1-u <= exp(-u). It does not assume independent
collision events or any random-function property of SHA-256.

## 5. Success threshold and distinct messages

Let E be the event of a repeated sampled digest, and F the event of any repeated
original input message. On E minus F the scan certainly returns a distinct
collision. For each pair of sample positions, input equality has probability
1/D, so a union bound gives

    Pr(success) >= 1 - exp(-q(q-1)/(2N)) - q(q-1)/(2D).

For R=2^128 and q=R+1,

    q(q-1)/(2N) = 1/2 + 2^-129 > 1/2,
    q(q-1)/(2D) = 2^-185 + 2^-313 < 2^-184.

An elementary rational lower bound certifies the threshold, without dependence
on a rounded numerical exponential:

    exp(1/2) > 1 + 1/2 + 1/8 + 1/48 + 1/384 = 211/128.

Therefore Pr(success) > 83/211 - 2^-184. Since
83/211 - 39/100 = 71/21100 > 2^-184, the success probability is strictly greater
than 0.39. The claim reports the conservative lower bound 0.39, not a measured
frequency or confidence in an AI reviewer. The entire sampling, sorting, and
scan budgets are paid on failing random tapes too. Verification at most once
is also included in the worst-case cost. There is no hidden success amplification.

## 6. Charged implementation and time

### 6.1 Core instructions and their expansion

Use a uniform, bounded-loop RAM program, not an unrolled table of instructions.
A core scalar instruction (assignment, binary operation, comparison, conditional
branch, addressed load, or addressed store) is implemented by at most eight
priced ordinary operations: up to four instruction-word fetches, two operand
loads, the primitive operation, and one result store. No multiple-operation
expression is counted as one instruction. Address arithmetic is separate core
work. Array loads/stores are themselves core instructions; their data accesses
and scratch spills fit this same allowance. Core comparison and subsequent
branch are separate instructions. A record address uses three additions; three
field addresses, three field loads, and three field stores are explicitly budgeted.

Loop bounds and index increments use ordinary arithmetic. Every counter and
address fits 256 bits (section 7), so no multiprecision primitive is required.
All public constants are in fixed scratch or fixed instructions with their
loading paid. Assignment overhead, instruction fetches, random-word dispatch,
and compression-interface dispatch are not treated as free.

### 6.2 Sampling and complete-hash wrapper

Per sample allow 200 core instructions for: masking y; constructing the second
packed block word; unpacking the two 256-bit words into sixteen 32-bit words
(at most 32 shifts/masks); copying the eight IV words and bounded input/output
scratch; packing the final digest (at most 16 shifts/ORs); record addressing and
three stores; loop tests, branches, and updates; and additional scratch copies.
The total leaves over 100 instructions for the bounded copies, addressing, and
control after the listed bit operations. The wrapper is the same on every
message; no general string library or arbitrary-length serialization is needed.
The final byte output may be written using fixed shifts/masks in the verification
budget. Fixed masks and the padding/length constants are loaded during setup.

In addition allow eight ordinary operations for each of two random-word
dispatches and one selected compression dispatch. Thus ordinary work per sampled
record is at most 8*200+8*3=1624 < 2048, plus exactly one separately priced
selected compression. Internal expansion, round operations, and feed-forward
are inside that compression price, not this ordinary-work cap.

### 6.3 Radix passes

The following padded core-instruction counts include full address arithmetic,
loop tests/branches/increments, assignments, loads, stores, and scratch handling:

| Phase in one pass | Core bound | Included work |
| --- | ---: | --- |
| Clear C | 8R | address, zero store, test, branch, increment, loop back |
| Histogram source | 24q | source address and digest load, two digit operations, count address/load/add/store, loop control |
| Prefix sums | 16R | count address/load, write start, add to total, assignments, loop control |
| Stable scatter | 64q | source and destination record addresses/field offsets, digit extraction, count access/update, three field loads and stores, loop control and scratch copies |
| Pass setup and exits | 64 | loop initialization/final tests, selecting shift, pointer swap |

These caps bound even degenerate digit distributions; no expected bucket length
assumption is used. Each output record is copied once and each count entry is
cleared and prefix-summed once. The displayed pseudocode requires fewer than the
allowed instructions in every row. With R=q-1 the sum is

    8R + 24q + 16R + 64q + 64 = 112q + 40 <= 128q.

After expansion by the eight-operation allowance, each pass costs at most
1024q ordinary operations. Both passes together cost at most 2048q. Sorting
never incurs a target compression.

### 6.4 Scan and final verification

Allow 128 core instructions per scan position, including adjacent-record address
formation, all six field loads, full digest and two message-field comparisons,
branches, loop updates, and copying a prospective pair. This is at most 1024q
ordinary operations for the entire scan, including its loop exits. The simple
adjacent scan uses fewer than 64 core instructions per position, leaving slack
for final loop handling and candidate copies.

Two final complete hashes consume at most two further selected compressions.
Their ordinary wrappers, full comparisons, fixed byte serialization and output
stores, and the final return/FAIL path fit within 8192 ordinary operations.
Nothing requires recomputing all hashes during sorting or on every scan step.

### 6.5 Setup and total bound

The fixed program fits in 4096 core-instruction slots, with at most four 256-bit
words per slot: at most 2^19 bytes. It contains bounded loops, one fixed hash
wrapper, the four radix loops, scan, and verification. Allocate 4096 additional
256-bit words for all fixed scratch, constants, block/state arrays, masks,
counters, pointers, and output: 2^17 bytes. The explicitly listed objects need
far fewer words; the cap covers spills and unused schedule slots. Loading all
code/constants, initializing fixed scratch, and computing bases costs at most
2^20 ordinary operations, including loader accesses and loop control. This is
uniform specification data, not free nonuniform advice. Large-array writes are
already charged in generation and the two radix passes, not concealed in setup.

The total worst-case resource ledger is:

| Phase | Selected compression calls | Ordinary operations |
| --- | ---: | ---: |
| Fixed setup | 0 | 2^20 |
| Generate q records | q | 2048q |
| Two radix passes | 0 | 2048q |
| Scan | 0 | 1024q |
| Final verification/output | at most 2 | 8192 |

Thus H_calls <= q+2 and W <= 5120q+1056768. Under the actual SHA-256 r32
operation price 1/2224,

    T <= q+2 + (5120q+1056768)/2224
       = (459/139)(2^128+1) + 2 + 1056768/2224.

The coefficient 1+5120/2224 equals 459/139. Including the constants gives

    log2(T_bound) = 129.72340927069030052162554961953372924017580781444...
       < 129.724.

The declaration rounds upward with a margin greater than 0.00059 bits, rather
than treating an approximate downward value as an upper bound. The integer
counts and rational expression define the bound exactly. As an additional
simple check, 459/139 < 4 and the additive constants are negligible relative
to (4-459/139)2^128, so T_bound < 2^130. Preprocessing is inside T;
`preprocessing_log2: 20` is a conservative compression-unit upper bound on the
actual fixed setup cost 2^20/2224. All trials, failed runs, memory traffic,
randomness, sorting, recovery, instruction fetches, and verification are paid.
Total work is serial work, not a discounted parallel latency.

## 7. Memory, data, and advice

A and B together use 6q words = 192q bytes. C uses R words = 32R bytes. All
fixed code, scratch, constants, and output together use less than 2^20 bytes.
Randomness is retained only in the x,y record fields and fixed copies; there is
no separate stored random tape. Therefore on every random tape,

    M <= 192q + 32R + 2^20
       = 224*2^128 + 192 + 2^20 < 256*2^128 = 2^136 bytes.

This proves `memory_log2_bytes: 136`. Word and byte addresses are less than
2^136, all prefix counts are at most q, and all loop indices and shifts fit in
one 256-bit word. The largest word offset is less than 7*2^128+6. Address
arithmetic therefore never wraps. Choosing direct indexing by a 128-bit digit
does not presume an address space larger than the model permits. No sparse
zero-initialized virtual array or hidden dictionary is used.

`data_log2: 135` bounds bytes of complete padded input hashed, including
verification. At most q+2 complete messages are evaluated, each using one
64-byte padded block, so data is at most 64(q+2) = 64(2^128+3) < 2^135 bytes.
Original message bytes are at most 55(q+2). The same cap also bounds message,
compression, and random-word counts. Radix copies and count-table traffic are
internal work, charged in T and M, not acquired external input data.

Actual nonuniform advice is zero. The schema's required nonnegative
`nonuniform_advice_log2_bytes: 0` is the conventional one-byte upper bound,
not a claim that log2(0) is defined. No cached collision, favorable tape,
external message corpus, target-dependent precomputation, or advice string is
provided. Public uniform program and standard IV/constants are nevertheless
charged in storage and setup.

## 8. Evidence, provenance, and limitations

The heuristic list and certificate manifest are empty. No executable participant
source or experiment manifest is supplied. The probability guarantee and
worst-case costs are analytic for the explicit algorithm; a small experiment
would not establish a full-size SHA-256 collision or a 2^128-scale execution.
The trusted target reference remains `verifier/hash_functions.py:digest`.

The starting candidate is the organizer package at checkout
`8a0f02675cdcd58ebfc16119af02a094c3e1dd16`, with declared scalar 136. Its
all-distributions birthday argument is retained and stated completely here,
while the input domain, sample count, data structures, sorting, resource
accounting, and success declaration are changed. A declared inherited scalar
or nominal reference is not being used as evidence of accepted qualification.
This package requires new ordinary review bound to these changed inputs.

The memory is astronomically beyond physical machines, and the charged time
is likewise impractical. This is a generic upper bound, not a differential
advance, a practical break, or evidence of a weakened full-round SHA-256.
The large-radix tradeoff is permitted by the stated word-RAM and memory-only
reporting policy, but does not translate directly into feasible hardware.
Qualification remains an AI screening outcome, separate from mathematical proof,
manual acceptance, and successful publication/promotion.
