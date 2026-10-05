# sha3-256-r5: bitsliced grouped birthday search, time_log2 = 125.551

## 0. Summary and credit

A generic birthday search over full 256-bit digests; no cryptanalytic
weakness of SHA3 is claimed. Two known implementation ideas are combined:

- **Grouping** (jaazinn's framework): messages come in groups of 2^32 that
  share a random prefix. Inside a group, the round-2 theta output A2 is an
  exactly affine function of the 32-bit group counter z (Lemma 2). So round 1
  and the linear part of round 2 are paid once per group, not per message.
- **Bitslicing** (may93182's 256-message bit-plane Keccak): each 256-bit word
  holds one state bit of 256 messages. Rotations become renamings of word
  addresses, and an explicitly priced delta-swap transpose produces the
  per-message digests.

We evaluate a *batch* of 256 groups, one per bit position, at a common z. A
z-step is one counted straight-line program that evaluates 256 messages. Its
worst path is 48,451 operations. Charging one extra address addition for each
of its 14,360 direct-address loads and stores and one extra MOVI for each of
its 12 ALU immediates (Section 1) gives 62,823, or 245.40 per message. Of the
five rounds, round 1 and the theta of round 2 are paid per group, rounds 2-4
run bitsliced (round 4 storing only the five lanes the last round reads), and
round 5, the last, computes only the 256 digest bits (Section 3.1).

| quantity | value |
| --- | --- |
| messages N | 2^128 = 2^88 batches x 256 groups x 2^32 values of z |
| ops per z-step (256 messages), worst path | 48,451 counted; 62,823 charged |
| charged ops per message | 248 (245.40 + setup < 2^-20 + spare) |
| total T | <= 2^128 * 248/1355 + 3 < 2^125.55012 |
| claimed time_log2 | **125.551** |
| success probability | >= 0.39334 under H1; claimed 0.39 |
| memory | < 2^145.01 bytes; claimed 146 |

**Credit.** **jaazinn** (Yukon ticket 0a5b7ae8, blake3-r2, in review)
originated grouped partial evaluation, the Briggs-Torczon sparse set on the top
140 key bits, the F1/F2/F3 analysis with heuristic H1 and the scaled-experiment
design, and is named as co-author in that sense. **may93182** introduced on
the sha3-256-r6 track the 256-way bit-plane Keccak (rotations as plane renaming) and the
8-stage delta-swap transpose at 6 operations per row pair (sha3-256-r6
submission 11c46f4d, 126.995, in review); we reuse both, and may93182 is likewise named as co-author in that sense (as on our sha3-256-r6 package). Neither has reviewed
this package, nor has ercumentyildirim (below). It is the five-round port of our sha3-256-r6 package (ticket
377eebd5, in review): same program, accounting and heuristic, one full round
shorter. Ours: the SHA3 column pairing and affine reduction (Lemmas 1-2), the
62-word Gray support (Lemma 3), the fused round forming the next D words in
the same pass, the bitsliced digest-only last round written into transpose
rows (the scalar last-round early abort was published on this track by
ercumentyildirim, 4c969300; Section 8), the register-blocked transpose
feeding the sparse set, and the counted program.

## 1. Target, machine and charging conventions

- Target `sha3-256-r5-prefix-v1`: the complete SHA3-256 sponge (rate 1088,
  capacity 512, suffix 0x06, pad10*1, zero IV), the first five Keccak rounds
  (rounds 1..5 in our numbering, constants RC[0..4]) and all 256 output bits,
  as in `verifier/keccak.py:sha3_256(msg, 5)`.
  Messages are exactly 64 bytes, so there is one block. Lane k (k < 8) is
  bytes 8k..8k+7 read little-endian. Lane 8 = 0x06, lane 16 = 0x80 << 56, and
  the other lanes are 0. Lane index is L = x + 5y.
- Digest = lanes 0..3 after round 5, little-endian. The key is
  K = int.from_bytes(digest, "little"), so bit k of K is bit k mod 64 of
  digest lane floor(k/64), with iota of round 5 included. Equal digests and
  equal keys are the same event.
- Cost model `collision-frontier-v5`, C = 1355. One five-round permutation
  costs 1 unit and any other primitive costs 1/1355. Machine: a 256-bit word RAM with 64
  registers. The register count is our assumption; v5 specifies only the
  word RAM, and the program never uses more than 48 registers.
- Every executed primitive costs 1: load, store, XOR, AND, NOT, shift, add,
  compare, conditional branch, immediate move and random word. No indirect
  jump is used. Most addresses are constants of the unrolled program (direct
  addressing). Table accesses (S, DK, DI, PREF) use a register address formed
  by an explicit counted ADD of a base held in a register. **The claimed bound
  also charges one additional address addition to every direct-address load
  and store, and one additional MOVI to every ALU instruction with a constant
  operand** (AND/XOR/compare with an immediate: 12 per z-step, all in
  control). So no address or constant generation is free under either
  reading. Shift amounts are part of v5's "shift or rotation" primitive;
  Section 9 also prices them, and gives the count without any extra charge.
- No rotation is ever executed. In the bitsliced layout, rho and theta's
  rot-by-1 are fixed renamings of word addresses (Lemma 4).

## 2. Messages, groups, batches and the bit mapping

For group g the algorithm draws two fresh uniform 256-bit words R0, R1. Their
little-endian bytes form a uniform 64-byte prefix P_g, which is stored. For
z in {0,1}^32:

    m(g, z) = P_g with LE32(z) XORed into bytes 0..3 and into bytes 40..43,

so z is XORed into the low 32 bits of lane 0 (x=0, y=0) and of lane 5
(x=0, y=1). Write g = 256*beta + p, with batch index beta < 2^88 and bit
position (slot) p < 256. Batch beta runs t = 0, 1, ..., 2^32 - 1 with
z = gray(t) = t XOR (t >> 1). At each t it evaluates the 256 messages
m(256*beta + p, gray(t)), p = 0..255, and offers them to the table in slot
order p = r + 32i (r = 0..31, i = 0..7). Batches run in order beta = 0, 1, ....
Every message is evaluated exactly once, and N = 2^88 * 256 * 2^32 = 2^128.

**Bit mapping.** The word P(L, b), for lane L and bit b, holds in bit
position p the bit b of lane L of message m(256*beta + p, z). Prefix words:
row p of input matrix w (w = 0, 1) is the word R_w of slot p. Its bit k is
bit k mod 64 of lane 4w + floor(k/64). After the transpose (Lemma 5), row k of
matrix w is the plane P(4w + floor(k/64), k mod 64). Padding planes are
constants: P(8,1) = P(8,2) = P(16,63) = all-ones, and all other planes of
lanes 8..24 are 0.

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
vectors L_j (depending on the group). This is plain algebra, with no
probability involved.

**Lemma 3 (62-word support).** Let j' = (j + 36) mod 64. The round-1 output
varies only in bit j of lanes 0, 3, 4 (row 0: B[0] enters out[0], out[4],
out[3]) and in bit j' of lanes 15, 16, 19 (row 3: B[1] enters out[1], out[0],
out[4]). The changed column parities are C[0] at j and j', C[3] at j, C[4] at
j and j', and C[1] at j'. Since C[c][b] enters D[c+1][b] and D[c-1][b+1], the
D words that can change are (x, b) = (1,j), (4,j+1), (1,j'), (4,j'+1), (4,j),
(2,j+1), (0,j), (3,j+1), (0,j'), (3,j'+1), (2,j'), (0,j'+1) (bits mod 64).
These are 12 distinct pairs and give 60 words P(x+5y, b), y = 0..4. Four of
the six directly varying bits, (0,j), (4,j), (15,j') and (16,j'), lie among
them. The other two, (3,j) and (19,j'), make 62. So L_j vanishes outside the
fixed list SUPPORT_j of 62 words. (Some of its words may also vanish for a
particular group; the program XORs all 62 regardless.) Gray order then gives
the update A2(gray(t)) = A2(gray(t-1)) XOR L_{ctz(t)}.

### 3.1 Which of the five rounds vanish, and the last-round early abort

- **Round 1 and round-2 theta: paid per group.** Lemmas 1-2 hold verbatim for
  five rounds (they concern only round 1 and round-2 theta). Per message only
  the Gray update of A2 remains.
- **Round 2 onwards is not affine in z.** Round-2 chi multiplies pairs of A2
  words that vary with different z bits. We checked this numerically: for
  one prefix, 33 of 44 random pairs (e_j, e_k) give a nonzero second derivative of the round-2 output,
  whereas A2 had zero second derivative for all 50 random pairs (a, b) tested.
  This check is participant-side and not shipped; it is informational only, since
  the program never assumes that round 2 is affine.
  So rounds 2, 3, 4 and the digest part of round 5 are computed per message,
  exactly as in the six-round program, which is one full round longer.
- **Round 5 (last) early abort.** The digest is lanes 0..3 of the round-5
  output, i.e. chi row Y = 0, X = 0..3. Those read B(X, 0) for X = 0..4, whose
  pi sources are the diagonal lanes 0, 6, 12, 18, 24 of the round-4 output
  (pisrc(X, 0) = (X, X)), after round-5 theta. Round-5 theta needs all 25
  lanes of the round-4 output, but only through the five column parities, and
  ROUND accumulates those in registers while it produces round 4. So round 4
  stores only the 5 diagonal lanes and the round-5 D words, and round 5
  computes 4 x 64 output planes (ROUND5 below). Omitted lanes never reach the
  digest, so no output bit changes; the simulator check of Section 10.1
  confirms this bit for bit against `sha3_256(m, 5)`.

## 4. Bitsliced Keccak and the transpose (exact)

**Lemma 4 (bitsliced round).** Write pisrc(X, Y) = (x, y) with y = X and
x = 3(Y - 3X) mod 5, the inverse of pi (B[y, 2x+3y] = rot(A[x,y], RHO[x,y])).
On planes the round is:

- theta: C[x][b] = XOR_y P(x+5y, b), D[x][b] = C[x-1][b] XOR C[x+1][b-1]
  (bit b of rot(C, 1) is bit b-1 of C), A'(L, b) = P(L, b) XOR D[x][b];
- rho/pi: B(X, Y, b) = A'(L, (b - RHO[L]) mod 64), with L = x + 5y and
  (x, y) = pisrc(X, Y);
- chi: P'(X+5Y, b) = B(X,Y,b) XOR (NOT B(X+1,Y,b) AND B(X+2,Y,b));
- iota: P'(0, b) = NOT P'(0, b) for each bit b set in RC[r].

Every operation is bitwise on 256-bit words, so it acts independently on
each bit position p. In position p it is exactly the scalar round on the lanes
of message p. By induction over rounds, the planes equal the transposed
scalar states. Rotations move no data. They only change which address is
read.

**Lemma 5 (transpose).** For d in {1, 2, ..., 128}, let M_d be the word whose
bit c is set iff c AND d = 0. A delta swap of rows a = R[i] and b = R[i+d]
(with i AND d = 0) is

    t = a SHR d ; t = t XOR b ; t = t AND M_d ; u = t SHL d ; a = a XOR u ; b = b XOR t

(6 operations). It exchanges entry (i, c+d) with (i+d, c) for every c with
c AND d = 0. Stage d applies it to all 128 such row pairs, which swaps bit
log2(d) of the row index with the same bit of the column index. The 8 stages
act on different index bits, so they commute. All 8 together turn entry (r, c)
into (c, r), the transpose. We run stages 1..16 inside blocks of 32
consecutive rows (phase 1), then stages 32, 64 and 128 on the 8 rows r, r+32,
..., r+224 for each r < 32 (phase 2). Each stage still costs 128 swaps.

## 5. The algorithm and its counted program

### 5.1 Batch setup (once per batch of 2^40 messages)

1. Draw 512 random words (RAND). Store each word to PREF + 512*beta + 2p + w
   (register address, incremented by ADD) and to STATE0 + 256w + p.
2. Transpose both 256 x 256 matrices in place (Lemma 5, storing phase 2). This
   gives the planes of lanes 0..7.
3. Store the 1088 padding planes (constants all-ones or 0).
4. Compute the round-1 D words of the input (parity by loads, D as in 5.2).
5. Run round 1 (ROUND below, all lanes) to STATE1 with the round-2 D words.
   Then A2(L, b) = STATE1(L, b) XOR D[x][b] for all 1600 words.
6. For j = 0..31: complement P(0, j) and P(5, j) of the input. The parities
   do not change (Lemma 1), so the step-4 D words are reused. Run round 1
   again. Store COEF[j][k] = (STATE1 XOR D) XOR A2 at the k-th word of
   SUPPORT_j (k < 62). Then restore the two planes.
7. Set s = t = 0 and IDZ = beta * 2^40 (z = 0).

Counted setup: 473,034 operations (661,406 charged); with batch-loop control
(increment beta, compare, branch, reset s) below 2^20, i.e. < 2^-20 per message.

### 5.2 Per z-step program (exact listing, fully unrolled)

Persistent registers are s (the step counter t), IDZ = beta*2^40 + z, IDM
(running id), n (the table size) and the constants SB = SBASE, DK = DKBASE,
DI = DIBASE, ONE = 1, K32 = 2^32 (set once per run). Other registers are
allocated per block (maximum 48 live, in transpose phase 1). For t = 0 the
step starts at (c).

    (a) control, t >= 1 (17 ops, 11 immediates): s = s + ONE ; then a 5-level
        branch tree on ctz(s) with 32 duplicated leaves (no indirect jump).
        A node with known low part j0 tests v = s AND ((2^sh - 1) << j0) ;
        c = (v == 0) ; branch, for sh = 16, 8, 4, 2, 1 (j0 += sh if c).
        Leaf j: IDZ = IDZ XOR 2^j (z ^= 2^j), then falls into Gray block j.
    (b) Gray block j (249): for k = 0..61, (L, b) = SUPPORT_j[k]:
          c = LOAD [COEF + 64j + k] ; w = LOAD [A2 + 64L + b] ; w = w XOR c ;
          STORE [A2 + 64L + b] = w
        jump to (c)
    (c) ROUND(A2, -, ST0, all, RC[1], DA)        ; round 2: A2 is already theta'd
        ROUND(ST0, DA, ST1, all, RC[2], DB)      ; round 3
        ROUND(ST1, DB, ST0, DIAG, RC[3], DA)     ; round 4, stores lanes 0,6,12,18,24
    (d) ROUND5(ST0, DA) -> ROWS                  ; round 5 (last): digest planes only
        IDM = IDZ AND IDZ                        ; q = 0
    (e) transpose phase 1 on ROWS ; phase 2 with SPARSE on each finished key
    (f) c = (s < 2^32 - 1) ; branch              ; next t, or the next batch

ROUND(src, Din, dst, LANES, rc, Dout). Here B[0..4], t, o, d, acc[0..4] and
prev[0..4] are registers, and "acc <-> prev" is a static renaming (no
instruction):

    for b = 0..63:
      for Y = 0..4:
        for X = 0..4:                            ; (x,y) = pisrc(X,Y), L = x+5y, b' = (b - RHO[L]) mod 64
          B[X] = LOAD [src + 64L + b']
          if Din: d = LOAD [Din + 64x + b'] ; B[X] = B[X] XOR d       ; theta
        for X = 0..4:
          t = NOT B[X+1] ; t = t AND B[X+2] ; o = B[X] XOR t            ; o is acc[X] when Y = 0
          if X + 5Y = 0 and bit b of rc: o = NOT o                      ; iota
          if X + 5Y in LANES: STORE [dst + 64(X+5Y) + b] = o
          if Y > 0: acc[X] = acc[X] XOR o                               ; C'[X][b]
      if b = 0: STORE [CSAVE + x] = acc[x]               (x = 0..4)
      else:     d = acc[x-1] XOR prev[x+1] ; STORE [Dout + 64x + b] = d  (x = 0..4)
      acc <-> prev
    for x = 0..4: d = LOAD [CSAVE + x-1] ; d = d XOR prev[x+1] ; STORE [Dout + 64x] = d

Per plane: 25 + 25 loads, 25 theta XORs, 75 chi ops, |LANES| stores, 20
parity XORs, and (b >= 1) 10 D ops; the next round's D words need no parity
pass. Counts: a full round is 64*195 + 63*10 + 5 + 15 + popcount(rc), which is
13,135 for round 3 (popcount(RC[2]) = 5). Round 2 (no theta loads or XORs) is
64*145 + 650 + 3 = 9,933. Round 4 (5 stores per plane, popcount(RC[3]) = 3) is
64*175 + 650 + 3 = 11,853.

ROUND5(src, Din) uses only output row Y = 0, whose sources are the diagonal
lanes 6X (Section 3.1):

    for b = 0..63:
      for X = 0..4: b' = (b - RHO[6X]) mod 64 ; B[X] = LOAD [src + 64*6X + b'] ;
                    d = LOAD [Din + 64X + b'] ; B[X] = B[X] XOR d
      for X = 0..3: t = NOT B[X+1] ; t = t AND B[X+2] ; o = B[X] XOR t ;
                    (X = 0 and bit b of RC[4]: o = NOT o) ; STORE [ROWS + 64X + b] = o

That is 64*31 + popcount(RC[4]) = 1,984 + 5 = 1,989 operations. Row k = 64X + b of ROWS is key bit k.

Transpose phase 1 is 5 MOVI (masks) plus 8 blocks of (32 loads, 5 stages x 16
swaps x 6, 32 stores), which is 4,357. Phase 2 is 3 MOVI plus 32 x (8 loads,
3 stages x 4 swaps x 6). After phase 2 for index r, register R[i] holds
row r + 32i of the transposed matrix. That is the key K of slot p = r + 32i
(Lemma 5), and it goes straight into SPARSE(K, p), with no store or reload.
Phase 2 with 256 worst-path sparse steps costs 3 + 2,560 + 256*17 = 6,915.

SPARSE(K, p), the Briggs-Torczon step on the top 140 key bits:

    h = K SHR 116 ; a = h + SB ; i = LOAD [a] ; c = (i < n) ; if !c goto INSERT
    e = i + DK ; k2 = LOAD [e] ; u = k2 SHR 116 ; c = (u == h) ; if !c goto INSERT
    c = (k2 == K) ; if c goto MATCH ; IDM = IDM + K32 ; goto NEXT  ; different key
    INSERT: e = n + DK ; STORE [e] = K ; e = n + DI ; STORE [e] = IDM ;
            STORE [a] = n ; n = n + ONE ; IDM = IDM + K32
    NEXT:

IDM = beta*2^40 + q*2^32 + z, where q = 8r + i is the processing index of slot
p = r + 32i (p = (q >> 3) + 32(q AND 7)). No immediate occurs on this path
apart from the shift amount. Path lengths: empty slot then insert, 12; stale
pointer (i < n, different top bits) then insert, 17 (the worst); occupied by a
different key, 14; match, 12, after which verification starts.

**Ledger (one z-step, worst path: ctz(t) = 31, every message on the 17-op
path).** "charged" adds one op per direct-address load/store and per ALU
immediate.

| block | ops | direct loads/stores + immediates | charged |
| --- | ---: | ---: | ---: |
| (a) control | 17 | 0 + 11 | 28 |
| (b) Gray update + return | 249 | 186 | 435 |
| round 2 | 9,933 | 3,530 | 13,463 |
| round 3 | 13,135 | 5,130 | 18,265 |
| round 4 (diagonal lanes stored) | 11,853 | 3,850 | 15,703 |
| round 5 digest rows | 1,989 | 896 | 2,885 |
| IDM reset | 1 | 0 | 1 |
| transpose phase 1 | 4,357 | 512 | 4,869 |
| transpose phase 2 + 256 sparse steps | 6,915 | 256 | 7,171 |
| (f) loop test | 2 | 0 + 1 | 3 |
| **total per 256 messages** | **48,451** | **14,360 + 12** | **62,823** |

By opcode: 9,291 direct and 512 register loads, 5,069 direct and 768
register stores, 16,511 XOR, 6,086 AND, 5,072 NOT, 1,024 SHL, 1,536 SHR, 1,537
ADD, 518 CMP, 519 branch, 8 MOVI: 189.26 per message, 245.40 charged.

### 5.3 Verification and halting

On the first MATCH: load DI[i] (2 operations). The new id is IDM. Decode
both ids beta*2^40 + q*2^32 + z, with p = (q >> 3) + 32(q AND 7) (at most 24
operations). Load both prefixes from PREF + 512*beta + 2p + w (at most 12).
Rebuild both messages (at most 40). If they are equal (only in event F3, as
each (beta, p, z) is processed once), halt with failure. Otherwise evaluate both with two reference
permutations (2 units), compare the 256 digest bits (at most 20), and output
the pair (at most 10). This is under 2 units + 200 operations, capped at
3 units.

### 5.4 Sparse set (as in jaazinn's package)

S has 2^140 words and is never initialised. Garbage is never trusted. Slot h
is valid iff S[h] < n and DK[S[h]] >> 116 = h. A key is inserted only into an
invalid slot, which the insertion makes valid, and entries are never
rewritten. So a valid slot holds exactly the first inserted key with top bits
h. Each message is compared with that key, if it exists. An equal key is a
MATCH. A different key means the message is discarded (event F2 below). An
invalid slot means insertion.

## 6. Correctness (unconditional)

- **Evaluator exactness.** Lemma 2 and Lemma 3 make A2 exact at every t. Lemma
  4 makes the rounds exact, and the D words of round r+1 are formed from the
  complete parities of round r's output (including iota). Round 5 computes
  exactly digest lanes 0..3 (Section 3.1). Lemma 5 makes K the digest read little-endian.
  The organizer-executed experiments re-check this in every trial
  (Section 10.2).
- **Outputs.** Any output pair is two distinct messages whose full digests
  were equal under two reference permutations. It is a full collision.

## 7. Success probability

The run halts at the first MATCH. The failure events are:

- **F3**: two groups produce the same message. This happens only if
  P_g XOR P_g' is one of the 2^32 values ins(z) XOR ins(z'). By the union
  bound, Pr[F3] < 2^191 * 2^32 / 2^512 = 2^-289. Without F3 all N messages
  are distinct.
- **F1**: no two of the N messages have equal digests.
- **F2**: some colliding pair (a, b), with a processed before b, has a's slot
  already held by an earlier message c that has the same top 140 bits and a
  different key, so a is discarded.

If none of F1, F2, F3 occurs, take a colliding pair (a, b). When a is
processed, either a's slot already holds key(a), which gives MATCH, or a is
inserted. In the second case a MATCH occurs no later than b. So
Pr[fail] <= Pr[F1] + Pr[F2] + Pr[F3].

**Heuristic H1 (declared; identical text in claim.json).** For the failure
events F1 and F2 (Section 7), the 2^128 keys of the grouped message set
{m(g, z)} (independent uniform prefixes P_g, all z in {0,1}^32, processed in
any fixed order chosen independently of the digests, in particular the order
of Section 2: batch by batch, t = 0..2^32-1 with z = gray(t), slots
p = r + 32i for r = 0..31 and i = 0..7) behave like N independent uniform
256-bit values, i.e. Pr[F1] <= exp(-N(N-1)/2^257) and
Pr[F2] <= N^3/6 * 2^-396.

Under H1:

- Pr[F1] <= exp(-N(N-1)/2^257) = exp(-(1 - 2^-128)/2) < 0.6065307.
- Pr[F2] <= N^3/6 * 2^-140 * 2^-256 < 2^-14.5. We use 2^-13 < 0.0001221.
- Success >= 1 - 0.6065307 - 0.0001221 - 2^-289 > 0.39334. We claim 0.39,
  which leaves an allowance of 0.0033.

**Rigorous partial support.** Take two groups g != g' and any z, z'. The
messages m(g, z) and m(g', z') are independent and each is uniform on 64-byte
strings, so by Cauchy-Schwarz Pr[digests equal] >= 2^-256. Within-group pairs
are a 2^-96 fraction of all pairs. The expected number of colliding pairs is
therefore at least (1 - 2^-96) * N(N-1)/2^257, close to 1/2 as in the uniform
model. H1 is needed only for the second-moment (Poisson-like) behaviour behind
Pr[F1], and for F2. This is jaazinn's argument.

**Bitslicing and batching do not change the message set.** Batching fixes
only the processing order, a function of (beta, t, p), never of digests;
bitslicing changes how a digest is computed, not its value (Section 6).

## 8. Time bound

Per message, the charge is the charged z-step total divided by 256 (245.40),
plus amortised setup (< 2^-20), plus a 2.59 spare. That is 248
operations, or 248/1355 units. It covers the Gray update, rounds 2-5, both
transpose phases, every table load, store, compare and branch, and all loop
control. The only other cost is verification (< 3 units, at most once). So

    T <= 2^128 * 248/1355 + 3 = 0.1830258... * 2^128 + 3 < 2^125.55012.

The claimed time_log2 is **125.551**, rounded up. The bound is worst-case for
every run, with no restarts. preprocessing_log2 = 0: setup is per batch and
inside T.

Comparison on this track (all in review when written): tekkac 126.99
(c0f097f0), ercumentyildirim 127.12 (4c969300) and may93182 127.215
(e36def61), all four-way lane-packed, distribution-free searches without a
heuristic. Ours relies on H1, as jaazinn's package (0a5b7ae8, in review) does.
ercumentyildirim's package also computes only the digest lanes in the last
round (their "last-round early abort"); our round-5 rows and diagonal-only
round 4 are the bitsliced form of the same observation, which our r6 package
uses for its last round as well.

## 9. Sensitivity of the bound to conventions

| variant | ops/message | time_log2 |
| --- | ---: | ---: |
| as claimed (+1 per direct load/store and per ALU immediate, + spare) | 248 | 125.551 |
| no extra charges (48,451/256 + spare) | 192 | 125.181 |
| claimed, plus +1 per shift amount (65,383/256 + spare) | 258 | 125.608 |
| two extra ops per direct access and immediate (77,195/256) | 302 | 125.835 |

Every variant is below 126.99, the lowest score on this track when written.
The register budget is 48 of 64.

## 10. Evidence

### 10.1 Counted simulator (participant evidence)

The program of Section 5 was written as instructions for a counted 256-bit
word-RAM simulator. The simulator has an explicit 64-register file with a
high-water check, counts every primitive, and separates direct from register
addresses. Uninitialised memory reads 0 in even batches and random garbage in
odd ones. Results:

- 16 batches x 4 z-steps x 256 = 16,384 messages. Batch 0 starts at t = 0,
  batch 1 crosses t = 2^31 (ctz 31), and the others start at random t. Every
  key equals int.from_bytes(sha3_256(m, 5), "little") from
  `verifier/keccak.py`: 0 mismatches. The register high-water mark is 48.
  Every inserted id decodes (via q) to a slot whose key matches DK.
- For 4 groups and z bits 0, 5, 17, 31, a scalar recomputation of
  A2(e_j) XOR A2(0) is 0 outside SUPPORT_j and equals the COEF bits inside it.
- The ledger of Section 5.2 is the simulator's per-block count of one
  worst-path z-step. Sparse-set paths were exercised: empty 12, stale 17,
  occupied 14, match 12. Replaying a z-step gave 256 MATCHes whose ids decode
  to the same (beta, p, z).

### 10.2 Declared experiments (organizer-executed, `python-message-pairs-v1`)

All four experiments use `experiments/s3r5_bitslice_birthday.py`. It
implements the bitsliced evaluator of Sections 4-5: per-batch A2 and COEF from
bitsliced round 1, the Gray update on the 62 support words, bitsliced rounds
2-4 forming D on the fly, the row-0 round 5 (last round), and the phased delta-swap
transpose. Every digest used for matching comes from that evaluator. Each
organizer seed derives fresh 64-byte group prefixes with SHA-256.
N_t = 2^9 messages and an 18-bit mask give N_t^2/2^18 = 1 = N^2/2^256. The
uniform-model success probability is 0.39307, with 0.4990 expected masked
pairs per trial; for 256 trials, 100.6 successes (sd 7.8). Trials sharing a
256-position batch own disjoint bit positions, and no operation mixes
positions, so each trial depends only on its seed. Every trial checks 5 keys
(the first 4 in processing order and the last, at a Gray-updated z) at full width against an independent direct sponge (own rho offsets and round
constants) and the support of each coefficient column; any failure aborts.

Layouts: `k5r5-bs-full-width` 256 groups x 2 (t < 2; one trial fills a batch,
groups far outnumber group size, as at full scale); `k5r5-bs-spread` 16 x 32;
`k5r5-bs-single-group` 1 x 512 (strongest within-group structure);
`k5r5-bs-high-z` 4 x 128 with z = gray(t) << 25 (z bits 25..31; for j >= 27
the support wraps around the lane). All use z = gray(t).

### 10.3 Local runs (our seeds; not organizer evidence; all runs reported)

Organizer-runner replay (`experiments/runner.py`, subprocess executor in
place of Docker, track config hash, seed `hashsmash-public-seed-v1`, 256
trials): each experiment ran twice, byte-identical stdout, 2-7 s per run
(Python 3.12); every pair re-checked with `verifier`; all 1,280 exactness
checks per experiment passed (5 per trial; the success counts and masked
pairs are identical to an earlier run of the program with 4 checks per trial).

| experiment | successes / 256 | z (model 100.6, sd 7.8) | masked pairs (exp. 127.8) |
| --- | ---: | ---: | ---: |
| k5r5-bs-full-width | 89 | -1.5 | 107 |
| k5r5-bs-spread | 82 | -2.4 | 98 |
| k5r5-bs-single-group | 107 | +0.8 | 145 |
| k5r5-bs-high-z | 98 | -0.3 | 128 |

The spread result is low at this seed (-2.4 sd; it was 109 for the six-round
package at the same seed). We did not change seeds, tags or masks after
seeing it. To resolve it we ran the same program at 64 times the size
(`--local`, 8,192 trials per layout and batch, seeds `r5-b1` and `r5-b2`,
both fixed before either was run). Every run we made is listed. The model is
3220.1 +- 44.2 per batch and 6440.1 +- 62.5 pooled:

| layout | batch 1 | batch 2 | pooled | pooled z | pairs (exp. 8176) |
| --- | ---: | ---: | ---: | ---: | ---: |
| full-width | 3254 (+0.8) | 3329 (+2.5) | 6583 | +2.3 | 8339 |
| spread | 3247 (+0.6) | 3219 (-0.0) | 6466 | +0.4 | 8250 |
| single-group | 3240 (+0.5) | 3207 (-0.3) | 6447 | +0.1 | 8205 |
| high-z | 3243 (+0.5) | 3264 (+1.0) | 6507 | +1.1 | 8329 |

At 8,192 trials the spread layout sits at the model value, so the 256-trial
-2.4 is read as sampling noise. The full-width layout has only 256
within-group pairs out of 130,816 per trial, so it is essentially a birthday
test on independent uniform messages; its pooled +2.3 is also read as noise
(the six-round package gave +1.5 with the same layout). Any excess of
collisions would in any case only lower Pr[F1].

**Direct within-group check (local, informational).** Within-group pairs
are where the affine structure of A2 could matter, so we also measured them
directly with the same bitsliced evaluator: 1,024 batches x 256 groups x 32
pairs (z = 0, z = e_j for every j = 0..31), 8,388,608 pairs. The four
experiment masks matched 34, 35, 37 and 33 times (32.0 expected each under
uniformity; 139 in total against 128 +- 11.3). The full 256-bit digest
difference had mean Hamming weight 128.00 and minimum 87 over all pairs (the expected
minimum for 2^23 uniform samples is about 86, median 87). No low-weight or masked-collision
bias appears for one-bit z differences after the four nonlinear rounds 2-5.

## 11. Memory

| array | 32-byte words | bytes |
| --- | --- | --- |
| S | 2^140 | 2^145 |
| DK, DI | <= 2^128 each | <= 2^133 each |
| PREF | 2^97 | 2^102 |
| state, A2, D, ROWS, COEF | < 2^13 | < 2^18 |
| code (unrolled z-step, 32 Gray blocks, setup) | < 2^20 instructions | < 2^25 |

Total < 2^145.01 bytes; we claim 146. Memory is reported only (not a Pareto
improvement over a distinguished-point search).

## 12. Limitations

- H1 is a heuristic. It extends the grouped structure (A2 affine in z within a
  group; shared prefix pairs across groups) from the tested scale
  (N_t = 2^9, 18-bit masks) to N = 2^128 and the full 256-bit key. Organizer
  seeds are public. A 256-trial experiment resolves the success frequency
  only to about +-0.03 (one of our four replays is at -2.4 sd), and the
  0.0033 allowance is not statistically certified. Five rounds leave only
  four nonlinear layers after the affine A2, one fewer than in our six-round
  package.
- Within one group the digest has algebraic degree at most 16 in z (A2 is
  affine in z and four chi layers follow), so it sums to zero over every
  17-dimensional affine subspace of z values. A participant-side check (not
  shipped) with `verifier.keccak.sha3_256(m, 5)` confirms this: two random
  17-dimensional cubes give zero sums, while a 15- and a 16-dimensional cube
  do not. No experiment varies more than 9 z bits, so the experiments cannot
  see this. It concerns only within-group pairs, a 2^-96 fraction of all
  pairs. A relation between two whole groups would need their message sets
  to overlap, i.e. P_g XOR P_g' in the 32-dimensional z-insertion span, which
  has probability 2^-480 per pair of groups. We see no route from this
  structure to clustering of cross-group collisions, but H1 assumes there is
  none.
- The gain comes entirely from operation-level pricing. Bitslicing amortises
  each word operation over 256 messages, and grouping removes round 1 and the
  linear part of round 2. All executed work, including memory traffic and an
  address addition per direct access, is charged. The 64-register machine is
  an assumption (48 are used).
- No sub-birthday attack, collision certificate or full-scale run is claimed.

## 13. Credit

**jaazinn** (0a5b7ae8; co-author in the sense of Section 0) and **may93182**
(11c46f4d; likewise co-author in the sense of Section 0). The scalar last-round early abort on this track
is **ercumentyildirim**'s (4c969300). Errors are ours.
