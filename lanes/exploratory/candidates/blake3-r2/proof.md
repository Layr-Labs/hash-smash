# BLAKE3 r2: initialized radix-sort birthday construction

This analytic package concerns only `blake3-r2-exploratory`, target
`blake3-r2-prefix-v1`, under `collision-frontier-v5`. It supplies a finite
classical algorithm with total charged computation below `2^133.20`
target-compression equivalents, peak storage below `2^137` bytes, and success
probability greater than `0.39`. These are mathematical resource claims for
review, not measured attack performance or a computed collision.

The required `blake3-r2-nominal-v2` identifier is a nominal reference, not
proof of a qualified baseline or security bound. This package does not beat
its nominal exponent 128. It reduces the declared cost of the repository's
140 package by replacing comparison sorting and reducing its excess success
budget. It does not claim to beat every pending public submission. Readiness,
mechanical validity, AI qualification, manual acceptance, and promotion are
separate states. No prior AI verdict is used as a premise.

## 1. Exact complete hash

Each message is exactly 64 bytes, of bit length 512 < 2^64. Two 256-bit words
u,v encode m=LE32(u)||LE32(v), where LE32 includes all 32 little-endian bytes,
including zeros. These encodings bijectively cover a domain D of size 2^512.
There is no unknown IV, free-start state, or supplied prefix/advice.

H is unkeyed BLAKE3-256 with 2 prefix rounds in every compression.
On these exactly 64-byte messages there is one chunk, one full block, no parent,
and exactly one compression with CHUNK_START | CHUNK_END | ROOT = 11.
There is no extra padding block, key, or derivation flag. The true block length
is 64 and both the chunk index and root-output counter are zero.

Decode m into sixteen little-endian 32-bit words w[0..15]. The eight-word IV is

    6a09e667 bb67ae85 3c6ef372 a54ff53a
    510e527f 9b05688c 1f83d9ab 5be0cd19.

Initialize v[0..7]=IV, v[8..11]=IV[0..3], and
v[12..15]=(0,0,64,11). All arithmetic additions below are modulo 2^32;
ROR rotates right within a 32-bit lane. Define G(a,b,c,d,x,y) on v by

    v[a] = v[a]+v[b]+x; v[d] = ROR(v[d] XOR v[a],16)
    v[c] = v[c]+v[d];   v[b] = ROR(v[b] XOR v[c],12)
    v[a] = v[a]+v[b]+y; v[d] = ROR(v[d] XOR v[a],8)
    v[c] = v[c]+v[d];   v[b] = ROR(v[b] XOR v[c],7).

For each round, use the current message schedule s, initially w, and call

    G(0,4,8,12,s[0],s[1]);    G(1,5,9,13,s[2],s[3])
    G(2,6,10,14,s[4],s[5]);   G(3,7,11,15,s[6],s[7])
    G(0,5,10,15,s[8],s[9]);   G(1,6,11,12,s[10],s[11])
    G(2,7,8,13,s[12],s[13]);  G(3,4,9,14,s[14],s[15]).

Between rounds replace s by s[P[i]], where
P=(2,6,3,10,7,0,4,13,1,11,12,5,9,14,15,8).
Execute exactly the first 2 rounds, with no later rounds. The full
compression output is o[i]=v[i] XOR v[i+8], and
o[i+8]=v[i+8] XOR IV[i], for i=0..7. The digest H(m) is
LE4(o[0]) || ... || LE4(o[7]), the first 32 root-output bytes.
This retains the ordinary hash's flags and feed-forward, rather than searching
for a collision of a free-start or non-root compression function.

The target profile permits other message lengths and preserves the complete
standard 1024-byte chunk tree, parent nodes, counters and root output, with the
same prefix reduction in every compression. This algorithm only generates
64-byte messages, so the one-root-compression description covers every hash
it evaluates, including final verification. No uncharged parent, chunk or
second root-output compression is needed on this domain.

For the algorithm below, H(u,v) denotes this complete hash of LE32(u)||LE32(v), interpreted as one unsigned little-endian 256-bit digest word. This integer encoding preserves equality of all output bits.

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

One B2 call costs one target-compression unit. Every other primitive operation
costs 1/430 units. We count ordinary operations W and compression calls H_calls
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

Define B2 as the selected two-round BLAKE3 compression primitive with the
complete semantics in Section 1. One H wrapper loads the standard eight-word IV,
unpacks u,v into sixteen little-endian 32-bit words, supplies counter 0,
block length 64 and flags 11, invokes B2 once, and packs the first eight output
words little-endian into one digest word. This is the complete unkeyed hash on
this message domain. There is no extra chunk-finalization, parent, or root call.

At most 256 ordinary wrapper instructions suffice, including extraction into
narrow input words if needed: each of sixteen fields uses a shift and mask,
and output packing takes at most seven shifts and seven ORs. Initialization,
argument/result transfers and dispatch fit in the remaining instructions.
Allow 4096 ordinary operations per wrapper, larger than the 256*8 bound. The
one B2 call is separately charged, including its internal two rounds and output
XORs. True block length and flags are supplied unchanged at final verification.

The following are upper bounds on finite instruction counts, not measurements
or unpriced asymptotic notation:

| Component | Ordinary operations and justification |
| --- | --- |
| Fixed initialization | 2^25, covering uniform finite program/constants, scratch, bases, q, R, masks, loop values and root flags. No offline search. |
| One sample and stored record | 8192: one H wrapper below 4096, two random draws, four record stores, pointer calculations and at most 128 additional instructions at eight operations each. Plus one separate B2 call. |
| One histogram item | 512: at most 8 instructions to load/address the digest, 4 to extract the digit, 12 to address/load/increment/store its count, and 12 for loop/cursor control and transfers; 36*8=288<512. |
| One scatter item | 1024: at most 12 instructions for digest/digit, 12 for bucket pointer access, 12 to construct source and destination addresses, 24 to load/store four fields, 12 to increment/store Next and 16 for loop control/transfers; 88*8=704<1024. |
| All bucket work, per bucket per pass | 2048 combined for clearing Count in its separate loop and the prefix loop: fewer than 128 instructions at eight operations each for addresses, zero store, Next store, Count load, total increment and both loop controls. |
| Other pass overhead | 1024 for setup, base swap, digit shift and four-pass control. |
| One adjacent scan position | 1024: at most six record-field reads with addressing, digest comparison, two message comparisons, Boolean/branch operations and cursor updates; below 128 instructions at eight operations each. |
| Final verification and output | 2^16 ordinary operations plus two B2 calls: two wrappers, comparisons and byte-by-byte serialization of two 64-byte messages, including shifts/masks/stores and loop control. |

All q positions are processed in both histogram and scatter on each pass, even
when digest values are adversarially concentrated. Prefix sum and clearing each
visit all R buckets. No distributional or average-case assumption enters time.
Total ordinary operations on every possible choice of coins satisfy

```
W <= 2^25 + 8192q + 4(1536q + 2048R + 1024) + 1024q + 2^16
   = 15360q + 8192R + 33624064.
H_calls <= q+2.
T <= q+2 + (15360q+8192R+33624064)/430.
```

Here q=2^128 and R=2^64. Since the constant and bucket terms are tiny relative
to q, exact integer arithmetic gives `T < (3673/100) q`. To certify the stated
exponent without relying on rounded logarithms, integer exponentiation gives
`3673^5 < 2^26 * 100^5`. Therefore

`T < (3673/100) * 2^128 < 2^(128+26/5) = 2^133.20`.

The direct logarithm of the displayed T upper bound is approximately
133.198530701159. The claimed 133.20 rounds upward with a small explicit margin;
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
of its body. Fixed IV/permutation/flags/masks fit in 1024 words, while
4096 words cover all scratch and spill locations, including compression wrapper
state, message buffers, prefix accumulator, address temporaries and outputs.
These finite allowances are below 2^24 bytes together. No recursion is needed.
Code and fixed initialization fit inside the 2^25 ordinary-operation budget;
large table initialization is charged separately per pass, not hidden here.

Thus `M <= 256q+64R+2^24 < 2^137` bytes. Word addresses, including the fixed
storage and one-past-end values, are far below the 256-bit address limit.
These enormous abstract resources are not claimed to be practical hardware.

Fixed preprocessing takes at most `2^25/430` target-compression equivalents;
`preprocessing_log2=25` is a conservative bound and that work is already in T.
There is no target-specific nonuniform advice, collision database, or omitted
search. The nonnegative schema field `nonuniform_advice_log2_bytes=0` bounds
zero actual advice by one byte; it is not an attempt to take log2(0) or conceal
uniform program storage. No optional legacy data metric is asserted.

## 7. Evidence and limitations

Heuristics are empty. The proof uses only exact selected-hash semantics, the
stipulated independent random-word primitive, deterministic radix-sort
invariants, the distribution-free probability argument, and explicit resource
bounds. In particular, it needs no BLAKE3 output-balance or random-oracle
premise. There is no extrapolation from reduced-output experiments.

The certificate manifest remains valid and empty. No participant executable or
experiment manifest is supplied; no concrete collision or full-scale run is
claimed. Mechanical checks establish package consistency only. AI screening,
if it passes, establishes the exploratory label `plausible_not_refuted`, not a
mathematical proof, manual acceptance, or successful publication.

The starting BLAKE3 r2 repository package at commit
`86f1102ff2d6873db29d992599412ae9eb23bda2` declared exponent 140, 2^129
samples, iterative merge sorting, and success 0.5. Section 1 retains its exact
complete-hash definition, checked against the organizer reference as text.
This replacement halves the sample count, uses the permitted 0.39 success
requirement, and substitutes four fully initialized radix passes.

The initialized radix construction and self-contained probability proof are
adapted from this solver's SHA-256 r32 submission
`728e01db-9b30-4dbc-8555-d0bb6a008f70`. That package passed AI screening at
131.16 and is awaiting human review; its verdict is not a premise here. BLAKE3
uses a different wrapper and price: one selected compression rather than two
per message, and C=430 rather than 2224. All success, memory and time obligations
are stated afresh in this package, which needs its own review. No unpromoted
contribution from another solver is incorporated. The operation caps favor an
auditable bound over aggressive constant optimization. Memory is a reported
resource, not a claim of physical feasibility or a scalar tie-break.
