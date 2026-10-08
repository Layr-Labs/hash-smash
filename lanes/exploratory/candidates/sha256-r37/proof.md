# A distribution-free complete-message baseline for SHA-256 r37

## Claim and scope

This package specifies a classical randomized algorithm for the exact
`sha256-r37-prefix-v1` target in the exploratory lane. Its worst-case total
charged time is less than `2^132` target-compression units, its peak memory is
less than `2^136` bytes, its preprocessing is less than `2^125` such time units,
and its probability of returning distinct complete messages with equal full
256-bit digests exceeds `0.39`. The probability is over fresh independent
algorithmic coins for the fixed target; no property resembling a random oracle,
balance, differential independence, or pseudorandomness of SHA-256 is assumed.
The claim reports conservative upper bounds, not measured work or an executed
collision search. No collision witness or empirical evidence is asserted.

The required `baseline_improved` value `sha256-r37-nominal-v2` identifies an
organizer nominal reference, not an established attack. This construction does
not claim to beat that reference's display value of 128. `ready` requests review;
it is not qualification, a trusted score, or human acceptance.

All arithmetic in the algorithm below fits a 256-bit RAM word except that a
message block occupies two words and each retained record occupies three.
Large integers used only in the mathematical analysis need not be computed by
the algorithm. The selected target compression is the cost model's priced
primitive: standard SHA-256 schedule and constants, indices 0 through 36
inclusive, and the standard wordwise feed-forward. Other operations, including
its input/output marshaling, are charged separately at `1/C`, with `C = 2644`.

## Complete messages and their hashes

Put `n = 2^128`. In each of exactly n trials obtain two fresh independent uniform
256-bit random words U and R, and set `V = R AND (2^128 - 1)`. The complete
message is the 48-byte string `BE32(U) || BE16(V)`, where BEk denotes exactly k
bytes in big-endian order. Thus messages are iid uniform on a domain D of size
`d = 2^384`. All have original bit length 384, which satisfies the profile's
length limit. Repeated sampled inputs are allowed and are not counted as
collisions merely because their digests agree.

The sole padded block, viewed as two 256-bit big-endian words, is exactly

```
B0 = U
B1 = (V << 128) OR (1 << 127) OR 384.
```

Indeed, the message uses bytes 0 through 47; byte 48 is 0x80, bytes 49 through
55 are zero, and bytes 56 through 63 encode the original bit length 384 in
64-bit big-endian form. There is no omitted extra padding block. Each digest
computation begins anew at the standard fixed SHA-256 IV, executes the first
37 rounds of this block, adds each working word to its incoming chaining word
modulo `2^32`, and serializes all eight resulting words in standard order.
Denote this complete-message function by h and its 256-bit digest word by Y.
No chaining state is chosen by the algorithm and no output bit is discarded.

For clarity, the eight incoming 32-bit IV words are
`6a09e667 bb67ae85 3c6ef372 a54ff53a 510e527f 9b05688c 1f83d9ab 5be0cd19`.
Compression expands the usual schedule only as needed through index 36, uses
the original-index constants, and performs the usual feed-forward after round
36. The trusted profile defines this primitive; calling it once on the stated
padded block computes h, not a compression-only collision relation.

## Algorithm, data structures, and stopping rule

Use two arrays A and B, each of n records. A record is three separate 256-bit
words `(Y,U,V)`; the upper 128 bits of V are zero. There is no implicit nonce
recovery algorithm, hash table, pointer per record, or stored list of trial
seeds. Initialize both arrays to zero, counting this work. Sample all n messages,
compute h once for each, and write their records into A. Discard R after forming
V. No rejection sampling, deduplication, or early trial stopping occurs.

Sort A by its entire unsigned 256-bit Y key with bottom-up two-buffer merge
sort. At width w, initially 1, merge each consecutive pair of runs of exactly w
records from the source into the destination, then exchange the buffer roles
and double w. Stop after width n/2. Since n is a power of two, every pair is
full and there are exactly 128 passes. Copy all three record words on every
emission. Compare full digest keys and choose the left run on equality. This
sorting procedure has a distribution-independent work bound even when every
digest or every message is the same.

The following is inert algorithmic pseudocode, not an experiment program.
Indices in this description count records; the implementation maintains word
pointers with stride 3, and computes `3*x` as `(x << 1) + x` when needed.

```
for t = 0,...,n-1:
    U = RANDOM256(); R = RANDOM256(); V = R AND (2^128-1)
    form (B0,B1) as above; Y = COMPRESS37_WITH_FEEDFORWARD(IV,B0,B1)
    A[t] = (Y,U,V)
src = A; dst = B; w = 1
while w < n:
    for l = 0,2*w,4*w,...,n-2*w:
        i = l; j = l+w; left_end = l+w; right_end = l+2*w
        for k = l,...,right_end-1:
            if i == left_end: p = j; j = j+1
            else if j == right_end: p = i; i = i+1
            else if src[i].Y <= src[j].Y: p = i; i = i+1
            else: p = j; j = j+1
            dst[k] = src[p]   # all three words
    exchange(src,dst); w = w+w
for k = 1,...,n-1:
    if src[k-1].Y == src[k].Y:
        if (src[k-1].U != src[k].U) OR (src[k-1].V != src[k].V):
            reconstruct both 48-byte messages
            recompute their complete hashes from the fixed IV
            return the messages if they are distinct and both hashes agree
            otherwise return FAILURE
return FAILURE
```

The final check uses two additional selected compressions at most; it never
retries failed verifications. In the exact computation model this check cannot
fail after a true table match. No restart or success amplification is used.
Failures from samples containing no distinct-input collision return FAILURE
after the bounded scan; their entire work is included in the claim.

Merge correctness follows by induction on w: one-record runs are sorted;
choosing the smaller unconsumed front key preserves order and emits every
record exactly once. All equal digest keys are therefore consecutive in the
final array. If any equal-key run contains two different messages, some adjacent
records in that run have different messages: otherwise transitivity of equality
would make the whole run one repeated message. Consequently the adjacent scan
finds a distinct-input collision whenever one exists among the samples, even
if other records are repeated copies of an input. Conversely the final explicit
check prevents returning anything other than two distinct complete target inputs
with equal full digests. Returning the same sampled input twice is not success.

## Distribution-free success bound

Fix h throughout. For each 256-bit digest y define
`p_y = |{m in D : h(m)=y}| / d`. Applying a fixed deterministic function to iid
inputs produces iid outputs with this distribution, which need not be uniform.
There are `M = 2^256` possible output labels, including those with empty fibers.
For `2 <= n <= M`, the probability that all outputs differ is
`n! e_n(p_1,...,p_M)`, where e_n is the elementary symmetric polynomial of degree
n: each unordered set of n distinct output labels has n! possible orders.

Here is a full justification that this probability is maximized by the uniform
output distribution. Holding the other coordinates fixed, e_n has the form
`A + (a+b) B + a*b E` in any two selected coordinates, with `E >= 0`.
Replacing a and b by their average preserves their sum and cannot decrease e_n.
On the compact probability simplex choose a maximizer of e_n which minimizes
the sum of squares of its coordinates among all maximizers. If two coordinates
differ, averaging them either increases e_n, contradicting maximality, or
preserves it while strictly decreasing the sum of squares, contradicting the
choice of maximizer. Hence that maximizer is uniform. This also covers zero
coordinates and distributions with fewer than n nonempty fibers.

It follows, for this fixed target and without an output-distribution hypothesis,
that

```
Pr[no repeated output] <= n! choose(M,n) / M^n
                       = product(i=0,...,n-1) (1-i/M)
                       <= exp(-n(n-1)/(2*M)).
```

The last inequality follows by multiplying `1-z <= exp(-z)` for `0 <= z < 1`.
For example, `log(1-z) <= -z` follows by integrating `1/(1-z) >= 1` from 0 to z.
No independence among pairwise collision events was used.

Let E_out be the event of any repeated output and E_in the event of any repeated
input. Each of the `choose(n,2)` input pairs is equal with probability `1/d`,
so the union bound gives `Pr[E_in] <= n(n-1)/(2*d)`. On `E_out` outside `E_in`
there is a collision of distinct messages and the scan succeeds. This is a
sufficient success event, not a claim that input repetition always prevents
success. Therefore

```
Pr[success] >= 1 - exp(-n(n-1)/(2*M)) - n(n-1)/(2*d).
```

For the actual chosen parameters,

```
x = n(n-1)/(2*M) = 1/2 - 2^-129 > 499/1000,
n(n-1)/(2*d) = 2^-129 - 2^-257 < 2^-129.
```

A rational check avoids relying on rounded floating-point exponentials:

```
exp(x) > 1 + 499/1000 + (499/1000)^2/2 + (499/1000)^3/6
       = 9865254499/6000000000,
exp(-x) < 6000000000/9865254499 < 609/1000.
```

The final comparison is verified by
`6000000000000 < 609*9865254499 = 6007939989891`.
Also `2^-129 < 1/1000`. Thus success is strictly greater than
`391/1000 - 2^-129 > 390/1000 = 0.39`. The bound applies to every fixed function
on these messages with a 256-bit output, including the exact reduced SHA-256
profile. It neither extrapolates from smaller rounds nor assumes a cryptanalytic
property of the fixed target. The ideal independent random-word primitive is
part of collision-frontier-v5, not an assumption that a finite deterministic
seed expansion supplies the full attack's coins.

## Complete operation ledger

One target compression costs 1 and every ordinary 256-bit primitive costs
`1/2644`. Count total work on one processor; parallel latency is irrelevant.
All bounds below hold on every random tape. There is no expected-time tail,
uncharged offline search, advice generation, or unbounded restart loop.

For explicit lowering, a simple scalar assignment, one-operation arithmetic
assignment, comparison-and-branch, or one direct array word load/store with a
base-plus-offset address uses at most eight primitive operations. This allowance
covers up to two operand loads, one arithmetic/address/comparison operation and
one result store or branch, plus up to four instruction fetches if these are
charged. More complex expressions are split into these elementary statements;
copying a three-word record uses six elementary loads/stores. Registers, if
spilled, fit the same convention. All loops below are iterative; no recursion
stack or multiword comparison routine is needed. A branch back can use a fixed
true condition. Loop tests, increments, moves and branches are charged.

Initialization: zero the `6*n` array words in a pointer loop. A word takes at
most four elementary statements (store, pointer increment, comparison and
branch), or 32 primitives. The bound `256*n` therefore covers all array clearing,
including its end tests and initial pointers for n >= 2. Load/initialize the
fixed program, constants and scratch area within an additional `2^24` primitives.
This initialization is counted as preprocessing, even though the two large
arrays could instead have been written lazily.

Sampling and hashing: allow 128 elementary statements, or 1024 ordinary
primitives per trial, besides the one priced compression. This covers the two
random words (each draw including destination storage fits the allowance), mask,
padded-block formation, loading the fixed IV, compression argument setup,
full digest packing, record stores and loop control. More explicitly, forming
the mask and padded block needs at most 12 statements; initializing and
marshaling the eight IV words and two block words at most 24; packing the eight
32-bit output words by load/shift/OR at most 32; random draws, masking, three
record stores, pointer operations and loop control at most 32. Their sum is
100, below 128. The standard schedule, 37 rounds and feed-forward are in the
priced compression primitive, not additional free hash computations.

Sorting: at most 256 ordinary primitives per emitted record per pass, with an
additional fixed overhead of at most `2^24` primitives for all pass boundaries
and final verification together. The following expansion establishes the per
record bound instead of treating comparison sorting as a unit-cost black box:

| Emission work in a word-pointer implementation | Elementary statements, at most |
| --- | ---: |
| Left/right exhaustion tests, two front-key loads, key comparison/branch | 5 |
| Choose source pointer and advance that run by three words | 2 |
| Load and store the three fields using offsets 0, 1 and 2 | 6 |
| Advance destination, output loop control, dispatch/back branches | 7 |
| Reserved spill/address temporaries beyond those already counted | 4 |
| Total per emission before pair setup | 24 |

Use pointer endpoints so each exhaustion test is one comparison/branch.
A pair's setup/advance requires at most 16 elementary statements: deriving
run span from w with shift/add, setting two source pointers and two endpoints,
the destination pointer/end, and advancing/testing the next pair. Each pair
emits at least two records, so this adds at most eight elementary statements
per emission. The combined maximum is `(24+8)*8 = 256` primitives per record.
Nonzero constant offsets in the six field moves use at most four underlying
operations even when address construction and moves are charged. There are
exactly `128*n` emissions across all passes. For the 128 outer passes, fewer
than 32 elementary statements each suffice to exchange pointers and update/test
w; these fit amply within the stated fixed overhead. No bucket distribution or
expected lookup cost is assumed.

Scanning: charge 256 ordinary primitives per adjacent pair, rounded to `256*n`.
The worst case has two digest loads, comparison/branch, four message-word loads,
two word comparisons, their Boolean combination, and loop/address control,
within 32 elementary statements. This includes repeated-input matches that are
skipped. On the first distinct pair only, reconstruct the two blocks, reload IVs,
recompute two complete hashes, compare both full digests and messages, and write
the output (96 bytes in at most four output words). Its ordinary work fits the
fixed `2^24` sort/verification overhead above, and its two compressions are
counted separately. No verification is repeatedly performed per identical input.

The combined conservative ledger is consequently

| Category | Selected compressions | Ordinary primitives, upper bound |
| --- | ---: | ---: |
| Preprocessing, including both arrays | 0 | `256*n + 2^24` |
| All n random messages and complete hashes | n | `1024*n` |
| All 128 merge passes | 0 | `32768*n` |
| Complete adjacency scan | 0 | `256*n` |
| Pass boundaries, final verification and output | 2 | `2^24` |
| Total | `n+2` | `34304*n + 2^25` |

This includes `2*n` independent random words, even though half of each R is
discarded. Random generation is streamed; no random tape is stored separately.
All unsuccessful trials are among the n paid trials. There is no preprocessing
that finds a collision for later inclusion in the code.

Thus the worst-case charged total is

```
T <= n+2 + (34304*n + 2^25)/2644
   = (36948*n + 2^25 + 5288)/2644
   < 16*n = 2^132.
```

For the strict inequality, `16*2644 - 36948 = 5356` and
`2^25 + 5288 < 5356*2^128`. The claim `time_log2 = 132` is therefore rounded
up conservatively. It is not merely the birthday sample exponent 128.
Preprocessing separately obeys

```
P <= (256*n + 2^24)/2644 < n/8 = 2^125,
```

because `2644/8 - 256 = 74.5` and `2^24 < 74.5*2^128`.
Preprocessing is already included in T; it is not added again to the score.

## Peak memory, code, and advice

Each record occupies 96 bytes. Two n-record buffers use exactly `192*n` bytes;
this includes retained complete messages (in reconstructible two-word form),
the full digest and the unused upper half of V. Each table is initialized and
fully charged above. No third table, sorting permutation, per-record pointer,
auxiliary lookup structure, or retained random tape is used.

Reserve an additional `2^20` bytes for code, public constants, counters, stack,
compression state/schedule, temporary record fields and output. This comfortably
admits a direct bounded-loop implementation of the above pseudocode and SHA-256:
at most 4096 instructions, each encoded in at most four 256-bit words, use
`2^19` bytes; fewer than 4096 additional 256-bit words of constants, schedule,
register spill slots and I/O use `2^17` bytes. The code needs no unrolled n-sized
program: only the sample loop, three merge loops, scan and constant-round hash
routine. A 37-word schedule, eight IV words, the first 37 public round constants
and fixed masks fit these static bounds. Reading/initializing this storage is
included in the fixed preprocessing allowance. Code storage is counted even
though execution of the selected compression is priced as one unit.

Peak live storage is at most `192*n + 2^20 < 256*n = 2^136` bytes. Array bases,
endpoints and byte addresses, including fixed storage, are below `2^137` and
fit within a 256-bit word. The largest loop count is n and products by 2 or 3
are exact without overflow; no multiplication instruction is needed. The
resource model permits this theoretical RAM size; feasibility on existing
hardware is not asserted.

The program is uniform and uses only the public fixed profile constants and
fixed numerical parameters stated here, all charged as code/constants. There
is zero target-dependent nonuniform advice and no precomputed collision. Since
the schema requires a nonnegative logarithmic advice bound, the claim's
`nonuniform_advice_log2_bytes = 0` means an upper bound of one byte, which covers
zero bytes; it does not assign a logarithm to zero or hide the code. No legacy
`data_log2` field is used.

## Evidence and source context

The entire success and resource argument is given above. The empty certificate
manifest asserts no supplied witness. No experiment is declared or required by
this analysis, and none of the bounds relies on sampled toy behavior, benchmark
timing, a seeded PRNG, or executing the infeasible full search. `heuristics: []`
means there are no premises beyond the specified RAM/random-word/target model
and the mathematical arguments here; advisory or official reviewers may still
identify mistakes in those arguments.

Primary sources consulted for scope and conceptual context:

- NIST, FIPS 180-4, Sections 5.1.1, 5.3.3 and 6.2.2, for standard SHA-256 padding,
  initialization, schedule and feed-forward. The organizer profile, not the
  unmodified 64-round standard, fixes the prefix reduction to 37 rounds.
  Source: `https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf`.
- Mihir Bellare and Tadayoshi Kohno, *Hash Function Balance and Its Impact on
  Birthday Attacks*, full version, May 2004, Figure 1 and Sections 3-4, distinguish
  fixed functions, iid sampled inputs and trivial repeated-input matches from
  distinct-input collisions. Source:
  `https://homes.cs.washington.edu/~yoshi/papers/Hash/balance.pdf`.

Those citations supply context rather than a missing proof step or a claimed
attack on this round count. The symmetric-polynomial maximization, distinct-input
correction and target-specific operation ledger needed to assess this package
are supplied directly here. No historical candidate's score or qualification is
transferred to this package.
