# A free half-collision and a table-free residual search for 2-round BLAKE3

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
separately reported resource bound.

This exploratory package targets blake3-r2-prefix-v1. It has an exact part and
a heuristic part, and it keeps them apart.

**Exact part.** An explicit construction maps any nine 32-bit words to a
60-byte message A and a 62-byte message B whose complete 2-round BLAKE3-256
digests agree on digest words 0, 2, 5 and 7, that is on 128 of the 256 digest
bits. There is no search in this construction and no probability: it holds for
all 2^288 choices of the nine words (Sections 2 to 5).

**Heuristic part.** A collision needs the other four digest words to agree as
well. The algorithm searches 2^128 such pairs for one where they do. The
search keeps no table and does no sorting or lookup. Seven trials are
evaluated in one 256-bit word, and a trial is charged 38 primitive operations,
memory loads included. Under the declared heuristic H1 the search succeeds
with probability at least 0.39. Total charged time is below 2^124.5
target-compression units, so the claimed scalar is 124.5. Peak memory is
below 2^20 bytes (Sections 6 to 9).

No full 2-round collision is exhibited, and the search is far beyond feasible
computation. What is exhibited, and checked by the organizer's own runner, is
the exact half-collision and a toy-scale run of the search.

## 1. Exact complete hash on the messages used

H is unkeyed BLAKE3-256 with only rounds 0 and 1 kept in every compression.
Every message produced has n = 60 or n = 62 bytes. A message of n <= 64 bytes
is one chunk consisting of one block, with no parent node, so H evaluates
exactly one compression. The block is the message followed by 64 - n zero
bytes, used only for loading words. The compression has flags
CHUNK_START | CHUNK_END | ROOT = 11, true block length n, and chunk counter
and root-output counter both zero. There is no key and no derivation flag.

Decode the zero-filled block into sixteen little-endian 32-bit words w[0..15].
The IV is

    6a09e667 bb67ae85 3c6ef372 a54ff53a
    510e527f 9b05688c 1f83d9ab 5be0cd19.

Initialize v[0..7] = IV, v[8..11] = IV[0..3] and v[12..15] = (0, 0, n, 11).
The block length n is the initial value of v[14] and enters nowhere else. All
additions and subtractions on state and message words are modulo 2^32. ROR and
ROL rotate a 32-bit word. G(a,b,c,d,x,y) is

    v[a] = v[a]+v[b]+x;  v[d] = ROR(v[d] XOR v[a],16)
    v[c] = v[c]+v[d];    v[b] = ROR(v[b] XOR v[c],12)
    v[a] = v[a]+v[b]+y;  v[d] = ROR(v[d] XOR v[a],8)
    v[c] = v[c]+v[d];    v[b] = ROR(v[b] XOR v[c],7).

A round is four column calls followed by four diagonal calls on the current
schedule s, and between rounds s is replaced by s[P[i]] with
P = (2,6,3,10,7,0,4,13,1,11,12,5,9,14,15,8). Written out for the two retained
rounds, with names used throughout:

    round 0   K0 = G(0,4,8,12, w0, w1)     K1 = G(1,5,9,13, w2, w3)
              K2 = G(2,6,10,14, w4, w5)    K3 = G(3,7,11,15, w6, w7)
              D0 = G(0,5,10,15, w8, w9)    D1 = G(1,6,11,12, w10, w11)
              D2 = G(2,7,8,13, w12, w13)   D3 = G(3,4,9,14, w14, w15)
    round 1   C0 = G(0,4,8,12, w2, w6)     C1 = G(1,5,9,13, w3, w10)
              C2 = G(2,6,10,14, w7, w0)    C3 = G(3,7,11,15, w4, w13)
              E0 = G(0,5,10,15, w1, w11)   E1 = G(1,6,11,12, w12, w5)
              E2 = G(2,7,8,13, w9, w14)    E3 = G(3,4,9,14, w15, w8)

S denotes the state after K0..K3, X the state after round 0, Y the state after
C0..C3 and Z the final state. The compression output is
o[i] = Z[i] XOR Z[i+8] and o[i+8] = Z[i+8] XOR IV[i] for i = 0..7. The digest
H(m) is the first 32 output bytes, LE4(o[0]) || ... || LE4(o[7]).

This is the complete hash of the target profile restricted to inputs of 60
and 62 bytes: standard IV, standard flags, true block length, both retained
rounds with the standard permutation, standard feed-forward and the full
256-bit digest. It is not a free-start, chosen-IV, compression-only or
truncated-output setting.

## 2. Inverting one G call

Consider one call G(a,b,c,d,x,y) with input values A, B, C, D and name its
eight assignments

    a1 = A + B + x           d1 = ROR(D XOR a1, 16)
    c1 = C + d1              b1 = ROR(B XOR c1, 12)
    a2 = a1 + b1 + y         d2 = ROR(d1 XOR a2, 8)
    c2 = c1 + d2             b2 = ROR(b1 XOR c2, 7).

Its outputs are (a2, b2, c2, d2).

**Fact 1.** Reading the assignments backwards,

    b1 = ROL(b2, 7) XOR c2       c1 = c2 - d2       d1 = ROL(d2, 8) XOR a2
    B  = ROL(b1, 12) XOR c1      C  = c1 - d1
    a1 = ROL(d1, 16) XOR D       y  = a2 - a1 - b1      x = a1 - A - B.

So the four outputs determine b1, c1, d1 and the inputs B and C; and whenever
values A, B, C, D, a2, b2, c2, d2 satisfy the two equations for B and C, the
words x and y given by the last line make the call map (A,B,C,D) to
(a2,b2,c2,d2). Each line is one assignment solved for another of its terms.

## 3. Three ingredients

**3.1 The length is cancelled inside K2.** K2 is the only call of round 0 that
reads v[14], and the only call of round 0 that reads w4 and w5. Its inputs are
(IV[2], IV[6], IV[2], n). Put K = IV[2] + IV[6] = 5bf2cd1d. For lengths 60 and
62, whose XOR is 2, define for any w4, w5

    w4' = ((K + w4) XOR 2) - K        w5' = w5 + w4 - w4'.

**Lemma L.** K2 with block length 60 and words (w4, w5) leaves the same four
state words as K2 with block length 62 and words (w4', w5').

Proof. Let a1 = K + w4. In the second execution the first assignment gives
K + w4' = a1 XOR 2, so the second gives ROR(62 XOR a1 XOR 2, 16) =
ROR(60 XOR a1, 16), the same d1. The third and fourth depend only on d1 and
constants. The fifth gives (a1 XOR 2) + b1 + w5' = a1 + b1 + w5 because
w5' - w5 = w4 - w4' = a1 - (a1 XOR 2). The last three depend only on values
already shown equal. QED.

Hence two messages of 60 and 62 bytes that share every word except w4, w5,
related as above, have the same state S after the column step and the same
state X after round 0, since no other call of round 0 reads v[14], w4 or w5
before K2 has made the states equal. For both to be honest byte strings of
their lengths, word 15 must be zero in both: bytes 60..63 are zero fill for
the 60-byte message, and the 62-byte message is chosen to end in two zero
bytes, with bytes 62, 63 zero fill. This is the only constraint on the words.

**3.2 A pinned call C3.** Fix the six constants

    X3 = 38c3f8fd   X7 = df3c0829   X11 = f910a0e9   X15 = 16f60e91
    W4 = e7fffed8   W13 = 716f0d2f

Then K + W4 = 43f2cbf5 and W4' = ((K + W4) XOR 2) - K = e7fffeda, so
W4 - W4' = fffffffe. Evaluate C3 = G(3,7,11,15, w4, W13) on the inputs
(X3, X7, X11, X15) with w4 = W4 and with w4 = W4':

    w4 = W4    a1=fffffffe d1=f16fe909 c1=ea8089f2 b1=1db35bc8
               a2=8f2268f5 d2=fc7e4d81 c2=e6fed773 b2=77f69b19
    w4 = W4'   a1=00000000 d1=0e9116f6 c1=07a1b7df b1=ff6d89db
               a2=70dc970a d2=fc7e4d81 c2=04200560 b2=77f69b19

**Fact P.** The two executions give the same d output fc7e4d81 and the same b
output 77f69b19. They differ in the a output (8f2268f5, 70dc970a) and in the c
output (e6fed773, 04200560). This is a finite computation on the displayed
constants.

**3.3 Half of the digest does not see the difference.**

**Lemma H.** Take two executions of the 2-round compression that have the same
state X after round 0 and the same message words except w4 and w5. Suppose
(X[3], X[7], X[11], X[15]) = (X3, X7, X11, X15), w13 = W13, and w4 is W4 in the
first execution and W4' in the second. Then the two digests agree on digest
words 0, 2, 5 and 7.

Proof. C0, C1, C2 read neither w4 nor w5 and act on identical states, so they
leave identical values in both executions. C3 reads state words 3, 7, 11, 15
and the words w4, w13; by Fact P it leaves the same v[7] and v[15] in both
executions and may differ only in v[3] and v[11]. So Y agrees except possibly
in Y[3] and Y[11]. E0 reads Y[0], Y[5], Y[10], Y[15] and w1, w11. E2 reads
Y[2], Y[7], Y[8], Y[13] and w9, w14. None of these is Y[3], Y[11], w4 or w5, so
E0 and E2 produce identical outputs Z[0], Z[5], Z[10], Z[15] and Z[2], Z[7],
Z[8], Z[13]. Finally o[0] = Z[0] XOR Z[8], o[2] = Z[2] XOR Z[10],
o[5] = Z[5] XOR Z[13] and o[7] = Z[7] XOR Z[15] use only those eight words.
QED.

The remaining digest words o[1] = Z[1] XOR Z[9], o[3] = Z[3] XOR Z[11],
o[4] = Z[4] XOR Z[12] and o[6] = Z[6] XOR Z[14] are computed from the outputs
of E1 and E3 only. The **residual** of a pair is the 128-bit string
R = (o[1] XOR o'[1], o[3] XOR o'[3], o[4] XOR o'[4], o[6] XOR o'[6]). The pair
is a collision exactly when R = 0.

## 4. Construction: the message from the state after round 0

Round 0 with the fixed initial state is invertible: the state X after it
determines the sixteen message words. The construction uses this to place the
six constants of 3.2 where Lemma H needs them. Its input is nine free words

    X1, X2, X5, X6, X9, X10, X12, X13, X14.

**Step S1.** Set X3, X7, X11, X15 to the constants, w4 = W4, w13 = W13,
w15 = 0, and compute in this order, all arithmetic modulo 2^32:

    constants of K2:  p = K + W4;  q = ROR(p XOR 60, 16);  r = q + IV[2];
                      u = ROR(r XOR IV[6], 12)
    from D1:   b = ROL(X6,7) XOR X11;   c = X11 - X12;   d = ROL(X12,8) XOR X1
               S6 = ROL(b,12) XOR c;    S11 = c - d;     keep b, d as bD1, dD1
    link:      S10 = u XOR ROL(S6,7)
    from D0:   b = ROL(X5,7) XOR X10;   c = X10 - X15;   S5 = ROL(b,12) XOR c
               d = c - S10;             X0 = d XOR ROL(X15,8);  keep b, d as bD0, dD0
    K2:        S14 = S10 - r;   S2 = ROL(S14,8) XOR q;   w5 = S2 - p - u
    from D3:   d = ROL(X14,8) XOR X3;   a = ROL(d,16) XOR S14;   b = X3 - a - w15
               X4 = ROR(b XOR X9, 7);   c = X9 - X14
               S4 = ROL(b,12) XOR c;    S9 = c - d;      keep a as aD3
    K1:        (S1, S13, w2, w3) = COL(1, S5, S9, 0)
    from D2:   d = ROL(X13,8) XOR X2;   a = ROL(d,16) XOR S13;   b = X2 - a - w13
               X8 = b XOR ROL(X7,7);    c = X8 - X13
               S7 = ROL(b,12) XOR c;    S8 = c - d;      w12 = a - S2 - S7
    K0:        (S0, S12, w0, w1) = COL(0, S4, S8, 0)
    K3:        (S3, S15, w6, w7) = COL(3, S7, S11, 11)
    words:     a = ROL(dD0,16) XOR S15;  w8 = a - S0 - S5;   w9 = X0 - a - bD0
               a = ROL(dD1,16) XOR S12;  w10 = a - S1 - S6;  w11 = X1 - a - bD1
               w14 = aD3 - S3 - S4

where COL(j, sb, sc, d0) inverts column call Kj from its b and c outputs:

    b1 = ROL(sb,7) XOR sc;   c1 = ROL(b1,12) XOR IV[4+j];   sd = sc - c1
    d1 = c1 - IV[j];         a1 = ROL(d1,16) XOR d0
    x = a1 - IV[j] - IV[4+j];   sa = ROL(sd,8) XOR d1;   y = sa - a1 - b1
    result (sa, sd, x, y).

**Step S2.** w4' = W4' and w5' = w5 + W4 - W4'.

**Step S3.** A is the first 60 bytes of the little-endian encoding of
w0..w15. B is the first 62 bytes of the encoding of the same words with w4, w5
replaced by w4', w5'.

**Lemma S.** For every choice of the nine free words, running round 0 forward
on the words of step S1 with block length 60 gives the column-step state
S[0..15] and the state X[0..15] of step S1, in particular
(X[3], X[7], X[11], X[15]) equal to the four constants; and w4 = W4,
w13 = W13, w15 = 0.

Proof. The three word values hold by definition. The rest is Fact 1 applied
call by call; every quantity is defined before it is used.

- D1 has outputs (X1, X6, X11, X12). Fact 1 gives its b and c inputs as the
  S6 and S11 of step S1, and its words as w10, w11 once its a and d inputs
  S1, S12 are known.
- D0 has outputs (X0, X5, X10, X15). Its b input is S5 by Fact 1. Its c input
  is c - d with d = ROL(X15,8) XOR X0; step S1 chooses X0 so that this equals
  S10. Its words are w8, w9 by Fact 1.
- D3 has outputs (X3, X4, X9, X14) and d input S14. With d and a as in step
  S1, Fact 1 gives y = X3 - a - b1 where b1 = ROL(X4,7) XOR X9; step S1
  chooses X4 so that b1 equals X3 - a - w15, hence y = w15 = 0. Its b and c
  inputs are S4, S9 and its first word is w14.
- D2 has outputs (X2, X7, X8, X13) and d input S13. In the same way step S1
  chooses X8 so that its second word is w13 = W13; its b and c inputs are
  S7, S8 and its first word is w12.
- K2 has inputs (IV[2], IV[6], IV[2], 60) and first word W4, so its first
  four assignments give p, q, r, u. Its outputs must be (S2, S6, S10, S14):
  the last assignment requires u XOR S10 = ROL(S6,7), which is the link line;
  the seventh requires S10 = r + S14; the sixth requires
  q XOR S2 = ROL(S14,8); the fifth gives w5 = S2 - p - u.
- K1, K0 and K3 have inputs (IV[j], IV[4+j], IV[j], d0) with d0 = 0, 0, 11
  and prescribed b and c outputs. COL is Fact 1 for that situation: it returns
  the a and d outputs and the two words.

So the sixteen words map the initial state to S under the column step, and S
to X under the diagonal step. QED.

## 5. The half-collision

**Theorem.** For every choice of the nine free words, steps S1 to S3 output
two distinct messages A and B, of 60 and 62 bytes, whose complete 2-round
digests agree on digest words 0, 2, 5 and 7.

Proof. By Lemma S, word 15 is zero, so A is an honest 60-byte message and B
an honest 62-byte message ending in two zero bytes, and the compression of A
is the one analysed in Lemma S. By Lemma L the compression of B has the same
state X after round 0. The two compressions share every word except w4, w5,
and satisfy the hypotheses of Lemma H by Lemma S and step S2. Lemma H gives
the four digest words. The messages are distinct because their lengths
differ. QED.

Distinct choices of the nine words give distinct states X and so distinct
messages A: the construction yields 2^288 different half-colliding pairs.

## 6. The search for the other half

**6.1 Trials.** A *context* is the output of step S1 for some nine words. Two
one-parameter families change four message words and keep everything else of
the context, including S and all of w0..w7 and w12..w15.

    D0 family, parameter alpha:
        c = alpha - X15;   d = c - S10;   X0 = ROL(X15,8) XOR d
        b = ROR(S5 XOR c, 12);   X5 = ROR(b XOR alpha, 7);   X10 = alpha
        a = ROL(d,16) XOR S15;   w8 = a - S0 - S5;   w9 = X0 - a - b
    D1 family, parameter gamma:
        X12 = X11 - gamma;   d = gamma - S11;   X1 = ROL(X12,8) XOR d
        b = ROR(S6 XOR gamma, 12);   X6 = ROR(b XOR X11, 7)
        a = ROL(d,16) XOR S12;   w10 = a - S1 - S6;   w11 = X1 - a - b

**Lemma F.** For every alpha, D0 with inputs (S0, S5, S10, S15) and words
(w8, w9) has outputs (X0, X5, alpha, X15). For every gamma, D1 with inputs
(S1, S6, S11, S12) and words (w10, w11) has outputs (X1, X6, X11, X12).

Proof. For D0: the first assignment gives a; the second ROR(S15 XOR a, 16) = d;
the third S10 + d = c; the fourth b; the fifth a + b + w9 = X0; the sixth
ROR(d XOR X0, 8) = X15 by the definition of X0; the seventh c + X15 = alpha;
the eighth X5. For D1: a; d; S11 + d = gamma; b; X1; ROR(d XOR X1, 8) = X12 by
the definition of X1; gamma + X12 = X11; X6. QED.

A *trial* is a context together with a pair (alpha, gamma). By Lemma F its
words give the same S and a state X that still has the four pinned values, so
the trial is the output of step S1 for nine words with X1, X5, X6, X10, X12
replaced, and by the theorem its pair (A, B) is a half-collision.

**6.2 The residual of a trial.** With Y3, Y3', Y11, Y11' the a and c outputs of
C3 from Fact P (8f2268f5, 70dc970a, e6fed773, 04200560) and
delta = W4 - W4' = fffffffe:

    (.., Y4, .., Y12) = C0 = G(X0, X4, X8, X12, w2, w6)
    (Y1, .., Y9, ..)  = C1 = G(X1, X5, X9, X13, w3, w10)
    (.., Y6, .., Y14) = C2 = G(X2, X6, X10, X14, w7, w0)
    E1 on A:  G(Y1, Y6, Y11,  Y12, w12, w5)         E1 on B:  G(Y1, Y6, Y11', Y12, w12, w5 + delta)
    E3 on A:  G(Y3,  Y4, Y9, Y14, w15, w8)          E3 on B:  G(Y3', Y4, Y9, Y14, w15, w8)

and R is formed from the eight output words of E1 and E3 as in 3.3. Write
a1, d1, c1, b1, a2, .. for the assignments of E1 and e1, h1, g1, f1, e2, h2,
g2, f2 for those of E3 in the order a, d, c, b; a prime marks message B.

**6.3 An early test on 32 bits.**

**Lemma E.** If R = 0 then
(f1 XOR f1') = t XOR ROR(t, 1) with t = a2 XOR a2'.

Proof. In E1 the inputs Y1, Y6, Y12 and the first word are the same for A and
B, so a1 and d1 are the same, and d2 XOR d2' = ROR(a2 XOR a2', 8). In E3,
f2 XOR f2' = ROR((f1 XOR f1') XOR (g2 XOR g2'), 7). R = 0 says in its first
word that a2 XOR a2' = g2 XOR g2' (digest word 1 is Z[1] XOR Z[9], the a output
of E1 and the c output of E3) and in its third word that
d2 XOR d2' = f2 XOR f2' (digest word 4 is Z[4] XOR Z[12], the b output of E3
and the d output of E1). Substituting, ROR(t, 8) = ROR((f1 XOR f1') XOR t, 7),
and rotating both sides left by 7 gives the claim. QED.

The test needs only the first five assignments of E1 and the first four of E3
for both messages.

**6.4 Algorithm.**

1. Draw one fresh uniform 256-bit word and take from it the seven words
   X1, X2, X5, X6, X9, X10, X12.
2. For each of the 2^64 values of (X13, X14) in a fixed order: run step S1 to
   get a context. For each of the 2^32 values of alpha: compute the D0 family and
   the per-alpha constants. For gamma = 0, 7, 14, ...: evaluate the early test
   for the seven trials gamma, .., gamma+6 in one packed word (6.5).
3. For every trial that passes the early test, compute R in full. If R = 0,
   build A and B by steps S2 and S3 from the trial's words, evaluate H(A) and
   H(B), check that they agree, output (A, B) and halt.
4. Halt with failure if 2^100 trials have passed the early test without R = 0,
   or when all trials are exhausted.

The trials are 2^64 * 2^32 * 2^32 = 2^128 distinct half-colliding pairs:
contexts differ in X13 or X14, which the families do not touch, and trials of
one context differ in X10 = alpha or X12 = X11 - gamma.

**6.5 Seven trials in one word.** A packed word holds seven lanes of 36 bits
at bit offsets 0, 36, .., 216. A lane represents its value modulo 2^32; bits
32..35 are carry guards. A constant is placed in all seven lanes once per
context or per alpha. Additions are single 256-bit additions. A rotation of
every lane by r is the five operations

    PROR(z, r) = ((z >> r) AND A_r) OR ((z << (32-r)) AND B_r)

with A_r selecting the low 32-r bits of every lane and B_r the next r bits;
the masks discard guard bits and bits shifted in from the neighbouring lane,
so the result is reduced below 2^32. A subtraction x - y of a constant x and a
lane y is (y XOR M) + (x + 1) with M = 2^32 - 1 in every lane, and adding the
constant -y for a constant y is one addition.

The lane layout, seven 36-bit lanes with reduction delayed to the rotations
and a five-operation masked rotation, follows the public ticket 2bf40fb on
this track, which uses it for a birthday search. What is evaluated in the
lanes here is different.

*No lane overflows.* Rotation outputs and constants are below 2^32. Every sum
formed in the batch has at most three summands that are each below 2^34, so
every lane stays below 2^36 and no carry leaves a lane. In detail, with
B = 2^32: X12, d, X1 and w10 of the D1 family are below 2B; in C0 the sums
are below 2B, 2B and 3B; in C1 they are below 3B (a1), 2B, 7B (a2) and 3B; in
C2 below 2B, 2B, 4B and 3B; in E1 below 3B (a1), 2B, 2B, 4B (e), 5B and 7B
(the two a2); in E3 below 2B. Since every lane sum is below 2^36, the low 32
bits of every lane equal the scalar value modulo 2^32, and XOR and PROR read
only those bits.

*Operation count of one batch.* The batch runs on a load/store machine with
16 registers. The second column counts additions, XOR, AND, OR, shifts, the
final comparison and the branch, with PROR = 5. The third column counts
memory traffic: every constant operand, that is a per-context or per-alpha
constant, a rotation mask or the reduction mask, is fetched from memory each
time it is used and charged as one load. Shift distances are fixed in the
instruction.

| Part | What is computed | Operations | Loads |
| --- | --- | ---: | ---: |
| loop | advance gamma in all lanes | 1 | 1 |
| D1 family | X12 (2), d (1), X1 (6), b (6), X6 (6), a (6), w10 (1) | 28 | 15 |
| C0 | from d1 on; a1 is a per-alpha constant | 27 | 12 |
| C1 | all but the b output; reduce Y1 and Y9 | 25 | 12 |
| C2 | all four outputs | 29 | 12 |
| E1, A and B | a1, d1, c1, c1', b1, b1', a2, a2' | 26 | 11 |
| E3, A and B | e1, e1', h1, h1', g1, g1', f1, f1' | 28 | 10 |
| early test | t, the test word, reduce, zero-lane detection, compare, branch | 14 | 6 |
| | total for seven trials | 178 | 79 |

So a batch is 178 + 79 = 257 primitive operations. No store is needed: gamma
stays in a register across batches, and at most 13 batch values are live at
any point (the six column outputs Y1, Y4, Y6, Y9, Y12, Y14 and the values of
the call being evaluated), so they fit in the 16 registers.

Each XOR followed by a rotation is 6 operations, a two-term sum 1, a
three-term sum 2; a rotation loads its two masks. For example C0 is
ROR(X12 XOR a1, 16) (6), + X8 (1), XOR X4 and rotate (6), b1 + (a1 + w6) (1),
XOR and rotate (6), + (1), XOR and rotate (6) = 27 operations, with loads for
a1, X8, X4, (a1 + w6) and four mask pairs = 12. The zero-lane detection adds
2^32 - 1 to every lane of the reduced test word and selects bit 32 of every
lane, which is set exactly in the lanes whose test word is nonzero.

## 7. Success probability

The probability space is the one uniform 256-bit word of step 1, for the
fixed target. The algorithm is otherwise deterministic.

**Heuristic H1 (score-critical).** Over the coins, the 2^128 trials behave
with respect to the event R = 0 like independent events of probability at
least 2^-129 each, to the extent that the probability that no trial has R = 0
is at most exp(-1/2) + 0.002. The rate 2^-129 is half the rate of a uniform
128-bit value; Section 10 explains why half is assumed and not the full rate.

**Heuristic H2 (supporting).** With probability at least 0.999 over the
coins, fewer than 2^100 of the 2^128 trials pass the early test of Lemma E
without having R = 0. (The test is one 32-bit condition; a rate of 2^-32 would
give 2^96.)

Under H1 and H2 the algorithm outputs a collision with probability at least
1 - exp(-1/2) - 0.002 - 0.001 > 0.3934 - 0.003 = 0.3904 >= 0.39. When it
outputs a pair, the pair is a genuine collision: step 3 checks both complete
digests, and the messages have different lengths.

Neither heuristic is proved. Section 10 lists the evidence and its limits.

## 8. Charged time

One 2-round target compression costs one unit and every other primitive word
operation costs 1/C units with C = 430.

- **Main loop.** A batch of seven trials uses 257 primitive operations by
  6.5, memory loads included. It is charged 266, that is 38 per trial. The
  extra 9 per batch cover the last partial batch of each gamma loop (2^32 is
  not a multiple of 7; the final batch holds four trials and is charged in
  full) and a small margin. The main loop costs at most 2^128 * 38
  operations.
- **Per alpha.** The D0 family (about 25 operations) and placing about 14
  constants in seven lanes (12 operations each) are below 256 operations.
  There are 2^96 values of alpha in total: 2^104 operations.
- **Per context.** Step S1 is below 2^10 operations. There are 2^64 contexts:
  2^74 operations.
- **Early-test passes.** At most 2^100 are processed (step 4). Each costs the
  remaining assignments of E1 and E3 for one trial and the comparison of R,
  below 2^8 operations: 2^108 operations.
- **Final step.** Steps S2, S3 and two complete hash evaluations with their
  input handling: below 2^11 operations and 2 units, once.
- **Randomness.** One random word.
- **Preprocessing.** The six constants of 3.2 are stored in the program. They
  were found by a solver run of under one second. As a bound that does not
  depend on that solver, exhaustive search over (w4, w13) for the four fixed
  inputs finds them with at most 2^64 candidates at two G evaluations and a
  comparison each, below 128 operations: 2^71 operations, below 2^63 units.

Total:

    T <= (38 * 2^128 + 2^108 + 2^104 + 2^74 + 2^11) / 430 + 2 + 2^63
       <  38 * 2^128 * (1 + 2^-25) / 430 + 2^64
       <  2^124.4998 + 2^64
       <  2^124.50.

Here 38 * 2^128 / 430 = 2^(128 + 5.24793 - 8.74819) = 2^124.49974. The
submitted bound is time_log2 = 124.5. This is a worst-case bound for the
algorithm as stated, which halts within these budgets on every run.

No table, sorting or lookup is charged because the algorithm has none: a
trial is tested against zero, not against other trials.

## 9. Memory, preprocessing and advice

The program is the step S1 formulas, the two families, the packed batch of
6.5 and a compression routine for the final check. Bound the code by 4096
instruction templates of at most four 256-bit words each: 2^14 words, which
is 2^19 bytes. Data is the context (48 words), the per-alpha constants
(below 32 words), the masks A_r and B_r (16 words), the batch temporaries
(below 64 words) and the two messages and digests of the final check: fewer
than 256 words, below 2^13 bytes. Peak memory is therefore below
2^19 + 2^13 < 2^20 bytes. There is no table and nothing grows with the number
of trials.

preprocessing_log2 = 63 is the bound of Section 8 for recomputing the six
constants; it is included in T. nonuniform_advice_log2_bytes = 5 covers the
24 bytes of those constants. There is no other stored data and no stored
collision.

## 10. Evidence, scope and field meanings

**What is exact.** Sections 2 to 5 and Lemmas F and E. The declared
experiment `half-collision` runs steps S1 to S3 for the organizer's seeds and
the organizer recomputes both digests; the theorem predicts that every trial
agrees on the 128 masked digest bits.

**Evidence for H1.**

- The declared experiment `residual-search` runs the search of Section 6 at
  toy scale: one context and one alpha per seed, consecutive gamma, stopping
  at the first trial whose residual has a zero low byte in digest word 1. The
  organizer checks that every returned pair agrees on 136 digest bits. This
  shows that trials with additional vanishing residual bits occur at about
  the expected frequency for 8 bits. It says nothing direct about 128 bits.
- Participant measurement, not organizer-verified: 2^38 trials (2^20
  contexts, one alpha each, 2^18 consecutive gamma). The number of trials
  whose residual has at least k trailing zero bits, counting from the low bit
  of digest word 1, was 1143183735, 76191207, 4901748, 299705, 18286, 1282,
  89 and 3 for k = 8, 12, 16, 20, 24, 28, 32 and 36, against the uniform
  values 2^(38-k) = 1073741824, 67108864, 4194304, 262144, 16384, 1024, 64
  and 4. The four residual words were entirely zero in 89, 33, 80 and 60
  trials, against 64 for a uniform word. The early test passed 40 times,
  against 64 at rate 2^-32, and never when Lemma E would forbid it. The best
  trial had 39 trailing zero residual bits; its two digests agree on 215 of
  256 bits.
- The same measurement is why H1 assumes half the uniform rate. One residual
  word (digest word 3) was zero about half as often as a uniform word, and
  the product of the four word frequencies relative to uniform is about 0.84.
  If the four words were independent, the rate of R = 0 would be about 0.84
  times 2^-128. H1 assumes 2^-129, that is 0.5 times 2^-128, and the
  algorithm runs 2^128 trials accordingly.
- Participant computation, not organizer-verified: the pair (E1, E3) can
  reach R = 0 for these constants when its other inputs are free. A SAT
  solver found, among others, Y1 = 3c444a80, Y6 = 41f64591, Y12 = 004e9c8f,
  w12 = ff01052f, w5 = d58fa000, Y4 = ca1f8768, Y9 = 1ce071be, Y14 = c39a3e02,
  w15 = 0, w8 = e7985464, for which the four residual words of 6.2 are zero.
  This can be checked by hand from 6.2. It shows that the constants of 3.2 do
  not exclude R = 0; it does not show that a message reaches such values.

**Limits of the evidence.** The residual is not uniform: individual residual
bits were measured with frequencies of 1 between 0.32 and 0.65. Trailing
zero runs occur at or slightly above the uniform rate in the measured range,
but that range ends at 36 bits, far below 128, and a structural reason that
would make R = 0 rarer than 2^-129 over the enumerated trials cannot be
excluded by these measurements. Independence of the four residual words and
of the trials is assumed, not shown. H2 rests on the same kind of measurement
for one 32-bit condition.

**Scope and limitations.**

- No full collision of the 2-round hash is exhibited. The search is an
  analytical cost claim like other packages on this track; unlike a birthday
  search it tests each trial against zero and so uses no memory.
- The two messages have different lengths, 60 and 62 bytes, and the
  construction relies on the true block length being a compression input, as
  the target profile specifies.
- The gain over a generic birthday search is a constant factor: half of the
  digest is matched by construction, which removes the table and about half
  of the round-1 work per trial. The exponent of the number of trials is not
  reduced.
- No literature survey was done for these properties and no priority or
  novelty claim is made.
- The time bound counts the arithmetic, logical and shift operations of the
  packed batch and one load for every use of a constant, on a 16-register
  machine. It is an upper bound under that convention, not a measured running
  time. Other packages on this track count arithmetic operations of their
  inner loop without such loads; scores are comparable only under one
  convention.

**Field meanings.**

- time_log2 = 124.5 bounds total charged time by 2^124.5 units.
- memory_log2_bytes = 20 bounds simultaneous storage by 2^20 bytes.
- preprocessing_log2 = 63 bounds the recomputation of the six constants.
- nonuniform_advice_log2_bytes = 5 bounds the stored constants by 32 bytes.
- success_probability = 0.39 holds under H1 and H2 as shown in Section 7.

The required baseline_improved identifier blake3-r2-nominal-v2 names the
organizer's nominal display reference 128, which is not an established attack,
a qualified baseline or a security bound. The claimed scalar 124.5 is lower
than that display value. Whether a qualified result improves the Yukon
incumbent is decided separately, and no Pareto dominance claim follows from
the scalar.
