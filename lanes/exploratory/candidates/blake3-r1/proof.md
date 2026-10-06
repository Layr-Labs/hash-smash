# A deterministic two-word collision for 1-round BLAKE3

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
separately reported resource bound.

This exploratory package targets `blake3-r1-prefix-v1`. It gives a
deterministic, straight-line algorithm that always outputs two distinct 64-byte
messages with equal complete 1-round BLAKE3-256 digests. It performs no search,
no sampling and no full compression. Its total charged time is at most 416
primitive word operations, i.e. at most 416/222 < 1.874 target-compression
units. The claimed scalar is 1.5, a bound of 2^1.5 = 2.83 units (628
operations), which leaves headroom for stricter operation-counting conventions.
Success probability is exactly 1. No heuristic is used, and the heuristic list
is empty.

The idea is a complementation property of the BLAKE3 G function: when one
intermediate word is 0 (or 2^31), complementing G's first output word by a
change of its second message word complements all four of its output words.
After one round, the digest pairs the outputs of two diagonal G calls by XOR, so
complementing both of them leaves the digest unchanged.

## 1. Exact complete hash evaluated

Every message produced has exactly 64 bytes (bit length 512 < 2^64), so the
profile's tree has one chunk, one block, no parent node, and exactly one
compression: the root compression, with flags CHUNK_START | CHUNK_END | ROOT =
1 | 2 | 8 = 11, true block length 64, chunk counter 0 and root-output counter 0.
There is no padding block, key, or derivation flag. This is the same reduction
the organizer's generic package uses, and it matches `verifier/blake3.py`:
`_chunk_output` returns the single block with CHUNK_START | CHUNK_END, and the
root call ORs in ROOT.

Decode the message into little-endian 32-bit words m[0..15]. All additions are
modulo 2^32, `~` is bitwise complement on 32 bits, and ROR/ROL rotate within a
32-bit lane. The IV is

    6a09e667 bb67ae85 3c6ef372 a54ff53a 510e527f 9b05688c 1f83d9ab 5be0cd19.

The initial state is v[0..7] = IV, v[8..11] = IV[0..3], v[12..15] =
(0, 0, 64, 11). G(a,b,c,d,x,y) acts on v as

    a1 = a + b + x;   d1 = ROR(d ^ a1, 16)
    c1 = c + d1;      b1 = ROR(b ^ c1, 12)
    a2 = a1 + b1 + y; d2 = ROR(d1 ^ a2, 8)
    c2 = c1 + d2;     b2 = ROR(b1 ^ c2, 7)

and writes (a2, b2, c2, d2) back to positions (a, b, c, d). The single round is
the column step G(0,4,8,12,m0,m1), G(1,5,9,13,m2,m3), G(2,6,10,14,m4,m5),
G(3,7,11,15,m6,m7), then the diagonal step G(0,5,10,15,m8,m9),
G(1,6,11,12,m10,m11), G(2,7,8,13,m12,m13), G(3,4,9,14,m14,m15). With one round
the message permutation is never applied. The digest is LE32(o[0]) || ... ||
LE32(o[7]) with o[i] = v[i] ^ v[i+8]. The other feed-forward words
o[8..15] = v[i+8] ^ IV[i] are not part of the 256-bit digest.

This is the ordinary hash with its real IV, flags, counter, length and
feed-forward. It is not a free-start, compression-only, truncated-output or
different-round collision.

## 2. How the digest depends on the diagonal step

The four diagonal G calls touch the disjoint index sets {0,5,10,15},
{1,6,11,12}, {2,7,8,13} and {3,4,9,14}, which partition 0..15. Each reads only
column-step outputs and its own two message words, so none affects another's
input, and their order does not matter. Write D0 = G(0,5,10,15,m8,m9) and
D2 = G(2,7,8,13,m12,m13). After the round:

| Digest word | = | from | and from |
| --- | --- | --- | --- |
| o[0] | v[0] ^ v[8] | D0 output a | D2 output c |
| o[2] | v[2] ^ v[10] | D2 output a | D0 output c |
| o[5] | v[5] ^ v[13] | D0 output b | D2 output d |
| o[7] | v[7] ^ v[15] | D2 output b | D0 output d |
| o[1], o[3], o[4], o[6] | v[1]^v[9], v[3]^v[11], v[4]^v[12], v[6]^v[14] | only G(1,6,11,12,...) and G(3,4,9,14,...) | |

So if, between two messages, the column step is identical, the two other
diagonal calls are identical, and every output word of D0 and of D2 is bitwise
complemented, then each of o[0], o[2], o[5], o[7] is the XOR of two complemented
words, which is unchanged, and o[1], o[3], o[4], o[6] are unchanged outright.

## 3. Two lemmas about G

**Lemma 1 (complementation).** Fix (a, b, c, d, x) such that
c1 = c + ROR(d ^ (a + b + x), 16) is 0 or 2^31. For any y, let
(a2, b2, c2, d2) = G(a,b,c,d,x,y) and y' = y - 2*a2 - 1. Then
G(a,b,c,d,x,y') = (~a2, ~b2, ~c2, ~d2).

*Proof.* a1, d1, c1 and b1 depend only on (a, b, c, d, x), so they are the same
in both evaluations. Primes mark the second evaluation. Recall ~z = -z - 1
modulo 2^32.

1. a2' = a1 + b1 + y' = (a1 + b1 + y) - 2*a2 - 1 = a2 - 2*a2 - 1 = -a2 - 1 = ~a2.
2. d2' = ROR(d1 ^ ~a2, 8) = ROR(~(d1 ^ a2), 8) = ~ROR(d1 ^ a2, 8) = ~d2,
   because complementing commutes with XOR by a fixed word and with rotation.
3. c2' = c1 + ~d2 = c1 - d2 - 1, while ~c2 = -c1 - d2 - 1. These are equal
   exactly when 2*c1 = 0 modulo 2^32, i.e. when c1 is 0 or 2^31, which holds by
   hypothesis. So c2' = ~c2.
4. b2' = ROR(b1 ^ ~c2, 7) = ~ROR(b1 ^ c2, 7) = ~b2. ∎

**Lemma 2 (solving for c1).** For any (a, b, c, d) and t in {0, 2^31}, the word
x = (ROL(t - c, 16) ^ d) - a - b gives c1 = t.

*Proof.* a1 = a + b + x = ROL(t - c, 16) ^ d, so
d1 = ROR(d ^ a1, 16) = ROR(ROL(t - c, 16), 16) = t - c, and c1 = c + d1 = t. ∎

Both lemmas are exact identities over 32-bit words; neither uses probability.

## 4. The algorithm and why it always succeeds

Fix the free words m[0..7], m[9], m[10], m[11], m[13], m[14], m[15]. The scored
algorithm sets all of them to zero and uses t = 0 for both solves; Section 8
shows a second executed instance with other values and t = 2^31.

1. Initialise v as in Section 1 and run the four column G calls on m[0..7].
2. Using Lemma 2 on the column-step state, set
   m[8] = (ROL(t - v[10], 16) ^ v[15]) - v[0] - v[5] (the inputs of D0) and
   m[12] = (ROL(t - v[8], 16) ^ v[13]) - v[2] - v[7] (the inputs of D2).
   Both are computed from the same column-step state, which is correct because
   D0 and D2 read disjoint, still-unmodified words.
3. Run D0 = G(0,5,10,15,m8,m9) and D2 = G(2,7,8,13,m12,m13) to obtain their
   first outputs A0 = v[0] and A2 = v[2].
4. Set m'[i] = m[i] for all i except m'[9] = m[9] - 2*A0 - 1 and
   m'[13] = m[13] - 2*A2 - 1.
5. Output M = LE32(m[0]) || ... || LE32(m[15]) and
   M' = LE32(m'[0]) || ... || LE32(m'[15]).

The diagonal calls G(1,6,11,12,...) and G(3,4,9,14,...) are never evaluated:
their values are irrelevant to the construction.

**Theorem.** For every choice of free words and of t, M != M' and
H(M) = H(M'), where H is the complete 1-round BLAKE3-256 of Section 1.

*Proof.* M and M' agree on m[0..7], so the column step gives the same state.
They agree on m[10], m[11], m[14], m[15], so G(1,6,11,12,...) and
G(3,4,9,14,...) give identical outputs. For D0, Step 2 makes c1 = t by
Lemma 2, so Lemma 1 with y = m[9] and y' = m'[9] shows that D0 outputs the
complement of all four words on M'. The same holds for D2 with m[13], m'[13].
By Section 2, all eight digest words are therefore equal. Finally
m'[9] - m[9] = -(2*A0 + 1) is odd, so it is nonzero modulo 2^32 and M != M'.
Both messages have 64 bytes, inside the domain. ∎

There is no random coin, no trial that can fail, and no checking step whose
outcome matters, so the success probability is exactly 1. The construction is
not a search, so no expected-cost argument is needed.

The family is large: 14 free words and two choices of t give 2^450 distinct
messages M, each with its partner M'. Nothing below depends on that count.

## 5. Fully charged cost under collision-frontier-v5

Model: the classical 256-bit word RAM of the cost model, with registers and
explicit loads and stores. Every primitive (load, store, add, subtract, AND,
OR, XOR, NOT, shift, comparison, branch) costs 1/C with C = 222. No full target
compression is evaluated, so no unit-cost compression is charged, and every G
step is charged as primitives. A 32-bit lane is held in a 256-bit word.
Reduction modulo 2^32 is an AND with 2^32-1 after each add or subtract chain.
A 32-bit rotation is two shifts, an OR and an AND. This follows the explicit
256-bit rotation convention the organizer's reference cost script states.

**One G call** is 30 arithmetic/logical/shift operations: a1 (add, add, and =
3), d1 (xor, shr, shl, or, and = 5), c1 (add, and = 2), b1 (5), a2 (3),
d2 (5), c2 (2), b2 (5). It also makes 10 memory accesses: loads of a, b, c, d,
x, y and stores of the four outputs. Temporaries stay in registers.

**One solve (Lemma 2)** is 10 operations: t - c and mask (2), ROL by 16
(shl, shr, or, and = 4), XOR with d (1), two subtractions and a mask (3). It
also makes 5 memory accesses: four state loads and one store of x.

| Step | Arithmetic / logic / shift | Loads / stores |
| --- | ---: | ---: |
| Initialise 16 state words and 16 message lanes (immediates) | 0 | 32 |
| Four column G calls | 120 | 40 |
| Two solves, m[8] and m[12] | 20 | 10 |
| D0 and D2 | 60 | 20 |
| m'[9], m'[13]: shift, subtract, subtract, mask, each | 8 | 6 |
| Serialise M and M' as four 256-bit words: 7 shifts + 7 ORs per word | 56 | 36 |
| **Subtotal** | **264** | **144** |
| Control (halt, output) | ≤ 8 | |

The total is at most 264 + 144 + 8 = 416 primitive operations. The program is
straight-line, with no loops, branches on data, restarts or failed trials:

    T <= 416 / 222 < 1.874 target-compression units, log2(T) < 0.91.

**Claimed bound: time_log2 = 1.5**, i.e. T <= 2^1.5 = 2.83 units, or 628
operations. The 212-operation headroom is deliberate. It covers reasonable
stricter conventions, for example charging a load for every immediate operand
(shift amounts, masks and constants), which adds at most 6 * 16 = 96 operations
for the six G calls and fewer than 20 elsewhere. It also covers charging a
separate mask after every individual addition rather than after each chain.
Every category in the cost model's `total_time_includes` is covered:

- preprocessing: none;
- message and differential construction: all of the table;
- randomness: none;
- trials including failures: exactly one deterministic run;
- sorting and lookup: none;
- collision checking: none is needed for correctness. The theorem guarantees
  the output, and an optional final check is not part of the scored algorithm;
- restart and amplification: none.

For comparison only, re-hashing both outputs as a defensive check would add two
target compressions plus a 256-bit comparison, giving T < 2 + 1.874 + 0.01 < 4,
i.e. log2(T) < 2. The scored algorithm does not include that check.

## 6. Memory

Data: 16 state words, 18 message lanes (16 shared plus the two changed ones), 4
serialised output words and a constant number of temporaries, fewer than 64
256-bit words = 2^11 bytes. Code: a straight-line program of at most 416
instructions. Encoding each in at most four 256-bit words (opcode and up to three
operands) takes at most 416 * 128 = 53,248 bytes < 2^16. Peak memory, code
included, is below 2^16 + 2^11 < 2^17 bytes: `memory_log2_bytes = 17`. No table,
advice, precomputed collision or retained randomness exists.

## 7. Claim fields

- `time_log2 = 1.5`: total charged time at most 2^1.5 target-compression
  units. The explicit tally gives at most 1.874.
- `memory_log2_bytes = 17`: peak storage, including code, below 2^17 bytes.
- `preprocessing_log2 = 0`: there is no preprocessing. 0 is the schema's
  minimum and bounds it by one unit; the actual amount is zero.
- `success_probability = 1`: deterministic success (Section 4), above the
  required 0.39.
- `nonuniform_advice_log2_bytes = 0`: no advice. The schema cannot express
  log2(0). The algorithm does not read the certificates.
- `heuristics = []`: every step is an exact identity.

## 8. Evidence: executed witnesses

Two pairs produced by this construction are declared in
`certificates/manifest.json` and checked by the organizer's deterministic
certificate checker against `verifier.blake3.blake3(rounds=1)`:

1. `blake3-r1-zero-free-words` is the scored instance: every free word is 0
   and t = 0. As words:

   | Word | M | M' |
   | --- | --- | --- |
   | m[0..7], m[10], m[11], m[14], m[15] | 0 | 0 |
   | m[8] (solved) | 0xbd8ae831 | 0xbd8ae831 |
   | m[9] | 0 | 0x48e28fd3 |
   | m[12] (solved) | 0x580179c0 | 0x580179c0 |
   | m[13] | 0 | 0x34efa635 |

   The 64-byte messages (hex, little-endian words) and their common digest:

       M  = 000000000000000000000000000000000000000000000000000000000000000031e88abd000000000000000000000000c0790158000000000000000000000000
       M' = 000000000000000000000000000000000000000000000000000000000000000031e88abdd38fe2480000000000000000c079015835a6ef340000000000000000
       H  = a60b648064d9445baa8f41405ca2283f497c0ecbe4ab151c020d61c692d60301

2. `blake3-r1-seeded-free-words-c1-2p31` uses pseudo-random free words and
   t = 2^31 for both solves, showing that the theorem's freedom is real rather
   than a property of zero inputs. Its digest is
   38dd9debb1db03944ede2ecbbbec1c4141af8304938a1713afe23484aea31267.

These are reproducibility evidence for the construction, not inputs to it. The
claim does not rest on them; Sections 3 and 4 prove the result for every input.
During development the construction was also run on 10,000 random free-word
assignments, half with t = 0 and half with t = 2^31, using the reference
implementation, and all 10,000 pairs collided. That run is reported for context
only; no experiment manifest is declared, and none is needed because the
argument is exact.

## 9. Scope, limitations and novelty

- This is 1 of BLAKE3's 7 rounds. Nothing here bears on the full function. The
  construction does not extend unchanged to 2 rounds. There the complemented
  words of D0 and D2 enter the second column step together with uncomplemented
  words from the other two diagonal calls, and Lemma 1's condition would have
  to hold in the second round as well.
- The message domain used is 64-byte messages. The profile allows others; the
  algorithm needs none.
- No novelty is claimed. The underlying fact, that x + ~y = x - y - 1 lets a
  complement pass through a modular addition exactly when the other addend is 0
  or 2^31, is elementary. Complementation and rotational properties of ARX
  designs are well known. This package only checks that, at one round with the
  real IV, flags and digest, it gives a complete ordinary collision.
- `baseline_improved` names the organizer's nominal reference
  `blake3-r1-nominal-v2` (display value 128). The claimed bound 1.5 is below it
  and below the organizer's generic package (149). Whether that is an
  improvement for ranking is for review and Yukon's incumbent comparison.
- An AI review outcome is not a mathematical proof. The lemmas above are short
  enough to check by hand, and the certificates can be checked by machine.
