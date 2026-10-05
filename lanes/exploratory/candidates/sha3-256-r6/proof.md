# Bit-sliced 256-message birthday search for six-round SHA3-256

## 1. Claim and scope

Target: `sha3-256-r6-prefix-v1`. Lane: exploratory. Attack class:
ordinary collision. The selected hash has all-zero IV, rate 1088, capacity
512, SHA3 suffix 0x06, the first six Keccak-f[1600] rounds (0 through 5),
and the complete 256-bit digest. Neither the round convention nor the hash
domain is changed.

Under `collision-frontier-v5`, with C=1626, the algorithm below has:

| Resource | Upper bound |
| --- | --- |
| Total computation | 2^126.995 selected-permutation equivalents |
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
0,1,2,3,4,5. The first four resulting lanes, serialized little-endian,
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

The six constants, as 64-bit hexadecimal integers, are:

    0000000000000001, 0000000000008082, 800000000000808a,
    8000000080008000, 000000000000808b, 0000000080000001.

These are public FIPS 202 constants. The target uses prefix rounds rather
than Keccak-p's last-round convention.

## 3. Fixed-register bit slicing of 256 independent messages

A group contains exactly 256 iid messages. The entire attack still uses
n=2^128 messages, hence n/256 groups. For each of the 1600 Keccak state
bits, hold one 256-bit word X[x,y,z]. Its bit j is state bit (x,y,z) of
message j, 0<=j<256. All XOR, AND and NOT operations then implement that
Boolean gate on 256 independently sampled states simultaneously. This
uses only the cost model's listed word operations, not a SIMD oracle.

The program has a fixed finite register bank of fewer than 2^14 words,
independent of n. It can hold the current, theta-updated and next state
banks (3*1600), 320 parity words, 320 theta words, two 256-word input
matrices, a 256-word output matrix, retained message words and reusable
scalar/gate temporaries. Registers and their stored values count toward
memory. Primitive instructions read their named register operands as part
of the operation; indirect main-memory loads and stores are charged below.
The core uses no data-memory lookup and no register bank growing with n.
A literal register reference is not an indirect free memory access.

This is the same finite-register 256-bit word-RAM model as ordinary lane
code, with a larger fixed constant workspace. No registers wider than
256 bits, multiplication, bit-gather, transpose opcode or vector primitive
are assumed. Even redundant destination placements and state copies are
charged in the conservative envelopes below.

### Exact 256 by 256 transpose using listed primitives

For 256 input words U[0],...,U[255], let matrix entry (j,k) be bit k of
U[j]. We need one word per bit position k, containing all message bits j.
The following straight-line network computes precisely that transpose.

For s=128,64,32,16,8,4,2,1, define a public 256-bit mask M_s whose bit c
is one exactly when (c AND s)=0. For every index i with (i AND s)=0,
set a=U[i], b=U[i+s] and perform, from their old values:

    t0 = a >> s
    t1 = t0 XOR b
    t2 = t1 AND M_s
    t3 = t2 << s
    a  = a XOR t3
    b  = b XOR t2.

Both assignments use the old a,b and the same t2. There are six word
operations per pair. Charge three additional register placements per
pair, for a bound of nine. There are 128 pairs at each of eight stages,
so one complete transpose costs at most 9*128*8=9216 ordinary operations.
All indices, register names, shifts and masks are compiled into the fixed
unrolled program. There is no uncharged run-time loop or addressing in
this network. Setup constructs and stores its eight masks.

To prove the network, consider a low block position c with (c AND s)=0.
The update swaps bit c+s of row i with bit c of row i+s, and changes no
other bit: XORing their difference into both positions performs the swap.
Thus this stage exchanges the s bit of the row coordinate with the s bit
of the column coordinate wherever they differ. It fixes entries where
those two coordinate bits agree. Successively exchanging the eight bits
maps every original entry (j,k) to (k,j). This proves the complete transpose,
including both ends of the 256-bit words. The transpose is its own inverse.
This is an exact algebraic circuit argument, not a seeded experiment.

Use two transposes for the two independent 256-bit message words. After
transposition, input matrix b in {0,1}, row k in [0,255], maps to Keccak
lane floor((256*b+k)/64), bit k mod 64. The remaining 1088 state-bit words
are initialized to zero or all-ones according to the exact suffix and
padding in Section 2. These are fixed register placements, charged below.

After the final round, collect the 256 output bit-plane words in order
64*i+z, where i=0,1,2,3 and z=0,...,63. One more transpose converts them
into 256 ordinary full-digest words. Its bit k has exactly the conventional
little-endian output bit k of message j. Therefore the group uses exactly
three transposes and retains all 256 output bits.

## 4. Bit-plane round circuit and its operation envelope

All coordinates here are public compile-time indices. Arithmetic on
x,y is modulo 5 and on z modulo 64. Write Z=2^256-1. For every round:

    C[x,z] = XOR_{y=0}^4 X[x,y,z]
    D[x,z] = C[x-1,z] XOR C[x+1,z-1]
    A[x,y,z] = X[x,y,z] XOR D[x,z]
    B[y,(2*x+3*y) mod 5,z] = A[x,y,z-rho[x,y]]
    Y[x,y,z] = B[x,y,z] XOR
               ((NOT B[x+1,y,z]) AND B[x+2,y,z])
    Y[0,0,z] = Y[0,0,z] XOR Z whenever bit z of RC[round] is 1.

A rotation of a 64-bit lane changes which bit-plane register is referenced.
It is therefore implemented by this fixed wiring, not by incorrectly
rotating message bits inside a plane word. Rho/pi register names are
hardwired for each round. We still allow 1600 extra word moves to materialize
all B references, whether the compiler instead uses aliases or copies.

Each word's bit j obeys exactly the scalar round equations in Section 2.
By induction over rounds 0 through 5, the resulting state and output of
each of the 256 fields are precisely the selected complete hash. Padding,
IV, prefix-round constants and output length are unchanged. Computing
many independent instances with Boolean word operations changes neither
their message distribution nor the target function.

The complete conservative round envelope is:

| Stage | Logical word operations | Extra destination placements |
| --- | ---: | ---: |
| Five columns times 64 bits, four XORs per parity | 1280 | 1280 |
| Five columns times 64 theta differences | 320 | 320 |
| Twenty-five lanes times 64 theta XORs | 1600 | 1600 |
| Rho/pi, fixed references with optional materialized copies | 0 | 1600 |
| Twenty-five lanes times 64 NOT/AND/XOR sequences | 4800 | 4800 |
| Iota, pessimistically every bit of the round constant set | 64 | 64 |
| Totals | 8064 | 9664 |

The totals sum to 17728. Charge 18000 ordinary operations per round,
leaving 272 for further scalar placements and boundary/control details.
The six rounds are fully unrolled, with separate input/output state banks
so chi never destroys a neighbor before it is used. XOR/NOT/AND operands
are named finite registers; this table additionally charges a placement
for every logical result, beyond its primitive's normal result write.
No indirect array access, lookup, random word, transpose or target-hash
invocation is hidden in the core. Public round constants are in setup.

## 5. Complete grouped sampling, storage and initialization

For each group draw 512 fresh independent uniform 256-bit words: two
per message. Before transposing their register matrices, store the original
u,v in their assigned source records. Run the two input transposes,
initialize the padded state, execute six bit-plane rounds, transpose the
256 output planes, and store each resulting digest in that same record.
The record is exactly (h,u,v). The messages stay associated with their
complete digests through every later sorting pass. No repeated input or
unfavorable output is discarded.

In addition to the three transposes and the round circuits, charge the
following finite envelope per group:

| Work per group | Bound |
| --- | ---: |
| 512 fresh random-word primitives and register placements | 1024 |
| Store two original message words in each record, with addresses and moves | 3072 |
| 512 input-plane placements and 1088 fixed padding/zero placements | 2048 |
| Copy 256 output planes and any additional output placements | 512 |
| 256 full digest stores, record addressing and pointer/control operations | 2560 |
| Group index/base updates, comparisons, branches and scalar setup/moves | 1024 |
| Further spare moves and fixed boundary handling | 2048 |
| Envelope | 12288 |

The fixed 256-message inner loops can all be unrolled. Only the n/256
outer-group loop needs run-time control. The generous address/control
rows include each memory store, offset formation, pointer increment and
operand move; they do not assume free memory traffic. Neither sampling
nor grouping uses deterministic seed expansion. Independent ideal coins
come only from the explicitly charged random-word primitive.

Before generation, initialize both complete three-word record arrays.
The joint loop uses three stores, two offset additions and one 96-byte
pointer increment per array, plus shared index increment, comparison and
branch: 15 operations per paired record. Charge 16n including loop setup.
No cell is read before being initialized or subsequently written.

Thus generation costs at most

    (6*18000 + 3*9216 + 12288)*(n/256)
       = 577.875*n ordinary word operations.

There are no selected-permutation primitive calls during generation.
Instead its explicitly implemented word circuit is charged at 1/1626
per primitive operation. Charging the same core again as n hash-oracle
calls would count that computation twice. The final two independent
witness checks do use the selected-permutation primitive, at unit price.

## 6. Stable radix sorting with four 64-bit digits

Let b=2^64. Allocate one array Q of b counters, each a 256-bit word.
It is reused for all passes. A count or prefix sum can be n, which is
still representable in one 256-bit word. Records are stably sorted by
four consecutive least-significant digits of their complete digest:
shifts s=0,64,128,192, mask b-1. No shorter digest is treated as a collision.

For each of the four passes:

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
digit t and preserves the ordering of lower digits among ties. Four passes
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
branch). Charge 12b operations per pass, hence 48b across all four.
Only the counter cells need this clearing between passes; the destination
record array is completely overwritten before becoming a source again.

## 7. Recovering and checking a collision

Scan every adjacent record pair. Test equality of the complete h word and
inequality of the two-word message. If both hold, reconstruct the two
64-byte messages and independently recompute both complete six-round
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
messages. The bit-plane round and transpose identities prove that its stored digests are exact.
Independent recomputation prevents accepting either a repeated input or
a truncated/compression-only result. In the mathematical RAM these checks
cannot fail on a correctly identified pair, but their cost is included.

## 8. Success probability for the fixed target

Let H be the selected deterministic complete hash. Write q=2^256 and
p_y=|H^-1(y) intersect D| / |D|. The sampled messages M_i are iid uniform
on D. Thus their outputs Y_i=H(M_i) are iid with probability vector p;
p need not be uniform and H is not randomized. Bit slicing 256 independent
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

There are n/256 groups, four sorting passes and one bounded scan. Charge
2^24 additional ordinary operations for one-time constants, masks, code,
base/register setup and all finite boundary work. The entire unrolled
program has fewer than 2^18 instructions. Encoding an instruction in at
most eight 256-bit words uses less than 2^27 bytes. Its initialization,
eight transpose masks, round constants, fixed register bank, outputs and
scalar workspace fit within 2^28 bytes and the 2^24-operation setup charge.
For example each M_s is generated by ORing its at most 128 public runs
of low s bits at fixed offsets, using fewer than 2^12 operations for all
masks. All this setup is included, not supplied as preinitialized advice.

The complete ordinary-operation and target-equivalent bounds are

    W <= ((6*18000+3*9216+12288)/256 + 16 + 4*44 + 40)*n
         + 48*2^64 + 2^24 + 200
       = 809.875*n + 48*2^64 + 2^24 + 200.

    T <= W/1626 + 2.

The leading logarithm is

    128 + log2(809.875/1626) = 126.99444390039272...

The nonleading terms are less than 2^-57 of the leading term. Therefore
T<2^126.995, with more than 0.00055 bits of upward-rounding margin.
This is a worst-run bound: each failing batch consumes the same budget,
and no expectation conditioned on success, restart or successful-only
search work replaces total charged computation.

Preprocessing is bounded by

    P <= (16*n + 5*2^64 + 2^24)/1626 < 2^122.

It is already in W. There is no precomputed collision, secret advice,
differential search, unexplained seed or discarded search work. Zero
advice bytes are conservatively encoded by schema value zero.

Peak memory is bounded by

    192*n + 32*2^64 + 2^28 bytes < 2^136 bytes.

This covers both three-word record arrays, all counters, the entire
finite register bank, retained random words, code, masks and output.
Place A at byte address 2^28, B after A and Q after B. Their highest
address is below 2^136, so every 96*i address and 32*j counter offset,
n-valued count and sentinel fits in one 256-bit word. No wider word or
zero-initialized giant table is assumed.

## 10. Evidence, provenance and limits

The construction is specified and supported by the exact transpose
identity, bit-plane round-by-round equivalence, stable radix invariant and the
fixed-function probability proof. The certificate manifest is empty.
There is no executable experiment declaration and no claimed measured
collision. Infeasibility of a full-scale run is disclosed, not replaced
by a model's confidence or a smaller-output experiment.

The target definitions and numerical primitive price are organizer-owned
contract facts. FIPS 202 supplies the public Keccak maps, rho offsets and
round constants. The 256-message transpose and bit-plane implementation, sorting choice,
finite instruction envelopes and bound in this package are independently
derived. It contains no copied organizer implementation or peer program.
The organizer candidate's generic-birthday direction supplies context;
this document gives the necessary probability argument in full.

The required `baseline_improved` identifier denotes the organizer's
nominal reference. The supported scalar is below that nominal exponent,
but this is not a mathematical security boundary or a practical defeat
of SHA3. The larger memory compared with a distinguished-point search is
an explicit tradeoff; no Pareto dominance is claimed.

Mechanical intake cannot certify these resource or probability arguments.
Exploratory AI qualification, rigorous AI qualification, official scoring,
manual organizer acceptance and promotion remain separate outcomes.
