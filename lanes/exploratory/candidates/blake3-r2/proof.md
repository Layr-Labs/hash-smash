# A last-chunk half-collision and a chunk-counter search for 2-round BLAKE3

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
separately reported resource bound.

This exploratory package targets blake3-r2-prefix-v1. It has an exact part and
a heuristic part, and it keeps them apart. The search draws independent outer
steps, filters them exactly, and in an outer step that reaches the solver
follows the one path of a static slot named by four random selector bits, so
that the certified count of the outer step is 0 or 1 with mean exactly its
number of successes divided by 16 (9.8, Lemma SL). The guard (G15) of 9.8
prescribes bit 15 of the solved word from its lower bits, which lets 16 slots
cover every success. The six constants, eta, beta*, the outcomes of the filter
and S are fixed nonuniform advice of 73 bytes, and the success bound holds for
these stated values however they were found (Lemma ADV, Section 12); the
selection procedure SEL that found them is charged in full in the time, at a
cap of 8,882,224,365,081,579,520 operations that holds by construction (Section
12); no premise is declared for it.

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
call E1, next to y. The search holds c1 inside the set Q* of the 2^21 words for
which the first-half b difference of E1 is beta* = 18b0e098, the difference of
the solution with which the constants were found (Section 12).

**Heuristic part.** A collision needs the other four words of the chaining
value to agree as well. The algorithm draws 12,992,078,947,537,682,895,094 =
2^73.460 outer steps at random, seven to a batch, 2^21 trials each. An exact
filter, two carry automata on two words of the outer step, skips every outer
step that cannot hold a collision with an outcome of S (Lemma F); it passes
2^-9.9782 of uniform pairs of words. The second automaton runs in every lane,
and the first only in a lane whose word passes the second, 2^-4.1998 of uniform
words; each is read as one load from its direct table (9.10). In a passing
outer step three bits of E1.b1 that every success shares are a function of the
words of the outer step, and they allow an outcome of S for only two of their
eight values: the pre-check skips the solver in the other passing outer steps,
exactly and without loss (Lemma VP); two more of these bits fix bit 7 of the
solved word before the solver starts (Lemma G7), and five bits of the cube of
c1 fix its bit 15 from its bits 0 to 14 (Lemma G15). The solver walks the bits
of the solved word under guards that exact counts of the class prove lossless
(9.4, 9.9). With (G15) every success of an outer step lies at one of at most 16
leaf positions, and the search gives each a static slot from 0 to 15; four
selector bits of the outer step's random word name one slot, the solver follows
that one path, and a sparse certificate tests its leaf (Lemma SC). Every
success of the outer step owns exactly one slot, so the outer step certifies a
success with probability exactly its number of successes divided by 16, at a
cost of at most 9,461 machine units for a passing outer step whatever its words
(Sections 9 and 11, Lemmas V, SC, VP, G7, G15, CV and SL). Every budget is a
halt and is charged at its bound; no mean of any count enters the time bound.
One heuristic carries the success bound: H1', that the valid trials (t not
zero) complete the collision with an outcome of S at a mean rate of at least
98,937,639,497 * 2^-128 = 2^-91.474, five sevenths of the model's rate for this
prescription and these outcomes rounded down, with no clause on how successes
cluster (10.3). The three budgets of the run, of lanes whose word passes the
second automaton, of passing outer steps and of outer steps that reach the
solver, are one proved figure L, 855/2048 of the run plus ceil(sqrt(5 *
RUN_STEPS)): at every fixing of the other coordinates of a chart of the outer
words, at most 1,710 of the 4,096 values of twelve fresh bits let a lane pass
the second automaton, so a budget halts the run with probability below 0.0005
(Lemma BUD). There is no budget premise, and each of the three rows is charged
at L + 1. Under H1' the search succeeds with probability at least 0.39, for the
stated advice (Lemma ADV, Section 12). The search, with the building of the
direct tables and the final step, is charged below 2^76.67710
target-compression units. The selection procedure SEL that found the advice is
charged in full, below 2^54.198 units, at a cap that holds by construction
(Section 12). The total, 2^76.67709988..., is below 2^76.6771: the claimed
scalar is 76.6771. The search needs less than 2^39 bytes of memory,
2^38 of them for the direct tables; its two messages are shorter than 2^42
bytes each, and the declared 2^44 bytes cover them, the code, the advice, the
search and every run of SEL, even all held at once (Section 12).

The rate in H1' is an assumption. Under the seven-word model of Section 13, with
Y4 uniform in the class, prescribing c1 in Q* multiplies by 2^11 the part of
beta* in the rate of the class: counting the six outcomes of S, the rate is
2^11 * 67,633,152 = 138,512,695,296 times 2^-128, which is 853.61 times the
model rate of a trial of the class, and the conditioning leaves the law of the
other call, E3, unchanged (Lemma S1). The figure 67,633,152 is the sum of six
exact outcome counts of the counting program printed with its output in
Section 16. Whether the trials of the construction realise that conditional law,
to at least 5/7 of its rate, is the part that is not proved, and it is declared
as H1' for the whole class and S; Lemmas S2 to S4 prove parts of it. How the successes
of one outer step depend on each other does not enter: the slot selection makes
the certified count of an outer step 0 or 1 with an exact mean (Lemma SL).
Participant measurements on real counter trials reach events of probability
about 2^-31.7 and agree with the model, and a scaled-down end-to-end run with
real collisions of complete messages realises the predicted gain of the
prescription at 0.94 +- 0.13 of its value (Section 13). No run reaches a
collision at 32 bits.

No full 2-round collision is exhibited, and the search is far beyond feasible
computation. The two declared experiments run the root instance of the same
construction: single chunks of 55 and 63 bytes, compressed with counter 0 and
flags 11 (Sections 4 to 6). An organizer experiment tests an event on the two
complete digests, and the half-collision of the counter instance lies in the
chaining value of a chunk that is not the root, which no digest experiment can
show (6.4). What the experiments exhibit, and what the organizer's runner
checks, is the exact half-collision of the root instance, on a pair built by the
steps CO and CT of this search, and a short search of 8 more digest bits over
the class. The program the organizer runs runs the search of 9.1 on the root
instance for 1,792 outer steps per organizer seed, with the 16-slot selection,
(G15) and the one-path solver, and counts every row by its ledger (425
per batch and 35 per Q path, the other rows as charged); its counts and its
self-test are its own, which the organizer does not check, and on the root
instance a root is a collision only when its forced counter word is 0 (Section
13). The direct tables and the schedule on 64 registers are proved allowances
that the program does not run.

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
are written to. Arithmetic is modulo 2^32.

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
(Lemma N).

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
satisfies rule A with probability 2^-8.

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
Lemmas L and H, the class, Lemma N and the machine of 6.5; the sub-class, rule
A and Lemma A belong to the root instance, not to the counter search of this
package. The instances differ in the counter and the flags that the compression
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

- `half-collision` runs, per organizer seed, the search of 9.1 on the root
  instance for 256 batches (1,792 outer steps), with the slot selection
  and the one-path solver of 9.8, and returns the pair that steps CO and CT
  give on the trial's first passing outer step with the one c1 of Lemma IP for
  which the forced counter word is 0. Every such pair agrees on digest words 0,
  2, 5 and 7 (Section 13, *The submitted program*).
- `residual-search` runs the same trial, then takes the members of the class
  of Lemma Q in order from the member of that outer step, at most 131,072 of
  them, each with its own pair at counter word 0, and stops at the first pair
  whose residual (3.3) has a zero low byte in digest word 1.

Neither experiment runs the counter instance, and neither measures a rate of
the counter search. A search of the root instance is not part of the claim:
the trials of the experiments are short, and on this instance a root of step 2
is a collision only when its forced counter word is 0 (Section 13).

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
  compared with the memory word `stage-2 budget`; in the root instance its value
  has no influence on any output.
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
lane. No sum of the build leaves its lane: with B = 2^32, table words, list
words, stored words, rotation outputs and constants are below B, an XOR with a
value below B keeps a bound that is a multiple of B, and Y12 and C0.a1 are
below 2B, XA below 3B before it is reduced, D1.c1 below 3B, D1.d1 below 4B and
X1 below 4B before it is reduced, all below 2^36; so the low 32 bits of every
lane are the scalar value; the words stored after a sum are reduced by an AND
with M, and R and X6 are rotation outputs. XA is C0.a1 plus the stored -X4. (b)
Y12, C0.a1, X6, X1 and D1.d1 are table lines and X4 is an outer line, so by
Lemma T2 (c) none depends on X2. (c) The six equations are the lines for X0,
C2.a1, C2.b1, C1.a1, D1.a1 and E1.d1 of Section 4 with the words of (a) in
place of the names: XA[j] - w2 = C0.a1 - X4 - w2, R[j] XOR S12 = ROL(D1.d1,16)
XOR S12, and the other four contain X6, X1 and Y12 as they stand. QED.

*The machine.* The pieces run on a load/store machine with 16 registers. One
operation is charged for every addition, XOR, AND, OR and shift of 256-bit
words, for every comparison and for every branch, so PROR = 5. One load is
charged every time a word is fetched from memory, from a list or from the table
into a register, and one store every time a register is written to memory or to
the table. Shift distances are fixed in the instruction, and a register may
hold a memory word across several operations.

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
that the participant's implementation of the construction computes, in 2,000 of
2,000; words 0, 2, 5 and 7 of the two chaining values were equal in all 2,000
and all eight words in none; and 204,000 internal words of the construction
were equal to a separately written forward computation of the compression. (2)
For five counter trials with t = 1, 3, 3, 4 and 16,383, the complete messages F
|| A and F || B, with F a string of t chunks of pseudorandom bytes, were hashed
by `blake3(m, 2)`. In each, the messages have 1024 t + 55 and 1024 t + 63
bytes; the code makes exactly one compression with block length 55 or 63, and
its inputs are (IV, the block words, t, 55 or 63, 3); its chaining values agree
on words 0, 2, 5 and 7 and not on all eight; the two digests differ; and when
the output of that compression of F || B is replaced by the output of the one
of F || A, blake3 returns the digest of F || A, and the other way round. (3)
Separately, a helper agent checked (b) in the same way for 25 values of t from
1 to 1,025, on 150 messages and 75 pairs with a replaced output, all as the
lemma says.

## 8. The counter construction

*Words and constants.* The construction has nine free words: the seven *outer
words* C0.d1, D2.a1, D2.b1, S11, S4, X9 and w6 (the submitted program's
`OUTER_WORDS`); a member y of the class of 6.1 (Lemma Q), which becomes the
value of Y4; and the *inner word* c1, which becomes the third value of E1 on
message A. The constants are those of Section 4: X3, X7, X11 and X15, w4 = W4,
w13 = W13, w14 = w15 = 0, the four constant first values K2.a1, K2.d1, K2.c1
and K2.b1 of K2 given in step O, and Y3, Y11 of Fact P. The compression reads
three more values besides the message and the IV. K3 reads the flags, here 3
(the line for K3.d1); K1 reads v[13], here 0 (the line for K1.a1); and K0 reads
the counter v[12], which is not fixed in advance: the line for t solves K0's
second assignment for it. The names are those of Section 4.

*The cube Q*.* Q* is the set of the 2^21 words c with (c AND 0e09818b) =
02008000; the submitted program names them `QSTAR_MASK` and `QSTAR_VALUE`.
Member number j of Q*, for 0 <= j < 2^21, is the word whose bits at the 21
positions where 0e09818b has a zero are the bits of j, in increasing order of
position.

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
for K3.d1 used. Otherwise the words w0 to w12 of the lines, with w4 = W4 and
w13 = W13, and w14 = w15 = 0 form the block of A; A is the first 55 bytes of
its little-endian encoding, and B the first 63 bytes of that of the same words
with w4' = W4' and w5' = w5 + fffffff8 in place of w4 and w5, as in steps S2
and S3 of Section 4. F is the string of 1024 t zero bytes, and the two messages
are F || A, of 1024 t + 55 bytes, and F || B, of 1024 t + 63 bytes.

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

**Lemma IP (the inner permutations and the member with t = 0).**
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
in 40 outer steps and rejected by the participant's implementation in 40 of 40;
over 8,192 further outer steps it lay in Q* 4 times, against 4.0 expected, and
was rejected 4 times out of 4.

*The length of the messages.* Within one outer step the 2^21 members of Q* give
2^21 different values of t below 2^32 (Lemma IP); over 2,000 trials of the
participant's check t ran from 891,836 to 4,291,586,422 with a mean of log2 t
of 30.56. A pair found by the search has messages of 1024 t + 55 and 1024 t +
63 bytes, shorter than 2^42 bytes and about 2^41 on average. A small t cannot
be chosen: it is the value of a permutation of c1 at the member that the search
finds.

**The outer filter.** Number the seven outcomes of beta* whose tau ends in
5020a0 (10.1) j = 1 to 7 in the order of the table of 10.1: 175020a0, 185020a0,
275020a0, 285020a0, 385020a0, 675020a0 and 685020a0, the seven of the submitted
program's `TAUS`. This search lists six of them, the set S = {1, 2, 3, 4, 5,
7}: all but 675020a0 (j = 6). In the hexadecimal masks below, with bit j - 1
for outcome j, S is 5f. Beta* has seven more outcomes on the class, the same
seven with bit 14 of tau set (j = 8 to 14 of 10.1); this search does not list
them either. Let tau_j be the tau of outcome j, sigma_j = tau_j XOR ROR(tau_j,
1) and theta_j = ROL(sigma_j, 12); all seven have eps = 6e21be55. For an outer
step put omega = Y3 + y + w8, with Y3 of Fact P, y the member of the outer step
and w8 the name of step CO; DY3 = Y3' - Y3 = fdb77cfd is that of Section 6. For
a word x:

- condition (1)_j holds for x when some word h gives
  (x + h) XOR (x + (h XOR eta)) = theta_j;
- condition (2)_j holds for x when some word f gives
  (x + f) XOR ((x + DY3) + (f XOR sigma_j)) = eps.

An outer step *passes* the filter when for some j in S both (1)_j holds for its Y9
and (2)_j holds for its omega. Y9 and w8 are names of step CO and y is drawn with
the outer words, so whether an outer step passes depends on the outer step alone
and on no c1.

**Lemma F (the outer filter).** Fix an outer
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
!= 0, and it holds for any list of outcomes, S among them.
The filter can pass outer steps that hold no success, since (1)_j and (2)_j are
solved with separate witnesses; it cannot reject an outer step that holds a
success with an outcome of S.

**The exact share.** Let pi be the share of the 2^64 pairs (x1, x2) of words such
that for some j in S condition (1)_j holds for x1 and (2)_j for x2. Then

    pi = 18,289,159,183,466,496 / 2^64 = 279,070,422,111 / 2^48,

about 0.00099145731 = 2^-9.978162. With all seven outcomes j = 1 to 7 in place
of S the share is 20,504,986,129,465,344 / 2^64 = 312,881,258,079 / 2^48 =
2^-9.813176; this search does not use it. Let pi_E be the share of the 2^32
words x for which (2)_j holds for some j in S: pi_E = 233,715,456 / 2^32, about
0.054416120 = 2^-4.199822.

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
arithmetic on the table).

*The automata.* The submitted program's `automaton` builds the subset
construction above as four byte tables: a state is the carry of x + DY3 (zero
for (1)) and, per outcome, the set of reachable carry pairs, four bits; the
table of byte p maps a state and byte p of x to the next state, and the table
of the last byte maps to the mask. `build_tables` builds the two automata once
per run for the seven outcomes of `TAUS` and ANDs every entry of their last
tables with 5f, so that every mask it reads is restricted to S; the states and
the number of table loads do not change. The search of this package builds the
same two automata (step 0 of 9.1). The construction has 1, 18, 43, 37 and 1, 3,
7, 7 states at the four byte boundaries and tables of 25,344 and 4,608 entries
(a participant run of the program's own functions). `look` runs an automaton on
a word with one table load per byte; an outer step passes when the AND of the
mask of Y9 under (1) and the mask of omega under (2) is not zero. The program's
self-test recounts SHARE and E_COUNT from its own tables and checks the
automata against brute force (Section 13, *The self-test*).

## 9. The counter search

**9.1 The algorithm.** The algorithm is stated with fixed values, its
nonuniform advice of Section 12 (73 bytes): the six constants of 3.2, eta =
830303cf, beta* = 18b0e098 with the mask 0e09818b and the value 02008000 of its
cube, the seven values of tau with eps = 6e21be55 from which the automata of
the filter are built, and the mask 5f of S. They are written into the
algorithm, which runs no selection; Lemma ADV (Section 12) lists what the
analysis uses of them, each property checked in this text for the stated
values. The search uses these numbers, derived from the advice by exact counts
and formulas (Section 12): FACTOR = floor(5 *
138,512,695,296 / 7) = 98,937,639,497, the factor of H1', five sevenths of the
count of the six outcomes of S in 10.1 rounded down (10.3); RUN_STEPS =
ceil(lambda * 16 * 2^128 / (FACTOR * (2^21 - 1))) =
12,992,078,947,537,682,895,094, about 2^73.460, with lambda = 0.49512 = 12378 /
25000, so that the expected number of outer steps of a run that certify a trial
is at least lambda at the rate of H1' (Lemma SL, 10.4);
SHARE = 18,289,159,183,466,496,
the number of pairs that pass the filter for S (Section 8), so that its share pi
is SHARE / 2^64; E_COUNT = 233,715,456, the number of words that pass the
automaton of (2) for S (Section 8); V_COUNT = 558,140,844,222 = 2 * SHARE /
2^16, the count of the pre-check of 9.7 over 2^51; the margin s =
ceil(sqrt(5 * RUN_STEPS)) = 254,873,291,535; and three budgets, all equal to
the proved figure L of Lemma BUD (10.3):

    E_BUDGET = PASS_BUDGET = SOLVER_BUDGET = L
             = ceil(855 * RUN_STEPS / 2048) + s
             = 5,423,939,209,309,911,804,868,  about 2^72.200;

and RUN_BATCHES = ceil(RUN_STEPS / 7) = 1,856,011,278,219,668,985,014, about
2^70.653, the number of batches of seven outer steps (9.6); RUN_STEPS = 7
(RUN_BATCHES - 1) + 3. L uses none of SHARE, E_COUNT and V_COUNT, which only
the ledger figures of Sections 11 and 13 and the program's self-test use. The
submitted program (Section 13) holds FACTOR, SHARE, E_COUNT and V_COUNT as
above and a shorter run length, RUN_STEPS = 814,694,561,164,316,144,946 (lambda
= 12419 / 25000, without the slot factor), with RUN_BATCHES computed from it
and three budgets computed from it as ceil(17 * RUN_STEPS * E_COUNT / 2^36),
ceil(17 * RUN_STEPS * SHARE / 2^68) and ceil(17 * RUN_STEPS * V_COUNT / 2^55),
not by the formula of L; its self-test checks those values. A trial of the
program walks 1,792 outer steps and reaches none of its budgets, so these
constants do not change what it returns.

0. Before the batches, build the two automata of the outer filter for the seven
   outcomes, with the entries of their last tables ANDed with S (Section 8), and
   from them the direct tables TAB2 and TAB1 of 9.10, the
   table VMASK of the pre-check (9.7), and the three transition arrays, the
   static row descriptors of the six outcomes of S, the static slot ranges of
   9.8 and the statically written one-path code of the solver (9.4, 9.8,
   Section 11). None depends on an outer word.
1. For each of the RUN_BATCHES batches in turn, b = 0, 1, ..: draw eight fresh
   uniform 256-bit words R_0 to R_7. Lane i, for i = 0 to 6, is bits 36 i to 36
   i + 35 of a word (9.6). Lane i of batch b holds the outer step of number 7
   b + i if that number is below RUN_STEPS, which holds for all seven lanes
   except in the last batch, whose lanes 3 to 6 are not used. The *random word*
   of that outer step is the 256-bit word whose k-th 32-bit word, for k = 0 to
   7, is the low 32 bits of lane i of R_k. Its first seven 32-bit words are the
   outer words C0.d1, D2.a1, D2.b1, S11, S4, X9 and w6. Its eighth word W gives
   the member y with e1 = Y3 + y = 030c0303 + (W AND fc307cfc), that is the
   member of the class whose 19 free bits of e1 (Lemma Q) are the bits of W at
   the same positions; its member number (Section 8) is these 19 bits in
   increasing order of position. W also gives the *selector* J = W[0] + 2 W[1] +
   4 W[8] + 8 W[9], a number from 0 to 15, from four of the 13 bits
   of W outside fc307cfc (9.8); the raw word R_7 is kept before its AND with
   fc307cfc for this. *Test (2):* run in all lanes at once on packed
   words (9.6) the lines of step CO that reach Y9 or omega, omega = Y3 + y + w8,
   and read in each lane the mask of (2) on omega, restricted to S, as the
   entry TAB2[omega] of its direct table (9.10). A lane
   whose mask of (2) is zero ends its outer step there. *Q path:* then for each
   lane whose mask of (2) is not zero, in increasing order of i: advance the
   count of such lanes, the *E count*, and halt with failure when it exceeds
   E_BUDGET; else read the mask of (1) on the Y9 of the lane, restricted to S,
   as the entry TAB1[Y9] (9.10), and AND it with that of (2), giving the mask X
   of the outer step. If X is zero the
   outer step ends there. Otherwise the outer step *passes* (Section 8): advance
   the count of passing outer steps and halt with failure when it exceeds
   PASS_BUDGET; else compute on scalar words, from the eight words of the lane,
   the names of step CO that steps 2 and 3 read. *Pre-check:* compute the word
   nu of 9.7 from Y9, y, C2.c1 and C2.b1 and T = X AND VMASK[nu]. If T is zero
   the outer step ends there (it holds no listed good trial, Lemma VP).
   Otherwise advance the count of outer steps that reach the solver, the *solver
   count*, halt with failure when it exceeds SOLVER_BUDGET, and else run steps 2
   and 3 for this outer step.
2. *Slot:* run the one-path solver of 9.8 on Y9, y, omega, T and the selector
   J. It chooses the envelope of rows from the mask of (1) on Y9, reads the row
   and the free-bit values of slot J, ends the outer step if the slot is padding
   or its row is not in T, and otherwise follows the one path of that slot from
   the common state of 9.4 to its leaf, with bit 15 prescribed by the guard
   (G15). It returns at most one root h, with the outcome j of its row (9.8).
3. *Certificate:* for the returned root h, if there is one, with its outcome j:
   compute c1 from h by the inverse of Lemma IP, Y14 = ROL(h,16) XOR (Y3 + y),
   Y6 = ROR((Y14 + C2.c1) XOR C2.b1, 7), E1.a1 = Y6 + Y1 + w12 and c1 = Y11 +
   ROR(E1.a1 XOR Y12, 16); drop the root if c1 is not in Q*, that is if c1 AND
   0e09818b is not 02008000, the test (Q) of Lemma SC (10.2); then drop it
   unless the tests (A), (C) and (T) of Lemma SC hold. By Lemma SC the four
   tests hold exactly when c1 is in Q*, the counter word t of step CT is not
   zero and E1 on A and on B (6.2) gives the XOR differences tau_j and eps =
   6e21be55 of its a and c outputs (their first-half b difference is beta*, by
   Theorem C (iv)). A root that is not dropped is *certified*. For a certified root, form F || A and F || B by
   steps CT and CS for its c1, evaluate blake3 of both in full, check that the
   two digests agree, output the pair and halt. A dropped root, or no root,
   ends the outer step; the slot is not drawn again.
4. After the last batch, halt with failure.

The run halts with failure in exactly four ways, each a test on a count that the
algorithm keeps: the E count exceeds E_BUDGET, the count of passing outer steps
exceeds PASS_BUDGET, the solver count exceeds SOLVER_BUDGET, or the outer steps
are exhausted. So at most E_BUDGET lanes read TAB1, at most
PASS_BUDGET passing outer steps are rebuilt and pre-checked, and at most
SOLVER_BUDGET outer steps run steps 2 and 3, which have no budget of their own:
the solver follows one path and returns at most one root, and the work of steps
2 and 3 is bounded in every outer step that reaches them, whatever its words
(9.8, Section 11). So the work of every run is bounded by the counts of Section
11, and a pair of messages is formed and hashed at most once, for a certified
root.

A trial is *valid* when its t is not zero; a valid trial with R = 0 is *good*; a
good trial is *listed* when its E1 outcome is in S (Section 8, 10.1). Each
listed good trial of an outer step owns one slot from 0 to 15, and distinct
listed good trials of an outer step own distinct slots (Lemma SL, 10.2). A
listed good trial is found when its outer step is reached and the selector J of
that outer step is its slot: its outer step passes the filter by Lemma F, the
pre-check keeps its outcome by Lemma VP, the solver follows the path of the slot
to its E3.h1, and step 3 certifies it (Lemmas CV and SL, 10.2). Every certified
root is the E3.h1 of a listed good trial (Lemma CV). The run ends before an
outer step only by one of the three budgets or by the output of another pair. A
good trial that is not listed is not found, and Section 10 does not count it; by
the count of 10.1 beta* has eight more outcomes on the class, 675020a0 and the
seven with bit 14 of tau set, which carry 4,065,280 of its 71,698,432 (5.7 per
cent) and are not listed. When the run outputs a pair, the pair is a collision
of two complete messages: the certified trial has R = 0 (Lemma V, 10.2), step 3
has checked both digests, and Lemma TR (c) says that R = 0 with the
half-collision of Theorem C gives equal digests.

*What the submitted program holds.* The submitted program (Section 13) runs
this search on the root instance: the member of the class from the 19 free
bits of the eighth word and the selector J from its bits 0, 1, 8 and 9;
step CO compiled from its lines onto packed words of seven 36-bit lanes; the
two automata with their last tables restricted to S, (2) in every lane and (1)
on the Q path, in place of the direct tables of 9.10, which it does not build
and which give the same masks (Lemma TAB); the E, pass and solver counts against
the budgets it holds
(above); the pre-check of 9.7; the slot selection and the one path of 9.8 on
the static rows of 9.4, with the guards (a) to (g), (G7), (G15), Lemma J0 and
the guards at positions 25 and 29; and step 3 for every root, evaluated on the
compressions of A and B. Its steps CO and CT
read counter 0 and flags 11, so its trials are trials of the root instance,
where a root of step 2 is certified only when the counter word that step CT
forces is 0 (Section 13). It counts each row with the units of the program's
ledger of Section 11 (425 per batch and 35 per Q path, the other rows as
charged) on Python integers; it does not run the 64-register schedule of
Section 11, so its counts are not counts of that machine (9.5).

**9.4 The joint solver.** Fix a passing outer step and write Q = Y9, y for its
member, E = omega = Y3 + y + w8 and E' = E + DY3; x[i] is bit i of a word x,
bit 0 the lowest, and maj is the majority of three bits. Put e1 = Y3 + y and b
= e1[2], u = e1[21] and v = e1[26], three bits that are free in the class (in
the sub-class of 6.1, u = v = 0). For an outcome j of beta* (10.1) put sigma =
sigma_j and theta = theta_j (Section 8), eps = 6e21be55, gamma = eta XOR theta,
D = (sigma XOR eps) AND 7fffffff, kappa = sigma XOR eps XOR E XOR E' and mu =
ROR(eta XOR eps, 8) = 9aed22bd. For a word h put g = Q + h, f = ROR(y XOR g,
12), e2 = E + f and h2 = ROR(h XOR e2, 8): for E3.h1 = h these are E3.g1, E3.f1
and E3.e2 of step CT and the d output of E3 on message A (6.2). The *static
descriptor* of outcome j holds sigma, theta, gamma, D and the positions of its
constants and guards; the static descriptors of the six outcomes of S depend on
no outer word and are formed once per run.

This subsection defines the joint roots, the guards, the transition arrays and
the static trees of the solver, and the complete depth-first traversal over
them, which returns every joint root of the searched outcomes. The search of
this package does not run the complete traversal: it runs the one-path form of
9.8, which follows the single path of one slot through the same trees, with the
same arrays and guards.

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

*The phase equations.* The participant's
counter, run on the class with its E3 count split by the pattern of h on the
sixteen bits 0 to 3, 6 to 13, 16, 17, 24 and 25 and by (b, u, v), records for
each of the eight values of (b, u, v) every pattern that occurs in a solution
of E3 with an outcome of beta* (records of the participant, not in the
package). Every recorded pattern was checked against

    h[0] = 0,  h[1] = 1,  h[2] = 1 XOR b,  h[10] = b,  h[16] = h[17] = 0,
    h[11] = 1 XOR h[3],  h[24] = h[3] XOR h[12] XOR u                   (PHASE)

with no violation in any of the eight cells, whose sets have 88, 88, 108,
132, 108, 132, 88 and 88 patterns in the order b + 2u + 4v. Each of the fourteen
outcomes of beta* on the class has an E1 count L_j > 0 that depends neither on y
nor on h, so a zero count outside (PHASE) means that no joint root of any of
them, the six of S among them, violates (PHASE). The equations are
consequences of the count, which the solver uses as guards; they are not a rule
that drops members or solutions. (PHASE) is also certified pointwise, for every
joint root of the fourteen outcomes in all eight phases, by the exact verifier
of 9.9, which the participant ran: its count of joint roots that violate
(PHASE) or (P*) is zero in every phase and on every row.

*The parity certificate.* Call the outcomes j = 1 to 7,
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
w8. Every N3_j is split by the phase (b, u, v) of Y4 and by the parity pi
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
function N3_count of the counting program of Section 16 and the parity as one
more condition, gives all fourteen counts with pi = 0 on the old rows, pi = 1
on the new rows and the count 0 with the other pi, as the table says. The cells
of all eight phases, for all fourteen rows, were recomputed by the exact
verifier of 9.9, which the participant ran: it asserts a
zero count of wrong guards and the counts of this table in every phase, and it
printed "all eight phases: exact guards and counts certified". The count shows as well that a new row has no joint root when u =
v, and a new row 175, 275 or 675 none when b = 0; the search of this package
lists no new row.

*The guard on the third addition.*

**Lemma J0.** Every joint root h of every one of the seven outcomes has
h2[0] = 0, that is h[8] = e2[8].

Proof. For all seven outcomes tau_j[0] = tau_j[1] = 0, theta_j[0] =
theta_j[1] = 1 and gamma[1] = gamma[2] = 0, and mu[0] = 1, mu[1] = 0. By
(PHASE), certified for every joint root in all eight phases (9.9), h[0] = 0
and h[1] = 1. In (J1) both carries into bit 0 are 0. Since
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
and the outcome before it branches, or checks during the traversal. Every member of the
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
 , where e2[1] = E[1] XOR f[1] XOR a[1] and f[1] = y[13] XOR
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
(every row). (P*) is not a rule but a consequence
of the count of the class, true of every joint root.

*One traversal.* Every carry guess a[20] that (a) keeps reaches, after the
constants h[0] to h[6], the same state: the same bits h[0] to h[6], the same
carries u[7] and a[27], and the same e2[26]; the values e2[20] and e2[21],
which depend on the guess, are not used by any guard. So the solver walks bits
0 to 6 under both kept guesses with the tests of (a), (b) and (e), then drops
the guesses and starts one depth-first traversal for each searched outcome at
depth 7 from that state, and checks (J1), (J2) and (J3) as words at each leaf,
which enforces the closure of the carries that the guess stood for. Every joint root survives a guess and reaches
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
position has a constant and its value, and whether i = 31 and k = 31. The solver reads the arcs from three arrays built once per run, each entry computed by the relation above, which is the same
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
J0), and n_32 = 2^|F| leaves:

| tau | free positions | forced nodes | free nodes | selected nodes | leaves |
| --- | --- | ---: | ---: | ---: | ---: |
| 175020a0 | 13, 15, 30 | 72 | 7 | 4 | 8 |
| 185020a0 | 13, 15, 30 | 72 | 7 | 4 | 8 |
| 275020a0 | 9, 13, 15, 30 | 140 | 15 | 8 | 16 |
| 285020a0 | 9, 13, 15, 30 | 140 | 15 | 8 | 16 |
| 385020a0 | 9, 13, 15, 30 | 140 | 15 | 8 | 16 |
| 675020a0 | 13, 15, 30 | 72 | 7 | 4 | 8 |
| 685020a0 | 13, 15, 30 | 72 | 7 | 4 | 8 |

Against the solver with the phase guards alone,
position 20 is no longer free on any row (Lemma J0), and (P*) fixes position 25
on the low rows and position 6 on the high rows; no position becomes free. These
are counts of the static trees: an arc that fails a carry test or a guard only
removes nodes, and the trees that occur may be smaller. The guard (G7) of 9.7
fixes position 7 on every row before the traversal, so
position 7 is free on no row: the table gives the trees of the solver with (G7),
in which the rows 175020a0, 285020a0 and 685020a0 have lost the free position 7
that they have without it (there 142, 278 and 142 forced nodes and 16, 32 and 16
leaves). The row 675020a0 is not in S, and this search does not build its tree.

The outcomes searched in an outer step that reaches the solver have their bits
set in T, a subset of the mask of Y9 under (1) and of S. By the certificate of
Section 8 every nonzero mask under (1) is one of the twelve nonzero seven-bit
masks of its table, and each of these is a subset of {275020a0}, {175020a0,
675020a0}, {285020a0, 385020a0} or {185020a0, 385020a0, 685020a0}. So the
searched outcomes are among the rows of one of these four sets restricted to S:
{275020a0}, {175020a0}, {285020a0, 385020a0} and {185020a0, 385020a0, 685020a0}.
With (G7) these have 1, 1, 2 and 3 rows; (140, 15, 8), (72, 7, 4), (280, 30, 16)
and (284, 29, 16) forced, free and selected nodes; and 16, 8, 32 and 32 leaves.
A leaf gives at most one root. So an outer step has at most 3 searched outcomes,
32 leaves and 32 roots, whatever its words.

*Families.* Within one of the four sets the rows fall into *families* by two
marks: low row (175, 275, 675) or high row (185, 285, 385, 685), and the bit
gamma[10] (on the class the new rows, which this search does not list, would
form families of their own). gamma[3] is 0 on the low rows and 1 on the high
rows, gamma[10] is 1 on the rows 675 and 685 and 0 on the others, and sigma[20]
to sigma[26] and sigma[0] to sigma[3] are the same on all low rows and on all
high rows; gamma[10] fixes the reset of u[11] in (c). So the formulas of (a) to
(e) and the walks of bits 0 to 5 under both guesses are the same for the rows of
a family and are evaluated once per family. Restricted
to S the four sets have 1, 1, 1 and 2 families, and at most two rows of a set
share a family. gamma[7] can differ within a family, so bit 6 and its outgoing
carries, h[6], h[7] and h[26] are computed for each row: no prefix of seven bits
is shared.

*Checks.* The participant recomputed the free positions, the node, leaf and
selected counts of the table and of the four sets (for the fourteen rows, for
the seven and for S, with and without (G7)), the families, the bits of the
fourteen outcomes that Lemma J0 reads, and the sums of the parity certificate
against the counts of 10.1, and ran the verifier of 9.9, which certifies
(PHASE) and (P*) for every joint root of the fourteen outcomes in all eight
phases; the other constants and guards of this subsection were not re-derived
independently by the participant. At positions 25 and 29 the guard selects the
candidate before the table read: these positions are not prescribed by the
carries (gamma[i] = 0 and D[k] = 0 there, on the old rows for position 25 and
on every row for position 29), so the value of the guard is written into the
key before the read, within the same allowance (Section 11). Lemma CV (10.2)
states what the complete traversal returns, and Lemma SL (10.2) what the
one-path form of 9.8 certifies. The layout is specified and charged by this
text; it is not an implementation (9.5).

**9.5 Checks of the joint solver.** The solver of 9.4 and 9.8 for the class,
in the layout of 9.4 and 9.8 and with the schedule of Section 11 on 64
registers, has not been implemented, and neither have the slot selection of
9.8, the lean lanes of 9.6, the direct tables of 9.10 or the pre-check and the
guard (G7) of 9.7 in that schedule. The submitted program runs their logic on
the root instance, the automata in place of the direct tables, with counts
taken from the program's ledger of Section 11, and its measured counts are
reported in Section 13 (*The submitted program*); it is a participant
implementation in Python, not the schedule, and its runs are short: the
completeness of the solver's paths rests on the proofs cited in 9.4, on the
count of the class and on the guard certificate of 9.9, which was run, and its
cap of 8,936 machine units on the schedule of 9.8 and Section 11, an upper
allowance written out by blocks and not a count of an executed program; the
pre-check rests on Lemma VP, whose bit identity was checked on real trials
(9.7).

**9.6 Seven outer steps in one word.** The batch of step 1 of 9.1 runs on
packed 256-bit words with the seven 36-bit lanes of 6.5: lane i is bits 36 i to
36 i + 35 of a word, and it holds a 32-bit value in its low 32 bits with four
guard bits above them. The conventions are those of 6.5. The low 32 bits of a
lane are the scalar value modulo 2^32, and every lane of every sum stays below
2^36, so that no carry leaves its lane; where an interval bound of a sum could
reach 2^36, an AND with the word M that has the low 32 bits of every lane set
is made first, and charged. x - z is formed as x + (z XOR M) + 1, never by a
packed subtraction, whose borrows could cross lanes. A rotation by r is PROR:
((x >> r) AND A_r) OR ((x << (32 - r)) AND B_r), five operations, with A_r and
B_r the masks of its two parts in every lane. The addition of a constant is
kept pending until the value is read by an XOR, an OR, a shift, a rotation or a
table index, and the one addition that then forms it is charged. All interval
bounds depend on the lines and the constants only, not on the words.

*What a batch computes.* Each of R_0 to R_7 is drawn and ANDed with M, except
R_7, which is first copied to one more register as drawn (the raw word, from
which a passing lane takes its selector J, 9.8) and then ANDed with the word
that has the bits of fc307cfc set in every lane; lane i of R_k is then the k-th
word of the random word of lane i. The lines of step CO run on the packed
words, with y = (W AND fc307cfc) + (030c0303 - Y3), a pending constant
addition, and without the lines whose values reach neither Y9 nor omega = Y3 +
y + w8. Then omega, and in each lane i the automaton of (2) on omega, for the
seven outcomes with its last table restricted to S: for each byte of the lane a
shift by 36 i plus eight times the byte's position, an AND with 255, the
addition of the state from the second byte on, and one table load; then the
test of its mask against zero and the branch. The automaton of (1) does not run
in the batch. *The lean lanes.* The lanes whose mask of (2) is not zero are
taken at once, in increasing order of i, each by its *Q path*: the E count and
its test (9.1), then the automaton of (1) on the Y9 of that lane, four bytes
taken out by a shift and an AND, three state additions and four table loads,
the AND with the mask of (2), its test and the branch. A lane whose mask X is
not zero is then a passing lane and is processed at once (below). No pass
bitmap is formed and no backup of R_0 to R_7 is stored in the batch.

**Lemma PL (the lanes are independent ordinary outer steps).** (a) The random
words of the RUN_STEPS outer steps of a run are independent and uniform on the
2^256 words, and the algorithm reads no other bit of R_0 to R_7: the guard
bits, bits 252 to 255 and the lanes 3 to 6 of the last batch are not used. (b)
The seven outer words, the member and the selector J of an outer step are
independent; the outer words are uniform words, the member is uniform on the
class, as when the eighth word modulo 2^19 is the member number (Section 8),
and J is uniform on 0 to 15. (c) So the outer steps of a run are independent
and identically distributed, and each has the law of an outer step that draws
its own uniform 256-bit word: every count of an outer step, among them the
count N_o of H1', the certified count N_16 of Lemma SL and the indicators of
Lemma BUD, has the law that it has for such an outer step. The algorithm is a
function of the RUN_STEPS random words, the probability space of 10.4.

Proof. (a) The low 32 bits of lane i of R_k are a set of bit positions of R_k,
and these sets are disjoint for different lanes; different k and different
batches are different draws. So the random words of different outer steps are
made of disjoint sets of the independent uniform bits of the draws, and they
are independent and uniform. The batch reads R_k only through its AND with M or
with the word of fc307cfc, and through bits 0, 1, 8 and 9 of each lane of
the raw R_7, which a passing lane reads for its own lane only; a passing lane
reads only its own lane of the stored words; so no other bit is read. (b) The
bits of 030c0303 and of fc307cfc are disjoint, so the addition is an OR: e1 has
the value 030c0303 at the 13 positions of 03cf8303 and the bits of W at the
other 19, so y = e1 - Y3 is the member of the class (Lemma Q) whose number is
the 19 bits of W at the free positions (Section 8). For a uniform W this number
is uniform on 0 to 2^19 - 1, as W modulo 2^19 is, and it is a function of the
19 bits of W at fc307cfc alone. J is a function of bits 0, 1, 8 and 9 of W,
which lie outside fc307cfc (03cf8303 has them set), so J is uniform on 0 to 15
and independent of the member and of the seven outer words, which are other
bits of the draws. (c) An
outer step and everything computed from it are functions of its random word
only, so (c) follows from (a) and (b). QED. Packing is a representation of
disjoint fresh random bits: it adds no premise to H1' and none to Lemma BUD.

**Lemma PB (the batch computes the outer steps of its lanes).** In every used
lane of a batch, the low 32 bits of the packed words that the batch forms for Y9
and omega are the values Y9 and omega = Y3 + y + w8 of step CO for the outer
step of that lane; the mask that the lane reads from the automaton of (2) is
that of (2) on omega restricted to S; the automaton of (1) is run on the Y9 of
exactly the lanes whose mask of (2) is not zero, and its mask is that of (1) on
Y9; and the lane is taken as passing exactly when its outer step passes the
filter of Section 8. No sum leaves its lane.

Proof. Every line of step CO is an addition, subtraction, XOR or rotation of
32-bit words. On packed words an XOR, an OR and an AND with a constant act on
each bit; an addition acts on each lane separately while no lane reaches 2^36,
and the low 32 bits of a lane are then the sum modulo 2^32; x + (z XOR M) + 1
has the low 32 bits of x - z modulo 2^32; and PROR gives in the low 32 bits of
each lane the rotation of the low 32 bits of that lane, whatever its guard bits,
since A_r and B_r keep only bits that come from the low 32 bits of the same
lane. The dropped lines reach neither Y9 nor omega, so their absence changes
neither. A table index takes bits 8 p to 8 p + 7 of the low 32 bits of lane i,
as the automaton of Section 8 takes byte p of the scalar word, so the masks are
those of the two automata, and the AND of the last tables with S restricts them
to S. An outer step passes exactly when the AND of its two masks, restricted to
S, is not zero; when the mask of (2) is zero that AND is zero whatever the mask
of (1), so running the automaton of (1) only in the other lanes changes no
decision. The bound of every lane at every operation is a function of the lines
and the constants; the participant implementation below carries it through every
operation and makes the AND with M wherever a sum could reach 2^36, so no lane
reaches 2^36. QED.
That bound computation is the participant's, a finite computation on the lines
and the constants, not on the words. It was made with the mask f8107cfc of the
sub-class in place of fc307cfc; W AND either mask is below 2^32 and the pending
constant is the same, so the bounds of the lines are the same.

*The count of a batch.* On the machine of Section 11, with 64 registers and
every constant an immediate, the batch is straight-line code with the same
count in every batch. The participant implementation counts 400 units without
the automaton of (1): the eight random words, one operation and one AND each,
16; the lines of step CO that reach Y9 or omega, 261; omega, 2; the automaton
of (2) in the seven lanes with the test of its mask and the branch, 118; the
advance of the batch count, its comparison with RUN_BATCHES and the branch, 3.
At most 25 registers are live, the two counts included, and nothing is spilled.
The certificate of the lean lanes adds 7 for the base addresses of the first
table of the automaton of (2) in the seven lanes (every other table entry holds
the base address of the next table, written once with the automata) and 16 for
the test of the last batch, the cursor and the dispatch to the lanes whose mask
of (2) is not zero: 400 + 7 + 16 = 423, charged 424; and one more move per
batch that keeps the raw R_7 in its own register for the selector, charged even
where an AND into another register would avoid it: 425 units per batch (Section
11). The raw word takes one more register, at most 26 live. A Q path costs at
most 19: four shifts, four byte masks, three state and index additions, four
table loads, the AND with the mask of (2), its comparison and the branch, and
the base addition of the first byte; with 16 for the E count, its comparison
with E_BUDGET, the branch, the store and the address, 35. Only the lanes whose
mask of (2) is not zero pay it. The implementation formed the member with the
mask of the sub-class, ran the automata of the seven outcomes, and ran the
automaton of (1) in every lane, 125 units more; for the class the member is the
same AND with another mask and the same pending addition, and restricting the
last tables to S changes no count, so the 400 units are the same. The lean
form, with the automaton of (1) in the Q path, has not been implemented.

*A passing lane.* For each passing lane, after the pass count and its test (step
1 of 9.1): its eight words are reloaded and taken out of lane i by a shift and
an AND, and step CO runs on scalar words, giving all the names that steps 2 and
3 read, 295 units in the participant's count; the context of the batch, at most
16 words (the eight packed random words, the packed Y9 and omega, the lane and
batch cursor, the current mask and the counts), is stored in fixed memory words
and reloaded, at most 4 units a word; then the pre-check of 9.7, 16 units with
the solver count and its test, and 6 for storing C2.c1, C2.b1 and e1 in fixed
words for the guard (G7); and, if T is not zero, steps 2 and 3, which may use
all 64 registers. The save and reload of the raw R_7 and the extraction of J
from lane i of it belong to step 2 (the 64 units of selection of 9.8). The
counts live in fixed memory words and are reloaded, never restored from a stale
copy. Section 11 charges 512 for the lane outside steps 2 and 3, the pre-check
and the 6 included, and 8,936 for steps 2 and 3.

*The participant check.* A participant implementation of the batch, which is
not part of the package, ran 142,858 batches, 1,000,006 outer steps drawn from
SHAKE-256, with a participant scalar implementation of step CO and of the
filter (the same lines as in the package) as the reference, with the mask and
the seven outcomes of the sub-class. In every lane all names of step CO and the
mask of the filter equal those of the scalar step CO and filter run on the
eight words of the lane with its member number: 1,000,006 of 1,000,006. The
rebuilt names of the passing lanes equal those of the scalar step CO in 4,452
of 4,452 rebuilds, and the counts are the same in every batch. In that check
the batch with the mask of the class did not run, nor the lean lanes; its
automata, those of the seven outcomes, are the ones that ran, here with their
last tables restricted to S. The submitted program runs the batch with the mask
of the class and the lean lanes on the root instance; its self-test compares
the packed batch with the scalar step CO lane by lane (Section 13). These are
participant measurements; the organizer does not run the self-test.

*In the charged schedule.* The count of a batch above is that of the batch with
the automaton of (2), and the Q path above is that of the automaton of (1),
which the submitted program keeps as its ledger (Section 11). The charge of
this package reads both masks from the direct tables of 9.10 instead: the 118
units of the automaton of (2) and the 7 base additions of its first tables
become 41 units of direct-table lane tests, 425 becomes 341 per batch, and the
Q path becomes 13 units (Section 11). Lemmas PL and PB hold for that batch as
stated, with the entries of the tables in place of the automata (Lemma TAB).

**9.7 The s-pattern pre-check and the guard (G7).** Fix a
passing outer step, with mask X, and write Q = Y9, e1 = Y3 + y and, for a trial
of it, s = E1.b1 AND beta*. By the lines of step CT read backwards, Y14 =
ROL(E3.h1, 16) XOR e1, Y10 = Y14 + C2.c1, Y6 = ROR(Y10 XOR C2.b1, 7) and E1.b1 =
ROR(Y6 XOR c1, 12), so for each bit p of beta*

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

*The allowed values.* For an outcome j of beta*, a
pattern s is compatible when E1 can give the differences beta*, tau_j and eps
with that s. With Delta(s) = beta* - 2 s - 8 modulo 2^32, the relation a XOR
(a + Delta) = tau has a solution exactly when d = (tau - Delta) mod 2^32 is even
and d / 2 has no bit outside tau, since a XOR tau - a = tau - 2 (a AND tau)
modulo 2^32 and tau[31] = 0. Enumerating the 2,048 submasks of beta* with this
exact criterion for the fourteen outcomes gives:

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
the counting program of Section 16): 16, 32, 8, 16, 32, 8 and 16 patterns with a
nonzero count on the old rows, each with nu = 3 or nu = 4, half of the count of
the row on each, and every row sum equal to its L_j of 10.1.

**Lemma VP (the pre-check is lossless).** Fix a passing outer step with mask X
and let nu be given by (V). Every listed good trial of the outer step has its
outcome in T = X AND VMASK[nu]. So an outer step or an outcome that the
pre-check skips holds no listed good trial, and the count N_o of H1' of every
outer step is the same, pointwise, as without the pre-check.

Proof. Let a listed good trial have outcome j in S and E3.h1 = h. By the proof
of Lemma F, bit j - 1 is set in both masks, so j is in X; by Lemma V, h is a
joint root of outcome j. By (PHASE), certified for every joint root in all
eight phases (9.9), and (g) of 9.4, h[16] = h[17] = 0 and h[18] = 1 XOR Q[18],
and e1[0] = e1[1] = 1 for every member, so by the identity above
the bits s[13], s[14] and s[15] of the trial are those of nu. The trial's E1
gives beta*, tau_j and eps, so its s is compatible with outcome j, and by the
enumeration above nu is allowed for j: VMASK[nu] has bit j - 1. So j is in T.
QED. The lemma uses no law of the words. It says which outcomes a passing outer
step can hold; it does not say how often nu takes a value, which no bound of
this package uses (Lemma BUD bounds the solver count without it).

*Checks (participant computations, not part of the package).* On 30,000,000 real
outer steps of the whole class (seed 7, the lines of step CO of a participant
program with the class member), 324,098 real trials with c1 in Q* whose E3.h1
had h[16] = h[17] = 0 and h[18] = 1 XOR Q[18] gave s[13] to s[15] equal to nu by
(V) in 324,098 of 324,098. Planted joint roots with y in the class (seed 11,
every root re-tested against the E3 conditions) had h[16] = h[17] = 0 and h[18]
= 1 XOR Q[18] in 2,944 of 2,944, with all fourteen outcomes covered (82 to 477
roots each). These are checks, not proofs; Lemma VP rests on (PHASE), on (g) of
9.4 and on the exact enumeration.

*The charge.* On a passing lane, after the rebuild of
step CO on scalar words, Y9, e1, C2.c1 and C2.b1 are names of the rebuild. (V)
takes 8 operations (a shift, an XOR, an AND, an XOR, an addition, an XOR, an XOR
and an AND); the address and load of VMASK[nu], the AND with X, the comparison
and the branch take 5; and the solver count, its comparison with SOLVER_BUDGET
and the branch take 3: 16 units, inside the 512 of the lane (9.6, Section 11),
paid by every passing lane, also when T is empty. The pre-check never enlarges
T, so the cap of 9.4 holds for every T. VMASK is built once from the enumeration
above, below 2^23 operations, inside the once-only allowance of Section 11.

*The guard (G7).* Every compatible s has s[3] = s[4] = 1
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
after it the solver computes h[7] by (G7) for the row of the selected slot
(9.8; the complete traversal of 9.4 does it for each searched row). On a row on
which position 7 is otherwise free, it becomes prescribed with that value; on a
row on which h[7] is already a constant ((g) of 9.4), the row is dropped for
this outer step when the two values differ, and the slot then ends the outer
step. By Lemma G7 no listed good trial is lost; joint roots that would fail the
E1 test of step 3 may be dropped early, so the paths of the solver lead to the
joint roots of the outcomes of T that satisfy (G7), and these contain the root
of every listed good trial (Lemmas CV and SL). Position 7 is then free on no
row (the table of 9.4). h[7] is computed after the row's own patch of h[6] and
is never shared across a family.

*The charge of (G7).* 128 more units for each searched
row, here the one row of the selected slot, inside its 1,408 (9.8): the six source bits e1[22], e1[23], C[22], C[23], B[22] and B[23], the
loads and addresses of the three source words, x, the carry a22, the majority,
h[7], the comparison with an existing constant and its branch, and the insertion
of the value into the descriptor of position 7, fewer than 16 blocks of at most
8 units; the scratch words are released before the 32 descriptors are resident,
so the traversal uses no more registers. The caller stores C2.c1, C2.b1 and e1
in three fixed memory words, at most 6 more units, inside the 512 of the lane.
The extra prescribed bit of the written-out rows is inside the once-only
allowance. No new budget, mean or premise: the solver count still counts every
outer step whose T is not empty, before (G7) runs.

**9.8 One slot per outer step: the one-path solver with the guard (G15).** The
search of this package does not return every joint root of an outer step. In an
outer step that reaches the solver it follows the single path of one static
slot, named by the selector J of step 1 of 9.1, and certifies at most one trial.
Every listed good trial of the outer step owns exactly one of 16 slots, so the
certified count of the outer step is 0 or 1 with mean exactly its number of
listed good trials divided by 16 (Lemma SL, 10.2). This rests on the guards of
9.4 being exact for every joint root, which the certificate of 9.9 establishes
in all eight phases, on the single traversal from the common state of 9.4, on
the guard (G15) below, and on the exact envelopes of the mask of (1) from the
certificate of Section 8.

*The guard (G15).* Write e = e1 = Y3 + y, C = C2.c1, B = C2.b1, A = Y1 + w12 and
V = Y12, names of step CO, and for a word h put Y14 = ROL(h, 16) XOR e,
Z = (Y14 + C) XOR B, Y6 = ROR(Z, 7), a1 = Y6 + A, d = ROR(a1 XOR V, 16) and
c = Y11 + d, all modulo 2^32, with Y11 = 7af77f38 (Fact P), whose bit 0 is 0. For h = E3.h1
of a trial these are the words of step 3 of 9.1, and c is its c1 (the inverse of
Lemma IP). For a row whose h[6] is fixed (9.4) define two bits and five row
words,

    alpha = h[6] XOR e[22] XOR C[22] XOR B[22],   v = V[16] XOR 1 XOR A[16],
    E22 = e >> 22,   CA = (C >> 22) + alpha,   B22 = B >> 22,
    AV = ((A >> 16) AND 511) + v,   V16 = (V >> 16) AND 511,

and for a prefix H that holds bits 0 to 14 (every higher bit zero)

    L      = (H >> 6) XOR E22,
    zeta   = ((((L + CA) mod 2^10) XOR B22) >> 1) AND 511,
    p      = (zeta + AV) AND 511,
    c_star = (Y11 AND 511) + (p XOR V16).                               (G15)

**Lemma G15.** Let a listed good trial of an outer step have outcome j and E3.h1
= h, and let c_star be computed by (G15) from H = h AND 7fff and the row words
of row j. Then c_star AND 08b = 0, and h[15] is bit 8 of c_star.

Proof. By Lemma CV (a) the bits of h at the prescribed positions of row j, h[6]
among them, are those of the row, so alpha and the row words are formed with
h[6] of h. By the proof of Lemma G7, Z[22] = 0 and Z[23] = 1. The trial's c1 = c
is in Q*, and 0e09818b has the bits 0, 1, 3, 7 and 8 set while 02008000 has them
zero, so c[0] = c[1] = c[3] = c[7] = c[8] = 0. Let h' = h with bit 15 cleared,
and write Y14', Z', Y6', a1', d' and c' for its words. (i) The carries. Let
alpha' be the carry into bit 22 of Y14' + C, and v' the carry into bit 16 of
Y6' + A. Bit 15 of h is bit 31 of Y14, which enters neither carry, so alpha' and
v' are also the carries of h. Bit 22 of Y14 is h[6] XOR e[22], and
Z[22] = (Y14 + C)[22] XOR B[22] = 0 gives alpha' = h[6] XOR e[22] XOR C[22] XOR
B[22] = alpha. c[0] = Y11[0] XOR d[0] = d[0], so d[0] = 0 and a1[16] = V[16]; with
Y6[16] = Z[23] = 1 the sum bit a1[16] = Y6[16] XOR A[16] XOR v' gives v' =
V[16] XOR 1 XOR A[16] = v. (ii) The slice. Bits 22 to 31 of Y14' are the ten
bits of (H >> 6) XOR E22 = L, since H holds bits 6 to 14 of h' and bit 15 of h'
is zero. With the carry alpha into bit 22, bits 22 to 31 of Y14' + C are (L +
CA) mod 2^10, and after the XOR with B22 they are bits 22 to 31 of Z'; bits 23
to 31 of Z' are bits 16 to 24 of Y6' = ROR(Z', 7), that is zeta. With the carry
v into bit 16, bits 16 to 24 of a1' = Y6' + A are p; bits 0 to 8 of d' = ROR(a1'
XOR V, 16) are p XOR V16; and since no carry enters bit 0, bits 0 to 8 of c' =
Y11 + d' are the low nine bits of c_star. (iii) Bit 15. Y14 and Y14' differ in
bit 31 alone, so Y14 + C and Y14' + C agree in bits 0 to 30 and differ in bit
31, and Z, Z' differ in bit 31 alone; Y6, Y6' differ in bit 24 alone; a1, a1'
agree in bits 0 to 23 and differ in bit 24; d, d' agree in bits 0 to 7 and
differ in bit 8; and c, c' agree in bits 0 to 7 and differ in bit 8, since the
carry into bit 8 of Y11 + d depends on bits 0 to 7 only. If h[15] = 0 then c =
c'; if h[15] = 1 then c and c' agree in bits 0 to 7 and differ in bit 8. In both
cases bits 0, 1, 3 and 7 of c_star are those of c, which are zero, so c_star
AND 08b = 0; and c[8] = 0 gives bit 8 of c_star = c'[8] = h[15]. QED. The lemma
uses no law of the words. A joint root whose true carries differ from alpha and
v is not a listed good trial and may be dropped by the guard; the certificate of
step 3 does not depend on the guard.

*Use in the solver.* The five row words are computed once for the selected row
after its h[6] is fixed, from e1, C2.c1 and C2.b1, which the caller keeps in
fixed words (9.7), and from the names Y1 + w12 and Y12 of step CO, and are kept
in five fixed words. Position 15 is free on every row of S (the table of 9.4).
When the path reaches position 15 its prefix holds bits 0 to 14 of h and no
other bit; the solver computes c_star by (G15), ends the outer step if c_star
AND 08b is not zero, and otherwise reads the forced array with a temporary copy
of the key of position 15 in which the constant flag is set and the constant is
bit 8 of c_star, as at a prescribed position; the static key is not changed. The
remaining free positions, the set F' of the row, are {13, 30} on the rows
175020a0, 185020a0 and 685020a0 and {9, 13, 30} on the rows 275020a0, 285020a0
and 385020a0. By Lemma G15 no listed good trial is lost: the path of its root
reaches position 15 with the root's own prefix, passes the test and takes the
arc of the root's own bit 15. Other joint roots may be dropped.

*Envelopes.* Let m1 be the mask of (1) on Y9 of the outer step, restricted to S
(9.6). In an outer step that reaches the solver m1 is not empty, and by the
certificate of Section 8 it is a subset of one of the four sets {175020a0},
{275020a0}, {285020a0, 385020a0} and {185020a0, 385020a0, 685020a0} (9.4). The
*envelope* of the outer step is the first of these four sets, in this order,
that contains m1. It is a function of Y9 alone, and it contains every outcome
of T, since T is a subset of X and X of m1.

*Slots.* Each envelope has static ranges of slots, padded to 16:

| envelope | slots 0 to 15 |
| --- | --- |
| {175020a0} | 0 to 3: row 175020a0; 4 to 15: padding |
| {275020a0} | 0 to 7: row 275020a0; 8 to 15: padding |
| {285020a0, 385020a0} | 0 to 7: row 285020a0; 8 to 15: row 385020a0 |
| {185020a0, 385020a0, 685020a0} | 0 to 3: row 185020a0; 4 to 11: row 385020a0; 12 to 15: row 685020a0 |

A row with the set F' has 2^|F'| slots, 4 or 8. For a slot s in the range of a
row that starts at s0, the offset is r = s - s0, and bit k of r is the value
that the slot gives to the k-th position of F' in increasing order; position 15
is not a slot bit. The ranges depend on the outer step only through the
envelope: they are not compacted around rows that are not in T or around paths
that a carry test or a guard prunes.

*The one path.* Given J: if slot J is padding, or its row j is not in T, the
outer step ends with no root. Otherwise the solver runs the formulas and tests
(a) to (g) of 9.4 for the family of row j and for row j, the patches of the row,
the guard (G7) of 9.7 and the row words of (G15), as the complete traversal of
9.4 does for that row; if a test says that the row has no joint root, the outer
step ends. Both carry guesses a[20] that (a) keeps reach the same common state
at depth 7 (9.4, one traversal), so one path from that state serves both, and
the check of (J2) as a word at the leaf enforces the carry closure. From depth 7
the solver walks the positions 7 to 31 once: a prescribed position reads the
forced array, or at position 20 the selected array, with its constant or guard
written into the key as in 9.4, and takes its one arc; position 15 is prescribed
by (G15) as above; a position of F' reads the dual array and takes the arc whose
bit of h is the value that slot J gives to that position. If a position has no
such arc, the outer step ends. At depth 32 the solver checks (J1), (J2) and (J3)
as words for the h of the path; if they hold, it returns h with the outcome j,
and otherwise the outer step ends. A failure is not followed by another slot: J
is drawn once per outer step, with the outer step's own random word, and is
never drawn again.

*The charge, 8,936.* One selected row costs at most

    4,096 global + 2,304 one family + 1,408 one row + 25 * 32 single-path
    nodes + 64 (G15) + 80 leaf + 120 root + 64 selection = 8,936

machine units, with the blocks of Section 11: 4,096 once per outer step that
reaches the solver (E' and E XOR E', the names of step CO, the control); 2,304
for the family of the row, the formulas of (a) to (e) of 9.4 and the walks of
bits 0 to 5 under both guesses; 1,408 for the row, its 32 descriptors, the walks
of bit 6, the patches, the 128 of (G7) and the 128 of the five row words of
(G15); one node at each of the 25 positions 7 to 31, at most 32 each: a forced
node costs at most 20 (Section 11), the selected node at position 20 at most 24,
and a free node at most 8 more operations than a forced one to take one arc out
of the dual entry by the slot's bit, at most 28; 64 more at position 15 for
(G15); 80 for the leaf check; 120 for step 3 on the one root by the tests of
Lemma SC; and 64 for the selection: the save and reload of the raw R_7, the
extraction of J from bits 0, 1, 8 and 9 of lane i, the choice of the envelope
from m1, the dispatch to the static range and the rank bits of the offset. No
parent is saved and no second child restored. At most one leaf check, one
(G15) and one certificate are charged, and the whole 8,936 is charged also when
the path fails or the slot is padding. The registers are those of the complete
traversal (Section 11) without its five saved parents, with one more for the
offset r: at most 59 of the 64; (G15) and the certificate use only its ten
temporaries. This schedule is a proved upper allowance written out by blocks in
Section 11; it has not been executed.

**9.9 The all-eight-phase certificate of the guards.**
The guards (PHASE) and (P*) of 9.4 are used by Lemmas J0, VP, G7, CV and SL as
facts about every joint root on the whole class. This subsection gives an exact
finite verification of both, for the fourteen outcomes of beta* in all eight
phases (b, u, v), and its output.

*The reduction.* Change the coordinates of E3 from (y,
h, Q, w8) to (y, h, g, e), where g = Q + h, f = ROR(y XOR g, 12) and e = Y3 + y +
w8 + f. The inverse is Q = g - h and w8 = e - Y3 - y - f, so the change is a
bijection. Put k = h XOR e and j = ROR(k, 8), and with sgn(p, M) = M - 2 p
modulo 2^32 enumerate

    ph = h AND eta,  pg = g AND theta,  pf = f AND sigma,  pe = e AND eps,
    pt = (g + j) AND tau,  pb = j AND mu.

The three difference identities, which are necessary and sufficient, are

    sgn(ph, eta) = sgn(pg, theta) = d;
    sgn(pe, eps) = DY3 + sgn(pf, sigma);
    sgn(pb, mu)  = sgn(pt, tau) - d.

Also y AND theta = ROL(pf, 12) XOR pg. Given these masks, a carry recurrence
with two states counts the remaining (g, k) additions exactly; outside eta OR
eps, h has 256 independent choices. Every bit that (PHASE) and (P*) test lies in
eta OR eps, so the part of h fixed by the masks suffices. Every concrete tuple
contributes once, with a nonnegative weight, to the total of its phase, and to
the wrong-guard count of its phase when its h violates (PHASE) or (P*).
Therefore a zero wrong-guard count proves that no joint root violates (PHASE) or
(P*), pointwise and in all eight phases, and not a statement about average
retention.

*The verifier.* The following text is ASCII Python
that uses only the pinned constants and the class. It reads no participant
record; it enumerates the actual class (all 2^19 members) to form its
histograms, and assumes nothing about representatives of the phases. For both
values of `new`, that is for the seven old rows and the seven new rows, it
asserts that the wrong-guard count is zero in each of the eight phases and that
the total in each phase equals the count of the table of the parity certificate
in 9.4 (a * 2^49 on an old row; a * 2^47 or 0 on a new row, by the phase). The
function `wrong` tests h[0] = 0, h[1] = 1, h[2] = 1 XOR b, h[10] = b, h[16] =
h[17] = 0, h[11] = 1 XOR h[3], h[24] = h[3] XOR h[12] XOR u, which is (PHASE),
and h[6] XOR h[13] XOR h[25] = u XOR tau[14], which is (P*). The text has 67
lines and 2,261 bytes.

```python
from collections import Counter
from functools import lru_cache
M=(1<<32)-1; A=0x830303cf; E=0x6e21be55; AE=A|E
Y=0x8127c181; DY=(0x7edf3e7e-Y)&M
Cmask=0x03cf8303; Cv=0x030c0303
def bit(x,i): return (x>>i)&1
def rr(x,r): return ((x>>r)|(x<<(32-r)))&M
def rl(x,r): return rr(x,32-r)
def sub(m):
 x=m
 while True:
  yield x
  if not x: break
  x=(x-1)&m
def sg(x,m): return (m-2*x)&M
def pat(m,d):
 q=(m-d)&M
 if q&1 or (q>>1)&~m: return ()
 q>>=1
 return (q,q|(1<<31)) if m>>31 else (q,)
@lru_cache(None)
def dp(pg,T,k,pt,t):
 s=[1,0]
 for i in range(32):
  j=(i+8)&31; z=[0,0]
  for c in (0,1):
   for x in ((bit(pg,i),) if bit(T,i) else (0,1)):
    for v in ((bit(k,j),) if bit(AE,j) else (0,1)):
     a=x+v+c
     if not bit(t,i) or (a&1)==bit(pt,i): z[a>>1]+=s[c]
  s=z
 return sum(s)
def wrong(h,p,t):
 b=p&1; u=(p>>1)&1
 return (h&3)!=2 or bit(h,2)!=(1^b) or bit(h,10)!=b or bool(h&0x30000) or bit(h,11)!=(1^bit(h,3)) or bit(h,24)!=(bit(h,3)^bit(h,12)^u) or ((h&0x02002040).bit_count()&1)!=(u^bit(t,14))
G=sum(1<<i for i in (0,1,2,3,6,10,11,12,13,16,17,24,25))
X=(A&E)|(E&~A&G); B=rr(A^E,8)
for new in (0,1):
 for base,a in zip((0x175020a0,0x185020a0,0x275020a0,0x285020a0,0x385020a0,0x675020a0,0x685020a0),(24,16,4,24,32,1,6)):
  t=base^(new<<14); sig=t^rr(t,1); T=rl(sig,12)
  H=Counter()
  for f in sub(M^Cmask):
   e=Cv|f; p=bit(e,2)+2*bit(e,21)+4*bit(e,26)
   H[p,((e-Y)&M)&T]+=1
  D=[(ph,pg,sg(ph,A)) for ph in sub(A) for pg in pat(T,sg(ph,A))]
  L=[(pf,pe) for pf in sub(sig) for pe in pat(E,(DY+sg(pf,sig))&M)]
  W={}
  for pg in {q[1] for q in D}:
   w=Counter()
   for pf,pe in L:
    for p in range(8): w[pe&X,p]+=H[p,rl(pf,12)^pg]
   W[pg]=w
  tot=[0]*8; bad=[0]*8
  for ph,pg,d in D:
   for pt in sub(t):
    for pb in pat(B,(sg(pt,t)-d)&M):
     kb=rl(pb,8)
     for (x,p),w in W[pg].items():
      if not w: continue
      n=w*dp(pg,T,kb|((ph^x)&A&E),pt,t)<<(32-AE.bit_count())
      h=ph|((x^kb)&E&~A)
      tot[p]+=n
      if wrong(h,p,t): bad[p]+=n
  assert bad==[0]*8,(hex(t),bad)
  want=[a<<(47 if new else 49) if not new or (((p>>1)^(p>>2))&1 and (base in (0x185020a0,0x285020a0,0x385020a0,0x685020a0) or p&1)) else 0 for p in range(8)]
  assert tot==want,(hex(t),tot,want)
print("all eight phases: exact guards and counts certified")
```

*Its output.* The participant ran this text verbatim, locally. Its complete
output is the one line

    all eight phases: exact guards and counts certified

which the program reaches only when all fourteen pairs of assertions hold
(assertions enabled, the default): for every row of the fourteen and every
phase, zero joint roots violate (PHASE) or (P*), and the total equals the count
of the table of 9.4. So (PHASE) and (P*) hold for
every joint root of every outcome of beta* on the whole class, in all eight
phases, and the cells of the parity table of 9.4 are exact in all eight phases.
This is a participant computation of an exact count, not a sample; the
organizer does not run it, and it is not one of the declared experiments. It
closes the finite guard requirement of the solver for the stated advice (Lemma
ADV (f)); it does not bear on the rate of H1' or on Lemma BUD.

**9.10 Direct filter tables.** The charged schedule of
this package reads the two masks of the outer filter from two tables that step
0 of 9.1 builds once. For every 32-bit word w,

    TAB2[w] = the mask of the automaton of (2) on w, restricted to S;
    TAB1[w] = the mask of the automaton of (1) on w, restricted to S,

with the automata of Section 8 and their last tables ANDed with 5f, as in
9.1. Each table has 2^32 entries of one 256-bit word, 2^37 bytes, so the two
take 2^38 bytes. Step 0 fills them by running the two automata on every word:
below 2^38 primitive operations for both, every automaton lookup, address,
store, mask and loop included, charged 2^39 machine units once.

**Lemma TAB (the direct tables decide as the automata do).** For every word w,
TAB2[w] and TAB1[w] are the masks, restricted to S, that the automata of (2) and
(1) give on w. So in every outer step the mask of (2), the E count, the mask
X, the pass decision, the pre-check, the slot and every later step of 9.1 are
the same whether the masks are read from the tables or computed by the
automata. Lemmas F, PL, VP, G7, V, CV and SL and the bound of 10.4 hold
unchanged, and Lemma PB holds with TAB2[omega] and TAB1[Y9] in place of the masks
of the automata.

Proof. Step 0 writes into entry w of each table the output of the same
automaton, with the same last tables restricted to S, on the same word w. The
search reads TAB2 at omega and TAB1 at Y9, the words on which the automata run
(Lemma PB), so each mask that it reads equals the mask of the automaton. Every
decision of 9.1 is a function of these masks and of words that the tables do
not change. The tables are fixed before the first batch and read no random
bit, so the random words of the outer steps, their disjoint bits and the
selector J are those of Lemma PL. QED.

*The independence that the bound uses*. As
in 9.6, the eight fresh 256-bit words of a batch give seven 36-bit lanes; the
seven outer words, the 19 member bits and the four selector bits of a lane are
disjoint from those of every other lane, and the selector comes from bits of
the lane's raw eighth word that the member does not read, kept before the AND
with fc307cfc. Every listed good trial of an outer step owns exactly one of
the 16 slots (Lemma SL), so the certified count N_16 of each outer step is 0
or 1, with mean exactly E[N_o] / 16 and E[N_16 (N_16 - 1)] = 0, and the outer
steps are independent (Lemma PL). The success bound of 10.4 therefore needs
no premise on how successes depend on each other, within one outer step,
between members, between outer steps or between batches. The direct tables
change none of this.

*The charge with direct tables.* Section 11 charges the batch with the direct
tables 341 machine units and a Q path 13. The packed lines of 9.6, their
interval bounds and their ANDs with M are unchanged, so no lane's guard bits
escape, and the lane tests use no packed subtraction. With the 512 of a passing
lane and the 8,936 of steps 2 and 3, a passing outer step costs at most 13 +
512 + 8,936 = 9,461 machine units, whatever its words.

*What is not implemented.* The direct tables have not been built, and no batch
with them has been run. The charges 41, 17, 1 and 13 are bounds written out in
words, and 16, 261, 2 and 3 are the counts of 9.6; the submitted program
computes the same masks with the automata (Section 13).

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

The rows j = 1 to 7 have the L_j of the sub-class of 6.1 and four times its
N3_j, so on this scale they carry exactly its 67,698,688 = 1,033 * 2^16. S
leaves out row 6, 675020a0, with 65,536 = 2^16, and carries 67,633,152 =
1,032 * 2^16, so p = 1,032 * 2^-101 exactly; the rows j = 8 to 14, with bit
14 of tau set, add 3,999,744, 5.6 per cent of the part of beta*, and are not
listed either. The integers L_j and N3_j are those of the participant's
counting program, printed in Section 16 with the six rows of its output that
this search lists; it prints L_j N3_j / 2^81, four times the last column, and
the six listed rows sum to 270,532,608 = 4 * 67,633,152 there, and the scale
2^83 is that of a trial with Y4 uniform in the 2^19 members of the class. Of
the 52 values of tau that pass the screens of the count, 30 have N3_j > 0 and
14 have L_j N3_j > 0. The count uses no rule on h1.

*Why S.* Of the 16,383 nonempty sets of outcomes of beta*, S gives the least
exact charge of the complete traversal (the cap 31,456 of 9.4); it has not been compared under the one-path charge
of Section 11. S is part of the stated advice, and the analysis uses its stated
value only (Lemma ADV), not that it is least under any charge.
The row 675020a0 carries 0.1 per cent of the count of the seven, but dropping it
lowers the share of passing pairs by a factor of 1.12 (Section 8).

*Why beta*.* Beta* is not chosen by a ranking in this package: it is the beta
of the solution with which the participant's solver found the six constants
(Section 12), and it is stated here as advice with its cube. Its cube of c1 has
k = 11 fixed bits, mask 0e09818b and value 02008000. The submitted program
stores beta* (`BETA_STAR`) and the mask and value of its cube.

**10.2 Lemmas on the counter sampler.** The following lemmas are given with
their hypotheses and proofs; each is exact mathematics under the hypotheses
stated. The participant compared Lemmas S1 to S4 and Lemma IP with the
construction line by line; the carry Lemma S5 was not re-derived by the
participant. They do
not prove the rate of H1' or the success probability; 10.3 states what remains
a premise. The proofs of Lemmas S1 and S9 hold for any fixed set of members; here the set is the class.

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
the counting program of Section 16 and are not proved by this lemma.

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

**Lemma S9 (the success mass lies on passing outer steps).**
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
probability pi_o of the sampler itself; that pi_o equals pi is not proved, and
no bound of this package uses it.
Statement (b) is about M and says nothing about the sampler.

*What the search certifies.* The lemmas below concern the search of 9.1. Lemma V
follows from 3.3; Lemma SC is the certificate of step 3; Lemma CV rests on the
constants and guards of 9.4, among them (PHASE) and the parity certificate
(P*), certified for every joint root on the class in all eight phases by the
verifier of 9.9, and Lemma J0; Lemma SL, the one-slot lemma, rests on Lemmas
CV, G7 and G15.

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

**Lemma SC (the sparse certificate).** Fix an outer step and a joint root h of
outcome j, tau = tau_j, and let Y14, Z, Y6, a1, d and c be the words of h of 9.8
(c is the c1 of its trial, by the inverse of Lemma IP). Put b = ROR(Y6 XOR c,
12), a = a1 + b + w5, s = b AND beta*, z = ROR(d XOR a, 8), DY11 = Y11' - Y11 =
0a08818b (Fact P) and p_tau(s) = ((tau - beta* + 8 + 2 s) mod 2^32) >> 1, all
modulo 2^32. Consider the four tests

    (Q)  c AND 0e09818b = 02008000;
    (A)  a AND tau = p_tau(s);
    (C)  (c + z) XOR ((c + DY11) + (z XOR ROR(tau, 8))) = eps;
    (T)  t is not zero, where Y2 = ROL(Y14, 8) XOR C2.d1,
         w0 = Y2 - C2.a1 - C2.b1 and t = ROL(K0.d1, 16) XOR (IV[0] + IV[4] + w0).

All four hold exactly when c1 = c is in Q*, its counter word t is not zero, and
E1 on A and on B gives the XOR differences tau and eps of its a and c outputs.

*Proof.* By 6.2, E1 on A is G(Y1, Y6, Y11, Y12, w12, w5) and on B G(Y1, Y6,
Y11', Y12, w12, w5 + delta) with delta = fffffff8. On A its first-half values
are E1.a1 = Y6 + Y1 + w12 = a1, E1.d1 = d, E1.c1 = c and E1.b1 = b, its a output
is a, and its d and c outputs are z and c + z. On B the values a1 and d are the
same, the third is c + DY11 and the fourth b' = ROR(Y6 XOR (c + DY11), 12), as in
the proof of Theorem C (iv), which also shows that b XOR b' = beta* exactly when
(Q) holds, that is when c is in Q*. If (Q) fails, c is not in Q* and both sides
are false. Assume (Q). Then b' = b XOR beta* = b + beta* - 2 s, since x XOR y =
x + y - 2 (x AND y), and the a output on B is a' = a1 + b' + w5 - 8 = a +
Delta(s), with Delta(s) = beta* - 2 s - 8. a XOR a' = tau holds exactly when
a + Delta(s) = a XOR tau; by the identity (a XOR tau) - a = tau - 2 (a AND tau)
modulo 2^32, that is when 2 (a AND tau) = tau - Delta(s) modulo 2^32. As tau[31]
= 0, a AND tau < 2^31, so 2 (a AND tau) is below 2^32 and the condition says
that the number (tau - beta* + 8 + 2 s) mod 2^32 is twice a AND tau. That number
is even, since tau, beta* and 8 are even, so the condition is (A). Assume (Q)
and (A). Then a' = a XOR tau, the d output on B is ROR(d XOR a XOR tau, 8) = z
XOR ROR(tau, 8), and the c output on B is (c + DY11) + (z XOR ROR(tau, 8)), so
the c difference is eps exactly when (C) holds. (T) computes the counter word
of step CT for c: Y14 is that of the inverse of Lemma IP, and Y2, w0, K0.a1 =
IV[0] + IV[4] + w0 and t are the lines of step CT. So the four tests hold
exactly when c is in Q*, the a and c differences are tau and eps, and t is not
zero. QED. The lemma uses no law of the words; with Lemma V a joint root passes
the four tests exactly when it is the E3.h1 of a listed good trial.

**Lemma CV (coverage of the complete traversal).** Fix an outer step that
passes the filter, with T = X AND VMASK[nu] of 9.7. (a) When T is not empty,
the complete traversal of 9.4 returns every joint root that satisfies (G7) of
every outcome whose bit is set in T, each once, and nothing else; the path to
each such root follows, at every position, the one arc of the root's own bit.
(b) Applied to every returned root, step 3 of 9.1 certifies exactly the roots
that are the E3.h1 of a listed good trial of the outer step, and the E3.h1 of
every listed good trial of the outer step is among the roots; when T is empty
the outer step holds no listed good trial (Lemma VP). So the number of joint
roots of a passing outer step that step 3 would certify, zero when T is empty,
is its count N_o of H1' (10.3), the number of its listed good valid trials over
all of Q*, and N_o is at most 32.

*Proof.* (a) A leaf gives a root only when (J1), (J2) and (J3) hold as words,
so every returned word is a joint root of the outcome it is returned with.
Conversely, let h be a joint root of a searched outcome that satisfies (G7). By
(PHASE) and (P*), which hold for every joint root in all eight phases (9.9), by
Lemma J0, (G7) and the constants and guards of 9.4 its bits have those values,
and
its carries pass every test of (a), (b) and (e) there: its own carry into bit
20 is a kept guess, every kept guess reaches the common state at depth 7, and
the single traversal follows the arcs of its bits from the carry pairs that its
own carries give, each read from the array of its position with the guard
values that its own bits give, and reaches its leaf, where the three conditions
hold. A depth-first traversal reaches each node once, so h is returned once. No
word is a joint root of two outcomes (9.4). (b) Let c1 in Q* give a listed good
trial with outcome j, and let h be its E3.h1. By the proof of Lemma F, h
witnesses (1)_j for Y9 and the trial's f witnesses (2)_j for omega, so bit j - 1
is set in both masks, and by Lemma VP it is set in T; in particular T is not
empty. By Lemma V, h satisfies (J1) to (J3) of outcome j, so it is a joint root;
it satisfies (G7) by Lemma G7, and the traversal returns it by (a). Step 3 maps it to
c1, since it computes the inverse of the permutation c1 -> E3.h1 of Lemma IP; c1
is in Q*, its t is not zero and its E1 outcome is j, so the root is certified
(Lemma SC).
Conversely, a certified root h of outcome j gives a c1 in Q* with t not zero
whose E1 differences are tau_j and eps, and h satisfies (J1) to (J3), so by
Lemma V the trial of c1 has R = 0 with outcome j: it is a listed good trial.
Different roots give different c1 (Lemma IP), and an outer step has at most 32
roots (9.4). QED.

**Lemma SL (one slot per success).** Fix the seven outer words and the member of
an outer step, O, and let N(O) be its count N_o of H1': the number of its listed
good valid trials over all of Q*. Let N_16 be 1 when the search of 9.1, reaching
this outer step, certifies a root in it, and 0 otherwise. (a) There is a set of
N(O) distinct slots in 0 to 15, a function of O alone, such that N_16 = 1
exactly when the selector J of the outer step lies in it. (b) So N(O) <= 16,
N_16 is 0 or 1, and since J is uniform on 0 to 15 and independent of O (Lemma
PL),

    E[N_16 | O] = N(O) / 16,   E[N_16] = E[N_o] / 16,   E[N_16 (N_16 - 1)] = 0.

*Proof.* (a) If N(O) = 0 then no root is certified, since every certified root
is the E3.h1 of a listed good trial (Lemmas CV (b) and SC); the set is empty.
Otherwise the outer step passes, T is not empty, and every listed good trial has
its outcome j in T (Lemmas F and VP). Its E3.h1, h, is a joint root of outcome j
that satisfies (G7) (Lemmas V and G7), and (G15) gives its own bit 15 from its
bits 0 to 14 (Lemma G15). The envelope of the outer step contains T (9.8), so
row j has a range of slots in it; the *slot of the trial* is the slot of that
range whose offset gives the positions of F' of row j the bits of h at those
positions. Run with that J, the one-path solver of 9.8 finds row j in T, passes
the tests of (a) to (g) of 9.4 and (G7) for row j, since h satisfies them
(Lemma CV (a)), and at every position takes the arc of h's own bit: at a
prescribed position other than 15 the only arc, which is h's by Lemma CV (a); at
position 15 the arc of the bit that (G15) computes from the prefix of the path,
which is the prefix of h, so the test passes and the bit is h[15] (Lemma G15);
and at a position of F' the arc whose bit is the slot's value, which is h's bit
by the choice of the slot. So it reaches the leaf of h, where (J1) to (J3) hold,
and step 3 certifies h (Lemmas CV (b) and SC). Two listed good trials have
different roots (Lemma IP). If their rows differ, their slots lie in different
ranges; if their rows are the same, the same slot would give the same bits at
the positions of F', and the path, which has one arc at every other position
(at position 15 the arc of the bit that (G15) computes from the prefix), would
reach the same leaf; so their slots differ. Conversely, for a J outside the set
of these N(O) slots, the slot is padding, or its row is not in T, or its path
ends, or it reaches a leaf that is not the root of a listed good trial, which
step 3 then does not certify (Lemmas CV (b) and SC); in every case N_16 = 0.
The set is a function of O alone, since the envelope, T, the ranges, the row
words of (G15) and the roots are. (b) The set has N(O) distinct elements among
16 values, so N(O) <= 16. N_16 is the indicator of J in the set, and J is
uniform and independent of O, so E[N_16 | O] = N(O) / 16; taking the
expectation over O gives E[N_16] = E[N_o] / 16; and N_16 (N_16 - 1) = 0 for a
count of 0 or 1. QED. The lemma uses no law of the outer words or of the member:
it holds for each O. It needs the guards of 9.4 to hold for every joint root,
which the certificate of 9.9 gives in all eight phases, the single traversal
from the common state (9.4), and Lemma G15.

So the search of 9.1 keeps, in every outer step, exactly 1/16 of the mean
number of listed good trials that an enumeration of all of Q* in that outer step
finds, with the same outer steps, the same members y and the same filter. The
count N_o of every outer step is the same as for that enumeration, and H1' is
about its mean only; Lemma BUD is about three counts of the outer steps, which
the slot selection does not change, since J is read only after the solver
count.
Lemmas V, SC, VP, G7, G15, CV and SL use no law of the words. The guards of the
solver are lossless: (PHASE) and (P*) are consequences of exact counts of the
class, certified for every joint root in all eight phases by the verifier of
9.9, (P*) with a count of 0 for the other parity in every phase and every
outcome (9.4), and Lemma J0 is algebra; none drops a member or a joint root. The
pre-check and the guards (G7) and (G15) lose no listed good trial (Lemmas VP, G7
and G15), and drawing the outer steps seven to a batch changes no outer step
(Lemma PL).

**10.3 Heuristics.**

**Heuristic H1' (score-critical; a rate only).** Over the coins of the run, the
RUN_STEPS independent uniform words of step 1 of 9.1, let N_o be the number of
listed good valid trials (9.1) of one outer step, counted over all of Q*
whether or not the outer step passes the filter or the pre-check. *Rate:*

    E[N_o] >= (2^21 - 1) q,   q = FACTOR * 2^-128,

just under 5p / 7, about 2^-91.474. Nothing else is declared about N_o: no
clause on how the listed good trials of one outer step depend on each other,
and no bound on its factorial ratio rho.

The rate is declared for these trials: the whole class of eta with no rule on
h1, the six outcomes of S, and the independent outer steps of 9.1, each with its
own random word made of disjoint fresh bits (Lemma PL). Neither the filter nor
the pre-check changes it: both skip only outer steps and outcomes that hold no
listed good trial (Lemmas F and VP), so N_o is the same count, pointwise. The
slot selection of 9.8 does not change N_o either; it changes what the search
certifies, N_16, whose mean is exactly E[N_o] / 16 for every law of the words
(Lemma SL).

In the terms of Lemmas S1 to S4 the premise is this: the construction's
pushforward of the uniform outer words and members, with c1 running over all of
Q*, onto the seven model words (E1.d1, E1.b1, E1.a2, Y4, Y9, w8, E3.h1) carries
at least the share FACTOR / 138,512,695,296, just under 5/7, of the
complete-success integral p of the conditional law of Lemma S1, and that stays
true after the member with t = 0 is dropped (Lemma IP). It does not follow
from the model or from Lemmas S1 to S5 and S9. The factor FACTOR = 98,937,639,497 is
assumed; 10.1 gives what it is set against, the count 138,512,695,296 of the
six outcomes of S, of which it is five sevenths rounded down. The filter does
not change it.

*No dependence clause.* No clause on how the listed good trials of one outer
step depend on each other is declared. The search certifies at most one trial
per outer step, and N_16 has the exact mean E[N_o] / 16 and E[N_16 (N_16 - 1)] =
0 whatever the joint law of the trials of an outer step (Lemma SL).

*The rate on passing outer steps.* By Lemma S9 (a), N_o is zero on every outer
step that the filter rejects, so the rate says E[N_o | the outer step passes]
>= (2^21 - 1) q / pi_o, with pi_o of Lemma S9. Per member of Q* of a passing
outer step the rate is then at least about q / pi_o; for pi_o = pi it is q / pi
= 98,937,639,497 / (279,070,422,111 * 2^80), about 2^-81.496: the rate of H1'
divided by the pass share, with no part of the counted mass lost (Lemma S9).
The success argument below uses the rate per walked outer step and needs no
value of pi_o, and pi_o enters no budget: the three are the proved figure L of
Lemma BUD.

*What is proved and what is not.* Proved (Lemmas S2 to S4): the outer words of
a step are uniform in the chart of the seven context words of Section 4; Y12
and w5 are independent uniform words; E1.a1 and E1.a2 - E1.b1 are independent
uniform words at every fixed c1; and the sampler of Section 8 is exactly the
uniform-counter sampler conditioned on c1 in Q*. Proved as well (Lemmas V, CV
and SL, 10.2): every listed good trial of an outer step owns exactly one of the
16 slots, and the search certifies it exactly when the selector of the outer
step names that slot, so N_16 is 0 or 1 with mean E[N_o] / 16. Not proved: that
E1.b1, E1.a2, E3.h1, Y9 and w8 have the model's joint law with the rest; the
rate reduces to one success-weighted density of seven words that
the outer step fixes, Y12, Y1 + w12, C2.b1, C2.c1, w5, Y9 and w8, and that
density has not been counted. Not proved either: how much of the success mass
the member with t = 0 carries (Lemma IP bounds the number of dropped trials,
one in 2^21, not their mass).

*No budget of steps 2 and 3.* The search declares no premise on the mean of any
count of work. Steps 2 and 3 need no budget of their own: in every outer step
that reaches them, whatever its words, the solver follows one path, returns at
most one root, and steps 2 and 3 cost at most 8,936 machine units (9.8, Section
11). The final pair is formed and hashed only for a certified root, after which
the run halts, so it is formed at most once and is a collision (Lemma V). The
run halts with failure only when one of the three counts of 9.1 exceeds its
budget, which Lemma BUD bounds, or after the last outer step, which the rate
of H1' and Lemma SL cover (10.4).

**Lemma BUD (the budgets of this run, proved).** For an outer step of the run
let I_E be 1 when the mask of (2) of its omega meets S, I_2 be 1 when its mask
X is not zero (it passes the filter, Section 8), and I_3 be 1 when its T = X
AND VMASK[nu] of 9.7 is not zero; let N_E, N_2 and N_3 be the sums of I_E, I_2
and I_3 over the RUN_STEPS outer steps of step 1 of 9.1, each outer step
counted whether or not the run reaches it. Then:

- (a) I_3 <= I_2 <= I_E in every outer step, so N_3 <= N_2 <= N_E in every run.
- (b) For the outer step of the sampler, Pr(I_E = 1) <= 855/2048, and the bound
  holds under every fixing of the member y, of six of the seven chart words
  below and of every bit of the seventh except twelve.
- (c) With s = ceil(sqrt(5 * RUN_STEPS)) = 254,873,291,535 and L =
  ceil(855 * RUN_STEPS / 2048) + s = 5,423,939,209,309,911,804,868,
  Pr(N_E > L) <= exp(-2 s^2 / RUN_STEPS) <= exp(-10) < 0.0005.

So with probability above 0.9995 none of the three budgets of 9.1, all equal
to L, halts the run. The selector J is read only after the solver count of an
outer step is taken, and none of the three indicators depends on it.

Proof. (a) The masks of (1) and (2) are restricted to S (step 0 of 9.1). An
outer step passes when X, the AND of the two masks, is not zero, so the mask
of (2) meets S; and T = X AND VMASK[nu] is not zero only when X is not zero.

(b) *A second chart of the outer words.* Fix the member y. Step CO computes,
from the seven outer words (C0.d1, D2.a1, D2.b1, S11, S4, X9, w6), among
others the seven words (D2.b1, C0.b1, K1.c1, S7, K0.c1, w6, X2), written (b,
B, k1, S7, k0, f, X2) below. Every line of step CO that leads to them can be
solved backwards, which gives the outer words from these seven:

    X8 = ROL(X7,7) XOR b;          D2.c1 = ROL(b,12) XOR S7
    X13 = X8 - D2.c1;              D2.d1 = ROL(X13,8) XOR X2
    D2.a1 = X2 - b - W13;          S13 = ROL(D2.d1,16) XOR D2.a1
    S9 = k1 + S13;                 S8 = D2.c1 - D2.d1
    K0.b1 = ROR(k0 XOR IV[4],12);  S4 = ROR(K0.b1 XOR S8,7)
    K3.a1 = IV[3] + IV[7] + f;     K3.d1 = ROR(K3.a1 XOR 3,16)
    K3.c1 = IV[3] + K3.d1;         K3.b1 = ROR(IV[7] XOR K3.c1,12)
    S11 = ROL(S7,7) XOR K3.b1;     S15 = S11 - K3.c1
    S3 = ROL(S15,8) XOR K3.d1;     D3.a1 = S3 + S4
    D3.b1 = X3 - D3.a1;            D3.c1 = ROL(D3.b1,12) XOR S4
    D3.d1 = D3.c1 - S9;            X14 = ROR(D3.d1 XOR X3,8)
    X9 = D3.c1 + X14;              X4 = ROR(D3.b1 XOR X9,7)
    C0.c1 = ROL(B,12) XOR X4;      C0.d1 = C0.c1 - X8

Each line undoes one line of step CO (Section 8). Going from the outer words
to the seven and back, or from the seven to the outer words and forward,
returns the start, so at every fixed y the map is a bijection of the 2^224
points. Given b and S7, X2 -> D2.d1 -> S8 is a bijection too, so (b, S7, S8,
k0, k1, B, f) is a third chart. The outer words of an outer step are
independent uniform words (Lemma PL), so the seven chart words are independent
uniform words, also after any of them, or any of their bits, are fixed.

*The fresh byte and nibble.* Fix y, b, S7, S8, k0, k1, f and every bit of B =
C0.b1 except its bits 8 to 19: P = bits 8 to 15 (byte 1) and u = bits 16 to
19, which are then independent and uniform, P on 0 to 255 and u on 0 to 15.
Bytes are numbered from the low end. The names X8, X4, w2 = K1.a1 - IV[1] -
IV[5], S0, S5, S15 and the constant X15 are fixed: none is computed from B.
With W = ROL(y,7), step CO gives c = C0.c1 = ROL(B,12) XOR X4, h = C0.d1 =
c - X8, v = Y12 = (W XOR B) - c, R = Y0 = ROL(v,8) XOR h, C0.a1 = R - B - f and
X0 = C0.a1 - X4 - w2 = R - B - H with H = f + X4 + w2. Then D0.a1 =
ROL(X0,16) XOR Q0 with Q0 = ROL(X15,24) XOR S15, and omega = Y3 + y + w8 =
D0.a1 + C with C = Y3 + y - S0 - S5, so

    byte 0 of omega = ((byte 2 of X0) XOR q) + c'   (mod 256),

with q and c' the low bytes of Q0 and C, both fixed.

*Byte 2 of R depends on P alone and is a permutation of it.* The nibble u
enters c = ROL(B,12) XOR X4 only at bits 28 to 31, so bits 0 to 27 of c and
of h = c - X8 and bits 0 to 15 of v = (W XOR B) - c do not depend on u. Bits 0
to 19 of c read bits 20 to 31 and 0 to 7 of B and are fixed; bits 20 to 23
read P_low4, the low four bits of P, and bits 24 to 27 read its high four. So
bits 0 to 19 of h are fixed, and bits 20 to 23 depend on P_low4 alone (the
borrow into bit 20 is fixed). Byte 0 of v is fixed, and byte 1 of v is (byte 1
of W XOR P) - k modulo 256 for a fixed k (byte 1 of c and the borrow out of
byte 0 are fixed). Byte 1 of R is byte 0 of v XOR byte 1 of h, a fixed byte
R1. Byte 2 of R is r(P) = byte 1 of v XOR byte 2 of h, which does not depend
on u. A prescribed value of r(P) fixes, by its low nibble (the low nibble of
byte 2 of h is fixed), the low nibble of byte 1 of v and so P_low4; then byte
2 of h is fixed, and byte 1 of v, hence P, is fixed. So P -> r(P) is a
permutation of 0 to 255. Adding 128 to P flips bit 7 of byte 1 of W XOR P,
adds 128 to byte 1 of v modulo 256 and leaves byte 2 of h unchanged (it
depends on P_low4 only), so r(P + 128) = r(P) + 128 modulo 256 for 0 <= P <
128.

*The borrow into byte 2.* Byte 2 of X0 = R - B - H is r(P) - B2 - H2 - zeta
modulo 256, with B2 = 16 b2 + u the byte 2 of B (b2 its fixed high nibble), H2
the fixed byte 2 of H and zeta = zeta(P, u) the borrow out of the low 16 bits:

    zeta(P, u) = ceil((256 P + K - R0(P, u)) / 65536),
    K = B0 + H_low16 - 256 R1,

with B0 byte 0 of B, H_low16 the low 16 bits of H and R0(P, u) byte 0 of R,
which may depend on u. For each P the numerator lies in [256 P + K - 255, 256
P + K]. These 256 intervals are disjoint and consecutive and hold 65,536
consecutive integers in all, so the ceiling steps at most once over their
union, and at most one interval, at P = P*, contains the step inside it. So
zeta takes at most two consecutive values, zeta0 and zeta0 + 1. Put b0(P) =
zeta(P, 0) - zeta0. The numerator at u = 0 grows by at least 256 - 255 = 1
from P to P + 1, so the P with b0(P) = 1 form a suffix of 0 to 255 (possibly
empty), and zeta(P, u) - zeta0 = b0(P) for every u when P is not P*.

*The byte support of (2) for S.* For every j in S, byte 0 of sigma_j is f0,
byte 0 of DY3 is fd and byte 0 of eps is 55. The low byte of each sum in (2)_j
depends only on the low bytes, so (2)_j for omega needs a byte x with

    (a + x) XOR ((a - 3) + (x XOR f0)) = 55   (mod 256),  a = byte 0 of omega.

Write x = 16 n + i with 0 <= i <= 15, and p1 and p2 for the two sums. Then x
XOR f0 = 16 (15 - n) + i and p1 + p2 = 2 (a + i) + 237 modulo 256. With p1 XOR
p2 = 55, p1 + p2 = 85 + 2 u' where u' = p1 AND p2 has no bit of 55, so a + i =
u' - 76 modulo 128, and the low seven bits of u' are one of 0, 2, 8, 10, 32,
34, 40 and 42 (hex, the submasks of 2a), giving u' - 76 = 52, 54, 60, 62, 84,
86, 92 or 94 (decimal). With i from 0 to 15 this gives the necessary support:
byte 0 of omega lies in S8 = S7 union (S7 + 128), S7 = [25, 3e] union [45, 5e]
(hex, inclusive), 104 bytes. Necessity is all that is used.

*The count of 1,710.* Put d = 16 b2 + H2 + zeta0 and z(P) = r(P) - d modulo
256, so byte 2 of X0 is z(P) - u - (zeta(P, u) - zeta0). Let TT = {z : ((z XOR
q) + c') mod 256 is in S8}; z -> (z XOR q) + c' is a bijection, so TT has 104
elements, and TT + 128 = TT since S8 + 128 = S8. An outer step with I_E = 1
has byte 2 of X0 in TT, so the number of the 4,096 values of (P, u) for which
I_E can be 1 is at most

    C = sum over P and u of 1_TT(z(P) - u - (zeta(P, u) - zeta0)).

Let C0 be the same sum with b0(P) in place of zeta(P, u) - zeta0. With b0 = 0
everywhere it would be the sum over u of the sum over P of 1_TT(z(P) - u),
that is 16 * 104 = 1,664, since z is a permutation. For a P with b0(P) = 1 the
sum over u telescopes,

    sum (u = 0 to 15) [1_TT(z - u - 1) - 1_TT(z - u)] = 1_TT(z - 16) - 1_TT(z),

with z = z(P), so C0 = 1,664 + the sum over the suffix of D(P) = 1_TT(z(P) -
16) - 1_TT(z(P)). From r(P + 128) = r(P) + 128, D(P + 128) = D(P). For P < 128
the low seven bits of z(P) are a permutation of 0 to 127: equal low bits would
give z(P) = z(P') or z(P) = z(P') + 128 = z(P' + 128), and z is injective. So
on each of the halves 0 to 127 and 128 to 255, D takes the value
1_T7(x - 16) - 1_T7(x) once for each x in Z/128, with T7 = TT mod 128 (52
elements), and its sum over a half is 0. The suffix ends at 255: it is at
most one whole half, whose sum is 0, and one run inside a half, whose sum is at
most the number of x in Z/128 with x - 16 in T7 and x not in T7,

    B16 = |(T7 + 16) \ T7|.

C differs from C0 only at P = P*, and there only for the u from 1 to 15 at
which zeta(P*, u) - zeta0 is not b0(P*) (they agree at u = 0). With z* =
z(P*), such a u adds 1_TT(z* - u - 1) - 1_TT(z* - u) when b0(P*) = 0 and its
negative when b0(P*) = 1. So C - C0 is at most the number of k from 1 to 15
at which the indicator of T7 changes with one fixed sign between the points
z* - k and z* - k - 1: a count of transitions of one sign on the 15 edges
between the 16 consecutive points z* - 16 to z* - 1. Let E15 be the largest
such count over all z* and both signs. Then C <= 1,664 + B16 + E15. The rest
of the proof shows B16 <= 42 and E15 <= 4 for every q and c'. Only q and c'
modulo 128 matter: x is in T7 exactly when ((x XOR q) + c') mod 128 is in S7.

*B16 <= 42.* Write x = 16 j + l, q = 16 qH + qL and c' = 16 cH + cL modulo
128, with j, qH and cH from 0 to 7 and l, qL and cL from 0 to 15; put s_l =
((l XOR qL) + cL) mod 16 and k_l = floor(((l XOR qL) + cL) / 16). Then ((x XOR
q) + c') mod 128 = 16 m + s_l with m = ((j XOR qH) + cH + k_l) mod 8, and
16 m + s is in S7 exactly when m is in A_s, where, from the end points of S7,

    A_s = {3, 5} for s = 0 to 4,   A_s = {2, 3, 4, 5} for s = 5 to 14,
    A_s = {2, 4} for s = 15.

The map l -> s_l is a permutation of 0 to 15, so six columns l have two
points in A_{s_l} and ten have four. Adding 16 to x changes j by one and keeps
l, so B16 is the sum over the sixteen columns of the number of j on the
8-cycle with j - 1 in M_l and j not in M_l, M_l = {j : m in A_{s_l}}, that is
of the number of runs of M_l on the cycle. In a column the parity of m is that
of j up to one flip for all j, fixed by qH, cH and k_l. A two-point A_s has
both points of one parity, so M_l is two points of one parity, never adjacent:
2 runs. A four-point A_s has two even and two odd points, and so has M_l; four
pairwise non-adjacent points on the 8-cycle would leave four gaps of at least
2 that sum to 8, all equal to 2, and so would all have one parity; so M_l has
at most 3 runs. Hence B16 <= 6 * 2 + 10 * 3 = 42.

*Three facts on images under XOR.* On the values 0 to 15 of l, a run is a
maximal set of consecutive values, cyclically (15 next to 0) or linearly, as
stated. XOR with a fixed four-bit word maps every aligned dyadic interval
(2^i consecutive values starting at a multiple of 2^i) onto another of the
same length. (D1) A prefix or a suffix of 0 to 15 of length at most 5 is a
union of at most two aligned dyadic intervals (lengths 1, 2, 2 + 1, 4 and
4 + 1), so its image has at most two linear runs. (D2) The image of any prefix
or suffix has at most three cyclic runs: up to length 8 it is a union of at
most three aligned dyadic intervals (7 = 4 + 2 + 1 is the largest case), and
above length 8 its complement is a prefix or suffix of length below 8, and a
set that is neither empty nor everything has as many cyclic runs as its
complement. (D3) The image of a six-point interval [t0, t0 + 5] inside 0 to 15
has at most three cyclic runs, and so has the image of its complement. For t0
= 0, 2 or 3 modulo 4 the interval is a union of 4 + 2, 2 + 4 or 1 + 4 + 1
aligned intervals. For t0 = 1 modulo 4 it is three points of each of two
neighbouring aligned blocks of four, missing their local positions 0 and 3;
after the XOR the missing local positions are qL AND 3 and 3 XOR (qL AND 3),
and the two image blocks are still neighbours among the four blocks of the
16-cycle (XOR on two bits keeps the 4-cycle of the blocks). If the missing
positions are 0 and 3, each image block is one run: at most two. If they are 1
and 2, each image block is two runs with both of its end points present, and
the end points where the two neighbouring blocks meet join two of them: at
most 2 + 2 - 1 = 3.

*E15 <= 4.* The 16 points z* - 16 to z* - 1 lie in one block of 16 (the x of
one j) or in two neighbouring blocks j and j + 1 (modulo 8), a suffix of the
first in l followed by a prefix of the second. In block j put m' = ((j XOR
qH) + cH) mod 8, p = l XOR qL and e = cL; the indicator is 1 exactly when (16
m' + p + e) mod 128 is in S7, and since p + e is from 0 to 30, from the end
points of S7:

    m' = 0, 6 or 7: empty;          m' = 2 or 4: p + e >= 5;
    m' = 1: p + e >= 21;            m' = 3: p + e <= 14 or p + e >= 21;
    m' = 5: p + e <= 14.

Neighbouring blocks have values of m' of opposite parity, as in a column above
(also from j = 7 to j = 0). Case e from 0 to 4: p + e <= 19, so a block with m'
= 1 is empty; a block with m' = 2 or 4 has the zero set p < 5 - e, a prefix of
length 1 to 5, and one with m' = 3 or 5 the zero set p > 14 - e, a suffix of
length 1 to 5. In l these zero sets are their images under XOR with qL, with
at most two linear runs each (D1), and restricting to a suffix or a prefix of
the block does not add runs. So the 16 points hold at most 2 + 2 = 4 runs of
zeros (at most 3 when one of the two blocks is empty, at most 2 inside one
block). A transition from 1 to 0 begins a run of zeros and one from 0 to 1 ends
one, so either sign has at most 4 transitions. Case e from 5 to 15: p + e >= 5,
so a block with m' = 2 or 4 is all ones and one with m' = 0 or 6 all zeros:
every block with even m' is constant. A block with odd m' is empty (m' = 7),
the suffix p >= 21 - e (m' = 1), the prefix p <= 14 - e (m' = 5) or the
complement of the six-point interval [15 - e, 20 - e], which lies inside 0 to
15 (m' = 3). Its image in l has at most three cyclic runs (D2, D3), so at most
three cyclic transitions of each sign, and the transitions inside a suffix or a
prefix of the block are among them. Of the two blocks one has even m' and is
constant, and the edge where they meet adds at most one transition. So either
sign has at most 3 + 1 = 4 transitions. Hence E15 <= 4.

So C <= 1,664 + 42 + 4 = 1,710 at every fixing, and averaging over the fixings
gives (b): Pr(I_E = 1) <= 1,710 / 4,096 = 855 / 2048.

(c) The outer steps of the run are independent (Lemma PL) and each I_E is a
function of the random word of its outer step, so N_E is a sum of RUN_STEPS
independent indicators with means at most 855/2048 by (b), and E[N_E] <= 855 *
RUN_STEPS / 2048 <= L - s. For a centered indicator the logarithm of the moment
generating function f has f(0) = f'(0) = 0 and f'' <= 1/4, so f(t) <= t^2 / 8;
multiplying over the independent outer steps and applying Markov's inequality
at t = 4 s / RUN_STEPS gives Pr(N_E - E[N_E] >= s) <= exp(-2 s^2 / RUN_STEPS)
(Hoeffding). N_E > L implies N_E - E[N_E] > s, and s^2 >= 5 * RUN_STEPS, so the
probability is at most exp(-10), and exp(10) > 2,000 already from its Taylor
terms through degree 6 (their sum is above 2,866). The counts are those of the
sequence without halts; a halt cannot raise a charged count. By (a), on the
event N_E <= L also N_2 <= L and N_3 <= L. QED.

*Recounts (participant computations, not part of the proof).* An exact
enumeration of all 16,384 pairs (q, c') modulo 128 gives the largest B16 = 42,
the largest E15 = 4 and the largest B16 + E15 = 46; for the six outcomes of S
the byte support of the byte equation above is exactly S8, 104 bytes; and on
600 random fixings of the words of *The fresh byte and nibble*, the 4,096 values
of (P, u) put byte 0 of omega in S8 for at most 1,672 of them each.

*What Lemma BUD is and is not.* It is a bound on the actual chart of step CO
at every fixed member, proved by algebra, with no premise. It proves no
near-uniform law of omega or Y9, no model share (the proved 855/2048 is about
7.67 times the nominal share 233,715,456 / 2^32 = 2^-4.1998 of the lanes that
pass the automaton of (2)) and nothing about the rate of H1'. The pass and
solver budgets are taken equal to L as well, since (a) bounds them by N_E;
Section 11 charges all three rows at L + 1.

*No premise on the advice.* The only premise of this package is H1', and the
success bound rests on it and on proved lemmas alone. The values that the
search reads as advice are stated in this text (Section 12), and the success
bound is proved
for them as stated (Lemma ADV), from properties that this text checks exactly
for those values: Fact P, Lemma Q, Theorem C (iv), the table of 10.1 with the
program of Section 16, the certificate of the filter for S (Section 8) and the
verifier of 9.9. No statement of the analysis concerns the output of a
selection procedure. The search that found the values is not part of the
algorithm; it is written as the selection procedure SEL and charged in full at
its caps as preprocessing, included in T (Section 12).

**10.4 Success probability.** The probability space is the random words of the
RUN_STEPS outer steps of step 1 of 9.1, independent uniform 256-bit words made
of disjoint bits of the fresh draws (Lemma PL), for the fixed target and the
stated advice of Section 12. The algorithm is otherwise deterministic. For each
outer step let N_16 be its
certified count of Lemma SL, a function of its random word whether or not the
run reaches it. The N_16 of the outer steps are independent (Lemma PL), each is
0 or 1, and by Lemma SL and the rate of H1' each has mean

    E[N_16] = E[N_o] / 16 >= (2^21 - 1) * FACTOR / (16 * 2^128).

If the run outputs no pair, then either a budget was reached, or every outer
step was reached and none has N_16 = 1 (an outer step with N_16 = 1 that is
reached certifies a root, and the run outputs its pair, 9.1). The first event
has probability below 0.0005 by Lemma BUD, which is proved. The second has
probability at most

    (1 - E[N_16])^RUN_STEPS <= exp(-RUN_STEPS * (2^21 - 1) * FACTOR / (16 * 2^128))
                            <= exp(-lambda),

since RUN_STEPS * (2^21 - 1) * FACTOR >= lambda * 16 * 2^128 by the choice of
RUN_STEPS in 9.1 (in integers: RUN_STEPS * (2^21 - 1) * FACTOR * 25,000 >=
12,378 * 16 * 2^128). So under H1' the search outputs a collision with
probability at least

    1 - exp(-0.49512) - 0.0005 = 0.3900022368238... > 0.39

This is the union bound over the two events, which
need not be independent: the rate of H1' with Lemma SL bounds the second and
Lemma BUD the first. No allowance for dependence inside
an outer step enters. When the algorithm
outputs a pair, the pair is a genuine collision: its trial is certified, so R =
0 (Lemma V), step 3 checks both complete digests, and the messages have
different lengths. The run is the shortest of this form that gives 0.39: 0.49512
is the smallest number of five decimals for which the bound reaches it, and with
0.49511 in its place the bound is below 0.389997.

*Sensitivity to the factor.* If the valid trials are listed good trials at f *
2^-128 each on average, the run gives at least 1 - exp(-f * RUN_STEPS * (2^21 -
1) / (16 * 2^128)) - 0.0005, which reaches 0.39 only when f is at least
98,936,906,150; the assumed FACTOR is 1.0000074 times that. The margin of the
claim lies between the assumed 98,937,639,497 and the counted 138,512,695,296, a
factor of 1.40.
If the count is exact, the run has a mean of 0.6932 certified trials and the
bound is 0.4995.

H1' is not proved; Section 13 lists its evidence. Lemmas BUD and ADV are
proved and need no evidence.

## 11. Charged time

One 2-round target compression costs one unit, and every other primitive word
operation, every load and every store included, costs 1/430 of a unit. The rows
below are in operations, loads and stores, called machine units here; 430 of
them make one unit of time.

*The machine.* The search is charged on the load/store machine of 6.5, with its
256-bit words, its packed lanes, its masked rotation and its charge of one unit
for every operation, load and store, with two changes: it has 64 registers in
place of 16, and every constant is an immediate operand, written in its
instruction and not loaded. The cost model of the track charges primitive word
operations and sets no register count; this text charges as well a load for
every other word fetched from memory into a register and a store for every word
written to memory, spills included. The batch of seven outer steps runs on
packed words (9.6); the rebuild of a passing lane, the joint solver and step 3
run on scalar words of the same machine, one 32-bit value to a word. The ledger
counts of the submitted program (Section 13) are not part of the charge. The
schedules of this section are upper bounds written out by blocks, not counts of
an executed program; the only counted parts are 282 units of the batch (the 400
counted units of 9.6 without the 118 of the automaton of (2)) and the 295 of
the rebuild of a passing lane, which a participant implementation counted with
the mask of the sub-class and the filter of the seven outcomes (9.6).

**The cost, with every term.** Every row is machine units times an upper bound
on how often a run executes it; a row with a budget runs at most that many
times, plus the one that halts, because the algorithm halts with failure when a
count passes its budget (9.1). Exponents of counts and products are rounded up.

| Row | How often over a run, at most | Units | log2 of the product |
| --- | --- | ---: | ---: |
| batch of seven outer steps (9.6, 9.10): the eight random words, the lines of step CO that reach Y9 or omega on packed words, omega and the batch count (counted, 282), seven direct-table lane tests of TAB2 (41), the test of the last batch, the cursor and the dispatch (bound in words, 17), and the move that keeps the raw R_7 (1) | RUN_BATCHES = 2^70.653 | 341 | 79.067 |
| Q path of a lane whose mask of (2) meets S: the E count, its store and its test (6), then TAB1 at its Y9, the AND, the test and the branch (7) | E_BUDGET + 1 = L + 1 = 2^72.200 | 13 | 75.901 |
| passing lane: the pass count, the rebuild of its outer step on scalar words, the context of the batch, and the pre-check of 9.7 with the solver count (bound in words, 512) | PASS_BUDGET + 1 = L + 1 = 2^72.200 | 512 | 81.200 |
| outer step that reaches the solver: the slot selection and the one-path solver of 9.8 with the guards (G7) and (G15), and step 3 for its root by the tests of Lemma SC (bound in words) | SOLVER_BUDGET + 1 = L + 1 = 2^72.200 | 8,936 | 85.326 |
| once: the direct tables TAB2 and TAB1 (2^39); the static rows and descriptors (2^20); the code of Lemma SC and (G15) and the 16-slot ranges (3 * 2^20); the automata of the filter, the three transition arrays, the written-out code of the search, and the row metadata, VMASK, array bases and initialisation (2^26 each); the resident constants and the last test (40); a final failed budget test (16) | once | 550,028,443,704 | 39.001 |
| **total** | | | **85.426** |

In exact integers, with E_BUDGET = PASS_BUDGET = SOLVER_BUDGET = L, the sum of
the rows is 341 * RUN_BATCHES + 13 * (L + 1) + 512 * (L + 1) + 8,936 * (L +
1) + 2^39 + 4 * 2^20 + 4 * 2^26 + 40 + 16 = 632,899,845,872,907,123,889,774 +
70,511,209,721,028,853,463,297 + 2,777,056,875,166,674,844,092,928 +
48,468,320,774,393,371,888,309,384 + 550,028,443,704 =
51,948,788,705,154,532,738,199,087 machine units. The selection procedure SEL
is charged below and in Section 12.

*Why each budget plus one.* At most E_BUDGET lanes run the Q path, at most
PASS_BUDGET passing lanes are rebuilt and pre-checked, and at most SOLVER_BUDGET
outer steps run steps 2 and 3: in each case the next one advances its count past
the budget and halts the run before the work of its stage. Each row charges its
whole allowance for its budget plus one, which covers these and the one that
halts.

*The batch, 341*. Counted by the participant
implementation of 9.6 on the machine above, the same in every batch: the eight
random words, one operation and one AND each, 16; the lines of step CO that
reach Y9 or omega, 261; omega, 2; the advance of the batch count, its
comparison with RUN_BATCHES and the branch, 3: 282. Bound in words: seven
direct-table lane tests, each the extraction of omega from its lane, the
address of TAB2[omega], its load, the comparison of the mask with zero and the
branch, 6 units a lane and 5 for lane 0, 41; and 16 for the test of the last
batch, whose lanes 3 to 6 are not used, the cursor and the dispatch to the lanes whose
mask of (2) is not zero, with the one unit by which 9.6 rounded 423 up to 424,
17. 282 + 41 + 17 = 340; and one move that keeps the raw
R_7 in its own register before its AND with fc307cfc, for the selector of 9.8: 341. No pass bitmap and no other backup of R_0 to
R_7 is stored in the batch. Against the 425 of 9.6, the 118 units of the
automaton of (2) and the 7 base additions of its first tables are replaced by
the 41 of the lane tests; the 22 units of omega, the batch count and the
dispatch are kept in full, even where they duplicate a test. The count was made
with the mask and the seven outcomes of the sub-class; with the mask of the
class the lines and the loop are the same (9.6).

*A Q path, 13*, for each lane whose mask of (2) is
not zero: 6 for the E count, kept in a fixed memory word, with its address, its
load, the increment, the store of the new count before its comparison with
E_BUDGET, the comparison and the branch; then 7 for the extraction of the
lane's Y9, the address of TAB1[Y9], its load, the AND with the mask of (2), the
comparison with zero and the branch. A run that fails the test halts and never
resumes, and no count wraps. A lane whose mask of (2) is zero cannot pass and
does not pay it (Lemma PB). The Q path of 9.6 with the automaton of (1) costs
35.

*A passing lane, 512 outside steps 2 and 3*: the eight words taken out of lane i by a shift and an AND, and step
CO on scalar words with all the names that steps 2 and 3 read, 295, counted by
the participant implementation (9.6); 16 for reloading the eight raw words with
their addresses; 32 for the other restoration of the caller; 16 for the pass
count, its comparison with the budget, the branch and the dispatch to the next
lane; 64 for storing and reloading at most 16 words of the context of the batch
in fixed memory words around steps 2 and 3, which may use all 64 registers, at
most 4 units a word: 423; 16 for the pre-check of 9.7 with the solver count and
its test; and 6 for storing C2.c1, C2.b1 and e1 in three fixed words for the
guard (G7): 445,
charged 512. It is paid by every passing lane, also when T is empty. The counts
live in fixed memory words and are reloaded, never restored from a stale copy.

*Steps 2 and 3, 8,936.* An outer step that reaches the solver is charged by
blocks, each an upper bound on its operations, loads and stores, with addresses,
branches, spills and the restoration of registers included. The blocks are those
of the complete traversal of 9.4, with one family, one row, one node at each
position, (G15) once and at most one leaf and one root:

- 4,096 once per outer step that reaches the solver: E' = omega + DY3 and E XOR
  E', keeping the names of step CO that steps 2 and 3 read, the control and the
  record of the root.
- 2,304 for the family of the selected row (9.4): at most 128 blocks of the
  formulas of (a) to (e) of 9.4, the phase checks, (P*) and their preparation,
  at 12 units each, 1,536 (112 blocks of the formulas and 16
  more; a block is the extraction of one source bit, a majority of four
  operations, an XOR of at most five inputs, the comparison or choice of a carry
  prescription, or a carry update, with its branch and assignment); the walks of
  bits 0 to 5 under the two guesses, at most 32 units a bit, 384; and 384 for
  the record of the family, the packing of the guard planes and the dispatch.
- 1,408 for the selected row: its 32 descriptors built into 32 registers, at 32
  each, 1,024 (seven fields vary with the outer step, Q[i], y[i], E[k], E'[k],
  kappa[k], kappa[k+1] and the value of a constant, at 4 operations each, and 4
  for the static base, the shift of the key and the assignment); 128 for the
  walks of bit 6 under the two guesses (64), the patches of h[6], h[7], h[13]
  and h[26] (24), kappa and the consistency of bit 6 (8), and the dispatch of
  the row (32); 128 for the guard (G7) of 9.7; and 128 for the five row words
  of (G15) in five fixed words: the addressed loads of e1, C2.c1, C2.b1, Y1,
  w12 and Y12, at most 24; Y1 + w12, the shifts, masks and additions and the
  two carry bits alpha and v, at most 24; five addressed stores, 10; and the
  control, 16: at most 74, run in the ten temporaries before the descriptors
  are resident.
- 32 for each of the 25 positions 7 to 31 of the one path, 800. A forced node
  costs at most 20: the key from the carry pair, the descriptor and the base of
  the array, and the read, 3; the validity, its comparison and the branch, 3;
  the next carry pair and the saved bit e2[29] (at position 9 the new bit is put
  in its place), 3; the chosen bit of h, shifted to its place and ORed into the
  prefix, 3; the guard of position 25 or 29 written into the key, at most 7 (at
  25, bit 13 of the prefix shifted and masked, XORed with h[6] XOR u, which is
  held, shifted and ORed into the key, 5; at 29, the saved bit e2[29] masked,
  shifted and XORed into the key, 3); and the continuation, 1. The selected
  node at position 20 costs at most 24, with bit 8 of the prefix as the desired
  bit of the key of the selected array. A free node costs at most 28: the key
  and the read of the dual array, and at most 8 more operations to take out the
  one arc whose bit is the slot's value for the position, with its validity,
  carry pair, saved bit and prefix. No parent is saved and no second child
  restored.
- 64 for (G15) at position 15, beyond its node: the five addressed loads of the
  row words, 10; the shift, XOR, addition, XOR, shift and AND of zeta, 6; the
  addition, AND, XOR and addition of p and c_star, 4; the AND with 08b, the
  comparison and the branch, 3; the extraction of bit 8 and the patch of a
  temporary copy of the key, at most 6; copies and control, at most 16: at most
  45. It uses the ten temporaries only: the five row words, an accumulator, a
  temporary descriptor, a Boolean and control word, an address and a prefix
  temporary. The prefix, the carries, the descriptors and the static key are
  not changed, and nothing is spilled.
- 80 for the leaf: g, f, e2 and h2 of its h and (J1), (J2) and (J3) as words,
  a rotation at five operations, 64; and 16 to reload the context words.
- 120 for the root: step 3 of 9.1 by the tests of Lemma SC, with a rotation
  charged 4 (two shifts, an OR and a mask) and a mask after every modular
  addition or subtraction: Y14, Z, Y6, a1, d and c, 22; the test (Q), its AND,
  comparison and branch, 3; b, s, a, p_tau(s) and the test (A), 16; z and the
  test (C), 15; Y2, w0, t and the test (T), 17; twelve addressed loads with
  their addresses (h, e1, C2.c1, C2.b1, Y1, w12, Y12, w5, K0.d1, C2.a1, C2.d1
  and C2.b1 again), 24; the row constants tau - beta* + 8 and ROR(tau, 8), the
  dispatch, the return and the other control, 16: 113. Y11, beta*, eps, DY11,
  IV[0] + IV[4] and the row constants are immediate operands. The tests run
  inline at the leaf in the ten temporaries r0 to r9, whose leaf-test values
  are dead by then: r7 holds comparisons and control, r8 the first shift of a
  rotation and r9 an addressed load, and the values fit r0 to r6 in four
  phases. (T) runs first, with Y14 and at most four loaded or counter
  temporaries, of which only Y14 is kept. Then Y6 (r0), a1 (r1), d (r2), c
  (r3), b (r4), s (r5) and w5 or another source (r6), s formed before a
  overwrites a1; then a (r1), d (r2), c (r3), s (r5), p_tau(s) (r4) and the
  test of (A) (r0); then z (r0), c (r3), the two sums of (C) (r1, r2) and z XOR
  ROR(tau, 8) (r4). A rotation of x by r first sets r8 = x << (32 - r), then
  the destination to x >> r, then the OR and the mask, so the destination may
  be x itself when x dies; a left rotation uses the reversed shifts. A loaded
  source goes to a value register or to one whose value has died, and h is read
  without overwriting the current-state word. No traversal word is spilled, and
  a failing test touches only r0 to r9, so the traversal state is intact on
  both outcomes.
- 64 for the selection: the save and reload of the raw R_7, the extraction of
  J from bits 0, 1, 8 and 9 of lane i, the choice of the envelope from the
  mask of (1), the dispatch to the static range of the slot and the rank bits
  of its offset.

So steps 2 and 3 cost at most

    4,096 + 2,304 + 1,408 + 25 * 32 + 64 + 80 + 120 + 64 = 8,936

machine units in every outer step that reaches them, whatever its words,
whatever its T and whatever its slot. The whole allowance is charged also when
the slot is padding, its row is not in T or its path ends early. The blocks are
added whether or not they occur together, so this is an upper bound; it is not
claimed to be attained or to be the least such bound.

*Registers of steps 2 and 3*. The one-path code of 9.8 is written out
statically for each row: a prescribed position has one arc, whose code follows
that of its parent; a free position takes one arc by the bit of the offset r;
the last position jumps to the leaf check. No parent is saved. The registers
are the 32 descriptors, six context words, eight constants, array bases and
control words, two words of the current state (the prefix of h and, above bit
32, the two carries and the bit e2[29], the only earlier output bit that a
later guard reads; the guard of position 25 reads bit 13 of the prefix), ten
temporaries and the offset r: 59 of the 64. The leaf keeps the descriptors and
uses the others for its check, after which the context words are reloaded (the
16 above); (G15) and the tests of Lemma SC use the ten temporaries only,
allocated as in the blocks of 64 and 120 above. The formulas of a family run
before the descriptors are built, in at most 58 registers: at most 35 bits and
carries, five source and context words, eight table, literal and control words
and ten temporaries. No register is addressed by a value: every position and
register is named in the code.

*Once.* 2^39 for the direct tables TAB2 and TAB1 of 9.10, below 2^38 primitive
operations for both with every automaton lookup, address, store, mask and loop. 2^20 for the six static rows of the outcomes of S, the static fields of
their descriptors at the 32 positions and the metadata of the batches. 3 *
2^20 for the code of the tests of Lemma SC with its row constants, the code of
(G15) and the layout of its five row words, and the ranges of the four
envelopes with 16 slots. 2^26 for
the two automata of the filter for the seven outcomes, built and composed into
eight byte tables whose entries hold the base address of the next table, with
the entries of the last tables ANDed with S:
their states at each of the 32 bits are images of those of the fourteen-outcome
automata, at most 146, so the allowance covers them. 2^26 for the
three transition arrays of 9.4: their 2^18 entries at most 256 operations each,
the enumeration of the keys, both candidate arcs, the test for an invalid or a
second arc, the selection and the store included. 2^26 for
writing the code of the search: the one-path code of 9.8 for the six rows of
S, 25 positions each with the prescribed bit of (G7) at position 7, and the
static slot ranges of the four envelopes, far fewer than 2^14 labels, at most
256 operations each with their set-up. And 2^26 for the row metadata,
the absolute bases of the arrays and their initialisation, a fourth allowance
kept for safety, which also covers the enumeration
of the compatible patterns of 9.7 and the eight words of VMASK, below 2^23
operations. 32 for loading the resident constants and array bases
into their registers, 8 for the test of the final halt, and 16 for a final
failed budget test, kept conservatively.

*One-time items.* The items above are in the last row. The final step, once:
steps CT and CS for the trial found, writing the two messages, shorter than
2^42 bytes each, and two complete evaluations of blake3; each message has at
most 2^32 chunks of 16 compressions each and fewer than 2^32 parent
compressions, below 2^37.1 compressions for both, and writing them is below
2^38 machine units: below 2^38 units of time in all. Preprocessing: the
selection procedure SEL of Section 12, charged in full at its caps by
construction, S_old = 8,882,224,365,081,579,520 machine units, below 2^54.198
units of time.

Total:

    T <= (sum of the rows + S_old) / 430 + 2^38
      <  2^76.6771.

In exact arithmetic, with N = 51,948,788,705,154,532,738,199,087 + 430 * 2^38 +
S_old = 51,948,788,705,154,532,738,199,087 + 118,197,499,985,920 +
8,882,224,365,081,579,520 = 51,948,797,587,497,095,319,764,527 machine units,
T = N / 430 = 120,811,157,180,225,803,069,219.83... units and log2 T =
76.6770998793347...; in integers, N^10000 < 430^10000 * 2^766771 and N^10000 >=
430^10000 * 2^766770, that is T^10000 < 2^766771 and T^10000 >= 2^766770. The
submitted bound is time_log2 = 76.6771, the total rounded up at the fourth
decimal. The search part, the rows and the final step, is 2^76.6770996326...;
S_old / 430 is less than 2^-22.479 times it and adds less than 0.0000003 to
log2 T. The search part is a worst-case bound for the algorithm as stated,
which halts within its three budgets on every run and whose steps 2 and 3 are
bounded in every outer step that reaches them, and SEL is bounded by its caps.
No mean of a count of work enters T, and H1' and Lemma BUD enter only the
success probability of 10.4. The claim uses this schedule on 64 registers; the
schedule is not claimed to be the cheapest.

*Where the search part goes.* The batches are 1.22 per cent of the sum of the
rows, the Q paths 0.14 per cent, the passing lanes 5.35 per cent, the outer
steps that reach the solver 93.30 per cent and the one-time items, the direct
tables included, less than 10^-11 per cent: the three rows charged at L + 1
carry almost all of it. Per walked trial, RUN_STEPS * 2^21 of them, the sum is
0.0019067 machine units (2^-9.034); per member of Q* in L + 1 outer steps that
reach the solver it is 0.0046.

The algorithm has no sorting and no lookup by value: a root is tested against
the conditions of its outcome, and a certified trial is not compared with other
trials. It reads the direct table TAB2 at the omega of every lane of a batch and
TAB1 at the Y9 of a lane whose mask of (2) is not zero, each one load at an
address formed from the word; in a passing
outer step, the stored words of its batch and the entry VMASK[nu]; in an outer
step that reaches the solver, the raw R_7 of its lane, the three transition
arrays at the keys of the one path, the record of its family and the static row
and slot range of its outcome.
Its loads are counted: the seven loads of TAB2 in a batch are among its 41 units
of lane tests, the load of TAB1 of a Q path among its 7, and the loads of a passing
lane, of the pre-check, of the slot selection, of the one-path solver and of
step 3 are inside the allowances above.

*The ledger of the submitted program.* The submitted program (Section 13) does
not build the direct tables. It computes the two masks with the automata of
9.6, one table load per byte, and counts with the charges of the automata for
the batch and the Q path, 425 and 35 (9.6), 512 per passing lane, and per solver
step the blocks of 9.8 that it executes (Section 13). At the nominal shares a
walked outer step costs 425 / 7 + 35 * 2^-4.1998 + 512 * 2^-9.9782 + 8,936 *
2^-11.9782 = 65.341 by the program's ledger with steps 2 and 3 at the cap, and
341 / 7 + 13 * 2^-4.1998 + 512 * 2^-9.9782 + 8,936 * 2^-11.9782 = 48.714 +
0.707 + 0.508 + 2.215 = 52.144 by the rows of this section at those shares;
with every budget at L plus one, this section charges 3,998.498 per walked
outer step. The time bound uses the rows of this section and no count of the
program.

## 12. Memory, preprocessing and advice

The program of the search is the lines of steps CO, CT and CS, the outer
filter, the batch of 9.6, the one-path solver of 9.8 with its statically
written code and slot ranges, and a compression routine for step 3 and the final check: below 2^28
bytes of code and metadata (Section 11). Data, one word of 256 bits each unless
said otherwise: the 29,952 entries of the tables of the filter's two automata;
the two direct tables TAB2 and TAB1 of 9.10, 2^32 words each, 2^38 bytes;
the three transition arrays of 9.4, 2^18 words of 32 bits, 2^20 bytes; fewer
than 4,096 words for the solver (the descriptors of the positions of a row,
the six static descriptors of S, the slot ranges of the four envelopes, the
record of a family, the one root and scratch); and fewer than 1,024 words for the names of step
CO, the context of a batch, the constants and masks, VMASK, the three counts and the
cells of step 3. The memory of the search is therefore below 2^38 + 2^28 +
2^21 + 2^20 + 2^18 < 2^39 bytes. Nothing grows with the number of trials. The two
messages of a found pair have 1024 t + 55 and 1024 t + 63 bytes with t < 2^32,
each shorter than 2^42 bytes; the output, the two messages with their digests,
takes less than 2^43 bytes.

**The advice.** The algorithm of 9.1 is stated with the following fixed
values, its nonuniform advice. They are written into the algorithm and into the
submitted program, and no step of either computes or selects them.

    the six constants of 3.2: X3 = 29d4fa98, X7 = bee3af28,
      X11 = 44036000, X15 = 40c58500, W4 = 97475638, W13 = 0007c006   24 bytes
    eta = 830303cf, the class of Lemma Q                              4 bytes
    beta* = 18b0e098, with the mask 0e09818b and the value 02008000
      of its cube Q* (Theorem C (iv))                                12 bytes
    the seven values of tau from which the filter's automata are
      built, 175020a0, 185020a0, 275020a0, 285020a0, 385020a0,
      675020a0 and 685020a0, and eps = 6e21be55 (Section 8)         32 bytes
    the mask of S, 5f                                                 1 byte
    in all                                                           73 bytes

nonuniform_advice_log2_bytes = 7 covers these 73 bytes, since 73 < 2^7 = 128.
The submitted program stores no word of the sub-class or of rule A. The tables
of the filter's automata, the direct tables, VMASK, the three transition
arrays, the descriptors, the slot ranges and the traversal are not advice: step
0 of 9.1 computes them from these values, and the last row of Section 11
charges that. FACTOR, RUN_STEPS, SHARE, E_COUNT, V_COUNT, the three budgets and
RUN_BATCHES of 9.1 are not advice either: 9.1 derives them from these values by
its formulas and by the exact counts of 10.1 with Section 16, of Section 8 and
of 9.7, and that derivation is preprocessing, charged within the selection
procedure SEL below (its steps 2 and 3 compute the counts of 10.1 and of
Section 8 and the formulas of 9.1) and in the last row of Section 11 (the
enumeration of 9.7). The flags 3 and the counter rule are part of the
algorithm. There is no other stored data and no stored collision.

**Lemma ADV (the success bound holds for the stated advice).** Let the
algorithm of 9.1 run with the advice above. Under H1' (10.3) it outputs
a collision with probability at least 0.39 (10.4); every pair that it outputs is
a collision of two complete messages; and its time is at most the T of Section
11. The proofs of these statements use, of the advice, only the following
properties, each checked in this text for the displayed values:

(a) Fact P (3.2), a finite computation on the six displayed constants, and with
    it Lemma H;
(b) Lemma Q: the class of eta = 830303cf has exactly 524,288 members, given by
    the 19 free bits of e1 at fc307cfc; with (a), Theorem C (i) to (iii);
(c) Theorem C (iv): c1 gives the difference beta* = 18b0e098 exactly when c1
    AND 0e09818b = 02008000, the 2^21 words of Q*;
(d) the table of 10.1 with the counting program of Section 16, printed with its
    output: the fourteen outcomes of beta* on the class, all with eps =
    6e21be55, and the part 67,633,152 = 1,032 * 2^16 of the six of S = 5f, from
    which 9.1 derives FACTOR and RUN_STEPS;
(e) the certificate of the filter for S (Section 8): pi = 279,070,422,111 /
    2^48 and E_COUNT = 233,715,456, with Lemma F; and the allowed patterns of
    the pre-check with V_COUNT and Lemmas VP and G7 (9.7);
(f) the verifier of 9.9, printed in full and run by the participant: (PHASE)
    and (P*) for every joint root of every outcome of beta* on the class, in
    all eight phases, which Lemmas V, CV and SL use (10.2);
(g) the static rows of S, the slot ranges, (G15) with Y11 of Fact P, and the
    cap of 8,936 of 9.8 and Section 11, written for the six rows of S;
(h) the direct tables of 9.10, which step 0 builds from the automata of the
    filter, with Lemma TAB;
(i) the low bytes f0 of sigma_j for the six outcomes of S, fd of DY3 and 55 of
    eps, which give the byte support S8 of Lemma BUD (10.3).

Proof. The bound of 10.4 combines the rate of H1', whose FACTOR 9.1 derives
from (d); Lemma BUD, by (i), whose budget L 9.1 derives from (d); Lemma SL,
whose guards are exact by (e), (f), (g) and Lemma G15; Lemma PL; Lemma
TAB, by (h); and the run length of 9.1. That an output pair is a collision
follows from Lemma V, Theorem C and Lemma TR, which use (a) to (c). The time
bound of Section 11 uses (e), (g), (h), the budget L of 9.1 and the cap S_old
of SEL below, fixed numbers. Each of these statements is about the displayed
values.
None refers to what a selection procedure returns, a solver log, a recount or
any output of a search: the analysis does not use that S is least under some
charge, that these constants have the largest part among the instances of a
solver log, or that beta* is the beta of a solution of a solver. So the lemma
holds for the stated advice however it was found. QED.

**The selection procedure SEL.** The advice was found by a solver search and
one count per model, which the submitted program does not contain. This section
writes that search as a procedure, SEL, and charges its whole cost as
preprocessing, included in T (Section 11). The cost model charges any search
omitted from the submitted program; SEL is that search, and its whole capped
cost is charged. The charge is a bound by construction: every search of SEL
runs over a range stated here, and every run of a program in SEL halts as soon
as it has executed a stated number of primitive word operations, its cap, or
holds 2^34 bytes; a run that halts so returns nothing, and SEL goes on.
Operations are counted as in Section 11, 430 to the unit. SEL runs two programs
of the participant that are not in the package: the solver kissat, on instances
made by a generator of the participant, and a counter that computes in integer
arithmetic the part of one beta in the rate of the class of a given eta, with
no rule on h1, as the program of Section 16 does for beta* on the class of eta
= 830303cf; a run of the counter whose part would be 2^192 or more counts as
one that reaches its cap.

*Step 1, the pinned call (solver runs).* For each of the 116 runs of the
participant's solver log for this search (51 runs for the lengths 55 and 63,
the other 65 for nine other variants of the instance; bounds 97 to 118; logged
seeds), build the instance of the run and run kissat on it with the logged
seed, the two together with a cap of 2^56 operations. For the lengths 55 and 63
the instance is: the call C3 for both messages with equal b and d outputs, the
two words w4 related as the length cancellation prescribes for the XOR 8 of the
lengths, the top byte of word 13 zero, E1 and E3 for both messages, a zero
residual, and a bound on the number of bit positions, bit 31 excepted, at which
a difference is active in six additions of E1 and E3. A run that finds a model
returns six constants X3, X7, X11, X15, W4, W13 and the values of a solution,
among them its Y4 and its beta. Cost: at most 116 * 2^56 < 2^62.86 operations.

*Step 2, the constants, the class and beta* (a count for each model).* For each
model of step 1, compute Y3 and Y3' by C3 from its constants, its class eta =
ROR((Y3 + Y4) XOR (Y3' + Y4), 16) from the Y4 of its solution and its beta from
the c1 of its solution, and with the counter the part of that beta in the rate
of the class of that eta, with a cap of 2^52. Output the six constants, the eta
and the beta of the model with the largest part, the first in the order of the
log if parts are equal. Cost: at most 116 * (2^52 + 2^10) < 2^58.86 operations.

*Step 3, the cube, the outcomes, S and the numbers of 9.1.* With DY11 =
Y11' - Y11 for the output of step 2, form the mask ROL(beta, 12) AND
7fffffff and the value (ROL(beta, 12) - DY11) / 2 of the cube of the words
c1 that give beta (proof of Theorem C (iv)), and the outcomes (tau, eps) of
beta whose product L * N3 is not zero, which the count of step 2 lists; for
beta* these are the fourteen of 10.1. Then, for each of the 16,383 nonempty
sets S of these outcomes, compute in integers, from its count, from the
mask certificates of the two automata of its outcomes (Section 8) and from
the trees and caps of 9.4, the numerator of the exact charge of the
complete traversal under which S was chosen (10.1). Output the S with the
least numerator, the first in increasing order of its mask if two are
equal, the outcomes whose tau has bit 14 equal to 0, from which the outer
filter's automata are built, and, for that S, the numbers of 9.1 by its
formulas. Step 3 and the bookkeeping of SEL run under a cap of 2^50
operations.

**The bound.** Steps 1 to 3 cost at most

    S_old = 116 * 2^56 + 116 * (2^52 + 2^10) + 2^50 = 8,882,224,365,081,579,520

operations, below 2^62.946 (in integers S_old^1000 < 2^62946), and so below
2^(62.946 - 8.748) < 2^54.198 units (S_old^1000 < 430^1000 * 2^54198). The
whole of S_old is in T (Section 11). It bounds SEL as defined, whatever the two
programs do inside and whatever they return, because every run halts at its cap
and every loop has the range stated. SEL is not a premise of this package, and
no heuristic is declared for it. preprocessing_log2 = 55 bounds SEL with the
once-only work of step 0, rounded up to a whole number: (S_old +
550,028,443,704) / 430 = 2^54.19743396... units, and in integers (S_old +
550,028,443,704)^1000 < 430^1000 * 2^54198.

*What rests on records.* The bound rests on no record. That SEL returns exactly
the six constants of 3.2, eta = 830303cf, beta* = 18b0e098 and S = 5f rests on
the participant's records: for S, on the participant's exact comparison of the
16,383 sets in integers, without and with the guard (G7) (10.1); for the rest,
on the participant's solver log, by which the run for the lengths 55 and 63
with bound 104 and seed 506 found these constants after 4,770 seconds, with a
solution of class 830303cf and beta 18b0e098, and on an exact integer recount,
by the participant's counter on the whole class of each instance, of all 65
distinct instances that the runs of the log returned with a model, in which
these constants have the part 71,698,432, the largest, and the next is
13,107,200 (a strict maximum, 5.47 times the next); every model was replayed on
32-bit words. Every run of the log stopped within 9,010.5 seconds on one
processor core and every recount within 320 seconds; at 2^42 operations a
second for a core, a rate the participant states and does not prove, every run
stayed below 2^55.14 operations and every recount below 2^50.33, inside the
caps. The log does not fix every instance: some runs excluded pairs that runs
finished before them had found, and 32 runs were stopped from outside without a
record of the cause. So the records certify a historical run of the solver, not
a replay with operation caps, and the generator of the instances, the solver
log and the counter are not in the package; no organizer experiment runs them.
If a record were wrong, SEL could return other constants or none; its cost
would stay within the bound.

*Memory of SEL.* Every program run of SEL halts when it holds 2^34 bytes, and
SEL runs one program at a time; its own data stay below 2^20 bytes, the parts
of step 2 and the outputs. SEL therefore holds fewer than 2^34 + 2^20 bytes at
any time; the search fewer than 2^39 bytes, its direct tables included; the
advice 73 bytes; the output fewer than 2^43 bytes. Held at once, these total
below 2^43 + 2^39 + 2^35 + 2^7 < 2^44: memory_log2_bytes = 44 bounds all. The
measurements of Section 13 on real and on scaled-down messages are not part of
SEL: they test the heuristic H1' and select nothing, and neither their work nor
their memory is in these figures. The cost model does not score memory.

## 13. Evidence, scope and field meanings

Throughout this text costs and bounds are rounded up, and margins, rooms and the
whole numbers of the count that the claim uses are rounded down. Counts printed
with decimals are rounded to the nearest.

**What is exact.** Sections 2 to 5, 7 and 8; Lemmas L, H, Q, Q2, T, T2, T4, N,
A, TR, CT, IP, F, J0, PL, PB, V, SC, VP, G7, G15, CV, SL, TAB, BUD and ADV
and Theorem C; the count
of passing pairs of Section 8 and the allowed patterns of the pre-check (9.7);
(PHASE) and the parity certificate (P*), exact counts, certified in all eight
phases by the verifier of 9.9; the slot ranges of 9.8; the constants and caps of
the solver (9.4, 9.8) with its schedule (Section 11), as upper bounds; and
Lemmas S1 to S5 and S9 under their stated hypotheses. Lemma A says
what stage A tests, not that a collision passes it. The declared experiment
`half-collision` runs the search of 9.1 on the root instance for 1,792 outer
steps per organizer seed and returns a pair built by steps CO and CT at
counter word 0, and the organizer recomputes both digests; every such pair
agrees on the 128 masked digest bits (*The submitted program*, below). The
counter instance has no organizer-run check (6.4).

*Who wrote and who checked the exact part.* The exact part was written by the
AI models of Section 15. The participant's checks of it are computations, not
proofs, each reported where it belongs: the counter construction against the
organizer's own functions on 2,000 trials, with 204,000 internal words compared
with a separately written forward computation, and complete messages hashed by
the organizer's code (Section 7); the automata of the filter against brute
force (*The submitted program*, below); all 2^21 members of Q*, each giving the
difference beta*, and the rule t != 0 (Section 8); the paths of the 16 slots
against the complete traversal on the same trials (*The submitted program*,
below); the free positions, static trees, families and caps of the solver and
the cells of (P*) against the counts of 10.1 (9.4); the run of the verifier of
9.9; the integers of Section 11; the batch (9.6); the word nu of the pre-check
on 324,098 real trials (9.7); and the submitted program (*The submitted
program*, below). For Sections 1 to 6, three independent reruns, by a checking
agent, a reviewing agent and a participant tool that reads the printed text,
found no wrong value in the displays, Table C and Lemmas Q, Q2, L, A, T2 and
T4, and Lemma A was checked by complete enumeration in three ways. These are
checks, not proofs, and no person has read any part of this text.

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
The search of this package makes the clustering inside an outer step
irrelevant to its success bound: it certifies at most one trial per outer step,
with mean exactly 1/16 of the mean count (Lemma SL).

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

**The count (participant computation).** The count runs over the 60 words beta
that have a part in the rate of the whole class: of the 133,742 words that
occur as beta, the 4,550 with k at most 14 were enumerated, and for the 129,192
others a SAT solver was asked whether the whole system has a solution with that
beta and answered no for 129,147, without certificates; an exact integer
enumeration over every beta finds the same 60. For the whole class the rate is
85074516985129/524288 = 162,266,763.66, from 60 betas and 453 outcomes with a
nonzero product. For the sub-class of the root instance it is r =
194382080300609/1048576 = 185,377,197.55, from 53 betas and 317 outcomes, about
2^27.47 and 1.142 times the rate of the class, so that under M a trial of the
sub-class has R = 0 with probability about 2^-100.53; with rule A it is r_A =
6219586146887739/33554432 = 185,358,111.47, so the rule loses about one part in
10,000 (of the 317 outcomes, 99 have only solutions that satisfy it, 76 none
and 142 both; the sum over the 99 is 185,355,453.45). On the whole class the
same eight conditions keep 76,072,772.68, less than half: the rule belongs to
the sub-class. The heaviest beta, beta* = 18b0e098, has 7 outcomes and the part
67,698,688 in r, the same with rule A (10.1), 36.5% of r; the four heaviest
carry 98.8%, so the count rests on few paths. The claim of this package uses
only the part of beta* on the class (10.1, Section 16).

**Checks of the counter (participant computations).** (1) Complete enumeration
with 8-bit words of every quadruple (Y4, h1, Y9, w8) through both executions of
E3 and every triple of the E1 side, over random constants, classes, sub-classes
with up to three more fixed bits of e1 and rules with parities of three bits:
five runs, 1,472,040 and 5,332,992 integers, none different from the counter.
(2) At 32 bits two functions compute the E3 side with its split by the rule and
agree on all 687 outcomes both counted; the other 285 (16 with a nonzero
product) were counted by one alone. The E1 count agrees with a separate
calculator on 972 of 972 outcomes. (3) That calculator, untouched, with an
option of its own for a sub-class, finished 54 of the 60 betas in the time
allowed, each equal to the participant's part at its one printed decimal; the
six unfinished carry a share of 1.8 * 10^-9 of r. (4) For the whole class, a
helper agent counted both factors of all 453 outcomes with two programs written
from the definitions of 6.2 and 6.3 alone: the same total,
85074516985129/524288, and the same parts for 60 of 60 betas.

**How the constants and the class were found** is told in Section 12: they come
from a SAT solver search, beta* is the beta of the solver's solution, and they
were chosen by the count, as were the sub-class and the rule. The analysis uses
none of this history (Lemma ADV).

**Real messages in the root arrangement.** Earlier participant measurements in
the arrangement of Sections 4 to 6 (counter 0, flags 11); they bear on the
seven-word model M, on which the counter rate rests as well, and on rule A, not
on the counter search or its budgets. Rule A is satisfied by 2^-8.0019,
2^-7.9992 and 2^-8.0000 of three runs of 2^30 real trials and by 2^-8.000002 of
2^44.59 trials of the sub-class on a graphics card; the share of batches that
enter stage 2 is about 0.0262, against 0.0270 for independent trials, with
single contexts between 0.0071 and 0.0421. Layout runs of the two-level
arrangement on the whole class (24 outer tuples of 2^40 trials, two runs of
2^44 and others, recounted by a second helper agent) agree with the model on
average within their statistical error at every level, from the rules at 2^-4
to 2^-6 to the listed E1 outcome at 2^-40.15 (138 seen against 152.0); 24 runs
of 2^45 real trials in a second triangular order of the construction agree at
every level (listed E1 outcomes 692 against 690.78). What these runs do not
support, and what this text must not claim, is independence of the trials
inside one outer step: the share of the trials of one value of X2 that satisfy
a rule is not binomial (for five conditions its variance is 2.7 to 181 times
the binomial one), the members of a batch pass together, and the rate of a
listed tau given a listed beta is a property of the outer tuple, between 0.02
and 2 times its average for 17 cells that carry 24% of the count, because Y12
and w5 are fixed inside an outer step. One count is unexplained: in one window
of 2^44 trials of one tuple, 3 listed E1 outcomes were seen where 14.65 were
expected (probability 0.0003 under a Poisson law); the next window has 16.
Single outer steps of the sub-class differ from the average over outer steps by
about plus or minus 8.48 per cent in the model's weighted rate, while the claim
uses the average.

*Scaled-down end-to-end runs in the root arrangement.* The whole search of this
pair of lengths was run on small versions of the hash, with 8-bit and 10-bit
words, every trial hashed completely, against the number of solutions of the
seven-word system by complete enumeration. In the job whose expected values and
rule of judgement were written down before it ran, 8,448 runs found 8,108
collisions against 8,313.6 predicted (-2.25 standard deviations): 6,276 against
6,489.6 with 8-bit words (3.3 per cent low, -2.65) and 1,832 against 1,824.0
with 10-bit words (+0.19), with no failed check and no false collision; by that
rule only a deviation of more than 3 standard deviations below the prediction
would speak against the model, and the cause of the shortfall at 8 bits is not
known (the first 92 runs, the first job, were low as well, 56 against 74.8). In
a second triangular order of the construction, 1,272 runs found 345 collisions
against 335.76 (+0.50). With a sub-cube that keeps a quarter of the members and
an eight-condition rule on an eight-bit hash, 30 runs found 121 collisions
against 120.23 (z +0.07; six runs planned in advance, 24 declared after the
first result): selection by a sub-cube condition on e1 and by a rule on h1
leaves the collision rate of the survivors at the exact per-trial count, to
within 9 per cent, but at eight bits no rule keeps almost all of the collision
mass, so the kept mass of rule A stays a counting claim. These runs have no
counter, no filter and no packed batch of this search.

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
error is larger because these events cluster by outer step (whole class 0.971
+- 0.028); each of the four residual words zero 1.019, 1.009, 0.984 and 0.990,
each +- 0.006 to 0.021. In the arrangement of Sections 4 to 6 the same events
of beta* are rarer by the factor of the prescription: c1 lies in Q* with
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
are 3.9 to 31.8 on the eight sets, against 853.61 here), and it has no rule A,
no sub-class and no packed batch.

**Real messages in passing outer steps.** A participant measurement made for
this package, untrusted evidence like the two paragraphs before it, which the
organizer's harness does not run. On a graphics card a helper agent ran the
counter construction on real 32-bit messages with Y4 in the sub-class. Uniform
random outer steps, drawn by the measuring program, were filtered by conditions
(1) and (2) with the tables of the automata of Section 8 for the seven outcomes
j = 1 to 7, and every passing outer step enumerated the whole of Q*, all 2^21
values of c1 in the member order of Section 8, as 299,594 words of seven lanes:
2^22.00 passing outer steps, 2^43.00 trials. A control with the filter off ran
2^18 outer steps, 2^39 trials. On 330 records a check against a participant
scalar implementation (step CO, the filter, the member order, rule A and the
word n of the E1 test from the compression of the real last chunks) found no
difference. Errors are taken per outer step, because the trials of one outer
step cluster.

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
most one per outer step. These measurements bear on the rate of H1' inside
passing outer steps; they reach no event deeper than about 2^-31.7 and no
collision.

**Real counter trials on the whole class.** A participant measurement made for
the class, untrusted evidence like the paragraphs before it, which the
organizer's harness does not run. On a graphics card a helper agent ran the
counter construction on real 32-bit messages in two classes of one build: the
whole class of eta (all 2^19 members, no rule, the filter of the fourteen
outcomes of beta*), and as a control the sub-class of 6.1 with rule A and the
seven-outcome filter. Each run walked 2^35 uniform random outer steps and
enumerated all of Q* in 2^25 of its passing outer steps, 2^46 trials per class;
the passing steps kept are the first in the order of the card's atomic counter,
which does not depend on their content, and the pass share uses every walked
step. Before the runs, the filter tables were compared with the construction of
Section 8, 1,000 members of each class with the member lists, and a sweep of
all 2^32 values of tau and of eps at beta* showed that the counters list
exactly the fourteen and the seven outcomes of 10.1; no trial lacked the
difference beta*. The counters are the E1 outcome and the filter; errors are
clustered by outer step. The model per trial is the sum of L_j over the listed
outcomes times 2^-85 (2^-96 for the triples times 2^11 for c1 in Q*).

| Event | Exact model | Measured | z |
| --- | --- | --- | --- |
| E1 outcome among the seven j = 1 to 7, whole class | 53 * 2^-38 = 2^-32.2721 per trial | 2^-32.2692 (13,595 events), 1.0020 +- 0.0086 of the model | +0.23 |
| the same, sub-class control | 2^-32.2721 | 2^-32.2540 (13,739 events), 1.0126 +- 0.0086 | +1.46 |
| ratio whole class / sub-class, the seven | 1 | 0.9895 +- 0.0120 | -0.87 |
| E1 outcome among all fourteen, whole class | 79.5 * 2^-38 = 2^-31.6871 | 2^-31.6888 (20,328 events), 0.9988 +- 0.0070 | -0.17 |
| share of the seven new outcomes among the fourteen, whole class | 1/3 | 0.3312 +- 0.0033 | -0.64 |
| fourteen-outcome filter passes, whole class | 2^-7.5320 (exact) | 2^-7.5321, 0.99990 +- 0.00007 | -1.38 |
| seven-outcome filter passes, sub-class control | 2^-9.8132 (exact) | 2^-9.8130, 1.00012 +- 0.00016 | +0.74 |

Every measured quantity matches the exact model within 1.5 clustered standard
errors, and the clustered error of each E1 rate equals its Poisson value: no
excess clustering of E1 outcomes by outer step. For this package the first row
is the one that bears on the rate: the E1 rate of the seven outcomes j = 1 to
7, with members drawn from the whole class and no rule, in trials of passing
outer steps of the fourteen-outcome filter, which contain every passing outer
step of the filter for S (Lemma F); it equals the rate of the same seven
outcomes on the sub-class with rule A, as the model says. The counter covered
the seven outcomes together: the E1 event of S, six of them, is a sub-event of
the measured event, with model rate 52 * 2^-38 per trial, 52/53 of it, and it
was not counted on its own. The run has no counter of the E3 side and none of
the joint event: the E3 count of these outcomes on the class (N3_j four times
that of the sub-class, 10.1) and the joint event of H1', about 2^-91 per trial,
are not measured, and the seven-outcome filter was run only in the sub-class
control. These measurements bear on H1'; they reach no collision.

**The submitted program (experiments/halfsearch.py).** The program of the two
declared experiments is one Python 3 file of 60,753 bytes that uses only
the standard library and imports no BLAKE3 library. It runs the search of 9.1 on
the root instance only: one chunk, counter 0 and flags 11, the instance that the
organizer's harness hashes. It does not run the counter instance (flags 3,
counter t), on which the claim is made. Step 2 runs by the 16-slot selection of
9.8 with (G15) by default, in both organizer modes and in the self-test; the
option `--no-slot16` runs the complete traversal of 9.4 instead, and the
declared experiments do not use it.

*One trial.* Per organizer seed the program runs 256 batches, 1,792 outer
steps, whose eight words come from SHAKE-256 of the text "halfsearch batch",
the seed and the batch number. In order: (1) step 1 of 9.1: the whole-class
sampler; step CO compiled from its lines onto packed words of seven 36-bit
lanes; the automaton of (2) on omega in all seven lanes, then the automaton of
(1) on Y9 (the Q path), with masks restricted to S; an outer step passes when X
is not zero; the E, pass and solver counts against the budgets the program
holds (9.1), which a trial never reaches. (2) The pre-check of 9.7: nu by (V),
then T = X AND VMASK[nu]. (3) Step 2 by 9.8: J from bits 0, 1, 8 and 9 of
the raw eighth word, kept before its AND with fc307cfc; the envelope of m1, the
first of the four sets of 9.8 that contains it; the row and the offset of slot
J in the static ranges of 9.8. A padding slot, or a row not in T, ends the
outer step with no root. Otherwise the row is set up with the guards (a) to
(g) of 9.4, (G7), the walks of bits 0 to 6 and the five row words of (G15), and
one path is followed from the first state at depth 7: a prescribed position
takes its one arc, with Lemma J0 at position 20 and the guards at positions 25
and 29; at position 15, (G15) computes c_star from the prefix, ends the path
when c_star AND 08b is not zero, and otherwise takes the forced arc of bit 8 of
c_star; and the n-th position of F' takes one of the two arcs of its dual entry
by bit n of the offset. At depth 32, (J1) to (J3) are checked as words. So a
solver step returns at most one root. (4) Step 3 for every root: c1 by the
inverse of Lemma IP, then the tests in this order: c1 in Q*, the counter word t
= 0 of this instance, the names of steps CO and CT equal to the 2-round
compression, (J1) to (J3) equal to E3 on A and B, the E1 differences, and equal
chaining values (here, equal digests). It evaluates the compressions, where the
charged schedule uses the equivalent tests of Lemma SC. A root is counted as
certified only when every test holds.

*The ledger.* The program counts machine units with the charges of its ledger
in Section 11 (*The ledger of the submitted program*), those of the automata:
425 per batch (the counted 424 of the packed batch and the move that keeps the
raw word), 35 per lane whose mask of (2) meets S, 512 per passing lane; per
solver step 4,096 and 64 for the selection; 2,304 and 1,408 when a row is set
up, which contain the walks of bits 0 to 6 as in 9.8; 20 per forced node, the
node at position 15 included, 64 more for (G15), 24 at the selected node, 28
per free node taking one arc, 9 and 4 more at the guard nodes 25 and 29, 1 per
arc kept at position 9, 80 per leaf and 120 per root. So a solver step counts
at most

    4,096 + 64 + 2,304 + 1,408 + 22 * 20 + 3 * 28 + 4 + 9 + 4 + 1 + 64 + 80 + 120
    = 8,678.

These are the program's counts of what it executes, node by node. The time bound of Section 11 does not use them: it
charges the whole 8,936 on every outer step that
reaches the solver, whether or not a row is set up, and 341 per batch and 13
per Q path for the direct tables of 9.10, which the program does not build.

*The returned pair.* The pair of a trial comes from its first passing outer
step, or from its first outer step if none passes. Step CT is run with the one
c1 for which the counter word that step CT forces is 0, from Lemma IP: K0.a1 =
ROL(K0.d1, 16), w0 = K0.a1 - IV[0] - IV[4], Y2 = w0 + C2.a1 + C2.b1, Y14 =
ROR(Y2 XOR C2.d1, 8), E3.h1 = ROR(Y14 XOR (Y3 + y), 16), and c1 by the inverse
of Lemma IP. The program asserts that step CT then gives t = 0. The pair is a
55-byte A and a 63-byte B, built from the lines of steps CO and CT, not by the
compression. At counter 0 and flags 11 the counter, v[13], the flags and the
block length difference are as in the proof of Theorem C (ii), with 0 and 11
in place of t and 3, and the colliding compression is the root, so its output
words are the digest words: every such pair agrees on digest words 0, 2, 5 and
7. The program checks on every root, and the self-test on every case, that the
names of steps CO and CT equal those of the compression. In `residual-search`,
after the trial, the seven outer words are kept and the members of the class of
Lemma Q are taken in order from the member of that outer step, at most 131,072
of them; each gives an outer step by step CO and a pair at t = 0, and the
search stops at the first pair whose residual has a zero low byte in digest
word 1, 136 bits in all. Its observation `member_units` counts that loop at one
unit per 32-bit word operation and 3 per rotation: 1,002 per member tried, 3
per next member from the second, and 1 for the first, computed from tries.

*The self-test.* `python3 experiments/halfsearch.py --selftest 256 7` ran in
about 2 seconds and exited with 0: the constants of 9.1 that the program holds;
the automata against brute force at width 8, 256 of 256; SHARE and E_COUNT from
the program's tables; an envelope of 9.8 for every mask of (1); the packed batch
against the scalar step CO on 16,380 lanes, 0 failures and no lane above 36
bits; 424 units per packed batch; the mask of (1) against the (J1) mask, step
CT against the compression, the inverse of Lemma IP, the J words against E3,
the c1 with t = 0, and the half-collision at counter 0 and flags 11, each 256
of 256; and (G15) on 65,536 words h: when both carries of h with bit 15 cleared
equal alpha and v, the low nine bits of c_star equal those of its c1, in 15,286
of 15,286 such words; and every h with Z[22] = 0, Z[23] = 1 and c1 AND 18b = 0,
what Lemma G15 uses of a success, passes (G15) with its own bit 15, in 485 of
485.

*Other participant checks of the program.* A participant script, not part of
the package, ran the program's own functions on 7,340,032 trials of the
half-collision experiment, 3,260,898 solver steps, and in every solver step
both the complete traversal of 9.4 and the 16 slots with (G15). The complete
traversal reached 329,364 leaves and 90 joint roots. The 16 slots reached
20,446 leaves, each a leaf of the complete traversal and each in exactly one
slot, and these are exactly the leaves of the complete traversal whose prefix
passes (G15) with their own bit 15; no slot reached any other leaf. One of the
90 joint roots passes (G15); exactly one slot returned it, and the complete
traversal returns it too; no slot returned any other root, and none of the 90
is certified. Every row of T lay in its envelope. The last 6,291,456 of these
trials ran with a version of the file that differed only in charging the walks
of bits 0 to 6 a second time, which changes no leaf, root or slot; with the
file as submitted, the largest solver step on the first 1,048,576 trials cost
8,558 units by the program's ledger, below 8,678. A second participant
script checked Lemma SC with the program's step CT and compressions on 20,000
random outer steps with c1 in Q*: the words of h gave its c1, the test (Q) and
its counter word t in 20,000 of 20,000; with tau and eps set to the actual a
and c differences of E1 where that tau is even with bit 31 zero (17,428 cases),
(A) and (C) held in every case, and with one bit of tau or of eps changed they
failed in every case.

*The runs of this package.* Both declared experiments were run locally as the
organizer runs them: one execution answers 256 organizer-style trials, twice per
experiment, under the limits of the sandbox (timeout 20 s with start-up, one
CPU, 128 MB of address space; Python 3.14). Every returned pair was hashed with
the organizer's own 2-round BLAKE3 function, and the two executions of each
experiment gave identical output.

| 256 seeds, slot of 9.8 | half-collision | residual-search |
| --- | ---: | ---: |
| pairs returned / event met / failed | 256 / 256 / 0 | 256 / 256 / 0 |
| time of one execution of 256 trials, two runs | 0.85 s, 0.98 s | 2.31 s, 2.42 s |
| largest resident memory | 28 MB | 28 MB |
| outer steps, 256 trials of 1,792 | 458,752 | 458,752 |
| passing outer steps (share; exact 0.00099146) | 496 (0.0010812) | 441 (0.0009613) |
| solver steps per pass (nominal 1/4) | 0.2339 | 0.2698 |
| solver steps / of them with a row set up | 116 / 53 | 119 / 48 |
| solver units per solver step, mean / max (cap 8,936) | 5,861 / 8,133 | 5,667 / 8,309 |
| units per outer step, outer part (ledger 63.126) | 63.199 | 63.110 |
| units per outer step, steps 2 and 3 (2.215 at the cap) | 1.482 | 1.470 |
| units per outer step, trial (ledger 65.341) | 64.681 | 64.580 |
| member loop per outer step | - | 204.433 |
| members tried, mean (least, most) | - | 364.5 (1, 2,463) |
| over cap, halts | 0, 0 | 0, 0 |
| roots / past Q* and t = 0 / certified | 0 / 0 / 0 | 0 / 0 / 0 |

The ledger figures per walked outer step are those of the program's ledger
(Section 11) at the nominal shares: 425 / 7 = 60.714 for the batch, 35 *
2^-4.1998 = 1.905 for the Q path and 512 * 2^-9.9782 = 0.508 for the pass,
63.126 together, and 8,936 * 2^-11.9782 = 2.215 for steps 2 and 3 at the cap,
65.341 in all. The rows that Section 11 charges, with the direct tables, give
52.144 at the nominal shares and, with every budget at L plus one, 3,998.498
per walked outer step. The measured outer part agrees with the ledger; steps 2
and 3 use
about 66 per cent of their allowance on average (5,861 / 8,936), and no solver
step exceeded the cap, the largest at 93 per cent of it.

*The limitation of the root instance, stated plainly.* On counter 0 and flags
11 a joint root of step 2 gives c1 by the inverse of Lemma IP, and step CT then
forces the counter word t = ROL(K0.d1, 16) XOR K0.a1. Once the outer step and
c1 are fixed, t is fixed, and no free word is left to set it; the harness
hashes counter 0, so a root of this instance is a collision only if that t is
0. If t were uniform, about 2^-32 of the certified roots would have it; that is
an assumption, not a measurement. No root has reached the test t = 0 in these
runs. The returned pairs are therefore not output of the attack: they are
half-collisions of 128 bits (136 in `residual-search`) on the outer steps of
the search with the c1 that makes t = 0, which is in general not the c1 of a
joint root and does not meet the E1 and E3 conditions of a full collision. The
experiments show that the program's steps CO and CT give real messages that
hash as this text says on the harness instance, and they record the program's
counts of the search on that instance. They do not show that the search finds
a collision on either instance, and they measure neither the factor of H1' nor
the half-collision of the counter instance. No certified root exists, so the
test of equal digests has never held on a real root. All counts are the
program's own; the organizer records them as untrusted and does not recompute
them.

**Scope.** No full collision is exhibited; this is an analytical cost claim
that tests each trial against zero and needs no memory that grows with the
trials. The messages have 1024 t + 55 and 1024 t + 63 bytes, with 1 <= t < 2^32
the solved chunk counter; the colliding compression is that of the last chunk,
which is not the root, and Lemma TR carries the collision to the complete
digests in the profile's own tree mode. No priority or novelty claim is made.

**Field meanings.**

- time_log2 = 76.6771: the total of Section 11, log2 T = 76.6770998793347...,
  checked in integers (T^10000 < 2^766771); the search part, worst case for the
  algorithm as stated, is below 2^76.67710 units, and the selection procedure
  SEL, charged in full at its caps, below 2^54.198 units (Section 12).
- memory_log2_bytes = 44: the search with its code and the direct tables (below
  2^39 bytes), the advice (73 bytes), the output (below 2^43 bytes) and
  every run of the selection procedure SEL (below 2^35 bytes), even all held at
  once (Section 12).
- preprocessing_log2 = 55: the selection procedure SEL of Section 12, charged
  in full at its caps, S_old = 8,882,224,365,081,579,520 operations, with the
  once-only work of step 0 of 9.1 and the direct tables: (S_old +
  550,028,443,704) / 430 = 2^54.19743396... units, below 2^55 (in integers,
  (S_old + 550,028,443,704)^1000 < 430^1000 * 2^54198). Every search of SEL
  runs over a stated range and every program run in it halts at a stated cap,
  so this is a bound by construction, with no premise; that SEL returns exactly
  the stored values rests on the participant's records (Section 12).
- nonuniform_advice_log2_bytes = 7: the advice of Section 12, 73 bytes, below
  128 bytes; the slot ranges and the direct tables are computed from the advice
  and are not advice.
- success_probability = 0.39: under the rate of H1', for the stated advice
  (Lemma ADV, 10.4), 1 - exp(-0.49512) - 0.0005 = 0.3900022..., where 0.0005
  bounds a proved tail of the budgets (Lemma BUD), with no dependence clause
  (Lemma SL).
- heuristics: H1prime-rate (score-critical, the mean rate only), and no other:
  the budgets are proved (Lemma BUD), and the charge of SEL holds by
  construction.

The required baseline_improved identifier blake3-r2-nominal-v2 names the
organizer's nominal display reference 128, not an established attack, qualified
baseline or security bound; 76.6771 is below it. Whether a qualified result
improves the Yukon incumbent is decided separately; no Pareto dominance claim
follows.

## 14. Earlier entries

Earlier entries on this track whose parts this package uses, one line each:

- 17bba2ae (123.5), 5ceb1802 (121.5), 04638ed8 (112.4), c47c1a80 (99.4): the half-collision, the class search and the two tests.
- c66f230d (97.6) and 64c075ac (92.53): the root instance of Sections 1 to 6 with the sub-class and rule A.
- e7b17fd1: the counter construction of Section 8 with Lemmas TR, CT, IP and Theorem C.
- 26ebba63 (71.39): the outer filter, the joint roots and the walk over independent outer steps, on the sub-class with rule A.
- 59f8915e: the whole class with no rule, the guards (PHASE), (P*) and Lemma J0, the lanes of Lemmas PL and PB, and the selection procedure SEL with its cap S_old.
- 0bc5f130 (66.8751): S, the pre-check, (G7) and the complete traversal, with a dependence clause.
- 78ac164c (71.7481): this search with 32 slots and a declared selection-return premise.

## 15. Credit

- GPT Sol 6.1 (OpenAI), an AI model run by the participant: the 16-slot selection with (G15) and Lemma G15, the certificate of Lemma SC and the charge 8,936; Lemma BUD, the bound 855/2048 on the three counts; the earlier slot repair, the joint solver, its guards and caps, the filter, the pre-check, (G7), the lanes and the direct tables; Lemmas IP, F, S1 to S5, S9 and SL and the verifier of 9.9.
- The participant who filed entry dd91b2f6: dropping the sub-class and rule A in the solver design, and the fourteen outcomes of beta* on the class.
- winglock: searching a sub-class of members chosen by an exact count per member (entry 18a7fc52).
- Th0rgal: the values of the member built once per outer step (entry df8bd46d), and three coding steps of 6.5 (entry 8c81a219).
- 5kyguy: masks kept in registers across the loop over the members (entry 404d14df).
- tekkac: the seven 36-bit lanes with a masked rotation of 6.5 and 9.6 (public ticket 2bf40fb).
- GordoAR: the margin 1.4 between the counted rate and the assumed factor.
- Subflatus3 and leech1996: a budget just above its mean, here s above the bound of Lemma BUD.
- Grok 4.7 (xAI), an AI model run by the participant: the hostile review of entry c66f230d.
- Helper agents of the participant, instances of the author's AI model: the searches, counts, programs, checks and runs of this package, and this text.

## 16. The counting program for 67,633,152

The program below computes the part of beta* = 18b0e098 in the rate of the
class of eta (Section 10.1), outcome by outcome, in exact integer arithmetic,
with the standard library only: every tau (taus), both roots eps (eps_roots),
the E1 count L_j (L_count) and the E3 count N3_j (N3_count), each as an exact
carry count over all bit positions, with Y4 over all 524,288 members of the
class (Lemma Q) and no rule on h1. Nothing is sampled, capped or delegated to a
solver. Run as `python3 -B count.py`, it printed the outcome table below in
about 2.5 minutes (Python 3.14). Its column L*N3/2^81 is four times the last
column of the table of 10.1; its column "rule A" is the count with the empty
rule and equals N3 in every row. Its self-test, a brute force at width 6 that
follows the listing in the file, ran 12 seeds with no mismatch. The program
prints all fourteen outcomes of beta* on the class and their sum; this package
lists the six outcomes of S, and only their rows are shown below, in the
program's order. They sum to 270,532,608 = 4 * 67,633,152 on the program's
scale 2^81, that is 67,633,152 on the scale 2^83 of a trial with Y4 uniform in
the class (10.1). The eight rows that are left out, 675020a0 and the seven with
tau ending in 5060a0, sum to 16,261,120 = 4 * 4,065,280 and are listed, with
their L_j and N3_j, in the table of 10.1; the sum and check lines of the
program, which follow the rows, are those of all fourteen.

```python
#!/usr/bin/env python3
# Exact count of the part of beta* in the rate of the WHOLE class of eta, no rule filter.
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

**End of Section 16.**
