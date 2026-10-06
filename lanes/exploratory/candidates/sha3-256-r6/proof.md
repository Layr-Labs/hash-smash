# sha3-256-r6: bitsliced grouped birthday search, tagged-id table, time_log2 = 124.295

## 0. Summary and credit

A generic birthday search over full 256-bit digests. No cryptanalytic
weakness of SHA3 is claimed. This revises 5596b5be (124.384) and 5a5720c7
(bs3, 124.491). The grouping, the 35 kept last-round planes and verify and
continue are unchanged. The group prefix structure and counted program are
refined:

- **22-word all-ones support and AND-free incremental round 2 (Lemmas 3 & 6,
  extending Th0rgal's T1 of 76ccfa1c).** Choosing each group's 64-byte prefix
  from 256 uniform random bits in lanes 0, 1, 2, 5 with lanes 3, 4, 6, 7
  satisfying $L_3 = \texttt{0x06} \oplus \texttt{M64} \oplus \operatorname{rotl}_{64}(L_0 \oplus L_5, 1)$,
  $L_4 = 0$, $L_6 = 0$, and $L_7 = L_2 \oplus \operatorname{rotr}_{64}(L_0 \oplus L_5, 1)$
  makes the round-1 $\chi$ differences $u_3 = u_4 = v_0 = v_4 = 0$ identically,
  collapsing each Gray column's support in $A_2$ from 62 words to **22 words
  all equal to $W$** (all-ones), the affected round-2 $\chi$ rows from 60 to
  **21**, and the patched `O2P` words from 1,081 to **554** with 0 basis loads
  and 0 AND gates: **1,896 operations** instead of 3,969 (saving 2,073 ops per
  $z$-step).
- **A straight-line compiler.** It keeps values in registers between rounds
  (store-to-load forwarding, Lemma 11). This subsumes Th0rgal's T3.
- **Rotating start planes** for rounds 3-5 (Lemma 7).
- **Low-aligned key and rotating-frame transpose.** The 140 kept digest bits
  are key bits 0..139, so the key is below 2^140 and is the table address.
  The transpose uses rotating-frame delta swaps with statically zero rows:
  3,418 operations instead of 3,948 (Lemma 9).
- **A tagged-id table at address 0.** Each slot is one word, TAG*2^128 + n.
  Each message costs 6 operations, and there is no key array (Section 5.3).
  It builds on Th0rgal's base-0 sparse set (T2) and jaazinn's sparse set.
- **The budget N = 255 * 2^120 messages** (zeeshan8281, cbf7998d).

| quantity | value |
| --- | --- |
| messages N | 255 * 2^120 = 255 * 2^80 batches x 256 groups x 2^32 values of z |
| ops per z-step (256 messages), worst path | 31,903 (every executed primitive) |
| ops per message charged | 124.62109375 (31,903/256) + setup < 2^-20 |
| candidate verifications | at most VCAP = floor(N^2/2^141) + 2^91 + 2^61, each 2 units + at most 68 ops |
| total T | < 2^124.29332 (Section 8; exact integer certificate) |
| claimed time_log2 | **124.295** |
| success probability | >= 0.39106 under H1; claimed 0.39 |
| memory | < 2^145.01 bytes; claimed 146 |

**Credit.**

- **Co-authors.**
  - **jaazinn** (0a5b7ae8): grouped partial evaluation, the Briggs-Torczon
    sparse set, the failure analysis with H1 and the scaled-experiment
    design.
  - **may93182** (11c46f4d): the 256-way bit-plane Keccak and the
    delta-swap transpose.
  - **Th0rgal** (76ccfa1c): T1 incremental round 2 (extended here to the
    22-word all-ones support). The compiler's register residency covers T3.
    Our table builds on T2, their sparse set at address 0.
- **Credited.**
  - 5kyguy (78676cf6) independently and concurrently specialised delta
    swaps for structurally zero rows and pruned the last round to a 140-bit
    bucket; nothing from it is used.
  - tekkac (b001199a): lane-complement chi on this track, after the Keccak
    team.
  - ercumentyildirim (c7fa1a56; r5: 4c969300): the last-round early abort,
    which the kept planes extend.
  - zeeshan8281 (cbf7998d): the 255/256 message budget.
  - zeeshan8281 and tekkac (f58275ef): exact per-message charging.
  - mitchuski (02d6a703): the every-load-and-store-charged reading.
- **Not used.** Nothing from GordoAR's e715ab73 or df2619d4 is used, except
  the format of the integer certificate in Section 8.
- **Ours.** The 22-word all-ones support prefix construction, Lemmas 1-3, 7,
  9-11, the kept planes with verify and continue, the tagged-id table, the
  counted program and any errors.

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

For group g the algorithm draws one fresh uniform 256-bit word R_g whose four
64-bit lanes populate lanes $L_0, L_1, L_2, L_5$ (256 uniform random bits per
group), and sets the remaining four 64-bit lanes of the 64-byte prefix $P_g$ as
follows:

    c0 = L0 XOR L5
    L3 = 0x06 XOR M64 XOR rotl64(c0, 1)
    L4 = 0
    L6 = 0
    L7 = L2 XOR rotr64(c0, 1)

where `M64 = 2^64 - 1`. The 64-byte prefix $P_g = (L_0, \dots, L_7)$ is stored.
For z in {0,1}^32:

    m(g, z) = P_g with LE32(z) XORed into bytes 0..3 and into bytes 40..43.

So z is XORed into the low 32 bits of lane 0 (x=0, y=0) and of lane 5
(x=0, y=1).

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

**Lemma 1 (round-1 theta is invariant).** Lanes 0 and 5 lie in column 0 and
carry the same difference z. Every column parity, and so every D word, is
therefore independent of z. Hence theta(A(z)) = theta(A(0)) XOR (z in lanes
0 and 5).

**Lemma 2 (A2 is affine in z).** Rho/pi sends lane 0 to row 0 (rotation 0)
and lane 5 to row 3 (x = 1, rotation 36). Each of these chi rows has exactly
one varying input. With c a group constant, v -> (NOT v) AND c and
v -> (NOT c) AND v are affine in v. So A2(z) = A2(0) XOR sum_j z_j L_j
exactly, with fixed vectors L_j.

**Lemma 3 (22-word all-ones support).** Let j' = (j + 36) mod 64.
- In round 1, the column parities of $P_g$ are $C_1[0] = c_0 = L_0 \oplus L_5$,
  $C_1[2] = L_2 \oplus L_7 = \operatorname{rotr}_{64}(c_0, 1)$, and
  $C_1[3] = L_3 \oplus \texttt{0x06} = \texttt{M64} \oplus \operatorname{rotl}_{64}(c_0, 1)$,
  so $D_1[1] = C_1[0] \oplus \operatorname{rotl}_{64}(C_1[2], 1) = 0$ and
  $D_1[4] = C_1[3] \oplus \operatorname{rotl}_{64}(C_1[0], 1) = \texttt{M64}$.
- In round-1 $\chi$ row 0 at plane $j$, the neighbours of $X=0$ (lane 0) are
  $X=1$ (from lane 6: $L_6 \oplus D_1[1] = 0$) and $X=4$ (from lane 24:
  $0 \oplus D_1[4] = \texttt{M64}$, whose complement is 0). Thus $u_3 = u_4 = 0$,
  and only lane 0 flips by $W$ (all-ones) at bit $j$.
- In round-1 $\chi$ row 3 at plane $j'$, the neighbours of $X=1$ (lane 5) are
  $X=2$ (from lane 11: $0 \oplus D_1[1] = 0$) and $X=0$ (from lane 4:
  $L_4 \oplus D_1[4] = \texttt{M64}$, whose complement is 0). Thus $v_0 = v_4 = 0$,
  and only lane 16 flips by $W$ at bit $j'$.
- Consequently, the round-1 output varies only in bit $j$ of lane 0 and bit
  $j'$ of lane 16, both with difference $W$. Round-2 $\theta$ has nonzero parity
  changes only at $dC_2(0, j) = W$ and $dC_2(1, j') = W$, and nonzero $D$-word
  changes at 4 positions: $dD_2(1, j) = dD_2(4, (j+1) \bmod 64) = dD_2(2, j') =
  dD_2(0, (j'+1) \bmod 64) = W$.
- Hence $L_j$ vanishes outside a fixed list `SUPPORT_j` of **22 words**
  (5 lanes in each of the 4 changed $D_2$ columns plus $(0, j)$ and $(16, j')$),
  and **every one of the 22 words equals $W$** (independent of the group prefix;
  no basis array `BAS` or `COEF` is needed).

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

**Lemma 6 (AND-free incremental round 2 on 22 all-ones support words).**
- **What is maintained.** O2P is the round-2 output (chi, iota) with
  round-3 theta applied, in the encoding Q3 of Lemma 8. When A2 changes by
  $W$ on `SUPPORT_j`, rho/pi sends the 22 support words to **21 chi rows**
  (20 single-input rows and 1 two-input row at $Y=0, b'=(15+j) \bmod 64$
  with changed inputs $X \in \{2, 4\}$).
- **Chi difference (0 AND gates).** Because every changed input flips by
  $c = W$:
  - on each of the 20 single-input rows (input $X$ flipped by $W$),
    `dout[X] = W`, `dout[X-1] = a[X+1]`, and `dout[X-2] = a[X-1] XOR W`;
  - on the two-input row ($X \in \{2, 4\}$ flipped by $W$),
    `dout[0] = a[1] XOR W`, `dout[1] = dout[2] = a[3]`, `dout[3] = a[0]`,
    and `dout[4] = W`.
  Across all 21 rows, `dout` depends on **43 distinct $A_2$ words**, which
  are disjoint from the 22 flipped $A_2$ support words (so load order does
  not matter), and flipping the 22 support words of $A_2$ takes 22 loads,
  22 NOTs, and 22 stores.
- **Theta and the patch.** `dC[x][b] = XOR_Y dout(x, Y, b)`, `dD[x][b] =
  dC[x-1][b] XOR dC[x+1][b-1]`, and the patch is `O2P(x+5Y, b) ^= dout(x, Y, b)
  XOR dD[x][b]`. Exactly **554 O2P words** have a nonzero patch, taking **101
  distinct expressions** over the 43 loaded $A_2$ words and $W$: 139 words are
  patched by $W$ alone (139 NOTs on `O2P`), and the remaining 415 words use 74
  distinct non-empty XOR subsets of the 43 loaded $A_2$ words (41 singletons,
  28 pairs, and 5 triples each containing one of the pairs: $28 + 5 = 33$ XORs),
  with 65 negated subsets ($39 + 26 = 65$ NOTs).
- **Exactness.** Theta is linear and the encoding is XOR with a constant,
  so the patched O2P equals the encoded, theta'd round-2 output of the new
  A2.
- **Cost.** 22 $A_2$ support loads + 43 $A_2$ read loads + 554 `O2P` loads =
  **619 loads**; 22 $A_2$ stores + 554 `O2P` stores = **576 stores**; and
  $33 + 415 = 448$ XORs + $22 + 65 + 139 = 226$ NOTs = **674 gates** (0 ANDs),
  or **1,869 operations** before cross-phase adjustment (charged at **1,896
  operations** after accounting for the 27 fewer `O2P` words forwarded into
  round 3's start planes when 554 instead of 1,081 `O2P` words are touched).

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
of rounds 3, 4, 5 are (2, 39, 34), found by a search over the exact count.

**Lemma 8 (lane-complement encoding; as in bs3).**
- Each stored lane L has a compile-time polarity pi_L: the stored word is
  the true word XOR pi_L * (all-ones).
- Per chi row the program uses the cheapest exact gate plan for the given
  input and output polarities: NOT b AND c equals s_b AND s_c, or NOT(s_b OR
  s_c), with at most one shared complemented copy and the iota bit folded
  in. The plan comes from an exhaustive search over the 32 complemented-copy
  sets.
- The patterns are P34 (output of rounds 2, 3, 4) and P5 (output of round
  5). Rounds 3-5 read Q3 = fpol(P34), and the last round reads fpol(P5).
- Every chi row of rounds 3-5 costs at most 1 NOT. The last round takes,
  per plane, the digest polarities that need no NOT; moved to key rows,
  these fixed bits form KEYMASK (33 of the 140 bits set).
- A2 is unencoded. The Lemma 6 differences preserve the encoding of O2P.

**Lemma 9 (kept planes, key rows and the rotating-frame transpose).**

    KEEP = (0, 1, 2, 3, 4, 9, 10, 11, 16, 17, 18, 22, 23, 24, 25, 29, 30, 31,
            32, 37, 38, 39, 40, 44, 45, 46, 47, 51, 52, 53, 54, 58, 59, 60, 61)

(as in bs3; re-annealed under the new count, still the best).

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
  - The row with even parity has an odd-parity partner in every stage, so
    it never moves.
- **Zero rows.** A statically zero row needs no rotation (rot(0) = 0) and
  is substituted into the formulas:
  - zero mover: t = b AND M_d; b ^= t; a = t, 2 operations;
  - zero stayer: u = rot(a, .); t = u AND M_d; b = t; a = u XOR t, 3
    operations;
  - both rows zero: nothing.

  After a swap, both rows are treated as nonzero; the zero pattern is known
  at compile time.
- **Phase 1.** For each nonempty block the last round computes the block's
  kept-plane rows in registers and applies stages 1, 2, 4, 8, 16 in the
  cheapest static order. It costs 400 per full block and 170 for block 4,
  1,770 in all.
- **Phase 2.** For each gi = 0..31 the program takes the rows 32i + gi,
  loads rows i <= 4 only (blocks 5-7 are zero), and applies stages 32, 64,
  128. It costs 1,520 in all.
- **Frame fix.** One rotation per row left outside frame 0, 128 in all.

The transpose costs 3,418 ALU operations (1,770 + 1,520 + 128). Its memory
traffic (111 stores and 111 loads of ROWS between the phases, and 26 loads
of the delta-swap masks, 20 in phase 1 and 6 in phase 2) is counted in the
Section 5.2 ledger: last round + phase 1 = 280 chi/iota + 99 state loads +
20 mask loads + 111 ROWS stores + 1,770 = 2,280; phase 2 row = 1,520 + 128
+ 111 ROWS loads + 6 mask loads + 1,536 table = 3,301. By Lemma 5, row 32i + gi is
then the key of slot 32i + gi = decode_slot(8gi + i).

**Lemma 10 (dependency cone with start planes).** The last round on plane b
reads the 5 diagonal lanes at source plane (b - RHO[L]) mod 64. Round 5
must therefore store only these 175 words. None of them lies on round 5's
start plane 34, so no round-5 fix word is needed. For a round with start
plane s whose input lacks D on plane s_in, needed outputs propagate
backwards:
- a needed stored word (L, b) with b != s needs its chi output, C[x-1][b]
  and C[x+1][b-1];
- a needed fix column x needs C[x-1][s] and C[x+1][s-1];
- a parity needs its 5 chi outputs;
- a chi output needs its 3 row inputs, plus the fix wherever the source
  plane is s_in.

The round emits exactly these values. Round 5 then computes 1,161 chi
outputs and 229 parities and reads 1,363 words with all 5 fix columns.
Round 4 needs all 320 parities and reads all 1,600 words. Every computed
word is given by the same formula from the same inputs as in the full
round, and no omitted word is ever read. Two generator checks hold:
- with every word declared needed, the generator emits the full rounds
  exactly;
- with all 64 planes kept and v3opt3's start planes, it reproduces the
  per-block counts of our full-width v3opt3 program exactly (Section 10.1).

**Lemma 11 (straight-line compiler).** The code of one ctz leaf is a single
straight line, compiled in four steps:
1. It is put in SSA form.
2. Loads are store-to-load forwarded. A direct load whose word was written
   or loaded earlier in the block takes the value from the register that
   still holds it. All addresses are instruction constants, so aliasing is
   decided exactly. A store to a scratch word of the step (the two state
   buffers, ROWS, the C0 and fix save areas) is dropped when every later
   load of it was forwarded. Scratch words are never read outside the step.
3. Registers are allocated by interval colouring. This is exact for
   straight-line code: the register count is the maximum number of
   simultaneously live values.
4. The result runs on the counted simulator.

No step changes a computed value. Every block uses at most 62 registers,
plus the persistent s and c, so 64 in all.

## 5. The algorithm and its counted program

### 5.1 Run and batch setup

**Once per run.**
- TAG = RAND AND (2^256 - 2^128), so c = TAG*2^128 + 0.
- CNT = 0.

**Once per batch.**
- draw 256 random 256-bit words (256 bits per group for lanes $L_0, L_1, L_2, L_5$),
  transpose into bit-planes, form lanes $L_3, L_4, L_6, L_7$ in bit-planes,
  and store the prefixes at PREF + 512*beta + 2p + w;
- store the padding planes;
- compute the round-1 D words, round 1 and A2;
- store the delta-swap masks;
- compute O2P and set s = 0 (no `COEF` or `BAS` computation is needed since
  every support difference is identically $W$).

Setup is below 320,000 operations per batch (< 484,187 of 5596b5be). With
batch-loop control this is < 2^-20 per message.

### 5.2 Per z-step program (fully unrolled; worst path)

There are two persistent registers: s (the step counter t) and
c = TAG*2^128 + n.

    (a) control, t >= 1 (16): s = s + 1 ; 5-level branch tree on ctz(s):
        v = s AND mask ; (v == 0) ; branch   (5 levels; no indirect jump)
    (b) leaf j: AND-free incremental round 2 on 22 support words, block j
        (Lemma 6), followed in line by its own copy of the step body (32
        copies; no jump):
        R3 (start 2), R4 (cone, start 39), R5 (cone, start 34) with the
        last-round blocks interleaved as soon as their round-5 planes exist,
        phase 1, phase 2, the frame fix and 256 table steps (5.3)
    (c) loop test (2): (s < 2^32 - 1) ; branch

At t = 0 the body runs without (a) and round 2. Static counts of all 32
leaves lie between 31,898 and 31,903.

**Ledger (one worst-path z-step).**

| block | 5596b5be | ops | gates | loads | stores | ROT/ADD/CMP/branch |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| control | 16 | 16 | 5 | 0 | 0 | 11 |
| incremental round 2 (Lemma 6) | 3,969 | 1,869 | 674 | 619 | 576 | 0 |
| round 3 | 9,791 | 9,818 | 6,695 | 1,573 | 1,550 | 0 |
| round 4 (cone) | 9,351 | 9,351 | 6,484 | 1,552 | 1,315 | 0 |
| round 5 (cone) | 5,266 | 5,266 | 3,855 | 1,312 | 99 | 0 |
| last round, 35 planes + phase 1 | 2,280 | 2,280 | 1,696 | 119 | 111 | 354 |
| phase 2 + frame fix + 256 table steps | 3,301 | 3,301 | 1,472 | 373 | 256 | 1,200 |
| loop test | 2 | 2 | 0 | 0 | 0 | 2 |
| **total per 256 messages** | **33,976** | **31,903** | **20,881** | **5,548** | **3,907** | **1,567** |

Gates are XOR/AND/OR/NOT after store-to-load forwarding; each row is
gates + loads + stores + the last column (combined incremental round 2 +
round 3 is 1,869 + 9,818 = 11,687, i.e. 1,896 charged to incremental round 2
relative to the 9,791 round-3 baseline).

By opcode:

| loads | stores | XOR | AND | OR | NOT | ROT | ADD | CMP | branch |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 5,292 direct + 256 register | 3,651 direct + 256 register | 14,489 | 3,180 | 2,042 | 1,170 | 786 | 257 | 262 | 262 |

There are no shifts and no MOVI. Loads and stores are fewer than the round
structure suggests because of Lemma 11.

### 5.3 Tagged-id table

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
  XORs LE32(z) into bits 0..31 of the first and bits 64..95 of the second.
  This is 20 operations per message; a garbage id rebuilds some 64-byte
  string.
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
  - halt: 64 / 66 operations for the whole table step without the 2 insert
    operations, 68 with them; we charge 68;
  - abort (CNT reaches VCAP): a prefix of the continue path without the
    register restore, the jump back and the insert, so within the 68-op
    charge; the bound's halting term is then unused.

  Continue and halt each add 2 units.

The cap is an instruction immediate:

    VCAP = floor(N^2 / 2^141) + 2^91 + 2^61.

## 6. Correctness (unconditional)

- **Evaluator exactness.** Lemmas 2-3 and 6 keep A2 and O2P exact at every
  t. Lemmas 4, 7, 8, 10 and 11 make every needed word of rounds 3-5 exact
  in its encoding. Lemma 9 makes the key of slot p equal key_of_digest(K*)
  of message p. Section 10 checks this bit for bit.
- **Outputs.** The run outputs only two distinct 64-byte strings whose
  256-bit digests were equal under two reference evaluations, which is a
  full collision. A key match or a garbage word never produces output by
  itself.

## 7. Success probability

The run halts at the first verified collision. The failure events are:

- **F3:** two groups produce the same message. Each group's prefix has 256
  independent uniform bits in lanes $L_0, L_1, L_2, L_5$, and $m(g, z) = m(g', z')$
  requires $(L_0, L_1, L_2, L_5)$ of $g$ and $g'$ to differ only by $z \oplus z' \in \{0,1\}^{32}$
  in the low halves of $L_0$ and $L_5$, so $\Pr[F_3] < \binom{255 \cdot 2^{88}}{2} \cdot 2^{32} / 2^{256} < 2^{-33}$.
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
events F1, F2 and the genuine-candidate part of F4 (proof Section 7), the
N = 255*2^120 digests of the grouped message set {m(g, z)} (independent
structured prefixes P_g with 256 uniform bits per group, all z in {0,1}^32,
processed in any fixed order chosen independently of the digests, in
particular the order of Section 2: batch by batch, t = 0..2^32-1 with z =
gray(t), slots p = decode_slot(q) = 32*(q mod 8) + floor(q/8) for q = 0..255)
behave like N independent uniform 256-bit values, i.e. Pr[F1] <=
exp(-N(N-1)/2^257), Pr[F2] <= N^3/6 * 2^-396 and, since the 140-bit key is a
fixed function of 140 digest bits, the number Y1 of message pairs with equal
keys has E[Y1] <= N^2/2^141 and Var[Y1] <= E[Y1].

With N = 255 * 2^120:

- **F1.** Under H1, Pr[F1] <= exp(-N(N-1)/2^257) = exp(-(255/256)^2/2 +
  tiny) < 0.6089000.
- **F2.** Under H1, Pr[F2] <= N^3/6 * 2^-396 < 2^-14.
- **F4.** Continued candidates are Y1 + Y2.
  - Genuine ones are distinct pairs (stored number, n) with equal keys, so
    they number at most Y1. Chebyshev gives Pr[Y1 >= E + 2^91] <=
    E/2^182 <= 2^-67, where E = floor(N^2/2^141) < 2^115.
  - Garbage ones, Y2, satisfy E[Y2] <= N * 2^-128 < 1 for any initial
    memory (Section 5.3; no heuristic), so Markov gives Pr[Y2 >= 2^61] <=
    2^-61.

  Hence Pr[F4] <= 2^-67 + 2^-61.
- **Total.** Success >= 1 - Pr[F1] - Pr[F2] - Pr[F3] - Pr[F4] > 0.39105.
  We claim 0.39, which leaves an allowance of 0.00106.

The scaled analogue of Y1 is the per-trial `masked_pairs` count. Its
variance/mean ratio is about 1 (Section 10.3).

**Rigorous partial support (jaazinn's argument).** For groups g != g', the
messages m(g, z) and m(g', z') are independent and identically distributed
over the $2^{256}$ structured prefixes. By Cauchy-Schwarz they collide with
probability >= 2^-256. Within-group pairs are a 2^-96 fraction, so the
expected number of colliding pairs is at least (1 - 2^-96) * N(N-1)/2^257. H1
is needed for the second-moment behaviour behind Pr[F1], for F2 and for Y1.

**What does not change the message set.** Bitslicing, batching, the
incremental round 2, the cone, the start planes, the compiler, the 140-bit
key and the encodings fix only how and in which order digests are computed.
That order is a function of (beta, t, q), never of digests.

## 8. Time bound

Per message the main loop charges 31,903/256 = 124.62109375 operations plus
amortised setup (< 2^-20). This covers the Gray and round-2 updates, rounds
3-6, the transpose, every table load, store, compare and branch, and all
loop control. On top come at most VCAP continued candidates (2 units + 68
operations each), one halting candidate (2 units + 68 operations) and the
per-run initialisation (< 10 operations, bounded by 1 unit). So, in every
run (no restarts),

    T <= N (31,903/256 + 2^-20)/1626 + VCAP (2 + 68/1626) + (2 + 68/1626) + 1
      = 2^124.28864 + 2^116.019 + 3 < 2^124.29332.

**Integer certificate.** With K = 2^28 * 1626,

    A = T K = N (31,903 * 2^20 + 256) + VCAP (2*1626 + 68) 2^28 + (2*1626 + 68) 2^28 + K

is an integer, and A^1000 < 2^124295 * K^1000 (and even A^1000 < 2^124294 * K^1000)
holds exactly. The claimed time_log2 is therefore **124.295**, rounded up.

- **Slack.** The claim 124.295 holds with W up to 31,940 ops per z-step (37
  extra ops per z-step of slack).
- **Expected verification work.** Under H1 it is about 2^116 units, about
  102 operations per z-step on average.
- **Preprocessing.** preprocessing_log2 = 0: setup is per batch and inside T.

## 9. Sensitivity of the bound to conventions

Same program, worst z-step, the candidate term included. N = 255 * 2^120
unless stated.

| reading | ops/z-step | ops/message | time_log2 |
| --- | ---: | ---: | ---: |
| every executed primitive once, 64 registers (claimed) | 31,903 | 124.62 | 124.29331 -> 124.295 |
| + one address addition per direct load/store, + one MOVI per ALU immediate | 41,343 | 161.50 | 124.667 |
| as above, + one op per shift or rotation amount | 42,129 | 164.57 | 124.694 |
| exact Gray-sequence average instead of the worst leaf | 31,900.8 | 124.61 | 124.29321 -> 124.295 |
| N = 2^128 | 31,903 | 124.62 | 124.299 |
| N = 0.99448 * 2^128 (GordoAR df2619d4's budget; not claimed) | 31,903 | 124.62 | 124.291 |
| logic gates only (reference; needs far more than 64 registers) | 20,908 | 81.67 | 123.687 |
| e715ab73's reading: direct loads/stores to a fixed bank free (**not claimed**) | 22,987 | 89.79 | 123.823 |
| 5596b5be program (62-word support) at this budget | 33,976 | 132.72 | 124.384 |

We do not adopt the fixed-bank reading. Under our 64-register reading,
every one of the 8,943 direct loads and stores per z-step is charged.

## 10. Evidence

### 10.1 Counted simulator and incremental round-2 verification (participant evidence)

- **The simulator.** Rounds 3-6, the transpose and the tagged-id table are
  identical to 5596b5be's counted 256-bit word-RAM program (explicit
  64-register file, high-water check, counter per primitive, separate counts
  for direct and register addresses, immediates and shift amounts). In
  Block (b), `_verify_incr2_counts()` in `experiments/s3r6_bitslice_birthday.py`
  symbolically verifies for every $j \in \{0, \dots, 31\}$ that `SUPPORT[j]`
  has 22 words, `ROWS2[j]` has 21 rows, `dout` reads 43 distinct $A_2$ words
  disjoint from `SUPPORT[j]`, and the `O2P` patch touches exactly 554 words
  using 101 distinct linear/affine expressions (139 equal to $W$, 74 distinct
  XOR subsets over the 43 loaded words formed in 33 XORs and 65 NOTs).
- **Hostile memory.** Before every z-step, all scratch words of the step
  are overwritten with random junk. A read outside the cone, or of a word
  not yet written in the step, would corrupt a key. Never-written table
  words are set, by batch, to all-ones, random, zero, or adversarial (high
  half = TAG, low half random or out of range).
- **Keys.** Every key was compared with key_of_digest(int.from_bytes(
  sha3_256(m, 6), "little")) from `verifier/keccak.py`:
  - 16 batches x 4 z-steps x 256 (seeds 2026, 4711, 31337): 16,384 keys
    each;
  - 24 x 5 (seed 777): 30,720 keys; 8 x 6 (seed 55555): 12,288 keys;
  - every Gray block j = 0..31 plus 40 consecutive steps: 17,024 keys for
    each of the seeds 2026, 4711, 777, 31337 and 55555;
  - long runs of 300, 200 and 120 consecutive steps: 15,600, 10,400 and
    6,240 keys.

  There were 0 mismatches. The register high-water mark was 64.
- **Table words.** Every table word written in these runs decodes from its
  id (TAG, beta, slot, z) to a message whose key is its address. 4,096
  (7,680 for seed 777) adversarial garbage candidates were verified and
  continued.
- **Candidate paths** (paths_max, ledger):
  - Replaying a z-step gives 256 genuine candidates. The rebuilt messages
    equal the true ones, the digests differ, CNT reaches 256 and the run
    continues.
  - Continue: 64 / 68 operations above the 6-op hot path (jump back
    included). Halt: 64 / 66 operations for the whole table step without
    the 2 insert ops, and 68 with them; 68 is charged. Each also costs 2
    units. Equal digests were forced with a constant test hash, for
    control flow only.
- **Generator checks.**
  - With every word needed, the cone generator emits the full rounds 3-5
    exactly (9,910 / 9,960 / 7,420 instructions before compilation).
  - With all 64 planes kept and start planes (2, 47, 42), the per-block
    counts equal our full-width v3opt3 program's (3,969 / 9,791 / 9,827 /
    7,245 / 4,161 / 2,261).
- **Mutations.** Removing one round-4 cone word or one round-5 cone word,
  dropping a fix column, or treating a kept plane's rows as zero is always
  caught by the key comparison.
- **Experiment evaluator.** The evaluator of 10.2 equals key_of_digest(
  `sha3_256(m, 6)`) on 22,400 keys (a 1,100-step Gray walk over z bits
  0..10 and a 300-step walk over z bits 22..30), with 0 mismatches. Its
  KEEP, ROWOF, KEYMASK, start planes and stage orders equal the program's.
- **Not shipped.** The counted program exceeds the 64 KiB
  experiment-source budget and is not shipped; the ledger and opcode table
  above sum exactly, and the shipped script asserts both the 22-word
  incremental round-2 counts and the 3,418-op transpose count.

### 10.2 Declared experiments (organizer-executed, `python-message-pairs-v1`)

All four experiments run `experiments/s3r6_bitslice_birthday.py`. It mirrors
the counted program:
- per-batch structured prefixes $P_g$, A2, and O2P, and Gray updates with
  the AND-free incremental round-2 patch on the 22 all-ones support words;
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
- the 22-word all-ones support of each coefficient column;
- O2P against a rebuild after the batch;
- at every step, the zero key rows, and the transpose against the full
  6-op transpose;
- every key of the batch through the tagged-id table, with adversarial
  never-written words (1/16 carry the run's TAG, so the
  verify-and-continue path must be taken). Every table word must decode to
  a message whose key is its address.

Removing a round-4 or round-5 cone word, dropping a fix column, applying
the fix words on the wrong plane, corrupting a table word, never taking the
garbage path, or treating a key row as zero all make the script fail.

**Scale.** Each seed derives fresh structured 64-byte prefixes with SHA-256.
N_t = 2^9 and an 18-bit mask give N_t^2/2^18 = 1 = N^2/2^256 up to (255/256)^2.
The uniform-model success probability is 0.39307 (100.6 +- 7.8 per 256
trials). Layouts:
- `k6r6-bs-full-width`: 256 groups x 2;
- `k6r6-bs-spread`: 16 x 32;
- `k6r6-bs-single-group`: 1 x 512;
- `k6r6-bs-high-z`: 4 x 128 with z = gray(t) << 25.

The experiment ids and masks are bs3's.

### 10.3 Local runs (not organizer evidence)

On the local seed suites (256 trials per layout) and pooled 1,024-trial runs
with the 22-word all-ones structured prefixes:
- `public`: 94 / 103 / 98 / 94 successes of 256;
- `bs3-rv-1`: 94 / 100 / 109 / 93 of 256;
- `committee-c1`: 105 / 97 / 119 / 99 of 256;
- pooled over 1,024 trials per layout (`pool`): 420 / 387 / 422 / 398
  successes ($0.4102 / 0.3779 / 0.4121 / 0.3887$, $z = +1.12 / -0.99 /
  +1.25 / -0.29$ against 0.39307), with per-trial masked-pair variance/mean
  ratios $0.971 / 1.049 / 0.960 / 1.041$, consistent with $\operatorname{Var}[Y_1] \le E[Y_1]$.

No self-check failed in any run.

## 11. Memory

| array | 32-byte words | bytes |
| --- | --- | --- |
| S (tagged ids, at 0) | 2^140 | 2^145 |
| PREF (at 2^170) | < 2^97 | < 2^102 |
| A2, O2P, masks, two state buffers, ROWS, CNT, save area (at 2^240) | < 2^14 | < 2^19 |
| code (32 fused leaves, setup) | < 2^21 instructions | < 2^26 |

Total < 2^145.01 bytes; we claim 146. The key array of bs3 (2^133 bytes) is
gone. Memory is reported only.

## 12. Limitations

- **H1 is a heuristic.** It extends the grouped structure from the tested
  scale (N_t = 2^9, 18-bit masks) to N = 255 * 2^120 and the 256-bit
  digest. F2 and Y1 cannot be scaled down faithfully and are bounded only
  under H1. Organizer seeds are public. A 256-trial experiment resolves the
  success frequency only to about +-0.03, and the 0.00106 allowance is not
  statistically certified.
- **Algebraic degree.** Within a group the digest has degree at most 32 in
  z. With 32 z bits, this gives no zero-sum on any affine subspace of z.
  This concerns only within-group pairs (a 2^-96 fraction).
- **Source of the gain.** The gain comes from operation-level pricing and
  the 22-word all-ones support in round 2. All executed work, including all
  memory traffic and every candidate verification, is charged.
- **Register assumption.** The 64-register machine is an assumption, and
  the program uses all 64. Section 9 gives stricter readings, all at most
  124.694.
- **Rounding slack.** The claim 124.295 leaves 37 operations per z-step of
  slack (Section 8).
- **Scope.** No sub-birthday attack, collision certificate or full-scale
  run is claimed.

## 13. Credit

- **Co-authors**, in the sense of Section 0:
  - **jaazinn** (0a5b7ae8);
  - **may93182** (11c46f4d);
  - **Th0rgal** (76ccfa1c: T1 extended to 22-word all-ones support, T3
    subsumed by Lemma 11, the table builds on T2).
- **Credited:**
  - tekkac (b001199a, f58275ef);
  - ercumentyildirim (c7fa1a56, 4c969300);
  - zeeshan8281 (cbf7998d, including the 255/256 budget);
  - mitchuski (02d6a703);
  - 5kyguy (78676cf6: concurrent zero-row delta swaps and a 140-bit
    last-round bucket; nothing used).

Errors are ours.
