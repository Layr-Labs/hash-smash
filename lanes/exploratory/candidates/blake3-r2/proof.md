# A 0.39-success fixed-function collision search for 2-round BLAKE3

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains
a separately reported resource bound.

This independent exploratory package targets blake3-r2-prefix-v1. It proposes
a classical randomized algorithm with success above 0.39, total charged time
at most 2^134 units, and peak memory at most 2^136 bytes under
collision-frontier-v5. These are conservative analytical upper bounds, not
measured execution costs. The claimed scalar is 134. Relative to the promoted
generic package, the research hypothesis is that the required 0.39 success
threshold permits 2^128 samples, and fixed-width radix sorting removes the
129-pass merge-sort cost. Neither change assumes random hash outputs.

The construction uses the promoted generic-birthday package's full-target hash
definition and independent-input sampling. The sample count, sorting program,
success calculation and charged work bound below are new for this package.
One selected 2-round compression costs 1; every other listed 256-bit RAM
primitive costs 1/C with C=430. The nominal display exponent 128 is not used
as a qualified baseline.

The proof uses no distributional property of the selected hash: every fixed function from
the chosen message domain to 256-bit strings satisfies its probability bound.
Fresh independent uniform coins are the explicit RAM model's random-word
primitive. No PRNG, random-oracle, round-independence, or differential heuristic
is assumed. Accordingly the heuristic list is empty.

## 1. Exact complete hash

Each message is exactly 64 bytes, of bit length 512 < 2^64. Two 256-bit words
u,v encode m=LE32(u)||LE32(v), where LE32 includes all 32 little-endian bytes,
including zeros. These encodings bijectively cover a domain D of size 2^512.
There is no unknown IV, free-start state, or supplied prefix/advice.

H is unkeyed BLAKE3-256 with 2 prefix rounds in every compression.
On these exactly 64-byte messages there is one chunk, one full block, no parent,
and exactly one compression with CHUNK_START | CHUNK_END | ROOT = 11.
There is no extra padding block, key, or derivation flag. The true block length
is 64 and both the chunk index and root-output counter are zero.

Decode m into sixteen little-endian 32-bit words w[0..15]. The eight-word IV is

    6a09e667 bb67ae85 3c6ef372 a54ff53a
    510e527f 9b05688c 1f83d9ab 5be0cd19.

Initialize v[0..7]=IV, v[8..11]=IV[0..3], and
v[12..15]=(0,0,64,11). All arithmetic additions below are modulo 2^32;
ROR rotates right within a 32-bit lane. Define G(a,b,c,d,x,y) on v by

    v[a] = v[a]+v[b]+x; v[d] = ROR(v[d] XOR v[a],16)
    v[c] = v[c]+v[d];   v[b] = ROR(v[b] XOR v[c],12)
    v[a] = v[a]+v[b]+y; v[d] = ROR(v[d] XOR v[a],8)
    v[c] = v[c]+v[d];   v[b] = ROR(v[b] XOR v[c],7).

For each round, use the current message schedule s, initially w, and call

    G(0,4,8,12,s[0],s[1]);    G(1,5,9,13,s[2],s[3])
    G(2,6,10,14,s[4],s[5]);   G(3,7,11,15,s[6],s[7])
    G(0,5,10,15,s[8],s[9]);   G(1,6,11,12,s[10],s[11])
    G(2,7,8,13,s[12],s[13]);  G(3,4,9,14,s[14],s[15]).

Between rounds replace s by s[P[i]], where
P=(2,6,3,10,7,0,4,13,1,11,12,5,9,14,15,8).
Execute exactly the first 2 rounds, with no later rounds. The full
compression output is o[i]=v[i] XOR v[i+8], and
o[i+8]=v[i+8] XOR IV[i], for i=0..7. The digest H(m) is
LE4(o[0]) || ... || LE4(o[7]), the first 32 root-output bytes.
This retains the ordinary hash's flags and feed-forward, rather than searching
for a collision of a free-start or non-root compression function.

The target profile permits other message lengths and preserves the complete
standard 1024-byte chunk tree, parent nodes, counters and root output, with the
same prefix reduction in every compression. This algorithm only generates
64-byte messages, so the one-root-compression description covers every hash
it evaluates, including final verification. No uncharged parent, chunk or
second root-output compression is needed on this domain.

## 2. Algorithm and representation

Set n=2^128. A record is three 256-bit words (h,u,v), with h the little-endian
integer encoding of H(LE32(u)||LE32(v)). Unsigned comparison of h is a total
order whose equality is full digest equality. Use two flat arrays A and B,
each of n records, and one counter array D of 2^64 256-bit words. Explicitly
initialize all six record words per index across the two arrays; allocation,
counter initialization and prefix-sum work are charged.

1. For i=0,...,n-1, draw fresh independent uniform 256-bit words u and v,
   construct their 64-byte message, compute its complete H, and store
   (h,u,v) in A[i]. Retain repeated inputs; there is no resampling.
2. Sort by full h using four stable least-significant-digit counting-sort
   passes. Pass p=0,1,2,3 extracts digit d=(h>>(64p)) AND (2^64-1).
   Zero all 2^64 counters, count each source record by digit, then replace
   D[d] with the exclusive prefix sum of the original counts up to d.
   Scan source records in increasing index order: write each complete
   (h,u,v) record to destination position D[d], then increment D[d].
   Exchange the A and B base pointers after the pass. Each pass reads and
   writes n records and traverses the counter array twice. No comparison
   sort, sparse-table assumption or uncharged allocation is used.
3. Scan all adjacent positions j-1,j in the sorted source array, from j=1
   through n-1. Test h equality and inequality of the pair (u,v), testing
   both message words. On the first qualifying pair, reconstruct both
   messages and recompute both complete hashes from the all-zero state.
   Check message distinctness and equality of all 256 recomputed output
   bits. Return the two messages if verified; otherwise halt with failure.
4. If the scan finishes without such a pair, halt with failure.

There is one batch, no restart, and at most one final verification of two
messages. Verification failure cannot occur in the exact RAM model because
the original digests came from the same deterministic H. This explicit
defensive check is still charged. Every outcome halts within the same budget.

For the prefix scan, keep a one-word sum s initially zero; for each
d=0,...,2^64-1, load c=D[d], store s in D[d], then set s=s+c.
At the end s=n. During scatter, the counter at D[d] is the next free
destination index in that digit's interval. Stability follows because source
indices are scanned in order and each counter advances by one. After pass p,
the records are ordered by the low 64(p+1) bits of h; induction gives full
256-bit order after pass 3. There is no recursive stack or library sort.

Record i starts at byte address base+96i, calculated as
base+(i<<6)+(i<<5), without multiplication. Word offsets are 0,32,64.
Indices, counters, sentinels, run boundaries and byte addresses are less than
2^137, far below 2^256. The value n is made by 1<<128. Message contents occupy
two words; no 512-bit single-word arithmetic is assumed. The proof's symbolic
domain/codomain cardinalities need not be represented in the machine.

## 3. Correctness of any returned collision

The counting-sort scatter writes each record exactly once to a unique index
in its digit interval. Copying complete records preserves each digest's
associated message. Stable passes from low to high digits therefore sort all
original records by their full 256-bit key without deleting any.

Every fixed digest occupies a contiguous interval in the sorted array. If
that interval contains distinct messages, some adjacent messages differ:
otherwise equality of every adjacent pair would make the entire interval
one repeated message by transitivity. Thus the scan finds a distinct-message
collision whenever the sample contains one, including samples with repeated
inputs. Repeated inputs alone are never accepted as collisions.

Every returned message is in the profile's allowed domain. The explicit final
checks establish inequality of the messages and equality of the entire
complete-message hash from Section 1. This is an ordinary collision, not a
compression-only, free-start, raw-permutation, truncated-output, or
different-round result.

## 4. Success for every fixed function

The sole probability space consists of 2n independent uniform 256-bit words
drawn in Step 1. Hence the messages M_1,...,M_n are independent uniform samples
from D. For fixed deterministic H, the Y_i=H(M_i) are iid with probabilities

    p_y = |{m in D : H(m)=y}| / 2^512.

There are Q=2^256 possible output strings, including any with probability zero.
These probabilities may be arbitrarily nonuniform. Independence here follows
from applying a fixed function separately to independent inputs, not from
assuming independent internal rounds or assuming a randomly chosen hash.

For any probability vector p of length Q, let e_n(p) denote the sum of products
of n distinct coordinates. Independence gives

    Pr[all Y_i distinct] = n! e_n(p).

For completeness, uniform p maximizes e_n. A maximum exists by continuity on
the compact simplex. Among maximizers choose one minimizing the sum of squared
coordinates. If coordinates a,b differ, average them. With other coordinates
r fixed,

    e_n(p) = ab e_(n-2)(r) + (a+b)e_(n-1)(r) + e_n(r).

All coefficients are nonnegative. Averaging cannot decrease e_n, so it remains
maximal, while the sum of squared coordinates strictly decreases. This
contradicts the choice. The maximizing vector is therefore uniform, and

    Pr[all Y_i distinct]
      <= Q(Q-1)...(Q-n+1)/Q^n
       = product_(j=0,...,n-1) (1-j/Q)
      <= exp(-n(n-1)/(2Q))
       = exp(-(1/2-2^-129)).

Here n<Q and 1-t<=exp(-t) on 0<=t<1, obtained by integrating the derivative
-1/(1-t)<=-1 of log(1-t). This also covers distributions with small support.

Let E be the event that some input messages repeat. The union bound gives

    Pr[E] <= n(n-1)/(2|D|) < 2^256/(2*2^512) = 2^-257.

No independence of the pair-events is required. If outputs collide and E
does not occur, the algorithm succeeds. Thus

    Pr[success] >= 1 - Pr[all Y_i distinct] - Pr[E]
                > 1 - exp(-(1/2-2^-129)) - 2^-257
                > 0.39.

For an explicit rational margin, 1/2-2^-129 > 499/1000. The first four
nonnegative terms of the exponential series give
exp(499/1000) > 1+499/1000+(499/1000)^2/2+(499/1000)^3/6
> 1000/609, so exp(-(1/2-2^-129)) < 609/1000. Also
2^-257 < 1/10000. Hence the success bound exceeds
1-609/1000-1/10000 = 0.3909 > 0.39.
This bound proves the declared 0.39. Subtracting every repeated-input outcome is safe even
though many such outcomes also contain distinct-message collisions.
The number concerns algorithmic success, not confidence in a proof or review.

## 5. Fully charged RAM implementation

One 256-bit word is 32 bytes. Each selected compression costs one unit; every other listed RAM
primitive costs 1/C units, where C=430. All bounds include
message construction, failed samples, randomness, memory initialization,
sorting, verification, and fixed code/constants. There is no external disk,
unaccounted preprocessing service, whole-hash oracle, or free sorting step.

Code and fixed storage are bounded explicitly. The algorithm above can use
fewer than 100 loop-body statements outside the selected permutation, each
expandable into fewer than 64 primitive instruction templates. A direct
implementation of the displayed compression formulas needs fewer than 2,000
additional templates, retaining a fixed loop over the selected rounds; operations on constant
32-bit lane positions use shifts, masks and fixed addresses. The loops over
records, four passes and 64-bit counter values remain loops. A ceiling of 2^16 instruction templates
therefore exceeds the required code. Encode each template in at most four
256-bit words (opcode and up to three operands), using separate primitive
instructions for loads, stores and branches. Its size is at most 2^23 bytes.

Reserve another 2^23 bytes for public target constants, working state,
register spills, loop counters, address variables, the current message/records,
verification scratch and final output. In particular the compression may keep
16 state words, 16 message words, 16 permuted message words and 8 IV words
in individual RAM words. Thus all fixed
storage is at most 2^24 bytes, or 2^19 words. This bound includes the program;
no precomputed collision, target advice or hidden runtime is present. The
counter array is charged separately. The bound refers to the specified RAM program, not Python or a
host library. All fixed storage is initialized and its cost is charged below.

The following large caps allow redundant copying, instruction decoding,
explicit operand loading/storing and address arithmetic. They do not depend
on treating high-level sort/serialization as unit-cost operations.

| Activity | Primitive-operation upper bound |
| --- | ---: |
| Initialize code, constants and all fixed workspace | 2^24 |
| Initialize both record arrays | 128n |
| Generate and retain n messages, excluding target compressions | 17408n |
| Four stable counting-sort passes: record count and scatter | 4 * 2048n |
| Four passes: counter zeroing and prefix scans | 2^74 |
| Fixed setup for the four passes and final scan | 2^20 |
| Scan adjacent records | 1024n |
| Final reconstruction, verification and output, excluding target compressions | 2^16 |

For fixed initialization, 2^19 words with at most 16 units per word costs
at most 2^23, within the stated 2^24 cap. This loads the finite explicit code
and public constants; it does not assume a target-dependent advice oracle.
Array initialization uses six stores per index and fewer than 120 additional
load/address/counter/control units, fitting the 128n cap.

Here is an explicit wrapper construction justifying 17408 per generated
record. Extract the 64 message bytes from u,v by shifts and masks, pack them
into sixteen little-endian 32-bit words, initialize the eight IV words and
sixteen compression-state words, and encode the eight digest words into the
one 256-bit record key. Fewer than 256 constant-size loop iterations suffice;
each expands into fewer than 64 word operations including loads, stores,
address arithmetic and control. Two fresh random-word draws, sample-loop
control and three record stores fit in a further 1024 word operations.
Thus all non-compression work fits below 256*64+1024=17408 operations. The one selected
root compression per message is charged separately, including at verification.
Its code and working buffers are included in the fixed reserve.

On each counting-sort pass, extracting a 64-bit digit requires a fixed shift
and mask. A count step loads one record key and one counter, increments the
counter and advances the source cursor. A scatter step loads and writes the
three record words, loads and increments the selected counter, and advances
the source cursor. Each step uses fewer than 64 logical operations, each
expandable into at most 16 listed primitives including address arithmetic,
operand memory accesses, loop control and spills. Count plus scatter thus
costs at most 2048 primitives per record. Pointer swaps and loop setup
are charged separately under the 2^20 fixed pass allowance. The counter address is
base+(d<<5), and every counter holds at most n=2^128, so both fit a 256-bit
RAM word. Zeroing and prefix scan take at most 256 primitives per counter
per pass, including both traversals and loop bounds. Across four passes this
is at most 4*256*2^64=2^74 primitives. Each adjacent-record scan step
uses two hash loads, at most four message-word loads, three equality tests,
loop/address updates and branches: fewer than 64 logical operations, each
bounded by 16 primitives as above, so it fits 1024n. Scan setup is included
in the fixed 2^20 allowance. Record address
calculation by stride 96 is expanded into shifts and adds as above.

Final verification uses at most two complete hash wrappers, message
distinctness, full digest comparisons and output serialization: less than
2*17408+1024 <2^16 ordinary primitives. The two target compressions are
charged separately. There is no restart cost because no restart occurs.

The table is an operation-count envelope, not a v5 price. Collision-frontier-v5
charges one selected-round target compression as 1 and every other listed
256-bit RAM primitive as 1/C, with C=430 for blake3-r2
(operation_weights.word_operation = 1/430).

Separate the two disjoint categories. Target compressions are the n hashes of
Step 1 plus the two verification hashes:

    H = n + 2 < 2^129.

All remaining listed RAM primitives, including fixed-storage initialization
and verification's non-compression work, are
bounded by the same table:

    W <= (128 + 17408 + 4*2048 + 1024)n + 2^74 + 2^24 + 2^20 + 2^16
       = 26752n + 2^74 + 2^24 + 2^20 + 2^16.

Hence the v5 charged time is

    T = H + W/C
      <= (n + 2) + (26752n + 2^74 + 2^24 + 2^20 + 2^16)/430.

Using n=2^128 and 26752/430 < 62.22,

    2 + (2^74 + 2^24 + 2^20 + 2^16)/430 < 2^66 < n/2,

    T < (1 + 62.22 + 0.5)n
      < 64n
      = 2^134.

The strict margin is over 0.28n beyond all fixed costs.

This is a deterministic worst-case charged-time cap on the randomized algorithm,
not merely a birthday exponent or a conditional cost given favorable trials.
It includes preprocessing, failed samples, sorting, verification and the two
final recompressions. The submitted bound 134 is the smallest integer
ceiling of this envelope under C=430. The raw-count envelope can support
subsequent repricing without inventing an operation mix.

Each array uses n*3*32=96n bytes. With all fixed storage included,

    peak bytes <= 192n + 2^69 + 2^24 < 256n = 2^136.

The arrays contain every retained message, digest and sampled random word.
There is one 2^64-word counter array, but no extra index array, recursion,
message database or pointer per record.
The reserve includes all temporary randomness, state, code/advice/constants,
verification state and final output. Both arrays, counters and the reserve fit
below byte address 2^137. This validates the one-word pointer/counter assumption.
The memory figure is an abstract RAM allowance, not a claim of physical feasibility.

The claim fields have these precise meanings:

- time_log2=134 bounds total charged v5 time by 2^134 units, i.e. T=H+W/C
  with C=430 as derived above.
- memory_log2_bytes=136 bounds simultaneous storage by 2^136 bytes.
- data_log2=129 bounds complete-hash evaluations by n+2 <=2^129, including
  the two final re-evaluations. It counts evaluated message instances, not
  bytes or distinct messages. Every repeated sample is counted; external
  supplied data is zero and all retained data bytes are in peak memory.
- preprocessing_log2=127 bounds fixed setup, both-array initialization,
  and the first counter-array zeroing after v5 word-operation pricing:
  (2^24 + 128n + 256*2^64)/430 < 0.30n + 2^65 < 2^127.
  The later counter-array zeroing and prefix scans are charged in the
  sorting bound. All this work is already included in T.
- nonuniform_advice_log2_bytes=0 means at most 2^0=1 byte of advice; actual
  nonuniform advice is zero. The schema cannot express log2(0). Public
  constants and code are fully charged in the fixed storage and initialization.
- success_probability=0.39 is the lower bound proved in Section 4.

## 6. Evidence and interpretation

This is a conservative generic baseline proposal, not a new cryptanalytic
advance. The complete algorithm, target definition, probability proof and RAM
ledger are the supporting evidence. No full-scale execution, observed collision
pair, measured success rate, experimental independence or measured resource
usage is asserted. No sampled experiment is needed for the universal finite
probability argument. The certificate manifest is valid and empty; no
experiment manifest or participant executable is supplied.

The required baseline_improved identifier blake3-r2-nominal-v2 names the
organizer's nominal display reference 128. It is not an established attack,
qualified baseline or security bound; the identifier's field name is not a
claim of improvement. This candidate's scalar bound 134 exceeds 128. No
Pareto dominance claim follows from scalar scoring.

submission_state=ready means this independent exploratory package is complete
for review. It does not assert an actual qualifying review, an emitted score,
human acceptance, or Yukon promotion. Its substantive obligations and evidence
are intended to meet rigorous standards, while each lane still requires its own
correctly bound package and selected-lane review outcome.
