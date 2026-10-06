# sha3-256-r6: bitsliced grouped birthday search, time_log2 = 124.680

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

New in this package (ours): an **incremental round 2** (each Gray step patches
the stored, already theta'd round-3 input with the exact chi difference of the
60 affected rows, Lemma 6), **theta applied at the store** (each round adds the
next round's D words while a plane's 25 outputs are still in registers, with a
5-word plane-0 fix-up, Lemma 7), the **last round fused with five transpose
stages**, and a **sparse set whose stored index is the message number**.

A z-step evaluates 256 messages with one counted, fully unrolled program
(branches only in the ctz tree, the table step and the loop test). Its
worst path is **41,679 executed primitives** (162.81 per message with setup).

| quantity | value |
| --- | --- |
| messages N | 2^128 = 2^88 batches x 256 groups x 2^32 values of z |
| ops per z-step (256 messages), worst path | 41,679 (every executed primitive) |
| ops per message charged | 162.81 (41,679/256 + setup < 2^-20) |
| total T | <= 2^128 * 162.81/1626 + 3 < 2^124.67994 |
| claimed time_log2 | **124.680** |
| success probability | >= 0.39334 under H1; claimed 0.39 |
| memory | < 2^145.01 bytes; claimed 146 |

**Credit.** **jaazinn** (Yukon ticket 0a5b7ae8, blake3-r2, in review)
originated grouped partial evaluation, the Briggs-Torczon sparse set on the top
140 key bits, the failure analysis with heuristic H1 and the scaled-experiment
design, and is named as co-author in that sense. **may93182** (11c46f4d, in
review) introduced for this track the 256-way bit-plane Keccak and the
delta-swap transpose at 6 operations per row pair, and is likewise named as
co-author in that sense. **tekkac** (b001199a) brought the
Keccak team's lane-complement chi with round constants folded into polarity
to this track; our polarity patterns were found by our own search. The
last-round early abort (the digest-only last round, for which the previous
round stores only the 5 diagonal lanes 0, 6, 12, 18, 24) is
**ercumentyildirim**'s, in the bit-sliced circuit on this track (c7fa1a56)
and on sha3-256-r5 (4c969300). Charging the exact per-message count instead
of a rounded one follows zeeshan8281 (cbf7998d) and tekkac (f58275ef). The
reading of Section 1 (64 registers, every load and store charged)
corresponds to the every-core-load-and-store-charged row of **mitchuski**'s
sensitivity table (02d6a703). None of them has reviewed this package. Ours:
the SHA3 column pairing and affine reduction (Lemmas 1-3), Lemmas 6-7, the
fused last round, the table layout and the counted program. Errors are ours.

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
  specifies only the word RAM. The program uses at most 56 registers. Our
  basis: a word RAM has a fixed-size register file, and an operation on
  register operands is one primitive, not a memory access; 64 registers of
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
  shift amount; every such variant stays below 125.10.

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
round each plane's 4 digest outputs take whichever polarity costs no NOT; the
resulting fixed bits form KEYMASK (lane 0 complemented except bits 0 and 31;
lanes 1-3 plain; 62 bits set). All gates are exact; no data-dependent choice
is made. A2 is stored unencoded; the incremental updates of Lemma 6 are
differences and preserve the Q3 encoding of O2P.

**Lemma 9 (fused last round and transpose order).** Key row r = 64x + b
(x < 4) is digest-lane x, bit b. For block g = 0..7, the last round computes
the 32 rows with b = 8g + bl (bl < 8), x < 4, in registers (register index
8x + bl), applies the delta-swap stages d = 1, 2, 4 (row bits of bl) and
d = 64, 128 (row bits of x) inside the block, and stores the 32 rows. Phase 2
then loads, for each of the 32 pairs (x, bl), the 8 rows 64x + 8i + bl
(i < 8), applies stages 8, 16, 32 and hands row 64x + 8i + bl straight to the
table. By Lemma 5 all 8 stages are applied exactly once, so row r ends as the
256-bit key of slot r; the offer order is q = 8(8x + bl) + i, i.e. slot
decode_slot(q) of Section 2.

## 5. The algorithm and its counted program

### 5.1 Batch setup (once per batch of 2^40 messages)

1. Draw 512 random words (RAND); store each to PREF + 512*beta + 2p + w and to
   STATE0 + 256w + p. 2. Transpose both 256 x 256 matrices. 3. Store the 1088
   padding planes. 4. Compute the round-1 D words. 5. Run round 1 (plain
   encoding) and form A2 = STATE1 XOR D for all 1600 words. 6. For j = 0..31:
   complement P(0, j) and P(5, j), rerun round 1 (D words reused, Lemma 1),
   store COEF[j][k] = A2(e_j) XOR A2(0) on SUPPORT_j[k], restore.
7. Build O2P: round 2 from A2 with output polarity P34 and theta at the store
   (Lemma 7), then apply the plane-0 fix in memory. 8. s = 0.

Counted setup: 483,643 operations per batch (675,265 with the extra charges
of Section 9). With batch-loop control (< 2^20 in all) this is < 2^-20 per
message.

### 5.2 Per z-step program (fully unrolled; worst path)

Persistent registers: s (the step counter t), n (the message number), SB =
SBASE and ONE = 1 (set once per run). Other registers are allocated per block
(at most 56 live in all). For t = 0 the step starts at (c).

    (a) control, t >= 1 (16): s = s + ONE ; 5-level branch tree on ctz(s):
        v = s AND ((2^sh - 1) << j0) ; c = (v == 0) ; branch   (sh = 16,8,4,2,1)
        32 duplicated leaves, no indirect jump; leaf j falls into block j.
    (b) incremental round 2, block j (4,149; Lemma 6): per affected plane in
        a fixed order, per affected row: load COEF and A2 words, A2 ^= COEF,
        store A2, form dout; then dC, dD and O2P ^= dout ^ dD (load, XOR,
        store) on every structurally affected O2P word; jump to (c).
    (c) R3 = ROUND_TS(O2P, -,   ST0, all,  RC[2], Q3 -> P34)        9,895
        R4 = ROUND_TS(ST0, fix, ST1, all,  RC[3], Q3 -> P34)        9,920
        R5 = ROUND_TS(ST1, fix, ST0, DIAG, RC[4], Q3 -> P5)         7,380
    (d) LAST(ST0, fix): last round fused with stages 1,2,4,64,128   4,938
    (e) PHASE2: stages 8,16,32 and SPARSE(K) on each finished key   5,379
    (f) c = (s < 2^32 - 1) ; branch                                     2

ROUND_TS(src, fix, dst, LANES, rc, qin -> pout); registers out[0..24], B[0..4],
one complement scratch, t, two 5-word parity buffers and C0[0..4]:

    for b = 0..63:
      for Y = 0..4:
        for X = 0..4: (x,y) = pisrc(X,Y), L = x+5y, b' = (b - RHO[L]) mod 64
          B[X] = LOAD [src + 64L + b'] ; if b' = 0 and fix: B[X] = B[X] XOR fix[x]
        chi row Y by the Lemma 8 plan: 1 NOT, 5 AND/OR, 5 XOR -> out[X+5Y]
      C[x] = out[x] ^ out[x+5] ^ out[x+10] ^ out[x+15] ^ out[x+20]  (x = 0..4; C0 if b = 0)
      for x = 0..4:
        if b > 0: t = C[x-1] XOR Cprev[x+1]
        for L in LANES with L mod 5 = x: if b > 0: out[L] ^= t ; STORE [dst + 64L + b] = out[L]
    fix'[x] = C0[x-1] XOR C63[x+1]   (x = 0..4, returned in registers)

Per plane: 25 loads, 5 + 50 chi ops, 20 parity XORs, |LANES| stores, and for
b >= 1, 5 + |LANES| theta XORs. Round 3 (no fix input, all lanes):
64*(25+55+20+25) + 63*30 + 5 = 9,895; round 4 adds 25 fix XORs: 9,920;
round 5 stores the 5 diagonal lanes 0, 6, 12, 18, 24 (the only inputs of
output row 0): 64*(25+55+20+5) + 63*10 + 25 + 5 = 7,380.

LAST: 5 MOVI (masks), then for g = 0..7: for bl = 0..7: 5 loads of the
diagonal lanes (plus the 5 fix XORs in all where b' = 0), 4 outputs x 2 ops
(no NOT, Lemma 8); then 5 stages x 16 swaps x 6 ops; 32 stores. Total
5 + 64*13 + 5 + 8*480 + 256 = 4,938. PHASE2: 3 MOVI + 32 x (8 loads +
3 x 4 x 6) = 2,563, plus 256 SPARSE steps of at most 11: 5,379.

SPARSE(K), Briggs-Torczon step on the top 140 key bits (n is the number of
the current message, DK[n] lives at address n):

    h = K SHR 116 ; a = h + SB ; i = LOAD [a] ; c = (i < n) ; if !c goto INS
    k2 = LOAD [i] ; c = (k2 == K) ; if c goto MATCH
    INS: STORE [n] = K ; STORE [a] = n ; n = n + ONE

Paths: S[h] >= n (never written, or garbage) 8; S[h] < n with a different
key 11 (the worst); match 8, then verification. No immediate occurs apart
from the shift amount.

**Ledger (one z-step, worst path: ctz(t) = 31, every message on the 11-op
path; counted by the simulator, Section 10.1).**

| block | ops | of which direct loads/stores |
| --- | ---: | ---: |
| (a) control | 16 | 0 (+10 immediates) |
| (b) incremental round 2 + jump | 4,149 | 2,488 |
| round 3 | 9,895 | 3,200 |
| round 4 | 9,920 | 3,200 |
| round 5 | 7,380 | 1,920 |
| last round + stages 1,2,4,64,128 | 4,938 | 576 |
| stages 8,16,32 + 256 sparse steps | 5,379 | 256 |
| (f) loop test | 2 | 0 (+1 immediate) |
| **total per 256 messages** | **41,679** | **11,640 (+11)** |

By opcode: 6,712 direct and 512 register loads, 4,928 direct and 512 register
stores, 17,898 XOR, 3,915 AND, 2,304 OR, 1,036 NOT, 1,024 SHL, 1,280 SHR,
513 ADD, 518 CMP, 519 branch, 8 MOVI. Block (b) is 1,336 loads, 1,152
stores, 1,450 XOR, 134 AND, 76 NOT and 1 branch for every j = 0..31, so the
worst case equals the Gray average.

### 5.3 Sparse set

S has 2^140 words at SBASE = 2^200 and is never initialised; DK[n] = K is
written at address n for every processed message, so every address below
the current n holds a key of an earlier message, written once and never
changed. A lookup is valid iff S[h] < n; then DK[S[h]] is the key of an
earlier message, and MATCH requires equality of all 256 bits. On every
non-match S[h] is overwritten with n. Garbage in S is therefore either
>= n (insertion) or points to a genuine earlier key (a full comparison, then
overwrite); it is never trusted further.

### 5.4 Verification and halting

On the first MATCH (ids i = S[h] and n): decode each id to beta = id >> 40,
t = (id >> 8) mod 2^32, q = id mod 256, p = decode_slot(q), z = gray(t)
(under 20 operations each), load the two prefix words of each (under 10),
rebuild both messages (under 20). If they are equal (only in event F3),
halt with failure. Otherwise evaluate both with two reference permutations
(2 units), compare the 256 digest bits and output the pair. This is under
2 units + 200 operations, capped at 3 units.

## 6. Correctness (unconditional)

- **Evaluator exactness.** Lemmas 2-3 make A2 exact at every t; Lemma 6 keeps
  O2P equal to the encoded, theta'd round-2 output of the current A2; Lemma 4
  with Lemmas 7 and 8 makes rounds 3-5 exact in their encodings; the last
  round computes digest lanes 0..3 in the KEYMASK encoding; Lemma 9 makes
  the key of slot r equal K* XOR KEYMASK. Section 10 checks this bit for bit.
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
  different key (so S[h] no longer points to a or to a copy of key(a)).

If none of F1, F2, F3 occurs, take a colliding pair (a, b). When a is
processed it either matches (success) or sets S[h] = n_a. Any later c with
the same top bits either has key(a) and matches, or (excluded by not-F2) does
not exist before b. So at b's lookup S[h] holds n_a or the number of a message
with key(a), which is < n_b, and DK at that address equals key(b): MATCH no
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

Per message, the charge is 41,679/256 = 162.80859 plus amortised setup
(< 2^-20), at most 162.81 operations or 162.81/1626 units. It covers the Gray
and incremental round-2 updates, rounds 3-6, both transpose phases, every
table load, store, compare and branch, and all loop control. The only other
cost is verification (< 3 units, at most once). So

    T <= 2^128 * 162.81/1626 + 3 = 0.1001291... * 2^128 + 3 < 2^124.67994.

The claimed time_log2 is **124.680**, rounded up. The bound is worst-case for
every run, with no restarts. preprocessing_log2 = 0: setup is per batch and
inside T.

## 9. Sensitivity of the bound to conventions

| reading (same program, worst z-step) | ops/z-step | ops/message | time_log2 |
| --- | ---: | ---: | ---: |
| every executed primitive once (claimed) | 41,679 | 162.81 | 124.680 |
| + one address addition per direct load/store, + one MOVI per ALU immediate | 53,330 | 208.33 | 125.036 |
| as above, + one op per shift amount | 55,634 | 217.33 | 125.097 |
| logic gates only (reference; would need > 64 registers) | 25,153 | 98.26 | 123.952 |

The second row is the convention of our earlier package 377eebd5, whose
program gives 61,583 / 81,085 per z-step (125.244 / 125.640) under the first
two rows; it claimed 125.655 after rounding to 320 per message. For
comparison, mitchuski (02d6a703) reports 126.42 for its circuit with every
core load and store charged, the convention of our first row (and 126.64
for a narrow 64-register file with +1 per direct access). The register
budget is 56 of 64.

## 10. Evidence

### 10.1 Counted simulator (participant evidence)

The program of Section 5 was written as instructions for a counted 256-bit
word-RAM simulator with an explicit 64-register file (high-water check), a
counter per primitive, and separate counts for direct and register
addresses, immediates and shift amounts. Uninitialised memory reads 0 in even
batches (which sends every lookup down the 11-op path) and random garbage in
odd ones. Results:

- 16 batches x 4 z-steps x 256 = 16,384 messages; batch 0 starts at t = 0,
  batch 1 crosses t = 2^31 (ctz 31), the others start at random t. Every key
  equals int.from_bytes(sha3_256(m, 6), "little") XOR KEYMASK with
  `verifier/keccak.py`: 0 mismatches. Every stored DK[n] decodes from n to a
  message whose key it is (16,384 checked). Register high-water mark 56.
- Every Gray block j = 0..31 once, plus 40 consecutive steps from t = 0
  (the incremental updates accumulate): 17,024 keys, 0 mismatches; all 32
  blocks cost exactly 41,679 per z-step.
- For 4 groups and z bits 0, 5, 17, 31, a scalar recomputation of
  A2(e_j) XOR A2(0) is 0 outside SUPPORT_j and equals the COEF bits inside.
- The ledger of Section 5.2 is the simulator's per-block count of one
  worst-path z-step. Replaying a z-step gave 256 MATCHes, each pairing the
  same (beta, p, z) one z-step apart; a crafted key sharing the top 140 bits
  takes the 11-op path.
- Re-checks during our internal review, with coins drawn afresh: 12 batches
  x 6 z-steps (18,432 keys, 0 mismatches, all 18,432 stored keys decode
  from their message number); 600 consecutive z-steps from t = 3*2^20 - 300
  (ctz up to 20; 4,200 keys checked, 0 mismatches; the incrementally
  maintained O2P equals a rebuild from A2 at every 100th step); 4,608 more
  keys and another full j = 0..31 pass (0 mismatches). The experiment
  evaluator of Section 10.2 was also compared with `sha3_256(m, 6)` on
  20,480 keys (random prefixes, crossing t = 2^31, 40 consecutive steps):
  0 mismatches.

### 10.2 Declared experiments (organizer-executed, `python-message-pairs-v1`)

All four experiments use `experiments/s3r6_bitslice_birthday.py`. It mirrors
the counted program: per-batch A2, COEF and O2P; the Gray update of A2 with
the incremental round-2 patch of O2P (Lemma 6); lane-complement rounds 3-5
with theta at the store and the plane-0 fix (Lemmas 7-8); the row-0 last
round in the KEYMASK encoding; the transpose in stage order 1, 2, 4, 64, 128,
8, 16, 32; keys offered in processing order decode_slot(q). Every digest used
for matching comes from that evaluator; equal masked keys are equal masked
digests. Each organizer seed derives fresh 64-byte group prefixes with
SHA-256. N_t = 2^9 messages and an 18-bit mask give N_t^2/2^18 = 1 =
N^2/2^256; the uniform-model success probability is 0.39307 (0.4990 expected
masked pairs per trial; for 256 trials, 100.6 successes, sd 7.8). Trials
sharing a batch own disjoint bit positions, and no operation mixes
positions. Every trial checks at full width, against an independent direct
sponge (own rho offsets and round constants), its first 4 keys and its first
key at each step t = 2^i (one step of every Gray block used); checks the
support of each coefficient column; and after the batch's last step compares
the incrementally maintained O2P word for word with O2P rebuilt from A2. Any
failure aborts.

Layouts: `k6r6-bs-full-width` 256 groups x 2; `k6r6-bs-spread` 16 x 32;
`k6r6-bs-single-group` 1 x 512 (strongest within-group structure);
`k6r6-bs-high-z` 4 x 128 with z = gray(t) << 25 (z bits 25..31; for j >= 27
the support wraps around the lane). All use z = gray(t).

### 10.3 Local runs (our seeds; not organizer evidence; all runs reported)

Organizer-runner replay (`experiments/runner.py`, subprocess executor in
place of Docker, track config hash, seed `hashsmash-public-seed-v1`, 256
trials): each experiment ran twice, byte-identical stdout, 1.6-3.2 s per run;
every returned pair re-checked with `verifier`; no self-check failed
(1,280 / 2,304 / 2,816 / 2,816 full-width key checks and 256 O2P rebuild
checks per experiment).

| experiment | successes / 256 | z (model 100.6, sd 7.8) | masked pairs (exp. 127.8) |
| --- | ---: | ---: | ---: |
| k6r6-bs-full-width | 100 | -0.1 | 123 |
| k6r6-bs-spread | 109 | +1.1 | 150 |
| k6r6-bs-single-group | 107 | +0.8 | 144 |
| k6r6-bs-high-z | 111 | +1.3 | 138 |

These equal the counts of our earlier package's evaluator on the same seed,
as they must: the digests are the same values, and a trial's success and
pair count depend only on its multiset of masked digests, not on the order
or encoding in which they are computed.

Larger runs of the same program (`--local`, 8,192 trials per layout and
batch, local seeds "bs2-a" and "bs2-b", both fixed before either was run).
Every run we made with this program is listed. The model is 3220.0 +- 44.2
per batch and 6440.1 +- 62.5 pooled:

| layout | batch a | batch b | pooled | pooled z | pairs (exp. 8176) |
| --- | ---: | ---: | ---: | ---: | ---: |
| full-width | 3243 (+0.5) | 3253 (+0.7) | 6496 | +0.9 | 8148 |
| spread | 3248 (+0.6) | 3270 (+1.1) | 6518 | +1.2 | 8271 |
| single-group | 3318 (+2.2) | 3205 (-0.3) | 6523 | +1.3 | 8278 |
| high-z | 3197 (-0.5) | 3174 (-1.0) | 6371 | -1.1 | 8099 |

One of the eight cells is at +2.2 (single-group, batch a; batch b gave -0.3);
with eight cells this is within what sampling noise gives (about 1 in 5 for
some |z| >= 2.2), and it is in the direction of more collisions. Before
these, one 256-trial timing run per layout (local seed "timing") gave 108,
99, 103 and 99 successes (full-width, spread, single-group, high-z; z +1.0,
-0.2, +0.3, -0.2).

Internal-review replays (organizer runner as above, 256 trials, coins
drawn afresh after the runs above; every run made is listed, no
self-check failed, every returned pair re-checked with `verifier`):

| seed | full-width | spread | single-group | high-z |
| --- | ---: | ---: | ---: | ---: |
| cmt-fresh-1006 | 102 | 91 | 108 | 92 |
| fresh-review-coin-20261006-a | 93 | 111 | 99 | 98 |
| rv-coin-b | 102 | 107 | 98 | 92 |
| rv-coin-c | 102 | 98 | 103 | 107 |
| rv-coin-d | 102 | 110 | 94 | 94 |
| rv-coin-e | 97 | 94 | 101 | 98 |
| rv-coin-f | 108 | 75 | 80 | 92 |
| rv-coin-g | 98 | 99 | 100 | 94 |
| rv-coin-h | 88 | 98 | 113 | 89 |
| rv-coin-i | 112 | 97 | 98 | 102 |
| total / 2,560 (model 1,006.3 +- 24.7) | 1,004 (-0.1) | 980 (-1.1) | 994 (-0.5) | 958 (-2.0) |

The lowest cell is 75 (spread, rv-coin-f, -3.3 sd per cell; the same seed
gave 80 for single-group, -2.7). Among 40 cells one at -3.3 is more than
sampling noise usually gives (about 1 in 25 for some |z| >= 3.3); it is in
the direction of fewer collisions. Pooled over every run listed in this
section (19,456 trials per layout) the z-scores are +0.9 (full-width), +0.9
(spread), +1.2 (single-group) and -1.6 (high-z). We report the cell; we
have no explanation for it beyond sampling noise.

## 11. Memory

| array | 32-byte words | bytes |
| --- | --- | --- |
| S (at 2^200) | 2^140 | 2^145 |
| DK (key of message n at address n) | <= 2^128 | <= 2^133 |
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
  of round 2; lane complementing removes most NOTs. All executed work,
  including all memory traffic, is charged once. The 64-register machine is
  an assumption (56 are used). Section 9 gives the bound under stricter
  readings.
- No sub-birthday attack, collision certificate or full-scale run is claimed.

## 13. Credit

**jaazinn** (0a5b7ae8) and **may93182** (11c46f4d), co-authors in the sense
of Section 0; **tekkac** (b001199a; lane complementing in this track, after
the Keccak team); **ercumentyildirim** (c7fa1a56, 4c969300; last-round early
abort); **zeeshan8281** (cbf7998d) / **tekkac** (f58275ef) for exact
charging; **mitchuski** (02d6a703; the counting reading), as in Section 0.
Errors are ours.
