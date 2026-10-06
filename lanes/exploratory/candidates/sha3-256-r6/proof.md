# sha3-256-r6: bitsliced grouped birthday search, 140-bit candidate key, time_log2 = 124.491

## 0. Summary and credit

A generic birthday search over full 256-bit digests; no cryptanalytic
weakness of SHA3 is claimed. This revises our package bfc8c418 (124.680):
the evaluator, the message set and the table are the same, but the last
round now computes only 140 of the 256 digest bits, and a key match is
verified with two full permutations before the run halts.

Reused (credit below): grouping with A2 exactly affine in the 32-bit group
counter z (jaazinn's framework; Lemma 2), so round 1 and the linear part of
round 2 are paid once per group; may93182's 256-message bit-plane Keccak
(rotations are address renamings) and delta-swap transpose; the
lane-complement chi of the Keccak team as brought to this track by tekkac
(at most one NOT per chi row in rounds 3-5, none in the last round); and
ercumentyildirim's last-round early abort (only digest row 0 is computed).
Ours from bfc8c418: the incremental round 2 (Lemma 6), theta at the store
(Lemma 7), the last round fused with transpose stages, and a sparse set whose
stored index is the message number.

New here (ours, extending the early abort from lanes to bit planes): the
last round computes digest lanes 0..3 on only **35 fixed bit planes** (140
digest bits), and rounds 5 and 4 compute and store only what those planes
read (Lemma 10). The other 116 key rows are constant zero and the transpose
skips them (Lemma 9). The key is a fixed bit permutation of the 140 kept
bits and equals the 140-bit table index, so a key match is only a
**candidate**: both messages are rebuilt from their ids and evaluated in full
(2 units). The run halts only on equal 256-bit digests of distinct messages;
otherwise it **counts the event and continues**, aborting at a hard cap
VCAP = 2^115 + 2^91 so that the time bound holds in every run.

| quantity | value |
| --- | --- |
| messages N | 2^128 = 2^88 batches x 256 groups x 2^32 values of z |
| ops per z-step (256 messages), worst path | 36,449 (every executed primitive) |
| ops per message charged | 142.3789 (36,449/256) + setup < 2^-20 |
| candidate verifications | at most VCAP = 2^115 + 2^91, each 2 units + 47 ops |
| total T | <= 2^128 * 142.37890625/1626 + VCAP*(2 + 47/1626) + 3 < 2^124.49056 |
| claimed time_log2 | **124.491** |
| success probability | >= 0.39334 under H1; claimed 0.39 |
| memory | < 2^145.01 bytes; claimed 146 |

**Credit.** **jaazinn** (Yukon ticket 0a5b7ae8, blake3-r2, in review)
originated grouped partial evaluation, the Briggs-Torczon sparse set on the top
140 key bits, the failure analysis with heuristic H1 and the scaled-experiment
design; **may93182** (11c46f4d, in review) introduced for this track the
256-way bit-plane Keccak and the delta-swap transpose at 6 operations per row
pair. Both are named as co-authors in that sense. **tekkac** (b001199a)
brought the Keccak team's lane-complement chi with round constants folded
into polarity to this track (our polarity patterns come from our own
search). The last-round early abort is **ercumentyildirim**'s (c7fa1a56;
sha3-256-r5: 4c969300); the kept planes with verify and continue extend it.
Exact per-message charging follows zeeshan8281 (cbf7998d) and tekkac
(f58275ef). The reading of Section 1 matches the every-core-load-and-store-
charged row of **mitchuski**'s table (02d6a703). None of them has reviewed
this package. Ours: Lemmas 1-3 (column pairing, affine reduction), 6, 7, 9
and 10, the table with verify and continue, and the counted program. This
package does not use the changes in Th0rgal's 76ccfa1c (which builds on
bfc8c418). Errors are ours.

## 1. Target, machine and charging conventions

- Target `sha3-256-r6-prefix-v1`: the complete SHA3-256 sponge (rate 1088,
  capacity 512, suffix 0x06, pad10*1, zero IV), Keccak rounds 0..5 (RC[0..5])
  and all 256 output bits, as in `verifier/keccak.py:sha3_256(msg, 6)`.
  Messages are exactly 64 bytes (one block). Lane k (k < 8) is bytes
  8k..8k+7 read little-endian; lane 8 = 0x06, lane 16 = 0x80 << 56, the other
  lanes are 0. Lane index L = x + 5y. Rounds are numbered 1..6 below.
- Digest = lanes 0..3 after round 6, little-endian; K* = int.from_bytes(digest,
  "little"). The program stores the **key** K = key_of_digest(K*): digest bit
  (x, b) (lane x < 4, plane b in KEEP, Lemma 9) is moved to key bit
  ROWOF(x, b) in 116..255, the result is XORed with a fixed public constant
  KEYMASK, and key bits 0..115 are 0. K is a fixed function of 140 digest
  bits. Equal digests give equal keys, but **equal keys are only a candidate**.
  The table index is h = K >> 116, which is all 140 key bits.
- Cost model `collision-frontier-v5`, C = 1626: one permutation costs 1 unit
  and any other 256-bit word primitive 1/1626. Machine: a 256-bit word RAM
  with 64 registers (our stated assumption; v5 specifies only the word
  RAM; the program uses at most 56). An operation on register operands is
  one primitive, not a memory access; 64 registers of 256 bits are 2 KiB, a
  32-entry 512-bit SIMD register file. We do not claim the bound under a
  memory-to-memory reading (every ALU operand loaded, every result stored).
- **Charging (the reading we claim).** Every executed primitive of the v5
  list costs 1: every load and store (direct or register-addressed), XOR, AND,
  OR, NOT, shift, add, compare, conditional branch, immediate move and random
  word. A constant address or an immediate operand is a field of the
  instruction that executes, not a separate executed operation. Register
  reads and writes are part of the instruction. No indirect jump is used and
  no rotation is ever executed (Lemma 4). A candidate verification evaluates
  two messages with the reference six-round function, 1 unit each. Section 9
  also prices one extra address addition per direct access, one MOVI per ALU
  immediate and each shift amount; every such variant stays below 124.91.

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

    p = decode_slot(q) = 32*(q mod 8) + floor(q/8).

Batches run in order beta = 0, 1, .... Message (beta, t, q) gets the
**message number** n = beta*2^40 + t*2^8 + q, which is also the count of
messages processed before it. Every message is evaluated exactly once, and
N = 2^128.

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

**Lemma 3 (62-word support).** Let j' = (j + 36) mod 64. The round-1 output
varies only in bit j of lanes 0, 3, 4 and in bit j' of lanes 15, 16, 19. The
changed column parities are C[0] at j and j', C[3] at j, C[4] at j and j', and
C[1] at j'. Since C[c][b] enters D[c+1][b] and D[c-1][b+1], the D words that
can change are (x, b) = (1,j), (4,j+1), (1,j'), (4,j'+1), (4,j), (2,j+1),
(0,j), (3,j+1), (0,j'), (3,j'+1), (2,j'), (0,j'+1) (bits mod 64): 12 pairs,
60 words P(x+5y, b). The directly varying (3,j) and (19,j') make 62. So L_j
vanishes outside the fixed list SUPPORT_j of 62 words, and Gray order gives
A2(gray(t)) = A2(gray(t-1)) XOR L_{ctz(t)}.

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
`t = a SHR d; t = t XOR b; t = t AND M_d; u = t SHL d; a = a XOR u; b = b XOR t`
(6 operations) and exchanges entries (i, c+d) and (i+d, c) for c AND d = 0.
Stage d applies it to all 128 such row pairs and swaps bit log2(d) of the row
index with the same bit of the column index. The 8 stages act on different
index bits, so they commute, and all 8 in any order transpose the matrix.

**Lemma 6 (incremental round 2).** Let O2P be the round-2 output (chi, iota)
with the round-3 theta applied, stored in the lane-complement encoding Q3 of
Lemma 8. When A2 changes by L_j on SUPPORT_j, rho/pi sends the 62 words to 60
distinct chi rows (58 rows with one changed input, 2 rows with two; the map
(L, b) -> (X, Y, plane) is a bijection, fixed by j). For a row with one
changed input a[X] -> a[X] XOR c, the exact output difference is
dout[X] = c, dout[X-1] = c AND a[X+1], dout[X-2] = (NOT a[X-1]) AND c (indices
mod 5; a[X+1], a[X-1] are unchanged). For a row with two changed inputs the
program loads all 5 old inputs, forms the new ones and computes
dout[k] = (n[k] XOR o[k]) XOR (NOT n[k+1] AND n[k+2]) XOR (NOT o[k+1] AND o[k+2])
for the affected k. Then dC[x][b] = XOR_Y dout(x, Y, b) and
dD[x][b] = dC[x-1][b] XOR dC[x+1][b-1], and O2P(x+5Y, b) ^= dout(x, Y, b) XOR
dD[x][b]. Theta is linear and the encoding is XOR with a constant, so the
patched O2P equals the encoded theta'd round-2 output of the new A2 exactly.
Terms that are structurally zero for this j emit no code. The cost is the
same for every j: 4,149 operations.

**Lemma 7 (theta at the store).** In a round, plane b's 25 chi outputs are
held in registers, so the column parities C'[x][b] of the output are complete
before any store, and D'[x][b] = C'[x-1][b] XOR C'[x+1][b-1] is available for
b >= 1 from the previous plane's parities (kept in 5 registers). Each output
word of plane b >= 1 is stored with D'[x][b] already added. Plane 0 is stored
without it; after plane 63, fix[x] = D'[x][0] = C'[x-1][0] XOR C'[x+1][63]
stays in 5 registers, and the next round XORs fix[x] into each loaded word
whose source plane is 0 (25 words, one per lane). The stored state plus the
fix is exactly the theta'd state, so the next round needs no theta pass.

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
round each plane's 4 digest outputs take whichever polarity costs no NOT
(lane 0 complemented except bits 0 and 31; lanes 1-3 plain); moved to key
rows by Lemma 9, these fixed bits form KEYMASK (33 of the 140 kept bits set).
Rounds 4-5 compute only the rows of Lemma 10, each still with at most one
NOT. All gates are exact; no data-dependent choice
is made. A2 is stored unencoded; the incremental updates of Lemma 6 are
differences and preserve the Q3 encoding of O2P.


**Lemma 9 (kept planes, key rows and the transpose with zero rows).** Fix

    KEEP = (0, 1, 2, 3, 4, 9, 10, 11, 16, 17, 18, 22, 23, 24, 25, 29, 30, 31,
            32, 37, 38, 39, 40, 44, 45, 46, 47, 51, 52, 53, 54, 58, 59, 60, 61)

(35 planes, chosen once by a search over the exact counted cost; a fixed
public constant). Plane KEEP[k] gets slot s = 29 + k, and digest bit (x, b),
x < 4, becomes key row ROWOF(x, b) = 4s + x, so rows 116..255 hold the 140
kept digest bits and rows 0..115 are constant zero. Block g holds rows
32g..32g+31 (slots 8g..8g+7); blocks 0-2 are empty, block 3 holds slots 29-31
only, blocks 4-7 are full. For each nonempty block the last round computes
its kept planes' 4 outputs into registers 4*bl + x and applies stages d = 1,
2 (row bits of x) and 4, 8, 16 (row bits of bl) in registers, then stores the
32 rows. A delta swap of rows a, b (Lemma 5) where a row is statically known
to be zero is cheaper and exact: if a = 0, `t = b AND M_d; a = t SHL d;
b = b XOR t` (3 ops); if b = 0, `t = a SHR d; b = t AND M_d; u = b SHL d;
a = a XOR u` (4 ops); if both are zero, nothing (a swap leaves both zero).
These are the 6-op formulas with the zero operand substituted. After a swap
both rows are treated as nonzero; the zero pattern is compile-time. Phase 2,
for each gi = 0..31, takes the 8 rows 32i + gi (i < 8). It loads only rows
i >= 3 (rows of the empty blocks are zero), applies stages 32, 64, 128 with
the same zero tracking (57 instead of 72 ops), and hands row 32i + gi to the
table in order q = 8gi + i. By Lemma 5 every stage is applied exactly once,
so row 32i + gi is the key of slot 32i + gi = decode_slot(q).

**Lemma 10 (dependency cone of rounds 5 and 4).** Call a word *needed* if a
later computation reads it. The last round, on plane b, reads the 5 diagonal
lanes L at source plane (b - RHO[L]) mod 64, so round 5 must store only these
175 words, with the plane-0 fix of columns {x : RHO[DIAG[x]] in KEEP} =
{0, 1}. For a round with theta at the store (Lemma 7) and a set of needed
stored words and needed fix columns:

- a stored word (L, b) with b >= 1 needs its chi output and the parities
  C[x-1][b] and C[x+1][b-1];
- a needed fix column x needs C[x-1][0] and C[x+1][63];
- a parity C[x][b] needs the 5 chi outputs of its column;
- a chi output (X, Y, b) needs the 3 row inputs X, X+1, X+2, read through
  rho/pi from the round's input, plus the input's fix wherever the source
  plane is 0.

The round emits exactly these chi outputs, parities, theta XORs and stores,
using the gate plan of Lemma 8 restricted to the needed outputs of each row.
Its needed inputs are the needed stored words of the previous round. From
the 175 words the program finds round 5 (1,161 chi outputs, 229 parities)
reading 1,363 words, which is round 4's store set. Round 4 needs every chi
output (all 320 parities) and reads all 1,600 words, so round 3 and the
incremental round 2 are unchanged. Every word that is computed has exactly
its bfc8c418 value: it is given by the same formula from the same inputs,
and no omitted word is ever read. With every word declared needed, the
generator emits the bfc8c418 rounds exactly (9,895 / 9,920 / 7,380
operations; checked).

## 5. The algorithm and its counted program

### 5.1 Batch setup (once per batch of 2^40 messages)

As in bfc8c418: draw 512 random words (RAND), store them to PREF + 512*beta
+ 2p + w and STATE0 + 256w + p; transpose; store the padding planes; round-1
D words; round 1 and A2 = STATE1 XOR D; for j = 0..31 the coefficient words
COEF[j][k] = A2(e_j) XOR A2(0) on SUPPORT_j (round 1 rerun, D reused, Lemma
1); O2P = round 2 from A2 with output polarity P34, theta at the store and the
plane-0 fix (Lemma 7); s = 0.

Counted setup: 483,643 operations per batch (675,265 with the extra charges
of Section 9). With batch-loop control (< 2^20 in all) this is < 2^-20 per
message. Once per run: CNT = 0 (the candidate counter, one word).

### 5.2 Per z-step program (fully unrolled; worst path)

Persistent registers: s (the step counter t), n (the message number), SB =
SBASE and ONE = 1 (set once per run). Other registers are allocated per block
(at most 56 live in all). For t = 0 the step starts at (c).

    (a) control, t >= 1 (16): s = s + ONE ; 5-level branch tree on ctz(s):
        v = s AND ((2^sh - 1) << j0) ; c = (v == 0) ; branch   (sh = 16,8,4,2,1)
        32 duplicated leaves, no indirect jump; leaf j falls into block j.
    (b) incremental round 2, block j (4,149; Lemma 6), then jump to (c).
    (c) R3 = ROUND_TS(O2P, -,   ST0, all 1,600 words,  RC[2], Q3 -> P34)  9,895
        R4 = ROUND_TS(ST0, fix, ST1, cone: 1,363 words, RC[3], Q3 -> P34)  9,451
        R5 = ROUND_TS(ST1, fix, ST0, cone: 175 words,   RC[4], Q3 -> P5)   5,387
    (d) LAST(ST0, fix): 35 kept planes, stages 1,2,4,8,16 (Lemma 9)       2,746
    (e) PHASE2: stages 32,64,128 and SPARSE(K) on each finished key       4,803
    (f) c = (s < 2^32 - 1) ; branch                                           2

ROUND_TS is the bfc8c418 round (registers out[0..24], B[0..4], one
complement scratch, t, two 5-word parity buffers, C0[0..4]) restricted to the
cone of Lemma 10. Per plane b and row Y with a needed output, it loads the
needed inputs B[X] = [src + 64L + (b - RHO[L]) mod 64] (XOR fix[x] on source
plane 0) and computes the needed chi outputs. It then forms the needed
parities, and for each needed stored word adds D = C[x-1] ^ Cprev[x+1] (b > 0;
one XOR per column, shared) and stores it. At the end it returns
fix'[x] = C0[x-1] ^ C63[x+1] for the needed columns.

Counted per block (simulator, Section 10.1): round 4 has 1,600 loads, 1,363
stores, 4,568 XOR, 896 AND, 704 OR, 320 NOT; round 5 has 1,363 loads, 175
stores, 2,445 XOR, 597 AND, 564 OR, 243 NOT. The XOR counts decompose as
R4 = 1,600 chi + 1,280 parity + 1,343 store-theta (the 20 needed stores on
plane 0 get none) + 315 D + 25 load-fix + 5 fix-out = 4,568 and R5 = 1,161
chi + 916 parity + 173 store-theta (2 needed stores on plane 0) + 173 D +
20 load-fix + 2 fix-out = 2,445; R5 has 290 rows with a needed output, 243
of which need a NOT. LAST has 5 MOVI (masks), 175
loads (5 diagonal words per kept plane; 2 fix XORs, for (lane 0, b = 0) and
(lane 6, b = 44)), and 160 stores (5 blocks of 32 rows). Its 2,746
operations include 1,194 XOR, 434 AND, 70 OR, 364 SHL and 344 SHR. Block 3's
stages cost 204 instead of 480. PHASE2 has 3 MOVI, 32 x (5 loads + 57 swap
operations) and 256 SPARSE steps of at most 11 operations: 4,803.

SPARSE(K), Briggs-Torczon step on the 140-bit key (n is the number of the
current message, DK[n] lives at address n):

    h = K SHR 116 ; a = h + SB ; i = LOAD [a] ; c = (i < n) ; if !c goto INS
    k2 = LOAD [i] ; c = (k2 == K) ; if !c goto INS
    CAND (Section 5.4; laid out inline here, falls through to INS)
    INS: STORE [n] = K ; STORE [a] = n ; n = n + ONE

Paths: S[h] >= n (never written, or garbage) 8; S[h] < n with a different
key 11 (the worst); equal key: CAND, then either halt or fall through to
INS. No path has an uncounted jump.

**Ledger (one z-step, worst path: ctz(t) = 31, every message on the 11-op
path; counted by the simulator, Section 10.1).**

| block | bfc8c418 | ops | loads | stores |
| --- | ---: | ---: | ---: | ---: |
| (a) control | 16 | 16 | 0 | 0 |
| (b) incremental round 2 + jump | 4,149 | 4,149 | 1,336 | 1,152 |
| round 3 | 9,895 | 9,895 | 1,600 | 1,600 |
| round 4 (cone) | 9,920 | 9,451 | 1,600 | 1,363 |
| round 5 (cone) | 7,380 | 5,387 | 1,363 | 175 |
| last round, 35 planes + stages 1,2,4,8,16 | 4,938 | 2,746 | 175 | 160 |
| stages 32,64,128 + 256 sparse steps | 5,379 | 4,803 | 160 + 512 | 512 |
| (f) loop test | 2 | 2 | 0 | 0 |
| **total per 256 messages** | **41,679** | **36,449** | **6,746** | **4,962** |

By opcode: 6,234 direct and 512 register loads, 4,450 direct and 512 register
stores, 15,296 XOR, 3,314 AND, 2,042 OR, 959 NOT, 716 SHL, 856 SHR, 513 ADD,
518 CMP, 519 branch, 8 MOVI. Block (b) costs the same for every j = 0..31,
so the worst case equals the Gray average.

### 5.3 Sparse set

S has 2^140 words at SBASE = 2^200 and is never initialised; DK[n] = K is
written at address n for every processed message, so every address below
the current n holds a key of an earlier message, written once and never
changed. A lookup is valid iff S[h] < n; then DK[S[h]] is the key of an
earlier message, and CAND requires equality of all 256 key bits (the 140
kept bits; the rest are 0). After INS, S[h] = n. Garbage in S is therefore
either >= n (insertion) or points to a genuine earlier key (a comparison,
then CAND or overwrite); it is never trusted further.

### 5.4 Candidates: verify and continue, halting, cap

On CAND (ids i = S[h] and n, equal 140-bit keys) the program decodes each id
to beta = id >> 40, t = (id >> 8) mod 2^32, q = id mod 256,
p = decode_slot(q), z = gray(t). It loads the two prefix words at
PREF + 2(256*beta + p) and XORs LE32(z) into bits 0..31 of the first and
bits 64..95 of the second: 20 operations per message. It evaluates both
messages with the reference six-round function (2 units) and compares the
256-bit digests. If the digests are equal and the messages differ, it
**outputs the pair and halts**. Otherwise (different digests, or the same
message, possible only in F3) it loads CNT, adds 1, stores it, and aborts
the run with failure if CNT >= VCAP. Then it falls through to INS, so
S[h] = n as on an ordinary overwrite. A
continued candidate costs 47 operations more than the 11-op path, plus
2 units; the halting path costs at most 54 operations plus 2 units. Here

    VCAP = 2^115 + 2^91   (an instruction immediate).

## 6. Correctness (unconditional)

- **Evaluator exactness.** Lemmas 2-3 make A2 exact at every t; Lemma 6 keeps
  O2P equal to the encoded, theta'd round-2 output of the current A2; Lemma 4
  with Lemmas 7, 8 and 10 makes every needed word of rounds 3-5 exact in its
  encoding; Lemma 9 makes the key of slot p equal key_of_digest(K*) of message
  p. Section 10 checks this bit for bit.
- **Outputs.** The run outputs only two distinct messages whose full
  256-bit digests were equal under two reference evaluations: a full
  collision. A key match alone never produces output.

## 7. Success probability

The run halts at the first verified collision. The failure events are:

- **F3**: two groups produce the same message. This needs P_g XOR P_g' to be
  one of the 2^32 values ins(z) XOR ins(z'); Pr[F3] < 2^191 * 2^32 / 2^512 =
  2^-289. Without F3 all N messages are distinct.
- **F1**: no two of the N messages have equal digests.
- **F2**: for some colliding pair (a, b), a processed before b, some message c
  processed after a and before b has the same 140-bit key as a and a
  different digest.
- **F4**: the number of continued candidates reaches VCAP (abort).

If none of F1-F4 occurs, take a colliding pair (a, b). When a is processed it
either halts the run with a collision (success) or sets S[h] = n_a. Let c be
any later message before b with the same key. By not-F2, c has a's digest.
The entry S[h] at that point holds n_a, or the number of an earlier message
with a's key and hence (not-F2) a's digest. So c's CAND finds equal digests
of distinct messages (not-F3), and the run succeeds. Otherwise, at b's
lookup S[h] holds such a number, which is < n_b, DK there equals key(b), and
CAND finds the collision no later than b. Without F4 the run is not aborted
before then. So Pr[fail] <= Pr[F1] + Pr[F2] + Pr[F3] + Pr[F4].

**Heuristic H1 (declared; identical text in claim.json).** For the failure
events F1, F2 and F4 (Section 7), the 2^128 digests of the grouped message
set {m(g, z)} (independent uniform prefixes P_g, all z in {0,1}^32,
processed in any fixed order chosen independently of the digests, in
particular the order of Section 2: batch by batch, t = 0..2^32-1 with
z = gray(t), slots p = decode_slot(q) = 32*(q mod 8) + floor(q/8) for
q = 0..255) behave like N independent uniform 256-bit values, i.e.
Pr[F1] <= exp(-N(N-1)/2^257), Pr[F2] <= N^3/6 * 2^-396 and, since the 140-bit
key is a fixed function of 140 digest bits, Pr[F4] <= 2^-67.

Under H1:

- Pr[F1] <= exp(-N(N-1)/2^257) = exp(-(1 - 2^-128)/2) < 0.6065307.
- Pr[F2] <= (number of ordered triples a < c < b) * 2^-256 * 2^-140
  <= N^3/6 * 2^-396 < 2^-14.5. We use 2^-13 < 0.0001221.
- F4: each continued candidate is a distinct pair (S[h], n) with equal keys,
  so their number is at most Y = #{pairs with equal 140-bit keys}. Under H1
  the keys are independent uniform 140-bit values: E[Y] = C(N, 2) 2^-140
  < 2^115, and Var[Y] <= E[Y], since events of pairs that share one message
  are independent and disjoint pairs are independent. Chebyshev gives
  Pr[Y >= VCAP] <= 2^115 / (2^91)^2 = 2^-67. The scaled analogue of Y is
  the per-trial `masked_pairs` count; over 8,192 trials per layout its
  variance/mean ratio is 1.003 / 0.982 / 1.015 / 1.013 (Section 10.3),
  consistent with Var[Y] <= E[Y]. At full scale F4 is bounded only under H1.
- Success >= 1 - 0.6065307 - 0.0001221 - 2^-289 - 2^-67 > 0.39334. We claim
  0.39, which leaves an allowance of 0.0033.

**Rigorous partial support.** For groups g != g' and any z, z', the messages
m(g, z) and m(g', z') are independent and each is uniform on 64-byte strings,
so by Cauchy-Schwarz Pr[digests equal] >= 2^-256. Within-group pairs are a
2^-96 fraction of all pairs, so the expected number of colliding pairs is at
least (1 - 2^-96) * N(N-1)/2^257, close to 1/2 as in the uniform model. H1 is
needed for the second-moment behaviour behind Pr[F1], for F2 and for F4. This
is jaazinn's argument.

**Bitslicing, batching, truncation and encodings do not change the message
set.** They fix only the processing order, a function of (beta, t, q), never
of digests. Bitslicing, the incremental round 2, the dependency cone and the
encodings change how a digest bit is computed, not its value (Section 6).
F2 is the same event as in bfc8c418: there, too, a later message with equal
top-140 bits and a different digest overwrote S[h].

## 8. Time bound

Per message the main loop charges 36,449/256 = 142.37890625 operations plus
amortised setup (< 2^-20). This covers the Gray and incremental round-2
updates, rounds 3-6, both transpose phases, every table load, store, compare
and branch, and all loop control. On top of that come at most VCAP continued
candidates (2 units + 47 operations each) and at most one halting candidate
(2 units + 54 operations). So, in every run,

    T <= 2^128 * (142.37890625 + 2^-20)/1626 + VCAP * (2 + 47/1626) + (2 + 54/1626)
       = 2^124.48648 + 2^116.02 + 3 < 2^124.49056.

The claimed time_log2 is **124.491**, rounded up. The bound is worst-case for
every run, with no restarts: the cap turns a heavy-tailed count of
verifications into a hard limit. preprocessing_log2 = 0: setup is per batch
and inside T. Under H1 the expected verification cost is about 2^116 units,
about 103 operations per z-step on average.

## 9. Sensitivity of the bound to conventions

Each row is the same program and its worst z-step, except the bfc8c418
row. Rows for this program include its candidate term VCAP*(2 + 47/1626)
+ 3 (VCAP = 2^115 + 2^91; the 40-plane row uses its own cap 2^95 + 2^81);
the bfc8c418 row has none.

| reading | ops/z-step | ops/message | time_log2 |
| --- | ---: | ---: | ---: |
| every executed primitive once (claimed) | 36,449 | 142.38 | 124.4906 -> 124.491 |
| + one address addition per direct load/store, + one MOVI per ALU immediate | 47,144 | 184.16 | 124.861 |
| as above, + one op per shift amount | 48,716 | 190.30 | 124.909 |
| logic gates only (reference; would need > 64 registers) | 21,611 | 84.42 | 123.740 |
| bfc8c418 program, claimed reading (for comparison) | 41,679 | 162.81 | 124.680 |
| this program with 40 kept planes (160-bit key) | 37,440 | 146.25 | 124.526 |

Each candidate costs 2 units, so a smaller key with more candidates does
not pay. With 35 planes the candidate term adds 0.004 to time_log2; with
40 planes it is negligible. The register budget is 56 of 64. The
claimed 124.491 has 0.000445 of rounding slack: it would still hold if each
candidate verification cost up to 360 further operations (0.22 units), for
example for state assembly and digest extraction around the `hash`
instruction.

## 10. Evidence

### 10.1 Counted simulator (participant evidence)

The program of Section 5 was written as instructions for a counted 256-bit
word-RAM simulator with an explicit 64-register file (high-water check), a
counter per primitive, and separate counts for direct and register
addresses, immediates and shift amounts. The simulator also has a `hash`
instruction (1 unit), the reference six-round function. On 64 random
messages it equals `verifier/keccak.py:sha3_256(m, 6)`. Uninitialised
memory reads 0 in even batches (which sends every lookup down the 11-op
path) and random garbage in odd ones. Results:

- 16 batches x 4 z-steps x 256 = 16,384 messages; batch 0 starts at t = 0,
  batch 1 crosses t = 2^31 (ctz 31), the others start at random t. Every key
  equals key_of_digest(int.from_bytes(sha3_256(m, 6), "little")) computed
  from `verifier/keccak.py`: 0 mismatches. Every stored DK[n] decodes from n
  to a message whose key it is (16,384 checked). Register high-water mark 56.
- Every Gray block j = 0..31 once, plus 40 consecutive steps from t = 0:
  17,024 keys, 0 mismatches; all 32 blocks cost exactly 36,449 per z-step.
  Further seeds: 12 x 6 z-steps (18,432 keys and ids), every j plus 300
  consecutive steps (21,184 keys), 24 x 5 z-steps (30,720 keys and ids),
  and 10 x 5 z-steps on each of seeds 31337, 9001 (internal review) and
  4242 (12,800 keys and ids each): 0 mismatches. The ledger of Section 5.2
  is the simulator's per-block count of one worst-path z-step.
- **Candidate paths.** Replaying a z-step gives 256 candidates, each pairing
  the same (beta, p) one Gray step apart; the rebuilt messages equal the true
  ones, the digests differ, CNT reaches 256 and the run continues. A crafted
  candidate between distinct messages continues in 58 operations + 2 units
  (47 more than the 11-op path). With the hash replaced by a constant
  (control-flow test only) the halting path costs 54 operations + 2 units.
  The same message under two ids (only possible in F3) continues.
- With every word declared needed, the round generator emits the bfc8c418
  rounds 3-5 exactly (9,895 / 9,920 / 7,380 operations).
- The experiment evaluator of Section 10.2 was compared with
  `sha3_256(m, 6)` on 12,296 keys (a 1,100-step Gray walk over z bits 0..10 and a 300-step
  walk on z bits 22..30), with its key layout, KEYMASK and processing order
  equal to the program's: 0 mismatches.

### 10.2 Declared experiments (organizer-executed, `python-message-pairs-v1`)

All four experiments run `experiments/s3r6_bitslice_birthday.py`, which
mirrors the counted program: per-batch A2, COEF and O2P; Gray updates with
the incremental round-2 patch (Lemma 6); lane-complement rounds 3-5 with
theta at the store and the plane-0 fix (Lemmas 7-8). Rounds 4 and 5 are
computed in full, and then every stored word and fix column outside the
Lemma 10 cone (round 4: 1,363 words, all 5 fix columns; round 5: 175
words, fix columns {0, 1}) is replaced by an unrelated SHA-256-derived
constant before anything reads it; the six cone sizes are asserted. A
missing word in the cone would therefore corrupt keys and trip the sponge
check below (in review, 12 cones each missing one word all failed; in our
tests, 8 more such cones and one key row wrongly treated as zero all
failed). The last round runs on the 35 kept planes into key rows ROWOF
in the KEYMASK encoding (Lemma 9); the transpose uses
Lemma 9's zero-row delta swaps (asserted to cost 3,948 operations, the
ledger's 4 x 480 + 204 + 32 x 57) and is compared at every step with the
full 6-op transpose; key rows outside ROWOF must be 0. Keys are offered in
processing order decode_slot(q). Every digest bit used for matching comes
from that evaluator. The script maps the organizer's digest mask to key
rows and refuses a mask with a bit outside the kept planes, so equal masked
keys are equal masked digests. Each seed derives fresh 64-byte group
prefixes with SHA-256. N_t = 2^9 messages and an 18-bit mask give
N_t^2/2^18 = 1 = N^2/2^256; the uniform-model success probability is
0.39307 (0.4990 expected masked pairs per trial; 100.6 successes per 256
trials, sd 7.8). Trials sharing a batch own disjoint bit positions.
Self-checks (any failure aborts): the whole 140-bit key of each trial's
first 4 messages and of its first message at each step t = 2^i, against an
independent direct sponge (own rho offsets and round constants) mapped
through key_of_digest; the support of each coefficient column; the
incrementally maintained O2P against a rebuild after the batch's last step;
and, at every step, the zero rows and the zero-row transpose as above.
These cone and transpose checks were added after review; the script's
outputs are byte-identical to the earlier version on every seed run
(Section 10.3).

Layouts: `k6r6-bs-full-width` 256 groups x 2; `k6r6-bs-spread` 16 x 32;
`k6r6-bs-single-group` 1 x 512 (strongest within-group structure);
`k6r6-bs-high-z` 4 x 128 with z = gray(t) << 25 (for j >= 27 the support
wraps around the lane). The four 18-bit masks are spread over digest lanes
0-3 and use only kept planes; they differ from bfc8c418's masks, some of
whose bits this program does not compute. The experiment ids and the
prefix label are those of bfc8c418, so for a given organizer seed the
trials use the same message sets as there; only the masks differ.

### 10.3 Local runs (not organizer evidence; every run reported)

Every run of the experiment script is listed, including those of our
internal review (marked R). The script was run in two versions: before
review, and the final version with the cone and transpose checks of
Section 10.2. Every seed in the first table and the bs3-a,
committee-oct6 and memprobe runs were run with both, with identical
results (replay stdout byte-identical); the two reviewer pair-statistics
runs below used only the earlier version, which computes the same keys.
Organizer-runner replays use `experiments/runner.py` with a subprocess
executor instead of Docker, 256 trials, every returned pair recomputed by
the organizer predicate, and each experiment executed twice per replay.
No self-check failed in any run (1,280 / 2,304 / 2,816 / 2,816 key checks
and 256 O2P rebuilds per experiment and seed). The public seed was replayed
at least seven times; the stdout hashes are always ea33eeca / b6132c29 /
14511d57 / b16f17a4. The `bs3-rv-*` and `bs3-a` seeds were fixed before
any of them was run. Successes (z against 100.6 +- 7.8):

| seed | full-width | spread | single-group | high-z |
| --- | ---: | ---: | ---: | ---: |
| hashsmash-public-seed-v1 | 93 (-1.0) | 98 (-0.3) | 99 (-0.2) | 109 (+1.1) |
| bs3-rv-1 | 103 (+0.3) | 104 (+0.4) | 110 (+1.2) | 111 (+1.3) |
| bs3-rv-2 | 104 (+0.4) | 99 (-0.2) | 99 (-0.2) | 99 (-0.2) |
| bs3-rv-3 | 101 (0.0) | 102 (+0.2) | 100 (-0.1) | 92 (-1.1) |
| bs3-rv-4 | 117 (+2.1) | 107 (+0.8) | 99 (-0.2) | 106 (+0.7) |
| committee-c1 (R) | 97 (-0.5) | 100 (-0.1) | 107 (+0.8) | 97 (-0.5) |
| `--local` seed "timing3" | 107 (+0.8) | 90 (-1.4) | 100 (-0.1) | 101 (0.0) |

Masked pairs on the public seed: 111 / 121 / 132 / 137 (expected 127.8).
Larger `--local` runs (successes, z, masked pairs):

| layout | bs3-a, 8,192 trials (model 3,220.0 +- 44.2; 4,088.0 pairs) | committee-oct6 (R), 2,048 trials (model 805.0 +- 22.1; 1,022.0 pairs) |
| --- | ---: | ---: |
| full-width | 3,251, +0.7, 4,127 | 808, +0.1, 1,013 |
| spread | 3,222, 0.0, 4,049 | 802, -0.1, 1,026 |
| single-group | 3,151, -1.6, 3,993 | 806, 0.0, 1,040 |
| high-z | 3,149, -1.6, 3,977 | 771, -1.5, 951 |

A single-group run with seed "memprobe" (R, 256 trials) gave 95 successes
(z -0.7) and 113 masked pairs. Pooled over every run with a success count
(12,032 / 12,032 / 12,288 / 12,032 trials) the successes are 4,781 /
4,724 / 4,766 / 4,635 against 4,729.5 +- 53.6 (single-group 4,830.1 +-
54.1): z = +1.0 / -0.1 / -1.2 / -1.8. Our own runs alone (9,728 trials per
layout) give z +1.1 / 0.0 / -1.4 / -1.2. The largest cell is +2.1
(bs3-rv-4, full-width). bfc8c418 reported pooled z +0.9 / +0.9 / +1.2 /
-1.6 (19,456 trials per layout, other masks, same digests).

**Candidate count (F4).** `masked_pairs` is the scaled analogue of Y.
Per trial in bs3-a, mean / variance are 0.504 / 0.505, 0.494 / 0.485,
0.487 / 0.495 and 0.486 / 0.492 (uniform model 0.499 / 0.499), so
variance / mean is 1.003 / 0.982 / 1.015 / 1.013; in committee-oct6 it is
0.978 / 1.028 / 1.031 / 0.978. A reviewer's separate run (R, 2,048 trials
per layout, own wrapper, only pair statistics recorded) gave mean 0.497 /
0.496 / 0.513 / 0.501 and variance / mean 1.003 / 1.001 / 0.973 / 1.023.
This is consistent with Var[Y] <= E[Y] as used for F4.

**Within-group and cross-group pairs** (pair counts only; expected value
and z under the uniform model; the R rows use seeds "split-c1-t"):

| run | layout | trials | within group | cross group |
| --- | --- | ---: | ---: | ---: |
| bs3-a | full-width | 8,192 | 8 (8.0, 0.0) | 4,119 (4,080.0, +0.6) |
| bs3-a | spread | 8,192 | 252 (248.0, +0.3) | 3,797 (3,840.0, -0.7) |
| bs3-a | high-z | 8,192 | 990 (1,016.0, -0.8) | 2,987 (3,072.0, -1.5) |
| committee-oct6 (R) | high-z | 2,048 | 238 (254.0, -1.0) | 713 (768.0, -2.0) |
| split (R) | high-z | 16,384 | 2,021 (2,032.0, -0.2) | 6,023 (6,144.0, -1.5) |
| split (R) | single-group | 8,192 | 4,151 (4,088.0, +1.0) | none |
| split (R) | spread | 8,192 | 262 (248.0, +0.9) | 3,825 (3,840.0, -0.2) |

The high-z shortfall lies in cross-group pairs: over the three independent
high-z sets (26,624 trials) within-group pairs are 3,249 against 3,302
(z -0.9) and cross-group pairs 9,723 against 9,984 (z -2.6). Cross-group
pairs join messages with independent uniform prefixes, so their expected
count is provably at least the uniform value (Cauchy-Schwarz, Section 7);
a deficit there cannot be a systematic effect, and we read it as sampling
fluctuation. Recomputing every digest of the bs3-a and committee-oct6
high-z trials with `verifier/keccak.py` (5,242,880 digests) gives exactly
the evaluator's per-trial pair counts (10,240 of 10,240 trials), so the
counts are properties of the digests, not of the evaluator.

## 11. Memory

| array | 32-byte words | bytes |
| --- | --- | --- |
| S (at 2^200) | 2^140 | 2^145 |
| DK (key of message n at address n) | <= 2^128 | <= 2^133 |
| PREF (at 2^170) | 2^97 | 2^102 |
| A2, O2P, two state buffers, ROWS, COEF, CNT, setup arrays (at 2^240) | < 2^14 | < 2^19 |
| code (unrolled z-step, 32 incremental blocks, setup) | < 2^20 instructions | < 2^25 |

Total < 2^145.01 bytes; we claim 146. Memory is reported only.

## 12. Limitations

- H1 is a heuristic. It extends the grouped structure (A2 affine in z within a
  group; shared prefix pairs across groups) from the tested scale
  (N_t = 2^9, 18-bit masks) to N = 2^128 and the 256-bit digest. The
  experiments use a full dictionary of masked keys; the table loss F2 and
  the candidate count F4 cannot be scaled down faithfully and are bounded
  only under H1. F4 enters only through Pr[F4] <= 2^-67. Organizer seeds
  are public. A 256-trial experiment resolves the success frequency only to
  about +-0.03, and the 0.0033 allowance is not statistically certified.
- Within a group the digest has algebraic degree at most 2^5 = 32 in z
  (five chi layers, rounds 2-6, after the affine A2). z has 32 bits, so
  this bound gives no zero-sum over any affine subspace of z (a guaranteed
  zero-sum needs dimension at least 33). This concerns only within-group
  pairs (a 2^-96 fraction of pairs).
- The gain comes from operation-level pricing (bitslicing, grouping,
  Lemma 6, lane complementing, and skipping 116 digest bits at a charge of
  2 units per candidate). All executed work, including all memory traffic
  and every candidate verification, is charged. The 64-register machine is
  an assumption (56 are used); Section 9 gives stricter readings.
- No sub-birthday attack, collision certificate or full-scale run is claimed.

## 13. Credit

Co-authors in the sense of Section 0: **jaazinn** (0a5b7ae8), **may93182**
(11c46f4d). Credited: tekkac (b001199a, f58275ef), ercumentyildirim
(c7fa1a56, 4c969300), zeeshan8281 (cbf7998d), mitchuski (02d6a703), as in
Section 0. Errors are ours.
