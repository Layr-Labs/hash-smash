# Grouped partial-evaluation birthday search on 2-round BLAKE3 (constant-factor refinement)

## 0. Summary

Exploratory package for blake3-r2-prefix-v1 under collision-frontier-v5 (C = 430).

| quantity | value |
| --- | --- |
| messages N | 2^128 one-block root messages, 2^96 groups x 2^32 |
| word operations per full 7-message batch, counted (worst case) | 420 (227 body + 101 extraction/keys + 84 table + 7 record counters + 1 packed-counter update), plus loop control |
| word operations per batch, **charged** | **448** (more than 27 spare operations) |
| total charged time T | < 0.14885393 * 2^128 < 2^125.25197 |
| claimed `time_log2` | **125.252** (bound rounded up) |
| success probability | 0.39 under heuristic H1 (model value > 0.39343) |
| memory (unscored) | every address below 2^161 words = 2^166 bytes; reported as 167; < 2^134.001 bytes written |
| preprocessing / advice | 0 / 0 |

**Credit.** This package directly builds on winglock's public ticket 3022205
(`time_log2=127.252`), including its grouped evaluator, sparse table, experiments,
proof structure and refinement of jaazinn's accepted ticket 0a5b7ae8
(`time_log2=127.481`). The new contribution is the delayed-reduction program in
Section 4, followed here by a seven-lane SWAR program that evaluates seven
messages in one 256-bit word while preserving the exact message set, success
analysis and evidence protocol. Both winglock and jaazinn are co-authors.

This is a generic birthday search with a smaller constant factor. It is not a
differential or algebraic attack on BLAKE3, and it does not claim an improvement
over the nominal reference 128: the saving comes only from not recomputing
work that is identical within a group and not computing output words the key
does not need (charging a full compression per message would give about
2^128.07). The time bound is a worst-case cap on every run.
Every output is re-hashed with two reference compressions before it is returned.
Only the success probability uses the heuristic H1.

## 1. Target and message set

H is unkeyed BLAKE3-256 with prefix rounds 0-1 (verifier/blake3.py:blake3 with
rounds = 2). Every evaluated message is exactly 64 bytes, i.e. one root
compression with chaining value IV, counter 0, block length 64 and flags
CHUNK_START|CHUNK_END|ROOT = 11. Its words m0..m15 are little-endian. The state
is v = (IV[0..7], IV[0..3], 0, 0, 64, 11). G(a,b,c,d,x,y) is

    v[a]=v[a]+v[b]+x; v[d]=ROR(v[d]^v[a],16); v[c]=v[c]+v[d]; v[b]=ROR(v[b]^v[c],12)
    v[a]=v[a]+v[b]+y; v[d]=ROR(v[d]^v[a],8);  v[c]=v[c]+v[d]; v[b]=ROR(v[b]^v[c],7)

with additions mod 2^32. A round applies G to columns (0,4,8,12), (1,5,9,13),
(2,6,10,14), (3,7,11,15) with schedule pairs (s0,s1)..(s6,s7), and then to
diagonals (0,5,10,15), (1,6,11,12), (2,7,8,13), (3,4,9,14) with (s8,s9)..(s14,s15).
Round 1 uses s = m. Round 2 uses s_i = m[P[i]] with
P = (2,6,3,10,7,0,4,13,1,11,12,5,9,14,15,8). The digest is o_i = v[i] ^ v[i+8]
for i = 0..7.

**Message set.** For each group g = 0..2^96-1 the algorithm draws two independent
uniform 256-bit words U0_g and U1_g. They give m0..m7 (U0_g) and m8..m14 (the low
224 bits of U1_g). Write

    a3h, b4h = v[3], v[4] after the first half of round 1's last call G(3,4,9,14,m14,m15),
    S_g = (a3h + b4h) mod 2^32       (a function of m0..m14 only).

The group enumerates t = 0..2^32-1 and uses m15 = (t - S_g) mod 2^32. Then t is
exactly the round-1 state word a3' = (a3h + b4h + m15) mod 2^32 after that addition.

**Lemma 1 (bijection).** For fixed m0..m14, t -> m15 = (t - S_g) mod 2^32 is a
bijection of Z/2^32. So group g contains exactly the 2^32 messages
(m0..m14, m15) with m15 = 0..2^32-1, the same set jaazinn's package enumerates.
Messages of the same group are pairwise distinct. Messages of different groups
are distinct unless the groups have identical m0..m14 (event F3, Section 6).

## 2. Dependency analysis and group constants

Round 1 reads m15 only as y in its last call G(3,4,9,14,m14,m15). Round 2 reads
m15 only as x = s14 in its last call G(3,4,9,14,s14,s15), with s15 = m8. For fixed
m0..m14:

- The four round-1 column calls, the first three diagonal calls and the first
  half of the last one are group constants. After round 1, only v3 = t, v4, v9
  and v14 depend on t.
- Each round-2 column call receives exactly one varying word, in a different
  role in each call: v4 (b role), v9 (c role), v14 (d role) and v3 (a role).
  Their invariant prefixes are group constants: v0+s0 (b role);
  a1h = v1+v5+s2, d13h = ROR(v13^a1h,16) and a1h+s3 (c role);
  a2h = v2+v6+s4 and a2h+s5 (d role); v7+s6 (a role).
- The four round-2 diagonal calls and the output words are recomputed per message.

The hot loop keeps 27 group constants in registers. Names in capitals:
D14, C9, B4 (v14, v9, v4 after the first half of the last round-1 call);
NS = (-S_g) mod 2^32; A0x = v0+s0, D12, C8, s1; D13h, B5, A1y = a1h+s3;
A2h, C10, B6, A2y = a2h+s5; B7x = v7+s6, D15, C11, B7, s7; s8..s13; s15.
Every sum is reduced mod 2^32.

**Group setup count** (itemized; charged 1024 operations per group):
draw U0, U1 (2); U1 = U1 & (2^224-1) (1); unpack m0..m14 (m0 = U0 & M is 1,
each further word (U >> 32i) & M is 2: 28); the 27 constants and S (244, counted
by the shipped `--selftest`: every operation with a message-dependent operand;
operations on IV words alone are program constants); the remaining scalar setup
costs 14, giving the prior scalar total 289. Broadcasting one constant takes
seven operations: three shift/OR doubling steps produce eight copies and an AND
removes the truncated eighth slot. Thus 27 broadcasts cost 189. One tail mask
costs 1. Total 479 < 1024.

## 3. Algorithm and memory layout

Registers and constants: M = 2^32-1; MC = (2^128-1) << 32 (bits 32..159);
SB = 2^160 (sparse-array base); INC = 2^32. Memory is never initialised.
All addresses are word addresses below 2^161:

| region | addresses |
| --- | --- |
| dense array | j * 2^32 for j < 2^128 (below 2^160) |
| group records U0_g, U1_g, S_g | 4g+1, 4g+2, 4g+3 (below 2^98) |
| scalars: group counter, VC | 2^99 + 1, 2^99 + 3 |
| output buffer (two 64-byte messages) | 2^99 + 5, 7, 9, 11 |
| program code (< 2^17 instructions) | odd addresses in [2^100, 2^100 + 2^18) |
| sparse array | SB + K for K < 2^160, i.e. [2^160, 2^161) |

The regions are pairwise disjoint: dense addresses are multiples of 2^32;
record addresses are 1, 2 or 3 mod 4; scalar, output and code addresses are odd
and at least 2^99 > 2^98; scalars and outputs are below 2^100; only sparse
addresses reach 2^160. In particular no record, scalar or code word ever sits
at a dense address, which Lemma 4 needs.

1. Set CC = 0 (the next dense address, i.e. 2^32 times the number of records)
   and store VC = 0.
2. For g = 0..2^96-1: group setup (Section 2), storing U0, U1, S at 4g+1..4g+3.
3. Inner loop: a straight-line block evaluates seven consecutive t values in
   parallel. It runs the packed body (227), extracts seven scalar 160-bit keys
   (101), performs seven table steps (at most 84), advances scalar R seven times
   (7), and advances packed T (1): 420 operations. Straight-line code
   is unrolled 64 batches at a time; its compare/branch/counter overhead is
   covered by the 28-operation slack in the 448 charge. There are
   q=floor(2^32/7)=613566756 full batches and one final batch whose first four
   lanes cover the remainder. The final batch is charged the full 448 operations.
4. MATCH (Section 5). Each of the 448 table copies in an unrolled block has its
   own copy of the MATCH
   handler. On success it writes both messages to the output buffer and halts.
   Otherwise it branches back to its own copy's `R = R + 1`, so no indirect
   jump is needed. Factoring the shared packed body and key extraction from the
   seven table copies, an unrolled block has fewer than
   64*(227+101+7*(12+1+120)) = 80576 < 2^17 instructions.
5. After the last group, halt with failure.

The program halts after at most N = 2^128 messages and at most 2^110
verifications. Section 8 prices this worst case.

## 4. Seven-message SWAR program and its exact count

The counting convention is that of scripts/reference_operation_costs.py: every
operation with a batch-dependent operand is counted, including one whose other
operand is constant. One 256-bit word holds seven 32-bit payloads at offsets
0,36,...,216, with four guard bits after each payload. The highest slot ends at
bit 251.

For r in {7,8,12,16}, let A_r select the low 32-r bits of every payload and B_r
select its high r result positions. A lane-wise rotate uses five operations:

    PROR(z,r) = ((z >> r) & A_r) | ((z << (32-r)) & B_r).

These masks discard guard bits and bits shifted across slot boundaries. The
packed body deliberately leaves additions unreduced between rotations. Tracking
every live sum in units of B=2^32 gives strict maxima

    a0 < 8B, a1 < 6B, a2 < 6B, a3 < 9B,
    c8 < 5B, c9 < 6B, c10 < 5B, c11 < 5B.

The b and d words are normalized by each packed rotation. Thus every live word
is below 2^36 in each slot and no carry crosses a slot boundary. XOR preserves
the layout. Induction through the shipped straight-line program proves that
each payload equals the scalar evaluator at its corresponding t. No native
narrow or SIMD operation is assumed.

The exact itemization is:

| packed-body component | operations |
| --- | ---: |
| 42 additions | 42 |
| 30 input XORs and 30 five-operation rotations | 180 |
| five output XORs | 5 |
| **seven-lane body** | **227** |
| derive four key-position masks, extract and pack seven keys | 101 |
| seven sparse-set table steps, worst path | 84 |
| advance scalar record R seven times | 7 |
| advance packed T by broadcast(7) | 1 |
| **counted full batch** | **420** |

For lane zero, direct key extraction takes five ANDs, four shifts and four ORs:
13 operations. Each later lane takes five ANDs, five shifts and four ORs: 14.
Deriving the four masks at scalar-key offsets 32,64,96,128 takes four shifts, so
the total is 13+6*14+4=101. The shipped counting-word evaluator reports
`(body,extraction)=(227,101)` and checks every extracted key against the
independent reference. It retains the scalar `(202,8)` test and evidence-only
eight-word comparison as additional checks.

**Charge.** We charge 448 operations per full or partial batch. This covers 420
counted operations, fewer than 3/64 operations of unrolled-loop control, and
more than 27.95 spare operations. The partial four-message batch at each group
end is also charged 448.

**Lemma 2 (T lanes).** Packed T has lane j equal to t+j and enters the body in
the three scalar positions formerly occupied by t. Lemma 1 gives
`(t+j+NS) mod 2^32 = m15`, while each following packed rotation discards the
guard bits. Adding broadcast(7) advances every lane to the next batch without a
cross-slot carry. Scalar R=t+g*2^160 advances beside T and is used only for table
records and decoding. At the final batch, the first four lanes cover
2^32-4,...,2^32-1; the three unused lanes are ignored. One mask of T at that
boundary, charged to group setup, keeps even those unused lanes below B.

**Lemma 3 (key).** Extraction masks the selected payload of each packed output,
so its five scalar words are below 2^32. Therefore
K = o0 + 2^32 o1 + 2^64 o2 + 2^96 o3 + 2^128 o5 < 2^160, with the five fields
disjoint. Two messages with the same full digest have the same K.

**Why exactly these words.** o0..o3 = a ^ c need every final a and c word. Each
final c is c + d, so every final d is needed too. Only the final b rotations
(5 operations each) are optional, plus the XORs and packing of words not used.
We keep o5 = b5 ^ d13, so G(0,5,10,15) is complete. The other three final b
rotations, three output XORs and three shift/OR pairs are skipped: 18 body
operations and 6 key operations. 160 key bits are more than enough (Section 6).

**Control flow and registers.** The code is three-address: each listed
operation writes its result to its destination register, so no register moves
occur. Within a batch, control falls through from one line to the next; the only
branches are the two table tests (Section 5), which are counted. The machine
has 64 registers. The hot loop needs 27 broadcast group constants, 16 state
words, 2 temporaries, 8 rotation masks, T, scalar R, CC, M, MC, SB, INC and one
loop/end word: 62 registers. The five target key masks and table temporaries
reuse state registers that are dead after the body. Shift amounts are instruction
immediates. The group counter and VC live in memory; only group setup and MATCH
access them, within their budgets.

## 5. Sparse-set collision table

The sparse array is at SB + K, one word for each possible 160-bit key. The dense
array is at addresses j*2^32, one entry per record. Both are never initialised.
A record word is R | CC.

    sa = K | SB                       1   (K < 2^160 = SB)
    w  = load [sa]                    1
    p  = w & MC                       1
    f  = (p < CC); branch !f -> INS   2
    q  = load [p]                     1
    f  = (q == K); branch f -> MATCH  2
    INS: store [sa] <- R | CC         2   (or + store)
         store [CC] <- K              1
         CC = CC + INC                1
                                      12 on the path through both tests then
                                      INS; 9 on the early INS path; 8 to MATCH

INS is the next instruction after the second test, so the fall-through needs no
jump; after INS control falls through to `R = R + 1`.

**Invariant.** After j insertions, CC = j*2^32. For i < j, dense[i*2^32] holds the
key k_i of the i-th inserted record. sparse[SB + k_i] = R_i | i*2^32 and is never
written again. Other sparse words hold arbitrary values.

**Lemma 4 (lookup).** The step reaches MATCH iff K was inserted earlier, and then
w is that record's word.
If K = k_i, then w = R_i | i*2^32. Because R_i has no bits in 32..159 and
i < 2^128, p = i*2^32 < CC and dense[p] = k_i = K, so the step goes to MATCH.
If K was never inserted and p >= CC, the step inserts. If p < CC, then p is a
multiple of 2^32 (MC has only bits 32..159), so p = i*2^32 for some i < j, an
address that holds only dense entries (Section 3), and dense[p] = k_i differs
from K. So the step inserts. Garbage in a sparse word can never produce a MATCH.

**Lemma 5 (no displacement).** By Lemma 4, INS runs only for a key not yet
inserted. A record, once written, is never overwritten. The record for key k is
always the first message that had key k.

**Lemma 6 (decoding).** In w = R_i | i*2^32 (i*2^32 < 2^160), the fields are
disjoint, so t_i = w & M and g_i = w >> 160.

**MATCH handler** (itemized; charged 2 units plus 1024 operations per entry):

1. VC: load, add, store, compare with 2^110, branch; if VC > 2^110, halt with
   failure (5).
2. Earlier message: t' = w & M, g' = w >> 160 (2); addresses 4g'+1..4g'+3 (4);
   three loads (3); unpack m0..m14 (28); m15' = (t' - S') & M (2). Total 39.
3. Current message: g = R >> 160 and its record addresses (5); three loads (3);
   unpack (28); m15 = (R + NS) & M (2). Total 38.
4. Distinctness of (U0, U1, m15) against (U0', U1', m15'): 3 compares, 2 ORs,
   1 branch (6).
5. Two reference compressions (2 units). Equality of all eight digest words:
   8 XORs, 7 ORs, 1 compare, 1 branch (17).
6. On equality: form the 4 output words and store them at the output buffer,
   then halt (at most 9). Otherwise branch back to the copy's `R = R + 1` (1);
   the current message is not inserted.

At most 115 operations < 1024.

## 6. Correctness and success probability

**Correctness (no heuristic).** Any output pair was checked in MATCH steps 4-5
to consist of two distinct 64-byte messages with equal complete blake3-r2
digests. It is a valid collision.

**Failure events.**

- F3: two groups have identical m0..m14.
- F1: the N messages contain no full-digest collision.
- F2': some message x has a full-digest partner z processed before it, but the
  first message y with K_y = K_x has a different digest from x.
- Fcap: more than 2^110 MATCH entries.

**Lemma 7.** If none of F1, F2', F3 and Fcap occurs, the algorithm outputs a
collision.
Proof. By not F3 and Lemma 1, all messages are distinct. By not F1, let x be the
first message in processing order that has a full-digest partner z processed
earlier. Assume the algorithm has not already halted with an output. When x is
processed, Lemma 3 gives K_z = K_x, so some record holds key K_x. By Lemma 5,
that record belongs to the first message y with K_y = K_x. By not F2', y has the
same digest as x. By not Fcap, the verification runs, and it outputs (y, x).

**Bounds.**

- Pr[F3] < C(2^96, 2) * 2^-480 < 2^-289, exactly, because the words are
  independent and uniform.
- Under H1 (Section 7), treat the N digests as independent uniform 256-bit
  values. Then:
  - Pr[F1] <= prod_{i<N} (1 - i/2^256) <= exp(-N(N-1)/2^257)
    = exp(-(1 - 2^-128)/2) < 0.6065307.
  - F2' needs distinct x, y, z with D_x = D_z and K_y = K_x. There are fewer than
    N^3/2 such triples, each with probability 2^-256 * 2^-160. So
    Pr[F2'] < 2^383 * 2^-416 = 2^-33.
  - Each MATCH entry belongs to a distinct pair (y, x) of distinct messages
    with equal 160-bit keys (x is the current message, so the pairs differ).
    E[#pairs] = C(N,2) * 2^-160 < 2^95, so by Markov Pr[Fcap] <= 2^95/2^110 = 2^-15.

Success > 1 - 0.6065307 - 2^-33 - 2^-15 - 2^-289 > **0.39343**. The claim is
0.39. Like jaazinn's package, it keeps an allowance of about 0.0034 for deviation
of the real digests from the model.

**Partial justification of the model.** Within-group pairs are a 2^-96
fraction of all pairs. A cross-group pair with the same t collides with
probability sum_d p_t(d)^2 >= 2^-256 (Cauchy-Schwarz over the uniform group
words). H1 asserts the rest.

## 7. Heuristic H1 and declared experiments

**H1 (grouped digests behave like independent uniform values).** For the
message set of Section 1, the complete 2-round BLAKE3 digests of the 2^128
messages, and their 160-bit keys (o0..o3, o5), have failure probability for
events F1, F2' and Fcap at most the value computed for independent uniform
256-bit values, up to a negligible amount.

It is score-critical for success_probability only. The time cap and output
validity do not use it. It is the same premise as jaazinn's H1. Our key uses
o0..o3 and o5 instead of all eight words, so the key-based events also need the
160-bit projection to behave uniformly. Every full-digest event is unchanged.

**Experiments** (experiments/manifest.json, program experiments/b3r2_grouped.py;
declared for organizer execution as python-message-pairs-v1). Each trial runs
the algorithm of Section 3 scaled to N_t = 2^10 messages. Digest words come only
from the seven-lane grouped evaluator of Section 4, run with the t-enumeration;
scalar R = t + g*2^160 accompanies it for table records. The scaled key is a 20-bit event mask applied to the key. The
table step is the operation-counting function `table_step`, a literal transcript
of Section 5, over a memory whose unwritten words are adversarial garbage: about
half of them carry, in bits 32..159, the address of a written dense entry, so the
stale-pointer case of Lemma 4 is exercised in every trial. A key match is
re-hashed with an independent reference compression before the pair is
returned. The organizer recomputes the masked event with the trusted digest.
The scaled analogue keeps N_t^2 / 2^20 = 1 = N^2 / 2^256.

- `b3r2-grouped-spread`: 32 groups x t = 0..31. Mask: 4 bits in each of
  o0, o1, o2, o3, o5.
- `b3r2-single-group`: 1 group x t = 0..1023, the most structured case.
  A different mask, again 4 bits in each of o0, o1, o2, o3, o5.
- `b3r2-grouped-fullword`: 32 groups x t = 0..31, with the evaluator in its
  evidence-only full mode, which also performs the three skipped final b
  rotations and outputs o0..o7. Mask: 3 bits in each of o0..o3 and 2 bits in
  each of o4..o7, applied to the whole digest. This tests o4, o6 and o7, which
  the counted hot path never computes. The counted program is unchanged.

The uniform model value for 1024 values and a 20-bit event is
1 - prod_{i<1024}(1 - i/2^20) = 0.39327 (256 trials: 100.7, sd 7.8).

Every counted-path trial also reports untrusted observations: the counted body
and extraction operations of its first seven-message batch, the minimum and maximum counted table step,
the number of verifications and the number of stale garbage pointers read.

**Our local replay of the organizer runner** (experiments.runner.run_experiments
with the track's config_sha256, seed hashsmash-public-seed-v1, 256 trials, the
Docker executor replaced by a local Python subprocess because Docker was not
available to us; these are not organizer results):

- spread 107/256, single group 98/256, fullword 92/256 (model 100.7, sd 7.8);
- no repeated pairs; at most 1 verification per trial;
- observations in every counted-path trial: packed body 227, extraction 101,
  table steps between 8 or 9 and
  12, about 435 stale garbage pointers per trial;
- two byte-identical stdout runs per experiment, 1.3-1.6 s each.

**Our additional runs (our seeds).** With 4096 trials per row, the model
predicts 1610.8 successes (sd 31) and 2046 masked pairs:

| layout | mask | successes | masked pairs |
| --- | --- | --- | --- |
| spread | spread mask | 1629 | 2101 |
| spread | single-group mask | 1600 | 2020 |
| single | single-group mask | 1615 | 2053 |
| single | spread mask | 1586 | 2057 |
| spread, full mode | fullword mask | 1605 | - |
| single, full mode | fullword mask | 1666 (+1.8 sd) | - |

We extended the last row by 12288 further trials (4816 successes). In total it
gave 6482/16384, against a model of 6443.3 (sd 62.5), i.e. +0.6 sd.
With 32-bit masks inside o0..o3, o5 and N_t = 2^16, 200 seeds per row (model
78.7 successes, sd 6.9; 100 masked pairs): 16 groups x 4096 with 8 bits in each
of o0..o3 gave 74 (86 pairs); 1 group x 65536 on all of o3 gave 78 (98); on all
of o5 gave 81 (110). All are within 1.5 sd.

**Extrapolation and limitations.** The experiments test 20-bit (and our
32-bit) projections with 2^10 (2^16) messages; the claim applies the model to
256-bit digests, 160-bit keys and 2^128 messages. Projections cannot detect
structure visible only in full-width equality. Organizer seeds are public. Each
256-trial experiment resolves success only to about +-0.03, while the allowance
above 0.39 is 0.0034 and is not statistically certified.

## 8. Total time, memory and claim fields

Let q=floor(2^32/7)=613566756. There are 2^96(q+1) charged batches, including
one four-message tail batch per group. Each costs 448 operations. Per group:
at most 1024 operations. Per MATCH entry: 2 units plus at most
1024 operations, for at most 2^110 entries; the (2^110+1)-th entry halts after
step 1. Constant setup: below 1 unit.

    T <= 2^96 * (q+1) * 448/430
         + 2^96 * 1024/430 + 2^110 * (2 + 1024/430) + 1
      <  0.14885393 * 2^128  <  2^125.25197

The claim is time_log2 = 125.252, the bound rounded up.

**Sensitivity** (charged operations per batch; log2 T rounded up):

| charge | 420 + 3/64 (no spare) | 421 | 424 | **448 (claimed)** | 480 | 560 |
| --- | --- | --- | --- | --- | --- | --- |
| log2 T | 125.1591 | 125.1624 | 125.1726 | 125.2520 | 125.3515 | 125.5739 |

All of them are below the current best of 127.481.

**Memory** (unscored, reported).

- Every address used, including code, is below 2^161 words (Section 3), so the
  span is at most 2^161 * 32 = 2^166 bytes. We report memory_log2_bytes = 167,
  rounded up for caution.
- The regions used are: sparse array 2^160 words (2^128 written); dense array
  2^128 entries spread over 2^160 - 2^32 + 1 words; group records 3 * 2^96 words
  spread over 2^98 words; 6 scalar/output words; code below 2^17 words.
- At most 2^129 + 3 * 2^96 + 2^17 + 6 words are ever written:
  less than 2^134.001 bytes.
- A variant that indexes by K >> 20 (span about 2^146 bytes, like jaazinn's)
  costs one more counted operation and adds Pr[F2] <= 2^-12. It is not used.

**Other claim fields.** preprocessing_log2 = 0 (no precomputation; the constant
setup is below 1 unit). Nonuniform advice is 0. success_probability = 0.39.

## 9. Relation to jaazinn's accepted package (ticket 0a5b7ae8)

The following are the same as jaazinn's: the message set (groups of 2^32 sharing
uniform m0..m14, all m15 values), the dependency analysis, the group setup idea,
the use of a never-initialised sparse-set (Briggs-Torczon) table, verification
by 2 reference compressions, the premise of H1, and the shape of the scaled
experiments.

The scalar refinement first lowers jaazinn's counted per-message cost from 286
to 223. The SWAR step then evaluates seven such messages with a 227-operation
body and 101-operation key extraction; the full charged batch is 448, or 64
operations per message before the negligible group-tail correction.

| change | ops |
| --- | --- |
| enumerate t = a3' instead of m15: round-1 tail 12 instead of 14; last diagonal's first add 4 instead of 3 | -1 |
| key from o0..o3, o5 only: skip 3 final b rotations and 3 output XORs | -18 body |
| pack 5 words instead of 8 | -6 key |
| table indexed by the whole 160-bit key; dense array at base 0 with stride 2^32 so that CC is both the dense address and the record field; record = R | CC. This removes the index shift, base adds and discard branch, and no slot is ever displaced | -9 |
| single register R = t + g*2^160: counter, t and record id in one add per message | -3 |
| carry redundant words and delay 31 modular reductions until five key outputs | -26 |
| pack seven executions into 36-bit slots with explicit guard bounds and packed rotations | amortizes body and extraction across seven messages |

Every number is exact under the convention of Section 4 and is reproduced by the
shipped `--selftest` (body and key) and by `table_step` (table). Under the same
convention a whole compression is 16 * 30 + 16 = 496 operations, as in jaazinn's
note. The program never evaluates a whole compression per message: 250 of those
496 operations are group-invariant, and 18 are skipped.

**Not used:** dropping the p < CC test, which needs initialised memory.

## Appendix A. Mechanical checks

**Shipped** (`python3 experiments/b3r2_grouped.py --selftest 7000 3`, about 1.5 s):

- body and key counted by a counting word type on 7000 random cases (random
  m0..m14, t, and g < 2^96 placed in R): (202, 8) on all 7000; the key equals
  o0|o1<<32|o2<<64|o3<<96|o5<<128 of the program's reference compression;
- 1000 independently generated seven-message batches: counted packed body and
  extraction `(227,101)` on all batches; all 7000 extracted keys equal the
  corresponding independent reference keys;
- the evidence-only full mode equals all eight reference digest words on all
  7000 cases;
- group constants with counted message words: 244 operations (first 200 cases),
  and the counted constants equal the uncounted ones;
- `table_step` under adversarial garbage, 100 runs x 256 steps with 12-bit keys
  (so MATCH occurs): MATCH exactly when the key was inserted before, with the
  first record's word; step counts 12, 9 and 8 only.

**Organizer-mode observations** (declared experiments, Section 7): every
counted-path trial runs its first batch through the packed counting evaluator
(body 227, extraction 101) and counts every table step (at most 12).

**Local, not shipped.** An earlier counted whole-program simulation (older
memory layout) matched the brute-force specification on 600 scaled runs under
adversarial garbage. The itemized hand counts of Sections 2, 4 and 5 are
authoritative.

## 4A. Register-Resident Scalar-Key Masks `M1..M4` (-4 Extraction Ops/Batch, `416` Counted Ops/Batch, `time_log2 = 125.173`)

In Section 4 above (`2bf40fb6`), the register count for the 64-register file was summed as:
`27 (broadcast group constants) + 16 (state words) + 2 (temporaries) + 8 (rotation masks) + 8 (T, R, CC, M, MC, SB, INC, loop/end) = 61 registers` (reported as 62), and the four shifted scalar-key masks `M1 = M << 32`, `M2 = M << 64`, `M3 = M << 96`, `M4 = M << 128` were recomputed from `M = 2^32 - 1` inside every 7-message batch at a cost of 4 shift operations per batch (`101` extraction ops, `420` counted batch ops).

However, the 16 packed-body state words and 2 packed-body temporaries are only live during the packed body and key extraction (at most 17 registers simultaneously live during the body and extraction), while the 47 batch-invariant registers are:
- 27 broadcast group constants (`D14, C9, B4, NS, A0x, D12, C8, s1, D13h, B5, A1y, A2h, C10, B6, A2y, B7x, D15, C11, B7, s7, s8..s13, s15`),
- 8 rotation masks (`A_7, B_7, A_8, B_8, A_12, B_12, A_16, B_16`),
- 7 control/table registers (`T, R, CC, MC, SB, INC, loop_end`),
- **5 scalar-key position masks (`M = 2^32 - 1`, `M1 = M << 32`, `M2 = M << 64`, `M3 = M << 96`, `M4 = M << 128`)**.

Total persistent registers: `27 + 8 + 7 + 5 = 47`, leaving `64 - 47 = 17` registers for the packed body (which needs 15 state words `v0..v14`—since `v15` is never live after `d15` is updated—plus 2 temporaries = 17 registers). Thus `M1..M4` remain permanently in registers across the entire run (initialized once in constant setup in 4 operations), eliminating the 4 per-batch shift instructions!

This reduces key extraction from `101` to **`97` operations** (`13 + 6 * 14 = 97`) and the counted full 7-message batch from `420` to **`416` operations** (`227` body + `97` extraction + `84` table + `7` scalar `R` + `1` packed `T` = `416`, plus `< 3/64` loop control). Charging **`424` operations per batch** leaves `7.95` spare operations per batch (`> 508` spare operations per 64-batch unrolled block) and yields:

    T <= 2^96 * (q + 1) * 424 / 430 + 2^96 * 1024 / 430 + 2^110 * (2 + 1024 / 430) + 1
      < 0.14086157 * 2^128 < 2^125.17233 < 2^125.173.

We therefore claim **`time_log2 = 125.173`**.

## Appendix B. Reference Counting Evaluator and Scaled Walk (`b3r2_grouped.py`)

```python
"""Scaled end-to-end run of the grouped partial-evaluation birthday search.

Stdlib only. Organizer mode (default) reads one JSON request on stdin and writes
one JSON result. Each organizer trial runs the algorithm of proof.md Section 3
once, scaled to N_t = 2^10 messages (proof.md Section 7):

  b3r2-grouped-spread:   32 groups x t = 0..31, key = mask on o0..o3, o5;
  b3r2-single-group:      1 group  x t = 0..1023, key = mask on o0..o3, o5;
  b3r2-grouped-fullword: 32 groups x t = 0..31, key = mask on all of o0..o7.

A group draws U0 (m0..m7) and U1 (m8..m14) from SHA-256 of (domain, seed, group
index); a message is (m0..m14, m15) with m15 = (t - S) mod 2^32, where
S = a3h + b4h is the group constant of proof.md Section 2, so t is the round-1
state word a3'. Digest words come only from the seven-way SWAR evaluator
`packed_body` (proof.md Section 4). It returns packed o0..o3, o5 fields, and
o4, o6, o7 are never computed. In the evidence-only full mode
(b3r2-grouped-fullword) it also performs the three skipped final b rotations and
returns all eight words with the scalar evaluator; the counted hot path never
uses this mode.

The table is the sparse-set step of proof.md Section 5, executed by the
operation-counting function `table_step`, over a memory whose unwritten words
are adversarial garbage: about half of them carry a pointer field equal to a
genuinely written dense entry (proof.md Lemma 4). Group records live at 4g+1,
4g+2, 4g+3 and the sparse array at SB = 2^160 + key, as in proof.md Section 5;
the full mode uses 2^256 + key (its key has 256 bits; evidence only). On a key
match both messages are rebuilt from the stored records and re-hashed with an
independent reference compression (compress2); the pair is returned when the
messages differ and the masked digest bits agree. A failed trial returns two
nulls. Observations (untrusted) include the counted operations of the first
seven-message batch's body and key extraction, and the extreme table-step counts.

Local mode (not used by the organizer):
  python3 FILE --selftest CASES SEED   counted evaluators vs compress2 (expect
                                       scalar 202+8; packed batch 227+101),
                                       counted group setup, and counted table
                                       steps under adversarial garbage (12/9/8)
"""

import hashlib
import json
import struct
import sys

M = 0xFFFFFFFF
W = (1 << 256) - 1
LANES = 7
STRIDE = 36
PM = sum(M << (STRIDE * j) for j in range(LANES))
RM = {r: sum(((1 << (32 - r)) - 1) << (STRIDE * j) for j in range(LANES))
      for r in (7, 8, 12, 16)}
LM = {r: sum((((1 << r) - 1) << (32 - r)) << (STRIDE * j) for j in range(LANES))
      for r in (7, 8, 12, 16)}
MC = ((1 << 128) - 1) << 32          # pointer field, bits 32..159
SB = 1 << 160                        # sparse-array base (proof.md Section 5)
INC = 1 << 32
IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
      0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
PERM = (2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)
LAYOUT = {"b3r2-grouped-spread": (32, 32, False), "b3r2-single-group": (1, 1024, False),
          "b3r2-grouped-fullword": (32, 32, True)}
KEY_WORDS = (0, 1, 2, 3, 5)          # digest words packed into the counted key


def ror(z, r):
    return ((z >> r) | (z << (32 - r))) & M


def ror_lazy(z, r):
    """Rotate the low 32 bits while allowing harmless garbage above bit 31.

    The double shift truncates the right-shifted arm to the low 32-bit lane.
    The result's low 32 bits are the desired rotation; callers delay the final
    mask until the five digest words used by the key are formed.
    """
    low = z << 224
    if isinstance(low, int):
        low &= W  # Python emulation of the 256-bit machine's shift truncation.
    return (low >> (224 + r)) | (z << (32 - r))


def g(a, b, c, d, x, y):
    a = (a + b + x) & M; d = ror(d ^ a, 16); c = (c + d) & M; b = ror(b ^ c, 12)
    a = (a + b + y) & M; d = ror(d ^ a, 8); c = (c + d) & M; b = ror(b ^ c, 7)
    return a, b, c, d


def compress2(m):
    """Independent reference: digest words o0..o7 of the 2-round root compression
    of one 64-byte block (IV chaining value, counter 0, length 64, flags 11)."""
    v = list(IV) + list(IV[:4]) + [0, 0, 64, 11]
    for _ in (0, 1):
        for (a, b, c, d), i in zip(((0, 4, 8, 12), (1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15),
                                    (0, 5, 10, 15), (1, 6, 11, 12), (2, 7, 8, 13), (3, 4, 9, 14)),
                                   range(0, 16, 2)):
            v[a], v[b], v[c], v[d] = g(v[a], v[b], v[c], v[d], m[i], m[i + 1])
        m = [m[i] for i in PERM]
    return [v[i] ^ v[i + 8] for i in range(8)]


def unpack(U0, U1):
    """m0..m14 from the two group words (m0 = U0 & M, m_i = (U0 >> 32i) & M, ...)."""
    return [(U0 >> (32 * i)) & M if i else U0 & M for i in range(8)] + \
           [(U1 >> (32 * i)) & M if i else U1 & M for i in range(7)]


def setup(m):
    """Group constants (proof.md Section 2) from m0..m14."""
    v = list(IV) + list(IV[:4]) + [0, 0, 64, 11]
    calls = ((0, 4, 8, 12), (1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15),
             (0, 5, 10, 15), (1, 6, 11, 12), (2, 7, 8, 13))
    for (a, b, c, d), i in zip(calls, range(0, 14, 2)):
        v[a], v[b], v[c], v[d] = g(v[a], v[b], v[c], v[d], m[i], m[i + 1])
    a3h = (v[3] + v[4] + m[14]) & M
    d14 = ror(v[14] ^ a3h, 16)
    c9 = (v[9] + d14) & M
    b4 = ror(v[4] ^ c9, 12)
    S = (a3h + b4) & M
    s = [m[i] if i != 15 else None for i in PERM]
    a1h = (v[1] + v[5] + s[2]) & M
    a2h = (v[2] + v[6] + s[4]) & M
    return {
        "S": S, "negS": (-S) & M, "d14": d14, "c9": c9, "b4": b4,
        "A0x": (v[0] + s[0]) & M, "d12": v[12], "c8": v[8], "s1": s[1],
        "d13h": ror(v[13] ^ a1h, 16), "b5": v[5], "A1y": (a1h + s[3]) & M,
        "a2h": a2h, "c10": v[10], "b6": v[6], "A2y": (a2h + s[5]) & M,
        "B7x": (v[7] + s[6]) & M, "d15": v[15], "c11": v[11], "b7": v[7], "s7": s[7],
        "s8": s[8], "s9": s[9], "s10": s[10], "s11": s[11], "s12": s[12], "s13": s[13], "s15": s[15],
    }


def body(K, R, full=False):
    """Per-message program of proof.md Section 4 (R = t + (g << 160)); returns
    o0, o1, o2, o3, o5. With full=True (evidence only, never counted) it also
    performs the three skipped final b rotations and returns o0..o7."""
    z = K["d14"] ^ R; d14 = ror_lazy(z, 8); c9 = K["c9"] + d14; z = K["b4"] ^ c9; b4 = ror_lazy(z, 7)
    a0 = K["A0x"] + b4
    z = K["d12"] ^ a0; d12 = ror_lazy(z, 16); c8 = K["c8"] + d12; z = b4 ^ c8; b4 = ror_lazy(z, 12)
    a0 = a0 + b4 + K["s1"]
    z = d12 ^ a0; d12 = ror_lazy(z, 8); c8 = c8 + d12; z = b4 ^ c8; b4 = ror_lazy(z, 7)
    c9 = c9 + K["d13h"]; z = K["b5"] ^ c9; b5 = ror_lazy(z, 12)
    a1 = K["A1y"] + b5
    z = K["d13h"] ^ a1; d13 = ror_lazy(z, 8); c9 = c9 + d13; z = b5 ^ c9; b5 = ror_lazy(z, 7)
    z = d14 ^ K["a2h"]; d14 = ror_lazy(z, 16); c10 = K["c10"] + d14; z = K["b6"] ^ c10; b6 = ror_lazy(z, 12)
    a2 = K["A2y"] + b6
    z = d14 ^ a2; d14 = ror_lazy(z, 8); c10 = c10 + d14; z = b6 ^ c10; b6 = ror_lazy(z, 7)
    a3 = R + K["B7x"]
    z = K["d15"] ^ a3; d15 = ror_lazy(z, 16); c11 = K["c11"] + d15; z = K["b7"] ^ c11; b7 = ror_lazy(z, 12)
    a3 = a3 + b7 + K["s7"]
    z = d15 ^ a3; d15 = ror_lazy(z, 8); c11 = c11 + d15; z = b7 ^ c11; b7 = ror_lazy(z, 7)
    # diagonal G(0,5,10,15): complete (b5 is kept for o5)
    a0 = a0 + b5 + K["s8"]; z = d15 ^ a0; d15 = ror_lazy(z, 16); c10 = c10 + d15; z = b5 ^ c10; b5 = ror_lazy(z, 12)
    a0 = a0 + b5 + K["s9"]; z = d15 ^ a0; d15 = ror_lazy(z, 8); c10 = c10 + d15; z = b5 ^ c10; b5 = ror_lazy(z, 7)
    # diagonals G(1,6,11,12) and G(2,7,8,13): final b rotation skipped (counted mode)
    a1 = a1 + b6 + K["s10"]; z = d12 ^ a1; d12 = ror_lazy(z, 16); c11 = c11 + d12; z = b6 ^ c11; b6 = ror_lazy(z, 12)
    a1 = a1 + b6 + K["s11"]; z = d12 ^ a1; d12 = ror_lazy(z, 8); c11 = c11 + d12
    a2 = a2 + b7 + K["s12"]; z = d13 ^ a2; d13 = ror_lazy(z, 16); c8 = c8 + d13; z = b7 ^ c8; b7 = ror_lazy(z, 12)
    a2 = a2 + b7 + K["s13"]; z = d13 ^ a2; d13 = ror_lazy(z, 8); c8 = c8 + d13
    # diagonal G(3,4,9,14): x = m15 = t - S, so a3 + b4 + m15 = a3 + b4 + R + negS
    a3 = a3 + b4 + R + K["negS"]; z = d14 ^ a3; d14 = ror_lazy(z, 16); c9 = c9 + d14; z = b4 ^ c9; b4 = ror_lazy(z, 12)
    a3 = a3 + b4 + K["s15"]; z = d14 ^ a3; d14 = ror_lazy(z, 8); c9 = c9 + d14
    if not full:
        return (a0 ^ c8) & M, (a1 ^ c9) & M, (a2 ^ c10) & M, (a3 ^ c11) & M, (b5 ^ d13) & M
    b6 = ror_lazy(b6 ^ c11, 7); b7 = ror_lazy(b7 ^ c8, 7); b4 = ror_lazy(b4 ^ c9, 7)
    return tuple(x & M for x in (a0 ^ c8, a1 ^ c9, a2 ^ c10, a3 ^ c11,
                                 b4 ^ d12, b5 ^ d13, b6 ^ d14, b7 ^ d15))


def broadcast(x):
    """Seven copies of one 32-bit value in 36-bit fields."""
    return sum(x << (STRIDE * j) for j in range(LANES))


def pack_lanes(xs):
    """Pack at most seven 32-bit lane values; omitted high lanes are zero."""
    return sum((x & M) << (STRIDE * j) for j, x in enumerate(xs))


def packed_constants(K):
    return {name: broadcast(value) for name, value in K.items() if name != "S"}


def padd2(a, b):
    return a + b


def padd3(a, b, c):
    return a + b + c


def padd4(a, b, c, d):
    return a + b + c + d


def pror(z, r):
    """Rotate each of seven 32-bit fields, preserving the two guard bits."""
    return ((z >> r) & RM[r]) | ((z << (32 - r)) & LM[r])


def packed_body(K, T):
    """Seven-way SWAR form of the counted five-output body."""
    z = K["d14"] ^ T; d14 = pror(z, 8); c9 = padd2(K["c9"], d14); z = K["b4"] ^ c9; b4 = pror(z, 7)
    a0 = padd2(K["A0x"], b4)
    z = K["d12"] ^ a0; d12 = pror(z, 16); c8 = padd2(K["c8"], d12); z = b4 ^ c8; b4 = pror(z, 12)
    a0 = padd3(a0, b4, K["s1"])
    z = d12 ^ a0; d12 = pror(z, 8); c8 = padd2(c8, d12); z = b4 ^ c8; b4 = pror(z, 7)
    c9 = padd2(c9, K["d13h"]); z = K["b5"] ^ c9; b5 = pror(z, 12)
    a1 = padd2(K["A1y"], b5)
    z = K["d13h"] ^ a1; d13 = pror(z, 8); c9 = padd2(c9, d13); z = b5 ^ c9; b5 = pror(z, 7)
    z = d14 ^ K["a2h"]; d14 = pror(z, 16); c10 = padd2(K["c10"], d14); z = K["b6"] ^ c10; b6 = pror(z, 12)
    a2 = padd2(K["A2y"], b6)
    z = d14 ^ a2; d14 = pror(z, 8); c10 = padd2(c10, d14); z = b6 ^ c10; b6 = pror(z, 7)
    a3 = padd2(T, K["B7x"])
    z = K["d15"] ^ a3; d15 = pror(z, 16); c11 = padd2(K["c11"], d15); z = K["b7"] ^ c11; b7 = pror(z, 12)
    a3 = padd3(a3, b7, K["s7"])
    z = d15 ^ a3; d15 = pror(z, 8); c11 = padd2(c11, d15); z = b7 ^ c11; b7 = pror(z, 7)
    a0 = padd3(a0, b5, K["s8"]); z = d15 ^ a0; d15 = pror(z, 16); c10 = padd2(c10, d15); z = b5 ^ c10; b5 = pror(z, 12)
    a0 = padd3(a0, b5, K["s9"]); z = d15 ^ a0; d15 = pror(z, 8); c10 = padd2(c10, d15); z = b5 ^ c10; b5 = pror(z, 7)
    a1 = padd3(a1, b6, K["s10"]); z = d12 ^ a1; d12 = pror(z, 16); c11 = padd2(c11, d12); z = b6 ^ c11; b6 = pror(z, 12)
    a1 = padd3(a1, b6, K["s11"]); z = d12 ^ a1; d12 = pror(z, 8); c11 = padd2(c11, d12)
    a2 = padd3(a2, b7, K["s12"]); z = d13 ^ a2; d13 = pror(z, 16); c8 = padd2(c8, d13); z = b7 ^ c8; b7 = pror(z, 12)
    a2 = padd3(a2, b7, K["s13"]); z = d13 ^ a2; d13 = pror(z, 8); c8 = padd2(c8, d13)
    a3 = padd4(a3, b4, T, K["negS"]); z = d14 ^ a3; d14 = pror(z, 16); c9 = padd2(c9, d14); z = b4 ^ c9; b4 = pror(z, 12)
    a3 = padd3(a3, b4, K["s15"]); z = d14 ^ a3; d14 = pror(z, 8); c9 = padd2(c9, d14)
    return a0 ^ c8, a1 ^ c9, a2 ^ c10, a3 ^ c11, b5 ^ d13


def target_key_masks(base=M):
    """Masks at the five scalar-key destinations (four charged shifts)."""
    return [base] + [base << d for d in (32, 64, 96, 128)]


def extract_keys(o, masks=None):
    """Extract each lane directly into its five scalar-key destinations."""
    masks = target_key_masks() if masks is None else masks
    keys = []
    for lane in range(LANES):
        source = STRIDE * lane
        pieces = []
        for x, dest, mask in zip(o, (0, 32, 64, 96, 128), masks):
            y = x >> (source - dest) if source > dest else \
                (x << (dest - source) if source < dest else x)
            pieces.append(y & mask)
        keys.append(pieces[0] | pieces[1] | pieces[2] | pieces[3] | pieces[4])
    return keys


def pack(o):
    """Counted key: o0 | o1<<32 | o2<<64 | o3<<96 | o5<<128 (8 operations)."""
    return o[0] | (o[1] << 32) | (o[2] << 64) | (o[3] << 96) | (o[4] << 128)


def key_masks(mask_hex):
    """(mask on the packed 5-word key or None, mask on the packed 8-word digest, words)."""
    words = struct.unpack("<8I", bytes.fromhex(mask_hex))
    k8 = sum(w << (32 * i) for i, w in enumerate(words))
    k5 = None if any(words[i] for i in (4, 6, 7)) else sum(words[w] << (32 * j) for j, w in enumerate(KEY_WORDS))
    return k5, k8, words


def group_words(seed, gi):
    h = hashlib.sha256(b"b3r2-grouped-v1" + seed + gi.to_bytes(4, "little")).digest()
    h += hashlib.sha256(b"b3r2-grouped-v1" + seed + gi.to_bytes(4, "little") + b"\x01").digest()
    w = struct.unpack("<16I", h)
    U0 = sum(w[i] << (32 * i) for i in range(8))
    U1 = sum(w[8 + i] << (32 * i) for i in range(7))
    return U0, U1


class Memory:
    """Never-initialised memory. An unwritten word reads as seed-derived garbage;
    for about half of the unwritten addresses (once a record exists) the garbage
    carries, in bits 32..159, the address of a genuinely written dense entry."""
    def __init__(self, seed):
        self.seed, self.cells, self.stale = seed, {}, 0

    def load(self, a, CC=0):
        if a in self.cells:
            return self.cells[a]
        h = hashlib.sha256(b"garbage" + self.seed + a.to_bytes(33, "little")).digest()
        x = int.from_bytes(h, "little")
        if CC >= INC and h[0] & 1:
            j = int.from_bytes(hashlib.sha256(b"stale" + h).digest(), "little") % (CC >> 32)
            x = (x & ~MC) | (j << 32)
            self.stale += 1
        return x

    def store(self, a, v):
        self.cells[a] = v


def table_step(mem, key, sbase, R, CC):
    """Sparse-set step of proof.md Section 5, with its operations counted exactly
    as listed there. Returns (matched, w, CC, ops)."""
    ops = 0
    sa = key | sbase; ops += 1                     # OR
    w = mem.load(sa, CC); ops += 1                 # load
    p = w & MC; ops += 1                           # AND
    ops += 2                                       # compare p < CC, branch
    if p < CC:
        q = mem.load(p, CC); ops += 1              # load
        ops += 2                                   # compare q == key, branch
        if q == key:
            return True, w, CC, ops                # MATCH: 8
    mem.store(sa, R | CC); ops += 2                # OR, store
    mem.store(CC, key); ops += 1                   # store
    CC = CC + INC; ops += 1                        # add
    return False, w, CC, ops                       # 12 or 9


class V:
    """Counting word: every operation with a V operand is counted once."""
    n = 0

    def __init__(self, x): self.x = x

    def _op(self, f, o):
        V.n += 1
        return V(f(self.x, o.x if isinstance(o, V) else o) & ((1 << 256) - 1))

    def __add__(self, o): return self._op(lambda a, b: a + b, o)
    __radd__ = __add__
    def __xor__(self, o): return self._op(lambda a, b: a ^ b, o)
    __rxor__ = __xor__
    def __and__(self, o): return self._op(lambda a, b: a & b, o)
    __rand__ = __and__
    def __or__(self, o): return self._op(lambda a, b: a | b, o)
    __ror__ = __or__
    def __rshift__(self, k): return self._op(lambda a, b: a >> b, k)
    def __lshift__(self, k): return self._op(lambda a, b: a << b, k)
    def __neg__(self): return self._op(lambda a, b: -a, 0)


def counted_body_key(K, R):
    V.n = 0
    o = body(K, V(R))
    nb = V.n
    k = pack(o)
    return k.x, nb, V.n - nb


def counted_packed_body_keys(K, ts):
    """Count one seven-way body and extraction of all seven scalar keys."""
    V.n = 0
    o = packed_body(packed_constants(K), V(pack_lanes(ts)))
    nb = V.n
    masks = target_key_masks(V(M))
    keys = extract_keys(o, masks)
    return [k.x for k in keys], nb, V.n - nb


def trial(seed, groups, per_group, full, k5, k8, wmask):
    mem = Memory(seed)
    CC = 0
    msgs = verifications = 0
    tmin, tmax = 99, 0
    obs = {}
    sbase = (1 << 256) if full else SB
    for gi in range(groups):
        U0, U1 = group_words(seed, gi)
        m = unpack(U0, U1)
        K = setup(m)
        PK = packed_constants(K)
        mem.store(4 * gi + 1, U0)                  # group record: 4g+1, 4g+2, 4g+3
        mem.store(4 * gi + 2, U1)
        mem.store(4 * gi + 3, K["S"])
        G, R = gi << 160, gi << 160
        for base in range(0, per_group, LANES):
            active = min(LANES, per_group - base)
            ts = list(range(base, base + active))
            if full:
                keys = [sum(w << (32 * i) for i, w in enumerate(body(K, G + t, True))) & k8 for t in ts]
            else:
                if msgs == 0:                      # counted run of the first packed batch
                    _, obs["first_packed_body_ops"], obs["first_extract_key_ops"] = \
                        counted_packed_body_keys(K, ts + [0] * (LANES - active))
                keys = [key & k5 for key in extract_keys(packed_body(PK, pack_lanes(ts)))]
            for key in keys[:active]:
                msgs += 1
                matched, w, CC, ops = table_step(mem, key, sbase, R, CC)
                tmin, tmax = min(tmin, ops), max(tmax, ops)
                if matched:
                    verifications += 1
                    tz, gz = w & M, w >> 160
                    mz = unpack(mem.load(4 * gz + 1), mem.load(4 * gz + 2)) + [(tz - mem.load(4 * gz + 3)) & M]
                    mx = m + [((R & M) + K["negS"]) & M]
                    dz, dx = compress2(mz), compress2(mx)
                    if mz != mx and all((dz[i] ^ dx[i]) & wmask[i] == 0 for i in range(8)):
                        obs.update(messages=msgs, verifications=verifications, table_ops_min=tmin,
                                   table_ops_max=tmax, stale_garbage_pointers=mem.stale)
                        return struct.pack("<16I", *mz).hex(), struct.pack("<16I", *mx).hex(), obs
                R += 1
    obs.update(messages=msgs, verifications=verifications, table_ops_min=tmin,
               table_ops_max=tmax, stale_garbage_pointers=mem.stale)
    return None, None, obs


def selftest(cases, seed):
    counts, packed_counts, packed_ok, full_ok, setup_ops = {}, {}, 0, 0, set()
    for c in range(cases):
        h = hashlib.sha256(b"selftest" + seed.to_bytes(8, "little") + c.to_bytes(8, "little")).digest() * 2
        words = struct.unpack("<16I", h)
        m, t, gi = list(words[:15]), words[15], int.from_bytes(h[:12], "little")
        K = setup(m)
        R = t + (gi << 160)
        k, nb, npk = counted_body_key(K, R)
        d = compress2(m + [(t - K["S"]) & M])
        assert k == pack([d[i] for i in KEY_WORDS]), c
        assert list(body(K, R, True)) == d, c
        full_ok += 1
        counts[(nb, npk)] = counts.get((nb, npk), 0) + 1
        if c < 200:
            V.n = 0
            KV = setup([V(x) for x in m])
            setup_ops.add(V.n)
            assert {n: (v.x if isinstance(v, V) else v) for n, v in KV.items() if n != "S"} == \
                   {n: v for n, v in K.items() if n != "S"}
        if c % LANES == 0:
            ts = []
            for j in range(LANES):
                hj = hashlib.sha256(h + j.to_bytes(1, "little")).digest()
                ts.append(int.from_bytes(hj[:4], "little"))
            keys, npb, npe = counted_packed_body_keys(K, ts)
            packed_counts[(npb, npe)] = packed_counts.get((npb, npe), 0) + 1
            for j, tj in enumerate(ts):
                dj = compress2(m + [(tj - K["S"]) & M])
                assert keys[j] == pack([dj[i] for i in KEY_WORDS]), (c, j)
                packed_ok += 1
    # table steps under adversarial garbage: scaled runs with a 12-bit key
    tcounts, agree = {}, 0
    for r in range(100):
        mem, CC, seen, R = Memory(b"tbl" + r.to_bytes(4, "little")), 0, {}, 0
        for i in range(256):
            key = int.from_bytes(hashlib.sha256(b"k" + r.to_bytes(4, "little") + i.to_bytes(4, "little")).digest()[:2], "little") & 0xFFF
            matched, w, CC, ops = table_step(mem, key, SB, R, CC)
            tcounts[ops] = tcounts.get(ops, 0) + 1
            if matched != (key in seen) or (matched and w != seen[key]):
                raise AssertionError("table semantics")
            if not matched:
                seen[key] = R | (CC - INC)
            R += 1
        agree += 1
    print(json.dumps({"cases": cases, "body_key_op_counts": {"%d,%d" % kk: n for kk, n in counts.items()},
                      "packed_body_extract_op_counts": {"%d,%d" % kk: n for kk, n in packed_counts.items()},
                      "packed_lanes_equal_reference": packed_ok,
                      "full_mode_equals_reference": full_ok, "setup_ops_counted": sorted(setup_ops),
                      "table_runs_ok": agree, "table_op_counts": {str(kk): n for kk, n in sorted(tcounts.items())}}))


def main():
    if len(sys.argv) == 4 and sys.argv[1] == "--selftest":
        selftest(int(sys.argv[2]), int(sys.argv[3]))
        return
    request = json.load(sys.stdin)
    if request["schema_version"] != 1 or request["target_profile"] != "blake3-r2-prefix-v1":
        raise ValueError("unexpected organizer target")
    event = request["event"]
    if event.get("kind") != "digest-xor-mask" or int(event["expected_hex"], 16) != 0:
        raise ValueError("unexpected organizer event")
    groups, per_group, full = LAYOUT[request["experiment_id"]]
    k5, k8, wmask = key_masks(event["mask_hex"])
    if not full and k5 is None:
        raise ValueError("counted-key experiments need a mask inside o0..o3, o5")
    rows = []
    for item in request["trials"]:
        first, second, obs = trial(bytes.fromhex(item["seed"]), groups, per_group, full, k5, k8, wmask)
        rows.append({"trial": item["trial"], "message_a_hex": first, "message_b_hex": second,
                     "observations": obs})
    json.dump({"schema_version": 1, "trials": rows}, sys.stdout, separators=(",", ":"), sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()

```
