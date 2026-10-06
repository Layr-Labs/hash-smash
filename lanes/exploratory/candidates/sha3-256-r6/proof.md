# sha3-256-r6: bitsliced grouped birthday search, time_log2 = 124.650

## 0. Summary and credit

A generic birthday search over full 256-bit digests; no cryptanalytic
weakness of SHA3 is claimed. It combines known implementation ideas:

- **Grouping** (jaazinn's framework): messages come in groups of 2^32 that
  share a random prefix. Inside a group, the round-2 theta output A2 is an
  exactly affine function of the 32-bit group counter z (Lemma 2), so round 1
  and the linear part of round 2 are paid once per group.
- **Bitslicing** (may93182's 256-message bit-plane Keccak): each 256-bit word
  holds one state bit of 256 messages. Rotations are renamings of word
  addresses; an explicitly priced delta-swap transpose produces the keys.
- **Lane complementing** (the Keccak team's lane-complement transform, applied
  to this track's bit-plane circuit by tekkac in b001199a): every lane is
  stored with a fixed polarity, so chi needs one NOT per row in rounds 3-5
  and none in the last round, with round constants folded into polarity.
- **Incremental round 2, theta at the store, and fused last round** (winglock,
  6a250bf): each Gray step patches the stored, already theta'd round-3 input
  with the exact chi difference of the 60 affected rows; each round adds the
  next round's D words while a plane's outputs are in registers; the last round
  fuses five transpose stages.

New in this package:
1. **8-word basis, uncomplemented-product linear folding and closed-form
   cancellation in incremental round 2** (Lemma 6): out of the 62 support words
   of COEF[j], 20 are identically all-ones (W, independent of the group prefix)
   and the remaining 42 take at most 8 distinct group-dependent values U_0..U_7.
   Loading only U_0..U_7 (8 loads instead of 62), eliminating the 34 AND gates
   on the 17 single-input rows with c = W, evaluating both two-input rows in
   closed form (9 A2 loads, 3 NOT, 2 AND, 1 XOR instead of 10 A2 loads, 18 NOT,
   18 AND, 17 XOR), rewriting `(NOT a[X-1]) AND c = (a[X-1] AND c) XOR c` on 22
   single-input rows to save 22 NOT gates while folding the linear `+c` shifts
   into dC/dD/O2P (costing +2 net XORs for -17 ops), and cancelling two dD
   columns cuts Block (b) from 4,149 to **3,959 operations** for every j = 0..31.
2. **Countdown Briggs-Torczon sparse set at base 0** (Section 5.3): placing S
   at base address 0 (h = K SHR 116 IS the table address, removing `a = h + SB`)
   and counting the message index n down from 2^256 - 1 by adding M1 = 2^256 - 1
   (so `n < i` holds iff `i in {n + 1, ..., 2^256 - 1}`, the exact set of DK
   addresses written earlier in the run, disjoint from S at 0..2^140 - 1) cuts
   every worst-path sparse-set step from 11 to **10 operations** (-256 ops per
   z-step) and frees register SB.
3. **Full 64-register cross-phase residency and in-place row/parity scheduling**
   (Lemma 7, Section 5.2): scheduling row Y = 4 and column-0 parity/store in
   26 registers inside ROUND_TS, accumulating round-5 parities row-by-row, and
   inlining planes b = 0..4 of R3 into each leaf j allows passing **55 modified
   O2P words** across Block (b) -> R3 (-55 loads), **46 ST0 words** across
   R3 -> R4, **49 ST1 words** across R4 -> R5, **41 diagonal words** across
   R5 -> LAST, and **52 row words** across LAST -> PHASE2 (**-431 operations**
   total; or **-343 operations** under a 56-register cap).

A z-step evaluates 256 messages with one counted, fully unrolled program
(branches only in the ctz tree, the table step and the loop test). Its
worst path is **40,802 executed primitives** (159.39 per message with setup).

| quantity | value |
| --- | --- |
| messages N | 2^128 = 2^88 batches x 256 groups x 2^32 values of z |
| ops per z-step (256 messages), worst path | 40,802 (every executed primitive) |
| ops per message charged | 159.39 (40,802/256 = 159.3828125 + setup < 2^-20) |
| total T | <= 2^128 * 159.39/1626 + 3 < 2^124.64931 |
| claimed time_log2 | **124.650** (56-register schedule: 40,890 ops -> 124.653) |
| success probability | >= 0.39334 under H1; claimed 0.39 |
| memory | < 2^145.01 bytes; claimed 146 |

**Credit.** **jaazinn** (Yukon ticket 0a5b7ae8, blake3-r2, in review)
originated grouped partial evaluation, the Briggs-Torczon sparse set on the top
140 key bits, the failure analysis with heuristic H1 and the scaled-experiment
design, and is named as co-author in that sense. **may93182** (11c46f4d, in
review) introduced for this track the 256-way bit-plane Keccak and the
delta-swap transpose at 6 operations per row pair, and is likewise named as
co-author in that sense. **winglock** (6a250bf, in review) introduced the
incremental round-2 patch on A2/O2P, theta at the store with plane-0 fix-up,
the fused last round and the 64-register word-RAM program structure on which
this package builds directly, and is likewise named as co-author in that sense.
**tekkac** (b001199a) brought the Keccak team's lane-complement chi with round
constants folded into polarity to this track. The last-round early abort (the
digest-only last round, for which the previous round stores only the 5 diagonal
lanes 0, 6, 12, 18, 24) is **ercumentyildirim**'s (c7fa1a56; sha3-256-r5:
4c969300). Charging the exact per-message count instead of a rounded one
follows zeeshan8281 (cbf7998d) and tekkac (f58275ef). The reading of Section 1
(64 registers, every load and store charged) corresponds to the
every-core-load-and-store-charged row of **mitchuski**'s sensitivity table
(02d6a703). None of them has reviewed this package. Errors are ours.

## 1. Target, machine and charging conventions

- Target `sha3-256-r6-prefix-v1`: the complete SHA3-256 sponge (rate 1088,
  capacity 512, suffix 0x06, pad10*1, zero IV), Keccak rounds 0..5 (RC[0..5])
  and all 256 output bits, as in `verifier/keccak.py:sha3_256(msg, 6)`.
  Messages are exactly 64 bytes (one block). Lane k (k < 8) is bytes
  8k..8k+7 read little-endian; lane 8 = 0x06, lane 16 = 0x80 << 56, the other
  lanes are 0. Lane index L = x + 5y. Rounds are numbered 1..6 below.
- Digest = lanes 0..3 after round 6, little-endian; K* = int.from_bytes(digest,
  "little"). The program stores the key K = K* XOR KEYMASK for a fixed public
  256-bit constant KEYMASK (Lemma 8). This is a bijection: equal keys and
  equal digests are the same event, and so are equal top 140 bits.
- Cost model `collision-frontier-v5`, C = 1626: one permutation costs 1 unit
  and any other 256-bit word primitive 1/1626. Machine: a 256-bit word RAM
  with 64 registers. The register count is our stated assumption; v5
  specifies only the word RAM. Both the 64-register schedule (40,802 ops) and
  a 56-register schedule (40,890 ops) are given. A word RAM has a fixed-size
  register file whose operands are not memory accesses; 64 registers of
  256 bits are 2 KiB, the size of a 32-entry 512-bit SIMD register file. A
  memory-to-memory reading (every ALU operand loaded and every result
  stored) is a different machine; we do not claim the bound under it.
- **Charging (the reading we claim).** Every executed primitive of the v5
  list costs 1: every load and store (direct or register-addressed), XOR, AND,
  OR, NOT, shift, add, compare, conditional branch, immediate move and random
  word. A constant address or an immediate operand is a field of the
  instruction that executes, not a separate executed operation. Register
  reads and writes are part of the instruction. No indirect jump is used and
  no rotation is ever executed (Lemma 4). Section 9 also prices one extra
  address addition per direct access, one MOVI per ALU immediate and each
  shift amount; every such variant stays below 125.07 (and row 2 is < 125.00).

## 2. Messages, groups, batches and processing order

For group g the algorithm draws two fresh uniform 256-bit words R0, R1. Their
little-endian bytes form a uniform 64-byte prefix P_g, which is stored. For
z in {0,1}^32:

    m(g, z) = P_g with LE32(z) XORed into bytes 0..3 and into bytes 40..43,

so z is XORed into the low 32 bits of lane 0 (x=0, y=0) and of lane 5
(x=0, y=1). Write g = 256*beta + p, batch beta < 2^88, slot p < 256. Batch
beta runs t = 0, 1, ..., 2^32 - 1 with z = gray(t) = t XOR (t >> 1). At each t
it evaluates the 256 messages m(256*beta + p, gray(t)) and offers them to the
table in processing order q = 0..255, slot

    p = decode_slot(q) = 64*floor(q/64) + 8*(q mod 8) + (floor(q/8) mod 8).

Batches run in order beta = 0, 1, .... Message (beta, t, q) has ordinal
k_ord = beta*2^40 + t*2^8 + q (the count of messages processed before it) and
is assigned the **countdown message number** n = (2^256 - 1) - k_ord. Every
message is evaluated exactly once, and N = 2^128.

**Bit mapping.** Word P(L, b) holds in bit position p the bit b of lane L of
message m(256*beta + p, z). Row p of input matrix w (w = 0, 1) is R_w of slot
p; after the transpose (Lemma 5), row k of matrix w is plane
P(4w + floor(k/64), k mod 64). Padding planes are constants: P(8,1) = P(8,2)
= P(16,63) = all-ones; all other planes of lanes 8..24 are 0.

## 3. Dependency analysis (exact)

Every step map except chi is GF(2)-linear on the 1600-bit state. Fix a group
and view each state as a function of z. A2 denotes the state after round 1
and the theta of round 2, which is the input of round-2 rho/pi.

**Lemma 1 (round-1 theta is invariant).** Lanes 0 and 5 lie in column x = 0
and carry the same difference z. Every column parity C[x] = XOR_y A[x+5y] is
therefore independent of z, and so is D[x] = C[x-1] XOR rot(C[x+1], 1). Hence
theta(A(z)) = theta(A(0)) XOR (z in lanes 0 and 5).

**Lemma 2 (A2 is affine in z).** Rho/pi sends lane 0 to position 0 (row 0,
rotation 0) and lane 5 to position 16 (row 3, x = 1, rotation 36). Chi acts
on each row separately as A'[x] = B[x] XOR (NOT B[x+1] AND B[x+2]). Rows 0 and
3 each contain exactly one varying input, so no AND multiplies two varying
inputs. With c a group constant, v -> (NOT v) AND c and v -> (NOT c) AND v are
affine in v. The round-1 output is therefore affine in z, and iota and round-2
theta are affine. So A2(z) = A2(0) XOR sum_j z_j L_j exactly, with fixed
vectors L_j (depending on the group). This is plain algebra.

**Lemma 3 (62-word support and 8-word basis).** Let j' = (j + 36) mod 64. In
round 1, flipping bit j of lanes 0 and 5 flips B(0,0,j) and B(1,3,j') by W
(all-ones). Thus the round-1 chi output varies only in bit j of lanes 0, 3, 4
with differences (W, u_3, u_4) and in bit j' of lanes 15, 16, 19 with
differences (v_0, W, v_4), where only 4 words (u_3, u_4, v_0, v_4) depend on
the group prefix. The changed column parities are:
C[0][j] = W, C[3][j] = u_3, C[4][j] = u_4, C[0][j'] = v_0, C[1][j'] = W,
C[4][j'] = v_4. Since C[c][b] enters D[c+1][b] and D[c-1][b+1], the 12 changed
D words are:
- 4 words equal to W: D[1][j] = W, D[4][j+1] = W, D[2][j'] = W, D[0][j'+1] = W
  (5 lanes each -> 20 support words equal to W, because the direct changes on
  lane 0 at j and lane 16 at j' lie in columns with D = 0);
- 8 words taking values U_0..U_7 in {u_3, u_4, v_0, v_4, u_3 ^ W, u_4 ^ v_0}:
  D[4][j] = u_3 (5 words), D[2][j+1] = u_3 (5 words), D[0][j] = u_4 (5 words;
  lane 0 has W ^ u_4, which equals D[3][j+1]), D[3][j+1] = W ^ u_3 ^ u_4
  (5 words), D[1][j'] = v_0 (5 words), D[4][j'+1] = v_0 ^ v_4 (5 words),
  D[0][j'] = v_4 (5 words), D[3][j'+1] = v_0 ^ v_4 (5 words), plus the two
  direct words (3, j) = u_3 and (19, j') = v_4.
Hence across all 62 support words of SUPPORT_j, **20 words are identically W**
and the **remaining 42 words take at most 8 distinct values U_0..U_7**, which
Setup stores as an 8-word basis per j.

## 4. Bitsliced Keccak, encodings and the transpose (exact)

**Lemma 4 (bitsliced round).** Write pisrc(X, Y) = (x, y) with y = X and
x = 3(Y - 3X) mod 5, the inverse of pi. On planes the round is: theta
C[x][b] = XOR_y P(x+5y, b), D[x][b] = C[x-1][b] XOR C[x+1][b-1],
A'(L, b) = P(L, b) XOR D[x][b]; rho/pi B(X, Y, b) = A'(L, (b - RHO[L]) mod 64)
with L = x + 5y, (x, y) = pisrc(X, Y); chi P'(X+5Y, b) = B(X,Y,b) XOR
(NOT B(X+1,Y,b) AND B(X+2,Y,b)); iota complements P'(0, b) for each bit b of
RC. Every operation is bitwise, so in bit position p it is exactly the scalar
round on message p. Rotations only change which address is read.

**Lemma 5 (transpose).** For d in {1, 2, ..., 128} let M_d have bit c set iff
c AND d = 0. A delta swap of rows a = R[i], b = R[i+d] (i AND d = 0) is
`t = a SHR d; t = t XOR b; t = t AND M_d; b = b XOR t; t = t SHL d; a = a XOR t`
(6 operations, 1 temporary register t) and exchanges entries (i, c+d) and
(i+d, c) for c AND d = 0. Stage d applies it to all 128 such row pairs and
swaps bit log2(d) of the row index with the same bit of the column index. The
8 stages act on different index bits, so they commute, and all 8 in any order
transpose the matrix.

**Lemma 6 (incremental round 2 with 8-word basis, uncomplemented-product
folding, and linear cancellation).** Let O2P be the round-2 output (chi, iota)
with the round-3 theta applied, stored in the lane-complement encoding Q3 of
Lemma 8. When A2 changes by L_j on SUPPORT_j, rho/pi sends the 62 words to 60
distinct chi rows (58 rows with one changed input, 2 rows with two; the map
(L, b) -> (X, Y, plane) shifts by (plane + j) mod 64):
- **Basis loads**: Load the 8 basis words U_0..U_7 of j into 8 registers (8
  loads; W is already in persistent register M1).
- **58 single-input rows and uncomplemented-product folding**: For a row with
  changed input a[X] -> a[X] XOR c, the output difference is dout[X] = c,
  dout[X-1] = c AND a[X+1], and dout[X-2] = (NOT a[X-1]) AND c. On the 17
  single-input rows where c = W, dout[X-1] = a[X+1] (0 ANDs) and dout[X-2] =
  NOT a[X-1] (1 NOT, 0 ANDs), saving 34 ANDs. On 22 of the 41 rows where c in
  U_0..U_7 (`UNCOMP_BASE0` shifted by +j mod 64), we use the exact identity
  `(NOT a[X-1]) AND c = (a[X-1] AND c) XOR c`, computing `p = a[X-1] AND c`
  without a NOT gate (-22 NOTs, reducing NOTs across all 58 rows from 58 to 36)
  and folding the linear basis term `XOR c` into dC, dD and `dout XOR dD`.
- **2 two-input rows**: (1) `(Y = 0, bp = (15 + j) mod 64)` with c_2 = c_4 = W:
  load B[0..4] (5 loads), update A2 at X = 2, 4 (2 XORs, 2 stores), and set
  `dout[0] = NOT B[1]` (1 NOT), `dout[1] = dout[2] = B[3]`, `dout[3] = B[0]`,
  `dout[4] = W`. (2) `(Y = 0, bp = (44 + j) mod 64)` with c_1 = W, c_2 = U_r:
  load B[0..3] (4 loads), update A2 at X = 1, 2 (2 XORs, 2 stores), and set
  `dout[0] = B[2] XOR (B[1] AND c_2)` (1 AND, 1 XOR), `dout[1] = NOT (c_2 AND
  B[3])` (1 AND, 1 NOT), `dout[2] = c_2`, `dout[3] = 0`, `dout[4] = NOT B[0]`.
- **Linear cancellation and deduplication in dC, dD and O2P**: With the 22
  folded `+c` terms, forming the distinct dC expressions (45 XORs), distinct dD
  expressions (67 XORs; columns `(1, (41+j) mod 64)` and `(3, (40+j) mod 64)`
  vanish identically), and distinct `dout XOR dD` expressions (161 XORs) updates
  the **1,081 non-zero O2P words** (1,081 loads, 1,081 XORs, 1,081 stores).
Total cost of Block (b) for every j = 0..31: 1,272 loads, 1,143 stores,
1,417 XOR, 84 AND, 39 NOT and 1 branch = **3,959 operations**.

**Lemma 7 (theta at the store, 26-register plane schedule, and full 64-register
cross-phase residency).** In ROUND_TS, plane b = 0 stores each row Y's outputs
without D'[x][0] and accumulates C0[0..4] row-by-row (at most 21 registers). In
planes b = 1..63, rows Y = 0..3 place B[0..4] and the complement scratch inside
unoccupied output registers `out[5Y+5..24]`, and row Y = 4 (where S = [1])
computes `out[24]` first, negates `B[1]` in place, and schedules the remaining 4
outputs in at most 26 registers; then `C[0]` is allocated (26 registers),
`Cprev[2] ^= C[0]` is added to column x = 1 and stored, freeing 5 registers
before `C[1..4]` are formed. In round 5 (storing only DIAG = (0, 6, 12, 18, 24)),
column parities C[0..4] are accumulated row-by-row in at most 33 active
registers (28 at plane 63). Because `fix[x]` registers become dead after plane
`max_{L=x} RHO[L]` (39, 41, 45, 56, 62 for x = 4, 0, 1, 3, 2; at plane 62,
`fix[2]` is consumed in row Y = 4 before row 4's 26-register peak), the program
passes in registers across all five phase boundaries (64-register schedule, with
the 56-register schedule in parentheses):
- **Block (b) -> R3**: Inlining planes b = 0..4 of R3 at the end of each leaf
  j = 0..31 (before jumping to shared R3 at b = 5) keeps **55 modified O2P
  words** in registers from the end of Block (b) into R3 (up to 24 in b = 3..4,
  up to 29 in b = 2..4, and the rest in b = 0..1; **47 words** for 56 regs),
  eliding 55 direct loads in R3 (-55 ops; -47 ops for 56 regs);
- **R3 -> R4**: **46 words** of ST0 (all 24 produced at planes 0..62 for R4
  plane 0, plus 22 of plane 63: 1 each for b = 0, 1, 2 and 19 for b >= 5),
  saving 46 stores in R3 and 46 loads in R4 (-92 ops; 30 words / -60 for 56);
- **R4 -> R5**: **49 words** of ST1 (all 24 produced at planes 0..62 for R5
  plane 0, plus all 25 of plane 63), saving 49 stores in R4 and 49 loads in R5
  (-98 ops; 41 words / -82 ops for 56 regs);
- **R5 -> LAST**: **41 diagonal words** of ST0 (36 from planes < 63 plus all 5
  of plane 63), saving 41 stores and 41 loads (-82 ops; 33 / -66 for 56 regs);
- **LAST -> PHASE2**: **52 row words** of ROWS (20 of g = 6 and all 32 of g = 7),
  saving 52 stores and 52 loads (-104 ops; 44 / -88 for 56 regs).

**Lemma 8 (lane-complement encoding).** Each stored lane L has a compile-time
polarity bit pi_L: the stored word is the true word XOR pi_L * (all-ones).
For one chi row with input polarities and wanted output polarities, NOT b AND
c equals s_b AND s_c when (pi_b, pi_c) = (1, 0), and NOT(s_b OR s_c) when
(0, 1) (the OR result then has polarity 1). For other combinations a
complemented copy of one input is formed (one NOT, shared within the row).
The output polarity is pi_a XOR (gate polarity) XOR (iota bit); if it differs
from the wanted one, one NOT is added. For each (row polarities, wanted
outputs, iota) the program uses the cheapest plan found by exhaustive search
over the 32 complemented-copy sets and both gate choices. Theta on encoded
words: the stored parity is the true parity XOR the parity of polarities, so
the theta'd next-round input has polarity fpol(pout)_L = pout_L XOR pc[x-1]
XOR pc[x+1], pc[x] = XOR_y pout_{x+5y}. The chosen patterns are P34 (output of
rounds 2, 3, 4; lanes 0,4,8,9,13,14,18,20 complemented) and P5 (output of
round 5; lanes 0,4,8,9,13,17,20), so rounds 3 and 4 and round 5 read
polarity Q3 = fpol(P34) and the last round reads fpol(P5). With them, every
chi row of rounds 3, 4 and 5 costs exactly 1 NOT (iota absorbed). In the last
round each plane's 4 digest outputs take whichever polarity costs no NOT; the
resulting fixed bits form KEYMASK (lane 0 complemented except bits 0 and 31;
lanes 1-3 plain; 62 bits set). All gates are exact; no data-dependent choice
is made. A2 is stored unencoded; the incremental updates of Lemma 6 are
differences and preserve the Q3 encoding of O2P.

**Lemma 9 (fused last round and transpose order).** Key row r = 64x + b
(x < 4) is digest-lane x, bit b. For block g = 0..7, the last round computes
the 32 rows with b = 8g + bl (bl < 8), x < 4, in registers (register index
8x + bl), applies the delta-swap stages d = 1, 2, 4 (row bits of bl) and
d = 64, 128 (row bits of x) inside the block, and stores the finished rows (with
52 rows passed directly in registers to Phase 2). Phase 2 then takes, for each
of the 32 pairs (x, bl), the 8 rows 64x + 8i + bl (i < 8), applies stages 8,
16, 32 and hands row 64x + 8i + bl straight to the table. By Lemma 5 all 8
stages are applied exactly once, so row r ends as the 256-bit key of slot r;
the offer order is q = 8(8x + bl) + i, i.e. slot decode_slot(q) of Section 2.

## 5. The algorithm and its counted program

### 5.1 Batch setup (once per batch of 2^40 messages)

1. Draw 512 random words (RAND); store each to PREF + 512*beta + 2p + w and to
   STATE0 + 256w + p. 2. Transpose both 256 x 256 matrices. 3. Store the 1088
   padding planes. 4. Compute the round-1 D words. 5. Run round 1 (plain
   encoding) and form A2 = STATE1 XOR D for all 1600 words. 6. For j = 0..31:
   complement P(0, j) and P(5, j), rerun round 1 (D words reused, Lemma 1),
   store the 8 basis words U_0..U_7 of COEF[j] = A2(e_j) XOR A2(0), restore.
7. Build O2P: round 2 from A2 with output polarity P34 and theta at the store
   (Lemma 7), then apply the plane-0 fix in memory. 8. s = 0.

Counted setup: < 484,000 operations per batch (< 676,000 with the extra charges
of Section 9). With batch-loop control (< 2^20 in all) this is < 2^-20 per
message.

### 5.2 Per z-step program (fully unrolled; worst path)

Persistent registers: s (the step counter t), n (the countdown message number,
initialised once per run to 2^256 - 1), ONE = 1 and M1 = 2^256 - 1 (all-ones W,
set once per run). Other registers are allocated per block (64 registers used;
or 56 in the 56-register variant). For t = 0 the step starts at (c) with b = 0.

    (a) control, t >= 1 (16): s = s + ONE ; 5-level branch tree on ctz(s):
        v = s AND ((2^sh - 1) << j0) ; c = (v == 0) ; branch   (sh = 16,8,4,2,1)
        32 duplicated leaves, no indirect jump; leaf j falls into block j.
    (b) incremental round 2, block j (3,959; Lemma 6): load 8 basis words
        U_0..U_7; per affected row, update A2, form dout using c = W on 17
        single-input rows, uncomplemented-product folding on 22 rows, and
        closed-form 2-input formulas; form deduplicated dC, dD (211 non-zero
        columns) and patch the 1,081 non-zero O2P words (holding 55 in regs
        across R3 planes 0..4 inlined at the end of leaf j); jump to R3 b = 5.
    (c) R3 = ROUND_TS(O2P, -,   ST0, all,  RC[2], Q3 -> P34)        9,794
        R4 = ROUND_TS(ST0, fix, ST1, all,  RC[3], Q3 -> P34)        9,825
        R5 = ROUND_TS(ST1, fix, ST0, DIAG, RC[4], Q3 -> P5)         7,290
    (d) LAST(ST0, fix): last round fused with stages 1,2,4,64,128   4,845
    (e) PHASE2: stages 8,16,32 and SPARSE(K) on each finished key   5,071
    (f) c = (s < 2^32 - 1) ; branch                                     2

Baseline ROUND_TS counts before cross-phase register residency are 9,895 (R3),
9,920 (R4), 7,380 (R5), 4,938 (LAST), and 2,563 + 256*10 = 5,123 (PHASE2 with
the 10-op countdown sparse set). Passing 55 O2P words across Block (b) -> R3
(-55 loads in R3), 46 words across R3 -> R4 (-46 stores in R3, -46 loads in R4),
49 words across R4 -> R5 (-49 stores in R4, -49 loads in R5), 41 words across
R5 -> LAST (-41 stores in R5, -41 loads in LAST), and 52 words across
LAST -> PHASE2 (-52 stores in LAST, -52 loads in PHASE2) yields 9,794, 9,825,
7,290, 4,845, and 5,071 (or 9,818, 9,849, 7,306, 4,861, 5,079 for 56 regs).

SPARSE(K), countdown Briggs-Torczon step on the top 140 key bits (S lives at
base address 0; n starts at 2^256 - 1 and decrements by 1 via `n = n + M1`;
DK[n] lives at address n >= 2^256 - 2^128 >> 2^140):

    a = K SHR 116 ; i = LOAD [a] ; c = (n < i) ; if !c goto INS
    k2 = LOAD [i] ; c = (k2 == K) ; if c goto MATCH
    INS: STORE [n] = K ; STORE [a] = n ; n = n + M1

Paths: S[a] <= n (never written in this run, or garbage <= n) 7; S[a] > n with
a different key 10 (the worst); match 7, then verification. No immediate occurs
apart from the shift amount.

**Ledger (one z-step, worst path: ctz(t) = 31, every message on the 10-op
path; counted by the simulator, Section 10.1).**

| block | ops (64 regs) | direct loads/stores | ops (56 regs) |
| --- | ---: | ---: | ---: |
| (a) control | 16 | 0 (+10 immediates) | 16 |
| (b) incremental round 2 + jump | 3,959 | 2,415 | 3,959 |
| round 3 | 9,794 | 3,099 | 9,818 |
| round 4 | 9,825 | 3,105 | 9,849 |
| round 5 | 7,290 | 1,830 | 7,306 |
| last round + stages 1,2,4,64,128 | 4,845 | 483 | 4,861 |
| stages 8,16,32 + 256 sparse steps | 5,071 | 204 | 5,079 |
| (f) loop test | 2 | 0 (+1 immediate) | 2 |
| **total per 256 messages** | **40,802** | **11,136 (+11)** | **40,890** |

By opcode (64-register schedule): 6,405 direct and 512 register loads, 4,731
direct and 512 register stores, 17,865 XOR, 3,865 AND, 2,304 OR, 999 NOT,
1,024 SHL, 1,280 SHR, 257 ADD, 518 CMP, 519 branch, 8 MOVI. Block (b) is 1,272
loads, 1,143 stores, 1,417 XOR, 84 AND, 39 NOT and 1 branch for every j = 0..31,
so the worst case equals the Gray average.

### 5.3 Countdown sparse set at base 0

S has 2^140 words at base address 0 (`0 .. 2^140 - 1`) and is never
initialised. The message counter n starts at `2^256 - 1` and is decremented by
1 (`n = n + M1` mod 2^256) after each processed message, so after k_ord
messages have been processed, the set of addresses written in DK is
`{n + 1, ..., 2^256 - 1}` (all >= `2^256 - 2^128`, disjoint from S, PREF and
scratch arrays). Because every 256-bit word `i = S[a]` automatically satisfies
`i <= 2^256 - 1`, the single unsigned comparison `n < i` holds iff `i` is in
`{n + 1, ..., 2^256 - 1}`, i.e. iff `i` is the address of a key written by an
earlier message of the current run. On every non-match `S[a]` is overwritten
with `n`. Garbage in S is therefore either `<= n` (insertion) or points to a
genuine earlier key (a full 256-bit comparison, then overwrite); it is never
trusted further.

### 5.4 Verification and halting

On the first MATCH (ids i = S[a] and n): recover `k_ord = (2^256 - 1) - id`,
decode each to `beta = k_ord >> 40`, `t = (k_ord >> 8) mod 2^32`,
`q = k_ord mod 256`, `p = decode_slot(q)`, `z = gray(t)` (under 20 operations
each), load the two prefix words of each (under 10), rebuild both messages
(under 20). If they are equal (only in event F3), halt with failure. Otherwise
evaluate both with two reference permutations (2 units), compare the 256 digest
bits and output the pair. This is under 2 units + 200 operations, capped at 3
units.

## 6. Correctness (unconditional)

- **Evaluator exactness.** Lemmas 2-3 make A2 and the 8-word basis of COEF[j]
  exact at every t; Lemma 6 keeps O2P equal to the encoded, theta'd round-2
  output of the current A2; Lemma 4 with Lemmas 7 and 8 makes rounds 3-5 exact
  in their encodings; the last round computes digest lanes 0..3 in the KEYMASK
  encoding; Lemma 9 makes the key of slot r equal K* XOR KEYMASK. Section 10
  checks this bit for bit.
- **Outputs.** Any output pair is two distinct messages whose full digests
  were equal under two reference permutations: a full collision.

## 7. Success probability

The run halts at the first MATCH. The failure events are:

- **F3**: two groups produce the same message. This needs P_g XOR P_g' to be
  one of the 2^32 values ins(z) XOR ins(z'); Pr[F3] < 2^191 * 2^32 / 2^512 =
  2^-289. Without F3 all N messages are distinct.
- **F1**: no two of the N messages have equal digests.
- **F2**: for some colliding pair (a, b), a processed before b, some message c
  processed after a and before b has the same top 140 key bits as a and a
  different key (so S[a] no longer points to a or to a copy of key(a)).

If none of F1, F2, F3 occurs, take a colliding pair (a, b). When a is
processed it either matches (success) or sets S[h] = n_a. Any later c with
the same top bits either has key(a) and matches, or (excluded by not-F2) does
not exist before b. So at b's lookup S[h] holds n_a or the number of a message
with key(a), which is > n_b, and DK at that address equals key(b): MATCH no
later than b. So Pr[fail] <= Pr[F1] + Pr[F2] + Pr[F3].

**Heuristic H1 (declared; identical text in claim.json).** For the failure
events F1 and F2 (Section 7), the 2^128 keys of the grouped message set
{m(g, z)} (independent uniform prefixes P_g, all z in {0,1}^32, processed in
any fixed order chosen independently of the digests, in particular the order
of Section 2: batch by batch, t = 0..2^32-1 with z = gray(t), slots
p = decode_slot(q) = 64*floor(q/64) + 8*(q mod 8) + (floor(q/8) mod 8) for
q = 0..255) behave like N independent uniform 256-bit values, i.e.
Pr[F1] <= exp(-N(N-1)/2^257) and Pr[F2] <= N^3/6 * 2^-396.

Under H1:

- Pr[F1] <= exp(-N(N-1)/2^257) = exp(-(1 - 2^-128)/2) < 0.6065307.
- Pr[F2] <= (number of ordered triples a < c < b) * 2^-140 * 2^-256
  <= N^3/6 * 2^-396 < 2^-14.5. We use 2^-13 < 0.0001221.
- Success >= 1 - 0.6065307 - 0.0001221 - 2^-289 > 0.39334. We claim 0.39,
  which leaves an allowance of 0.0033.

The keys stored are the digests XOR a fixed constant, so H1 for keys and for
digests is the same statement.

**Rigorous partial support.** For groups g != g' and any z, z', the messages
m(g, z) and m(g', z') are independent and each is uniform on 64-byte strings,
so by Cauchy-Schwarz Pr[digests equal] >= 2^-256. Within-group pairs are a
2^-96 fraction of all pairs, so the expected number of colliding pairs is at
least (1 - 2^-96) * N(N-1)/2^257, close to 1/2 as in the uniform model. H1 is
needed only for the second-moment behaviour behind Pr[F1], and for F2. This
is jaazinn's argument.

**Bitslicing, batching and encodings do not change the message set.** They fix
only the processing order, a function of (beta, t, q), never of digests;
bitslicing, the incremental round 2 and the encodings change how a digest is
computed, not its value (Section 6).

## 8. Time bound

Per message, the charge is 40,802/256 = 159.3828125 plus amortised setup
(< 2^-20), at most 159.39 operations or 159.39/1626 units. It covers the Gray
and incremental round-2 updates, rounds 3-6, both transpose phases, every
table load, store, compare and branch, and all loop control. The only other
cost is verification (< 3 units, at most once). So

    T <= 2^128 * 159.39/1626 + 3 = 0.0980258... * 2^128 + 3 < 2^124.64931.

The claimed time_log2 is **124.650**, rounded up (or **124.653** for the
56-register variant at 40,890 ops/z-step, 159.73 ops/msg). The bound is
worst-case for every run, with no restarts; preprocessing_log2 = 0.

## 9. Sensitivity of the bound to conventions

| reading (same program, worst z-step) | ops/z-step | ops/message | time_log2 |
| --- | ---: | ---: | ---: |
| every executed primitive once (64 regs, claimed) | 40,802 | 159.39 | 124.650 |
| + one address addition per direct load/store, + one MOVI per ALU immediate | 51,949 | 202.93 | 124.998 |
| as above, + one op per shift amount | 54,253 | 211.93 | 125.061 |
| 56-register variant under row 1 / row 2 / row 3 | 40,890 | 159.73 | 124.653 |
| logic gates only (reference; would need > 64 registers) | 25,039 | 97.81 | 123.945 |

For comparison, winglock (6a250bf) reports 41,679 / 53,330 / 55,634 per z-step
(124.680 / 125.036 / 125.097) under the first three rows, and mitchuski
(02d6a703) reports 126.42 for its circuit with every core load and store
charged (and 126.64 for a narrow 64-register file with +1 per direct access).
Notice that even under row 2 (+1 per direct access and ALU immediate), our
64-register schedule stays strictly below 125.00 (**124.998**).

## 10. Evidence

### 10.1 Counted verification and simulator checks (participant evidence)

The program of Section 5 was verified against the counted 256-bit word-RAM
model with an explicit 64-register file (and 56-register cap check), a counter
per primitive, and separate counts for direct and register addresses, immediates
and shift amounts:

- Across all 32 Gray blocks j = 0..31 on random 256-group batches, every
  COEF[j] column has exactly 20 all-ones words (W) and 42 words in an 8-word
  basis U_0..U_7; the closed-form 1-input, uncomplemented-product 22-row, and
  2-input dout equations and the 1,081-word O2P patch match a full round-2
  rebuild bit-for-bit with 0 mismatches.
- All 32 Gray blocks j = 0..31 execute the exact same instruction mix: 3,959
  operations in Block (b) and 40,802 operations for the full z-step on the
  worst path (64 registers; 40,890 on 56 registers).
- Together with the 16,384-message, 17,024-key, 18,432-key, and 20,480-key
  full-width verification runs against `verifier/keccak.py:sha3_256(m, 6)`
  inherited from 6a250bf (0 mismatches across all runs), the evaluator is
  bit-identical to the reference 6-round sponge.

### 10.2 Declared experiments (organizer-executed, `python-message-pairs-v1`)

All four experiments use `experiments/s3r6_bitslice_birthday.py`. It mirrors
the counted program: per-batch A2, COEF (with 20 W words and 8 basis words
verified per column) and O2P; the Gray update of A2 with the closed-form
incremental round-2 patch of the 1,081 active words of O2P (Lemma 6);
lane-complement rounds 3-5 with theta at the store and the plane-0 fix
(Lemmas 7-8); the row-0 last round in the KEYMASK encoding; the transpose in
stage order 1, 2, 4, 64, 128, 8, 16, 32; keys offered in processing order
decode_slot(q). Every digest used for matching comes from that evaluator; equal
masked keys are equal masked digests. Each organizer seed derives fresh 64-byte
group prefixes with SHA-256. N_t = 2^9 messages and an 18-bit mask give
N_t^2/2^18 = 1 = N^2/2^256; the uniform-model success probability is 0.39307
(0.4990 expected masked pairs per trial; for 256 trials, 100.6 successes, sd
7.8). Trials sharing a batch own disjoint bit positions, and no operation mixes
positions. Every trial checks at full width, against an independent direct
sponge (own rho offsets and round constants), its first 4 keys and its first
key at each step t = 2^i (one step of every Gray block used); checks the
62-word support and 8-word basis of each coefficient column; checks the exact
3,959-op / 40,802-op schedule and cancellation of the two dD columns; and after
the batch's last step compares the incrementally maintained O2P word for word
with O2P rebuilt from A2. Any failure aborts.

Layouts: `k6r6-bs-full-width` 256 groups x 2; `k6r6-bs-spread` 16 x 32;
`k6r6-bs-single-group` 1 x 512 (strongest within-group structure);
`k6r6-bs-high-z` 4 x 128 with z = gray(t) << 25 (z bits 25..31; for j >= 27
the support wraps around the lane). All use z = gray(t).

### 10.3 Local runs (our seeds; not organizer evidence; all runs reported)

Because the evaluator computes the exact same keys in the exact same processing
order as 6a250bf, all trial outputs and collision counts are byte-for-byte
identical. Organizer-runner replay (`experiments/runner.py`, seed
`hashsmash-public-seed-v1`, 256 trials): every returned pair re-checked with
`verifier`; no self-check failed (1,280 / 2,304 / 2,816 / 2,816 full-width key
checks and 256 O2P rebuild checks per experiment).

| experiment | successes / 256 | z (model 100.6, sd 7.8) | masked pairs (exp. 127.8) |
| --- | ---: | ---: | ---: |
| k6r6-bs-full-width | 100 | -0.1 | 123 |
| k6r6-bs-spread | 109 | +1.1 | 150 |
| k6r6-bs-single-group | 107 | +0.8 | 144 |
| k6r6-bs-high-z | 111 | +1.3 | 138 |

Larger runs of the same evaluator (`--local`, 8,192 trials per layout and
batch, local seeds "bs2-a" and "bs2-b"). The model is 3220.0 +- 44.2 per batch
and 6440.1 +- 62.5 pooled:

| layout | batch a | batch b | pooled | pooled z | pairs (exp. 8176) |
| --- | ---: | ---: | ---: | ---: | ---: |
| full-width | 3243 (+0.5) | 3253 (+0.7) | 6496 | +0.9 | 8148 |
| spread | 3248 (+0.6) | 3270 (+1.1) | 6518 | +1.2 | 8271 |
| single-group | 3318 (+2.2) | 3205 (-0.3) | 6523 | +1.3 | 8278 |
| high-z | 3197 (-0.5) | 3174 (-1.0) | 6371 | -1.1 | 8099 |

Before these, one 256-trial timing run per layout (local seed "timing") gave
108, 99, 103 and 99 successes (full-width, spread, single-group, high-z; z
+1.0, -0.2, +0.3, -0.2). Ten further 256-trial replays on fresh seeds gave
totals 1,004 / 980 / 994 / 958 of 2,560 (z -0.1 / -1.1 / -0.5 / -2.0; lowest
cell 75 of 256 at -3.3 sd, spread layout, seed rv-coin-f). Pooled over all
runs (19,456 trials per layout) the z-scores are +0.9 (full-width), +0.9
(spread), +1.2 (single-group) and -1.6 (high-z).

## 11. Memory

| array | 32-byte words | bytes |
| --- | --- | --- |
| S (at base address 0) | 2^140 | 2^145 |
| DK (key of message n at address n >= 2^256 - 2^128) | <= 2^128 | <= 2^133 |
| PREF (at 2^170) | 2^97 | 2^102 |
| A2, O2P, two state buffers, ROWS, COEF, setup arrays (at 2^240) | < 2^14 | < 2^19 |
| code (unrolled z-step, 32 incremental blocks, setup) | < 2^20 instructions | < 2^25 |

Total < 2^145.01 bytes; we claim 146. Memory is reported only.

## 12. Limitations

- H1 is a heuristic. It extends the grouped structure (A2 affine in z within a
  group; shared prefix pairs across groups) from the tested scale
  (N_t = 2^9, 18-bit masks) to N = 2^128 and the full 256-bit key. The
  experiments use a full dictionary of masked keys; the top-140-bit loss F2
  cannot be scaled down faithfully and is bounded only under H1. Organizer
  seeds are public. A 256-trial experiment resolves the success frequency
  only to about +-0.03, and the 0.0033 allowance is not statistically
  certified.
- Within a group the digest has algebraic degree at most 2^5 = 32 in z
  (five chi layers, rounds 2-6, after the affine A2). z has 32 bits, so
  this bound gives no zero-sum over any affine subspace of z (a guaranteed
  zero-sum needs dimension at least 33). This concerns only within-group
  pairs (a 2^-96 fraction of pairs).
- The gain comes from operation-level pricing: bitslicing amortises each word
  operation over 256 messages; grouping and Lemma 6 remove round 1 and most
  of round 2; lane complementing removes most NOTs; cross-phase register
  residency and the countdown sparse set remove redundant scratch and address
  arithmetic. All executed work, including all memory traffic, is charged once.
  The 64-register machine is an assumption (both 64- and 56-register schedules
  are given). Section 9 gives the bound under stricter readings.
- No sub-birthday attack, collision certificate or full-scale run is claimed.

## 13. Credit

**jaazinn** (0a5b7ae8), **may93182** (11c46f4d), and **winglock** (6a250bf),
co-authors in the sense of Section 0; **tekkac** (b001199a; lane complementing
in this track, after the Keccak team); **ercumentyildirim** (c7fa1a56,
4c969300; last-round early abort); **zeeshan8281** (cbf7998d) / **tekkac**
(f58275ef) for exact charging; **mitchuski** (02d6a703; the counting reading),
as in Section 0. Errors are ours.
