# Distribution-free SHA3-256/6 collision by radix-sorted birthday sampling

## 1. Target definition

Profile `sha3-256-r6-prefix-v1` instantiates `sha3-256-standard-v1` with
`rounds=6`. The selected target is the complete SHA3-256 hash of a message,
with Keccak-f[1600] reduced to its first 6 rounds in every permutation call.
It is not a raw permutation output, a compression-only result, a free-start
result, or a truncated-output result.

The rate is r=1088 bits and the capacity is c=512 bits. The state is 25 lanes
of 64 bits, stored as the low 64 bits of 25 separate 256-bit RAM words. Index
lanes as A[x+5y]. A complete evaluation does all of the following.

1. Zero all 25 lanes.
2. Absorb the message under multi-rate padding 10*1. For the two-word messages
   used below, the padded rate block is the eight little-endian 64-bit lanes of
   the two 256-bit words, followed by a 0x06 byte in lane 8 and the SHA3
   domain-separation bit in lane 16 (the high bit of the rate, value
   2^63 in that lane). No other lane is nonzero. The message length is 64
   bytes, which is less than the rate, so there is exactly one permutation call.
3. Apply the first 6 rounds of Keccak-f[1600], in the standard round order,
   starting from round index 0. Each round is theta, rho, pi, chi, iota, with
   the standard rotation offsets, pi rearrangement, and round constants. Rounds
   6 through 23 are not computed.
4. Squeeze 256 bits: the first four lanes after the permutation, interpreted
   as a little-endian 256-bit string. All 256 bits are retained. There is no
   second permutation call.

Denote this function by H. Its domain restriction below is every pair of
256-bit words, hence |D|=2^512. Two messages collide when they differ as
512-bit strings and H returns identical 256-bit strings. That is an ordinary
collision of the selected complete hash.

The machine is the classical probabilistic 256-bit word RAM of
`collision-frontier-v5`. One selected 6-round permutation costs 1. Every other
listed primitive costs 1/C, with C=1626 for `sha3-256-r6`. The listed
primitives are 256-bit load/store, addition or subtraction modulo 2^256,
bitwise AND/OR/XOR/NOT, shift or rotation, comparison, conditional branch,
and an independent uniform 256-bit word. Multiplication is not a primitive
and is not used. Address arithmetic uses shifts and adds.

## 2. Algorithm

Set n=2^129. A record is three 256-bit words (h,u,v), with h the little-endian
integer encoding of H(LE64 lanes of u, then v), as defined in Section 1.
Unsigned comparison of h is a total order whose equality is full digest
equality. Use two flat arrays A and B, each of n records. Explicitly
initialize all six words per index across the two arrays. Allocation and
initialization are charged.

1. For i=0,...,n-1, draw fresh independent uniform 256-bit words u and v,
   construct their 64-byte message, compute its complete H, and store (h,u,v)
   in A[i]. Retain repeated inputs. There is no resampling.
2. Sort by the full h using stable least-significant-digit radix sort, with A
   and B as alternating source and destination arrays. For shifts
   s=0,32,64,96,128,160,192,224, counting-sort every record on the digit
   (h >> s) AND 0xFFFFFFFF. Copy all three words of every record, and exchange
   the two array base pointers at the end of each pass. Exactly 8 passes each
   read and write exactly n records. A separate count array of 2^32 words is
   cleared and prefix-summed on every pass.
3. Scan adjacent positions j-1,j in the sorted source array, from j=1 through
   n-1. Test h equality and inequality of the pair (u,v), testing both message
   words. On the first qualifying pair, reconstruct both messages and recompute
   both complete hashes from the all-zero state. Check message distinctness
   and equality of all 256 recomputed output bits. Return the two messages if
   verified; otherwise halt with failure.
4. If the scan finishes without such a pair, halt with failure.

There is one batch, no restart, and at most one final verification of two
messages. Verification failure cannot occur for a correct implementation of H,
because the stored digests came from the same deterministic function. The
defensive recomputation is still charged. Every outcome halts within the same
budget.

For a concrete radix pass at a fixed shift s, clear the 2^32 counters, then
for i=0,...,n-1 load the source record's h, set d=(h >> s) AND 0xFFFFFFFF, and
increment count[d]. Replace count by its exclusive prefix sums. Then for
i=0,...,n-1 again, recompute d, write all three words of the source record to
the destination slot count[d], and increment that counter. Swap the source and
destination base pointers. Digit shifts are the eight constants above. The
mask is the low 32 bits. Address of count[d] is count_base+(d<<5). Address of
record i is base+(i<<6)+(i<<5), which is base+96i, with no multiplication.
The scatter half writes every record exactly once. There is no recursive stack
and no library sort.

Indices, counters, digit shifts, and byte addresses used by this program are
less than 2^138, far below 2^256. The value n is made by 1<<129. Message
contents occupy two words. The proof's symbolic domain and codomain
cardinalities need not be represented in the machine.

## 3. Correctness of any returned collision

Counting sort on one digit writes every record exactly once, at the position
given by the exclusive prefix sum of its digit, so it is a permutation of the
input records. Scanning left to right makes it stable. Composing eight stable
digit sorts from the low digit to the high digit therefore sorts every record
by the full 256-bit digest. Induction over the passes preserves every original
record.

Every fixed digest occupies a contiguous interval in the sorted array. If that
interval contains distinct messages, some adjacent messages differ: otherwise
equality of every adjacent pair would make the entire interval one repeated
message by transitivity. Thus the scan finds a distinct-message collision
whenever the sample contains one, including samples that also contain repeated
inputs. Repeated inputs alone are never accepted as collisions.

Every returned message is in the domain of Section 1. The explicit final checks
establish inequality of the messages and equality of the entire complete-hash
output. This is an ordinary collision of 6-round SHA3-256, not a
permutation-only, free-start, capacity-only, or truncated-output result.

## 4. Success for every fixed function

The sole probability space consists of the 2n independent uniform 256-bit words
drawn in Step 1. The messages M_1,...,M_n are therefore independent uniform
samples from D. For fixed deterministic H, the outputs Y_i=H(M_i) are iid with

    p_y = |{m in D : H(m)=y}| / 2^512.

There are Q=2^256 possible output strings, including any with probability zero.
These probabilities may be arbitrarily nonuniform. Independence follows from
applying a fixed function separately to independent inputs. It does not assume
independent internal rounds or a randomly chosen hash.

For any probability vector p of length Q, let e_n(p) denote the elementary
symmetric sum of degree n. Independence gives

    Pr[all Y_i distinct] = n! e_n(p).

Uniform p maximizes e_n. A maximum exists by continuity on the compact simplex.
Among maximizers, choose one minimizing the sum of squared coordinates. If two
coordinates a,b differ, replace them by their average. With the other
coordinates collected as r,

    e_n(p) = ab e_(n-2)(r) + (a+b) e_(n-1)(r) + e_n(r).

All three coefficients are nonnegative, so the average does not decrease e_n,
while the sum of squares strictly decreases. This contradicts the choice.
Therefore the maximizer is uniform, and

    Pr[all Y_i distinct]
      <= Q(Q-1)...(Q-n+1)/Q^n
       = product_(j=0,...,n-1) (1-j/Q)
      <= exp(-n(n-1)/(2Q))
       = exp(-(2-2^-128))
      < exp(-1).

Here n<Q, and 1-t<=exp(-t) on 0<=t<1 follows by integrating the derivative
-1/(1-t)<=-1 of log(1-t). This covers distributions with small support.

Let E be the event that some input messages repeat. The union bound gives

    Pr[E] <= n(n-1)/(2|D|) < 2^258/(2*2^512) = 2^-255.

No independence of the pair events is required. If some outputs collide and E
does not occur, Section 3 says the scan returns a valid collision. Thus

    Pr[success] >= 1 - Pr[all Y_i distinct] - Pr[E]
                > 1 - exp(-1) - 2^-255
                > 1/2.

Indeed e=sum_(k>=0) 1/k! > 8/3, so exp(-1)<3/8, and 2^-255<1/8. Subtracting
every repeated-input outcome is safe even though many such outcomes also
contain a distinct-message collision. The number 0.5 is an algorithmic success
probability, not a confidence level in the proof. It exceeds the required 0.39.

## 5. Fully charged RAM implementation

One selected 6-round permutation costs 1. Every other listed primitive costs
1/C with C=1626. The bounds below include message construction, failed samples,
randomness, memory initialization, sorting, the count array, verification, and
fixed code. There is no external disk, unaccounted preprocessing service,
whole-hash oracle, or free sorting step.

Code and fixed storage are bounded explicitly. The algorithm can use fewer than
100 loop-body statements outside the selected permutation, each expandable into
fewer than 64 primitive instruction templates. A direct implementation of the
6-round Keccak formulas needs fewer than 4,000 additional templates for the
fixed round index, rotation offsets, pi map, and round constants. A ceiling of
2^16 instruction templates exceeds the required code. Encode each template in
at most four 256-bit words. Its size is at most 2^23 bytes. Reserve another
2^23 bytes for public constants, the 25-lane state, register spills, loop
counters, address variables, the current message, verification scratch, and
final output. Fixed storage is therefore at most 2^24 bytes. This bound
includes the program. It contains no precomputed collision, target advice, or
hidden runtime. The 2^32-word count array is zeroed workspace outside this
2^24 reserve. Its bytes and initialization are charged in the peak-memory and
2^40 terms below.

The following caps allow redundant copying, instruction decoding, explicit
operand traffic, and address arithmetic. They do not treat sorting as a
unit-cost library call.

| Activity | Charged-operation upper bound |
| --- | ---: |
| Initialize code, constants, and fixed workspace | 2^30 |
| Zero both record arrays | 2^12 n |
| Generate, hash, and retain n messages | 2^12 n |
| Exactly 8 radix passes | 8 * 1024 n |
| Count-array clear and prefix sums, all passes | 2^40 |
| Scan adjacent records | 2^12 n |
| Final reconstruction, verification, and output | 2^14 |

Zeroing six words per index, with address arithmetic and loop control, is
within 512 primitives before a fetch allowance of five extra loads per
executed instruction. That product is 3072, rounded up to 4096. The same
4096 cap covers generation of one record excluding the permutation call:
25 lane clears, eight lane extractions by shifts and masks, two padding
stores, copying the 25 lanes to and from the permutation interface, four
output-lane loads, three shifts or ORs, two random draws, three record stores,
and sample-loop control. The promoted merge-sort proof for this same target
already used this 4096 generation and scan cap. It is retained here. The one
selected permutation per generated message, and the two verification
permutations, are charged in H, not in this table.

A radix pass moves one record with fewer than 64 enumerated primitives across
the count loop and the scatter loop together: form base+(i<<6)+(i<<5), load
h, shift by the pass's constant, mask, form count_base+(d<<5), update one
counter, then on the scatter loop reload the three record words and store them
at the exclusive prefix-sum slot. Sixty-four primitives with five fetch loads
each is 384. The charged cap is 1024 per record per pass, more than twice that
enumeration, which also pays for instruction fetch, spills, and redundant
address reloads. Eight passes therefore cost at most 8192 n. This is the same
1024 cap accepted for the blake3-r2 radix package, and it is tighter than the
4096 merge-output cap of the promoted SHA3 proof. Clearing and prefix-summing
2^32 counters takes at most 32 primitives per counter, so eight passes cost at
most 8*32*2^32=2^40 word operations in total, not per record. Final
verification is two hash wrappers, message distinctness, full digest
comparison, and output stores, bounded by 2^14 as in the promoted proof.
There is no restart cost.

Separate the two disjoint categories. Target permutations are the n hashes of
Step 1 plus the two verification hashes:

    H = n + 2.

All remaining listed RAM primitives are bounded by the table. With n=Q_sample
written Q=2^129 below, and K=2^40+2^30+2^14,

    W <= (4096 + 4096 + 8*1024 + 4096) Q + K
       = 20480 Q + K.

The v5 charged time is T=H+W/C. The integer comparison used below is the
claimed ceiling. It is a deterministic worst-case cap on the randomized
algorithm, not an expected-time bound and not a cost conditional on favorable
trials.

## 6. Integer proof that T < 2^132.8

Let Q=2^129 and C=1626. Then

    C*H + W <= 1626(Q+2) + 20480 Q + K
             = 22106 Q + 3252 + K.

Since 22106/1626 = 11053/813,

    T <= (11053/813) Q + (3252+K)/1626.

The constant is K=2^40+2^30+2^14, so

    3252+K = 1100585389236
    1626*2^31 = 3491808411648.

The first is strictly smaller, hence (3252+K)/1626 < 2^31 and

    T < (11053/813) Q + 2^31
      = (11053 Q + 813*2^31) / 813.

Let S = 11053*2^98 + 813. Then 11053 Q + 813*2^31 = 2^31*S. Also

    S < 11054*2^98 = 5527*2^99,

because 11054=2*5527, so 11053 Q + 813*2^31 < 5527*2^130. Raising this
positive bound to the fifth power gives

    (11053 Q + 813*2^31)^5 < 5527^5 * 2^650.

The fifth-power comparison T < 2^132.8 is equivalent to

    (11053 Q + 813*2^31)^5 < 813^5 * 2^664,

because 132.8*5=664. It is therefore enough to show

    5527^5 * 2^650 < 813^5 * 2^664,

which cancels to 5527^5 < 813^5 * 2^14. The products are:

    5527^2 = 30547729
    5527^3 = 168837298183
    5527^4 = 933163747057441
    5527^5 = 5157596029986476407
    813^2 = 660969
    813^3 = 537367797
    813^4 = 436880018961
    813^5 = 355183455415293
    813^5 * 2^14 = 5819325733524160512.

The last quantity is strictly larger, so T < 2^132.8. The same envelope is
also below 2^133 by the shorter comparison 26016 Q - 22106 Q = 3910 Q >
3252+K, since 1626*2^133 = 26016 Q and 3910 Q > 2^140 > 3252+K. The submitted
scalar is the fractional ceiling, not that integer.

A direct evaluation of this same closed form, not used as a premise, is
log2(T)=132.76504. The submitted 132.8 sits strictly above it.

Replacing the 1024 radix cap by the promoted proof's 4096 cap changes 20480 to
11*4096=45056 and gives log2(T)=133.84347. That figure is not a valid ceiling
at 133.843, because the exact value is larger than 133.843. It is recorded only
to retire that truncated reading. This package does not submit it.

## 7. Memory and the other claim fields

Each record array uses n*3*32=96n bytes. Both arrays use 192n bytes. The count
array uses 2^32 words, hence 2^37 bytes. It is zero-initialized workspace, not
target advice and not a precomputed table. With the 2^24 fixed reserve,

    peak bytes <= 192 Q + 2^37 + 2^24.

Now 192 Q = 3*2^135, and 2^137 - 3*2^135 = 2^135 > 2^37+2^24, so the peak is
strictly below 2^137 bytes. Both arrays, the count array, and the reserve fit
below byte address 2^138, which validates the one-word pointer assumption.
The memory figure is an abstract RAM allowance, not a claim of physical
feasibility.

- time_log2=132.8 bounds total charged v5 time by 2^132.8, as proved in
  Section 6. The promoted merge-sort package on this track claims 137.4. Its
  own inequality has exact log2 137.38161, which 132.8 improves.
- memory_log2_bytes=137 bounds simultaneous storage by 2^137 bytes.
- data_log2=130 bounds complete-hash evaluations by n+2<2^130, including the
  two final re-evaluations. It counts evaluated messages, not bytes. It is not
  a scored resource.
- preprocessing_log2=131 bounds fixed setup, both-array initialization, and
  the eight count-array clears after v5 pricing. Their word-operation count is
  at most 2^12 Q + 2^30 + 2^40. This is less than 1626*2^131 = 6504 Q, because
  4096 Q + 2^41 < 4097 Q < 6504 Q. This work is already inside T. It is not an
  omitted phase.
- nonuniform_advice_log2_bytes=0 means at most one byte of advice. Actual
  nonuniform advice is zero. The schema cannot express log2(0). Public
  constants and code are charged in fixed storage.
- success_probability=0.5 is the lower bound proved in Section 4.

The required baseline identifier `sha3-256-r6-nominal-v2` names the organizer
nominal reference of 128. This package does not improve that reference.
132.8 is below the promoted exploratory package's 137.4 and above 128.

## 8. What this does not claim

No full-scale execution was performed, and no colliding message pair was
computed. The certificate list is empty. An empty list is not evidence of a
collision. The supporting evidence is the algorithm, the target definition,
the probability argument, and the RAM ledger above.

This is a classical generic birthday bound with an explicit matching
implementation. It is not a differential, algebraic, or structural attack on
6-round Keccak, and it does not use the unused capacity bits as a free
collision degree of freedom beyond the charged 2^512-element domain. A later
structural attack can replace this package. A hash-table or Markov filter is
not substituted, because the cost model requires a worst-case charged cap
rather than an expected-time bound.

The promoted 137.4 proof charges 129 merge passes at 2^12 primitives per
record. This proof deletes those passes and charges eight radix passes plus
the count array instead. Every other target convention is unchanged.
