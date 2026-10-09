# A last-chunk half-collision and a chunk-counter search for 2-round BLAKE3

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
separately reported resource bound.

This exploratory package targets blake3-r2-prefix-v1. It has an exact part and a
heuristic part, and it keeps them apart. It refiles the search of our entry
78ac164c (71.7481), restructured after its review so that the score does not
depend on what a selection procedure returns (Section 15, labelled history).
It is the search of our entry 0bc5f130
(Section 15), the counter search of entries e7b17fd1 (84.98) and 26ebba63
(71.39) run on the whole class of eta with no sub-class and no rule A, with one
change, GPT Sol's (answer BA 1.3 and 1.4): in an outer step that reaches the
solver, the search no longer returns every success of the outer step. Five
fresh selector bits, taken from the outer step's own random word at bits that
nothing else reads, name one of 32 static slots, and the solver follows the one
path of that slot and certifies at most one trial (9.8). Every success of an
outer step has exactly one slot, so the number of trials certified in an outer
step is 0 or 1, its mean is exactly the mean number of successes of the outer
step divided by 32, and the success bound needs no premise on how the successes
of one outer step cluster (Lemma SL, 10.2, and 10.4). This is the design of
entry 0bc5f130 made premise-light at a higher price: that entry declared, inside
its rate premise, a bound on the factorial ratio rho of the successes of one
outer step, and this package removes that clause and pays for it with a run
about 32 times as long (Section 15). The outcome set S is six of the seven outcomes of
beta* whose tau ends in 5020a0, namely 175020a0, 185020a0, 275020a0, 285020a0,
385020a0 and 685020a0 (675020a0 is dropped); an exact s-pattern pre-check, a
test of three bits that the outer step fixes, runs before the solver and skips
it in about three passing outer steps out of four without losing any success
(9.7); an early guard on E1, (G7), fixes one more bit of the solver's word
before its path starts (9.7); and the outer steps run in lean lanes, which run
the second automaton of the filter in every lane and the first only in a lane
that the second passes (9.6). The exact filter (Section 8) skips every outer
step that cannot hold a success with an outcome of S. The eight other outcomes
of beta* on the class are not searched. The premises of the success bound are
two: H1' as a rate only, with no dependence clause, and H4' with its budget
clauses, restated for the run of this package (10.3). The six constants, eta,
beta*, the outcomes of the filter and S are stated in this text as fixed
nonuniform advice of 73 bytes (Section 12): the success bound holds for these
stated values however they were found (Lemma ADV), and all computation that
found them, which the submitted program omits, is charged as preprocessing at
P = 2^70 primitive word operations, 2^70 / 430 = 2^61.25181 units, included in
the time bound. That P covers that computation is a third heuristic, HPRE,
declared as supporting (10.3): a bound from the peak rates of the participant's
attested devices over a window of 30 days, which enters only the preprocessing
term of the time bound. Dropping the sub-class and rule A is the
step of entry dd91b2f6 of another participant (Section 16). The solver reads
its guards from exact certificates of the class: the phase equations (PHASE)
and the parity certificate (P*), both certified in all eight phases by an exact
verifier that the participant ran (9.9), and a guard on the third addition of
E3, Lemma J0. It has a proved cap of 8,912 machine units, with (G7), in every
outer step that reaches it (9.8); the outer steps are drawn seven to a batch of
eight fresh 256-bit words, as independent outer steps with the law of one drawn
alone (9.6); and every budget is charged at its bound on a machine with 64
registers and constants as immediate operands (Section 11). The layout of the
solver, its cap, the slot selection, the pre-check, the guard (G7), the lean
lanes and the schedule on 64 registers are GPT Sol's (answers AL, AO, AQ, AR,
AT, AW, AX and BA) and are proved upper allowances, not an implementation of
that schedule. The submitted program runs the logic of this search, the
slot selection and the one-path solver included, on the root instance only,
with counts taken from the ledger of Section 11 (Section 13, *The submitted
program*); it does not run the 64-register schedule (9.5). The
package continues entry 64c075ac (92.53) of the same participant with the same
block lengths and six constants, without the clusters of that entry. Section 14
corrects the text of entry c66f230d, Section 15 says what is the same as entries
64c075ac, e7b17fd1, 26ebba63, 59f8915e and 0bc5f130 and what is new, with the
labelled history of entries 78ac164c and 0bc5f130, and Section 16 credits the
people and models whose work is used.

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

**Heuristic part.** A collision needs the other four words of the chaining value
to agree as well. The algorithm draws 25,984,157,895,075,365,790,188 = 2^74.460
outer steps at random, seven to a batch, 2^21 trials each. An exact filter, two
carry automata on two words of the outer step, skips every outer step that
cannot hold a collision with an outcome of S (Lemma F); it passes 2^-9.9782 of
uniform pairs of words. The second automaton runs in every lane, and the first
only in a lane whose word passes the second, 2^-4.1998 of uniform words. In a
passing outer step three bits of E1.b1 that every success shares are a function
of the words of the outer step, and they allow an outcome of S for only two of
their eight values: the pre-check skips the solver in the other passing outer
steps, exactly and without loss (Lemma VP); two more of these bits fix one more
bit of the internal word before the solver starts (Lemma G7). The solver walks
the bits of one internal word under guards that exact counts of the class prove
lossless (9.4, 9.9). Its trees have at most 32 leaves in an outer step, and the
search gives each leaf position a static slot from 0 to 31; five selector bits
of the outer step's random word name one slot, the solver follows that one path,
and a certificate maps its leaf back to its trial and tests it. Every success of
the outer step owns exactly one slot, so the outer step certifies a success
with probability exactly its number of successes divided by 32, at a cost of at
most 9,459 machine units for a passing outer step whatever its words (Sections
9 and 11, Lemmas V, VP, G7, CV and SL). Every budget is a halt and is charged at
its bound; no mean of any count enters the time bound. Three heuristics are
declared. Two bear on success: H1', that the valid trials (t not zero) complete
the collision with an outcome of S at a mean rate of at least 98,937,639,497 *
2^-128 = 2^-91.474,
five sevenths of the model's rate for this prescription and these outcomes
rounded down, with no clause on how successes cluster; and H4', that the three
budgets of the run suffice: of lanes whose word passes the second automaton, of
passing outer steps and of outer steps that reach the solver (10.3). Under these
two the search succeeds with probability at least 0.39, for the stated advice
(Lemma ADV, Section 12). The search is charged below 2^71.74802
target-compression units. The construction of the advice, all computation of
the participant that found it, is charged as preprocessing at P = 2^70
primitive word operations, 2^70 / 430 = 2^61.25181 units. The third heuristic,
HPRE (supporting), is that this computation is at most 2^70 charged word
operations: the peak rates of the devices that the participant attests, over
a window of 30 days, give below 2^69.740 (Section 12). The total,
2^71.74901350..., is below 2^71.7491: the claimed scalar is 71.7491. The
search needs less than 2^29 bytes of memory; its two messages are shorter than
2^42 bytes each, and the declared 2^44 bytes cover them, the code, the advice,
the search and the recorded memory of the construction, even all held at once
(Section 12).

The rate in H1' is an assumption. Under the seven-word model of Section 13, with
Y4 uniform in the class, prescribing c1 in Q* multiplies by 2^11 the part of
beta* in the rate of the class: counting the six outcomes of S, the rate is
2^11 * 67,633,152 = 138,512,695,296 times 2^-128, which is 853.61 times the
model rate of a trial of the class, and the conditioning leaves the law of the
other call, E3, unchanged (Lemma S1, proved by another AI model, GPT Sol 6.1).
The figure 67,633,152 is the sum of six exact outcome counts of the
participant's counting program, printed with its output in Section 17. Whether
the trials of the construction realise that conditional law, to at least 5/7 of
its rate, is the part that is not proved, and it is declared as H1' for the
whole class and S; Lemmas S2 to S4 prove parts of it. How the successes of one
outer step depend on each other does not enter: the slot selection makes the
certified count of an outer step 0 or 1 with an exact mean (Lemma SL). Participant measurements on
real counter trials reach events of probability about 2^-31.7 and agree with the
model, among them the E1 rate on the whole class of the seven outcomes of entry
59f8915e, of which the event of S is a part (52/53 of it in the model), and a
scaled-down end-to-end run with real collisions of complete messages realises
the predicted gain of the prescription at 0.94 +- 0.13 of its value (Section
13). No run reaches a collision at 32 bits. With the uniform rate, and not
98,937,639,497 times it, the same search needs about 2^131.986 walked trials and
gives time_log2 = 108.28.

No full 2-round collision is exhibited, and the search is far beyond feasible
computation. The two declared experiments run the root instance of the same
construction: single chunks of 55 and 63 bytes, compressed with counter 0 and
flags 11 (Sections 4 to 6). An organizer experiment tests an event on the two
complete digests, and the half-collision of the counter instance lies in the
chaining value of a chunk that is not the root, which the parent and root
compressions above it mix: no digest experiment can show it (Section 6.4). What
the experiments exhibit, and what the organizer's runner checks, is the exact
half-collision of the root instance, on a pair built by the steps CO and CT of
this search, and a short search of 8 more digest bits over the class.
The program the organizer runs is new in this package. Per organizer seed it
runs the search of 9.1 on the root instance (counter 0, flags 11) for 1,792
outer steps: the whole-class sampler, the packed batch of seven outer steps,
the exact outer filter for S, the pre-check of 9.7, the slot selection and the
one-path solver of 9.8 with the guards of 9.4 and (G7), step 3 for every root,
and a count of every row by the ledger of Section 11. Its counts and its
self-test are the program's own, which the organizer does not check. It does
not run the counter instance, and on the root instance a root is a collision
only when its forced counter word is 0 (Section 13). The share of the filter
for S, the factor, the run length, the three budgets and the charge of the
search of this package are defined in this text (Sections 8, 9 and 11); the
layout of the solver, the slot selection, the pre-check, the guard (G7) and the
schedule on 64 registers are proved allowances, and the program does not run
that schedule.

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
C0.a1. Arithmetic is modulo 2^32. The earlier program (6.5) has steps O and M in
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
Lemmas L and H, the class, Lemma N and the machine of 6.5; the sub-class, rule
A and Lemma A belong to the root instance and to the earlier program's counter batch
(9.2), not to the counter search of this package. The instances differ in the
counter and the flags that the compression reads, and in the order in which the
construction solves the assignments of rounds 0 and 1 (Sections 4 and 8).

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
is a collision only when its forced counter word is 0 (Section 13). Until this
package the two experiments of the same ids ran the earlier program of 6.5.

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

*The count in the earlier program.* The program filed as
experiments/halfsearch.py with entries 26ebba63, 59f8915e and 0bc5f130, called
*the earlier program* in this text, is not part of this package: the program of
this package replaced it and is described in Section 13 (*The submitted
program*). Where Sections 6 to 13 name a function `ctr_...` or report a check
or a count of *the program* or its self-test, they mean the earlier program,
unless they name the submitted program. The earlier program contains the four pieces, the counter
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
root instance the earlier program keeps unchanged, 1,000,000 cases with seed 61,
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

In the experiment `residual-search` of those entries the earlier program evaluates, per
organizer seed, one outer step, the table words of one list word, one middle
step and one batch, for that seed's context and the list position of the first
member tried, and returns the operations and loads of the two stages of the
batch, its number of right lanes and whether a lane satisfied rule A as
observations. The organizer's runner records observations as untrusted and does
not recompute them. The self-test and these observations therefore showed what
the earlier program counted, and that its lanes agree with its own compression
of the real messages. They are a participant check, not an
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
member y of the class of 6.1 (Lemma Q), which becomes the value of Y4; and the
*inner word* c1, which becomes the third value of E1 on message A. The constants are
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

**The outer filter.** Number the seven outcomes of beta* whose tau ends in 5020a0
(10.1) j = 1 to 7 in the order of the table of 10.1: 175020a0, 185020a0, 275020a0,
285020a0, 385020a0, 675020a0 and 685020a0, the seven of entry 26ebba63 and of the
program's `CTR_TAUS`. This search lists six of them, the set S = {1, 2, 3, 4, 5,
7}: all but 675020a0 (j = 6). In the hexadecimal masks below, with bit j - 1 for
outcome j, S is 5f. Beta* has seven more outcomes on the class, the same seven with
bit 14 of tau set (j = 8 to 14 of 10.1); this search does not list them either.
Let tau_j be the tau of outcome j, sigma_j = tau_j XOR ROR(tau_j, 1) and theta_j =
ROL(sigma_j, 12); all seven have eps = 6e21be55. For an outer step put omega = Y3 +
y + w8, with Y3 of Fact P, y the member of the outer step and w8 the name of step
CO; DY3 = Y3' - Y3 = fdb77cfd is that of Section 6. For a word x:

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
2^-9.813176, the share of the filter of entry 26ebba63 and the earlier program's
`CTR_SHARE`; this search does not use it. Let pi_E be the share of the 2^32
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
arithmetic on the table; GPT Sol's answer AW 3 gives the same 279,070,422,111
and 233,715,456). With the seven other outcomes of beta* on the class added, GPT
Sol's certificate of the fourteen-outcome filter (answer AN 2) gives
99,669,577,442,459,648 passing pairs, 2^-7.531997; that filter is not used here.

*The automata.* The program's `ctr_automaton` builds the subset construction
above as four byte tables: a state is the carry of x + DY3 (zero for (1)) and,
per outcome, the set of reachable carry pairs, four bits; the table of byte p
maps a state and byte p of x to the next state, and the table of the last byte
maps to the mask. `ctr_tables` builds the two automata once per run from
`CTR_TAUS` and `CTR_EPS`, which in the earlier program hold the seven outcomes
of entry 26ebba63. The search of this package builds the same two automata (step
0 of 9.1) and ANDs every entry of their last tables with 5f once, so that every
mask it reads is restricted to S; the states and the number of table loads do
not change. The program's construction has 1, 18, 43, 37 and 1, 3, 7, 7 states
at the four byte boundaries and tables of 25,344 and 4,608 entries (a
participant run of the program's own functions). `ctr_look` runs an automaton on
a word with one table load per byte, and `ctr_filter` returns the AND of the
mask of Y9 under (1) and the mask of omega under (2); the program's outer step
passes when it is not zero. The program's count of passing pairs from its own
tables is `CTR_SHARE` = 20,504,986,129,465,344, for the seven outcomes, which
the self-test of 9.3 recounts, and it checks those automata against brute force.

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
ceil(lambda * 32 * 2^128 / (FACTOR * (2^21 - 1))) =
25,984,157,895,075,365,790,188, about 2^74.460, with lambda = 0.49512 = 12378 /
25000, so that the expected number of outer steps of a run that certify a trial
is at least lambda at the rate of H1' (Lemma SL, 10.4; GPT Sol, answer BA 1.4);
SHARE = 18,289,159,183,466,496,
the number of pairs that pass the filter for S (Section 8), so that its share pi
is SHARE / 2^64; E_COUNT = 233,715,456, the number of words that pass the
automaton of (2) for S (Section 8); V_COUNT = 558,140,844,222 = 2 * SHARE /
2^16, the count of the pre-check of 9.7 over 2^51 (GPT Sol, answer AW 3); three
budgets, each the expected count of its outer steps in a run under the nominal
shares of H4' times the margin 17/16, rounded up (GPT Sol, answer AW 3):

    E_BUDGET      = ceil(17 * RUN_STEPS * E_COUNT / 2^36)
                  = 1,502,329,371,444,650,570,489,  about 2^70.348;
    PASS_BUDGET   = ceil(17 * RUN_STEPS * SHARE / 2^68)
                  = 27,372,319,633,926,710,491,     about 2^64.570;
    SOLVER_BUDGET = ceil(17 * RUN_STEPS * V_COUNT / 2^55)
                  = 6,843,079,908,481,677,623,      about 2^62.570;

and RUN_BATCHES = ceil(RUN_STEPS / 7) = 3,712,022,556,439,337,970,027, about
2^71.653, the number of batches of seven outer steps (9.6). The submitted
program (Section 13) holds FACTOR, SHARE, E_COUNT and V_COUNT as above, but
the run length of entry 0bc5f130, RUN_STEPS = 814,694,561,164,316,144,946
(lambda = 12419 / 25000, without the factor 32), and the budgets and
RUN_BATCHES computed from it by the same formulas; its self-test checks those
values. A trial of the program walks 1,792 outer steps and reaches none of
its budgets, so these constants do not change what it returns.

0. Before the batches, build the two automata of the outer filter for the seven
   outcomes, with the entries of their last tables ANDed with S (Section 8), the
   table VMASK of the pre-check (9.7), and the three transition arrays, the
   static row descriptors of the six outcomes of S, the static slot ranges of
   9.8 and the statically written one-path code of the solver (9.4, 9.8,
   Section 11). None depends on an outer word.
1. For each of the RUN_BATCHES batches in turn, b = 0, 1, ..: draw eight fresh
   uniform 256-bit words R_0 to R_7. Lane i, for i = 0 to 6, is bits 36 i to 36
   i + 35 of a word (9.6). Lane i of batch b holds the outer step of number 7
   b + i if that number is below RUN_STEPS, which holds for all seven lanes
   except in the last batch, whose lane 6 is not used. The *random word*
   of that outer step is the 256-bit word whose k-th 32-bit word, for k = 0 to
   7, is the low 32 bits of lane i of R_k. Its first seven 32-bit words are the
   outer words C0.d1, D2.a1, D2.b1, S11, S4, X9 and w6. Its eighth word W gives
   the member y with e1 = Y3 + y = 030c0303 + (W AND fc307cfc), that is the
   member of the class whose 19 free bits of e1 (Lemma Q) are the bits of W at
   the same positions; its member number (Section 8) is these 19 bits in
   increasing order of position. W also gives the *selector* J = W[0] + 2 W[1] +
   4 W[8] + 8 W[9] + 16 W[15], a number from 0 to 31, from five of the 13 bits
   of W outside fc307cfc (9.8); the raw word R_7 is kept before its AND with
   fc307cfc for this. *Test (2):* run in all lanes at once on packed
   words (9.6) the lines of step CO that reach Y9 or omega, omega = Y3 + y + w8,
   and the automaton of (2) on omega, whose mask is restricted to S. A lane
   whose mask of (2) is zero ends its outer step there. *Q path:* then for each
   lane whose mask of (2) is not zero, in increasing order of i: advance the
   count of such lanes, the *E count*, and halt with failure when it exceeds
   E_BUDGET; else run the automaton of (1) on the Y9 of the lane and AND its
   mask with that of (2), giving the mask X of the outer step. If X is zero the
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
   the common state of 9.4 to its leaf. It returns at most one root h, with the
   outcome j of its row (9.8).
3. *Certificate:* for the returned root h, if there is one, with its outcome j:
   compute c1 from h by the inverse of Lemma IP, Y14 = ROL(h,16) XOR (Y3 + y),
   Y6 = ROR((Y14 + C2.c1) XOR C2.b1, 7), E1.a1 = Y6 + Y1 + w12 and c1 = Y11 +
   ROR(E1.a1 XOR Y12, 16); drop the root if c1 is not in Q*, that is if c1 AND
   0e09818b is not 02008000; compute Y2, w0, K0.a1 and t by the lines of step
   CT, and drop the root if t = 0; evaluate E1 on A and on B (6.2) for this c1,
   and drop the root unless the XOR differences between A and B of their a
   outputs and of their c outputs are tau_j and eps = 6e21be55 (their
   first-half b difference is beta*, by Theorem C (iv)). A root that is not
   dropped is *certified*. For a certified root, form F || A and F || B by
   steps CT and CS for its c1, evaluate blake3 of both in full, check that the
   two digests agree, output the pair and halt. A dropped root, or no root,
   ends the outer step; the slot is not drawn again.
4. After the last batch, halt with failure.

The run halts with failure in exactly four ways, each a test on a count that the
algorithm keeps: the E count exceeds E_BUDGET, the count of passing outer steps
exceeds PASS_BUDGET, the solver count exceeds SOLVER_BUDGET, or the outer steps
are exhausted. So at most E_BUDGET lanes run the automaton of (1), at most
PASS_BUDGET passing outer steps are rebuilt and pre-checked, and at most
SOLVER_BUDGET outer steps run steps 2 and 3, which have no budget of their own:
the solver follows one path and returns at most one root, and the work of steps
2 and 3 is bounded in every outer step that reaches them, whatever its words
(9.8, Section 11). So the work of every run is bounded by the counts of Section
11, and a pair of messages is formed and hashed at most once, for a certified
root.

A trial is *valid* when its t is not zero; a valid trial with R = 0 is *good*; a
good trial is *listed* when its E1 outcome is in S (Section 8, 10.1). Each
listed good trial of an outer step owns one slot from 0 to 31, and distinct
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
bits of the eighth word and the selector J from its bits 0, 1, 8, 9 and 15;
step CO compiled from its lines onto packed words of seven 36-bit lanes; the
two automata with their last tables restricted to S, (2) in every lane and (1)
on the Q path; the E, pass and solver counts against the budgets it holds
(above); the pre-check of 9.7; the slot selection and the one path of 9.8 on
the static rows of 9.4, with the guards (a) to (g), (G7), Lemma J0 and the
guards at positions 25 and 29; and step 3 for every root. Its steps CO and CT
read counter 0 and flags 11, so its trials are trials of the root instance,
where a root of step 2 is certified only when the counter word that step CT
forces is 0 (Section 13). It counts each row with the units of Section 11 as a
ledger on Python integers; it does not run the 64-register schedule of Section
11, so its counts are not counts of that machine (9.5).

*What the earlier program holds.* The earlier program (6.5) is the earlier
version of this search, on the sub-class. It contains steps CO and CT (`ctr_outer`, `ctr_trial`), the outer filter (`ctr_tables`,
`ctr_look`, `ctr_filter`) and the walk over outer steps (`ctr_run`) of the
sub-class search of that entry, one outer step at a time on scalar words: its
member is the member of the sub-class of 6.1 of a number taken modulo 2^17, its
filter has the seven outcomes of `CTR_TAUS`, and its constants are those of that
search: `CTR_MEMBERS` = 2^21, `CTR_FACTOR` = 99,033,509,302, `RUN_OUTER_STEPS` =
813,905,892,669,542,263,145, `CTR_SHARE` = 20,504,986,129,465,344 and
`CTR_PASS_BUDGET` = 961,264,466,727,415,003. Its two automata are those of the
search of this section, which restricts their last tables to S; its outcome
list, its share and its constants are those of the seven outcomes and are not
those of this search. For each outer step it is given, `ctr_run` runs step CO
and the filter; a failing outer step is skipped; a passing one advances the pass
count, the walk halts with failure when that count exceeds CTR_PASS_BUDGET, and
otherwise it runs the function of the outer step that `ctr_run` is given. Its
counted form `ctr_count` charges one walked outer step on a machine with scalar
words and 16 registers (9.3); the charge of Section 11 does not use that count.
The search of this section differs from it in the member (the class, from the 19
free bits of the eighth word), the outcome set S and with it the share, the
factor, the run length and the pass budget, the E count and the solver count
with their budgets, the batch of seven outer steps in lean lanes (9.6), the
pre-check and the guard (G7) (9.7), the selector J and the one-path solver
(9.8) and the charge (Section 11). The earlier program also holds the counted enumeration of all of Q* that a
passing outer step ran in the version of this search that the joint solver
replaces, and its self-test checks it (9.3): `CTR_WORDS` = 299,594, the packed
words of seven lanes that hold the members of Q*, of which the last holds member
2^21 - 1 in all seven lanes (7 * 299,594 = 2^21 + 6); the run-wide table of the
packed words RT[j], whose lane i holds ROL(E1.d1, 16), and DT[j], whose lane i
holds E1.d1 = c1 - Y11, for c1 the member min(7 j + i, 2^21 - 1) of Q*
(`ctr_table_word`); the words that a passing outer step stores for it, each in
all seven lanes (`ctr_memory`): Y12, -Y1 - w12, C2.b1, -C2.c1, w5, w5 + delta,
the word v of Lemma A (c) for y, and beta*; and the counter batch of 9.2
(`ctr_batch`) with its two end tests: the part "loop" compares the advanced
table position with the word `end of list`, which holds CTR_WORDS, and the part
"entry count" compares the advanced number of stage-2 entries with the word
`stage-2 budget`, which holds STAGE_2_BUDGET = floor(CTR_PASS_BUDGET * CTR_WORDS
/ 32) = 8,999,658,332,647,911,575,274, called E. The search of this section runs
none of these; 9.2 and 9.3 describe them as the earlier program and its
self-test hold them.

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

**9.3 The counter part of the self-test.** This subsection reports the
self-test of the earlier program (6.5), as filed with entry 26ebba63; the
self-test of the submitted program is described in Section 13. The earlier
program's command `python3 experiments/halfsearch.py --selftest N [seed]` of 6.5 also runs N cases of the
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
counted outer steps right, and the counts used in Section 11: 467 units for the
outer step (348 operations, 119 loads), 41 for the filter (24 operations, 17
loads) and 4 for the pass count (3 operations, 1 load).

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

This subsection defines the joint roots, the guards, the transition arrays and
the static trees of the solver, and the complete depth-first traversal over
them, which returns every joint root of the searched outcomes; that traversal
was the solver of entry 0bc5f130. The search of this package does not run the
complete traversal: it runs the one-path form of 9.8, which follows the single
path of one slot through the same trees, with the same arrays and guards.

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
that drops members or solutions. (PHASE) is also certified pointwise, for every
joint root of the fourteen outcomes in all eight phases, by the exact verifier
of 9.9, which the participant ran: its count of joint roots that violate
(PHASE) or (P*) is zero in every phase and on every row.

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
of all eight phases, for all fourteen rows, were recomputed by the exact
verifier of 9.9 (GPT Sol, answer BA 2), which the participant ran: it asserts a
zero count of wrong guards and the counts of this table in every phase, and it
printed "all eight phases: exact guards and counts certified". The count shows as well that a new row has no joint root when u =
v, and a new row 175, 275 or 675 none when b = 0; the search of this package
lists no new row.

*The guard on the third addition (GPT Sol, answer AR 6.1).*

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
32 leaves and 32 roots, whatever its words (GPT Sol, answers AT 1, AW 2 and AX
1.1).

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
restriction of that solver to the seven outcomes, the four sets of rows and their
counts, and the cap of 37,032 are GPT Sol's answer AT 1; its restriction to S,
with the same cap, is answer AW 2; and the guard (G7), the trees without the free
position 7 and the cap of 31,456 for S (row sets 17,120, 12,416, 27,840 and
31,456) are answer AX 1: the same solver, visiting only the outcomes of T, with
the same proofs and one more guard; an outcome outside S is not counted as a
success, and no listed good trial of an outcome of S is lost. The participant
recomputed the free positions from those of answer AO 6.2 and the new guards, the
node, leaf and selected counts of the table and of the four sets (for the fourteen
rows, for the seven and for S, with and without (G7)), the
families, the bits of the fourteen outcomes that Lemma J0 reads, and the sums
of the parity certificate against the counts of 10.1, and ran the verifier of
9.9, which certifies (PHASE) and (P*) for every joint root of the fourteen
outcomes in all eight phases; the other constants and guards were not
re-derived by the participant. At positions 25 and 29 the
guard selects the candidate before the table read, as in GPT Sol's corrected
answer AR 6.3: these positions are not prescribed by the carries (gamma[i] = 0
and D[k] = 0 there, on the old rows for position 25 and on every row for
position 29), so the value of the guard is written into the key before the
read, within the same allowance (Section 11). Lemma CV (10.2) states what the
complete traversal returns, and Lemma SL (10.2) what the one-path form of 9.8
certifies. The layout is specified and charged by this text; it is not an
implementation (9.5).

**9.5 Checks of the joint solver.** The solver of 9.4 and 9.8 for the class,
in the layout of 9.4 and 9.8 and with the schedule of Section 11 on 64
registers, has not been implemented, and neither have the slot selection of
9.8, the lean lanes of 9.6 or the pre-check and the guard (G7) of 9.7 in that
schedule. The submitted program runs their logic on the root instance, with
counts taken from the ledger of Section 11, and its measured counts are
reported in Section 13 (*The submitted program*); it is a participant
implementation in Python, not the schedule, and its runs are short: the
completeness of the solver's paths rests on the proofs cited in 9.4, on the
count of the class and on the guard certificate of 9.9, which was run, and its
cap of 8,912 machine units on the schedule of 9.8 and Section 11, an upper
allowance written out by blocks and not a count of an executed program; the
pre-check rests on Lemma VP, whose bit identity was checked on real trials
(9.7). For
entry 26ebba63 a participant implementation of the solver of that entry, with
rule A, the seven outcomes and a traversal per carry guess, was compared with an
earlier solver on 332,000 passing outer steps of real walks and on 8,400 planted
instances, with the same roots in every step and every planted root found, and
no step exceeded the bound of that entry. Those checks concern other guards and
are reported only as context; the organizer runs none of them.

**9.6 Seven outer steps in one word (GPT Sol, answer AQ).** The batch of step 1
of 9.1 runs on packed 256-bit words with the seven 36-bit lanes of 6.5: lane i
is bits 36 i to 36 i + 35 of a word, and it holds a 32-bit value in its low 32
bits with four guard bits above them. The conventions are those of 6.5 and of
Lemma CB (d). The low 32 bits of a lane are the scalar value modulo 2^32, and
every lane of every sum stays below 2^36, so that no carry leaves its lane;
where an interval bound of a sum could reach 2^36, an AND with the word M that
has the low 32 bits of every lane set is made first, and charged. x - z is
formed as x + (z XOR M) + 1, never by a packed subtraction, whose borrows could
cross lanes. A rotation by r is PROR: ((x >> r) AND A_r) OR ((x << (32 - r))
AND B_r), five operations, with A_r and B_r the masks of its two parts in every
lane. The addition of a constant is kept pending until the value is read by an
XOR, an OR, a shift, a rotation or a table index, and the one addition that
then forms it is charged. All interval bounds depend on the lines and the
constants only, not on the words.

*What a batch computes.* Each of R_0 to R_7 is drawn and ANDed with M, except
R_7, which is first copied to one more register as drawn (the raw word, from
which a passing lane takes its selector J, 9.8) and then ANDed with the word
that has the bits of fc307cfc set in every lane; lane i of R_k is then the k-th
word of the random word of lane i. The
lines of step CO, the program's `ctr_outer`, run on the packed words, with y =
(W AND fc307cfc) + (030c0303 - Y3), a pending constant addition, in place of the
program's deposit of a member number, and without the lines whose values reach
neither Y9 nor omega = Y3 + y + w8. Then omega, and in each lane i the automaton
of (2) on omega, for the seven outcomes with its last table restricted to S: for
each byte of the lane a shift by 36 i plus eight times the byte's position, an
AND with 255, the addition of the state from the second byte on, and one table
load; then the test of its mask against zero and the branch. The automaton of
(1) does not run in the batch. *The lean lanes (GPT Sol, answer AT 4).* The
lanes whose mask of (2) is not zero are taken at once, in increasing order of i,
each by its *Q path*: the E count and its test (9.1), then the automaton of (1)
on the Y9 of that lane, four bytes taken out by a shift and an AND, three state
additions and four table loads, the AND with the mask of (2), its test and the
branch. A lane whose mask X is not zero is then a passing lane and is processed
at once (below). No pass bitmap is formed and no backup of R_0 to R_7 is stored
in the batch.

**Lemma PL (the lanes are independent ordinary outer steps).** (a) The random
words of the RUN_STEPS outer steps of a run are independent and uniform on the
2^256 words, and the algorithm reads no other bit of R_0 to R_7: the guard
bits, bits 252 to 255 and the lane 6 of the last batch are not used. (b)
The seven outer words, the member and the selector J of an outer step are
independent; the outer words are uniform words, the member is uniform on the
class, as when the eighth word modulo 2^19 is the member number (Section 8),
and J is uniform on 0 to 31. (c) So the outer steps of a run are independent
and identically distributed, and each has the law of an outer step that draws
its own uniform 256-bit word: every count of an outer step, among them the
count N_o of H1', the certified count N_32 of Lemma SL and the indicators of
H4', has the law that it has for such an outer step. The algorithm is a
function of the RUN_STEPS random words, the probability space of 10.4.

Proof. (a) The low 32 bits of lane i of R_k are a set of bit positions of R_k,
and these sets are disjoint for different lanes; different k and different
batches are different draws. So the random words of different outer steps are
made of disjoint sets of the independent uniform bits of the draws, and they
are independent and uniform. The batch reads R_k only through its AND with M or
with the word of fc307cfc, and through bits 0, 1, 8, 9 and 15 of each lane of
the raw R_7, which a passing lane reads for its own lane only; a passing lane
reads only its own lane of the stored words; so no other bit is read. (b) The
bits of 030c0303 and of fc307cfc are disjoint, so the addition is an OR: e1 has
the value 030c0303 at the 13 positions of 03cf8303 and the bits of W at the
other 19, so y = e1 - Y3 is the member of the class (Lemma Q) whose number is
the 19 bits of W at the free positions (Section 8). For a uniform W this number
is uniform on 0 to 2^19 - 1, as W modulo 2^19 is, and it is a function of the
19 bits of W at fc307cfc alone. J is a function of bits 0, 1, 8, 9 and 15 of W,
which lie outside fc307cfc (03cf8303 has them set), so J is uniform on 0 to 31
and independent of the member and of the seven outer words, which are other
bits of the draws (GPT Sol, answer BA 1.3). (c) An
outer step and everything computed from it are functions of its random word
only, so (c) follows from (a) and (b). QED. Packing is a representation of
disjoint fresh random bits: it adds no premise to H1' and H4' (GPT Sol, answer
AQ 1).

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
as the program's `ctr_look` takes byte p of the scalar word, so the masks are
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
every constant an immediate, the batch is straight-line code with the same count
in every batch. The participant implementation counts 400 units without the
automaton of (1): the eight random words, one operation and one AND each, 16;
the lines of step CO that reach Y9 or omega, 261; omega, 2; the automaton of (2)
in the seven lanes with the test of its mask and the branch, 118; the advance of
the batch count, its comparison with RUN_BATCHES and the branch, 3. At most 25
registers are live, the two counts included, and nothing is spilled. GPT Sol's
certificate of the lean lanes (answer AT 4) adds 7 for the base addresses of the
first table of the automaton of (2) in the seven lanes (every other table entry
holds the base address of the next table, written once with the automata) and 16
for the test of the last batch, the cursor and the dispatch to the lanes whose
mask of (2) is not zero: 400 + 7 + 16 = 423, charged 424; and one more move
per batch that keeps the raw R_7 in its own register for the selector (GPT
Sol, answer BA 1.3), charged even where an AND into another register would
avoid it: 425 units per batch (Section 11). The raw word takes one more
register, at most 26 live. A Q path costs at most 19: four shifts, four byte masks, three
state and index additions, four table loads, the AND with the mask of (2), its
comparison and the branch, and the base addition of the first byte; with 16 for
the E count, its comparison with E_BUDGET, the branch, the store and the
address, 35 (answer AT 4). Only the lanes whose mask of (2) is not zero pay it.
The implementation formed the member with the mask of the sub-class, ran the
automata of the seven outcomes of entry 26ebba63, and ran the automaton of (1)
in every lane, 125 units more (the batch of entry 59f8915e); for the class the
member is the same AND with another mask and the same pending addition (GPT Sol,
answers AN 1 and AQ 2), and restricting the last tables to S changes no count,
so the 400 units are the same. The lean form, with the automaton of (1) in the Q
path, has not been implemented.

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
and the 6 included, and 8,912 for steps 2 and 3.

*The participant check.* A participant implementation of the batch, which is
not part of the package, ran 142,858 batches, 1,000,006 outer steps drawn from
SHAKE-256, with the program's own functions (`ctr_outer`, `ctr_tables`,
`ctr_look`, `ctr_filter`, the same lines as in the package) as the reference,
with the mask and the seven outcomes of the sub-class that the program holds.
In every lane all names of step CO and the mask of the filter equal those of
the program's scalar `ctr_outer` and `ctr_filter` run on the eight words of the
lane with its member number: 1,000,006 of 1,000,006. The rebuilt names of the
passing lanes equal those of `ctr_outer` in 4,452 of 4,452 rebuilds, and the
counts are the same in every batch. In that check the batch with the mask of
the class did not run, nor the lean lanes; its automata, those of the seven
outcomes, are the ones that ran, here with their last tables restricted to S.
The submitted program runs the batch with the mask of the class and the lean
lanes on the root instance; its self-test compares the packed batch with the
scalar step CO lane by lane (Section 13). These are participant measurements;
the organizer does not run the self-test.

**9.7 The s-pattern pre-check and the guard (G7) (GPT Sol, answers AW 1 and 2
and AX 1; the pre-check found by a helper agent of the participant).** Fix a
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
joint root of outcome j. By (PHASE), certified for every joint root in all
eight phases (9.9), and (g) of 9.4, h[16] = h[17] = 0 and h[18] = 1 XOR Q[18],
and e1[0] = e1[1] = 1 for every member, so by the identity above
the bits s[13], s[14] and s[15] of the trial are those of nu. The trial's E1
gives beta*, tau_j and eps, so its s is compatible with outcome j, and by the
enumeration above nu is allowed for j: VMASK[nu] has bit j - 1. So j is in T.
QED. The lemma uses no law of the words. It says which outcomes a passing outer
step can hold; it does not say how often nu takes a value, which enters only the
budget SOLVER_BUDGET (H4').

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
and the branch take 5; and the solver count, its comparison with SOLVER_BUDGET
and the branch take 3: 16 units, inside the 512 of the lane (9.6, Section 11),
paid by every passing lane, also when T is empty. The pre-check never enlarges
T, so the cap of 9.4 holds for every T. VMASK is built once from the enumeration
above, below 2^23 operations, inside the once-only allowance of Section 11.

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

*The charge of (G7) (GPT Sol, answer AX 1.1).* 128 more units for each searched
row, here the one row of the selected slot, inside its 1,280 (9.8): the six source bits e1[22], e1[23], C[22], C[23], B[22] and B[23], the
loads and addresses of the three source words, x, the carry a22, the majority,
h[7], the comparison with an existing constant and its branch, and the insertion
of the value into the descriptor of position 7, fewer than 16 blocks of at most
8 units; the scratch words are released before the 32 descriptors are resident,
so the traversal uses no more registers. The caller stores C2.c1, C2.b1 and e1
in three fixed memory words, at most 6 more units, inside the 512 of the lane.
The extra prescribed bit of the written-out rows is inside the once-only
allowance. No new budget, mean or premise: the solver count still counts every
outer step whose T is not empty, before (G7) runs (GPT Sol, answer AX 1.2).

**9.8 One slot per outer step: the one-path solver (GPT Sol, answer BA 1.3).**
The search of this package does not return every joint root of an outer step.
In an outer step that reaches the solver it follows the single path of one
static slot, named by the selector J of step 1 of 9.1, and certifies at most
one trial. Every listed good trial of the outer step owns exactly one slot, so
the certified count of the outer step is 0 or 1 with mean exactly its number of
listed good trials divided by 32 (Lemma SL, 10.2). This rests on the guards of
9.4 being exact for every joint root, which the certificate of 9.9 establishes
in all eight phases, on the single traversal from the common state of 9.4, and
on the exact envelopes of the mask of (1) from the certificate of Section 8.

*Envelopes.* Let m1 be the mask of (1) on Y9 of the outer step, restricted to S
(9.6). In an outer step that reaches the solver m1 is not empty, and by the
certificate of Section 8 it is a subset of one of the four sets {175020a0},
{275020a0}, {285020a0, 385020a0} and {185020a0, 385020a0, 685020a0} (9.4). The
*envelope* of the outer step is the first of these four sets, in this order,
that contains m1. It is a function of Y9 alone, and it contains every outcome
of T, since T is a subset of X and X of m1.

*Slots.* Each envelope has static ranges of slots, padded to 32:

| envelope | slots 0 to 31 |
| --- | --- |
| {175020a0} | 0 to 7: row 175020a0; 8 to 31: padding |
| {275020a0} | 0 to 15: row 275020a0; 16 to 31: padding |
| {285020a0, 385020a0} | 0 to 15: row 285020a0; 16 to 31: row 385020a0 |
| {185020a0, 385020a0, 685020a0} | 0 to 7: row 185020a0; 8 to 23: row 385020a0; 24 to 31: row 685020a0 |

A row with the free set F of the table of 9.4 (with (G7): {13, 15, 30} on the
rows 175020a0, 185020a0 and 685020a0, and {9, 13, 15, 30} on the rows 275020a0,
285020a0 and 385020a0) has 2^|F| slots, 8 or 16, the number of leaves of its
static tree. For a slot s in the range of a row that starts at s0, the offset
is r = s - s0, and bit k of r is the value that the slot gives to the k-th free
position of the row in increasing order. The ranges depend on the outer step
only through the envelope: they are not compacted around rows that are not in T
or around paths that a carry test prunes.

*The one path.* Given J: if slot J is padding, or its row j is not in T, the
outer step ends with no root. Otherwise the solver runs the formulas and tests
(a) to (g) of 9.4 for the family of row j and for row j, the patches of the row
and the guard (G7) of 9.7, as the complete traversal of 9.4 does for that row;
if a test says that the row has no joint root, the outer step ends. Both carry
guesses a[20] that (a) keeps reach the same common state at depth 7 (9.4, one
traversal), so one path from that state serves both, and the check of (J2) as a
word at the leaf enforces the carry closure. From depth 7 the solver walks the
positions 7 to 31 once: a prescribed position reads the forced array, or at
position 20 the selected array, with its constant or guard written into the key
as in 9.4, and takes its one arc; a free position reads the dual array and takes
the arc whose bit of h is the value that slot J gives to that position. If a
position has no such arc, the outer step ends. At depth 32 the solver checks
(J1), (J2) and (J3) as words for the h of the path; if they hold, it returns h
with the outcome j, and otherwise the outer step ends. A failure is not followed
by another slot: J is drawn once per outer step, with the outer step's own
random word, and is never drawn again.

*Why a slot, and not the first root.* Returning the first root that the
complete traversal finds would also make the certified count of an outer step 0
or 1, but its mean would be the probability that the outer step holds a listed
good trial, which the mean count of H1' does not determine; only a bound of
1/32 of that mean would follow from the cap of 32 roots. The static slot gives
the mean exactly (GPT Sol, answer BA 1.3).

*The charge, 8,912 (GPT Sol, answer BA 1.3).* One selected row costs at most

    4,096 global + 2,304 one family + 1,280 one row + 25 * 32 single-path
    nodes + 80 leaf + 288 root + 64 selection = 8,912

machine units, with the blocks of Section 11: 4,096 once per outer step that
reaches the solver (E' and E XOR E', the names of step CO, the control); 2,304
for the family of the row, the formulas of (a) to (e) of 9.4 and the walks of
bits 0 to 5 under both guesses; 1,280 for the row, its 32 descriptors, the walks
of bit 6, the patches and the 128 of (G7); one node at each of the 25 positions
7 to 31, at most 32 each: a forced node costs at most 20 (Section 11), the
selected node at position 20 at most 24, and a free node at most 8 more
operations than a forced one to take one arc out of the dual entry by the
slot's bit, at most 28; 80 for the leaf check; 288 for step 3 on the one root;
and 64 for the selection: the save and reload of the raw R_7, the extraction of
J from bits 0, 1, 8, 9 and 15 of lane i, the choice of the envelope from m1,
the dispatch to the static range and the rank bits of the offset. No parent is
saved and no second child restored. At most one leaf check and one
certificate are charged, and the whole 8,912 is charged also when the path
fails or the slot is padding. The registers are those of the complete traversal
(Section 11) without its five saved parents, with one more for the offset r: at
most 59 of the 64. This schedule is GPT Sol's, written out by blocks; it is a
proved upper allowance and has not been executed.

**9.9 The all-eight-phase certificate of the guards (GPT Sol, answer BA 2).**
The guards (PHASE) and (P*) of 9.4 are used by Lemmas J0, VP, G7, CV and SL as
facts about every joint root on the whole class. This subsection gives an exact
finite verification of both, for the fourteen outcomes of beta* in all eight
phases (b, u, v), and its output.

*The reduction (GPT Sol, answer BA 2).* Change the coordinates of E3 from (y,
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

*The verifier.* The following text, GPT Sol's (answer BA 2), is ASCII Python
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
lines and 2,261 bytes. GPT Sol wrote it and did not run it.

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
of the table of 9.4. GPT Sol read the source of the run and its logs and found
the source the same as this text (answer BA 2). So (PHASE) and (P*) hold for
every joint root of every outcome of beta* on the whole class, in all eight
phases, and the cells of the parity table of 9.4 are exact in all eight phases.
This is a participant computation of an exact count, not a sample; the
organizer does not run it, and it is not one of the declared experiments. It
closes the finite guard requirement of the solver for the stated advice (Lemma
ADV (f)); it does not bear on the rate of H1' or on the budgets of H4'.

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

*Why S.* Of the 16,383 nonempty sets of outcomes of beta*, S gives the least
exact charge of the complete traversal of entry 0bc5f130 (GPT Sol, answers AW
4 and AX 1.2; Section 12); it has not been compared under the one-path charge
of Section 11. S is part of the stated advice, and the analysis uses its stated
value only (Lemma ADV), not that it is least under any charge.
The row 675020a0 carries 0.1 per cent of the count of the seven, but dropping it
lowers the share of passing pairs by a factor of 1.12 (Section 8).

*Why beta*.* Beta* is not chosen by a ranking in this package: it is the beta
of the solution with which the participant's solver found the six constants
(Section 12), and it is stated here as advice with its cube. Its cube of c1 has k
= 11 fixed bits, mask 0e09818b and value 02008000. On the sub-class of entry
26ebba63, GPT Sol 6.1 ranked the 53 values of beta with a part by their
conditional rates 2^k r(beta), and beta* was first. The program stores beta*
(`CTR_BETA`) and the mask and value of its cube.

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
successes of one outer step is that of 9.4 with Lemma CV: at most 32 listed
good trials (10.3).

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
of the outer steps, at most exp(-mu b(rho) times their number). QED. Lemma S8
is kept for the comparison with entry 0bc5f130 (10.4, Section 15); the success
bound of this package does not use it, since its certified count N_32 is 0 or 1
and so has rho = 0 (Lemma SL).

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
Statement (b) is about M and says nothing about the sampler.

*What the search certifies.* The three lemmas below concern the search of 9.1.
Lemma V follows from 3.3 and is the participant's; Lemma CV rests on the
constants and guards of 9.4, proved by GPT Sol (answers AE 4 and 7, AF 1.3, AO
6.1 and AR 1, 2 and 6.1), among them (PHASE) and the parity certificate (P*),
certified for every joint root on the class in all eight phases by the verifier
of 9.9, and Lemma J0; Lemma SL, the one-slot lemma, is GPT Sol's (answer BA
1.3).

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
is in Q*, its t is not zero and its E1 outcome is j, so the root is certified.
Conversely, a certified root h of outcome j gives a c1 in Q* with t not zero
whose E1 differences are tau_j and eps, and h satisfies (J1) to (J3), so by
Lemma V the trial of c1 has R = 0 with outcome j: it is a listed good trial.
Different roots give different c1 (Lemma IP), and an outer step has at most 32
roots (9.4). QED.

**Lemma SL (one slot per success; GPT Sol, answer BA 1.3).** Fix the seven outer
words and the member of an outer step, O, and let N(O) be its count N_o of H1':
the number of its listed good valid trials over all of Q*. Let N_32 be 1 when
the search of 9.1, reaching this outer step, certifies a root in it, and 0
otherwise. (a) There is a set of N(O) distinct slots in 0 to 31, a function of
O alone, such that N_32 = 1 exactly when the selector J of the outer step lies
in it. (b) So N_32 is 0 or 1, and since J is uniform on 0 to 31 and
independent of O (Lemma PL),

    E[N_32 | O] = N(O) / 32,   E[N_32] = E[N_o] / 32,   E[N_32 (N_32 - 1)] = 0.

*Proof.* (a) If N(O) = 0 then no root is certified, since every certified root
is the E3.h1 of a listed good trial (Lemma CV (b)); the set is empty. Otherwise
the outer step passes, T is not empty, and every listed good trial has its
outcome j in T (Lemmas F and VP). Its E3.h1, h, is a joint root of outcome j that
satisfies (G7) (Lemmas V and G7). The envelope of the outer step contains T
(9.8), so row j has a range of slots in it; the *slot of the trial* is the slot
of that range whose offset gives the free positions of row j the bits of h at
those positions. Run with that J, the one-path solver of 9.8 finds row j in T,
passes the tests of (a) to (g) of 9.4 and (G7) for row j, since h satisfies
them (Lemma CV (a)), and at every position takes the arc of h's own bit: at a
prescribed position the only arc, which is h's by Lemma CV (a), and at a free
position the arc whose bit is the slot's value, which is h's bit by the choice
of the slot. So it reaches the leaf of h, where (J1) to (J3) hold, and step 3
certifies h (Lemma CV (b)). Two listed good trials have different roots (Lemma
IP). If their rows differ, their slots lie in different ranges; if their rows
are the same, the same slot would give the same bits at the free positions, and
the path, which has one arc at every prescribed position, would reach the same
leaf; so their slots differ. Conversely, for a J outside the set of these N(O)
slots, the slot is padding, or its row is not in T, or its path ends, or it
reaches a leaf that is not the root of a listed good trial, which step 3 then
does not certify (Lemma CV (b)); in every case N_32 = 0. The set is a function
of O alone, since the envelope, T, the ranges and the roots are. (b) N_32 is
the indicator of J in a set of N(O) elements of the 32 values, and J is uniform
and independent of O, so E[N_32 | O] = N(O) / 32; taking the expectation over O
gives E[N_32] = E[N_o] / 32; and N_32 (N_32 - 1) = 0 for a count of 0 or 1.
QED. The lemma uses no law of the outer words or of the member: it holds for
each O. It needs the guards of 9.4 to hold for every joint root, which the
certificate of 9.9 gives in all eight phases, and the single traversal from the
common state (9.4).

So the search of 9.1 keeps, in every outer step, exactly 1/32 of the mean
number of listed good trials that an enumeration of all of Q* in that outer step
finds, with the same outer steps, the same members y and the same filter. The
count N_o of every outer step is the same as for that enumeration, and H1' is
about its mean only; H4' is about three counts of the outer steps, which the
slot selection does not change, since J is read only after the solver count
(GPT Sol, answers AE 7, AW 1 and BA 1.3). Lemmas V, VP, G7, CV and SL use no law
of the words. The guards of the solver are lossless: (PHASE) and (P*) are
consequences of exact counts of the class, certified for every joint root in
all eight phases by the verifier of 9.9, (P*) with a count of 0 for the other
parity in every phase and every outcome (9.4), and Lemma J0 is algebra; none
drops a member or a joint root. The pre-check and the guard (G7) lose no listed
good trial (Lemmas VP and G7), and drawing the outer steps seven to a batch
changes no outer step (Lemma PL).

**10.3 Heuristics.**

**Heuristic H1' (score-critical; a rate only).** Over the coins of the run, the
RUN_STEPS independent uniform words of step 1 of 9.1, let N_o be the number of
listed good valid trials (9.1) of one outer step, counted over all of Q*
whether or not the outer step passes the filter or the pre-check. *Rate:*

    E[N_o] >= (2^21 - 1) q,   q = FACTOR * 2^-128,

just under 5p / 7, about 2^-91.474. Nothing else is declared about N_o: no
clause on how the listed good trials of one outer step depend on each other,
and no bound on its factorial ratio rho.

This is the rate clause of the premise of entry 26ebba63, restated for this
search: the whole class of eta with no rule on h1, the six outcomes of S, and
the independent outer steps of 9.1, each with its own random word made of
disjoint fresh bits (Lemma PL) (GPT Sol, answers AO 3.1 and 6.3, AQ 1, AR 6.6,
AT 2, AW 1 and BA 1.4). The clause of entry 26ebba63, reviewed
(plausible_not_refuted), concerns the sub-class with rule A and its seven
outcomes, and it does not by itself imply the law of these trials, whose
members range over the whole class with no rule and whose success event is
that of S: equal model counts and equal budget constants do not identify the
law of the count N_o (GPT Sol, answer AT 2). The rate is declared anew for these
trials and S. Neither the filter nor the pre-check changes it: both skip only
outer steps and outcomes that hold no listed good trial (Lemmas F and VP), so
N_o is the same count, pointwise (GPT Sol, answer AW 1). The slot selection of
9.8 does not change N_o either; it changes what the search certifies, N_32,
whose mean is exactly E[N_o] / 32 for every law of the words (Lemma SL).

In the terms of Lemmas S1 to S4 the premise is this: the construction's
pushforward of the uniform outer words and members, with c1 running over all of
Q*, onto the seven model words (E1.d1, E1.b1, E1.a2, Y4, Y9, w8, E3.h1) carries
at least the share FACTOR / 138,512,695,296, just under 5/7, of the
complete-success integral p of the conditional law of Lemma S1, and that stays
true after the member with t = 0 is dropped (Lemma IP). It does not follow
from the model or from Lemmas S1 to S9. The factor FACTOR = 98,937,639,497 is
assumed; 10.1 gives what it is set against, the count 138,512,695,296 of the
six outcomes of S, of which it is five sevenths rounded down. The filter does
not change it.

*No dependence clause.* Entry 0bc5f130 declared, as part (ii) of its H1', that
the listed good trials of one outer step depend on each other weakly enough for
its run, with the sufficient condition rho = E[N_o (N_o - 1)] / E[N_o] <= 0.0065
of Lemma S8 (Section 15). That clause is not declared here. The search
certifies at most one trial per outer step, and N_32 has the exact mean E[N_o]
/ 32 and rho = 0 whatever the joint law of the trials of an outer step (Lemma
SL); the price is a run about 32 times as long (9.1). The cap N_o <= 32 of Lemma
CV is used only through the 32 slots.

*The rate on passing outer steps.* By Lemma S9 (a), N_o is zero on every outer
step that the filter rejects, so the rate says E[N_o | the outer step passes]
>= (2^21 - 1) q / pi_o, with pi_o of Lemma S9. Per member of Q* of a passing
outer step the rate is then at least about q / pi_o; for pi_o = pi it is q / pi
= 98,937,639,497 / (279,070,422,111 * 2^80), about 2^-81.496: the rate of H1'
divided by the pass share, with no part of the counted mass lost (Lemma S9).
The success argument below uses the rate per walked outer step and needs no
value of pi_o; pi_o enters only the pass budget (H4').

*What is proved and what is not.* Proved (Lemmas S2 to S4): the outer words of
a step are uniform in the chart of the seven context words of Section 4; Y12
and w5 are independent uniform words; E1.a1 and E1.a2 - E1.b1 are independent
uniform words at every fixed c1; and the sampler of Section 8 is exactly the
uniform-counter sampler conditioned on c1 in Q*. Proved as well (Lemmas V, CV
and SL, 10.2): every listed good trial of an outer step owns exactly one of the
32 slots, and the search certifies it exactly when the selector of the outer
step names that slot, so N_32 is 0 or 1 with mean E[N_o] / 32. Not proved: that
E1.b1, E1.a2, E3.h1, Y9 and w8 have the model's joint law with the rest; GPT
Sol 6.1 reduces the rate to one success-weighted density of seven words that
the outer step fixes, Y12, Y1 + w12, C2.b1, C2.c1, w5, Y9 and w8, and that
density has not been counted. Not proved either: how much of the success mass
the member with t = 0 carries (Lemma IP bounds the number of dropped trials,
one in 2^21, not their mass).

*No budgets of stage 2 and of step 3.* The enumeration of all of Q* that the
joint solver replaces had two more halts, a budget of the lanes processed in its
step 3 and a budget E of the words that enter stage 2, and two more heuristics,
H2' and H3', that these budgets do not end the run. The search of 9.1 has
neither budget and declares neither heuristic, and it declares no premise on the
mean of any count of work. Steps 2 and 3 need no budget of their own: in every
outer step that reaches them, whatever its words, the solver follows one path,
returns at most one root, and steps 2 and 3 cost at most 8,912 machine units
(9.8, Section 11). The final pair is formed and hashed only for a certified
root, after which the run halts, so it is formed at most once and is a
collision (Lemma V). The run halts with failure only when one of the three
counts of 9.1 exceeds its budget, which H4' covers, or after the last outer
step, which the rate of H1' and Lemma SL cover (10.4).

**Heuristic H4' (supporting; the budget clauses of this run).** For an outer
step of the run, before any halt, let I_E be 1 when the mask of (2) of its omega
meets S, I_2 be 1 when its mask X is not zero (it passes the filter, Section 8),
and I_3 be 1 when its T = X AND VMASK[nu] of 9.7 is not zero; let N_E, N_2 and
N_3 be the sums of I_E, I_2 and I_3 over the RUN_STEPS outer steps of this run.
H4' says: with probability at least 0.9995 over the coins, N_E <= E_BUDGET, N_2
<= PASS_BUDGET and N_3 <= SOLVER_BUDGET, all three, for the RUN_STEPS and the
budgets of 9.1; so no budget halts the run. It has three clauses, one for each
count, and one failure allowance, 0.0005, for their union (GPT Sol, answers AW
3 and BA 1.4):

- *the pass budget*, N_2 <= PASS_BUDGET. Its nominal share is the exact share pi
  = 279,070,422,111 / 2^48 = 2^-9.978162 of Section 8, for uniform independent
  pairs (Y9, omega).
- *the pre-check budget*, N_3 <= SOLVER_BUDGET. Its nominal share is p_3 =
  558,140,844,222 / 2^51 = pi / 4 = 2^-11.978162, in the counting model M_v of
  the masks for uniform independent (Y9, omega) and an independent uniform nu
  of three bits: for S every nonzero X survives for exactly two of the eight
  values of nu, 3 and 4. This quarter is an exact share of the augmented model,
  not a proved probability of the sampler, whose nu is a function of the outer
  step (9.7); the clause is a physical statement and is not a consequence of
  the pass budget.
- *the lean test-(2) budget*, N_E <= E_BUDGET. Its nominal share is p_E =
  233,715,456 / 2^32 = 2^-4.199822, the exact share of words omega that pass
  the automaton of (2) for S (Section 8).

The clauses are stated for this run, whose RUN_STEPS is about 32 times that of
entry 0bc5f130: a tail bound for a run of fixed length does not by itself
extend to a longer one (GPT Sol, answer BA 1.4). The selector J is read only
after the solver count of an outer step is taken, and none of the three
indicators depends on it. The outer steps of a run are independent and
identically distributed (step 1 of 9.1 and Lemma PL), and each indicator is a
function of the random word of its outer step, so each N is binomial with
RUN_STEPS steps and the sampler's probability of its indicator; the three
indicators of one outer step may depend on each other in any way. Each budget
is ceil(17/16 * RUN_STEPS * p) for its nominal share p. A sufficient condition
for H4' is that the sampler's probability of each indicator is at most 1.06
times its nominal share: then each mean is at most 1.06 / 1.0625 of its budget,
the relative excess is at least 1/424, and the Chernoff bound puts the
probability that a count exceeds its budget below exp(-RUN_STEPS * p * 53 /
18,020,000): below exp(-4.1 * 10^15) for N_E, exp(-7.5 * 10^13) for N_2 and
exp(-1.8 * 10^13) for N_3, the smallest exponent. By the union bound the
probability that some budget is exceeded is then below 3 * exp(-1.8 * 10^13),
far below 0.0005 (GPT Sol, answers AW 3 and BA 1.4). That the three
probabilities are at most 1.06 times their nominal shares is not proved: the
sampler's Y9, omega and nu are not proved independent and uniform. What H4'
needs is these three counts, not a mean of any work: the quarter share of the
pre-check enters only SOLVER_BUDGET, which halts the run if it is exceeded, and
the time bound does not depend on it. Measured (Section 13, participant
evidence on the whole class): on 60,000,000 real outer steps, N_E is 1.0004 +-
0.0005, N_2 0.9980 +- 0.0041 and N_3 1.0123 +- 0.0082 of RUN-scaled nominal
values; on another 30,000,000, the share of passing outer steps that survive the
pre-check is 0.25101 against 1/4 (z = +0.40), and N_2 is 0.9981 +- 0.0058 of its
nominal value. With the seven-outcome filter of entry 26ebba63 and members of
the sub-class, the pass share was 2^-9.8127 against its exact 2^-9.8132 on 2^22
passing outer steps, and 1.00012 +- 0.00016 of it on 2^35 outer steps. If a
budget is reached the run halts with failure; the time bound charges each
budget plus one and is not affected. This is H4' of entry 0bc5f130 with the
same three clauses and shares, stated for the run of this package (GPT Sol,
answers AO 6.3, AW 3 and BA 1.4).

**Heuristic HPRE (supporting; the bound on the computation that found the
advice; HPRE-discovery-bound in claim.json).** All computation that produced
the stated advice of Section 12, the solver runs, the exact counts, the choice
of S and the exact computations that derive the numbers of 9.1 from the advice
included, is at most 2^70 charged word operations of the cost model, under the
device list and the window of 30 days that the participant attests (Section
12). It is charged as P = 2^70 machine units = 2^70 / 430 = 2^61.25181 units of
time (Section 11), and preprocessing_log2 = 61.2519. *Evidence:* the table of
Section 12, the peak rate of every attested device at its boost clock, with
every lane busy in every cycle and fused operations counted as two, 3.805 *
10^14 = 2^48.43 operations a second in all; times the window, 2,592,000 s =
2^21.31, that is 986,170,982,400,000,000,000 = 2^69.740 operations, below 2^70.
*Limitation:* the conversion from hardware 32-bit lane-instructions to charged
word operations is taken as one-to-one, that is every charged operation of the
programs that ran is taken to need at least one lane-instruction; this is not
certified. The device list and the window are the participant's attestation,
which no organizer run checks, and the inference of the AI models that wrote
formulas and code searched no candidates and is not counted. *Sensitivity:*
were the bound 2^72 operations, the total of Section 11 with 2^72 / 430 in
place of P would have log2 T = 71.75200488803260..., time_log2 = 71.7521
(preprocessing_log2 63.2519), against 71.7491 at 2^70 (Section 11). HPRE
enters only P: neither the success bound (Lemma ADV, 10.4) nor the search part
of T uses it.

*No premise on the advice values.* The values that the search reads as advice
are stated in this text (Section 12), and the success bound is proved for them
as stated (Lemma ADV), from properties that this text checks exactly for those
values: Fact P, Lemma Q, Theorem C (iv), the table of 10.1 with the program of
Section 17, the certificate of the filter for S (Section 8) and the verifier of
9.9. No statement of the analysis concerns the output of a selection
procedure, and no selection procedure is part of the algorithm: the premises of
the success bound are H1' and H4' and nothing else. The search that found the
values is not part of the algorithm; its cost is charged in T as the
preprocessing P under HPRE (Section 12). Entry 78ac164c declared a premise
HSEL-selection-return, that a capped selection procedure returns these values;
it is not declared here (Section 15).

**10.4 Success probability.** The probability space is the random words of the
RUN_STEPS outer steps of step 1 of 9.1, independent uniform 256-bit words made
of disjoint bits of the fresh draws (Lemma PL), for the fixed target and the
stated advice of Section 12. The algorithm is otherwise deterministic. For each
outer step let N_32 be its
certified count of Lemma SL, a function of its random word whether or not the
run reaches it. The N_32 of the outer steps are independent (Lemma PL), each is
0 or 1, and by Lemma SL and the rate of H1' each has mean

    E[N_32] = E[N_o] / 32 >= (2^21 - 1) * FACTOR / (32 * 2^128).

If the run outputs no pair, then either a budget was reached, or every outer
step was reached and none has N_32 = 1 (an outer step with N_32 = 1 that is
reached certifies a root, and the run outputs its pair, 9.1). The first event
has probability at most 0.0005 by H4'. The second has probability at most

    (1 - E[N_32])^RUN_STEPS <= exp(-RUN_STEPS * (2^21 - 1) * FACTOR / (32 * 2^128))
                            <= exp(-lambda),

since RUN_STEPS * (2^21 - 1) * FACTOR >= lambda * 32 * 2^128 by the choice of
RUN_STEPS in 9.1 (in integers: RUN_STEPS * (2^21 - 1) * FACTOR * 25,000 >=
12,378 * 32 * 2^128). So under H1' and H4' the search outputs a collision with
probability at least

    1 - exp(-0.49512) - 0.0005 = 0.3900022368238... > 0.39

(GPT Sol, answer BA 1.4). This is the union bound over the two events, which
need not be independent: the rate of H1' with Lemma SL bounds the second and
H4', its three clauses together, the first. No allowance for dependence inside
an outer step enters: the 0.001 of entry 0bc5f130 is gone. When the algorithm
outputs a pair, the pair is a genuine collision: its trial is certified, so R =
0 (Lemma V), step 3 checks both complete digests, and the messages have
different lengths. The run is the shortest of this form that gives 0.39: 0.49512
is the smallest number of five decimals for which the bound reaches it, and with
0.49511 in its place the bound is below 0.389997.

*Sensitivity to the factor.* If the valid trials are listed good trials at f *
2^-128 each on average, the run gives at least 1 - exp(-f * RUN_STEPS * (2^21 -
1) / (32 * 2^128)) - 0.0005, which reaches 0.39 only when f is at least
98,936,906,150; the assumed FACTOR is 1.0000074 times that. The margin of the
claim lies between the assumed 98,937,639,497 and the counted 138,512,695,296, a
factor of 1.40. The entries on this track that build on entry c66f230d, entries
64c075ac and e7b17fd1 among them, took half of an exact model count, a factor
of 2.00; this package takes five sevenths, as entries 26ebba63 and 0bc5f130 did.
If the count is exact, the run has a mean of 0.6932 certified trials and the
bound is 0.4995. For an f between 1 and 98,937,639,497 the same success needs
0.49512 * 32 * 2^128 / f walked trials; RUN_STEPS and the three budgets scale
with it, and at f = 1, the uniform rate, the package would submit 108.28.

*Against the complete traversal.* The complete traversal of 9.4, which certifies
every listed good trial of an outer step, has rho <= 31 by the cap of 32 roots
(Lemma CV), and Lemma S8 gives b(31) = 1/32: run as long as this search, with
its own charge of 31,456 per outer step that reaches the solver and 424 per
batch, it also proves the bound 0.39 from the rate alone, at log2 T =
71.87100104... with the preprocessing P of Section 12 and the final step of
Section 11, 71.8711 rounded up at the fourth decimal (recomputed in integers by
the participant). GPT Sol's figure 71.87009... (answer BA 1.4) charged in place
of P the cap of the selection procedure of entry 78ac164c (Section 15) and
belongs to that labelled history. The one-path form gives the same retained
mean, 1/32, exactly and at the lower charge of 8,912, and is the search of this
package.

None of the three heuristics is proved. Section 13 lists the evidence for H1'
and H4', and Section 12 that for HPRE.

## 11. Charged time

One 2-round target compression costs one unit, and every other primitive word
operation, every load and every store included, costs 1/430 of a unit. The rows
below are in operations, loads and stores, called machine units here; 430 of
them make one unit of time.

*The machine.* The search is charged on the
load/store machine of 6.5, with its 256-bit words, its packed lanes, its masked
rotation and its charge of one unit for every operation, load and store, with
two changes: it has 64 registers in place of 16, and every constant is an
immediate operand, written in its instruction and not loaded. The cost model of
the track charges primitive word operations and sets no register count; this
text charges as well a load for every other word fetched from memory into a
register and a store for every word written to memory, spills included. The
batch of seven outer steps runs on packed words (9.6); the rebuild of a passing
lane, the joint solver and step 3 run on scalar words of the same machine, one
32-bit value to a word. The pieces of 6.5, the earlier program's own counts on
16 registers (9.3) and the ledger counts of the submitted program (Section 13)
are not part of the charge.
The schedules of this section are GPT Sol's (answers AL 2, AQ 2, AR 3 and 6.2 to
6.6, AT 1 and 4, AW 2 and 4, AX 1 and BA 1.3 and 1.4), upper bounds written out by blocks, not
counts of an executed program; the only counted parts are the 400 units of the
batch and the 295 of the rebuild of a passing lane, which a participant
implementation counted with the mask of the sub-class and the filter of the
seven outcomes (9.6).

**The cost, with every term.** Every row is machine units times an upper bound
on how often a run executes it; a row with a budget runs at most that many
times, plus the one that halts, because the algorithm halts with failure when a
count passes its budget (9.1). Exponents of counts and products are rounded up.

| Row | How often over a run, at most | Units | log2 of the product |
| --- | --- | ---: | ---: |
| batch of seven outer steps (9.6): the eight random words, the lines of step CO that reach Y9 or omega on packed words, omega and the automaton of (2) in every lane (counted, 400), the first table bases of (2), the test of the last batch, the cursor and the dispatch (bound in words, 24), and the move that keeps the raw R_7 (1) | RUN_BATCHES = 2^71.653 | 425 | 80.385 |
| Q path of a lane whose mask of (2) meets S: the automaton of (1) on its Y9, the AND, the test and the branch (19), the E count, its test and its store (16) | E_BUDGET + 1 = 2^70.348 | 35 | 75.477 |
| passing lane: the pass count, the rebuild of its outer step on scalar words, the context of the batch, and the pre-check of 9.7 with the solver count (bound in words, 512) | PASS_BUDGET + 1 = 2^64.570 | 512 | 73.570 |
| outer step that reaches the solver: the slot selection and the one-path solver of 9.8 with the guard (G7), and step 3 for its root (bound in words) | SOLVER_BUDGET + 1 = 2^62.570 | 8,912 | 75.691 |
| once: the static rows and descriptors (2^20); the automata of the filter, the three transition arrays, the written-out code of the search, and the row metadata, VMASK, array bases and initialisation (2^26 each); the resident constants and the last test (40); a final failed budget test (16) | once | 269,484,088 | 28.006 |
| **total** | | | **80.497** |

In exact integers the sum of the rows is 425 * RUN_BATCHES + 35 * (E_BUDGET +
1) + 512 * (PASS_BUDGET + 1) + 8,912 * (SOLVER_BUDGET + 1) + 2^20 + 4 * 2^26 +
40 + 16 = 1,577,609,586,486,718,637,261,475 + 52,581,528,000,562,769,967,150 +
14,014,627,652,570,475,771,904 + 60,985,528,144,388,710,985,088 + 269,484,088 =
1,705,191,270,284,240,863,469,705 machine units, the numerator O_32 of GPT
Sol's answer BA 1.4 without its selection term, in integer arithmetic.

*Why each budget plus one.* At most E_BUDGET lanes run the Q path, at most
PASS_BUDGET passing lanes are rebuilt and pre-checked, and at most SOLVER_BUDGET
outer steps run steps 2 and 3: in each case the next one advances its count past
the budget and halts the run before the work of its stage. Each row charges its
whole allowance for its budget plus one, which covers these and the one that
halts (GPT Sol, answers AW 4 and BA 1.4).

*The batch, 425.* Counted by the participant implementation of 9.6 on the
machine above, the same in every batch: the eight random words, one operation
and one AND each, 16; the lines of step CO that reach Y9 or omega, 261; omega,
2; the automaton of (2) in the seven lanes, each with the extraction of its four
bytes, the additions of the states, four table loads, the test of its mask and
the branch, 118; the advance of the batch count, its comparison with RUN_BATCHES
and the branch, 3: 400. Bound in words (GPT Sol, answer AT 4): 7 for adding the
base address of the first table of the automaton of (2) in each lane, and 16 for
the test of the last batch, whose lane 6 is not used, the cursor and the
dispatch to the lanes whose mask of (2) is not zero. 400 + 7 + 16 = 423, charged
424; and one move that keeps the raw R_7 in its own register before its AND
with fc307cfc, for the selector of 9.8 (GPT Sol, answer BA 1.3): 425. No pass
bitmap and no other backup of R_0 to R_7 is stored in the batch. The
count was made with the mask and the seven outcomes of the sub-class, the
automata of this search; with the mask of the class and the last tables
restricted to S the lines, the four byte lookups per lane and the tests are the
same (9.6).

*A Q path, 35* (GPT Sol, answer AT 4), for each lane whose mask of (2) is not
zero: four shifts, four byte masks, three state and index additions, four table
loads, the AND with the mask of (2), its comparison and the branch, and the base
addition of the first byte, 19; and 16 for the E count, its comparison with
E_BUDGET, the branch, the store and the address. A lane whose mask of (2) is
zero cannot pass and does not pay it (Lemma PB).

*A passing lane, 512 outside steps 2 and 3* (GPT Sol, answers AQ 2, AT 4, AW 2
and AX 1.1): the eight words taken out of lane i by a shift and an AND, and step
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

*Steps 2 and 3, 8,912.* An outer step that reaches the solver is charged by
blocks, each an upper bound on its operations, loads and stores, with addresses,
branches, spills and the restoration of registers included (GPT Sol, answers AL
2, AR 3 and 6.3 to 6.5, AT 1, AW 2, AX 1.1 and BA 1.3). The blocks are those of
the complete traversal of entry 0bc5f130, with one family, one row, one node at
each position and at most one leaf and one root:

- 4,096 once per outer step that reaches the solver: E' = omega + DY3 and E XOR
  E', keeping the names of step CO that steps 2 and 3 read, the control and the
  record of the root.
- 2,304 for the family of the selected row (9.4): at most 128 blocks of the
  formulas of (a) to (e) of 9.4, the phase checks, (P*) and their preparation,
  at 12 units each, 1,536 (the 112 blocks of the formulas of answer AI 2 and 16
  more; a block is the extraction of one source bit, a majority of four
  operations, an XOR of at most five inputs, the comparison or choice of a carry
  prescription, or a carry update, with its branch and assignment); the walks of
  bits 0 to 5 under the two guesses, at most 32 units a bit, 384; and 384 for
  the record of the family, the packing of the guard planes and the dispatch.
- 1,280 for the selected row: its 32 descriptors built into 32 registers, at 32
  each, 1,024 (seven fields vary with the outer step, Q[i], y[i], E[k], E'[k],
  kappa[k], kappa[k+1] and the value of a constant, at 4 operations each, and 4
  for the static base, the shift of the key and the assignment); 128 for the
  walks of bit 6 under the two guesses (64), the patches of h[6], h[7], h[13]
  and h[26] (24), kappa and the consistency of bit 6 (8), and the dispatch of
  the row (32); and 128 for the guard (G7) of 9.7 (answer AX 1.1).
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
- 80 for the leaf: g, f, e2 and h2 of its h and (J1), (J2) and (J3) as words,
  a rotation at five operations, 64; and 16 to reload the context words.
- 288 for the root: step 3 of 9.1, that is the inverse of Lemma IP, the cube
  test, t and its test, E1 on A and on B and the comparison of their
  differences, 256; and 32 to reload the context words.
- 64 for the selection: the save and reload of the raw R_7, the extraction of
  J from bits 0, 1, 8, 9 and 15 of lane i, the choice of the envelope from the
  mask of (1), the dispatch to the static range of the slot and the rank bits
  of its offset.

So steps 2 and 3 cost at most

    4,096 + 2,304 + 1,280 + 25 * 32 + 80 + 288 + 64 = 8,912

machine units in every outer step that reaches them, whatever its words,
whatever its T and whatever its slot (GPT Sol, answer BA 1.3; the arithmetic
recomputed by the participant). The whole allowance is charged also when the
slot is padding, its row is not in T or its path ends early. The blocks are
added whether or not they occur together, so this is an upper bound; it is not
claimed to be attained or to be the least such bound. For comparison, the
complete traversal of 9.4, which visits every row of T and every node of the
static trees, has the cap 31,456 with (G7) (answer AX 1.1), the charge of
entry 0bc5f130; this search does not run it.

*Registers of steps 2 and 3* (GPT Sol, answers AL 2, AR 3 and 6.3 and BA 1.3).
The one-path code of 9.8 is written out statically for each row: a prescribed
position has one arc, whose code follows that of its parent; a free position
takes one arc by the bit of the offset r; the last position jumps to the leaf
check. No parent is saved. The registers are the 32 descriptors, six context
words, eight constants, array bases and control words, two words of the current
state (the prefix of h and, above bit 32, the two carries and the bit e2[29],
the only earlier output bit that a later guard reads; the guard of position 25
reads bit 13 of the prefix), ten temporaries and the offset r: 59 of the 64.
The leaf and the root keep the descriptors and use the others for their check,
after which the context words are reloaded (the 16 and the 32 above). The
formulas of a family run before the descriptors are built, in at most 58
registers: at most 35 bits and carries, five source and context words, eight
table, literal and control words and ten temporaries. No register is addressed
by a value: every position and register is named in the code.

*Once.* 2^20 for the six static rows of the outcomes of S, the static fields of
their descriptors at the 32 positions and the metadata of the batches. 2^26 for
the two automata of the filter for the seven outcomes, built and composed into
eight byte tables whose entries hold the base address of the next table, with
the entries of the last tables ANDed with S (GPT Sol, answers AN 2 and AQ 2):
their states at each of the 32 bits are images of those of the fourteen-outcome
automata, at most 146, so the allowance of answer AN 2 covers them. 2^26 for the
three transition arrays of 9.4: their 2^18 entries at most 256 operations each,
the enumeration of the keys, both candidate arcs, the test for an invalid or a
second arc, the selection and the store included (answer AR 6.2). 2^26 for
writing the code of the search: the one-path code of 9.8 for the six rows of
S, 25 positions each with the prescribed bit of (G7) at position 7, and the
static slot ranges of the four envelopes, far fewer than 2^14 labels, at most
256 operations each with their set-up (answers AL 2 and BA 1.3). And 2^26 for the row metadata,
the absolute bases of the arrays and their initialisation, a fourth allowance
that GPT Sol keeps for safety (answer AR 6.2), which also covers the enumeration
of the compatible patterns of 9.7 and the eight words of VMASK, below 2^23
operations (answer AW 2). 32 for loading the resident constants and array bases
into their registers, 8 for the test of the final halt, and 16 for a final
failed budget test, kept conservatively (answer AW 4).

*One-time items.* The items above are in the last row. The final step, once:
steps CT and CS for the trial found, writing the two messages, shorter than
2^42 bytes each, and two complete evaluations of blake3; each message has at
most 2^32 chunks of 16 compressions each and fewer than 2^32 parent
compressions, below 2^37.1 compressions for both, and writing them is below
2^38 machine units: below 2^38 units of time in all. Preprocessing: all
computation that produced the advice, charged as P = 2^70 machine units, that
is 2^70 / 430 = 2,745,561,908,645,142,566.10... units of time, 2^61.25180715...,
under the supporting heuristic HPRE (10.3; the table of Section 12).

Total:

    T <= (sum of the rows) / 430 + 2^38 + 2^70 / 430
      <  2^71.7491.

In exact arithmetic, with N = 1,705,191,270,284,240,863,469,705 + 430 * 2^38 +
2^70 = 1,705,191,270,284,240,863,469,705 + 118,197,499,985,920 +
1,180,591,620,717,411,303,424 = 1,706,371,862,023,155,774,759,049 machine
units, T = N / 430 = 3,968,306,655,867,804,127,346.62... units and log2 T =
71.74901350873373...; in integers, N^10000 < 430^10000 * 2^717491 and N^10000 >=
430^10000 * 2^717490, that is T^10000 < 2^717491 and T^10000 >= 2^717490.
The submitted bound is time_log2 = 71.7491, the total rounded up at the fourth
decimal. The search part, the rows and the final step, is
2^71.74801500237263...; P is 2^-10.496 times it and adds 0.000999 to log2 T.
Were the bound of HPRE 2^72 operations, N would be
1,709,913,636,885,308,008,669,321, log2 T = 71.75200488803260... and the claim
71.7521 (N^10000 < 430^10000 * 2^717521 and N^10000 >= 430^10000 * 2^717520).
Entry 78ac164c charged in place of P the cap of a selection procedure,
8,882,224,365,081,579,520 machine units, and claimed 71.7481 (Section 15).
The search part is a worst-case bound for the algorithm as stated, which halts
within its three budgets on every run and whose steps 2 and 3 are bounded in
every outer step that reaches them; P is a fixed number. No mean of a count of
work enters T; H1' and H4' enter only the success probability of 10.4, and
HPRE only the size of P. The claim uses this schedule on 64
registers; no figure on 16 registers is claimed, and the schedule is not
claimed to be the cheapest.

*Where the search part goes.* The batches are 92.52 per cent of the sum of the
rows, the Q paths 3.08 per cent, the passing lanes 0.82 per cent, the outer
steps that reach the solver 3.58 per cent and the one-time items less than
10^-12 per cent. Per walked trial, RUN_STEPS * 2^21 of them, the sum is
0.0000312921 machine units (2^-14.964); per member of Q* in SOLVER_BUDGET + 1
outer steps that reach the solver it is 0.1188.

*The one formula.* In the form used for the entries of this track, time_log2 =
log2(lambda) + 128 - log2(C / m) + log2(ops / 430) + c, with lambda = 32 *
0.49512 = 15.84384 expected listed good trials (of which the slots keep a mean
of 0.49512 certified), C = 138,512,695,296 the count of the six outcomes of S in
10.1, m = 1.4 the margin and ops = 0.0000312921 machine units per walked trial
from the sum above, gives 71.7480 for the search. The one-time items and the
final step are far below the allowance c; the preprocessing P adds 0.000999
(above), and the claim charges it in full in the exact total.

The algorithm has no sorting and no lookup by value: a root is tested against
the conditions of its outcome, and a certified trial is not compared with other
trials. It reads the two automata of the filter, four table entries per lane of
a batch at positions given by the bytes of omega and four more at positions
given by the bytes of Y9 in a lane whose mask of (2) is not zero; in a passing
outer step, the stored words of its batch and the entry VMASK[nu]; in an outer
step that reaches the solver, the raw R_7 of its lane, the three transition
arrays at the keys of the one path, the record of its family and the static row
and slot range of its outcome.
Its loads are counted: the 28 table loads of (2) in a batch are among its 400
counted units, the four of a Q path among its 19, and the loads of a passing
lane, of the pre-check, of the slot selection, of the one-path solver and of
step 3 are inside the allowances above.

## 12. Memory, preprocessing and advice

The program of the search is the lines of steps CO, CT and CS, the outer
filter, the batch of 9.6, the one-path solver of 9.8 with its statically
written code and slot ranges, and a compression routine for step 3 and the final check: below 2^28
bytes of code and metadata (Section 11). Data, one word of 256 bits each unless
said otherwise: the 29,952 entries of the tables of the filter's two automata;
the three transition arrays of 9.4, 2^18 words of 32 bits, 2^20 bytes; fewer
than 4,096 words for the solver (the descriptors of the positions of a row,
the six static descriptors of S, the slot ranges of the four envelopes, the
record of a family, the one root and scratch); and fewer than 1,024 words for the names of step
CO, the context of a batch, the constants and masks, VMASK, the three counts and the
cells of step 3. The memory of the search is therefore below 2^28 + 2^21 +
2^20 + 2^18 < 2^29 bytes. Nothing grows with the number of trials. The two
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
The submitted program stores no word of the sub-class or of rule A. The earlier
program (6.5) also stored 20 bytes for its root instance and its sub-class
search, the 8 bytes that name the two bits of the sub-class and their values
and the 12 bytes of the two masks and the word ALL of Lemma A, 93 bytes in all;
either way the advice is below 128 bytes. The tables of the filter's automata,
VMASK, the three transition arrays, the descriptors, the slot ranges and the
traversal are not advice: step 0 of 9.1 computes them from these values, and
the last row of Section 11 charges that. FACTOR, RUN_STEPS, SHARE, E_COUNT,
V_COUNT, the three budgets and RUN_BATCHES of 9.1 are not advice either: 9.1
derives them from these values by its formulas and by the exact counts of 10.1
with Section 17, of Section 8 and of 9.7, and that derivation is preprocessing,
inside the preprocessing P below. The flags 3 and the counter rule are part of the
algorithm. There is no other stored data and no stored collision.

**Lemma ADV (the success bound holds for the stated advice).** Let the
algorithm of 9.1 run with the advice above. Under H1' and H4' (10.3) it outputs
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
(d) the table of 10.1 with the counting program of Section 17, printed with its
    output: the fourteen outcomes of beta* on the class, all with eps =
    6e21be55, and the part 67,633,152 = 1,032 * 2^16 of the six of S = 5f, from
    which 9.1 derives FACTOR and RUN_STEPS;
(e) the certificate of the filter for S (Section 8): pi = 279,070,422,111 /
    2^48 and E_COUNT = 233,715,456, with Lemma F; and the allowed patterns of
    the pre-check with V_COUNT and Lemmas VP and G7 (9.7);
(f) the verifier of 9.9, printed in full and run by the participant: (PHASE)
    and (P*) for every joint root of every outcome of beta* on the class, in
    all eight phases, which Lemmas V, CV and SL use (10.2);
(g) the static rows of S, the slot ranges and the cap of 8,912 of 9.8 and
    Section 11, written for the six rows of S.

Proof. The bound of 10.4 combines the rate of H1', whose FACTOR 9.1 derives
from (d); the three clauses of H4', whose budgets 9.1 derives from (d) and (e);
Lemma SL, whose guards are exact by (f); Lemma PL; and the run length of 9.1.
That an output pair is a collision follows from Lemma V, Theorem C and Lemma
TR, which use (a) to (c). The time bound of Section 11 uses (e), (g), the
budgets and P, whose size is the bound of HPRE (10.3). Each of these statements
is about the displayed values. None refers to a selection procedure, a solver
log, a recount or any output of a search: the analysis does not use that S is
least under some charge, that these constants have the largest part among the instances of a
solver log, or that beta* is the beta of a solution of a solver. So the lemma
holds for the stated advice however it was found. QED.

**The construction of the advice, charged as preprocessing.** The advice was
found by a search of the participant that the submitted program does not run
(below). The cost model counts all preprocessing, including any search omitted
from the submitted program, in the total time. This text charges all
computation that produced the advice as

    P = 2^70 machine units (charged word operations)
      = 2^70 / 430 = 2,745,561,908,645,142,566.10... units of time,
        about 2^61.25181,

included in T (Section 11); preprocessing_log2 = 61.2519 is log2 P rounded up
at the fourth decimal (in integers, 2^700000 < 430^10000 * 2^612519 and
2^700000 >= 430^10000 * 2^612518). That P bounds that computation is the
supporting heuristic HPRE (10.3). P is not a statement about what any search
returns and not the cost of a step of the algorithm, and the success bound
does not use it (Lemma ADV). P also covers the exact computations that derive
the numbers of 9.1 from the advice: the count of Section 17, which ran in about
2.5 minutes, the certificate of Section 8, the formulas of 9.1 and 9.7, and the
comparison of the 16,383 outcome sets below.

*The bound of HPRE.* Every charged word operation (an addition, subtraction,
XOR, rotation, AND, comparison or load of a 32-bit word) is taken to need at
least one hardware 32-bit lane-instruction, so a device performs at most lanes
x clock x operations per lane per cycle charged operations a second. The rates
below are deliberate over-estimates: peak boost clock, every lane busy in every
cycle, fused operations counted as two. The participant attests that the list
covers every machine used by any of the project's models, over a window of 30
days, 2,592,000 s, from the start of the project on 2026-10-05.

| Device (attested by the participant) | Charged operations a second, at most |
| --- | ---: |
| 1 x RTX 3090 (local): 10,496 lanes x 2.1 GHz x 2 | 4.408 * 10^13 |
| 4 x RTX 3070 (server): 5,888 lanes x 2.0 GHz x 2 each | 9.421 * 10^13 |
| 24 local CPU cores: 64 lanes (AVX-512 x 4 ports) x 5.5 GHz x 2 each | 1.690 * 10^13 |
| 64 server CPU cores (an allowance): the same rate per core | 4.506 * 10^13 |
| cloud and model sandboxes: at most 4 running at all times for the whole window, each as 64 cores at the same rate per core | 1.802 * 10^14 |
| **total** | **3.805 * 10^14 = 2^48.43** |

Over the window: 380,467,200,000,000 * 2,592,000 = 986,170,982,400,000,000,000
= 2^69.740 charged operations, below 2^70 = 1,180,591,620,717,411,303,424 by a
factor of 1.197. The inference of the AI models that wrote formulas and code
is not a search over candidates and is not counted. What is not certified: the
conversion from lane-instructions to charged operations, taken as one-to-one;
the device list and the window rest on the participant's attestation, which no
organizer run checks (HPRE, 10.3).

*Context: the logged search.* The participant's records of the search,
described below, show 116 solver runs, each stopped within 9,010.5 seconds on
one processor core, and 65 recounts, each within 320 seconds, at most 1,066,018
core-seconds in all, below 2^20.024; at the rate per core of the table, 7.04 *
10^11 operations a second, that is below 2^59.381 operations, 2^-10.6 of P.
These records are context, not the basis of P: the bound above also covers
work that they do not record.

*How the values were found (participant records; not part of the algorithm or
of the analysis).* The participant's solver log for this search has 116 runs of
the SAT solver kissat (51 for the lengths 55 and 63, the other 65 for nine other
variants of the instance; bounds 97 to 118; logged seeds) on instances made by a
generator of the participant. For the lengths 55 and 63 the instance is that of
entry c66f230d (its Section 10): the call C3 for both messages with equal b and
d outputs, the two words w4 related as the length cancellation prescribes for
the XOR 8 of the lengths, the top byte of word 13 zero, E1 and E3 for both
messages, a zero residual, and a bound on the number of bit positions, bit 31
excepted, at which a difference is active in six additions of E1 and E3. The run
for the lengths 55 and 63 with bound 104 and seed 506 found these six constants
after 4,770 seconds, with a solution of class 830303cf and beta 18b0e098, which
is beta*. An exact integer recount, by the participant's counter on the whole
class of each instance, of all 65 distinct instances that the runs of the log
returned with a model gave these constants the part 71,698,432, the largest, and
the next 13,107,200 (a strict maximum, 5.47 times the next); every model was
replayed on 32-bit words. The cube of beta* follows from beta* by the proof of
Theorem C (iv), and its outcomes by the count of 10.1. S = 5f has the least
numerator of the complete-traversal charge of entry 0bc5f130 among the 16,383
nonempty sets of outcomes of beta* (GPT Sol, answers AW 4 and AX 1.2, in exact
integers, without and with the guard (G7); a helper agent of the participant
found the same S for the charge with the cap 56,096); whether S is also the
least set under the charge of Section 11 has not been compared. The log does
not fix every instance: some runs excluded pairs that runs finished before them
had found, and 32 runs were stopped from outside without a record of the cause.
The generator, the solver log and the counter are not in the package, and no
organizer experiment runs them. Entry 78ac164c wrote this search as a capped
procedure, SEL, charged its cap of 8,882,224,365,081,579,520 operations, and
declared the premise HSEL that SEL returns these values (Section 15). This text
states the values instead, and the size of P rests on the bound of HPRE above,
not on these records.

*Memory.* The discovery computation ran on the attested devices of Section 12, whose
memory together is below 2^41 bytes (observed peak below 2^34). The search holds fewer than
2^29 bytes, the advice 73 bytes and the output fewer than 2^43 bytes. Held at
once, these total below 2^43 + 2^41 + 2^29 + 2^7 < 2^44: memory_log2_bytes = 44
bounds all, the discovery's memory included at the full device total
(not only its observed peak). The measurements of Section 13 on real and on scaled-down
messages are not part of the construction; they test the heuristics and select
nothing, and neither their work nor their memory is in these figures. The cost
model does not score memory.

## 13. Evidence, scope and field meanings

Throughout this text costs and bounds are rounded up, and margins, rooms and the
whole numbers of the count that the claim uses are rounded down. Counts printed
with decimals are rounded to the nearest.

**What is exact.** Sections 2 to 5, 7 and 8; Lemmas L, H, Q, Q2, T, T2, T4, N,
A, TR, CT, IP, F, CB, J0, PL, PB, V, VP, G7, CV, SL and ADV and Theorem C; the count
of passing pairs of Section 8 and the allowed patterns of the pre-check (9.7);
(PHASE) and the parity certificate (P*), exact counts, certified in all eight
phases by the verifier of 9.9; the slot ranges of 9.8; the constants and caps of
the solver (9.4, 9.8) with its schedule (Section 11), as upper bounds; and
Lemmas S1 to S9 under their stated hypotheses. Lemma A says
what stage A tests, not that a collision passes it. The declared experiment
`half-collision` runs the search of 9.1 on the root instance for 1,792 outer
steps per organizer seed and returns a pair built by steps CO and CT at
counter word 0, and the organizer recomputes both digests; every such pair
agrees on the 128 masked digest bits (*The submitted program*, below). The
counter instance has no organizer-run check (6.4).

*What is new in the exact part and who has checked it.* Sections 1 to 6 are
those of entry 64c075ac without its clusters; Lemmas L, H, Q, T and N and Fact P
go back to entry c66f230d. New in entry e7b17fd1 were Lemma TR, the counter
order with Lemma CT and Theorem C, and the counter batch with Lemma CB, written
by helper agents of the participant, instances of the same AI model as the
author of this text; and Lemmas IP and S1 to S8, proved by GPT Sol 6.1. New in
this package are the outer filter, proposed by a helper agent of the
participant; Lemma F and Lemma S9, proved by GPT Sol in its answer AC, the proof
of Lemma F written out in Section 8 by a helper agent of the participant from
the assignments of E3; the count of passing pairs with its certificate, derived
by GPT Sol in the same answer; and the joint solver of 9.4, its constants and
caps proved by GPT Sol in its answers AE and AF, with Lemma V of the participant
and Lemma CV (10.2); and, for the class of this package, the phase guards and
the single traversal of the solver (GPT Sol, answer AO 6), the parity
certificate (P*), Lemma J0, the transition arrays and the families (answer AR),
the restriction of the solver to the seven outcomes with its cap of 37,032
(answer AT 1) and to S (answer AW 2), the guard (G7) with Lemma G7 and the cap
of 31,456 (answer AX 1), the lean lanes (answer AT 4), the s-pattern pre-check
with Lemma VP (answer AW 1 and 2; found by a helper agent of the participant),
and the independent lanes of the batch with Lemmas PL and PB (answer AQ); and,
new in this package, the selector bits, the 32 static slots and the one-path
solver with Lemma SL and the cap of 8,912 (answer BA 1.3), and the verifier of
the guards in all eight phases (answer BA 2), which the participant ran
(9.9). The participant's checks of the new exact part are computations,
not proofs: the counter construction against the organizer's own functions on
2,000 trials, with 204,000 internal words compared with a separately written
forward computation, and complete messages hashed by the organizer's code
(Section 7); every lane of the counter batch against the program's own
compression of the real last chunks (9.3); all 2^21 members of Q*, each giving
the difference beta*; the rule t != 0 (Section 8); the program's automata
against brute force at 10 bits (9.3); a participant implementation of the joint
solver against an earlier solver on real walks and on planted instances (9.5);
the free positions, static trees, families and caps of the solver, and the sums
of the cells of (P*) against the counts of 10.1, with a separate count of (P*)
in one phase of 2^16 members (9.4); the run of the verifier of 9.9, which
printed that the guards and counts are exact in all eight phases; the sum
8,912 of the one-path charge and the integers of Section 11; a participant implementation of the batch,
with the mask and the filter of the sub-class, against the program's own
functions (9.6); the program's own tables of the seven-outcome filter, whose
count of passing pairs the self-test recounts (9.3, Section 8); and the word nu of
the pre-check against the bits s[13] to s[15] of 324,098 real trials (9.7);
the submitted program on the root instance against three participant reference
programs and in its self-test, and its pairs against an independent BLAKE3 of
the specification (*The submitted program*, below). For
Sections 1
to 6, three independent reruns, by a checking agent, a reviewing agent and a
participant tool that reads the printed text, found no wrong value in the
displays, Table C and Lemmas Q, Q2, L, A, T2 and T4, and Lemma A was checked by
complete enumeration in three ways: the earlier program on all 2^16 patterns
of the 13 bits of z and the 3 bits of e1 that the rule reads (65,536 packed
words); a second statement of rule and test typed by hand on 4,194,304 inputs;
and seven wrong plans of the test, all of which the program refuses. These are
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
with mean exactly 1/32 of the mean count (Lemma SL).

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

*Rule A in the count.* Of the 317 outcomes, 99 have only solutions that satisfy
rule A, 76 have none that does, and 142 have both. The exact rate with rule A is

    r_A = 6219586146887739/33554432 = 185,358,111.47,

so the rule loses 19,086.08 of r, about one part in 10,000, and the sum over
the 99 outcomes is 12147454997539/65536 = 185,355,453.45, the figure that entry
64c075ac set its H1 against. For beta*, the only part that the claim of this
package uses, the three figures coincide (10.1). On the whole class the same
eight conditions keep 76,072,772.68, less than half, and no outcome there is
free of violating solutions: the rule belongs to this sub-class.

The earlier program also holds the rules of four and six conditions that rule
A contains; it uses only rule A.

**Where the sub-class and the rule come from, and the second count.** Both were
proposed by another AI model, GPT Sol 6.1 (OpenAI), run by the participant with
briefs that asked for exact counting: its answers give this sub-class, r =
194382080300609/1048576, and the eight conditions, r_A =
6219586146887739/33554432, as "best found" by a search over conditions that is
not exhaustive. A second instance of the same model reports the same two
fractions, calls the sub-class the only best of the sub-cubes with 15 fixed
bits of e1, and calls the eight conditions a certified best among all sets of
eight affine conditions on h1. The participant has not checked these two
statements, and nothing the participant has checked shows that no better
sub-class or rule exists. The participant's counter, extended by the sub-class,
agrees with the other model's files on 21 exact fractions, on the rate of every
beta and on 3,243 integers over 1,081 outcomes, with no difference; this was a
recount with those figures at hand, not a blind one.

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
The analysis uses none of this history: it is proved for the values as stated
(Lemma ADV, Section 12).

**Real messages in the root arrangement: what exists.** All of the following
are participant measurements, made for entry 64c075ac in the arrangement of
Sections 4 to 6 (counter 0, flags 11), and summarised here. They bear on the
seven-word model M, on which the counter rate rests as well, and on rule A;
they are not measurements of the counter search or of its budgets.

*Processor.* Every lane of the self-tests of 6.5 is compared with the complete
digests of its two real messages (7,000,000 lanes in the long run, and all
18,725 batches of one value of X2 in one complete outer step). In three runs of
2^30 real trials of the sub-class, rule A passes 2^-8.0019, 2^-7.9992 and
2^-8.0000 of the trials and 0.02617 to 0.02622 of the batches run stage 2,
against 0.0270 for independent trials and a budget of 0.03125 (single contexts
0.0071 to 0.0421); three remeasurements by helper agents gave 0.02617 to
0.02620.

*Layout runs (graphics card, whole class, two-level order).* 24 outer tuples of
2^40 trials, two runs of 2^44 and spreads of X2, of the outer words and of w5,
recounted by a second helper agent. Averaged over outer tuples the counts agree
with the model within their statistical error: rules of four to six conditions
within one part in a million; listed beta +0.73, listed beta and tau +0.83 and
the listed partial E3 event (2^-32.2) -0.24 standard deviations; the listed E1
outcome (2^-40.15) 138 against 152.0 (-1.14). They do not support independence
of the trials inside one outer step: rule shares within one value of X2 are not
binomial (variance 2.7 to 181 times the binomial one), the members of a batch
pass together, and the rate of a listed tau given a listed beta is a property
of the outer tuple (0.02 to 2 times its average), since Y12 and w5 are fixed
inside an outer step. One count is unexplained: 3 listed E1 outcomes where
14.65 are expected in one window of 2^44 trials (Poisson probability 0.0003;
the next window has 16); chance is the likelier reading, and another cause is
not excluded.

*Scaled-down end-to-end runs* (8-bit and 10-bit words, every trial hashed
completely, no rule and no filter, predictions by complete enumeration). In the
two-level order: 436 runs of the first folder, 470 collisions against 467.6
predicted (+0.11 standard deviations; its first job of 92 runs was low, -2.17);
the larger job, with its rule of judgement written down before it ran, 8,448
runs, 8,108 against 8,313.6 (-2.25), 3.3 per cent low with 8-bit words (6,276
against 6,489.6, -2.65) and level with 10-bit words (1,832 against 1,824.0,
+0.19). By that rule only more than 3 standard deviations below the prediction
would speak against the model; the cause of the 8-bit shortfall is not known (a
dependence of the rate of one outer step on its fixed words is one possible
reading, not established). In the order of entry c66f230d: 1,272 planned runs,
345 against 335.76 (+0.50). No run has a failed check or a false collision;
none has a sub-class, rule A or a packed batch.

*Real messages in the order of entry c66f230d (2^49.58 trials, whole class).*
Listed beta -0.76, listed beta and tau -0.07, listed E1 outcomes 692 against
690.78 (+0.05) and partial E3 events -0.53 standard deviations, every run
within 2.2 on every count: support for the model on average at about 2^-40, for
the whole class and not for the sub-class or rule A.

*The sub-class with rule A (graphics card, 2^44.59 trials).* Rule A passes
2^-8.000002 of the trials, and 0.026178 of the packed words enter stage 2,
0.838 of the charge 0.03125. The listed partial E3 event comes at 1.18 times
its whole-class rate (6,314 against 5,353.63), a marker one call deep at 2^-32
that is positively correlated with rule A and is not the counted gain; the
listed E1 outcome comes at 14 against 21.59, a shortfall this run does not
resolve. The kept mass of rule A, 185,358,111.47 of 185,377,197.55, is not
measured. A scaled-down run with a sub-cube and an eight-condition rule (8-bit
words, 30 runs, six of them declared before the first result was read) found
121 collisions against 120.23 (z +0.07): such a selection leaves the collision
rate of the survivors at the exact per-trial count to within 9 per cent, and
says nothing on the kept mass of rule A.

*Chosen and random outer words (sub-class).* Arms chosen for more and for fewer
listed E1 outcomes give 421 against 421.2 and 235 against 226.1, 5.04 standard
deviations apart, as the model predicts: single outer steps of the sub-class
differ from the average by about plus or minus 8.48 per cent in the model's
weighted rate, and random outer steps by about 3.7 to 4.0 per cent, while the
claim uses the average over outer steps. It reaches no collision and does not
measure the factor.

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
are 3.9 to 31.8 on the eight sets, against 853.61 here), and it has no rule A,
no sub-class and no packed batch.

**Real messages in passing outer steps.** A participant measurement made for
this package, untrusted evidence like the two paragraphs before it, which the
organizer's harness does not run. On a graphics card a helper agent ran the
counter construction on real 32-bit messages with Y4 in the sub-class. Uniform
random outer steps, drawn by the measuring program, were filtered by conditions
(1) and (2) with tables generated as the earlier program generates them, and
every passing outer step enumerated the whole of Q*, all 2^21 values of c1 in
the program's member order, as 299,594 words of seven lanes in the layout of
the run-wide table: 2^22.00 passing outer steps, 2^43.00 trials. A control with
the filter off ran 2^18 outer steps, 2^39 trials. On 330 records a check
against the earlier program (step CO, the filter, the member order, rule A
and the word n of the E1 test from the program's compression of the real last
chunks) found no difference. Errors are taken per outer step, because the
trials of one outer step cluster.

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
outcomes of beta*), and as a control the sub-class of entry 26ebba63 with rule
A and the seven-outcome filter. Each run walked 2^35 uniform random outer steps
and enumerated all of Q* in 2^25 of its passing outer steps, 2^46 trials per
class; the passing steps kept are the first in the order of the card's atomic
counter, which does not depend on their content, and the pass share uses every
walked step. Before the runs, the filter tables were compared with the program's
construction, 1,000 members of each class with the member lists, and a sweep of
all 2^32 values of tau and of eps at beta* showed that the counters list
exactly the fourteen and the seven outcomes of 10.1; no trial lacked the
difference beta*. The counters are the E1 outcome and the filter; errors are
clustered by outer step. The model per trial is the sum of L_j over the listed
outcomes times 2^-85 (2^-96 for the triples times 2^11 for c1 in Q*).

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

**The submitted program (experiments/halfsearch.py).** The program of the two
declared experiments is new in this package and replaces the earlier program of
6.5. It is one Python 3 file of 57,864 bytes that uses only the standard
library and imports no BLAKE3 library. It runs the search of 9.1 on the root
instance only: one chunk, counter 0 and flags 11, the instance that the
organizer's harness hashes. It does not run the counter instance (flags 3,
counter t), on which the claim is made. Step 2 runs by the one-success slot of
9.8 by default, in both organizer modes and in the self-test; the option
`--no-slot32` runs the complete traversal of 9.4 instead, the earlier
behaviour, and the declared experiments do not use it. The program was written
by helper agents of the participant from three participant reference programs
of steps CO and CT, the solver and the search, which are not in the package.

*One trial.* Per organizer seed the program runs 256 batches, 1,792 outer
steps, whose eight words come from SHAKE-256 of the text "halfsearch batch",
the seed and the batch number. In order: (1) step 1 of 9.1: the whole-class
sampler; step CO compiled from its lines onto packed words of seven 36-bit
lanes; the automaton of (2) on omega in all seven lanes, then the automaton of
(1) on Y9 (the Q path), with masks restricted to S; an outer step passes when X
is not zero; the E, pass and solver counts against the budgets the program
holds (9.1), which a trial never reaches. (2) The pre-check of 9.7: nu by (V),
then T = X AND VMASK[nu]. (3) Step 2 by 9.8: J from bits 0, 1, 8, 9 and 15 of
the raw eighth word, kept before its AND with fc307cfc; the envelope of m1, the
first of the four sets of 9.8 that contains it; the row and the offset of slot
J in the static ranges of 9.8. A padding slot, or a row not in T, ends the
outer step with no root. Otherwise the row is set up with the guards (a) to
(g) of 9.4, (G7) and the walks of bits 0 to 6, and one path is followed from
the first state at depth 7: a prescribed position takes its one arc, with Lemma
J0 at position 20 and the guards at positions 25 and 29, and the n-th free
position takes one of the two arcs of its dual entry by bit n of the offset.
At depth 32, (J1) to (J3) are checked as words. So a solver step returns at
most one root. (4) Step 3 for every root: c1 by the inverse of Lemma IP, then
the tests in this order: c1 in Q*, the counter word t = 0 of this instance,
the names of steps CO and CT equal to the 2-round compression, (J1) to (J3)
equal to E3 on A and B, the E1 differences, and equal chaining values (here,
equal digests). A root is counted as certified only when every test holds.

*The ledger.* The program counts machine units with the charges of Section 11:
425 per batch (the counted 424 of the packed batch and the move that keeps the
raw word), 35 per lane whose mask of (2) meets S, 512 per passing lane; per
solver step 4,096 and 64 for the selection; 2,304 and 1,280 when a row is set
up; 20 per forced node, the walks of bits 0 to 6 included, 24 at the selected
node, 28 per free node taking one arc, 9 and 4 more at the guard nodes 25 and
29, 1 per arc kept at position 9, 80 per leaf and 288 per root. These are the
program's counts of what it executes, node by node. The time bound of Section
11 does not use them: it charges the whole 8,912 on every outer step that
reaches the solver, whether or not a row is set up.

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
2 seconds and exited with 0: the constants of 9.1 that the program holds; the
automata against brute force at width 8, 256 of 256; SHARE and E_COUNT from the
program's tables; an envelope of 9.8 for every mask of (1); the packed batch
against the scalar step CO on 16,380 lanes, 0 failures and no lane above 36
bits; 424 units per packed batch; the mask of (1) against the (J1) mask, step
CT against the compression, the inverse of Lemma IP, the J words against E3,
the c1 with t = 0, and the half-collision at counter 0 and flags 11, each 256
of 256. An earlier participant run with 1,024 cases and the same seed passed
the same checks, with 65,534 lanes in the packed comparison.

*Other participant checks of the program.* Against the three reference
programs set to flags 11: step CO on 3,000 random outer steps, 0 mismatches;
the solver of 9.4 on 4,000 random inputs, 0 mismatches in roots, counts or
notes; the pipeline on 60,000 batches, the same 421 passes and 115 solver
steps; step 3 on 6,000 constructed roots, the same verdict in every case. The
solver units differ from the reference by design, since the program also
charges the guard nodes, the arcs at position 9 and the walks of bits 0 to 6.
Over 184 set-up (outer step, row) pairs, the paths of all offsets of 9.8
reached exactly the leaves of the complete traversal of 9.4, each once.

*The runs of this package.* Both declared experiments were run locally with 64
organizer seeds each, with the default (the slot of 9.8). The requests were
built by a participant checker, not part of the package, which then hashed
every returned pair with its own BLAKE3, written from the specification with
the round count as a parameter; its 7-round digests equal the published
vectors for "" and "abc".

| 64 seeds, slot of 9.8 | half-collision | residual-search |
| --- | ---: | ---: |
| pairs returned / event met / failed | 64 / 64 / 0 | 64 / 64 / 0 |
| wall time of the 64 trials | 0.3 s | 0.8 s |
| outer steps, 64 trials of 1,792 | 114,688 | 114,688 |
| passing outer steps (share; exact 0.00099146) | 110 (0.0009591) | 118 (0.0010289) |
| solver steps per pass (nominal 1/4) | 0.2636 | 0.2288 |
| solver steps / of them with a row set up | 29 / 13 | 27 / 12 |
| solver units per solver step, mean / max (cap 8,912) | 5,829 / 8,044 | 5,820 / 8,249 |
| units per outer step, outer part (ledger 63.126) | 63.107 | 63.163 |
| units per outer step, steps 2 and 3 (2.209 at the cap) | 1.474 | 1.370 |
| units per outer step, trial (ledger 65.335) | 64.581 | 64.533 |
| member loop per outer step | - | 206.076 |
| members tried, mean (least, most) | - | 367.5 (7, 1,599) |
| over cap, halts | 0, 0 | 0, 0 |
| roots / past Q* and t = 0 / certified | 0 / 0 / 0 | 0 / 0 / 0 |

The ledger figures per walked outer step are those of Section 11 at the
nominal shares: 425 / 7 = 60.714 for the batch, 35 * 2^-4.1998 = 1.905 for the
Q path and 512 * 2^-9.9782 = 0.508 for the pass, 63.126 together, and 8,912 *
2^-11.9782 = 2.209 for steps 2 and 3 at the cap, 65.335 in all. With every
budget plus one, Section 11 charges 65.624 per walked outer step. The measured
outer part agrees with the ledger; steps 2 and 3 use about 65 per cent of their
allowance on average (5,829 / 8,912), and no solver step exceeded the cap, the
largest at 93 per cent of it. With the complete traversal of 9.4 (option
`--no-slot32`), the participant's earlier runs of 256 seeds per experiment,
made with an earlier version of the file whose trial walked 114,688 outer
steps (16,384 batches; a trial of the file now walks 1,792), returned 512
pairs, all meeting the event, with 8,314 and 8,302 solver units per
solver step on average and at most 14,178, against that traversal's cap of
31,456; one root (trial 214 of `residual-search`) was found and stopped at the
test c1 in Q*, its forced t being 10e104cf.

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

**What does not exist.**

- No organizer-run check of the counter instance: an experiment of the harness
  tests events of complete digests, and the half-collision of the counter
  instance lies in the chaining value of a chunk that is not the root (6.4,
  Section 7). Its checks are participant computations with the organizer's
  functions imported (Section 7) and the earlier program's self-test (9.3).
- No measurement of the joint event of H1', at about 2^-91 per trial. The
  deepest counter events measured are the listed E1 outcome at 2^-31.7 and that
  outcome together with rule A, 55 events at about 2^-39.8.
- No proof that the construction's trials have the joint law of the model
  words, or of the share of the success mass that the rule t != 0 removes.
  These are the open parts that the rate of H1' declares (10.3). No bound on rho
  for the construction's own outer steps is proved or assumed: the search does
  not need one (Lemma SL).
- No proof that the shares of the three counts of H4' for the sampler equal their
  nominal shares; they are measured (H4', above). No measurement in passing outer
  steps deeper than the listed E1 outcome at about 2^-31.7 per trial, and no
  separate count of the E1 rate of the six outcomes of S: it is a sub-event of the
  measured seven.
- No run of the counter search with the outer filter, the solver or the slot
  selection, scaled down or not; the toy run has none of them. The submitted
  program runs them on the root instance only, for 1,792 outer steps per
  trial, and has found no root that reached the test t = 0.
- No complete message of a found pair; the complete messages hashed (Section 7)
  are trials, with t from 1 to 16,383.
- The count of the class, 71,698,432 with fourteen outcomes, and its six rows of
  67,633,152 that this package lists are reproduced by Section 17. The
  analysis uses no list of values of beta.
- The search of 9.1 on the counter instance exists only in this text. The
  submitted program runs its member in the class, its outcome set S, its batch
  of seven outer steps in lean lanes, the pre-check of 9.7, the selector and
  the one-path solver of 9.8 with the guards of 9.4 and (G7), and step 3, on the
  root instance, with the factor and SHARE of 9.1 but the run length and
  budgets of entry 0bc5f130, which its trials never reach (9.1). No
  implementation of the solver, the slot selection, the lean lanes, the
  pre-check or the guard (G7) in the layout and the 64-register schedule of 9.4,
  9.8 and Section 11 has been run (9.5); the program counts the rows of Section
  11 as a ledger. The verifier of the guards (9.9) has been run. Every row of
  Section 11 is bounded in words, apart from the counted 400 and 295 of 9.6.

**Limits of the evidence.**

- H1' is an assumption. The factor is set against a count under M with c1
  conditioned in Q*; the count does not show that M holds, and Lemma S1 is a
  statement inside M. Lemmas S2 to S4 prove parts of the transfer to the
  construction, not the joint law of the seven words. H1' has no dependence
  part: the slots make the certified count of an outer step 0 or 1 with an exact
  mean (Lemma SL).
- M fails inside one context and one outer step: in the root arrangement for
  rule A and for the call E1, and in the counter arrangement for rule A, whose
  count per outer step has a variance 572 times its mean. Where it was measured
  it holds on averages over outer steps. The counter search fixes Y4, Y9, w8,
  Y12 and w5 for the 2^21 trials of an outer step, so the success of a run
  rests on many independent outer steps, 2^74.460 walked, about 2^64.48 of them
  passing and 2^62.48 reaching the solver. How the successes cluster inside one
  outer step does not enter the bound: each outer step certifies at most one,
  with the exact mean of Lemma SL, at the price of a run about 32 times as long
  as one that counted every success.
- The shares of the three counts of H4' are measured, not proved equal to their
  nominal shares: on the whole class 0.9980 +- 0.0041 of pi, 1.0004 +- 0.0005 of
  p_E and 1.0123 +- 0.0082 of p_3 on 60,000,000 real outer steps. The quarter
  share of the pre-check is an exact share of a model with nu uniform, not a
  property of the sampler. Lemmas F and VP need no law of the words, and the time
  bound needs none either, since the budgets halt the run.
- The model is checked on real messages to about 2^-40, not at 2^-91.
  Scaled-down whole-collision runs are level for the counter arrangement
  (0.94 +- 0.13 of the predicted gain) and, for the root arrangement, level at
  10 bits and 3.3 per cent low at 8 bits in the largest job.
- The constants and the class were chosen by the count, and beta* with them,
  so they favour any choice that the model overrates; S was chosen by the charge
  of the complete traversal (Section 12).
  The part of the six outcomes of S that this package lists is 41.7 per cent of
  the count of the class and rests on six outcomes with one value of eps. Most
  measurements of this section are on the sub-class and the seven outcomes of
  entry 26ebba63; on the whole class the E1 side of those seven outcomes, which
  contain S, was measured (2^46 trials), and their E3 side was not.
- The count rests on programs that are not in the package and on a list of
  values of beta that is complete only by uncertified solver answers and the
  other model's enumeration; the other model reconciled the records and did not
  recount them.
- H4' concerns three run totals; single outer steps differ strongly. A reached
  budget halts with failure, which lowers the success probability and not the
  time bound.
- Every row of Section 11 is bounded in words by GPT Sol's schedules on 64
  registers, built on the earlier program's counts of the outer step of the
  sub-class (9.3) and a participant recount of it; no row is a count of an
  executed program on that machine. The submitted program's counts apply the
  units of these rows to what it executes on the root instance; they are not
  counts of the 64-register machine.
- The messages of a found pair have about 2^41 bytes on average and fewer than
  2^42; computing their digests costs about 2^37 compressions, which is
  charged, and no check of this package computes them.
- Helper agents of the participant wrote and checked the counter construction,
  the filter and this text, and another AI model proved Lemmas IP, F, S1 to S9
  and SL, wrote the verifier of 9.9 and derived the count of passing pairs; no
  person has read it.

**Approaches tried that did not improve this path.** Each is a negative result
for this family, not a general one: inside-out solving of the residual with
redundancy (at 2^32 per unit it needs redundancy one, and the complete known
sets start at two); a SAT solver per trial forcing further conditions (0.6 to
6.0 seconds or no answer, against about seven operations per trial); forcing a
second condition by a coupled block of equations (at least 0.7 bit lost);
bit-level steering and neutral bits for the first test (no zero-loss skip
exists); table lookups prescribing a second word, and loops of more than two
levels (no fewer per-trial equations); other absolute values of the pinned
constants (better by one part in a million at most); the four-active fork (best
complete trail 253 against 100, worse by evidence and not by proof); better
pinned constants in the same length family (none found by GPT-6 Luna on the
owner's server); other message-length families (estimated at 101.3 to 107, each
needing its own package); two "knob" words fixing first-stage bits (false on
2,000 real trials; from a model reached through the service Venice); and a
constant chunk counter (the trials are only relabelled; the gain of this
package comes from solving t per trial, Section 8). Where no other source is
named they were proposed by the participant, its helper agents or GPT Sol 6.1,
and run by helper agents.

**Scope and limitations.**

- No full collision is exhibited; this is an analytical cost claim like other
  packages on this track and, unlike a birthday search, tests each trial
  against zero, needing no memory that grows with the trials.
- The messages have 1024 t + 55 and 1024 t + 63 bytes, with 1 <= t < 2^32 the
  solved chunk counter, about 2^41 bytes on average. They rely on the chunk
  counter and the true block length being inputs of the compression, as the
  target profile specifies; the colliding compression is that of the last
  chunk, which is not the root, and Lemma TR carries the collision to the
  complete digests in the profile's own tree mode. The 63-byte last chunk ends
  in eight zero bytes, and both zero-filled last blocks have words 14, 15 and
  the top byte of word 13 zero.
- The gain over a birthday search comes from matching half the chaining value
  by construction, constants that let the other half match usefully, the
  prescription of c1 in the cube of beta* that the solved counter makes
  possible, assumed at 98,937,639,497 times the uniform rate, work shared per
  outer step, the outer filter, which skips all but about one outer step in
  2^9.98 without losing any success with an outcome of S, the pre-check, which
  skips the solver in about three passing outer steps of four without losing any,
  and the solver, which follows the path of one static slot of an outer step
  without enumerating its trials: 2^95.460 trials walked, at most 2^85.482 of
  them in passing outer steps and 2^83.482 in outer steps that reach the
  solver, not 2^128 (about 2^131.986 at the uniform rate, with the slots). The
  slots keep 1/32 of the mean number of successes and cost a factor of about 32
  in walked trials against a search that certifies every success; in exchange
  the success bound needs no premise on how the successes of one outer step
  cluster.
- A brief literature search found free-start collisions and near-collisions of
  reduced BLAKE compression functions and no collision attack on 2-round
  BLAKE3. No priority or novelty claim is made.
- The time bound charges every operation, load and store of the machine of
  Section 11, with 64 registers and constants as immediate operands, every row
  at the budget at which the run halts, each as bounded in words by the
  schedules of Section 11: an upper bound under that convention, not a measured
  time, and checked by no organizer run. The layout of the one-path solver and
  its cap of 8,912, the slot selection, the guard (G7), the lean lanes and the
  pre-check are proved allowances of a schedule that is not implemented. Its
  largest term is the search part; all computation that produced the advice is
  charged as P = 2^70 / 430 units (Section 12), 2^-10.496 times it, under the
  supporting heuristic HPRE (10.3).

**Field meanings.**

- time_log2 = 71.7491 bounds total charged time by 2^71.7491 units (Section
  11): log2 T = 71.74901350873373..., checked in integers (T^10000 <
  2^717491); the search is below 2^71.74802 units and the preprocessing P is
  2^70 / 430 units. The search part is worst case for the algorithm
  as stated: every budget halts the run and is charged at its value plus one,
  and steps 2 and 3 cost at most 8,912 in every outer step that reaches them;
  no premise enters it. P is the bound of the supporting heuristic HPRE on all
  computation that produced the advice (10.3, Section 12); were that bound
  2^72 operations, the claim would be 71.7521.
- memory_log2_bytes = 44 bounds the search with its code (below 2^29 bytes),
  the advice (73 bytes), the output (below 2^43 bytes) and the recorded memory
  of the discovery (all attested device memory, below 2^41 bytes), even all held at once: their sum is
  below 2^44 (Section 12).
- preprocessing_log2 = 61.2519 is P = 2^70 / 430 target-compression units
  (2^70 primitive word operations), log2 P = 61.25180715... rounded up at the
  fourth decimal, charged for all computation that produced the advice, the
  counts that derive the numbers of 9.1 from it included. Its basis is the
  supporting heuristic HPRE: the peak rates of the devices that the
  participant attests, over a window of 30 days, give below 2^69.740 charged
  operations (Section 12). The participant's records of the search, at most
  1,066,018 core-seconds, are context, not its basis. The success bound does
  not use it.
- nonuniform_advice_log2_bytes = 7 bounds the advice of Section 12, 73 bytes,
  by 128 bytes: the six constants, eta, beta* with the mask and value of its
  cube, the seven values of tau with eps of the outer filter's automata and the
  mask of S. The submitted program stores no word of the sub-class or of rule
  A, and the 93 bytes of the earlier program with those words are below 128 as
  well (Section 12). The slot ranges are computed from the rows and are not
  advice.
- success_probability = 0.39 holds under the rate of H1' and the three budget
  clauses of H4', for the stated advice (Lemma ADV), as shown in 10.4: 1 -
  exp(-0.49512) - 0.0005 = 0.3900022... It uses no clause on the dependence of
  the successes of one outer step (Lemma SL) and no statement about how the
  advice was found.
- heuristics: H1prime-rate (score-critical, the mean rate only),
  H4prime-pass-budget (supporting, the three budget clauses of this run) and
  HPRE-discovery-bound (supporting, the bound on all computation that produced
  the advice, which enters only P).

The required baseline_improved identifier blake3-r2-nominal-v2 names the
organizer's nominal display reference 128, not an established attack, qualified
baseline or security bound; 71.7491 is below it. Whether a qualified result
improves the Yukon incumbent is decided separately; no Pareto dominance claim
follows.

## 14. Corrections to our entry c66f230d

Entry c66f230d (time_log2 97.6) cannot be edited. After it was filed its text
was examined by a hostile review of another AI model (Grok 4.7), by a referee
report of another AI model (GPT Sol 6.1) and by an audit of a helper agent of
the participant that had written nothing of it. Twenty-four points were raised;
none changes a lemma, the count or the scalar of that entry, or a figure of its
claim block, and the corrected wording is used in this package wherever the
passage recurs. The full list, with the filed wording beside the corrected one,
is in the work folder of entry 64c075ac. Two of the points bear on this text.
H1 was not implied by the model M alone, since it also assumed that the good
trials of a run do not come in clusters; here H1' is a rate only, and the
search certifies at most one trial per outer step with an exact mean (Lemma
SL). The declared preprocessing did not bound the selection of the constants,
of eta and of rule A; here the values are stated advice, and all computation
that found them is charged as P under HPRE (Section 12). That entry also said
it had no scaled-down end-to-end run for this pair of lengths; Section 13
reports the runs made since.

## 15. What is the same as earlier entries, what is new, and the labelled history

*The same as earlier entries of the participant.* From entry 64c075ac: the
target, the two block lengths with the zero words they force, the six constants
and Fact P, Lemmas L and H, the class of eta = 830303cf with Lemmas Q, T and N,
the sub-class with Lemma Q2 and rule A with Lemma A (kept by the root instance,
not used by this search), the root instance of Sections 4 to 6 with the machine
of 6.5, the ids, kinds and masks of the two declared experiments, the
seven-word model, the method of the count, the solver search that found the six
constants (Section 12), and the form of H1, here H1'. From entry e7b17fd1:
Section 8 (Lemmas TR, CT and IP, Theorem C), the counter batch of 9.2 with
Lemma CB, the cube Q* of beta*, and Lemmas S1 to S5 and S8. From entry
26ebba63: the outer filter with Lemmas F and S9, the joint roots of 9.4 with
Lemmas V and CV, the walk over independent outer steps with the pass budget as
a halt, the factor of H1' at five sevenths of the count, and the rate clause of
H1' and H4', here for the whole class, S and this run. From entry 59f8915e: the
whole class with no sub-class and no rule, the guards (PHASE), (P*) and Lemma
J0, the arrays and families of the solver, the lanes of 9.6 with Lemmas PL and
PB, the machine of Section 11, and the records of the search that found the
advice (Section 12), apart from the choice of S. From entry 0bc5f130: S and its
count 67,633,152, the factor 98,937,639,497, Lemmas VP and G7, the lean lanes,
the three budget clauses of H4' with the margin 17/16, the static trees of the
solver, the charges 35 per Q path and 512 per passing lane, and the choice of S
(Section 12).

*History, labelled: entry 78ac164c.* Entry 78ac164c (71.7481) was the previous
filing of this package, with the same search, rate clause, budgets and run. It
declared a third premise, HSEL-selection-return, that a capped selection
procedure SEL returns the six constants, eta, beta* and S that the search
reads, and charged the cap of SEL, 8,882,224,365,081,579,520 operations, as
preprocessing. The review ruled it not_evaluable on HSEL, since exact checks of
the stated values do not establish that SEL returns them and no organizer
experiment replays SEL. This filing states the values as fixed advice of 73
bytes and proves the success bound for them as stated (Section 12, Lemma ADV);
HSEL is not declared, and all computation that found the values is charged as P
= 2^70 primitive word operations under HPRE (10.3). Replacing the cap by P
raises log2 T by 0.00099, from 71.74802 to 71.74901, and the claimed bound from
71.7481 to 71.7491 (Section 11). The figure 71.7481 belongs to that entry and
to this labelled history only.

*History, labelled: entry 0bc5f130.* Entry 0bc5f130 (66.8751), the filing of
this design before entry 78ac164c, certified every listed good trial of an
outer step that reached the solver, by the complete traversal of 9.4 at a cap
of 31,456 machine units, with RUN_STEPS = 2^69.465 for 0.49676 expected listed
good trials. Its H1' had a second part, a dependence clause with the sufficient
condition rho = E[N_o (N_o - 1)] / E[N_o] <= 0.0065 per outer step (Lemma S8),
declared and neither proved nor measured; a clause of the same kind was found
unsupported in the review of another entry. This package drops that clause,
certifies at most one trial per outer step by a static slot with an exact mean
(9.8, Lemma SL), and pays with a run about 32 times as long. The figure 66.8751
belongs to that entry and to this labelled history only; it is not a claim of
this package.

*New against entry 0bc5f130* (GPT Sol, answer BA 1.3, 1.4 and 2): the selector
J from five bits of the eighth random word that nothing else reads (one more
move per batch, 425 units); the 32 static slots and the one-path solver of 9.8,
with Lemma SL and its cap of 8,912 machine units; H1' as a rate only and the
success bound 1 - exp(-0.49512) - 0.0005 = 0.3900022... (10.4); the run of
RUN_STEPS = 2^74.460 outer steps, 31.89 times that entry's, with its three
budgets; and the verifier of 9.9, run by the participant, which certifies
(PHASE) and (P*) for every joint root in all eight phases. Also new: the
submitted program of the two declared experiments (Section 13), which replaces
the earlier program of entries 26ebba63, 59f8915e and 0bc5f130. The claimed
bound rises from 66.8751 to 71.7491: the run is 2^4.995 times as long, the
cheaper solver step gives back part of it, and P adds 0.0010. Against entry
26ebba63 (71.39, reviewed plausible_not_refuted, with a dependence clause for
the sub-class with rule A) it is higher by 0.3591, with no dependence clause.
The chunk counter solved per trial of entry e7b17fd1, which makes one more
round-1 word prescribable, is new on this track as far as the participant
knows.

## 16. Credit

The contest is cooperative and this package builds on the work of others. Each
is named for what they did. Apart from the helper agents of the participant,
nobody named here has reviewed this package, and a credit is not an endorsement
by the person or model credited.

- **The participant who filed entry dd91b2f6** on this track (built on entry
  47804be2 of this participant): dropping the sub-class and rule A in the
  solver design, because rule A only served the enumeration of the cube, so
  that y ranges over the whole class of eta; and the observation that the
  counting program of Section 17, run on the class, gives fourteen outcomes of
  beta* with part 71,698,432, of which this package lists six. This package
  uses neither the program, nor the sample, nor the premises of entry dd91b2f6.
  That participant has not reviewed this package.
- **winglock**, a participant on this track: the idea of searching only a
  sub-class of the members, chosen by an exact count per member (entry
  18a7fc52, to the participant's knowledge also the first public count of the
  model rate without sampling); the sub-class of the root instance follows
  winglock's choice in entries 2125212 and 2bb5d604. The search of this package
  uses no sub-class.
- **Th0rgal**, a participant on this track: building the values that depend on
  the member alone once per outer step and not once per trial, first published
  in entry df8bd46d (the arrangement of the root instance was derived later,
  with that entry known); and three coding steps of 6.5 (entry 8c81a219): one
  stored constant w12 - S1 - S6 across two calls, the rotation by one bit with
  one mask, and an order of the operations that frees registers.
- **5kyguy**, a participant on this track: keeping masks in registers across
  the loop over the members (entry 404d14df).
- **tekkac**, a participant on this track: the lane layout of 6.5, seven 36-bit
  lanes with a masked rotation (public ticket 2bf40fb); the same lanes carry
  the seven outer steps of the batch of 9.6.
- **GPT Sol 6.1 (OpenAI)**, an AI model run by the participant. For the root
  instance: the sub-class, the eight conditions of rule A, the exact fractions
  of the rates, and the referee report on entry c66f230d (Section 14); a second
  instance: a further count of the two fractions and the statements on
  optimality quoted in Section 13. For the counter search: Lemmas IP and S1 to
  S8, the reconciliation of the outcomes of beta* with the count records, the
  ranking of the 53 values of beta, and the wording of the open part as a
  premise (H1'); AC: Lemmas F and S9 and the certificate of the pass share; AI,
  AL, AN, AO, AQ, AR and AT: the solver of 9.4 for the class (transition
  relation and arrays, register traversal and allowances, phase guards, (P*),
  Lemma J0, the ledger of the static trees), the filter certificate for
  fourteen outcomes, the packed lanes of 9.6 with their proof and charges, and
  the lean lanes; AW: Lemma VP, the three budgets with their nominal shares and
  the union clause of H4', and the choice of S over all 16,383 sets; AX 1: the
  guard (G7) with Lemma G7; BA: the 32 slots and the one-path solver of 9.8
  with Lemma SL and its charges, the price and run length of the one-path form,
  and the all-eight-phase verifier of 9.9, which the participant ran.
- **Grok 4.7 (xAI)**, an AI model run by the participant: the hostile review of
  entry c66f230d (Section 14), and a tightened batch for the first form of the
  two-level program, which agrees with the batch of 6.5 in idea and is not a
  batch of this package.
- **A model reached through the service Venice**: a statement on prior art and
  an argument that fixing single bits of message words does not help the first
  test. Both are unverified, and nothing of them is used in a proof or a figure
  of this package.
- **Helper agents of the participant**, instances of the same AI model as the
  author of this text: the order of Section 4, the programs and their tests,
  the counts of Sections 13 and 17, the first form of Lemmas T2 to T4, the
  measurements and scaled-down runs of Section 13 with their checks, and the
  audit of entry c66f230d; the finding that a chunk counter solved per trial
  makes E1.d1 prescribable next to Y4, the order of Section 8 and an
  independent check of the tree mode with the organizer's code; the outer-step
  filter (proposed, built and measured) and the s-pattern pre-check (9.7); the
  recount of the selection records (Section 12) and the pricing of the subsets
  of the outcomes; the checks of (P*) and of the free positions, trees and caps
  (9.4, Section 11); the batch of 9.6; the run of the verifier of 9.9; the
  price of Section 11 in integers; the submitted program with its checks and
  runs (Section 13); and this text.

The half-collision, the class search and the two tests are those of the
participant's earlier entries 17bba2ae, 5ceb1802, 04638ed8, c47c1a80, c66f230d
and 64c075ac on this track.

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
