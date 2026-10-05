# A radix-sort collision accounting for five-round SHA3-256

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains
a separately reported resource bound.

This independent exploratory package targets sha3-256-r5-prefix-v1. It proposes
a classical randomized algorithm with success at least 1/2, total charged time
at most 2^132.879 units, and peak memory at most 2^137 bytes under
collision-frontier-v5. These are conservative analytical upper bounds, not
measured execution costs. The claimed scalar is 132.879.

The proof uses no distributional property of SHA3: every fixed function from
the chosen message domain to 256-bit strings satisfies its probability bound.
Fresh independent uniform coins are the explicit RAM model's random-word
primitive. No PRNG, random-oracle, round-independence, or differential heuristic
is assumed. Accordingly the heuristic list is empty.

Relative to the organizer merge-sort baseline (scalar 137.785), the only
algorithmic change is replacing iterative merge sort with a stable two-pass
least-significant-digit radix (counting) sort on 128-bit digest digits, plus a
tightened but still conservative generation-wrapper envelope. Memory may grow
because the cost model scores memory as a reviewed metric only.

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
order whose equality is full digest equality. Use two flat arrays Src and Dst,
each of n records, and one flat count array Count of B=2^128 words. Explicitly
initialize all six words per record index across Src and Dst, and initialize
Count; allocation and initialization are charged.

1. For i=0,...,n-1, draw fresh independent uniform 256-bit words u and v,
   construct their 64-byte message, compute its complete H, and store
   (h,u,v) in Src[i]. Retain repeated inputs; there is no resampling.
2. Sort by full h using a stable two-pass least-significant-digit radix sort
   with 128-bit digits. Pass 0 uses digit0 = h mod 2^128 (low 128 bits).
   Pass 1 uses digit1 = floor(h / 2^128) (high 128 bits). Each pass is a
   stable counting sort into the opposite record array:
   (a) For t=0,...,B-1 set Count[t]=0.
   (b) For i=0,...,n-1 extract the pass digit from Src[i].h, then
       Count[digit] <- Count[digit]+1.
   (c) Prefix-sum: for t=1,...,B-1 set Count[t] <- Count[t]+Count[t-1],
       so Count[t] equals the number of keys with digit <= t. Set base
       offsets so the first slot of digit d is Count[d-1] (with Count[-1]=0).
       Equivalently maintain an exclusive prefix so the write index for the
       next key of digit d is the running Count[d] cursor.
   (d) Stable scatter: for i=n-1,...,0 extract digit d from Src[i].h,
       decrement the exclusive cursor for d, and copy all three words of
       Src[i] into Dst[cursor].
   (e) Swap the roles of Src and Dst (exchange base pointers). After pass 1,
       Src holds records sorted by full 256-bit h.
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

Digit extraction uses shifts and masks on the single 256-bit word h; no
multi-word digest representation is required. Indices, counters, sentinels
and byte addresses stay below 2^138. The value n is made by 1<<129 and B by
1<<128. Message contents occupy two words. The proof's symbolic
domain/codomain cardinalities need not be represented in the machine.

Record i starts at byte address base+96i, calculated as
base+(i<<6)+(i<<5), without multiplication. Word offsets are 0,32,64.
Count[t] starts at count_base+(t<<5).

## 3. Correctness of any returned collision

A stable counting sort places records into contiguous digit buckets while
preserving relative order within each bucket. Two successive LSD passes on
128-bit digits therefore sort by the full 256-bit key: after the low-digit
pass, equal low digits are contiguous and stably ordered by input order;
after the high-digit pass, records are ordered by high digit and, within
each high digit, retain the already-sorted low-digit order. Copying entire
records preserves each digest's associated message. No record is deleted.

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
unit; every other listed RAM primitive costs 1/1355 units. Ordinary-operation
counts W below are separate from permutation calls H_calls. The permutation's
internal rounds are not counted again in W. All bounds include
message construction, failed samples, randomness, memory initialization,
sorting, verification, and fixed code/constants. There is no external disk,
unaccounted preprocessing service, whole-hash oracle, or free sorting step.

Code and fixed storage are bounded explicitly. The algorithm above can use
fewer than 100 loop-body statements outside the selected permutation, each
expandable into fewer than 64 primitive instruction templates. A direct
implementation of the displayed permutation formulas needs fewer than 2,000
additional templates, retaining a fixed loop over the five rounds; operations on constant
64-bit lane positions use shifts, masks and fixed addresses. The loops over
records and digit buckets remain loops. A ceiling of 2^16 instruction templates
therefore exceeds the required code. Encode each template in at most four
256-bit words (opcode and up to three operands), using separate primitive
instructions for loads, stores and branches. Its size is at most 2^23 bytes.

Reserve another 2^23 bytes for public target constants, working state,
register spills, loop counters, address variables, the current message/records,
verification scratch and final output. In particular the permutation may keep
25 A lanes, 25 B lanes and 10 C/D lanes in individual RAM words. Thus all fixed
storage is at most 2^24 bytes, or 2^19 words. This bound includes the program;
no precomputed collision, target advice, large lookup table beyond Count, or
hidden runtime is present. The bound refers to the specified RAM program, not
Python or a host library. All fixed storage is initialized and its cost is
charged below.

The following large caps allow redundant copying, instruction decoding,
explicit operand loading/storing and address arithmetic. They do not depend
on treating high-level sort/serialization as unit-cost operations.

| Activity | Permutation calls, at cost 1 each | Ordinary operations, at cost 1/1355 each |
| --- | ---: | ---: |
| Initialize code, constants and all fixed workspace | 0 | 2^24 |
| Initialize both record arrays | 0 | 128n |
| Generate, hash and retain n messages | n | 8192n |
| Two radix passes: per-record count and scatter | 0 | 8192n |
| Two radix passes: Count zero and prefix (over B=2^128) | 0 | 16n |
| Scan adjacent records | 0 | 2048n |
| Final reconstruction, verification and output | at most 2 | 2^18 |

The counts in the last column are ordinary-operation envelopes; their
instruction fetches, memory traffic and spare allowance are retained. The
permutation calls in the middle column are priced independently.
Because B=2^128 and n=2^129, the identity 2·8·B = 16·2^128 = 8n holds for an
8-primitive-per-bucket zero-plus-prefix charge; the table uses the still larger
16n envelope (2× margin).

For fixed initialization, processing 2^19 words at at most 16 ordinary
operations per word takes at most 2^23 operations, within the stated 2^24 cap.
Array initialization uses six stores per index and fewer than 120 additional
load/address/counter/control operations, fitting the 128n cap.

Generation wrapper (8192 ordinary operations per record). Store each 64-bit
lane in its own RAM word. Extract message bytes from u,v by shifts and masks,
store the padding bytes, initialize the 25-lane state, combine successive
groups of eight bytes into the 17 rate lanes, and XOR those lanes into the
state. At most 410 constant-size loop iterations suffice in total: 64 byte
extraction, 136 padding/block initialization, 25 state initialization, 136
byte-to-lane packing, 17 absorptions, and 32 output byte encodings. Each
iteration can be implemented in fewer than 16 ordinary operations including
operand access, bit operations, loop control and address arithmetic, giving
at most 6560 ordinary operations. Two random-word draws, the one selected
permutation's dispatch, output-word packing, sample-loop control, and storing
the three-word record fit within a further 1024 ordinary operations. Ordinary
total <= 7584 < 8192; add one target-permutation unit per hash. The
permutation's code and buffers remain in the fixed reserve. (The organizer
baseline used 65536 for the same wrapper; 8192 is a tightened but still
conservative envelope above the explicit 7584 reconstruction.)

Radix per-record work (4096 ordinary operations per record per pass, hence
8192n across two passes). For the count phase of one pass, each record needs
digit extraction (shifts/masks), load-increment-store of Count[digit], and
loop/address control. For the stable scatter phase, each record needs digit
extraction, cursor decrement, three-word record load, three-word store into
Dst, and loop/address control. Fewer than 64 logical operations cover both
phases of one pass for one record; expanding each into at most 16 charged
primitives (instruction fetch, operand access, spills) costs at most 1024
primitives, and the merge-sort baseline's 4096-per-record-per-pass envelope
is reused as a deliberately loose upper bound for the combined count+scatter
work of one radix pass. Pass setup beyond Count maintenance is absorbed in
that same per-record margin because each pass emits n records.

Count zero and prefix (16n). Zeroing B words is B stores. An inclusive or
exclusive prefix over B words uses a constant handful of loads, adds, stores
and loop branches per bucket. Charging 8 primitives per bucket per pass gives
2·8·B = 8n operations; the ledger uses 16n.

The adjacent scan uses fewer operations per pair than one radix pass and so
fits 2048n. Address calculation by stride 96 is expanded into shifts/adds.

Final verification uses at most two complete hash wrappers, message
distinctness, full digest comparisons and output serialization: less than
2*8192+1024 < 2^18 ordinary operations, plus two permutation calls.
There is no restart cost because no restart occurs.

Summing all phases, including the cost of batches that fail to find a collision,

    H_calls <= n+2
    W <= (128 + 8192 + 8192 + 16 + 2048)n + 2^24 + 2^18
       = 18576n + 17039360
    T = H_calls + W/1355
      <= (1 + 18576/1355)n + 2 + 17039360/1355
       = (19931/1355)n + (2 + 17039360/1355)
       < (14709225/1000000)n
       < 2^3.879 n = 2^132.879,  for n=2^129.

Both strict inequalities can be checked with integers: substitute n=2^129
and clear denominators for the setup term; the leading coefficient satisfies
19931/1355 < 14.709225, and 14.709225 < 2^3.879 because
log2(14.709225) < 3.879 (equivalently 14.709225^1000 < 2^3879). The fixed
setup and final verification are dominated by the leading term at this n.
No old rounded total is divided by C. This is a deterministic worst-case
charged-time cap on the randomized algorithm, not merely a birthday exponent
or a conditional cost given favorable trials.

Memory. Each record array uses n·3·32 = 96n bytes. The Count array uses
B·32 = 2^133 bytes. With all fixed storage included,

    peak bytes <= 192n + 2^133 + 2^24
               = 1.5 · 2^136 + 2^133 + 2^24
               < 2^137.

The arrays contain every retained message, digest and sampled random word,
plus the radix count table. The reserve includes all temporary randomness,
state, code/constants, verification state and final output. All addresses
fit below byte address 2^138. The memory figure is an abstract RAM allowance,
not a claim of physical feasibility. Under collision-frontier-v5 memory does
not contribute to the scalar score.

The claim fields have these precise meanings:

- time_log2=132.879 bounds total charged time by 2^132.879 units.
- memory_log2_bytes=137 bounds simultaneous storage by 2^137 bytes.
- preprocessing_log2=126 bounds fixed setup plus both-array initialization:
  (2^24+128n)/1355 < 2^126 target-compression units. Actual setup is included
  in T, not an omitted phase.
- nonuniform_advice_log2_bytes=0 means at most 2^0=1 byte of advice; actual
  nonuniform advice is zero. The schema cannot express log2(0). Public
  constants and code are fully charged in the fixed storage and initialization.
- success_probability=0.5 is the lower bound proved in Section 4.

## 6. Evidence and interpretation

This package improves only the collision-detection data structure and the
generation-wrapper accounting relative to the organizer merge-sort baseline.
It is not a new cryptanalytic break of SHA3. The complete algorithm, target
definition, probability proof and RAM ledger are the supporting evidence. No
full-scale execution, observed collision pair, measured success rate,
experimental independence or measured resource usage is asserted. No sampled
experiment is needed for the universal finite probability argument. The
certificate manifest is valid and empty; no experiment manifest or participant
executable is supplied.

The required baseline_improved identifier sha3-256-r5-nominal-v2 names the
organizer's nominal display reference 128. It is not an established attack,
qualified baseline or security bound; the identifier's field name is not a
claim of improvement. This candidate's scalar bound 132.879 still exceeds 128.
No Pareto dominance claim follows from scalar scoring.

submission_state=ready means this independent exploratory package is complete
for review. It does not assert an actual qualifying review, an emitted score,
human acceptance, or Yukon promotion. Its substantive obligations and evidence
are intended to meet exploratory standards; each lane still requires its own
correctly bound package and selected-lane review outcome.

## 7. Source and accounting revision

Starting point: the organizer SHA3-256 r5 exploratory candidate in this
checkout, which declared time_log2=137.785 using stable iterative merge sort
(129 passes · 4096n) and a 65536n generation wrapper under collision-frontier-v5
with C=1355.

Changes in this package:

1. Replace merge sort with a stable two-pass LSD radix (counting) sort on
   128-bit digits, eliminating the log2(n)=129 merge-pass factor. Count-array
   work over B=2^128 is charged explicitly (16n envelope).
2. Tighten the generation wrapper from 65536n to 8192n, above an explicit
   reconstruction of at most 7584 ordinary operations per record.
3. Retain the same complete hash, n=2^129, three-word records, adjacent scan,
   fixed-function probability proof, success lower bound 0.5, empty heuristic
   list, and empty certificate manifest.

Public awaiting-review notes mentioned related radix themes; those notes were
treated as untrusted hints only. Every envelope and the final scalar were
reconstructed independently from the cost model and target reference cost
C=1355. This new package requires fresh ordinary review; no historical
qualification is asserted.
