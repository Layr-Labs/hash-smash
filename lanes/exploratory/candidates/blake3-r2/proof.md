# A last-chunk half-collision and a chunk-counter search for 2-round BLAKE3, on the winner sub-class

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a separately reported resource bound.

**Which section governs.** This entry is the chunk-counter search of Sections 8 and 9 run on one phase of the class of eta, the *winner sub-class* (b, u, v) = (1, 0, 1): the 2^16 members y with e1 =
Y3 + y = 070c0307 + (W AND f8107cf8). Section 18 defines it and governs: its member, the count of its rate, its budgets, its two premises, its numerator, its advice record, its preprocessing charge
and its limits. The claimed scalar is time_log2 = 75.4218 (Section 18.7), with success probability at least 0.3919693 under the two premises of Section 18.5. Sections 1 to 17 are the base text on the
whole class of eta (all 2^19 members), which was not filed as an entry. Everything in them that Section 18 uses, the construction, the tree lemma, the filter of fourteen outcomes, the joint solver
with its guards and its cap of 56,096 machine units, the packed batch and its charges and the lemmas of Section 10, holds on the winner sub-class as stated there (Section 18.2). The whole-class
figures of those sections, FACTOR, RUN_STEPS, PASS_BUDGET, RUN_BATCHES, the premises H1' and H4' in their whole-class form, the success bound 0.390000993950 and the time bound 69.3343, are history:
they are kept for reference and are not claimed. Where a figure of Sections 1 to 17 differs from one of Section 18, Section 18 governs.

History (the base text of the whole-class search; this filing is the winner search of Section 18): this exploratory package targets blake3-r2-prefix-v1. It has an exact part and a heuristic part, and
it keeps them apart. It is the search of entry 26ebba63 (time_log2 71.39), itself the counter search of entry e7b17fd1 (84.98) with an exact filter on the outer steps (Section 8) and a joint solver
that finds the successes of a passing outer step without enumerating its trials (Section 9), run here on the whole class of eta: there is no sub-class and no rule A, the filter and the solver cover
all fourteen outcomes of beta* on the class, and the heuristics are the two of entry 26ebba63, H1' and H4', restated for this search (10.3). Dropping the sub-class and rule A is the step of entry
dd91b2f6 of another participant (Section 16). The joint solver reads its guards from an exact parity certificate of the class, (P*), and from a guard on the third addition of E3, Lemma J0, and has a
proved cap of 56,096 machine units in every passing outer step (9.4); the outer steps are drawn seven to a batch of eight fresh 256-bit words, as independent outer steps with the law of one drawn
alone (9.6); and every budget is charged at its bound on a machine with 64 registers and constants as immediate operands (Section 11). The layout of the solver, its cap and the schedule on 64
registers are GPT Sol's (answers AL, AO, AQ and AR) and are proved upper allowances, not an implementation: no implementation of this solver has been run (9.5). The package continues entry 64c075ac
(92.53) of the same participant with the same block lengths and six constants, without the clusters of that entry. Section 14 corrects the text of entry c66f230d, Section 15 says what is the same as
entries 64c075ac, e7b17fd1 and 26ebba63 and what is new, and Section 16 credits the people and models whose work is used.

**Exact part.** An explicit construction maps seven 32-bit words, a member y of the class of eta, a set of 524,288 values, and one more word c1 to a number t and to a 55-byte string A and a 63-byte
string B. When t is not zero, F || A and F || B, with F a string of t full chunks of 1,024 bytes, are messages of 1024 t + 55 and 1024 t + 63 bytes whose last chunks are A and B, and the 2-round
compressions of these last chunks, with chunk counter t and flags 3, give chaining values that agree on their words 0, 2, 5 and 7, that is on 128 of their 256 bits. There is no search in this and no
probability: it holds for every choice (Sections 7 and 8). In the organizer's tree mode the digest of such a message depends on F and on the chaining value of its last chunk alone (Lemma TR), so a
pair whose last-chunk chaining values agree in all eight words is a collision of two complete messages. The number t is not chosen: it is the chunk counter that the round-0 call K0 reads, solved per
trial as t = ROL(K0.d1,16) XOR K0.a1. It takes up the freedom of the message word w0, and that is what lets the construction prescribe c1, the third value of the round-1 call E1, next to y. The search
holds c1 inside the set Q* of the 2^21 words for which the first-half b difference of E1 is beta* = 18b0e098, the difference of the solution with which the constants were found (Section 12).

**Heuristic part.** A collision needs the other four words of the chaining value to agree as well. The algorithm of this entry (Section 18.3) draws B = 52,256,980,094,639,195,695,325 = 2^75.468
proposals (outer steps) at random, seven to a batch, each with a member of the winner sub-class and 2^21 trials. An exact filter, two carry automata on two words of the outer step, skips every outer
step that cannot hold a collision with the fourteen outcomes of the counted rate (Lemma F); it passes 2^-7.5320 of uniform pairs of words. Only a passing outer step is searched further: a joint
solver, one depth-first traversal over the bits of one internal word with guards that exact counts of the class prove lossless, returns every value of that word that meets the conditions of one of the
fourteen outcomes, and a certificate maps each back to its trial and tests it. Together they find exactly the trials of the outer step that complete the collision with one of the fourteen outcomes, at
a cost of at most 56,608 machine units whatever its words (Section 9, Lemmas V and CV). Every budget is a halt and is charged at its bound; no mean of any count enters the time bound. Two premises on
the success are declared, both for the law of the winner sub-class (Section 18.5): H1prime-winner, that a proposal holds on average at least (2^21 - 1) * 5 * 9297 / (7 * 2^104) valid trials (t not
zero) that complete the collision with one of the fourteen outcomes, five sevenths of the exact model rate 9297 / 2^104 per trial of the winner sub-class, a rate premise only (the no-hit bound follows
from the proved cap Zwin <= 72 of Lemma CV); and H4prime-winner, that the pass budget suffices. Under the two the search succeeds with probability at least 0.3919693. The search is charged below
2^75.42169 target-compression units. The values that the search reads, the six constants, eta, beta* with its cube, the fourteen outcomes and the winner phase, are a fixed nonuniform advice record of
124 bytes printed in Section 18.6; by Lemma ADV the claim uses only properties of that record that this text proves or counts exactly, and no premise states how it was found. The computation that
found it is charged as preprocessing, 2^70 primitive word operations (2^70 / 430 units, below 2^61.252), under a third declared premise, HPRE-discovery-bound, which bears on the time bound only
(18.6). The total, 2^75.42176509..., is below 2^75.4218: the claimed scalar is 75.4218 (Section 18.7). The search needs less than 2^29 bytes of memory; its two messages are shorter than 2^42 bytes
each, and the declared 2^44 bytes cover them, the code, the advice and the search, even all held at once (Sections 12 and 18.8).

The rate in H1' is an assumption. (This paragraph states the whole-class rate of the base text; the rate of this entry, that of the winner sub-class, is counted in Section 18.4 from the same cells.)
Under the seven-word model of Section 13, with Y4 uniform in the class, prescribing c1 in Q* multiplies by 2^11 the part of beta* in the rate of the class: the rate is 2^11 * 71,698,432 =
146,838,388,736 times 2^-128, which is 904.92 times the model rate of a trial of the class, and the conditioning leaves the law of the other call, E3, unchanged (Lemma S1, proved by another AI model,
GPT Sol 6.1). The figure 71,698,432 is the sum of fourteen exact outcome counts of the participant's counting program, printed with its output in Section 17. Whether the trials of the construction
realise that conditional law, to at least 5/7 of its rate, is the part that is not proved, and it is declared as H1'; Lemmas S2 to S4 prove parts of it, and Lemma S8 states how weak the dependence
inside one outer step has to be. Participant measurements on real counter trials reach events of probability about 2^-31.7 and agree with the model, and a scaled-down end-to-end run with real
collisions of complete messages realises the predicted gain of the prescription at 0.94 +- 0.13 of its value (Section 13). No run reaches a collision at 32 bits. With the uniform rate, and not
104,884,563,382 times it, the same search needs about 2^126.991 walked trials and gives time_log2 = 105.95 (a whole-class figure of the base text, history).

No full 2-round collision is exhibited, and the search is far beyond feasible computation. The two declared experiments run the root instance of the same construction: single chunks of 55 and 63
bytes, compressed with counter 0 and flags 11 (Sections 4 to 6). An organizer experiment tests an event on the two complete digests, and the half-collision of the counter instance lies in the chaining
value of a chunk that is not the root, which the parent and root compressions above it mix: no digest experiment can show it (Section 6.4). What the experiments exhibit, and what the organizer's
runner checks, is the exact half-collision of the root instance and a toy-scale search over the sub-class. The program the organizer runs is that of entry 26ebba63, unchanged: the earlier version of
this search, on the sub-class. It also contains the counter construction, its counted batch, and the outer filter and the walk over outer steps of the sub-class search of that entry, with its seven
outcomes and its constants, a machine that counts their operations and loads, and a self-test of the batches and the filter (Sections 6.5 and 9.3), whose counts and checks the organizer does not
check. The member, the fourteen-outcome filter, the constants, the batch of seven outer steps, the joint solver with its layout, and the charge of the search of this package are defined in this text
(Sections 8, 9 and 11); the layout of the solver and its schedule on 64 registers are proved allowances and are not implemented.

## 1. Exact complete hash on the messages used

H is unkeyed BLAKE3-256 with only rounds 0 and 1 kept in every compression. Every message of the root instance (Sections 4 to 6) has n = 55 or n = 63 bytes. A message of n <= 64 bytes is one chunk
consisting of one block, with no parent node, so H evaluates exactly one compression. The block is the message followed by 64 - n zero bytes, used only for loading words. The compression has flags
CHUNK_START | CHUNK_END | ROOT = 11, true block length n, and chunk counter and root-output counter both zero. There is no key and no derivation flag.

Decode the zero-filled block into sixteen little-endian 32-bit words w[0..15]. The IV is

    6a09e667 bb67ae85 3c6ef372 a54ff53a
    510e527f 9b05688c 1f83d9ab 5be0cd19.

Initialize v[0..7] = IV, v[8..11] = IV[0..3] and v[12..15] = (0, 0, n, 11). The block length n is the initial value of v[14] and enters nowhere else. All additions and subtractions on state and
message words are modulo 2^32. ROR and ROL rotate a 32-bit word. G(a,b,c,d,x,y) is

    v[a] = v[a]+v[b]+x;  v[d] = ROR(v[d] XOR v[a],16)
    v[c] = v[c]+v[d];    v[b] = ROR(v[b] XOR v[c],12)
    v[a] = v[a]+v[b]+y;  v[d] = ROR(v[d] XOR v[a],8)
    v[c] = v[c]+v[d];    v[b] = ROR(v[b] XOR v[c],7).

A round is four column calls followed by four diagonal calls on the current schedule s, and between rounds s is replaced by s[P[i]] with P = (2,6,3,10,7,0,4,13,1,11,12,5,9,14,15,8). Written out for
the two retained rounds, with names used throughout:

    round 0   K0 = G(0,4,8,12, w0, w1)     K1 = G(1,5,9,13, w2, w3)
              K2 = G(2,6,10,14, w4, w5)    K3 = G(3,7,11,15, w6, w7)
              D0 = G(0,5,10,15, w8, w9)    D1 = G(1,6,11,12, w10, w11)
              D2 = G(2,7,8,13, w12, w13)   D3 = G(3,4,9,14, w14, w15)
    round 1   C0 = G(0,4,8,12, w2, w6)     C1 = G(1,5,9,13, w3, w10)
              C2 = G(2,6,10,14, w7, w0)    C3 = G(3,7,11,15, w4, w13)
              E0 = G(0,5,10,15, w1, w11)   E1 = G(1,6,11,12, w12, w5)
              E2 = G(2,7,8,13, w9, w14)    E3 = G(3,4,9,14, w15, w8)

S denotes the state after K0..K3, X the state after round 0, Y the state after C0..C3 and Z the final state. The compression output is o[i] = Z[i] XOR Z[i+8] and o[i+8] = Z[i+8] XOR IV[i] for i =
0..7. The digest H(m) is the first 32 output bytes, LE4(o[0]) || ... || LE4(o[7]).

This is the complete hash of the target profile restricted to inputs of 55 and 63 bytes: standard IV, standard flags, true block length, both retained rounds with the standard permutation, standard
feed-forward and the full 256-bit digest. It is not a free-start, chosen-IV, compression-only or truncated-output setting.

*The same compression in a last chunk.* Sections 7 to 9 use the same compression, with the same names, as the compression of the last chunk of a longer message: there v[12..15] = (t mod 2^32, t >> 32,
n, 3), with the chunk counter t and the flags CHUNK_START | CHUNK_END = 3, and the output words o[0], .., o[7] are the chaining value of the chunk (Lemma TR). Nothing else changes: the IV, the block,
the two rounds and the output.

## 2. Inverting one G call

Consider one call G(a,b,c,d,x,y) with input values A, B, C, D and name its eight assignments

    a1 = A + B + x           d1 = ROR(D XOR a1, 16)
    c1 = C + d1              b1 = ROR(B XOR c1, 12)
    a2 = a1 + b1 + y         d2 = ROR(d1 XOR a2, 8)
    c2 = c1 + d2             b2 = ROR(b1 XOR c2, 7).

Its outputs are (a2, b2, c2, d2). The values a1, d1, c1, b1 are called the first, second, third and fourth value of the call, a2 the fifth, and so on.

**Fact 1.** Reading the assignments backwards,

    b1 = ROL(b2, 7) XOR c2       c1 = c2 - d2       d1 = ROL(d2, 8) XOR a2
    B  = ROL(b1, 12) XOR c1      C  = c1 - d1
    a1 = ROL(d1, 16) XOR D       y  = a2 - a1 - b1      x = a1 - A - B.

Each line is one assignment solved for another of its terms. A set of words A, B, C, D, x, y, a1, d1, c1, b1, a2, d2, c2, b2 is the execution of one call exactly when the eight assignments hold, in
whatever order and for whichever of their terms they were solved. The constructions below use nothing else: every line of theirs is one assignment of one call, solved for the name on its left.

## 3. Three ingredients

**3.1 The length is cancelled inside K2.** K2 is the only call of round 0 that reads the block length n, the initial value of v[14], and it overwrites that word; it is also the only call of round 0
that reads w4 and w5. Its inputs are (IV[2], IV[6], IV[2], n). Put K = IV[2] + IV[6] = 5bf2cd1d. For lengths 55 and 63, whose XOR is 8, define for any w4, w5

    w4' = ((K + w4) XOR 8) - K        w5' = w5 + w4 - w4'.

**Lemma L.** K2 with block length 55 and words (w4, w5) leaves the same four state words as K2 with block length 63 and words (w4', w5').

Proof. Let a1 = K + w4. In the second execution the first assignment gives K + w4' = a1 XOR 8, so the second gives ROR(63 XOR a1 XOR 8, 16) = ROR(55 XOR a1, 16) because 63 XOR 8 = 55: the same d1. The
third and fourth depend only on d1 and constants. The fifth gives (a1 XOR 8) + b1 + w5' = a1 + b1 + w5 because w5' - w5 = w4 - w4' = a1 - (a1 XOR 8). The last three depend only on values already shown
equal. QED.

Hence two messages of 55 and 63 bytes that share every word except w4, w5, related as above, have the same state S after the column step and the same state X after round 0, since no other call of
round 0 reads v[14], w4 or w5 before K2 has made the states equal.

*Which words must be zero.* For both messages to be honest byte strings of their lengths with the same words w6..w15, the bytes 55 to 63 of the block must be zero in both. In the 55-byte message they
are zero fill. In the 63-byte message bytes 55 to 62 are its last eight bytes, which are chosen to be zero, and byte 63 is zero fill. Byte 55 is the top byte of w13, bytes 56 to 59 are w14 and bytes
60 to 63 are w15. So the family needs

    w14 = 0,   w15 = 0,   top byte of w13 = 0,

and nothing else: bytes 0 to 54 are free in both messages.

**3.2 A pinned call C3.** Fix the six constants

    X3 = 29d4fa98   X7 = bee3af28   X11 = 44036000   X15 = 40c58500
    W4 = 97475638   W13 = 0007c006

The top byte of W13 is zero. K + W4 = f33a2355 and W4' = ((K + W4) XOR 8) - K = 97475640, so W4 - W4' = fffffff8, that is -8 modulo 2^32. Evaluate C3 = G(3,7,11,15, w4, W13) on the inputs (X3, X7,
X11, X15) with w4 = W4 and with w4 = W4':

    w4 = W4    a1=7ffffff8 d1=7af83f3a c1=befb9f3a b1=01200183
               a2=8127c181 d2=bbfbdffe c2=7af77f38 b2=76f7aefd
    w4 = W4'   a1=80000000 d1=8500c0c5 c1=c90420c5 b1=fed77e78
               a2=7edf3e7e d2=bbfbdffe c2=850000c3 b2=76f7aefd

**Fact P.** The two executions give the same d output bbfbdffe and the same b output 76f7aefd. They differ in the a output (8127c181, 7edf3e7e) and in the c output (7af77f38, 850000c3). This is a
finite computation on the displayed constants.

**3.3 Half of the digest does not see the difference.**

**Lemma H.** Take two executions of the 2-round compression that have the same state X after round 0 and the same message words except w4 and w5. Suppose (X[3], X[7], X[11], X[15]) = (X3, X7, X11,
X15), w13 = W13, and w4 is W4 in the first execution and W4' in the second. Then the two digests agree on digest words 0, 2, 5 and 7.

Proof. C0, C1, C2 read neither w4 nor w5 and act on identical states, so they leave identical values in both executions. C3 reads state words 3, 7, 11, 15 and the words w4, w13; by Fact P it leaves
the same v[7] and v[15] in both executions and may differ only in v[3] and v[11]. So Y agrees except possibly in Y[3] and Y[11]. E0 reads Y[0], Y[5], Y[10], Y[15] and w1, w11. E2 reads Y[2], Y[7],
Y[8], Y[13] and w9, w14. None of these is Y[3], Y[11], w4 or w5, so E0 and E2 produce identical outputs Z[0], Z[5], Z[10], Z[15] and Z[2], Z[7], Z[8], Z[13]. Finally o[0] = Z[0] XOR Z[8], o[2] = Z[2]
XOR Z[10], o[5] = Z[5] XOR Z[13] and o[7] = Z[7] XOR Z[15] use only those eight words. QED.

The remaining digest words o[1] = Z[1] XOR Z[9], o[3] = Z[3] XOR Z[11], o[4] = Z[4] XOR Z[12] and o[6] = Z[6] XOR Z[14] are computed from the outputs of E1 and E3 only. The **residual** of a pair is
the 128-bit string R = (o[1] XOR o'[1], o[3] XOR o'[3], o[4] XOR o'[4], o[6] XOR o'[6]). The pair is a collision exactly when R = 0.

## 4. Construction: the message from eight words, in three levels

This section, Section 5 and Section 6 build the root instance of the construction, whose messages are single chunks compressed with counter 0 and flags 11 (Section 1). The counter instance, which the
claim uses, is built in Section 8 from the same constants (6.4).

The construction places the six constants of 3.2 where Lemma H needs them and gives Y4, the b output of C0, a prescribed value y. Its input is eight free words. Six form an *outer step*: C0.c1 and
C0.d1 (the third and the second value of the round-1 call C0), D3.d1 (the second value of the round-0 call D3), S15 and S9 (words of the state S) and the message word w5. The seventh is X2, a word of
the state X; with it the six are a *context*. The eighth is y. X3, X7, X11, X15 are the constants, w4 = W4, w13 = W13 and w14 = w15 = 0.

*Names.* TAG.a1, TAG.d1, TAG.c1, TAG.b1 are the first to fourth value of the call TAG (Section 2); its outputs carry the names of the state S, X or Y they are written to; entry c66f230d writes vc, vd,
vb, va for C0.c1, C0.d1, C0.b1, C0.a1. Arithmetic is modulo 2^32. The submitted program has steps O and M in `outer` and `middle` ("Step S1" of entry c66f230d), step Y in `member`, step T in `trial`.

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

**Step S2.** w4' = W4' and w5' = w5 + W4 - W4', all modulo 2^32. For the constants of 3.2 that is w5' = w5 + fffffff8, the same as w5 - 8.

**Step S3.** A is the first 55 bytes of the little-endian encoding of w0..w15; B is the first 63 bytes of that of the same words with w4', w5' for w4, w5.

*Round 1, forwards (24 lines).* The tests of 6.3 read these values of round 1 of message A. Y3 and Y11 are the constants of Fact P for w4 = W4, and Y4 = y.

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

These 24 lines define nothing of the message. E3.h1, E3.g1, E3.f1, E3.e2 are the h1, g1, f1, e2 of 6.2, and the word z of Lemma A is C2.d1 XOR Y2.

**The order and the levels.** The 29 + 21 + 10 + 12 + 24 = 96 lines above are taken in the printed order. Lines of step O are *outer*, of step M *middle*, of step Y *table* lines; the 12 lines of step
T and the 24 of round 1 are the 36 *trial* lines. Table C gives each call's eight assignments by their left sides.

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

The inputs, message words and outputs of the eleven calls are those of Section 1 for n = 55: Ki (i = 0..3) maps (IV[i], IV[i+4], IV[i], d) with d = 0, 0, 55, 11 to (S[i], S[i+4], S[i+8], S[i+12]);
D0..D3 map (S0, S5, S10, S15), (S1, S6, S11, S12), (S2, S7, S8, S13), (S3, S4, S9, S14), and C0..C2 map (X0, X4, X8, X12), (X1, X5, X9, X13), (X2, X6, X10, X14), to the X and the Y words of the same
indices.

**Lemma T2.** (a) *Triangular.* In the printed order every line assigns a name that no earlier line assigns and that is neither one of the eight words nor a constant, and it reads only constants, the
eight words (the eighth under the name Y4 in the lines of round 1) and names of earlier lines. A line of step O reads no word other than the six of the outer step, a line of step M reads neither y nor
a name of step Y, and a line of step Y reads neither X2 nor a name of step M. Every line is one assignment of one call, solved for the name on its left; the two exceptions are the lines for E1.b1 and
for E3.h1, each of which is two assignments with the first substituted into the second (c1 = Y11 + E1.d1 and e1 = Y3 + Y4 + w15), and the line for E3.e2 uses the same e1. By Table C the 96 lines are,
each exactly once: the eight assignments of each of the eleven calls K0..K3, D0..D3, C0..C2, with the inputs and the message words of Section 1 for block length 55, with w4 = W4, w13 = W13, w14 =
w15 = 0, and with the constants X3, X7, X11, X15 as the a output of D3, the b output of D2, the c output of D1 and the d output of D0; and the first five assignments of E1 and of E3 for message A.

(b) *The calls.* For every choice of the eight words, the names of steps O, M, Y and T are the executions of the eleven calls as listed after Table C, each with its two message words; C0 has first,
second, third and fourth value C0.a1, C0.d1, C0.c1, C0.b1 and outputs (Y0, y, Y8, Y12); and E1.a1, E1.d1, E1.b1, E1.a2 and E3.h1, E3.g1, E3.f1, E3.e2 are the first, second, fourth and fifth value of
E1 and the second, third, fourth and fifth value of E3 in the compression of message A.

(c) *The levels.* An outer line is a function of the six words alone. A middle line is a function of the six words and X2 and does not depend on y. A table line is a function of the six words and y
and does not depend on X2. In particular the sixteen message words of two trials of one context differ at most in w8, w9, w10, w11.

(d) *Admissible blocks.* Call a block (w0, .., w15) *admissible* if w4 = W4, w13 = W13, w14 = w15 = 0 and round 0 on it with block length 55 ends with (X[3], X[7], X[11], X[15]) equal to the four
constants. The map of this section from the eight words to the block of A is a bijection onto the admissible blocks.

Proof. (a) is read off the displays, each formula compared with Section 2 and its call's inputs, outputs and message words; Table C has one name in each of its 88 cells, all different, and with the
eight of E1 and E3 they are the 96.

(b) An assignment solved for one of its terms is an equivalent equation modulo 2^32 (Fact 1), so a line's assignment holds once it has run, and by (a) no later line changes its names. By (a) and Table
C all eight assignments of each call hold, a constant output in its place (lines D3.b1, X14; D2.b1; D1.c1, X6; D0.d1, X10) and y as the b output of C0 (line Y8); by Fact 1 the names are the execution
of the call. The E1 and E3 lines are those of 6.2 for message A with Y11, Y3 of Fact P, run forwards from A's Y1, Y6, Y12, Y4, Y9, Y14.

(c) By induction over the printed order, with (a): an outer line reads only constants, the six words and outer lines; a middle line in addition only X2 and middle lines; a table line in addition only
y and table lines. w6, w7 are outer and w0..w3, w12 middle lines, w5 is one of the six words, w4, w13, w14, w15 are constants; only w8..w11 are trial lines.

(d) By (b), round 0 with block length 55 on an output block leaves the state X of the names, with the constants as X[3], X[7], X[11], X[15], and the pinned words are constants: the block is
admissible. *Injective:* by (b) each of the eight words is a value in the compression of A, so a function of the block. *Onto:* the forward values of an admissible block (block length 55) satisfy
every equation of (a): they execute the calls, the constant outputs hold by admissibility, and C3 has the inputs X3, X7, X11, X15, W4, W13, so Y3, Y11 are those of Fact P. Run on the eight words taken
from them, each line returns the forward value of its name, by induction, since an assignment has exactly one solution for any one term given the others. So the lines return the block. QED.

*The same pairs as entry c66f230d.* That entry builds the block of A from the eight words (vc, vd, S11, S4, X13, X14, w0, y) by 72 lines, the assignments of the nine calls K0..K3, D0..D3, C0 in
another triangular order (its Lemmas S, F and Y). By the argument of (d) both are bijections onto the same admissible blocks and B is determined by A: the 2^256 pairs are the same, in another order;
only which of them a run visits, and in which groups, differs. This remark is not used in any proof below.

*What Lemma T2 does not say.* Eleven of the trial lines are the line for E3.h1 and the ten it depends on (X0, D0.d1, D0.c1, X10, C2.a1, C2.d1, C2.c1, C2.b1, Y2, Y14). That no order with fewer exists
was the answer of a solver in the search that produced the order; it is not used here and not claimed.

## 5. The half-collision

**Theorem.** For every choice of the seven words of a context (C0.c1, C0.d1, D3.d1, S15, S9, w5, X2) and of the word y, steps O, M, Y, T, S2 and S3 output two distinct messages A and B, of 55 and 63
bytes, whose complete 2-round digests agree on digest words 0, 2, 5 and 7; and in both compressions the b output of C0 is Y4 = y.

Proof. The sixteen words of steps O, M, Y and T have w14 = w15 = 0 and w13 = W13, whose top byte is zero. So bytes 55 to 63 of their encoding are zero: A, the first 55 bytes, is an honest 55-byte
message whose zero-filled block is the sixteen words, and B is an honest 63-byte message that ends in eight zero bytes and whose zero-filled block is the sixteen words with w4, w5 replaced (3.1). Run
round 0 on the words of A with block length 55. By Lemma T2 (b) the column calls leave the state S of the names and the diagonal calls, which act on disjoint state words, leave the state X of the
names. So the state after round 0 has (X[3], X[7], X[11], X[15]) equal to the four constants, and w4 = W4, w13 = W13. By Lemma L the compression of B has the same state X after round 0. The two
compressions share every word except w4, w5, so Lemma H gives the four digest words. C0 reads X0, X4, X8, X12 and w2, w6, which are the same in both compressions, and has b output y by Lemma T2 (b).
The messages are distinct because their lengths differ. QED.

Distinct choices of the eight words give distinct messages A: C0.c1 and C0.d1 are values inside C0, D3.d1 is a value inside D3, S15 and S9 are state words after the column step of round 0, w5 is a
message word, X2 is a state word after round 0 and y is a state word after the column step of round 1, and all of them are functions of the message (Lemma T2 (d)). The construction yields 2^256
different half-colliding pairs.

## 6. The root instance: trials, tests and the counted batch

**6.1 Trials.** A *context* is the six words of an outer step (C0.c1, C0.d1, D3.d1, S15, S9, w5), a word X2, and everything that steps O and M compute from them. The class and the sub-class defined
next are sets of values of Y4. A **trial** is a context and a member y of the sub-class; its messages A and B are the output of steps O, M, Y, T, S2 and S3 for the context's seven words and y. Only
steps Y and T depend on y: the trials of one context differ in the four message words w8..w11 and in nothing else of the message (Lemma T2 (c)). Step Y does not depend on X2: for one outer step and
one member its ten names are the same for all 2^32 values of X2. The table of 6.5 rests on this.

*The class.* The first message word of E3 is w15 = 0, so the first assignment of E3 is e1 = Y3 + Y4 for message A and e1' = Y3' + Y4 for message B, with Y3 = 8127c181 and Y3' = 7edf3e7e from Fact P.
Put DY3 = Y3' - Y3 = fdb77cfd. The second assignment is h1 = ROR(Y14 XOR e1, 16), so the XOR difference between A and B of E3's first-half d value is

    eta = h1 XOR h1' = ROR((Y3 + Y4) XOR (Y3 + Y4 + DY3), 16),

a function of Y4 alone. Fix eta = 830303cf. The *class* is the set of all words Y4 that give this eta.

**Lemma Q.** The class is the set of all Y4 with

    ((Y3 + Y4) AND 03cf8303) = 030c0303.

It has 524,288 members: the 19 bits of e1 = Y3 + Y4 at the positions where 03cf8303 has a zero are free, bit 31 among them, and Y4 = e1 - Y3.

Proof. Put x = ROL(eta,16) = 03cf8303, which has no bit 31. Y4 is in the class exactly when e1 XOR (e1 + DY3) = x, that is when (e1 XOR x) - e1 = DY3 modulo 2^32. For words e and x, (e XOR x) - e is,
modulo 2^32, the sum over the bits i of x of 2^i where bit i of e is 0 and of -2^i where it is 1, which is 2 ((NOT e) AND x) - x. So the condition is 2 ((NOT e1) AND x) = DY3 + x = 01870000 modulo
2^32. As (NOT e1) AND x has no bit 31, the doubling is exact and the condition is ((NOT e1) AND x) = 01870000 >> 1 = 00c38000. All bits of 00c38000 lie in x, so this fixes the 13 bits of e1 on x to
(e1 AND x) = (NOT 00c38000) AND x = 030c0303 and leaves the other 19 bits free. QED.

*The sub-class.* The search uses only the members of the class whose e1 = Y3 + Y4 has bit 21 and bit 26 equal to zero. With Lemma Q that is the set of all Y4 with

    ((Y3 + Y4) AND 07ef8303) = 030c0303.

**Lemma Q2.** The sub-class is a subset of the class and has 131,072 members: the 17 bits of e1 at the positions 2 to 7, 10 to 14, 20 and 27 to 31, where 07ef8303 has a zero, are free, and Y4 = e1 -
Y3.

Proof. 07ef8303 = 03cf8303 OR 04200000, and 04200000 has the bits 21 and 26, which are two of the 19 positions that Lemma Q leaves free. The value 030c0303 has zeros at both. So the condition is the
condition of Lemma Q together with bit 21 = bit 26 = 0, and 17 positions stay free. QED.

Member number k of the sub-class, for 0 <= k < 131072, is the Y4 whose e1 has the bits of k at its 17 free positions, in increasing order of position. From here on "member" means a member of the
sub-class. A part of the class is searched and not all of it because, under the model of Section 13, the rate of collisions differs from member to member and is higher on this part. Nothing exact
depends on that.

**Lemma T.** For every context and every member y of the class, and so for every member of the sub-class, the messages A and B of the trial are distinct messages of 55 and 63 bytes whose complete
2-round digests agree on digest words 0, 2, 5 and 7; in both compressions Y4 = y; and the XOR difference between A and B of E3's first-half d value is eta = 830303cf.

Proof. The first two statements are the theorem of Section 5. In both compressions w15 = 0 and Y14 is the same, the a input of E3 is Y3 for A and Y3' for B by Fact P, and Y4 = y is a member of the
class, so the difference is eta by the definition of the class. QED.

**6.2 The residual of a trial.** With Y3, Y3', Y11, Y11' the a and c outputs of C3 from Fact P (8127c181, 7edf3e7e, 7af77f38, 850000c3), delta = W4 - W4' = fffffff8 and the trial's words and state:

    (.., Y4, .., Y12) = C0 = G(X0, X4, X8, X12, w2, w6)
    (Y1, .., Y9, ..)  = C1 = G(X1, X5, X9, X13, w3, w10)
    (.., Y6, .., Y14) = C2 = G(X2, X6, X10, X14, w7, w0)
    E1 on A:  G(Y1, Y6, Y11,  Y12, w12, w5)
    E1 on B:  G(Y1, Y6, Y11', Y12, w12, w5 + delta)
    E3 on A:  G(Y3,  Y4, Y9, Y14, w15, w8)
    E3 on B:  G(Y3', Y4, Y9, Y14, w15, w8)

and R is formed from the eight output words of E1 and E3 as in 3.3. Y4 = y and Y12 are known from step Y without evaluating C0 forwards. Write a1, d1, c1, b1, a2, .. for the assignments of E1 and e1,
h1, g1, f1, e2, h2, g2, f2 for those of E3 in the order a, d, c, b; a prime marks message B.

**6.3 Two tests of a trial.** The algorithm uses two tests: rule A, a condition on one word of E3 (Lemma A), and the E1 test, a 32-bit condition on E1 alone (Lemma N). The early test of the first
entries on this track (Lemma E of entry c66f230d) is not used and is not restated.

**Lemma N.** For a trial of 6.1 put beta = b1 XOR b1' and eps = c2 XOR c2', both taken from E1, and

    n = eps XOR ROL(beta XOR eps, 1) XOR eta.

Let D3 and D6 be the XOR differences between A and B of digest words 3 and 6, which are the second and the fourth word of R. Then n = D3 XOR ROL(D6, 8) for every trial. In particular R = 0 implies
n = 0.

Proof. Digest word 3 is Z[3] XOR Z[11], the a output of E3 and the c output of E1, so D3 = (e2 XOR e2') XOR eps. Digest word 6 is Z[6] XOR Z[14], the b output of E1 and the d output of E3, so D6 = (b2
XOR b2') XOR (h2 XOR h2'). In E1, b2 = ROR(b1 XOR c2, 7), so b2 XOR b2' = ROR(beta XOR eps, 7). In E3, h2 = ROR(h1 XOR e2, 8), and h1 XOR h1' = eta for every Y4 in the class (Lemma T), so h2 XOR h2' =
ROR(eta XOR e2 XOR e2', 8). Rotating D6 left by 8 gives ROL(D6, 8) = ROL(beta XOR eps, 1) XOR eta XOR (e2 XOR e2'). The XOR with D3 cancels e2 XOR e2' and leaves n. QED.

A trial *passes the E1 test* when n = 0. The word n needs the first seven assignments of E1 for both messages and nothing of E3, whose eta is the constant of the class.

*Rule A.* Let h1 be the second value of E3 on message A, as in 6.2, and write h[i] for bit i of h1, bit 0 being the lowest. A trial *satisfies rule A* when all of the following hold:

    h[0] = 0;    h[1] = 1;    h[16] = 0;    h[17] = 0;
    h[2] XOR h[10] = 1;    h[3] XOR h[11] = 1;
    h[3] XOR h[12] XOR h[24] = 0;    h[6] XOR h[13] XOR h[25] = 0.

Each of the eight conditions contains a bit that no other contains (bits 0, 1, 16, 17, 10, 11, 12 and 13), so they are independent and a uniform word satisfies rule A with probability 2^-8. The first
four are the first four conditions of the rule of entry c66f230d; the other four replace its fifth condition (bits 2 and 3 of h1 differ), which is not part of this rule.

**Lemma A.** Write z[i] and e[i] for bit i of the words z and e1 defined next.

(a) For a trial of 6.1 let z = C2.d1 XOR Y2 be the XOR of the second and the fifth value of C2, and e1 = Y3 + Y4. Then ROL(h1, 24) = z XOR ROL(e1, 8): h[i] = z[(i + 24) mod 32] XOR e[(i + 16) mod 32].

(b) For every Y4 in the sub-class, the trial satisfies rule A exactly when

    z[24] = 0;    z[25] = 1;    z[8] = 1;    z[9] = 1;
    z[26] XOR z[2] = 0;    z[27] XOR z[3] = e[27];
    z[27] XOR z[4] XOR z[16] = e[28];   z[30] XOR z[5] XOR z[17] = 1 XOR e[29].

The bits 27, 28 and 29 of e1 are free in the sub-class, so the last three right sides depend on the member.

(c) Let Z be a word of 36 bits or a lane of a packed word of 6.5 whose low 32 bits are z; its bits 32 to 35 and the neighbouring lanes may hold anything. Form the word y by

    s = (Z << 12) AND 0003c000;    y = Z XOR s;
    s = s << 12;                   y = y XOR s;
    s = (y << 13) AND 40010000;    y = y XOR s,

the shifts being shifts of the whole packed word and each mask word holding the printed value in every lane (6.5). Write y[i] for bit i of the lane. Then

    y[8] = z[8];    y[9] = z[9];    y[24] = z[24];    y[25] = z[25];
    y[26] = z[26] XOR z[2];    y[27] = z[27] XOR z[3];
    y[16] = z[16] XOR z[4] XOR z[3];    y[30] = z[30] XOR z[17] XOR z[5].

Put ALL = 4f010300, the word with the bits 8, 9, 16, 24, 25, 26, 27 and 30. For a member of the sub-class let v be the word with

    v[8] = 0;    v[9] = 0;    v[24] = 1;    v[25] = 0;    v[26] = 1;
    v[27] = 1 XOR e[27];    v[16] = 1 XOR e[27] XOR e[28];    v[30] = e[29]

and zeros elsewhere. Then the trial satisfies rule A exactly when (y XOR v) AND ALL = ALL.

(d) Put u = (y XOR v) AND ALL. Then u + (2^32 - ALL) is at most 2^32, and its bit 32 is 1 exactly when the trial satisfies rule A.

Proof. (a) The sixth assignment of C2 is Y14 = ROR(C2.d1 XOR Y2, 8) = ROR(z, 8), and the second assignment of E3 is h1 = ROR(Y14 XOR e1, 16). So h1 = ROR(z,
24) XOR ROR(e1, 16), and rotating left by 24 gives the claim.

(b) By (a) the eight conditions read: z[24] XOR e[16] = 0; z[25] XOR e[17] = 1; z[8] XOR e[0] = 0; z[9] XOR e[1] = 0; z[26] XOR e[18] XOR z[2] XOR e[26] = 1; z[27] XOR e[19] XOR z[3] XOR e[27] = 1;
z[27] XOR e[19] XOR z[4] XOR e[28] XOR z[16] XOR e[8] = 0; z[30] XOR e[22] XOR z[5] XOR e[29] XOR z[17] XOR e[9] = 0. The bits 0, 1, 8, 9, 16, 17, 18, 19, 22 and 26 of e1 lie in the mask 07ef8303 of
Lemma Q2, so they have the same value for every member of the sub-class: in 030c0303 the bits 0, 1, 8, 9, 18 and 19 are 1 and the bits 16, 17, 22 and 26 are 0. Inserting these values gives the
conditions on z. Bit 26 is fixed only in the sub-class, not in the class.

(c) On one lane: in Z << 12, position p holds bit p - 12 of the same lane for 12 <= p <= 35, and the mask 0003c000 keeps the positions 14 to 17, so the first s holds z[2], z[3], z[4], z[5] there and
nothing else. The second s holds the same four bits at the positions 26 to 29, still inside the lane; so y[26] = z[26] XOR z[2], y[27] = z[27] XOR z[3], and the positions 3 and 17 hold z[3] and z[17]
XOR z[5]. In y << 13 the mask 40010000 keeps the positions 16 and 30, which hold those two bits; after the third step y[16] = (z[16] XOR z[4]) XOR z[3] and y[30] = z[30] XOR (z[17] XOR z[5]). The
positions 8, 9, 24 and 25 never change. Every bit that entered one of the eight positions is a bit 2, 3, 4, 5, 8, 9, 16, 17, 24, 25, 26, 27 or 30 of the lane itself: no bit above 31 and no bit of
another lane. That proves the eight equations. A position of v holds a 1 exactly where the right side that (b) requires is 0, so bit t of y XOR v is 1 exactly when y[t] has the required value. At the
positions 8, 9, 24, 25, 26 and 27 these are six of the conditions of (b) as they stand, at 30 the eighth, and at 16 it is y[16] = e[27] XOR e[28], the XOR of the sixth and the seventh condition,
because y[16] = (z[27] XOR z[3]) XOR (z[27] XOR z[4] XOR z[16]). When the sixth holds, that one holds exactly when the seventh does. So all eight positions of ALL hold a 1 in y XOR v exactly when all
eight conditions of
(b) hold.

(d) u has no bit outside ALL, so u <= ALL, and u + (2^32 - ALL) >= 2^32 exactly when u = ALL; the sum is at most 2^32. By (c), u = ALL exactly when the trial satisfies rule A. QED.

*What Lemma A does not say.* Lemma A says that the word of (c) tests rule A exactly. It does not say that a collision satisfies rule A, and that is not true in general: there are solutions of R = 0
with Y4 in the sub-class whose h1 violates rule A. Rule A is therefore a filter that can lose solutions: a word of seven trials in which no trial satisfies it is dropped, whether or not one of its
trials has a zero residual. How much it loses is answered in Section 13: inside the sub-class the rule keeps all but 19,086.08 of the 185,377,197.55 counted, and for the difference beta* that the
counter search uses it keeps all of it, 67,698,688 of 67,698,688, because in every outcome of beta* every solution satisfies rule A (10.1). On the whole class the same eight conditions would keep less
than half of the count; the rule is a rule for this sub-class only.

**6.4 The root instance and the two declared experiments.** Sections 4 to 6 build the *root instance* of the construction: its messages are single chunks of 55 and 63 bytes, and the colliding
compression is the root compression, with counter 0 and flags 11 (Section 1). The claim of this package is made for the *counter instance* of Sections 7 to 9, whose messages have 1024 t + 55 and 1024
t + 63 bytes and whose colliding compression is that of the last chunk, with counter t and flags 3. The two instances share the six constants, Fact P, Lemmas L and H, the class, Lemma N and the
machine of 6.5; the sub-class, rule A and Lemma A belong to the root instance and to the program's counter batch (9.2), not to the counter search of this package. The instances differ in the counter
and the flags that the compression reads, and in the order in which the construction solves the assignments of rounds 0 and 1 (Sections 4 and 8).

The two declared experiments run the root instance of the same construction, counter 0 and flags 11. An experiment of the organizer's harness returns pairs of complete messages and tests an event on
their two digests, while the half-collision of the counter instance is an agreement of four words of the chaining value of a chunk that is not the root. The parent and root compressions above that
chunk mix all eight words, so the digests of a counter pair are not expected to agree on the masked words, and on two counter pairs with t = 1 they do not (Section 7). No digest experiment can show a
half-collision of a non-root chunk's chaining value. In the root instance the colliding compression is the root itself, so its half-collision is an agreement of four digest words, which the organizer
recomputes.

- `half-collision` runs one trial of 6.1 per organizer seed: the seven words of a context and a member number are taken from the seed, and steps O, M, Y, T, S2 and S3 of Section 4 build the pair.
  Lemma T predicts that every pair agrees on digest words 0, 2, 5 and 7.
- `residual-search` runs a search of the root instance at toy scale: per organizer seed one context, then the members of the sub-class in the order of their numbers from a member number taken from the
  seed, at most all 131,072 of them, stopping at the first trial whose residual (3.3) has a zero low byte in digest word 1. For the same context it also evaluates the four counted pieces of 6.5 on the
  program's machine and returns their counts as observations.

Neither experiment runs the counter construction or its batch, and neither measures a rate of the counter search. A search of the root instance over all contexts is not part of the claim, and this
text defines no loops, ranges or budgets for it.

**6.5 Seven trials in one word.** A packed word holds seven lanes of 36 bits at bit offsets 0, 36, .., 216. A lane represents its value modulo 2^32; bits 32..35 are carry guards. A constant is placed
in all seven lanes before the batches that use it. Additions are single 256-bit additions. A rotation of every lane by r is the five operations

    PROR(z, r) = ((z >> r) AND A_r) OR ((z << (32-r)) AND B_r)

with A_r selecting the low 32-r bits of every lane and B_r the next r bits; the masks discard guard bits and bits shifted in from the neighbouring lane, so the result is reduced below 2^32. With M =
2^32 - 1 in every lane, the complement of the low 32 bits of a lane is an XOR with M, a difference x - y of a constant x and a lane y is (y XOR M) + (x + 1), and subtracting a constant y is one
addition of the constant -y.

The lane layout, seven 36-bit lanes with reduction delayed to the rotations and a five-operation masked rotation, follows the public ticket 2bf40fb on this track, which uses it for a birthday search.
What is evaluated in the lanes here is different.

*The two lists.* List word j holds the members 7j, .., 7j + 6 in the order of their numbers; list word 18,724 holds the numbers 131,068 to 131,071, and the last of them three times more. For list word
j, U[j] holds ROL(y, 7) and V[j] the word v of Lemma A (c), one member y per lane, member 7j + i in lane i. Each list has 18,725 packed words, because 131072 = 18,724 * 7 + 4. Both lists are computed
once, from eta, the two bits of the sub-class, Y3 and the rule (Lemmas Q2 and A). The build of the table reads U; stage A of a batch reads V.

*The words of an outer step.* Step O is run with every value in all seven lanes, and 21 words are stored, each below 2^32 in every lane, in the form in which the later pieces load them:

- loaded by the build of the table (7): C0.b1, -C0.c1, -C0.b1 - w6, -X4, ROL(C0.d1,16), S6, -S11;
- loaded by the middle step (8): -D2.b1 - W13, ROL(X13,8), -S2 - S7, S9 + 1, 1 - S6, D2.c1 + 1, ROL(S4,7), w7;
- loaded by a batch (6): S10 + X15, X14, X13, X9, w5, w5 + delta.

*The table of an outer step.* Five lists of 18,725 packed words each, built once per outer step from U, the seven words above and the word C0.d1 of the context. For list word j and lane i, with y the
member of that lane and the names of step Y:

    Y12[j] = Y12        XA[j] = C0.a1 - X4        X6[j] = X6
    X1[j]  = X1         R[j]  = ROL(D1.d1, 16)

all modulo 2^32 and below 2^32 in every lane. The build computes, in every lane:

- C0 backwards: Y8 = U[j] XOR C0.b1; Y12 = Y8 + (-C0.c1), reduced and stored; Y0 = ROL(Y12,8) XOR C0.d1; C0.a1 = Y0 + (-C0.b1 - w6); XA = C0.a1 + (-X4), reduced and stored; X12 = C0.a1 XOR
  ROL(C0.d1,16).
- D1 backwards: D1.c1 = (X12 XOR M) + (X11 + 1), which is X11 - X12; D1.b1 = ROR(D1.c1 XOR S6, 12); X6 = ROR(D1.b1 XOR X11, 7), stored; D1.d1 = D1.c1 + (-S11); X1 = ROL(X12,8) XOR D1.d1, reduced and
  stored; R = ROL(D1.d1,16), stored.

*The words of a middle step.* Step M is run in all seven lanes, and nine words are stored: X2 itself; the seven words that a batch loads, X2 + w7, -w2, w0, S5, w3, S12 and w12 - S1 - S6; and w1, which
no batch loads (it is a word of the message).

*What a batch computes.* The seven trials of a batch share a context and are seven consecutive list places. Stage A computes in every lane:

- D0, as far as C2 needs it: X0 = XA[j] + (-w2); D0.d1 = X0 XOR ROL(X15,8); X10 = D0.d1 + (S10 + X15), the third value S10 + D0.d1 plus X15 in one addition.
- C2 to z: its first value C2.a1 = X6[j] + (X2 + w7), its second, third and fourth value, the fifth as the first plus the fourth plus w0, and z, the XOR of the fifth and the second.
- Rule A: the word y of Lemma A (c) from z, u = (y XOR V[j]) AND ALL, the sum u + (2^32 - ALL) of Lemma A (d), and whether its bit 32 is set in some lane.

If it is set in no lane, the batch ends. Otherwise stage 2 computes:

- The entry count: the number of words that have run stage 2 is advanced and compared with the memory word `stage-2 budget`. In the program that word holds the constant STAGE_2_BUDGET, the budget E of
  the counter search (9.1); in the root instance its value has no influence on any output.
- C2, rest: z and the third value of C2 are formed again; Y14 = ROR(z, 8); and Y6 from the third value plus Y14 and the fourth value.
- D0, rest, and C1 to Y1: D0's third value as X10 + (-X15), D0.b1 with S5, and X5; C1's first value X5 + X1[j] + w3, its second, third and fourth value; D1.a1 = R[j] XOR S12; and the sum of C1's first
  value, its fourth value and D1.a1, which is Y1 + S1 + S6, since w10 = D1.a1 - S1 - S6.
- E1 on A and B: a1 as that sum plus Y6 plus the stored w12 - S1 - S6; d1 = ROR(a1 XOR Y12[j], 16); c1, c1', b1, b1', a2, a2', c2, c2', with Y11' and w5 + delta for B.
- The E1 test: eps = c2 XOR c2', beta XOR eps, the word n of Lemma N, and whether n is zero in some lane.

Nothing of E3 is evaluated in a batch: rule A is a condition on E3.h1, but by Lemma A it is tested on z, a value of C2, with the bits of e1 folded into the constants and into the list V. The words
w8..w11 are never formed in a batch.

**Lemma T4 (the table).** Fix the six words of an outer step, and let the memory hold the 21 words that step O stores for them. (a) For every list word j the build stores the five words displayed
above: in lane i, the values Y12, C0.a1 - X4, X6, X1 and ROL(D1.d1,16) of the member of that lane, each below 2^32. (b) These five words do not depend on X2. (c) For every value of X2, every list word
j and every lane, the lines of a batch that read a table word compute names of the trial (the six words, X2, the member of the lane):

    X0 = XA[j] - w2                          C2.a1 = X6[j] + X2 + w7
    C2.b1 = ROR(X6[j] XOR C2.c1, 12)         C1.a1 = X5 + X1[j] + w3
    D1.a1 = R[j] XOR S12                     E1.d1 = ROR(E1.a1 XOR Y12[j], 16).

Proof. (a) The ten lines of the build are the ten lines of step Y in the packed forms of this section: U[j] is ROL(y,7), an addition of a stored word -v is the subtraction of v, and (X12 XOR M) +
(X11 + 1) is X11 - X12 modulo 2^32 in a lane. No sum leaves its lane (below), so the low 32 bits of every lane are the scalar value; the words stored after a sum are reduced by an AND with M, and R
and X6 are rotation outputs. XA is C0.a1 plus the stored -X4. (b) Y12, C0.a1, X6, X1 and D1.d1 are table lines and X4 is an outer line, so by Lemma T2 (c) none depends on X2. (c) The six equations are
the lines for X0, C2.a1, C2.b1, C1.a1, D1.a1 and E1.d1 of Section 4 with the words of (a) in place of the names: XA[j] - w2 = C0.a1 - X4 - w2, R[j] XOR S12 = ROL(D1.d1,16) XOR S12, and the other four
contain X6, X1 and Y12 as they stand. QED.

*The machine, and which words are kept in registers.* The pieces run on a load/store machine with 16 registers. One operation is charged for every addition, XOR, AND, OR and shift of 256-bit words,
for every comparison and for every branch, so PROR = 5. One load is charged every time a word is fetched from memory, from a list or from the table into a register, and one store every time a register
is written to memory or to the table. Shift distances are fixed in the instruction. A register may hold a memory word across several operations, and that is the one place where this text counts
differently from entry c66f230d, which charged a load for every use of a constant. Nine words are loaded once per value of X2, in the last part of the middle step ("class loop entry", 9 loads), and
stay in their registers for all 18,725 batches of that value: the two masks of the rotation by 16, the two of the rotation by 12, the two masks of Lemma A (c), ALL, 2^32 - ALL, and the word that has
every bit of the seven lanes except bit 32. Stage 2 needs the registers of the last four for its own values and loads them again at its end (the part "restore", 4 loads, charged to stage 2). Stage A
does not keep z and the third value of C2 in registers; stage 2 forms both again (5 operations and 3 loads, charged to stage 2). Two registers hold the list position and the entry count for the whole
search. With that, the batch uses all 16 registers, and 15 do not run it, under the program's convention that the result of an instruction may reuse a register whose source value is used for the last
time on that instruction; if instead every source stays live until its instruction finishes, the batch peaks at 17 registers. The idea of keeping masks in registers across a loop is credited in
Section 16. Under the convention of entry c66f230d, with every read of a memory word charged as a load, the same program counts 57 and 143 for the two stages (its line `KEPT = 0`); no address
arithmetic is charged for the list and table loads, as in that entry, and with one operation for each such load the stages would be 50 and 139.

*No lane overflows.* Put B = 2^32. Table words, list words, stored words, rotation outputs and constants are below B, and an XOR with a value below B keeps a bound that is a multiple of B. In the
build, Y12 and C0.a1 are below 2B, XA below 3B before it is reduced, D1.c1 below 3B, D1.d1 below 4B, and X1 below 4B before it is reduced. In stage A, X0 is below 2B and X10 below 3B; C2's first value
is below 2B, its third, X10 plus a rotation output, below 4B, and its fifth below 4B, so z is below 4B; by Lemma A (c) the bits of z above 31 never reach a position that is read, and by Lemma A (d)
the sum of rule A is at most B. In stage 2, z and the third value are within the same bounds and the sum for Y6 is below 5B; X10 + (-X15) is below 4B; C1's first value is below 3B, its third below 2B,
and Y1 + S1 + S6 below 5B; in E1, a1 is below 7B, c1 and c1' below 2B, the two a2 below 9B and c2 and c2' below 3B. In the E1 test beta XOR eps is below 4B, so its shift left by one bit stays inside
the lane, n is reduced by an AND with M, and the sum that forms the flags is below 2B. So every sum of a batch is below 9B and every sum of the build below 4B, both below 2^36 = 16B: no carry leaves a
lane, the low 32 bits of every lane equal the scalar value modulo 2^32, and XOR and PROR read only those bits. For the outer step and the middle step a participant tool derives the bounds by interval
arithmetic on a second machine: below 7B and below 8B. Every word that is stored and every word that enters the flags of stage 2 is below B.

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

So stage A is 37 + 10 = 47 and stage 2 is 105 + 30 = 135. The three other pieces:

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

The build is 43 + 26 + 5 = 74 per list word, that is 74 * 18,725 = 1,385,650 per outer step; the middle step is 85 + 40 + 9 = 134 and the outer step 148 + 91 + 21 = 260. Registers in use at one time,
the two for the list position and the entry count included: 16 in a batch, 11 in the outer step, 7 in the build, 13 in the middle step.

Each XOR followed by a rotation is 6 operations, a two-term sum 1 and a three-term sum 2. The loads of stage A are the list end, XA[j], -w2, ROL(X15,8), S10 + X15, X6[j], X2 + w7, X14, w0 and
V[j]: 10. In "rule A" the word y is 8 operations (two shifts with an AND and an XOR, one shift with an XOR), u an XOR with the loaded V[j] and an AND, the sum one addition, and the flags an OR with
the word that has every bit except bit 32 of each lane, a comparison with that word and the branch: 14 operations and one load. The loads of stage 2 are the budget; X6[j], X2 + w7 and w0 for z, and
the two mask pairs of the rotations by 8 and by 7; -X15, S5, X1[j], w3, X13, X9, R[j] and S12; w12 - S1 - S6, Y12[j], Y11, w5, Y11' and w5 + delta; the mask of the rotation by one bit, M, the mask of
bit 32 and eta; and the four words of "restore": 30. The count of the middle step is for all 21 lines of step M and its nine stores; two of the lines (S0 and w1) and the store of w1 serve only the
processing of a trial whose E1 test word is zero and are counted for every value of X2 all the same.

*The count in the submitted program.* The program of the two declared experiments, experiments/halfsearch.py, contains the four pieces, the counter construction and the counter batch of Sections 8 and
9, and the machine that counts them, a packed word being one integer with seven 36-bit lanes. The pieces are written only with calls that each add one operation (an addition, XOR, AND, OR, shift,
comparison or branch), one load (a fetch of a memory, list or table word, unless it is one of the nine kept in registers) or one store. The program always evaluates both stages of a batch, so that
stage 2 is counted and checked for every batch; a search runs stage 2 only after a pass of stage A. The command

    python3 experiments/halfsearch.py --selftest N [seed]

runs N cases. A case is one outer step, one word of each list of the table, one middle step and one packed batch; the seven context words and the list position of a case come from SHAKE-256 of the
seed text (default 1) and the case number. Every fourth case is the last batch of the sub-class, and in every fifth case each context word is 0, 2^32 - 1 or as drawn. Every lane is checked against the
real messages of its trial: the program builds A and B by steps O, M, Y, T, S2 and S3 and compresses each in full, with a 2-round compression written out from Section 1 and no shortcut of the batch,
and takes from them Y4 of A, h1 of E3 on A, the word n of Lemma N from E1 evaluated for A and B on their own states and words, and the two digests. A lane is right when the sixteen words of the 55
bytes of A are the words of the trial, Y4 is the member of the lane, the digests agree on digest words 0, 2, 5 and 7, the stage-A flag says whether h1 satisfies rule A as written in 6.3, the reduced
word of stage 2 equals n, n equals D3 XOR ROL(D6, 8) of the two digests, and the stage-2 flag says whether n is nonzero; and no lane counts as right unless every word that the outer step, the build
and the middle step have stored is the word of the context, and both branches are taken exactly when one of the seven words in front of them is zero. The program prints one JSON line with the counts
per part, the largest lane of a sum per part next to its bound, the registers per piece, the kept words, the members in the lists, the lanes checked, right and satisfying rule A, and two complete
enumerations: the flags of stage 2 on all 128 patterns of zero and nonzero lanes, and the flags of stage A on packed words in which every pattern of the 13 bits of z that rule A reads, with every
pattern of the bits 27 to 29 of e1, occurs once in every lane. Its exit status is 0 only if all of these agree with this section. The same command also runs the counter part of the self-test (9.3),
reported under the key `counter` of the same line, and the exit status is 0 only if that part passes as well.

With N = 2,000 and seed 1 it reports 14,000 of 14,000 lanes right; 37 operations and 10 loads in stage A and 105 and 30 in stage 2, per part as in the table and the same in every case; largest sums of
2.968, 3.831, 1.000, 4.818, 4.511, 7.999 and 1.999 times 2^32 in the parts "X0 to X10", "C2 to z", "rule A", "C2, rest", "C1 to Y1", "E1, A and B" and "E1 test", below the bounds 3, 4, 2, 5, 5, 9 and
2; 131,072 members in the 18,725 words of each list; and 16, 11, 7 and 13 registers. In that run 54 lanes satisfy rule A, in 46 batches. None of its words n is zero, which is why the flags of stage 2
are also formed for all 128 patterns of zero and nonzero lanes: all 128 are right. For rule A the 65,536 packed words, each of the 2^16 patterns once in every lane with different other bits and filled
guard bits, are compared with rule A as written on h1 = ROR(ROR(z, 8) XOR e1, 16): all 65,536 are right, and in 1,792 = 7 * 256 of them some lane satisfies the rule, each lane in 256, the share 2^-8.

A longer run of the program as filed for entry 64c075ac, whose part for the root instance this program keeps unchanged, 1,000,000 cases with seed 61, reports 7,000,000 of 7,000,000 lanes right, the
same counts in every case, the same registers and a largest sum of 8.349 * 2^32; 27,068 of its lanes satisfy rule A, in 23,368 batches. Its contexts are random or extreme by design and are not laid
out as a run of a search, and every fourth case is the short last batch, whose spare lanes repeat a member, so these two counts are not a measurement of a rate. A participant tool with a second
counting machine, sharing no code with the program's, counts the same operations, loads and stores for all four pieces and refuses the batch with 15 registers; another derives the bounds of the sums
for all inputs by interval arithmetic and finds every one below the bound of its part.

In the declared experiment `residual-search` the same program evaluates, per organizer seed, one outer step, the table words of one list word, one middle step and one batch, for that seed's context
and the list position of the first member tried, and returns the operations and loads of the two stages of the batch, its number of right lanes and whether a lane satisfied rule A as observations. The
organizer's runner records observations as untrusted and does not recompute them. The self-test and these observations therefore show what the program in the package counts, and that its lanes agree
with the program's own compression of the real messages. They are a participant check, not an organizer verification of the cost.

## 7. The tree lemma: the last chunk decides the digest

The claim is made for messages of more than one chunk. This section shows, from the organizer's reference code, that for such a message the digest is a function of the prefix and of the chaining value
of the last chunk alone.

The organizer's hash, `verifier/blake3.py`, computes `blake3(data, rounds)`, with rounds = 2 for this target, by these lines of its code:

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

There `_chunk_output(chunk, counter, rounds)` compresses every block of a chunk but the last, starting from the chaining value IV, and returns the last block as a descriptor (cv, words, counter,
len(block), flags | CHUNK_END), where flags is CHUNK_START = 1 when that block is the first of its chunk; its last block starts at `last_offset = max(0, (len(chunk) - 1) // 64 * 64)`. `_compress(cv,
words, counter, block_len, flags, rounds)` is the compression of Section 1 with v[0..7] = cv and v[12..15] = (counter mod 2^32, counter >> 32, block_len, flags); it returns sixteen output words, of
which the first eight are the chaining value. `_parent_output(left, right)` is the descriptor (IV, left + right, 0, 64, PARENT) of a parent node.

**Lemma TR (the last chunk decides).** Let t >= 1 and let F be any string of 1024 t bytes. For a string A of 1 to 64 bytes write words(A) for the sixteen little-endian words of A followed by zero
bytes up to 64 bytes, and CV_t(A) for `_compress(IV, words(A), t, len(A), 3, 2)[:8]`.

(a) The last chunk of F || A is A, and the organizer's code compresses it once, as `_compress(IV, words(A), t, len(A), 3, 2)`: the compression of Section 1 with block A, block length len(A), counter t
and flags CHUNK_START | CHUNK_END = 3. It is not the root compression.

(b) blake3(F || A, 2) is a function of F and of CV_t(A) alone.

(c) For strings A and B of 1 to 64 bytes with CV_t(A) = CV_t(B), blake3(F || A, 2) = blake3(F || B, 2).

Proof. (a) F || A has 1024 t + len(A) bytes with 1 <= len(A) <= 64, so chunk_count = t + 1 and the last chunk is data[t * 1024:] = A. In `_chunk_output(A, t, 2)`, last_offset = 0, so that function
stops at its first block, offset 0, and returns (IV, words(A), t, len(A), CHUNK_START | CHUNK_END). The final loop of blake3 compresses this descriptor once, in its first pass, which runs because the
stack is not empty (b).

(b) The loop over counter = 0, .., t - 1 reads data[counter*1024:(counter+1)*1024], which lies inside F, and no other byte of the message; so the stack that it leaves depends on F alone. Each pass
appends one value and pops values only while total is even, so after t >= 1 passes the stack holds as many values as t has one bits, at least one. The final loop therefore runs at least once. Its
first pass forms `_parent_output` of the top of the stack and CV_t(A), and every later pass forms a parent descriptor from the next value of the stack and the chaining value of the descriptor before
it. The root compression reads the last descriptor. So the digest is computed from the stack, which depends on F alone, and from CV_t(A).

(c) follows from (b). QED.

The code accepts messages shorter than 2^61 bytes; the messages of this package are shorter than 2^42 bytes (Section 8). The tree, its counters and flags and its root output are those of the target
profile. The two messages of a pair are complete messages of the domain, and a pair with equal digests is an ordinary collision, not a free-start or compression-only one. The converse of (c) is not
used.

*The digest does not show a partial agreement.* When CV_t(A) and CV_t(B) agree on four words only, the parent and root compressions over them mix all eight, and the two digests are not expected to
agree on a fixed set of words. On two counter pairs of Section 8 with t = 1, messages of 1,079 and 1,087 bytes, the chaining values agree on words 0, 2, 5 and 7, and the two digests do not agree on
digest words 0, 2, 5 and 7 (participant computation with the organizer's code). This is why the declared experiments run the root instance (6.4).

*Participant checks with the organizer's code.* In each of the following the organizer's `verifier/blake3.py` was imported unchanged; they are participant computations, which the organizer has not
run. (1) For 2,000 trials of the counter construction of Section 8 in 40 outer steps, 8 of them with outer words 0 or ffffffff, `_chunk_output` of the last chunk returned (IV, the block words, t, 55
or 63, 3) for A and for B, and `_compress` returned the chaining value that the program computes, in 2,000 of 2,000; words 0, 2, 5 and 7 of the two chaining values were equal in all 2,000 and all
eight words in none; and 204,000 internal words of the construction were equal to a separately written forward computation of the compression. (2) For five counter trials with t = 1, 3, 3, 4 and
16,383, the complete messages F || A and F || B, with F a string of t chunks of pseudorandom bytes, were hashed by `blake3(m, 2)`. In each, the messages have 1024 t + 55 and 1024 t + 63 bytes; the
code makes exactly one compression with block length 55 or 63, and its inputs are (IV, the block words, t, 55 or 63, 3); its chaining values agree on words 0, 2, 5 and 7 and not on all eight; the two
digests differ; and when the output of that compression of F || B is replaced by the output of the one of F || A, blake3 returns the digest of F || A, and the other way round. (3) Before the program
was written a helper agent checked (b) in the same way for 25 values of t from 1 to 1,025, on 150 messages and 75 pairs with a replaced output, all as the lemma says.

## 8. The counter construction

*Words and constants.* The construction has nine free words: the seven *outer words* C0.d1, D2.a1, D2.b1, S11, S4, X9 and w6 (the program's `CTR_BASIS`); a member y of the class of 6.1 (Lemma Q),
which becomes the value of Y4; and the *inner word* c1, which becomes the third value of E1 on message A. The constants are those of Section 4: X3, X7, X11 and X15, w4 = W4, w13 = W13, w14 = w15 = 0,
the four constant first values K2.a1, K2.d1, K2.c1 and K2.b1 of K2 given in step O, and Y3, Y11 of Fact P. The compression reads three more values besides the message and the IV. K3 reads the flags,
here 3 (the line for K3.d1); K1 reads v[13], here 0 (the line for K1.a1); and K0 reads the counter v[12], which is not fixed in advance: the line for t solves K0's second assignment for it. The names
are those of Section 4.

*The cube Q*.* Q* is the set of the 2^21 words c with (c AND 0e09818b) = 02008000; the program names the mask and the value `CTR_MASK` and `CTR_VALUE`. Member number j of Q*, for 0 <= j < 2^21, is the
word whose bits at the 21 positions where 0e09818b has a zero are the bits of j, in increasing order of position (the program's `ctr_c1`).

*Members.* In Sections 8 to 12 a *member* is a member of the class of Lemma Q, not of the sub-class of 6.1. Member number k of the class, for 0 <= k < 2^19, is the Y4 whose e1 = Y3 + Y4 has the bits
of k at the 19 positions where 03cf8303 has a zero, in increasing order of position, and Y4 = e1 - Y3. The search of this package uses every member; it has no sub-class and no rule A.

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

**Step CS (the messages).** If t = 0 the trial is invalid and is dropped: a message with no full chunk before its last chunk has that chunk as its root, compressed with counter 0 and flags 11 and not
with the flags 3 that the line for K3.d1 used. Otherwise the words w0 to w12 of the lines, with w4 = W4 and w13 = W13, and w14 = w15 = 0 form the block of A; A is the first 55 bytes of its
little-endian encoding, and B the first 63 bytes of that of the same words with w4' = W4' and w5' = w5 + fffffff8 in place of w4 and w5, as in steps S2 and S3 of Section 4. F is the string of 1024 t
zero bytes, and the two messages are F || A, of 1024 t + 55 bytes, and F || B, of 1024 t + 63 bytes. In the program step CO is `ctr_outer`, step CT and the two blocks of step CS are `ctr_trial`, which
returns nothing for t = 0, and the flags are the constant `CTR_FLAGS` = 3.

*The order and the calls.* Table CT gives each call's eight assignments by the name that the line for that assignment assigns; the cells K2.a1, K2.d1, K2.c1 and K2.b1 are the four constant values.
E1's first five assignments are the lines for Y6, E1.a1, E1.d1, E1.b1 and E1.a2, in the order of the assignments; E3's first two assignments are the line for E3.h1, and its third to fifth the lines
for E3.g1, E3.f1 and E3.e2.

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

The order was found by a solver search of the participant's helper agents for an order in which Y4 and E1.d1 are both free words.

**Lemma CT (the counter order).** (a) *Triangular.* In the printed order, step CO and then step CT, every line assigns a name that no earlier line assigns and that is neither one of the nine free
words nor a constant, and it reads only constants, the nine words and names of earlier lines; a line of step CO reads neither c1 nor a name of step CT. Every line is one assignment of one call solved
for the name on its left; the exceptions are the line for E3.h1, which is the first two assignments of E3 with the first substituted into the second (e1 = Y3 + Y4 + w15, w15 = 0), and the line for
E3.e2, which uses the same e1. By Table CT the 93 lines and the four constant values of K2 are, each exactly once, the eight assignments of each of the eleven calls K0..K3, D0..D3, C0..C2, with the
inputs and the message words of Section 1 for block length 55, counter v[12] = t, v[13] = 0 and flags v[15] = 3, with w4 = W4, w13 = W13, w14 = w15 = 0, and with the constants X3, X7, X11, X15 as the
a output of D3, the b output of D2, the c output of D1 and the d output of D0; and the first five assignments of E1 and of E3 for message A, E1 with c input Y11 and E3 with a input Y3.

(b) *The calls.* For every choice of the nine words, the names of the lines are the executions of these calls. In particular round 0 on the block of A, with block length 55, counter t, v[13] = 0 and
flags 3, leaves the state X of the names, with the four constants as X[3], X[7], X[11] and X[15]; C0 has outputs (Y0, y, Y8, Y12); and in the compression of A, E1.c1 = c1, since E1's third assignment
is E1.c1 = Y11 + E1.d1.

(c) *The levels.* A line of step CO is a function of the seven outer words and y. Of the message words only w0 and w1 are lines of step CT, and so is the counter t; every other message word is a line
of step CO or a constant. So the trials of one outer step differ in w0, w1 and t and in nothing else of their two messages.

Proof. (a) is read off the displays, each formula compared with Section 2 and with its call's inputs, outputs and message words (Section 1, with v[12] = t, v[13] = 0 and v[15] = 3); Table CT has one
name in each of its 88 cells, all different, the four constant values of K2 among them, and with the five names of E1 and the four lines of E3 they are the 93 lines and the four constants.
(b) As in Lemma T2 (b): an assignment solved for one of its terms is an equivalent equation modulo 2^32 (Fact 1), so a line's assignment holds once it has run, and by (a) no later line changes its
names. By (a) and Table CT all eight assignments of each call hold, a constant output in its place (the lines for D3.b1 and D3.d1; X8; D1.c1 and X6; D0.d1 and X10) and y as the b output of C0 (the
line for Y8); by Fact 1 the names are the execution of the call. (c) By induction over the printed order, with (a): a line of step CO reads only constants, the seven outer words, y and lines of step
CO; w2, w3, w5 and w7 to w12 are lines of step CO, w6 is an outer word, w4, w13, w14 and w15 are constants, and w0, w1 and t are lines of step CT. QED.

**Theorem C (the last-chunk half-collision).** For every choice of the seven outer words, of a member y of the class and of a word c1, steps CO and CT give a counter t. If t is not zero, step CS
outputs two distinct messages F || A and F || B of 1024 t + 55 and 1024 t + 63 bytes, with 1 <= t < 2^32, such that

(i) their last chunks are A and B, compressed with counter t, v[13] = 0 and flags 3 (Lemma TR (a));

(ii) the chaining values CV_t(A) and CV_t(B) agree on words 0, 2, 5 and 7;

(iii) in both last-chunk compressions Y4 = y, and the XOR difference between A and B of E3's first-half d value is eta = 830303cf;

(iv) in the compression of A, E1.c1 = c1; and if c1 is in Q*, the XOR difference between A and B of E1's first-half b value is beta* = 18b0e098.

Proof. t is the XOR of two 32-bit words, so t < 2^32 and t >> 32 = 0, the value v[13] = 0 that the line for K1.a1 used. The sixteen words have w14 = w15 = 0 and w13 = W13, whose top byte is zero, so A
and B are honest strings of 55 and 63 bytes whose zero-filled blocks are the sixteen words and the same words with w4 and w5 replaced, as in Section 5. By Lemma TR (a) the last chunks are compressed
with counter t, v[13] = 0, flags 3 and block lengths 55 and 63. By Lemma CT (b) round 0 on the block of A leaves the state X of the names, with the four constants as X[3], X[7], X[11] and X[15]. The
counter, v[13] and the flags are the same in both compressions, and K2 is the only call of round 0 that reads the block length, w4 or w5; Lemma L, whose proof concerns K2 alone, therefore gives the
same state X for B. Lemma H gives (ii): its proof uses only round 1 and o[i] = Z[i] XOR Z[i + 8] for i = 0, 2, 5 and 7, and the chaining value is (o[0], .., o[7]). (iii) As in the proof of Lemma T: C0
reads the same words of X and w2, w6 in both compressions and has b output y by Lemma CT (b); w15 = 0, Y14 is the same in both, the a input of E3 is Y3 for A and Y3' for B by Fact P, and y is in the
class, so the difference is eta by the definition of the class (6.1). (iv) E1.c1 = c1 is Lemma CT (b). E1 has inputs (Y1, Y6, Y11, Y12) and message words (w12, w5) for A, and (Y1, Y6, Y11', Y12) and
(w12, w5 + delta) for B. Its first and second values are the same for both, so its third values are c1 and c1 + DY11, with DY11 = Y11' - Y11 = 0a08818b, and its fourth values are ROR(Y6 XOR c1, 12)
and ROR(Y6 XOR (c1 + DY11), 12). Their XOR is ROR(c1 XOR (c1 + DY11), 12), which is beta* exactly when c1 XOR (c1 + DY11) = ROL(beta*, 12) = 0e09818b. For words c and x, (c XOR x) - c = x - 2 (c AND
x) modulo 2^32, which is the identity of the proof of Lemma Q; with x = 0e09818b this holds exactly when 2 (c1 AND 0e09818b) = 0e09818b - DY11 = 04010000. As 0e09818b has no bit 31 the doubling is
exact, and it holds exactly when (c1 AND 0e09818b) = 02008000, that is when c1 is in Q*. The messages are distinct because their lengths differ. QED.

*The counter is the free word.* In the root instance the second assignment of K0 reads the counter 0, so K0.a1 = ROL(K0.d1,16) follows from the context, and with it the message word w0. Here that
assignment is solved for the counter instead, which leaves K0.a1, and with it w0, free. The word w0 enters round 1 only in the fifth assignment of C2, and the lines for Y2, Y14, Y10, Y6, E1.a1 and
E1.d1 of step CT map their running word one to one, so every value of E1.d1, and so of c1, can be prescribed in one outer step. With the counter fixed, no order of the assignments has both Y4 and
E1.d1 among its free words, and with the counter free no order has Y4, E1.d1 and E3.h1 all free: the counter buys one prescribed word. These two statements are results of a participant search over the
orders, decided by an exact peeling test that was checked against brute force; nothing below uses them.

**Lemma IP (the inner permutations and the member with t = 0; GPT Sol 6.1).** Fix the seven outer words and y. (a) The maps c1 -> E3.h1 and c1 -> t given by step CT are permutations of the 32-bit
words. (b) So the 2^21 members of Q* give 2^21 different values of E3.h1 and of t, and at most one member of Q* has t = 0.

Proof. With the names of step CO fixed, the lines for E1.d1, E1.a1, Y6, Y10, Y14 and E3.h1, with e1 = Y3 + y, each map their running word one to one. Read backwards: Y14 = ROL(E3.h1,16) XOR e1, Y6 =
ROR((Y14 + C2.c1) XOR C2.b1, 7), E1.a1 = Y6 + Y1 + w12 and c1 = Y11 + ROR(E1.a1 XOR Y12, 16). For the counter, Y2 = ROL(Y14,8) XOR C2.d1 = ROL(E3.h1,24) XOR ROL(e1,8) XOR C2.d1, and the lines for w0,
K0.a1 and t give t = ROL(K0.d1,16) XOR (Y2 + IV[0] + IV[4] - C2.a1 - C2.b1), where K0.d1, C2.a1, C2.b1, C2.d1 and e1 are names of step CO. That is a composition of permutations of E3.h1. Its only zero
is at E3.h1 = ROR((ROL(K0.d1,16) - IV[0] - IV[4] + C2.a1 + C2.b1) XOR ROL(e1,8) XOR C2.d1, 24), and the inverse above gives its one value of c1, which may or may not lie in Q*. QED.

So an outer step has 2^21 or 2^21 - 1 valid trials. Lemma IP bounds the number of trials that the rule t != 0 drops, one in 2^21 at most; it does not bound the share of the collision mass that the
dropped trial carries (10.3). In the participant's checks the member with t = 0 was constructed by the inverse above in 40 outer steps and rejected by the program in 40 of 40; over 8,192 further outer
steps it lay in Q* 4 times, against 4.0 expected, and was rejected 4 times out of 4.

*The length of the messages.* Within one outer step the 2^21 members of Q* give 2^21 different values of t below 2^32 (Lemma IP); over 2,000 trials of the participant's check t ran from 891,836 to
4,291,586,422 with a mean of log2 t of 30.56. A pair found by the search has messages of 1024 t + 55 and 1024 t + 63 bytes, shorter than 2^42 bytes and about 2^41 on average. A small t cannot be
chosen: it is the value of a permutation of c1 at the member that the search finds.

**The outer filter.** Number the fourteen outcomes of beta* on the class (10.1) j = 1 to 14 in the order of the table of 10.1: the seven of entry 26ebba63, 175020a0, 185020a0, 275020a0, 285020a0,
385020a0, 675020a0 and 685020a0, as j = 1 to 7, and the same seven with bit 14 of tau set, 175060a0, 185060a0, 275060a0, 285060a0, 385060a0, 675060a0 and 685060a0, as j = 8 to 14. Let tau_j be the tau
of outcome j, sigma_j = tau_j XOR ROR(tau_j, 1) and theta_j = ROL(sigma_j, 12); all fourteen have eps = 6e21be55, and theta_8 to theta_14 are 850f01cf, 850f0147, 850f034f, 850f03c7, 850f0247, 850f054f
and 850f05c7. For an outer step put omega = Y3 + y + w8, with Y3 of Fact P, y the member of the outer step and w8 the name of step CO; DY3 = Y3' - Y3 = fdb77cfd is that of Section 6. For a word x:

- condition (1)_j holds for x when some word h gives (x + h) XOR (x + (h XOR eta)) = theta_j;
- condition (2)_j holds for x when some word f gives (x + f) XOR ((x + DY3) + (f XOR sigma_j)) = eps.

An outer step *passes* the filter when for some j both (1)_j holds for its Y9 and (2)_j holds for its omega. Y9 and w8 are names of step CO and y is drawn with the outer words, so whether an outer
step passes depends on the outer step alone and on no c1.

**Lemma F (the outer filter; GPT Sol 6.1, answers AC and AN).** Fix an outer step that does not pass the filter. Then no trial of the outer step, for any word c1, has R = 0 with an E1 outcome among
the fourteen outcomes of beta*. If the fourteen are all the outcomes of beta* that have a solution with Y4 in the class, as the count of Section 17 finds, then no trial of the outer step with c1 in Q*
has R = 0.

Proof. Take a trial with R = 0 whose E1 outcome is outcome j. Write h, g, f and e2 for E3.h1, E3.g1, E3.f1 and E3.e2 in the compression of A, and h', g', f' and e2' for the same values in that of B.
Y9 and w8 are the same in both compressions: w8 is a line of step CO and a word of both blocks, and Y9 is an output of C1, which reads words of the state X, the same for A and B (proof of Theorem C),
and the message words w3 and w10, which the two blocks share. Both compressions have Y4 = y and h' = h XOR eta (Theorem C (iii)), and the a input of E3 is Y3 for A and Y3' for B (Fact P). The
conditions of R = 0 (Section 13, how r is counted) give that the XOR difference of E3's first-half b values is psi = tau_j XOR ROR(tau_j, 1) = sigma_j, and that of its a outputs is eps' = eps. Now g =
Y9 + h and g' = Y9 + (h XOR eta); f = ROR(y XOR g, 12) and f' = ROR(y XOR g', 12), so f XOR f' = ROR(g XOR g', 12) = sigma_j gives g XOR g' = theta_j, and h witnesses (1)_j for Y9. With w15 = 0, e2 =
Y3 + y + f + w8 = omega + f and e2' = Y3' + y + f' + w8 = (omega + DY3) + (f XOR sigma_j), and e2 XOR e2' = eps, so f witnesses (2)_j for omega. So the outer step passes, against the hypothesis. The
second statement follows because every trial with c1 in Q* has the difference beta* (Theorem C (iv)). QED.

The lemma uses no law of the words: no uniformity, no independence and no relation between h and f besides the two equations. It does not use the rule t != 0, and it holds for any list of outcomes
(GPT Sol, answer AN 2). The filter can pass outer steps that hold no success, since (1)_j and (2)_j are solved with separate witnesses; it cannot reject an outer step that holds a success with one of
the fourteen outcomes.

**The exact share (GPT Sol, answers AC and AN; recounted by the participant).** Let pi be the share of the 2^64 pairs (x1, x2) of words such that for some j condition (1)_j holds for x1 and (2)_j for
x2. Then

    pi = 99,669,577,442,459,648 / 2^64 = 1,520,837,058,143 / 2^48,

about 0.0054030986 = 2^-7.531997. For the seven outcomes j = 1 to 7 alone, the filter of entry 26ebba63, the share is 20,504,986,129,465,344 / 2^64 = 2^-9.813176; pi is 4.8607 times that.

*Method.* Whether (1)_j holds for x is decided bit by bit from bit 0 upwards. At bit i the XOR of the two sum bits prescribes the XOR of the two incoming carries; the state is the set of incoming
carry pairs that some choice of the lower bits of the witness reaches with the lower bits of x, and the next state is the set of carry pairs out of bit i that some witness bit gives from a pair of the
set that meets the prescription. The condition holds when the set is still nonempty after bit 31, which has no outgoing carry to prescribe because the arithmetic is modulo 2^32. For (2)_j the carry of
x + DY3 is carried as well. The fourteen sets for the fourteen outcomes are carried together over the same bits of x, each with its own witness (a subset construction), so one pass over the bits of x
gives its *mask*, the set of j for which the condition holds; equal states add their counts of prefixes of x, and witnesses are never counted. A pair passes exactly when the mask of x1 under (1) and
the mask of x2 under (2) intersect, so the number of passing pairs is the sum, over pairs of intersecting masks a and b, of the number of words with mask a under (1) times the number of words with
mask b under (2).

*Certificate.* Masks are written in hexadecimal with bit j - 1 for outcome j (bit 0 for 175020a0, bit 6 for 685020a0, bit 7 for 175060a0, bit 13 for 685060a0). First the seven outcomes j = 1 to 7
alone: the numbers of words with each nonzero seven-bit mask m are 7,936 a_m under (1), a_m the second column, and 1,082,016 b_m under (2), b_m the fourth and the sixth columns:

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

No other nonzero seven-bit mask occurs; 134,896,128 words satisfy some (1)_j and 233,715,456 some (2)_j with j <= 7, and the sum of a_m b_n over the pairs of intersecting masks m and n is 2,387,944.

For all fourteen outcomes, write m << 7 for the mask m moved to the rows j = 8 to 14. For every nonzero mask m of the table the numbers of words with a fourteen-bit mask are

    under (1):  m: 256 a_m,      m << 7: 8,192 a_m,      m OR (m << 7): 7,680 a_m;
    under (2):  m: 955,552 b_m,  m << 7: 2,023,424 b_m,  m OR (m << 7): 126,464 b_m,

and no other nonzero mask occurs: 36 nonzero masks under (1) and 72 under (2). 274,143,744 words satisfy some (1)_j and 670,775,040 some (2)_j; 4,020,823,552 and 3,624,192,256 have mask 0, so each
histogram sums to 2^32, and merging the rows j and j + 7 of each mask gives back the histograms of the seven. A mask of the kind m under (1) never meets one of the kind n << 7 under (2), nor m << 7
one of the kind n; every other pair of kinds meets exactly when m and n intersect. So every intersecting pair (m, n) of the table has the weight

    256 (955,552 + 126,464) + 8,192 (2,023,424 + 126,464) + 7,680 * 3,105,440
      = 256 * 163,041,632,

and the number of passing pairs is 256 * 2,387,944 * 163,041,632 = 99,669,577,442,459,648. The histograms are those of the carry-set recurrence of the method above over the 31 constrained bits, with
at most 133 and 146 determinised states (GPT Sol, answer AN 2).

*The automata.* The program's `ctr_automaton` builds the subset construction above as four byte tables: a state is the carry of x + DY3 (zero for (1)) and, per outcome, the set of reachable carry
pairs, four bits; the table of byte p maps a state and byte p of x to the next state, and the table of the last byte maps to the mask. `ctr_tables` builds the two automata once per run from `CTR_TAUS`
and `CTR_EPS`, which in the submitted program hold the seven outcomes of entry 26ebba63; the search of this package builds them with the fourteen values of tau above (step 0 of 9.1). In a participant
computation, the program's construction run with the fourteen values in place of `CTR_TAUS` has 1, 18, 43, 37 and 1, 3, 19, 19 states at the four byte boundaries, tables of 25,344 and 10,752 entries,
and the count of passing pairs 99,669,577,442,459,648; the carry-set recurrence and GPT Sol's closed-form masks give the same histograms, and a brute force of the fourteen-outcome automata at 10 bits
found 240 of 240 verdict words right. `ctr_look` runs an automaton on a word with one table load per byte, and `ctr_filter` returns the AND of the mask of Y9 under (1) and the mask of omega under (2);
the outer step passes when it is not zero. With its own seven outcomes the program's count of passing pairs is `CTR_SHARE` = 20,504,986,129,465,344, which the self-test of 9.3 recounts, and it checks
those automata against brute force.

## 9. The counter search

*History label (Section 18 governs).* Sections 9.1 to 9.6 state the search on the whole class of eta. Its algorithm, the filter, the joint solver of 9.4 with its guards and cap, the batch of 9.6 and
Lemmas V, CV, PL and PB are used by this entry on the winner sub-class as Section 18.2 and 18.3 state. The member rule of step 1 (030c0303 + (W AND fc307cfc)) and the constants FACTOR, RUN_STEPS,
PASS_BUDGET and RUN_BATCHES of 9.1 are the whole-class values of the base text, history (SHARE is unchanged); this entry uses the member rule of 18.1 and the budgets B, J7 and L of 18.3.

**9.1 The algorithm.** The search uses these constants: FACTOR = floor(5 * 146,838,388,736 / 7) = 104,884,563,382, the factor of H1', five sevenths of the count of 10.1 rounded down (10.3);
RUN_STEPS = ceil(0.49676 * 2^128 / (FACTOR * (2^21 - 1))) = 768,501,619,242,806,100,822, about 2^69.381, with 0.49676 = 12419 / 25000, so that a run has 0.49676 expected listed good trials at the rate
of H1' (10.4); SHARE = 99,669,577,442,459,648, the number of passing pairs of Section 8, so that the share pi of Section 8 is SHARE / 2^64; PASS_BUDGET = ceil(17 * RUN_STEPS * SHARE / 2^68) =
4,411,808,165,546,457,948, about 2^61.936, the share pi of the outer steps of a run times the margin 17/16, rounded up; and RUN_BATCHES = ceil(RUN_STEPS / 7) = 109,785,945,606,115,157,261, about
2^66.574, the number of batches of seven outer steps (9.6). The submitted program does not hold these five constants (below).

0. Before the batches, build the two automata of the outer filter for the fourteen outcomes (Section 8), and the three transition arrays, the fourteen static row descriptors and the statically written
   traversal of the joint solver (9.4, Section 11). None depends on an outer word.
1. For each of the RUN_BATCHES batches in turn, b = 0, 1, ..: draw eight fresh uniform 256-bit words R_0 to R_7. Lane i, for i = 0 to 6, is bits 36 i to 36 i + 35 of a word (9.6). Lane i of batch b
   holds the outer step of number 7 b + i if that number is below RUN_STEPS, which holds for all seven lanes except in the last batch, whose lanes 2 to 6 are not used. The *random word* of that outer
   step is the 256-bit word whose k-th 32-bit word, for k = 0 to 7, is the low 32 bits of lane i of R_k. Its first seven 32-bit words are the outer words C0.d1, D2.a1, D2.b1, S11, S4, X9 and w6. Its
   eighth word W gives the member y with e1 = Y3 + y = 030c0303 + (W AND fc307cfc), that is the member of the class whose 19 free bits of e1 (Lemma Q) are the bits of W at the same positions; its
   member number (Section 8) is these 19 bits in increasing order of position. *Filter:* run step CO and the filter in all lanes at once on packed words (9.6): omega = Y3 + y + w8, the automaton of
   (1) on Y9 and that of (2) on omega in every lane, and the AND of their masks for each lane. A lane whose AND is zero ends its outer step there. Then for each lane whose AND is not zero, in
   increasing order of i, the outer step passes (Section 8): advance the count of passing outer steps, and halt with failure when it exceeds PASS_BUDGET; else compute on scalar words, from the eight
   words of the lane, the names of step CO that steps 2 and 3 read, and run steps 2 and 3 for this outer step.
2. *Roots:* run the joint solver of 9.4 on Y9, y and omega for every outcome j whose bit is set in the AND of the two masks. It returns the joint roots of these outcomes, each a word h with the
   outcome of which it is a root; an outer step has at most 72 of them (9.4).
3. *Certificate:* for each returned root h, with its outcome j, in turn: compute c1 from h by the inverse of Lemma IP, Y14 = ROL(h,16) XOR (Y3 + y), Y6 = ROR((Y14 + C2.c1) XOR C2.b1, 7), E1.a1 = Y6 +
   Y1 + w12 and c1 = Y11 + ROR(E1.a1 XOR Y12, 16); drop the root if c1 is not in Q*, that is if c1 AND 0e09818b is not 02008000; compute Y2, w0, K0.a1 and t by the lines of step CT, and drop the root
   if t = 0; evaluate E1 on A and on B (6.2) for this c1, and drop the root unless the XOR differences between A and B of their a outputs and of their c outputs are tau_j and eps = 6e21be55 (their
   first-half b difference is beta*, by Theorem C (iv)). A root that is not dropped is *certified*. For the first certified root, form F || A and F || B by steps CT and CS for its c1, evaluate blake3
   of both in full, check that the two digests agree, output the pair and halt.
4. After the last batch, halt with failure.

The run halts with failure in exactly two ways, each a test on a count that the algorithm keeps: the count of passing outer steps exceeds PASS_BUDGET, or the outer steps are exhausted. So at most
PASS_BUDGET outer steps run steps 2 and 3, which have no budget of their own: the joint solver returns at most 72 roots, and the work of steps 2 and 3 is bounded in every passing outer step, whatever
its words (9.4, Section 11). So the work of every run is bounded by the counts of Section 11, and a pair of messages is formed and hashed at most once, for a certified root.

A trial is *valid* when its t is not zero; a valid trial with R = 0 is *good*; a good trial is *listed* when its E1 outcome is one of the fourteen outcomes of beta* (10.1). A listed good trial is
found unless the run ends before its outer step is reached, by the pass budget or by the output of another pair: its outer step passes the filter by Lemma F, the joint solver returns its E3.h1 as a
root of its outcome, and step 3 certifies it (Lemma CV, 10.2). Every certified root is the E3.h1 of a listed good trial (Lemma CV). A good trial that is not listed is not found, and Section 10 does
not count it; by the count of Section 17 the fourteen are all the outcomes of beta* with a solution in the class. When the run outputs a pair, the pair is a collision of two complete messages: the
certified trial has R = 0 (Lemma V, 10.2), step 3 has checked both digests, and Lemma TR (c) says that R = 0 with the half-collision of Theorem C gives equal digests.

*What the submitted program holds.* The program is that of entry 26ebba63, unchanged: the earlier version of this search, on the sub-class. It contains steps CO and CT (`ctr_outer`, `ctr_trial`), the
outer filter (`ctr_tables`, `ctr_look`, `ctr_filter`) and the walk over outer steps (`ctr_run`) of the sub-class search of that entry, one outer step at a time on scalar words: its member is the
member of the sub-class of 6.1 of a number taken modulo 2^17, its filter has the seven outcomes of `CTR_TAUS`, and its constants are those of that search: `CTR_MEMBERS` = 2^21, `CTR_FACTOR` =
99,033,509,302, `RUN_OUTER_STEPS` = 813,905,892,669,542,263,145, `CTR_SHARE` = 20,504,986,129,465,344 and `CTR_PASS_BUDGET` = 961,264,466,727,415,003. For each outer step it is given, `ctr_run` runs
step CO and the filter; a failing outer step is skipped; a passing one advances the pass count, the walk halts with failure when that count exceeds CTR_PASS_BUDGET, and otherwise it runs the function
of the outer step that `ctr_run` is given. Its counted form `ctr_count` charges one walked outer step on a machine with scalar words and 16 registers (9.3); the charge of Section 11 does not use that
count. The search of this section differs from it in the member (the class, from the 19 free bits of the eighth word), the fourteen outcomes of the filter, the five constants above, the batch of seven
outer steps (9.6) and the charge (Section 11). These, the bound RUN_BATCHES on the number of batches (steps 1 and 4), the joint solver of 9.4 and step 3 are defined by this text only; no
implementation of them is part of the package, and no implementation of the joint solver for the class, in the layout of 9.4, has been run (9.5). The program also holds the counted enumeration of all
of Q* that a passing outer step ran in the version of this search that the joint solver replaces, and its self-test checks it (9.3): `CTR_WORDS` = 299,594, the packed words of seven lanes that hold
the members of Q*, of which the last holds member 2^21 - 1 in all seven lanes (7 * 299,594 = 2^21 + 6); the run-wide table of the packed words RT[j], whose lane i holds ROL(E1.d1, 16), and DT[j],
whose lane i holds E1.d1 = c1 - Y11, for c1 the member min(7 j + i, 2^21 - 1) of Q* (`ctr_table_word`); the words that a passing outer step stores for it, each in all seven lanes (`ctr_memory`): Y12,
-Y1 - w12, C2.b1, -C2.c1, w5, w5 + delta, the word v of Lemma A (c) for y, and beta*; and the counter batch of 9.2 (`ctr_batch`) with its two end tests: the part "loop" compares the advanced table
position with the word `end of list`, which holds CTR_WORDS, and the part "entry count" compares the advanced number of stage-2 entries with the word `stage-2 budget`, which holds STAGE_2_BUDGET =
floor(CTR_PASS_BUDGET * CTR_WORDS / 32) = 8,999,658,332,647,911,575,274, called E. The search of this section runs none of these; 9.2 and 9.3 describe them as the program and its self-test hold them.

**9.2 Seven trials in one word.** The counter batch runs on the machine of 6.5, with the same packed words of seven 36-bit lanes, the same masked rotation, the same charge of one unit for every
operation, load and store, and the same convention for registers. For table word j and lane i, with c1 the member of that lane, it computes in every lane:

- Stage A. *Cube word to Y14*: E1.a1 = RT[j] XOR Y12; Y6 = E1.a1 + (-Y1 - w12); Y14 = (ROL(Y6, 7) XOR C2.b1) + (-C2.c1). *z*: z = ROL(Y14, 8). *Rule A*: the word y and the test of Lemma A (c) and (d),
  with the word v of the outer step's y in place of the list word V[j]. *Loop*: the next table position, its comparison with `end of list` and the branch.
- Stage 2. *Entry count*: the next count of stage-2 entries, its comparison with `stage-2 budget` and the branch. *E1, A and B*: E1.a1 and Y6 again from RT[j]; d1 = DT[j]; c1 = d1 + Y11 and c1' = d1 +
  Y11'; then b1 = ROR(c1 XOR Y6, 12), a2 = w5 + E1.a1 + b1 and c2 = c1 + ROR(a2 XOR d1, 8) for A, and the same with c1' and w5 + delta for B. *E1 test*: eps = c2 XOR c2', beta* XOR eps, the word n =
  (ROL(beta* XOR eps, 1) XOR eps XOR eta) AND M of Lemma N, and the flags and the branch of the E1 test of 6.5.

Seven words stay in registers for all words of an outer step: Y12, -Y1 - w12, C2.b1, -C2.c1 and the masks A25, B25 and A24 of the rotations by 25 and by 24 (the program's `CTR_RESIDENT`); their loads
belong to the passing outer step. The batch uses 16 registers, the two that hold the table position and the entry count included.

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

So stage A is 31 + 10 = 41 units per word of seven trials and stage 2 is 50 + 22 = 72 units per word that enters it; no part stores anything. These counts are the program's table `CTR_TABLE`. The
loads of stage A are the end of the table, RT[j], the mask B24, the two masks of Lemma A (c), the word v, ALL, 2^32 - ALL and twice the word with every bit of the lanes except bit 32. The loads of
stage 2 are the budget; RT[j], DT[j], Y11, Y11', w5 and w5 + delta; the masks of the rotations by 12 and by 8, twice each; beta*, the mask of the rotation by one bit, eta and M; and M and the mask of
bit 32 for the flags and the mask of bit 32 for the branch.

**Lemma CB (the counter batch).** Fix an outer step, and let the memory hold the words that `ctr_memory` stores for it and the run-wide table (9.1). For every table word j and every lane i, with c1
the member of Q* of that lane and the trial given by the outer step and c1:

(a) the lanes of Y6 and Y14 hold, modulo 2^32, the values Y6 and Y14 of step CT, and z = ROL(Y14, 8) = C2.d1 XOR Y2;

(b) the flag of stage A says whether the trial satisfies rule A;

(c) the reduced word of stage 2 is the word n of Lemma N for the trial, and n = D3 XOR ROL(D6, 8), where D3 and D6 are the XOR differences between A and B of words 3 and 6 of the two last-chunk
chaining values; in particular R = 0 implies n = 0;

(d) no sum leaves its lane.

Proof. (a) RT[j] holds ROL(E1.d1, 16) for E1.d1 = c1 - Y11, so E1.a1, Y6 and Y14 are the lines for E1.a1, Y6, Y10 and Y14 of step CT, with the stored -Y1 - w12 and -C2.c1. C2's sixth assignment is
Y14 = ROR(C2.d1 XOR Y2, 8). (b) The proof of Lemma A uses only the sixth assignment of C2, the first two assignments of E3 with w15 = 0, the value Y3 of Fact P and the membership of Y4 in the
sub-class; all of them hold for the trial by Lemma CT and Theorem C. So Lemma A (a) to (d) hold for the trial, with the word v of y, and the operations of the part "rule A" are those of 6.5. (c) The
lines are those of 6.2 for E1 on A and on B, with c1 = d1 + Y11, c1' = d1 + Y11' and w5 + delta; beta* is the XOR difference of E1's first-half b values by Theorem C (iv). The proof of Lemma N uses
only E1, the second and sixth assignments of E3 and the difference eta of E3's first-half d values, which holds for the trial by Theorem C (iii); and words 3 and 6 of the chaining value are o[3] and
o[6]. (d) With B = 2^32: table words, stored words, constants and outputs of a masked rotation are below B; Y6 and Y14 are below 2B; in stage 2, c1 and c1' are below 2B, the two a2 and the two c2
below 3B, and eps and beta* XOR eps below 4B, so that the shift of the latter by one bit stays inside the 36-bit lane and the rotation by one bit is formed as in 6.5; the sum of the rule test is at
most B (Lemma A (d)) and the sum of the flags below 2B. So every sum is below 3B < 2^36. QED.

**9.3 The counter part of the self-test.** The command `python3 experiments/halfsearch.py --selftest N [seed]` of 6.5 also runs N cases of the counter batch (the program's `ctr_selftest`). A case is
one outer step, one table word and the counted batch on a new machine. Its eight words, its table position and a starting count of stage-2 entries come from SHAKE-256 of the text "halfsearch counter
selftest", the seed and the case number; every fourth case is the last table word, in every fourth case the count of entries starts one below E, and in every fifth case each outer word is 0, ffffffff
or as drawn. Each lane is checked against its trial (the program's `ctr_lane`): the program builds the two last-chunk blocks by steps CO, CT and CS and compresses each in full with counter t and flags
3 by the compression `compress2` of 6.5. It requires the round-1 words of the trial and its values of E1 and E3, the block words and the zero bytes, t < 2^32, words 0, 2, 5 and 7 of the two chaining
values equal, e1 in the sub-class, c1 in Q*, the difference beta* and the difference eta. A lane is right when all of these hold, its stage-A flag says whether the h1 of the compression satisfies rule
A, its stage-2 word equals the n of the compression, and its stage-2 flag says whether that n is nonzero. The end tests of a case are right when both branches agree with the lanes, the loop test ends
exactly at the last table word and the entry test fires exactly when the count reaches E. The exit status is 0 only if every lane and every end test is right, the counts equal the table of 9.2 in
every case, the registers are at most 16 and no lane exceeds 36 bits.

With N = 2,000 and seed 1 the counter part reports 14,000 of 14,000 lanes right, 55 lanes that satisfy rule A, 2,000 of 2,000 cases with right end tests, the counts of the table of 9.2 in every case,
41 and 72 units, 6.1786 units per trial at the share 1/32, 16 registers and a largest lane of 34 bits; the part for the root instance of the same run is the one reported in 6.5. These are the
program's own checks. The program's compression with counter t and flags 3 was compared with the organizer's `_compress` on 2,000 trials (Section 7); the organizer does not run the self-test.

*The filter part of the self-test.* The same command also runs the filter part (the program's `ctr_filter_selftest`, with the same seed), and the exit status is 0 only if it is right as well. (a)
Brute force: in 64 cases, the automata built for words of 10 bits, with the real targets truncated to 10 bits in the even cases and with random targets, for (2) with a random word in place of DY3, of
which three have a planted solution in the odd cases, run on a word drawn from SHAKE-256 of the text "halfsearch filter", the seed and the case number; each of the 128 masks is compared with the mask
that all 1,024 witnesses give. (b) The count of passing pairs from the program's own tables of 32 bits, compared with CTR_SHARE. (c) 2^16 real outer steps, their eight words from SHAKE-256 of the text
"halfsearch filter steps", the seed and the step number, walked by `ctr_run` with a stand-in that records each cube enumeration: the share that passes, the enumerations and the skipped outer steps; a
second walk of the same outer steps with pass budget 2 must halt at the third passing outer step after exactly two enumerations, and the counted pass test must stop the run when the advanced count is
CTR_PASS_BUDGET + 1. (d) The counted outer step and filter (`ctr_count`) against the plain ones on the first four outer steps and on the first four passing ones, with the same counts on all eight.
With seed 1 it reports 128 of 128 masks right, the count of passing pairs equal to CTR_SHARE (2^-9.8132), 74 of the 65,536 real outer steps passing (2^-9.791, standard error 0.000131 on the share
0.001129, z = +0.14 against pi), 74 enumerations and 65,462 skipped outer steps, the halt right, 8 of 8 counted outer steps right, and the counts used in Section 11: 467 units for the outer step (348
operations, 119 loads), 41 for the filter (24 operations, 17 loads) and 4 for the pass count (3 operations, 1 load).

**9.4 The joint solver (GPT Sol, answers AE, AF, AI, AL, AO and AR).** Fix a passing outer step and write Q = Y9, y for its member, E = omega = Y3 + y + w8 and E' = E + DY3; x[i] is bit i of a word x,
bit 0 the lowest, and maj is the majority of three bits. Put e1 = Y3 + y and b = e1[2], u = e1[21] and v = e1[26], three bits that are free in the class (in the sub-class of entry 26ebba63, u = v =
0). For an outcome j of beta* (10.1) put sigma = sigma_j and theta = theta_j (Section 8), eps = 6e21be55, gamma = eta XOR theta, D = (sigma XOR eps) AND 7fffffff, kappa = sigma XOR eps XOR E XOR E'
and mu = ROR(eta XOR eps, 8) = 9aed22bd. For a word h put g = Q + h, f = ROR(y XOR g, 12), e2 = E + f and h2 = ROR(h XOR e2, 8): for E3.h1 = h these are E3.g1, E3.f1 and E3.e2 of step CT and the d
output of E3 on message A (6.2). The *static descriptor* of outcome j holds sigma, theta, gamma, D and the positions of its constants and guards; the fourteen static descriptors depend on no outer
word and are formed once per run.

*Joint roots.* A word h is a *joint root* of outcome j when

    (J1)  (Q + h) XOR (Q + (h XOR eta)) = theta,
    (J2)  (E + f) XOR (E' + (f XOR sigma)) = eps,
    (J3)  (g + h2) XOR ((g XOR theta) + (h2 XOR mu)) = tau_j.

(J1) and (J2) are the conditions (1)_j and (2)_j of Section 8, with the two witnesses tied by f = ROR(y XOR (Q + h), 12). By (J1) theta is a function of h, and then so is the left side of (J3); the
fourteen values of tau are different, so no word is a joint root of two outcomes. There is no rule A: a joint root is any word that satisfies (J1) to (J3).

*Carries.* Write u[i] and u'[i] for the carries into bit i of Q + h and of Q + (h XOR eta), and a[k] and a'[k] for those into bit k of E + f and of E' + (f XOR sigma), all 0 into bit 0. Bit by bit,
(J1) holds exactly when u'[i] = u[i] XOR gamma[i] for every i, and (J2) exactly when a'[k] = a[k] XOR kappa[k] for every k. Bit i of h gives g[i] = Q[i] XOR h[i] XOR u[i] and bit k = (i + 20) mod 32
of f, f[k] = y[i] XOR g[i]. So the solver chooses h from bit 0 to bit 31 and runs both pairs of additions along it: those of (J1) on bits 0 to 31, and those of (J2) on bits 20 to 31 and then 0 to 19.
The carry a[20] is not known at the start; it is guessed for the constants of (a) below, and the check of (J2) as a word at each leaf enforces that bits 0 to 19 give the right carry into bit 20 (one
traversal, below). At a bit k < 31 with D[k] = 1, the *prescription* of f[k] is f[k] = E[k] XOR sigma[k] XOR kappa[k+1] if a[k] = E[k], and f[k] = E'[k] XOR kappa[k+1] otherwise: from carries a[k] and
a[k] XOR kappa[k], it is the only value of f[k] that gives the carries into bit k + 1 the difference kappa[k+1] (Lemma S5).

*The phase equations (GPT Sol, answer AO 5 and 6.1).* The participant's counter, run on the class with its E3 count split by the pattern of h on the sixteen bits 0 to 3, 6 to 13, 16, 17, 24 and 25 and
by (b, u, v), records for each of the eight values of (b, u, v) every pattern that occurs in a solution of E3 with an outcome of beta* (records of the participant, not in the package). GPT Sol checked
every recorded pattern against

    h[0] = 0,  h[1] = 1,  h[2] = 1 XOR b,  h[10] = b,  h[16] = h[17] = 0,
    h[11] = 1 XOR h[3],  h[24] = h[3] XOR h[12] XOR u                   (PHASE)

and found no violation in any of the eight cells, whose sets have 88, 88, 108, 132, 108, 132, 88 and 88 patterns in the order b + 2u + 4v. Each of the fourteen outcomes has an E1 count L_j > 0 that
depends neither on y nor on h, so a zero count outside (PHASE) means that no joint root of any of the fourteen outcomes violates (PHASE). The equations are consequences of the count, which the solver
uses as guards; they are not a rule that drops members or solutions.

*The parity certificate (GPT Sol, answer AR 1).* Call the outcomes j = 1 to 7, whose tau ends in 20a0, the *old rows*, and j = 8 to 14, whose tau ends in 60a0 and has bit 14 set, the *new rows*; a row
is also named by the first three hexadecimal digits of its tau. Every joint root h of outcome j, for y in the class, satisfies

    h[6] XOR h[13] XOR h[25] = u XOR tau_j[14],                        (P*)

that is h[6] XOR h[13] XOR h[25] = u on the old rows and u XOR 1 on the new rows. The proof is an exact finite count. The count N3_j of 10.1 counts the quadruples (Y4, E3.h1, Y9, w8), Y4 in the class,
that meet the E3 conditions of outcome j, and by the proof of Lemma V (10.2) these are exactly the quadruples whose E3.h1 is a joint root of outcome j for Q = Y9, y = Y4 and E = Y3 + Y4 + w8. GPT Sol
split every N3_j by the phase (b, u, v) of Y4 and by the parity pi = h[6] XOR h[13] XOR h[25] of the root. The split is a sum of nonnegative integers over an exact enumeration of submasks, through the
identity (z XOR m) - z = m - 2 (z AND m) modulo 2^32 and a carry recurrence with two states in integers, in coordinates of E3 that are a bijection of the counted quadruples; nothing is sampled. With
a = 24, 16, 4, 24, 32, 1 and 6 for the rows 175, 185, 275, 285, 385, 675 and 685:

| rows | phases (b, u, v) with a nonzero count | count in each such phase | pi | count with the other pi |
| --- | --- | ---: | --- | ---: |
| old, all seven | all eight | a * 2^49 | u | 0 |
| new 185, 285, 385, 685 | u XOR v = 1 | a * 2^47 | u XOR 1 | 0 |
| new 175, 275, 675 | u XOR v = 1 and b = 1 | a * 2^47 | u XOR 1 | 0 |

Every other cell has count 0. Every joint root adds at least 1 to the cell of its phase and its parity, so a cell of count 0 holds no root at all: (P*) holds for every joint root of the fourteen
outcomes on the whole class, pointwise and not on average, and it drops no member and no root. The cells add up to the fourteen N3_j of 10.1 exactly: 8 * a * 2^49 = a * 2^52 on the old rows, 4 * a *
2^47 on the new rows 185, 285, 385 and 685, and 2 * a * 2^47 on the new rows 175, 275 and 675 (checked by a helper agent of the participant). In the phase b = 1, u = 0, v = 1, the 2^16 members of the
class with e1 AND 07ef8307 = 070c0307, a separate exact count of a helper agent of the participant, with the function N3_count of the counting program of Section 17 and the parity as one more
condition, gives all fourteen counts with pi = 0 on the old rows, pi = 1 on the new rows and the count 0 with the other pi, as the table says. The cells of the other seven phases are GPT Sol's
evaluation and were not re-run by the participant. The count shows as well that a new row has no joint root when u = v, and a new row 175, 275 or 675 none when b = 0; the solver does not use this, and
the caps below count every row.

*The guard on the third addition (GPT Sol, answer AR 6.1).*

**Lemma J0.** Every joint root h of every one of the fourteen outcomes has h2[0] = 0, that is h[8] = e2[8].

Proof. For all fourteen outcomes tau_j[0] = tau_j[1] = 0, theta_j[0] = theta_j[1] = 1 and gamma[1] = gamma[2] = 0, and mu[0] = 1, mu[1] = 0. By (PHASE) h[0] = 0 and h[1] = 1. In (J1) both carries into
bit 0 are 0. Since eta[0] = eta[1] = 1 and gamma[1] = 0, the carry Q[0] AND (h[0] XOR 1) = Q[0] of the second addition into bit 1 must equal the carry Q[0] AND h[0] = 0 of the first, so Q[0] = 0 and
g[0] = 0; since gamma[2] = 0, the carry maj(Q[1], 0, 0) = 0 of the second addition into bit 2 must equal the carry maj(Q[1], 1, 0) = Q[1] of the first, so Q[1] = 0 and g[1] = 1. Both additions of (J3)
have carry 0 into bit 0. At bit 0, g + h2 adds 0 and h2[0], with sum bit h2[0] and carry 0 out; (g XOR theta) + (h2 XOR mu) adds 1 and h2[0] XOR 1, with sum bit h2[0] and carry 1 XOR h2[0] out. At bit
1, g + h2 adds 1, h2[1] and 0, with sum bit 1 XOR h2[1]; the other adds g[1] XOR theta[1] = 0, h2[1] XOR mu[1] = h2[1] and 1 XOR h2[0], with sum bit h2[1] XOR 1 XOR h2[0]. (J3) at bit 1 requires the
XOR of the two sum bits, which is h2[0], to be tau_j[1] = 0. So h2[0] = 0, and h2[0] is bit 8 of h XOR e2. QED. The zero carries into bit 0 are those of addition modulo 2^32; nothing is guessed. The
participant checked the bits of the fourteen outcomes that the proof reads.

e2[8] is produced at position i = 20 of the traversal (k = 8): e2[8] = E[8] XOR f[8] XOR a[8] with f[8] = y[20] XOR Q[20] XOR h[20] XOR u[20], and every term but h[20] is known when position 20 is
reached, h[8] among them. So Lemma J0 is a forward guard that sets h[20] = h[8] XOR E[8] XOR a[8] XOR y[20] XOR Q[20] XOR u[20]. It holds for every joint root, so no root is lost, and position 20,
which no constant and no carry prescribes on any row, is no longer free.

*The constants and guards of an outcome.* For y in the class, every joint root of outcome j has the following values, which the solver computes from Q, y, E and the outcome before it branches, or
checks during the traversal (GPT Sol, answers AE 2.1, AF 1.2, AN 6, AO 6.1 and AR 2 and 6.1). Every member of the class has y[0] = 0, y[1] = 1 and bits 16 to 19 of y equal to 0, 0, 1, 0, so f[20] =
f[21] = 0, bits 4 to 7 of f are the constant 2, the carry u[20] is Q[19], and the first addition is reset as in the sub-class.

(a) *The carry into bit 22.* For each guess a[20] = 0 and a[20] = 1, with a'[20] = a[20] XOR kappa[20], run bits 20 and 21 of both additions of (J2) with f[20] = f[21] = 0, and keep the guess only if
a'[21] = a[21] XOR kappa[21] and a'[22] = a[22] XOR kappa[22]. If no guess is kept, the outcome has no joint root. Two kept guesses have the same carries into bit 21, and so into bit 22: all fourteen
outcomes have sigma[20] = sigma[21] = 1, eps[20] = 0 and eps[21] = 1, and the cases E[20] = E'[20], E[20] = 0 with E'[20] = 1, and E[20] = 1 with E'[20] = 0 give, in turn, at most one guess that
passes bit 21, equal carries into bit 21 for both guesses, and at most one guess that passes bit 22. Write a[22] for the common carry.

(b) f[22] is its prescription (D[22] = 1). If gamma[3] = 0, then D[23] = 1 and f[23] is its prescription; if gamma[3] = 1, f[23] = 1 XOR Q[3] XOR y[3]. Run bits 22 and 23 of (J2); if a'[23] is not
a[23] XOR kappa[23] or a'[24] is not a[24] XOR kappa[24], the outcome has no joint root. This gives a[24].

(c) h[0] = 0, h[1] = 1 and u[2] = 0; h[2] = y[2] XOR f[22] XOR Q[2], and the outcome has no joint root unless h[2] = 1 XOR b; u[3] = maj(h[2], Q[2], 0); h[3] = y[3] XOR f[23] XOR Q[3] XOR u[3] and
u[4] = maj(h[3], Q[3], u[3]); h[10] = b and h[11] = 1 XOR h[3]; u[11] = maj(h[10], Q[10], Q[9]) if gamma[10] = 0 and u[11] = Q[10] if gamma[10] = 1; u[12] = maj(h[11], Q[11], u[11]).

(d) f[0] is its prescription with a[0] = 0 (D[0] = 1), and a[1] = maj(E[0], f[0], 0); h[12] = y[12] XOR f[0] XOR Q[12] XOR u[12], u[13] = maj(h[12], Q[12], u[12]) and h[24] = h[3] XOR h[12] XOR u.

(e) Bit 16 of h2 is 0, so f[24] = h[24] XOR E[24] XOR a[24]; h[4] = y[4] XOR f[24] XOR Q[4] XOR u[4] and u[5] = maj(h[4], Q[4], u[4]). Run bit 24 of (J2); if a'[25] is not a[25] XOR kappa[25], the
outcome has no joint root. f[25] is its prescription (D[25] = 1), a[26] = maj(E[25], f[25], a[25]) and h[5] = y[5] XOR f[25] XOR Q[5] XOR u[5].

(f) Bits 6, 13, 25 and 26 depend on the kind of the outcome; (P*) is used on every row.

- *Low old rows, 175020a0, 275020a0 and 675020a0:* if E[1] = a[1], the carry into bit 2 is E[1], f[2] is its prescription (D[2] = 1) and e2[2] = E[2] XOR f[2] XOR E[1]; otherwise the outcome has no
  joint root if kappa[2] = 1, and e2[2] = E[2] XOR kappa[3] if kappa[2] = 0. Then h[26] = 1 XOR h[2] XOR e2[2] XOR Q[26] XOR Q[25], f[26] = h[26] XOR E[26] XOR a[26] and h[6] = f[26] XOR y[6] XOR
  gamma[7]. By (P*), h[25] = h[6] XOR h[13] XOR u: a forward guard, set once bit 13 of h is chosen.
- *High old rows, 185020a0, 285020a0, 385020a0 and 685020a0:* h[25] = e2[1] (answer AE 2.1), where e2[1] = E[1] XOR f[1] XOR a[1] and f[1] = y[13] XOR Q[13] XOR h[13] XOR u[13]. With (P*), h[6] =
  h[13] XOR h[25] XOR u = y[13] XOR Q[13] XOR u[13] XOR E[1] XOR a[1] XOR u, in which h[13] cancels: h[6] is fixed by (c) and (d), which give u[13] and a[1]. The guard of position 25 is then h[25] =
  h[6] XOR h[13] XOR u, the same as h[25] = e2[1]. h[26] = e2[26] (bit 18 of h2 is 0), and e2[26] is given by position 6, whose value is now fixed, so h[26] is a constant of the row.
- *The seven new rows, 175060a0 to 685060a0:* h[25] = h[24] and h[26] = Q[26]; so f[26] = h[26] XOR E[26] XOR a[26] and h[6] = f[26] XOR y[6] XOR gamma[7] are fixed (answer AN 6), and by (P*) h[13] =
  h[6] XOR h[24] XOR u XOR 1 is fixed as well.

(g) h[16] = h[17] = 0, h[18] = 1 XOR Q[18], h[19] = Q[19], and, if gamma[7] = 1, h[7] = 1 XOR gamma[8] XOR h[6], now a constant on every row.

On every row h[29] = 1 XOR e2[29] (bit 21 of h2 is 1), where e2[29] is known once bit 9 of h is chosen, and h[20] is set by Lemma J0. These are the *constants and guards* of the outcome. On every row
h[0] to h[6] are fixed before the traversal; the guards that read bits chosen during the traversal are those of position 20 (every row), position 25 (the old rows) and position 29 (every row). In
entry 26ebba63 the parity h[25] = h[6] XOR h[13] was a condition of rule A on the sub-class; here (P*) is not a rule but a consequence of the count of the class, true of every joint root.

*One traversal.* Every carry guess a[20] that (a) keeps reaches, after the constants h[0] to h[6], the same state: the same bits h[0] to h[6], the same carries u[7] and a[27], and the same e2[26]; the
values e2[20] and e2[21], which depend on the guess, are not used by any guard. So the solver walks bits 0 to 6 under both kept guesses with the tests of (a), (b) and (e), then drops the guesses and
starts one depth-first traversal for each searched outcome at depth 7 from that state, and checks (J1), (J2) and (J3) as words at each leaf, which enforces the closure of the carries that the guess
stood for (GPT Sol, answers AO 2 and 6.1 and AR 2). Every joint root survives a guess and reaches this common state, and a single traversal over the bits of h reaches every h at most once.

*Transitions.* For each position i = 7, .., 31, with k = (i + 20) mod 32, each pair (u[i], a[k]) of incoming carries and each value v of h[i], put g[i] = Q[i] XOR v XOR u[i], u[i+1] = maj(Q[i], v,
u[i]) and u'[i+1] = maj(Q[i], v XOR eta[i], u[i] XOR gamma[i]), and require u'[i+1] = u[i+1] XOR gamma[i+1] if i < 31; put f[k] = y[i] XOR g[i], e2[k] = E[k] XOR f[k] XOR a[k], a[k+1] = maj(E[k],
f[k], a[k]) and a'[k+1] = maj(E'[k], f[k] XOR sigma[k], a[k] XOR kappa[k]), and require a'[k+1] = a[k+1] XOR kappa[k+1] if k < 31. A value that passes is an arc to the pair (u[i+1], a[k+1]), or to
(u[i+1], 0) if k = 31, since both carries into bit 0 of (J2) are 0 (kappa[0] = 0: E'[0] differs from E[0], eps[0] = 1 and sigma[0] = 0 for all fourteen outcomes); the arc records v and e2[k]. The
*descriptor* of a position is 14 bits: Q[i], y[i], E[k], E'[k], eta[i], gamma[i], sigma[k], kappa[k], gamma[i+1], kappa[k+1], whether the position has a constant and its value, and whether i = 31 and
k = 31 (GPT Sol, answer AI 1). The solver reads the arcs from three arrays built once per run (answer AR 6.2), each entry computed by the relation above, which is the same relation and not an
approximation; an arc is five bits, the next carry pair, h[i], e2[k] and a validity bit:

| array | key | words | entry |
| --- | --- | ---: | --- |
| forced | descriptor and carry pair | 2^16 | the one passing arc, or invalid |
| dual | descriptor and carry pair | 2^16 | both arcs, packed in one word |
| selected | descriptor, carry pair and a desired bit | 2^17 | the passing arc whose e2[k] is the desired bit, or invalid |

A position with a constant reads the forced array with the constant in its descriptor. A position i < 31 with gamma[i] = 1, or with k < 31 and D[k] = 1, has at most one passing value by Lemma S5 and
reads the forced array as well. A position with a guard on bits chosen during the traversal, 25 on the old rows and 29 on every row, reads the forced array with the value of the guard written into the
constant field of its key: 1 XOR e2[29], from the saved bit e2[29], and h[6] XOR h[13] XOR u, from bit 13 of the prefix of h. Position 20 reads the selected array with the desired bit h[8] (Lemma J0);
as e2[8] changes with h[20], at most one arc has it. A free position (below) reads the dual array. So a position that is not free has at most one child.

*The search.* From the common state at depth 7, search depth first over the positions 7 to 31: a node at depth d has a child at depth d + 1 for each arc of position d from its carry pair that meets
the guards of the position. A node at depth 32 is a *leaf*; it gives a root when its h satisfies (J1), (J2) and (J3) as words. The root is returned with the outcome j.

*Counts.* Call a position i >= 7 *free* when it has no constant and no guard, gamma[i] = 0 or i = 31, and D[(i + 20) mod 32] = 0, and *prescribed* otherwise. For a row with the set F of free positions
put n_i = 2^(the number of free positions p with 7 <= p < i), for i = 7, .., 32. A traversal of the row has at most n_i nodes at depth i: at most the sum of n_i over the prescribed positions *forced*
nodes, the sum over the free positions *free* nodes, n_20 *selected* nodes among the forced ones (position 20 is prescribed on every row, by Lemma J0), and n_32 = 2^|F| leaves (GPT Sol, answer AR 6.5;
recomputed by the participant from the free positions):

| tau | free positions | forced nodes | free nodes | selected nodes | leaves |
| --- | --- | ---: | ---: | ---: | ---: |
| 175020a0 | 7, 13, 15, 30 | 142 | 15 | 8 | 16 |
| 185020a0 | 13, 15, 30 | 72 | 7 | 4 | 8 |
| 275020a0 | 9, 13, 15, 30 | 140 | 15 | 8 | 16 |
| 285020a0 | 7, 9, 13, 15, 30 | 278 | 31 | 16 | 32 |
| 385020a0 | 9, 13, 15, 30 | 140 | 15 | 8 | 16 |
| 675020a0 | 13, 15, 30 | 72 | 7 | 4 | 8 |
| 685020a0 | 7, 13, 15, 30 | 142 | 15 | 8 | 16 |
| 175060a0 | 7, 15, 30 | 78 | 7 | 4 | 8 |
| 185060a0 | 15, 30 | 40 | 3 | 2 | 4 |
| 275060a0 | 9, 15, 30 | 76 | 7 | 4 | 8 |
| 285060a0 | 7, 9, 15, 30 | 150 | 15 | 8 | 16 |
| 385060a0 | 9, 15, 30 | 76 | 7 | 4 | 8 |
| 675060a0 | 15, 30 | 40 | 3 | 2 | 4 |
| 685060a0 | 7, 15, 30 | 78 | 7 | 4 | 8 |

Against the solver with the phase guards alone (GPT Sol, answer AO 6.2), position 20 is no longer free on any row (Lemma J0), and (P*) fixes position 25 on the old low rows, position 6 on the old high
rows and position 13 on the new rows; no position becomes free. These are counts of the static trees: an arc that fails a carry test or a guard only removes nodes, and the trees that occur may be
smaller.

The outcomes searched in a passing outer step have their bits set in the mask of Y9 under (1). By the certificate of Section 8 every nonzero mask under (1) is m, m << 7 or m OR (m << 7) for one of the
twelve nonzero seven-bit masks m, and each of these is a subset of {275020a0}, {175020a0, 675020a0}, {285020a0, 385020a0} or {185020a0, 385020a0, 685020a0}. So the searched outcomes are among the rows
of one of these four sets, each row in its two versions ..20a0 and ..60a0. With both versions of every row, whether or not the phase of the outer step excludes the new rows, the four sets have 2, 4, 4
and 6 rows; (216, 22, 12), (332, 32, 18), (644, 68, 36) and (548, 54, 30) forced, free and selected nodes; and 24, 36, 72 and 60 leaves. A leaf gives at most one root. So a passing outer step has at
most 6 searched outcomes, 72 leaves and 72 roots, whatever its words. The certificate re-proves for the seven new rows the exclusions between rows that it gives for the seven old ones; it does not
assume them.

*Families.* Within one of the four sets the rows fall into *families* by three marks: low row (175, 275, 675) or high row (185, 285, 385, 685), the bit gamma[10], and old or new row. gamma[3] is 0 on
the low rows and 1 on the high rows, gamma[10] is 1 on the rows 675 and 685 and 0 on the others, and sigma[20] to sigma[26] and sigma[0] to sigma[3] are the same on all low rows and on all high rows;
gamma[10] fixes the reset of u[11] in (c). So the formulas of (a) to
(e) and the walks of bits 0 to 5 under both guesses are the same for the rows of a family and are evaluated once per family (GPT Sol, answer AR 6.4). The four sets have 2, 4, 2 and 4 families, and at
most two rows of a set share a family. gamma[7] can differ within a family, so bit 6 and its outgoing carries, h[6], h[7], h[26] and, on the new rows, h[13] are computed for each row: no prefix of
seven bits is shared.

*What is proved and by whom.* The phase equations, the guards of (c), (d) and (e), the single traversal and the common state are GPT Sol's (answers AO 5, 6.1 and 6.2 and AR 2), on the constants of
answers AE 2.1, AF 1.2 to 1.4 and AN 6 and the transition relation of answer AI 1; the parity certificate (P*), Lemma J0, the guards of (f) with (P*), the three arrays, the families and the counts of
the static trees are GPT Sol's answer AR (1, 2 and 6.1 to 6.5). The participant recomputed the free positions from those of answer AO 6.2 and the new guards, the node, leaf and selected counts of the
table and of the four sets, the families, the bits of the fourteen outcomes that Lemma J0 reads, and the sums of the parity certificate against the counts of 10.1; the other constants and guards were
not re-derived by the participant. Answer AR 6.3 charges the tests of positions 25 and 29 after a read of the forced array; these positions are not prescribed by the carries (gamma[i] = 0 and D[k] = 0
there, on the old rows for position 25 and on every row for position 29: a computation of the participant), so this text writes the value of the guard into the key before the read, within the same
allowance (Section 11). Lemma CV (10.2) states what the solver returns. The layout is specified and charged by this text; it is not an implementation (9.5).

**9.5 Checks of the joint solver.** The solver of 9.4 for the class, in the layout of 9.4 and with the schedule of Section 11, has not been implemented or run for this package: its completeness rests
on the proofs cited in 9.4, on the count of the class and on the parity certificate, and its cap of 56,096 machine units on the schedule of Section 11, an upper allowance written out by blocks and not
a count of an executed program. For entry 26ebba63 a participant implementation of the solver of that entry, with rule A, the seven outcomes and a traversal per carry guess, was compared with an
earlier solver on 332,000 passing outer steps of real walks and on 8,400 planted instances, with the same roots in every step and every planted root found, and no step exceeded the bound of that
entry. Those checks concern other guards and are reported only as context; the organizer runs none of them.

**9.6 Seven outer steps in one word (GPT Sol, answer AQ).** The batch of step 1 of 9.1 runs on packed 256-bit words with the seven 36-bit lanes of 6.5: lane i is bits 36 i to 36 i + 35 of a word, and
it holds a 32-bit value in its low 32 bits with four guard bits above them. The conventions are those of 6.5 and of Lemma CB (d). The low 32 bits of a lane are the scalar value modulo 2^32, and every
lane of every sum stays below 2^36, so that no carry leaves its lane; where an interval bound of a sum could reach 2^36, an AND with the word M that has the low 32 bits of every lane set is made
first, and charged. x - z is formed as x + (z XOR M) + 1, never by a packed subtraction, whose borrows could cross lanes. A rotation by r is PROR: ((x >> r) AND A_r) OR ((x << (32 - r)) AND B_r), five
operations, with A_r and B_r the masks of its two parts in every lane. The addition of a constant is kept pending until the value is read by an XOR, an OR, a shift, a rotation or a table index, and
the one addition that then forms it is charged. All interval bounds depend on the lines and the constants only, not on the words.

*What a batch computes.* Each of R_0 to R_7 is drawn and ANDed with M, except R_7, which is ANDed with the word that has the bits of fc307cfc set in every lane; lane i of R_k is then the k-th word of
the random word of lane i. The lines of step CO, the program's `ctr_outer`, run on the packed words, with y = (W AND fc307cfc) + (030c0303 - Y3), a pending constant addition, in place of the program's
deposit of a member number, and without the lines whose values reach neither Y9 nor omega = Y3 + y + w8. Then omega, and in each lane i the automaton of (2) on omega and that of (1) on Y9, each for
the fourteen outcomes: for each byte of the lane a shift by 36 i plus eight times the byte's position, an AND with 255, the addition of the state from the second byte on, and one table load; then the
AND of the two masks, its test against zero and the branch. Both automata run in every lane, whatever the mask of (2). Last, the seven-bit pass bitmap is formed and stored with R_0 to R_7, which a
passing lane reads back.

**Lemma PL (the lanes are independent ordinary outer steps).** (a) The random words of the RUN_STEPS outer steps of a run are independent and uniform on the 2^256 words, and the algorithm reads no
other bit of R_0 to R_7: the guard bits, bits 252 to 255 and the lanes 2 to 6 of the last batch are not used. (b) The seven outer words and the member of an outer step are independent; the outer words
are uniform words, and the member is uniform on the class, as when the eighth word modulo 2^19 is the member number (Section 8). (c) So the outer steps of a run are independent and identically
distributed, and each has the law of an outer step that draws its own uniform 256-bit word: every count of an outer step, among them the count N_o of H1' and the pass of H4', has the law that it has
for such an outer step. The algorithm is a function of the RUN_STEPS random words, the probability space of 10.4.

Proof. (a) The low 32 bits of lane i of R_k are a set of bit positions of R_k, and these sets are disjoint for different lanes; different k and different batches are different draws. So the random
words of different outer steps are made of disjoint sets of the independent uniform bits of the draws, and they are independent and uniform. The batch reads R_k only through its AND with M or with the
word of fc307cfc, and a passing lane reads only its own lane of the stored words; so no other bit is read. (b) The bits of 030c0303 and of fc307cfc are disjoint, so the addition is an OR: e1 has the
value 030c0303 at the 13 positions of 03cf8303 and the bits of W at the other 19, so y = e1 - Y3 is the member of the class (Lemma Q) whose number is the 19 bits of W at the free positions (Section
8). For a uniform W this number is uniform on 0 to 2^19 - 1, as W modulo 2^19 is, and it is a function of the eighth word alone. (c) An outer step and everything computed from it are functions of its
random word only, so (c) follows from (a) and (b). QED. Packing is a representation of disjoint fresh random bits: it adds no premise to H1' and H4' (GPT Sol, answer AQ 1).

**Lemma PB (the batch computes the outer steps of its lanes).** In every used lane of a batch, the low 32 bits of the packed words that the batch forms for Y9 and omega are the values Y9 and omega =
Y3 + y + w8 of step CO for the outer step of that lane; the masks that the lane reads from the two automata are those of (1) on Y9 and of (2) on omega; and the lane is taken as passing exactly when
its outer step passes the filter of Section 8. No sum leaves its lane.

Proof. Every line of step CO is an addition, subtraction, XOR or rotation of 32-bit words. On packed words an XOR, an OR and an AND with a constant act on each bit; an addition acts on each lane
separately while no lane reaches 2^36, and the low 32 bits of a lane are then the sum modulo 2^32; x + (z XOR M) + 1 has the low 32 bits of x - z modulo 2^32; and PROR gives in the low 32 bits of each
lane the rotation of the low 32 bits of that lane, whatever its guard bits, since A_r and B_r keep only bits that come from the low 32 bits of the same lane. The dropped lines reach neither Y9 nor
omega, so their absence changes neither. A table index takes bits 8 p to 8 p + 7 of the low 32 bits of lane i, as the program's `ctr_look` takes byte p of the scalar word, so the masks and the test
are those of the filter of Section 8. The bound of every lane at every operation is a function of the lines and the constants; the participant implementation below carries it through every operation
and makes the AND with M wherever a sum could reach 2^36, so no lane reaches 2^36. QED. That bound computation is the participant's, a finite computation on the lines and the constants, not on the
words. It was made with the mask f8107cfc of the sub-class in place of fc307cfc; W AND either mask is below 2^32 and the pending constant is the same, so the bounds of the lines are the same.

*The count of a batch.* On the machine of Section 11, with 64 registers and every constant an immediate, the batch is straight-line code with the same count in every batch. The participant
implementation counts 400 units without the automaton of (1): the eight random words, one operation and one AND each, 16; the lines of step CO that reach Y9 or omega, 261; omega, 2; the automaton
of (2) in the seven lanes with the test of its mask and the branch, 118; the advance of the batch count, its comparison with RUN_BATCHES and the branch, 3. The automaton of (1) in all seven lanes, the
AND with the mask of (2), its test and the branch add 125. At most 25 registers are live, the two counts included, and nothing is spilled. GPT Sol's certificate (answer AQ 2) adds 14 for the base
addresses of the first tables of the two automata in the seven lanes (every other table entry holds the base address of the next table, written once with the automata), 64 for storing R_0 to R_7 and
the counts, masks and cursor of the caller in fixed memory words, 21 for forming and storing the pass bitmap, and 16 for the test of the last batch and the dispatch to the passing lanes: 400 + 125 +
14 + 64 + 21 + 16 = 640 units per batch (Section 11). The implementation formed the member with the mask of the sub-class and ran the automata of its seven outcomes; for the class the member is the
same AND with another mask and the same pending addition, and the automata of the fourteen outcomes have the same four byte lookups per lane, with masks of fourteen bits (GPT Sol, answers AN 1 and AQ
2), so the count is the same.

*A passing lane.* The lanes whose bits are set in the pass bitmap are taken in increasing order. For each, after the pass count and its test (step 1 of 9.1): its eight words are reloaded from the
stored R_0 to R_7 and taken out of lane i by a shift and an AND, and step CO runs on scalar words, giving all the names that steps 2 and 3 read, 295 units in the participant's count; then steps 2 and
3 run and may use all 64 registers, the state of the batch being stored before them and reloaded after them. Section 11 charges 512 for the lane outside steps 2 and 3 and 56,096 for steps 2 and 3.

*The participant check.* A participant implementation of the batch, which is not part of the package, ran 142,858 batches, 1,000,006 outer steps drawn from SHAKE-256, with the program's own functions
(`ctr_outer`, `ctr_tables`, `ctr_look`, `ctr_filter`, the same lines as in the package) as the reference, with the mask and the seven outcomes of the sub-class that the program holds. In every lane
all names of step CO and the mask of the filter equal those of the program's scalar `ctr_outer` and `ctr_filter` run on the eight words of the lane with its member number: 1,000,006 of 1,000,006. The
rebuilt names of the passing lanes equal those of `ctr_outer` in 4,452 of 4,452 rebuilds, and the counts are the same in every batch. The batch with the mask of the class and the automata of the
fourteen outcomes has not been run. These are participant measurements; the organizer does not run them.

## 10. The rate of a counter trial and the success probability

**10.1 The model rate.** The seven-word model M of Section 13 treats the residual of a trial as a function of seven words, E1.d1, E1.b1 and E1.a2 of message A and Y4, Y9, w8 and E3.h1. In this package
Y4 is uniform in the class of eta, not in the sub-class, and the other six are independent uniform words, so M has 2^192 * 2^19 = 2^211 inputs. Under M the rate of the class is 85074516985129 /
524288 = 162,266,763.66 (Section 13): a trial has R = 0 with probability that number times 2^-128. The part of a value beta of E1's first-half b difference in it is written r(beta); the part of beta*
is 71,698,432. A trial of Section 8 has c1 in Q* and so the difference beta* (Theorem C (iv)); under M the event that c1 = Y11 + E1.d1 lies in Q* has probability 2^-11 and is the event that the
difference is beta* (Lemma S1). The rate of a trial that M conditions on c1 in Q* is therefore

    p = 2^11 * 71,698,432 * 2^-128 = 146,838,388,736 * 2^-128 = 35,009 * 2^-106,

about 2^-90.905. It is 904.92 = 2^9.822 times the model rate of a trial of the class.

*The fourteen outcomes of beta*.* In the count of Section 13 an outcome of beta is a pair (tau, eps) of the differences of E1's a and c outputs. For an outcome j of beta*, L_j is the number of triples
(E1.c1, E1.b1, E1.a2) of words for which E1 on A and on B (6.2) gives the differences beta*, tau_j and eps_j; and N3_j is the number N3 of step 3 of the count for that outcome: the number of
quadruples (Y4, E3.h1, Y9, w8), Y4 in the class, for which E3 on A and on B gives the differences eta and tau_j XOR ROR(tau_j, 1) of its first-half d and b values and tau_j and eps_j of its c and a
outputs. Every input of the 2^211 of the model falls into one outcome, so r(beta*) = sum over j of L_j N3_j / 2^83. Beta* has fourteen outcomes on the class, all with eps = 6e21be55:

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
| sum | | | | 71,698,432 |

The rows j = 1 to 7 have the L_j of the sub-class of entry 26ebba63 and four times its N3_j, so on this scale they carry its 67,698,688; the rows j = 8 to 14 add 3,999,744. 71,698,432 = 35,009 * 2^11,
so p = 35,009 * 2^-106 exactly. The integers L_j and N3_j are those of the participant's counting program, printed with its output in Section 17; it prints L_j N3_j / 2^81, four times the last column,
and their sum 286,793,728 = 4 * 71,698,432, and the scale 2^83 is that of a trial with Y4 uniform in the 2^19 members of the class (GPT Sol, answer AQ 3). Of the 52 values of tau that pass the screens
of the count, 30 have N3_j > 0 and 14 have L_j N3_j > 0. The count uses no rule on h1.

*Why beta*.* Beta* is not chosen by a ranking in this package: it is the beta of the solution with which the solver found the six constants, and it is stored with them in the advice record of 18.6.
Its cube of c1 has k = 11 fixed bits, mask 0e09818b and value 02008000. On the sub-class of entry 26ebba63, GPT Sol 6.1 ranked the 53 values of beta with a part by their conditional rates 2^k r(beta),
and beta* was first. The program stores beta* (`CTR_BETA`) and the mask and value of its cube.

**10.2 Lemmas on the counter sampler (GPT Sol 6.1).** The following lemmas were proved by GPT Sol 6.1 for this construction, Lemma S9 by GPT Sol in its answer AC, and are given with their hypotheses;
each is exact mathematics under the hypotheses stated. The participant compared Lemmas S1 to S4 and Lemma IP with the construction line by line; the carry Lemmas S5 to S7 were not re-derived by the
participant. They do not prove the rate of H1' or the success probability; 10.3 states what remains a premise. The proofs of Lemmas S1 and S9 hold for any fixed set of members (GPT Sol, answer AN 1);
here the set is the class.

**Lemma S1 (conditioning the model).** *Hypotheses:* under M the six words E1.d1, E1.b1, E1.a2, Y9, w8 and E3.h1 are independent uniform words, independent of Y4, which is uniform in the class; c1 =
Y11 + E1.d1. *Statement:* c1 lies in Q* with probability 2^-11, and that is the event that E1's first-half b difference is beta*. Conditional on it, E1.d1 is uniform on Q* - Y11, E1.b1 and E1.a2 keep
their independent uniform laws, and (Y4, Y9, w8, E3.h1) keeps its law and stays independent of (E1.d1, E1.b1, E1.a2). Hence Pr_M(R = 0 | c1 in Q*) = 2^11 Pr_M(R = 0 and c1 in Q*) = 2^11 * 71,698,432 *
2^-128 = p, the last step by the count of 10.1.

*Proof.* Translation by Y11 makes c1 uniform and independent of every other coordinate. By the identity of the proof of Theorem C (iv), c1 lies in Q* exactly when the difference is beta*, and Q* fixes
11 bits of c1, so the probability is 2^-11. The event depends on E1.d1 alone, so for every event G1 of the words of E1 and G3 of the words of E3, Pr_M(G1 and G3 | c1 in Q*) = Pr_M(G1 | c1 in Q*)
Pr_M(G3). No independence of the output differences inside E1 or inside E3 is used. QED. The finite counts behind 71,698,432 are those of the counting program of Section 17 and are not proved by this
lemma.

**Lemma S2 (the outer chart).** *Hypotheses:* y and c1 are fixed; the seven outer words are independent uniform words; the names obey the assignments of step CO, with flags 3 and v[13] = 0.
*Statement:* the seven outer words are in bijection with the seven context words (C0.c1, C0.d1, D3.d1, S15, S9, w5, X2) of Section 4. These are therefore independent uniform words, and their law does
not depend on c1 or y.

*Proof.* Given the context words, these assignments, which are lines of steps O and M of Section 4 with flags 3 in place of 11, return the outer words: S2 = K2.a1 + K2.b1 + w5; S14 = ROR(K2.d1 XOR S2,
8); D3.a1 = ROL(D3.d1,16) XOR S14; D3.b1 = X3 - D3.a1; D3.c1 = S9 + D3.d1; S4 = ROL(D3.b1,12) XOR D3.c1; S3 = D3.a1 - S4; X14 = ROR(D3.d1 XOR X3, 8); X9 = D3.c1 + X14; K3.d1 = ROL(S15,8) XOR S3; w6 =
(ROL(K3.d1,16) XOR 3) - IV[3] - IV[7]; S11 = IV[3] + K3.d1 + S15; X8 = C0.c1 - C0.d1; D2.b1 = ROL(X7,7) XOR X8; D2.a1 = X2 - D2.b1 - W13. Substituted into K2, D3, K3 and D2 they return w5, D3.d1, S9,
S15, X2, C0.c1 and C0.d1, and the lines of step CO, run on the outer words they return, give the context words back. Both maps are inverse bijections between two sets of 2^224 elements, and the
uniform law is carried to the uniform law. QED.

**Lemma S3 (two independent offsets).** *Hypotheses:* those of Lemma S2. *Statement:* (w5, D3.a1, Y12, S15, X2, X8, C0.d1) is another chart of the outer words, so these seven are independent uniform
words; in particular Y12 and w5, which E1 reads, are independent uniform words.

*Proof.* The chart is reached by replacements of coordinates, each a bijection with the other coordinates held fixed: (w6, S11) by (S3, S15), with inverse K3.d1 = ROL(S15,8) XOR S3, w6 =
(ROL(K3.d1,16) XOR 3) - IV[3] - IV[7], S11 = IV[3] + K3.d1 + S15; (D2.a1, D2.b1) by (X2, X8), with D2.b1 = ROL(X7,7) XOR X8 and D2.a1 = X2 - D2.b1 - W13; (S3, S4, X9) by (D3.a1, S4, S14), with inverse
D3.b1 = X3 - D3.a1, D3.d1 = ROR(S14 XOR D3.a1, 16), X14 = ROR(D3.d1 XOR X3, 8), D3.c1 = ROL(D3.b1,12) XOR S4, X9 = D3.c1 + X14, S3 = D3.a1 - S4; S14 by w5, with S2 = K2.a1 + K2.b1 + w5 and S14 =
ROR(K2.d1 XOR S2, 8); at fixed D3.a1 and S14, S4 by X4, with inverse X9 = ROL(X4,7) XOR D3.b1, D3.c1 = X9 - X14, S4 = ROL(D3.b1,12) XOR D3.c1; and last, with C0.c1 = X8 + C0.d1, X4 by Y12, with
C0.b1 = (Y12 + C0.c1) XOR ROL(y,7) and X4 = ROL(C0.b1,12) XOR C0.c1. The composition proves the chart and the uniform law. It says nothing about the independence of Y12 and w5 from functions that also
depend on them, such as the residual. QED.

**Lemma S4 (a marginal and the physical conditioning).** *Hypotheses:* those of Lemmas S2 and S3, and c1 independent of the outer words. *Statement:* (a) At each fixed c1 and y, E1.a1 and E1.a2 -
E1.b1 are independent uniform words. (b) For two members c1 and c1' of Q* in one outer step, put m4 = ROL((c1 - Y11) XOR (c1' - Y11), 16); then the difference of their values of E1.a2 - E1.b1 is m4 -
2 (E1.a1 AND m4), E1.a1 being that of c1, and conditional only on the value of E1.a2 - E1.b1 at c1 it is uniform on the values m4 - 2 s, s a submask of m4 AND 7fffffff, which are all different. (c)
Let a baseline sampler draw t as a uniform 32-bit word, t = 0 included as an algebraic trace, with flags 3, the same constants and the same outer words, and solve c1 from it; then c1 is uniform and
independent of the outer words and y, and the sampler of Section 8, c1 uniform in Q*, is exactly the baseline conditioned on c1 in Q*: for every event of the trace, its probability under the sampler
of Section 8 is 2^11 times the probability under the baseline that it happens and c1 lies in Q*.

*Proof.* (a) By Lemma S3, Y12 and w5 are independent uniform, so E1.a1 = ROL(E1.d1,16) XOR Y12 and w5 are, and E1.a2 - E1.b1 = E1.a1 + w5 by E1's fifth assignment; replacing (E1.a1, w5) by (E1.a1,
E1.a1 + w5) is a bijection. (b) The same outer words give c1' the first value E1.a1 XOR m4 and the same w5, and (X XOR m4) - X = m4 - 2 (X AND m4) modulo 2^32. Conditional on the first value, E1.a1
stays uniform, its bits under m4 AND 7fffffff give the uniform law stated, and different submasks below 2^31 have different doubles. (c) By Lemma IP, c1 -> t is a permutation for every outer step and
y, so a uniform t makes c1 uniform and independent of them; conditioning on c1 in Q*, an event of probability 2^-11, leaves the outer words and y unchanged, and step CT run forwards from c1 is the
same trace. QED. Statement (c) is about the construction's own sampler and does not identify it with M; it lets an event include t != 0 but does not say how much of the rare success mass the rule t !=
0 removes.

**Lemma S5 (a carry prescription).** *Statement:* let x, s, s', a and d be words of w bits with (x + s) XOR ((x XOR a) + s') = d. Every bit i < w - 1 at which a and d differ is determined by the lower
bits of x and by the constants; so at most 2^(w - n1) words x solve the equation, n1 being the number of bits of (a XOR d) AND (2^(w - 1) - 1).

*Proof.* Write u_i and u'_i for the carries into bit i of the two additions. Equality at bit i gives a_i XOR d_i = s_i XOR s'_i XOR u_i XOR u'_i. If its left side is 1, exactly one of the pairs (s_i,
u_i) and (s'_i, u'_i) has unequal bits; the carry out of that addition is its variable input bit, x_i or x_i XOR a_i, and the carry out of the other addition is its fixed common bit. Equality at bit
i + 1 prescribes the XOR of the two carries out, which fixes x_i. Counting the choices from the low bits to the high bits gives the bound; bit w - 1 has no next bit, which is why it is left out. QED.

**Lemmas S6 and S7 of entry 26ebba63**, an E3 prescription and a cap of 3,072 complete successes in one outer step, are stated for the sub-class with rule A and its seven outcomes, and this package
does not use them. Its cap on the successes of one outer step is that of 9.4 with Lemma CV: at most 72 listed good trials (10.3).

**Lemma S8 (success from a mean and a factorial moment).** *Statement:* let N_o be a count with values in {0, 1, ..}, mu = E[N_o] > 0 and rho = E[N_o (N_o - 1)] / mu. Then Pr(N_o > 0) >= mu b(rho),
where b(rho) = (2 r_o - rho) / (r_o (r_o + 1)) and r_o = floor(rho) + 1; for 0 <= rho <= 1 this is 1 - rho / 2, and b decreases with rho. If the outer steps of a run are independent and each has mean
at least mu and ratio at most rho, the probability that some outer step has N_o > 0 is at least 1 - exp(-mu b(rho) times the number of outer steps).

*Proof.* For integers r_o >= 1 and z >= 0, the indicator of z > 0 is at least (2 r_o z - z (z - 1)) / (r_o (r_o + 1)): with equality at z = 0, and for z >= 1 the inequality is (z - r_o)(z -
r_o - 1) >= 0, which holds for integers. Taking expectations gives the first statement. For independent outer steps, the probability that none has N_o > 0 is the product of the values 1 - Pr(N_o > 0)
of the outer steps, at most exp(-mu b(rho) times their number). QED.

**Lemma S9 (the success mass lies on passing outer steps; GPT Sol, answer AC).** (a) *No hypothesis.* In every outer step that does not pass the filter, the count N_o of H1' (10.3) is zero. Let pi_o
be the probability that an outer step of step 1 of 9.1 passes the filter, the share of the 2^256 values of its random word whose outer step passes. If pi_o > 0, then E[N_o | the outer step passes] =
E[N_o] / pi_o.
(b) *Hypotheses:* those of Lemma S1. Under M, also conditional on c1 in Q*, Y9 and omega = Y3 + Y4 + w8 are independent uniform words, and the filter passes with probability pi. Let S be the event
that R = 0 and the E1 outcome is one of the fourteen; given c1 in Q*, S has probability p under M (Lemma S1 and the count of 10.1). S lies inside the event that the filter passes. So Pr_M(S | c1 in Q*
and the filter passes) = p / pi = 2,693 / (116,987,466,011 * 2^58), about 2^-83.373, and Pr_M(the filter passes | c1 in Q*) times this conditional rate is p: conditioning on the pass loses no part of
p.

*Proof.* (a) A listed good trial has R = 0 with one of the fourteen outcomes, so by Lemma F its outer step passes; N_o is a count that is zero off the event that the outer step passes, and E[N_o] =
pi_o E[N_o | the outer step passes].
(b) Under M, Y9 and w8 are independent uniform words, independent of Y4; for fixed Y4, w8 -> omega is a translation, so (Y9, omega) is uniform on all 2^64 pairs and independent of Y4, and Lemma S1
leaves the law of (Y4, Y9, w8, E3.h1) unchanged under c1 in Q*. The proof of Lemma F uses only the assignments of E3 and the conditions of R = 0, which hold for the model words, so it gives the
inclusion; by 10.1 all of p comes from the fourteen outcomes. Dividing by the probability pi of the pass gives the conditional rate. QED. Statement (a) uses the pass probability pi_o of the sampler
itself; that pi_o equals pi is not proved (H4'). Statement (b) is about M and says nothing about the sampler.

*The search lists exactly the listed good trials.* The two lemmas below concern the search of 9.1. Lemma V follows from 3.3 and is the participant's; Lemma CV rests on the constants and guards of 9.4,
proved by GPT Sol (answers AE 4 and 7, AF 1.3, AO 6.1 and AR 1, 2 and 6.1), among them the parity certificate (P*) and Lemma J0, which hold for every joint root on the class.

**Lemma V (the certificate of a root).** Fix an outer step, a word c1 in Q* and an outcome j of beta*, and let h be E3.h1 of the trial. The trial has R = 0 with E1 outcome j exactly when E1 on A and
on B gives the XOR differences tau_j and eps = 6e21be55 of its a and c outputs and h satisfies the joint conditions (J1), (J2) and (J3) of outcome j (9.4).

*Proof.* Write tau, eps and beta for the XOR differences between A and B of E1's a output, c output and first-half b value, and eta, psi, tau' and eps' for those of E3's first-half d and b values and
its c and a outputs, as in Section 13. beta = beta* because c1 is in Q* (Theorem C (iv)), and eta = 830303cf (Theorem C (iii)). By 3.3, R is formed from o[1] = Z[1] XOR Z[9], o[3] = Z[3] XOR Z[11],
o[4] = Z[4] XOR Z[12] and o[6] = Z[6] XOR Z[14], where Z[1], Z[6], Z[11] and Z[12] are the a, b, c and d outputs of E1 and Z[3], Z[4], Z[9] and Z[14] those of E3. The first two values of E1 are the
same for A and B (proof of Theorem C (iv)), so the d and b outputs of E1 differ by ROR(tau, 8) and ROR(beta XOR eps, 7); by the last three assignments of E3, its b and d outputs differ by ROR(psi XOR
tau', 7) and ROR(eta XOR eps', 8). So R = 0 exactly when tau' = tau, eps' = eps, psi = tau XOR ROR(tau, 1) and eta = eps XOR ROL(beta XOR eps, 1), the conditions of Section 13. For E1 outcome j, tau =
tau_j and eps = 6e21be55, and the last condition holds: 6e21be55 XOR ROL(18b0e098 XOR 6e21be55, 1) = 830303cf. As in the proof of Lemma F, with h' = h XOR eta, g' = Y9 + h' and f' = ROR(y XOR g', 12),
psi = f XOR f' = ROR(g XOR g', 12), so psi = sigma_j exactly when (J1) holds. Then f' = f XOR sigma_j and the a output of E3 on B is (omega + DY3) + f', so eps' = eps exactly when (J2) holds. Then the
d output of E3 on B is ROR(h XOR eta XOR e2 XOR eps, 8) = h2 XOR mu and g' = g XOR theta_j, so tau' = tau_j exactly when (J3) holds. QED.

**Lemma CV (coverage of the search).** Fix an outer step that passes the filter. (a) Step 2 of 9.1 returns every joint root of every outcome whose bit is set in the AND of the two masks, each once,
and nothing else. (b) Run over the whole list, step 3 certifies exactly the roots that are the E3.h1 of a listed good trial of the outer step, and the E3.h1 of every listed good trial of the outer
step is among the roots. So the number of certified roots of a passing outer step is its count N_o of H1' (10.3), the number of its listed good valid trials over all of Q*, and N_o is at most 72.

*Proof.* (a) A leaf gives a root only when (J1), (J2) and (J3) hold as words, so every returned word is a joint root of the outcome it is returned with. Conversely, let h be a joint root of a searched
outcome. By (PHASE), (P*), Lemma J0 and the constants and guards of 9.4 its bits have those values, and its carries pass every test of (a), (b) and (e) there: its own carry into bit 20 is a kept
guess, every kept guess reaches the common state at depth 7, and the single traversal follows the arcs of its bits from the carry pairs that its own carries give, each read from the array of its
position with the guard values that its own bits give, and reaches its leaf, where the three conditions hold. A depth-first traversal reaches each node once, so h is returned once. No word is a joint
root of two outcomes (9.4). (b) Let c1 in Q* give a listed good trial with outcome j, and let h be its E3.h1. By the proof of Lemma F, h witnesses (1)_j for Y9 and the trial's f witnesses (2)_j for
omega, so bit j is set in both masks. By Lemma V, h satisfies (J1) to (J3) of outcome j, so it is a joint root and step 2 returns it by (a). Step 3 maps it to c1, since it computes the inverse of the
permutation c1 -> E3.h1 of Lemma IP; c1 is in Q*, its t is not zero and its E1 outcome is j, so the root is certified. Conversely, a certified root h of outcome j gives a c1 in Q* with t not zero
whose E1 differences are tau_j and eps, and h satisfies (J1) to (J3), so by Lemma V the trial of c1 has R = 0 with outcome j: it is a listed good trial. Different roots give different c1 (Lemma IP),
and a passing outer step has at most 72 roots (9.4). QED.

So in every passing outer step that it reaches, the search of 9.1 certifies exactly the listed good valid trials that an enumeration of all of Q* in that outer step finds, with the same outer steps,
the same members y and the same filter. The count N_o of every outer step is the same, and with it the joint law of the counts of the outer steps of a run: H1' is about these counts and H4' about the
filter and the outer steps, and neither changes (GPT Sol, answer AE 7). Lemmas V and CV use no law of the words. The guards of the solver are lossless: (PHASE) and (P*) are consequences of exact
counts of the class, (P*) with a count of 0 for the other parity in every phase and every outcome (9.4), and Lemma J0 is algebra; none drops a member or a joint root, and drawing the outer steps seven
to a batch changes no outer step (Lemma PL).

**10.3 Heuristics.**

*History label.* H1' and H4' below are the whole-class form of the base text. This entry does not declare them in this form; it declares H1prime-winner and H4prime-winner of Section 18.5, which are
stated for the law of the winner sub-class, its budget B and its pass budget L.

**Heuristic H1' (score-critical).** Over the coins of the run, the RUN_STEPS independent uniform words of step 1 of 9.1, let N_o be the number of listed good valid trials (9.1) of one outer step,
counted over all of Q* whether or not the outer step passes the filter. (i) *Rate:* E[N_o] >= (2^21 - 1) q, with q = FACTOR * 2^-128, just under 5p / 7, about 2^-91.390. (ii) *Dependence:* the listed
good trials of one outer step depend on each other weakly enough that the probability that no valid trial of the run is a listed good trial is at most exp(-0.49676) + 0.001.

This is the premise of entry 26ebba63 in its full form, rate and dependence, scoped to this search: the class of eta with no rule on h1, all fourteen outcomes of beta*, and the independent outer steps
of 9.1, each with its own random word made of disjoint fresh bits (Lemma PL) (GPT Sol, answers AO 3.1 and 6.3, AQ 1 and AR 6.6). It does not follow from the premise of entry 26ebba63, which concerns
the sub-class, rule A and seven outcomes; it is declared for these trials.

In the terms of Lemmas S1 to S4 the premise is this: the construction's pushforward of the uniform outer words and members, with c1 running over all of Q*, onto the seven model words (E1.d1, E1.b1,
E1.a2, Y4, Y9, w8, E3.h1) carries at least the share FACTOR / 146,838,388,736, just under 5/7, of the complete-success integral p of the conditional law of Lemma S1; that stays true after the member
with t = 0 is dropped (Lemma IP); and the dependence between trials that share an outer step is weak enough for the stated success at the declared run length. The two parts are separate: neither
follows from the other, and neither follows from the model or from Lemmas S1 to S9. The factor FACTOR = 104,884,563,382 is assumed; 10.1 gives what it is set against, the count 146,838,388,736, of
which it is five sevenths rounded down. The filter does not change it.

*The rate on passing outer steps.* By Lemma S9 (a), N_o is zero on every outer step that the filter rejects, so (i) says E[N_o | the outer step passes] >= (2^21 - 1) q / pi_o, with pi_o of Lemma S9.
Per member of Q* of a passing outer step the rate is then at least about q / pi_o; for pi_o = pi it is q / pi = 52,442,281,691 / (1,520,837,058,143 * 2^79), about 2^-83.858: the rate of H1' divided by
the pass share, with no part of the counted mass lost (Lemma S9). The success argument below uses (i) per walked outer step and needs no value of pi_o; pi_o enters only the pass budget (H4').

*What is proved and what is not.* Proved (Lemmas S2 to S4): the outer words of a step are uniform in the chart of the seven context words of Section 4; Y12 and w5 are independent uniform words; E1.a1
and E1.a2 - E1.b1 are independent uniform words at every fixed c1; and the sampler of Section 8 is exactly the uniform-counter sampler conditioned on c1 in Q*. Proved as well (Lemmas V and CV, 10.2):
in every passing outer step that it reaches, the search of 9.1 certifies exactly the listed good valid trials of the outer step, so N_o is the same count for it as for an enumeration of all of Q*. Not
proved: that E1.b1, E1.a2, E3.h1, Y9 and w8 have the model's joint law with the rest; GPT Sol 6.1 reduces part (i) to one success-weighted density of seven words that the outer step fixes, Y12, Y1 +
w12, C2.b1, C2.c1, w5, Y9 and w8, and that density has not been counted. Not proved either: how much of the success mass the member with t = 0 carries (Lemma IP bounds the number of dropped trials,
one in 2^21, not their mass), and the dependence inside an outer step.

For part (ii): the outer steps of a run are independent by step 1 and Lemma PL, and by part (i) the run has RUN_STEPS * E[N_o] >= RUN_STEPS * (2^21 - 1) * FACTOR * 2^-128 >= 0.49676. So by Lemma S8
part (ii) holds when rho = E[N_o (N_o - 1)] / E[N_o] <= 0.0065: then b(rho) >= 0.99675, the exponent of Lemma S8 is at least 0.4951455, and exp(-0.4951455) < 0.609483 < exp(-0.49676) + 0.001. That rho
is this small is the assumption; it is not measured and cannot be at full size. What is known of it: an outer step has N_o <= 72 (Lemma CV), so rho <= 71, which does not help at this run length (GPT
Sol, answer AO 1, shows the same for a cap of 64 on the sub-class). GPT Sol 6.1 proves the bound 2^-13 for it in a model in which E1.b1, E1.a2 and E3.h1 are drawn afresh for every member of Q*, and
proves as well that the construction's own pair law is not of that kind: for two members of one outer step the second member's three words take at most 2^62 values given the first's, not 2^96. So that
bound does not transfer. A participant estimate on the sub-class, which is not a proof, also puts rho near zero.

*No budgets of stage 2 and of step 3.* The enumeration of all of Q* that the joint solver replaces had two more halts, a budget of the lanes processed in its step 3 and a budget E of the words that
enter stage 2, and two more heuristics, H2' and H3', that these budgets do not end the run. The search of 9.1 has neither budget and declares neither heuristic, and it declares no premise on the mean
of any count of work. Steps 2 and 3 need no budget: in every passing outer step, whatever its words, the joint solver returns at most 72 roots and a passing outer step costs at most 56,608 machine
units, the handling of its lane included (9.4, Section 11). The final pair is formed and hashed only for a certified root, after which the run halts, so it is formed at most once and is a collision
(Lemma V). The run halts with failure only when the pass count exceeds PASS_BUDGET, which H4' covers, or after the last outer step, which H1' covers.

**Heuristic H4' (supporting).** With probability at least 0.9995 over the coins, at most PASS_BUDGET outer steps of a run pass the filter; so the pass count does not halt the run. (The outer steps of
a run are independent and identically distributed (step 1 of 9.1 and Lemma PL), and whether one passes is a function of its random word, so the number of passing outer steps is binomial, with
RUN_STEPS steps and the probability pi_o of Lemma S9. pi_o is a fixed number that has not been computed: pi is the share for uniform independent pairs (Y9, omega), and the sampler's Y9 and omega are
not proved to be such. If pi_o <= 1.06 pi, the mean is at most 1.06 / 1.0625 of PASS_BUDGET, and the Chernoff bound puts the probability of more than PASS_BUDGET passing outer steps below exp(-10^13);
a smaller pi_o makes it smaller. Measured with the fourteen-outcome filter in a participant walk of real outer steps: 1,600,000 passing among 296.2 million, 2^-7.5324 against pi = 2^-7.5320 (z =
-0.18), with members drawn from a part of 2^16 members of the class; and with the seven-outcome filter on the sub-class, 2^-9.8127 against 2^-9.8132 (Section 13). Entry dd91b2f6 reports 2^-7.532050 on
real outer steps of the class against the same exact share.) If the budget is reached the run halts with failure; the time bound charges PASS_BUDGET + 1 passing outer steps and is not affected. This
is H4' of entry 26ebba63 for this filter, run and budget (GPT Sol, answer AO 6.3).

*No selection premise.* (History label: entry e85fffe8 left the return of the selection procedure SEL undeclared, and entry 78ac164c declared it as HSEL-selection-return; both were ruled not_evaluable
on that point, 18.9.) This entry declares no premise on what a procedure returns. The values that the search reads are the fixed advice record of 18.6, and by Lemma ADV the claim uses only properties
of that record that this text proves or counts exactly. The computation that found the record is charged as preprocessing under the supporting premise HPRE-discovery-bound (18.6), which bears on the
time bound only.

**10.4 Success probability.** (History label: this subsection computes the success of the whole-class run of the base text; the success of this entry is that of Section 18.5.) The probability space is
the random words of the RUN_STEPS outer steps of step 1 of 9.1, independent uniform 256-bit words made of disjoint bits of the fresh draws (Lemma PL), for the fixed target. The algorithm is otherwise
deterministic. Under H1' and H4' it outputs a collision with probability at least 1 - (exp(-0.49676) + 0.001) - 0.0005 > 0.3915 - 0.0015 = 0.39; the exact value of the bound is 0.390000993950... This
is the union bound over the two events "no valid trial is a listed good trial" and "the pass budget is reached", which need not be independent: H1' bounds the first and H4' the second. A listed good
trial lies in a passing outer step (Lemma F), and the search certifies it unless the run ends before its outer step is reached, by the pass budget or by the output of another pair (9.1, Lemma CV).
When the algorithm outputs a pair, the pair is a genuine collision: its trial is certified, so R = 0 (Lemma V), step 3 checks both complete digests, and the messages have different lengths. The run is
the shortest of this form that gives 0.39: 0.49676 is the smallest number of five decimals for which the bound reaches it, and with 0.49675 in its place the bound is below 0.389995.

*Sensitivity to the factor.* If the valid trials are listed good trials at f * 2^-128 each on average, with the dependence part of H1', the run gives at least 1 - exp(-f * RUN_STEPS * (2^21 - 1) /
2^128) - 0.0005, which reaches 0.39 only when f is at least 104,537,523,355; the assumed FACTOR is 1.0033 times that. The margin of the claim lies between the assumed 104,884,563,382 and the counted
146,838,388,736, a factor of 1.40. The entries on this track that build on entry c66f230d, entries 64c075ac and e7b17fd1 among them, took half of an exact model count, a factor of 2.00; this package
takes five sevenths, as entry 26ebba63 did. If the count is exact, the run has at least 0.6954 expected listed good trials, and by Lemma S8 the bound 0.39 then holds for rho up to 0.576, that is when
a listed good trial has on average up to about 0.58 others in its outer step. For an f between 1 and 104,884,563,382 the same success needs 0.49676 * 2^128 / f walked trials; RUN_STEPS and the pass
budget scale with it, and the search part of Section 11 is below 2^(105.945 - log2 f) units plus the preprocessing: at f = 1, the uniform rate, the package would submit 105.95.

Neither heuristic is proved. Section 13 lists the evidence.

## 11. Charged time

*History label.* The machine, the rows, the allowances and the cap of 56,096 machine units of this section are those of this entry. The run lengths RUN_BATCHES and PASS_BUDGET + 1 in the table and the
totals 320,006,... and 69.3343 below are the whole-class figures of the base text, history; the rows of this entry, with J7 batches and L + 1 passing lanes, and its total are in Section 18.7.

One 2-round target compression costs one unit, and every other primitive word operation, every load and every store included, costs 1/430 of a unit. The rows below are in operations, loads and stores,
called machine units here; 430 of them make one unit of time.

*The machine.* The search is charged on the load/store machine of 6.5, with its 256-bit words, its packed lanes, its masked rotation and its charge of one unit for every operation, load and store,
with two changes: it has 64 registers in place of 16, and every constant is an immediate operand, written in its instruction and not loaded. The cost model of the track charges primitive word
operations and sets no register count; this text charges as well a load for every other word fetched from memory into a register and a store for every word written to memory, spills included. The
batch of seven outer steps runs on packed words (9.6); the rebuild of a passing lane, the joint solver and step 3 run on scalar words of the same machine, one 32-bit value to a word. The pieces of
6.5, which the declared experiments run, and the program's own counts on 16 registers (9.3) are not part of the charge. The schedules of this section are GPT Sol's (answers AL 2, AQ 2 and AR 3 and 6.2
to 6.6), upper bounds written out by blocks, not counts of an executed program; the only counted parts are the 525 units of the batch and the 295 of the rebuild of a passing lane, which a participant
implementation counted with the mask and the filter of the sub-class (9.6).

**The cost, with every term.** Every row is machine units times an upper bound on how often a run executes it; a row with a budget runs at most that many times, because the algorithm halts with
failure when a count passes its budget (9.1). Exponents of counts and products are rounded up.

| Row | How often over a run, at most | Units | log2 of the product |
| --- | --- | ---: | ---: |
| batch of seven outer steps (9.6): the eight random words, step CO on packed words, omega and both automata in every lane (counted, 525), the first table bases, the stored words, the pass bitmap and the dispatch (bound in words, 115) | RUN_BATCHES = 2^66.574 | 640 | 75.896 |
| passing lane: the pass count, the rebuild of its outer step on scalar words and the state of the batch (bound in words, 512), the joint solver of 9.4 and step 3 for every root (bound in words, 56,096) | PASS_BUDGET + 1 = 2^61.937 | 56,608 | 77.725 |
| once: the static rows and descriptors (2^20); the automata of the filter, the three transition arrays, the written-out code of the search, and the row metadata, array bases and initialisation (2^26 each); the resident constants and the last test (40) | once | 269,484,072 | 28.006 |
| **total** | | | **78.083** |

In exact integers the sum of the rows is 640 * RUN_BATCHES + 56,608 * (PASS_BUDGET + 1) + 2^20 + 4 * 2^26 + 40 = 70,263,005,187,913,700,647,040 + 249,743,636,635,253,891,576,992 + 269,484,072 =
320,006,641,823,167,861,708,104 machine units, the numerator of GPT Sol's answer AR 6.6 without the selection procedure, in integer arithmetic.

*Why PASS_BUDGET + 1.* At most PASS_BUDGET passing lanes run steps 2 and 3: the next passing lane advances the count past the budget and halts the run. The row charges the whole 56,608 for
PASS_BUDGET + 1 lanes, which covers these and the lane that halts.

*The batch, 640.* Counted by the participant implementation of 9.6 on the machine above, the same in every batch: the eight random words, one operation and one AND each, 16; the lines of step CO that
reach Y9 or omega, 261; omega, 2; the automaton of (2) in the seven lanes, each with the extraction of its four bytes, the additions of the states, four table loads, the test of its mask and the
branch, 118; the advance of the batch count, its comparison with RUN_BATCHES and the branch, 3; and the automaton of (1) in all seven lanes, the AND with the mask of (2), its test and the branch, 125,
run in every lane whatever the mask of (2). Bound in words (GPT Sol, answer AQ 2): 14 for adding the base address of the first table of each automaton in each lane; 64 for storing R_0 to R_7 and the
counts, masks and cursor of the caller in fixed memory words; 21 for forming the seven-bit pass bitmap and storing it; and 16 for the test of the last batch, whose lanes 2 to 6 are not used, and the
dispatch to the passing lanes. 400 + 125 + 14 + 64 + 21 + 16 = 640. The count was made with the mask and the seven outcomes of the sub-class; with the mask of the class and the automata of the
fourteen outcomes the lines, the four byte lookups per lane and the tests are the same (9.6).

*A passing lane, 512 outside steps 2 and 3* (GPT Sol, answer AQ 2): the eight words taken out of lane i by a shift and an AND, and step CO on scalar words with all the names that steps 2 and 3 read,
295, counted by the participant implementation (9.6); 16 for reloading the eight stored words with their addresses; 32 for storing and reloading the state of the batch around steps 2 and 3, which may
use all 64 registers; and 16 for the pass count, its comparison with the budget, the branch and the dispatch to the next lane: 359, charged 512.

*Steps 2 and 3, 56,096.* A passing outer step is charged by blocks, each an upper bound on its operations, loads and stores, with addresses, branches, spills and the restoration of registers included
(GPT Sol, answers AL 2 and AR 3 and 6.3 to 6.5):

- 4,096 once per passing outer step: E' = omega + DY3 and E XOR E', keeping the names of step CO that steps 2 and 3 read, the choice of the outcomes from the mask, the list of roots and the control.
- 2,304 for each family (9.4): at most 128 blocks of the formulas of (a) to (e) of 9.4, the phase checks, (P*) and their preparation, at 12 units each, 1,536 (the 112 blocks of the formulas of answer
  AI 2 and 16 more; a block is the extraction of one source bit, a majority of four operations, an XOR of at most five inputs, the comparison or choice of a carry prescription, or a carry update, with
  its branch and assignment); the walks of bits 0 to 5 under the two guesses, at most 32 units a bit, 384; and 384 for the record of the family, which at most two rows of a set share (64 to store a
  record of 32 words and 128 to load it twice), the packing of the guard planes and the dispatch.
- 1,152 for each searched row: its 32 descriptors built into 32 registers, at 32 each, 1,024 (seven fields vary with the outer step, Q[i], y[i], E[k], E'[k], kappa[k], kappa[k+1] and the value of a
  constant, at 4 operations each, and 4 for the static base, the shift of the key and the assignment); and 128 for the walks of bit 6 under the two guesses (64), the patches of h[6], h[7], h[13] and
  h[26] (24), kappa and the consistency of bit 6 (8), and the dispatch of the row (32).
- 20 for each forced node: the key from the carry pair, the descriptor and the base of the array, and the read, 3; the validity, its comparison and the branch, 3; the next carry pair and the saved bit
  e2[29] (at position 9 the new bit is put in its place), 3; the chosen bit of h, shifted to its place and ORed into the prefix, 3; the guard of position 25 or 29 written into the key, at most 7 (at
  25, bit 13 of the prefix shifted and masked, XORed with h[6] XOR u, which is held, shifted and ORed into the key, 5; at 29, the saved bit e2[29] masked, shifted and XORed into the key, 3); and the
  continuation, 1.
- 4 more for each selected node, at position 20: bit 8 of the prefix as the desired bit of the key of the selected array.
- 48 for each free node: the parent saved in one register, 2; the key and the read of the dual array, 3; the two arcs taken apart, 2; 11 for each of the two children, for the validity, the carry pair
  and the saved bit, the prefix and the control; the parent restored before the second child, 2; and 5 for dispatch and return: 36, charged 48. No guard reads a free position.
- 80 for each leaf: g, f, e2 and h2 of its h and (J1), (J2) and (J3) as words, a rotation at five operations, 64; and 16 to reload the context words.
- 288 for each root: step 3 of 9.1, that is the inverse of Lemma IP, the cube test, t and its test, E1 on A and on B and the comparison of their differences, 256; and 32 to reload the context words.

For each of the four sets of rows of 9.4, with both versions of every row, steps 2 and 3 cost at most 4,096 + 2,304 F + 1,152 A + 20 N_f + 48 N_r + 4 N_s + (80 + 288) Lf machine units, with A rows, F
families, N_f forced, N_r free and N_s selected nodes and Lf leaves, roots being at most leaves:

| searched rows among | A | F | N_f | N_r | N_s | Lf | steps 2 and 3, at most |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 275 | 2 | 2 | 216 | 22 | 12 | 24 | 25,264 |
| 175, 675 | 4 | 4 | 332 | 32 | 18 | 36 | 39,416 |
| 285, 385 | 4 | 2 | 644 | 68 | 36 | 72 | 56,096 |
| 185, 385, 685 | 6 | 4 | 548 | 54 | 30 | 60 | 55,976 |

So steps 2 and 3 cost at most 56,096 machine units in every passing outer step, whatever its words (GPT Sol, answer AR 6.5; the arithmetic recomputed by the participant). The counts are those of the
static trees, every row of a set is counted in both versions and the blocks are added whether or not they occur together, so this is an upper bound; it is not claimed to be attained or to be the least
such bound.

*Registers of steps 2 and 3* (GPT Sol, answers AL 2 and AR 3 and 6.3). The search of 9.4 is written out statically for each row and each prefix of free choices: a node at a prescribed position has at
most one child, whose code follows that of its parent, and a leaf label jumps to the leaf check; a node at a free position, at most five on a path, saves its parent in one register, the prefix of h
and, above bit 32, the two carries and the bit e2[29], the only earlier output bit that a later guard reads (the guard of position 25 reads bit 13 of the prefix). The registers of the traversal are
the 32 descriptors, five saved parents, six context words, eight constants, array bases and control words, two words of the current state and ten temporaries: 63 of the 64. A leaf or a root keeps the
descriptors and the saved parents and uses the others for its check, after which the context words are reloaded (the 16 and the 32 above). The formulas of a family run before the descriptors are
built, in at most 58 registers: at most 35 bits and carries, five source and context words, eight table, literal and control words and ten temporaries. No register is addressed by a value: every
position and register is named in the code.

*Once.* 2^20 for the fourteen static rows of the outcomes, the static fields of their descriptors at the 32 positions and the metadata of the batches. 2^26 for the two automata of the filter for the
fourteen outcomes, with at most 146 states at each of their 32 bits, built and composed into eight byte tables whose entries hold the base address of the next table (GPT Sol, answers AN 2 and AQ 2).
2^26 for the three transition arrays of 9.4: their 2^18 entries at most 256 operations each, the enumeration of the keys, both candidate arcs, the test for an invalid or a second arc, the selection
and the store included (answer AR 6.2). 2^26 for writing the code of the search: 1,846 static nodes over the fourteen rows, fewer than 2^14 labels, at most 256 operations each with their set-up
(answer AL 2). And 2^26 for the row metadata, the absolute bases of the arrays and their initialisation, a fourth allowance that GPT Sol keeps for safety (answer AR 6.2). 32 for loading the resident
constants and array bases into their registers, and 8 for the test of the final halt.

*One-time items.* The items above are in the last row. The final step, once: steps CT and CS for the trial found, writing the two messages, shorter than 2^42 bytes each, and two complete evaluations
of blake3; each message has at most 2^32 chunks of 16 compressions each and fewer than 2^32 parent compressions, below 2^37.1 compressions for both, and writing them is below 2^38 machine units: below
2^38 units of time in all. Preprocessing: the selection procedure of Section 12, at most 8,882,224,365,081,579,520 machine units, below 2^54.198 units of time, charged in full. (History label: this
term, 116 * 2^56 + 116 * (2^52 + 2^10) + 2^50 operations for the capped selection procedure SEL of the base text, and the total below are those of the base text. This entry runs no selection
procedure; it charges in its place the discovery bound of 18.6, 2^70 word operations, in the ledger of 18.7.)

Total:

    T <= (sum of the rows) / 430 + 2^38 + 8,882,224,365,081,579,520 / 430
      <  2^69.3343.

In exact arithmetic the numerator is 320,006,641,823,167,861,708,104 + 8,882,224,365,081,579,520 = 320,015,524,047,532,943,287,624 machine units, T = 320,015,524,047,532,943,287,624 / 430 + 2^38 =
744,222,149,222,628,937,845.45... units, and log2 T = 69.33429522572521...; in integers, T^10000 < 2^693343. The bound of the base text (history) was time_log2 = 69.3343, the total rounded up at the
fourth decimal. Without the selection procedure, the search part, the rows and the final step, is 2^69.3342551822963... (GPT Sol, answer AR 6.6: 69.33425518229635 without and 69.33429522572521 with
the selection procedure); the selection procedure, charged in full, is below 2^-15.13 times the search part. It is a worst-case bound for the algorithm as stated, which halts within its pass budget on
every run and whose steps 2 and 3 are bounded in every passing outer step; no mean of a count of work enters it, and H1' and H4' enter only the success probability of 10.4. The claim uses this
schedule on 64 registers; no figure on 16 registers is claimed, and the schedule is not claimed to be the cheapest.

*Where the search part goes.* The batches are 21.96 per cent of the sum of the rows, the passing lanes 78.04 per cent and the one-time items less than 10^-13 per cent. Per walked trial, RUN_STEPS *
2^21 of them, the sum is 0.00019856 machine units (2^-12.298); per member of Q* in PASS_BUDGET + 1 passing outer steps it is 0.0270.

*The one formula.* In the form used for the entries of this track, time_log2 = log2(lambda) + 128 - log2(C / m) + log2(ops / 430) + c, with lambda = 0.49676 expected listed good trials, C =
146,838,388,736 the count of 10.1, m = 1.4 the margin and ops = 0.00019856 machine units per walked trial from the sum above, gives 69.3343 for the search. The one-time items, the final step and the
selection procedure are far below the allowance c.

The algorithm has no sorting and no lookup by value: a root is tested against the conditions of its outcome, and a certified trial is not compared with other trials. It reads the two automata of the
filter, eight table entries per lane of a batch at positions given by the bytes of Y9 and omega; in a passing outer step, the stored words of its batch, the three transition arrays at the keys of the
searched rows, the records of the families and the static rows of the outcomes. Its loads are counted: the 56 table loads of a batch are among its 525 counted units, and the loads of a passing lane,
of the joint solver and of step 3 are inside the allowances above.

## 12. Memory, preprocessing and advice

The program of the search is the lines of steps CO, CT and CS, the outer filter, the batch of 9.6, the joint solver of 9.4 with its statically written traversal, and a compression routine for step 3
and the final check: below 2^28 bytes of code and metadata (Section 11). Data, one word of 256 bits each unless said otherwise: the 36,096 entries of the tables of the filter's two automata; the three
transition arrays of 9.4, 2^18 words of 32 bits, 2^20 bytes; fewer than 4,096 words for the joint solver (the descriptors of the positions of a row, the fourteen static descriptors, the records of the
families, the list of at most 72 roots and scratch); and fewer than 1,024 words for the names of step CO, the stored words of a batch, the constants and masks, the counts and the cells of step 3. The
memory of the search is therefore below 2^28 + 2^21 + 2^20 + 2^18 < 2^29 bytes. Nothing grows with the number of trials. The two messages of a found pair have 1024 t + 55 and 1024 t + 63 bytes with t
< 2^32, each shorter than 2^42 bytes; the output, the two messages with their digests, takes less than 2^43 bytes.

**How the advice was found (history; not part of the algorithm or of the claim).** The values that the search reads, listed under advice below and in the record of 18.6, were found by a solver search
and one exact count per model. The participant's solver kissat ran 116 times on instances made by a generator of the participant (51 runs for the lengths 55 and 63, the other 65 for nine other
variants of the instance; bounds 97 to 118; logged seeds). The run for the lengths 55 and 63 with bound 104 and seed 506 found the six constants of 3.2 after 4,770 seconds, with a solution of class
830303cf and beta 18b0e098. An exact integer recount by the participant's counter, on the whole class of each instance, of all 65 distinct instances that the runs returned with a model gave these
constants the part 71,698,432, the largest, 5.47 times the next (13,107,200); every model was replayed on 32-bit words. The cube and the fourteen outcomes of beta* are those of 10.1, and the winner
phase is that of 18.4. Entries e85fffe8 and 78ac164c wrote these runs and counts as a procedure SEL with an operation cap on every run and charged SEL in T; 78ac164c also declared, as a premise, that
SEL returns these values. This entry does neither: the values are a fixed advice record whose used properties this text proves or counts (Lemma ADV, 18.6), and the computation that found them, these
runs and counts included, is charged as preprocessing within the discovery bound of 18.6. The generator, the solver log and the counter as run are not in the package; Section 17 prints the counting
program.

*Memory.* The search with its code holds fewer than 2^29 bytes, the advice 124 bytes and the output fewer than 2^43 bytes; held at once they total below 2^44 bytes: memory_log2_bytes = 44 bounds the
run. The discovery computation of 18.6 is preprocessing; the discovery computation is covered too: every attested device together has less than 2^41 bytes of memory (the local RTX 3090 and its host, the four-GPU server and its host, and at most four cloud sandboxes of at most 256 GiB each), so even counted at once with the search and its output (below 2^43 + 2^29 bytes) the total stays below 2^43 + 2^41 + 2^29 < 2^44 (the participant observed every solver and counting run below 2^34 bytes). The measurements of
Section 13 on real and on scaled-down messages test the heuristics and select nothing. The cost model does not score memory.

(History label: the advice count below, 120 bytes, is that of the base text; this entry stores one more word, the phase of the winner, 124 bytes in all, the record of 18.6.)
nonuniform_advice_log2_bytes = 7 covers what the search reads from storage, the 28 bytes of the six constants and eta, the 12 bytes of beta* and of the mask and value of its cube, and the 60 bytes of
the fourteen values of tau and of eps of the outer filter, 100 bytes; and the 20 bytes that the submitted program also stores for its root instance and its sub-class search, the 8 bytes that name the
two bits of the sub-class and their values and the 12 bytes of the two masks and the word ALL of Lemma A: 120 bytes in all. The tables of the filter's automata, the three transition arrays, the
descriptors and the traversal are not advice: they are computed from these constants. SHARE is the count of passing pairs of Section 8, and the budgets of 9.1 are computed from it and from the other
constants of 9.1. The flags 3 and the counter rule are part of the algorithm. There is no other stored data and no stored collision.

## 13. Evidence, scope and field meanings

Throughout this text costs and bounds are rounded up, and margins, rooms and the whole numbers of the count that the claim uses are rounded down. Counts printed with decimals are rounded to the
nearest.

**What is exact.** Sections 2 to 5, 7 and 8; Lemmas L, H, Q, Q2, T, T2, T4, N, A, TR, CT, IP, F, CB, J0, PL, PB, V and CV and Theorem C; the count of passing pairs of Section 8; the parity certificate
(P*), an exact count, and the constants and caps of the joint solver (9.4) with its schedule (Section 11), as upper bounds; and Lemmas S1 to S9 under their stated hypotheses. Lemma A says what stage A
tests, not that a collision passes it. The declared experiment `half-collision` runs one trial of the root instance (6.1) per organizer seed, with the seven words of a context and a member number
taken from the seed, and the organizer recomputes both digests; Lemma T predicts that every trial agrees on the 128 masked digest bits. The counter instance has no organizer-run check (6.4).

*What is new in the exact part and who has checked it.* Sections 1 to 6 are those of entry 64c075ac without its clusters; Lemmas L, H, Q, T and N and Fact P go back to entry c66f230d. New in entry
e7b17fd1 were Lemma TR, the counter order with Lemma CT and Theorem C, and the counter batch with Lemma CB, written by helper agents of the participant, instances of the same AI model as the author of
this text; and Lemmas IP and S1 to S8, proved by GPT Sol 6.1. New in this package are the outer filter, proposed by a helper agent of the participant; Lemma F and Lemma S9, proved by GPT Sol in its
answer AC, the proof of Lemma F written out in Section 8 by a helper agent of the participant from the assignments of E3; the count of passing pairs with its certificate, derived by GPT Sol in the
same answer; and the joint solver of 9.4, its constants and caps proved by GPT Sol in its answers AE and AF, with Lemma V of the participant and Lemma CV (10.2); and, for the class of this package,
the fourteen-outcome filter with its share (GPT Sol, answer AN 2), the phase guards and the single traversal of the solver (answer AO 6), the parity certificate (P*), Lemma J0, the transition arrays,
the families and the cap of 56,096 (answer AR), and the independent lanes of the batch with Lemmas PL and PB (answer AQ). The participant's checks of the new exact part are computations, not proofs:
the counter construction against the organizer's own functions on 2,000 trials, with 204,000 internal words compared with a separately written forward computation, and complete messages hashed by the
organizer's code (Section 7); every lane of the counter batch against the program's own compression of the real last chunks (9.3); all 2^21 members of Q*, each giving the difference beta*; the rule t
!= 0 (Section 8); the program's automata against brute force at 10 bits (9.3); a participant implementation of the joint solver against an earlier solver on real walks and on planted instances (9.5);
the free positions, static trees, families and caps of the solver, and the sums of the cells of (P*) against the counts of 10.1, with a separate count of (P*) in one phase of 2^16 members (9.4); a
participant implementation of the batch, with the mask and the filter of the sub-class, against the program's own functions (9.6); and the two pattern histograms of the program's own tables against
the certificate, equal in all 36 nonzero masks and both zero counts, with the same count of passing pairs and the same seven per-outcome counts (Section 8). For Sections 1 to 6, three independent
reruns, by a checking agent, a reviewing agent and a participant tool that reads the printed text, found no wrong value in the displays, Table C and Lemmas Q, Q2, L, A, T2 and T4, and Lemma A was
checked by complete enumeration in three ways: the submitted program on all 2^16 patterns of the 13 bits of z and the 3 bits of e1 that the rule reads (65,536 packed words); a second statement of rule
and test typed by hand on 4,194,304 inputs; and seven wrong plans of the test, all of which the program refuses. These are checks, not proofs, and no person has read any part of this text.

**The seven-word model.** By 6.2 the residual of a trial, of the root instance or of the counter instance, is a function of the constants and of seven 32-bit words: for E1 its first-half values d1 and
b1 and its a output a2 on message A, and for E3 the words Y4, Y9, w8 and its first-half value h1 on A. The model M says that over the trials the six words other than Y4 behave like independent uniform
words, independent of Y4, which is uniform in the sub-class. Under M a trial has R = 0 with probability r * 2^-128, where r * 2^81 is the number of solutions of R = 0 among the 2^209 values of the
seven words with Y4 in the sub-class. Call r the *rate of the sub-class*. Rule A is a condition on h1, so under M the trials with R = 0 that satisfy rule A have a rate of the same kind, r_A, counting
only the solutions that satisfy rule A; r_A is at most r. The counter search prescribes c1 = Y11 + d1 in Q*, and under M that is a conditioning on d1 (Lemma S1); its rate p is formed from the part of
beta* in r (10.1). On the outer steps that pass the filter of Section 8 the rate under M is p / pi, and no part of p lies on the others (Lemma S9). M and the count give the rate of a single trial.
They do not give the probability that a run has a good trial, which also depends on how the good trials of a run cluster; a model of the single trial says nothing about that.

Given M, the rates are properties of the constants, the sub-class and beta* alone and can be counted without sampling; the count says nothing about whether M holds. The six words are not free in a
trial. In the counter search Y4, Y9 and w8 are fixed for the 2^21 trials of an outer step, and so are Y12 and w5, which E1 reads; the trials of an outer step differ in d1 and in what follows from it
(Lemma CT (c)), and E1.b1, E1.a2 and E3.h1 move with d1. M is a statement about averages over the outer steps of a run. Lemmas S2 to S4 show which parts of it hold exactly for the construction, and
H1' declares the rest. The measurements below show where M fails inside one context and inside one outer step.

**How r is counted (participant computation, not organizer-verified).** Write tau, eps, beta for the XOR differences between A and B of E1's a output, c output and first-half b, and eta, psi, tau',
eps' for those of E3's first-half d and b and its c and a outputs. Because E1's a1 and d1 are the same for A and B, R = 0 holds exactly when tau' = tau, eps' = eps, psi = tau XOR ROR(tau, 1) and eta =
eps XOR ROL(beta XOR eps, 1); for Y4 in the class the left side of the last equation is the constant 830303cf. The counter works in integers (128-bit unsigned integers; exact fractions for the
products and sums), has no sampling branch, and needed no fallback on any outcome of the count below; no floating-point number is on the path of a figure printed below as a fraction.

1. *The betas.* beta is a function of d1 alone: with c1 = Y11 + d1 and DY11 = Y11' - Y11 = 0a08818b, beta = ROR(c1 XOR (c1 + DY11), 12). As in Lemma Q, the d1 with a given beta are a share 2^-k of all
   d1, k being the number of bits of the mask ROL(beta,12) AND 7fffffff.
2. *The outcomes of one beta.* An outcome is a pair (tau, eps); the admissible tau are enumerated with a carry automaton, with no bound on the weight of tau. A beta for which beta XOR ROR(eta, 1) has
   odd weight contributes nothing; every other has two candidates for eps.
3. *The E3 side.* N3 is the number of quadruples (Y4, h1, Y9, w8) for which E3 produces eta, psi, eps and tau; all of them have Y4 in the class.
4. *The E1 side.* P1 is the probability that E1 produces tau and eps when d1 is uniform among the values with this beta and b1 and a2 are uniform.
5. *The sum.* For the sub-class, N3 counts only the quadruples with Y4 in the sub-class, and the part of a beta in r is 2^(15 - k) times the sum over its outcomes of P1 * N3, where 15 is the number of
   bits that Lemma Q2 fixes, so that the sub-class is a share 2^-15 of all Y4: the sum of N3 over all 2^96 values of (d1, b1, a2) is r * 2^81, and 2^96 / 2^81 = 2^15. r is the sum of the parts over
   all betas. Parts are not negative, so the sum over any set of betas is a lower bound for r. For r_A, N3 counts only the quadruples whose h1 satisfies rule A.

**The count for this package (participant computation).** The count runs over the 60 words beta that have a part in the rate of the whole class, the list of entry c66f230d: of the 133,742 words that
occur as beta, the 4,550 with k at most 14 were enumerated, and for the 129,192 others a SAT solver was asked whether the whole system has a solution with that beta and answered no for 129,147,
without certificates. The integer enumeration of GPT Sol 6.1 over every beta finds the same 60. A beta without a part in the class has none in the sub-class; the other betas were not searched again
here.

For the whole class the rate is 85074516985129/524288 = 162,266,763.66, from 60 betas and 453 outcomes with a nonzero product. For the sub-class it is

    r = 194382080300609/1048576 = 185,377,197.55,

from 53 betas and 317 outcomes, about 2^27.47, so that under M a trial has R = 0 with probability about 2^-100.53. The rate of the sub-class is 1.142 times the rate of the class: under M the members
do not have the same rate, and the quarter of the class in which bits 21 and 26 of e1 are zero has more than its share.

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

"With rule A" is the part of the beta in r_A. "Kept for H1", the figure that entry 64c075ac used, adds only the outcomes in which every solution satisfies rule A. The heaviest beta carries 36.5% of
the count and the four heaviest 98.8%. The count rests on few paths.

*Rule A in the count.* Of the 317 outcomes, 99 have only solutions that satisfy rule A, 76 have none that does, and 142 have both. The exact rate with rule A is

    r_A = 6219586146887739/33554432 = 185,358,111.47,

so the rule loses 19,086.08 of r, about one part in 10,000, and the sum over the 99 outcomes is 12147454997539/65536 = 185,355,453.45, the figure that entry 64c075ac set its H1 against. For beta*, the
only part that the claim of this package uses, the three figures coincide (10.1). On the whole class the same eight conditions keep 76,072,772.68, less than half, and no outcome there is free of
violating solutions: the rule belongs to this sub-class.

The submitted program also holds the rules of four and six conditions that rule A contains; it uses only rule A.

**Where the sub-class and the rule come from, and the second count.** Both were proposed by another AI model, GPT Sol 6.1 (OpenAI), run by the participant with briefs that asked for exact counting.
With a counter of its own it computed the rate of sub-cubes of the class and searched for affine conditions on h1 that keep the count; its answers give this sub-class, r = 194382080300609/1048576, and
the eight conditions, r_A = 6219586146887739/33554432. It calls its sets "best found": its search over conditions is not exhaustive. A second instance of the same model, given the decimal figures,
reports the same two fractions and calls the sub-class the only best of the sub-cubes with 15 fixed bits of e1, and the eight conditions, in another basis of the same affine set, a certified best
among all sets of eight affine conditions on h1. The participant has not checked these two statements, and nothing the participant has checked shows that no better sub-class or rule exists. The
participant's counter, extended by the sub-class, agrees with the other model's files on 21 exact fractions (totals and rule masses for this sub-class, for a second sub-class of 32,768 members and for
the whole class), on the rate of every beta and on 3,243 integers over 1,081 outcomes, with no difference; this was a recount with those figures at hand, not a blind one. The other model does not
give, and the participant alone has, the figure "kept for H1", the split by beta, and the rules with four and six conditions inside the sub-class.

**Checks of the counter (participant computations).** (1) Complete enumeration with 8-bit words of every quadruple (Y4, h1, Y9, w8) through both executions of E3 and every triple of the E1 side, over
random constants, classes, sub-classes with up to three more fixed bits of e1 and rules with parities of three bits: five runs, 1,472,040 and 5,332,992 integers, none different from the counter.
(2) At 32 bits two functions compute the E3 side with its split by the rule and agree on all 687 outcomes both counted; the other 285 (16 with a nonzero product) were counted by one alone. The E1
count agrees with the earlier calculator on 972 of 972 outcomes. (3) The untouched calculator of entry c66f230d, with an option of its own for a sub-class, finished 54 of the 60 betas in the time
allowed, each equal to the part printed above at its one printed decimal; the six unfinished carry together 0.3346 of the 185,377,197.55 of r, a share of 1.8 * 10^-9. (4) For the whole class, a helper
agent that audited entry c66f230d counted both factors of all 453 outcomes with two programs written from the definitions of 6.2 and 6.3 alone: the same total, 85074516985129/524288, and the same
parts for 60 of 60 betas. The checks that entry c66f230d reports for the whole class (an approximate model counter on the sixteen largest outcomes, brute force with 8-bit words, a sampler for the four
heaviest betas) were not repeated for the sub-class.

**How the constants and the class were found.** As in entry c66f230d: the six constants come from a SAT solver search for a pinned call with the property of Fact P and a zero residual, with the two
words w4 related as the length cancellation prescribes and a zero top byte of word 13; the class is the class of the solver's solution, and the constants were chosen among the solver's sets by the
count. The constants and the class were chosen to make the count large, and the sub-class and the rule by the count as well. Beta* is the beta of the solver's solution for these constants (Section 12)
and the first of the 53 values of beta with a part in the sub-class by the conditional rate of 10.1.

**Real messages in the root arrangement: what exists.** All of the following are participant measurements, made for entry 64c075ac in the arrangement of Sections 4 to 6 (counter 0, flags 11). They
bear on the seven-word model M, on which the counter rate rests as well, and on rule A; they are not measurements of the counter search or of its budgets.

*The self-test and the equivalence runs (processor).* Every lane of the self-tests of 6.5 is compared with the complete digests of its two real messages: 7,000,000 lanes in the long run. On 200,000
batches the program makes the same decisions (members, table words, flags and branches of both stages) as a first form of the two-level program that fetches every word where it reads it, keeps nothing
in registers and tests the rule as written on h1. One complete outer step was run: all 18,725 table words equal the words of their members, and with that one table all 18,725 batches of one value of
X2 (131,075 lanes) and 3,000 batches of each of three more values of X2 are right against the complete digests.

*Rule A and the entry to stage 2 in the sub-class (processor).* Three runs of 2^30 real trials each, in the member order of the program, with h1 taken from the trial and anchored against the complete
compression of message A on 65,536 trials per run: 8,192 independent contexts; 512 outer steps with 16 values of X2 each; and 8,192 contexts from a second seed. The first two were drawn from the same
seed text, so the 512 contexts of the first value of X2 of each outer step of the second are also contexts of the first. Rule A is satisfied by 2^-8.0019, 2^-7.9992 and 2^-8.0000 of the trials. The
share of the batches that run stage 2 is 0.02617, 0.02622 and 0.02622; independent trials would give 0.0270, and the root batch's budget was 0.03125. Single contexts have between 0.0071 and 0.0421,
the 512 outer steps between 0.0238 and 0.0289, and the one value of X2 run in full above has 574 of 18,725, a share of 0.0307. In the review of the text of entry 64c075ac three helper agents measured
the same share again, each once and with a program of its own, in contexts in the ranges of the root search of that entry: 0.026171 in 8,192 contexts, 2^30 trials from four seeds (0.02609 to 0.02626
per seed, 5 contexts above the budget, h1 anchored on 16,384 trials, all equal); 0.02619 on 2^22 trials; and 0.02620 in 640 contexts, 4 of them above the budget. The first was run again for that text
with the same output. Until the graphics-card and scaled-down runs below, these were the only measurements that have the sub-class and the rule of this package.

*Layout runs of the two-level arrangement (graphics card).* Real messages enumerated as the root search of entry 64c075ac enumerates them (six outer words fixed for a run, consecutive values of X2,
every member in list order, batches of seven consecutive members), but for the whole class of 524,288 members and with the rules of four, five and six conditions of entry c66f230d: 24 outer tuples of
2^40 trials, two deeper runs of 2^44, eight runs with X2 spread over its range, 4,096 random outer tuples and 4,096 consecutive values of w5. A second helper agent recounted the raw outputs with its
own parser (451 comparisons, 449 equal, two differing in the last printed digit), rebuilt the program, repeated one run, and checked on the processor that the layout is the algorithm's. Averaged over
outer tuples the counts agree with the model within their statistical error; for the deepest event that error is large, 138 of 152.0 being a ratio of 0.91 with one-sided 95% limits 0.785 and 1.046.

| Event | Probability per trial | Average against the model |
| --- | --- | --- |
| rule with 4, 5, 6 conditions | 2^-4 to 2^-6 | within one part in a million |
| listed beta | 2^-7.96 | +0.73 standard deviations |
| listed beta and tau | 2^-18.88 | +0.83 standard deviations |
| listed partial E3 event | 2^-32.2 | -0.24 standard deviations |
| listed E1 outcome | 2^-40.15 | 138 of 152.0 expected (-1.14) |

What they do not support, and what this text must not claim: independence of the trials inside one outer step. The share of the trials of one value of X2 that satisfy a rule is not binomial (for five
conditions its variance is 2.7 to 181 times the binomial one), and the members of a batch pass together. For E1 the rate of a listed tau given a listed beta is a property of the outer tuple: for 17
cells carrying 24% of the count it lies between 0.02 and 2 times its average, it is the same for 4,096 consecutive values of w5, and the cause is known (Y12 and w5 are fixed inside an outer step). A
weighted estimate of the rate of solutions of one outer tuple, relative to the average, has a standard deviation of about 0.7% between tuples; it has mean 1 by construction and stops at the level of
beta and tau. One count is unexplained: in one window of 2^44 trials of one tuple, 3 listed E1 outcomes were seen where 14.65 are expected (probability 0.0003 under a Poisson law); the next window of
the same tuple has 16, and the cells one level up do not differ. Chance is the likelier reading and it is not excluded that it is not chance. The E1 test passes at 2^-31.41 per trial (2^-31.20 in the
tuple with the most). The outer words here are random words: no run has C0.d1 in the short range of the root search, and none holds a whole outer step, the longest having 2^26 values of X2 of one
tuple.

*Scaled-down end-to-end runs in the two-level order.* The whole search of this pair of lengths was run on small versions of the hash, with 8-bit and 10-bit words and 2-bit bytes, messages of 7W - 1
and 7W + 7 such bytes, random constant sets and for each its best class of 4 to 64 members. A run is four random seed words and a number of outer steps, each with all 2^W values of X2 and all members;
both byte strings of every trial are hashed completely and all eight digest words compared, with no rule and no filter. The prediction for a run is the number of solutions of the seven-word system for
that set, by complete enumeration, times the number of outer steps over 2^(5W). All runs made in this folder, each counted once: 436 runs, 470 collisions found against 467.6 predicted (+0.11 standard
deviations); with 8-bit words 463 against 455.9 in 415 runs, with 10-bit words 7 against 11.7 in 21 runs. Every collision was confirmed from its two byte strings. The history must be said with the
sum: the first job of 92 runs was low (56 against 74.8, -2.17 standard deviations); two more jobs were then made, each written down before it was run, and they were not low (307 against 284.0 in 280
runs, and 104 against 102.0 in 60 runs for the one constant set that had stood out); the other four runs are the self-check of the scripts (3 against 6.8). One series of that set, 2 collisions against
13.0 in 26 runs, was taken as chance. The larger job of the same kind, whose expected values and rule of judgement were written down before it was run, ran on another machine after the text of entry
64c075ac was first assembled. It has 8,448 runs (the 92 of the first job among them): 8,108 collisions against 8,313.6 predicted (-2.25 standard deviations); with 8-bit words 6,276 against 6,489.6 in
6,528 runs, 3.3 per cent low (-2.65); with 10-bit words 1,832 against 1,824.0 in 1,920 runs (+0.19). By that rule a deviation between 2 and 3 standard deviations is written down and only one of more
than 3 below the prediction would speak against the model; the series of the set that had stood out has 38 against 40.0 there. No run has a failed check or a false collision. The cause of the
shortfall at 8 bits is not known; a dependence of the rate of one outer step on its fixed words, which is stronger at small word sizes, is one possible reading and is not established. These runs test
the model for whole collisions in this loop order at small word sizes. They have no sub-class, no rule A and no packed batch.

*Scaled-down end-to-end runs in the order of entry c66f230d.* The same test with the trials enumerated as that entry enumerates them: in the plan fixed before the runs, 1,272 runs, 345 collisions
against 335.76 predicted (+0.50 standard deviations); a second helper agent rebuilt and rehashed every collision with code of its own and recounted two whole runs and the prediction of four constant
sets. In a second plan, made after the first had been read, one row has 2 runs without a collision where 0.25 are expected (probability 0.024); 24 further runs made to look at this have 93 collisions
against 93.97 and one empty run against 0.49. That entry said it had no scaled-down run for this pair of lengths; these are the runs, made after it was filed.

*Real messages in the order of entry c66f230d (graphics cards of another machine).* After the text of entry 64c075ac was first assembled, 24 runs of 2^45 real trials each, 2^49.58 in all, were made
with the six constants of this package for the whole class, in the layout of that entry, and counted against the exact expectations of the model: listed beta 3,401,612,690,888 against
3,401,614,098,432 (-0.76 standard deviations), listed beta and tau 1,750,004,875 against 1,750,007,808 (-0.07), listed E1 outcomes 692 against 690.78 (+0.05) and partial E3 events 171,097 against
171,316.3 (-0.53); every run lies within 2.2 standard deviations on every count and no run has a failed check. Like the layout runs, these support the model on average and at about 2^-40, for the
whole class and not for the sub-class or rule A.

*Real messages for the sub-class with rule A (graphics card).* After the text of entry 64c075ac was first assembled, the sub-class and rule A were run on real messages on a graphics card: 24 outer
tuples, 2^23 values of X2 each with all 131,072 members, 2^44.59 trials in all, bad 0 and contradictions 0. The added rule agrees with rule A of the submitted program on 2^21 random words of h1, with
0 disagreements. Rule A passes at 2^-8.000002 of the trials (103,079,088,429 passes), the same statement as the processor runs at 8,192 times the trials; and 0.026178 of the packed words of seven
consecutive members enter stage 2, against 0.027025 if the seven members were independent and 0.03125 charged there, so the measured entry was 0.838 of that charge. The deepest events with an exact
probability that the run reaches are the listed partial E3 event at 2^-32.2 (6,314 seen against 5,353.63 on the whole-class value) and the listed E1 outcome at 2^-40.15 (14 seen against 21.59, a
shortfall this run does not resolve). On the same pin and geometry the listed partial E3 event comes at 1.18 times its whole-class rate (8.9 standard deviations of the run scatter apart), in the
sub-class's favour; in an independent-context model run restricted to the sub-class the same marker is 1.148 plus or minus 0.051 times its whole-class value, and with real messages on the same members
0.998 of that. This is the first real-message figure of any kind that says the sub-class is richer than the class, and it points the way the count does. It is NOT the counted gain: the marker is one
call deep at 2^-32 while the gain 1.142 is in the counted rate r at 2^-100.53, which no measurement can reach; and rule A is a necessary condition for a collision and so is positively correlated with
the marker (268 of the 6,314 partial E3 events pass rule A, a factor of 10.9 over the rule's own rate), which is what this package's own argument predicts and is not evidence that the rule keeps the
counted mass. The kept mass of rule A, 185,358,111.47 of 185,377,197.55, is not measured by it.

*A scaled-down end-to-end run with the sub-class and an eight-condition rule.* The whole search was run on an eight-bit version of the hash with both pieces that entry 64c075ac added to the path of
entry c66f230d: a sub-cube that keeps a quarter of the members (two more fixed bits of e1, the step by which this sub-class fixes two more bits than the class) and an eight-condition parity rule on
the eight-bit word h1 (pass rate 2^-8), on two constant sets, with every trial that passes the rule built as two real messages of 55 and 63 toy bytes and hashed in full. In 30 runs, 515,396,075,520
trials examined and 2,013,236,457 of them passing the rule and hashed: 121 collisions against 120.23 predicted from the exact table over exactly the trials tried (standard deviation 10.96, z +0.07),
with bad 0, bogus 0 and lost 0, and the first stage on its own 2,013,236,457 passes against 2,013,265,920 expected (z -0.66). The plan and the reading rule were written and hash-stamped before the
first six of the thirty counted runs; the other twenty-four were declared after that first result (29 collisions against 24.05) had been read, and are reported apart from it. This establishes, with
real collisions, that selecting trials by a sub-cube condition on e1 and by an eight-condition rule on h1 leaves the collision rate of the survivors at the exact per-trial count, to within 9 per cent.
It does NOT establish the kept mass of rule A: at eight-bit words no eight-condition rule keeps almost all of the collision mass (the scaled rule keeps 7 to 9 per cent, where the real rule keeps 99.99
per cent by the count), so that part of the rate stays a counting claim, untested here.

*Chosen and random outer words for the sub-class (graphics card).* The sub-class was also run with the fixed outer words set three ways: an arm whose outer words are chosen so that the model predicts
more listed E1 outcomes (good), one chosen for fewer (bad), and one with random outer words. The model predicts how single outer steps differ: the good arm has 421 listed E1 outcomes against the
model's 421.2 and an average over outer steps of 345.7, the bad arm 235 against the model's 226.1 and an average of 288.1, and the random arm 275 against an average of 288.1; the good and bad arms
differ by 5.04 standard deviations, as the model says single outer steps should. The disclosure it carries: single outer steps of the sub-class differ from the average over outer steps by about plus
or minus 8.48 per cent in the model's weighted rate (the chosen arms measured 1.0980 and 0.9115 times the random arm; earlier runs of the same two settings in another folder gave 1.087 and 0.914), and
random outer steps by about 3.7 to 4.0 per cent from one step to the next, while the claim uses the average over outer steps. It is a measurement at a 2^-40 marker for the whole-class count; it
reaches no collision and does not measure the factor.

**Real messages in the counter arrangement.** This and the next paragraph report participant measurements of the counter arrangement; the organizer's harness does not run them, and they are untrusted
evidence for it. On a graphics card a helper agent ran the counter construction on real 32-bit messages, with random outer words and 2^12 consecutive members of Q* per outer step: 2^45 trials with Y4
in the sub-class and 2^44 with Y4 in the whole class, and the same counters on the seven-word model with c1 in Q* (2^44 and 2^43 model trials); on a processor, four runs of 2^20 outer steps with 2^16
members each. Every real trial had the difference beta* (2^45 of 2^45). Against the exact figures of the model:

| Event | Model, exact | Real counter trials |
| --- | --- | --- |
| tau listed for beta* | 2^-10.696 per trial | 2^-10.696 per trial |
| listed E1 outcome (beta*, tau, eps), sub-class | 10,176.0 | 10,129, that is 2^-31.694 per trial |
| listed E1 outcome, both classes together | 15,264 | 15,139 (-0.8% +- 0.8%) |
| rule A | 2^-8 | 2^-8.000 |
| listed E1 outcome and rule A, both classes | 59.6 | 55 |
| listed partial E3 event, whole class | 3,569 | 3,626 |
| E1 test of Lemma N passed (n = 0) | | 2^-26.02 per trial |

The ratios of the real to the model runs, in the sub-class with Poisson errors: listed E1 outcome 1.009 +- 0.017; listed tau 1.0001; rule A 1.0000; E1 test 0.9998 +- 0.0024; listed tau and rule A
0.9999 +- 0.0002; listed E1 outcome and rule A 0.90 +- 0.25; listed partial E3 event 1.057 +- 0.020, where the true error is larger because these events cluster by outer step (whole class 0.971 +-
0.028); each of the four residual words zero 1.019, 1.009, 0.984 and 0.990, each +- 0.006 to 0.021. In the arrangement of entry 64c075ac the same events of beta* are rarer by the factor of the
prescription: c1 lies in Q* with probability 2^-11 there, and the listed E1 outcome of beta* has 2^-42.69 per trial, against 1 and 2^-31.69 here. So the E1 side of a counter trial carries the factor
2^11 that the count predicts, and the E3 side is unchanged. On the processor the number of trials of one outer step that satisfy rule A has a variance 572 times its mean, and that of the listed tau
247 times: single outer steps differ strongly, and only averages over outer steps agree with M. No event here is deeper than about 2^-40, the listed E1 outcome with rule A; none is the joint event of
H1', at about 2^-91.

**A scaled-down end-to-end run of the counter arrangement.** The whole counter search was run on an eight-bit version of the hash: 2-round BLAKE3 with 8-bit words, 2-bit toy bytes, 64-byte blocks and
1,024-byte chunks, with eight sets of toy constants fixed before any counted run and the class of each. The messages are F || A and F || B of 1024 t + 55 and 1024 t + 63 toy bytes with t = 1 to 255, F
being t chunks of zero bytes; the last chunk is compressed with counter t and flags 3, and t = 0 is dropped (79.3 million of 20.3 billion trials, one in 256, as expected). The inner word d1 runs over
the values of the heaviest beta of each set, the toy form of c1 in Q*. Both last-chunk compressions of every trial were evaluated in full and all eight words compared, with no rule and no filter;
every collision was rebuilt as two complete messages and confirmed by two independent toy tree hashes, one of them written after the organizer's code. The predictions are exact model counts for each
set. Over the eight sets:

| Arrangement | Collisions found | Predicted | Trials per collision |
| --- | ---: | ---: | ---: |
| root instance (counter 0, flags 11) | 67 | 64.0 | 8.8 * 10^8 |
| counter, d1 in the set of the heaviest beta | 251 | 255.0 | 8.1 * 10^7 |
| counter, d1 not restricted (control) | 54 | 47.8 | 8.2 * 10^8 |

All 372 collisions are collisions of complete messages, and no trial failed a check. The realised fraction of the predicted gain of the prescription is (251 / 255.0) / (67 / 64.0) = 0.94 +- 0.13, that
is -0.09 +- 0.20 bit: no loss is detected. The control shows that the counter alone, without the prescription, changes nothing. This tests the mechanism with real collisions. It does not test the size
of the factor at 32 bits, which the toy cannot reach (its factors are 3.9 to 31.8 on the eight sets, against 747.92 here), and it has no rule A, no sub-class and no packed batch.

**Real messages in passing outer steps.** A participant measurement made for this package, untrusted evidence like the two paragraphs before it, which the organizer's harness does not run. On a
graphics card a helper agent ran the counter construction on real 32-bit messages with Y4 in the sub-class. Uniform random outer steps, drawn by the measuring program, were filtered by conditions
(1) and (2) with tables generated as the submitted program generates them, and every passing outer step enumerated the whole of Q*, all 2^21 values of c1 in the program's member order, as 299,594
words of seven lanes in the layout of the run-wide table: 2^22.00 passing outer steps, 2^43.00 trials. A control with the filter off ran 2^18 outer steps, 2^39 trials. On 330 records a check against
the submitted program (step CO, the filter, the member order, rule A and the word n of the E1 test from the program's compression of the real last chunks) found no difference. Errors are taken per
outer step, because the trials of one outer step cluster.

| Event | Over all outer steps | In passing outer steps | Ratio |
| --- | --- | --- | --- |
| outer step passes the filter | 2^-9.8132 (pi, exact) | 2^-9.8127 | z = +0.7 |
| rule A, per lane | 2^-8 | 2^-8.000 | 1.0003 +- 0.0006 |
| E1 test of Lemma N passed, per trial | 2^-26.02 | 2^-26.023 | 0.9945 +- 0.0031 |
| listed E1 outcome, per trial | 2^-31.694 | 2^-31.724 | 0.979 +- 0.022 |
| listed partial E3 event, per trial | about 2^-32.4 (control, 98 events) | 2^-24.17 | about 2^8 |

So inside passing outer steps rule A and the E1 test keep their values over all outer steps, and the listed E1 outcome keeps its value within its error. Per outer step the count of trials that satisfy
rule A has standard deviation 9,785 against a mean of 8,195: the trials that satisfy it cluster. Over the 12 patterns of the filter's masks with at least 40,000 passing outer steps each, rule A lies
between 2^-8.006 and 2^-7.996 and the E1 test between 2^-26.08 and 2^-26.00. The partial E3 event, a condition on E3 like (1) and (2), is concentrated by the filter, as expected. Trials with t = 0
were not dropped, at most one per outer step. These measurements bear on H4' and on the rate of H1' inside passing outer steps; they reach no event deeper than about 2^-31.7 and no collision.

**What does not exist.**

- No organizer-run check of the counter instance: an experiment of the harness tests events of complete digests, and the half-collision of the counter instance lies in the chaining value of a chunk
  that is not the root (6.4, Section 7). Its checks are participant computations with the organizer's functions imported (Section 7) and the program's self-test (9.3).
- No measurement of the joint event of H1', at about 2^-91 per trial. The deepest counter events measured are the listed E1 outcome at 2^-31.7 and that outcome together with rule A, 55 events at about
  2^-39.8.
- No proof that the construction's trials have the joint law of the model words, of the share of the success mass that the rule t != 0 removes, or of a bound on rho for the construction's own outer
  steps. These are the open parts that H1' declares (10.3).
- No proof that the share pi_o of the sampler's outer steps that pass the filter equals pi; it is measured (H4'). No measurement in passing outer steps deeper than the listed E1 outcome at about
  2^-31.7 per trial.
- No scaled-down run of the counter search with the outer filter or the joint solver; the toy run has neither.
- No complete message of a found pair; the complete messages hashed (Section 7) are trials, with t from 1 to 16,383.
- The count 71,698,432 of the class and its fourteen outcomes are reproduced by Section 17. No list of values of beta is stored or ranked (18.6).
- The search of 9.1 exists only in this text: its member in the class, its fourteen-outcome filter, its constants, its batch of seven outer steps, the bound on the number of batches, the joint solver
  in the layout of 9.4 and step 3. No implementation of the joint solver for the class has been run (9.5), and the batch was run only with the mask and the filter of the sub-class (9.6). The program,
  that of entry 26ebba63 and the earlier version of this search, has the walk over outer steps with the seven-outcome filter and the pass budget of the sub-class search, and it counts that outer step
  and that filter; every row of Section 11 is bounded in words, apart from the counted 525 and 295 of 9.6.

**Limits of the evidence.**

- H1' is an assumption. The factor is set against a count under M with c1 conditioned in Q*; the count does not show that M holds, and Lemma S1 is a statement inside M. Lemmas S2 to S4 prove parts of
  the transfer to the construction, not the joint law of the seven words, and nothing proves the dependence part of H1'.
- M fails inside one context and one outer step: in the root arrangement for rule A and for the call E1, and in the counter arrangement for rule A, whose count per outer step has a variance 572 times
  its mean. Where it was measured it holds on averages over outer steps. The counter search fixes Y4, Y9, w8, Y12 and w5 for the 2^21 trials of an outer step, so the success of a run rests on many
  independent outer steps, 2^69.381 walked and about 2^61.85 of them passing in the whole-class run of the base text (2^75.468 and 2^68.024 in the winner run of this entry, Section 18.3), and on the
  premise that one outer step rarely holds more than one listed good trial.
- The share of the sampler's outer steps that pass the filter is measured, not proved equal to pi: 2^-9.8127 against 2^-9.8132 on 2^22 passing outer steps. Lemma F needs no law of the words, and the
  time bound needs none either, since the pass budget halts the run.
- The model is checked on real messages to about 2^-40, not at 2^-91. Scaled-down whole-collision runs are level for the counter arrangement (0.94 +- 0.13 of the predicted gain) and, for the root
  arrangement, level at 10 bits and 3.3 per cent low at 8 bits in the largest job.
- The constants and the class were chosen by the count, and beta* with them, so they favour any choice that the model overrates. The part of beta* is 44.2 per cent of the count of the class and rests
  on fourteen outcomes with one value of eps. Most measurements of this section are on the sub-class and its seven outcomes; the seven outcomes added on the class carry 5.6 per cent of the count and
  are not measured separately.
- The count rests on programs that are not in the package and on a list of values of beta that is complete only by uncertified solver answers and the other model's enumeration; the other model
  reconciled the records and did not recount them.
- H4' concerns a run total; single outer steps differ strongly. A reached pass budget halts with failure, which lowers the success probability and not the time bound.
- Every row of Section 11 is bounded in words by GPT Sol's schedules on 64 registers, built on the program's counts of the outer step of the sub-class (9.3) and a participant recount of it; no row is
  a count of an executed program.
- The messages of a found pair have about 2^41 bytes on average and fewer than 2^42; computing their digests costs about 2^37 compressions, which is charged, and no check of this package computes
  them.
- Helper agents of the participant wrote and checked the counter construction, the filter and this text, and another AI model proved Lemmas IP, F and S1 to S9 and derived the count of passing pairs;
  no person has read it.

**Approaches tried that did not improve this path.** Each is a negative result for this family, not a general one.

- Inside-out solving of the residual with redundancy: complete known sets start at redundancy two on one side (222,513, none with a split equation), are absent at two on another (three not completed)
  and up to four for all seven words; at 2^32 per unit this needs redundancy one. Proposed by the participant.
- A SAT solver per trial forcing further conditions: 0.6 to 6.0 seconds at levels 0 to 2, no answer in 900 seconds at levels 3 and 4, against about seven operations per trial. Proposed by the
  participant; run by a helper agent.
- Forcing a second condition via a coupled block of equations: thirty of thirty cases unsatisfiable; smallest forcing blocks 35, 20 and 49 equations (one test word, the other, both); the heaviest cube
  costs at least 18,900 operations per forced trial against break-even 11,673, at least 0.7 bit lost. Helper agents.
- Bit-level steering and neutral bits for the first-stage test: no neutral bit or zero-loss single-bit skip exists; a free-bit flip changes the five-condition rule of entry c66f230d with probability
  0.035 to 0.063 and leaves rule A unchanged in at most 2 times 2^-8 of cases; no deeper word steers cheaply. Proposed by the participant; helper agents.
- Table lookups prescribing a second word, and loops of over two levels: per-trial equations stay at the two-level numbers (11, 25 and 26 to the first test word, the second and both; 6, 18 and 19 for
  entry c66f230d). Helper agents.
- Other absolute values of the pinned constants: the best of 4,432 realizations beats the count in use, 162,266,764, by 177.69, about one part in a million. From an observation of GPT Sol 6.1; helper
  agents.
- The four-active fork: best complete trail 253 against 100, unsatisfiability proved only up to 70 to 77, so evidence, not proof, that it is worse; revisiting needs a proof above 100 or a trail below
  it. Helper agents; GPT Sol 6.1 and Grok 4.7 expected it to be weak.
- Better pinned constants in the same length family: two and a half hours of server search found none at bounds 100 to 103 and two at 104, with class rates 107,785 and 30,487 against 162,266,764.
  GPT-6 Luna, on the owner's server.
- Other message-length families: the best are estimated at 101.3 to 107, not dead but each needing its own package. Helper agents.
- Two "knob" words fixing first-stage bits: false on 2,000 real trials. Proposed by a model reached through the service Venice.
- A constant chunk counter: with t fixed for a run the trials are only relabelled and the rates do not change; a helper agent measured several constant counters and found no gain. The gain of this
  package comes from solving t per trial (Section 8). Helper agents.

**Scope and limitations.**

- No full collision is exhibited; this is an analytical cost claim like other packages on this track and, unlike a birthday search, tests each trial against zero, needing no memory that grows with the
  trials.
- The messages have 1024 t + 55 and 1024 t + 63 bytes, with 1 <= t < 2^32 the solved chunk counter, about 2^41 bytes on average. They rely on the chunk counter and the true block length being inputs
  of the compression, as the target profile specifies; the colliding compression is that of the last chunk, which is not the root, and Lemma TR carries the collision to the complete digests in the
  profile's own tree mode. The 63-byte last chunk ends in eight zero bytes, and both zero-filled last blocks have words 14, 15 and the top byte of word 13 zero.
- The gain over a birthday search comes from matching half the chaining value by construction, constants that let the other half match usefully, the prescription of c1 in the cube of beta* that the
  solved counter makes possible, assumed at 104,884,563,382 times the uniform rate, work shared per outer step, the outer filter, which skips all but about one outer step in 2^7.53 without losing any
  success with the fourteen outcomes, and the joint solver, which finds the successes of a passing outer step without enumerating its trials: 2^90.381 trials walked, at most 2^82.937 of them in
  passing outer steps, not 2^128 (about 2^126.991 at the uniform rate).
- A brief literature search found free-start collisions and near-collisions of reduced BLAKE compression functions and no collision attack on 2-round BLAKE3. No priority or novelty claim is made.
- The time bound charges every operation, load and store of the machine of Section 11, with 64 registers and constants as immediate operands, every row at the budget at which the run halts, each as
  bounded in words by the schedules of Section 11: an upper bound under that convention, not a measured time, and checked by no organizer run. The layout of the joint solver and its cap of 56,096 are
  proved allowances of a schedule that is not implemented. Its largest term is the search part; the discovery preprocessing of 18.6, 2^70 word operations, is charged in full, below 2^-14.16 times it
  (18.7).

**Field meanings.** The fields of the claim of this entry are explained in Section 18.8. The field meanings that the base text gave here were those of the whole-class search (time_log2 69.3343,
success 0.39 under H1' and H4' of 10.3, advice 120 bytes); they are history and are not claimed. The required baseline_improved identifier blake3-r2-nominal-v2 names the organizer's nominal display
reference 128, not an established attack, qualified baseline or security bound; 75.4218 is below it. Whether a qualified result improves the Yukon incumbent is decided separately; no Pareto dominance
claim follows.

## 14. Corrections to our entry c66f230d

Entry c66f230d (time_log2 97.6) cannot be edited. After it was filed its text was examined three times: by a hostile review of another AI model (Grok 4.7), by a referee report of another AI model (GPT
Sol 6.1), and by an audit of a helper agent of the participant that had written nothing of it. Twenty-four points were raised. Each was looked up in the filed text and checked against its source; none
of them changes a lemma, the count or the scalar of that entry, or the value of a figure of its claim block. The same corrections are applied in this package wherever the passage recurs. The full
list, with the filed wording beside the corrected wording, is in the work folder of entry 64c075ac; below are the four that bore on a figure or a scope of the text of that entry, and then the other
twenty in one line each.

*The four that bore on entry 64c075ac.*

1. H1 is not implied by the model M alone. The filed text said that H1 is M together with a rate; in truth M and the rate give the rate of a single trial, and H1 also assumes that the good trials of a
   run do not come in clusters, which M does not imply. (GPT Sol 6.1, with a counterexample: one model sample repeated for every trial has the model's law in every trial and no independence.) Section
   10.3 of this text states H1' in a two-part form.
2. The declared preprocessing of 2^63 units is an exhaustive search over the two message words (W4, W13) at the four given inputs. It does not recompute the four inputs and does not bound the
   selection of the constants, of eta or of rule A; for that selection there is only an estimate from running times, below 2^60 operations, which is not a count. (Grok 4.7 and GPT Sol 6.1.) Section
   18.6 of this text replaces that estimate by a bound on all discovery computation.
3. The share 74,899 / 65,536 = 1.142868 rounds to 1.1429, not to the filed "1.142 times 2^-5" read as 1.1428; the filed figure understates the room of H3. (Audit and GPT Sol 6.1.)
4. The filed sentence that "the six means lie between 0.9977 and 0.9994, all on the low side" is true of the six samples that were chosen. Two further samples of the same program have means 1.0008 and
   0.9978, and the audit's own 512 independent contexts give 1.0039 with a standard error of 0.0028. (Audit.)

*The other twenty, in one line each.* Three were errors of statement whose corrected form this text carries: that the inequality H3 uses holds in every context, while only its form on trials holds on
average alone; that every statement of that text about the pass rate is about an average except H1, which is worded for every trial; and that a member is processed once however many lanes hold it,
because H2 counts trials and not lanes. Two were arithmetic read the wrong way: the per-context cost and charge of the main loop were printed as if they were the totals of the run, and a budget said
to be 2^15.3 above the expected passes is 2^15.4. Six were last digits: 1.39 and not 1.38 times 2^-4 (the largest count is 45,271 of 524,288 members); at most 0.1501 and 0.9994 times 2^-4 for one
context; a Poisson probability of 0.92 and not 0.94; 144,123,440.89 and not 144,123,441; four cells printed under the headings of exact parts that hold estimates, whose exact values are 3,679.1722,
162,266,763.6588 and 2.3109 with the exact total 85074516985129/524288; and 18.2521 operations per trial stated as 18.253. Four were statements stronger than their evidence, now withdrawn or
qualified: a claim about how other tickets count the arithmetic of their inner loop; a sentence that joined two measurements from different samples; the undisclosed rounding of the rule table and of
"1.87 expected good trials", with the two stage-2 shares of its other rows now named; and a summary that can be read as if the estimates were 36.26 million, where that figure is the mass of the
outcomes left out in full and the estimates are 0.28. Two were conventions of the review process that only the note stated: that the 22 findings of an earlier review were applied and not read again,
and what the recounting model was given, that it ran as a coding agent on the participant's machine, and that its answer file names its author otherwise than the package credits it. Three were
reported and are not errors of fact: the mean of the sums against the sum of the four printed means; an ambiguous sentence about lanes and words, which 6.5 of this text states both ways; and a maximum
over 13,312 contexts, which the audit recomputed from the raw files of all ten samples and confirmed. The filed entry also said that it had no scaled-down end-to-end run for this pair of lengths. That
was true when it was filed; Section 13 reports the runs made since.

## 15. What is the same as entries 64c075ac, e7b17fd1 and 26ebba63 and what is new

*The same as entry 64c075ac.* The target and the two block lengths with the zero words they force; the six constants and Fact P; the length cancellation and Lemmas L and H; the class of eta = 830303cf
and Lemmas Q, T and N; the sub-class with Lemma Q2 and rule A with Lemma A, which the root instance and the program keep and the search of this package does not use; the root instance of Sections 4 to
6 with its two-level batch, which the declared experiments run, with their kinds and masks unchanged; the packed word of seven lanes and the machine of 6.5 with its convention; the seven-word model
and the method of the count; the solver search that found the constants (Section 12); and the form of the heuristic H1, here H1'.

*The same as entry e7b17fd1.* The counter construction of Section 8 with Lemma TR, Lemma CT, Theorem C and Lemma IP; the counter batch of 9.2 with Lemma CB and its counts 41 and 72, which the program
holds and the search of 9.1 does not run; the cube Q* of beta*; and Lemmas S1 to S5 and S8.

*The same as entry 26ebba63.* The submitted program and the two declared experiments, unchanged; the outer filter of Section 8 with Lemma F and Lemma S9, here for fourteen outcomes; the joint solver
of 9.4 with Lemmas V and CV, here with the guards of the class and one traversal; the walk over independent outer steps with the pass budget as a halt, here with the outer steps drawn seven to a batch
(9.6); the run set for 0.49676 expected listed good trials; the factor of H1' at five sevenths of the count; and the two heuristics H1' and H4', here declared for the class.

*New.*

| | entry e7b17fd1 | entry 26ebba63 | whole-class base text (history) |
| --- | --- | --- | --- |
| members | sub-class, 2^17 | sub-class, 2^17 | class, 2^19 |
| rule on h1 | rule A | rule A | none |
| outcomes of beta* | 7 | 7 | 14 |
| count for H1 | 138,646,913,024 | 138,646,913,024 | 146,838,388,736 |
| assumed factor | 69,323,456,512 | 99,033,509,302 | 104,884,563,382 |
| margin | 2.00 | 1.40 | 1.40 |
| outer filter | none | exact, share 2^-9.8132 | exact, share 2^-7.5320 |
| guards of the solver | | rule A | (PHASE), (P*) and Lemma J0, all lossless |
| outer steps drawn | | one 256-bit word each | seven to a batch of eight 256-bit words (Lemma PL) |
| trials walked | 2^90.987 | 2^90.463 | 2^90.381 |
| heuristics | H1', H2', H3' | H1', H4' | H1', H4' |
| machine | 16 registers | 16 registers | 64 registers, constants as immediates |
| per walked outer step | all of Q*, 6.5 per trial | 524 | 640 per batch of seven |
| per passing outer step | | 418,816 | 56,608 |
| preprocessing | 2^80, with one more step | 2^70 | 2^55 |
| search part of the time | below 2^84.940 | below 2^70.708 | below 2^69.3343 |
| time_log2 | 84.98 | 71.39 | 69.3343 |

New against entry 26ebba63: the search runs on the whole class of eta with no sub-class and no rule A, after entry dd91b2f6 (Section 16); the count of beta* on the class, 71,698,432 with fourteen
outcomes, and its counting program (10.1, Section 17); the filter for the fourteen outcomes with its exact share (Section 8); the joint solver for the class, with the phase guards, the parity
certificate (P*) of the class and the guard of Lemma J0 on the third addition, one traversal from a common state at depth 7, three transition arrays and a set-up shared by families, and a proved cap
of 56,096 machine units per passing outer step (9.4, Section 11); the outer steps drawn seven to a batch as independent outer steps (9.6); the search charged on a machine with 64 registers and
constants as immediate operands (Section 11); and the selection procedure reduced to the solver runs and one count for each model (Section 12).

(History: the comparison in this table and the next two paragraphs is that of the whole-class base text, not filed; this entry, on the winner sub-class, claims 75.4218, Section 18.) The bound of the
base text falls from 71.39 to 69.3343, by 2.06. The selection procedure falls from 2^69.976 to 2^54.198 units and no longer weighs: it added 0.68 to the bound of entry 26ebba63 and adds 0.00004 here.
The search part falls from below 2^70.708 to below 2^69.3343: the walked outer steps are 0.082 fewer in the exponent, since the count is 1.059 times larger, and a walked outer step costs 91.43 machine
units in a batch against 524; the filter passes 4.86 times as many outer steps (2^-7.532 against 2^-9.813), but a passing outer step is charged at most 56,608 machine units against 418,816. This
package declares no premise beyond the two of entry 26ebba63.

Entry e7b17fd1 was 7.55 below the bound 2^92.53 of entry 64c075ac in the exponent: the prescription of c1 gained 9.55, the factor 747.92, and the cheaper batch 0.24, 6.5 against the 7.7 per trial that
the arrangement of entry 64c075ac charges without its clusters, while the clusters of that entry, worth 2.22 there, are not used, and the selection procedure, charged in full, weighed 0.02 more there
than the allowance of the one formula. Also new in entry e7b17fd1, and new on this track as far as the participant knows: a chunk counter solved per trial, which makes one more round-1 word
prescribable, and a claim whose colliding compression is not the root.

## 16. Credit

The contest is cooperative and this package builds on the work of others. Each is named for what they did. Apart from the helper agents of the participant, nobody named here has reviewed this package,
and a credit is not an endorsement by the person or model credited.

- **GPT Sol 6.1 (OpenAI)**, an AI model run by the participant: the sub-class of the root instance as a sub-cube of the class, with the exact rates of sub-cubes from which it was chosen; the eight
  conditions of rule A; the exact fractions of the rates with and without the rule, which our counter reproduces digit for digit; and the referee report on entry c66f230d behind items 1, 2, 4, 6, 7,
  11, 12, 19 and 23 of Section 14. A second instance of the same model, run separately: a further count of the two fractions and the statements on optimality quoted in Section 13. For the counter
  construction: Lemmas IP and S1 to S8 with their proofs; the reconciliation of the seven outcomes of beta* and of their sum with the count records; the ranking of the 53 values of beta by their
  conditional rates; and the statement of the open part as a premise, from which H1' is worded.
- **winglock**, a participant on this track: the idea of searching only a sub-class of the members, chosen by an exact count per member. It was first used in winglock's entry 18a7fc52 (108.9) on the
  class of our entry 04638ed8 (112.4). That entry is also, to the participant's knowledge, the first public count of the model rate without sampling (a carry automaton on the E1 side, sign patterns
  and a carry recursion on the E3 side). The split used here is for another class and comes from another count; the idea is winglock's. The sub-class of the root instance follows winglock's choice of
  the sub-class S8 in entries 2125212 and 2bb5d604 from the exact rate of every member of the class; the search of this package uses no sub-class.
- **Th0rgal**, a participant on this track: building the values that depend on the member alone once per outer step and not once per trial was first published in Th0rgal's entry df8bd46d (111.75), for
  two lists of the family with lengths 60 and 62. The arrangement of the root instance, five lists per member for the family with lengths 55 and 63, was derived by a solver search of the participant
  some hours later, with that entry known. Three coding steps of 6.5 follow Th0rgal's entry 8c81a219 (98.70), which made them on the batch of our entry c47c1a80: one stored constant w12 - S1 - S6
  across two calls, the rotation by one bit with one mask, and an order of the operations that frees registers.
- **5kyguy**, a participant on this track: keeping masks in registers across the loop over the members, in entry 404d14df (112.12), there on a machine with 32 registers. Here nine words are kept in
  the batch of 6.5 and seven in the counter batch, on the machine with 16 registers.
- **tekkac**, a participant on this track: the lane layout of 6.5, seven 36-bit lanes with a masked rotation, from the public ticket 2bf40fb; the same lanes carry the seven independent outer steps of
  the batch of 9.6.
- **Grok 4.7 (xAI)**, an AI model run by the participant: the hostile review of entry c66f230d behind items 3, 4, 5, 8, 13, 14, 19, 20, 21, 22 and 24 of Section 14; and a tightened batch of its own
  for the first form of the two-level program (stage A 41, stage 2 127), which was compared with the batch of 6.5 and agrees with it in idea; it is not a batch of this package.
- **A model reached through the service Venice**: a statement on prior art and an argument that fixing single bits of message words does not help the first test. Both are unverified, and nothing of
  them is used in a proof or a figure of this package.
- **Helper agents of the participant**, instances of the same AI model as the author of this text: the solver search for the order of Section 4, the program and its tests, the count of Section 13, the
  first form of Lemmas T2 to T4 and their check, the layout runs and their check, the scaled-down runs and their check, and the audit of entry c66f230d. For the counter construction: the search that
  found that a chunk counter solved per trial makes E1.d1 prescribable next to Y4, and the order of Section 8; an independent check of the tree mode with the organizer's code, of the free words of the
  orders and of the construction in 32-bit arithmetic; the measurements on real counter trials and the count of the counter batch on the program's machine; the scaled-down end-to-end run with real
  collisions of complete messages; an adjudication of these reports; the counter part of the program, its self-test and the checks of Section 7; and this text.

The half-collision, the class search and the two tests are those of the participant's entries 17bba2ae, 5ceb1802, 04638ed8, c47c1a80, c66f230d and 64c075ac on this track, which claim 123.5, 121.5,
112.4, 99.4, 97.6 and 92.53.
- GPT Sol 6.1 (OpenAI), answer AC: Lemma F (the outer-step filter lemma), Lemma S9 and the exact certificate of the pass share; helper agents (instances of the AI model that wrote this text) proposed
  the outer-step filter and built and measured it.
- **The participant who filed entry dd91b2f6** on this track (69.3452, built on entry 47804be2 of this participant): dropping the sub-class and rule A in the solver design, because rule A only served
  the enumeration of the cube, so that y ranges over the whole class of eta and the selection procedure shrinks to the solver runs and one count per model; the observation that the counting program of
  Section 17, run on the class, gives fourteen outcomes of beta* with part 71,698,432; and its measurement of the pass share of the fourteen-outcome filter quoted in 10.3. This package takes that step
  with the deterministic charge and the two premises of entry 26ebba63, and uses neither the program, nor the sample, nor the premises of entry dd91b2f6. That participant has not reviewed this
  package.
- **GPT Sol 6.1 (OpenAI)**, answers AI, AL, AN, AO, AQ and AR: the transition relation of the solver and the blocks of its formulas (AI); its register traversal on 64 registers and the allowances of a
  leaf and of a root (AL); the filter certificate for fourteen outcomes and its share (AN); the phase guards, the single traversal and the common state of the solver for the class (AO); the
  independent packed lanes of the batch with their proof and the charges of 640 per batch and 512 per passing lane, and the scale of the count of the class (AQ); and the parity certificate (P*) of the
  class, Lemma J0, the three transition arrays, the allowances of the nodes, the set-up shared by families, the ledger of the static trees with the cap of 56,096 and the complete charge of this
  package (AR).
- **Helper agents of the participant**, for this package: the count of the class of Section 17, the exact recount of the selection records of Section 12, the checks of the fourteen-outcome filter
  (Section 8), the count of (P*) in one phase and the check of the cells of (P*) against the counts of 10.1 (9.4), the recount of the free positions, the static trees, the families and the caps from
  GPT Sol's answers (9.4, Section 11), the implementation of the batch of seven outer steps and its check (9.6), and this text.

## 17. The counting program for 71,698,432

The program below computes the part of beta* = 18b0e098 in the rate of the class of eta (Section 10.1) in exact integer arithmetic, with the standard library only: every tau (taus), both roots eps
(eps_roots), the E1 count L_j (L_count) and the E3 count N3_j (N3_count), each as an exact carry count over all bit positions, with Y4 over all 524,288 members of the class (Lemma Q) and no rule on
h1. Nothing is sampled, capped or delegated to a solver. It is the program printed by entry 26ebba63 with these changes only: the header comment, the member list (the class in place of the sub-class)
with its size check, the empty rule, and the final check. Run as `python3 -B count.py`, it printed the table below in about 2.5 minutes (Python 3.14). Its column L*N3/2^81 and its sum, 286,793,728,
are four times the last column of the table of 10.1 and its sum, 71,698,432, the part on the scale of a trial with Y4 uniform in the class (10.1); its column "rule A" is the count with the empty rule
and equals N3 in every row. Its self-test, a brute force at width 6 that follows the listing in the file, ran 12 seeds with no mismatch.

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

Output of that run (the outcome table):

```text
beta 18b0e098: 14 outcomes with L * N3 > 0
tau       eps       L                  N3                 L*N3/2^81  rule A
175020a0  6e21be55  562949953421312    108086391056891904  25165824   all
175060a0  6e21be55  281474976710656    6755399441055744   786432     all
185020a0  6e21be55  2251799813685248   72057594037927936  67108864   all
185060a0  6e21be55  1125899906842624   9007199254740992   4194304    all
275020a0  6e21be55  562949953421312    18014398509481984  4194304    all
275060a0  6e21be55  281474976710656    1125899906842624   131072     all
285020a0  6e21be55  2251799813685248   108086391056891904  100663296  all
285060a0  6e21be55  1125899906842624   13510798882111488  6291456    all
385020a0  6e21be55  1125899906842624   144115188075855872  67108864   all
385060a0  6e21be55  562949953421312    18014398509481984  4194304    all
675020a0  6e21be55  140737488355328    4503599627370496   262144     all
675060a0  6e21be55  70368744177664     281474976710656    8192       all
685020a0  6e21be55  562949953421312    27021597764222976  6291456    all
685060a0  6e21be55  281474976710656    3377699720527872   393216     all
part = sum / 2^81 = 286793728 remainder 0; with rule A 286793728 remainder 0
seconds 141.6
sum / 2^83 = 71698432 remainder 0  (= sum / 2^81 divided by 2^19 / 2^17 = 4)
CHECK whole class, no rule: sum / 2^81 = 286,793,728; sum / 2^83 = 71,698,432 (rival dd91b2f6)
exit 0
```

**End of Section 17.**

## 18. The winner sub-class: the search of this entry (governing)

This section defines the search of this entry and governs every figure of the claim. It restricts the members of the search of Section 9 to one phase of the class of eta and prices the run with the
guarded solver cap and the packed lanes of Sections 9.4, 9.6 and 11. Its pricing follows GPT Sol 6.1, answer AN 7 (AN 7.1 for the transfer, AN 7.2 for the budgets, the success and the numerator
without a selection term); its solver cap is that of answer AR 6 and its packed lanes those of answer AQ (Section 18.10).

**18.1 The winner member.** As in 9.4, for a member y write e1 = Y3 + y and b = e1[2], u = e1[21], v = e1[26]; these three bits are free in the class (Lemma Q and step 1 of 9.1: e1 = 030c0303 + (W AND
fc307cfc), and bits 2, 21 and 26 are set in fc307cfc and clear in 030c0303). The *phase* of a member is (b, u, v). The *winner sub-class* is the set of the 2^16 members of the class with phase (1, 0,
1). In this entry the eighth word W of the random word of an outer step gives the member by

    e1 = Y3 + y = 070c0307 + (W AND f8107cf8),   y = e1 - Y3.

The two constants are formed from those of the class: 070c0307 = 030c0303 OR 04000004 sets b = 1 and v = 1, and 07ef8307 = 03cf8303 OR 04200004 is the mask of the 16 fixed positions, the 13 of Lemma Q
and bits 2, 21 and 26; f8107cf8 = NOT 07ef8307 has 16 bits and is a subset of fc307cfc. 070c0307 AND f8107cf8 = 0, so the addition is an OR, e1 = 070c0307 OR (W AND NOT 07ef8307), the form of answer
AN 7.1.

**Lemma PLw (the winner member).** (a) For every W the word y is a member of the class with phase (1, 0, 1), and each of the 2^16 such members arises from exactly one value of W AND f8107cf8. (b) If W
is uniform, y is uniform on the winner sub-class; the bits of W outside f8107cf8 are ignored, not conditioned on. (c) With this member rule the statements of Lemma PL hold as written, with "the class"
replaced by "the winner sub-class": the outer steps of a run are independent and identically distributed, each with the law of one outer step drawn alone, its seven outer words uniform and independent
of its member.

Proof. (a) e1 has the value 030c0303 at the 13 positions of 03cf8303, so y is a member of the class (Lemma Q); bits 2 and 26 of e1 are 1 and bit 21 is 0 by the constant 070c0307, so the phase is (1,
0, 1); the other 16 positions of e1 are the bits of W at the positions of f8107cf8, and every assignment of them occurs once. (b) follows from (a), since W AND f8107cf8 is uniform on its 2^16 values
when W is uniform. (c) The proof of Lemma PL uses of the member rule only that the member is a function of the eighth word alone and uniform on its set of members; (b) gives both. QED. (GPT Sol,
answer AN 7.1: the member is an exact uniform winner member; the extra raw bits are ignored, not conditioned.)

*The batch with the winner member.* The batch of 9.6 ANDs R_7 with the word that has the bits of f8107cf8 set in every lane, in place of fc307cfc, and the pending constant is 070c0307 - Y3 in place of
030c0303 - Y3. These are the same AND with another mask and the same pending addition with another constant; every lane of W AND f8107cf8 is below 2^32 and the constant is below 2^32, as in 9.6, so
the interval bounds of Lemma PB, the count of 640 units per batch and the 512 units of a passing lane are unchanged (9.6 notes that its bound computation was made with the mask f8107cfc of the
sub-class of entry 26ebba63, of which f8107cf8 is a subset). No group or frame dependence premise is introduced: the lanes are disjoint fresh bits (Lemma PL (a)).

**18.2 What transfers to the winner sub-class.** Each item below holds for every member of the class, so for every member of the winner sub-class.

- The construction and the half-collision of Sections 7 and 8 (Theorem C, Lemmas TR and IP): they hold for every member y of the class.
- The filter of Section 8 with Lemma F and its exact share pi14 = 1,520,837,058,143 / 2^48 (the share pi of Section 8): Lemma F uses no law of the words and holds for any member; pi14 is the share of
  uniform word pairs.
- The joint solver of 9.4 with Lemmas V and CV: the phase equations (PHASE), the parity certificate (P*) and Lemma J0 hold for every joint root of every one of the fourteen outcomes for y in the
  class, in every phase. The winner is the phase b = 1, u = 0, v = 1, so every old and every new row is covered, with the parity h[6] XOR h[13] XOR h[25] = u XOR tau_j[14] = tau_j[14]; its guards are
  the specialization of 9.4 to this phase (answer AN 7.1, from AR 6). The traversal checks all three full-word equations at every leaf and reaches each h once. Steps 2 and 3 cost at most 56,096
  machine units in every passing outer step, whatever its words, including the global set-up, every leaf and the inverse, cube, t and E1 checks of each accepted root (Section 11; answer AR 6.5), and a
  passing outer step has at most 72 roots (Lemma CV). This all-phase cap covers the winner pointwise; it is not claimed to be the least winner-only bound (answer AN 7.3).
- The packed batch of 9.6 at 640 machine units per batch of seven lanes and 512 more per passing lane, with the member of 18.1 (Lemma PLw).
- The once-only set-up of Section 11, Dnew = 2^20 + 4 * 2^26 + 40 = 269,484,072 machine units.
- Lemmas S1, S8 and S9 (10.2): the proofs of S1 and S9 hold for any fixed set of members (GPT Sol, answer AN 1), here the winner sub-class; Lemma S8 is general.

**18.3 The algorithm of this entry and its budgets.** The algorithm is that of 9.1, steps 0 to 4, with three changes: (1) the member rule of 18.1 in step 1;
(2) the number of proposals (outer steps) B in place of RUN_STEPS and the number of batches J7 in place of RUN_BATCHES; (3) the pass budget L in place of PASS_BUDGET. With

    mu = (2^21 - 1) * 5 * 9297 / (7 * 2^104),

the premised mean per proposal of H1prime-winner (18.5),

    B    = 52,256,980,094,639,195,695,325              (about 2^75.468),
    J7   = ceil(B / 7) = 7,465,282,870,662,742,242,190,
    L    = ceil(17 * B * pi14 / 16)
         = 299,996,468,082,244,789,290                 (about 2^68.024),
    pi14 = 1,520,837,058,143 / 2^48.

B is the least integer with B * mu / 72 >= x = -ln(exp(-1/2) + 0.001) = 0.49835263637816257546522013..., so that exp(-B * mu / 72) <= exp(-1/2) + 0.001 (18.5): B * mu / 72 =
0.49835263637816257546522591... and (B - 1) * mu / 72 = 0.49835263637816257546521637..., with mu exact and x evaluated to 80 digits. 7 * J7 = B + 5, so in the last batch lanes 2 to 6 are not used
(their proposals are discarded, not retained), and the last batch is charged 640 in full. The run halts with failure when the count of passing lanes exceeds L, or after the J7-th batch. As in 9.1, a
pair is formed and hashed only for a certified root, and it is then a collision of two complete messages (Lemma V, Lemma TR (c)).

**18.4 The count of the winner rate.** The cells of the parity certificate (P*) of 9.4 split every N3_j of 10.1 by the phase (b, u, v) of Y4: an old row has the count a_j * 2^49 in every phase; a new
row 185, 285, 385 or 685 has a_j * 2^47 in the phases with u XOR v = 1 and 0 otherwise; a new row 175, 275 or 675 has a_j * 2^47 in the phases with u XOR v = 1 and b = 1 and 0 otherwise; a_j = 24, 16,
4, 24, 32, 1 and 6 for the rows 175, 185, 275, 285, 385, 675 and 685, in both versions. In the winner phase (1, 0, 1), u XOR v = 1 and b = 1, so all fourteen rows count. With N3w_j the count of the
quadruples of 10.1 with Y4 in the winner sub-class, and the scale 2^80 of a trial with Y4 uniform on 2^16 members (2^83 for the 2^19 members of 10.1):

| j | tau | L_j | N3w_j | L_j * N3w_j / 2^80 |
| ---: | --- | ---: | ---: | ---: |
| 1 | 175020a0 | 562,949,953,421,312 | 13,510,798,882,111,488 | 6,291,456 |
| 2 | 185020a0 | 2,251,799,813,685,248 | 9,007,199,254,740,992 | 16,777,216 |
| 3 | 275020a0 | 562,949,953,421,312 | 2,251,799,813,685,248 | 1,048,576 |
| 4 | 285020a0 | 2,251,799,813,685,248 | 13,510,798,882,111,488 | 25,165,824 |
| 5 | 385020a0 | 1,125,899,906,842,624 | 18,014,398,509,481,984 | 16,777,216 |
| 6 | 675020a0 | 140,737,488,355,328 | 562,949,953,421,312 | 65,536 |
| 7 | 685020a0 | 562,949,953,421,312 | 3,377,699,720,527,872 | 1,572,864 |
| 8 | 175060a0 | 281,474,976,710,656 | 3,377,699,720,527,872 | 786,432 |
| 9 | 185060a0 | 1,125,899,906,842,624 | 2,251,799,813,685,248 | 2,097,152 |
| 10 | 275060a0 | 281,474,976,710,656 | 562,949,953,421,312 | 131,072 |
| 11 | 285060a0 | 1,125,899,906,842,624 | 3,377,699,720,527,872 | 3,145,728 |
| 12 | 385060a0 | 562,949,953,421,312 | 4,503,599,627,370,496 | 2,097,152 |
| 13 | 675060a0 | 70,368,744,177,664 | 140,737,488,355,328 | 8,192 |
| 14 | 685060a0 | 281,474,976,710,656 | 844,424,930,131,968 | 196,608 |
| sum | | | | 76,161,024 |

The L_j are those of 10.1, and 76,161,024 = 9297 * 2^13. By Lemma S1 for this set of members (it holds for any fixed set, 18.2), the model rate of a trial with c1 in Q* and Y4 uniform on the winner
sub-class is

    pwin = 2^11 * 76,161,024 * 2^-128 = 9297 / 2^104,   about 2^-90.8175,

1.06224 (= 37,188 / 35,009) times the rate p = 35,009 / 2^106 of the class.

*The eight phases.* The same cells give the part of beta* in every phase, on the scale 2^80:

| phases (b, u, v) | rows with a nonzero count | part | model rate of the phase |
| --- | --- | ---: | ---: |
| (0,0,0), (0,1,1), (1,0,0), (1,1,1) | the seven old rows | 67,698,688 | 8,264 / 2^104 |
| (0,0,1), (0,1,0) | old rows and new 185, 285, 385, 685 | 75,235,328 | 9,184 / 2^104 |
| (1,0,1), (1,1,0) | all fourteen | 76,161,024 | 9,297 / 2^104 |

The mean of the eight parts is 71,698,432, the part of the class (10.1). The two largest parts are equal; the advice record of 18.6 stores (1, 0, 1), the first in lexicographic order. The part
67,698,688 of the old rows is that of the sub-class of entry 26ebba63 (10.1).

*Who counted what.* The cells are GPT Sol's evaluation (answer AR 1), checked against the fourteen N3_j of 10.1 by a helper agent of the participant (9.4). For the winner phase, a separate exact count
of a helper agent of the participant, with the function N3_count of the program of Section 17 and the parity as one more condition, gave all fourteen counts of the first table; the cells of the other
seven phases were not re-run by the participant. The arithmetic of both tables was recomputed by a helper agent in exact integers.

**18.5 The two premises and the success probability.** Both are stated for the law of the winner sub-class, not for the law of the class (10.3) or of the sub-class of entry 26ebba63; no premise on a
mean of work and none on groups of proposals is made (answer AN 7.2).

**Heuristic H1prime-winner (score-critical; claim id H1prime-winner-rate).** Over the coins of the run, the B independent retained proposals of 18.3, let Zwin be the number of valid trials (t != 0) of
one proposal that are listed good trials (R = 0 with an E1 outcome among the fourteen of beta*), counted over all of Q* whether or not the proposal passes the filter. *Rate:* E[Zwin] >= mu =
(2^21 - 1) * 5 * 9297 / (7 * 2^104), five sevenths (margin 1.4) of the exact model rate pwin per trial. This is the whole premise: it states no dependence clause.

*No hit, from the rate and the proved cap.* A proposal has Zwin <= 72 (Lemma CV; a proposal that fails the filter has Zwin = 0, Lemma F), so rho_w = E[Zwin (Zwin - 1)] / E[Zwin] <= 71 and b(rho_w) >=
b(71) = 73 / (72 * 73) = 1/72 in Lemma S8 (directly: 1[Zwin > 0] >= Zwin / 72). The proposals are independent (Lemma PLw), so under the rate premise the probability that no proposal of the run holds
such a trial is at most exp(-B * mu / 72) <= exp(-1/2) + 0.001, by the choice of B in 18.3. No bound on rho_w beyond the proved rho_w <= 71 is assumed. (History: entry afbe2154 assumed rho_w <= 0.0065
in a part (ii) of this premise; 18.9.)

**Heuristic H4prime-winner (supporting; claim id H4prime-winner-pass-budget).** With probability at least 0.9995 over the coins, at most L of the B retained proposals pass the filter of the fourteen
outcomes, so the pass-count halt is not reached. Reaching it halts the run with failure; the time bound charges L + 1 passing lanes. (The proposals are independent and identically distributed (Lemma
PLw), so the number of passing proposals is binomial with B steps and the sampler's pass probability pi_ow of a winner proposal. pi14 is the exact share for uniform independent pairs (Y9, omega); that
the sampler's pair has this law is not proved. If pi_ow <= 1.06 pi14 the mean is at most 1.06 / 1.0625 of L, and the Chernoff bound puts the probability of more than L passing proposals below
exp(-10^13). The product-model share alone is not a proof of this premise (answer AN 7.2). The participant's measurement of the pass share quoted in 10.3 drew members from a part of the class; none
was made on the winner sub-class.)

**Success.** The probability space is the B random words of the retained proposals, made of disjoint fresh bits (Lemma PLw); the algorithm is otherwise deterministic. B * mu / 72 >= x by 18.3. Under
H1prime-winner and H4prime-winner the run outputs a collision with probability at least

    1 - (exp(-1/2) + 0.001) - 0.0005 = 0.391969340287...  > 0.3919693,

the union bound over the two failure events, "no proposal holds a listed good valid trial" (H1prime-winner with Lemma CV) and "the pass budget is reached" (H4prime-winner). A listed good trial lies in
a passing proposal (Lemma F) and is certified unless the run ends before its proposal is reached (Lemma CV); an output pair is a genuine collision (18.3). No workload-mean premise and no work-tail
subtraction enters: every row of the time is charged at its budget.

**18.6 The advice record, Lemma ADV and the preprocessing bound.** The algorithm of 18.3 reads the values below as fixed nonuniform advice. They are printed here in full; nothing else that was chosen
enters the run.

| item | value | bytes |
| --- | --- | ---: |
| X3, X7, X11, X15, W4, W13 (3.2) | 29d4fa98 bee3af28 44036000 40c58500 97475638 0007c006 | 24 |
| eta (6.1) | 830303cf | 4 |
| beta*, the mask and the value of its cube (10.1) | 18b0e098 0e09818b 02008000 | 12 |
| the fourteen tau_j (10.1) | 175020a0 185020a0 275020a0 285020a0 385020a0 675020a0 685020a0 175060a0 185060a0 275060a0 285060a0 385060a0 675060a0 685060a0 | 56 |
| the eps of all fourteen outcomes (10.1) | 6e21be55 | 4 |
| the winner phase (b, u, v) (18.1) | (1, 0, 1), one word | 4 |
| the two bits 21 and 26 of e1 that define the sub-class and their value 0, which the submitted program stores for its root instance (6.1, Section 12) | two words | 8 |
| the two masks and the word ALL of Lemma A, stored by the submitted program | 0003c000 40010000 4f010300 | 12 |
| total | | 124 |

The record has 124 bytes, below 2^7: nonuniform_advice_log2_bytes = 7. The member constants 070c0307 and 07ef8307 are formed from the phase and eta (18.1); the automata of the filter, the transition
arrays and the descriptors of the solver are computed from the record (Section 12); B, J7 and L are the integers of 18.3.

**Lemma ADV (the claim uses only the printed record).** Every property of the record that the budgets of 18.3, the success bound of 18.5 and the time bound of 18.7 use is a statement about the printed
values that this text proves by a finite computation or counts exactly:

(a) the six constants: Fact P, a finite computation on them (lines 150-164), and Theorem C, which rests on it with Lemmas L, H and CT (lines 873-894);
(b) eta: Lemma Q, the class and its 2^19 members (lines 369-378); the phase: Lemma PLw, the exact uniform winner member (lines 2545-2553);
(c) beta* and its cube: Theorem C (iv), c1 is in Q* exactly when the difference is beta* (lines 873-894);
(d) the fourteen outcomes: their exact counts L_j and N3_j (lines 1400-1426), from the counting program printed with its output in Section 17 (lines 2273-2527); the filter of Lemma F and its exact share
pi14 (lines 929-1002); the guards (P*) and Lemma J0 of the joint solver (lines 1136-1321) and Lemmas V and CV (lines 1517-1547);
(e) the winner rate: the counts N3w_j and pwin = 9297 / 2^104 (lines 2592-2635).

The premises H1prime-winner and H4prime-winner are stated for this record and the law of its winner sub-class (18.5). Hence the budgets, the success bound and the time bound hold for the record as
printed, whatever computation produced it, and the claim contains no statement that a procedure returns these values.

Proof. 18.3 computes B, J7 and L from 9297 and pi14 alone. 18.5 uses the two premises, the integers of 18.3 and Lemmas CV, F, PLw, V and S8. 18.7 uses the caps of 9.4, 9.6 and Section 11, which hold
for every member of the class and every outer step (18.2). Each of these lemmas and counts is listed in (a) to (e), or holds for any values (Lemmas TR and S8). QED.

*The preprocessing bound.* The record was found by computation of the participant's project: the solver runs and counts of Section 12, the counts of 10.1, Section 17 and 18.4, and every other program
that the participant, its helper agents and the models it used ran. This entry neither replays that computation nor claims that a procedure returns the record. It charges as preprocessing a bound on
all of it, from the participant's attested list of every machine used by any of the project's models over a window of 30 days, 2,592,000 seconds, each device at its peak rate, lanes times clock times
2 operations per lane and cycle, one primitive word operation per hardware 32-bit lane-instruction:

| device | operations per second |
| --- | ---: |
| 1 RTX 3090: 10,496 lanes, 2.1 GHz | 44,083,200,000,000 |
| 4 RTX 3070: 5,888 lanes, 2.0 GHz each | 94,208,000,000,000 |
| 24 local processor cores: 64 lanes (AVX-512, 4 ports), 5.5 GHz each | 16,896,000,000,000 |
| 64 server processor cores (allowance), the same rate per core | 45,056,000,000,000 |
| at most 4 cloud and model sandboxes at all times, each as 64 such cores | 180,224,000,000,000 |
| total | 380,467,200,000,000 |

The total rate is below 2^48.4348 operations a second. Over the window

    380,467,200,000,000 * 2,592,000 = 986,170,982,400,000,000,000
      < 2^70 = 1,180,591,620,717,411,303,424,

about 2^69.7404. The entry charges PREPROCESSING = 2^70 primitive word operations, 2^70 / 430 units, below 2^61.2519 units, in full inside T (18.7); preprocessing_log2 = 62 bounds it. This is the
supporting premise HPRE-discovery-bound: all discovery computation is at most 2^70 charged word operations, under the attested device list and window. It assumes that the list and the window are
complete (participant attestation), that one hardware 32-bit lane-instruction is charged as one primitive word operation, and that model reasoning that produced formulas is not candidate search and is
not counted. If the bound were 2^72, then X = N + 2^72 + 430 * 2^38 = 21,764,703,469,024,935,481,870,216, log2 T = 75.42199988700337..., and the claim would be time_log2 = 75.4220, checked as in 18.7
with the exponents 754220 and 754219.

**18.7 Charged time.** The machine and the allowances are those of Section 11. The rows of this entry, each charged at its budget:

| Row | How often over a run, at most | Units | Machine units | log2 |
| --- | --- | ---: | ---: | ---: |
| batch of seven lanes (9.6, 18.1) | J7 = 7,465,282,870,662,742,242,190 | 640 | 4,777,781,037,224,155,035,001,600 | 81.9826 |
| passing lane: 512 outside steps 2 and 3, and the cap 56,096 of steps 2 and 3 | L + 1 = 299,996,468,082,244,789,291 | 56,608 | 16,982,200,065,199,713,032,184,928 | 83.8122 |
| once: Dnew (Section 11) | once | 269,484,072 | 269,484,072 | 28.0057 |

The numerator, in exact integers:

    N = 640 * J7 + 56,608 * (L + 1) + 269,484,072
      = 21,759,981,102,423,868,336,670,600 machine units,

the numerator of answer AN 7.2 in form, with the budgets of 18.3. The final step is below 2^38 units (Section 11, one-time items). The preprocessing of 18.6, PREPROCESSING = 2^70 primitive word
operations, is charged in full:

    T <= (N + 2^70) / 430 + 2^38 = X / 430,
    X  = N + 2^70 + 430 * 2^38
       = 21,761,161,694,162,783,247,959,944,
    T <= 50,607,352,777,122,751,739,441.730... units,
    log2 T = 75.42176509782586...

Without the preprocessing term, log2 (N / 430 + 2^38) = 75.42168682627473.... In integers,

    X^10000 <= 430^10000 * 2^754218   and   X^10000 > 430^10000 * 2^754217,

so the total rounded up at the fourth decimal is time_log2 = 75.4218. The batches are 21.96 per cent of N and the passing lanes 78.04 per cent. Per walked trial, B * 2^21 of them, N is 0.00019856
machine units (2^-12.298). The preprocessing is below 2^-14.16 times the search part and adds less than 0.00008 to log2 T. This is a worst-case bound for the algorithm as stated: it halts within its
pass budget on every run and steps 2 and 3 are bounded in every passing proposal; no mean of a count of work enters it, the two premises of 18.5 enter only the success probability, and
HPRE-discovery-bound enters only the preprocessing term. Not used: the small selection procedure SEL-small of answer AN 7.2, whose charge gave 69.2789 at the B of entry afbe2154 (18.9), and the
selection procedure SEL that entries e85fffe8 and 78ac164c charged at 8,918,253,162,100,551,680 operations (18.9).

**18.8 Field meanings.**

- time_log2 = 75.4218 bounds the total charged time, search and preprocessing, by 2^75.4218 units (18.7): log2 T = 75.42176509782586....
- memory_log2_bytes = 44: as in Section 12, the search with its code (below 2^29 bytes), the advice and the output (below 2^43 bytes), even all held at once; the discovery computation is covered too: every attested device together has less than 2^41 bytes of memory (the local RTX 3090 and its host, the four-GPU server and its host, and at most four cloud sandboxes of at most 256 GiB each), so even counted at once with the search and its output (below 2^43 + 2^29 bytes) the total stays below 2^43 + 2^41 + 2^29 < 2^44.
- preprocessing_log2 = 62 bounds the discovery computation of 18.6, 2^70 primitive word operations, by 2^62 units (2^70 / 430 is below 2^61.2519 units), under HPRE-discovery-bound; it is included in
  time_log2.
- nonuniform_advice_log2_bytes = 7: the record of 18.6 has 124 bytes, at most 2^7 = 128; the member constants 070c0307 and 07ef8307 are formed from it (18.1).
- success_probability = 0.3919693 holds under H1prime-winner (the rate) and H4prime-winner as shown in 18.5 (the bound is 0.391969340287...).

**18.9 What is proved, what is assumed, and the limits.**

*Exact or proved:* the construction and its half-collision (Sections 7 and 8); the filter and its exact share; the winner member and Lemma PLw (18.1); the completeness of the joint solver and its cap
of 56,096 machine units per passing proposal, proved for all phases by GPT Sol (answers AR 1, 2 and 6, AN 7.1) and not implemented; the packing at 640 and 512 units (answer AQ); the model rate pwin =
9297 / 2^104 as an exact count under the model of Section 10 (18.4); every integer of 18.3, 18.6 and 18.7; Lemma ADV for the printed record (18.6); the no-hit bound from the rate, by the cap Zwin <=
72 (Lemma CV) and Lemma S8 with b = 1/72 (18.5).

*Assumed:* H1prime-winner, that the construction's winner trials realise at least five sevenths of pwin (a rate only, with no dependence clause); and H4prime-winner, the pass budget. The margin of the
rate is the factor 1.4 between pwin and the premised rate. For the time bound only: HPRE-discovery-bound, that all discovery computation is at most 2^70 charged word operations under the attested
device list and window (18.6). No premise states what a selection procedure returns (Lemma ADV).

*History: entry afbe2154 (69.2566).* Entry afbe2154 was this section with B = 728,190,579,544,334,257,776 (the least B with B * mu >= 1/2), J7 = 104,027,225,649,190,608,254, L =
4,180,390,859,908,750,542, the numerator 303,220,990,213,196,809,504,776 and time_log2 69.2566, under a premise H1prime-winner-rate-and-dependence whose part (ii), a no-hit and dependence clause, was
sufficient with rho_w <= 0.0065. It was ruled not_evaluable on 2026-10-09: all four review lanes rated that premise unsupported, naming the dependence clause (only rho_w <= 71 is proved) and the
absence of a measurement of the rate on the winner sub-class. That entry reported the pricing with the proved bound alone, 75.4217, and did not claim it. This section drops part (ii) and claims that
pricing, 75.4218 with the preprocessing term of 18.7 (B is 71.76 times the B of afbe2154); the rate premise and H4prime-winner are unchanged in form.

*History: entries e85fffe8 and 78ac164c (75.4217).* Both filed this search with the selection procedure SEL charged in T at 8,918,253,162,100,551,680 operations. Entry e85fffe8 was ruled not_evaluable
on 2026-10-09: the evaluability lane rated an implicit premise, that SEL returns these values, unsupported; the package had not declared it. Entry 78ac164c declared that premise as
HSEL-selection-return and was ruled not_evaluable: the experiments lane rated it unsupported, and the ruling pointed to a structure in which the score does not depend on SEL returning these exact
values. This entry has that structure: the values are the advice record printed in 18.6, Lemma ADV shows that the claim uses only properties of the record proved or counted in this text,
HSEL-selection-return is withdrawn, and the selection term of T is replaced by the discovery bound of 18.6, 2^70 word operations under HPRE-discovery-bound, which moves time_log2 from 75.4217 to
75.4218.

*Not done:* no implementation of the winner search, of the joint solver in the layout of 9.4 or of the batch with the winner mask has been run; no measurement on the winner sub-class of the rate, of
the dependence or of the pass share has been made. The organizer-run experiments run the root instance of the construction (counter 0, flags 11), and the submitted program is that of entry 26ebba63,
which does not run the winner path: it has no winner member, no fourteen-outcome filter, no guarded solver and no packed proposals. The joint 128-bit event, about 2^-91.3 per trial at the premised
rate, is not measured at 32 bits. The cap of 56,096 is the all-phase bound and may not be the least winner-only bound (answer AN 7.3). The discovery computation is bounded from the attested devices
and window, not replayed or metered (18.6).

**18.10 Credit and lineage.**

- **GPT Sol 6.1 (OpenAI)**, an AI model run by the participant: answer AN 7 (the transfer of the guard proof and of the packing to the winner sub-class, the winner-specific premises, the exact budgets
  B, J7 and L and the hard numerator 303,220,990,213,196,809,504,776 without a selection term, those of entry afbe2154, 18.9; this section keeps their form at the new B); answer AR (the parity
  certificate (P*) with its cells by phase, Lemma J0, the guarded single traversal and its cap of 56,096 with the once-only set-up); answer AQ (seven independent proposal lanes packed from disjoint
  input bits, 640 per batch and 512 per passing lane).
- **The base text** of Sections 1 to 17, the whole-class search of the participant (not filed), whose construction, filter, solver and batch this entry uses.
- **Entry 26ebba63** of the participant (71.39, reviewed: plausible_not_refuted), the chunk-counter search with the exact filter and the guarded joint solver on the sub-class, of which this entry is a
  continuation; and an earlier draft of this winner entry by the participant, not filed, which charged the selection outside the time.
- **Helper agents of the participant**, instances of the AI model that wrote this text: the separate exact count of the winner phase (9.4), the exact recomputation of every integer of this section,
  and this section.
- The people and models credited in Section 16 are credited for the same work here.

**End of Section 18.**
