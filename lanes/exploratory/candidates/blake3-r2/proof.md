# Full-resident and complement-propagated derivative of the BLAKE3 class search

This package directly derives from Jbenisek submission
04638ed8-4aa3-4e27-ab72-16755587ae48 (112.4) and 5kyguy submission
c85fc92 (112.12), with material credit also to tekkac (2bf40fb) for the
packed-word technique; all three are credited as originators and co-authors in
that sense. It is not human accepted.

**Reading convention:** Sections 1-10 below preserve the source proof and its
participant-reported evidence for the unchanged construction and H1/H2. Their
16-register implementation and 112.4 scalar describe the source. Section 11
specifies this derivative's complement-propagated K3/D1 equations and
64-register full-resident schedule (55 registers used; 151 ALU/control ops +
2 list loads + 2 list-address ops = 155 ops/batch, time_log2 = 111.81), as well
as the 32-register schedule (112.07). The three declared experiments
(`half-collision`, `residual-search`, `resident-audit`) are executed by the
organizer runner and provide finite-scale organizer-verified evidence for the
exact half-collision, the 136-bit class residual search, and the shared-seed
`S5`-fixed early-test pass rate and packed schedule equivalence.

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
construction enumerates such pairs while it holds one internal word of round
1, called Y4, inside a set of 4,096 values, the *class* (Section 6.1).

**Heuristic part.** A collision needs the other four digest words to agree as
well. The algorithm searches 2^116 such pairs, all with Y4 in the class, for
one where they do. The search has no table that grows with the number of
trials and does no sorting or lookup. Seven trials are evaluated in one
256-bit word, and a trial is charged 34 primitive operations, memory loads
included. Under the declared heuristics, H1 that a trial completes the
collision with probability at least 2^-117 and H2 that a budget on early-test
passes suffices, the search succeeds with probability at least 0.39. Total
charged time is below 2^112.36 target-compression units, so the claimed
scalar is 112.4. Peak memory is below 2^20 bytes (Sections 6 to 9).

The rate in H1 is an assumption: 2,048 times the rate of a uniform 128-bit
value. It is not read off single digest words. Section 10 describes what it
is set against. The remaining half of the digest depends on seven words, one
of which is Y4. The number of values of the other six that give a collision
was estimated, for Y4 in the class, by sampling. The count for one sample is
exact when its enumeration fits a work budget and a random-subset estimate
otherwise; in the run that gives the quoted figure every nonzero value is a
count made in full. Under the model that the six words behave like
independent uniform words, the estimate is a lower bound of 7,319 +- 816
times 2^-128. H1 assumes 2,048 times. The class and the six constants were
selected by measurements of this kind; the quoted figure was obtained
afterwards, on fresh samples. The model was compared with real messages only
on events of probability about 2^-32 and above. The organizer-run experiments verify the 128-bit half-collision, the 136-bit
class residual search (`residual-search`), and the shared-seed `S5`-fixed
early-test and schedule audit (`resident-audit`) at finite scale; reaching the
full 256-bit event (`R = 0` at rate `2^-117`) requires the heuristic
extrapolation of H1 and H2. With the uniform rate
in place of 2,048 times it, the same search needs 2^127 trials and gives
time_log2 = 123.4.

No full 2-round collision is exhibited, and the search is far beyond feasible
computation. What is exhibited, and checked by the organizer's own runner, is
the exact half-collision on trials of the search and a toy-scale run of the
class search, without the early test and the packing that set the cost of a
trial. The program the organizer runs also contains the packed batch, a
machine that counts its operations and loads, and a self-test of that count
(Section 6.5). Those counts are the program's own; the organizer does not
check them.

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

    X3 = a6c3b8c5   X7 = 793c473a   X11 = 5c32535c   X15 = 8367c7bb
    W4 = 60000001   W13 = 29bd3f58

Then K + W4 = bbf2cd1e and W4' = ((K + W4) XOR 2) - K = 5fffffff, so
W4 - W4' = 00000002. Evaluate C3 = G(3,7,11,15, w4, W13) on the inputs
(X3, X7, X11, X15) with w4 = W4 and with w4 = W4':

    w4 = W4    a1=80000000 d1=c7bb0367 c1=23ed56c3 b1=1f95ad11
               a2=c952ec69 d2=0e0ee9ef c2=31fc40b2 b2=465cd3db
    w4 = W4'   a1=7ffffffe d1=3845fc98 c1=94784ff4 b1=8ceed440
               a2=36ac1396 d2=0e0ee9ef c2=a28739e3 b2=465cd3db

**Fact P.** The two executions give the same d output 0e0ee9ef and the same b
output 465cd3db. They differ in the a output (c952ec69, 36ac1396) and in the c
output (31fc40b2, a28739e3). This is a finite computation on the displayed
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

**Step S2.** w4' = W4' and w5' = w5 + W4 - W4'.

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
of E3 is e1 = Y3 + Y4 for message A and e1' = Y3' + Y4 for message B, with
Y3 = c952ec69 and Y3' = 36ac1396 from Fact P. Put DY3 = Y3' - Y3 = 6d59272d.
The second assignment is h1 = ROR(Y14 XOR e1, 16), so the XOR difference
between A and B of E3's first-half d value is

    eta = h1 XOR h1' = ROR((Y3 + Y4) XOR (Y3 + Y4 + DY3), 16),

a function of Y4 alone. Fix eta = e96d6d6b. The *class* is the set of all
words Y4 that give this eta.

**Lemma Q.** The class is the set of all Y4 with

    ((Y3 + Y4) AND 6d6be96d) = 00096120.

It has 4,096 members: the 12 bits of e1 = Y3 + Y4 at the positions where
6d6be96d has a zero are free, and Y4 = e1 - Y3.

Proof. Put x = ROL(eta,16) = 6d6be96d; Y4 is in the class exactly when
e1 XOR (e1 + DY3) = x, that is when (e1 XOR x) - e1 = DY3. For words e and x,
(e XOR x) - e is the sum over the bits i of x of 2^i where bit i of e is 0
and of -2^i where it is 1, which is 2 ((NOT e) AND x) - x. So the condition
is 2 ((NOT e1) AND x) = DY3 + x modulo 2^32. Here DY3 + x = dac5109a is even,
and doubling discards bit 31, which x does not have, so the condition is
((NOT e1) AND x) = dac5109a >> 1 = 6d62884d. All bits of 6d62884d lie in x,
so this fixes the 20 bits of e1 on x to (e1 AND x) = (NOT 6d62884d) AND x =
00096120 and leaves the other 12 bits free. QED.

Member number k of the class, for 0 <= k < 4096, is the Y4 whose e1 has the
bits of k at its 12 free positions, in increasing order of position.

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
one of the 2^288 pairs of Section 5, picked so that its Y4 lies in the class.

**6.2 The residual of a trial.** With Y3, Y3', Y11, Y11' the a and c outputs of
C3 from Fact P (c952ec69, 36ac1396, 31fc40b2, a28739e3),
delta = W4 - W4' = 00000002 and the trial's words and state:

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

**6.3 An early test on 32 bits.**

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

The test needs only the first five assignments of E1 and the first four of E3
for both messages. For a trial of 6.1 two of them cost almost nothing:
h1' = h1 XOR eta, because h1 XOR h1' is the constant eta for every Y4 in the
class, and f1 XOR f1' = ROR(g1 XOR g1', 12), because f1 = ROR(Y4 XOR g1, 12)
and f1' = ROR(Y4 XOR g1', 12) have the same Y4.

**6.4 Algorithm.**

1. Draw one fresh uniform 256-bit word and take from it the four words
   X2, X5, X6, X9. Set X1 = X10 = 0: every trial replaces X1, and the D0
   family replaces X5 and X10 and keeps S5, which the drawn X5 determines.
2. For each of the 2^72 values of (X12, X13, X14) with X12 < 2^8, in a fixed
   order: run step S1 to get a context. For each of the 2^32 values of alpha:
   compute the D0 family, the first half of C0 and the per-alpha constants.
   Then evaluate the early test for the 4,096 members of the class in the
   order of their numbers, seven members in one packed word (6.5).
3. For every trial that passes the early test, compute its words by 6.1 and
   R in full. If R = 0, build A and B by steps S2 and S3 from the trial's
   words, evaluate H(A) and H(B), check that they agree, output (A, B) and
   halt.
4. Halt with failure if 2^104 trials have passed the early test without
   R = 0, or when all trials are exhausted.

The trials are 2^72 * 2^32 * 2^12 = 2^116 half-colliding pairs by Lemma T,
and they are distinct. Two contexts differ in X12, X13 or X14, which no trial
changes, so their trials have different states X and different words. Trials
of one context with different alpha differ in X10 = alpha. Trials of one
context and one alpha with different members differ in Y4, which is a
function of the words.

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
alpha and are seven consecutive members of the class. The members enter
through two lists that do not depend on the context: for batch j, U[j] holds
ROL(y,7) and V[j] holds Y3 + y modulo 2^32, one member y per lane. Each list
has 586 packed words, because 4096 = 585 * 7 + 1; the six spare lanes of the
last word repeat its member. The lists are computed once, before step 2. The
batch computes in every lane, in the names of 6.1 to 6.3:

- C0 backwards: Y8 = U[j] XOR pb, Y12 = Y8 - pc, Y0 = ROL(Y12,8) XOR pd and
  ka = Y0 + (IV[3] + IV[7] - pa - pb), which is IV[3] + IV[7] + w6.
- K3: kd, kc, kb, S11, S15 = S11 - kc, S3, and the first value of C2,
  v = X2 + X6 + w7, as S3 - (ka + kb) + (X2 + X6).
- D1: d = (X11 - X12) - S11, X1 = ROL(X12,8) XOR d and a = ROL(d,16) XOR S12.
- C1: its first seven assignments. The first is X1 + (X5 + w3) and the fifth
  is the sum of the first, the fourth, a and the constant -S1 - S6, since
  w10 = a - S1 - S6. The fifth and seventh values are Y1 and Y9.
- C2: its other seven assignments. The sixth and the eighth are Y14 and Y6.
- E1 on A and B: a1, d1, c1, c1', b1, b1', a2, a2'.
- E3 on A and B: h1 = ROR(Y14 XOR V[j], 16), h1' = h1 XOR eta, g1 = Y9 + h1,
  g1' = Y9 + h1' and f1 XOR f1' = ROR(g1 XOR g1', 12).
- The early test: t = a2 XOR a2', the word (f1 XOR f1') XOR t XOR ROR(t,1),
  and whether that word is zero in some lane.

The words w6, w7 and w10 are never formed on their own, and w8, w9, w11 and
w14 are not needed for the early test: step 3 computes them for the trials
that pass.

*No lane overflows.* Rotation outputs, list entries and constants are below
B = 2^32, and an XOR is never longer in bits than its operands. Every sum
formed in the batch is below 10 B, which is below 2^36, so no carry leaves a
lane. In detail: Y12 and ka are below 2B. In K3, kc is below 2B, S15 below
3B, ka + kb below 3B, its complement (ka + kb) XOR M below 4B and v below 6B.
In D1, d and X1 are below 2B. In C1 the sums are below 3B (first), 2B, 6B
(Y1, a sum of a value below 3B and three values below B) and 3B (Y9). In C2
they are below 2B, 8B (the fifth assignment, v plus two values below B) and
3B. In E1 they are below 8B (a1 = Y1 + Y6 + w12), 2B, 2B and 10B (the two
a2). In E3, g1 and g1' are below 4B. Since every lane stays below 2^36, the
low 32 bits of every lane equal the scalar value modulo 2^32, and XOR and
PROR read only those bits.

*Operation count of one batch.* The batch runs on a load/store machine with
16 registers. The second column counts additions, XOR, AND, OR, shifts, the
comparisons and the branches, with PROR = 5. The third column counts memory
traffic: every constant operand, that is a per-context or per-alpha constant,
a list entry, a rotation mask or the mask M, is fetched from memory each time
it is used and charged as one load. Shift distances are fixed in the
instruction.

| Part | What is computed | Operations | Loads |
| --- | --- | ---: | ---: |
| loop | next list position, end test, branch | 3 | 1 |
| C0 backwards | Y8 (1), Y12 (1), Y0 (6), ka (1) | 9 | 7 |
| K3 | kd (6), kc (1), kb (6), S11 (1), S15 (3), S3 (6), v (4) | 27 | 14 |
| D1 | d (2), X1 (1), a (6) | 9 | 6 |
| C1 | first (1), d1 (6), c1 (1), b1 (6), Y1 (3), d2 (6), Y9 (1) | 24 | 11 |
| C2 | d1 (6), c1 (1), b1 (6), fifth (2), Y14 (6), c2 (1), Y6 (6) | 28 | 12 |
| E1, A and B | a1 (2), d1 (6), c1 c1' (2), b1 b1' (12), a2 a2' (4) | 26 | 11 |
| E3, A and B | h1 (6), h1' (1), g1 g1' (2), f1 XOR f1' (6) | 15 | 6 |
| early test | t, word (8), reduce, flags (3), compare, branch (2) | 13 | 6 |
| | total for seven trials | 154 | 74 |

So a batch is 154 + 74 = 228 primitive operations. No store is needed: the
list position stays in a register across batches, and at most 10 batch values
are live at any point, so they fit in the 16 registers.

Each XOR followed by a rotation is 6 operations, a two-term sum 1, a
three-term sum 2 and a difference of two lanes 3; a rotation loads its two
masks. For example K3 is: ka XOR 11 and rotate (6), + IV[3] (1), XOR IV[7]
and rotate (6), XOR ROL(S7,7) (1), S11 - kc (3), rotate S15 and XOR kd (6),
and for v the sum ka + kb (1), XOR M (1), + S3 (1), + (X2 + X6 + 1) (1): 27
operations, with loads for 11, IV[3], IV[7], ROL(S7,7), M, 1, M, X2 + X6 + 1
and three mask pairs: 14. The loads of C0 backwards are U[j], pb, -pc, pd,
the constant IV[3] + IV[7] - pa - pb and one mask pair; those of E3 are
V[j], eta and two mask pairs. The loop advances the list position, compares
it with the end of the lists, which is loaded, and branches. In the early
test, t is one XOR and the word two XORs and one PROR (8); the word is
reduced by an AND with M, and the flags are formed by adding 2^32 - 1 to
every lane and selecting bit 32 of every lane, which is set exactly in the
lanes whose word is nonzero (3); the flags are compared with a loaded
constant and the batch ends with a branch (2).

The per-alpha constants are seven: pb, -pc, pd and IV[3] + IV[7] - pa - pb
for C0, X5 and X5 + w3 for C1, and alpha for C2.

*The count in the submitted program.* The program of the two declared
experiments, experiments/halfsearch.py, contains this batch and the machine
that counts it. A packed word is one integer with seven 36-bit lanes. Every
addition, XOR, AND, OR and shift of packed words is a call that adds one
operation, every constant operand and list entry is fetched by a call that
adds one load, and the two comparisons and the two branches add one
operation each. The batch is written with these calls only; forming the
constants and the two list words is not part of it. The command

    python3 experiments/halfsearch.py --selftest N [seed]

runs N batches. The nine context words, alpha and the list position of a
case come from SHAKE-256 of the seed text (default 1) and the case number.
Every fourth case is the last batch of the class, and in every fifth case
each context word and alpha is 0, 2^32 - 1 or as drawn. In each of the
seven lanes the reduced test word and its flag are compared with the test
word of Lemma E computed in 32-bit arithmetic, forwards from the trial's
message words: C0, C1 and C2 in full, then the first halves of E1 and E3
for both messages as written in 6.2 and 6.3, without h1' = h1 XOR eta and
the other shortcuts of the batch. The program prints one JSON line: the
number of cases, the lanes checked and the lanes equal, the operations and
loads of every part and in total, whether they are the same in every case
and equal to the table above, for every part the largest lane of a sum
next to the bound quoted above, the largest number of registers in use at
one time, the number of per-context and per-alpha constants, the number of
class members in the two lists, and for how many patterns of zero and
nonzero lanes the flags are right. Its exit status is 0 only if all of
these agree with this section.

With N = 2000 and seed 1 it reports 14,000 of 14,000 lanes equal; 154
operations and 74 loads, per part as in the table and the same in every
case; largest sums of 1.982, 4.913, 1.996, 5.597, 6.565, 8.774 and 3.936
times 2^32 in C0 backwards, K3, D1, C1, C2, E1 and E3, below the bounds 2,
6, 2, 6, 8, 10 and 4; 14 per-context and 7 per-alpha constants; 4,096
members in the 586 words of a list; and at most 10 registers in use. The
register figure follows every value, loaded constants and the intermediate
values of a rotation included, from the step that makes it to its last
use, with the operations in the order of the program, and adds one
register for the list position. None of the 14,000 test words of that run
is zero, so the flags are also formed for all 128 patterns of zero and
nonzero lanes: all 128 are right.

In the declared experiment `residual-search` the same program evaluates one
batch per organizer seed, for that seed's context and alpha and the list
position that holds the first member tried, and returns its operations, its
loads and its number of equal lanes as observations. The organizer's runner
records observations as untrusted and does not recompute them. The
self-test and these observations therefore show what the program in the
package counts, and that its lanes agree with its own scalar computation.
They are a participant check, not an organizer verification of the cost.

## 7. Success probability

The probability space is the one uniform 256-bit word of step 1, for the
fixed target. The algorithm is otherwise deterministic. The trials depend on
that word only through the four words X2, X5, X6, X9.

**Heuristic H1 (score-critical).** Over the coins, the 2^116 trials behave
with respect to the event R = 0 like independent events of probability at
least 2^-117 each, to the extent that the probability that no trial has R = 0
is at most exp(-1/2) + 0.002. The rate 2^-117 is 2,048 times the rate of a
uniform 128-bit value. The factor 2,048 is assumed. Section 10 describes
what it is set against: for Y4 in the class, an estimated lower bound of
7,319 with standard error 816 under the seven-word model, from a participant
computation. The organizer-run experiments do not measure the factor.

**Heuristic H2 (supporting).** With probability at least 0.999 over the
coins, fewer than 2^104 of the 2^116 trials pass the early test of Lemma E
without having R = 0. (The budget corresponds to a pass rate of 2^-12. The
pass rate measured on real trials of the class search is 2^-29.6, which
would give 2^86.4 passes, below the budget by a factor of 2^17.6. That the
number of passes of one run stays near this mean is part of the assumption;
Section 10 reports eight runs of 2^37 trials in support.)

Under H1 and H2 the algorithm outputs a collision with probability at least
1 - exp(-1/2) - 0.002 - 0.001 > 0.3934 - 0.003 = 0.3904 >= 0.39. When it
outputs a pair, the pair is a genuine collision: step 3 checks both complete
digests, and the messages have different lengths.

*Sensitivity to the factor.* If the rate is f * 2^-128, the 2^116 trials
give 1 - exp(-f/4096) - 0.003 with the same allowances, which reaches 0.39
only for f >= 2,045: the assumed 2,048 leaves no slack on the probability
side. The margin of the claim lies between the assumed 2,048 and the
estimated 7,319. For a general f the same success probability needs
2^127 / f trials and, at the same 34 operations per trial,
time_log2 = 123.34 - log2 f: that is 112.34 at f = 2,048, and 123.34 at
f = 1, the uniform rate, where 34 * 2^127 / 430 = 2^123.33927 and the
package would submit 123.4.

Neither heuristic is proved. Section 10 lists the evidence and its limits.

## 8. Charged time

One 2-round target compression costs one unit and every other primitive word
operation costs 1/C units with C = 430.

- **Main loop.** For one context and one alpha the 4,096 members take 586
  batches: 585 full ones and one that holds the last member and is charged
  in full. A batch is 228 primitive operations by 6.5, memory loads included,
  so the batches cost 586 * 228 = 133,608 operations. The work per alpha
  before the batches is the D0 family and the first half of C0 (below 40
  operations), the seven per-alpha constants of 6.5, each placed in seven
  lanes (12 operations) and stored, and the loads of the context words read:
  below 256 operations. One alpha therefore costs below 133,864 operations.
  It is charged 34 * 4096 = 139,264, that is 34 per trial; the difference of
  about 5,400 operations per alpha, 4%, is margin. The main loop costs at
  most 2^116 * 34 operations.
- **Per context.** Step S1 is below 2^10 operations. Placing the 14
  per-context constants of the batch in seven lanes and storing them is
  14 * 13 = 182 more. Together they are below 2^11 operations. There are
  2^72 contexts: 2^83 operations.
- **Lists.** The two lists of 6.5 are computed once from eta and Y3: 4,096
  members at fewer than 64 operations each, 2^18 operations.
- **Early-test passes.** At most 2^104 are processed (step 4). The batch
  keeps no values of a passing trial, so the trial is recomputed in scalar
  form from its member number: its words by 6.1, the calls C1 and C2, E1
  and E3 for both messages, and the comparison of R. That is below 2^10
  operations each, loads included: 2^114 operations, a share 2^-7.09 of
  the main loop.
- **Final step.** Steps S2, S3 and two complete hash evaluations with their
  input handling: below 2^11 operations and 2 units, once.
- **Randomness.** One random word, charged as one operation.
- **Preprocessing.** The six constants of 3.2 and the word eta of 6.1 are
  stored in the program. The constants were produced by a solver run of
  under one second and selected among 4,140 such sets, and eta was selected
  among the classes of those constants, by the measurements of Section 10,
  which used fewer than 2^60 primitive operations in total. As a bound for
  recomputing a valid set of constants that does not depend on that solver,
  exhaustive search over (w4, w13) for the four fixed inputs finds the
  constants with at most 2^64 candidates at two G evaluations and a
  comparison each, below 128 operations: 2^71 operations, below 2^63 units.

Total:

    T <= (34 * 2^116 + 2^114 + 2^83 + 2^60 + 2^18 + 2^11 + 1) / 430
         + 2 + 2^63
       <  34 * 2^116 * (1 + 2^-7) / 430 + 2^64
       <  2^112.3506 + 2^64
       <  2^112.36.

Here 34 * 2^116 / 430 = 2^(116 + 5.08746 - 8.74819) = 2^112.33927. The
terms after the first add up to less than 2^114.01, which is below
34 * 2^116 * 2^-7 = 2^114.087, and log2(1 + 2^-7) < 0.01123. The submitted
bound is time_log2 = 112.4, a factor of about 1.03 above this total. This
is a worst-case bound for the algorithm as stated, which halts within these
budgets on every run.

No sorting or lookup is charged because the algorithm has none: a trial is
tested against zero, not against other trials. The only stored lists are the
two fixed lists of class members of 6.5, which are read in order; their loads
are among the 74 of a batch.

## 9. Memory, preprocessing and advice

The program is the step S1 formulas, the trial of 6.1, the packed batch of
6.5 and a compression routine for the final check. Bound the code by 4096
instruction templates of at most four 256-bit words each: 2^14 words, which
is 2^19 bytes. Data is the context (48 words), the per-context and per-alpha
constants in packed form (below 32 words), the masks and the fixed constants
(below 32 words), the two lists of class members (1,172 words), the batch
temporaries (below 64 words) and the two messages and digests of the final
check: fewer than 1,536 words, below 2^16 bytes. Peak memory is therefore
below 2^19 + 2^16 < 2^20 bytes. Nothing grows with the number of trials.

preprocessing_log2 = 63 is the bound of Section 8 for recomputing the six
constants; it also covers their selection and the selection of eta, and it is
included in T. nonuniform_advice_log2_bytes = 5 covers the 28 bytes of the
six constants and eta. The lists of 6.5 are not advice: the program computes
them from eta and Y3 by Lemma Q. There is no other stored data and no stored
collision.

## 10. Evidence, scope and field meanings

**What is exact.** Sections 2 to 5 and Lemmas Q, F, Y, K, T and E. The
declared experiment `half-collision` runs one trial of 6.1 per organizer
seed, with nine state words, alpha and a member number taken from the seed,
and the organizer recomputes both digests; Lemma T predicts that every trial
agrees on the 128 masked digest bits.

**The seven-word model.** By 6.2 the residual of a trial is a function of
the constants and of seven 32-bit words: for E1 its first-half values d1 and
b1 and its a output a2 on message A, and for E3 the words Y4, Y9, w8 and its
first-half value h1 on message A. (E1's a1 and d1 are the same for A and B,
so a1 enters only through d1 and a2; each of the seven words is a bijective
image of one input or message word of its call when the others are fixed.)
In the algorithm Y4 takes every member of the class equally often. The model
M says that over the trials the other six words behave like independent
uniform words, independent of Y4. Under M a trial has R = 0 with probability
r * 2^-128, where r * 2^76 is the number of solutions of R = 0 among the
2^204 values of the seven words with Y4 in the class. Call r the *class
rate*. H1 is M together with r >= 2,048.

**How r was estimated (participant computation, not organizer-verified).**
Write tau, eps for the XOR differences between A and B of E1's a and c
outputs and beta for that of its first-half b. As in the proof of Lemma E,
E1's d and b output differences are ROR(tau, 8) and ROR(beta XOR eps, 7),
and E3's d and b output differences are ROR(eta XOR eps', 8) and
ROR(psi XOR tau', 7), where eta, psi are the XOR differences of E3's
first-half d and b and tau', eps' those of its c and a outputs. So R = 0
holds exactly when tau' = tau, eps' = eps, psi = tau XOR ROR(tau, 1) and
eta = eps XOR ROL(beta XOR eps, 1). For Y4 in the class the left side of the
last equation is the constant e96d6d6b, so that equation is a condition on E1
alone. Say that a value of (d1, b1, a2) *requires* the class if it holds.

1. beta is a function of d1 alone: with c1 = Y11 + d1 and
   DY11 = Y11' - Y11 = 708af931, beta = ROR(c1 XOR (c1 + DY11), 12). As in
   Lemma Q, the d1 with a given beta are those for which c1 has prescribed
   bits on the mask ROL(beta,12) AND 7fffffff; they are a share 2^-k of all
   d1, where k is the number of bits of the mask. For one beta, draw d1
   uniformly among those values and b1, a2 uniformly, and keep the draws
   that require the class.
2. For a kept draw, count the quadruples (Y4, h1, Y9, w8) for which E3
   produces eta, psi, eps and tau; all of them have Y4 in the class. For
   a word x and a mask m, (x XOR m) - x is the signed sum over the bits i of
   m of (1 - 2 x_i) 2^i, so an addition whose XOR output difference is
   prescribed fixes the bits of its result on that mask once its additive
   input difference is known. E3 has four such additions. Their additive
   differences are the constant Y3' - Y3 and three signed sums (over the
   bits of eta, psi and ROR(eta XOR eps, 8)); the admissible values of those
   three are enumerated with a carry automaton, and for each choice the
   number of completions is a product of two carry automata, one for Y4
   against e1 = Y3 + Y4 and one for g1 + h2. When the enumeration exceeds a
   work budget a uniform random subset is used with the matching weight, so
   that the result is unbiased by construction. The value for such a draw
   is then an estimate and not a count, and a zero estimate does not prove
   a zero count. Necessary conditions for a nonzero count, one per addition
   (that an admissible additive difference exists at all), are tested
   first.
3. For one beta let m be the mean of that value over all its draws, with
   zero for the draws not kept. Then r = 2^20 times the sum over all beta
   of 2^-k * m: the sum of the counts over all 2^96 values of (d1, b1, a2)
   is r * 2^76, and 2^96 / 2^76 = 2^20. Counts are not negative, so the sum
   over any set of betas that is fixed before the draws is a lower bound
   for r, and its estimate from the draws is unbiased. Where a beta has
   more than 3,000 kept draws, 3,000 of them are counted, in the order in
   which they were drawn, and their sum is scaled up.

The class and the betas were chosen on other draws than the ones that give
the quoted figure.

- *First sample.* 2^40 uniform draws of (d1, b1, a2), counted by step 2 for
  the eta that each draw requires. 4,245 draws had a nonzero value, 993 of
  them a random-subset estimate; they require 4,194 different classes.
- *Second sample.* 2^45 fresh uniform draws. The 76,274 of them that passed
  the necessary conditions and require one of those 4,194 classes were
  counted, 30,879 of them with the random subset; 2,683 had a nonzero
  value. The 24 classes with the largest sum of values relative to their
  size in this sample, among the classes with at least two nonzero values,
  were measured in a small pass of the third sample (2^36 draws per beta,
  for the betas that had a nonzero value).
  The 18 classes whose sum in that pass exceeded 200 were kept as
  candidates, each with the list of betas that occurred with it in the
  second sample. For the class e96d6d6b there were 45 such draws, 2 with a
  nonzero value, and 22 betas.
- *First pass.* Steps 1 to 3 with 2^36 fresh draws for every beta of every
  candidate, 533 pairs in all. The two largest sums were 3,389 with
  standard error 924 for the class e96d7579 and 2,404 with standard error
  831 for e96d6d6b, the second from 256 kept draws that passed the
  necessary conditions, 13 of them with a nonzero value. A smaller pass
  before this one, over the betas that had a nonzero value in the second
  sample, had given 9,472 with standard error 4,793 for e96d6d6b, from one
  beta and 10 nonzero values.
- *Second pass.* The eight classes with the largest sums of the first pass
  were measured again by steps 1 to 3 with 2^41 fresh draws per beta, for
  the 66 betas that had contributed at least 0.05 to a sum of the first
  pass. Classes and betas were fixed before the pass. The table below gives
  the sums. For e96d6d6b the three betas are 953908d0 (k = 11) with 6,218
  and standard error 772, 953f08d0 (k = 13) with 949 and 95, and 95390bd0
  (k = 13) with 6 and 2; the largest single value is about 4% of the sum
  of its beta.
- *Third pass.* e96d6d6b is the largest of eight in the second pass, and
  the largest of several noisy figures is biased upwards. It was therefore
  measured once more, with the same three betas and 2^41 fresh draws per
  beta from a new seed: 7,319 with standard error 816, from 417 nonzero
  counts (6,168, 1,140 and 11 for the three betas). The constants, the
  class and its betas were fixed before these draws, so this figure is
  free of the selection, and it is the one quoted for r. The second pass,
  7,173, agrees with it. The class e96d7579 was measured again in the same
  pass, with its six betas: 2,995 with standard error 163.
- *Eight further seeds.* The measurement of the third pass was then
  repeated with eight more seeds, each with the same three betas and 2^41
  fresh draws per beta. The sums are 6,888, 5,946, 7,785, 6,155, 7,630,
  7,628, 7,074 and 6,918, each from 407 to 433 nonzero values: mean 7,003,
  smallest 5,946, largest 7,785. The standard deviation of the eight sums
  is 682, in line with the standard errors of 566 to 831 computed for the
  single passes, and it gives the mean a standard error of 241. With the
  second and the third pass these are ten passes of 2^41 draws per beta,
  all between 5,946 and 7,785. The figure quoted for r stays the 7,319 of
  the third pass; the eight-seed mean is lower and has the smaller error.
  Only the sums and the numbers of nonzero values of these eight passes
  are used here; how often the random-subset branch was used in them was
  not examined.

What was counted in the third pass for e96d6d6b: 5,388 kept draws (1,733,
3,000 and 655 for the three betas). The 417 nonzero values are all counts
made in full; none of them came from the random-subset branch of the
counting program, so no part of the 7,319 is an estimate of that branch.
The branch was used for 915 of the other 4,971 draws, and each of these
gave the estimate zero. Because a zero estimate does not prove a zero
count, 80 of the 915 were drawn at random and given to a SAT solver: all 80
have no solution. Several draws can require the same E3 system, and the 80
draws are 52 different systems. The other 835 were not checked one by one.
Since every value of the branch in this pass is zero, the branch cannot
have raised the figure; solutions that it missed would make the true sum
larger. For the second pass, for the earlier passes and for the other
classes of the table, how often the branch was used was not examined.

| Class, second pass | Betas | Nonzero values | Sum | Standard error |
| --- | ---: | ---: | ---: | ---: |
| e96d6d6b | 3 | 430 | 7,173 | 778 |
| e96d7579 | 6 | 1,185 | 3,337 | 189 |
| e95f75e9 | 8 | 1,292 | 2,402 | 97 |
| e95775b9 | 10 | 867 | 1,893 | 136 |
| e97375af | 5 | 665 | 1,501 | 86 |
| e95373b9 | 8 | 1,013 | 1,369 | 76 |
| e96d956b | 4 | 221 | 846 | 104 |
| e8d5f5eb | 22 | 1,914 | 418 | 22 |

The class e96d6d6b is used because it has the largest estimated rate. H1
assumes 2,048 where the estimate is 7,319 with standard error 816: 28% of
the estimate, and more than six of its standard errors below it. Against
the eight further seeds, 2,048 is 3.4 times below their mean and 2.9 times
below the smallest of them.

A standard error here is the square root of the sum of the squared values,
scaled like the values.

*Selection.* Two things were selected by measurements of this kind: the six
constants, as the best of 4,140 farmed sets, and the class, among the
classes seen in the samples. Two figures were obtained after the selection
that concerns them, on fresh draws with a new seed: the 10.6 of the first
sample, quoted below, after the constants were chosen; and the 7,319 of the
third pass, after the constants, the class and its three betas were fixed.
The eight further seeds are fresh draws after the same choices as well.
The other figures are not free of selection. Every class of the table is
there because its first-pass sum was among the eight largest, and e96d6d6b
was chosen because its second-pass sum, 7,173, was the largest of the
eight, so the sums of the first and second passes are biased upwards. The
three betas were chosen on the first pass. Smaller earlier runs on these
constants include the run by which the constants were chosen; they are
biased upwards by that choice and are not quoted.

For comparison, the mean value of the first sample over all its draws is the
rate of a search that does not restrict Y4, in the same units: 10.6 with
standard error 1.3 (eight disjoint parts of 2^37 draws gave 7.2 to 18.0).
Of its 2^40 draws, 217,243 passed the necessary conditions and were
counted; for 84,443 of them the random subset was used, and those carry
13.3% of the sum (third check below). The class is a share 2^-20 of all Y4.
The value is heavy-tailed in both settings: in the first sample the 50
largest of the 4,245 nonzero values carry 63% of the sum.

The unrestricted estimate was repeated on another machine, as support for
the count under the model and not for the class rate. An agent of another
model ran the same programs there on RTX 3070 cards, with another seed and
2^39 draws: 13.5 with standard error 3.7 for the constants of 3.2, against
the 10.6 with standard error 1.3 above; the two agree within their errors.
In that run 109,179 draws were counted, 55,707 of them with the random
subset, and 2,044 had a nonzero value. It repeats the estimate on other
hardware and other draws with the same counting program; it is not an
independent implementation, and it says nothing about a single class.

**Checks of the count (participant computations).** One counting program
produced every figure of this section. Its first four checks below were made
on uniform draws, not on draws of the class. The 80 draws of the third pass
above and the fifth check concern the class.

First, for 30 outcomes of uniform draws, 20 with counts between 2^15 and
2^32 and 10 with count zero, the same E3 system was encoded as CNF and given
to a SAT solver and to the approximate model counter ApproxMC (tolerance
0.4, confidence 0.9). The 10 were unsatisfiable and the 20 counts agreed
within 0.07 bits. All 30 were outcomes enumerated in full: this check skips
every outcome that used the random subset.

Second, the counting program, compiled for 8-bit words, returned exactly the
brute-force count on each of 400 random constant sets of the scaled-down
hash described below. With 8-bit words the lists stay far below the work
budget, so that build cannot reach the random-subset branch on any set.

Third, a check of the random-subset branch on the first sample, the
unrestricted run of 2^40 draws. Of the 84,443 draws that used the branch,
993 have a nonzero estimate and 83,450 the estimate zero. Three groups of
them were given to the SAT solver and to ApproxMC with the same settings.
For the 40 largest estimates, which carry 10.0% of the sum of the sample,
the sum of the estimates is 0.986 times the sum of the independent counts;
the log2 differences have mean +0.15 and standard deviation 0.39 and lie
between -0.86 and +1.32. For 100 others drawn at random among the nonzero
estimates the ratio of the sums is 1.050; the log2 differences have mean
+0.26 and standard deviation 1.12 and lie between -2.81 and +4.92, so a
single estimate can be far off while the sums agree. All 100 outcomes drawn
at random among the zero estimates are unsatisfiable. This check covers 240
of the 84,443 outcomes of the branch.

Fourth, the same for the outcomes of the first sample that were counted in
full: 3,252 with a nonzero count and 129,548 with zero, which carry 86.7%
of the sum. For the 40 largest, which carry 55.0% of the sum and include
the largest count 2^39.6, the sum of the counter's values is 1.005 times
the sum of the independent counts, and the log2 differences have standard
deviation 0.05 and lie between -0.08 and +0.10. For 60 further nonzero
counts drawn at random the ratio of the sums is 1.000, and the log2
differences have standard deviation 0.03 and lie between -0.08 and +0.08.

Fifth, the counts behind the class rate itself: the 417 nonzero values of
the third pass for e96d6d6b, all counts made in full. 100 of them were given
to the SAT solver and to ApproxMC with the same settings, and all 100 were
counted. For the 40 largest, which carry 45.6% of the sum of the class, the
sum of the counter's values is 1.027 times the sum of the independent
counts, and the log2 differences lie between -0.08 and +0.07. For 60 further
ones drawn at random the ratio of the sums is 0.969, and the log2
differences lie between -0.15 and +0.08.

What these checks mean for the class rate. The 417 nonzero values behind
the 7,319 are counts made in full, the code path of the first, second and
fourth checks. By the fifth check 100 of those 417 values, among them the 40
largest with 45.6% of the sum, were themselves confirmed by the independent
counter, with ratios of sums of 1.027 and 0.969; the other 317 were not.
The random-subset branch enters the 7,319 only through 915 zero estimates,
of which 80 were confirmed. All of these checks are participant
computations.

**Checks of the trial on real messages (participant computation).** A host
program built the messages of 16,384 random trials of 6.1 in the class of
this package, and of 16,384 in each of the classes e96d7579 and e95f75e9,
and evaluated the complete 2-round hash of both messages of every trial: all
agree on digest words 0, 2, 5 and 7, have Y4 in their class and the pinned
words in place, and have the residual that 6.2 computes. A second program,
written independently from the text of this proof, checked each of Lemmas Q,
F, Y, K and T on 20,000 random trials in the class of this package against
a plain forward compression.

**Checks of the model on real messages (participant measurement).** Real
trials of 6.1 were compared with the same number of draws from M (Y4 a
uniform member of the class, the other six words uniform and independent),
on the same statistics: how often each of the four residual words, or its
low 16 bits, is zero, how many trials have a residual of weight at most 32
or at most 40, and how often the early test of Lemma E passes.

In the four comparisons that follow, the real trials are not laid out as in
6.4. Every thread of the generating program draws its own context, nine
random state words from a random stream of its own, independent of the
other threads, and makes 4,096 trials in it, each with a random alpha and a
random member of the class. No two contexts share seed words, and X12 is
not restricted. These comparisons therefore measure rates averaged over
independent contexts. They do not test a run of 6.4, in which all contexts
share the four seed words. A measurement in that layout comes after them.

For the class of this package, with 2^42 trials of each kind (real messages
/ model): early test passes 5,498 / 5,463; the four residual words zero
1,042, 987, 1,012, 986 / 1,031, 982, 1,033, 1,032; residual of weight at
most 32: 50,055 / 50,408; of weight at most 40: 78,467,681 / 78,463,488; all
four residual words with a zero low byte: 1,008 / 1,008. Among all the
statistics that the two programs print for this class, the largest deviation
is 1.5 standard deviations, real messages higher (at least 28 trailing zero
residual bits: 16,402 / 16,135).

The same comparison was made for two other classes and for the search that
does not restrict Y4. The figures are again real messages / model.

- Class e96d7579, 2^42 trials of each kind: early test passes 8,822 /
  8,712; the four residual words zero 878, 1,431, 994, 1,018 / 822, 1,381,
  1,037, 1,038; residual of weight at most 32: 61,018 / 61,006; of weight
  at most 40: 90,510,112 / 90,501,817; all four residual words with a zero
  low byte: 934 / 1,048, the largest deviation of this run, 2.6 standard
  deviations. The second residual word is zero more often than a uniform
  word would be (1,024 expected), on real messages and in the model alike.
- Class e95f75e9, 2^40 trials of each kind, without a count of early-test
  passes: the four residual words zero 207, 235, 233, 232 / 227, 275, 286,
  237, in total 907 / 1,025, the model higher by 2.7 standard deviations;
  weight at most 32: 18,953 / 19,329; weight at most 40: 25,343,736 /
  25,342,577.
- No restriction on Y4, 2^40 trials of each kind: early test passes 2,350 /
  2,381; the four residual words zero 249, 283, 273, 263 / 201, 264, 276,
  292; weight at most 32: 11,748 / 11,940; weight at most 40: 19,910,536 /
  19,904,766; the low 16 bits of the first and third residual words both
  zero: 632 / 748, the model higher by 3.1 standard deviations. That is the
  largest deviation among all the statistics the programs print for these
  three runs.
- No restriction on Y4, a second run with 2^42 trials of each kind: early
  test passes 9,337 / 9,310; the four residual words zero 954, 1,043,
  1,032, 1,092 / 977, 1,042, 1,042, 1,085; weight at most 32: 48,586 /
  48,623; weight at most 40: 79,620,594 / 79,647,116; the low 16 bits of
  the first and third residual words both zero: 2,778 / 2,553, real
  messages higher by 3.1 standard deviations, again the largest deviation
  of the run.

A standard deviation here is the square root of the sum of the two counts.
Each run compares about twenty statistics, which are not independent of one
another. For the class of this package the largest deviation is 1.5. In
the four other runs the largest deviations are 2.6, 2.7, 3.1 and 3.1; a
single 3.1 has a probability of about one in ten somewhere among some sixty
comparisons, and in the first unrestricted run the model count 201 for the
first residual word is itself 3.4 standard deviations below the 256 of a
uniform word.

The two unrestricted runs show the same pair statistic 3.1 standard
deviations off in opposite directions: the model higher at 2^40 trials,
real messages higher at 2^42. So this is not a consistent bias of real
messages against M. It is a spread between runs that is larger than a
Poisson count allows: scaled to 2^40 trials, the real figures are 632 and
695, which are 2.2 standard deviations apart, and the model figures are 748
and 638, which are 3.6 apart. A count that varies from run to run by more
than its Poisson error is what dependence between trials would produce, so
this bears on the independence that H1 assumes. Here the larger spread is
in the model draws, which are independent by construction, so it may as
well be chance or a property of the sampling program. It is under study
and is not explained.

Four runs that each show a deviation of 2.6 or more are more than chance
readily gives, so these four comparisons are recorded as showing possible
deviations from M at 2^-32, for two other classes and for the unrestricted
search, and not as agreement within sampling error. They are reported and
not explained. No real trial and no model draw in the comparison for the
class of this package had two residual words zero at once, so nothing in it
exercises Lemma E, which is exact.

A second measurement uses the layout of the algorithm, for the class of this
package: eight runs of 2^37 real trials of 6.1. Each run has its own four
seed words X2, X5, X6 and X9, shared by all its contexts. A context is one
thread of the program, 2^25 per run: a random (X12, X13, X14) with
X12 < 2^8, and 4,096 trials, each with a random alpha and a random member
of the class. Every thread has a random stream of its own. In one respect
the runs differ from 6.4: the program left the context word X10 random in
every thread where step 1 sets it to zero. A trial depends on X5 and X10
only through S5, so S5, which the algorithm holds fixed over a run, changed
from context to context, and sharing X5 fixed nothing. What the runs share
as the algorithm does is X2, X6 and X9 and the restriction of X12 to 256
values; w5, S2, S6, S10 and S14 depend on X6 and X12 only.

The 2^42 figures above for this class are divided by four to compare them
with the 2^40 trials of the eight runs; a standard deviation below combines
the sampling error of both figures.

- Early test: 150, 163, 169, 157, 171, 164, 177 and 168 passes, in all
  1,319. The scaled figures are 1,374.5 for real messages with independent
  contexts and 1,365.8 for the model: 1,319 is 1.4 and 1.1 standard
  deviations below them. The standard deviation of the eight counts is 8.4,
  against 12.8 for independent trials at that mean.
- The four residual words were zero 267, 285, 288 and 266 times over the
  eight runs, in all 1,106 times. The scaled figures are 1,006.8 and
  1,019.5, and uniform words would give 1,024: 1,106 is 2.7, 2.3 and 2.6
  standard deviations above these. The second word alone, 285 against 245.5
  in the model, is 2.1 above.
- Residuals of weight at most 32: 12,659, against 12,513.8 and 12,602.0
  (1.2 and 0.5 above). Of weight at most 40: 19,605,418, against 19,616,920
  and 19,615,872 (2.3 and 2.1 below).
- E1 required the class of the trial's Y4 in 217 trials, against 217.8 and
  226.0.

Two of these statistics, the zero words and the weight at most 40, are
more than two standard deviations from the model, in opposite directions.
They are recorded as measured and not explained. This measurement covers
eight seeds and events of probability about 2^-32 and above, with S5 not
shared; it does not test lower probabilities, and the pair statistics of
its runs were not kept.

These statistics concern events of probability about 2^-32 and above. They
do not reach the event R = 0.

**Scaled-down end-to-end check of the class search (participant
computation).** With short words the whole search can be run and its
collisions counted. The toy hash is BLAKE3 with 2 rounds and W-bit words,
for W = 8 and W = 10. Its IV words are the top W bits of the real IV words.
The permutation, the flags 11 and the block lengths 60 and 62 are the same.
G uses the rotations (4, 3, 2, 1) for W = 8 and (5, 4, 3, 2) for W = 10.
Everything used from Sections 3 to 6 is independent of the word size and is
applied unchanged: the length cancellation of 3.1, a pinned call as in 3.2,
Lemma H, the construction of Section 4, and the trial of 6.1 with Lemmas F,
Y, K and T. A constant set is six W-bit constants with the property of
Fact P. As in 6.1, eta is the XOR difference of E3's first-half d value, a
function of Y4 alone, and a class is the set of all Y4 with one eta.

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
trial is computed in full; the early test of 6.3 and the packing of 6.5
change the cost of a trial and not its outcome, and are not used. M predicts
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

The dispersion of the collisions per run was computed for every series as
the ratio of their variance to their mean, which is 1 for independent
trials. Over the eleven series, the ten of the two tables and the 20 runs
with Y4 held at one member, it lies between 0.46 and 1.60, and pooled over
their 253 degrees of freedom it is 0.96. One series stands out: constants
49 58 24 e9 20 b7 in layout (b), 40 runs, has 1.60, about 2.65 standard
errors above 1 (for 40 runs the standard error of the ratio is 0.23). In
every one of these series every run had a collision, as it must with
between 4 and 78 collisions per run on average. So whether a run has at
least one collision is not tested for the class search; it is tested only
for the unrestricted search, in the paragraph that follows.

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
runs of a GPU program on the same constants gave 826 against 810.2 and a
collision in 196 runs against 196.5. A further 10-bit job on three more
constant sets was stopped before any set had finished and contributes
nothing.

These checks test M and the independence of the trials down to actual
collisions for words of 8 and 10 bits, for runs laid out as described here.
They do not prove either for 32-bit words.

The declared experiment `residual-search` runs the search of Section 6 at toy
scale: one context and one alpha per seed, then the members of the class in
order from a number taken from the seed, stopping at the first trial whose
residual has a zero low byte in digest word 1. The search runs without the
early test and without the packing of 6.5, which change the cost of a trial
and not its outcome. The organizer checks that every returned pair agrees
on 136 digest bits. It checks the trial generator and the residual
computation on real digests. It provides finite-scale organizer-executed evidence for the class residual
search (testing 8 additional residual bits beyond the 128-bit half-collision on
256 organizer seeds), while reaching the full 128-bit residual event (`R = 0`)
is extrapolated via H1. Beside the search, the program evaluates one packed batch
per seed on the counting machine of 6.5 and returns its operations, loads
and equal lanes as observations; the organizer records them as untrusted
and does not check them.

**Limits of the evidence.**

- The factor 2,048 in H1 is assumed. It is set against an estimated lower
  bound of 7,319 +- 816 from a participant computation. The organizer-run
  experiments do not measure the factor, and the success bound needs it to
  be at least 2,045. With factor 1, the uniform rate, the same search needs
  2^127 trials and gives time_log2 = 123.4.
- M has been tested end to end, down to actual collisions, only for words
  of 8 and 10 bits. For 32-bit words it has been tested on real messages
  only for events of probability about 2^-32 and above. There the largest
  deviation for the class of this package is 1.5 standard deviations with
  independent contexts, and 2.3 and 2.1 for two statistics of the runs in
  the layout of the algorithm; for two other classes and for the
  unrestricted search deviations of 2.6, 2.7 and 3.1 were seen, and a
  second unrestricted run showed the 3.1 again with the opposite sign: not
  a consistent bias, but one pair count whose spread between runs is larger
  than a Poisson count allows. That is under study. That the
  trials meet the solution set at the rate M predicts, at probability
  2^-117, is an extrapolation that no feasible experiment can test
  directly.
- The quoted r is an estimated lower bound of a heavy-tailed quantity: a
  sum of counts of very different sizes, 84% of it from one beta. For this
  class the small passes scattered far more than their standard errors
  suggest: 9,472 (standard error 4,793) from 10 nonzero values, then 2,404
  (831) from 13, against 7,173 (778) and 7,319 (816) from 430 and 417. A
  standard error computed from a few values of such a quantity is not
  reliable. Only the passes with 2^41 draws per beta are relied on: the
  second, the third and eight further seeds, ten sums between 5,946 and
  7,785. The spread of the eight seeds, 682, agrees with the standard
  errors computed for single passes of that size. H1 still assumes 2,048
  and not an estimated figure: 3.4 times below the eight-seed mean and 2.9
  times below the smallest seed.
- The six constants were selected among 4,140 sets, and the class among the
  classes seen in the samples, by measurements of this kind. The largest of
  many noisy estimates is biased upwards. The second-pass figure for
  e96d6d6b has that bias, as the largest of eight, and so have the other
  sums of the first and second passes. Only the third-pass figure and the
  eight further seeds, and for the unrestricted search the 10.6, were
  obtained on fresh draws after the choices they depend on. The betas
  themselves were chosen on the first pass; betas that showed no count
  there are left out, which can only lower the figure.
- The counting program is the participant's, and so is every check of it.
  The 417 nonzero values behind the quoted r are counts made in full. The
  independent counter confirmed 100 of them, the 40 largest with 45.6% of
  the sum and 60 drawn at random, with ratios of sums of 1.027 and 0.969;
  the other 317 were not given to it. On uniform draws that counter was
  applied to 30 outcomes of a first check, and to 100 counts made in full
  and 240 outcomes of the random-subset branch of the first sample, with
  ratios of sums between 0.986 and 1.050. In the third pass the branch
  gave 915 values, all zero, of which 80 drawn at random were confirmed to
  have no solution. How often the branch was used
  in the other passes and for the other classes was not examined. Brute
  force confirms the program only for 8-bit words, where the branch cannot
  be reached.
- All trials of a run share the four seed words: X2, X6, X9 and S5 are the
  same in every trial of a run, w5 and the column-state words S2, S6, S10
  and S14 take at most 256 values in a run because they depend on X6 and
  X12 only, trials of one context share most of their other words, and the
  4,096 trials of one context and one alpha differ only in Y4 and what
  follows from it. Independence of the trials is assumed, not shown. The
  main 32-bit comparisons gave every context its own random words and so
  measure rates averaged over independent contexts. The eight runs in the
  layout of the algorithm share X2, X6 and X9 and the 256 values of X12,
  but not S5, and cover events of probability about 2^-32 and above. The
  scaled-down runs count actual collisions, but a run there holds X2, X9,
  X13 and X14 fixed, not the seed words. So the distribution of collisions
  within one run of 6.4 has not been tested directly at any word size; the
  scaled-down runs test it for another choice of the words held fixed.
- Single-word statistics are not evidence for the joint rate. An earlier
  version of this package, cancelled by the submitter before screening, used
  other constants and inferred a rate of half the uniform one from the
  frequencies of single zero residual words; the count described above gave
  0.024 for those constants. For some constant sets one residual word
  vanishes 40 times more often than a uniform word while the count is zero.
- H2 rests on the early-test pass rate measured on real trials of the
  class search: 2^42 trials with independent contexts, and eight runs of
  2^37 trials in the layout of the algorithm, in which S5 was not shared.
  That the number of passes of a full run of 2^116 trials stays near the
  mean is assumed.

**Scope and limitations.**

- No full collision of the 2-round hash is exhibited. The search is an
  analytical cost claim like other packages on this track; unlike a birthday
  search it tests each trial against zero and so needs no memory that grows
  with the number of trials.
- The two messages have different lengths, 60 and 62 bytes, and the
  construction relies on the true block length being a compression input, as
  the target profile specifies.
- The gain over a generic birthday search has three sources: half of the
  digest is matched by construction, which removes the table and about half
  of the round-1 work per trial; the constants are chosen so that the
  remaining half can match at all with a useful rate; and the search stays
  inside one class of Y4, where that rate is assumed to be 2,048 times the
  uniform one. The exponent of the number of trials is 116 instead of 128,
  and 127 if only the uniform rate is assumed.
- A brief literature search found free-start collisions and near-collisions
  of the compression function for reduced BLAKE variants, and no collision
  attack on the 2-round BLAKE3 hash. No priority or novelty claim is made.
- The time bound counts the arithmetic, logical and shift operations of the
  packed batch, its two comparisons and its two branches, and one load for
  every use of a constant or list entry, on a 16-register machine. It is an
  upper bound under that convention, not a measured running time. The count
  of a batch can be rerun with the self-test of the submitted program
  (6.5); that is a participant check and no organizer run verifies it.

**Field meanings.**

- time_log2 = 112.4 bounds total charged time by 2^112.4 units.
- memory_log2_bytes = 20 bounds simultaneous storage by 2^20 bytes.
- preprocessing_log2 = 63 bounds the recomputation of the six constants and
  the selection of the constants and of eta by 2^63 target-compression
  units.
- nonuniform_advice_log2_bytes = 5 bounds the stored constants and eta, 28
  bytes, by 32 bytes.
- success_probability = 0.39 holds under H1 and H2 as shown in Section 7.

The required baseline_improved identifier blake3-r2-nominal-v2 names the
organizer's nominal display reference 128, which is not an established attack,
a qualified baseline or a security bound. The claimed scalar 112.4 is lower
than that display value. Whether a qualified result improves the Yukon
incumbent is decided separately, and no Pareto dominance claim follows from
the scalar.


## 11. Full-resident and complement-propagated schedule (this derivative)

The ordered trials, random seed, fixed constants, class, early predicate,
full-collision check, and cap are exactly those of Section 6.4. Only the
algebraic evaluation of K3/D1 inside a batch and the register residency of
batch constants change. Every lane produces the exact same 32-bit early-test
word and flag as Section 6.5. There is no change to H1 or H2.

### 11.0 Complement propagation in K3 and D1 (-3 ALU ops, -1 constant)

In Section 6.5, K3 and D1 compute (modulo 2^32 in each 36-bit lane):

    s11 = kb XOR ROL(S7, 7)
    s15 = s11 + (kc XOR M) + 1                     (3 ALU ops: S11 - kc)
    s3  = ROL(s15, 8) XOR kd
    v   = s3 + ((ka + kb) XOR M) + (X2 + X6 + 1)   (4 ALU ops: X2 + X6 + S3 - ka - kb)
    d   = (s11 XOR M) + (X11 - X12 + 1)            (2 ALU ops: X11 - X12 - S11)

Using the two's-complement identity `~(A - B) = ~A + B (mod 2^32)` and
replacing the per-context constant `ROL(S7, 7)` by `~ROL(S7, 7) = ROL(S7, 7) XOR M`
and `X2 + X6 + 1` by `X2 + X6`:

    ns11  = kb XOR (~ROL(S7, 7))                   (1 ALU op:  ~S11)
    ns15  = ns11 + kc                              (1 ALU op:  ~S15 = ~(S11 - kc))
    ns3   = ROL(ns15, 8) XOR kd                    (6 ALU ops: ~S3)
    first = ((ns3 + (ka + kb)) XOR M) + (X2 + X6)  (4 ALU ops: X2 + X6 + S3 - ka - kb)
    d     = ns11 + (X11 - X12 + 1)                 (1 ALU op:  X11 - X12 - S11)

Because `kb` is a rotation output (`0 <= kb < 2^32`), `ns11 < 2^32`; since
`kc < 2 * 2^32`, `ns15 = ns11 + kc < 3 * 2^32` (the exact same lane bound as
Section 6.5), and `ns3 + ka + kb < 4 * 2^32`, so `(ns3 + ka + kb) XOR M` flips
all 32 lane bits without carry out of bit 35, and `first < 5 * 2^32 < 6 * 2^32`.
This saves **2 ALU operations in K3** (25 instead of 27) and **1 ALU operation
in D1** (8 instead of 9), reducing batch ALU/control operations from 154 to
**151**, and eliminates the constant `1` completely.

### 11.0b Full-resident 64-register schedule (claimed: 155 ops/batch, time_log2 = 111.81)

On a 256-bit word-RAM with a 64-register file (2 KiB, the size of a 32-entry
512-bit SIMD register file; the same machine convention as 6a250bf on
sha3-256-r6), pin all **42 batch constants** across the 586 batches of each
alpha:
- **14 mask constants**: `M`, `bit 32`, and the 12 rotation masks `L_r, H_r`
  for `r in {1, 7, 8, 12, 16, 24}`;
- **7 fixed constants**: `11`, `IV3`, `IV7`, `Y11`, `Y11'`, `eta`, and the loop
  bound `BATCHES = 586` (`1` is eliminated by Section 11.0);
- **14 per-context constants**: `~ROL(S7,7)`, `X2+X6`, `X11-X12+1`,
  `ROL(X12,8)`, `S12`, `X13`, `X9`, `-S1-S6`, `X14`, `X6`, `w0`, `w12`, `w5`,
  `w5+delta`;
- **7 per-alpha constants**: `pb`, `-pc`, `pd`, `IV3+IV7-pa-pb`, `X5`,
  `X5+w3`, `alpha`.

Loading these 42 registers is charged once per alpha (42 preload loads inside
the 512-op per-alpha setup allowance). Only the **two class-list entries**
`U[j]` and `V[j]` are loaded from memory in each batch (2 loads), plus 2
list-address additions to form `&U[j]` and `&V[j]` from the two list-base
registers and the list-index register `j`.

| Part | ALU/control (151) | List loads (64-reg) | Remaining loads (32-reg) |
| --- | ---: | ---: | ---: |
| loop | 3 | 0 | 1 |
| C0 backwards | 9 | 1 (`U[j]`) | 5 |
| K3 | 25 | 0 | 4 |
| D1 | 8 | 0 | 3 |
| C1 | 24 | 0 | 5 |
| C2 | 28 | 0 | 4 |
| E1 A and B | 26 | 0 | 5 |
| E3 A and B | 15 | 1 (`V[j]`) | 2 |
| early test | 13 | 0 | 0 |
| **Total** | **151** | **2 (+2 addr = 155)** | **29 (+2 addr = 182)** |

Register count (`FullResidentMachine.registers()`): at most 10 live dynamic
registers (including the list index `j`) + 42 resident constants + 3 reserved
slots (destination + two list bases) = **55 registers** (<= 56 of 64). Under
the 32-register machine of c85fc92 (14 mask registers resident, <= 27 of 32
registers used), Section 11.0 reduces the batch to 151 ALU ops + 29 loads + 2
list-address additions = 182 operations (`time_log2 = 112.07`).

Per alpha (4,096 trials, 586 batches), the 512-operation per-alpha budget
covers `per_alpha` (< 40 ops), packing and loading all 42 constants (`7*12 + 42
= 126` ops), and loop setup. Thus one alpha costs:

    586 * 155 + 512 = 90,830 + 512 = 91,342 operations = 22.300293 * 4,096 < 22.5 * 4,096 = 92,160.

Using the exact per-alpha count of `91,342` operations across all `2^104`
context-alpha groups (`91,342 * 2^104 = 22.300293 * 2^116` main-loop operations;
or conservatively charging `22.5` operations per trial with 818 operations per
alpha of slack) and retaining the expanded confirmation allowance of `4,096`
operations per early-test pass (`2^104 * 4,096 = 2^116` operations, Section 11.1):

    T_exact <= (91,342 * 2^104 + 2^116 + 2^83 + 2^60 + 2^18 + 2^11 + 1) / 430 + 2 + 2^63
            =  23.300293 * 2^116 / 430 + < 2^84
            =  2^111.79448 + < 2^84
            <  2^111.81  (with 0.0155 bits of arithmetic headroom).

Even under the rounded 22.5-op/trial upper bound (`23.5 * 2^116 / 430 =
2^111.8068 < 2^111.81`), or an integer 23-op/trial charge (`24 * 2^116 / 430 =
2^111.8372 < 2^111.84`), the bound holds cleanly. We claim **time_log2 = 111.81**
under the 64-register full-resident schedule.

| Schedule variant | Registers used | Ops/batch | Ops/trial charged | Confirmation | time_log2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| **64-reg full-resident + Section 11.0 (exact 91,342/alpha)** | **55 / 64** | **155** | **22.3003** | **2^116 (4096/pass)** | **111.80 (claimed 111.81)** |
| 64-reg full-resident + Section 11.0 (22.5 rounded) | 55 / 64 | 155 | 22.5 | 2^116 (4096/pass) | 111.81 |
| 64-reg full-resident, integer per-trial charge | 55 / 64 | 155 | 23.0 | 2^116 (4096/pass) | 111.84 |
| 32-reg 14-mask resident + Section 11.0 | 27 / 32 | 182 | 27.0 | 2^116 (4096/pass) | 112.07 |
| 5kyguy (c85fc92) 32-reg 14-mask baseline | 27 / 32 | 187 | 28.0 | 2^116 (4096/pass) | 112.12 |
| Jbenisek (04638ed8) 16-reg baseline | 10 / 16 | 228 | 34.0 | 2^114 (1024/pass) | 112.40 |

The `resident-audit` experiment tests four contexts per organizer seed in the
exact shared-seed layout of Section 6.4 (`X2, X5, X6, X9` shared, `X10 = 0`, so
`S5` is fixed and shared across all four contexts, and `X12 < 256`), verifying
on both the first and padded final batch that `FullResidentMachine` (151 ops,
2 loads, <= 55 registers) and `ResidentMachine` (154 ops, 31 loads, <= 27
registers) produce the exact same 7 lane words and 7 flags as `Machine` and
`scalar_early`, while also recording the shared-seed `S5`-fixed early-test pass
count (`H2`) and low-nibble residual hits (`H1`).

### 11.1 Expanded confirmation allowance

Charge 4096 primitive operations for each trial passing the early predicate,
up to the unchanged cap of 2^104. This deliberately replaces the source's
1024 allowance. No rate assumption is used to reduce the charged cap.

Decode the at most twelve free bits of the class member as in class_member:
right shift, AND 1, left shift and OR for each bit, followed by subtraction
and reduction. Allow 64 arithmetic operations. Recompute per_alpha and
trial rather than retain hot temporaries. Syntactic expansion gives 39 and
105 arithmetic operations respectively, counting each scalar rotate as five
operations (two shifts, subtraction of the rotation distance, OR, AND).
Evaluate C1, C2 and E1/E3 for A and B: six G calls, each 14 arithmetic
operations plus four five-operation rotations, hence 204 operations.
Form the four residual words from these outputs: at most sixteen XOR,
OR and comparison operations. Total: at most 64+39+105+204+16 = 428.

This describes a deliberately simple implementation with intermediate
scalars assigned fixed scratch slots. Charge seven primitives for each
of those 428 arithmetic steps: up to two operand loads, one result store,
up to three address additions, and the arithmetic instruction. This is
2996 operations and accounts for scalar constant operands as loads too.
Reserve another 1100 operations for the following fixed operations:

* Save and restore at most 56 hot registers, with address formation:
  at most 168 operations (leaving 740 operations for cap counter, context/alpha reloads, fixed-argument G setup, scratch initialization, branching and return; 2996 + 1100 = 4096).
* Copy the sixteen context message words to sixteen working slots, using
  explicit address formation: at most 64 operations.
* Obtain the class-member number from the list index and lane number,
  reject the six padding lanes of the last batch, and scan the seven
  lane flags: at most 128 operations, charged once per nonempty batch to
  its first genuine passing lane. Padding repeats the genuine final lane;
  a padded pass therefore cannot occur without a genuine pass.
* Cap counter, context/alpha reloads, fixed-argument G setup, scratch
  initialization, branching and return: at most 780 operations. A concrete
  allocation uses at most 128 explicit word transfers and 128 control or
  pointer operations; allowing an address addition per transfer gives 384,
  leaving 396 for initialization and call boundaries. No recursive calls,
  variable-size allocation or unbounded traversal is used.

Thus 2996+1100 = 4096 bounds the confirmation procedure. Construct complete
messages and perform two complete target hashes only when all four residual
words vanish; the exact construction then guarantees success. That final
step is charged separately once as in the source. Failures consume the cap.
This is a deterministic cost allowance, not a measurement of Python runtime.

The reduction in main-loop reloads and this increased confirmation charge
leave the total below 2^111.81 (2^111.7945 exact, 0.0155 bits headroom; and below 2^112.07 on 32 registers), assuming the unchanged historical costs.
The historical allowance and full-run probability extrapolations remain
unresolved, exactly as disclosed in the inherited source claim.
