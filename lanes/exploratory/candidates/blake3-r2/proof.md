# A free half-collision and a search inside one class for 2-round BLAKE3

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
separately reported resource bound.

This exploratory package targets blake3-r2-prefix-v1. It has an exact part and
a heuristic part, and it keeps them apart.

**Exact part.** An explicit construction maps any nine 32-bit words to a
60-byte message A and a 62-byte message B whose complete 2-round BLAKE3-256
digests agree on digest words 0, 2, 5 and 7, that is on 128 of the 256 digest
bits. There is no search in this construction and no probability: it holds for
all 2^288 choices of the nine words (Sections 2 to 5). A second exact
construction enumerates such pairs while it holds one internal word of round 1,
called Y4, inside a set of 65,536 values, the *class* (Section 6.1).

**Heuristic part.** A collision needs the other four digest words to agree as
well. The algorithm searches 2^104 such pairs, all with Y4 in the class, for
one where they do. The search has no table that grows with the number of trials
and does no sorting or lookup. Seven trials are evaluated in one 256-bit word,
in two stages. Every batch runs stage A, which tests six bit conditions on one
internal word of every trial (rule A). Only a batch in which a trial satisfies
rule A runs stage 2, which tests a 32-bit condition that every collision
satisfies. A batch in which no trial satisfies rule A is dropped; a trial that
fails rule A is examined further only if another trial of its batch satisfies
it, and Section 7 does not count such a trial. A trial is charged 17.4
primitive operations, memory loads included. Three heuristics are declared: H1,
that a trial satisfies rule A and completes the collision with probability at
least 2^-105; H2, that a budget on the passes of the second test suffices; and
H3, that at most one eighth of the batches run stage 2. Under the three the
search succeeds with probability at least 0.39. Total charged time is below
2^99.39 target-compression units, so the claimed scalar is 99.4. The search
needs less than 2^20 bytes of memory; the declared 2^35 bytes also cover the
computations by which the constants and the class were selected (Sections 6 to
9).

The rate in H1 is an assumption: 2^23 = 8,388,608 times the rate of a uniform
128-bit value. It is not read off single digest words. Section 10 describes
what it is set against. The remaining half of the digest depends on seven
words, one of which is Y4. Under the model that the other six behave like
independent uniform words over the trials, the rate is the number of solutions
of a fixed system of equations, and that number is counted: an enumeration
without sampling gives 29,977,922 times 2^-128 for Y4 in the class, as a lower
bound because part of the enumeration is left out. Rule A is not implied by a
collision: some solutions violate it and are lost. The figure that the claim
uses is therefore smaller. It leaves out every part of the count for which a
solver found a solution that violates rule A, 12,040 in all, and is 29,965,882.
H1 assumes 8,388,608 times, 3.57 times less. The six constants were found by a
solver search and chosen by this count. The class is the second largest by this
count among the 34 classes of these constants that were counted; Section 10
says why it is used. The counting program is not part of the package, and it
and all its checks are the participant's. The model was compared with real
messages only on events of probability about 2^-32 and above. The organizer-run
experiments measure neither the model nor the factor. With the uniform rate in
place of 8,388,608 times it, the same search needs 2^127 trials and gives
time_log2 = 122.4.

No full 2-round collision is exhibited, and the search is far beyond feasible
computation. What is exhibited, and checked by the organizer's own runner, is
the exact half-collision on trials of the search and a toy-scale run of the
class search, without the two tests and the packing that set the cost of a
trial. The program the organizer runs also contains the packed two-stage
batch, a machine that counts its operations and loads, and a self-test of
that count (Section 6.5). Those counts are the program's own; the organizer
does not check them.

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

    X3 = d5d881ca   X7 = aa277e35   X11 = 1f208000   X15 = 123f2142
    W4 = 7fffffff   W13 = fffd6e01

Then K + W4 = dbf2cd1c and W4' = ((K + W4) XOR 2) - K = 80000001, so W4 - W4' =
fffffffe, that is -2 modulo 2^32. Evaluate C3 = G(3,7,11,15, w4, W13) on the
inputs (X3, X7, X11, X15) with w4 = W4 and with w4 = W4':

    w4 = W4    a1=fffffffe d1=debcedc0 c1=fddd6dc0 b1=3f557fa1
               a2=3f52eda0 d2=60e1ee00 c2=5ebf5bc0 b2=c2c3d448
    w4 = W4'   a1=00000000 d1=2142123f c1=4062923f b1=c0aea45e
               a2=c0ac125f d2=60e1ee00 c2=a144803f b2=c2c3d448

**Fact P.** The two executions give the same d output 60e1ee00 and the same b
output c2c3d448. They differ in the a output (3f52eda0, c0ac125f) and in the c
output (5ebf5bc0, a144803f). This is a finite computation on the displayed
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
               d = c - S10;             X0 = d XOR ROL(X15,8)
               keep b, d as bD0, dD0
    K2:        S14 = S10 - r;   S2 = ROL(S14,8) XOR q;   w5 = S2 - p - u
    from D3:   d = ROL(X14,8) XOR X3;  a = ROL(d,16) XOR S14;  b = X3 - a - w15
               X4 = ROR(b XOR X9, 7);   c = X9 - X14
               S4 = ROL(b,12) XOR c;    S9 = c - d;      keep a as aD3
    K1:        (S1, S13, w2, w3) = COL(1, S5, S9, 0)
    from D2:   d = ROL(X13,8) XOR X2;  a = ROL(d,16) XOR S13;  b = X2 - a - w13
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

**Step S2.** w4' = W4' and w5' = w5 + W4 - W4', all modulo 2^32. For the
constants of 3.2 that is w5' = w5 + fffffffe, the same as w5 - 2.

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

**6.1 Trials.** A *context* is the output of step S1 for some nine words: the
words w0..w15 and the states S and X. A trial replaces seven message words of
a context, w6..w11 and w14, so that one word of round 1 takes a prescribed
value. That word is Y4, the b output of C0.

*The class.* The first message word of E3 is w15 = 0, so the first assignment
of E3 is e1 = Y3 + Y4 for message A and e1' = Y3' + Y4 for message B, with Y3 =
3f52eda0 and Y3' = c0ac125f from Fact P. Put DY3 = Y3' - Y3 = 815924bf. The
second assignment is h1 = ROR(Y14 XOR e1, 16), so the XOR difference between A
and B of E3's first-half d value is

    eta = h1 XOR h1' = ROR((Y3 + Y4) XOR (Y3 + Y4 + DY3), 16),

a function of Y4 alone. Fix eta = e7c1815f. The *class* is the set of all words
Y4 that give this eta.

**Lemma Q.** The class is the set of all Y4 with

    ((Y3 + Y4) AND 015fe7c1) = 00036181.

It has 65,536 members: the 16 bits of e1 = Y3 + Y4 at the positions where
015fe7c1 has a zero are free, bit 31 among them, and Y4 = e1 - Y3.

Proof. Put x = ROL(eta,16) = 815fe7c1 and m = x AND 7fffffff = 015fe7c1. Here x
has bit 31, so m is x without that bit. Y4 is in the class exactly when e1 XOR
(e1 + DY3) = x, that is when (e1 XOR x) - e1 = DY3 modulo 2^32. For words e and
x, (e XOR x) - e is, modulo 2^32, the sum over the bits i of x of 2^i where bit
i of e is 0 and of -2^i where it is 1, which is 2 ((NOT e) AND x) - x; for i =
31 the two signs give the same word. So the condition is 2 ((NOT e1) AND x) =
DY3 + x modulo 2^32. Here DY3 + x = 02b90c80 modulo 2^32, which is even.
Doubling modulo 2^32 discards bit 31 of (NOT e1) AND x, so the condition does
not involve bit 31 of e1, and on the other bits it is ((NOT e1) AND m) =
02b90c80 >> 1 = 015c8640. All bits of 015c8640 lie in m, so this fixes the 16
bits of e1 on m to (e1 AND m) = (NOT 015c8640) AND m = 00036181 and leaves the
other 16 bits free. QED.

Member number k of the class, for 0 <= k < 65536, is the Y4 whose e1 has the
bits of k at its 16 free positions, in increasing order of position.

*The trial.* A **trial** is a context, a word alpha and a member y of the
class. Its message words are those of the context with w6..w11 and w14
replaced as follows. The lines are executed in order; S, X and w on the right
are the context's values until a line assigns the name, and the new value
from then on. bD1 and aD3 are the values kept in step S1.

    D0 family, parameter alpha:
        c = alpha - X15;   dD0 = c - S10;   X0 = ROL(X15,8) XOR dD0
        bD0 = ROR(S5 XOR c, 12);   X5 = ROR(bD0 XOR alpha, 7);   X10 = alpha
    C0 backwards from its b output y:
        pa = X0 + X4 + w2;   pd = ROR(X12 XOR pa, 16);   pc = X8 + pd
        pb = ROR(X4 XOR pc, 12);   Y8 = ROL(y,7) XOR pb;   Y12 = Y8 - pc
        Y0 = ROL(Y12,8) XOR pd;   w6 = Y0 - pa - pb
    K3 with its b output S7 kept:
        ka = IV[3] + IV[7] + w6;   kd = ROR(ka XOR 11, 16);   kc = IV[3] + kd
        kb = ROR(IV[7] XOR kc, 12);   S11 = ROL(S7,7) XOR kb;   S15 = S11 - kc
        S3 = ROL(S15,8) XOR kd;   w7 = S3 - ka - kb
    D1, D0 and D3 with the new S11, S15 and S3:
        d = (X11 - X12) - S11;   X1 = ROL(X12,8) XOR d
        a = ROL(d,16) XOR S12;   w10 = a - S1 - S6;   w11 = X1 - a - bD1
        a = ROL(dD0,16) XOR S15;   w8 = a - S0 - S5;   w9 = X0 - a - bD0
        w14 = aD3 - S3 - S4

The names assigned are X0, X5, X10, then S11, S15, S3, then X1, and the seven
words. Everything else, S7 in particular, keeps the context's value.

**Lemma F.** (a) For every alpha and every word S15, D0 with inputs
(S0, S5, S10, S15) and the words (w8, w9) above has outputs
(X0, X5, alpha, X15), and X0, X5 do not depend on S15. (b) For every word
S11, D1 with inputs (S1, S6, S11, S12) and the words (w10, w11) above has
outputs (X1, X6, X11, X12), where X6, X11, X12 are the context's. (c) For
every word S3, D3 with inputs (S3, S4, S9, S14) and the words (w14, w15) has
the context's outputs (X3, X4, X9, X14).

Proof. (a) The first assignment gives S0 + S5 + w8 = a; the second
ROR(S15 XOR a, 16) = dD0; the third S10 + dD0 = c; the fourth bD0; the fifth
a + bD0 + w9 = X0; the sixth ROR(dD0 XOR X0, 8) = X15 by the definition of X0;
the seventh c + X15 = alpha; the eighth X5. The lines that define X0 and X5
do not contain S15. (b) Put c = X11 - X12. In step S1, bD1 = ROL(X6,7) XOR X11
and S6 = ROL(bD1,12) XOR c, and none of X6, X11, X12, S6 is assigned by the
trial. The first assignment gives S1 + S6 + w10 = a; the second
ROR(S12 XOR a, 16) = d; the third S11 + d = c; the fourth
ROR(S6 XOR c, 12) = bD1; the fifth a + bD1 + w11 = X1; the sixth
ROR(d XOR X1, 8) = X12 by the definition of X1; the seventh c + X12 = X11;
the eighth ROR(bD1 XOR X11, 7) = X6. (c) D3 reads S3 only in its first
assignment, which gives S3 + S4 + w14 = aD3, the value it has in the context.
Its other inputs and w15 are the context's, so its outputs are. QED.

**Lemma Y.** For every word y, C0 with inputs (X0, X4, X8, X12) and words
(w2, w6) has b output y and d output Y12.

Proof. C0 reads w6 only in its fifth assignment. Its first four assignments
give pa, pd, pc, pb. The fifth gives pa + pb + w6 = Y0; the sixth
ROR(pd XOR Y0, 8) = Y12 by the definition of Y0; the seventh pc + Y12 = Y8;
the eighth ROR(pb XOR Y8, 7) = y by the definition of Y8. QED.

**Lemma K.** For every word w6, K3 with words (w6, w7) has outputs
(S3, S7, S11, S15): its b output is the S7 of the context, and its a, c and d
outputs are the new S3, S11 and S15.

Proof. K3 has inputs (IV[3], IV[7], IV[3], 11). Its first four assignments
give ka, kd, kc, kb. The fifth gives ka + kb + w7 = S3; the sixth
ROR(kd XOR S3, 8) = S15 by the definition of S3; the seventh kc + S15 = S11;
the eighth ROR(kb XOR S11, 7) = S7 by the definition of S11. QED.

**Lemma T.** For every trial, round 0 with block length 60 maps the trial's
words to the context's column-step state with S3, S11, S15 replaced, and to
the context's state X with X0, X1, X5, X10 replaced, as assigned above. So
(X[3], X[7], X[11], X[15]) are the four constants and w4 = W4, w13 = W13,
w15 = 0. In round 1, C0 has b output Y4 = y, a member of the class. The
messages A and B built from the trial's words by steps S2 and S3 have complete
2-round digests that agree on digest words 0, 2, 5 and 7.

Proof. The words w0..w5 are the context's, so K0, K1, K2 leave the context's
values by Lemma S, and K3 leaves (S3, S7, S11, S15) by Lemma K. D2 reads state
words 2, 7, 8, 13 and w12, w13, none of which changed, and leaves the
context's X2, X7, X8, X13. D0, D1 and D3 leave the stated outputs by Lemma F.
C0 reads X0, X4, X8, X12 and w2, w6, so Lemma Y gives Y4 = y. Finally, the
proof of the theorem of Section 5 uses the output of step S1 only through
three properties: w15 = 0, the state X after round 0 for block length 60 has
the four constants, and w4 = W4, w13 = W13. The trial's words have them, so
that proof applies to the trial unchanged. QED.

Every line of step S1 is an equation of one call of round 0, or one of the
three word values, solved for the name on its left. So it holds for any
sixteen words whose round 0 has these three word values and these four state
words, and the trial is the output of step S1 for the nine words
(X1, X2, X5, X6, X9, alpha, X12, X13, X14) of its own state. A trial is thus
one of the 2^288 pairs of Section 5, chosen so that its Y4 lies in the class.

**6.2 The residual of a trial.** With Y3, Y3', Y11, Y11' the a and c outputs of
C3 from Fact P (3f52eda0, c0ac125f, 5ebf5bc0, a144803f), delta = W4 - W4' =
fffffffe and the trial's words and state:

    (.., Y4, .., Y12) = C0 = G(X0, X4, X8, X12, w2, w6)
    (Y1, .., Y9, ..)  = C1 = G(X1, X5, X9, X13, w3, w10)
    (.., Y6, .., Y14) = C2 = G(X2, X6, X10, X14, w7, w0)
    E1 on A:  G(Y1, Y6, Y11,  Y12, w12, w5)
    E1 on B:  G(Y1, Y6, Y11', Y12, w12, w5 + delta)
    E3 on A:  G(Y3,  Y4, Y9, Y14, w15, w8)
    E3 on B:  G(Y3', Y4, Y9, Y14, w15, w8)

and R is formed from the eight output words of E1 and E3 as in 3.3. Y4 = y
and Y12 are known from 6.1 without evaluating C0. Write a1, d1, c1, b1, a2, ..
for the assignments of E1 and e1, h1, g1, f1, e2, h2, g2, f2 for those of E3
in the order a, d, c, b; a prime marks message B.

**6.3 Three tests of a trial.** The algorithm uses two tests: rule A, a
condition on one word of E3 (Lemma A), and the E1 test, a 32-bit condition
on E1 alone (Lemma N). A third test, the early test of Lemma E, was the test
of the submissions named in Section 10. The algorithm of this package does
not use it. It is kept because the measurements of Section 10 report its
passes.

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

A trial *passes the early test* when the word
(f1 XOR f1') XOR t XOR ROR(t, 1) is zero. The test needs the first five
assignments of E1 and the first four of E3 for both messages.

**Lemma N.** For a trial of 6.1 put beta = b1 XOR b1' and eps = c2 XOR c2',
both taken from E1, and

    n = eps XOR ROL(beta XOR eps, 1) XOR eta.

Let D3 and D6 be the XOR differences between A and B of digest words 3 and
6, which are the second and the fourth word of R. Then n = D3 XOR ROL(D6, 8)
for every trial. In particular R = 0 implies n = 0.

Proof. Digest word 3 is Z[3] XOR Z[11], the a output of E3 and the c output
of E1, so D3 = (e2 XOR e2') XOR eps. Digest word 6 is Z[6] XOR Z[14], the b
output of E1 and the d output of E3, so D6 = (b2 XOR b2') XOR (h2 XOR h2').
In E1, b2 = ROR(b1 XOR c2, 7), so b2 XOR b2' = ROR(beta XOR eps, 7). In E3,
h2 = ROR(h1 XOR e2, 8), and h1 XOR h1' = eta for every Y4 in the class (6.1),
so h2 XOR h2' = ROR(eta XOR e2 XOR e2', 8). Rotating D6 left by 8 gives
ROL(D6, 8) = ROL(beta XOR eps, 1) XOR eta XOR (e2 XOR e2'). The XOR with D3
cancels e2 XOR e2' and leaves n. QED.

A trial *passes the E1 test* when n = 0. The word n needs the first seven
assignments of E1 for both messages and nothing of E3: for a trial of 6.1
the eta of E3 is the constant of the class.

*Rule A.* Let h1 be the second value of E3 on message A, as in 6.2. A trial
*satisfies rule A* when all of the following hold:

    bit 16 of h1 is 1;
    bits 0 and 1 of h1 are equal;
    bits 1 and 2 of h1 are equal;
    bits 2 and 3 of h1 are equal;
    bits 3 and 4 of h1 differ;
    bits 23 and 24 of h1 differ.

These are six conditions, each on one bit or on the XOR of two bits, so a
uniform word satisfies rule A with probability 2^-6.

**Lemma A.** (a) For a trial of 6.1 let z = a2 XOR d1 be the XOR of the
fifth and the second value of C2, and e1 = Y3 + Y4. Then
ROL(h1, 24) = z XOR ROL(e1, 8): bit i of h1 is bit (i + 24) mod 32 of z XOR
bit (i + 16) mod 32 of e1. (b) For every Y4 in the class, the trial
satisfies rule A exactly when

    bit 8 of z is 0;
    bits 24 and 25 of z are equal;
    bits 25 and 26 of z differ;
    bits 26 and 27 of z are equal;
    bits 27 and 28 of z differ;
    bits 15 and 16 of z differ.

(c) Put S = 0f008000, ALL = 0f008100 and V = 0a008000. The word

    ((z XOR ((z >> 1) AND S)) AND ALL) XOR V

is zero exactly when the trial satisfies rule A.

Proof. (a) The sixth assignment of C2 is Y14 = ROR(d1 XOR a2, 8) = ROR(z, 8),
and the second assignment of E3 is h1 = ROR(Y14 XOR e1, 16). So h1 = ROR(z,
24) XOR ROR(e1, 16), and rotating left by 24 gives the claim. (b) Rule A
reads the bits 0, 1, 2, 3, 4, 16, 23 and 24 of h1. By (a) each of them is a
bit of z XOR a bit of e1, and the bits of e1 that enter are bits 0, 7, 8, 16,
17, 18, 19 and 20. All of these lie in the mask 015fe7c1 of Lemma Q, so they
have the same value for every member of the class: in 00036181, bit 0 is 1,
bit 7 is 1, bit 8 is 1, bit 16 is 1, bit 17 is 1, bit 18 is 0, bit 19 is 0
and bit 20 is 0. Inserting these values into the six conditions gives the
conditions on z. (c) Bit p of z XOR ((z >> 1) AND S) is the XOR of bits p and
p + 1 of z at the positions p of S and bit p of z elsewhere. S holds the
lower positions of the five conditions on two bits, ALL holds these and the
position of the condition on one bit, and V holds the required values. QED.

*What Lemma A does not say.* Lemma A says that the word of (c) tests rule A
exactly. It does not say that a collision satisfies rule A, and that is not
true: there are solutions of R = 0 with Y4 in the class whose h1 violates rule
A, and Section 10 prints one. Rule A is therefore a filter that loses
solutions. A batch in which no trial satisfies it is dropped, whether or not
one of its trials has a zero residual; a trial that fails rule A is examined
further only if another trial of its batch satisfies it (6.4). How much is lost
is a question about the count of Section 10 and is answered there: the figure
that H1 is set against leaves out, in full, every outcome of the count for
which a solver found a solution that violates rule A. For the other outcomes
three solvers answer that no such solution exists; these answers are not
certified.

**6.4 Algorithm.**

1. Draw one fresh uniform 256-bit word and take from it the four words X2, X5,
   X6, X9. Set X1 = X10 = 0: every trial replaces X1, and the D0 family
   replaces X5 and X10 and keeps S5, which the drawn X5 determines.
2. For each of the 2^56 values of (X12, X13, X14) with X12 < 2^8 and X13 <
   2^16, in a fixed order: run step S1 to get a context. For each of the 2^32
   values of alpha: compute the D0 family, the first half of C0 and the
   per-alpha constants. Then run the batches of 6.5 for the 65,536 members of
   the class in the order of their numbers, seven members in one packed word.
   Every batch runs stage A, which tests rule A for its seven trials. If none
   of them satisfies rule A the batch ends and its trials are dropped.
   Otherwise the batch runs stage 2, which evaluates the E1 test for its seven
   trials.
3. For every trial of a batch that ran stage 2 whose E1 test word is zero,
   compute its words by 6.1 and R in full. If R = 0, build A and B by steps S2
   and S3 from the trial's words, evaluate H(A) and H(B), check that they
   agree, output (A, B) and halt.
4. Halt with failure if 2^88 trials have been processed in step 3 without R =
   0; or if 9,363 * 2^85 batches have run stage 2, which is one eighth of the
   9,363 * 2^88 batches of a run; or when all trials are exhausted.

A trial with R = 0 that satisfies rule A is found: its batch runs stage 2,
its E1 test word is zero by Lemma N, and step 3 computes its residual,
unless one of the two budgets of step 4 has ended the run before. A trial
with R = 0 that violates rule A is found only if another trial of its batch
satisfies rule A; Section 7 does not count such trials.

The contexts are 2^8 * 2^16 * 2^32 = 2^56, and the trials are 2^56 * 2^32 *
2^16 = 2^104 half-colliding pairs by Lemma T, and they are distinct. Two
contexts differ in X12, X13 or X14, which no trial changes, so their trials
have different states X and different words. Trials of one context with
different alpha differ in X10 = alpha. Trials of one context and one alpha with
different members differ in Y4, which is a function of the words.

**6.5 Seven trials in one word.** A packed word holds seven lanes of 36 bits
at bit offsets 0, 36, .., 216. A lane represents its value modulo 2^32; bits
32..35 are carry guards. A constant is placed in all seven lanes once per
context or per alpha. Additions are single 256-bit additions. A rotation of
every lane by r is the five operations

    PROR(z, r) = ((z >> r) AND A_r) OR ((z << (32-r)) AND B_r)

with A_r selecting the low 32-r bits of every lane and B_r the next r bits;
the masks discard guard bits and bits shifted in from the neighbouring lane,
so the result is reduced below 2^32. With M = 2^32 - 1 in every lane, a
difference x - y of two lanes is x + (y XOR M) + 1, the difference of a
constant x and a lane y is (y XOR M) + (x + 1), and adding the constant -y
for a constant y is one addition.

The lane layout, seven 36-bit lanes with reduction delayed to the rotations
and a five-operation masked rotation, follows the public ticket 2bf40fb on
this track, which uses it for a birthday search. What is evaluated in the
lanes here is different.

*What a batch computes.* The seven trials of a batch share a context and an
alpha and are seven consecutive members of the class. The members enter through
one list that does not depend on the context: for batch j, U[j] holds ROL(y,7),
one member y per lane. The list has 9,363 packed words, because 65536 = 9,362 *
7 + 2; the five spare lanes of the last word repeat its last member. The list
is computed once, before step 2. A batch has two stages. Stage A computes in
every lane, in the names of 6.1 to 6.3:

- C0 backwards: Y8 = U[j] XOR pb, Y12 = Y8 - pc, Y0 = ROL(Y12,8) XOR pd and
  ka = Y0 + (IV[3] + IV[7] - pa - pb), which is IV[3] + IV[7] + w6.
- K3: kd, kc, kb, S11, S15 = S11 - kc, S3, and the first value of C2,
  v = X2 + X6 + w7, as S3 - (ka + kb) + (X2 + X6).
- C2 to z: its second to fifth values and z, the XOR of the fifth and the
  second.
- Rule A: the word of Lemma A (c), and whether it is zero in some lane.

If that word is zero in no lane, the batch ends. Otherwise stage 2 computes:

- The entry count: the number of batches that have run stage 2 is advanced
  and compared with its budget (step 4).
- C2, rest: Y14 = ROR(z, 8) and Y6, its sixth and eighth values.
- D1: d = (X11 - X12) - S11, X1 = ROL(X12,8) XOR d and a = ROL(d,16) XOR S12.
- C1 to Y1: its first five assignments. The first is X1 + (X5 + w3) and the
  fifth, Y1, is the sum of the first, the fourth, a and the constant
  -S1 - S6, since w10 = a - S1 - S6.
- E1 on A and B: a1, d1, c1, c1', b1, b1', a2, a2', c2, c2'.
- The E1 test: eps = c2 XOR c2', beta XOR eps, the word n of Lemma N, and
  whether n is zero in some lane.

Nothing of E3 is evaluated in a batch. Rule A is a condition on h1, a value
of E3, but by Lemma A it is tested on z, a value of C2, with the bits of e1
that it needs folded into the constant V. The words w6, w7 and w10 are never
formed on their own, and w8, w9, w11 and w14 are not needed in a batch: step
3 computes them for the trials it processes.

*No lane overflows.* Rotation outputs, list entries and constants are below
B = 2^32, and an XOR is never longer in bits than its operands. Every sum
formed in the batch is below 10 B, which is below 2^36, so no carry leaves a
lane. In detail: Y12 and ka are below 2B. In K3, kc is below 2B, S15 below
3B, ka + kb below 3B, its complement (ka + kb) XOR M below 4B and v below 6B.
In C2 the third value is below 2B and the fifth, v plus two values below B,
is below 8B; z, the XOR of the fifth and the second, is below 8B. The only
sum of the rule A part is the one that forms the flags, below 2B. In stage
2 the sum for Y6 is below 3B. In D1, d and X1 are below 2B. In C1 the sums
are below 3B (first), 2B and 6B (Y1, a sum of a value below 3B and three
values below B). In E1 they are below 8B (a1 = Y1 + Y6 + w12), 2B (c1 and
c1'), 10B (the two a2) and 3B (c2 and c2'). The only sum of the E1 test
forms the flags, below 2B. Since every lane stays below 2^36, the low 32
bits of every lane equal the scalar value modulo 2^32, and XOR and PROR
read only those bits. In the word of Lemma A (c), S and ALL lie below bit
31, so (z >> 1) AND S reads bit p + 1 of the same lane for the positions p
of S, the AND with ALL discards the guard bits of z, and the word is below
B. The word n is reduced by an AND with M.

*Operation count of one batch.* The batch runs on a load/store machine with 16
registers. The second column counts additions, XOR, AND, OR, shifts, the
comparisons and the branches, with PROR = 5. The third column counts memory
traffic: every constant operand, that is a per-context or per-alpha constant, a
list entry, a rotation mask, the mask M, a constant of rule A or a budget, is
fetched from memory each time it is used and charged as one load. Shift
distances are fixed in the instruction.

| Part | What is computed | Operations | Loads |
| --- | --- | ---: | ---: |
| loop | next list position, end test, branch | 3 | 1 |
| C0 backwards | Y8 (1), Y12 (1), Y0 (6), ka (1) | 9 | 7 |
| K3 | kd (6), kc (1), kb (6), S11 (1), S15 (3), S3 (6), v (4) | 27 | 14 |
| C2 to z | d1 (6), c1 (1), b1 (6), fifth (2), z (1) | 16 | 8 |
| rule A | word (5), flags and branch (4) | 9 | 6 |
| | stage A, every batch | 64 | 36 |
| entry count | next count, budget test, branch | 3 | 1 |
| C2, rest | Y14 (5), c2 (1), Y6 (6) | 12 | 4 |
| D1 | d (2), X1 (1), a (6) | 9 | 6 |
| C1 to Y1 | first (1), d1 (6), c1 (1), b1 (6), Y1 (3) | 17 | 9 |
| E1, A and B | a1 d1 (8), c1 c1' b1 b1' (14), a2 a2' c2 c2' (18) | 40 | 15 |
| E1 test | eps, beta XOR eps (3), n (8), flags and branch (4) | 15 | 7 |
| | stage 2, only after a pass of stage A | 96 | 42 |

So stage A is 64 + 36 = 100 primitive operations and stage 2 is 96 + 42 = 138.
No store is needed: the list position and the entry count stay in two registers
across batches, and the batch values that are live at any point fit in the
other 14; the self-test below reports the number in use.

Each XOR followed by a rotation is 6 operations, a two-term sum 1, a
three-term sum 2 and a difference of two lanes 3; a rotation loads its two
masks. For example K3 is: ka XOR 11 and rotate (6), + IV[3] (1), XOR IV[7]
and rotate (6), XOR ROL(S7,7) (1), S11 - kc (3), rotate S15 and XOR kd (6),
and for v the sum ka + kb (1), XOR M (1), + S3 (1), + (X2 + X6 + 1) (1): 27
operations, with loads for 11, IV[3], IV[7], ROL(S7,7), M, 1, M, X2 + X6 + 1
and three mask pairs: 14. The loads of C0 backwards are U[j], pb, -pc, pd,
the constant IV[3] + IV[7] - pa - pb and one mask pair. The loop advances
the list position, compares it with the end of the list, which is loaded,
and branches. In the rule A part the word of Lemma A (c) is a shift, an AND
with S, an XOR with z, an AND with ALL and an XOR with V (5 operations, 3
loads); the flags are formed by adding 2^32 - 1 to every lane and selecting
bit 32 of every lane, which is set exactly in the lanes whose word is
nonzero (2 operations, 2 loads); the flags are compared with a loaded
constant and stage A ends with a branch (2 operations, 1 load). The entry
count is one addition, a comparison with the loaded budget and a branch. In
C2, Y14 is a rotation of z (5) and Y6 a sum, an XOR and a rotation (7). In
E1, each of c2 and c2' is an XOR, a rotation and a sum (7). In the E1 test,
eps is one XOR, beta XOR eps two, and n a rotation by one, two XORs and the
AND with M (8, with loads for one mask pair, eta and M); the flags, the
comparison and the branch are as in stage A.

The per-alpha constants are seven: pb, -pc, pd and IV[3] + IV[7] - pa - pb
for C0, X5 and X5 + w3 for C1, and alpha for C2. The per-context constants
are fourteen. The constants S, ALL and V of rule A depend on the class
only.

*The count in the submitted program.* The program of the two declared
experiments, experiments/halfsearch.py, contains this batch and the machine
that counts it. A packed word is one integer with seven 36-bit lanes. Every
addition, XOR, AND, OR and shift of packed words is a call that adds one
operation, every constant operand and list entry is fetched by a call that
adds one load, and every comparison and every branch adds one operation.
The batch is written with these calls only; forming the constants and the
list word is not part of it. The program always evaluates both stages, so
that stage 2 is counted and checked for every batch; the algorithm runs
stage 2 only after a pass of stage A. The command

    python3 experiments/halfsearch.py --selftest N [seed]

runs N batches. The nine context words, alpha and the list position of a
case come from SHAKE-256 of the seed text (default 1) and the case number.
Every fourth case is the last batch of the class, and in every fifth case
each context word and alpha is 0, 2^32 - 1 or as drawn. Every lane is
checked against the real messages of its trial. The program builds the
messages A and B of the trial by steps S2 and S3 and compresses each in
full, with a 2-round compression written out from Section 1 and with no
shortcut of the batch. From these two compressions it takes Y4 of A; h1,
the second value of E3 on A; the word n of Lemma N, from E1 evaluated for A
and for B on their own states and words; and the two digests. A lane is
right when Y4 is the member of the lane, the digests agree on digest words
0, 2, 5 and 7, the stage-A flag says whether h1 satisfies rule A as written
in 6.3, the reduced word of stage 2 equals n, n equals D3 XOR ROL(D6, 8) of
the two digests, and the stage-2 flag says whether n is nonzero; and no
lane of a batch counts as right unless both branches are taken exactly when
one of the seven words in front of them is zero. The program prints one
JSON line: the number of cases, the lanes checked and the lanes right, the
lanes that satisfy rule A and the batches in which one does, the operations
and loads of every part and of both stages, whether they are the same in
every case and equal to the table above, for every part the largest lane of
a sum next to the bound quoted above, the largest number of registers in
use at one time, the number of per-context and per-alpha constants, the
number of class members in the list, for how many patterns of zero and
nonzero lanes the flags are right, and for how many packed words built from
all patterns of the bits of z that rule A reads the stage-A flags are
right. Its exit status is 0 only if all of these agree with this section.

With N = 2,000 and seed 1 it reports 14,000 of 14,000 lanes right; 64
operations and 36 loads in stage A and 96 and 42 in stage 2, per part as in the
table and the same in every case; largest sums of 1.997, 4.911, 6.622, 1.058,
2.952, 1.969, 5.618, 8.509 and 1.999 times 2^32 in C0 backwards, K3, C2 to z,
rule A, C2 rest, D1, C1, E1 and the E1 test, below the bounds 2, 6, 8, 2, 3, 2,
6, 10 and 2; 14 per-context and 7 per-alpha constants; 65,536 members in the
9,363 words of the list; and at most 11 registers in use. The register figure
follows every value, loaded constants and the intermediate values of a rotation
included, from the step that makes it to its last use, with the operations in
the order of the program, and adds two registers for the list position and the
entry count. In that run 215 lanes satisfy rule A, in 177 batches. None of the
14,000 words n of that run is zero, so the flags are also formed for all 128
patterns of zero and nonzero lanes: all 128 are right. Rule A reads eight bits
of z; the program forms 256 packed words in which every pattern of these bits
occurs once in every lane, with different other bits, filled guard bits and
another member of the class in every lane, and compares the stage-A flags with
rule A as written on h1 = ROR(ROR(z, 8) XOR e1, 16): all 256 are right, and a
lane satisfies rule A in 28 of them.

Longer runs of the same self-test, N = 1,200,000 with seed 61 and N = 1,200,000
with seed 62, report 16,800,000 of 16,800,000 lanes right and the same counts
in every batch; 261,798 lanes pass rule A, which is a share of 2^-6.004, in
205,330 of the 2,400,000 batches, a share of 0.0856 (every fourth batch of the
self-test is the last batch of the class, whose seven lanes hold only two
different members, so this share is below that of a run); no stage-2 test word
is zero; the largest lane of a sum is 9.496 times 2^32, and at most 11
registers are in use. The batch was first written and counted in the research
program in which rule A was found, with the same machine and the same
primitives: 8,400,000 lanes of this class, each compared with the complete
digests of its two messages, all right; 64 operations and 36 loads for stage A
and 93 and 41 for the rest, which is the stage 2 of this package without the
count of its own entry; 130,929 lanes passed rule A, in 102,378 of 1,200,000
batches.

In the declared experiment `residual-search` the same program evaluates one
batch per organizer seed, for that seed's context and alpha and the list
position that holds the first member tried, and returns the operations and
loads of its two stages, its number of right lanes and whether a lane
satisfied rule A as observations. The organizer's runner records
observations as untrusted and does not recompute them. The self-test and
these observations therefore show what the program in the package counts,
and that its lanes agree with the program's own compression of the real
messages. They are a participant check, not an organizer verification of
the cost.

## 7. Success probability

The probability space is the one uniform 256-bit word of step 1, for the
fixed target. The algorithm is otherwise deterministic. The trials depend on
that word only through the four words X2, X5, X6, X9.

Call a trial *good* when R = 0 and the trial satisfies rule A. By 6.4 a
good trial is found unless a budget of step 4 ends the run before.

**Heuristic H1 (score-critical).** Over the coins, the 2^104 trials behave with
respect to the event "good" like independent events of probability at least
2^-105 each, to the extent that the probability that no trial is good is at
most exp(-1/2) + 0.002. The rate 2^-105 is 2^23 = 8,388,608 times the rate of a
uniform 128-bit value. The factor is assumed. Section 10 describes what it is
set against: for Y4 in the class and under the seven-word model, a count
without sampling of the solutions of R = 0, from which every outcome for which
a solver found a solution that violates rule A is left out, and which gives the
lower bound 29,965,882 if the solvers' answers for the other outcomes are
right; a participant computation. The organizer-run experiments do not measure
the factor.

**Heuristic H2 (supporting).** With probability at least 0.9995 over the coins,
fewer than 2^88 of the 2^104 trials pass the E1 test of Lemma N without having
R = 0. (The budget corresponds to a pass rate of 2^-16. The pass rate measured
on real trials of the class search is 2^-29.42, which would give 2^74.58
passes, below the budget by a factor of 2^13.42. Step 3 processes only the
passes that lie in batches that ran stage 2, which are fewer. That the number
of passes of one run stays near this mean is part of the assumption; Section 10
reports eight runs of 2^40 trials in the layout of the algorithm, with between
1,432 and 1,527 passes of the E1 test each and no spread beyond chance.)

**Heuristic H3 (supporting).** With probability at least 0.9995 over the coins,
fewer than 9,363 * 2^85 of the 2^104 trials satisfy rule A. (A batch runs stage
2 only if one of its trials satisfies rule A, and every trial lies in one
batch, so the number of batches that run stage 2 is at most the number of
trials that satisfy rule A. The budget is a share 2^-5.81 of the trials. A
uniform h1 satisfies rule A with probability 2^-6. On real trials in the layout
of 6.4, with contexts and values of alpha sampled and every class loop
complete, 24 samples of 2^30 trials each have a share of trials that satisfy
rule A between 0.999565 and 1.000452 times 2^-6 and a share of batches that run
stage 2 of at most 0.104059; the budget of one eighth of the batches is larger
by a factor of 1.201. Four longer runs of 2^38 trials each, laid out like those
of the algorithm with the differences stated in Section 10, have a share of
trials of 2^-6.0000; seven times it is at most 0.10938, and the budget is
larger by a factor of 1.142. That the share of one run stays this close to its
mean is part of the assumption.)

Under H1, H2 and H3 the algorithm outputs a collision with probability at
least 1 - exp(-1/2) - 0.002 - 0.0005 - 0.0005 > 0.3934 - 0.003 = 0.3904 >=
0.39. When it outputs a pair, the pair is a genuine collision: step 3
checks both complete digests, and the messages have different lengths.

*Sensitivity to the factor.* If the rate of good trials is f * 2^-128, the
2^104 trials give 1 - exp(-f/2^24) - 0.003 with the same allowances, which
reaches 0.39 only for f >= 8,375,631: the assumed 8,388,608 leaves no slack on
the probability side. The margin of the claim lies between the assumed
8,388,608 and the counted 29,965,882, a factor of 3.57. For an f between 1 and
2^23 the same success probability needs 2^127 / f trials and, at the same 17.4
operations per trial, the total of Section 8 is below 2^(122.39 - log2 f):
below 2^99.39 at f = 2^23, and below 2^122.39 at f = 1, the uniform rate, where
17.4 * 2^127 / 430 = 2^122.37282 and the package would submit 122.4. With the
more cautious f = 2^22 = 4,194,304, which is 7.1 times below the count, the
same package would search 2^105 trials, twice as many contexts, and would
submit 100.4.

*Remark on clustering.* H1 asks for more than a rate: it asks that the good
trials do not come in clusters. Under M the count of Section 10 gives
29,965,882 * 2^104 / 2^128 = 1.78 expected good trials in a run, or more, where
H1 needs 0.5. Suppose that these trials came in clusters of m on average and
that the clusters fell independently. Then a run would contain one with
probability about 1 - exp(-1.78 / m), and the bound 0.39 would hold for m up to
3.57. So if the counted rate is right, the bound survives a clustering of the
successes by that factor. This is a remark and not a proof: the counted rate
rests on M, and nothing here bounds m. Section 10 reports what was measured on
the question.

None of the three heuristics is proved. Section 10 lists the evidence.

## 8. Charged time

One 2-round target compression costs one unit and every other primitive word
operation costs 1/C units with C = 430.

- **Main loop.** For one context and one alpha the 65,536 members take 9,363
  batches: 9,362 full ones and one that holds the last two members and is
  charged in full. A run has 2^88 pairs of a context and an alpha and so
  9,363 * 2^88 batches. Every batch runs stage A, 100 primitive operations by
  6.5, memory loads included. By step 4 at most one eighth of the batches,
  9,363 * 2^85, run stage 2, 138 operations each. The work per alpha before
  the batches is the D0 family and the first half of C0 (below 40
  operations), the seven per-alpha constants of 6.5, each placed in seven
  lanes (12 operations) and stored, and the loads of the context words read:
  below 256 operations. On every run the main loop therefore costs at most
  2^88 times 9,363 * 100 + 9,363 * 138 / 8 + 256 = 1,098,067.75 operations,
  which is less than 16.756 per trial. It is charged 2^88 times 17.4 * 65536
  = 1,140,326.4, that is 17.4 per trial; the difference, 3.8% of the bound,
  is margin. The main loop is charged 2^104 * 17.4 operations. This is the
  budgeted cost, a bound for every run. The expected cost is lower: if a
  trial satisfies rule A with probability 2^-6, at most 7 * 2^-6 = 0.109375
  of the batches run stage 2 on average, and a trial costs at most 16.448
  operations on average.
- **Per context.** Step S1 is below 2^10 operations. Placing the 14 per-context
  constants of the batch in seven lanes and storing them is 14 * 13 = 182 more.
  Together they are below 2^11 operations. There are 2^56 contexts: 2^67
  operations.
- **List.** The list of 6.5 is computed once from eta and Y3: 65,536 members at
  fewer than 64 operations each, 2^22 operations. The three constants of rule A
  are stored.
- **Passes of the E1 test.** At most 2^88 are processed (step 4). The batch
  keeps no values of a passing trial, so the trial is recomputed in scalar form
  from its member number: its words by 6.1, the calls C1 and C2, E1 and E3 for
  both messages, and the comparison of R. That is below 2^10 operations each,
  loads and the count of the processed trials included: 2^98 operations, a
  share below 2^-10.12 of the main loop.
- **Final step.** Steps S2, S3 and two complete hash evaluations with their
  input handling: below 2^11 operations and 2 units, once.
- **Randomness.** One random word, charged as one operation.
- **Preprocessing.** The six constants of 3.2, the word eta of 6.1 and rule A
  are stored in the program. The constants were found by a solver search and
  chosen by the count of Section 10, and rule A was read off counts of the same
  kind. That search, the counts and the measurements of Section 10 used fewer
  than 2^60 primitive operations in total; this figure is the participant's
  estimate from the running times, not a count. As a bound for recomputing a
  valid set of constants that does not depend on that solver, exhaustive search
  over (w4, w13) for the four fixed inputs finds constants with the property of
  Fact P with at most 2^64 candidates at two G evaluations and a comparison
  each, below 128 operations: 2^71 operations, below 2^63 units.

Total:

    T <= (17.4 * 2^104 + 2^98 + 2^67 + 2^60 + 2^22 + 2^11 + 1) / 430
         + 2 + 2^63
       <  17.4 * 2^104 * (1 + 2^-7) / 430 + 2^64
       <  2^99.3841 + 2^64
       <  2^99.39.

Here 17.4 * 2^104 / 430 = 2^(104 + 4.121015 - 8.748193) = 2^99.37282. The terms
after the first add up to less than 2^98.01, which is below 17.4 * 2^104 * 2^-7
= 2^101.121, and log2(1 + 2^-7) < 0.01123. The submitted bound is time_log2 =
99.4, a factor of about 1.01 above this total. This is a worst-case bound for
the algorithm as stated, which halts within its two budgets on every run.

No sorting or lookup is charged because the algorithm has none: a trial is
tested against zero, not against other trials. The only stored list is the
fixed list of class members of 6.5, which is read in order; its loads are among
the 36 of stage A.

## 9. Memory, preprocessing and advice

The program is the step S1 formulas, the trial of 6.1, the packed batch of 6.5
and a compression routine for the final check. Bound the code by 4096
instruction templates of at most four 256-bit words each: 2^14 words, which is
2^19 bytes. Data is the context (48 words), the per-context and per-alpha
constants in packed form (below 32 words), the masks and the fixed constants
(below 32 words), the list of class members (9,363 words), the batch
temporaries (below 64 words) and the two messages and digests of the final
check: fewer than 10,240 words, that is 327,680 bytes. The memory of the search
is therefore below 2^19 + 327,680 < 2^20 bytes. Nothing grows with the number
of trials.

*Memory of the preprocessing.* The computations by which the constants and the
class were selected needed far more memory than the search. The solver search
and the counting programs ran on a desktop machine and stayed below 16 GB of
main memory, 2^34 bytes; the sampling programs and the programs for real
messages stayed below 10 GB of the memory of one graphics card. These two
limits are the participant's observation of the runs, not instrumented peaks.
memory_log2_bytes = 35 covers both at once, 2^34 + 10 * 2^30 < 2^35 bytes, and
with them the search. The cost model does not score memory.

preprocessing_log2 = 63 is the bound of Section 8 for recomputing the six
constants; it also covers their selection and the selection of eta and of rule
A, and it is included in T. nonuniform_advice_log2_bytes = 6 covers the 28
bytes of the six constants and eta and the 12 bytes of the three constants S,
ALL and V of rule A (Lemma A), 40 bytes in all. The list of 6.5 is not advice:
the program computes it from eta and Y3 by Lemma Q. There is no other stored
data and no stored collision.

## 10. Evidence, scope and field meanings

**What is exact.** Sections 2 to 5 and Lemmas Q, F, Y, K, T, E, N and A.
Lemma A says what stage A tests, not that a collision passes it. The
declared experiment `half-collision` runs one trial of 6.1 per organizer
seed, with nine state words, alpha and a member number taken from the seed,
and the organizer recomputes both digests; Lemma T predicts that every trial
agrees on the 128 masked digest bits.

**The seven-word model.** By 6.2 the residual of a trial is a function of the
constants and of seven 32-bit words: for E1 its first-half values d1 and b1 and
its a output a2 on message A, and for E3 the words Y4, Y9, w8 and its
first-half value h1 on message A. (E1's a1 and d1 are the same for A and B, so
a1 enters only through d1 and a2; each of the seven words is a bijective image
of one input or message word of its call when the others are fixed.) In the
algorithm Y4 takes every member of the class equally often. The model M says
that over the trials the other six words behave like independent uniform words,
independent of Y4. Under M a trial has R = 0 with probability r * 2^-128, where
r * 2^80 is the number of solutions of R = 0 among the 2^208 values of the
seven words with Y4 in the class. Call r the *class rate*. Rule A is a
condition on h1, one of the seven words, so under M the trials with R = 0 that
satisfy rule A have a rate of the same kind, r_A, which counts only the
solutions that satisfy rule A; r_A is at most r. H1 is M together with r_A >=
8,388,608.

Given M, the class rate is a property of the constants and the class alone:
the number of solutions of a system of equations in seven words. It can be
counted without sampling, and this section describes the count. The count
says nothing about whether M holds.

**How r is counted (participant computation, not organizer-verified).** Write
tau, eps for the XOR differences between A and B of E1's a and c outputs and
beta for that of its first-half b. As in the proof of Lemma E, E1's d and b
output differences are ROR(tau, 8) and ROR(beta XOR eps, 7), and E3's d and b
output differences are ROR(eta XOR eps', 8) and ROR(psi XOR tau', 7), where
eta, psi are the XOR differences of E3's first-half d and b and tau', eps'
those of its c and a outputs. So R = 0 holds exactly when tau' = tau, eps' =
eps, psi = tau XOR ROR(tau, 1) and eta = eps XOR ROL(beta XOR eps, 1). For Y4
in the class the left side of the last equation is the constant e7c1815f.

1. *The betas.* beta is a function of d1 alone: with c1 = Y11 + d1 and DY11 =
   Y11' - Y11 = 4285247f, beta = ROR(c1 XOR (c1 + DY11), 12). As in Lemma Q,
   the d1 with a given beta are those for which c1 has prescribed bits on the
   mask ROL(beta,12) AND 7fffffff; they are a share 2^-k of all d1, where k is
   the number of bits of the mask. Only finitely many words occur as beta, and
   they can be listed by increasing k.
2. *The outcomes of one beta.* An outcome is a pair (tau, eps). In E1, a2' =
   a2 + delta + (b1' - b1), and b1' - b1 = (b1 XOR beta) - b1 is a signed sum
   over the bits of beta. So tau = a2 XOR a2' is one of the XOR differences
   that an addition can show when its additive difference is delta plus such a
   signed sum. These words are enumerated by a depth-first search over the
   bits of tau, lowest first, with a carry automaton that keeps, for every
   carry, the number of sign choices on the lower bits of beta that lead to
   it; a branch ends when no sign choice is left. No bound is put on the
   weight of tau. For eps, the last equation above says eps XOR ROR(eps, 1) =
   beta XOR ROR(eta, 1). A word has the form eps XOR ROR(eps, 1) exactly when
   its weight is even, and then for exactly two words eps, each the complement
   of the other. So a beta for which beta XOR ROR(eta, 1) has odd weight
   contributes nothing, and every other beta has two candidates for eps.
3. *The E3 side.* For an outcome, N3 is the number of quadruples (Y4, h1, Y9,
   w8) for which E3 produces eta, psi, eps and tau; all of them have Y4 in the
   class. For a word x and a mask m, (x XOR m) - x is the signed sum over the
   bits i of m of (1 - 2 x_i) 2^i, so an addition whose XOR output difference
   is prescribed fixes the bits of its result on that mask once its additive
   input difference is known. E3 has four such additions. Their additive
   differences are the constant Y3' - Y3 and three signed sums (over the bits
   of eta, psi and ROR(eta XOR eps, 8)); the admissible values of those three
   are enumerated with a carry automaton, and for each choice the number of
   completions is a product of two carry automata, one for Y4 against e1 = Y3 +
   Y4 and one for g1 + h2. When the enumeration exceeds a work budget the
   program uses a uniform random subset with the matching weight; it reports
   every outcome for which it did, and such a value is an estimate and not a
   count.
4. *The E1 side.* For an outcome, P1 is the probability that E1 produces tau
   and eps when d1 is uniform among the values with this beta and b1 and a2 are
   uniform. Put nu = ROR(tau, 8), the XOR difference of E1's d output. Two
   additive differences are involved: db = b1' - b1, a signed sum over the bits
   of beta, and dd = d2' - d2, a signed sum over the bits of nu. The first must
   make the addition a2 + (delta + db) show tau, the second must make the
   addition c2 + (DY11 + dd) show eps. For every such pair (db, dd) the bits of
   a2 on tau, of d2 on nu and of c2 on eps are prescribed, and the number of
   pairs (c1, a2) that have them is counted by an automaton over the bits of c1
   with two state bits, the borrow of d1 = c1 - Y11 and the carry of c2 = c1 +
   d2. A triple (c1, b1, a2) determines db and dd, so the counts of the pairs
   (db, dd) are added. When the list of the db or of the dd exceeds a limit the
   program falls back to a product formula that treats the additions as
   independent; it reports every outcome for which it did, and such a value is
   not a count.
5. *The sum.* The class-rate part of a beta is 2^(16 - k) times the sum over
   its outcomes of P1 * N3. Here 16 is the number of bits that Lemma Q fixes,
   so that the class is a share 2^-16 of all Y4. r is the sum of the parts over
   all betas: the sum of N3 over all 2^96 values of (d1, b1, a2) is r * 2^80,
   and 2^96 / 2^80 = 2^16. Parts are not negative, so the sum over any set of
   betas is a lower bound for r.

Steps 1 to 5 use no random number unless one of the two fallbacks of steps
3 and 4 is taken. The arithmetic is double-precision floating point: sums
and products of integers, with a relative rounding error of 2^-53 per
operation once a value exceeds 2^53.

**The count for this package.** The betas were listed by increasing k. The list
given to the calculator holds every beta with k at most 14: 4,272 betas, the
smallest k being 9. A uniform d1 has a beta of the list with probability 0.469;
that is not the share of the class rate that the list holds, which is not
known. For 2,110 betas of the list beta XOR ROR(eta, 1) has odd weight, so that
no eps exists. The other 2,162 were enumerated completely (for three of them,
all without a part, not without sampling: see the second count below), and 39
of them have a nonzero part; these parts add up to 29,977,922. No beta outside
that list was counted, so the count is 29,977,922. What is left out, all betas
with k above 14, makes the figure a lower bound for r. It is about 2^24.84, so
that under M a trial has R = 0 with probability about 2^-103.16, or more, since
the figure is a lower bound.

| beta | k | Outcomes | Exact part | Sampler | Error | Deviation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 481c6852 | 10 | 16 | 14,038,016 | 13,518,848 | 1,321,388 | -0.4 |
| 58146852 | 11 | 10 | 3,956,736 | 4,753,408 | 371,457 | +2.1 |
| 481c5852 | 10 | 10 | 3,596,288 | 3,260,416 | 344,272 | -1.0 |
| 58145852 | 11 | 12 | 2,924,544 | 2,990,080 | 323,233 | +0.2 |
| 481c3852 | 10 | 7 | 2,839,808 | | | |
| 48346852 | 11 | 14 | 715,328 | | | |
| 58143852 | 11 | 10 | 485,248 | | | |
| 48345852 | 11 | 10 | 337,664 | | | |
| f8145852 | 13 | 12 | 322,560 | | | |
| 781c6852 | 12 | 6 | 175,104 | | | |
| 48343852 | 11 | 8 | 145,440 | | | |
| 58745852 | 13 | 16 | 82,560 | | | |
| 78346852 | 13 | 12 | 53,520 | | | |
| f83c5852 | 14 | 12 | 51,840 | | | |
| 781c3852 | 12 | 4 | 43,008 | | | |
| 781c5852 | 12 | 4 | 39,936 | | | |
| f83c6852 | 14 | 8 | 35,200 | | | |
| f83c3852 | 14 | 12 | 26,600 | | | |
| 58746852 | 13 | 5 | 25,344 | | | |
| 78345852 | 13 | 8 | 21,648 | | | |
| f8143852 | 13 | 6 | 14,560 | | | |
| 78343852 | 13 | 10 | 13,320 | | | |
| 481cf852 | 12 | 12 | 11,816 | | | |
| f8342852 | 13 | 8 | 8,448 | | | |
| 58743852 | 13 | 16 | 5,138 | | | |
| 48f45852 | 13 | 4 | 3,712 | | | |
| 48f46852 | 13 | 4 | 2,176 | | | |
| f87c2852 | 14 | 6 | 720 | | | |
| 4834f852 | 13 | 8 | 556 | | | |
| c81c39b3 | 14 | 2 | 384 | | | |
| 48f43852 | 13 | 2 | 288 | | | |
| 787c6852 | 14 | 1 | 128 | | | |
| 787c5852 | 14 | 1 | 128 | | | |
| 787c3852 | 14 | 1 | 64 | | | |
| 5814f852 | 13 | 2 | 40 | | | |
| d81428d3 | 13 | 2 | 16 | | | |
| d81428b3 | 13 | 2 | 14 | | | |
| d8142873 | 13 | 2 | 12 | | | |
| 58fc3852 | 14 | 2 | 10 | | | |
| sum | | 287 | 29,977,922 | | | |

In the table, k is the number of bits that beta fixes in c1, "outcomes" is the
number of outcomes (tau, eps) with P1 * N3 > 0, and "exact part" is the
class-rate part of the beta. The heaviest beta, 481c6852, carries 47% of the
count, and the two heaviest together 60%.

The calculator was run a second time for all 39 betas with a nonzero part and
returned the same parts. Its output states, for every one of them, how many
outcomes went through the random-subset branch of the E3 count and how many E1
counts fell back to a product formula: 0 and 0 in all. Of the 508 outcomes of
these betas that have a nonzero E3 count, 287 have a nonzero E1 count as well;
only these enter the sum.

*The outcomes of the heaviest beta.* The counting program is not part of
this package. So that the largest part of the count can be recomputed
without it, the outcomes of the heaviest beta are written out here.

| tau | eps | N1 | N3 | Adds |
| --- | --- | ---: | ---: | ---: |
| 481c1830 | 2d5730a9 | 2^52 | 2^50 | 4,194,304 |
| 481c2830 | 2d5730a9 | 3 * 2^52 | 2^48 | 3,145,728 |
| 581c1830 | 2d5730a9 | 2^51 | 2^50 | 2,097,152 |
| 581c2830 | 2d5730a9 | 3 * 2^51 | 2^48 | 1,572,864 |
| 481c1850 | 2d5730a9 | 2^53 | 2^47 | 1,048,576 |
| 581c1850 | 2d5730a9 | 2^52 | 2^47 | 524,288 |
| 481c2850 | 2d5730a9 | 2^54 | 2^45 | 524,288 |
| 581c2850 | 2d5730a9 | 2^53 | 2^45 | 262,144 |
| 581c18b0 | 2d5730a9 | 2^50 | 2^48 | 262,144 |
| 481c6830 | 2d5730a9 | 2^51 | 2^46 | 131,072 |
| 581c6830 | 2d5730a9 | 2^50 | 2^46 | 65,536 |
| 581c28b0 | 2d5730a9 | 2^50 | 2^46 | 65,536 |
| 481c6850 | 2d5730a9 | 2^53 | 2^43 | 65,536 |
| 581c6850 | 2d5730a9 | 2^52 | 2^43 | 32,768 |
| 581c68b0 | 2d5730a9 | 3 * 2^49 | 2^44 | 24,576 |
| 581be8b0 | 2d5730a9 | 3 * 2^45 | 7 * 2^45 | 21,504 |
| sum | | | | 14,038,016 |

The table lists the 16 outcomes with a nonzero product of the heaviest beta,
481c6852 (k = 10). N1 is the number of triples (c1, b1, a2), with c1 XOR (c1 +
DY11) = ROL(beta, 12), for which E1 produces tau and eps; it is P1 times 2^86.
N3 is the number of quadruples (Y4, h1, Y9, w8) of step 3. "Adds" is N1 * N3 /
2^80, what the outcome adds to the class-rate part of the beta: 2^(16 - k) *
P1 * N3. Both counts can be recomputed with a model counter from the
definitions of 6.2 and of steps 2 to 4, without the calculator. The calculator
computes in floating point; a value shown as an odd number times a power of
two differs from the computed one by a relative error below 10^-12. The
solution printed below has the outcome tau = 481c2830, eps = 2d5730a9 of this
table.

**Rule A and the count that the claim uses (participant computation).**
Rule A is a condition on h1, one of the four words of the E3 side. So for
an outcome (tau, eps) the number N3 of step 3 splits into the quadruples
whose h1 satisfies rule A and those whose h1 violates it, and under M the
rate of the trials with R = 0 that satisfy rule A is the sum of step 5 with
the first of the two numbers in place of N3. The claim does not use that
sum. It uses a smaller figure: every outcome for which a solver found a
solution that violates rule A is left out in full, with all its solutions.

Which outcomes these are was decided with a SAT solver. For each of the 287
outcomes with a nonzero product P1 * N3, over all betas of the list, the E3
system of step 3 was written as a CNF formula from its definition: the unknowns
Y4, h1, Y9 and w8, E3 for both messages, and the four XOR differences that the
outcome prescribes. The solver kissat was asked two questions. First, whether
the formula has a solution. It has one for all 287 outcomes, and every model,
evaluated again in plain arithmetic, is a solution of its outcome with Y4 in
the class; 270 of these models satisfy rule A. Second, whether the formula has
a solution together with the clause that h1 violates rule A. For 247 outcomes
the answer is that it has none: if these answers are right, every solution of
these outcomes satisfies rule A, and stage A drops none of them. For all 16
outcomes of the heaviest beta, 481c6852, which are written out above with their
two counts, the answer is that no solution violates rule A. So for 47% of the
count the question can be put again to any SAT solver from the definitions of
6.2 and 6.3, without any file of the participant. The 25 betas without a
dropped outcome carry 99.65% of the count. For the other 40 outcomes, in 14
betas, the solver returned a solution that violates rule A, and each was
evaluated again in plain arithmetic. These 40 outcomes carry 12,040 of the
count, 0.0402% of it:

| beta | k | Outcomes | Dropped | Part of the beta | Part dropped |
| --- | ---: | ---: | ---: | ---: | ---: |
| f8342852 | 13 | 8 | 8 | 8,448.0 | 8,448.0 |
| 78346852 | 13 | 12 | 4 | 53,520.0 | 1,296.0 |
| f87c2852 | 14 | 6 | 6 | 720.0 | 720.0 |
| 78343852 | 13 | 10 | 4 | 13,320.0 | 648.0 |
| c81c39b3 | 14 | 2 | 2 | 384.0 | 384.0 |
| 78345852 | 13 | 8 | 2 | 21,648.0 | 144.0 |
| 787c5852 | 14 | 1 | 1 | 128.0 | 128.0 |
| 787c6852 | 14 | 1 | 1 | 128.0 | 128.0 |
| 787c3852 | 14 | 1 | 1 | 64.0 | 64.0 |
| 58743852 | 13 | 16 | 3 | 5,138.0625 | 27.5625 |
| d81428d3 | 13 | 2 | 2 | 16.0 | 16.0 |
| d81428b3 | 13 | 2 | 2 | 14.0 | 14.0 |
| d8142873 | 13 | 2 | 2 | 12.0 | 12.0 |
| 58fc3852 | 14 | 2 | 2 | 10.25 | 10.25 |
| sum | | | 40 | | 12,039.8125 |

The 40 outcomes one by one, so that the questions can be put again; "Adds" is
what the outcome adds to the count, as in the table of the heaviest beta:

| beta | tau | eps | Adds |
| --- | --- | --- | ---: |
| f8342852 | 17d4e830 | f298b0a9 | 4,096.0 |
| f8342852 | 17dce850 | f298b0a9 | 1,024.0 |
| f8342852 | 27dce850 | f298b0a9 | 1,024.0 |
| f8342852 | 17d4e8b0 | f298b0a9 | 512.0 |
| f8342852 | 17dce830 | f298b0a9 | 512.0 |
| f8342852 | 27dce830 | f298b0a9 | 512.0 |
| f8342852 | 37dce850 | f298b0a9 | 512.0 |
| f8342852 | 37dce830 | f298b0a9 | 256.0 |
| 78346852 | a85c18b0 | 0d6730a9 | 768.0 |
| 78346852 | 585c18b0 | 0d6730a9 | 384.0 |
| 78346852 | a85c58b0 | 0d6730a9 | 96.0 |
| 78346852 | 585c58b0 | 0d6730a9 | 48.0 |
| f87c2852 | 17d4e830 | f2e8b0a9 | 256.0 |
| f87c2852 | 27dce830 | f2e8b0a9 | 256.0 |
| f87c2852 | 17dce830 | f2e8b0a9 | 64.0 |
| f87c2852 | 37dce830 | f2e8b0a9 | 64.0 |
| f87c2852 | 57dce830 | f2e8b0a9 | 48.0 |
| f87c2852 | 17d4e8b0 | f2e8b0a9 | 32.0 |
| 78343852 | a85c18b0 | 0d6750a9 | 384.0 |
| 78343852 | 585c18b0 | 0d6750a9 | 192.0 |
| 78343852 | a85c58b0 | 0d6750a9 | 48.0 |
| 78343852 | 585c58b0 | 0d6750a9 | 24.0 |
| c81c39b3 | 481437b1 | 2d5751e8 | 256.0 |
| c81c39b3 | 481c37b1 | 2d5751e8 | 128.0 |
| 78345852 | a85c58b0 | 0d6710a9 | 96.0 |
| 78345852 | 585c58b0 | 0d6710a9 | 48.0 |
| 787c5852 | a85c58b0 | 0d1710a9 | 128.0 |
| 787c6852 | a85c58b0 | 0d1730a9 | 128.0 |
| 787c3852 | a85c58b0 | 0d1750a9 | 64.0 |
| 58743852 | a8ac6830 | 32e750a9 | 17.5 |
| 58743852 | a8ac5830 | 32e750a9 | 8.75 |
| 58743852 | a8acd830 | 32e750a9 | 1.3125 |
| d81428d3 | 582c27b1 | 32a74fa8 | 8.0 |
| d81428d3 | 586c27b1 | 32a74fa8 | 8.0 |
| d81428b3 | 582c27b1 | 32a74fe8 | 7.0 |
| d81428b3 | 586c27b1 | 32a74fe8 | 7.0 |
| d8142873 | 582c27b1 | 32a74f68 | 6.0 |
| d8142873 | 586c27b1 | 32a74f68 | 6.0 |
| 58fc3852 | a8ac5830 | 321750a9 | 8.0 |
| 58fc3852 | a8acd830 | 321750a9 | 2.25 |
| sum | | | 12,039.8125 |

The figures of these two tables are printed in full, except the part of beta
78346852, whose value from the printed factors differs from 53,520 by the
calculator's floating-point rounding (about 10^-10) and is rounded to one
decimal. The largest of them is the outcome tau = 17d4e830, eps = f298b0a9 of
beta f8342852, with 4,096.0. Without these outcomes the count is

    29,977,922 - 12,040 = 29,965,882.

This is the figure that H1 is set against. Under M it is a lower bound for the
rate of the trials with R = 0 that satisfy rule A, provided that the 247
answers "no solution" are right. The answers reported so far are those of
kissat in one run. The same 287 pairs of questions were then put to two other
solvers, cadical and cryptominisat5, with a CNF formula of another making. A
reviewing helper agent wrote it from 6.2 alone: its unknown is Y14 where the
first formula has h1, it prescribes the differences of h1 and of the four
outputs of E3 where the first prescribes those of e1, g1, e2 and g2, and its
clauses for the additions are its own. It was run again for this text. Each of
these solvers gives the answer of kissat for every outcome: a solution for all
287, no violating solution for 247 and one for 40, and every model was
evaluated again in plain arithmetic. So three solvers and two formulas agree.
No proof certificate was kept or checked for any of them, and both formulas
were written by instances of the same AI model. The figure is 0.999598 of the
count of all solutions.

For this package the 39 betas with a nonzero part were counted once more with
the compiled calculator in its present form, which was run and not built again:
it returns the same 39 parts, 29,977,922 in all, no outcome through either
fallback, and the same 287 outcomes with a nonzero product. The products P1 *
N3 of the single outcomes are taken from the recount that prints both factors
in full; their logarithms agree with the two decimals that the calculator
prints for every outcome. The whole list was also counted once more with that
binary, all 4,272 betas: the same betas have no eps, the same 39 have a part,
every part is the same, and the sum is 29,977,922. For three betas of the list,
c81cd8b3, f81c2873 and f81c28b3, all without a part, that run reports what the
per-beta file of the first count does not record: the E3 count of seven
outcomes went through the random-subset branch, so these values are estimates.
The 69 outcomes of these betas with a nonzero E3 value all have an exact E1
count of zero, so their product is zero whatever N3 is. An outcome whose E3
value that branch estimated as zero would be missing from the sum; that can
only make the figure smaller. So for these betas the E3 side was not counted
without sampling.

How much of the rate rule A really keeps was counted for a shorter list. The
thread that found the rule split the E3 count of every outcome by the bits of
h1, with a program of its own, for the 242 outcomes of the 30 betas with a part
among the 1,500 lightest betas, whose parts add up to 29,862,848: rule A keeps
0.999839 of that sum. The figure that the claim uses keeps less, because it
gives up in full every outcome for which a violating solution was found. Rule A
was read from the outcomes of these 30 betas. Of their 242 outcomes 27 have a
violating solution, and these carry 10,606 of 29,862,848, 0.036%. The longer
list of this package adds nine betas with a part, all with k = 14, with 115,074
together. Of their 45 outcomes 13 have a violating solution, and these carry
1,434, 1.25% of what these betas add: a share about 35 times as large, and six
of the nine betas are left out in full. So the betas that the rule was not read
from comply with it less, and the betas with k above 14, which are not counted,
may violate it more often still. This does not change the figure that the claim
uses: it leaves all these outcomes out, and no uncounted beta is in it. The
same question had been put to the solver before, by the thread that found the
rule, for the 242 outcomes of that shorter list: its answers, 215 without and
27 with a violating solution, are the same as those above for every one of
these outcomes. That thread also compared the E3 count N3 with the approximate
model counter ApproxMC (tolerance 0.4, confidence 0.9) on the CNF of the same
E3 system, for the 30 outcomes with the largest products of its list, which
carry 0.8866 of its sum: the mean of log2(N3 / ApproxMC) is -0.002 and the
largest difference 0.10 bits.

A complete solution of the seven-word system with Y4 in the class that violates
rule A, which can be checked by hand from 6.2: Y1 = 052ce267, Y6 = fad31d99,
Y12 = 69da227b, w12 = 00000000, w5 = 57d7dfef, Y4 = c0d07bf1, Y9 = fcde77b6,
Y14 = a48cb1ee, w15 = 0, w8 = 5141ce8c. For these values the four residual
words of 6.2 are zero, and h1 = d87fa4af does not satisfy rule A: "bits 23 and
24 differ" fails. Its outcome is tau = 17d4e830, eps = f298b0a9 with beta =
f8342852, one of the outcomes that the count leaves out. The E3 values are the
solver's model for that outcome and the E1 values come from a second solver
call. It shows that a collision need not satisfy rule A; it does not show that
a message reaches such values.

*The sampler as a check.* The last three columns of the first table come from
the sampler of submission 04638ed8, which is used here as a check and not for
the figure. For one beta it draws d1 among the values with that beta and b1, a2
uniformly, keeps the draws that require the class, and counts E3 for each kept
draw with the count of step 3. Four betas of the table were given 16 runs of
2^34 draws each. The runs of every beta, and of every class, use the same
seeds, 8301 to 8316, so the figures of different betas are not independent of
each other. "Sampler" is the mean of the class-rate parts of the runs, "error"
is the standard deviation of the runs divided by the square root of their
number, and "deviation" is the difference from the exact part in units of that
error. For these four betas together the sampler gives 24,522,752 with standard
error 1,451,568 against 24,515,584 counted; the single betas lie between -1.0
and +2.1 standard errors. That the sums agree so closely is a cancellation: the
four differences are -0.52, +0.80, -0.34 and +0.07 million. Taken over the 16
seeds, the error of the sum is 1,501,693 where the single errors combine to
1,451,568. That figure is a reviewing helper agent's; the helper agents named
in this section are further instances of the AI model that wrote this package,
which the submission note names. The deviation of +2.1 for beta 58146852 is not
explained. A reviewing helper agent compared the sampler's draws per outcome
with the calculator's P1: for this beta the chi-square statistic is 29.1 on 10
degrees of freedom, for the other three 9.8 on 12, 3.3 on 6 and 11.1 on 10; its
own Monte Carlo of the same probabilities agrees with the calculator. So the
excess is on the sampler's side, and its cause was not found. The sampler runs
are short because the sampler fails when a run is long and the rate is as high
as here (its output buffer overflows).

*The other classes, and why this one is used.* A solver search with the
constants held fixed, which asks for a solution with a pair (eta, beta) not
seen before, returned 40 pairs in 33 different classes. An exact grid over
2,847 classes within Hamming distance 6 of the first two, restricted to the 522
betas with k at most 12, was stopped before it had finished; the classes that
its partial output showed as strong were counted in full as well. This
exploration was closed before the text was finished, so the figures that follow
are its final state. In all, 34 classes of these constants have a count over
one common list, the 1,500 lightest betas:

| eta | Members | Betas with a part | Count |
| --- | ---: | ---: | ---: |
| e74181df | 65,536 | 13 | 36,249,523 |
| e7c1815f | 65,536 | 30 | 29,862,848 |
| 2fc1815f | 131,072 | 12 | 26,021,728 |
| 27c1815f | 262,144 | 19 | 25,204,132 |
| e741815f | 131,072 | 14 | 24,530,100 |
| 67c181df | 65,536 | 13 | 23,766,776 |
| 27c182df | 131,072 | 45 | 16,494,326 |
| e741835e | 131,072 | 24 | 12,982,696 |
| 67c182df | 65,536 | 61 | 9,158,758 |
| 25c1815f | 524,288 | 6 | 8,855,552 |

The table shows the ten largest. The other 24 classes have counts from
6,045,516 down to 0; four of them have no part at all. The common list is not
even-handed between classes. It leaves out 153 betas with k = 13. For a class
whose eta has odd weight, as for the class of this package and for e74181df,
none of these betas has an eps, so the list is complete for it up to k = 13;
for a class whose eta has even weight every one of them has an eps, and its
count could still rise (2fc1815f, e741815f, 27c182df, e741835e and 25c1815f
among the classes shown). The nearest of these, 2fc1815f, would need 15% more
to pass the class used; that was not counted. The claim does not depend on the
rank.

The class of this package is the second largest of them, with 29,862,848 over
that list. The largest, eta = e74181df, a class of 65,536 members, has
36,249,523, and 36,358,944 over all 4,272 betas with k at most 14. It is not
used here, and the reason is not its evidence: this text, the run that counts
partial E3 events and the reviews were made for the class of the package,
before the checks of e74181df existed. For e74181df there are the count; the
sampler on four of its betas, with 15,891,456 +- 809,041 against 16,515,072
counted (beta 581c6872), 11,107,795 +- 764,310 against 11,214,208 counted
(581c3872), 2,591,744 +- 135,637 against 2,875,392 counted (581c5872) and
2,138,112 +- 156,922 against 2,334,720 counted (58346872), that is between -2.1
and -0.1 standard errors; its E1 count against ApproxMC for beta 581c6872 (24
outcomes, largest difference 0.00 bits) and its E3 count against a SAT solver
and ApproxMC (ratio of sums 1.017 for the 30 largest counts, 1.000 for 40
others; 40 zero counts tested, none with a solution); and on real messages the
host check of the trial (16,384 of 16,384 trials), a comparison of 2^40 real
trials with M (early test passes 11,928 against 11,880, trials in which E1
requires the class 1,443 against 1,411, largest deviation 1.8 standard
deviations), a second comparison of 2^42 real trials with M (early test passes
47,912 against 47,472, trials in which E1 requires the class 5,613 against
5,550, largest deviation 2.4 standard deviations), eight runs in the layout of
the algorithm, with the same sets of seed words as the runs of the class of
this package, with 12,124, 11,961, 12,033, 12,014, 11,959, 11,799, 12,018 and
11,931 early-test passes (ratio of their variance to their mean 0.74,
chi-square 5.2 on 7 degrees of freedom, no excess) and a run of 2^44 real
trials that counts its heavy E1 outcomes (40 seen where the expectation file of
that run has 37.52, +0.4 standard deviations; trials with one of its listed
betas -0.8). It lacks a run that counts partial E3 events on real messages,
which the class of the package has. So the other class has the larger count and
nearly the same checks. With a batch of one stage the claim would be the same
for both classes. Rule A and the two-stage batch of this package were worked
out, counted and checked for the class of the package only, and that is a
second reason why the other class is not used. For e74181df the thread that
found rule A reports, from the same split of the E3 counts by the bits of h1,
five conditions that keep 1.000000 of the counted rate of its list, to six
decimals. Two of them hold for every counted solution; the other three are
violated by counted solutions, which carry less than 0.000001 of the rate. The
best further condition that it found keeps 0.973 of the rate. With five
conditions a trial passes with probability 2^-5, so that more batches would run
stage 2 than here; no batch was written or counted for that class, and no claim
is derived for it. The two counts are 3.57 and 4.33 times the assumed 2^23
(rounded down; for the class of the package this is the count of all solutions,
before rule A); against the next power of two, 2^24, they would leave factors
of only 1.78 and 2.16. The sampler was also run for eta = e741835e on four
betas (13,225,404 with standard error 1,039,270 against 11,482,432 counted;
single betas between +0.8 and +2.4 standard errors) and eta = e5c1815f on seven
betas (5,627,648 with standard error 225,130 against 5,799,040 counted; single
betas between -1.6 and +0.3 standard errors).

**Checks of the calculator (participant computations).** The E3 count of step 3
is the program of submission 04638ed8; the checks reported there were made with
other constants: a SAT solver and the approximate model counter ApproxMC on 30
outcomes, brute force with 8-bit words on 400 constant sets, and further checks
against ApproxMC on 440 outcomes with ratios of sums between 0.969 and 1.050.
The enumeration of outcomes of step 2 and the E1 count of step 4 are new code,
written in the night before this text. Five checks were made of the calculator
as it is used here.

First, the calculator against the sampler on other constants, where the sampler
figures are those of the earlier submissions or of the night's runs: for the
constants of submission 04638ed8, class e96d6d6b, beta 953908d0, 6,164.7
against 6,168 with standard error 810 (third pass) and 6,218 with standard
error 772 (second pass); for the same class, beta 953f08d0, 945.7 against 1,140
with standard error 104 (third pass) and 949 with standard error 95 (second
pass); here 7 of the calculator's outcomes went through the random-subset
branch of the E3 count; for the same constants, class e96d7579, beta 953908d0,
2,549.9 against 2,489 with standard error 147 (third pass) and 2,546 with
standard error 149 (second pass); for another pin of the same solver search
(eta 31b13fea, beta c93210a5), 106,520 against 119,740 with standard error
7,338 (seed 8101) and 91,882 with standard error 6,147 (seed 8102). The 8
sampler figures are between 0.0 and 2.4 standard errors from the calculator's.
In the last case the two sampler runs differ from each other by 2.9 of their
combined standard errors, and the calculator's figure lies between them.

Second, the exact E1 count against brute force with 8-bit words: for 40 random
cases, all 55,447 outcomes that have solutions were compared and 55,447 are
equal; of the outcomes without solutions, 40,134 were sampled and 40,134 are
zero in the calculator as well.

Third, the exact E1 count at 32 bits against ApproxMC, for these constants, the
class of this package and beta 481c6852: the E1 system of an outcome was
written as CNF straight from its definition and its solutions were counted. For
16 outcomes with a nonzero count the mean of log2(calculator / ApproxMC) is
-0.001 and the largest difference is 0.00 bits; for the one outcome that the
calculator counts as zero, ApproxMC finds no solution either. These are all
outcomes of that beta with a nonzero E3 count.

Fourth, the E3 count for these constants and the class of this package. The
sampler runs of the betas 481c6852, 58146852, 481c5852 and 58145852 produced
120 different outcomes, 47 with a nonzero E3 count and 73 with zero, none of
them counted through the random-subset branch. They were given to a SAT solver
and to the approximate model counter ApproxMC (tolerance 0.4, confidence 0.9)
with the checking program of the earlier submissions. For the 30 largest counts
the sum of the counter's values is 0.994 times the sum of the independent
counts, with log2 differences between -0.10 and +0.07; for the other 17 the
ratio is 0.999, with log2 differences between -0.11 and +0.13. Of the 73 zero
counts, 40 drawn at random were tested and none has a solution.

Fifth, the enumeration of step 2 was run without any limit on the weight of tau
for every beta of the table: the program's limit was set to 31, the largest
possible weight below bit 31. For the heaviest beta, 481c6852, it finds 17
outcomes with a nonzero E3 count, of which 16 have a nonzero product.

What these checks cover: the E1 count against brute force only for 8-bit words
and against an independent counter for one beta at 32 bits; the E3 count
against an independent counter for the outcomes of four betas; and the whole
calculation against the sampler for the betas of the table that were sampled,
which carry 82% of the count, to within the sampler's errors. The sampler
shares the E3 count with the calculator, so that comparison tests the
enumeration of outcomes and the E1 count, not the E3 count. All of these are
participant computations.

**Checks by reviewing helper agents (participant computations).** Three helper
agents, further instances of the AI model that wrote this package, reviewed an
earlier version of it, which had the same constants, the same class and the
same count and a batch of one stage, and wrote programs of their own from the
text of that proof. They are not independent parties, and what follows is
quoted from their reports. Rule A, the two-stage batch and the count with rule
A did not exist then and were not in front of them. One compared the whole
calculation at 8-bit words, that is the enumeration of outcomes, the E1 count,
the E3 count, the weights and the sum over betas, with a brute force of the
seven-word system written from 6.2 alone: 60 random constant sets, 1,019
classes, 17,258 pairs of a class and a beta, 874 of them with solutions,
694,652,928 solutions in all; no pair differs, and the 8,632 pairs without an
eps are all empty. The same agent repeated the brute-force check of the E1
count at 8 bits with another seed (60 cases, 85,908 outcomes with solutions all
equal, 60,448 sampled outcomes without solutions all zero) and made a Monte
Carlo of the E1 probabilities at 32 bits for the four sampled betas with no
code of the project: for their 48 outcomes with a nonzero product the
chi-square statistics are 12.6 on 16, 10.6 on 10, 8.3 on 10 and 16.7 on 12
degrees of freedom, and the sums of P1 * N3 are 0.980, 0.990, 1.005 and 1.012
of the calculator's. The second agent made a Monte Carlo of E1 for the heaviest
beta with 2^39 draws, 587 hits on its 16 outcomes against 628.2 predicted
(628.75 by the counts N1 of the table above; the report worked from logarithms
kept to two decimals) and none on the outcome that the calculator counts as
zero, and a Monte Carlo of the E3 count for the four heaviest outcomes with
2^36 draws each: log2 N3 = 50.06 +- 0.06, 48.14 +- 0.12, 49.95 +- 0.09 and
48.04 +- 0.18 against 50, 48, 50 and 48. It also found the solution inside the
class that is printed below. The third agent compared the whole calculation
with a brute force of its own at 8-bit words, for 10 random cases, half of them
with delta = -2, and 182 classes: all 125 pairs of a class and a beta with
solutions are equal, and all 46,467 pairs without solutions are zero. With a
Monte Carlo of its own at 32 bits it found, for the heaviest beta, the E1
probabilities of all 16 outcomes within 0.14 bits of the calculator's, and the
E3 counts of the six largest outcomes at 2^50.05, 2^47.88, 2^50.01, 2^47.92,
2^46.89 and 2^45.08 against 2^50, 2^48, 2^50, 2^48, 2^47 and 2^45; for these
six outcomes together it gives 12.20 million with standard error 0.44 million
against 12.58 million counted. Two of the agents report that the calculator
returns the same outcomes and parts for the heavy betas when delta = +2 is put
in place of -2. So the count does not check the sign of delta; that is checked
by the hash tests of the trial, not by the count.

Three further helper agents, again instances of the same AI model and not
independent parties, reviewed the version of this package before the present
one, which already had rule A, the two-stage batch and the count with rule A.
Three programs of theirs are reported in this section, each where its subject
is treated and named there as a reviewing helper agent's: a second CNF formula
for the questions on rule A, the count of rule A and of the batches that run
stage 2 in the layout of 6.4, and the same over many sets of seed words. Each
of them was run again for this text, and the figures printed are those of the
second runs. A further helper agent, also an instance of the same AI model and
not an independent party, then checked the changes made after their findings
against the files and ran the three programs once more, with the same output;
what was changed after that check has not been reviewed.

A complete solution of the seven-word system with Y4 in the class, which can be
checked by hand from 6.2: Y1 = 00000000, Y6 = 7e1401e5, Y12 = 5a538ab4, w12 =
00000000, w5 = 234e3245, Y4 = 0ad073e5, Y9 = 61e4852d, Y14 = ddcc82f4, w15 = 0,
w8 = a2ee086c. For these values the four residual words of 6.2 are zero. E1 has
beta = 481c6852, and the XOR differences of its a and c outputs are tau =
481c2830 and eps = 2d5730a9: one of the outcomes of the table above. The
solution was found by a reviewing helper agent with a short search of its own
and was evaluated again for this text with the G function alone. It shows that
the constants and the class do not exclude R = 0; it does not show that a
message reaches such values. The solution that the solver search returned with
the constants has eta = e5c1815f and so lies in another class. For the solution
printed here h1 = e37197ef, which satisfies rule A.

**How the constants and the class were found.** The constants come from a
solver search, not from farming random sets. One CNF instance holds, with real
word values: the call C3 for both messages with equal b and d outputs, so that
every model is a set of constants with the property of Fact P; E1 and E3 for
both messages; a zero residual; and a bound on the number of bit positions, bit
31 excepted, at which a difference is active in six additions of E1 and E3. The
solver is kissat. When its log was read for this text it held 21 sets of
constants found in this way, in runs of up to 118 minutes each, several at a
time on a desktop machine; the search for further sets was still running. The
constants of 3.2 came from an instance with bound 108, after 2,149 seconds,
with 106 active positions; the solver's solution has eta = e5c1815f and beta =
f8345852. For 17 of these sets, the class of the solver's solution was counted
over its 150 lightest betas. The constants of 3.2 had the largest count,
5,072,896; the largest of the others was 2,925,288 and their median 9,618. The
class of this package is not the class of that solution; its eta differs from
that of the solver's solution in one bit. It is one of the classes of the table
above, where the choice among them is described. The bound steers the search
towards solutions that are reached with high probability under M; the count,
not the bound, is what H1 is set against.

**Checks of the trial on real messages (participant computation).** A host
program built the messages of 16,384 random trials of 6.1 with these constants
and this class, and evaluated the complete 2-round hash of both messages of
every trial: all agree on digest words 0, 2, 5 and 7, have Y4 in the class and
the pinned words in place, and have the residual that 6.2 computes. A second
program, written independently from the text of this proof, checked each of
Lemmas Q, F, Y, K, T, N and A on 20,000 random trials with these constants and
this class against a plain forward compression, and evaluated the two solutions
that this section prints.

**Checks of the model on real messages (participant measurement).** Real
trials of 6.1 were compared with the same number of draws from M (Y4 a
uniform member of the class, the other six words uniform and independent),
on the same statistics: how often each of the four residual words, or its
low 16 bits, is zero, how many trials have a residual of weight at most 32
or at most 40, how often the early test of Lemma E passes, and in how many
trials E1 requires the class. The last of these is the event
eps XOR ROL(beta XOR eps, 1) = eta, so a trial in which E1 requires the
class is a trial that passes the E1 test of Lemma N. The algorithm of this
package uses the E1 test and not the early test; both are reported because
the programs print both.

In these comparisons the real trials are not laid out as in 6.4. Every
thread of the generating program draws its own context, nine random state
words from a random stream of its own, independent of the other threads,
and makes 4,096 trials in it, each with a random alpha and a random member
of the class. No two contexts share seed words, and X12 and X13 are not
restricted. These comparisons therefore measure rates averaged over
independent contexts. They do not test a run of 6.4, in which all contexts
share the four seed words.

For the constants and the class of this package, with 2^40 trials of each kind
(real messages / model): early test passes 11,418 / 11,249; trials in which E1
requires the class 1,521 / 1,442; the four residual words zero 238, 2,415, 181,
362 / 216, 2,355, 191, 341; residual of weight at most 32: 105,429 / 104,997;
of weight at most 40: 65,224,561 / 65,205,546; all four residual words with a
zero low byte: 1,007 / 981. Among all the statistics that the two programs
print with at least 30 events, the largest deviation is 2.5 standard
deviations, the model higher (the low 16 bits of the first residual word zero:
13,183,827 / 13,196,581). The second residual word is zero about 9 times as
often as a uniform word would be (256 expected), on real messages and in the
model alike. 24 statistics were compared; 2 of them deviate by 2.0 standard
deviations or more. A standard deviation here is the square root of the sum of
the two counts.

A second comparison, with 2^42 trials of each kind (real messages / model):
early test passes 45,141 / 45,349; trials in which E1 requires the class 5,877
/ 6,035; the four residual words zero 920, 9,509, 719, 1,500 / 873, 9,468, 767,
1,445; residual of weight at most 32: 420,201 / 420,583; of weight at most 40:
260,866,716 / 260,864,998; all four residual words with a zero low byte: 3,889
/ 4,077. Among all the statistics that the two programs print with at least 30
events, the largest deviation is 2.1 standard deviations, the model higher (all
four residual words with a zero low byte: 3,889 / 4,077). The second residual
word is zero about 9 times as often as a uniform word would be (1,024
expected), on real messages and in the model alike. 24 statistics were
compared; 1 of them deviates by 2.0 standard deviations or more.

A further measurement goes deeper on the E1 side. It counts, among real trials
of 6.1 with independent contexts, those whose E1 outcome (beta, tau, eps) is
one of the 69 outcomes with a nonzero product of the six heaviest betas of the
table. The calculator's P1 gives these a probability of 2^-38.57 per trial. Two
runs of 2^44 real trials each, with different random words, are on file. In
each 43.16 such trials are expected (from the counts N1 of the recount; the
expectation file written before the runs has 43.12, from logarithms kept to two
decimals); they found 42 and 59, that is -0.2 and +2.4 standard deviations of a
Poisson count. Together that is 101 in 2^45 trials against 86.32 expected, +1.6
standard deviations. The beta of a trial was one of the six in 77,308,903,893
and 77,309,005,969 trials against 77,309,411,328 expected per run, -1.8 and
-1.5 standard deviations, and together -2.3: a shortfall of about 6 in a
million that is not explained. The same counter on 2^42 draws from M found 10
listed outcomes where 10.79 are expected, and a beta of the list in
19,327,357,609 draws against 19,327,352,832 expected: a check of the counter
and of the expectation, not of real messages. This tests the E1 probabilities
of the count on real messages at that depth. It does not test the two sides
together.

The second of these runs also counts an event on the E3 side. For an outcome
(tau, eps), the E3 count of step 3 puts three conditions on the inputs of E3:
the XOR difference of its first-half b value is psi = tau XOR ROR(tau, 1), that
of its a output is eps, and that of its c output is tau. A partial E3 event is
the first two of the three, for one of the 69 pairs (psi, eps) that belong to
the listed outcomes of the heaviest betas above. Both differences can be read
off the outputs of E3. The third condition is left out, because with it the
event is too rare to be counted. The probability of a partial event under M
comes from a program derived from the E3 count: the same enumeration and
automata, without the list for the third condition. At 8-bit words that program
was compared with brute force on 30 cases: 87,242 outcomes with solutions, all
equal, and 59,183 sampled outcomes without solutions, all empty in the program
as well. The 69 events have a probability of 2^-34.54 per trial together,
between 2^-44.0 and 2^-38.0 each. In 2^44 real trials 706.0 are expected and
721 were seen, +0.6 standard deviations of a Poisson count. The same counter on
2^42 draws from M found 161, where 176.5 are expected (-1.2 standard
deviations): a check of the counter and of the expectation, not of real
messages. So the E3 side is now tested on real messages as well, at these
depths, but without its third condition. Nothing tests the full E3 count on
real messages, and nothing tests E1 and E3 together.

A second measurement uses the layout of the algorithm, for the constants and
the class of this package: eight runs of 2^40 real trials of 6.1. Each run has
its own four seed words X2, X5, X6 and X9, shared by all its contexts. A
context is one thread of the program: a random (X12, X13, X14) with X12 < 2^8,
and 4,096 trials, each with a random alpha and a random member of the class.
Two things differ from 6.4: X13 is not restricted, and the program leaves the
context word X10 random in every thread where step 1 sets it to zero, so that
S5, which the algorithm holds fixed over a run, changes from context to
context. Early-test passes: 11,382, 11,211, 11,200, 11,098, 11,621, 11,308,
11,148 and 11,098, in all 90,066. The run with independent contexts gave 11,418
in the same number of trials; the mean of the runs, 11,258.2, is 1.4 standard
deviations below it. The ratio of the variance of the eight pass counts to
their mean is 2.8, where independent trials give 1 on average; the chi-square
statistic against a common mean is 19.4 on 7 degrees of freedom, which chance
exceeds with probability about 0.007. Run 5 is 3.7 standard deviations above
the mean of the other seven. So the number of early-test passes of a run
differs between runs by more than chance: it depends on the seed words of the
run, by about 1.3% of its value. The cause was not found. E1 required the class
of the trial's Y4 in 1,462, 1,494, 1,486, 1,472, 1,432, 1,468, 1,471 and 1,527
trials, against 1,521 with independent contexts. For these counts the
chi-square statistic is 3.6 on 7 degrees of freedom, no excess. These runs
record these two counts and nothing else; in particular no residual words and
no pair statistics.

What this means for the three heuristics. The count that differs between runs
is that of the early test of Lemma E, which the algorithm of this package does
not use. H2 is about the E1 test of Lemma N. Its passes are the trials in which
E1 requires the class; their counts in these runs show no such spread, and the
budget of H2 is 2^13.47 above their mean. H3 is about rule A, which these runs
did not record; four other runs in the same layout did, and each has a share of
trials that satisfy rule A within 1.3e-05 of 2^-6, relatively (reported below).
For H1 it is a warning. H1 treats the trials of a run as independent with
respect to its event, and here another event of the same trials, at a depth of
about 2^-26.52, is seen to depend on the seed words that all trials of a run
share. The number of trials in which E1 requires the class, an event that R = 0
needs, shows no such dependence at a depth of about 2^-29.5, but that is far
from the depth of R = 0. Four things bear on the question; none settles it for
32-bit words. First, averaged over independent contexts the pass rate agrees
with M: 45,141 passes against 45,349 in 2^42 trials of each kind (above), that
is 11,285 against 11,337 per 2^40 trials, and the mean of the eight layout runs
is 11,258; it is the spread between runs that M does not give. Second, the
scaled-down runs in the layout of the algorithm reported below count collisions
per run, at word sizes of 8 to 10 bits and with other constants: 7,072 of
18,080 runs had a collision where independent trials predict 7,113.9. Third,
eight runs of the class eta = e74181df of the same constants, made with the
same eight sets of seed words, show no excess: the ratio of the variance of
their pass counts to their mean is 0.74 (chi-square 5.2 on 7 degrees of
freedom), and the run with the seed words of run 5 is 0.2 standard deviations
below the mean of the others there. So those seed words do not give a high pass
count for every class. Fourth, the remark at the end of Section 7: under M the
count gives 1.78 expected trials with R = 0 and rule A per run, so the bound
0.39 would survive a clustering of them by a factor of up to 3.57.

**Rule A and the E1 test on real trials (participant measurement).** The runs
above did not record rule A. The thread that found the rule ran real trials of
6.1 for these constants and this class with a program of the same kind that
also counts rule A, in the layout of the runs above: every run has its own four
seed words, shared by all its contexts, X12 is below 2^8, and the two
differences from 6.4 named above apply. Four runs of 2^38 trials counted
4,294,916,967, 4,294,925,479, 4,295,022,265 and 4,294,920,099 trials that
satisfy rule A, where a share of 2^-6 is 4,294,967,296: they are -0.8, -0.6,
+0.8 and -0.7 standard deviations of a binomial count away from it, and no run
differs from it by more than 1.3e-05 of its value. Together 17,179,784,810 of
2^40 trials satisfy rule A, a share of 2^-6.0000 (-0.6 standard deviations from
2^-6). A batch runs stage 2 only if one of its seven trials satisfies rule A,
so at most seven times this share of the batches do, 0.10938, against the
budget of 0.125 in step 4. In the same runs 1,390 trials passed the E1 test, a
share of 2^-29.56, and 11,407 the early test of Lemma E. These runs have no
model run beside them; they give pass rates and nothing about M. The self-test
of the program reports the same share of lanes on its own, much smaller, sample
(6.5).

The layout of 6.4 itself was measured on a CPU, with a program that a reviewing
helper agent wrote from Sections 4 and 6 and that was run again for this text.
It computes the word z of Lemma A for every trial in scalar arithmetic. On
20,000 random trials its z and its verdict on rule A are those of the complete
compression of the real message A, whose digest is that of the organizer's
reference hash. A sample has four seed words of its own and X1 = X10 = 0 as in
step 1, 1,024 contexts drawn at random with X12 below 2^8 and X13 below 2^16,
16 random values of alpha for each of them, and for every pair of a context and
an alpha all 65,536 members of the class in the order of their numbers, seven
to a batch: 2^30 trials in 153,403,392 batches. So contexts and values of alpha
are sampled, and every class loop is complete. In 24 samples the share of
trials that satisfy rule A lies between 0.999565 and 1.000452 times 2^-6, and
is 1.000029 times that over all of them; the chi-square of the 24 counts
against 2^-6 is 18.7 on 24 degrees of freedom. The share of batches that run
stage 2 lies between 0.103535 and 0.104059 and is 0.103873 over all samples;
the budget of 0.125 is 1.201 times the largest. In every sample it is below 1 -
(1 - 2^-6)^7 = 0.104379, the value for seven independent trials: trials of one
batch tend to satisfy rule A together, which lowers the number of batches. The
24 batch counts differ from each other by more than binomial counts with a
common share would (chi-square 1,073 on 23 degrees of freedom); the largest
exceeds the smallest by 0.50% of the common share. So this count depends on the
sample, that is on the seed words or on the contexts drawn; the cause was not
examined.

A second program of a reviewing helper agent, also run again for this text,
takes many sets of seed words and, for each, a random sample of the batches of
the run that 6.4 defines for it: X1 = X10 = 0, X12 below 2^8, X13 below 2^16,
and a context, a value of alpha and a position in the class drawn at random for
every batch. It computes h1 for the seven trials of a batch; for 33,504 trials
its h1 was compared with that of the complete compression of the real message,
and none differs. For 8,192 sets of seed words with 2^15 batches each,
1,878,904,437 trials in all, the share of trials that satisfy rule A is
2^-5.9996 (+1.4 standard deviations of a binomial count from 2^-6). Per set it
lies between 0.9308 and 1.0746 times 2^-6, where one binomial standard
deviation of a set is 0.0166 and H3 needs less than 1.1429; the chi-square of
the sets against 2^-6 is 8,358.7 on 8,192 degrees of freedom. The share of
batches that run stage 2 is 0.10383 over all sets and between 0.09720 and
0.11115 per set (chi-square against the common share 8,391.6 on 8,191); no set
reaches the budget of 0.125. A set here is a sample of 2^15 batches of a run,
not a run.

The same comparisons were made earlier for the constants of submission 04638ed8
and are reported there. For its class the largest deviation with independent
contexts was 1.5 standard deviations. Two other classes of those constants and
the search that does not restrict Y4 showed 2.6, 2.7 and, in two runs of the
unrestricted search with opposite signs, 3.1: a spread between runs that is
larger than a Poisson count allows and that was not explained. Those figures
belong to other constants. They are repeated here because they bear on M and on
these programs in general.

The comparisons with M concern events of probability about 2^-32 and above. The
counts of E1 outcomes concern an event of probability 2^-38.57 per trial, all
listed outcomes together, for E1 alone; the count of partial E3 events concerns
one of 2^-34.54, with single events from 2^-38 to 2^-44, for E3 alone and
without its third condition. None of them reaches the event R = 0, and none
joins the two calls.

**Scaled-down end-to-end check of the class search (participant
computation, other constants).** With short words the whole search can be
run and its collisions counted. These runs were made before the constants
of this package were found. They use constant sets of their own with 8-bit
and 10-bit words, none of which is derived from the constants of 3.2, and
the rate they are compared with is computed by brute force, the role that
the calculator has at 32 bits. They are evidence for the method, that is
for M and for the independence of the trials at the depth of actual
collisions when words are short. They are not evidence about the constants
or the class of this package.

The toy hash is BLAKE3 with 2 rounds and W-bit words, for W = 8 and W = 10.
Its IV words are the top W bits of the real IV words. The permutation, the
flags 11 and the block lengths 60 and 62 are the same. G uses the rotations
(4, 3, 2, 1) for W = 8 and (5, 4, 3, 2) for W = 10. Everything used from
Sections 3 to 6 is independent of the word size and is applied unchanged:
the length cancellation of 3.1, a pinned call as in 3.2, Lemma H, the
construction of Section 4, and the trial of 6.1 with Lemmas F, Y, K and T. A
constant set is six W-bit constants with the property of Fact P. As in 6.1,
eta is the XOR difference of E3's first-half d value, a function of Y4
alone, and a class is the set of all Y4 with one eta.

For a constant set the number of solutions of the seven-word system is
computed by brute force for every value of Y4 separately, over all values of
the other six words. The class rate r of a class is the mean of that number
over its members, divided by 2^(2W); it is exact. The class with the largest
r is used; it has n members, a power of two.

One run is 2^(4W) trials of 6.1 for one choice of (X2, X9, X13, X14): every
value of X5, X6 and X10, and either (a) every value of X12, with member
number (X10 + X12) mod n, or (b) every X12 that is a multiple of n, each
with all n members of the class. Layout (b) is the one of 6.4 in that the
whole class is tried with everything else held fixed. In both layouts a run
differs from a run of 6.4 in the words it holds fixed: here X2, X9, X13 and
X14, there the seed words X2, X5, X6 and X9. The residual of every
trial is computed in full; rule A, the tests of 6.3 and the packing of 6.5
are not used. The E1 test and the packing change the cost of a trial and
not its outcome. Rule A drops trials, and these runs do not test it. M predicts
r collisions per run. Every collision found is checked again by building
both messages and evaluating the toy hash on each in full. The number of
runs of every series was fixed before the series started.

Results for W = 8:

| Constants | Class (members) | Layout | Runs | Predicted | Observed |
| --- | --- | --- | ---: | ---: | ---: |
| 30 19 41 90 28 9b | f7 (2) | (a) | 20 | 296.6 | 305 |
| 55 c9 21 52 63 5b | 35 (16) | (a) | 20 | 208.8 | 205 |
| 73 6a 84 e7 e3 44 | 97 (8) | (a) | 40 | 2,895.0 | 2,898 |
| 73 6a 84 e7 e3 44 | 97 (8) | (b) | 40 | 2,895.0 | 2,938 |
| 55 c9 21 52 63 5b | 35 (16) | (b) | 40 | 417.5 | 383 |
| 49 58 24 e9 20 b7 | 97 (8) | (b) | 40 | 3,125.0 | 3,106 |

"Predicted" is r times the number of runs; one run is 2^32 trials. In total
9,835 collisions were observed and 9,837.9 predicted. The largest deviation
is 1.7 standard deviations of a Poisson count (383 against 417.5). No trial
produced a Y4 outside its class, and no collision failed the full re-hash.
A further 20 runs with Y4 held at the single best member of the first set
gave 308 collisions against 296.6 predicted.

Results for W = 10:

| Constants | Class (members) | Layout | Runs | Predicted | Observed |
| --- | --- | --- | ---: | ---: | ---: |
| 3ad 17c 2d3 ab 1d7 48 | 36a (16) | (a) | 12 | 170.2 | 192 |
| af 23e 186 d3 12 70 | 1be (16) | (a) | 12 | 61.7 | 48 |
| 39b aa da 25e 279 163 | 3f2 (16) | (b) | 10 | 290.9 | 300 |
| 3ad 17c 2d3 ab 1d7 48 | 36a (16) | (b) | 10 | 141.8 | 153 |

One run is 2^40 trials. In total 693 collisions were observed and 664.6
predicted. The deviations are +1.7, -1.7, +0.5 and +0.9 standard deviations
of a Poisson count; their squares sum to 7.0 over the four rows. No trial
produced a Y4 outside its class, and no collision failed the full re-hash.

The dispersion of the collisions per run was computed for every series as the
ratio of their variance to their mean, which is 1 for independent trials. Over
the eleven series, the ten of the two tables and the 20 runs with Y4 held at
one member, it lies between 0.46 and 1.60, and pooled over their 253 degrees of
freedom it is 0.96. One series stands out: constants 49 58 24 e9 20 b7 in
layout (b), 40 runs, has 1.60, about 2.65 standard errors above 1 (for 40 runs
the standard error of the ratio is 0.23). In every one of these series every
run had a collision, as it must with between 4 and 78 collisions per run on
average. So these series do not test whether a run has at least one collision.
For the class search that is tested by the runs in the layout of the algorithm
reported further below, and for the unrestricted search in the paragraph that
follows.

The same check was made for the search that does not restrict Y4, whose
trials are outputs of step S1 enumerated by four one-word parameters, 2^(4W)
per run. There M predicts c collisions per run, where c is the exact number
of solutions of the seven-word system divided by 2^(3W). Ten constant sets
with c from 0.03 to 4.05, seven at 8 bits and three at 10 bits, and 1,465
runs gave 1,813 collisions against 1,807.2 predicted. No set differs from
its prediction by more than 1.7 standard deviations of a Poisson count. A
collision occurred in 658 runs, against 660.2 expected for independent
trials. The weakest series of that check is one of two on the 8-bit set
with c = 4.051: 40 runs of a CPU program gave 161 collisions against 162.0
predicted, but a collision in only 37 runs where 39.3 are expected; 200
runs of the GPU version on the same constants gave 826 against 810.2 and a
collision in 196 runs against 196.5. A further 10-bit job on three more
constant sets was stopped before any set had finished and contributes
nothing.

These checks test M and the independence of the trials down to actual
collisions for words of 8 and 10 bits, for runs laid out as described here
and for the constant sets named in the tables. They do not prove either for
32-bit words or for the constants of this package.

**Scaled-down runs in the layout of the algorithm (participant computation by a
helper agent, other constants).** The runs of the class search above hold other
words fixed than a run of 6.4 does, and every one of them had many collisions.
A second set of runs, made in the night before this text, has neither gap. The
toy hash is the one described above, with W = 8, 9 and 10; for W = 9 the
rotations are (4, 3, 2, 1). A run is laid out as in 6.4: its four seed words
X2, X5, X6 and X9 are drawn at random, X1 = X10 = 0, the contexts (X12, X13,
X14) are taken in a fixed order, and for every context all 2^W values of alpha
and all members of the class are tried. For every constant set the class with
the largest rate per member among the classes with at least four members is
used, with rates computed by brute force as above. A configuration is a
constant set with that class and a number of contexts per run, chosen so that M
predicts L collisions per run: L = 0.5, the value at which H1 gives its bound,
or L = 1.7, close to the 1.78 that the count of this package gives per run. The
constant sets are drawn at random. Jobs B, C, F and G keep only the sets whose
best class has a rate per member above a threshold; every job skips a
configuration that would need more trials per run than a limit; the 10-bit sets
of job D are the three with the largest class rate in an earlier scan of 24
random sets. These rules were fixed beforehand and use exact rates only, never
outcomes. A configuration has 40 to 100 runs. Every collision is confirmed by
hashing both messages in full. The jobs, the number of runs per configuration
and the statistics were fixed in a written plan shortly before the first
counted run (the plan is of about 03:25 by its own heading; the counted runs
started at 03:26). The number of configurations of a job was not fixed: a job
stops at a time limit, tested between constant sets. Results for L = 0.5:

| Job | W | Configs | Runs | With collision | Predicted | Coll. | Predicted |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 8 | 65 | 2,600 | 1,008 | 1,023.0 +- 24.9 | 1,305 | 1,300.0 |
| B | 8 | 95 | 9,500 | 3,748 | 3,738.0 +- 47.6 | 4,790 | 4,750.0 |
| C | 9 | 73 | 2,920 | 1,150 | 1,148.9 +- 26.4 | 1,460 | 1,460.0 |
| D | 10 | 3 | 180 | 75 | 70.8 +- 6.6 | 95 | 90.0 |
| F | 9 | 37 | 1,480 | 544 | 582.3 +- 18.8 | 691 | 740.0 |
| G | 9 | 35 | 1,400 | 547 | 550.9 +- 18.3 | 669 | 700.0 |
| all | | 308 | 18,080 | 7,072 | 7,113.9 +- 65.7 | 9,010 | 9,040.0 |

In the table, "configs" is the number of configurations, "with collision" the
number of runs with at least one collision, followed by its prediction and the
standard deviation of the prediction, and "coll." the number of collisions.
With L = 0.5 a run has a collision with probability 1 - exp(-1/2) = 0.3935 when
the trials are independent. Over all jobs the observed fraction is 0.3912 with
standard error 0.0036: 7,072 of 18,080 runs against 7,113.9 predicted. The
collisions number 9,010 against 9,040.0 predicted. The ratio of the variance of
the collisions per run to its prediction, 1 for independent trials, is 1.002
with standard error 0.015. No two collisions of a run fell in the same context.
No trial had a wrong Y4 or S5, and no collision failed the full re-hash. Job F
is the one job beyond two standard deviations: 544 runs with a collision
against 582.3 +- 18.8 (-2.0), and 691 collisions against 740.0 (-1.8). Jobs F
and G were added to the plan after earlier jobs had been read, which the plan
records (amendments of 03:49 and 04:14); job G repeats the settings of job F
with a new seed, as a test fixed after F was read. All jobs are in the totals.
With L = 1.7, 82 configurations and 4,300 runs gave 3,518 runs with a collision
against 3,514.5 +- 25.3 predicted, and 7,378 collisions against 7,310.0. In job
C of that series the configurations differ from each other more than chance
would often give (chi-square 44.8 on 27 degrees of freedom, probability 0.017);
its totals agree with the prediction. A reviewing helper agent recounted every
figure of the table and of the series with L = 1.7 from the raw lines of the
runs and found the same. It also found the plan in the helper's log at 03:22,
unchanged as the beginning of the plan file.

These runs test directly, at the depth of actual collisions and in the layout
of 6.4, whether a run contains a collision as often as independent trials give.
The text of submission 04638ed8 named that test as missing. They make it for
words of 8 to 10 bits, for classes of 4 to 64 members, for runs of 2^24.7 to
2^34.7 trials and for other constants. They are not evidence about 32-bit
words, where a run has 2^104 trials, or about the constants of this package,
whose count rests on few paths.

**Scaled-down runs with staged tests (participant computation, other
constants).** The thread that found rule A repeated the scaled-down class
search of the kind described above with tests placed in front of the residual
computation: a rule on the bits of h1, a rule on beta, and the E1 test of Lemma
N, on the toy hash described above, with five constant sets at 8 bits and one
constant set at 10 bits. The rule on h1 used there is not rule A. It is made of
the XOR conditions on bits of h1 that every solution of the class satisfies,
found by brute force for each constant set; there are between zero and three of
them, and such a rule loses nothing. Six of the nine series also restrict Y4 to
half of the class, and all use the rule on beta; this package does neither. A
trial that fails a test is dropped, and the prediction is the brute-force count
of the solutions that pass. Results: with 8-bit words, 8 series: 13,337
collisions against 13,505.6 predicted, -1.5 standard deviations of a Poisson
count (single series up to 2.1); with 10-bit words, 1 series: 84 collisions
against 93.3 predicted, -1.0 standard deviations of a Poisson count. In every
series every collision found passed the rules and the E1 test, the E1 test word
of every trial was equal to the word D3 XOR ROL(D6, r) of its residual, where r
is the toy's third rotation (Lemma N for the toy hash), no trial had a Y4
outside its class, and no collision failed the full re-hash. These runs test
the logic of dropping trials early and Lemma N, end to end and down to
collisions, at small word sizes. They do not test rule A of this package, which
has six conditions and loses solutions, and they are not evidence about its
constants.

The declared experiment `residual-search` runs the search of Section 6 at toy
scale: one context and one alpha per seed, then the members of the class in
order from a number taken from the seed, stopping at the first trial whose
residual has a zero low byte in digest word 1. The search runs without rule
A, without the E1 test and without the packing of 6.5. The organizer checks
that every returned pair agrees on 136 digest bits. It checks the trial
generator and the residual computation on real digests. It is not a test of
H1, H2 or H3 and says nothing direct about 128 bits. Beside the search, the
program evaluates one packed batch per seed on the counting machine of 6.5
and returns the operations and loads of its two stages, its right lanes and
whether a lane satisfied rule A as observations; the organizer records them
as untrusted and does not check them.

**Limits of the evidence.**

- The factor 2^23 in H1 is assumed. It is set against a count of 29,965,882
  under M, from a participant computation. The organizer-run experiments do not
  measure the factor, and the success bound needs it to be at least 8,375,631.
  With factor 1, the uniform rate, the same search needs 2^127 trials and gives
  time_log2 = 122.4.
- Rule A is not implied by a collision; it loses solutions. That it loses no
  more than the count allows rests on the answers of SAT solvers, for 247 of
  the 287 outcomes of the count, that no solution violates rule A. These are
  the answers of three solvers, two of them on a formula written separately by
  a reviewing helper agent, without a checked certificate; the solvers were run
  and the formulas written by the participant and the participant's helper
  agents. The 40 outcomes with a violating solution are left out in full. Rule
  A was read off counts of the same kind as the count itself, for this class:
  it was chosen to fit the solutions that the count knows. Among the counted
  betas, those that the rule was not read from comply with it less: the
  outcomes with a violating solution carry 1.25% of the part of the nine betas
  that were added after the rule was chosen, against 0.036% for the 30 that it
  was read from. Solutions of betas outside the list are not in the count;
  nothing is known about whether they satisfy rule A, and by this comparison
  they may violate it more often. The claim does not use them. No measurement
  on real messages reaches the event of H1, so none tests rule A together with
  R = 0, and the scaled-down runs with staged tests use rules of another kind.
- The count is exact only under M. It counts the solutions of the seven-word
  system; that the trials of the algorithm meet those solutions at the rate M
  predicts is the assumption. M has been tested end to end, down to actual
  collisions, only for words of 8 to 10 bits and with other constants. For
  32-bit words and these constants it has been compared with real messages only
  for events of probability about 2^-32 and above, with a largest deviation of
  2.5 standard deviations; below that, E1 alone has been counted on an event of
  probability 2^-38.57, and E3 alone, without its third condition, on one of
  2^-34.54. Its use at the probability of the event R = 0, about 2^-103.16, is
  an extrapolation that no feasible experiment can test directly.
- The constants and the class were chosen to make the count large: by a solver
  search that minimises the number of active bit positions of one solution, and
  then by the count itself. Among the 34 classes of these constants that were
  counted, the class used is the second largest. The count is deterministic, so
  no sampling noise enters it and no choice among noisy estimates was made. But
  a choice that is best under M says nothing about M. If M overstates the rate
  for some constants, a search for the largest count under M will tend to find
  those constants, and nothing here measures that.
- The count rests on few paths: 47% of it comes from one beta and 60% from two,
  with 26 outcomes (tau, eps) between them. An error in the count of these
  outcomes would change the figure in proportion. The sampler confirms the
  betas it was run on to within its errors, and it shares the E3 count with the
  calculator.
- The calculator is not part of the package, and it and every check of it are
  the participant's, the checks of the reviewing helper agents included. Its E1
  count and its enumeration of outcomes are new code, written in the night
  before this text, checked against brute force only for 8-bit words and
  against an independent counter for one beta at 32 bits. Its E3 count is the
  program of submission 04638ed8, whose checks were made with other constants,
  apart from the fourth check above.
- The count covers all 4,272 betas with k at most 14. Everything else is left
  out. That can only make the true class rate under M larger than the figure.
- All trials of a run share the four seed words: X2, X6, X9 and S5 are the same
  in every trial of a run, w5 and the column-state words S2, S6, S10 and S14
  take at most 256 values in a run because they depend on X6 and X12 only,
  trials of one context share most of their other words, and the 65,536 trials
  of one context and one alpha differ only in Y4 and what follows from it.
  Independence of the trials is assumed, not shown. With a count that rests on
  few paths, whether a run contains a collision may depend on a few shared
  words more than it would for a rate spread over many paths; this was not
  examined. The 32-bit comparison gave every context its own random words and
  so measures rates averaged over independent contexts. For these constants and
  this class there are eight runs of 2^40 trials in the layout of the
  algorithm, in which S5 was not shared and X13 was not restricted; they record
  only the early test and the number of trials in which E1 requires the class,
  and their pass counts differ by more than chance. The scaled-down runs in the
  layout of the algorithm count the runs with at least one collision, but for
  words of 8 to 10 bits and with other constants. So the distribution of
  collisions within one run of 6.4 has been tested directly only at those word
  sizes, and not for 32-bit words or for the constants of this package.
- The comparisons of M with real messages that were made for the constants of
  submission 04638ed8 showed deviations of up to 3.1 standard deviations in
  settings other than its own class, among them a spread between two runs that
  was not explained. For the constants of this package fewer runs exist, and
  what they show is stated above.
- Single-word statistics are not evidence for the joint rate. An earlier
  version of this construction, cancelled by the submitter before screening,
  used other constants and inferred a rate of half the uniform one from the
  frequencies of single zero residual words; a count of the kind described
  above gave 0.024 for those constants. For some constant sets one residual
  word vanishes 40 times more often than a uniform word while the count is
  zero.
- H2 rests on the pass rate of the E1 test measured on real trials of the class
  search with these constants: 1,521 passes in 2^40 trials with independent
  contexts. That the number of passes of a full run of 2^104 trials stays near
  the mean is assumed. In the eight runs with shared seed words the counts of
  this event are 1,462, 1,494, 1,486, 1,472, 1,432, 1,468, 1,471 and 1,527,
  with no spread beyond chance; the budget is 2^13.47 above their mean.
- H3 rests on the share of trials that satisfy rule A in four runs of 2^38 real
  trials with shared seed words, each within 1.3e-05 of 2^-6 relatively; on 24
  samples of 2^30 trials in the layout of 6.4, whose shares of batches that run
  stage 2 are at most 0.104059; and on the fact that a uniform word satisfies
  the rule with that probability. The budget is 1.142 times seven times the
  share measured in those four runs. That no run of 2^104 trials has a share
  that far above the mean is assumed. Of 8,192 sets of seed words, each sampled
  with 2^15 batches, none reached the budget; the largest share of batches was
  at most 0.1112. If a share q of all sets of seed words gave a sample at or
  above the budget, none among 8,192 would have probability (1 - q)^8192, which
  is still above 0.05 for q = 3.6 * 10^-4. So sets of seed words that rare are
  not excluded, and a sample of 2^15 batches is not a run. The number of
  batches that run stage 2 differs between the samples in the algorithm's
  layout by more than chance; the largest exceeds the smallest by 0.50% of the
  common share. If either budget of step 4 is exceeded the algorithm halts with
  failure: that lowers the success probability, by the 0.0005 allowed for each
  of H2 and H3, and does not raise the time bound.
- The charge of 17.4 operations per trial is the budgeted cost of a two-stage
  batch. With one stage, as in the submissions named below, a trial costs 34
  charged operations and the total would be larger by a factor of about 2^0.97.
  The stage counts are those of the machine in the submitted program; no
  organizer run verifies them.
- The two memory figures of the preprocessing in Section 9 are observations of
  the runs and were not measured by a tool.

**Scope and limitations.**

- No full collision of the 2-round hash is exhibited. The search is an
  analytical cost claim like other packages on this track; unlike a birthday
  search it tests each trial against zero and so needs no memory that grows
  with the number of trials.
- The two messages have different lengths, 60 and 62 bytes, and the
  construction relies on the true block length being a compression input, as
  the target profile specifies.
- The gain over a generic birthday search has three sources: half of the digest
  is matched by construction, which removes the table and about half of the
  round-1 work per trial; the constants are chosen so that the remaining half
  can match at all with a useful rate; and the search stays inside one class of
  Y4, where that rate is assumed to be 8,388,608 times the uniform one. The
  exponent of the number of trials is 104 instead of 128, and 127 if only the
  uniform rate is assumed.
- The construction and the trial are those of the submissions 17bba2ae,
  5ceb1802 and 04638ed8 on this track, which claim 123.5, 121.5 and 112.4. What
  is new here is the set of constants, the class, the count that replaces the
  sampled estimate of the rate, and the batch: it has two stages, with rule A
  in front and the E1 test of Lemma N in place of the early test of Lemma E,
  where those submissions have a batch of one stage. The claimed scalar is 13.0
  below that of submission 04638ed8. Of that difference, 12 bits are the factor
  that H1 assumes, 2^23 here against 2^11 there, and about 0.97 bits are the
  cost charged per trial, 17.4 operations here against 34 there; the rest is
  rounding of the two bounds.
- A brief literature search found free-start collisions and near-collisions of
  the compression function for reduced BLAKE variants, and no collision attack
  on the 2-round BLAKE3 hash. No priority or novelty claim is made.
- The time bound counts the arithmetic, logical and shift operations of the
  packed batch, its comparisons and its branches, and one load for every use of
  a constant or list entry, on a 16-register machine, with stage 2 counted for
  the share of the batches that step 4 allows. It is an upper bound under that
  convention, not a measured running time. The count of a batch can be rerun
  with the self-test of the submitted program (6.5); that is a participant
  check and no organizer run verifies it.

**Field meanings.**

- time_log2 = 99.4 bounds total charged time by 2^99.4 units.
- memory_log2_bytes = 35 bounds the storage of the preprocessing and of the
  search by 2^35 bytes; the search alone needs less than 2^20 bytes (Section
  9).
- preprocessing_log2 = 63 bounds the recomputation of the six constants and the
  selection of the constants, of eta and of rule A by 2^63 target-compression
  units.
- nonuniform_advice_log2_bytes = 6 bounds the stored constants, eta and the
  three constants of rule A, 40 bytes, by 64 bytes.
- success_probability = 0.39 holds under H1, H2 and H3 as shown in Section 7.

The required baseline_improved identifier blake3-r2-nominal-v2 names the
organizer's nominal display reference 128, which is not an established attack,
a qualified baseline or a security bound. The claimed scalar 99.4 is lower than
that display value. Whether a qualified result improves the Yukon incumbent is
decided separately, and no Pareto dominance claim follows from the scalar.


## 11. Complement-propagated, cross-call constant-folded, and unmasked-shift two-stage full-resident schedule (this derivative)

The set of $2^{104}$ trials, the single random 256-bit seed word, the six
constants of Section 3.2, the 65,536-member class of $Y_4$ defined by
$\eta = \mathtt{e7c1815f}$ (Lemma Q), rule A (Lemma A), the E1 test (Lemma N),
the stage-2 entry budget ($9{,}363 \times 2^{85}$ batches) and E1-test pass
budget ($2^{88}$ passes), and the full-collision confirmation are **100%
identical** to those of Section 6.4. Only the algebraic evaluation of `K3`,
`D1`, `C1`/`E1`, and `E1 test` inside a batch, the liveness order of temporary
registers, and the register residency of batch constants change. Every lane
produces the exact same 32-bit `z` word and rule-A flag in Stage A, and the
exact same 32-bit E1-test word and flag in Stage 2, as Section 6.5. There is no
change to heuristics H1, H2, or H3.

### 11.0a Two's-complement propagation in `K3` and `D1` (-2 ALU ops in Stage A, -1 ALU op in Stage 2, -1 constant)

In Section 6.5, `K3` (in Stage A) and `D1` (in Stage 2) compute (modulo $2^{32}$
in each 36-bit lane):

    s11   = kb XOR ROL(S7, 7)
    s15   = s11 + (kc XOR M) + 1                     (3 ALU ops: S11 - kc)
    s3    = ROL(s15, 8) XOR kd
    first = s3 + ((ka + kb) XOR M) + (X2 + X6 + 1)   (4 ALU ops: X2 + X6 + S3 - ka - kb)
    d     = (s11 XOR M) + (X11 - X12 + 1)            (2 ALU ops: X11 - X12 - S11)

Using the two's-complement identity $\sim(A - B) \equiv (\sim A) + B \pmod{2^{32}}$
and replacing the per-context constant $\mathrm{ROL}(S_7, 7)$ by
$\sim\mathrm{ROL}(S_7, 7) = \mathrm{ROL}(S_7, 7) \oplus M$ and $X_2 + X_6 + 1$
by $X_2 + X_6$:

    ns11  = kb XOR (~ROL(S7, 7))                     (1 ALU op:  ~S11)
    ns15  = ns11 + kc                                (1 ALU op:  ~S15 = ~(S11 - kc))
    ns3   = ROL(ns15, 8) XOR kd                      (6 ALU ops: ~S3)
    first = ((ns3 + (ka + kb)) XOR M) + (X2 + X6)    (4 ALU ops: X2 + X6 + S3 - ka - kb)
    d     = ns11 + (X11 - X12 + 1)                   (1 ALU op:  X11 - X12 - S11)

Because `kb` is a rotation output ($0 \le kb < 2^{32}$), `ns11 < 2^32`; since
`kc < 2 * 2^32`, `ns15 = ns11 + kc < 3 * 2^32` (smaller than the $4 \cdot 2^{32}$
lane bound of Section 6.5), and `ns3 + ka + kb < 4 * 2^32`, so
`(ns3 + ka + kb) XOR M` flips bits $0\dots31$ of each 36-bit lane without carry
out of bit 35, and `first < 5 * 2^32 < 6 * 2^32`. Similarly, in `D1`,
`d = ns11 + (X11 - X12 + 1) < 2 * 2^32`. This saves **2 ALU operations and 2
loads in `K3` (Stage A)** (25 ops and 12 loads instead of 27 ops and 14 loads),
saves **1 ALU operation and 1 load in `D1` (Stage 2)** (8 ops and 5 loads
instead of 9 ops and 6 loads), and eliminates the constant `1` from `K3`.

### 11.0b Cross-call constant folding (`w12 - S1 - S6`) across `C1` and `E1` (-1 ALU op in Stage 2, -1 per-context constant)

In Section 6.5, `C1 to Y1` computes `y1 = ((a1 + b1 + X9) XOR M) + (-S1 - S6)`
using the per-context constant `(-S1 - S6) mod 2^32`, and `E1, A and B` then
uses `y1` **only once**, in `a1 = y1 + y6 + w12`, using the per-context constant
`w12`. Because addition in each 36-bit lane is associative and every subsequent
consumer of `a1` (`d1 = ROR(a1 XOR X14, 16)` and `a2 = a1 + b1 + w5`) depends
only on `a1 mod 2^32`, we fold `w12` into the per-context constant
`(w12 - S1 - S6) mod 2^32`:

    y1_w12 = ((a1 + b1 + X9) XOR M) + (w12 - S1 - S6)   (in C1 to Y1: Y1 + w12 mod 2^32)
    a1     = y1_w12 + y6                                 (in E1, A and B: Y1 + Y6 + w12 mod 2^32)

Since `a1 + b1 + X9 < 5 * 2^32` in `C1 to Y1`, `y1_w12 < 6 * 2^32` (Matching the
Section 6.5 bound `6 * 2^32`), and in `E1, A and B`, `a1 = y1_w12 + y6 < 7 * 2^32`
(well below the Section 6.5 bound `10 * 2^32`). This eliminates **1 ALU addition
and 1 constant load in Stage 2** and reduces the number of per-context constants
from **14 to 13** (`w12` and `-S1 - S6` merge into `w12 - S1 - S6`).

### 11.0c Unmasked 1-bit left-shift in `E1 test` via 2-bit guard headroom (-1 ALU op in Stage 2, -1 mask constant)

In Section 6.5, `E1 test` computes `ROL(x, 1)` on `x = b1 XOR b1' XOR eps` in
5 ALU ops using `L31` (`1` in every lane) and `H31` (`0xFFFFFFFE` in every lane):

    rot  = ((x >> 31) & L31) | ((x << 1) & H31)
    word = (rot XOR eps XOR eta) & M

Observe the exact lane bounds of all operands entering `x = (b1 XOR b1') XOR eps`:
- `b1` and `b1'` are outputs of `ROR(..., 12)`, so `0 <= b1, b1' < 2^32`;
- `c2 = IV3 + d1 < 2 * 2^32` and `c2' = c2 + delta < 3 * 2^32 < 2^34`;
- `eps = c2 XOR c2'`, so `0 <= eps < 2^34`, and therefore `0 <= x < 2^34` in
  every 36-bit lane (bits 34 and 35 of every lane of `x` are strictly `0`).

Because bit 35 of every lane of `x` is `0`, the unmasked left shift `x << 1`
satisfies `0 <= (x << 1) < 2^35` in every 36-bit lane and **never crosses a
36-bit lane boundary** into the adjacent lane! Furthermore, in each lane,
`((x >> 31) & L31)` has bit 0 equal to bit 31 of `x` and bits `1..35` equal to
`0`, while `x << 1` has bit 0 equal to `0` and bits `1..31` equal to bits
`0..30` of `x`. When `word = ((((x >> 31) & L31) | (x << 1)) XOR eps XOR eta) & M`
applies the final `& M` mask, bits `32..34` of `x << 1` are cleared at the same
time as bits `32..33` of `eps`. Consequently, the intermediate `& H31` mask on
`x << 1` is completely redundant:

    rot  = ((x >> 31) & L31) | (x << 1)                  (3 ALU ops instead of 4)
    word = (rot XOR eps XOR eta) & M                     (3 ALU ops)

This produces the **exact same 256-bit `word` and `flags`** as Section 6.5 in
**13 ALU operations and 6 loads** instead of 14 ALU operations and 7 loads, and
eliminates the mask constant `H31` completely.

### 11.0d Liveness-ordered schedule and multi-tier register residency (16, 32, and 64 registers)

Re-ordering independent operations within `K3` (computing `ka + kb` immediately
after `kb` so `ka` dies before `ns15`), `D1` (computing `a = first + d` before
`x1` so `first` dies immediately), `C1 to Y1` (accumulating `a1 + X9` before `b1`
is rotated so `a1` dies early), and `E1` (forming `beta = b1 XOR b1'` inside
`E1, A and B` as soon as `b1'` is computed so `b1` and `b1'` do not both stay
live across `c2'`) reduces peak live dynamic registers from 9 to **8** (so
`Machine.registers()` on the load-every-use 16-register baseline drops from
**11 to 10**, or **7 dynamic registers** when rotation masks are resident).

With Sections 11.0a–11.0d, the two-stage batch requires **62 ALU/control
operations in Stage A** (down from 64) and **93 ALU/control operations in Stage
2** (down from 96). Across the entire two-stage batch, all constant operands (in
addition to the 9,363-word class list `U[j]`) belong to a fixed pool of **44
packed constants**:
- **16 lane/rotation/test masks**: `M`, `bit32`, `L31`, `A_SHIFT`, `A_ALL`,
  `A_VALUE`, and `(L_r, H_r)` for `r in {7, 8, 12, 16, 24}` (`H31` is eliminated
  by Section 11.0c);
- **8 fixed constants**: `1`, `11`, `IV3`, `IV7`, `Y11`, `Y11'`, `eta`, and the
  loop bound `BATCHES = 9363`;
- **13 per-context constants**: `~ROL(S7,7)`, `X2+X6`, `X11-X12+1`,
  `ROL(X12,8)`, `S12`, `X13`, `X9`, `w12-S1-S6`, `X14`, `X6`, `w0`, `w5`,
  `w5+delta` (`w12` and `-S1-S6` are merged by Section 11.0b);
- **7 per-alpha constants**: `pb`, `-pc`, `pd`, `IV3+IV7-pa-pb`, `X5`, `X5+w3`,
  `alpha`.

We evaluate four machine register tiers in `halfsearch.py` (`FullResidentMachine64`,
`ResidentMachine32`, `ResidentMachine16`, and `Machine`):
1. **64-register full-resident (`FullResidentMachine64`, 54 of 64 registers used)**:
   All 44 packed constants reside in dedicated registers across the 9,363-batch
   class loop (loaded once per `(context, alpha)` inside a 512-op per-alpha setup
   budget: scalar setup `< 40` ops + packing/loading 20 context/alpha constants
   `< 260` ops = `< 300 <= 512` ops). Inside the class loop, Stage A executes
   **62 ALU/control ops + 1 list load (`U[j]`) + 1 list-address addition = 64
   operations**, and Stage 2 executes **93 ALU/control ops + 0 memory loads = 93
   operations**. Peak register usage is `7` dynamic + `1` list index (`j`) + `1`
   stage-2 counter (` entered`) + `44` resident constants + `1` list-base register
   = **54 registers** (`<= 64`).
2. **32-register resident (`ResidentMachine32`, 32 of 32 registers used)**:
   22 highest-use constants (all 13 masks/fixed constants used in rotations and
   tests, plus 9 multi-use constants) are held in registers (`7` dynamic + `2`
   counters + `1` destination/base + `22` resident = **32 registers**). Stage A
   executes `62` ops + `7` loads = **69 operations**, and Stage 2 executes `93`
   ops + `16` loads = **109 operations**.
3. **16-register 6-mask resident (`ResidentMachine16`, 16 of 16 registers used)**:
   6 multi-use rotation masks (`M, L8, H8, L16, H16, L12`) are held in registers
   (`7` dynamic + `2` counters + `1` destination + `6` resident = **16
   registers**). Stage A executes `62` ops + `22` loads = **84 operations**, and
   Stage 2 executes `93` ops + `23` loads = **116 operations**.
4. **16-register load-every-use (`Machine`, 10 of 16 registers used)**:
   No constants are held across uses (`8` dynamic + `2` counters = **10
   registers**). Stage A executes `62` ops + `34` loads = **96 operations**
   (down from 100 in Section 6.5), and Stage 2 executes `93` ops + `39` loads =
   **132 operations** (down from 138 in Section 6.5).

| Part | Stage | ALU/control ops | Loads (64-reg) | Loads (32-reg) | Loads (16-reg res) | Loads (16-reg base) | Bound ($2^{32}$) |
| --- | :---: | ---: | ---: | ---: | ---: | ---: | ---: |
| loop | A | 3 | 0 | 0 | 1 | 1 | - |
| C0 backwards | A | 9 | 1 (`U[j]`) | 4 | 5 | 7 | 2 |
| K3 | A | 25 | 0 | 2 | 7 | 12 | 6 |
| C2 to z | A | 16 | 0 | 1 | 3 | 8 | 8 |
| rule A | A | 9 | 0 | 0 | 6 | 6 | 2 |
| **Stage A total** | **A** | **62** | **1 (+1 addr = 64)** | **7 (= 69)** | **22 (= 84)** | **34 (= 96)** | - |
| entry count | 2 | 3 | 0 | 1 | 1 | 1 | - |
| C2, rest | 2 | 12 | 0 | 0 | 2 | 4 | 3 |
| D1 | 2 | 8 | 0 | 3 | 3 | 5 | 2 |
| C1 to Y1 | 2 | 17 | 0 | 3 | 4 | 9 | 6 |
| C1 to Y6 | 2 | 12 | 0 | 2 | 2 | 6 | 4 |
| E1, A and B | 2 | 40 | 0 | 7 | 7 | 14 | 10 |
| E1 test | 2 | 13 | 0 | 0 | 4 | 6 | 2 |
| **Stage 2 total** | **2** | **93** | **0 (= 93)** | **16 (= 109)** | **23 (= 116)** | **39 (= 132)** | - |

### 11.1 Charged time across register tiers

For one context and one $\alpha$ (65,536 trials in 9,363 batches, with Stage 2
budgeted for at most $1/8$ of all batches by Step 4 and 512 operations charged
for per-$\alpha$ setup and constant preload), the main-loop cost per
$(\text{context}, \alpha)$ under the 64-register full-resident schedule is:

    9,363 * 64 + 9,363 * 93 / 8 + 512 = 599,232 + 108,844.875 + 512
                                      = 708,588.875 operations
                                      = 10.812208 * 65,536
                                      < 10.85 * 65,536 = 711,065.6.

Even if we also increase the E1-test pass confirmation allowance from $2^{10} =
1{,}024$ operations (Section 8) to $2^{12} = 4{,}096$ operations per pass across
the full $2^{88}$-pass budget ($2^{88} \times 4{,}096 = 2^{100}$ operations,
covering register save/restore of 54 registers, scalar recomputation of the
trial, six scalar `G` calls with 5-op rotations, and explicit load/store address
formation), total charged time is:

    T <= (10.85 * 2^104 + 2^100 + 2^67 + 2^60 + 2^22 + 2^11 + 1) / 430 + 2 + 2^63
       = (10.9125 * 2^104 + < 2^68) / 430 + 2 + 2^63
       = 2^98.69969 + < 2^64
       < 2^98.70.

With the original $2^{98}$-operation E1-test pass budget of Section 8 and the
exact per-alpha count $708{,}588.875 \times 2^{88} = 10.812208 \times 2^{104}$,
the total is $10.82783 \times 2^{104} / 430 + 2^{64} = 2^{98.68845} < 2^{98.70}$.
We claim **time_log2 = 98.70** under the 64-register full-resident schedule.

| Schedule variant | Registers used | Stage A ops | Stage 2 ops | Charged ops/trial | E1 pass budget | time_log2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **64-reg full-resident + Sec 11.0a-d (exact + 2^98 pass)** | **54 / 64** | **64** | **93** | **10.8122** | **2^98 (1024/pass)** | **98.688 (claimed 98.70)** |
| **64-reg full-resident + Sec 11.0a-d (10.85 + 2^100 pass)** | **54 / 64** | **64** | **93** | **10.85** | **2^100 (4096/pass)** | **98.700 (claimed 98.70)** |
| 32-reg 22-constant resident + Sec 11.0a-d | 32 / 32 | 69 | 109 | 11.85 | 2^100 (4096/pass) | 98.83 |
| 16-reg 6-mask resident + Sec 11.0a-d | 16 / 16 | 84 | 116 | 14.10 | 2^98 (1024/pass) | 99.07 |
| 16-reg load-every-use + Sec 11.0a-d (`Machine`) | 10 / 16 | 96 | 132 | 16.10 | 2^98 (1024/pass) | 99.26 |
| Source 16-reg load-every-use (`3a6f4182`, Section 8) | 11 / 16 | 100 | 138 | 17.40 | 2^98 (1024/pass) | 99.40 |

The declared organizer-executed experiment `resident-audit` runs four contexts
per organizer seed in the exact shared-seed layout of Section 6.4 (`X2, X5, X6,
X9` shared, `X10 = 0`, `X12 < 2^8`, `X13 < 2^16`), auditing both the first batch
(`j = 0`) and the padded final batch (`j = 9362`) across all four machine tiers
(`FullResidentMachine64`, `ResidentMachine32`, `ResidentMachine16`, and
`Machine`) against the scalar reference compression `compress2` and recording
the shared-seed counts of rule-A passes (`H3`), Stage-2 batch entries (`H3`),
E1-test passes (`H2`), and low-nibble residual hits (`H1`).

