# A fixed-function collision baseline for five-round SHA3-256

This independent exploratory package targets sha3-256-r5-prefix-v1. It proposes
a classical randomized algorithm with success at least 1/2, total charged time
at most 2^149 units, and peak memory at most 2^137 bytes under
collision-frontier-v3. These are conservative analytical upper bounds, not
measured execution costs. The claimed scalar is 149 + 137 = 286.

The proof uses no distributional property of SHA3: every fixed function from
the chosen message domain to 256-bit strings satisfies its probability bound.
Fresh independent uniform coins are the explicit RAM model's random-word
primitive. No PRNG, random-oracle, round-independence, or differential heuristic
is assumed. Accordingly the heuristic list is empty.

## 1. Exact complete hash

Each message is exactly 64 bytes, of bit length 512 < 2^64. Two 256-bit words
u,v encode m=LE32(u)||LE32(v), where LE32 includes all 32 little-endian bytes,
including zeros. These encodings bijectively cover a domain D of size 2^512.
There is no unknown IV, free-start state, or supplied prefix/advice.

H is the following complete hash. Initialize a 1600-bit state to zero, as
25 lanes A[x,y] of 64 bits indexed x+5y. Pad m to the one 136-byte rate block

    m || 0x06 || (70 zero bytes) || 0x80.

This is SHA3's domain suffix 01 followed by pad10*1, with delimited suffix
0x06. There is no length trailer. XOR the 17 little-endian 8-byte lanes of
this block into A[0],...,A[16]. The remaining eight capacity lanes are zero.
Apply rounds 0,1,2,3,4, in order, each with the following formulas; x,y and
coordinate subscripts are modulo 5:

    C[x] = XOR over y of A[x,y]
    D[x] = C[x-1] XOR ROT64(C[x+1],1)
    A[x,y] = A[x,y] XOR D[x]
    B[y,2x+3y] = ROT64(A[x,y],rho[x,y])
    A[x,y] = B[x,y] XOR ((NOT64 B[x+1,y]) AND B[x+2,y])
    A[0,0] = A[0,0] XOR RC[round].

All chi right-hand sides read the temporary B array. ROT64 rotates left
within 64 bits; NOT64 complements only those bits. The rho offsets, with
rows y=0,...,4 and columns x=0,...,4, are:

    0   1  62  28  27
   36  44   6  55  20
    3  10  43  25  39
   41  45  15  21   8
   18   2  61  56  14

The five hexadecimal round constants, in order, are:

    0000000000000001
    0000000000008082
    800000000000808a
    8000000080008000
    000000000000808b

After round 4, H(m)=LE8(A[0])||LE8(A[1])||LE8(A[2])||LE8(A[3]).
These are all 256 output bits, the first 32 squeeze bytes in SHA3 order.
No additional permutation is required because 32 < 136. Absorption XORs into
the 1088-bit rate; the capacity is 512 bits and there is no Davies-Meyer
feed-forward. Thus each complete hash uses exactly one selected five-round
permutation. This specifies the profile's complete padded, fixed-IV hash on
every message the algorithm can generate. The prefix is the first five
Keccak-f rounds, not Keccak-p's last-round convention.

## 2. Algorithm and representation

Set n=2^129. A record is three 256-bit words (h,u,v), with h the little-endian
integer encoding of H(LE32(u)||LE32(v)). Unsigned comparison of h is a total
order whose equality is full digest equality. Use two flat arrays A and B,
each of n records. Explicitly initialize all six words per index across the
two arrays; allocation and initialization are charged.

1. For i=0,...,n-1, draw fresh independent uniform 256-bit words u and v,
   construct their 64-byte message, compute its complete H, and store
   (h,u,v) in A[i]. Retain repeated inputs; there is no resampling.
2. Sort by full h using stable, iterative bottom-up merge sort with A and B
   as alternating source/destination arrays. For widths w=1,2,4,...,2^128,
   merge successive pairs of sorted runs of length w. Choose the left run
   on digest ties, copy all three words of every record, and exchange the
   two array base pointers at the end of each pass. Exactly 129 passes
   each write exactly n records.
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
2^138, far below 2^256. The value n is made by 1<<129. Message contents occupy
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
       = exp(-(2-2^-128))
       < exp(-1).

Here n<Q and 1-t<=exp(-t) on 0<=t<1, obtained by integrating the derivative
-1/(1-t)<=-1 of log(1-t). This also covers distributions with small support.

Let E be the event that some input messages repeat. The union bound gives

    Pr[E] <= n(n-1)/(2|D|) < 2^258/(2*2^512) = 2^-255.

No independence of the pair-events is required. If outputs collide and E
does not occur, the algorithm succeeds. Thus

    Pr[success] >= 1 - Pr[all Y_i distinct] - Pr[E]
                > 1 - exp(-1) - 2^-255
                > 1/2.

Indeed e=sum_(k>=0)1/k! > 8/3, so exp(-1)<3/8, and 2^-255<1/8.
This intentionally conservative bound proves the declared 0.5 and exceeds
the required 0.39. Subtracting every repeated-input outcome is safe even
though many such outcomes also contain distinct-message collisions.
The number concerns algorithmic success, not confidence in a proof or review.

## 5. Fully charged RAM implementation

One 256-bit word is 32 bytes. Each selected five-round permutation costs one
unit; every other listed RAM primitive costs one unit. All bounds include
message construction, failed samples, randomness, memory initialization,
sorting, verification, and fixed code/constants. There is no external disk,
unaccounted preprocessing service, whole-hash oracle, or free sorting step.

Code and fixed storage are bounded explicitly. The algorithm above can use
fewer than 100 loop-body statements outside the selected permutation, each
expandable into fewer than 64 primitive instruction templates. A direct
implementation of the displayed permutation formulas needs fewer than 2,000
additional templates, retaining a fixed loop over the five rounds; operations on constant
64-bit lane positions use shifts, masks and fixed addresses. The loops over
records and merge widths remain loops. A ceiling of 2^16 instruction templates
therefore exceeds the required code. Encode each template in at most four
256-bit words (opcode and up to three operands), using separate primitive
instructions for loads, stores and branches. Its size is at most 2^23 bytes.

Reserve another 2^23 bytes for public target constants, working state,
register spills, loop counters, address variables, the current message/records,
verification scratch and final output. In particular the permutation may keep
25 A lanes, 25 B lanes and 10 C/D lanes in individual RAM words. Thus all fixed
storage is at most 2^24 bytes, or 2^19 words. This bound includes the program;
no precomputed collision, target advice, large lookup table or hidden runtime
is present. The bound refers to the specified RAM program, not Python or a
host library. All fixed storage is initialized and its cost is charged below.

The following large caps allow redundant copying, instruction decoding,
explicit operand loading/storing and address arithmetic. They do not depend
on treating high-level sort/serialization as unit-cost operations.

| Activity | Charged-unit upper bound |
| --- | ---: |
| Initialize code, constants and all fixed workspace | 2^24 |
| Initialize both record arrays | 128n |
| Generate, hash and retain n messages | 65536n |
| Exactly 129 merge passes | 129 * 4096n |
| Scan adjacent records | 2048n |
| Final reconstruction, verification and output | 2^18 |

For fixed initialization, 2^19 words with at most 16 units per word costs
at most 2^23, within the stated 2^24 cap. This loads the finite explicit code
and public constants; it does not assume a target-dependent advice oracle.
Array initialization uses six stores per index and fewer than 120 additional
load/address/counter/control units, fitting the 128n cap.

Here is an explicit wrapper construction justifying 65536 per generated
record. Store each 64-bit lane in its own RAM word. Extract message bytes
from u,v by shifts and masks, store the padding bytes, initialize the 25-lane
state, combine successive groups of eight bytes into the 17 rate lanes,
and XOR those lanes into the state. At most 512 constant-size loop iterations
suffice in total: 64 byte extraction, 136 padding/block initialization, 25
state initialization, 136 byte-to-lane packing, 17 absorptions, and 32 output
byte encodings sum to 410. Each iteration can be implemented in fewer than
64 charged units including operand access, bit operations, loop control and
address arithmetic. These cost at most 32768. Two random-word draws, the one
selected permutation, output-word packing, sample-loop control, and storing
the three-word record fit within a further 1024 units. Total <65536. Every
selected permutation is charged; its code and buffers are in the fixed reserve.

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

Summing all phases, including the cost of batches that fail to find a collision,

    T <= (128 + 65536 + 129*4096 + 2048)n + 2^24 + 2^18
       = 596096n + 2^24 + 2^18
       < 1048576n
       = 2^149.

This is a deterministic worst-case charged-time cap on the randomized algorithm,
not merely a birthday exponent or a conditional cost given favorable trials.

Each array uses n*3*32=96n bytes. With all fixed storage included,

    peak bytes <= 192n + 2^24 < 256n = 2^137.

The arrays contain every retained message, digest and sampled random word.
There is no extra index array, recursion, message database or pointer per record.
The reserve includes all temporary randomness, state, code/advice/constants,
verification state and final output. Both arrays and the reserve fit below
byte address 2^138. This validates the one-word pointer/counter assumption.
The memory figure is an abstract RAM allowance, not a claim of physical feasibility.

The claim fields have these precise meanings:

- time_log2=149 bounds total charged time by 2^149 units.
- memory_log2_bytes=137 bounds simultaneous storage by 2^137 bytes.
- data_log2=130 bounds complete-hash evaluations by n+2 <=2^130, including
  the two final re-evaluations. It counts evaluated message instances, not
  bytes or distinct messages. Every repeated sample is counted; external
  supplied data is zero and all retained data bytes are in peak memory.
- preprocessing_log2=137 bounds fixed setup plus both-array initialization:
  2^24+128n <2^137 units. It is already included in T, not an omitted phase.
- nonuniform_advice_log2_bytes=0 means at most 2^0=1 byte of advice; actual
  nonuniform advice is zero. The schema cannot express log2(0). Public
  constants and code are fully charged in the fixed storage and initialization.
- success_probability=0.5 is the lower bound proved in Section 4.

## 6. Evidence and interpretation

This is a conservative generic baseline proposal, not a new cryptanalytic
advance. The complete algorithm, target definition, probability proof and RAM
ledger are the supporting evidence. No full-scale execution, observed collision
pair, measured success rate, experimental independence or measured resource
usage is asserted. No sampled experiment is needed for the universal finite
probability argument. The certificate manifest is valid and empty; no
experiment manifest or participant executable is supplied.

The required baseline_improved identifier sha3-256-r5-nominal-v2 names the
organizer's nominal display reference 128. It is not an established attack,
qualified baseline or security bound; the identifier's field name is not a
claim of improvement. This candidate's scalar bound 286 exceeds 128. No
Pareto dominance claim follows from scalar scoring.

submission_state=ready means this independent exploratory package is complete
for review. It does not assert an actual qualifying review, an emitted score,
human acceptance, or Yukon promotion. Its substantive obligations and evidence
are intended to meet rigorous standards, while each lane still requires its own
correctly bound package and selected-lane review outcome.
