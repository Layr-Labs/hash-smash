# A deterministic closed-form collision for 1-round BLAKE3

## 0. Claim

Target: `blake3-r1-prefix-v1`, unkeyed BLAKE3-256 with only round 0 in every
compression, ordinary collision of complete messages. Lane: exploratory.

We give a deterministic algorithm that outputs two distinct 64-byte messages
M and M' with identical 256-bit blake3-r1 digests. Under `collision-frontier-v5`:

- success probability: exactly 1 (no random coins; Sections 3 to 5 prove it);
- charged time: 176 primitive 256-bit RAM operations (Section 7), that is
  176/222 = 0.793 target-compression units. log2(0.793) = -0.335. We claim
  `time_log2 = 0`, the schema minimum, which bounds total time by 1 unit;
- memory: at most 2,752 bytes in total, counting the encoded program text,
  the constant table, both output messages, the registers, the program
  counter and the instruction register (Section 8). 2,752 < 2^12, so
  `memory_log2_bytes = 12`;
- preprocessing: the 36-operation constant-table charge, 36/222 < 1 unit,
  so `preprocessing_log2 = 0`; it is already included in the 176;
- nonuniform advice: none. The only literals are public specification
  constants and small fixed integers (Sections 7 and 9). No stored collision is
  used;
- collision checking and code placement: not charged, because the algorithm
  performs neither. Section 7 gives the argument. It also gives the values a
  reviewer would get by charging them anyway, which are outside the cost model:
  code placement charged per image word still gives 212/222 < 1, so 0; a
  self-check gives at most 1.6, and both together at most 1.7.

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
either source. Every statement needed is proved here.

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

Distinctness: G with fixed inputs is a function of (x, y). If
(w8, w9) = (w8', w9'), G4 would produce the same c-output for M and M'. But
those c-outputs are g4 and ~g4, which differ in all 32 bits. So M != M'. Both
messages are 64-byte strings in the profile's domain. QED.

The theorem holds for every value of every free word. No choice needs to be
searched for. The instance below fixes them to trivial values in advance.

Size of the family. There are 12 free 32-bit words, so 2^384 parameter choices.
Distinct choices give distinct messages M. Each free word is either a message
word of M (w10, w11, w14, w15) or an output of a G call evaluated on the words
of M (t0, u1, t1, t2, u3, t3 are c- or d-outputs of the column G calls, and g4,
g6 are the c-outputs of G4 and G6). So the free words can be read back from M,
and the map from free words to M is injective. The theorem is thus a uniform
construction of 2^384 distinct collision pairs, not a single stored pair.

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
machine. It has 16 general registers and a data memory, and three instruction
kinds:

- LD r <- [addr] (a 256-bit load);
- ST [addr] <- r (a 256-bit store);
- a register-to-register ALU operation r <- s op t, with op in ADD, SUB
  (mod 2^256), AND, OR, XOR, SHL and SHR. The shift count is itself a register.

Every executed instruction is one primitive operation and is charged 1/222
unit. ALU instructions take no immediate operands: every constant, including 0,
1, the mask and each shift count, is read from an 18-word constant table by a
charged LD. The table is static data loaded together with the program text
(RAM words 0..17, Section 8). It is present in memory when execution starts and is counted under memory
(576 bytes, Section 8).

Narrow arithmetic follows `scripts/reference_operation_costs.py` and the
verifier's own formulas:

- a 32-bit sum or difference is computed mod 2^256 and then ANDed with F;
- a 32-bit rotation by k is SHR by k, SHL by 32-k, OR and AND F, which is 4
  operations. ROTL16 uses SHR 16, SHL 16, OR, AND.

Because 2^32 divides 2^256, AND F after any chain of 256-bit additions and
subtractions yields the exact mod-2^32 value. Every value stored or rotated is
below 2^32. No native narrow rotate, no compression call, no comparison, no
branch and no random word is used.

Constant table (18 words): IV0..IV7, 64, 11, F, 1, 0, 7, 12, 16, 20, 25.

Output. M is written to M[0..15] and M' to N[0..15], one 32-bit message word
per RAM word, in little-endian word order as in Section 1. Shared words are
stored twice from the same register. This is the layout in which the reference
compression, and so the unit C = 222, consumes a block: sixteen 32-bit words.
The organizer's normalisation excludes serialisation from C (docs/RESCORING.md,
"Prices": "Public loop/index arithmetic, Python overhead, memory traffic and
serialization are excluded from this reference normalization").

Robustness to packed output. Suppose a reviewer instead requires each message
as two 256-bit words holding the 64 bytes. Packing w0..w7 (shared by M and M')
into one 256-bit word takes 7 SHL and 7 OR, which is 14 ALU operations. In the
second word only w8, w9, w12 and w13 are nonzero (w10, w11, w14, w15 are 0), so
packing it takes 3 SHL and 3 OR per message, 12 in total. The extra shift
counts 32, 64, ..., 224 add 7 table words, so 7 LD and 14 table operations
under the charge below. Stores fall from 32 to 4. The total becomes
25 LD + 4 ST + 116 ALU + 50 table = 195 operations, which is still below 222.
The remaining margin of 27 operations would also pay for up to 13 register
spills (one ST and one LD each) if the extra live values needed them. So
`time_log2 = 0` holds with packed output too. The byte order inside a 256-bit
word is fixed by the machine's load/store convention and needs no operation.

Operation counts per G (ALU operations only):

| Part | Formula pieces (ALU ops) | ALU |
| --- | --- | ---: |
| G0 | n0 (2), A0 = ROTL16 (4), w0 (3), ROTR12(IV4) (4), w1 (3) | 16 |
| G1 | w2 (3), IV5^IV1 (1), B1 (4), w3 (2), B1^IV1 (1), p5 (4) | 15 |
| G2 | n2 (2), ROTL16 (4), ^64 (1), w4 (3), ROTR12(IV6) (4), w5 (3) | 17 |
| G3 | w6 (3), IV7^IV3 (1), B3 (4), w7 (3), B3^IV3 (1), p7 (4) | 16 |
| G4 (both messages) | s4 (2), w8 (2), w8' (1), B4 (4), w9 (2), w9' (2) | 13 |
| G6 (both messages) | s6 (2), w12 (2), w12' (1), B6 (4), w13 (2), w13' (2) | 13 |
| Total | | 90 |

The complete program is listed in the appendix. Its 140 instructions are:

| Kind | Count |
| --- | ---: |
| LD (each table word loaded exactly once) | 18 |
| ST (16 words of M, 16 words of M') | 32 |
| ADD | 6 |
| SUB | 19 |
| AND | 28 |
| OR | 10 |
| XOR | 7 |
| SHL | 10 |
| SHR | 10 |
| Total executed | 140 |

There are 6 + 19 + 28 + 10 + 7 + 10 + 10 = 90 ALU operations. Register pressure
is at most 15 simultaneously live values, counting the destination of each
instruction as live together with its sources, so 16 registers suffice and
there are no spills. The program is straight-line: no loop, no branch, no
restart. It ends at a HALT sentinel word that follows the last instruction
(Section 8). HALT performs none of the primitive operations listed in the cost
model, so it is not counted among the 140 executed instructions; charging it
as one more operation would give 177 < 222 and change nothing below.

Constant table. The table is loaded together with the program text, so writing it
costs no executed instruction. We nevertheless add a voluntary over-charge of 2
primitive operations per table word, as if each word were produced by one
immediate move and written by one ST, and book it as preprocessing:
2 * 18 = 36. This charge is not a required step of the algorithm; it only
widens the safety margin. Without it the total would be 140 operations.

Total charged time:

    T = 140 + 36 = 176 primitive operations
      = 176 / 222 target compressions = 0.7928 units < 1 = 2^0.

The phase categories in the cost model are covered as follows:

- preprocessing: the 36 table operations;
- message and differential construction: the 90 ALU, 18 LD and 32 ST;
- randomness: none;
- failed trials: none, since success is certain;
- sorting and lookup: none;
- collision checking: none performed (see below);
- restarts: none.

Why nothing is charged for collision checking or verification. The cost model
lists the categories of work that total time includes: preprocessing, message
and differential construction, randomness, all trials including failures,
sorting and lookup, collision checking, and restart and success amplification
(`collision-frontier-v5`, `total_time_includes`). Each category charges work
that the algorithm actually performs. This algorithm has no search step, no
candidate to test, and no decision that depends on a hash value. It never
evaluates a compression and never compares digests. By the theorem of Section 5
its output is a collision on every execution, so a check could not change the
output or the success probability, and there is nothing to restart. A
closed-form construction is not charged for re-checking its own output. We read
the "verification" item in docs/CANDIDATE_QUALIFICATION.md (item 2) the same
way: it charges verification work that an algorithm performs, such as testing
candidates during a search. The cost-model sentence "BLAKE3 must charge all chunk/parent/root
compressions" concerns compressions an algorithm computes: it rules out
charging only the root compression of a multi-chunk evaluation. It does not
require an algorithm to hash anything it does not hash. The attached
certificate is organizer-side evidence, checked by the organizer's verifier.
It is not part of the charged algorithm.

Fallback if a reviewer charges a self-check anyway. Adding an in-program check
costs 2 compressions (one root compression for each message, 2 units) plus at
most 48 primitive operations to load, XOR, OR-reduce and branch on the eight
digest-word pairs. That gives at most 2 + (176 + 48)/222 = 3.009 units, and
log2(3.009) = 1.589, so `time_log2 <= 1.6`.

Margin: 222 - 176 = 46 operations below one unit. So `time_log2 = 0` holds with
room for more conservative bookkeeping of the listed kinds. The claimed scalar
is the schema minimum. Under these rules, the true value log2(0.7928) = -0.335
cannot be reported below 0.

Code. We charge every executed instruction and count the program text in
memory (Section 8). We do not charge time for placing the program in memory,
for these reasons.

1. The cost model lists `code` under `memory_includes`. None of the seven
   `total_time_includes` categories is code loading, and the list of primitive
   operations has no instruction-fetch primitive.
2. In a RAM the program is fixed control. It is not data written by executed
   instructions, and loading it is not a step of the algorithm.
3. The unit itself does not pay this cost. The reference cost C = 222 counts
   only the data-path operations of one compression. Program text, loop and
   index arithmetic and memory traffic are excluded from it (docs/RESCORING.md,
   "Prices", quoted above). Charging code placement to the attack but not to
   the unit it is measured in would be inconsistent.
4. The attack already pays more than the unit does: all 18 loads and 32 stores
   are charged, although the reference normalisation excludes memory traffic.

Outside the cost model, for disclosure only. The program image occupies 18
RAM words (Section 8). If a reviewer nevertheless charged placing it, at the
same 2 operations per word as the table over-charge, that adds 36: the total is
176 + 36 = 212 operations, 212/222 < 1 (213/222 < 1 if the HALT sentinel is
also charged as an operation), so `time_log2 = 0` holds even under that
charge. If code placement and a self-check were both charged, the self-check's
48 extra instructions need 6 more image words (12 more placement operations),
and the total is at most 2 + (213 + 48 + 12)/222 = 3.230 units, log2 = 1.692,
so `time_log2 <= 1.7`. These are not charges under `collision-frontier-v5`; we
list them so a reviewer can see that every reading gives a constant far below
the nominal 128. The submitted scalar is 0.

## 8. Memory

The cost model counts code, nonuniform advice, precomputed data, messages,
working state, tables and retained randomness under memory. This program
allocates nothing at run time and frees nothing, so its peak memory is simply
everything that is resident from start to halt. We list every byte.

Layout. The machine of Section 7 has one RAM of 256-bit (32-byte) words, 16
registers of 256 bits, a program counter and an instruction register. The RAM
holds:

- data words 0..17: the constant table, in the order IV0..IV7, 64, 11, F, 1, 0,
  7, 12, 16, 20, 25;
- data words 18..33: M[0..15], and data words 34..49: N[0..15], one 32-bit
  message word per RAM word (Section 7, "Output");
- code words 50..67: the program image of Appendix B, in 18 RAM words,
  disjoint from the data words 0..49. No ST targets an address of 50 or more
  (every ST address is in 18..49), so the program cannot modify itself.

Instruction encoding. Every instruction is one fixed 32-bit word:

| Bits | Field |
| --- | --- |
| 31..28 | opcode: LD 0, ST 1, ADD 2, SUB 3, AND 4, OR 5, XOR 6, SHL 7, SHR 8, HALT 15 |
| 27..24 | destination register (LD and ALU), or source register (ST) |
| 23..20 | first source register (ALU only; 0 otherwise) |
| 19..16 | second source register (ALU only; 0 otherwise) |
| 15..0 | data word address (LD and ST only; 0 otherwise) |

Every field fits: there are ten opcodes, 16 registers, and every data address
is below 50. The image has 141 words: the 140 instructions of Appendix A in
order, with the SSA labels mapped to physical registers r0..r15, followed by
the HALT sentinel (opcode 15, all other fields 0). That is 141 x 4 = 564 bytes.
Instruction i (from 0) is the little-endian 32-bit field at byte offset
4(i mod 8) of code word floor(i/8) (RAM word 50 + floor(i/8)), so the image fills 18 RAM words; the unused
12 bytes of the last word, which holds 4 instructions and the sentinel, are
counted anyway. The program counter is an instruction index from 0 to 140.
The instruction register holds the 256-bit code word containing the current
instruction, from which the 32-bit field at offset 4(i mod 8) is decoded; it
is machine state and is charged as one full word. As
in Section 7, there is no instruction-fetch primitive: the program counter
selecting the next field is the machine's fixed control. The image text is not
a primitive operation and is not charged as time (Section 7, "Code"); its bytes
are charged here.

Byte ledger (peak = total):

| Item | RAM words | Bytes |
| --- | ---: | ---: |
| program image, 141 x 4 B = 564 B, held in whole RAM words | 18 | 576 |
| constant table, 18 words x 32 B | 18 | 576 |
| output M and M', 32 words x 32 B | 32 | 1,024 |
| registers, 16 x 32 B | 16 | 512 |
| program counter, charged as one full 32 B word | 1 | 32 |
| instruction register (fetched code word), 1 x 32 B | 1 | 32 |
| Total | 86 | 2,752 |

2,752 bytes = 2^11.43 < 2^12 = 4,096, so `memory_log2_bytes = 12`.

Nothing else is resident. The algorithm has no input: the IV, 64 and 11 are in
the table. There is no stack, no heap, no spill area (at most 15 values are
live, Section 7), no random word, no stored message other than the output, no
stored digest and no stored collision. Each output message word occupies a
whole 32-byte RAM word although only 4 of its bytes are nonzero, and all 32
bytes are counted. The table words, which are all below 2^32, are also counted
at 32 bytes each.

Relation to the earlier version. An earlier version of this package
(submission 754f0f26) claimed `memory_log2_bytes = 15`. Its ledger counted 4 RAM
words (128 bytes) per instruction, a placeholder that made the program text
17,920 of its 20,032 bytes. That figure was an over-count, not a property of
the program. The program, the table, the outputs and the register file are
unchanged here. Only the program text is now counted at its actual encoded
size.

Robustness. The bound does not depend on the 4-byte encoding being tight:

- With one full 256-bit RAM word per instruction, the image is 141 x 32 =
  4,512 bytes. The total is then 6,688 bytes < 2^13, so even charging every
  instruction a whole RAM word keeps the program below 2^13 bytes.
- Under the packed-output reading of Section 7, the output shrinks to 4 RAM
  words (128 bytes) and the table grows to 25 words (800 bytes). The program
  grows to 145 executed instructions (25 LD, 4 ST, 116 ALU; the other 50 of
  the 195 operations there are the notional table charge, not instructions),
  plus at most 26 spill instructions and the sentinel: 172 x 4 = 688 bytes, or
  22 RAM words = 704 bytes. With 13 spill words (416 bytes), 512 bytes of
  registers, 32 for the program counter and 32 for the instruction register,
  the total is at most 2,624 bytes < 2^12.

Mechanical check of the image. Appendix B gives all 141 words in hexadecimal,
with their SHA-256. Each word decodes by hand with the table above. For
example, the first four words, 0000000c 01000000 32010000 0300000a, are
LD r0 <- [12] (ZERO), LD r1 <- [0] (IV0), SUB r2 <- r0, r1 and
LD r3 <- [10] (MASK), which are lines 1 to 4 of Appendix A. We also decoded
the image and executed it on a 256-bit word-RAM interpreter. It executed 140
instructions with exactly the counts of Section 7 (18 LD, 32 ST, 6 ADD, 19 SUB,
28 AND, 10 OR, 7 XOR, 10 SHL, 10 SHR) and then reached HALT. The 32 output
words, read as little-endian 32-bit words, are byte for byte the two
certificate files. This check is evidence that the encoding is consistent. The
collision itself rests on the theorem of Section 5, and the organizer
certificate check confirms it independently.

## 9. Success probability, advice and precomputation

The algorithm has no coins and no failure branch. By the theorem of Section 5,
which holds for every value of the free words and so for the fixed instance,
its output is always a pair of distinct 64-byte messages with equal blake3-r1
digests. Hence `success_probability = 1`, which exceeds the required 0.39.

No precomputed collision or search result is embedded. The program's literals
are the eight IV words, the block length 64 and flags value 11 from the target
profile, and the small integers 0, 1, F and the shift counts 7, 12, 16, 20, 25.
Every message word and every intermediate value is computed at run time by the
charged instructions. The free parameters were fixed to trivial values (0, IV1,
IV3, F) because the theorem holds for all values. They were not selected by
trial, so there is no omitted search to charge. The theorem gives 2^384 distinct
collision pairs, one for each choice of the free words (Section 5); the program
computes one of them from public constants. The derivation is the closed-form algebra of Lemmas 1 and 2. `nonuniform_advice_log2_bytes = 0` records that no
advice is used; the schema cannot express log2(0).

## 10. Evidence and limitations

- The attached certificate contains exactly the program's output M and M'. The
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
- `submission_state` is `ready`.

## Appendix: the complete charged program (140 instructions)

`N[i]` is the output word i of M'. A suffix `p` marks a word of M'
(m8p = w8'). Register names are SSA labels. Appendix B fixes a concrete
allocation to the 16 physical registers r0..r15 and gives the encoded image.

```
  1 LD  zero <- [ZERO]
  2 LD  iv0 <- [IV0]
  3 SUB t1 <- zero, iv0
  4 LD  mask <- [MASK]
  5 AND n0 <- t1, mask
  6 LD  s16 <- [S16]
  7 SHR t2 <- n0, s16
  8 SHL t3 <- n0, s16
  9 OR  t4 <- t2, t3
 10 AND A0 <- t4, mask
 11 SUB t5 <- A0, iv0
 12 LD  iv4 <- [IV4]
 13 SUB t6 <- t5, iv4
 14 AND m0 <- t6, mask
 15 LD  s12 <- [S12]
 16 SHR t7 <- iv4, s12
 17 LD  s20 <- [S20]
 18 SHL t8 <- iv4, s20
 19 OR  t9 <- t7, t8
 20 AND B0 <- t9, mask
 21 SUB t10 <- n0, A0
 22 SUB t11 <- t10, B0
 23 AND m1 <- t11, mask
 24 ST  M[0] <- m0
 25 ST  N[0] <- m0
 26 ST  M[1] <- m1
 27 ST  N[1] <- m1
 28 LD  iv1 <- [IV1]
 29 LD  iv5 <- [IV5]
 30 ADD t12 <- iv1, iv5
 31 SUB t13 <- zero, t12
 32 AND m2 <- t13, mask
 33 XOR W1 <- iv5, iv1
 34 SHR t14 <- W1, s12
 35 SHL t15 <- W1, s20
 36 OR  t16 <- t14, t15
 37 AND B1 <- t16, mask
 38 SUB t17 <- zero, B1
 39 AND m3 <- t17, mask
 40 XOR U1 <- B1, iv1
 41 LD  s7 <- [S7]
 42 SHR t18 <- U1, s7
 43 LD  s25 <- [S25]
 44 SHL t19 <- U1, s25
 45 OR  t20 <- t18, t19
 46 AND p5 <- t20, mask
 47 ST  M[2] <- m2
 48 ST  N[2] <- m2
 49 ST  M[3] <- m3
 50 ST  N[3] <- m3
 51 LD  iv2 <- [IV2]
 52 SUB t21 <- zero, iv2
 53 AND n2 <- t21, mask
 54 SHR t22 <- n2, s16
 55 SHL t23 <- n2, s16
 56 OR  t24 <- t22, t23
 57 AND R2 <- t24, mask
 58 LD  c64 <- [C64]
 59 XOR A2 <- R2, c64
 60 SUB t25 <- A2, iv2
 61 LD  iv6 <- [IV6]
 62 SUB t26 <- t25, iv6
 63 AND m4 <- t26, mask
 64 SHR t27 <- iv6, s12
 65 SHL t28 <- iv6, s20
 66 OR  t29 <- t27, t28
 67 AND B2 <- t29, mask
 68 SUB t30 <- n2, A2
 69 SUB t31 <- t30, B2
 70 AND m5 <- t31, mask
 71 ST  M[4] <- m4
 72 ST  N[4] <- m4
 73 ST  M[5] <- m5
 74 ST  N[5] <- m5
 75 LD  c11 <- [C11]
 76 LD  iv3 <- [IV3]
 77 SUB t32 <- c11, iv3
 78 LD  iv7 <- [IV7]
 79 SUB t33 <- t32, iv7
 80 AND m6 <- t33, mask
 81 XOR W3 <- iv7, iv3
 82 SHR t34 <- W3, s12
 83 SHL t35 <- W3, s20
 84 OR  t36 <- t34, t35
 85 AND B3 <- t36, mask
 86 ADD t37 <- c11, B3
 87 SUB t38 <- zero, t37
 88 AND m7 <- t38, mask
 89 XOR U3 <- B3, iv3
 90 SHR t39 <- U3, s7
 91 SHL t40 <- U3, s25
 92 OR  t41 <- t39, t40
 93 AND p7 <- t41, mask
 94 ST  M[6] <- m6
 95 ST  N[6] <- m6
 96 ST  M[7] <- m7
 97 ST  N[7] <- m7
 98 ADD t42 <- n0, p5
 99 AND s4 <- t42, mask
100 SUB t43 <- zero, s4
101 AND m8 <- t43, mask
102 XOR m8p <- s4, mask
103 SHR t44 <- p5, s12
104 SHL t45 <- p5, s20
105 OR  t46 <- t44, t45
106 AND B4 <- t46, mask
107 SUB t47 <- zero, B4
108 AND m9 <- t47, mask
109 LD  one <- [ONE]
110 ADD t48 <- B4, one
111 AND m9p <- t48, mask
112 ST  M[8] <- m8
113 ST  N[8] <- m8p
114 ST  M[9] <- m9
115 ST  N[9] <- m9p
116 ADD t49 <- n2, p7
117 AND s6 <- t49, mask
118 SUB t50 <- zero, s6
119 AND m12 <- t50, mask
120 XOR m12p <- s6, mask
121 SHR t51 <- p7, s12
122 SHL t52 <- p7, s20
123 OR  t53 <- t51, t52
124 AND B6 <- t53, mask
125 SUB t54 <- zero, B6
126 AND m13 <- t54, mask
127 ADD t55 <- B6, one
128 AND m13p <- t55, mask
129 ST  M[12] <- m12
130 ST  N[12] <- m12p
131 ST  M[13] <- m13
132 ST  N[13] <- m13p
133 ST  M[10] <- zero
134 ST  N[10] <- zero
135 ST  M[11] <- zero
136 ST  N[11] <- zero
137 ST  M[14] <- zero
138 ST  N[14] <- zero
139 ST  M[15] <- zero
140 ST  N[15] <- zero
```

## Appendix B: the encoded program image (141 words, 564 bytes)

The 32-bit words are in execution order, eight per line. The number before each
line is the Appendix A line number of its first word. Word 141 is the HALT
sentinel. Stored little-endian, the 564-byte image has SHA-256
7545b1944505329e3ff610b5502c81a182c9b415356bc1abe6d962afc112ae0f.

```
  1: 0000000c 01000000 32010000 0300000a 44230000 0200000f 85420000 76420000
  9: 57560000 45730000 36510000 01000004 37610000 46730000 0700000e 88170000
 17: 09000010 7a190000 518a0000 48130000 31450000 35180000 41530000 16000012
 25: 16000022 11000013 11000023 01000001 05000005 26150000 38060000 46830000
 33: 68510000 85870000 7a890000 585a0000 45830000 38050000 4a830000 68510000
 41: 0100000d 85810000 0b000011 7c8b0000 585c0000 45830000 16000014 16000024
 49: 1a000015 1a000025 06000002 38060000 4a830000 88a20000 7ca20000 528c0000
 57: 48230000 02000008 6c820000 32c60000 06000006 38260000 42830000 88670000
 65: 7d690000 568d0000 48630000 36ac0000 3c680000 46c30000 12000016 12000026
 73: 16000017 16000027 02000009 06000003 38260000 0c000007 3d8c0000 48d30000
 81: 6dc60000 8cd70000 7ed90000 5dce0000 4cd30000 2d2c0000 320d0000 4d230000
 89: 62c60000 86210000 712b0000 52610000 41230000 18000018 18000028 1d000019
 97: 1d000029 22450000 44230000 32040000 46230000 62430000 84570000 78590000
105: 55480000 44530000 35040000 48530000 0500000b 2b450000 44b30000 1600001a
113: 1200002a 1800001b 1400002b 22a10000 44230000 32040000 46230000 62430000
121: 84170000 77190000 51470000 44130000 31040000 47130000 21450000 44130000
129: 1600001e 1200002e 1700001f 1400002f 1000001c 1000002c 1000001d 1000002d
137: 10000020 10000030 10000021 10000031 f0000000
```
