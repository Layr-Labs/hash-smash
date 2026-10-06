# Seven-lane grouped birthday search on 2-round BLAKE3 with a 64-operation key extraction and a pointer-free table

## 0. Summary

Exploratory package for blake3-r2-prefix-v1 under collision-frontier-v5 (C = 430).

| quantity | value |
| --- | --- |
| messages N | 2^128 one-block root messages, 2^96 groups x 2^32 |
| counted operations per full 7-message batch (worst case) | 355 = 227 body + 64 key extraction + 63 table (7 x 9) + 1 T advance |
| counted per 64-batch unrolled block | 64 x 355 + 3 loop control |
| operations **charged** per batch (full or tail) | **360** (covers loop control; about 4.9 spare per batch) |
| total charged time T | < 0.1196181 * 2^128 < 2^124.93651 |
| claimed `time_log2` | **124.937** (bound rounded up) |
| success probability | 0.39 under heuristic H1 (model value > 0.39343) |
| memory (unscored) | every address below 2^256 words = 2^261 bytes (reported 261); < 2^134.001 bytes written |
| preprocessing / advice | 2^10 units (installation, also charged inside T) / 0 |

**Credit first.** This package refines public packages and uses their ideas
directly; their authors are co-authors. None of the tickets cited here has been
promoted: all are public, AI-screened and in review.

- **tekkac** (tickets 1c8c7c53, 125.149, and 2bf40fb6): the seven-lane SWAR
  layout (seven 32-bit payloads in 36-bit slots of a 256-bit word), the
  delayed-reduction body and its live-value bounds, the 227-operation packed
  body schedule (Section 4 reproduces it operation for operation), the gapped
  injective 176-bit key, and the proof structure of Sections 1-2 and 6-7.
- **ercumentyildirim** (tickets b2508e27, 126.67, and 2e96a19e, 125.98): the
  first public SWAR packing of BLAKE3 lanes into one 256-bit word on this
  track (b2508e27 predates 2bf40fb6) and the 5-operation masked-shift-pair
  rotation that the packed body uses.
- **jaazinn** (public ticket 0a5b7ae8, 127.481): the grouping idea and message
  set, the never-initialised Briggs-Torczon sparse-set table, verification by
  two reference compressions, and the premise H1.
- Our own earlier ticket 3022205a (127.252) contributed the t = a3'
  enumeration, the 160-bit key o0..o3, o5, and the experiment protocol that
  tekkac's package and this one reuse.

New here (Sections 4-5): (i) an interleaved key extraction that produces the
same seven gapped keys in 64 operations instead of 97; (ii) a table whose record is the
dense address itself, with the dense array growing down from 2^256 - 1, so no
record word, alignment mask or record counter is needed (12 -> 9 operations
per table step, and the 7 record-counter increments disappear); (iii) the key
word is used directly as the sparse address (no base OR). The body itself is
tekkac's; our rotation masks before the left shift
((z >> r) & LOW_{32-r}) | ((z & LOW_r) << (32-r)), a register-saving variant
of ercumentyildirim's and tekkac's 5-operation masked shift pair, not a new
idea.

This is a generic birthday search with a smaller constant factor. It is not a
differential or algebraic attack and claims no improvement over the nominal
reference 128. The time bound is a worst-case cap on every run. Every output is
re-hashed with two reference compressions. Only the success probability uses H1.

## 1. Target and message set

H is unkeyed BLAKE3-256 with prefix rounds 0-1 (verifier/blake3.py:blake3 with
rounds = 2). Every evaluated message is exactly 64 bytes: one root compression
with chaining value IV, counter 0, block length 64 and flags
CHUNK_START|CHUNK_END|ROOT = 11. Words m0..m15 are little-endian. The state is
v = (IV[0..7], IV[0..3], 0, 0, 64, 11). G(a,b,c,d,x,y) is

    v[a]=v[a]+v[b]+x; v[d]=ROR(v[d]^v[a],16); v[c]=v[c]+v[d]; v[b]=ROR(v[b]^v[c],12)
    v[a]=v[a]+v[b]+y; v[d]=ROR(v[d]^v[a],8);  v[c]=v[c]+v[d]; v[b]=ROR(v[b]^v[c],7)

with additions mod 2^32. A round applies G to columns (0,4,8,12), (1,5,9,13),
(2,6,10,14), (3,7,11,15) with schedule pairs (s0,s1)..(s6,s7), then to
diagonals (0,5,10,15), (1,6,11,12), (2,7,8,13), (3,4,9,14) with (s8,s9)..(s14,s15).
Round 1 uses s = m; round 2 uses s_i = m[P[i]] with
P = (2,6,3,10,7,0,4,13,1,11,12,5,9,14,15,8). The digest is o_i = v[i] ^ v[i+8].

**Message set.** For each group g = 0..2^96-1 the algorithm draws two independent
uniform 256-bit words U0_g, U1_g. They give m0..m7 (U0_g) and m8..m14 (the low
224 bits of U1_g). With a3h, b4h = v[3], v[4] after the first half of round 1's
last call G(3,4,9,14,m14,m15), let S_g = (a3h + b4h) mod 2^32 (a function of
m0..m14 only). The group enumerates t = 0..2^32-1 with m15 = (t - S_g) mod 2^32,
so t is exactly the round-1 state word a3' = a3h + b4h + m15.

**Lemma 1 (bijection).** For fixed m0..m14, t -> (t - S_g) mod 2^32 is a bijection,
so group g contains exactly the 2^32 messages with m15 = 0..2^32-1 (jaazinn's
set). Messages of one group are distinct; messages of different groups are
distinct unless the groups have identical m0..m14 (event F3, Section 6).

## 2. Group constants and group setup

Round 1 reads m15 only as y in its last call; round 2 reads m15 only as
x = s14 in its last call. For fixed m0..m14, the four round-1 column calls,
the first three diagonal calls and the first half of the last one are group
constants; after round 1 only v3 = t, v4, v9, v14 depend on t; each round-2
column call receives one varying word, and its invariant prefix is a group
constant. The hot loop keeps these 27 constants (each reduced mod 2^32):

    d14, c9, b4 (after the first half of the last round-1 call); negS = -S_g;
    A0x = v0+s0, d12, c8, s1; d13h = ROR(v13 ^ a1h, 16), b5, A1y = a1h+s3;
    a2h, c10, b6, A2y = a2h+s5; B7x = v7+s6, d15, c11, b7, s7; s8..s13; s15
    (a1h = v1+v5+s2, a2h = v2+v6+s4).

**Group setup** (counted by our VM, Appendix A; charged 1024 operations):
draw U0, U1 (2); U1 &= 2^224-1 (1); unpack m0..m14 (15 ANDs, 13 shifts: 28);
the 27 constants and S (266 in our VM's strict scalar convention, with every
32-bit addition masked and every rotation 4 operations; the shipped
`--selftest` counts 244 under the convention of Section 4); load
W7 = 2^252-1 (1) and 27 broadcasts into r0..r26, each
x |= x<<36; x |= x<<72; x |= x<<144; x &= W7 (7 operations: 189); the record
addresses (g << 36) | 2^32 | k (5); three record stores (3); T = T0 (1 load);
END = CC - 7*64*9586980 (3). That is 499 counted. Add g = (NOT CC) >> 32 and
the group-loop test (at most 4): at most 503 under the direct reading and at
most 770 even with +1 for every direct access, immediate and shift amount;
below 1024.

## 3. Algorithm, registers and memory layout

**Registers** (64; three-address code; shift amounts are instruction fields):

| registers | content |
| --- | --- |
| r0..r26 | the 27 broadcast group constants (Section 2) |
| r27..r33 | LOW_k for k = 7, 8, 12, 16, 20, 24, 25 (low k bits of every slot) |
| r34, r35, r36, r37 | packed T (lane j = t + j), CC, BC7 = broadcast(7), ONE = 1 |
| r38..r46 | nine extraction masks W0, W14, W25, W36, M012, W13, W05, W246, M34 |
| r47..r63 | 17 temporaries of the straight-line batch program |

Here LOW(32, J) has the 32 payload bits of the slots j in J; W_G = LOW(32, G) and
M_S = LOW(32, S) with S read as key-slot indices. No constant is reloaded and
nothing is spilled in the hot loop (the shipped allocation uses r0..r63 only).

**Memory** (word-addressed RAM of 256-bit words, as in 1c8c7c53; never
initialised):

| region | addresses |
| --- | --- |
| dense array | TOP - i for the i-th table step, TOP = 2^256 - 1, i < 2^128 |
| sparse array | the key K itself, K < 2^176 with bits 32..35 of K zero |
| group records U0_g, U1_g, S_g | (g << 36) \| 2^32 \| k, k = 1, 2, 3 |
| scalars (END, VC), spill area of MATCH, output | 2^32 + [16, 2^14) |
| program code (< 2^18 instructions) | 2^33 + [0, 2^18) |

Disjointness: every key has bits 32..35 zero (Lemma 3), while every record,
scalar and code address has bit 32 or bit 33 set; records with g >= 1 are at
least 2^36, records with g = 0 are 2^32 + 1..3, below the scalars; code has bit
32 clear and records and scalars have it set; every non-dense address is below
2^177, while dense addresses exceed 2^256 - 2^128 - 1 > 2^255.

**Algorithm.**

1. Install the fixed registers and program constants; CC = TOP; VC = 0.
2. For g = 0..2^96-1: group setup (Section 2).
3. Repeat 9586980 times: a straight-line block of 64 batches, then the loop
   test (load END, compare END < CC, branch: 3 operations). Then 36 further
   straight-line batches, T &= PM (load PM, and: 2), and the tail batch, which
   evaluates all seven lanes and tables lanes 0..3 only. Here
   613566756 = 64 * 9586980 + 36 full batches and 4 tail lanes give exactly
   2^32 = 7 * 613566756 + 4 table steps per group.
4. A batch is the counted program of Section 4 followed by T = T + BC7.
5. MATCH (Section 5): each of the 448 table sites of a block has its own handler
   copy, which branches back to the instruction after its site, so no indirect
   jump is needed. A block has fewer than 64*298 + 448*160 = 90752 instructions;
   the 36 straight batches with their 252 handler copies fewer than
   36*298 + 252*160 = 51048; the tail batch with its handlers fewer than 925;
   setup, installation and loop code fewer than 546. All code together is
   below 90752 + 51048 + 925 + 546 = 143271 < 2^18 instructions.
6. After the last group, halt with failure.

The program halts after at most 2^128 table steps and at most 2^110
verifications. Section 8 prices this worst case.

## 4. The counted seven-lane batch program

Convention (that of scripts/reference_operation_costs.py and of the
our public package 3022205a and of 1c8c7c53): every executed 256-bit operation costs one,
including loads, stores, compares and branches; operands are registers; shift
amounts are instruction fields. One 256-bit word holds seven 32-bit payloads at
offsets 0, 36, ..., 216, with four guard bits after each; bits 252..255 are zero.

**Rotation.** For r in {7, 8, 12, 16},

    PROR(z, r) = ((z >> r) & LOW_{32-r}) | ((z & LOW_r) << (32-r))     5 operations.

If every slot of z is below 2^36, the first arm keeps bits r..31 of each slot
(bits of the next slot and the slot's own guard bits land at positions >= 32-r
and are masked off) and the second moves bits 0..r-1 to 32-r..31 inside the
slot. So each slot becomes ROR32 of its low 32 bits, normalised below 2^32.

**Body (tekkac, 1c8c7c53 Section 4, operation for operation).** With packed T
(lane j holds t + j), the body evaluates the round-1 tail, the four reduced
round-2 columns and the four diagonals with unreduced additions, and returns
o0 = a0^c8, o1 = a1^c9, o2 = a2^c10, o3 = a3^c11, o5 = b5^d13. It skips the
final b rotations of G(1,6,11,12), G(2,7,8,13), G(3,4,9,14) and the XORs for
o4, o6, o7. Count: 42 additions, 30 input XORs and 30 PROR (180), 5 output
XORs: 227 (and 60, or 30, shl 30, shr 30, add 42, xor 35).

**Lemma 2 (range and lanes).** The shipped `range_check` walks the exact
program and keeps a strict per-slot bound for every register (constants and T
lanes < 2^32; PROR results < 2^32; each addition adds bounds). Every addition
has bounded inputs and the largest addition result is below 9 * 2^32 < 2^36
(a3 is the largest, as in 1c8c7c53), so no carry crosses a slot boundary and
each payload's low 32 bits equal the scalar value mod 2^32. In full batches
t + j <= 7*613566756 - 1 < 2^32; after the last full batch the T advance may set
a guard bit (7q + 4..6 >= 2^32), and T &= PM restores lanes below 2^32 before
the tail batch.

**Key extraction (ours, 64 operations).** The key of lane j is tekkac's gapped
key K_j = o0 + 2^36 o1 + 2^72 o2 + 2^108 o3 + 2^144 o5 (key slots 0..4 hold
o0, o1, o2, o3, o5). Key slots are extracted in two sets, S = {0,1,2} and
S = {3,4}. For a set S and a lane group G with offset delta, one word is

    w = OR over k in S of shift((o_k & W_G), k - delta slots)

so lane j in G has its key slot k at word slot j - delta + k. A shift of w by
delta - j slots puts lane j's fields at key slots S; if a field of another lane
of G would also land in slots 0..7, an AND with M_S removes it. The plan used:

| S | lane groups (delta) | build | lane shifts | lane masks |
| --- | --- | ---: | ---: | ---: |
| {0,1,2} | {0}(0), {1,4}(1), {2,5}(2), {3,6}(2) | 4 x 7 = 28 | 4 | 3 |
| {3,4} | {1,3}(3), {0,5}(3), {2,4,6}(4) | 3 x 4 = 12 | 5 | 5 |

A build costs |S| ANDs, |S|-1 ORs and one shift per k != delta. The two parts
of every lane are ORed (7). Total 40 + 9 + 8 + 7 = 64 (and 26, or 18, shr 12,
shl 8). tekkac's direct per-lane extraction costs 97. (Our own search over
plans of this shape found nothing cheaper than 64; that search is not shipped
and no claim depends on it: the count 64 is that of the shipped program.)

**Lemma 3 (key).** Every field is ANDed with a 32-bit payload mask before any
slot shift, every shift is by a multiple of 36 bits, and every other-lane field
landing in slots 0..7 is masked off; so K_j is exactly the gapped key of lane j:
below 2^176, bits 32..35, 68..71, ... zero, and K_j = K_i iff the five selected
digest words are equal. Two messages with equal full digests have equal keys.

**The program.** The 227 + 64 ALU operations and the 7 table steps are
scheduled by our list scheduler (table steps kept in lane order 0..6) and
register-allocated onto r47..r63 without spills. The resulting straight-line
program is shipped verbatim as `PROG_FULL` (298 instructions) and the tail
version as `PROG_TAIL` (285 instructions: same body, lanes 0..3 only) in
experiments/b3r2_swar.py. It contains no load or store other than those inside
the 7 table steps. The worst batch:

| component | operations |
| --- | ---: |
| packed body | 227 |
| key extraction | 64 |
| 7 table steps, worst path (Section 5) | 63 |
| T = T + BC7 | 1 |
| **counted full batch** | **355** |
| tail batch: 281 ALU + 4 x 9 + T &= PM (2) | 319 |
| loop test per 64-batch block | 3 |

By opcode, the worst full batch is: ldr 14, str 14, xor 35, and 86, or 48,
shl 38, shr 42, add 43, sub 7, cmp 14, br 14. **Charge:** we charge 360
operations for every full and tail batch. Over a 64-batch block this covers
64 x 355 + 3 with more than 316 spare.

## 5. Pointer-free sparse-set table (ours)

CC is the address of the next dense entry; it starts at TOP = 2^256 - 1 and
decreases. One table step on key K (register r_k; scratch r_s, r_w):

    w = load [K]                         1   (the key word is the sparse address)
    f = (CC < w); branch !f -> INS       2
    q = load [w]                         1
    f = (q == K); branch f -> MATCH      2
    INS: store [K] <- CC                 1
         store [CC] <- K                 1
         CC = CC - ONE                   1
                                         9 through both tests; 6 on the early INS path;
                                         6 to MATCH (the handler writes a dummy entry)

INS falls through after the second test and falls through to the next
instruction afterwards. A declined MATCH (Section 5 handler, step 6) writes the
dummy dense entry `store [CC] <- K; CC = CC - ONE` and returns after its site.

**Invariant.** After j steps, CC = TOP - j; for every i < j the dense word
TOP - i holds the key k_i of step i (both for insertions and dummy entries);
for every key k first tabled at step i, sparse[k] = TOP - i, written once.

**Lemma 4 (lookup).** A step reaches MATCH iff K was tabled at an earlier step,
and then w = TOP - i where i is the first step with key K.
If K was first tabled at step i, then w = TOP - i > CC and load [w] = K: MATCH.
If K was never tabled, the word at address K was never written: addresses ever
written are sparse addresses of earlier keys (all different from K), dense
addresses (above 2^255 > K), and record, scalar and output addresses (bit 32 or
33 set; K has both clear). So w is arbitrary garbage. If w <= CC the step
inserts. If w > CC then w = TOP - i for some i < j, a written dense entry with
k_i != K (a dummy entry repeats a key that was tabled before it, hence also
!= K), so the second test fails and the step inserts. Garbage never yields a
MATCH; no zero-initialised memory is assumed.

**Lemma 5 (no displacement; decoding).** INS runs only for a key never tabled,
so sparse[k] is written once and always names the first message with key k.
Each group performs exactly 2^32 steps (Section 3) in t order (lanes in order),
so step i is message t = i mod 2^32 of group g = i >> 32 and NOT w = TOP - w = i.

**MATCH handler** (itemised; charged 2 compressions plus 1024 operations):

1. Save r47..r63 to the spill area (17 stores); VC: load, add, store, load
   the constant 2^110, compare, branch (6); if VC > 2^110, halt with failure.
2. Earlier message: i' = NOT w, g' = i' >> 32, t' = i' AND M (load M: 4);
   record addresses: g' << 36, three loads of the constants 2^32 | k and
   three ORs (7); three record loads (3); m15' = (t' - S') AND M (2):
   message words U0', U1' | (m15' << 224) (2). Total 18.
3. Current message: i = NOT CC and the same steps (18).
4. Distinctness of (U0, U1, m15) and (U0', U1', m15'): 3 compares, 2 ORs, 1 branch (6).
5. Two reference compressions (2 units); digest equality: 1 compare, 1 branch.
6. On equality: store the four output words (4 address constants, 4 stores),
   halt. Otherwise the dummy entry (2), restore r47..r63 (17 loads) and branch
   back (1).

At most 17 + 6 + 18 + 18 + 6 + 2 + 8 + 20 = 95 operations < 1024 (every
constant is loaded and counted; all addresses are 2^32 + small constants of
the program).

## 6. Correctness and success probability

**Correctness (no heuristic).** Any output pair was checked in handler steps 4-5
to consist of two distinct 64-byte messages with equal complete blake3-r2
digests: a valid collision.

**Failure events.** F3: two groups have identical m0..m14. F1: the N messages
contain no full-digest collision. F2': some message x has a full-digest partner
z processed before it, but the first message y with K_y = K_x has a different
digest from x. Fcap: more than 2^110 MATCH entries.

**Lemma 6.** If none of F1, F2', F3, Fcap occurs, the algorithm outputs a collision.
Proof. By not F3 and Lemma 1 all messages are distinct. By not F1 let x be the
first message in processing order with a full-digest partner z processed
earlier. If the algorithm has not halted before x, then K_z = K_x (Lemma 3), so
some step tabled K_x; by Lemmas 4-5 the step of x reaches MATCH with the record
of the first message y with K_y = K_x. By not F2', D_y = D_x. By not Fcap the
verification runs and outputs (y, x).

**Bounds.**

- Pr[F3] < C(2^96, 2) * 2^-480 < 2^-289, exactly.
- Under H1 (Section 7), treat the N digests as independent uniform 256-bit values:
  - Pr[F1] <= exp(-N(N-1)/2^257) = exp(-(1 - 2^-128)/2) < 0.6065307.
  - F2' needs distinct x, y, z with D_x = D_z and K_y = K_x: fewer than N^3/2
    triples, each of probability 2^-256 * 2^-160, so Pr[F2'] < 2^-33.
  - Each MATCH entry is a distinct pair (y, x) with equal 160-bit keys;
    E[#pairs] = C(N,2) * 2^-160 < 2^95, so by Markov Pr[Fcap] <= 2^-15.

In the model, Pr[F1 or F2' or Fcap] < 0.6065307 + 2^-33 + 2^-15 < 0.6065613,
so success > 1 - 0.6065613 - 2^-289 > **0.39343**. H1 (Section 7) allows the
real failure probability to exceed this model bound by at most 0.0034, i.e.
Pr[F1 or F2' or Fcap] <= 0.6099613 < 0.61; then success
>= 1 - 0.6099613 - 2^-289 > 0.39003 >= 0.39, the claimed value (jaazinn's
allowance of 0.0034).

**Partial justification of the model.** Within-group pairs are a 2^-96 fraction
of all pairs. A cross-group pair with the same t collides with probability
sum_d p_t(d)^2 >= 2^-256 (Cauchy-Schwarz over the uniform group words). H1
asserts the rest.

## 7. Heuristic H1 and declared experiments

**H1 (grouped digests behave like independent uniform values).** For the
message set of Section 1, the complete 2-round BLAKE3 digests of the 2^128
messages, and their 160-bit keys (o0..o3, o5, stored injectively in the gapped
176-bit representation), have failure probability Pr[F1 or F2' or Fcap] at
most the bound computed for independent uniform 256-bit values (0.6065613,
Section 6) plus 0.0034, i.e. at most 0.6099613 < 0.61.

H1 is score-critical for success_probability only; time and validity do not
use it. It is the premise of jaazinn's public package 0a5b7ae8 with tekkac's and our
160-bit key. The message set, the key information and the events are exactly
those of 3022205a and 1c8c7c53; only the evaluator and the table changed, and
both are exact (Lemmas 2-5), so H1 is unchanged.

**Experiments** (experiments/manifest.json, program experiments/b3r2_swar.py,
python-message-pairs-v1). Each trial runs the algorithm of Section 3 scaled to
N_t = 2^10 messages. In the three counted-path experiments every seven-message
batch is executed by an interpreter of the shipped register program PROG_FULL
on a 64-register file, followed by the T advance; the program's key register
is ANDed with the event mask restricted to o0..o3, o5 (the only scaling step) before the table
step, which is the literal transcript `table_step` of Section 5 over adversarial
garbage memory: once a dense entry exists, about half of the unwritten words
hold the address of a written dense entry (the w > CC case of Lemma 4). The
scaled index is i = g * per_group + t. A key match is re-hashed with an
independent reference compression before the pair is returned; the organizer
recomputes the masked event with the trusted digest. N_t^2 / 2^20 = 1 = N^2 / 2^256.

- `b3r2-swar-spread`: 32 groups x t = 0..31; 4 bits in each of o0, o1, o2, o3, o5.
- `b3r2-swar-single`: 1 group x t = 0..1023 (the most structured case); a
  different mask, again 4 bits in each of o0, o1, o2, o3, o5.
- `b3r2-swar-fullword`: 32 groups x t = 0..31, with the readable packed body in
  its evidence-only full mode (the three skipped b rotations performed, all
  eight words extracted); 3 bits in each of o0..o3 and 2 bits in each of
  o4..o7. This tests o4, o6, o7, which the counted program never computes.
- `b3r2-swar-keysub`: 32 groups x t = 0..31 on the counted path; the 20-bit
  event has 16 bits in the key words (4 in o0, 3 in each of o1, o2, o3, o5) and
  4 outside them (2 in o4, 1 in o6, 1 in o7), and the table key is the 16-bit
  restriction. Like the full-scale key (a projection of the 256-bit digest),
  the scaled key is a strict projection of the event, so key matches with
  differing event bits occur, the handler declines them and writes dummy dense
  entries, and later steps of the same key are answered by the first record
  only: the declined-MATCH path, the dummy-entry invariant of Lemma 4 and the
  scaled analogue of F2' are all executed.

Model value for the first three (1024 values, 20-bit event):
1 - prod_{i<1024}(1 - i/2^20) = 0.39327 (256 trials: 100.7, sd 7.8). For keysub
the uniform model is: 1024 independent uniform 20-bit values, key = 16-bit
projection, success iff some value equals on all 20 bits the first earlier
value with its key. With d distinct keys so far, a step is a new key with
probability 1 - d/2^16 and otherwise fails to succeed with probability 15/16;
the exact recursion over d gives 0.391796 (256 trials: 100.3, sd 7.8). It is
below 0.39327 by the scaled F2' effect (a later event partner hidden behind
the first record of its key; at full scale Pr[F2'] < 2^-33). A Monte Carlo of
this model (950000 trials, ours) gave 0.39174.

**Our local replay of the organizer runner** (experiments.runner.run_experiments,
the track's config_sha256, seed hashsmash-public-seed-v1, 256 trials; Docker
replaced by a local Python 3.12 subprocess because Docker was not available to
us; not organizer results): spread 101/256, single group 91/256, fullword
101/256, keysub 109/256 (model 100.3, +1.1 sd; up to 16 verifications and 16
dummy entries per trial); no repeated pairs; two byte-identical stdout runs
per experiment, 1.9-4.8 s each.

**Our additional runs (our seeds; 4096 trials per row; model 1610.8, sd 31.3).**
Every counted-path batch executed exactly 291 ALU operations; table steps took
6 or 9 operations; 0 to about 580 stale garbage pointers were read per trial.

| layout | mask | successes |
| --- | --- | ---: |
| spread | spread mask | 1669 |
| spread | single-group mask | 1644 |
| single | single-group mask | 1643 |
| single | spread mask | 1654 |
| spread, full mode | fullword mask | 1670 |
| single, full mode | fullword mask | 1631 |

The six rows pooled give 9911/24576 against 9665.0 (+3.2 sd), all rows at or
above the model. A second, independent seed set with 8192 trials per row (model
3221.7, sd 44.2) gave 3209 (spread), 3187 (single) and 3238 (spread, full mode):
9634/24576, -0.4 sd. Both sets together: 19545/49152 against 19330.1 (+2.0 sd).
Any excess is in the direction of more collisions than the model, which does
not lower the success probability; we report it rather than discard it.

keysub (our seeds; two independent seed sets of 4096 trials for each of the
spread layout and a single-group layout, the same mask; model 1604.8, sd 31.2
per row): spread 1604 and 1540, single group 1595 and 1580; together
6319/16384 against 6419.2 (-1.6 sd; the lowest row -2.1 sd). Every row
executed 291 ALU operations per batch; about 6 dummy entries per trial on
average (at most 22). On 300 of these seeds an independent implementation of
the same scaled algorithm on verifier/blake3.py blake3(m, 2) digests returned
identical outcomes (105 successes, identical pairs), so the shipped program
implements the scaled algorithm exactly. We report the deficit as observed; it
is within sampling error of the model at about 1.6 sd.

On 1024 identical seeds, this program and the program of our public package
3022205a returned identical outcomes (412 successes, identical pairs), so the
evaluator and table change nothing observable.

**Extrapolation and limitations.** The experiments test 20-bit projections with
2^10 messages; the claim applies the model to 256-bit digests, 160-bit keys
and 2^128 messages. Projections cannot detect structure visible only in
full-width equality. Organizer seeds are public. Each 256-trial experiment
resolves success only to about +-0.03, while the allowance above 0.39 is
0.0034 and is not statistically certified. Fcap is not exercised at scale (a
keysub trial has about 8 key-colliding pairs; at full scale the cap 2^110 is
2^15 times the model mean), so its bound rests on H1 and Markov only.

## 8. Total time, memory and claim fields

Let q = 613566756 = 64 * 9586980 + 36. Per group there are q + 1 batches, each
charged 360 operations, and 9586980 loop tests (3 each, inside the charge), plus
group setup charged 1024. Per MATCH entry: 2 units plus 1024 operations, for at
most 2^110 entries (the (2^110+1)-th halts in step 1). Installation (31
register constants and 12 stores, counted 43, plus writing the fewer than
2^18 code words) is charged 2^18 operations.

    T <= 2^96 * ((q+1) * 360 + 1024) / 430 + 2^110 * (2 + 1024/430) + 2^18/430
      <  0.1196181 * 2^128  <  2^124.93651

The claim is time_log2 = 124.937, the bound rounded up.

**Sensitivity** (log2 T for the same structure; bound rounded up):

| reading or charge | ops per batch | ops/message | log2 T |
| --- | ---: | ---: | ---: |
| exact count, direct reading (355 + 3/64, tail 319) | 355 | 50.72 | 124.917 |
| **claimed charge** | **360** | **51.43** | **124.937** |
| +1 per direct-addressed load/store and per ALU immediate | 355 (loop test 4) | 50.72 | 124.917 |
| also +1 per shift amount (80 shift immediates per batch) | 435 | 62.14 | 125.210 |
| tekkac's extraction (97) with this table | 388 | 55.43 | 125.045 |
| tekkac's batch charge for comparison | 417 | 59.57 | 125.149 |

The hot loop has no direct-addressed access and no ALU immediate except shift
amounts, so the second reading changes only the loop test. The last-but-two
row charges every shift amount as an extra operation; this is stricter than the
reference cost script, our public 3022205a and 1c8c7c53, which all treat shift
amounts as instruction fields.

**Memory** (unscored, reported). Dense addresses reach TOP = 2^256 - 1, so the
address span is 2^256 words = 2^261 bytes (a word-addressed RAM: 2^261 bytes
is the whole 2^256-word address space, the same reading as 1c8c7c53);
memory_log2_bytes = 261. Written:
at most 2^128 sparse words, exactly one dense word per table step (an insertion
or a dummy entry; a successful MATCH halts) and so at most 2^128 dense words,
3 * 2^96 record words,
fewer than 2^14 scalar/output/spill words and code below 2^18 words: less than
2^134.001 bytes.

**Other claim fields.** preprocessing_log2 = 10: installation (2^18
operations, about 2^9.25 units, which also covers writing the fewer than 2^18
code words of Section 3) is reported there and is also already inside T;
nonuniform advice 0; success_probability 0.39.

## 9. Relation to 1c8c7c53, 0a5b7ae8 and 3022205a

Same as tekkac's 1c8c7c53: message set, group constants, packed layout, the
227-operation body, the gapped key, the success analysis and the experiment
layouts and masks. Same as jaazinn's 0a5b7ae8: grouping, Briggs-Torczon table,
two-compression verification, H1.

| change against 1c8c7c53 (per batch) | ops |
| --- | ---: |
| interleaved extraction: 97 -> 64 (same keys) | -33 |
| sparse address = key (no K OR SB) | -7 |
| record = dense address, dense array growing down from TOP: no alignment AND (p = w & MC), no record OR, no R register | -14 |
| CC decrement replaces the record counter: 7 scalar R advances removed | -7 |
| counted batch 416 -> 355 | -61 |

Not used: zero-initialised memory; dropping the CC < w test (Lemma 4 needs it);
5kyguy's fixed-a3 message family (200fd0ea), which would save about 17 more
operations per batch in our count (15 in 5kyguy's) but needs a further
heuristic.

## Appendix A. Mechanical checks

**Shipped** (`python3 experiments/b3r2_swar.py --selftest 2000 3`, about 1 s):

- PROG_FULL on 1800 random batches and PROG_TAIL on 200 tail batches
  (t0 = 7q, lanes 4..6 wrapped by T &= PM) with random m0..m14 and t0:
  291 / 281 ALU instructions and 7 / 4 table steps on every batch; all 13400
  keys equal o0|o1<<36|o2<<72|o3<<108|o5<<144 of the independent reference
  compression; registers used r0..r63 only;
- readable packed body and extraction counted by a counting word type:
  (227, 64) on all 2000 batches, keys equal to the program's;
- the full mode equals all eight reference digest words for every lane;
- `range_check` on both programs: every addition stays below 9 * 2^32;
- group constants with counted message words: 244 operations;
- `table_step` under adversarial garbage, 100 runs x 256 steps with 12-bit keys:
  MATCH exactly when the key was tabled before, with the first step's dense
  address; paths cost 6 (fresh), 9 (stale pointer) and 6 (MATCH entry).

**Local, not shipped (ours).** A counted 64-register VM simulation of the
whole per-group schedule (install, group setup, unrolled 64-batch blocks with
their loop test, the 36 straight batches, T &= PM, the tail batch) against
verifier/blake3.py blake3(m, 2): 96 groups (group start, random middle and group
end), 23872 tabled keys and 672 full eight-word digests, 0 mismatches; 672/672
replays MATCH their own first record and decode to (g, t); after a group end
CC = TOP - (g+1) * 2^32. Worst batch 355, tail 319, loop test 3, setup 499
(its own grouped-variant verifier and ledger; the shipped selftest is the
independent stdlib re-implementation of the same program).
