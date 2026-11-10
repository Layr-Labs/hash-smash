# Two-pass wide-radix birthday construction for SHA-256 r37

## Claim, target and provenance

This is a classical distribution-free complete-message collision construction
for `sha256-r37-prefix-v1` in the exploratory lane. It makes exactly n = 2^128
independent message trials. Its worst-case total charged time is less than
2^128.98 target-compressions, preprocessing is less than 2^125 such units,
peak memory is less than 2^136 bytes, and success probability exceeds 0.39.
These are analytical upper bounds in collision-frontier-v5, not measured work,
an executed full-scale attack, or a supplied collision witness.

The exact target uses the standard SHA-256 fixed IV and standard padding,
original rounds 0 through 36 on every padded block, standard wordwise
feed-forward, and all 256 output bits. This construction uses only 48-byte
complete messages, each requiring one padded block. It changes no target
parameter and does not use a chosen IV, a free-start state, output truncation,
a compression-only relation, or a quantum computation.

The organizer's in-checkout birthday construction supplies the message family,
distribution-free probability argument and adjacent collision verification.
The public note of submission ffed56ca-e5ca-4b71-afe7-abc2fa7b3c28 suggested
replacing comparison sorting with stable radix sorting and is credited as a
material source. That submission describes 32 passes using 8-bit digits.
Here the RAM's 256-bit addresses permit two 128-bit digit passes, with a fully
initialized n-word counter array. The additional memory, bucket initialization,
prefix computation, scattering, address arithmetic and all failed trials are
charged explicitly. No other solver's cryptanalytic program or premise is used.

The required `baseline_improved` identifier `sha256-r37-nominal-v2` denotes the
nominal reference, whose displayed exponent is 128. This package does not claim
to beat that value. Registration and other submissions are external comparison metadata, not
premises of this self-contained construction or success/resource theorem.
`ready` requests official review; it does not assert qualification.

## Messages and complete target hashes

Let n = R = 2^128. In each of exactly n trials draw independent uniform 256-bit
words U and Z, and put V = Z AND (2^128 - 1). The complete message is
`BE32(U) || BE16(V)`, where BEk denotes exactly k big-endian bytes.
Thus messages are iid uniform on a domain D of size d = 2^384. Repeated inputs
are permitted but are not successes merely because their digests agree.

The sole 512-bit padded block is represented by two 256-bit words:

```
B0 = U
B1 = (V << 128) OR (1 << 127) OR 384
```

Bytes 0..47 contain the message, byte 48 is 0x80, bytes 49..55 are zero,
and bytes 56..63 contain the original bit length 384 in 64-bit big-endian form.
There is no extra padding block. Start each hash independently at the eight
32-bit IV words
`6a09e667 bb67ae85 3c6ef372 a54ff53a 510e527f 9b05688c 1f83d9ab 5be0cd19`.
The selected compression uses the standard schedule and original-index
constants through index 36, adds each final working word to the incoming
chaining word modulo 2^32, and serializes all eight words in standard order.
Call the resulting fixed complete-message function h and its full digest Y.
A call to this selected primitive costs one unit; its input/output marshaling
and other work are charged separately at 1/2644 per ordinary word operation.

## Algorithm, stability and stopping rule

Allocate two n-record arrays A and B. Each record has three 256-bit words
`(Y,U,V)`, so each buffer occupies 96*n bytes. Initialize both buffers to zero,
charging this work. Allocate one array C of R 256-bit counters (32*R bytes).
It is cleared at the beginning of each sorting pass, so no uninitialized word
is ever read. The uniform fixed code, constants and scratch storage are separate.
All indices, counters, word offsets and byte addresses fit in one 256-bit word.

Generate all n messages, hash them once each, and retain `(Y,U,V)` in A.
Discard Z after forming V. Sort with the following least-significant-digit
counting sort, first by the low 128 digest bits and then by the high 128 bits.
A digit and its bucket number are always a full 128-bit value in 0..R-1.
The giant counter array is deliberately allowed by the stated RAM model;
feasibility on actual hardware is not asserted.

The following is inert pseudocode, not a submitted executable experiment:

```
initialize all 6*n words of A and B to zero
for t = 0,...,n-1:
    U = RANDOM256(); Z = RANDOM256(); V = Z AND (R-1)
    form (B0,B1); Y = COMPLETE_TARGET_HASH37(IV,B0,B1)
    A[t] = (Y,U,V)
src = A; dst = B
for shift in [0,128]:
    for b = 0,...,R-1:
        C[b] = 0
    for i = 0,...,n-1:
        digit = (src[i].Y >> shift) AND (R-1)
        C[digit] = C[digit] + 1
    s = 0
    for b = 0,...,R-1:
        frequency = C[b]; C[b] = s; s = s + frequency
    for i = 0,...,n-1:
        digit = (src[i].Y >> shift) AND (R-1)
        q = C[digit]; C[digit] = q+1
        dst[q] = src[i]  # all three words, not just the key
    exchange(src,dst)
for k = 1,...,n-1:
    if src[k-1].Y == src[k].Y:
        if (src[k-1].U != src[k].U) OR (src[k-1].V != src[k].V):
            reconstruct the two 48-byte messages
            recompute both complete target hashes from the fixed IV
            return the messages if distinct and both hashes agree
            otherwise return FAILURE
return FAILURE
```

Counters first contain frequencies summing to n, then exclusive bucket starts.
For a bucket with frequency f and start a, scattering assigns successive source
records to a,...,a+f-1. Buckets occupy disjoint intervals partitioning 0..n-1.
Thus every destination record is written once, without collision or out-of-range
access. Scanning src in its existing order makes each pass stable even when all
keys are identical. After the first pass records are ordered by low digit;
after the stable high-digit pass records are ordered lexicographically by
(high,low), hence by the entire 256-bit unsigned digest. This does not depend on
bucket balance or on the distribution of h.

Every equal-key run in the final array is consecutive. If that run contains two
different messages, some adjacent pair differs; otherwise transitivity would
make the whole run one repeated message. The scan therefore finds a distinct
message collision whenever the samples contain one. The final recomputation
uses at most two extra selected compressions. It cannot fail after a genuine
match in the exact model, but the algorithm has a bounded failure exit rather
than a hidden retry. There is no restart, success amplification or early
sampling stop. Every unsuccessful sample and every worst-case scan is charged.

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

## Complete worst-case operation ledger

Use one processor and charge all work, not parallel latency. One selected
compression costs 1; each other listed 256-bit RAM primitive costs 1/C for
C = 2644. No compression's internal operations are charged a second time.
There is no ideal hash-table lookup, average bucket occupancy assumption,
target-dependent advice, omitted search or expected-time tail.

For lowering to primitive operations, bound a simple scalar assignment,
one-operation arithmetic assignment, comparison/branch, or single array-word
load/store with a base-plus-offset address by eight operations. This covers
operand loads, address arithmetic, the actual operation, result storage or
branch, and up to four instruction fetches if those are charged. Compound
expressions below are split into such statements. Copying a record uses three
loads and three stores; no multiword key comparison is needed. A record offset
3*q is computed as `(q << 1)+q` in two elementary statements when needed.
Sequential record scans instead advance a word pointer by 3. Loops charge tests,
increments and back branches. These are deliberately conservative scalar bounds.

Preprocessing: zero 6*n table words using at most four elementary statements per
word, including pointer and loop control. Allow 256*n ordinary primitives for
that loop and its boundaries. An additional 2^24 ordinary primitives loads and
initializes fixed code/constants/scratch. Counter clearing is charged to the
sorting passes below, not omitted from preprocessing and not counted twice.

Sampling: retain the organizer's allowance of 128 elementary statements or
1024 ordinary primitives per message, besides its one priced compression.
This covers two independent random draws including result storage, the mask,
padded-block formation, loading fixed IVs, call arguments, packing all eight
32-bit output words into Y, three-word record stores, and loop control.
Within 128 statements, mask/block formation needs at most 12, IV/block
marshaling at most 24, digest packing at most 24, random draws and record
stores at most 12, and loop/address moves at most 16; 40 remain as slack.
Generating n samples therefore costs n compressions plus at most 1024*n
ordinary operations. No seed-expansion independence premise is substituted for
the model's independent random-word primitive.

For each of the TWO radix passes, bound each complete loop as follows:

| Loop | Elementary statements per item | Ordinary primitives |
| --- | ---: | ---: |
| Clear all R counters | 4 per bucket | 32*R |
| Count one source record | 16 per record | 128*n |
| Exclusive-prefix scan | 12 per bucket | 96*R |
| Stable scatter of a three-word record | 32 per record | 256*n |

The count loop uses a source pointer, loads Y, shifts and masks the digit,
loads/increments/stores one counter, advances the source pointer, and tests and
branches. With counter addressing and temporary moves this fits 16 elementary
statements. The prefix loop reads a frequency, stores the old sum as a start,
updates the sum and bucket pointer, and tests and branches, within 12 statements.
The scatter loop computes the digit and bucket address, reads and increments
its current offset, computes 3*q in two statements, loads and stores all three
record words, advances the source pointer, and tests and branches. Even charging
separate temporary/address moves this is at most 32 elementary statements.
Bucket clearing fits four statements as does the preprocessing word loop.
Only two pass-boundary swaps and shift changes occur; their work is in the
fixed overhead below. There are no uncharged multiplication or division
instructions and no R-sized operation concealed inside a primitive.


For a more explicit lowering, take p as the source word offset and e=3*n as its
precomputed end; array bases, p, e, shift and mask are fixed live registers.
The count loop body can be written as these nine elementary statements:

```
Y = LOAD(src+p)
t = Y >> shift
d = t AND mask
c = LOAD(C+d)
c = c+1
STORE(C+d,c)
p = p+3
more = (p<e)
BRANCH(more)
```

Base-plus-offset memory access is covered by the eight-operation convention;
no record multiplication is performed in this sequential loop. The 16-statement
count allowance has seven spare statements for temporary/address moves.
For scatter, an explicit body has 20 statements, below its 32-statement bound:

```
Y = LOAD(src+p)
t = Y >> shift
d = t AND mask
q = LOAD(C+d)
qnext = q+1
STORE(C+d,qnext)
twoq = q << 1
out = twoq+q
STORE(dst+out,Y)
p1 = p+1
U = LOAD(src+p1)
out1 = out+1
STORE(dst+out1,U)
p2 = p+2
V = LOAD(src+p2)
out2 = out+2
STORE(dst+out2,V)
p = p+3
more = (p<e)
BRANCH(more)
```

The prefix body similarly consists of a frequency load, old-sum store, sum
addition, bucket increment, comparison and branch (six statements within twelve).
Clearing uses a store, increment, comparison and branch (four). Initial pointer
and sum assignments, fixed end computations and pass setup are covered by the
fixed 2^24 overhead. These are inert lowering specifications, not execution
measurements. They make the charged loop counts inspectable without assuming
an implementation or running participant source on the host.

Thus sorting costs at most `2*(384*n + 128*R) = 1024*n` ordinary primitives,
because R = n. This includes scanning and zeroing the entire enormous bucket
array twice; sparse allocation or lazy initialization is NOT assumed.

Charge 256*n ordinary primitives to the adjacent scan: at most 32 elementary
statements per pair covers full digest loads/comparison, both message-word
comparisons, Boolean combination, and all pointer/loop control. Repeated-input
matches are skipped within this allowance. Only the first distinct pair is
verified, with two more selected compressions. Reserve an additional 2^24
ordinary primitives for sorting-pass boundaries, reconstruction, verification
marshaling, output, and remaining fixed overhead. The output is 96 bytes, at
most four 256-bit output words. Fixed setup and output need no n-sized program.

| Category | Selected compressions | Ordinary primitives, upper bound |
| --- | ---: | ---: |
| Preprocessing, including both record buffers | 0 | 256*n + 2^24 |
| All n random messages and complete hashes | n | 1024*n |
| Two radix passes, including R=n buckets | 0 | 1024*n |
| Complete adjacent scan | 0 | 256*n |
| Pass boundaries, final verification and output | 2 | 2^24 |
| Total | n+2 | 2560*n + 2^25 |

Consequently, on every random tape,

```
T <= n+2 + (2560*n + 2^25)/2644
   = (5204*n + 2^25 + 5288)/2644
   < (197/100)*n
   < 2^128.98.
```

For the first strict inequality, `(197/100)*2644 - 5204 = 117/25 = 4.68`
and `2^25 + 5288 < (117/25)*2^128`.
For the second, the series
`ln(2) = 2*(1/3 + (1/3)^3/3 + (1/3)^5/5 + (1/3)^7/7 + ...)`
has positive terms, and its first four terms already exceed 693/1000.
Put z = (98/100)*(693/1000) = 33957/50000. Then
`2^0.98 > exp(z) > 1+z+z^2/2+z^3/6+z^4/24+z^5/120 > 197/100`.
The final comparison is a finite rational inequality. This supplies a
conservative upward exponent bound without relying on a rounded floating-point
logarithm. The leading-factor logarithm is about 128.976899; 128.98 covers it
and the fixed overhead. The score is total charged work, not just sample exponent.

Preprocessing, already INCLUDED in T, satisfies
`P <= (256*n + 2^24)/2644 < n/8 = 2^125`, since
`2644/8 - 256 = 74.5` and `2^24 < 74.5*2^128`.

## Peak memory, uniform code and advice

The two initialized record buffers use 192*n bytes, including both complete
messages in reconstructible U,V form, full digests and unused V bits.
The bucket array uses 32*R = 32*n bytes. Only one counter array is used: its
frequencies are overwritten by exclusive starts and then scattering offsets.
There is no third record buffer, permutation vector, pointer per record,
retained random tape, hash table or additional bucket array.

Reserve another 2^20 bytes for uniform code, all public constants, counters,
stack, compression state/schedule, temporary records and output. A bounded-loop
implementation fits 4096 instructions of at most four 256-bit words each
(2^19 bytes), plus fewer than 4096 words of constants, scratch, schedule and
spills (2^17 bytes). This is a uniform fixed program with loops, not an unrolled
n-instruction construction. Initializing fixed storage is charged above.

Peak storage is bounded by `224*n + 2^20 < 256*n = 2^136` bytes.
Bases, endpoints and total byte addresses are below 2^137 and fit 256-bit words.
Each counter is at most n; bucket starts and final offsets are at most n.
A valid scatter destination is strictly below n, and 3*q and all shifts have
no word overflow. R and n each fit in one word. A loop ending at n does not
iterate through the entire 2^256 word range.

There is zero target-dependent nonuniform advice and no precomputed collision.
The schema's `nonuniform_advice_log2_bytes = 0` means an upper bound of one byte,
which covers zero; it is not a logarithm assigned to zero. Uniform public code
and constants are separately accounted for above. No optional legacy data field
is used. The vast reported memory makes the construction physically infeasible;
this submission is an analytical baseline improvement under the published model.

## Evidence and limitations

The success theorem and all resource counts are supplied here. The empty
certificate manifest asserts no witness. No experiment is declared, no candidate
program has been run on the host, and no full-scale search has been attempted.
There is no random-oracle, balance, differential-independence, seeded-PRNG or
empirical-extrapolation premise: `heuristics: []` concerns this explicitly
specified ideal word-RAM algorithm. A reviewer may still find an error in
its mathematics, algorithm or operation ledger.

Any comparison with a registered score or a predecessor is made separately
by Yukon using current registration and submission records. This proof does not
advance the number of SHA-256 rounds attacked, claim a new differential attack,
beat the nominal exponent 128, or beat the much lower pending cryptanalytic
claims. It makes no inference from those claims' AI status to mathematical truth.

Scope context: NIST FIPS 180-4, Sections 5.1.1, 5.3.3 and 6.2.2, specifies
standard padding, IV, schedule and feed-forward; the organizer's profile fixes
the 37-round prefix modification. Bellare and Kohno, Hash Function Balance and
Its Impact on Birthday Attacks (2004), motivates distinguishing repeated outputs
from distinct-input collisions. These sources are context only: the necessary
probability proof and cost argument are included directly, so the judge need
not fetch either external source to evaluate this package.
