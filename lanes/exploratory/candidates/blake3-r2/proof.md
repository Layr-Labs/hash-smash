# A free half-collision and a two-level sub-class search for 2-round BLAKE3

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
separately reported resource bound.

This exploratory package targets blake3-r2-prefix-v1. It has an exact part and
a heuristic part, and it keeps them apart. It continues entry c66f230d of the
same participant (time_log2 97.6) on the same pair of lengths and with the same
six constants. Section 11 corrects the errors that were found in the text of
that entry, Section 12 says what is the same and what is new, and Section 13
credits the people and the models whose work is used here.

**Exact part.** An explicit construction maps any eight 32-bit words to a
55-byte message A and a 63-byte message B whose complete 2-round BLAKE3-256
digests agree on digest words 0, 2, 5 and 7, that is on 128 of the 256 digest
bits. There is no search in this construction and no probability: it holds for
all 2^256 choices of the eight words (Sections 2 to 5). One of the eight words
is the value of one internal word of round 1, called Y4. The search holds Y4
inside a set of 131,072 values, a *sub-class* of the class of 524,288 values
that entry c66f230d searched (Section 6.1).

**Heuristic part.** A collision needs the other four digest words to agree as
well. The algorithm searches 2^100.534 such pairs, all with Y4 in the
sub-class, for one where they do. The search is arranged in two levels: the
values of a trial that depend only on the outer loop and on Y4 are computed
once per outer step and kept in a table of fixed size, which serves 2^32 passes
over the sub-class. Nothing grows with the number of trials, and nothing is
sorted or looked up by value. Seven trials are evaluated in one 256-bit word,
in two stages. Every batch runs stage A, which tests eight bit conditions on
one internal word of every trial (rule A). Only a batch in which a trial
satisfies rule A runs stage 2, which tests a 32-bit condition that every
collision satisfies. A batch in which no trial satisfies rule A is dropped; a
trial that fails rule A is examined further only if another trial of its batch
satisfies it, and Section 7 does not count such a trial. A trial is charged
1.71 primitive operations, memory loads and stores included. Three heuristics
are declared: H1, that a trial satisfies rule A and completes the collision
with probability at least 92,675,904 * 2^-128 = 2^-101.534, and that such
trials do not come in clusters; H2, that a budget on the passes of the second
test suffices; and H3, that at most one batch in 32 runs stage 2. Under the
three the search succeeds with probability at least 0.39. Total charged time is
below 2^92.58 target-compression units, so the claimed scalar is 92.58. The
search needs less than 2^23 bytes of memory; the declared 2^35 bytes also cover
the computations by which the constants, the class, the sub-class and the rule
were selected (Sections 6 to 9).

The rate in H1 is an assumption: 92,675,904 times the rate of a uniform 128-bit
value. It is not read off single digest words. Section 10 describes what it is
set against. The remaining half of the digest depends on seven words, one of
which is Y4. Under the model that the other six behave like independent uniform
words over the trials, the rate is the number of solutions of a fixed system of
equations, and that number is counted in integer arithmetic: it is
185,377,197.55 times 2^-128 for Y4 in the sub-class (162,266,763.66 for the
whole class). Rule A is not implied by a collision: some solutions violate it
and are lost. Of the count, 185,358,111 satisfy rule A; the figure that the
claim uses is the smaller 185,355,453, which leaves out in full every part of
the count in which some solution violates rule A. H1 assumes 92,675,904 times,
2.00 times less. The rates with and without rule A are equal, to the last digit
of every fraction, to those of another AI model (GPT Sol 6.1), which proposed
the sub-class and the rule; the figure 185,355,453 that the claim uses is the
participant's alone. The counting programs are not part of the package, and
they and all their checks are the participant's or that model's. The model was
compared with real messages only on events of probability about 2^-40 and
above. In the arrangement of this package those comparisons show that the model
does not hold inside one outer step, neither for rule A nor for the call E1:
only averages over outer steps have the model's values (Section 10). Real
messages have since been run for the sub-class with rule A on a graphics card
(2^44.59 trials; rule A passes at 2^-8.000002 and a marker at 2^-32.2 is about
1.18 times richer in the sub-class than in the whole class, which is not the
counted gain 1.142; the deeper marker of those tools, at 2^-40.15, has 14
counts against 21.59 expected and settles nothing at that precision, while the
same sub-class on random outer words in a later run has 275 against 288.1) and
in a scaled-down end-to-end run with real collisions that has both the
sub-class and an eight-condition rule; no run reaches a collision together with
rule A, and the organizer-run experiments measure neither the model nor the
factor (Section 10). With the uniform rate, and not 92,675,904 times it, the
same search needs 2^127 trials and gives time_log2 = 119.1.

No full 2-round collision is exhibited, and the search is far beyond feasible
computation. What is exhibited, and checked by the organizer's own runner, is
the exact half-collision on trials of the search and a toy-scale run of the
search over the sub-class, without the two tests, the table and the packing
that set the cost of a trial. The program the organizer runs also contains the
four counted pieces of the search (outer step, table build, middle step, packed
two-stage batch), a machine that counts their operations, loads and stores, and
a self-test of that count (Section 6.5). Those counts are the program's own;
the organizer does not check them.

## 1. Exact complete hash on the messages used

H is unkeyed BLAKE3-256 with only rounds 0 and 1 kept in every compression.
Every message produced has n = 55 or n = 63 bytes. A message of n <= 64 bytes
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

This is the complete hash of the target profile restricted to inputs of 55
and 63 bytes: standard IV, standard flags, true block length, both retained
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

Its outputs are (a2, b2, c2, d2). The values a1, d1, c1, b1 are called the
first, second, third and fourth value of the call, a2 the fifth, and so on.

**Fact 1.** Reading the assignments backwards,

    b1 = ROL(b2, 7) XOR c2       c1 = c2 - d2       d1 = ROL(d2, 8) XOR a2
    B  = ROL(b1, 12) XOR c1      C  = c1 - d1
    a1 = ROL(d1, 16) XOR D       y  = a2 - a1 - b1      x = a1 - A - B.

Each line is one assignment solved for another of its terms. A set of words
A, B, C, D, x, y, a1, d1, c1, b1, a2, d2, c2, b2 is the execution of one
call exactly when the eight assignments hold, in whatever order and for
whichever of their terms they were solved. The constructions below use
nothing else: every line of theirs is one assignment of one call, solved
for the name on its left.

## 3. Three ingredients

**3.1 The length is cancelled inside K2.** K2 is the only call of round 0 that
reads the block length n, the initial value of v[14], and it overwrites that
word; it is also the only call of round 0 that reads w4 and w5. Its inputs are
(IV[2], IV[6], IV[2], n). Put K = IV[2] + IV[6] = 5bf2cd1d. For lengths 55 and
63, whose XOR is 8, define for any w4, w5

    w4' = ((K + w4) XOR 8) - K        w5' = w5 + w4 - w4'.

**Lemma L.** K2 with block length 55 and words (w4, w5) leaves the same four
state words as K2 with block length 63 and words (w4', w5').

Proof. Let a1 = K + w4. In the second execution the first assignment gives
K + w4' = a1 XOR 8, so the second gives ROR(63 XOR a1 XOR 8, 16) =
ROR(55 XOR a1, 16) because 63 XOR 8 = 55: the same d1. The third and fourth
depend only on d1 and constants. The fifth gives
(a1 XOR 8) + b1 + w5' = a1 + b1 + w5 because
w5' - w5 = w4 - w4' = a1 - (a1 XOR 8). The last three depend only on values
already shown equal. QED.

Hence two messages of 55 and 63 bytes that share every word except w4, w5,
related as above, have the same state S after the column step and the same
state X after round 0, since no other call of round 0 reads v[14], w4 or w5
before K2 has made the states equal.

*Which words must be zero.* For both messages to be honest byte strings of
their lengths with the same words w6..w15, the bytes 55 to 63 of the block
must be zero in both. In the 55-byte message they are zero fill. In the
63-byte message bytes 55 to 62 are its last eight bytes, which are chosen
to be zero, and byte 63 is zero fill. Byte 55 is the top byte of w13, bytes
56 to 59 are w14 and bytes 60 to 63 are w15. So the family needs

    w14 = 0,   w15 = 0,   top byte of w13 = 0,

and nothing else: bytes 0 to 54 are free in both messages.

**3.2 A pinned call C3.** Fix the six constants

    X3 = 29d4fa98   X7 = bee3af28   X11 = 44036000   X15 = 40c58500
    W4 = 97475638   W13 = 0007c006

The top byte of W13 is zero. K + W4 = f33a2355 and W4' = ((K + W4) XOR 8) - K =
97475640, so W4 - W4' = fffffff8, that is -8 modulo 2^32. Evaluate C3 =
G(3,7,11,15, w4, W13) on the inputs (X3, X7, X11, X15) with w4 = W4 and with w4
= W4':

    w4 = W4    a1=7ffffff8 d1=7af83f3a c1=befb9f3a b1=01200183
               a2=8127c181 d2=bbfbdffe c2=7af77f38 b2=76f7aefd
    w4 = W4'   a1=80000000 d1=8500c0c5 c1=c90420c5 b1=fed77e78
               a2=7edf3e7e d2=bbfbdffe c2=850000c3 b2=76f7aefd

**Fact P.** The two executions give the same d output bbfbdffe and the same b
output 76f7aefd. They differ in the a output (8127c181, 7edf3e7e) and in the c
output (7af77f38, 850000c3). This is a finite computation on the displayed
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

## 4. Construction: the message from eight words, in three levels

The construction places the six constants of 3.2 where Lemma H needs them and
gives Y4, the b output of C0, a prescribed value y. Its input is eight free
words. Six form an *outer step*: C0.c1 and C0.d1 (the third and the second
value of the round-1 call C0), D3.d1 (the second value of the round-0 call D3),
S15 and S9 (words of the state S) and the message word w5. The seventh is X2, a
word of the state X; with it the six are a *context*. The eighth is y. X3, X7,
X11, X15 are the constants, w4 = W4, w13 = W13 and w14 = w15 = 0.

*Names.* TAG.a1, TAG.d1, TAG.c1, TAG.b1 are the first to fourth value of the
call TAG (Section 2); its outputs carry the names of the state S, X or Y they
are written to; entry c66f230d writes vc, vd, vb, va for C0.c1, C0.d1, C0.b1,
C0.a1. Arithmetic is modulo 2^32. The submitted program has steps O and M in
`outer` and `middle` ("Step S1" of entry c66f230d), step Y in `member`, step T
in `trial`.

**Step O (the outer step; 29 lines).**

    K2, forwards from w5; its first four values are constants:
        K2.a1 = IV[2] + IV[6] + W4;   K2.d1 = ROR(55 XOR K2.a1, 16)
        K2.c1 = IV[2] + K2.d1;   K2.b1 = ROR(IV[6] XOR K2.c1, 12)
        S2 = K2.a1 + K2.b1 + w5;   S14 = ROR(K2.d1 XOR S2, 8)
        S10 = K2.c1 + S14;   S6 = ROR(K2.b1 XOR S10, 7)
    D3 with w14 = w15 = 0, from D3.d1, its inputs S9, S14, its output X3:
        D3.a1 = ROL(D3.d1,16) XOR S14;   D3.c1 = S9 + D3.d1
        D3.b1 = X3 - D3.a1;   S4 = ROL(D3.b1,12) XOR D3.c1
        S3 = D3.a1 - S4;   X14 = ROR(D3.d1 XOR X3, 8)
        X9 = D3.c1 + X14;   X4 = ROR(D3.b1 XOR X9, 7)
    K3, backwards from its outputs S3, S15:
        K3.d1 = ROL(S15,8) XOR S3;   K3.c1 = IV[3] + K3.d1
        K3.b1 = ROR(IV[7] XOR K3.c1, 12);   S11 = K3.c1 + S15
        S7 = ROR(K3.b1 XOR S11, 7);   K3.a1 = ROL(K3.d1,16) XOR 11
        w6 = K3.a1 - IV[3] - IV[7];   w7 = S3 - K3.a1 - K3.b1
    C0, third assignment and fourth value; D2, backwards from X7, X8, S7:
        X8 = C0.c1 - C0.d1;   C0.b1 = ROR(X4 XOR C0.c1, 12)
        D2.b1 = ROL(X7,7) XOR X8;   D2.c1 = ROL(D2.b1,12) XOR S7
        X13 = X8 - D2.c1

**Step M (the middle step; 21 lines, from X2).**

    D2, rest:
        D2.a1 = X2 - D2.b1 - W13;   D2.d1 = ROL(X13,8) XOR X2
        S13 = ROL(D2.d1,16) XOR D2.a1;   S8 = D2.c1 - D2.d1
        w12 = D2.a1 - S2 - S7
    K1, backwards from its outputs S9, S13:
        K1.c1 = S9 - S13;   K1.d1 = K1.c1 - IV[1]
        K1.a1 = ROL(K1.d1,16);   K1.b1 = ROR(IV[5] XOR K1.c1, 12)
        S1 = ROL(S13,8) XOR K1.d1;   S5 = ROR(K1.b1 XOR S9, 7)
        w2 = K1.a1 - IV[1] - IV[5];   w3 = S1 - K1.a1 - K1.b1
    K0, backwards from its outputs S4, S8:
        K0.b1 = ROL(S4,7) XOR S8;   K0.c1 = ROL(K0.b1,12) XOR IV[4]
        K0.d1 = K0.c1 - IV[0];   K0.a1 = ROL(K0.d1,16)
        S12 = S8 - K0.c1;   S0 = ROL(S12,8) XOR K0.d1
        w0 = K0.a1 - IV[0] - IV[4];   w1 = S0 - K0.a1 - K0.b1

**Step Y (the member; 10 lines, from y and the outer step, without X2).**

    C0, backwards from its b output y:
        Y8 = ROL(y,7) XOR C0.b1;   Y12 = Y8 - C0.c1
        Y0 = ROL(Y12,8) XOR C0.d1;   C0.a1 = Y0 - C0.b1 - w6
        X12 = ROL(C0.d1,16) XOR C0.a1
    D1, backwards from its outputs X11, X12, with its inputs S6, S11:
        D1.c1 = X11 - X12;   D1.b1 = ROR(S6 XOR D1.c1, 12)
        X6 = ROR(D1.b1 XOR X11, 7);   D1.d1 = D1.c1 - S11
        X1 = ROL(X12,8) XOR D1.d1

**Step T (the four words w8..w11; 12 lines).**

    C0, its first assignment:
        X0 = C0.a1 - X4 - w2
    D0, backwards from its outputs X0, X15:
        D0.d1 = ROL(X15,8) XOR X0;   D0.c1 = S10 + D0.d1
        X10 = D0.c1 + X15;   D0.b1 = ROR(S5 XOR D0.c1, 12)
        X5 = ROR(D0.b1 XOR X10, 7);   D0.a1 = ROL(D0.d1,16) XOR S15
        w8 = D0.a1 - S0 - S5;   w9 = X0 - D0.a1 - D0.b1
    D1, rest:
        D1.a1 = ROL(D1.d1,16) XOR S12;   w10 = D1.a1 - S1 - S6
        w11 = X1 - D1.a1 - D1.b1

**Step S2.** w4' = W4' and w5' = w5 + W4 - W4', all modulo 2^32. For the
constants of 3.2 that is w5' = w5 + fffffff8, the same as w5 - 8.

**Step S3.** A is the first 55 bytes of the little-endian encoding of w0..w15;
B is the first 63 bytes of that of the same words with w4', w5' for w4, w5.

*Round 1, forwards (24 lines).* The tests of 6.3 read these values of round 1
of message A. Y3 and Y11 are the constants of Fact P for w4 = W4, and Y4 = y.

    C1, the call G(X1, X5, X9, X13; w3, w10):
        C1.a1 = X1 + X5 + w3;   C1.d1 = ROR(X13 XOR C1.a1, 16)
        C1.c1 = X9 + C1.d1;   C1.b1 = ROR(X5 XOR C1.c1, 12)
        Y1 = C1.a1 + C1.b1 + w10;   Y13 = ROR(C1.d1 XOR Y1, 8)
        Y9 = C1.c1 + Y13;   Y5 = ROR(C1.b1 XOR Y9, 7)
    C2, the call G(X2, X6, X10, X14; w7, w0):
        C2.a1 = X2 + X6 + w7;   C2.d1 = ROR(X14 XOR C2.a1, 16)
        C2.c1 = X10 + C2.d1;   C2.b1 = ROR(X6 XOR C2.c1, 12)
        Y2 = C2.a1 + C2.b1 + w0;   Y14 = ROR(C2.d1 XOR Y2, 8)
        Y10 = C2.c1 + Y14;   Y6 = ROR(C2.b1 XOR Y10, 7)
    E1 on A, with its c input Y11; third and fourth assignment in one line:
        E1.a1 = Y1 + Y6 + w12;   E1.d1 = ROR(Y12 XOR E1.a1, 16)
        E1.b1 = ROR(Y6 XOR (Y11 + E1.d1), 12);   E1.a2 = E1.a1 + E1.b1 + w5
    E3 on A, with its a input Y3 and w15 = 0; first and second in one line:
        E3.h1 = ROR(Y14 XOR (Y3 + Y4), 16);   E3.g1 = Y9 + E3.h1
        E3.f1 = ROR(Y4 XOR E3.g1, 12);   E3.e2 = (Y3 + Y4) + E3.f1 + w8

These 24 lines define nothing of the message. E3.h1, E3.g1, E3.f1, E3.e2 are
the h1, g1, f1, e2 of 6.2, and the word z of Lemma A is C2.d1 XOR Y2.

**The order and the levels.** The 29 + 21 + 10 + 12 + 24 = 96 lines above are
taken in the printed order. Lines of step O are *outer*, of step M *middle*, of
step Y *table* lines; the 12 lines of step T and the 24 of round 1 are the 36
*trial* lines. Table C gives each call's eight assignments by their left sides.

| Call | 1st | 2nd | 3rd | 4th | 5th | 6th | 7th | 8th |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| K0 | w0 | K0.a1 | K0.d1 | K0.c1 | w1 | S0 | S12 | K0.b1 |
| K1 | w2 | K1.a1 | K1.d1 | K1.b1 | w3 | S1 | K1.c1 | S5 |
| K2 | K2.a1 | K2.d1 | K2.c1 | K2.b1 | S2 | S14 | S10 | S6 |
| K3 | w6 | K3.a1 | K3.c1 | K3.b1 | w7 | K3.d1 | S11 | S7 |
| D0 | w8 | D0.a1 | D0.c1 | D0.b1 | w9 | D0.d1 | X10 | X5 |
| D1 | w10 | D1.a1 | D1.d1 | D1.b1 | w11 | X1 | D1.c1 | X6 |
| D2 | w12 | S13 | S8 | D2.c1 | D2.a1 | D2.d1 | X13 | D2.b1 |
| D3 | S3 | D3.a1 | D3.c1 | S4 | D3.b1 | X14 | X9 | X4 |
| C0 | X0 | X12 | X8 | C0.b1 | C0.a1 | Y0 | Y12 | Y8 |
| C1 | C1.a1 | C1.d1 | C1.c1 | C1.b1 | Y1 | Y13 | Y9 | Y5 |
| C2 | C2.a1 | C2.d1 | C2.c1 | C2.b1 | Y2 | Y14 | Y10 | Y6 |

The inputs, message words and outputs of the eleven calls are those of Section
1 for n = 55: Ki (i = 0..3) maps (IV[i], IV[i+4], IV[i], d) with d = 0, 0, 55,
11 to (S[i], S[i+4], S[i+8], S[i+12]); D0..D3 map (S0, S5, S10, S15), (S1, S6,
S11, S12), (S2, S7, S8, S13), (S3, S4, S9, S14), and C0..C2 map (X0, X4, X8,
X12), (X1, X5, X9, X13), (X2, X6, X10, X14), to the X and the Y words of the
same indices.

**Lemma T2.** (a) *Triangular.* In the printed order every line assigns a name
that no earlier line assigns and that is neither one of the eight words nor a
constant, and it reads only constants, the eight words (the eighth under the
name Y4 in the lines of round 1) and names of earlier lines. A line of step O
reads no word other than the six of the outer step, a line of step M reads
neither y nor a name of step Y, and a line of step Y reads neither X2 nor a
name of step M. Every line is one assignment of one call, solved for the name
on its left; the two exceptions are the lines for E1.b1 and for E3.h1, each of
which is two assignments with the first substituted into the second (c1 = Y11 +
E1.d1 and e1 = Y3 + Y4 + w15), and the line for E3.e2 uses the same e1. By
Table C the 96 lines are, each exactly once: the eight assignments of each of
the eleven calls K0..K3, D0..D3, C0..C2, with the inputs and the message words
of Section 1 for block length 55, with w4 = W4, w13 = W13, w14 = w15 = 0, and
with the constants X3, X7, X11, X15 as the a output of D3, the b output of D2,
the c output of D1 and the d output of D0; and the first five assignments of
E1 and of E3 for message A.

(b) *The calls.* For every choice of the eight words, the names of steps O, M,
Y and T are the executions of the eleven calls as listed after Table C, each
with its two message words; C0 has first, second, third and fourth value C0.a1,
C0.d1, C0.c1, C0.b1 and outputs (Y0, y, Y8, Y12); and E1.a1, E1.d1, E1.b1,
E1.a2 and E3.h1, E3.g1, E3.f1, E3.e2 are the first, second, fourth and fifth
value of E1 and the second, third, fourth and fifth value of E3 in the
compression of message A.

(c) *The levels.* An outer line is a function of the six words alone. A middle
line is a function of the six words and X2 and does not depend on y. A table
line is a function of the six words and y and does not depend on X2. In
particular the sixteen message words of two trials of one context differ at
most in w8, w9, w10, w11.

(d) *Admissible blocks.* Call a block (w0, .., w15) *admissible* if w4 = W4,
w13 = W13, w14 = w15 = 0 and round 0 on it with block length 55 ends with
(X[3], X[7], X[11], X[15]) equal to the four constants. The map of this section
from the eight words to the block of A is a bijection onto the admissible
blocks.

Proof. (a) is read off the displays, each formula compared with Section 2 and
its call's inputs, outputs and message words; Table C has one name in each of
its 88 cells, all different, and with the eight of E1 and E3 they are the 96.

(b) An assignment solved for one of its terms is an equivalent equation modulo
2^32 (Fact 1), so a line's assignment holds once it has run, and by (a) no
later line changes its names. By (a) and Table C all eight assignments of each
call hold, a constant output in its place (lines D3.b1, X14; D2.b1; D1.c1, X6;
D0.d1, X10) and y as the b output of C0 (line Y8); by Fact 1 the names are the
execution of the call. The E1 and E3 lines are those of 6.2 for message A with
Y11, Y3 of Fact P, run forwards from A's Y1, Y6, Y12, Y4, Y9, Y14.

(c) By induction over the printed order, with (a): an outer line reads only
constants, the six words and outer lines; a middle line in addition only X2
and middle lines; a table line in addition only y and table lines. w6, w7 are
outer and w0..w3, w12 middle lines, w5 is one of the six words, w4, w13, w14,
w15 are constants; only w8..w11 are trial lines.

(d) By (b), round 0 with block length 55 on an output block leaves the state X
of the names, with the constants as X[3], X[7], X[11], X[15], and the pinned
words are constants: the block is admissible. *Injective:* by (b) each of the
eight words is a value in the compression of A, so a function of the block.
*Onto:* the forward values of an admissible block (block length 55) satisfy
every equation of (a): they execute the calls, the constant outputs hold by
admissibility, and C3 has the inputs X3, X7, X11, X15, W4, W13, so Y3, Y11 are
those of Fact P. Run on the eight words taken from them, each line returns the
forward value of its name, by induction, since an assignment has exactly one
solution for any one term given the others. So the lines return the block. QED.

*The same pairs as entry c66f230d.* That entry builds the block of A from the
eight words (vc, vd, S11, S4, X13, X14, w0, y) by 72 lines, the assignments of
the nine calls K0..K3, D0..D3, C0 in another triangular order (its Lemmas S, F
and Y). By the argument of (d) both are bijections onto the same admissible
blocks and B is determined by A: the 2^256 pairs are the same, in another
order; only which of them a run visits, and in which groups, differs. This
remark is not used in any proof below.

*What Lemma T2 does not say.* Eleven of the trial lines are the line for E3.h1
and the ten it depends on (X0, D0.d1, D0.c1, X10, C2.a1, C2.d1, C2.c1, C2.b1,
Y2, Y14). That no order with fewer exists was the answer of a solver in the
search that produced the order; it is not used here and not claimed.

## 5. The half-collision

**Theorem.** For every choice of the seven words of a context (C0.c1, C0.d1,
D3.d1, S15, S9, w5, X2) and of the word y, steps O, M, Y, T, S2 and S3 output
two distinct messages A and B, of 55 and 63 bytes, whose complete 2-round
digests agree on digest words 0, 2, 5 and 7; and in both compressions the b
output of C0 is Y4 = y.

Proof. The sixteen words of steps O, M, Y and T have w14 = w15 = 0 and w13 =
W13, whose top byte is zero. So bytes 55 to 63 of their encoding are zero: A,
the first 55 bytes, is an honest 55-byte message whose zero-filled block is the
sixteen words, and B is an honest 63-byte message that ends in eight zero bytes
and whose zero-filled block is the sixteen words with w4, w5 replaced (3.1).
Run round 0 on the words of A with block length 55. By Lemma T2 (b) the column
calls leave the state S of the names and the diagonal calls, which act on
disjoint state words, leave the state X of the names. So the state after round
0 has (X[3], X[7], X[11], X[15]) equal to the four constants, and w4 = W4, w13
= W13. By Lemma L the compression of B has the same state X after round 0. The
two compressions share every word except w4, w5, so Lemma H gives the four
digest words. C0 reads X0, X4, X8, X12 and w2, w6, which are the same in both
compressions, and has b output y by Lemma T2 (b). The messages are distinct
because their lengths differ. QED.

Distinct choices of the eight words give distinct messages A: C0.c1 and C0.d1
are values inside C0, D3.d1 is a value inside D3, S15 and S9 are state words
after the column step of round 0, w5 is a message word, X2 is a state word
after round 0 and y is a state word after the column step of round 1, and all
of them are functions of the message (Lemma T2 (d)). The construction yields
2^256 different half-colliding pairs.

## 6. The search for the other half

**6.1 Trials.** A *context* is the six words of an outer step (C0.c1, C0.d1,
D3.d1, S15, S9, w5), a word X2, and everything that steps O and M compute from
them. The class and the sub-class defined next are sets of values of Y4. A
**trial** is a context and a member y of the sub-class; its messages A and B
are the output of steps O, M, Y, T, S2 and S3 for the context's seven words and
y. Only steps Y and T depend on y: the trials of one context differ in the four
message words w8..w11 and in nothing else of the message (Lemma T2 (c)). Step Y
does not depend on X2: for one outer step and one member its ten names are the
same for all 2^32 values of X2. The table of 6.5 rests on this.

*The class.* The first message word of E3 is w15 = 0, so the first assignment
of E3 is e1 = Y3 + Y4 for message A and e1' = Y3' + Y4 for message B, with Y3 =
8127c181 and Y3' = 7edf3e7e from Fact P. Put DY3 = Y3' - Y3 = fdb77cfd. The
second assignment is h1 = ROR(Y14 XOR e1, 16), so the XOR difference between A
and B of E3's first-half d value is

    eta = h1 XOR h1' = ROR((Y3 + Y4) XOR (Y3 + Y4 + DY3), 16),

a function of Y4 alone. Fix eta = 830303cf. The *class* is the set of all words
Y4 that give this eta.

**Lemma Q.** The class is the set of all Y4 with

    ((Y3 + Y4) AND 03cf8303) = 030c0303.

It has 524,288 members: the 19 bits of e1 = Y3 + Y4 at the positions where
03cf8303 has a zero are free, bit 31 among them, and Y4 = e1 - Y3.

Proof. Put x = ROL(eta,16) = 03cf8303, which has no bit 31. Y4 is in the class
exactly when e1 XOR (e1 + DY3) = x, that is when (e1 XOR x) - e1 = DY3 modulo
2^32. For words e and x, (e XOR x) - e is, modulo 2^32, the sum over the bits i
of x of 2^i where bit i of e is 0 and of -2^i where it is 1, which is 2 ((NOT
e) AND x) - x. So the condition is 2 ((NOT e1) AND x) = DY3 + x = 01870000
modulo 2^32. As (NOT e1) AND x has no bit 31, the doubling is exact and the
condition is ((NOT e1) AND x) = 01870000 >> 1 = 00c38000. All bits of 00c38000
lie in x, so this fixes the 13 bits of e1 on x to (e1 AND x) = (NOT 00c38000)
AND x = 030c0303 and leaves the other 19 bits free. QED.

*The sub-class.* The search uses only the members of the class whose e1 = Y3 +
Y4 has bit 21 and bit 26 equal to zero. With Lemma Q that is the set of all Y4
with

    ((Y3 + Y4) AND 07ef8303) = 030c0303.

**Lemma Q2.** The sub-class is a subset of the class and has 131,072 members:
the 17 bits of e1 at the positions 2 to 7, 10 to 14, 20 and 27 to 31, where
07ef8303 has a zero, are free, and Y4 = e1 - Y3.

Proof. 07ef8303 = 03cf8303 OR 04200000, and 04200000 has the bits 21 and 26,
which are two of the 19 positions that Lemma Q leaves free. The value 030c0303
has zeros at both. So the condition is the condition of Lemma Q together with
bit 21 = bit 26 = 0, and 17 positions stay free. QED.

Member number k of the sub-class, for 0 <= k < 131072, is the Y4 whose e1 has
the bits of k at its 17 free positions, in increasing order of position. From
here on "member" means a member of the sub-class. A part of the class is
searched and not all of it because, under the model of Section 10, the rate of
collisions differs from member to member and is higher on this part. Nothing
exact depends on that.

**Lemma T.** For every context and every member y of the class, and so for
every member of the sub-class, the messages A and B of the trial are distinct
messages of 55 and 63 bytes whose complete 2-round digests agree on digest
words 0, 2, 5 and 7; in both compressions Y4 = y; and the XOR difference
between A and B of E3's first-half d value is eta = 830303cf.

Proof. The first two statements are the theorem of Section 5. In both
compressions w15 = 0 and Y14 is the same, the a input of E3 is Y3 for A and Y3'
for B by Fact P, and Y4 = y is a member of the class, so the difference is eta
by the definition of the class. QED.

**6.2 The residual of a trial.** With Y3, Y3', Y11, Y11' the a and c outputs of
C3 from Fact P (8127c181, 7edf3e7e, 7af77f38, 850000c3), delta = W4 - W4' =
fffffff8 and the trial's words and state:

    (.., Y4, .., Y12) = C0 = G(X0, X4, X8, X12, w2, w6)
    (Y1, .., Y9, ..)  = C1 = G(X1, X5, X9, X13, w3, w10)
    (.., Y6, .., Y14) = C2 = G(X2, X6, X10, X14, w7, w0)
    E1 on A:  G(Y1, Y6, Y11,  Y12, w12, w5)
    E1 on B:  G(Y1, Y6, Y11', Y12, w12, w5 + delta)
    E3 on A:  G(Y3,  Y4, Y9, Y14, w15, w8)
    E3 on B:  G(Y3', Y4, Y9, Y14, w15, w8)

and R is formed from the eight output words of E1 and E3 as in 3.3. Y4 = y
and Y12 are known from step Y without evaluating C0 forwards. Write a1, d1,
c1, b1, a2, .. for the assignments of E1 and e1, h1, g1, f1, e2, h2, g2, f2
for those of E3 in the order a, d, c, b; a prime marks message B.

**6.3 Two tests of a trial.** The algorithm uses two tests: rule A, a condition
on one word of E3 (Lemma A), and the E1 test, a 32-bit condition on E1 alone
(Lemma N). The early test of the first entries on this track (Lemma E of entry
c66f230d) is not used and is not restated.

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
h2 = ROR(h1 XOR e2, 8), and h1 XOR h1' = eta for every Y4 in the class
(Lemma T), so h2 XOR h2' = ROR(eta XOR e2 XOR e2', 8). Rotating D6 left by 8
gives ROL(D6, 8) = ROL(beta XOR eps, 1) XOR eta XOR (e2 XOR e2'). The XOR
with D3 cancels e2 XOR e2' and leaves n. QED.

A trial *passes the E1 test* when n = 0. The word n needs the first seven
assignments of E1 for both messages and nothing of E3, whose eta is the
constant of the class.

*Rule A.* Let h1 be the second value of E3 on message A, as in 6.2, and write
h[i] for bit i of h1, bit 0 being the lowest. A trial *satisfies rule A* when
all of the following hold:

    h[0] = 0;    h[1] = 1;    h[16] = 0;    h[17] = 0;
    h[2] XOR h[10] = 1;    h[3] XOR h[11] = 1;
    h[3] XOR h[12] XOR h[24] = 0;    h[6] XOR h[13] XOR h[25] = 0.

Each of the eight conditions contains a bit that no other contains (bits 0, 1,
16, 17, 10, 11, 12 and 13), so they are independent and a uniform word
satisfies rule A with probability 2^-8. The first four are the first four
conditions of the rule of entry c66f230d; the other four replace its fifth
condition (bits 2 and 3 of h1 differ), which is not part of this rule.

**Lemma A.** Write z[i] and e[i] for bit i of the words z and e1 defined next.

(a) For a trial of 6.1 let z = C2.d1 XOR Y2 be the XOR of the second and the
fifth value of C2, and e1 = Y3 + Y4. Then ROL(h1, 24) = z XOR ROL(e1, 8): h[i]
= z[(i + 24) mod 32] XOR e[(i + 16) mod 32].

(b) For every Y4 in the sub-class, the trial satisfies rule A exactly when

    z[24] = 0;    z[25] = 1;    z[8] = 1;    z[9] = 1;
    z[26] XOR z[2] = 0;    z[27] XOR z[3] = e[27];
    z[27] XOR z[4] XOR z[16] = e[28];   z[30] XOR z[5] XOR z[17] = 1 XOR e[29].

The bits 27, 28 and 29 of e1 are free in the sub-class, so the last three right
sides depend on the member.

(c) Let Z be a word of 36 bits or a lane of a packed word of 6.5 whose low 32
bits are z; its bits 32 to 35 and the neighbouring lanes may hold anything.
Form the word y by

    s = (Z << 12) AND 0003c000;    y = Z XOR s;
    s = s << 12;                   y = y XOR s;
    s = (y << 13) AND 40010000;    y = y XOR s,

the shifts being shifts of the whole packed word and each mask word holding the
printed value in every lane (6.5). Write y[i] for bit i of the lane. Then

    y[8] = z[8];    y[9] = z[9];    y[24] = z[24];    y[25] = z[25];
    y[26] = z[26] XOR z[2];    y[27] = z[27] XOR z[3];
    y[16] = z[16] XOR z[4] XOR z[3];    y[30] = z[30] XOR z[17] XOR z[5].

Put ALL = 4f010300, the word with the bits 8, 9, 16, 24, 25, 26, 27 and 30. For
a member of the sub-class let v be the word with

    v[8] = 0;    v[9] = 0;    v[24] = 1;    v[25] = 0;    v[26] = 1;
    v[27] = 1 XOR e[27];    v[16] = 1 XOR e[27] XOR e[28];    v[30] = e[29]

and zeros elsewhere. Then the trial satisfies rule A exactly when (y XOR v) AND
ALL = ALL.

(d) Put u = (y XOR v) AND ALL. Then u + (2^32 - ALL) is at most 2^32, and its
bit 32 is 1 exactly when the trial satisfies rule A.

Proof. (a) The sixth assignment of C2 is Y14 = ROR(C2.d1 XOR Y2, 8) = ROR(z,
8), and the second assignment of E3 is h1 = ROR(Y14 XOR e1, 16). So h1 = ROR(z,
24) XOR ROR(e1, 16), and rotating left by 24 gives the claim.

(b) By (a) the eight conditions read: z[24] XOR e[16] = 0; z[25] XOR e[17] = 1;
z[8] XOR e[0] = 0; z[9] XOR e[1] = 0; z[26] XOR e[18] XOR z[2] XOR e[26] = 1;
z[27] XOR e[19] XOR z[3] XOR e[27] = 1; z[27] XOR e[19] XOR z[4] XOR e[28] XOR
z[16] XOR e[8] = 0; z[30] XOR e[22] XOR z[5] XOR e[29] XOR z[17] XOR e[9] = 0.
The bits 0, 1, 8, 9, 16, 17, 18, 19, 22 and 26 of e1 lie in the mask 07ef8303
of Lemma Q2, so they have the same value for every member of the sub-class: in
030c0303 the bits 0, 1, 8, 9, 18 and 19 are 1 and the bits 16, 17, 22 and 26
are 0. Inserting these values gives the conditions on z. Bit 26 is fixed only
in the sub-class, not in the class.

(c) On one lane: in Z << 12, position p holds bit p - 12 of the same lane for
12 <= p <= 35, and the mask 0003c000 keeps the positions 14 to 17, so the first
s holds z[2], z[3], z[4], z[5] there and nothing else. The second s holds the
same four bits at the positions 26 to 29, still inside the lane; so y[26] =
z[26] XOR z[2], y[27] = z[27] XOR z[3], and the positions 3 and 17 hold z[3]
and z[17] XOR z[5]. In y << 13 the mask 40010000 keeps the positions 16 and 30,
which hold those two bits; after the third step y[16] = (z[16] XOR z[4]) XOR
z[3] and y[30] = z[30] XOR (z[17] XOR z[5]). The positions 8, 9, 24 and 25 never
change. Every bit that entered one of the eight positions is a bit 2, 3, 4, 5,
8, 9, 16, 17, 24, 25, 26, 27 or 30 of the lane itself: no bit above 31 and no
bit of another lane. That proves the eight equations. A position of v holds a 1
exactly where the right side that (b) requires is 0, so bit t of y XOR v is 1
exactly when y[t] has the required value. At the positions 8, 9, 24, 25, 26 and
27 these are six of the conditions of (b) as they stand, at 30 the eighth, and
at 16 it is y[16] = e[27] XOR e[28], the XOR of the sixth and the seventh
condition, because y[16] = (z[27] XOR z[3]) XOR (z[27] XOR z[4] XOR z[16]).
When the sixth holds, that one holds exactly when the seventh does. So all
eight positions of ALL hold a 1 in y XOR v exactly when all eight conditions of
(b) hold.

(d) u has no bit outside ALL, so u <= ALL, and u + (2^32 - ALL) >= 2^32 exactly
when u = ALL; the sum is at most 2^32. By (c), u = ALL exactly when the trial
satisfies rule A. QED.

*What Lemma A does not say.* Lemma A says that the word of (c) tests rule A
exactly. It does not say that a collision satisfies rule A, and that is not
true: there are solutions of R = 0 with Y4 in the sub-class whose h1 violates
rule A. Rule A is therefore a filter that loses solutions. A batch in which no
trial satisfies it is dropped, whether or not one of its trials has a zero
residual; a trial that fails rule A is examined further only if another trial
of its batch satisfies it (6.4). How much is lost is answered in Section 10:
inside the sub-class the rule keeps all but 19,086.08 of the 185,377,197.55
counted, and the figure that H1 is set against leaves out, in full, every
outcome of the count in which some solution violates rule A. On the whole class
the same eight conditions would keep less than half of the count; the rule is a
rule for this sub-class only.

**6.4 Algorithm.**

1. Draw one fresh uniform 256-bit word and take from it the four words C0.c1,
   D3.d1, S15 and S9.
2. For each of the 1,184,670 values of C0.d1 from 0 to 1,184,669, in increasing
   order, and for each of the 2^32 values of w5, in increasing order, do one
   *outer step*: (a) run step O for the six words and store the 21 words of 6.5
   that the later steps load; (b) build the table of 6.5: for each of the
   18,725 words of the list U, in order, run the lines of step Y for its seven
   members in one packed word and store five words; (c) for each of the 2^29
   values of X2 whose bits 14, 30 and 31 are zero, in increasing order: run
   step M and store its nine words, and store as well the nine words of the
   seven sibling values of X2 that differ from it in those three bits, which
   the neighbour path reads (6.7); then run the batches of 6.5 for the 16,384
   REPRESENTATIVE members of the sub-class, those whose member number has bits
   10, 15 and 16 zero, in the order of their numbers, seven in one packed word
   (2,341 words), as 6.7 prescribes. Every batch runs stage A, which reads two
   words of the table and one word of the list V and tests rule A for its seven
   trials, and the gate H4 of 6.7 as well. If none of its trials satisfies rule
   A and none passes the gate, the batch ends and its trials are dropped. A
   trial that satisfies rule A sends its batch to stage 2, which reads the
   three other words of the table and evaluates the E1 test for the seven
   trials. A trial that passes the gate opens its CLUSTER: the 63 neighbour
   trials of 6.7 are run in packed words through stage A, and a neighbour word
   with a trial that satisfies rule A runs stage 2 in the same way.
3. For every trial of a batch that ran stage 2 whose E1 test word is zero,
   compute its words by steps Y and T and R in full. If R = 0, build A and B by
   steps S2 and S3 from the trial's words, evaluate H(A) and H(B), check that
   they agree, output (A, B) and halt. The last word of the list holds four
   members; its three spare lanes repeat the last member, and a member is
   processed once however many lanes hold it.
4. Halt with failure if 2^84 trials have been processed in step 3 without R =
   0; or if E batches have run stage 2, where E is 18,725 * J / 32 rounded down
   and J is 2^110 / 92,675,904 rounded up; or when all trials are exhausted.

A run has 1,184,670 * 2^64 pairs of an outer step and a value of X2, which is
at least J, and 18,725 batches for each pair. So E is less than one part in 32
of the batches of a run. E is the constant `STAGE_2_BUDGET` of the submitted
program, and J is its `RUN_PAIRS`.

A trial with R = 0 that satisfies rule A is found: its batch runs stage 2, its
E1 test word is zero by Lemma N, and step 3 computes its residual, unless one
of the two budgets of step 4 has ended the run before. A trial with R = 0 that
violates rule A is found only if another trial of its batch satisfies rule A;
Section 7 does not count such trials.

**The ranges.**

| Word | Values | Where it comes from |
| --- | --- | --- |
| C0.c1, D3.d1, S15, S9 | any word, fixed for the run | random word of step 1 |
| C0.d1 | 0, 1, .., 1,184,669 | slow outer loop |
| w5 | 0, 1, .., 2^32 - 1 | outer loop, piece "next w5" |
| X2 | 0, 1, .., 2^32 - 1 | middle loop, piece "next X2" |
| member number k | 0, 1, .., 131,071 | lists U and V, table |

List word j holds the members 7j, .., 7j + 6; list word 18,724 holds the
numbers 131,068 to 131,071, and the last of them three times more.

*What the submitted program holds of this, and what it does not.* The program
contains the four counted pieces (outer step, table build for one list word,
middle step, batch), the two lists, and the constant E. It contains no loop
over C0.d1, w5 or X2, no step 3 and no budget of step 3, and it does not act on
the result of an end test; its experiments draw all seven context words as full
32-bit words. The ranges above, the form of the loops and step 3 are defined by
this text only.

**The loop form and the two end tests.** The counted piece *next X2*, the first
part of the middle step, is: load the cell X2, add 1, reduce to 32 bits, load
the cell `X2 end`, compare, branch; then store the new X2 and form and store X2
+ w7. The middle loop is entered behind the branch with X2 = 0 in the register:

    X2 := 0;  go to (*)
    repeat
        X2 := (X2 + 1) mod 2^32;  leave the loop if X2 = 0
    (*) store X2, form and store X2 + w7
        the rest of step M, the class loop entry, the batches

The cell `X2 end` holds 0, so the comparison is true exactly when the word has
come back to 0, after the passes for 0, 1, .., 2^32 - 1. Each half of the piece
is executed 2^32 times in an outer step, so the piece counts once per value of
X2, as in 6.5. The loop over w5 has the same form with the piece *next w5*,
the cell `w5 end`, which holds 0, and the words w5 and w5 + delta: once per
outer step. The loop over the list words, in the build and in the batches,
advances the list position, compares it with 18,725 and branches (the part
"loop" of 6.5), once per list word.

*What starts a loop.* The machine counts of 6.5 do not contain: the entry of
the middle loop, once per outer step (X2 := 0 and the four words that the first
half of the piece would have fetched: at most 5 operations and loads); setting
the list position to zero before the build and before the batches of a value of
X2 (one operation each); and, once per value of C0.d1, the next value of C0.d1
with its end test, its store and the entry of the loop over w5 (at most 16
operations, loads and stores). They are at most 1 operation per value of X2, at
most 8 per outer step and at most 16 per value of C0.d1, and Section 8 adds
them as such. They are stated in words and were not written out on the machine.

**Lemma T3 (the trials of a run are distinct).** For every choice of the four
words of step 1, the 1,184,670 * 2^32 * 2^32 * 131,072 = 1,184,670 * 2^81
quadruples (C0.d1, w5, X2, k) of step 2 give pairwise distinct messages A, and
so that many distinct pairs (A, B). Each pair is a trial with the properties of
Lemma T.

Proof. The properties are Lemma T, which holds for all values of the eight
words. Two different quadruples differ in C0.d1, w5, X2 or k, and two different
member numbers are two different words y (by Lemma Q2 the number fills the 17
free bits of e1 = Y3 + Y4, and y = e1 - Y3). So the two tuples (C0.c1, C0.d1,
D3.d1, S15, S9, w5, X2, y) differ in at least one word, and by Lemma T2 (d)
they give different blocks and so different messages A. QED.

**How many trials.** One outer step supplies 2^32 values of X2 with 131,072
members each: 2^49 trials, in 2^32 * 18,725 batches, all with one table. With
the factor 92,675,904 of H1 the search needs 2^127 / 92,675,904 = 2^100.534
trials. The 1,184,670 values of C0.d1 (2^46 / 92,675,904 times 64 / 41.02, rounded up) give
1,184,670 * 2^81 trials, which is that many or more, in 1,184,670 * 2^32 =
2^52.442 outer steps. Entry c66f230d ran C0.d1 (its vd) below 2^19 and all
524,288 members; here the members are a quarter and the range of C0.d1 is 2.72
times as long.

The probability space of Section 7 is the one random word of step 1; the trials
depend on it only through C0.c1, D3.d1, S15 and S9. All trials of a run share
these four words; the 2^49 trials of one outer step share six words; the
131,072 trials of one context share seven. Some names are shared more widely
(Section 4). X9 and X14 are computed from D3.d1 and S9 alone, so six of the
sixteen words of X are the same in every trial of a run. Of the 29 lines of
step O, 25 (among them w6 and w7) do not read C0.d1. Y8 and Y12 are computed
from C0.c1, D3.d1, S9, w5 and y alone: for one value of w5 and one member, Y12
and w5, two of the words that E1 reads, are the same in all 1,184,670 * 2^32
trials of a run with them, about 2^52.18, and a run has 2^49 such pairs of w5
and a member.

**6.5 Seven trials in one word.** A packed word holds seven lanes of 36 bits
at bit offsets 0, 36, .., 216. A lane represents its value modulo 2^32; bits
32..35 are carry guards. A constant is placed in all seven lanes before the
batches that use it. Additions are single 256-bit additions. A rotation of
every lane by r is the five operations

    PROR(z, r) = ((z >> r) AND A_r) OR ((z << (32-r)) AND B_r)

with A_r selecting the low 32-r bits of every lane and B_r the next r bits;
the masks discard guard bits and bits shifted in from the neighbouring lane,
so the result is reduced below 2^32. With M = 2^32 - 1 in every lane, the
complement of the low 32 bits of a lane is an XOR with M, a difference
x - y of a constant x and a lane y is (y XOR M) + (x + 1), and subtracting a
constant y is one addition of the constant -y.

The lane layout, seven 36-bit lanes with reduction delayed to the rotations
and a five-operation masked rotation, follows the public ticket 2bf40fb on
this track, which uses it for a birthday search. What is evaluated in the
lanes here is different.

*The two lists.* The members are listed in CLUSTER ORDER: first the 16,384
representative members (member number with bits 10, 15 and 16 zero) in the
order of their numbers, then the other members grouped so that the seven
neighbours of a representative word lie in one word each (6.7). For list word
j, U[j] holds ROL(y, 7) and V[j] the word v of Lemma A (c), one member y per
lane; lane i belongs to the member in place 7j + i of that order, and the
first 2,341 words are the representative words. Nothing else in 6.5 or in
Lemma T4 depends on the order: both are stated for a list word and its seven
members, whatever members those are. Each list has 18,725 packed words, because
131072 = 18,724 * 7 + 4; the three spare lanes of the last word repeat its last
member. Both lists are computed once, before step 2, from eta, the two bits of
the sub-class, Y3 and the rule (Lemmas Q2 and A). The build of the table reads
U; stage A of a batch reads V; step 3 reads U for the member of a passing lane.

*The words of an outer step.* Step O is run with every value in all seven
lanes, and 21 words are stored, each below 2^32 in every lane, in the form in
which the later pieces load them:

- loaded by the build of the table (7): C0.b1, -C0.c1, -C0.b1 - w6, -X4,
  ROL(C0.d1,16), S6, -S11;
- loaded by the middle step (8): -D2.b1 - W13, ROL(X13,8), -S2 - S7, S9 + 1,
  1 - S6, D2.c1 + 1, ROL(S4,7), w7;
- loaded by a batch (6): S10 + X15, X14, X13, X9, w5, w5 + delta.

*The table of an outer step.* Five lists of 18,725 packed words each, built
once per outer step from U, the seven words above and the word C0.d1 of the
slow loop. For list word j and lane i, with y the member of that lane and the
names of step Y:

    Y12[j] = Y12        XA[j] = C0.a1 - X4        X6[j] = X6
    X1[j]  = X1         R[j]  = ROL(D1.d1, 16)

all modulo 2^32 and below 2^32 in every lane. The build computes, in every
lane:

- C0 backwards: Y8 = U[j] XOR C0.b1; Y12 = Y8 + (-C0.c1), reduced and stored;
  Y0 = ROL(Y12,8) XOR C0.d1; C0.a1 = Y0 + (-C0.b1 - w6); XA = C0.a1 + (-X4),
  reduced and stored; X12 = C0.a1 XOR ROL(C0.d1,16).
- D1 backwards: D1.c1 = (X12 XOR M) + (X11 + 1), which is X11 - X12; D1.b1 =
  ROR(D1.c1 XOR S6, 12); X6 = ROR(D1.b1 XOR X11, 7), stored; D1.d1 = D1.c1 +
  (-S11); X1 = ROL(X12,8) XOR D1.d1, reduced and stored; R = ROL(D1.d1,16),
  stored.

*The words of a middle step.* Step M is run in all seven lanes, and nine words
are stored: X2 itself; the seven words that a batch loads, X2 + w7, -w2, w0,
S5, w3, S12 and w12 - S1 - S6; and w1, which no batch loads (it is a word of
the message and is needed in step 3).

*What a batch computes.* The seven trials of a batch share a context and are
seven consecutive list places. Stage A computes in every lane:

- D0, as far as C2 needs it: X0 = XA[j] + (-w2); D0.d1 = X0 XOR ROL(X15,8); X10
  = D0.d1 + (S10 + X15), the third value S10 + D0.d1 plus X15 in one addition.
- C2 to z: its first value C2.a1 = X6[j] + (X2 + w7), its second, third and
  fourth value, the fifth as the first plus the fourth plus w0, and z, the XOR
  of the fifth and the second.
- Rule A: the word y of Lemma A (c) from z, u = (y XOR V[j]) AND ALL, the sum
  u + (2^32 - ALL) of Lemma A (d), and whether its bit 32 is set in some lane.

If it is set in no lane, the batch ends. Otherwise stage 2 computes:

- The entry count: the number of batches that have run stage 2 is advanced and
  compared with its budget E (step 4).
- C2, rest: z and the third value of C2 are formed again; Y14 = ROR(z, 8); and
  Y6 from the third value plus Y14 and the fourth value.
- D0, rest, and C1 to Y1: D0's third value as X10 + (-X15), D0.b1 with S5, and
  X5; C1's first value X5 + X1[j] + w3, its second, third and fourth value;
  D1.a1 = R[j] XOR S12; and the sum of C1's first value, its fourth value and
  D1.a1, which is Y1 + S1 + S6, since w10 = D1.a1 - S1 - S6.
- E1 on A and B: a1 as that sum plus Y6 plus the stored w12 - S1 - S6; d1 =
  ROR(a1 XOR Y12[j], 16); c1, c1', b1, b1', a2, a2', c2, c2', with Y11' and
  w5 + delta for B.
- The E1 test: eps = c2 XOR c2', beta XOR eps, the word n of Lemma N, and
  whether n is zero in some lane.

Nothing of E3 is evaluated in a batch: rule A is a condition on E3.h1, but by
Lemma A it is tested on z, a value of C2, with the bits of e1 folded into the
constants and into the list V. The words w8..w11 are never formed in a batch;
step 3 computes them, with the values of C1 and E3 that the batch leaves out,
for the trials it processes.

**Lemma T4 (the table).** Fix the six words of an outer step, and let the
memory hold the 21 words that step O stores for them. (a) For every list word j
the build stores the five words displayed above: in lane i, the values Y12,
C0.a1 - X4, X6, X1 and ROL(D1.d1,16) of the member of that lane, each below
2^32. (b) These five words do not depend on X2. (c) For every value of X2,
every list word j and every lane, the lines of a batch that read a table word
compute names of the trial (the six words, X2, the member of the lane):

    X0 = XA[j] - w2                          C2.a1 = X6[j] + X2 + w7
    C2.b1 = ROR(X6[j] XOR C2.c1, 12)         C1.a1 = X5 + X1[j] + w3
    D1.a1 = R[j] XOR S12                     E1.d1 = ROR(E1.a1 XOR Y12[j], 16).

Proof. (a) The ten lines of the build are the ten lines of step Y in the packed
forms of this section: U[j] is ROL(y,7), an addition of a stored word -v is the
subtraction of v, and (X12 XOR M) + (X11 + 1) is X11 - X12 modulo 2^32 in a
lane. No sum leaves its lane (below), so the low 32 bits of every lane are the
scalar value; the words stored after a sum are reduced by an AND with M, and R
and X6 are rotation outputs. XA is C0.a1 plus the stored -X4. (b) Y12, C0.a1,
X6, X1 and D1.d1 are table lines and X4 is an outer line, so by Lemma T2 (c)
none depends on X2. (c) The six equations are the lines for X0, C2.a1, C2.b1,
C1.a1, D1.a1 and E1.d1 of Section 4 with the words of (a) in place of the
names: XA[j] - w2 = C0.a1 - X4 - w2, R[j] XOR S12 = ROL(D1.d1,16) XOR S12, and
the other four contain X6, X1 and Y12 as they stand. QED.

*The machine, and which words are kept in registers.* The pieces run on a
load/store machine with 16 registers. One operation is charged for every
addition, XOR, AND, OR and shift of 256-bit words, for every comparison and for
every branch, so PROR = 5. One load is charged every time a word is fetched
from memory, from a list or from the table into a register, and one store every
time a register is written to memory or to the table. Shift distances are fixed
in the instruction. A register may hold a memory word across several
operations, and that is the one place where this text counts differently from
entry c66f230d, which charged a load for every use of a constant. Nine words
are loaded once per value of X2, in the last part of the middle step ("class
loop entry", 9 loads), and stay in their registers for all 18,725 batches of
that value: the two masks of the rotation by 16, the two of the rotation by
12, the two masks of Lemma A (c), ALL, 2^32 - ALL, and the word that has every
bit of the seven lanes except bit 32. Stage 2 needs the registers of the last
four for its own values and loads them again at its end (the part "restore", 4
loads, charged to stage 2). Stage A does not keep z and the third value of C2
in registers; stage 2 forms both again (5 operations and 3 loads, charged to
stage 2). Two registers hold the list position and the entry count for the
whole search. With that, the batch uses all 16 registers, and 15 do not run
it, under the program's convention that the result of an instruction may reuse
a register whose source value is used for the last time on that instruction;
if instead every source stays live until its instruction finishes, the batch
peaks at 17 registers, and the one extra word, spilled and loaded again inside
the batch, costs far less than the margin already left between the budget and
the charge. The idea of keeping masks in registers across a loop is credited
in Section 13. Under the convention of entry c66f230d, with every read of a
memory word charged as a load, the same program counts 57 and 143 for the two
stages (its line `KEPT = 0`), and the claim would be 96.0; no address
arithmetic is charged for the list and table loads, as in that entry, and with
one operation for each such load the stages would be 50 and 139 and the claim
95.8.

*No lane overflows.* Put B = 2^32. Table words, list words, stored words,
rotation outputs and constants are below B, and an XOR with a value below B
keeps a bound that is a multiple of B. In the build, Y12 and C0.a1 are below
2B, XA below 3B before it is reduced, D1.c1 below 3B, D1.d1 below 4B, and X1
below 4B before it is reduced. In stage A, X0 is below 2B and X10 below 3B;
C2's first value is below 2B, its third, X10 plus a rotation output, below 4B,
and its fifth below 4B, so z is below 4B; by Lemma A (c) the bits of z above 31
never reach a position that is read, and by Lemma A (d) the sum of rule A is at
most B. In stage 2, z and the third value are within the same bounds and the
sum for Y6 is below 5B; X10 + (-X15) is below 4B; C1's first value is below
3B, its third below 2B, and Y1 + S1 + S6 below 5B; in E1, a1 is below 7B, c1
and c1' below 2B, the two a2 below 9B and c2 and c2' below 3B. In the E1 test
beta XOR eps is below 4B, so its shift left by one bit stays inside the lane,
n is reduced by an AND with M, and the sum that forms the flags is below 2B.
So every sum of a batch is below 9B and every sum of the build below 4B, both
below 2^36 = 16B: no carry leaves a lane, the low 32 bits of every lane equal
the scalar value modulo 2^32, and XOR and PROR read only those bits. For the
outer step and the middle step a participant tool derives the bounds by
interval arithmetic on a second machine: below 7B and below 8B. Every word that
is stored and every word that enters the flags of stage 2 is below B.

*Operation counts.* For the rule with eight conditions, on the machine above:

| Part | What is computed | Operations | Loads |
| --- | --- | ---: | ---: |
| loop | next list position, end test, branch | 3 | 1 |
| X0 to X10 | X0 (1), D0.d1 (1), X10 (1) | 3 | 4 |
| C2 to z | a1 (1), d1 (6), c1 (1), b1 (6), z (3) | 17 | 4 |
| rule A | word y (8), flags and branch (6) | 14 | 1 |
|  | stage A, every batch | 37 | 10 |
| entry count | next count, budget test, branch | 3 | 1 |
| C2, rest | z again (4), c1 again (1), Y14 (5), Y6 (7) | 17 | 7 |
| C1 to Y1 | D0.b1 X5 (13), a1 (2), d1 (6), c1 (1), b1 (6), sum (3) | 31 | 8 |
| E1, A and B | a1 d1 (8), A: c1 b1 a2 c2 (16), B: (16), beta (1) | 41 | 6 |
| E1 test | eps, beta XOR eps (2), n (7), flags and branch (4) | 13 | 4 |
| restore | four kept words loaded again | 0 | 4 |
|  | stage 2, only after a pass of stage A | 105 | 30 |

So stage A is 37 + 10 = 47 and stage 2 is 105 + 30 = 135. The three other
pieces:

| Piece | Part | Operations | Loads | Stores |
| --- | --- | ---: | ---: | ---: |
| table build | build loop | 3 | 1 | 0 |
| table build | build C0 | 13 | 11 | 2 |
| table build | build D1 | 27 | 14 | 3 |
|  | table build, per list word | 43 | 26 | 5 |
| middle step | next X2 | 6 | 7 | 2 |
| middle step | D2 and K1 | 47 | 15 | 4 |
| middle step | K0 | 32 | 9 | 3 |
| middle step | class loop entry | 0 | 9 | 0 |
|  | middle step, per value of X2 | 85 | 40 | 9 |
| outer step | next w5 | 6 | 6 | 2 |
| outer step | K2 and D3 | 67 | 39 | 9 |
| outer step | K3 | 43 | 25 | 4 |
| outer step | C0 and D2 | 32 | 21 | 6 |
|  | outer step | 148 | 91 | 21 |

The build is 43 + 26 + 5 = 74 per list word, that is 74 * 18,725 = 1,385,650
per outer step; the middle step is 85 + 40 + 9 = 134 and the outer step 148 +
91 + 21 = 260. Registers in use at one time, the two for the list position and
the entry count included: 16 in a batch, 11 in the outer step, 7 in the build,
13 in the middle step.

Each XOR followed by a rotation is 6 operations, a two-term sum 1 and a
three-term sum 2. The loads of stage A are the list end, XA[j], -w2,
ROL(X15,8), S10 + X15, X6[j], X2 + w7, X14, w0 and V[j]: 10. In "rule A" the
word y is 8 operations (two shifts with an AND and an XOR, one shift with an
XOR), u an XOR with the loaded V[j] and an AND, the sum one addition, and the
flags an OR with the word that has every bit except bit 32 of each lane, a
comparison with that word and the branch: 14 operations and one load. The
loads of stage 2 are the budget; X6[j], X2 + w7 and w0 for z, and the two mask
pairs of the rotations by 8 and by 7; -X15, S5, X1[j], w3, X13, X9, R[j] and
S12; w12 - S1 - S6, Y12[j], Y11, w5, Y11' and w5 + delta; the mask of the
rotation by one bit, M, the mask of bit 32 and eta; and the four words of
"restore": 30. The count of the middle step is for all 21 lines of step M and
its nine stores; two of the lines (S0 and w1) and the store of w1 serve only
step 3 and are counted for every value of X2 all the same.

*The count in the submitted program.* The program of the two declared
experiments, experiments/halfsearch.py, contains the four pieces and the
machine that counts them, a packed word being one integer with seven 36-bit
lanes. The pieces are written only with calls that each add one operation (an
addition, XOR, AND, OR, shift, comparison or branch), one load (a fetch of a
memory, list or table word, unless it is one of the nine kept in registers) or
one store. The program always evaluates both stages of a batch, so that stage
2 is counted and checked for every batch; the algorithm runs stage 2 only
after a pass of stage A. The command

    python3 experiments/halfsearch.py --selftest N [seed]

runs N cases. A case is one outer step, one word of each list of the table, one
middle step and one packed batch; the seven context words and the list position
of a case come from SHAKE-256 of the seed text (default 1) and the case number.
Every fourth case is the last batch of the sub-class, and in every fifth case
each context word is 0, 2^32 - 1 or as drawn. Every lane is checked against the
real messages of its trial: the program builds A and B by steps O, M, Y, T, S2
and S3 and compresses each in full, with a 2-round compression written out from
Section 1 and no shortcut of the batch, and takes from them Y4 of A, h1 of E3
on A, the word n of Lemma N from E1 evaluated for A and B on their own states
and words, and the two digests. A lane is right when the sixteen words of the
55 bytes of A are the words of the trial, Y4 is the member of the lane, the
digests agree on digest words 0, 2, 5 and 7, the stage-A flag says whether h1
satisfies rule A as written in 6.3, the reduced word of stage 2 equals n, n
equals D3 XOR ROL(D6, 8) of the two digests, and the stage-2 flag says whether
n is nonzero; and no lane counts as right unless every word that the outer
step, the build and the middle step have stored is the word of the context,
and both branches are taken exactly when one of the seven words in front of
them is zero. The program prints one JSON line with the counts per part, the
largest lane of a sum per part next to its bound, the registers per piece, the
kept words, the members in the lists, the lanes checked, right and satisfying
rule A, and two complete enumerations: the flags of stage 2 on all 128 patterns
of zero and nonzero lanes, and the flags of stage A on packed words in which
every pattern of the 13 bits of z that rule A reads, with every pattern of the
bits 27 to 29 of e1, occurs once in every lane. Its exit status is 0 only if
all of these agree with this section.

With N = 2,000 and seed 1 it reports 14,000 of 14,000 lanes right; 37
operations and 10 loads in stage A and 105 and 30 in stage 2, per part as in
the table and the same in every case; largest sums of 2.968, 3.831, 1.000,
4.818, 4.511, 7.999 and 1.999 times 2^32 in the parts "X0 to X10", "C2 to z",
"rule A", "C2, rest", "C1 to Y1", "E1, A and B" and "E1 test", below the bounds
3, 4, 2, 5, 5, 9 and 2; 131,072 members in the 18,725 words of each list; and
16, 11, 7 and 13 registers. In that run 54 lanes satisfy rule A, in 46 batches.
None of its words n is zero, which is why the flags of stage 2 are also formed
for all 128 patterns of zero and nonzero lanes: all 128 are right. For rule A
the 65,536 packed words, each of the 2^16 patterns once in every lane with
different other bits and filled guard bits, are compared with rule A as written
on h1 = ROR(ROR(z, 8) XOR e1, 16): all 65,536 are right, and in 1,792 = 7 * 256
of them some lane satisfies the rule, each lane in 256, the share 2^-8.

A longer run, 1,000,000 cases with seed 61, reports 7,000,000 of 7,000,000
lanes right, the same counts in every case, the same registers and a largest
sum of 8.349 * 2^32; 27,068 of its lanes satisfy rule A, in 23,368 batches. Its
contexts are random or extreme by design and are not laid out as a run of 6.4,
and every fourth case is the short last batch, whose spare lanes repeat a
member, so these two counts are not a measurement of a rate. A participant tool
with a second counting machine, sharing no code with the program's, counts the
same operations, loads and stores for all four pieces and refuses the batch
with 15 registers; another derives the bounds of the sums for all inputs by
interval arithmetic and finds every one below the bound of its part.

In the declared experiment `residual-search` the same program evaluates, per
organizer seed, one outer step, the table words of one list word, one middle
step and one batch, for that seed's context and the list position of the first
member tried, and returns the operations and loads of the two stages of the
batch, its number of right lanes and whether a lane satisfied rule A as
observations. The organizer's runner records observations as untrusted and does
not recompute them. The self-test and these observations therefore show what
the program in the package counts, and that its lanes agree with the program's
own compression of the real messages. They are a participant check, not an
organizer verification of the cost.

**6.7 Clusters.** A *representative* is a trial whose bits 14, 30 and 31 of e1
and whose bits 14, 30 and 31 of X2 are zero. Its *neighbours* are the 63 trials
reached by flipping any non-empty subset of those six bits, the other words of
the context and the member being unchanged. A representative and its neighbours
form a *cluster* of 64 trials. The *gate* H4 is the condition that the word h1
of 6.3 has bits 16, 17 and 0 zero and bit 1 one. It is four of the eight
conditions of rule A, so every trial that satisfies rule A passes the gate.

The algorithm runs stage A on the representatives only, and the neighbours of a
representative only when that representative passes the gate. It is cheaper per
trial whose collision mass rule A keeps, because a trial whose representative
passes the gate satisfies rule A far more often than an arbitrary trial:
Section 10 reports 40.02 trial-equivalents of such trials found per
representative, measured on real messages in three independent ways (an opened
cluster yields about 2.50 neighbours that satisfy rule A, and the gate opens
for one representative in sixteen). The gate has to be weaker than rule A for
this: its four conditions are carried from a trial to its neighbours, the other
four conditions of rule A are not (Section 10).

**Lemma C (the clusters partition the trials).** Fix a context's six outer
words and the four words of step 1. Every trial of the sub-class with those
words lies in exactly one cluster, and the algorithm runs stage A on it at most
once.

*Proof.* A trial of the sub-class is a pair (X2, y) with y a member. Bits 14,
30 and 31 of e1 = Y3 + y are free in the sub-class: the mask of Lemma Q2 fixes
15 bits of e1 and none of those three. So the members split into 16,384 groups
of eight, a group being the members that agree outside those three bits of e1,
and each group holds exactly one member whose three bits are zero. The 2^32
values of X2 split in the same way into groups of eight by bits 14, 30 and 31,
each with exactly one value whose three bits are zero. A trial (X2, y)
therefore belongs to the single cluster whose representative is the pair with
those six bits cleared, and the 64 trials of a cluster are the pairs of one
member group with one X2 group, all distinct. The algorithm enumerates the
representatives once, in the order of their numbers, and the neighbours of a
representative once, so no trial is run through stage A twice. The trials of a
run remain distinct by Lemma T3, which depends on the context words only. QED

## 7. Success probability

The probability space is the one uniform 256-bit word of step 1, for the fixed
target. The algorithm is otherwise deterministic. The trials depend on that
word only through the four words C0.c1, D3.d1, S15 and S9. A run walks
1,184,670 * 2^81 = 2^101.176 trials. Of the 64 trials of a cluster it EXAMINES
the representative always and the 63 neighbours only when the gate opens, and
so finds 41.02 trial-equivalents per representative (6.7, H4): write N =
759,300 * 2^81 = 2^100.534 for the trial-equivalents a run finds, which is
what the rate of H1 and the charge of Section 8 are per. The walked range of
C0.d1 is 64 / 41.02 times the range that N alone would need, so that the
equivalents a run finds reach N.

Call a trial *good* when R = 0 and the trial satisfies rule A. By 6.4 a good
trial is found unless a budget of step 4 ends the run before.

**Heuristic H1 (score-critical).** Over the coins, the N trials behave with
respect to the event "good" like independent events of probability at least
92,675,904 * 2^-128 = 2^-101.534 each, to the extent that the probability that
no trial is good is at most exp(-1/2) + 0.002. This is one assumption with two
parts: a rate, and that the good trials of a run do not come in clusters.
Neither part follows from the other, and neither follows from the model of
Section 10. The factor 92,675,904 is assumed. Section 10 describes what it is
set against: for Y4 in the sub-class and under the seven-word model, a count in
integer arithmetic of the solutions of R = 0 that satisfy rule A,
185,358,111.47, and the smaller figure 185,355,453.45 that leaves out every
outcome of the count in which some solution violates rule A; participant
computations, of which the first equals the fraction of another AI model and
the second is the participant's alone. The organizer-run experiments do not
measure the factor.

**Heuristic H2 (supporting).** With probability at least 0.9995 over the
coins, fewer than 2^84 of the N trials pass the E1 test of Lemma N without
having R = 0. (The budget corresponds to a pass rate of 2^-17.44. The pass
rate measured on real trials of the whole class in the arrangement of this
package is 2^-31.41, which would give 2^70.03 passes, below the budget by a
factor of more than 2^13.9; in the sub-class the graphics-card run of Section
10 counts 9,537 passes of the E1 test in 2^44.585 trials, a rate of 2^-31.37.
Step 3 processes only the passes that lie in batches that ran stage 2, which
are fewer. That the number of passes of one run stays near this mean is part
of the assumption.)

**Heuristic H3 (supporting).** With probability at least 0.9995 over the coins,
fewer than E of the batches of a run hold a trial that satisfies rule A, where
E is the budget of step 4, just under one in 32 of the batches. (A batch runs
stage 2 exactly when one of its trials satisfies rule A. In every context the
number of such batches is at most the number of trials that satisfy the rule;
so H3 holds whenever fewer than E trials of the run satisfy rule A, a share of
1.1429 times 2^-8 of the trials, where a uniform h1 satisfies the rule with
probability 2^-8. H3 is a statement about the total over a run and is not true
context by context. Measured on 2^30 real trials of the sub-class, three times,
the share of the batches that run stage 2 is 0.02617, 0.02622 and 0.02622,
against the budget 0.03125; single contexts have between 0.0071 and 0.0421, so
a single context can exceed the budget on its own batches; the averages of 512
outer steps over 16 values of X2 each lie between 0.0238 and 0.0289. That the
average over the outer steps of one run stays below the budget, with the room
of 19 percent that these samples show, is the assumption.)

**Heuristic H4 (score-critical, new in this package).** Over the coins, the
number of trials found to satisfy rule A per representative, divided by the
probability that a trial satisfies rule A, is at least 40.02 on the run as a
whole. This is the yield of 6.7. It is a measured mean, not a count: Section 10
reports three independent measurements of it on real messages, and a spread of
about 14 per cent between outer steps. The charge of Section 8 divides by 41.02
trial-equivalents per representative, which is one for the representative and
40.02 for its neighbours, so the claimed time is proportional to 1 / (1 +
40.02) and a yield lower by one part in ten raises the claimed time by about
0.15.

**Heuristic H5 (score-critical, new in this package).** Over the coins, the
trials that this algorithm examines carry, per trial, at least the collision
mass that rule A keeps on average over the whole sub-class, and the good trials
of a run do not come in clusters any more than H1 already allows. The first
part is the question whether selecting a trial because its representative
passed the gate biases the trial: Section 10 reports measurements that find no
bias (one part in two thousand on one side of the event and three parts in a
thousand on the other), and the exact model of Section 10 shows that the
collision mass of a member does not depend on the three bits of e1 that the
clusters flip. The second part cannot be measured: the collision has
probability about 2^-100.53 per trial, and the deepest events these tools reach
are about 2^-32 and 2^-40. What is measured is clustering of rule-A passes
inside a cluster, which is slightly NEGATIVE (a passing neighbour next to a
passing neighbour carries one of the four heavy first-side values 3.0 per cent
less often than independent trials). Trials of one cluster share their six
outer words and differ in three bits of X2 and three bits of e1, so this is the
assumption of this package that a reviewer should test first; Section 10 says
what would settle it.

Under H1, H2 and H3 the algorithm outputs a collision with probability at least
1 - exp(-1/2) - 0.002 - 0.0005 - 0.0005 > 0.3934 - 0.003 = 0.3904 >= 0.39: by
the union bound over the three events "no trial is good", "the budget of step 3
is reached" and "the budget E is reached", which need not be independent. H1 is
read here over the trials this algorithm EXAMINES, which H5 asserts carry at
least the average mass of the trials rule A keeps; H4 and H5 do not enter that
union bound, because they are about the charge and about the trials examined,
not about a budget being reached. If H5 fails, the number of trial-equivalents
of a run falls short of N and the success probability falls with it; if H4
fails, the charge of Section 8 is too low by the ratio. When it outputs a pair,
the pair is a genuine collision: step 3 checks both complete digests, and the
messages have different lengths.

*Sensitivity to the factor.* If the rate of good trials is f * 2^-128, the N
trials give 1 - exp(-f * 759,300 / 2^47) - 0.003 with the same allowances,
which reaches 0.39 only when f is at least 92,532,532: the assumed 92,675,904
leaves no slack on the probability side. The margin of the claim lies between
the assumed 92,675,904 and the counted 185,355,453, a factor of 2.00. It is
the convention of the entries on this track that build on entry c66f230d,
half of an exact model count, used from winglock's 2bb5d604 onward; entry
c66f230d and our 60f94c5c used 3.75. If the count is exact, a factor of 2
still gives success 0.39 when good trials come in clusters of up to about 2.0
trials (3.76 at a factor of 3.75); clustering worse than pairs, or an error of
the model, is not covered by it, and H4 and H5 are not touched by any factor.
Here the rule loses almost nothing, and the three figures, 185,355,453,
185,358,111 and 185,377,197, are 2.00, 2.00 and 2.00 times the factor. For an f
between 1 and 92,675,904 the same success probability needs 2^127 / f trials
and, at the same 1.71 operations per trial, the total of Section 8 is below
2^(119.038 - log2 f): below 2^92.58 at the assumed factor, and below 2^119.038
at f = 1, the uniform rate, where the package would submit 119.1. With the more
cautious f = 2^25 = 33,554,432, the factor of entry c66f230d, which is 5.52
times below the count, the same package would search 2^102 trials, with C0.d1
below 2^21, and would submit 94.1.

*Remark on clustering.* H1 asks for more than a rate: it asks that the good
trials do not come in clusters. Under M the count of Section 10 gives
185,355,453 * N / 2^128 = 1.87 expected good trials in a run, or more, where H1
needs 0.5. Suppose that these trials came in clusters of m on average and that
the clusters fell independently. Then a run would contain one with probability
about 1 - exp(-1.87 / m), and the bound 0.39 would hold for m up to 3.74. So if
the counted rate is right, the bound survives a clustering of the successes by
that factor. This is a remark and not a proof: the counted rate rests on M, and
nothing here bounds m. Two dependences are measured and stated in Section 10:
the share of the trials that satisfy rule A depends on the context, and the
rates of single events of E1 depend on the outer step.

None of the three heuristics is proved. Section 10 lists the evidence.

## 8. Charged time

One 2-round target compression costs one unit and every other primitive word
operation, every load and every store included, costs 1/C units with C = 430.

**The cost, with every term.** The clusters of 6.7 change what a cost is per.
Stage A runs on a REPRESENTATIVE word, not on every member, and a trial of a
cluster is examined only when its representative passes the gate; what the
charge is per is therefore a TRIAL-EQUIVALENT, the collision mass that rule A
keeps on one trial of the sub-class on average. A representative yields 41.02
of them: one for itself and 40.02 for the neighbours its gate opens (H4). The
table below is per representative, and the last two rows divide by 41.02.

Let R = 16,384 be the representatives of one value of X2 and 2,341 the packed
words that hold them.

| Term | How often | Per representative |
| --- | --- | ---: |
| stage A and the gate, per representative | always | 71 / 7 |
| the dispatch of the lanes a gate opens | one in sixteen | 513 / 16 |
| a word entering stage 2, inputs placed | 0.1676 | 110.51 |
| lists, table and middle cache | amortised, 6.7 | 0.0869 |
| **budgeted, per representative** | | **67.225** |
| **budgeted, per trial-equivalent** | | **1.6389** |
| charged, per trial-equivalent | | **1.71** |

The first three rows are machine counts of the program (Section 10); the budget
of the neighbour path is 1.2 times its measured share, as 6.4 budgets the entry
to stage 2. The charge is 4.3 per cent above the budget. The cost table of the
entry this package improves on, which charges 7.7 per trial without clusters
and claims 95.7, is Section 12.

The first five terms are machine counts of the program. The term "loop control"
is a bound stated in words in 6.4 and is not a machine count. The charge is 4.3
percent above the budgeted cost; that difference is margin for operations that
a reader may find uncounted, 0.49 per batch of seven trials.

- **Main loop.** For one value of X2 the 131,072 members take 18,725 batches:
  18,724 full ones and one that holds the last four members and is charged in
  full. A run has 1,184,670 * 2^64 values of X2 in 1,184,670 * 2^32 outer
  steps, and so 18,725 * 1,184,670 * 2^64 batches. Every batch runs stage A, 47
  primitive operations by 6.5, memory loads included. By step 4 fewer than one
  batch in 32 runs stage 2, 135 operations each. On every run the main loop
  therefore costs at most 1,184,670 * 2^64 * P operations with P =
  959,206.0941, which is less than 1.639 per trial. It is charged 1.71 per
  trial, that is 1.71 * N operations. This is the budgeted cost, a bound for
  every run. The expected cost is lower: if the trials of a batch satisfied
  rule A independently with probability 2^-8, a share of 0.027025 of the
  batches, which rounds to 0.0270, would run stage 2 and a trial would cost
  7.2367 operations on average; the measured share is lower still (H3).
- **Per outer step.** Nothing is charged separately: the outer step and the
  build of the table are machine counts and are in P.
- **Lists.** The lists U and V are computed once from eta, the sub-class, Y3
  and the rule: 131,072 members at fewer than 64 operations for each list, 2^24
  operations.
- **Passes of the E1 test.** At most 2^84 are processed (step 4). The batch
  keeps no values of a passing trial. Its batch is evaluated again, both
  stages, and the rest is added in the same packed form: Y9 by the sixth and
  seventh assignment of C1; the b output of E1 for A and for B; S0 by the first
  five assignments of K0 from the stored words w0 and w1, then D0.a1 and w8; y
  from the list word U[j]; E3 for A and for B; the four words of R, their
  comparison with zero in the lane of the trial, the count of the processed
  trials, and the nine loads that put the kept words back into their registers.
  That is below 2^10 operations each: 2^94 operations, a share below 2^-8.2 of
  the main loop. This bound is stated in words and was not written out on the
  machine.
- **Final step.** Steps S2, S3 and two complete hash evaluations with their
  input handling: below 2^11 operations and 2 units, once.
- **Randomness.** One random word, charged as one operation.
- **Preprocessing.** The six constants of 3.2, the word eta, the two bits of
  the sub-class and rule A with the plan of its test are stored in the program.
  The constants were found by a solver search and chosen by the count of
  Section 10; the sub-class and the rule were read off exact counts of the same
  kind. Two different figures are involved, and this text keeps them apart. (1)
  A bound: a pair (W4, W13) with the property of Fact P and a zero top byte of
  W13, for the four given inputs X3, X7, X11, X15, is found by exhaustive
  search over at most 2^64 candidates at two G evaluations and a comparison
  each, below 128 operations: 2^71 operations, below 2^63 units. This bound
  covers the recomputation of those two words and nothing else. (2) An
  estimate: the solver search that produced all six constants and the counts by
  which the constants, eta, the sub-class and rule A were selected used fewer
  than 2^60 primitive operations in total, by the participant's estimate from
  the running times; that is not a count and not a bound, and no bounded
  algorithm for the selection is given. The measurements on real and on
  scaled-down messages of Section 10 test the heuristics and select nothing;
  they are not part of this figure, and some of them ran on graphics cards for
  hours.

Total:

    T <= (1.71 * N + 2^94 + 2^60 + 2^24 + 2^11 + 1) / 430 + 2 + 2^63
       <  1.71 * N * (1 + 2^-7) / 430 + 2^64
       <  2^92.5714 + 2^64
       <  2^92.58.

Here N = 759,300 * 2^81 = 2^100.534311 and 1.71 * N / 430 = 2^(100.534311 +
0.773997 - 8.748192) = 2^92.560116; the three logarithms are rounded so that
the result is not too small. The terms after the first add up to less than
2^94.01, which is below 1.71 * N * 2^-7, itself more than 2^94.308, and
log2(1 + 2^-7) < 0.01123. The submitted bound is time_log2 = 92.58, the total
rounded up to two decimals. The 2^60 in the first line is the estimate (2)
above, entered as if it were a bound; if the selection had cost 2^90
operations instead, the total would still be below 2^92.58. This is a
worst-case bound for the algorithm as stated, which halts within its two
budgets on every run.

The algorithm has no sorting and no lookup by value: a trial is tested against
zero, not against other trials. It has three kinds of lists, all read in the
order of the list position: the fixed list U, read once per outer step by the
build; the fixed list V, read by stage A; and the table of the current outer
step, five words per list word, written once per outer step and read by the
batches of all its 2^32 values of X2. Their loads are counted, 1 of the 26
loads of the build, 3 of the 10 loads of stage A and 4 of the 30 loads of stage
2, and so are the 5 stores per list word. One table word serves seven members
times 2^32 values of X2; that this is allowed is Lemma T4 (b). If a table had
to be built for every value of X2, the build would add 10.5717 operations per
trial.

## 9. Memory, preprocessing and advice

The program is the lines of steps O, M, Y and T, the four packed pieces of 6.5
and a compression routine for the final check. Bound the code by 4096
instruction templates of at most four 256-bit words each: 2^14 words, which is
2^19 bytes. Data, one packed word of 256 bits each: the table of one outer step
(5 * 18,725 words), the lists U and V (2 * 18,725), and fewer than 512 words
for the cells of the outer step and the middle step, the context, the fixed
constants and masks, the temporaries and the two messages and digests of the
final check: fewer than 131,587 words, that is 4,210,784 bytes. The memory of
the search is therefore below 2^19 + 4,210,784 < 2^23 bytes. Nothing grows with
the number of trials: the table is overwritten at every outer step.

*Memory of the preprocessing.* The computations by which the constants, the
class, the sub-class and the rule were selected needed far more memory than the
search. The solver search and the counting programs ran on a desktop machine
and stayed below 16 GB of main memory, 2^34 bytes; the sampling programs and
the programs for real messages stayed below 10 GB of the memory of one graphics
card. These two limits are the participant's observation of the runs, not
instrumented peaks. memory_log2_bytes = 35 covers both at once, 2^34 + 10 *
2^30 < 2^35 bytes, and with them the search. The cost model does not score
memory.

preprocessing_log2 = 63 is the bound (1) of Section 8 for recomputing the two
pinned message words at the four given inputs. It is not a bound for the
selection of the four inputs, of eta, of the sub-class or of rule A; for that
selection the text has only the estimate (2) of Section 8, which is below 2^63
units and is the participant's. Both are included in T.
nonuniform_advice_log2_bytes = 6 covers the 28 bytes of the six constants and
eta, the 8 bytes that name the two bits of the sub-class and their values, and
the 12 bytes of the two masks and the word ALL of Lemma A, 48 bytes in all. The
lists U and V are not advice: the program computes them from these constants by
Lemmas Q2 and A. There is no other stored data and no stored collision.

## 10. Evidence, scope and field meanings

Throughout this text costs and bounds are rounded up, and margins, rooms and the
whole numbers of the count that the claim uses are rounded down. Counts printed
with decimals are rounded to the nearest.

**What is exact.** Sections 2 to 5 and Lemmas L, H, Q, Q2, T, T2, T3, T4, N and
A. Lemma A says what stage A tests, not that a collision passes it. The declared
experiment `half-collision` runs one trial of 6.1 per organizer seed, with the
seven words of a context and a member number taken from the seed, and the
organizer recomputes both digests; Lemma T predicts that every trial agrees on
the 128 masked digest bits.

*What is new in the exact part and who has checked it.* Sections 1 to 3, Lemmas
L, H, Q, T and N and Fact P are those of entry c66f230d; new are the order of
Section 4 with Lemma T2, the loops with Lemma T3, the table with Lemma T4, the
sub-class with Lemma Q2 and Lemma A in the form of 6.3. All of it was written by
helper agents of the participant, instances of the same AI model as the author
of this text, and three further helper agents reviewed the assembled text (the
review is described under the limits below). Three independent reruns, by a
checking agent, a reviewing agent and a participant tool that reads the printed
text, found no wrong value in the displays, Table C and Lemmas Q, Q2, L, A, T2
and T4; only changes of wording were asked for, and they are made here. Lemma A
was checked by complete enumeration in three ways: the submitted program on all
2^16 patterns of the 13 bits of z and the 3 bits of e1 that the rule reads
(65,536 packed words); a second statement of rule and test typed by hand on
4,194,304 inputs; and seven wrong plans of the test, all of which the program
refuses. The statements (a) to (d) of 6.3 were compared with the rule and the
list V of the program on 262,144 cases: no difference. These are checks, not
proofs, and no person has read any part of this text.

**The seven-word model.** By 6.2 the residual of a trial is a function of the
constants and of seven 32-bit words: for E1 its first-half values d1 and b1 and
its a output a2 on message A, and for E3 the words Y4, Y9, w8 and its first-half
value h1 on A. In the algorithm Y4 takes every member of the sub-class equally
often; the model M says that over the trials the other six behave like
independent uniform words, independent of Y4. Under M a trial has R = 0 with
probability r * 2^-128, where r * 2^81 is the number of solutions of R = 0 among
the 2^209 values of the seven words with Y4 in the sub-class. Call r the *rate
of the sub-class*. Rule A is a condition on h1, so under M the trials with R = 0
that satisfy rule A have a rate of the same kind, r_A, counting only the
solutions that satisfy rule A; r_A is at most r. M and r_A >= 92,675,904
together give the rate that H1 assumes for a single trial. They do not give H1:
H1 also assumes that the good trials of a run do not come in clusters, and a
model of the single trial says nothing about that.

Given M, the rate is a property of the constants and the sub-class alone and can
be counted without sampling; the count says nothing about whether M holds. The
six words are not free in a trial: within one context each is a function of Y4,
and Y12 and w5 are the same in all 1,184,670 * 2^32 trials of a run with one
value of w5 and one member, which lie in 1,184,670 outer steps (6.4). M is a
statement about averages over the outer steps of a run, and the measurements
below show where it fails inside one context and inside one outer step.

**How r is counted (participant computation, not organizer-verified).** Write
tau, eps, beta for the XOR differences between A and B of E1's a output, c
output and first-half b, and eta, psi, tau', eps' for those of E3's first-half d
and b and its c and a outputs. Because E1's a1 and d1 are the same for A and B,
R = 0 holds exactly when tau' = tau, eps' = eps, psi = tau XOR ROR(tau, 1) and
eta = eps XOR ROL(beta XOR eps, 1); for Y4 in the class the left side of the
last equation is the constant 830303cf. The counter works in integers (128-bit
unsigned integers; exact fractions for the products and sums), has no sampling
branch, and needed no fallback on any outcome of the count below; no
floating-point number is on the path of a figure printed below as a fraction.

1. *The betas.* beta is a function of d1 alone: with c1 = Y11 + d1 and DY11 =
   Y11' - Y11 = 0a08818b, beta = ROR(c1 XOR (c1 + DY11), 12). As in Lemma Q, the
   d1 with a given beta are a share 2^-k of all d1, k being the number of bits
   of the mask ROL(beta,12) AND 7fffffff.
2. *The outcomes of one beta.* An outcome is a pair (tau, eps); the admissible
   tau are enumerated with a carry automaton, with no bound on the weight of
   tau. A beta for which beta XOR ROR(eta, 1) has odd weight contributes
   nothing; every other has two candidates for eps.
3. *The E3 side.* N3 is the number of quadruples (Y4, h1, Y9, w8) for which E3
   produces eta, psi, eps and tau; all of them have Y4 in the class.
4. *The E1 side.* P1 is the probability that E1 produces tau and eps when d1 is
   uniform among the values with this beta and b1 and a2 are uniform.
5. *The sum.* For the sub-class, N3 counts only the quadruples with Y4 in the
   sub-class, and the part of a beta in r is 2^(15 - k) times the sum over its
   outcomes of P1 * N3, where 15 is the number of bits that Lemma Q2 fixes, so
   that the sub-class is a share 2^-15 of all Y4: the sum of N3 over all 2^96
   values of (d1, b1, a2) is r * 2^81, and 2^96 / 2^81 = 2^15. r is the sum of
   the parts over all betas. Parts are not negative, so the sum over any set of
   betas is a lower bound for r. For r_A, N3 counts only the quadruples whose h1
   satisfies rule A.

**The count for this package (participant computation).** The count runs over
the 60 words beta that have a part in the rate of the whole class, the list of
entry c66f230d: of the 133,742 words that occur as beta, the 4,550 with k at
most 14 were enumerated, and for the 129,192 others a SAT solver was asked
whether the whole system has a solution with that beta and answered no for
129,147, without certificates. The integer enumeration of GPT Sol 6.1 over every
beta finds the same 60. A beta without a part in the class has none in the
sub-class; the other betas were not searched again here.

For the whole class the rate is 85074516985129/524288 = 162,266,763.66, from 60
betas and 453 outcomes with a nonzero product. For the sub-class it is

    r = 194382080300609/1048576 = 185,377,197.55,

from 53 betas and 317 outcomes, about 2^27.47, so that under M a trial has R = 0
with probability about 2^-100.53. The rate of the sub-class is 1.142 times the
rate of the class: under M the members do not have the same rate, and the
quarter of the class in which bits 21 and 26 of e1 are zero has more than its
share.

| beta | Outcomes | Part of r | With rule A | Kept for H1 |
| --- | ---: | ---: | ---: | ---: |
| 18b0e098 | 7 | 67,698,688 | 67,698,688 | 67,698,688 |
| 18b1a098 | 16 | 51,384,320 | 51,384,320 | 51,384,320 |
| 18d0e098 | 12 | 50,790,400 | 50,790,400 | 50,790,400 |
| 18d1a098 | 12 | 13,246,464 | 13,246,464 | 13,246,464 |
| 18b3e098 | 4 | 1,474,560 | 1,474,560 | 1,474,560 |
| 18d3e098 | 6 | 755,712 | 755,712 | 755,712 |
| 18d16398 | 6 | 13,328 | 456 | 0 |
| 18f1e098 | 8 | 3,465 | 1,665 | 0 |
| 45 others | 246 | 10,260.5523 | 5,846.4676 | 5,309.4537 |
| sum | 317 | 185,377,197.5523 | 185,358,111.4676 | 185,355,453.4537 |

"With rule A" is the part of the beta in r_A. "Kept for H1" adds only the
outcomes in which every solution satisfies rule A. The heaviest beta carries
36.5% of the count and the four heaviest 98.8%. The count rests on few paths.

*Rule A in the count.* Of the 317 outcomes, 99 have only solutions that satisfy
rule A, 76 have none that does, and 142 have both. The exact rate with rule A is

    r_A = 6219586146887739/33554432 = 185,358,111.47,

so the rule loses 19,086.08 of r, about one part in 10,000, and the sum over the
99 outcomes is 12147454997539/65536 = 185,355,453.45. H1 is set against this
smaller figure, as entry c66f230d set it against the outcomes without a
violating solution; the two differ by 2,658.01 and no figure of the claim
changes with the choice. On the whole class the same eight conditions keep
76,072,772.68, less than half, and no outcome there is free of violating
solutions: the rule belongs to this sub-class.

*The rules that were prepared.* The submitted program holds three rules, each
containing the one before it: the first four conditions; those and the two on
bits 2, 10 and 3, 11; and all eight. For each, the same counter gives the rate
inside the sub-class and the program's machine the cost.

| Rule | r_A, exact | Kept for H1 | Stage A, 2 | Entry | Charged | Scalar |
| ---: | ---: | ---: | --- | --- | ---: | ---: |
| 4 | 185,358,154.95 | 185,355,465.45 | 37, 128 | 1/2 | 15.1 | 95.8 |
| 6 | 185,358,125.47 | 185,355,465.45 | 41, 135 | 1/8 | 8.6 | 95.0 |
| 8 | 185,358,111.47 | 185,355,453.45 | 47, 135 | 1/32 | 7.7 | 94.8 |

Inside the sub-class the four further conditions cost 43.48 of the count and
divide the share of the batches that run stage 2 by sixteen. "Rule" is the
number of conditions, "Entry" the share of the batches that may run stage 2,
"Scalar" what the package would submit with that rule and the factor 92,675,904.
The rules with four and six conditions are not claimed; their figures are given
so that the choice can be seen.

**Where the sub-class and the rule come from, and the second count.** Both were
proposed by another AI model, GPT Sol 6.1 (OpenAI), run by the participant with
briefs that asked for exact counting. With a counter of its own it computed the
rate of sub-cubes of the class and searched for affine conditions on h1 that
keep the count; its answers give this sub-class, r = 194382080300609/1048576,
and the eight conditions, r_A = 6219586146887739/33554432. It calls its sets
"best found": its search over conditions is not exhaustive. A second instance of
the same model, given the decimal figures, reports the same two fractions and
calls the sub-class the only best of the sub-cubes with 15 fixed bits of e1, and
the eight conditions, in another basis of the same affine set, a certified best
among all sets of eight affine conditions on h1. The participant has not checked
these two statements, and nothing the participant has checked shows that no
better sub-class or rule exists. The participant's counter, extended by the
sub-class, agrees with the other model's files on 21 exact fractions (totals and
rule masses for this sub-class, for a second sub-class of 32,768 members and for
the whole class), on the rate of every beta and on 3,243 integers over 1,081
outcomes, with no difference; this was a recount with those figures at hand, not
a blind one. The other model does not give, and the participant alone has, the
figure "kept for H1", the split by beta, and the rules with four and six
conditions inside the sub-class.

**Checks of the counter (participant computations).** (1) Complete enumeration
with 8-bit words of every quadruple (Y4, h1, Y9, w8) through both executions of
E3 and every triple of the E1 side, over random constants, classes, sub-classes
with up to three more fixed bits of e1 and rules with parities of three bits:
five runs, 1,472,040 and 5,332,992 integers, none different from the counter.
(2) At 32 bits two functions compute the E3 side with its split by the rule and
agree on all 687 outcomes both counted; the other 285 (16 with a nonzero
product) were counted by one alone. The E1 count agrees with the earlier
calculator on 972 of 972 outcomes. (3) The untouched calculator of entry
c66f230d, with an option of its own for a sub-class, finished 54 of the 60 betas
in the time allowed, each equal to the part printed above at its one printed
decimal; the six unfinished carry together 0.3346 of the 185,377,197.55 of r, a
share of 1.8 * 10^-9. (4) For the whole class, a helper agent that audited entry
c66f230d counted both factors of all 453 outcomes with two programs written from
the definitions of 6.2 and 6.3 alone: the same total, 85074516985129/524288, and
the same parts for 60 of 60 betas. The checks that entry c66f230d reports for
the whole class (an approximate model counter on the sixteen largest outcomes,
brute force with 8-bit words, a sampler for the four heaviest betas) were not
repeated for the sub-class.

**How the constants and the class were found.** As in entry c66f230d: the six
constants come from a SAT solver search for a pinned call with the property of
Fact P and a zero residual, with the two words w4 related as the length
cancellation prescribes and a zero top byte of word 13; the class is the class
of the solver's solution, and the constants were chosen among the solver's sets
by the count. The constants and the class were chosen to make the count large,
and the sub-class and the rule by the count as well.

**Real messages in the arrangement of this package: what exists.** All of the
following are participant measurements.

*The self-test and the equivalence runs (processor).* Every lane of the
self-tests of 6.5 is compared with the complete digests of its two real
messages: 7,000,000 lanes in the long run. On 200,000 batches the program makes
the same decisions (members, table words, flags and branches of both stages) as
a first form of the two-level program that fetches every word where it reads it,
keeps nothing in registers and tests the rule as written on h1. One complete
outer step was run: all 18,725 table words equal the words of their members, and
with that one table all 18,725 batches of one value of X2 (131,075 lanes) and
3,000 batches of each of three more values of X2 are right against the complete
digests.

*Rule A and the entry to stage 2 in the sub-class (processor).* Three runs of
2^30 real trials each, in the member order of the program, with h1 taken from
the trial and anchored against the complete compression of message A on 65,536
trials per run: 8,192 independent contexts; 512 outer steps with 16 values of X2
each; and 8,192 contexts from a second seed. The first two were drawn from the
same seed text, so the 512 contexts of the first value of X2 of each outer step
of the second are also contexts of the first. Rule A is satisfied by 2^-8.0019,
2^-7.9992 and 2^-8.0000 of the trials. The share of the batches that run stage 2
is 0.02617, 0.02622 and 0.02622; independent trials would give 0.0270, and the
budget is 0.03125. Single contexts have between 0.0071 and 0.0421, the 512 outer
steps between 0.0238 and 0.0289, and the one value of X2 run in full above has
574 of 18,725, a share of 0.0307. In the review of this text three helper agents
measured the same share again, each once and with a program of its own, in
contexts in the ranges of step 2: 0.026171 in 8,192 contexts, 2^30 trials from
four seeds (0.02609 to 0.02626 per seed, 5 contexts above the budget, h1
anchored on 16,384 trials, all equal); 0.02619 on 2^22 trials; and 0.02620 in
640 contexts, 4 of them above the budget. The first was run again for this text
with the same output. Until the graphics-card and scaled-down runs below, these
were the only measurements that have the sub-class and the rule of this package.

*Layout runs of the two-level arrangement (graphics card).* Real messages
enumerated as step 2 enumerates them (six outer words fixed for a run,
consecutive values of X2, every member in list order, batches of seven
consecutive members), but for the whole class of 524,288 members and with the
rules of four, five and six conditions of entry c66f230d: 24 outer tuples of
2^40 trials, two deeper runs of 2^44, eight runs with X2 spread over its range,
4,096 random outer tuples and 4,096 consecutive values of w5. A second helper
agent recounted the raw outputs with its own parser (451 comparisons, 449 equal,
two differing in the last printed digit), rebuilt the program, repeated one run,
and checked on the processor that the layout is the algorithm's. Averaged over
outer tuples the counts agree with the model within their statistical error; for
the deepest event that error is large, 138 of 152.0 being a ratio of 0.91 with
one-sided 95% limits 0.785 and 1.046.

| Event | Probability per trial | Average against the model |
| --- | --- | --- |
| rule with 4, 5, 6 conditions | 2^-4 to 2^-6 | within one part in a million |
| listed beta | 2^-7.96 | +0.73 standard deviations |
| listed beta and tau | 2^-18.88 | +0.83 standard deviations |
| listed partial E3 event | 2^-32.2 | -0.24 standard deviations |
| listed E1 outcome | 2^-40.15 | 138 of 152.0 expected (-1.14) |

What they do not support, and what this text must not claim: independence of the
trials inside one outer step. The share of the trials of one value of X2 that
satisfy a rule is not binomial (for five conditions its variance is 2.7 to 181
times the binomial one), and the members of a batch pass together. For E1 the
rate of a listed tau given a listed beta is a property of the outer tuple: for
17 cells carrying 24% of the count it lies between 0.02 and 2 times its average,
it is the same for 4,096 consecutive values of w5, and the cause is known (Y12
and w5 are fixed inside an outer step). A weighted estimate of the rate of
solutions of one outer tuple, relative to the average, has a standard deviation
of about 0.7% between tuples; it has mean 1 by construction and stops at the
level of beta and tau. One count is unexplained: in one window of 2^44 trials of
one tuple, 3 listed E1 outcomes were seen where 14.65 are expected (probability
0.0003 under a Poisson law); the next window of the same tuple has 16, and the
cells one level up do not differ. Chance is the likelier reading and it is not
excluded that it is not chance. The E1 test passes at 2^-31.41 per trial
(2^-31.20 in the tuple with the most). The outer words here are random words: no
run has C0.d1 in the short range of step 2, and none holds a whole outer step,
the longest having 2^26 values of X2 of one tuple.

*Scaled-down end-to-end runs in the two-level order.* The whole search of this
pair of lengths was run on small versions of the hash, with 8-bit and 10-bit
words and 2-bit bytes, messages of 7W - 1 and 7W + 7 such bytes, random constant
sets and for each its best class of 4 to 64 members. A run is four random seed
words and a number of outer steps, each with all 2^W values of X2 and all
members; both byte strings of every trial are hashed completely and all eight
digest words compared, with no rule and no filter. The prediction for a run is
the number of solutions of the seven-word system for that set, by complete
enumeration, times the number of outer steps over 2^(5W). All runs made in this
folder, each counted once: 436 runs, 470 collisions found against 467.6
predicted (+0.11 standard deviations); with 8-bit words 463 against 455.9 in 415
runs, with 10-bit words 7 against 11.7 in 21 runs. Every collision was confirmed
from its two byte strings. The history must be said with the sum: the first job
of 92 runs was low (56 against 74.8, -2.17 standard deviations); two more jobs
were then made, each written down before it was run, and they were not low (307
against 284.0 in 280 runs, and 104 against 102.0 in 60 runs for the one constant
set that had stood out); the other four runs are the self-check of the scripts (3
against 6.8). One series of that set, 2 collisions against 13.0 in 26 runs, was
taken as chance. The larger job of the same kind, whose expected values and rule
of judgement were written down before it was run, ran on another machine after
the text of this package was first assembled. It has 8,448 runs (the 92 of the
first job among them): 8,108 collisions against 8,313.6 predicted (-2.25
standard deviations); with 8-bit words 6,276 against 6,489.6 in 6,528 runs, 3.3
per cent low (-2.65); with 10-bit words 1,832 against 1,824.0 in 1,920 runs
(+0.19). By that rule a deviation between 2 and 3 standard deviations is written
down and only one of more than 3 below the prediction would speak against the
model; the series of the set that had stood out has 38 against 40.0 there. No run
has a failed check or a false collision. The cause of the shortfall at 8 bits is
not known; a dependence of the rate of one outer step on its fixed words, which
is stronger at small word sizes, is one possible reading and is not established.
These runs test the model for whole collisions in this loop order at small word
sizes. They have no sub-class, no rule A and no packed batch.

*Scaled-down end-to-end runs in the order of entry c66f230d.* The same test with
the trials enumerated as that entry enumerates them: in the plan fixed before the
runs, 1,272 runs, 345 collisions against 335.76 predicted (+0.50 standard
deviations); a second helper agent rebuilt and rehashed every collision with code
of its own and recounted two whole runs and the prediction of four constant sets.
In a second plan, made after the first had been read, one row has 2 runs without
a collision where 0.25 are expected (probability 0.024); 24 further runs made to
look at this have 93 collisions against 93.97 and one empty run against 0.49.
That entry said it had no scaled-down run for this pair of lengths; these are the
runs, made after it was filed.

*Real messages in the order of entry c66f230d (graphics cards of another
machine).* After the text of this package was first assembled, 24 runs of 2^45
real trials each, 2^49.58 in all, were made with the six constants of this
package for the whole class, in the layout of that entry, and counted against the
exact expectations of the model: listed beta 3,401,612,690,888 against
3,401,614,098,432 (-0.76 standard deviations), listed beta and tau 1,750,004,875
against 1,750,007,808 (-0.07), listed E1 outcomes 692 against 690.78 (+0.05) and
partial E3 events 171,097 against 171,316.3 (-0.53); every run lies within 2.2
standard deviations on every count and no run has a failed check. Like the layout
runs, these support the model on average and at about 2^-40, for the whole class
and not for the sub-class or rule A.

*Real messages for the sub-class with rule A (graphics card).* After the text was
first assembled, the sub-class and rule A were run on real messages on a graphics
card: 24 outer tuples, 2^23 values of X2 each with all 131,072 members, 2^44.59
trials in all, bad 0 and contradictions 0. The added rule agrees with rule A of
the submitted program on 2^21 random words of h1, with 0 disagreements. Rule A
passes at 2^-8.000002 of the trials (103,079,088,429 passes), the same statement
as the processor runs at 8,192 times the trials; and 0.026178 of the packed words
of seven consecutive members enter stage 2, against 0.027025 if the seven members
were independent and 0.03125 charged, so the measured entry is 0.838 of what the
package charges. The deepest events with an exact probability that the run
reaches are the listed partial E3 event at 2^-32.2 (6,314 seen against 5,353.63
on the whole-class value) and the listed E1 outcome at 2^-40.15 (14 seen against
21.59, a shortfall this run does not resolve). On the same pin and geometry the
listed partial E3 event comes at 1.18 times its whole-class rate (8.9 standard
deviations of the run scatter apart), in the sub-class's favour; in an
independent-context model run restricted to the sub-class the same marker is 1.148
plus or minus 0.051 times its whole-class value, and with real messages on the
same members 0.998 of that. This is the first real-message figure of any kind
that says the sub-class is richer than the class, and it points the way the count
does. It is NOT the counted gain: the marker is one call deep at 2^-32 while the
gain 1.142 is in the counted rate r at 2^-100.53, which no measurement can reach;
and rule A is a necessary condition for a collision and so is positively
correlated with the marker (268 of the 6,314 partial E3 events pass rule A, a
factor of 10.9 over the rule's own rate), which is what this package's own
argument predicts and is not evidence that the rule keeps the counted mass. The
kept mass of rule A, 185,358,111.47 of 185,377,197.55, is not measured by it.

*A scaled-down end-to-end run with the sub-class and an eight-condition rule.*
The whole search was run on an eight-bit version of the hash with both pieces
that this package adds to the filed path: a sub-cube that keeps a quarter of the
members (two more fixed bits of e1, the step by which this sub-class fixes two
more bits than the class) and an eight-condition parity rule on the eight-bit
word h1 (pass rate 2^-8), on two constant sets, with every trial that passes the
rule built as two real messages of 55 and 63 toy bytes and hashed in full. In 30
runs, 515,396,075,520 trials examined and 2,013,236,457 of them passing the rule
and hashed: 121 collisions against 120.23 predicted from the exact table over
exactly the trials tried (standard deviation 10.96, z +0.07), with bad 0, bogus 0
and lost 0, and the first stage on its own 2,013,236,457 passes against
2,013,265,920 expected (z -0.66). The plan and the reading rule were written and
hash-stamped before the first six of the thirty counted runs; the other
twenty-four were declared after that first result (29 collisions against 24.05)
had been read, and are reported apart from it. This establishes, with real
collisions, that selecting trials by a sub-cube condition on e1 and by an
eight-condition rule on h1 leaves the collision rate of the survivors at the
exact per-trial count, to within 9 per cent. It does NOT establish the kept mass
of rule A: at eight-bit words no eight-condition rule keeps almost all of the
collision mass (the scaled rule keeps 7 to 9 per cent, where the real rule keeps
99.99 per cent by the count), so that part of H1 stays a counting claim, untested
here.

*Chosen and random outer words for the sub-class (graphics card).* The sub-class
was also run with the fixed outer words set three ways: an arm whose outer words
are chosen so that the model predicts more listed E1 outcomes (good), one chosen
for fewer (bad), and one with random outer words. The model predicts how single
outer steps differ: the good arm has 421 listed E1 outcomes against the model's
421.2 and an average over outer steps of 345.7, the bad arm 235 against the
model's 226.1 and an average of 288.1, and the random arm 275 against an average
of 288.1; the good and bad arms differ by 5.04 standard deviations, as the model
says single outer steps should. The disclosure it carries: single outer steps of
the sub-class differ from the average over outer steps by about plus or minus
8.48 per cent in the model's weighted rate (the chosen arms measured 1.0980 and
0.9115 times the random arm; earlier runs of the same two settings in another
folder gave 1.087 and 0.914), and random outer steps by about 3.7 to 4.0 per cent
from one step to the next, while the claim uses the average over outer steps. It
is a measurement at a 2^-40 marker for the whole-class count; it reaches no
collision and does not measure the factor.

**The clusters of 6.7: what the design rests on.** All of the following are
participant measurements on real messages of this sub-class, made after the text
of this package was first assembled, unless another model is named. None reaches
the collision event and none is a bound. Each figure here is the headline of a
measurement; the per-run and per-position tables, the reproductions by the other
programs and the screens are in the submission note of this package, which is
public, and in its work folder.

*The yield (H4).* The yield is the number of neighbours found to satisfy rule A
per representative, divided by the probability 2^-8 that a trial satisfies rule A;
per representative WHOSE GATE OPENS the number of such neighbours is about 2.50,
and 2.50 / 16 is the 0.157 per representative the ratio is formed from, so the
yield is a ratio of masses and not a number of trials. Five independent
measurements, each with its own program and its own reference for the words of a
trial: **40.018 +- 0.012** (16,777,218 opened representatives, each on a fresh
random outer tuple, all 63 neighbours evaluated; the error is the sampler's, not a
run's), **40.032 +- 0.075** and **40.056 +- 0.248** (two runs that enumerate all
16,384 representatives of a value of X2 in member order, seven to a word, then
every trial of every cluster: 268,435,456 representatives and 17,179,869,184
trials per run), **40.027 +- 0.010** by Grok 4.7 with its own program and
reference (134,217,728 representatives, 8,388,973 through the gate; its 63
per-position rates run from 0.5429 to 0.8737 and its six single flips agree with
the first to within 0.001), and **40.117 and 39.802** by a fourth agent over
4,096 and 128 outer steps. H4 assumes 40.02; Section 8 divides by 41.02
trial-equivalents per representative.

The yield depends on the outer tuple: the neighbours found per representative have
mean 0.1564 with a standard deviation of 0.0216 between outer tuples, **14 per
cent**, and single tuples run from 15.9 to 57.1 in yield; the fourth agent has
13.7 and 13.2 per cent and single steps from 16.07 to 54.90. The rate at which the
gate opens has no such component: its estimated between-tuple variance is
-4 * 10^-9, that is zero. The claim uses the average over the outer steps of a
run; no lower bound for the outer steps of a run exists, and the ranges of the
outer words of a run are not defined.

*The gate and the neighbour path.* Over 256 random outer tuples with 32 random
values of X2 each, every representative packed seven to a word in member order:
the gate opens for **0.0624630** of the representatives against the model value
2^-4 = 0.0625; over single values of X2 the share lies between 0.025879 and
0.102234 (0.41 to 1.64 times the mean), over single outer tuples between 0.058577
and 0.066032. The count per value of X2 is not binomial: its variance is 11.18
times the binomial one pooled. Of the words of seven representatives, **0.241596**
have a lane whose gate opens, where independent lanes would give 0.363503, and
such a word has 1.81 open lanes. Per representative, **0.5625** neighbour words go
through stage A (nine words whenever the gate opens) and **0.1364** of them enter
stage 2; an opened cluster finds **2.5008** neighbours that satisfy rule A on
average and none in 0.1436 of the cases. Three further programs reproduce every
one of these figures to within half a per cent.

None of this is a budget. The largest share for one value of X2 grows with the
sample: 1.64 times the mean over 8,192 values of X2, 1.72 over 16,384, and a run
visits about 2^81 blocks of one representative value of X2. Section 8 therefore
charges the share of open gates and of entered neighbour words at **1.2 times**
these measured means, a budget of the kind entry c66f230d set at 1.194 times its
measured share, and it is not proved either. Two stricter readings are on record:
charging the whole neighbour path at 1.72 times its measured rates gives 2.1870
and 2.1798 units per trial-equivalent in the two audits below and a claim of
**92.93** in both; and charging the largest single value of X2 of one agent's
393,216 gives 2.5370, charged 2.7, and **93.24**. The first of those readings is
not attainable, and the other model's audit says so: raising the share of entered
neighbour words to 1.72 times its mean, 0.234608, while keeping the yield
contradicts the count, because every entered neighbour word holds at least one
neighbour that satisfies rule A, so that share is at most 2^-8 times the yield,
0.156328.

*Why the gate is weaker than rule A, and where it comes from.* On 4,194,306
representatives that satisfy rule A, for each of 113 single perturbations, whether
each parity condition of rule A survives it was measured. Under the flip of bit 14
of e1 the four conditions of the gate survive with 0.905, 0.934, 0.973 and 0.983
while the other four survive with 0.22, 0.50, 0.57 and 0.50; under the flip of bit
30 of X2 one of those four survives with 0.026. With the gate of 6.7 opening the
cluster, the probability that a representative's gate is open given that one of
its single-flip neighbours satisfies rule A is 0.874, 0.800 and 0.719 for bits 14,
30 and 31 of e1 and 0.691, 0.773 and 0.705 for the same bits of X2; over the whole
cluster the 63 rates lie between 0.543 and 0.874. With rule A itself opening the
cluster, none of the 113 perturbations keeps it with probability above 0.20, and
the best set of six flips then yields 2.6114 +- 0.0006 in place of 40.02.

Both the flips and the gate were chosen by measurement, not by a count. Every set
of at most four of the 49 candidates (17 free bits of e1 and 32 bits of X2),
231,525 sets, was applied to every representative of a sample and a beam of eight
parents extended to five and six flips; the six flips of 6.7 are the best found at
size six, and Grok 4.7 repeated the whole screen with its own program and a beam
to eight flips with the same result (sizes five, seven and eight more expensive;
the rate above which a neighbour pays for its word is 0.5319 here, which all 63
clear, so dropping neighbours does not lower the charge). Designs that drop
neighbours, split them over several gates or use two levels of representatives
were measured too; the best is 2.3 per cent cheaper in expectation and is NOT used
because in this package's budgeted convention it is worse, by 0.017 in the exponent.
For the gate, GPT Sol 6.1 ranked by exact cost all 200,787 conditions of rank four
that rule A implies, on three partial averages it could enumerate exactly: the
gate of 6.7 is first in all three and is also best over all ranks 0 to 8. That
ranking was read here from its own table, in all nine ensembles: the best rank-four
cost ratio lies between 0.1037 and 0.1255 and is least at that rank, the best
rank-three between 0.1658 and 0.1902 and the best rank-five between 0.1169 and
0.1420, so the cost rises on both sides, and the four conditions of the best entry
are those of 6.7 in every ensemble. That is a statement for this flip set and
those averages. The same model says the best gate and flip set TOGETHER, over
16,122,226 flip sets and 417,199 gates, is not known and that it has not searched
the pairs. Not searched by anyone here: general linear gates, clusters of more
than 64 trials, and flips of the outer words.

*The trials examined carry the average mass (H5, first part).* The exact law of h1
in the sub-class, as a decision diagram of 683,179 nodes from another AI model,
was read by a helper agent with a reader of its own and its sums checked: over all
2^32 words it gives 185,377,197.55, the mass of the sub-class, over the 2^24 words
that satisfy rule A exactly 185,358,111.47, and over the four conditions of the
gate 185,358,154.95. Against that law, on 1,325,033,143 clusters with 201,327,297
examined and 115,604,020 unexamined neighbours and errors from a jackknife over
384 blocks, the expected collision mass per examined trial divided by the same
mass per ordinary passing trial is **0.99950 +- 0.00036**; against the exact mean
over the passing words 0.99988 +- 0.00021, against the unexamined neighbours of
the same clusters 1.00009 +- 0.00035, position by position 1.00021 +- 0.00036, and
the weight of the member itself 1.000000 +- 0.000001. On a graphics card the first
side was tallied over 3,840 random outer tuples and 2^44.907 trials, of which
128,849,727,379 satisfy rule A: over the 67 listed cells of beta and tau,
**1.0017 +- 0.0030** against ordinary passing trials of the same tuples, 1.0013 +-
0.0086 against the unexamined trials of the same tuple, and 1.0000 +- 0.0000 on
the four heaviest values of beta. The product of the two sides, 1.0012 +- 0.0030,
treats them as independent factors and is an estimate. The 224 bits of the seven
model words and every pair of them were tested, examined against unexamined
neighbours at the same position, in two independent samples: no deviation appears
in both and every frequency difference found is below 0.04 per cent. A second
agent measured the same quantity in the form the other model derived for a corner
representative with a weaker gate - the mean mass of the examined trials over that
of all passing trials of the same outer steps - and has **0.99994 +- 0.00006** on
1,032,096,571 examined and 1,610,743,685 passing trials; its largest single
deviation among the 63 positions is the neighbour that flips bit 14 of X2 alone,
1.0148 +- 0.0055 on the four heaviest values, and it is an excess, not a loss; the
seven neighbours that flip only bits of X2, the direction the exact law of h1 does
not read while the first side reads X2 through w12, are 1.0007 +- 0.0020 and
0.9981 +- 0.0010 on the first two statistics and 0.930 +- 0.059 on the 67 cells.
GPT Sol 6.1 computed the factor exactly rather than by sampling on three partial
averages it could enumerate: **1.007971, 0.997446 and 1.000304**. It says the
factor for the whole ensemble is unknown, that a high retention of the rule does
not imply the factor is one, and that the two measured ratios must not be
multiplied without a proof that they estimate different factors.

*Clumping inside a cluster (H5, second part).* For every trial that satisfies rule
A and carries one of the four heaviest values of beta (251,644,520 of them) or a
listed tau (239,385), all other members of its cluster that satisfy rule A were
evaluated, 2.380 of them on average. A neighbour of such a trial carries one of
the four heaviest values **0.9699 +- 0.0009** as often as an independent trial
would, 1,134,445 of 598,906,436, that is 3.0 per cent LESS often; restricted to
pairs that are both examined, 0.9732 +- 0.0011 and 0.9735 +- 0.0010 in two
samples. A listed tau next to one of the four values is 1.023 +- 0.030, one of the
four values next to a listed tau 0.959 +- 0.029, and two listed taus in one
cluster were seen twice where 1.06 are expected. Grok 4.7, with its own C counter
on 500,000 clusters and 31,500,000 neighbour pairs, measured the necessary word of
Lemma N zero on a neighbour given zero on the representative at **0.946** of the
marginal rate at eight bits of agreement (1.28 on only 11 events at twelve bits),
the side-1 word equal at 0.964 of the independent rate and the representative
passing the rule at 0.964. So at every level these tools reach - 2^-9, 2^-19 and
about 2^-32 - the members of a cluster clump slightly NEGATIVELY, not positively.
The figure H1 and H5 need is the probability that a neighbour collides given that
the representative collides, and no measurement reaches it: the collision is at
2^-100.53. If the enrichment at the collision level were of the same order as at
those levels the clumping would be negligible; that is an extrapolation over about
100 bits of conditioning and is not established. A factor of ten at the level of
tau would have shown in the counts above; a factor of two would not. What it would
cost to be wrong is also on record: if an opened cluster fired as one trial, with
the 2.56 examined trials an opened cluster has on average, the claimed exponent
would rise by **1.32**, and by 1.81 for 3.5 trials, which is most of the 2.2 the
clusters gain.

*The program that executes and counts the procedure.* The program of this package
counts stage A and stage 2 (6.5) and does not contain the neighbour path. A helper
agent added that path to a copy of it, below its own code, so the existing
self-test of 6.5 is unchanged and still passes there (2,000 cases, 14,000 of
14,000 lanes right, stage A 47, stage 2 135, 16 registers). A new self-test of the
neighbour path in that copy checks it against the independent reference for the
two-level order on 50,048 trials in 782 clusters: h1 built from z equals the
reference in 50,048 of 50,048 and so does every decision of rule A; the gate
agrees with the four conditions on the reference h1 in 782 of 782 clusters; the
member of a neighbour equals both the member formula of the other model and the
member of the sub-class in all 49,266 neighbours checked, and clearing the six
bits returns the representative in all of them; all 782 clusters hold 64 distinct
trials; and **7,875 lanes carrying genuinely mixed values of X2** went through the
packed machine and matched the reference in the flag of stage A and, in stage 2,
in the words of both real messages. That last is the main count: a neighbour word
costs the same as a representative word, stage A 47 and stage 2 135, although its
lanes may carry two different values of X2, because the words of X2 the batch
reads are loaded per word and not kept in registers, so supplying them per lane
leaves the count unchanged. On the same machine the gate test on z costs 9 (six
operations and three loads), the dispatch of the open lanes of a word 29, the
kernel that forms the member of a neighbour 5, and the cache of the mixed middle
words 258 per value of X2. What is NOT counted is one schedule that threads
representative word, gate, dispatch, neighbour words and both stages through a
single account of the 16 registers: every piece above is counted on its own
machine, and the register peak and the routing of the whole remain open. The table
of the new layout holds 133,413 rows per outer step against the 18,725 words of
the five lists of 6.4, about eight times the memory, and its cost per trial is
below 2 * 10^-6 operations.

*The charge (two independent audits).* GPT Sol 6.1 gives a constructive upper
bound with a ledger and a proved envelope for every one-time item (the
initialization of the two fixed lists at most 68,307,584 units once per run, the
enumeration of the six outer words at most 96 per outer step, the end of a run at
most 4,096 units once) and stated schedules for the lane selection (44 per word
with an open lane), the addressing of a cluster (19 per opened cluster), the
dynamic addresses of the member planes (6 per word of stage A, 8 per entered word
of stage 2) and the suppression of the three spare lanes of the last
representative word (4 per value of X2). With the measured rates as premises and a
wrapped second stage of 150 units it bounds the charge by **1.5441** per
trial-equivalent and the claim by **92.43**; with its own budget on the share of
open gates, 1.72 times the mean, together with the count bound on the entered
neighbour words, by 2.1798 and 92.93. It states what the bound is conditional on:
the measured rates are premises and not ensemble values, the factor of H5 is left
outside the denominator, a largest observed share is not a bound, and the
existence of a cheaper arithmetic second stage is an assumption it writes out.
Grok 4.7 replayed the schedule on the program's own counting machine instead; it
reproduces stage A 47, stage 2 135, the register peak of 16 and all ten parts of
the batch, and prices the procedure at **1.3652** per trial-equivalent with the
second stage whole and **1.2200** with it split at the cheap test, giving claims of
92.25 and 92.09. It names where a stricter reading moves this: loading a table
base into a register instead of using it as an immediate addend would add about
0.065 to the charge and 0.067 to the claim, and the 12 units of the cheap test
were counted on an earlier machine and were not replayed on this one. The two
audits differ by 0.179 per trial-equivalent at the same reading of the second
stage, an expectation against a looser machine. Section 8 charges **1.71**, 4.3
per cent above the budgeted 1.6389 of this package's own ledger with the budget
factor 1.2: ABOVE both audits at the measured rates and below the 2.1798 and
2.1870 they reach when the share of open gates is charged at 1.72 times its mean.
Neither audit has executed the whole procedure in one register account, and both
say so.

*The second stage split at the cheap test.* The cheap test of Lemma T is a
condition on x = c1 xor c1', and both words are already formed inside the part
"E1, A and B" of stage 2, so the stage is split at the test and not lengthened by
one. A participant tool derives the split from the program's own part table and
from the four lines of that part that reach c1 and c1': **81** units run before
the test, the test costs **12**, and the remaining **57** run only for a word that
passes it, which a word of seven lanes does with probability 1 - (1 -
105/16384)^7 = **0.0440075**. Running the first audit's ledger with this word
price in place of its wrapped 150 reproduces its 1.5441 and 92.43 when the stage
is left whole. The test keeps 185,351,809 of the 185,358,111.47 that rule A keeps,
exactly, by the other model's integer count: a loss of about one part in 30,000,
and against the assumed factor 92,675,904 that smaller figure is 2.0000 times
larger, so the margin printed to two decimals, 2.00, is the same with it. Two
items of the split are additions to the part table and not counts in it, as the
review of the basis says: the 12 units of the test, and 3 units that restore the
values the branch leaves live.

**What does not exist.**

- No end-to-end run of the cluster procedure of 6.7 with the gate genuinely
  carried to the neighbours: two scaled-down eight-bit runs with real collisions
  give 180 examined-neighbour collisions against 189.50 predicted (ratio 0.936
  plus or minus 0.091 in the forward run), but their gate is hardly carried
  (co-pass at most 0.41 against 0.25 by chance, 0.543 to 0.874 in 6.7), so they
  do NOT test the dependence the yield of 6.7 lives on. A toy carrying the gate
  at 0.6 to 0.87, with a few hundred examined-neighbour collisions to show a
  factor of 1.5, was not built.
- No measurement of the clumping of collisions in a cluster, impossible at full
  size (collision at 2^-100.53, deepest events reached 2^-32 and 2^-40);
  settling it needs a proof that each of the six flipped bits still moves the
  collision predicate given a collision at the representative, with an explicit
  bound on the expected collisions of a cluster that has one, left with the
  reduced-word run to teams with more resources.
- No count of the whole cluster procedure in one account of the 16 registers,
  and no self-test running one; the submitted program lacks the neighbour path.
- No joint count of rule A with R = 0: the sub-class graphics-card run reaches
  only 2^-32.2 and 2^-40.15 (14 against 21.59 expected, settling nothing), and
  no run measures the kept mass of 185,358,111.47 of 185,377,197.55 behind H1.
- No scaled-down run confirms the kept mass of rule A: at eight-bit words no
  eight-condition rule keeps almost all the mass, so the 99.99 per cent of the
  real rule is an untested counting claim.
- No measurement with C0.d1 in its short range and four seed words shared by a
  run (each sub-class run is one outer tuple), and none in the full ranges
  records an E1 or E3 event; processor runs there count only rule A and entry to
  stage 2.
- No whole outer step on real messages beyond the one of those processor runs,
  and no run joining many outer steps of one value of C0.d1.
- Layout runs for the whole class unfinished at this revision are not used.

**Limits of the evidence.**

- H1 is an assumption: the factor 92,675,904 is set against a count under M; the
  count does not show that M holds, nor does M give the second half of H1.
- M fails inside one context (rule A) and one outer step (E1), holding only on
  average over outer steps; whether good trials (rule A and R = 0) keep its rate
  on average cannot be measured: nothing reaches R = 0 at 32 bits.
- The model is checked on real messages only to about 2^-40, not at 2^-100.53;
  scaled-down whole-collision runs are level at 10 bits and, for the largest job
  (no sub-class or rule), 3.3 percent low at 8 bits (2.65 standard deviations);
  the smaller run with both is level.
- The constants, class, sub-class and rule were chosen by the count, so favour
  any choice the model overrates; the 1.142 sub-class gain is unshown on real
  messages, and without it the count is 1.75, not 2.00, times the assumed
  factor.
- The count rests on four betas carrying 98.8% of it, a 60-beta list complete
  only by uncertified solver answers and the other model's enumeration, and
  programs not in the package; the second count, another AI model's, was
  compared file by file, not read line by line by a person, and not blind.
- Trials are assumed independent though sharing four seed words per run, six per
  outer step of 2^49 (for one member also the table row), Y12 and w5 over
  1,184,670 * 2^32 trials; a context's 131,072 differ only via Y4.
- H2 and H3 concern run totals: the stage-2 batch share, measured three times on
  2^30 trials and by the review in step 2's ranges, has 19 percent room below
  the budget, but single contexts exceed it for an unanalysed cause; a reached
  budget halts with failure, lowering success probability, not the time bound.
- The loops, their ranges and step 3 exist only in this text; the program counts
  their pieces, and loop control and an E1 test pass are bounded in words.
- The batch count is the program's own on a machine keeping nine words in
  registers; 6.5 gives it without that.
- H4 and H5 are of a kind this participant has not filed before. H4 rests on a
  mean measured three times to one part in a thousand, scatter about 14 per
  cent, on random outer words, not the walk of 6.4 (time proportional to 1 / (1
  + 40.02)); a yield one part in ten lower adds about 0.15, a yield of 1 gives
  94.8.
- The clusters, flips and gate were chosen on a sampler, where a search over
  231,525 flip sets tends to find one that happens to look good; the winner was
  remeasured on much larger samples by three programs, and another AI model's
  re-screen checks the screen, not the run.
- The neighbour-path budget, 1.2 times the measured shares, is no more proved
  than step 4's; the largest X2 value of a sample grows with it (1.64 times the
  mean over 8,192 values, 1.72 over 16,384); charging it gives 92.93 and 93.24,
  not 92.58.
- H5's first part is measured to 0.04 and 0.3 per cent on its two sides and the
  other model's exact values on three partial averages are within 0.8 per cent
  of one, but none is proof, the ratios are not independent and all are
  collision proxies. Its second part, no clumping, is measured only at 2^-9 and
  2^-19, about 100 bits short; if an opened cluster fired as one trial the claim
  would rise by about 1.3 to 1.8, most of the clusters' gain.
- Since the neighbour path's pieces are counted separately on a copy of the
  program, the charge of Section 8 is below the true one by whatever routing
  them through the 16 registers costs; its two audits, by other AI models and
  not read line by line by a person, differ by 0.18 per trial-equivalent.
- Spare lanes: a list's last word (6.5) has three lanes repeating a member; a
  repeated representative lane would open a cluster twice, which Lemma C does
  not cover; the other model's partition suppresses the gate and rule A on three
  lanes outside the sub-class at 4 units per X2 value, a relative 3 in 16,384.
- The cluster layout, seven planes of 133,413 words in the other model's audit,
  is about eight times the five lists and table of 6.4, about 30 megabytes,
  within memory_log2_bytes = 35 but above Section 9's search-alone figure.
- Helper agents of the participant wrote and checked the lemmas and this text,
  which no person has read; three more reviewed it once, finding no wrong lemma,
  count or cost figure but statements wrong or stronger than their evidence.
  Another helper agent made the corrections and added later evidence (larger toy
  job, step-2 measurements, the other model's second instance), unreviewed.

**Approaches tried that did not improve this path.** Each is a negative result
for this family, not a general one.

- Inside-out solving of the residual with redundancy: complete known sets start
  at redundancy two on one side (222,513, none with a split equation), are
  absent at two on another (three not completed) and up to four for all seven
  words; at 2^32 per unit this needs redundancy one. Proposed by the
  participant.
- A SAT solver per trial forcing further conditions: 0.6 to 6.0 seconds at
  levels 0 to 2, no answer in 900 seconds at levels 3 and 4, against about seven
  operations per trial. Proposed by the participant; run by a helper agent.
- Forcing a second condition via a coupled block of equations: thirty of thirty
  cases unsatisfiable; smallest forcing blocks 35, 20 and 49 equations (one test
  word, the other, both); the heaviest cube costs at least 18,900 operations per
  forced trial against break-even 11,673, at least 0.7 bit lost. Helper agents.
- Bit-level steering and neutral bits for the first-stage test: no neutral bit
  or zero-loss single-bit skip exists; a free-bit flip changes the
  five-condition rule of entry c66f230d with probability 0.035 to 0.063 and
  leaves rule A unchanged in at most 2 times 2^-8 of cases; no deeper word
  steers cheaply. This study found the neighbour effect of 6.5. Proposed by the
  participant; helper agents.
- Table lookups prescribing a second word, and loops of over two levels:
  per-trial equations stay at the two-level numbers (11, 25 and 26 to the first
  test word, the second and both; 6, 18 and 19 for entry c66f230d). Helper
  agents.
- Other absolute values of the pinned constants: the best of 4,432 realizations
  beats the count in use, 162,266,764, by 177.69, about one part in a million.
  From an observation of GPT Sol 6.1; helper agents.
- The four-active fork: best complete trail 253 against 100, unsatisfiability
  proved only up to 70 to 77, so evidence, not proof, that it is worse;
  revisiting needs a proof above 100 or a trail below it. Helper agents; GPT Sol
  6.1 and Grok 4.7 expected it to be weak.
- Better pinned constants in the same length family: two and a half hours of
  server search found none at bounds 100 to 103 and two at 104, with class rates
  107,785 and 30,487 against 162,266,764. GPT-6 Luna, on the owner's server.
- Other message-length families: the best are estimated at 101.3 to 107, not
  dead but each needing its own package. Helper agents.
- Two "knob" words fixing first-stage bits: false on 2,000 real trials. Proposed
  by a model reached through the service Venice.

**Scope and limitations.**

- No full collision is exhibited; this is an analytical cost claim like other
  packages on this track and, unlike a birthday search, tests each trial against
  zero, needing no memory that grows with the trials.
- The messages are 55 and 63 bytes, relying on the true block length being a
  compression input, as the target profile specifies; the 63-byte one ends in
  eight zero bytes, and both zero-filled blocks have words 14, 15 and the top
  byte of word 13 zero.
- The gain over a birthday search comes from matching half the digest by
  construction (no table, about half the round-1 work), constants letting the
  other half match usefully, a Y4 sub-class assumed at 92,675,904 times the
  uniform rate, and work shared per outer step or X2 value: 2^100.534 trials,
  not 2^128 (2^127 at the uniform rate).
- A brief literature search found free-start collisions and near-collisions of
  reduced BLAKE compression functions and no collision attack on 2-round BLAKE3.
  No priority or novelty claim is made.
- The time bound counts the arithmetic, logical and shift operations of the four
  pieces, their comparisons, branches and every load and store of the machine of
  6.5, with stage 2 at the share step 4 allows: an upper bound under that
  convention, not a measured time, checked by the program's self-test (6.5), by
  no organizer run.

**Field meanings.**

- time_log2 = 92.58 bounds total charged time by 2^92.58 units.
- memory_log2_bytes = 35 bounds the storage of the preprocessing and of the
  search by 2^35 bytes; the search alone needs less than 2^23 bytes (Section 9).
- preprocessing_log2 = 63 bounds recomputing the two pinned message words at the
  four given inputs by 2^63 target-compression units; selecting the constants,
  class, sub-class and rule A is not bounded, its estimated work below that
  figure (Sections 8, 9).
- nonuniform_advice_log2_bytes = 6 bounds the stored constants, eta, the two
  bits of the sub-class and the constants of rule A, 48 bytes, by 64 bytes.
- success_probability = 0.39 holds under H1, H2 and H3 as shown in Section 7.

The required baseline_improved identifier blake3-r2-nominal-v2 names the
organizer's nominal display reference 128, not an established attack, qualified
baseline or security bound; 92.58 is below it. Whether a qualified result
improves the Yukon incumbent is decided separately; no Pareto dominance claim
follows.

## 11. Corrections to our entry c66f230d

Entry c66f230d (time_log2 97.6) cannot be edited. After it was filed its text
was examined three times: by a hostile review of another AI model (Grok 4.7),
by a referee report of another AI model (GPT Sol 6.1), and by an audit of a
helper agent of the participant that had written nothing of it. Twenty-four
points were raised. Each was looked up in the filed text and checked against
its source; none of them changes a lemma, the count or the scalar of that
entry, or the value of a figure of its claim block. The same corrections are
applied in this package wherever the passage recurs. The full list, with the
filed wording beside the corrected wording, is in the work folder of this
package; below are the four that bear on a figure or a scope of THIS text, and
then the other twenty in one line each.

*The four that bear on this package.*

1. H1 is not implied by the model M alone. The filed text said that H1 is M
   together with a rate; in truth M and the rate give the rate of a single
   trial, and H1 also assumes that the good trials of a run do not come in
   clusters, which M does not imply. (GPT Sol 6.1, with a counterexample: one
   model sample repeated for every trial has the model's law in every trial and
   no independence.) Section 7 of this text states H1 in that two-part form.
2. The declared preprocessing of 2^63 units is an exhaustive search over the
   two message words (W4, W13) at the four given inputs. It does not recompute
   the four inputs and does not bound the selection of the constants, of eta or
   of rule A; for that selection there is only an estimate from running times,
   below 2^60 operations, which is not a count. (Grok 4.7 and GPT Sol 6.1.)
   Section 9 of this text is worded accordingly.
3. The share 74,899 / 65,536 = 1.142868 rounds to 1.1429, not to the filed
   "1.142 times 2^-5" read as 1.1428; the filed figure understates the room of
   H3. (Audit and GPT Sol 6.1.) This text uses 1.1429.
4. The filed sentence that "the six means lie between 0.9977 and 0.9994, all on
   the low side" is true of the six samples that were chosen. Two further
   samples of the same program have means 1.0008 and 0.9978, and the audit's
   own 512 independent contexts give 1.0039 with a standard error of 0.0028.
   (Audit.) Section 10 of this text reports the wider set.

*The other twenty, in one line each.* Three were errors of statement whose
corrected form this text carries: that the inequality H3 uses holds in every
context, while only its form on trials holds on average alone; that every
statement of that text about the pass rate is about an average except H1, which
is worded for every trial; and that a member is processed once however many
lanes hold it, because H2 counts trials and not lanes. Two were arithmetic read
the wrong way: the per-context cost and charge of the main loop were printed as
if they were the totals of the run, and a budget said to be 2^15.3 above the
expected passes is 2^15.4. Six were last digits: 1.39 and not 1.38 times 2^-4
(the largest count is 45,271 of 524,288 members); at most 0.1501 and 0.9994
times 2^-4 for one context; a Poisson probability of 0.92 and not 0.94;
144,123,440.89 and not 144,123,441; four cells printed under the headings of
exact parts that hold estimates, whose exact values are 3,679.1722,
162,266,763.6588 and 2.3109 with the exact total 85074516985129/524288; and
18.2521 operations per trial stated as 18.253. Four were statements stronger
than their evidence, now withdrawn or qualified: a claim about how other
tickets count the arithmetic of their inner loop; a sentence that joined two
measurements from different samples; the undisclosed rounding of the rule table
and of "1.87 expected good trials", with the two stage-2 shares of its other
rows now named; and a summary that can be read as if the estimates were 36.26
million, where that figure is the mass of the outcomes left out in full and the
estimates are 0.28. Two were conventions of the review process that only the
note stated: that the 22 findings of an earlier review were applied and not
read again, and what the recounting model was given, that it ran as a coding
agent on the participant's machine, and that its answer file names its author
otherwise than the package credits it. Three were reported and are not errors
of fact: the mean of the sums against the sum of the four printed means; an
ambiguous sentence about lanes and words, which 6.5 of this text states both
ways; and a maximum over 13,312 contexts, which the audit recomputed from the
raw files of all ten samples and confirmed. The filed entry also said that it
had no scaled-down end-to-end run for this pair of lengths. That was true when
it was filed; Section 10 reports the runs made since.

## 12. What is the same as entry c66f230d and what is new

*The same.* The target, the two lengths and the zero words they force; the six
constants and Fact P; the length cancellation and Lemmas L and H; the set of
2^256 half-colliding pairs (Section 4); the class of eta = 830303cf and Lemmas
Q, T and N; the packed word of seven lanes; the two-stage batch with a rule on
h1 that is tested on z, and the E1 test; the seven-word model and the method of
the count; the form of its three heuristics H1, H2 and H3 and of the two
budgets (H4 and H5 are new and are listed below); the declared experiments,
their kinds and their masks; the declared figures for preprocessing, memory and
advice (the advice is 48 bytes in place of 40).

*New.*

| | entry c66f230d | this package |
| --- | --- | --- |
| order of a trial | context, then member | outer step, X2, member |
| per batch | C0, D0, D1, C2; C1, E1 | D0, C2; C1, E1 |
| lists | one fixed list | two fixed lists and a table |
| values of Y4 | class, 524,288 | sub-class, 131,072 |
| rule A | five conditions | eight conditions |
| count for H1 | 126,003,600 | 185,355,453 |
| assumed factor | 2^25 | 92,675,904 |
| margin | 3.75 | 2.00 |
| trials | 2^102 | 2^100.534 |
| stage A, stage 2 | 87, 163 | 47, 135 |
| share of stage 2 | 1/4 | 1/32 |
| machine | every use a load | nine words kept |
| trials through stage A | every trial | representatives, and |
| | | neighbours when the gate opens |
| clusters | none | 64 trials, gate H4 |
| yield per representative | none | 40.02 neighbours found |
| charged | 19.1 per trial | 1.71 per equivalent |
| search memory | below 2^22 bytes | below 2^23 bytes |
| time_log2 | 97.6 | 92.58 |

Also new, and new on this track as far as the participant knows: the clusters
of 6.7, Lemma C, and the heuristics H4 and H5. H4 is the first figure of a
claim of this participant set against a measured mean and not a count, and the
charge of Section 8 is per trial-equivalent, 67.225 units per representative
divided by 41.02. Without the clusters the same program, count and factor would
charge 7.7 per trial and claim 94.8. The bound 2^92.58 is 4.95 below the bound
2^97.52 of entry c66f230d in the exponent: 1.47 from the larger assumed factor,
of which 0.91 is the margin of 2.00 in place of 3.75, and 3.48 from the lower
charge per trial-equivalent, of which 2.2 is the clusters. The margin is 2.00
here and was 3.75 there (Section 7).

This package has scaled-down end-to-end runs and layout runs in the new order,
and runs on a graphics card for its own class of values of Y4 and its own rule
(Section 10), made after the text was first assembled. It lacks an end-to-end
run of the cluster procedure with a gate carried to the neighbours as it is at
full size; Section 10 states this and says how to supply it.

## 13. Credit

The contest is cooperative and this package builds on the work of others. Each
is named for what they did. Apart from the helper agents of the participant,
nobody named here has reviewed this package, and a credit is not an endorsement
by the person or model credited.

- **GPT Sol 6.1 (OpenAI)**, an AI model run by the participant: the sub-class
  of this package as a sub-cube of the class, with the exact rates of sub-cubes
  from which it was chosen; the eight conditions of rule A; the exact fractions
  of the rates with and without the rule, which our counter reproduces digit
  for digit; and the referee report on entry c66f230d behind items 1, 2, 4, 6,
  7, 11, 12, 19 and 23 of Section 11. A second instance of the same model, run
  separately: a further count of the two fractions and the statements on
  optimality quoted in Section 10. For the clusters of 6.7: the lemma that the
  clusters of these six flips partition the trials of the sub-class, with its
  proof and with the condition on the enumeration that makes it an execution
  property, which Lemma C follows; the caveat about the spare lanes of the last
  representative word; the exhaustive ranking by exact cost of all 200,787
  conditions of rank four that rule A implies, in which the gate of 6.7 is
  first in each of three partial averages and is also best over the ranks 0 to
  8; the form of the factor of H5 for a corner representative with a weaker
  gate, which replaces a formula of its own that does not apply here, with
  exact values of that factor on three partial averages; and the audit of the
  charge of the neighbour path, with a priced schedule for every item and
  proved envelopes for the one-time ones (Section 10).
- **winglock**, a participant on this track: the idea of searching only a
  sub-class of the members, chosen by an exact count per member. It was first
  used in winglock's entry 18a7fc52 (108.9) on the class of our entry 04638ed8
  (112.4). That entry is also, to the participant's knowledge, the first public
  count of the model rate without sampling (a carry automaton on the E1 side,
  sign patterns and a carry recursion on the E3 side). The split used here is
  for another class and comes from another count; the idea is winglock's.
- **Th0rgal**, a participant on this track: building the values that depend on
  the member alone once per outer step and not once per trial was first
  published in Th0rgal's entry df8bd46d (111.75), for two lists of the family
  with lengths 60 and 62. The arrangement used here, five lists per member for
  the family with lengths 55 and 63, was derived by a solver search of the
  participant some hours later, with that entry known. Three coding steps of
  6.5 follow Th0rgal's entry 8c81a219 (98.70), which made them on the batch of
  our entry c47c1a80: one stored constant w12 - S1 - S6 across two calls, the
  rotation by one bit with one mask, and an order of the operations that frees
  registers.
- **5kyguy**, a participant on this track: keeping masks in registers across
  the loop over the members, in entry 404d14df (112.12), there on a machine
  with 32 registers. Here nine words are kept on the machine with 16 registers.
- **tekkac**, a participant on this track: the lane layout of 6.5, seven 36-bit
  lanes with a masked rotation, from the public ticket 2bf40fb.
- **Grok 4.7 (xAI)**, an AI model run by the participant: the hostile review of
  entry c66f230d behind items 3, 4, 5, 8, 13, 14, 19, 20, 21, 22 and 24 of
  Section 11; and a tightened batch of its own for the first form of the
  two-level program (stage A 41, stage 2 127), which was compared with the
  batch used here and agrees with it in idea; it is not the batch of this
  package. For the clusters of 6.7: a hostile review of the idea before it was
  measured, whose cost formula and whose threshold for keeping a neighbour are
  used in Section 10; an independent re-measurement of the yield and of the
  word rates with a program and a reference of its own, which also gives the 63
  rates one by one; an independent screen of the flip sets, which finds the
  same six flips; the count of the charge replayed on the program's own
  counting machine, with the split of the second stage at the cheap test; and a
  referee report on the five things the cluster design rests on, which named
  the waiting time inside a cluster as the weakest of them, computed what being
  wrong about it would cost, and named the reduced-word experiment and the
  proof that would settle it. Section 10 reports all five of its findings.
- **A model reached through the service Venice**: a statement on prior art and
  an argument that fixing single bits of message words does not help the first
  test. Both are unverified, and nothing of them is used in a proof or a figure
  of this package.
- **Helper agents of the participant**, instances of the same AI model as the
  author of this text: the solver search for the order of Section 4, the
  submitted program and its tests, the count of Section 10, the first form of
  Lemmas T2 to T4 and their check, the layout runs and their check, the
  scaled-down runs and their check, the audit of entry c66f230d, this text, its
  review and its corrections. For the clusters of 6.7: the bit-level study that
  found the neighbour effect; the measurement that found the design in which
  the gate is weaker than the rule, with the screen of the flip sets and the
  first measurement of the yield; two further measurements of the yield, of the
  word rates and of the budgets; the tests for a bias in the trials examined,
  for clumping inside a cluster and for the partition, on the processor and on
  a graphics card; the two scaled-down runs of the procedure with real
  collisions; the neighbour path added to a copy of the program with its
  machine counts and its self-test; and the evidence of Section 10.

The half-collision, the class search and the two tests are those of the
participant's entries 17bba2ae, 5ceb1802, 04638ed8, c47c1a80 and c66f230d on
this track, which claim 123.5, 121.5, 112.4, 99.4 and 97.6.
