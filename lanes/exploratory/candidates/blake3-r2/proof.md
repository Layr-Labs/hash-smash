# A free half-collision and a search inside one class for 2-round BLAKE3

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
separately reported resource bound.

This exploratory package targets blake3-r2-prefix-v1. It has an exact part and
a heuristic part, and it keeps them apart.

**Exact part.** An explicit construction maps any eight 32-bit words to a
55-byte message A and a 63-byte message B whose complete 2-round BLAKE3-256
digests agree on digest words 0, 2, 5 and 7, that is on 128 of the 256 digest
bits. There is no search in this construction and no probability: it holds for
all 2^256 choices of the eight words (Sections 2 to 5). One of the eight words
is the value of one internal word of round 1, called Y4. The search holds Y4
inside a set of 524,288 values, the *class* (Section 6.1).

**Heuristic part.** A collision needs the other four digest words to agree as
well. The algorithm searches 2^102 such pairs, all with Y4 in the class, for
one where they do. The search has no table that grows with the number of trials
and does no sorting or lookup. Seven trials are evaluated in one 256-bit word,
in two stages. Every batch runs stage A, which tests five bit conditions on one
internal word of every trial (rule A). Only a batch in which a trial satisfies
rule A runs stage 2, which tests a 32-bit condition that every collision
satisfies. A batch in which no trial satisfies rule A is dropped; a trial that
fails rule A is examined further only if another trial of its batch satisfies
it, and Section 7 does not count such a trial. A trial is charged 19.1
primitive operations, memory loads included. Three heuristics are declared: H1,
that a trial satisfies rule A and completes the collision with probability at
least 2^-103; H2, that a budget on the passes of the second test suffices; and
H3, that at most one quarter of the batches run stage 2. Under the three the
search succeeds with probability at least 0.39. Total charged time is below
2^97.52 target-compression units, so the claimed scalar is 97.6. The search
needs less than 2^22 bytes of memory; the declared 2^35 bytes also cover the
computations by which the constants and the class were selected (Sections 6 to
9).

The rate in H1 is an assumption: 2^25 = 33,554,432 times the rate of a uniform
128-bit value. It is not read off single digest words. Section 10 describes
what it is set against. The remaining half of the digest depends on seven
words, one of which is Y4. Under the model that the other six behave like
independent uniform words over the trials, the rate is the number of solutions
of a fixed system of equations, and that number is counted: it is 162,266,764
times 2^-128 for Y4 in the class, all but a part below 1 from an enumeration
without sampling. Rule A is not implied by a collision: some solutions violate
it and are lost. The figure that the claim uses is therefore smaller. It leaves
out every part of the count for which a solver found a solution that violates
rule A, and the part that rests on estimates, about 36.26 million in all, and
is 126,003,600. H1 assumes 33,554,432 times, 3.75 times less. The counting
program is not part of the package, and it and all its checks are the
participant's. The model was compared with real messages only on events of
probability about 2^-40 and above, the deepest of them events of one of the two
calls alone, and one comparison shows that the model does not hold inside a
single context: the share of the trials of one context that satisfy rule A
differs from context to context, and only its average over contexts is the
model's value (Section 10). The organizer-run experiments measure neither the
model nor the factor. With the uniform rate in place of 33,554,432 times it,
the same search needs 2^127 trials and gives time_log2 = 122.6.

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

## 4. Construction: the message from eight words

The construction places the six constants of 3.2 where Lemma H needs them,
keeps w14 = w15 = 0, and gives the word Y4, the b output of C0, a
prescribed value. Its input is eight free words: the seven words of a
*context*,

    vc, vd, S11, S4, X13, X14, w0,

where vc and vd are the third and the second value of the round-1 call C0,
S11 and S4 are words of the state after the column step of round 0, X13
and X14 are words of the state after round 0 and w0 is a message word; and
one more word y, the value that Y4 is to have. The state words X3, X7, X11,
X15 are the constants, w4 = W4, w13 = W13 and w14 = w15 = 0. Step S1 uses
the seven words of the context only. Step T uses y. In both steps a name
on the right is a context word, a constant or a name assigned on an
earlier line, and all arithmetic is modulo 2^32.

**Step S1 (the context).**

    K0, forwards from w0 and backwards from S4:
        ka = IV[0] + IV[4] + w0;   kd = ROR(ka, 16);   kc = IV[0] + kd
        kb = ROR(IV[4] XOR kc, 12)
        S8 = ROL(S4,7) XOR kb;   S12 = S8 - kc;   S0 = ROL(S12,8) XOR kd
        w1 = S0 - ka - kb
    D2, backwards from its outputs X7, X8, X13:
        X8 = vc - vd;   tc = X8 - X13;   td = tc - S8;   tb = ROL(X7,7) XOR X8
        S7 = ROL(tb,12) XOR tc;   X2 = ROL(X13,8) XOR td
        ta = X2 - tb - W13;   S13 = ROL(td,16) XOR ta
    K3, backwards from its outputs S7, S11:
        mb = ROL(S7,7) XOR S11;   mc = ROL(mb,12) XOR IV[7];   md = mc - IV[3]
        S15 = S11 - mc;   S3 = ROL(S15,8) XOR md;   ma = ROL(md,16) XOR 11
        w6 = ma - IV[3] - IV[7];   w7 = S3 - ma - mb
    K2, its first four values:
        p = K + W4;   q = ROR(p XOR 55, 16);   r = IV[2] + q
        u = ROR(IV[6] XOR r, 12)
    D3 with w14 = w15 = 0, the lines that do not read X14:
        ea = S3 + S4;   eb = X3 - ea;   ec = ROL(eb,12) XOR S4
    D3, the lines that read X14:
        ed = ROL(X14,8) XOR X3;   S9 = ec - ed;   S14 = ROL(ed,16) XOR ea
        X9 = ec + X14;   X4 = ROR(eb XOR X9, 7)
    K2, rest:
        S10 = r + S14;   S6 = ROR(u XOR S10, 7);   S2 = ROL(S14,8) XOR q
        w5 = S2 - p - u
    D2, its first word:
        w12 = ta - S2 - S7
    K1, backwards from its outputs S9, S13:
        nc = S9 - S13;   nd = nc - IV[1];   na = ROL(nd,16)
        nb = ROR(IV[5] XOR nc, 12);   S1 = ROL(S13,8) XOR nd
        S5 = ROR(nb XOR S9, 7);   w2 = na - IV[1] - IV[5];   w3 = S1 - na - nb
    C0, its fourth value:
        vb = ROR(X4 XOR vc, 12)

Step S1 assigns the twelve message words w0..w7, w12 and, as constants,
w4 = W4, w13 = W13, w14 = w15 = 0; the sixteen words S0..S15; and X2, X4,
X8, X9. The lines before "D3, the lines that read X14" do not contain X14,
and all later lines do, directly or through S9, S14, X9 or X4.

**Step T (the four words w8..w11, from y).**

    C0, backwards from its b output y:
        Y8 = ROL(y,7) XOR vb;   Y12 = Y8 - vc;   Y0 = ROL(Y12,8) XOR vd
        va = Y0 - vb - w6;   X0 = va - X4 - w2;   X12 = ROL(vd,16) XOR va
    D0, backwards from its outputs X0, X15:
        fd = ROL(X15,8) XOR X0;   fc = S10 + fd;   X10 = fc + X15
        fb = ROR(S5 XOR fc, 12);   X5 = ROR(fb XOR X10, 7)
        fa = ROL(fd,16) XOR S15;   w8 = fa - S0 - S5;   w9 = X0 - fa - fb
    D1, backwards from its outputs X11, X12:
        gc = X11 - X12;   gb = ROR(S6 XOR gc, 12);   X6 = ROR(gb XOR X11, 7)
        gd = gc - S11;   X1 = ROL(X12,8) XOR gd
        ga = ROL(gd,16) XOR S12;   w10 = ga - S1 - S6;   w11 = X1 - ga - gb

Step T assigns X0, X12, X10, X5, X6, X1 and the four words w8..w11. It
changes no name of step S1.

**Step S2.** w4' = W4' and w5' = w5 + W4 - W4', all modulo 2^32. For the
constants of 3.2 that is w5' = w5 + fffffff8, the same as w5 - 8.

**Step S3.** A is the first 55 bytes of the little-endian encoding of
w0..w15. B is the first 63 bytes of the encoding of the same words with w4, w5
replaced by w4', w5'.

**Lemma S.** For every choice of the seven words of the context, the six
calls K0, K1, K2, K3, D2 and D3 of round 0 with block length 55, with the
words of step S1, are as follows.

- K0 maps (IV[0], IV[4], IV[0], 0) to (S0, S4, S8, S12).
- K1 maps (IV[1], IV[5], IV[1], 0) to (S1, S5, S9, S13).
- K2 maps (IV[2], IV[6], IV[2], 55) to (S2, S6, S10, S14).
- K3 maps (IV[3], IV[7], IV[3], 11) to (S3, S7, S11, S15).
- D2 maps (S2, S7, S8, S13) to (X2, X7, X8, X13).
- D3 maps (S3, S4, S9, S14) to (X3, X4, X9, X14).

Proof. For each call the eight assignments of Section 2 are checked against
the lines of step S1; "holds by the line for N" means that the line of step
S1 that assigns N is that assignment, solved for N.

- K0, words (w0, w1). The first four assignments are the lines for ka, kd
  (its d input is 0), kc and kb. The fifth, ka + kb + w1 = S0, holds by the
  line for w1; the sixth, ROR(kd XOR S0, 8) = S12, by the line for S0; the
  seventh, kc + S12 = S8, by the line for S12; the eighth,
  ROR(kb XOR S8, 7) = S4, by the line for S8. S4 is the context word.
- K3, words (w6, w7). The eighth assignment, ROR(mb XOR S11, 7) = S7, holds
  by the line for mb; the fourth, ROR(IV[7] XOR mc, 12) = mb, by the line
  for mc; the third, IV[3] + md = mc, by the line for md; the seventh,
  mc + S15 = S11, by the line for S15; the sixth, ROR(md XOR S3, 8) = S15,
  by the line for S3; the second, ROR(11 XOR ma, 16) = md, by the line for
  ma; the first, IV[3] + IV[7] + w6 = ma, by the line for w6; the fifth,
  ma + mb + w7 = S3, by the line for w7. S7 comes from the lines of D2,
  S11 is the context word.
- K2, words (W4, w5). The first four assignments are the lines for p, q, r
  and u. The seventh, r + S14 = S10, holds by the line for S10; the eighth,
  ROR(u XOR S10, 7) = S6, by the line for S6; the sixth,
  ROR(q XOR S2, 8) = S14, by the line for S2; the fifth, p + u + w5 = S2,
  by the line for w5. S14 comes from the lines of D3.
- K1, words (w2, w3). The seventh assignment, nc + S13 = S9, holds by the
  line for nc; the third, IV[1] + nd = nc, by the line for nd; the second,
  ROR(0 XOR na, 16) = nd, by the line for na; the first,
  IV[1] + IV[5] + w2 = na, by the line for w2; the fourth is the line for
  nb; the sixth, ROR(nd XOR S1, 8) = S13, holds by the line for S1; the
  eighth is the line for S5; the fifth, na + nb + w3 = S1, holds by the
  line for w3. S9 comes from the lines of D3 and S13 from those of D2.
- D2, words (w12, W13). The seventh assignment, tc + X13 = X8, holds by the
  line for tc; the third, S8 + td = tc, by the line for td; the eighth,
  ROR(tb XOR X8, 7) = X7, by the line for tb; the fourth,
  ROR(S7 XOR tc, 12) = tb, by the line for S7; the sixth,
  ROR(td XOR X2, 8) = X13, by the line for X2; the fifth,
  ta + tb + W13 = X2, by the line for ta; the second,
  ROR(S13 XOR ta, 16) = td, by the line for S13; the first,
  S2 + S7 + w12 = ta, by the line for w12. X7 is the constant, X13 the
  context word, and X8 = vc - vd is a definition.
- D3, words (w14, w15) = (0, 0). The first assignment, S3 + S4 + 0 = ea, is
  the line for ea; the fifth, ea + eb + 0 = X3, holds by the line for eb;
  the fourth, ROR(S4 XOR ec, 12) = eb, by the line for ec; the sixth,
  ROR(ed XOR X3, 8) = X14, by the line for ed; the third, S9 + ed = ec, by
  the line for S9; the second, ROR(S14 XOR ea, 16) = ed, by the line for
  S14; the seventh, ec + X14 = X9, is the line for X9; the eighth is the
  line for X4. X3 is the constant, X14 the context word.

Every name is assigned once, and every line uses only names assigned on
earlier lines: the lines of K0 give S8, which the lines of D2 use; these
give S7 and S13; the lines of K3 use S7 and give S3; the lines of D3 use S3
and give S9, S14 and X4; the rest of K2 uses S14 and gives S2, which the
line for w12 uses; the lines of K1 use S9 and S13. QED.

**Lemma F.** For every context and every word y, with the words of steps S1
and T: D0 maps (S0, S5, S10, S15) to (X0, X5, X10, X15), and D1 maps
(S1, S6, S11, S12) to (X1, X6, X11, X12).

Proof. D0, words (w8, w9): the sixth assignment, ROR(fd XOR X0, 8) = X15,
holds by the line for fd; the third is the line for fc; the seventh is the
line for X10; the fourth is the line for fb; the eighth is the line for X5;
the second, ROR(S15 XOR fa, 16) = fd, holds by the line for fa; the first,
S0 + S5 + w8 = fa, by the line for w8; the fifth, fa + fb + w9 = X0, by the
line for w9. D1, words (w10, w11): the seventh assignment,
gc + X12 = X11, holds by the line for gc; the fourth is the line for gb;
the eighth is the line for X6; the third, S11 + gd = gc, holds by the line
for gd; the sixth, ROR(gd XOR X1, 8) = X12, by the line for X1; the second,
ROR(S12 XOR ga, 16) = gd, by the line for ga; the first,
S1 + S6 + w10 = ga, by the line for w10; the fifth, ga + gb + w11 = X1, by
the line for w11. The inputs S0, S1, S5, S6, S10, S11, S12, S15 are those
of step S1, X15 and X11 are the constants, and X0 and X12 come from the
first lines of step T. QED.

**Lemma Y.** For every context and every word y, C0 with inputs
(X0, X4, X8, X12) and words (w2, w6) has first, second, third and fourth
value va, vd, vc and vb, and outputs (Y0, y, Y8, Y12).

Proof. The first assignment, X0 + X4 + w2 = va, holds by the line for X0;
the second, ROR(X12 XOR va, 16) = vd, by the line for X12; the third,
X8 + vd = vc, by the line X8 = vc - vd of step S1; the fourth is the line
for vb of step S1; the fifth, va + vb + w6 = Y0, holds by the line for va;
the sixth, ROR(vd XOR Y0, 8) = Y12, by the line for Y0; the seventh,
vc + Y12 = Y8, by the line for Y12; the eighth, ROR(vb XOR Y8, 7) = y, by
the line for Y8. QED.

## 5. The half-collision

**Theorem.** For every choice of the seven words of a context and of the
word y, steps S1, T, S2 and S3 output two distinct messages A and B, of 55
and 63 bytes, whose complete 2-round digests agree on digest words 0, 2, 5
and 7; and in both compressions the b output of C0 is Y4 = y.

Proof. The sixteen words of steps S1 and T have w14 = w15 = 0 and
w13 = W13, whose top byte is zero. So bytes 55 to 63 of their encoding are
zero: A, the first 55 bytes, is an honest 55-byte message whose zero-filled
block is the sixteen words, and B is an honest 63-byte message that ends in
eight zero bytes and whose zero-filled block is the sixteen words with w4,
w5 replaced (3.1). Run round 0 on the words of A with block length 55. The
column calls read the initial state, so by Lemma S they leave the state S
of step S1. The diagonal calls then read S: D0 and D1 leave
(X0, X5, X10, X15) and (X1, X6, X11, X12) by Lemma F, D2 and D3 leave
(X2, X7, X8, X13) and (X3, X4, X9, X14) by Lemma S; the four calls act on
disjoint state words. So the state after round 0 has
(X[3], X[7], X[11], X[15]) equal to the four constants, and w4 = W4,
w13 = W13. By Lemma L the compression of B has the same state X after
round 0. The two compressions share every word except w4, w5, so Lemma H
gives the four digest words. C0 reads X0, X4, X8, X12 and w2, w6, which are
the same in both compressions, and has b output y by Lemma Y. The messages
are distinct because their lengths differ. QED.

Distinct choices of the eight words give distinct messages A: vc and vd are
values inside C0, S11 and S4 are state words after the column step, X13
and X14 are state words after round 0, w0 is a message word and y is a
state word after the column step of round 1, and all of them are functions
of the message. The construction yields 2^256 different half-colliding
pairs.

## 6. The search for the other half

**6.1 Trials.** A *context* is seven words (vc, vd, S11, S4, X13, X14, w0)
together with everything that step S1 computes from them. The class
defined next is a set of values of Y4. A **trial** is a context and a
member y of the class; its messages A and B are the output of steps S1, T,
S2 and S3 for the context's seven words and y. Only step T depends on y: the
trials of one context differ in the four message words w8..w11 and in
nothing else of the message.

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

Proof. Put x = ROL(eta,16) = 03cf8303 and m = x AND 7fffffff = 03cf8303. Here x
has no bit 31, so m = x. Y4 is in the class exactly when e1 XOR (e1 + DY3) = x,
that is when (e1 XOR x) - e1 = DY3 modulo 2^32. For words e and x, (e XOR x) -
e is, modulo 2^32, the sum over the bits i of x of 2^i where bit i of e is 0
and of -2^i where it is 1, which is 2 ((NOT e) AND x) - x; for i = 31 the two
signs give the same word. So the condition is 2 ((NOT e1) AND x) = DY3 + x
modulo 2^32. Here DY3 + x = 01870000 modulo 2^32, which is even. Doubling
modulo 2^32 discards bit 31 of (NOT e1) AND x, so the condition does not
involve bit 31 of e1, and on the other bits it is ((NOT e1) AND m) = 01870000
>> 1 = 00c38000. All bits of 00c38000 lie in m, so this fixes the 13 bits of e1
on m to (e1 AND m) = (NOT 00c38000) AND m = 030c0303 and leaves the other 19
bits free. QED.

Member number k of the class, for 0 <= k < 524288, is the Y4 whose e1 has the
bits of k at its 19 free positions, in increasing order of position.

**Lemma T.** For every context and every member y of the class, the messages A
and B of the trial are distinct messages of 55 and 63 bytes whose complete
2-round digests agree on digest words 0, 2, 5 and 7; in both compressions Y4 =
y; and the XOR difference between A and B of E3's first-half d value is eta =
830303cf.

Proof. The first two statements are the theorem of Section 5. In both
compressions w15 = 0 and Y14 is the same, the a input of E3 is Y3 for A and
Y3' for B by Fact P, and Y4 = y is a member of the class, so the difference
is eta by the definition of the class. QED.

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
and Y12 are known from step T without evaluating C0 forwards. Write a1, d1,
c1, b1, a2, .. for the assignments of E1 and e1, h1, g1, f1, e2, h2, g2, f2
for those of E3 in the order a, d, c, b; a prime marks message B.

**6.3 Three tests of a trial.** The algorithm uses two tests: rule A, a
condition on one word of E3 (Lemma A), and the E1 test, a 32-bit condition
on E1 alone (Lemma N). A third test, the early test of Lemma E, was the test
of the first submissions named in Section 10. The algorithm of this package
does not use it. It is kept because the measurements of Section 10 report
its passes.

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
h2 = ROR(h1 XOR e2, 8), and h1 XOR h1' = eta for every Y4 in the class
(Lemma T), so h2 XOR h2' = ROR(eta XOR e2 XOR e2', 8). Rotating D6 left by 8
gives ROL(D6, 8) = ROL(beta XOR eps, 1) XOR eta XOR (e2 XOR e2'). The XOR
with D3 cancels e2 XOR e2' and leaves n. QED.

A trial *passes the E1 test* when n = 0. The word n needs the first seven
assignments of E1 for both messages and nothing of E3: for a trial of 6.1
the eta of E3 is the constant of the class.

*Rule A.* Let h1 be the second value of E3 on message A, as in 6.2. A trial
*satisfies rule A* when all of the following hold:

    bit 0 of h1 is 0;
    bit 16 of h1 is 0;
    bit 17 of h1 is 0;
    bit 1 of h1 is 1;
    bits 2 and 3 of h1 differ.

These are five conditions, each on one bit or on the XOR of two bits, so a
uniform word satisfies rule A with probability 2^-5.

**Lemma A.** (a) For a trial of 6.1 let z = a2 XOR d1 be the XOR of the
fifth and the second value of C2, and e1 = Y3 + Y4. Then
ROL(h1, 24) = z XOR ROL(e1, 8): bit i of h1 is bit (i + 24) mod 32 of z XOR
bit (i + 16) mod 32 of e1. (b) For every Y4 in the class, the trial
satisfies rule A exactly when

    bit 24 of z is 0;
    bit 25 of z is 1;
    bit 8 of z is 1;
    bit 9 of z is 1;
    bits 26 and 27 of z differ.

(c) Put S = 04000000, ALL = 07000300 and V = 06000300. The word

    ((z XOR ((z >> 1) AND S)) AND ALL) XOR V

is zero exactly when the trial satisfies rule A.

Proof. (a) The sixth assignment of C2 is Y14 = ROR(d1 XOR a2, 8) = ROR(z, 8),
and the second assignment of E3 is h1 = ROR(Y14 XOR e1, 16). So h1 = ROR(z, 24)
XOR ROR(e1, 16), and rotating left by 24 gives the claim. (b) Rule A reads the
bits 0, 1, 2, 3, 16 and 17 of h1. By (a) each of them is a bit of z XOR a bit
of e1, and the bits of e1 that enter are bits 0, 1, 16, 17, 18 and 19. All of
these lie in the mask 03cf8303 of Lemma Q, so they have the same value for
every member of the class: in 030c0303, bit 0 is 1, bit 1 is 1, bit 16 is 0,
bit 17 is 0, bit 18 is 1 and bit 19 is 1. Inserting these values into the five
conditions gives the conditions on z. (c) Bit p of z XOR ((z >> 1) AND S) is
the XOR of bits p and p + 1 of z at the positions p of S and bit p of z
elsewhere. S holds the lower position of the one condition on two bits, ALL
holds it and the positions of the four conditions on one bit, and V holds the
required values. QED.

*What Lemma A does not say.* Lemma A says that the word of (c) tests rule A
exactly. It does not say that a collision satisfies rule A, and that is not
true: there are solutions of R = 0 with Y4 in the class whose h1 violates
rule A, and Section 10 prints one. Rule A is therefore a filter that loses
solutions. A batch in which no trial satisfies it is dropped, whether or
not one of its trials has a zero residual; a trial that fails rule A is
examined further only if another trial of its batch satisfies it (6.4).
How much is lost is a question about the count of Section 10 and is
answered there: the figure that H1 is set against leaves out, in full, every
outcome of the count for which a solver found a solution that violates
rule A. For the other outcomes three SAT solvers answered that no such
solution exists, and an exact count of the E3 side finds none; Section 10
says how these answers were checked and by whom.

**6.4 Algorithm.**

1. Draw one fresh uniform 256-bit word and take from it the four words S11, S4,
   X13 and w0.
2. For each of the 2^51 values of (vc, vd) with vd < 2^19, in a fixed order:
   run the lines of step S1 that do not read X14, and store what the later
   steps need. For each of the 2^32 values of X14, in increasing order: run the
   lines of step S1 that read X14 and form the constants of 6.5 that depend on
   X14. Then run the batches of 6.5 for the 524,288 members of the class in the
   order of their numbers, seven members in one packed word. Every batch runs
   stage A, which tests rule A for its seven trials. If none of them satisfies
   rule A the batch ends and its trials are dropped. Otherwise the batch runs
   stage 2, which evaluates the E1 test for its seven trials.
3. For every trial of a batch that ran stage 2 whose E1 test word is zero,
   compute its words by step T and R in full. If R = 0, build A and B by steps
   S2 and S3 from the trial's words, evaluate H(A) and H(B), check that they
   agree, output (A, B) and halt.
4. Halt with failure if 2^86 trials have been processed in step 3 without R =
   0; or if 74,899 * 2^81 batches have run stage 2, which is one quarter of the
   74,899 * 2^83 batches of a run; or when all trials are exhausted.

A trial with R = 0 that satisfies rule A is found: its batch runs stage 2,
its E1 test word is zero by Lemma N, and step 3 computes its residual,
unless one of the two budgets of step 4 has ended the run before. A trial
with R = 0 that violates rule A is found only if another trial of its batch
satisfies rule A; Section 7 does not count such trials.

The pairs (vc, vd) are 2^32 * 2^19 = 2^51, and the trials are 2^51 * 2^32 *
2^19 = 2^102 half-colliding pairs by Lemma T. They are distinct by the remark
after the theorem of Section 5: two trials differ in vc, in vd, in X14 or in
Y4, and each of these is a function of the message A.

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

*What a batch computes.* The seven trials of a batch share a context and are
seven consecutive members of the class. The members enter through one list that
does not depend on the context: for batch j, U[j] holds ROL(y,7), one member y
per lane. The list has 74,899 packed words, because 524288 = 74,898 * 7 + 2;
the five spare lanes of the last word repeat its last member. The list is
computed once, before step 2. A batch has two stages. Stage A computes in every
lane, in the names of step T and of 6.2 to 6.3:

- C0 backwards: Y8 = U[j] XOR vb, Y12 = Y8 - vc, Y0 = ROL(Y12,8) XOR vd,
  va = Y0 + (-vb - w6), and the complement of X12 as
  va XOR NOT ROL(vd,16).
- D0 and D1, as far as C2 needs them: fd = (va + (-X4 - w2)) XOR ROL(X15,8),
  which is ROL(X15,8) XOR X0; X10 = fd + (S10 + X15); gc = X11 - X12, formed
  as (NOT X12) + (X11 + 1); gb and X6.
- C2 to z: its first value X6 + (X2 + w7), its second, third and fourth
  value, the fifth as the first plus the fourth plus w0, and z, the XOR of
  the fifth and the second.
- Rule A: the word of Lemma A (c), and whether it is zero in some lane.

If that word is zero in no lane, the batch ends. Otherwise stage 2 computes:

- The entry count: the number of batches that have run stage 2 is advanced
  and compared with its budget (step 4).
- C2, rest: Y14 = ROR(z, 8) and Y6, its sixth and eighth values.
- D0 and D1, rest: fb from X10 + (-X15) and S5, and X5; gd = gc + (-S11);
  X1 = ROL(X12,8) XOR gd, formed from the complement of X12 and one more
  XOR with M; and ga = ROL(gd,16) XOR S12.
- C1 to Y1: its first value X1 + X5 + w3, its second, third and fourth
  value, and its fifth, Y1, as the sum of the first, the fourth, ga and
  the constant -S1 - S6, since w10 = ga - S1 - S6.
- E1 on A and B: a1, d1, c1, c1', b1, b1', a2, a2', c2, c2'.
- The E1 test: eps = c2 XOR c2', beta XOR eps, the word n of Lemma N, and
  whether n is zero in some lane.

Nothing of E3 is evaluated in a batch. Rule A is a condition on h1, a value
of E3, but by Lemma A it is tested on z, a value of C2, with the bits of e1
that it needs folded into the constant V. The words w8..w11 are never
formed in a batch: w10 enters Y1 through ga, and step 3 computes all four
for the trials it processes.

*No lane overflows.* Put B = 2^32. Rotation outputs, list entries and
constants are below B. An XOR with a value below B changes only the low 32
bits of a lane, so it keeps a bound that is a multiple of B. In C0
backwards the sums are Y12 and va, below 2B. In the part D0 and D1 they
are va + (-X4 - w2), below 3B; X10, a value below 3B plus a constant, below
4B; and gc, below 3B. In C2 the first value is below 2B, the third,
X10 plus a rotation output, below 5B, and the fifth below 4B. In the rest
of C2 the sum for Y6 is the third value plus Y14, below 6B. In the rest of
D0 and D1 the sums are X10 + (-X15), below 5B, and gd, below 4B; X1 is
below 4B. In C1 the first value is below 6B, the third below 2B, and Y1, a
value below 6B plus three values below B, below 9B. In E1 a1 is below 11B,
c1 and c1' are below 2B, the two a2 are below 13B and c2 and c2' are below
3B. The sums that form the flags of the two tests are below 2B. Every sum
is therefore below 13B, which is below 2^36 = 16B, so no carry leaves a
lane, the low 32 bits of every lane equal the scalar value modulo 2^32,
and XOR and PROR read only those bits. In the word of Lemma A (c) every
shifted bit that is kept comes from the low 32 bits of the same lane,
because a condition joins two bits p < q <= 31 of z and is kept at
position p; the AND with ALL discards the guard bits of z, and the word is
below B. The word n is reduced by an AND with M.

*Operation count of one batch.* The batch runs on a load/store machine with
16 registers. The second column counts additions, XOR, AND, OR, shifts, the
comparisons and the branches, with PROR = 5. The third column counts memory
traffic: every constant operand, that is a constant of the context, a list
entry, a rotation mask, the mask M, a constant of rule A or a budget, is
fetched from memory each time it is used and charged as one load. Shift
distances are fixed in the instruction.

| Part | What is computed | Operations | Loads |
| --- | --- | ---: | ---: |
| loop | next list position, end test, branch | 3 | 1 |
| C0 backwards | Y8 (1), Y12 (1), Y0 (6), va (1), NOT X12 (1) | 10 | 8 |
| D0 and D1 | fd (2), X10 (1), gc (1), gb (6), X6 (6) | 16 | 10 |
| C2 to z | first (1), d1 (6), c1 (1), b1 (6), z (3) | 17 | 7 |
| rule A | word (5), flags and branch (4) | 9 | 6 |
| | stage A, every batch | 55 | 32 |
| entry count | next count, budget test, branch | 3 | 1 |
| C2, rest | Y14 (5), Y6 (7) | 12 | 4 |
| D0 and D1, rest | fb (7), X5 (6), gd (1), X1 (7), ga (6) | 27 | 13 |
| C1 to Y1 | first (2), d1 (6), c1 (1), b1 (6), Y1 (3) | 18 | 8 |
| E1, A and B | a1 d1 (8), c1 c1' b1 b1' (14), a2 a2' c2 c2' (18) | 40 | 15 |
| E1 test | eps, beta XOR eps (3), n (8), flags and branch (4) | 15 | 7 |
| | stage 2, only after a pass of stage A | 115 | 48 |

So stage A is 55 + 32 = 87 primitive operations and stage 2 is 115 + 48 = 163.
No store is needed: the list position and the entry count stay in two registers
across batches, and the batch values that are live at any point fit in the
other 14; the self-test below reports the number in use.

Each XOR followed by a rotation is 6 operations, a two-term sum 1 and a
three-term sum 2; a rotation loads its two masks. The loads of C0 backwards are
U[j], vb, -vc, vd, -vb - w6, NOT ROL(vd,16) and one mask pair. The loads of the
part D0 and D1 are -X4 - w2, ROL(X15,8), S10 + X15, X11 + 1, S6, X11 and two
mask pairs. In C2 the loads are X2 + w7, X14, w0 and two mask pairs; its third
value adds two registers. The loop advances the list position, compares it with
the end of the list, which is loaded, and branches. In the rule A part the word
of Lemma A (c) is a shift, an AND with S and an XOR for the one distance (3
operations, 1 load), then an AND with ALL and an XOR with V (2 operations, 2
loads). The flags are formed by adding 2^32 - 1 to every lane and selecting bit
32 of every lane, which is set exactly in the lanes whose word is nonzero (2
operations, 2 loads); the flags are compared with a loaded constant and stage A
ends with a branch (2 operations, 1 load). The entry count is one addition, a
comparison with the loaded budget and a branch. In the rest of C2, Y14 is a
rotation of z (5) and Y6 a sum, an XOR and a rotation (7). In the rest of D0
and D1, fb is a sum, an XOR and a rotation (7, with loads for -X15, S5 and one
mask pair), X5 an XOR and a rotation (6), gd one addition of -S11, X1 a
rotation and two XORs (7, with loads for one mask pair and M) and ga a rotation
and an XOR with S12 (6). In C1 the loads are w3, X13, X9, -S1 - S6 and two mask
pairs. In E1, each of c2 and c2' is an XOR, a rotation and a sum (7); its loads
are w12, Y11, Y11', w5, w5 + delta and five mask pairs. In the E1 test, eps is
one XOR, beta XOR eps two, and n a rotation by one, two XORs and the AND with M
(8, with loads for one mask pair, eta and M); the flags, the comparison and the
branch are as in stage A.

The constants of a batch that change with X14 are thirteen: vb, -vb - w6,
-X4 - w2, S10 + X15, S6, X14, S5, w3, X9, -S1 - S6, w12, w5 and
w5 + delta. Those that change only with the other six words of the context
are eight: -vc, vd, NOT ROL(vd,16), X2 + w7, w0, -S11, S12 and X13. The
constants of rule A depend on the class only, and ROL(X15,8), X11 + 1,
X11, -X15, Y11, Y11', eta, M and the masks are fixed.

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

runs N batches. The seven context words and the list position of a case
come from SHAKE-256 of the seed text (default 1) and the case number.
Every fourth case is the last batch of the class, and in every fifth case
each context word is 0, 2^32 - 1 or as drawn. Every lane is
checked against the real messages of its trial. The program builds the
messages A and B of the trial by steps S1, T, S2 and S3 and compresses each
in full, with a 2-round compression written out from Section 1 and with no
shortcut of the batch. From these two compressions it takes Y4 of A; h1,
the second value of E3 on A; the word n of Lemma N, from E1 evaluated for A
and for B on their own states and words; and the two digests. A lane is
right when the sixteen words of the 55 bytes of A are the words of the
trial, Y4 is the member of the lane, the digests agree on digest words
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
use at one time, the number of constants per context and per value of X14,
the number of class members in the list, for how many patterns of zero and
nonzero lanes the flags are right, and for how many packed words built from
all patterns of the bits of z that rule A reads the stage-A flags are
right. Its exit status is 0 only if all of these agree with this section.

With N = 2,000 and seed 1 it reports 14,000 of 14,000 lanes right; 55
operations and 32 loads in stage A and 115 and 48 in stage 2, per part as in
the table and the same in every case; largest sums of 1.967, 3.942, 4.777,
1.027, 5.750, 4.689, 7.994, 10.777 and 1.999 times 2^32 in C0 backwards, D0 and
D1, C2 to z, rule A, the rest of C2, the rest of D0 and D1, C1, E1 and the E1
test, below the bounds 2, 4, 5, 2, 6, 5, 9, 13 and 2; 8 constants per context
and 13 per value of X14; 524,288 members in the 74,899 words of the list; and
at most 12 registers in use. The register figure follows every value, loaded
constants and the intermediate values of a rotation included, from the step
that makes it to its last use, with the operations in the order of the program,
and adds two registers for the list position and the entry count. In that run
456 lanes satisfy rule A, in 205 batches. None of the 14,000 words n of that
run is zero, so the flags are also formed for all 128 patterns of zero and
nonzero lanes: all 128 are right. Rule A reads six bits of z; the program forms
64 packed words in which every pattern of these bits occurs once in every lane,
with different other bits, filled guard bits and another member of the class in
every lane, and compares the stage-A flags with rule A as written on h1 =
ROR(ROR(z, 8) XOR e1, 16): all 64 are right, and a lane satisfies rule A in 14
of them.

A longer run of the same self-test, 1,000,000 batches with seed 61, reports
7,000,000 of 7,000,000 lanes right, the same counts in every case, at most 12
registers and a largest sum of 11.592 * 2^32; 218,402 of its lanes satisfy rule
A, a share of 2^-5.002, in 102,072 batches. Its contexts are random or extreme
by design and are not laid out as a run of 6.4. A separate participant tool
derives the bounds of the sums for all inputs by interval arithmetic on a
second machine and finds every one below the bound of its part.

In the declared experiment `residual-search` the same program evaluates one
batch per organizer seed, for that seed's context and the list position
that holds the first member tried, and returns the operations and loads of
its two stages, its number of right lanes and whether a lane satisfied
rule A as observations. The organizer's runner records observations as
untrusted and does not recompute them. The self-test and these
observations therefore show what the program in the package counts, and
that its lanes agree with the program's own compression of the real
messages. They are a participant check, not an organizer verification of
the cost.

## 7. Success probability

The probability space is the one uniform 256-bit word of step 1, for the
fixed target. The algorithm is otherwise deterministic. The trials depend on
that word only through the four words S11, S4, X13 and w0.

Call a trial *good* when R = 0 and the trial satisfies rule A. By 6.4 a
good trial is found unless a budget of step 4 ends the run before.

**Heuristic H1 (score-critical).** Over the coins, the 2^102 trials behave with
respect to the event "good" like independent events of probability at least
2^-103 each, to the extent that the probability that no trial is good is at
most exp(-1/2) + 0.002. The rate 2^-103 is 2^25 = 33,554,432 times the rate of
a uniform 128-bit value. The factor is assumed. Section 10 describes what it is
set against: for Y4 in the class and under the seven-word model, a count
without sampling of the solutions of R = 0, from which every outcome for which
a solver found a solution that violates rule A is left out, and which gives the
lower bound 126,003,600 if the solvers' answers for the other outcomes are
right; a participant computation. The organizer-run experiments do not measure
the factor.

**Heuristic H2 (supporting).** With probability at least 0.9995 over the coins,
fewer than 2^86 of the 2^102 trials pass the E1 test of Lemma N without having
R = 0. (The budget corresponds to a pass rate of 2^-16. The pass rate measured
on real trials with these constants is 2^-31.39, which would give 2^70.6
passes, below the budget by a factor of 2^15.3. Step 3 processes only the
passes that lie in batches that ran stage 2, which are fewer. That the number
of passes of one run stays near this mean is part of the assumption.)

**Heuristic H3 (supporting).** With probability at least 0.9995 over the coins,
fewer than 74,899 * 2^81 of the 2^102 trials satisfy rule A. (A batch runs
stage 2 only if one of its trials satisfies rule A, and every trial lies in one
batch, so the number of batches that run stage 2 is at most the number of
trials that satisfy rule A. The budget is a share 2^-4.81 of the trials, 1.142
times 2^-5. A uniform h1 satisfies rule A with probability 2^-5. What step 4
budgets is batches, and the statement on trials is a sufficient condition for
it. It leaves less room than the batches themselves do: a factor of 1.142 on
the average share of the trials, where the measured share of the batches that
hold a trial satisfying rule A is 0.1216 for random contexts and 0.1133 for
contexts laid out in the ranges of the algorithm, and at most 0.1684 for any
single context among the 13,312 of the samples of Section 10, against the
budget of 0.25. H3 is a statement about the average over the 2^83 contexts of a
run. In its form on trials it is not true context by context: the largest share
of the trials of one context seen in the samples of Section 10 is 1.46 times
2^-5, and such a context exceeds the budget on its own trials, though not on
its own batches. What was measured is that the average over contexts is 2^-5 to
within the errors stated there. That the average over the contexts of one run
stays that close to this mean is the assumption.)

Under H1, H2 and H3 the algorithm outputs a collision with probability at
least 1 - exp(-1/2) - 0.002 - 0.0005 - 0.0005 > 0.3934 - 0.003 = 0.3904 >=
0.39. When it outputs a pair, the pair is a genuine collision: step 3
checks both complete digests, and the messages have different lengths.

*Sensitivity to the factor.* If the rate of good trials is f * 2^-128, the
2^102 trials give 1 - exp(-f/2^26) - 0.003 with the same allowances, which
reaches 0.39 only for f >= 33,502,523: the assumed 33,554,432 leaves no slack
on the probability side. The margin of the claim lies between the assumed
33,554,432 and the counted 126,003,600, a factor of 3.75. For an f between 1
and 2^25 the same success probability needs 2^127 / f trials and, at the same
19.1 operations per trial, the total of Section 8 is below 2^(122.52 - log2 f):
below 2^97.52 at f = 2^25, and below 2^122.52 at f = 1, the uniform rate, where
19.1 * 2^127 / 430 = 2^122.50731 and the package would submit 122.6. With the
more cautious f = 2^24 = 16,777,216, which is 7.5 times below the count, the
same package would search 2^103 trials, twice as many pairs (vc, vd), and would
submit 98.6.

*Remark on clustering.* H1 asks for more than a rate: it asks that the good
trials do not come in clusters. Under M the count of Section 10 gives
126,003,600 * 2^102 / 2^128 = 1.87 expected good trials in a run, or more,
where H1 needs 0.5. Suppose that these trials came in clusters of m on average
and that the clusters fell independently. Then a run would contain one with
probability about 1 - exp(-1.87 / m), and the bound 0.39 would hold for m up to
3.76. So if the counted rate is right, the bound survives a clustering of the
successes by that factor. This is a remark and not a proof: the counted rate
rests on M, and nothing here bounds m. The dependence of rule A on the context,
stated under H3, is a clustering of one of the two conditions of "good" by
context, of the size measured in Section 10.

None of the three heuristics is proved. Section 10 lists the evidence.

## 8. Charged time

One 2-round target compression costs one unit and every other primitive word
operation costs 1/C units with C = 430.

- **Main loop.** For one context the 524,288 members take 74,899 batches:
  74,898 full ones and one that holds the last two members and is charged in
  full. A run has 2^83 contexts, that is pairs of a pair (vc, vd) and a value
  of X14, and so 74,899 * 2^83 batches. Every batch runs stage A, 87 primitive
  operations by 6.5, memory loads included. By step 4 at most one quarter of
  the batches, 74,899 * 2^81, run stage 2, 163 operations each. The work per
  value of X14 before its batches is the next value of X14 and its end test,
  the lines of step S1 that read X14 and the thirteen constants of 6.5 that
  change with X14, each placed in seven lanes and stored. Written out on the
  machine of the submitted program by a participant tool, it is 91 operations,
  59 loads and 13 stores, 163 in all; it is charged as 1,024. On every run the
  main loop therefore costs at most 2^83 times 74,899 * 87 + 74,899 * 163 / 4 +
  1,024 = 9,569,371.25 operations, which is less than 18.253 per trial. It is
  charged 2^83 times 19.1 * 524288 = 10,013,900.8, that is 19.1 per trial; the
  difference, 4.6% of the bound, is margin. The main loop is charged 2^102 *
  19.1 operations. This is the budgeted cost, a bound for every run. The
  expected cost is lower: if the average share of the trials that satisfy rule
  A is 2^-5, at most 7 * 2^-5 = 0.21875 of the batches run stage 2 on average,
  and a trial costs at most 17.525 operations on average.
- **Per pair (vc, vd).** The lines of step S1 that do not read X14 are 31
  assignments, each below 16 operations, its loads and its store included.
  Storing the nine words that the lines of X14 read, placing the eight
  constants of 6.5 that do not change with X14 in seven lanes and storing them,
  and the step to the next pair with its end test and branch are below 200
  operations more. Together they are below 2^11 operations; this is a bound and
  was not written out on the machine. There are 2^51 pairs: 2^62 operations.
- **List.** The list of 6.5 is computed once from eta and Y3: 524,288 members
  at fewer than 64 operations each, 2^25 operations. The constants of rule A
  are stored.
- **Passes of the E1 test.** At most 2^86 are processed (step 4). The batch
  keeps no values of a passing trial, so the trial is recomputed in scalar form
  from its member number: its words by step T, the calls C1 and C2, E1 and E3
  for both messages, and the comparison of R. That is below 2^10 operations
  each, loads and the count of the processed trials included: 2^96 operations,
  a share below 2^-10.25 of the main loop.
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
  Fact P and a zero top byte of w13 with at most 2^64 candidates at two G
  evaluations and a comparison each, below 128 operations: 2^71 operations,
  below 2^63 units.

Total:

    T <= (19.1 * 2^102 + 2^96 + 2^62 + 2^60 + 2^25 + 2^11 + 1) / 430
         + 2 + 2^63
       <  19.1 * 2^102 * (1 + 2^-7) / 430 + 2^64
       <  2^97.5186 + 2^64
       <  2^97.52.

Here 19.1 * 2^102 / 430 = 2^(102 + 4.255501 - 8.748193) = 2^97.50731. The terms
after the first add up to less than 2^96.01, which is below 19.1 * 2^102 * 2^-7
= 2^99.255, and log2(1 + 2^-7) < 0.01123. The submitted bound is time_log2 =
97.6, a factor of about 1.06 above this total. This is a worst-case bound for
the algorithm as stated, which halts within its two budgets on every run.

No sorting or lookup is charged because the algorithm has none: a trial is
tested against zero, not against other trials. The only stored list is the
fixed list of class members of 6.5, which is read in order; its loads are among
the 32 of stage A.

## 9. Memory, preprocessing and advice

The program is the lines of steps S1 and T, the packed batch of 6.5 and a
compression routine for the final check. Bound the code by 4096 instruction
templates of at most four 256-bit words each: 2^14 words, which is 2^19 bytes.
Data is the context (below 64 words), the constants of a batch in packed form
(below 64 words), the masks and the fixed constants (below 32 words), the list
of class members (74,899 words), the batch temporaries (below 64 words) and the
two messages and digests of the final check: fewer than 75,776 words, that is
2,424,832 bytes. The memory of the search is therefore below 2^19 + 2,424,832 <
2^22 bytes. Nothing grows with the number of trials.

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
bytes of the six constants and eta and the 12 bytes of the three constants of
rule A (Lemma A), 40 bytes in all. The list of 6.5 is not advice: the program
computes it from eta and Y3 by Lemma Q. There is no other stored data and no
stored collision.

## 10. Evidence, scope and field meanings

**What is exact.** Sections 2 to 5 and Lemmas Q, T, E, N and A. Lemma A
says what stage A tests, not that a collision passes it. The declared
experiment `half-collision` runs one trial of 6.1 per organizer seed, with
the seven words of a context and a member number taken from the seed, and
the organizer recomputes both digests; Lemma T predicts that every trial
agrees on the 128 masked digest bits.

*What is new in the exact part and who has checked it.* The length pair, step
S1, step T and Lemmas S, F and Y are new against the submissions named below;
Lemmas L, H, Q, E, N and A are those of the earlier text with the new
constants, and Lemma A is restated for a rule with a condition that joins two
bits of z (in this rule two neighbouring bits; the submitted program handles
any distance). The proofs of Lemmas S, F and Y are written out assignment by
assignment in Section 4. These proofs were written by one helper agent of the
participant, an instance of the same AI model. Two further helper agents, whose
task was to review this text, checked them. One read the two steps line by line
against the eight assignments of each call and tested them with an
implementation of its own, typed from this text: on 120,000 trials, hashed with
the organizer's reference hash, each of the nine calls of Lemmas S, F and Y has
the inputs, the words and the eight values that the lemmas state. The other
read the proofs of the three lemmas and tested the construction from this text
on 1,200 real trials in the same way. Neither reported an error in the lemmas
or their proofs. No person has read them. Machine checks of the same statements
are reported under "Checks of the construction on real messages" below; they
are checks on random inputs, not proofs.

**The seven-word model.** By 6.2 the residual of a trial is a function of the
constants and of seven 32-bit words: for E1 its first-half values d1 and b1 and
its a output a2 on message A, and for E3 the words Y4, Y9, w8 and its
first-half value h1 on message A. (E1's a1 and d1 are the same for A and B, so
a1 enters only through d1 and a2; each of the seven words is a bijective image
of one input or message word of its call when the others are fixed.) In the
algorithm Y4 takes every member of the class equally often. The model M says
that over the trials the other six words behave like independent uniform words,
independent of Y4. Under M a trial has R = 0 with probability r * 2^-128, where
r * 2^83 is the number of solutions of R = 0 among the 2^211 values of the
seven words with Y4 in the class. Call r the *class rate*. Rule A is a
condition on h1, one of the seven words, so under M the trials with R = 0 that
satisfy rule A have a rate of the same kind, r_A, which counts only the
solutions that satisfy rule A; r_A is at most r. H1 is M together with r_A >=
33,554,432.

Given M, the class rate is a property of the constants and the class alone:
the number of solutions of a system of equations in seven words. It can be
counted without sampling, and this section describes the count. The count
says nothing about whether M holds. In a trial the six words are not free:
within one context each of them is a function of Y4. M is therefore a
statement about averages over the contexts of a run, and the measurements
below show one place where it fails inside a single context.

**How r is counted (participant computation, not organizer-verified).** Write
tau, eps for the XOR differences between A and B of E1's a and c outputs and
beta for that of its first-half b. As in the proof of Lemma E, E1's d and b
output differences are ROR(tau, 8) and ROR(beta XOR eps, 7), and E3's d and b
output differences are ROR(eta XOR eps', 8) and ROR(psi XOR tau', 7), where
eta, psi are the XOR differences of E3's first-half d and b and tau', eps'
those of its c and a outputs. So R = 0 holds exactly when tau' = tau, eps' =
eps, psi = tau XOR ROR(tau, 1) and eta = eps XOR ROL(beta XOR eps, 1). For Y4
in the class the left side of the last equation is the constant 830303cf.

1. *The betas.* beta is a function of d1 alone: with c1 = Y11 + d1 and DY11 =
   Y11' - Y11 = 0a08818b, beta = ROR(c1 XOR (c1 + DY11), 12). As in Lemma Q,
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
5. *The sum.* The class-rate part of a beta is 2^(13 - k) times the sum over
   its outcomes of P1 * N3. Here 13 is the number of bits that Lemma Q fixes,
   so that the class is a share 2^-13 of all Y4. r is the sum of the parts over
   all betas: the sum of N3 over all 2^96 values of (d1, b1, a2) is r * 2^83,
   and 2^96 / 2^83 = 2^13. Parts are not negative, so the sum over any set of
   betas is a lower bound for r.

Steps 1 to 5 use no random number unless one of the two fallbacks of steps
3 and 4 is taken. The arithmetic is double-precision floating point: sums
and products of integers, with a relative rounding error of 2^-53 per
operation once a value exceeds 2^53.

**The count for this package.** For these constants 133,742 words occur as
beta. The 4,550 betas with k at most 14 were given to the calculator: for 2,949
of them beta XOR ROR(eta, 1) has odd weight, so that no eps exists; the other
1,601 were enumerated completely, without a limit on the weight of tau, and
fifteen of them have a nonzero part. These parts add up to 162,263,084.4866,
from 183 outcomes with a nonzero product; no outcome of these betas went
through either fallback, so this figure is a count. The 129,192 betas with k of
15 or more were treated in two ways. A SAT solver (kissat) was asked, for every
beta, whether the whole system (E1 and E3 for both messages, a zero residual,
Y4 in the class, this beta) has a solution: it answered that it has none for
129,147 of them and returned a solution for 45, and every returned solution has
a zero residual in plain arithmetic. The calculator, with a pruned search over
tau that gives the same outcomes on the betas where both were run, finished
27,041 of these betas before it was stopped, among them all 45 that the solver
found satisfiable; these 45 have parts that add up to 3,679.1713. In seven of
them, outcomes went through the random-subset branch of step 3; their parts,
0.282 together, are estimates. In all the count is 162,266,763.6579, from 60
betas and 453 outcomes; without the seven betas that hold estimates it is
162,266,763.3758, from 53 betas and 392 outcomes. It is about 2^27.27, so that
under M a trial has R = 0 with probability about 2^-100.73. That every beta is
covered rests on the solver's answers for the betas with k of 15 or more, which
are answers without a proof certificate, and on the recount reported below.

| beta | k | Outcomes | Exact part | Sampler | Error | Deviation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 18b0e098 | 11 | 14 | 71,698,432.0 | 77,225,148 | 13,619,663 | +0.41 |
| 18d0e098 | 11 | 19 | 54,005,760.0 | 47,906,293 | 8,273,827 | -0.74 |
| 18b1a098 | 11 | 16 | 25,692,160.0 | 26,624,000 | 2,432,080 | +0.38 |
| 18d1a098 | 11 | 18 | 8,429,568.0 | 7,301,120 | 1,284,239 | -0.88 |
| 18b3e098 | 13 | 8 | 1,566,720.0 | | | |
| 18d3e098 | 13 | 10 | 838,656.0 | | | |
| 18d1a398 | 13 | 6 | 11,152.0 | | | |
| 19f1a098 | 13 | 10 | 8,640.0 | | | |
| 18d16398 | 13 | 6 | 6,664.0 | | | |
| 18f1e098 | 13 | 12 | 3,632.5 | | | |
| 19f0e098 | 13 | 7 | 1,357.25 | | | |
| 19b1e098 | 13 | 28 | 314.1248 | | | |
| 19d1e098 | 13 | 10 | 15.8071 | | | |
| 19b0a098 | 11 | 16 | 12.6172 | | | |
| 19d0a098 | 11 | 3 | 0.1875 | | | |
| 45 betas, k >= 15 | | 270 | 3,679.1713 | | | |
| sum | | 453 | 162,266,763.6579 | | | |

In the table, k is the number of bits that beta fixes in c1, "outcomes" is the
number of outcomes (tau, eps) with P1 * N3 > 0, and "exact part" is the
class-rate part of the beta. The heaviest beta, 18b0e098, carries 44% of the
count, the two heaviest together 77% and the four heaviest 98%. The last three
columns come from the sampler of the first submissions, which is used here as a
check and not for the figure: for one beta it draws d1 among the values with
that beta and b1, a2 uniformly, and counts E3 for each draw with the count of
step 3. Four betas were given 16 runs each, with the same seeds for every beta.
"Sampler" is the mean of the runs, "error" the standard deviation of the runs
divided by the square root of their number, and "deviation" the difference from
the exact part in units of that error. For the four betas together the sums of
the 16 seeds have mean 159,056,562 with standard error 16,128,603, against
159,825,920 counted (-0.05 standard errors). This is a weak check: the quantity
is heavy-tailed, and the sums of single seeds range from 68,322,367 to
280,776,148. The sampler shares the E3 count with the calculator.

**An independent recount (another AI model, checked here).** After the count
was finished, another AI model, GPT Sol 6.1 (OpenAI), was given the definition
of the seven-word system, the constants and the class, and was asked to count
the class rate with a method and a program of its own; by its own account it
did not read or use the participant's counting programs. The recount was not
blind: the request also stated the participant's total, the parts of the four
heaviest betas and the number of betas with a part, as figures to be confirmed
or refuted, and it offered a hint at the method (fix beta, enumerate the
differences that are possible, carry conditions of single additions). The parts
of the other 56 betas and the two factors of every outcome were not given to
it. Its program is integer arithmetic throughout: it visits every word that can
occur as beta (133,742 of them, 66,871 with an eps), and for every outcome it
counts both sides with carry automata of its own design. Its result is r =
85074516985129 / 524288 = 162,266,763.6588, from 60 betas. For this text its
program was compiled and run again by the participant's helper agent, with the
same output, and its parts were compared with the count beta by beta. The same
60 betas have a part. For the 53 betas that the count has in full, the two
parts are identical as fractions (the calculator prints the factor N1 through a
logarithm; in two outcomes the printed value misses an odd multiple of a power
of two by a relative error below 10^-11 and is read as that multiple). For the
seven betas in which the count holds estimates, the recount gives 0.282956
where the count has 0.282041. The recount is larger than the count by 0.0009 in
all. It confirms the count; the figure that the claim uses is not taken from
it. What was checked of it here is that its program reproduces its figures and
that they agree with the count; its method was read in its own description and
not re-derived.

*The outcomes of the heaviest beta.* The counting program is not part of
this package. So that the largest part of the count can be recomputed
without it, the outcomes of the heaviest beta are written out here.

| tau | eps | N1 | N3 | Adds |
| --- | --- | ---: | ---: | ---: |
| 285020a0 | 6e21be55 | 2^51 | 3 * 2^55 | 25,165,824.0 |
| 385020a0 | 6e21be55 | 2^50 | 2^57 | 16,777,216.0 |
| 185020a0 | 6e21be55 | 2^51 | 2^56 | 16,777,216.0 |
| 175020a0 | 6e21be55 | 2^49 | 3 * 2^55 | 6,291,456.0 |
| 685020a0 | 6e21be55 | 2^49 | 3 * 2^53 | 1,572,864.0 |
| 285060a0 | 6e21be55 | 2^50 | 3 * 2^52 | 1,572,864.0 |
| 385060a0 | 6e21be55 | 2^49 | 2^54 | 1,048,576.0 |
| 275020a0 | 6e21be55 | 2^49 | 2^54 | 1,048,576.0 |
| 185060a0 | 6e21be55 | 2^50 | 2^53 | 1,048,576.0 |
| 175060a0 | 6e21be55 | 2^48 | 3 * 2^51 | 196,608.0 |
| 685060a0 | 6e21be55 | 2^48 | 3 * 2^50 | 98,304.0 |
| 675020a0 | 6e21be55 | 2^47 | 2^52 | 65,536.0 |
| 275060a0 | 6e21be55 | 2^48 | 2^50 | 32,768.0 |
| 675060a0 | 6e21be55 | 2^46 | 2^48 | 2,048.0 |
| sum | | | | 71,698,432.0 |

The table lists the 14 outcomes with a nonzero product of the heaviest beta,
18b0e098 (k = 11). N1 is the number of triples (c1, b1, a2), with c1 XOR (c1 +
DY11) = ROL(beta, 12), for which E1 produces tau and eps; it is P1 times 2^85.
N3 is the number of quadruples (Y4, h1, Y9, w8) of step 3. "Adds" is N1 * N3 /
2^83, what the outcome adds to the class-rate part of the beta. Both counts can
be recomputed with a model counter from the definitions of 6.2 and of steps 2
to 4, without the calculator.

**Rule A and the count that the claim uses (participant computation).**
Rule A is a condition on h1, one of the four words of the E3 side. So for
an outcome (tau, eps) the number N3 of step 3 splits into the quadruples
whose h1 satisfies rule A and those whose h1 violates it, and under M the
rate of the trials with R = 0 that satisfy rule A is the sum of step 5 with
the first of the two numbers in place of N3. The claim does not use that
sum. It uses a smaller figure: every outcome for which a solver found a
solution that violates rule A is left out in full, with all its solutions.

Which outcomes these are was decided with a SAT solver. For each of the 453
outcomes with a nonzero product P1 * N3, over all 60 betas with a part, the E3
system of step 3 was written as a CNF formula from its definition: the unknowns
Y4, h1, Y9 and w8, E3 for both messages, and the four XOR differences that the
outcome prescribes. The solver kissat was asked two questions. First, whether
the formula has a solution. It has one for all 453 outcomes, and every model,
evaluated again in plain arithmetic, is a solution of its outcome with Y4 in
the class; 109 of these models satisfy rule A. Second, whether the formula has
a solution together with the clause that h1 violates rule A. For 54 outcomes
the answer is that it has none: if these answers are right, every solution of
these outcomes satisfies rule A, and stage A drops none of them. For the other
399 outcomes, in 60 betas, the solver returned a solution that violates rule A,
and each was evaluated again in plain arithmetic. So most outcomes of the count
have solutions that rule A drops. The count that the claim uses keeps only the
outcomes without such a solution, and only from the 53 betas that were counted
in full. Per beta, for the betas with a part of at least one:

| beta | k | Outcomes | Kept | Part of the beta | Part kept |
| --- | ---: | ---: | ---: | ---: | ---: |
| 18b0e098 | 11 | 14 | 8 | 71,698,432.0 | 64,061,440.0 |
| 18d0e098 | 11 | 19 | 13 | 54,005,760.0 | 50,036,736.0 |
| 18b1a098 | 11 | 16 | 4 | 25,692,160.0 | 4,259,840.0 |
| 18d1a098 | 11 | 18 | 6 | 8,429,568.0 | 5,505,024.0 |
| 18b3e098 | 13 | 8 | 4 | 1,566,720.0 | 1,392,640.0 |
| 18d3e098 | 13 | 10 | 5 | 838,656.0 | 745,472.0 |
| 18d1a398 | 13 | 6 | 0 | 11,152.0 | 0.0 |
| 19f1a098 | 13 | 10 | 2 | 8,640.0 | 1,280.0 |
| 18d16398 | 13 | 6 | 0 | 6,664.0 | 0.0 |
| 18f1e098 | 13 | 12 | 0 | 3,632.5 | 0.0 |
| 19f0e098 | 13 | 7 | 3 | 1,357.25 | 1,162.5 |
| 18d3e398 | 15 | 6 | 0 | 1,226.25 | 0.0 |
| 18d1af98 | 15 | 4 | 0 | 1,156.0 | 0.0 |
| 18d16f98 | 15 | 4 | 0 | 850.0 | 0.0 |
| 19b1e098 | 13 | 28 | 0 | 314.1248 | 0.0 |
| 18d37f98 | 17 | 4 | 0 | 165.0 | 0.0 |
| 18d1ff98 | 17 | 4 | 0 | 153.0 | 0.0 |
| 18d3bf98 | 17 | 2 | 0 | 61.875 | 0.0 |
| 18d3ef98 | 17 | 2 | 0 | 30.9375 | 0.0 |
| 19d1e098 | 13 | 10 | 2 | 15.8071 | 2.5 |
| 19b0a098 | 11 | 16 | 3 | 12.6172 | 3.625 |
| 19f1a398 | 15 | 4 | 0 | 12.5 | 0.0 |
| 19f0e398 | 15 | 7 | 0 | 12.2188 | 0.0 |
| 19f3e398 | 17 | 10 | 0 | 7.0703 | 0.0 |
| 18f1e398 | 15 | 4 | 0 | 2.1973 | 0.0 |
| 35 others | | 222 | 4 | 2.3100 | 0.1348 |
| sum | | 453 | 54 | 162,266,763.6579 | 126,003,600.7598 |

The 54 outcomes that are kept, one by one, so that the two questions can be put
again to any SAT solver from the definitions of 6.2 and 6.3; "Adds" is what the
outcome adds to the count, as in the table of the heaviest beta:

| beta | tau | eps | Adds |
| --- | --- | --- | ---: |
| 18b0e098 | 285020a0 | 6e21be55 | 25,165,824.0 |
| 18b0e098 | 385020a0 | 6e21be55 | 16,777,216.0 |
| 18b0e098 | 185020a0 | 6e21be55 | 16,777,216.0 |
| 18d0e098 | 285020a0 | 6e61be55 | 12,582,912.0 |
| 18d0e098 | 17d020a0 | 6e61be55 | 12,582,912.0 |
| 18d0e098 | 385020a0 | 6e61be55 | 8,388,608.0 |
| 18d0e098 | 185020a0 | 6e61be55 | 8,388,608.0 |
| 18d1a098 | 185060a0 | 6e603e55 | 2,097,152.0 |
| 18b1a098 | 185060a0 | 6e203e55 | 2,097,152.0 |
| 18d0e098 | 685020a0 | 6e61be55 | 1,572,864.0 |
| 18d0e098 | 285060a0 | 6e61be55 | 1,572,864.0 |
| 18d0e098 | 27d020a0 | 6e61be55 | 1,572,864.0 |
| 18b0e098 | 685020a0 | 6e21be55 | 1,572,864.0 |
| 18b0e098 | 285060a0 | 6e21be55 | 1,572,864.0 |
| 18d1a098 | 385060a0 | 6e603e55 | 1,048,576.0 |
| 18d1a098 | 2850a0a0 | 6e603e55 | 1,048,576.0 |
| 18d1a098 | 285060a0 | 6e603e55 | 1,048,576.0 |
| 18d0e098 | 385060a0 | 6e61be55 | 1,048,576.0 |
| 18d0e098 | 185060a0 | 6e61be55 | 1,048,576.0 |
| 18b3e098 | 185020a0 | 6e23be55 | 1,048,576.0 |
| 18b1a098 | 385060a0 | 6e203e55 | 1,048,576.0 |
| 18b1a098 | 285060a0 | 6e203e55 | 1,048,576.0 |
| 18b0e098 | 385060a0 | 6e21be55 | 1,048,576.0 |
| 18b0e098 | 185060a0 | 6e21be55 | 1,048,576.0 |
| 18d0e098 | 2850a0a0 | 6e61be55 | 786,432.0 |
| 18d3e098 | 185020a0 | 6e63be55 | 524,288.0 |
| 18b3e098 | 285020a0 | 6e23be55 | 262,144.0 |
| 18d0e098 | 685060a0 | 6e61be55 | 196,608.0 |
| 18d0e098 | 67d020a0 | 6e61be55 | 196,608.0 |
| 18d3e098 | 285020a0 | 6e63be55 | 131,072.0 |
| 18d1a098 | 6850a0a0 | 6e603e55 | 131,072.0 |
| 18d1a098 | 685060a0 | 6e603e55 | 131,072.0 |
| 18d0e098 | 6850a0a0 | 6e61be55 | 98,304.0 |
| 18b0e098 | 685060a0 | 6e21be55 | 98,304.0 |
| 18d3e098 | 185060a0 | 6e63be55 | 65,536.0 |
| 18b3e098 | 185060a0 | 6e23be55 | 65,536.0 |
| 18b1a098 | 685060a0 | 6e203e55 | 65,536.0 |
| 18d3e098 | 285060a0 | 6e63be55 | 16,384.0 |
| 18b3e098 | 285060a0 | 6e23be55 | 16,384.0 |
| 18d3e098 | 2850a0a0 | 6e63be55 | 8,192.0 |
| 19f1a098 | 6850a0a0 | 6fa03e55 | 1,024.0 |
| 19f0e098 | 6850a0a0 | 6fa1be55 | 768.0 |
| 19f0e098 | 685060a0 | 6fa1be55 | 384.0 |
| 19f1a098 | 685060a0 | 6fa03e55 | 256.0 |
| 19f0e098 | 67d160a0 | 6fa1be55 | 10.5 |
| 19b0a098 | 379160a0 | 6fde3e55 | 3.0 |
| 19d1e098 | 6850a0a0 | 6f9fbe55 | 1.5 |
| 19d1e098 | 685060a0 | 6f9fbe55 | 1.0 |
| 19b0a098 | 279160a0 | 6fde3e55 | 0.5 |
| 19d0a098 | 67d160a0 | 6f9e3e55 | 0.125 |
| 19b0a098 | 679160a0 | 6fde3e55 | 0.125 |
| 1fb3a098 | 279560a0 | 6bdc3e55 | 0.0078 |
| 1fd3a098 | 67d560a0 | 6b9c3e55 | 0.0010 |
| 1fb3a098 | 679560a0 | 6bdc3e55 | 0.0010 |
| sum | | | 126,003,600.7598 |

The kept outcomes add up to 126,003,600.7598. The claim uses this figure
rounded down,

    126,003,600.

It is 77.65% of the count of all solutions; 36,263,162.6160 is given up with
the 338 outcomes that have a violating solution, and 0.282 with the betas that
hold estimates. The largest outcome given up is tau = 189060a0, eps = 6e203e55
of beta 18b1a098, with 8,388,608.0. Under M the figure is a lower bound for the
rate of the trials with R = 0 that satisfy rule A, provided that the 54 answers
"no solution" behind it are right. The true rate under M is larger, because the
outcomes given up also have solutions that satisfy the rule. An exact count
that is described below gives it: r_A = 144,123,440.89 over all 60 betas (the
rule with four conditions has 162,243,609.86 and the rule with six conditions
has 123,244,449.00). So the figure that the claim uses is 87.4% of the model's
own value of r_A. The claim keeps the smaller figure.

The two questions were put a second time with another formula and other
solvers. The second formula has the unknown Y14 in place of h1 and prescribes
the four output differences of E3 in place of the differences inside it; it was
written by a reviewing helper agent of the filed package from the text of that
package, and for this package only its constants and its rule were changed.
cadical (2.1.3) and cryptominisat5 (CryptoMiniSat version 5.11.21) each
answered both questions for all 453 outcomes with the same result as kissat:
every base formula satisfiable, and the same 54 outcomes without a violating
solution. The three solvers are different programs; these runs kept no proof
certificate.

*Two further checks of the kept outcomes (programs of reviewing helper agents,
run again for this text).* First, a helper agent that reviewed this text put
the two questions again with a third formula of its own: two full G calls, the
class by the mask of Lemma Q, and R = 0 on the four output differences. With it
kissat gave the same answers for all 453 outcomes. For the 54 kept outcomes
cadical, run without preprocessing, wrote a DRAT proof of its answer
"unsatisfiable", and a checker that the same agent wrote, which accepts a
clause only when unit propagation derives a conflict from its negation,
accepted all 54 proofs, 187,867 clauses in all. In three controls the checker
rejected the same proof for the formula without the clause of the rule, which
is satisfiable, and rejected a proof cut in half. No standard proof checker was
used: the checker is a participant-side program, and the formula that it checks
is that agent's. Second, another helper agent that reviewed this text wrote an
exact count of the E3 side split by the rule: for an outcome, the number of
quadruples (Y4, h1, Y9, w8) of step 3 whose h1 satisfies the rule and the
number whose h1 violates it, in integers, from the definitions of 6.2 and
without a solver. Its N3 equals the calculator's for all 392 outcomes of the
betas counted in full and for 60 of the 61 outcomes of the betas that hold
estimates. The outcomes in which no quadruple violates the rule are exactly the
54 for which the solvers answered "unsatisfiable" (132 for the rule with four
conditions and 35 for the rule with six conditions, again the solvers' sets),
and they add up to the figure above. So the 54 answers behind the figure are
confirmed by a count as well as by solvers. For the betas that hold estimates
this count gives 0.282956 where the calculator's estimates add up to 0.282041;
with it the count of all solutions is 162,266,763.6588, the figure of the
independent recount. Both programs are the work of helper agents of the
participant, instances of the same AI model. The answers behind "no further
beta has a part" remain answers of one solver without certificates.

*Two solutions, written out.* A complete solution of the seven-word system with
Y4 in the class, which satisfies rule A, in the names of 6.2: Y1 = 8568b448, Y6
= 7a974bb8, Y12 = 2af81899, w12 = 00000000, w5 = 9e465eb8, Y4 = f9e4858e, Y9 =
77fdc40c, Y14 = cfd68bd7, w15 = 0, w8 = dcfafe9e. It has beta = 18b0e098, tau =
285020a0, eps = 6e21be55 and h1 = ccd8b4da. A complete solution of the
seven-word system with Y4 in the class that violates rule A: Y1 = 186cad47, Y6
= e79352b9, Y12 = 2d0c0d7d, w12 = 00000000, w5 = ffef9ff7, Y4 = e6049a1a, Y9 =
f0a9f131, Y14 = b5924807, w15 = 0, w8 = 3d56f91e. It has beta = 18b1a098, tau =
189060a0, eps = 6e203e55 and h1 = 139cd2be. For both, E1 and E3 evaluated for A
and B with the G function alone give R = 0. They are solutions of the system,
not messages: no context is known that produces these seven words.

*The other rules and the other factor.* Three rules were prepared, with four,
five and six conditions, each containing the one before it: the rule with four
conditions is the first four lines of rule A, and the rule with six adds that
bits 7 and 8 of h1 differ. The submitted program contains all three and the
long self-test was run for each. The same solver questions were put for each
rule. A rule with more conditions makes a trial cheaper, because fewer batches
run stage 2, and gives up more of the count. The package uses the cheapest rule
that leaves the count at least 3.5 times the assumed factor. The table gives,
per rule (named by its number of conditions), the count that H1 would be set
against, its ratio to the factors 2^25 and 2^26, the operations and loads of
stage A, the budgeted and (in brackets) the charged cost of a trial with the
margin of this package, and the scalar that the package would submit with each
factor.

| Rule | Count for H1 | / 2^25 | / 2^26 | Stage A | Per trial | 2^25 | 2^26 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 4 | 162,241,316 | 4.83 | 2.41 | 52 + 31 | 23.503 (24.6) | 97.9 | 96.9 |
| 5 | 126,003,600 | 3.75 | 1.87 | 55 + 32 | 18.253 (19.1) | 97.6 | 96.6 |
| 6 | 91,072,901 | 2.71 | 1.35 | 58 + 33 | 15.913 (16.7) | 97.4 | 96.4 |

This package is the row with five conditions and the factor 2^25. The other
rows and the other column are stated so that the choice can be seen; none of
them is claimed. With the factor 2^26 the count of every rule is less than 3.5
times the factor.

**Checks of the calculator (participant computations).** The E3 count of step 3
is the program of submission c47c1a80, and the enumeration of outcomes and the
E1 count are those of that submission; the checks reported there were made with
other constants and with delta = 2 or -2. For this package the calculator was
built again from the same sources, and the following checks were made for these
constants, this class and delta = -8.

First, the two counts at 32 bits against the approximate model counter ApproxMC
(tolerance 0.4, confidence 0.9), for the sixteen outcomes with the largest
products, which carry 83% of the count: the E1 system and the E3 system of an
outcome were each written as CNF straight from their definitions and their
solutions were counted. For E1, 16 of 16 outcomes were compared; the mean of
log2(calculator / ApproxMC) is +0.0014 and the largest difference 0.023 bits.
For E3, 16 of 16; mean +0.0118, largest difference 0.159 bits. ApproxMC is
approximate, so this check excludes an error of a factor of two in a large
outcome, not a small one.

Second, which betas have a part. For all 4,550 betas with k at most 14 the
solver was asked whether the whole system has a solution with that beta: 15 are
satisfiable, 4,535 are not, none is undecided; the 15 satisfiable ones are
exactly the fifteen betas with a part, and all 15 models are solutions in plain
arithmetic. Over all 133,742 betas the satisfiable ones (60) are exactly the
betas with a part (60).

Third, both counts against brute force with 8-bit words. The E1 count with a
difference of 8 or -8 between the two words: for 30 random cases, all 36,826
outcomes that have solutions were compared and 36,826 are equal; of the
outcomes without solutions, 30,448 were sampled and 30,448 are zero in the
calculator as well. A second seed with 60 cases gave 85,708 of 85,708. The E3
count: for 6 cases, 62,639 of 62,639 outcomes with solutions equal, and
1,572,897 sampled outcomes without solutions agree.

Fourth, the sampler, for the four heaviest betas, as reported under the table
of the count. Fifth, the independent recount reported above: another method,
another program, integer arithmetic, every beta. It is the only one of these
checks that covers both factors of every outcome. It was a confirmation with
the total and four parts known to the other model, not a blind recount.

What these checks cover: the E1 count against brute force only for 8-bit
words and against an approximate independent counter for the sixteen
heaviest outcomes at 32 bits; the E3 count in the same two ways; which
betas have a part, against a solver on a formula of the whole system; the
whole count against the independent recount above, which is the only
check that covers both factors of every outcome; and the E3 factor of
every outcome against the exact count reported with rule A above. All of
these are participant computations.

**How the constants and the class were found.** The constants come from the
solver search of submission c47c1a80, not from farming random sets. One CNF
instance holds, with real word values: the call C3 for both messages with equal
b and d outputs, so that every model is a set of constants with the property of
Fact P; E1 and E3 for both messages; a zero residual; and a bound on the number
of bit positions, bit 31 excepted, at which a difference is active in six
additions of E1 and E3. For this package the instance was changed in two
places: the two words w4 differ as the length cancellation prescribes for the
XOR of the two lengths, and the top byte of the pinned word 13 is zero. The
solver is kissat. The search was run for several XORs of the two lengths other
than 2; its log holds 65 sets of constants, 27 of them for the XOR 8, from runs
of up to 119 minutes each. The constants of 3.2 came from an instance with
bound 104, after 4,770 seconds, with 100 active positions; the solver's
solution has eta = 830303cf and beta = 18b0e098. The class of this package is
the class of that solution, and its beta is the heaviest beta of the count. For
every set of the log, the beta of the solver's solution was counted in the
class of that solution: the constants of 3.2 had the largest value, 71,698,432;
the largest of the others was 13,107,200 and their median 80,028. The bound
steers the search towards solutions that are reached with high probability
under M; the count, not the bound, is what H1 is set against. Of 305 classes
near this one, counted over a list of 799 betas of their own, 76 have a part;
this class has the largest, 162,245,268 on that list, and the next is eta =
8f0306cf, with 2^17 members and 47,846,517.

**Checks of the construction on real messages (participant computations).** A
reference program for steps S1 and T, written before this text from the solved
equations and not from the experiment program, built 200,000 trials (4,000
random contexts, 50 members each) and hashed both messages of each with a
forward compression that equals the organizer's reference hash on 20,000 random
messages: in all of them the lengths are 55 and 63, the last eight bytes of B
and the words 14 and 15 are zero, the states after round 0 are equal, the four
constants are in place, Y4 is the prescribed member in A and in B, digest words
0, 2, 5 and 7 agree and the difference of E3's first-half d value is eta. A
second program, written separately from the experiment program, has the lines
of steps S1 and T a second time, name by name; on 20,000 random trials it runs
round 0 and round 1 forwards on the trial's words and compares every one of the
nine calls of Lemmas S, F and Y, with all its eight values, with the names of
the lines, and checks Lemmas L, Q, T, E, N and A on the same trials; all of its
checks hold. The lines of the two displays of Section 4 were also typed again
from this text, with its names, and run on 20,000 trials, half of them with a
word y outside the class: the sixteen words are those of the submitted program,
a forward round 0 gives the state S and the state X of the text, and each of
the nine calls has the eight values that Lemmas S, F and Y state. The program
that produced the measurements below was checked against 2,000 test vectors of
the reference (message words and both digests equal in all) and on 16,384 of
its own trials, rebuilt as real strings of 55 and 63 bytes and hashed
completely on the host: all agree on digest words 0, 2, 5 and 7, have Y4 in the
class, the pinned words in place and the residual that 6.2 computes. The
self-test of the submitted program checks every lane of its batches against the
complete digests of the two messages of the lane's trial (6.5). An earlier
scalar program for the same batch checked 16,777,216 trials of 32 contexts in
the same way: all agree on the four digest words, and in all the word n of
Lemma N equals D3 XOR ROL(D6, 8) of the two digests. These are checks on random
inputs. They do not prove the lemmas; Section 4 does.

**Checks of the model on real messages (participant measurement).** Real
trials of 6.1 were compared with draws from M (Y4 a uniform member of the
class, the other six words uniform and independent), on the same
statistics: how often each of the four residual words, or its low 16 bits,
is zero, how many trials have a residual of low weight or with many
trailing zero bits, how often the early test of Lemma E passes, and in how
many trials E1 requires the class. The last of these is the event
eps XOR ROL(beta XOR eps, 1) = eta, so a trial in which E1 requires the
class is a trial that passes the E1 test of Lemma N. The algorithm of this
package uses the E1 test and not the early test; both are reported because
the programs print both. For some events the probability under M is known
exactly from the count, and the real trials are then compared with that
number directly: the event that E1 has one of the betas of the table with
k <= 14 ("listed beta"), that it also has a tau of one of the counted
outcomes of that beta, that it has both tau and eps of a counted outcome
("listed E1 outcome"), and an event on the E3 side alone, that E3 shows
the differences psi and eps of a counted outcome after its first six
assignments ("listed partial E3 event").

Three layouts of real trials were used. In the runs with *independent contexts*
every thread of the generating program draws its own context, seven random
words, and makes its trials in it with random members of the class. In a
*layout run* one sextuple (vc, vd, S11, S4, X13, w0) is drawn at random and
held, X14 runs through 2^21 consecutive values and every member of the class is
tried for each: 2^40 trials. A layout run is laid out like the work of step 2
for one pair (vc, vd), of which it covers a share 2^-11, except that its vd is
a random 32-bit word and not one below 2^19. Different layout runs have
different sextuples. A *spread run* has the sextuple and the first value of X14
of one of the first eight layout runs, and its 2^21 values of X14 lie a fixed
odd step apart, so that they are spread over all 2^32 values; the eight spread
runs were made as a diagnostic after the first eight layout runs. No run has
the structure of a whole run of 6.4, in which all pairs share four seed words.

*Real trials against draws from M, independent contexts.* 2^40 real trials
against 2^40 draws from M: 87 statistics with at least 30 events, largest
deviation -2.92 standard deviations (listed beta with a listed tau); 2^42 real
trials against 2^42 draws from M: 90 statistics with at least 30 events,
largest deviation -3.04 standard deviations (the first residual word zero);
2^45 real trials against 2^44 draws from M: 95 statistics with at least 30
events, largest deviation +2.55 standard deviations (residuals with exactly 1
trailing zero bit). The comparing program of the groundwork had the runs with
independent contexts of 2^40, 2^42 and 2^45 trials, the first eight layout
runs, the eight spread runs and the draws from M. Over all comparisons that it
made, between these runs and with the exact expectations, 1,880 tests in all,
11 are beyond three standard deviations, where about 5.1 are expected by
chance. Nine of them concern the first four conditions of rule A in the layout
runs and the spread runs, four of the nine in the spread runs; they are the
subject of the next heading. The other two are one event counted under two
names, the first residual word being zero, in the comparison at 2^42 (990 real
against 1,130 from M); it does not repeat in the larger comparison.

*Real trials against exact expectations.* For the events whose probability
under M is known from the count, the counts were added up from the result files
of every finished run with real trials: eight runs with independent contexts
(2^40, 2^42 and 2^45 trials and five later runs of 2^45 trials each, those that
were finished when this text was built), the 24 layout runs and the eight
spread runs, 2^47.84 trials together. They give: listed beta, 1,014,284,575,998
against 1,014,283,370,496 expected (+1.20); listed beta with a listed tau,
521,815,234 against 521,812,224 expected (+0.13); listed partial E3 event,
51,093 against 51,082.60 expected (+0.05); and listed E1 outcome, 204 against
205.97 expected (a Poisson count; the probability of a count this far from its
mean is 0.94). The numbers in brackets are standard deviations. The runs with
independent contexts alone, 2^47.62 trials, give: listed beta, 872,551,323,030
against 872,549,449,728 expected (+2.01); with a listed tau, 448,912,155
against 448,895,232 expected (+0.80); listed partial E3 event, 43,814 against
43,944.42 expected (-0.62); listed E1 outcome, 180 against 177.19. The listed
E1 outcome has probability about 2^-40.2 per trial and the listed partial E3
event about 2^-32.2; these are the deepest events on which M was compared with
real messages, each on one call alone. Per beta, the listed E1 outcomes
observed and expected in all real runs for the six heaviest betas are 38 and
35.56, 55 and 51.88, 56 and 61.50, 51 and 48.30, 2 and 2.68 and 2 and 3.13. The
same events in the 2^44.39 draws from M agree with the exact expectations as
well (listed beta, 93,012,538,681 against 93,012,885,504 expected (-1.14); with
a listed tau, 47,850,289 against 47,851,776 expected (-0.21); listed partial E3
event, 4,659 against 4,684.43 expected (-0.37); listed E1 outcome, 22 against
18.89), which checks the expectations against the program that draws from M.

*Layout runs.* 24 layout runs of 2^40 trials were made, eight first and sixteen
later with the same program and arguments. The passes of the early test per run
have mean 48,523.2 (the model run of 2^40 draws gave 48,615) and a ratio of
variance to mean of 1.283, where 1 is the value for independent trials
(chi-square 29.50 on 23 degrees of freedom, probability 0.16). The first eight
runs alone have 2.23 (chi-square 15.60 on 7, probability 0.029) and the sixteen
later ones 0.925 (probability 0.54). The value of the first eight was known
before the sixteen were started, and the sixteen were made to see whether it
would repeat; it did not. The passes of the E1 test per run have a ratio of
0.84 (probability 0.68). In the 24 runs together the listed events are listed
beta, 106,299,960,790 against 106,300,440,576 expected (-1.47); with a listed
tau, 54,683,696 against 54,687,744 expected (-0.55); listed partial E3 event,
5,493 against 5,353.63 expected (+1.90); listed E1 outcome, 19 against 21.59.
These runs test the spread between pairs (vc, vd) with independent seed words
on events of probability about 2^-24 and above. They do not test a run of 6.4.

*Spread runs.* The eight spread runs, 2^40 trials each, have 48,545, 48,321,
48,787, 48,540, 48,737, 48,512, 48,307 and 48,703 passes of the early test, a
ratio of variance to mean of 0.67 (chi-square 4.68 on 7, probability 0.70).
Their listed events together are listed beta, 35,433,292,178 against
35,433,480,192 expected (-1.00); with a listed tau, 18,219,383 against
18,229,248 expected (-2.31); listed partial E3 event, 1,786 against 1,784.54
expected (+0.03); listed E1 outcome, 5 against 7.20.

**Rule A on real trials: the model fails inside one context (participant
measurement).** The programs for the graphics card record the first four
conditions of rule A (bits 0, 1, 16 and 17 of h1), which a uniform word
satisfies with probability 2^-4. In a sample of 4,096 independent contexts,
each with all 524,288 members, the number of members that satisfy them has mean
32,788.1, which is 2^-3.9991 of the members, but a variance of 4,230,272 where
independent trials would give 30,738: 138 times as much. In that sample a
single context has between 21,660 and 45,271 such members, that is between 0.66
and 1.38 times 2^-4. These are the smallest and the largest value of one sample
and not bounds: the samples on the processor reported below have values from
0.58 to 1.46. So inside one context the trials do not satisfy the conditions
like independent uniform words: the share depends on the context, with a
standard deviation of 6.3% of its mean. In the same contexts a single one of
the four conditions is far more regular than independent trials would be (its
count has 0.003 of the binomial variance), and the event that E1 has a listed
beta is as for independent trials (ratio 1.016). The cause of this structure
was not analysed. Averaged over contexts the share is the model's: in all runs
with independent contexts together, 13,537,739,903,614 trials satisfy the four
conditions where 2^-4 of the trials is 13,537,736,916,992 (+0.84 standard
deviations of a binomial count).

*The four conditions in the layout runs and the spread runs.* In a layout run
2^21 contexts share their outer words and have consecutive values of X14. In
each of the 24 layout runs the share of the trials that satisfy the four
conditions is within 5 parts in 100,000 of 2^-4; 14 of the 24 are below it, and
their mean is 3.8 parts in a million below it. The variance of the 24 counts is
24.7 times the binomial one (first eight 39.4, the sixteen later ones 11.4).
Added up, the 24 runs are 5.04 binomial standard deviations below 2^-4; the
first eight alone are 11.92 below and the sixteen later ones 2.25 above. The
binomial yardstick does not fit, because the runs scatter more than binomial
counts do. Measured with the scatter of the runs themselves, the 24 together
are 1.0 standard errors below 2^-4 (23 degrees of freedom), the first eight
alone 1.9 below (7 degrees of freedom) and the sixteen later ones 0.7 above (15
degrees of freedom). The variance between independent contexts found above is
not the yardstick either. Single contexts of a layout run do scatter like
independent contexts: for the sextuple of layout run 1 the program that counts
per context was run on 4,096 contexts with consecutive values of X14 and on
4,096 with values a fixed odd step apart, and the count of one context has 146
and 107 times the binomial variance and lies between 0.72 and 1.33, and between
0.71 and 1.32, times 2^-4. A run of independent contexts would then have about
138 times the binomial variance, and the layout runs have 24.7: the deviations
of the contexts of a run largely cancel in its sum (with the variance of
independent contexts the first eight would be 1.0 standard deviations below
2^-4 and all 24 0.4). The eight spread runs have 95.6 times the binomial
variance; each is within 6 parts in 100,000 of 2^-4, and together they are 8.17
binomial standard deviations below it, which is 0.8 standard errors of their
own scatter (7 degrees of freedom). So these runs show the dependence on the
context again, and measured with the scatter of the runs themselves no group of
runs differs significantly from 2^-4.

*The four conditions together with an event of E3.* The programs for the
graphics card also count, among the listed partial E3 events, those whose h1
satisfies the four conditions. This is the one measurement that joins the rule
with a deep event of the call that h1 belongs to; the event has probability
about 2^-32.2 per trial. The share to expect under M is far from 2^-4, because
the event and the rule both depend on h1. It was computed exactly, by an
enumeration that a reviewing helper agent wrote from the definitions of 6.2 and
that was run again for this text: its counts of the 183 listed events equal
those of the list for all 183, and under M a share of 0.580935 of the listed
partial E3 events have an h1 that satisfies the four conditions (0.484216 for
the five conditions of rule A, 0.412442 for six). On real trials: all runs
together, 29,693 of 51,093, a share of 0.5812 (+0.10); the runs with
independent contexts, 25,486 of 43,814, a share of 0.5817 (+0.32); the 24
layout runs, 3,155 of 5,493, a share of 0.5744 (-0.99); the spread runs, 1,052
of 1,786, a share of 0.5890 (+0.69). The numbers in brackets are standard
deviations from the exact share. The draws from M have 2,791 of 4,659, a share
of 0.5991, which is 2.51 standard deviations above the exact share under M
itself: where the real trials look low against these draws, it is the draws
that are high. So where the first four conditions of the rule meet an event of
E3 of this depth, the real trials have the model's share. This measurement does
not have the fifth condition, it is an event of one call, and it is far from R
= 0.

*Rule A with all its conditions (processor).* The fifth condition is not
recorded by the programs for the graphics card. A participant tool that uses
the context and the trial of the submitted program counted the three rules on
the processor, for 2,048 random contexts with all 524,288 members each, 2^30
real trials: 33,485,196 trials satisfy rule A, a share of 2^-5.0030. They are
0.50002 of the trials that satisfy the first four conditions, so the fifth
condition halves the count. The share of one context is 0.9979 times 2^-5 on
average, with a standard error of 0.0013, and in that sample it lies between
0.72 and 1.32 times 2^-5. 18,651,177 of the 153,393,152 batches hold a trial
that satisfies rule A, a share of 0.1216; in that sample the share of the
batches of one context lies between 0.0731 and 0.1654. A second run of the tool
with another seed, again 2,048 contexts, gives 2^-5.0025, that is 0.9983 times
2^-5 with a standard error of 0.0014; one context between 0.61 and 1.36 times
2^-5; a share of 0.1219 of the batches, for one context between 0.0674 and
0.1606. The budget of step 4 is 0.250 of the batches of a run. No context of
the samples of this section reaches the budget in batches: the largest share of
the batches of one context is 0.1684, among 13,312 contexts. But the bound that
H3 uses, one batch per trial that satisfies the rule, is exceeded by single
contexts and holds only on average: seven times the average share of the trials
is 0.2183, and seven times the largest share of one context in these samples,
1.46 times 2^-5, is 0.319.

*Rule A in the ranges of the algorithm (processor).* The same tool was run with
contexts laid out as step 2 lays them out: eight sets of the four seed words,
for each set four pairs (vc, vd) with vd below 2^19, and for each pair 64
consecutive values of X14 from a random start; 2,048 contexts with all members,
2^30 trials. 33,535,120 trials satisfy rule A, a share of 2^-5.0008: 0.9994
times 2^-5, with a standard error of 0.0010 from the scatter of the 32 pair
means. The means of the eight sets lie between 0.9942 and 1.0021, and single
contexts between 0.61 and 1.31. The share of the batches that hold such a trial
is 0.1133, for one context at most 0.1500; for random contexts it was 0.1216.
For the rules with four and six conditions the shares are 0.9993 times 2^-4 and
0.9992 times 2^-6. The start of X14 is random here; the algorithm starts every
pair at X14 = 0.

*Two programs of reviewing helper agents, run again (processor).* Two of the
helper agents that reviewed this text measured the same share with
implementations of their own, typed from Sections 1, 4 and 6 of this text and
not taken from the submitted program. Both programs were run again for this
text. The first checks its construction on 1,200 real trials with the
organizer's reference hash and then counts all members of the class in four
layouts. In 1,024 independent contexts the share is 0.99879 times 2^-5, with a
standard error of 0.00204 (single contexts from 0.584 to 1.253). In 1,024
independent contexts with vd below 2^19 it is 0.99941, with 0.00198 (single
contexts up to 1.325). For 12 sets of seed words with 192 contexts each (vc
random, vd below 2^19, X14 random) the set means lie between 0.9926 and 1.0065,
where the standard error of one set mean is 0.0044; a chi-square test of equal
means gives probability 0.45. For 12 pairs (vc, vd) with 192 random values of
X14 each the means lie between 0.9882 and 1.0063 (probability 0.36). The second
program compares 10,000 of its lanes with rule A on the h1 of the complete
compression of the real message A; all are right. In 1,024 independent contexts
it finds 0.99771 times 2^-5, with a standard error of 0.00206 that follows from
the scatter between contexts that it prints, and with single contexts from
0.730 to 1.455 (for the four conditions from 0.729 to 1.455 times 2^-4), and a
share of 0.1222 of the batches, for one context at most 0.1684. For six pairs
(vc, vd) with vd below 2^19 and 1,024 consecutive values of X14 each, with seed
words held, its pair means lie between 1.00021 and 1.00080 times 2^-5: they
scatter by 0.021% where independent contexts would give 0.206%. So the mean
over consecutive values of X14 is far more regular than a mean over independent
contexts, as the layout runs on the graphics card show for the four conditions;
and all six of these means are above 2^-5, by 0.02% to 0.08%, more than their
scatter, so that over windows of this kind the average is not exactly 2^-5; the
difference is far inside the budget. In the six processor samples for which a
mean and its standard error are given under this and the two headings before
it, the mean is within 1.6 standard errors of 2^-5; the six means lie between
0.9977 and 0.9994, all on the low side. No shift from the restricted range of
vd or from shared seed words is visible at this size. These are processor runs
of 2^29 to 2^32 trials, a share of 2^-70 of a run or less. A run on the
graphics card that records all five conditions in the layout of the algorithm
is still owed.

*The E1 test.* In the eight runs with independent contexts together, 77,238 of
2^47.62 real trials pass the E1 test, a share of 2^-31.39; the 2^44.39 draws
from M gave 8,242, a share of 2^-31.38 (-0.09 standard deviations between the
two). In the 24 layout runs 9,520 of 2^44.58 trials pass, a share of 2^-31.37,
and in the eight spread runs 3,075 of 2^43.00, a share of 2^-31.41. A uniform
32-bit word would be zero with probability 2^-32; the test passes about 1.5
times as often, and M predicts that. H2 budgets a share of 2^-16.

**Scaled-down end-to-end checks (participant computations; another
construction, other constants).** With short words the whole search can be run
and its collisions counted. Such runs exist only for the construction of
submission c47c1a80, with lengths 60 and 62 and its trial, and with constant
sets of their own with 8-bit and 10-bit words; they are reported in the text of
that submission and are not repeated here. They compared the collisions found
with the model's exact prediction: 9,835 against 9,837.9 predicted over six
series at 8 bits, 693 against 664.6 over four series at 10 bits, and 1,813
against 1,807.2 for the search without the class restriction. They are evidence
for the method, that is for M and for the independence of the trials at the
depth of actual collisions when words are short, in another layout of the
trial. No scaled-down run has been made for lengths 55 and 63, for steps S1 and
T of this text, or with a first-stage rule of the kind used here. This is the
largest piece of evidence that the filed package has and this package does not
have.

The declared experiment `residual-search` runs the search of Section 6 at toy
scale: one context per seed, then the members of the class in order from a
number taken from the seed, stopping at the first trial whose residual has
a zero low byte in digest word 1. The search runs without rule A, without
the E1 test and without the packing of 6.5. The organizer checks that
every returned pair agrees on 136 digest bits. It checks the trial
generator and the residual computation on real digests. It is not a test of
H1, H2 or H3 and says nothing direct about 128 bits. Beside the search, the
program evaluates one packed batch per seed on the counting machine of 6.5
and returns the operations and loads of its two stages, its right lanes and
whether a lane satisfied rule A as observations; the organizer records them
as untrusted and does not check them.

**Limits of the evidence.**

- The factor 2^25 in H1 is assumed. It is set against a count of 126,003,600
  under M, from a participant computation. The organizer-run experiments do not
  measure the factor, and the success bound needs it to be at least 33,502,523.
  With factor 1, the uniform rate, the same search needs 2^127 trials and gives
  time_log2 = 122.6.
- M does not hold inside one context for rule A: the share of the trials of one
  context that satisfy the rule depends on the context (for its first four
  conditions it lay between 0.66 and 1.38 times 2^-4 in a sample of 4,096
  contexts, and other samples have values up to 1.46). Only the average over
  contexts has the model's value. Every statement of this text about the pass
  rate of rule A, about the stage-2 budget and about r_A is a statement about
  that average. The cause of the dependence was not analysed. Whether the rate
  of the good trials, which need rule A and R = 0 together, also has the
  model's value on average was not measured and cannot be: no measurement
  reaches R = 0. If the good trials sat mostly in contexts with a low share,
  r_A would be overstated. One measurement joins the rule with a deep event of
  E3 (of the listed partial E3 events of all real runs, 29,693 of 51,093 have
  an h1 that satisfies the first four conditions, where M gives a share of
  0.5809) and shows no such shift; it has the first four conditions only, an
  event of one call, and a probability far above that of R = 0, so it does not
  exclude it.
- Rule A is not implied by a collision; it loses solutions. That it loses no
  more than the count allows rests on the answers, for 54 of the 453 outcomes
  of the count, that no solution violates rule A. These answers come from three
  solvers on two formulas, which kept no proof certificate; from a third
  formula, for which one solver wrote proofs that a checker written by a helper
  agent accepted, no standard proof checker being used; and from an exact count
  of the E3 side split by the rule. All of these programs were written and run
  by the participant's helper agents, instances of the same AI model. The 399
  outcomes with a violating solution are left out in full, and that is 22.35%
  of the count: this rule gives up far more than the rule of the filed package
  did (0.04%). Rule A was read off counts of the same kind as the count itself,
  for this class: it was chosen to fit the solutions that the count knows. No
  measurement on real messages reaches the event of H1, so none tests rule A
  together with R = 0.
- The count is exact only under M. It counts the solutions of the seven-word
  system; that the trials of the algorithm meet those solutions at the rate M
  predicts is the assumption. For 32-bit words and these constants M has been
  compared with real messages only for events of probability about 2^-40 and
  above. Its use at the probability of the event R = 0, about 2^-100.73, is an
  extrapolation that no feasible experiment can test directly. M has been
  tested end to end, down to actual collisions, only for words of 8 and 10
  bits, with other constants and with the trial of the earlier submissions, not
  with steps S1 and T.
- The constants and the class were chosen to make the count large: by a solver
  search that minimises the number of active bit positions of one solution, and
  then by the count itself. The count is deterministic, so no sampling noise
  enters it and no choice among noisy estimates was made. But a choice that is
  best under M says nothing about M. If M overstates the rate for some
  constants, a search for the largest count under M will tend to find those
  constants, and nothing here measures that.
- The count rests on few paths: 44% of it comes from one beta and 77% from two,
  and 83% from sixteen outcomes. An error in the count of these outcomes would
  change the figure in proportion.
- The calculator is not part of the package, and it and every check of it are
  the participant's. The statement that no beta with k >= 15 beyond the 45
  counted ones has a part rests on a solver's answers "unsatisfiable" for
  129,147 betas, from one solver and one formula, without certificates, and on
  the independent recount, which visited every beta with its own method.
- The independent recount was made by another AI model with a program of its
  own. It was not blind: the request stated the participant's total, the four
  heaviest parts and the number of betas with a part. Its program was compiled
  and run again by the participant's helper agents, and its parts were compared
  beta by beta; its method was read in its own description and was not
  re-derived or reviewed line by line.
- All trials of a run share the four seed words S11, S4, X13 and w0, the 2^32
  contexts of one pair (vc, vd) share everything that step S1 computes without
  X14, and the 524,288 trials of one context differ only in Y4 and what follows
  from it. There is a further shared structure: step S1 reads vc and vd only in
  X8 = vc - vd and in its last line, vb. So the 2^19 pairs (vc, vd) with the
  same difference vc - vd have, for every X14, the same state S and the same
  words w0..w7 and w12, and the 2^38 trials of such a group and one X14 are
  messages that differ only in w8..w11. The 2^51 pairs are 2^32 such groups. No
  measurement has this structure: every layout run holds a single pair.
  Independence of the trials is assumed, not shown. With a count that rests on
  few paths, whether a run contains a collision may depend on a few shared
  words more than it would for a rate spread over many paths; this was not
  examined. The layout runs hold one sextuple of outer words each and cover
  2^21 of the 2^32 values of X14; the first eight had a ratio of variance to
  mean of 2.23 in the passes of the early test, which the sixteen later runs
  did not repeat (0.92; all 24: 1.28). No run on the graphics card shares seed
  words between pairs as a run of 6.4 does, or has a vd below 2^19; the
  processor runs that do, reported under rule A, measure only the share of the
  trials that satisfy the rule.
- Single-word statistics are not evidence for the joint rate. An earlier
  version of this construction, cancelled by the submitter before screening,
  used other constants and inferred a rate of half the uniform one from the
  frequencies of single zero residual words; a count of the kind described
  above gave 0.024 for those constants.
- H2 rests on the pass rate of the E1 test measured on real trials with these
  constants: 77,238 passes in 2^47.62 trials with independent contexts, and
  9,520 in the 24 layout runs. That the number of passes of a full run of 2^102
  trials stays near the mean is assumed. The budget is 2^15.3 times the passes
  expected at the measured rate.
- H3 rests on the share of the trials that satisfy rule A, averaged over
  contexts: 2^-5.0030 and 2^-5.0025 for rule A in two samples of 2,048 random
  contexts on the processor; 2^-5.0008 in 2,048 contexts laid out in the ranges
  of the algorithm (eight sets of seed words, vd below 2^19, consecutive values
  of X14); and 2^-4 to within 0.84 standard deviations for its first four
  conditions in 2^47.62 trials with independent contexts on the graphics card.
  The fifth condition was not measured on the graphics card. What step 4
  budgets is batches: the measured share of the batches that hold a trial
  satisfying rule A is 0.1216 for random contexts and 0.1133 in the ranges of
  the algorithm, against 0.25. The budget on trials is 1.142 times 2^-5. That
  the average over the contexts of one run of 2^102 trials is not that far
  above the mean is assumed. If either budget of step 4 is exceeded the
  algorithm halts with failure: that lowers the success probability, by the
  0.0005 allowed for each of H2 and H3, and does not raise the time bound.
- The charge of 19.1 operations per trial is the budgeted cost of a two-stage
  batch plus a margin of 4.6%. The stage counts are those of the machine in the
  submitted program; no organizer run verifies them. The work per pair (vc, vd)
  is bounded in words and was not counted on the machine; with the bound of
  Section 8 it is a share below 2^-40 of the main loop.
- The two memory figures of the preprocessing in Section 9 are observations of
  the runs and were not measured by a tool.

**Scope and limitations.**

- No full collision of the 2-round hash is exhibited. The search is an
  analytical cost claim like other packages on this track; unlike a birthday
  search it tests each trial against zero and so needs no memory that grows
  with the number of trials.
- The two messages have different lengths, 55 and 63 bytes, and the
  construction relies on the true block length being a compression input, as
  the target profile specifies. The 63-byte message ends in eight zero bytes:
  in the zero-filled block of both messages the words 14 and 15 and the top
  byte of word 13 are zero.
- The gain over a generic birthday search has three sources: half of the digest
  is matched by construction, which removes the table and about half of the
  round-1 work per trial; the constants are chosen so that the remaining half
  can match at all with a useful rate; and the search stays inside one class of
  Y4, where that rate is assumed to be 33,554,432 times the uniform one. The
  exponent of the number of trials is 102 instead of 128, and 127 if only the
  uniform rate is assumed.
- The half-collision, the class search, the two tests and the two-stage batch
  are those of the submissions 17bba2ae, 5ceb1802, 04638ed8 and c47c1a80 on
  this track, which claim 123.5, 121.5, 112.4 and 99.4. What is new against the
  last of them is the pair of lengths, 55 and 63 in place of 60 and 62, with
  the zero words that it forces; the constants, found by the same solver search
  run for that length pair; the construction of Section 4, in which the context
  is seven words and a trial changes four message words; the class; rule A; and
  the counts of the batch. Against c47c1a80: the class has 524,288 members in
  place of 65,536; the count that H1 is set against is 126,003,600 in place of
  29,965,882; the assumed factor is 2^25 in place of 8,388,608; stage A is 55
  operations and 32 loads in place of 64 and 36, stage 2 115 and 48 in place of
  96 and 42, with stage 2 counted for one quarter of the batches in place of
  one eighth; and a trial is charged 19.1 operations in place of 17.4.
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

- time_log2 = 97.6 bounds total charged time by 2^97.6 units.
- memory_log2_bytes = 35 bounds the storage of the preprocessing and of the
  search by 2^35 bytes; the search alone needs less than 2^22 bytes (Section
  9).
- preprocessing_log2 = 63 bounds the recomputation of the six constants and the
  selection of the constants, of eta and of rule A by 2^63 target-compression
  units.
- nonuniform_advice_log2_bytes = 6 bounds the stored constants, eta and the
  constants of rule A, 40 bytes, by 64 bytes.
- success_probability = 0.39 holds under H1, H2 and H3 as shown in Section 7.

The required baseline_improved identifier blake3-r2-nominal-v2 names the
organizer's nominal display reference 128, which is not an established attack,
a qualified baseline or a security bound. The claimed scalar 97.6 is lower than
that display value. Whether a qualified result improves the Yukon incumbent is
decided separately, and no Pareto dominance claim follows from the scalar.
