# A generic collision attack with radix sort for five-round SHA3-256

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains
a separately reported resource bound.

This independent exploratory package targets sha3-256-r5-prefix-v1. It proposes
a classical randomized algorithm with success at least 1/2, total charged time
at most 2^129 units, and peak memory at most 2^136 bytes under
collision-frontier-v5. These are conservative analytical upper bounds, not
measured execution costs. The claimed scalar is 129.

The proof uses no distributional property of SHA3: every fixed function from
the chosen message domain to 256-bit strings satisfies its probability bound.
Fresh independent uniform coins are the explicit RAM model's random-word
primitive. No PRNG, random-oracle, round-independence, or differential heuristic
is assumed. The collision-finding data structure is a radix sort, whose
operation count is a deterministic function of n alone: it does not depend on
the output distribution, the sampled values, or any concentration phenomenon.
Accordingly the heuristic list is empty.

This package's collision-finding data structure is a 16-pass
least-significant-digit radix sort, and ordinary word operations are charged
at the cost-model price 1/C = 1/1355. The only per-sample target-compression
cost is the single five-round permutation that hashes the sample; every other
operation is an ordinary 256-bit RAM primitive charged at 1/1355. The time cap
below is a worst-case bound over the algorithm's coins, and the success bound
is distribution-free. For context, `yukon benchmark show` reports the track's
current promoted best scalar as 137.785; this candidate's scalar is 129. The
relationship between the two is Yukon's incumbent comparison, not an assertion
this package makes about any qualified baseline.

## 1. Exact complete hash

Each message is exactly 64 bytes, of bit length 512 < 2^64. Two 256-bit words
u,v encode m=LE32(u)||LE32(v), where LE32 includes all 32 little-endian bytes,
including zeros. These encodings bijectively cover a domain D of size 2^512.
There is no unknown IV, free-start state, or supplied prefix/advice.

H is the following complete hash. Initialize a 1600-bit state to zero, as
25 lanes A[x,y] of 64 bits indexed x+5y. Pad m to the one 136-byte rate block

    m || 0x06 || (70 zero bytes) || 0x80.

This is SHA3's domain suffix 01 followed by pad10*1, with delimited suffix
0x06: the 64 message bytes occupy bytes 0..63, the delimited suffix byte 0x06
occupies byte 64, bytes 65..134 are zero (70 bytes), and the final block byte
135 is 0x80, for 64+1+70+1 = 136 bytes in total. There is no length trailer.
XOR the 17 little-endian 8-byte lanes of this block into A[0],...,A[16]. The
remaining eight capacity lanes are zero. Apply rounds 0,1,2,3,4, in order,
each with the following formulas; x,y and coordinate subscripts are modulo 5:

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

Let n = 5*2^126 = 1.25*2^128. A record is three 256-bit words (h,u,v), with h
the little-endian integer encoding of H(LE32(u)||LE32(v)). Unsigned comparison
of h is a total order whose equality is full digest equality. Use two flat
arrays A and B, each of n records, as the alternating source/destination of a
radix sort, and one counting array C of 2^16 counters.

1. For i=0,...,n-1, draw fresh independent uniform 256-bit words u and v,
   construct their 64-byte message, compute its complete H, and store
   (h,u,v) in A[i]. Retain repeated inputs; there is no resampling.
2. Sort the n records by the full 256-bit key h with a least-significant-
   digit radix sort using 16-bit digits (16 passes). For pass j = 0,...,15:
   (a) zero the 2^16 counters; (b) for each record in the source array, in
   order, extract digit j of h (bits 16j..16j+15) and increment its counter;
   (c) turn the counters into starting positions by a prefix sum; (d) for
   each record in the source array, in order, extract digit j, copy the whole
   record into the destination array at the position given by its counter,
   and increment that counter. Counting sort is stable, so after pass j the
   records are sorted by the low 16(j+1) bits of h, and after all 16 passes
   they are sorted by the full 256-bit h. Source and destination alternate
   between A and B each pass.
3. Scan all adjacent positions j-1,j in the final sorted array, from j=1
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

Every pass of the radix sort performs exactly n counting increments and
exactly n record copies, independent of the data values; the only data-
dependent quantities are the counter values, which only affect where records
are written, never how many operations are performed. The total operation
count of Steps 1-4 is therefore a deterministic function of n alone.

Record i starts at byte address base+96i, calculated as base+(i<<6)+(i<<5),
without multiplication. Word offsets are 0,32,64. Indices, counters, digit
positions and byte addresses are less than 2^138, far below 2^256. The value
n is made by 5*(1<<126). Message contents occupy two words; no 512-bit
single-word arithmetic is assumed. The proof's symbolic domain/codomain
cardinalities need not be represented in the machine.

## 3. Correctness of any returned collision

A stable counting sort by each 16-bit digit, from the least significant to
the most significant, sorts by the full 256-bit key: this is the standard
correctness invariant of least-significant-digit radix sort and holds for
every input multiset. Copying entire records preserves each digest's
associated message, so no record is created, deleted, or altered.

Every fixed digest occupies a contiguous interval in the sorted array. If
that interval contains distinct messages, some adjacent messages differ:
otherwise equality of every adjacent pair would make the entire interval one
repeated message by transitivity. Thus the scan finds a distinct-message
collision whenever the sample contains one, including samples with repeated
inputs. Repeated inputs alone are never accepted as collisions.

Every returned message is in the profile's allowed domain. The explicit final
checks establish inequality of the messages and equality of the entire
complete-message hash from Section 1. This is an ordinary collision, not a
compression-only, free-start, raw-permutation, truncated-output, or
different-round result.

## 4. Success for every fixed function

The sole probability space consists of 2n independent uniform 256-bit words
drawn in Step 1. Hence the messages M_1,...,M_n are independent uniform
samples from D. For fixed deterministic H, the Y_i=H(M_i) are iid with
probabilities

    p_y = |{m in D : H(m)=y}| / 2^512.

There are Q=2^256 possible output strings, including any with probability
zero. These probabilities may be arbitrarily nonuniform. Independence here
follows from applying a fixed function separately to independent inputs, not
from assuming independent internal rounds or assuming a randomly chosen hash.

For any probability vector p of length Q, let e_n(p) denote the sum of
products of n distinct coordinates. Independence gives

    Pr[all Y_i distinct] = n! e_n(p).

Uniform p maximizes e_n: a maximum exists by continuity on the compact
simplex, and among maximizers choose one minimizing the sum of squared
coordinates; if two coordinates a,b differ, averaging them leaves e_n
maximal (all coefficients in the expansion of e_n are nonnegative) while
strictly decreasing the sum of squares, a contradiction. Hence

    Pr[all Y_i distinct]
      <= Q(Q-1)...(Q-n+1)/Q^n
       = product_(j=0,...,n-1) (1-j/Q)
      <= exp(-n(n-1)/(2Q)).

Here n<Q and 1-t<=exp(-t) on 0<=t<1, obtained by integrating the derivative
-1/(1-t)<=-1 of log(1-t). With n = 1.25*2^128 and Q = 2^256,

    n(n-1)/(2Q) = (1.5625 * 2^256 - 1.25*2^128) / 2^257
                = 0.78125 - 1.25*2^-129
                > 0.78124,

so

    Pr[all Y_i distinct] <= exp(-0.78124) < 0.4579.

This also covers distributions with small support.

Let E be the event that some input messages repeat. The union bound gives

    Pr[E] <= n(n-1)/(2|D|) < 1.5625*2^256/(2*2^512) = 1.5625*2^-257 < 2^-256.

No independence of the pair-events is required. If outputs collide and E
does not occur, the algorithm succeeds. Thus

    Pr[success] >= 1 - Pr[all Y_i distinct] - Pr[E]
                > 1 - 0.4579 - 2^-256
                > 0.54.

This intentionally conservative bound proves the declared 0.5 and exceeds
the required 0.39. Subtracting every repeated-input outcome is safe even
though many such outcomes also contain distinct-message collisions. The
number concerns algorithmic success, not confidence in a proof or review.
The sorting and scanning work is identical on every outcome, so the success
event is exactly "the sample contains a distinct-message collision", and its
probability is the one bounded here.

## 5. Fully charged RAM implementation

One 256-bit word is 32 bytes. Under collision-frontier-v5, each selected
five-round permutation costs one unit and every other listed RAM primitive
costs 1/C units with C = 1355. All bounds include message construction,
failed samples, randomness, memory initialization, sorting, scanning,
verification, and fixed code/constants. There is no external disk,
unaccounted preprocessing service, whole-hash oracle, or free sorting step.

Code and fixed storage are bounded explicitly. The algorithm above can use
fewer than 100 loop-body statements outside the selected permutation, each
expandable into fewer than 64 primitive instruction templates. A direct
implementation of the displayed permutation formulas needs fewer than 2,000
additional templates, retaining a fixed loop over the five rounds; operations
on constant 64-bit lane positions use shifts, masks and fixed addresses. The
loops over records, digits and passes remain loops. A ceiling of 2^16
instruction templates therefore exceeds the required code. Encode each
template in at most four 256-bit words (opcode and up to three operands),
using separate primitive instructions for loads, stores and branches. Its
size is at most 2^23 bytes.

Reserve another 2^23 bytes for public target constants, working state,
register spills, loop counters, address variables, the current
message/record, verification scratch and final output. In particular the
permutation may keep 25 A lanes, 25 B lanes and 10 C/D lanes in individual
RAM words. Thus all fixed storage is at most 2^24 bytes, or 2^19 words. This
bound includes the program; no precomputed collision, target advice, large
lookup table or hidden runtime is present. The bound refers to the specified
RAM program, not Python or a host library. All fixed storage is initialized
and its cost is charged below.

The following large caps allow redundant copying, instruction decoding,
explicit operand loading/storing and address arithmetic. They do not depend
on treating high-level sort/serialization as unit-cost operations, and they
do not depend on the sampled data.

| Activity | Charged word-operation upper bound |
| --- | ---: |
| Initialize code, constants and fixed workspace | 2^24 |
| Generate, hash and store n records | 128n |
| 16 radix-sort passes | 16 * 32n = 512n |
| Scan adjacent records | 8n |
| Final reconstruction, verification and output | 2^18 |

For fixed initialization, 2^19 words with at most 16 word operations per
word costs at most 2^23, within the stated 2^24 cap. This loads the finite
explicit code and public constants; it does not assume a target-dependent
advice oracle.

Here is an explicit wrapper construction justifying 128 word operations per
generated record. Store each 64-bit lane in its own RAM word. Draw two random
words u and v (2 operations). The 64-byte message is eight 64-bit lanes:
lanes 0..3 are the four quarters of u, lanes 4..7 those of v, obtained by
shift and mask (16 operations). The initial state is rebuilt from a fixed
precomputed template that already holds the padding and capacity lanes (lane
8 = 0x06, lanes 9..15 = 0, lane 16 = 2^63, lanes 17..24 = 0): copy the 25-lane
template (at most 25 loads and 25 stores = 50) and overwrite the 8 message
lanes (8 stores). The digest is packed into one 256-bit word h from state
lanes 0..3 after the permutation (at most 16 operations). Storing the
three-word record costs at most 12 operations. Sample-loop control costs at
most 8 operations. The direct line count is

    2 (draws) + 16 (message lanes) + 58 (state rebuild) + 16 (pack)
    + 12 (store) + 8 (control) = 112,

and the claimed cap 128 adds headroom. Every selected permutation is charged
separately at one unit; its code and buffers are in the fixed reserve.

For the radix sort, each pass performs, per record, a counting sweep and a
distribution sweep. The counting sweep: load the key word h (1), extract the
16-bit digit (one shift and one mask = 2), form the counter address (one
shift and one add = 2), load the counter (1), increment it (1), store it (1),
and advance the record loop (increment, compare, branch = 3), for 11
operations. The distribution sweep: load h (1), extract the digit (2), form
the counter address (2), load the counter to get the destination index (1),
increment and store the counter (2), form the destination record address
base+(dest<<6)+(dest<<5) (two shifts and two adds = 4), copy the three-word
record (3 loads and 3 stores = 6), and advance the record loop (3), for 21
operations. That is 32 operations per record per pass, which the cap charges
in full. The per-pass counter zeroing is 2^16 stores and the prefix sum over
2^16 counters is at most 2^17 operations; over 16 passes this is
16*(2^16 + 2^17) < 2^21.5 operations in total, which is below 2^22 and is
absorbed into the 512n cap since 512n > 2^22 for n = 1.25*2^128. The scan
loads two adjacent records' keys and messages, compares, and branches: at
most 8 operations per pair, hence 8n.

Final verification uses at most two complete hash wrappers, message
distinctness, full digest comparisons and output serialization: less than
2*128 + 1024 < 2^18 word operations and 2 further permutations. There is no
restart cost because no restart occurs.

Summing all phases, including the cost of batches that fail to find a
collision, the total charged time in units is

    T <= (n + 2) * 1 + (128n + 512n + 8n + 2^24 + 2^18) / 1355
       = (n + 2) + (648n + 2^24 + 2^18) / 1355.

With n = 1.25*2^128,

    (n + 2)                  < 1.2500001 * 2^128,
    648n / 1355              = 810 * 2^128 / 1355
                             < 0.5978 * 2^128,
    (2^24 + 2^18)/1355       < 2^14,

so

    T < (1.2500001 + 0.5978) * 2^128 + 2^14
      < 1.8479 * 2^128 + 2^14
      < 1.8479 * 2^128 * (1 + 2^-110)
      < 2^128.89
      < 2^129.

This is a deterministic worst-case charged-time cap on the randomized
algorithm: the operation counts above do not depend on the sampled data, the
output distribution, or any probabilistic concentration. The dominant term is
the n selected permutations plus the data-independent sorting work.

Each array uses n*3*32 = 96n bytes, so the two record arrays use 192n bytes.
The counting array uses 2^16 words = 2^21 bytes. With all fixed storage
included,

    peak bytes <= 192n + 2^21 + 2^24
               = 240 * 2^128 + 2^21 + 2^24
               < 2^135.91 + 2^25
               < 2^136.

The arrays contain every retained message, digest and sampled random word.
There is no extra index array, recursion, message database or per-record
pointer. The reserve includes all temporary randomness, state,
code/constants, verification state and final output. The arrays and the
reserve fit below byte address 2^137. This validates the one-word
pointer/counter assumption. The memory figure is an abstract RAM allowance,
not a claim of physical feasibility.

The claim fields have these precise meanings:

- time_log2=129 bounds total charged time by 2^129 units.
- memory_log2_bytes=136 bounds simultaneous storage by 2^136 bytes.
- data_log2=129 bounds complete-hash evaluations by n+2 <= 2^129, including
  the two final re-evaluations. It counts evaluated message instances, not
  bytes or distinct messages. Every repeated sample is counted; external
  supplied data is zero and all retained data bytes are in peak memory.
- preprocessing_log2=120 bounds fixed setup plus counter-array
  initialization: (2^24 + 16*(2^16 + 2^17))/1355 < 2^14 < 2^120 units. It is
  already included in T, not an omitted phase.
- nonuniform_advice_log2_bytes=0 means at most 2^0=1 byte of advice; actual
  nonuniform advice is zero. The schema cannot express log2(0). Public
  constants and code are fully charged in the fixed storage and
  initialization.
- success_probability=0.5 is the lower bound proved in Section 4.

## 6. Evidence and interpretation

This is a conservative generic attack, not a new cryptanalytic advance. The
complete algorithm, target definition, probability proof and RAM ledger are
the supporting evidence. No full-scale execution, observed collision pair,
measured success rate, experimental independence or measured resource usage
is asserted. No sampled experiment is needed: the success argument is a
universal finite probability bound, and the time argument is a deterministic
data-independent operation count. The certificate manifest is valid and
empty; no experiment manifest or participant executable is supplied.

The required baseline_improved identifier sha3-256-r5-nominal-v2 names the
organizer's nominal display reference 128. It is not an established attack,
qualified baseline or security bound; the identifier's field name is not a
claim of improvement. This candidate's scalar bound 129 exceeds 128. No
Pareto dominance claim follows from scalar scoring.

submission_state=ready means this independent exploratory package is complete
for review. It does not assert an actual qualifying review, an emitted score,
human acceptance, or Yukon promotion. Its substantive obligations and
evidence are intended to meet rigorous standards, while each lane still
requires its own correctly bound package and selected-lane review outcome.
