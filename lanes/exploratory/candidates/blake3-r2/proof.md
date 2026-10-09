# The chunk counter on the 62/64 length pair with an exact fixed pin for 2-round BLAKE3

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
separately reported resource bound.

This exploratory package targets blake3-r2-prefix-v1. It records a distinct
attack path at its own price, time_log2 = 109.2779. The path is the
chunk-counter search of the participant's 55/63 entries, moved to the block
lengths 62 and 64. It uses a length cancellation in the round-0 call K2 that
needs an even difference of the message words (Lemma L62), six fixed 32-bit
pin words for which the round-1 call C3 gives equal b and d outputs on both
messages (Fact P62), two more free message words, w14 and the low half of w15,
a 20-bit class of eta = 85492711, a 16-bit cube of beta = f5519714 and two
outcome rows of E1 and E3. Every algorithm of the path is specified here and
every lemma it uses is proved here: the row equations (Lemma RES, 10.2), the
two existence filters with their automata and their necessity (Lemmas NEC and
AUT, 11.2), and the joint solver with its forced positions, its two-seed
traversal and its listing of every root (Lemmas CR, FM and LS, 11.4). The text
has an exact part and a heuristic part, and keeps them apart. Section 15 lists
every premise and the status of its evidence.

**Exact part.** For every choice of seven outer words, a word r, a word z below
2^16, a word y whose e = Y3 + y + z lies in the class of eta (2^20 values) and
a word c1, an explicit construction (Section 9) gives a counter t, a 62-byte
string A and a 64-byte string B. When t is not zero, F || A and F || B, with F
a string of t full chunks of 1,024 bytes, are messages of 1024 t + 62 and
1024 t + 64 bytes whose last chunks are A and B; the 2-round compressions of
these last chunks, with chunk counter t and flags 3, give chaining values that
agree on their words 0, 2, 5 and 7 (Theorem C62). There is no search in this
and no probability. In the organizer's tree mode the digest of such a message
depends on F and on the chaining value of its last chunk alone (Lemma TR,
Section 7), so a pair whose last-chunk chaining values agree in all eight words
is a collision of two complete messages. The counter t is solved per trial from
the round-0 call K0, as in the participant's 55/63 counter entries, and the
prescribed word is E1.c1; when c1 lies in a cube of 2^16 words, the first-half
b difference of E1 is beta (Theorem C62 (iv)). The pin words are W4 = a40d3321,
X3 = 435d473f, X7 = 9895859e, X11 = 9003b0e0, X15 = a7590cb9 and W13 =
b2077fc6; Fact P62 is a finite computation on them.

**Heuristic part.** A collision needs the other four chaining-value words to
agree as well. By Lemma RES that happens, with a given outcome of E1 and E3,
exactly when five explicit word equations hold. Under the counting model of
10.2, the exact local counts of the two outcome rows (Section 10, recounted
independently) give the mass mu = 36583 / 2^121 = 2^-105.8411 per raw proposal
of 2^16 trials, that is 36583 / 2^137 per trial with c1 in the cube. The search
draws B = 50,575,779,322,124,053,188,182,925,749,242 = 2^105.318 raw proposals,
seven to a batch. Two exact existence filters, byte-compiled carry automata on
two words of the proposal, skip proposals that cannot hold a success of the two
rows; for the others a joint solver with a proved cap of 44,543,808 machine
units lists the trials that complete the collision. Every budget is a halt and
is charged at its bound. Two premises are declared for the success
probability: H1-62, that the valid trials complete the collision at a rate of
at least 51 * 2^-128 each (five sevenths of the model rate, rounded down) with
weak dependence; and H4-62, that the two filter budgets suffice. Under the two
the search succeeds with probability at least 0.39. The pin, the class, the
cube, eps and the two rows are a fixed record of 76 bytes (Section 12); the
success analysis uses only properties of that record that this text verifies
exactly (Lemma ADV).

**The record and its selection are charged.** The search reads the record as
nonuniform advice. The computation that found it is written out as a
procedure, SEL (12.2), whose every program run halts at a stated cap of
operations; its whole capped cost, S_SEL = 6 * 2^58 + 2^50 word operations, is
charged as preprocessing and is included in the time bound, and so are the
tables (2^29 units). The charged time is

    T <= (O_run + S_SEL) / 430 + 2^38 = 2^109.2778200...,

with O_run = 338,353,089,784,844,219,711,771,094,306,765,632 machine units
(Section 13), and the claimed scalar is 109.2779, checked by integer 10,000th
powers.

**What the organizer-run program does.** The two declared experiments and their
program, experiments/halfsearch.py, are those of the participant's entry
26ebba63, unchanged. They run the root instance of the participant's 55/63
construction: single chunks of 55 and 63 bytes, compressed with counter 0 and
flags 11 (Sections 3 to 6). The program does not run this path: nothing of the
62/64 construction, the pin, the class, the filters or the solver is in it,
and no implementation of any part of this path has been run. The
participant's local exact counts of Section 10 and the runs of SEL were made by
programs that are not in the package. No full 2-round collision is exhibited.

*How this text is arranged.* Sections 1 to 7 are taken from the participant's
55/63 counter text; only cross-references, the sentences that named the claim
of that text and a closing note on the lengths 62 and 64 in Section 7 are
changed. Sections 1, 2 and 7 (the compression, the inversion of one call and
the tree lemma) are used by this path; Sections 3 to 6 describe the 55/63 root
instance that the organizer-run program builds, and they are kept because the
experiment manifest refers to them. The path of this package is Sections 8 to
15.

## 1. Exact complete hash on the messages used

H is unkeyed BLAKE3-256 with only rounds 0 and 1 kept in every compression.
Every message of the root instance (Sections 4 to 6) has n = 55 or n = 63
bytes. A message of n <= 64 bytes is one chunk consisting of one block, with no
parent node, so H evaluates exactly one compression. The block is the message
followed by 64 - n zero bytes, used only for loading words. The compression has
flags CHUNK_START | CHUNK_END | ROOT = 11, true block length n, and chunk
counter and root-output counter both zero. There is no key and no derivation
flag.

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

*The same compression in a last chunk.* Section 7 and Sections 9 to 11 use the
same compression, with the same names, as the compression of the last chunk of
a longer message, in Sections 9 to 11 with n = 62 or n = 64 (Section 8): there
v[12..15] = (t mod 2^32, t >> 32, n, 3), with the chunk
counter t and the flags CHUNK_START | CHUNK_END = 3, and the output words o[0],
.., o[7] are the chaining value of the chunk (Lemma TR). Nothing else changes:
the IV, the block, the two rounds and the output.

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

This section, Section 5 and Section 6 build the root instance of the
construction, whose messages are single chunks compressed with counter 0 and
flags 11 (Section 1). The participant's 55/63 counter instance was built from
the same constants; the counter instance of this package, which the claim
uses, is built in Section 9 from other constants and the lengths 62 and 64
(Section 8, and 6.4).

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

## 6. The root instance: trials, tests and the counted batch

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
searched and not all of it because, under the counting model of the
participant's 55/63 entries, the rate of
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
true in general: there are solutions of R = 0 with Y4 in the sub-class whose h1
violates rule A. Rule A is therefore a filter that can lose solutions: a word
of seven trials in which no trial satisfies it is dropped, whether or not one
of its trials has a zero residual. How much it loses was counted for the
participant's 55/63 entries: inside the sub-class the rule keeps all but
19,086.08 of the 185,377,197.55 counted, and for the difference beta* that
their counter search uses it keeps all of it, 67,698,688 of 67,698,688, because
in every outcome of beta* every solution satisfies rule A. On the whole class the same eight conditions
would keep less than half of the count; the rule is a rule for this sub-class
only.

**6.4 The root instance and the two declared experiments.** Sections 4 to 6
build the *root instance* of the construction: its messages are single chunks
of 55 and 63 bytes, and the colliding compression is the root compression, with
counter 0 and flags 11 (Section 1). The claim of this package is made for the
*62/64 counter instance* of Sections 8 to 11, whose messages have 1024 t + 62
and 1024 t + 64 bytes and whose colliding compression is that of the last
chunk, with counter t and flags 3. It shares with the root instance only the
compression of Section 1, the inversion of Section 2, the way the outer words
are solved for in round 0 and the solved counter; its constants, its K2
cancellation, its class and its outcome rows are its own (Sections 8 to 10).
The participant's 55/63 counter instance, whose construction and counter batch
are in the program, shares with the root instance the six constants, Fact P,
Lemmas L and H, the class, Lemma N and the machine of 6.5; the sub-class, rule
A and Lemma A belong to the root instance and to the program's counter batch.

The two declared experiments run the root instance of the same construction,
counter 0 and flags 11. An experiment of the organizer's harness returns pairs
of complete messages and tests an event on their two digests, while the
half-collision of the counter instance is an agreement of four words of the
chaining value of a chunk that is not the root. The parent and root
compressions above that chunk mix all eight words, so the digests of a counter
pair are not expected to agree on the masked words, and on two 55/63 counter
pairs with t = 1 they do not (Section 7). No digest experiment can show a
half-collision of a non-root chunk's chaining value. In the root instance the
colliding compression is the root itself, so its half-collision is an agreement
of four digest words, which the organizer recomputes.

- `half-collision` runs one trial of 6.1 per organizer seed: the seven words of
  a context and a member number are taken from the seed, and steps O, M, Y, T,
  S2 and S3 of Section 4 build the pair. Lemma T predicts that every pair
  agrees on digest words 0, 2, 5 and 7.
- `residual-search` runs a search of the root instance at toy scale: per
  organizer seed one context, then the members of the sub-class in the order of
  their numbers from a member number taken from the seed, at most all 131,072
  of them, stopping at the first trial whose residual (3.3) has a zero low byte
  in digest word 1. For the same context it also evaluates the four counted
  pieces of 6.5 on the program's machine and returns their counts as
  observations.

Neither experiment runs a counter construction or its batch, and neither
measures a rate of any counter search; neither runs anything of the 62/64 path
of this package. A search of the root instance over all
contexts is not part of the claim, and this text defines no loops, ranges or
budgets for it.

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

*The two lists.* List word j holds the members 7j, .., 7j + 6 in the order of
their numbers; list word 18,724 holds the numbers 131,068 to 131,071, and the
last of them three times more. For list word j, U[j] holds ROL(y, 7) and V[j]
the word v of Lemma A (c), one member y per lane, member 7j + i in lane i. Each
list has 18,725 packed words, because 131072 = 18,724 * 7 + 4. Both lists are
computed once, from eta, the two bits of the sub-class, Y3 and the rule (Lemmas
Q2 and A). The build of the table reads U; stage A of a batch reads V.

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
context. For list word j and lane i, with y the member of that lane and the
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
the message).

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

- The entry count: the number of words that have run stage 2 is advanced and
  compared with the memory word `stage-2 budget`. In the program that word
  holds the constant STAGE_2_BUDGET, a budget of the program's 55/63 counter
  search;
  in the root instance its value has no influence on any output.
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
constants and into the list V. The words w8..w11 are never formed in a batch.

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
that value: the two masks of the rotation by 16, the two of the rotation by 12,
the two masks of Lemma A (c), ALL, 2^32 - ALL, and the word that has every bit
of the seven lanes except bit 32. Stage 2 needs the registers of the last four
for its own values and loads them again at its end (the part "restore", 4
loads, charged to stage 2). Stage A does not keep z and the third value of C2
in registers; stage 2 forms both again (5 operations and 3 loads, charged to
stage 2). Two registers hold the list position and the entry count for the
whole search. With that, the batch uses all 16 registers, and 15 do not run it,
under the program's convention that the result of an instruction may reuse a
register whose source value is used for the last time on that instruction; if
instead every source stays live until its instruction finishes, the batch peaks
at 17 registers. The idea of keeping masks in registers across a loop is
credited in Section 17. Under the convention of entry c66f230d, with every read
of a memory word charged as a load, the same program counts 57 and 143 for the
two stages (its line `KEPT = 0`); no address arithmetic is charged for the list
and table loads, as in that entry, and with one operation for each such load
the stages would be 50 and 139.

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
comparison with that word and the branch: 14 operations and one load. The loads
of stage 2 are the budget; X6[j], X2 + w7 and w0 for z, and the two mask pairs
of the rotations by 8 and by 7; -X15, S5, X1[j], w3, X13, X9, R[j] and S12;
w12 - S1 - S6, Y12[j], Y11, w5, Y11' and w5 + delta; the mask of the rotation
by one bit, M, the mask of bit 32 and eta; and the four words of "restore": 30.
The count of the middle step is for all 21 lines of step M and its nine stores;
two of the lines (S0 and w1) and the store of w1 serve only the processing of a
trial whose E1 test word is zero and are counted for every value of X2 all the
same.

*The count in the submitted program.* The program of the two declared
experiments, experiments/halfsearch.py, contains the four pieces, the counter
construction and the counter batch of the participant's 55/63 counter search
(not the construction of Section 9 of this text), and the machine that
counts them, a packed word being one integer with seven 36-bit lanes. The
pieces are written only with calls that each add one operation (an addition,
XOR, AND, OR, shift, comparison or branch), one load (a fetch of a memory, list
or table word, unless it is one of the nine kept in registers) or one store.
The program always evaluates both stages of a batch, so that stage 2 is counted
and checked for every batch; a search runs stage 2 only after a pass of stage
A. The command

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
step, the build and the middle step have stored is the word of the context, and
both branches are taken exactly when one of the seven words in front of them is
zero. The program prints one JSON line with the counts per part, the largest
lane of a sum per part next to its bound, the registers per piece, the kept
words, the members in the lists, the lanes checked, right and satisfying rule
A, and two complete enumerations: the flags of stage 2 on all 128 patterns of
zero and nonzero lanes, and the flags of stage A on packed words in which every
pattern of the 13 bits of z that rule A reads, with every pattern of the bits
27 to 29 of e1, occurs once in every lane. Its exit status is 0 only if all of
these agree with this section. The same command also runs the counter part of
the self-test, for the 55/63 counter construction of the program, reported
under the key `counter` of the same line, and the
exit status is 0 only if that part passes as well.

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

A longer run of the program as filed for entry 64c075ac, whose part for the
root instance this program keeps unchanged, 1,000,000 cases with seed 61,
reports 7,000,000 of 7,000,000 lanes right, the same counts in every case, the
same registers and a largest sum of 8.349 * 2^32; 27,068 of its lanes satisfy
rule A, in 23,368 batches. Its contexts are random or extreme by design and are
not laid out as a run of a search, and every fourth case is the short last
batch, whose spare lanes repeat a member, so these two counts are not a
measurement of a rate. A participant tool with a second counting machine,
sharing no code with the program's, counts the same operations, loads and
stores for all four pieces and refuses the batch with 15 registers; another
derives the bounds of the sums for all inputs by interval arithmetic and finds
every one below the bound of its part.

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

## 7. The tree lemma: the last chunk decides the digest

The claim is made for messages of more than one chunk. This section shows, from
the organizer's reference code, that for such a message the digest is a
function of the prefix and of the chaining value of the last chunk alone.

The organizer's hash, `verifier/blake3.py`, computes `blake3(data, rounds)`,
with rounds = 2 for this target, by these lines of its code:

    chunk_count = max(1, (len(data) + 1023) // 1024)
    stack = []
    for counter in range(chunk_count - 1):
        output = _chunk_output(data[counter * 1024:(counter + 1) * 1024], counter, rounds)
        cv = _compress(*output, rounds)[:8]
        total = counter + 1
        while total & 1 == 0:
            cv = _compress(*_parent_output(stack.pop(), cv), rounds)[:8]
            total >>= 1
        stack.append(cv)
    output = _chunk_output(data[(chunk_count - 1) * 1024:], chunk_count - 1, rounds)
    while stack:
        output = _parent_output(stack.pop(), _compress(*output, rounds)[:8])
    cv, words, _, block_len, flags = output
    root_words = _compress(cv, words, 0, block_len, flags | ROOT, rounds)
    return struct.pack("<8I", *root_words[:8])

There `_chunk_output(chunk, counter, rounds)` compresses every block of a chunk
but the last, starting from the chaining value IV, and returns the last block
as a descriptor (cv, words, counter, len(block), flags | CHUNK_END), where
flags is CHUNK_START = 1 when that block is the first of its chunk; its last
block starts at `last_offset = max(0, (len(chunk) - 1) // 64 * 64)`.
`_compress(cv, words, counter, block_len, flags, rounds)` is the compression of
Section 1 with v[0..7] = cv and v[12..15] = (counter mod 2^32, counter >> 32,
block_len, flags); it returns sixteen output words, of which the first eight
are the chaining value. `_parent_output(left, right)` is the descriptor (IV,
left + right, 0, 64, PARENT) of a parent node.

**Lemma TR (the last chunk decides).** Let t >= 1 and let F be any string of
1024 t bytes. For a string A of 1 to 64 bytes write words(A) for the sixteen
little-endian words of A followed by zero bytes up to 64 bytes, and CV_t(A) for
`_compress(IV, words(A), t, len(A), 3, 2)[:8]`.

(a) The last chunk of F || A is A, and the organizer's code compresses it once,
as `_compress(IV, words(A), t, len(A), 3, 2)`: the compression of Section 1
with block A, block length len(A), counter t and flags CHUNK_START |
CHUNK_END = 3. It is not the root compression.

(b) blake3(F || A, 2) is a function of F and of CV_t(A) alone.

(c) For strings A and B of 1 to 64 bytes with CV_t(A) = CV_t(B), blake3(F ||
A, 2) = blake3(F || B, 2).

Proof. (a) F || A has 1024 t + len(A) bytes with 1 <= len(A) <= 64, so
chunk_count = t + 1 and the last chunk is data[t * 1024:] = A. In
`_chunk_output(A, t, 2)`, last_offset = 0, so that function stops at its first
block, offset 0, and returns (IV, words(A), t, len(A), CHUNK_START |
CHUNK_END). The final loop of blake3 compresses this descriptor once, in its
first pass, which runs because the stack is not empty (b).

(b) The loop over counter = 0, .., t - 1 reads
data[counter*1024:(counter+1)*1024], which lies inside F, and no other byte of
the message; so the stack that it leaves depends on F alone. Each pass appends
one value and pops values only while total is even, so after t >= 1 passes the
stack holds as many values as t has one bits, at least one. The final loop
therefore runs at least once. Its first pass forms `_parent_output` of the top
of the stack and CV_t(A), and every later pass forms a parent descriptor from
the next value of the stack and the chaining value of the descriptor before it.
The root compression reads the last descriptor. So the digest is computed from
the stack, which depends on F alone, and from CV_t(A).

(c) follows from (b). QED.

The code accepts messages shorter than 2^61 bytes; the messages of this package
are shorter than 2^42 bytes (Section 9). The tree, its counters and flags and
its root output are those of the target profile. The two messages of a pair are
complete messages of the domain, and a pair with equal digests is an ordinary
collision, not a free-start or compression-only one. The converse of (c) is not
used.

*The digest does not show a partial agreement.* When CV_t(A) and CV_t(B) agree
on four words only, the parent and root compressions over them mix all eight,
and the two digests are not expected to agree on a fixed set of words. On two
counter pairs of the participant's 55/63 counter construction with t = 1,
messages of 1,079 and 1,087 bytes, the
chaining values agree on words 0, 2, 5 and 7, and the two digests do not agree
on digest words 0, 2, 5 and 7 (participant computation with the organizer's
code). This is why the declared experiments run the root instance (6.4).

*Participant checks with the organizer's code.* In each of the following the
organizer's `verifier/blake3.py` was imported unchanged; they are participant
computations, which the organizer has not run. (1) For 2,000 trials of the
participant's 55/63 counter construction in 40 outer steps, 8 of them with outer words
0 or ffffffff, `_chunk_output` of the last chunk returned (IV, the block words,
t, 55 or 63, 3) for A and for B, and `_compress` returned the chaining value
that the program computes, in 2,000 of 2,000; words 0, 2, 5 and 7 of the two
chaining values were equal in all 2,000 and all eight words in none; and
204,000 internal words of the construction were equal to a separately written
forward computation of the compression. (2) For five counter trials with t = 1,
3, 3, 4 and 16,383, the complete messages F || A and F || B, with F a string of
t chunks of pseudorandom bytes, were hashed by `blake3(m, 2)`. In each, the
messages have 1024 t + 55 and 1024 t + 63 bytes; the code makes exactly one
compression with block length 55 or 63, and its inputs are (IV, the block
words, t, 55 or 63, 3); its chaining values agree on words 0, 2, 5 and 7 and
not on all eight; the two digests differ; and when the output of that
compression of F || B is replaced by the output of the one of F || A, blake3
returns the digest of F || A, and the other way round. (3) Before the program
was written a helper agent checked (b) in the same way for 25 values of t from
1 to 1,025, on 150 messages and 75 pairs with a replaced output, all as the
lemma says.

*The lengths 62 and 64.* The checks above were made on the lengths 55 and 63.
No check with the organizer's code was run on the lengths 62 and 64 of this
package. Lemma TR holds for every string A of 1 to 64 bytes and so for 62 and
64: for len(A) = 64, chunk_count = t + 1 and last_offset = max(0, 63 // 64 *
64) = 0, so the last chunk is again one block, compressed once with counter t
and flags 3.


## 8. The 62/64 length pair and the exact pin

This section and the next are the exact construction of the path. Section 3
above is the 55/63 version of the same three ingredients; nothing below uses
its constants.

**8.1 The length is cancelled inside K2 for an even difference.** K2 =
G(2,6,10,14, w4, w5) is the only call of round 0 that reads the block length n,
the initial value of v[14], and the only call of round 0 that reads w4 and w5;
its inputs are (IV[2], IV[6], IV[2], n). Put K = IV[2] + IV[6] = 5bf2cd1d. The
lengths are 62 = 3e and 64 = 40, and 62 XOR 64 = 7e.

**Lemma L62.** Let w4 be a word with ((K + w4) AND 7e) = 3e, and put w4' = w4 +
2 and w5' = w5 - 2, modulo 2^32. Then K2 with block length 62 and words (w4,
w5) leaves the same four state words as K2 with block length 64 and words
(w4', w5').

Proof. Let a1 = K + w4. Its bits 1 to 6 are 1, 1, 1, 1, 1 and 0, so a1 XOR 7e
has them 0, 0, 0, 0, 0 and 1 and equals a1 - 3e + 40 = a1 + 2 = K + w4': the
first assignment of the second execution gives a1 XOR 7e. Its second
assignment gives ROR(64 XOR a1 XOR 7e, 16) = ROR(62 XOR a1, 16), because 64
XOR 7e = 3e = 62: the same d1. The third and fourth assignments depend only on
d1 and constants. The fifth gives (a1 + 2) + b1 + (w5 - 2) = a1 + b1 + w5. The
last three depend only on values already shown equal. QED.

The condition ((K + w4) AND 7e) = 3e makes the difference w4' - w4 equal to
+2, so the difference of the y-message of E1, w5' - w5, is -2. As in 3.1,
two blocks of 62 and 64 bytes that share every word except w4 and w5, related
as above, have the same state S after the column step and the same state X
after round 0.

*Which bytes must be zero.* Message A has 62 bytes, message B 64. For both to
be honest byte strings whose zero-filled blocks share the words w6 to w15, the
bytes 62 and 63 of the block must be zero in both: in A they are zero fill, in
B they are its last two bytes, chosen to be zero. Bytes 62 and 63 are the top
two bytes of w15. So the family needs

    w15 < 2^16,

and nothing else: w13 and w14 are free full words, and bytes 0 to 61 are free in
both messages.

**8.2 The pin.** Fix the six constants

    W4 = a40d3321   X3 = 435d473f   X7 = 9895859e   X11 = 9003b0e0
    X15 = a7590cb9  W13 = b2077fc6

K + W4 = 0000003e, so W4 satisfies Lemma L62 with a1 = 3e, and W4' = W4 + 2 =
a40d3323. The four first values of K2 for message A (length 62) are the
constants

    K2.a1 = 0000003e   K2.d1 = ROR(62 XOR 3e, 16) = 00000000
    K2.c1 = IV[2] + K2.d1 = 3c6ef372   K2.b1 = ROR(IV[6] XOR K2.c1, 12) = ad923ed2.

Evaluate C3 = G(3,7,11,15, w4, W13) on the inputs (X3, X7, X11, X15) with w4 =
W4 and with w4 = W4':

    w4 = W4    a1=7ffffffe d1=f347d8a6 c1=834b8986 b1=c181bde0
               a2=f3893da4 d2=0200cee5 c2=854c586b b2=16899bcb
    w4 = W4'   a1=80000000 d1=0cb92759 c1=9cbcd839 b1=da704295
               a2=0c77c25b d2=0200cee5 c2=9ebda71e b2=16899bcb

**Fact P62.** The two executions give the same d output 0200cee5 and the same
b output 16899bcb. They differ in the a output, Y3 = f3893da4 and Y3' =
0c77c25b, and in the c output, Y11 = 854c586b and Y11' = 9ebda71e. The modular
differences are DY3 = Y3' - Y3 = 18ee84b7 and DY11 = Y11' - Y11 = 19714eb3. This
is a finite computation on the displayed constants; the participant's
arithmetic script recomputes all sixteen values and the four K2 constants in
exact integer arithmetic.

DY3 and DY11 are modular B-minus-A differences, not XOR differences; the XOR
words Y3 XOR Y3' = fffeffff and Y11 XOR Y11' = 1bf1ff75 are not used. These
constants are not those of Fact P of Section 3.

**8.3 Half of the chaining value does not see the difference.**

**Lemma H62.** Take two executions of the 2-round compression that have the
same state X after round 0 and the same message words except w4 and w5.
Suppose (X[3], X[7], X[11], X[15]) = (X3, X7, X11, X15) of 8.2, w13 = W13, and
w4 is W4 in the first execution and W4' in the second; w14 and w15 are any
words, the same in both. Then the two outputs agree on words 0, 2, 5 and 7.

Proof. As for Lemma H. C0, C1 and C2 read neither w4 nor w5 and act on
identical states. C3 reads state words 3, 7, 11, 15 and the words w4 and w13;
by Fact P62 it leaves the same v[7] and v[15] and may differ only in v[3] and
v[11]. E0 reads Y[0], Y[5], Y[10], Y[15] and w1, w11; E2 reads Y[2], Y[7],
Y[8], Y[13] and w9, w14. None of these is Y[3], Y[11], w4 or w5, and w14 is the
same in both, so E0 and E2 give identical Z[0], Z[5], Z[10], Z[15] and Z[2],
Z[7], Z[8], Z[13], and o[0], o[2], o[5], o[7] use only those eight words.
QED.

The residual of a pair is formed from the outputs of E1 and E3 as in 3.3, and
the pair is a collision of the last-chunk chaining values exactly when it is 0.

## 9. The counter construction on the 62/64 pair

*Words and constants.* The construction has these free words: the seven *outer
words* C0.d1, D2.a1, D2.b1, S11, S4, X9 and w6 of the participant's 55/63
counter construction; r, which becomes w14; z, with 0 <= z < 2^16, which
becomes w15; a word y, which becomes Y4; and the *inner word* c1, which becomes
the third value of E1 on message A. The constants are X3, X7, X11, X15, w4 =
W4 and w13 = W13 of 8.2, the four constant first values of K2 of 8.2, and Y3,
Y11 of Fact P62. The compression reads three more values besides the message
and the IV: K3 reads the flags, here 3 (the line for K3.d1); K1 reads v[13],
here 0 (the line for K1.a1); and K0 reads the counter v[12], which the line for
t solves K0's second assignment for. Compared with the 55/63
construction exactly two lines change, those for D3.a1 and D3.b1, which become
D3's first and fifth assignments with w14 = r and w15 = z; the outer basis and
the order of every other line are kept, with the new constants.

*The member.* In Sections 9 to 15 a *member* is a word e of the class of eta
(10.1). The search draws e and sets y = e - Y3 - z, so that the first value of
E3 on message A is e1 = Y3 + Y4 + w15 = e.

**Step CO62 (the outer step; 77 lines, from the seven outer words, r, z and y).**

    X2 = D2.a1 + D2.b1 + W13;   X8 = ROL(X7,7) XOR D2.b1
    C0.c1 = X8 + C0.d1;   K3.a1 = IV[3] + IV[7] + w6
    K3.d1 = ROR(K3.a1 XOR 3,16);   K3.c1 = IV[3] + K3.d1
    S15 = S11 - K3.c1;   S3 = ROL(S15,8) XOR K3.d1
    K3.b1 = ROR(IV[7] XOR K3.c1,12);   D3.a1 = S3 + S4 + r
    S7 = ROR(K3.b1 XOR S11,7);   D3.b1 = X3 - D3.a1 - z
    D2.c1 = ROL(D2.b1,12) XOR S7;   D3.c1 = ROL(D3.b1,12) XOR S4
    X4 = ROR(D3.b1 XOR X9,7);   X13 = X8 - D2.c1
    X14 = X9 - D3.c1;   C0.b1 = ROR(X4 XOR C0.c1,12)
    D2.d1 = ROL(X13,8) XOR X2;   D3.d1 = ROL(X14,8) XOR X3
    Y8 = ROL(Y4,7) XOR C0.b1;   S13 = ROL(D2.d1,16) XOR D2.a1
    S9 = D3.c1 - D3.d1;   Y12 = Y8 - C0.c1
    K1.c1 = S9 - S13;   Y0 = ROL(Y12,8) XOR C0.d1
    K1.d1 = K1.c1 - IV[1];   C0.a1 = Y0 - C0.b1 - w6
    K1.a1 = ROL(K1.d1,16);   w2 = K1.a1 - IV[1] - IV[5]
    X0 = C0.a1 - X4 - w2;   S14 = ROL(D3.d1,16) XOR D3.a1
    K1.b1 = ROR(IV[5] XOR K1.c1,12);   S10 = K2.c1 + S14
    D0.d1 = ROL(X15,8) XOR X0;   S5 = ROR(K1.b1 XOR S9,7)
    D0.c1 = S10 + D0.d1;   D0.b1 = ROR(S5 XOR D0.c1,12)
    X10 = D0.c1 + X15;   X5 = ROR(D0.b1 XOR X10,7)
    S1 = ROL(S13,8) XOR K1.d1;   w3 = S1 - K1.a1 - K1.b1
    X12 = ROL(C0.d1,16) XOR C0.a1;   D1.c1 = X11 - X12
    D1.d1 = D1.c1 - S11;   S8 = D2.c1 - D2.d1
    K0.b1 = ROL(S4,7) XOR S8;   S2 = ROL(S14,8) XOR K2.d1
    S6 = ROR(K2.b1 XOR S10,7);   X1 = ROL(X12,8) XOR D1.d1
    K0.c1 = ROL(K0.b1,12) XOR IV[4];   D1.b1 = ROR(S6 XOR D1.c1,12)
    C1.a1 = X1 + X5 + w3;   S12 = S8 - K0.c1
    w7 = S3 - K3.a1 - K3.b1;   X6 = ROR(D1.b1 XOR X11,7)
    C1.d1 = ROR(X13 XOR C1.a1,16);   D1.a1 = ROL(D1.d1,16) XOR S12
    C1.c1 = X9 + C1.d1;   C2.a1 = X2 + X6 + w7
    w10 = D1.a1 - S1 - S6;   C1.b1 = ROR(X5 XOR C1.c1,12)
    C2.d1 = ROR(X14 XOR C2.a1,16);   w12 = D2.a1 - S2 - S7
    Y1 = C1.a1 + C1.b1 + w10;   C2.c1 = X10 + C2.d1
    Y13 = ROR(C1.d1 XOR Y1,8);   C2.b1 = ROR(X6 XOR C2.c1,12)
    K0.d1 = K0.c1 - IV[0];   Y9 = C1.c1 + Y13
    S0 = ROL(S12,8) XOR K0.d1;   D0.a1 = ROL(D0.d1,16) XOR S15
    w8 = D0.a1 - S0 - S5;   w5 = S2 - K2.a1 - K2.b1
    w9 = X0 - D0.a1 - D0.b1;   w11 = X1 - D1.a1 - D1.b1
    Y5 = ROR(C1.b1 XOR Y9,7)

The lines are those of the participant's 55/63 step CO with D3.a1 = S3 + S4 + r
and D3.b1 = X3 - D3.a1 - z in place of D3.a1 = S3 + S4 and D3.b1 = X3 - D3.a1,
and with the constants of 8.2.

**Step CT62 (the trial; 16 lines, from c1 and the names of step CO62).**

    E1.d1 = c1 - Y11;   E1.a1 = ROL(E1.d1,16) XOR Y12
    Y6 = E1.a1 - Y1 - w12;   Y10 = ROL(Y6,7) XOR C2.b1
    Y14 = Y10 - C2.c1;   E1.b1 = ROR(Y6 XOR c1,12)
    Y2 = ROL(Y14,8) XOR C2.d1;   E3.h1 = ROR(Y14 XOR (Y3 + Y4 + z),16)
    w0 = Y2 - C2.a1 - C2.b1;   E3.g1 = Y9 + E3.h1
    K0.a1 = IV[0] + IV[4] + w0;   E3.f1 = ROR(Y4 XOR E3.g1,12)
    t = ROL(K0.d1,16) XOR K0.a1;   w1 = S0 - K0.a1 - K0.b1
    E1.a2 = E1.a1 + E1.b1 + w5;   E3.e2 = Y3 + Y4 + z + E3.f1 + w8

With e = Y3 + Y4 + z the lines for E3.h1, E3.g1, E3.f1 and E3.e2 read h =
ROR16(Y14 XOR e), g = Q + h with Q = Y9, f = ROR12(y XOR g) and e2 = E + f
with E = e + w8: E3's first value is e, and its b input is y = e - Y3 - z.

**Step CS62 (the messages).** If t = 0 the trial is invalid and is dropped: a
message with no full chunk before its last chunk has that chunk as its root,
compressed with counter 0 and flags 11 and not with the flags 3 that the line
for K3.d1 used. Otherwise the words w0 to w12 of the lines, with w4 = W4, w13 =
W13, w14 = r and w15 = z, form the block of A; A is the first 62 bytes of its
little-endian encoding, and B the 64 bytes of that of the same words with w4' =
W4' = a40d3323 and w5' = w5 + fffffffe = w5 - 2 in place of w4 and w5. F is the
string of 1024 t zero bytes, and the two messages are F || A, of 1024 t + 62
bytes, and F || B, of 1024 t + 64 bytes.

*The order and the calls.* Table CT gives each call's eight assignments by the
name that the line for that assignment assigns; the cells K2.a1, K2.d1, K2.c1
and K2.b1 are the four constant values of 8.2. It is the table of the 55/63
construction: the names are the same, and the D3 cells D3.a1 and D3.b1 now
name the lines with r and z. E1's first five assignments are the lines for Y6,
E1.a1, E1.d1, E1.b1 and E1.a2, in the order of the assignments; E3's first two
assignments are the line for E3.h1, and its third to fifth the lines for
E3.g1, E3.f1 and E3.e2.

| Call | 1st | 2nd | 3rd | 4th | 5th | 6th | 7th | 8th |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| K0 | K0.a1 | t | K0.d1 | K0.c1 | w1 | S0 | S12 | K0.b1 |
| K1 | w2 | K1.a1 | K1.d1 | K1.b1 | w3 | S1 | K1.c1 | S5 |
| K2 | K2.a1 | K2.d1 | K2.c1 | K2.b1 | w5 | S2 | S10 | S6 |
| K3 | K3.a1 | K3.d1 | K3.c1 | K3.b1 | w7 | S3 | S15 | S7 |
| D0 | w8 | D0.a1 | D0.c1 | D0.b1 | w9 | D0.d1 | X10 | X5 |
| D1 | w10 | D1.a1 | D1.d1 | D1.b1 | w11 | X1 | D1.c1 | X6 |
| D2 | w12 | S13 | S8 | D2.c1 | X2 | D2.d1 | X13 | X8 |
| D3 | D3.a1 | S14 | S9 | D3.c1 | D3.b1 | D3.d1 | X14 | X4 |
| C0 | X0 | X12 | C0.c1 | C0.b1 | C0.a1 | Y0 | Y12 | Y8 |
| C1 | C1.a1 | C1.d1 | C1.c1 | C1.b1 | Y1 | Y13 | Y9 | Y5 |
| C2 | C2.a1 | C2.d1 | C2.c1 | C2.b1 | w0 | Y2 | Y14 | Y10 |

**Lemma CT62 (the counter order).** (a) *Triangular.* In the printed order,
step CO62 and then step CT62, every line assigns a name that no earlier line
assigns and that is neither a free word nor a constant, and it reads only
constants, the free words and names of earlier lines; a line of step CO62 reads
neither c1 nor a name of step CT62. Every line is one assignment of one call
solved for the name on its left; the exceptions are the line for E3.h1, which
is the first two assignments of E3 with the first substituted into the second
(e1 = Y3 + Y4 + w15, w15 = z), and the line for E3.e2, which uses the same e1.
By Table CT the 93 lines and the four constant values of K2 are, each exactly
once, the eight assignments of each of the eleven calls K0..K3, D0..D3, C0..C2,
with the inputs and the message words of Section 1 for block length 62,
counter v[12] = t, v[13] = 0 and flags v[15] = 3, with w4 = W4, w13 = W13, w14
= r and w15 = z, and with the constants X3, X7, X11, X15 as the a output of D3,
the b output of D2, the c output of D1 and the d output of D0; and the first
five assignments of E1 and of E3 for message A, E1 with c input Y11 and E3
with a input Y3.

(b) *The calls.* For every choice of the free words, the names of the lines
are the executions of these calls. In particular round 0 on the block of A,
with block length 62, counter t, v[13] = 0 and flags 3, leaves the state X of
the names, with the four constants as X[3], X[7], X[11] and X[15]; C0 has
outputs (Y0, y, Y8, Y12); and in the compression of A, E1.c1 = c1.

(c) *The levels.* A line of step CO62 is a function of the seven outer words,
r, z and y. Of the message words only w0 and w1 are lines of step CT62, and so
is the counter t; w14 = r and w15 = z are free words of the outer step and
every other message word is a line of step CO62 or a constant. So the trials
of one outer step differ in w0, w1 and t and in nothing else of their two
messages.

Proof. As for the 55/63 order, read off the displays, each formula compared
with Section 2 and with its call's inputs, outputs and message words (Section
1, with n = 62, v[12] = t, v[13] = 0 and v[15] = 3). The lines that differ from
the 55/63 order are: D3.a1 = S3 + S4 + r, D3's first assignment a1 = A + B + x
with inputs A = S3, B = S4 and x = w14 = r; D3.b1 = X3 - D3.a1 - z, D3's fifth
assignment a2 = a1 + b1 + y with a2 = X3 and y = w15 = z, solved for b1; the
four constants of K2, its first four values for n = 62 and w4 = W4; and the
lines for E3.h1 and E3.e2, whose e1 now contains w15 = z. D3's other six
assignments and every other line are those of the 55/63 order, whose
triangularity does not depend on the values of r, z or the constants. Table CT
has one name in each of its 88 cells, all different,
the four constant values of K2 among them. (b) An assignment solved for one of
its terms is an equivalent equation modulo 2^32 (Fact 1), so a line's
assignment holds once it has run, and by (a) no later line changes its names;
by (a) and Table CT all eight assignments of each call hold, a constant output
in its place, and y as the b output of C0 (the line for Y8). (c) By induction
over the printed order with (a). QED.

**Theorem C62 (the 62/64 last-chunk half-collision).** For every choice of the
seven outer words, of r, of z < 2^16, of y and of c1, steps CO62 and CT62 give a
counter t. If t is not zero, step CS62 outputs two distinct messages F || A and
F || B of 1024 t + 62 and 1024 t + 64 bytes, with 1 <= t < 2^32, such that

(i) their last chunks are A and B, compressed with counter t, v[13] = 0 and
flags 3 (Lemma TR (a));

(ii) the chaining values CV_t(A) and CV_t(B) agree on words 0, 2, 5 and 7;

(iii) in both last-chunk compressions Y4 = y, and the XOR difference between A
and B of E3's first-half d value is ROR(e XOR (e + DY3), 16) with e = Y3 + y +
z; it is eta = 85492711 exactly when e is in the class of 10.1;

(iv) in the compression of A, E1.c1 = c1; and the XOR difference between A and
B of E1's first-half b value is beta = f5519714 exactly when c1 is in the cube
Q_beta of 10.1.

Proof. t is the XOR of two 32-bit words, so t < 2^32 and t >> 32 = 0, the value
v[13] = 0 that the line for K1.a1 used. The sixteen words have w15 = z < 2^16,
so bytes 62 and 63 of their encoding are zero: A, the first 62 bytes, is an
honest 62-byte string whose zero-filled block is the sixteen words, and B is an
honest 64-byte string, ending in two zero bytes, whose block is the sixteen
words with w4 and w5 replaced. By Lemma TR (a) the last chunks are compressed
with counter t, v[13] = 0, flags 3 and block lengths 62 and 64. By Lemma CT62
(b) round 0 on the block of A leaves the state X of the names, with the four
constants as X[3], X[7], X[11] and X[15]. The counter, v[13] and the flags are
the same in both compressions, and K2 is the only call of round 0 that reads
the block length, w4 or w5; W4 satisfies the condition of Lemma L62 (8.2), so
that lemma, whose proof concerns K2 alone, gives the same state X for B. Lemma
H62 gives (ii): its proof uses only round 1 and o[i] = Z[i] XOR Z[i + 8] for i
= 0, 2, 5 and 7, and the chaining value is (o[0], .., o[7]). (iii) C0 reads the
same words of X and w2, w6 in both compressions and has b output y by Lemma
CT62 (b). E3 has a input Y3 for A and Y3' = Y3 + DY3 for B (Fact P62), the same
b input y, the same d input Y14 and the same first message word w15 = z, so its
first values are e and e + DY3 and its second values ROR(Y14 XOR e, 16) and
ROR(Y14 XOR (e + DY3), 16), whose XOR is ROR(e XOR (e + DY3), 16). By Lemma FB
(10.1) this is eta exactly on the class. (iv) E1.c1 = c1 is Lemma CT62 (b). E1
has inputs (Y1, Y6, Y11, Y12) and message words (w12, w5) for A, and (Y1, Y6,
Y11', Y12) and (w12, w5 - 2) for B. Its first and second values are the same
for both, so its third values are c1 and c1 + DY11, and its fourth values
ROR(Y6 XOR c1, 12) and ROR(Y6 XOR (c1 + DY11), 12), whose XOR is ROR(c1 XOR
(c1 + DY11), 12). That is beta exactly when c1 XOR (c1 + DY11) = ROL(beta, 12)
= 19714f55, which by Lemma FB holds exactly on the cube Q_beta. The messages
are distinct because their lengths differ. QED.

**Lemma IP62 (the inner permutations and the member with t = 0).** Fix the
seven outer words, r, z and y, and put e = Y3 + y + z. (a) The maps c1 ->
E3.h1 and c1 -> t given by step CT62 are permutations of the 32-bit words. (b)
So the 2^16 members of the cube Q_beta give 2^16 different values of E3.h1 and
of t, and at most one member of the cube has t = 0.

Proof. With the names of step CO62 fixed, the lines for E1.d1, E1.a1,
Y6, Y10, Y14 and E3.h1 each map their running word one to one. Read backwards:
Y14 = ROL(E3.h1,16) XOR e, Y6 = ROR((Y14 + C2.c1) XOR C2.b1, 7), E1.a1 = Y6 +
Y1 + w12 and c1 = Y11 + ROR(E1.a1 XOR Y12, 16). For the counter, Y2 =
ROL(Y14,8) XOR C2.d1 = ROL(E3.h1,24) XOR ROL(e,8) XOR C2.d1, and the lines for
w0, K0.a1 and t give t = ROL(K0.d1,16) XOR (Y2 + IV[0] + IV[4] - C2.a1 -
C2.b1), where K0.d1, C2.a1, C2.b1 and C2.d1 are names of step CO62. That is a
composition of permutations of E3.h1, and its only zero has one value of c1,
which may or may not lie in the cube. QED.

So an outer step has 2^16 or 2^16 - 1 valid trials; this is the factor N_c - 1
of H1-62 (Section 15). *The length of the messages.* The messages have 1024 t
+ 62 and 1024 t + 64 bytes with t < 2^32, so each is shorter than 2^42 bytes. A
small t cannot be chosen: it is the value of a permutation of c1 at the member
that the search finds. The common counter of the two messages and the
same-prefix argument of Lemma TR hold for these lengths; they add no counter or
materialization charge beyond the reserve of 13.1.

## 10. The class, the cube, the row equations and the local mass

**10.1 Fibres of an increment.**

**Lemma FB.** Let d and m be words and put p = ((m - d) mod 2^32) / 2. The set
of words x with x XOR (x + d) = m is nonempty exactly when m - d is even and p
has no bit outside m' = m AND 7fffffff; then it is the cube of all x with (x
AND m') = p, which has 2^(32 - wt(m')) members, bit 31 of x always free.

Proof. x XOR (x + d) = m holds exactly when x + d = x XOR m, that is when (x
XOR m) - x = d modulo 2^32. For words x and m, (x XOR m) - x is the sum over
the bits i of m of 2^i where bit i of x is 0 and of -2^i where it is 1, which
is m - 2 (x AND m). Modulo 2^32, 2 (x AND m) = 2 (x AND m'), because the term of
bit 31 doubles to 2^32. So the condition is 2 (x AND m') = m - d modulo 2^32.
As x AND m' < 2^31 the doubling is exact: the condition holds exactly when m -
d is even and (x AND m') = p, and that needs p inside m'. The bits of x outside
m', bit 31 among them, are free. QED.

The identity (x XOR m) - x = m - 2 (x AND m) modulo 2^32 of this proof is used
again in 10.2.

*The class of eta.* Fix eta = 85492711 and m = ROL(eta, 16) = 27118549, d =
DY3 = 18ee84b7. Then m - d = 0e230092 is even, p = 07118049 lies inside m' =
27118549, and wt(m') = 12. The *class* is

    C_eta = { e : (e AND 27118549) = 07118049 },   n_eta = 2^20 members.

Member number k of the class, 0 <= k < 2^20, is the e whose bits at the 20
positions where 27118549 has a zero are the bits of k, in increasing order of
position; y = e - Y3 - z.

*The cube of beta.* Fix beta = f5519714 and m = ROL(beta, 12) = 19714f55, d =
DY11 = 19714eb3. Then m - d = 000000a2, p = 00000051 lies inside m' = 19714f55,
and wt(m') = 16. The *cube* is

    Q_beta = { c : (c AND 19714f55) = 00000051 },   N_c = 2^16 members.

Member number j of the cube, 0 <= j < 2^16, is the c whose bits at the 16
positions where 19714f55 has a zero are the bits of j, in increasing order of
position. Both cubes are recomputed from Lemma FB by the participant's
arithmetic script, and by a brute force over all 2^32 words in the
participant's independent recount (10.4).

**10.2 The outcome of a trial and the row equations.** Take a valid trial
whose member e is in the class and whose c1 is in the cube. Write the two
executions of E1 and of E3, for A and for B, with the names of Section 2,
primed for B, and write Delta v for the XOR difference v XOR v' of a value
between B and A. E1 = G(1,6,11,12, w12, w5) has the outputs Z1, Z6, Z11, Z12
and E3 = G(3,4,9,14, w15, w8) the outputs Z3, Z4, Z9, Z14, so by 3.3 and Lemma
H62 the two last-chunk chaining values are equal exactly when

    Delta Z1 = Delta Z9,  Delta Z3 = Delta Z11,
    Delta Z4 = Delta Z12, Delta Z6 = Delta Z14.

The *outcome* of the trial is the pair (tau, eps) = (Delta Z1, Delta Z11), the
differences of E1's a and c outputs.

*Names.* In E1 on A: c = c1 (its third value), d = c - Y11 (its second value,
the same on B), b = ROR(Y6 XOR c, 12) (its fourth value) and a (its fifth
value, E1.a2). In E3 on A: e (its first value), h = E3.h1 (its second), Q = Y9
(its c input, the same on B), g = Q + h (its third), f = ROR(y XOR g, 12) (its
fourth), E = e + w8 and e2 = E + f (its fifth). Put E' = E + DY3. For words tau
and eps put

    sigma = tau XOR ROR(tau, 1),   theta = ROL(sigma, 12),
    lam = ROR(eta XOR eps, 8).

**Lemma RES (the row equations).** For a valid trial with e in the class and
c1 in the cube, and words tau and eps, the two last-chunk chaining values are
equal and the outcome is (tau, eps) exactly when these five conditions hold:

    (EPS) eps XOR ROL(eps, 1) = eta XOR ROL(beta, 1);
    (E1)  a XOR a' = tau and
          (c + ROR(d XOR a, 8)) XOR (c + DY11 + ROR(d XOR a', 8)) = eps,
          where a' = a + beta - 2 (b AND beta) - 2;
    (J1)  (Q + h) XOR (Q + (h XOR eta)) = theta;
    (J2)  (E + f) XOR (E' + (f XOR sigma)) = eps;
    (J3)  (g + ROR(h XOR e2, 8)) XOR ((g XOR theta) + (ROR(h XOR e2, 8) XOR lam))
          = tau.

Proof. *E1.* Its inputs are (Y1, Y6, Y11, Y12) on A and (Y1, Y6, Y11 + DY11,
Y12) on B, and its message words (w12, w5) and (w12, w5 - 2) (step CS62, Fact
P62). Its first and second values are the same on both. Its third values are c
and c + DY11, and by Theorem C62 (iv) its fourth values are b and b XOR beta.
By the identity of 10.1, (b XOR beta) - b = beta - 2 (b AND beta) modulo 2^32,
so its fifth value on B is a + (beta - 2 (b AND beta)) - 2 = a', and Delta Z1
= a XOR a'. Its sixth values are ROR(d XOR a, 8) and ROR(d XOR a', 8), so
Delta Z12 = ROR(Delta Z1, 8); its seventh values are the two sums of (E1), so
Delta Z11 is their XOR; and Delta Z6 = ROR(beta XOR Delta Z11, 7).

*E3.* Its inputs are (Y3, y, Q, Y14) on A and (Y3 + DY3, y, Q, Y14) on B, and
its message words are (z, w8) on both. Its first values are e and e + DY3, and
by Theorem C62 (iii) its second values are h and h XOR eta. Its third values
are g and g' = Q + (h XOR eta); its fourth values are f and f' = ROR(y XOR g',
12), so f XOR f' = ROR(g XOR g', 12); its fifth values are e2 = E + f and
(e + DY3) + f' + w8 = E' + f'. So Delta Z3 = e2 XOR (E' + f'), Delta Z14 =
ROR(eta XOR Delta Z3, 8), Delta Z9 is the XOR of g + ROR(h XOR e2, 8) and its
value on B, and Delta Z4 = ROR((f XOR f') XOR Delta Z9, 7).

*Only if.* Let the chaining values be equal with outcome (tau, eps). Then
Delta Z1 = tau and Delta Z11 = eps, which is (E1), and Delta Z9 = tau, Delta
Z3 = eps and Delta Z12 = ROR(tau, 8). Delta Z14 = Delta Z6 reads ROR(eta XOR
eps, 8) = ROR(beta XOR eps, 7); rotating both sides left by 8 gives eta XOR eps
= ROL(beta, 1) XOR ROL(eps, 1), which is (EPS). Delta Z4 = Delta Z12 reads
ROR((f XOR f') XOR tau, 7) = ROR(tau, 8), so f XOR f' = tau XOR ROR(tau, 1) =
sigma and g XOR g' = ROL(sigma, 12) = theta, which is (J1). With (J1), f' = f
XOR sigma, and Delta Z3 = eps is (J2). With (J2) the sixth value of E3 on B is
ROR(h XOR eta XOR e2 XOR eps, 8) = ROR(h XOR e2, 8) XOR lam, and with (J1) its
third value on B is g XOR theta, so Delta Z9 = tau is (J3).

*If.* (E1) gives Delta Z1 = tau, Delta Z11 = eps, Delta Z12 = ROR(tau, 8) and
Delta Z6 = ROR(beta XOR eps, 7). (J1) gives f XOR f' = ROR(theta, 12) = sigma
and g' = g XOR theta; (J2) gives Delta Z3 = eps, so Delta Z14 = lam and the
sixth value of E3 on B is ROR(h XOR e2, 8) XOR lam; (J3) then gives Delta Z9 =
tau, and Delta Z4 = ROR(sigma XOR tau, 7) = ROR(ROR(tau, 1), 7) = ROR(tau, 8).
By (EPS), lam = ROR(eta XOR eps, 8) = ROR(beta XOR eps, 7). So the four
equalities of the display hold. QED.

*eps and the rows.* x -> x XOR ROL(x, 1) is linear over GF(2), its kernel is
{00000000, ffffffff} and its image is the 2^31 words of even weight; eta XOR
ROL(beta, 1) = 6fea0938 has weight 16, so (EPS) has exactly two solutions,
2559f8e8 and its complement. The record fixes eps = 2559f8e8 (eps XOR ROL(eps,
1) = 6fea0938, recomputed). A *row* is an outcome (tau, eps) with this eps.
The search uses two rows:

    row 1: tau = aaaf751e        row 2: tau = aaaf771e.

**10.3 The counts of a row and the model mass.** For a row, L is the number of
triples (c, b, a), with c in the cube and b and a any words, that satisfy (E1)
with d = c - Y11; out of 2^16 * 2^64 triples. N3Sigma is the sum over z = 0,
.., 65535 of the number of quadruples (e, h, Q, E), with e in the class and h,
Q and E any words, that satisfy (J1), (J2) and (J3) with y = e - Y3 - z, g = Q
+ h, f = ROR(y XOR g, 12), e2 = E + f and E' = E + DY3; out of 2^16 * 2^20 *
2^96 = 2^132 tuples. The *model mass* of the row is

    mu_row = (L / 2^64) * (N3Sigma / 2^132) = L * N3Sigma / 2^196:

the expected number of the 2^16 trials of one raw proposal that satisfy (E1),
(J1), (J2) and (J3) of the row when, for each trial, (b, a) is uniform and,
independently, (z, e, h, Q, E) is uniform on its domain. By Lemma RES, with
(EPS) true for the record, these are the trials that complete the collision
with the row's outcome. The counting model is this independence; the actual
words of a trial are functions of the proposal and of c1 (Section 9), and the
model is not a statement about them.

| row | tau | L (E1, exact) | N3Sigma (E3, exact) | L * N3Sigma | mu_row |
| --- | --- | ---: | ---: | ---: | ---: |
| 2 | aaaf771e | 134217728 = 2^27 | 6773413839565225984 = 47 * 2^57 | 909112216350201139379044352 | 2^-106.4454 |
| 1 | aaaf751e | 268435456 = 2^28 | 1761892616720351232 = 12519 * 2^47 | 472954447992360707442081792 | 2^-107.3882 |

The pair total is 1382066664342561846821126144 / 2^196 = 2^75 * (47 * 2^9 +
12519) / 2^196 = 36583 / 2^121, so

    mu = 36583 / 2^121 = 2^-105.8411,

the model expectation of the number of trials of one raw proposal (an outer
step with its member) that complete the collision with the outcome of one of
the two rows. Per trial with c1 in the cube it is 36583 / 2^137 = 71.45 *
2^-128. These are local quantities of independent words. Neither these counts
nor the number of free words of the construction prove the first moment of the
physical sampler; that is premise H1-62.

The factor of H1-62 is

    f = floor(5 * mu * 2^128 / (7 * N_c)) = floor(5 * 36583 / 3584) = 51,

five sevenths of the model rate per trial, rounded down.

**10.4 Evidence for the counts (participant, untrusted by the harness).** The
participant's local exact computation (2026-10-09), the runs of steps 3 and 4
of SEL (12.2), screened all 15,180 pairs of the grid of SEL with 2^28 values
of tau each by exact necessary carry tests of (J1), (J2), (J3) and (E1), on a
graphics card, computed the exact count L of all 225,014 rows that pass (461
have L > 0) and the exact count N3Sigma of all 461 of them: the two rows above
are the only rows with L > 0 and N3Sigma > 0. A sampled 2,001 rows that fail
the E1 carry test all have L = 0; a brute force over all 2^32 words a for 24
random (c, s) of a positive row agrees with the E1 counter, with concrete
witnesses. An independent recount, by a second program written without reading
the first, solves the same equations with its own carry recurrences, matches a
full brute force at widths 6, 7 and 8 in 368 of 368 E1 and 368 of 368 E3 tests,
and at 32 bits agrees exactly on L and N3Sigma of both rows; it found that the
first program had divided by 2^197 and fixed the normalization at 2^196 (a
class of 2^20 members). Not done: the recount did not repeat the 15,180-pair
screen; no complete collision or physical rate is measured. The claim uses the
counts of the two rows only, through the factor f of H1-62.

## 11. The filtered search and its charged pieces

The pieces below are specified here, and their costs are upper allowances
proved here; none of them is implemented or measured. Operations are counted
on the load/store machine of 6.5: one unit for every addition, subtraction,
XOR, AND, OR and shift of a word, every comparison and every branch, one for
every load and one for every store, shift distances fixed in the instruction,
16 registers. A rotation of a 32-bit value is two shifts, an OR and an AND: 4
units. maj(x, y, w) denotes the majority of three bits, (x AND y) OR (w AND (x
XOR y)): 4 units.

**11.1 The run.** The search runs J = 7,225,111,331,732,007,598,311,846,535,606
batches of seven *raw proposals*, B = 7 J = 50,575,779,322,124,053,188,182,925,
749,242 raw proposals in all. A raw proposal draws, with fresh coins, the seven
outer words, r uniform on all words, z uniform on 0..65535 and a member number
k uniform on 0..2^20 - 1; it sets e to member k of the class and y = e - Y3 -
z, runs step CO62 and forms the two filter input words, Q = Y9 and E = e + w8.
Then:

1. *E filter.* A byte-compiled automaton maps E to a two-bit mask, bit i - 1
   set when E passes the E test of row i (11.2). If the mask is 0 the proposal
   ends.
2. *Q filter.* For an E-positive proposal the count of E-positive proposals is
   advanced and compared with the budget LE; the second automaton maps Q to its
   two-bit mask, and the proposal ends if the AND of the two masks is 0.
3. *Solver.* For a proposal whose masks meet, the count of such proposals is
   advanced and compared with the budget L2; the caller rebuilds the proposal
   and runs the joint solver of 11.4 for each row whose bit is set in the AND,
   which returns every member c1 of the cube with t != 0 whose trial completes
   the collision with that row's outcome (Lemma LS).
4. *Halts.* The run halts with failure when a count exceeds its budget or after
   J batches. A returned c1 ends the run with success: the two messages are
   written out and verified (13.1).

Both filters are necessary conditions for a root of a row (Lemma NEC), so the
filtered search returns every root of the two rows that a search without
filters, running the solver on every raw proposal, would return, as long as no
budget halts it. The count of solver entries is the second and last halt.

**11.2 The two existence filters.** For a raw proposal, Q and E are fixed
words. The *Q test* of a row asks whether some word h satisfies (J1) with this
Q; the *E test* of a row asks whether some word f satisfies (J2) with this E
and E' = E + DY3; sigma, theta and eps are the row's (10.2).

**Lemma NEC.** If a trial of a raw proposal completes the collision with the
outcome of a row, the proposal passes the Q test and the E test of that row.

Proof. The trial's E3.h1 satisfies (J1) with the proposal's Q, and its E3.f1
satisfies (J2) with the proposal's E, by Lemma RES. QED.

*The automata.* The Q test of a row is decided by an automaton that reads the
bits Q_0, .., Q_31 of Q in increasing order. Its state before bit j is a set
S_j of pairs (u, u') of bits; S_0 = {(0, 0)}. Reading x = Q_j, S_(j+1) is the
set of the pairs (maj(x, w, u), maj(x, w XOR eta_j, u')) over (u, u') in S_j
and w in {0, 1} with (x XOR w XOR u) XOR (x XOR w XOR eta_j XOR u') = theta_j.
The test passes when S_32 is not empty. The automaton of the E test reads E_0,
.., E_31 and keeps also the carry v of E + DY3, initially 0: reading x = E_j it
puts x' = x XOR DY3_j XOR v, the bit j of E', sets v to maj(x, DY3_j, v), and
S_(j+1) is the set of (maj(x, w, a), maj(x', w XOR sigma_j, a')) over (a, a')
in S_j and w with (x XOR w XOR a) XOR (x' XOR w XOR sigma_j XOR a') = eps_j.

**Lemma AUT.** The Q automaton of a row passes on Q exactly when some h
satisfies (J1); the E automaton passes on E exactly when some f satisfies
(J2).

Proof. For the Q automaton, by induction on j: S_j is the set of the pairs
(carry into bit j of Q + h, carry into bit j of Q + (h XOR eta)) over the words
h for which bits 0 to j - 1 of (Q + h) XOR (Q + (h XOR eta)) equal those of
theta. For j = 0 both carries are 0 and there is no condition. Bit j of the
two sums is x XOR w XOR u and x XOR w XOR eta_j XOR u' with w = h_j, and the
carries out of bit j are the two majorities; so the rule of the automaton is
the step from j to j + 1, and h_j ranges over both values. At j = 32 the set is
nonempty exactly when some h satisfies all 32 bits of (J1); the carries out of
bit 31 are discarded by the modular sums and are not tested. The E automaton
is the same argument for E + f and E' + (f XOR sigma), where v is the carry of
E + DY3, so that x' is bit j of E'. QED.

*The histograms.* Both rows are read on the same input word. The *mask* of a
word is the two-bit word whose bit i - 1 is set when the test of row i passes.
The participant's arithmetic script runs the two automata of the two rows
jointly, as one automaton whose state is the pair of sets (and v), over all
2^32 input words by counting input prefixes per state, and finds these exact
numbers of input words per mask:

| mask | Q histogram | E histogram |
| ---: | ---: | ---: |
| 0 | 4222025728 | 4277405696 |
| 1 | 5505024 | 6995968 |
| 2 | 34406400 | 9877504 |
| 3 | 33030144 | 688128 |

Both columns sum to 2^32. So, for uniform independent Q and E, the share of
raw proposals whose E mask is not 0 and the share whose two masks meet are

    pE = (6995968 + 9877504 + 688128) / 2^32 = 8575 / 2^21,
    p2 = sum over masks a, b with (a AND b) != 0 of H_Q(a) H_E(b) / 2^64
       = 985888670613504 / 2^64 = 7345443 / 2^37.

These are shares of uniform independent input words. The physical marginals of
the sampler's Q and E and their independence do not follow; they enter only
the budgets (H4-62), not the time bound.

**11.3 Tables, lookups and the per-proposal charges.** *Tables.* Each filter
runs the two rows jointly as one deterministic automaton whose state is the
pair of sets (and, for E, the carry v), compiled by bytes: for each byte
position p = 0, 1, 2, 3, each state reachable at bit 8p from the initial state
and each of the 256 values of the byte, one entry holds the state reached at
bit 8p + 8, as the base address of its block of entries at position p + 1, or,
for p = 3, the two-bit mask. The reachable states at bits 0, 8, 16 and 24
number 1, 3, 4 and 7 for Q and 1, 6, 8 and 8 for E (the participant's
arithmetic script), so the tables have (15 + 23) * 256 = 9,728 entries, each in
one 256-bit word: 311,296 bytes. No subword gather, packed-byte read or SIMD
instruction is used. Building them is once-only work: the reachable states are
found by a walk over the 256 byte values at each position, and each entry is
computed by eight steps of the set rule for both rows, at most 480 units a bit
(at most 4 pairs and 2 witness bits per row, at most 30 units each) and 256 for
its address and store, so at most 4,096 an entry and 9,728 * 4,096 < 2^26 in
all; the walk is at most 38 * 256 * 4,096 < 2^26, and the histogram count of
11.2 at most 32 * 38 * 2 * 4,096 < 2^24. With the descriptors and the fixed
metadata, all of it fits D_tables = 2^29 units.

*A lookup* costs at most 64 units: four byte stages of at most 7 units (a
shift and an AND to extract the byte, an addition of the byte to the current
base, the load of the entry, and up to three units to keep the next base), 8
for initialization, reading the final mask and its comparison with 0 and the
branch, 12 for the caller's loop control, and 16 to store and restore up to
eight scratch words around the lookup. At most 16 registers are live.

*A raw proposal* costs at most 4,096 units: drawing its ten words from the
source of coins, at most 64 units each, 640; the 77 lines of step CO62, each
one assignment of one call solved for one name, so at most two additions,
subtractions or XORs and one rotation, at most 6 operations, with at most 3
loads and 1 store: at most 10 units a line, 770 in all; the member, e = the
class value OR the 20 bits of k placed at the zero positions of the class
mask, at most 4 units a bit, 80; y = e - Y3 - z, E = e + w8 and Q, at most 16
with loads and stores; storing the ten coins for a later caller, 10; and loop
control, 32. That is at most 1,548 units, within 4,096. The charges are

    P7 = 7 * (4096 + 64) = 29,120 per batch: seven raw proposals of 4,096
         units each and their E lookups, a final partial batch padded and
         charged;
    q7 = 80 per E-positive proposal: the Q lookup, 64, and 16 for the AND of
         the masks, the count of E-positive proposals, its comparison with LE
         and the branch;
    U = 4,128 per solver entry: the caller rebuilds the proposal from its ten
         stored coins, step CO62 and the member again, within the 4,096 of a
         raw proposal, so that the names of step CO62 that the solver's checks
         read are in memory; and 32 for the count of solver entries, its
         comparison with L2, saving the batch state and the dispatch to the
         rows of the mask.

A lane id is an ordinary loop index; failed comparisons and spills are inside
these allowances.

**11.4 The joint solver.** The solver is called with a raw proposal (its names
of step CO62, e, y, Q, E and E' = E + DY3) and a row whose bit is set in both
masks. It builds the word h = E3.h1 bit by bit, h_0 first, which determines c1
(Lemma IP62), and it keeps the carries of the two additions of (J1) and the
two of (J2).

*Bit positions.* Bit i of h enters bit i of g = Q + h and, since f = ROR(y XOR
g, 12), bit k = (i + 20) mod 32 of f:

    f_k = y_i XOR g_i = y_i XOR Q_i XOR h_i XOR u_i,

where u_i is the carry into bit i of Q + h. As i runs from 0 to 31, k runs 20,
21, .., 31, 0, 1, .., 19. Let a_k be the carry into bit k of E + f, and put

    gamma = eta XOR theta,   delta = E XOR E',   kappa = delta XOR sigma XOR eps.

**Lemma CR (carry relations).** Let h satisfy (J1) and let f = ROR(y XOR (Q +
h), 12) satisfy (J2). Then for every i the carry into bit i of Q + (h XOR eta)
is u_i XOR gamma_i, and for every k the carry into bit k of E' + (f XOR sigma)
is a_k XOR kappa_k. Hence gamma_0 = 0 and kappa_0 = 0, and for i < 31 and k <
31

    maj(Q_i, h_i XOR eta_i, u_i XOR gamma_i) XOR maj(Q_i, h_i, u_i)
        = gamma_(i+1),                                             (C1)
    maj(E'_k, f_k XOR sigma_k, a_k XOR kappa_k) XOR maj(E_k, f_k, a_k)
        = kappa_(k+1).                                             (C2)

Proof. Bit i of the two sums of (J1) is Q_i XOR h_i XOR u_i and Q_i XOR h_i
XOR eta_i XOR u'_i, with u'_i the carry of the second sum, and (J1) says that
their XOR is theta_i; so u'_i = u_i XOR eta_i XOR theta_i = u_i XOR gamma_i.
Bit k of the two sums of (J2) is E_k XOR f_k XOR a_k and E'_k XOR f_k XOR
sigma_k XOR a'_k, and (J2) gives a'_k = a_k XOR delta_k XOR sigma_k XOR eps_k
= a_k XOR kappa_k. Both carries into bit 0 of each pair of sums are 0, so
gamma_0 = kappa_0 = 0. The carry into bit i + 1 of a sum is the majority of
its two input bits at i and its carry into bit i; with the relations at i + 1
and at k + 1 this is (C1) and (C2). QED.

For the record, gamma_0 = 0 for both rows; bit 0 of E' is E_0 XOR DY3_0 = E_0
XOR 1, so delta_0 = 1 for every E, and sigma_0 XOR eps_0 = 1 for both rows, so
kappa_0 = 0 for every proposal (the participant's arithmetic script).

**Lemma FM (forced positions).** Put F = (gamma AND 7fffffff) OR ROL((sigma
XOR eps) AND 7fffffff, 12). At a position i with F_i = 1, given u_i and a_k
for k = (i + 20) mod 32, at most one value of h_i is allowed by (C1) and (C2):

(a) if gamma_i = 1 and i < 31, (C1) holds only for h_i = Q_i XOR gamma_(i+1)
    when eta_i = 0, and only for h_i = u_i XOR 1 XOR gamma_(i+1) when eta_i =
    1;
(b) if (sigma XOR eps)_k = 1 and k < 31, (C2) holds only for f_k = E_k XOR
    sigma_k XOR kappa_(k+1) when a_k = E_k, and only for f_k = E'_k XOR
    kappa_(k+1) when a_k != E_k; that is, only for h_i = f_k XOR y_i XOR Q_i
    XOR u_i with this f_k.

When both (a) and (b) apply and give different bits, no h_i is allowed.

Proof. Two facts on the majority: if exactly one input of maj is complemented,
the value changes exactly when the other two inputs differ; if exactly two are
complemented, it changes exactly when those two are equal. (a) gamma_i = 1
complements the carry input of (C1). If eta_i = 0 that is the only
complemented input, so the left side of (C1) is Q_i XOR h_i, and (C1) gives
h_i = Q_i XOR gamma_(i+1). If eta_i = 1 the h input is complemented too, so the
left side is 1 XOR h_i XOR u_i, and (C1) gives h_i = u_i XOR 1 XOR
gamma_(i+1). (b) In (C2) the E, f and carry inputs are complemented by
delta_k, sigma_k and kappa_k, and delta_k XOR kappa_k = sigma_k XOR eps_k = 1,
so exactly one of the E input and the carry input is complemented. If it is the
E input (E'_k = 1 XOR E_k, kappa_k = 0), the left side of (C2) is f_k XOR a_k
when sigma_k = 0 and 1 XOR f_k XOR E_k when sigma_k = 1. If it is the carry
input (E'_k = E_k, kappa_k = 1), the left side is E_k XOR f_k when sigma_k = 0
and 1 XOR f_k XOR a_k when sigma_k = 1. In each of the four cases (C2) fixes
f_k: to a_k XOR kappa_(k+1), E'_k XOR kappa_(k+1), E_k XOR kappa_(k+1) and 1
XOR a_k XOR kappa_(k+1) respectively; splitting each case on a_k = E_k or a_k =
1 XOR E_k, each equals the formula of (b). Then h_i follows from f_k = y_i XOR
Q_i XOR h_i XOR u_i. QED.

*The traversal.* A node is a frame of five words: the depth i (0 to 32), the
low i bits of h, u_i, a_k for k = (i + 20) mod 32 (for i = 32, a_20), and the
seed s. The solver runs the traversal twice, with s = 0 and with s = 1, each
from the node (0, 0, 0, s, s): u_0 = 0, and the carry into bit 20 of E + f is
guessed to be s. Nodes are kept on a stack (last in, first out). A node of
depth i < 32 is expanded: the allowed values of h_i are the value of Lemma FM
if F_i = 1 (none if (a) and (b) disagree) and both values otherwise; for each
allowed h_i the solver computes g_i and f_k, the next carries u_(i+1) =
maj(Q_i, h_i, u_i) and a_(k+1) = maj(E_k, f_k, a_k), drops the value if i < 31
and (C1) fails or if k < 31 and (C2) fails, sets the next a to 0 when k = 31
(the carry into bit 0 of E + f; the carry out of bit 31 is discarded), and,
when i = 31 (so k = 19 and the next a is a_20), drops the value unless a_20 =
s; otherwise it pushes the child (i + 1, the low i + 1 bits of h, u_(i+1), the
next a, s). A node of depth 32 is a *candidate* h. For a candidate the solver
(i) evaluates (J1), (J2) and (J3) on the full words; (ii) if they hold,
inverts h to c1 by the lines of Lemma IP62 read backwards, checks that c1 is in
the cube, runs step CT62, checks t != 0, checks (E1) for the row's tau and eps
with the trial's b and a, computes both last-block compressions of the trial in
full (Section 1, counter t, v[13] = 0, flags 3, lengths 62 and 64, blocks of
step CS62) and compares the two chaining values; (iii) returns c1 if all of
these hold.

**Lemma LS (the solver lists every root).** For a raw proposal and a row whose
masks meet, the solver returns exactly the members c1 of the cube with t != 0
whose trial completes the collision of the last-chunk chaining values with the
row's outcome, each once.

Proof. A returned c1 passed (ii): it is in the cube, its t is not 0, its two
chaining values were computed in full and are equal, and its outcome is the
row's by (E1). Conversely let c1 be such a member, and h = E3.h1 of its trial.
By Lemma RES, h satisfies (J1) and the trial's f satisfies (J2), and (J3) and
(E1) hold; by Lemma CR the true carries satisfy (C1) at every i < 31 and (C2)
at every k < 31. Take the traversal whose seed is the true carry into bit 20 of
E + f. By induction on i it reaches the node with the low i bits of h, the true
u_i and the true a_k: at a forced position the true h_i is the value of Lemma
FM, the only value that (C1) and (C2) allow, and at a free one both values are
tried; the true next carries satisfy (C1) and (C2); the true carry into bit 0
of E + f is 0; and at i = 31 the computed a_20 is the true carry, which is s.
So h is a candidate; it passes (i) and (ii), and c1 is returned. In the other
traversal, any node with the low bits of h carries the true a_k from k = 0 on,
because a_0 = 0 is set at k = 31, so at i = 31 its computed a_20 is the true
carry, which is not that seed, and h is not a candidate there. Distinct h give
distinct c1 (Lemma IP62), so c1 is returned once. QED.

*Tree size.* Let the free positions be the i with F_i = 0, d their number and
b_i the number of free positions below i. A node of depth i has at most one
child at a forced position and at most two at a free one, so one traversal has
at most 2^(b_i) nodes of depth i and at most 2^d candidates:

    N_internal = sum over i = 0..31 of 2^(b_i),   leaves = 2^d,
    N_total = N_internal + leaves.

| tau | gamma | F | free h positions | N_internal | leaves | N_total | C_row |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| aaaf751e | 09b038ee | 1bf7bdee | 0,4,9,14,19,26,29,30,31 | 949 | 512 | 1461 | 8948640 |
| aaaf771e | 098038ee | 1bc7bdee | 0,4,9,14,19,20,21,26,29,30,31 | 3189 | 2048 | 5237 | 35595168 |

(sigma = fff8cf91 and fff8cc91, theta = 8cf91fff and 8cc91fff, lam = f9a010df
for both rows; every word of the table is recomputed by the participant's
arithmetic script.)

*Charges of one row.* A call for one row costs at most

    C_row = 8192 + 288 * N_total + 16640 * leaves:

- 8,192 for its setup: E', delta, kappa, gamma, sigma, theta, lam and F, and
  for each depth i a descriptor of at most 16 one-bit words (Q_i, y_i, eta_i,
  gamma_i, gamma_(i+1), E_k, E'_k, sigma_k, kappa_k, kappa_(k+1), the flags of
  (a) and (b), the flags k = 31 and i = 31, and the word 2^i), each made by one
  shift, one AND and one store, 32 * 16 * 3 = 1,536 units, and the two seed
  frames;
- 144 for every node popped, in each of the two traversals, 2 * 144 = 288 per
  node of N_total. Popping the frame costs 8 (5 loads, 3 for the stack
  pointer and the empty test) and the address of its descriptor 2. One
  attempt, for one value of h_i, costs at most 61: at most 15 loads of
  descriptor words, g_i and f_k (3), the four majorities with their
  complemented inputs (20), the tests of (C1) and (C2) with their flags (8),
  the reset and the seed test (5), the child's prefix and depth (4) and the
  push (5 stores and 1 for the stack pointer). A free node loads and tests the
  two flags (6) and makes at most two attempts: at most 8 + 2 + 6 + 2 * 61 + 4
  = 142 units with 4 of loop control. A forced node computes the value of
  Lemma FM (at most 17 operations and 8 loads) and makes one attempt: at most
  8 + 2 + 25 + 61 + 4 = 100. A node of depth 32 is popped and dispatched in at
  most 16;
- 16,640 for every candidate of each traversal, at most 2 * leaves of them:
  128 for (i), the full-word checks (at most one rotation and 9 other
  operations per equation, and at most 12 loads), and 8,192 for (ii): the four inverse lines
  and the cube test, the 16 lines of step CT62 and the test of t, the check of
  (E1), at most 12 units a line and 512 in all with control; and the two
  complete last-block compressions, each 16 calls of 8 assignments of at most
  10 units with their loads and stores (1,280), plus the 16 state words, the
  16 message words and the 8 chaining-value words (at most 128), and the
  comparison of the two chaining values (at most 64): at most 512 + 2 * 1,408
  + 64 = 3,392 units, within 8,192.

Hence Cmax = 8,948,640 + 35,595,168 = 44,543,808. The frames, at most 64
pending slots, the descriptors and the saved parents are memory resident with
charged accesses; the frame's five words, at most eight descriptor bits and
three temporaries are live at once, within 16 registers. Every candidate is
checked; no average tree size, observed root count or cheaper check for
successful candidates only is used. Cmax is a deterministic upper cap and is
charged at every solver entry, even when only one row is active.

## 12. The advice record and the procedure that found it

**12.1 The record.** The search reads 19 fixed 32-bit words, 76 bytes, as
nonuniform advice:

    pin (8.2)     W4 = a40d3321   X3 = 435d473f   X7 = 9895859e
                  X11 = 9003b0e0  X15 = a7590cb9  W13 = b2077fc6
    class (10.1)  eta = 85492711, mask 27118549, value 07118049
    cube (10.1)   beta = f5519714, mask 19714f55, value 00000051
    eps (10.2)    2559f8e8
    row 1 (11.4)  tau = aaaf751e, gamma = 09b038ee, F = 1bf7bdee
    row 2 (11.4)  tau = aaaf771e, gamma = 098038ee, F = 1bc7bdee

That is 6 + 3 + 3 + 1 + 3 + 3 = 19 words, 76 bytes, declared as
nonuniform_advice_log2_bytes = 6.248 (76 < 2^6.248). The automaton tables are
computed from the record and charged (D_tables = 2^29, 11.3); they are not
advice. The procedure that found the record, SEL, is written out and charged
in 12.2.

**Lemma ADV (the record enters only through exact facts).** Of the record, the
success bound of Section 15 uses only (a) to (c), each a finite computation on
the displayed words that this text carries out exactly; everything else it uses
is the declared premises H1-62 and H4-62, statements about the sampler of 11.1
with the record fixed:

(a) K + W4 = 0000003e and Fact P62 (8.2), which give Lemma H62 and part (ii)
    of Theorem C62;
(b) the class is the cube of Lemma FB for m = ROL(eta, 16) and d = DY3, with
    2^20 members (10.1), which gives part (iii);
(c) the cube is the cube of Lemma FB for m = ROL(beta, 12) and d = DY11, with
    2^16 members (10.1), which gives part (iv).

eps and the words tau, gamma and F of the two rows enter only as parameters of
the filters and the solver, whose properties (Lemmas RES, NEC, AUT, CR, FM and
LS) are proved here for every value of these words; the counts L and N3Sigma of
10.3 enter only the extrapolation of H1-62, the choice f = 51. No statement
about how the record was found, or about what SEL returns, is used.

Proof. The success bound of Section 15 combines H1-62 (ii), H4-62 and the
exact part. The exact part is Theorem C62 with Lemma TR; its proof reads the
record only through the condition of Lemma L62 on W4, Fact P62 and Lemma FB
for the class and the cube, that is through (a) to (c). Lemmas RES, NEC, AUT,
CR, FM and LS assume (a) to (c) and nothing else of the record; the filters
and the solver are built from the record's words by 11.2 to 11.4. QED.

**12.2 The selection procedure SEL.** The record was found by computation that
the submitted program does not contain. This section writes that computation
as a procedure, SEL, and charges its whole cost as preprocessing, included in
T (Section 13). The charge is a bound by construction: every program run of
SEL is over the range stated here and halts as soon as it has executed 2^58
primitive word operations, its cap, or holds 2^36 bytes; a run that halts so
returns nothing, and SEL goes on. Operations are counted as in Section 11, 430
to a target compression. SEL runs six programs of the participant that are not
in the package, one run each, in five steps.

*Step 1, the pin (one run).* Put W4 = 0000003e - K = a40d3321, so that K + W4
= 3e (Lemma L62), and a1 = 7ffffffe, the first value of C3 on message A. The
participant's pin search draws pairs (X15, X11) from a xorshift generator with
seed 7, at most 30,000,000 pairs. For each it computes C3's second and third
values on both messages (first values a1 and a1 + 2), counts with a carry
recurrence the words that, as the common sixth value, give equal b outputs,
and, when there are at most 2^20 of them, walks them; for each it solves for a
fourth value whose two fifth values give that common sixth value, sets X7 from
the fourth assignment and W13 from the fifth, and checks both executions of C3
in full. It stops after two pins. SEL takes the first,
with X3 = a1 - X7 - W4.

*Step 2, the census and the grid (two runs).* With DY3 and DY11 of Fact P62
for the pin of step 1, the participant's census program lists, for each of the
two differences d, every mask m whose fibre {x : x XOR (x + d) = m} is not
empty, with the mask and value of its cube (Lemma FB), by the distinct carry
paths of x + d: 431,544 masks for DY3 and 846,737 for DY11. The participant's
pair program keeps the beta = ROR(m, 12) of the DY11 list whose cube has 2^16
members, with beta even and of weight 16 (341 of them), and the eta = ROR(m,
16) of the DY3 list whose class has 2^20 members, with eta of weight 12 (76),
forms the pairs (eta, beta) in which (eta XOR beta) AND ff has an even number
of one bits, 15,180 pairs, and gives each the solution eps of (EPS) with bit 0
equal to 0.

*Step 3, the screen (one run).* For each pair and each of the 2^28 words tau
with tau AND 3 = 2, bit 8 of tau equal to 1 and bit 21 of tau equal to bit 20
of tau XOR bit 0 of eta, the participant's screen program, on a graphics card,
applies carry tests of (J1), (J2) and (J3) and a carry test of (E1), and
outputs the rows (eta, beta, eps, tau) that pass all of them.

*Step 4, the counts (two runs).* The participant's E1 counter computes L
(10.3) for each row of step 3, and the participant's E3 counter computes
N3Sigma for each row with L > 0.

*Step 5, the choice.* SEL outputs the pair with the largest sum of L * N3Sigma
over its rows, the first in the order of step 2 if two sums are equal, with
its eps, the masks and values of its class and cube, its rows with L * N3Sigma
> 0 and their words gamma and F (11.4); EMPTY if no sum is positive. The
bookkeeping of SEL runs under a cap of 2^50 operations.

**The bound.** Six program runs and the bookkeeping cost at most

    S_SEL = 6 * 2^58 + 2^50 = 1,730,508,156,817,113,088

operations, below 2^60.5859, and with the tables, (S_SEL + 2^29) / 430 <
2^51.8378 target compressions: preprocessing_log2 = 52 is this bound rounded up
to a whole number, and the whole of S_SEL and of the tables is in T (Section
13). The bound holds for SEL as defined, whatever the programs do inside and
whatever they return, because every run halts at its cap and every loop has
the range stated. SEL is not a premise of this package, and no heuristic is
declared for it.

*What rests on records.* The bound rests on no record. That SEL returns
exactly the record of 12.1 rests on the participant's records of the runs. The
pin search, run again with the same arguments, prints this pin first, in 0.01
s of one processor core with 1.9 MB of memory. The census program and the pair
program, run again, write files byte-identical to those of the records, in 6.9
s and 1.8 s of one core; a separate program checked the census over all 2^32
words of each difference. The screen ran in 31.5 s on one graphics card and
passed 225,014 rows; the E1 counts of these rows ran in 527 s on that card and
found 461 rows with L > 0; the E3 counts of the 461 ran in 177 s of processor
time and found exactly two rows with N3Sigma > 0, the rows of 10.2, both in the
pair (85492711, f5519714) with eps = 2559f8e8. At 2^46 operations a second for
the card and 2^42 for a processor core, rates the participant states and does
not prove, every run stayed below 2^56 operations, inside its cap. The
programs and the records are not in the package. If a record were wrong, SEL
could return other words or none; its cost would stay within the bound, and
the analysis uses only the stated words of 12.1 (Lemma ADV).

*Memory of SEL.* Every program run of SEL halts when it holds 2^36 bytes, and
SEL runs one program at a time; the files that SEL keeps between runs (the
census lists, the pairs, the passed rows and their counts) stay below 2^29
bytes. SEL therefore holds fewer than 2^36 + 2^29 bytes at any time.

## 13. Charged time

**13.1 The budgets.** With the success convention of the participant's counter
entries (an expected count of 0.49676 listed roots), N_c = 2^16 and f = 51:

    B  = ceil(0.49676 * 2^128 / ((N_c - 1) * f))
       = 50,575,779,322,124,053,188,182,925,749,242;
    J  = B / 7 = 7,225,111,331,732,007,598,311,846,535,606;
    LE = ceil(17/16 * B * pE) = 219,723,112,305,481,250,688,653,171,096;
    L2 = ceil(17/16 * B * p2) = 2,871,968,522,982,158,364,169,218,308.

B is the least integer with B (N_c - 1) f / 2^128 >= 0.49676, and 7 J = B; the
participant's arithmetic script computes each value from the displayed formula
in exact rational arithmetic. Writing the two messages and verifying them in
full is reserved at 2^38 compressions: each message is shorter than 2^42 bytes,
so its hash needs fewer than 2^36 block compressions in its chunks, fewer than
2^32 parent compressions and one root compression, and both together fewer
than 2^37.1; writing the 1024 t zero bytes of F, fewer than 2^37 stores of
256-bit words, is below 2^29 compressions.

**13.2 The operation bound.** Every budget is charged at its bound plus one,
for the overflowing budget-check attempt; the tables (2^29) and 16 boundary
units are added:

    O_run = 29120 * J + 80 * (LE + 1) + (4128 + 44543808) * (L2 + 1)
            + 2^29 + 16
          = 338,353,089,784,844,219,711,771,094,306,765,632 machine units.

| term | value | log2 |
| --- | ---: | ---: |
| batches, 29120 * J | 210395241980036061262840971116846720 | 117.3406 |
| Q lookups, 80 * (LE + 1) | 17577848984438500055092253687760 | 103.7935 |
| solver entries, (4128 + 44543808) * (L2 + 1) | 127940269955823719948875030399360224 | 116.6230 |
| tables, boundary | 2^29 + 16 | 29.0000 |
| SEL (12.2), S_SEL | 1730508156817113088 | 60.5859 |

With 430 machine units per target compression,

    T <= (O_run + S_SEL) / 430 + 2^38.

**13.3 The claim.**

    T <= N / 430,   N = O_run + S_SEL + 430 * 2^38
                      = 338,353,089,784,844,221,442,397,448,623,864,640,

and log2(N / 430) = 109.2778200345... The claimed scalar is 109.2779, the
bound rounded up at the fourth decimal. Integer check, exact:

    N^10000 < 2^1092779 * 430^10000   (so T < 2^109.2779),
    N^10000 > 2^1092778 * 430^10000   (so 109.2778 would not bound T).

The preprocessing (the tables and SEL) is included in this bound.

## 14. Memory, preprocessing and advice

*Memory.* The search holds the lookup tables, 9,728 256-bit words, 311,296
bytes (11.3); the solver's frames, at most 64 pending slots and 32
descriptors of at most 16 words; the names of step CO62, the stored coins of a
batch, the counters and the 76-byte record: in all below 2^21 bytes with the
code. The output, the two messages with their digests, takes fewer than 2^43
bytes. SEL holds fewer than 2^36 + 2^29 bytes (12.2). Held at once, these
total below 2^43 + 2^37 < 2^44: memory_log2_bytes = 44 bounds everything held
at once, the computation that found the record included. The cost model does
not score memory.

*Preprocessing.* The once-only work is the tables (2^29 units, 11.3) and SEL
(S_SEL, 12.2): (S_SEL + 2^29) / 430 < 2^51.8378 target compressions, declared
as preprocessing_log2 = 52 and included in time_log2.

*Advice.* The search reads the record of 12.1: the six pin words (24 bytes) and
eta, the class mask and value, beta, the cube mask and value, eps, the two tau,
the two gamma and the two F words (52 bytes), 76 bytes in all, declared as
nonuniform_advice_log2_bytes = 6.248. The tables are computed and charged, not
stored as advice. The computation that found the record is SEL, charged at its
cap; nothing in the record is free.

## 15. Premises and the status of their evidence

The time bound of Section 13 is an operation bound: given the record of 12.1,
it uses no premise about the law of any word, since every count halts at its
budget and is charged at it, and SEL is charged at its cap. The success
probability uses two premises, both declared as heuristics of claim.json;
neither is a statement about a selection procedure (Lemma ADV).

**H1-62 (score-critical).** For the actual sampler of 11.1 (the pin of 8.2,
members of the class, r and z drawn as stated, the two outcome rows), (i) the
expected number of valid listed roots of one raw proposal is at least (N_c -
1) * f / 2^128 = 65535 * 51 / 2^128, and (ii) the probability that the
unhalted run of B raw proposals has no listed root is at most exp(-0.49676) +
0.001. *Status:* declared, not proved. The local exact counts of 10.3
(recounted independently) give the model mass mu; the factor f is five
sevenths of the model rate, rounded down. Neither the local mass of E1 and E3
nor the number of free words of the construction proves this physical first
moment or the dependence clause. The 55/63 premise H1 of the participant's
earlier entries is not transferred. No measurement of any rate of this path
exists: the organizer-run experiments run the 55/63 root instance, and no
implementation of this path has been run.

**H4-62 (supporting).** The probability that the count of E-positive proposals
exceeds LE or the count of solver entries exceeds L2 is at most 0.0005. A
sufficient form: the raw proposals are independent and P(E-positive) <= 1.06
pE and P(both masks meet) <= 1.06 p2; Chernoff then gives the budgets, each
ceil(17/16 * B * share). *Status:* declared, not proved, not measured. The
shares pE and p2 are exact for uniform independent input words (11.2); the
sampler's Q and E are not proved uniform. The time bound does not depend on
this premise.

*Success.* Conditional on H1-62 and H4-62, with the record of 12.1 fixed (Lemma
ADV), the run succeeds with probability at least 1 - (exp(-0.49676) + 0.001) -
0.0005 = 0.3900009..., so at least 0.39: with probability at least 1 -
exp(-0.49676) - 0.001 the unhalted run has a listed root (H1-62 (ii)); the
filters lose none of them (Lemma NEC) and the solver lists every one (Lemma
LS); and with probability at least 1 - 0.0005 no budget halts the run (H4-62).
The filters' necessity, the automata and the solver's listing of every root
are Lemmas NEC, AUT, CR, FM and LS, proved in Section 11.

## 16. Scope, the program and earlier entries

*Organizer-run program.* The experiments and their program are those of the
participant's entry 26ebba63, unchanged: the half-collision and the toy-scale
residual search of the 55/63 root instance (Sections 4 to 6). They check the
compression and the 55/63 half-collision on real digests. They do not run this
path and are not evidence for its exact part, its counts or its premises; the
exact part of this path rests on Sections 8 to 11, which are finite
computations and algebra.

*What is the same as the participant's 55/63 counter entries.* The compression
(Section 1), the inversion of one call (Section 2), the tree lemma (Section
7), the outer basis and order of the counter construction, the solved counter
and the inner permutations (Lemma IP62), the success convention 0.49676 and the
budget rule ceil(17/16 * B * share).

*Earlier entries,* one line each:

| entry | time_log2 | kept in this text |
| --- | ---: | --- |
| 26ebba63 | 71.39 | the program and the experiments, unchanged |
| 0f409bf9 | 109.2779 | the construction, the record and the run of this path |

## 17. Credit

One line per contributor; a credit is not an endorsement.

- **GPT Sol 6.1 (OpenAI)**, an AI model run by the participant: the 62/64
  length pair and its even difference, the extended construction with w14 and
  w15, the row equations, the class and cube census and the grid of pairs,
  the counts L and N3Sigma, the existence automata, the solver's forced
  positions and two-seed traversal with its caps, the charges P7, q7 and U and
  the premises H1-62 and H4-62, all restated and proved in this text.
- **Jbenisek**, the participant who files this package: the counter
  construction of the participant's entries, Sections 1 to 7 and the outer
  step of Section 9.
- **Helper agents of the participant**, instances of the AI model that wrote
  this text: the pin search, the census and pair programs, the screen, the
  exact counts of L and N3Sigma and their independent recount, the arithmetic
  script and this text.
- **5kyguy**, a participant on this track: keeping masks in registers across
  the loop over the members, used in the 55/63 batch of 6.5.
- **tekkac**, a participant on this track: the lane layout of 6.5, from the
  public ticket 2bf40fb.

No priority or novelty claim is made.
