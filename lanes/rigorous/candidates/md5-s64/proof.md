# MD5, all 64 steps: a complete generic collision construction

This is the rigorous package for `md5-s64-prefix-v1`, ordinary collisions,
under `collision-frontier-v3`. It proposes a conservative analytic baseline,
not a practical attack, novelty claim, or improvement over published MD5
cryptanalysis. The required `baseline_improved` value `md5-s64-nominal-v2`
identifies nominal display metadata, not an established attack, qualified
baseline, or security bound. The claimed resource sum is 82 + 73 = 155, with
algorithmic success probability at least 1/2. Readiness requests review;
neither readiness nor AI qualification is human acceptance or a formal proof.

## 1. Exact complete-message function

Set N = 2^65, D = 2^128, and U = 2^256. The algorithm uses exactly the
32-byte strings, a subset of the profile's finite byte strings of bit length
less than 2^64. A 256-bit word x denotes the message m(x) whose byte j is
(x >> (8j)) AND 255, for j = 0,...,31. This encoding is a bijection, including
all zero bytes; no variable-length integer encoding is used.

H(x) is the selected complete 64-step MD5 hash of m(x). Append byte 80
hexadecimal, then 23 zero bytes, then the eight little-endian bytes of the
original bit length 256: `00 01 00 00 00 00 00 00`. The result is one 64-byte
block. Its sixteen little-endian 32-bit words are W[j] = (x >> (32j)) AND
ffffffff for j=0,...,7; W[8]=00000080; W[9] through W[13] are zero;
W[14]=00000100; W[15]=0. Padding belongs to H, not to the returned message.

The fixed initial chaining state is
(A0,B0,C0,D0) = (67452301, efcdab89, 98badcfe, 10325476), in hexadecimal.
Initialize (a,b,c,d) to that tuple. For i=0,...,63 in this order, set

| Step indices | f | g | Rotation amounts, repeated in order |
| --- | --- | --- | --- |
| 0..15 | (b AND c) OR ((NOT b) AND d) | i | 7,12,17,22 |
| 16..31 | (d AND b) OR ((NOT d) AND c) | (5i+1) mod 16 | 5,9,14,20 |
| 32..47 | b XOR c XOR d | (3i+5) mod 16 | 4,11,16,23 |
| 48..63 | c XOR (b OR (NOT d)) | (7i) mod 16 | 6,10,15,21 |

These bitwise expressions operate on 32 bits, including NOT. With the
indicated rotation s, set t=(a+f+K[i]+W[g]) mod 2^32, then simultaneously
replace (a,b,c,d) by (d, (b+ROTL32(t,s)) mod 2^32, b, c).
ROTL32(t,s) = ((t << s) OR (t >> (32-s))) AND ffffffff.
The constants K in hexadecimal, in increasing step order, are:

```text
d76aa478 e8c7b756 242070db c1bdceee f57c0faf 4787c62a a8304613 fd469501
698098d8 8b44f7af ffff5bb1 895cd7be 6b901122 fd987193 a679438e 49b40821
f61e2562 c040b340 265e5a51 e9b6c7aa d62f105d 02441453 d8a1e681 e7d3fbc8
21e1cde6 c33707d6 f4d50d87 455a14ed a9e3e905 fcefa3f8 676f02d9 8d2a4c8a
fffa3942 8771f681 6d9d6122 fde5380c a4beea44 4bdecfa9 f6bb4b60 bebfbc70
289b7ec6 eaa127fa d4ef3085 04881d05 d9d4d039 e6db99e5 1fa27cf8 c4ac5665
f4292244 432aff97 ab9423a7 fc93a039 655b59c3 8f0ccc92 ffeff47d 85845dd1
6fa87e4f fe2ce6e0 a3014314 4e0811a1 f7537e82 bd3af235 2ad7d2bb eb86d391
```

Feed forward to obtain (h0,h1,h2,h3) =
((A0+a) mod 2^32, (B0+b) mod 2^32, (C0+c) mod 2^32, (D0+d) mod 2^32).
Serialize h0,h1,h2,h3 in order, four little-endian bytes each. Store that
full 16-byte digest in the low 128 bits of a 256-bit word with high bits zero:
h0 OR (h1 << 32) OR (h2 << 64) OR (h3 << 96). Equality of stored digest words
is exactly equality of all profile digest bytes. This definition includes
steps 0 through 63 of the sole padded block and all feed-forward state words.
There is no chosen IV, free-start state, truncation, or compression-only target.

## 2. Finite algorithm and stopping rule

Draw exactly N independent uniform 256-bit words X[0],...,X[N-1] using the
model's random-word primitive. Do not filter, reject, redraw duplicates, or
expand a deterministic seed. Complete all N draws and hash evaluations even
if an early prefix would contain a collision.

Reserve flat arrays A and B, each with N two-word records. A record is
(full digest H(x), message word x), occupying 64 bytes. Record i starts at
the array base plus (i << 1) word positions. Explicitly zero both arrays,
then for i=0,...,N-1 draw x, compute section 1's H(x), and store (H(x),x)
in A[i]. All retained randomness is in the stored message words.

Sort lexicographically by unsigned (digest word, message word), using stable
bottom-up merge sort. Initialize source=A, destination=B. For
w=1,2,4,...,N/2, and within that pass l=0,2w,...,N-2w, merge source[l:l+w]
and source[l+w:l+2w] into destination[l:l+2w]. Set i=l, j=l+w, k=l. Until
k=l+2w, choose the left head if the right run is exhausted, or if the left
run is nonempty and its key is no greater than the right head's key; otherwise
choose the right head. Test exhaustion before loading a head. Copy both
words of the chosen record; increment its head index and k. After ALL run
pairs of one complete pass have been merged, swap the two array base
registers and double w. This swap copies no array. There are exactly 65
passes and no partial runs, because N is a power of two. Do not recurse.

Scan consecutive records (i-1,i), i=1,...,N-1, in the final source array.
If their digest words differ OR their message words are equal, continue the
scan. In particular, a repeated identical message never terminates the scan.
At the first equal-digest, unequal-message pair, recompute both complete
hashes from their original 32-byte messages. Check distinctness and equality
of the recomputed full digest words, output the two messages if the checks
pass, and halt. If those checks fail, halt with failure; that branch cannot
occur in exact RAM execution. If the scan ends without such a pair, halt
with failure. Perform no restart or hidden preliminary collision search.
There are at most two extra hash evaluations for final verification.

Induction on the passes establishes sorting: singleton runs are sorted, and
repeatedly taking the smaller available head preserves the records and merges
two sorted runs. After 65 passes the whole array is sorted. Equal-digest
records are contiguous. A digest block containing different messages has
an adjacent boundary between different message keys. The scan detects one.
Therefore it succeeds exactly when some two sampled DISTINCT messages have
equal full hashes. Rechecking the full messages enforces the profile's
collision relation; identical inputs never count as success.

## 3. Distribution-free success proof

The probability space is solely N independent uniform draws from U message
words. H is one fixed deterministic function. For each of the D possible
full digests y, put p[y] = |{x:H(x)=y}|/U. These probabilities may be highly
nonuniform or zero. The H(X[i]) are independent with this common distribution:
summing the product input law over each fixed preimage set gives the product
of the corresponding p[y]. This does not assume random MD5, uniform hashes,
independent internal MD5 steps, or any random-oracle property.

The uniform output distribution maximizes the probability of N distinct
outputs. Here is a self-contained proof. Let e_k(p) sum products over all
k-element subsets of coordinates; e_0=1 and e_k=0 for impossible subset
sizes. The no-repeat probability is N! e_N(p). On the compact probability
simplex, e_N has a maximum; among its maximizers choose a point minimizing
the sum of coordinate squares. For two coordinates a,b and remaining vector r,

e_N(p) = e_N(r) + (a+b)e_(N-1)(r) + ab e_(N-2)(r).

Replace a,b by their mean. Their sum is unchanged and their product increases
by (a-b)^2/4. Since e_(N-2)(r)>=0, e_N cannot decrease. It cannot increase
at a maximum, so the averaged point is also a maximizer. If a!=b, its sum
of squares decreases by (a-b)^2/2, contradicting the choice of maximizer.
Thus all coordinates of that maximizer are 1/D. This proves the inequality
also for distributions with zero-probability outputs, without surjectivity.
Since N<=D,

P(all full hash outputs distinct) <= N! binom(D,N)/D^N
                                = product_(j=0)^(N-1) (1-j/D).

For t_j=j/D in [0,1), 1/(1-t_j)>=1+t_j, and
product_j(1+t_j)>=1+sum_j(t_j) since the other terms are nonnegative. Hence

product_j(1-t_j) <= 1/(1+sum_j(t_j)),
sum_j(t_j) = N(N-1)/(2D) = 2 - 2^-64 >= 3/2.

Consequently the event C that some full hash repeats has probability at
least 3/5. This could include identical inputs. Let R denote any repeated
input word. Independence and a union bound give

P(R) <= binom(N,2)/U < 2^129/2^256 = 2^-127.

On C intersect complement(R) two DISTINCT messages collide, and section 2's
scan returns a valid pair. Therefore

P(success) >= P(C)-P(R) >= 3/5 - 2^-127 > 1/2 >= 0.39.

The strict inequality already follows from 2^-127<1/10. The submitted 0.5
is a conservative algorithmic lower bound, not an exact success estimate or
reviewer confidence. This finite proof applies to the exact input and output
sizes and the stated N, with no birthday approximation or empirical
extrapolation. It needs only a deterministic map with 128 output bits.

## 4. Charged implementation ledger

A word is 256 bits = 32 bytes. Under `collision-frontier-v3`, a selected
64-step MD5 compression costs one `target-compressions` unit, and every
OTHER primitive word operation also costs one unit. The selected compression
includes its step function. Below, input construction, IV, feed-forward and
output packing receive additional allowances even if partly included in the
primitive's interface. Loops use flat direct addressing, comparisons,
branches, loads/stores, additions and shifts; multiplication by two is a
shift. No uncharged allocator, sort, division, arbitrary-length integer
comparison, floating point, or software library is assumed. Counters and
addresses fit in one word: all table byte offsets are below 2^73 and loop
indices below 2^67. The maximum message fits exactly in one word.

Both arrays occupy fixed disjoint intervals; no allocation search is needed.
Only their actually reserved capacity is counted as table memory. Model RAM
registers and scratch are included in fixed storage below. The hash primitive
is specified in section 1, so no outside target specification must be fetched
to establish its input/output semantics. Every budget includes loop tests,
branches, address arithmetic, operand access and register transfers, allowing
a register transfer to cost a load and a store.

| Work, including unsuccessful executions | Upper bound in charged units |
| --- | ---: |
| Initialize fixed program, literals and scratch | 2^24 |
| Clear both arrays; draw, hash and store all N records | 2^10 N |
| One complete merge-sort pass, with setup/bookkeeping | 2^8 N |
| All 65 merge-sort passes | 65 * 2^8 N |
| Full adjacent scan, plus final verification and output | 2^10 N + 2^16 |

The following explicit allocations justify the operation constants. Clearing
the 4N array words takes at most sixteen operations per word for pointer
access, store, increment, comparison, branch and constants, hence 64N units.
For each record, a random word costs one and a compression costs one.
Extracting eight 32-bit message words takes at most 64 operations; assigning
the remaining eight padded words and IV takes at most 64; feed-forward and
digest packing take at most 128; addressing, storing the record, retaining
the random word and loop control have another 128. These sum to less than
512 per record including clearing, beneath the 1024 allowance. Explicit
32-byte serialization would add fewer than 256 per record and still fit;
the actual computation directly uses the equivalent padded block words.

A merge output iteration has 32 operations for exhaustion tests/branches and
operand access, 48 for loading up to two two-word heads and lexicographic
comparison, 32 for addresses and copying the chosen two words, and 32 for
index updates/loop tests: at most 144 operations. Run-pair setup/termination
uses at most 128 more operations per pair. Each pair emits at least two
records, so this contributes at most 64N per pass. The remaining 48N within
256N covers pass control, base swaps and operand management. Lexicographic
comparison uses at most two order comparisons and one equality comparison,
plus branches; there is no larger-than-word key primitive. Head reads follow
exhaustion tests. No array copy or recursion stack is hidden in this budget.

Loading two adjacent records, comparisons, branches, indices and loop
control take at most 128 operations per scan pair, beneath its 1024N
allowance. At most one pair is verified. Two complete one-block hashes,
distinctness/full-equality tests and outputting both 32-byte messages cost
less than 2^16 additional units, including byte conversion by 32 shift/mask
iterations per message. Charge the full scan even on early success.

Provision a separate fixed area of 2^24 BYTES for code, literals, scratch,
counters and output. A straightforward loop implementation uses fewer than
2^12 primitive instructions after expanding scratch loads and stores: fewer than 128 straight-line operations for
sampling and padding/packing, fewer than 256 for merge selection/copy,
fewer than 256 for scan/verification, with fixed initialization and loop
control well within the remainder. These are reusable instructions, not N
unrolled iterations or 65 separately unrolled passes. Even an instruction
encoding of an opcode plus seven full 256-bit operand words occupies at
most 2^12*8*32 = 2^20 bytes. Constants (64 MD5 constants, rotations, IV,
array bounds and masks) use fewer than 256 words; fewer than 512 scratch
words suffice for indices, heads, padded block, state and output. Together
those two sets use fewer than 2^15 bytes. The 2^24-byte fixed provision thus
also has room for this finite specification text and any stated slack.
Clearing its 2^19 word locations at at most sixteen operations per location,
and populating its small code/literal tables, take fewer than 2^24 operations.
This fixed initialization is the first ledger row; there is no uncharged
precomputation. No nonuniform advice or stored collision is used.

Total charged time on EVERY execution, including failure, is bounded by

T <= (2^10 + 65*2^8 + 2^10) N + 2^24 + 2^16
   = 18688 * 2^65 + 2^24 + 2^16 < 2^82.

Thus expected time also satisfies the bound. Exactly N model random draws
are charged. No stored random tape or seed expansion is assumed; the message
words already retain all randomness used by the algorithm. There are zero
restarts, so no omitted restart or amplification factor is needed for 0.5.

The simultaneous arrays use exactly 2*N*2*32 = 128N = 2^72 bytes, including
both copies of every stored message and digest. The fixed area gives
peak M <= 2^72+2^24 < 2^73 bytes. This includes code, literals, all randomness
retained, tables, padding, working state and output; it is theoretical RAM
capacity, not an assertion that the experiment can run on available hardware.

| Claim field | Value | Units and interpretation |
| --- | ---: | --- |
| time_log2 | 82 | log2 of the upper bound on all charged operations/compressions |
| memory_log2_bytes | 73 | log2 of the upper bound on peak bytes, including code |
| data_log2 | 66 | N+2 < 2^66 complete-message evaluations, each on 32 message bytes: N samples plus at most two verification repeats; no external data |
| preprocessing_log2 | 72 | Fixed initialization plus clearing all table words: at most 2^24+64N < 2^72 operations, already included in the first two time rows |
| nonuniform_advice_log2_bytes | 0 | Zero actual advice; because log2(0) cannot be encoded, 0 supplies a valid outward bound log2(1 byte) |
| success_probability | 0.5 | Proven conservative lower bound under the specified model coins |

The data field counts evaluations, not memory bytes or free oracle answers;
every answer is computed and charged. Fixed public constants and program are
charged as preprocessing and memory even though they are not nonuniform
advice. No precomputed target table, differential trail or imported collision
exists. The score 155 is a conservative time-plus-byte-memory upper bound,
not a birthday exponent used as a complete ledger or Pareto-dominance claim.

## 5. Evidence, assumptions and limits

`heuristics` is empty. Fresh independent random words are exactly the model's
primitive, rather than an additional hash heuristic. Section 1 specifies the
exact complete target; section 2 specifies a finite algorithm and proves
detection; section 3 proves its success bound at the actual sizes; section 4
accounts for its implementation. No ideal-MD5 assumption, internal-step
independence, empirical extrapolation or deterministic PRNG is used.

The valid certificate manifest is empty: no particular collision is supplied
as advice or certified evidence. There is no experiment manifest and no
submitted executable source. Full-scale execution and sampled toy programs
are not claimed as support for the finite argument. Each material claim is
analytic and can be assessed from this package without external links.
The selected target is the explicit full-round MD5 control, not a claim
about a first-unbroken boundary. A selected-lane AI review remains distinct
from mathematical proof and human acceptance.
