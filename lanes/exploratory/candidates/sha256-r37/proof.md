# SHA-256 r37: grouped round-skip birthday search, bit-sliced and physically scheduled

Lane: exploratory. Target: `sha256-r37-prefix-v1`. Attack class: ordinary
collision. Cost model `collision-frontier-v5`, C = 2644: one 37-round target
compression costs 1 unit; every other 256-bit RAM word operation costs 1/2644.

## 0. Claim, summary and credit

* Output: two distinct 55-byte messages whose complete 37-round SHA-256
  digests agree on all 256 bits (Section 6, unconditional).
* Time: at most 2^124.17421 units in every run (Section 8), on a 64-register
  256-bit word RAM in which every executed primitive, every load and every
  store is charged. Claimed `time_log2: 124.17421`.
* Success: at least 0.3905 under one heuristic, H1 (Sections 7, 11). Claimed
  0.39.
* Memory below 2^150 bytes (reported only); preprocessing under 2^9 units;
  advice zero (Section 9).

This revises our abaa09ae (124.947). The message family, N, NB, the
pre-last-round key idea, the success argument and H1 are unchanged. What
changes is the evaluator's accounting and three exact savings. abaa09ae
charged its bit-sliced circuit under a register-bank convention (one
placement per gate, operand reads free). Here the same kind of circuit is
emitted as a straight-line program for a 64-register machine, register-
allocated, and every load and store it executes is charged, as in jaazinn's
817d4440 (r37, 124.205), which built on our circuit. Per batch of 256
messages the program executes exactly **47,932** operations (Section 3):
31,751 circuit gates, 7,079 loads and 2,178 stores of the circuit, 4,077
transpose operations with 313 loads (8 of them the delta-swap masks) and 160
stores, 256 table steps of 9, and 70 for batch setup and control: **187.234375
per message**. Three exact
savings over 817d4440's 190.25 on this track (our r38 twin: 196.390625, 124.19796): the key is
taken on the raw state words that the feed-forward maps bijectively to the
digest words, so no feed-forward adders are computed; the full adder is
NOT-free in all four polarity cases by the self-duality of the majority; and
a per-bit lock-step emission with clean-first eviction brings the memory
traffic to the floor set by the input and output planes of each round.
No cryptanalytic weakness of SHA-256 is claimed. `baseline_improved` names
the nominal reference `sha256-r37-nominal-v2` (display value 128, not a
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
store charged. jungjipdo (sha256-r37 f0065dce, 383bad42): the 55-byte
single-block domain on this track, keying on digest words fixed before the
last round, the tagged uninitialised table and the candidate cap.
may93182 (11c46f4d) and winglock (377eebd5, 982bf613): bit planes, the
delta-swap transpose and the tagged-id table lineage. ercumentyildirim
(c7fa1a56): computing only what the key needs. Ours: the bit-sliced SHA-256
circuit with constant folding and polarity flags (abaa09ae), the NOT-free
full adder in all four polarity cases, the raw-state key, the emission order
and eviction policy of Section 3, the counted program, the experiments and
any errors.

## 1. Target, messages, groups and the key

The target hashes a byte string with the standard SHA-256 IV, FIPS 180-4
padding, rounds 0..36 of the standard schedule and constants on every block,
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
h_0) = IV and (a_37, ..., h_37) is the state after round 36, and the digest
words as (A, B, Cw, D, E, F, G, H). Then Cw = a_35 + IV[2], D = a_34 +
IV[3], F = e_36 + IV[5], G = e_35 + IV[6], H = e_34 + IV[7]: adding a
constant modulo 2^32 is a bijection on 32-bit words, so two messages have
equal (Cw, D, G, H) and equal low 16 bits of F exactly when they have equal
(a_35, a_34, e_35, e_34) and equal low 16 bits of e_36 (the low 16 bits of
a sum depend only on the low 16 bits of the addends). The table key K of a
message is the 144-bit word K = a_35 || a_34 || e_35 || e_34 || e_36[0..15]
(bit layout in Section 3). These words depend only on rounds 0..35; the low
16 bits of e_36 need only bits 0..15 of round 35's T1. Round 36, the T2 half
of round 35 and bits 16..31 of its T1 half are never computed. Equal digests
give equal keys; equal keys are checked by recomputing both full digests
(Section 5.3).

## 2. Machine model and charging

Classical probabilistic 256-bit word RAM with **64 registers** (our stated
assumption; Section 8 gives the bound with 48 and with 32): three-address
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
planes). Gates are 256-bit XOR, AND and OR, one operation each; a mixed-
polarity AND costs one NOT and one AND. Identities, applied once when the
program is written:

* XOR of two stored signals: one XOR, flags added mod 2. AND with flags
  (0,0): one AND; (1,1): one OR with flag 1; mixed: NOT then AND.
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
* Constant operand bit k: sum = x XOR c (flag flipped if k = 1), carry =
  x AND c (k = 0) or x OR c (k = 1): two operations, plus one NOT when the
  flags of x and c differ (287 such NOT-then-AND pairs per batch: 160 in the K adds, 28 in the
  schedule, 83 at carry-chain starts with a constant carry, the rest in the
  round sums; where the allocator would place the NOT in the register of a
  still-needed operand, the program uses the equal-cost form (a OR b) XOR b).
* Ch(e, f, g) = g XOR (e AND (f XOR g)), or f XOR (NOT e AND (f XOR g)),
  whichever has equal flags at the AND: 3 operations. Maj uses whichever of
  b XOR ((a XOR b) AND (b XOR c)), a XOR ((a XOR b) AND (a XOR c)),
  c XOR ((a XOR c) AND (b XOR c)) has equal flags at the AND, reusing the
  previous round's a XOR b as this round's b XOR c: 3 or 4 operations.
* Sigma0, Sigma1: two XORs per bit; sigma0, sigma1: two XORs per bit, one
  where SHR supplies a zero.

**Emission order (column lock step).** For each round t = 13..34 and bit
j = 0..31, in this order: bit j of the dependent schedule word W_t (its
three carry chains), the K add, Sigma1(e)[j], Ch[j], the three T1 chains,
e_{t+1}[j], Sigma0(a)[j], Maj[j], the T2 chain, a_{t+1}[j]; then round 35
bits 0..15 of W_35, the K add, Sigma1, Ch, the T1 chains and e_36. Every
carry chain stays open across the bit loop, so at any point the live set is
a few carries, the current bits and the planes the next bits read. Dead
code elimination removes everything the key does not need (bits 16..31 of
round 35's T1 chains and all of its T2).

**Hoisting.** A gate whose inputs are all group planes or lane planes is
computed once per group (22,477 gates, bit-sliced over the 256 lanes, which
includes rounds 0..12) and its plane written to memory; the batch loads it
like any input.

**Register allocation.** The straight-line program (circuit, then
transpose, then the table sinks) is allocated onto registers 0..57 by
furthest-next-use eviction with a clean-first tie-break: an operand not in
a register is loaded (1 operation); an evicted value that is used later and
is not already in memory is stored first (1 operation); dead operands are
freed before the result is placed; inputs are loaded at every use that
misses the registers. The emitted program uses at most 58 circuit
registers and never reads an unwritten word.

**Transpose.** The 144 key planes, in the order a_35 (planes 0..31), a_34
(32..63), e_35 (64..95), e_34 (96..127), e_36 bits 0..15 (128..143), are
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
table sink. 4,077 operations, 313 loads (the 8 masks m_k, loaded from memory at the
start of the transpose, and 305 row loads) and 160 stores per batch.

**Table sink** (9 per message): idx = Kw >> 111; e = LOAD T[idx]; x = Kw
XOR BIDL; y = x XOR e; z = y >> 128; compare z with 0 and branch to
CANDIDATE if equal; STORE T[idx] = x; BIDL = BIDL + 1. Batch setup and
control: the 16 batch planes (4 each), the batch id word BIDL (load the
stored group word, shift b, OR: 3) and the loop (3): 70.

**Ledger (one batch of 256 messages, exact; printed by the self-test):**

| part | operations |
|---|---:|
| circuit gates: XOR 20,403, AND 6,791, OR 5,777, and 287 AND-NOT pairs (574 operations) | 31,751 |
| circuit loads | 7,079 |
| circuit stores | 2,178 |
| transpose (+ 313 loads, 160 stores) | 4,550 |
| table sinks, 256 x 9 | 2,304 |
| batch setup and loop | 70 |
| **total** | **47,932** |

187.234375 per message. The counted program is in the experiment file
(Section 10, Appendix A); its self-test regenerates the program, runs it on a
random group and batch index through the counting VM, compares all 256 key
words and transposed addresses with the reference digests, and asserts the
total 47,932 (r38 twin: 50,276).

## 4. Groups, batches and ids

Group g (0 <= g < G = 256 NB) runs batches b = 0 .. 2^16 - 1; batch b holds
messages u = 256 b + L, L = 0..255, in lane L. The message id is
id = g * 2^24 + b * 2^8 + L (below 2^128 since G < 2^104).

### 4.1 Group setup (once per group)

Draw two uniform 256-bit words r0, r1 and store them at PT[g]; unpack
W[0..12]; write the 416 prefix planes (shift, AND 1, negate, store: 4
operations per plane) and evaluate the 22,477 hoisted gates bit-sliced
(rounds 0..12, the group schedule words with their K sums, and every later
gate whose inputs are all group or lane planes; 2 loads, 1 gate, 1 store
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

Lane L's word is (RTAG << 128) OR id with id = g * 2^24 + b * 2^8 + L <
2^128 (the increments never carry into the tag). The entry of a message is
x = Kw XOR BIDL: bits 0..110 hold id bits 0..110, bits 111..127 hold key
bits XOR id bits 111..127, bits 128..254 hold key bits XOR RTAG, bit 255
holds 1 XOR RTAG's top bit. Two messages in the same slot share key bits
111..254, so the occupant's id is recovered exactly: bits 0..110 of e, and
bits 111..127 of e XOR Kw.

### 5.3 Candidates

CANDIDATE: increment a counter v; if v > V halt with failure. Recover the
occupant's id as id' = (e XOR Kw) mod 2^128 (Section 5.2), its group
g' = id' >> 24 and u' = id' mod 2^24, rebuild both 55-byte messages from PT (at most 200
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
found distinct, and both full 37-round digests were recomputed by the
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
a's on bits 111..255, so z = 0, the ids decode to a and b, which differ
(not-F3), and the recomputed digests agree: output. Not-F4 and
not-F5 exclude a halt at the cap before that.

**Heuristic H1 (declared; equivalent text in claim.json).** For the events
F1, F2 and F4, the N digests of the grouped message set {m(g, u)}
(independent uniform prefixes P_g, all u in {0,1}^24, processed in the fixed
order of Section 4) behave like N independent uniform 256-bit values:
Pr[F1] <= exp(-N(N-1)/2^257), Pr[F2] <= N^3/6 * 2^-396, and the number Y
of pairs with equal 144-bit keys and different digests has E[Y] <= N^2/2^145
and Var[Y] <= N^2/2^145.

Under H1, with x = N(N-1)/2^257 >= 0.495316: Pr[F1] <= exp(-x) <= 0.609378;
Pr[F2] < 2^-14.5, we use 2^-13; E[Y] < 2^111, so Pr[F4] <= Var[Y]/(V -
E[Y])^2 < 2^111/2^222 = 2^-111 (Chebyshev); Pr[F5] <= 2^-61 by Markov
(expected garbage candidates N * 2^-128 < 1, over the tag alone, without
H1, on the premise that the uninitialised contents of T are independent
of RTAG, as in jaazinn's and jungjipdo's tables); Pr[F3] < 2^-209. NB is the smallest batch count for which 1 -
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
| Batches | N / 256 | 47,932 / 2644 | N * 187.234375 / 2644 |
| Group setup | G = 256 NB | <= 2^17 / 2644 | < 2^109.6 |
| Candidates | <= V + 2^61 + 1 | 3 | < 2^113.6 |
| Once per run | 1 | 2^12 / 2644 + 3 | < 2^2 |

    T <= N * 47932/(256 * 2644) + 256 NB * 2^17/2644 + (2^112 + 2^61 + 1) * (2 + 1000/2644) + 2^12/2644.

log2(N * 47932/(256 * 2644)) = 124.17341; the other terms add a relative
2^-10.4 (0.00078 bits). **log2 T <= 124.174210 < 124.17421**, the claimed
`time_log2` (the integer certificate of Appendix B evaluated at 10^-5 and
rounded up). Every batch, every load and store, every group setup, every
candidate up to the cap, the garbage candidates and the output are included;
there is no other precomputation, no stored collision, no parameter search
and no repetition.

Sensitivity (the same program re-allocated and re-executed):

| reading | per message | log2 T |
|---|---:|---:|
| **64 registers, every load and store charged (claimed)** | **187.23** | **124.17421** |
| 48 registers | 189.57 | 124.192 |
| 32 registers | 194.11 | 124.226 |
| loads and stores free (reference only, not claimed) | 149.23 | 123.846 |
| register-bank reading of abaa09ae (one placement per gate, operand reads free; that package's own circuit) | 320 | 124.947 |

jungjipdo's 383bad42 charges a 7-lane SWAR batch at about 217 operations per
message (124.329) under the same machine; the difference here is bit
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
  operands by register number, executes every instruction of the emitted
  circuit program, and counts the eight mask loads, the transpose swaps with
  their row loads and stores, and the 256 table sinks exactly as Section 3
  lists them; it compares all 256 key words and the transposed addresses (K XOR pol, pol the
  public polarity constant) with the program's scalar reference, aborts the
  experiment on any mismatch, and asserts the exact total 47,932. Its ledger
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

Local runs, all reported: our dev harness with our own seeds (256 trials per layout) gave 106, 98, 97 and 92 successes; the organizer's own Docker executor run locally with the public seed (`hashsmash-public-seed-v1`, two runs each, byte-identical output) gave 93, 105, 105 and 105, and 256/256 on the equivalence check, with the trial-0 witness asserting 47,932 in every experiment. A pre-registered larger run with our seeds (8,192 trials per layout, every pair re-verified with the reference digest, no bad pair; the program's fast evaluator, whose circuit is byte-identical across the witness revisions) gave 3196, 3188, 3170 and 3235 against the model's 3220 +- 44 (largest deviation -1.2 sigma, in the single-group layout).

The experiments test the circuit, the counted program and the scaled
birthday law on the real reduced-round target; they cannot certify the
full-width second moment, F2 or the 0.0005 allowance.

## 11. Heuristics (complete list)

H1 only (Section 7), score-critical, used only for the success probability.
Correctness of every output and all resource bounds are unconditional.

## 12. Limitations

* H1 is unproved; within a group the state entering round 13 is shared by
  2^24 messages.
* The 64-register machine is our stated assumption (Section 8: 48 registers
  124.191).
* The organizer seeds are public; scaled runs resolve the success frequency
  to about +-0.03 at 256 trials.
* Memory is far above the organizer baseline's and is reported, not scored.

## 13. Prior work

jaazinn 0a5b7ae8, 817d4440; jungjipdo f0065dce, 383bad42; may93182
11c46f4d; winglock 377eebd5, 982bf613; ercumentyildirim c7fa1a56; our
abaa09ae; the organizer-authored sha256-r37 merge-sort candidate at f46ab58
(132).

## Appendix A. The counted program

The per-batch program whose operations Section 8 charges is generated, register-allocated and executed
by the declared experiment program itself; nothing in the ledger is a cost-model-only figure.

1. **Generator** (`build(R, "counted")`). A symbolic SHA-256 over signals: a public constant bit, or a
   stored plane with a public polarity flag (NOT and XOR with a constant are flag flips). Inputs are the
   416 prefix planes (group constants), the 8 fixed lane planes (W13 bits 8..15) and the 16 batch planes
   (W13 bits 16..31). Gates are XOR, AND, OR and AND-NOT (the last charged as 2). Rounds are emitted in
   column lockstep: for each round t and bit j, the schedule word W_t (three open carry chains), the K add,
   Sigma1, Ch, the three T1 chains, e_t, Sigma0, Maj, the T2 chain and a_t, each by the polarity-aware
   full adder, Ch and Maj of Section 3. Round R-1 is not emitted; round R-2 emits only bits 0..15 of its
   e-half. The outputs are the 144 key planes: state words a, b, e, f entering round R-2 and e[0:16]
   entering round R-1.
2. **Dead-code elimination** (`live_gates`): only gates reachable from the 144 outputs survive; gates whose
   inputs are all group constants or lane planes are group work (computed once per group of 2^24 messages,
   stored, loaded by the batch like inputs); the rest is the per-batch circuit.
3. **Allocator** (`allocate`): linear pass over the per-batch gates with 58 physical registers; an operand
   not in a register is loaded (1 op); when no register is free the value with the furthest next use is
   evicted, clean values first, and an evicted value that is still needed and not yet in memory is stored
   (1 op); operands dead after the gate free their register before the result is placed; the 144 outputs
   are stored. Instructions carry register numbers; AND-NOT is two instructions (NOT then AND, or
   (a | b) ^ b when the destination is a's register). Every load and store is an instruction with a
   register or small-immediate address.
4. **Counting VM** (`counted_witness`): a physical register machine (registers addressed by number; a read
   of a stale register is an error) for the allocated circuit program, with the transpose, the mask loads
   and the table sinks executed on the row values and charged by count; it executes the batch setup (16 batch planes x 4 ops, batch id 3,
   loop 3), the group gates (not charged per batch), the allocated program, then the register-blocked
   zero-aware delta-swap transpose of the STORED plane words (rows 0..110 zero, 111..254 the key planes,
   255 all-ones; the eight swap masks loaded once per batch, 8 loads; zero-row cases from the layout: 6 ops
   per swap, 3 when the lower row is zero, 4 when the upper row is zero; loads and stores of non-zero rows), and the 256 table
   sinks of Section 5 exactly: with BIDL = (RTAG << 128) | (g*2^24 + b*2^8) formed in the batch setup
   (3 ops) and RTAG one uniform 128-bit word per run, each lane runs idx = Kw >> 111 (addresses in
   [2^144, 2^145)); e = LOAD T[idx]; x = Kw ^ BIDL; y = x ^ e; z = y >> 128; compare z with 0; branch to
   CANDIDATE; STORE T[idx] = x; BIDL = BIDL + 1 (9 ops; the lane id g*2^24 + b*2^8 + L stays below 2^128,
   so it never carries into RTAG). The batch is one seeded prefix, one seeded 104-bit group index and one
   seeded 16-bit batch index, 256 lanes; never-written slots return seeded garbage and a z = 0 on garbage
   is counted as a candidate.
5. **Self-test**: all 256 key words (polarity applied in the check) and all 256 transposed addresses
   (the reference key XOR the public polarity constant, shifted to bits 111..254, plus bit 255) are compared
   with the scalar reference (itself checked against `verifier/hash_functions.py` in our local harness); any
   mismatch, or a total different from the charged 47,932 (R = 37) / 47,932 (R = 38), aborts the experiment
   with a nonzero exit. The witness runs in trial 0 of every declared experiment; its ledger goes into that trial's
   observations (untrusted numbers).
6. **Run**: `python3 -I experiments/grouped_search_phys.py < request.json` (organizer executor), or the
   local harness `python -I dev_run_phys.py` (reference check, five experiments x two round counts x 256
   trials, every returned pair re-verified with the organizer verifier, two runs byte-identical).

## Appendix B. Certificate script

`cert.py` (stdlib `decimal` at 60 digits and exact integers; listed in full
below): (1) finds NB as the least batch count with success bound 1 -
exp(-N(N-1)/2^257) - 2^-13 - 2^-209 - 2^-100 - 2^-61 >= 0.3905 and prints it
(78856234692123534151746250567, N = 0.995306 * 2^128, bound 0.3905000...);
(2) forms T_num = N * 47932 + G * 2^17 * 256 + (2^112 + 2^61 + 1) * (2 * 2644
+ 1000) * 256 + 2^12 * 256, so that T = T_num / (256 * 2644), and checks
T_num^100000 < (256 * 2644)^100000 * 2^12417421, i.e. T < 2^124.17421, by
exact integer comparison (True), and prints log2 T = 124.174209.

```python
import sys
from decimal import Decimal, getcontext
getcontext().prec = 60
R = int(sys.argv[1]) if len(sys.argv) > 1 else 37
OPS, C, CLAIM5 = {38: (50276, 2728, 12419796), 37: (47932, 2644, 12417421)}[R]
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
Output (R = 37): NB 78856234692123534151746250567, N/2^128 0.9953056...,
bound 0.3905000..., log2 T = 124.174209..., `T < 2^124.17421 : True`.
