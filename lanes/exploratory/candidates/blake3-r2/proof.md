# A last-chunk half-collision, an outer filter and an exact E3 solver for 2-round BLAKE3, walked in seven lanes

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
separately reported resource bound.

**This package (v108).** It is winglock's entry dd91b2f6 (v107, time_log2
69.34520), kept as filed, with one change by leech1996: the walk over outer
steps (step 1 of 9.1) runs seven independent outer steps at once, one in each
36-bit lane of a 256-bit machine word, by the rules of Lemma L7 (9.2), and the
filter reads two tables of 2^32 entries that are built once, instead of four
bytes of each automaton. Every outer step is still one independent uniform draw
of the seven outer words and of y in the class. The filter's masks, the solver,
step 3, the pass units X, the premises H1' and H2'', RUN_OUTER_STEPS and
PASS_BUDGET are unchanged. The walk is charged 378 machine units per batch of
seven outer steps (54 per outer step) instead of 329 per outer step. The
passing-step bookkeeping that the change adds (the lane dispatch and the
extraction of the lane's words, 40 units) stays inside the bound of Lemma U.
Total charged time is below 2^67.8127726 units, the claimed scalar 67.81278
(Section 11). Where the text below says v107, it describes dd91b2f6. All of it
holds for v108 except where Sections 9.1, 9.2, 9.3, 11, 12, 15 and 16 say
otherwise.

This exploratory package (v107, winglock) targets blake3-r2-prefix-v1. It is
Jbenisek's entry 47804be2 (time_log2 75.42): the chunk-counter construction of
e7b17fd1 and its exact outer filter (Lemma F), with four changes that are ours
and are listed in Section 15:

1. **Y4 in the whole class, no rule A.** The member y runs over the 2^19 members
   of the class of eta (Lemma Q), not over the sub-class of 2^17, and rule A is
   not used. The count of Section 17, run on the class, gives beta* the part
   71,698,432 from fourteen outcomes (10.1); on the sub-class it is 67,698,688
   from seven. The organizer experiments still run the root instance on the
   sub-class, as filed.
2. **An exact E3 solver in place of the cube enumeration.** A passing outer step
   fixes Y4, Y9 and omega = Y3 + Y4 + w8, and E3 of both messages depends on
   these and on E3.h1 alone. A depth-first walk over the bits of E3.f1, pruned
   by the joint alive sets of the two carry automata of the filter, returns every
   E3.h1 for which E3 of both messages has the differences of an outcome
   (Lemma E3); Lemma IP turns each into its c1, and only those whose c1 is in Q*
   are trials. So a passing outer step costs about 15,500 machine units on
   average (13.5) instead of 12,957,444 (Section 9). A step whose solver work passes a
   cap falls back to the enumeration of all of Q* (Lemma SC).
3. **Margin 1.400** on the model-count factor instead of 2.000, the choice of
   GordoAR (entries 3f8e4e89 and 6a600434, both plausible_not_refuted),
   disclosed in 10.3 with the evidence against it that we know of.
4. **Accounting.** The walked outer step and the filter are counted on a machine
   with 64 registers whose constants are instruction fields (294 and 32 machine
   units), and the loop adds 3. The solver is charged per itemized event; the
   program's count of the solver primitive by primitive gives exactly those
   units plus the machine's own bookkeeping, which is at most 1/15 of them
   (Lemma U, 9.2). The pass units have a budget set 1/6000 above a premise
   (leech1996's convention) that a preregistered sample of single outer steps
   measured (13.5; Subflatus3's design of single uniform units), and are charged
   at 16/15 of the budget plus one step's maximum. The selection procedure is
   steps 1 and 2 of that of 47804be2, because the sub-class, rule A and the
   ranking of betas are no longer selected (Section 12).

**Exact part.** An explicit construction maps seven 32-bit words, a member y of
the class and one more word c1 to a number t and to a 55-byte string A and a
63-byte string B. When t is not zero, F || A and F || B, with F a string of t
full chunks of 1,024 bytes, are messages of 1024 t + 55 and 1024 t + 63 bytes
whose last chunks are A and B, and the 2-round compressions of these last
chunks, with chunk counter t and flags 3, give chaining values that agree on
their words 0, 2, 5 and 7 (Theorem C). In the organizer's tree mode the digest
of such a message depends on F and on the chaining value of its last chunk alone
(Lemma TR). For every outer step that fails the filter no trial has R = 0 with
an outcome of the list (Lemma F); for every passing outer step and outcome the
solver returns exactly the words E3.h1 for which E3 of both messages has that
outcome's differences (Lemma E3); a returned word gives a trial with R = 0 if and
only if its c1 is in Q*, its t is not zero and E1 of both messages has the same
outcome's differences (Lemma G). So the search finds every listed good trial of
every outer step it walks, unless a budget halts it first.

**Heuristic part.** A collision needs the remaining 128 bits of the chaining
value to agree. The algorithm draws 767,186,645,459,980,621,344 = 2^69.378
outer steps at random. Two heuristics are declared: H1', that the valid trials
of an outer step are listed good trials at a rate of at least 104,884,563,382 *
2^-128 each, the model's rate 2^11 * 71,698,432 * 2^-128 divided by 1.4, with
the successes of one outer step weakly dependent (the premise of e7b17fd1 and
47804be2 with the class and margin 1.4); and H2'', that the mean of the pass
units X of one uniform outer step (the solver's charged machine units, 9.2) is
at most 1369/16 = 85.5625, the premise that the preregistered sample sets (13.5).
Under the two the search succeeds with probability at least 0.39. Total charged
time is below 2^67.8127726 target-compression units, the claimed scalar 67.81278
(v108; v107 is charged 2^69.3451998).

The rate in H1' is an assumption: an exact count under the seven-word model,
taken at 1/1.4. Real trials of the counter construction have been compared with
the model on partial events by Jbenisek (Section 13, inherited) and by us: the E3
side of a success, in full, on 2^35 real outer steps (13.5), and the E1 side on
real trials (13.6). No run reaches a collision at 32 bits, and none was computed.
The two declared experiments run the root instance (counter 0, flags 11), as in
47804be2: no digest experiment can show a half-collision of a non-root chunk's
chaining value (6.4). They check the shared construction, not the counter
instance, the filter, the solver or any rate.

*How to read the inherited text.* Sections 1 to 7 and 14 are Jbenisek's text
from 47804be2, kept with the edits that v107 needs (the class in Section 8, the
observation of `residual-search` in 6.4, Section 6.5 replaced). Where that text
cites Sections 9, 10.1 or 13, or speaks of the sub-class, rule A or the
root-instance batch, it cites 47804be2's sections, which describe them; rule A,
Lemma A and the batch are not used by v107. In this text Sections 8.3 to 13 and 15
to 16 describe v107; "we" there is winglock, and "our entry" in Section 14 is
Jbenisek's.

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

## 6. The root instance: trials, tests and the experiments

**6.1 Trials.** A *context* is the six words of an outer step (C0.c1, C0.d1,
D3.d1, S15, S9, w5), a word X2, and everything that steps O and M compute from
them. The class and the sub-class defined next are sets of values of Y4. A
**trial** is a context and a member y of the sub-class; its messages A and B
are the output of steps O, M, Y, T, S2 and S3 for the context's seven words and
y. Only steps Y and T depend on y: the trials of one context differ in the four
message words w8..w11 and in nothing else of the message (Lemma T2 (c)). Step Y
does not depend on X2: for one outer step and one member its ten names are the
same for all 2^32 values of X2.

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

*The sub-class.* The root instance's experiments use only the members of the class whose e1 = Y3 +
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
here on, in this section and in the root instance of the experiments, "member"
means a member of the sub-class, as 47804be2 filed it: a part of the class was
searched there because, under the model, the rate of collisions differs from
member to member and was taken to be higher on this part. For the beta* of the
counter search that is not so (the class has 1.059 times the count of the
sub-class, 10.1), and Sections 8 to 12 use the whole class. Nothing exact
depends on that.

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
of its trials has a zero residual. How much it loses was answered in 47804be2's
Section 13 (its records, not reproduced in this package): inside the sub-class
the rule keeps all but 19,086.08 of the 185,377,197.55 counted there, and for
the difference beta* it keeps all of it, 67,698,688 of 67,698,688, because in
every outcome of beta* in the sub-class every solution satisfies rule A. On the
whole class the same eight conditions keep 33,849,344 of 71,698,432 (Section
17); the rule is a rule for the sub-class only, and v107 does not use it.

**6.4 The root instance and the two declared experiments.** Sections 4 to 6
build the *root instance* of the construction: its messages are single chunks
of 55 and 63 bytes, and the colliding compression is the root compression, with
counter 0 and flags 11 (Section 1). The claim of this package is made for the
*counter instance* of Sections 7 to 9, whose messages have 1024 t + 55 and 1024
t + 63 bytes and whose colliding compression is that of the last chunk, with
counter t and flags 3. The two instances share the six constants, Fact P,
Lemmas L and H, the class, Lemma N and the model; they differ in the counter and the flags that the compression
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
  in digest word 1. It returns the number of members tried as its only
  observation (v107; 47804be2 also returned the counts of its root batch).

Neither experiment runs the counter construction, the filter or the solver, and
neither measures a rate of the counter search. A search of the root instance over all
contexts is not part of the claim, and this text defines no loops, ranges or
budgets for it.


**6.5 The packed batch of 47804be2 (not in v107).** Entry 47804be2 had here a
packed word of seven 36-bit lanes with a masked rotation (tekkac's layout, ticket
2bf40fb), the counted root-instance batch on a 16-register machine, its
operation tables and its self-test, and its counter batch with rule A was built
on them. The v107 program contains none of these: its search has no cube
enumeration (8.4) and does not use rule A, and the declared experiments do not
return the batch's counts. Lemma A (c) and (d) above speak of such lanes; they
are kept as inherited text and nothing in v107 uses them. Rule A and Lemma A are
not used by the v107 search; Lemma N is (8.4).

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


## 8. The counter construction, the outer filter and the E3 solver

*Words and constants.* The construction has nine free words: the seven *outer
words* C0.d1, D2.a1, D2.b1, S11, S4, X9 and w6 (the program's `CTR_BASIS`); a
member y of the class of 6.1 (v107: the whole class, 2^19 members; 47804be2 used
the sub-class), which becomes the value of Y4; and the *inner
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
outer words, of a member y of the class and of a word c1, steps CO and CT
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


**8.3 The outer filter (Jbenisek, 47804be2; fourteen outcomes in v107).** Number
the fourteen outcomes of beta* in the class (10.1) j = 0 to 13 in the order of
the program's `CTR_TAUS` (the order of the table of 10.1), and let tau_j be the
tau of outcome j, sigma_j = tau_j XOR ROR(tau_j, 1) and theta_j = ROL(sigma_j,
12); all fourteen have eps = 6e21be55. For an outer step put omega = Y3 + y + w8,
with Y3 of Fact P, y the member of the outer step and w8 the name of step CO;
DY3 = Y3' - Y3 = fdb77cfd is that of Section 6. For a word x:

- condition (1)_j holds for x when some word h gives
  (x + h) XOR (x + (h XOR eta)) = theta_j;
- condition (2)_j holds for x when some word f gives
  (x + f) XOR ((x + DY3) + (f XOR sigma_j)) = eps.

An outer step *passes* the filter when for some j both (1)_j holds for its Y9
and (2)_j holds for its omega; its *mask* is the set of these j. Y9 and w8 are
names of step CO and y is drawn with the outer words, so the mask depends on the
outer step alone and on no c1.

**Lemma F (the outer filter; GPT Sol, answer AC to Jbenisek, for 47804be2).** Fix
an outer step and an outcome j that is not in its mask. Then no trial of the
outer step, for any word c1, has R = 0 with E1 outcome j.

Proof (47804be2, Section 8, with "seven" read as "fourteen"; nothing in it uses
the number of outcomes, the sub-class or rule A). Take a trial with R = 0 whose
E1 outcome is outcome j. Write h, g, f and e2 for E3.h1, E3.g1, E3.f1 and E3.e2
in the compression of A, and h', g', f' and e2' for the same values in that of
B. Y9 and w8 are the same in both compressions: w8 is a line of step CO and a
word of both blocks, and Y9 is an output of C1, which reads words of the state X,
the same for A and B (proof of Theorem C), and the message words w3 and w10,
which the two blocks share. Both compressions have Y4 = y and h' = h XOR eta
(Theorem C (iii)), and the a input of E3 is Y3 for A and Y3' for B (Fact P). The
conditions of R = 0 (Lemma D of 8.4 below) give that the
XOR difference of E3's first-half b values is sigma_j and that of its a outputs
is eps. Now g = Y9 + h and g' = Y9 + (h XOR eta); f = ROR(y XOR g, 12) and
f' = ROR(y XOR g', 12), so f XOR f' = ROR(g XOR g', 12) = sigma_j gives g XOR
g' = theta_j, and h witnesses (1)_j for Y9. With w15 = 0, e2 = Y3 + y + f + w8 =
omega + f and e2' = Y3' + y + f' + w8 = (omega + DY3) + (f XOR sigma_j), and e2
XOR e2' = eps, so f witnesses (2)_j for omega. So j is in the mask, against the
hypothesis. QED.

The lemma uses no law of the words: no uniformity, no independence and no
relation between h and f besides the two equations. The filter can pass outer
steps that hold no success, since (1)_j and (2)_j are solved with separate
witnesses; it cannot drop an outcome that a success of the outer step has.

**The exact share of passing pairs (recounted for the fourteen outcomes).** Let
pi be the share of the 2^64 pairs (x1, x2) of words such that for some j
condition (1)_j holds for x1 and (2)_j for x2. Then

    pi = 99,669,577,442,459,648 / 2^64,

about 0.0054031 = 2^-7.531997 (the program's `CTR_SHARE`). *Method* (47804be2):
whether (1)_j holds for x is decided bit by bit from bit 0 upwards by a subset
construction over the carry pairs that some prefix of a witness reaches; for (2)_j
the carry of x + DY3 is carried as well. The fourteen sets are carried together
over the bits of x, so one pass gives the mask of x; equal states add their counts
of prefixes of x, and witnesses are never counted. A pair passes exactly when the
mask of x1 under (1) and the mask of x2 under (2) intersect. *Certificate* (from
the program's own tables, `ctr_tables`, whose construction is that of 47804be2
with the fourteen tau): 4,020,823,552 words have mask 0 under (1) and
3,624,192,256 under (2); 274,143,744 words satisfy some (1)_j (36 nonzero masks,
counts multiples of 512) and 670,775,040 some (2)_j (72 nonzero masks, counts
multiples of 416); the sum over intersecting masks of the products of the
counts is 99,669,577,442,459,648. Per outcome (words with (1)_j, words with
(2)_j, pairs with both):

| tau | (1)_j | (2)_j | pairs |
| --- | ---: | ---: | ---: |
| 175020a0 | 14,110,208 | 86,561,280 | 1,221,397,665,546,240 |
| 175060a0 | 28,220,416 | 171,991,040 | 4,853,658,697,072,640 |
| 185020a0 | 56,440,832 | 190,434,816 | 10,748,299,456,806,912 |
| 185060a0 | 112,881,664 | 378,380,288 | 42,712,196,534,239,232 |
| 275020a0 | 14,110,208 | 86,561,280 | 1,221,397,665,546,240 |
| 275060a0 | 28,220,416 | 171,991,040 | 4,853,658,697,072,640 |
| 285020a0 | 14,110,208 | 47,608,704 | 671,768,716,050,432 |
| 285060a0 | 28,220,416 | 94,595,072 | 2,669,512,283,389,952 |
| 385020a0 | 56,440,832 | 142,826,112 | 8,061,224,592,605,184 |
| 385060a0 | 112,881,664 | 283,785,216 | 32,034,147,400,679,424 |
| 675020a0 | 27,998,208 | 86,561,280 | 2,423,560,722,186,240 |
| 675060a0 | 55,996,416 | 171,991,040 | 9,630,881,824,112,640 |
| 685020a0 | 27,998,208 | 47,608,704 | 1,332,958,397,202,432 |
| 685060a0 | 55,996,416 | 94,595,072 | 5,296,985,003,261,952 |

The seven rows with tau ending in 5020a0 are those of the certificate of
47804be2, digit for digit. The self-test (9.3) recounts the share from the
program's tables and checks the automata against brute force at 10 bits. The
tables have 1, 18, 43, 37 and 1, 3, 19, 19 states at the four byte boundaries.

**8.4 The exact E3 solver (new in v107).** Fix an outer step and an outcome j of
its mask. The step fixes y = Y4, Y9 and omega; E3 of message A is
G(Y3, y, Y9, Y14; 0, w8) and of B is G(Y3', y, Y9, Y14; 0, w8), so with h =
E3.h1 = ROR(Y14 XOR (Y3 + y), 16) all first-half values and outputs of E3 of
both messages are functions of h and of (y, Y9, omega):

    g = Y9 + h,  f = ROR(y XOR g, 12),  e2 = omega + f,  h2 = ROR(h XOR e2, 8),  g2 = g + h2,
    h' = h XOR eta,  g' = Y9 + h',  f' = ROR(y XOR g', 12),  e2' = (omega + DY3) + f',
    h2' = ROR(h' XOR e2', 8),  g2' = g' + h2'.

(h' = h XOR eta for every member of the class, Theorem C (iii).) Call h
*E3-good for j* when g XOR g' = theta_j, e2 XOR e2' = eps and g2 XOR g2' = tau_j
(the program's `ctr_e3`). By the proof of Lemma F (the conditions on theta_j and
eps) and by Lemma D (D1 = 0 gives g2 XOR g2' = a2 XOR a2' = tau_j), a trial of
the outer step with R = 0 and E1 outcome j has an E3-good h for j; conversely the residual of a trial
whose h is E3-good for j and whose E1 has the differences (beta*, tau_j, eps) is
zero (Lemma G).

*The two automata on the bits of f.* For every f there is exactly one h with
f = ROR(y XOR (Y9 + h), 12), namely h = (ROL(f, 12) XOR y) - Y9. Write the
condition g XOR g' = theta_j as an automaton A on the bits i of g = ROL(f, 12)
XOR y, from bit 0 up: its state is the borrow of g - Y9 (which gives the bits of
h) and the carry of Y9 + (h XOR eta), and the bit i of g is accepted when the bit
i of Y9 + (h XOR eta) equals g_i XOR theta_j,i. Write e2 XOR e2' = eps, with f'
= f XOR sigma_j (which g XOR g' = theta_j gives), as the automaton B on the bits
k of f from bit 0 up: its state is the carries of omega + f and (omega + DY3) +
(f XOR sigma_j), and the bit k is accepted when the two sum bits differ by
eps_k. Bit k of f is bit i = k + 12 mod 32 of g XOR y. So the bits k = 0..19 of
f are the bits i = 12..31 of g (the *top run* of A) and the bits k = 20..31 are
the bits i = 0..11 (the *low run*, which starts at bit 0 in the state (0, 0) and
must end, after bit 11, in the state in which the top run started).

**Lemma E3 (the solver is exact).** For a guess s of the state of A at bit 12,
let W_s be the depth-first walk of the program's `ctr_solve`: from the root (k
= 0, B in state 0, A in state s) a node (k, prefix f_0..f_{k-1}, B state, A
state) has the children f_k = 1 and f_k = 0 whose transitions of B at bit k and
of A at bit i = k + 12 mod 32 (the A state set to (0, 0) after k = 19) lead to a
pair of states in the joint alive set J_{k+1}; J_32 is the set of pairs whose A
state is s, and J_k (k < 32) is the set of pairs from which some value of bit k
leads into J_{k+1}. A node with k = 32 is a leaf; at a leaf the program forms h =
(ROL(f, 12) XOR y) - Y9 and keeps it when `ctr_e3` holds. Then the union over
s = 0..3 of the kept words is exactly the set of words h that are E3-good for j,
each kept once.

Proof. *Every kept word is E3-good:* `ctr_e3` is the definition. *Every E3-good h
is kept once:* let f = ROR(y XOR (Y9 + h), 12) and let s be the state of A at bit
12 when A runs on g = Y9 + h from bit 0; s is unique. Since g XOR g' = theta_j, A
accepts every bit of g; since e2 XOR e2' = eps with f' = f XOR sigma_j, B accepts
every bit of f. So along the bits of f, run as in the walk with the guess s, the
pair of states at every k is defined, and from it the remaining bits of f lead to
J_32 (the low run ends in s): by induction from k = 32 down, every pair on this
path is in J_k. So the walk with guess s visits every prefix of f, reaches the
leaf f and keeps h. With another guess s' the low run of A on the bits 0..11 of g
ends in s, not s', so the path leaves J at k = 32 and f is not a leaf of W_s'.
Every leaf is a distinct f, and f -> h is one to one. QED.

The alive sets only prune: they remove prefixes that cannot reach a leaf, so they
change the number of nodes and not the set of leaves. The walk visits only
prefixes that some leaf extends; the self-test compares its output with a second
enumeration that walks automaton B alone and tests every complete f with
`ctr_e3` (9.3), and with 28 planted solutions.

*Bounds.* By Lemma S5 (GPT Sol 6.1 for e7b17fd1), every bit k < 31 of f at which
sigma_j and eps differ is fixed by the lower bits of f, and every bit i < 31 of h
at which eta and theta_j differ is fixed by the lower bits of h, hence (for i <
12) bit i + 20 of f by the bits 20..i + 19 of f. So at most 2^(32 - n_j) words h
are E3-good for j, with n_j the number of bits of ((sigma_j XOR eps) AND
7fffffff) OR (((eta XOR theta_j) AND fff) << 20); summed over the fourteen
outcomes this is 286,720 (`ctr_goods_max`). The walk has at most 33 nodes per
leaf and at most 2^(32 - n'_j) leaves, n'_j the bits of (sigma_j XOR eps) AND
7fffffff alone.

**Lemma SC (the cap and the fallback scan).** If the solver's units in a passing
outer step pass CTR_STEP_CAP = 2^23, the program stops the call at hand and runs
`ctr_scan` for the outcomes of the mask from that one on: for every member c1 of
Q* it computes E3.h1 of the trial (the lines of step CT for E1.d1, E1.a1, Y6,
Y10, Y14 and E3.h1) and keeps (h, j) when h is E3-good for j. Then the kept
pairs with c1 in Q* are exactly the pairs that the solver would have returned for
those outcomes with c1 in Q*. Proof: c1 -> E3.h1 is a permutation for a fixed
outer step (Lemma IP), so the scan visits every h whose c1 is in Q*, and
`ctr_e3` decides each. QED. The scan returns only words whose c1 is in Q*; the
solver also returns words whose c1 is outside Q*, which step 3 of 9.1 drops.

**Lemma D (the residual words; winglock, from Lemma N of c66f230d).** For a trial
write (a1, d1, c1, b1, a2, d2, c2, b2) for E1 and (e1, h1, g1, f1, e2, h2, g2,
f2) for E3 on message A, primes for B. Z1, Z12, Z11, Z6 are E1's a2, d2, c2, b2
and Z3, Z14, Z9, Z4 are E3's e2, h2, g2, f2, so the XOR differences of words 1,
3, 4 and 6 of the two chaining values are D1 = (a2 XOR a2') XOR (g2 XOR g2'), D3
= (e2 XOR e2') XOR (c2 XOR c2'), D4 = ROR(f1 XOR f1' XOR g2 XOR g2', 7) XOR (d2
XOR d2') and D6 = ROR(b1 XOR b1' XOR c2 XOR c2', 7) XOR (h2 XOR h2'), and R = 0
exactly when all four are 0. Proof: the output assignments of G and o[i] = Z[i]
XOR Z[i + 8]; f2 = ROR(f1 XOR g2, 7) and b2 = ROR(b1 XOR c2, 7), and ROR
distributes over XOR. QED. In E1, d1 is shared, so d2 XOR d2' = ROR(a2 XOR a2',
8).

**Lemma G (deciding R = 0).** Let h be E3-good for j in an outer step, c1 its
word by Lemma IP and suppose c1 is in Q* and t != 0. Then the trial of c1 has R =
0 if and only if E1 of the two messages has the differences beta*, tau_j and eps
of its first-half b values, a outputs and c outputs. Proof. By Lemma D,
R = 0 exactly when D1 = D3 = D4 = D6 = 0, and with d1 shared these are: a2 XOR
a2' = g2 XOR g2', c2 XOR c2' = e2 XOR e2', f1 XOR f1' XOR g2 XOR g2' = ROL(ROR(a2
XOR a2', 8), 7) and ROR(b1 XOR b1' XOR c2 XOR c2', 7) = h2 XOR h2'. If E1 has
(beta*, tau_j, eps) and h is E3-good for j, then g2 XOR g2' = tau_j, e2 XOR e2' =
eps, f1 XOR f1' = sigma_j = tau_j XOR ROR(tau_j, 1) and h2 XOR h2' = ROR(eta XOR
eps, 8) = ROR(beta* XOR eps, 7) (Lemma N with n = 0 for these constants, checked
in the program), so the four hold. Conversely R = 0 forces the first two to give
E1's differences tau_j and eps, and beta* holds because c1 is in Q* (Theorem C
(iv)). QED. The program's `ctr_good` forms c1 by Lemma IP, tests Q*, computes t
and E1 of both messages (the program's G) and compares; the self-test checks its
E1 differences against those of the two real compressions on every trial.

## 9. The counter search

**9.1 The algorithm.** The search uses these constants of the submitted program
(experiments/halfsearch.py): `CTR_MEMBERS` = 2^21, the members of Q*; `CTR_CSIZE`
= 2^19, the members of the class; `CTR_TAUS`, `CTR_EPS` and `CTR_PARTS`, the
fourteen outcomes of 10.1 and their parts; `CTR_FACTOR` = floor(2^11 *
71,698,432 * 5 / 7) = 104,884,563,382, the factor of H1' (10.3); `LAMBDA` =
495,910 / 10^6; `RUN_OUTER_STEPS` = ceil(LAMBDA * 2^128 / (CTR_FACTOR * (2^21 -
1))) = 767,186,645,459,980,621,344, about 2^69.378; `CTR_SHARE` =
99,669,577,442,459,648 (8.3); `CTR_STEP_CAP` = 2^23 and `SCAN_UNITS` = 2^21 *
192 (Lemma SC); `PASS_PREMISE` = 1369/16 = 85.5625, the premise of H2'' (10.3), and
`PASS_BUDGET` = ceil(RUN_OUTER_STEPS * PASS_PREMISE * 6001 / 6000) =
65,653,347,753,394,953,512,399, about 2^75.7973; `LOOP_UNITS` = 3,
`PASS_SCALE` = 16/15 and `X_MAX` = 447,764,408, the largest X of one outer step
(9.2, Lemma U).

0. Before the outer steps, build once: the two automata of the filter (8.3;
   `ctr_tables`), the two mask tables T1 and T2 of 9.2 (v108, 2^32 entries each,
   in place of v107's member table; `ctr_table`), the
   transition tables of the automata A and B and the two joint alive tables of
   9.2 (`CTR_TB`, `CTR_TA`, `ctr_jt`), and the table of the 2^21 members of Q*
   for the scan (`ctr_c1`).
1. (v108) RUN_OUTER_STEPS = 7 * 109,598,092,208,568,660,192 is divisible by
   seven. For each of the RUN_OUTER_STEPS / 7 batches in turn (a count,
   decremented, compared and branched on: 3 machine units): draw eight fresh
   uniform 256-bit words R0 to R7. Outer step i of the batch (i = 0 to 6) has
   as its outer words C0.d1, D2.a1, D2.b1, S11, S4, X9 and w6 the bits 36i to
   36i + 31 of R0 to R6. Its e1 = Y3 + y is (bits 36i to 36i + 31 of R7) AND NOT
   CTR_CLASS, OR (CLASS_VALUE AND CTR_CLASS). So y = e1 - Y3 is uniform in the
   class, the seven outer words are uniform, and all of them are independent,
   within the batch and across batches. Run step CO on the seven lanes at once
   (`ctr_batch`, Lemma L7). *Filter:* compute omega = e1 + w8 in the lanes; for
   each lane i put z_i = T1[Y9_i] AND T2[omega_i], with Y9_i and omega_i the
   words of lane i; z_i is the mask that v107's automata give for outer step i.
   If the OR of the seven z_i is zero, go on with the next batch. Otherwise each
   lane i with z_i != 0, in lane order, is a passing outer step with mask z_i,
   done by step 2. The other lanes are skipped.
2. Otherwise the outer step *passes* (`ctr_step`): for each outcome j of the mask,
   in increasing order, run the solver of 8.4 (`ctr_solve`) and collect its
   words h. First store the ten words of the step that step 3 reads (v108: after
   the lane's y, Y9, omega and these ten words are extracted from the batch's lane
   words, 9.2). The solver's
   machine units of the step (9.2) are kept in a register u as it runs, and
   before every pop u is compared with CTR_STEP_CAP; when u exceeds it, the call
   is stopped and the scan of Lemma SC (`ctr_scan`) does the outcomes of the mask
   from j on. Add the pass units X of the step (the dispatch over the mask, u,
   and if the scan ran SCAN_UNITS and 128 for each word it returned) to the run's
   count of pass units; halt with failure when the count exceeds PASS_BUDGET.
3. For every collected (h, j) (`ctr_good`): c1 from h by Lemma IP; drop it unless
   c1 is in Q*; compute t by step CT and drop it if t = 0; compute E1 of both
   messages and, if its differences are (beta*, tau_j, eps), R = 0 (Lemma G):
   form F || A and F || B by step CS, evaluate blake3 of both in full, check that
   the two digests agree, output the pair and halt.
4. After the last outer step, halt with failure.

The run halts with failure in exactly two ways, each a test on a count that the
algorithm keeps: the pass units exceed PASS_BUDGET, or the outer steps are
exhausted. So the work of every run is bounded by the counts of Section 11.

A trial (an outer step and a c1 in Q*) is *valid* when its t is not zero; a valid
trial with R = 0 is *good*; a good trial is *listed* when its E1 outcome is one of
the fourteen. A listed good trial is found unless the pass budget halts the run
before it is reached: its outer step passes the filter with its outcome j in the
mask (Lemma F); its E3.h1 is E3-good for j (8.4: the proof of Lemma F and Lemma
D); the solver
returns it (Lemma E3), or the scan does if the cap was passed (Lemma SC); its c1
is in Q* and t != 0 because it is a valid trial, and E1 has outcome j, so step 3
outputs it (Lemma G). Rule A is not used: a listed good trial need not satisfy
it. When the run outputs a pair, the pair is a collision of two complete
messages: step 3 has checked both digests, and Lemma TR (c) says that R = 0
with the half-collision of Theorem C gives equal digests.

*What the submitted program holds of this.* Steps CO and CT (`ctr_outer`,
`ctr_trial`), the filter (`ctr_tables`, `ctr_look`, `ctr_filter`), the solver
(`ctr_solve`, `ctr_jt`), the scan (`ctr_scan`), a passing step (`ctr_step`),
step 3 up to the decision R = 0 (`ctr_good`), the walk (`ctr_run`, with the pass
budget as a halt), the counted batch and filter (v108: `LW`, `ctr_batch`,
`ctr_table`, `ctr_count`), the per-event
units of the solver (`SOLVER_UNITS`), the solver with its bookkeeping, step 3 and
a scan member on the counting machine (`ctr_solve_counted`, `ctr_good_counted`,
`ctr_scan_counted`), the ledger of Section 11 (`ctr_time`, `ctr_ledger`) and
the self-test (`ctr_selftest`). The bound RUN_OUTER_STEPS (step 4) and the final
step (building the messages of a found pair) are defined by this text; the program
holds RUN_OUTER_STEPS as a constant.

**9.2 The machine and the counts.** One unit is charged for every executed
primitive: an addition, subtraction, XOR, AND, OR or shift of a 256-bit word, a
comparison, a branch, a load, a store and a random 256-bit word. Shift distances,
constant operands and the base addresses of tables are instruction fields; there
are 64 registers. (Entry 47804be2 charged one load for every constant operand on
a machine with 16 registers; the 64-register convention with immediates is that of
our entries ef052659 and d598fe29 and of Subflatus3's 5ca02dfb, all
plausible_not_refuted. Section 11 also gives the total under 47804be2's
convention.)

*Counted by the program (v108).* `ctr_count` runs one batch of seven outer steps
with every value a counted word (`Word`, `Cnt`, and the lane words `LW`, whose
operations count their primitives). The batch part is 319: the eight random
words (8), the seven outer words masked to their lanes (7), e1 (2: an AND and an
OR), y = e1 - Y3 (1), and step CO, as `ctr_outer` writes it, evaluated on lane
words by the rules of Lemma L7 (301). The filter is 56: omega = e1 + w8 (1); the
extraction of Y9_i and omega_i from the lanes, a shift and an AND each (one AND
for lane 0), 26; the two table loads per lane, 14; the AND of each pair, 7; the
OR of the seven, 6; and the comparison with zero and the branch, 2. These are
straight-line code, so their counts do not depend on the words. The self-test
finds 319 and 56 on all of its 16 counted batches, eight of them with lanes that
hold the words 0 and ffffffff. At most 32 registers are live (the count's peak,
plus two for the temporaries of a rotation). The loop of step 1 adds 3 (a count,
its decrement, a compare and a branch). So the walk is charged 378 per batch, 54
per outer step. (v107 counted 294 for one outer step and 32 for its filter on a
scalar machine word, plus the loop: 329 per outer step.)

**Lemma L7 (seven lanes; leech1996).** A lane word is a 256-bit word read as
seven lanes of 36 bits, lane i being bits 36i to 36i + 35; bits 252 to 255 are
zero. Every lane word of a batch carries two numbers lo <= hi < 2^36, and the
invariant is: lane i lies in [lo, hi] and is congruent modulo 2^32 to the value of
the same name in outer step i, as step CO computes it with 32-bit words. Write c
for a 32-bit constant, rep(c) for its copy in every lane and M = rep(ffffffff).
The rules of `LW` are these.

- An outer word is R AND M (1 unit, bounds [0, ffffffff]). e1 is (R AND
  rep(NOT CTR_CLASS)) OR rep(CLASS_VALUE AND CTR_CLASS) (2 units).
- a + b is one addition when hi_a + hi_b < 2^36. Otherwise each operand whose
  hi exceeds ffffffff is first reduced by an AND with M (1 unit each, new bounds
  [0, ffffffff]). a + c is one addition of rep(c), with the same reduction of a
  when hi_a + c would reach 2^36.
- a - c is one subtraction of rep(c) if lo_a >= c, and otherwise one addition
  of rep(2^32 - c).
- a - b is one subtraction if lo_a >= hi_b. Otherwise b is first reduced if its
  hi reaches 2^34, k = max(33, bit length of hi_b), a is reduced if hi_a + 2^k
  would reach 2^36, and the result is (a OR rep(2^k)) - b, two units, with bounds
  [2^k - hi_b, hi_a + 2^k - lo_b]. c - b is rep(c + 2^k) - b, one unit, with
  bounds [c + 2^k - hi_b, c + 2^k - lo_b].
- a XOR b and a XOR c are one unit, with bounds [0, 2^L - 1], where L is the
  larger bit length (at least 32).
- ROL(a, r) is ((a AND rep(2^(32 - r) - 1)) << r) OR ((a >> (32 - r)) AND
  rep(2^r - 1)): five units, with bounds [0, ffffffff]. ROR(a, r) = ROL(a, 32 -
  r).
- The AND with ffffffff that the scalar lines apply after an addition or a
  subtraction is not executed.

Every rule checks hi < 2^36 when it makes a word; the program raises an error
otherwise, and none is raised. The rule chosen and the bounds depend only on the
lines and on the starting bounds ([0, ffffffff] for an outer word, [CLASS_VALUE
AND CTR_CLASS, ffffffff] for e1), never on the words. So a batch executes the
same operations with the same bounds for every choice of R0 to R7, and the checks
made on one batch hold for all of them. A lane of a batch is read only by
extraction, (W >> 36i) AND ffffffff.

*Proof.* By induction over the lines of step CO, each rule keeps the invariant.

- Addition: the lanes stay below 2^36 by the bound, so no carry leaves a lane.
  Each lane is the sum of the operands' lanes, which is congruent to the 32-bit
  sum.
- Subtraction: in every case the minuend's lane is at least the subtrahend's
  lane, so no borrow leaves a lane. The OR sets bit k >= 33, which changes no
  residue modulo 2^32 and makes the lane at least 2^k > hi_b. So the difference
  is congruent to the 32-bit difference, and the bounds follow.
- XOR acts bit by bit.
- Rotation: the first AND keeps bits 0 to 31 - r of each lane, and the shift
  moves them to bits r to 31 of the same lane. The right shift moves bits 32 - r
  to 31 of each lane to bits 0 to r - 1, the lane's bits 32 to 35 to bits r to
  r + 3, and bits of the next lane to bit r + 4 or above; the second AND keeps
  bits 0 to r - 1 only. So each lane is the 32-bit rotation of its value modulo
  2^32.
- Extraction returns the lane modulo 2^32, which is the outer step's value.

QED. The self-test compares every name of step CO, in every lane, with the scalar
`ctr_outer` on 16 batches.

*The mask tables.* T1[x] and T2[x] are, for each of the 2^32 words x, the masks
that the automata of conditions (1) and (2) of 8.3 give on x (one machine word per
entry). So z_i = T1[Y9_i] AND T2[omega_i] is the mask that v107's filter
(`ctr_filter`) computes for outer step i, with omega_i = e1_i + w8_i = Y3 + y_i +
w8_i modulo 2^32. The tables are built once (Section 11). The program computes an
entry from the byte tables when it is first read (`ctr_table`), and the self-test
compares the batch's seven masks with `ctr_filter` on every lane of its 16
counted batches.

*The solver, charged per event* (`SOLVER_UNITS`, itemized; each item is a
sequence of the machine's primitives that the walk of 8.4 executes, and the
program counts the events):

| Event | Machine units | What it executes |
| --- | ---: | --- |
| call | 546 | omega + DY3 reduced (2); for each k < 32 the key of B (bit k of omega and of omega + DY3, two shifts and ANDs, a shift, two ORs with the constant bits of sigma_j and eps: 7), the key of A at bit i = k + 12 (7), their join (2) and its store (1) |
| guess (four per call) | 199 | the start set J_32 (2); for each k the table index from the key and J_{k+1} (3), the load of the joint alive table (1), its store (1) and the extraction of J_k (1); the root test, J_0's bit of the guess (3), compare and branch (2) |
| root | 5 | the root word, its store and the stack count (3); the last loop test when the stack is empty (2) |
| pop | 13 | load (1), stack count (1), loop test (2), unpacking k, the two states and f (7), leaf test (2) |
| internal node | 14 | i = k + 12 mod 32 (2), the key and its two halves (3), the joint set of k + 1 and its 64-bit form (2), the reset mask of k (1), the bases of the two transitions (6) |
| child (two per node) | 11 | the two transition indices and loads (4), the reset AND (1), the joint index (2), its test (2), compare and branch (2) |
| push | 11 | f with the bit (2), k + 1 shifted (2), the two states shifted (2), three ORs (3), store (1), stack count (1) |
| leaf | 49 | h = (ROL(f, 12) XOR y) - Y9 (7); E3 of both messages to g2 and g2' (33); three differences against theta_j, eps and tau_j with compares and branches (9) |
| good word (step 3) | 128 | at most 96 counted (`ctr_good_counted`): Lemma IP back to c1, which gives E1's a1, d1 and c1 on the way; the test of Q*; the lines of step CT for t and its test; E1 of both messages from there; the three differences, each compared |

The dispatch of a passing step is 56 (a shift, an AND, a compare and a branch for
each of the fourteen bits of the mask). The units of a passing step are its pass
units X: 56, plus the sum over its calls of the units of the table, plus, if the
scan ran, SCAN_UNITS = 2^21 * 192 (a member counted at most 100 by
`ctr_scan_counted`: c1 from the table of Q*, step CT to E3.h1, E3 of both
messages, the difference eps first because all outcomes share it, then tau_j of
each outcome and, for the one that matches, its mask bit and theta_j, and the
loop) and 128 for each word it returned. The joint alive tables (two, for the bit k = 19 and for
the others, 2^24 entries each, indexed by the eight key bits and the 16-bit set
J_{k+1}) are built once (Section 11, one-time items). The walk of the program
counts the events exactly as listed; the C program of the sample (13.5) counts
the same events and gave the same pass units on every one of 40,000 outer steps
(226 passing) and on three steps with the cap forced low, before the sample was
frozen. (It charged a good word 2,048 units, not 128; none of those 40,000 steps
had one. 13.5 corrects for it.)

*The machine's bookkeeping.* X lists the work of the walk of 8.4; the machine
also keeps the register u of step 2 of 9.1 and tests it: one addition of an
immediate at each call (546), guess (199), root (5), push (11) and good word
(128) and after the leaf test of each pop (49 for an internal node, 62 for a
leaf), and before each pop the test u > CTR_STEP_CAP (a compare and a branch).
Per passing step it sets u to 0 (1), stores the ten words that step 3 reads
(10), adds X to the run's count (1) and tests the count against PASS_BUDGET (2):
14 in all. A good word's addition is inside the good word's charge (step 3
counts 96 against 128), and so are the scan's (a member counts 100 against
192): the scan adds SCAN_UNITS and 128 per returned word to u and loads the
words it reads.

**Lemma U.** In every outer step, the machine units of its pass work,
bookkeeping included, are at most (16/15) X. *Proof.* Outside the charges the
bookkeeping is Delta = 3 per pop, 1 per push, call, guess and root, 14 per
passing step, and 2 for the test that stops a call at the cap (inside the scan's
charge, since the scan follows). X holds at least 49 per pop (13, and 36 for an
internal node and its two children or 49 for a leaf), 11 per push, 546 per call,
199 per guess and 56 per passing step, which has at least one call. Every push
but those left on the stack of a call stopped by the cap is popped, so pushes are
at most pops plus 64, and the 64 are in a step whose X exceeds SCAN_UNITS; roots
are at most guesses. So 15 Delta <= 45 pops + 15 pushes + 15 calls + 30 guesses +
210 per passing step <= 49 pops + 11 pushes + 546 calls + 199 guesses <= X, as
45 p + 15 q <= 49 p + 11 q when q <= p. QED. The machine units of a run's pass
work are therefore at most (16/15) times the run's count, which the halt keeps
below PASS_BUDGET + X_MAX (the last step's X is added before the test).

*Lemma U in v108.* A passing outer step now has 40 more units of bookkeeping:

- the lane dispatch of its batch, a test of each z_i (14), charged to every
  passing step of the batch;
- the extraction of the lane's y, Y9, omega and the ten words that step 3 reads,
  a shift and an AND each (26).

So the bookkeeping is 54 per passing step, not 14. The proof of Lemma U then
reads 15 Delta <= 45 pops + 15 pushes + 15 calls + 30 guesses + 810 per passing
step. A passing step has at least one call, and a call that the cap does not
stop has four guesses. So 210 per passing step became 810 <= 546 - 15 + 4 *
(199 - 30) = 1,207 per call. The case of a call stopped by the cap is as before
(its step has X > SCAN_UNITS). The same inequality follows, and the pass work,
bookkeeping included, is still at most (16/15) times the run's count.

*The solver counted as well.* The program also runs the solver on the machine
itself (`ctr_solve_counted`: the keys, the joint alive sets read from the tables,
the stack walk and the leaves, and the register u with its test, every value a
counted word), step 3 (`ctr_good_counted`) and one member of the scan
(`ctr_scan_counted`). The table above is the itemization of that count: on every
call of the self-test (9.3, check 4) the counted units of the solver equal the
units of the table for the call's events plus 3 per pop and 1 per call, guess,
root, push and good word, with the same words and at most 17 registers; u equals
the call's units; and with the cap set to 1,500 the counted call stops exactly
where `ctr_solve` does, with 2 more for the stopping test. Step 3 counts 96 on its
longest path (c1 in Q* and t != 0) and 33 otherwise, against 128 charged; a
member of the scan counts at most 100, against 192 charged. The charges are what
the run, the sample and the bound X_MAX use.

*Bounds of X.* Every call that runs past the cap is stopped at the next pop, and
a call adds at most 1,347 units before its first pop; so X <= 56 + 2^23 + 14 *
1,600 + SCAN_UNITS + 128 * 286,720 = 447,764,408 = X_MAX (2^28.74) in every outer
step, the bound B of the sample's analysis. *Registers.* The batch and its filter
use at most 32 (v108). While the passing steps of a batch run, it keeps 20: the
thirteen lane words y, Y9, omega and the ten words of step 3, and the seven z_i.
The solver, with y, Y9, omega, u and the cap, uses at most 17. Step 3 uses at
most 10 and a scan member at most 12, loading the stored words they read
(counted). At most 64 throughout.

**9.3 The self-test.** `python3 experiments/halfsearch.py --selftest N [seed]`,
run from the repository root, prints one JSON line and exits with status 0 only
if every check below holds. (1) *Trials:* N cases, each an outer step from
SHAKE-256 of the text "halfsearch v107 trial", the seed and the case number
(every fifth with outer words 0, ffffffff or as drawn) and a member c1 of Q*: the
two last-chunk blocks by steps CO, CT and CS compressed in full with counter t and
flags 3 (`ctr_lane`: the round-1 words, E1 and E3 values, the block words, t <
2^32, chaining-value words 0, 2, 5, 7 equal, e1 in the class, c1 in Q*, beta*,
eta); Lemma IP read backwards gives c1 back from E3.h1; the E1 differences of
`ctr_good`'s formula equal those of the two real compressions; and every 25th
case the organizer's `verifier/blake3.py` `_compress` of the last chunk equals the
program's chaining value. (2) *Filter:* the automata against brute force at 10
bits (128 masks, as in 47804be2); the exact share recounted from the program's
tables equals CTR_SHARE; (v108) 2,340 batches, 16,380 real outer steps from
SHAKE-256 of "halfsearch v108 batch", the seed, the batch and the word number,
walked by `ctr_run` (passing steps run the solver), and a second walk with half
their pass units as budget halts. 16 counted batches (`ctr_count`), eight of them
with lanes holding 0 or ffffffff, are compared lane by lane with the scalar
`ctr_outer` and `ctr_filter`: every name of step CO and the mask. All 16 have the
same counts and at most 64 registers. (3) *Solver:* the 28
planted solutions (`CTR_FIXTURES`: y in the class, Y9, omega, j and h, made by our
development tool with conditions B and C planted and A by rejection) each pass
`ctr_e3`, have j in their mask and are found by the solver; on 30 calls (six of
the planted ones and the passing steps of (2)) the solver's output equals a
second enumeration that walks automaton B alone and tests every complete f with
`ctr_e3`; the cap path: the first planted solution placed at member 777 of Q*
(the words that step CT reads chosen for it, `ctr_planted`), its step run with
the cap 0, so that the solver stops at once and the scan (over the first 2^10
members) returns the planted word; the bound 286,720 of Lemma E3. (4)
*Counted:* on the 30 calls of (3), the units of `ctr_solve_counted` equal those
of `SOLVER_UNITS` for the events of `ctr_solve` plus the bookkeeping of 9.2, with
the same words and its register u equal to the call's units; with the cap 1,500
it stops where `ctr_solve` does; `ctr_good_counted` returns what `ctr_good`
returns on 64 words (half of them E3.h1 of trials with c1 in Q*), at most 127
units; `ctr_scan_counted` on 56 members (the planted solutions placed at a member
of Q* by `ctr_planted`, with the full mask and with the solution's bit cleared)
returns what the scan's test returns, at most 192 units; at most 64 registers
throughout; X_MAX as defined. It also checks that eps ^ ROL(beta* ^ eps, 1) ^ eta
= 0 (Lemma G) and prints the ledger of Section 11, with the exact check of the
claim (`claim_exact`). The walk of (2) is 16,380 outer steps (v108), so its pass
units per step vary much with the seed (X has a long tail, 13.5): 77.5 for seed 1
and 20.4 for seed 7, against the mean 83.74 of 2^35 steps.

Run for this package (v108) with N = 2,000 and seed 1, in the organizer's pinned
Python image without network: exit status 0. The report:

- trials 2,000 of 2,000 right, Lemma IP backwards 2,000 of 2,000, E1 differences
  2,000 of 2,000, the organizer's `_compress` 80 of 80;
- filter brute force 128 of 128, share 99,669,577,442,459,648 = CTR_SHARE;
  16,380 real outer steps with 91 passing and 1,268,752 pass units, the budget
  halt right;
- the counted batch 16 of 16 (319 and 56 units, at most 32 registers);
- solver: 28 of 28 planted solutions found, 30 of 30 calls equal to the second
  enumeration, the cap path right (the planted word returned by the scan), goods
  bound 286,720, eps ^ ROL(beta* ^ eps, 1) ^ eta = 0;
- counted: 30 of 30 solver calls equal to the table plus the bookkeeping, 30 of
  30 stops at the cap 1,500 equal, step 3 64 of 64 right with at most 96 units,
  the scan 56 of 56 right with at most 100 units, at most 17 registers;
- ledger time_log2 67.8127726, claim 67.81278, claim_exact true.

It took about 70 seconds. Seed 7 also exits with status 0 (16,380 outer steps, 99 passing, 334,530 pass units in its walk).

## 10. The rate of a counter trial and the success probability

**10.1 The model rate (v107: the class, fourteen outcomes).** The seven-word
model M of Section 13 treats the residual of a trial as a function of seven
words, E1.d1, E1.b1 and E1.a2 of message A and Y4, Y9, w8 and E3.h1. In v107 Y4
is uniform in the *class* (2^19 members) and the other six are independent
uniform words. In the count of Section 13 an outcome of beta is a pair (tau,
eps) of the differences of E1's a and c outputs; for an outcome j of beta*, L_j
is the number of triples (E1.c1, E1.b1, E1.a2) for which E1 on A and on B gives
the differences beta*, tau_j and eps_j, and N3_j the number of quadruples (Y4,
E3.h1, Y9, w8), Y4 in the class, for which E3 on A and on B gives the
differences eta and sigma_j of its first-half d and b values and tau_j and eps_j
of its c and a outputs. Every input of the 2^211 of the model falls into one
outcome, so the part of beta* in the rate of the class is r(beta*) = sum over j
of L_j N3_j / 2^83. The counting program of Section 17 (Jbenisek's, printed in
47804be2, exact integers, every tau with a nonzero E1 and E3 count enumerated
from both roots of eps), run on the class (its member list `Y4s` set to the 2^19
members of the class and the divisor to 2^83; its output in Section 17), finds
fourteen outcomes, all with eps = 6e21be55 (the other root, 91de41aa, has no tau):

| tau | L_j | N3_j (class) | L_j N3_j / 2^83 |
| --- | ---: | ---: | ---: |
| 175020a0 | 562,949,953,421,312 | 108,086,391,056,891,904 | 6,291,456 |
| 175060a0 | 281,474,976,710,656 | 6,755,399,441,055,744 | 196,608 |
| 185020a0 | 2,251,799,813,685,248 | 72,057,594,037,927,936 | 16,777,216 |
| 185060a0 | 1,125,899,906,842,624 | 9,007,199,254,740,992 | 1,048,576 |
| 275020a0 | 562,949,953,421,312 | 18,014,398,509,481,984 | 1,048,576 |
| 275060a0 | 281,474,976,710,656 | 1,125,899,906,842,624 | 32,768 |
| 285020a0 | 2,251,799,813,685,248 | 108,086,391,056,891,904 | 25,165,824 |
| 285060a0 | 1,125,899,906,842,624 | 13,510,798,882,111,488 | 1,572,864 |
| 385020a0 | 1,125,899,906,842,624 | 144,115,188,075,855,872 | 16,777,216 |
| 385060a0 | 562,949,953,421,312 | 18,014,398,509,481,984 | 1,048,576 |
| 675020a0 | 140,737,488,355,328 | 4,503,599,627,370,496 | 65,536 |
| 675060a0 | 70,368,744,177,664 | 281,474,976,710,656 | 2,048 |
| 685020a0 | 562,949,953,421,312 | 27,021,597,764,222,976 | 1,572,864 |
| 685060a0 | 281,474,976,710,656 | 3,377,699,720,527,872 | 98,304 |
| sum | | | 71,698,432 |

The same figure, 71,698,432, is the part of the solver's beta in the class that
the record of entry c66f230d gives for these constants (47804be2, Section 12,
"what rests on records"). It was recomputed independently by our counter (the
carry automata of our entries c19feef to d598fe29, `count_s8.py`, with the class
as member list): the same fourteen L_j and N3_j digit for digit, and on the
sub-class the seven rows of 47804be2 and 67,698,688, with N3 = 0 for the seven
taus ending in 5060a0. With rule A the class keeps only 33,849,344 of the
71,698,432 (Section 17); v107 does not use rule A. A trial of Section 8 has c1 in
Q* and so the difference beta* (Theorem C (iv)); under M the event c1 in Q* has
probability 2^-11 (Lemma S1, which holds for any member set). The rate of a trial
that M conditions on c1 in Q* is therefore

    p = 2^11 * 71,698,432 * 2^-128 = 146,838,388,736 * 2^-128,

about 2^-90.904. The class is four times as large as the sub-class (2^19
members against 2^17); per trial the rate is 1.0591 times that of 47804be2 (71,698,432 / 67,698,688), because the members of
the class outside the sub-class carry the seven outcomes with tau ending in 5060a0
and more of the others.

*Why beta*, and why the class.* beta* is the beta of the solver's solution from
which the six constants were chosen (step 2 of the selection procedure, Section
12): no ranking of betas is used. The class is the set of all Y4 of eta (Lemma
Q): no sub-class is chosen. The fourteen outcomes are all the outcomes of beta*
with a nonzero part in the class, as the counting program enumerates them.

**10.2 Lemmas on the counter sampler (GPT Sol 6.1; as in 47804be2).** *v107 note:*
with Y4 in the class, read "sub-class" as "class" in the hypotheses of Lemmas
S1 to S4, whose proofs do not use which member set it is; Lemma S5 is general;
Lemmas S6 and S7 assume the seven outcomes of the sub-class and rule A and are not
used by v107's claim (8.4 uses only Lemma S5 for its bound); Lemma S8 is general.
 The following lemmas were
proved by GPT Sol 6.1 for this construction, Lemma S9 by GPT Sol in its answer
AC, and are given with their hypotheses; each is exact mathematics under the
hypotheses stated. The
participant compared Lemmas S1 to S4 and Lemma IP with the construction line by
line; the carry Lemmas S5 to S7 were not re-derived by the participant. They do
not prove the rate of H1' or the success probability; 10.3 states what remains
a premise.

**Lemma S1 (conditioning the model).** *Hypotheses:* under M the six words
E1.d1, E1.b1, E1.a2, Y9, w8 and E3.h1 are independent uniform words,
independent of Y4, which is uniform in the class (v107; 47804be2 stated the lemma
for the sub-class, and the proof does not use which member set it is); c1 = Y11 +
E1.d1.
*Statement:* c1 lies in Q* with probability 2^-11, and that is the event that
E1's first-half b difference is beta*. Conditional on it, E1.d1 is uniform on
Q* - Y11, E1.b1 and E1.a2 keep their independent uniform laws, and (Y4, Y9, w8,
E3.h1) keeps its law and stays independent of (E1.d1, E1.b1, E1.a2). Hence
Pr_M(R = 0, the E1 outcome listed | c1 in Q*) = 2^11 Pr_M(R = 0, the E1 outcome
listed, c1 in Q*) = 2^11 * 71,698,432 * 2^-128 = p, the last step by the count of
10.1 (no rule A in v107).

*Proof.* Translation by Y11 makes c1 uniform and independent of every other
coordinate. By the identity of the proof of Theorem C (iv), c1 lies in Q*
exactly when the difference is beta*, and Q* fixes 11 bits of c1, so the
probability is 2^-11. The event depends on E1.d1 alone, so for every event G1
of the words of E1 and G3 of the words of E3, Pr_M(G1 and G3 | c1 in Q*) =
Pr_M(G1 | c1 in Q*) Pr_M(G3). No independence of the output differences inside
E1 or inside E3 is used. QED. The finite count 71,698,432 is the integer
computation of Section 17 (and of our counter); it is not proved by this
lemma.

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


**Lemma S9' (the success mass lies on passing outer steps; Lemma S9 of
47804be2 with the fourteen outcomes and the class).** (a) *No hypothesis.* In
every outer step, the count N_o of H1' below is the number of its listed good
trials, and each of them has its outcome in the mask of the step (Lemma F); in a
step that fails the filter N_o = 0. (b) *Hypotheses:* those of Lemma S1 with Y4
uniform in the class. Under M, also conditional on c1 in Q*, Y9 and omega are
independent uniform words, and the event S that R = 0 with an outcome among the
fourteen lies inside the event that the outcome is in the mask; so Pr_M(S | c1
in Q*) = p loses nothing on the steps that fail. *Proof:* as in 47804be2 (Y9
and w8 are independent uniform under M, w8 -> omega is a translation for fixed
Y4, Lemma S1 keeps the law of (Y4, Y9, w8, E3.h1), and Lemma F gives the
inclusion; by 10.1 all of p comes from the fourteen outcomes). QED. Statement
(b) is about M and says nothing about the sampler.

**10.3 Heuristics.**

**Heuristic H1' (score-critical).** Over the coins of the run, the
RUN_OUTER_STEPS independent uniform words of step 1 of 9.1, let N_o be the
number of listed good trials of one outer step (valid trials, t != 0, with R = 0
and an E1 outcome among the fourteen of 10.1). (i) *Rate:* E[N_o] >= (2^21 - 1)
q, with q = CTR_FACTOR * 2^-128 = 104,884,563,382 * 2^-128, the model's rate p
of 10.1 divided by 1.4 (rounded down). (ii) *Dependence:* rho = E[N_o (N_o -
1)] / E[N_o] <= 0.0065.

This is the premise of e7b17fd1 and 47804be2 (their H1') with three changes:
the member set is the class (their sub-class), the listed outcomes are the
fourteen of the class (their seven), and the factor is the count divided by 1.4
(theirs by 2). In the terms of Lemmas S1 to S4: the construction's pushforward of
the uniform outer words, with c1 over Q*, onto the seven model words carries at
least 1/1.4 of the integral p of the conditional law of Lemma S1, also after the
member with t = 0 is dropped (Lemma IP); and the successes of one outer step are
weakly dependent. Proved (Lemmas S2 to S4, which hold for any member y): the
outer words of a step are uniform in the chart of the seven context words of
Section 4; Y12 and w5 are independent uniform words; E1.a1 and E1.a2 - E1.b1 are
independent uniform words at every fixed c1; the sampler is the uniform-counter
sampler conditioned on c1 in Q*. Not proved: that E1.b1, E1.a2, E3.h1, Y9 and w8
have the model's joint law with the rest (GPT Sol 6.1 reduced this to the density
of seven words that the outer step fixes, Y12, Y1 + w12, C2.b1, C2.c1, w5, Y9 and
w8, which has not been counted; we searched all triangular orders of the
assignments for a chart in which Y12, Y1 + w12 and w5, or Y9 and w8, are free
words and found none, Section 13.8); how much success mass the member with t =
0 carries; and the dependence (ii). For (ii), Lemma S7's cap assumed rule A and
the sub-class and is not used here; GPT Sol 6.1's bound 2^-13 in a fresh-draw
model does not transfer (47804be2). What supports (ii) in v107 (13.7): every
success of an outer step is an E3-good word of that step (8.4), and on 2^33.58
real outer steps of the class no step had more than two E3-good words (620 steps
had one or two; in 51 of the 53 pairs the two words differ in bit 3 or bit 18 of
E3.f1). Conditioned on a success at each of these 673 words, with the words that
join E1 to E3 drawn under the model (65,536 draws per word), the other word of the
step had c1 in Q* in 881,396 draws and the E1 outcome of a second success in none
of 44,105,728. So rho, the expected number of further successes in the outer
step of a success, is estimated at 0 and is below 0.00015 for every one of the
673 words at once (95 per cent); (ii) asks for 0.0065. That the joining words
follow the model inside an outer step is the assumption.

*The margin 1.400 (disclosed).* The factor is the exact model count divided by
1.4, GordoAR's choice in 6a600434 and 3f8e4e89 (both plausible_not_refuted, on
Subflatus3's machines) and ours in d598fe29 (plausible_not_refuted); the entries
on this track that build on c66f230d, e7b17fd1 and 47804be2 among them, divide
by 2. RUN_OUTER_STEPS is minimal for success 0.39 (10.4), so a real rate of the
listed events below 1/1.4 = 0.714 of the model's would put the success bound
below 0.39; at margin 2 it took a rate below 0.5. What we know against it: in our
own d598fe29 the weakest real-trial check of a different arrangement of the same
construction (the root instance with D3.d1 = X3, a 2^-30 event) had ratio 0.82 +-
0.13 to the model, 0.8 standard errors above 0.714; it is not a check of this
arrangement. For this arrangement: Jbenisek's reduced-width end-to-end run found
251 collisions of complete messages against 255.0 predicted (0.98; at 8-bit word
width, without filter or solver), and his listed-E1-outcome rate on real counter
trials was 0.979 +- 0.022 of the model in passing outer steps (2^43 trials, sub-
class); our sample measured the full E3 side of a success on real outer steps of
the class, 0.948 (1,799 against 1,897.0) of the model (13.5), and the E1 side on real trials,
1.03 (82 against 79.5) of the model (13.6). Taken together the two sides give
0.948 * 1.03 = 0.977 of the model, with a standard error of about 0.11 if the
counts are Poisson (that of the E1 side dominates), so 0.714 lies about 2.4
standard errors below the estimate. The joint 2^-91 event itself is not
measured, and the product of the two sides is the model's independence, not a
measurement.

**Heuristic H2'' (score-critical).** Let X be the pass units (9.2) of one outer
step drawn as in step 1 of 9.1; the outer steps of a run are independent draws
of it. Then E[X] <= PASS_PREMISE = 1369/16 = 85.5625. Given it, the probability
that the pass units of a run exceed PASS_BUDGET = PASS_PREMISE * 6001/6000 *
RUN_OUTER_STEPS (rounded up) is below exp(-2,036,002): the outer steps are
independent, every X is in [0, B] with B = X_MAX = 447,764,408 (9.2), and Bernstein's
inequality with variance at most B * PASS_PREMISE per step gives the exponent
(RUN_OUTER_STEPS * PASS_PREMISE / 6000)^2 / (2 RUN_OUTER_STEPS B PASS_PREMISE +
(2/3) B RUN_OUTER_STEPS PASS_PREMISE / 6000). The premise rests on the
preregistered sample of 13.5: 2^35 single outer steps drawn uniformly, the same
program's units (with the correction of 13.5 for good words), empirical
Bernstein bound at most 85.50133 at 2^-64, and PASS_PREMISE the next multiple of
1/16. It bounds the mean of X, a fixed number; most outer steps have X = 0 and a
passing step about 15,500 on average, with a long tail (13.5). If the budget is
reached the run halts with failure: the time bound of Section 11 charges the
budget in full and is not affected. The success bound of 10.4 needs H2'': with
E[X] above 1369/16 * 6001/6000 the halt would be likely, so H2'' is
score-critical, although its sample makes it the better supported of the two.

**10.4 Success probability.** The probability space is the 8 * RUN_OUTER_STEPS / 7
independent uniform 256-bit words of step 1 of 9.1 (v108: they give RUN_OUTER_STEPS
independent outer steps, each distributed as in v107), for the fixed target. The
algorithm is otherwise deterministic. By H1' (i), lambda = RUN_OUTER_STEPS *
(2^21 - 1) * q >= 0.495910 (RUN_OUTER_STEPS is the smallest with this; the
program's LAMBDA). By Lemma S8 with H1' (ii), b(rho) >= 1 - 0.0065/2 = 0.99675
and the probability that no valid trial is a listed good trial is at most
exp(-0.99675 * 0.495910) = exp(-0.4942983) < 0.6099993. A listed good trial is
found unless the pass budget halts the run first (9.1; Lemmas F, E3, SC and G).
So the run outputs a collision with probability at least 1 - 0.6099993 -
exp(-2,036,002) > 0.39. When the algorithm outputs a pair, the pair is a genuine
collision: step 3 checks both complete digests, and the messages have different
lengths.

*Sensitivity.* At margin 2 instead of 1.4 the run would need 1.4286 times as many
outer steps and the claim would be higher by log2(2/1.4) = 0.515. If the listed
events occur at f * 2^-128 per valid trial with f < CTR_FACTOR, the success
bound falls below 0.39; for f between 1 and CTR_FACTOR the same success needs
RUN_OUTER_STEPS * CTR_FACTOR / f outer steps.

None of the heuristics is proved. Section 13 lists the evidence.

## 11. Charged time

One 2-round target compression costs one unit, and every other primitive word
operation, every load and every store included, costs 1/430 of a unit. The rows
below are in machine units of 9.2; 430 of them make one unit of time.

**The cost, with every term.** Every row is machine units times an upper bound on
how often a run executes it; the pass work is charged through the run's count of
pass units, which the halt of 9.1 keeps below PASS_BUDGET + X_MAX, times 16/15
(Lemma U).

| Row | How often over a run, at most | Machine units | log2 of the product |
| --- | --- | ---: | ---: |
| batch of seven walked outer steps (v108): eight random words, the lanes, e1 and y, step CO in the lanes (counted, 319); the filter (counted, 56); the loop (3) | RUN_OUTER_STEPS / 7 = 109,598,092,208,568,660,192 = 2^66.5707 | 378 | 75.1330 |
| pass work of all passing outer steps: dispatch, solver events of 9.2, scans and their words, and the machine's bookkeeping (Lemma U) | once | (16/15) * (PASS_BUDGET + X_MAX) = 70,030,237,603,621,761,361,927.5 | 75.8904 |
| tables built once: the filter's automata, the mask tables T1 and T2 (v108), the table of Q*, the transition and joint alive tables (bound in words) | once | 2^38 | 38 |
| **sum of the rows** | | | **76.5609** |

*The counted rows* are the program's `ctr_count` (9.2). The batch and the filter
are straight-line code, so their counts do not depend on the words; the self-test
finds 319 and 56 on 16 batches. *The pass work* is charged in
full at (16/15) (PASS_BUDGET + X_MAX), PASS_BUDGET = ceil(RUN_OUTER_STEPS * 1369/16
* 6001/6000); per walked outer step that is 91.282 machine units, against the
83.739 of X measured in the sample (13.5) and an estimated 88.6 with the
bookkeeping that Lemma U bounds (3 per pop and 1 per push, at about 1.18 pops
per walked outer step). *The tables built once:* the two automata below
2^26 (47804be2); the table of Q*, 2^21 words by a deposit of 21 bits,
below 2^28; the two joint alive tables, 2^25 entries, each from sixteen pairs of
states, two bits and two transitions with fewer than 256 operations in all, below
2^33; the transition tables, 256 entries. (v108) The mask tables: for each of the
2^33 entries of T1 and T2, the automaton on four bytes (13 units), the store (1)
and the loop (3), 17 * 2^33 < 2^37.09. Together below 2^34 + 2^37.09 < 2^38.
v108 needs no member table.

*One-time items outside the rows.* The final step, once: steps CT and CS for the
trial found, writing the two messages, shorter than 2^42 bytes each, and two
complete evaluations of blake3, below 2^38 units of time in all (47804be2).
Preprocessing: the selection procedure and our development of Section 12, below
2^62.95 operations, 2^54.2 units, charged in full.

Total:

    T = ((RUN_OUTER_STEPS / 7) * 378 + (16/15) (PASS_BUDGET + X_MAX) + 2^38) / 430 + 2^38
        + (116 * 2^56 + 116 * (2^52 + 2^10) + 2^50) / 430
      = 2^67.8127726...,

the program's `ctr_time` and `ctr_ledger` (in the self-test output; `SEL_OPS` holds
the last numerator). The claimed scalar is time_log2 = 67.81278, the total
rounded up at the fifth decimal: 2^6781277 < T^100000 < 2^6781278 in exact integer
arithmetic (T a fraction, both sides raised to the power 100,000; the self-test
checks it, `claim_exact`). It is a worst-case bound for the algorithm as stated,
which halts within its budget on every run; H1' and H2'' enter only the success
probability of 10.4.

*Where the time goes (v108).* The walk is 37.2 per cent of the sum of the rows
and the pass work 62.8. Per walked outer step the run is charged 145.28 machine
units, against 420.28 in v107 and 15,811.4 at the pass budget in 47804be2, whose
passing outer steps enumerate all of Q*. The search part is below 2^67.81266
units; the selection procedure is below 2^-13.6 of the total.

*Readings.* With the margin 2 of 47804be2 instead of 1.4, RUN_OUTER_STEPS and the
budget would grow by 1.4286 and T would be 2^68.3273 (v108). v107's readings under
47804be2's load-per-constant convention (2^69.8643) concern its scalar outer step,
which v108 does not use.
With the pass units charged at their worst case X_MAX in every passing outer step
the bound would not be useful; the budget is the halt that lets the average
count.

*The one formula.* In the form used on this track, time_log2 = log2(lambda) + 128
- log2(C / m) + log2(ops / 430), with lambda = 0.495910, C = 146,838,388,736 the
count of 10.1, m = 1.4 the margin and ops = 145.2819 / (2^21 - 1) machine units
per valid trial, gives 67.81266 for the search (v108).

The algorithm has no sorting and no lookup by value: it reads the mask tables at
positions Y9_i and omega_i (v108), and in passing steps the joint alive tables at
positions given by its own keys and sets.

## 12. Memory, preprocessing and advice

**Memory.** The program of the search is the lines of steps CO, CT and CS, the
filter, the solver, the scan and a compression routine for the final check;
bound the code by 2^19 bytes as in 47804be2. Data, one word of 256 bits each
unless said: the filter's tables (fewer than 2^15 entries), the mask tables T1
and T2 (v108: 2^33 words; no member table), the table of Q* for the scan (2^21
words), the two joint alive
tables (2 * 2^24 entries of at most 80 bits, one word each), the solver's arrays
and stack (fewer than 2^12 words) and fewer than 2^10 words of names, constants
and counts: fewer than 2^33.01 words, below 2^38.01 bytes. Nothing grows with the
number of trials. The two messages of a found pair are each shorter than 2^42
bytes; the selection procedure holds fewer than 2^34 + 2^31 bytes (47804be2).
Even all held at once these stay below 2^44 bytes: memory_log2_bytes = 44.

**Preprocessing: the selection procedure SEL.** The stored values are the six
constants and eta, beta* with its cube, and the fourteen outcomes (tau, eps).
v107 stores no sub-class, no rule and no ranking of betas, so its SEL is steps 1
and 2 of the selection procedure of 47804be2, which we take over as written
there (Section 12 of 47804be2; summarized). As there, every run of a program in
SEL halts as soon as it has executed its cap of primitive word operations,
counted as in Section 11 (430 to the unit), or holds 2^34 bytes, and a run so
halted returns nothing; its inputs are the participant's solver log (116
instances with their bounds and seeds) and the counting program, which takes the
member list as an input (the class's list is Lemma Q's):

*Step 1, the pinned call (solver runs).* For each of the 116 runs of the
participant's solver log for this search (Jbenisek's log: 51 runs for the lengths
55 and 63, 65 for nine other variants of the instance; logged bounds and seeds),
build the instance of the run and run kissat on it with the logged seed, with a
cap of 2^56 operations. A run that finds a model returns six constants X3, X7,
X11, X15, W4, W13 and the values of a solution, among them its Y4 and its beta.
Cost: at most 116 * 2^56 < 2^62.86 operations.

*Step 2, the constants, the class and beta*.* For each model of step 1, compute
Y3 and Y3' by C3 from its constants, its class eta = ROR((Y3 + Y4) XOR (Y3' +
Y4), 16) from the Y4 of its solution, and with the counter the part of the beta
of its solution in the rate of that class, with a cap of 2^52 (47804be2). Output
the six constants, the eta and the beta of the model with the largest part. In
v107 the run of the counter on the selected model also outputs the outcomes of
that beta with a nonzero part in the class: the counting program of Section 17
enumerates them while it counts (its function `taus` and the E3 screen), so no
further run is needed. Cost: at most 116 * (2^52 + 2^10) < 2^58.86 operations.
By the records of 47804be2 (its Section 12, "what rests on records") step 2
returns the constants of 3.2, eta = 830303cf and beta* = 18b0e098, with the part
71,698,432 in the class; our run of the counting program on the class returns
the fourteen outcomes of 10.1 with that sum (Section 17).

*Our development and measurement* (charged as preprocessing, though they select
only the design: the class, the solver, the margin, the cap, the event units):
every counter run, filter count, chart search, C measurement and the sample of
13.5, below 2^50 operations in all by their run times on one machine. (v108) The
development of the seven-lane walk (counts, lane checks and self-test runs, a few
minutes of one core) is below 2^42 operations and is inside the same 2^50 term.

*The bound.* SEL and development cost fewer than 2^62.86 + 2^58.86 + 2^50 <
2^62.95 operations, below 2^54.21 units: preprocessing_log2 = 55, charged in full
in T (Section 11). Steps 3 to 6 of 47804be2's SEL (the betas, the betas with a
part in the class, the sub-class, rule A and the ranking of betas) select values
that v107 does not use, and are not charged.

**Advice.** nonuniform_advice_log2_bytes = 7 covers the 28 bytes of the six
constants and eta, 12 bytes of beta* and the mask and value of its cube, 60
bytes of the fourteen tau and eps, 8 bytes of the class mask and value, and 4
bytes of the part 71,698,432, from which RUN_OUTER_STEPS, PASS_BUDGET and X_MAX
follow by the formulas of 9.1: 112 bytes. The tables are not advice: the program
computes them from these constants. The flags 3 and the counter rule are part of the algorithm. There is
no stored collision.

## 13. Evidence, scope and field meanings

Costs and bounds are rounded up, margins and the counts that the claim uses are
rounded down, and counts printed with decimals are rounded to the nearest.

**13.1 What is exact.** Sections 2 to 5 and 7; in Section 8 Theorem C, Lemmas
CT, IP and F, the share of 8.3, and Lemmas E3, SC, D and G of 8.4; Lemmas L, H,
Q, Q2, T, T2, N and TR; Lemma U of 9.2; the count of Section 17 (an integer
computation); and Lemmas S1 to S8 and S9' under their stated hypotheses. The
declared experiment `half-collision` runs one trial of the root instance per organizer seed, and the
organizer recomputes both digests; Lemma T predicts the 128 masked digest bits.
The counter instance, the filter and the solver have no organizer-run check
(6.4); the self-test (9.3) is the program's own check.

*Who wrote and who checked what is new in v107.* Lemmas E3, SC, D (as used here),
G and U, the solver, the joint alive tables, the cap and scan, the event units and
the program changes were written by us (winglock, with helper agents that are
instances of the AI model that wrote this text). Their checks are computations,
not proofs: the self-test (9.3), which also counts the solver, step 3 and a
member of the scan primitive by primitive against their charges; the solver
against the plain C solver of our
development on 302 passing calls (the same words and the same node counts) and
against brute force over the planted solutions; the C program of the sample
against the Python program on 40,000 outer steps and three forced scans (9.2);
and the count of the class by two programs (10.1). No person has read this text.

**13.2 The seven-word model.** As in 47804be2 (its Section 13): by Lemma D the
residual of a trial is a function of the constants and of seven words, E1's d1,
b1 and a2 on message A and E3's Y4, Y9, w8 and h1 on A. The model M says that
over the trials the six words other than Y4 behave like independent uniform
words, independent of Y4, which in v107 is uniform in the class. Under M the
part of beta* is the count of 10.1, and conditioning on c1 in Q* gives p (Lemma
S1). M gives the rate of a single trial; it does not give the probability that a
run has a listed good trial, which also depends on how successes cluster (H1'
(ii)).

**13.3 Inherited evidence (Jbenisek, e7b17fd1 and 47804be2; participant
measurements on the sub-class, untrusted by the harness).** About 2^45.6 real
32-bit counter trials whose measurable partial events matched the exact model
within about 1%; a reduced-width (8-bit) end-to-end run with complete messages in
which the counter arrangement found 251 collisions against 255.0 predicted;
inside passing outer steps (2^43 trials) the E1 test of Lemma N at 0.9945 +-
0.0031 and the listed E1 outcome at 0.979 +- 0.022 of the model; the pass share
of the seven outcomes on real outer steps at 1.0003 of the exact share. These
were measured with Y4 in the sub-class. The E1 side does not read Y4 except
through the outer words; the E3 side does, and 13.5 measures it on the class.

**13.4 Organizer experiments.** Unchanged from 47804be2 in what they test (6.4);
`residual-search` no longer returns the root batch's counts (6.5). On 32 seeds we
checked, both experiments output byte-identical messages to those of 47804be2's
program. We present no inference over organizer trials: the experiments'
predictions are exact per seed.

**13.5 The preregistered sample (the premise of H2'', and the E3 side of H1').**
*Plan.* Before any run we froze and hashed (SHA-256, frozen 2026-10-09T02:46:42Z,
SHA-256 of the hash file
494c7013b8ed910bc82027ed7ef6d12dc2a0f6d8cf6f1554c395c75c024a8cc1) the plan, the C program (`sample.c` with
`e3core.h` and `jsolve.h`: step CO, the filter by the two carry automata, the
solver with the cap and the scan, `ctr_good`, the same events and units as the
Python program, cross-checked before freezing as in 9.2), the seed rule (SHA-256
of "v107 sample", the hash of the hash file and the run index), the analysis
(`analyze.py`) and the launcher. Units: single outer steps, each from a fresh
256-bit word of xoshiro256** seeded per run (participant-side generator); 32 runs
of 2^30 outer steps, 2^35 in all. All 32 runs are reported; none was dropped or
restarted. The statistic of the premise: X, the pass units of the step (0 when
the step fails the filter); the premise bounds the mean of X for one uniform
outer step (the plan's "run average of the pass units per walked outer step"). The bound: the empirical Bernstein bound U = mean +
sqrt(2 V ln(2/d) / n) + 7 B ln(2/d) / (3 (n - 1)) with d = 2^-64 and B =
447,764,408 (9.2); the premise is the next multiple of 1/16 above U.

*Result.* n = 2^35 = 34,359,738,368 outer steps in 32 runs; 185,642,280 passed the filter (2^-7.532050, 0.99996 of the exact share 2^-7.531997); 237,913,184 solver calls; the cap was never passed (no scan) and the largest X_C was 4,967,706; the mean of X_C (X as the C program counted it, see the correction below) is 83.73916 machine units with standard deviation 7,660.38 and the empirical Bernstein bound U = 85.50143, and for X itself the mean is 83.73906 and U is at most 85.50133, so the premise is 1369/16 = 85.5625, the decision the plan fixed. Words E3-good for an outcome (goods): 1,799 against 1,897.0 under the model, 0.948 (a standard error of 0.022 if the counts are Poisson; clustering inside an outer step would make it larger), 2.2 standard errors below 1. Per outcome (measured against the model, in the order of 10.1): 346/384, 37/24, 249/256, 26/32, 57/64, 2/4, 365/384, 37/48, 503/512, 60/64, 16/16, 1/1, 89/96, 11/12; weighted by the parts of 10.1 the ratio is 0.953. None of the 1,799 had c1 in Q* (0.88 expected), so none reached E1. The run records (one JSON line per run with its seed), the hash file, the plan and the programs are kept; the analysis printed these figures.

*The 32 runs* (n = 2^30 each, no scan in any; X_C is X as the C program counted it, see below; the sums of squares were accumulated in double precision, to about 1 part in 10^7):

| run | seed | passing | calls | Sum X_C | Sum X_C^2 | max X_C | goods |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 00 | 4474353983366526014 | 5,800,957 | 7,435,403 | 89,762,895,188 | 62779585477967600 | 4,967,706 | 47 |
| 01 | 12944255982443061366 | 5,802,357 | 7,437,138 | 90,325,970,534 | 63454309045487696 | 4,967,000 | 63 |
| 02 | 10117918062397586130 | 5,803,546 | 7,438,637 | 89,767,476,140 | 62514917664508944 | 4,967,000 | 54 |
| 03 | 6341918958781563761 | 5,798,844 | 7,432,646 | 89,847,798,592 | 62500520715730352 | 4,967,000 | 66 |
| 04 | 5802417771639244809 | 5,800,930 | 7,433,306 | 89,933,156,360 | 63148373813859184 | 4,967,000 | 62 |
| 05 | 2111846467043059547 | 5,798,751 | 7,431,316 | 89,839,036,326 | 62526623244289344 | 4,967,706 | 68 |
| 06 | 6341896410922616008 | 5,804,522 | 7,437,400 | 89,811,083,440 | 62851473795386672 | 4,967,000 | 68 |
| 07 | 16361129110341092974 | 5,808,717 | 7,443,747 | 90,352,145,666 | 63141612923373344 | 4,967,000 | 52 |
| 08 | 9986205922099658083 | 5,804,043 | 7,437,544 | 90,370,225,820 | 63834386081475200 | 4,967,000 | 52 |
| 09 | 14916648442200170617 | 5,800,209 | 7,431,704 | 89,815,771,658 | 62889245706156464 | 4,967,000 | 55 |
| 10 | 1571490514761722729 | 5,797,331 | 7,427,817 | 89,959,035,946 | 63366417511304416 | 4,967,000 | 59 |
| 11 | 11202644098530051171 | 5,801,266 | 7,435,128 | 89,923,404,086 | 63295430154059856 | 4,967,000 | 69 |
| 12 | 5308755110206028863 | 5,802,837 | 7,438,031 | 90,167,489,148 | 63375452101495744 | 4,967,000 | 58 |
| 13 | 12253544939496062338 | 5,800,337 | 7,432,705 | 90,058,486,978 | 63325577393070080 | 4,967,000 | 54 |
| 14 | 1835763974283119762 | 5,801,115 | 7,436,426 | 89,874,100,478 | 62995957980312000 | 4,967,000 | 62 |
| 15 | 16564361723776721645 | 5,802,103 | 7,435,419 | 89,275,958,318 | 62339111146412000 | 4,967,000 | 34 |
| 16 | 5460910542284182391 | 5,802,720 | 7,437,338 | 90,212,543,962 | 63095496473409648 | 4,967,706 | 62 |
| 17 | 5397746531329042153 | 5,798,842 | 7,430,185 | 89,658,870,414 | 62769864182452320 | 4,967,000 | 49 |
| 18 | 16973733355920003834 | 5,800,185 | 7,433,810 | 89,694,977,020 | 62874051642410224 | 4,967,000 | 50 |
| 19 | 18216326774540161900 | 5,799,950 | 7,431,663 | 89,945,852,232 | 62757817460708080 | 4,967,000 | 55 |
| 20 | 14040267027338959019 | 5,799,124 | 7,431,963 | 90,009,812,270 | 63511114070893936 | 4,967,000 | 57 |
| 21 | 9675455109907391375 | 5,797,229 | 7,428,759 | 89,775,865,956 | 62772032573216992 | 4,967,000 | 52 |
| 22 | 12172675593399644458 | 5,801,644 | 7,436,357 | 90,174,147,618 | 62936885908219024 | 4,967,000 | 51 |
| 23 | 10383202261829555013 | 5,801,440 | 7,435,185 | 89,996,915,746 | 63075492864088800 | 4,967,000 | 53 |
| 24 | 6165406361431053387 | 5,797,681 | 7,426,767 | 90,255,367,888 | 63530079962177312 | 4,967,706 | 40 |
| 25 | 381733957220384815 | 5,803,617 | 7,437,418 | 90,050,332,504 | 63219715348337920 | 4,967,706 | 62 |
| 26 | 18012134941967445385 | 5,798,360 | 7,432,298 | 89,752,128,004 | 63006816416608480 | 4,967,706 | 53 |
| 27 | 13221774855490117762 | 5,802,148 | 7,436,560 | 89,253,796,516 | 62402602709939616 | 4,967,000 | 56 |
| 28 | 16544001116756992192 | 5,799,518 | 7,432,982 | 89,862,381,622 | 63274492619480736 | 4,967,706 | 62 |
| 29 | 17731994910957527879 | 5,801,683 | 7,435,966 | 89,862,057,316 | 62633954486645904 | 4,967,000 | 67 |
| 30 | 17987617500572578483 | 5,804,003 | 7,438,180 | 89,499,051,706 | 62692875587731600 | 4,967,000 | 45 |
| 31 | 14886266609514840075 | 5,806,271 | 7,443,386 | 90,167,374,232 | 63624603335885856 | 4,967,000 | 62 |

*A correction after the run.* The frozen C program charged a good word 2,048
units, not the 128 of the Python program and of the plan's B; the cross-check of
9.2 had no good word, so it did not show. All 1,799 good words of the sample
were returned by the solver (no scan), and the cap was never near (the largest
X_C was 4,967,706 < 2^23), so no stop differs and on every sampled step X = X_C
- 1,920 * (its good words). Hence the mean of X is exactly (Sum X_C - 1,920 *
1,799) / n = 83.73906, and Sum X^2 <= Sum X_C^2, so the sample variance of X is
at most the value computed from the run sums; the empirical Bernstein bound with
these is at most 85.50133, against 85.50143 as the frozen analysis computed it on
X_C, and the premise stays 1369/16. The bound applies to X, which lies in [0, B];
X_C does not provably.

*Reading.* The pass share on real outer steps agrees with the exact share of
uniform pairs, as in 47804be2 for the seven outcomes: the filter sees the
sampler's (Y9, omega) as uniform at this resolution. The E3-good count is a
direct measurement, on 2^35 real outer steps of the class, of the E3 side of a
success: the expected number of words E3.h1 for which E3 of both messages has an
outcome's differences, against the model's Sum_j N3_j / 2^83 = 2^-24.1105 per
outer step (1,897.0 for 2^35). The measured events are those that the run's
successes need on the E3 side; none of them had c1 in Q* together with the E1
outcome (none expected: about 2^-46 each).

**13.6 The E1 side on real trials (participant evidence, not preregistered; all
runs reported).** 16 runs (seeds 1 to 16, fixed before the runs; the program `e1meas.c` with `e3core.h`, hashed before the runs) of 2^22 outer steps of the class and 2^12 random members of Q* each, 2^38 trials. Every trial had beta* (Theorem C (iv)). 82 trials had E1 differences (tau, eps) among the fourteen outcomes, against 79.5 under the model (the sum over j of 2^11 L_j / 2^96 = 2^-31.687 per trial): ratio 1.03, with a standard error of 0.11 if Poisson. Per outcome (measured against the model): 3/4.0, 1/2.0, 22/16.0, 6/8.0, 3/4.0, 0/2.0, 17/16.0, 8/8.0, 14/8.0, 2/4.0, 0/1.0, 0/0.5, 6/4.0, 0/2.0. The E1 test of Lemma N passed 3,925 times, 2^-26.06 per trial (Jbenisek: 2^-26.02 on the sub-class). These agree with 47804be2's 0.979 +- 0.022 for the seven outcomes inside passing outer steps.

**13.7 Two successes in one outer step (participant evidence for H1' (ii); not
preregistered; all runs reported).** *Real outer steps.* A walk of 12 runs of
2^30 uniform outer steps of the class (seeds from SHA-256 of "v107 rho walk" and
the run index; the program `rho_walk.c`, the sample's code with an output line for
every step with an E3-good word) found 673 E3-good words in 620 steps (711.4
expected under the model, 0.946): 567 steps with one word, 53 with two, none with
more. In 51 of the 53 pairs the two words differ in h by 00008000 or c0000000 (bit
3 or bit 18 of E3.f1) with the same outcome. Every success of an outer step is an
E3-good word of it (8.4), so a second success in the outer step of a success
needs one of these pairs.

*Conditioned on a success.* For each of the 673 words, `rho_sim.c` drew 65,536
times an E1 success of the word's outcome (c1 in Q*, E1.b1 and E1.a2 with E1's
differences beta*, tau_j and eps, from a pool of 4,096 per outcome made by a carry
walk) and the words that join E1 to E3 (Y12 and C2.c1 uniform; Y6, Y1 + w12, w5
and C2.b1 solved so that the trial of that c1 has E3.h1 = the word), checked the
planted trial forward (Lemma IP returns the c1, and E1 has the outcome; all
44,105,728 right), and for the other word of the step computed its c1 (Lemma IP)
and its E1. Result: 6,946,816 partner words, 881,396 with c1 in Q*, and a second
success (the partner's own outcome, or any of the fourteen) in none. Under the
model for the joining words this puts rho at 0, below 0.00015 for every one of the
673 words at once at 95 per cent, against the 0.0065 of H1' (ii). The joining
words are drawn as the model draws them; that they behave so inside a real outer
step is what H1' (ii) assumes.

**13.8 Searches that found nothing.** To prescribe more of the model's words than
Y4 and c1 we searched all triangular orders of the 92 assignments of the eleven
round-0 and round-1 calls and E1's first three (a peeling test over every choice
of the free words, cross-checked on the order of e7b17fd1): there is no order with
Y4, the counter's inner word and C2.c1, or Y1 + w12, free; none with Y12, Y1 +
w12 and w5 free; none with Y9 and w8 free together with Y4 and an inner word; and
no order in which Y9 and w8 are computed before a free word that could vary the
rest. So the E3 side cannot be prescribed by a triangular order, and v107
solves it per outer step instead (8.4).

**13.9 Field meanings.** time_log2 is the logarithm of the total charged time of
Section 11, an upper bound for every run; memory_log2_bytes = 44 and
preprocessing_log2 = 55 as in Section 12; success_probability 0.39 under H1' and
H2'' (10.4); nonuniform_advice_log2_bytes = 7 (112 bytes).

## 14. Corrections to our entry c66f230d

*(Jbenisek's section of 47804be2, unchanged; "our" is his.)*

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
   no independence.) Section 10.3 of this text states H1' in a two-part form.
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


## 15. What is the same as 47804be2 and what is new

*The same* (Jbenisek's, with his credits in 16): the construction and the root
instance of Sections 1 to 7 and the two declared experiments; the counter order,
Theorem C and Lemmas CT and IP; the outer filter, its automata and its byte
tables, Lemma F; the seven-word model; Lemmas S1 to S8; the premise H1' in its
form; the selection procedure's steps 1 and 2; the counting program of Section 17;
the final step and the memory of the messages.

*New in v108 (leech1996):* the walk of step 1 of 9.1 in batches of seven outer
steps, one per 36-bit lane, with lane words that carry bounds and skip the 32-bit
masks (Lemma L7); the filter by two mask tables of 2^32 entries built once; the
counted batch (319 + 56 + 3 = 378 machine units per seven outer steps, against
7 * 329 = 2,303 in v107); the passing-step bookkeeping of the lanes inside Lemma
U; the self-test's lane-by-lane check of 16 counted batches; and the one-time
charge 2^38. Nothing else changes. The total falls from 2^69.3451998 to
2^67.8127726, a factor 2^1.532: the charge per walked outer step goes from 420.28
to 145.28 machine units.

*New in v107 (winglock):*

- the member set is the class (2^19), not the sub-class, and rule A is not used;
  with it the listed outcomes are the fourteen of the class, whose part is
  71,698,432 (10.1), and the filter carries fourteen outcomes (8.3, recounted
  share 2^-7.531997);
- the cube enumeration of a passing outer step (12,957,444 machine units) is
  replaced by the exact E3 solver of 8.4 with Lemmas E3, SC and G, the cap and the
  fallback scan, and step 3 decides R = 0 from E1's differences (Lemma G);
- the factor of H1' is the count divided by 1.4 (GordoAR's margin), not by 2;
- the outer step and the filter are counted on a machine with 64 registers and
  immediate constants (294 and 32 units), and the loop adds 3; the solver is
  charged per itemized event and counted primitive by primitive, with the
  machine's bookkeeping bounded by Lemma U; the pass units have a budget 1/6000
  above a premise (H2'') that a preregistered sample of 2^35 single outer steps
  set, and the pass work is charged at 16/15 of the budget plus one step's
  maximum; RUN_OUTER_STEPS is the smallest run for success 0.39 (lambda =
  0.495910);
- the within-step measurement of 13.7 for H1' (ii);
- the selection procedure is steps 1 and 2 of 47804be2's, plus our development
  (2^62.95 operations), because the sub-class, rule A and the ranking of betas are
  not used;
- the program: the root instance's counted batch, the counter batch and rule A's
  machinery are removed; the class, the solver, the scan, step 3's decision, the
  counted outer step on our machine, the counted solver, step 3 and scan member,
  the ledger and a new self-test are added; `residual-search` returns only the
  number of tries.

The search part drops from 2^75.191 units (47804be2) to 2^69.34517; the claim
from 75.42 to 69.34520. Of the 6.075: the work per walked outer step about 5.234
(15,811.4 machine units at 47804be2's pass budget against 420.28 here: the solver
in place of the cube enumeration, and the outer step's convention), the margin
0.515, the selection procedure 0.228 (47804be2's SEL was 2^-2.551 of its search
part), the class 0.083 (71,698,432 against 67,698,688), and lambda and rounding
the rest.

## 16. Credit

Ideas and work are credited to their authors; co-authors are named in the
submission's co-author field for the contributions credited to them here, and none
of them is represented as having reviewed or endorsed this package.

- **Jbenisek** (co-author): the construction and the root instance (c66f230d,
  64c075ac), the chunk-counter construction with Theorem C, Lemmas TR, CT and IP
  and the counter search (e7b17fd1), the exact outer filter with its automata, byte
  tables, Lemma F, Lemma S9 and the exact share (47804be2), the counting program of
  Section 17 and its records, the selection procedure whose steps 1 and 2 we use,
  the reduced-width end-to-end run and the measurements of 13.3; with the
  contributions he credits to GPT Sol 6.1 (OpenAI; Lemmas S1 to S9, IP, F, the
  certificate of the share, the sub-class and rule A of the earlier entries) and to
  his helper agents.
- **Subflatus3** (co-author): preregistered samples of single uniform units with
  an empirical Bernstein decision rule (52bb50ee, 1d5e54ce, 5ca02dfb), the design
  of our sample of 13.5; register residency and paired tests in the counter batch
  (836705d7, 383ac0b3), which v107 does not need because it has no cube
  enumeration.
- **GordoAR** (co-author): the margin 1.400 on the model count (6a600434,
  3f8e4e89).
- **leech1996** (co-author): budgets 1/6000 above their premises (5266c5ce).
- **tekkac** (co-author): the seven 36-bit lanes with a masked rotation (ticket
  2bf40fb), used by the filter's predecessors and by 47804be2's batch, credited
  there and in 6.5.
- **Th0rgal** (co-author): values that depend on the member alone built once per
  outer step (df8bd46d) and coding steps from 8c81a219, used by e7b17fd1.
- **5kyguy** (co-author): masks kept in registers across a loop (404d14df), used by
  e7b17fd1 and 47804be2.
- **leech1996 (v108)**: the seven-lane walk with bounded lane words (Lemma L7),
  the mask tables, the counted batch, the change to Lemma U's bookkeeping and the
  v108 edits of this text and of the program. The work was done by Claude Opus 5.5
  (Anthropic) in Claude Code. The 36-bit lanes with a masked rotation are tekkac's
  (ticket 2bf40fb). Everything else in this package is v107's.
- **winglock (v107, dd91b2f6)**: the exact E3 solver (8.4) with the joint alive
  tables, Lemmas E3, SC and G, the cap and the scan, the class without rule A and
  the fourteen outcomes, the counted outer step on the 64-register machine, the
  per-event units, H2'' with its preregistered sample, the E1 measurement, the
  searches of 13.8, the within-step measurement of 13.7, the program changes and this text; earlier: the per-member
  sub-class selection (18a7fc52), the counter of our entries c19feef to d598fe29
  that recounted 10.1, the 64-register convention (ef052659, d598fe29). Helper
  agents, instances of the AI model that wrote this text, wrote the code, ran the
  checks and wrote the text.

## 17. The counting program (Jbenisek, 47804be2) and its run on the class

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


*v107: the same program run on the class.* We ran the program above, unchanged
except for three lines that set the member list `Y4s` to the 2^19 members of the
class (`subs(~0x03cf8303 & 0xffffffff)` in place of `subs(~0x07ef8303 &
0xffffffff)`), the assertion on their number to 2^19, and the divisor of the
printed parts to 2^83 (the label of the column still reads 2^81), with `python3
-B` (Python 3.14). Its output:

```text
eps 91de41aa: 0 tau pass N1 and N2, 0 also the E3 screen
eps 6e21be55: 18620 tau pass N1 and N2, 52 also the E3 screen
beta 18b0e098: 14 outcomes with L * N3 > 0
tau       eps       L                  N3                 L*N3/2^81  rule A
175020a0  6e21be55  562949953421312    108086391056891904  6291456    54043195528445952
175060a0  6e21be55  281474976710656    6755399441055744   196608     0
185020a0  6e21be55  2251799813685248   72057594037927936  16777216   36028797018963968
185060a0  6e21be55  1125899906842624   9007199254740992   1048576    0
275020a0  6e21be55  562949953421312    18014398509481984  1048576    9007199254740992
275060a0  6e21be55  281474976710656    1125899906842624   32768      0
285020a0  6e21be55  2251799813685248   108086391056891904  25165824   54043195528445952
285060a0  6e21be55  1125899906842624   13510798882111488  1572864    0
385020a0  6e21be55  1125899906842624   144115188075855872  16777216   72057594037927936
385060a0  6e21be55  562949953421312    18014398509481984  1048576    0
675020a0  6e21be55  140737488355328    4503599627370496   65536      2251799813685248
675060a0  6e21be55  70368744177664     281474976710656    2048       0
685020a0  6e21be55  562949953421312    27021597764222976  1572864    13510798882111488
685060a0  6e21be55  281474976710656    3377699720527872   98304      0
part = sum / 2^81 = 71698432 remainder 0; with rule A 33849344 remainder 0
seconds 68.6
```

(The 38 taus with an N3 and L = 0, which the program also prints, are left out
here.) The parts are those of 10.1; our own counter (carry automata, written for
our entries c19feef to d598fe29) gave the same fourteen L_j and N3_j.

**End of Section 17.**
