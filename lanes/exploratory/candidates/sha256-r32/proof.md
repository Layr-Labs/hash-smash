# Seven-way packed SHA-256 birthday construction

## Contract and scope

This is an analytic algorithm for sha256-r32-prefix-v1, ordinary collisions,
exploratory lane, collision-frontier-v5. Its claimed time bound is 127.96,
memory bound 199, and success lower bound 0.39. No collision has been computed.
Readiness requests review and is not acceptance. The nominal reference identifier
is metadata, not evidence. The improvement is in the specified classical
256-bit RAM cost model, not a structural cryptanalytic weakness of SHA-256.

We reuse the two-level validated direct-address dictionary idea described in
cadamcat's public submission 3458d67 (unpromoted when read), and credit that
contribution. This package extends our r31 submission 66f9b527 to 32 rounds, with a fresh
resource calculation. Its AI review is not evidence for this target.
The principal component is a seven-way exact packed implementation of
the target, with explicit costs including instruction and scratch traffic.
No random-oracle, differential, or empirical-extrapolation heuristic is used.

## 1. Messages and target

Let n = ceil(9943*2^128/10000), D=2^320, N=2^256, B=ceil(n/7).
Every actual sample draws independent uniform 256-bit words x,z, takes
 y=z AND (2^64-1), and uses m=BE_32(x)||BE_8(y). This is uniform on D
40-byte messages, injectively represented by (x,y). Discarded random bits are
not reused. Sample exactly n messages, with at most six dummy lanes in the
last batch; dummy lanes are never inserted in the dictionary.

Padding produces one block with message words W[0..9], W[10]=0x80000000,
W[11..14]=0, and W[15]=320. Parse all words big-endian. The standard IV is
6a09e667 bb67ae85 3c6ef372 a54ff53a 510e527f 9b05688c 1f83d9ab 5be0cd19.
Execute rounds 0..31, original constants and expansion, then add the IV
componentwise modulo 2^32 and concatenate all eight words big-endian.

The constants K[0],...,K[31] are, in hexadecimal and original index order,

    428a2f98 71374491 b5c0fbcf e9b5dba5 3956c25b 59f111f1 923f82a4 ab1c5ed5
    d807aa98 12835b01 243185be 550c7dc3 72be5d74 80deb1fe 9bdc06a7 c19bf174
    e49b69c1 efbe4786 0fc19dc6 240ca1cc 2de92c6f 4a7484aa 5cb0a9dc 76f988da
    983e5152 a831c66d b00327c8 bf597fc7 c6e00bf3 d5a79147 06ca6351 14292967


Define ror32, small sigma0=(ror7 XOR ror18 XOR shr3), small sigma1=
(ror17 XOR ror19 XOR shr10), big Sigma0=(ror2 XOR ror13 XOR ror22),
big Sigma1=(ror6 XOR ror11 XOR ror25). Expand W[t]=W[t-16]+sigma0(W[t-15])
+W[t-7]+sigma1(W[t-2]) modulo 2^32 for t=16..31. Each round uses
T1=h+Sigma1(e)+Ch(e,f,g)+K[t]+W[t], T2=Sigma0(a)+Maj(a,b,c), and replaces
(a,b,c,d,e,f,g,h) with (T1+T2,a,b,c,d+T1,e,f,g), reducing new a,e modulo
2^32. Ch=g XOR (e AND (f XOR g)); Maj=(a AND b) XOR (c AND (a XOR b)).
These Boolean forms equal the standard functions bit by bit.

## 2. Exact packed implementation

For seven lanes define P(v)=sum(v_j*2^(36*j),j=0..6), with 32-bit v_j.
Let broadcast(v)=sum(v*2^(36*j),j=0..6), M=broadcast(2^32-1).
All operations below are permitted 256-bit word operations. Define

    R(X,r) = ((X >> r) AND broadcast(2^(32-r)-1))
           OR ((X << (32-r)) AND broadcast(2^32-2^(32-r)))
    S(X,r) = (X >> r) AND broadcast(2^(32-r)-1)

R costs five primitive algebra operations, S costs two. Masks are fixed
constants constructed during preprocessing. BOTH masks in R are essential:
four guard bits alone do not prevent cross-lane shift contamination.
In each retained lane, the first term selects its own upper 32-r bits and
the second selects its own lower r bits shifted upward. All bits moved from
adjacent lanes are excluded by their respective masks. Thus R is exactly
seven independent 32-bit rotations and S exactly seven logical shifts.
Bitwise functions preserve packing. Addition of at most seven 32-bit lane
values has lane sum <7*2^32<2^35, so it never carries into the next lane at
bit 36. AND M reduces every lane modulo 2^32. The highest used sum bit is
at most 250, below 256; global modular addition therefore loses no needed bit.

The following straight-line program is expanded at construction time for
fixed t. Its instruction stream is fixed, finite and explicitly charged.

    packed_sigma0(X) = R(X,7) XOR R(X,18) XOR S(X,3)
    packed_sigma1(X) = R(X,17) XOR R(X,19) XOR S(X,10)
    packed_Sigma0(X) = R(X,2) XOR R(X,13) XOR R(X,22)
    packed_Sigma1(X) = R(X,6) XOR R(X,11) XOR R(X,25)
    W[t] = (W[t-16]+packed_sigma0(W[t-15])+W[t-7]
             +packed_sigma1(W[t-2])) AND M       # t=16..31
    (a,b,c,d,e,f,g,h) = broadcast(IV[0..7])
    T1 = h+packed_Sigma1(e)+(g XOR (e AND (f XOR g)))+broadcast(K[t])+W[t]
    T2 = packed_Sigma0(a)+((a AND b) XOR (c AND (a XOR b)))
    new_a = (T1+T2) AND M
    new_e = (d+T1) AND M
    (a,b,c,d,e,f,g,h) = (new_a,a,b,c,new_e,e,f,g)
    output[k] = (state[k]+broadcast(IV[k])) AND M

T1 is deliberately not masked: it is a sum of five canonical lanes; T2
is a sum of two. Their seven-term sum obeys the guard-bit bound above.
After each round all eight state words are again canonical. Register names
in the displayed simultaneous assignment are compile-time aliases: the two
new values overwrite dead old h,d scratch slots. No runtime permutation or
free memory copy is assumed. W and temporary operands occupy fixed scratch
addresses; all operand traffic is included below.

An induction on expansion index and round index proves each output lane is
exactly the target digest on its corresponding padded message. Output packing
into one 256-bit digest per lane preserves all eight words, in order.

## 3. Exact collision dictionary

Let S1 reserve 2^192 word cells with arbitrary initial contents. Let S2 reserve
n*2^64 word cells, grouped into n blocks of 2^64 cells. Let Keys reserve n
words and Records reserve n triples (digest,x,y). Initialize c=r=0 only.
These arrays are disjoint. All pointers and byte addresses are below 2^199.
No array is assumed zero and no virtual-memory or operating-system facility
is assumed. For each real lane, use this algorithm, where each array access
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
measured randomness or experimental extrapolation. Dummy lanes do not enter
this argument. There are no restarts, hidden trials, or advice.

## 5. Charged implementation and operation counts

Every algebra, comparison, branch, assignment, or explicit memory access in
the RAM pseudocode is called a core instruction here. Use a finite program
with scratch addresses under 2^16 words. Each instruction encodes opcode and
at most three scratch/immediate-address operands in one 256-bit code word.
Large table addresses are values in scratch, not in the instruction encoding.
A binary algebra instruction is conservatively charged five primitive costs:
one code load, two scratch loads, the operation, and one scratch store.
An indirect memory instruction uses code load, pointer scratch load, data
load/store and destination/source scratch access, at most five too. A branch
uses at most the same allowance. Literal constants occupy initialized scratch.
All data address calculations are separate core instructions; they are not
hidden inside a free array-access primitive. Finite instruction sequencing is
ordinary RAM control, not a simulated general-purpose interpreter. No code
fetch is free. Fixed register renaming means fixed addresses in the emitted
instruction stream, not runtime assignments.

### Packed core

A big Sigma costs 3*5+2=17 core instructions; a small sigma costs 2*5+2+2=14.
An ordinary expanded schedule word costs 14+14+3 additions+1 mask=32.
A round costs 17+17+3 for Ch+4 for Maj+4 for T1+1 for T2+2 for new_a+
2 for new_e=50. Feed-forward costs 16. Before constant folding the total is
16*32+32*50+16=2128 core instructions for seven messages.

We use only these specified constant folds, all justified by fixed IV/padding:
* Round 0: all state functions are constant; T1=constant+W[0], new_a and
  new_e each need an add and mask. Cost 5 instead of 50, saving 45.
* W[16]: sigma1(W[14])=0, saving 14 sigma instructions and one addition: 15.
* W[17]: sigma1(W[15]) is a preprocessing constant, saving 14.
* W[25..30]: their sigma0 inputs are W[10..15], all fixed; save 6*14=84.
No other savings are required. Core total is 2128-45-15-14-84=1970.
The partial-sum guard argument also covers the constant-folded expressions.

### Per-lane wrapper: at most 80 core instructions

Two random draws and masking z cost 3. Retaining (x,y) in fixed batch scratch
costs 2. Extracting x's eight 32-bit words costs at most 15 shift/mask operations,
and y's two words at most 3. Inserting the ten words into their zeroed packed
W slots costs at most 20 shifts/ORs. After compression, extracting the eight
words costs 16 shifts/masks and combining them into a digest costs 14
shifts/ORs. Sum: 3+2+15+3+20+16+14=73. Seven additional core instructions
cover sample counter increment, bound comparison/branch, fixed-lane dispatch,
and loading the saved message pair. The seven lane bodies are statically
unrolled; shifts are constants. All operations cost at most five including
scratch traffic. Final unused lanes are initialized to fixed zero messages.

### Dictionary: at most 60 core instructions per real sample

Count even mutually exclusive insertion/hit branches together:

| Phase | Core instruction cap |
| --- | ---: |
| Split digest, form S1 address, load j | 4 |
| Range test/branch, Keys address/load, equality test/branch | 6 |
| New-prefix path: copy c, Keys and S1 stores, c increment | 6 |
| S2 block shift, two additions, load candidate k | 4 |
| Range test/branch, triple address by three additions, digest load/compare/branch | 8 |
| Two message field addresses/loads, comparisons and branches | 8 |
| New triple address, three stores with two field offsets, S2 store, r increment | 10 |
| Validity flag/control transfers and remaining fixed bookkeeping | 14 |
| Total | 60 |

The one-time final verification/output is charged separately. Prefix count and
record count never exceed n. An arbitrary failed lookup is fully covered by
the combined path budget; no expected-time dictionary premise is used.

### Fixed per-batch and global work

Allow 70 further core instructions per batch for clearing 16 packed W slots,
loading 8 initial state constants, setting the padding constants, clearing
fixed lane buffers and batch controls. Only W[0..9] and actual saved message
slots need clearing/initialization; output and expanded schedule scratch are
written before read. With static lane bodies and constant addresses, the 70
cap covers these at most 40 initializations and at most 30 loop/counter/exit
instructions. All real or dummy lanes receive the full 80+60 budget, so the
last batch's partial handling is covered without an uncharged exceptional path.

Total charged ordinary operations per batch are therefore at most

    5*(1970 + 70 + 7*(80+60)) = 15100.

The straight-line core uses fewer than 4096 code words; wrapper/dictionary
unrolling, controls and setup keep the whole program below 2^16 words.
Code and fixed scratch together require fewer than 2^23 bytes. Constructing
all constants, masks and the finite program, loading them, and setting up
base addresses uses fewer than 2^24 ordinary operations (simple bounded loops
suffice). Preprocessing is bounded by 2^14 target-compression units and is
included in total time. No candidate collision is stored as advice.

Verify the one output pair, if present, by two ordinary complete one-block
32-round target compressions, full digest equality, message inequality and
output serialization. Charge two compression units plus a further 2^24 ordinary
operations; this deliberately large allowance covers all scratch and control.
Thus total cost on every random tape, including failed runs, is

    T <= (15100*ceil(n/7) + 2^25)/2224 + 2
      < 2^127.96.

For an easy loose check, n < 0.994301*2^128, so the coefficient of 2^128
is less than (15100/15568)*0.994301 < 0.965, whereas 2^-0.04 > 0.972.
The additive constants are far smaller than the remaining 0.007*2^128.
The implementation uses elementary operations instead of a compression oracle
for batched evaluation. It does not count seven compression calls and then
also charge their internals: only actual word operations are charged, each
at 1/2224. The two final oracle calls are charged in addition. This is an
implementation optimization inside the published computation model, not a
change to the hash, round count, or target price.

## 6. Memory and limitations

S1 occupies 2^192 words; S2 occupies n*2^64 <2^192 words. Keys and Records
occupy 4n words. Code, fixed scratch, masks and output require <2^23 bytes.
Consequently total memory is <2^199 bytes. All table word and byte addresses
fit in 256 bits, as do counters and shifts j<<64. Arrays are reserved but
not cleared; their arbitrary initial contents are handled by the proven
validation invariant. No demand-zero pages, sparse virtual memory, memory
allocation oracle, or free backing storage is assumed. All reserved storage,
including untouched cells, counts in this memory bound. Array base reservation
is assigning disjoint address intervals, not touching each cell.

There is zero nonuniform advice; the schema's log2 advice value 0 is a
one-byte upper bound. No experiment manifest is requested and the empty
certificate manifest does not certify a witness. This is an analytic
construction at infeasible scale. No local evaluation or participant program
was run. Its algebra, probability and resource argument require review;
AI qualification is not mathematical proof, manual acceptance or promotion.
