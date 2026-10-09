# A last-chunk half-collision and a chunk-counter search for 2-round BLAKE3

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
separately reported resource bound.

This exploratory package targets blake3-r2-prefix-v1. It has an exact part and a
heuristic part, and it keeps them apart. It uses the counter construction of
entry e7b17fd1 (time_log2 84.98) with a new search over it (Section 9), the
method of GPT Sol's answer AK: for each *frame*, six of the seven outer words
and a member of the sub-class, one table of 2^32 entries solves an exact 32-bit
equation for the seventh outer word, so that the third value c1 and the a output
of the round-1 call E1 are both prescribed. In this package each frame is drawn
fresh together with its own value of the seventh outer word and serves that one
outer step only, its table built again every time, so that the frames are
independent outer steps of the kind that the reviewed entries (judged plausible_not_refuted) on this track
assume. It is the search of entry 9a9f3b7b with the one premise removed for
which that entry was ruled not evaluable, a premise on the good trials of a
whole frame of 2^32 outer steps, at a higher time bound (Section 15). It
continues entry 64c075ac (92.53) of the same participant with the same block
lengths, six constants, sub-class of Y4 and rule A, without the clusters of that
entry. Section 14 corrects the text of entry c66f230d, Section 15 says what is
the same as entries 64c075ac and e7b17fd1 and what is new, with the history of
entry 9a9f3b7b, and Section 16 credits the people and models whose work is used.

**Exact part.** An explicit construction maps seven 32-bit words, a member y of
a set of 131,072 values and one more word c1 to a number t and to a 55-byte
string A and a 63-byte string B. When t is not zero, F || A and F || B, with F
a string of t full chunks of 1,024 bytes, are messages of 1024 t + 55 and 1024
t + 63 bytes whose last chunks are A and B, and the 2-round compressions of
these last chunks, with chunk counter t and flags 3, give chaining values that
agree on their words 0, 2, 5 and 7, that is on 128 of their 256 bits. There is
no search in this and no probability: it holds for every choice (Sections 7 and
8). In the organizer's tree mode the digest of such a message depends on F and
on the chaining value of its last chunk alone (Lemma TR), so a pair whose
last-chunk chaining values agree in all eight words is a collision of two
complete messages. The number t is not chosen: it is the chunk counter that the
round-0 call K0 reads, solved per trial as t = ROL(K0.d1,16) XOR K0.a1. It
takes up the freedom of the message word w0, and that is what lets the
construction prescribe c1, the third value of the round-1 call E1, next to y.
The search holds c1 inside the set Q* of the 2^21 words for which the
first-half b difference of E1 is beta* = 18b0e098, the difference with the
largest conditional collision rate (Section 10.1).

**Heuristic part.** A collision needs the other four words of the chaining value
to agree as well. The algorithm draws FRAMES = 843,790,834,046,997,321,198 =
2^69.516 frames at random, each with its own value of the seventh outer word,
D2.a1, so that each frame is one outer step of 2^21 trials and the frames are
independent. For each it builds the table of the 2^32 values of D2.a1, keyed by
one 32-bit word that each value gives, keeps the key K* of its own D2.a1, and
scans a fixed table of 53 * 2^26 = 3,556,769,792 records of the call E1 alone:
the values of c1 in Q* and E1.a2, with a pattern of E1.b1, that give one of the
seven E1 outcomes of beta* with which a collision is counted. A record that the
frame keeps and whose word equals K* gives the trial of the frame with exactly
that E1, and only these trials are formed and tested in full, at most 2^21 in a
frame (Section 9). The frames cover 2^90.516 trials. One heuristic is declared,
H1', in the form of the reviewed entries (judged plausible_not_refuted) on this track: that the valid trials (t
not zero) satisfy rule A and complete the collision with one of the seven
outcomes at a rate of at least 5/7 of the model's rate for this prescription,
(5/7) * 1033 * 2^-101 = 2^-91.473, and that the good trials of one outer step of
2^21 trials do not cluster beyond the bound of those entries. Under it the
search succeeds with probability at least 0.40. No premise on a whole frame and
no root cap is needed: the work of a frame is bounded whatever its words.
Building the table again for every outer step costs most of the
2,443,836,395,520 machine units, below 2^41.153, of a frame, and the time is
charged below 2^101.91954 target-compression units, the selection procedure of
Section 12, charged in full, and the final step included: the claimed scalar is
101.9196. The search needs less than 2^39 bytes of memory, almost all of it for
its two tables; its two messages are shorter than 2^42 bytes each, and the
declared 2^44 bytes cover them, the code, the search and the selection
procedure, even all held at once (Section 12).

The rate in H1' is an assumption. Under the seven-word model of Section 13,
prescribing c1 in Q* multiplies by 2^11 the part of beta* in the rate of the
sub-class: the rate is 2^11 * 67,698,688 = 138,646,913,024 times 2^-128, which
is 747.92 times the model rate of a trial of entry 64c075ac, and the
conditioning leaves the law of the other call, E3, unchanged (Lemma S1, proved
by another AI model, GPT Sol 6.1). The figure 67,698,688 is the sum of seven
exact outcome counts of the participant's counter, reconciled by that model; the
counting program is printed in Section 17. Whether the trials of the
construction realise that conditional law, to at least 5/7 of its rate, is the
part that is not proved, and it is declared as H1'; Lemmas S2 to S4 prove parts
of it, and Lemma S8 states how weak the dependence inside one outer step has to
be.
Participant measurements on real counter trials reach events of probability
about 2^-31.7 and agree with the model, and a scaled-down end-to-end run with
real collisions of complete messages realises the predicted gain of the
prescription at 0.94 +- 0.13 of its value (Section 13). No run reaches a
collision at 32 bits, and the search of Section 9 has not been run at any size.
At half the counted rate, the convention of the earlier entries on this track,
the same search gives time_log2 = 102.4342; at the uniform rate it needs
2^106.043 frames and gives 138.4468 (10.4).

No full 2-round collision is exhibited, and the search is far beyond feasible
computation. The two declared experiments run the root instance of the same
construction: single chunks of 55 and 63 bytes, compressed with counter 0 and
flags 11 (Sections 4 to 6). An organizer experiment tests an event on the two
complete digests, and the half-collision of the counter instance lies in the
chaining value of a chunk that is not the root, which the parent and root
compressions above it mix: no digest experiment can show it (Section 6.4). What
the experiments exhibit, and what the organizer's runner checks, is the exact
half-collision of the root instance and a toy-scale search over the sub-class.
The program the organizer runs also contains the counter construction, its
counted batch, the outer filter and the walk over outer steps, a machine that
counts their operations and loads, and a self-test of the batches and the filter
(Sections 6.5 and 9.3), whose counts and checks the organizer does not check.
It does not contain the search of Section 9, which exists only in this text.

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

*The same compression in a last chunk.* Sections 7 to 9 use the same
compression, with the same names, as the compression of the last chunk of a
longer message: there v[12..15] = (t mod 2^32, t >> 32, n, 3), with the chunk
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
flags 11 (Section 1). The counter instance, which the claim uses, is built in
Section 8 from the same constants (6.4).

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
searched and not all of it because, under the model of Section 13, the rate of
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
of its trials has a zero residual. How much it loses is answered in Section 13:
inside the sub-class the rule keeps all but 19,086.08 of the 185,377,197.55
counted, and for the difference beta* that the counter search uses it keeps all
of it, 67,698,688 of 67,698,688, because in every outcome of beta* every
solution satisfies rule A (10.1). On the whole class the same eight conditions
would keep less than half of the count; the rule is a rule for this sub-class
only.

**6.4 The root instance and the two declared experiments.** Sections 4 to 6
build the *root instance* of the construction: its messages are single chunks
of 55 and 63 bytes, and the colliding compression is the root compression, with
counter 0 and flags 11 (Section 1). The claim of this package is made for the
*counter instance* of Sections 7 to 9, whose messages have 1024 t + 55 and 1024
t + 63 bytes and whose colliding compression is that of the last chunk, with
counter t and flags 3. The two instances share the six constants, Fact P,
Lemmas L and H, the class and the sub-class, rule A, Lemmas N and A and the
machine of 6.5; they differ in the counter and the flags that the compression
reads, and in the order in which the construction solves the assignments of
rounds 0 and 1 (Sections 4 and 8).

The two declared experiments run the root instance of the same construction,
counter 0 and flags 11. An experiment of the organizer's harness returns pairs
of complete messages and tests an event on their two digests, while the
half-collision of the counter instance is an agreement of four words of the
chaining value of a chunk that is not the root. The parent and root
compressions above that chunk mix all eight words, so the digests of a counter
pair are not expected to agree on the masked words, and on two counter pairs
with t = 1 they do not (Section 7). No digest experiment can show a
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

Neither experiment runs the counter construction or its batch, and neither
measures a rate of the counter search. A search of the root instance over all
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
  holds the constant STAGE_2_BUDGET, the budget E of the counter search (9.1);
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
credited in Section 16. Under the convention of entry c66f230d, with every read
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
construction and the counter batch of Sections 8 and 9, and the machine that
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
the self-test (9.3), reported under the key `counter` of the same line, and the
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
are shorter than 2^42 bytes (Section 8). The tree, its counters and flags and
its root output are those of the target profile. The two messages of a pair are
complete messages of the domain, and a pair with equal digests is an ordinary
collision, not a free-start or compression-only one. The converse of (c) is not
used.

*The digest does not show a partial agreement.* When CV_t(A) and CV_t(B) agree
on four words only, the parent and root compressions over them mix all eight,
and the two digests are not expected to agree on a fixed set of words. On two
counter pairs of Section 8 with t = 1, messages of 1,079 and 1,087 bytes, the
chaining values agree on words 0, 2, 5 and 7, and the two digests do not agree
on digest words 0, 2, 5 and 7 (participant computation with the organizer's
code). This is why the declared experiments run the root instance (6.4).

*Participant checks with the organizer's code.* In each of the following the
organizer's `verifier/blake3.py` was imported unchanged; they are participant
computations, which the organizer has not run. (1) For 2,000 trials of the
counter construction of Section 8 in 40 outer steps, 8 of them with outer words
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

## 8. The counter construction

*Words and constants.* The construction has nine free words: the seven *outer
words* C0.d1, D2.a1, D2.b1, S11, S4, X9 and w6 (the program's `CTR_BASIS`); a
member y of the sub-class of 6.1, which becomes the value of Y4; and the *inner
word* c1, which becomes the third value of E1 on message A. The constants are
those of Section 4: X3, X7, X11 and X15, w4 = W4, w13 = W13, w14 = w15 = 0, the
four constant first values K2.a1, K2.d1, K2.c1 and K2.b1 of K2 given in step O,
and Y3, Y11 of Fact P. The compression reads three more values besides the
message and the IV. K3 reads the flags, here 3 (the line for K3.d1); K1 reads
v[13], here 0 (the line for K1.a1); and K0 reads the counter v[12], which is
not fixed in advance: the line for t solves K0's second assignment for it. The
names are those of Section 4.

*The cube Q*.* Q* is the set of the 2^21 words c with (c AND 0e09818b) =
02008000; the program names the mask and the value `CTR_MASK` and `CTR_VALUE`.
Member number j of Q*, for 0 <= j < 2^21, is the word whose bits at the 21
positions where 0e09818b has a zero are the bits of j, in increasing order of
position (the program's `ctr_c1`).

**Step CO (the outer step; 77 lines, from the seven outer words and y).**

    X2 = D2.a1 + D2.b1 + W13;   X8 = ROL(X7,7) XOR D2.b1
    C0.c1 = X8 + C0.d1;   K3.a1 = IV[3] + IV[7] + w6
    K3.d1 = ROR(K3.a1 XOR 3,16);   K3.c1 = IV[3] + K3.d1
    S15 = S11 - K3.c1;   S3 = ROL(S15,8) XOR K3.d1
    K3.b1 = ROR(IV[7] XOR K3.c1,12);   D3.a1 = S3 + S4
    S7 = ROR(K3.b1 XOR S11,7);   D3.b1 = X3 - D3.a1
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

**Step CT (the trial; 16 lines, from c1 and the names of step CO).**

    E1.d1 = c1 - Y11;   E1.a1 = ROL(E1.d1,16) XOR Y12
    Y6 = E1.a1 - Y1 - w12;   Y10 = ROL(Y6,7) XOR C2.b1
    Y14 = Y10 - C2.c1;   E1.b1 = ROR(Y6 XOR c1,12)
    Y2 = ROL(Y14,8) XOR C2.d1;   E3.h1 = ROR(Y14 XOR (Y3 + Y4),16)
    w0 = Y2 - C2.a1 - C2.b1;   E3.g1 = Y9 + E3.h1
    K0.a1 = IV[0] + IV[4] + w0;   E3.f1 = ROR(Y4 XOR E3.g1,12)
    t = ROL(K0.d1,16) XOR K0.a1;   w1 = S0 - K0.a1 - K0.b1
    E1.a2 = E1.a1 + E1.b1 + w5;   E3.e2 = Y3 + Y4 + E3.f1 + w8

**Step CS (the messages).** If t = 0 the trial is invalid and is dropped: a
message with no full chunk before its last chunk has that chunk as its root,
compressed with counter 0 and flags 11 and not with the flags 3 that the line
for K3.d1 used. Otherwise the words w0 to w12 of the lines, with w4 = W4 and
w13 = W13, and w14 = w15 = 0 form the block of A; A is the first 55 bytes of
its little-endian encoding, and B the first 63 bytes of that of the same words
with w4' = W4' and w5' = w5 + fffffff8 in place of w4 and w5, as in steps S2
and S3 of Section 4. F is the string of 1024 t zero bytes, and the two messages
are F || A, of 1024 t + 55 bytes, and F || B, of 1024 t + 63 bytes. In the
program step CO is `ctr_outer`, step CT and the two blocks of step CS are
`ctr_trial`, which returns nothing for t = 0, and the flags are the constant
`CTR_FLAGS` = 3.

*The order and the calls.* Table CT gives each call's eight assignments by the
name that the line for that assignment assigns; the cells K2.a1, K2.d1, K2.c1
and K2.b1 are the four constant values. E1's first five assignments are the
lines for Y6, E1.a1, E1.d1, E1.b1 and E1.a2, in the order of the assignments;
E3's first two assignments are the line for E3.h1, and its third to fifth the
lines for E3.g1, E3.f1 and E3.e2.

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

The order was found by a solver search of the participant's helper agents for
an order in which Y4 and E1.d1 are both free words.

**Lemma CT (the counter order).** (a) *Triangular.* In the printed order, step
CO and then step CT, every line assigns a name that no earlier line assigns and
that is neither one of the nine free words nor a constant, and it reads only
constants, the nine words and names of earlier lines; a line of step CO reads
neither c1 nor a name of step CT. Every line is one assignment of one call
solved for the name on its left; the exceptions are the line for E3.h1, which
is the first two assignments of E3 with the first substituted into the second
(e1 = Y3 + Y4 + w15, w15 = 0), and the line for E3.e2, which uses the same e1.
By Table CT the 93 lines and the four constant values of K2 are, each exactly
once, the eight assignments of each of the eleven calls K0..K3, D0..D3, C0..C2,
with the inputs and the message words of Section 1 for block length 55, counter
v[12] = t, v[13] = 0 and flags v[15] = 3, with w4 = W4, w13 = W13, w14 = w15 =
0, and with the constants X3, X7, X11, X15 as the a output of D3, the b output
of D2, the c output of D1 and the d output of D0; and the first five
assignments of E1 and of E3 for message A, E1 with c input Y11 and E3 with a
input Y3.

(b) *The calls.* For every choice of the nine words, the names of the lines are
the executions of these calls. In particular round 0 on the block of A, with
block length 55, counter t, v[13] = 0 and flags 3, leaves the state X of the
names, with the four constants as X[3], X[7], X[11] and X[15]; C0 has outputs
(Y0, y, Y8, Y12); and in the compression of A, E1.c1 = c1, since E1's third
assignment is E1.c1 = Y11 + E1.d1.

(c) *The levels.* A line of step CO is a function of the seven outer words and
y. Of the message words only w0 and w1 are lines of step CT, and so is the
counter t; every other message word is a line of step CO or a constant. So the
trials of one outer step differ in w0, w1 and t and in nothing else of their
two messages.

Proof. (a) is read off the displays, each formula compared with Section 2 and
with its call's inputs, outputs and message words (Section 1, with v[12] = t,
v[13] = 0 and v[15] = 3); Table CT has one name in each of its 88 cells, all
different, the four constant values of K2 among them, and with the five names
of E1 and the four lines of E3 they are the 93 lines and the four constants.
(b) As in Lemma T2 (b): an assignment solved for one of its terms is an
equivalent equation modulo 2^32 (Fact 1), so a line's assignment holds once it
has run, and by (a) no later line changes its names. By (a) and Table CT all
eight assignments of each call hold, a constant output in its place (the lines
for D3.b1 and D3.d1; X8; D1.c1 and X6; D0.d1 and X10) and y as the b output of
C0 (the line for Y8); by Fact 1 the names are the execution of the call. (c) By
induction over the printed order, with (a): a line of step CO reads only
constants, the seven outer words, y and lines of step CO; w2, w3, w5 and w7 to
w12 are lines of step CO, w6 is an outer word, w4, w13, w14 and w15 are
constants, and w0, w1 and t are lines of step CT. QED.

**Theorem C (the last-chunk half-collision).** For every choice of the seven
outer words, of a member y of the sub-class and of a word c1, steps CO and CT
give a counter t. If t is not zero, step CS outputs two distinct messages F ||
A and F || B of 1024 t + 55 and 1024 t + 63 bytes, with 1 <= t < 2^32, such
that

(i) their last chunks are A and B, compressed with counter t, v[13] = 0 and
flags 3 (Lemma TR (a));

(ii) the chaining values CV_t(A) and CV_t(B) agree on words 0, 2, 5 and 7;

(iii) in both last-chunk compressions Y4 = y, and the XOR difference between A
and B of E3's first-half d value is eta = 830303cf;

(iv) in the compression of A, E1.c1 = c1; and if c1 is in Q*, the XOR
difference between A and B of E1's first-half b value is beta* = 18b0e098.

Proof. t is the XOR of two 32-bit words, so t < 2^32 and t >> 32 = 0, the value
v[13] = 0 that the line for K1.a1 used. The sixteen words have w14 = w15 = 0
and w13 = W13, whose top byte is zero, so A and B are honest strings of 55 and
63 bytes whose zero-filled blocks are the sixteen words and the same words with
w4 and w5 replaced, as in Section 5. By Lemma TR (a) the last chunks are
compressed with counter t, v[13] = 0, flags 3 and block lengths 55 and 63. By
Lemma CT (b) round 0 on the block of A leaves the state X of the names, with
the four constants as X[3], X[7], X[11] and X[15]. The counter, v[13] and the
flags are the same in both compressions, and K2 is the only call of round 0
that reads the block length, w4 or w5; Lemma L, whose proof concerns K2 alone,
therefore gives the same state X for B. Lemma H gives (ii): its proof uses only
round 1 and o[i] = Z[i] XOR Z[i + 8] for i = 0, 2, 5 and 7, and the chaining
value is (o[0], .., o[7]). (iii) As in the proof of Lemma T: C0 reads the same
words of X and w2, w6 in both compressions and has b output y by Lemma CT (b);
w15 = 0, Y14 is the same in both, the a input of E3 is Y3 for A and Y3' for B
by Fact P, and y is in the class, so the difference is eta by the definition of
the class (6.1). (iv) E1.c1 = c1 is Lemma CT (b). E1 has inputs (Y1, Y6, Y11,
Y12) and message words (w12, w5) for A, and (Y1, Y6, Y11', Y12) and (w12, w5 +
delta) for B. Its first and second values are the same for both, so its third
values are c1 and c1 + DY11, with DY11 = Y11' - Y11 = 0a08818b, and its fourth
values are ROR(Y6 XOR c1, 12) and ROR(Y6 XOR (c1 + DY11), 12). Their XOR is
ROR(c1 XOR (c1 + DY11), 12), which is beta* exactly when c1 XOR (c1 + DY11) =
ROL(beta*, 12) = 0e09818b. For words c and x, (c XOR x) - c = x - 2 (c AND x)
modulo 2^32, which is the identity of the proof of Lemma Q; with x = 0e09818b
this holds exactly when 2 (c1 AND 0e09818b) = 0e09818b - DY11 = 04010000. As
0e09818b has no bit 31 the doubling is exact, and it holds exactly when (c1 AND
0e09818b) = 02008000, that is when c1 is in Q*. The messages are distinct
because their lengths differ. QED.

*The counter is the free word.* In the root instance the second assignment of
K0 reads the counter 0, so K0.a1 = ROL(K0.d1,16) follows from the context, and
with it the message word w0. Here that assignment is solved for the counter
instead, which leaves K0.a1, and with it w0, free. The word w0 enters round 1
only in the fifth assignment of C2, and the lines for Y2, Y14, Y10, Y6, E1.a1
and E1.d1 of step CT map their running word one to one, so every value of
E1.d1, and so of c1, can be prescribed in one outer step. With the counter
fixed, no order of the assignments has both Y4 and E1.d1 among its free words,
and with the counter free no order has Y4, E1.d1 and E3.h1 all free: the
counter buys one prescribed word. These two statements are results of a
participant search over the orders, decided by an exact peeling test that was
checked against brute force; nothing below uses them.

**Lemma IP (the inner permutations and the member with t = 0; GPT Sol 6.1).**
Fix the seven outer words and y. (a) The maps c1 -> E3.h1 and c1 -> t given by
step CT are permutations of the 32-bit words. (b) So the 2^21 members of Q*
give 2^21 different values of E3.h1 and of t, and at most one member of Q* has
t = 0.

Proof. With the names of step CO fixed, the lines for E1.d1, E1.a1, Y6, Y10,
Y14 and E3.h1, with e1 = Y3 + y, each map their running word one to one. Read
backwards: Y14 = ROL(E3.h1,16) XOR e1, Y6 = ROR((Y14 + C2.c1) XOR C2.b1, 7),
E1.a1 = Y6 + Y1 + w12 and c1 = Y11 + ROR(E1.a1 XOR Y12, 16). For the counter,
Y2 = ROL(Y14,8) XOR C2.d1 = ROL(E3.h1,24) XOR ROL(e1,8) XOR C2.d1, and the
lines for w0, K0.a1 and t give t = ROL(K0.d1,16) XOR (Y2 + IV[0] + IV[4] -
C2.a1 - C2.b1), where K0.d1, C2.a1, C2.b1, C2.d1 and e1 are names of step CO.
That is a composition of permutations of E3.h1. Its only zero is at E3.h1 =
ROR((ROL(K0.d1,16) - IV[0] - IV[4] + C2.a1 + C2.b1) XOR ROL(e1,8) XOR C2.d1,
24), and the inverse above gives its one value of c1, which may or may not lie
in Q*. QED.

So an outer step has 2^21 or 2^21 - 1 valid trials. Lemma IP bounds the number
of trials that the rule t != 0 drops, one in 2^21 at most; it does not bound
the share of the collision mass that the dropped trial carries (10.3). In the
participant's checks the member with t = 0 was constructed by the inverse above
in 40 outer steps and rejected by the program in 40 of 40; over 8,192 further
outer steps it lay in Q* 4 times, against 4.0 expected, and was rejected 4
times out of 4.

*The length of the messages.* Within one outer step the 2^21 members of Q* give
2^21 different values of t below 2^32 (Lemma IP); over 2,000 trials of the
participant's check t ran from 891,836 to 4,291,586,422 with a mean of log2 t
of 30.56. A pair found by the search has messages of 1024 t + 55 and 1024 t +
63 bytes, shorter than 2^42 bytes and about 2^41 on average. A small t cannot
be chosen: it is the value of a permutation of c1 at the member that the search
finds.

**The outer filter.** Number the seven outcomes of beta* (10.1) j = 1 to 7 in
the order of the table of 10.1, and let tau_j be the tau of outcome j,
sigma_j = tau_j XOR ROR(tau_j, 1) and theta_j = ROL(sigma_j, 12); all seven
have eps = 6e21be55. For an outer step put omega = Y3 + y + w8, with Y3 of Fact
P, y the member of the outer step and w8 the name of step CO; DY3 = Y3' - Y3 =
fdb77cfd is that of Section 6. For a word x:

- condition (1)_j holds for x when some word h gives
  (x + h) XOR (x + (h XOR eta)) = theta_j;
- condition (2)_j holds for x when some word f gives
  (x + f) XOR ((x + DY3) + (f XOR sigma_j)) = eps.

An outer step *passes* the filter when for some j both (1)_j holds for its Y9
and (2)_j holds for its omega. Y9 and w8 are names of step CO and y is drawn
with the outer words, so whether an outer step passes depends on the outer step
alone and on no c1.

**Lemma F (the outer filter; GPT Sol 6.1, answer AC).** Fix an outer step that does
not pass the filter. Then no trial of the outer step, for any word c1, has R = 0
with an E1 outcome among the seven outcomes of beta*. If, as Lemma S6 assumes,
the seven are all the outcomes of beta* that have a solution, then no trial of
the outer step with c1 in Q* has R = 0.

Proof. Take a trial with R = 0 whose E1 outcome is outcome j. Write h, g, f and
e2 for E3.h1, E3.g1, E3.f1 and E3.e2 in the compression of A, and h', g', f' and
e2' for the same values in that of B. Y9 and w8 are the same in both
compressions: w8 is a line of step CO and a word of both blocks, and Y9 is an
output of C1, which reads words of the state X, the same for A and B (proof of
Theorem C), and the message words w3 and w10, which the two blocks share. Both
compressions have Y4 = y and h' = h XOR eta (Theorem C (iii)), and the a input
of E3 is Y3 for A and Y3' for B (Fact P). The conditions of R = 0 (Section 13,
how r is counted) give that the XOR difference of E3's first-half b values is
psi = tau_j XOR ROR(tau_j, 1) = sigma_j, and that of its a outputs is eps' =
eps. Now g = Y9 + h and g' = Y9 + (h XOR eta); f = ROR(y XOR g, 12) and f' =
ROR(y XOR g', 12), so f XOR f' = ROR(g XOR g', 12) = sigma_j gives g XOR g' =
theta_j, and h witnesses (1)_j for Y9. With w15 = 0, e2 = Y3 + y + f + w8 =
omega + f and e2' = Y3' + y + f' + w8 = (omega + DY3) + (f XOR sigma_j), and e2
XOR e2' = eps, so f witnesses (2)_j for omega. So the outer step passes, against
the hypothesis. The second statement follows because every trial with c1 in Q*
has the difference beta* (Theorem C (iv)). QED.

The lemma uses no law of the words: no uniformity, no independence and no
relation between h and f besides the two equations. It does not use rule A or
the rule t != 0. The filter can pass outer steps that hold no success, since
(1)_j and (2)_j are solved with separate witnesses; it cannot reject an outer
step that holds a success with one of the seven outcomes.

**The exact share (GPT Sol 6.1, answer AC; recounted from the program's tables).**
Let pi be the share of the 2^64 pairs (x1, x2) of words such that for some j
condition (1)_j holds for x1 and (2)_j for x2. Then

    pi = 20,504,986,129,465,344 / 2^64 = 312,881,258,079 / 2^48,

about 0.0011115775 = 2^-9.813176.

*Method.* Whether (1)_j holds for x is decided bit by bit from bit 0 upwards.
At bit i the XOR of the two sum bits prescribes the XOR of the two incoming
carries; the state is the set of incoming carry pairs that some choice of the
lower bits of the witness reaches with the lower bits of x, and the next state
is the set of carry pairs out of bit i that some witness bit gives from a pair
of the set that meets the prescription. The condition holds when the set is
still nonempty after bit 31, which has no outgoing carry to prescribe because
the arithmetic is modulo 2^32. For (2)_j the carry of x + DY3 is carried as
well. The seven sets for the seven outcomes are carried together over the same
bits of x, each with its own witness (a subset construction), so one pass over
the bits of x gives its *mask*, the set of j for which the condition holds;
equal states add their counts of prefixes of x, and witnesses are never
counted. A pair passes exactly when the mask of x1 under (1) and the mask of x2
under (2) intersect, so the number of passing pairs is the sum, over pairs of
intersecting masks a and b, of the number of words with mask a under (1) times
the number of words with mask b under (2).

*Certificate.* Masks are written in hexadecimal with bit j - 1 for outcome j
(bit 0 for 175020a0, bit 6 for 685020a0). The numbers of words with each
nonzero mask are 7,936 times the second column under (1), and 1,082,016 times
the fourth and the sixth columns under (2):

| mask, (1) | words / 7,936 | mask, (2) | words / 1,082,016 | mask, (2) | words / 1,082,016 |
| --- | ---: | --- | ---: | --- | ---: |
| 01 | 266 | 01 | 10 | 36 | 30 |
| 02 | 2,044 | 02 | 18 | 41 | 10 |
| 04 | 1,778 | 03 | 5 | 43 | 1 |
| 08 | 254 | 09 | 10 | 49 | 10 |
| 10 | 2,032 | 12 | 22 | 53 | 1 |
| 12 | 2,044 | 13 | 5 | 5b | 2 |
| 18 | 1,524 | 16 | 30 | 62 | 1 |
| 20 | 2,016 | 1b | 2 | 63 | 4 |
| 21 | 1,512 | 1e | 2 | 72 | 1 |
| 40 | 504 | 1f | 8 | 73 | 4 |
| 42 | 1,512 | 22 | 15 | 7e | 2 |
| 52 | 1,512 | 32 | 15 | 7f | 8 |

No other nonzero mask occurs. 4,160,071,168 words have mask 0 under (1) and
4,061,251,840 under (2), so each histogram sums to 2^32: 134,896,128 words
satisfy some (1)_j and 233,715,456 some (2)_j. The sum over intersecting masks
of the products of the scaled counts is 2,387,944, and 7,936 * 1,082,016 *
2,387,944 = 20,504,986,129,465,344. Per outcome:

| tau | words with (1)_j | words with (2)_j | pairs with both |
| --- | ---: | ---: | ---: |
| 175020a0 | 14,110,208 | 86,561,280 | 1,221,397,665,546,240 |
| 185020a0 | 56,440,832 | 190,434,816 | 10,748,299,456,806,912 |
| 275020a0 | 14,110,208 | 86,561,280 | 1,221,397,665,546,240 |
| 285020a0 | 14,110,208 | 47,608,704 | 671,768,716,050,432 |
| 385020a0 | 56,440,832 | 142,826,112 | 8,061,224,592,605,184 |
| 675020a0 | 27,998,208 | 86,561,280 | 2,423,560,722,186,240 |
| 685020a0 | 27,998,208 | 47,608,704 | 1,332,958,397,202,432 |

A pair that passes for several outcomes is counted once in pi and once per
outcome in the last column, whose sum, 25,680,607,215,943,680, is larger.

*The program's automata.* `ctr_automaton` builds the subset construction above
as four byte tables: a state is the carry of x + DY3 (zero for (1)) and, per
outcome, the set of reachable carry pairs, four bits; the table of byte p maps a
state and byte p of x to the next state, and the table of the last byte maps to
the mask. `ctr_tables` builds the two automata once per run from `CTR_TAUS` and
`CTR_EPS`: (1) with eta and the seven theta_j (the program's `ctr_g`), (2) with
DY3, the seven sigma_j and eps. Their numbers of states at the four byte
boundaries are 1, 18, 43, 37 and 1, 3, 7, 7, and their tables have 25,344 and
4,608 entries. `ctr_look` runs an automaton on a word with one table load per
byte, and `ctr_filter` returns the AND of the mask of Y9 under (1) and the mask
of omega under (2); the outer step passes when it is not zero. In a participant
computation the two pattern histograms of the program's own tables equal the
certificate in all 36 nonzero masks and in both zero counts, and their count of
passing pairs is `CTR_SHARE` = 20,504,986,129,465,344; the self-test of 9.3
recounts the latter and checks the automata against brute force.

## 9. The frame search

The search of this section is the method of GPT Sol's answer AK. Its unit is a
*frame*: the six outer words C0.d1, D2.b1, S11, S4, X9 and w6 and the member y.
A frame with a word g as D2.a1 is an outer step of Section 8, and an outer step
with a word c1 is a trial. The search does not run through the trials of an
outer step. It takes from a fixed table the values of c1 and E1.a2 and the
pattern of E1.b1 under beta* that give one of the seven E1 outcomes of beta*
(9.6), and for each of them it finds, with one table per frame, every g whose
trial has these values (9.4, 9.5). Only those trials are formed and tested. In
this package a frame serves one outer step only: its value g* of D2.a1 is drawn
with it, and its table, built in full, is used for that one value (9.1).

**9.1 The algorithm.** The search uses these numbers: RECORDS = 53 * 2^26 =
3,556,769,792, the number of records of the E1 record table (9.6), written Nrec
in GPT Sol's answer AK; and FRAMES = ceil(721 * 2^101 / (1000 * 1033 * (2^21 -
1))) = 843,790,834,046,997,321,198, about 2^69.516, the number of frames, the
least whole number for which FRAMES * (2^21 - 1) q >= 0.515 with q of H1'
(10.3). Each frame serves one outer step. This is the restatement that GPT Sol
gives in Section 3 of its answer AP for removing the premise on whole frames: a
fresh frame for every outer step, with its table built again each time.

0. Before the frames, build the E1 record table of 9.6. It depends on no outer
   word.
1. For each of the FRAMES frames in turn: draw one fresh uniform 256-bit word
   and split it into eight 32-bit words. The first six are the outer words
   C0.d1, D2.b1, S11, S4, X9 and w6, the seventh is the frame's value g* of
   D2.a1, and the eighth, modulo 2^17, is a member number, with y the member of
   the sub-class of that number (6.1). Run the 35 frame lines of 9.4.
2. *Table:* build the table of the frame (9.5): for every word g, the value
   K_O(g) of 9.4, with g linked into the list of that value. When g = g*, keep
   K_O(g*) as the word K*.
3. *Targets:* for each record (c, z, s, j) of the E1 record table in turn, put d
   = c - Y11, a = d XOR ROL(z, 8), u = ROL(d, 16) XOR Y12 and b = a - u - w5,
   with Y12 and w5 of the frame lines. If b AND beta* is not s, go on with the
   next record. Otherwise put H = u - (ROL(b, 12) XOR c) and compare H with K*;
   if they are equal, the record is a *root* of the frame. No list of the table
   is followed.
4. *Certificate:* for each root (c, z, s, j), in turn: run step CO on the outer
   words C0.d1, g*, D2.b1, S11, S4, X9 and w6 and the member y, and step CT with
   c1 = c; drop the root if c is not in Q*, if t = 0 or if E3.h1 does not
   satisfy rule A (6.3); form the two blocks of step CS, compress each with
   counter t, v[13] = 0 and flags 3, and drop the root unless the two chaining
   values agree in all eight words. A root that is not dropped is *certified*.
   For the first certified root, form F || A and F || B by step CS, evaluate
   blake3 of both in full, check that the two digests agree, output the pair and
   halt.
5. After the last frame, halt with failure.

The table of step 2 is built in full although a frame reads only K* from it:
that is the restatement as GPT Sol prices it, and Section 11 charges the whole
table in every frame. Computing K_O(g*) alone, without the table, would cost
less; that variant is not claimed here.

The run halts with failure in exactly one way, a test on a count that the
algorithm keeps: the frames are exhausted. So steps 1 to 3 run at most FRAMES
times, and step 4 runs on at most 2^21 roots in a frame, since different roots
of a frame give different trials of its one outer step and c takes 2^21 values
in Q* (Lemma TG1, 9.6): the work of one frame is bounded whatever its words
(Section 11). A pair of messages is formed and hashed at most once, for a
certified root.

A trial is *valid* when its t is not zero; a valid trial with R = 0 that
satisfies rule A is *good*; a good trial is *listed* when its E1 outcome is one
of the seven outcomes of beta* (10.1). A trial is *E1-listed* when its c1 is in
Q* and its E1 outcome is one of the seven, whatever its E3, its t and rule A.
The trials of a frame are those of its one outer step, with D2.a1 = g* and c1 in
Q*, 2^21 in all. Every listed good trial of a frame is certified in step 4
unless the run ends first, by the output of another pair; every certified root
is a listed good trial of its frame (Lemma TG1, 9.6). A good trial that is not
listed, and a trial with R = 0 that violates rule A, is not found; Section 10
does not count them. When the run outputs a pair, the pair is a collision of two
complete messages: the certified trial has two last-chunk chaining values equal
in all eight words, so R = 0, step 4 has checked both digests, and Lemma TR (c)
says that equal last-chunk chaining values give equal digests.

*What the submitted program holds of this.* The program contains steps CO and CT
(`ctr_outer`, `ctr_trial`), which step 4 runs, the compression `compress2` of
6.5, which it runs with counter t and flags 3, and the test of rule A (Lemma A).
It contains neither the E1 record table, the table of a frame nor steps 0 to 5:
the search of this section is defined by this text only, and no implementation
of it exists; a participant check of the equation that its table solves is
reported in 9.7. The program also holds parts of an earlier search of the same
construction, which walked the outer steps and enumerated all of Q* in those
that pass the filter of Section 8. The search of this section runs none of them,
and the self-test checks them (9.3). They are the outer filter (`ctr_tables`,
`ctr_look`, `ctr_filter`); the walk over outer steps (`ctr_run`), which runs
step CO and the filter for each outer step it is given, skips a failing outer
step, advances a pass count for a passing one, halts with failure when that
count exceeds `CTR_PASS_BUDGET`, and otherwise runs the function of the outer
step that `ctr_run` is given; its counted form `ctr_count`, which charges one
walked outer step on a machine with scalar words; the constants of that walk,
`CTR_FACTOR` = 69,323,456,512, half the count of 10.1, `RUN_OUTER_STEPS` =
ceil(2^127 / (CTR_FACTOR * (2^21 - 1))) = 1,170,306,288,553,394,342,854,
`CTR_SHARE` = 20,504,986,129,465,344, the number of passing pairs of Section 8,
and `CTR_PASS_BUDGET` = floor(RUN_OUTER_STEPS * CTR_SHARE * 17 / 2^68) =
1,382,191,553,723,981,663; and the counted enumeration of all of Q* in one outer
step: `CTR_WORDS` = 299,594, the packed words of seven lanes that hold the
members of Q*, of which the last holds member 2^21 - 1 in all seven lanes (7 *
299,594 = 2^21 + 6); the run-wide table of the packed words RT[j], whose lane i
holds ROL(E1.d1, 16), and DT[j], whose lane i holds E1.d1 = c1 - Y11, for c1 the
member min(7 j + i, 2^21 - 1) of Q* (`ctr_table_word`); the words that a passing
outer step stores for it, each in all seven lanes (`ctr_memory`): Y12, -Y1 -
w12, C2.b1, -C2.c1, w5, w5 + delta, the word v of Lemma A (c) for y, and beta*;
and the counter batch of 9.2 (`ctr_batch`) with its two end tests: the part
"loop" compares the advanced table position with the word `end of list`, which
holds CTR_WORDS, and the part "entry count" compares the advanced number of
stage-2 entries with the word `stage-2 budget`, which holds STAGE_2_BUDGET =
floor(CTR_PASS_BUDGET * CTR_WORDS / 32) = 12,940,509,260,824,455,073,275, called
E. 9.2 and 9.3 describe them as the program and its self-test hold them.

**9.2 Seven trials in one word.** The counter batch runs on the machine of 6.5,
with the same packed words of seven 36-bit lanes, the same masked rotation, the
same charge of one unit for every operation, load and store, and the same
convention for registers. For table word j and lane i, with c1 the member of
that lane, it computes in every lane:

- Stage A. *Cube word to Y14*: E1.a1 = RT[j] XOR Y12; Y6 = E1.a1 + (-Y1 - w12);
  Y14 = (ROL(Y6, 7) XOR C2.b1) + (-C2.c1). *z*: z = ROL(Y14, 8). *Rule A*: the
  word y and the test of Lemma A (c) and (d), with the word v of the outer
  step's y in place of the list word V[j]. *Loop*: the next table position, its
  comparison with `end of list` and the branch.
- Stage 2. *Entry count*: the next count of stage-2 entries, its comparison
  with `stage-2 budget` and the branch. *E1, A and B*: E1.a1 and Y6 again from
  RT[j]; d1 = DT[j]; c1 = d1 + Y11 and c1' = d1 + Y11'; then b1 = ROR(c1 XOR
  Y6, 12), a2 = w5 + E1.a1 + b1 and c2 = c1 + ROR(a2 XOR d1, 8) for A, and the
  same with c1' and w5 + delta for B. *E1 test*: eps = c2 XOR c2', beta* XOR
  eps, the word n = (ROL(beta* XOR eps, 1) XOR eps XOR eta) AND M of Lemma N,
  and the flags and the branch of the E1 test of 6.5.

Seven words stay in registers for all words of an outer step: Y12, -Y1 - w12,
C2.b1, -C2.c1 and the masks A25, B25 and A24 of the rotations by 25 and by 24
(the program's `CTR_RESIDENT`); their loads belong to the passing outer step.
The batch uses 16 registers, the two that hold the table position and the entry
count included.

| Part | What is computed | Operations | Loads |
| --- | --- | ---: | ---: |
| loop | next table position, end test, branch | 3 | 1 |
| cube word to Y14 | E1.a1 (1), Y6 (1), Y14 (7) | 9 | 1 |
| z | rotation by 8 | 5 | 1 |
| rule A | word y (8), u and sum (3), flags and branch (3) | 14 | 7 |
|  | stage A, every word | 31 | 10 |
| entry count | next count, budget test, branch | 3 | 1 |
| E1, A and B | E1.a1, Y6 (2), A: c1 b1 a2 c2 (16), B: (16) | 34 | 14 |
| E1 test | eps, beta* XOR eps (2), n (7), flags and branch (4) | 13 | 7 |
|  | stage 2, only after a pass of stage A | 50 | 22 |

So stage A is 31 + 10 = 41 units per word of seven trials and stage 2 is 50 +
22 = 72 units per word that enters it; no part stores anything. These counts
are the program's table `CTR_TABLE`. The loads of stage A are the end of the
table, RT[j], the mask B24, the two masks of Lemma A (c), the word v, ALL,
2^32 - ALL and twice the word with every bit of the lanes except bit 32. The
loads of stage 2 are the budget; RT[j], DT[j], Y11, Y11', w5 and w5 + delta;
the masks of the rotations by 12 and by 8, twice each; beta*, the mask of the
rotation by one bit, eta and M; and M and the mask of bit 32 for the flags and
the mask of bit 32 for the branch.

**Lemma CB (the counter batch).** Fix an outer step, and let the memory hold
the words that `ctr_memory` stores for it and the run-wide table (9.1). For
every table word j and every lane i, with c1 the member of Q* of that lane and
the trial given by the outer step and c1:

(a) the lanes of Y6 and Y14 hold, modulo 2^32, the values Y6 and Y14 of step
CT, and z = ROL(Y14, 8) = C2.d1 XOR Y2;

(b) the flag of stage A says whether the trial satisfies rule A;

(c) the reduced word of stage 2 is the word n of Lemma N for the trial, and n =
D3 XOR ROL(D6, 8), where D3 and D6 are the XOR differences between A and B of
words 3 and 6 of the two last-chunk chaining values; in particular R = 0
implies n = 0;

(d) no sum leaves its lane.

Proof. (a) RT[j] holds ROL(E1.d1, 16) for E1.d1 = c1 - Y11, so E1.a1, Y6 and
Y14 are the lines for E1.a1, Y6, Y10 and Y14 of step CT, with the stored -Y1 -
w12 and -C2.c1. C2's sixth assignment is Y14 = ROR(C2.d1 XOR Y2, 8). (b) The
proof of Lemma A uses only the sixth assignment of C2, the first two
assignments of E3 with w15 = 0, the value Y3 of Fact P and the membership of Y4
in the sub-class; all of them hold for the trial by Lemma CT and Theorem C. So
Lemma A (a) to (d) hold for the trial, with the word v of y, and the operations
of the part "rule A" are those of 6.5. (c) The lines are those of 6.2 for E1 on
A and on B, with c1 = d1 + Y11, c1' = d1 + Y11' and w5 + delta; beta* is the
XOR difference of E1's first-half b values by Theorem C (iv). The proof of
Lemma N uses only E1, the second and sixth assignments of E3 and the difference
eta of E3's first-half d values, which holds for the trial by Theorem C (iii);
and words 3 and 6 of the chaining value are o[3] and o[6]. (d) With B = 2^32:
table words, stored words, constants and outputs of a masked rotation are below
B; Y6 and Y14 are below 2B; in stage 2, c1 and c1' are below 2B, the two a2 and
the two c2 below 3B, and eps and beta* XOR eps below 4B, so that the shift of
the latter by one bit stays inside the 36-bit lane and the rotation by one bit
is formed as in 6.5; the sum of the rule test is at most B (Lemma A (d)) and
the sum of the flags below 2B. So every sum is below 3B < 2^36. QED.

**9.3 The counter part of the self-test.** The command `python3
experiments/halfsearch.py --selftest N [seed]` of 6.5 also runs N cases of the
counter batch (the program's `ctr_selftest`). A case is one outer step, one
table word and the counted batch on a new machine. Its eight words, its table
position and a starting count of stage-2 entries come from SHAKE-256 of the
text "halfsearch counter selftest", the seed and the case number; every fourth
case is the last table word, in every fourth case the count of entries starts
one below E, and in every fifth case each outer word is 0, ffffffff or as
drawn. Each lane is checked against its trial (the program's `ctr_lane`): the
program builds the two last-chunk blocks by steps CO, CT and CS and compresses
each in full with counter t and flags 3 by the compression `compress2` of 6.5.
It requires the round-1 words of the trial and its values of E1 and E3, the
block words and the zero bytes, t < 2^32, words 0, 2, 5 and 7 of the two
chaining values equal, e1 in the sub-class, c1 in Q*, the difference beta* and
the difference eta. A lane is right when all of these hold, its stage-A flag
says whether the h1 of the compression satisfies rule A, its stage-2 word
equals the n of the compression, and its stage-2 flag says whether that n is
nonzero. The end tests of a case are right when both branches agree with the
lanes, the loop test ends exactly at the last table word and the entry test
fires exactly when the count reaches E. The exit status is 0 only if every lane
and every end test is right, the counts equal the table of 9.2 in every case,
the registers are at most 16 and no lane exceeds 36 bits.

With N = 2,000 and seed 1 the counter part reports 14,000 of 14,000 lanes
right, 55 lanes that satisfy rule A, 2,000 of 2,000 cases with right end tests,
the counts of the table of 9.2 in every case, 41 and 72 units, 6.1786 units per
trial at the share 1/32, 16 registers and a largest lane of 34 bits; the part
for the root instance of the same run is the one reported in 6.5. These are the
program's own checks. The program's compression with counter t and flags 3 was
compared with the organizer's `_compress` on 2,000 trials (Section 7); the
organizer does not run the self-test.

*The filter part of the self-test.* The same command also runs the filter part
(the program's `ctr_filter_selftest`, with the same seed), and the exit status
is 0 only if it is right as well. (a) Brute force: in 64 cases, the automata
built for words of 10 bits, with the real targets truncated to 10 bits in the
even cases and with random targets, for (2) with a random word in place of
DY3, of which three have a planted solution in the odd cases, run on a word
drawn from SHAKE-256 of the text "halfsearch
filter", the seed and the case number; each of the 128 masks is compared with
the mask that all 1,024 witnesses give. (b) The count of passing pairs from the
program's own tables of 32 bits, compared with CTR_SHARE. (c) 2^16 real outer
steps, their eight words from SHAKE-256 of the text "halfsearch filter steps",
the seed and the step number, walked by `ctr_run` with a stand-in that records
each cube enumeration: the share that passes, the enumerations and the skipped
outer steps; a second walk of the same outer steps with pass budget 2 must halt
at the third passing outer step after exactly two enumerations, and the counted
pass test must stop the run when the advanced count is CTR_PASS_BUDGET + 1. (d)
The counted
outer step and filter (`ctr_count`) against the plain ones on the first four
outer steps and on the first four passing ones, with the same counts on all
eight. With seed 1 it reports 128 of 128 masks right, the count of passing
pairs equal to CTR_SHARE (2^-9.8132), 74 of the 65,536 real outer steps passing
(2^-9.791, standard error 0.000131 on the share 0.001129, z = +0.14 against
pi), 74 enumerations and 65,462 skipped outer steps, the halt right, 8 of 8
counted outer steps right, and the counts of the counted walk: 467 units for the
outer step (348 operations, 119 loads), 41 for the filter (24 operations, 17
loads) and 4 for the pass count (3 operations, 1 load).

**9.4 The exact equation (GPT Sol, answer AK).** Fix a frame O = (C0.d1, D2.b1,
S11, S4, X9, w6, y), and write g for the outer word D2.a1. The 77 lines of step
CO fall into three groups. The 35 *frame lines*, in this order:

    X8 = ROL(X7,7) XOR D2.b1;   C0.c1 = X8 + C0.d1
    K3.a1 = IV[3] + IV[7] + w6;   K3.d1 = ROR(K3.a1 XOR 3,16)
    K3.c1 = IV[3] + K3.d1;   S15 = S11 - K3.c1
    S3 = ROL(S15,8) XOR K3.d1;   K3.b1 = ROR(IV[7] XOR K3.c1,12)
    D3.a1 = S3 + S4;   S7 = ROR(K3.b1 XOR S11,7)
    D3.b1 = X3 - D3.a1;   D2.c1 = ROL(D2.b1,12) XOR S7
    D3.c1 = ROL(D3.b1,12) XOR S4;   X4 = ROR(D3.b1 XOR X9,7)
    X13 = X8 - D2.c1;   X14 = X9 - D3.c1
    C0.b1 = ROR(X4 XOR C0.c1,12);   D3.d1 = ROL(X14,8) XOR X3
    Y8 = ROL(Y4,7) XOR C0.b1;   S9 = D3.c1 - D3.d1
    Y12 = Y8 - C0.c1;   Y0 = ROL(Y12,8) XOR C0.d1
    C0.a1 = Y0 - C0.b1 - w6;   S14 = ROL(D3.d1,16) XOR D3.a1
    S10 = K2.c1 + S14;   X12 = ROL(C0.d1,16) XOR C0.a1
    D1.c1 = X11 - X12;   D1.d1 = D1.c1 - S11
    S2 = ROL(S14,8) XOR K2.d1;   S6 = ROR(K2.b1 XOR S10,7)
    X1 = ROL(X12,8) XOR D1.d1;   D1.b1 = ROR(S6 XOR D1.c1,12)
    w7 = S3 - K3.a1 - K3.b1;   X6 = ROR(D1.b1 XOR X11,7)
    w5 = S2 - K2.a1 - K2.b1

the 29 *g-lines*, in this order:

    X2 = D2.a1 + D2.b1 + W13;   D2.d1 = ROL(X13,8) XOR X2
    S13 = ROL(D2.d1,16) XOR D2.a1;   K1.c1 = S9 - S13
    K1.d1 = K1.c1 - IV[1];   K1.a1 = ROL(K1.d1,16)
    w2 = K1.a1 - IV[1] - IV[5];   X0 = C0.a1 - X4 - w2
    K1.b1 = ROR(IV[5] XOR K1.c1,12);   D0.d1 = ROL(X15,8) XOR X0
    S5 = ROR(K1.b1 XOR S9,7);   S8 = D2.c1 - D2.d1
    K0.b1 = ROL(S4,7) XOR S8;   K0.c1 = ROL(K0.b1,12) XOR IV[4]
    S12 = S8 - K0.c1;   D0.c1 = S10 + D0.d1
    D0.b1 = ROR(S5 XOR D0.c1,12);   X10 = D0.c1 + X15
    X5 = ROR(D0.b1 XOR X10,7);   S1 = ROL(S13,8) XOR K1.d1
    w3 = S1 - K1.a1 - K1.b1;   C1.a1 = X1 + X5 + w3
    C1.d1 = ROR(X13 XOR C1.a1,16);   D1.a1 = ROL(D1.d1,16) XOR S12
    C1.c1 = X9 + C1.d1;   w10 = D1.a1 - S1 - S6
    C1.b1 = ROR(X5 XOR C1.c1,12);   w12 = D2.a1 - S2 - S7
    Y1 = C1.a1 + C1.b1 + w10

and the other 13 lines, for C2.a1, C2.d1, C2.c1, Y13, C2.b1, K0.d1, Y9, S0,
D0.a1, w8, w9, w11 and Y5. Put K_O(g) = Y1 + w12 for the names of these lines,
and for words d and a

    u = ROL(d,16) XOR Y12,
    H_O(d, a) = u - (ROL(a - u - w5, 12) XOR (d + Y11)),

with Y12 and w5 of the frame lines and Y11 of Fact P.

**Lemma AK (the exact equation; GPT Sol, answer AK).** (a) Each frame line reads
only constants, the six outer words of O, y and names of earlier frame lines;
each g-line reads only constants, the words of O, g and names of frame lines and
of earlier g-lines. They are 64 different lines of step CO. So the names of the
frame lines, Y12 and w5 among them, are functions of O alone, and K_O(g) is a
function of O and g. (b) For every frame O, every word g and every word c1, let
d = c1 - Y11 and a be the values of E1.d1 and E1.a2 that steps CO and CT give
for the outer step of O with D2.a1 = g and for c1. Then K_O(g) = H_O(d, a). (c)
Conversely, for every frame O, every word g and all words d and a with K_O(g) =
H_O(d, a), steps CO and CT, run for the outer step of O with D2.a1 = g and for
c1 = d + Y11, give E1.d1 = d, E1.a1 = u, E1.b1 = a - u - w5 and E1.a2 = a.

Proof. (a) is read off the two displays and step CO: each displayed line is a
line of step CO, the 64 are different, and each reads the names stated, in the
printed order; by Lemma CT (a) no other line assigns them. (b) Step CT gives
E1.d1 = c1 - Y11 = d and E1.a1 = ROL(d,16) XOR Y12 = u, then Y6 = E1.a1 - Y1 -
w12, E1.b1 = ROR(Y6 XOR c1, 12) and E1.a2 = E1.a1 + E1.b1 + w5 = a. So E1.b1 =
a - u - w5, Y6 = ROL(a - u - w5, 12) XOR c1 and Y1 + w12 = u - Y6 = H_O(d, a),
with c1 = d + Y11; by (a) the names Y1 and w12 of step CO are those of the
g-lines, so Y1 + w12 = K_O(g). (c) Step CT with c1 = d + Y11 gives E1.d1 = d
and E1.a1 = u; then Y6 = u - (Y1 + w12) = u - H_O(d, a) = ROL(a - u - w5, 12)
XOR c1, so E1.b1 = ROR(Y6 XOR c1, 12) = a - u - w5 and E1.a2 = u + (a - u -
w5) + w5 = a. QED.

The equation K_O(g) = H_O(d, a) is one equality of 32-bit words: its left side
runs 29 lines on g, its right side three word formulas on d and a. It uses no
law of the words and no further condition: v[13] = 0, the flags 3 and the
constants are those of Section 8, and every implication in the proof can be
reversed. Every outer step and c1 give their unique O, g, d and a and satisfy
it, by (b). A pair (d, a) can have no root g, one or many; nothing below assumes
how many, and step 4 of 9.1 treats every root. Once g is known the rest of the
trial is triangular: the other 13 lines of step CO and step CT.

*The condition it removes.* The earlier searches on this construction formed
every trial of an outer step and tested it. Under M a trial with c1 in Q* is
E1-listed with probability 53 * 2^-38 = 2^-32.27 (9.6); in a participant census
of the conditions, this is a condition on s = E1.b1 AND beta* of probability
2^-5.19 and, given s, a condition on E1.a2 of probability 2^-26.0. With Y4 and
E1.d1 prescribed, no order of the assignments, with or without the word v[13],
has E1.a2 or E1.b1 among its free words: they are tied to the outer words by one
cyclic 32-bit equation (a peeling result of the participant's helper agents; the
census and peeling programs are not in the package). Lemma AK writes that
equation out, with v[13] = 0. The table of 9.5 solves it for all right sides of
one frame at once, and the search then forms only E1-listed trials.

**9.5 The table of a frame (GPT Sol, answer AK).** Fix a frame and run its 35
frame lines. The table has 2^32 *heads*, indexed by the 32-bit words, and 2^32
*records*, indexed by g, one 256-bit word each. First every head is set to the
null value. Then for g = 0, 1, .., 2^32 - 1 in turn: compute K_O(g) by the 29
g-lines and one addition, write into record g the word g and the value of the
head at index K_O(g), and set that head to g. A link, a record index or the null
value, takes 33 bits and fits one word with the 32 bits of g. There is no
sorting and no hash function. A *query* for a word H reads the head at index H
and follows the links from record to record until the null value, returning the
g of every record on the way.

**Lemma KT (the table; GPT Sol, answer AK).** For every frame and every word H,
the query for H returns every word g with K_O(g) = H, each exactly once, and
nothing else; it returns no word when there is none.

Proof. Each g is written once, into record g, and becomes the head of the list
at index K_O(g), with a link to the earlier head of that list. So a link points
to a record written earlier or is null, every list ends, and after the last g
the list at index H holds exactly the records g with K_O(g) = H, each once. QED.

*Charge (GPT Sol, answer AK).* Every intermediate word is stored after use and
its operands are loaded again, so that no more than 16 registers are relied on.
Each of the 29 g-lines and the addition of K_O(g) is then at most 12 machine
units, its operand loads, its 32-bit normalisation and its store included, and
at most 128 more per g cover the record and its link, the head, setting the head
to null, the loop and the addresses: at most 512 per g, 2^41 per frame. At 12
for each of the 35 frame lines, 420, the allowance of 4,096 per frame leaves
more than 3,600 for the random word of step 1, the member y and the loop over
frames. A record of step 3, with its query, is at most 64 machine units, and the
work of each root in step 4, with its count, at most 8,192 (Section 11). These
are upper allowances given in words, not counts of an implementation. For Q
queries in one frame that return M roots in all, the table and the queries cost
at most 4,096 + 512 * 2^32 + 64 Q + 8,192 M machine units: a long list is not
free, its members are paid in the term of M.
In the search of 9.1 a record of step 3 compares H with K* in place of a query,
within the same 64; keeping K* is within the 128 of its g; and a frame has at
most 2^21 roots (Lemma TG1), so M <= 2^21.

*Limits (GPT Sol, answer AK).* The table is built once per frame, not once per
run: a frame has 192 free bits besides y, and no small table is known that
serves all frames. No way is known to solve the equation for a single right side
without the table; splitting g into halves does not give a meet in the middle,
since both halves feed rotations and carries of both branches.

**9.6 The E1 record table and the targets (GPT Sol, answer AK).** *The local
equations.* For a trial with c1 in Q* write c = c1, d = c - Y11, b = E1.b1 and
a = E1.a2 on message A, Bc = ROL(beta*, 12) = 0e09818b, and put

    s = b AND beta*,   Delta(s) = beta* - 2 s - 8,   z = ROR(d XOR a, 8),
    tau = a XOR (a + Delta(s)),   rho = ROR(tau, 8),
    epsilon = (c + z) XOR ((c + DY11) + (z XOR rho)).

E1's first-half b difference is beta* (Theorem C (iv)), and tau and epsilon are
the XOR differences between A and B of its a output and its c output. Indeed E1
has the same first two values on A and B, third values c and c + DY11, fourth
values b and b XOR beta*, and message word w5 + fffffff8 on B (step CS); so its
a output on B is a + (b XOR beta*) - b - 8 = a + Delta(s), since (b XOR beta*) -
b = beta* - 2 (b AND beta*); its d output is ROR(d XOR a, 8) = z on A and z XOR
rho on B; and its c output is c + z on A and (c + DY11) + (z XOR rho) on B. So
the E1 outcome of the trial is (tau, epsilon), and it is outcome j of 10.1
exactly when tau = tau_j and epsilon = eps = 6e21be55.

*Records.* For an outcome j and a word s with s AND beta* = s, s is *compatible*
with j when tau_j - Delta(s) is even modulo 2^32 and its half p_j(s) has no bit
outside tau_j. A word x has x XOR (x + D) = tau exactly when D = tau - 2 (x AND
tau); since every tau_j has bit 31 zero, x XOR (x + Delta(s)) = tau_j holds
exactly when s is compatible with j and x AND tau_j = p_j(s). A *record* is a
quadruple (c, z, s, j) with c in Q*, j an outcome of 10.1, s compatible with j,
and, for d = c - Y11, a = d XOR ROL(z, 8) and rho = ROR(tau_j, 8): a AND tau_j =
p_j(s) and (c + z) XOR ((c + DY11) + (z XOR rho)) = eps. The E1 record table
holds every record once, one 256-bit word each (32 bits of c, 32 of z, 11 of s
and 3 of j). By the two paragraphs above, a trial with c1 in Q* and E1 values d,
b, a is E1-listed with outcome j exactly when (c1, ROR(d XOR a, 8), b AND beta*,
j) is a record.

*Its size (GPT Sol).* For each outcome j, the number of s compatible with j and
the number D_j(s) of pairs (c, z) that make a record with s, the same for every
compatible s:

| tau_j | compatible s | D_j(s), each | 2^21 times the sum over s | L_j of 10.1 |
| --- | ---: | ---: | ---: | ---: |
| 175020a0 | 16 | 2^24 | 2^49 | 562,949,953,421,312 |
| 185020a0 | 32 | 2^25 | 2^51 | 2,251,799,813,685,248 |
| 275020a0 | 8 | 2^25 | 2^49 | 562,949,953,421,312 |
| 285020a0 | 16 | 2^26 | 2^51 | 2,251,799,813,685,248 |
| 385020a0 | 32 | 2^24 | 2^50 | 1,125,899,906,842,624 |
| 675020a0 | 8 | 2^23 | 2^47 | 140,737,488,355,328 |
| 685020a0 | 16 | 2^24 | 2^49 | 562,949,953,421,312 |

So the table has RECORDS = 53 * 2^26 = 3,556,769,792 records, and the 128
compatible pairs (s, j) use 56 values of s. A record fixes the 11 bits of b
under beta* and leaves the other 21 free, so 2^21 times the records of an
outcome is its number L_j of triples (E1.c1, E1.b1, E1.a2): the fourth column
equals L_j of 10.1 in all seven rows, a check of GPT Sol's counts against the
participant's count records. Under M, with c1 uniform in Q* and E1.b1 and E1.a2
uniform, a trial is therefore E1-listed with probability 53 * 2^47 / 2^85 = 53 *
2^-38.

*Construction (GPT Sol).* A recurrence over the bits of c and z from bit 0
upwards keeps the borrow of c - Y11, the carry of c + z (for c in Q*, c + DY11 =
c XOR Bc, and epsilon = eps holds exactly when at every bit the carries into
that bit of c + z and of (c XOR Bc) + (z XOR rho) differ by the bit of Bc XOR
rho XOR eps), the bits of z that a later bit of the condition on tau_j still has
to read, and a guess of bits 29 and 31 of z, which ROL(z, 8) moves to bits 5 and
7, where tau_j reads them. It has at most 2^16 transitions for one pair (s, j),
counts D_j(s) at 128 machine units per transition, below 2^31 for the 128 pairs,
and, run backwards, lists every record once with no rejection and no duplicate,
at most 2^13 machine units per record. So the E1 record table is built in at
most 2^46 machine units, once, before the frames; it depends on the constants
alone. The participant has not implemented the recurrence; the counts D_j(s) are
GPT Sol's, and the participant compared only their sums with L_j.

*Targets.* In step 3 of 9.1 a frame scans every record. For a record (c, z, s,
j) it forms d = c - Y11, a = d XOR ROL(z, 8), u = ROL(d,16) XOR Y12 and b = a -
u - w5, keeps the record exactly when b AND beta* = s, and queries the table for
H = u - (ROL(b, 12) XOR c) = H_O(d, a). The test does not assume that
prescribing a controls the b pattern or epsilon: the b of the trial that a root
gives is a - u - w5 (Lemma AK (c)), and the record is kept only when that b has
the record's pattern.

**Lemma TG (the targets; GPT Sol, answer AK).** Fix a frame O. (a) Every root of
the frame, a kept record (c, z, s, j) with a word g that its query returns,
gives the trial of the outer step of O with D2.a1 = g and c1 = c, and that trial
is E1-listed with outcome j. Different roots give different trials. (b) Every
E1-listed trial of the frame is given by exactly one root of the frame. (c) Run
over all roots of the frame, step 4 certifies exactly the roots that give the
listed good trials of the frame, and each listed good trial of the frame by one
root.

Proof. (a) The record was kept, so b = a - u - w5 has b AND beta* = s, and g was
returned for H = H_O(d, a), so K_O(g) = H_O(d, a) (Lemma KT). By Lemma AK (c)
the trial with D2.a1 = g and c1 = c has E1.d1 = d, E1.b1 = b and E1.a2 = a, so
ROR(d XOR a, 8) = z and b AND beta* = s; c is in Q*, and (c, z, s, j) is a
record, so the trial is E1-listed with outcome j (9.6). A trial determines its
root: g and c are its own, z and s are functions of its E1 values, and j is its
outcome. (b) Let the trial have D2.a1 = g, c1 = c in Q*, E1 values d, b and a
and outcome j, and put s = b AND beta* and z = ROR(d XOR a, 8). Then (c, z, s,
j) is a record (9.6). Step 3 forms from it the same d and a, u = E1.a1 by step
CT, and b' = a - u - w5 = E1.b1 = b by E1's fifth assignment, so it keeps the
record; by Lemma AK (b) H_O(d, a) = K_O(g), so the query returns g (Lemma KT).
By (a) no other root gives the trial. (c) By (a) every root gives an E1-listed
trial, and step 4 certifies it exactly when c is in Q*, t is not zero, rule A
holds and the two last-chunk chaining values agree in all eight words, that is,
with Theorem C (ii), when R = 0: exactly when the trial is a listed good trial.
With (b), each listed good trial of the frame is given by one root. QED.

**Lemma TG1 (one outer step).** Fix a frame O and its word g*, and put K* =
K_O(g*). (a) A record kept in step 3 of 9.1 with H = K* gives the trial of the
outer step (O, g*) with c1 = c, and that trial is E1-listed with outcome j;
different such records give different trials, so a frame has at most 2^21 roots.
(b) Every E1-listed trial of the outer step (O, g*) is given by exactly one
record kept with H = K*. (c) Run over these roots, step 4 of 9.1 certifies
exactly the listed good trials of the outer step (O, g*), each once.

Proof. A kept record and the word g* form a root of the frame in the sense of
Lemma TG exactly when the query for H returns g*, that is (Lemma KT) exactly
when K_O(g*) = H, that is H = K*. So the roots of step 3 of 9.1 are the roots of
the frame in the sense of Lemma TG whose word is g*. By Lemma TG (a) each gives
the trial with D2.a1 = g* and c1 = c, E1-listed with outcome j, and different
roots give different trials; a trial of the outer step is fixed by its c1, one
of the 2^21 words of Q*. By Lemma TG (b) every E1-listed trial with D2.a1 = g*
is given by exactly one root of the frame, and its word is g*. (c) follows from
Lemma TG (c) restricted to these roots. QED.

So in every frame that it processes in full, the search of 9.1 certifies exactly
the listed good valid trials of the frame's one outer step over all of Q*: the
trials that an enumeration of all of Q* in that outer step would find. Lemmas
AK, KT, TG and TG1 use no law of the words. The number of roots of a frame, the
number of E1-listed trials of its outer step, is at most 2^21 whatever the
words, so no root cap and no premise on its mean is needed.

**9.7 A check of the equation.** A participant computation, which is not part of
the package, checked Lemma AK and the local equations of 9.6 against the
program's own steps CO and CT (`ctr_outer`, `ctr_trial`) on 200,000 outer steps
drawn from a seeded generator, every fifth with each outer word 0, ffffffff or
as drawn. In every one, the 35 frame lines, computed from the frame alone, equal
the program's names, and they are unchanged for a second, random D2.a1 with the
same frame; the 29 g-lines equal the program's names and K_O(g) = Y1 + w12. For
c1 drawn from Q* in half of the outer steps and a uniform word in the other
half, K_O(g) = H_O(d, a) held on all 200,000 trials. For a second c1 in Q*, the
word a solved from K_O(g) = H_O(d, a) was the E1.a2 of that trial in all
200,000. On the 100,059 trials with c1 in Q*, E1 run on A and on B gave the
differences beta*, tau and epsilon of 9.6 and the d output z, with a = d XOR
ROL(z, 8), and the keep test of step 3 held. There were no mismatches. The check
covers the algebra and its transcription only: no table of a frame or E1 record
table has been built, no part of the search has been run at any word size, and
none of its operations has been counted by a program.

## 10. The rate of a counter trial and the success probability

**10.1 The model rate.** The seven-word model M of Section 13 treats the
residual of a trial as a function of seven words, E1.d1, E1.b1 and E1.a2 of
message A and Y4, Y9, w8 and E3.h1, with Y4 uniform in the sub-class and the
other six independent uniform words. Under M the rate of the sub-class is r =
185,377,197.55 (Section 13): a trial has R = 0 with probability r * 2^-128. The
part of a value beta of E1's first-half b difference in r is written r(beta);
the part of beta* is 67,698,688. A trial of Section 8 has c1 in Q* and so the
difference beta* (Theorem C (iv)); under M the event that c1 = Y11 + E1.d1 lies
in Q* has probability 2^-11 and is the event that the difference is beta*
(Lemma S1). The rate of a trial that M conditions on c1 in Q* is therefore

    p = 2^11 * 67,698,688 * 2^-128 = 138,646,913,024 * 2^-128 = 1033 * 2^-101,

about 2^-90.987. It is (138,646,913,024 * 2^20) / 194,382,080,300,609 =
747.92 = 2^9.547 times r * 2^-128, the model rate of a trial of entry 64c075ac.

*The seven outcomes of beta*.* In the count of Section 13 an outcome of beta is
a pair (tau, eps) of the differences of E1's a and c outputs. For an outcome j
of beta*, L_j is the number of triples (E1.c1, E1.b1, E1.a2) of words for which
E1 on A and on B (6.2) gives the differences beta*, tau_j and eps_j, so that
L_j = 2^(96 - k) P1 with P1 and k of step 4 of the count; and N3_j is the
number N3 of step 3 of the count for that outcome: the number of quadruples
(Y4, E3.h1, Y9, w8), Y4 in the sub-class, for which E3 on A and on B gives the
differences eta and tau_j XOR ROR(tau_j, 1) of its first-half d and b values
and tau_j and eps_j of its c and a outputs. Every input of the 2^209 of the
model falls into one outcome, so r(beta*) = sum over j of L_j N3_j / 2^81.
Beta* has seven outcomes, all with eps = 6e21be55:

| tau | L_j | N3_j | L_j * N3_j / 2^81 |
| --- | ---: | ---: | ---: |
| 175020a0 | 562,949,953,421,312 | 27,021,597,764,222,976 | 6,291,456 |
| 185020a0 | 2,251,799,813,685,248 | 18,014,398,509,481,984 | 16,777,216 |
| 275020a0 | 562,949,953,421,312 | 4,503,599,627,370,496 | 1,048,576 |
| 285020a0 | 2,251,799,813,685,248 | 27,021,597,764,222,976 | 25,165,824 |
| 385020a0 | 1,125,899,906,842,624 | 36,028,797,018,963,968 | 16,777,216 |
| 675020a0 | 140,737,488,355,328 | 1,125,899,906,842,624 | 65,536 |
| 685020a0 | 562,949,953,421,312 | 6,755,399,441,055,744 | 1,572,864 |
| sum | | | 67,698,688 |

In each of the seven outcomes every solution satisfies rule A: the number of
quadruples whose E3.h1 also satisfies rule A equals N3_j. So the part of beta*
in r, in r_A and in the figure "kept for H1" of Section 13 is the same,
67,698,688, and rule A loses nothing of it. The seven terms are 2^16 times 96,
256, 16, 384, 256, 1 and 24, which sum to 1033: p = 1033 * 2^-101 exactly. The
integers L_j and N3_j are those of the participant's count (Section 13), the
records from which the table of Section 13 is summed; GPT Sol 6.1 reconciled
the seven rows and their sum with those records and with the totals r, r_A and
the kept figure, by integer arithmetic on the records and without a new
enumeration. The counting program and its output are in Section 17.

*Why beta*.* For a value beta of the difference, let k be the number of bits of
ROL(beta, 12) AND 7fffffff, so that the words c1 that give beta form a cube
with k fixed bits; the conditional rate of a trial with c1 uniform in that cube
is phi(beta) * 2^-128 with phi(beta) = 2^k r(beta), and phi_A(beta) and
phi_H(beta) are formed the same way from the parts with rule A and kept for H1.
GPT Sol 6.1 formed the three for all 53 values of beta that have a part in the
sub-class, from the same records, on which every other value has none, and
beta* is first for all three:

| beta | k | mask and value of c1 | phi = phi_A = phi_H |
| --- | ---: | --- | ---: |
| 18b0e098 | 11 | 0e09818b, 02008000 | 138,646,913,024 |
| 18b1a098 | 11 | 1a09818b, 08008000 | 105,235,087,360 |
| 18d0e098 | 11 | 0e09818d, 02008001 | 104,018,739,200 |
| 18d1a098 | 11 | 1a09818d, 08008001 | 27,128,758,272 |
| 18b3e098 | 13 | 3e09818b, 1a008000 | 12,079,595,520 |
| 18d3e098 | 13 | 3e09818d, 1a008001 | 6,190,792,704 |

The other 47 have phi below 2^27. A uniform draw from the union of the cubes of
several values of beta has the average of their rates weighted by the sizes of
the cubes, so no union does better than beta* alone. The program stores beta*
(`CTR_BETA`) and the mask and value of its cube.

**10.2 Lemmas on the counter sampler (GPT Sol 6.1).** The following lemmas were
proved by GPT Sol 6.1 for this construction, Lemma S9 by GPT Sol in its answer
AC, and are given with their hypotheses; each is exact mathematics under the
hypotheses stated. The
participant compared Lemmas S1 to S4 and Lemma IP with the construction line by
line; the carry Lemmas S5 to S7 were not re-derived by the participant. They do
not prove the rate of H1' or the success probability; 10.3 states what remains
a premise.

**Lemma S1 (conditioning the model).** *Hypotheses:* under M the six words
E1.d1, E1.b1, E1.a2, Y9, w8 and E3.h1 are independent uniform words,
independent of Y4, which is uniform in the sub-class; c1 = Y11 + E1.d1.
*Statement:* c1 lies in Q* with probability 2^-11, and that is the event that
E1's first-half b difference is beta*. Conditional on it, E1.d1 is uniform on
Q* - Y11, E1.b1 and E1.a2 keep their independent uniform laws, and (Y4, Y9, w8,
E3.h1) keeps its law and stays independent of (E1.d1, E1.b1, E1.a2). Hence
Pr_M(R = 0 and rule A | c1 in Q*) = 2^11 Pr_M(R = 0 and rule A and c1 in Q*) =
2^11 * 67,698,688 * 2^-128 = p, the last step by the count of 10.1.

*Proof.* Translation by Y11 makes c1 uniform and independent of every other
coordinate. By the identity of the proof of Theorem C (iv), c1 lies in Q*
exactly when the difference is beta*, and Q* fixes 11 bits of c1, so the
probability is 2^-11. The event depends on E1.d1 alone, so for every event G1
of the words of E1 and G3 of the words of E3, Pr_M(G1 and G3 | c1 in Q*) =
Pr_M(G1 | c1 in Q*) Pr_M(G3). No independence of the output differences inside
E1 or inside E3 is used. QED. The finite counts behind 67,698,688 are inherited
records and are not proved by this lemma.

**Lemma S2 (the outer chart).** *Hypotheses:* y and c1 are fixed; the seven
outer words are independent uniform words; the names obey the assignments of
step CO, with flags 3 and v[13] = 0. *Statement:* the seven outer words are in
bijection with the seven context words (C0.c1, C0.d1, D3.d1, S15, S9, w5, X2)
of Section 4. These are therefore independent uniform words, and their law does
not depend on c1 or y.

*Proof.* Given the context words, these assignments, which are lines of steps O
and M of Section 4 with flags 3 in place of 11, return the outer words: S2 =
K2.a1 + K2.b1 + w5; S14 = ROR(K2.d1 XOR S2, 8); D3.a1 = ROL(D3.d1,16) XOR S14;
D3.b1 = X3 - D3.a1; D3.c1 = S9 + D3.d1; S4 = ROL(D3.b1,12) XOR D3.c1; S3 =
D3.a1 - S4; X14 = ROR(D3.d1 XOR X3, 8); X9 = D3.c1 + X14; K3.d1 = ROL(S15,8)
XOR S3; w6 = (ROL(K3.d1,16) XOR 3) - IV[3] - IV[7]; S11 = IV[3] + K3.d1 + S15;
X8 = C0.c1 - C0.d1; D2.b1 = ROL(X7,7) XOR X8; D2.a1 = X2 - D2.b1 - W13.
Substituted into K2, D3, K3 and D2 they return w5, D3.d1, S9, S15, X2, C0.c1
and C0.d1, and the lines of step CO, run on the outer words they return, give
the context words back. Both maps are inverse bijections between two sets of
2^224 elements, and the uniform law is carried to the uniform law. QED.

**Lemma S3 (two independent offsets).** *Hypotheses:* those of Lemma S2.
*Statement:* (w5, D3.a1, Y12, S15, X2, X8, C0.d1) is another chart of the outer
words, so these seven are independent uniform words; in particular Y12 and w5,
which E1 reads, are independent uniform words.

*Proof.* The chart is reached by replacements of coordinates, each a bijection
with the other coordinates held fixed: (w6, S11) by (S3, S15), with inverse
K3.d1 = ROL(S15,8) XOR S3, w6 = (ROL(K3.d1,16) XOR 3) - IV[3] - IV[7], S11 =
IV[3] + K3.d1 + S15; (D2.a1, D2.b1) by (X2, X8), with D2.b1 = ROL(X7,7) XOR X8
and D2.a1 = X2 - D2.b1 - W13; (S3, S4, X9) by (D3.a1, S4, S14), with inverse
D3.b1 = X3 - D3.a1, D3.d1 = ROR(S14 XOR D3.a1, 16), X14 = ROR(D3.d1 XOR X3, 8),
D3.c1 = ROL(D3.b1,12) XOR S4, X9 = D3.c1 + X14, S3 = D3.a1 - S4; S14 by w5,
with S2 = K2.a1 + K2.b1 + w5 and S14 = ROR(K2.d1 XOR S2, 8); at fixed D3.a1 and
S14, S4 by X4, with inverse X9 = ROL(X4,7) XOR D3.b1, D3.c1 = X9 - X14, S4 =
ROL(D3.b1,12) XOR D3.c1; and last, with C0.c1 = X8 + C0.d1, X4 by Y12, with
C0.b1 = (Y12 + C0.c1) XOR ROL(y,7) and X4 = ROL(C0.b1,12) XOR C0.c1. The
composition proves the chart and the uniform law. It says nothing about the
independence of Y12 and w5 from functions that also depend on them, such as the
residual. QED.

**Lemma S4 (a marginal and the physical conditioning).** *Hypotheses:* those of
Lemmas S2 and S3, and c1 independent of the outer words. *Statement:* (a) At
each fixed c1 and y, E1.a1 and E1.a2 - E1.b1 are independent uniform words. (b)
For two members c1 and c1' of Q* in one outer step, put m4 = ROL((c1 - Y11) XOR
(c1' - Y11), 16); then the difference of their values of E1.a2 - E1.b1 is m4 -
2 (E1.a1 AND m4), E1.a1 being that of c1, and conditional only on the value of
E1.a2 - E1.b1 at c1 it is uniform on the values m4 - 2 s, s a submask of m4 AND
7fffffff, which are all different. (c) Let a baseline sampler draw t as a
uniform 32-bit word, t = 0 included as an algebraic trace, with flags 3, the
same constants and the same outer words, and solve c1 from it; then c1 is
uniform and independent of the outer words and y, and the sampler of Section 8,
c1 uniform in Q*, is exactly the baseline conditioned on c1 in Q*: for every
event of the trace, its probability under the sampler of Section 8 is 2^11
times the probability under the baseline that it happens and c1 lies in Q*.

*Proof.* (a) By Lemma S3, Y12 and w5 are independent uniform, so E1.a1 =
ROL(E1.d1,16) XOR Y12 and w5 are, and E1.a2 - E1.b1 = E1.a1 + w5 by E1's fifth
assignment; replacing (E1.a1, w5) by (E1.a1, E1.a1 + w5) is a bijection. (b)
The same outer words give c1' the first value E1.a1 XOR m4 and the same w5, and
(X XOR m4) - X = m4 - 2 (X AND m4) modulo 2^32. Conditional on the first value,
E1.a1 stays uniform, its bits under m4 AND 7fffffff give the uniform law
stated, and different submasks below 2^31 have different doubles. (c) By Lemma
IP, c1 -> t is a permutation for every outer step and y, so a uniform t makes
c1 uniform and independent of them; conditioning on c1 in Q*, an event of
probability 2^-11, leaves the outer words and y unchanged, and step CT run
forwards from c1 is the same trace. QED. Statement (c) is about the
construction's own sampler and does not identify it with M; it lets an event
include t != 0 but does not say how much of the rare success mass the rule t !=
0 removes.

**Lemma S5 (a carry prescription).** *Statement:* let x, s, s', a and d be
words of w bits with (x + s) XOR ((x XOR a) + s') = d. Every bit i < w - 1 at
which a and d differ is determined by the lower bits of x and by the constants;
so at most 2^(w - n1) words x solve the equation, n1 being the number of bits
of (a XOR d) AND (2^(w - 1) - 1).

*Proof.* Write u_i and u'_i for the carries into bit i of the two additions.
Equality at bit i gives a_i XOR d_i = s_i XOR s'_i XOR u_i XOR u'_i. If its
left side is 1, exactly one of the pairs (s_i, u_i) and (s'_i, u'_i) has
unequal bits; the carry out of that addition is its variable input bit, x_i or
x_i XOR a_i, and the carry out of the other addition is its fixed common bit.
Equality at bit i + 1 prescribes the XOR of the two carries out, which fixes
x_i. Counting the choices from the low bits to the high bits gives the bound;
bit w - 1 has no next bit, which is why it is left out. QED.

**Lemma S6 (an E3 prescription).** *Hypotheses:* an outer step and y are fixed,
so Y9 and w8 are fixed. The seven outcomes of 10.1 are all the outcomes of
beta* that have a solution: every complete success has eps = 6e21be55 and tau
among the seven. This is a premise on the finite enumeration, not a law of the
words. *Statement:* for each of the seven outcomes put sigma = tau XOR ROR(tau,
1), theta = ROL(sigma, 12), M1 = (sigma XOR eps) AND 7fffffff, M2 = ((eta XOR
theta) AND 00000fff) << 20 and M3 = e13000f0. At most 2^(32 - n1) values of
E3.h1 give a complete success that satisfies rule A with that outcome, n1 being
the number of bits of M1 OR M2 OR M3.

*Proof.* In this proof write e1 = Y3 + y, h = E3.h1, g = Y9 + h, f = ROR(y XOR
g, 12), e2 = e1 + f + w8 and j = ROR(h XOR e2, 8), the first-half d, c and b
values and the a and d outputs of E3 on A (6.2), and primes for B, with h' = h
XOR eta. At fixed Y9 and y the map h -> f is a permutation. A complete match
with the outcome gives f XOR f' = sigma, e2 XOR e2' = eps, g' = g XOR theta,
j' = j XOR ROR(eta XOR eps, 8) with ROR(eta XOR eps, 8) = 9aed22bd, and (g + j)
XOR (g' + j') = tau. By Lemma S5, M1 prescribes bits of f from lower bits of f.
Lemma S5 applied to h + Y9 and (h XOR eta) + Y9 prescribes bits i < 12 of h,
which correspond to bits i + 20 of f; their mask is M2. The conditions h[0] =
0, h[1] = 1, h[2] XOR h[10] = 1 and h[3] XOR h[11] = 1 of rule A likewise
prescribe bits 20, 21, 30 and 31 of f from earlier bits. For all seven rows
gamma = eta XOR theta has bits 16 to 20 equal to 0, 0, 1, 1, 0, while eta has
bits 16 to 19 equal to 1, 1, 0, 0. The carry recurrence with h[16] = h[17] = 0
gives bits 16 to 19 of g equal to 0, 1, 1, 0 and the carry into bit 20 of h +
Y9 equal to bit 19 of Y9; hence bits 4 to 7 of f are constants. For the last
addition g + j, its carry-XOR word theta XOR 9aed22bd XOR tau has bits 16 to 22
equal to 0, 1, 0, 0, 1, 1, 0, and the same recurrence gives, with k_i the carry
of the addition on A, j[16] = 0, k_17 = 0, k_18 = j[17], j[18] = 0, k_19 =
k_18, j[19] = 0, k_20 = 0, j[20] = 1 XOR g[20], k_21 = 0 and j[21] = 1. So
j[16] = h[24] XOR e2[24] = 0 and j[21] = h[29] XOR e2[29] = 1 prescribe bits 24
and 29 of f: the known carry into bit 20 makes h[24] depend only on bits 8 to
12 of f, and h[29] only on bits 8 to 17, and the addition e2 = e1 + f + w8 is
triangular. The common mask is M3 = e13000f0. All bits of M1 OR M2 OR M3 are
determined by lower bits of f, and an overlap counts once. QED.

**Lemma S7 (at most 3,072 complete successes in one outer step).**
*Hypotheses:* those of Lemmas S6 and IP. *Statement:* in one outer step at most
3,072 members of Q* give a complete success that satisfies rule A, the member
with t = 0 included. No law of the outer words is assumed.

*Proof.* Lemma S6 gives:

| tau | M1 | M2 | bits of M1 OR M2 OR M3 | values of E3.h1, at most |
| --- | --- | --- | ---: | ---: |
| 175020a0 | 72d98ea5 | 20000000 | 22 | 1,024 |
| 185020a0 | 7a598ea5 | 28800000 | 23 | 512 |
| 275020a0 | 5ad98ea5 | 08000000 | 23 | 512 |
| 285020a0 | 52598ea5 | 00800000 | 22 | 1,024 |
| 385020a0 | 4a598ea5 | 18800000 | 23 | 512 |
| 675020a0 | 3ad98ea5 | 68000000 | 23 | 512 |
| 685020a0 | 32598ea5 | 60800000 | 22 | 1,024 |

The low carry equations of h + Y9 with h[0] = 0 and h[1] = 1 give bits 0 and 1
of Y9 equal to 0, no carry into bit 2 and bit 2 of Y9 equal to bit 3 of gamma.
So one outer step admits only the rows 175020a0, 275020a0 and 675020a0 when bit
2 of Y9 is 0, with 2,048 values in all, or only 185020a0, 285020a0, 385020a0
and 685020a0 when it is 1, with 3,072. Since c1 -> E3.h1 is one to one (Lemma
IP), at most 3,072 members succeed. QED. For the number N_o of listed good
valid trials of an outer step (10.3) this gives E[N_o (N_o - 1)] <= 3,071
E[N_o]: a
bound on the worst case only, far from what 10.3 needs.

**Lemma S8 (success from a mean and a factorial moment).** *Statement:* let N_o
be a count with values in {0, 1, ..}, mu = E[N_o] > 0 and rho = E[N_o (N_o -
1)] / mu. Then Pr(N_o > 0) >= mu b(rho), where b(rho) = (2 r_o - rho) / (r_o
(r_o + 1)) and r_o = floor(rho) + 1; for 0 <= rho <= 1 this is 1 - rho / 2, and
b decreases with rho. If the outer steps of a run are independent and each has
mean at least mu and ratio at most rho, the probability that some outer step
has N_o > 0 is at least 1 - exp(-mu b(rho) times the number of outer steps).

*Proof.* For integers r_o >= 1 and z >= 0, the indicator of z > 0 is at least
(2 r_o z - z (z - 1)) / (r_o (r_o + 1)): with equality at z = 0, and for z >= 1
the inequality is (z - r_o)(z - r_o - 1) >= 0, which holds for integers. Taking
expectations gives the first statement. For independent outer steps, the
probability that none has N_o > 0 is the product of the values 1 - Pr(N_o > 0)
of the outer steps, at most exp(-mu b(rho) times their number). QED.

**Lemma S9 (the success mass lies on passing outer steps; GPT Sol, answer
AC).** (a) *No hypothesis.* In every outer step that does not pass the filter,
the count N_o of 10.3 is zero. Let pi_o be the probability that an outer step
passes the filter when its seven outer words are independent uniform words and
its member is uniform in the sub-class. If pi_o > 0, then E[N_o | the outer step
passes] = E[N_o] / pi_o.
(b) *Hypotheses:* those of Lemma S1. Under M, also conditional on c1 in Q*, Y9
and omega = Y3 + Y4 + w8 are independent uniform words, and the filter passes
with probability pi. Let S be the event that R = 0, rule A holds and the E1
outcome is one of the seven; given c1 in Q*, S has probability p under M
(Lemma S1 and the count of 10.1). S lies inside the event that the filter
passes. So Pr_M(S | c1 in Q* and the filter passes) = p / pi = 1033 /
(312,881,258,079 * 2^53), about 2^-81.174, and Pr_M(the filter passes | c1 in
Q*) times this conditional rate is p: conditioning on the pass loses no part of
p.

*Proof.* (a) A listed good trial has R = 0 with one of the seven outcomes, so
by Lemma F its outer step passes; N_o is a count that is zero off the event that
the outer step passes, and E[N_o] = pi_o E[N_o | the outer step passes]. (b)
Under M, Y9 and w8 are independent uniform words, independent of Y4; for fixed
Y4, w8 -> omega is a translation, so (Y9, omega) is uniform on all 2^64 pairs
and independent of Y4, and Lemma S1 leaves the law of (Y4, Y9, w8, E3.h1)
unchanged under c1 in Q*. The proof of Lemma F uses only the assignments of E3
and the conditions of R = 0, which hold for the model words, so it gives the
inclusion; by 10.1 all of p comes from the seven outcomes, and every one of
their solutions satisfies rule A. Dividing by the probability pi of the pass
gives the conditional rate. QED. Statement (a) uses the pass probability pi_o
of the sampler itself; that pi_o equals pi is not proved. Statement (b)
is about M and says nothing about the sampler.

Lemma S9 concerns the filter of Section 8, which the search of 9.1 does not use.
What the search finds is stated by Lemma TG (9.6): in every frame that it
processes in full, it certifies exactly the listed good valid trials of the
frame.

**10.3 Heuristics.** For a frame drawn by step 1 of 9.1, with its word g*, let
N_o be the number of listed good valid trials of its outer step (D2.a1 = g*)
over all of Q*. One heuristic is declared, in the form of the premise H1' of the
reviewed entries on this track (entry e7b17fd1 and its successors): a rate and a
bound on the dependence of the good trials of one outer step. GPT Sol's answer
AK declared two more premises for the frames of 2^32 outer steps of entry
9a9f3b7b, on the good trials and on the roots of a whole frame; the search of
9.1 needs neither, because each frame is one outer step and its roots are at
most 2^21 (Lemma TG1). H1' is not measured at its scale.

**Heuristic H1' (score-critical; the rate and the dependence).** For an outer
step whose seven outer words are independent uniform words and whose member is
uniform in the sub-class, (i) E[N_o] >= (2^21 - 1) q, with q = (5/7) p = 5 *
1033 / (7 * 2^101), about 2^-91.473; and (ii) E[N_o (N_o - 1)] <= 0.0065 E[N_o].

Step 1 of 9.1 draws the seven outer words of a frame and its member uniformly
and independently of the other frames, so the frames are independent outer steps
of this law, and FRAMES * E[N_o] >= 0.515: FRAMES is the least whole number for
which FRAMES * (2^21 - 1) q >= 0.515. In the terms of Lemmas S1 to S4 part (i)
is this: the construction's pushforward of the uniform outer words, with c1
running over all of Q*, onto the seven model words (E1.d1, E1.b1, E1.a2, Y4, Y9,
w8, E3.h1) carries at least 5/7 of the complete-success integral p of the
conditional law of Lemma S1, and that stays true after the member with t = 0 is
dropped (Lemma IP). It is a statement about a mean only; it asserts neither
independent trials nor independent uniform E1 or E3 words, and it follows
neither from the model nor from Lemmas S1 to S9. The search of 9.1 does not
change it: a frame is one outer step, drawn as the premise draws it. The factor
(5/7) * 138,646,913,024 = 99,033,509,302.86 times 2^-128 per valid trial is a
margin of 1.40 on the count, chosen by the participant for this search; entry
e7b17fd1 and the earlier entries on this track assumed half of the count, a
margin of 2.00. This part is stronger than theirs and is not implied by it; 10.4
gives the price at half the count.

Part (ii) is the bound 0.0065 on the dependence of the good trials of one outer
step of 2^21 trials that the entries on this track declare with the rate; Lemma
S8 turns it into the factor 1 - 0.0065 / 2 of 10.4. It is not proved: Lemma S7
gives only E[N_o (N_o - 1)] <= 3,071 E[N_o], and single outer steps of the
counter arrangement differ strongly in partial events (Section 13). It concerns
one outer step, the group of the reviewed entries (judged plausible_not_refuted), and no group of several outer
steps: here a frame is one outer step.

*What is proved and what is not.* Proved (Lemmas S2 to S4): the outer words of a
step are uniform in the chart of the seven context words of Section 4; Y12 and
w5 are independent uniform words; E1.a1 and E1.a2 - E1.b1 are independent
uniform words at every fixed c1; and the sampler of Section 8 is exactly the
uniform-counter sampler conditioned on c1 in Q*. Proved as well (Lemmas AK, KT,
TG and TG1): in every frame that it processes in full, the search of 9.1
certifies exactly the listed good valid trials of the frame's outer step, so N_o
is the same count for it as for an enumeration of all of Q* in that outer step,
and a frame has at most 2^21 roots. Not proved: that E1.b1, E1.a2, E3.h1, Y9 and
w8 have the model's joint law with the rest (H1' (i)); how much of the success
mass the member with t = 0 carries (Lemma IP bounds the number of dropped
trials, one in 2^21, not their mass); and the dependence of the good trials of
one outer step (H1' (ii)).

**10.4 Success probability.** The probability space is the FRAMES independent
uniform 256-bit words of step 1 of 9.1, for the fixed target. The algorithm is
otherwise deterministic. Under H1' it outputs a collision with probability at
least

    1 - exp(-0.515 * (1 - 0.0065 / 2)) = 1 - exp(-0.51332625)
      = 0.4014985013... >= 0.40.

The frames are independent and identically distributed (step 1 of 9.1), and each
is one outer step with E[N_o] >= 0.515 / FRAMES (H1' (i)) and E[N_o (N_o - 1)] /
E[N_o] <= 0.0065 (H1' (ii)); Lemma S8 bounds the probability that no frame has
N_o > 0 by exp(-0.515 * 0.99675) < 0.598502. The run has no cap but FRAMES: it
processes the frames in turn until step 4 certifies a root, which it does at the
latest in the first frame with N_o > 0 (Lemma TG1); then it outputs a pair. When
the algorithm outputs a pair, the pair is a genuine collision: its trial is
certified, so its two last-chunk chaining values agree in all eight words, step
4 checks both complete digests, and the messages have different lengths.

*Sensitivity to the rate.* If the valid trials are listed good trials at f *
2^-128 each on average, with H1' (ii) unchanged, the same bound needs FRAMES(f)
= ceil(0.515 * 2^128 / ((2^21 - 1) f)) frames, and by the charge of Section 11
the time is log2(O(f) / 430 + 2^38), with O(f) = S + 2^46 + FRAMES(f) *
2,443,836,395,520 and S the cap of SEL. At the assumed f = (5/7) *
138,646,913,024 this is 101.91954, claimed as 101.9196. At half the count, f =
69,323,456,512, the assumption of entry e7b17fd1, it is 102.43411 with
1,205,415,477,209,996,173,140 frames, about 2^70.030, and the package would
submit 102.4342. At the uniform rate, f = 1, it is 138.44674, with
83,563,567,413,258,896,800,296,174,585,121 frames, about 2^106.043. These
figures are the participant's arithmetic with the formula of Section 11.

H1' is not proved. Section 13 lists the evidence.

## 11. Charged time

One 2-round target compression costs one unit, and every other primitive word
operation, every load and every store included, costs 1/430 of a unit. The rows
below are in operations, loads and stores of the machine of 6.5, called machine
units here, with scalar values, one 32-bit value or one record to a word of 256
bits; 430 of them make one unit of time. Every load is one machine unit wherever
its word lies, the loads from the two tables of the search included, as the cost
model counts them; memory is reported in Section 12.

**The cost, with every term.** Every row is machine units times an upper bound
on how often a run executes it. The rows of a frame run at most FRAMES times,
because the algorithm halts with failure after FRAMES frames (9.1), and the row
of step 4 at most 2^21 times in a frame, because the roots of a frame give
different trials of its one outer step (Lemma TG1): at most FRAMES * 2^21 times
in a run. The allowances are GPT Sol's (answer AK) and are stated in words in
9.5 and 9.6: they are upper bounds on operations, loads and stores, not counts
of an implementation. Exponents of counts are rounded up.

| Row | How often over a run, at most | Machine units each | Machine units |
| --- | --- | ---: | ---: |
| the selection procedure SEL of Section 12 | once | | 498,959,033,940,035,296,819,072 |
| the E1 record table (9.6) | once | 2^46 | 70,368,744,177,664 |
| a frame: the random word, the 35 frame lines, the word K* and the loop over frames (9.5) | FRAMES = 843,790,834,046,997,321,198 | 4,096 | 3,456,167,256,256,501,027,627,008 |
| the table of a frame: one value of D2.a1 (9.5) | FRAMES * 2^32 = 2^101.516 | 512 | 1,855,515,666,890,965,412,631,048,980,791,296 |
| a record in step 3: d, a, u, b, the keep test and the comparison with K* (9.6) | FRAMES * RECORDS = 2^101.244 | 64 | 192,074,863,955,510,091,541,885,929,652,224 |
| a root in step 4: steps CO and CT, the tests of Q*, t and rule A, two last-chunk compressions and the comparison | FRAMES * 2^21 = 2^90.516 | 8,192 | 14,496,216,147,585,667,286,180,070,162,432 |
| **total, O_tot** | | | **2,062,086,750,949,187,461,726,020,049,229,696** |

In a formula, O_tot = S + 2^46 + FRAMES * (4,096 + 512 * 2^32 + 64 * RECORDS +
8,192 * 2^21), with S the cap of SEL and FRAMES * 2,443,836,395,520 =
2,062,086,750,450,228,427,715,616,008,232,960 for the frames (the allowances of
GPT Sol, answer AK; recomputed by the participant in integers).

*The allowance of a root.* GPT Sol bounds the reconstruction and the checks of a
root by 8,192 machine units. At the same 12 machine units for an assignment as
in 9.5, the 77 lines of step CO and the 16 of step CT are at most 1,116, and the
two compressions of the last chunks, 16 calls of eight assignments each, at most
3,072; the test of Q*, the test of t, rule A (Lemma A), the two blocks of step
CS and the comparison of eight words take the rest. This breakdown is the
participant's, given to show that the allowance covers a full test; it is not a
count.

*The final step*, once: steps CT and CS for the trial found, writing the two
messages, shorter than 2^42 bytes each, and two complete evaluations of blake3;
each message has at most 2^32 chunks of 16 compressions each and fewer than 2^32
parent compressions, below 2^37.1 compressions for both, and writing them is
below 2^38 machine units: below 2^38 units of time in all. This holds because t
< 2^32 and v[13] = 0 (Theorem C).

Total:

    T <= O_tot / 430 + 2^38
      =  2,062,086,750,949,187,461,726,020,049,229,696 / 430 + 2^38
      =  4,795,550,583,602,761,538,897,721,044,720.22... + 274,877,906,944,

so log2 T <= 101.9195393091... The submitted bound is time_log2 = 101.9196, the
total rounded up at the fourth decimal; in integers, (O_tot + 430 * 2^38)^10000
<= 430^10000 * 2^1019196, and the same with 2^1019195 fails. The search part,
every row but SEL, is 2,062,086,750,450,228,427,785,984,752,410,624 machine
units, below 2^101.91954 units of time; SEL, charged in full, is below 2^69.976
units, below 2^-31.94 times the search part. It is a worst-case bound for the
algorithm as stated, which halts after at most FRAMES frames on every run and
whose work in one frame, its roots included, is bounded whatever its words; H1'
enters only the success probability of 10.4.

*Where the time goes.* Of O_tot, the tables of the frames are 89.98 per cent,
the scans of the E1 record table 9.31 and the roots 0.70; SEL is below 3 parts
in 10^10 and the frame lines below 2 parts in 10^9. Per trial covered, FRAMES *
2^21 = 2^90.516 of them, the search part is 1,165,312.002 machine units, about
2^20.152. Building the table again for every outer step is the price of removing
the premise on whole frames: in entry 9a9f3b7b one table served the 2^32 outer
steps of a frame.

*Memory access.* There is no sorting and no hash function. A frame writes its
table in the order of D2.a1 and reads from it only K*, kept while the table is
written; each kept record is compared with K* in a register. These loads and
stores are inside the allowances of the rows above.

## 12. Memory, preprocessing and advice

The program of the search is the lines of steps CO, CT and CS, the 35 frame
lines and the 29 g-lines of 9.4, the table and the queries of 9.5, the
recurrence and the scan of 9.6, the test of rule A and a compression routine
for step 4 and the final check. Bound the code by 4096 instruction templates of
at most four 256-bit words each: 2^14 words, which is 2^19 bytes. Data, one
word of 256 bits each: the E1 record table (RECORDS = 3,556,769,792 words); the
table of the frame in hand (2^32 heads and 2^32 records, 8,589,934,592 words),
which the next frame overwrites; and fewer than 1,024 words for the frame
lines, the names of the trial in step 4, the constants and masks, the count of
frames, the temporaries and the cells of step 4: fewer than 12,146,705,408
words, that is 388,694,573,056 bytes. The recurrence of 9.6, which runs before
the frames, keeps one weight for each of its states of one pair (s, j), fewer
than 2^14 words. The memory of the search is therefore below 2^19 + 2^19 +
388,694,573,056 < 2^39 bytes; GPT Sol (answer AK) gives 32 * (RECORDS + 2 *
2^32) = 388,694,540,288 bytes for the two tables. It does not grow with the
number of frames or of trials.
The two messages of a found pair have 1024 t + 55 and 1024 t + 63 bytes with
t < 2^32, each shorter than 2^42 bytes; the output, the two messages with their
digests, takes less than 2^43 bytes; with the code, less than 2^43 + 2^19.

**The selection procedure SEL.** The values that the program stores (listed
under advice below) were selected by searches and counts. This section writes
that selection as a procedure, SEL. Its cost is charged as preprocessing, and
it has an upper bound by construction: every search of SEL runs over a range
stated here, and every run of a program in SEL halts as soon as it has executed
a stated number of primitive word operations, its cap, or holds 2^34 bytes. A
run that halts so returns nothing, and SEL goes on. Operations are counted as
in Section 11, 430 to the unit. SEL runs two programs of the participant that
are not in the package: the solver kissat, on instances made by a generator of
the participant, and the counter of Section 13, which computes in integer
arithmetic the part of one beta in the rate of a given set of members of the
class, with or without a given rule on h1. A run of the counter whose part
would be 2^192 or more counts as one that reaches its cap, so every part that
SEL uses is below 2^192 and every mass, rate, mean, value of xi, sum and
product that steps 4 to 6 form from parts is below 2^255 in absolute value and
fits in one word of 256 bits, as their operation counts assume.

*Step 1, the pinned call (solver runs).* For each of the 116 runs of the
participant's solver log for this search (51 runs for the lengths 55 and 63,
the other 65 for nine other variants of the instance; bounds 97 to 118; logged
seeds), build the instance of the run and run kissat on it with the logged
seed, the two together with a cap of 2^56 operations. For the lengths 55 and
63 the instance is that of entry c66f230d (its Section 10): the call C3 for
both messages with equal b and d outputs, the two words w4 related as the
length cancellation prescribes for the XOR 8 of the lengths, the top byte of
word 13 zero, E1 and E3 for both messages, a zero residual, and a bound on the
number of bit positions, bit 31 excepted, at which a difference is active in
six additions of E1 and E3. A run that finds a model returns six constants X3,
X7, X11, X15, W4, W13 and the values of a solution, among them its Y4 and its
beta. Cost: at most 116 * 2^56 < 2^62.86 operations.

*Step 2, the constants and the class (a count for each model).* For each model
of step 1, compute Y3 and Y3' by C3 from its constants, its class
eta = ROR((Y3 + Y4) XOR (Y3' + Y4), 16) from the Y4 of its solution, and with
the counter the part of the beta of its solution in the rate of that class,
with a cap of 2^52. Output the six constants and the eta of the model with the
largest part. Cost: at most 116 * (2^52 + 2^10) < 2^58.86 operations.

*Step 3, the betas.* With DY11 = Y11' - Y11 for the output of step 2, mark for
every word c1 from 0 to 2^32 - 1 the word ROR(c1 XOR (c1 + DY11), 12) in a
table of 2^32 bits, then list the marked words. These are all the words that
occur as beta (Section 13, step 1 of the count): 133,742 for the constants of
3.2. If there are more than 133,742, SEL halts with failure. Cost: below 2^36
operations.

*Step 3a, the betas with a part in the class.* For each beta of step 3,
compute with the counter its part in the rate of the class, with a cap of
2^52. Keep the betas whose run finished with a part that is not zero, in
increasing order; if more than 64 are kept, SEL halts with failure. Steps 4, 5
and 6 run over the kept betas only. A beta whose part in the class is zero has
a zero part in the rate of every set of members of the class, with or without
a rule on h1: by steps 3 to 5 of the count of Section 13 its part is a
positive multiple of a sum of products P1 * N3 that are not negative, so a
zero part makes every product zero; for such a set N3 counts some of the same
quadruples and P1 is unchanged, so its products are zero as well. So if every
run of this step finishes, steps 4 to 6 record over the kept betas the same
rates, masses and parts as over all betas of step 3, and otherwise lower
bounds, as before. By the records of Section 13, 60 betas have a part in the
class. Cost: 133,742 * (2^52 + 2^6) < 2^69.03 operations.

*Step 4, the sub-class.* For each of the 524,288 members y of the class and
each beta kept in step 3a, compute with the counter the part of the beta in the
rate of the one-member set {y}, with a cap of 2^52; the rate of a member is the
sum of its parts. A part whose run reaches its cap is recorded as unfinished.
Parts are not negative, so a recorded rate is a lower bound, and it is exact
when none of its parts is unfinished. Then, for every sub-cube of the class,
that is for each of the 3^19 ways to fix each of the 19 free bits of e1 to 0,
to fix it to 1 or to leave it free, form the mean of the rates of its members,
in one pass that keeps no list of the means. The sub-class of 6.1 is one of
these sub-cubes: bits 21 and 26 of e1 fixed to 0, the other 17 free. Cost:
524,288 * 64 * (2^52 + 2^6) < 2^77.01 operations for the counts, and 2^38
additions of at most 32 operations each, with the comparisons of the pass,
below 2^43.02 for the means. This step follows winglock, who chose the
sub-class S8 of the entries 2125212 and 2bb5d604 from the exact rate of every
one of the 524,288 members of the same class (the best of 8,992,320 candidate
sub-classes, by the text of those entries).

*Step 5, rule A.* Let W be the sixteen bits 0 to 3, 6 to 13, 16, 17, 24 and 25
of h1. For each of the 2^16 patterns of W and each beta kept in step 3a,
compute with the counter the part of the beta in the mass of the solutions with
Y4 in the sub-class whose h1 agrees with the pattern on W (a rule of sixteen
one-bit conditions), with a cap of 2^52, recording unfinished parts as in step
4; the mass of a pattern is the sum of its parts. A rule of eight independent
affine conditions on the bits of W is a set of patterns, an affine subspace of
codimension 8, and its exact mass is the sum of the masses of its 2^8 patterns.
Generate every such subspace once, as the patterns alpha, vectors of sixteen
bits, with J alpha = chi for a reduced row echelon matrix J over GF(2) with
eight rows, sixteen columns and rank 8 and a right side chi of eight bits:
there are [16 choose 8]_2 = 63,379,954,960,524,853,651 < 2^65.79 matrices J,
where [16 choose 8]_2 is the number of subspaces of dimension 8 of a space of
dimension 16 over GF(2), and 2^8 * [16 choose 8]_2 < 2^73.79 rules. The masses
of all rules come from one transform. Let zeta(alpha) be the mass of the
pattern alpha, and xi(kappa) the sum over the patterns alpha of
(-1)^(kappa.alpha) zeta(alpha) for each of the 2^16 vectors kappa of sixteen
bits, computed by the fast Walsh-Hadamard transform, where kappa.alpha is the
parity of the bitwise AND of kappa and alpha. For each J and each of the 2^8
vectors nu of eight bits, let kappa_nu be the sum over GF(2) of the rows of J
that the bits of nu select; then compute, for every chi, the sum over nu of
(-1)^(nu.chi) xi(kappa_nu), by the transform of size 2^8. This sum is 2^8
times the mass of the rule J alpha = chi: since nu.(J alpha) = kappa_nu.alpha,
xi(kappa_nu) is the sum over chi of (-1)^(nu.chi) times the mass of
J alpha = chi, and the transform of size 2^8 applied twice multiplies by 2^8.
So every rule gets the sum of the masses of its 2^8 patterns, as before. For
the masses, zeta and xi, each load, addition, subtraction or comparison counts
as at most 16 operations.

The transform of size 2^8 is computed in two halves of four stages, and the
first half is shared by all matrices J with the same first four rows. The first
four rows of J form a reduced row echelon matrix P of rank 4, its prefix, and
the last four rows R of J are zero in the four pivot columns of P, because J is
reduced. There are [16 choose 4]_2 = 914,807,651,274,739 < 2^49.71 prefixes;
every J has exactly one, so taking for each prefix the matrices J that have it
takes every J once. For a prefix P let I be its four pivot columns, Z_P the
set of vectors of sixteen bits that are zero in I, P(a) the sum over GF(2) of
the rows of P that the bits of a vector a of four bits select, and R(b) the
same for R. P is the identity on I, so every vector of sixteen bits is
P(a) XOR q for exactly one a and one q in Z_P, and every R(b) is in Z_P. For q
in Z_P and each of the 16 vectors t of four bits let

    xi_P(q, t) = sum over a of (-1)^(a.t) xi(P(a) XOR q),

2^16 values, kept at the index q OR e(t), where e(t) puts the four bits of t
into the columns I; the index takes every value of sixteen bits once. Write
nu = (a, b) and chi = (t, c), with a and t for the rows of P and b and c for
the rows of R; then kappa_nu = P(a) XOR R(b) and (-1)^(nu.chi) =
(-1)^(a.t) (-1)^(b.c), and exchanging the sums over a and b gives

    sum over nu of (-1)^(nu.chi) xi(kappa_nu)
      = sum over b of (-1)^(b.c) xi_P(R(b), t).

So the 2^8 sums of J are 16 transforms of size 16, one for each t, of the
values xi_P(R(b), t) over the 16 vectors b: the same sums as before, once
for every rule J alpha = chi. A mass is a sum of at most 64 parts below 2^192,
and every value of xi, of xi_P and of a stage of these transforms is a sum
of at most 2^24 masses with signs, so it is below 2^222 in absolute value. It
is held in one word of 256 bits, a negative value in two's complement, in which
addition and subtraction modulo 2^256 give the exact result; the sums over nu
are 2^8 times masses, not negative, and are compared as unsigned words.

SEL takes the prefixes one at a time and keeps the table of one. Each addition
or subtraction of two words is one operation, as the machine of 6.5 counts it
and as the cost model lists addition and subtraction modulo 2^256, and every
load, store, address computation, comparison and branch is charged besides.
Per prefix P at most 2^22 operations: gathering the 2^16 values
xi(P(a) XOR q) into a table at the index q OR e(a), with the updates of the
index, the masks, the addresses, the loads and the stores, at most 16 per
value, 2^20; the four stages of the transform over the bits in I, each of 2^15
butterflies of two loads, an addition, a subtraction and two stores, at most 16
per butterfly with its addresses and loop, 2^21; and 2^20 for enumerating P,
its small index tables, the counters of the Gray code below and the set-up of
each choice of the pivot columns of R, four columns after the last pivot of P
in which P is zero, at most 12 * 11 * 10 * 9 / 24 = 495 choices. For each
choice the matrices J of the prefix are taken in the order of a Gray code over
the free entries of R, at most 32, one entry changing at each step. Per matrix
J at most 5120 operations:

    the step of the Gray code, the packed rows of R, set-up           256
    16 transforms of size 16, one for each t, each with
      16 inputs: a row of R by two shifts, the XOR into the
        index R(b), the OR with e(t), the address and the load,
        6 each                                                         96
      8 stores and 8 loads of the first half, with addresses           32
      32 butterflies, an addition and a subtraction each               64
      16 outputs: the right side (a load and an OR), the
        comparison, the branch and two copies, 6 each                  96
      control, and the store and load of the recorded right side      11
    the comparison and record of J after its 2^8 sums                  32
    other addresses and control of J                                   32

    256 + 16 * (96 + 32 + 64 + 96 + 11) + 32 + 32 = 5104 < 5120.

This uses at most the 16 registers of 6.5. The four rows of R are packed in
one register, from which a row is taken by two shifts by fixed distances. A
transform of size 16 is two of size 8 and eight more butterflies: the eight
results of the first are stored in eight scratch words and loaded one at a
time for the last eight butterflies. A transform of size 8 needs nine data
registers, the sum of a butterfly going into the free one and the difference
into a register of an operand. While inputs are read, at most eight data
registers are held with the index R(b), the table base, e(t), t, the recorded
value, the scratch base, the input address and the packed rows, 16 in all, and
the recorded right side is stored; a last butterfly needs at most ten data
registers with the table base, t, the recorded value and right side, the
scratch base and the address. The 16 values of t and the order of the 16
inputs are written out in the code, so the transforms of one J keep no loop
counter. Cost: 65,536 * 64 * (2^52 + 2^6) < 2^74.01 operations for the counts;
16 * (2^16 * 64 + 16 * 2^16 + 2^16) < 2^27 for zeta and xi;
[16 choose 4]_2 * 2^22 < 2^71.71 for the prefixes; and
[16 choose 8]_2 * 5120 < 2^78.11 for all rules. Rule A reads only bits of W
(6.3), so it is
one of these rules.

*Step 6, the difference beta*.* For each beta kept in step 3a, compute with the
counter its part in the rate of the sub-class of step 4 with the rule of step
5, with a cap of 2^52, recording unfinished parts as in step 4. By the identity
of the proof of Theorem C (iv), the words c1 that give beta are those whose
bits under the mask ROL(beta, 12) AND 7fffffff equal (ROL(beta, 12) - DY11) /
2, with DY11 of step 3: a cube with k fixed bits, k the number of bits of the
mask. Output the beta with the largest product of 2^k and its part, the mask
and value of its cube, and the outcomes (tau, eps) of that beta whose product
in its part is not zero, which its count lists (step 2 of the count of Section
13); for beta* these are the seven of 10.1, which the outer filter uses. Cost:
64 * (2^52 + 2^6) < 2^58.01 operations.
The ranking runs over every kept beta, and a beta that step 3a drops after a
finished run has a zero part here (step 3a), so it is exhaustive when every run
of step 3a finishes; by the records of Section 13, 53 of the kept betas have a
part in the sub-class.

**The bound.** Steps 1 to 6, with step 3a, cost fewer than

    2^62.86 + 2^58.86 + 2^36 + 2^69.03 + 2^77.01 + 2^43.02 + 2^74.01 + 2^27
      + 2^71.71 + 2^78.11 + 2^58.01 < 2^78.74 operations,

which is below 2^(78.74 - 8.748) < 2^70 units. In whole numbers, with 2^36 for
step 3, 2^44 for the means of step 4 and 2^27 for zeta and xi, the costs of
steps 1 to 6 sum to at most 498,959,033,940,035,296,819,072 operations, less
than 430 * 2^70 = 507,654,396,908,486,860,472,320. The E1 record table of 9.6,
built once before the search from the constants alone, adds at most 2^46
operations, 498,959,034,010,404,040,996,736 in all, still less than 430 * 2^70.
preprocessing_log2 = 70 is this bound for both, and both are included in T
(Section 11); the tables of the frames are built in the search and charged
there. It bounds SEL
as
defined, whatever the two programs do inside and whatever they return, because
every run halts at its cap and every loop has the range stated. It replaces
both figures that entry c66f230d gave: the bound 2^63 for recomputing W4 and
W13 at the four given inputs, which SEL does not need because step 1 returns
all six constants, and the estimate below 2^60 operations, which is not used.

*What rests on records.* The bound rests on no record. That SEL returns the six
constants of 3.2 and eta = 830303cf does: on the participant's solver log, by
which the run for the lengths 55 and 63 with bound 104 and seed 506 found these
constants after 4,770 seconds, with a solution of class 830303cf and beta
18b0e098; on the record of entry c66f230d (its Section 10) that for these
constants the part of the solver's beta in the class was the largest of the
sets of the log, 71,698,432 where the largest of the others was 13,107,200; on
the solver and the counter being deterministic for given inputs; and on the
participant's observation that the solver and the counting programs stayed
below 16 GB of memory. Every run of the log stopped within 9,000 seconds on one
processor core, and no processor core executes 2^40 primitive operations in a
second, so every run used fewer than 2^53.14 operations, below its cap of 2^56.
That step 6 returns beta* = 18b0e098 and its seven outcomes rests on the count
records of Section 13 and on GPT Sol 6.1's ranking of the 53 values of beta
with a part in the sub-class (10.1). That step 3a keeps beta* and at most 64
betas rests on the records of Section 13 (60 betas with a part in the class)
and on its runs for these betas finishing within the cap; for beta*, the beta
of the solver's solution, it is the same run as the one of step 2 whose part,
71,698,432, the record above gives. The generator of the instances, the solver
log and the counter are not in the package. If a record were wrong, SEL could
return other constants or none; its cost would stay within the bound.

The stored sub-class, rule A and beta* are members of the ranges of steps 4, 5
and 6, as their definitions in 6.1, 6.3 and Section 8 show, beta* once step 3a
keeps it (above); the stored bytes listed under advice name them. SEL computes
the same figure for every member of each range, and choosing one member by
those figures reads them once, inside the bound of its step. SEL does not show
that the stored sub-class and rule are the best of their ranges by any one
criterion. They were proposed by GPT Sol 6.1 from searches of its own, which
the participant has not repeated; by that model's statements, which the
participant has not checked (Section 13), the sub-class is the only best of
the sub-cubes with 15 fixed bits of e1 and the rule a best set of eight affine
conditions on h1. Steps 3a, 4, 5 and 6 have not been run as written; the bound
does not need them to have been.

*Memory of SEL.* Every program run of SEL halts when it holds 2^34 bytes, and
SEL runs one at a time. Its own data stay below 2^31 bytes: the table of step 3
(2^29 bytes), and the parts of steps 3a and 6, the rates of step 4, and the
masses, the 2^16 values of xi and of xi_P of one prefix, and the small
tables and scratch words of step 5
(32
bytes a beta, a member, a pattern or a value). SEL therefore holds fewer than
2^34 + 2^31 bytes at any time; the search, which runs after it, fewer than 2^39
bytes; the output fewer than 2^43 bytes; the code 2^19 bytes. Held at once,
these total below 2^43 + 2^39 + 2^35 + 2^19 < 2^44: memory_log2_bytes = 44 bounds all. The measurements of Section 13 on real and on scaled-down messages are
not part of SEL; they test the heuristics and select nothing, and neither their
work nor their memory is in these figures. The cost model does not score
memory.

nonuniform_advice_log2_bytes = 7 covers the 28 bytes of the six constants and
eta, the 8 bytes that name the two bits of the sub-class and their values, the
12 bytes of the two masks and the word ALL of Lemma A, the 12 bytes of beta* and
of the mask and value of its cube, and the 32 bytes of the seven values of tau
and of eps of the outcomes of beta*, which the E1 record table of 9.6 and the
outer filter use (the program's `CTR_TAUS` and `CTR_EPS`), 92 bytes in all.
These bytes are also the names by which the stored sub-class, rule, beta* and
its outcomes are chosen among the candidates of steps 4, 5 and 6. The E1 record
table, the run-wide table, the tables of the filter's automata and the lists U
and V are not advice: they are computed from these constants, and so are the
tables of the frames, from the random words of the search as well. CTR_SHARE is
the count of passing pairs of Section 8, which the program's tables give, and
the program's pass budget is computed from it (9.1); FRAMES of 9.1 is computed
from the count of 10.1. The flags 3 and
the counter rule are part of the algorithm. There is no other stored data and no
stored collision.

## 13. Evidence, scope and field meanings

Throughout this text costs and bounds are rounded up, and margins, rooms and the
whole numbers of the count that the claim uses are rounded down. Counts printed
with decimals are rounded to the nearest.

**What is exact.** Sections 2 to 5, 7 and 8; Lemmas L, H, Q, Q2, T, T2, T4, N,
A, TR, CT, IP, F and CB and Theorem C; Lemmas AK, KT and TG of the search and
the local E1 equations of 9.6; the count of passing pairs of Section 8;
and Lemmas S1 to S9 under their stated hypotheses. Lemma A says what stage A
tests, not that a collision passes it. The declared experiment `half-collision`
runs one trial of the root instance
(6.1) per organizer seed, with the seven words of a context and a member number
taken from the seed, and the organizer recomputes both digests; Lemma T
predicts that every trial agrees on the 128 masked digest bits. The counter
instance has no organizer-run check (6.4).

*What is new in the exact part and who has checked it.* Sections 1 to 6 are
those of entry 64c075ac without its clusters; Lemmas L, H, Q, T and N and Fact
P go back to entry c66f230d. New in entry e7b17fd1 were Lemma TR, the counter
order with Lemma CT and Theorem C, and the counter batch with Lemma CB, written
by helper agents of the participant, instances of the same AI model as the
author of this text; and Lemmas IP and S1 to S8, proved by GPT Sol 6.1. New in
this package are the outer filter, proposed by a helper agent of the
participant; Lemma F and Lemma S9, proved by GPT Sol in its answer AC, the
proof of Lemma F written out in Section 8 by a helper agent of the participant
from the assignments of E3; and the count of passing pairs with its
certificate, derived by GPT Sol in the same answer. New in the search of this
package are Lemmas AK, KT and TG, the table of a frame and the E1 record table
with its counts, from GPT Sol's answer AK. The participant's checks of
the new exact part are computations, not proofs: the counter construction
against the organizer's own functions on 2,000 trials, with 204,000 internal
words compared with a separately written forward computation, and complete
messages hashed by the organizer's code (Section 7); every lane of the counter
batch against the program's own compression of the real last chunks (9.3); all
2^21 members of Q*, each giving the difference beta*; the rule t != 0 (Section
8); the program's automata against brute force at 10 bits (9.3); and the two
pattern histograms of the program's own tables against the certificate, equal
in all 36 nonzero masks and both zero counts, with the same count of passing
pairs and the same seven per-outcome counts (Section 8). For the search of
Section 9 the participant checked Lemma AK and the local E1 equations of 9.6
against the program's steps CO and CT on 200,000 real counter trials (9.7),
recomputed the figures of 9.1 and Section 11 in integers, and compared the
counts of the E1 record table with the L_j of 10.1; it did not re-derive the
recurrence that builds that table. For Sections 1 to 6,
three independent reruns, by a checking agent, a
reviewing agent and a participant tool that reads the printed text, found no
wrong value in the displays, Table C and Lemmas Q, Q2, L, A, T2 and T4, and
Lemma A was checked by complete enumeration in three ways: the submitted
program on all 2^16 patterns of the 13 bits of z and the 3 bits of e1 that the
rule reads (65,536 packed words); a second statement of rule and test typed by
hand on 4,194,304 inputs; and seven wrong plans of the test, all of which the
program refuses. These are checks, not proofs, and no person has read any part
of this text.

**The seven-word model.** By 6.2 the residual of a trial, of the root instance
or of the counter instance, is a function of the constants and of seven 32-bit
words: for E1 its first-half values d1 and b1 and its a output a2 on message A,
and for E3 the words Y4, Y9, w8 and its first-half value h1 on A. The model M
says that over the trials the six words other than Y4 behave like independent
uniform words, independent of Y4, which is uniform in the sub-class. Under M a
trial has R = 0 with probability r * 2^-128, where r * 2^81 is the number of
solutions of R = 0 among the 2^209 values of the seven words with Y4 in the
sub-class. Call r the *rate of the sub-class*. Rule A is a condition on h1, so
under M the trials with R = 0 that satisfy rule A have a rate of the same kind,
r_A, counting only the solutions that satisfy rule A; r_A is at most r. The
counter search prescribes c1 = Y11 + d1 in Q*, and under M that is a
conditioning on d1 (Lemma S1); its rate p is formed from the part of beta* in r
(10.1). On the outer steps that pass the filter of Section 8 the rate under M is
p / pi, and no part of p lies on the others (Lemma S9). M and the count give the
rate of a single trial. They do not give the
probability that a run has a good trial, which also depends on how the good
trials of a run cluster; a model of the single trial says nothing about that.

Given M, the rates are properties of the constants, the sub-class and beta*
alone and can be counted without sampling; the count says nothing about whether
M holds. The six words are not free in a trial. In the counter search Y4, Y9
and w8 are fixed for the 2^21 trials of an outer step, and so are Y12 and w5,
which E1 reads; the trials of an outer step differ in d1 and in what follows
from it (Lemma CT (c)), and E1.b1, E1.a2 and E3.h1 move with d1; in the search
of 9.1 a frame is one outer step, and these words are fixed for its 2^21 trials.
M is a statement about averages over the outer steps of a run. Lemmas S2 to S4
show which parts of it hold exactly for the construction, and H1' declares the
rest.
The measurements below show where M fails inside one context and inside one
outer step.

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

"With rule A" is the part of the beta in r_A. "Kept for H1", the figure that
entry 64c075ac used, adds only the outcomes in which every solution satisfies
rule A. The heaviest beta carries 36.5% of the count and the four heaviest
98.8%. The count rests on few paths.

*Rule A in the count.* Of the 317 outcomes, 99 have only solutions that satisfy
rule A, 76 have none that does, and 142 have both. The exact rate with rule A is

    r_A = 6219586146887739/33554432 = 185,358,111.47,

so the rule loses 19,086.08 of r, about one part in 10,000, and the sum over
the 99 outcomes is 12147454997539/65536 = 185,355,453.45, the figure that entry
64c075ac set its H1 against. For beta*, the only part that the claim of this
package uses, the three figures coincide (10.1). On the whole class the same
eight conditions keep 76,072,772.68, less than half, and no outcome there is
free of violating solutions: the rule belongs to this sub-class.

The submitted program also holds the rules of four and six conditions that rule
A contains; it uses only rule A.

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
and the sub-class and the rule by the count as well. Beta* is the beta of the
solver's solution for these constants (Section 12) and the first of the 53
values of beta with a part in the sub-class by the conditional rate of 10.1.

**Real messages in the root arrangement: what exists.** All of the following
are participant measurements, made for entry 64c075ac in the arrangement of
Sections 4 to 6 (counter 0, flags 11). They bear on the seven-word model M, on
which the counter rate rests as well, and on rule A; they are not measurements
of the counter search or of its budgets.

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
trials per run: 8,192 independent contexts; 512 outer steps with 16 values of
X2 each; and 8,192 contexts from a second seed. The first two were drawn from
the same seed text, so the 512 contexts of the first value of X2 of each outer
step of the second are also contexts of the first. Rule A is satisfied by
2^-8.0019, 2^-7.9992 and 2^-8.0000 of the trials. The share of the batches that
run stage 2 is 0.02617, 0.02622 and 0.02622; independent trials would give
0.0270, and the root batch's budget was 0.03125. Single contexts have between
0.0071 and 0.0421, the 512 outer steps between 0.0238 and 0.0289, and the one
value of X2 run in full above has 574 of 18,725, a share of 0.0307. In the
review of the text of entry 64c075ac three helper agents measured the same
share again, each once and with a program of its own, in contexts in the ranges
of the root search of that entry: 0.026171 in 8,192 contexts, 2^30 trials from
four seeds (0.02609 to 0.02626 per seed, 5 contexts above the budget, h1
anchored on 16,384 trials, all equal); 0.02619 on 2^22 trials; and 0.02620 in
640 contexts, 4 of them above the budget. The first was run again for that text
with the same output. Until the graphics-card and scaled-down runs below, these
were the only measurements that have the sub-class and the rule of this
package.

*Layout runs of the two-level arrangement (graphics card).* Real messages
enumerated as the root search of entry 64c075ac enumerates them (six outer
words fixed for a run, consecutive values of X2, every member in list order,
batches of seven consecutive members), but for the whole class of 524,288
members and with the rules of four, five and six conditions of entry c66f230d:
24 outer tuples of 2^40 trials, two deeper runs of 2^44, eight runs with X2
spread over its range, 4,096 random outer tuples and 4,096 consecutive values
of w5. A second helper agent recounted the raw outputs with its own parser (451
comparisons, 449 equal, two differing in the last printed digit), rebuilt the
program, repeated one run, and checked on the processor that the layout is the
algorithm's. Averaged over outer tuples the counts agree with the model within
their statistical error; for the deepest event that error is large, 138 of
152.0 being a ratio of 0.91 with one-sided 95% limits 0.785 and 1.046.

| Event | Probability per trial | Average against the model |
| --- | --- | --- |
| rule with 4, 5, 6 conditions | 2^-4 to 2^-6 | within one part in a million |
| listed beta | 2^-7.96 | +0.73 standard deviations |
| listed beta and tau | 2^-18.88 | +0.83 standard deviations |
| listed partial E3 event | 2^-32.2 | -0.24 standard deviations |
| listed E1 outcome | 2^-40.15 | 138 of 152.0 expected (-1.14) |

What they do not support, and what this text does not claim: independence of
the trials inside one outer step. The share of the trials of one value of X2
that satisfy a rule is not binomial (for five conditions its variance is 2.7 to
181 times the binomial one), and the members of a batch pass together. For E1
the rate of a listed tau given a listed beta is a property of the outer tuple:
for 17 cells carrying 24% of the count it lies between 0.02 and 2 times its
average, it is the same for 4,096 consecutive values of w5, and the cause is
known (Y12 and w5 are fixed inside an outer step). A weighted estimate of the
rate of solutions of one outer tuple, relative to the average, has a standard
deviation of about 0.7% between tuples; it has mean 1 by construction and stops
at the level of beta and tau. One count is unexplained: in one window of 2^44
trials of one tuple, 3 listed E1 outcomes were seen where 14.65 are expected
(probability 0.0003 under a Poisson law); the next window of the same tuple has
16, and the cells one level up do not differ. Chance is the likelier reading
and it is not excluded that it is not chance. The E1 test passes at 2^-31.41
per trial (2^-31.20 in the tuple with the most). The outer words here are
random words: no run has C0.d1 in the short range of the root search, and none
holds a whole outer step, the longest having 2^26 values of X2 of one tuple.

*Scaled-down end-to-end runs in the two-level order.* The whole search of this
pair of lengths was run on small versions of the hash, with 8-bit and 10-bit
words and 2-bit bytes, messages of 7W - 1 and 7W + 7 such bytes, random
constant sets and for each its best class of 4 to 64 members. A run is four
random seed words and a number of outer steps, each with all 2^W values of X2
and all members; both byte strings of every trial are hashed completely and all
eight digest words compared, with no rule and no filter. The prediction for a
run is the number of solutions of the seven-word system for that set, by
complete enumeration, times the number of outer steps over 2^(5W). All runs
made in this folder, each counted once: 436 runs, 470 collisions found against
467.6 predicted (+0.11 standard deviations); with 8-bit words 463 against 455.9
in 415 runs, with 10-bit words 7 against 11.7 in 21 runs. Every collision was
confirmed from its two byte strings. The history must be said with the sum: the
first job of 92 runs was low (56 against 74.8, -2.17 standard deviations); two
more jobs were then made, each written down before it was run, and they were
not low (307 against 284.0 in 280 runs, and 104 against 102.0 in 60 runs for
the one constant set that had stood out); the other four runs are the
self-check of the scripts (3 against 6.8). One series of that set, 2 collisions
against 13.0 in 26 runs, was taken as chance. The larger job of the same kind,
whose expected values and rule of judgement were written down before it was
run, ran on another machine after the text of entry 64c075ac was first
assembled. It has 8,448 runs (the 92 of the first job among them): 8,108
collisions against 8,313.6 predicted (-2.25 standard deviations); with 8-bit
words 6,276 against 6,489.6 in 6,528 runs, 3.3 per cent low (-2.65); with
10-bit words 1,832 against 1,824.0 in 1,920 runs (+0.19). By that rule a
deviation between 2 and 3 standard deviations is written down and only one of
more than 3 below the prediction would speak against the model; the series of
the set that had stood out has 38 against 40.0 there. No run has a failed check
or a false collision. The cause of the shortfall at 8 bits is not known; a
dependence of the rate of one outer step on its fixed words, which is stronger
at small word sizes, is one possible reading and is not established. These runs
test the model for whole collisions in this loop order at small word sizes.
They have no sub-class, no rule A and no packed batch.

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
machine).* After the text of entry 64c075ac was first assembled, 24 runs of
2^45 real trials each, 2^49.58 in all, were made with the six constants of this
package for the whole class, in the layout of that entry, and counted against
the exact expectations of the model: listed beta 3,401,612,690,888 against
3,401,614,098,432 (-0.76 standard deviations), listed beta and tau
1,750,004,875 against 1,750,007,808 (-0.07), listed E1 outcomes 692 against
690.78 (+0.05) and partial E3 events 171,097 against 171,316.3 (-0.53); every
run lies within 2.2 standard deviations on every count and no run has a failed
check. Like the layout runs, these support the model on average and at about
2^-40, for the whole class and not for the sub-class or rule A.

*Real messages for the sub-class with rule A (graphics card).* After the text
of entry 64c075ac was first assembled, the sub-class and rule A were run on
real messages on a graphics card: 24 outer tuples, 2^23 values of X2 each with
all 131,072 members, 2^44.59 trials in all, bad 0 and contradictions 0. The
added rule agrees with rule A of the submitted program on 2^21 random words of
h1, with 0 disagreements. Rule A passes at 2^-8.000002 of the trials
(103,079,088,429 passes), the same statement as the processor runs at 8,192
times the trials; and 0.026178 of the packed words of seven consecutive members
enter stage 2, against 0.027025 if the seven members were independent and
0.03125 charged there, so the measured entry was 0.838 of that charge. The
deepest events with an exact probability that the run reaches are the listed
partial E3 event at 2^-32.2 (6,314 seen against 5,353.63 on the whole-class
value) and the listed E1 outcome at 2^-40.15 (14 seen against 21.59, a
shortfall this run does not resolve). On the same pin and geometry the listed
partial E3 event comes at 1.18 times its whole-class rate (8.9 standard
deviations of the run scatter apart), in the sub-class's favour; in an
independent-context model run restricted to the sub-class the same marker is
1.148 plus or minus 0.051 times its whole-class value, and with real messages
on the same members 0.998 of that. This is the first real-message figure of any
kind that says the sub-class is richer than the class, and it points the way
the count does. It is NOT the counted gain: the marker is one call deep at
2^-32 while the gain 1.142 is in the counted rate r at 2^-100.53, which no
measurement can reach; and rule A is a necessary condition for a collision and
so is positively correlated with the marker (268 of the 6,314 partial E3 events
pass rule A, a factor of 10.9 over the rule's own rate), which is what this
package's own argument predicts and is not evidence that the rule keeps the
counted mass. The kept mass of rule A, 185,358,111.47 of 185,377,197.55, is not
measured by it.

*A scaled-down end-to-end run with the sub-class and an eight-condition rule.*
The whole search was run on an eight-bit version of the hash with both pieces
that entry 64c075ac added to the path of entry c66f230d: a sub-cube that keeps
a quarter of the members (two more fixed bits of e1, the step by which this
sub-class fixes two more bits than the class) and an eight-condition parity
rule on the eight-bit word h1 (pass rate 2^-8), on two constant sets, with
every trial that passes the rule built as two real messages of 55 and 63 toy
bytes and hashed in full. In 30 runs, 515,396,075,520 trials examined and
2,013,236,457 of them passing the rule and hashed: 121 collisions against
120.23 predicted from the exact table over exactly the trials tried (standard
deviation 10.96, z +0.07), with bad 0, bogus 0 and lost 0, and the first stage
on its own 2,013,236,457 passes against 2,013,265,920 expected (z -0.66). The
plan and the reading rule were written and hash-stamped before the first six of
the thirty counted runs; the other twenty-four were declared after that first
result (29 collisions against 24.05) had been read, and are reported apart from
it. This establishes, with real collisions, that selecting trials by a sub-cube
condition on e1 and by an eight-condition rule on h1 leaves the collision rate
of the survivors at the exact per-trial count, to within 9 per cent. It does
NOT establish the kept mass of rule A: at eight-bit words no eight-condition
rule keeps almost all of the collision mass (the scaled rule keeps 7 to 9 per
cent, where the real rule keeps 99.99 per cent by the count), so that part of
the rate stays a counting claim, untested here.

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

**Real messages in the counter arrangement.** This and the next paragraph
report participant measurements of the counter arrangement; the organizer's
harness does not run them, and they are untrusted evidence for it. On a
graphics card a helper agent ran the counter construction on real 32-bit
messages, with random outer words and 2^12 consecutive members of Q* per outer
step: 2^45 trials with Y4 in the sub-class and 2^44 with Y4 in the whole class,
and the same counters on the seven-word model with c1 in Q* (2^44 and 2^43
model trials); on a processor, four runs of 2^20 outer steps with 2^16 members
each. Every real trial had the difference beta* (2^45 of 2^45). Against the
exact figures of the model:

| Event | Model, exact | Real counter trials |
| --- | --- | --- |
| tau listed for beta* | 2^-10.696 per trial | 2^-10.696 per trial |
| listed E1 outcome (beta*, tau, eps), sub-class | 10,176.0 | 10,129, that is 2^-31.694 per trial |
| listed E1 outcome, both classes together | 15,264 | 15,139 (-0.8% +- 0.8%) |
| rule A | 2^-8 | 2^-8.000 |
| listed E1 outcome and rule A, both classes | 59.6 | 55 |
| listed partial E3 event, whole class | 3,569 | 3,626 |
| E1 test of Lemma N passed (n = 0) | | 2^-26.02 per trial |

The ratios of the real to the model runs, in the sub-class with Poisson errors:
listed E1 outcome 1.009 +- 0.017; listed tau 1.0001; rule A 1.0000; E1 test
0.9998 +- 0.0024; listed tau and rule A 0.9999 +- 0.0002; listed E1 outcome and
rule A 0.90 +- 0.25; listed partial E3 event 1.057 +- 0.020, where the true
error is larger because these events cluster by outer step (whole class
0.971 +- 0.028); each of the four residual words zero 1.019, 1.009, 0.984 and
0.990, each +- 0.006 to 0.021. In the arrangement of entry 64c075ac the same
events of beta* are rarer by the factor of the prescription: c1 lies in Q* with
probability 2^-11 there, and the listed E1 outcome of beta* has 2^-42.69 per
trial, against 1 and 2^-31.69 here. So the E1 side of a counter trial carries
the factor 2^11 that the count predicts, and the E3 side is unchanged. On the
processor the number of trials of one outer step that satisfy rule A has a
variance 572 times its mean, and that of the listed tau 247 times: single outer
steps differ strongly, and only averages over outer steps agree with M. No
event here is deeper than about 2^-40, the listed E1 outcome with rule A; none
is the joint event of H1', at about 2^-91.

**A scaled-down end-to-end run of the counter arrangement.** The whole counter
search was run on an eight-bit version of the hash: 2-round BLAKE3 with 8-bit
words, 2-bit toy bytes, 64-byte blocks and 1,024-byte chunks, with eight sets
of toy constants fixed before any counted run and the class of each. The
messages are F || A and F || B of 1024 t + 55 and 1024 t + 63 toy bytes with
t = 1 to 255, F being t chunks of zero bytes; the last chunk is compressed with
counter t and flags 3, and t = 0 is dropped (79.3 million of 20.3 billion
trials, one in 256, as expected). The inner word d1 runs over the values of the
heaviest beta of each set, the toy form of c1 in Q*. Both last-chunk
compressions of every trial were evaluated in full and all eight words
compared, with no rule and no filter; every collision was rebuilt as two
complete messages and confirmed by two independent toy tree hashes, one of them
written after the organizer's code. The predictions are exact model counts for
each set. Over the eight sets:

| Arrangement | Collisions found | Predicted | Trials per collision |
| --- | ---: | ---: | ---: |
| root instance (counter 0, flags 11) | 67 | 64.0 | 8.8 * 10^8 |
| counter, d1 in the set of the heaviest beta | 251 | 255.0 | 8.1 * 10^7 |
| counter, d1 not restricted (control) | 54 | 47.8 | 8.2 * 10^8 |

All 372 collisions are collisions of complete messages, and no trial failed a
check. The realised fraction of the predicted gain of the prescription is (251
/ 255.0) / (67 / 64.0) = 0.94 +- 0.13, that is -0.09 +- 0.20 bit: no loss is
detected. The control shows that the counter alone, without the prescription,
changes nothing. This tests the mechanism with real collisions. It does not
test the size of the factor at 32 bits, which the toy cannot reach (its factors
are 3.9 to 31.8 on the eight sets, against 747.92 here), and it has no rule A,
no sub-class and no packed batch.

**Real messages in passing outer steps.** A participant measurement made for
this package, untrusted evidence like the two paragraphs before it, which the
organizer's harness does not run. On a graphics card a helper agent ran the
counter construction on real 32-bit messages with Y4 in the sub-class. Uniform
random outer steps, drawn by the measuring program, were filtered by conditions
(1) and (2) with tables generated as the submitted program generates them, and
every passing outer step enumerated the whole of Q*, all 2^21 values of c1 in
the program's member order, as 299,594 words of seven lanes in the layout of
the run-wide table: 2^22.00 passing outer steps, 2^43.00 trials. A control with
the filter off ran 2^18 outer steps, 2^39 trials. On 330 records a check
against the submitted program (step CO, the filter, the member order, rule A
and the word n of the E1 test from the program's compression of the real last
chunks) found no difference. Errors are taken per outer step, because the
trials of one outer step cluster.

| Event | Over all outer steps | In passing outer steps | Ratio |
| --- | --- | --- | --- |
| outer step passes the filter | 2^-9.8132 (pi, exact) | 2^-9.8127 | z = +0.7 |
| rule A, per lane | 2^-8 | 2^-8.000 | 1.0003 +- 0.0006 |
| word enters stage 2 | 0.022512 +- 0.000050 (control) | 0.022503 +- 0.000013 | 0.9996 +- 0.0023 |
| E1 test of Lemma N passed, per trial | 2^-26.02 | 2^-26.023 | 0.9945 +- 0.0031 |
| listed E1 outcome, per trial | 2^-31.694 | 2^-31.724 | 0.979 +- 0.022 |
| lane processed in step 3, per trial | | 2^-31.477 | 1.01 +- 0.02 of E1 test times word share |
| listed partial E3 event, per trial | about 2^-32.4 (control, 98 events) | 2^-24.17 | about 2^8 |

So inside passing outer steps rule A, the share of the words that enter stage
2 and the E1 test keep their values over all outer steps, and the lanes that
step 3 processes are as many as an E1 test independent of the entry to stage 2
gives. The share of the words that enter stage 2 is 0.8327 +- 0.0005 of the
0.02703 of seven independent lanes, because the lanes that satisfy rule A
cluster inside a word (per outer step the count of trials that satisfy rule A
has standard deviation 9,785 against a mean of 8,195). Over the 12 patterns of
the filter's masks with at least 40,000 passing outer steps each, rule A lies
between 2^-8.006 and 2^-7.996, the word share between 0.0224 and 0.0226 and the
E1 test between 2^-26.08 and 2^-26.00. The partial E3 event, a condition on E3
like (1) and (2), is concentrated by the filter, as expected. Trials with t = 0
were not dropped, at most one per outer step. These measurements bear on the
filter and the counter batch of the program, which the search of 9.1 does not
run; they reach no event deeper than about 2^-31.7 and no collision.

**What does not exist.**

- No organizer-run check of the counter instance: an experiment of the harness
  tests events of complete digests, and the half-collision of the counter
  instance lies in the chaining value of a chunk that is not the root (6.4,
  Section 7). Its checks are participant computations with the organizer's
  functions imported (Section 7) and the program's self-test (9.3).
- No measurement of the joint event of H1', at about 2^-91 per trial. The
  deepest counter events measured are the listed E1 outcome at 2^-31.7 and that
  outcome together with rule A, 55 events at about 2^-39.8.
- No proof that the construction's trials have the joint law of the model words,
  of the share of the success mass that the rule t != 0 removes, or of a bound
  on the factorial ratio of the good trials of an outer step. These are the open
  parts that H1' declares (10.3).
- No implementation of the search of 9.1 at any word size: no E1 record table,
  no table of a frame and no run of its steps exist, and none of its operations
  is counted by a program. The participant checked the equation that the table
  solves and the local E1 equations on real trials (9.7), not the search.
- No measurement of H1' (ii); a workload measurement that the participant made
  for another search of this construction does not apply to this one (GPT Sol,
  answer AK).
- No proof that the share pi_o of the sampler's outer steps that pass the filter
  equals pi; it is measured. The search of 9.1 does not use the filter.
- No scaled-down run of the counter search with rule A, the sub-class, the
  packed batch or the outer filter; the toy run has none of them.
- No complete message of a found pair; the complete messages hashed (Section 7)
  are trials, with t from 1 to 16,383.
- The count 67,698,688 and its seven outcomes are reproduced by Section 17;
  the list of 60 values of beta used by SEL rests on uncertified solver
  answers and on the other model's enumeration.
- The search of 9.1, its tables and its step 4 exist only in this
  text; the program has steps CO and CT, the test of rule A and the compression
  that step 4 uses, and it counts the batch, the outer step and the filter,
  which the search does not run.

**Limits of the evidence.**

- H1' is an assumption, at 5/7 of the count where the earlier entries on this
  track assumed half. The factor is set against a count under M with c1
  conditioned in Q*; the count does not show that M holds, and Lemma S1 is a
  statement inside M. Lemmas S2 to S4 prove parts of the transfer to the
  construction, not the joint law of the seven words, and nothing proves H1'
  (ii).
- M fails inside one context and one outer step: in the root arrangement for
  rule A and for the call E1, and in the counter arrangement for rule A, whose
  count per outer step has a variance 572 times its mean. Where it was measured
  it holds on averages over outer steps. The search of 9.1 fixes Y4, Y9, w8, Y12
  and w5 for the 2^21 trials of a frame, which is one outer step, so the success
  of a run rests on FRAMES = 843,790,834,046,997,321,198, about 2^69.516,
  independent outer steps and on H1' (ii), that one outer step rarely holds more
  than one listed good trial: the premise of entry e7b17fd1, on groups of the
  same size.
- The model is checked on real messages to about 2^-40, not at 2^-91.
  Scaled-down whole-collision runs are level for the counter arrangement
  (0.94 +- 0.13 of the predicted gain) and, for the root arrangement, level at
  10 bits and 3.3 per cent low at 8 bits in the largest job.
- The constants, the class, the sub-class, rule A and beta* were chosen by the
  count, so they favour any choice that the model overrates. The part of beta*
  is 36.5 per cent of the count of the sub-class and rests on seven outcomes
  with one value of eps.
- The count rests on programs that are not in the package and on a list of
  values of beta that is complete only by uncertified solver answers and the
  other model's enumeration; the other model reconciled the records and did not
  recount them.
- The costs of the search are GPT Sol's allowances in words (Sections 9.5, 9.6
  and 11); none is counted by a program, and the participant has not implemented
  the search. The counts of the counter batch, the outer step and the filter are
  the program's own, on the machine of 6.5, and are not used in the time bound.
- The messages of a found pair have about 2^41 bytes on average and fewer than
  2^42; computing their digests costs about 2^37 compressions, which is
  charged, and no check of this package computes them.
- Helper agents of the participant wrote and checked the counter construction,
  the filter and this text, and another AI model proved Lemmas IP, F, S1 to S9,
  AK, KT and TG, derived the count of passing pairs and the counts of the E1
  record table, and gave the search and its allowances; no person has read it.

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
  steers cheaply. Proposed by the participant; helper agents.
- Table lookups prescribing a second word, and loops of over two levels:
  per-trial equations stay at the two-level numbers (11, 25 and 26 to the first
  test word, the second and both; 6, 18 and 19 for entry c66f230d). Helper
  agents. These were lookups per trial; the table of Section 9 is built once per
  frame and serves the one outer step of the frame.
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
- A constant chunk counter: with t fixed for a run the trials are only
  relabelled and the rates do not change; a helper agent measured several
  constant counters and found no gain. The gain of this package comes from
  solving t per trial (Section 8). Helper agents.

**Scope and limitations.**

- No full collision is exhibited; this is an analytical cost claim like other
  packages on this track and, unlike a birthday search, tests each trial that it
  forms against zero; its tables, below 2^39 bytes, do not grow with the number
  of frames or of trials.
- The messages have 1024 t + 55 and 1024 t + 63 bytes, with 1 <= t < 2^32 the
  solved chunk counter, about 2^41 bytes on average. They rely on the chunk
  counter and the true block length being inputs of the compression, as the
  target profile specifies; the colliding compression is that of the last
  chunk, which is not the root, and Lemma TR carries the collision to the
  complete digests in the profile's own tree mode. The 63-byte last chunk ends
  in eight zero bytes, and both zero-filled last blocks have words 14, 15 and
  the top byte of word 13 zero.
- The gain over a birthday search comes from matching half the chaining value by
  construction, constants that let the other half match usefully, the sub-class
  of Y4, the prescription of c1 in the cube of beta* that the solved counter
  makes possible, assumed at 99,033,509,302 times the uniform rate (5/7 of the
  count), and the table of a frame with the E1 record table, which find the
  records whose trial in the frame's outer step has that E1, so that only
  E1-listed trials are formed: 2^90.516 trials covered in FRAMES frames, at most
  2^21 formed in each, not 2^128.
- A brief literature search found free-start collisions and near-collisions of
  reduced BLAKE compression functions and no collision attack on 2-round
  BLAKE3. No priority or novelty claim is made.
- The time bound charges every step of the search at an allowance in words (GPT
  Sol, answer AK), every row at its worst case in a run of FRAMES frames: an
  upper bound under the cost model's convention, not a measured time, checked by
  no program and by no organizer run. Its largest term is the search part, below
  2^101.91954 units, almost all of it for the table built in every frame; the
  selection procedure of Section 12, charged in full, is below 2^69.976, below
  2^-31.94 times it.

**Field meanings.**

- time_log2 = 101.9196 bounds total charged time by 2^101.9196 units (Section
  11): the search below 2^101.91954 units, the selection procedure SEL, charged
  in full, below 2^69.976, and the final step below 2^38; the exact bound is
  2^101.9195393091...
- memory_log2_bytes = 44 bounds the storage of the selection procedure (below
  2^35 bytes), the search (below 2^39: the E1 record table and the table of one
  frame, 388,694,540,288 bytes, and fewer than 2^21 bytes more), the code (2^19)
  and the output (below 2^43 bytes), even all held at once: their sum is below
  2^44 (Section 12).
- preprocessing_log2 = 70 bounds the selection procedure SEL of Section 12 and
  the E1 record table of 9.6 by 2^70 target-compression units (at most
  498,959,034,010,404,040,996,736 primitive operations, less than 430 * 2^70).
  Every search of SEL runs over a stated range and every program run in it halts
  at a stated cap, so this is a bound by construction; that SEL returns the
  stored values rests on the participant's records (Section 12). The tables of
  the frames are built during the search, one per frame, and are charged in
  time_log2.
- nonuniform_advice_log2_bytes = 7 bounds the stored constants, eta, the two
  bits of the sub-class, the constants of rule A, beta* with its cube and the
  seven values of tau with eps of the outcomes of beta*, 92 bytes, by 128 bytes.
- success_probability = 0.40 holds under H1' as shown in 10.4, whose bound is
  0.4014985013...

The required baseline_improved identifier blake3-r2-nominal-v2 names the
organizer's nominal display reference 128, not an established attack, qualified
baseline or security bound; 101.9196 is below it. Whether a qualified result
improves the Yukon incumbent is decided separately; no Pareto dominance claim
follows.

## 14. Corrections to our entry c66f230d

Entry c66f230d (time_log2 97.6) cannot be edited. After it was filed its text
was examined three times: by a hostile review of another AI model (Grok 4.7),
by a referee report of another AI model (GPT Sol 6.1), and by an audit of a
helper agent of the participant that had written nothing of it. Twenty-four
points were raised. Each was looked up in the filed text and checked against
its source; none of them changes a lemma, the count or the scalar of that
entry, or the value of a figure of its claim block. The same corrections are
applied in this package wherever the passage recurs. The full list, with the
filed wording beside the corrected wording, is in the work folder of entry
64c075ac; below are the four that bore on a figure or a scope of the text of
that entry, and then the other twenty in one line each.

*The four that bore on entry 64c075ac.*

1. H1 is not implied by the model M alone. The filed text said that H1 is M
   together with a rate; in truth M and the rate give the rate of a single
   trial, and H1 also assumes that the good trials of a run do not come in
   clusters, which M does not imply. (GPT Sol 6.1, with a counterexample: one
   model sample repeated for every trial has the model's law in every trial and
   no independence.) Section 10.3 of this text declares the rate and the
   clustering of the good trials of one outer step as the two parts of H1'.
2. The declared preprocessing of 2^63 units is an exhaustive search over the
   two message words (W4, W13) at the four given inputs. It does not recompute
   the four inputs and does not bound the selection of the constants, of eta or
   of rule A; for that selection there is only an estimate from running times,
   below 2^60 operations, which is not a count. (Grok 4.7 and GPT Sol 6.1.)
   Section 12 of this text replaces that estimate by a selection procedure with
   a bound.
3. The share 74,899 / 65,536 = 1.142868 rounds to 1.1429, not to the filed
   "1.142 times 2^-5" read as 1.1428; the filed figure understates the room of
   H3. (Audit and GPT Sol 6.1.)
4. The filed sentence that "the six means lie between 0.9977 and 0.9994, all on
   the low side" is true of the six samples that were chosen. Two further
   samples of the same program have means 1.0008 and 0.9978, and the audit's
   own 512 independent contexts give 1.0039 with a standard error of 0.0028.
   (Audit.)

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
it was filed; Section 13 reports the runs made since.

## 15. What is the same as entries 64c075ac and e7b17fd1 and what is new

*The same as entry 64c075ac.* The target and the two block lengths with the zero
words they force; the six constants and Fact P; the length cancellation and
Lemmas L and H; the class of eta = 830303cf, the sub-class and Lemmas Q, Q2, T
and N; rule A and Lemma A; the root instance of Sections 4 to 6 with its
two-level batch, which the declared experiments run, with their kinds and masks
unchanged; the packed word of seven lanes and the machine of 6.5 with its
convention; the seven-word model, the count of the sub-class and the method of
the count; the selection procedure SEL for the constants, the class, the
sub-class and rule A; and the form of the rate premise H1, here H1'.

*The same as entry e7b17fd1.* The counter construction of Section 8 with Lemma
TR, Lemma CT, Theorem C and Lemma IP; the counter batch of 9.2 with Lemma CB and
its counts 41 and 72, which the program holds and the search of 9.1 does not
run; the cube Q* of beta* and the count 138,646,913,024; Lemmas S1 to S8; and
the selection procedure SEL, its steps 1 to 6 with their ranges, charged in
full.

*New.*

| | entry 64c075ac | entry e7b17fd1 | this package |
| --- | --- | --- | --- |
| colliding compression | root: counter 0, flags 11 | last chunk: counter t, flags 3 | last chunk: counter t, flags 3 |
| messages | 55 and 63 bytes | 1024 t + 55 and 1024 t + 63 bytes | 1024 t + 55 and 1024 t + 63 bytes |
| inner word of a trial | the member y | c1, with t solved | c1 from a record, D2.a1 drawn with the frame and tested through the key K* of its table, with t solved |
| difference beta* of E1 | probability 2^-11 | by construction | by construction |
| E1 outcome of a formed trial | tested | tested | one of the seven, by construction |
| count for H1 | 185,355,453 | 138,646,913,024 | 138,646,913,024 |
| assumed factor | 92,675,904 | 69,323,456,512 | 99,033,509,302 |
| margin | 2.00 | 2.00 | 1.40 |
| outer filter | none | none | exact, Lemma F; in the program, not used by the search |
| trials | 2^100.534 trial-equivalents | 2^90.987 | 2^90.516 covered, at most 2^21 formed per frame |
| clusters | 64 trials, gate H4 | none | none |
| heuristics | H1 to H6 | H1', H2', H3' | H1' (rate and dependence) |
| stage A, stage 2 | 47, 135 | 41, 72 | 41, 72 in the program, not run by the search |
| share of stage 2 | 1/32 | 1/32 of all words | none |
| budget of step 3 | | 2^72 lanes | none: at most 2^21 roots per frame |
| charged | 1.65 per equivalent | 6.5 per trial | 2^20.152 machine units per covered trial, allowances in words |
| search memory | below 2^26 bytes | below 2^25 bytes | below 2^39 bytes |
| preprocessing | 2^80 | 2^80, with one more step | 2^70 |
| search part of the time | | below 2^84.940 | below 2^101.91954 |
| time_log2 | 92.53 | 84.98 | 101.9196 |

New against entry e7b17fd1: the outer filter, its exact share and Lemmas F and
S9 (Sections 8 and 10.2), which the program holds and the search of 9.1 does not
use; the search of Section 9, from GPT Sol's answer AK: the exact equation of
Lemma AK, which ties E1.a2 to the seventh outer word, the table of a frame with
Lemma KT, and the E1 record table of the seven outcomes with Lemmas TG and TG1;
a fresh frame for every outer step, with its table built again each time (GPT
Sol, answer AP), so that the heuristic is H1' in the form of entry e7b17fd1,
rate and dependence, without H2' and H3' and without a root cap; the rate part
of H1' at 5/7 of the count in place of half of it; the measurements inside
passing outer steps (Section 13); the outcomes of beta* as an output of SEL step
6; step 3a of SEL, which keeps only the betas with a part in the class, and the
transform of its step 5, with its first half shared by the matrices of one
prefix, so that SEL, over the same ranges, is bounded by 2^69.976 units in place
of 2^79.71; the E1 record table, 2^46 operations, charged with SEL as
preprocessing; and 32 more bytes of advice for the seven values of tau and eps,
92 bytes in all.

The search part of the time is below 2^101.91954 units here against 2^84.940 in
entry e7b17fd1, 16.98 more in the exponent. Entry e7b17fd1 formed every trial of
its run, 2^90.987 of them, at 6.5 machine units each. This search covers
2^90.516 trials and forms only the E1-listed ones, at most 2^21 in a frame at
8,192 machine units each, but pays 2,443,836,395,520 machine units, below
2^41.153, per frame of 2^21 trials, almost all of it for the table of the frame,
built again for every outer step: 2^20.152 machine units per covered trial. The
assumed rate is 5/7 of the count where entry e7b17fd1 assumed half, which
shortens the run by a factor of 1.4, 0.485 in the exponent; at half the count
this search would be submitted at 102.4342 (10.4). The claimed bound is 101.9196
against 84.98: this package is filed to record the path of the frame search with
premises of the already-reviewed kind only, not as an improvement. The selection
procedure of Section 12, charged in full in both, was 2^-5.229 of the search
part in entry e7b17fd1 and is below 2^-31.94 of it here, where steps 3a and 5
bound it by 2^69.976 units in place of 2^79.71.

Entry e7b17fd1 was 7.55 below the bound 2^92.53 of entry 64c075ac in the
exponent: the prescription of c1 gained 9.55, the factor 747.92, and the
cheaper batch 0.24, 6.5 against the 7.7 per trial that the arrangement of
entry 64c075ac charges without its clusters, while the clusters of that entry,
worth 2.22 there, are not used, and the selection procedure, charged in full,
weighed 0.02 more there than the allowance of the one formula. Also new in
entry e7b17fd1, and new on this track as far as the participant knows: a chunk
counter solved per trial, which makes one more round-1 word prescribable, and
a claim whose colliding compression is not the root.

*History: entry 9a9f3b7b.* The search of Section 9 was filed as entry 9a9f3b7b
at time_log2 71.15, with frames of 2^32 outer steps, one table serving all of
them, and three heuristics: H1' (the rate only), H7' (the good trials of a whole
frame of 2^53 trials: E[W (W - 1)] <= 0.0065 E[W] for their number W) and H8'
(the mean number of E1-listed trials of a frame, which set a root cap). The
organizer's review found that entry not evaluable on H7' alone: a score-critical
premise with no proof, no experiment and no scaled-down analogue at the scale of
a frame. This package removes that premise rather than argue for it. Each frame
serves one outer step, so the dependence premise is the one on outer steps of
the reviewed entries (judged plausible_not_refuted) (H1' (ii)); a frame has at most 2^21 roots (Lemma TG1), so
the root cap and H8' are no longer needed. The price is the table built again
for every outer step, and the bound rises from 71.15 to 101.9196. GPT Sol
(answer AP, Section 3) gives 99.04 for the same restatement under its own cost
rows, which charge the table at 80 machine units per value of D2.a1; this
package keeps its own allowances of 9.5 and Section 11, 512 per value of D2.a1
and the scan of the E1 record table in every frame, and its success target 0.40.

## 16. Credit

The contest is cooperative and this package builds on the work of others. Each
is named for what they did. Apart from the helper agents of the participant,
nobody named here has reviewed this package, and a credit is not an endorsement
by the person or model credited.

- **GPT Sol 6.1 (OpenAI)**, an AI model run by the participant: the sub-class
  of this package as a sub-cube of the class, with the exact rates of sub-cubes
  from which it was chosen; the eight conditions of rule A; the exact fractions
  of the rates with and without the rule, which our counter reproduces digit
  for digit; and the referee report on entry c66f230d behind items 1, 2, 4, 6,
  7, 11, 12, 19 and 23 of Section 14. A second instance of the same model, run
  separately: a further count of the two fractions and the statements on
  optimality quoted in Section 13. For the counter construction: Lemmas IP and
  S1 to S8 with their proofs; the reconciliation of the seven outcomes of beta*
  and of their sum with the count records; the ranking of the 53 values of beta
  by their conditional rates; and the statement of the open part as a premise,
  from which H1' is worded.
- **winglock**, a participant on this track: the idea of searching only a
  sub-class of the members, chosen by an exact count per member. It was first
  used in winglock's entry 18a7fc52 (108.9) on the class of our entry 04638ed8
  (112.4). That entry is also, to the participant's knowledge, the first public
  count of the model rate without sampling (a carry automaton on the E1 side,
  sign patterns and a carry recursion on the E3 side). The split used here is
  for another class and comes from another count; the idea is winglock's. Step
  4 of the selection procedure of Section 12 follows winglock's choice of the
  sub-class S8 in entries 2125212 and 2bb5d604 from the exact rate of every
  member of the class.
- **Th0rgal**, a participant on this track: building the values that depend on
  the member alone once per outer step and not once per trial was first
  published in Th0rgal's entry df8bd46d (111.75), for two lists of the family
  with lengths 60 and 62. The arrangement of the root instance, five lists per
  member for the family with lengths 55 and 63, was derived by a solver search
  of the participant some hours later, with that entry known. Three coding
  steps of 6.5 follow Th0rgal's entry 8c81a219 (98.70), which made them on the
  batch of our entry c47c1a80: one stored constant w12 - S1 - S6 across two
  calls, the rotation by one bit with one mask, and an order of the operations
  that frees registers.
- **5kyguy**, a participant on this track: keeping masks in registers across
  the loop over the members, in entry 404d14df (112.12), there on a machine
  with 32 registers. Here nine words are kept in the batch of 6.5 and seven in
  the counter batch, on the machine with 16 registers.
- **tekkac**, a participant on this track: the lane layout of 6.5, seven 36-bit
  lanes with a masked rotation, from the public ticket 2bf40fb.
- **Grok 4.7 (xAI)**, an AI model run by the participant: the hostile review of
  entry c66f230d behind items 3, 4, 5, 8, 13, 14, 19, 20, 21, 22 and 24 of
  Section 14; and a tightened batch of its own for the first form of the
  two-level program (stage A 41, stage 2 127), which was compared with the
  batch of 6.5 and agrees with it in idea; it is not a batch of this package.
- **A model reached through the service Venice**: a statement on prior art and
  an argument that fixing single bits of message words does not help the first
  test. Both are unverified, and nothing of them is used in a proof or a figure
  of this package.
- **Helper agents of the participant**, instances of the same AI model as the
  author of this text: the solver search for the order of Section 4, the
  program and its tests, the count of Section 13, the first form of Lemmas T2
  to T4 and their check, the layout runs and their check, the scaled-down runs
  and their check, and the audit of entry c66f230d. For the counter
  construction: the search that found that a chunk counter solved per trial
  makes E1.d1 prescribable next to Y4, and the order of Section 8; an
  independent check of the tree mode with the organizer's code, of the free
  words of the orders and of the construction in 32-bit arithmetic; the
  measurements on real counter trials and the count of the counter batch on the
  program's machine; the scaled-down end-to-end run with real collisions of
  complete messages; an adjudication of these reports; the counter part of the
  program, its self-test and the checks of Section 7; and this text.

The half-collision, the class search and the two tests are those of the
participant's entries 17bba2ae, 5ceb1802, 04638ed8, c47c1a80, c66f230d and
64c075ac on this track, which claim 123.5, 121.5, 112.4, 99.4, 97.6 and 92.53.
- GPT Sol 6.1 (OpenAI), answer AC: Lemma F (the outer-step filter lemma), Lemma S9 and the exact certificate of the pass share; helper agents (instances of the AI model that wrote this text) proposed the outer-step filter and built and measured it.
- GPT Sol 6.1 (OpenAI), answer AK: the search of Section 9, from the exact equation of Lemma AK and the table of a frame (Lemma KT) to the E1 record table with its recurrence and counts and Lemma TG; the allowances of Sections 9.5 and 11; and the rate premise from which H1' (i) is worded. The participant checked the equation and the local E1 equations on real trials (9.7) and recomputed the figures in integers.
- GPT Sol 6.1 (OpenAI), answer AP, Section 3: the restatement of the search with a fresh frame and table for every outer step, which removes the premise on whole frames on which entry 9a9f3b7b was ruled not evaluable.

## 17. The counting program for 67,698,688

The program below computes the part of beta* = 18b0e098 in the rate of the sub-class (Section 10.1) in exact integer
arithmetic, with the standard library only: every tau (taus), both roots eps (eps_roots), the E1 count L_j (L_count) and
the E3 count N3_j with and without rule A (N3_count), each as an exact carry count over all bit positions. Nothing is
sampled, capped or delegated to a solver. Run as `python3 -B count.py`, it printed the table below in about 2 minutes
(Python 3.14); the seven rows and their sum are those of Section 10.1: 67,698,688 = 1033 * 2^16, all kept by rule A.

```python
#!/usr/bin/env python3
# Exact count of the part of beta* in the rate of the sub-class (proof.md 10.1, Section 17).
# Integer arithmetic only on the count; no sampling, no cap, no solver; standard library only.
# Run: python3 -B count.py [--beta HEX]   (--selftest: brute force at width 6, below the listing)
import sys, time
from collections import Counter
from functools import lru_cache
from itertools import product

class Inst:                                     # word width, rotations of G, constants
    def __init__(s, n, r16, r12, r8, r7, Y3, Y3B, Y11, Y11B, delta, eta, Y4s, rule):
        s.n, s.m, s.r16, s.r12, s.r8, s.sh = n, (1 << n) - 1, r16, r12, r8, r8 - r7
        s.Y3, s.Y11, s.delta, s.eta, s.Y4s, s.rule = Y3, Y11, delta, eta, Y4s, rule
        s.DY3, s.DY11 = (Y3B - Y3) & s.m, (Y11B - Y11) & s.m

def ror(c, x, r): r %= c.n; return ((x >> r) | (x << (c.n - r))) & c.m
def rol(c, x, r): return ror(c, x, c.n - r % c.n)
def wt(x): return bin(x).count('1')
def subs(X):                                    # every p with p AND NOT X = 0
    p = X
    while True:
        yield p
        if p == 0: return
        p = (p - 1) & X
def sgn(c, p, X): return (X - 2 * p) & c.m      # (v XOR X) - v for every v with v AND X = p
def pats(c, X, d):                              # every p in subs(X) with sgn(p, X) = d
    w = (X - d) & c.m
    if w & 1 or (w >> 1) & ~X: return []
    top = 1 << (c.n - 1)
    return [w >> 1, (w >> 1) | top] if X & top else [w >> 1]
def bit(x, i): return (x >> i) & 1
def adv(S, base, plus_ok, minus_ok):            # one digit of a sum checked to be 0 mod 2^n
    return {(base + cy + x - y) >> 1 for cy in S for x in range(plus_ok + 1)
            for y in range(minus_ok + 1) if (base + cy + x - y) % 2 == 0}

def eps_roots(c, beta):                         # eps XOR ror(eps, sh) = ror(eta, sh) XOR beta
    y = ror(c, c.eta, c.sh) ^ beta
    return [e for e in (solve(c, y, 0), solve(c, y, 1)) if e is not None]
def solve(c, y, x0):                            # needs gcd(sh, n) = 1
    x, i = x0, 0
    for _ in range(c.n):
        j = (i + c.sh) % c.n
        b = bit(x, i) ^ bit(y, i)
        if j == 0: return x if b == x0 else None
        x |= b << j; i = j

def taus(c, beta, eps):                         # every tau with N1 and N2 (a superset of L > 0)
    n, r8 = c.n, c.r8
    K1, K2, out = (beta + c.delta) & c.m, (eps - c.DY11) & c.m, []
    def rec(t, tau, S1, S2):
        if t == n:
            for j in range(n - r8, n):          # N2 positions that need tau bits 0..r8-1
                S2 = adv(S2, bit(K2, j) - bit(tau, (j + r8) % n),
                         bit(tau, (j - 1 + r8) % n), bit(eps, j - 1))
                if not S2: return
            out.append(tau); return
        for b in (0, 1):
            tau2 = tau | (b << t)
            T1 = adv(S1, b - bit(K1, t), bit(beta, t - 1) if t else 0, bit(tau, t - 1) if t else 0)
            if not T1: continue
            T2, j = S2, t - r8
            if j >= 0:
                T2 = adv(S2, bit(K2, j) - b, bit(tau, t - 1) if j else 0, bit(eps, j - 1) if j else 0)
                if not T2: continue
            rec(t + 1, tau2, T1, T2)
    rec(0, 0, {0}, {0})
    return out

def L_count(c, beta, tau, eps):                 # triples (c1, b1, a2) with differences beta, tau, eps
    Bc, R8 = rol(c, beta, c.r12), ror(c, tau, c.r8)
    mult = Counter(pa for q in subs(beta) for pa in pats(c, tau, (sgn(c, q, beta) + c.delta) & c.m))
    tot = 0
    for qc in pats(c, Bc, c.DY11):              # c1 AND Bc = qc: the cube of beta
        for pa, w in mult.items():
            for pd in subs(R8):
                for pc in pats(c, eps, (c.DY11 + sgn(c, pd, R8)) & c.m):
                    tot += w * e1_dp(c, Bc, qc, tau, rol(c, pd, c.r8) ^ pa, R8, pd, eps, pc)
    return tot << (c.n - wt(beta))              # b1 is free off beta
def e1_dp(c, Bc, qc, tau, need, R8, pd, eps, pc):
    S = {(0, 0): 1}                             # (borrow of c1 - Y11, carry of c1 + d2)
    for i in range(c.n):
        T = Counter()
        for (bo, ca), w in S.items():
            for x in ((bit(qc, i),) if bit(Bc, i) else (0, 1)):
                v = x - bit(c.Y11, i) - bo
                if bit(tau, i) and (v & 1) != bit(need, i): continue
                for z in ((bit(pd, i),) if bit(R8, i) else (0, 1)):
                    s = x + z + ca
                    if bit(eps, i) and (s & 1) != bit(pc, i): continue
                    T[(1 if v < 0 else 0, s >> 1)] += w
        S = T
    return sum(S.values())

def N3_count(c, tau, eps):                      # quadruples (Y4, h1, Y9, w8); and those with rule A
    A, E, T = c.eta, eps, tau
    psi = tau ^ ror(c, tau, c.sh); Psi = rol(c, psi, c.r12)
    B = A ^ E; B8 = ror(c, B, c.r8); AE = A | E
    D1 = {}
    for ph in subs(A):
        pg = pats(c, Psi, sgn(c, ph, A))
        if pg: D1.setdefault(sgn(c, ph, A), ([], pg))[0].append(ph)
    D2 = [(pf, pe) for pf in subs(psi) for pe in pats(c, E, (c.DY3 + sgn(c, pf, psi)) & c.m)]
    if not D1 or not D2: return 0, 0
    RB = 0
    for mk, _ in c.rule: RB |= mk
    X = (A & E) | (E & ~A & RB)                 # the bits of pe that G and the rule read
    Yc = Counter(y & Psi for y in c.Y4s)
    W = {pg: Counter() for _, pgs in D1.values() for pg in pgs}
    for pg, Wg in W.items():                    # W[pg][x]: sum of Y over (pf, pe) with pe AND X = x
        for pf, pe in D2:
            Wg[pe & X] += Yc[rol(c, pf, c.r12) ^ pg]
    tot = totA = 0
    for d1, (phs, pgs) in D1.items():
        D3 = [(pb, pt) for pt in subs(T) for pb in pats(c, B8, (sgn(c, pt, T) - d1) & c.m)]
        for ph in phs:
            for pg in pgs:
                for x, y in W[pg].items():
                    if not y: continue
                    for pb, pt in D3:
                        kb = rol(c, pb, c.r8)
                        g = g_dp(c, pg, Psi, kb | ((ph ^ x) & A & E), AE, pt, T)
                        tot += y * g
                        totA += y * g * rule_count(c, ph | ((x ^ kb) & E & ~A), AE)
    return tot << (c.n - wt(AE)), totA
@lru_cache(maxsize=None)
def g_dp(c, pg, Psi, kfix, AE, pt, T):          # (g1, k): g1 AND Psi = pg, k AND AE = kfix
    S = [1, 0]                                  # carry of g2 = g1 + ror(k, r8)
    for i in range(c.n):
        j = (i + c.r8) % c.n
        nxt = [0, 0]
        for ca in (0, 1):
            for x in ((bit(pg, i),) if bit(Psi, i) else (0, 1)):
                for z in ((bit(kfix, j),) if bit(AE, j) else (0, 1)):
                    s = x + z + ca
                    if bit(T, i) and (s & 1) != bit(pt, i): continue
                    nxt[s >> 1] += S[ca]
        S = nxt
    return S[0] + S[1]
@lru_cache(maxsize=None)
def rule_count(c, hfix, AE):                    # h1 with h1 AND AE = hfix that satisfy the rule
    F = 0
    for mk, _ in c.rule: F |= mk & ~AE
    ok = sum(all(wt((hfix | f) & mk) % 2 == v for mk, v in c.rule) for f in subs(F))
    return ok << (c.n - wt(AE) - wt(F))

def solvable(c, eqs, masks):                    # do patterns p_v of masks[v] make every
    S = {(0,) * len(eqs)}                       # sum(s*word) + sum(2*s*p_v) zero mod 2^n?
    for i in range(c.n):
        nS = set()
        for ch in product(*[(0, 1) if i and bit(mk, i - 1) else (0,) for mk in masks]):
            for st in S:
                nxt = []
                for (consts, coefs), cy in zip(eqs, st):
                    d = cy + sum(s * bit(w, i) for s, w in consts) + sum(s * ch[v] for v, s in coefs)
                    if d % 2: break
                    nxt.append(d >> 1)
                else: nS.add(tuple(nxt))
        S = nS
        if not S: return False
    return True
def e3_screen(c, tau, eps):                     # (a) with (c), and (b): necessary for N3 > 0
    A, psi = c.eta, tau ^ ror(c, tau, c.sh)
    Psi, B8 = rol(c, psi, c.r12), ror(c, c.eta ^ eps, c.r8)
    ac = [([(1, Psi), (-1, A)], [(0, 1), (1, -1)]),                  # vars 0 ph, 1 pg, 2 pt, 3 pb
          ([(1, tau), (-1, A), (-1, B8)], [(0, 1), (3, 1), (2, -1)])]   # (var, sign of 2 p_var)
    b = [([(1, eps), (-1, c.DY3), (-1, psi)], [(0, -1), (1, 1)])]     # vars 0 pe, 1 pf
    return solvable(c, ac, [A, Psi, tau, B8]) and solvable(c, b, [eps, psi])

def beta_part(c, beta, show=print):
    tot = totA = 0; rows = []
    for eps in eps_roots(c, beta):
        ts = taus(c, beta, eps)
        ts3 = [tau for tau in ts if e3_screen(c, tau, eps)]
        show(f"eps {eps:08x}: {len(ts)} tau pass N1 and N2, {len(ts3)} also the E3 screen")
        for tau in ts3:
            n3, n3a = N3_count(c, tau, eps)
            if n3 == 0: continue
            L = L_count(c, beta, tau, eps)
            show(f"  tau {tau:08x}  L {L}  N3 {n3}  N3_ruleA {n3a}")
            if L: rows.append((tau, eps, L, n3, n3a))
            tot += L * n3; totA += L * n3a
    return rows, tot, totA

def inst32():
    Y3, Y3B, Y11, Y11B = 0x8127c181, 0x7edf3e7e, 0x7af77f38, 0x850000c3   # Fact P
    W4, W4B = 0x97475638, 0x97475640
    Y4s = [((0x030c0303 | f) - Y3) & 0xffffffff for f in subs(~0x07ef8303 & 0xffffffff)]
    rule = [(0x00000001, 0), (0x00000002, 1), (0x00010000, 0), (0x00020000, 0),
            (0x00000404, 1), (0x00000808, 1), (0x01001008, 0), (0x02002040, 0)]   # rule A
    c = Inst(32, 16, 12, 8, 7, Y3, Y3B, Y11, Y11B, (W4 - W4B) & 0xffffffff, 0x830303cf, Y4s, rule)
    assert len(Y4s) == 131072 and all(ror(c, ((Y3 + y) ^ (Y3B + y)) & c.m, 16) == c.eta for y in Y4s)
    return c

def main32(beta):
    t0 = time.perf_counter()
    c = inst32()
    rows, tot, totA = beta_part(c, beta)
    print(f"beta {beta:08x}: {len(rows)} outcomes with L * N3 > 0")
    print("tau       eps       L                  N3                 L*N3/2^81  rule A")
    for tau, eps, L, n3, n3a in sorted(rows):
        q, rem = divmod(L * n3, 2**81)
        print(f"{tau:08x}  {eps:08x}  {L:<17}  {n3:<17}  {q:<9}{'' if rem == 0 else ' +rem'}  "
              f"{'all' if n3a == n3 else n3a}")
    q, rem = divmod(tot, 2**81); qA, remA = divmod(totA, 2**81)
    print(f"part = sum / 2^81 = {q} remainder {rem}; with rule A {qA} remainder {remA}")
    print(f"seconds {time.perf_counter() - t0:.1f}")
    return tot, totA

if __name__ == "__main__" and "--selftest" not in sys.argv:
    beta = int(sys.argv[sys.argv.index("--beta") + 1], 16) if "--beta" in sys.argv else 0x18b0e098
    tot, totA = main32(beta)
    if beta == 0x18b0e098:
        assert tot == 67698688 << 81 and totA == tot
        print("CHECK part of beta* = 67,698,688 = 1033 * 2^16, rule A keeps all of it")
```

Output of that run (the outcome table):

```text
beta 18b0e098: 7 outcomes with L * N3 > 0
tau       eps       L                  N3                 L*N3/2^81  rule A
175020a0  6e21be55  562949953421312    27021597764222976  6291456    all
185020a0  6e21be55  2251799813685248   18014398509481984  16777216   all
275020a0  6e21be55  562949953421312    4503599627370496   1048576    all
285020a0  6e21be55  2251799813685248   27021597764222976  25165824   all
385020a0  6e21be55  1125899906842624   36028797018963968  16777216   all
675020a0  6e21be55  140737488355328    1125899906842624   65536      all
685020a0  6e21be55  562949953421312    6755399441055744   1572864    all
part = sum / 2^81 = 67698688 remainder 0; with rule A 67698688 remainder 0
seconds 121.2
CHECK part of beta* = 67,698,688 = 1033 * 2^16, rule A keeps all of it
exit 0
```

**End of Section 17.**
