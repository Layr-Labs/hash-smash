# SHA-256 r32: initialized radix-sort birthday construction

This analytic package concerns only `sha256-r32-exploratory`, target
`sha256-r32-prefix-v1`, under `collision-frontier-v5`. It supplies a finite
classical algorithm with total charged computation below `2^131.16`
target-compression equivalents, peak storage below `2^137` bytes, and success
probability greater than `0.39`. These are mathematical resource claims for
review, not measured attack performance or a computed collision.

The required `sha256-r32-nominal-v2` identifier is a nominal reference, not
proof of a qualified baseline or security bound. This package does not beat
its nominal exponent 128. It reduces the declared cost of the repository's
136 package by replacing comparison sorting and reducing its excess success
budget. It does not claim to beat every pending public submission. Readiness,
mechanical validity, AI qualification, manual acceptance, and promotion are
separate states. No prior AI verdict is used as a premise.

## 1. Exact complete-message target

The attack uses only messages of exactly 64 bytes, a subset of the profile's
finite-byte-string domain with bit length less than `2^64`. Write each message
as `BE256(u) || BE256(v)`, where each of `u,v` is a 256-bit unsigned integer and
`BE256` means exactly 32 bytes, most significant byte first, including zeros.
This encoding is injective. The message is padded to two 64-byte blocks:

- `B0 = BE256(u) || BE256(v)`.
- `B1 = 0x80 || 55 zero bytes || BE64(512)`.

The eight-word initial state, in the order used throughout, is
`(6a09e667, bb67ae85, 3c6ef372, a54ff53a, 510e527f, 9b05688c, 1f83d9ab, 5be0cd19)`.
Hexadecimal words here have 32 bits. Initialize this fixed IV once, process B0
and then B1, and retain the second block's complete feed-forward state.

For completeness the selected compression `C32(S,B)` is specified here.
All working words have 32 bits; additions and complements are modulo `2^32`.
`R_n(x)` is right rotation by n within 32 bits and `x >> n` is logical shift.
Parse B into sixteen big-endian 32-bit words `W[0],...,W[15]`. For `t=16,...,31`,
set

```
sigma0(x) = R_7(x) xor R_18(x) xor (x >> 3)
sigma1(x) = R_17(x) xor R_19(x) xor (x >> 10)
W[t] = W[t-16] + sigma0(W[t-15]) + W[t-7] + sigma1(W[t-2])
Sigma0(x) = R_2(x) xor R_13(x) xor R_22(x)
Sigma1(x) = R_6(x) xor R_11(x) xor R_25(x)
Ch(x,y,z) = (x and y) xor ((not x) and z)
Maj(x,y,z) = (x and y) xor (x and z) xor (y and z)
```

The constants K[t], with original indices 0 through 31, are:

```
428a2f98 71374491 b5c0fbcf e9b5dba5 3956c25b 59f111f1 923f82a4 ab1c5ed5
d807aa98 12835b01 243185be 550c7dc3 72be5d74 80deb1fe 9bdc06a7 c19bf174
e49b69c1 efbe4786 0fc19dc6 240ca1cc 2de92c6f 4a7484aa 5cb0a9dc 76f988da
983e5152 a831c66d b00327c8 bf597fc7 c6e00bf3 d5a79147 06ca6351 14292967
```

Set `(a,b,c,d,e,f,g,h)=S`. For `t=0,...,31`, using the old values on the
right-hand side, do

```
T1 = h + Sigma1(e) + Ch(e,f,g) + K[t] + W[t]
T2 = Sigma0(a) + Maj(a,b,c)
(a,b,c,d,e,f,g,h) = (T1+T2, a, b, c, d+T1, e, f, g)
```

Return `S+(a,b,c,d,e,f,g,h)` componentwise modulo `2^32`. In particular,
feed-forward uses the incoming state of each block; it is never omitted.
Define `H(u,v)` as the concatenation, in state order and big-endian encoding,
of all eight words of `C32(C32(IV,B0),B1)`. This is the full 256-bit digest.
Thus H is exactly the fixed-IV, first-32-round, padded complete hash required
by this profile. There is no selected IV, suffix-round convention, compression-
only substitute, changed padding, or digest truncation in this construction.

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
        recompute the two complete H values from the fixed IV
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

One C32 call costs one target-compression unit. Every other primitive operation
costs 1/2224 units. We count ordinary operations W and compression calls H_calls
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

One H wrapper initializes the eight standard IV words, prepares the two message
words and two fixed padding words, invokes C32 twice, and packs eight output
words into one digest. At most 256 ordinary instructions suffice for the wrapper
including field extraction into narrow input words if required: each of the 32
input fields needs at most two shifts/masks, and output packing takes at most
seven shifts and seven ORs. Allow 4096 ordinary operations per wrapper, larger
than the 256*8 bound. The two C32 calls remain separately charged. This uses
exactly the same two-block complete-hash construction as Section 1.

The following are upper bounds on finite instruction counts, not measurements
or unpriced asymptotic notation:

| Component | Ordinary operations and justification |
| --- | --- |
| Fixed initialization | 2^25, covering uniform finite program/constants, scratch, bases, q, R, masks, loop values and padding. No offline search. |
| One sample and stored record | 8192: one H wrapper below 4096, two random draws, four record stores, pointer calculations and at most 128 additional instructions at eight operations each. Plus two separate C32 calls. |
| One histogram item | 512: at most 8 instructions to load/address the digest, 4 to extract the digit, 12 to address/load/increment/store its count, and 12 for loop/cursor control and transfers; 36*8=288<512. |
| One scatter item | 1024: at most 12 instructions for digest/digit, 12 for bucket pointer access, 12 to construct source and destination addresses, 24 to load/store four fields, 12 to increment/store Next and 16 for loop control/transfers; 88*8=704<1024. |
| All bucket work, per bucket per pass | 2048 combined for clearing Count in its separate loop and the prefix loop: fewer than 128 instructions at eight operations each for addresses, zero store, Next store, Count load, total increment and both loop controls. |
| Other pass overhead | 1024 for setup, base swap, digit shift and four-pass control. |
| One adjacent scan position | 1024: at most six record-field reads with addressing, digest comparison, two message comparisons, Boolean/branch operations and cursor updates; below 128 instructions at eight operations each. |
| Final verification and output | 2^16 ordinary operations plus four C32 calls: two wrappers, comparisons and byte-by-byte serialization of two 64-byte messages, including shifts/masks/stores and loop control. |

All q positions are processed in both histogram and scatter on each pass, even
when digest values are adversarially concentrated. Prefix sum and clearing each
visit all R buckets. No distributional or average-case assumption enters time.
Total ordinary operations on every possible choice of coins satisfy

```
W <= 2^25 + 8192q + 4(1536q + 2048R + 1024) + 1024q + 2^16
   = 15360q + 8192R + 33624064.
H_calls <= 2q+4.
T <= 2q+4 + (15360q+8192R+33624064)/2224.
```

Here q=2^128 and R=2^64. Since the constant and bucket terms are tiny relative
to q, exact integer arithmetic gives `T < (891/100) q`. To certify the stated
exponent without relying on rounded logarithms, integer exponentiation gives
`891^25 < 2^79 * 100^25`. Therefore

`T < (891/100) * 2^128 < 2^(128+79/25) = 2^131.16`.

The direct logarithm of the displayed T upper bound is approximately
131.154854526491. The claimed 131.16 rounds upward with a small explicit margin;
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
of its body. Fixed round constants/IV/padding/masks fit in 1024 words, while
4096 words cover all scratch and spill locations, including compression wrapper
state, message buffers, prefix accumulator, address temporaries and outputs.
These finite allowances are below 2^24 bytes together. No recursion is needed.
Code and fixed initialization fit inside the 2^25 ordinary-operation budget;
large table initialization is charged separately per pass, not hidden here.

Thus `M <= 256q+64R+2^24 < 2^137` bytes. Word addresses, including the fixed
storage and one-past-end values, are far below the 256-bit address limit.
These enormous abstract resources are not claimed to be practical hardware.

Fixed preprocessing takes at most `2^25/2224` target-compression equivalents;
`preprocessing_log2=25` is a conservative bound and that work is already in T.
There is no target-specific nonuniform advice, collision database, or omitted
search. The nonnegative schema field `nonuniform_advice_log2_bytes=0` bounds
zero actual advice by one byte; it is not an attempt to take log2(0) or conceal
uniform program storage. No optional legacy data metric is asserted.

## 7. Evidence and limitations

Heuristics are empty. The proof uses only exact selected-hash semantics, the
stipulated independent random-word primitive, deterministic radix-sort
invariants, the distribution-free probability argument, and explicit resource
bounds. In particular, it needs no SHA-256 output-balance or random-oracle
premise. There is no extrapolation from reduced-output experiments.

The certificate manifest remains valid and empty. No participant executable or
experiment manifest is supplied; no concrete collision or full-scale run is
claimed. Mechanical checks establish package consistency only. AI screening,
if it passes, establishes the exploratory label `plausible_not_refuted`, not a
mathematical proof, manual acceptance, or successful publication.

The starting repository package at commit
`86f1102ff2d6873db29d992599412ae9eb23bda2` declared exponent 136, q=2^129,
lexicographic comparison sorting and success 0.8. Its complete-hash definition
and distribution-free birthday argument are reused with their obligations
rechecked here. This replacement halves the sample count, uses the permitted
0.39 success requirement, and substitutes four fully initialized radix passes.
It does not inherit any previous qualification. The operation caps deliberately
favor an auditable bound over aggressive constant optimization. Memory remains
a reported resource and is not a claim of practical feasibility or a tie-break.
