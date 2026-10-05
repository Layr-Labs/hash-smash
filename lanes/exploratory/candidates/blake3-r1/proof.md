# A deterministic two-compression collision of complete 1-round BLAKE3

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains
a separately reported resource bound.

This exploratory package targets blake3-r1-prefix-v1, the complete unkeyed
BLAKE3-256 hash with only the first round kept in every compression. It gives
a deterministic, straight-line algorithm that outputs two distinct 64-byte
messages with equal complete 1-round BLAKE3 digests. The algorithm uses no
random coins and no heuristic. Its success probability is exactly 1.

The collision is algebraic. With the eight column-step message words held
equal, the digest splits by the four diagonal G calls (Section 3). In two of
those calls we choose the first message word so that one internal addition
has the constant summand t in {0, 2^31}. We then choose the second message
word in two ways, so that each of the call's four output words differs by the
all-ones word 0xffffffff between the two messages. Those differences cancel in
pairs in the feed-forward. The other two diagonal calls are identical in both
messages.

Total charged time is computed exactly in Section 7, and the claim uses a
deliberately conservative accounting. The claimed program has no registers:
every operand is loaded from memory and every result is stored to memory, and
each message is also written out as 64 separate byte cells. It uses 2 target
compressions (the two verification hashes) plus exactly 2570 other 256-bit
word primitives, so T = 2 + 2570/222 = 1507/111 = 13.577 units and
log2 T = 3.7630. The claimed bound is time_log2 = 4, i.e. T <= 16 units, which
allows at most 3108 primitives besides the two compressions (538 of slack; the
bound exceeds the exact T by 17.8%). The same algorithm on a machine with
sixteen 256-bit registers and two-word output needs only 468 primitives
(log2 T = 2.0385); that tighter figure is given for information and is not the
claimed bound. Memory is below 2^16 bytes in both accountings. There is no
preprocessing and no advice.

A deterministic one-round collision of this target also follows from the
one-round inversion algorithm of Aumasson et al. (FSE 2010, Section 5.2); see
Section 12. We claim no novelty for the existence of a cheap deterministic
collision, only for this specific construction and its exact v5 accounting.

Every symbol is defined where it first appears. Throughout, words are 32-bit
unless they are explicitly called 256-bit RAM words.

## 1. Notation

- `+` and `-` on 32-bit words are modulo 2^32.
- `XOR` is bitwise exclusive or.
- `~u` is the 32-bit complement, `u XOR J`.
- `J = 0xffffffff` is the all-ones word.
- `ROR_r(u)` rotates u right by r bit positions within 32 bits.
- `ROL_r(u) = ROR_(32-r)(u)` rotates left. Hence ROR_r(ROL_r(u)) = u.
- LE4(u) is the 4-byte little-endian encoding of u.
- In two's complement modulo 2^32 we have `~u = -u - 1`, since u + ~u = J = -1.

## 2. Exact target

The target is the complete hash H(m) = blake3(m, rounds=1) of
target-profiles/blake3-r1-prefix-v1.json. That is unkeyed BLAKE3-256 with the
standard IV, chunk tree, flags, counters, padding and root output, keeping only
round 0 in every compression. The relation is ordinary collision: two distinct
byte strings of bit length below 2^64 whose complete 256-bit digests are equal.
This is not a free-start, compression-only, truncated or different-round
result.

Every message this algorithm produces or hashes is exactly 64 bytes, i.e. 512
bits. For such a message the standard mode does the following.

- There is one chunk (chunk counter 0) containing exactly 64 bytes, i.e. one
  full 64-byte block.
- There are no parent nodes and no padding block.
- There is exactly one compression: the root compression of that block. Its
  input chaining value is the IV, counter = 0, block length = 64, and
  flags = CHUNK_START | CHUNK_END | ROOT = 1 | 2 | 8 = 11.

The reference implementation verifier/blake3.py does exactly this for a
64-byte input. In `_chunk_output`, last_offset = 0, so the only block is
returned with flags 1|2 and the input CV equal to IV. The root step then
compresses it with flags | ROOT, counter 0 and block length 64.

Decode m into sixteen little-endian words w0..w15. The IV is

    IV = 6a09e667 bb67ae85 3c6ef372 a54ff53a 510e527f 9b05688c 1f83d9ab 5be0cd19.

The 16-word state v is initialised as v[0..7] = IV, v[8..11] = IV[0..3], and
v[12..15] = (0, 0, 64, 11): counter low, counter high, block length, flags.
The function G(a,b,c,d,x,y), with a,b,c,d state indices and x,y message words,
performs eight steps in order:

    (G1) v[a] = v[a] + v[b] + x      (G2) v[d] = ROR_16(v[d] XOR v[a])
    (G3) v[c] = v[c] + v[d]          (G4) v[b] = ROR_12(v[b] XOR v[c])
    (G5) v[a] = v[a] + v[b] + y      (G6) v[d] = ROR_8(v[d] XOR v[a])
    (G7) v[c] = v[c] + v[d]          (G8) v[b] = ROR_7(v[b] XOR v[c])

Round 0 applies eight calls in order, with no message permutation before it.
The permutation acts only between rounds, so it never acts here.

    column step:   G(0,4,8,12,w0,w1)   G(1,5,9,13,w2,w3)
                   G(2,6,10,14,w4,w5)  G(3,7,11,15,w6,w7)
    diagonal step: A = G(0,5,10,15,w8,w9)    B = G(1,6,11,12,w10,w11)
                   C = G(2,7,8,13,w12,w13)   D = G(3,4,9,14,w14,w15)

The output words are o[i] = v[i] XOR v[i+8] and o[i+8] = v[i+8] XOR IV[i] for
i = 0..7. The digest is the first 32 root-output bytes,
H(m) = LE4(o[0]) || ... || LE4(o[7]). Only o[0..7] enter the digest.

## 3. One-round dependency structure

**Proposition 1 (column step).** Write s = (s[0..15]) for the state after the
column step. Then s is a function of w0..w7 only.

*Proof.* The initial state is the same for every 64-byte message: it is built
from IV, 0, 0, 64 and 11. Column call i (i = 0..3) reads and writes only the
indices {i, i+4, i+8, i+12} and the words w_(2i), w_(2i+1). These four index
sets are disjoint. Each call is therefore a function of the initial words at
its own indices and of w0..w7. No word w8..w15 is read before the diagonal
step. QED.

**Proposition 2 (diagonal step).** The diagonal calls act on these index sets:

- A on {0,5,10,15}
- B on {1,6,11,12}
- C on {2,7,8,13}
- D on {3,4,9,14}

These sets partition {0,...,15}. Hence each call's four output words are a
function of the post-column words s at its own four indices and of its own two
message words only. The order of the four calls does not matter.

*Proof.* G(a,b,c,d,x,y) reads and writes only v[a], v[b], v[c] and v[d]. The
four sets are pairwise disjoint and their union is {0..15}. So no call reads a
word that another diagonal call writes. QED.

**Corollary 3 (digest pairing).** The eight digest words pair the diagonal
calls as follows:

| digest word | written by | depends only on |
| --- | --- | --- |
| o0 = v0 XOR v8 | A, C | s, w8, w9, w12, w13 |
| o2 = v2 XOR v10 | C, A | s, w8, w9, w12, w13 |
| o5 = v5 XOR v13 | A, C | s, w8, w9, w12, w13 |
| o7 = v7 XOR v15 | C, A | s, w8, w9, w12, w13 |
| o1 = v1 XOR v9 | B, D | s, w10, w11, w14, w15 |
| o3 = v3 XOR v11 | D, B | s, w10, w11, w14, w15 |
| o4 = v4 XOR v12 | D, B | s, w10, w11, w14, w15 |
| o6 = v6 XOR v14 | B, D | s, w10, w11, w14, w15 |

Here, for each index, "written by" is read off from Proposition 2. With w0..w7
fixed, s is a constant by Proposition 1. Then digest words {0,2,5,7} depend
only on diagonal calls A and C, and digest words {1,3,4,6} depend only on
diagonal calls B and D. Each of A, B, C and D contributes exactly one of the
two words of each digest word in its half.

This exact decomposition was stated for this target in the Yukon submission
4f436735 (PR #142, closed) and in its revision d6e2d67b (PR #144, open,
unpromoted); see Section 12. Those submissions used it for a
generalised-birthday search. Here we use it for a deterministic construction.

## 4. Two lemmas on the all-ones difference

**Lemma 1.** Let c be a 32-bit word. For a 32-bit word e,

    (c + e) XOR (c + ~e) = J    if and only if    2c = 0 (mod 2^32),

that is, if and only if c is 0 or 2^31. In particular, if c is 0 or 2^31, the
identity holds for every e. For any other c it holds for no e.

*Proof.* Put u = c + e and u' = c + ~e. Since ~e = -e - 1, we have
u + u' = 2c - 1 (mod 2^32).

- (If) Suppose 2c = 0. Then u' = -1 - u = ~u, so u XOR u' = u XOR ~u = J.
- (Only if) Suppose u XOR u' = J. Then u' = ~u = -1 - u, so u + u' = -1, and
  comparing with u + u' = 2c - 1 gives 2c = 0.

The solutions of 2c = 0 modulo 2^32 are exactly c = 0 and c = 2^31. QED.

So for a uniformly random c and any fixed e, the all-ones difference survives
the addition c + e with probability 2/2^32 = 2^-31. The construction below avoids this cost
by forcing c to be 0 or 2^31 through a free message word.

**Lemma 2.** Suppose u XOR u' = J. Then for every r and every word z:

- ROR_r(u) XOR ROR_r(u') = J
- (u XOR z) XOR (u' XOR z) = J

*Proof.* Rotation is linear over XOR, so ROR_r(u) XOR ROR_r(u') =
ROR_r(u XOR u') = ROR_r(J). A rotation of the all-ones word is the all-ones
word. The XOR with z cancels. QED.

## 5. Construction

Fix the following public constants:

- the twelve words w0..w7, w10, w11, w14, w15;
- t_A and t_C, each in {0, 2^31};
- e_A and e_C, any 32-bit words.

The claimed program (Section 6) uses the all-zero choice K0: all twelve words
are 0, t_A = t_C = 0, and e_A = e_C = 0. Let s be the post-column state, which
is a constant by Proposition 1.

For each diagonal call P in {A, C}, let (a,b,c,d) be its indices:
(0,5,10,15) for A and (2,7,8,13) for C. Its pre-state is
(a0,b0,c0,d0) = (s[a], s[b], s[c], s[d]), and (t,e) = (t_P, e_P). Define

    d'  = t - c0
    a'  = ROL_16(d') XOR d0
    x   = a' - a0 - b0
    b'  = ROR_12(b0 XOR t)
    T1  = ROL_8(e) XOR d'
    y1  = T1  - (a' + b')
    y2  = ~T1 - (a' + b')

For call A, x is w8 and y1, y2 are the two values of w9. For call C, x is w12
and y1, y2 are the two values of w13.

The two messages are:

- m1: words w0..w7, w10, w11, w14, w15 as fixed, w8 = x_A, w9 = y1_A,
  w12 = x_C, w13 = y1_C.
- m2: the same, except w9 = y2_A and w13 = y2_C.

**Lemma 3 (one manipulated G call).** Run G on pre-state (a0,b0,c0,d0) with
message words (x, y1), and separately with (x, y2). Then the output words
(a,b,c,d) of the two runs differ by (J, J, J, J). In the first run d = e. In
the second run d = ~e.

*Proof.* Steps G1 to G4 depend only on (a0,b0,c0,d0,x), so they are identical
in both runs:

- G1: a1 = a0 + b0 + x = a'.
- G2: d1 = ROR_16(d0 XOR a') = ROR_16(ROL_16(d')) = d'.
- G3: c1 = c0 + d' = t.
- G4: b1 = ROR_12(b0 XOR t) = b'.

At G5, a2 = a' + b' + y. This gives a2 = T1 in the first run and a2 = ~T1 in
the second, so Delta a2 = J.

At G6, d2 = ROR_8(d' XOR a2).

- First run: d2 = ROR_8(d' XOR ROL_8(e) XOR d') = e.
- Second run: d2 = ROR_8(d' XOR ~T1) = ROR_8(~ROL_8(e)) = ~e.

So Delta d2 = J. This also follows from Lemma 2 applied to a2.

At G7, c2 = t + d2, i.e. t + e in the first run and t + ~e in the second.
Since t is 0 or 2^31, Lemma 1 gives Delta c2 = J.

At G8, b2 = ROR_7(b' XOR c2). By Lemma 2, Delta b2 = J. QED.

**Theorem 4.** m1 and m2 are distinct 64-byte messages with H(m1) = H(m2).

*Proof.*

(i) Distinctness. Since ~T1 = -T1 - 1, we have
y1_A - y2_A = T1 - ~T1 = 2*T1 + 1 (mod 2^32). This is odd, hence nonzero, so
w9 differs. The same argument shows that w13 differs. Both messages are 64
bytes long, i.e. 512 < 2^64 bits, so both are in the domain.

(ii) Equal digests. Both messages share w0..w7, so they have the same
post-column state s (Proposition 1). Calls B and D receive the same pre-state
words and the same message words (w10, w11, w14, w15) in both messages. So
v1, v6, v11, v12, v3, v4, v9 and v14 are equal across the two messages
(Proposition 2), and o1, o3, o4 and o6 are equal.

Calls A and C share x but use y1 or y2. By Lemma 3, each of v0, v5, v10, v15
(from A) and v2, v7, v8, v13 (from C) differs by J between the messages. Each
of o0, o2, o5 and o7 is the XOR of one word from A and one from C
(Corollary 3), so its difference is J XOR J = 0.

Hence o[0..7] are equal, and the 32-byte digests are equal. QED.

The construction works for every choice of the public constants, of which
there are 2^384 * 4 * 2^64. Each choice yields an explicit colliding pair. Only
K0 is needed for the claim. The certificates exercise four different choices (Section 10).

## 6. Algorithm

The algorithm takes no input and draws no randomness. This section first
describes it as a straight-line program on an abstract 256-bit word RAM with
sixteen 256-bit registers and 256-bit memory cells at fixed public addresses
(the "register program"). Section 7.2 then derives from it, mechanically, the
register-free program with byte-cell output on which the claimed bound rests.
Every instruction except
COMPRESS is one v5 primitive, charged 1/C_op units with C_op = 222 (the
blake3-r1 reference operation cost; C_op is unrelated to diagonal call C).

| Instruction | Meaning |
| --- | --- |
| LI | load a constant (immediate) into a register; charged as a load |
| LD / ST | load or store a cell |
| ADD / SUB | addition or subtraction modulo 2^256 |
| AND / OR / XOR / NOT | bitwise operations |
| SHL / SHR | shift by an immediate amount |
| EQ | comparison |
| BZ | conditional branch to the program's single FAIL halt (the target is implicit) |
| COMPRESS | one 1-round BLAKE3 compression on 28 prepared input cells (8 CV, 16 message words, counter low, counter high, block length, flags), writing the 8 digest words to 8 output cells; charged exactly 1 unit |

All addresses and shift amounts are immediates, so there is no address
arithmetic and there are no loops.

Narrow 32-bit operations on values below 2^32 use the explicit convention also
used by the organizer's reference cost script:

- a 32-bit sum p + q is ADD then AND with the mask M = 2^32 - 1;
- a sum p + q + r is ADD, ADD, AND;
- ROR_r(z) is SHR r, SHL (32-r), OR, AND M, i.e. 4 primitives;
- a 32-bit complement is NOT then AND M;
- a 32-bit difference is SUB then AND M. Subtraction modulo 2^256 followed by
  AND M gives the correct residue modulo 2^32 because 2^32 divides 2^256.

The program, phase by phase:

```
    Phase 0  M <- 2^32-1.
    Phase 1  For i = 0..3: load the four initial state words of column i and
             w_(2i), w_(2i+1) as immediates; evaluate G (steps G1..G8);
             store the two of its four outputs that belong to calls A and C
             (indices {0,5,10,15} and {2,7,8,13}).
    Phase 2  For P in {A, C}: load (a0,b0,c0,d0), t, e; compute
             d', a', x, b', T1, u = a' + b', y1 = T1 - u, T2 = ~T1,
             y2 = T2 - u (formulas of Section 5); store x, y1, y2.
    Phase 3  Pack each message as two 256-bit words, with message word j of
             a half at bits 32j..32j+31, which is the little-endian 32-byte
             encoding of that half.
             First half (w0..w7, the same for both messages): LI, then 7 times
             LI, SHL, OR; store into both outputs.
             Second half common part P0 = w8 | w10<<64 | w11<<96 | w12<<128
             | w14<<192 | w15<<224 (w8 and w12 loaded, the rest immediates).
             For each message: OR in its w9<<32 and w13<<160; store.
    Phase 4  Collision check, part 1. For each message: store the 8 IV words
             as its input CV; unpack its 16 message words from the two
             256-bit words (SHR 32j, AND M, ST); store counter low 0,
             counter high 0, length 64, flags 11; COMPRESS.
    Phase 5  Collision check, part 2. acc = OR over i of (digest1[i] XOR
             digest2[i]); f = EQ(acc, 0); BZ f -> FAIL.
             g = EQ((m1 word 0 XOR m2 word 0) OR (m1 word 1 XOR m2 word 1), 0);
             n = g XOR 1; BZ n -> FAIL.
    Output   the two stored messages (no further instruction).
```

By Theorem 4 neither branch is taken: the digests are equal and the messages
differ. The register program halts with the collision after exactly 470
instructions: 468 word primitives and 2 COMPRESS. The claimed register-free
program of Section 7.2 executes 2570 word primitives and the same 2 COMPRESS.
The program shape, and therefore the cost, is the same for every choice of
the public constants.

## 7. Time under collision-frontier-v5

One selected-round target compression costs 1 unit. Every other listed 256-bit
RAM primitive costs 1/C_op with C_op = 222: load or store, addition or subtraction,
bitwise operation, shift, comparison, branch and random word. All work is
charged:

- constant initialisation;
- message construction;
- every load, store and branch;
- the collision check, i.e. the two complete hash evaluations and the digest
  and distinctness comparisons;
- output: the messages remain in the four cells written by the four Phase 3
  stores, which are charged; in the claimed accounting (Section 7.2) each
  message is also written out as 64 byte cells, which is charged too.

There is no address arithmetic, no randomness, no failed trial and no restart.

### 7.1 Register program (informative)

The 30 data-path primitives of one G evaluation are:

- G1 and G5 (three-input add): 3 each;
- G2, G4, G6 and G8 (XOR + rotate): 5 each;
- G3 and G7 (add): 2 each.

That gives 3+5+2+5+3+5+2+5 = 30.

Exact primitive counts by phase (LI counted as a load):

| Phase | LI | LD | ST | ALU | BR | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 mask constant | 1 | 0 | 0 | 0 | 0 | 1 |
| 1 column step | 24 | 0 | 8 | 120 | 0 | 152 |
| 2 diagonal A and C (closed form) | 4 | 8 | 6 | 54 | 0 | 72 |
| 3 pack and output | 12 | 6 | 4 | 32 | 0 | 54 |
| 4 verification wrapper | 24 | 4 | 56 | 60 | 0 | 144 |
| 5 digest and distinctness check | 2 | 20 | 0 | 21 | 2 | 45 |
| **Total W** | 67 | 38 | 74 | 287 | 2 | **468** |

Derivation of each row:

- **Phase 1.** Per column call there are 6 LI (4 state words and 2 message
  words), 30 ALU and 2 ST. Column i writes indices {i, i+4, i+8, i+12}, of
  which exactly two lie in {0,2,5,7,8,10,13,15}: (0,8), (5,13), (2,10) and
  (7,15). Total 4 x 38 = 152.
- **Phase 2.** Per call there are 4 LD and 2 LI (t, e), and 27 ALU:
  - d' = SUB, AND: 2
  - a' = ROL_16 + XOR: 5
  - x = SUB, SUB, AND: 3
  - b' = XOR + ROR_12: 5
  - T1 = ROL_8 + XOR: 5
  - u = a' + b' = ADD: 1 (left unmasked; the following SUB, AND masks it)
  - y1 = SUB, AND: 2
  - T2 = NOT, AND: 2
  - y2 = SUB, AND: 2

  plus 3 ST. Total 2 x 36 = 72.
- **Phase 3.** First half: 8 LI, 7 SHL and 7 OR, then 2 ST (24). Common
  second-half part P0: 2 LD, 4 LI, 5 SHL and 5 OR (16). Per message: 2 LD,
  2 SHL, 2 OR and 1 ST (7), twice. Total 24 + 16 + 14 = 54.
- **Phase 4.** Per message: 8 x (LI, ST) for the IV is 16. The unpacking is
  2 x (LD + [AND, ST] + 7 x [SHR, AND, ST]) = 2 x 24 = 48. The four parameter
  words cost 4 x (LI, ST) = 8. That is 72 per message, 144 in total. The two
  COMPRESS instructions are charged 2 units. The compression's internal
  operations (its state initialisation, 8 G calls and feed-forward) are not
  charged a second time, because v5 prices a whole compression at 1 unit.
  Supplying the CV, counter, length and flag inputs is hash-level work outside
  the compression and is charged here.
- **Phase 5.** 16 LD, 8 XOR and 7 OR for the digests (31). Then LI 0, EQ, BZ
  (3). Then 4 LD, 2 XOR, 1 OR, 1 EQ, LI 1, 1 XOR and 1 BZ (11). Total 45.

The hand derivations above are complete. As a development cross-check (the
tool is not part of this package), a counting interpreter executed the program
with a hard limit of 16 registers and reproduced exactly these counts; a
second, independently written interpreter did the same. Both derive the
message pair again directly from the formulas of Section 5 and confirm that
the bytes agree, and the digests computed inside the program agree with the
reference verifier.

**Register-program total (informative, not claimed).** N = 2 target
compressions and W = 468 primitives:

    T = N + W/C_op = 2 + 468/222 = 912/222 = 152/37 = 4.1081...,   log2 T = 2.0385.

The construction alone (phases 0 to 3) is 279/222 = 1.257 units. Most of the
cost is the collision check. This is the tightest figure for this program; it
assumes sixteen reusable registers and two-word output. The claimed bound
below does not depend on either assumption.

### 7.2 Claimed accounting: no registers and byte-cell output

The claimed bound is computed for a stricter machine and output convention,
so that it holds even if registers or packed output are not accepted. Two
changes are made to the register program, and both are charged.

**Phase 3b: byte-cell output.** After Phase 3, each message is also written
out as 64 separate memory cells, cell k holding byte k of the message (a value
below 256). In register form: LI 0xff once; then for each of the four packed
256-bit words, one LD and, for j = 0..31, SHR 8j (omitted for j = 0), AND 0xff
and ST into the byte cell. That is 1 LD + 31 SHR + 32 AND + 32 ST = 96 per
packed word, and 1 + 4 x 96 = 385 for both messages. (The earlier estimate of
"about 384" omitted the mask constant.) With Phase 3b the register program has
W_b = 468 + 385 = 853 primitives (log2 T = 2.5465), consisting of 68 LI,
42 LD, 202 ST, 325 binary operations (26 ADD, 10 SUB, 208 AND, 46 OR, 33 XOR,
2 EQ), 214 unary operations (2 NOT, 38 SHL, 174 SHR) and 2 BZ.

**No registers.** Each of the sixteen registers is replaced by its own memory
cell, and every instruction is rewritten in load-operands / operate /
store-result form. The machine keeps no value between instructions except in
memory:

| Register instruction | Register-free form | Primitives |
| --- | --- | ---: |
| LI r, imm | LI, ST to the cell of r | 2 |
| LD r, [a] | LD [a], ST to the cell of r | 2 |
| ST [a], r | LD the cell of r, ST [a] | 2 |
| binary op (ADD, SUB, AND, OR, XOR, EQ) | LD, LD, op, ST | 4 |
| unary op or shift (NOT, SHL, SHR) | LD, op, ST | 3 |
| BZ r | LD the cell of r, BZ | 2 |
| COMPRESS | unchanged (1 unit) | 0 |

Applied to the 853-primitive program with Phase 3b:

    W_free = 2 x (68 + 42 + 202) + 4 x 325 + 3 x 214 + 2 x 2
           = 624 + 1300 + 642 + 4 = 2570.

By phase: 2 (Phase 0), 512 (Phase 1), 238 (Phase 2), 156 (Phase 3),
1150 (Phase 3b), 380 (Phase 4) and 132 (Phase 5), which sum to 2570.

**Total time (claimed accounting).** N = 2 and W_free = 2570:

    T = 2 + 2570/222 = 1507/111 = 13.5766...,   log2 T = 3.7630.

**Claimed bound.** time_log2 = 4, i.e. T <= 16 units. Equivalently, with
N = 2, the bound allows W <= (16 - 2) x 222 = 3108 primitives. The exact count
2570 leaves 538 primitives of slack, and the bound exceeds the exact T by
17.8%. This covers additional items a reviewer might wish to charge, for
example a halt instruction or one further output instruction per byte cell
(128). The next lower one-decimal value, 3.9 (T <= 14.929), would also bound
the exact count but would exceed it by under 10%, so we claim 4 for margin.

This count is an upper bound for a register-free machine. It charges every
memory access that a direct memory-to-memory encoding would make, and more:
every value loaded by LD or LI passes through a register cell and is loaded
again. For comparison, the coarser memory-to-memory rule "charge every binary
operand its own load and every result its own store (3 extra per binary
operation), 2 extra per unary operation and 1 per branch" gives
W' = 853 + 3 x 325 + 2 x 214 + 2 = 2258 (log2 3.6054) for the same program,
and W' = 1241 (log2 2.9241) without Phase 3b. All these figures are within
the claimed bound.

The collision check in Phase 4 hashes the message words unpacked from the
packed 256-bit words. The byte cells are derived from the same words by exact
shifts and masks. If the check were instead required to reassemble each
32-bit word from its four byte cells (4 LD, 3 SHL, 3 OR and 1 ST per word),
the register program would grow to 1109 primitives. The coarser rule above
then gives 2842 (log2 3.8877), still within the bound, while the mechanical
translation of that variant gives 3278 (log2 4.0674). We do not use that
variant.

As a development cross-check (not part of this package), a second counting
interpreter executed the register-free program for all four certificate
constant sets on a machine with no registers. It has three transient operand
latches that are cleared after every operation, store and branch, and reading
a latch that was not freshly loaded is an error. It reproduced the count of
2570, checked that the byte cells equal the 64 message bytes and that the
pair matches the direct derivation of Section 5, and confirmed the equal
digests with the reference verifier. The table and formulas above are
complete without it.

For comparison, the organizer's generic baseline for this track claims 149,
and the nominal display reference is 128.

## 8. Memory

Memory consists of the following.

- **Data.** 90 cells of 32 bytes, 2880 B:
  - 8 post-column words;
  - 6 cells for x, y1, y2 of A and C;
  - 4 cells for the two packed messages;
  - 2 x 28 compression-input cells;
  - 2 x 8 digest cells.
- **Registers.** 16 x 32 B = 512 B.
- **Main program code.** 3772 B. Each instruction is encoded as a 1-byte
  opcode plus 1 byte per register, address or shift field. LI also carries a
  32-byte immediate, so it is 34 B. BZ has an implicit target (the single FAIL
  halt), so no code address is encoded. Even with every field widened to
  2 bytes the main code grows by less than 470 x 4 = 1880 B, and every total
  below stays under 2^16.
- **One-round compression subroutine.**
  - Code: at most 1100 instructions of at most 36 B, i.e. 39600 B. A straight
    memory-to-memory implementation needs at most 960 instructions for
    8 G x 30 ALU operations with up to 3 load/store each, at most 32 for state
    initialisation, at most 32 for the feed-forward and 1 mask constant.
  - Working state: at most 32 cells, 1024 B.

For the register program the total is at most
2880 + 512 + 3772 + 39600 + 1024 = 47788 B.

For the claimed register-free program of Section 7.2:

- **Data.** 234 cells, 7488 B: the 90 cells above, 128 byte cells for the two
  messages and 16 cells that replace the registers.
- **Operand latches.** 3 x 32 B = 96 B (transient; no registers).
- **Main program code.** 12865 B. The encoding is a 1-byte opcode, 2 bytes per
  memory address, 1 byte per latch, operation or shift field, and a 32-byte
  immediate for LI. That gives 68 LI x 34 B, 1110 LD x 4 B, 851 ST x 4 B,
  539 operations x 5 B, 2 BZ x 2 B and 2 COMPRESS x 5 B.
- **One-round compression subroutine.** The same bound as above, 39600 B of
  code and 1024 B of working state.

That total is at most 7488 + 96 + 12865 + 39600 + 1024 = 61073 B. Both totals
are below 2^16 = 65536 B, so memory_log2_bytes = 16.

The public constants are immediates inside the code, and their loads are
charged in Section 7. There is no table, no stored collision, no advice and no
precomputed data.

## 9. Success probability, preprocessing and advice

The algorithm is deterministic. It has no random coins, no seed and no
parameter search. Theorem 4 is an identity that holds for every value of the
public constants, so the one execution succeeds with probability exactly 1,
and success_probability = 1 >= 0.39. No heuristic is used anywhere; the
heuristics list is empty.

Preprocessing is zero. The post-column constant s is computed inline in
phase 1 and charged, rather than hard-coded. preprocessing_log2 = 0 states the
bound 2^0 = 1 unit, because the schema cannot express log2(0).

Nonuniform advice is zero. nonuniform_advice_log2_bytes = 0 is likewise the
smallest expressible bound. The choice of K0 involves no search: the all-zero
constants were picked before any hash was evaluated, and every choice works.

## 10. Certificates

certificates/manifest.json declares four hash-collision-witness-v2 entries for
blake3-r1-prefix-v1. Each entry has two raw 64-byte message files and the
expected 32-byte digest in lowercase hex. The organizer checker recomputes both
complete digests with verifier/blake3.py at rounds = 1 and checks that the
messages differ.

| id | constants | expected digest |
| --- | --- | --- |
| w0-zero | K0: all words 0, t_A = t_C = 0, e_A = e_C = 0 (the claimed program's output) | 33f72d1264d9445bbe9c3b8f5ca2283f497c0ecb128bb4d9020d61c6baa07d44 |
| w1-index | w_i = i for each of the twelve fixed words, t_A = 0, t_C = 2^31, e_A = e_C = 0 | 332b2ac9fc46cf59be9c3b0ed2ec8007302b71fc290334189da5b9188728fa0a |
| w2-ones | all twelve fixed words J, t_A = t_C = 2^31, e_A = e_C = J | 32f82ea0f1de2f20b59b3c41eaab0e8dd7951b1f275f7458e6eb99eabecc3dc5 |
| w3-iv-pi | w_i = IV[i mod 8] for each of the twelve fixed words, t_A = 2^31, t_C = 0, e_A = 243f6a88, e_C = 85a308d3 | d38973ceaf89ab7a0c837f36eec8848f725a95e8e329a053ade05827bab31c28 |

The w0-zero pair, as message words w8, w9, w12, w13 (all other words 0):

    m1: w8 = bd8ae831  w9 = 369f3f1d  w12 = 580179c0  w13 = 29b36fd9
    m2: w8 = bd8ae831  w9 = 124350b6  w12 = 580179c0  w13 = 0b3c365c

As hex bytes:

    m1 = 0000...0000 (32 zero bytes) 31e88abd1d3f9f36 0000000000000000
         c0790158d96fb329 0000000000000000
    m2 = 0000...0000 (32 zero bytes) 31e88abdb6504312 0000000000000000
         c07901585c363c0b 0000000000000000

In all four certificates, only words 9 and 13 differ. For each pair, the
digests differ at every round count from 2 to 7, so the collision is specific
to the 1-round target. Independently of the certificates, the following were
checked during development:

- Lemma 1 exhaustively for all (c, e) at widths 4, 8 and 10 bits.
- Lemma 1 on 2 x 10^5 random 32-bit samples.
- Lemma 3's four-word all-ones difference at each manipulated call.

The certificates illustrate the theorem; they are not needed for the
probability argument, which is exact.

## 11. Scope: why this does not extend to two rounds

Nothing beyond the 1-round target is claimed.

In round 1 (the second round), the message permutation feeds the differing
words w9 and w13 into other G calls. Those calls also receive state words that
already carry all-ones differences. By Lemma 1, an all-ones difference
survives an addition only when the other summand is 0 or 2^31. That condition
is no longer under the attacker's direct control, and differences entering
through both message slots and state words interact through carries.

The certificate pairs collide at 1 round and at no round count from 2 to 7.

## 12. Prior work and attribution

- **Yukon submissions 4f436735 (PR #142, closed) and d6e2d67b (PR #144, open,
  unpromoted).** These exploratory packages for this track, the second a
  revision of the first, stated the exact column-fixing decomposition of
  Section 3: with w0..w7 fixed, the digest splits into two 128-bit halves,
  each the XOR of functions of one diagonal message pair. They then searched
  for a four-sum collision in each half with Wagner's algorithm, claiming
  time_log2 = 48 under a declared four-sum-abundance heuristic. The present
  construction keeps that decomposition and replaces the search with a
  deterministic algebraic choice. That idea substantially informed this work,
  and we credit it. We re-verified the decomposition and give our own proof
  (Section 3).
- **Aumasson, Guo, Knellwolf, Matusiewicz and Meier, "Differential and
  invertibility properties of BLAKE", FSE 2010, full version IACR ePrint
  2010/043.** We checked the following in the ePrint full version.
  - Section 5.1, Proposition 9: for any fixed state, one round of BLAKE is a
    permutation on the message space.
  - Section 5.2, "Inverting f_v^1": using explicit input-output equations of
    G (equations (1) to (10), stated with the constants k_i taken to be zero,
    which is exactly BLAKE3's G), a deterministic algorithm recovers the
    message block from the initial state and any one-round output state.
    Applied to this target, where the single root block leaves all sixteen
    message words free, this immediately gives a deterministic collision, and
    in fact preimages, of the complete 1-round hash: choose two distinct
    one-round output states with equal words v[i] XOR v[i+8] for i = 0..7 and
    invert both. We confirmed this reduction against verifier/blake3.py
    during development (200 of 200 random instances gave verified preimages
    of a random digest and distinct colliding pairs).
  - Section 3.2, Proposition 5 and its proof: for BLAKE, the MSB difference
    0x80000000 is the only difference that passes modular addition with
    differential probability one, and the probability-one characteristics of
    G use only it. The paper adds that when the constants k_i are zero, as in
    BLAKE3's G, more probability-one differentials exist with respect to
    integer addition. Proposition 5 therefore concerns BLAKE, not BLAKE3.
  - Sections 6.1 and 6.2: differences invariant under rotation by 4 bits
    (such as 0x88888888) are used with a linearised G to obtain near-collisions
    on 232 bits for the compression function of a 4-round variant of BLAKE-32
    (rounds 3 to 6).

  The all-ones word is the extreme rotation-invariant difference: it is
  invariant under every rotation. It does not pass a random addition with
  probability one; Lemma 1 gives probability 2^-31. The present construction
  makes it pass deterministically by forcing the other summand to be 0 or 2^31
  with a free message word. Lemmas 1 and 2 are elementary facts. We do not
  claim them as new, and we did not locate the exact all-ones statement in
  that paper.
- **Li Ji and Xu Liangyu (Ji Li and Liangyu Xu), "Attacks on Round-Reduced
  BLAKE", IACR ePrint 2009/238.** The FSE 2010 paper cites them as
  "Ji, L., Liangyu, X.". We checked the following in the ePrint version.
  - Section 2.1, Observation 1: one of the four output words of a G call can
    be controlled by choosing the value of its second message word. Phase 2
    uses this mechanism: the second message word y sets the G5 value of a.
  - Section 3.1: a collision attack on 1.5 rounds of BLAKE-32 with time 2^96
    and trivial memory, and preimages at 2^192. Its Table 5 lists free-start
    collision attacks on 2 and 2.5 rounds of BLAKE-32 at 2^112.
- **Later related work.** Guo, Karpman, Nikolic, Wang and Wu, "Analysis of
  BLAKE2", CT-RSA 2014, ePrint 2013/467, is cited as general context. We
  checked only that its Section 3 notes the absence of constants in BLAKE2's
  G function (as in BLAKE3's G); we rely on no other claim in it.
- **Organizer baseline.** The organizer's generic birthday baseline for this
  track (time_log2 = 149) supplied the house style and the target description
  of Section 2.
- **Specification.** The BLAKE3 specification
  (BLAKE3-team/BLAKE3-specs, blake3.tex) and the trusted reference
  verifier/blake3.py define the target.

**Novelty.** A deterministic collision (indeed a preimage) of the 1-round hash
on single-block messages follows directly from Aumasson et al. (FSE 2010,
Section 5.2). We claim no novelty for that result. What this package
contributes is a specific two-call all-ones construction (only w9 and w13
differ, and only two diagonal G calls are touched), a self-contained proof,
and an exact v5 cost accounting of a complete program including its collision
check. We did not survey the literature exhaustively. One round of BLAKE3 is
far from the full seven rounds, and this result says nothing about full
BLAKE3.

## 13. Claim fields and limitations

- **time_log2 = 4.** Total charged time is at most 2^4 = 16 units under the
  conservative accounting of Section 7.2 (no registers, byte-cell output). The
  exact count there is 1507/111 = 13.577 units (log2 3.7630), leaving 538
  primitives of slack. With sixteen registers and two-word output the same
  algorithm costs 152/37 = 4.108 units (log2 2.0385); that figure is
  informative and not claimed.
- **memory_log2_bytes = 16.** Peak memory, including code, the compression
  subroutine, all data and the cells or registers holding intermediate values,
  is at most 61073 B for the register-free program and 47788 B for the
  register program; both are below 2^16 B.
- **preprocessing_log2 = 0** and **nonuniform_advice_log2_bytes = 0.** Both
  quantities are actually zero. The values are the smallest the schema
  accepts.
- **success_probability = 1.** The algorithm is deterministic, with no coins
  and no heuristic.
- **baseline_improved = "blake3-r1-nominal-v2".** This is the required
  organizer reference identifier for the nominal display value 128. It is not
  an established attack or security bound. The claimed scalar 4 is below both
  128 and the organizer baseline's 149, but no Pareto-dominance or acceptance
  claim follows from that.

Limitations:

- The target keeps only one of BLAKE3's seven rounds. It is an organizer-chosen
  exploration target, and the owner may decide to re-scope a target that turns
  out to be this degenerate.
- The cost model is an abstract 256-bit word RAM. The numbers are exact
  operation counts in that model, not CPU timings.
- submission_state = ready means the package is complete for review. It does
  not assert a review outcome, a score or promotion; promotion on this track is
  manual.
