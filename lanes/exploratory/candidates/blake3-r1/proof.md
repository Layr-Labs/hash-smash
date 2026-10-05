# A smaller fixed-function collision batch for 1-round BLAKE3

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains
a separately reported resource bound.

This independent exploratory package targets blake3-r1-prefix-v1. It proposes
a classical randomized algorithm with success at least 0.39, total charged time
at most 2^139.381363 units, and peak memory at most 2^136 bytes under
collision-frontier-v5. These are conservative analytical upper bounds, not
measured execution costs. The claimed scalar is 139.381363.

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

H is unkeyed BLAKE3-256 with 1 prefix rounds in every compression.
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
Execute exactly the first 1 rounds, with no later rounds. The full
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
each of n records. Explicitly initialize all six words per index across the
two arrays; allocation and initialization are charged.

1. For i=0,...,n-1, draw fresh independent uniform 256-bit words u and v,
   construct their 64-byte message, compute its complete H, and store
   (h,u,v) in A[i]. Retain repeated inputs; there is no resampling.
2. Sort by full h using stable, iterative bottom-up merge sort with A and B
   as alternating source/destination arrays. For widths w=1,2,4,...,2^127,
   merge successive pairs of sorted runs of length w. Choose the left run
   on digest ties, copy all three words of every record, and exchange the
   two array base pointers at the end of each pass. Exactly 128 passes
   each write exactly n records.
3. Scan all adjacent positions j-1,j in the sorted source array, from j=1
   through n-1. Test h equality and inequality of the pair (u,v), testing
   both message words. On the first qualifying pair, reconstruct both
   messages and recompute both complete hashes with the standard IV and
   root flags from Section 1.
   Check message distinctness and equality of all 256 recomputed output
   bits. Return the two messages if verified; otherwise halt with failure.
4. If the scan finishes without such a pair, halt with failure.

There is one batch, no restart, and at most one final verification of two
messages. Verification failure cannot occur in the exact RAM model because
the original digests came from the same deterministic H. This explicit
defensive check is still charged. Every outcome halts within the same budget.

For a concrete merge, maintain w, run start b, source cursors i=b,j=b+w,
ends b+w,b+2w, and destination cursor k=b. While k<b+2w, choose the nonempty
run if the other is exhausted; otherwise load and compare both h words.
Copy all three words of the selected record, advance its source cursor, and
advance k. When the run is complete, advance b by 2w. When the pass ends,
swap source/destination base pointers and double w. All boundaries are exact
because n is a power of two. There is no recursive stack or library sort.

Record i starts at byte address base+96i, calculated as
base+(i<<6)+(i<<5), without multiplication. Word offsets are 0,32,64.
Indices, counters, sentinels, run boundaries and byte addresses are less than
2^138, far below 2^256. The value n is made by 1<<128. Message contents occupy
two words; no 512-bit single-word arithmetic is assumed. The proof's symbolic
domain/codomain cardinalities need not be represented in the machine.

## 3. Correctness of any returned collision

The standard merge invariant says each output prefix contains the smallest
remaining keys of its two sorted inputs. Copying entire records preserves
each digest's associated message. Induction over the passes therefore sorts
all original records without deleting any.

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

An elementary rational bound certifies the last inequality without relying on
floating-point arithmetic. The first four terms of exp(1/2) sum to 79/48, so
exp(-1/2) < 48/79. Set epsilon=2^-129. For 0<=epsilon<=1/2, the exponential
series is bounded by the geometric series, giving
exp(epsilon)<=1/(1-epsilon)<=1+2*epsilon. Consequently

    Pr[success] > 1 - (48/79)(1+2^-128) - 2^-257
                = 31/79 - (48/79)2^-128 - 2^-257.

Since 31/79 - 39/100 = 19/7900, while
(48/79)2^-128 + 2^-257 < 2^-127 < 1/1024 < 19/7900,
the advertised success probability 0.39 follows. The sharper exponential
lower bound is approximately 0.3934693402873665764. This is a lower bound for
every fixed H on the specified domain; it does not model H as a random oracle.
Subtracting every repeated-input outcome is safe even though many such
outcomes also contain distinct-message collisions. The number concerns
algorithmic success, not confidence in a proof or review. The batch is not
restarted and the cost includes outcomes that fail to produce a collision.

## 5. Fully charged RAM implementation

One 256-bit word is 32 bytes. Each selected compression costs one unit; every other listed RAM
primitive costs 1/C units, where C=222. All bounds include
message construction, failed samples, randomness, memory initialization,
sorting, verification, and fixed code/constants. There is no external disk,
unaccounted preprocessing service, whole-hash oracle, or free sorting step.

Code and fixed storage are bounded explicitly. The algorithm above can use
fewer than 100 loop-body statements outside the selected permutation, each
expandable into fewer than 64 primitive instruction templates. A direct
implementation of the displayed compression formulas needs fewer than 2,000
additional templates, retaining a fixed loop over the selected rounds; operations on constant
32-bit lane positions use shifts, masks and fixed addresses. The loops over
records and merge widths remain loops. A ceiling of 2^16 instruction templates
therefore exceeds the required code. Encode each template in at most four
256-bit words (opcode and up to three operands), using separate primitive
instructions for loads, stores and branches. Its size is at most 2^23 bytes.

Reserve another 2^23 bytes for public target constants, working state,
register spills, loop counters, address variables, the current message/records,
verification scratch and final output. In particular the compression may keep
16 state words, 16 message words, 16 permuted message words and 8 IV words
in individual RAM words. Thus all fixed
storage is at most 2^24 bytes, or 2^19 words. This bound includes the program;
no precomputed collision, target advice, large lookup table or hidden runtime
is present. The bound refers to the specified RAM program, not Python or a
host library. All fixed storage is initialized and its cost is charged below.

The following large caps allow redundant copying, instruction decoding,
explicit operand loading/storing and address arithmetic. They do not depend
on treating high-level sort/serialization as unit-cost operations.

| Activity | Non-compression primitive-operation upper bound |
| --- | ---: |
| Initialize code, constants and all fixed workspace | 2^24 |
| Initialize both record arrays | 128n |
| Generate messages, hash wrappers and retain records (compressions separate) | 65536n |
| Exactly 128 merge passes | 128 * 4096n |
| Scan adjacent records | 2048n |
| Final reconstruction, verification wrappers and output (compressions separate) | 2^18 |

For fixed initialization, 2^19 words with at most 16 primitive operations
per word use at most 2^23 operations, within the stated 2^24 cap. This loads the finite explicit code
and public constants; it does not assume a target-dependent advice oracle.
Array initialization uses six stores per index and fewer than 120 additional
load/address/counter/control operations, fitting the 128n cap.

Here is an explicit wrapper construction justifying 65536 per generated
record. Extract the 64 message bytes from u,v by shifts and masks, pack them
into sixteen little-endian 32-bit words, initialize the eight IV words and
sixteen compression-state words, and encode the eight digest words into the
one 256-bit record key. Fewer than 256 constant-size loop iterations suffice;
each expands into fewer than 64 word operations including loads, stores,
address arithmetic and control. Two fresh random-word draws, sample-loop
control and three record stores fit in a further 1024 word operations.
Thus all non-compression work fits below 65536 operations. The one selected
root compression per message is charged separately, including at verification.
Its code and working buffers are included in the fixed reserve.

For merges, each output record requires at most two exhaustion comparisons
with branches, two key loads and a comparison/branch, three record loads and
three stores, plus cursor/address updates and loop control. There are fewer
than 64 such logical operations, each implementable with at most 16 charged
primitive operations even allowing instruction/operand memory accesses and
spills. This costs at most 1024 per record. Run setup is at most 64 such
operations, or 1024 per run; every run emits at least two records. Pass setup
is also at most 1024 per pass, which emits n>=2 records. Hence the per-output
charge is at most 1024+512+512=2048, below the chosen 4096. This includes
pointer swaps, run/pass endings and initialization of merge cursors.
The scan uses fewer operations per pair than this merge loop and so fits
2048n. Address calculation by stride 96 is expanded into shifts/adds as above.

Final verification uses at most two complete hash wrappers, message
distinctness, full digest comparisons and output serialization: less than
2*65536+1024 <2^18. There is no restart cost because no restart occurs.

The table counts non-compression operations W, not compression-equivalent
units. Whole compressions are disjoint from this count: each generated record
uses one, and final verification uses at most two. Denote this number by K.
With n=2^128 and C=222, the same explicit wrapper and sorting bounds yield

    K <= n+2,
    W <= (128 + 65536 + 128*4096 + 2048)n + 2^24 + 2^18
       = 592000n + 2^24 + 2^18,
    T = K + W/222
      <= (592222/222) 2^128 + 2 + (2^24+2^18)/222
       < 2^139.381363.

For reproducible scalar arithmetic, log2 of the displayed total upper bound is
139.3813626931671219043699403590632071430830716335469... . The submitted
139.381363 rounds this upward. The finite initialization and verification
terms are included in that calculation, not discarded asymptotically.
No compression's internal arithmetic is charged twice, and no wrapper,
message construction, random draw, memory operation, control operation,
preprocessing, failed sample or verification is made free by normalization.

This is a deterministic worst-case charged-time cap on the randomized
algorithm. It is not a conditional cost given favorable trials, not an
observed runtime and not merely the birthday exponent. The coefficient
592000 deliberately retains the inherited implementation envelopes; the
scalar is tightened to six decimal places for those envelopes, not asserted
optimal among all RAM implementations or collision algorithms.

Each array uses n*3*32=96n bytes. With all fixed storage included,

    peak bytes <= 192n + 2^24 < 256n = 2^136.

The arrays contain every retained message, digest and sampled random word.
There is no extra index array, recursion, message database or pointer per record.
The reserve includes all temporary randomness, state, code/advice/constants,
verification state and final output. Both arrays and the reserve fit below
byte address 2^138. This validates the one-word pointer/counter assumption.
The memory figure is an abstract RAM allowance, not a claim of physical feasibility.

The claim fields have these precise meanings:

- time_log2=139.381363 bounds total charged time by 2^139.381363 units.
- memory_log2_bytes=136 bounds simultaneous storage by 2^136 bytes.
- preprocessing_log2=128 bounds fixed setup and both-array initialization:
  (2^24+128n)/222 < n = 2^128 units. Indeed 2^24 < 94n.
  This phase is already included in T, not added or omitted afterward.
- nonuniform_advice_log2_bytes=0 means at most 2^0=1 byte of advice; actual
  nonuniform advice is zero. The schema cannot express log2(0). Public
  constants and code are fully charged in fixed storage and initialization.
- success_probability=0.39 is the lower bound proved in Section 4.
- The optional legacy data_log2 field is omitted. There are at most n+2
  complete-hash evaluations, including the two final re-evaluations; every
  repeated sample is charged. All retained message/data bytes enter memory.

## 6. Evidence and interpretation

This is a conservative generic baseline proposal, not a new cryptanalytic
advance. The complete algorithm, target definition, probability proof and RAM
ledger are the supporting evidence. No full-scale execution, observed collision
pair, measured success rate, experimental independence or measured resource
usage is asserted. No sampled experiment is needed for the universal finite
probability argument. The certificate manifest is valid and empty; no
experiment manifest or participant executable is supplied.

The required baseline_improved identifier blake3-r1-nominal-v2 names the
organizer's nominal display reference 128. It is not an established attack,
qualified baseline or security bound; the identifier's field name is not a
claim of improvement. This candidate's scalar bound 139.381363 exceeds 128. No
Pareto dominance claim follows from scalar scoring.

submission_state=ready means this independent exploratory package is complete
for review. It does not assert an actual qualifying review, an emitted score,
human acceptance, or Yukon promotion. Its substantive obligations and evidence
are intended to meet rigorous standards, while each lane still requires its own
correctly bound package and selected-lane review outcome.


## 7. Provenance and scope of the revision

The starting point is the generic exploratory candidate at repository commit
8a0f02675cdcd58ebfc16119af02a094c3e1dd16, whose claimed scalar is 149.
This revision halves its batch from 2^129 to 2^128, proves that the required
0.39 success threshold still holds, reduces the merge-pass count to 128, and
prices the existing non-compression operation caps at the stated 1/222 rate.
It also states standard-IV initialization explicitly during verification.
The probability proof, complete-hash target and charged implementation remain
self-contained above. This is a generic analytical improvement to that
candidate's bound, with no structural BLAKE3 attack, empirical experiment,
precomputed witness or unpromoted solver construction used as evidence.

A local mechanical check cannot qualify this result. Public pending
submissions with smaller reported scores are separate claims; this package
makes no claim to improve those results. AI review, incumbent comparison,
human acceptance and successful promotion remain separate gates.
