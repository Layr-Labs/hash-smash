# MD5-s63: rigorous complete-message generic collision construction

This package fixes `md5-s63-prefix-v1`, 63 steps, ordinary collisions,
`collision-frontier-v3`, and the rigorous lane. The result below is a
self-contained analytic upper bound for a concrete finite randomized algorithm.
It uses no cryptanalytic heuristic, precomputed collision, or empirical premise.
It is deliberately conservative and computationally infeasible in practice.
The required `baseline_improved` value `md5-s63-nominal-v2` is an organizer
identifier only: its nominal exponent 64 is not an established attack, qualified
baseline, or security bound. This submission does not claim to improve it.
An eventual AI qualification is distinct from mathematical or human acceptance.

## 1. Exact message family and complete hash

Let q = 2^64 and N = 2^128. For a 256-bit word x, let m(x) be its 32-byte
little-endian encoding, including leading zero bytes. This encoding is injective.
All these messages have exactly 256 bits, within the profile's bit-length limit
2^64. The input domain has D = 2^256 elements. No IV is chosen by the algorithm.

Every m(x) receives the mandatory complete-message MD5 padding: append byte 0x80,
then 23 zero bytes, then the eight-byte little-endian integer 256. Thus there is
exactly one 64-byte block. As two little-endian 256-bit RAM words this block is
(x, P), where P = 0x80 + (256 << 192). Splitting it into sixteen 32-bit words
M[0], ..., M[15] gives M[j] = (x >> (32*j)) AND 0xffffffff for 0 <= j < 8,
M[8] = 0x80, M[9] through M[13] = 0, M[14] = 256, and M[15] = 0.

Here is the exact compression and output definition. All intermediate MD5 state
values are reduced modulo 2^32, NOT means the 32-bit complement, and ROL32(v,s)
is ((v << s) OR (v >> (32-s))) AND 0xffffffff after masking v to 32 bits.
Start (a,b,c,d) = (A0,B0,C0,D0) =
(0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476).
For i = 0,1,...,62 in that order, use these original-index rules:

| Index i | F | g | rotation s, repeating every four steps |
| --- | --- | --- | --- |
| 0..15 | (b AND c) OR ((NOT b) AND d) | i | 7,12,17,22 |
| 16..31 | (d AND b) OR ((NOT d) AND c) | (5*i+1) mod 16 | 5,9,14,20 |
| 32..47 | b XOR c XOR d | (3*i+5) mod 16 | 4,11,16,23 |
| 48..62 | c XOR (b OR (NOT d)) | (7*i) mod 16 | 6,10,15,21 |

Perform the simultaneous assignment
(a,b,c,d) := (d, b + ROL32(a+F+K[i]+M[g],s), b, c), modulo 2^32.
The 63 constants K[0] through K[62], in index order, are the following
literal hexadecimal integers. They are public program constants, with storage
and loading charged below; there is no run-time trigonometric computation.

```text
d76aa478 e8c7b756 242070db c1bdceee f57c0faf 4787c62a a8304613 fd469501
698098d8 8b44f7af ffff5bb1 895cd7be 6b901122 fd987193 a679438e 49b40821
f61e2562 c040b340 265e5a51 e9b6c7aa d62f105d 02441453 d8a1e681 e7d3fbc8
21e1cde6 c33707d6 f4d50d87 455a14ed a9e3e905 fcefa3f8 676f02d9 8d2a4c8a
fffa3942 8771f681 6d9d6122 fde5380c a4beea44 4bdecfa9 f6bb4b60 bebfbc70
289b7ec6 eaa127fa d4ef3085 04881d05 d9d4d039 e6db99e5 1fa27cf8 c4ac5665
f4292244 432aff97 ab9423a7 fc93a039 655b59c3 8f0ccc92 ffeff47d 85845dd1
6fa87e4f fe2ce6e0 a3014314 4e0811a1 f7537e82 bd3af235 2ad7d2bb
```

After step 62, feed forward every word: (A,B,C,D) =
(A0+a, B0+b, C0+c, D0+d), modulo 2^32. The digest is the 16-byte concatenation
LE32(A) || LE32(B) || LE32(C) || LE32(D). Write H(x) for its injective numeric
encoding A + (B << 32) + (C << 64) + (D << 96), stored in one 256-bit RAM word
with upper 128 bits zero. Numeric equality of H values is equality of all 16
digest bytes. There is no truncation or omitted padding block. This definition
matches the selected profile and its organizer digest reference. In particular,
step 63 of full MD5 is not executed; MD5-s64 is a different target.

## 2. Algorithm, layout, and stopping rule

Allocate two arrays U and V, each holding q records. A record occupies exactly
two 256-bit words, first its digest H(x) and then the message word x. The array
word offsets for record i are (i << 1) and (i << 1)+1. There are no pointers per
record, hidden object headers, or retained random tapes. Explicitly zero all 4q
array words before sampling. This is a word-RAM construction, not a claim about
Python object memory or a supplied executable. The pseudocode is inert proof.

For i = 0,...,q-1, draw one fresh independent uniform 256-bit word x using the
primitive provided by the cost model. Evaluate the complete H(x) above and store
(H(x),x) in U[i]. Every draw is kept, including repeated messages. Do not seed a
pseudorandom generator or assume its expansion is independent randomness.

Sort U by digest, using bottom-up mergesort with V as its scratch array:

```text
src := U; dst := V; width := 1
while width < q:
    for left := 0, 2*width, 4*width, ..., q-2*width:
        mid := left+width; end := mid+width
        i := left; j := mid; k := left
        while k < end:
            if i == mid:
                copy src[j] to dst[k]; j := j+1
            else if j == end:
                copy src[i] to dst[k]; i := i+1
            else if src[i].digest <= src[j].digest:
                copy src[i] to dst[k]; i := i+1
            else:
                copy src[j] to dst[k]; j := j+1
            k := k+1
    swap src,dst
    width := width << 1
```

A copy transfers both words. Since q is a power of two, there are exactly 64
passes, all subruns have their stated lengths, and every pass writes q records.
The tie rule is deterministic; sorting stability is unnecessary for correctness.
The current source after the last pass is the sorted array; do not copy it again.

Scan adjacent records k-1 and k for k = 1,...,q-1. If digests differ, continue.
If the two message words are identical, continue as well: a repeated input is
not success and does not stop the scan. At the first adjacent equal digest with
different message words x,y, recompute both complete H(x),H(y) using Section 1,
check x != y and H(x) == H(y), and return (m(x),m(y)). If verification fails,
return failure; this branch is unreachable under exact RAM operations. If the
scan finishes, return failure. There is exactly one batch and no restart,
amplification, early successful sampling stop, or uncharged adaptive search.

Correctness of sorting follows by induction on width: each merge emits the
smaller next digest from its two sorted runs, preserving each record, so the
new runs are sorted. In a final equal-digest run containing at least two distinct
message words, some adjacent message words differ. Otherwise equality of every
adjacent pair would, by transitivity, make every message in that run identical.
Consequently the scan returns precisely when the sampled multiset contains a
collision of distinct messages. Duplicate copies cannot hide such a collision.
The final explicit check certifies the target relation for every returned pair.

## 3. Probability proof for this fixed function

H is fixed and deterministic. For each of the N possible digest values z, let
p_z = |{x in {0,1}^256 : H(x)=z}|/D. These probabilities are nonnegative and sum
to one. They are not assumed equal and are not estimated by experiments. For
independent input words X_1,...,X_q, the outputs H(X_1),...,H(X_q) are independent
with this common distribution: for any sets S_j of outputs, independence of the
X_j gives Pr[all H(X_j) in S_j] = product_j Pr[X_j in H^(-1)(S_j)]. This fact
requires no independence of internal MD5 states or random-oracle model.

We prove the needed distribution-free birthday inequality. For nonnegative
p_1,...,p_N with sum one, write e_k(p) for the sum of products over all k-element
subsets of coordinates, with e_0=1. For independent draws with distribution p,
Pr[all q outputs distinct] = q! e_q(p).
For any two coordinates a,b and the vector r of remaining coordinates,

    e_q(p) = e_q(r) + (a+b)e_(q-1)(r) + ab e_(q-2)(r).

At fixed a+b, replacing a,b by their average cannot decrease this expression,
because e_(q-2)(r) >= 0 and ab increases. For completeness, the averaging
argument has an exact finite-dimensional maximization justification. The
probability simplex is compact, so e_q has a maximum; among its maximizers
choose one minimizing sum_j p_j^2. If two coordinates were unequal, averaging
them would either increase e_q, contradicting maximality, or retain its maximum
while strictly decreasing sum_j p_j^2, contradicting the choice. Hence this
maximizer is uniform. This proves, also for distributions with zero coordinates,

    Pr[all q outputs distinct]
      <= q! binomial(N,q) / N^q
       = product_(j=0)^(q-1) (1-j/N)
      <= exp(-q(q-1)/(2N)).

The last inequality uses 1-u <= exp(-u) for 0 <= u < 1. Here q <= N, so it
applies to every factor. The uniform distribution minimizes birthday collision
probability; the proof does not assert that the selected MD5 variant is uniform.

Let E be the event of some equal pair of sampled digests. Let R be the event
of any equal pair of sampled input words. The union bound gives

    Pr[R] <= binomial(q,2)/D < 2^-129,
    Pr[E] >= 1-exp(-1/2 + 2^-65).

On E outside R the algorithm certainly returns a collision of distinct inputs.
Some outcomes in R also succeed; discarding all of them only weakens the bound.
Therefore its success probability is at least

    1-exp(-1/2 + 2^-65) - 2^-129 > 0.39.

An exact comparison avoids reliance on floating-point numerics: a=1/2-2^-65
is greater than 499/1000; the positive series for exp(a) gives
exp(a) > 1 + 499/1000 + (499/1000)^2/2 + (499/1000)^3/6 > 41/25.
Thus success > 16/41 - 2^-129 > 39/100, because
16/41 - 39/100 = 1/4100 and 2^-129 < 1/4100.
The `success_probability: 0.39` field is a conservative lower bound, rather
than an exact success estimate, reviewer confidence, or physical feasibility.

## 4. Explicit 256-bit word-RAM resource ledger

Every primitive listed by `collision-frontier-v3` costs one unit, as does one
selected 63-step target compression. A 32-byte message requires exactly one
such compression. Target-internal steps in Section 1 specify this trusted
primitive, whose one-unit cost is stipulated by the model. Padding, loading the
IV and input, packing/unpacking, calls/returns, address arithmetic, loop counters,
comparisons, branches, and storage outside that primitive are charged separately.
No multiplication, unbounded integer, dynamic library, or unit-cost sort is used.
Every index, pointer, length, intermediate address, and counter is less than
2^80 and hence fits in a single 256-bit word. MD5's narrower masks and rotations
are explicit above; integers do not silently acquire unbounded precision.

To make the conservative constants reproducible, use a direct RAM instruction
encoding with an opcode and at most three operand/immediate words, at most four
256-bit words per instruction. All temporary values may live in word-addressed
scratch slots. A primitive using scratch operands can be expanded into at most
two operand loads, the primitive, one result store, and one transfer of control.
The bounds below allow this five-operation expansion even when registers would
avoid these loads and stores. Fixed-address constants and two-word records need
no allocation machinery. Fetching constant operands is included among the loads.
Ordinary instruction fetching has the usual RAM semantics; executable storage
is explicitly counted even though there is no extra implicit fetch-time tax.

Here are conservative operation bounds for the specified loops. Each count
includes the relevant end test and its branch, and branches do not hide extra
message/hash work.

| Component | Derivation of charged upper bound |
| --- | --- |
| Static setup | At most 2^20 operations to install the fixed code/constants and initialize at most 256 scratch words, pointers and counters. |
| Array initialization | At most 256q operations: 4q zero stores, each with index increment, end comparison, branch, and address/scratch overhead bounded by twelve simple statements or sixty expanded operations. The allowance also covers the final test. |
| Sampling and hash wrapper | At most 512q operations: per sample one random word, two block-word stores, four IV loads/stores, one target compression, four output-word loads, six shifts/ORs for packing, record stores and loop/address overhead. There are fewer than 64 simple primitive statements, each expandable within five operations, plus the one compression; 512 allows padding and call bookkeeping. |
| One merge pass | At most 256q operations, including all merge setup and pass control. Derivation follows immediately below. |
| Adjacent scan | At most 256q operations: at most four record-word loads, two equality tests, branches, two shifted record offsets, address additions and index control per adjacent position; fewer than 40 simple statements expanded by five, with room for the final test. |
| Final verification/output | At most 4096 operations for two complete digest evaluations with the same wrapper, distinctness/full-digest comparisons, two 32-byte output stores, and return/failure control. Zero or one verification occurs. |

For the merge bound, retain i,j,k,mid,end and the two array bases as scratch
words. Per emitted record there are at most four control comparisons and four
branches (end test, exhausted-left, exhausted-right, digest order), at most two
digest loads, two message/digest loads for the selected record, two destination
stores, at most four record/word offset shifts or increments, at most six base
or field address additions, and at most three index/control updates. This is
at most 27 simple statements, or 135 expanded operations; reserve 160 per record.
Initializing mid,end,i,j,k and advancing left takes at most 60 expanded operations
per merged pair. There are at most q/2 pairs, contributing at most 30q. Reserve
64 operations for pass control and swapping base pointers. Thus a pass costs
at most 190q+64 <= 256q for q=2^64. Record copies always copy both words;
no implicit comparison sort or hash-table operation is assigned unit cost.
All 64 passes therefore cost at most 16384q operations.

The code is uniform straight-line initialization plus the displayed bounded
loops and the hash wrapper. Fewer than 512 simple statements suffice for the
outer algorithm: fewer than 64 for generation, fewer than 64 for merge/control,
fewer than 40 for scanning, fewer than 128 for initialization/output, and fewer
than 64 for the wrapper/control glue. Implement the target definition as a loop,
not an unrolled 63-step program. Its loop body and initialization require fewer
than 128 additional simple statements: the Boolean functions, shifts, masks,
additions, table loads, feed-forward and serialization are all explicit in
Section 1. Compute 5*i as (i << 2)+i, 3*i as (i << 1)+i, 7*i as (i << 3)-i,
and reduction modulo 16 as AND 15. Thus no multiplication/division opcode is
needed. Expanding all fewer than 640 statements by the five-operation scratch
rule gives fewer than 4096 static RAM instructions. At four words per
instruction, their code occupies at most 2^19 bytes. Store the 63 K constants,
16 rotations, fixed IV, masks, padding, and loop bounds in fewer than 128 words
(4096 bytes). No additional unrolled target description is retained.
This establishes ample room within the charged 2^20-byte static/scratch allowance.
Writing all code/constants/scratch words costs less than 2^20 operations as
budgeted; there is no input-dependent compilation, advice search, or preprocessing
omitted from the charge. The mathematical prose is an analysis, not an auxiliary
data structure read by the algorithm.

Combining worst-case work, whether this batch succeeds or fails, gives

    T <= 2^20 + 256q + 512q + 64*256q + 256q + 4096
       = 2^20 + 17408q + 4096
       < 32768q = 2^79.

All randomness, unsuccessful samples, repeated messages, sorting, verification,
and initialization have been included. There are no restarts to average away.
`time_log2: 79` denotes this deterministic upper bound on total charged work,
not just the exponent of the q hash evaluations. If target primitive internals
are provided by trusted fixed hardware, their specification remains Section 1;
if their constants/code are retained, the static allowance already includes them.

Peak memory comprises two arrays of 2q words, exactly 128q = 2^71 bytes, plus
at most 2^20 bytes for code, constants, working state, all scratch words, pointers,
block buffers, and the two returned messages. The arrays include all retained
randomness. Buffers are reused for final checking while arrays remain allocated.
No recursive stack is used. Thus M <= 2^71+2^20 < 2^72 bytes, justifying
`memory_log2_bytes: 72`. The addresses require at most 72 bits even if byte
addresses are used, so the RAM word can address the entire claimed memory.

`data_log2: 65` bounds the number of complete input-message evaluations supplied
to the fixed digest operation: q during generation and at most two during final
checking, q+2 <= 2^65. No external corpus is provided. Their total unpadded input
volume is 32(q+2) bytes; their padded block volume is 64(q+2) bytes. These volumes
are generated and charged, not additional unaccounted storage. All internal
sorting movement is already in T; data counts evaluations, not bytes moved.

`preprocessing_log2: 73` bounds preprocessing operations, specifically static
setup plus explicit table initialization: 2^20+256q < 2^73. This is disclosed
separately but included in T. There is no hash search before the charged batch.
`nonuniform_advice_log2_bytes: 0` means an upper bound of one byte, consistent
with actual zero bytes of nonuniform advice (the schema does not permit log(0)).
Fixed public code/constants are counted in memory and setup even though they
are uniform, not advice. No stored collision is given free of construction cost.
The proposed scalar is therefore 79+72 = 151, only if the selected lane qualifies;
it is not an already emitted score and does not assert Pareto improvement.

## 5. Evidence, applicability, and limitations

The claim's empty heuristic list is intentional: Sections 1-3 prove correctness
and the success bound for every fixed function with these domain/range sizes,
and Section 4 gives an explicit upper-bound implementation in the specified
RAM model. There is no assumed random output distribution, Markov model,
trail independence, state-uniformity extrapolation, quantum operation, or oracle
for an unknown mathematical property. The model explicitly supplies independent
uniform random words; replacing them with a deterministic seed expander would
be a different claim needing a different success analysis.

The package contains an empty certificate manifest and declares no experiment
manifest or executable experiment source. Its analytic evidence consists of the
exact target definition, collision-search algorithm, finite probability argument,
and RAM resource ledger above. No full-scale execution, sampled experiment, or
concrete collision certificate is reported. The probability calculation uses the
independent uniform random-word primitive specified by the cost model.
