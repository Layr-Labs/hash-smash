# A closed-form collision for 1-round BLAKE3

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
separately reported resource bound.

This exploratory package targets blake3-r1-prefix-v1. It gives an explicit
randomized algorithm that outputs a 23-byte message and a 24-byte message with
the same complete 1-round BLAKE3-256 digest. The output is a collision for
every value of the algorithm's random coin, so the success probability is 1.
Total charged time is below 3.6 target-compression units, including a final
verification by two complete hash evaluations. The claimed bound is 2^2 = 4
units, so the claimed scalar is 2. Peak memory is below 2^20 bytes.

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
so the single root compression above covers every hash it evaluates.

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
4. Verify: evaluate the complete hashes H(A) and H(B) and check that they
   agree on all 256 bits. Output (A, B) if the check passes and halt with
   failure otherwise.

The top byte of y is zero, so byte 23 of the block of A is zero fill and A
really is the 23-byte message consisting of bytes 0..22. B is by definition
the 24-byte string given by its six words, whatever the value of its last
byte. The program is straight-line: it has no loop, no restart, and no branch
before step 4. Lanes 6 and 7 of R and the top byte of lane 5 are discarded.

## 4. Correctness for every value of the coin

**Theorem.** For every R the algorithm outputs two distinct messages A and B,
of 23 and 24 bytes, with H(A) = H(B); the check of step 4 never fails.

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
operation costs 1/C units with C = 222.

**Counting convention.** A 32-bit quantity is held in the low 32 bits of a
256-bit word. One *data operation* is one addition or subtraction modulo
2^256, one AND, OR or XOR, one shift, one comparison, one conditional
branch, or one draw of a uniform random word.
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
part of a compression is executed in steps 1 to 3: the construction needs
only the constant K, not any intermediate state.

**Step 4.**

- Lanes R[0..3], needed as compression inputs: one AND, then three times
  shift and AND, which is 7 data operations, charged as 28 primitive
  operations.
- Two complete hash evaluations: 2 target compressions, charged 2 units. Their
  input and output handling is charged separately at 80 primitive operations
  each: a load and a store for each of the 16 initial state words (including
  the block length), each of the 16 message words (ten of them the constant
  zero) and each of the 8 digest words. This is 160 primitive operations.
- Digest equality: 8 XORs, 7 ORs, a comparison with zero and a branch. These
  17 data operations are charged as 68 primitive operations. Distinctness
  needs no test because the two lengths are the fixed constants 23 and 24.
- Storing the two message words and the two lengths and halting: at most 8
  primitive operations.

Step 4 therefore costs 2 units and 264 primitive operations.

**Total.** The algorithm uses H = 2 target compressions and
W = 76 + 264 = 340 other primitive operations, so

    T = H + W/C = 2 + 340/222 < 2 + 1.54 = 3.54 < 4 = 2^2.

The program is straight-line, so these counts are the same for every value of
the coin: this is a worst-case bound, not an expectation, and it covers the
complete run at success probability 1, including message construction,
randomness, memory traffic and collision checking. The submitted bound
time_log2 = 2 leaves a margin of more than 0.46 units, that is more than 100
primitive operations, over the count above.

## 7. Memory, preprocessing and advice

The straight-line program has 340 primitive instructions. A direct
implementation of the compression of Section 1 adds fewer than 2000
instruction templates. Bound the whole code by 4096 templates of at most four
256-bit words each (opcode and up to three operands): 2^14 words, which is
2^19 bytes. Data consists of fewer than 512 words: the 16 state words, 16
message words, the coin word, the two message-encoding words, two digests,
the public constants, and the temporaries of steps 1 to 4 and of the
compression. That is below 2^14 bytes. Peak memory is therefore below
2^19 + 2^14 < 2^20 bytes. Nothing else is retained: there is no table, no
stored message database and no stored collision.

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

The package also declares two executable experiments. The first is
`closed-form-collisions`, whose program `experiments/collide.py` implements
steps 1 to 3 and returns the pair (A, B) for each organizer seed. It does not
evaluate the hash itself: the two hash evaluations and the comparison of
step 4 are carried out by the organizer runner, which recomputes both digests. The
seed is expanded with SHAKE-256 into R only to make runs reproducible. No
probability claim rests on that expansion, since the theorem holds for every
coin value. The proof predicts that every trial returns a 23-byte and a
24-byte message forming a full collision. This run is an independent check of
the identity on concrete inputs; it is not offered as evidence of attack
cost, which is established by Section 6 alone. The second experiment,
`second-message-family`, and two further witnesses concern Section 9 only
and are described there. The certificate manifest declares three witnesses;
the first, `zero-coin-pair`, is the pair described next.

For hand checking, the coin R = 0 gives x = y = 0, a1 = 5bf2cd1d,
a1' = 5bf2cd12, x' = fffffff5 and y' = 0000000b. Message A is 23 zero bytes.
Message B is the 24 bytes

    00000000 00000000 00000000 00000000 f5ffffff 0b000000

written as six groups of four bytes. Both have the digest

    f759c198040e5c92fdd8a52dea06b624254433662bfc29951599a35b626a5ce0.

This pair is the first declared witness certificate, so the organizer's
deterministic checker recomputes both digests. It illustrates the output; it
is not used by the algorithm, which stores no collision and would produce
this pair itself from the coin R = 0.

Scope and limitations:

- The result is specific to the 1-round prefix. The identity is proved for
  one round only. When two or more rounds are kept, the later rounds read
  w[4] and w[5] again and the two executions separate: the witness pair
  above has different digests at 2, 3, 4, 5, 6 and 7 rounds. No claim is made
  about blake3-r2 or about full BLAKE3.
- The two messages have different lengths, 23 and 24 bytes. The construction
  relies on the true block length being a compression input, as the target
  profile specifies.
- No literature survey was done for this 1-round property and no priority or
  novelty claim is made. Prior work that we know of only through another
  team's public note is named below under "Relation to other work known to
  us".
- The time bound depends on the counting convention of Section 6, which
  charges four primitive operations per data operation and includes the
  redundant final verification. It is an upper bound under that convention,
  not a measured running time. Steps 1 to 3 alone, without the verification,
  cost 76 primitive operations, less than 0.35 of a unit; that reading is
  not claimed here. The submitted bound is 4 units. It is the only bound
  this package claims; no lower figure is offered as an alternative or as a
  fallback.
- Step 4 compares the digests and does not test that the two messages
  differ, because their lengths are the constants 23 and 24 (Section 6).
  Made explicit, that test is a comparison of the two stored lengths and a
  branch: two data operations, 8 primitive operations under the convention
  of Section 6. The total would then be 2 units and 348 primitive
  operations, less than 3.57 units and still below the bound of 4 units.
- The verification is charged because the organizer's files name it. The
  cost model lists "collision checking" among the items of total time
  (`cost-models/collision-frontier-v5.json`, field `total_time_includes`).
  `docs/CANDIDATE_QUALIFICATION.md`, lines 48 to 50, asks the proof to
  specify the "collision check", and its lines 58 to 59 say "Charge
  preprocessing, message construction, all trials including failures,
  randomness, sorting/lookups, verification and restarts."
  `docs/FRONTIER_LANES.md`, lines 65 to 66, says "Preprocessing, failed
  trials, verification, advice and code storage count in the resource
  ledger." The line numbers are those of repository commit 86f1102. Step 4
  of the algorithm and its charge in Section 6 follow these sentences as
  written. `docs/CANDIDATE_QUALIFICATION.md` is the organizer's guide for
  authors of baseline packages. The baseline package that the organizer's
  repository carries for this track at that commit says of its own final
  check: "Verification failure cannot occur in the exact RAM model because
  the original digests came from the same deterministic H. This explicit
  defensive check is still charged." That check also tests that the two
  messages are distinct; for this package see the previous item.

Relation to other work known to us. This paragraph is context only; nothing
in Sections 1 to 7 depends on it, and it is a description of what we read,
not a priority claim.

- Other entries on this track. In the public listing of this track read on
  2026-10-07 at 01:56 UTC (58 submissions), the two entries with the lowest
  claimed scalar, 0 (754f0f26 and 724598e3), each build two messages of the
  same length, 64 bytes. Their two final states differ, and the difference
  cancels in the feed-forward XOR v[i] XOR v[i+8]. Here the two messages
  have different lengths and their final states are identical (Section 4):
  the only difference between the two compressions, the block length, is
  removed inside the one call that reads it. We found no other note in that
  listing that describes a collision between messages of different lengths,
  apart from our own earlier filing of this construction with a claim of 0
  (beea45d4, filed on 2026-10-05 and cancelled by us before it was judged).
  The same as in the other entries are the target, the cost model and the
  kind of evidence: an exact identity, witness certificates and
  organizer-run experiments. The claimed scalar, 2, is higher than the
  lowest claimed scalars of that listing.
- One round is invertible: prior work, not ours. That one round, for a
  fixed chaining value, counter, block length and flags, is an injective
  map from the sixteen message words to the state, with an explicit
  inverse, is known. The public note of submission bd119446 on this track
  (hybridnoise, 2026-10-05 12:47 UTC, some hours before our first filing)
  attributes it to Aumasson, Guo, Knellwolf, Matusiewicz and Meier,
  "Differential and invertibility properties of BLAKE", FSE 2010 (IACR
  ePrint 2010/043, Sections 5.1 and 5.2), and states that deterministic
  collisions and preimages of the complete 1-round hash on 64-byte
  messages follow from it. We have not read the paper and rely on that
  note for the citation. The Remark of Section 9 proves the injectivity
  again in a few lines only because the package has to be self-contained;
  it is credited to that work and not claimed. This package uses it only
  in that Remark, to say which one-block pairs can have identical states.
- Two rounds. The Lemma of Section 2 is also the first step of this
  project's entries on the track blake3-r2-exploratory (17bba2ae, 5ceb1802,
  04638ed8, c47c1a80, c66f230d). There the cancellation only makes the
  states after the first round equal, and those entries pay for a search:
  their claimed scalars lie between 97.6 and 123.5. They are separate
  claims and are not relied on here.
- An independent derivation. Grok (xAI; the version was not recorded), in
  a chat session of the project owner's that is separate from the sessions
  that wrote this package, found the case of lengths 24 and 25: when
  K + w[4] is even, w[4] + 1 and w[5] - 1 give the second message. That is
  the Lemma with n XOR n' = 1, and a case of Corollary 1 in Section 9. It is
  not part of this package's claimed algorithm.

The claim fields mean:

- time_log2 = 2 bounds total charged time by 2^2 = 4 units.
- memory_log2_bytes = 20 bounds simultaneous storage by 2^20 bytes.
- preprocessing_log2 = 0 and nonuniform_advice_log2_bytes = 0 are as explained
  in Section 7; actual preprocessing and advice are zero.
- success_probability = 1 is the exact value proved in Section 5.

The required baseline_improved identifier blake3-r1-nominal-v2 names the
organizer's nominal display reference 128, which is not an established attack,
a qualified baseline or a security bound. The claimed scalar 2 is lower than
that display value. Whether a qualified result improves the Yukon incumbent
is decided separately, and no Pareto dominance claim follows from the scalar.

## 9. What else the Lemma gives: proved here, not claimed

Nothing in this section is part of the claimed algorithm. The claim, its
cost and its success probability are those of Sections 3 to 7 and would
stand unchanged if this section were removed. The statements are included
because each follows from the Lemma in a few lines, and because they change
what the result means: the block length yields a second message for a given
message, not only some colliding pairs.

H is the 1-round hash. As in Section 1, a message of n <= 64 bytes is one
chunk of one block: one root compression on the message followed by 64 - n
zero bytes, with flags 11 and block length n. The profile gives the same
rule for the empty message (n = 0): one empty block with block length 0.

**Corollary 1 (one-block messages).** Let A be any message of n bytes,
0 <= n <= 63, with block words w[0..15], and let n' be any length with
max(n + 1, 24) <= n' <= 64. Put

    a1 = K + w[4],   a1' = a1 XOR n XOR n',
    x' = a1' - K,    y' = w[5] + a1 - a1'.

Let B be the first n' bytes of the block whose words are w[0..3], x', y',
w[6..15]. Then B is a message of n' bytes, B differs from A, and
H(B) = H(A).

Proof. Bytes n' to 63 of that block lie in words 6 to 15, because n' >= 24.
Those words are words of A's block, whose bytes from position n on are zero,
and n' > n. So bytes n' to 63 are zero, and the zero-filled block of the
n'-byte string B is exactly the block with words w[0..3], x', y', w[6..15].
The two hashes are single compressions with the same initial state except
v[14] = n for A and n' for B, and the same message words except words 4 and
5. The first two column calls read neither v[14] nor words 4 and 5. The
third leaves identical values by the Lemma. Every later call sees identical
states and identical words. So the final states are identical and
H(B) = H(A). B differs from A because the lengths differ. QED.

The algorithm of Section 3 is the case n = 23, n' = 24 with a random A. The
bound n' >= 24 is what makes the statement unconditional: for n' < 24 the
same replacement gives a valid message only when the bytes of x' and y' from
position n' on happen to be zero.

So the corollary does not say that every pair of lengths works. Of the
2,080 pairs of different lengths from 0 to 64 it covers 1,804: the 24 * 41
pairs with n < 24 <= n' and the 820 pairs with 24 <= n < n'. The other 276
pairs have both lengths below 24. For n' <= 20 the replacement never gives
a valid message: A has fewer than 20 bytes, so w[5] = 0 and
y' = a1 - a1', which is not zero because n and n' differ, while an n'-byte
message with n' <= 20 has word 5 equal to zero. That is 210 pairs. For
21 <= n' <= 23 it gives a valid message for every A of at most 16 bytes
(51 pairs; there w[4] = w[5] = 0, so the outcome does not depend on A, and
each pair was evaluated), and for some A but not for others in the
remaining 15 pairs (an example of each kind exists for every pair). For
the empty message, for example, the replacement gives the valid 23-byte
message

    00000000 00000000 00000000 00000000 edffffff 130000

(same digest as the empty message, printed below), and it gives no valid
17-byte message. The Lemma itself, a statement about the one G call, holds
for every pair of block lengths.

Three instances, written as groups of four bytes:

- The empty message and the 24-byte message

      00000000 00000000 00000000 00000000 e8ffffff 18000000

  both have the digest

      111b0e9672ca328b7216e00d36bc0449f86e5e5f919ef9ba0c70ddd58581b23c.

  Here a1 = K = 5bf2cd1d, a1' = K XOR 24 = 5bf2cd05, x' = ffffffe8 and
  y' = 00000018. No certificate file is declared for this pair.
- The 3-byte message 616263 ("abc") and the 24-byte message

      61626300 00000000 00000000 00000000 e9ffffff 17000000

  both have the digest

      a406784b1f6377cd7acd513b8c4af00bc0b8d7b028ddad36e085043c3d6bab5f.

  This is the declared witness `abc-pair`.
- The 63-byte message with bytes 00, 01, ..., 3e and the 64-byte message
  that agrees with it except for bytes 16 to 23, which become
  35111213 ef141617, and ends with one further zero byte, both have the
  digest

      a88352860d5f627109bc7d7f88bcf25994423bcedb57354ee0f419df564b0c5b.

  This is the declared witness `full-block-pair`.

The declared experiment `second-message-family` (program
`experiments/family.py`) draws, for each organizer seed, a length n in 0..63,
a length n' in the allowed range and n message bytes, and returns A and B as
defined above. It does not evaluate the hash; the organizer runner
recomputes both digests. The corollary predicts a full collision in every
trial. Like the first experiment, this run checks an exact identity on
concrete inputs and is not evidence of cost.

**Corollary 2 (longer messages).** Let A be a message of L > 64 bytes whose
last block holds n <= 63 bytes, where n = ((L - 1) mod 64) + 1. Let h be the
chaining value that enters the compression of the last block of the last
chunk (h is the IV if that block is the first block of its chunk), and let
K_h = h[2] + h[6]. Choose n' with max(n + 1, 24) <= n' <= 64, apply the
replacement of Corollary 1 to the last block with K_h in place of K, and let
B be A with its last n bytes replaced by the first n' bytes of the new
block. Then B has L - n + n' bytes, differs from A, and H(B) = H(A).

Proof. In the complete hash of the profile, a message is cut into chunks of
1024 bytes and each chunk into blocks of 64 bytes; only the last block of
the last chunk may be shorter. Every block is compressed from the state
v[0..7] = h, the chaining value of its chunk so far (the IV for the first
block of a chunk), v[8..11] = IV[0..3], v[12] and v[13] = a counter that
depends only on the position of the chunk, v[14] = the number of message
bytes in the block, and v[15] = flags that depend only on the position of
the block (first or last of its chunk, root or not). The outputs of the
chunks are combined by parent compressions whose inputs are chaining values
only.

A and B have the same number of chunks and of blocks, because the last block
of B still has at most 64 bytes, and they agree in every block but the last.
So every compression before the last block has identical inputs, h is the
same for both, and the two last-block compressions have the same h, counter
and flags. They differ only in v[14] and in words 4 and 5. The proof of the
Lemma uses about v[2], v[6] and v[10] only that they are the same in both
executions and that v[2] + v[6] = K; so it applies to this compression with
K_h in place of K. The block of B is honestly zero filled, by the argument
of Corollary 1. Hence the final states of the two last-block compressions
are identical, so are their sixteen output words, and every later
compression, if there is one, receives identical inputs. QED.

Finding h costs the compressions of the earlier blocks of the last chunk. No
cost is claimed for either corollary. No organizer-run experiment is
declared for Corollary 2; it rests on the proof above.

**Remark (one-block messages of equal length cannot have identical states,
and the Lemma is the only way for different lengths).** For a fixed
chaining value, counter, block length and flags, one round is an injective
map from the sixteen message words to the sixteen state words.

This statement is prior work and is not claimed by this package: see the
paragraph "Relation to other work known to us" in Section 8. The proof
below is included only to keep the package self-contained.

Proof. Write a G call with inputs (a, b, c, d), words (x, y), intermediate
values a1, d1, c1, b1 and outputs (a2, b2, c2, d2) as in Section 2, and let
ROL rotate a 32-bit word left. Reading the eight assignments of G backwards
gives

    d1 = ROL(d2, 8) XOR a2      c1 = c2 - d2      b1 = ROL(b2, 7) XOR c2
    c  = c1 - d1                b  = ROL(b1, 12) XOR c1
    a1 = ROL(d1, 16) XOR d      x  = a1 - a - b   y  = a2 - a1 - b1.

Take any final state. (i) For each diagonal call, the first five equations
give its b and c inputs from its four outputs. Over the four diagonal calls
these inputs are v[4..7] and v[8..11] as they stand after the column step.
(ii) In each column call the inputs (a, b, c, d) are the known initial
values and the outputs b2 and c2 are now known, so b1 = ROL(b2, 7) XOR c2,
c1 = ROL(b1, 12) XOR b, d1 = c1 - c, a1 = ROL(d1, 16) XOR d, x = a1 - a - b,
d2 = c2 - c1, a2 = ROL(d2, 8) XOR d1 and y = a2 - a1 - b1 are determined.
This fixes w[0..7] and the whole state after the column step. (iii) Now
every diagonal call has known inputs a and d, and the last three equations
give its two words. This fixes w[8..15]. So at most one block reaches a
given final state. QED.

Two consequences. First, two different messages of the same length n <= 64
have different blocks and the same initial state, hence different final
states: a collision between them has to cancel a nonzero state difference in
the XORs v[i] XOR v[i+8] of the output. That is how the equal-length
constructions on this track that we read work. This is a statement about
one-block messages; longer messages of equal length can already agree
after an earlier compression. Second, for lengths n != n'
and a given block for length n, at most one block for length n' has the same
final state, and by the Lemma it is the block with words w[0..3], x', y',
w[6..15]. So the pairs of Corollary 1, together with those pairs of lengths
both below 24 for which that block happens to be a valid n'-byte message,
are all the pairs of one-block messages with identical final states.
