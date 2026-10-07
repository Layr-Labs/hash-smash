# sha3-256-r6: bitsliced grouped birthday search on linear-structure prefixes, time_log2 = 124.271

## 0. Summary and credit

A generic birthday search over full 256-bit digests. No cryptanalytic
weakness of SHA3 is claimed. This revises our 949c283b (bs4, 124.384). The
grouping, the 35 kept last-round planes, the tagged-id table and verify and
continue are unchanged. What changed:

- **Linear-structure prefixes (Th0rgal 4867f093; Guo-Liu-Song 2016).** Each
  group's 64-byte prefix carries 256 uniform bits and is constrained so that
  round 1 is linear in z. Each z-bit then flips a fixed 22-word set of the
  round-2 input by all-ones, in every group (Lemmas 2-3). Th0rgal used z in
  lanes 0 and 5; we use **lanes 1 and 6**, which needs 508 patched words
  instead of 554.
- **An AND-free incremental round 2** (Lemma 6). Only the flipped words
  that some later step reads are updated (13-18 per leaf). A2 is stored with
  a compile-time polarity that removes NOTs. Each of the 508 patched round-3
  input words gets a fixed XOR expression, merged into the round-3 loads.
  This costs 1,786..1,816 operations instead of T1's 3,969.
- **A rebuilt counted program.** The whole z-step and the batch setup were
  regenerated, compiled and run on a counted 64-register simulator. Every key
  was compared with the verifier's `sha3_256(m, 6)` (Section 10.1).

| quantity | value |
| --- | --- |
| messages N | 255 * 2^120 = 255 * 2^80 batches x 256 groups x 2^32 values of z |
| ops per z-step (256 messages), worst path | 31,410 (every executed primitive; leaves 31,380..31,410) |
| ops per message charged | 122.6953125 (31,410/256) + setup < 2^-20 |
| candidate verifications | at most VCAP = floor(N^2/2^141) + floor(N^2/2^148) + 2^91 + 2^61, each 2 units + at most 68 ops |
| total T | < 2^124.27096 (Section 8; exact integer certificate) |
| claimed time_log2 | **124.271** |
| success probability | > 0.39105 under H1 (model value 0.39106, rounded); claimed 0.39 |
| memory | < 2^145.01 bytes; claimed 146 |

**Credit.**

- **Co-authors.**
  - **Th0rgal** (4867f093): the linear-structure prefix, which makes round 1
    linear in z and round 2 incrementally AND-free. We use it in our
    lanes-1/6 variant and re-implemented it. Earlier (76ccfa1c): our table
    builds on T2, their sparse set at address 0, and our compiler subsumes
    T3. T1 is no longer used.
  - **jaazinn** (0a5b7ae8): grouped partial evaluation, the Briggs-Torczon
    sparse set, the failure analysis with H1 and the scaled-experiment
    design.
  - **may93182** (11c46f4d): the 256-way bit-plane Keccak and the
    delta-swap transpose.
- **Credited.**
  - Jian Guo, Meicheng Liu and Ling Song, "Linear Structures: Applications
    to Cryptanalysis of Round-Reduced Keccak", ASIACRYPT 2016: linear
    structures.
  - tekkac (b001199a): lane-complement chi on this track, after the Keccak
    team.
  - ercumentyildirim (c7fa1a56; r5: 4c969300): the last-round early abort,
    which the kept planes extend.
  - zeeshan8281 (cbf7998d): the 255/256 message budget.
  - zeeshan8281 and tekkac (f58275ef): exact per-message charging.
  - mitchuski (02d6a703): the every-load-and-store-charged reading.
  - 5kyguy (78676cf6) independently and concurrently specialised delta
    swaps for structurally zero rows and pruned the last round to a 140-bit
    bucket; nothing from it is used.
- **Not used.** Nothing from newjordan's b54bb98c is used. From GordoAR's
  e715ab73 and df2619d4 we use only the integer-certificate format of
  Section 8.
- **Ours.** The lanes-1/6 variant, read-only flips with storage polarity,
  patches merged into round 3, Lemmas 7 and 9-11, the kept planes with
  verify and continue, the tagged-id table, the counted program and any
  errors.

None of them has reviewed this package.

## 1. Target, machine and charging conventions

- **Target.** `sha3-256-r6-prefix-v1`: the complete SHA3-256 sponge (rate
  1088, capacity 512, suffix 0x06, pad10*1, zero IV) with Keccak rounds
  0..5 and all 256 output bits, as in `verifier/keccak.py:sha3_256(msg, 6)`.
  Messages are exactly 64 bytes. Lane k (k < 8) is bytes 8k..8k+7, read
  little-endian. Lane 8 = 0x06, lane 16 = 0x80 << 56, and the other lanes
  are 0. Lane index L = x + 5y. Rounds are numbered 1..6.
- **Digest and key.** The digest is lanes 0..3 after round 6, and K* =
  int.from_bytes(digest, "little"). The program stores the **key**
  K = key_of_digest(K*):
  - digest bit (x, b), with x < 4 and b in KEEP, moves to key bit
    ROWOF(x, b) = 4k + x, where b = KEEP[k];
  - the result is XORed with a public constant KEYMASK;
  - key bits 140..255 are 0.

  K is a fixed function of 140 digest bits, so **equal keys are only a
  candidate**.
- **Cost model.** `collision-frontier-v5`, C = 1626. One permutation costs 1
  unit. Any other 256-bit word primitive costs 1/1626.
- **Machine.** A 256-bit word RAM with **64 registers**. This is our stated
  assumption, and the program uses all 64. An operation on register
  operands is one primitive, not a memory access. 64 registers of 256 bits
  are 2 KiB, a 32-entry 512-bit SIMD register file. This reading does not
  cover a register bank of thousands of words; we claim no bound under such
  a reading, nor under a memory-to-memory reading.
- **Charging (claimed).** Every executed primitive of the v5 list costs 1:
  - every load and store, direct or register-addressed;
  - XOR, AND, OR, NOT, shift or rotation, add, compare, conditional branch,
    immediate move and random word.

  A constant address or an immediate is a field of the instruction that
  executes. A candidate verification evaluates two messages with the
  reference six-round function, 1 unit each. Section 9 prices address
  additions, immediates and shift amounts separately.

## 2. Messages, groups, batches and processing order

For group g the algorithm draws one fresh uniform 256-bit word and splits it
into four 64-bit lanes L1, L2, L5, L6. The **structured prefix** P_g is

    L0 = L7 = 0,  c1 = L1 XOR L6 XOR 2^63,
    L3 = 0x06 XOR rotr64(c1, 1),  L4 = NOT rotl64(c1, 1),

with lanes 1, 2, 5, 6 as drawn. The map (L1, L2, L5, L6) -> P_g is
injective, so P_g is uniform over a set S of 2^256 prefixes. P_g is stored.
For z in {0,1}^32:

    m(g, z) = P_g with LE32(z) XORed into bytes 8..11 and into bytes 48..51.

So z is XORed into the low 32 bits of lane 1 (x=1, y=0) and of lane 6
(x=1, y=1). XORing the same value into lanes 1 and 6 keeps c1, so for every
z the map P -> m(P, z) is a permutation of S.

- **Batches.** Write g = 256*beta + p, with batch beta < 255 * 2^80 and slot
  p < 256. Batch beta runs t = 0, 1, ..., 2^32 - 1 with z = gray(t) =
  t XOR (t >> 1).
- **Processing order.** At each t the batch evaluates the 256 messages
  m(256*beta + p, gray(t)). It offers them to the table in the order
  q = 0..255, slot p = decode_slot(q) = 32*(q mod 8) + floor(q/8).
- **Message number.** Message (beta, t, q) gets n = beta*2^40 + t*2^8 + q,
  which is also the count of messages processed before it. Every message
  is evaluated once.

**Bit mapping.** Word P(L, b) holds, in bit position p, bit b of lane L of
m(256*beta + p, z). Padding planes are constants: P(8,1) = P(8,2) =
P(16,63) = all-ones, and all other planes of lanes 8..24 are 0.

## 3. Dependency analysis (exact)

Every step map except chi is GF(2)-linear. A2 denotes the state after round
1 and the theta of round 2.

**Lemma 1 (round-1 theta is invariant).** Lanes 1 and 6 lie in column 1 and
carry the same difference z. Every column parity, and so every D word, is
therefore independent of z. The round-1 parities are C0 = L5,
C1 = L1 XOR L6 XOR 2^63 = c1, C2 = L2, C3 = L3 XOR 0x06 = rotr(c1, 1) and
C4 = L4. Hence D0 = C4 XOR rotl(C1, 1) = all-ones and
D2 = C1 XOR rotl(C3, 1) = 0.

**Lemma 2 (round 1 is linear in z; linear structure).** Rho/pi sends lane 1
(rotation 1) to row Y = 2, X = 0, and lane 6 (rotation 44) to row Y = 0,
X = 1. In chi, out[X] = b[X] XOR (NOT b[X+1] AND b[X+2]); a varying input
b[X] also enters out[X-1] through NOT b[X] AND b[X+1] and out[X-2] through
NOT b[X-1] AND b[X]. Both terms are constant when b[X+1] = 0 and
b[X-1] = all-ones on the varying plane.
- Row 2: b[1] comes from lane 7, which is 0 after theta (L7 = 0, D2 = 0).
  b[4] comes from lane 20, which is D0 = all-ones.
- Row 0: b[2] comes from lane 12, which is D2 = 0. b[0] comes from lane 0,
  which is L0 XOR D0 = all-ones.

So z changes exactly two round-1 outputs, bit j+1 of lane 10 and bit j+44 of
lane 1, each by z_j itself. Hence A2(z) = A2(0) XOR sum_j z_j E_j exactly,
where E_j is a fixed vector that does not depend on the group.

**Lemma 3 (22-word support, all-ones).** Round-2 theta spreads the two
flipped bits over 4 D columns. In bitsliced form z_j is the same in all 256
groups, so E_j is all-ones (W) on exactly these 22 words and 0 elsewhere
(planes mod 64):
- bit j+1 of lane 10 and bit j+44 of lane 1 (the chi outputs);
- D1 at plane j+1: lanes 1, 6, 11, 16, 21;
- D4 at plane j+2: lanes 4, 9, 14, 19, 24;
- D2 at plane j+44: lanes 2, 7, 12, 17, 22;
- D0 at plane j+45: lanes 0, 5, 10, 15, 20.

These sets are disjoint, so there are 22 words. A2(gray(t)) =
A2(gray(t-1)) XOR E_{ctz(t)}. The setup check, the counted simulator and
every organizer trial check this support against a from-scratch evaluation.

## 4. Bitsliced Keccak, encodings, transpose and compiler (exact)

**Lemma 4 (bitsliced round).** On planes the round is bitwise:
- theta: C[x][b] = XOR_y P(x+5y, b), D[x][b] = C[x-1][b] XOR C[x+1][b-1],
  and A'(L, b) = P(L, b) XOR D[x][b];
- rho/pi: B(X, Y, b) = A'(L, b - RHO[L]), with (x, y) = pisrc(X, Y);
- chi and iota: as in the scalar round.

Bit position p therefore runs the scalar round on message p. A lane
rotation in a round only changes which address is read. The only executed
rotations are 256-bit word rotations in the transpose (Lemma 9).

**Lemma 5 (delta swap).** For d in {1, ..., 128} let M_d have bit c set iff
c AND d = 0. A swap of rows a = R[i] and b = R[i+d] (i AND d = 0) exchanges
entries (i, c+d) and (i+d, c) for c AND d = 0. Stage d applies it to all 128
such row pairs and swaps bit log2(d) of the row index with the same bit of
the column index. The 8 stages act on different index bits, so they
commute. All 8, in any order, transpose the 256 x 256 matrix.

**Lemma 6 (AND-free incremental round 2).**
- **What is maintained.** O2P is the round-2 output (chi, iota) with
  round-3 theta applied, in the encoding Q3 of Lemma 8.
- **Chi difference.** For a row with old inputs a and input change c, the
  exact output difference is

      dout[k] = c_k ^ c_{k+2} ^ a_{k+1} c_{k+2} ^ c_{k+1} a_{k+2} ^ c_{k+1} c_{k+2}.

  By Lemma 3 every c is 0 or W, so every product is either 0, W or a single
  A2 word. Each dout is an XOR of at most two A2 words and possibly W, with
  no AND. The 22 flipped words lie in 21 round-2 chi rows.
- **Theta and the patch.** dC[x][b] = XOR_Y dout(x, Y, b), dD[x][b] =
  dC[x-1][b] XOR dC[x+1][b-1], and O2P(x+5Y, b) ^= dout(x, Y, b) XOR
  dD[x][b]. Symbolically, for each z-bit j, 508 O2P words get a fixed patch
  expression: an XOR of at most 5 terms, each an A2 word (44 distinct
  words per leaf) or W. 132 of them are W alone. A term that is itself flipped by
  this step is read after its flip, with W toggled.
- **Read-only flips.** Only the 1,152 A2 words that some leaf's expression
  reads are maintained. Leaf j flips the words of its support that lie in
  this set (13-18 words; load, NOT, store). Other A2 words are never read.
- **Storage polarity.** A2 word i is stored as A2[i] XOR pi_i W, for a fixed
  set pi of 439 words chosen by a deterministic local search to minimise
  the complemented expressions. Each stored term toggles W in its
  expression. The value is unchanged.
- **Merged into round 3.** Round 3 loads each patched O2P word once,
  XORs the expression, stores it back and uses the new value directly.
  When the expression is W alone, new = NOT old, so both polarities are in
  registers for the chi gate plans of Lemma 8. Distinct non-trivial
  expressions are formed once and reused (a small scratch cache).
- **Exactness.** Theta is linear and every encoding is an XOR with a
  constant, so the patched O2P equals the encoded, theta'd round-2 output of
  the new A2.
- **Cost.** 1,786..1,816 operations per leaf (worst leaf: 607 gates = 426
  XOR + 181 NOT, 659 loads, 550 stores).

**Lemma 7 (theta at the store, rotating start plane).** A round processes
planes b = s, s+1, ..., s+63 (mod 64) for a fixed start plane s.
- Plane b's 25 chi outputs are in registers, so its parities C'[x][b] are
  complete before any store.
- For b != s, D'[x][b] = C'[x-1][b] XOR C'[x+1][b-1] is available, because
  plane b-1 was processed just before. Each output word is stored with D'
  already added.
- Plane s is stored raw. After plane s+63, the 5 fix words fix[x] =
  D'[x][s] = C'[x-1][s] XOR C'[x+1][s-1] are known.
- The next round XORs fix[x] into each loaded word whose source plane is s.

The stored state plus the fix is exactly the theta'd state. The start planes
of rounds 3, 4, 5 are (2, 39, 34), as in bs4.

**Lemma 8 (lane-complement encoding; as in bs4).**
- Each stored lane L has a compile-time polarity pi_L: the stored word is
  the true word XOR pi_L * (all-ones).
- Per chi row the program uses the cheapest exact gate plan for the given
  input and output polarities: NOT b AND c equals s_b AND s_c, or NOT(s_b OR
  s_c), with at most one shared complemented copy and the iota bit folded
  in. The plan comes from an exhaustive search over the 32 complemented-copy
  sets. Where a complemented input is already in a register (Lemma 6), it
  costs nothing.
- The patterns are P34 (output of rounds 2, 3, 4) and P5 (output of round
  5). Rounds 3-5 read Q3 = fpol(P34), and the last round reads fpol(P5).
- Every chi row of rounds 3-5 costs at most 1 NOT. The last round takes,
  per plane, the digest polarities that need no NOT; moved to key rows,
  these fixed bits form KEYMASK (33 of the 140 bits set).

**Lemma 9 (kept planes, key rows and the rotating-frame transpose; as in
bs4).**

    KEEP = (0, 1, 2, 3, 4, 9, 10, 11, 16, 17, 18, 22, 23, 24, 25, 29, 30, 31,
            32, 37, 38, 39, 40, 44, 45, 46, 47, 51, 52, 53, 54, 58, 59, 60, 61)

- **Key rows.** Plane KEEP[k] gets slot k, and digest bit (x, b) becomes key
  row 4k + x. Rows 0..139 hold the kept bits and rows 140..255 are
  constant zero.
- **Blocks.** Block g holds rows 32g..32g+31. Blocks 0-3 are full, block 4
  holds slots 32-34, and blocks 5-7 are empty.
- **Frames.** Row r is held in a **frame** OFF[r]: physical bit q holds
  logical bit (q + OFF[r]) mod 256. A stage-d swap of rows a = R[i] and
  b = R[i+d] keeps the row of even index parity (popcount) in frame 0 and
  moves the other.
  - If b stays in frame 0, then u = rot(a, OFF[a] - d) puts logical bit c+d
    of a at physical position c. Then t = (u XOR b) AND M_d; b ^= t;
    a = u XOR t; OFF[a] = d. These are 5 operations, and they exchange
    exactly the entries of Lemma 5.
  - The case where a stays in frame 0 is symmetric, with NOT M_d and
    OFF[b] = -d.
- **Zero rows.** A statically zero row needs no rotation and is substituted
  into the formulas: zero mover 2 operations, zero stayer 3, both zero
  nothing. The zero pattern is known at compile time.
- **Phase 1.** As soon as a block's kept planes exist, the last round
  computes that block's rows in registers and applies stages 1, 2, 4, 8, 16
  in the cheapest static order: 1,770 operations in all.
- **Phase 2.** For each gi = 0..31 the program takes rows 32i + gi, loads
  rows i <= 4 only, and applies stages 32, 64, 128: 1,520 in all.
- **Frame fix.** One rotation per row left outside frame 0, 128 in all.

The transpose costs 3,418 ALU operations (1,770 + 1,520 + 128). Its memory
traffic is counted in Section 5.2: 109 stores and 109 loads of ROWS between
the phases, and 25 loads of the delta-swap masks (17 in phase 1, 8 in phase
2). Last round + phase 1 = 280 chi/iota + 115 state loads + 17 mask loads +
109 ROWS stores + 1,770 = 2,291; phase 2 = 1,520 + 128 + 109 ROWS loads + 8
mask loads, and with the 1,536-op table 3,301. By Lemma 5, row 32i + gi is
then the key of slot 32i + gi = decode_slot(8gi + i).

**Lemma 10 (dependency cone with start planes; as in bs4).** The last round
on plane b reads the 5 diagonal lanes at source plane (b - RHO[L]) mod 64.
Round 5 must therefore store only these 175 words. None lies on round 5's
start plane 34, so no round-5 fix word is needed. For a round with start
plane s whose input lacks D on plane s_in, needed outputs propagate
backwards:
- a needed stored word (L, b) with b != s needs its chi output, C[x-1][b]
  and C[x+1][b-1];
- a needed fix column x needs C[x-1][s] and C[x+1][s-1];
- a parity needs its 5 chi outputs;
- a chi output needs its 3 row inputs, plus the fix wherever the source
  plane is s_in.

Round 5 computes 1,161 chi outputs and 229 parities and reads 1,363 words
with all 5 fix columns. Round 4 needs all 320 parities and reads all 1,600
words. Every computed word is given by the same formula from the same
inputs as in the full round, and no omitted word is ever read.

**Lemma 11 (straight-line compiler).** The code of one ctz leaf is a single
straight line, compiled in four steps:
1. It is put in SSA form.
2. Loads are store-to-load forwarded. A direct load whose word was written
   or loaded earlier in the block takes the value from the register that
   still holds it, chosen by an exact max-weight selection under the
   62-register budget. All addresses are instruction constants, so aliasing
   is decided exactly. A store to a scratch word of the step is dropped when
   no later load reads it. Scratch words are never read outside the step.
3. Registers are allocated by interval colouring. This is exact for
   straight-line code: the register count is the maximum number of
   simultaneously live values.
4. The result runs on the counted simulator.

No step changes a computed value. Every leaf uses at most 62 registers,
plus the persistent s and c, so 64 in all.

## 5. The algorithm and its counted program

### 5.1 Run and batch setup

**Once per run.**
- c = RAND AND (2^256 - 2^128), i.e. c = TAG*2^128 with TAG its uniform
  high 128 bits.
- CNT = 0.

**Once per batch** (a counted straight-line program of 52,558 operations,
62 registers; 72,154 with the address and immediate charges of Section 9):
- draw 256 random words and build the 256 structured prefixes (Section 2);
  store them at PREF + 512*beta + 2p + w and transpose them;
- store the padding planes;
- compute round 1 and A2 (stored with polarity pi), and O2P;
- store the delta-swap masks and set s = 0.

The setup program's A2, O2P, masks and prefix words were compared with an
independent reference. With batch-loop control this is < 2^-20 per message.

### 5.2 Per z-step program (fully unrolled; worst path)

There are two persistent registers: s (the step counter t) and
c = TAG*2^128 + n.

    (a) control, t >= 1 (16): s = s + 1 ; 5-level branch tree on ctz(s):
        v = s AND mask ; (v == 0) ; branch   (5 levels; no indirect jump)
    (b) leaf j: incremental round 2, block j (Lemma 6), followed in line by
        its own copy of the step body (32 copies; no jump):
        R3 (start 2, with the O2P patches merged), R4 (cone, start 39),
        R5 (cone, start 34) with the last-round blocks and phase 1
        interleaved as soon as their round-5 planes exist, phase 2, the
        frame fix and 256 table steps (5.3)
    (c) loop test (2): (s < 2^32 - 1) ; branch

At t = 0 the body runs without (a) and round 2 (30,085 operations). The 32
leaves cost 31,380..31,410. The simulator's measured counts equal the
static ones on every step run.

**Ledger (one worst-path z-step, leaf j = 28; simulator count).**

| block | bs4 | ops | gates | loads | stores | ROT/ADD/CMP/branch |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| control | 16 | 16 | 5 | 0 | 0 | 11 |
| incremental round 2 | 3,969 | 1,816 | 607 | 659 | 550 | 0 |
| round 3 | 9,791 | 9,331 | 6,666 | 1,097 | 1,568 | 0 |
| round 4 (cone) | 9,351 | 9,367 | 6,484 | 1,565 | 1,318 | 0 |
| round 5 (cone) | 5,266 | 5,286 | 3,855 | 1,316 | 115 | 0 |
| last round, 35 planes + phase 1 | 2,280 | 2,291 | 1,696 | 132 | 109 | 354 |
| phase 2 + frame fix + 256 table steps | 3,301 | 3,301 | 1,472 | 373 | 256 | 1,200 |
| loop test | 2 | 2 | 0 | 0 | 0 | 2 |
| **total per 256 messages** | **33,976** | **31,410** | **20,785** | **5,142** | **3,916** | **1,567** |

Gates are XOR/AND/OR/NOT after store-to-load forwarding; each row is
gates + loads + stores + the last column. Rounds 4 and 5 differ slightly
from bs4 because the compiler's register choices change with the new round
2.

By opcode:

| loads | stores | XOR | AND | OR | NOT | ROT | ADD | CMP | branch |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 4,886 direct + 256 register | 3,660 direct + 256 register | 14,528 | 3,169 | 2,053 | 1,035 | 786 | 257 | 262 | 262 |

There are no shifts and no MOVI on the step path.

### 5.3 Tagged-id table (as in bs4)

S has 2^140 words at address 0 and is never initialised. All other arrays
lie at addresses >= 2^170. The key K < 2^140 is the address. Per message
(hot path, 6 operations):

    w = LOAD [K] ; x = w XOR c ; f = (x < 2^128) ; if f goto CAND
    STORE [K] = c ; c = c + 1

- **Hot path.** x < 2^128 iff the high half of S[K] equals TAG. A written
  slot always holds TAG*2^128 + (number of the last message with key K),
  so every lookup of a written slot is a **genuine candidate**: an earlier
  message with an equal 140-bit key.
- **Garbage candidates.** A never-written slot is a candidate only if its
  initial high half equals TAG. TAG is uniform and drawn after the initial
  memory is fixed, so each lookup is a garbage candidate with probability
  at most 2^-128, whatever the initial memory.
- **Overwrite rule.** After the step, S[K] = TAG*2^128 + n, as in a
  Briggs-Torczon set whose stored index is the message number. Only the
  last message with each key is remembered.

### 5.4 Candidates: verify and continue, halting, cap

- **Rebuild.** On CAND the program saves 7 registers and takes i = w AND
  (2^128 - 1) and n = c AND (2^128 - 1). It decodes each id to beta =
  id >> 40, t = (id >> 8) mod 2^32, q = id mod 256, p = decode_slot(q) and
  z = gray(t). It loads the two prefix words at PREF + 2(256*beta + p) and
  XORs LE32(z) into bits 64..95 of the first and bits 128..159 of the
  second (lanes 1 and 6). This is 20 operations per message; a garbage id
  rebuilds some 64-byte string.
- **Verify.** It evaluates both messages with the reference function (2
  units) and compares the 256-bit digests and then the messages.
- **Halt.** If the digests are equal and the messages differ, it outputs
  the pair and halts.
- **Continue.** Otherwise it loads CNT, adds 1 and stores it. It aborts the
  run with failure if CNT >= VCAP. It then restores the registers and
  jumps back to the insert (1 counted branch; the candidate block is out of
  line).
- **Costs** (simulator, every outcome measured):
  - continue: 64 operations above the 6-op hot path when the digests
    differ, and 68 when the digests are equal but the messages are the same
    (both include the jump back); we charge 68;
  - halt: 55 operations after the branch, 59 for the whole table step; we
    charge 68;
  - abort (CNT reaches VCAP): a prefix of the continue path, so within the
    68-op charge.

  Continue and halt each add 2 units.

The cap is an instruction immediate:

    VCAP = floor(N^2 / 2^141) + floor(N^2 / 2^148) + 2^91 + 2^61.

The term floor(N^2/2^148) = E/128 is a margin for H1 (Section 7).

## 6. Correctness (unconditional)

- **Evaluator exactness.** Lemmas 1-3 and 6 keep every read A2 word and all
  of O2P exact at every t. Lemmas 4, 7, 8, 10 and 11 make every needed word
  of rounds 3-5 exact in its encoding. Lemma 9 makes the key of slot p
  equal key_of_digest(K*) of message p. Section 10 checks this bit for bit.
- **Outputs.** The run outputs only two distinct 64-byte strings whose
  256-bit digests were equal under two reference evaluations, which is a
  full collision. A key match or a garbage word never produces output by
  itself.

## 7. Success probability

The run halts at the first verified collision. The failure events are:

- **F3:** two groups produce the same message. m(g, z) = m(g', z') needs
  L2, L5 equal and L1 XOR L1' = L6 XOR L6' in a set of 2^32 values, an
  event of probability 2^32/2^256 per pair of groups. There are fewer than
  2^191 pairs, so Pr[F3] < 2^-33 (no heuristic).
- **F1:** no two of the N messages have equal digests.
- **F2:** for some colliding pair (a, b), a processed before b, some message
  c between them has a's key and a different digest.
- **F4:** the number of continued candidates reaches VCAP.

**If none of F1-F4 occurs, the run succeeds.** Take a colliding pair
(a, b).
1. When a is processed, it either halts with a collision or sets
   S[K] = TAG*2^128 + n_a.
2. Each later message c before b with that key: by not-F2, c has a's
   digest. The slot holds a's number or that of an earlier message with
   a's key, hence (not-F2) with a's digest. So c's candidate finds equal
   digests of distinct messages (not-F3), and the run succeeds.
3. Otherwise, at b's lookup the slot holds such a number, and the
   candidate finds the collision.
4. Without F4 the run is not aborted before then.

So Pr[fail] <= Pr[F1] + Pr[F2] + Pr[F3] + Pr[F4].

**Heuristic H1 (declared; identical text in claim.json).** For the failure
events F1, F2 and the genuine-candidate part of F4 (proof Section 7), the N
= 255*2^120 digests of the grouped message set {m(g, z)} (independent
prefixes P_g, each uniform over the 2^256 structured prefixes of Section 2,
all z in {0,1}^32, processed in any fixed order chosen independently of the
digests, in particular the order of Section 2: batch by batch, t = 0..2^32-1
with z = gray(t), slots p = decode_slot(q) = 32*(q mod 8) + floor(q/8) for q
= 0..255) behave like N independent uniform 256-bit values, i.e. Pr[F1] <=
exp(-N(N-1)/2^257), Pr[F2] <= N^3/6 * 2^-396 and, since the 140-bit key is a
fixed function of 140 digest bits, the number Y1 of message pairs with equal
keys has E[Y1] <= N^2/2^141 and Var[Y1] <= E[Y1].

With N = 255 * 2^120:

- **F1.** Under H1, Pr[F1] <= exp(-N(N-1)/2^257) < 0.6089000.
- **F2.** Under H1, Pr[F2] <= N^3/6 * 2^-396 < 2^-14.
- **F3.** Pr[F3] < 2^-33.
- **F4.** Continued candidates are Y1 + Y2.
  - Genuine ones are distinct pairs (stored number, n) with equal keys, so
    they number at most Y1. With E = floor(N^2/2^141) < 2^115 and
    E' = floor(N^2/2^148) > 2^107.98, Chebyshev gives
    Pr[Y1 >= E + E' + 2^91] <= E/E'^2 < 2^-100.
  - **Sensitivity.** F4 is the most sensitive use of H1: by
    Cauchy-Schwarz any non-uniformity of the 140-bit key can only raise
    E[Y1]. The cap tolerates a relative excess of 2^-7 (0.78%) over
    N^2/2^141, plus 2^91 pairs. The scaled experiments resolve the
    masked-pair mean only to about 1% (pooled ratio to the uniform model
    1.008 +- 0.006 over the 49,152 trials of Section 10.3), so this margin
    is not certified by them. Within-group pairs would need an average
    key-collision probability above about 2^-51, or above about 2^-19 for
    the pairs of one z-difference, to matter.
  - Garbage ones, Y2, satisfy E[Y2] <= N * 2^-128 < 1 for any initial
    memory (Section 5.3; no heuristic), so Markov gives Pr[Y2 >= 2^61] <=
    2^-61.

  Hence Pr[F4] <= 2^-100 + 2^-61.
- **Total.** Success >= 1 - Pr[F1] - Pr[F2] - Pr[F3] - Pr[F4] > 0.39105.
  We claim 0.39, which leaves an allowance of 0.00106.

The scaled analogue of Y1 is the per-trial `masked_pairs` count. Its
variance/mean ratio is about 1 (Section 10.3).

**Rigorous partial support (jaazinn's argument, adapted).** For every z,
P -> m(P, z) permutes S (Section 2), so each m(g, z) is uniform over S. For
groups g != g' the messages m(g, z) and m(g', z') are independent and
identically distributed, so by Cauchy-Schwarz they collide with probability
>= 2^-256. Within-group pairs are a 2^-96 fraction, so the expected number
of colliding pairs is at least (1 - 2^-96) * N(N-1)/2^257. H1 is needed for
the second-moment behaviour behind Pr[F1], for F2 and for Y1.

**What does not change the message set.** Bitslicing, batching, the
incremental round 2, the cone, the start planes, the compiler, the 140-bit
key and the encodings fix only how and in which order digests are computed.
That order is a function of (beta, t, q), never of digests. The structured
prefixes do change the message set relative to bs4. H1 is stated for this
set, and the experiments of Section 10 use it.

## 8. Time bound

Per message the main loop charges 31,410/256 = 122.6953125 operations plus
amortised setup (< 2^-20). This covers the Gray and round-2 updates, rounds
3-6, the transpose, every table load, store, compare and branch, and all
loop control. On top come at most VCAP continued candidates (2 units + 68
operations each), one halting candidate (2 units + 68 operations) and the
per-run initialisation (< 10 operations, bounded by 1 unit). So, in every
run (no restarts),

    T <= N (31,410/256 + 2^-20)/1626 + VCAP (2 + 68/1626) + (2 + 68/1626) + 1
      = 2^124.26618 + 2^116.030 + 3 < 2^124.27096.

**Integer certificate.** With K = 2^28 * 1626,

    A = T K = N (31,410 * 2^20 + 256) + VCAP (2*1626 + 68) 2^28 + (2*1626 + 68) 2^28 + K

is an integer, and A^1000 < 2^124271 * K^1000 holds exactly. The claimed
time_log2 is therefore **124.271**, rounded up (and 124.270 is not reached).

- **Slack.** The claim would still hold with up to 31,411 ops per z-step,
  or with up to 99 operations per candidate.
- **Expected verification work.** Under H1 it is about 2^116 units, about
  103 operations per z-step on average (2 units + 68 operations per
  candidate).
- **Preprocessing.** preprocessing_log2 = 0: setup is per batch and inside T.

## 9. Sensitivity of the bound to conventions

Same program, worst z-step, the candidate term included. N = 255 * 2^120
unless stated.

| reading | ops/z-step | ops/message | time_log2 |
| --- | ---: | ---: | ---: |
| every executed primitive once, 64 registers (claimed) | 31,410 | 122.70 | 124.27096 -> 124.271 |
| + one address addition per direct load/store, + one MOVI per ALU immediate | 40,480 | 158.13 | 124.636 |
| as above, + one op per shift or rotation amount | 41,266 | 161.20 | 124.664 |
| exact Gray-sequence average instead of the worst leaf | 31,397.4 | 122.65 | 124.271 |
| N = 2^128 | 31,410 | 122.70 | 124.277 |
| logic gates only (reference; needs far more than 64 registers) | 20,785 | 81.19 | 123.678 |
| direct loads/stores to a fixed bank free (**not claimed**) | 22,864 | 89.31 | 123.815 |
| bs4 program (949c283b) at this budget | 33,976 | 132.72 | 124.384 |

We do not adopt the fixed-bank reading. Under our 64-register reading,
every one of the 8,546 direct loads and stores per z-step is charged.

## 10. Evidence

### 10.1 Counted simulator (participant evidence)

- **The simulator.** The program runs on a counted 256-bit word-RAM
  simulator with an explicit 64-register file (high-water check) and a
  counter per primitive. Its `hash` instruction (1 unit) is
  `verifier/keccak.py:sha3_256(m, 6)`.
- **Hostile memory.** Before every z-step, all scratch words of the step
  and all 62 non-persistent registers are overwritten with random junk. A
  read outside the cone, or of a word not yet written in the step, would
  corrupt a key. Never-written table words are set, by batch, to all-ones,
  random, zero, or adversarial (high half = TAG, low half random or out of
  range).
- **Keys.** Every key was compared with key_of_digest(int.from_bytes(
  sha3_256(m, 6), "little")) from `verifier/keccak.py`:
  - for each of the seeds 2026, 4711, 31337, 7 and 99: 16 batches x 4
    z-steps from random start steps (16,384 keys), every Gray block
    j = 0..31 once (8,192 keys) and 40 consecutive steps from t = 0
    (10,240 keys), so 34,816 keys per seed;
  - runs of 300 and 200 consecutive steps (76,800 and 51,200 keys).

  There were 0 mismatches. The register high-water mark was 64. Leaf 28
  measured 31,410 on every run, and no step exceeded it.
- **Persistent state.** After each leaf j = 0..31 (two seeds, and two
  steps each) and every 7 steps of the long runs, the stored A2 on all
  1,152 read words and all 1,600 words of O2P were equal to a rebuild from
  the prefixes at the current z (202 checks). This is also a proof-grade
  check: a static scan of every compiled leaf shows that each store to A2
  or O2P depends only on loads of A2 and O2P through XOR and NOT (also via
  scratch words of the same step), so a leaf's update of (read A2 words,
  O2P) is a compile-time affine map, applied per bit position, with no
  rotations. Checking it against the true update on uniformly random
  states (all 1,600 A2 and O2P words; two runs for every leaf j = 0..31, 0
  mismatches) misses a wrong map with probability at most 2^-256 per word.
- **Table words.** Every table word decodes from its id (TAG, beta, slot,
  z) to a message whose key is its address. 12,288 adversarial garbage
  candidates per seed were verified and continued.
- **Candidate paths.** Replaying a z-step gives 256 genuine candidates,
  with and without resetting c. The rebuilt messages equal the true ones.
  Continue costs 64 / 68 operations, halting 55 after the branch; equal
  digests were forced with a constant test hash, for control flow only.
- **Setup.** The counted setup program was compared word for word with an
  independent reference (prefix rows, A2 in polarity pi, O2P, masks) on two
  seeds.
- **Mutations.** Dropping an O2P patch store, a round-4 or round-5 state
  store, or swapping a delta-swap mask is caught by the key comparison.
  Dropping any one A2 flip store (67 cases in leaves 0, 1, 7, 28) is caught
  by the persistent-state check; dropped flips and patches and an XOR
  turned into AND are also caught by the random-state check. A static
  check confirms that every one of the 33 x 256 table steps is the exact
  6-op hot path, and each simulated step asserts that the number of
  candidate paths taken equals the number of lookups whose high half is
  TAG; turning the table XOR into OR is caught by both.
- **Experiment evaluator.** The evaluator of 10.2 equals key_of_digest(
  `sha3_256(m, 6)`) on 76,160 keys (a 1,100-step Gray walk over z bits
  0..10 and a 300-step walk over z bits 22..30), with 0 mismatches. Its
  prefixes, flips, polarity, patch expressions, KEEP, ROWOF, KEYMASK, start
  planes and stage orders equal the program's.
- **Not shipped.** The generator, compiler and simulator (about 88 KB)
  exceed the 64 KiB experiment-source budget and are not shipped. The 33
  compiled bodies are rebuilt byte-identically from the generator (pickle
  SHA-256 f6c5f58107703846a726889deff06b554ab26728f7f203269bb77509869fefb0);
  every leaf count equals its static count. The ledger and opcode table
  above sum exactly, and the shipped script asserts the transpose count,
  the 22-word supports and the patch geometry (1,152 read words, 508
  patched words, 13-18 flips).

### 10.2 Declared experiments (organizer-executed, `python-message-pairs-v1`)

All four experiments run `experiments/s3r6_bitslice_birthday.py`. It mirrors
the counted program:
- structured prefixes (Section 2) derived from the organizer seed with
  SHA-256, z in lanes 1 and 6;
- per-batch A2 (polarity pi) and O2P, and Gray updates that flip the read
  support words and XOR the fixed patch expressions into the 508 O2P words;
- lane-complement rounds 3-5 with theta at the store and the start planes
  (2, 39, 34) stored raw and fixed on read;
- rounds 4 and 5 computed in full, after which every word and fix column
  outside the Lemma 10 cone (1,363 and 175 words) is replaced by an
  unrelated constant;
- the last round on the 35 kept planes at key rows 4k + x in the KEYMASK
  encoding;
- the rotating-frame zero-row transpose (asserted at 3,418 operations) and
  the processing order decode_slot(q).

Every digest bit used for matching comes from this evaluator. The script
maps the digest mask to key rows and refuses a mask bit outside the kept
planes.

**Self-checks** (any failure aborts the run):
- the whole 140-bit key of each trial's first 4 messages, and of its first
  message at each step t = 2^i, against an independent direct sponge;
- for every z-bit used, A2(e_j) XOR A2(0), computed from scratch, is
  all-ones exactly on the 22 support words;
- the maintained A2 (read words) and O2P against a rebuild from the
  prefixes after the batch;
- at every step, the zero key rows, and the transpose against the full
  6-op transpose;
- every key of the batch through the tagged-id table, with adversarial
  never-written words (1/16 carry the run's TAG, so the
  verify-and-continue path must be taken). Every table word must decode to
  a message whose key is its address.

Dropping one flip, dropping one patched word or corrupting one patch
constant makes the script fail.

**Scale.** N_t = 2^9 and an 18-bit mask give N_t^2/2^18 = 1 = N^2/2^256 up
to (255/256)^2. The uniform-model success probability is 0.39307 (100.6 +-
7.8 per 256 trials). Layouts:
- `k6r6-bs-full-width`: 256 groups x 2;
- `k6r6-bs-spread`: 16 x 32;
- `k6r6-bs-single-group`: 1 x 512;
- `k6r6-bs-high-z`: 4 x 128 with z = gray(t) << 25.

The experiment ids and masks are bs4's. The prefix label is new
(`s3r6-ls-v1`), since the message set changed.

### 10.3 Participant-reported local runs (not organizer evidence; untrusted)

Participant-reported local replays on the solver's machine, 256 trials,
each experiment twice with byte-identical output (about 2.3 s and at most
46 MB per run), successes for full-width / spread / single-group / high-z:
- bs3-rv-1: 96 / 97 / 95 / 96;
- committee-c1: 101 / 108 / 112 / 109.

Participant-reported local statistics with the `--local` mode, 12,288
trials per layout (48 chunks of 256):

| layout | successes | z | cells (min, max) | masked-pair variance/mean |
| --- | ---: | ---: | --- | ---: |
| full-width | 4,835 | +0.09 | -1.49, +2.10 | 0.991 |
| spread | 4,852 | +0.41 | -1.49, +1.97 | 1.008 |
| single-group | 4,959 | +2.38 | -0.98, +2.10 | 0.987 |
| high-z | 4,853 | +0.42 | -2.51, +2.61 | 0.985 |

Because single-group was the largest deviation, we ran 24,576 further
single-group trials with fresh seeds: z = -1.10, variance/mean 1.006. Pooled
over 36,864 single-group trials, z = +0.48. The other three layouts were not
rerun. No self-check failed in any run.

## 11. Memory

| array | 32-byte words | bytes |
| --- | --- | --- |
| S (tagged ids, at 0) | 2^140 | 2^145 |
| PREF (at 2^180) | < 2^97 | < 2^102 |
| A2, O2P, patch cache, masks, state buffers, ROWS, CNT, save area (at 2^170) | < 2^14 | < 2^19 |
| code (32 fused leaves, setup) | < 2^21 instructions | < 2^26 |

Total < 2^145.01 bytes; we claim 146. Memory is reported only.

## 12. Limitations

- **H1 is a heuristic.** It extends the grouped structure from the tested
  scale (N_t = 2^9, 18-bit masks) to N = 255 * 2^120 and the 256-bit
  digest. F2 and Y1 cannot be scaled down faithfully and are bounded only
  under H1. Organizer seeds are public. A 256-trial experiment resolves the
  success frequency only to about +-0.03, and the 0.00106 allowance is not
  statistically certified.
- **Stronger within-group structure.** Round 1 is now linear in z, with
  fixed group-independent differences (Lemmas 2-3). Five nonlinear chi
  layers follow. Within a group the digest has degree at most 32 in z; with
  32 z bits, this gives no zero-sum on any affine subspace of z. Within-
  group pairs are a 2^-96 fraction of all pairs.
- **Source of the gain.** The gain comes from operation-level pricing. All
  executed work, including all memory traffic and every candidate
  verification, is charged.
- **Register assumption.** The 64-register machine is an assumption, and
  the program uses all 64. Section 9 gives stricter readings, all at most
  124.664.
- **Candidate cap.** F4 is the most sensitive use of H1 (Section 7): the
  cap tolerates a relative excess of 2^-7 of E[Y1] over N^2/2^141, which
  the experiments do not certify.
- **Rounding slack.** It is small: 1 operation per z-step (Section 8).
- **Scope.** No sub-birthday attack, collision certificate or full-scale
  run is claimed.

## 13. Credit

- **Co-authors**, in the sense of Section 0:
  - **Th0rgal** (4867f093: the linear-structure prefix, used in our
    lanes-1/6 variant; 76ccfa1c: the table builds on T2, T3 subsumed by
    Lemma 11);
  - **jaazinn** (0a5b7ae8);
  - **may93182** (11c46f4d).
- **Credited:**
  - Guo, Liu and Song (ASIACRYPT 2016), linear structures;
  - tekkac (b001199a, f58275ef);
  - ercumentyildirim (c7fa1a56, 4c969300);
  - zeeshan8281 (cbf7998d, including the 255/256 budget);
  - mitchuski (02d6a703);
  - 5kyguy (78676cf6: concurrent zero-row delta swaps and a 140-bit
    last-round bucket; nothing used).
  - GordoAR (e715ab73, df2619d4: the integer-certificate format of
    Section 8; nothing else used).

Errors are ours.
