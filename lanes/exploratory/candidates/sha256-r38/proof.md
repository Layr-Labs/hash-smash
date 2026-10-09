# SHA-256 r38: grouped round-skip birthday search, bit-sliced and physically scheduled

Lane: exploratory. Target: `sha256-r38-prefix-v1`. Attack class: ordinary
collision. Cost model `collision-frontier-v5`, C = 2728: one 38-round target
compression costs 1 unit; every other 256-bit RAM word operation costs 1/2728.

## 0. Claim, summary and credit

* Output: two distinct 55-byte messages whose complete 38-round SHA-256
  digests agree on all 256 bits (Section 6, unconditional).
* Time: at most 2^124.13389 units in every run (Section 8), on a 64-register
  256-bit word RAM in which every executed primitive, every load and every
  store is charged. Claimed `time_log2: 124.13389`.
* Success: at least 0.3905 under one heuristic, H1 (Sections 7, 11). Claimed
  0.39.
* Memory below 2^150 bytes (reported only); preprocessing under 2^9 units;
  advice zero (Section 9).

This revises our c839d33d (124.19796), which revised our 875a5083 (124.968). The message family, N, NB, the
pre-last-round key idea, the success argument and H1 are unchanged. What
changes is the evaluator's accounting and five exact savings. 875a5083
charged its bit-sliced circuit under a register-bank convention (one
placement per gate, operand reads free). Here the same kind of circuit is
emitted as a straight-line program for a 64-register machine, register-
allocated, and every load and store it executes is charged, as in jaazinn's
817d4440 (r37, 124.205), which built on 875a5083's circuit. Per batch of 256
messages the program executes exactly **48,091** operations (Section 3):
31,844 circuit gates, 4,077 transpose operations, 7,406 loads and 2,390
stores (circuit, transpose and sinks allocated as one program), 256 table
steps of 9, and 70 for batch setup and control: **187.85546875 per
message**. Five exact savings over 817d4440's 190.25 at r37 (our r37 twin:
178.80078125): the key is taken on the raw state words that the feed-forward
maps bijectively to the digest words, so no feed-forward adders are
computed; every multi-operand sum folds its constant and group-constant
addends (with K_t) into one group word computed once per group, which
removes whole per-batch carry chains; the per-batch addends of every sum are
added in a searched fixed order; carries are NOT-free in every polarity
case (majority self-duality for full adders, one AND with the sum's stored
word for mixed-polarity half adders); and a per-bit lock-step emission with
one furthest-next-use allocation over circuit, transpose and table sinks
brings the memory traffic down to the planes each round must read and
write.
No cryptanalytic weakness of SHA-256 is claimed. `baseline_improved` names
the nominal reference `sha256-r38-nominal-v2` (display value 128, not a
baseline or a bound); the track's displayed current best, 132, is the
organizer-authored merge-sort candidate shipped at f46ab58.

Credit (unpromoted ideas, their authors credited; none has reviewed this
package). jaazinn (blake3-r2 0a5b7ae8; sha256-r37 817d4440): the grouped
partial-evaluation birthday search, the never-initialised table and the
F1/F2/F3 analysis under H1; and, from 817d4440, the batch layout (one group
per batch, the lane index as the low 8 bits of u, 16 batch planes), the
column-lock-step emission, the 144-bit key with digest word f truncated to
16 bits, the zero-aware delta-swap transpose with a constant row, the
9-operation table step, and the 64-register machine with every load and
store charged. jungjipdo (sha256-r38 325d628d, 6a3c483e): the 55-byte
single-block domain on this track, keying on digest words fixed before the
last round, the tagged uninitialised table and the candidate cap.
may93182 (11c46f4d) and winglock (377eebd5, 982bf613): bit planes, the
delta-swap transpose and the tagged-id table lineage. ercumentyildirim
(c7fa1a56): computing only what the key needs. Ours: the bit-sliced SHA-256
circuit with constant folding and polarity flags (875a5083), the NOT-free
carries, the raw-state key, the folded sums and the addend order, the
emission order and the single allocation of Section 3, the counted program,
the experiments and any errors.

## 1. Target, messages, groups and the key

The target hashes a byte string with the standard SHA-256 IV, FIPS 180-4
padding, rounds 0..37 of the standard schedule and constants on every block,
feed-forward, and the full big-endian 256-bit digest. A 55-byte message pads
to exactly one block: W[0..13] carry the 55 message bytes and the byte 0x80,
W[14] = 0, W[15] = 440. Its digest is therefore the feed-forward output of a
single reduced compression on that block from the IV.

**Groups.** A group g has a prefix P_g of 13 uniform 32-bit words
W[0..12] (416 fresh coins). The message m(g, u), for u in {0, .., 2^24 - 1},
is m(g, u) = BE32(W[0]) || ... || BE32(W[12]) || BE24(u) (55 bytes), so
W[13] = (u << 8) | 0x80. Distinct (g, u) with distinct prefixes give
distinct messages. N = NB * 256 * 2^24 messages with NB =
78856234692123534151746250567 (N = 0.995306 * 2^128): G = 256 NB groups,
each a run of 2^16 batches of 256 messages, u = 256 b + L for batch index b
and lane L (Section 4). The processing order (group, b, L) is fixed in
advance and never depends on a digest.

**Key.** Write the state entering round t as (a_t, ..., h_t), so (a_0, ...,
h_0) = IV and (a_38, ..., h_38) is the state after round 37, and the digest
words as (A, B, Cw, D, E, F, G, H). Then Cw = a_36 + IV[2], D = a_35 +
IV[3], F = e_37 + IV[5], G = e_36 + IV[6], H = e_35 + IV[7]: adding a
constant modulo 2^32 is a bijection on 32-bit words, so two messages have
equal (Cw, D, G, H) and equal low 16 bits of F exactly when they have equal
(a_36, a_35, e_36, e_35) and equal low 16 bits of e_37 (the low 16 bits of
a sum depend only on the low 16 bits of the addends). The table key K of a
message is the 144-bit word K = a_36 || a_35 || e_36 || e_35 || e_37[0..15]
(bit layout in Section 3). These words depend only on rounds 0..36; the low
16 bits of e_37 need only bits 0..15 of round 36's T1. Round 37, the T2 half
of round 36 and bits 16..31 of its T1 half are never computed. Equal digests
give equal keys; equal keys are checked by recomputing both full digests
(Section 5.3).

## 2. Machine model and charging

Classical probabilistic 256-bit word RAM with **64 registers** (our stated
assumption; Section 8 gives the bound with 48 and with 32 allocatable
registers): three-address
operations on registers, immediate shift counts, and loads and stores with a
register address or a small immediate address. Every executed primitive is
one operation: add, subtract, AND, OR, XOR, NOT, shift, compare, branch,
load, store, RAND. Values in registers are read free; every other operand is
loaded and every spilled or persisted result is stored, and those loads and
stores are in the count. Instruction fetch is not charged; program text
counts as memory. All planes, spill slots and constants live below 2^24; the
table lives at [2^144, 2^145). Registers 0..57 are allocated to the circuit
and transpose by the allocator of Section 3; registers 58..63 hold the batch
id word, the loaded table entry, two temporaries, the batch counter and a
scratch value. The algorithm never reads memory it has not written, except
the table, whose contents are never trusted (Section 5.3). A scalar
compression (verification only) costs 1 unit plus at most 300 operations.

## 3. The counted batch program

A batch is 256 messages of one group with u = 256 b + L, L = 0..255. Plane j
of a 32-bit word X is the 256-bit word whose bit L is bit j of X for message
L; a word is 32 planes. Inputs of the batch program: the group planes (the
planes of the state entering round 13, of the group schedule words with
their K sums, of the Maj reuse word and of every gate whose two inputs are
group planes, each 0 or all-ones for the batch's group, written once per
group, Section 4.1); eight fixed lane planes (bit L of lane plane i is bit i
of L: u bits 0..7, which are W13 bits 8..15); sixteen batch planes (all-ones
or zero by bit i of b: W13 bits 16..31); and the constant 0x80 in W13 bits
0..7.

**Signals and gates.** Every intermediate is a stored plane with a public
polarity flag (the true plane is the stored word XOR flag*all-ones), so NOT,
XOR with a constant, and every rotation or shift by a constant cost nothing
(a rotation renames planes; a shift renames planes and supplies constant-0
planes). Gates are 256-bit XOR, AND and OR, one operation each; the per-batch
program contains no NOT. Identities, applied once when the program is written:

* XOR of two stored signals: one XOR, flags added mod 2. AND with flags
  (0,0): one AND; (1,1): one OR with flag 1.
* Full adder on stored x, y, c, with x chosen as the odd-polarity operand
  (two of three flags always agree), p = y XOR c, sum = x XOR p, and
  carry = (y AND c) OR (p AND x) when flag(x) = flag(y) = 0;
  carry = NOT[(Y AND C) OR (P AND X)] on the stored words when all three
  flags are 1; carry = (y OR c) XOR (p AND X) when flag(x) = 1 and
  flag(y) = flag(c) = 0; carry = NOT[(Y OR C) XOR (P AND X)] when
  flag(x) = 0 and flag(y) = flag(c) = 1. The last three follow from the
  first by maj(x,y,c) = (y OR c) XOR ((y XOR c) AND NOT x) and the
  self-duality maj(NOT x, NOT y, NOT z) = NOT maj(x, y, z). Five operations,
  no materialised NOT, in every case.
* Half adder (two stored inputs u, v) and constant operand bit: the sum's
  stored word S = U XOR V is computed anyway. When the flags agree the carry
  is U AND V (or U OR V with both flags 1). When they differ the carry is one
  AND with S: for u = U, v = NOT V, u AND v = U AND NOT V = U AND (U XOR V);
  for u = NOT U, v = V, u OR v = NOT (U AND (U XOR V)), a flag flip (one
  AND with the stored word of the flag-1 operand). A
  constant operand bit k gives sum = x XOR c (flag flipped if k = 1) and
  carry = x AND c (k = 0) or x OR c (k = 1) by the same rule. Two
  operations, no NOT, in every case.
* Folded sums. Every multi-operand sum modulo 2^32 (the schedule word
  W_t = sigma1(W_{t-2}) + W_{t-7} + sigma0(W_{t-15}) + W_{t-16}, T1 = h +
  Sigma1(e) + Ch + K_t + W_t, T2, e' = d + T1, a' = T1 + T2) first adds its
  constant and group-constant addends, with K_t merged into that word
  whenever one exists, in group gates (once per group); the per-batch
  program adds only the message-dependent addends and that single group
  word. Whole per-batch carry chains disappear: the schedule words W22, W24,
  W26, W27, W28, W30 and W32 and T1 of rounds 13-16 (whose h, d and W are
  group values). Modular addition is associative and commutative, so the
  sums are unchanged.
* Addend order. The per-batch addends of each sum are added in one fixed
  order chosen by a coordinate-descent search over static operation counts
  (never over a digest): the folded group word first; T1 as K/W, h, Ch,
  Sigma1; the schedule as W_{t-16}, W_{t-7}, sigma1, sigma0; Maj before
  Sigma0 in T2.
* Ch(e, f, g) = g XOR (e AND (f XOR g)), or f XOR (NOT e AND (f XOR g)),
  whichever has equal flags at the AND: 3 operations. Maj uses whichever of
  b XOR ((a XOR b) AND (b XOR c)), a XOR ((a XOR b) AND (a XOR c)),
  c XOR ((a XOR c) AND (b XOR c)) has equal flags at the AND, reusing the
  previous round's a XOR b as this round's b XOR c: 3 or 4 operations.
* Sigma0, Sigma1: two XORs per bit; sigma0, sigma1: two XORs per bit, one
  where SHR supplies a zero.

**Emission order (column lock step).** For each round t = 13..35 and bit
j = 0..31, in this order: bit j of the dependent schedule word W_t, Sigma1(e)[j],
Ch[j], the T1 chains (addends in the order of the addend-order rule),
Maj[j], Sigma0(a)[j], the T2 chain, a_{t+1}[j], then e_{t+1}[j]; then round
36 bits 0..15 of W_36, Sigma1, Ch, the T1 chains and e_37. Every carry chain stays open across the bit loop, so at
any point the live set is a few carries, the current bits and the planes the
next bits read. Dead
code elimination removes everything the key does not need (bits 16..31 of
round 36's T1 chains and all of its T2).

**Hoisting.** A gate whose inputs are all group planes or lane planes is
computed once per group (23,766 gates, bit-sliced over the 256 lanes, which
includes rounds 0..12 and the folded group words) and its plane written to memory; the batch loads it
like any input.

**Register allocation.** The circuit, the transpose and the 256 table
sinks are one straight-line SSA program, allocated as a whole onto registers
0..57 by furthest-next-use eviction with a clean-first tie-break, so key
planes still in registers when the circuit ends go straight into the
transpose. The 8 swap masks and the all-ones row are memory words loaded
like any operand when needed: an operand not in
a register is loaded (1 operation); an evicted value that is used later and
is not already in memory is stored first (1 operation); dead operands are
freed before the result is placed; inputs are loaded at every use that
misses the registers. The emitted program uses at most 58 circuit
registers and never reads an unwritten word.

**Transpose.** The 144 key planes, in the order a_36 (planes 0..31), a_35
(32..63), e_36 (64..95), e_35 (96..127), e_37 bits 0..15 (128..143), are
rows 111..254 of a 256 x 256 bit matrix (plane i is row 111 + i); row 255 is
the constant all-ones plane and rows 0..110 are zero. A stored plane with flag 1 contributes its
stored word, so the transposed key is K XOR pol for a fixed public constant
pol: an injective relabelling, harmless for collision detection. The
delta-swap transpose swaps index bit k of rows and columns for k = 0..7:
for rows i and i + 2^k (bit k of i clear) with mask m_k of the columns whose
bit k is clear, t = ((a >> 2^k) XOR b) AND m_k; b' = b XOR t; a' = a XOR
(t << 2^k) (6 operations); 3 when the lower row is zero (a = 0: t = b AND m_k,
a' = t << 2^k, b' = b XOR t) and 4 when the upper row is zero (b = 0:
t = (a >> 2^k) AND m_k, b' = t, a' = a XOR (t << 2^k)). Phase 1 applies
k = 0..4 inside the non-zero 32-row blocks in registers; phase 2 applies
k = 5..7 to 8-row sets and hands each finished row (the key word Kw of
message L: key bits at 111..254, bit 255 set, bits 0..110 zero) to the
table sink. Phase 1 processes the non-zero blocks in the order 6, 3, 4,
7, 5. 4,077 transpose operations per batch; its loads and stores (masks,
the all-ones row, spilled rows) are counted with the circuit's in the
ledger.

**Table sink** (9 per message): idx = Kw >> 111; e = LOAD T[idx]; x = Kw
XOR BIDL; y = x XOR e; z = y >> 128; compare z with 0 and branch to
CANDIDATE if equal; STORE T[idx] = x; BIDL = BIDL + 1. Batch setup and
control: the 16 batch planes (4 each), the batch id word BIDL (load the
stored group word, shift b, OR: 3) and the loop (3): 70.

**Ledger (one batch of 256 messages, exact; printed by the self-test):**

| part | operations |
|---|---:|
| circuit gates (no NOT) | 31,844 |
| transpose operations | 4,077 |
| loads (circuit 7,191, transpose 215, incl. masks and the all-ones row) | 7,406 |
| stores (circuit 2,281, transpose 109) | 2,390 |
| table sinks, 256 x 9 | 2,304 |
| batch setup and loop | 70 |
| **total** | **48,091** |

By instruction: XOR 21,663, AND 7,385, OR 5,514, shifts 1,359 (the
transpose's), loads 7,406, stores 2,390, sinks 2,304, setup 70.

187.85546875 per message. The counted program is in the experiment file
(Section 10, Appendix A); its self-test regenerates the program, runs it on a
random group and batch index through the counting VM, compares all 256 key
words and transposed addresses with the reference digests, and asserts the
total 48,091 (r37 twin: 45,773).

## 4. Groups, batches and ids

Group g (0 <= g < G = 256 NB) runs batches b = 0 .. 2^16 - 1; batch b holds
messages u = 256 b + L, L = 0..255, in lane L. The message id is
id = g * 2^24 + b * 2^8 + L (below 2^128 since G < 2^104).

### 4.1 Group setup (once per group)

Draw two uniform 256-bit words r0, r1 and store them at PT[g]; unpack
W[0..12]; write the 416 prefix planes (shift, AND 1, negate, store: 4
operations per plane) and evaluate the 23,766 hoisted gates bit-sliced
(rounds 0..12, the group schedule words with their K sums, and every later
gate whose inputs are all group or lane planes; 2 loads, 1 gate (2 for the 13 group gates that are AND-NOT), 1 store
each); form and store
the word (RTAG << 128) OR (g << 24), from which each batch forms BIDL by a
load, a shift and an OR. At most 2^17 operations per group, i.e. below 2^-7
per message.

## 5. Algorithm

### 5.1 Once per run

Draw a uniform 128-bit tag RTAG (one RAND word). Write the 8 masks m_k,
the all-ones plane and the 8 lane planes (under 2^12 operations). The table
T of 2^144 words at addresses [2^144, 2^145) is never initialised.
Candidate cap V = 2^112.

### 5.2 Run

    for g = 0 .. G-1:
        group setup (4.1)
        for b = 0 .. 2^16-1:
            write the 16 batch planes; BIDL = (RTAG << 128) OR (g << 24) OR (b << 8)
            run the batch program (Section 3); its 256 table sinks
            store x = Kw XOR BIDL or branch to CANDIDATE; BIDL = BIDL + 1
    halt with failure

The 256 sinks of a batch run in the phase-2 order of the transpose (rows
r0 + 32k for r0 = 0..31, k = 0..7), so the n-th sink (n = 0..255) handles
lane L = rotr8(n, 3) (rotation of the 8-bit index right by 3) and stores
id = g * 2^24 + b * 2^8 + n with n = rotl8(L, 3): the lane field of a
stored id is a fixed public permutation of the lane, decoded by L =
rotr8(n, 3). The id stays below 2^128, so the increments never carry into
the tag. The entry of a message is
x = Kw XOR BIDL: bits 0..110 hold id bits 0..110, bits 111..127 hold key
bits XOR id bits 111..127, bits 128..254 hold key bits XOR RTAG, bit 255
holds 1 XOR RTAG's top bit. Two messages in the same slot share key bits
111..254, so the occupant's id is recovered exactly: bits 0..110 of e, and
bits 111..127 of e XOR Kw.

### 5.3 Candidates

CANDIDATE: increment a counter v; if v > V halt with failure. Recover the
occupant's id as id' = (e XOR Kw) mod 2^128 (Section 5.2), its group
g' = id' >> 24, b' = (id' >> 8) mod 2^16 and lane L' = rotr8(id' mod 2^8,
3) (Section 5.2), so u' = 256 b' + L' (the current message's (g, b, L) is
known); rebuild both 55-byte messages from PT (at most 200
operations), check that they differ (equal only in event F3: halt with
failure), compute both complete reference digests (2 units + 600) and
compare all eight words (20). If equal, output the pair and halt; otherwise
continue with the pending store. One candidate costs at most 2 units plus
1,000 operations, charged 3 units. Garbage: for a never-written slot the
test z = 0 requires bits 128..255 of the garbage word to equal Kw XOR
(RTAG << 128) there, probability 2^-128 per probe over RTAG alone. For a
genuine occupant with the same slot, bits 128..255 of x and e agree, so the
test fires on every genuine match.

## 6. Every output is a collision (unconditional)

An output is produced only after both messages were rebuilt from their ids,
found distinct, and both full 38-round digests were recomputed by the
reference compression and found equal. Bit slicing, the raw-state key and
the transpose change how a key is computed, not which messages collide;
Section 10's checks confirm the program, but correctness of outputs does
not rely on them.

## 7. Success probability

The run halts at the first successful verification. Failure events:

* **F3**: two groups have equal prefixes. Pr[F3] <= G^2/2 * 2^-416 < 2^-209.
* **F1**: no two of the N messages have equal digests.
* **F2**: for some colliding pair (a, b), a processed before b, a message c
  with a's 144-bit key and a different digest is stored between a
  and b (the slot then holds c when b arrives and the pair is lost: either
  no candidate, or a false candidate on (b, c)).
* **F4**: the candidate counter reaches V = 2^112.
* **F5**: more than 2^61 garbage candidates occur.

**Lemma 7.1.** If none of F1-F5 occurs, the run outputs a collision. Take a
colliding pair (a, b), a first, and suppose no earlier collision was
output. When a is processed it is stored in its slot (a candidate on a
garbage or different-digest occupant fails and the store proceeds). By
not-F2 the slot holds a's entry when b arrives; b's key word agrees with
a's on bits 111..255, so z = 0, the ids decode (with the lane permutation of Section 5.2) to a
and b, which differ
(not-F3), and the recomputed digests agree: output. Not-F4 and
not-F5 exclude a halt at the cap before that.

**Heuristic H1 (declared; equivalent text in claim.json).** For the events
F1, F2 and F4, the N digests of the grouped message set {m(g, u)}
(independent uniform prefixes P_g, all u in {0,1}^24, processed in the fixed
order of Sections 4 and 5.2: group by group, batch by batch, and within a
batch lanes in the order L = rotr8(n, 3), n = 0..255) behave like N independent uniform 256-bit values:
Pr[F1] <= exp(-N(N-1)/2^257), Pr[F2] <= N^3/6 * 2^-396, and the number Y
of pairs with equal 144-bit keys and different digests has E[Y] <= N^2/2^145
and Var[Y] <= N^2/2^145.

Under H1, with x = N(N-1)/2^257 >= 0.495316: Pr[F1] <= exp(-x) <= 0.609378;
Pr[F2] < 2^-14.5, we use 2^-13; E[Y] < 2^111, so Pr[F4] <= Var[Y]/(V -
E[Y])^2 < 2^111/2^222 = 2^-111 (Chebyshev); Pr[F5] <= 2^-61 by Markov
(expected garbage candidates N * 2^-128 < 1, over the tag alone, without
H1, on the premise that the uninitialised contents of T are independent
of RTAG, as in jaazinn's and jungjipdo's tables); Pr[F3] < 2^-209. NB is the smallest value for which 1 -
exp(-N(N-1)/2^257) - 2^-13 - 2^-209 - 2^-100 - 2^-61 >= 0.3905 (the script
in Appendix B checks this with 60-digit arithmetic). So Pr[success] >=
0.3905 under H1, claimed **0.39**.

**Rigorous partial support (jaazinn's argument, in aggregate form).** For two
groups g != g', let q(v) = sum over u of Pr[digest of m(g, u) = v] over the
uniform prefix. The two groups' prefixes are independent, so the expected
number of colliding pairs between them is sum over v of q(v)^2 >= (sum over
v of q(v))^2 / 2^256 = 2^48 / 2^256 by Cauchy-Schwarz. Within-group pairs
are a 2^-104 fraction of all pairs. The expected number of colliding pairs
is therefore at least (1 - 2^-104) N(N-1)/2^257 > 0.4953 without any
heuristic. H1 is needed for the second-moment behaviour behind Pr[F1], for
F2 and for Y. Within a group, rounds 0..12 and the state entering round 13
are identical for all 2^24 messages, which differ only in W[13]; 24 further
rounds with the full schedule follow. This is a stronger structure than
independent sampling, and is the reason H1 is a heuristic.

## 8. Total charged time (worst case, every run)

| Phase | Count | Units each | Bound |
|---|---|---|---:|
| Batches | N / 256 | 48,091 / 2728 | N * 187.85546875 / 2728 |
| Group setup | G = 256 NB | <= 2^17 / 2728 | < 2^109.6 |
| Candidates | <= V + 2^61 + 1 | 3 | < 2^113.6 |
| Once per run | 1 | 2^12 / 2728 + 3 | < 2^2 |

    T <= N * 48091/(256 * 2728) + 256 NB * 2^17/2728 + (2^112 + 2^61 + 1) * (2 + 1000/2728) + 2^12/2728.

log2(N * 48091/(256 * 2728)) = 124.13306; the other terms add a relative
2^-10.78 (0.00082 bits). **log2 T <= 124.133883 < 124.13389**, the claimed
`time_log2` (the integer certificate of Appendix B evaluated at 10^-5 and
rounded up). Every batch, every load and store, every group setup, every
candidate up to the cap, the garbage candidates and the output are included;
there is no other precomputation, no stored collision, no parameter search
and no repetition.

Sensitivity (the same program re-allocated and re-executed):

| reading | per message | log2 T |
|---|---:|---:|
| **64 registers, every load and store charged (claimed)** | **187.86** | **124.13389** |
| 48 allocatable registers (+6 reserved) | 190.35 | 124.153 |
| 32 allocatable registers (+6 reserved) | 195.63 | 124.192 |
| loads and stores free (reference only, not claimed) | 149.59 | 123.805 |
| register-bank reading of 875a5083 (one placement per gate, operand reads free; that package's own circuit) | 335 | 124.968 |

jungjipdo's 6a3c483e charges a 7-lane SWAR batch at 217.14 operations per
message (124.351) under the same machine; the difference here is bit
slicing (free rotations, 5-gate adders over 256 lanes), not a different
model.

## 9. Memory, preprocessing, advice

T: 2^144 words = 2^149 bytes at addresses [2^144, 2^145), an address span
of 2^145 words = 2^150 bytes. PT: 2 G words < 2^110 bytes. Group planes and
hoisted gate planes: under 2^16 words per group, rewritten per group, under
2^22 bytes resident. Program text, spill slots and registers: under 2^24
bytes. Address span under 2^150.01 bytes, resident data under 2^149.01 bytes:
`memory_log2_bytes: 150` (reported only). Preprocessing:
generating the fixed program once (under 2^20 operations = 2^8.6 units):
`preprocessing_log2: 9`, inside the spare of T. Advice: zero.

## 10. Experiments and evidence

Five `python-message-pairs-v1` experiments, declared for organizer
execution, share one stdlib program, `experiments/grouped_search_phys.py`.
It contains the counted program of Section 3 (generator, dead-code
elimination, allocator, counting VM, transpose and table sinks) and a fast
evaluator of the same circuit over 256 lanes that may belong to different
trials.

* **Counted witness.** In trial 0 of every experiment the program runs the
  counted batch on one group and one batch index drawn from the trial seed:
  the VM, a register machine with 58 + 6 physical registers that reads
  operands by register number, executes the single allocated program
  (circuit, transpose with its mask and row loads, and the 256 table sinks);
  it compares the 144 key planes with the program's scalar reference and
  every sunk row with the transpose of the stored planes (K XOR pol, pol the
  public polarity constant), aborts the experiment on any mismatch, and
  asserts the exact total 48,091. Its ledger
  is reported in the observations (untrusted numbers; the organizer's
  recomputation of every returned pair on the real target is the evidence).
* `r-bs-fullwidth-equivalence` (12-bit mask on digest word H): one batch of
  256 lanes from the trial seed; four lanes are checked in full against the
  scalar reference; returns two lanes agreeing on the masked bits.
* Four scaled searches with N_t = 512 messages per trial and an 18-bit key
  (the low 18 bits of H, a projection of the 144-bit key): `r-bs-full-width`
  (256 groups x 2 u), `r-bs-spread` (16 x 32), `r-bs-single-group`
  (1 x 512), `r-bs-high-z` (4 x 128 with the varying u bits at 17..23). The
  uniform model gives success 1 - prod(1 - i/2^18, i < 512) = 0.3931 per
  trial (100.6 +- 7.8 per 256 trials). Several trials share one 256-lane
  batch of the fast evaluator, each owning its own lanes.

Local runs, all reported: our dev harness with our own seeds (256 trials per layout) gave 106, 98, 97 and 92 successes; the organizer's own Docker executor run locally with the public seed (`hashsmash-public-seed-v1`, two runs each, byte-identical output) gave 93, 105, 105 and 105, and 256/256 on the equivalence check, with the trial-0 witness asserting 48,091 in every experiment (v3 program). A pre-registered larger run with our seeds (8,192 trials per layout, every pair re-verified with the reference digest, no bad pair; run with the v2 program, whose fast evaluator is functionally identical to v3's: the same seeds return identical pairs, checked on 5 x 256 trials) gave 3181, 3315, 3228 and 3282 against the model's 3220 +- 44 (largest deviation +2.1 sigma, in the spread layout).

The experiments test the circuit, the counted program and the scaled
birthday law on the real reduced-round target; they cannot certify the
full-width second moment, F2 or the 0.0005 allowance.

## 11. Heuristics (complete list)

H1 only (Section 7), score-critical, used only for the success probability.
Correctness of every output and all resource bounds are unconditional.

## 12. Limitations

* H1 is unproved; within a group the state entering round 13 is shared by
  2^24 messages.
* The 64-register machine is our stated assumption (Section 8: 48 allocatable registers
  124.153).
* The organizer seeds are public; scaled runs resolve the success frequency
  to about +-0.03 at 256 trials.
* Memory is far above the organizer baseline's and is reported, not scored.

## 13. Prior work

jaazinn 0a5b7ae8, 817d4440; jungjipdo 325d628d, 6a3c483e; may93182
11c46f4d; winglock 377eebd5, 982bf613; ercumentyildirim c7fa1a56; our
875a5083, c839d33d; the organizer-authored sha256-r38 merge-sort candidate at f46ab58
(132).

## Appendix A. The counted program

The per-batch program whose operations Section 8 charges is generated, register-allocated and executed
by the declared experiment program itself; nothing in the ledger is a cost-model-only figure.

1. **Generator** (`build(R, "counted")`). A symbolic SHA-256 over signals: a public constant bit, or a
   stored plane with a public polarity flag (NOT and XOR with a constant are flag flips). Inputs are the
   416 prefix planes (group constants), the 8 fixed lane planes (W13 bits 8..15) and the 16 batch planes
   (W13 bits 16..31). Gates are XOR, AND and OR (no NOT is emitted). Every multi-operand sum has its constant
   and group-constant addends folded into one group word, and its per-batch addends added in the fixed
   order of Section 3. Rounds are emitted in column lockstep: for each round t and bit j, the schedule word
   W_t, the T1 chains, the T2 chain, a_t and then e_t, each by the polarity-aware full adder, the NOT-free
   carries, Ch and Maj of Section 3. Round R-1 is not emitted; round R-2 emits only bits 0..15 of its
   e-half. The outputs are the 144 key planes: state words a, b, e, f entering round R-2 and e[0:16]
   entering round R-1.
2. **Dead-code elimination** (`live_gates`): only gates reachable from the 144 outputs survive; gates whose
   inputs are all group constants or lane planes are group work (computed once per group of 2^24 messages,
   stored, loaded by the batch like inputs); the rest is the per-batch circuit.
3. **Program** (`build_program`): the per-batch circuit, the zero-aware delta-swap transpose (rows 0..110
   zero, 111..254 the key planes, 255 all-ones; 6 ops per swap, 3 when the lower row is zero, 4 when the
   upper row is zero, decided from the row layout; phase-1 blocks in the order 6, 3, 4, 7, 5) and the 256
   table sinks are emitted as ONE straight-line SSA program; the 8 masks and the all-ones row are memory
   words read like any operand.
4. **Allocator and VM** (`allocate2`, `counted_witness2`): one linear pass with 58 physical registers;
   an operand not in a register is loaded (1 op); when no register is free the value with the furthest
   next use is evicted, clean values first, and an evicted value still needed and not yet in memory is
   stored (1 op); operands dead after an instruction free their register before the result is placed.
   Instructions carry register numbers and the VM reads operands by register number (a stale register
   aborts). The batch setup (16 batch planes x 4, BIDL = (RTAG << 128) | (g*2^24 + b*2^8) in 3, loop 3:
   70) is written directly and charged by count; the VM evaluates the group gates (not charged per batch)
   and executes the whole allocated program on registers, including every sink (the sink's internals and
   the 6 reserved registers are not register-modelled; the sink is charged 9): idx = Kw >> 111 (addresses in [2^144, 2^145)); e = LOAD T[idx]; x = Kw ^ BIDL; y = x ^ e;
   z = y >> 128; compare; branch; STORE T[idx] = x; BIDL = BIDL + 1 (9 ops; the id stays below 2^128).
   Every stored entry is decoded back to its (g, b, L) through the lane permutation and its run tag. The batch is one seeded prefix, one seeded 104-bit group index and one seeded 16-bit batch
   index, 256 lanes; never-written slots return seeded garbage and a z = 0 on garbage is counted.
5. **Self-test**: the 144 key planes are compared with the scalar reference (itself checked against
   `verifier/hash_functions.py` in our local harness) and every sunk row with the transpose of the stored
   planes; any mismatch, or a total different from the charged 45,773 (R = 37) / 48,091 (R = 38), aborts
   the experiment with a nonzero exit. The witness runs in trial 0 of every declared experiment; its ledger
   goes into that trial's observations (untrusted numbers).
6. **Run**: `python3 -I experiments/grouped_search_phys.py < request.json` (organizer executor), or the
   local harness `python -I dev_run_phys2.py` (reference check, five experiments x two round counts x 256
   trials, every returned pair re-verified with the organizer verifier, two runs byte-identical).

## Appendix B. Certificate script

`cert.py` (stdlib `decimal` at 60 digits and exact integers; listed in full
below): (1) finds NB as the least batch count with success bound 1 -
exp(-N(N-1)/2^257) - 2^-13 - 2^-209 - 2^-100 - 2^-61 >= 0.3905 and prints it
(78856234692123534151746250567, N = 0.995306 * 2^128, bound 0.3905000...);
(2) forms T_num = N * 48091 + G * 2^17 * 256 + (2^112 + 2^61 + 1) * (2 * 2728
+ 1000) * 256 + 2^12 * 256, so that T = T_num / (256 * 2728), and checks
T_num^100000 < (256 * 2728)^100000 * 2^12413389, i.e. T < 2^124.13389, by
exact integer comparison (True), and prints log2 T = 124.133883.

```python
import sys
from decimal import Decimal, getcontext
getcontext().prec = 60
R = int(sys.argv[1]) if len(sys.argv) > 1 else 38
OPS, C, CLAIM5 = {38: (48091, 2728, 12413389), 37: (45773, 2644, 12410776)}[R]
TWO = Decimal(2)
def success_bound(NB):
    N = Decimal(NB) * TWO**32
    x = N * (N - 1) / TWO**257
    return 1 - (-x).exp() - TWO**-13 - TWO**-209 - TWO**-100 - TWO**-61
lo, hi = 1, 2**96
while lo < hi:
    mid = (lo + hi) // 2
    if success_bound(mid) >= Decimal("0.3905"): hi = mid
    else: lo = mid + 1
NB = lo; N = NB * 2**32; G = NB * 256; V = 2**112
T_num = N * OPS + G * (2**17) * 256 + (V + 2**61 + 1) * (2 * C + 1000) * 256 + (2**12) * 256
print("NB", NB, "N/2^128", Decimal(N) / TWO**128, "bound", success_bound(NB))
print("log2 T =", (Decimal(T_num) / (256 * C)).ln() / TWO.ln())
print("T < 2^%.5f :" % (CLAIM5 / 1e5), T_num ** 100000 < ((256 * C) ** 100000) << CLAIM5)
```
Output (R = 38): NB 78856234692123534151746250567, N/2^128 0.9953056...,
bound 0.3905000..., log2 T = 124.133882..., `T < 2^124.13389 : True`.
