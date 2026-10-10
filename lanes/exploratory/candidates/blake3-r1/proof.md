# A chunk-counter collision for 1-round BLAKE3

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
separately reported resource bound.

This exploratory package targets blake3-r1-prefix-v1. It gives a
deterministic algorithm that outputs a 3,136-byte message A, all zero bytes,
and a 2,112-byte message B, 2,048 zero bytes and a 64-byte block w, with the
same complete 1-round BLAKE3-256 digest. A has four chunks and B three, so the
roots of both have the same left child, while their right children are the
parent R of A's chunks 2 and 3 (counter 0, flags PARENT = 4) and B's one-block
chunk 2 (counter 2, flags CHUNK_START | CHUNK_END = 3). The counter difference
is cancelled in the column call that reads the low counter word, by the
message words m0, m1, and the flag difference in the column call that reads
the flag word, by m6, m7 (Lemma 1, Section 2): w is R's message words with
those four words moved. The output is a collision, so the success probability
is 1. The algorithm is charged 54 target compressions (every compression of
the complete hashes of both messages, for the final collision check) and 4,734
other primitive operations: 16,722/222 < 75.33 units, below 2^6.2351. The
claimed scalar is 6.2351. Peak memory is below 2^23 bytes.

There is no preprocessing, table, stored collision or nonuniform advice, and
no heuristic: the collision follows from Lemma 1, proved below. Accordingly
the heuristic list is empty.

## 1. The complete hash on the two messages

H is unkeyed BLAKE3-256 with only round 0 kept in every compression. All
additions and subtractions on words are modulo 2^32; ROR rotates a 32-bit word
right. The IV is

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

    G(0,4,8,12; m[0],m[1])     G(1,5,9,13; m[2],m[3])
    G(2,6,10,14; m[4],m[5])    G(3,7,11,15; m[6],m[7])

and the diagonal step

    G(0,5,10,15; m[8],m[9])     G(1,6,11,12; m[10],m[11])
    G(2,7,8,13; m[12],m[13])    G(3,4,9,14; m[14],m[15]),

with no message permutation because no second round follows, and outputs
o[i] = v[i] XOR v[i+8] and o[i+8] = v[i+8] XOR c[i] for i = 0..7. Its
chaining value is o[0..7]. The flags are CHUNK_START = 1, CHUNK_END = 2,
PARENT = 4 and ROOT = 8.

A chunk of 1,024 bytes at chunk counter t is 16 full blocks: block k has
chaining value h_k, with h_0 = IV, counter t, block length 64 and flags 1 for
k = 0, 0 for k = 1..14 and 2 for k = 15, and the chunk's chaining value is
h_16. A chunk of one full block at counter t is one compression with chaining
value IV, counter t, block length 64 and flags 3. A parent compression has
chaining value IV, message words (left chaining value) || (right chaining
value), counter 0, block length 64 and flags PARENT = 4, or PARENT | ROOT = 12
at the root. The tree puts the largest power-of-two number of chunks in the
left subtree. The digest is LE4(o[0]) || ... || LE4(o[7]) of the root.

**Message A** has 3,136 zero bytes: four chunks, c0, c1 and c2 of 1,024 bytes
at counters 0, 1 and 2, and c3 of one block at counter 3. With CV_t the
chaining value of chunk t, its tree is L = parent(CV0, CV1),
R = parent(CV2, CV3) and the root (IV, L || R, counter 0, length 64,
flags 12): 52 compressions.

**Message B** has 2,112 bytes: the same 2,048 zero bytes, chunks c0 and c1 at
counters 0 and 1, and the one-block chunk w at counter 2. Its tree is the same
L, the chunk compression of w, with chaining value CVw, and the root (IV,
L || CVw, counter 0, length 64, flags 12): 35 compressions.

Standard IV, chunk tree, counters, flags, true block lengths, feed-forward and
the full 256-bit digest are used. This is not a free-start, chosen-IV,
compression-only or truncated-output setting.

## 2. Lemma 1: a column call cancels a change of its d word

For j = 0..3, in one round the column call G(j, 4+j, 8+j, 12+j; m[2j],
m[2j+1]) is the only call that reads the initial v[12+j] and the only call
that reads m[2j] and m[2j+1]. In a compression with chaining value IV its
inputs are a0 = IV[j], b0 = IV[4+j], c0 = IV[j] and d0 = v[12+j]. Put
K_j = IV[j] + IV[4+j]. With x = m[2j] and y = m[2j+1] the call computes
a1 = K_j + x, d1 = ROR(d0 XOR a1, 16), and then c1, b1, a2, d2, c2, b2 as in
Section 1.

**Lemma 1.** Let d and d' be two values of v[12+j] and x, y any words. Define

    a1' = a1 XOR d XOR d',    x' = a1' - K_j,    y' = y + a1 - a1'.

Then the call with d' and words (x', y') leaves the same four values as the
call with d and words (x, y).

Proof. In the second call the first assignment gives K_j + x' = a1'. Then
d' XOR a1' = d' XOR a1 XOR d XOR d' = d XOR a1, so the second assignment gives
ROR(d XOR a1, 16) = d1. The third and fourth assignments depend only on d1
and the inputs IV[j], IV[4+j], so they give c1 and b1. The fifth gives
a1' + b1 + y' = a1' + b1 + y + a1 - a1' = a1 + b1 + y = a2. The last three
depend only on d1, a2, c1 and b1, so they give d2, c2 and b2. QED.

**Corollary 1.** Let two compressions have chaining value IV and initial
states that differ only in v[12+j] for j in a set S, and message words that
agree except that, for each j in S, (m[2j], m[2j+1]) is (x, y) in the first
and (x', y') of Lemma 1 for column j in the second. Then all 16 output words
agree.

Proof. The four column calls act on disjoint state words. A column not in S
has the same inputs and words in both, and a column in S leaves the same
values by Lemma 1. After the column step the states are equal, the diagonal
calls read the same words m[8..15], so the final states are equal, and the
feed-forward uses the same chaining value IV. QED.

Here S = {0, 3}. Column 0 reads the low counter word: 0 for the parent R and 2
for the chunk w, XOR 2, with K_0 = 6a09e667 + 510e527f = bb1838e6. Column 3
reads the flag word: 4 for R and 3 for w, XOR 7, with K_3 = a54ff53a +
5be0cd19 = 0130c253. Both have v[13] = 0 and v[14] = 64.

## 3. Algorithm

The machine is the 256-bit word RAM of the cost model. M = 2^32 - 1, and a
32-bit quantity is held in the low 32 bits of a RAM word. The constants are
the IV, K_0, K_3, 2, 7 and M. The algorithm has no input and no coins.

1. CV2 is the chaining value of 16 zero blocks at counter 2 and CV3 that of
   one zero block at counter 3, as Section 1 lists them. Set P = CV2 || CV3.
2. w = P except w[0] = a1' - K_0 and w[1] = P[1] + a1 - a1', where
   a1 = K_0 + P[0] and a1' = a1 XOR 2, and w[6] = e1' - K_3 and
   w[7] = P[7] + e1 - e1', where e1 = K_3 + P[6] and e1' = e1 XOR 7. Each sum
   or difference is reduced by an AND with M.
3. Output A, 98 RAM words of zero, and B, 64 RAM words of zero followed by
   w in two RAM words, each formed from eight little-endian 32-bit words by 7
   shifts and 7 ORs.
4. Verify: compute the chunk compressions of c0 and c1 (32) and L, which are
   the same computations on the same inputs in H(A) and H(B) and are run once;
   R and the root of A; the compression of w and the root of B. With step 1
   these are all the compressions of H(A) and H(B). Compare the two digests on
   all 256 bits and output (A, B) if they agree; else halt with failure.

The RAM program is straight-line: no loop, no restart, no coin, and one
branch, in step 4.

## 4. Correctness

**Theorem.** The algorithm outputs two distinct messages A of 3,136 bytes and
B of 2,112 bytes with H(A) = H(B); the test of step 4 never fails.

Proof. By Section 1 the root of A is the compression (IV, L || R, 0, 64, 12)
and the root of B is (IV, L || CVw, 0, 64, 12), with the same L, since c0 and
c1 are the same bytes at the same counters in both messages. R comes from the
compression with chaining value IV, words P, counter 0, length 64 and flags 4,
and CVw from the compression with chaining value IV, words w, counter 2,
length 64 and flags 3. Their initial states differ only in v[12] (0 and 2)
and v[15] (4 and 3), and w agrees with P except at 0, 1, 6 and 7, which step 2
sets exactly as Lemma 1 sets x' and y' for column 0 (d = 0, d' = 2) and for
column 3 (d = 4, d' = 3). By Corollary 1 with S = {0, 3} the two compressions
have the same output words, so CVw = R, the two roots are the same
compression, and H(A) = H(B). A and B are distinct because their lengths
differ, and both lie in the message domain. This is an ordinary collision of
the complete hash. QED.

## 5. Success probability

The algorithm is deterministic and, by the theorem, outputs a collision: the
success probability is exactly 1, above the required 0.39. There is no failed
trial, restart or amplification. This number concerns the algorithm, not
confidence in a review.

## 6. Charged time

One 1-round target compression costs one unit and every other primitive word
operation costs 1/C units with C = 222.

**Counting convention**, as in entries f0dab7bd and 31acfdbb. One *data
operation* is one addition or subtraction modulo 2^256, one AND, OR or XOR,
one shift, one comparison or one conditional branch. Reduction modulo 2^32 is
an explicit AND with M and is counted; one AND reduces a short sum or
difference correctly because 2^32 divides 2^256. Memory traffic is charged in
full: every data operation is charged as four primitive operations, a load
for each of at most two operands, the operation and a store of its result.
Constants are operands covered by those loads; shift distances are fixed in
the instruction. The internals of a target compression are its unit and are
not charged again; its input and output handling is charged at 80 primitive
operations, a load and a store of each of its 16 initial state words, its 16
message words and its 8 output words.

| Step | Work | Units | Primitive operations |
| --- | --- | ---: | ---: |
| 1 | 17 chunk compressions of c2 and c3 | 17 | |
| 1 | their input and output handling, 17 * 80 | | 1,360 |
| 2 | two moves of Lemma 1, 8 data operations each: 16 | | 64 |
| 3 | 98 + 64 stores of the constant 0 | | 162 |
| 3 | w: 2 RAM words of 7 shifts and 7 ORs, 28 data operations | | 112 |
| 4 | c0 and c1 (32), L, R, the root of A, w, the root of B | 37 | |
| 4 | their input and output handling, 37 * 80 | | 2,960 |
| 4 | digest test: 8 XORs, 7 ORs, a comparison with zero and a branch, 17 data operations | | 68 |
| 4 | output and halt | | 8 |
| | total | 54 | 4,734 |

**Total.** H = 54 target compressions and W = 4,734 other primitive
operations, so

    T = H + W/C = 54 + 4,734/222 = 16,722/222 = 75.3243... units,
    log2 T = 6.23504... < 6.2351.

The claim 6.2351 is log2 T rounded up at the fourth decimal:
222^10000 * 2^62350 <= 16,722^10000 < 222^10000 * 2^62351. The program is
straight-line, so this is the count of every run, at success probability 1,
including message construction, memory traffic and collision checking.

## 7. Memory, preprocessing and advice

Code: the 54 compressions inlined, fewer than 400 instructions each (the
round, the feed-forward and the 80 loads and stores), and fewer than 300
other instructions: fewer than 2^15 instruction templates of at most four
256-bit words each, below 2^22 bytes. Data: the 40 words of one compression,
P, w, the chaining values CV0 to CV3, L, R, CVw, the two digests, the 164
output RAM words and the constants: fewer than 512 words, below 2^14 bytes.
Peak memory is below 2^22 + 2^14 < 2^23 bytes. There is no table, no stored
message database and no stored collision.

There is no preprocessing phase: all work is the run counted in Section 6.
There is no nonuniform advice: the program holds only public constants (the
IV, K_0 and K_3, each the sum of two IV words, 2, 7 and M), and every output
word is computed by the counted steps. The fields preprocessing_log2 = 0 and
nonuniform_advice_log2_bytes = 0 are upper bounds of one unit and one byte,
because the schema cannot express the logarithm of zero.

## 8. Evidence and scope

The supporting evidence is the algorithm, the exact hash of Section 1,
Lemma 1 with its corollary, the theorem and the count of Section 6. The
argument is exact and uses no sampled quantity. The certificate
`counter-pair` is the algorithm's output, `certificates/counter-pair-a.bin`
(A) and `certificates/counter-pair-b.bin` (B), so the organizer's checker
recomputes both digests. No experiment is declared.

Worked values. CV2 || CV3 = P is

    a4036299 e7c3b904 e10102c9 88daee7a f35caa0e 06459f5a 6cced398 502313a4
    ca6d115a 666da456 2b447cc8 96ad4fa3 4e2ef42a e902e102 b43f0450 2987fa9b.

Then a1 = 5f1b9b7f, a1' = 5f1b9b7d, w[0] = a4036297, w[1] = e7c3b906,
e1 = 6dff95eb, e1' = 6dff95ec, w[6] = 6cced399 and w[7] = 502313a3; the other
twelve words of w are those of P. Both messages have the digest

    c236b0dfd53fef88d45ca3022a60daf5af522af90243c280f01c03797a2a4e9d.

Scope and limitations:

- The result is specific to the 1-round prefix. This pair's 2-round digests
  differ. No claim is made about blake3-r2 or full BLAKE3.
- The two messages have different lengths and tree shapes: four chunks and
  three chunks.
- Shared with entries f0dab7bd and 31acfdbb: Lemma 1, there for the block
  length (column 2) and for the flag word (column 3) between two roots. New
  here: the move in column 0, which cancels a chunk-counter difference
  (v[12], 0 against 2) between a parent and a one-block chunk below the roots
  of a four-chunk and a three-chunk tree. The collision needs it together
  with the flag move; on this pair either move alone gives different outputs.
- No literature survey was done and no priority or novelty claim is made.

The claim fields mean: time_log2 = 6.2351 bounds total charged time
(Section 6); memory_log2_bytes = 23 bounds simultaneous storage (Section 7);
preprocessing_log2 = 0 and nonuniform_advice_log2_bytes = 0 as in Section 7;
success_probability = 1 as in Section 5. The required baseline_improved
identifier blake3-r1-nominal-v2 names the organizer's nominal display
reference 128, which is not an established attack, a qualified baseline or a
security bound.

## 9. Earlier entries and credit

Earlier entries of the participant on this track, one line each:

| entry | time_log2 | ruling | kept here |
| --- | ---: | --- | --- |
| beea45d4 | 0 | cancelled | nothing |
| f0dab7bd | 2 | accepted | Lemma 1, there for the block length |
| 31acfdbb | 4.7545 | plausible_not_refuted, not promoted | Lemma 1, there for the flag word |

Credit, one line per contributor; a credit is not an endorsement.

- **Grok 4.7 (xAI)**, run by the participant: cancelling a chunk-counter
  difference in round 0 with m0 and m1 (Lemma 1 for column 0).
- **Jbenisek**, the participant who files this package: Lemma 1 for the block
  length and the flag word (entries f0dab7bd and 31acfdbb), the construction
  with four and three chunks, and this package.
