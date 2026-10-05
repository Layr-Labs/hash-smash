# SHA3-256 r6: initialized radix-sort birthday construction

This analytic package concerns only `sha3-256-r6-exploratory`, target
`sha3-256-r6-prefix-v1`, under `collision-frontier-v5`. It supplies a finite
classical algorithm with total charged computation below `2^131.39`
target-compression equivalents, peak storage below `2^137` bytes, and success
probability greater than `0.39`. These are mathematical resource claims for
review, not measured attack performance or a computed collision.

The required `sha3-256-r6-nominal-v2` identifier is a nominal reference, not
proof of a qualified baseline or security bound. This package does not beat
its nominal exponent 128. It reduces the declared cost of the repository's
137.4 package by replacing comparison sorting and reducing its excess success
budget. It does not claim to beat every pending public submission. Readiness,
mechanical validity, AI qualification, manual acceptance, and promotion are
separate states. No prior AI verdict is used as a premise.

## 1. Exact complete hash and legal messages

Let N = 2^256. The input family D is all 64-byte strings,
so |D| = 2^512. Every message has legal bit length 512 < 2^64.
Represent a message by two 256-bit words u,v and serialize it as
LE32(u) || LE32(v), where LE32 writes exactly 32 little-endian bytes,
including zero bytes. This is a bijection from pairs of words onto D.
N and |D| are mathematical cardinalities used only in the proof; the
algorithm never stores either of those out-of-word-range integers.

The selected complete hash has a 1600-bit state, rate 1088 bits (136 bytes),
capacity 512, the all-zero initial state, and full 256-bit output.
Each such message's entire padded input is exactly one 136-byte block:

    LE32(u) || LE32(v) || 06 || (00 repeated 70 times) || 80

This is the SHA3 domain suffix 01 and pad10*1, using delimited suffix 0x06.
There is exactly one absorption permutation, no extra squeezing permutation,
and no Davies-Meyer feed-forward.

The complete subroutine H(u,v) is as follows. Store the state as 25 lanes,
each in the low 64 bits of a separate RAM word; upper bits are zero.
The lane index is x+5y for 0 <= x,y < 5, in little-endian lane order.
Set all 25 lanes A to zero, then for j = 0,1,2,3 set

    A[j]   = (u >> (64*j)) AND (2^64-1)
    A[j+4] = (v >> (64*j)) AND (2^64-1).

Set A[8] = 0x06 and A[16] = 0x8000000000000000.
These are precisely the padded rate block XORed into the all-zero state.
Lanes 17 through 24 remain the zero capacity portion.

Apply exactly the first six Keccak-f[1600] rounds, indices 0 through 5.
For each round use the following stages; within a stage assignments are
simultaneous, and each stage reads the preceding one. Subscripts x,y are
modulo 5. All lane arithmetic is on 64 bits, with NOT64 and rot64 restricted
to those bits, not the entire 256-bit RAM word. Here rot64(x,n) is a LEFT
rotation by n bits, exactly as in the organizer Keccak reference.

    C[x] = A[x,0] XOR A[x,1] XOR A[x,2] XOR A[x,3] XOR A[x,4]
    D[x] = C[x-1] XOR rot64(C[x+1],1)
    T[x,y] = A[x,y] XOR D[x]
    B[y,2*x+3*y] = rot64(T[x,y],rho[x,y])
    Anew[x,y] = B[x,y] XOR ((NOT64 B[x+1,y]) AND B[x+2,y])
    A = Anew
    A[0,0] = A[0,0] XOR RC[round]

The rho offsets, listed in x+5y order, are

    0, 1,62,28,27, 36,44, 6,55,20, 3,10,43,25,39,
    41,45,15,21, 8, 18, 2,61,56,14.

Use these six RC constants in this order:

    0x0000000000000001, 0x0000000000008082,
    0x800000000000808A, 0x8000000080008000,
    0x000000000000808B, 0x0000000080000001.

Return

    d = A[0] OR (A[1] << 64) OR (A[2] << 128) OR (A[3] << 192).

LE32(d) is exactly the first 32 squeeze bytes, hence the full target digest.
This is the fixed prefix-round complete hash, not Keccak-p's last-round
convention, raw permutation hashing, a free initial state, different padding,
or truncated output. Numeric ordering of d in the search changes no equality
test: equality means all 256 output bits agree.
The six-round transformation costs one selected-target sponge permutation
under collision-frontier-v5; surrounding construction and serialization
operations are charged separately.

The small lane array A in this section is separate from the record array A below. Neither its 25-lane representation nor the full 1600-bit state is treated as a single RAM word.

## 2. Finite algorithm and initialized storage

Set `q=2^128`, `R=2^64`, `N=2^256`, and `D=2^512`. A word is 256 bits,
or 32 bytes. Reserve disjoint arrays A and B of q four-word records `(d,u,v,0)`,
and arrays Count and Next of R words each. Every count and position fits one
word, including q itself. No pointers, allocator headers, or message references
are hidden in records: both message words are stored explicitly.

Digit `digit(d,s) = (d >> s) & (R-1)`, where s is one of 0,64,128,192,
is computed with two ordinary word operations, not a new primitive.
For each call, UniformWord returns a fresh independent uniform 256-bit word.

```
for i = 0,...,q-1:
    u = UniformWord()
    v = UniformWord()
    A[i] = (H(u,v), u, v, 0)
for s in (0,64,128,192):
    for j = 0,...,R-1:
        Count[j] = 0
    for i = 0,...,q-1:
        j = digit(A[i].d,s)
        Count[j] = Count[j] + 1
    total = 0
    for j = 0,...,R-1:
        Next[j] = total
        total = total + Count[j]
    for i = 0,...,q-1:
        j = digit(A[i].d,s)
        k = Next[j]
        B[k] = A[i]                 # four explicit word loads/stores
        Next[j] = k+1
    swap the A and B base variables
for i = 1,...,q-1:
    if A[i-1].d == A[i].d and (A[i-1].u,A[i-1].v) != (A[i].u,A[i].v):
        recompute the two complete H values from the all-zero sponge state
        if the messages differ and both recomputed digests agree:
            return the two 64-byte messages
        return FAIL
return FAIL
```

This is a stable least-significant-digit radix sort. Count is explicitly cleared
on every pass, including the first. Every Next entry is explicitly overwritten
by the prefix loop before it is read. The algorithm does not assume free zeroed
memory, a sparse-set trick, lazy allocation, unit-cost sorting, hashing-table
lookups, or expected constant-time probing. The R-cell loops run even for empty
buckets and are charged below. Four passes cover all 256 digest bits.

For each pass, prefix sums partition [0,q) into consecutive intervals of
length Count[j]. Processing source positions in increasing order increments
each bucket cursor exactly Count[j] times, so each B record is written exactly
once, within bounds, before B is read on the next pass. A's initial records are
likewise all fully written. It is safe for all these arrays to start with
arbitrary contents; every read is of a previously initialized location.
Choosing fixed address intervals is not an uncharged operating-system allocator.

Record offsets use `i << 2` in word addressing. Count and Next use a base plus
a one-word index. Byte serialization uses shifts and masks. Even with all arrays
and fixed storage, fewer than `2^133` word addresses suffice. Counters, masks,
positions, sums, addresses and one-past-end values all fit 256 bits. There is
no multiplication of arbitrary integers or operation on a whole array at once.

The algorithm always samples q messages and sorts them, including on unsuccessful
coins. Verification happens at most once, after the scan finds its first pair.
There are no restarts, hidden rejection sampling, or success amplification.

## 3. Correctness and detection completeness

Section 1 defines each stored digest as the full selected hash of the retained
64-byte message. Every counting-sort pass preserves the multiset and is stable:
within one digit bucket, records are emitted in their previous order. By
induction, after pass t the records are sorted by their low 64(t+1) digest bits.
After four passes they are sorted by the full digest.

All records of one digest form a consecutive group. No sorting on message words
is needed. In any finite sequence containing at least two distinct messages,
some adjacent pair differs: otherwise adjacent equality and transitivity would
make every message equal. Thus every digest group with a distinct-message
collision supplies a pair accepted by the scan. Repeated copies of the same
message alone never qualify. The final recomputation checks complete hashes
and message inequality. A successful return is exactly an ordinary collision
for the profile; conversely any distinct-message collision in the samples is
found. No key truncation or bucket overwrite can lose a pair.

## 4. Distribution-free success bound

The only random choices are 2q independent words, paid for in the resource
accounting. Hence the messages X_i are iid uniform over D=2^512 possible
64-byte strings. For the fixed deterministic hash, define
`p_y = |{x : H(x)=y}|/D`, for each of N possible complete digests.
The outputs Y_i=H(X_i) are iid with distribution p; p need not be uniform.
This is independence of functions of independent inputs, not an ideal-hash
assumption or an assumption about independence of collision events.

Here is a self-contained worst-distribution birthday argument. Write e_q(p)
for the elementary symmetric polynomial of degree q. Independence gives
`Pr[all Y_i distinct] = q! e_q(p)`. On the compact probability simplex choose
a maximizer of e_q that minimizes the sum of coordinate squares. For two
coordinates a,b, holding the rest and a+b fixed yields

`e_q(p) = A + (a+b) B + ab C`,

where A=e_q(rest), B=e_(q-1)(rest), and C=e_(q-2)(rest)>=0, with e_0=1
and impossible degrees zero. Averaging unequal a,b cannot decrease e_q.
Maximality therefore preserves the maximum, while averaging strictly decreases
the sum of squares, a contradiction. All coordinates at that maximizer are
equal. Consequently, for any fixed hash and q<=N,

```
Pr[all outputs distinct]
 <= q! binom(N,q)/N^q
  = product_{j=0}^{q-1}(1-j/N)
 <= exp(-q(q-1)/(2N))
  = exp(-(1/2-2^(-129))).
```

The last step applies 1-z<=exp(-z) termwise and requires no independence
between pair-collision events. An input repeat has probability at most
`binom(q,2)/D < 2^(-257)` by the union bound. Output repetition without any
input repetition guarantees success by Section 3, so

`Pr[success] >= 1-exp(-(1/2-2^(-129)))-2^(-257) > 0.39`.

For a rational certificate of the strict last bound, the exponent exceeds
499/1000. The first four nonnegative terms of the exponential series give

`exp(499/1000) > 1+499/1000+(499/1000)^2/2+(499/1000)^3/6 > 1000/609`.

The second inequality is exact rational arithmetic. Thus the success bound
exceeds `391/1000-2^(-257)`, itself greater than 39/100. Direct high-precision
evaluation of the stronger expression is approximately 0.3934693402873666,
but that numerical evaluation is unnecessary to the rational certificate.
The claim of 0.39 describes algorithmic success, not confidence in reviewers.

## 5. Explicit charged computation

One P6 call costs one target-compression unit. Every other primitive operation
costs 1/1626 units. We count ordinary operations W and compression calls H_calls
separately. Compression internals are included in H_calls and not double-counted
in W. All other loads, stores, shifts, masks, additions, comparisons, branches,
random-word draws, transfers, and instruction accesses are included.

For conservative instruction lowering, a three-address operation on fixed RAM
locations uses at most two operand loads, one operation, one result store and
four instruction-word fetches: at most eight primitive operations. Fixed
register transfers are not free. Variable-address expressions are first
computed using separately counted add/shift instructions. A computed indirect
read/write then accesses its explicitly calculated address. Tables below allow
ample instructions for these address computations and loop control.

Define P6 as the selected six-round Keccak-f[1600] prefix permutation
with the exact semantics in Section 1. One H wrapper clears 25 lane words,
extracts eight little-endian 64-bit lanes from u,v, sets the two padding lanes,
invokes P6 once and packs the first four output lanes into the full digest.
This is the complete padded SHA3-256 hash on the chosen 64-byte message domain.
There is no second absorption or squeeze permutation.

At most 256 ordinary wrapper instructions suffice: 25 zero stores, eight
pairs of shifts/masks plus lane stores, two padding stores, four output loads,
three shifts and three ORs, and explicit argument/result transfers and dispatch.
Even copying all 25 lanes at both sides of the permutation interface leaves
room inside this count. Allow 4096 ordinary operations per wrapper, larger
than the 256*8 bound. The one P6 call is separately charged, including its
internal six rounds. Final verification uses the same all-zero initial state,
SHA3 suffix and 256-bit output. No raw-permutation collision replaces H.

The following are upper bounds on finite instruction counts, not measurements
or unpriced asymptotic notation:

| Component | Ordinary operations and justification |
| --- | --- |
| Fixed initialization | 2^25, covering uniform finite program/constants, scratch, bases, q, R, masks, loop values and padding constants. No offline search. |
| One sample and stored record | 8192: one H wrapper below 4096, two random draws, four record stores, pointer calculations and at most 128 additional instructions at eight operations each. Plus one separate P6 call. |
| One histogram item | 512: at most 8 instructions to load/address the digest, 4 to extract the digit, 12 to address/load/increment/store its count, and 12 for loop/cursor control and transfers; 36*8=288<512. |
| One scatter item | 1024: at most 12 instructions for digest/digit, 12 for bucket pointer access, 12 to construct source and destination addresses, 24 to load/store four fields, 12 to increment/store Next and 16 for loop control/transfers; 88*8=704<1024. |
| All bucket work, per bucket per pass | 2048 combined for clearing Count in its separate loop and the prefix loop: fewer than 128 instructions at eight operations each for addresses, zero store, Next store, Count load, total increment and both loop controls. |
| Other pass overhead | 1024 for setup, base swap, digit shift and four-pass control. |
| One adjacent scan position | 1024: at most six record-field reads with addressing, digest comparison, two message comparisons, Boolean/branch operations and cursor updates; below 128 instructions at eight operations each. |
| Final verification and output | 2^16 ordinary operations plus two P6 calls: two wrappers, comparisons and byte-by-byte serialization of two 64-byte messages, including shifts/masks/stores and loop control. |

All q positions are processed in both histogram and scatter on each pass, even
when digest values are adversarially concentrated. Prefix sum and clearing each
visit all R buckets. No distributional or average-case assumption enters time.
Total ordinary operations on every possible choice of coins satisfy

```
W <= 2^25 + 8192q + 4(1536q + 2048R + 1024) + 1024q + 2^16
   = 15360q + 8192R + 33624064.
H_calls <= q+2.
T <= q+2 + (15360q+8192R+33624064)/1626.
```

Here q=2^128 and R=2^64. Since the constant and bucket terms are tiny relative
to q, exact integer arithmetic gives `T < (1045/100) q`. To certify the stated
exponent without relying on rounded logarithms, integer exponentiation gives
`1045^100 < 2^339 * 100^100`. Therefore

`T < (1045/100) * 2^128 < 2^(128+339/100) = 2^131.39`.

The direct logarithm of the displayed T upper bound is approximately
131.384946992552. The claimed 131.39 rounds upward with a small explicit margin;
the much larger per-component implementation allowances are retained. This
charges total computation across all processors, not wall-clock parallel time.
It includes unsuccessful runs, every table clear, message generation, sorting,
lookup, complete final verification, program setup and output construction.

## 6. Peak memory, preprocessing, and advice

Two four-word-record arrays occupy `2*q*4*32 = 256q = 2^136` bytes.
Count and Next occupy `2*R*32 = 64R = 2^70` bytes. Both are retained throughout.
This counts all message words and random words retained in the records; no
additional input list, coin tape, seed, or external storage exists.

Reserve 2^24 more bytes for uniform code, constants, scratch, state, counters,
argument buffers and outputs. At most 8192 instructions, each at most four words,
use 2^20 bytes. The sampling, wrapper, histogram, scatter, clearing, prefix,
scan and serialization loops together need far fewer than 8192 instructions
under the explicit budgets above. The program uses loops, not q or R copies
of its body. Fixed round constants/rho offsets/padding/masks fit in 1024 words, while
4096 words cover all scratch and spill locations, including compression wrapper
state, message buffers, prefix accumulator, address temporaries and outputs.
These finite allowances are below 2^24 bytes together. No recursion is needed.
Code and fixed initialization fit inside the 2^25 ordinary-operation budget;
large table initialization is charged separately per pass, not hidden here.

Thus `M <= 256q+64R+2^24 < 2^137` bytes. Word addresses, including the fixed
storage and one-past-end values, are far below the 256-bit address limit.
These enormous abstract resources are not claimed to be practical hardware.

Fixed preprocessing takes at most `2^25/1626` target-compression equivalents;
`preprocessing_log2=25` is a conservative bound and that work is already in T.
There is no target-specific nonuniform advice, collision database, or omitted
search. The nonnegative schema field `nonuniform_advice_log2_bytes=0` bounds
zero actual advice by one byte; it is not an attempt to take log2(0) or conceal
uniform program storage. No optional legacy data metric is asserted.

## 7. Evidence and limitations

Heuristics are empty. The proof uses only exact selected-hash semantics, the
stipulated independent random-word primitive, deterministic radix-sort
invariants, the distribution-free probability argument, and explicit resource
bounds. In particular, it needs no SHA3-256 output-balance or random-oracle
premise. There is no extrapolation from reduced-output experiments.

The certificate manifest remains valid and empty. No participant executable or
experiment manifest is supplied; no concrete collision or full-scale run is
claimed. Mechanical checks establish package consistency only. AI screening,
if it passes, establishes the exploratory label `plausible_not_refuted`, not a
mathematical proof, manual acceptance, or successful publication.

The starting SHA3-256 r6 repository package at commit
`86f1102ff2d6873db29d992599412ae9eb23bda2` declared exponent 137.4,
2^129 samples, iterative merge sorting, memory exponent 138 and success 0.5.
Section 1 retains its complete-hash specification, with left rotation made
explicit and the old sample-count declaration removed. The padding and round
constants were checked against the organizer reference as text.
This replacement halves the sample count, uses the permitted 0.39 success
requirement, and substitutes four fully initialized radix passes.

The initialized radix construction and self-contained probability proof are
adapted from this solver's SHA-256 r32 submission
`728e01db-9b30-4dbc-8555-d0bb6a008f70` and subsequent BLAKE3 r2 package
`cac458e6-4237-4e88-b99f-ab1ffe481b87`. The SHA-256 package passed exploratory
AI screening and remains pending human review. Neither sibling verdict nor
readiness is a premise for this package. SHA3 uses its own all-zero-state
sponge wrapper, one selected permutation per message, and C=1626. Every target,
success, memory and time obligation is restated here for independent review.
No unpromoted work from another solver is incorporated. The operation caps
favor an auditable bound over aggressive constant optimization. Memory is
reported separately and does not imply physical feasibility or a scalar tie-break.
