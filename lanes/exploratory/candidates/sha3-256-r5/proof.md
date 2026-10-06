# sha3-256-r5: bitsliced grouped birthday search v2, time_log2 = 124.551

## 0. Summary and credit

A generic birthday search over full 256-bit digests; no cryptanalytic
weakness of SHA3 is claimed. This is version 2 of our bitsliced grouped
package on this track (ticket ae9a4286, 125.551, in review). The message set,
heuristic H1 and failure analysis are the same; the per-message program has
34% fewer operations.

- **Grouping** (jaazinn): groups of 2^32 messages share a random prefix; the
  round-2 theta output A2 is exactly affine in the counter z (Lemma 2).
- **Bitslicing** (may93182): each 256-bit word holds one state bit of 256
  messages; rotations are address renamings; a priced transpose gives keys.
- **New in v2** (Sections 4.1-4.3): incremental round 2 (only the 60 chi
  rows touched by a Gray step are differenced), theta added before each
  store, lane-complemented chi, the last round fused with the transpose.

A z-step evaluates 256 messages. It is one counted, fully unrolled program
(branches only in the ctz tree, the table step and the loop test) whose
worst path is **31,759 operations**, every executed primitive counted
once, including every load and store (Section 1): 124.06 per message.

| quantity | value |
| --- | --- |
| messages N | 2^128 = 2^88 batches x 256 groups x 2^32 values of z |
| ops per z-step (256 messages), worst path | 31,759 (every load/store, logic op, shift, add, compare, branch, MOVI) |
| ops per message charged | 124.06 (31,759/256 = 124.0586 + setup < 2^-20 + spare) |
| total T | <= 2^128 * 124.06/1355 + 3 < 2^124.55082 |
| claimed time_log2 | **124.551** |
| success probability | >= 0.39334 under H1; claimed 0.39 |
| memory | < 2^145.01 bytes; claimed 146 |

**Credit.** **jaazinn** (Yukon ticket 0a5b7ae8, blake3-r2, in review)
originated grouped partial evaluation, the Briggs-Torczon sparse set on the
top 140 key bits, the F1/F2/F3 analysis with heuristic H1 and the
scaled-experiment design, and is named as co-author in that sense.
**may93182** introduced on the sha3-256-r6 track the 256-way bit-plane Keccak
(rotations as plane renaming) and the delta-swap transpose (submission
11c46f4d, in review), and is likewise named as co-author in that sense. The
**lane-complement** representation of chi is the Keccak team's
implementation technique; **tekkac** applied it on the sha3-256-r6 track with
per-row polarity search and round constants folded into polarity
(b001199a, in review), which is where we took it from. The scalar last-round
early abort on this track is **ercumentyildirim**'s (4c969300). Charging
the exact per-message count instead of a rounded one follows **zeeshan8281**
(sha3-256-r6, cbf7998d) and **tekkac** (f58275ef); the reading of Section 1
corresponds to the every-core-load-and-store-charged row of **mitchuski**'s
sensitivity table (sha3-256-r6, 02d6a703). None of them has reviewed this
package. Ours: Lemmas 1-3 and 6-7, the 62-word Gray support, the incremental
round 2, theta-at-store with the plane-0 fix, the fused last round and
transpose, the key-at-message-number table layout, the polarity patterns used
here and the counted program; errors are ours.

## 1. Target, machine and charging conventions

- Target `sha3-256-r5-prefix-v1`: the complete SHA3-256 sponge (rate 1088,
  capacity 512, suffix 0x06, pad10*1, zero IV), Keccak rounds 1..5 in our
  numbering (constants RC[0..4]) and all 256 output bits, as in
  `verifier/keccak.py:sha3_256(msg, 5)`. Messages are exactly 64 bytes (one
  block). Lane k (k < 8) is bytes 8k..8k+7 little-endian; lane 8 = 0x06,
  lane 16 = 0x80 << 56, the other lanes 0. Lane index L = x + 5y.
- Digest = lanes 0..3 after round 5, little-endian; D = int.from_bytes(digest,
  "little"). The program stores the key K = D XOR KEYMASK for a fixed
  256-bit constant KEYMASK (Lemma 8). This is a bijection, so equal keys and
  equal digests are the same event, and the top 140 bits of K determine those
  of D.
- Cost model `collision-frontier-v5`, C = 1355: one five-round permutation
  costs 1 unit; every other primitive (256-bit load or store, add/sub,
  AND/OR/XOR/NOT, shift, compare, conditional branch, random word) costs
  1/1355. Machine: a 256-bit word RAM with 64 registers. The register count
  is our stated assumption; v5 specifies only the word RAM. The program never
  has more than 56 live registers. Our basis: a word RAM has a fixed-size
  register file, and an operation on register operands is one primitive,
  not a memory access; 64 registers of 256 bits are 2 KiB, the size of a
  32-entry 512-bit SIMD register file. A memory-to-memory reading (every
  ALU operand loaded and every result stored) is a different machine; we
  do not claim the bound under it.
- **Charging (the claimed reading).** Every executed primitive costs one:
  every load and store (direct or register-addressed), XOR, AND, OR, NOT,
  shift, add, compare, conditional branch, immediate move (MOVI) and random
  word. The program is fully unrolled, so most addresses are constants of the
  instruction, as are the immediate operands of AND/compare in loop control
  (11 per z-step) and shift amounts; those are instruction fields, not
  executed operations, and are not charged a second time. S addresses are
  SB + h by a counted ADD; DK is addressed by the message number itself
  (base 0); PREF is used only in setup and verification. Our earlier
  packages also charged one address addition per direct access and one
  MOVI per immediate; Section 9 gives that count (124.892) and stricter
  ones. All of them are below every score on this track as of
  2026-10-06 03:09Z (Section 8).
- No rotation or indirect jump is executed (Lemma 4).

## 2. Messages, groups, batches and processing order

For group g the algorithm draws two fresh uniform 256-bit words R0, R1; their
little-endian bytes form a uniform 64-byte prefix P_g, which is stored. For
z in {0,1}^32:

    m(g, z) = P_g with LE32(z) XORed into bytes 0..3 and into bytes 40..43,

so z is XORed into the low 32 bits of lane 0 (x=0, y=0) and of lane 5
(x=0, y=1). Write g = 256*beta + p with batch index beta < 2^88 and slot
p < 256. Batch beta runs t = 0, 1, ..., 2^32 - 1 with z = gray(t) =
t XOR (t >> 1) and evaluates the 256 messages m(256*beta + p, gray(t)) at
each t. They are offered to the table in processing order q = 0..255 with

    p = decode_slot(q) = 64*(q >> 6) + 8*(q AND 7) + ((q >> 3) AND 7),

a fixed permutation of 0..255. Batches run in order beta = 0, 1, .... The
message number of (beta, t, q) is n = beta*2^40 + t*2^8 + q, which is also
the count of messages processed before it. Every message is evaluated exactly
once, and N = 2^128.

**Bit mapping.** Word P(L, b) holds in bit position p bit b of lane L of
message m(256*beta + p, z). Row p of input matrix w is R_w of slot p; after
the transpose row k of matrix w is P(4w + floor(k/64), k mod 64). Padding
planes: P(8,1) = P(8,2) = P(16,63) = all-ones, other planes of lanes 8..24 0.

## 3. Dependency analysis (exact)

Every step map except chi is GF(2)-linear. Fix a group and view each state as
a function of z. A2 is the state after round 1 and the theta of round 2.

**Lemma 1.** Lanes 0 and 5 lie in column x = 0 and carry the same difference
z, so all round-1 parities C[x] and D words are independent of z.

**Lemma 2 (A2 is affine in z).** Rho/pi sends lane 0 to position 0 (row 0,
rotation 0) and lane 5 to position 16 (row 3, x = 1, rotation 36). Chi acts on
each row as A'[x] = B[x] XOR (NOT B[x+1] AND B[x+2]); rows 0 and 3 each contain
exactly one varying input, so no AND multiplies two varying inputs, and with c
a group constant v -> (NOT v) AND c and v -> (NOT c) AND v are affine in v.
Iota and round-2 theta are affine. So A2(z) = A2(0) XOR sum_j z_j L_j exactly,
with fixed vectors L_j depending on the group.

**Lemma 3 (62-word support).** Let j' = (j + 36) mod 64. The round-1 output
varies only in bit j of lanes 0, 3, 4 and bit j' of lanes 15, 16, 19. The
changed column parities are C[0] at j and j', C[3] at j, C[4] at j and j', and
C[1] at j'. Since C[c][b] enters D[c+1][b] and D[c-1][b+1], the D words that
can change are (x, b) = (1,j), (4,j+1), (1,j'), (4,j'+1), (4,j), (2,j+1),
(0,j), (3,j+1), (0,j'), (3,j'+1), (2,j'), (0,j'+1) (bits mod 64): 12 pairs,
60 words P(x+5y, b). Four of the six directly varying bits lie among them; the
other two, (3,j) and (19,j'), make 62. L_j vanishes outside this fixed list
SUPPORT_j, and Gray order gives A2(gray(t)) = A2(gray(t-1)) XOR L_{ctz(t)}.

### 3.1 Which rounds vanish, and the last-round early abort

- Round 1 and round-2 theta are paid per group (Lemmas 1-2).
- Round 2 onwards is not affine in z (participant-side check, not shipped:
  33 of 44 random pairs (e_j, e_k) give a nonzero second derivative of the
  round-2 output). The program never assumes it; round 2 is differenced
  exactly (Lemma 7).
- **Round 5 (last) early abort.** The digest is chi row Y = 0, X = 0..3 of
  round 5. It reads B(X, 0), X = 0..4, whose pi sources are the diagonal lanes
  0, 6, 12, 18, 24 of the theta'd round-4 output. Round-5 theta needs all 25
  lanes of the round-4 output, but only through column parities, which are
  formed in registers while round 4 runs. So round 4 stores only the 5
  diagonal lanes (theta'd, Lemma 6) and round 5 computes 4 x 64 planes.

## 4. Bitsliced Keccak and the exact rewrites

**Lemma 4 (bitsliced round).** With pisrc(X, Y) = (x, y), y = X,
x = 3(Y - 3X) mod 5, the round on planes is: theta C[x][b] = XOR_y P(x+5y, b),
D[x][b] = C[x-1][b] XOR C[x+1][b-1], A'(L, b) = P(L, b) XOR D[x][b]; rho/pi
B(X, Y, b) = A'(L, (b - RHO[L]) mod 64), L = x + 5y; chi P'(X+5Y, b) =
B(X,Y,b) XOR (NOT B(X+1,Y,b) AND B(X+2,Y,b)); iota complements P'(0, b) for
each bit b of RC[r]. Every operation is bitwise, so in bit position p it is
exactly the scalar round of message p.

**Lemma 5 (transpose).** For d in {1, 2, ..., 128} let M_d have bit c set iff
c AND d = 0. The delta swap of rows a = R[i], b = R[i+d] (i AND d = 0)

    t = a SHR d ; t = t XOR b ; t = t AND M_d ; u = t SHL d ; a = a XOR u ; b = b XOR t

(6 operations) exchanges entries (i, c+d) and (i+d, c) for every c with
c AND d = 0. Stage d (128 swaps) swaps bit log2(d) of the row index with the
same bit of the column index. The 8 stages act on different index bits and
commute; together they transpose. v2 runs stages 1, 2, 4, 64, 128 in
registers on the 32 rows 64x + 8g + bl (x < 4, bl < 8) produced by the last
round for planes 8g..8g+7, and stages 8, 16, 32 on the 8 rows 64x + 8i + bl
(i < 8) of each of the 32 groups (x, bl). Row index bits {0,1,2,6,7} and
{3,4,5} are exactly the bits each phase swaps, so each phase is closed on its
row sets. After both phases, row p is the key of slot p; phase 2 group (x, bl)
yields slots 64x + 8i + bl = decode_slot(8(8x + bl) + i), which is the
processing order of Section 2.

### 4.1 Theta at store (Lemma 6)

**Lemma 6.** Let O be a round's chi output. The next round needs
O'(L, b) = O(L, b) XOR D[x][b] with D[x][b] = C[x-1][b] XOR C[x+1][b-1]. The
program produces O plane by plane (b = 0..63), all 25 outputs of plane b in
registers. Then C[.][b] is 20 XORs, and for b >= 1, with C[.][b-1] kept from
the previous plane, D[.][b] is 5 XORs and is XORed into each output before its
store. For b = 0, C[.][63] is not yet known: plane 0 is stored without D, and
after plane 63 the five words fix[x] = C[x-1][0] XOR C[x+1][63] are kept in
registers. In the next round each input word read from plane 0 of lane L
(there is exactly one such read per lane) gets fix[x(L)] XORed in after the
load. So every input of the next round is theta'd, with no D loads or stores.

### 4.2 Incremental round 2 (Lemma 7)

Let O2(z) = theta_3(iota(chi(pi(rho(A2(z)))))), the theta'd round-2 output
(the round-3 input), built at setup and kept across z-steps.

**Lemma 7.** A Gray step on z-bit j changes A2 by c_k = COEF[j][k] on the
62 words SUPPORT_j[k]. Their images under rho/pi are 62 words B(X, Y, b)
lying in 60 chi rows (Y, b); 58 rows have one changed input and 2 rows have
two (for every j, a structural fact of the fixed position lists). For a row
with one changed input B[k] -> B[k] XOR c, chi's output difference is exactly

    dO[k] = c,  dO[k-1] = c AND B[k+1],  dO[k-2] = (NOT B[k-1]) AND c,

(the other two outputs are unchanged; B[k+1] and B[k-1] are unchanged inputs).
For the two rows with two changed inputs the program loads the 5 old words,
forms the new ones, and computes dO[X] = (new[X] XOR old[X]) XOR
(NOT new[X+1] AND new[X+2]) XOR (NOT old[X+1] AND old[X+2]) for each affected X.
Iota cancels in differences. Theta is linear, so

    dC2[x][b] = XOR_Y dO(x+5Y, b),  dD3[x][b] = dC2[x-1][b] XOR dC2[x+1][b-1],
    O2(L, b) ^= dO(L, b) XOR dD3[x][b]   for all (L, b) where this is not structurally 0.

Which terms can be nonzero is fixed by j; the others emit no code. A2 is
updated too (the next step's differences read it). No property of the data
is assumed. Planes are processed cyclically from a plane whose predecessor
has no dC2, so dC2[.][b-1] is always in registers.

### 4.3 Lane-complement chi (Lemma 8)

Each stored word s of lane L holds v XOR pol(L)*ONES, with a polarity bit
pol(L) fixed per lane and round (a compile-time constant; uniform over the
64 planes). In a chi row, NOT b AND c equals s_b AND s_c if
(pol_b, pol_c) = (1, 0) (true polarity), and equals NOT(s_b OR s_c) if
(0, 1) (so s_b OR s_c is the term in polarity 1). Otherwise one input gets a
complemented copy (one NOT, shared within the row). The output s_a XOR term
has a known polarity; one NOT corrects it if it differs from the wanted output
polarity. Iota is a flip of the true value of lane 0 on the planes where RC
has a 1, and is absorbed into the same polarity bookkeeping. For each row
pattern the program uses the cheapest of the 32 x 8^5 choices
(`solve_row`, a compile-time search). With polarity pattern P34 = 1336081
(bit L = pol(L)) for the outputs of rounds 2 and 3 and P5 = 1188625 for
round 4, every chi row of rounds 3 and 4 costs exactly one NOT (the plain
form costs five), and the last round costs none: its output polarity per
plane is free, and the resulting fixed mask is KEYMASK (low 64 bits
0xffffffffffff7f74, other bits 0).

Theta commutes with the encoding. A column parity of stored words is the true
parity XOR a constant, so the stored D differs from the true D by a constant
pattern per column, and the theta'd stored words carry the polarity
fpol(P)(L) = P(L) XOR pc(x-1) XOR pc(x+1), with pc(x) the parity of P over
column x. Rho/pi only move lanes, and the polarity moves with them. The XOR
updates of Lemma 7 are differences, which do not depend on the encoding; A2 is
uncomplemented. So every round input is known in a known encoding, and the
last round yields K = D XOR KEYMASK. This is exact; the polarity search
depends on no data.

## 5. The algorithm and its counted program

### 5.1 Batch setup (once per batch of 2^40 messages)

1. Draw 512 random words (RAND); store each to PREF + 512*beta + 2p + w
   (register address, ADD) and to STATE0 + 256w + p; transpose (Lemma 5);
   store the 1088 padding planes; round-1 D words by loads.
2. Round 1 to STATE1 with round-2 D words; A2 = STATE1 XOR D. For j = 0..31:
   complement P(0, j), P(5, j), rerun round 1 with the same D (Lemma 1),
   store COEF[j][k] = (STATE1 XOR D) XOR A2 on SUPPORT_j, restore.
3. O2 = theta_3(round 2(A2)) in encoding fpol(P34) (Lemmas 6, 8), plane-0 fix
   applied in memory. Set s = t = 0.

Counted: 483,643 operations per batch (675,265 with the extra charges of
Section 9). With batch-loop control this is below 2^20, i.e. < 2^-20 per
message. The run starts with n = 0 at beta = 0.

### 5.2 Per z-step program (fully unrolled)

Persistent registers: s (= t), n (message number), SB = SBASE, ONE = 1.
Other registers are allocated per block (at most 56 live in total).

    (a) control, t >= 1 (16 ops): s = s + ONE; a 5-level branch tree on
        ctz(s) with 32 duplicated leaves (no indirect jump): v = s AND
        ((2^sh - 1) << j0); c = (v == 0); branch, for sh = 16, 8, 4, 2, 1.
    (b) Gray block j (4,149 ops; identical count for every j): Lemma 7.
        62 COEF loads; A2 load, XOR, store on the 62 support words; for the
        58 one-change rows 2 neighbour loads, 1 NOT, 2 AND; the 2 two-change
        rows as in Lemma 7; dC2/dD3 by XORs in registers; O2 load, XOR(s),
        store on the touched words; jump to (c).
    (c) R3 = ROUND(O2 -> ST0, all 25 lanes, RC[2], P34)        ; round 3
        R4 = ROUND(ST0 -> ST1, diagonal lanes only, RC[3], P5)   ; round 4
    (d) LAST(ST1) fused with transpose stages 1,2,4,64,128 -> ROWS
    (e) for each of 32 groups: 8 row loads, stages 8,16,32, SPARSE on 8 keys
    (f) c = (s < 2^32 - 1); branch                               ; next t or next batch

ROUND(src -> dst, LANES, rc, pattern), input already theta'd except plane 0,
whose fix words fin[0..4] are in registers (none for round 3):

    for b = 0..63:
      for Y = 0..4:
        for X = 0..4: B[X] = LOAD [src + 64L + b'] ; if b' = 0 and fin: B[X] ^= fin[x]
        chi row (Lemma 8): 1 NOT, then per X: t = B AND/OR B ; o[X+5Y] = B XOR t
      C[x] = o[x] ^ o[x+5] ^ o[x+10] ^ o[x+15] ^ o[x+20]                (20 XOR)
      if b >= 1: for x: d = C[x-1] ^ Cprev[x+1] ; for L in column x and LANES: o[L] ^= d
      for L in LANES: STORE [dst + 64L + b] = o[L]
    fout[x] = C0[x-1] ^ C63[x+1]                                        (5 XOR)

Round 3: per plane 25 loads, 55 chi ops, 20 parity XORs, 5 D XORs and 25
theta XORs (b >= 1), 25 stores: 63*155 + 125 + 5 = 9,895. Round 4 stores 5
lanes: 63*115 + 105 + 25 (fix) + 5 = 7,380.

LAST(ST1): for each plane b, 5 diagonal loads (+ the 5 fix XORs once), chi
row 0 outputs X = 0..3 with no NOT (8 ops) into register R[x, b mod 8]; after
8 planes, stages 1,2,4 (row bits of b) and 64,128 (row bits of x) on the 32
registers (5 x 16 swaps x 6), 32 stores to ROWS. Total 5 MOVI + 64*13 + 5 +
8*(480 + 32) = 4,938. Phase 2 (e): 3 MOVI + 32*(8 loads + 72) = 2,563, plus
256 sparse steps of at most 11 = 2,816: 5,379.

SPARSE(K), message number n (the Briggs-Torczon variant of Section 5.4):

    h = K SHR 116 ; a = h + SB ; i = LOAD [a] ; c = (i < n) ; branch
    if c: k2 = LOAD [i] ; c = (k2 == K) ; branch ; if c: MATCH (i, n)
    STORE [n] = K ; STORE [a] = n ; n = n + ONE

DK[n] lives at address n, so the stored index is the message number.
Paths: invalid pointer then insert, 8; valid pointer, different key, then
insert, 11 (the worst); match, 8, then verification.

**Ledger (one z-step, worst path: every message on the 11-op path; all Gray
blocks cost the same).** Counts are from the simulator (Section 10.1).

| block | ops |
| --- | ---: |
| (a) control | 16 |
| (b) incremental round 2 + jump | 4,149 |
| round 3 (theta'd input, lane-complement chi, theta at store) | 9,895 |
| round 4 (25 chi outputs for parities, 5 diagonal lanes stored) | 7,380 |
| round 5 rows fused with transpose stages 1,2,4,64,128 | 4,938 |
| transpose stages 8,16,32 + 256 sparse steps | 5,379 |
| (f) loop test | 2 |
| **total per 256 messages** | **31,759** |

By opcode: 5,112 direct and 512 register loads, 3,328 direct and 512
register stores, 13,098 XOR, 3,019 AND, 1,600 OR, 716 NOT, 1,024 SHL, 1,280
SHR, 513 ADD, 518 compare, 519 branch, 8 MOVI. That is 124.0586 per message.
The previous version (ae9a4286) needed 48,451 for the same 256 messages.

### 5.3 Verification and halting

On the first MATCH (i, n): decode both numbers: beta = id >> 40,
t = (id >> 8) mod 2^32, z = t XOR (t >> 1), q = id AND 255,
p = decode_slot(q) (at most 30 operations). Load both prefixes from
PREF + 512*beta + 2p + w (at most 12) and rebuild both messages (at most 40).
If they are equal (only in event F3), halt with failure. Otherwise evaluate
both with two reference permutations (2 units), compare the 256 digest bits
(at most 20) and output the pair. This is under 2 units + 200 operations;
we charge 3 units.

### 5.4 Sparse set (variant of jaazinn's)

S has 2^140 words at SBASE and is never initialised; garbage is never
trusted. DK[m] (address m) holds the key of message number m for every
m < n, since every processed message writes it. A pointer i = S[h] is used
only if i < n; then DK[i] is a genuine earlier key, and a MATCH is declared
only if it equals K in all 256 bits. On every non-match, S[h] is overwritten
with n. So after message a with top bits h is processed, S[h] points to a
until a later message with the same top bits is processed. A false MATCH is
impossible, and an equal key found through a garbage pointer i < n is still a
genuine collision of messages i and n.

## 6. Correctness (unconditional)

- **Evaluator exactness.** Lemmas 2-3 make A2 exact at every t. Lemma 7
  makes O2 exact at every t (by induction from setup). Lemmas 4, 6 and 8 make
  rounds 3-5 exact in the stated encodings. Lemma 5 makes K = D XOR KEYMASK
  for the slot of Section 2. The simulator (Section 10.1) and the
  organizer-executed experiments (Section 10.2) check this.
- **Outputs.** Any output is two distinct messages with equal full digests
  under two reference permutations.

## 7. Success probability

The run halts at the first MATCH. Failure events:

- **F3**: two groups produce the same message, i.e. P_g XOR P_g' is one of
  the 2^32 values ins(z) XOR ins(z'). Pr[F3] < 2^191 * 2^32 / 2^512 = 2^-289.
  Without F3 all N messages are distinct.
- **F1**: no two of the N messages have equal digests.
- **F2**: some colliding pair (a, b), a processed before b, has a message c
  processed between them with the same top 140 key bits and a different key
  (c overwrites S[h], so b does not find a).

If none occurs, take the colliding pair (a, b) whose b is processed first.
After a is processed, S[h] = a until a message with the same top bits comes.
Without F2, every such message processed before b has key(a) and so itself
matches (a MATCH no later than b), or there is none and b reads S[h] = a and
matches. So Pr[fail] <= Pr[F1] + Pr[F2] + Pr[F3]. (Version 1 kept the oldest
key per bucket and discarded the newer; the event and its bound are the same.)

**Heuristic H1 (declared; identical text in claim.json).** For the failure
events F1 and F2 (Section 7), the 2^128 keys of the grouped message set
{m(g, z)} (independent uniform prefixes P_g, all z in {0,1}^32, processed in
any fixed order chosen independently of the digests, in particular the order
of Section 2: batch by batch, t = 0..2^32-1 with z = gray(t), slots
p = decode_slot(q) for q = 0..255) behave like N independent uniform 256-bit
values, i.e. Pr[F1] <= exp(-N(N-1)/2^257) and Pr[F2] <= N^3/6 * 2^-396.

Under H1:

- Pr[F1] <= exp(-N(N-1)/2^257) = exp(-(1 - 2^-128)/2) < 0.6065307.
- Pr[F2] <= (number of ordered triples a < c < b) * 2^-256 * 2^-140
  <= N^3/6 * 2^-396 < 2^-14.5. We use 2^-13 < 0.0001221.
- Success >= 1 - 0.6065307 - 0.0001221 - 2^-289 > 0.39334. We claim 0.39,
  an allowance of 0.0033.

**Rigorous partial support.** For groups g != g' and any z, z', the messages
m(g, z), m(g', z') are independent and uniform on 64-byte strings, so by
Cauchy-Schwarz Pr[digests equal] >= 2^-256. Within-group pairs are a 2^-96
fraction of all pairs, so the expected number of colliding pairs is at least
(1 - 2^-96) * N(N-1)/2^257. H1 is needed for the second-moment behaviour
behind Pr[F1] and for F2 (jaazinn's argument).

**v2 does not change the message set or any digest.** Batching fixes only the
processing order, a function of (beta, t, q), never of digests; bitslicing,
incremental round 2, theta at store and lane complementing change how a
digest is computed, not its value (Section 6).

## 8. Time bound

Per message the charge is 31,759/256 = 124.0586 plus amortised setup
(< 2^-20) plus a spare of 0.0014: 124.06 operations = 124.06/1355 units. It
covers the Gray and incremental round-2 update, rounds 3-5, both transpose
phases, every table load, store, compare and branch, and all loop control.
The only other cost is verification (< 3 units, at most once). So

    T <= 2^128 * 124.06/1355 + 3 = 0.0915572... * 2^128 + 3 < 2^124.55082.

The claimed time_log2 is **124.551**, rounded up. The bound holds for every
run (no restarts). preprocessing_log2 = 0: setup is per batch and inside T.

On this track as of 2026-10-06 03:09Z (scored entries, all in review): ours
v1 125.551 (ae9a4286), tekkac 126.99, Subflatus3 126.99, ercumentyildirim
127.12.

## 9. Sensitivity of the bound to conventions

| variant | ops / z-step | ops/message | time_log2 |
| --- | ---: | ---: | ---: |
| as claimed: every executed primitive, all loads/stores | 31,759 | 124.06 | 124.551 |
| + one address ADD per direct load/store, + one MOVI per ALU immediate (v1's claimed convention) | 40,210 | 157.08 | 124.892 |
| the same, also + one per shift amount | 42,514 | 166.08 | 124.972 |
| two extra ops per direct access and per immediate | 48,661 | 190.09 | 125.167 |
| (not claimed) logic gates only, loads/stores free | 18,433 | 72.01 | 123.766 |

Every claimed-type variant is below 125.551 (our v1) and 126.99. The register
budget is 56 of 64; a machine with fewer registers would need spills, which
we do not price.

## 10. Evidence

### 10.1 Counted simulator (participant evidence)

The program of Section 5 runs on a counted 256-bit word-RAM simulator with an
explicit 64-register file that counts every primitive. Uninitialised memory
reads 0 in even batches and random garbage in odd ones.

- 16 batches x 4 z-steps x 256 = 16,384 keys; batch 0 starts at t = 0,
  batch 1 crosses t = 2^31 (ctz 31), the others start at random t. Every key
  equals int.from_bytes(sha3_256(m, 5), "little") XOR KEYMASK from
  `verifier/keccak.py`: 0 mismatches. A second run, 32 batches x 8 z-steps
  (65,536 keys): 0 mismatches. Register high-water mark 56.
- Every Gray block j = 0..31 once, plus 40 consecutive steps from t = 0 (the
  incremental O2 accumulating over many steps): 17,024 keys, 0 mismatches;
  every block costs exactly 4,149.
- Every stored DK[n] equals the key of the message n decodes to. A scalar
  recomputation of A2(e_j) XOR A2(0) (4 groups, j = 0, 5, 17, 31) is 0
  outside SUPPORT_j and equals COEF inside.
- The ledger of Section 5.2 is the simulator's per-block count of one
  worst-path z-step (all 256 messages on the 11-op path). Replaying a z-step
  gave 256 MATCHes, each pairing a message with the same (beta, slot, z) one
  z-step of numbering earlier.
- Re-checks during our internal review, with coins drawn afresh: 12 batches
  x 6 z-steps (18,432 keys, 0 mismatches, all 18,432 stored keys decode
  from their message number); 600 consecutive z-steps from t = 3*2^20 - 300
  (ctz up to 20; 4,200 keys checked, 0 mismatches; the incrementally
  updated O2 equals a fresh recomputation at every 100th step); 4,608 more
  keys and another full j = 0..31 pass (0 mismatches). The experiment
  evaluator of Section 10.2 was also compared with `sha3_256(m, 5)` on
  20,480 keys (random prefixes, crossing t = 2^31, 40 consecutive steps):
  0 mismatches.

### 10.2 Declared experiments (organizer-executed, `python-message-pairs-v1`)

All four experiments use `experiments/s3r5_bitslice_birthday.py`, which
implements the v2 evaluator: per-batch A2, COEF and O2 from bitsliced
rounds 1-2; the Gray update with the incremental round 2 of Lemma 7 (O2 is
never recomputed between z-steps); rounds 3 and 4 with theta applied before
the store and lane-complemented chi with the same polarity patterns; the
row-0 last round with KEYMASK; the transpose in the program's stage order;
messages offered in the processing order of Section 2. Every digest used for
matching comes from that evaluator. Each organizer seed derives fresh 64-byte
group prefixes with SHA-256. N_t = 2^9 messages and an 18-bit mask give
N_t^2/2^18 = 1 = N^2/2^256; the uniform-model success probability is
0.39307 (100.6 successes per 256 trials, sd 7.8). Trials sharing a batch own
disjoint bit positions, and no operation mixes positions. Every trial checks
5 keys (the first 4 in processing order and its last key at the last,
Gray-updated z) at full width against an independent direct sponge, the
support of each coefficient column, and, at the last z of each batch, O2
against a fresh recomputation; any failure aborts.

Layouts: `k5r5-bs-full-width` 256 groups x 2; `k5r5-bs-spread` 16 x 32;
`k5r5-bs-single-group` 1 x 512 (strongest within-group structure);
`k5r5-bs-high-z` 4 x 128 with z = gray(t) << 25 (for j >= 27 the support
wraps around the lane). Ids, masks and seed derivation are unchanged from
version 1, so the digests are the same and only the evaluator differs.

### 10.3 Local runs (not organizer evidence; all runs reported)

Organizer-runner replay (`experiments/runner.py` with a subprocess executor
in place of Docker, track config hash, seed `hashsmash-public-seed-v1`, 256
trials), run twice with byte-identical stdout, 1.4-4.2 s per run, every pair
re-checked with `verifier`, all 1,280 exactness checks per experiment passed:

| experiment | successes / 256 | z (model 100.6, sd 7.8) | masked pairs (exp. 127.8) |
| --- | ---: | ---: | ---: |
| k5r5-bs-full-width | 89 | -1.5 | 107 |
| k5r5-bs-spread | 82 | -2.4 | 98 |
| k5r5-bs-single-group | 107 | +0.8 | 145 |
| k5r5-bs-high-z | 98 | -0.3 | 128 |

These equal version 1's replay trial by trial (same success set and pair
counts), as they must: digests are unchanged and a trial's success does not
depend on the processing order. The spread layout was -2.4 sd already in
version 1; seeds, tags and masks were not changed. The 8,192-trial local runs
of version 1 (seeds `r5-b1`, `r5-b2`, fixed in advance), rerun with the v2
program, are identical to version 1 (model 3220.1 +- 44.2 per batch):

| layout | batch 1 | batch 2 | pooled | pooled z | pairs (exp. 8176) |
| --- | ---: | ---: | ---: | ---: | ---: |
| full-width | 3254 (+0.8) | 3329 (+2.5) | 6583 | +2.3 | 8339 |
| spread | 3247 (+0.6) | 3219 (-0.0) | 6466 | +0.4 | 8250 |
| single-group | 3240 (+0.5) | 3207 (-0.3) | 6447 | +0.1 | 8205 |
| high-z | 3243 (+0.5) | 3264 (+1.0) | 6507 | +1.1 | 8329 |

We also ran both evaluators on one extra local seed (`cmp1`, 256 trials per
layout): identical successes 112, 112, 92, 97 (z = +1.5, +1.5, -1.1, -0.5)
and pair counts. A participant-side check of the v2 experiment evaluator
against `sha3_256(m, 5)` on all 256 slots of 3 batches over 64 Gray steps
(16,384 keys, z bits 0..5, 20..23 and 25..28) found 0 mismatches.

Internal-review replays (organizer runner as above, 256 trials, coins
drawn afresh after the runs above; every run made is listed, no
self-check failed, every returned pair re-checked with `verifier`):

| seed | full-width | spread | single-group | high-z |
| --- | ---: | ---: | ---: | ---: |
| cmt-fresh-1006 | 108 | 100 | 94 | 93 |
| fresh-review-coin-20261006-a | 80 | 100 | 99 | 108 |
| rv-coin-b | 85 | 107 | 105 | 110 |
| rv-coin-c | 91 | 98 | 109 | 94 |
| rv-coin-d | 103 | 107 | 110 | 99 |
| rv-coin-e | 87 | 94 | 90 | 85 |
| rv-coin-f | 99 | 112 | 103 | 114 |
| rv-coin-g | 104 | 96 | 100 | 96 |
| rv-coin-h | 74 | 102 | 107 | 100 |
| rv-coin-i | 104 | 105 | 101 | 86 |
| total / 2,560 (model 1,006.3 +- 24.7) | 935 (-2.9) | 1,021 (+0.6) | 1,018 (+0.5) | 985 (-0.9) |

The full-width total is low: 827 of 2,304 (-3.4 sd) over the nine seeds
`fresh-review-coin-20261006-a` and `rv-coin-b..i`, with a lowest cell of 74
(rv-coin-h, -3.4 sd per cell). **After seeing this**, we ran 40 more
full-width seeds (`ext-0-0` .. `ext-7-4`, 256 trials each, same harness
calling the experiment program directly with the runner's seed derivation):
4,035 of 10,240 (+0.2 sd; per seed 85 to 115). These were chosen after the low
value was seen, so they are reported separately and not as a planned test.
Over all 50 fresh full-width seeds: 4,970 of 12,800 (-1.1 sd). Pooled over
every run listed in this section (29,696 full-width trials and 19,456 for
each other layout), the z-scores are +1.0 (full-width), +0.5 (spread), +0.2
(single-group) and +0.6 (high-z). The largest deviations of any reported
series are the -3.4 of these nine full-width seeds and the +2.3 of the
pooled full-width 8,192-trial batches above, in opposite directions.

**Direct within-group check (version 1 evaluator; digests identical).**
1,024 batches x 256 groups x 32 pairs (z = 0, z = e_j, j = 0..31), 8,388,608
pairs: the four experiment masks matched 34, 35, 37 and 33 times (32.0
expected each; 139 in total against 128 +- 11.3). The full digest difference
had mean Hamming weight 128.00 and minimum 87 (about 86-87 expected).

## 11. Memory

| array | 32-byte words | bytes |
| --- | --- | --- |
| S | 2^140 | 2^145 |
| DK (addresses 0..2^128) | <= 2^128 | <= 2^133 |
| PREF | 2^97 | 2^102 |
| state, A2, O2, ROWS, COEF | < 2^13 | < 2^18 |
| code (unrolled z-step, 32 Gray blocks, setup) | < 2^20 instructions | < 2^25 |

Total < 2^145.01 bytes; we claim 146. Memory is reported only.

## 12. Limitations

- H1 is a heuristic. It extends the grouped structure from the tested scale
  (N_t = 2^9, 18-bit masks) to N = 2^128 and the full key. Organizer seeds are
  public. A 256-trial experiment resolves the success frequency only to about
  +-0.03, and the 0.0033 allowance is not statistically certified. Only four
  nonlinear layers follow the affine A2.
- Within a group the digest has degree at most 16 in z, so it sums to zero
  over every 17-dimensional affine subspace of z (participant check: two
  17-cubes give zero, a 15- and a 16-cube do not); no experiment varies more
  than 9 z bits. This concerns only within-group pairs (a 2^-96 fraction); we
  see no route to clustering of cross-group collisions, but H1 assumes none.
- The gain comes from operation-level pricing (bitslicing, grouping). All
  executed work, including every memory access, is charged; the 64-register
  machine is an assumption (56 used); instruction fields (constant
  addresses, immediates, shift amounts) are priced only in Section 9.
- No sub-birthday attack, collision certificate or full-scale run is claimed.

## 13. Credit

As in Section 0: **jaazinn** and **may93182** (co-authors in that sense),
the Keccak team and **tekkac**, **ercumentyildirim**, **zeeshan8281**,
**mitchuski**. Errors are ours.
