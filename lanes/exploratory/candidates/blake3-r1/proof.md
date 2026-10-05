# A deterministic closed-form collision for 1-round BLAKE3

## 0. Claim

Target: `blake3-r1-prefix-v1`, unkeyed BLAKE3-256 with only round 0 in every
compression, ordinary collision of complete messages. Lane: exploratory.

We give a deterministic algorithm that outputs two distinct 64-byte messages
M and M' with identical 256-bit blake3-r1 digests. It is a 174-instruction
program: a 134-instruction straight-line construction of M and M', followed by
a 40-instruction verification step. The verification recomputes both complete
hashes (two root compressions), checks that all 256 digest bits are equal,
checks that the two output messages are distinct, and halts with failure if
either check fails. Under `collision-frontier-v5`:

- success probability: exactly 1 (no random coins; Sections 3 to 5 prove it,
  so neither failure branch of the verification is ever taken);
- charged time (Section 7): 2 target compressions for the verification, plus
  381 charged primitive operations. Of these, 171 are executed 256-bit RAM
  instructions (134 construction, 37 verification), 36 are a notional charge
  for the 18-word constant table (no instruction is executed for it), and 174
  are a notional charge for placing the 174-instruction program in memory (one
  per instruction). That is T = 2 + 381/222 = 3.7162 target-compression units,
  log2(3.7162) = 1.8938, and we claim `time_log2 = 2.0` (rounded up to one
  decimal, with a margin of 63 primitive operations below 4 units);
- memory: at most 26,176 bytes including code, so `memory_log2_bytes = 15`;
- preprocessing: the 36-operation constant-table charge plus the 174-operation
  program placement, 210/222 < 1 unit, so `preprocessing_log2 = 0`; both are
  already included in the 381;
- nonuniform advice: none. The only literals are public specification
  constants and small fixed integers (Sections 7 and 9). No stored collision is
  used;
- collision checking (digest equality and message distinctness) and code
  placement are both charged, so the scalar does not depend on whether a
  closed-form construction must re-check its output or on whether program text
  costs time as well as memory. Section 7 tabulates the readings we
  considered; the largest is log2 = 1.982, so each of them is covered by the
  claimed 2.0. Section 7 also names two stricter combinations that we do not
  cover and explains why they conflict with the cost model's normalisation.

Provenance. The construction and its proofs are our own derivation. We know of
no published collision attack on 1-round BLAKE3 and do not claim one. Aumasson,
Guo, Knellwolf, Matusiewicz and Meier, "Differential and Invertibility Properties
of BLAKE", FSE 2010 (IACR ePrint 2010/043), studies how the BLAKE G function can
be inverted. We mention it only as background. The BLAKE3 specification
(O'Connor, Aumasson, Neves and Wilcox-O'Hearn, "BLAKE3: one function, fast
everywhere", 2020) tabulates differential-trail probabilities for reduced-round
variants, including one round, in its security analysis. That table shows that
one round has essentially no differential resistance, but the specification
gives no explicit ordinary-collision construction. No step below relies on
either source. Every statement needed is proved here. This package replaces
the organizer-accepted in-repo exploratory package for this track (a Wagner
four-sum search with `time_log2` 48 and success probability 0.9 under a
declared heuristic); none of its content is used here, and our verification
step checks the same two properties as its final verification (digest
equality and message distinctness).

No heuristic is used, so the heuristic list is empty. A witness pair produced by
the program is attached as a `hash-collision-witness-v2` certificate. It is a
mechanical check of the theorem's output. The time claim does not rest on it.

## 1. The exact function on 64-byte messages

All words are 32-bit. `+` and `-` are modulo 2^32. `^` is XOR and `~z = z ^ F`
with `F = 0xFFFFFFFF`. `ROTR_k` and `ROTL_k` rotate a 32-bit word right or left
by k bits.

A 64-byte message is one chunk with one block. Following the target profile and
`verifier/blake3.py`, its digest is one root compression. The inputs are
cv = IV, the sixteen little-endian message words w[0..15], counter 0,
block length 64, and flags CHUNK_START|CHUNK_END|ROOT = 1|2|8 = 11. There are no
parent nodes and no other compressions. The 16-word state is initialized as

    v[0..7]   = IV[0..7]
    v[8..11]  = IV[0..3]
    v[12..15] = (0, 0, 64, 11)       (counter low, counter high, block length, flags)

    IV = 6a09e667 bb67ae85 3c6ef372 a54ff53a 510e527f 9b05688c 1f83d9ab 5be0cd19

G(a,b,c,d; x,y) updates four state words as follows. The subscripts name
intermediate values.

    a1 = a + b + x;    d1 = ROTR16(d ^ a1);  c1 = c + d1;  b1 = ROTR12(b ^ c1)
    a2 = a1 + b1 + y;  d2 = ROTR8(d1 ^ a2);  c2 = c1 + d2; b2 = ROTR7(b1 ^ c2)
    output (a,b,c,d) <- (a2, b2, c2, d2)

Round 0 uses the message words unpermuted. It runs the column step and then the
diagonal step.

    column:   G0 on (0,4,8,12) with (w0,w1)     G1 on (1,5,9,13) with (w2,w3)
              G2 on (2,6,10,14) with (w4,w5)    G3 on (3,7,11,15) with (w6,w7)
    diagonal: G4 on (0,5,10,15) with (w8,w9)    G5 on (1,6,11,12) with (w10,w11)
              G6 on (2,7,8,13) with (w12,w13)   G7 on (3,4,9,14) with (w14,w15)

The four G calls within one step touch pairwise disjoint index sets, so their
order inside the step does not matter. With one round there is no message
permutation. The digest is the little-endian encoding of

    o[i] = v[i] ^ v[i+8],   i = 0..7,

the first 32 bytes of the root output. The words o[8..15] are not part of the
256-bit digest. This is exactly `verifier/blake3.py:blake3(m, 1)` for
len(m) = 64. That function calls `_chunk_output`, which returns
(IV, words, 0, 64, 3). The root call `_compress(IV, words, 0, 64, 3|8, 1)` then
builds the state above.

## 2. Two elementary facts

(F1) Rotation commutes with complement and with XOR:
ROTR_k(~z) = ~ROTR_k(z) and ROTR_k(u ^ z) = ROTR_k(u) ^ ROTR_k(z). Rotation only
permutes bit positions.

(F2) For 32-bit u and z: (~u) ^ (~z) = u ^ z. Also ~z = F - z = -z - 1.

## 3. Lemma 1 (choosing the c and d outputs of G)

Let a, b, c, d be any input words and let c*, d* be any target words. Define

    c1 = c* - d*
    d1 = c1 - c
    a1 = d ^ ROTL16(d1)
    x  = a1 - a - b
    b1 = ROTR12(b ^ c1)
    a2 = ROTL8(d*) ^ d1
    y  = a2 - a1 - b1

Then G(a,b,c,d; x,y) outputs (a2, ROTR7(b1 ^ c*), c*, d*).

Proof. Evaluate G forward with these x and y, one line at a time.

- a + b + x = a1, by the definition of x.
- ROTR16(d ^ a1) = ROTR16(ROTL16(d1)) = d1, because d ^ a1 = ROTL16(d1).
- c + d1 = c1, by the definition of d1.
- ROTR12(b ^ c1) = b1, by definition.
- a1 + b1 + y = a2, by the definition of y.
- ROTR8(d1 ^ a2) = ROTR8(ROTL8(d*)) = d*, because d1 ^ a2 = ROTL8(d*).
- c1 + d* = c*, by the definition of c1.
- The last output is ROTR7(b1 ^ c*).

All intermediate values coincide with those named in the lemma. QED.

Lemma 1 is an exact identity. It has no condition and no probability.

## 4. Lemma 2 (complement step)

Apply Lemma 1 with c = 0, d* = 0 and c* = g, for an arbitrary word g. Then
c1 = g, d1 = g, a2 = ROTL8(0) ^ g = g, and

    x(g) = (d ^ ROTL16(g)) - a - b
    y(g) = g - (d ^ ROTL16(g)) - ROTR12(b ^ g)
    G(a,b,0,d; x(g),y(g)) = (g, beta(g), g, 0),  beta(g) = ROTR7(ROTR12(b ^ g) ^ g).

Claim: beta(~g) = beta(g). Thus replacing g by ~g complements the a and c
outputs and leaves the b and d outputs unchanged.

Proof. By (F1), ROTR12(b ^ ~g) = ~ROTR12(b ^ g). By (F2),
(~ROTR12(b ^ g)) ^ (~g) = ROTR12(b ^ g) ^ g. Apply ROTR7. QED.

## 5. Theorem (collision family)

Fix any choice of the following free words:

- d-targets t0 and t2 for G0 and G2;
- (c,d)-targets (u1,t1) for G1 and (u3,t3) for G3;
- g4 and g6;
- w10, w11, w14, w15.

Build M as follows.

1. Column step. Apply Lemma 1 to G0 with target (0, t0), to G1 with (u1, t1), to
   G2 with (0, t2) and to G3 with (u3, t3). Each uses its actual column input
   words from Section 1. This gives w0..w7, and the post-column state has
   v[8] = v[10] = 0.
2. Diagonal step. Apply Lemma 2 to G4, with inputs (v0, v5, v10 = 0, v15) and
   g = g4, giving (w8, w9). Apply Lemma 2 to G6, with inputs (v2, v7, v8 = 0,
   v13) and g = g6, giving (w12, w13).

Build M' identically except that G4 uses ~g4 and G6 uses ~g6, giving
(w8', w9', w12', w13'). Then M != M' and blake3-r1(M) = blake3-r1(M').

Proof. Words 0..7 are equal in M and M'. The column inputs are the fixed
initial state, so the post-column states are identical. By Lemma 1 they have
v[8] = 0 (c-output of G0) and v[10] = 0 (c-output of G2). In the diagonal step,
G5 and G7 have identical inputs and identical message words in M and M', so
their outputs are identical. By Lemma 2 the outputs are:

- G4 on (v0, v5, v10, v15): (g4, beta4, g4, 0) for M and (~g4, beta4, ~g4, 0)
  for M';
- G6 on (v2, v7, v8, v13): (g6, beta6, g6, 0) for M and (~g6, beta6, ~g6, 0)
  for M'.

So the final states differ exactly in v0 and v10 (complemented by G4) and in v2
and v8 (complemented by G6). Check the digest words:

- o[0] = v0 ^ v8 is g4 ^ g6 for M and (~g4) ^ (~g6) = g4 ^ g6 for M', by (F2).
- o[2] = v2 ^ v10 is g6 ^ g4 for both messages, by the same argument.
- o[1], o[3], o[4], o[5], o[6], o[7] use v1, v9, v3, v11, v4, v12, v5, v13, v6,
  v14, v7, v15. None of these differs.

All 256 digest bits are therefore equal.

Distinctness: in fact w8 != w8'. By Lemma 2, w8 = x(g4) = z - a - b and
w8' = x(~g4) = z' - a - b, where a, b, d are the common inputs of G4,
z = d ^ ROTL16(g4) and z' = d ^ ROTL16(~g4). By (F1), ROTL16(~g4) =
~ROTL16(g4), so z' = ~z, which differs from z in all 32 bits. Subtracting the
same a + b modulo 2^32 is a bijection, so w8 != w8'. Hence M != M', and the
single word pair (w8, w8') already witnesses distinctness for every choice of
the free words; the verification of Section 7 tests exactly this pair. Both
messages are 64-byte strings in the profile's domain. QED.

The theorem holds for every value of every free word. No choice needs to be
searched for. The instance below fixes them to trivial values in advance.

Size of the family. There are 12 free 32-bit words, so 2^384 parameter choices.
Distinct choices give distinct messages M. Each free word is either a message
word of M (w10, w11, w14, w15) or an output of a G call evaluated on the words
of M (t0, u1, t1, t2, u3, t3 are c- or d-outputs of the column G calls, and g4,
g6 are the c-outputs of G4 and G6). So the free words can be read back from M,
and the map from free words to M is injective. The theorem is thus a uniform
construction of 2^384 ordered collision pairs (M, M'), not a single stored
pair. The parameter choices (g4, g6) and (~g4, ~g6), with the other ten free
words equal, give the same pair with M and M' exchanged, so there are 2^383
distinct unordered pairs.

## 6. The instance and closed forms

We choose t0 = t2 = 0; (u1,t1) = (IV1, 0); (u3,t3) = (IV3, 0); g4 = g6 = 0, so
the complemented values are F; and w10 = w11 = w14 = w15 = 0. The column inputs
are (IV_i, IV_{i+4}, IV_i, D_i) with D = (0, 0, 64, 11). Substituting into
Lemma 1 gives:

- G0 (c*, d* = 0, 0): c1 = 0, d1 = -IV0 =: n0, a1 = ROTL16(n0) =: A0, and the
  a-output is v0 = n0.
- G2: n2 := -IV2, a1 = 64 ^ ROTL16(n2) =: A2, and v2 = n2.
- G1 (c*, d* = IV1, 0): c1 = IV1, d1 = 0, a1 = 0, a2 = 0. The outputs are
  v5 = ROTR7(B1 ^ IV1) =: p5 and v13 = 0, where B1 = ROTR12(IV5 ^ IV1).
- G3 (c*, d* = IV3, 0): c1 = IV3, d1 = 0, a1 = 11, a2 = 0. The outputs are
  v7 = ROTR7(B3 ^ IV3) =: p7 and v15 = 0, where B3 = ROTR12(IV7 ^ IV3).

The resulting message words are:

    w0 = A0 - IV0 - IV4                w1 = n0 - A0 - ROTR12(IV4)
    w2 = 0 - (IV1 + IV5)               w3 = 0 - B1
    w4 = A2 - IV2 - IV6                w5 = n2 - A2 - ROTR12(IV6)
    w6 = 11 - IV3 - IV7                w7 = 0 - (11 + B3)

The diagonal inputs are G4 = (n0, p5, 0, 0) and G6 = (n2, p7, 0, 0), both with
d = 0. Lemma 2 gives the following, where s4 = n0 + p5, B4 = ROTR12(p5),
s6 = n2 + p7 and B6 = ROTR12(p7):

    g = 0 (M):    w8  = 0 - s4,  w9  = 0 - B4,  w12  = 0 - s6,  w13  = 0 - B6
    g = F (M'):   w8' = s4 ^ F,  w9' = B4 + 1,  w12' = s6 ^ F,  w13' = B6 + 1

For M', ROTL16(F) = F, so x(F) = F - s4 = s4 ^ F. Also
ROTR12(p5 ^ F) = ~B4 = F - B4, so y(F) = F - F - (F - B4) = B4 + 1 (mod 2^32).
G6 is the same. The other twelve words are shared.

Numerical values. These are not literals of the program; they are listed so a
reader can spot-check the arithmetic.

    n0=95f61999 A0=199995f6 ROTR12(IV4)=27f510e5 B1=6092062c p5=53b7eb51
    n2=c3910c8e A2=0c8ec3d1 ROTR12(IV6)=9ab1f83d B3=823feaf3 p7=924ee03f
    s4=e9ae04ea B4=b5153b7e s6=55dfeccd B6=03f924ee

    M  words: 5e815d10 546772be a992e8ef 9f6df9d4 b09bf6b4 1c505080 fecf3db8 7dc01502
              1651fb16 4aeac482 00000000 00000000 aa201333 fc06db12 00000000 00000000
    M' words: identical except w8'=1651fb15 w9'=b5153b7f w12'=aa201332 w13'=03f924ef

    digest (both): 00000000418bb1df00000000d5abb187084b5da6762a6afdf8479cd949f207dc

As predicted, o[0] = o[2] = g4 ^ g6 = 0. The message bytes are the
little-endian encodings of these words, and they are the certificate files.

## 7. Machine model and exact operation count

Model. This is the cost model's 256-bit word RAM, realised as a load/store
machine. It has 16 general registers and a data memory, and these instruction
kinds:

- LD r <- [addr] (a 256-bit load);
- ST [addr] <- r (a 256-bit store);
- a register-to-register ALU operation r <- s op t, with op in ADD, SUB
  (mod 2^256), AND, OR, XOR, SHL and SHR. The shift count is itself a register;
- BNZ r -> L and BZ r -> L, conditional branches to label L if r is nonzero,
  respectively zero (the cost model lists "conditional branch" as a primitive);
- HALT, which ends execution;
- COMP D <- X, one blake3-r1 target compression: the root compression of
  Section 1 (cv = IV, counter 0, block length 64, flags 11) applied to the
  block X[0..15], writing the digest words o[0..7] to D[0..7], one 32-bit word
  per RAM word. For a 64-byte message this is the complete hash.

Every executed COMP is charged one unit, as the cost model prescribes for a
selected-round target compression. Loading the IV, counter, block length and
flags into the compression state, and the compression's own reads of its block
and writes of its digest, are part of that compression's internals, which the
unit C = 222 prices; docs/RESCORING.md states that "a whole compression's
internals must not also be charged individually". Every other executed
instruction is one primitive operation and is charged 1/222 unit; we charge
HALT too, although it is not in the cost model's list of primitives. ALU
instructions take no immediate operands: every constant, including 0, 1, the
mask and each shift count, is read from an 18-word constant table by a charged
LD. The table is part of the program image, like the program text. It is
present in memory when execution starts and is counted under memory (576
bytes, Section 8).

Narrow arithmetic follows `scripts/reference_operation_costs.py` and the
verifier's own formulas:

- a 32-bit sum or difference is computed mod 2^256 and then ANDed with F;
- a 32-bit rotation by k is SHR by k, SHL by 32-k, OR and AND F, which is 4
  operations. ROTL16 uses SHR 16, SHL 16, OR, AND.

Because 2^32 divides 2^256, AND F after any chain of 256-bit additions and
subtractions yields the exact mod-2^32 value. Deferred masks: six rotation
results (A0 = ROTL16(n0), R2 = ROTL16(n2), and B0, B2, B4, B6, the ROTR12 of
IV4, IV6, p5, p7) are used only as operands of further ADD or SUB (and, for R2,
one XOR with the constant 64) whose result is ANDed with F before it is stored,
shifted or XORed into anything else. For these six we omit the rotation's own
final AND. The unreduced value is below 2^52 and congruent to the rotation
modulo 2^32; ADD and SUB preserve congruence modulo 2^32, and XOR with a
constant below 2^32 changes only the low 32 bits, so it does too. The later
AND F therefore yields the exact 32-bit result. These six rotations cost 3
operations each; every other rotation costs 4. Every value that is stored or
shifted is below 2^32. The construction (instructions 1-134) uses no native
narrow rotate, no compression, no comparison, no branch and no random word.
The verification (instructions 135-174) uses two compressions and two
conditional branches. No random word is used anywhere.

Constant table (18 words): IV0..IV7, 64, 11, F, 1, 0, 7, 12, 16, 20, 25.

Output. M is written to M[0..15] and M' to N[0..15], one 32-bit message word
per RAM word, in little-endian word order as in Section 1. Shared words are
stored twice from the same register. This is the layout in which the reference
compression, and so the unit C = 222, consumes a block: sixteen 32-bit words.
It is also the layout that the two COMP instructions of the verification read.
The organizer's normalisation excludes serialisation from C (docs/RESCORING.md,
"Prices": "Public loop/index arithmetic, Python overhead, memory traffic and
serialization are excluded from this reference normalization").

Robustness to packed output. Suppose a reviewer instead requires each message
as two 256-bit words holding the 64 bytes. In that reading COMP is the same
compression with a different input format: it takes the 64-byte block as two
256-bit words, with the byte order inside a word fixed by the machine's
load/store convention, so that convention needs no operation. Packing w0..w7
(shared by M and M') into one 256-bit word takes 7 SHL and 7 OR, which is 14
ALU operations. In the second word only w8, w9, w12 and w13 are nonzero (w10,
w11, w14, w15 are 0), so packing it takes 3 SHL and 3 OR per message, 12 in
total. The extra shift counts 32, 64, ..., 224 add 7 table words, so 7 LD and
14 table operations under the charge below. Stores fall from 32 to 4. The
construction then executes 25 LD + 4 ST + 110 ALU = 139 instructions, plus 50
table operations, 189 in all. The verification keeps its 40 instructions and
37 executed operations besides the two compressions; its distinctness test
loads the two second packed words, which contain w8 and w8', so it remains a
sufficient test that by Section 5 always passes. With placement of the
139 + 40 = 179 program instructions, the total is
2 + (189 + 37 + 179)/222 = 2 + 405/222 = 3.8243 units, log2 = 1.935, so
`time_log2 = 2.0` holds with packed output too. The remaining margin of
444 - 405 = 39 operations would also pay for up to 9 register spills (one ST
and one LD executed, and two instructions placed, each) if the extra live
values needed them.

Operation counts per G (ALU operations only):

| Part | Formula pieces (ALU ops) | ALU |
| --- | --- | ---: |
| G0 | n0 (2), A0 = ROTL16, mask deferred (3), w0 (3), ROTR12(IV4), mask deferred (3), w1 (3) | 14 |
| G1 | w2 (3), IV5^IV1 (1), B1 (4), w3 (2), B1^IV1 (1), p5 (4) | 15 |
| G2 | n2 (2), ROTL16, mask deferred (3), ^64 (1), w4 (3), ROTR12(IV6), mask deferred (3), w5 (3) | 15 |
| G3 | w6 (3), IV7^IV3 (1), B3 (4), w7 (3), B3^IV3 (1), p7 (4) | 16 |
| G4 (both messages) | s4 (2), w8 (2), w8' (1), B4, mask deferred (3), w9 (2), w9' (2) | 12 |
| G6 (both messages) | s6 (2), w12 (2), w12' (1), B6, mask deferred (3), w13 (2), w13' (2) | 12 |
| Total | | 84 |

The complete program is listed in the appendix. Its 134 construction
instructions (1-134) are:

| Kind | Count |
| --- | ---: |
| LD (each table word loaded exactly once) | 18 |
| ST (16 words of M, 16 words of M') | 32 |
| ADD | 6 |
| SUB | 19 |
| AND | 22 |
| OR | 10 |
| XOR | 7 |
| SHL | 10 |
| SHR | 10 |
| Total executed | 134 |

There are 6 + 19 + 22 + 10 + 7 + 10 + 10 = 84 ALU operations.

Verification (instructions 135-174). After M and M' are stored, the program
recomputes both complete hashes, compares them, and checks that the two output
messages are distinct:

| Kind | Instructions | Executed | Charge |
| --- | ---: | ---: | --- |
| COMP (digest of M to D, digest of M' to E) | 2 | 2 | 2 units |
| LD (D[0..7] and E[0..7]) | 16 | 16 | 16 ops |
| XOR (word-wise digest difference) | 8 | 8 | 8 ops |
| OR (accumulate the 8 differences) | 7 | 7 | 7 ops |
| BNZ (to FAIL if any digest bit differs) | 1 | 1 | 1 op |
| LD (M[8] and N[8], from the output memory) | 2 | 2 | 2 ops |
| XOR (M[8] ^ N[8]) | 1 | 1 | 1 op |
| BZ (to FAIL if M[8] = N[8]) | 1 | 1 | 1 op |
| HALT (success: output M, M') | 1 | 1 | 1 op |
| HALT at label FAIL (output failure) | 1 | 0 | none |
| Total | 40 | 39 | 2 units + 37 ops |

The accumulator is zero exactly when all eight digest words agree, that is,
when blake3-r1(M) = blake3-r1(M') on all 256 bits. The distinctness test
passes only if word 8 of the two stored messages differs, which implies
M != M'; it is a sufficient test, and Section 5 proves that w8 != w8' for every
choice of the free words, so it is also always passed. By the theorem of
Section 5 the digest accumulator is always zero and the word-8 difference is
always nonzero, so neither branch is taken and the algorithm always halts with
success. The FAIL instruction is part of the program text but is never
executed. A full 16-word distinctness comparison is unnecessary: one differing
word suffices to establish M != M'.

Register pressure is at most 15 simultaneously live values, counting the
destination of each instruction as live together with its sources, so 16
registers suffice and there are no spills (the verification needs at most 4
live values, and no construction value is live in it). The program has no loop
and no restart; its only branches are instructions 168 and 172, which are
never taken.

Constant table. The table is loaded with the program image, so writing it
costs no executed instruction. We nevertheless charge 2 primitive operations
per table word, as if each word were produced by one immediate move and written
by one ST, and book it as preprocessing: 2 * 18 = 36. This is twice the
one-operation-per-word placement charge we apply to program text below.

Program placement. We also charge one primitive operation per program
instruction for placing the program text in memory, 174 operations for the
174 instructions (including the never-executed FAIL instruction), and book it
as preprocessing. One instruction (an opcode from 13 kinds, at most three
4-bit register fields, and one table, data or label address of at most 16
bits) fits easily in one 256-bit word, so one ST per instruction suffices to
place it. The 4-word-per-instruction figure in Section 8 is only a generous
upper bound on memory. The cost model lists `code` under `memory_includes` and
has no instruction-fetch primitive, so this charge may not be required; we pay
it so that the claimed scalar does not depend on that reading.

Total charged time:

    target compressions:              2                    =  2 units
    construction (executed):        134 operations
    verification (executed):         37 operations
    constant table (notional):       36 operations
    program placement (notional):   174 operations
    primitive operations total:     381 operations         =  381/222 units

    T = 2 + 381/222 = 3.7162 target-compression units,
    log2(T) = 1.8938, claimed time_log2 = 2.0 (rounded up to one decimal).

The margin below 2^2.0 = 4 units is 4 * 222 - (2 * 222 + 381) = 63 primitive
operations. We claim the one-decimal value 2.0 rather than 1.9 as a robust
upper bound that also covers the stricter readings tabulated below.

The phase categories in the cost model are covered as follows:

- preprocessing: the 36 table operations and the 174 placement operations,
  210 in all, which is 210/222 < 1 unit, so `preprocessing_log2 = 0`;
- message and differential construction: the 84 ALU, 18 LD and 32 ST of
  instructions 1-134;
- randomness: none;
- all trials including failures: one trial, which always succeeds;
- sorting and lookup: none;
- collision checking: the 2 compressions and the 18 LD, 9 XOR, 7 OR, 1 BNZ
  and 1 BZ of instructions 135-172 (digest equality and message distinctness),
  and the final HALT;
- restart and success amplification: none.

Why the verification is part of the algorithm. The cost model counts
collision checking in total time and requires BLAKE3 to charge all
chunk/parent/root compressions an algorithm computes. A closed-form
construction whose output is a collision by theorem does not logically need
to re-check that output. The usual practice is nevertheless to verify every
returned pair by complete hash recomputations, charged as target
compressions, and to check that the two messages are distinct. We follow that
practice: verification is the last step of the algorithm's output procedure,
it is executed on every run, and it is charged in full. For 64-byte messages
one complete hash is exactly one root compression (Section 1), so the two
recomputations cost 2 units. The attached certificate is separate,
organizer-side evidence checked by the organizer's verifier; it is not part of
the charged algorithm.

Alternative readings. The following table gives the total under each
accounting convention we considered. The claimed row is the one above. The
last row adds charges that we consider unnecessary but that a stricter
reviewer might impose: memory traffic of each COMP (loading its 16 block
words and storing its 8 digest words, 24 operations per compression, 48 in
all; the reference normalisation C = 222 excludes memory traffic,
docs/RESCORING.md, "Prices", quoted above) and a separate comparison
instruction before each of the two conditional branches (one executed and one
placed instruction each, 4 operations in all).

| Reading | Units | log2 |
| --- | ---: | ---: |
| Construction and table only, no verification, no placement: 170/222 | 0.7658 | -0.385 |
| Plus placement of the 134 construction instructions: 304/222 | 1.3694 | 0.454 |
| Verification, no placement: 2 + 207/222 | 2.9324 | 1.552 |
| **Claimed**: verification and placement of all 174 instructions, 2 + 381/222 | **3.7162** | **1.894** |
| Claimed, with packed 256-bit output (above): 2 + 405/222 | 3.8243 | 1.935 |
| Claimed, plus COMP memory traffic and two separate comparisons: 2 + 433/222 | 3.9505 | 1.982 |

Each of these readings is at most 2^2.0 = 4 units, so the claimed
`time_log2 = 2.0` holds under each of them; the strictest leaves a margin of
11 operations. The first three rows are below the claim; we do not claim them
because they omit the verification or the placement.

Readings we do not cover. Two further combinations would exceed 2.0, and we
state them so that the coverage claim above is exact:

- adding to the last row the compression's own state initialisation (8 IV
  words, counter, block length and flags, 12 loads per COMP, 24 in all) gives
  2 + 457/222 = 4.0586 units, log2 = 2.021;
- combining the packed-output reading with a COMP that is charged for its own
  I/O, including unpacking each packed message into sixteen 32-bit words
  (about 15 shift and mask operations per packed word, 60 for the four packed
  words, before any placement or traffic charge), gives at least
  2 + 465/222 = 4.0946 units, log2 = 2.034.

Both charge parts of a compression's own computation (state set-up, block and
digest I/O, or deserialisation of its input) as attack-side operations, on top
of the unit that already prices the whole compression. docs/RESCORING.md
excludes memory traffic and serialisation from C = 222 and says that a whole
compression's internals must not also be charged individually. Under the cost
model as written, the claimed row is the applicable one, and the table's
strictest covered row charges only COMP's block and digest traffic in
addition.

## 8. Memory

| Item | Bytes |
| --- | ---: |
| 16 registers x 32 B | 512 |
| constant table, 18 words x 32 B | 576 |
| output, 32 words x 32 B | 1,024 |
| digests D[0..7] and E[0..7], 16 words x 32 B | 512 |
| compression working state (16 state, 16 block and 8 chaining words) x 32 B | 1,280 |
| program, 174 instructions x 4 words x 32 B (generous encoding; one word per instruction suffices) | 22,272 |
| Total | 26,176 < 2^15 |

So `memory_log2_bytes = 15`. There are no other tables and no stored messages
beyond the output.

## 9. Success probability, advice and precomputation

The algorithm has no coins. By the theorem of Section 5, which holds for every
value of the free words and so for the fixed instance, the pair it constructs
is always a pair of distinct 64-byte messages with equal blake3-r1 digests,
and its words 8 differ. So the verification always finds equal digests and a
nonzero word-8 difference, neither branch to FAIL (the only failure exit) is
ever taken, and the algorithm always halts with success and outputs that
pair. Hence `success_probability = 1`, which exceeds the required
0.39.

No precomputed collision or search result is embedded. The program's literals
are the eight IV words, the block length 64 and flags value 11 from the target
profile, and the small integers 0, 1, F and the shift counts 7, 12, 16, 20, 25.
Every message word and every intermediate value is computed at run time by the
charged instructions. The free parameters were fixed to trivial values (0, IV1,
IV3, F) because the theorem holds for all values. They were not selected by
trial, so there is no omitted search to charge. The theorem gives 2^384 ordered
(2^383 unordered) collision pairs, one ordered pair for each choice of the free
words (Section 5); the program computes one of them from public constants. The
derivation is the closed-form algebra of Lemmas 1 and 2.
`nonuniform_advice_log2_bytes = 0` records that no advice is used; the schema
cannot express log2(0).

## 10. Evidence and limitations

- The attached certificate contains exactly the program's output M and M'
  (the pair that passed the program's own verification). The
  organizer certificate checker hashes both with `verifier/hash_functions.digest`
  at 1 round and compares the result with the expected digest above.
- This is a full ordinary collision of the complete 1-round BLAKE3-256 hash with
  the standard IV, flags, counter, block length and root output. It is not
  free-start, not compression-only and not truncated.
- The construction uses only the structure of a single round: the c-input of
  each diagonal G is controllable, and the digest pairs the a-output of one
  diagonal G with the c-output of another. It says nothing about two or more
  rounds. The same pair does not collide at 2 or 7 rounds.
- The `baseline_improved` identifier `blake3-r1-nominal-v2` is the required
  nominal reference ID. The nominal value 128 is not an attack bound.
- `submission_state` is `draft`.

## Appendix: the complete charged program (174 instructions)

`N[i]` is the output word i of M'. A suffix `p` marks a word of M'
(m8p = w8'). Register names are SSA labels, and the allocation to 16 physical
registers follows from the live-range bound above. Instructions 1-134 are the
construction; instructions 135-174 are the verification, where `D[i]` and
`E[i]` receive digest word o[i] of M and of M', instructions 135-168 check
digest equality and instructions 169-172 check distinctness. FAIL labels
instruction 174. The registers A0, B0, R2, B2, B4 and B6 hold rotations whose
final mask is deferred (Section 7): they are below 2^52 and congruent modulo
2^32 to the values of Section 6, and every value stored or shifted is below
2^32.

```
  1 LD  zero <- [ZERO]
  2 LD  iv0 <- [IV0]
  3 SUB t1 <- zero, iv0
  4 LD  mask <- [MASK]
  5 AND n0 <- t1, mask
  6 LD  s16 <- [S16]
  7 SHR t2 <- n0, s16
  8 SHL t3 <- n0, s16
  9 OR  A0 <- t2, t3
 10 SUB t5 <- A0, iv0
 11 LD  iv4 <- [IV4]
 12 SUB t6 <- t5, iv4
 13 AND m0 <- t6, mask
 14 LD  s12 <- [S12]
 15 SHR t7 <- iv4, s12
 16 LD  s20 <- [S20]
 17 SHL t8 <- iv4, s20
 18 OR  B0 <- t7, t8
 19 SUB t10 <- n0, A0
 20 SUB t11 <- t10, B0
 21 AND m1 <- t11, mask
 22 ST  M[0] <- m0
 23 ST  N[0] <- m0
 24 ST  M[1] <- m1
 25 ST  N[1] <- m1
 26 LD  iv1 <- [IV1]
 27 LD  iv5 <- [IV5]
 28 ADD t12 <- iv1, iv5
 29 SUB t13 <- zero, t12
 30 AND m2 <- t13, mask
 31 XOR W1 <- iv5, iv1
 32 SHR t14 <- W1, s12
 33 SHL t15 <- W1, s20
 34 OR  t16 <- t14, t15
 35 AND B1 <- t16, mask
 36 SUB t17 <- zero, B1
 37 AND m3 <- t17, mask
 38 XOR U1 <- B1, iv1
 39 LD  s7 <- [S7]
 40 SHR t18 <- U1, s7
 41 LD  s25 <- [S25]
 42 SHL t19 <- U1, s25
 43 OR  t20 <- t18, t19
 44 AND p5 <- t20, mask
 45 ST  M[2] <- m2
 46 ST  N[2] <- m2
 47 ST  M[3] <- m3
 48 ST  N[3] <- m3
 49 LD  iv2 <- [IV2]
 50 SUB t21 <- zero, iv2
 51 AND n2 <- t21, mask
 52 SHR t22 <- n2, s16
 53 SHL t23 <- n2, s16
 54 OR  R2 <- t22, t23
 55 LD  c64 <- [C64]
 56 XOR A2 <- R2, c64
 57 SUB t25 <- A2, iv2
 58 LD  iv6 <- [IV6]
 59 SUB t26 <- t25, iv6
 60 AND m4 <- t26, mask
 61 SHR t27 <- iv6, s12
 62 SHL t28 <- iv6, s20
 63 OR  B2 <- t27, t28
 64 SUB t30 <- n2, A2
 65 SUB t31 <- t30, B2
 66 AND m5 <- t31, mask
 67 ST  M[4] <- m4
 68 ST  N[4] <- m4
 69 ST  M[5] <- m5
 70 ST  N[5] <- m5
 71 LD  c11 <- [C11]
 72 LD  iv3 <- [IV3]
 73 SUB t32 <- c11, iv3
 74 LD  iv7 <- [IV7]
 75 SUB t33 <- t32, iv7
 76 AND m6 <- t33, mask
 77 XOR W3 <- iv7, iv3
 78 SHR t34 <- W3, s12
 79 SHL t35 <- W3, s20
 80 OR  t36 <- t34, t35
 81 AND B3 <- t36, mask
 82 ADD t37 <- c11, B3
 83 SUB t38 <- zero, t37
 84 AND m7 <- t38, mask
 85 XOR U3 <- B3, iv3
 86 SHR t39 <- U3, s7
 87 SHL t40 <- U3, s25
 88 OR  t41 <- t39, t40
 89 AND p7 <- t41, mask
 90 ST  M[6] <- m6
 91 ST  N[6] <- m6
 92 ST  M[7] <- m7
 93 ST  N[7] <- m7
 94 ADD t42 <- n0, p5
 95 AND s4 <- t42, mask
 96 SUB t43 <- zero, s4
 97 AND m8 <- t43, mask
 98 XOR m8p <- s4, mask
 99 SHR t44 <- p5, s12
100 SHL t45 <- p5, s20
101 OR  B4 <- t44, t45
102 SUB t47 <- zero, B4
103 AND m9 <- t47, mask
104 LD  one <- [ONE]
105 ADD t48 <- B4, one
106 AND m9p <- t48, mask
107 ST  M[8] <- m8
108 ST  N[8] <- m8p
109 ST  M[9] <- m9
110 ST  N[9] <- m9p
111 ADD t49 <- n2, p7
112 AND s6 <- t49, mask
113 SUB t50 <- zero, s6
114 AND m12 <- t50, mask
115 XOR m12p <- s6, mask
116 SHR t51 <- p7, s12
117 SHL t52 <- p7, s20
118 OR  B6 <- t51, t52
119 SUB t54 <- zero, B6
120 AND m13 <- t54, mask
121 ADD t55 <- B6, one
122 AND m13p <- t55, mask
123 ST  M[12] <- m12
124 ST  N[12] <- m12p
125 ST  M[13] <- m13
126 ST  N[13] <- m13p
127 ST  M[10] <- zero
128 ST  N[10] <- zero
129 ST  M[11] <- zero
130 ST  N[11] <- zero
131 ST  M[14] <- zero
132 ST  N[14] <- zero
133 ST  M[15] <- zero
134 ST  N[15] <- zero
135 COMP D <- M
136 COMP E <- N
137 LD  d0 <- D[0]
138 LD  e0 <- E[0]
139 XOR x0 <- d0, e0
140 LD  d1 <- D[1]
141 LD  e1 <- E[1]
142 XOR x1 <- d1, e1
143 OR  q1 <- x0, x1
144 LD  d2 <- D[2]
145 LD  e2 <- E[2]
146 XOR x2 <- d2, e2
147 OR  q2 <- q1, x2
148 LD  d3 <- D[3]
149 LD  e3 <- E[3]
150 XOR x3 <- d3, e3
151 OR  q3 <- q2, x3
152 LD  d4 <- D[4]
153 LD  e4 <- E[4]
154 XOR x4 <- d4, e4
155 OR  q4 <- q3, x4
156 LD  d5 <- D[5]
157 LD  e5 <- E[5]
158 XOR x5 <- d5, e5
159 OR  q5 <- q4, x5
160 LD  d6 <- D[6]
161 LD  e6 <- E[6]
162 XOR x6 <- d6, e6
163 OR  q6 <- q5, x6
164 LD  d7 <- D[7]
165 LD  e7 <- E[7]
166 XOR x7 <- d7, e7
167 OR  q7 <- q6, x7
168 BNZ q7 -> FAIL
169 LD  y8 <- M[8]
170 LD  y8p <- N[8]
171 XOR z8 <- y8, y8p
172 BZ  z8 -> FAIL
173 HALT success (output M, N)
174 FAIL: HALT failure (unreachable)
```
