# A closed-form collision for 1-round BLAKE3

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
separately reported resource bound.

This exploratory package targets blake3-r1-prefix-v1. It gives an explicit
randomized algorithm that outputs a 23-byte message and a 24-byte message with
the same complete 1-round BLAKE3-256 digest. The output is a collision for
every value of the algorithm's random coin, so the success probability is 1.
The algorithm evaluates no compression. Its total charged time is at most 80
primitive word operations, which is less than 0.37 of one target-compression
unit. The claimed bound is 2^0 = 1 unit, so the claimed scalar is 0, the
schema minimum. Peak memory is below 2^15 bytes.

There is no preprocessing, table, stored collision or nonuniform advice. No
differential probability, independence assumption or other heuristic is used:
the collision is an algebraic identity of the 1-round function, proved in
Sections 2 and 4. Accordingly the heuristic list is empty.

## 1. Exact complete hash on the messages used

H is unkeyed BLAKE3-256 with only round 0 kept in every compression. Every
message produced has n = 23 or n = 24 bytes. A message of n bytes with
1 <= n <= 64 is one chunk consisting of one block, with no parent node, so H
evaluates exactly one compression. The block is the message followed by
64 - n zero bytes, used only for loading words. The compression has flags
CHUNK_START | CHUNK_END | ROOT = 1 + 2 + 8 = 11, true block length n, and
chunk counter and root-output counter both zero. There is no key and no
derivation flag.

Decode the zero-filled block into sixteen little-endian 32-bit words w[0..15].
For n <= 24 the words w[6..15] are zero. The IV is

    6a09e667 bb67ae85 3c6ef372 a54ff53a
    510e527f 9b05688c 1f83d9ab 5be0cd19.

Initialize v[0..7] = IV, v[8..11] = IV[0..3] and v[12..15] = (0, 0, n, 11).
The block length n is therefore the initial value of v[14], and it enters the
compression nowhere else. All additions and subtractions on state and message
words are modulo 2^32. ROR rotates a 32-bit word right. G(a,b,c,d,x,y) is

    v[a] = v[a]+v[b]+x;  v[d] = ROR(v[d] XOR v[a],16)
    v[c] = v[c]+v[d];    v[b] = ROR(v[b] XOR v[c],12)
    v[a] = v[a]+v[b]+y;  v[d] = ROR(v[d] XOR v[a],8)
    v[c] = v[c]+v[d];    v[b] = ROR(v[b] XOR v[c],7).

The one retained round is the column step

    G(0,4,8,12,w[0],w[1]);   G(1,5,9,13,w[2],w[3])
    G(2,6,10,14,w[4],w[5]);  G(3,7,11,15,w[6],w[7])

followed by the diagonal step

    G(0,5,10,15,w[8],w[9]);   G(1,6,11,12,w[10],w[11])
    G(2,7,8,13,w[12],w[13]);  G(3,4,9,14,w[14],w[15]).

No message permutation is applied because no second round follows. The
compression output is o[i] = v[i] XOR v[i+8] and o[i+8] = v[i+8] XOR IV[i] for
i = 0..7. The digest H(m) is the first 32 output bytes,
LE4(o[0]) || ... || LE4(o[7]).

This is the complete hash of the target profile restricted to inputs of 23 and
24 bytes: standard IV, standard flags, true block length, standard
feed-forward and the full 256-bit digest. It is not a free-start, chosen-IV,
compression-only or truncated-output setting. The profile also admits longer
messages and the full chunk tree; the algorithm never produces such messages,
so the single root compression above is the complete hash of every message it
outputs.

## 2. The one G call that reads the block length

The four column calls act on disjoint index sets. The third call,
G(2,6,10,14,w[4],w[5]), is the first and only column call that reads v[14],
and it is also the only call of the column step that reads w[4] and w[5].
Before it, v[2] = IV[2], v[6] = IV[6], v[10] = IV[2] and v[14] = n. Put

    K = IV[2] + IV[6] = 3c6ef372 + 1f83d9ab = 5bf2cd1d.

Write x = w[4] and y = w[5], and name the results of the eight assignments of
this call

    a1 = K + x                d1 = ROR(n XOR a1, 16)
    c1 = IV[2] + d1           b1 = ROR(IV[6] XOR c1, 12)
    a2 = a1 + b1 + y          d2 = ROR(d1 XOR a2, 8)
    c2 = c1 + d2              b2 = ROR(b1 XOR c2, 7).

The call leaves (a2, b2, c2, d2) in (v[2], v[6], v[10], v[14]).

**Lemma.** Let n and n' be two block lengths and let x, y be any words. Define

    a1' = a1 XOR n XOR n',    x' = a1' - K,    y' = y + a1 - a1'.

Then the call with block length n' and words (x', y') leaves the same four
values in v[2], v[6], v[10], v[14] as the call with block length n and words
(x, y).

Proof. In the second execution the first assignment gives K + x' = a1'. Then
n' XOR a1' = n' XOR a1 XOR n XOR n' = n XOR a1, so the second assignment gives
ROR(n XOR a1, 16) = d1. The third and fourth assignments depend only on d1 and
constants, so they give c1 and b1. The fifth gives
a1' + b1 + y' = a1' + b1 + y + a1 - a1' = a1 + b1 + y = a2. The last three
assignments depend only on d1, a2, c1 and b1, so they give d2, c2 and b2. QED.

## 3. Algorithm

The machine is the 256-bit word RAM of the cost model. Let M = 2^32 - 1. Lane
j of a 256-bit word X is X[j] = (X >> 32j) AND M for j = 0..7. A message of
n <= 32 bytes is encoded by the word whose little-endian bytes are the message
followed by zeros, together with its length n, so that w[j] is lane j.

The lengths are n = 23 and n' = 24, and n XOR n' = 15. The only randomness is
one fresh uniform 256-bit word R.

1. Set x = R[4] and y = R[5] AND 00ffffff.
2. Compute

       a1 = K + x;   a1' = a1 XOR 15;   x' = a1' - K;   y' = y + a1 - a1'.

3. Message A has 23 bytes: its word is R with all bits from position 184
   upward cleared, so that w[0..3] = R[0..3], w[4] = x and w[5] = y. Message B
   has 24 bytes: its word has lanes 0..3 equal to R[0..3], lane 4 equal to x',
   lane 5 equal to y' and lanes 6 and 7 zero.
4. Output (A, B) and halt.

The top byte of y is zero, so byte 23 of the block of A is zero fill and A
really is the 23-byte message consisting of bytes 0..22. B is by definition
the 24-byte string given by its six words, whatever the value of its last
byte. The program is straight-line: it has no loop, no branch and no restart,
and it never evaluates the hash. Lanes 6 and 7 of R and the top byte of lane 5
are discarded.

## 4. Correctness for every value of the coin

**Theorem.** For every R the algorithm outputs two distinct messages A and B,
of 23 and 24 bytes, with H(A) = H(B).

Proof. By Section 1 each hash is a single compression on the zero-filled
block. The two executions have the same initial state except that v[14] is 23
for A and 24 for B. They have the same message words except w[4] and w[5]:
words 0..3 are R[0..3] in both, and words 6..15 are zero in both.

The first two column calls read neither v[14] nor w[4], w[5], so they leave
identical values in both executions. The third column call is the call of
Section 2, executed with (n, x, y) for A and with (n', x', y') for B, where
x' and y' are exactly those of the Lemma. Hence it leaves identical values in
v[2], v[6], v[10] and v[14]. From this point on the two executions have
identical states, and every remaining call, namely the fourth column call
with (w[6], w[7]) and the four diagonal calls with w[8..15], uses identical
message words. The final states are therefore identical, and so are the
digests. In fact all 16 output words agree, not only the 8 digest words.

A and B are distinct because their lengths differ. Both lie in the profile's
message domain. This is an ordinary collision of the complete hash. QED.

Distinct values of the 184 retained bits of R give distinct messages A, so
the construction yields 2^184 different colliding pairs.

## 5. Success probability

The probability space is the one fresh uniform 256-bit word R, for the fixed
target. By the theorem the success event contains every point of this space,
so the algorithmic success probability is exactly 1, which exceeds the
required 0.39. There are no failed trials, no restart and no success
amplification. This number concerns the algorithm's coin only, not confidence
in a review.

## 6. Charged time

One 1-round target compression costs one unit and every other primitive word
operation costs 1/C units with C = 222. The algorithm executes no target
compression, so its whole cost is ordinary word operations.

**Counting convention.** A 32-bit quantity is held in the low 32 bits of a
256-bit word. One *data operation* is one addition or subtraction modulo
2^256, one AND, OR or XOR, one shift, or one draw of a uniform random word.
Reduction modulo 2^32 is an explicit AND with M and is counted; one AND
reduces a short sum or difference correctly because 2^32 divides 2^256.

Memory traffic is charged in full: every data operation is charged as four
primitive operations, namely a load for each of at most two operands, the
operation itself, and a store of its result. Constants (K, M, 15, the byte
and lane masks) are operands covered by those loads; shift distances are
fixed in the instruction.

**Steps 1 to 3.**

| Step | Work | Data operations |
| --- | --- | ---: |
| 1 | draw R | 1 |
| 1 | x = (R >> 128) AND M | 2 |
| 1 | y = (R >> 160) AND 00ffffff | 2 |
| 2 | a1 = (K + x) AND M | 2 |
| 2 | a1' = a1 XOR 15 | 1 |
| 2 | x' = (a1' - K) AND M | 2 |
| 2 | y' = (y + a1 - a1') AND M | 3 |
| 3 | word of A: R AND (2^184 - 1) | 1 |
| 3 | word of B: (R AND (2^128 - 1)) OR (x' << 128) OR (y' << 160) | 5 |
| | total | 19 |

These 19 data operations are charged as 4 * 19 = 76 primitive operations. No
part of a compression is executed: the construction needs only the constant
K, not any intermediate state.

**Step 4.** The two message words are already stored as the results of step
3. Recording the two constant lengths and halting is charged as at most 4
further primitive operations.

**Total.** The algorithm uses no target compression and at most
W = 76 + 4 = 80 other primitive operations, so

    T = W/C = 80/222 < 0.37 < 1 = 2^0.

The program is straight-line, so these counts are the same for every value of
the coin: this is a worst-case bound, not an expectation, and it covers the
complete run at success probability 1, including message construction,
randomness and memory traffic. The base-2 logarithm of T is negative, and the
schema does not admit a negative time_log2, so the submitted bound is the
minimum time_log2 = 0, a bound of one full unit. That leaves a margin of 142
primitive operations: the bound would still hold if every data operation were
charged eleven primitive operations instead of four.

**No collision check is performed.** The algorithm does not hash its output
and does not compare digests. By the theorem of Section 4 its output is a
collision for every value of the coin, so a check could never change what is
output; it would be work that the algorithm does not do. The cost model
charges collision checking as part of the work an algorithm performs, and
here that work is zero. Anyone can confirm an output pair afterwards with two
hash evaluations, and the declared experiment has the organizer do exactly
that; this is verification of the claim, not a step of the attack. For
transparency: a different algorithm that also recomputed and compared both
digests would spend two target compressions plus their input and output
handling, under 4 units in total. That variant outputs exactly the same
pairs and is not the submitted algorithm.

## 7. Memory, preprocessing and advice

The straight-line program has at most 80 primitive instructions, and no
compression routine is part of it. Bound the code by 128 instruction
templates of at most four 256-bit words each (opcode and up to three
operands): 512 words, which is 2^14 bytes. Data consists of fewer than 64
words: the coin word, x, y, a1, a1', x', y', the two message-encoding words,
the constants K, M and 15, and the byte and lane masks. That is below 2^11
bytes. Peak memory is therefore below 2^14 + 2^11 < 2^15 bytes. Nothing else
is retained: there is no table, no stored message database and no stored
collision.

There is no preprocessing phase: all work is the run counted in Section 6.
There is no nonuniform advice: the program contains only public constants of
the target (K is the sum of two IV words) and fixed masks. The fields
preprocessing_log2 = 0 and nonuniform_advice_log2_bytes = 0 are upper bounds
of one unit and one byte, because the schema cannot express the logarithm of
zero.

## 8. Evidence, scope and field meanings

The supporting evidence is the complete algorithm, the exact target
description, the proof of Sections 2 and 4, and the operation count of
Section 6. The argument is exact for all 2^256 coin values and uses no
sampled quantity.

The package also declares one executable experiment,
`closed-form-collisions`, whose program `experiments/collide.py` implements
steps 1 to 3 and returns the pair (A, B) for each organizer seed. It does not
evaluate the hash itself; the organizer runner recomputes both digests. The
seed is expanded with SHAKE-256 into R only to make runs reproducible. No
probability claim rests on that expansion, since the theorem holds for every
coin value. The proof predicts that every trial returns a 23-byte and a
24-byte message forming a full collision. This run is an independent check of
the identity on concrete inputs; it is not offered as evidence of attack
cost, which is established by Section 6 alone. The certificate manifest
declares one witness, `zero-coin-pair`, which is the pair described next.

For hand checking, the coin R = 0 gives x = y = 0, a1 = 5bf2cd1d,
a1' = 5bf2cd12, x' = fffffff5 and y' = 0000000b. Message A is 23 zero bytes.
Message B is the 24 bytes

    00000000 00000000 00000000 00000000 f5ffffff 0b000000

written as six groups of four bytes. Both have the digest

    f759c198040e5c92fdd8a52dea06b624254433662bfc29951599a35b626a5ce0.

This pair is the declared witness certificate, so the organizer's
deterministic checker recomputes both digests. It illustrates the output; it
is not used by the algorithm, which stores no collision and would produce
this pair itself from the coin R = 0.

Scope and limitations:

- The result is specific to the 1-round prefix. The pairs produced here do
  not collide when two or more rounds are kept. No claim is made about
  blake3-r2 or about full BLAKE3.
- The two messages have different lengths, 23 and 24 bytes. The construction
  relies on the true block length being a compression input, as the target
  profile specifies.
- No literature survey was done for this 1-round property and no priority or
  novelty claim is made.
- The time bound depends on the counting convention of Section 6, which
  charges four primitive operations per data operation, and on the algorithm
  performing no collision check, as explained there. It is an upper bound
  under that convention, not a measured running time.

The claim fields mean:

- time_log2 = 0 bounds total charged time by 2^0 = 1 unit; the count of
  Section 6 is below 0.37 units.
- memory_log2_bytes = 15 bounds simultaneous storage by 2^15 bytes.
- preprocessing_log2 = 0 and nonuniform_advice_log2_bytes = 0 are as explained
  in Section 7; actual preprocessing and advice are zero.
- success_probability = 1 is the exact value proved in Section 5.

The required baseline_improved identifier blake3-r1-nominal-v2 names the
organizer's nominal display reference 128, which is not an established attack,
a qualified baseline or a security bound. The claimed scalar 0 is lower than
that display value. Whether a qualified result improves the Yukon incumbent
is decided separately, and no Pareto dominance claim follows from the scalar.
