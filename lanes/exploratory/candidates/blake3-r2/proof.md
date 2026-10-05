# Exact finite birthday construction: blake3-r2

This package selects blake3-r2-prefix-v1, ordinary-collision, exploratory lane,
and collision-frontier-v5. It proposes time_log2 129.52, memory_log2_bytes 199,
preprocessing_log2 14 and success_probability 0.39. It is an analytic algorithm,
not a computed collision. No local benchmark or candidate was executed.
Readiness requests review; it is not AI qualification, human acceptance or promotion.

The two-level validated direct-address idea is credited to cadamcat's unpromoted
public SHA-256 submission 3458d67. The full invariant and accounting appear here;
that submission's verdict does not establish this target's correctness. The
construction is generic and uses no random-oracle, output-balance or differential
heuristic. It is not claimed to beat all competing pending submissions.

## Sampling and stopping rule

Set n=ceil(9943*2^128/10000), D=2^320, N=2^256. In one finite run sample
exactly n independent messages unless a verified collision is found earlier.
Each sample draws fresh independent uniform 256-bit words x,z, sets
y=z AND (2^64-1), and forms LE_32(x)||LE_8(y). This is an injective encoding
of independent uniform 320-bit messages. No seeded expansion is substituted.
Evaluate the complete target below, producing a full 256-bit digest integer,
and process it using the exact dictionary in section 3. Return a distinct
pair only after rehashing both complete messages and comparing full digests.
If no collision is found, return FAIL. No restart or uncharged amplification.
All time bounds charge every sample on failed runs too.

## Complete target evaluation

Messages are LE_32(x)||LE_8(y), exactly 40 bytes. They form one chunk and
one block. Zero-fill bytes 40..63 for word loading only; the true block
length remains 40. Load the 16 message words little-endian. The chaining
value is the standard IV, counter is zero, and flags are 11 = CHUNK_START
OR CHUNK_END OR ROOT. Invoke one 2-round root compression directly on this
message descriptor. Do not first finalize a chunk CV and rehash it. No
parent compression is needed because this is a one-block, one-chunk message.

IV in hexadecimal is 6a09e667 bb67ae85 3c6ef372 a54ff53a 510e527f 9b05688c
1f83d9ab 5be0cd19. Initialize v=IV||IV[0..3]||(0,0,40,11). A G call on
positions (a,b,c,d) with message operands X,Y executes, modulo 2^32:

    a=a+b+X; d=ROR32(d XOR a,16)
    c=c+d; b=ROR32(b XOR c,12)
    a=a+b+Y; d=ROR32(d XOR a,8)
    c=c+d; b=ROR32(b XOR c,7)

Each round calls G on (0,4,8,12),(1,5,9,13),(2,6,10,14),(3,7,11,15),
then (0,5,10,15),(1,6,11,12),(2,7,8,13),(3,4,9,14), with consecutive
message pairs m[0..15] in that order. Between the two rounds, permute m by
indices (2,6,3,10,7,0,4,13,1,11,12,5,9,14,15,8). Execute rounds 0 and 1.
Compression output is v[i] XOR v[i+8] for i=0..7 followed by v[i+8] XOR
input_cv[i] for i=0..7. Return the first eight words, serialized little-endian,
which are all 256 target output bits. The supplied compression primitive
includes this feed-forward. Its unused last eight output words are not hashed
again or used as a replacement root CV.

## 3. Exact collision dictionary

Let S1 reserve 2^192 word cells with arbitrary initial contents. Let S2 reserve
n*2^64 word cells, grouped into n blocks of 2^64 cells. Let Keys reserve n
words and Records reserve n triples (digest,x,y). Initialize c=r=0 only.
These arrays are disjoint. All pointers and byte addresses are below 2^199.
No array is assumed zero and no virtual-memory or operating-system facility
is assumed. For each sample, use this algorithm, where each array access
is expanded into address arithmetic followed by an ordinary load/store:

    p = digest >> 64; lo = digest AND (2^64-1)
    j = S1[p]
    valid_prefix = false
    if j < c:
        if Keys[j] == p: valid_prefix = true
    if not valid_prefix:
        j = c; Keys[j] = p; S1[p] = j; c = c+1
    u = base_S2 + (j << 64) + lo
    k = memory[u]
    if k < r:
        a = base_Records + k+k+k
        if memory[a] == digest:
            if memory[a+1] != x or memory[a+2] != y:
                verify both complete target hashes and return the two messages
            else:
                continue to next real sample
    a = base_Records + r+r+r
    memory[a] = digest; memory[a+1] = x; memory[a+2] = y
    memory[u] = r; r = r+1

Only Keys[0..c) and Records[0..r) are read. S1 and S2 may contain arbitrary
words, but they are merely candidate indices. An uninserted prefix cannot pass
validation because every initialized Keys entry belongs to an inserted prefix.
An inserted prefix retains its correct S1 pointer forever. Within that prefix,
an uninserted digest cannot pass validation against an initialized record,
since record digests are exactly previously inserted distinct digests. An
inserted digest retains its S2 pointer forever. These invariants follow by
induction from empty initialized dense prefixes. A new block need not be cleared.
The full digest comparison also prevents arbitrary S2 words from confusing
prefixes. Thus the algorithm finds a distinct-message collision whenever one
exists in the n samples. Duplicate identical messages are ignored without
removing the first record. Stop after n samples if none is found. All bounds
charge the full batch budget even on early success or on failure.


## 4. Distribution-free success bound

For the fixed target let p_z be its digest probabilities on uniform 40-byte
messages. Independent messages give independent outputs distributed as p;
no uniformity of p is assumed. For elementary symmetric polynomial e_n,
Pr(no equal digest)=n!e_n(p). This is maximized by uniform p on N values.
Here is a proof: among maximizers on the compact probability simplex choose
one minimizing sum p_z^2. For coordinates a,b and remaining vector v,
e_n(p)=e_n(v)+(a+b)e_(n-1)(v)+ab e_(n-2)(v). Averaging unequal a,b
cannot decrease this expression, since coefficients are nonnegative, and
strictly decreases sum p_z^2. This contradicts that choice of maximizer.
The maximizing vector is therefore uniform. Consequently

    Pr(equal digest) >= 1-exp(-n(n-1)/(2N)).

The chance any input repeats is at most n(n-1)/(2D). Subtracting this event
without assuming independence gives

    Pr(success) >= 1-exp(-n(n-1)/2^257)-n(n-1)/2^321.

Our n gives the first exponent greater than 0.4943 and the subtraction less
than 2^-64. An entirely rational lower certification uses
exp(0.4943) > sum((4943/10000)^j/j!, j=0..8) > 1000000/609999.
Thus success > 0.390001-2^-64 > 0.39. The finite polynomial inequality is
an integer-arithmetic statement after multiplying by 10000^8*8!; it uses no
measured randomness or experimental extrapolation. There are no restarts, hidden trials, or advice.


## 5. Fully charged implementation

A complete sampled target evaluation costs one selected compression/permutation
unit as established above. Its internal round work is not charged a second time.
All other primitive 256-bit word operations cost 1/430 units. The attack pays
message preparation, interface transfers, dictionary work, program/scratch
traffic, loop control, randomness, verification and preprocessing.

Use a fixed program with all scalar scratch and constants within 2^16 words.
Each core instruction has opcode and up to three scratch-address operands in
one 256-bit code word. A binary arithmetic/Boolean instruction costs at most
five primitive operations: code load, two operand loads, operation and result
store. Indirect memory accesses and branches also fit five. Table address
calculations are separate instructions. Constants occupy initialized scratch.
Ordinary finite RAM instruction sequencing is not a simulated interpreter.

The complete per-sample wrapper is capped at 100 core instructions. It includes
three instructions for fresh draws and masking, message retention, unpacking
into primitive input words, initialization of the fixed state and padding or
flags, primitive dispatch/interface, output packing and loop/counter control.
For SHA3, unpack four 64-bit slices in at most seven shift/mask operations;
25 state stores, two saved-message stores, six output shifts/ORs and eight
interface/control instructions together with the three draws/mask use at most
51 core instructions. For BLAKE3, ten input words require at most 18 shift/mask
operations, 16 message-word stores, eight IV transfers, three control-parameter
transfers, two saved-message stores, 14 digest shifts/ORs, and eight interface/
loop instructions, together with three draws/mask, use at most 72. Extra result
loads if an interface uses memory rather than fixed scratch fit the remaining
28 instructions. Thus the same cap covers the selected target. Only the
selected wrapper is used, not both. No host-language object overhead is presumed.

The dictionary uses at most 60 core instructions per sample, counting both
hit and insertion paths even though not all execute:

| Phase | Core cap |
| --- | ---: |
| Split digest, S1 address and load | 4 |
| Range check, Keys address/load and equality check | 6 |
| New prefix assignments, stores and count | 6 |
| S2 block address and candidate index load | 4 |
| Record range test, triple address, digest load/test | 8 |
| Message addresses, loads, comparisons and branches | 8 |
| Insert record, field offsets, stores and count | 10 |
| Flags, control transfers and fixed bookkeeping | 14 |

Together ordinary per-sample work is at most 5*(100+60)=800 operations.
There are no unbounded strings, expected probing costs, or free address
calculations. All pointer and counter arithmetic fits in a single word.

Code, masks, constants, output and scratch occupy less than 2^23 bytes.
Constructing/loading this finite program, setting constants and base addresses,
and initializing fixed scratch uses fewer than 2^24 ordinary operations.
Only c and r initialize the large dictionary: arbitrary table words are
validated against initialized dense prefixes. There is no large clearing pass.
The preprocessing cost 2^24/430 is below 2^14 target units for this C and
is included in total time. No collision, search output or uncharged advice is
stored in the program. The advice exponent zero represents a one-byte upper
bound on zero actual advice.

One-time successful-output verification costs two complete target evaluations,
plus at most 2^24 ordinary operations for message rereading, interface, equality
checks and output. Hence, on every random tape,

    H <= n+2, W <= 800*n+2^25
    T <= n+2+(800*n+2^25)/430 < 2^129.52.

Memory is the full reserved address footprint: S1 uses 2^192 words; S2 uses
n*2^64<2^192 words; Keys and Records use 4n words. Code/scratch and output
are lower-order. Total is below 2^199 bytes and all addresses fit in 256 bits.
Untouched cells count in full. The model does not charge scalar time merely
for reserving disjoint address ranges; every actual read/write is charged.
No virtual-memory allocator, zero-page service or hidden external storage is used.

## 6. Limitations and evidence

The package supplies analytic evidence, not an executed full-scale attack.
The probability lower bound is distribution-free for the fixed hash. Memory
is physically infeasible. No heuristic, experimental extrapolation, certificate
witness, or claimed differential weakness is needed. The certificate manifest
is valid and empty. No experiment manifest is requested. The target-specific
wrapper, dictionary invariant and cost argument remain subject to substantive
review. An exploratory score is not proof, human acceptance, or publication.
The required nominal reference identifier does not assert an accepted baseline.
