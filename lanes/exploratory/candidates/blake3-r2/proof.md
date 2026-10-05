# Grouped partial-evaluation birthday search on 2-round BLAKE3 (constant-factor refinement)

## 0. Summary

Exploratory package for blake3-r2-prefix-v1 under collision-frontier-v5 (C = 430).

| quantity | value |
| --- | --- |
| messages N | 2^128 one-block root messages, 2^96 groups x 2^32 |
| word operations per message, counted exactly (worst case) | 249 (228 body + 8 key + 12 table + 1 counter), plus 3/256 loop control |
| word operations per message, **charged** | **256** (about 7 spare operations) |
| total charged time T | < 0.5953656 * 2^128 < 2^127.25185 |
| claimed `time_log2` | **127.252** (bound rounded up) |
| success probability | 0.39 under heuristic H1 (model value > 0.39343) |
| memory (unscored) | every address below 2^161 words = 2^166 bytes; reported as 167; < 2^134.001 bytes written |
| preprocessing / advice | 0 / 0 |

**Credit.** The grouping idea is jaazinn's (accepted package for this track,
ticket 0a5b7ae8, time_log2 127.481): messages in 2^96 groups of 2^32 share all
words except one, so about half of the compression is computed once per group,
and a sparse-set table finds the collision. jaazinn is a co-author of this
package. We use the same message set and the same heuristic premise. Our success
analysis is analogous, with events F2' and Fcap (Section 6) in place of their
displacement event F2. This package changes the per-message program and the
table step, and every change is counted exactly (Section 9 lists them).

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
operations on IV words alone are program constants); record addresses
(g << 2) | 1 and two increments (4) and three stores (3); R = g << 160 and
Rend = R + 2^32 (2); group counter load, add, store, compare, branch (5).
Total 289 < 1024.

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
3. Inner loop: straight-line code unrolled 256 times. Each copy processes one
   message with the current R (low 32 bits = t, bits 160..255 = g):
   body (228 ops), key K (8), table step (at most 12), R = R + 1 (1).
   After the 256th copy: compare R with Rend and branch back to copy 0, falling
   through to the group loop when equal (charged 3 per 256 messages).
   2^32 is a multiple of 256.
4. MATCH (Section 5). Each of the 256 copies has its own copy of the MATCH
   handler. On success it writes both messages to the output buffer and halts.
   Otherwise it branches back to its own copy's `R = R + 1`, so no indirect
   jump is needed. Code size: 256 x (about 260 hot-path + at most 120 handler)
   instructions < 2^17.
5. After the last group, halt with failure.

The program halts after at most N = 2^128 messages and at most 2^110
verifications. Section 8 prices this worst case.

## 4. Per-message program and its exact count

The counting convention is that of scripts/reference_operation_costs.py, made
strict: every operation with a per-message operand is counted, including those
whose other operand is a constant. A 32-bit addition is the 256-bit add followed
by `& M`. ROR(z,r) = ((z >> r) | (z << (32-r))) & M is 4 operations, exactly
verifier/blake3.py:_ror (no native rotation is used). Notation and costs:

    A2(x,y) = (x + y) & M          2 ops
    A3(x,y,z) = (x + y + z) & M    3 ops
    ROR(u ^ w, r)                  5 ops (xor + 4)

Listing (R is used directly as t; see Lemma 2):

    -- round 1, 2nd half of G(3,4,9,14,m14,m15); v3 = t                  12
    d14 = ROR(D14 ^ R, 8)                5
    c9  = A2(C9, d14)                    2
    b4  = ROR(B4 ^ c9, 7)                5
    -- round 2, column G(0,4,8,12,s0,s1), b varies                       29
    a0 = A2(A0x, b4); d12 = ROR(D12 ^ a0, 16); c8 = A2(C8, d12); b4 = ROR(b4 ^ c8, 12)
    a0 = A3(a0, b4, s1); d12 = ROR(d12 ^ a0, 8); c8 = A2(c8, d12); b4 = ROR(b4 ^ c8, 7)
                                         2+5+2+5+3+5+2+5
    -- column G(1,5,9,13,s2,s3), c varies                               21
    c9 = A2(c9, D13h); b5 = ROR(B5 ^ c9, 12)
    a1 = A2(A1y, b5); d13 = ROR(D13h ^ a1, 8); c9 = A2(c9, d13); b5 = ROR(b5 ^ c9, 7)
                                         2+5+2+5+2+5
    -- column G(2,6,10,14,s4,s5), d varies                              26
    d14 = ROR(d14 ^ A2h, 16); c10 = A2(C10, d14); b6 = ROR(B6 ^ c10, 12)
    a2 = A2(A2y, b6); d14 = ROR(d14 ^ a2, 8); c10 = A2(c10, d14); b6 = ROR(b6 ^ c10, 7)
                                         5+2+5+2+5+2+5
    -- column G(3,7,11,15,s6,s7), a varies                              29
    a3 = A2(R, B7x); d15 = ROR(D15 ^ a3, 16); c11 = A2(C11, d15); b7 = ROR(B7 ^ c11, 12)
    a3 = A3(a3, b7, s7); d15 = ROR(d15 ^ a3, 8); c11 = A2(c11, d15); b7 = ROR(b7 ^ c11, 7)
                                         2+5+2+5+3+5+2+5
    -- diagonals                                                       106
    G(0,5,10,15, s8, s9)   complete (b5 is needed for o5)                30
    G(1,6,11,12, s10, s11) without its final b6 = ROR(b6 ^ c11, 7)       25
    G(2,7,8,13,  s12, s13) without its final b7 = ROR(b7 ^ c8, 7)        25
    G(3,4,9,14,  m15, s15): a3 = (a3 + b4 + R + NS) & M   (= a3+b4+m15)   4
                 then the rest of G without its final b4 rotation       22
    -- outputs actually needed                                            5
    o0 = a0^c8; o1 = a1^c9; o2 = a2^c10; o3 = a3^c11; o5 = b5^d13
    -- key                                                                8
    K = o0 | (o1 << 32) | (o2 << 64) | (o3 << 96) | (o5 << 128)
    -- table step (Section 5), worst-case path                           12
    -- message counter: R = R + 1                                         1
    counted total                                                       249

Body: 12 + 29 + 21 + 26 + 29 + 106 + 5 = 228. The full G call is
3+5+2+5+3+5+2+5 = 30 operations. **Charge.** We charge 256 operations per
message, which covers the 249 counted operations, the 3/256 of loop control and
about 6.99 spare operations, so that no single disputed operation (a register
move, a flag, a jump) can make the time bound understated.

**Lemma 2 (R as t).** R = t + g*2^160 with t < 2^32, so bits 32..159 of R are zero.
R enters the body in three places. In ROR(D14 ^ R, 8), the low 32 bits of
(z >> 8) are bits 8..39 of z, and bits 32..39 are zero. The low 32 bits of
(z << 24) are bits 0..7 of z. The final `& M` removes everything else, so the
result equals ROR(D14 ^ t, 8). In A2(R, B7x) and (a3 + b4 + R + NS) & M, a
sum's low 32 bits depend only on the operands' low 32 bits. So every value equals
the one computed with t. Also (t + NS) mod 2^32 = m15, so the last diagonal's
first addition is exactly a3 + b4 + m15.

**Lemma 3 (key).** Every o_i above is the XOR of two values below 2^32, so
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
occur. Within a copy, control falls through from one line to the next; the only
branches are the two table tests (Section 5), which are counted. The machine
has 64 registers. The hot loop needs 27 group constants, 16 state words, 2
rotation temporaries, R, Rend, CC, and M, MC, SB, INC: 52 registers. Key and
table temporaries reuse state registers that are dead by then. Shift amounts are
instruction immediates (63 registers if the eleven distinct amounts were held in
registers). The group counter and VC live in memory (Section 3); only group
setup and MATCH access them, within their budgets. If instead all 27 group
constants are reloaded from memory for every message (+27 loads), the counted
cost is 276 and the bound becomes 2^127.3605, or 2^127.3966 with the same 7
spare operations (Section 8).

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
from the grouped evaluator of Section 4, run with the t-enumeration and
R = t + g*2^160. The scaled key is a 20-bit event mask applied to the key. The
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

Every trial also reports untrusted observations: the counted body and key
operations of its first message, the minimum and maximum counted table step,
the number of verifications and the number of stale garbage pointers read.

**Our local replay of the organizer runner** (experiments.runner.run_experiments
with the track's config_sha256, seed hashsmash-public-seed-v1, 256 trials, the
Docker executor replaced by a local Python subprocess because Docker was not
available to us; these are not organizer results):

- spread 107/256, single group 98/256, fullword 92/256 (model 100.7, sd 7.8);
- no repeated pairs; at most 1 verification per trial;
- observations in every trial: body 228, key 8, table steps between 8 or 9 and
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

Per message: 256 charged operations (249 counted, 3/256 loop control, the rest
spare). Per group: at most 1024 operations. Per MATCH entry: 2 units plus at most
1024 operations, for at most 2^110 entries; the (2^110+1)-th entry halts after
step 1. Constant setup: below 1 unit.

    T <= 2^128 * 256/430 + 2^96 * 1024/430 + 2^110 * (2 + 1024/430) + 1
      <  2^128 * 0.59534884 + 2^97.252 + 2^112.132 + 1
      <  0.5953656 * 2^128  <  2^127.25185

The claim is time_log2 = 127.252, the bound rounded up. In log2, the
per-message main term alone is 127.25181; setup and verification together add
less than 0.0001.

**Sensitivity** (charged operations per message; log2 T rounded up):

| charge | 249 + 3/256 (no spare) | 252 | 255 | **256 (claimed)** | 276 + 3/256 (all reloaded) | 283 (all reloaded, 7 spare) |
| --- | --- | --- | --- | --- | --- | --- |
| log2 T | 127.2120 | 127.2292 | 127.2463 | 127.2519 | 127.3605 | 127.3966 |

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

The counted per-message cost falls from 286 to 249, and the charge from 300
(286 + 14 spare) to 256 (249 + 3/256 + about 7 spare):

| change | ops |
| --- | --- |
| enumerate t = a3' instead of m15: round-1 tail 12 instead of 14; last diagonal's first add 4 instead of 3 | -1 |
| key from o0..o3, o5 only: skip 3 final b rotations and 3 output XORs | -18 body |
| pack 5 words instead of 8 | -6 key |
| table indexed by the whole 160-bit key; dense array at base 0 with stride 2^32 so that CC is both the dense address and the record field; record = R | CC. This removes the index shift, base adds and discard branch, and no slot is ever displaced | -9 |
| single register R = t + g*2^160: counter, t and record id in one add per message | -3 |

Every number is exact under the convention of Section 4 and is reproduced by the
shipped `--selftest` (body and key) and by `table_step` (table). Under the same
convention a whole compression is 16 * 30 + 16 = 496 operations, as in jaazinn's
note. The program never evaluates a whole compression per message: 250 of those
496 operations are group-invariant, and 18 are skipped.

**Not used** (disclosed so the claim is not read as tight against them): lazy
masking after additions (about 223 ops per message), SWAR packing of several
messages per word, and dropping the p < CC test (needs initialised memory).

## Appendix A. Mechanical checks

**Shipped** (`python3 experiments/b3r2_grouped.py --selftest 3000 1`, about 0.4 s):

- body and key counted by a counting word type on 3000 random cases (random
  m0..m14, t, and g < 2^96 placed in R): (228, 8) on all 3000; the key equals
  o0|o1<<32|o2<<64|o3<<96|o5<<128 of the program's reference compression;
- the evidence-only full mode equals all eight reference digest words on all
  3000 cases;
- group constants with counted message words: 244 operations (first 200 cases),
  and the counted constants equal the uncounted ones;
- `table_step` under adversarial garbage, 100 runs x 256 steps with 12-bit keys
  (so MATCH occurs): MATCH exactly when the key was inserted before, with the
  first record's word; step counts 12, 9 and 8 only.

**Organizer-mode observations** (declared experiments, Section 7): every trial
runs its first message through the counted evaluator (body 228, key 8) and
counts every table step (at most 12).

**Local, not shipped.** An earlier counted whole-program simulation (older
memory layout) matched the brute-force specification on 600 scaled runs under
adversarial garbage. The itemized hand counts of Sections 2, 4 and 5 are
authoritative.
