# SHA-256 r31: distribution-free one-block birthday search with wide radix sort

This package selects `sha256-r31-exploratory`, target
`sha256-r31-prefix-v1`, cost model `collision-frontier-v5`, and review policy
`paired-lanes-v1`. It specifies an analytic classical RAM construction, not a
computed collision or a practical attack. Its submitted total-time upper bound
is `time_log2: 129.953`; its separately reported peak storage bound is
`memory_log2_bytes: 136`. Its algorithmic success lower bound is 0.39.

The construction is distribution-free for the fixed selected hash. It requires
neither uniform SHA-256 outputs nor independence of collision events. Fresh
independent uniform random words are supplied by the organizer's computation
model, not by a short seed. No heuristic premises or experiments are declared.

The required `baseline_improved: sha256-r31-nominal-v2` identifies the nominal
reference only. A bound above 128 does not improve that nominal display value.
The comparison made here is to the initial candidate's declared 136, not to a
proved SHA-256 security bound, an independently verified baseline, or other
solvers' pending practical attacks. Readiness requests review, not acceptance.

## 1. Exact messages and complete selected hash

Let q = 2^128, N = 2^256, and D = 2^440. For each of exactly q samples draw two
fresh independent uniform 256-bit words x and s. Put y = s >> 72 and define

    m(x,y) = BE_32(x) || BE_23(y),  0 <= y < 2^184.

BE_k denotes fixed-width k-byte big-endian encoding. These are uniform independent
samples, with replacement, from the D distinct 55-byte messages. The discarded
72 bits do not bias y; each y has exactly 2^72 preimages under the shift. The
two retained words x,y identify the original message injectively.

Each message has bit length 440, below 2^64. Its complete FIPS 180-4 padded
block is exactly

    BE_32(x) || BE_23(y) || 0x80 || BE_8(440).

There are no zero-padding bytes in this case and no second block. As two packed
256-bit words this block is (x, (y << 72) OR 2^71 OR 440). The fields occupy
disjoint positions. The final eight bytes are the original bit length, not
the padded length. All shifts and additions fit the 256-bit word model.

Initialize the eight 32-bit chaining words in this order:

    6a09e667 bb67ae85 3c6ef372 a54ff53a
    510e527f 9b05688c 1f83d9ab 5be0cd19

Parse the block into W[0],...,W[15], in big-endian 32-bit word order. All data
additions below are modulo 2^32; NOT, shifts, and rotations act on 32-bit words.

    s0(z) = ROTR32(z,7) XOR ROTR32(z,18) XOR (z >> 3)
    s1(z) = ROTR32(z,17) XOR ROTR32(z,19) XOR (z >> 10)
    S0(z) = ROTR32(z,2) XOR ROTR32(z,13) XOR ROTR32(z,22)
    S1(z) = ROTR32(z,6) XOR ROTR32(z,11) XOR ROTR32(z,25)
    Ch(e,f,g) = (e AND f) XOR ((NOT e) AND g)
    Maj(a,b,c) = (a AND b) XOR (a AND c) XOR (b AND c)
    W[t] = W[t-16] + s0(W[t-15]) + W[t-7] + s1(W[t-2]),
        for t = 16,...,30.

The constants at their original indices K[0],...,K[30] are

    428a2f98 71374491 b5c0fbcf e9b5dba5 3956c25b 59f111f1 923f82a4 ab1c5ed5
    d807aa98 12835b01 243185be 550c7dc3 72be5d74 80deb1fe 9bdc06a7 c19bf174
    e49b69c1 efbe4786 0fc19dc6 240ca1cc 2de92c6f 4a7484aa 5cb0a9dc 76f988da
    983e5152 a831c66d b00327c8 bf597fc7 c6e00bf3 d5a79147 06ca6351

Copy the IV into (a,b,c,d,e,f,g,h). Execute exactly t = 0,...,30:

    T1 = h + S1(e) + Ch(e,f,g) + K[t] + W[t]
    T2 = S0(a) + Maj(a,b,c)
    (a,b,c,d,e,f,g,h) = (T1+T2, a, b, c, d+T1, e, f, g).

The update is simultaneous. Add every final working word to its corresponding
IV word modulo 2^32. Concatenate BE_4 of all eight results in standard order.
This complete 256-bit digest is H(m), also retained as one 256-bit integer d.
No IV choice, truncation, round renumbering, missing feed-forward, or
compression-only collision is being substituted for the target.

The selected compression, including expansion, rounds and feed-forward, costs
one unit by the organizer's model. Packing, parsing, state transfers, calls,
and all other wrapper operations are additionally charged in section 5.

## 2. Concrete bounded RAM algorithm

A RAM word has 256 bits and occupies 32 bytes. Allocate two arrays A and B,
each with q records, and a counter array P with q words. Each record is exactly
three words (digest,x,y). Record i occupies base+3*i through base+3*i+2;
base+3*i is formed by additions, not by an assumed multiplication primitive.
Scalar state and output buffers live in the separately charged fixed scratch.

1. Generate every sample as in section 1, compute its complete H, and write
   (H,x,y) to A. There is no early exit or sampling without replacement.
2. Perform the stable counting-sort pass below, first for the low 128 digest
   bits from A to B, then for the high 128 bits from B to A. Both have exactly
   q buckets. P is explicitly cleared at the start of EACH pass.
3. Scan A in ascending index order. If adjacent records have equal full
   digests and different (x,y), copy their messages to the fixed output buffer,
   recompute both complete hashes, and check full equality and message
   inequality. Return that pair if the check succeeds; otherwise return FAIL.
   If the scan finds no pair, return FAIL. No restarts are performed.

For the low pass digit(d) = d AND (2^128-1); for the high pass digit(d) = d >> 128.
The shift/mask is counted on every use. Pass code, including endpoint tests, is

    for b = 0,...,q-1:
        P[b] = 0
    for i = 0,...,q-1:
        r = digit(source[i].digest)
        P[r] = P[r] + 1
    total = 0
    for b = 0,...,q-1:
        count = P[b]
        P[b] = total
        total = total + count
    for i = 0,...,q-1:
        (d,x,y) = source[i]
        r = digit(d)
        j = P[r]
        destination[j] = (d,x,y)
        P[r] = j + 1

The loops are ordinary increasing-index loops with explicit increment, test,
and branch instructions. The q loop endpoint is representable. P entries and
prefix sums never exceed q. No scatter writes index q: a nonempty bucket's last
used position is its exclusive endpoint minus one. P may equal that endpoint
only after its final write. Empty buckets cause no destination accesses.

After the histogram, P[b] is the count of records with digit b. The prefix scan
turns it into the start of that bucket's disjoint destination interval. Scatter
uses every slot in the interval exactly once, in source order, preserving the
order of equal-digit records. Thus each pass is a stable permutation of all q
records. After the low pass they are sorted by low half. The stable high pass
orders high halves and retains the low-half order within each high-half group.
Consequently A is sorted by the full 256-bit digest after both passes.

No array is assumed initialized for free. Generation fills all of A, the low
pass fills all of B, and the high pass fills all of A before scanning. Each pass
initializes all q counters. There is no occupied-bucket heuristic, dictionary,
allocation of individual records, or expected-O(1) lookup assumption.

All equal-digest records are contiguous. A contiguous group with at least two
distinct messages has at least one adjacent unequal-message transition, even
though messages within a group are not sorted. Thus the scan returns a pair
whenever the samples contain any collision between distinct messages. Repeated
copies of only one message never count as success. Final verification occurs at
most once and a successful output is always an ordinary complete-hash collision.

## 3. Distribution-free digest-repeat probability

For each possible digest z let p_z be the proportion of the D messages mapping
to z under the fixed deterministic H. Include zeros so p has N coordinates.
Independent input samples produce independent output samples from p. This
does not assert uniformity of p or randomness of the target.

Let e_q(p) be the sum of products over all q-element subsets of coordinates.
The probability that all q digests differ is q! e_q(p). On the compact
probability simplex, e_q attains a maximum. Among maximizers select one
minimizing sum_z p_z^2. If two coordinates a,b differ, write r for the others:

    e_q(p) = e_q(r) + (a+b)e_(q-1)(r) + ab e_(q-2)(r).

Every coefficient is nonnegative; take e_0=1 and out-of-range e_j=0.
Averaging a,b preserves their sum and increases their product by (a-b)^2/4.
It cannot decrease e_q, so the averaged vector is still a maximizer, but it has
a smaller sum of squares. That contradicts the selected minimizer. Hence the
uniform vector maximizes e_q. Since 2 <= q <= N, for every output distribution

    Pr(no digest repeat) <= product_(j=0)^(q-1) (1-j/N)
                        <= exp(-q(q-1)/(2N)).

The second inequality applies 1-u <= exp(-u) term by term. No independence of
pair-collision events is assumed. This is a worst-case bound for any selected
hash on this message family, including a biased or highly concentrated one.

## 4. Success lower bound, distinctness, and failure costs

Let C denote a repeated digest and R a repeated original message. C without R
ensures a valid pair. By the union bound for input repeats, without needing
independence of these events,

    Pr(success) >= Pr(C) - Pr(R)
      >= 1 - exp(-q(q-1)/(2N)) - q(q-1)/(2D).

Here q(q-1)/(2N) = 1/2 - 2^-129 > 499/1000, and
q(q-1)/(2D) = 2^-185 - 2^-313 < 2^-185. For an elementary certification of the
declared success probability, put a = 499/1000. Exact rational arithmetic gives

    exp(a) > 1 + a + a^2/2 + a^3/6 + a^4/24 > 1000/609.

Therefore the probability above is greater than

    391/1000 - 2^-185 > 390/1000 = 0.39.

The approximate uniform-output birthday value is 0.39346934, but that
approximation is not needed for the certified decimal. The claim reports a
lower bound, not equality with the actual probability or AI confidence.
All q samples, both whole-array sorts, and the scan are charged on failed
executions too. Only the bounded final verification can be absent on a failure,
and its worst-case cost is included regardless. There are no hidden restarts,
success-conditioned costs, external message data, or precomputed witnesses.

## 5. Charged implementation and resources

For this track each selected compression costs one unit and every other 256-bit
primitive operation costs 1/2140 units. We separate compression calls from
ordinary operations W; compression internals are never charged a second time.

### 5.1 Scalar, instruction, and interface convention

Implement core instructions for assignment, load/store, two-operand arithmetic,
bit operations, comparisons, branches, and random words. Each core instruction
has at most four instruction words (opcode and operand/immediate fields).
Allow eight charged operations per core instruction: at most four instruction
fetches, two scalar operand loads, the primitive operation, and a result store.
An indirect load/store's address has already been computed by separate core
instructions. This permits all scalars to reside in scratch; it does not require
free constant reloads or an unlimited free-register bank. Address construction,
field offsets, compression dispatch and transfers are explicitly budgeted.

Every increasing-index loop uses at most eight core instructions for its
increment, endpoint comparison, conditional branch, and bookkeeping. The table
below bounds each iteration including this control, addresses, loads/stores,
temporaries, field copies and the digit operation. There are no variable-length
keys or recursion.

| Part of one radix pass | Core instructions per iteration, capped | Iterations |
| --- | ---: | ---: |
| Counter clearing: address, zero store and loop | 16 | q |
| Histogram: record address/digest load/digit, counter address/load/increment/store and loop | 48 | q |
| Prefix scan: counter address/load, start store, total update and loop | 32 | q |
| Stable scatter: read triple, digit, counter load, destination address, three stores, counter update and loop | 96 | q |

For clarity, computing a triple address takes three additions; accessing its
two subsequent fields takes two more. Histogram needs fewer than 24 core
instructions outside its loop: three record-address additions, one digest
load, one digit operation, one counter-address addition, one counter load, one
increment, one store, and scalar copies. Prefix needs fewer than 16 outside
its loop. Scatter needs fewer than 64 outside its loop: two triple addresses
(six additions), four field offsets, three source loads, three destination
stores, one digit operation, one counter-address addition, one counter load,
one increment, one counter store, and bounded scalar copies. These figures
leave slack even with every assignment explicit.

The per-pass loop bodies therefore cost at most

    8*(16+48+32+96)*q = 1536q ordinary operations.

Four loop initializations and exits, total=0, source/destination base selection,
and the pass call/return together cost fewer than 256 ordinary operations per
pass. Unlike per-iteration work, these constants are retained separately below.
The count is independent of the digest distribution, including a single bucket
containing all records. Large bucket ranges are paid for, not treated as free.

Generation costs at most 2048 ordinary operations per message, besides its one
compression. It fits below 256 core instructions: two random draws and y's
shift, padded-word construction, up to 32 shifts/masks to parse 16 words,
eight IV loads/copies, compression input/output transfers and dispatch, up to
24 shifts/ORs to serialize the eight digest words, record addresses/stores,
loop control, and bounded scalar copies. The round schedule and feed-forward
are inside the compression unit. This wrapper allowance exceeds 200 core
instructions even with the random-word instruction fetches charged.

The scan costs at most 1024 ordinary operations per position (128 core
instructions): two triple addresses and field offsets, six loads, digest and
message comparisons and their branches, index/control work, and copying a
potential output pair. It examines at most q positions. Message serialization
for the final output can instead write the first 55 bytes of each already
specified padded block; a byte-at-a-time realization is covered below.

Final verification, comparisons, message-output serialization, and termination
cost at most 16384 ordinary operations plus two compressions, for two complete
one-block hashes. Two wrappers cost at most 4096 ordinary operations. Emitting
110 bytes needs at most twelve core instructions per byte for source selection,
shifting, masking, output addressing/store, and loop control, or 10560 ordinary
operations; comparisons and termination fit in the remaining 1728. Byte values
can each occupy a scratch word before the fixed output interface, so there is
no uncharged variable-length conversion. All small phase-entry/exit and radix-pass
constants fit in the fixed-overhead allowance of 2^20 ordinary operations,
which also covers program loading and scratch initialization.

### 5.2 Storage, advice, and initialization

Two triple arrays require 6q words; P requires q more. They occupy exactly
224q bytes. P is reused between passes. No third record table, sparse index,
pointer headers, retained random tape, or extra bucket list is needed.

Bounded loops allow the fixed program to occupy fewer than 4096 instruction
slots with at most four 256-bit words per slot, or 2^19 bytes. Its wrapper,
four counting-sort loop bodies, scan, initialization and verification need far
fewer than those slots. At most 4096 further words (2^17 bytes) hold constants,
IV, all scratch, padded-block words, states, counters, saved triples, output,
and transfers. No operating system, Python runtime, compiler, or per-record
allocator is part of the specified RAM construction.

Combined fixed storage is less than 2^20 bytes. Program loading, fixed scratch
initialization and all constant phase overheads together need fewer than 2^20
ordinary operations: code has at most 16384 words, scratch 4096 words, and
even eight paid operations per initialized word use well below this allowance.
The q counter clears belong to the sort cost, not to this fixed setup budget.
The fixed setup in compression equivalents is below 2^20/2140; the claimed
`preprocessing_log2: 20` is a conservative upper bound, included in total time.

For q = 2^128, peak memory on every execution is

    M <= 224q + 2^20 < 256q = 2^136 bytes.

Both output messages are included in fixed scratch. All indices, cumulative
counts and allocated word/byte addresses are below 2^136, far below 2^256, so
there is no overflow. N and D are mathematical notation, not stored RAM values.
q, masks and all program constants fit in one word. Actual nonuniform advice
is zero bytes. The schema's nonnegative log field `nonuniform_advice_log2_bytes:
0` is a one-byte upper bound, not an assertion of log2(0). Public fixed code
and SHA constants are still charged to storage and initialization.

### 5.3 Total time and submitted scalar

The following are worst-case bounds, paid on every random tape:

| Phase | Selected compressions | Ordinary operations |
| --- | ---: | ---: |
| Fixed setup and all constant phase overheads | 0 | 2^20 |
| Generate all messages and records | q | 2048q |
| Low and high counting-sort passes | 0 | 3072q |
| Adjacent scan | 0 | 1024q |
| Final complete verification and output | at most 2 | 16384 |

Thus H_calls <= q+2 and W <= 6144q+1064960, so total computation is

    T = H_calls + W/2140
      <= (1 + 6144/2140)q + 2 + 1064960/2140
       = (8284/2140)q + 2 + 1064960/2140
       < 2^129.953.

The coefficient is 3.87102803738317757..., whose log2 is
1.95271675693200256.... The rounded-up exponent leaves more than 0.00075q
units of slack, whereas the constant cost is below 500 units. For q=2^128 the
constants cannot consume that slack. Equivalently, an exact integer check of

    (8284*q + 2140*2 + 1064960)^1000 < 2140^1000 * 2^129953

certifies the strict decimal bound without floating-point rounding. All failed
trials, randomness, counting, table clearing, addressing, sorting, checking,
setup and output costs are included. Time sums work, not parallel latency.
There is no data_log2 claim because that legacy field is optional and unscored.

## 6. Evidence and scope

The certificate manifest is valid and empty. No experiment manifest or executable
participant source is declared. Sections 1-5 are the self-contained analytic
evidence; the judge need not fetch a paper or execute participant code. No
finite experiment or small-word extrapolation supplies a probability premise.

This candidate changes the initial package's 64-byte two-block family to a
55-byte one-block family, reduces its sample count from 2^129 to 2^128 with a
new success lower bound, and replaces comparison sorting with two paid stable
128-bit radix passes. These are algorithm changes requiring fresh review, not
a replay of the initial package's AI qualification. The initial candidate was
read from source 86f1102ff2d6873db29d992599412ae9eb23bda2; its local evaluation
was mechanically valid but had no completed AI review in this environment.

This astronomically large construction uses close to 2^136 bytes of RAM. It
does not establish a practical collision, a security lower bound, a differential
attack, an improvement over the nominal 128 display reference, or superiority
to practical-attack packages awaiting manual review. Mechanical validity is
not AI qualification. AI qualification is not mathematical proof, human
acceptance, or successful promotion. Only the selected exploratory track is
submitted; no conclusion about its rigorous sibling is inherited.
