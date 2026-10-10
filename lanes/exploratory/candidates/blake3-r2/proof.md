# A last-chunk half-collision and a chunk-counter search for 2-round BLAKE3

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
separately reported resource bound.

This exploratory package targets blake3-r2-prefix-v1. It has an exact part and a
heuristic part, and it keeps them apart. It is a distinct path, filed to record
it: the search of our entry e582a556, with the same outcomes, run, budgets and
heuristics, and with steps 2 and 3 repriced by guards proved in this text. Next
to the six outcomes of beta* = 18b0e098 in S (175020a0, 185020a0, 275020a0,
285020a0, 385020a0 and 685020a0, eps 6e21be55) it lists three outcomes of a
second difference beta3 = 18d0e098, with tau 185020a0, 285020a0 and 385020a0 and
eps 6e61be55: nine outcomes in all, the set S9 (9.8). The trials of an outer
step are the words c1 of the union U of the cube Q* of beta* and the cube Q3 of
beta3, 2^22 words; the cube test of the certificate is a test, not a restriction
of the enumeration, so the trials of beta3 are reached in the same outer steps
(9.8).

Steps 2 and 3 of a passing outer step cost at most 314,996,576 machine units,
whatever its words: 17,504 for the outcomes of S, by the joint solver of 9.4
with the guards (G7) and (G15) and the root certificate of Lemma RC (9.7, 10.2,
Section 11); and 157,489,536 for each of at most two rows of beta3, by a generic
two-carry traversal with both guesses of the carry a20, guarded at positions 7,
15 and 20 by (G7), by (G15b), the form of (G15) for the cube of beta3, whose
fixed low bit differs, and by (G20b), the forward guard of Lemma J0 proved for
beta3 by modular arithmetic on (J2) (Lemmas G7b, G15b and G20b, 9.8). The batch
of seven outer steps is charged 341 machine units and a Q path 13, the schedule
of the direct filter tables (9.8). The claim is time_log2 = 78.8913. The exact
filter (Section 8, widened in 9.8) skips every outer step that cannot hold a
success with an outcome of S9, and the s-pattern pre-check of 9.7 serves the
outcomes of S. The heuristics are H1' and H4', stated for the union U and the
nine outcomes (10.3); H4' has two clauses, one for each count that halts the
run. GPT Sol, an AI model run by the participant, proved the guards, the
schedules and the caps (Section 16).

**Exact part.** An explicit construction maps seven 32-bit words, a member y of
the class of eta, a set of 524,288 values, and one more word c1 to a number t
and to a 55-byte string A and a 63-byte string B. When t is not zero, F || A
and F || B, with F a string of t full chunks of 1,024 bytes, are messages of
1024 t + 55 and 1024 t + 63 bytes whose last chunks are A and B, and the
2-round compressions of these last chunks, with chunk counter t and flags 3,
give chaining values that agree on their words 0, 2, 5 and 7, that is on 128 of
their 256 bits. There is no search in this and no probability: it holds for
every choice (Sections 7 and 8). In the organizer's tree mode the digest of
such a message depends on F and on the chaining value of its last chunk alone
(Lemma TR), so a pair whose last-chunk chaining values agree in all eight words
is a collision of two complete messages. The number t is not chosen: it is the
chunk counter that the round-0 call K0 reads, solved per trial as t =
ROL(K0.d1,16) XOR K0.a1. It takes up the freedom of the message word w0, and
that is what lets the construction prescribe c1, the third value of the round-1
call E1, next to y. The search holds c1 inside the union U of the set Q* of the
2^21 words for which the first-half b difference of E1 is beta* = 18b0e098 and
the set Q3 of the 2^21 words for which it is beta3 = 18d0e098 (9.8).

**Heuristic part.** A collision needs the other four words of the chaining value
to agree as well. The algorithm draws 568,084,180,184,553,153,661 = 2^68.945
outer steps at random, seven to a batch, 2^22 trials each. An exact filter, read
from two direct tables of carry-set masks on two words of the outer step, skips
every outer step that cannot hold a collision with an outcome of S9 (Lemma F9);
it passes 2^-9.6236 of uniform pairs of words. In a passing outer step the
pre-check of 9.7 serves the outcomes of S without loss (Lemma VP); the joint
solver of 9.4 returns every value of the internal word E3.h1 that meets the
conditions of an outcome of S and the guards (G7) and (G15); the generic solver
of 9.8 does the same for the outcomes of beta3 with (G7), (G15b) and (G20b); and
a certificate maps each value back to its trial and tests it. Together they find
exactly the trials of the outer step that complete the collision with an outcome
of S9, at a cost of at most 512 + 314,996,576 machine units for a passing outer
step whatever its words (Sections 9 and 11, Lemmas V, V9, VP, G7, G15, G7b,
G15b, G20b, RC, CV and CV9). Every budget is a halt and is charged at its bound;
no mean of any count enters the time bound. Two heuristics are declared: H1',
that the valid trials (t not zero) of U complete the collision with an outcome
of S9 at a rate of at least 70,943,656,228 * 2^-128 = 2^-91.954, five sevenths
of the model's rate for this prescription and these outcomes rounded down,
without clusters beyond a stated bound; and H4', that the two budgets of a run
suffice: of lanes whose word passes (2) and of passing outer steps. Under the
two the search succeeds with probability at least 0.39. The total charged time
is 241,046,662,574,423,655,669,972,046 machine units divided by 430, the final
step and the selection procedure of Section 12 included: 2^78.89125007..., below
2^78.8913. The search needs less than 2^39 bytes of memory, the direct tables of
the filter included; its two messages are shorter than 2^42 bytes each, and the
declared 2^44 bytes cover them, the code, the search and the selection
procedure, even all held at once (Section 12).

The rate in H1' is an assumption. Under the seven-word model of Section 13, with
Y4 uniform in the class, prescribing c1 in U multiplies by 2^10 the parts of
beta* and beta3 in the rate of the class: counting the nine outcomes of S9, the
rate is 2^10 * 96,993,280 = 99,321,118,720 times 2^-128 (10.1; Lemma S1, applied
to each of the two cubes). The figure 96,993,280 is the sum of the six exact
outcome counts of S of the participant's counting program, 67,633,152, printed
with its output in Section 17, and of the three exact parts of the outcomes of
beta3, 29,360,128 together, which GPT Sol derived from the participant's integer
records (answer AX 2.3) and which this package does not reprint. Whether the
trials of the construction realise that conditional law, to at least 5/7 of its
rate, is the part that is not proved, and it is declared as H1' for the union U
and S9; Lemmas S2 to S4 prove parts of it for Q*, and Lemma S8 states how weak
the dependence inside one outer step has to be. Participant measurements on real
counter trials reach events of probability about 2^-31.7 and agree with the
model for outcomes of beta* (Section 13); none of them touches beta3 or its
cube. No run reaches a collision at 32 bits.

No full 2-round collision is exhibited, and the search is far beyond feasible
computation. The declared experiment runs the search of 9.1 and 9.8 of this
package at toy scale on the root instance of the same construction: single
chunks of 55 and 63 bytes, compressed with counter 0 and flags 11, the instance
that the organizer's harness hashes (6.4, 9.2). An organizer experiment tests an
event on two complete digests, and the half-collision of the counter instance
lies in the chaining value of a chunk that is not the root, which the parent and
root compressions above it mix: no digest experiment can show it (6.4). Per
organizer seed the program runs 256 batches of seven outer steps of the search:
the sampler of the class, the widened filter of the nine outcomes, the two
counts and their budgets, the pre-check, the joint solver with (G7) and (G15) on
the outcomes of S, the generic solver with (G7), (G15b) and (G20b) on the
outcomes of beta3, and the certificate of every root with the cube, beta and eps
of its outcome; it returns the root-instance pair of its first passing outer
step, whose digests agree on the 128 masked bits. Its counts are the program's
own and the organizer does not check them; the layout on 64 registers and the
direct tables of the charge are proved allowances, and the program reads the
same masks from the automata of the filter (9.2, 9.8).

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
C0.a1. Arithmetic is modulo 2^32.

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

## 6. The root instance: trials, tests and the packed machine

**6.1 Trials.** A *context* is the six words of an outer step (C0.c1, C0.d1,
D3.d1, S15, S9, w5), a word X2, and everything that steps O and M compute from
them. The class and the sub-class defined next are sets of values of Y4. A
**trial** is a context and a member y of the sub-class; its messages A and B are
the output of steps O, M, Y, T, S2 and S3 for the context's seven words and y.
Only steps Y and T depend on y: the trials of one context differ in the four
message words w8..w11 and in nothing else of the message (Lemma T2 (c)). Step Y
does not read X2, so for one outer step and one member its ten names are the
same whatever X2 is.

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

**6.4 The root instance and the declared experiment.** Sections 4 to 6 build the
*root instance* of the construction: its messages are single chunks of 55 and 63
bytes, and the colliding compression is the root compression, with counter 0 and
flags 11 (Section 1). The claim of this package is made for the *counter
instance* of Sections 7 to 9, whose messages have 1024 t + 55 and 1024 t + 63
bytes and whose colliding compression is that of the last chunk, with counter t
and flags 3. The two instances share the six constants, Fact P, Lemmas L and H,
the class, Lemma N and the packed words of 6.5; the sub-class, rule A and Lemma
A belong to the root instance only and not to the search of this package. The
instances differ in the counter and the flags that the compression reads, and in
the order in which the construction solves the assignments of rounds 0 and 1
(Sections 4 and 8).

The declared experiment runs on the root instance, counter 0 and flags 11. An
experiment of the organizer's harness returns pairs of complete messages and
tests an event on their two digests, while the half-collision of the counter
instance is an agreement of four words of the chaining value of a chunk that is
not the root. The parent and root compressions above that chunk mix all eight
words, so the digests of a counter pair are not expected to agree on the masked
words, and on two counter pairs with t = 1 they do not (Section 7). No digest
experiment can show a half-collision of a non-root chunk's chaining value. In
the root instance the colliding compression is the root itself, so its
half-collision is an agreement of four digest words, which the organizer
recomputes.

- `union-search` runs, per organizer seed, the search of 9.1 with 9.8 on 256
  batches of seven outer steps, with the lines of steps CO and CT read at
  counter 0 and flags 11 (9.2), and returns the pair of its first passing outer
  step, built by step CT with the one c1 for which the counter word that step CT
  forces is 0. Theorem C, with 0 and 11 in place of t and 3, says that every
  returned pair agrees on digest words 0, 2, 5 and 7.

The experiment does not run the counter instance and does not measure a rate of
the counter search: at toy scale no root is expected, and on the root instance a
root is certified only when its forced counter word is 0.

**6.5 Packed words and the machine.** A packed word holds seven lanes of 36 bits
at bit offsets 0, 36, .., 216. A lane represents its value modulo 2^32; bits
32..35 are carry guards. A constant is placed in all seven lanes before the
batches that use it. Additions are single 256-bit additions. A rotation of every
lane by r is the five operations

    PROR(z, r) = ((z >> r) AND A_r) OR ((z << (32-r)) AND B_r)

with A_r selecting the low 32-r bits of every lane and B_r the next r bits; the
masks discard guard bits and bits shifted in from the neighbouring lane, so the
result is reduced below 2^32. With M = 2^32 - 1 in every lane, the complement of
the low 32 bits of a lane is an XOR with M, a difference x - y of a constant x
and a lane y is (y XOR M) + (x + 1), and subtracting a constant y is one
addition of the constant -y.

The lane layout, seven 36-bit lanes with reduction delayed to the rotations and
a five-operation masked rotation, follows the public ticket 2bf40fb on this
track, which uses it for a birthday search. What is evaluated in the lanes here
is different.

*The machine.* Costs are charged on a load/store machine with 16 registers: one
operation for every addition, XOR, AND, OR and shift of 256-bit words, for every
comparison and for every branch, so PROR = 5; one load every time a word is
fetched from memory or from a table into a register, and one store every time a
register is written to memory. Shift distances are fixed in the instruction.
Section 11 charges the search on the same machine with 64 registers and every
constant an immediate operand.

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
code). This is why the declared experiment runs on the root instance (6.4).

*Participant checks with the organizer's code.* In each of the following the
organizer's `verifier/blake3.py` was imported unchanged; they are participant
computations, which the organizer has not run. (1) For 2,000 trials of the
counter construction of Section 8 in 40 outer steps, 8 of them with outer words
0 or ffffffff, `_chunk_output` of the last chunk returned (IV, the block words,
t, 55 or 63, 3) for A and for B, and `_compress` returned the chaining value
that the participant's program computes, in 2,000 of 2,000; words 0, 2, 5 and 7
of the two chaining values were equal in all 2,000 and all eight words in none;
and 204,000 internal words of the construction were equal to a separately
written forward computation of the compression. (2) For five counter trials with
t = 1, 3, 3, 4 and 16,383, the complete messages F || A and F || B, with F a
string of t chunks of pseudorandom bytes, were hashed by `blake3(m, 2)`. In
each, the messages have 1024 t + 55 and 1024 t + 63 bytes; the code makes
exactly one compression with block length 55 or 63, and its inputs are (IV, the
block words, t, 55 or 63, 3); its chaining values agree on words 0, 2, 5 and 7
and not on all eight; the two digests differ; and when the output of that
compression of F || B is replaced by the output of the one of F || A, blake3
returns the digest of F || A, and the other way round. (3) A helper agent also
checked (b) in the same way for 25 values of t from 1 to 1,025, on 150 messages
and 75 pairs with a replaced output, all as the lemma says.

## 8. The counter construction

*Words and constants.* The construction has nine free words: the seven *outer
words* C0.d1, D2.a1, D2.b1, S11, S4, X9 and w6 (the program's `OUTER_WORDS`); a
member y of the class of 6.1 (Lemma Q), which becomes the value of Y4; and the
*inner word* c1, which becomes the third value of E1 on message A. The constants
are those of Section 4: X3, X7, X11 and X15, w4 = W4, w13 = W13, w14 = w15 = 0,
the four constant first values K2.a1, K2.d1, K2.c1 and K2.b1 of K2 given in step
O, and Y3, Y11 of Fact P. The compression reads three more values besides the
message and the IV. K3 reads the flags, here 3 (the line for K3.d1); K1 reads
v[13], here 0 (the line for K1.a1); and K0 reads the counter v[12], which is not
fixed in advance: the line for t solves K0's second assignment for it. The names
are those of Section 4.

*The cube Q*.* Q* is the set of the 2^21 words c with (c AND 0e09818b) =
02008000; the program names the mask and the value `QSTAR_MASK` and
`QSTAR_VALUE`. Member number j of Q*, for 0 <= j < 2^21, is the word whose bits
at the 21 positions where 0e09818b has a zero are the bits of j, in increasing
order of position .

*Members.* In Sections 8 to 12 a *member* is a member of the class of Lemma Q,
not of the sub-class of 6.1. Member number k of the class, for 0 <= k < 2^19,
is the Y4 whose e1 = Y3 + Y4 has the bits of k at the 19 positions where
03cf8303 has a zero, in increasing order of position, and Y4 = e1 - Y3. The
search of this package uses every member; it has no sub-class and no rule A.

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
for K3.d1 used. Otherwise the words w0 to w12 of the lines, with w4 = W4 and w13
= W13, and w14 = w15 = 0 form the block of A; A is the first 55 bytes of its
little-endian encoding, and B the first 63 bytes of that of the same words with
w4' = W4' and w5' = w5 + fffffff8 in place of w4 and w5, as in steps S2 and S3
of Section 4. F is the string of 1024 t zero bytes, and the two messages are F
|| A, of 1024 t + 55 bytes, and F || B, of 1024 t + 63 bytes. In the program the
lines of step CO are `LINES`, run by `scalar_outer`, and step CT with the two
blocks of step CS is `step_ct`; the program reads them at counter 0 and flags
11, on the root instance (9.2).

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
of trials that the rule t != 0 drops, one in 2^21 at most; it does not bound the
share of the collision mass that the dropped trial carries (10.3). In the
participant's checks the member with t = 0 was constructed by the inverse above
in 40 outer steps and rejected by the participant's program in 40 of 40; over
8,192 further outer steps it lay in Q* 4 times, against 4.0 expected, and was
rejected 4 times out of 4.

*The length of the messages.* Within one outer step the 2^21 members of Q* give
2^21 different values of t below 2^32 (Lemma IP); over 2,000 trials of the
participant's check t ran from 891,836 to 4,291,586,422 with a mean of log2 t
of 30.56. A pair found by the search has messages of 1024 t + 55 and 1024 t +
63 bytes, shorter than 2^42 bytes and about 2^41 on average. A small t cannot
be chosen: it is the value of a permutation of c1 at the member that the search
finds.

**The outer filter.** Number the seven outcomes of beta* whose tau ends in
5020a0 (10.1) j = 1 to 7 in the order of the table of 10.1: 175020a0, 185020a0,
275020a0, 285020a0, 385020a0, 675020a0 and 685020a0, the seven of entry 26ebba63
and of the program's `TAUS`. This search lists six of them, the set S = {1, 2,
3, 4, 5, 7}: all but 675020a0 (j = 6), and three outcomes of another difference,
beta3, with the widened filter of 9.8. In the hexadecimal masks below, with bit
j - 1 for outcome j, S is 5f. Beta* has seven more outcomes on the class, the
same seven with bit 14 of tau set (j = 8 to 14 of 10.1); this search does not
list them either. Let tau_j be the tau of outcome j, sigma_j = tau_j XOR
ROR(tau_j, 1) and theta_j = ROL(sigma_j, 12); all seven have eps = 6e21be55. For
an outer step put omega = Y3 + y + w8, with Y3 of Fact P, y the member of the
outer step and w8 the name of step CO; DY3 = Y3' - Y3 = fdb77cfd is that of
Section 6. For a word x:

- condition (1)_j holds for x when some word h gives
  (x + h) XOR (x + (h XOR eta)) = theta_j;
- condition (2)_j holds for x when some word f gives
  (x + f) XOR ((x + DY3) + (f XOR sigma_j)) = eps.

An outer step *passes* the filter when for some j in S both (1)_j holds for its Y9
and (2)_j holds for its omega. Y9 and w8 are names of step CO and y is drawn with
the outer words, so whether an outer step passes depends on the outer step alone
and on no c1.

**Lemma F (the outer filter; GPT Sol 6.1, answers AC and AN).** Fix an outer
step that does not pass the filter. Then no trial of the outer step, for any
word c1, has R = 0 with an E1 outcome in S. (A trial with R = 0 whose E1 outcome
is another outcome of beta* on the class may lie in a rejected outer step; the
search does not count it.)

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
the hypothesis. QED.

The lemma uses no law of the words: no uniformity, no independence and no
relation between h and f besides the two equations. It does not use the rule t
!= 0, and it holds for any list of outcomes (GPT Sol, answer AN 2), S among them.
The filter can pass outer steps that hold no success, since (1)_j and (2)_j are
solved with separate witnesses; it cannot reject an outer step that holds a
success with an outcome of S.

**The exact share (GPT Sol, answers AC, AN and AW; recounted by the
participant).** Let pi be the share of the 2^64 pairs (x1, x2) of words such
that for some j in S condition (1)_j holds for x1 and (2)_j for x2. Then

    pi = 18,289,159,183,466,496 / 2^64 = 279,070,422,111 / 2^48,

about 0.00099145731 = 2^-9.978162. With all seven outcomes j = 1 to 7 in place
of S the share is 20,504,986,129,465,344 / 2^64 = 312,881,258,079 / 2^48 =
2^-9.813176, the share of the filter of entry 26ebba63, which this search does
not use. Let pi_E be the share of the 2^32 words x for which (2)_j holds for
some j in S: pi_E = 233,715,456 / 2^32, about 0.054416120 = 2^-4.199822.

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
nonzero seven-bit mask m are 7,936 a_m under (1), a_m the second column, and
1,082,016 b_m under (2), b_m the fourth and the sixth columns:

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

No other nonzero seven-bit mask occurs; 134,896,128 words satisfy some (1)_j and
233,715,456 some (2)_j. Every mask of (2) in the table meets 5f, so the same
233,715,456 words satisfy (2)_j for some j in S. The sum of a_m b_n over the
pairs of masks m and n with m AND n AND 5f not zero is 2,129,896, and over all
pairs of intersecting masks it is 2,387,944. So the number of pairs that pass
for S is 7,936 * 1,082,016 * 2,129,896 = 18,289,159,183,466,496, and for all
seven 7,936 * 1,082,016 * 2,387,944 = 20,504,986,129,465,344 (the participant's
arithmetic on the table; GPT Sol's answer AW 3 gives the same 279,070,422,111
and 233,715,456). With the seven other outcomes of beta* on the class added, GPT
Sol's certificate of the fourteen-outcome filter (answer AN 2) gives
99,669,577,442,459,648 passing pairs, 2^-7.531997; that filter is not used here.

*The automata.* The program's `automaton` builds the subset construction above
as four byte tables: a state is the carry of x + DY3 (zero for (1)) and, per
outcome, the set of reachable carry pairs, four bits; the table of byte p maps a
state and byte p of x to the next state, and the table of the last byte maps to
the mask. `build_tables` builds the two automata once per run for ten outcomes,
the seven of the table above and the three of X3 of 9.8 with eps 6e61be55 in (2)
(`filter_targets`), and ANDs every entry of their last tables with the nine bits
of S9, so that every mask it reads is restricted to S9. With these targets the
construction has 1, 18, 43, 37 and 1, 3, 7, 13 states at the four byte
boundaries and tables of 25,344 and 6,144 entries. `look` runs an automaton on a
word with one table load per byte. The charged search reads instead the two
direct tables of 9.8, whose entries are these masks (Lemma TAB). The self-test
of 9.3 recounts from the program's own tables the passing pairs and the words
that pass (2), 18,289,159,183,466,496 and 233,715,456 for S and
23,384,160,813,285,376 and 305,100,224 for S9, and checks both automata against
brute force at 8 bits.

## 9. The counter search

**9.1 The algorithm.** The search lists the nine outcomes of S9, the six of S
and the three of X3, the outcomes of beta3 = 18d0e098 with tau 185020a0,
285020a0 and 385020a0 and eps 6e61be55, and its trials are the words c1 of the
union U of the cube Q* of beta* and the cube Q3 of beta3, 2^22 words (9.8). It
uses these constants (GPT Sol, answer AX 2.4): R9 = 96,993,280, the part of the
nine outcomes on the scale 2^-83 of 10.1; FACTOR = floor(5 * 2^10 * R9 / 7) =
floor(5 * 99,321,118,720 / 7) = 70,943,656,228, the factor of H1', five sevenths
of the conditional count of the nine outcomes on U rounded down (10.1, 10.3);
RUN_STEPS = ceil(0.49676 * 2^128 / (FACTOR * (2^22 - 1))) =
568,084,180,184,553,153,661, about 2^68.945, with 0.49676 = 12419 / 25000, so
that a run has 0.49676 expected listed good trials at the rate of H1' (10.4);
SHARE = 23,384,160,813,285,376, the number of pairs that pass the widened filter
for S9 (9.8), so that its share pi9 is SHARE / 2^64 = 2^-9.6236188; E_COUNT =
305,100,224, the number of words that pass the table of (2) for S9 (9.8); and
two budgets, each the expected count of its outer steps in a run under the
nominal shares of H4' times the margin 17/16, rounded up (GPT Sol, answer AX
2.4):

    E_BUDGET      = ceil(17 * RUN_STEPS * E_COUNT / 2^36)
                  = 42,876,990,928,602,462,880,  about 2^65.217;
    PASS_BUDGET   = ceil(17 * RUN_STEPS * SHARE / 2^68)
                  = 765,144,922,463,168,754,     about 2^59.409;

and RUN_BATCHES = ceil(RUN_STEPS / 7) = 81,154,882,883,507,593,381, about
2^66.138, the number of batches of seven outer steps (9.6). There is no solver
count and no solver budget: every passing outer step is charged the whole cap of
steps 2 and 3 (9.8, Section 11). The submitted program holds these constants and
its self-test compares them with the values printed here (9.3).

0. Before the batches, build the two direct tables of the widened filter (9.8),
   the table VMASK of the pre-check (9.7), the three transition arrays, the
   static row descriptors of the six outcomes of S and the statically written
   traversal of the joint solver with the guards (G7) and (G15) (9.4, 9.7,
   Section 11), and the descriptors of the three rows of X3 for the generic
   solver with (G7), (G15b) and (G20b) (9.8). None depends on an outer word.
1. For each of the RUN_BATCHES batches in turn, b = 0, 1, ..: draw eight fresh
   uniform 256-bit words R_0 to R_7. Lane i, for i = 0 to 6, is bits 36 i to
   36 i + 35 of a word (9.6). Lane i of batch b holds the outer step of number
   7 b + i if that number is below RUN_STEPS, which holds for all seven lanes
   except in the last batch, whose lanes 1 to 6 are not used. The *random
   word* of that outer step is the 256-bit word whose k-th 32-bit word, for k
   = 0 to 7, is the low 32 bits of lane i of R_k. Its first seven 32-bit words
   are the outer words C0.d1, D2.a1, D2.b1, S11, S4, X9 and w6. Its eighth
   word W gives the member y with e1 = Y3 + y = 030c0303 + (W AND fc307cfc),
   that is the member of the class whose 19 free bits of e1 (Lemma Q) are the
   bits of W at the same positions; its member number (Section 8) is these 19
   bits in increasing order of position. *Test (2):* run in all lanes at once
   on packed words (9.6) the lines of step CO that reach Y9 or omega, omega =
   Y3 + y + w8, and read the E table of 9.8 at omega, giving its mask of (2)
   for S9. A lane whose mask of (2) is zero ends its outer step there. *Q
   path:* then for each lane whose mask of (2) is not zero, in increasing
   order of i: advance the count of such lanes, the *E count*, and halt with
   failure when it exceeds E_BUDGET; else read the Q table of 9.8 at the Y9 of
   the lane and AND its mask with that of (2), giving the mask X of the outer
   step. If X is zero the outer step ends there. Otherwise the outer step
   *passes* the widened filter (9.8): advance the count of passing outer steps
   and halt with failure when it exceeds PASS_BUDGET; else compute on scalar
   words, from the eight words of the lane, the names of step CO that steps 2
   and 3 read. *Pre-check:* write X_S for the bits of X of the six outcomes of
   S, in the numbering of Section 8, and X_3 for those of the three outcomes
   of X3. Compute the word nu of 9.7 from Y9, y, C2.c1 and C2.b1 and T = X_S
   AND VMASK[nu]. If T and X_3 are both empty the outer step ends there (it
   holds no listed good trial, Lemmas VP and F9). Otherwise run steps 2 and 3
   for this outer step.
2. *Roots:* run the joint solver of 9.4 with the guards (G7) and (G15) of 9.7 on
   Y9, y and omega for every outcome of S whose bit is set in T, and the generic
   solver of 9.8 with the guards (G7), (G15b) and (G20b) for every outcome of X3
   whose bit is set in X_3. They return candidate roots, each a word h with the
   outcome of which it is a root: the joint solver at most 16 (9.4), the generic
   solver at most one for each leaf of its trees (9.8).
3. *Certificate:* for each returned root h, with its outcome j, in turn, at its
   leaf: compute c1 from h by the inverse of Lemma IP, Y14 = ROL(h,16) XOR (Y3 +
   y), Z = (Y14 + C2.c1) XOR C2.b1, Y6 = ROR(Z, 7), E1.a1 = Y6 + Y1 + w12, E1.d1
   = ROR(E1.a1 XOR Y12, 16) and c1 = Y11 + E1.d1, and t by the lines Y2, w0,
   K0.a1 and t of step CT. For an outcome of S the root is *certified* when the
   four one-word tests (Q), (A), (C) and (T) of Lemma RC hold (10.2): c1 in Q*,
   the bits of E1.a2 that tau_j prescribes, the c difference eps = 6e21be55, and
   t not zero. For an outcome of X3 it is certified when c1 AND 0e09818d =
   02008001, t is not zero, and E1 on A and on B (6.2) gives the XOR differences
   tau_j and eps = 6e61be55 of its a and c outputs (Lemma V9). For the first
   certified root, form F || A and F || B by steps CT and CS for its c1,
   evaluate blake3 of both in full, check that the two digests agree, output the
   pair and halt.
4. After the last batch, halt with failure.

The run halts with failure in exactly three ways, each a test on a count that
the algorithm keeps or on the batch number: the E count exceeds E_BUDGET, the
count of passing outer steps exceeds PASS_BUDGET, or the outer steps are
exhausted. So at most E_BUDGET lanes read the Q table and at most PASS_BUDGET
passing outer steps are rebuilt, pre-checked and run steps 2 and 3, which have
no budget of their own: the work of steps 2 and 3 is bounded in every outer step
that reaches them, whatever its words, by the cap of 9.8 (Section 11). So the
work of every run is bounded by the counts of Section 11, and a pair of messages
is formed and hashed at most once, for a certified root.

A trial is *valid* when its t is not zero; a valid trial with R = 0 is *good*; a
good trial is *listed* when c1 is in U and its E1 outcome, the triple of its
beta, tau and eps, is one of the nine of S9 (9.8, 10.1). A listed good trial is
found unless the run ends before its outer step is reached, by one of the two
budgets or by the output of another pair: its outer step passes the widened
filter by Lemma F9; for an outcome of S the pre-check keeps it by Lemma VP, it
satisfies (G7) and (G15) by Lemmas G7 and G15, and the joint solver returns its
E3.h1; for an outcome of X3 it satisfies (G7), (G15b) and (G20b) by Lemmas G7b,
G15b and G20b and the generic solver returns its E3.h1; and step 3 certifies it
(Lemmas RC, CV and CV9). Every certified root is the E3.h1 of a listed good
trial (Lemmas CV and CV9). A good trial that is not listed is not found, and
Section 10 does not count it; by the count of 10.1 beta* has eight more outcomes
on the class, 675020a0 and the seven with bit 14 of tau set, which carry
4,065,280 of its 71,698,432 (5.7 per cent) and are not listed, and no outcome of
beta3 outside X3 is listed. When the run outputs a pair, the pair is a collision
of two complete messages: the certified trial has R = 0 (Lemmas V, V9 and RC),
step 3 has checked both digests, and Lemma TR (c) says that R = 0 with the
half-collision of Theorem C gives equal digests.

*What the submitted program holds.* The submitted program (9.2) runs this search
on the root instance: the member of the class from the 19 free bits of the
eighth word; step CO compiled from its lines onto packed words of seven 36-bit
lanes; the two automata of the filter for ten outcomes with their last tables
restricted to S9, (2) in every lane and (1) on the Q path, which give the masks
of the direct tables (Lemma TAB, 9.8); the E and pass counts against the budgets
above; the pre-check of 9.7; the joint solver of 9.4 on the rows of T with the
guards (a) to (g), (G7), (G15), Lemma J0 and the guards at positions 25 and 29;
the generic solver of 9.8 on the rows of X_3 with (G7), (G15b) and (G20b); and
step 3 for every root with the cube, beta and eps of its outcome, by evaluating
E1 on A and on B, which Lemmas RC and V9 make equivalent to the tests above. Its
steps CO and CT read counter 0 and flags 11, so its trials are trials of the
root instance, where a root is certified only when the counter word that step CT
forces is 0. It charges each row with the units of Section 11 as a ledger on
Python integers; it does not run the 64-register schedule of Section 11, so its
counts are not counts of that machine.

**9.2 The submitted program.** The program of the declared experiment,
experiments/halfsearch.py, is one Python 3 file that uses only the standard
library and imports no BLAKE3 library. It runs the search of 9.1 with 9.8 on the
root instance only: one chunk, counter 0 and flags 11, the instance that the
organizer's harness hashes. It does not run the counter instance (flags 3,
counter t), on which the claim is made. It was adapted by helper agents of the
participant from the program of our entry ecd2496c, with the widened filter,
(G15), the generic solver with (G7), (G15b) and (G20b), the certificate of the
union and the ledger of this package.

*One trial.* Per organizer seed the program runs 256 batches, 1,792 outer steps,
whose eight words come from SHAKE-256 of the text "halfsearch batch", the seed
and the batch number (`draw`). In order: (1) step 1 of 9.1: the whole-class
sampler (`member_y`); step CO compiled from its lines onto packed words of seven
36-bit lanes (`compile_batch`, 9.6); the automaton of (2) on omega in all seven
lanes, then the automaton of (1) on Y9 (the Q path), with masks of ten outcomes
restricted to S9 (`build_tables`, `look`); an outer step passes when X is not
zero; the E and pass counts against E_BUDGET and PASS_BUDGET, which a trial
never reaches (`iter_passes`). (2) The pre-check of 9.7: nu by (V), then T = X_S
AND VMASK[nu]; the bits X_3 are never dropped (`pipeline`). (3) Step 2: for the
rows of T the joint solver of 9.4 (`row_setup`, `traverse`, `solve`) with the
guards (a) to (g), (G7), Lemma J0, the guards at positions 25 and 29 and, at
position 15, the test and the prescribed bit of (G15) (`g15_value`); for the
rows of X_3 the generic solver of 9.8 (`xsolve`) from bit 0 with both guesses of
a20, at most one child at a prescribed position, (G7) at position 7, (G15b) at
position 15 and (G20b) at position 20, which reads the selected array with the
desired bit h[8]. At every leaf (J1) to (J3) are checked as words, with the eps
and mu of the outcome. (4) Step 3 for every root (`certificate`): c1 by the
inverse of Lemma IP, then the tests in this order: c1 in the cube of its beta,
the counter word t = 0 of this instance, the names of steps CO and CT equal to
the 2-round compression, (J1) to (J3) equal to E3 on A and B, the E1 differences
tau_j, eps_j and beta of the outcome, and equal chaining values (here, equal
digests). A root is counted as certified only when every test holds.

*The ledger.* The program charges machine units with the allowances of Section
11: 341 per batch (its compiled lines counted, the automaton of (2) replaced by
the 41 of the direct-table lane tests, 9.8), 13 per lane whose mask of (2) is
not zero, 512 per passing lane; for the rows of T, 1,024 once, 2,304 per family,
1,408 per row, 20 per forced node, 4 more per selected node, 48 per free node,
64 more per node at position 15 and 200 per leaf; for each row of X_3, 8,576,
512 per node visited, 64 more per node at positions 7, 15 and 20 and 8,192 per
leaf. It counts the nodes and leaves that it visits and tests the units of every
passing outer step against 17,504 for T, against the row cap C_row of each row
of X_3 and against 314,979,072 for the rows of X_3 together (9.8); a test that
fails is counted as `over_cap`. The time bound of Section 11 does not use these
counts: it charges the whole cap on every passing outer step.

*The returned pair.* The pair of a trial comes from its first passing outer
step, or from its first outer step if none passes. Step CT is run with the one
c1 for which the counter word that step CT forces is 0, from Lemma IP: K0.a1 =
ROL(K0.d1, 16), w0 = K0.a1 - IV[0] - IV[4], Y2 = w0 + C2.a1 + C2.b1, Y14 =
ROR(Y2 XOR C2.d1, 8), E3.h1 = ROR(Y14 XOR (Y3 + y), 16), and c1 by the inverse
of Lemma IP (`c1_t0`). The program asserts that step CT then gives t = 0. The
pair is a 55-byte A and a 63-byte B, built from the lines of steps CO and CT,
not by the compression. At counter 0 and flags 11 the counter, v[13], the flags
and the block length difference are as in the proof of Theorem C (ii), with 0
and 11 in place of t and 3, and the colliding compression is the root, so its
output words are the digest words: every such pair agrees on digest words 0, 2,
5 and 7.

*Observations.* Fourteen per trial, the program's own counts, which the
organizer records as untrusted and does not recompute: outer_steps, passes,
s_steps (passing outer steps with T not empty), x3_steps (with X_3 not empty),
x3_rows (rows of X3 run), solver_units and solver_units_max (the ledger of steps
2 and 3, in all and in the largest outer step), over_cap, units (the outer
charges and solver_units), roots, certified, verify_fail (a passing lane whose
packed Y9 or omega differs from step CO on scalar words), halted and pair_step.

**9.3 The self-test.** The command `python3 experiments/halfsearch.py --selftest
N [seed]`, outside the organizer protocol, runs these checks and exits with
status 0 only when all hold: the constants of 9.1 against the values printed
there; the two automata of the ten outcomes against brute force on all 256 words
at 8 bits; from the program's own tables, the passing pairs and the words that
pass (2), 18,289,159,183,466,496 and 233,715,456 for S and
23,384,160,813,285,376 and 305,100,224 for S9 (Section 8, 9.8); that no mask of
(1) holds the bits of X3 for 185020a0 and 285020a0 together (9.8); the static
trees of the three rows of X3, (N, L, n_7, n_15, n_20) = (11,372, 4,096, 16, 64,
128), (22,668, 8,192, 16, 128, 256) and (22,668, 8,192, 16, 128, 256), and their
caps C_row (9.8); Lemma G20b on each row of X3 for every value of pf = f AND
sigma, through which alone (J2) reads f (e2' = e2 + DY3 + sigma - 2 pf): the
values for which some e2 meets (J2), found bit by bit over the carry, 48, 192
and 96 of them, all have bit 20 equal to 0, and with g[0] = 0 every solution of
(J3) at bits 0 and 1 has h2[0] = 0 (9.8); every lane of N * 64 / 7 batches
against step CO on scalar words, every packed sum below 2^36; two halt drills,
which reduce E_BUDGET to 3 and PASS_BUDGET to 0 and must halt at the fourth E
lane and at the first pass; the batch counted at 424 with the automaton and
charged 341; and, for N cases from SHAKE-256 of the seed, the mask of (1)
against a bit-serial decision, step CT against the 2-round compression, the
inverse of Lemma IP, (J1) to (J3) against E3 on A and B, the pair with t = 0 and
its half-collision at counter 0 and flags 11, the generic traversal with (G20b),
without (G7) and (G15b), on a planted word (Q, y, E and h from the seed, bit 8
of E set so that e2[8] = h[8], sigma and eps the targets of (J1) and (J2) that h
meets: h must be among its leaves that meet both), and (G7) with (G15) on words
c1 of Q*, and (G7) with (G15b) on words c1 of Q3, that have Z[22] = 0 and Z[23]
= 1 (Lemmas G7, G15, G7b and G15b). With N = 200 and the seeds 1, 3 and 7 every
check holds: 200 of 200 planted words with each seed, and, with seed 7, 374 of
374 words of Q* and 413 of 413 words of Q3 with Z[22] = 0 and Z[23] = 1 meet
their two guards. These are participant checks; the organizer does not run them.

**9.4 The joint solver (GPT Sol, answers AE, AF, AI, AL, AO and AR).** Fix a
passing outer step and write Q = Y9, y for its member, E = omega = Y3 + y + w8
and E' = E + DY3; x[i] is bit i of a word x, bit 0 the lowest, and maj is the
majority of three bits. Put e1 = Y3 + y and b = e1[2], u = e1[21] and v =
e1[26], three bits that are free in the class (in the sub-class of entry
26ebba63, u = v = 0). For an outcome j of beta* (10.1) put sigma = sigma_j and
theta = theta_j (Section 8), eps = 6e21be55, gamma = eta XOR theta, D = (sigma
XOR eps) AND 7fffffff, kappa = sigma XOR eps XOR E XOR E' and mu = ROR(eta XOR
eps, 8) = 9aed22bd. For a word h put g = Q + h, f = ROR(y XOR g, 12), e2 = E +
f and h2 = ROR(h XOR e2, 8): for E3.h1 = h these are E3.g1, E3.f1 and E3.e2 of
step CT and the d output of E3 on message A (6.2). The *static descriptor* of
outcome j holds sigma, theta, gamma, D and the positions of its constants and
guards; the static descriptors of the six outcomes of S depend on no outer word
and are formed once per run.

*Joint roots.* A word h is a *joint root* of outcome j when

    (J1)  (Q + h) XOR (Q + (h XOR eta)) = theta,
    (J2)  (E + f) XOR (E' + (f XOR sigma)) = eps,
    (J3)  (g + h2) XOR ((g XOR theta) + (h2 XOR mu)) = tau_j.

(J1) and (J2) are the conditions (1)_j and (2)_j of Section 8, with the two
witnesses tied by f = ROR(y XOR (Q + h), 12). By (J1) theta is a function of h,
and then so is the left side of (J3); the seven values of tau are different,
so no word is a joint root of two outcomes. There is no rule A: a joint root is
any word that satisfies (J1) to (J3).

*Carries.* Write u[i] and u'[i] for the carries into bit i of Q + h and of Q +
(h XOR eta), and a[k] and a'[k] for those into bit k of E + f and of E' + (f
XOR sigma), all 0 into bit 0. Bit by bit, (J1) holds exactly when u'[i] = u[i]
XOR gamma[i] for every i, and (J2) exactly when a'[k] = a[k] XOR kappa[k] for
every k. Bit i of h gives g[i] = Q[i] XOR h[i] XOR u[i] and bit k = (i + 20)
mod 32 of f, f[k] = y[i] XOR g[i]. So the solver chooses h from bit 0 to bit 31
and runs both pairs of additions along it: those of (J1) on bits 0 to 31, and
those of (J2) on bits 20 to 31 and then 0 to 19. The carry a[20] is not known
at the start; it is guessed for the constants of (a) below, and the check of
(J2) as a word at each leaf enforces that bits 0 to 19 give the right carry
into bit 20 (one traversal, below). At a bit k < 31 with D[k] = 1, the
*prescription* of f[k] is f[k] = E[k] XOR sigma[k] XOR kappa[k+1] if a[k] =
E[k], and f[k] = E'[k] XOR kappa[k+1] otherwise: from carries a[k] and a[k] XOR
kappa[k], it is the only value of f[k] that gives the carries into bit k + 1
the difference kappa[k+1] (Lemma S5).

*The phase equations (GPT Sol, answer AO 5 and 6.1).* The participant's
counter, run on the class with its E3 count split by the pattern of h on the
sixteen bits 0 to 3, 6 to 13, 16, 17, 24 and 25 and by (b, u, v), records for
each of the eight values of (b, u, v) every pattern that occurs in a solution
of E3 with an outcome of beta* (records of the participant, not in the
package). GPT Sol checked every recorded pattern against

    h[0] = 0,  h[1] = 1,  h[2] = 1 XOR b,  h[10] = b,  h[16] = h[17] = 0,
    h[11] = 1 XOR h[3],  h[24] = h[3] XOR h[12] XOR u                   (PHASE)

and found no violation in any of the eight cells, whose sets have 88, 88, 108,
132, 108, 132, 88 and 88 patterns in the order b + 2u + 4v. Each of the fourteen
outcomes of beta* on the class has an E1 count L_j > 0 that depends neither on y
nor on h, so a zero count outside (PHASE) means that no joint root of any of
them, the six of S among them, violates (PHASE). The equations are
consequences of the count, which the solver uses as guards; they are not a rule
that drops members or solutions.

*The parity certificate (GPT Sol, answer AR 1).* Call the outcomes j = 1 to 7,
whose tau ends in 20a0, the *old rows*, and j = 8 to 14, whose tau ends in 60a0
and has bit 14 set, the *new rows*; a row is also named by the first three
hexadecimal digits of its tau. Every joint root h of outcome j, for y in the
class, satisfies

    h[6] XOR h[13] XOR h[25] = u XOR tau_j[14],                        (P*)

that is h[6] XOR h[13] XOR h[25] = u on the old rows and u XOR 1 on the new
rows. This search lists only the old rows, on which (P*) reads h[6] XOR h[13]
XOR h[25] = u; the certificate is stated for all fourteen rows as it was
proved. The proof is an exact finite count. The count N3_j of 10.1 counts the
quadruples (Y4, E3.h1, Y9, w8), Y4 in the class, that meet the E3 conditions of
outcome j, and by the proof of Lemma V (10.2) these are exactly the quadruples
whose E3.h1 is a joint root of outcome j for Q = Y9, y = Y4 and E = Y3 + Y4 +
w8. GPT Sol split every N3_j by the phase (b, u, v) of Y4 and by the parity pi
= h[6] XOR h[13] XOR h[25] of the root. The split is a sum of nonnegative
integers over an exact enumeration of submasks, through the identity (z XOR
m) - z = m - 2 (z AND m) modulo 2^32 and a carry recurrence with two states in
integers, in coordinates of E3 that are a bijection of the counted quadruples;
nothing is sampled. With a = 24, 16, 4, 24, 32, 1 and 6 for the rows 175, 185,
275, 285, 385, 675 and 685:

| rows | phases (b, u, v) with a nonzero count | count in each such phase | pi | count with the other pi |
| --- | --- | ---: | --- | ---: |
| old, all seven | all eight | a * 2^49 | u | 0 |
| new 185, 285, 385, 685 | u XOR v = 1 | a * 2^47 | u XOR 1 | 0 |
| new 175, 275, 675 | u XOR v = 1 and b = 1 | a * 2^47 | u XOR 1 | 0 |

Every other cell has count 0. Every joint root adds at least 1 to the cell of
its phase and its parity, so a cell of count 0 holds no root at all: (P*) holds
for every joint root of the fourteen outcomes on the whole class, pointwise and
not on average, and it drops no member and no root. The cells add up to the
fourteen N3_j of 10.1 exactly: 8 * a * 2^49 = a * 2^52 on the old rows, 4 * a *
2^47 on the new rows 185, 285, 385 and 685, and 2 * a * 2^47 on the new rows
175, 275 and 675 (checked by a helper agent of the participant). In the phase b
= 1, u = 0, v = 1, the 2^16 members of the class with e1 AND 07ef8307 =
070c0307, a separate exact count of a helper agent of the participant, with the
function N3_count of the counting program of Section 17 and the parity as one
more condition, gives all fourteen counts with pi = 0 on the old rows, pi = 1
on the new rows and the count 0 with the other pi, as the table says. The cells
of the other seven phases are GPT Sol's evaluation and were not re-run by the
participant. The count shows as well that a new row has no joint root when u =
v, and a new row 175, 275 or 675 none when b = 0; the search of this package
lists no new row.

*The guard on the third addition (GPT Sol, answer AR 6.1).*

**Lemma J0.** Every joint root h of every one of the seven outcomes has
h2[0] = 0, that is h[8] = e2[8].

Proof. For all seven outcomes tau_j[0] = tau_j[1] = 0, theta_j[0] =
theta_j[1] = 1 and gamma[1] = gamma[2] = 0, and mu[0] = 1, mu[1] = 0. By
(PHASE) h[0] = 0 and h[1] = 1. In (J1) both carries into bit 0 are 0. Since
eta[0] = eta[1] = 1 and gamma[1] = 0, the carry Q[0] AND (h[0] XOR 1) = Q[0] of
the second addition into bit 1 must equal the carry Q[0] AND h[0] = 0 of the
first, so Q[0] = 0 and g[0] = 0; since gamma[2] = 0, the carry maj(Q[1], 0, 0)
= 0 of the second addition into bit 2 must equal the carry maj(Q[1], 1, 0) =
Q[1] of the first, so Q[1] = 0 and g[1] = 1. Both additions of (J3) have carry
0 into bit 0. At bit 0, g + h2 adds 0 and h2[0], with sum bit h2[0] and carry 0
out; (g XOR theta) + (h2 XOR mu) adds 1 and h2[0] XOR 1, with sum bit h2[0] and
carry 1 XOR h2[0] out. At bit 1, g + h2 adds 1, h2[1] and 0, with sum bit 1 XOR
h2[1]; the other adds g[1] XOR theta[1] = 0, h2[1] XOR mu[1] = h2[1] and 1 XOR
h2[0], with sum bit h2[1] XOR 1 XOR h2[0]. (J3) at bit 1 requires the XOR of
the two sum bits, which is h2[0], to be tau_j[1] = 0. So h2[0] = 0, and h2[0]
is bit 8 of h XOR e2. QED. The zero carries into bit 0 are those of addition
modulo 2^32; nothing is guessed. The participant checked the bits that the
proof reads for all fourteen outcomes of beta* on the class, the six of S among
them.

e2[8] is produced at position i = 20 of the traversal (k = 8): e2[8] = E[8] XOR
f[8] XOR a[8] with f[8] = y[20] XOR Q[20] XOR h[20] XOR u[20], and every term
but h[20] is known when position 20 is reached, h[8] among them. So Lemma J0 is
a forward guard that sets h[20] = h[8] XOR E[8] XOR a[8] XOR y[20] XOR Q[20]
XOR u[20]. It holds for every joint root, so no root is lost, and position 20,
which no constant and no carry prescribes on any row, is no longer free.

*The constants and guards of an outcome.* For y in the class, every joint root
of outcome j has the following values, which the solver computes from Q, y, E
and the outcome before it branches, or checks during the traversal (GPT Sol,
answers AE 2.1, AF 1.2, AN 6, AO 6.1 and AR 2 and 6.1). Every member of the
class has y[0] = 0, y[1] = 1 and bits 16 to 19 of y equal to 0, 0, 1, 0, so
f[20] = f[21] = 0, bits 4 to 7 of f are the constant 2, the carry u[20] is
Q[19], and the first addition is reset as in the sub-class.

(a) *The carry into bit 22.* For each guess a[20] = 0 and a[20] = 1, with
a'[20] = a[20] XOR kappa[20], run bits 20 and 21 of both additions of (J2) with
f[20] = f[21] = 0, and keep the guess only if a'[21] = a[21] XOR kappa[21] and
a'[22] = a[22] XOR kappa[22]. If no guess is kept, the outcome has no joint
root. Two kept guesses have the same carries into bit 21, and so into bit 22:
all seven outcomes have sigma[20] = sigma[21] = 1, eps[20] = 0 and eps[21] = 1,
and the cases E[20] = E'[20], E[20] = 0 with E'[20] = 1, and E[20] = 1 with
E'[20] = 0 give, in turn, at most one guess that passes bit 21, equal carries
into bit 21 for both guesses, and at most one guess that passes bit 22. Write
a[22] for the common carry.

(b) f[22] is its prescription (D[22] = 1). If gamma[3] = 0, then D[23] = 1 and
f[23] is its prescription; if gamma[3] = 1, f[23] = 1 XOR Q[3] XOR y[3]. Run
bits 22 and 23 of (J2); if a'[23] is not a[23] XOR kappa[23] or a'[24] is not
a[24] XOR kappa[24], the outcome has no joint root. This gives a[24].

(c) h[0] = 0, h[1] = 1 and u[2] = 0; h[2] = y[2] XOR f[22] XOR Q[2], and the
outcome has no joint root unless h[2] = 1 XOR b; u[3] = maj(h[2], Q[2], 0);
h[3] = y[3] XOR f[23] XOR Q[3] XOR u[3] and u[4] = maj(h[3], Q[3], u[3]); h[10]
= b and h[11] = 1 XOR h[3]; u[11] = maj(h[10], Q[10], Q[9]) if gamma[10] = 0
and u[11] = Q[10] if gamma[10] = 1; u[12] = maj(h[11], Q[11], u[11]).

(d) f[0] is its prescription with a[0] = 0 (D[0] = 1), and a[1] = maj(E[0],
f[0], 0); h[12] = y[12] XOR f[0] XOR Q[12] XOR u[12], u[13] = maj(h[12], Q[12],
u[12]) and h[24] = h[3] XOR h[12] XOR u.

(e) Bit 16 of h2 is 0, so f[24] = h[24] XOR E[24] XOR a[24]; h[4] = y[4] XOR
f[24] XOR Q[4] XOR u[4] and u[5] = maj(h[4], Q[4], u[4]). Run bit 24 of (J2);
if a'[25] is not a[25] XOR kappa[25], the outcome has no joint root. f[25] is
its prescription (D[25] = 1), a[26] = maj(E[25], f[25], a[25]) and h[5] = y[5]
XOR f[25] XOR Q[5] XOR u[5].

(f) Bits 6, 13, 25 and 26 depend on the kind of the outcome; (P*) is used on
every row. The outcomes of S are old rows of two kinds (675020a0, an old row that
this search does not list, is described with them).

- *Low old rows, 175020a0, 275020a0 and 675020a0:* if E[1] = a[1], the carry
  into bit 2 is E[1], f[2] is its prescription (D[2] = 1) and e2[2] = E[2] XOR
  f[2] XOR E[1]; otherwise the outcome has no joint root if kappa[2] = 1, and
  e2[2] = E[2] XOR kappa[3] if kappa[2] = 0. Then h[26] = 1 XOR h[2] XOR e2[2]
  XOR Q[26] XOR Q[25], f[26] = h[26] XOR E[26] XOR a[26] and h[6] = f[26] XOR
  y[6] XOR gamma[7]. By (P*), h[25] = h[6] XOR h[13] XOR u: a forward guard,
  set once bit 13 of h is chosen.
- *High old rows, 185020a0, 285020a0, 385020a0 and 685020a0:* h[25] = e2[1]
  (answer AE 2.1), where e2[1] = E[1] XOR f[1] XOR a[1] and f[1] = y[13] XOR
  Q[13] XOR h[13] XOR u[13]. With (P*), h[6] = h[13] XOR h[25] XOR u = y[13]
  XOR Q[13] XOR u[13] XOR E[1] XOR a[1] XOR u, in which h[13] cancels: h[6] is
  fixed by (c) and (d), which give u[13] and a[1]. The guard of position 25 is
  then h[25] = h[6] XOR h[13] XOR u, the same as h[25] = e2[1]. h[26] = e2[26]
  (bit 18 of h2 is 0), and e2[26] is given by position 6, whose value is now
  fixed, so h[26] is a constant of the row.

(g) h[16] = h[17] = 0, h[18] = 1 XOR Q[18], h[19] = Q[19], and, if gamma[7] =
1, h[7] = 1 XOR gamma[8] XOR h[6], now a constant on every row.

On every row h[29] = 1 XOR e2[29] (bit 21 of h2 is 1), where e2[29] is known
once bit 9 of h is chosen, and h[20] is set by Lemma J0. These are the
*constants and guards* of the outcome. On every row h[0] to h[6] are fixed
before the traversal; the guards that read bits chosen during the traversal are
those of position 20 (every row), position 25 (the old rows) and position 29
(every row). In entry 26ebba63 the parity h[25] = h[6] XOR h[13] was a
condition of rule A on the sub-class; here (P*) is not a rule but a consequence
of the count of the class, true of every joint root.

*One traversal.* Every carry guess a[20] that (a) keeps reaches, after the
constants h[0] to h[6], the same state: the same bits h[0] to h[6], the same
carries u[7] and a[27], and the same e2[26]; the values e2[20] and e2[21],
which depend on the guess, are not used by any guard. So the solver walks bits
0 to 6 under both kept guesses with the tests of (a), (b) and (e), then drops
the guesses and starts one depth-first traversal for each searched outcome at
depth 7 from that state, and checks (J1), (J2) and (J3) as words at each leaf,
which enforces the closure of the carries that the guess stood for (GPT Sol,
answers AO 2 and 6.1 and AR 2). Every joint root survives a guess and reaches
this common state, and a single traversal over the bits of h reaches every h at
most once.

*Transitions.* For each position i = 7, .., 31, with k = (i + 20) mod 32, each
pair (u[i], a[k]) of incoming carries and each value v of h[i], put g[i] = Q[i]
XOR v XOR u[i], u[i+1] = maj(Q[i], v, u[i]) and u'[i+1] = maj(Q[i], v XOR
eta[i], u[i] XOR gamma[i]), and require u'[i+1] = u[i+1] XOR gamma[i+1] if i <
31; put f[k] = y[i] XOR g[i], e2[k] = E[k] XOR f[k] XOR a[k], a[k+1] =
maj(E[k], f[k], a[k]) and a'[k+1] = maj(E'[k], f[k] XOR sigma[k], a[k] XOR
kappa[k]), and require a'[k+1] = a[k+1] XOR kappa[k+1] if k < 31. A value that
passes is an arc to the pair (u[i+1], a[k+1]), or to (u[i+1], 0) if k = 31,
since both carries into bit 0 of (J2) are 0 (kappa[0] = 0: E'[0] differs from
E[0], eps[0] = 1 and sigma[0] = 0 for all seven outcomes); the arc records v
and e2[k]. The *descriptor* of a position is 14 bits: Q[i], y[i], E[k], E'[k],
eta[i], gamma[i], sigma[k], kappa[k], gamma[i+1], kappa[k+1], whether the
position has a constant and its value, and whether i = 31 and k = 31 (GPT Sol,
answer AI 1). The solver reads the arcs from three arrays built once per run
(answer AR 6.2), each entry computed by the relation above, which is the same
relation and not an approximation; an arc is five bits, the next carry pair,
h[i], e2[k] and a validity bit:

| array | key | words | entry |
| --- | --- | ---: | --- |
| forced | descriptor and carry pair | 2^16 | the one passing arc, or invalid |
| dual | descriptor and carry pair | 2^16 | both arcs, packed in one word |
| selected | descriptor, carry pair and a desired bit | 2^17 | the passing arc whose e2[k] is the desired bit, or invalid |

A position with a constant reads the forced array with the constant in its
descriptor. A position i < 31 with gamma[i] = 1, or with k < 31 and D[k] = 1,
has at most one passing value by Lemma S5 and reads the forced array as well. A
position with a guard on bits chosen during the traversal, 25 on the old rows
and 29 on every row, reads the forced array with the value of the guard written
into the constant field of its key: 1 XOR e2[29], from the saved bit e2[29],
and h[6] XOR h[13] XOR u, from bit 13 of the prefix of h. Position 20 reads the
selected array with the desired bit h[8] (Lemma J0); as e2[8] changes with
h[20], at most one arc has it. A free position (below) reads the dual array. So
a position that is not free has at most one child.

*The search.* From the common state at depth 7, search depth first over the
positions 7 to 31: a node at depth d has a child at depth d + 1 for each arc of
position d from its carry pair that meets the guards of the position. A node at
depth 32 is a *leaf*; it gives a root when its h satisfies (J1), (J2) and (J3)
as words. The root is returned with the outcome j.

*Counts.* Call a position i >= 7 *free* when it has no constant and no guard,
gamma[i] = 0 or i = 31, and D[(i + 20) mod 32] = 0, and *prescribed* otherwise.
For a row with the set F of free positions put n_i = 2^(the number of free
positions p with 7 <= p < i), for i = 7, .., 32. A traversal of the row has at
most n_i nodes at depth i: at most the sum of n_i over the prescribed positions
*forced* nodes, the sum over the free positions *free* nodes, n_20 *selected*
nodes among the forced ones (position 20 is prescribed on every row, by Lemma
J0), and n_32 = 2^|F| leaves (GPT Sol, answer AR 6.5; recomputed by the
participant from the free positions):

| tau | free positions | forced nodes | free nodes | selected nodes | leaves |
| --- | --- | ---: | ---: | ---: | ---: |
| 175020a0 | 13, 15, 30 | 72 | 7 | 4 | 8 |
| 185020a0 | 13, 15, 30 | 72 | 7 | 4 | 8 |
| 275020a0 | 9, 13, 15, 30 | 140 | 15 | 8 | 16 |
| 285020a0 | 9, 13, 15, 30 | 140 | 15 | 8 | 16 |
| 385020a0 | 9, 13, 15, 30 | 140 | 15 | 8 | 16 |
| 675020a0 | 13, 15, 30 | 72 | 7 | 4 | 8 |
| 685020a0 | 13, 15, 30 | 72 | 7 | 4 | 8 |

Against the solver with the phase guards alone (GPT Sol, answer AO 6.2),
position 20 is no longer free on any row (Lemma J0), and (P*) fixes position 25
on the low rows and position 6 on the high rows; no position becomes free. These
are counts of the static trees: an arc that fails a carry test or a guard only
removes nodes, and the trees that occur may be smaller. The guard (G7) of 9.7
fixes position 7 on every row before the traversal (GPT Sol, answer AX 1.1), so
position 7 is free on no row: the table gives the trees of the solver with (G7),
in which the rows 175020a0, 285020a0 and 685020a0 have lost the free position 7
that they have without it (there 142, 278 and 142 forced nodes and 16, 32 and 16
leaves). The row 675020a0 is not in S, and this search does not build its tree.

*The trees with the guards (G7) and (G15).* The guard (G15) of 9.7 prescribes
position 15, which is free on every row of S with (G7) (GPT Sol, answer CF 7.2).
With both guards the rows 175020a0, 185020a0 and 685020a0 have the free
positions 13 and 30, 42 forced nodes, 3 free nodes, 2 selected nodes, 2 nodes at
position 15 and 4 leaves, and the rows 275020a0, 285020a0 and 385020a0 the free
positions 9, 13 and 30, 80 forced nodes, 7 free nodes, 4 selected nodes, 4 nodes
at position 15 and 8 leaves (the counts of the table's rule; a node at position
15 is a forced node). These trees with (G7) and (G15) are the trees of the
solver of this package.

The outcomes searched in an outer step that reaches the solver have their bits
set in T, a subset of the mask of Y9 under (1) and of S. By the certificate of
Section 8 every nonzero mask under (1) is one of the twelve nonzero seven-bit
masks of its table, and each of these is a subset of {275020a0}, {175020a0,
675020a0}, {285020a0, 385020a0} or {185020a0, 385020a0, 685020a0}. So the
searched outcomes are among the rows of one of these four sets restricted to S:
{275020a0}, {175020a0}, {285020a0, 385020a0} and {185020a0, 385020a0, 685020a0}.
With (G7) and (G15) these have 1, 1, 2 and 3 rows; (80, 7, 4), (42, 3, 2), (160,
14, 8) and (164, 13, 8) forced, free and selected nodes; 4, 2, 8 and 8 nodes at
position 15; and 8, 4, 16 and 16 leaves. A leaf gives at most one root. So an
outer step has at most 3 searched outcomes of S, 16 leaves and 16 roots,
whatever its words (GPT Sol, answers AT 1, AW 2, AX 1.1 and CF 7.2).

*Families.* Within one of the four sets the rows fall into *families* by two
marks: low row (175, 275, 675) or high row (185, 285, 385, 685), and the bit
gamma[10] (on the class the new rows, which this search does not list, would
form families of their own). gamma[3] is 0 on the low rows and 1 on the high
rows, gamma[10] is 1 on the rows 675 and 685 and 0 on the others, and sigma[20]
to sigma[26] and sigma[0] to sigma[3] are the same on all low rows and on all
high rows; gamma[10] fixes the reset of u[11] in (c). So the formulas of (a) to
(e) and the walks of bits 0 to 5 under both guesses are the same for the rows of
a family and are evaluated once per family (GPT Sol, answer AR 6.4). Restricted
to S the four sets have 1, 1, 1 and 2 families, and at most two rows of a set
share a family. gamma[7] can differ within a family, so bit 6 and its outgoing
carries, h[6], h[7] and h[26] are computed for each row: no prefix of seven bits
is shared.

*What is proved and by whom.* The phase equations, the guards of (c), (d) and
(e), the single traversal and the common state are GPT Sol's (answers AO 5, 6.1
and 6.2 and AR 2), on the constants of answers AE 2.1, AF 1.2 to 1.4 and AN 6
and the transition relation of answer AI 1; the parity certificate (P*), Lemma
J0, the guards of (f) with (P*), the three arrays, the families and the counts
of the static trees are GPT Sol's answer AR (1, 2 and 6.1 to 6.5); the
restriction of the solver to the outcomes of S, with the four sets above, is its
answer AW 2, the same solver visiting only the outcomes of T, with the same
proofs; the guard (G7), with its trees, is its answer AX 1; and the guard (G15),
with its trees above, is its answer CF 7, with the row-set caps 8,544, 6,656,
13,760 and 17,504 of Section 11 (answers CF 7.2 and CD 11). The participant
recomputed the free positions, the node, leaf and selected counts of the table
and of the four sets, the families, the bits that Lemma J0 reads, and the sums
of the parity certificate against the counts of 10.1; the other constants and
guards were not re-derived by the participant. At positions 25 and 29 the guard
selects the candidate before the table read, as in GPT Sol's corrected answer AR
6.3: these positions are not prescribed by the carries (gamma[i] = 0 and D[k] =
0 there, on the old rows for position 25 and on every row for position 29), so
the value of the guard is written into the key before the read, within the same
allowance and the same proved cap (Section 11). Lemma CV (10.2) states what the
solver returns. The submitted program runs this solver with these guards (9.2);
the layout on 64 registers is specified and charged by this text and is not
implemented (9.5).

**9.5 Checks of the joint solver.** The submitted program runs the joint solver
of 9.4 with the guards (G7) and (G15) and the generic solver of 9.8 with (G7),
(G15b) and (G20b) as the logic of this search, one node at a time on Python
integers (9.2); the layout of 9.4 on 64 registers, the schedule of Section 11,
the lean lanes of 9.6 in that layout and the direct tables are not implemented.
The completeness of the joint solver rests on the proofs cited in 9.4, on the
count of the class and on the parity certificate; that of the generic solver on
the transition relation of 9.4 and the closure of (J1) to (J3) as words (9.8);
and the losslessness of the guards on Lemmas G7, G15, G7b, G15b and G20b. The
caps, 17,504 and C_row, rest on the schedules of Section 11 and 9.8, upper
allowances written out by blocks and not counts of an executed program. The
self-test of 9.3 checks the generic traversal with (G20b) on planted words,
Lemma G20b for every value of f AND sigma, and the four guards on words of both
cubes. On a request of 256 trials made as the organizer's runner makes one (seed
text hashsmash-public-seed-v1), 458,752 outer steps, the program found 614
passing outer steps, 112 with T not empty and 211 with X_3 not empty, ran 264
rows of X3, and charged at most 3,987,200 machine units to steps 2 and 3 of one
outer step, with no test against a cap failing and no root. These are the
program's own counts, not a proof of the caps.

**9.6 Seven outer steps in one word (GPT Sol, answer AQ).** The batch of step 1
of 9.1 runs on packed 256-bit words with the seven 36-bit lanes of 6.5: lane i
is bits 36 i to 36 i + 35 of a word, and it holds a 32-bit value in its low 32
bits with four guard bits above them. The conventions are those of 6.5. The low
32 bits of a lane are the scalar value modulo 2^32, and every lane of every sum
stays below 2^36, so that no carry leaves its lane; where an interval bound of a
sum could reach 2^36, an AND with the word M that has the low 32 bits of every
lane set is made first, and charged. x - z is formed as x + (z XOR M) + 1, never
by a packed subtraction, whose borrows could cross lanes. A rotation by r is
PROR: ((x >> r) AND A_r) OR ((x << (32 - r)) AND B_r), five operations, with A_r
and B_r the masks of its two parts in every lane. The addition of a constant is
kept pending until the value is read by an XOR, an OR, a shift, a rotation or a
table index, and the one addition that then forms it is charged. All interval
bounds depend on the lines and the constants only, not on the words.

*What a batch computes.* Each of R_0 to R_7 is drawn and ANDed with M, except
R_7, which is ANDed with the word that has the bits of fc307cfc set in every
lane; lane i of R_k is then the k-th word of the random word of lane i. The
lines of step CO run on the packed words, with y = (W AND fc307cfc) +
(030c0303 - Y3), a pending constant addition, in place of the deposit of a
member number, and without the lines whose values reach neither Y9 nor omega =
Y3 + y + w8. Then omega, and in each lane i the automaton of (2) on omega, for
the outcomes with its last table restricted to S9 (in the charged search, one
load of the E table of 9.8): for each byte of the lane a shift by 36 i plus
eight times the byte's position, an AND with 255, the addition of the state
from the second byte on, and one table load; then the test of its mask against
zero and the branch. The automaton of (1) does not run in the batch. *The lean
lanes (GPT Sol, answer AT 4).* The lanes whose mask of (2) is not zero are
taken at once, in increasing order of i, each by its *Q path*: the E count and
its test (9.1), then the automaton of (1) on the Y9 of that lane, four bytes
taken out by a shift and an AND, three state additions and four table loads,
the AND with the mask of (2), its test and the branch. A lane whose mask X is
not zero is then a passing lane and is processed at once (below). No pass
bitmap is formed and no backup of R_0 to R_7 is stored in the batch.

**Lemma PL (the lanes are independent ordinary outer steps).** (a) The random
words of the RUN_STEPS outer steps of a run are independent and uniform on the
2^256 words, and the algorithm reads no other bit of R_0 to R_7: the guard
bits, bits 252 to 255 and the lanes 1 to 6 of the last batch are not used. (b)
The seven outer words and the member of an outer step are independent; the
outer words are uniform words, and the member is uniform on the class, as when
the eighth word modulo 2^19 is the member number (Section 8). (c) So the outer
steps of a run are independent and identically distributed, and each has the
law of an outer step that draws its own uniform 256-bit word: every count of an
outer step, among them the count N_o of H1' and the indicators of H4', has the law
that it has for such an outer step. The algorithm is a function of the
RUN_STEPS random words, the probability space of 10.4.

Proof. (a) The low 32 bits of lane i of R_k are a set of bit positions of R_k,
and these sets are disjoint for different lanes; different k and different
batches are different draws. So the random words of different outer steps are
made of disjoint sets of the independent uniform bits of the draws, and they
are independent and uniform. The batch reads R_k only through its AND with M or
with the word of fc307cfc, and a passing lane reads only its own lane of the
stored words; so no other bit is read. (b) The bits of 030c0303 and of fc307cfc
are disjoint, so the addition is an OR: e1 has the value 030c0303 at the 13
positions of 03cf8303 and the bits of W at the other 19, so y = e1 - Y3 is the
member of the class (Lemma Q) whose number is the 19 bits of W at the free
positions (Section 8). For a uniform W this number is uniform on 0 to 2^19 - 1,
as W modulo 2^19 is, and it is a function of the eighth word alone. (c) An
outer step and everything computed from it are functions of its random word
only, so (c) follows from (a) and (b). QED. Packing is a representation of
disjoint fresh random bits: it adds no premise to H1' and H4' (GPT Sol, answer
AQ 1).

**Lemma PB (the batch computes the outer steps of its lanes).** In every used
lane of a batch, the low 32 bits of the packed words that the batch forms for Y9
and omega are the values Y9 and omega = Y3 + y + w8 of step CO for the outer
step of that lane; the mask that the lane reads from the automaton of (2) is
that of (2) on omega restricted to S9; the automaton of (1) is run on the Y9 of
exactly the lanes whose mask of (2) is not zero, and its mask is that of (1) on
Y9; and the lane is taken as passing exactly when its outer step passes the
widened filter of 9.8. No sum leaves its lane.

That bound computation is a finite computation on the lines and the constants, not on the words; the
self-test of 9.3 checks every packed sum of its batches against it.

*The count of a batch.* On the machine of Section 11, with 64 registers and
every constant an immediate, the batch is straight-line code with the same count
in every batch. The submitted program compiles it from the lines and counts its
code, one unit for every operation and load: the eight random words, one
operation and one AND each, 16; the lines of step CO that reach Y9 or omega, 262
(261 and the one addition that forms the pending constant of Y9 before it is
read); omega, 2; and the automaton of (2) in the seven lanes with the test of
its mask and the branch, 125 (118, and 7 for the base addresses of the first
table of the automaton in the seven lanes, every other table entry holding the
base address of the next table): 405. With the advance of the batch count, its
comparison with RUN_BATCHES and the branch, 3, and the allowance of 16 for the
test of the last batch, the cursor and the dispatch to the lanes whose mask of
(2) is not zero (GPT Sol, answer AT 4), the batch with the automaton is 424
units. At most 25 registers are live, the two counts included, and nothing is
spilled. With the direct tables of 9.8 the 125 units of the automaton of (2) are
replaced by 41 lane tests, and the batch is charged 341 (9.8, Section 11).

*A passing lane.* For each passing lane, after the pass count and its test (step
1 of 9.1): its eight words are reloaded and taken out of lane i by a shift and
an AND, and step CO runs on scalar words, giving all the names that steps 2 and
3 read, 295 units in the participant's count; the context of the batch, at most
16 words (the eight packed random words, the packed Y9 and omega, the lane and
batch cursor, the current mask and the counts), is stored in fixed memory words
and reloaded, at most 4 units a word; then the pre-check of 9.7, 16 units with
the test of the bits X_3 of 9.8, and 6 for storing C2.c1, C2.b1 and e1 in fixed
words for the guards; and, if T or X_3 is not empty, steps 2 and 3, which may
use all 64 registers. The counts live in fixed memory words and are reloaded,
never restored from a stale copy. Section 11 charges 512 for the lane outside
steps 2 and 3, the pre-check and the 6 included, and the cap of 9.8,
314,996,576, for steps 2 and 3.

*The program's check.* In its self-test the submitted program compares every
lane of N * 64 / 7 batches with step CO run on scalar words on the eight words
of the lane (`scalar_outer`): every name of step CO that the batch forms, Y9,
omega and the masks of (2) and (1); and it checks every packed sum against its
interval bound (9.3). With N = 200 and seed 7, 12,796 of 12,796 lanes agree and
no bound is exceeded. In every passing lane of a trial the program also compares
the packed Y9 and omega with the scalar rebuild (`verify_fail`).

**9.7 The s-pattern pre-check and the guards (G7) and (G15) (GPT Sol, answers
AW 1 and 2, AX 1, CF 7 and CD 10; the pre-check found by a helper agent of the
participant).** Fix a passing outer step, with mask X, and write Q = Y9, e1 =
Y3 + y and, for a trial of it, s = E1.b1 AND beta*. By the lines of step CT
read backwards, Y14 = ROL(E3.h1, 16) XOR e1, Y10 = Y14 + C2.c1, Y6 = ROR(Y10
XOR C2.b1, 7) and E1.b1 = ROR(Y6 XOR c1, 12), so for each bit p of beta*

    s[p] = Z[(p + 19) mod 32] XOR c1[(p + 12) mod 32],   Z = (Y14 + C2.c1) XOR C2.b1.

At p = 13, 14 and 15 the bits of c1 are fixed by Q* (c1 AND 0e09818b =
02008000), with the values 1, 0 and 0, and the bits of Z are 0, 1 and 2. Every
joint root h has h[16] = h[17] = 0 and h[18] = 1 XOR Q[18] ((PHASE) and (g) of
9.4), and every member of the class has e1[0] = e1[1] = 1. So when E3.h1 is a
joint root the low three bits of Y14 are 1, 1 and 1 XOR Q[18] XOR e1[2], and the
number nu = s[13] + 2 s[14] + 4 s[15] is a function of the outer step:

    r  = (((Q >> 16) XOR e1) AND 4) XOR 7,
    nu = (((r + C2.c1) XOR C2.b1) XOR 1) AND 7.                          (V)

r is exactly the low three bits of Y14 at a joint root. The identity is used
only at joint roots; it says nothing of the other trials of the outer step.

*The allowed values (GPT Sol, answer AW 1).* For an outcome j of beta*, a
pattern s is compatible when E1 can give the differences beta*, tau_j and eps
with that s. With Delta(s) = beta* - 2 s - 8 modulo 2^32, the relation a XOR
(a + Delta) = tau has a solution exactly when d = (tau - Delta) mod 2^32 is even
and d / 2 has no bit outside tau, since a XOR tau - a = tau - 2 (a AND tau)
modulo 2^32 and tau[31] = 0. GPT Sol enumerated the 2,048 submasks of beta* with
this exact criterion for the fourteen outcomes:

| rows | compatible s, rows 175, 185, 275, 285, 385, 675, 685 | allowed nu |
| --- | --- | --- |
| old, tau ending in 20a0 | 16, 32, 8, 16, 32, 8, 16 | 3, 4 |
| new, tau ending in 60a0 | 32, 64, 16, 32, 64, 16, 32 | 2, 3, 4, 5 |

Every compatible s has s[3] = s[4] = 1. In the order (s[13], s[14], s[15]), nu =
3 is 110 and nu = 4 is 001. As a table over the fourteen outcomes, bit j - 1 for
outcome j, VMASK = [0, 0, 3f80, 3fff, 3fff, 3f80, 0, 0] for nu = 0 to 7. Every
outcome of S is an old row, so for this search T = X AND VMASK[nu] is X when nu
is 3 or 4 and empty otherwise. A helper agent of the participant found the same
allowed values from the exact E1 counts L_j split by s (the function L_count of
the counting program of Section 17): 16, 32, 8, 16, 32, 8 and 16 patterns with a
nonzero count on the old rows, each with nu = 3 or nu = 4, half of the count of
the row on each, and every row sum equal to its L_j of 10.1.

**Lemma VP (the pre-check is lossless).** Fix a passing outer step with mask X
and let nu be given by (V). Every listed good trial of the outer step has its
outcome in T = X AND VMASK[nu]. So an outer step or an outcome that the
pre-check skips holds no listed good trial, and the count N_o of H1' of every
outer step is the same, pointwise, as without the pre-check.

Proof. Let a listed good trial have outcome j in S and E3.h1 = h. By the proof
of Lemma F, bit j - 1 is set in both masks, so j is in X; by Lemma V, h is a
joint root of outcome j. By (PHASE) and (g) of 9.4, h[16] = h[17] = 0 and h[18]
= 1 XOR Q[18], and e1[0] = e1[1] = 1 for every member, so by the identity above
the bits s[13], s[14] and s[15] of the trial are those of nu. The trial's E1
gives beta*, tau_j and eps, so its s is compatible with outcome j, and by the
enumeration above nu is allowed for j: VMASK[nu] has bit j - 1. So j is in T.
QED. The lemma uses no law of the words. It says which outcomes of S a passing
outer step can hold; it does not say how often nu takes a value, which in this
package enters no budget (9.8). It is not claimed for the outcomes of X3.

*Checks (participant computations, not part of the package).* On 30,000,000 real
outer steps of the whole class (seed 7, the lines of step CO of a participant
program with the class member), 324,098 real trials with c1 in Q* whose E3.h1
had h[16] = h[17] = 0 and h[18] = 1 XOR Q[18] gave s[13] to s[15] equal to nu by
(V) in 324,098 of 324,098. Planted joint roots with y in the class (seed 11,
every root re-tested against the E3 conditions) had h[16] = h[17] = 0 and h[18]
= 1 XOR Q[18] in 2,944 of 2,944, with all fourteen outcomes covered (82 to 477
roots each). These are checks, not proofs; Lemma VP rests on (PHASE), on (g) of
9.4 and on the exact enumeration.

*The charge (GPT Sol, answer AW 2).* On a passing lane, after the rebuild of
step CO on scalar words, Y9, e1, C2.c1 and C2.b1 are names of the rebuild. (V)
takes 8 operations (a shift, an XOR, an AND, an XOR, an addition, an XOR, an XOR
and an AND); the address and load of VMASK[nu], the AND with X, the comparison
and the branch take 5; and the test of the bits X_3 of the outcomes of X3 (9.8),
its comparison and the branch take 3: 16 units, inside the 512 of the lane (9.6,
Section 11), paid by every passing lane, also when T is empty. The pre-check
never enlarges T, so the cap of Section 11 holds for every T. VMASK is built
once from the enumeration above, below 2^23 operations, inside the once-only
allowance of Section 11.

*The guard (G7) (GPT Sol, answer AX 1).* Every compatible s has s[3] = s[4] = 1
(above). At p = 3 and p = 4 the bits of c1 that Q* fixes are 1 and 0 and the
bits of Z are 22 and 23, so s[3] = Z[22] XOR 1 and s[4] = Z[23]: every listed
good trial has Z[22] = 0 and Z[23] = 1. Write C = C2.c1, B = C2.b1, and a22 and
a23 for the carries into bits 22 and 23 of Y14 + C. Bit 22 of Y14 = ROL(h, 16)
XOR e1 is x = h[6] XOR e1[22], and bit 23 is h[7] XOR e1[23]. The two required
sum bits give

    a22  = x XOR C[22] XOR B[22],
    a23  = maj(x, C[22], a22),
    h[7] = e1[23] XOR 1 XOR C[23] XOR B[23] XOR a23.                     (G7)

**Lemma G7.** Let a listed good trial of an outer step have outcome j and E3.h1
= h. Then h[7] is the value that (G7) gives from h[6], e1, C2.c1 and C2.b1.

Proof. The trial's E1 gives beta*, tau_j and eps, so its s is compatible with
outcome j and s[3] = s[4] = 1 by the enumeration above; that is, Z[22] = 0 and
Z[23] = 1 with Z = (Y14 + C) XOR B. Bit 22 of Y14 + C is x XOR C[22] XOR a22,
and it equals Z[22] XOR B[22] = B[22]; this gives a22. The carry out of bit 22
is a23 = maj(x, C[22], a22). Bit 23 of Y14 + C is h[7] XOR e1[23] XOR C[23] XOR
a23, and it equals Z[23] XOR B[23] = 1 XOR B[23]; this gives h[7]. QED. The
unknown carry a22 is fixed by the required bit 22 and need not be computed from
the lower 22 bits; a trial whose true carry differs is not a success, and the E1
test of step 3 would reject it. The lemma uses no law of the words.

*Use in the solver.* h[6] is fixed on every row before the traversal (9.4), so
after it the solver computes h[7] by (G7) for each searched row. On a row on
which position 7 is otherwise free, it becomes prescribed with that value; on a
row on which h[7] is already a constant ((g) of 9.4), the row is dropped for
this outer step when the two values differ. By Lemma G7 no listed good trial is
lost; joint roots that would fail the E1 test of step 3 may be dropped early, so
the solver returns the joint roots of the outcomes of T that satisfy (G7), and
these contain the root of every listed good trial (Lemma CV). Position 7 is then
free on no row (the table of 9.4). h[7] is computed after the row's own patch of
h[6] and is never shared across a family.

*The charge of (G7) (GPT Sol, answer AX 1.1).* 128 more units for each searched
row: the six source bits e1[22], e1[23], C[22], C[23], B[22] and B[23], the
loads and addresses of the three source words, x, the carry a22, the majority,
h[7], the comparison with an existing constant and its branch, and the insertion
of the value into the descriptor of position 7, fewer than 16 blocks of at most
8 units; the scratch words are released before the 32 descriptors are resident,
so the traversal uses no more registers. The caller stores C2.c1, C2.b1 and e1
in three fixed memory words, at most 6 more units, inside the 512 of the lane.
The extra prescribed bit of the written-out rows is inside the once-only
allowance. No new budget, mean or premise (GPT Sol, answer AX 1.2); in this
package there is no solver count at all (9.8). (G7) serves the outcomes of X3 as
well (Lemma G7b of 9.8).

*The guard (G15) (GPT Sol, answers CF 7 and CD 10).* Write C = C2.c1, B = C2.b1,
V = Y12 and A = (Y1 + w12) mod 2^32, so that Z = (Y14 + C) XOR B, Y6 = ROR(Z,
7), E1.a1 = Y6 + A, E1.d1 = ROR(E1.a1 XOR V, 16) and c1 = Y11 + E1.d1 (step CT),
with Y11 = 7af77f38, whose bit 0 is 0. Let a22 be the carry into bit 22 of Y14 +
C, as in (G7), and v16 the carry into bit 16 of Y6 + A, and put

    a22 = h[6] XOR e1[22] XOR C[22] XOR B[22],
    v16 = V[16] XOR 1 XOR A[16].

For the prefix H of the bits h[0] to h[14] of a node at position 15 (its higher
bits zero), with all words of 32 bits:

    L     = (H >> 6) XOR (e1 >> 22),
    zeta  = (((L + (C >> 22) + a22) XOR (B >> 22)) >> 1) AND 1ff,
    p15   = (zeta + ((A >> 16) AND 1ff) + v16) AND 1ff,
    cstar = (Y11 AND 1ff) + (p15 XOR ((V >> 16) AND 1ff)),

    (G15)  cstar AND 08b = 0  and  h[15] = bit 8 of cstar.

**Lemma G15.** Let a listed good trial of an outer step have an outcome j of S
and E3.h1 = h. Then h satisfies (G15).

Proof. The trial has Z[22] = 0 and Z[23] = 1 (proof of Lemma G7) and c1 in Q*,
so c1[0] = c1[1] = c1[3] = c1[7] = c1[8] = 0 (the mask 0e09818b and the value
02008000). Bit 22 of Y14 + C is h[6] XOR e1[22] XOR C[22] XOR a22 and equals
Z[22] XOR B[22] = B[22], which gives a22. c1[0] = 0 and Y11[0] = 0 give E1.d1[0]
= 0, that is E1.a1[16] = V[16]; Y6[16] = Z[23] = 1; and bit 16 of Y6 + A is 1
XOR A[16] XOR v16 = V[16], which gives v16. Bits 22 to 31 of Y14 = ROL(h, 16)
XOR e1 are h[6] to h[15] XOR e1[22] to e1[31], which are L when h[15] = 0.
Adding C[22..31] with the carry a22 and XORing B[22..31] gives Z[22..31], and
the shift drops Z[22]: zeta is Z[23..31] = Y6[16..24]. Adding A[16..24] with the
carry v16 gives E1.a1[16..24], so p15 XOR V[16..24] is E1.d1[0..8], and adding
Y11[0..8] with no carry into bit 0 gives c1[0..8]. So the low nine bits of cstar
are c1[0..8] of the trial with h[15] set to 0. Changing h[15] alone flips
Y14[31], hence Z[31], Y6[24], E1.a1[24], E1.d1[8] and c1[8], and no lower bit of
these words. As c1[0] = c1[1] = c1[3] = c1[7] = 0, cstar AND 08b = 0; as c1[8] =
0, h[15] = bit 8 of cstar. QED. The carries a22 and v16 are those of a listed
good trial: a word whose true carries differ is not a success, and step 3 still
tests every root in full (Lemma RC). The lemma uses no law of the words.

*Use in the solver.* For each searched row of S, after (G7), the solver stores
five words in fixed memory: e1 >> 22, (C >> 22) + a22, B >> 22, ((A >> 16) AND
1ff) + v16 and (V >> 16) AND 1ff; a22 needs h[6], fixed on the row. At each node
of position 15 it computes cstar from the prefix of the node, drops the prefix
when cstar AND 08b is not 0, and otherwise prescribes h[15] = bit 8 of cstar in
a temporary copy of the descriptor of position 15, which the forced transition
array then reads; the stored descriptor is not changed, since another prefix may
need the other value. Position 15 is then free on no row of S (the trees with
(G15) of 9.4). By Lemma G15 no listed good trial is lost; the solver returns the
joint roots of the outcomes of T that satisfy (G7) and (G15) (Lemma CV).

*The charge of (G15) (GPT Sol, answer CF 7.2).* 128 more units for each searched
row, for its five words: the loads and addresses of their sources, at most 24;
the additions, masks, shifts and the two carries, at most 24; five stores with
their addresses, 10; row control and addresses, 16: 74. 64 more units at each
node of position 15, besides its 20 as a forced node: five loads with their
addresses, 10; the shift, XOR, addition, XOR, shift and AND of zeta, 6; the
addition, AND, XOR and addition of p15 and cstar, 4; the test of cstar AND 08b
and its branch, 3; bit 8 taken out and the temporary key patched, at most 6;
copies and control, at most 16: 45. It uses the ten temporaries of the traversal
and spills nothing (Section 11). Its code and the layout of the five words are
inside a once-only allowance of 2^20 (Section 11).

**9.8 The extra beta outcomes: the widened search of this package (GPT Sol,
answers AX 2, CL 7 and CL 9).** This package lists three outcomes of a second
value of E1's first-half b difference, beta3 = 18d0e098, next to the six
outcomes of beta* in S. This subsection states what changes; the rest of
Sections 8 to 9.7 is used as written, for the outcomes of S.

*The outcomes.* X3 is the set of the three outcomes (tau, eps) of beta3 with
tau = 185020a0, 285020a0 and 385020a0 and eps = 6e61be55, and S9 is S together
with X3, nine outcomes. eps = 6e61be55 differs from the eps 6e21be55 of beta* in
bit 22 only. A trial has one triple (beta, tau, eps) of E1 differences, so the
nine events are disjoint and their success masses add with no double count
(GPT Sol, answer AX 2.2). In the masks of this subsection bits 0 to 5 are the
outcomes of S in the order 175020a0, 185020a0, 275020a0, 285020a0, 385020a0 and
685020a0, and bits 6, 7 and 8 the outcomes 185020a0, 285020a0 and 385020a0 of
X3; X_S of 9.1 is bits 0 to 5 written in the numbering of Section 8, and X_3 is
bits 6 to 8.

*The cube of beta3 and the union U (GPT Sol, answer AX 2.1).* With DY11 =
0a08818b, the identities c1 XOR (c1 + DY11) = ROL(beta, 12) and (c XOR m) - c =
m - 2 (c AND m) give the cube of the words c1 with a given beta (proof of
Theorem C (iv)). For beta3, ROL(beta3, 12) = 0e09818d and (0e09818d - 0a08818b)
/ 2 = 02008001, so the cube is

    Q3 = { c1 : c1 AND 0e09818d = 02008001 },

against Q* = { c1 : c1 AND 0e09818b = 02008000 }. Both masks have 11 bits, so
each cube has 2^21 words; bit 0 is in both masks, with value 0 in Q* and 1 in
Q3, so the cubes are disjoint, and their union U has 2^22 words (participant
arithmetic on GPT Sol's statement).

*Reachability (GPT Sol, answer AX 2.1).* Step 3 of 9.1 maps a root h to its c1
by the inverse of the permutation of Lemma IP: Y14 = ROL(h, 16) XOR (Y3 + y),
Y6 = ROR((Y14 + C2.c1) XOR C2.b1, 7), E1.a1 = Y6 + Y1 + w12 and c1 = Y11 +
ROR(E1.a1 XOR Y12, 16). Step CO does not depend on c1, and Lemma CT builds a
pair of messages for every word c1, not only for c1 in Q*. So in every outer
step every word c1 is reached through exactly one h: the cube test of step 3 is
a certification test, not a restriction of this enumeration. Widening it to U
admits the trials of beta3 in the same outer steps, with no new outer word and
no second chart of the compression; leaving it unchanged rejects all of them.
This is algebraic reachability, not a proved rate of success.

*Lemma V9.* Lemma V holds for c1 in Q3 and an outcome j of X3 with beta3 in
place of beta* and eps_j = 6e61be55: the last condition of R = 0 holds, since
ROL(18d0e098 XOR 6e61be55, 1) = ROL(76b15ecd, 1) = ed62bd9a and 6e61be55 XOR
ed62bd9a = 830303cf = eta (participant arithmetic), and the proof is otherwise
that of Lemma V, with eps_j in (J2) and mu = ROR(eta XOR eps_j, 8) in (J3).

*What the outcomes of beta3 share with those of S (GPT Sol, answers AX 2.2 and
CL 2).* With sigma = tau XOR ROR(tau, 1) and theta = ROL(sigma, 12), the first
joint equation (J1), (Q + h) XOR (Q + (h XOR eta)) = theta, is the same for an
outcome of X3 and for the outcome of S with the same tau, and so is condition
(1) of the filter. eps differs in bit 22, so the target of (J2), D and kappa of
9.4 change, and so does mu of (J3). A list of words that satisfy all three
equations for eps = 6e21be55 is not a list for 6e61be55, and running it once and
trying the other cube does not recover the missing roots. The phase guards
(PHASE), the parity certificate (P*), Lemma J0, VMASK with its share and the
caps of the joint solver of 9.4 are not claimed for the outcomes of X3, and the
set-up of the joint solver is not used for them. The guards (G7), (G15b) and
(G20b) of the generic solver below are proved for them (Lemmas G7b, G15b and
G20b); (G20b) has the conclusion of Lemma J0, by a proof that does not use
(PHASE).

*The widened filter and Lemma F9 (GPT Sol, answer AX 2.2).* Give each of the
nine outcomes its own bit. For an outcome of X3, condition (1) is that of the
outcome of S with the same tau (the shared bit of (J1) duplicated), and
condition (2) is (2) of Section 8 with its own eps, 6e61be55, and its own sigma.
An outer step passes the widened filter when for some outcome of S9 both of its
conditions hold, that is when the mask X of 9.1 is not zero. **Lemma F9.** An
outer step that does not pass the widened filter holds no trial, for any c1,
with R = 0 and an E1 outcome in S9. *Proof.* That of Lemma F, with the trial's
own tau and eps: for an outcome of X3 the trial's h witnesses (1) for Y9 and its
f witnesses (2) with eps = 6e61be55 for omega. QED. It uses no law of the words.
The certificate of step 3 uses the cube, beta, tau and eps of the root's own
outcome.

*Exact masses and filter counts (GPT Sol, answer AX 2.3).* Under the same
normalization as 10.1, L N3 / 2^83 with Y4 uniform in the class, the
participant's integer records of L and N3 for beta3 give the three outcomes of
X3 the parts 12,582,912 (285020a0), 8,388,608 (385020a0) and 8,388,608
(185020a0), 29,360,128 together. With the 67,633,152 of S (10.1):

| set | part, scale 2^-83 | passing (Q, E) pairs of 2^64 | words passing (2), of 2^32 |
| --- | ---: | ---: | ---: |
| S (mask 5f of Section 8) | 67,633,152 | 18,289,159,183,466,496 | 233,715,456 |
| S9, S with the three of X3 | 96,993,280 | 23,384,160,813,285,376 | 305,100,224 |

The pass share of S9 is pi9 = 23,384,160,813,285,376 / 2^64 = 2^-9.6236188261,
and the share of words that pass (2) is 305,100,224 / 2^32 = 2^-3.8152920. The
recount of S alone in the same computation gives 279,070,422,111 / 2^48, the
share of Section 8, which checks the normalization independently. The counts are
a finite 32-layer carry-set count, not a sample: for each target (dz, out) the
subset of the four addition-carry pairs is kept, bit by bit, as in the method of
Section 8, and the two histograms of masks, with 11 mask cells for (1) and 41
for (2) over the nine outcomes, each sum to 2^32; the passing pairs are the sum
over intersecting masks of the products of their word counts. The parts of X3
are GPT Sol's counts and are not recounted here; the widened counts
23,384,160,813,285,376 and 305,100,224 are recounted, with the counts of S, by
the self-test of the submitted program from its own automata of the ten outcomes
(9.3). Model counts do not prove the law of the sampler's words (H4').

*The direct tables (GPT Sol, answers AX 2.4, BA 18 and CL 8).* The widened
filter is read from two tables indexed by a whole 32-bit word: the Q table, read
at Y9, holds the nine-bit mask of (1), and the E table, read at omega, the
nine-bit mask of (2), one word of 2^32 for each. Together they hold 2^38 bytes,
below 2^44. Each entry is built by the finite carry-set existence recurrence, at
most 9 * 32 * 512 < 2^18 operations, and both tables together are charged 2^51
machine units once (Section 11).

**Lemma TAB (the direct tables decide as the automata do).** For every word w,
the entries of the E table and of the Q table at w are the masks, restricted to
S9, that the automata of (2) and (1) of Section 8 for the ten outcomes of the
program (the seven of Section 8 and the three of X3) give on w. So in every
outer step the mask of (2), the E count, the mask X, the pass decision, the
pre-check and every later step of 9.1 are the same whether the masks are read
from the tables or computed by the automata. *Proof.* Both decide, for each of
the nine outcomes, whether the carry-set recurrence of Section 8 accepts w with
the targets of that outcome, and a nine-bit mask fits one word. The tables are
fixed before the first batch and read no random bit, so the random words of the
outer steps are those of Lemma PL. QED.

*The batch with the direct tables, 341, and the Q path, 13 (GPT Sol, answers BA
18.1 and CL 8).* The batch of 9.6 keeps the eight fresh draws with their ANDs,
16, the lines of step CO that reach Y9 or omega, 262, and omega, 2, all counted,
the advance of the batch count with its comparison and branch, 3, and the
allowance of 16 for the test of the last batch, the cursor and the dispatch. The
automaton of (2) with the 7 base additions of its first tables, 125 units, is
replaced by seven direct-table lane tests, each the extraction of omega from its
lane, the address of the E table at omega, its load, the comparison of the mask
with zero and the branch: 6 units a lane and 5 for lane 0, which needs no shift,
41 in all. So a batch costs at most 16 + 262 + 2 + 3 + 16 + 41 = 340 machine
units, and it is charged 341. A Q path, for each lane whose mask of (2) is not
zero, in increasing order of i: 6 for the E count, kept in a fixed memory word
(its address, its load, the increment, the store of the new count before its
comparison with E_BUDGET, the comparison and the branch); then 7 for the
extraction of the lane's Y9, the address of the Q table at Y9, its load, the AND
with the mask of (2), the comparison with zero and the branch: 13. A run that
fails a budget test halts and never resumes, and no count wraps. A passing lane
then pays the 512 of 9.6. The packed lines of 9.6, their interval bounds and
their ANDs with M are unchanged. No quarter skip of the pre-check is claimed for
the outcomes of X3: in a passing outer step they reach the generic solver
whenever their bits are set in X.

*The generic solver for the outcomes of X3 (GPT Sol, answers AX 2.4, CL 7 and CL
9).* For each outcome of X3 whose bit is set in X_3, run the general two-carry
traversal of (J1) and (J2) of 9.4 from bit 0, with both guesses of the carry a20
into bit 20 of the addition of (J2), on the descriptors of the row: sigma and
theta of its tau, gamma = eta XOR theta, D = (sigma XOR eps3) AND 7fffffff and
kappa = sigma XOR eps3 XOR E XOR E', with eps3 = 6e61be55. At position i, with k
= (i + 20) mod 32, at most one child can survive when i < 31 and gamma[i] = 1,
or when k < 31 and D[k] = 1 (Lemma S5); it is read from the forced array. At
position 7 the solver keeps only the arc whose bit is the value that (G7) of 9.7
gives from the h[6] of the prefix; at position 15, after the test of (G15b)
below, only the arc whose bit is the h[15] that (G15b) gives; and at position 20
only the arc whose e2[8] is the h[8] of the prefix, read from the selected array
of 9.4 with the desired bit h[8] ((G20b) below). When another carry prescription
fixes the same bit, the arc of the other value is invalid and the prefix ends,
so the two requirements are compared and an inconsistent prefix is rejected. At
the other positions both values are taken from the dual array. No (PHASE),
parity guard or E1 guard of 9.4 is used, and Lemma J0 is not used as proved
there: (G20b) gives its conclusion for X3 by another proof. At every leaf the
three word equations (J1), (J2) and (J3) are checked with eps3 and mu3 = ROR(eta
XOR eps3, 8), and step 3 certifies the root with the cube Q3 and the E1 target
of the outcome. A true root survives under its true carry guess, and the final
word checks enforce the closure at the wrap; a word kept under both guesses is a
duplicate candidate, charged and harmless, which cannot lose a success.

*(G7) for the cube of beta3 (GPT Sol, answers CL 3 and CL 7).* beta* and beta3
have the same low byte 98, both give the step -8 of w5 in E1 on B, and every tau
of S9 has the low byte a0. With s = E1.b1 AND beta and Delta(s) = beta - 2 s -
8, the relation a XOR (a + Delta) = tau gives Delta = tau - 2 (a AND tau) modulo
2^32, whose residues modulo 256 are a0 and 60, while Delta modulo 256 is 90 - 16
s[3] - 32 s[4], one of 90, 80, 70 and 60 (the term of s[7] vanishes modulo 256).
The only common value is 60, so s[3] = s[4] = 1 for every listed good trial of
S9. The cube Q3 fixes c1[15] = 1 and c1[16] = 0, the values that Q* fixes, so,
as in 9.7, s[3] = Z[22] XOR 1 and s[4] = Z[23]: Z[22] = 0 and Z[23] = 1.

**Lemma G7b.** Let a listed good trial of an outer step have an outcome of X3
and E3.h1 = h. Then h[7] is the value that (G7) gives from h[6], e1, C2.c1 and
C2.b1.

*Proof.* That of Lemma G7, with Z[22] = 0 and Z[23] = 1 from the paragraph
above. QED. The generic solver needs no h[6] fixed in a set-up: at position 7 it
is already in the prefix.

*(G15b), the guard (G15) for the cube of beta3.* The cube Q3 fixes c1[0] = 1 and
c1[2] = c1[3] = c1[7] = c1[8] = 0 (the mask 0e09818d and the value 02008001), so
its fixed low bits are 0, 2, 3, 7 and 8, against 0, 1, 3, 7 and 8 for Q*. With
the notation of (G15) of 9.7 put

    v16b = V[16] XOR A[16],

form L, zeta, p15 and cstar as in (G15) with v16b in place of v16, and require

    (G15b)  cstar AND 08d = 001  and  h[15] = bit 8 of cstar.

**Lemma G15b.** Let a listed good trial of an outer step have an outcome of X3
and E3.h1 = h. Then h satisfies (G15b).

*Proof.* As for Lemma G15, with these changes. The trial has Z[22] = 0 and Z[23]
= 1 (above), which gives a22. c1[0] = 1 and Y11[0] = 0 give E1.d1[0] = 1, that
is E1.a1[16] = V[16] XOR 1; Y6[16] = Z[23] = 1; and bit 16 of Y6 + A is 1 XOR
A[16] XOR v16 = V[16] XOR 1, which gives v16 = V[16] XOR A[16] = v16b. The rest
is the proof of Lemma G15: the low nine bits of cstar are c1[0..8] of the trial
with h[15] set to 0, and changing h[15] alone flips c1[8] and no lower bit of
c1. As c1[0] = 1 and c1[2] = c1[3] = c1[7] = 0, cstar AND 08d = 001; as c1[8] =
0, h[15] = bit 8 of cstar. QED. Toggling h[15] flips c1[8] only among the fixed
low bits, so the test loses no listed good trial of X3, and it needs no
assumption on phases, parity, resets or coalescence. The lemma uses no law of
the words; step 3 still tests every root against the whole cube Q3, the J words,
t and the E1 target.

*(G20b), the guard of position 20 for the outcomes of X3 (GPT Sol, answer CL
9).* Lemma J0 of 9.4 rests on (PHASE), which is not claimed for X3. Its
conclusion holds for X3 by modular arithmetic on (J2) and one fixed bit of the
class:

**Lemma G20b.** Let y be a member of the class and h a word that satisfies (J2)
and (J3) of an outcome of X3. Then h2[0] = 0, that is h[8] = e2[8].

*Proof.* With E' = E + DY3, DY3 = fdb77cfd, (J2) says that e2' = E' + (f XOR
sigma) equals e2 XOR eps3, where e2 = E + f. For words a and m, (a XOR m) - a =
m - 2 (a AND m) modulo 2^32. Put pf = f AND sigma and pe = e2 AND eps3.
Subtracting e2 = E + f from e2' gives DY3 + sigma - 2 pf = eps3 - 2 pe modulo
2^32; DY3 and eps3 are odd and sigma is even (tau[0] = tau[1]), so DY3 + sigma -
eps3 is even and

    pf = pe + K  modulo 2^31,   K = ((DY3 + sigma - eps3) mod 2^32) / 2.

For tau = 185020a0, 285020a0 and 385020a0, K = 51e6f7cc, 65e6f7cc and 59e6f7cc;
the low 21 bits of each are 06f7cc. pe is a submask of eps3, whose low 21 bits
are 01be55, so the low 21 bits of pe and of K add to at most 01be55 + 06f7cc =
08b621, which is below 2^20: bit 20 of pf is 0, with no carry into it. sigma[20]
= 1 for all three outcomes, so f[20] = 0. f = ROR(y XOR g, 12), so f[20] is bit
0 of y XOR g, and y[0] = 0 for every member of the class (9.4): g[0] = 0. For
the three outcomes tau[0] = tau[1] = 0, theta[0] = theta[1] = 1, mu3[0] = 1 and
mu3[1] = 0. Both additions of (J3) have carry 0 into bit 0. At bit 0, g + h2
adds 0 and h2[0] with carry 0 out, and (g XOR theta) + (h2 XOR mu3) adds 1 and
h2[0] XOR 1 with carry 1 XOR h2[0] out. At bit 1 the first sum bit is g[1] XOR
h2[1], and the second is (g[1] XOR 1) XOR h2[1] XOR (1 XOR h2[0]) = g[1] XOR
h2[1] XOR h2[0]. (J3) at bit 1 requires their XOR, h2[0], to be tau[1] = 0. h2 =
ROR(h XOR e2, 8), so h2[0] = h[8] XOR e2[8]. QED. The lemma reads no phase,
parity, prefix or coalescence property, does not use g[1], and uses no law of
the words; it holds for every word h with (J2) and (J3) and so for the E3.h1 of
every listed good trial of X3 (Lemma V9).

As in 9.4, e2[8] is produced at position 20 of the traversal (k = 8): e2[8] =
E[8] XOR f[8] XOR a[8] with f[8] = y[20] XOR Q[20] XOR h[20] XOR u[20], where
u[20] and a[8] are the carries of the current state of the node and every other
term is known there, h[8] among them. So the forward guard is

    (G20b)  h[20] = h[8] XOR E[8] XOR y[20] XOR Q[20] XOR u[20] XOR a[8],

which the generic solver applies at position 20 by reading the selected array
with the desired bit h[8]: as e2[8] changes with h[20], at most one arc has it.
By Lemma G20b a true root survives under its true carry guess, and every leaf is
still tested against (J1) to (J3) as words, and every root by step 3 against the
cube Q3, t and the E1 target. No fixed low prefix, coalescence of duplicates or
parity of beta* is assumed.

*The trees and the row caps (GPT Sol, answers CL 7 and CL 9).* Before the
guards a position i is free when neither (i < 31 and gamma[i] = 1) nor (k < 31
and D[k] = 1), k = (i + 20) mod 32; (G7), (G15b) and (G20b) then take positions
7, 15 and 20, which are free before the guards as follows: 7 on the row
285020a0 only, 15 and 20 on all three. With n_i = 2^(the number of remaining
free positions below i), one guess of a20 visits at most n_i nodes at position
i, so at most N = n_0 + .. + n_31 nodes and L = n_32 leaves. From gamma and D
(participant computation; the self-test of 9.3 recomputes the trees):

| outcome of X3 | free before the guards | remaining free positions | N | L | n_7 | n_15 | n_20 | C_row |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 185020a0 | 14 | 1, 2, 4, 6, 11, 13, 16, 24, 25, 26, 29, 30 | 11,372 | 4,096 | 16 | 64 | 128 | 78,788,992 |
| 285020a0 | 16 | 1, 2, 4, 6, 9, 11, 13, 16, 24, 25, 26, 29, 30 | 22,668 | 8,192 | 16 | 128 | 256 | 157,489,536 |
| 385020a0 | 15 | 1, 2, 4, 6, 9, 11, 13, 16, 24, 25, 26, 29, 30 | 22,668 | 8,192 | 16 | 128 | 256 | 157,489,536 |

Steps 2 and 3 of a row of X3 cost at most

    C_row = 8,576 + 2 * (512 * N + 8,192 * L + 64 * (n_7 + n_15 + n_20))

machine units, both guesses included: 8,192 for the set-up of the row, its
descriptors, its source import, rebuild and checkpoints, so that it relies on no
scratch value surviving an earlier solver call, 128 for the constants of (G7),
128 for the fixed words of (G15b) and 128 for the source preparation and
descriptors of (G20b), 8,576 in all; 512 per node, which covers both candidate
full-adder computations, addresses, spilled parent records and loop control;
8,192 per leaf, which covers the closure, the inverse of Lemma IP and step CT,
and the full E1 and validity certificate (the final check of a found pair is
charged separately, Section 11); and 64 more per node at positions 7, 15 and 20.
At position 15 the 64 cover a22 from the h[6] of the prefix and the stored
source slices, ten loads, the predicted carry and the slices in fewer than 30
units, the low-cube test and the key patch in fewer than 10, and control and
copies in fewer than 14; at position 7 they cover the source loads, the majority
and the restriction of the descriptor; at position 20 they cover the addressed
source reads, the extraction of h[8] and of the carries of the state, the
six-term XOR or the desired bit of the selected key, the restriction of the
child and control. No traversal register is added: fixed memory words, the
scalar scratch of the row and the addressed parent frames of 9.4 hold the rest.
These are upper allowances, not minima; the 512 per node and the 8,192 per leaf
are kept in full, also at positions 7, 15 and 20.

*The cap of steps 2 and 3 (GPT Sol, answers CL 7 and CL 9).* The outcomes of X3
share their condition (1) with the outcomes 185020a0, 285020a0 and 385020a0 of
S, bits 1, 3 and 4 of the masks of (1) in Section 8, and no mask of (1) in the
table of Section 8 has bits 1 and 3 together: the rows of X3 can occur together
only as 285 and 385 or as 185 and 385, or as subsets. So steps 2 and 3 of a
passing outer step cost at most

    C_union = 17,504 + 157,489,536 + 157,489,536 = 314,996,576

machine units, whatever its words: the cap 17,504 of the joint solver for the
outcomes of S with (G7), (G15) and Lemma RC (Section 11), and the two largest
rows of X3 that can occur together (the other pair gives 236,278,528). The
pre-check of 9.7 reads the bits of S only and never drops a bit of X3, and the
mask X is kept in the words of the caller that the 512 of the lane pays (9.6).

**Lemma CV9 (coverage of the widened search).** Fix an outer step that passes
the widened filter. The roots returned by step 2 contain the E3.h1 of every
listed good trial of the outer step, with its outcome, and step 3 certifies
exactly the roots that are the E3.h1 of a listed good trial. So the number of
distinct c1 certified in the outer step, zero when T and X_3 are empty, is its
count N_o of H1' (10.3).

*Proof.* For an outcome of S: Lemmas VP, G7, G15, RC and CV, with Lemma F9 in
place of Lemma F. For an outcome j of X3: by Lemma F9 its bit is set in X_3; by
Lemma V9 the trial's h satisfies (J1) to (J3) of j; by Lemmas G7b, G15b and G20b
it satisfies (G7), (G15b) and (G20b), so at positions 7, 15 and 20 the generic
solver keeps the arc of its own bit, and at every other position the arc of its
own bit is valid from its own carries; so the generic solver reaches its leaf
under its true guess of a20; and step 3 maps it to its c1, which is in Q3, has t
not zero and has the E1 outcome j, so it is certified. Conversely, a certified
root gives a c1 in the cube of its beta with t not zero whose E1 differences are
those of its outcome, and h satisfies (J1) to (J3), so by Lemma V, RC or V9 the
trial of c1 is a listed good trial. Different c1 come from different h (Lemma
IP); a duplicate candidate gives the same c1. QED. Lemma CV9 uses no law of the
words. An outer step has at most 16 roots of the outcomes of S and at most 2 *
(8,192 + 8,192) = 32,768 candidate roots of X3.

*No solver budget.* There is no solver count and no SOLVER_BUDGET: every passing
outer step is charged the cap C_union whether or not its T and X_3 are empty, so
the time bound needs no count of the outer steps that reach the solvers, and H4'
has no clause for them (10.3). The 3 units of the pre-check for a solver count
hold the test of X_3 (9.7).

*What is open (GPT Sol, answers CL 8 and CL 9).* A tighter certificate of
prefixes or parities for the new eps, a slot map over the whole union and the
cheapest solver for the union are open. This package charges the upper schedule
above; it assumes no share of the pre-check and no smaller number of physical
roots for the new eps.

## 10. The rate of a counter trial and the success probability

**10.1 The model rate.** The seven-word model M of Section 13 treats the
residual of a trial as a function of seven words, E1.d1, E1.b1 and E1.a2 of
message A and Y4, Y9, w8 and E3.h1. In this package Y4 is uniform in the class
of eta, not in the sub-class, and the other six are independent uniform words,
so M has 2^192 * 2^19 = 2^211 inputs. Under M the rate of the class is
85074516985129 / 524288 = 162,266,763.66 (Section 13): a trial has R = 0 with
probability that number times 2^-128. The part of a value beta of E1's
first-half b difference in it is written r(beta); the part of beta* is
71,698,432, and the part of the six outcomes of S that this search lists (below)
is 67,633,152. A trial of Section 8 has c1 in Q* and so the difference beta*
(Theorem C (iv)); under M the event that c1 = Y11 + E1.d1 lies in Q* has
probability 2^-11 and is the event that the difference is beta* (Lemma S1). The
rate at which a trial that M conditions on c1 in Q* has R = 0 with an outcome of
S is therefore

    p = 2^11 * 67,633,152 * 2^-128 = 138,512,695,296 * 2^-128 = 1,032 * 2^-101,

about 2^-90.989. It is 853.61 = 2^9.738 times the model rate of a trial of the
class.

*The outcomes of beta*.* In the count of Section 13 an outcome of beta
is a pair (tau, eps) of the differences of E1's a and c outputs. For an outcome
j of beta*, L_j is the number of triples (E1.c1, E1.b1, E1.a2) of words for
which E1 on A and on B (6.2) gives the differences beta*, tau_j and eps_j; and
N3_j is the number N3 of step 3 of the count for that outcome: the number of
quadruples (Y4, E3.h1, Y9, w8), Y4 in the class, for which E3 on A and on B
gives the differences eta and tau_j XOR ROR(tau_j, 1) of its first-half d and b
values and tau_j and eps_j of its c and a outputs. Every input of the 2^211 of
the model falls into one outcome, so r(beta*) = sum over j of L_j N3_j / 2^83.
Beta* has fourteen outcomes on the class, all with eps = 6e21be55; this search
lists the six of S, j = 1 to 5 and 7:

| j | tau | L_j | N3_j | L_j * N3_j / 2^83 |
| ---: | --- | ---: | ---: | ---: |
| 1 | 175020a0 | 562,949,953,421,312 | 108,086,391,056,891,904 | 6,291,456 |
| 2 | 185020a0 | 2,251,799,813,685,248 | 72,057,594,037,927,936 | 16,777,216 |
| 3 | 275020a0 | 562,949,953,421,312 | 18,014,398,509,481,984 | 1,048,576 |
| 4 | 285020a0 | 2,251,799,813,685,248 | 108,086,391,056,891,904 | 25,165,824 |
| 5 | 385020a0 | 1,125,899,906,842,624 | 144,115,188,075,855,872 | 16,777,216 |
| 6 | 675020a0 | 140,737,488,355,328 | 4,503,599,627,370,496 | 65,536 |
| 7 | 685020a0 | 562,949,953,421,312 | 27,021,597,764,222,976 | 1,572,864 |
| 8 | 175060a0 | 281,474,976,710,656 | 6,755,399,441,055,744 | 196,608 |
| 9 | 185060a0 | 1,125,899,906,842,624 | 9,007,199,254,740,992 | 1,048,576 |
| 10 | 275060a0 | 281,474,976,710,656 | 1,125,899,906,842,624 | 32,768 |
| 11 | 285060a0 | 1,125,899,906,842,624 | 13,510,798,882,111,488 | 1,572,864 |
| 12 | 385060a0 | 562,949,953,421,312 | 18,014,398,509,481,984 | 1,048,576 |
| 13 | 675060a0 | 70,368,744,177,664 | 281,474,976,710,656 | 2,048 |
| 14 | 685060a0 | 281,474,976,710,656 | 3,377,699,720,527,872 | 98,304 |
| sum, S: j = 1 to 5 and 7 (listed) | | | | 67,633,152 |
| sum, j = 1 to 7 (the seven of the program) | | | | 67,698,688 |
| sum, all fourteen | | | | 71,698,432 |

The rows j = 1 to 7 have the L_j of the sub-class of entry 26ebba63 and four
times its N3_j, so on this scale they carry exactly its 67,698,688 = 1,033 *
2^16. S leaves out row 6, 675020a0, with 65,536 = 2^16, and carries 67,633,152 =
1,032 * 2^16, so p = 1,032 * 2^-101 exactly; the rows j = 8 to 14, with bit 14
of tau set, add 3,999,744, 5.6 per cent of the part of beta*, and are not listed
either. The integers L_j and N3_j are those of the participant's counting
program, printed in Section 17 with the six rows of its output that this search
lists; it prints L_j N3_j / 2^81, four times the last column, and the six listed
rows sum to 270,532,608 = 4 * 67,633,152 there, and the scale 2^83 is that of a
trial with Y4 uniform in the 2^19 members of the class (GPT Sol, answer AQ 3).
Of the 52 values of tau that pass the screens of the count, 30 have N3_j > 0 and
14 have L_j N3_j > 0. The count uses no rule on h1.

*The nine outcomes of this package and the union U.* The search lists S and
the three outcomes of X3 of beta3 (9.8), with parts 8,388,608 (185020a0),
12,582,912 (285020a0) and 8,388,608 (385020a0) on the same scale (GPT Sol,
answer AX 2.3, from the participant's integer records; not printed in Section
17), so the part of S9 is R9 = 67,633,152 + 29,360,128 = 96,993,280. Under M the
event that c1 lies in Q3 has probability 2^-11 and is the event that the
difference is beta3, by the proof of Lemma S1 with the cube of 9.8; the cubes are
disjoint, so c1 lies in U with probability 2^-10, and an outcome of S9 implies
c1 in the cube of its beta. Hence, with G9 the event that R = 0 with an outcome
of S9,

    p9 = Pr_M(G9 | c1 in U) = 2^10 * 96,993,280 * 2^-128
       = 99,321,118,720 * 2^-128,

about 2^-91.469 per trial of U, 612.09 times the model rate of a trial of the
class. It is the rate against which FACTOR is set (9.1, 10.3; GPT Sol, answer AX
2.4, a = floor(5 R 2^10 / 7)). p, above, is the part of S on Q* alone.

*Why S.* Of the 16,383 nonempty sets of outcomes of beta*, S gives the least
exact charge of the six-outcome search of entry 0bc5f130 (GPT Sol, answer AW 4;
step 3 of SEL, Section 12); this package keeps it and adds X3.
The row 675020a0 carries 0.1 per cent of the count of the seven, but dropping it
lowers the share of passing pairs by a factor of 1.12 (Section 8).

*Why beta*.* Beta* is not chosen by a ranking in this package: it is the beta of
the solution with which the solver found the six constants, and the selection
procedure of Section 12 keeps it with its count. Its cube of c1 has k = 11 fixed
bits, mask 0e09818b and value 02008000. On the sub-class of entry 26ebba63, GPT
Sol 6.1 ranked the 53 values of beta with a part by their conditional rates 2^k
r(beta), and beta* was first. The submitted program stores beta* (`BETA_STAR`)
with the mask and value of its cube (`QSTAR_MASK`, `QSTAR_VALUE`), and beta3
with its cube (`BETA3`, `Q3_MASK`, `Q3_VALUE`).

**10.2 Lemmas on the counter sampler (GPT Sol 6.1).** The following lemmas were
proved by GPT Sol 6.1 for this construction, Lemma S9 by GPT Sol in its answer
AC, and are given with their hypotheses; each is exact mathematics under the
hypotheses stated. The
participant compared Lemmas S1 to S4 and Lemma IP with the construction line by
line; the carry Lemmas S5 to S7 were not re-derived by the participant. They do
not prove the rate of H1' or the success probability; 10.3 states what remains
a premise. The proofs of Lemmas S1 and S9 hold for any fixed set of members
(GPT Sol, answer AN 1); here the set is the class.

**Lemma S1 (conditioning the model).** *Hypotheses:* under M the six words
E1.d1, E1.b1, E1.a2, Y9, w8 and E3.h1 are independent uniform words, independent
of Y4, which is uniform in the class; c1 = Y11 + E1.d1. *Statement:* c1 lies in
Q* with probability 2^-11, and that is the event that E1's first-half b
difference is beta*. Conditional on it, E1.d1 is uniform on Q* - Y11, E1.b1 and
E1.a2 keep their independent uniform laws, and (Y4, Y9, w8, E3.h1) keeps its law
and stays independent of (E1.d1, E1.b1, E1.a2). Hence, with G_S the event that R
= 0 with an outcome of S, Pr_M(G_S | c1 in Q*) = 2^11 Pr_M(G_S and c1 in Q*) =
2^11 * 67,633,152 * 2^-128 = p, the last step by the count of 10.1.

*Proof.* Translation by Y11 makes c1 uniform and independent of every other
coordinate. By the identity of the proof of Theorem C (iv), c1 lies in Q*
exactly when the difference is beta*, and Q* fixes 11 bits of c1, so the
probability is 2^-11. The event depends on E1.d1 alone, so for every event G1
of the words of E1 and G3 of the words of E3, Pr_M(G1 and G3 | c1 in Q*) =
Pr_M(G1 | c1 in Q*) Pr_M(G3). No independence of the output differences inside
E1 or inside E3 is used. QED. The finite counts behind 67,633,152 are those of
the counting program of Section 17 and are not proved by this lemma.

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

**Lemmas S6 and S7 of entry 26ebba63**, an E3 prescription and a cap of 3,072
complete successes in one outer step, are stated for the sub-class with rule A
and its seven outcomes, and this package does not use them. Its cap on the
successes of one outer step with an outcome of S is that of 9.4 with Lemma CV,
at most 16 listed good trials, and Lemma CV9 bounds the candidate roots of X3
(10.3).

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

**Lemma S9 (the success mass lies on passing outer steps; GPT Sol, answer AC).**
(a) *No hypothesis.* In every outer step that does not pass the filter, the
count N_o of H1' (10.3) is zero. Let pi_o be the probability that an outer step
of step 1 of 9.1 passes the filter, the share of the 2^256 values of its random
word whose outer step passes. If pi_o > 0, then E[N_o | the outer step passes] =
E[N_o] / pi_o. (b) *Hypotheses:* those of Lemma S1. Under M, also conditional on
c1 in Q*, Y9 and omega = Y3 + Y4 + w8 are independent uniform words, and the
filter passes with probability pi. G_S, the event that R = 0 and the E1 outcome
is in S, has probability p under M given c1 in Q* (Lemma S1 and the count of
10.1), and it lies inside the event that the filter passes. So Pr_M(G_S | c1 in
Q* and the filter passes) = p / pi = 1,032 / (279,070,422,111 * 2^53), about
2^-81.011, and Pr_M(the filter passes | c1 in Q*) times this conditional rate is
p: conditioning on the pass loses no part of p.

*Proof.* (a) A listed good trial has R = 0 with an outcome of S, so by Lemma F
its outer step passes; N_o is a count that is zero off the event that the outer
step passes, and E[N_o] = pi_o E[N_o | the outer step passes]. (b) Under M, Y9
and w8 are independent uniform words, independent of Y4; for fixed Y4, w8 ->
omega is a translation, so (Y9, omega) is uniform on all 2^64 pairs and
independent of Y4, and Lemma S1 leaves the law of (Y4, Y9, w8, E3.h1) unchanged
under c1 in Q*. The proof of Lemma F uses only the assignments of E3 and the
conditions of R = 0, which hold for the model words, so it gives the inclusion;
by 10.1 p is the part of the outcomes of S. Dividing by the probability pi of
the pass gives the conditional rate. QED. Statement (a) uses the pass
probability pi_o of the sampler itself; that pi_o equals pi is not proved (H4').
Statement (b) is about M and says nothing about the sampler. In this package
statement (a) is used for the widened filter of 9.8 and the whole count N_o of
H1', with Lemma F9 in place of Lemma F; the proof is the same.

*The search lists exactly the listed good trials.* The two lemmas below concern
the search of 9.1. Lemma V follows from 3.3 and is the participant's; Lemma RC
is GPT Sol's (answer CF 6); Lemma CV rests on the constants and guards of 9.4,
proved by GPT Sol (answers AE 4 and 7, AF 1.3, AO 6.1 and AR 1, 2 and 6.1),
among them the parity certificate (P*) and Lemma J0, which hold for every joint
root on the class.

**Lemma V (the certificate of a root).** Fix an outer step, a word c1 in Q* and
an outcome j of beta*, and let h be E3.h1 of the trial. The trial has R = 0
with E1 outcome j exactly when E1 on A and on B gives the XOR differences tau_j
and eps = 6e21be55 of its a and c outputs and h satisfies the joint conditions
(J1), (J2) and (J3) of outcome j (9.4).

*Proof.* Write tau, eps and beta for the XOR differences between A and B of
E1's a output, c output and first-half b value, and eta, psi, tau' and eps'
for those of E3's first-half d and b values and its c and a outputs, as in
Section 13. beta = beta* because c1 is in Q* (Theorem C (iv)), and eta =
830303cf (Theorem C (iii)). By 3.3, R is formed from o[1] = Z[1] XOR Z[9],
o[3] = Z[3] XOR Z[11], o[4] = Z[4] XOR Z[12] and o[6] = Z[6] XOR Z[14],
where Z[1], Z[6], Z[11] and Z[12] are the a, b, c and d outputs of E1 and
Z[3], Z[4], Z[9] and Z[14] those of E3. The first two values of E1 are the
same for A and B (proof of Theorem C (iv)), so the d and b outputs of E1
differ by ROR(tau, 8) and ROR(beta XOR eps, 7); by the last three
assignments of E3, its b and d outputs differ by ROR(psi XOR tau', 7) and
ROR(eta XOR eps', 8). So R = 0 exactly when tau' = tau, eps' = eps, psi =
tau XOR ROR(tau, 1) and eta = eps XOR ROL(beta XOR eps, 1), the conditions
of Section 13. For E1 outcome j, tau = tau_j and eps = 6e21be55, and the
last condition holds: 6e21be55 XOR ROL(18b0e098 XOR 6e21be55, 1) = 830303cf.
As in the proof of Lemma F, with h' = h XOR eta, g' = Y9 + h' and f' = ROR(y
XOR g', 12), psi = f XOR f' = ROR(g XOR g', 12), so psi = sigma_j exactly
when (J1) holds. Then f' = f XOR sigma_j and the a output of E3 on B is
(omega + DY3) + f', so eps' = eps exactly when (J2) holds. Then the d output
of E3 on B is ROR(h XOR eta XOR e2 XOR eps, 8) = h2 XOR mu and g' = g XOR
theta_j, so tau' = tau_j exactly when (J3) holds. QED.

**Lemma RC (the root certificate of the outcomes of S; GPT Sol, answers CF 6 and
6.1).** Fix an outer step, an outcome j of S and a word h, and let c1 be the
word that step 3 of 9.1 computes from h, that of the trial with E3.h1 = h (Lemma
IP), with E1.b1 = ROR(Y6 XOR c1, 12), E1.a2 = E1.a1 + E1.b1 + w5, s = E1.b1 AND
beta*, p = ((tau_j - beta* + 8 + 2 s) mod 2^32) >> 1 and z = ROR(E1.d1 XOR
E1.a2, 8). The four tests

    (Q)  c1 AND 0e09818b = 02008000,
    (A)  E1.a2 AND tau_j = p,
    (C)  (c1 + z) XOR ((c1 + DY11) + (z XOR ROR(tau_j, 8))) = eps,
    (T)  t != 0,

with DY11 = Y11' - Y11 = 0a08818b and eps = 6e21be55, hold exactly when c1 is in
Q*, t is not zero, and E1 on A and on B (6.2) gives the XOR differences tau_j
and eps of its a and c outputs.

*Proof.* The lines of step 3 are those of step CT read backwards from E3.h1 = h,
so they give the trial's Y14, Y6, E1.a1, E1.d1, c1, E1.b1, E1.a2 and t. (Q) is
the definition of Q*, and (T) is t != 0. Suppose (Q), and write a1, d1, c1, b1,
a2, d2, c2 for the assignments of E1 on A and primes for B (6.2). E1 on B has
the same a, b and d inputs and the same first message word, so a1' = a1 and d1'
= d1; its c input is Y11' = Y11 + DY11, so c1' = c1 + DY11; and b1' = b1 XOR
beta* (Theorem C (iv)), which is b1 + beta* - 2 s. With its second message word
w5 + fffffff8, a2' = a2 + Delta(s), Delta(s) = beta* - 2 s - 8 (as in 9.7). Now
a2 XOR a2' = tau_j exactly when a2 + Delta(s) = a2 XOR tau_j, that is when
Delta(s) = (a2 XOR tau_j) - a2 = tau_j - 2 (a2 AND tau_j) modulo 2^32, that is
when 2 (a2 AND tau_j) = (tau_j - Delta(s)) mod 2^32. Since tau_j[31] = 0, 2 (a2
AND tau_j) is below 2^32, and tau_j - Delta(s) = tau_j - beta* + 8 + 2 s is
even, as tau_j and beta* are; so this is (A). Given (A), a2' = a2 XOR tau_j, so
d2 = ROR(d1 XOR a2, 8) = z and d2' = ROR(d1 XOR a2', 8) = z XOR ROR(tau_j, 8);
with c2 = c1 + d2 and c2' = c1' + d2', c2 XOR c2' = eps is (C). The same
identities give (A) and (C) back from the two differences when c1 is in Q*. QED.
The lemma uses no law of the words; with Lemma V it says that a root of an
outcome of S is certified exactly when it is the E3.h1 of a listed good trial of
outcome j. The roots of X3 are certified by the full test of E1 on A and on B
(9.1, step 3; Lemma V9).

**Lemma CV (coverage of the search).** Fix an outer step that passes the filter,
with T = X AND VMASK[nu] of 9.7. (a) When T is not empty, step 2 of 9.1 returns
every joint root that satisfies (G7) and (G15) of every outcome whose bit is set
in T, each once, and nothing else. (b) Run over the whole list, step 3 certifies
exactly the roots that are the E3.h1 of a listed good trial of the outer step
with an outcome of S, and the E3.h1 of every such listed good trial is among the
roots; when T is empty the outer step holds no listed good trial with an outcome
of S (Lemma VP). So the number of certified roots of the outcomes of S of a
passing outer step, zero when T is empty, is the part of its count N_o of H1'
(10.3) with an outcome of S, the number of such listed good valid trials over
all of Q*, and that part is at most 16; Lemma CV9 of 9.8 adds the outcomes of
X3.

*Proof.* (a) A leaf gives a root only when (J1), (J2) and (J3) hold as words, so
every returned word is a joint root of the outcome it is returned with.
Conversely, take a joint root h of a searched outcome, with h satisfying (G7)
and (G15). By (PHASE), (P*), Lemma J0, (G7), (G15) and the constants and guards
of 9.4 its bits have those values, and its carries pass every test of (a), (b)
and (e) there: its own carry into bit 20 is a kept guess, every kept guess
reaches the common state at depth 7, and the single traversal follows the arcs
of its bits from the carry pairs that its own carries give, each read from the
array of its position with the guard values that its own bits give (at position
15 its prefix passes the test of (G15) and the prescribed bit is its h[15]), and
reaches its leaf, where the three conditions hold. A depth-first traversal
reaches each node once, so h is returned once. No word is a joint root of two
outcomes (9.4). (b) Let c1 in Q* give a listed good trial with outcome j, and
let h be its E3.h1. By the proof of Lemma F, h witnesses (1)_j for Y9 and the
trial's f witnesses (2)_j for omega, so bit j - 1 is set in both masks, and by
Lemma VP it is set in T; in particular T is not empty. By Lemma V, h satisfies
(J1) to (J3) of outcome j, so it is a joint root; it satisfies (G7) and (G15) by
Lemmas G7 and G15, and step 2 returns it by (a). Step 3 maps it to c1, since it
computes the inverse of the permutation c1 -> E3.h1 of Lemma IP; c1 is in Q*,
its t is not zero and its E1 outcome is j, so the root is certified (Lemma RC).
Conversely, by Lemma RC a certified root h of outcome j yields a word c1 in Q*
whose t is not zero and whose E1 differences are tau_j and eps, and h satisfies
(J1) to (J3), so by Lemma V the trial of c1 has R = 0 with outcome j: it is a
listed good trial. Different roots give different c1 (Lemma IP), and an outer
step has at most 16 roots of the outcomes of S (9.4). QED.

For the outcomes of X3 Lemma CV9 of 9.8 takes the place of Lemma CV. So in every
passing outer step that it reaches, the search of 9.1 certifies exactly the
listed good valid trials that an enumeration of all of U in that outer step
finds, with the same outer steps, the same members y and the same filter. The
count N_o of every outer step is the same, and with it the joint law of the
counts of the outer steps of a run: H1' is about these counts and H4' about two
counts of the outer steps, and neither changes (GPT Sol, answers AE 7 and AW 1).
Lemmas V, VP, G7, G15, RC and CV use no law of the words. The guards of the
solver are lossless: (PHASE) and (P*) are consequences of exact counts of the
class, (P*) with a count of 0 for the other parity in every phase and every
outcome (9.4), and Lemma J0 is algebra; none drops a member or a joint root. The
pre-check and the guards lose no listed good trial (Lemmas VP, G7, G15, G7b,
G15b and G20b), and drawing the outer steps seven to a batch changes no outer
step (Lemma PL).

**10.3 Heuristics.**

**Heuristic H1' (score-critical; restated for the union U and S9).** Over the
coins of the run, the RUN_STEPS independent uniform words of step 1 of 9.1, let
N_o be the number of listed good valid trials (9.1) of one outer step: trials
with c1 in U, t not zero, R = 0 and an E1 outcome in S9, counted over all of U
whether or not the outer step passes the widened filter or the pre-check. (i)
*Rate:* E[N_o] >= (2^22 - 1) q, with q = FACTOR * 2^-128, FACTOR =
70,943,656,228, just under 5 p9 / 7, about 2^-91.954. (ii) *No hit and
dependence:* the listed good trials of one outer step depend on each other
weakly enough that the probability that no valid trial of the run is a listed
good trial is at most exp(-0.49676) + 0.001.

This is the premise of entry 26ebba63 in its full form, rate and dependence,
restated for this search: the whole class of eta with no rule on h1, the nine
outcomes of S9 on the union U of two cubes, and the independent outer steps of
9.1, each with its own random word made of disjoint fresh bits (Lemma PL) (GPT
Sol, answers AO 3.1 and 6.3, AQ 1, AR 6.6, AT 2, AW 1 and AX 2.4). GPT Sol
prices this path only if H1' is restated for the union with its rate and its
no-hit and dependence clause (answer AX 2.4), and it is: neither the reviewed
clause of entry 26ebba63, for the sub-class with rule A and seven outcomes, nor
the H1' of entry 0bc5f130, for S on Q*, implies the law of these trials, whose
success event includes three outcomes of another beta on another cube: equal
model counts and equal budget constants do not identify the law of the count
N_o, and its factorial ratio rho need not be the same (GPT Sol, answer AT 2).
The premise is declared anew for these trials and S9. Neither the widened filter
nor the pre-check changes it: both skip only outer steps and outcomes that hold
no listed good trial (Lemmas F9 and VP), so N_o is the same count, pointwise
(Lemma CV9).

In the terms of Lemmas S1 to S4 the premise is this: the construction's
pushforward of the uniform outer words and members, with c1 running over all of
U, onto the seven model words (E1.d1, E1.b1, E1.a2, Y4, Y9, w8, E3.h1) carries
at least the share FACTOR / 99,321,118,720, just under 5/7, of the
complete-success integral p9 of the conditional law of 10.1; that stays true
after the members with t = 0 are dropped (Lemma IP); and the dependence between
trials that share an outer step is weak enough for the stated success at the
declared run length. The two parts are separate: neither follows from the other,
and neither follows from the model or from Lemmas S1 to S9. The factor FACTOR =
70,943,656,228 is assumed; 10.1 gives what it is set against, the count
99,321,118,720 of the nine outcomes of S9 on U, of which it is five sevenths
rounded down. The filter does not change it.

*The rate on passing outer steps.* N_o is zero on every outer step that the
widened filter rejects (Lemma F9, as Lemma S9 (a)), so (i) says E[N_o | the
outer step passes] >= (2^22 - 1) q / pi_o, with pi_o the sampler's pass
probability of the widened filter. Per member of U of a passing outer step the
rate is then at least about q / pi_o; for pi_o = pi9 it is q / pi9 =
70,943,656,228 / (23,384,160,813,285,376 * 2^64), about 2^-82.330, and in the
model p9 / pi9 is about 2^-81.845. The success argument below uses (i) per
walked outer step and needs no value of pi_o; pi_o enters only the pass budget
(H4').

*What is proved and what is not.* Proved (Lemmas S2 to S4): the outer words of
a step are uniform in the chart of the seven context words of Section 4; Y12
and w5 are independent uniform words; E1.a1 and E1.a2 - E1.b1 are independent
uniform words at every fixed c1; and the sampler of Section 8 is exactly the
uniform-counter sampler conditioned on c1 in Q*. For U the same sampler property
is not separately proved in this package: the algebraic reachability of every
c1 (9.8) is proved, its law is part of what (i) assumes. Proved as well (Lemmas
V, V9, CV and CV9): in every passing outer step that it reaches, the search of
9.1 certifies exactly the listed good valid trials of the outer step, so N_o is
the same count for it as for an enumeration of all of U. Not proved: that E1.b1,
E1.a2, E3.h1, Y9 and w8 have the model's joint law with the rest; GPT Sol 6.1
reduces part (i) to one success-weighted density of seven words that the outer
step fixes, Y12, Y1 + w12, C2.b1, C2.c1, w5, Y9 and w8, and that density has
not been counted. Not proved either: how much of the success mass the member
with t = 0 carries (Lemma IP bounds the number of dropped trials, one in 2^21,
not their mass), and the dependence inside an outer step.

For part (ii): the outer steps of a run are independent by step 1 and Lemma PL,
and by part (i) the run has RUN_STEPS * E[N_o] >= RUN_STEPS * (2^22 - 1) *
FACTOR * 2^-128 >= 0.49676. So by Lemma S8 part (ii) holds when rho = E[N_o
(N_o - 1)] / E[N_o] <= 0.0065: then b(rho) >= 0.99675, the exponent of Lemma S8
is at least 0.4951455, and exp(-0.4951455) < 0.609483 < exp(-0.49676) + 0.001.
That rho is this small is the assumption; it is not measured and cannot be at
full size. What is known of it: for the outcomes of S an outer step has at most
16 listed good trials (Lemma CV), and with X3 at most 16 + 32,768 candidate
roots (Lemma CV9), which does not help at this run length (GPT Sol's answer AO
1 shows the same for a cap of 64 on the sub-class). GPT Sol 6.1 proves the
bound 2^-13 for it in a model in which E1.b1, E1.a2 and E3.h1 are drawn afresh
for every member of Q*, and proves as well that the construction's own pair law
is not of that kind: for two members of one outer step the second member's
three words take at most 2^62 values given the first's, not 2^96. So that bound
does not transfer. A participant estimate on the sub-class, which is not a
proof, also puts rho near zero. On the whole class, the error of the E1 rate of
the seven outcomes of entry 59f8915e, which contain S, clustered by outer step
equals its Poisson value (Section 13), so there is no excess clustering of E1
outcomes by outer step; this bears on the E1 side only.

*No budget of steps 2 and 3.* The search of 9.1 declares no premise on the mean
of any count of work. Steps 2 and 3 need no budget of their own: in every outer
step that reaches them, whatever its words, the two solvers return a bounded
number of candidate roots and steps 2 and 3 cost at most the cap C_union =
314,996,576 machine units (9.8, Section 11). The final pair is formed and hashed
only for a certified root, after which the run halts, so it is formed at most
once and is a collision (Lemmas V, V9 and RC). The run halts with failure only
when one of the two counts of 9.1 exceeds its budget, which H4' covers, or after
the last outer step, which H1' covers.

**Heuristic H4' (supporting; the union count-budget clause of this package).**
For an outer step of the run, before any halt, let I_E be 1 when the mask of (2)
of its omega for S9 is not zero (9.8), and I_2 be 1 when its mask X is not zero
(it passes the widened filter); let N_E and N_2 be the sums of I_E and I_2 over
the RUN_STEPS outer steps. H4' says: with probability at least 0.9995 over the
coins, N_E <= E_BUDGET and N_2 <= PASS_BUDGET, both; so no budget halts the run.
It has two clauses, one for each count, and one failure allowance, 0.0005, for
their union (GPT Sol, answer AX 2.4: the new H4 union count-budget clause for
the widened E and pass indicators):

- *the pass budget*, N_2 <= PASS_BUDGET. Its nominal share is the exact share
  pi9 = 23,384,160,813,285,376 / 2^64 = 2^-9.6236188 of 9.8, for uniform
  independent pairs (Y9, omega).
- *the lean test-(2) budget*, N_E <= E_BUDGET. Its nominal share is p_E9 =
  305,100,224 / 2^32 = 2^-3.8152920, the exact share of words omega that pass
  (2) for S9 (9.8).

The outer steps of a run are independent and identically distributed (step 1 of
9.1 and Lemma PL), and each indicator is a function of the random word of its
outer step, so each N is binomial with RUN_STEPS steps and the sampler's
probability of its indicator; the two indicators of one outer step may depend
on each other in any way. Each budget is ceil(17/16 * RUN_STEPS * p) for its
nominal share p. A sufficient condition for H4' is that the sampler's
probability of each indicator is at most 1.06 times its nominal share: then each
mean is at most 1.06 / 1.0625 of its budget, the relative excess is at least
1/424, and the Chernoff bound puts the probability that a count exceeds its
budget below exp(-RUN_STEPS * p * 53 / 18,020,000): below exp(-1.1 * 10^14) for
N_E and exp(-2.1 * 10^12) for N_2 (participant arithmetic with GPT Sol's
form of answer AW 3). By the union bound the probability that some budget is
exceeded is then below 2 * exp(-2.1 * 10^12), far below 0.0005. That the two
probabilities are at most 1.06 times their nominal shares is not proved: the
sampler's Y9 and omega are not proved independent and uniform. What H4' needs is
these two counts, not a mean of any work: there is no solver budget (9.8), so no
share of the pre-check enters any budget, and the time bound depends on no
share. Measured (Section 13, participant evidence on the whole class, for the
six-outcome filter of S and not for the widened filter): on 60,000,000 real
outer steps, the count of (2) for S was 1.0004 +- 0.0005 and the pass count for
S 0.9980 +- 0.0041 of their nominal values. No measurement of the widened
filter, of its shares or of the outcomes of X3 was made for this package. If a
budget is reached the run halts with failure; the time bound charges each budget
plus one and is not affected. This is H4' of entry 26ebba63 for the widened
filter and this run, with the clause of the lean lanes (GPT Sol, answers AO 6.3,
AW 3 and AX 2.4).

**10.4 Success probability.** The probability space is the random words of the
RUN_STEPS outer steps of step 1 of 9.1, independent uniform 256-bit words made
of disjoint bits of the fresh draws (Lemma PL), for the fixed target. The
algorithm is otherwise deterministic. Under H1' and H4' it outputs a collision
with probability at least 1 - (exp(-0.49676) + 0.001) - 0.0005 > 0.3915 - 0.0015
= 0.39; the exact value of the bound is 0.390000993950... This is the union
bound over the two events "no valid trial is a listed good trial" and "a budget
is reached", which need not be independent: H1' bounds the first and H4', its
two clauses together, the second. A listed good trial lies in a passing outer
step (Lemma F9); an outcome of S is kept by the pre-check (Lemma VP) and an
outcome of X3 goes to the generic solver of 9.8; and the search certifies it
unless the run ends before its outer step is reached, by a budget or by the
output of another pair (9.1, Lemmas CV and CV9). When the algorithm outputs a
pair, the pair is a genuine collision: its trial is certified, so R = 0 (Lemmas
V and V9), step 3 checks both complete digests, and the messages have different
lengths. The run is the shortest of this form that gives 0.39: 0.49676 is the
smallest number of five decimals for which the bound reaches it, and with
0.49675 in its place the bound is below 0.389995.

*Sensitivity to the factor.* If the valid trials are listed good trials at f *
2^-128 each on average, with the dependence part of H1', the run gives at least
1 - exp(-f * RUN_STEPS * (2^22 - 1) / 2^128) - 0.0005, which reaches 0.39 only
when f is at least 70,708,919,222; the assumed FACTOR is 1.0033 times that. The
margin of the claim lies between the assumed 70,943,656,228 and the counted
99,321,118,720, a factor of 1.40. This package takes five sevenths of the count.
If the count is exact, the run has at least 0.6954 expected listed good trials,
and by Lemma S8 the bound 0.39 then holds for rho up to 0.576, that is when a
listed good trial has on average up to about 0.58 others in its outer step.

Neither heuristic is proved. Section 13 lists the evidence.

## 11. Charged time

One 2-round target compression costs one unit, and every other primitive word
operation, every load and every store included, costs 1/430 of a unit. The rows
below are in operations, loads and stores, called machine units here; 430 of
them make one unit of time.

*The machine.* The search and the selection procedure are charged on the
load/store machine of 6.5, with its 256-bit words, its packed lanes, its masked
rotation and its charge of one unit for every operation, load and store, with
two changes: it has 64 registers in place of 16, and every constant is an
immediate operand, written in its instruction and not loaded. The cost model of
the track charges primitive word operations and sets no register count; this
text charges as well a load for every other word fetched from memory into a
register and a store for every word written to memory, spills included. The
batch of seven outer steps runs on packed words (9.6); the rebuild of a passing
lane, the two solvers and step 3 run on scalar words of the same machine, one
32-bit value to a word. The schedules of this section are GPT Sol's (answers AL
2, AQ 2, AR 3 and 6.2 to 6.6, AT 1 and 4, AW 2 and 4, AX 1 and 2.4, BA 18, CD
11, CF 6 and 7, and CL 7 to 9), upper bounds written out by blocks, not counts
of an executed program; the counted parts are the 280 units of the batch that
the submitted program counts from its compiled code (9.6) and the 295 of the
rebuild of a passing lane, which a participant implementation counted (9.6).

**The cost, with every term.** Every row is machine units times an upper bound
on how often a run executes it; a row with a budget runs at most that many
times, plus the one that halts, because the algorithm halts with failure when a
count passes its budget (9.1). Exponents of counts and products are rounded up.

| Row | How often over a run, at most | Units | log2 of the product |
| --- | --- | ---: | ---: |
| batch of seven outer steps (9.6, 9.8): the eight random words, the lines of step CO that reach Y9 or omega on packed words, and omega (counted, 280), the advance of the batch count with its test (3), seven direct-table lane tests of the E table (41), the test of the last batch, the cursor and the dispatch (16), and one unit to spare | RUN_BATCHES = 2^66.138 | 341 | 74.551 |
| Q path of a lane whose mask of (2) is not zero: the E count in a fixed word with its test (6), the mask of (1) from the Q table at its Y9, the AND, the test and the branch (7) | E_BUDGET + 1 = 2^65.217 | 13 | 68.918 |
| passing outer step: the lane outside steps 2 and 3, that is the pass count, the rebuild of its outer step on scalar words, the context of the batch and the pre-check of 9.7 with the test of X_3 (512); and steps 2 and 3, the joint solver of 9.4 with (G7) and (G15) for the outcomes of T, the generic solver of 9.8 with (G7), (G15b) and (G20b) for those of X_3 and step 3 for every root (the cap C_union of 9.8, 314,996,576) | PASS_BUDGET + 1 = 2^59.409 | 314,997,088 | 87.640 |
| once: the direct tables of 9.8 (2^51); the static rows and descriptors (2^20); the automata of the filter, the three transition arrays, the written-out code of the search, and the row metadata, VMASK, array bases and initialisation (2^26 each); the resident constants and the last test (40); a final failed budget test (16); and six allowances of 2^20 for the guard and code changes of this package | once | 2,251,800,089,460,792 | 51.001 |
| **total** | | | **87.640** |

In exact integers the sum of the rows is 341 * RUN_BATCHES + 13 * (E_BUDGET +
1) + (512 + 314,996,576) * (PASS_BUDGET + 1) + 2^51 + 2^20 + 4 * 2^26 + 40 +
16 + 6 * 2^20 = 27,673,815,063,276,089,342,921 + 557,400,882,071,832,017,453 +
241,018,422,473,883,945,077,585,440 + 2,251,800,089,460,792 =
241,046,653,692,081,093,088,406,606 machine units (GPT Sol, answer CL 9, which
writes the one-time items as 2,251,800,089,460,792 = 269,484,072 + 2^51 + 6 *
2^20 + 16). The allowance of 2^26 for the automata of the filter is kept
although this search reads the direct tables; it is conservative.

*Why each budget plus one.* At most E_BUDGET lanes run the Q path, and at most
PASS_BUDGET passing lanes are rebuilt, pre-checked and run steps 2 and 3: in
each case the next one advances its count past the budget and halts the run
before the work of its stage. Each row charges its whole allowance for its
budget plus one, which covers these and the one that halts (GPT Sol, answer AW
4).

*The batch, 341, and the Q path, 13,* are those of the direct tables (9.8): the
counted 16, 262 and 2 of 9.6, the 3 of the batch count, the 41 of the lane tests
and the 16 of the last batch, the cursor and the dispatch, 340, charged 341; and
6 for the E count with 7 for the Q table, its AND and its test. A lane whose
mask of (2) is zero cannot pass and does not pay a Q path (Lemma PB).

*A passing lane, 512 outside steps 2 and 3* (GPT Sol, answers AQ 2, AT 4, AW 2
and AX 1.1): the eight words taken out of lane i by a shift and an AND, and step
CO on scalar words with all the names that steps 2 and 3 read, 295, counted by
the participant implementation (9.6); 16 for reloading the eight raw words with
their addresses; 32 for the other restoration of the caller; 16 for the pass
count, its comparison with the budget, the branch and the dispatch to the next
lane; 64 for storing and reloading at most 16 words of the context of the batch,
the mask X among them, in fixed memory words around steps 2 and 3, which may use
all 64 registers, at most 4 units a word: 423; 16 for the pre-check of 9.7 with
the test of X_3 (9.8); and 6 for storing C2.c1, C2.b1 and e1 in three fixed
words for the guards: 445, charged 512. It is paid by every passing lane, also
when T and X_3 are empty. The counts live in fixed memory words and are
reloaded, never restored from a stale copy.

*Steps 2 and 3 for the outcomes of S: C15(T), at most 17,504.* When T is not
empty, the part of steps 2 and 3 for the outcomes of S is charged block by
block, every block an upper bound on its operations, loads and stores, with
addresses, branches, spills and the restoration of registers included (GPT Sol,
answers AL 2, AR 3, AR 6.3 to 6.5, AT 1, AW 2, AX 1.1, CF 6.5 and 7.2 and CD
11.2):

- 1,024 once, the global ledger below; none when T is empty.
- 2,304 for each family (9.4): at most 128 blocks of the formulas of (a) to (e)
  of 9.4, the phase checks, (P*) and their preparation, at 12 units each, 1,536
  (the 112 blocks of the formulas of answer AI 2 and 16 more; a block is the
  extraction of one source bit, a majority of four operations, an XOR of at most
  five inputs, the comparison or choice of a carry prescription, or a carry
  update, with its branch and assignment); the walks of bits 0 to 5 under the
  two guesses, at most 32 units a bit, 384; and 384 for the record of the
  family, which at most two rows of a set share (64 to store a record of 32
  words and 128 to load it twice), the packing of the guard planes and the
  dispatch.
- 1,408 for each searched row. Its 32 descriptors are built in 32 registers at
  32 units each, 1,024 (seven fields vary with the outer step, Q[i], y[i], E[k],
  E'[k], kappa[k], kappa[k+1] and the value of a constant, at 4 operations each,
  and 4 for the static base, the shift of the key and the assignment); 128 for
  the walks of bit 6 under the two guesses (64), the patches of h[6], h[7],
  h[13] and h[26] (24), kappa and the consistency of bit 6 (8), and the dispatch
  of the row (32); the guard (G7) of 9.7 adds 128 (answer AX 1.1), and the guard
  (G15) of 9.7 128 more for its five words (answer CF 7.2).
- 20 for each forced node: the key from the carry pair, the descriptor and the
  base of the array, and the read, 3; the validity, its comparison and the
  branch, 3; the next carry pair and the saved bit e2[29] (at position 9 the new
  bit is put in its place), 3; the chosen bit of h, shifted to its place and
  ORed into the prefix, 3; the guard of position 25 or 29 written into the key,
  at most 7 (at 25, bit 13 of the prefix shifted and masked, XORed with h[6] XOR
  u, which is held, shifted and ORed into the key, 5; at 29, the saved bit
  e2[29] masked, shifted and XORed into the key, 3); and the continuation, 1.
- 4 more for each selected node, at position 20: bit 8 of the prefix as the
  desired bit of the key of the selected array.
- 64 more for each node at position 15: the test of (G15) and the prescription
  of h[15] in a temporary copy of the descriptor (9.7).
- 48 for each free node: the parent saved in one register, 2; the key and the
  read of the dual array, 3; the two arcs taken apart, 2; 11 for each of the two
  children, for the validity, the carry pair and the saved bit, the prefix and
  the control; the parent restored before the second child, 2; and 5 for
  dispatch and return: 36, charged 48. No guard reads a free position.
- 80 for each leaf: g, f, e2 and h2 of its h and (J1), (J2) and (J3) as words, a
  rotation at five operations, 64; and 16 to reload the context words.
- 120 for each root: the certificate of step 3 (Lemma RC), run at the leaf of
  the root: Y14, Z, Y6, E1.a1, E1.d1 and c1, 22; the test (Q), 3; E1.b1, s,
  E1.a2, p and the test (A), 16; z and the test (C), 15; Y2, w0, K0.a1, t and
  the test (T), 17; twelve addressed loads, h, e1, C2.c1, C2.b1 twice, Y1,
  w12, Y12, w5, K0.d1, C2.a1 and C2.d1, 24; dispatch, return and control, 16:
  113, charged 120. A rotation on scalar words takes four units (two shifts,
  an OR and a mask), every sum is masked to 32 bits, and Y11, beta*, DY11,
  eps, IV[0] + IV[4] and the constants tau_j - beta* + 8 and ROR(tau_j, 8) of
  each row are immediates of the written code (answers CF 6.2 and 6.5).

*The global ledger, 1,024 (GPT Sol, answer CD 11.2).* This is a specified
layout, not a count of a program. The lane of 9.6 has finished its paid
pre-check when it calls steps 2 and 3. So that the lane stores nothing for the
solver, steps 2 and 3 repeat the scalar rebuild of step CO and store the names
that they read as these become available, in a fixed bank of 32 memory words,
disjoint from the words of the batch, the family records and the words of (G15).
The names are the seven outer words, Q, y, E, e1, C2.a1, C2.b1, C2.c1, C2.d1,
Y1, Y12, w5, w12, K0.d1, E' and E XOR E', and the two phase bits: 24 words, each
stored before its register is reused. Every word of the bank that is read later
was written in this outer step, and no other word of it is read, so the bank
needs no clearing. Every address is a fixed offset from an immediate base, and
every name of a word, register and row is written in the code; nothing is looked
up by value. Once for a nonempty T:

| item | units, at most |
| --- | ---: |
| the scalar rebuild of step CO, repeated (295), and the addressed reloads of the eight raw words (16) | 311 |
| up to 32 addressed stores of names into the bank, 2 each | 64 |
| E' = E + DY3, E XOR E', the phase fields, their normalisation and stores | 16 |
| loading sources at the boundaries of families and rows | 128 |
| the choice of outcomes and families from the fixed mask, and the top-level dispatch | 128 |
| entry into the frame, bookkeeping of bank slots and control, and the final return | 128 |
| unused reserve | 249 |
| total | 1,024 |

The loads cover five source words for each family, at most three families, 30,
and six context words for each row, at most three rows, 36, with 62 to spare;
the reloads of a leaf and the loads of (G7) and (G15) keep their own allowances
above. The choice runs a fixed decision tree over the six bits of T: six bit
tests at 6 units each, three family entries and three row entries and exits at 8
units each, and 16 for entry and exit, 100 in all. The last 128 pay the call and
return edges, the preparation of the bank base and offsets, and up to 32 further
addressed accesses. Each root is certified at its leaf and a rejected root
returns straight into the traversal (step 3), so no list of roots is kept,
allocated or sorted.

Summing the blocks: when an outer step reaches the joint solver with searched
outcomes T, its part of steps 2 and 3 costs at most C15(T) = 1,024 + 2,304 F +
1,408 A + 20 N_f + 48 N_r + 4 N_s + 64 N_15 + (80 + 120) Lf machine units, where
A counts the rows of T, F their families, N_f, N_r, N_s and N_15 their forced,
free and selected nodes and their nodes at position 15, and Lf the leaves of
their trees with (G7) and (G15) in 9.4; roots are at most leaves. The four sets
of rows of 9.4, restricted to the outcomes of S, contain every T that occurs:

| rows searched, among | A | F | N_f | N_r | N_s | N_15 | Lf | cap of steps 2 and 3 for S |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 275 | 1 | 1 | 80 | 7 | 4 | 4 | 8 | 8,544 |
| 175 | 1 | 1 | 42 | 3 | 2 | 2 | 4 | 6,656 |
| 285, 385 | 2 | 1 | 160 | 14 | 8 | 8 | 16 | 13,760 |
| 185, 385, 685 | 3 | 2 | 164 | 13 | 8 | 8 | 16 | 17,504 |

So the part of steps 2 and 3 for the outcomes of S costs at most 17,504
machine units in every outer step that reaches it, whatever its words and
whatever its T, which the pre-check never enlarges: 1,024 + 2 * 2,304 + 3 *
1,408 + 20 * 164 + 48 * 13 + 4 * 8 + 64 * 8 + 200 * 16 = 17,504 on the rows
185, 385 and 685 (GPT Sol, answers CF 7.2, CD 10 and CD 11.3; the trees and
the arithmetic recomputed by the participant). The counts are those of the
static trees, and the blocks are added whether or not they occur together, so
this is an upper bound; it is not claimed to be attained or to be the least
such bound.

*Steps 2 and 3 for the outcomes of X3, at most 2 * 157,489,536.* Each row of X3
whose bit is set in X_3 is charged its row cap C_row of 9.8 (GPT Sol, answers CL
7 and CL 9): 8,576 for its set-up with the constants of (G7), the words of
(G15b) and the sources of (G20b), 512 per node and 8,192 per leaf of the trees
of both guesses of a20, and 64 more per node at positions 7, 15 and 20; at most
two rows occur together, and the two largest give 314,979,072.

*Steps 2 and 3 of this package, 314,996,576.* Every passing outer step is
charged C_union = 17,504 + 314,979,072 of 9.8, also when T and X_3 are empty,
which needs no count of the outer steps that reach the solvers. The part for S
does not rely on scratch values of the part for X3 or the reverse: each row of
X3 imports and rebuilds its sources inside its own 8,576, and the part for S
rebuilds its bank inside its 1,024.

*Registers of steps 2 and 3* (GPT Sol, answers AL 2, AR 3 and 6.3, CF 6.5 and
7.2). The search of 9.4 is written out statically for each row and each prefix
of free choices: a node at a prescribed position has at most one child, whose
code follows that of its parent, and a leaf label jumps to the leaf check; a
node at a free position, at most five on a path, saves its parent in one
register, the prefix of h and, above bit 32, the two carries and the bit
e2[29], the only earlier output bit that a later guard reads (the guard of
position 25 reads bit 13 of the prefix). The registers of the traversal are the
32 descriptors, five saved parents, six context words, eight constants, array
bases and control words, two words of the current state and ten temporaries: 63
of the 64. A leaf keeps the descriptors and the saved parents and uses the
others for its check, after which the context words are reloaded (the 16
above). The certificate of a root and the test of (G15) use only the ten
temporaries, with no spill. The formulas of a family run before the descriptors
are built, in at most 58 registers: at most 35 bits and carries, five source
and context words, eight table, literal and control words and ten temporaries.
The repeated rebuild and the stores into the bank run with the words of the
batch already saved, so all 64 registers are free for them. The generic solver
of 9.8 holds its parents in statically addressed scratch frames and adds no
traversal register. No register is addressed by a value: every position and
register is named in the code.

*Once.* 2^51 for the two direct tables of 9.8, 2^33 entries at most 2^18
operations each (GPT Sol, answer AX 2.4). 2^20 for the six static rows of the
outcomes of S, the static fields of their descriptors at the 32 positions and
the metadata of the batches. 2^26 for the two automata of the filter, built and
composed into eight byte tables whose entries hold the base address of the next
table, with the entries of the last tables ANDed with the outcome set (GPT Sol,
answers AN 2 and AQ 2). 2^26 for the three transition arrays of 9.4: their 2^18
entries at most 256 operations each, the enumeration of the keys, both candidate
arcs, the test for an invalid or a second arc, the selection and the store
included (answer AR 6.2). 2^26 for writing the code of the search, with the
prescribed bits of (G7) and (G15) at positions 7 and 15, fewer than 2^14 labels,
at most 256 operations each with their set-up (answer AL 2). And 2^26 for the
row metadata, the absolute bases of the arrays and their initialisation (answer
AR 6.2), which also covers the enumeration of the compatible patterns of 9.7,
the eight words of VMASK and the descriptors of the three rows of X3. 32 for
loading the resident constants and array bases into their registers, 8 for the
test of the final halt, and 16 for a final failed budget test, kept
conservatively (answer AW 4). And 6 * 2^20 for the guard and code changes of
this package (GPT Sol, answers CL 7 and CL 9): the code of (G15) with the layout
of the five words of a row; the global ledger with its bank of 32 words and its
labels; the root certificate of Lemma RC with the immediates of the rows and at
most 1,024 units to form the last blocks of the first returned pair; the
constants and metadata of (G7) and (G15b) for the rows of X3; the written-out
code of the generic solver with the modified initialisation; and the metadata
and code of (G20b).

*One-time items.* The items above are in the last row. The final step, once:
steps CT and CS for the trial found, writing the two messages, shorter than 2^42
bytes each, and two complete evaluations of blake3; each message has at most
2^32 chunks of 16 compressions each and fewer than 2^32 parent compressions,
below 2^37.1 compressions for both, and writing them is below 2^38 machine
units: below 2^38 units of time in all, charged as 430 * 2^38 machine units.
Preprocessing: the selection procedure SEL of Section 12, charged in full at its
cap by construction, S_old = 8,882,224,365,081,579,520 machine units, below
2^54.198 units of time.

Total:

    T <= (sum of the rows) / 430 + 2^38 + S_old / 430
      <  2^78.8913.

In exact arithmetic the numerator is

    N = 341 J + 13 (E + 1) + (512 + 314,996,576) (P + 1) + D + S_old + 430 * 2^38
      = 241,046,662,574,423,655,669,972,046

machine units, with J = RUN_BATCHES, E = E_BUDGET, P = PASS_BUDGET, D =
269,484,072 + 2^51 + 6 * 2^20 + 16 = 2,251,800,089,460,792 and S_old of Section
12 (GPT Sol, answer CL 9, recomputed by the participant in integers term by
term). T = N / 430 = 560,573,633,894,008,501,558,074.52... units, and log2 T =
78.89125007243636...; in integers, N^10000 < 430^10000 * 2^788913 and N^10000 >=
430^10000 * 2^788912. The claimed time_log2 is 78.8913, this total rounded up at
the fourth decimal. The bound holds in the worst case for the algorithm as
stated: every run halts within its two budgets and its RUN_BATCHES batches,
steps 2 and 3 are bounded in every outer step that reaches them, and SEL is
bounded by its caps. No mean of a count of work enters it; H1' and H4' bear on
the success probability only. The claim rests on this schedule on 64 registers:
no figure on 16 registers is claimed, and the schedule is not claimed to be the
cheapest.

*Where the sum goes.* The passing outer steps are 99.9883 per cent of the sum of
the rows, almost all of it the rows of X3; the batches are 0.0115 per cent, the
Q paths 0.0002 per cent and the one-time items less than 10^-8 per cent. Per
walked trial, RUN_STEPS * 2^22 of them, the sum of the rows is 0.10116 machine
units.

The algorithm has no sorting and no lookup by value: a root is tested against
the conditions of its outcome, and a certified trial is not compared with other
trials. It reads the two direct tables of the filter (9.8), the E table at omega
in every lane of a batch and the Q table at Y9 in a lane whose mask of (2) is
not zero, each at an address given by the whole word; in a passing outer step,
the stored words of its batch and the entry VMASK[nu]; in steps 2 and 3, the
three transition arrays at the keys of the searched rows, the five words of
(G15) of each searched row of S, the family records, the bank of the global
ledger, the static rows of the outcomes of S and the descriptors and scratch
frames of the rows of X3. Every such read is charged as one load: a batch counts
its 7 loads of the E table inside the 41 of its lane tests, a Q path its load of
the Q table inside its 7, and the loads of a passing lane, of the pre-check, of
the two solvers and of step 3 are inside the allowances above. No table grows
with the trials.

## 12. Memory, preprocessing and advice

The program of the search is the lines of steps CO, CT and CS, the outer filter,
the batch of 9.6, the joint solver of 9.4 with its statically written traversal
and the guards (G7) and (G15), the generic solver of 9.8 with (G7), (G15b) and
(G20b), and a compression routine for step 3 and the final check: below 2^28
bytes of code and metadata (Section 11). Data, one word of 256 bits each unless
said otherwise: the two direct tables of the widened filter, 2^33 words, 2^38
bytes (9.8); the 31,488 entries of the tables of the filter's two automata, from
which the direct tables are built; the three transition arrays of 9.4, 2^18
words of 32 bits, 2^20 bytes; fewer than 4,096 words for the joint solver (the
descriptors of the positions of a row, the six static descriptors of S, the
records of the families, the bank of 32 words of Section 11 and scratch); fewer
than 4,096 more words for the descriptors and the statically addressed scratch
frames of the generic solver of 9.8; and fewer than 1,024 words for the names of
step CO, the stored words of a batch, the five words of (G15) of each row, the
words of (G15b), the constants and masks, VMASK, the two counts and the cells of
step 3. The memory of the search is therefore below 2^38 + 2^28 + 2^21 + 2^20 +
2^19 < 2^39 bytes. Nothing grows with the number of trials. The two messages of
a found pair have 1024 t + 55 and 1024 t + 63 bytes with t < 2^32, each shorter
than 2^42 bytes; the output, the two messages with their digests, takes less
than 2^43 bytes.

**The advice record.** The search reads a fixed record, stated here in full,
which this package treats as nonuniform advice: the six constants X3 = 29d4fa98,
X7 = bee3af28, X11 = 44036000, X15 = 40c58500, W4 = 97475638 and W13 = 0007c006
of 3.2, 24 bytes; eta = 830303cf, 4 bytes; beta* = 18b0e098 with the mask
0e09818b and the value 02008000 of its cube, 12 bytes; the seven values of tau
of the filter's automata, 175020a0, 185020a0, 275020a0, 285020a0, 385020a0,
675020a0 and 685020a0, and eps = 6e21be55, 32 bytes; the mask 5f of S, 1 byte;
and for X3, beta3 = 18d0e098 with the mask 0e09818d and the value 02008001 of
its cube, 12 bytes, its eps 6e61be55, 4 bytes, and one byte that names the three
values of tau of X3 among the seven: 90 bytes in all, so
nonuniform_advice_log2_bytes = 7.

The success analysis of 10.3 and 10.4 uses only properties of this stated
record, and this text verifies each of them exactly, whatever the way the record
was found: Fact P, the equal d and b outputs of C3 for W4 and W4' (3.2); Lemma
Q, the class of eta with exactly 524,288 members; Theorem C (iii) and (iv), by
which c1 gives the difference beta* exactly when c1 AND 0e09818b = 02008000, and
its form for beta3 and Q3 (9.8); the fourteen outcomes of beta* on the class,
all with eps = 6e21be55, and the count 67,633,152 = 1,032 * 2^16 of the six of S
(10.1, with the program of Section 17); Lemma V9 for beta3 and eps 6e61be55; the
certificate of the filter for S, with its share, and the widened counts of S9,
which the self-test of 9.3 recounts from the program's tables (Section 8, 9.8);
and, for the search itself, the allowed patterns of the pre-check (9.7) and the
guards, trees and caps of the two solvers (9.4, 9.8, Lemmas J0, G7, G15, G7b,
G15b, G20b and RC, Section 11). The three parts of X3 in R9 are GPT Sol's counts
from the participant's integer records (9.8). H1' and H4' are stated for this
record (10.3). Nothing in the success analysis depends on how the record was
found, on a selection returning it, or on any record of the runs that found it.

**The selection procedure SEL.** The advice record was found by a solver search
and one count per model, which the submitted program does not contain. This
section writes that search as a procedure, SEL, and charges its whole cost as
preprocessing, included in T (Section 11). The cost model charges any search
omitted from the submitted program; SEL is that search, and its whole capped
cost is charged. The charge is a bound by construction: every search of SEL runs
over a range stated here, and every run of a program in SEL halts as soon as it
has executed a stated number of primitive word operations, its cap, or holds
2^34 bytes; a run that halts so returns nothing, and SEL goes on. Operations are
counted as in Section 11, 430 to the unit. SEL runs two programs of the
participant that are not in the package: the solver kissat, on instances made by
a generator of the participant, and the counter of Section 13, which computes in
integer arithmetic the part of one beta in the rate of the class of a given eta,
with no rule on h1; a run of the counter whose part would be 2^192 or more
counts as one that reaches its cap.

*Step 1, the pinned call (solver runs).* For each of the 116 runs of the
participant's solver log for this search (51 runs for the lengths 55 and 63, the
other 65 for nine other variants of the instance; bounds 97 to 118; logged
seeds), build the instance of the run and run kissat on it with the logged seed,
the two together with a cap of 2^56 operations. For the lengths 55 and 63 the
instance is that of entry c66f230d (its Section 10): the call C3 for both
messages with equal b and d outputs, the two words w4 related as the length
cancellation prescribes for the XOR 8 of the lengths, the top byte of word 13
zero, E1 and E3 for both messages, a zero residual, and a bound on the number of
bit positions, bit 31 excepted, at which a difference is active in six additions
of E1 and E3. A run that finds a model returns six constants X3, X7, X11, X15,
W4, W13 and the values of a solution, among them its Y4 and its beta. Cost: at
most 116 * 2^56 < 2^62.86 operations.

*Step 2, the constants, the class and beta* (a count for each model).* For each
model of step 1, compute Y3 and Y3' by C3 from its constants, its class eta =
ROR((Y3 + Y4) XOR (Y3' + Y4), 16) from the Y4 of its solution and its beta from
the c1 of its solution, and with the counter the part of that beta in the rate
of the class of that eta, with a cap of 2^52. Output the six constants, the eta
and the beta of the model with the largest part, the first in the order of the
log if parts are equal. Cost: at most 116 * (2^52 + 2^10) < 2^58.86 operations.

*Step 3, the cube, the outcomes and S.* With DY11 = Y11' - Y11 for the output of
step 2, form the mask ROL(beta, 12) AND 7fffffff and the value (ROL(beta, 12) -
DY11) / 2 of the cube of the words c1 that give beta (proof of Theorem C (iv)),
and the outcomes (tau, eps) of beta whose product L * N3 is not zero, which the
count of step 2 lists; for beta* these are the fourteen of 10.1. Then, for each
of the 16,383 nonempty sets S of these outcomes, compute in integers the
numerator O(S) of the ledger under which S was chosen, that of the six-outcome
search of entry 0bc5f130 (424 per batch, 35 per Q path, 512 per passing lane and
the cap of S per outer step that reaches the solver, each at its budget plus
one, and the one-time row): its count from the rows of step 2, its FACTOR,
RUN_STEPS and RUN_BATCHES on 2^21 - 1 trials; its E_COUNT, SHARE and its count
of the pre-check from the mask certificates of the two automata of the outcomes
and the allowed patterns of 9.7; its three budgets; and its cap, the largest
restricted ledger of 9.4 over the four maximal row sets and the eight values of
nu. Output the S with the least O(S), the first in increasing order of its mask
if two are equal, and the outcomes whose tau has bit 14 equal to 0, from which
the outer filter's automata are built when S lies among them. Step 3 and the
bookkeeping of SEL run under a cap of 2^50 operations. SEL does not choose beta3
or X3: this text fixes them (9.8), and the search stores them as advice.

**The bound.** Steps 1 to 3 cost at most

    S_old = 116 * 2^56 + 116 * (2^52 + 2^10) + 2^50 = 8,882,224,365,081,579,520

operations, below 2^62.946 (in integers S_old^1000 < 2^62946), and so below
2^(62.946 - 8.748) < 2^54.198 units (S_old^1000 < 430^1000 * 2^54198).
preprocessing_log2 = 55 is this bound rounded up to a whole number, and the
whole of S_old is in T (Section 11). It bounds SEL as defined, whatever the two
programs do inside and whatever they return, because every run halts at its cap
and every loop has the range stated. SEL is not a premise of this package, and
no heuristic is declared for it.

*What rests on records.* The bound rests on no record. That SEL returns exactly
the six constants of 3.2, eta = 830303cf, beta* = 18b0e098 and S = 5f rests on
the participant's records: for S, on GPT Sol's exact comparison of the 16,383
sets (answers AW 4 and AX 1.2); for the rest, on the participant's solver log,
by which the run for the lengths 55 and 63 with bound 104 and seed 506 found
these constants after 4,770 seconds, with a solution of class 830303cf and beta
18b0e098, and on an exact integer recount, by the participant's counter on the
whole class of each instance, of all 65 distinct instances that the runs of the
log returned with a model, in which these constants have the part 71,698,432,
the largest, and the next is 13,107,200 (a strict maximum, 5.47 times the next).
Every run of the log stopped within 9,010.5 seconds on one processor core and
every recount within 320 seconds; at 2^42 operations a second for a core, a rate
the participant states and does not prove, every run stayed below 2^55.14
operations and every recount below 2^50.33, inside the caps. The log does not
fix every instance: some runs excluded pairs that runs finished before them had
found, and 32 runs were stopped from outside without a record of the cause. So
the records certify a historical run of the solver, not a replay with operation
caps, and the generator of the instances, the solver log and the counter are not
in the package. If a record were wrong, SEL could return other constants or
none; its cost would stay within the bound.

*Memory of SEL.* Every program run of SEL halts when it holds 2^34 bytes, and
SEL runs one program at a time; its own data stay below 2^20 bytes, the parts of
step 2 and the outputs. SEL therefore holds fewer than 2^34 + 2^20 bytes at any
time; the search fewer than 2^39 bytes, its direct tables included; the output
fewer than 2^43 bytes. Held at once, these total below 2^43 + 2^39 + 2^35 <
2^44: memory_log2_bytes = 44 bounds all. The measurements of Section 13 are not
part of SEL: they test the heuristics and select nothing. The cost model does
not score memory.

The direct tables, like the tables of the filter's automata, VMASK, the three
transition arrays, the descriptors and the traversal, are not advice: they are
computed from the record. SHARE and E_COUNT are counts from the certificate of
Section 8 widened in 9.8, and the budgets of 9.1 are computed from them and from
the other constants of 9.1. The flags 3 and the counter rule are part of the
algorithm. There is no other stored data and no stored collision.

## 13. Evidence, scope and field meanings

Throughout this text costs and bounds are rounded up, and margins, rooms and the
whole numbers of the count that the claim uses are rounded down. Counts printed
with decimals are rounded to the nearest.

**What is exact.** Sections 2 to 5, 7 and 8; Lemmas L, H, Q, Q2, T, T2, N, A,
TR, CT, IP, F, F9, V9, TAB, J0, PL, PB, V, VP, G7, G15, G7b, G15b, G20b, RC, CV
and CV9 and Theorem C; the count of passing pairs of Section 8 and the widened
counts of 9.8; the allowed patterns of the pre-check (9.7); the parity
certificate (P*), an exact count; the trees and caps of the two solvers (9.4,
9.8) with their schedules (Section 11), as upper bounds; and Lemmas S1 to S9
under their stated hypotheses. Lemma A says what rule A tests in the root
instance; the search of this package does not use rule A. The declared
experiment `union-search` runs the search of 9.1 with 9.8 on the root instance
per organizer seed, and the organizer recomputes both digests of the returned
pair; Theorem C, read at counter 0 and flags 11, predicts that every pair agrees
on the 128 masked digest bits. The counter instance has no organizer-run check
(6.4).

*Who proved and who checked the exact part.* Lemmas L, H, Q, T and N and Fact P
are those of our entry c66f230d; Lemma TR, the counter order with Lemma CT and
Theorem C were written by helper agents of the participant; Lemmas IP and S1 to
S8 and Lemmas F and S9 were proved by GPT Sol 6.1 (answers AC and 6.1); the
joint solver of 9.4 with its constants, guards and caps, the lean lanes, the
pre-check, the guards (G7) and (G15), Lemma RC, the widened filter with Lemmas
F9, V9 and CV9, the direct tables and the guarded generic solver with Lemmas
G7b, G15b and G20b are GPT Sol's (answers AE, AF, AI, AL, AO, AQ, AR, AT, AW,
AX, BA 18, CD 10 and 11, CF 6 and 7, and CL 2, 3, 7, 8 and 9); Lemma V is the
participant's. The participant's checks of the exact part are computations, not
proofs: the counter construction against the organizer's own functions on 2,000
trials, with 204,000 internal words compared with a separately written forward
computation, and complete messages hashed by the organizer's code (Section 7);
all 2^21 members of Q*, each giving the difference beta*; the rule t != 0
(Section 8); the free positions, static trees, families and caps of the joint
solver, and the sums of the cells of (P*) against the counts of 10.1, with a
separate count of (P*) in one phase of 2^16 members (9.4); the word nu of the
pre-check against the bits s[13] to s[15] of 324,098 real trials (9.7); and the
self-test of the submitted program (9.3): the automata of the ten outcomes
against brute force, the counts of passing pairs for S and S9 from its own
tables, the static trees and caps of the rows of X3, Lemma G20b for every value
of f AND sigma on the three rows, every packed lane against step CO on scalar
words, the generic traversal with (G20b) on planted words, and the four guards
on words of both cubes. These are checks, not proofs, and no person has read any
part of this text.

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
from it (Lemma CT (c)), and E1.b1, E1.a2 and E3.h1 move with d1. M is a
statement about averages over the outer steps of a run. Lemmas S2 to S4 show
which parts of it hold exactly for the construction, and H1' declares the rest.
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
are 3.9 to 31.8 on the eight sets, against 853.61 for S on Q*), and it has no rule A,
no sub-class and no packed batch.

**Real messages in passing outer steps.** A participant measurement made for
this package, untrusted evidence like the two paragraphs before it, which the
organizer's harness does not run. On a graphics card a helper agent ran the
counter construction on real 32-bit messages with Y4 in the sub-class. Uniform
random outer steps, drawn by the measuring program, were filtered by conditions
(1) and (2) with tables generated as the program of entry 26ebba63 generates
them, and every passing outer step enumerated the whole of Q*, all 2^21 values
of c1 in that program's member order, as 299,594 words of seven lanes in the
layout of the run-wide table: 2^22.00 passing outer steps, 2^43.00 trials. A
control with the filter off ran 2^18 outer steps, 2^39 trials. On 330 records a
check against that program (step CO, the filter, the member order, rule A and
the word n of the E1 test from that program's compression of the real last
chunks) found no difference. Errors are taken per outer step, because the trials
of one outer step cluster.

| Event | Over all outer steps | In passing outer steps | Ratio |
| --- | --- | --- | --- |
| outer step passes the filter | 2^-9.8132 (pi, exact) | 2^-9.8127 | z = +0.7 |
| rule A, per lane | 2^-8 | 2^-8.000 | 1.0003 +- 0.0006 |
| E1 test of Lemma N passed, per trial | 2^-26.02 | 2^-26.023 | 0.9945 +- 0.0031 |
| listed E1 outcome, per trial | 2^-31.694 | 2^-31.724 | 0.979 +- 0.022 |
| listed partial E3 event, per trial | about 2^-32.4 (control, 98 events) | 2^-24.17 | about 2^8 |

So inside passing outer steps rule A and the E1 test keep their values over all
outer steps, and the listed E1 outcome keeps its value within its error. Per
outer step the count of trials that satisfy rule A has standard deviation 9,785
against a mean of 8,195: the trials that satisfy it cluster. Over the 12
patterns of the filter's masks with at least 40,000 passing outer steps each,
rule A lies between 2^-8.006 and 2^-7.996 and the E1 test between 2^-26.08 and
2^-26.00. The partial E3 event, a condition on E3 like (1) and (2), is
concentrated by the filter, as expected. Trials with t = 0 were not dropped, at
most one per outer step. These measurements bear on H4' and on the rate of H1'
inside passing outer steps; they reach no event deeper than about 2^-31.7 and
no collision.

**Real counter trials on the whole class.** A participant measurement made for
the class, untrusted evidence like the paragraphs before it, which the
organizer's harness does not run. On a graphics card a helper agent ran the
counter construction on real 32-bit messages in two classes of one build: the
whole class of eta (all 2^19 members, no rule, the filter of the fourteen
outcomes of beta*), and as a control the sub-class of entry 26ebba63 with rule A
and the seven-outcome filter. Each run walked 2^35 uniform random outer steps
and enumerated all of Q* in 2^25 of its passing outer steps, 2^46 trials per
class; the passing steps kept are the first in the order of the card's atomic
counter, which does not depend on their content, and the pass share uses every
walked step. Before the runs, the filter tables were compared with the
construction of the program of entry 26ebba63, 1,000 members of each class with
the member lists, and a sweep of all 2^32 values of tau and of eps at beta*
showed that the counters list exactly the fourteen and the seven outcomes of
10.1; no trial lacked the difference beta*. The counters are the E1 outcome and
the filter; errors are clustered by outer step. The model per trial is the sum
of L_j over the listed outcomes times 2^-85 (2^-96 for the triples times 2^11
for c1 in Q*).

| Event | Exact model | Measured | z |
| --- | --- | --- | --- |
| E1 outcome among the seven of entry 59f8915e, whole class | 53 * 2^-38 = 2^-32.2721 per trial | 2^-32.2692 (13,595 events), 1.0020 +- 0.0086 of the model | +0.23 |
| the same, sub-class control | 2^-32.2721 | 2^-32.2540 (13,739 events), 1.0126 +- 0.0086 | +1.46 |
| ratio whole class / sub-class, the seven | 1 | 0.9895 +- 0.0120 | -0.87 |
| E1 outcome among all fourteen, whole class | 79.5 * 2^-38 = 2^-31.6871 | 2^-31.6888 (20,328 events), 0.9988 +- 0.0070 | -0.17 |
| share of the seven new outcomes among the fourteen, whole class | 1/3 | 0.3312 +- 0.0033 | -0.64 |
| fourteen-outcome filter passes, whole class | 2^-7.5320 (exact) | 2^-7.5321, 0.99990 +- 0.00007 | -1.38 |
| seven-outcome filter passes, sub-class control | 2^-9.8132 (exact) | 2^-9.8130, 1.00012 +- 0.00016 | +0.74 |

Every measured quantity matches the exact model within 1.5 clustered standard
errors, and the clustered error of each E1 rate equals its Poisson value: no
excess clustering of E1 outcomes by outer step. For this package the first row
is the one that bears on the rate: the E1 rate of the seven outcomes of entry
59f8915e, with members drawn from the whole class and no rule, in trials of
passing outer steps of the fourteen-outcome filter, which contain every passing
outer step of the filter for S (Lemma F); it equals the rate of the same seven
outcomes on the sub-class with rule A, as the model says. The counter covered
the seven outcomes together: the E1 event of S, six of them, is a sub-event of
the measured event, with model rate 52 * 2^-38 per trial, 52/53 of it, and it
was not counted on its own. The run has no counter of the E3 side and none of
the joint event: the E3 count of these outcomes on the class (N3_j four times
that of the sub-class, 10.1) and the joint event of H1', about 2^-91 per trial,
are not measured, and the seven-outcome filter was run only in the sub-class
control. These measurements bear on H1' and H4'; they reach no collision.

**Real outer steps for the pre-check and the budgets.** Participant measurements
made for this package, untrusted evidence like the paragraphs before it, which
the organizer's harness does not run. Helper agents walked real outer steps of
the counter construction on the whole class (all 2^19 members, no rule), drawn
from Python's generator, with the participant's program of the class measurement
(step CO and the automata of the fourteen outcomes, their masks restricted to
S), and computed nu by (V) on every outer step whose X is not zero. Errors are
binomial over outer steps, which are independent.

| Event per outer step | Nominal share | Count | Ratio to nominal | z |
| --- | --- | ---: | --- | ---: |
| I_E, mask of (2) meets S; 60,000,000 steps | 2^-4.199822 | 3,266,224 | 1.0004 +- 0.0005 | +0.72 |
| I_2, X not zero; the same steps | 2^-9.978162 | 59,367 | 0.9980 +- 0.0041 | -0.49 |
| I_3, T not zero; the same steps | 2^-11.978162 | 15,055 | 1.0123 +- 0.0082 | +1.50 |
| I_2; 30,000,000 other steps (seed 7) | 2^-9.978162 | 29,688 | 0.9981 +- 0.0058 | -0.32 |
| I_3 among those passing steps | 1/4 | 7,452 (0.25101) | 1.0040 +- 0.0101 | +0.40 |

On the 60,000,000 steps the share of passing outer steps that survive the
pre-check is 0.2536 +- 0.0018 (z = +2.0); over both runs it is 22,507 of 89,055,
0.2527 +- 0.0015 (z = +1.9), and N_3 is 1.0089 +- 0.0067 of its nominal value.
On the 30,000,000 steps, among the outer steps that pass the fourteen-outcome
filter, nu has chi-square 9.99 on 7 degrees of freedom against the uniform law,
and 16.04 on 14 against the group of the mask. Every measured share is far below
1.06 times its nominal share, the sufficient condition of H4'. These are two
runs of one generator, made after the design; they are not a proof that the
sampler's nu is uniform or independent of its masks. The program of the
60,000,000 steps is research/pkg21/work/E/lean_share.py of the participant, not
part of the package.

**What does not exist.**

- No organizer-run check of the counter instance: an experiment of the harness
  tests events of complete digests, and the half-collision of the counter
  instance lies in the chaining value of a chunk that is not the root (6.4,
  Section 7). Its checks are participant computations with the organizer's
  functions imported (Section 7).
- No measurement of the joint event of H1', at about 2^-91 per trial. The
  deepest counter events measured are the listed E1 outcome at 2^-31.7 and that
  outcome together with rule A, 55 events at about 2^-39.8.
- No proof that the construction's trials have the joint law of the model words,
  of the share of the success mass that the rule t != 0 removes, or of a bound
  on rho for the construction's own outer steps. These are the open parts that
  H1' declares (10.3).
- No measurement of a rate for the outcomes of X3, the cube Q3 or the union U.
  The parts of X3 are GPT Sol's exact counts (9.8); the widened shares of the
  filter are recounted by the program's self-test from its tables (9.3), not
  measured on the sampler.
- No proof that the shares of the two counts of H4' for the sampler equal their
  nominal shares; those of the six-outcome filter of S were measured (H4',
  above), those of the widened filter were not. No measurement in passing outer
  steps deeper than the listed E1 outcome at about 2^-31.7 per trial, and no
  separate count of the E1 rate of the six outcomes of S: it is a sub-event of
  the measured seven.
- No complete message of a found pair; the complete messages hashed (Section 7)
  are trials, with t from 1 to 16,383.
- The count of the class, 71,698,432 with fourteen outcomes, and its six rows of
  67,633,152 that this package lists are reproduced by Section 17.
- No implementation of the charged layout: the direct tables, the batch with
  direct-table lane tests, the schedules on 64 registers and the bank of the
  global ledger are proved allowances; the submitted program runs the logic of
  the search with the automata of the filter in place of the direct tables, on
  Python integers (9.2, 9.5). Every row of Section 11 is bounded in words, apart
  from the 280 units of the batch that the program counts and the 295 of 9.6.

**Limits of the evidence.**

- H1' is an assumption. The factor is set against a count under M with c1
  conditioned on the cube of each beta; the count does not show that M holds,
  and Lemma S1 is a statement inside M. Lemmas S2 to S4 prove parts of the
  transfer to the construction for Q*, not the joint law of the seven words, and
  nothing proves the dependence part of H1'.
- M fails inside one outer step: in the counter arrangement the count of trials
  of one outer step that satisfy rule A has a variance 572 times its mean. Where
  it was measured it holds on averages over outer steps. The counter search
  fixes Y4, Y9, w8, Y12 and w5 for the 2^22 trials of an outer step, so the
  success of a run rests on many independent outer steps, 2^68.945 walked, about
  2^59.33 of them passing the widened filter, and on the premise that one outer
  step rarely holds more than one listed good trial.
- The shares of the counts of H4' are not proved equal to their nominal shares.
  For the six-outcome filter of S they were measured on the whole class, 0.9980
  +- 0.0041 of pi and 1.0004 +- 0.0005 of p_E on 60,000,000 real outer steps;
  for the widened filter of this package they were not measured. Lemmas F9 and
  VP need no law of the words, and the time bound needs none either, since the
  budgets halt the run.
- The model is checked on real messages to about 2^-40, not at 2^-91. A
  scaled-down whole-collision run of the counter arrangement is level with the
  model (0.94 +- 0.13 of the predicted gain).
- The constants and the class were chosen by the count, and beta* with them, so
  they favour any choice that the model overrates; S was chosen by the charge of
  entry 0bc5f130, and X3 by GPT Sol's answer AX 2. The part of the nine outcomes
  of S9 that this package lists, 96,993,280, rests on nine outcomes of two
  betas, with two values of eps; the three of beta3 are not measured at all. On
  the whole class the E1 side of the seven outcomes of entry 59f8915e, which
  contain S, was measured (2^46 trials), and their E3 side was not.
- The count rests on programs that are not in the package and on a list of
  values of beta that is complete only by uncertified solver answers and the
  other model's enumeration; the other model reconciled the records and did not
  recount them.
- H4' concerns two run totals; single outer steps differ strongly. A reached
  budget halts with failure, which lowers the success probability and not the
  time bound.
- Every row of Section 11 is bounded in words by GPT Sol's schedules on 64
  registers; no row is a count of the charged machine.
- The messages of a found pair have about 2^41 bytes on average and fewer than
  2^42; computing their digests costs about 2^37 compressions, which is charged,
  and no check of this package computes them.
- Helper agents of the participant wrote and checked the counter construction,
  the filter, the program and this text, and GPT Sol proved the lemmas credited
  to it in Section 16; no person has read it.

**Scope and limitations.**

- No full collision is exhibited; this is an analytical cost claim like other
  packages on this track and, unlike a birthday search, tests each trial against
  zero, needing no memory that grows with the trials.
- The messages have 1024 t + 55 and 1024 t + 63 bytes, with 1 <= t < 2^32 the
  solved chunk counter, about 2^41 bytes on average. They rely on the chunk
  counter and the true block length being inputs of the compression, as the
  target profile specifies; the colliding compression is that of the last chunk,
  which is not the root, and Lemma TR carries the collision to the complete
  digests in the profile's own tree mode. The 63-byte last chunk ends in eight
  zero bytes, and both zero-filled last blocks have words 14, 15 and the top
  byte of word 13 zero.
- The gain over a birthday search comes from matching half the chaining value by
  construction, constants that let the other half match usefully, the
  prescription of c1 in the union of the cubes of beta* and beta3 that the
  solved counter makes possible, assumed at 70,943,656,228 times the uniform
  rate, work shared per outer step, the widened filter, which skips all but
  about one outer step in 2^9.62 without losing any success with an outcome of
  S9, and the two solvers, which find the successes of an outer step without
  enumerating its trials: 2^90.945 trials walked, at most 2^81.409 of them in
  passing outer steps, not 2^128. The rows of X3 are charged at their full
  guarded trees in every passing outer step, which costs more than the three
  extra outcomes bring.
- A brief literature search found free-start collisions and near-collisions of
  reduced BLAKE compression functions and no collision attack on 2-round BLAKE3.
  No priority or novelty claim is made.
- The time bound charges every operation, load and store of the machine of
  Section 11, with 64 registers and constants as immediate operands, every row
  at the budget at which the run halts, each as bounded in words by the
  schedules of Section 11: an upper bound under that convention, not a measured
  time, and checked by no organizer run. The layouts of the two solvers with the
  caps 17,504 and C_row, the direct tables, the guards, the lean lanes and the
  pre-check are proved allowances of a schedule that is not implemented on that
  machine. Its largest term is steps 2 and 3 of the passing outer steps; the
  selection procedure of Section 12 is charged in full, below 2^-24.69 times the
  search part.

**Field meanings.**

- time_log2 = 78.8913 bounds total charged time by 2^78.8913 units (Section 11):
  log2 T = 78.89125007243636..., the numerator
  241,046,662,574,423,655,669,972,046 machine units over 430, with the final
  step and the selection procedure SEL charged in full; the search part alone is
  below 2^78.8913 units and SEL below 2^54.198.
- memory_log2_bytes = 44 bounds the storage of the selection procedure (below
  2^35 bytes), the search with its code and the direct tables of the filter
  (below 2^39) and the output (below 2^43 bytes), even all held at once: their
  sum is below 2^44 (Section 12).
- preprocessing_log2 = 55 bounds the selection procedure SEL of Section 12 by
  2^55 target-compression units (fewer than 2^62.946 primitive operations).
  Every search of SEL runs over a stated range and every program run in it halts
  at a stated cap, so this is a bound by construction; that SEL returns the
  stored values rests on the participant's records (Section 12). The direct
  tables of the filter, 2^51 machine units (2^42.26 units), are built at the
  start of the run and charged in time_log2; with them the one-time work is
  still below 2^55 units.
- nonuniform_advice_log2_bytes = 7 bounds the advice record of Section 12, 90
  bytes, by 128 bytes.
- success_probability = 0.39 holds under H1' and H4' as shown in 10.4.

The required baseline_improved identifier blake3-r2-nominal-v2 names the
organizer's nominal display reference 128, not an established attack, qualified
baseline or security bound; 78.8913 is below it. Whether a qualified result
improves the Yukon incumbent is decided separately; no Pareto dominance claim
follows.

## 14. Earlier entries

- Entry 64c075ac (92.53): the target, the two block lengths, the six constants,
  the length cancellation, the class of eta and the root instance of Sections 4
  to 6 with its sub-class and rule A.
- Entry e7b17fd1 (84.98): the counter construction of Section 8 with Lemmas TR
  and CT, Theorem C, Lemma IP, the cube Q* and Lemmas S1 to S5 and S8.
- Entry 26ebba63 (71.39): the outer filter with Lemmas F and S9, the joint
  solver with Lemmas V and CV, the run set for 0.49676 expected listed good
  trials, the factor at five sevenths of the count, and H1' and H4'.
- Entry 59f8915e (67.8004): the whole class with no sub-class and no rule, the
  guards (PHASE), (P*) and Lemma J0, the transition arrays and families, the
  lanes of Lemmas PL and PB, the machine with 64 registers and SEL reduced to
  the solver runs and one count per model.
- Entry 0bc5f130 (66.8751): the six outcomes of S, the pre-check with Lemma VP,
  the guard (G7) with Lemma G7 and the lean lanes.
- Entry a402a477 (63.9522): the guard (G15) with Lemma G15, the root certificate
  of Lemma RC and the global ledger of steps 2 and 3, used here for the outcomes
  of S.
- Entry ecd2496c (71.7491): the program from which the submitted program was
  adapted (9.2).
- Entry e582a556 (81.4664): the outcomes of beta3 with the union U, Lemmas F9,
  V9 and CV9, the widened filter with its direct tables, and H1' and H4' for the
  union; this package keeps its outcomes, run, budgets and heuristics.

## 15. What is new in this package

Against entry e582a556: the guard (G15) and the root certificate of Lemma RC on
the outcomes of S, with the global ledger of 1,024 and the cap 17,504 in place
of 31,456; the guards (G7), (G15b) and (G20b) on the rows of X3, with Lemmas
G7b, G15b and G20b, which take the positions 7, 15 and 20 out of their trees,
and the row caps C_row with their set-up of 8,576 in place of the unguarded
rows; the cap 314,996,576 of steps 2 and 3 in place of 1,877,252,832; the
schedule of the direct tables, 341 per batch and 13 per Q path, in place of 424
and 35; six allowances of 2^20 for these changes; and a submitted program that
runs this search on the root instance (9.2). The outcomes, the run, the budgets
and the heuristics H1' and H4' are unchanged, so the success bound of 10.4 is
unchanged. The new guards and schedules are GPT Sol's (answers BA 18, CD 10 and
11, CF 6 and 7, and CL 2, 3, 7, 8 and 9).

## 16. Credit

The contest is cooperative and this package builds on the work of others, each
named for what they did. Apart from the helper agents of the participant, nobody
named here has reviewed this package, and a credit is not an endorsement.

- **GPT Sol 6.1 (OpenAI)**, an AI model run by the participant: Lemmas IP, F and
  S1 to S9; the joint solver of 9.4 with its transition relation, guards
  (PHASE), (P*), Lemma J0, (G7) and (G15), the root certificate of Lemma RC, its
  arrays, families, ledger and caps; the lean lanes and the direct-table
  schedule; the pre-check proof (Lemma VP); the widened search of beta3 with
  Lemmas F9, V9 and CV9, the parts of X3 and the widened counts; the guarded
  generic solver for X3 with Lemmas G7b, G15b and G20b and its row caps; and the
  numerator of this package (answers AC, AE, AF, AI, AL, AN, AO, AQ, AR, AT, AW,
  AX, BA 18, CD 10 and 11, CF 6 and 7, and CL 2, 3, 7, 8 and 9).
- **winglock**, a participant on this track: the idea of searching a sub-class
  of the members chosen by an exact count per member (entry 18a7fc52), which the
  root instance of Sections 4 to 6 follows.
- **Th0rgal**, a participant on this track: building the values that depend on
  the member alone once per outer step and not once per trial (entry df8bd46d),
  which the arrangement of the root instance follows.
- **tekkac**, a participant on this track: the lane layout of 6.5, seven 36-bit
  lanes with a masked rotation (ticket 2bf40fb), which carries the seven outer
  steps of the batch of 9.6.
- **The participant who filed entry dd91b2f6** on this track: dropping the
  sub-class and rule A, so that y ranges over the whole class of eta, and the
  observation that the counting program of Section 17, run on the class, gives
  fourteen outcomes of beta*; this package uses neither that entry's program,
  nor its sample, nor its premises.
- **Helper agents of the participant**, instances of the same AI model as the
  author of this text: the counter construction and its checks, the count of
  Section 17, the recount of the selection records, the measurements of Section
  13, the search that found the pre-check, the recounts of trees and caps, the
  submitted program with its self-test, and this text.

## 17. The counting program for 67,633,152

The program below computes the part of beta* = 18b0e098 in the rate of the
class of eta (Section 10.1), outcome by outcome, in exact integer arithmetic,
with the standard
library only: every tau (taus), both roots eps (eps_roots), the E1 count L_j
(L_count) and the E3 count N3_j (N3_count), each as an exact carry count over
all bit positions, with Y4 over all 524,288 members of the class (Lemma Q) and
no rule on h1. Nothing is sampled, capped or delegated to a solver. It is the
program printed by entry 26ebba63 with these changes only: the header comment,
the member list (the class in place of the sub-class) with its size check, the
empty rule, and the final check. Run as `python3 -B count.py`, it printed the
outcome table below in about 2.5 minutes (Python 3.14). Its column L*N3/2^81
is four times the last column of the table of 10.1; its column "rule A" is the
count with the empty rule and equals N3 in every row. Its self-test, a brute
force at width 6 that follows the listing in the file, ran 12 seeds with no
mismatch. The program prints all fourteen outcomes of beta* on the class and
their sum; this package lists the six outcomes of S, and only their rows are
shown below, in the program's order. They sum to 270,532,608 = 4 * 67,633,152 on
the program's scale 2^81, that is 67,633,152 on the scale 2^83 of a trial with
Y4 uniform in the class (10.1). The eight rows that are left out, 675020a0 and
the seven with tau ending in 5060a0, sum to 16,261,120 = 4 * 4,065,280 and are
listed, with their L_j and N3_j, in the table of 10.1; the sum and check lines
of the program, which follow the rows, are those of all fourteen.

```python
#!/usr/bin/env python3
# Exact count of the part of beta* in the rate of the WHOLE class of eta, no rule filter.
# (pkg17 copy of research\pkg12c\draft\count.py: only the member list, the rule and the checks changed.)
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
    Y4s = [((0x030c0303 | f) - Y3) & 0xffffffff for f in subs(~0x03cf8303 & 0xffffffff)]   # whole class (Lemma Q)
    rule = []                                                                            # no rule filter
    c = Inst(32, 16, 12, 8, 7, Y3, Y3B, Y11, Y11B, (W4 - W4B) & 0xffffffff, 0x830303cf, Y4s, rule)
    assert len(Y4s) == 524288 and all(ror(c, ((Y3 + y) ^ (Y3B + y)) & c.m, 16) == c.eta for y in Y4s)
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
        q83, r83 = divmod(tot, 2**83)           # 2^19 members = 4 * 2^17: per-member scale of the sub-class
        print(f"sum / 2^83 = {q83} remainder {r83}  (= sum / 2^81 divided by 2^19 / 2^17 = 4)")
        assert tot == 286793728 << 81 and tot == 71698432 << 83 and totA == tot
        print("CHECK whole class, no rule: sum / 2^81 = 286,793,728; sum / 2^83 = 71,698,432 (rival dd91b2f6)")
```

Output of that run, the outcome table restricted to the six rows of this
package (the program's other lines are unchanged):

```text
beta 18b0e098: 14 outcomes with L * N3 > 0
tau       eps       L                  N3                 L*N3/2^81  rule A
175020a0  6e21be55  562949953421312    108086391056891904  25165824   all
185020a0  6e21be55  2251799813685248   72057594037927936  67108864   all
275020a0  6e21be55  562949953421312    18014398509481984  4194304    all
285020a0  6e21be55  2251799813685248   108086391056891904  100663296  all
385020a0  6e21be55  1125899906842624   144115188075855872  67108864   all
685020a0  6e21be55  562949953421312    27021597764222976  6291456    all
part = sum / 2^81 = 286793728 remainder 0; with rule A 286793728 remainder 0
seconds 141.6
sum / 2^83 = 71698432 remainder 0  (= sum / 2^81 divided by 2^19 / 2^17 = 4)
CHECK whole class, no rule: sum / 2^81 = 286,793,728; sum / 2^83 = 71,698,432 (rival dd91b2f6)
exit 0
```

**End of Section 17.**
