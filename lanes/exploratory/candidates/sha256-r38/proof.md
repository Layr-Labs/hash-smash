# SHA-256 r38: an unconditional generic organizer baseline

## Claim and scope

This package specifies a classical randomized collision construction for the exact
`sha256-r38-prefix-v1` complete-message hash. Its worst-case single-batch bounds are
total time at most `2^132` target-compressions, peak memory at most `2^136` bytes,
and preprocessing at most `2^123` target-compressions, already included in time.
Its algorithmic success probability is greater than 0.39. No nonuniform advice,
precomputed collision, cryptanalytic heuristic, or experiment is used.

These are analytical upper bounds, not measured resources or an executed attack.
The large memory requirement is part of the claim. This construction is not a
new reduced-round cryptanalytic result and does not beat the nominal exponent
128. The required identifier `sha256-r38-nominal-v2` names an organizer display
reference, not an established attack, qualified baseline, or security bound.
`ready` requests review; it does not establish qualification or an official score.

The target uses the standard SHA-256 IV, standard schedule and round constants,
round indices 0 through 37 inclusive on EVERY padded block, and normal addition
of the eight working words to the incoming chaining state modulo `2^32`.
All eight final words are serialized in standard big-endian order. No output
truncation, free-start choice, altered padding, or compression-only collision
relation is used. The probability argument applies to this fixed function,
without assuming it is random, uniform, balanced, or injective on any subset.

## Messages, representation, and hashing

Let `n = 2^128`, `M = 2^256`, and let `D` be all 48-byte strings, so `d = 2^384`.
Every message has bit length 384, less than the profile limit `2^64`.
For each sample call the model's independent uniform 256-bit random-word
primitive twice, obtaining `u,v`. Set `x = u` and `y = v AND (2^128 - 1)`.
The complete message is

```text
m(x,y) = BE_32_bytes(x) || BE_16_bytes(y).
```

This is an injective encoding of the RETAINED pair `(x,y)`, and is uniform on D.
The discarded upper 128 bits of v are still paid for. Every stored y is the
masked value with its upper 128 bits ZERO; the unmasked v is never a table field
or comparison key. Copying, comparing, and reverifying use this same canonical
representation. All `2n` word draws are fresh and independent. No seed expansion
or deterministic pseudorandom generator replaces the specified random primitive.

For 48 bytes, FIPS padding is the message, `80` in hexadecimal, seven zero bytes,
and the 8-byte big-endian integer 384. The resulting 64 bytes are EXACTLY ONE
padded block, not a raw 64-byte input followed by another padding block.
Represent this block by two 256-bit words interpreted in big-endian order:

```text
B0 = x
B1 = (y << 128) OR 2^127 OR 384.
```

The nonzero fields of B1 are disjoint. Splitting B0 and B1 into sixteen
big-endian 32-bit words yields the ordinary padded SHA-256 block. Reset to the
standard IV for EACH sample. Evaluate the selected 38-round compression,
including feed-forward. Serialize all eight resulting 32-bit words as one
256-bit digest word `h`. Thus one selected compression is the full hash of
each sampled message; there is no extra message block or padding compression.
This is a restriction of the permitted message domain, not a modified hash.

A table record consists of three 256-bit RAM words `(h,x,y)`, or 96 bytes.
The unused high half of the y word is zero. The record stores the entire
message, so reconstruction never requires a PRNG seed, inverse hash, or search.
The actual output pair consists of the two UNPADDED 48-byte messages.

## Bounded algorithm

Use two flat arrays A and B, each containing n three-word records. Allocate
disjoint word-address intervals of length `3n`; explicitly clear all `6n` words.
The reserve for code, constants, scalar variables, hash state, and output is
described below. No hash table, allocator service, recursion, or unpriced sort
subroutine is required.

1. For `i = 0,...,n-1`, independently generate x,y, construct the padded block,
   compute its full digest h as above, and put `(h,x,y)` in A[i]. Complete all
   n samples, including repeated inputs and every unsuccessful trial.
2. Sort A by the full digest word using iterative bottom-up merge sort with B
   as the destination buffer. At pass widths `w = 1,2,4,...,n/2`, merge each
   adjacent pair of runs of w records. Compare digests as unsigned 256-bit
   words; on equal keys take the left record first. Copy the WHOLE record.
   Exchange source/destination base pointers after each pass. All run lengths
   divide n exactly. There are exactly 128 passes; there is no leftover run.
3. Scan every adjacent record pair in the final sorted buffer. If the digests
   match and the retained pairs `(x,y)` differ, reconstruct both complete
   48-byte inputs, recompute both full selected hashes from the fixed IV, and
   check digest equality and message inequality again. Return those messages.
   Identical inputs are skipped; they do not terminate the scan.
4. If the scan finds no such adjacent pair, return FAILURE. A verification
   mismatch also returns FAILURE, rather than invoking an unbounded recovery.
   In the exact RAM model a mismatch cannot occur, as proved below.

This is a fixed-size batch, not an expected-time loop. It runs once, with no
restart, adaptive trial budget, success amplification, or parallel work omitted.
A success may terminate the final scan early, which only reduces the bound.

For clarity, the merge can be implemented by these word-pointer operations.
These are mathematical pseudocode, not an experiment to execute:

```text
run_words := 3                         # compute once as 1+1+1
repeat 128 times:
    source_start := source_base
    destination_start := destination_base
    while source_start < source_base + 3*n:
        L := source_start
        LE := L + run_words
        R := LE
        RE := R + run_words
        O := destination_start
        OE := O + run_words + run_words
        while O < OE:
            if L == LE: choose R
            else if R == RE: choose L
            else if source[L] <= source[R]: choose L
            else: choose R
            copy chosen[0], chosen[1], chosen[2] to O[0], O[1], O[2]
            advance the chosen pointer by 3
            O := O + 3
        source_start := RE
        destination_start := OE
    exchange source_base and destination_base
    run_words := run_words + run_words
```

Addresses are word addresses and pointers advance through disjoint arrays.
Base addresses plus `6n` and all counters are less than `2^256`, so the model's
modular arithmetic implements the needed integer additions without overflow.
`3n` is obtained by two additions; no multiplication primitive is assumed.
Generation, clearing, and scanning likewise use incremented pointers.
The merge body never reads an exhausted run. Tail records are copied by the
same bounded loop using the exhaustion branch, not by an uncharged bulk copy.

## Correctness

Generation stores the exact full hash of each retained message. Every merge
preserves records and sorts its two already sorted runs. Induction on passes
therefore gives a sorted permutation of all n records.

All equal-digest records form a contiguous group. If a group contains two
different messages, some adjacent pair in the group must differ: otherwise
transitivity of adjacent equality would make every message in that group equal.
Consequently the scan finds a distinct-input collision whenever ANY two sampled
distinct inputs have equal digests, including when repeated inputs are present.
Canonical masked y values ensure record-input equality is equivalent to complete
message equality. The rehash confirms that same deterministic relation and cannot
fail in this model. The returned messages satisfy the profile's domain,
distinctness, and full-digest equality requirements.

## Success probability for the fixed target

Fix the actual target function `f: D -> {0,1}^256`. For each possible digest z let
`p_z = |{m in D : f(m)=z}| / d`. Some fibers may be empty or unusually large.
Since the INPUT samples are independent, their deterministic images are
independent draws from p. This proves the independence needed below; it does not
assume independence of different collision-pair events or random-oracle behavior.

For `n <= M`, the probability of all n outputs being different is
`n! e_n(p_1,...,p_M)`, where `e_n` is the sum, over all n-element subsets of
coordinates, of the product of those coordinates. The factor n! counts all
orders of each set. The following argument bounds this probability without
making any supposition about SHA-256's output distribution.

For any two coordinates a,b, with all others fixed, write

```text
e_n = E_n + (a+b) E_(n-1) + ab E_(n-2),
```

where the E terms use the remaining coordinates and are nonnegative (with
`E_0=1`). Averaging a,b preserves their sum and does not decrease ab. Hence
averaging cannot decrease e_n. The probability simplex is finite dimensional
and compact; e_n is continuous. Among its maximizers choose one minimizing
the continuous quantity `sum p_z^2`. If two coordinates differed, averaging
would either increase e_n, contradicting maximality, or preserve e_n while
strictly decreasing that sum, contradicting the tie-break. The maximizing vector
is therefore uniform. This is an extremal argument, not an output assumption.

It follows that, for the event A of at least one repeated output,

```text
Pr(A) >= 1 - n! choose(M,n) / M^n
       = 1 - product_(i=0)^(n-1) (1 - i/M)
       >= 1 - exp(-n(n-1)/(2M)).
```

The last inequality uses `1-t <= exp(-t)` for `0 <= t < 1`, applied to each
factor and summed exponents. Let B be the event that some INPUT is repeated.
For each pair of indices that probability is exactly `1/d`; the union bound
gives `Pr(B) <= n(n-1)/(2d)`. On `A AND NOT B`, two distinct inputs collide.
The scan can additionally succeed on some outcomes in B, but we need only

```text
Pr(success) >= 1 - exp(-n(n-1)/(2M)) - n(n-1)/(2d).
```

This subtraction is essential: equality of two sampled inputs alone is not a
collision under the target relation. No independence between A and B is used.

With `n=2^128`, `M=2^256`, and `d=2^384`, set

```text
x = n(n-1)/(2M) = 1/2 - 2^-129 > 499/1000
b = n(n-1)/(2d) < 2^-129.
```

The positive exponential series gives the following rational bounds:

```text
exp(x) > 1 + (499/1000) + (499/1000)^2/2 + (499/1000)^3/6
       = 9865254499/6000000000.
exp(-x) < 6000000000/9865254499 < 609/1000.
Pr(success) > 391/1000 - 2^-129 > 39/100.
```

The last comparison holds because `2^-129 < 1/1000`. Thus the claimed 0.39 is
a lower bound over fresh algorithmic coins for this fixed reduced-round hash.
There is no conditional cryptanalytic premise or measured-confidence parameter.

## Resource ledger under collision-frontier-v5

One selected r38 compression costs 1; each other primitive costs exactly
`1/C` with `C=2728`. All bounds below count total serial computation and hold on
EVERY random tape, including batches that fail. A word is 256 bits = 32 bytes.
Both random-word calls are charged per sample. Hash input/output handling is
charged in addition to the selected compression.

The implementation uses only word loads/stores, additions/subtractions, shifts,
bitwise operations, comparisons, conditional branches, and the specified random
word primitive. No comparison, pointer arithmetic, or bulk copy is free.
Unsigned key comparison costs one comparison plus its control flow; no hashing
or byte-by-byte string comparison is hidden in a key comparison.
Scalar loads/stores and loop control are included in the following generous
straight-line budgets. Fixed loops are used instead of expanding n instructions.

### Initialization and preprocessing

Reserve the two arrays and the fixed workspace using explicit base addresses.
There is no hidden allocation oracle: all `6n` array words are cleared in a
pointer loop. Each word requires at most eight primitives: pointer load,
zero store, addition, updated-pointer store, limit load, comparison, branch,
and one spare operation. Charge `48n` ordinary operations.

Charge at most `2^20` additional ordinary operations to materialize the fixed
program/constants, initialize scalar state, form masks/limits, and clear the
fixed workspace. The code/working-store bounds below fit within `2^15` words;
even copying and clearing every such word with eight-operation loops twice
is less than `2^20`. Public constants can be loaded literally; no target-specific
search or other precomputation is performed.

Thus preprocessing is at most `(48n + 2^20)/2728` compression equivalents,
strictly less than `n/32 = 2^123`: multiply by 2728 and use
`48n + 2^20 < (2728/32)n = 85.25n`. This entire work is also in total time.
In particular, buffer initialization is NOT omitted from the preprocessing field.

### Per-sample work other than the compression

Use at most 512 ordinary operations per sample. A concrete upper allocation is:

| Work | Ordinary primitives per sample, at most |
| --- | ---: |
| Two independent word draws, retention, mask, B0/B1 construction | 32 |
| Split the two block words into 16 words, if needed by the compression interface | 96 |
| Load/reset all eight IV words and pass input/state to the selected primitive | 64 |
| Mask/pack all eight output words as a single full digest word | 64 |
| Store the three-word record, advance pointers, and generation-loop control | 64 |
| Extra scalar moves, mask/constant loads and call/return bookkeeping | 192 |
| Total | 512 |

For splitting, each of 16 fixed fields takes a load, shift, mask, store and at
most two associated moves, giving 96. Packing eight 32-bit fields by
shift-and-OR with masking/loading takes at most eight operations per field.
The padding formula needs only a shift and two ORs after masking y; no
byte-buffer allocator or library encoder is needed. Even an interface that
requires the explicit eight IV words is covered. The selected compression
includes its schedule, 38 rounds, and feed-forward at price 1.

There are n compression calls here, including samples later found to be repeats.

### Merge sort

For each emitted three-word record allocate at most 128 ordinary operations:
48 for run-exhaustion tests, two digest loads, comparison and selection;
48 for loading/storing all three fields and forming their addresses; and
32 for pointer updates, scalar stores, and output-loop comparison/branches.
These budgets cover explicit scalar memory traffic: there are at most two
exhaustion tests and one key comparison, three field loads and three field
stores, and two pointer advances per emitted record. Field addresses use
constant offsets 0,1,2. No tuple copying or array indexing hides a bulk operation.

Additionally allocate 128 operations to each merge's pointer/run-bound setup
and completion, and 256 to each pass's setup, base exchange, and width update.
There are n record emissions per pass, 128 passes, and
`n/2 + n/4 + ... + 1 = n-1` merges in total. Thus sorting costs at most

```text
128*128*n + 128*(n-1) + 256*128
< 192*128*n = 24576*n ordinary operations.
```

The expanded allowance on the right will be used in the total ledger.
Even an all-equal-digest batch fits the same worst-case bound.

### Scan, final verification, and termination

Scan at most `n-1` adjacent pairs, with at most 128 ordinary operations per
pair: load the two digests (with pointer loads/address formation), compare and
branch; if equal, load both x fields and both y fields, compare them and combine
the results; then advance the scan pointer and test its limit. The three word
comparisons and six field loads plus scalar/control traffic fit this budget.
This bound includes skipping arbitrarily many repeated identical inputs.

At most one pair triggers final verification. Charge two more selected
compressions. Allow 4096 ordinary operations for copying both retained pairs,
reconstructing and padding them, resetting IVs, hashing interface work,
packing/comparing full digests, checking distinctness, writing 96 output bytes,
and terminating. The per-sample interface budget applies twice; even emitting
individual output bytes by shifts/masks/stores fits the remainder. Failure
termination is included. No verification retry or restart is performed.

### Summation and claimed time

With H selected compressions and W other primitives, the preceding ledger yields

```text
H <= n + 2
W <= 48n + 2^20 + 512n + 24576n + 128n + 4096
  = 25264n + 2^20 + 4096
  < 32768n + 2^21.
T = H + W/2728
  <= n + 2 + (32768n + 2^21)/2728
  < 16n = 2^132.
```

For an integer-only check of the final inequality, multiply by 2728:
`2728 + 32768 = 35496 < 16*2728 = 43648`, and the remaining constant
`2*2728 + 2^21` is less than `8152n`. Thus `time_log2=132` is a conservative
upper bound, not just the birthday exponent or the number of hash invocations.
No failed work is conditioned away.

## Peak memory, code, and advice

The two arrays contain `6n` words in total, exactly `192n` bytes. Both are
counted at their simultaneous peak, including the spare half of every y word.
All retained randomness and every full message are already in these records.
No separate random tape or list of sampled inputs exists.

In addition reserve `2^20` bytes for all fixed storage. A loop-based program
implementing the displayed pseudocode, generation, comparison scan, and
verification needs fewer than 4096 fixed instructions. Even allowing four
256-bit words (128 bytes) per instruction uses at most `2^19` bytes. There is no
unrolling of n or run widths: a fixed counter iterates 128 times. Fixed
construction, initialization and merge bodies and their branches fit comfortably
within 4096 instructions; there are only the bounded bodies itemized above.
The selected compression is a priced primitive, but its public IV and round
constants are also included: fewer than 128 stored RAM words, or 4096 bytes.

Allow a further 4096 RAM words (`2^17` bytes) for working state: all scalar
pointers/counters, two random words, temporary padded block, sixteen-word input,
message schedule if materialized, chaining/working words, buffered records,
verification inputs/digests, and outputs. No recursion or growing call stack
is used. These explicit code/constants/working allowances together are less than
the reserved `2^20` bytes. Immutable public code is counted in memory even though
it is not nonuniform advice. Its initialization was conservatively paid above.

Consequently peak memory is at most `192n + 2^20 < 256n = 2^136` bytes, since
`2^20 < 64n`. All addresses fit within a 256-bit word even if byte addressing
is chosen. There is no external-memory capacity or time omitted from this RAM
bound. Physical feasibility at this size is not claimed.

Nonuniform advice has length zero: the program uses only public target constants
and fixed numerical parameters, with no target-specific collision, table, seed,
or search result. The schema cannot encode log2(0). Therefore
`nonuniform_advice_log2_bytes=0` denotes the valid upper bound of one byte,
which covers zero bytes; it does not hide an uncharged precomputed witness.

## Evidence, assumptions, and references

The essential finite-function theorem, target reduction, success calculation,
algorithm and implementation ledger are given above. `heuristics: []` is
intentional. The only randomness premise is the independent uniform-word
primitive explicitly provided by collision-frontier-v5, and both calls per
sample are charged. We make no claim about real PRNG independence, the balance
of concrete SHA-256, or experimental extrapolation.

The empty certificate manifest is deliberate: no full-size collision was found
or supplied. No experiment manifest is declared because no empirical premise
supports the argument. Mechanical checks and advisory review, if performed,
establish neither a collision witness nor official qualification.

Primary references consulted for definitions and context:

1. NIST, FIPS PUB 180-4, *Secure Hash Standard* (2015), sections 5.1.1, 5.2.1,
   5.3.3 and 6.2.2: standard padding, parsing, fixed IV and SHA-256 computation.
   https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf
   The selected profile changes only the compression round count as specified
   above; the 38-round target is not full-round FIPS SHA-256.
2. Mihir Bellare and Tadayoshi Kohno, *Hash Function Balance and its Impact on
   Birthday Attacks*, full version, May 2004, especially sections 2-4:
   https://homes.cs.washington.edu/~yoshi/papers/Hash/balance.pdf
   Their fixed-function formulation distinguishes genuine collisions from
   repetitions of an input and does not equate a concrete function with a
   random oracle. The explicit elementary-symmetric-polynomial bound and all
   target-specific numerical/resource bounds needed here are derived above;
   this package does not depend on the judge fetching or accepting an external
   theorem, a historical candidate, or a previous score.
