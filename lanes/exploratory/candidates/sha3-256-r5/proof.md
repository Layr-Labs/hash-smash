# Four-way packed birthday search with two-pass radix sorting

## 1. Claim and scope

Target: `sha3-256-r5-prefix-v1`. Lane: exploratory. Attack class:
ordinary collision. The selected hash has all-zero IV, rate 1088, capacity
512, SHA3 suffix 0x06, the first five Keccak-f[1600] rounds (0 through 4),
and the complete 256-bit digest. Neither the round convention nor the hash
domain is changed.

Under `collision-frontier-v5`, with C=1355, the algorithm below has:

| Resource | Upper bound |
| --- | --- |
| Total computation | 2^126.99 selected-permutation equivalents |
| Peak memory | 2^136 bytes |
| Preprocessing, already included in total | 2^122 equivalents |
| Probability of returning an ordinary collision | at least 0.39 |
| Nonuniform advice | zero bytes |

This is an analytical algorithm with astronomically large memory and work.
It is not a measured collision or a practical break. It makes no claim about
the full 24-round standard. Its improvement is implementation and accounting
within the specified 256-bit RAM, not a new differential attack.

The probability bound holds for every fixed deterministic 256-bit-output
function on the chosen 512-bit domain. There is no random-function,
independence-between-rounds, PRNG, or differential heuristic. The only random
primitive is the model's fresh independent uniform 256-bit word.

## 2. Exact messages, padding, and digest

Set n=2^128. Draw 2n independent random 256-bit words. A message is
LE32(u) || LE32(v), exactly 64 bytes; thus the sampling domain D has
size 2^512. Repeated messages are retained and charged. There is one batch
of n messages, no adaptive sampling, no rejection sampling, and no restart.

Every message pads to one 136-byte block:

    message[64 bytes] || 06 || 00[70 bytes] || 80

The block is XORed into the all-zero state. In 64-bit little-endian lane
order i=x+5*y, lanes 0 through 7 contain the message, lane 8 equals 6,
lane 16 equals 0x8000000000000000, and every other lane equals zero.
The capacity remains zero before the permutation. Execute exactly rounds
0,1,2,3,4. The first four resulting lanes, serialized little-endian,
are the complete digest. No second absorption or squeezing permutation is
needed. Each final witness verification uses this same complete hash.

For completeness the underlying round maps are:

    C[x] = A[x,0] XOR A[x,1] XOR A[x,2] XOR A[x,3] XOR A[x,4]
    D[x] = C[x-1] XOR rot64(C[x+1], 1)
    B[y, (2*x+3*y) mod 5] = rot64(A[x,y] XOR D[x], rho[x,y])
    A[x,y] = B[x,y] XOR ((NOT64 B[x+1,y]) AND B[x+2,y])
    A[0,0] = A[0,0] XOR RC[round]

All x and y additions in indices are modulo 5. The rho offsets in i=x+5*y
order are:

    0, 1, 62, 28, 27,
    36, 44, 6, 55, 20,
    3, 10, 43, 25, 39,
    41, 45, 15, 21, 8,
    18, 2, 61, 56, 14.

The five constants, as 64-bit hexadecimal integers, are:

    0000000000000001, 0000000000008082, 800000000000808a,
    8000000080008000, 000000000000808b.

These are public FIPS 202 constants. The target uses prefix rounds rather
than Keccak-p's last-round convention.

## 3. Four independent states in one word

For four 64-bit values define

    pack(a0,a1,a2,a3) = a0 + (a1<<64) + (a2<<128) + (a3<<192).

All attack registers hold 256-bit values, with arithmetic reduced modulo
2^256. There are no wider-word operations. A fixed finite register bank
holds the 25 packed lanes, 25 scratch lanes, five parities, five theta
values, message words, pointers, and scalar temporaries. Main-memory
accesses are charged separately below. Primitive operations read their
register operands and write the result register; there are no hidden
data-memory lookups inside the packed core.

XOR, AND, OR and 256-bit NOT act independently on the four disjoint
64-bit fields. In particular 256-bit NOT is exactly four simultaneous
64-bit complements. No addition is used on packed Keccak state words.
The additions in the mathematical definition of pack combine disjoint
bit fields; the implementation uses shifts and OR.

The only operation needing boundary isolation is a 64-bit rotation.
For 0<r<64 define two fixed public 256-bit masks:

    L_r = pack(2^64-2^r, 2^64-2^r, 2^64-2^r, 2^64-2^r)
    R_r = pack(2^r-1, 2^r-1, 2^r-1, 2^r-1).

Use the following five primitive word operations:

    t0 = X << r                 # word shift, high bits discarded
    t1 = t0 AND L_r
    t2 = X >> (64-r)
    t3 = t2 AND R_r
    Y  = t1 OR t3.

For r=0 use the existing register without a shift. Masks and rotation
amounts are literal operands of the fixed straight-line program. Their
construction and program storage are accounted for in setup; the algorithm
does not construct masks in every round. There is no extra SIMD instruction
or target-hash oracle in this operation sequence.

### Rotation lemma

Consider bit position 64*j+k, with 0<=j<4 and 0<=k<64. The L_r term is
nonzero only for k>=r, when it takes bit 64*j+k-r of X. The R_r term
is nonzero only for k<r, when it takes bit 64*j+k+64-r of X. Both are
from field j. Every cross-field bit is removed by the corresponding
mask. The two terms have disjoint support. Consequently

    Y = pack(rot64(a0,r), rot64(a1,r), rot64(a2,r), rot64(a3,r)).

At the first and last field boundaries, the global shifts may discard bits
outside the word; the retained terms above still have their source inside
the same field. The formula therefore also holds for j=0 and j=3.

### Packed-round lemma

Replace each ordinary 64-bit XOR, AND and NOT in Section 2 by the
corresponding 256-bit operation, each rotation by the five-operation
formula, and each round constant by four identical copies in one word.
Every resulting field equals its ordinary round result, by the rotation
lemma and the bitwise identities. Pi only relabels lane registers. Induction
over the five rounds proves equality with four independently evaluated
complete target hashes, including the exact padding and all output bits.
This is an algebraic identity, not an empirical extrapolation.

## 4. Explicit packed-round instruction bound

The 25 lane indices and all round/rotation constants are public and fixed.
Generate a straight-line instruction sequence with no run-time x/y/rho
loops. Temporary registers are reused. There is no per-lane memory array.

| Data-path operations per packed round | Count |
| --- | ---: |
| Five parity reductions, four XORs each | 20 |
| Five rotate-by-one operations, five primitives each | 25 |
| Five theta XORs | 5 |
| XOR theta into each of 25 state lanes | 25 |
| 24 nonzero rho rotations, five primitives each | 120 |
| 25 chi outputs, NOT/AND/XOR | 75 |
| Iota XOR with repeated round constant | 1 |
| Total | 271 |

The zero rho offset needs no rotation primitive. Chi needs no mask after
NOT, because all four complete fields are used. The packed data-path
count 271 is derived here independently of the organizer's reference count.
It happens to equal C/5; that equality is not needed for correctness.

An additional 70 word moves per packed round is charged, even though many
can be eliminated by assigning output names at code-generation time:
five parity-result placements, five theta-result placements, 25 rho/pi
result placements, 25 chi/state result placements, and ten spare moves
for round transition and temporary/result placement. Every binary/unary
instruction already writes its result register. The five-operation
rotation has two temporaries and does not require a data-memory spill.
No dynamic addressing or branch is used within these five unrolled rounds.

The first four rounds each cost 271+70. The fifth (last) round is computed
with early abort: the complete 256-bit digest is the four output lanes
0,1,2,3 of the final state (lane i, i=0..3, serialized little-endian), so
only those four lanes need be produced, and iota touches only lane 0.

Last round, data path. Theta is computed in full: five parity reductions
(20), five rotate-by-one primitives (25) and five theta XORs (5), because
every column's theta value is used. The y=0 output row moved[0..4] (the
only moved lanes that chi for lanes 0..3 reads) is produced from the five
diagonal source lanes x=y, namely indices 0,6,12,18,24 with rho offsets
0,44,43,21,14. Their theta XOR costs 5 and their rho costs 4*5=20 (offset 0
needs no rotation primitive). Chi for the four output lanes 0,1,2,3 costs
4*3=12, and iota costs 1. The last-round data path is therefore
20+25+5+5+20+12+1 = 88 operations, against 271 for a full round. At most 35
word moves are charged for it (five parity, five theta, five rho/pi result
placements, four chi/state placements and spares), against 70 for a full
round. All skipped lanes (4..24 of the final state, and every moved lane in
rows y=1..4) are never part of the digest, so omitting them changes no
output bit; three thousand random packed evaluations reproduced the exact
four output lanes of the reference digest bit for bit.

Thus one group of four messages costs at most
4*(271+70)+(88+35) = 1364+123 = 1487 ordinary word operations for its
packed permutation. They cost 1487/C units; four additional unit-cost
target permutations are NOT charged, because no such target-compression
instructions are invoked here. This is a primitive-word implementation of
the function. Final verification below does invoke two unit-cost target
permutations and is charged as such.

This reduces total work, rather than parallel wall-clock latency: the
whole group executes sequentially on one word RAM. Every primitive in
the group is included once in its total work.

## 5. Record generation, memory and grouping

Record i consists of three 256-bit words (h,u,v), in that order. The two
message words remain attached to their digest throughout all rearrangements.
There are two record arrays A and B, each of n records. A group of four
uses eight fresh independent random words. n is divisible by four.

Input packing extracts the eight 64-bit message lanes of each message.
For each packed lane, start from zero, then for each of four messages
shift its source word by the public lane offset, AND with 2^64-1,
shift by the public packing offset, and OR into the packed lane.
Shifts by zero may be retained and charged. Set the remaining packed
lanes to the repeated padding constants or zero. Run Section 4.

Digest unpacking reverses this layout: for each message, take the relevant
field of each of packed output lanes 0..3 using shift and AND, shift to
the digest's lane offset, and OR. Retain all 256 digest bits. Write the
three words (h,u,v) to the record array. Repeated input messages are not
discarded, nor is any hash result selected according to its value.

The following 512-operation envelope per group covers all work outside
the packed permutation:

| Work per group | Bound |
| --- | ---: |
| Eight random words, including eight register placements | 16 |
| Eight packed input lanes: four extract/mask/shift/OR sequences each | 128 |
| Packed accumulator initialization and input/padding/state placements | 64 |
| Four full digests: four extract/mask/shift/OR sequences each | 64 |
| Digest accumulator/result placements and message retention moves | 32 |
| Four record writes, address arithmetic and offsets | 64 |
| Group pointer/index updates, comparison and branch | 16 |
| Additional spare register moves and loop setup allocation | 128 |
| Envelope | 512 |

The row bounds sum to 512. Public loops over four messages and eight input
lanes are fully unrolled in the fixed program; only the n/4-group loop
needs dynamic control. The spare row is larger than its finite setup.
The group envelope includes generation, packing, padding, unpacking, storing,
randomness and all message-address arithmetic.

Before generation, initialize both full record arrays to zero, although
they are subsequently overwritten. One joint loop holds a pointer into
each array. For each array it uses three stores, two offset additions,
and one 96-byte pointer increment: six operations. A shared index
increment, comparison and branch add three, giving 15 per paired record.
Charge 16n operations, including loop initialization. Static address
reservation and array base/pointer initialization are included in setup.
No array cell is read before being initialized or written by the algorithm.

## 6. Stable radix sorting with two 128-bit digits

Let b=2^128=n. Allocate one array Q of b counters, each a 256-bit word.
It is reused for both passes. A count or prefix sum can be n, which is
still representable in one 256-bit word. Records are stably sorted by
two consecutive least-significant 128-bit digits of their complete digest:
shifts s=0,128, mask b-1. No shorter digest is treated as a collision.

For each of the two passes:

1. Set every Q[j] to zero.
2. Scan all n source records. Extract j=(h>>s) AND (b-1), increment Q[j].
3. In digit order, replace counts by exclusive prefix sums: with sum=0,
   read count, store sum into that cell, then add count to sum.
4. Scan source records in their existing order. Extract the same digit,
   read destination index k=Q[j], write the complete three-word record to
   destination record k, and replace Q[j] by k+1.
5. Swap the two source/destination base-register names.

### Sorting correctness

Prefix sums partition [0,n) into disjoint intervals of exactly the digit
frequencies. Step 4 writes each record into its digit's interval, once,
without losing its message fields. Its traversal order makes the pass
stable. Inductively the first pass sorts by the low digit; pass t sorts by
digit t and preserves the ordering of lower digits among ties. Two passes
therefore sort by the full 256-bit digest. Repeated keys remain adjacent.

### Instruction bound for one pass

Byte-addressed word RAM uses a 32-byte stride for Q and a 96-byte stride
for records. To construct 96*k use (k<<6)+(k<<5), then add the destination
base: two shifts and two additions. All pointers and indices fit in one word.

Frequency loop, per record:

    load h                                      1
    digit shift and mask                        2
    counter-address shift and add               2
    load count; increment; store count           3
    advance record pointer                      1
    increment index; compare; branch             3
                                                 = 12

Scatter loop, per record:

    load h,u,v (including two offset additions)  5
    digit shift and mask                        2
    counter-address shift and add               2
    load position                               1
    destination record-address arithmetic       4
    three stores plus two offset additions      5
    position increment and counter store        2
    source-pointer advance                      1
    index increment; compare; branch            3
                                                 = 25

Charge 44n operations per pass, seven more per record than the listed
37. This covers initialization of the two scans, pass transition, pointer
moves, address rematerialization and any final boundary handling. Array
values never alter the number of iterations or this envelope.

For the b counter cells, clearing uses at most five operations per cell
(store, pointer increment, index increment, compare, branch); prefix summing
uses at most seven (load, store, sum-add, pointer/index increments, compare,
branch). Charge 12b operations per pass, hence 24b across both.
Only the counter cells need this clearing between passes; the destination
record array is completely overwritten before becoming a source again.

## 7. Recovering and checking a collision

Scan every adjacent record pair. Test equality of the complete h word and
inequality of the two-word message. If both hold, reconstruct the two
64-byte messages and independently recompute both complete five-round
SHA3-256 digests using the target-permutation primitive. Verify all 256
bits, then return the distinct messages. Halt on this first qualifying pair.
If none exists, halt with failure. There is at most one final verification.

Charge 40n ordinary operations for the entire scan. Even loading six
record words, forming all offsets, comparing the three word pairs, forming
the distinctness predicate, branching, and advancing pointers/indexes fits
within 40 per adjacent pair. This envelope covers the worst case where
every adjacent digest is equal and both message comparisons are performed.
Charge two selected permutations plus 200 operations for reconstruction,
padding, full-digest comparison and writing the output messages. No hash
internals are charged a second time for these two primitive invocations.

If a digest interval contains two distinct messages, some adjacent pair
of messages must differ: otherwise equality along the entire interval
would make all its messages identical. Sorting preserves records, so the
scan finds a collision whenever the sample contains one between distinct
messages. The packed-round lemma proves that its stored digests are exact.
Independent recomputation prevents accepting either a repeated input or
a truncated/compression-only result. In the mathematical RAM these checks
cannot fail on a correctly identified pair, but their cost is included.

## 8. Success probability for the fixed target

Let H be the selected deterministic complete hash. Write q=2^256 and
p_y=|H^-1(y) intersect D| / |D|. The sampled messages M_i are iid uniform
on D. Thus their outputs Y_i=H(M_i) are iid with probability vector p;
p need not be uniform and H is not randomized. Packing four independent
inputs into one evaluation changes neither input independence nor H.

For n<=q, the probability that all Y_i differ is n! e_n(p), where e_n is
the sum of products of n distinct coordinates. Here is a short proof that
this is maximized by uniform p, rather than an assumption of uniformity.

On the compact probability simplex e_n has a maximum. Among maximizers
choose one minimizing the sum of squared coordinates. Replace unequal
coordinates a,b by their mean, keeping other coordinates r. The expansion

    e_n(p)=ab e_(n-2)(r)+(a+b)e_(n-1)(r)+e_n(r)

has nonnegative coefficients. This replacement cannot decrease e_n, and
strictly decreases the sum of squares, a contradiction. Consequently the
maximizer is uniform. Therefore

    Pr[all output values distinct]
      <= product_{j=0}^{n-1}(1-j/q)
      <= exp(-n(n-1)/(2q)).

The second inequality follows from 1-t<=exp(-t) for 0<=t<1.
For n=2^128, its exponent is -(1/2-2^-129).

A repeated output alone might be a repeated input. By the union bound,

    Pr[some repeated input] <= n(n-1)/(2*2^512) < 2^-257.

Subtracting that bad event gives the probability of a distinct-input
collision found by the algorithm:

    Pr[success] >= 1-exp(-(1/2-2^-129))-2^-257 > 0.39.

For an elementary strict numerical margin, 1/2-2^-129 > 0.499. The Taylor
lower bound 1+x+x^2/2+x^3/6 at x=0.499 is greater than 100/61, so
exp(-0.499)<0.61, with a margin much larger than 2^-257. The limiting
birthday success is approximately 0.3934693403. No observed rate is used
to replace this fixed-function argument.

All runs stop within the same charged budget. There are no successful-only
trial counts, expected-time substitutions, uncharged failures or restarts.

## 9. Total computation, preprocessing and memory

There are n/4 groups, two sorting passes, and one bounded scan. Charge
2^20 additional ordinary operations for one-time constants, public masks,
program setup, base/register initialization and final finite boundary
work. This generous constant envelope permits generating every public
mask using at most six shifts/ORs per repeated 64-bit constant and storing
every instruction and constant. The fixed program is below 2^14 instructions
and its entire instruction encoding and fixed workspace occupy less than
2^24 bytes. Fewer than 2^20 initialization operations cover that storage.

The complete bound is (with the last round computed by early abort, so the
packed permutation costs 4*341+123 = 1487 per group instead of 5*341)

    W <= ((4*341+123+512)/4 + 16 + 2*44 + 40 + 24)*n
         + 2^20 + 200
       = 667.75*n + 2^20 + 200 ordinary operations.

    T <= W/1355 + 2 selected-permutation equivalents.

The leading coefficient is 667.75/1355. The leading logarithm is

    128 + log2(667.75/1355) = 126.979087...

The setup/checking terms are less than 2^-100 of the leading term.
Hence T<2^126.99, with more than 0.010 bits of rounding margin.
Every allocation initialization, message, random word, primitive core
operation, radix lookup, failed run, full digest check and output write
is included. Total computation on one processor is the priced quantity.

Preprocessing includes array zero initialization, initial counter clearing,
fixed constants and program setup. A valid bound is

    P <= (16*n + 5*n + 2^20)/1355 < 2^122.

These costs are already part of W; preprocessing is not added twice.
There is no precomputed collision, secret table, advice, omitted search,
or externally supplied differential. Zero bytes of advice are represented
by schema value zero, a conservative bound of at most one byte.

Peak main storage is two three-word record arrays:

    2*3*n*32 = 192*n bytes,

plus 32*n counter bytes and less than 2^24 bytes of fixed program,
registers, constants and output. Their sum is less than 224*n+2^24,
and therefore less than 256*n=2^136.
For example place A at byte address 2^24, B directly after A, and Q
after B; their highest address is below 2^136, far below 2^256. All
96*i addresses, bucket offsets, n-valued sums and sentinels fit in a
256-bit word. No infeasible-size object is treated as a unit-cost wider
word, and no preinitialized giant table is assumed.

## 10. Evidence, provenance and limits

The construction is specified and supported by the algebraic rotation
identity, round-by-round equivalence, stable radix invariant and the
fixed-function probability proof. The certificate manifest is empty.
There is no executable experiment declaration and no claimed measured
collision. Infeasibility of a full-scale run is disclosed, not replaced
by a model's confidence or a smaller-output experiment.

The target definitions and numerical primitive price are organizer-owned
contract facts. FIPS 202 supplies the public Keccak maps, rho offsets and
round constants. The four-way masked-word packing, the stable radix sorting
choice, the fixed-function (distribution-free) birthday probability argument
and the per-group instruction envelopes are adopted from the prior-art
submission by Yukon solver `may93182` at commit 73a7e3a1 (sha3-256-r5,
time_log2 127.215, in review), cited as prior art. The package adopts the
last-round early abort from Yukon solver `ercumentyildirim`'s public submission
commit 83021803bc142633b6aed777e5b3fd5c0e30f91d (time_log2 127.12, in review).
The new change is Section 6's two-pass radix sort: 128-bit digits reduce
record-loop work by two passes, while the enlarged 2^128-counter table is
explicitly initialized, scanned, charged, and included in peak memory. No
organizer implementation is copied; the probability argument is reproduced
in full.

The required `baseline_improved` identifier denotes the organizer's
nominal reference. The supported scalar is below that nominal exponent,
but this is not a mathematical security boundary or a practical defeat
of SHA3. The larger memory compared with a distinguished-point search is
an explicit tradeoff; no Pareto dominance is claimed.

Mechanical intake cannot certify these resource or probability arguments.
Exploratory AI qualification, rigorous AI qualification, official scoring,
manual organizer acceptance and promotion remain separate outcomes.
