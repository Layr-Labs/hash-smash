# A domain-flag collision for 1-round BLAKE3

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
separately reported resource bound.

This exploratory package targets blake3-r1-prefix-v1. It gives a
deterministic algorithm that outputs a 1,088-byte message B, all zero bytes,
and a 64-byte message A with the same complete 1-round BLAKE3-256 digest. B
is hashed by a chunk tree whose root is a parent compression with flags 12; A
is hashed by one compression, a one-block root with flags 11. The algorithm
computes the two chunk chaining values of B, which are the message words of
B's root, and moves two of those words so that the flag difference is
cancelled inside the one G call that reads the flag word (Lemma 1,
Section 2); the result is A. The output is a collision, so the success
probability is 1. The algorithm is charged 19 target compressions (the
complete hashes of both messages, which also serve the final collision check)
and 1,774 other primitive operations: 5,992/222 < 26.992 units, below
2^4.7545. The claimed scalar is 4.7545. Peak memory is below 2^21 bytes.

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

**Message B** has 1,088 bytes, so it has two chunks: chunk 0 is bytes 0..1023
(16 full blocks) and chunk 1 is bytes 1024..1087 (one full block). No block
is zero filled. Here every byte of B is zero, so every message word of its
chunk compressions is 0. H(B) evaluates 18 compressions, all with block
length 64:

- chunk 0, counter 0: block k (k = 0..15) has chaining value h_k, with
  h_0 = IV, and h_{k+1} is the chaining value of its compression. Its flags
  are 1 for k = 0, 0 for k = 1..14 and 2 for k = 15. The chaining value of
  chunk 0 is h_16;
- chunk 1, counter 1: one compression with chaining value IV and flags
  CHUNK_START | CHUNK_END = 3. Its chaining value is g;
- the root, the parent of the two chunks: chaining value IV, message words
  P = h_16 || g, counter 0, block length 64 and flags PARENT | ROOT = 12.
  H(B) is LE4(o[0]) || ... || LE4(o[7]) of this compression.

This is the standard tree of the target profile for two chunks: one parent,
which is the root, and no ROOT flag on a chunk compression.

**Message A** has 64 bytes: one chunk of one full block, so H(A) is one
compression, the root, with chaining value IV, message words a[0..15] (the
little-endian words of A), counter 0, block length 64 and flags
CHUNK_START | CHUNK_END | ROOT = 11. H(A) is LE4(o[0]) || ... || LE4(o[7]).

Standard IV, flags, true block lengths, counters, feed-forward and the full
256-bit digest are used. This is not a free-start, chosen-IV,
compression-only or truncated-output setting.

## 2. Lemma 1: the flag word cancelled by two message words

In one round, the column call G(3,7,11,15; m[6], m[7]) is the only call that
reads the initial v[15], the flag word, and the only call that reads m[6] and
m[7]. In a compression with chaining value IV its inputs are a0 = IV[3],
b0 = IV[7], c0 = IV[3] and d0 = f. Put

    K = IV[3] + IV[7] = a54ff53a + 5be0cd19 = 0130c253.

With x = m[6] and y = m[7] the call computes a1 = K + x,
d1 = ROR(f XOR a1, 16), and then c1, b1, a2, d2, c2, b2 as in Section 1.

**Lemma 1.** Let f and f' be two flag words and x, y any words. Define

    a1' = a1 XOR f XOR f',    x' = a1' - K,    y' = y + a1 - a1'.

Then the call with flag word f' and words (x', y') leaves the same four values
as the call with flag word f and words (x, y).

Proof. In the second call the first assignment gives K + x' = a1'. Then
f' XOR a1' = f' XOR a1 XOR f XOR f' = f XOR a1, so the second assignment gives
ROR(f XOR a1, 16) = d1. The third and fourth assignments depend only on d1
and the inputs IV[3], IV[7], so they give c1 and b1. The fifth gives
a1' + b1 + y' = a1' + b1 + y + a1 - a1' = a1 + b1 + y = a2. The last three
depend only on d1, a2, c1 and b1, so they give d2, c2 and b2. QED.

**Corollary 1.** Let two compressions have chaining value IV, the same counter
and block length, flags f and f', and message words that agree except
m[6], m[7], which are (x, y) in the first and (x', y') of Lemma 1 in the
second. Then all 16 output words agree.

Proof. The initial states differ only in v[15]. The column calls on columns
0, 1 and 2 act on other state words and read neither v[15] nor m[6], m[7], so
they leave the same values; the column-3 call leaves the same values by
Lemma 1. After the column step the states are equal, the diagonal calls read
the same words m[8..15], so the final states are equal, and the feed-forward
uses the same chaining value IV. QED.

This is the lemma of entry f0dab7bd, which applied it to the block length
v[14] through m[4], m[5]. Here it is applied to the flag word: the first
compression is B's root, with f = 12, and the second is A's, with f' = 11;
f XOR f' = 7.

## 3. Algorithm

The machine is the 256-bit word RAM of the cost model. M = 2^32 - 1, and a
32-bit quantity is held in the low 32 bits of a RAM word. The constants are
the IV, K = 0130c253, 7 and M. The algorithm has no input and no coins.

1. Chunk chaining values of B: h_0 = IV and, for k = 0..15, h_{k+1} is the
   chaining value of the compression with chaining value h_k, all sixteen
   message words 0, counter 0, block length 64 and flags F_k, where F_0 = 1,
   F_k = 0 for k = 1..14 and F_15 = 2; g is the chaining value of the
   compression with chaining value IV, all message words 0, counter 1, block
   length 64 and flags 3. Set P = h_16 || g.
2. Words of A: a = P except a[6] = a1' - K and a[7] = P[7] + a1 - a1', where
   a1 = K + P[6] and a1' = a1 XOR 7. Each sum or difference is reduced by an
   AND with M.
3. Output A, two RAM words, each formed from eight little-endian 32-bit words
   of a by 7 shifts and 7 ORs, and B, 34 RAM words of zero.
4. Verify: compute the root compression of B (chaining value IV, words P,
   counter 0, length 64, flags 12) and the root compression of A (chaining
   value IV, words a, counter 0, length 64, flags 11). With the 17
   compressions of step 1 these are all the compressions of H(B) and H(A)
   (Section 1). Compare the two digests on all 256 bits and output (A, B) if
   they agree; else halt with failure.

The RAM program is straight-line: no loop, no restart, no coin, and one
branch, in step 4.

## 4. Correctness

**Theorem.** For every 1,088-byte message B, steps 1 and 2 applied to B's
words give a 64-byte message A with H(A) = H(B) and A different from B. In
particular the algorithm, with B = 1,088 zero bytes, outputs a collision of
the complete hash, and the test of step 4 never fails.

Proof. Step 1 runs the 17 chunk compressions of B exactly as Section 1 lists
them (with B's words in place of 0 for a general B), so the root compression
of B has chaining value IV, message words P, counter 0, length 64 and flags
12. The root compression of A has chaining value IV, message words a,
counter 0, length 64 and flags 11. The words a agree with P except at 6 and 7,
which step 2 sets exactly as Lemma 1 sets x' and y' for x = P[6], y = P[7],
f = 12 and f' = 11. By Corollary 1 the two root compressions have the same 16
output words, so H(A) = H(B). A and B are distinct because their lengths
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

**Counting convention**, as in entry f0dab7bd. One *data operation* is one
addition or subtraction modulo 2^256, one AND, OR or XOR, one shift, one
comparison or one conditional branch. Reduction modulo 2^32 is an explicit
AND with M and is counted; one AND reduces a short sum or difference
correctly because 2^32 divides 2^256. Memory traffic is charged in full:
every data operation is charged as four primitive operations, a load for each
of at most two operands, the operation and a store of its result. Constants
are operands covered by those loads; shift distances are fixed in the
instruction. The internals of a target compression are its unit and are not
charged again; its input and output handling is charged at 80 primitive
operations, a load and a store of each of its 16 initial state words, its 16
message words and its 8 output words.

| Step | Work | Units | Primitive operations |
| --- | --- | ---: | ---: |
| 1 | 17 chunk compressions of B | 17 | |
| 1 | their input and output handling, 17 * 80 | | 1,360 |
| 2 | a1 (2), a1' (1), a[6] (2), a[7] (3): 8 data operations | | 32 |
| 3 | A: 2 RAM words of 7 shifts and 7 ORs, 28 data operations | | 112 |
| 3 | B: 34 stores of the constant 0 | | 34 |
| 4 | 2 root compressions | 2 | |
| 4 | their input and output handling, 2 * 80 | | 160 |
| 4 | digest test: 8 XORs, 7 ORs, a comparison with zero and a branch, 17 data operations | | 68 |
| 4 | output and halt | | 8 |
| | total | 19 | 1,774 |

The experiment program performs, for the algorithm's output, exactly the 17
compressions of step 1 and the 36 data operations of steps 2 and 3, one Python
operator each; its other arithmetic is on list indices and shift distances,
which the straight-line RAM program fixes in its instructions.

**Total.** H = 19 target compressions and W = 1,774 other primitive
operations, so

    T = H + W/C = 19 + 1,774/222 = 5,992/222 = 26.9909... units,
    log2 T = 4.75440... < 4.7545.

The claim 4.7545 is log2 T rounded up at the fourth decimal:
222^10000 * 2^47544 <= 5,992^10000 < 222^10000 * 2^47545. The program is
straight-line, so this is the count of every run, at success probability 1,
including message construction, memory traffic and collision checking.

## 7. Memory, preprocessing and advice

Code: the 19 compressions inlined, fewer than 400 instructions each (the
round, the feed-forward and the 80 loads and stores), and fewer than 100
other instructions: fewer than 2^13 instruction templates of at most four
256-bit words each, below 2^20 bytes. Data: the 40 words of one compression,
P, a, the 36 output RAM words and the constants: fewer than 256 words, below
2^13 bytes. Peak memory is below 2^20 + 2^13 < 2^21 bytes. There is no table,
no stored message database and no stored collision.

There is no preprocessing phase: all work is the run counted in Section 6.
There is no nonuniform advice: the program holds only public constants (the
IV, K, the sum of two IV words, 7 and M), and every output word is computed
by the counted steps. The fields preprocessing_log2 = 0 and
nonuniform_advice_log2_bytes = 0 are upper bounds of one unit and one byte,
because the schema cannot express the logarithm of zero.

## 8. Evidence and scope

The supporting evidence is the algorithm, the exact hash of Section 1,
Lemma 1 with its corollary, the theorem and the count of Section 6. The
argument is exact and uses no sampled quantity.

The experiment `flag-cancel-pairs` runs `experiments/flagpair.py`, which
applies steps 1 to 3 to a 1,088-byte B and returns B with the A it derives.
Trial 0 uses the B of the first published pair of this construction, whose
16 chunk-0 blocks and one chunk-1 block were made by inverting the chunk
compressions so that A comes out as the bytes 00, 01, ..., 3f; trial 1 uses
B = 1,088 zero bytes and is the algorithm's output; every other trial uses a
B expanded from its organizer seed with SHAKE-256. The theorem covers every
such B. The program evaluates chunk compressions only; the organizer runner
recomputes both digests. The proof predicts that every trial returns a full
collision of a 64-byte and a 1,088-byte message. The run checks the identity
on concrete inputs; it is not evidence of attack cost, which Section 6 alone
establishes. The certificate `zero-b-pair` is the algorithm's output,
`certificates/zero-b-pair-a.bin` (A) and `certificates/zero-b-pair-b.bin` (B).

Worked values for B = 1,088 zero bytes. The parent words P = h_16 || g are

    d42f5875 7ee44f82 dcc6308c 1f7a2d21 19ca7444 df0bc125 768d665b d49565fd
    ca0a8dc1 9f4a0224 28b45cc8 419756f5 9e774de1 48e77706 0f21d6e6 7f4469c2.

Then a1 = K + P[6] = 77be28ae, a1' = 77be28a9, a[6] = 768d6656 and
a[7] = d4956602, so A is the 64 bytes

    75582fd4824fe47e8c30c6dc212d7a1f4474ca1925c10bdf56668d76026695d4
    c18d0aca24024a9fc85cb428f5569741e14d779e0677e748e6d6210fc269447f

and both messages have the digest

    a87831e830f74db01a302af3a9346be13aa5e21b0eac13a77cec42291125c270.

Scope and limitations:

- The result is specific to the 1-round prefix. This pair's 2-round digests
  differ. No claim is made about blake3-r2 or full BLAKE3.
- The two messages have different lengths and tree shapes, 1,088 bytes (two
  chunks under a parent, root flags 12) and 64 bytes (one block, root flags
  11). The construction relies on the flags being a compression input, v[15],
  and on both roots starting from the IV, as the target profile specifies.
- Shared with entry f0dab7bd: Lemma 1, there applied to the block length.
  Different here: the cancelled word is the flag word, the two roots belong
  to different tree shapes, and the 64-byte message is derived from the chunk
  chaining values of the long one.
- No literature survey was done and no priority or novelty claim is made.

The claim fields mean: time_log2 = 4.7545 bounds total charged time
(Section 6); memory_log2_bytes = 21 bounds simultaneous storage (Section 7);
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

Credit, one line per contributor; a credit is not an endorsement.

- **Grok 4.7 (xAI)**, run by the participant: the flag cancellation between a
  one-block root and a parent root, and the first pair of this kind (trial 0
  of the experiment).
- **Jbenisek**, the participant who files this package: Lemma 1 for the block
  length (entry f0dab7bd), the forward construction of Section 3 and this
  package.
