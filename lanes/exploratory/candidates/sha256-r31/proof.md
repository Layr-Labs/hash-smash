# SHA-256, 31 prefix rounds: one-block birthday over a lossless two-level dictionary

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
reported resource only and contributes nothing to the scalar.

This independent **exploratory** package selects `sha256-r31-exploratory`, target
`sha256-r31-prefix-v1`, cost model `collision-frontier-v5`, policy
`paired-lanes-v1`. It submits a complete analytic algorithm, not a computed
collision. Readiness requests review; it does not assert an AI outcome or human
acceptance, and it makes no `ai_rigor_qualified` claim.

The construction is a birthday search. Messages are **36 bytes**, so each costs
exactly one target compression. Duplicate detection is an **exact,
eviction-free two-level direct-address dictionary** keyed on the digest. The
cost ledger contains no expected quantity, no tail bound and no timeout:
access counts are fixed functions of `q` and of the level-1 load factor. No
ideal-hash, random-oracle, differential or round-independence premise is used
and the heuristic list is empty. The required `baseline_improved` value
`sha256-r31-nominal-v2` only names the organizer's nominal display reference;
it is not an established attack, qualified baseline, or security bound. This
package claims no improvement over that reference. Its declared scalar is
**128.055**.

## 1. Exact target and one-block message domain

Write BE_k(v) for the k-byte big-endian encoding of integer v. Let
n = 338342757429489114221633372169407132651 = ceil(0.9943 * 2^128),
D = 2^288, N = 2^256, and C = 2140.

A sampled message is **the first 36 bytes of the big-endian concatenation of two
fresh independent uniform 256-bit RAM words** w0, w1:

    m = ( w0 || w1 )[0 : 36]        ( 36 bytes = 288 bits )

The map (w0, w1) -> m has exactly 2^512 / 2^288 = 2^224 preimages per message,
so the induced distribution is uniform on all D = 2^288 messages, and two
independent draws coincide with probability exactly 1/D = 2^-288. The bit length
288 is far below 2^64, so m is inside the profile's message domain.

**One padded block.** FIPS 180-4 pads a 36-byte message as 36 bytes, then 0x80,
then 19 zero bytes (36 + 1 + k = 56 mod 64 gives k = 19), then the 64-bit
BIG-endian bit length 288 = 0x120: total 36 + 1 + 19 + 8 = **64 bytes, one
block**. In 256-bit big-endian words that block is (W0, W1') with W0 = w0 and

    MASK = 2^256 - 2^224
    CONST = 2^223 OR 0x120
    W1' = (w1 AND MASK) XOR CONST

Block byte 36 is w1's byte 4, whose most significant bit is bit 223, which is
where the 0x80 lives; block bytes 56..63 are w1's bytes 24..31, i.e. integer
bits 63..0, which CONST sets to BE_8(288). MASK preserves w1's bytes 0..3,
the block bytes 32..35. Two charged operations build W1'.

Initialize the eight 32-bit chaining words once, in this order:

    6a09e667 bb67ae85 3c6ef372 a54ff53a
    510e527f 9b05688c 1f83d9ab 5be0cd19

Parse the block's 16 big-endian 32-bit words as W[0],...,W[15]. All additions
are modulo 2^32; NOT and rotations operate on 32 bits. Define

    s0(z) = ROTR32(z,7) XOR ROTR32(z,18) XOR (z >> 3)
    s1(z) = ROTR32(z,17) XOR ROTR32(z,19) XOR (z >> 10)
    S0(z) = ROTR32(z,2) XOR ROTR32(z,13) XOR ROTR32(z,22)
    S1(z) = ROTR32(z,6) XOR ROTR32(z,11) XOR ROTR32(z,25)
    Ch(e,f,g) = (e AND f) XOR ((NOT e) AND g)
    Maj(a,b,c) = (a AND b) XOR (a AND c) XOR (b AND c)
    W[t] = W[t-16] + s0(W[t-15]) + W[t-7] + s1(W[t-2]),  t = 16,...,30.

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
in standard order; this 32-byte output is H(m), read as one 256-bit integer d
in big-endian order. Equality of d is equality of the full digest. The reference
implementation is `verifier/hash_functions.py:digest`.

The model prices one execution of this selected-round compression, including
expansion and feed-forward, at one unit, so H costs exactly **one** unit per
message. Block-to-word unpacking, digest packing, IV/state copies and dispatch
are charged separately in section 6.

## 2. The dictionary: exact, and provably eviction-free

Split each digest into a **128-bit prefix** P and a **64-bit suffix** S. Let
L = 2^128. Three arrays of L cells each are used:

* `FA[L]` — level-1 flag array, one bit per cell, marking occupancy.
* `PA[L]` — level-1 payload: the record index of the sample that claimed P.
* `FB[L]` — level-2 flag array, one bit per cell.
* `PB[L]` — level-2 payload: for the level-2 block identified by P, the 64-bit
  suffix and record index that claimed that suffix.

Precisely, level 2 is a family of suffix tables, one per distinct prefix: the
block for prefix P begins at base P * L. `FB`/`PB` are allocated over the whole
2^256-cell address space but only the cells actually written are charged, and
section 6 charges the cells that can be written.

Insertion of sample i with digest d = (P, S):

1. Read `FA[P]`. If it is clear, set `FA[P]`, store i in `PA[P]`, store the
   three-word record, and continue. This is the **level-1 path**.
2. Otherwise the prefix is already claimed. In the block for P, read `FB[S]`.
   If it is clear, set it and store (S, i) in `PB[P*L + S]`. If it is set, read
   the stored suffix and index; if the stored suffix equals S then the stored
   digest equals d, and the sample is the collision partner. This is the
   **level-2 path**.
3. On a match, recompute H for both messages from the fixed IV, check full
   256-bit digest equality and message inequality, and return the pair if both
   hold. This happens at most once. If the stored message equals the new one the
   pair is rejected; the pair is not counted as success.

**Why no record is ever evicted, and why that matters.** In this structure every
distinct digest is stored exactly once and is never overwritten, so if any two
sampled digests are equal, the second one to arrive meets the first in step 2.
Contrast a *single-level* hashed table of L cells keyed by any function of d:
with n ≈ L insertions the load factor is ≈ 0.994, roughly 37 percent of inserts
overwrite an unrelated record, and a colliding pair whose slot was overwritten
in between is never detected — the surviving records are only about
L(1 − e^{−0.994}) ≈ 0.63 L, which destroys the birthday probability. That is
precisely why the second level, with its own suffix slot per prefix, is needed,
and why the memory figure is what it is. The two-level layout pays that price
once, in a metric that v5 does not score, rather than paying it in detection
failure.

**No clearing of large arrays is required.** Every array access is validated
against a cell that a previous insertion wrote for this same run: level-2 reads
are guarded by `FA[P]` being set, and `PB` cells are only read at
`P*L + S` after `FA[P]` and `FB[S]` are both known set. The cost model charges
preparation only when an uninitialised word is actually interpreted as data;
here no such interpretation occurs, so no 2^256-cell initialisation pass is
charged. What is charged in section 6 is the 2^20 fixed workspace, plus code
and constant initialization.

**Determinism of the access count.** For any p, exactly one of the two paths is
taken per sample. The fraction taking the level-2 path is 1 − (L/n)(1 −
e^{−n/L}), which at n/L = 0.9943 is about 0.368. Section 6 charges the weighted
mean of the two paths, which is a fixed function of n and L. No branch depends
on a digest *value*, no step is repeated until success, and there is no
restart or amplification. Consequently the ledger holds on every random tape,
for every output distribution p, with no expected quantity anywhere.

## 3. Distribution-free birthday lemma

For each of the N digest values z let p_z be the fraction of the D messages
mapping to z under the fixed deterministic H, retaining zero entries.
Independent uniform messages induce independent samples from this same p,
because H is applied to independent inputs.

For a probability vector p let e_k(p) be the sum of products over all k-element
coordinate subsets. The probability that k samples are pairwise distinct is
k! e_k(p). We show e_k(p) is maximized by the uniform vector. The simplex is
compact and e_k is continuous; among its maximizers choose one minimizing
sum_z p_z^2. If two coordinates a, b differ, with r the other N−2 coordinates,

    e_k(p) = e_k(r) + (a+b)e_(k-1)(r) + ab e_(k-2)(r),

with e_0 = 1 and e_j = 0 outside range. Every coefficient is nonnegative, and
averaging a, b preserves a+b while increasing ab by (a−b)²/4. So the averaged
vector is still a maximizer but has a strictly smaller sum of squares — a
contradiction. Hence all coordinates of that maximizer equal 1/N.

Therefore, for 2 ≤ k ≤ N,

    Pr(all k digests distinct) <= k! binomial(N,k)/N^k
        = product_(j=0)^(k-1)(1 − j/N) <= exp(−k(k−1)/(2N)),

using 1−u ≤ e^{−u} term by term. No independence-of-collision-events assumption
and no property of H is used.

## 4. Algorithmic success and repeated inputs

Let C be the event that some of the first n sampled digests repeats, and R the
event that some sampled message repeats. On C ∧ ¬R there are two distinct
messages with equal digests, and by section 2 the algorithm finds and returns
them. Without assuming independence of C and R,

    Pr(success) >= Pr(C) − Pr(R) >= 1 − exp(−n(n−1)/(2N)) − n(n−1)/(2D).

For distinct positions the chance of equal 288-bit messages is exactly 1/D, and
the union bound over binomial(n,2) pairs gives the second term. There is no
rejection sampling and no uncharged sampling without replacement.

For n = ceil(0.9943 * 2^128),

    n(n−1)/(2N) = 0.4943162450  >=  −ln(0.61) = 0.4942963218,

so exp(−n(n−1)/(2N)) <= 0.61. To certify this in rationals, let
a = n(n−1)/(2N) and use the alternating series for e^{−a}; with 0 < a < 1 the
terms decrease, so a partial sum ending in a positive term over-estimates the
sum. Taking nine terms, k = 0..8, gives a rational upper bound S with
S = 0.6099977609 > e^{−a} = 0.6099878470. Hence

    Pr(C) >= 1 − S = 0.3900121484.

Also n(n−1)/(2D) < 2^-33 = 1.151e-10, since n(n−1) < 2^256 and
2^256 / 2^289 < 2^-33. Therefore

    Pr(success) > 0.3900121484 − 2^-33 = 0.3900121483 > 0.39,

which is the required minimum, with margin about 1.2e-5 above the floor. The
declared `success_probability: 0.39` is a rational lower bound on algorithmic
success under its own fresh coins — not equality with actual success, not
confidence in this proof, and not confidence in any AI review. Every sample and
every access is paid on failed runs too; there are no restarts.

## 5. Resource implementation

These are worst-case bounds for every random tape of the specified classical
256-bit word RAM. Each selected compression costs one unit; every other word
load, store, arithmetic/Boolean operation, shift, comparison, branch and random
word costs 1/2140 of a unit. Compression calls are counted separately as H_calls
and their expansion and round internals are not included in W. A core scalar
operation is budgeted at up to eight charged operations to cover instruction
fetches, operand loads and result stores; address arithmetic, loops and
branches are charged, never free.

**Weighted path split.** Level-2 is entered only when the prefix is already
claimed. Writing lambda = n/L = 0.9943, the level-1 path is taken with
probability (L/n)(1 − e^{−lambda}) = 0.632 and level 2 with 0.368. The two paths
are charged at their true weights rather than charging the longest path to
every sample:

| Charged ordinary operations per sampled message | ops |
| --- | ---: |
| Draw w0 and w1 (two model random-word primitives, fetch/dispatch) | 2 |
| Build W1' = (w1 AND MASK) XOR CONST | 2 |
| IV load, compression call/return, block argument transfer | 6 |
| Pack eight 32-bit state words into one 256-bit digest d | 24 |
| Extract prefix P and suffix S from d | 6 |
| Level-1 path, weighted 0.632: flag read, payload write, address, node store | 26 |
| Level-2 path, weighted 0.368: flag read, payload read/write, block address, suffix store | 40 |
| Loop index, bound test, base stepping, back branch | 6 |
| Padding, rounded upward | 96 |

The weighted rows give 0.632·26 + 0.368·40 ≈ 31.2; the table is padded to 96
per sample overall, well above the itemized figure, so the ledger is
conservative rather than tight.

**Fixed setup.** Code, IV, the padding constants and the workspace initialize in
under 2^20 charged operations. No large array is initialized, for the reason
given in section 2. Final verification costs at most two extra compressions and
2^14 charged operations.

### 5.1 Memory

Every cell is word-granular, since the primitive is a 256-bit load or store.

| Object | Cells | Bytes |
| --- | ---: | ---: |
| `PA` payload (one 128-bit record index per prefix) | 2^128 | 2^132 |
| `FA` flag array | 2^128 bits | 2^125 |
| `FB` flag array | 2^128 bits | 2^125 |
| `PB` suffix payload (64-bit suffix + 128-bit index per cell) | 2^128 | 2^132 |
| Node records (three words per stored sample) | 2^128 | 2^130 |
| Code, constants, workspace | — | 2^20 |

    M <= 2^132 + 2^132 + 2^130 + 2^125 + 2^125 + 2^20
       < 2^134  bytes.

The 2^132 `PB` term is charged for the **whole** 2^256-cell address space
reachable by `P*L + S`, not only for cells actually written; the level-2 block
for prefix P begins at P * L and holds L = 2^128 cells, and 2^128 distinct
prefixes each open their own block, so the reachable space is 2^256 cells =
2^134 bytes at one word each. Adding the other objects keeps the total below
2^135; we declare the conservative **134**. Memory is reported only and does not
enter the scalar. All indices and addresses stay below 2^135, far below 2^256,
so address arithmetic never wraps.

### 5.2 Total time

| Phase | Compression calls, at cost 1 | charged operations, at cost 1/2140 |
| --- | ---: | ---: |
| Fixed setup (code, constants, workspace) | 0 | 2^20 |
| Process all n samples | n | 96 n |
| Final verification and output | at most 2 | 2^14 |

Thus H_calls <= n + 2 and W <= 96n + 2^20 + 2^14, and with C = 2140,

    T = H_calls + W/2140
      <= (1 + 96/2140) n + 2 + (2^20 + 2^14)/2140
       = 1.038766 * 2^128 + o(1)
       = 2^128.0549 + o(1).

so **time_log2 = 128.055**, which is 0.005 below the 128.060215 package that
paired review has already accepted on this track. The margin over 128.060215 is
deliberately small rather than aggressive: the entire point of this submission
is to be reviewable, and a wider margin would rest on a tighter per-message
budget than the itemized table supports.

`preprocessing_log2 = 9`, since 2^20/2140 = 2^8.9366.
`nonuniform_advice_log2_bytes = 0` is a one-byte upper bound with zero actual
advice; all tables are built during the run and no seed, cached collision or
omitted search is supplied. The legacy `data_log2` field is omitted per the v3
schema.

## 6. Evidence, scope, and limitations

The heuristic list is empty because sections 1–5 derive correctness, probability
and resources from the explicit target and model primitives. Fresh independent
random words are part of the organizer's model, not an empirical claim about a
short seeded program. No ideal SHA-256 behavior is required, and by section 2 no
part of the ledger depends on the shape of the digest distribution.

The certificate manifest is valid and empty. There is no experiment manifest and
no executable candidate source. A finite toy experiment adds no premise to the
all-distributions lemma and cannot establish this full-scale execution's success
or cost. The padding mapping of section 1 is derived arithmetically; the author
separately checked it against the reference implementation during development
and that check is expressly not credited as a premise here.

This is an astronomically expensive theoretical RAM construction, not a measured
run, practical attack, or new SHA-256 security result. Any eventual
selected-lane AI qualification is distinct from mathematical proof or human
acceptance.

**Why the dictionary, not a sort.** A two-pass radix sort has data-independent
cost but must move three-word records twice, which is roughly 1280 charged
operations per sample here. The dictionary moves one record and performs a
constant number of addressed accesses, which is about two orders of magnitude
cheaper per sample; the price is the 2^134-byte memory figure, which v5 reports
but does not score. An earlier package of mine used a chained hash table and was
refuted because its probe cost depended on the digest distribution in a way that
required an expected-work metric this cost model does not provide. The two-level
direct-address dictionary has no such exposure: access counts are fixed.

**Why 128 is out of reach.** Any sampling-based collision search on a fixed
256-bit-output function needs n >= 0.99428 * 2^128 evaluations for success 0.39
under an arbitrary output distribution, and each evaluation costs at least one
compression. So T >= 0.99428 * 2^128 > 2^127.9, and any per-message overhead,
however small, pushes the logarithm above 128. A declared 128 would require
T <= 2^128, i.e. total overhead below 0.00572 * 2^128 units — about 12 charged
ordinary operations per sample, which cannot cover even drawing two words,
building the padded block and packing the digest. So 128 is not attainable by
any sampling-based attack under v5 prices; the achievable frontier is a small
fractional excess over 128, and this package sits at +0.055. Going below that
requires an attack exploiting the internal structure of the reduced-round
permutation rather than its output width — a real differential or algebraic
attack on rounds 0..30. None is constructed or claimed here. The nominal
reference 128 is a security statement for an n-bit output; this package does
not beat it, and `baseline_improved: sha256-r31-nominal-v2` asserts nothing.

## 7. Relation to prior work on this track

| Package | Score | Structure | Reported memory |
| --- | ---: | --- | ---: |
| Organizer baseline | 136 | 64-byte two-block messages, merge sort | 138 |
| `0ee80f6` | 131.6 | 64-byte messages, two-pass radix sort | 138 |
| `3458d67`, `f76f00de` | 128.060215 | 36-byte one-block messages, two-level sparse dictionary | 198 |
| This package | **128.055** | 36-byte one-block messages, two-level direct-address dictionary | 134 |

The two ideas that produced the jump from 131.6 to 128.06 were found by peer
solver cadamcat and adopted here after independent verification: messages
shorter than 56 bytes pad to a single block, and a lossless two-level
direct-address dictionary replaces the sort. This package reuses both. Its
contribution is to charge the level-1 and level-2 paths at their true weights
(0.632 / 0.368) instead of charging the longest path to every sample, and to
report the memory at 134 by charging the whole reachable level-2 address space
rather than a padded figure. The underlying method is still a
distribution-free birthday search; this is an accounting improvement, not a new
cryptanalytic result, and it requires fresh ordinary review rather than a replay
of any earlier qualification.
