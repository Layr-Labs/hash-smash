# A chaining-value collision for 1-round BLAKE3

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
separately reported resource bound.

This exploratory package targets blake3-r1-prefix-v1. It gives a
deterministic algorithm that outputs two distinct 128-byte messages A and B
with the same complete 1-round BLAKE3-256 digest. Each is one chunk of two
blocks. Block 0 of each is built by running round 0 backwards from a chosen
final state (Lemma 2, Section 3), so that the chaining values after block 0
are 0 for A and (1, 0, ..., 0) for B. Block 1 of A is zero and block 1 of B has
m0 = -1, which absorbs the chaining-value difference in the first addition of
the root's column call that reads chaining-value word 0 (Lemma 1, Section 2).
The output is a collision, so the success probability is 1. The algorithm is
charged 4 target compressions (the complete hashes of both messages, for the
final collision check) and 1,060 other primitive operations: 1,948/222 <
8.775 units, below 2^3.1334. The claimed scalar is 3.1334. Peak memory is
below 2^19 bytes.

There is no preprocessing, table, stored collision or nonuniform advice, and
no heuristic: the collision follows from Lemmas 1 and 2, proved below.
Accordingly the heuristic list is empty.

## 1. The complete hash on the two messages

H is unkeyed BLAKE3-256 with only round 0 kept in every compression. All
additions and subtractions on words are modulo 2^32; ROR and ROL rotate a
32-bit word right and left, and M = 2^32 - 1 = ffffffff. The IV is

    6a09e667 bb67ae85 3c6ef372 a54ff53a
    510e527f 9b05688c 1f83d9ab 5be0cd19.

A call G with inputs (a0, b0, c0, d0) and message words (x, y) performs eight
assignments, named

    a1 = a0 + b0 + x          d1 = ROR(d0 XOR a1, 16)
    c1 = c0 + d1              b1 = ROR(b0 XOR c1, 12)
    a2 = a1 + b1 + y          d2 = ROR(d1 XOR a2, 8)
    c2 = c1 + d2              b2 = ROR(b1 XOR c2, 7),

and leaves (a2, b2, c2, d2). G(i,j,k,l; x, y) applies it to the state words
v[i], v[j], v[k], v[l].

A compression takes a chaining value c[0..7], sixteen little-endian message
words m[0..15], a counter t, a block length n and flags f. It sets
v[0..7] = c, v[8..11] = IV[0..3], v[12] = t mod 2^32, v[13] = t div 2^32,
v[14] = n and v[15] = f, runs the column step

    C0 = G(0,4,8,12; m[0],m[1])     C1 = G(1,5,9,13; m[2],m[3])
    C2 = G(2,6,10,14; m[4],m[5])    C3 = G(3,7,11,15; m[6],m[7])

and the diagonal step

    D0 = G(0,5,10,15; m[8],m[9])     D1 = G(1,6,11,12; m[10],m[11])
    D2 = G(2,7,8,13; m[12],m[13])    D3 = G(3,4,9,14; m[14],m[15]),

with no message permutation because no second round follows. Call the state
after the diagonal step the final state s[0..15]. The outputs are
o[i] = s[i] XOR s[i+8] and o[i+8] = s[i+8] XOR c[i] for i = 0..7, and the
chaining value is o[0..7]. The flags are CHUNK_START = 1, CHUNK_END = 2 and
ROOT = 8.

**Both messages** have 128 bytes: one chunk of two full blocks, with no zero
fill and no parent. H evaluates two compressions: block 0 with chaining value
IV, counter 0, block length 64 and flags CHUNK_START = 1, whose chaining value
is h; and the root, block 1, with chaining value h, counter 0, block length 64
and flags CHUNK_END | ROOT = 10. H is LE4(o[0]) || ... || LE4(o[7]) of the
root. Standard IV, flags, true block lengths, counter, feed-forward and the
full 256-bit digest are used. This is not a free-start, chosen-IV,
compression-only or truncated-output setting.

## 2. Lemma 1: a chaining-value difference absorbed by one message word

**Lemma 1.** Let two compressions have the same counter, block length and
flags, chaining values c and c' that agree except c'[j] = c[j] + delta for one
j in 0..3, and message words that agree except m'[2j] = m[2j] - delta. Then
their final states are equal, and so are their chaining values o[0..7].

Proof. The column call Cj reads c[j] as its a input, c[4+j] as its b input,
IV[j] as its c input, v[12+j] as its d input, and m[2j], m[2j+1] as x, y. Its
first assignment gives c[j] + c[4+j] + m[2j] = c'[j] + c'[4+j] + m'[2j] in
both compressions, since c'[4+j] = c[4+j]. Every later assignment of Cj
depends only on that sum and on its b, c, d inputs and y, which agree, so Cj
leaves the same four values in both. The other column calls read neither
c[j] nor m[2j] and have the same inputs. After the column step the states are
equal, and the diagonal calls read the same words m[8..15], so the final
states are equal. The chaining value o[i] = s[i] XOR s[i+8] does not read the
input chaining value. QED.

## 3. Lemma 2: a block with a chosen final state

Fix a chaining value c, a counter t < 2^32, a block length n, flags f and 16
words s[0..15]. For a call D write D.a0, ..., D.d0 for its inputs and D.a1,
..., D.b2 for its assignments, named as in Section 1. Define the block
INV(c, t, n, f; s) as follows.

(D) Each diagonal call Dj (j = 0..3) leaves the state words j, 4 + (j+1 mod 4),
8 + (j+2 mod 4) and 12 + (j+3 mod 4), so its outputs must be Dj.a2 = s[j],
Dj.b2 = s[4 + (j+1 mod 4)], Dj.c2 = s[8 + (j+2 mod 4)] and
Dj.d2 = s[12 + (j+3 mod 4)]. Set

    Dj.b1 = ROL(Dj.b2, 7) XOR Dj.c2     Dj.c1 = Dj.c2 - Dj.d2
    Dj.d1 = ROL(Dj.d2, 8) XOR Dj.a2     Dj.b0 = ROL(Dj.b1, 12) XOR Dj.c1
    Dj.c0 = Dj.c1 - Dj.d1.

(C) Dj reads its b input from u[4 + (j+1 mod 4)] and its c input from
u[8 + (j+2 mod 4)], where u is the state after the column step; so column Ci
(i = 0..3) must leave b2 = u[4+i] and c2 = u[8+i] with those values. Ci has
inputs a0 = c[i], b0 = c[4+i], c0 = IV[i] and d0 = (t, 0, n, f)[i]. Set

    b1 = ROL(b2, 7) XOR c2        c1 = ROL(b1, 12) XOR b0
    d1 = c1 - c0                  a1 = ROL(d1, 16) XOR d0
    d2 = c2 - c1                  a2 = ROL(d2, 8) XOR d1
    m[2i] = a1 - a0 - b0          m[2i+1] = a2 - a1 - b1,

and u[i] = a2, u[12+i] = d2.

(W) Dj reads its a input from u[j] and its d input e_j from
u[12 + (j+3 mod 4)]. Set

    a1 = ROL(Dj.d1, 16) XOR e_j
    m[8+2j] = a1 - u[j] - Dj.b0       m[9+2j] = Dj.a2 - a1 - Dj.b1.

Stage D uses only s, stage C uses c, t, n, f and stage D, and stage W uses
stages C and D.

**Lemma 2.** The compression with chaining value c, counter t, block length
n, flags f and message words INV(c, t, n, f; s) has final state s, and hence
chaining value (s[i] XOR s[i+8]) for i = 0..7.

Proof. ROL(., r) undoes ROR(., r), XOR with a word undoes itself and
subtraction undoes addition. Column Ci starts from (c[i], c[4+i], IV[i], d0):
its first assignment gives a0 + b0 + m[2i] = a1; since d0 XOR a1 =
ROL(d1, 16), the second gives d1; the third gives c0 + d1 = c1; since
b0 XOR c1 = ROL(b1, 12), the fourth gives b1; the fifth gives
a1 + b1 + m[2i+1] = a2; since d1 XOR a2 = ROL(d2, 8), the sixth gives d2; the
seventh gives c1 + d2 = c2; since b1 XOR c2 = ROL(b2, 7), the eighth gives b2.
So the state after the column step is u. Diagonal Dj then starts from
(u[j], Dj.b0, Dj.c0, e_j): the first assignment gives u[j] + Dj.b0 + m[8+2j] =
a1 of stage W; since e_j XOR a1 = ROL(Dj.d1, 16), the second gives Dj.d1; the
third gives Dj.c0 + Dj.d1 = Dj.c1; since Dj.b0 XOR Dj.c1 = ROL(Dj.b1, 12),
the fourth gives Dj.b1; the fifth gives a1 + Dj.b1 + m[9+2j] = Dj.a2; since
Dj.d1 XOR Dj.a2 = ROL(Dj.d2, 8), the sixth gives Dj.d2; the seventh gives
Dj.c1 + Dj.d2 = Dj.c2; since Dj.b1 XOR Dj.c2 = ROL(Dj.b2, 7), the eighth
gives Dj.b2. So the final state is s. QED.

**The two blocks 0.** Here c = IV, t = 0, n = 64 and f = 1, so the d inputs of
C0 to C3 are 0, 0, 64 and 1. Substituting ROL(0, r) = 0, ROL(M, 12) = M and
ROL(1, 16) = 00010000 into stages D, C and W gives the following.

(Z) s = 0. Every diagonal has Dj.b1 = Dj.c1 = Dj.d1 = Dj.b0 = Dj.c0 = 0, so
every column has b2 = c2 = 0, and Ci gives b1 = 0, c1 = IV[4+i],
d1 = IV[4+i] - IV[i], a1 = ROL(d1, 16) XOR d0 (no XOR when d0 = 0),
d2 = 0 - IV[4+i], a2 = ROL(d2, 8) XOR d1, m[2i] = a1 - IV[i] - IV[4+i] and
m[2i+1] = a2 - a1. Each diagonal has a1 = e_j, m[8+2j] = e_j - u[j] and
m[9+2j] = 0 - e_j. The chaining value is 0.

(E) s = (1, 0, ..., 0). Only D0 has a nonzero output, D0.a2 = 1, so
D0.b1 = D0.c1 = D0.b0 = 0, D0.d1 = 1 and D0.c0 = 0 - 1 = M; the other
diagonals are as in (Z). The only column whose required outputs change is C2,
with b2 = 0 and c2 = u[10] = M: b1 = M, c1 = IV[6] XOR M,
d1 = c1 - IV[2], a1 = ROL(d1, 16) XOR 64, d2 = M - c1,
a2 = ROL(d2, 8) XOR d1, m[4] = a1 - IV[2] - IV[6] and m[5] = a2 - a1 - M. The
new u[2] = a2 and u[14] = d2 change the words of D2 and D3, which still have
zero outputs: m[12] = u[13] - u[2] and m[14] = u[14] - u[3], m[15] =
0 - u[14]; m[13] is as in (Z). D0 has a1 = 00010000 XOR u[15], m[8] =
a1 - u[0] and m[9] = 1 - a1. All other words are those of (Z). The chaining
value is (1, 0, ..., 0).

## 4. Algorithm

The machine is the 256-bit word RAM of the cost model; a 32-bit quantity is
held in the low 32 bits of a RAM word. The constants are the IV, M, 64, 1,
00010000 and two lane masks. The algorithm has no input and no coins.

1. Block 0 of A: the words of (Z), keeping u[0], u[3], u[13] and u[15].
2. Block 0 of B: the words of (E) that differ from (Z): m[4], m[5], m[8],
   m[9], m[12], m[14] and m[15].
3. Output A = block 0 of A || 64 zero bytes and B = block 0 of B || the block
   with m[0] = M and all other words 0. Block 0 of A is two RAM words, each
   formed from eight little-endian 32-bit words by 7 shifts and 7 ORs. Block 0
   of B is formed from them by clearing the lanes that differ with an AND and
   inserting the new words with shifts and ORs: lanes 4 and 5 of the first RAM
   word, lanes 0, 1, 4, 6 and 7 of the second. The blocks 1 are four RAM words
   of constants. Each sum or difference is reduced by an AND with M.
4. Verify: compute block 0 and the root of A and of B, the four compressions
   of H(A) and H(B) (Section 1), compare the two digests on all 256 bits and
   output (A, B) if they agree; else halt with failure.

The RAM program is straight-line: no loop, no restart, no coin, and one
branch, in step 4.

## 5. Correctness

**Theorem.** The algorithm outputs two distinct 128-byte messages A and B
with H(A) = H(B); the test of step 4 never fails.

Proof. By Lemma 2 with (Z) and (E), the chaining values after block 0 are
h_A = 0 and h_B = (1, 0, ..., 0). The two roots have the same counter, length
and flags; their chaining values agree except h_B[0] = h_A[0] + 1; their
message words agree except m0, which is 0 in A and M = 0 - 1 in B. By
Lemma 1 with j = 0 and delta = 1 the two roots have the same final state, so
the same o[0..7], and H(A) = H(B). A and B differ in byte 64, the first byte
of block 1 (00 against ff). Both lie in the message domain. This is an
ordinary collision of the complete hash. QED.

## 6. Success probability

The algorithm is deterministic and, by the theorem, outputs a collision: the
success probability is exactly 1, above the required 0.39. There is no failed
trial, restart or amplification. This number concerns the algorithm, not
confidence in a review.

## 7. Charged time

One 1-round target compression costs one unit and every other primitive word
operation costs 1/C units with C = 222.

**Counting convention**, as in entries f0dab7bd, 31acfdbb and c8160a0a. One
*data operation* is one addition or subtraction modulo 2^256, one AND, OR or
XOR, one shift, one comparison or one conditional branch. Reduction modulo
2^32 is an explicit AND with M and is counted; one AND reduces a short sum or
difference correctly because 2^32 divides 2^256. A rotation ROL(x, r) is
((x << r) OR (x >> (32 - r))) AND M: four data operations. Memory traffic is
charged in full: every data operation is charged as four primitive
operations, a load for each of at most two operands, the operation and a
store of its result. Constants are operands covered by those loads; shift
distances are fixed in the instruction. A store of a constant word is one
primitive operation. The internals of a target compression are its unit and
are not charged again; its input and output handling is charged at 80
primitive operations, a load and a store of each of its 16 initial state
words, its 16 message words and its 8 output words.

| Step | Work | Data operations |
| --- | --- | ---: |
| 1 | C0 and C1 of (Z): d1 (2), a1 (4), m[2i] (3), d2 (2), a2 (5), m[2i+1] (2): 18 each | 36 |
| 1 | C2 and C3 of (Z): the same and the XOR with d0 in a1: 19 each | 38 |
| 1 | four diagonals of (Z): two words, a subtraction and an AND each: 4 each | 16 |
| 2 | C2 of (E): c1 (1), d1 (2), a1 (5), m[4] (3), d2 (2), a2 (5), m[5] (3) | 21 |
| 2 | D0 of (E): a1 (1), m[8] (2), m[9] (2) | 5 |
| 2 | D2 and D3 of (E): m[12] (2), m[14] (2), m[15] (2) | 6 |
| 3 | block 0 of A: 2 RAM words of 7 shifts and 7 ORs | 28 |
| 3 | block 0 of B: an AND, 2 shifts and 2 ORs; an AND, 4 shifts and 5 ORs | 15 |
| | total | 165 |

| Step | Work | Units | Primitive operations |
| --- | --- | ---: | ---: |
| 1 to 3 | 165 data operations | | 660 |
| 3 | blocks 1: four stores of constant RAM words | | 4 |
| 4 | blocks 0 and roots of A and B | 4 | |
| 4 | their input and output handling, 4 * 80 | | 320 |
| 4 | digest test: 8 XORs, 7 ORs, a comparison with zero and a branch, 17 data operations | | 68 |
| 4 | output and halt | | 8 |
| | total | 4 | 1,060 |

**Total.** H = 4 target compressions and W = 1,060 other primitive
operations, so

    T = H + W/C = 4 + 1,060/222 = 1,948/222 = 8.7747... units,
    log2 T = 3.13336... < 3.1334.

The claim 3.1334 is log2 T rounded up at the fourth decimal:
222^10000 * 2^31333 <= 1,948^10000 < 222^10000 * 2^31334. The program is
straight-line, so this is the count of every run, at success probability 1,
including message construction, memory traffic and collision checking.

## 8. Memory, preprocessing and advice

Code: the 165 instructions of steps 1 to 3, the four constant stores, the 4
compressions inlined, fewer than 400 instructions each (the round, the
feed-forward and the 80 loads and stores), and the 17-instruction test: fewer
than 2^11 instruction templates of at most four 256-bit words each, below
2^18 bytes. Data: the 32 words of the two blocks 0, the temporaries of steps 1
and 2, the four RAM words of the blocks 0 and the four of the blocks 1, the
40 words of one compression, the two digests and the constants: fewer than
128 words, below 2^12 bytes. Peak memory is below 2^18 + 2^12 < 2^19 bytes.
There is no table, no stored message database and no stored collision.

There is no preprocessing phase: all work is the run counted in Section 7.
There is no nonuniform advice: the program holds only public constants (the
IV, M, 64, 1, 00010000 = ROL(1, 16) and the two lane masks), and every output
word is computed by the counted steps. The fields preprocessing_log2 = 0 and
nonuniform_advice_log2_bytes = 0 are upper bounds of one unit and one byte,
because the schema cannot express the logarithm of zero.

## 9. Evidence and scope

The supporting evidence is the algorithm, the exact hash of Section 1,
Lemmas 1 and 2 with the two cases of Section 3, the theorem and the count of
Section 7. The argument is exact and uses no sampled quantity. The
certificate `cv-pair` is the algorithm's output, `certificates/cv-pair-a.bin`
(A) and `certificates/cv-pair-b.bin` (B), so the organizer's checker
recomputes both digests. No experiment is declared.

Worked values. Block 0 of A is the words

    b100ae1e aa9106b2 639ac88c 6b02eec6 8a471637 b8f8d085 d6aef43e d1c279ea
    8d754531 5be0cd19 89e6df1e 510e527f c5c7e39b 9b05688c 36d9f5da 1f83d9ab

and block 0 of B differs at m[4] = d6efd730, m[5] = f4f1f5b1,
m[8] = 8d744531, m[9] = 5be1cd1a, m[12] = 3d25fd77, m[14] = 75e1a930 and
m[15] = e07c2655. Both messages have the digest

    1e21fb40c93b3b6d061886fdd267e9778bd691476e88fb27e4a2f0d32831c839.

The root outputs agree in o[0..7]; o[8] = s[8] XOR h[0] differs, and it is not
part of the 256-bit digest.

Scope and limitations:

- The result is specific to the 1-round prefix. This pair's 2-round digests
  differ. No claim is made about blake3-r2 or full BLAKE3.
- Shared with entries f0dab7bd, 31acfdbb and c8160a0a: a difference absorbed
  in the one column call that reads it. There the difference is in the
  counter, block length or flag word; here it is in a chaining-value word,
  carried from block 0 to block 1 inside one chunk, and the absorbing word is
  m0 of the next block. Block 0 of each message is built by running round 0
  backwards, the inversion used for one-block pairs in entries 93f45e26,
  61092754 and af4c65b0.
- No literature survey was done and no priority or novelty claim is made.

The claim fields mean: time_log2 = 3.1334 bounds total charged time
(Section 7); memory_log2_bytes = 19 bounds simultaneous storage (Section 8);
preprocessing_log2 = 0 and nonuniform_advice_log2_bytes = 0 as in Section 8;
success_probability = 1 as in Section 6. The required baseline_improved
identifier blake3-r1-nominal-v2 names the organizer's nominal display
reference 128, which is not an established attack, a qualified baseline or a
security bound.

## 10. Earlier entries and credit

Earlier entries of the participant on this track, one line each:

| entry | time_log2 | ruling | kept here |
| --- | ---: | --- | --- |
| beea45d4 | 0 | cancelled | nothing |
| f0dab7bd | 2 | accepted | the counting convention |
| 31acfdbb | 4.7545 | plausible_not_refuted, not promoted | the counting convention |
| c8160a0a | 6.2351 | plausible_not_refuted, not promoted | the counting convention |

Credit, one line per contributor; a credit is not an endorsement.

- **Grok 4.7 (xAI)**, run by the participant: absorbing a chaining-value
  difference in the next block's m0 (Lemma 1), the two target final states
  and the pair (Sections 3 to 5).
- **jvr0x** (entry 93f45e26): inverting the 1-round compression on this track.
- **AArnott** (entry 61092754): inverting the 1-round compression on this
  track.
- **jungjipdo** (entry af4c65b0): reaching the all-zero 1-round output by
  running G backwards; case (Z) of Section 3 is of this kind.
- **Jbenisek**, the participant who files this package: the counting and the
  lane-replacing output of step 3, and this package.
