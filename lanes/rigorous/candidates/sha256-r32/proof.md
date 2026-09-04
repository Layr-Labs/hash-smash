# SHA-256, first 32 rounds: rigorous analytic candidate

This package is bound to `sha256-r32-rigorous`, target profile
`sha256-r32-prefix-v1`, and cost model `collision-frontier-v3`. It gives a
classical probabilistic algorithm with worst-case charged time at most `2^148`,
peak memory at most `2^138` bytes, and algorithmic success probability at least
`0.8`. It is a complete analytic candidate; no full-scale execution or concrete
collision certificate is claimed. All necessary arguments appear below.

The required identifier `sha256-r32-nominal-v2` names an organizer display
reference, not an established attack, qualified baseline, or security bound.
The claimed time-memory scalar is `148 + 138 = 286`. This candidate does not
claim an improvement over the nominal number 128 or a cryptanalytic advance.
Readiness is a request for review, not a claim of AI qualification or acceptance.

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

## 2. Finite algorithm and concrete storage

Let `q=2^129`, `N=2^256`, and `D=2^512`. A RAM word has 256 bits and 32 bytes.
Each record occupies exactly four consecutive RAM words `(d,u,v,0)`, where
d is the entire digest interpreted as a big-endian 256-bit integer. The last
word is initialized zero and merely gives a power-of-two stride. Reserve two
arrays A and B of q such records in disjoint contiguous address intervals.
There is no per-record pointer, allocator header, random seed, or hidden index.
The message itself remains in its two record words.

The following pseudocode specifies one run. `UniformWord` is the independent
uniform 256-bit random-word primitive in the stipulated computation model.
It is invoked afresh twice per record, across every iteration. It is not a
seeded PRNG, an experiment seed, or an assumed pseudorandom hash expansion.

```
for i = 0,...,q-1:
    u = UniformWord()
    v = UniformWord()
    A[i] = (H(u,v), u, v, 0)
width = 1
while width < q:
    for left = 0, 2*width, 4*width, ..., q-2*width:
        merge sorted runs A[left:left+width], A[left+width:left+2*width]
        into B[left:left+2*width], in lexicographic (d,u,v) order
    swap the A and B base-address variables
    width = 2*width
for i = 1,...,q-1:
    if A[i-1].d == A[i].d and (A[i-1].u,A[i-1].v) != (A[i].u,A[i].v):
        reconstruct these two 64-byte messages
        recompute both complete H values from the fixed IV and compare all bits
        if the messages are unequal and their recomputed digests are equal:
            return these two messages
        return FAIL
return FAIL
```

A merge has two source cursors with fixed exclusive end addresses and one
output cursor. At each emission, test exhaustion; if neither input is exhausted,
compare d, then u, then v until unequal, taking the left record on complete
equality. Copy all four words of the selected record to the output cursor.
Advance that source and the destination by four words. Re-test the ends at the
next emission. No sentinels or out-of-range reads are used. All loops are
iterative: no recursion or stack proportional to q. Because q is a power of
two, every pass consists of full paired runs and there are exactly 129 passes.

The initial arrays need no bulk zero initialization: every A record is fully
written before reading, and every destination record is fully overwritten on
each merge pass before the next pass reads it. Memory allocation means choosing
explicit RAM address intervals, not invoking an uncharged operating-system
allocator. The code/constants/scratch region is disjoint from both intervals.

All counters, run bounds and addresses fit a single 256-bit word. Fewer than
`2^133` word addresses are used, including arrays, fixed storage, and one-past
end pointers. Record offsets are `i << 2`, byte offsets if needed are `i << 7`,
and doubling a run width is one shift. This implementation needs no unit-cost
multiplication of arbitrary integers, variable-size integer arithmetic, or
unit-cost operation on the entire table.

The run always samples q messages and completes the sort, even on unsuccessful
coins. It then stops at the first distinct-message digest equality, or fails
after scanning the table. There are no restarts, success amplification outside
this run, or omitted failed trials. The final verification is attempted at most
once; with exact arithmetic it cannot fail for a pair selected by the scan.

## 3. Collision correctness and sorting completeness

Each record stores exactly its sampled message and its complete H value. A
merge preserves the multiset of records and produces the stated sorted order,
by induction on emitted records. Induction on the 129 passes therefore shows
the final A contains precisely the original records in lexicographic order.
Records with a given digest form a contiguous group. Within that group, equal
messages form contiguous subgroups. If at least two distinct messages occur
in a digest group, the boundary between two such subgroups is an adjacent pair
accepted by the scan. Repeated copies of one message alone do not qualify.
The independent recomputation is of both full padded hashes, and explicit
message inequality is required before returning. Every successful return thus
satisfies the exact profile's ordinary-collision relation. Conversely, the
algorithm returns whenever the sample contains any distinct-message collision.

## 4. Success probability for this fixed deterministic hash

Here the only probability space consists of the `2q` fresh independent RAM
random words. The sampled messages `X_1,...,X_q` are exactly iid uniform on the
D possible 64-byte strings. The hash is fixed, not randomly selected. Write
`p_y = |{x : H(x)=y}|/D`, for each of the N possible full digest values, allowing
zero entries. The outputs `Y_i=H(X_i)` are iid with distribution p because each
is a deterministic function of one independent input. No claim that p is
uniform is needed.

We prove the distribution-free birthday bound rather than assume it. For
`2 <= q <= N`, let `e_q(p)` be the elementary symmetric polynomial, the sum of
products of q distinct coordinates. Independence gives
`Pr[all Y_i distinct] = q! e_q(p)` by summing disjoint ordered outcomes.
On the compact probability simplex, e_q attains a maximum. Among its maximizers
choose one minimizing the sum of squared coordinates, which also exists by
compactness. If two coordinates a,b differ, hold their sum and every other
coordinate fixed. Expansion by how many of a,b a monomial uses gives

`e_q(p) = A + (a+b) B + ab C`,

where `A=e_q(rest)`, `B=e_(q-1)(rest)`, and `C=e_(q-2)(rest) >= 0`, with
`e_0=1` and impossible degrees zero. Replacing a,b by their common average
increases ab. It cannot decrease e_q; maximality means the new vector is still
a maximizer, while its squared-coordinate sum strictly decreases. This
contradicts the choice of maximizer. Hence a maximizing vector is uniform,
and for every output distribution

```
Pr[all Y_i distinct]
  <= q! binom(N,q) N^(-q)
   = product_{j=0}^{q-1} (1-j/N)
  <= exp(-q(q-1)/(2N))
   = exp(-(2-2^(-128))).
```

The exponential inequality follows termwise from `1-z <= exp(-z)` for
`z >= 0`. Its use here does not assume pairwise events are independent.
Separately, any particular pair of sampled inputs is equal with probability
`1/D`; the union bound, which also requires no event independence, gives

`Pr[some input repeats] <= binom(q,2)/D < 2^(-255)`.

Let E be the event that some outputs agree, and R the event that some inputs
repeat. On `E and not R`, a distinct-message collision exists and the algorithm
returns one by Section 3. (There can also be success on R.) Consequently

`Pr[success] >= 1 - exp(-(2-2^(-128))) - 2^(-255) > 0.8`.

A purely rational margin verifies the last numerical bound. The exponent
`2-2^(-128)` exceeds `7/4`, and
`exp(7/4) > sum_{k=0}^4 (7/4)^k/k! = 34193/6144 > 16/3`.
Thus the failure bound is less than `3/16 + 2^(-255)`. The success bound exceeds
`13/16 - 2^(-255) > 4/5`, since `13/16 - 4/5 = 1/80 > 2^(-255)`.
The declared 0.8 is therefore a conservative algorithmic lower bound for this
fixed SHA-256 target, not confidence in the proof or in an AI review.

## 5. Charged time: a deliberately loose concrete instruction ledger

Every number in this section counts unit operations in the organizer's 256-bit
RAM, including a selected C32 compression at one unit. Loads, stores, random
words, arithmetic, masks, shifts, comparisons, and branches each count. Fixed
register transfers are charged as load/store operations rather than free moves.
Constants can be read from fixed RAM storage; their accesses are included.
A fixed-register transfer or arithmetic instruction with operands/results in
RAM expands to at most eight primitive operations (at most two operand
loads, the operation, a result store, and four instruction-word fetches). The budgets below include this conservative expansion where relevant.

A call to H requires exactly two C32 operations. An explicit wrapper loads the
eight IV words, places u,v and the two constant padding words in block registers,
passes the first feed-forward state to the second compression, and packs the
eight final 32-bit words by shifts and ORs into a digest word. Reserving 256
wrapper instructions, each at most eight operations, plus two compression
operations is below 4096 operations per H. This covers block loading/unpacking
if the primitive uses sixteen 32-bit input registers: at most 32 input fields
are extracted using two shifts/masks or fewer each. Padding is fixed and its
original length is 512 bits on every invocation. C32 itself is the selected
unit-cost primitive explicitly allowed by the model, with Section 1 specifying
its complete semantics. No separate full-hash unit-cost primitive is assumed.

The following implementation budgets are sufficient; all are upper bounds,
not measured costs or asymptotic notation:

| Phase or loop component | Upper bound and justification |
| --- | --- |
| Fixed initialization/preprocessing | `2^20` operations: load/initialize the finite program, IV/constants, padding and scratch described in Section 6; set array bases, q and counters. No offline search. |
| Sampling and storing one record | `8192` operations: two random-word draws, one H call below 4096, four record stores, and fewer than 128 remaining instructions of at most eight operations for word transfers, pointers, and loop control. |
| One merge emission | `1024` operations: at most 16 exhaustion-test/control instructions, 16 field-load/address instructions, 16 lexicographic comparison/branch instructions, 24 instructions to load/address/store four copied fields, 16 cursor/loop updates, and 16 extra transfers; at most 104 instructions, each expanded to at most eight operations, gives 832 with 192 spare. |
| One merge's setup and finish | `1024` operations: fewer than 128 instructions of at most eight operations to load bases, form boundaries by shifts/additions, initialize cursors and advance outer-loop position. |
| One sort pass | `2048q + 1024` operations: q emissions and at most q merges, with 1024 operations for swapping base variables, doubling width and pass control. |
| One adjacent scan position | `1024` operations: up to six field loads with addressing, full-word digest equality, two message-word comparisons, boolean/branch operations and cursor control; fewer than 128 instructions at eight operations. |
| Final verification/output | `2^16` operations total: two H calls, message/digest comparisons, copying four message words and serialization to at most 128 output bytes; even byte-at-a-time shifts, masks, stores and loop control fit. |

There is no comparison of more than three words hidden in the merge count.
When an input run is exhausted, the same emission budget copies from the other
run; no remainder-copy work is omitted. Self-assignments or constant increments
can be expanded with the same charged primitives. Table reads and writes are
counted on every pass. Instruction storage is charged below, independently of
these time bounds. Choosing direct conditional-branch targets needs no indirect
comparison oracle or uncharged sorting/library routine.

There are q samples, exactly 129 merge passes, at most q-1 scan positions, and
at most one final verification. Thus the total, on every choice of coins, is

```
T <= 2^20 + 8192q + 129(2048q+1024) + 1024q + 2^16
   = 273408q + 1246208
   < 2^19 q
   = 2^148.
```

(The constant is `1048576 + 132096 + 65536 = 1246208`.) Every sample, failure,
random draw, lookup, verification, construction and preprocessing operation is
inside T. There is one finite run, so there are no restart costs or expected-
time truncation assumptions. `time_log2=148` is a worst-case upper-bound
exponent expressed in the cost model's `target-compressions` unit.

## 6. Memory, code, data, and advice

Two q-record arrays, each four 32-byte words per record, occupy exactly
`2 * q * 4 * 32 = 256q = 2^137` bytes. This includes every digest, every retained
random word, every message, and stride padding, throughout the merge sort.
The unused former-source array stays allocated during verification and output.
There is no separate list of messages or index array and no uncharged external
storage. The random primitive returns a fresh word directly; no coin tape or
sampled seeds are retained outside the record fields.

Reserve additionally `2^21` bytes for all uniform code, constants, scratch,
program counters, register spills, output and fixed state. One concrete encoding
budget is at most 2048 RAM instructions, each encoded in at most four 256-bit
words (opcode, up to two operands, destination/branch target), i.e. `2^18` bytes.
The instruction sequence uses loops over the pseudocode, not unrolling q or
129 passes. The H wrapper has at most 256 instructions; merge and its setup/control
have fewer than 256; sampling, scan, initialization and byte-output loops
combined have fewer than 512. Even splitting every listed compound step into
two instructions fits the 2048-instruction envelope. Fixed constants, including
all 32 round constants and the eight IV words even though C32 is primitive,
fit in 256 RAM words (8192 bytes). At most 1024 further words (32768 bytes)
are needed for counters, argument/result staging, the two message buffers,
possible 32-word schedule scratch, and verification state. These conservative
subtotals fit well inside `2^21` bytes. There is no recursion, input-dependent
code, stored collision, omitted table advice, or precomputed target-specific
search result.

Accordingly peak storage obeys

`M <= 256q + 2^21 < 512q = 2^138 bytes`.

This is why `memory_log2_bytes=138` counts actual bytes, rather than the
collision exponent 128 or a nominal constant-memory value. Every address and
integer needed by this storage plan fits within the model's word width.

`preprocessing_log2=20` bounds fixed preprocessing in the same time units as T,
and those `2^20` units are already included in T. Array writes performed during
sampling and sorting are also already charged; there is no prior table build.
No nonuniform advice is used, so its actual size is zero bytes. The schema
requires a finite nonnegative logarithm; `nonuniform_advice_log2_bytes=0`
means a conservative upper bound of one byte, not the literal logarithm of
zero and not permission to hide the uniform code. Uniform code storage is
charged in M and its initialization in T.

For `data_log2=137`, the data unit is bytes of complete padded hash inputs
processed. There are q original 64-byte sampled messages and at most two
verification calls. Including both 64-byte blocks in every hash gives at most
`128(q+2) < 2^137` bytes. Original-message bytes, even counting the verification
re-reads, are `64(q+2) < 2^136`; there is no external chosen/challenge data
requirement. If data is instead recorded as the number of message evaluations,
`q+2 < 2^130 < 2^137`, so the declared exponent is also conservative in that
convention. Padding, construction and both compressions per evaluation are
already charged in T. The data field does not add an uncharged oracle or
remove stored messages from M.

## 7. Premises, evidence, and limitations

`heuristics` is empty because the argument depends only on the exact selected
hash definition, the stipulated independent-random-word RAM primitive, the
proved arbitrary-distribution inequality, and deterministic bookkeeping. It
assumes no ideal-hash behavior, output balance, differential-trail independence,
seed expansion, empirical extrapolation, or favorable cryptanalytic structure.
Independent coins are an explicit resource of the model and are paid for twice
per sample; independence of output variables follows mathematically from that
resource even for a constant or heavily biased fixed H. Input repeats were
separately charged in the probability bound rather than counted as collisions.

The certificate manifest is valid and empty. No experiment manifest or program
is supplied because no empirical premise is used. This analysis does not claim
full-scale practical feasibility, measured wall time, or a known message-pair
collision. Abstract resources are enormous but fit the stated RAM and message
domains. A reduced toy experiment would not strengthen the distribution-free
full-size proof and is not substituted for it. The rigorous and exploratory
packages require their own lane-bound organizer reviews; one lane's readiness
or score is not evidence that the other has qualified. AI review outcomes do
not constitute formal proof certification or human acceptance.
