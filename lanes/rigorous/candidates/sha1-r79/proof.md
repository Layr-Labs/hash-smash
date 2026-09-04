# A distribution-free baseline for complete SHA-1 with 79 prefix rounds

This package selects `sha1-r79-prefix-v1`, ordinary collisions, 79 rounds,
and the rigorous lane under `paired-lanes-v1` and `collision-frontier-v3`.
Its claim is an upper bound for a finite randomized RAM algorithm, not a
measurement, an executed collision search, or a cryptanalytic improvement.

## 1. Parameters and claimed bounds

Let N = 2^80, D be all 32-byte strings, d = |D| = 2^256, and M = 2^160.
Let H be the exact complete-message hash specified in Section 2. Sample N
independent uniform 256-bit words and interpret each as a 32-byte message in
big-endian order, retaining leading zero bytes. This is a bijection with D.
The probability space is the product of N uniform word spaces, with H fixed.
Independent random-word access is the charged primitive supplied by the
organizer's probabilistic RAM model, not a seeded PRNG or a random oracle.

| Claim field | Upper bound and units |
| --- | --- |
| `time_log2: 94` | At most 2^94 charged operations, in the model's target-compressions unit; each ordinary RAM primitive also costs one unit. |
| `memory_log2_bytes: 88` | At most 2^88 bytes of peak memory, including both arrays, code, constants, messages, retained coins, and scratch. |
| `data_log2: 81` | At most N+2 <= 2^81 complete selected-target evaluations counting final verification; at most N distinct chosen messages. |
| `preprocessing_log2: 20` | At most 2^20 charged initialization operations, included in total time. |
| `success_probability: 0.39` | Probability of returning distinct complete messages with equal full digests is greater than 0.39. |
| `nonuniform_advice_log2_bytes: 0` | Actual nonuniform advice is zero bytes; the field encodes the admissible upper bound 2^0 = 1 byte, not log2(0). |

The data field counts chosen-message evaluations, not bytes or entropy bits.
There is no external dataset. Exactly N random-word draws consume 256N
random bits; the sampled input bytes counting multiplicity total 32N; the
bytes submitted to hash evaluations total at most 32(N+2). No random tape is
stored separately from the messages. The scalar is 94+88 = 182, a conservative
upper bound rather than an optimality claim. The schema-required field
`baseline_improved` contains the reference identifier `sha1-r79-nominal-v2`.
The nominal reference value is 80; this construction's scalar is 182 > 80,
which is worse under the lower-is-better numerical comparison. The identifier
is metadata, and the candidate makes no assertion of improvement over that
reference or of Pareto dominance. The nominal entry is not an established
attack, qualified baseline, or security bound.

## 2. Exact complete-message target

Every message has 32 bytes and bit length 256 < 2^64. Append byte 0x80,
then 23 zero bytes, then the 8-byte big-endian encoding of 256. The padded
message is exactly one 64-byte block. Initialize the chaining words once
per message to these hexadecimal values, in order:

    h0=67452301; h1=efcdab89; h2=98badcfe; h3=10325476; h4=c3d2e1f0.

All hash-state words below are 32 bits, and all hash additions are modulo
2^32. For masked x, define ROL32(x,s) =
((x << s) OR (x >> (32-s))) AND 0xffffffff. Parse consecutive big-endian
32-bit block words W[0..15]. W[0..7] are the message words, W[8]=0x80000000,
W[9..14]=0, W[15]=0x00000100. For t=16,...,78 set

    W[t] = ROL32(W[t-3] XOR W[t-8] XOR W[t-14] XOR W[t-16],1).

Initialize (a,b,c,d,e)=(h0,h1,h2,h3,h4). Execute indices t=0,...,78:

    t=0..19:  f=(b AND c) OR ((NOT b) AND d); K=5a827999
    t=20..39: f=b XOR c XOR d; K=6ed9eba1
    t=40..59: f=(b AND c) OR (b AND d) OR (c AND d); K=8f1bbcdc
    t=60..78: f=b XOR c XOR d; K=ca62c1d6
    z=(ROL32(a,5)+f+e+K+W[t]) mod 2^32
    (a,b,c,d,e)=(z,a,ROL32(b,30),c,d)  [simultaneous update]

NOT is restricted to 32 bits, equivalently masked before use. Feed-forward
produces (g0,g1,g2,g3,g4)=(h0+a,h1+b,h2+c,h3+d,h4+e), wordwise modulo 2^32.
H is the concatenation of the five 4-byte big-endian encodings, all 160 bits.
Represent it in a record by g0*2^128+g1*2^96+g2*2^64+g3*2^32+g4, extended
with zero high bits to one 256-bit word. This representation is injective
on full 20-byte digests, including those with leading zero bytes.

For sampled word R, the padded block in two 256-bit words is precisely
(R, (0x80 << 248) OR 256). One selected-round target compression on this
block and the fixed IV costs one model unit, including expansion, rounds,
and feed-forward. Preparing the block, calling the primitive, and packing
the result are separately charged below. The displayed internal formula
specifies that primitive exactly. All returned messages use ordinary fixed-IV,
complete-message, 79-prefix-round hashing with full output.

## 3. Bounded algorithm and storage

Reserve two disjoint arrays A and B of N records. Each aligned record is
two 256-bit words (64 bytes): the digest integer followed by the entire
message integer. Put both arrays after a fixed code and scratch region.
Record i has byte address base+(i << 6); its second word is at address+32.
All byte addresses and counters are below 2^88 and fit in one 256-bit word.
Reservation is a choice of disjoint RAM addresses, not a library allocation;
each array word is written before being read, so no clearing pass is needed.
Both arrays are nevertheless fully included in peak memory.

Order records lexicographically by unsigned digest and then unsigned message.
For two exactly equal records take the left one. A record copy copies both
words. The algorithm uses the following loops, not a library sort, hash
table, recursion, or search oracle:

    N := 1 << 80
    for i := 0,...,N-1:
        R := independent_uniform_random_256_bit_word()
        X := H(the 32-byte big-endian encoding of R)
        A[i] := (X,R)

    source := A; destination := B; width := 1
    while width < N:
        for lo := 0,2*width,4*width,...,N-2*width:
            mid := lo+width; hi := mid+width
            i := lo; j := mid; k := lo
            while k < hi:
                if i == mid: choose right
                else if j == hi: choose left
                else if source[i] <= source[j] in the stated total order:
                    choose left
                else: choose right
                if choose left:
                    destination[k] := source[i]; i := i+1
                else:
                    destination[k] := source[j]; j := j+1
                k := k+1
        swap(source,destination); width := 2*width

    for k := 1,...,N-1:
        (x,r) := source[k-1]; (y,s) := source[k]
        if x == y and r != s:
            U := 32-byte big-endian encoding of r
            V := 32-byte big-endian encoding of s
            HU := H(U); HV := H(V)
            if U != V and HU == HV: return (U,V)
            else: return failure
    return failure

N is a power of two: every run has exactly width records, every pair is
complete, and there are exactly 80 merge passes. Exponential loops are not
unrolled. Swapping source/destination exchanges pointers. All N inputs are
sampled before scanning. The algorithm stops at the first nontrivial match,
or returns failure after all N-1 adjacent pairs. There is one attempt, no
restart, and no success amplification. Verification failure is a specified
halt but Section 4 proves it is unreachable under the algorithm's semantics.

## 4. Deterministic correctness

Every generated record is (H(R),R). A merge copies the smaller available
head, or the remaining head when a run is exhausted. Induction on emitted
records proves that it preserves the input multiset and produces the sorted
union. Induction over width proves that the final source contains exactly
the N sampled records in total order, including identical repeated messages.

Each digest's records are contiguous. Within such a group, message integers
are sorted. If two message values differ, some two consecutive records lie
at a boundary between unequal values. The scan reaches such a boundary and
finds equal digests but unequal messages. Repeated copies of one message
cannot conceal that boundary. Conversely, every candidate output has unequal
32-byte encodings and equal full digest integers. H is deterministic, so
recomputation accepts. Thus success occurs exactly when two distinct sampled
messages have equal complete hashes. The algorithm returns no false collision.

## 5. Distribution-free probability proof

For each possible full digest y define p_y=|{R in D:H(R)=y}|/d. The M
nonnegative p_y sum to one; zero-probability digests are allowed. The outputs
are iid with this distribution because H is fixed and inputs are iid.
Uniform outputs are not assumed.

Let e_N(p) be the degree-N elementary symmetric polynomial on these M
coordinates. For N<=M, the probability of no repeated output is N!e_N(p):
every N-element set of outputs occurs in N! possible orders, each having
the product of its coordinate probabilities. Its maximum is attained at
p_y=1/M, as the following finite proof shows. Fixing all coordinates except
a,b writes e_N as A+(a+b)B+abC with C>=0. Averaging a,b preserves a+b and
does not decrease ab. On the compact probability simplex choose a maximizer
minimizing the sum of squared coordinates. Such extrema exist by continuity.
If two coordinates differ, averaging either increases e_N, contradicting
maximality, or preserves it while decreasing the squared sum, contradicting
the tie-break. Thus that maximizer has all coordinates equal. Consequently

    Pr[no repeated output] <= N! choose(M,N)/M^N
                           = product_{i=0}^{N-1}(1-i/M)
                           <= exp(-N(N-1)/(2M)).

The last inequality applies 1-u<=exp(-u) to each factor. That elementary
inequality follows from exp(v)>=1+v for real v. No independence of
pair-collision events is asserted.

Let E be a repeated-output event and F a repeated-input event. On E outside
F a pair of distinct inputs collides, so Section 4 gives
Pr[success]>=Pr[E]-Pr[F]. Each specified input pair is equal with probability
1/d; a union bound gives Pr[F]<=N(N-1)/(2d)<2^-97. Hence

    Pr[success] >= 1-exp(-N(N-1)/(2M))-N(N-1)/(2d).

For the exact parameters x=N(N-1)/(2M)=1/2-2^-81>499/1000. The positive
exponential series gives

    exp(x) > 1+499/1000+(499/1000)^2/2+(499/1000)^3/6
           = 9865254499/6000000000,
    exp(-x) < 6000000000/9865254499 < 609/1000.

The last strict comparison is the integer inequality
609*9865254499=6007939989891>6000000000000. Therefore
Pr[success]>391/1000-2^-97>390/1000=0.39, since 2^97>1000.
This includes repeated-input false matches, arbitrary fiber imbalance,
and every unsuccessful attempt. It is a finite statement for the exact
target, not an asymptotic or empirical extrapolation.

## 6. Time and memory ledger

All accounting is in the fixed 256-bit RAM: load/store, addition/subtraction,
bitwise operation, shift/rotation, comparison, conditional branch and fresh
uniform word each cost one. The selected compression costs one. No unit-cost
sort or arbitrary-precision arithmetic is used. Moves, address arithmetic,
loop control, argument construction and scratch accesses are charged.

Here are explicit primitive expansions bounding the pseudocode. Reading a
record needs a shift, base addition, first load, addition of 32, and second
load: at most 5 operations. Writing uses the analogous 5. A total-order
test needs at most 3 comparisons and 3 branches: 6. A register assignment
can use a load and store (2 operations). A two-word move between register
pairs therefore costs at most 4. Counter increments take one addition;
each loop test takes a comparison and branch. All unconditional control
transfers are also charged one branch, implementable as a branch on true.

Generation costs at most 128 per message: one random draw, at most 16 for
the two block words and IV arguments, one compression, at most 32 for
masking/packing the five output words, 5 for writing the record, and at most
32 for counter control, call/return, and scratch moves. In particular there
is no hidden byte conversion: R is the first block word and the second is
a constant. Packing a digest uses four shifts and four ORs plus loads/masks.
These allowances sum to 87, below 128. All N trials, successful or not, count.

For each merge emission allow at most 10 for two head reads, 6 for the
total-order test, 4 for exhaustion comparisons/branches, 5 for the record
write, and 39 for choosing a side, index updates, temporary moves, loop
test, and jumps. This sums to 64; conservatively charge 96. Exhausted
paths read only valid heads. Initializing/advancing each pair of runs costs
at most 32; pass pointer/width setup and exit cost at most 32. There are
N emitted records and at most N/2 run pairs in a pass, so

    cost per pass <= 96N+32(N/2)+32 <= 128N.

Both arrays' entire contents are overwritten every pass before becoming the
next source. No extra full-array copy occurs. There are 80 passes.

A scan iteration costs at most 10 for adjacent record reads, 4 for equality
and distinctness comparisons/branches, and 32 for index/address scratch,
updates, control, and return checks. Charge 64N for the entire scan.
At most one final verification occurs; charge 256 for its two block
preparations, two complete hashes, full comparisons, and two 32-byte
output writes. Even early success was charged the whole scan.

Program storage is finite uniform code, not omitted advice. An explicit
encoding uses at most four 256-bit words per primitive instruction: opcode
plus up to three operands, including an immediate or branch destination.
Unary operations/load/store/branch fit in this format; binary operations
use result and two arguments. Lower Sections 2 and 3 with fixed registers,
scratch addresses, and counted loops. There are fewer than 256 elementary
assignment, test, loop-control, and action statements after splitting the
displayed tuple updates and compound expressions at their arithmetic
operators. Each stated record access or comparator macro takes fewer than
16 primitive instructions by the expansions above; the split hash statements
and loop scaffolding also fit that bound. Thus at most 4096 instruction
records suffice, including the looped hash specification even though its
evaluation is a selected primitive. They occupy at most
4096*4*32=2^19 bytes. There is no unrolling over N or table of answers.

Fewer than 256 data words suffice for constants, the 79 schedule words,
hash working state, record temporaries, pointers, counters, padding,
verification inputs/outputs, and flags. Reserving another 2^16 bytes for
them and instruction scratch is conservative. Code and all fixed state
therefore fit strictly within 2^20 bytes. Charge at most 2^20 operations
for writing/copying this finite code, constants and scratch and setting the
array base addresses. The program and fixed constants are specified above;
there is no target-dependent search, precomputed collision, external advice,
or hidden dataset. This initialization is the entire preprocessing phase.
The two table regions need no initial writes because every read follows a
write, as specified in Section 3.

Total worst-case time, including initialization and verification, is

    T <= 2^20 + 128N + 80*128N + 64N + 256
       = 10432N+2^20+256
       < 16384N = 2^94.

Both N-record arrays together occupy 128N=2^87 bytes. No recursion stack,
third array, separate message list, or extra random tape is used. The
message fields are the retained random choices. Including code, constants,
all scratch, and the two output messages, peak allocated memory is

    S < 2^87+2^20 < 2^88 bytes.

## 7. Evidence scope

All material claims are the specified algorithm, exact target, finite
counting argument and explicit conservative ledger. The heuristics array
is empty: no cryptanalytic, uniform-output, statistical-independence or
extrapolation premise is used beyond the organizer's defined computation
model. Replacing ideal random words with a deterministic PRNG would require
a different probability argument. Each ideal word here is charged.

The empty certificate manifest is intentional. No full-scale collision
search has been executed and no stored collision is used as advice. No
experiment manifest is declared: this analytic argument does not rely on
empirical support, and toy or seeded experiments cannot establish a
full-scale randomness premise. The enormous memory bound is not a claim
of practical feasibility.
