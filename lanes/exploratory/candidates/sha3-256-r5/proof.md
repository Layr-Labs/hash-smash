# A fixed-function collision baseline for five-round SHA3-256

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains
a separately reported resource bound.

This independent exploratory package targets sha3-256-r5-prefix-v1. It proposes
a classical randomized algorithm with success at least 0.39, total charged time
at most 2^128.264 units, and peak memory at most 2^136 bytes under
collision-frontier-v5. These are conservative analytical upper bounds, not
measured execution costs. The claimed scalar is 128.264.

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

Set n=2^128. A record is three 256-bit words (h,u,v), with h the little-endian
integer encoding of H(LE32(u)||LE32(v)). Unsigned comparison of h is a total
order whose equality is full digest equality. Use two flat arrays A and B,
each of n records, and one auxiliary array S of 2^128 256-bit counter words.

1. For i=0,...,n-1, draw fresh independent uniform 256-bit words u and v,
   construct their 64-byte message, compute its complete H, and store
   (h,u,v) in A[i]. Retain repeated inputs; there is no resampling.
   Generation writes every record slot of A exactly once, so A needs no
   pre-initialization.
2. Sort A by full h with a stable least-significant-digit radix sort using
   two counting-sort passes on 128-bit digits. Pass one sorts by the low
   128 bits of h from A into B; pass two sorts by the high 128 bits of h
   from B into A. Each pass first zeroes all 2^128 counters of S, counts
   digit occurrences into S, transforms S into starting offsets by an
   in-place prefix sum, then scatters every record to its offset, which
   increments the offset. Scatter writes every slot of the destination
   array exactly once because the offsets partition [0,n); therefore B
   needs no pre-initialization either. Counter zeroing and prefix-sum
   work is charged explicitly per pass in Section 5.
3. Scan all adjacent positions j-1,j in the sorted array, from j=1
   through n-1. Test h equality and, on equality, inequality of the pair
   (u,v), testing both message words. On the first qualifying pair,
   reconstruct both messages and recompute both complete hashes from the
   all-zero state. Check message distinctness and equality of all 256
   recomputed output bits. Return the two messages if verified; otherwise
   halt with failure.
4. If the scan finishes without such a pair, halt with failure.

There is one batch, no restart, and at most one final verification of two
messages. Verification failure cannot occur in the exact RAM model because
the original digests came from the same deterministic H. This explicit
defensive check is still charged. Every outcome halts within the same budget.

For a concrete counting-sort pass: zero S with a linear store loop. Then for
each record in source order, load its h, extract the digit by one mask
(low pass) or one shift (high pass), compute the counter byte address as
sbase+(digit<<5), load the counter, add one, and store it. Then prefix-sum
S in place with one running accumulator: load counter, add accumulator,
store sum, advance. Then scatter: for each record in source order, load h,
extract the digit, compute the counter address, load the offset, compute
the destination byte address as base+(offset<<6)+(offset<<5), store all
three record words there, increment the stored offset, and advance.
Stability holds because records are scattered in source order and each
bucket's offset increases per insertion. All boundaries are exact; the
counters, offsets and byte addresses are below 2^136, far below 2^256.
There is no recursive stack or library sort, and no multiplication
instruction is used.

Record i starts at byte address base+96i, calculated as
base+(i<<6)+(i<<5), without multiplication. Word offsets are 0,32,64.
Indices, counters, accumulators and byte addresses are less than
2^136, far below 2^256. The value n is made by 1<<128. Message contents
occupy two words; no 512-bit single-word arithmetic is assumed. The
proof's symbolic domain/codomain cardinalities need not be represented in
the machine.

## 3. Correctness of any returned collision

Stability of each counting-sort pass is shown above. The standard
least-significant-digit radix invariant then applies: after pass one the
records are ordered by the low 128 key bits, and after the stable second
pass they are ordered by the high 128 bits with ties broken by the low
bits, hence by the full 256-bit h. Scattering preserves each digest's
associated message words, and the offset partition property places all n
original records, deleting none.

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
contradicts the choice. The maximizing vector is therefore uniform, and with
n=2^128,

    Pr[all Y_i distinct]
      <= Q(Q-1)...(Q-n+1)/Q^n
       = product_(j=0,...,n-1) (1-j/Q)
       <= exp(-n(n-1)/(2Q))
       = exp(-(1/2 - 2^-129)).

Here n<Q and 1-t<=exp(-t) on 0<=t<1, obtained by integrating the derivative
-1/(1-t)<=-1 of log(1-t). The exponent equality uses
n(n-1)/(2Q)=(2^256-2^128)/2^257=1/2-2^-129. This also covers distributions
with small support.

To bound the right side elementarily, the series e=sum_(k>=0)1/k! exceeds
its partial sum 685/252=2.718253968..., and two exact integer checks give

    252/685 < 3678908/10^7,
      because 252*10^7 = 2520000000 < 2520051980 = 685*3678908;
    3678908/10^7 < (0.606542)^2,
      because 3678908*10^5 = 367890800000 < 367893197764 = 606542^2.

Hence e^(-1/2) < (252/685)^(1/2) < 0.606542. Also
e^x<=1+2x on 0<=x<=1, since e^x=1+x+x^2/2+...<=1+x+x^2 there. With
x=2^-129 this gives exp(2^-129)<=1+2^-128, so

    Pr[all Y_i distinct] <= 0.606542*(1+2^-128) < 0.606543.

Let E be the event that some input messages repeat. The union bound gives

    Pr[E] <= n(n-1)/(2|D|) < 2^256/(2*2^512) = 2^-257.

No independence of the pair-events is required. If outputs collide and E
does not occur, the algorithm succeeds. Thus

    Pr[success] >= 1 - Pr[all Y_i distinct] - Pr[E]
                > 1 - 0.606543 - 2^-257
                > 0.3934.

This intentionally conservative bound proves the declared 0.39 and exceeds
the required 0.39. Subtracting every repeated-input outcome is safe even
though many such outcomes also contain distinct-message collisions.
The number concerns algorithmic success, not confidence in a proof or review.

## 5. Fully charged RAM implementation

One 256-bit word is 32 bytes. Each selected five-round permutation costs one
unit; every other listed RAM primitive costs 1/1355 units. Ordinary-operation
counts W below are separate from permutation calls H_calls. The permutation's
internal rounds are not counted again in W. All bounds include
message construction, failed samples, randomness, counter-array zeroing,
sorting, verification, and fixed code/constants. There is no external disk,
unaccounted preprocessing service, whole-hash oracle, or free sorting step.
Neither record array nor the destination of a scatter pass is
pre-initialized; Sections 2 and 3 show each is fully written before any read.

Code and fixed storage are bounded explicitly. The algorithm above can use
fewer than 100 loop-body statements outside the selected permutation, each
expandable into fewer than 64 primitive instruction templates. A direct
implementation of the displayed permutation formulas needs fewer than 2,000
additional templates, retaining a fixed loop over the five rounds; operations
on constant 64-bit lane positions use shifts, masks and fixed addresses. The
loops over records, counters and the two passes remain loops. A ceiling of
2^16 instruction templates therefore exceeds the required code. Encode each
template in at most four 256-bit words (opcode and up to three operands),
using separate primitive instructions for loads, stores and branches. Its
size is at most 2^23 bytes.

Reserve another 2^23 bytes for public target constants, working state,
register spills, loop counters, address variables, the current message/records,
verification scratch and final output. In particular the permutation may keep
25 A lanes, 25 B lanes and 10 C/D lanes in individual RAM words. Thus all fixed
storage is at most 2^24 bytes, or 2^19 words. This bound includes the program;
no precomputed collision, target advice, large lookup table or hidden runtime
is present. The counter array S is working data charged in memory and its
maintenance is charged per pass below; it is not advice. The bound refers to
the specified RAM program, not Python or a host library. All fixed storage is
initialized and its cost is charged below.

The following caps allow redundant operand access, address arithmetic and
loop control. They do not depend on treating high-level sort/serialization
as unit-cost operations.

| Activity | Permutation calls, at cost 1 each | Ordinary operations, at cost 1/1355 each |
| --- | ---: | ---: |
| Initialize code, constants and all fixed workspace | 0 | 2^24 |
| Generate, hash and retain n messages | n | 128n |
| Two radix passes including counter zero and prefix sums | 0 | 128n |
| Scan adjacent records | 0 | 16n |
| Final reconstruction, verification and output | at most 2 | 2^18 |

The counts in the last column are ordinary-operation envelopes; their
operand loads/stores, address arithmetic and spare allowance are retained.
The permutation calls in the middle column are priced independently.

For fixed initialization, processing 2^19 words at at most 16 ordinary
operations per word takes at most 2^23 operations, within the stated 2^24 cap.
This loads the finite explicit code and public constants; it does not assume
a target-dependent advice oracle.

Here is an explicit wrapper construction justifying 128 per generated
record. The message m=LE32(u)||LE32(v) is exactly eight 8-byte lanes:
lanes 0-3 come from u and lanes 4-7 from v. Extract each lane by one shift
and one mask: 16 operations. The padded block's 17 rate lanes are these
eight, the constant 0x06 at lane 8, zero at lanes 9-15, and the constant
0x80<<56 at lane 16. Store all 17 rate lanes and zero the 8 capacity lanes:
25 stores; this fully reinitializes the per-call state, so no separate
clearing pass exists. After the selected permutation, load the four output
lanes and pack h with three shifts and three ORs: 10 operations. Two
random-word draws, three record stores with one running-pointer increment,
and sample-loop increment/compare/branch take 2+4+3. The explicit total is
2+16+25+10+4+3=60 ordinary operations. The 128n envelope is more than
twice this inventory and absorbs any instruction/operand access
double-counting; add one target-permutation unit per hash. The
permutation's code and buffers remain in the fixed reserve.

For each radix pass, the explicit per-record count is as follows. Counting:
load h (1), extract digit by one mask or one shift (1), counter address by
one shift and one add (2), load counter (1), increment (1), store (1),
record-pointer increment (1), loop compare and branch (2): 10. Scatter:
load h (1), extract digit (1), counter address (2), load offset (1),
destination address (offset<<6)+(offset<<5)+base by two shifts and two adds
(4), three record stores (3), offset increment and store (2),
record-pointer increment (1), loop compare and branch (2): 16. Each pass
takes 26n record operations. Counter maintenance per pass is charged
separately and explicitly: zeroing all 2^128 counters takes 4 per word
(store, pointer increment, compare, branch), that is 4n per pass; the
in-place prefix sum takes 6 per word (load, add, store, pointer increment,
compare, branch), that is 6n per pass. Two passes therefore cost
2*(26+4+6)n=72n ordinary operations. The 128n envelope exceeds this
explicit 72n by a factor above 1.7 and covers redundant operand handling
and pass setup; the counter zeroing and prefix sums are not absorbed into
or justified by the per-record envelope, they are counted in it.

The scan examines each adjacent pair once. The unequal branch takes two
digest loads, one comparison, one branch, one index increment, and loop
compare/branch: 7. The equal-h branch additionally loads all four message
words and performs both comparisons and the branch: at most 14 per pair.
If the messages are distinct the scan halts into verification, so a full
14-charge pair repeats only on identical inputs; regardless of that
frequency the scan costs at most 14(n-1)<16n operations in every outcome,
including batches that find no collision.

Final verification uses at most two complete hash wrappers, message
distinctness, full digest comparisons and output serialization: less than
2*128+1024<2^18 ordinary operations, plus two permutation calls.
There is no restart cost because no restart occurs.

Summing all phases, including the cost of batches that fail to find a
collision,

    H_calls <= n+2
    W <= (128 + 128 + 16)n + 2^24 + 2^18
       = 272n + 17039360
    T = H_calls + W/1355
      <= (1 + 272/1355)n + 2 + 17039360/1355
       = (1627/1355)n + 12577.2
       < (1627/1355)n + 2^14.

The final inequality uses 17039360/1355<12576 and 2+12576<2^14.
Three integer-checkable steps complete the bound. First,
1627*100000=162700000<162704335=120077*1355, so 1627/1355<120077/100000.
Second,

    (120077/100000 - 1627/1355) * 2^128
      = (4335/135500000) * 2^128
      > 2^14,

because 4335>2^12 and 2^14*135500000=2220032000000<4398046511104=2^42,
so 4335*2^128>2^140>2^42>2^14*135500000. Therefore

    T < (120077/100000) * 2^128.

Third, (120077/100000)^125 < 2^33, equivalently
120077^125 < 2^33 * 10^625: the left side has
log10 = 125*log10(120077) = 125*5.07945983 = 634.9324786, while the right
side has log10 = 33*log10 2 + 625 = 9.93398986+625 = 634.9339899, a strict
integer inequality decidable by exact arithmetic. Taking 125th roots gives
120077/100000 < 2^(33/125) = 2^0.264. Hence

    T < 2^0.264 * 2^128 = 2^128.264,  for n=2^128.

This rounds upward with the fixed setup and final verification included,
not just the leading coefficient (1627/1355 = 1.200738007...). No old
rounded total is divided by C. This is a deterministic worst-case
charged-time cap on the randomized algorithm, not merely a birthday
exponent or a conditional cost given favorable trials.

Each record array uses n*3*32=96n bytes. The counter array uses
2^128 words of 32 bytes, that is 2^133 bytes. With all fixed storage
included,

    peak bytes <= 192n + 2^133 + 2^24
               = 3*2^134 + 2^133 + 2^24
               < 3*2^134 + 2^133 + 2^133
               = 4*2^134
               = 2^136.

Here 192n=3*2^134 because 192=3*2^6, and the strict step uses 2^24<2^133.
The arrays contain every retained message, digest and sampled random word.
There is no extra index array, recursion, message database or pointer per
record. The reserve includes all temporary randomness, state,
code/advice/constants, verification state and final output. All storage
lies below byte address 2^136, far below 2^256. This validates the
one-word pointer/counter/accumulator assumption. The memory figure is an
abstract RAM allowance, not a claim of physical feasibility.

The claim fields have these precise meanings:

- time_log2=128.264 bounds total charged time by 2^128.264 units.
- memory_log2_bytes=136 bounds simultaneous storage by 2^136 bytes.
- data_log2=129 bounds complete-hash evaluations by n+2<=2^129, including
  the two final re-evaluations. It counts evaluated message instances, not
  bytes or distinct messages. Every repeated sample is counted; external
  supplied data is zero and all retained data bytes are in peak memory.
  Under the current review policy this legacy field is not a scored or
  reviewed resource bound.
- preprocessing_log2=14 bounds fixed setup: at most 2^24 ordinary
  operations, and (2^24)/1355<2^14 target-compression units. The record
  arrays need no initialization, as Sections 2 and 3 explain, and the
  counter-array zeroing is charged inside the radix envelope in the main
  ledger, not omitted to preprocessing.
- nonuniform_advice_log2_bytes=0 means at most 2^0=1 byte of advice; actual
  nonuniform advice is zero. The schema cannot express log2(0). Public
  constants and code are fully charged in the fixed storage and initialization.
- success_probability=0.39 is below the lower bound 0.3934 proved in
  Section 4 and equals the required minimum; the proof establishes strictly
  more than the claim.

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
claim of improvement. This candidate's scalar bound 128.264 exceeds 128. No
Pareto dominance claim follows from scalar scoring.

submission_state=ready means this independent exploratory package is complete
for review. It does not assert an actual qualifying review, an emitted score,
human acceptance, or Yukon promotion. Its substantive obligations and evidence
are intended to meet rigorous standards, while each lane still requires its own
correctly bound package and selected-lane review outcome.

## 7. Source and accounting revision

This is an accounting revision of the organizer's SHA3-256 r5 merge-sort
package `79dcf0c2f0e1b4448c0cdf2f77b769a59ae738c637e07b120bc451be9af50ec7`
in production base `0455d2b52f4f920fe5c3a6af8c71592a824e6a57`.
The complete hash specification, 64-byte two-word messages, three-word
records, fixed-function probability argument and success-lower-bound
technique are retained. Three changes tighten the bound:

- The batch size drops from 2^129 to 2^128. Section 4's proof still gives
  success above 0.3934, exceeding the required 0.39. Halving n halves both
  the permutation calls and the per-pass record work.
- The 129-pass merge sort (charged 129*4096n ordinary operations) is
  replaced by a two-pass stable LSD radix sort on 128-bit digits, with an
  explicit 72n reconstruction covering counter zeroing and prefix sums,
  charged under a 128n envelope. Sorting therefore requires no array
  pre-initialization.
- The message/hash wrapper, scan and setup envelopes are tightened to
  128n, 16n and 2^24 respectively, each above an explicit instruction-level
  inventory retained in Section 5.

The former declaration was 137.785; the same proof skeleton with this
construction supports 128.264 under collision-frontier-v5. This new package
requires fresh ordinary review; no historical qualification or new
cryptanalytic algorithm is asserted.
