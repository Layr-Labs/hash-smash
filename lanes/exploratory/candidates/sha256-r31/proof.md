# SHA-256, 31 prefix rounds: single-block birthday with a radix sort

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains a
separately reported resource bound and contributes nothing to the scalar.

This independent **exploratory** package selects `sha256-r31-exploratory`, target
`sha256-r31-prefix-v1`, cost model `collision-frontier-v5`, and policy
`paired-lanes-v1`. It submits a complete analytic algorithm, not an already
computed collision. Readiness requests review; it does not assert an AI outcome
or human acceptance. It submits no rigorous-lane obligation and makes no
`ai_rigor_qualified` claim.

The algorithm is a birthday search. Two properties carry the improvement over
the organizer baseline package that declared `time_log2: 136`: sampled messages
are **55 bytes, so each costs exactly one target compression**, and duplicate
detection is a **two-pass LSD radix sort whose cost is deterministic** — it does
not depend on the distribution of the digest and contains no expected-work term,
no tail argument and no timeout. Correctness, probability and resources are
derived from the explicit target and model primitives: no ideal-hash,
random-oracle, differential or round-independence premise is used, and the
heuristic list is empty. The required `baseline_improved` value
`sha256-r31-nominal-v2` only identifies the organizer's nominal display
reference; it is not an established attack, qualified baseline, or security
bound. This package does not claim improvement over that reference. Its declared
scalar is 129.

## 1. Exact target and one-block message domain

Write BE_k(v) for the k-byte big-endian encoding of integer v. Set
q = 2^128, D = 2^440, N = 2^256, and C = 2140 (the v5 price for `sha256-r31`).

A sampled message is **the first 55 bytes of the big-endian concatenation of two
fresh independent uniform 256-bit RAM words** w0, w1:

    m = ( w0 || w1 )[0 : 55]        ( 55 bytes = 440 bits )

This induces the uniform distribution on all D = 2^440 byte strings of length
55, because the map (w0, w1) -> m has exactly 2^512 / 2^440 = 2^72 preimages per
message. Two independent draws coincide with probability exactly 1/D = 2^-440.
The message bit length 440 is far below 2^64, so it is inside the profile's
message domain, and m is never byte-for-byte equal to itself as a second draw.

**One padded block.** Under FIPS 180-4 a 55-byte message is padded by appending
0x80, then k zero bytes with 55 + 1 + k = 56 (mod 64), so k = 0, then the 64-bit
BIG-endian original bit length 440 = 0x1B8. The padded length is
55 + 1 + 0 + 8 = 64 bytes: **exactly one block**. This is the single structural
change from the 64-byte-message baseline, and it is what makes one message cost
one compression instead of two.

In 256-bit big-endian words that block is (W0, W1') where W0 = w0 and

    MASK = 2^256 - 2^72
    CONST = 2^71 OR 0x1B8
    W1' = (w1 AND MASK) XOR CONST

In w1, byte j occupies integer bits 255-8j down to 248-8j. Block byte 55 is
w1's byte 23, spanning bits 71..64, and the byte's most significant bit is bit
71, so the constant 0x80 is 2^71. Block bytes 56..63 are w1's bytes 24..31,
i.e. integer bits 63..0, which CONST sets to BE_8(440) = 0x1B8. MASK keeps
w1's bytes 0..22, which are block bytes 32..54. Two charged operations build
W1'.

Initialize the eight 32-bit chaining words once, in this order:

    6a09e667 bb67ae85 3c6ef372 a54ff53a
    510e527f 9b05688c 1f83d9ab 5be0cd19

For the block, parse its 16 consecutive big-endian 32-bit words as
W[0],...,W[15]. All additions below are modulo 2^32; NOT and rotations operate
on 32 bits. Define

    s0(z) = ROTR32(z,7) XOR ROTR32(z,18) XOR (z >> 3)
    s1(z) = ROTR32(z,17) XOR ROTR32(z,19) XOR (z >> 10)
    S0(z) = ROTR32(z,2) XOR ROTR32(z,13) XOR ROTR32(z,22)
    S1(z) = ROTR32(z,6) XOR ROTR32(z,11) XOR ROTR32(z,25)
    Ch(e,f,g) = (e AND f) XOR ((NOT e) AND g)
    Maj(a,b,c) = (a AND b) XOR (a AND c) XOR (b AND c)
    W[t] = W[t-16] + s0(W[t-15]) + W[t-7] + s1(W[t-2]),
        for t = 16,...,30.

The constants K[0],...,K[30] are, in hexadecimal and original index order:

    428a2f98 71374491 b5c0fbcf e9b5dba5 3956c25b 59f111f1 923f82a4 ab1c5ed5
    d807aa98 12835b01 243185be 550c7dc3 72be5d74 80deb1fe 9bdc06a7 c19bf174
    e49b69c1 efbe4786 0fc19dc6 240ca1cc 2de92c6f 4a7484aa 5cb0a9dc 76f988da
    983e5152 a831c66d b00327c8 bf597fc7 c6e00bf3 d5a79147 06ca6351

Copy the incoming chaining words into (a,b,c,d,e,f,g,h), then execute exactly
t = 0,...,30 with simultaneous updates:

    T1 = h + S1(e) + Ch(e,f,g) + K[t] + W[t]
    T2 = S0(a) + Maj(a,b,c)
    (a,b,c,d,e,f,g,h) = (T1+T2, a, b, c, d+T1, e, f, g).

After round 30 add all eight working words to the corresponding incoming
chaining words; do not reset the IV. Concatenate BE_4 of the eight state words
in standard order. This 32-byte output is H(m); interpret it as one 256-bit
integer d in the same big-endian order. Equality of d is equality of the full
digest. The reference implementation is `verifier/hash_functions.py:digest`.

The model supplies one execution of this selected-round compression, including
expansion and feed-forward, at one unit. H uses exactly **one** such unit per
message. Its message handling and state/byte serialization are charged
separately in section 6; the internal 31 rounds are not charged a second time.
Section 6 charges unpacking the 256-bit block into eight 32-bit words, packing
the final state into one 256-bit word, IV/state copies, dispatch and operand
transfer, even if the compression primitive already accepts packed blocks.

## 2. Concrete RAM algorithm and stopping rule

Every RAM word is 256 bits. Draw words only through the model's independent
uniform random-word primitive. There is no finite seed, deterministic PRNG
expansion, or precomputed advice.

A record is exactly three words (digest, w0, w1); the last two regenerate the
55-byte message. Arrays `A` and `C` each hold q contiguous records. `cnt`
holds 2^128 counter words. All large loops are bounded loops.

**RADIX(digit):** stable least-significant-digit counting sort of the q records
in `A` on one 128-bit digit of each digest, writing into `C`, then exchange the
base addresses of `A` and `C`. Stability is obtained by scattering in
**decreasing** index order into precomputed **exclusive group-end** offsets:
`cnt[k]` is first converted so that it holds the first slot *past* digit class
k's range, and the scatter performs `cnt[k] -= 1; C[cnt[k]] = A[i]`. That puts
the earliest record of each digit class into the lowest slot of its class, which
preserves relative order within a class. Scattering in decreasing index order
into *starting* offsets (`C[cnt[k]++]` with `cnt` at group starts) instead
would reverse the order inside every class and would be incorrect.

1. Clear `cnt` to 0. For i = 0,...,q-1 accumulate `cnt[A[i] digest low 128]`.
   One prefix scan converts `cnt` into exclusive group-end offsets.
   For i = q-1,...,0 set key = A[i]'s low 128 digest bits, decrement `cnt[key]`,
   and store `A[i]` into `C[cnt[key]]`.
2. Exchange A and C. Clear `cnt` to 0. Repeat step 1 on the **high** 128 bits
   of the digest, scattering in decreasing index order.
3. Exchange A and C. `A` now holds the q records in nondecreasing order of the
   full 256-bit digest.
4. Scan j = 1,...,q-1, comparing A[j]'s digest with A[j-1]'s. At the first
   equal pair with a different message, copy both messages out and go to step 6.
   If the scan ends with no such pair, return FAIL.
5. Unused for this package; retained only to mark that no second scan strategy
   is required.
6. Recompute H for both messages from the fixed IV, check full 256-bit digest
   equality and check that the two messages are not byte-for-byte equal. If both
   hold, return the two messages; otherwise return FAIL. This happens at most
   once per execution.

Since the digits cover all 256 bits and each pass is stable, the LSD radix
invariant puts `A` in nondecreasing order of the complete digest. Records
sharing a digest are therefore contiguous and, within such a group, the messages
are pairwise distinct whenever the draws were distinct. So **on the event that
some sampled digest repeats while no sampled message repeats**, the adjacent
scan finds an equal-digest pair with different messages, and step 6 returns a
valid ordinary collision. This is the precise detection statement; the package
does not claim that a collision is found on every possible tape. If an identical
message is drawn twice first, step 4 sees an equal digest with an equal message,
does not accept it, and the algorithm may return FAIL. Section 4 bounds the
probability of that event separately, and it is the only loss channel.

The final check in step 6 is what guarantees the returned pair satisfies the
target relation: it re-executes the complete target on both messages from the
fixed IV and verifies digest equality and message inequality directly. No
returned pair is accepted on the strength of the table alone.

## 3. Distribution-free birthday lemma

For each of the N possible digest values z let p_z be the fraction of the D
one-block messages mapping to z under the fixed deterministic H. Retain zero
entries. Independent uniform messages induce independent output samples from
this same p, because H is applied separately to independent inputs. This says
nothing about whether p is uniform or SHA-256 behaves like a random function.

For a probability vector p let e_k(p) be the sum of products over all its
k-element coordinate subsets. The probability that k samples all differ is
k! e_k(p), since each unordered k-element set contributes its k! possible
orders. We prove e_k(p) is maximized by the uniform vector.

The N-coordinate simplex is compact and e_k is continuous. Among its maximizers
choose one minimizing sum_z p_z^2; that choice exists by compactness. If two
coordinates a,b differ, call the other N-2 coordinates r. Splitting subsets by
which of these two coordinates they contain gives:

    e_k(p) = e_k(r) + (a+b)e_(k-1)(r) + ab e_(k-2)(r).

Here e_0 = 1 and e_j = 0 outside the available subset sizes. Every coefficient
is nonnegative. Averaging a,b preserves a+b and increases ab by (a-b)^2/4, so it
cannot decrease e_k. The result must still be a maximizer (a strict increase
would contradict maximality), but its sum of squared coordinates is strictly
smaller, a contradiction. Therefore all coordinates of that maximizer equal
1/N. This proves the bound for every p, regardless of the actual hash's bias.

Since 2 <= k <= N, the probability that k samples contain no repeated digest is
at most

    k! binomial(N,k)/N^k = product_(j=0)^(k-1) (1 - j/N) <= exp(-k(k-1)/(2N)).

The final inequality uses 1-u <= exp(-u) term by term and sums j/N. No
independence-of-collision-events assumption and no structural property of H is
used.

## 4. Algorithmic success and repeated inputs

Let C mean that some of the first q sampled digests repeats, and R that some
original message repeats. C minus R guarantees two distinct messages with equal
full digests, and by section 2 the algorithm finds and returns them. Without
assuming independence of C and R,

    Pr(success) >= Pr(C) - Pr(R)
      >= 1 - exp(-q(q-1)/(2N)) - q(q-1)/(2D).

For two different positions the chance of equal 440-bit messages is exactly
1/D. The union bound over binomial(q,2) position pairs gives the repeated-input
term. There is no rejection sampling and no uncharged sampling without
replacement. The domain D = 2^440 relative to q = 2^128 is what keeps Pr(R)
negligible: q^2/D = 2^-184.

Now certify the declared decimal with rational arithmetic. For q = 2^128,

    q(q-1)/(2N) = (1 - 2^-128)/2 = 1/2 - 2^-129,

so exp(-q(q-1)/(2N)) = exp(-1/2) * exp(2^-129). The alternating series for
e^-x with 0 < x < 1 has strictly decreasing terms, so a partial sum ending in a
positive term over-estimates the sum:

    e^-1/2 <= 1 - 1/2 + 1/8 - 1/48 + 1/384 - 1/3840 + 1/46080 = 27949/46080.

The sixth term is (-1/2)^5/5! = -1/3840. The partial sum 27949/46080 =
0.60653211 exceeds e^-1/2 = 0.60653066, as an upper bound must. For
0 < x <= 1/2, e^x <= 1/(1-x) <= 1 + 2x, so

    exp(2^-129) <= 1 + 2^-128

and therefore

    exp(-q(q-1)/(2N)) <= (27949/46080)(1 + 2^-128).

Hence

    Pr(C) >= 1 - (27949/46080)(1 + 2^-128)
          = 18131/46080 - (27949/46080) 2^-128
          > 0.3934 - 2^-128,

because 18131 > 46080 * 0.3934 = 18130.272. Also

    Pr(R) <= q(q-1)/(2D) < 2^-185,

since q(q-1) < q^2 = 2^256 and 2^256 / 2^441 = 2^-185. Thus

    Pr(success) > 0.3934 - 2^-128 - 2^-185 > 0.393 > 0.39,

which is the required minimum. The declared `success_probability: 0.393` is a
strict rational lower bound on algorithmic success under its fresh coins, not
equality with actual success, confidence in this proof, or confidence in an AI
review. The entire q-sample construction and every sort pass are paid on failed
runs too. There are no restarts and no success amplification to account for
beyond the single fully charged execution.

## 5. Why the lookup cost needs no distributional argument

This section exists because the previous revision of this package used a
chained hash table and derived its cost from a conditional-distribution claim
that was false. The structure is now chosen so that **no such argument is
needed at all**.

A hash table keyed on the digest has data-dependent cost. For an arbitrary fixed
output distribution p, a bucket can receive most of the samples: if p is
supported on distinct digest values that all share one bucket, then every
earlier sample shares the query's bucket and the chain length at insert i is
i-1 rather than a small constant. Any argument that conditions on "no exact
repeat yet" and concludes the prior digests behave like a uniformly random
subset of the digest space is wrong for nonuniform p, because distinct subsets
are weighted by products of their probabilities. Such a table would require
either an expected-work metric, a tail bound, or a timeout, none of which this
cost model provides, and `total_time_includes` requires lookup work to be
charged.

The two-pass LSD radix sort has none of this exposure. Its cost is a fixed
function of q alone:

* each pass performs exactly q counter increments and exactly q scatter stores,
  plus one clear and one prefix scan over exactly 2^128 counters;
* there are exactly two passes, so the record-level work is exactly 2 * 2 * q
  operations and the counter-level work is exactly 4 * 2^128 operations;
* no branch, comparison or memory access in either pass depends on the values
  of the digests. The scatter target is `C[--cnt[key]]`, executed once per record
  whatever key that record carries.

So the charged lookup work is exactly determined, on every random tape, by
q and by the counter-array size alone. It does not matter whether p is uniform,
concentrated on one bucket, or anything else. Sections 6 charges those exact
counts, the success bound in section 4 already holds for arbitrary p by the
lemma in section 3, and the two arguments are independent: neither one needs an
assumption made by the other. There is no expected quantity anywhere in this
package, so there is no tail to bound and no success probability to trade
against a timeout.

## 6. Auditable resource implementation

These are worst-case bounds for every random tape in the specified classical
256-bit word RAM. Each selected compression costs one unit. Every other word
load, store, arithmetic/Boolean operation, shift, comparison, branch, and random
word costs 1/2140 target-compression units. In the instruction budgets below,
ordinary-operation counts are unpriced counts W, not target-compression units.
Compression calls are counted separately as H_calls; their expansion and round
internals are not included in W.

### 6.1 Instruction and interface budgets

A core scalar operation (two-operand arithmetic/comparison, assignment, branch,
or load/store) can be implemented with at most eight charged operations even
when scalar operands/results live in scratch: up to four instruction-word
fetches, two operand loads, the operation, and a result store. Instruction
fetches are charged explicitly. Address calculation is itself counted as core
work; base+3*i uses three additions. A record copy is three addressed loads and
three addressed stores. Loops, branches and addressing are not free.

Every budget below is a worst case on every tape; none is averaged over data.

Per sampled message i, charged work outside the compression:

| Work per sampled message | charged operations |
| --- | ---: |
| Draw w0 and w1 (two model random-word instructions, fetch/dispatch included) | 16 |
| Build W1' = (w1 AND MASK) XOR CONST | 16 |
| Unpack the 256-bit block into eight 32-bit words, IV/state copies, record addressing | 144 |
| Pack the eight output words into one 256-bit digest d | 144 |
| Store the three-word record into A[i] | 32 |
| Loop index, bound test, array base updates, loop-back branch | 64 |
| Fixed sub-total | 416 |
| Padding, rounded upward | 512 |

The 512 figure is about 1.23x the enumerated rows and covers block construction
and record addressing slack on both branch paths.

Per radix pass, per record:

| Work per record per pass | charged operations |
| --- | ---: |
| Load digest digit (low or high 128 bits) | 8 |
| Counter load, increment, counter store | 24 |
| Load source base and index, compute destination address | 32 |
| Load the three record words | 24 |
| Store the three record words to the destination | 24 |
| Loop index, bound test, loop-back branch (scatter order descending) | 32 |
| Padding, rounded upward | 160 |

Per radix pass, per counter (2^128 counters, two passes):

| Work per counter per pass | charged operations |
| --- | ---: |
| Clear to 0 | 8 |
| Prefix scan: load, add, store, index update and test | 24 |
| Padding, rounded upward | 32 |

Adjacent scan, per position:

| Work per position | charged operations |
| --- | ---: |
| Load two digests, compare | 24 |
| Address calculation for both records | 16 |
| On a match, copy both messages out | 32 |
| Loop index, bound test, loop-back branch | 32 |
| Padding, rounded upward | 128 |

Fixed setup: clearing and prefix-scanning `cnt` once per pass costs
32 * 2^128 charged operations per pass, i.e. 2 * 32 * 2^128 = 64 * 2^128 in
total. The rest of code, constants and scratch initialization is under 2^20.
Final verification costs at most two extra compressions and 8192 charged
operations.

### 6.2 Code, peak storage, and address width

All large loops are bounded loops, not unrolled code. The fixed program can be
laid out in fewer than 4096 instruction slots, each allowed four full 256-bit
words for opcode and operands, allocating 2^19 bytes for code. The per-sample
body uses at most 512 core-instruction slots; the pass body 160; the scan 128;
initialization, loop shells and the final checks fit in the remaining 3296
slots. No compiler, runtime, big-integer library, allocator or operating system
is used by the RAM algorithm. The full compression specification fixes its
supplied primitive; its internals need not be implemented a second time in the
attack program.

Allocate at most 4096 additional words (2^17 bytes) for the IV, the padding
constants, message/padding buffers, unpacked block words, eight-word input and
output states, indices, saved records, counters and output. A loader may
read/write every code/constant word, initialize all fixed scratch, and establish
array base addresses in under 2^20 ordinary operations.

Peak resident memory on every execution is

    M <= 2 * 96 * q  (arrays A and C, three words per record)
       + 2^132      (cnt, 2^128 one-word entries)
       + 2^20       (code, constants, scratch)
       = 2.5 * 2^134 + 2^20 < 2^136 bytes.

Every array is word-granular, since the model's primitive is a 256-bit load or
store. Large arrays are not assumed zero: `cnt` is explicitly cleared before each
use and every record array slot is written by the generation loop before it is
read. Randomness is retained only in the message fields and constant-size
copies; there is no stored random tape. This proves `memory_log2_bytes: 136`.
Memory is a reported metric under v5 and does not enter the scalar. All indices,
byte and word addresses and counter bounds are below 2^136, far below 2^256, so
address and counter arithmetic never wraps.

### 6.3 Total time and auxiliary claim fields

| Phase | Compression calls, at cost 1 each | charged operations, at cost 1/2140 each |
| --- | ---: | ---: |
| Fixed setup (clear + prefix `cnt`, twice; code, constants, scratch) | 0 | 64*2^128 + 2^20 |
| Generate all q records, one compression each | q | 512q |
| Pass 1, record loop (count + scatter) | 0 | 2 * 160q |
| Pass 2, record loop (count + scatter) | 0 | 2 * 160q |
| Adjacent scan | 0 | 128q |
| Final verification and output | at most 2 | 8192 |

Thus H_calls <= q + 2 and

    W <= 512q + 320q + 320q + 128q + 64*2^128 + 2^20 + 8192
       = 1280q + 64*2^128 + 2^20 + 8192.

With C = 2140 and q = 2^128, v5 gives

    T = H_calls + W/2140
      <= (1280/2140 + 1) q + 2 + (64*2^128 + 2^20 + 8192)/2140
       = 1.598130 * 2^128 + 2^122.9 + o(1)
       < 2^129  for q = 2^128.

The last strict inequality is rational arithmetic including the constant terms;
1 + 1280/2140 is approximately 1.598130, giving log2 T = 128.676, so the
smallest admissible integer is 129. This proves the submitted
`time_log2: 129`. All setup is inside T. The bound is robust to a large budget
inflation: even if every ordinary-operation row in section 6.1 were charged
twice, the coefficient becomes 1 + 2568/2140 = 2.200, and the declared scalar
would move to 130, so 129 does depend on the per-record budgets being roughly
right. Those budgets are itemized above rather than asserted, and each is a
worst case for the operation it covers.

`nonuniform_advice_log2_bytes: 0` is a one-byte upper bound, as required by the
nonnegative logarithmic schema. Actual nonuniform advice is zero bytes. Public
fixed code, IV and SHA-256 constants are uniform specification data, but their
storage and initialization are still charged. No favorable seed, cached
collision, hidden preprocessing or target-dependent advice is supplied. The
legacy `data_log2` field is omitted per the v3 schema description.

## 7. Evidence, scope, and limitations

The heuristic list is empty because sections 1-6 derive correctness, probability
and resources from the explicit target and model primitives. Fresh independent
random words are part of the organizer's model, not an empirical claim about a
short seeded program. No ideal SHA-256 behavior is required, and by section 5
no part of the cost ledger depends on the shape of the digest distribution.

The certificate manifest is valid and empty. There is no experiment manifest and
no executable candidate source. A finite toy experiment adds no premise to the
all-distributions lemma and cannot establish this full-scale execution's success
or cost. All necessary analytic evidence is included here, without external-link
dependence or participant-code execution. The one-block padding mapping in
section 1 is derived arithmetically and is not offered as empirical evidence;
the author separately checked it against the reference implementation during
development, and that check is explicitly not credited as a premise here.

This is an astronomically expensive theoretical RAM construction, not a measured
run, practical attack, or new SHA-256 security result. Any eventual
selected-lane AI qualification remains distinct from mathematical proof or human
acceptance.

**Why 129 is the floor for this family of arguments.** Any algorithm that finds
a collision by evaluating H on sampled messages needs at least
q >= 0.99428 * 2^128 evaluations to reach success probability 0.39 for an
arbitrary fixed output distribution (section 3), and each evaluation costs at
least one compression. Total time is therefore at least 0.99428 * 2^128, which
lies strictly between 2^127 and 2^128. Declaring `time_log2: 128` would require
the whole charged total to stay at or below 2^128, leaving at most
0.00572 * 2^128 units of headroom, i.e. about 12 charged ordinary operations per
sample at C = 2140. That budget cannot cover the mandatory per-sample work of
packing eight state words into a 256-bit digest (7 shifts and 7 ORs) plus the
record store, let alone a detection pass, so 128 is not attainable by this or
any comparable sampling-based attack under v5 prices, and 129 is the floor for
a fully deterministic ledger. Beating 129 requires an attack that exploits the
internal structure of the reduced-round permutation rather than its output
width, i.e. a real differential or algebraic attack on rounds 0..30 of the
compression function. None is constructed or claimed here. The nominal
reference 128 is a security statement for an n-bit output; this package reaches
129 and does not beat it.

## 8. Relation to the previous package

This replaces the exploratory SHA-256 r31 package that used 64-byte messages
(two compressions each, q = 2^129 samples) and detected duplicates by a
129-pass bottom-up merge sort over three-word records, declaring
`time_log2: 136`. Its complete-hash definition, distribution-free lemma,
repeated-input union bound and memory methodology are retained. Two changes
carry the improvement:

1. **One-block messages.** 55 bytes pad to a single 64-byte block, so a sample
   costs one compression instead of two. This is worth a full bit and is
   orthogonal to the detection structure.
2. **q = 2^128 instead of 2^129.** The successor probability certification needs
   only a 0.39 lower bound, which q = 2^128 meets at 0.393; the predecessor
   targeted 0.6, which cost a full bit of sample count.

The detection structure is a two-pass LSD radix sort on two 128-bit digits,
which removes the `log2(q)` comparison factor. Unlike a chained hash table it
has no data-dependent cost, so nothing in this package needs an expected-work
metric, a tail bound or a timeout; that property is the reason this structure
was chosen over the hash table that an earlier draft of this package used.
Together these move the charged total from about 2^136 to about 2^128.7. This is
a new package requiring fresh ordinary review, not a replay of an earlier
qualification and not a new cryptanalytic algorithm: the underlying method is
still a distribution-free birthday search.