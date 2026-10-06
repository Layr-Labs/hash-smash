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
well. The algorithm searches 2^127 such pairs for one where they do. The
search keeps no table and does no sorting or lookup. Seven trials are
evaluated in one 256-bit word, and a trial is charged 38 primitive operations,
memory loads included. Under the declared heuristics, H1 that a trial
completes the collision with probability at least 2^-128 and H2 that a budget
on early-test passes suffices, the search succeeds with probability at least
0.39. Total charged time is below 2^123.5 target-compression units, so the
claimed scalar is 123.5. Peak memory is below 2^20 bytes (Sections 6 to 9).

The rate in H1 is the rate of a uniform 128-bit value. It is still an
assumption, and it is not read off single digest words. Section 10 describes
the evidence. The remaining half of the digest depends on seven words. The
number of values of those seven words that give a collision was estimated by
sampling. The count for one sample is a full enumeration when it fits a work
budget and a random-subset estimate otherwise; the estimate was used for
84,443 of the 217,243 samples that reached the counter, and those carry
13.3% of the sum. Under the model that the seven words behave like
independent uniform words, the estimated rate is 10.6 +- 1.3 times 2^-128.
H1 assumes one times 2^-128, so the estimate leaves a factor of about 10 to
spare. The model was compared with real messages only on events of
probability 2^-32 and above. The organizer-run experiments measure neither
the model nor the rate.

No full 2-round collision is exhibited, and the search is far beyond feasible
computation. What is exhibited, and checked by the organizer's own runner, is
the exact half-collision and a toy-scale run of the two trial families,
without the early test and the packing that set the cost of a trial.

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
reads the block length n, the initial value of v[14], and it overwrites that
word; it is also the only call of round 0 that reads w4 and w5. Its inputs are
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

    X3 = a6c3b8c5   X7 = 793c473a   X11 = 5c32535c   X15 = 8367c7bb
    W4 = 60000001   W13 = 29bd3f58

Then K + W4 = bbf2cd1e and W4' = ((K + W4) XOR 2) - K = 5fffffff, so
W4 - W4' = 00000002. Evaluate C3 = G(3,7,11,15, w4, W13) on the inputs
(X3, X7, X11, X15) with w4 = W4 and with w4 = W4':

    w4 = W4    a1=80000000 d1=c7bb0367 c1=23ed56c3 b1=1f95ad11
               a2=c952ec69 d2=0e0ee9ef c2=31fc40b2 b2=465cd3db
    w4 = W4'   a1=7ffffffe d1=3845fc98 c1=94784ff4 b1=8ceed440
               a2=36ac1396 d2=0e0ee9ef c2=a28739e3 b2=465cd3db

**Fact P.** The two executions give the same d output 0e0ee9ef and the same b
output 465cd3db. They differ in the a output (c952ec69, 36ac1396) and in the c
output (31fc40b2, a28739e3). This is a finite computation on the displayed
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
words give the same S and a state X that still has the four pinned values,
and they keep w4 = W4, w13 = W13 and w15 = 0. Message B is formed from them
by step S2. By Lemma L it has the same X, and by Lemma H the pair (A, B) is a
half-collision; both are honest byte strings because word 15 is zero.

**6.2 The residual of a trial.** With Y3, Y3', Y11, Y11' the a and c outputs of
C3 from Fact P (c952ec69, 36ac1396, 31fc40b2, a28739e3) and
delta = W4 - W4' = 00000002:

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
2. For each of the 2^63 values of (X13, X14) with X14 < 2^31, in a fixed
   order: run step S1 to get a context. For each of the 2^32 values of alpha:
   compute the D0 family and the per-alpha constants. For gamma = 0, 7, 14,
   ...: evaluate the early test for the seven trials gamma, .., gamma+6 in one
   packed word (6.5).
3. For every trial that passes the early test, compute R in full. If R = 0,
   build A and B by steps S2 and S3 from the trial's words, evaluate H(A) and
   H(B), check that they agree, output (A, B) and halt.
4. Halt with failure if 2^106 trials have passed the early test without R = 0,
   or when all trials are exhausted.

The trials are 2^63 * 2^32 * 2^32 = 2^127 distinct half-colliding pairs:
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

These bounds are for lanes whose gamma is below 2^32. In the final batch of
a gamma loop the three top lanes hold gamma = 2^32, 2^32 + 1 and 2^32 + 2 and
repeat the trials gamma = 0, 1, 2. There X12 is below 3B, d below 2B + 3, X1
below 4B, and the sums of C1 are below 5B (a1) and 8B (a2), so these lanes
also stay below 2^36. Carries move upward only and the rotation masks
discard bits shifted in from a neighbouring lane, so the four lanes below
them are not disturbed.

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
the call being evaluated), so they fit in the 16 registers. The comparison
and the branch in the table belong to the early test. The loop-exit test of
the gamma loop is not in the table; Section 8 charges it from the margin.

Each XOR followed by a rotation is 6 operations, a two-term sum 1, a
three-term sum 2; a rotation loads its two masks. For example C0 is
ROR(X12 XOR a1, 16) (6), + X8 (1), XOR X4 and rotate (6), b1 + (a1 + w6) (1),
XOR and rotate (6), + (1), XOR and rotate (6) = 27 operations, with loads for
a1, X8, X4, (a1 + w6) and four mask pairs = 12. The zero-lane detection adds
2^32 - 1 to every lane of the reduced test word and selects bit 32 of every
lane, which is set exactly in the lanes whose test word is nonzero.

*Machine check of the count (participant computation, not
organizer-verified).* The submitted program `experiments/halfsearch.py`
contains the counting reference for this table. It has a packed-word type
that counts one operation for every addition, XOR, AND, OR and shift, one
each for the final comparison and the branch, and one load for every use of
a constant. The batch is written on that type part by part as in the table,
and the test word of Lemma E is computed beside it in ordinary 32-bit
arithmetic. The command

    python3 experiments/halfsearch.py --selftest 400

runs 400 batches with the constants of 3.2 on contexts derived from a fixed
seed text; a third argument changes the seed. Every fourth batch is the
final batch of a gamma loop, with 2^32, 2^32 + 1 and 2^32 + 2 in its three
top lanes. The command prints one JSON line: the number of batches, the
lanes checked, the lanes whose test word equals the scalar word, the
operations and loads of every part and in total, and the bit length of the
largest lane value of any sum or XOR. For 400 batches it reports 2,800 of
2,800 lanes equal, 178 operations and 79 loads in every batch with every
part equal to its row of the table, and a largest lane value below 2^35.

In the organizer's run the experiment `residual-search` evaluates one such
batch on each trial's own context and alpha and reports its operations, its
loads and its number of equal lanes as observations. The organizer records
observations as untrusted participant numbers and credits no operation
count from them. This makes the count reproducible from the package; it
does not make it organizer-verified.

## 7. Success probability

The probability space is the one uniform 256-bit word of step 1, for the
fixed target. The algorithm is otherwise deterministic.

**Heuristic H1 (score-critical).** Over the coins, the 2^127 trials behave
with respect to the event R = 0 like independent events of probability at
least 2^-128 each, to the extent that the probability that no trial has R = 0
is at most exp(-1/2) + 0.002. The rate 2^-128 is the rate of a uniform
128-bit value; no factor above it is assumed. Section 10 describes the
evidence that the rate is at least uniform: an estimate of 10.6 +- 1.3 times
the uniform rate for the constants of 3.2 under the seven-word model, from a
participant computation in which 13.3% of the sum comes from a random-subset
estimator. The organizer-run experiments do not measure the rate.

**Heuristic H2 (supporting).** With probability at least 0.999 over the
coins, fewer than 2^106 of the 2^127 trials pass the early test of Lemma E
without having R = 0. (The pass rate measured on real trials is 2^-28.8,
which would give 2^98.2 passes, below the budget by a factor of 2^7.8. That
the number of passes of one run stays near this mean is part of the
assumption; Section 10 reports eight runs of 2^37 trials in support.)

Under H1 and H2 the algorithm outputs a collision with probability at least
1 - exp(-1/2) - 0.002 - 0.001 > 0.3934 - 0.003 = 0.3904 >= 0.39. When it
outputs a pair, the pair is a genuine collision: step 3 checks both complete
digests, and the messages have different lengths.

*Sensitivity to the rate.* If the rate is c * 2^-128, the 2^127 trials give
1 - exp(-c/2) - 0.003 with the same allowances, which reaches 0.39 only for
c >= 0.9985: the uniform rate itself leaves almost no slack on the
probability side, and the margin is the factor of about 10 between the
estimate and 1. For a general c the same success probability needs 2^127 / c
trials and time_log2 = 123.5 - log2 c.

Neither heuristic is proved. Section 10 lists the evidence and its limits.

## 8. Charged time

One 2-round target compression costs one unit and every other primitive word
operation costs 1/C units with C = 430.

- **Main loop.** A batch of seven trials uses 257 primitive operations by
  6.5, memory loads included. It is charged 266, that is 38 per trial. The
  extra 9 per batch cover the loop-exit comparison and branch of each batch
  (2 operations and at most one load, not listed in the table of 6.5), the
  last partial batch of each gamma loop (2^32 is not a multiple of 7; the
  final batch holds four trials and is charged in full) and a small margin.
  A gamma loop has 613,566,757 batches; at 260 each that is 159,527,356,820
  operations, below 38 * 2^32 = 163,208,757,248. The main loop costs at
  most 2^127 * 38 operations.
- **Per alpha.** The D0 family (about 25 operations) and placing the 5 lane
  constants that depend on alpha (C0's a1 and a1 + w6, X5, X5 + w3 and
  alpha) in seven lanes and storing them, 12 operations and one store each,
  are below 256 operations. There are 2^95 values of alpha in total: 2^103
  operations.
- **Per context.** Step S1 is below 2^10 operations. Placing and storing the
  14 lane constants that depend only on the context (-S11, S6, S12,
  -S1 - S6, X8, X4, X13, X9, X2 + w7, X14, w0, w12, w5 and w5 + delta) is
  14 * 13 = 182 more. Together they are below 2^11 operations. There are
  2^63 contexts: 2^74 operations.
- **Early-test passes.** At most 2^106 are processed (step 4). The batch
  keeps no values of a passing trial, so the trial is recomputed in scalar
  form from its gamma and completed, with the comparison of R: below 2^10
  operations each, 2^116 operations, which is 2^107.25 units.
- **Final step.** Steps S2, S3 and two complete hash evaluations with their
  input handling: below 2^11 operations and 2 units, once.
- **Randomness.** One random word, charged as one operation.
- **Preprocessing.** The six constants of 3.2 are stored in the program. They
  were produced by a solver run of under one second and selected among 4,140
  such sets by the measurements of Section 10, which used fewer than 2^56
  primitive operations in total. As a bound for recomputing a valid set that
  does not depend on that solver, exhaustive search over (w4, w13) for the
  four fixed inputs finds the constants with at most 2^64 candidates at two G
  evaluations and a comparison each, below 128 operations: 2^71 operations,
  below 2^63 units.

Total:

    T <= (38 * 2^127 + 2^116 + 2^103 + 2^74 + 2^56 + 2^11 + 1) / 430
         + 2 + 2^63
       <  38 * 2^127 * (1 + 2^-16) / 430 + 2^64
       <  2^123.4998 + 2^64
       <  2^123.50.

Here 38 * 2^127 / 430 = 2^(127 + 5.24793 - 8.74819) = 2^123.49974 and
log2(1 + 2^-16) < 0.00003. The submitted bound is time_log2 = 123.5. This is
a worst-case bound: the algorithm as stated halts within these budgets.

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
constants; it also covers their selection, and it is included in T.
nonuniform_advice_log2_bytes = 5 covers the 24 bytes of those constants.
There is no other stored data and no stored collision.

## 10. Evidence, scope and field meanings

**What is exact.** Sections 2 to 5 and Lemmas F and E. The declared
experiment `half-collision` runs steps S1 to S3 for the organizer's seeds and
the organizer recomputes both digests; the theorem predicts that every trial
agrees on the 128 masked digest bits.

**The seven-word model.** By 6.2 the residual of a trial is a function of
the constants and of seven 32-bit words: for E1 its first-half values d1 and
b1 and its a output a2 on message A, and for E3 the words Y4, Y9, w8 and its
first-half value h1 on message A. (E1's a1 and d1 are the same for A and B,
so a1 enters only through d1 and a2; each of the seven words is a bijective
image of one input or message word of its call when the others are fixed.)
The model M says that over the trials of the algorithm these seven words
behave like independent uniform words. Under M a trial has R = 0 with
probability c * 2^-128, where c * 2^96 is the number of the 2^224 values of
the seven words with R = 0. H1 is M together with c >= 1.

**How c was estimated (participant computation, not organizer-verified).**
Write tau, eps for the XOR differences between A and B of E1's a and c
outputs and beta for that of its first-half b. As in the proof of Lemma E,
E1's d and b output differences are ROR(tau, 8) and ROR(beta XOR eps, 7),
and E3's d and b output differences are ROR(eta XOR eps', 8) and
ROR(psi XOR tau', 7), where eta, psi are the XOR differences of E3's
first-half d and b and tau', eps' those of its c and a outputs. So R = 0
holds exactly when tau' = tau, eps' = eps, psi = tau XOR ROR(tau, 1) and
eta = eps XOR ROL(beta XOR eps, 1).

1. Draw (d1, b1, a2) uniformly. This fixes tau, eps, beta and hence the
   values eta and psi that E3 must produce.
2. Count the quadruples (Y4, h1, Y9, w8) for which E3 produces eta, psi,
   eps and tau. For a word x and a mask m, (x XOR m) - x is the signed
   sum over the bits i of m of (1 - 2 x_i) 2^i, so an addition whose XOR
   output difference is prescribed fixes the bits of its result on that mask
   once its additive input difference is known. E3 has four such additions.
   Their additive differences are the constant Y3' - Y3 and three signed sums
   (over the bits of eta, psi and ROR(eta XOR eps, 8)); the admissible values
   of those three are enumerated with a carry automaton, and for each choice
   the number of completions is a product of two carry automata, one for Y4
   against e1 = Y3 + Y4 and one for g1 + h2. When the enumeration exceeds a
   work budget a uniform random subset is used with the matching weight, so
   that the result is unbiased by construction. The value for such a sample
   is then an estimate and not a count, and a zero estimate does not prove
   a zero count. Four necessary conditions for a nonzero count, one per
   addition (that an admissible additive difference exists at all), are
   tested first; they are nested.
3. c is the mean of that value over the samples of step 1.

Results for the constants of 3.2. In 2^40 samples, 217,243 passed the four
necessary conditions and reached the counter. For 84,443 of them (38.9%)
the random subset was used, so their values are estimates; the other
132,800 were counted in full. 4,245 samples had a nonzero value (between
2^14.3 and 2^39.6), and the mean value was 10.6. Eight disjoint parts of
2^37 samples gave 14.4, 10.4, 9.9, 18.0, 7.2, 7.8, 9.8 and 7.6; the standard
error of the mean is 1.3. A recount that marks the estimates (third check
below) shows that 993 of the nonzero values are estimates and that the
estimates carry 13.3% of the sum; the largest of them is 2^37.7, so the
largest values of the run are counts made in full.

*Selection.* The six constants are the best of 4,140 farmed sets, chosen by
measurements of this kind. The 2^40-sample run above was made after the
choice, on fresh samples with a seed different from the selection runs, so
its 10.6 +- 1.3 is not a selection-stage figure. Smaller earlier runs on
these constants include the selection run itself and are biased upwards by
the choice; they are not quoted.

*Replication.* An agent on a second machine (RTX 3070 cards) repeated this
measurement for the same constants, with another seed and 2^39 samples.
109,179 samples reached the counter, a rate of 2^-22.26 against 2^-22.27 in
the 2^40 run. The work budget of the count was set lower there, so the
random subset was used for 55,707 of them (51%). 2,044 samples had a nonzero
value, and the mean value was 13.5 with a standard error of 3.7 as printed
by the counting program, against 10.6 +- 1.3. The two figures differ by less
than the standard error of the replication. Two limits. The programs are
the participant's, so this repeats the run and does not check the method.
And the sampler of that run was a separate build made on that machine with a
duty-cycle limit on the card; the source hash recorded with the result is
not that of the participant's sampler source, so the two samplers were not
verified to be identical.

*Heavy tail.* The 50 largest values carry 63% of the sum and average about
2^37 each (0.627 * 2^43.41 / 50). Without them the mean is 3.97. That
figure discards real mass and is not a lower bound; it shows how much of
the estimate rests on few values: the ten largest carry 27% of the sum and
the largest one 7%. H1 assumes the uniform rate, c >= 1, against the
estimate 10.6 +- 1.3, whose smallest eighth was 7.2.

**Checks of the count.** The first two checks below do not cover the
random-subset branch of the counting program.

For 30 outcomes of a separate run of 2^37 samples on the same constants, 20
with counts between 2^15 and 2^32 and 10 with count zero, the E3 system was
encoded as CNF and given to a SAT solver and to the approximate model
counter ApproxMC (tolerance 0.4, confidence 0.9). The 10 were unsatisfiable
and the 20 counts agreed within 0.07 bits. All 30 were enumerated in full:
the check skips every outcome that used the random subset. Its counts stop
at 2^32; the larger values are covered by the fourth check below.

The counting program, compiled for 8-bit words, returned exactly the
brute-force count on each of 400 random constant sets (see the scaled-down
check below). With 8-bit words the lists stay far below the work budget, so
that build cannot reach the random-subset branch on any set.

The third check is a dedicated check of the random-subset branch. The 2^40
run was counted again by a build that marks the branch, on the same samples
and with the same budget, and it reproduced the totals of the first count.
Of the 84,443 samples that used the random subset, 993 have a nonzero
estimate and 83,450 an estimate of zero. The branch carries 13.3% of the
whole sum, so the samples counted in full give about 9.2 of the 10.6 by
themselves. Three groups of outcomes of the branch were then given to the
SAT solver and to ApproxMC (tolerance 0.4, confidence 0.9). For the 40
largest estimates, which carry 10.0% of the whole sum, the sum of the
estimates is 0.986 times the sum of the independent counts; the log2
differences have mean +0.15 and standard deviation 0.39 and lie between
-0.86 and +1.32. For 100 others drawn at random among the nonzero estimates
the ratio of the sums is 1.050; the log2 differences have mean +0.26 and
standard deviation 1.12 and lie between -2.81 and +4.92, so a single
estimate can be far off while the sums agree. All 100 outcomes drawn at
random among the zero estimates are unsatisfiable. No group shows a bias of
the branch in the sums beyond about 5%, which is inside the tolerance of the
independent counter. This check is also a participant computation, and it
covers 240 of the 84,443 outcomes of the branch.

The fourth check does the same for the outcomes that were counted in full:
3,252 with a nonzero count and 129,548 with zero, which carry 86.7% of the
whole sum. The 40 largest of them, which carry 55.0% of the whole sum and
include the largest count 2^39.6, were all counted by ApproxMC with the
same settings. The sum of the counter's values is 1.005 times the sum of
the independent counts, and the log2 differences have standard deviation
0.05 and lie between -0.08 and +0.10. For 60 further nonzero counts drawn at
random the ratio of the sums is 1.000, and the log2 differences have
standard deviation 0.03 and lie between -0.08 and +0.08.

Taken together, an independent counter confirms 55.0% of the whole sum
outcome by outcome (the 40 largest counts made in full, each within 0.10
bits) and a further 10.0% in sum (the 40 largest estimates, which singly
differ by -0.86 to +1.32 bits). The rest of the sum is covered by random
samples only. All four checks are participant computations.

A complete solution of the seven-word system, which can be checked by hand
from 6.2: Y1 = 7c96bbc3, Y6 = 8369443d, Y12 = 7931fd76, w12 = 00000000,
w5 = 9b4b734d, Y4 = 013e9e10, Y9 = 2d7d1bc5, Y14 = eda46000, w15 = 0,
w8 = f9608dfb. For these values the four residual words of 6.2 are zero. It
shows that the constants of 3.2 do not exclude R = 0; it does not show that a
message reaches such values.

**Checks of the model on real messages (participant measurement).** The
main comparison is 2^40 real trials against 2^40 draws of the seven words of
the model, with independent random streams. The real trials are pairs of the
theorem with the constants of 3.2: 2^28 independent random contexts with 2^12
trials each, every trial with a fresh random alpha and a fresh random Y4. The
last column is the difference over the square root of the sum of the counts.

| Statistic | Real | Model | Difference (sd) |
| --- | ---: | ---: | ---: |
| early test of Lemma E passed | 2,350 | 2,381 | -0.5 |
| residual word 0 zero | 249 | 201 | +2.3 |
| residual word 1 zero | 283 | 264 | +0.8 |
| residual word 2 zero | 273 | 276 | -0.1 |
| residual word 3 zero | 263 | 292 | -1.2 |
| Hamming weight of R at most 32 | 11,748 | 11,940 | -1.2 |
| Hamming weight of R at most 40 | 19,910,536 | 19,904,766 | +0.9 |
| low 16 bits zero in words 0 and 1 | 272 | 244 | +1.2 |
| low 16 bits zero in words 0 and 2 | 632 | 748 | -3.1 |
| low 16 bits zero in words 0 and 3 | 251 | 282 | -1.3 |
| low 16 bits zero in words 1 and 2 | 275 | 281 | -0.3 |
| low 16 bits zero in words 1 and 3 | 254 | 268 | -0.6 |
| low 16 bits zero in words 2 and 3 | 241 | 235 | +0.3 |

A uniform word gives 256 in each of the four word rows, and two independent
uniform words give 256 in each of the last six rows. The early test, a
32-bit condition that involves both E1 and E3, passes about nine times more
often than 2^-32 in both columns. Two differences stand out. The pair of
words 0 and 2 is 3.1 standard deviations below the model, and word 0 is 2.3
above it; the model count 201 for word 0 is itself 3.4 standard deviations
below 256. The squared differences sum to 23.5 over the 13 rows, which are
not independent of one another. One row of 13 at 3.1 is more than chance
readily gives, so this comparison is recorded as showing a possible
deviation from M at 2^-32, not as agreement within sampling error. No real
trial and no model draw had two residual words zero at once, so nothing in
this sample exercises Lemma E, which is exact.

Two limits of this comparison. First, its 2^28 contexts were drawn
independently of one another. That is not the enumeration of 6.4, in which
all contexts of a run share the seven seed words. Second, the generating
program draws Y4 for each trial and does not run the gamma family of 6.1,
which is a different but equivalent parametrisation of the same pairs.

A second measurement uses the layout of the algorithm: eight runs of 2^37
real trials of 6.1. Each run has its own seven seed words, shared by all its
contexts; a context is a random pair (X13, X14) with X14 < 2^29, which is a
quarter of the range of 6.4, and takes one alpha and a range of consecutive
gamma; every thread has an independent random stream. The early test passed
311, 298, 272, 266, 273, 283, 292 and 303 times, in all 2,298 times in 2^40
trials, against 2,367 in 2^40 draws of the model (1.0 standard deviations
below). The standard deviation of the eight counts is 16.3, against 16.9 for
independent trials at that mean. Summed over the eight runs, the four
residual words were zero 226, 263, 229 and 289 times, against 256 for a
uniform word. The model run of this measurement, made by a different program
from the one behind the table, printed only rounded rates for the four words
(2^-32.0, 2^-31.9, 2^-32.0 and 2^-31.9, so between 247 and 265 for word 0)
and does not repeat the low count 201. In every run the four nested necessary
conditions held at 2^-12.22, 2^-16.04, 2^-19.51 or 2^-19.52, and 2^-22.26 to
2^-22.28. This tests the shared-seed structure at 32 bits for eight seeds and
for events of probability 2^-32 and above; it does not test lower
probabilities, and it did not record the pair statistics of the table.

An earlier run of 2^40 trials in the form of 6.1 (2^22 contexts, one alpha
each, 2^18 consecutive gamma) gave 2,358 early-test passes, residual words
entirely zero in 270, 310, 262 and 269 trials, and a best trial with 41
trailing zero residual bits whose two digests agree on 210 of 256 bits. On
its trials the four nested necessary conditions of step 2 held with
frequencies 2^-12.22, 2^-16.04, 2^-19.51 and 2^-22.27, the same four values
to two decimals as in 2^40 draws of the model; these conditions involve
E1's three words only. The random streams of that program overlapped:
neighbouring threads shared context words shifted by one position. Every
trial was still a distinct valid pair, but the contexts were not independent
draws and X14 ranged over all 2^32 values, so this run is supporting
evidence and not the main comparison.

**Scaled-down end-to-end check (participant computation).** With short
words the whole search can be run and its collisions counted. The toy hash
is BLAKE3 with 2 rounds and W-bit words, for W = 8 and W = 10. Its IV words
are the top W bits of the real IV words. The permutation, the flags 11 and
the block lengths 60 and 62 are the same. G uses the rotations (4, 3, 2, 1)
for W = 8 and (5, 4, 3, 2) for W = 10. Everything used from Sections 3 to 6
is independent of the word size and is applied unchanged: the length
cancellation of 3.1, a pinned call as in 3.2, Lemma H, the construction of
Section 4, the two families of 6.1 and the residual of 6.2. A constant set
is six W-bit constants with the property of Fact P. The sets below were
taken from scans of random sets and chosen by their value of c alone. The
sets and the number of runs for each were fixed before its runs started.

One run is the search of 6.4 for one choice of the seven seed words, over
every (X13, X14), every alpha and every gamma: 2^(4W) trials. The residual
of every trial is computed in full; the early test of 6.3 and the packing
of 6.5 change the cost of a trial and not its outcome, and are not used. M
predicts c collisions per run, where c is the number of solutions of the
seven-word system divided by 2^(3W). Here c is exact: it is computed by
brute force, enumerating all values of E1's three words and of E3's four
words.

| W | c | Runs | Predicted | Observed | Runs with a collision | Expected |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | 4.051 | 240 | 972.2 | 987 | 233 | 235.8 |
| 8 | 3.248 | 50 | 162.4 | 147 | 48 | 48.1 |
| 8 | 2.521 | 64 | 161.3 | 175 | 60 | 58.9 |
| 8 | 0.998 | 161 | 160.7 | 152 | 98 | 101.7 |
| 8 | 0.269 | 250 | 67.4 | 81 | 66 | 59.1 |
| 8 | 0.102 | 250 | 25.4 | 29 | 28 | 24.2 |
| 8 | 0.030 | 250 | 7.5 | 6 | 6 | 7.4 |
| 10 | 1.966 | 80 | 157.3 | 146 | 64 | 68.8 |
| 10 | 1.135 | 80 | 90.8 | 88 | 53 | 54.3 |
| 10 | 0.054 | 40 | 2.2 | 2 | 2 | 2.1 |

Each row is one constant set. "Predicted" is c times the number of runs.
The last two columns are the number of runs with at least one collision
and the number expected if the trials were independent, which is the number
of runs times 1 - exp(-c). The first row adds 40 runs of a CPU program and
200 runs of a GPU program; the other 8-bit rows are from the CPU program
and the 10-bit rows from the GPU program.

The merged first row hides the weakest series. Taken alone, the 40 CPU runs
at c = 4.051 gave 161 collisions against 162.0 predicted, but a collision in
only 37 runs where 39.3 are expected: three runs without a collision against
0.7 expected, which chance alone gives with probability about 0.03. The 200
GPU runs on the same constants gave 826 collisions against 810.2 predicted
and a collision in 196 runs against 196.5 expected.

In total 1,813 collisions were observed and 1,807.2 predicted. No row
differs from its prediction by more than 1.7 standard deviations of a
Poisson count, and the squared differences in those units sum to 7.8 over
the ten rows. A collision occurred in 658 runs, against 660.2 expected (the
sum before rounding; the column as printed adds to 660.4). The ratio of
variance to mean of the collisions per run, which is 1 for independent
trials, was between 0.88 and 1.15 in every series of the table. Every hit
was checked again by building both messages and evaluating the toy hash on
each in full; none failed. A first test of the program on three further
8-bit sets, with four runs each, gave 2 collisions against 1.7 predicted,
both in the set predicted 0.7. A further 10-bit job on three more constant
sets was stopped before any set had finished; it contributes no row.

The counting program of the estimate above, compiled for 8-bit words,
returned exactly the brute-force count on each of 400 random constant sets.
An 8-bit build cannot reach the random-subset branch, on those 400 sets or
on the seven 8-bit sets of the table (which reported no use of it), so that
branch is not covered by this check.

This check tests M and the independence of the trials down to actual
collisions for words of 8 and 10 bits. It does not prove either for 32-bit
words.

The declared experiment `residual-search` runs the search of Section 6 at toy
scale: one context and one alpha per seed, consecutive gamma, stopping at the
first trial whose residual has a zero low byte in digest word 1. The search
runs without the early test and without the packing of 6.5, which change the
cost of a trial and not its outcome. The organizer checks that every
returned pair agrees on 136 digest bits. It says nothing direct about 128
bits. Beside the search, the program evaluates one packed batch per trial
and reports its operation count, its load count and its number of lanes
equal to the scalar test word as observations (6.5). The organizer does not
check these numbers.

**Limits of the evidence.**

- The rate in H1 is the uniform rate, and it is assumed. The estimate of
  10.6 +- 1.3 is quoted as supporting evidence that the rate is at least
  uniform, with a factor of about 10 to spare. It is a participant
  computation that the organizer-run experiments do not measure, and the
  success bound needs a factor of at least 0.9985.
- For 84,443 of the 217,243 samples that reached the counter the value is a
  random-subset estimate and not a count; these carry 13.3% of the sum. The
  first two checks of the counter did not cover that branch. The dedicated
  check covers 240 of its outcomes.
- The counting program is the participant's, and so is every check of it.
  An independent counter has confirmed 55.0% of the sum outcome by outcome
  (the 40 largest counts made in full, up to 2^39.6) and a further 10.0%
  in sum (the 40 largest estimates). The other 35% of the sum is covered
  only by random samples (60 counts made in full, 100 nonzero and 100 zero
  estimates), by the 30 outcomes of the first check on another sample, and
  by the exact agreement with brute force for 8-bit words.
- The count is a sample mean of a heavy-tailed quantity, and where the
  random subset was used a value is one noisy estimate (993 of the 4,245
  nonzero values). The standard error from eight parts may be optimistic.
  In a count over part of a second sample of 2^45 draws (76,274
  outcomes) the largest value was 2^43.3, well above the largest value
  2^39.6 of the 2^40 run. One value of that size among 2^40 samples adds
  about 10 to the mean, so the estimate can move by several times its
  quoted error according to whether such a value falls in the sample.
- The constants are the best of 4,140 sets by measurements of this kind.
  Only the 2^40-sample run is known to be free of that selection.
- M has been tested end to end, down to actual collisions, only for words
  of 8 and 10 bits. For 32-bit words it has been tested on real messages
  only for events of probability 2^-32 and above, and there one of the 13
  statistics compared is 3.1 standard deviations from the model. That the
  seven words of the enumerated trials meet the solution set at a rate of
  at least 2^-128 per trial over 2^127 trials is an extrapolation that no
  feasible experiment can test directly.
- All trials of a run share the seven seed words: w5, X2, X9 and the
  column-state words S2, S5, S6, S10, S11 and S14 are the same in every
  trial of a run, and trials of one context share most of their other
  words. Independence of the trials is assumed, not shown. The main 32-bit
  comparison drew 2^28 independent random contexts and so measures rates
  averaged over seeds. The run in the layout of the algorithm covers eight
  seeds and events of probability 2^-32 and above. The distribution of
  collisions within one run was tested only with 8-bit and 10-bit words.
- Single-word statistics are not evidence for the joint rate. An earlier
  version of this package, cancelled by the submitter before screening, used
  other constants and inferred a rate of half the uniform one from the
  frequencies of single zero residual words; the count described above gave
  0.024 for those constants. For some constant sets one residual word
  vanishes 40 times more often than a uniform word while the count is zero.
- H2 rests on the early-test pass rate measured on real trials: 2^40 with
  random contexts and eight runs of 2^37 in the layout of the algorithm.
  That the number of passes of a full run of 2^127 trials stays near the
  mean is assumed.

**Scope and limitations.**

- No full collision of the 2-round hash is exhibited. The search is an
  analytical cost claim like other packages on this track; unlike a birthday
  search it tests each trial against zero and so uses no memory.
- The two messages have different lengths, 60 and 62 bytes, and the
  construction relies on the true block length being a compression input, as
  the target profile specifies.
- The gain over a generic birthday search has two sources: half of the digest
  is matched by construction, which removes the table and about half of the
  round-1 work per trial, and the constants are chosen so that, by the
  estimate of this section, the remaining half matches at least as often as
  a uniform value. No factor above the uniform rate is assumed, so the
  exponent of the number of trials is reduced by one (2^127 instead of
  2^128), not by more.
- A brief literature search found free-start collisions and near-collisions
  of the compression function for reduced BLAKE variants, and no collision
  attack on the 2-round BLAKE3 hash. No priority or novelty claim is made.
- The time bound counts the arithmetic, logical and shift operations of the
  packed batch, its comparison and its branch, and one load for every use of
  a constant, on a 16-register machine. It is an upper bound under that
  convention, not a measured running time.

**Field meanings.**

- time_log2 = 123.5 bounds total charged time by 2^123.5 units.
- memory_log2_bytes = 20 bounds simultaneous storage by 2^20 bytes.
- preprocessing_log2 = 63 bounds the recomputation and selection of the six
  constants by 2^63 target-compression units.
- nonuniform_advice_log2_bytes = 5 bounds the stored constants by 32 bytes.
- success_probability = 0.39 holds under H1 and H2 as shown in Section 7.

The required baseline_improved identifier blake3-r2-nominal-v2 names the
organizer's nominal display reference 128, which is not an established attack,
a qualified baseline or a security bound. The claimed scalar 123.5 is lower
than that display value. Whether a qualified result improves the Yukon
incumbent is decided separately, and no Pareto dominance claim follows from
the scalar.
