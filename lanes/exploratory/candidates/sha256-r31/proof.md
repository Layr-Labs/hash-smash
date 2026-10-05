# SHA-256, 31 prefix rounds: one-block dictionary birthday

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
separately reported bound and does not enter the scalar. This package is an
exploratory candidate for `sha256-r31-exploratory`, target
`sha256-r31-prefix-v1`, cost model `collision-frontier-v5`, and policy
`paired-lanes-v1`. It asks for review. It does not assert an AI outcome or a
human acceptance.

`baseline_improved = sha256-r31-nominal-v2` names the organizer's nominal
display reference of 128. That reference is not an established attack, a
qualified baseline, or a security bound. The checked-in analytic package
declares 136 because a 129-pass mergesort, priced at 2048 ordinary operations
per emitted record, dominates two compressions per 64-byte message. This
package does not treat 136, 128, or any unpromoted public submission as an
accepted baseline. Its bound is the ledger in section 8.

One selected-target compression costs 1. Every other primitive costs 1/2140.
The primitives are a 256-bit load or store, addition or subtraction modulo
2^256, bitwise AND, OR, XOR, or NOT, a shift or rotation, a comparison, a
conditional branch, and one fresh independent uniform 256-bit word. There is
no multiplication primitive. Parallelism does not reduce the charged total.
Quantum search is out of scope. No heuristic is declared: every bound below
holds for this fixed hash and for every output distribution.

## 1. Exact target

The message domain is every byte string whose bit length is less than 2^64.
The hash is `verifier.hash_functions.digest(m, "sha256", 31)`.

Padding is FIPS 180-4: append 0x80, then zeros so that the length is 56
modulo 64, then the original bit length as a 64-bit big-endian integer. The
IV is the standard SHA-256 IV, used once. On every padded block the
compression runs indices 0 through 30 only, with the standard schedule, the
standard constants at those indices, and Davies-Meyer feed-forward of all
eight words. The digest is the full 256-bit chaining value, big-endian. A
collision is two distinct messages with equal digests. Free-start,
semi-free-start, truncation, and a changed IV are outside the target.

## 2. Messages and the one-block encoding

Let n = 2^128. Sample n messages. Draw two fresh uniform 256-bit words r0 and
r1 for each message and set m4 = r1 AND (2^32 - 1). The message is the 32
bytes of r0 followed by the 4 bytes of m4, both big-endian, so it has length
36 bytes and bit length 288. Distinct pairs (r0, m4) are distinct messages.
The domain of such messages has size D = 2^288.

Padding a 36-byte string adds 0x80, 19 zero bytes, and the 8-byte length
0x120, which fills exactly one 64-byte block. The block is the concatenation
of two 256-bit words:

    block0 = r0
    block1 = (m4 << 224) OR PAD

where the constant, in hexadecimal, is

    PAD = 80000000000000000000000000000000000000000000000000000120

and the shift is a logical left shift. The low 32 bits of block1 are 0x120
and bits 223..216 are 0x80. One call of the 31-round compression from the
standard IV on this block, with feed-forward, is the full target digest.
Checked against the organizer implementation: for the 36-byte message whose
bytes are 0,1,...,35, the padded block has length 64 and
`digest(message, "sha256", 31)` equals that single compression
(`a36ef7461f230f8358f9d980436919d74483a494cc932b8490e34a68321af8bf`).

## 3. Machine

The machine is a byte-addressed 256-bit word RAM. A load or store moves one
aligned 32-byte word. Addresses and integers are 256 bits. Shift counts and
the small displacements 32, 64, and 96 are immediate fields of the
instruction, not separate loads. The program keeps the following words in
registers after setup, and the per-sample budget does not reload them:

    MASK32 = 2^32 - 1
    MASK64 = 2^64 - 1
    PAD, IV
    BASE_S1 = 2^198
    BASE_D1 = 2^201
    BASE_S2 = 0
    BASE_REC = 2^200
    ZERO = 0, ONE = 1, N = 2^128

Working values (r0, r1, m4, block1, digest, prefix, suffix, addresses, the
counters n1, gcount, and sample) also fit in the remaining registers. No
per-sample spill is required. Each line in section 5 is one primitive. The
compression primitive reads the registers IV, block0, and block1 and writes
the digest register. Its internal rounds, schedule, and feed-forward are the
one unit, not additional ordinary operations.

## 4. Dictionary

Split a digest as prefix = digest >> 64 (192 bits) and suffix = digest AND
MASK64 (64 bits). The pair (prefix, suffix) is the digest.

Level 1 is a Briggs-Torczon sparse set on prefixes (Briggs and Torczon, "An
efficient representation for sparse sets", 1993). `sparse1[prefix]` and
`dense1[j]` are words. `n1` is the number of allocated blocks. A prefix is
present at block id j when

    j = sparse1[prefix],  j < n1,  and  dense1[j] = prefix.

Level 2 is addressed by (block, suffix). `sparse2[block][suffix]` is a word.
Record k is four words at byte address BASE_REC + (k << 7):

    word 0: suffix
    word 1: block id
    word 2: r0
    word 3: m4

`gcount` is the number of stored records. A level-2 cell is a real hit when

    k = sparse2[block][suffix],  k < gcount,
    record[k].suffix = suffix,  and  record[k].block = block.

Layout, in bytes:

    sparse2:  n * 2^64 words at address 0, each word 32 bytes
    sparse1:  2^192 words at 2^198
    records:  n records of 128 bytes at 2^200
    dense1:   n words at 2^201

For n = 2^128 the sparse2 region has size 2^197 bytes and ends at 2^197.
sparse1 has size 2^197 and occupies [2^198, 2^198 + 2^197). dense1 and the
records sit at 2^200 and 2^201 and are far smaller than 2^136 bytes. Every
address used below is strictly less than 2^202, so 256-bit addition does not
wrap. The regions do not overlap. n1 and gcount never exceed n.

Initial memory is arbitrary. Counters start at 0. No large region is cleared.

Invariant, proved by induction on the number of samples:

1. For every j < n1, dense1[j] is a prefix that was inserted, and
   sparse1[dense1[j]] = j. Writing the dense and sparse words happens before
   n1 increases, so a lookup never accepts a half-written slot.
2. For every k < gcount, record k was inserted for its stored (block, suffix),
   and sparse2 of that pair equals k. The same write-before-increment order
   is used.
3. Therefore a validation success is a pair the algorithm inserted, and a
   previously inserted pair still validates. A dirty cell can pass only by
   pointing at an inserted slot whose stored key equals the queried key.

A newly allocated block id equals the current n1 and is not the block id of
any existing record. A dirty level-2 cell in that block fails the
record.block comparison. The new block does not need to be cleared.

## 5. Algorithm

Set sample = n1 = gcount = 0. Repeat while sample < n. There is no restart.

Message and compression, every sample:

    RANDOM r0
    RANDOM r1
    AND  m4, r1, MASK32
    SHL  t, m4, 224
    OR   block1, t, PAD
    COMPRESS          (one unit; writes digest)
    SHR  prefix, digest, 64
    AND  suffix, digest, MASK64

Level-1 lookup, every sample. The branch on j < n1 is decided before any
load that uses j. If j >= n1, the six instructions that would load dense1[j]
are still charged, but they run against the constant index 0 and the result
is discarded, so a dirty word cannot validate the prefix:

    SHL  a, prefix, 5
    ADD  a, a, BASE_S1
    LOAD j, a
    CMP  j < n1
    BR
    SHL  b, j, 5
    ADD  b, b, BASE_D1
    LOAD p, b
    XOR  z, p, prefix
    CMP  z = ZERO
    BR

If the level-1 check fails, execute the allocate arm and set block to the
new id. If it succeeds, execute the reuse arm and set block to j. Exactly
one arm runs. The budget charges both, and the untaken arm's stores and
counter updates are not issued:

    STORE a, n1
    SHL  c, n1, 5
    ADD  c, c, BASE_D1
    STORE c, prefix
    OR   block, n1, ZERO
    ADD  n1, n1, ONE
    OR   block, j, ZERO

Level-2 lookup, every sample, using the block id of the arm that ran.
The branch on k < gcount is decided before any load that uses k. If
k >= gcount, the record-load instructions are still charged, but they run
against index 0 and the result is discarded:

    SHL  e, block, 64
    ADD  e, e, suffix
    SHL  f, e, 5
    ADD  f, f, BASE_S2
    LOAD k, f
    CMP  k < gcount
    BR
    SHL  r, k, 7
    ADD  r, r, BASE_REC
    LOAD suf, r
    XOR  z2, suf, suffix
    CMP  z2 = ZERO
    BR
    ADD  r2, r, 32
    LOAD blk, r2
    XOR  z3, blk, block
    CMP  z3 = ZERO
    BR

On a validated hit, compare messages. Exactly one of the hit arm and the
insert arm runs. Both are charged; stores and the gcount update of the
untaken arm are not issued:

    ADD  r3, r, 64
    LOAD m0, r3
    XOR  z4, m0, r0
    CMP  z4 = ZERO
    BR
    ADD  r4, r, 96
    LOAD m4s, r4
    XOR  z5, m4s, m4
    CMP  z5 = ZERO
    BR

If both message words match, the sample repeats an earlier message. Leave
the table unchanged and go to the loop epilogue. If the digest matches and
either message word differs, copy both message pairs into the output buffer
and go to verification. Do not insert the new sample.

If the level-2 check fails, insert. This arm is charged every sample:

    STORE f, gcount
    SHL  r, gcount, 7
    ADD  r, r, BASE_REC
    STORE r, suffix
    ADD  r2, r, 32
    STORE r2, block
    ADD  r3, r, 64
    STORE r3, r0
    ADD  r4, r, 96
    STORE r4, m4
    ADD  gcount, gcount, ONE

Loop epilogue, every sample:

    ADD  sample, sample, ONE
    CMP  sample < N
    BR

Counting these lines gives 18 + 7 + 18 + 10 + 11 + 3 = 67 primitives before
the compression unit. The per-sample ordinary budget is 80, leaving 13
primitives for a reload or an extra address add a reviewer may want. The
compression is not part of the 80.

Verification runs at most once. Rebuild each of the two blocks from its
stored (r0, m4), compress each from the IV, compare the two digests for
equality, and compare the two messages for inequality. That is two
compression units and fewer than 64 ordinary operations. If the check
succeeds, return the two 36-byte messages. If it fails, or if the loop ends
with no candidate, return FAIL. FAIL has no output relation.

## 6. A returned pair is a target collision

The two messages are 36-byte strings. Verification rejects equal messages.
Each digest compared in verification is the organizer one-block compression
of section 2, which is `digest(..., "sha256", 31)`. The table lookup is not
the output condition. Section 4 says a validated hit is an earlier sample
whose digest equals the current digest, so a message mismatch is a real
collision and the recomputation succeeds. The early-exit path is the only
success path.

## 7. Success probability

Let N = 2^256 be the number of digests and D = 2^288 the number of 36-byte
messages of section 2. For each digest z let p_z be the fraction of those
messages that hash to z. Independent uniform messages are independent samples
from p. This does not assume that p is uniform.

For a probability vector p, let e_q(p) be the sum of the products of
coordinates over all q-element subsets, with e_0 = 1 and e_q = 0 when q
exceeds the support. The probability that q samples are pairwise distinct is
q! e_q(p). On the simplex, e_q is maximized by the uniform vector. Indeed,
among maximizers, pick one of minimum sum of squares. If two coordinates
a and b differ and r is the rest,

    e_q(p) = e_q(r) + (a+b) e_(q-1)(r) + ab e_(q-2)(r),

with nonnegative coefficients. Replacing (a, b) by their average keeps a+b
and raises ab, so it does not decrease e_q, but it does decrease the sum of
squares. A maximizer therefore has a = b. The uniform vector is the unique
maximum, and it is the worst case for collisions.

Hence, for 2 <= q <= N, the probability of no repeated digest is at most

    q! binomial(N, q) / N^q = product_(j=0)^(q-1) (1 - j/N)
    <= exp(-q(q-1)/(2N)),

using 1 - u <= exp(-u). Let C be the event that some digest repeats and R
the event that some message repeats. The algorithm returns a collision on
C minus R: while messages are distinct every sample is inserted, and the
second sample with a given digest finds the first. A union bound gives
Pr(R) <= q(q-1)/(2D), because each pair of positions collides in the message
with probability 1/D.

Here q = n = 2^128, so

    q(q-1)/(2N) = (2^256 - 2^128) / 2^257 = 1/2 - 2^-129.

The no-collision probability is at most exp(-(1/2 - 2^-129))
= exp(-1/2) exp(2^-129). For y = 2^-129 < 1,

    exp(y) = sum y^k / k! < 1 + y + y^2,

because the tail after y^2 is at most y^2 (y/3 + y^2/12 + ...) < y^2.
The Taylor polynomial of exp(-1/2) through degree 10,

    s = 2253801941 / 3715891200,

ends on a positive term, and the terms decrease, so the alternating-series
remainder is negative and exp(-1/2) < s. Also

    s < 606531/1000000,

because 2253801941 * 1000000 = 2253801941000000 and
606531 * 3715891200 = 2253803205427200, and the second integer is larger by
1264427200. Therefore

    exp(-(1/2 - 2^-129)) < (606531/1000000) (1 + 2^-128)
    < 606531/1000000 + 2^-128,

and the collision probability is greater than

    1 - 606531/1000000 - 2^-128 = 393469/1000000 - 2^-128.

The repeated-message bound is

    q(q-1)/(2D) = (2^256 - 2^128) / 2^289 = 2^-33 - 2^-161 < 2^-33.

Subtracting it leaves more than 393469/1000000 - 2^-32 > 0.393. The declared
`success_probability` is 0.39, a lower bound under fresh coins, not an
equality and not a confidence score. The whole table is built on runs that
fail as well. There is no second amplification stage.

## 8. Resources

Ordinary operations per sample: at most 80. Samples: n. Setup loads the
eleven resident constants and clears three counters, at most 256 ordinary
operations. Verification adds at most 64 ordinary operations and 2
compressions. No other work exists.

    H = n + 2
    W = 80 n + 320
    C = 2140
    T = H + W/C = (2220 n + 4600) / 2140

With n = 2^128,

    T = (111/107) 2^128 (1 + delta),  delta = 4600 / (2220 * 2^128) < 2^-120.

Then T < 2^128.06 if and only if T^50 < 2^6403. A sufficient integer
condition is

    111^50 (2^114 + 1) < 8 * 107^50 * 2^114,

which implies (111/107)^50 (1 + 2^-114) < 8, and
(1 + 2^-120)^50 < 1 + 2^-114. Both the displayed comparison and
111^50 < 8 * 107^50 hold by direct arithmetic (the latter integer has 103
digits and is smaller than the right-hand side by a factor of about 1.276).
Hence T < 2^128.06. The submitted `time_log2` is 128.06. It is an upper
bound, not a claim that the minimum is 128.06.

Preprocessing is the 256-operation setup. Its cost is 256/2140 < 1, so
`preprocessing_log2 = 1` (an upper bound of 2 units) holds, and that setup
is already inside T.

Memory. sparse2 and sparse1 are 2^197 bytes each. Records are 2^135 bytes.
dense1 is 2^133 bytes. Code and the resident constants are under 2^20 bytes.
The sum is strictly less than 2^198 + 2^136 < 2^199. The declared
`memory_log2_bytes` is 199. Nothing is cleared by a hidden pass: each record
is written before it is read, and dirty cells are rejected by the section 4
test.

Advice is 0 bytes. `nonuniform_advice_log2_bytes = 0` is the schema's
one-byte upper bound on that empty string. No stored collision is an input.
The optional legacy `data_log2` field is omitted. Data movement is the loads
and stores inside W.

## 9. Non-claims

This is a generic birthday search. It uses no differential, no message
modification, and no property of SHA-256 beyond the definition in section 1.
It is not a 64-round break, and it is not an improvement on the published
31-step collision attacks of Mendel-Nad-Schlaeffer (EUROCRYPT 2013),
Li-Liu-Wang (EUROCRYPT 2024), or Li-Liu-Wang-Dong-Sun (ASIACRYPT 2024).
Those attacks are real published work. This package does not price them,
because a bound that cites a complexity without an explicit construction is
not a ledger, and the public slide-14 condition table is not reproduced
here. The improvement over the checked-in 136 is the removal of the 129-pass
sort and of the second compression: one block per message, and a
constant-time dictionary probe whose worst-case cost does not depend on the
hash.
