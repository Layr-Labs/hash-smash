# sha3-256-r6: bitsliced grouped birthday search, time_log2 = 125.635

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
worst path is 61,583 operations. Charging one extra address addition for each
of its 19,490 direct-address loads and stores and one extra MOVI for each of
its 12 ALU immediates (Section 1) gives 81,085, or 316.74 per message.

| quantity | value |
| --- | --- |
| messages N | 255*2^120 = (255*2^80) batches x 256 groups x 2^32 values of z |
| ops per z-step (256 messages), worst path | 61,583 counted; 81,085 charged |
| charged ops per message | 81,085/256 + 2^-20 < 316.738283 |
| total T | <= N*(81,085/256 + 2^-20)/1626 + 2^30/1626 + 3 < 2^125.635 |
| claimed time_log2 | **125.635** |
| success probability | > 0.390978 under H1; claimed 0.39 |
| memory | < 2^145.01 bytes; claimed 146 |

**Credit and provenance.** The evaluator and experiment source are reused
from winglock's unpromoted submission 377eebd, commit
`8ace5566b9451c6639d70bcb90bcd839ebf6f0d2` (125.655).
Its grouped framework and sparse set derive from jaazinn's promoted BLAKE3
submission 0a5b7ae8; its bit-plane representation and transpose derive from
may93182's unpromoted 11c46f4d. winglock and may93182 are co-authors for reused
unpromoted work; jaazinn is cited for the promoted foundation. None has reviewed
our changes. Our contribution is the reduced fixed batch budget, exact rational
accounting with an explicit global startup reserve, and fresh 510-message
scaled experiments. The inherited source has only the message-budget change.

## 1. Target, machine and charging conventions

- Target `sha3-256-r6-prefix-v1`: the complete SHA3-256 sponge (rate 1088,
  capacity 512, suffix 0x06, pad10*1, zero IV), Keccak rounds 0..5 (RC[0..5])
  and all 256 output bits, as in `verifier/keccak.py:sha3_256(msg, 6)`.
  Messages are exactly 64 bytes, so there is one block. Lane k (k < 8) is
  bytes 8k..8k+7 read little-endian. Lane 8 = 0x06, lane 16 = 0x80 << 56, and
  the other lanes are 0. Lane index is L = x + 5y.
- Digest = lanes 0..3 after round 5, little-endian. The key is
  K = int.from_bytes(digest, "little"), so bit k of K is bit k mod 64 of
  digest lane floor(k/64), with iota of round 5 included. Equal digests and
  equal keys are the same event.
- Cost model `collision-frontier-v5`, C = 1626. One permutation costs 1 unit and
  any other primitive costs 1/1626. Machine: a 256-bit word RAM with 64
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
(x=0, y=1). Write g = 256*beta + p, with batch index beta < 255*2^80 and bit
position (slot) p < 256. Batch beta runs t = 0, 1, ..., 2^32 - 1 with
z = gray(t) = t XOR (t >> 1). At each t it evaluates the 256 messages
m(256*beta + p, gray(t)), p = 0..255, and offers them to the table in slot
order p = r + 32i (r = 0..31, i = 0..7). Batches run in order beta = 0, 1, ....
Every message is evaluated exactly once, and N = (255*2^80) * 256 * 2^32 = 255*2^120. This truncates the inherited fixed batch order by 1/256; it never depends on digests.

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

The base reports 473,034 operations (661,406 charged). We use only the
coarser independently checkable bound < 2^20, including batch-loop control.
Here is a conservative construction budget: 33 full round-1 passes at <18,300
charged operations each; two input transposes at <8,300 each; prefix random
words, saves and address increments <3,000; padding <2,200; initial parity/D
construction <7,000; forming A2(0) <12,000; 32*62 coefficient differences and
stores <21,000; restoring toggled input planes <1,000; batch counter/control
<1,000. Their sum is <668,000 <2^20. Masks/constants are constructed once in
the global reserve. Dividing by 2^40 messages gives <2^-20 per message.
For worst-case bounds every z-step pays the full control/Gray path, including
the first step, which actually skips it.

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
        ROUND(ST1, DB, ST0, all, RC[3], DA)      ; round 4
        ROUND(ST0, DA, ST1, DIAG, RC[4], DB)     ; round 5, stores lanes 0,6,12,18,24
    (d) ROUND6(ST1, DB) -> ROWS                  ; digest planes only
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
13,135 for round 3 and 13,133 for round 4. Round 2 (no theta loads or XORs)
is 64*145 + 650 + 3 = 9,933. Round 5 (5 stores per plane) is
64*175 + 650 + 5 = 11,855.

ROUND6(src, Din) uses only output row Y = 0, whose sources are the diagonal
lanes 6X:

    for b = 0..63:
      for X = 0..4: b' = (b - RHO[6X]) mod 64 ; B[X] = LOAD [src + 64*6X + b'] ;
                    d = LOAD [Din + 64X + b'] ; B[X] = B[X] XOR d
      for X = 0..3: t = NOT B[X+1] ; t = t AND B[X+2] ; o = B[X] XOR t ;
                    (X = 0 and bit b of RC[5]: o = NOT o) ; STORE [ROWS + 64X + b] = o

That is 64*31 + 2 = 1,986 operations. Row k = 64X + b of ROWS is key bit k.

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
| round 4 | 13,133 | 5,130 | 18,263 |
| round 5 | 11,855 | 3,850 | 15,705 |
| round 6 digest rows | 1,986 | 896 | 2,882 |
| IDM reset | 1 | 0 | 1 |
| transpose phase 1 | 4,357 | 512 | 4,869 |
| transpose phase 2 + 256 sparse steps | 6,915 | 256 | 7,171 |
| (f) loop test | 2 | 0 + 1 | 3 |
| **total per 256 messages** | **61,583** | **19,490 + 12** | **81,085** |

By opcode: 12,496 direct and 512 register loads, 6,994 direct and 768
register stores, 21,311 XOR, 7,686 AND, 6,674 NOT, 1,024 SHL, 1,536 SHR, 1,537
ADD, 518 CMP, 519 branch, 8 MOVI: 240.56 per message, 316.74 charged.

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
  complete parities of round r's output (including iota). Round 6 computes
  exactly digest lanes 0..3. Lemma 5 makes K the digest read little-endian.
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
events F1 and F2 (Section 7), the N = 255*2^120 keys of the grouped message set
{m(g, z)} (independent uniform prefixes P_g, all z in {0,1}^32, processed in
any fixed order chosen independently of the digests, in particular the order
of Section 2: batch by batch, t = 0..2^32-1 with z = gray(t), slots
p = r + 32i for r = 0..31 and i = 0..7) behave like N independent uniform
256-bit values, i.e. Pr[F1] <= exp(-N(N-1)/2^257) and
Pr[F2] <= N^3/6 * 2^-396.

Under H1, with N = 255*2^120:

- N(N-1)/2^257 = (255/256)^2/2 - N/2^257.
  Thus Pr[F1] <0.608899908041 (the positive finite-N correction is <2^-129;
  exp(-0.49610137939453125) <0.608899908040).
- Pr[F2] <= N^3/(6*2^396) < 2^-13 <0.000122071.
- Pr[F3] <2^-289 still holds, since the group count is below 2^96.
- Success >1 - 0.608899908041 - 2^-13 - 2^-289 >0.390978 >0.39.

The score uses this explicit heuristic lower bound, not an empirically certified
probability. The reduction spends part of the inherited success margin.

**Rigorous partial support.** Take two groups g != g' and any z, z'. The
messages m(g, z) and m(g', z') are independent and each is uniform on 64-byte
strings, so by Cauchy-Schwarz Pr[digests equal] >= 2^-256. Within-group pairs
are less than a 2^-95 fraction of all pairs. The expected number of colliding pairs is
therefore at least (1 - 2^-95) * N(N-1)/2^257, close to 0.4961 as in the uniform
model. H1 is needed only for the second-moment (Poisson-like) behaviour behind
Pr[F1], and for F2. This is jaazinn's argument.

**Bitslicing and batching do not change the message set.** Batching fixes
only the processing order, a function of (beta, t, p), never of digests;
bitslicing changes how a digest is computed, not its value (Section 6).

## 8. Time bound and exact rounding

Do not round the z-step ledger to 320. Charge its entire conservative worst
path, 81,085 operations per 256 messages, and <2^20 setup operations per
2^40-message batch. There are exactly B =255*2^80 batches and N =255*2^120
messages. A one-time reserve of 2^30 operations covers global constants,
base-address/register setup and loading the <2^20-instruction program.
This reserve is more than 1,024 primitives per program instruction; only a
fixed number of loads, stores, address steps and immediate construction are
needed per instruction. The reserve is charged during the run, not omitted
as preprocessing. The sparse set is never initialized (Section 5.4).
Verification costs <3 units and occurs at most once. Hence

    c = 81,085/256 + 2^-20 = 316.73828220367431640625
    T <= N*c/1626 + 2^30/1626 + 3 < 2^125.635.

The leading exponent is approximately 125.63438933211927, but this decimal
is not the proof of rounding. For the exact rational right-hand side T=A/D
in lowest terms, the strict integer inequality

    A^200 < D^200 * 2^25127

holds, and 25127/200 =125.635. This includes the global reserve and terminal
verification. The same bound holds on failures and successful paths: no
restart, stopping rule or parallel wall-time discount is used.
preprocessing_log2=0: all setup is inside T.

## 9. Comparison and limitations of the improvement

The base spends 320 operations per message over 2^128 messages (125.655).
We preserve its conservative per-access and immediate charges, use its exact
ledger with separately bounded setup, and run 255/256 of its batches.
The latter reduces actual modeled work by 1/256; removal of spare accounting
tightens the upper bound but does not speed up its evaluator. This is a small
constant-factor improvement, approximately 1.4% in the reported bound.
The evaluator, its maximum 48 live registers and H1 remain inherited.
Our previous 126.902 package was distribution-free; this new package introduces
the explicitly declared H1 and higher memory of the grouped frontier.

## 10. Evidence

### 10.1 Inherited participant evidence; not rerun here

winglock's public package reports a counted simulator covering 16,384 keys,
zero mismatches against the organizer SHA3 reference, a 48-register high-water
mark, high Gray-bit cases, and all four sparse-set paths. That simulator is
not present in the inherited experiment archive and we did not rerun it.
These are attributed reports, not our measurements or trusted organizer counts.
The resource argument rests on the self-contained listing and ledger in Section
5, and the separate setup construction bound above. Our fresh organizer-sandbox
experiments below test the inherited evaluator and modified scale.

### 10.2 Declared experiments (organizer-executed, `python-message-pairs-v1`)

All four experiments use `experiments/s3r6_bitslice_birthday.py`. It
implements the bitsliced evaluator of Sections 4-5: per-batch A2 and COEF from
bitsliced round 1, the Gray update on the 62 support words, bitsliced rounds
2-5 forming D on the fly, the row-0 round 6, and the phased delta-swap
transpose. Every digest used for matching comes from that evaluator. Each
organizer seed derives fresh 64-byte group prefixes with SHA-256.
Each layout includes only its first N_t =510 messages. An 18-bit mask gives
N_t^2/2^18 =(255/256)^2 = N^2/2^256. The uniform-model success probability is
approximately 0.3907; this finite scaled model is not a full-width guarantee. Trials sharing a
256-position batch own disjoint bit positions, and no operation mixes
positions, so each trial depends only on its seed. Every trial checks 4 keys
at full width against an independent direct sponge (own rho offsets and round
constants) and the support of each coefficient column; any failure aborts.

Layouts: `k6r6-bs-full-width` 256 groups x 2 (t < 2; one trial fills a batch,
groups far outnumber group size, as at full scale); `k6r6-bs-spread` 16 x 32;
`k6r6-bs-single-group` 1 x 512 (strongest within-group structure);
`k6r6-bs-high-z` 4 x 128 with z = gray(t) << 25 (z bits 25..31; for j >= 27
the support wraps around the lane). All use z = gray(t); the last two messages of each listed 512-message
layout are skipped, leaving 510. The source asserts this budget per trial.

### 10.3 Fresh checks and evidence boundary

Fresh organizer intake results are recorded here after the immutable source
has run twice in the pinned, bounded, networkless Docker executor. We do not
execute any candidate source on the host. The organizer independently checks
distinctness and the masked output predicate of each returned pair. Full-width
self-checks, support assertions, the emitted 510-message budget and all other
participant observations are untrusted internal evidence. The experiments
are scaled mask events; they are not full collisions, a measurement of the
81,085-operation ledger, or certification of >=0.39 success at full scale.
No inherited local success table is represented as a measurement of this
modified candidate. The prior author reported those for 512-message layouts.

Fresh pinned Docker intake completed successfully. All four experiments ran
twice with byte-identical stdout, 256 trials each. Host-verified mask-event
success counts are:

| Layout | successes / trials |
| --- | ---: |
| k6r6-bs-full-width | 99/256 |
| k6r6-bs-spread | 107/256 |
| k6r6-bs-single-group | 107/256 |
| k6r6-bs-high-z | 111/256 |

All 1,024 trial observations reported 510 messages and four self-checks;
these observations are not independently certified. No full collision or
full-scale search is claimed. Experiment execution report SHA-256:
`de2a4dae4897c1bbfd4e26cc51414e2e95ad07d175c34ca4c5d05c3c2eef3c50`.


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
  (N_t =510, 18-bit masks) to N =255*2^120 and the full 256-bit key. Organizer
  seeds are public. A 256-trial experiment resolves the success frequency
  only to about +-0.03, and the approximately 0.000978 conservative success allowance is not
  statistically certified.
- The gain comes entirely from operation-level pricing. Bitslicing amortises
  each word operation over 256 messages, and grouping removes round 1 and the
  linear part of round 2. All executed work, including memory traffic and an
  address addition per direct access, is charged. The 64-register machine is
  an assumption (48 are used).
- No sub-birthday attack, collision certificate or full-scale run is claimed.

## 13. Credit

winglock (unpromoted 377eebd), may93182 (unpromoted 11c46f4d), and jaazinn
(promoted 0a5b7ae8), with contributions detailed in Section 0. Our changes and
any new errors are ours; prior authors have not endorsed this package.
