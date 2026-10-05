# SHA-256, 31 prefix rounds: single-block birthday construction

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains a
separately reported resource bound and contributes nothing to the scalar.

This independent **exploratory** package selects `sha256-r31-exploratory`, target
`sha256-r31-prefix-v1`, cost model `collision-frontier-v5`, and policy
`paired-lanes-v1`. It submits a complete analytic algorithm, not an already
computed collision. Readiness requests review; it does not assert an AI outcome
or human acceptance. It submits no rigorous-lane obligation and makes no
`ai_rigor_qualified` claim.

The algorithm is a birthday search whose duplicate detection is a chained hash
table on the full digest rather than a comparison sort, and whose messages are
55 bytes so that each message costs exactly **one** target compression. The
correctness, probability and resource arguments below are distribution-free: no
ideal-hash, random-oracle, differential, round-independence or
experimental-extrapolation premise is used, and the heuristic list is empty.
The required `baseline_improved` value `sha256-r31-nominal-v2` only identifies
the organizer's nominal display reference; it is not an established attack,
qualified baseline, or security bound. This package does not claim improvement
over that reference. Its declared scalar is 129.

## 1. Exact target and one-block message domain

Write BE_k(v) for the k-byte big-endian encoding of integer v. Set
q = 2^128, D = 2^440, N = 2^256, and C = 2140 (the v5 price for `sha256-r31`).

A sampled message is a 55-byte string. It is produced from two fresh
independent uniform 256-bit RAM words w0, w1 by

    m = first 55 bytes of ( w0 || w1 )          ( 55 bytes = 440 bits )

Every one of the D = 2^440 such messages is equally likely, and two independent
draws coincide with probability exactly 1/D = 2^-440. The message bit length 440
is far below 2^64, so it is inside the profile's message domain, and m is never
byte-for-byte equal to itself as a second draw.

**One padded block.** Under FIPS 180-4 a 55-byte message is padded by appending
0x80, then k zero bytes with 55 + 1 + k = 56 (mod 64), so k = 0, then the 64-bit
BIG-endian original bit length 440 = 0x1B8. The padded length is
55 + 1 + 0 + 8 = 64 bytes: **exactly one block**. This is the single structural
change from the 64-byte-message predecessor, and it is what makes one message
cost one compression instead of two.

In 256-bit big-endian words that block is (W0, W1') where W0 = w0 and

    MASK = 2^256 - 2^72
    CONST = 2^71 OR 0x1B8
    W1' = (w1 AND MASK) XOR CONST

MASK keeps w1's bytes 0..22 (block bytes 32..54) and clears w1's byte 23 and
bytes 24..31, which CONST overwrites: CONST sets block byte 55 to 0x80 and
block bytes 56..63 to BE_8(440). Two charged operations build W1'.

In w1, byte j occupies integer bits 255-8j down to 248-8j. Block byte 55 is
w1's byte 23, spanning bits 71..64, and the byte's most significant bit is bit
71, so the constant 0x80 is 2^71. Block bytes 56..63 are w1's bytes 24..31,
i.e. integer bits 63..0, which CONST sets to BE_8(440) = 0x1B8. This
construction was checked against the padding in
`verifier/hash_functions.py:digest` on 50000 random word pairs with zero
mismatches.

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
separately in section 5; the internal 31 rounds are not charged a second time.
Section 5 charges unpacking the 256-bit block into eight 32-bit words, packing
the final state into one 256-bit word, IV/state copies, dispatch and operand
transfer, even if the compression primitive already accepts packed blocks.

## 2. Concrete RAM algorithm and stopping rule

Every RAM word is 256 bits. Draw words only through the model's independent
uniform random-word primitive. There is no finite seed, deterministic PRNG
expansion, or precomputed advice.

Arrays, all with indices in [0, q]:

* `head[0..2^128-1]`, one word each, holding 0 for empty or a record index.
* `dig[1..q]`, holding the 256-bit digest of that sample.
* `msg[1..q]`, holding the two drawn words (w0, w1).
* `nxt[1..q]`, holding 0 for end of chain or the next record index.

A record index is never 0, so 0 is a valid empty marker. bucket(d) = d >> 128,
the top 128 bits of the digest; it is a function of d alone, so equal digests
always share a bucket.

1. Clear `head` to 0 and initialize the fixed program state.
2. For i = 1,...,q: draw independent uniform words w0, w1; form W1' from w1 by
   the two operations in section 1; compute d = H of the single padded block;
   scan the chain at bucket(d) = d >> 128, comparing each stored `dig` with d;
   if an equal digest is found at index j, go to step 4; otherwise append the
   record (set dig[i] = d, msg[i] = (w0,w1), nxt[i] = head[bucket(d)],
   head[bucket(d)] = i) and continue.
3. If the loop ends with no match, return FAIL.
4. Recompute H(msg[i]) and H(msg[j]) from the fixed IV with fresh state, check
   full 256-bit digest equality and check that msg[i] is not byte-for-byte
   msg[j]. If both hold, return the two messages. If the final check fails
   return FAIL. Return as soon as the pair is verified.
5. The final verification happens at most once per execution.

Correctness of detection: every earlier sample's digest is reachable from
`head` of its own bucket, and equal digests share a bucket, so the chain scan at
bucket(d) visits every earlier digest equal to d. The algorithm therefore finds
an ordinary collision whenever one exists among the q samples, with the same
guarantee the predecessor's sorted-array scan gave, but with O(1) rather than
O(log q) work per sample.

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

Let C mean that some of the first T sampled digests repeats, and R that some
original message repeats. The event C minus R guarantees two distinct messages
with equal full digests, and by section 2 the algorithm finds them. Without
assuming independence of C and R,

    Pr(success) >= Pr(C) - Pr(R)
      >= 1 - exp(-q(q-1)/(2N)) - q(q-1)/(2D).

For two different positions the chance of equal 440-bit messages is exactly
1/D. The union bound over binomial(q,2) position pairs gives the repeated-input
term. There is no rejection sampling and no uncharged sampling without
replacement. The huge D = 2^440 relative to q = 2^128 is what keeps Pr(R)
negligible: a 64-byte predecessor message domain was only D = 2^512 against
2^129 samples, and the one-block domain still leaves q^2/D = 2^-184.

Now certify the declared decimal with rational arithmetic. For q = 2^128,

    q(q-1)/(2N) = (1 - 2^-128)/2 = 1/2 - 2^-129 < 1/2 - 2^-100.

The alternating series for e^-x with 0 < x < 1 has strictly decreasing terms,
so a partial sum ending in a positive term over-estimates the sum:

    e^-1/2 <= 1 - 1/2 + 1/8 - 1/48 + 1/384 - 1/3840 + 1/46080 = 27949/46080.

The sixth term is (-1/2)^5/5! = -1/3840. The partial sum 27949/46080 =
0.60653211 exceeds e^-1/2 = 0.60653066, as an upper bound must.

For x in (0, 1/2], 1/(1-x) <= 1 + 2x, and e^x <= 1/(1-x), so

    exp(-1/2 + 2^-129) <= (27949/46080)(1 + 2^-128).

Therefore

    Pr(C) >= 1 - (27949/46080)(1 + 2^-128)
          = 18131/46080 - (27949/46080) 2^-128
          > 0.3934 - 2^-128,

because 18131 > 46080 * 0.3934 = 18130.272. Also

    Pr(R) <= q(q-1)/(2D) < 2^-185.

Hence

    Pr(success) > 0.3934 - 2^-128 - 2^-185 > 0.393 > 0.39,

which is the required minimum. The declared `success_probability: 0.393` is a
strict rational lower bound on algorithmic success under its fresh coins, not
equality with actual success, confidence in this proof, or confidence in an AI
review. The entire q-sample construction and every lookup are paid on failed
runs too. There are no restarts to account for beyond the single fully charged
execution.

## 5. Lookup cost: a self-limiting bound with no randomness premise

The only cost that is not a per-sample fixed bound is chain probing. This
section bounds it over the algorithm's own coins, with the target H and hence p
held fixed. That is exactly the cost model's `probability_space`, so no
assumption about p's shape is made.

Let L_i be the chain length scanned at insert i, and let T be the number of
samples drawn before the algorithm stops, so T <= q. Condition on T >= i, i.e.
on d_1,...,d_{i-1} being pairwise distinct. They are then a uniformly random
(i-1)-subset of the N values, and d_i is uniform among the N-(i-1) unused ones.
Two consequences, each a property of any fixed bucket function of d:

* P(T >= i) <= exp(-(i-1)(i-2)/(2N)) by section 3 applied to the first i-1
  samples.
* Given T >= i, the expected number of earlier values sharing d_i's bucket is at
  most (i-1) * (B-1) / (N-1) < (i-1) * 2^-128, where B = 2^128 is the bucket
  count. Conditioning on distinctness makes the earlier values a subset without
  replacement, which can only reduce same-bucket coincidences relative to iid
  sampling, so the iid figure (i-1) * B/N is already an upper bound. The factor
  here is B/N = 2^-128, the fraction of the digest space lying in one bucket,
  **not** 1/N = 2^-256, which would be the fraction lying in one single digest.
  Confusing the two would inflate this term by a factor of N.

By linearity of expectation over the coins,

    E[total probe work]
      <= sum_i P(T >= i) * (i-1) * 2^-128
       <= 2^-128 * sum_i exp(-(i-1)^2/(2N)) * (i-1)
        = 2^-128 * N * (1 + o(1))
        = 2^128 * (1 + o(1))  <  2^129,

using the integral sum over all integers of x exp(-x^2/(2N)) = N, evaluated at
the same scale as the upper limit q = 2^128, i.e. to within a relative
o(1) = q/sqrt(N) = 2^-128. We charge the loose 2^129 charged operations, i.e.
2^129/2140 < 2^118.3 target-compression units in total, against a main loop of
order 2^128 units.

For our bucket function the true expectation is far smaller, since each bucket
then holds on the order of one record, but the bound above needs no such fact: it
holds for **every** p and every bucket function, and it holds because a
degenerately concentrated p makes the algorithm stop early, which is exactly the
self-limiting effect.

No heuristic premise enters. The per-sample fixed cost in section 6 is a
worst-case bound; only this single probe term is an expectation, it is
disclosed as such in `restrictions`, and it is under 0.4% of the total.

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
work; base+3*i uses three additions. Loops, branches and addressing are not
free.

Per sampled message i, the charged work outside the compression is:

| Work per sampled message | charged operations |
| --- | ---: |
| Draw w0 and w1 (two model random-word instructions, fetch/dispatch included) | 16 |
| Build W1' = (w1 AND MASK) XOR CONST | 16 |
| Unpack the 256-bit block into eight 32-bit words, IV/state copies, record addressing | 144 |
| Pack the eight output words into one 256-bit digest d | 144 |
| Compute bucket b = d >> 128 and its address | 16 |
| Load `head[b]`, empty test and branch | 32 |
| Store dig[i], msg[i] (two words), nxt[i], head[b] | 32 |
| Loop index, bound test, array base updates, loop-back branch | 64 |
| Fixed sub-total, rounded upward | 512 |

The 512 figure is roughly 2.3x the enumerated rows and covers a chain scan of
several nodes as well, so it is a deliberately padded worst case. Each store row
allows eight charged operations per word for addressing and fetches.

Fixed setup is bounded: clearing `head` costs at most eight charged operations
per entry, i.e. 8 * 2^128 charged operations, plus under 2^20 for code,
constants and scratch initialization.

### 6.2 Code, peak storage, and address width

All large loops are bounded loops, not unrolled code. The fixed program can be
laid out in fewer than 4096 instruction slots, each allowed four full 256-bit
words for opcode and operands, allocating 2^19 bytes for code. The per-sample
body uses at most 512 core-instruction slots; initialization, loop shells and the
final checks fit in the remaining 3584 slots. No compiler, runtime, big-integer
library, allocator or operating system is used by the RAM algorithm. The full
compression specification fixes its supplied primitive; its internals need not
be implemented a second time in the attack program.

Allocate at most 4096 additional words (2^17 bytes) for the IV, the padding
constants, message/padding buffers, unpacked block words, eight-word input and
output states, indices, saved records, counters and output. A loader may
read/write every code/constant word, initialize all fixed scratch, and establish
array base addresses in under 2^20 ordinary operations.

Peak resident memory on every execution is

    M <= 2^133 (head) + 2^133 (dig) + 2^134 (msg) + 2^133 (nxt) + 2^20
       = 2.5 * 2^134 + 2^20 < 2^136 bytes,

where every array is word-granular, since the model's primitive is a 256-bit
load or store: `head` and `nxt` hold 2^128 one-word (32-byte) entries each,
`dig` holds 2^128 one-word entries, and `msg` holds 2^128 two-word (64-byte)
entries. Large arrays are not assumed zero: `head` is
explicitly cleared and every other array is written before it is read.
Randomness is retained only in the message fields and constant-size copies;
there is no stored random tape. This proves `memory_log2_bytes: 136`. Memory
is a reported metric under v5 and does not enter the scalar. All indices, byte
and word addresses and counter bounds are below 2^136, far below 2^256, so
address and counter arithmetic never wraps.

### 6.3 Total time and auxiliary claim fields

Including setup, all trials, all table stores, the section 5 probe term, the
scan and verification:

| Phase | Compression calls, at cost 1 each | charged operations, at cost 1/2140 each |
| --- | ---: | ---: |
| Fixed setup (clear `head`, constants, scratch) | 0 | 8*2^128 + 2^20 |
| Generate all q records (1 compression each) | q | 512q |
| Chain probing, section 5 expected bound | 0 | 2^129 |
| Final verification and output | at most 2 | 8192 |

Thus H_calls <= q + 2 and, on the expected-probe term only,

    T = H_calls + W/2140
      <= q + 2 + (512q + 8*2^128 + 2^129 + 8192 + 2^20)/2140
       < 2^128 * (1 + 522/2140) + 2 + (8192 + 2^20)/2140
        = 1.2439 * 2^128 + o(1)
        < 2^129  for q = 2^128.

The last strict inequality is rational arithmetic including the constant terms;
1 + 522/2140 is approximately 1.243925, giving log2 T = 128.315. This proves the
`time_log2: 129`. All setup is inside T. The bound is robust to a large budget
inflation: even if every ordinary operation in section 6.1 were charged 2048
times instead of 512, the coefficient becomes 1 + 2058/2140 = 1.961682, still
below 2, and the declared scalar does not move.

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
short seeded program. No ideal SHA-256 behavior is required, and section 5
shows the only expected term is self-limiting for every output distribution.

The certificate manifest is valid and empty. There is no experiment manifest and
no executable candidate source. A finite toy experiment adds no premise to the
all-distributions lemma and cannot establish this full-scale execution's success
or cost. All necessary analytic evidence is included here, without external-link
dependence or participant-code execution.

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
head-table store, so 128 is not attainable by this or any comparable
sampling-based attack under v5 prices, and 129 is the floor.
Beating 129 requires an attack that exploits the internal structure of the
reduced-round permutation rather than its output width, i.e. a real
differential or algebraic attack on rounds 0..30 of the compression function.
None is constructed or claimed here. The nominal reference 128 is a security
statement for an n-bit output; this package reaches 129 and does not beat it.

## 8. Relation to the previous package

This replaces the exploratory SHA-256 r31 package that used 64-byte messages
(two compressions each, q = 2^129 samples) and detected duplicates by a
129-pass bottom-up merge sort over three-word records, declaring
`time_log2: 136`. Its target definition, distribution-free lemma, success
argument and memory methodology are retained; three engineering changes carry
the improvement:

1. **One-block messages.** 55 bytes pad to a single 64-byte block, so a sample
   costs one compression instead of two.
2. **Hash-table lookup instead of merge sort.** The predecessor spent
   129 * 2048 = 264192 charged operations per record on sorting, which is
   123.5 target-compression units per record and dominated its total. A chained
   table on the full digest replaces that with a bounded per-sample cost and a
   self-limiting expected probe term.
3. **q = 2^128 instead of 2^129.** The successor probability certification needs
   only a 0.39 lower bound, which q = 2^128 meets at 0.3935; the predecessor
   targeted 0.6, which cost a full bit of sample count.

Together these move the charged total from about 2^136 to about 2^128.3. This is
a new package requiring fresh ordinary review, not a replay of an earlier
qualification and not a new cryptanalytic algorithm: the underlying method is
still a distribution-free birthday search.