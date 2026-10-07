# A staged two-level S8 search on the 55/63-byte half-collision of 2-round BLAKE3, with a sampled bound on the stage-B share

The scalar below is `time_log2` under `collision-frontier-v5` (C = 430).

**Credits.** The search, its counted program and almost all of this text
are those of **winglock**'s submission 098e66f4 (94.45), which is public,
AI-screened, in review and not promoted. **winglock**, **Jbenisek**,
**tekkac** and **Th0rgal** are co-authors of this submission. 098e66f4 is
built on two submissions of Jbenisek. From c66f230d (co-author tekkac):
the 55/63-byte length cancellation, the six pinned constants, Lemmas L and
H, the class of Y4 (eta = 830303cf), rule A and Lemma N. From 60f94c5c:
the three-level construction (steps O, M, Y and T of Section 2: an outer
step of six words, the middle word X2, the member y), the table of member
values that is built once per outer step and reused for all 2^32 values of
X2, and the **staged batch**: a cheap rule-A test after C2 for every batch,
the rest of the batch only for batches in which some lane passes, and a
budget on the number of such batches that halts the run. Building
member-dependent values once per outer step was first published by Th0rgal
in df8bd46d. The seven 36-bit lanes and the masked rotation are from ticket
2bf40fb (tekkac); the complement propagation follows 8c81a219 (Th0rgal).
winglock's (18a7fc52, d26a3c5f, 2bb5d604 and 098e66f4): the sub-class S8,
the beta filter and Lemma B, Lemmas D and D', the exact S8 count, the block
accumulator and the branch-free 64-register residual computation (stage C),
the beta filter as the test of a second stage, a fresh random word for every
outer step, the exact model values of the two stage events, budgets whose
overrun probability is bounded by a Chernoff bound (Theorem 2), the uniform
sample of Section 8.2 and every measurement of Sections 6, 8.1 and 8.2 that
is not marked as this package's. In the text taken over from 098e66f4,
"we" and "our" refer to its authors. 098e66f4 does not use the sub-class,
the eight-condition rule, the E1 test stage or the budget premises of
60f94c5c, and neither does this package.

**What this package changes (Subflatus3).** One constant of the algorithm
and one premise. The stage-B budget E_B falls from 1.02 p_B to 0.61 p_B
batches per batch, and the stage-B part of H1 (ii) falls from 1.01 p_B to
0.60 p_B, with p_B = 0.1992628 the exact value of the stage-B event under
the seven-word model M (Section 8.2). Everything else is 098e66f4: the
construction, S8, rule A, the filter, the counted pieces and their
operation counts, the stage-C budget, H1 (i), F, lambda, N and the
success bound. The real stage-B share of the run lies far below p_B,
because rule A clusters by context. 098e66f4's uniform sample gives
0.54629 +- 0.00047 of p_B. An independent, preregistered uniform sample
made for this package (Section 8.3: own program, own cross-check against a
forward compression and `verifier/blake3.py`, 65,536 outer steps, 2^39
trials) gives 0.54644 +- 0.00023 of p_B. If the run average were 0.60 p_B or
more, a sample mean this low would have probability below 3 * 10^-14
(Lemma C', proved here), and an empirical Bernstein bound puts the run
average below 0.5567 p_B at confidence 1 - 2^-64. The charge per trial
falls from 6.3408 to 5.4887 operations, and the claim falls from 94.45 to
**94.25**. The program is 098e66f4's with only the two ledger constants and
its credit docstring changed (Section 6).

**Exact part.** For every choice of eight 32-bit words the construction gives
a 55-byte message A and a 63-byte message B whose complete 2-round digests
agree on digest words 0, 2, 5 and 7 (Theorem 1). One of the eight words is
the round-1 state word Y4; the search keeps Y4 in S8. The stage tests are
exact: stage A passes a lane iff its trial satisfies rule A (Lemma A'),
stage B iff it satisfies rule A and the filter (Lemma F), and stage C
computes the residual exactly (Lemmas D, D'). Given H1 (ii), each budget
is exceeded with probability below exp(-2.3 * 10^9) (Theorem 2, a
Chernoff bound over independent outer steps; no independence inside an
outer step, a context or a batch is used).

**Heuristic part.** The search runs N = V * 2^80 pairs (V = 1,512,538,
N = 2^100.53). H1 (i) assumes a trial is *good* (R = 0, rule A, beta
filter) with probability at least F * 2^-128, F = 92,675,072 = 2^26.4657,
half of the exact model count 185,350,144 (Section 8; `python3
experiments/s8stage.py --count` recomputes this integer). H1 (ii) is the
first-moment statement of Section 7: the run average of the stage-B event is
at most 0.60 p_B, and the run average of rule A with the filter is at most
1.25 * 2^-11. Total charged time 2^94.2416, claimed 94.25. With the uniform
rate instead, the same search needs 2^127 trials and gives 120.96. No full
collision is exhibited.

**History of the margins (098e66f4, reported because the choice of a
margin after a measurement matters).** A first build of 098e66f4 stated
(ii) as 1.01 times the per-trial rates 2^-5 (rule A) and 2^-11, charged
stage B at 1.02 * 2^-5 per trial and claimed 94.50. Its authors' own review
pointed out that the 41 replays of Section 6 give rule A at 1.023 +- 0.016
times 2^-5, and that the only measurement of (ii) then covered a narrow
index range of the run. They replaced the stage-B part by the batch-level
event, whose run average was 0.51 of p_B in the measurement they had (so
the batch-level form was chosen after seeing that measurement; its margin
1.01 and the budget 1.02 were kept), widened the stage-C margin from 1.01
to 1.25 (budget 1.27), and then preregistered and ran the uniform sample of
Section 8.2 (0.5463 +- 0.0005 of p_B and 1.00001 +- 0.0001 of 2^-11). For
this package the value 0.60 p_B (budget 0.61 p_B) was chosen after reading
098e66f4's published sample and before this package's own sample, whose
plan fixed the value and the rule "change nothing unless the empirical
Bernstein bound at delta = 2^-64 is at most 0.60 p_B" (Section 8.3).

## 1. Target

H is unkeyed BLAKE3-256 with rounds 0 and 1 of every compression. A message
of n <= 64 bytes is one chunk of one block and one root compression: flags
CHUNK_START | CHUNK_END | ROOT = 11, counter 0, block length n, the message
followed by 64 - n zero bytes read as sixteen little-endian words w0..w15.
The state starts v[0..7] = IV, v[8..11] = IV[0..3], v[12..15] = (0, 0, n, 11),
with IV = 6a09e667 bb67ae85 3c6ef372 a54ff53a 510e527f 9b05688c 1f83d9ab
5be0cd19. Arithmetic is modulo 2^32. G(a,b,c,d,x,y) is

    a1 = A + B + x       d1 = ROR(D ^ a1, 16)   c1 = C + d1    b1 = ROR(B ^ c1, 12)
    a2 = a1 + b1 + y     d2 = ROR(d1 ^ a2, 8)   c2 = c1 + d2   b2 = ROR(b1 ^ c2, 7)

with outputs (a2, b2, c2, d2). Round 0 and round 1, with the permutation
P = (2,6,3,10,7,0,4,13,1,11,12,5,9,14,15,8) applied once between them:

    round 0  K0=G(0,4,8,12;w0,w1)  K1=G(1,5,9,13;w2,w3)  K2=G(2,6,10,14;w4,w5)  K3=G(3,7,11,15;w6,w7)
             D0=G(0,5,10,15;w8,w9) D1=G(1,6,11,12;w10,w11) D2=G(2,7,8,13;w12,w13) D3=G(3,4,9,14;w14,w15)
    round 1  C0=G(0,4,8,12;w2,w6)  C1=G(1,5,9,13;w3,w10) C2=G(2,6,10,14;w7,w0)  C3=G(3,7,11,15;w4,w13)
             E0=G(0,5,10,15;w1,w11) E1=G(1,6,11,12;w12,w5) E2=G(2,7,8,13;w9,w14) E3=G(3,4,9,14;w15,w8)

S is the state after K0..K3, X after round 0, Y after C0..C3, Z the final
state. The digest is o[i] = Z[i] ^ Z[i+8] for i = 0..7. Messages here have
55 and 63 bytes: complete hash, standard IV, flags, true length and
feed-forward, full 256-bit digest.

**Fact 1 (inverting G).** Each assignment of G can be solved for any one of
its terms (b1 = ROL(b2,7) ^ c2, c1 = c2 - d2, d1 = ROL(d2,8) ^ a2,
B = ROL(b1,12) ^ c1, C = c1 - d1, a1 = ROL(d1,16) ^ D, y = a2 - a1 - b1,
x = a1 - A - B). Fourteen words are an execution of one call exactly when
the eight assignments hold.

## 2. The half-collision (c66f230d) and the three-level construction (60f94c5c)

**Lemma L.** Put K = IV2 + IV6 = 5bf2cd1d and, for any w4, w5,
w4' = ((K + w4) ^ 8) - K and w5' = w5 + w4 - w4'. K2 with length 55 and
words (w4, w5) leaves the same four words as K2 with length 63 and
(w4', w5'). *Proof.* With a1 = K + w4 the second execution has first value
a1 ^ 8 and d1 = ROR(63 ^ a1 ^ 8, 16) = ROR(55 ^ a1, 16), the same; c1, b1
follow; the fifth value is (a1 ^ 8) + b1 + w5' = a1 + b1 + w5. QED. No other
round-0 call reads v[14], w4 or w5, so messages of 55 and 63 bytes that
share all other words have the same X. Both messages are honest byte
strings exactly when bytes 55..63 of the block are zero: w14 = w15 = 0 and
the top byte of w13 is zero (the 63-byte message ends in eight zero bytes).

**Fact P.** Constants X3 = 29d4fa98, X7 = bee3af28, X11 = 44036000,
X15 = 40c58500, W4 = 97475638, W13 = 0007c006 (top byte 0). Then
W4' = 97475640, delta = W4 - W4' = fffffff8, and C3 = G(X3, X7, X11, X15;
w4, W13) gives with w4 = W4 the outputs a = Y3 = 8127c181, b = 76f7aefd,
c = Y11 = 7af77f38, d = bbfbdffe, and with w4 = W4' the outputs
a = Y3' = 7edf3e7e, b = 76f7aefd, c = Y11' = 850000c3, d = bbfbdffe. (A
finite computation; the b and d outputs agree.)

**Lemma H.** If two executions have the same X, share all words except w4,
w5, have (X3, X7, X11, X15) as above, w13 = W13 and w4 = W4 resp. W4', then
the digests agree on words 0, 2, 5, 7. *Proof.* C0, C1, C2 are identical;
C3 differs only in Y3, Y11 (Fact P). E0 and E2 read neither Y3, Y11, w4 nor
w5, so Z[0,5,10,15] and Z[2,7,8,13] agree, and o0, o2, o5, o7 use only
these. QED. The **residual** R is the XOR of the two digests on words 1, 3,
4, 6; these come from E1 and E3 only. A pair collides iff R = 0.

**The construction (60f94c5c).** Eight free words: the
six words of an *outer step* (vc, vd, D3.d1, S15, S9, w5), where vc = C0.c1
and vd = C0.d1 are the third and second values of the round-1 call C0 and
D3.d1 is the second value of D3; the *middle word* X2; and the *member*
y = Y4. For a call, a1, d1, c1, b1 are its first four values (Fact 1). Every
line is one assignment of the named call solved for its left side;
w4 = W4, w13 = W13, w14 = w15 = 0.

**Step O (outer step; reads only the six words).**

    K2:  ka2 = K + W4; kd2 = ROR(ka2 ^ 55,16); kc2 = IV2 + kd2; kb2 = ROR(IV6 ^ kc2,12)       (constants)
         S2 = ka2 + kb2 + w5; S14 = ROR(kd2 ^ S2,8); S10 = kc2 + S14; S6 = ROR(kb2 ^ S10,7)
    D3:  D3.a1 = ROL(D3.d1,16) ^ S14; D3.c1 = S9 + D3.d1; D3.b1 = X3 - D3.a1; S4 = ROL(D3.b1,12) ^ D3.c1
         S3 = D3.a1 - S4; X14 = ROR(D3.d1 ^ X3,8); X9 = D3.c1 + X14; X4 = ROR(D3.b1 ^ X9,7)
    K3:  K3.d1 = ROL(S15,8) ^ S3; K3.c1 = IV3 + K3.d1; K3.b1 = ROR(IV7 ^ K3.c1,12); S11 = K3.c1 + S15
         S7 = ROR(K3.b1 ^ S11,7); K3.a1 = ROL(K3.d1,16) ^ 11; w6 = K3.a1 - IV3 - IV7; w7 = S3 - K3.a1 - K3.b1
    C0, D2:  X8 = vc - vd; vb = ROR(X4 ^ vc,12); D2.b1 = ROL(X7,7) ^ X8; D2.c1 = ROL(D2.b1,12) ^ S7; X13 = X8 - D2.c1

**Step M (middle; reads the outer step and X2, not y).**

    D2:  D2.a1 = X2 - D2.b1 - W13; D2.d1 = ROL(X13,8) ^ X2; S13 = ROL(D2.d1,16) ^ D2.a1
         S8 = D2.c1 - D2.d1; w12 = D2.a1 - S2 - S7
    K1:  K1.c1 = S9 - S13; K1.d1 = K1.c1 - IV1; K1.a1 = ROL(K1.d1,16); K1.b1 = ROR(IV5 ^ K1.c1,12)
         S1 = ROL(S13,8) ^ K1.d1; S5 = ROR(K1.b1 ^ S9,7); w2 = K1.a1 - IV1 - IV5; w3 = S1 - K1.a1 - K1.b1
    K0:  K0.b1 = ROL(S4,7) ^ S8; K0.c1 = ROL(K0.b1,12) ^ IV4; K0.d1 = K0.c1 - IV0; K0.a1 = ROL(K0.d1,16)
         S12 = S8 - K0.c1; S0 = ROL(S12,8) ^ K0.d1; w0 = K0.a1 - IV0 - IV4; w1 = S0 - K0.a1 - K0.b1

**Step Y (member; reads the outer step and y, not X2).**

    C0:  Y8 = ROL(y,7) ^ vb; Y12 = Y8 - vc; Y0 = ROL(Y12,8) ^ vd; va = Y0 - vb - w6; X12 = ROL(vd,16) ^ va
    D1:  gc = X11 - X12; gb = ROR(S6 ^ gc,12); X6 = ROR(gb ^ X11,7); gd = gc - S11; X1 = ROL(X12,8) ^ gd

**Step T (the trial).**

    C0:  X0 = va - X4 - w2
    D0:  fd = ROL(X15,8) ^ X0; fc = S10 + fd; X10 = fc + X15; fb = ROR(S5 ^ fc,12)
         X5 = ROR(fb ^ X10,7); fa = ROL(fd,16) ^ S15; w8 = fa - S0 - S5; w9 = X0 - fa - fb
    D1:  ga = ROL(gd,16) ^ S12; w10 = ga - S1 - S6; w11 = X1 - ga - gb

**Step S2.** w4 = W4 in A and w4' = W4' in B; w5' = w5 + (W4 - W4') = w5 + delta,
that is w5 - 8 (Lemma L); w13 = W13 and w14 = w15 = 0 in both.
**Step S3.** A = first 55 bytes of LE(w0..w15); B = first 63 bytes of the
same words with w4', w5'.

**Lemma S/F/Y.** For all eight words: K0, K1, K2 (length 55), K3 map the
initial state to (S0..S15); D0, D1, D2, D3 map S to (X0, X5, X10, X15),
(X1, X6, X11, X12), (X2, X7, X8, X13), (X3, X4, X9, X14); and C0 on
(X0, X4, X8, X12; w2, w6) has values va, vd, vc, vb and outputs
(Y0, y, Y8, Y12). The lines of step O read only the six words, those of
step M not y, those of step Y not X2. *Proof.* Each call's eight
assignments are lines above solved for one term, in order: K2 (all eight
forwards), D3 (D3.a1, D3.c1, D3.b1 from a2 = X3, S4, S3, X14, X9, X4), K3
(K3.d1, K3.c1, K3.b1, S11, S7, K3.a1, w6, w7), D2 (X8 with C0, D2.b1, D2.c1,
X13, D2.a1, D2.d1, S13, S8, w12), K1 (K1.c1, K1.d1, K1.a1, K1.b1, S1, S5,
w2, w3), K0 (K0.b1, K0.c1, K0.d1, K0.a1, S12, S0, w0, w1), C0 (vb, X8, Y8,
Y12, Y0, va, X12, X0), D1 (gc, gb, X6, gd, X1, ga, w10, w11), D0 (fd, fc,
X10, fb, X5, fa, w8, w9). Every name is assigned once and only from earlier
lines or the eight words; X3, X7, X11, X15 enter as the a output of D3, the
b output of D2, the c output of D1 and the d output of D0. By Fact 1 the
names are the executions of the calls. The lemma is also
checked on real messages by both experiments and the self-test
(Sections 5, 6). QED.

**Theorem 1.** For all eight words, A and B are distinct messages of 55 and
63 bytes whose complete 2-round digests agree on words 0, 2, 5, 7, and
Y4 = y in both. *Proof.* Bytes 55..63 of the block are zero (w13 top byte,
w14, w15), so A and B are honest messages with these blocks. By Lemma
S/F/Y round 0 on A leaves X with (X3, X7, X11, X15) the constants; by Lemma
L B has the same X; Lemma H gives the four digest words; C0 reads only
shared words, so Y4 = y in both. The lengths differ. QED. Each of the eight
words is a value of the forward computation of A (two values of C0, one of
D3, two state words of S, a message word, a word of X and Y4), so distinct
eight-word inputs give distinct messages A.

## 3. Class, sub-class S8, rule A, the beta filter and the residual words

**Class (Lemma Q, c66f230d).** E3's first assignment is e1 = Y3 + Y4 (for B
Y3' + Y4, w15 = 0) and its second h1 = ROR(Y14 ^ e1, 16), so
eta = h1 ^ h1' = ROR(e1 ^ (e1 + DY3), 16) with DY3 = Y3' - Y3 = fdb77cfd is a
function of Y4. With eta = 830303cf, the class is the set of Y4 with
(e1 AND 03cf8303) = 030c0303: since (e ^ x) - e = 2((~e) AND x) - x, the
condition e1 ^ (e1 + DY3) = x = ROL(eta,16) = 03cf8303 reads
2((~e1) AND x) = DY3 + x = 01870000, which fixes the 13 bits of e1 on x
(bit 31 is not in x) and leaves 19 free; 524,288 members.

**Sub-class S8 (winglock, 2bb5d604).** S8 is the set of class members whose e1 = Y3 + Y4
also has bits 2 and 3 equal to 1 and bit 21 equal to bit 26: 2^16 = 65,536
members (three linear conditions on free bits of e1). Member number i,
0 <= i < 2^16, has e1 = 030c0303 | 0000000c with the bits of i placed at the
free positions in the order 14, 30, 31, 4, 5, 6, 7, 10, 11, 12, 13, 20,
21, 27, 28, 29, then bit 26 set equal to bit 21; Y4 = e1 - Y3. (The order
is that of 2bb5d604, fixed before any stage measurement; the charge does not
depend on it, because the budgets of Section 4 follow values of M, which do
not depend on the order. The real share of batches entering stage B does
depend on it, Section 8.2.)

**Lemma T.** For a context and y in S8 (a subset of the class), the pair
of Theorem 1 has eta = 830303cf. (Fact P gives the a inputs Y3, Y3' of E3;
Y14 and w15 are shared.)

**Rule A (c66f230d).** h1 (E3, message A) satisfies rule A when bits 0, 16,
17 are 0, bit 1 is 1 and bits 2, 3 differ (probability 2^-5 for a uniform
word). **Lemma A.** With z = a2 ^ d1 of C2, ROL(h1, 24) = z ^ ROL(e1, 8)
(sixth assignment of C2: Y14 = ROR(z, 8)). The e1 bits entering (0, 1, 16,
17, 18, 19) are fixed by the class to 1, 1, 0, 0, 1, 1, so rule A holds iff
z24 = 0, z25 = 1, z8 = 1, z9 = 1 and z26 != z27.

**Lemma N (c66f230d).** With beta = b1 ^ b1' and eps = c2 ^ c2' of E1 and
n = eps ^ ROL(beta ^ eps, 1) ^ eta, n = D3 ^ ROL(D6, 8), where D3, D6 are
the XOR differences of digest words 3 and 6. So R = 0 implies n = 0.
*Proof.* o3 = Z3 ^ Z11 is E3's a and E1's c output, so D3 = (e2 ^ e2') ^ eps;
o6 = Z6 ^ Z14 is E1's b and E3's d output, b2 ^ b2' = ROR(beta ^ eps, 7)
and h2 ^ h2' = ROR(eta ^ e2 ^ e2', 8); rotating D6 left by 8 and adding D3
cancels e2 ^ e2'. QED.

**Beta filter (winglock, 2bb5d604).** E1's a1 and d1 are shared by A and B, c1 = Y11 + d1
and c1' = Y11' + d1 = c1 + DY11 with DY11 = 0a08818b, so
beta = ROR(c1 ^ (c1 + DY11), 12) is a function of c1. The filter passes a
trial when (c1 AND 00098188) = 00008000 (6 bits, rate 2^-6). Let
T6 = {18b0e098, 18b1a098, 18d0e098, 18d1a098, 18b3e098, 18d3e098}.

**Lemma B.** Every c1 with beta in T6 passes the filter. *Proof.* Put
x = ROL(beta, 12). Bit i of c1 ^ (c1 + D) is D_i ^ carry_i, so the carries
are carry_i = x_i ^ D_i; carry_{i+1} = maj(c1_i, D_i, carry_i), so where
D_i = carry_i the next carry must equal D_i (else no c1), and where
D_i != carry_i bit i of c1 equals carry_{i+1}. For each beta in T6 the
carries are consistent and the fixed bits of c1 include 3, 7, 8, 15, 16, 19
with values 0, 0, 0, 1, 0, 0. This is a finite computation on six words
(function `beta_conditions` of the program; the experiment `class-filter`
returns it as `lemma_b = 6`). It was also checked over all 2^32 values of
c1: exactly 2^21, 2^21, 2^21, 2^21, 2^19, 2^19 values give the six betas,
all of them pass, and 2^26 values pass the filter in all. QED.

**Lemma D (residual words, winglock).** For a trial write (a1, d1, c1, b1, a2,
d2, c2, b2) for E1 and (e1, h1, g1, f1, e2, h2, g2, f2) for E3 on message A,
primes for B. Then Z1, Z12, Z11, Z6 are E1's a2, d2, c2, b2 and Z3, Z14, Z9,
Z4 are E3's e2, h2, g2, f2, so the XOR differences of digest words 1, 3, 4, 6
are

    D1 = (a2 ^ a2') ^ (g2 ^ g2')          D3 = (e2 ^ e2') ^ (c2 ^ c2')
    D4 = ROR(f1 ^ f1' ^ g2 ^ g2', 7) ^ (d2 ^ d2')
    D6 = ROR(b1 ^ b1' ^ c2 ^ c2', 7) ^ (h2 ^ h2')

and R = 0 iff all four are 0. In E1, a1 and d1 are shared, c1' = Y11' + d1,
b1' = ROR(Y6 ^ c1', 12) and a2' = a1 + b1' + w5 + delta. In E3, Y4, Y9, Y14
and w8 are shared, e1' = Y3' + Y4 and h1' = h1 ^ eta with eta = 830303cf
(Lemma T), so g1' = Y9 + h1'. *Proof.* The output assignments of G and the
digest o[i] = Z[i] ^ Z[i+8]; f2 = ROR(f1 ^ g2, 7), b2 = ROR(b1 ^ c2, 7), and
ROR distributes over XOR. QED.

**Lemma D' (test words, winglock).** With P = a2 ^ a2', the word
W4 = (f1 ^ f1') ^ P ^ ROR(P, 1) equals ROL(D4, 7) ^ D1, so R = 0 iff
D1 = D3 = W4 = D6 = 0. *Proof.* d1 is shared, so d2 ^ d2' =
ROR(d1 ^ a2, 8) ^ ROR(d1 ^ a2', 8) = ROR(P, 8) and ROL(D4, 7) =
f1 ^ f1' ^ g2 ^ g2' ^ ROR(P, 1); XOR with D1 = P ^ g2 ^ g2' gives W4. The map
(D1, D4) -> (D1, ROL(D4, 7) ^ D1) is invertible. QED. Also
e2' = e1' + f1' + w8 = (e1 + w8) + f1' + DY3 with DY3 = Y3' - Y3, and
w8 = fa - S0 - S5 with fa = ROL(fd, 16) ^ S15 (D0, step T).


**Lemma A' (packed rule-A test, 098e66f4).** Let a lane hold a value Z < 2^35
whose low 32 bits are z = Y2 ^ C2.d1 of the trial. Put zr = Z + 2^26,
tA = (zr XOR 0A000300) AND 0B000300 and fA = tA + (2^32 - 1). Then fA < 2^33
and bit 32 of fA is 0 iff the trial satisfies rule A. *Proof.* Adding 2^26
leaves bits 0..25 unchanged and the carry into bit 27 is z26, so bit 27 of
zr is z27 ^ z26 and bits 8, 9, 24, 25 are those of z; zr < 2^35 + 2^26, so
nothing leaves the lane. The mask keeps bits 8, 9, 24, 25 and 27, and the
XOR with 0A000300 (bits 8, 9, 25, 27) makes each of them 0 exactly when
z8 = 1, z9 = 1, z24 = 0, z25 = 1 and z26 != z27, the five conditions of
Lemma A. So tA = 0 iff rule A holds; tA < 2^28, so tA + 2^32 - 1 has bit 32
equal to 1 iff tA != 0, and is below 2^33. QED.

**Lemma F (packed filter test, 098e66f4).** Let a lane hold C < 2^35 whose low
32 bits are E1's c1 of message A. Then wF = (C XOR 00008000) AND 00098188 is
0 iff the trial passes the filter, fF = wF + 2^32 - 1 < 2^33 has bit 32
equal to 1 iff it fails, and f = fA OR fF has bit 32 equal to 0 iff the
trial satisfies rule A and passes the filter. *Proof.* The mask lies in the
low 32 bits, so wF = 0 iff (c1 AND 00098188) = 00008000; fA and fF are
below 2^33, so bit 32 of their OR is the OR of their bits 32. QED.

**Stage decisions.** With B32 the word holding 2^32 in every lane, x = f
AND B32 holds exactly the seven bits 32 (bits 33..35 of f are 0, and so are
bits 0..31 of B32); x differs from B32 iff some lane has bit 32 equal to 0.
The same holds for fA. So the compare-and-branch of stage A is taken iff
some trial of the batch satisfies rule A, and that of stage B iff some
trial satisfies rule A and passes the filter.

## 4. Algorithm

Constants: V = 1,512,538 values of vd; N = V * 2^80 = 2^100.5285 trials in
V * 2^64 * 9,363 batches; p_B = 32,052,445,611,625 / 160,855,115,169,792 =
0.1992628 (Section 8.2); budgets

    E_B = ceil(0.61 * p_B * V * 2^64 * 9,363) = 31,753,907,200,547,407,136,523,550,720 = 2^94.6809
    E_C = ceil(1.27 * N * 2^-11)              =  1,133,912,952,398,586,629,867,039,622 = 2^89.8734

1. Once: the lists U and V of S8 (9,363 packed words each; list word j
   holds members 7j .. 7j + 6 in its seven lanes, the last word members
   65,534, 65,535 and 65,535 repeated): U[j] = ROL(y,7), V[j] = y per lane.
   Set the budget registers cB = E_B + 1 and cC = E_C + 1.
2. For each vd < V and each w5 in 0..2^32-1 (an *outer step*): draw one
   fresh uniform 256-bit word and take vc, D3.d1, S15, S9 from its 32-bit
   words 0 to 3; run step O and build the table: for each list word j, the
   five packed words XA[j] = va - X4, X6[j], X1[j], R[j] = ROL(gd,16) and
   Y12[j] of step Y for its seven members. Then for each X2 in 0..2^32-1:
   run the middle step (step M and the nine per-X2 registers of the batch;
   it sets the block accumulator acc to all ones), then the 9,363 batches
   (seven consecutive members per batch). Every batch runs stage A. If some
   lane passes rule A, the batch subtracts 1 from cB, halts the run with
   failure if cB reaches 0, and runs stage B. If some lane passes rule A
   and the filter, it subtracts 1 from cC, halts with failure if cC reaches
   0, and runs stage C, which computes the words D1, D3, W4, D6 of Lemmas D
   and D' for all seven lanes and ANDs a per-lane indicator into acc (bit 32
   of a lane stays 1 iff none of that lane's trials so far has all four
   words zero). After the last batch of the X2 value, one test: is bit 32
   of some lane of acc zero (compare and branch)?
3. If the test passes: recompute the 9,363 batches of this X2 value with
   all three stages and take the first lane with all four words zero (under
   2^22 operations), recompute that trial in scalar form from its member
   number (steps O, M, Y, T), build A, B (S2, S3), evaluate both complete
   digests, compare, output the pair if they are equal, and halt in either
   case.
4. Halt with failure when all trials are done.

There are N = V * 2^32 * 2^32 * 2^16 trials, all distinct pairs for every
value of the coins (Theorem 1: two trials differ in vd, w5, X2 or y, and
each is a value of the forward computation of A). Step 3 runs at most once.
At most E_B batches complete stage B and at most E_C complete stage C.

**Completeness.** Let a trial be good (R = 0, rule A, filter). Its lane
passes stage A (Lemma A'), so its batch enters stage B; its lane passes
stage B (Lemma F), so its batch enters stage C; stage C computes its four
words exactly (Lemmas D, D', Section 5) and its indicator clears bit 32 of
its lane of acc, which the AND keeps cleared to the end of its X2 value.
So, unless a budget has halted the run before, the block test of its X2
value (or of an earlier one) is taken, and step 3 outputs a pair with equal
complete digests (R = 0 is equality of the two digests, Lemmas H, D').
A trial with R = 0 that is not good is found only if its batch reaches
stage C; Section 7 does not count it.

**What the shipped program holds.** It contains the counted pieces (the
outer step with its random word, the table build of one list word, the
middle step, the three stages of a batch with both budget registers, the
block test), the two lists, and the ledger with E_B and E_C. The loops over
vd, w5 and X2 and step 3 are defined by this text; their counts are in
Section 9.

## 5. The counted pieces on a 64-register machine

A packed 256-bit word holds seven 36-bit lanes (offsets 0, 36, .., 216),
each representing a value modulo 2^32 with four guard bits. A rotation by
r is PROR = ((z >> r) AND A_r) OR ((z << (32 - r)) AND B_r), 5 operations,
reading only the low 32 bits of each lane. x - y with constant x is
(y XOR M) + (x + 1) (M = 2^32 - 1 per lane); subtracting a constant is
adding its negation. Every executed primitive (add, xor, and, or, shift,
compare, branch, load, store, random word) counts 1; shift amounts and load
offsets are instruction fields. The machine model is the 256-bit word RAM
of the cost model with 64 registers.

**The batch in three stages.** Loads are the five table words of list word
j and V[j]; every other operand is a register. Every execution of a stage
executes the same operations.

| Stage | Computes | Ops |
|---|---|---:|
| A | load XA[j] (1); X0 = XA + (-w2), fd = X0 ^ ROL(X15,8), X10 = fd + (S10 + X15) (3); load X6[j] (1) | 5 |
| A | C2: a1 = X6 + (X2 + w7) (1), d1 = ROR(a1 ^ X14,16) (6), c1 = X10 + d1 (1), b1 = ROR(X6 ^ c1,12) (6), a2 = a1 + b1 + w0 (2), z = a2 ^ d1 (1) | 17 |
| A | rule-A test (Lemma A'): zr = z + 2^26, tA = (zr ^ KA) AND ALLA, fA = tA + M (4); x = fA AND B32, compare with B32, branch (3) | 7 |
| B | budget: cB = cB - 1, compare with 0, branch to halt (3) | 3 |
| B | Y14 = ROR(z,8) (5), Y10 = c1 + Y14 (1), Y6 = ROR(b1 ^ Y10,7) (6); fc = X10 + (-X15) (1), X5 = ROR(ROR(fc ^ S5,12) ^ X10,7) (12) | 25 |
| B | load X1[j] (1); C1: a1 = X1 + X5 + w3 (2), d1 = ROR(a1 ^ X13,16) (6), c1 = d1 + X9 (1), b1 = ROR(c1 ^ X5,12) (6) | 16 |
| B | load R[j] (1); ga = R ^ S12 (1); Y1 = a1 + b1 + ga + (-S1 - S6) (3); Y13 = ROR(d1 ^ Y1,8) (6); Y9 = c1 + Y13 (1) | 12 |
| B | E1: a1 = Y1 + Y6 + w12 (2); load Y12[j] (1); d1 = ROR(a1 ^ Y12,16) (6); c1 = d1 + Y11 (1) | 10 |
| B | test of rule A and the filter (Lemma F): wF = (c1 ^ VF) AND MF, fF = wF + M, f = fA OR fF (4); x = f AND B32, compare with B32, branch (3) | 7 |
| C | budget: cC = cC - 1, compare with 0, branch to halt (3) | 3 |
| C | E1 for A and B: c1' (1), b1, b1' (6 each), a2, a2' (2 each), d2, d2' (6 each), c2, c2' (1 each) | 31 |
| C | P = a2 ^ a2', Q = c2 ^ c2' (2); ROR(b1 ^ b1' ^ Q, 7) (7) | 9 |
| C | load V[j] = y (1); e1 = y + Y3 (1); h1 (6), h1' = h1 ^ eta (1); g1, g1' (2); f1, f1' (6 each) | 23 |
| C | fa = ROL(fd,16) ^ S15 (6); e1 + w8 = e1 + fa + (-S0 - S5) (2); e2 (1), e2' (+ DY3, 2); h2, h2' (6 each); g2, g2' (1 each) | 25 |
| C | D1 = P ^ g2 ^ g2' (2); D3 = e2 ^ e2' ^ Q (2); W4 = ROR(P,1) ^ P ^ f1 ^ f1' (8); D6 (xor 2) | 14 |
| C | OR of the four (3), AND M (1), indicator u = T + M (1), acc = acc AND u (1); jump back to the batch loop (1) | 7 |
| | **stage A 29, stage B 73, stage C 112** | |

KA = 0A000300, ALLA = 0B000300, VF = 00008000, MF = 00098188 in every
lane. The stage-A branch is taken (to the out-of-line stages B and C) iff
some lane passes rule A; the stage-B branch falls through to stage C iff
some lane passes rule A and the filter, and otherwise jumps back. Stages B
and C are parts B, C, D and R of winglock's unsubmitted branch-free batch of 193
operations in this order, plus the budgets, the second test and the jump;
stage A is its part A plus the first test. The lines of steps Y and T that the batch
evaluates are exactly those of Section 2 with the table words in place of
their names: XA - w2 = va - X4 - w2 = X0, R ^ S12 = ROL(gd,16) ^ S12 = ga,
and X6, X1, Y12 as they stand; w9 and w11 are not needed for R.

*Indicator and block test.* After the AND in stage C, a lane holds
T = D1 OR D3 OR W4 OR D6 below 2^32, and bit 32 of u = T + 2^32 - 1 is 1
iff T != 0. acc starts at all ones and every stage C sets acc = acc AND u.
After the last batch of an X2 value, acc AND (2^32 per lane) equals the
broadcast 2^32 iff every lane of every batch that ran stage C had T != 0,
so the branch to step 3 (load 2^32, AND, compare, branch: 4 operations per
X2 value) is taken iff some trial of a batch that ran stage C has R = 0
(Lemma D').

*Budgets.* cB and cC are registers holding E_B + 1 and E_C + 1 at the
start of the run; an entry subtracts 1 and branches to the halt when the
result is 0, so stage B is completed at most E_B times and stage C at most
E_C times, and the (E_B + 1)-th entry halts the run with failure.

*Lane bounds.* Static per-lane upper bounds for all inputs are tracked by
the program for every addition: below 4.02, 8, 10, 5.5 and 2 times 2^32 in
stage A, stage B, the E1 part of stage C, the E3 part and the residual
part, all below 2^36, so no carry leaves a lane; XOR, AND and PROR read only
the low 32 bits of lanes or mask the rest. Table words and per-X2 registers
are reduced below 2^32 when they are formed.

*Registers.* 44 registers are resident during the batches: the 10 rotation
masks A_r, B_r (r = 16, 12, 8, 7, 1), 8 global constants (M, ROL(X15,8),
-X15, Y11, Y11', eta, Y3, DY3), 6 constants of the stage tests (2^26, KA,
ALLA, B32, VF, MF), the 2 budget registers, 7 per outer step (S10 + X15,
X14, X13, X9, S15, w5, w5 + delta), 9 per X2 value (-w2, X2 + w7, w0, S5,
w3, S12, -S1 - S6, w12, -S0 - S5), the list pointer and acc. With the live
temporaries the peak is 57 of 64 (the program's liveness count over the
path through all three stages; the other paths are prefixes of it).

**The middle step (per X2 value; 107 operations).** Next X2, mask and end
test (4); the 21 lines of step M in all seven lanes, which form the nine
per-X2 registers directly (each reduced below 2^32); acc = all ones (one
load) and the list pointer reset (1). Every word it reads from memory (the
nine words stored by the outer step for it, the masks for rotations by 24
and 20, the words 1 and 0 and six IV-derived constants) is charged as one
load. Peak 51 registers including the 44 above.

**The table build (per list word; 49 operations).** Load U[j]; the ten
lines of step Y in all seven lanes (Y12 = (U ^ vb) + (-vc); Y0 =
ROL(Y12,8) ^ vd; va = Y0 + (-vb - w6); XA = va + (-X4); X12 = va ^
ROL(vd,16); gc = (X12 ^ M) + (X11 + 1); gb, X6, gd = gc + (-S11);
X1 = ROL(X12,8) ^ gd; R = ROL(gd,16)), three masks to 2^32, five stores
and the loop step (3). Before the build of an outer step the eight words
it reads and its masks are loaded into registers (at most 26 operations);
peak 25 registers.

**The outer step (340 operations).** One fresh uniform 256-bit word (1) and
its words 0 to 3 as vc, D3.d1, S15, S9 (AND; shift and AND three times: 7);
step O in scalar form (each 32-bit addition or subtraction counted 2 with
its mask, rotation 4, XOR 1), the 24 packed words that the build, the
middle step and the batch read (each broadcast to seven lanes and stored, 8
operations), the next-w5 loop step and the loads of the seven per-outer
registers of the batch.

*Self-test of the shipped program.* `python3 experiments/s8stage.py
--selftest 2000 9`, run from the repository root, builds 2,000 cases (the
seven context words from SHAKE-256 of the seed, the random word of the
outer step holding the four coin words in words 0 to 3 and random words
4 to 7; every fourth case is the last list word; in every fifth each
context word is 0, 2^32 - 1 or random). Each case runs the counted outer
step from the random word, the table build of one list word, the middle
step, the three stages of one batch (stages B and C computed whatever the
decisions, the accumulator changed only as in the staged flow) and the
block test, and checks: the outer step takes exactly the four coin words
from the random word and every packed word it stores equals the value of
step O, every table word equals step Y for its lane's member, every per-X2
register equals step M; and for every lane it builds the trial's messages
A, B by steps O, M, Y, T, S2, S3, compresses them with the program's own
2-round compression and with `verifier/blake3.py blake3(m, 2)`, and checks:
X3, X7, X11, X15 after round 0 are the constants, digest words 0, 2, 5, 7
agree, Y4 = member in S8 for both, eta = 830303cf; bit 32 of the stage-A
flag is 1 iff h1 of E3 violates rule A, bit 32 of the stage-B flag is 1 iff
rule A or the filter on c1 of E1 fails; the four packed words equal D1, D3,
ROL(D4, 7) ^ D1 and D6 computed from the XOR of the two digests on words 1,
3, 4, 6, the packed T equals their OR, and bit 32 of the lane's indicator
is 1 iff the digests differ; both decisions equal 'some lane passes'; and
the block test is taken exactly when some lane of a batch that ran stage C
has equal digests. Result (`selftest_final`): 14,000 of 14,000 lanes right
with the verifier, 14,000 of 14,000 flags right, 2,000 of 2,000 decision
pairs and block tests right, 2,000 of 2,000 cases with every stored word
right; 29, 73 and 112 operations in every execution of stages A, B and C
(parts 29, 73, 43 + 48 + 21) and 4 in every block test; 340, 49 and 107
operations in every outer step, build and middle step; static bounds 4.02,
8, 10, 5.5, 2 times 2^32; peaks of 57, 25 and 51 registers. Pattern tests
on constructed words: the indicator and the block test (blocks of 1, 2 and
3 batches, all 128 zero/nonzero lane patterns, twice) 768 of 768; the
stage-A test (all 128 patterns of lanes passing rule A, passing lanes random
words with the five conditions set, failing lanes with one or more of them
violated, guard bits random, twice) 256 of 256; the stage-B test (all
16,384 pairs of rule-A and filter patterns of the seven lanes) 16,384 of
16,384; the budget registers (a register holding k lets exactly k - 1
entries pass, k = 1, 2, 3, both budgets) right. The 65,536 member numbers
give 65,536 distinct members of S8; Lemma B holds for 6 of 6 betas. Exit
status 0 only if all of these hold, and only if `verifier/blake3.py` was
imported. No real lane with R = 0 occurs at this size; the taken branch is
covered by the pattern tests. Three deliberately broken copies fail it (50 cases each): KA
with bit 24 set (stage-A patterns 2 of 256 right, flags 337 of 350), VF
with bit 3 set (stage-B patterns 2,108 of 16,384 right), and Y3 in place
of DY3 in e2' (0 of 350 lanes right).

## 6. Experiments (organizer-run)

`experiments/s8stage.py`, standard library only, seeds expanded by
SHAKE-256, no BLAKE3 import in organizer mode.

- `half-collision`: per seed, the seven context words (vc, vd, D3.d1, S15,
  S9, w5, X2) and a member number of S8; returns the pair of Theorem 1.
  Event: digest words 0, 2, 5, 7 agree (exact, all seeds). Observations:
  the counted outer step (from a 256-bit word whose words 0 to 3 are the
  four coin words), table build of the member's list word and middle step,
  then the three stages of the batch holding the member and the block test:
  stage_a_ops 29, stage_b_ops 73, stage_c_ops 112, block_test_ops 4,
  outer_ops 340, build_ops 49, middle_ops 107, pieces_right 1, lanes_right 7
  (four packed words and the indicator equal to the forward computation),
  flags_right 7 (both stage flags equal rule A, and rule A with the filter,
  of the forward computation), decisions_right 1, tests_right 1,
  member_in_s8 1 (predicted for every seed).
- `class-filter`: per seed, a context and nine consecutive batches (63
  members) of S8 run as one block in the staged flow with the block test,
  after the counted pieces; returns the seed member's pair (same event).
  Observations per seed: members 63, in_s8 63, y4_equal 63, eta_equal 63,
  lanes_right 63, flags_right 63, decisions_right 9, tests_right 1,
  pieces_right 1, lemma_b 6 (predicted for every seed), and the counts
  rule_a_lanes, filter_lanes, filter_and_rule_a_lanes (rates near 2^-5,
  2^-6, 2^-11 per trial), stage_b_batches and stage_c_batches (at most the
  first and the third count of the seed). Each seed is one context, whose
  members are not independent. The expected totals per run of 256 seeds
  under M are 504, 252 and 7.9 lanes and 459.1 and 7.9 batches; rule A
  clusters by context, so no per-run range is predicted.

*Replays (preregistered; participant-run local replays using the
repository's `experiments/runner.py`).* Before any replay of the first
build of this version, its program (SHA-256 e77c7274...397096b1), the
harness (which runs `experiments/runner.py` of the repository with
`verifier/blake3.py` as digest) and the list of 41 nonces (the public seed,
and holdout_nonce = the first 32 hex digits of SHA-256 of 'blake3-r2-v101
replay NN', NN = 01 to 40; our own nonces, not organizer holdouts) were
fixed and hashed, and all 41 runs were then made. Two earlier frozen
copies: the first (67,811 bytes) was refused by the runner's 64 KiB source
limit before any experiment ran, and only comments and docstrings were
shortened; the second (aa60cb33...7587a4) differs from the first build
only by a blank line at its end, which `git diff --check` rejects; its 41
runs gave results identical in every field except running time. The
revision after our review changed only the ledger and the printout of the
exact stage values (no experiment code); the shipped program (SHA-256
e027eb6f...1474709) was frozen and hashed in the same way and the same
41 nonces were rerun one after another: all 41 results are identical to
those of the first build in every field except running time. (A first
attempt at this rerun started three harness processes at once; they share
one temporary program file, and 2 of the 41 ended in harness errors; the
other 39 were identical as well. It was discarded for that reason and is
reported here.) In every run both experiments have 256 of 256 successes,
no repeated pair, and every predicted observation exact for every seed.
Totals of 16,128 lanes per run: rule A 419 to 663 (mean 515.4, sd 50.4,
about twice the binomial value because of the context clustering),
filter 209 to 295 (mean 254.4), both 3 to 14 (mean 7.4, sd 2.7);
batches entering stage B 212 to 316 of 2,304 (mean 259.9, sd 22.7) and
stage C 3 to 14 (mean 7.3), never more than the lanes with both; on the
public seed 462, 247, 14, 233 and 14. As ratios to M over the 41 runs
(standard error from the run-to-run sd; runs use independent contexts):
batches entering stage B 0.566 +- 0.008 of 459.1, rule A and the filter
0.94 +- 0.05 of 7.875, rule A 1.023 +- 0.016 of 504. These agree with the
uniform sample of Section 8.2 (0.546 and 1.00001; rule A 1.00004, so its
2.3% excess here is within 1.5 standard errors and rule A alone is not a
part of H1 (ii)). The public seed's 14 lanes with both is the largest
total of the 41 runs (1.78 times 7.875); one run of 256 clustered contexts
cannot resolve the 25% margin of (ii). One execution of `class-filter`
takes 1.5 to 4.6 s on our machine (one execution in the first build's
replays took 35 s while other jobs held the machine at a load average of
about 35), `half-collision` under 0.7 s.

*This package's program.* The shipped `experiments/s8stage.py` (SHA-256
b30ba566...fc6c7eab, 63,932 bytes) differs from 098e66f4's program
(e027eb6f...1474709) in three places only: the two ledger constants
PREMISE[0] (1.01 -> 0.60) and BUDGET[0] (1.02 -> 0.61), and the credit
lines of its docstring. No code that the experiments, the self-test or
`--count` execute was changed; `--ledger` evaluates the formula of
Section 9 with the new constants. Both experiments were run for this
package through the repository's organizer runner
(`experiments.run_experiments`, which executes the program only in its
pinned networkless Docker sandbox) on the public seed: 256 of 256
successes in each, no repeated pair, every predicted observation exact
for every seed, and class-filter totals 462, 247, 14, 233 and 14,
identical to 098e66f4's public-seed run. The same
40 nonces as 098e66f4's replays (the first 32 hex digits of SHA-256 of
'blake3-r2-v101 replay NN', NN = 01 to 40) were then run the same way,
after the program was frozen. All 41 runs have 256 of 256 successes in
both experiments, no repeated pair, and every predicted observation exact.
The class-filter totals have the same ranges, means and standard
deviations as 098e66f4's 41 replays: rule A 419 to 663 (mean 515.4,
sd 50.4), filter 209 to 295 (mean 254.4), both 3 to 14 (mean 7.4),
stage-B batches 212 to 316 (mean 259.9, sd 22.7) and stage-C batches 3 to
14 (mean 7.3). The self-test was not
rerun for this package; its result above is 098e66f4's, for a program
that differs only in the lines named.

Observations are the program's own and untrusted; they check the
generator, the class, the stage tests and the counted pieces against a
forward computation of real messages. They do not measure H1.

## 7. Success probability

The probability space is the V * 2^32 random words of step 2, one per outer
step, independent and uniform. Outer step k (k = 1, .., V * 2^32) is a fixed
pair (vd, w5), and all its trials, stage decisions and residuals are a
function of that pair and its own random word r_k.

**H1 (score-critical; the only premise).** Over the random words of the
algorithm:

(i) the N = V * 2^80 trials behave with respect to "good" (R = 0, rule A
and the beta filter) like independent events of probability at least
F * 2^-128 each, F = 92,675,072 (half of the exact count 185,350,144 of
Section 8; 2^26.4657), to the extent that the probability that no trial is
good is at most exp(-lambda) + 0.002 with lambda = N * F * 2^-128 =
0.4980001; and

(ii) averaged over the V * 2^64 * 9,363 batches of the run, the
probability that a batch has a trial satisfying rule A (and so enters
stage B) is at most 0.60 p_B, and averaged over the N trials, the
probability that a trial satisfies rule A and passes the filter is at most
1.25 * 2^-11. Under the same seven-word model M that gives the count of
(i), with the distinct trials of a batch independent as in (i), these
probabilities are exactly p_B = (9,362 (1 - (31/32)^7) + 1 - (31/32)^2) /
9,363 = 0.1992628 and 2^-11 (Section 8.2: 2^27 of the 2^32 words h1
satisfy rule A, 2^26 of the 2^32 words c1 pass the filter, h1 and
c1 = d1 + Y11 are independent uniform words of M, and 9,362 batches hold
seven distinct trials and one holds two). (ii) asserts, as averages over
the run, 0.60 times the first and 1.25 times the second. The stage-B value
lies below its M value because rule A clusters by context. It rests on two
uniform samples of the run (Sections 8.2 and 8.3), not on M.

Part (ii) is a statement about first moments only. It says nothing about
how passing trials are distributed inside a batch, a context or an outer
step; rule A is known to cluster by context, which lowers the share of
batches entering stage B well below p_B (Sections 8.2, 8.3). The stage-B
part of (ii) uses this effect only through the run average that the two
samples estimate; nothing below depends on how passing trials are
distributed inside a batch, a context or an outer step.

**Lemma C (Chernoff bound).** Let X_1, .., X_n be independent random
variables with values in [0, 1], and mu_H >= E[X_1 + .. + X_n]. Then for
0 < delta <= 1, P(X_1 + .. + X_n >= (1 + delta) mu_H) <= exp(-delta^2 mu_H / 3).
*Proof.* For t > 0 and x in [0, 1], e^(tx) <= 1 + x (e^t - 1) (convexity),
so E e^(t X_k) <= 1 + (e^t - 1) E X_k <= exp((e^t - 1) E X_k), and by
independence E e^(t sum X_k) <= exp((e^t - 1) mu_H). Markov's inequality
with t = ln(1 + delta) gives P(sum >= (1 + delta) mu_H) <=
exp(mu_H (delta - (1 + delta) ln(1 + delta))), and
(1 + delta) ln(1 + delta) >= delta + delta^2 / 3 for 0 <= delta <= 1. QED.

**Theorem 2 (budgets).** Let S_B and S_C be the numbers of batches that
would enter stage B and stage C in a run without budgets. If H1 (ii) holds,
then P(S_B > E_B) <= exp(-7.1 * 10^10) and P(S_C > E_C) <= exp(-2.3 * 10^9).

*Proof.* Write S_B = sum over k of S_k, S_k the number of batches of outer
step k that enter stage B. S_k is a function of r_k, so S_1, S_2, .. are
independent, and 0 <= S_k <= m = 9,363 * 2^32, the number of batches of an
outer step. By Lemma A' a batch enters stage B iff one of its distinct
trials satisfies rule A (the repeated lanes of the last list word hold the
same trial), so E S_B is the sum over all V * 2^64 * 9,363 batches of the
probability of this event, at most 0.60 p_B V 2^64 9,363 by H1 (ii). Put
X_k = S_k / m and mu_H = 0.60 p_B V 2^64 9,363 / m = 7.767 * 10^14. Since
E_B >= 0.61 p_B V 2^64 9,363 = (1 + delta) mu_H m with delta = 1/60,
Lemma C gives P(S_B > E_B) <= P(sum X_k >= (1 + delta) mu_H) <=
exp(-delta^2 mu_H / 3) = exp(-7.19 * 10^10). For stage C, a batch enters
only if one of its distinct trials satisfies rule A and the filter
(Lemma F), so S_k is at most the number of such trials of outer step k
(a union bound, valid for any dependence between the trials of a batch)
and E S_C <= 1.25 * 2^-11 * N by H1 (ii); mu_H = 1.25 * 2^-11 * N / m =
2.775 * 10^13, E_C >= 1.27 * 2^-11 * N gives delta = 0.016, and the bound
is exp(-2.37 * 10^9). QED. (`python3 experiments/s8stage.py --ledger`
prints E_B, E_C, mu_H, delta and both exponents.)

**Success.** The run with budgets executes exactly as the run without them
until a budget is spent, and no budget is spent if S_B <= E_B and S_C <=
E_C. If moreover some trial is good, the completeness argument of
Section 4 shows that step 3 outputs a pair of distinct messages of 55 and
63 bytes with equal complete digests. So, under H1,

    P(success) >= 1 - (exp(-lambda) + 0.002) - exp(-7.1 * 10^10) - exp(-2.3 * 10^9)
               >= 1 - exp(-0.4980001) - 0.002 - 10^-300 = 0.39025 >= 0.39.

The time of Section 9 holds for every value of the coins: stage B and
stage C are charged at their budgets. Sensitivity: with a good-trial rate
f * 2^-128 the same search reaches 0.39 only for f >= 2^26.4645 (lambda >=
0.49758); with the uniform rate (f = 1) it needs 2^127 trials and gives
120.96. The margin between (ii) and the budgets is
what Lemma C uses: with 0.609 p_B and 1.26 * 2^-11 in (ii), delta = 0.0016
and 0.0079, and the two bounds are still exp(-7.0 * 10^8) and
exp(-5.8 * 10^8).
## 8. Evidence for H1

### 8.1 Part (i): the count of good trials

**The seven-word model M (c66f230d).** By Section 3, R depends on the
constants and seven words: for E1 d1, b1, a2 (message A; a1 and d1 are
shared), for E3 Y4, Y9, w8 and h1. Y4 runs over S8 equally often. M says the
other six behave over the trials like independent uniform words. Under M a
trial is good with probability r * 2^-128, where r * 2^-128 is the share of
solutions of R = 0 with rule A and the filter among (Y4 in S8) x 2^192.
Using the conditions of Lemma N and its E3 analogue, R = 0 iff, with
tau = a2 ^ a2', eps = c2 ^ c2', beta of E1 and eta, psi the first-half d, b
differences of E3: E3's c and a output differences equal tau and eps,
psi = tau ^ ROR(tau, 1), and eta = eps ^ ROL(beta ^ eps, 1).

**How r is counted (shipped: `python3 experiments/s8stage.py --count`).**
For a beta, an outcome is (tau, eps).
N1 is the number of (d1, b1, a2) in 2^96 with this beta (Lemma B carry
conditions on c1) giving the outcome; N3 is the number of
(Y4 in S8, h1, Y9, w8) in 2^16 * 2^96 for which E3 produces eta, psi, eps,
tau and h1 satisfies the rule. Both are counted exactly by carry automata
over the 32 bit positions in exact integer arithmetic; no sampling and
no fallback. Then r = sum over outcomes of N1 * N3 / (2^16 * 2^64). Parts
are non-negative, so any subset of betas or outcomes gives a lower bound.
N1 (function `N1`): for each pattern pa of a2 on tau the number of b1
patterns on beta with DELTA + (beta - 2 Sb) = tau - 2 pa (two candidates
by `solve_sub`), times, for each pattern px of d1 ^ a2 on tau, a 16-state
automaton over (d1, d2 = ROR(d1 ^ a2, 8)) whose state is the four carries of
c1 = d1 + Y11, c1 + DY11, c1 + d2 and c1' + d2'; free bits of b1 off beta
give the factor 2^(32 - |beta|). N3 (function `N3`): for each pattern of
Y4 ^ g1 on P = ROL(psi, 12) the e2 patterns on eps from the E3 carry
condition, the h1 patterns on eta (rule A applied) with their g1 pattern,
and a 4-state automaton over (g1, h2) for the c-output difference tau;
members of S8 enter through their bits on P. The program lists the 85
outcomes of the six betas (the tau values; eps is fixed by beta) and prints
N1, N3 and the part of each.

**The count.** For the six betas of T6 (all with an eps; they fix 11, 11,
11, 11, 13, 13 bits of c1) the outcomes are enumerated without a bound on
the weight of tau, and:

| beta | outcomes (full class) | part, full class | outcomes (S8) | part, S8, rule A |
|---|---:|---:|---:|---:|
| 18b0e098 | 14 | 71,698,432 | 7 | 67,698,688 |
| 18d0e098 | 19 | 54,005,760 | 12 | 50,790,400 |
| 18b1a098 | 16 | 25,692,160 | 16 | 51,384,320 |
| 18d1a098 | 18 | 8,429,568 | 12 | 13,246,464 |
| 18b3e098 | 8 | 1,566,720 | 4 | 1,474,560 |
| 18d3e098 | 10 | 838,656 | 6 | 755,712 |
| T6 | 85 | 162,231,296 | 57 | **185,350,144** |

For the heaviest beta 18b0e098 (eps = 6e21be55) the seven nonzero S8
outcomes are (N1, N3 with rule A, part): tau 285020a0: 2^51, 12 * 2^50,
25,165,824; 185020a0: 2^51, 8 * 2^50, 16,777,216; 385020a0: 2^50,
16 * 2^50, 16,777,216; 175020a0: 2^49, 12 * 2^50, 6,291,456; 685020a0:
2^49, 3 * 2^50, 1,572,864; 275020a0: 2^49, 2 * 2^50, 1,048,576; 675020a0:
2^47, 2^49, 65,536; sum 67,698,688. Its seven other outcomes (tau with
bit 14 set) have N3 = 0 in S8.

The S8 total is the same exact integer with and without rule A: among
these outcomes no S8 solution violates rule A. The claimed factor
F = 92,675,072 is 185,350,144 / 2. All 15 betas with k <= 14 and the same counter give
185,355,230.33 for S8 with rule A (162,263,084.49 for the full class without
rule; 144,123,339.49 with rule A).

*Checks of the count.* (i) Three counting programs agree exactly: our C
counter, the shipped Python port (`--count`: all 85 outcomes, 57 nonzero,
the six parts and 185,350,144 in about 2.5 minutes; `--count all` also
gives the same total without rule A), and a counter written independently
by another helper agent, which gives 183,119,872 for the four heaviest
betas in S8 with and without rule A (1.976 F from these four alone).
A fourth, sampling estimator written by our review agent (Monte Carlo over
(y, h1, g1) for E3 and (c1, b1) for E1, exact automaton over e2 and a2)
gives 185,477,038 +- 878,331 (ratio 1.0007 +- 0.0047), with all 57 nonzero
outcomes within noise and the 28 zero outcomes zero. Per member of S8 the
exact factor (all 15 betas, rule A) lies between 184.57M and 186.14M, so
every member is above 1.99 F. (ii) The full-class parts and outcome
numbers equal the published table of c66f230d for all six betas
(computed there by a different program and recounted by another AI model);
the full-class rule-A splits for all 15 betas, 162,243,466.25 /
144,123,339.49 / 123,244,351.65 for 4 / 5 / 6 conditions, equal c66f230d's
published splits minus their parts for betas with k >= 15. (iii) Brute
force at 8-bit word size (rotations 4, 3, 2, 1) against the same counter:
52 random constant sets, 1,372,942 E1 outcomes and 19,258 E3 outcomes and
all 9 nonzero R = 0 totals equal; 48 further sets: 22,892 outcomes with the
per-member split (329,346 comparisons), the per-h1-pattern split
(1,471,448) and rule restrictions (22,892) all equal, no mismatch. (iv) The
count was rerun for this package with identical output.

**Real trials in the order of 2bb5d604 (participant measurements, C programs
on steps S1/T of c66f230d).**
In 4,096 random contexts with all 65,536 S8 members (2^28 trials): rule A
holds for 2^-4.9993 of the trials; the filter passes for 2^-6.006 of the
rule-A trials (model 2^-6). Over 896 draws of the seed words with 256
contexts each (229,376 contexts), rule A holds for 2^-5.0002 of the
trials, rule A and the filter for 2^-10.9997.

*Deeper events.* With real (c1, b1) from steps S1/T and a2 counted exactly,
the E1 part of the count has real/model 1.0086 over 2^33.8 S8 trials. For
E3 with real (y, h1, g1) and e2 counted exactly, partial events (rule A,
the g1 difference and the e2 carry conditions, probability about 2^-38 per
trial) match the model per outcome. The S8 advantage appears on real
trials: per outcome, the ratio of this partial event between S8 and the
other seven eighths of the class is, where the counter's per-member ratio
is 1, 2.333 and 7, 0.99-1.03, 2.20-2.47 and 5.15-8.66 on real trials
(2^33.8 each) and 0.98-1.02, 2.18-2.44 and 5.75-10.00 on draws from the
model itself. The full E3 event has too few hits at this sample size (25
to 38 nonzero trials in 2^33.8) to resolve the ratio: the same estimator
gives 0.80 +- 0.20 on real trials and 0.51 +- 0.15 on model draws, so it
tests neither direction. On 2^26 S8 trials against
2^28.8 trials of the other seven eighths of the class, the low 13 bits of
E3's g1 and e2 are uniform and homogeneous (chi-square z between -1.8 and
1.4); h1 restricted to the eta bits is not uniform (z = 11.6), and an
unrelated control 1/8 subset of the class shows the same (z = 21.3), so
this is the per-context clustering already reported for rule A by
c66f230d, not a property of S8.

**Real trials in the order of 60f94c5c (participant measurement for our
unsubmitted branch-free draft in this order, `rt2l.c`, a C program whose event counts equal those of the
shipped program's forward computation on 65,536 trials).** Run layout: per
run, the four coin words, 4 outer steps (vd = 0, w5 = 0..3), 2^16
consecutive values of X2 and all 65,536 members of S8, 2^34 trials; six
runs. The same program in the order of 2bb5d604 (six runs, 4 values of vd,
2^16 consecutive X14, all members) gives the comparison. Over 2^36.585
trials each:

| event | this order | real/model | other order | this/other |
|---|---:|---:|---:|---:|
| rule A | 2^-5.0000 | 1.0000 | 2^-5.0003 | 1.0002 +- 0.0000 |
| filter | 2^-5.9999 | 1.0000 | 2^-6.0000 | 1.0000 +- 0.0000 |
| rule A and filter | 2^-10.9999 | 1.0001 +- 0.0001 | 2^-11.0001 | 1.0001 +- 0.0002 |
| beta in T6 (model 2^-8.8301, exact) | 2^-8.8299 | 1.0001 +- 0.0001 | 2^-8.8301 | 1.0001 +- 0.0001 |
| beta in T6 and rule A | 2^-13.8300 | 1.0001 +- 0.0004 | 2^-13.8297 | 0.9998 +- 0.0005 |
| low 12 bits of n zero (Lemma N word) | 2^-10.9277 | | 2^-10.9276 | 0.9999 +- 0.0002 |
| beta in T6 and low 8 bits of n zero | 2^-15.4461 | | 2^-15.4455 | 0.9996 +- 0.0009 |
| E3: g1 ^ g1' = ROL(psi,12), tau 285020a0 | 2^-14.0004 | | 2^-14.0000 | 0.9998 +- 0.0006 |
| low 16 bits of D1 and of D3 zero | 2^-30.40 (73) | | 2^-30.28 (79) | 0.92 +- 0.16 |

The events without a closed-form model value have the same rate in both
orders; the deeper checks above (E1 part, E3 partial events at 2^-38) were
made in the order of 2bb5d604 and are not repeated here. The stages do not
change which trials are run or their residuals, only which are examined; a
fresh random word per outer step changes the coin words from one per run to
one set per outer step, which the measurements of 8.2 use.

### 8.2 Part (ii): the stage events

**Exact values under M.** Rule A reads bits 0, 1, 2, 3, 16 and 17 of h1;
of the 64 patterns of these bits exactly 2 satisfy it (bits 0, 16, 17 zero,
bit 1 one, bits 2 and 3 different), so 2 * 2^26 = 2^27 of the 2^32 words h1
do. The filter reads bits 3, 7, 8, 15, 16 and 19 of c1 (the mask 00098188);
exactly one pattern passes, so 2^26 of the 2^32 words c1 do. Under M, h1 and
the E1 word d1 are independent and uniform, and c1 = d1 + Y11 is uniform, so
a trial satisfies rule A with probability 2^27 / 2^32 = 2^-5 and rule A and
the filter with 2^27 * 2^26 / 2^64 = 2^-11 exactly. With the distinct trials
of a batch independent under M (as in H1 (i)), a batch of seven distinct
trials enters stage B with probability 1 - (31/32)^7 = 0.1992775 and the
last batch of a list (two distinct trials) with 1 - (31/32)^2, so the share
over the 9,363 batches of a list, which is the run average under M, is
p_B = (9,362 (1 - (31/32)^7) + 1 - (31/32)^2) / 9,363 =
32,052,445,611,625 / 160,855,115,169,792 = 0.1992628. `python3
experiments/s8stage.py --count` enumerates the 64 + 64 patterns and prints
the integers 2^27, 2^26 and 2^53 and the fraction p_B next to the count of
8.1; `--ledger` uses the same fraction. H1 (ii) asserts 0.60 p_B and
1.25 * 2^-11 as run averages; the budgets are 0.61 p_B = 0.1215503 batches
per batch for stage B and 1.27 * 2^-11 per trial (0.0043405 per batch) for
stage C.

**Real trials on a uniform sample of the run (098e66f4's participant
measurement, `rtuni.c`, Appendix A; preregistered).** Before it ran, the program, the
cross-check, the plan (16 runs of 1,024 outer steps with 256 values of X2
each, seeds 20261101 to 20261116) and the analysis below were fixed and
hashed. Each outer step draws vd uniformly below V, w5 uniformly and its
four coin words fresh (as step 2 does), and each of its 256 values of X2
uniformly; all 65,536 members of S8 run in the 9,363 batches of the
algorithm. Together 16,384 outer steps, 2^38.000 trials and 39,271,268,352
batches. Outer steps are independent and uniform over the run's outer
steps and X2 is uniform, so the mean over outer steps of each per-outer-step
ratio is an unbiased estimate of the run average that (ii) bounds, with
standard error sd / sqrt(16,384). The counts equal those of the shipped
program's forward computation and batching on two complete drawn contexts
(`rtunicheck.py`, seeds 7 and 13; 65,536 trials each).

| event | count | per-outer-step ratio to M: mean +- s.e. (sd) | 99.9% upper bound | (ii) factor | budget |
|---|---:|---:|---:|---:|---:|
| batch enters stage B | 4,274,878,152 | 0.54629 +- 0.00047 (0.0598) of p_B | 0.5477 | 0.60 | 0.61 |
| rule A and filter (trial) | 134,218,862 | 1.00001 +- 0.00009 (0.0121) of 2^-11 | 1.0003 | 1.25 | 1.27 |
| rule A (trial; not in (ii)) | 8,590,304,647 | 1.00004 +- 0.00004 (0.0052) of 2^-5 | 1.0002 | | |
| filter (trial; not in (ii)) | 4,294,942,914 | 0.99999 of 2^-6 (pooled) | | | |
| batch enters stage C | 132,822,030 | 0.0033822 per batch | | | 0.0043405 |

Per run (1,024 outer steps) the stage-B ratio lies between 0.5428 and
0.5495 and the stage-C trial ratio between 0.9993 and 1.0007. The largest
ratio of one outer step is 0.846 for stage B and 1.050 for rule A with the
filter; the largest stage-B share of one context (one X2 value, 9,363
batches) is 1.128 p_B, so single contexts can exceed p_B, which (ii) does
not exclude: it bounds the run average. A first invocation with a
malformed seed list (on this machine `seq` printed 2.02611e+07, so every
process ran seed 2) completed one run of the same size before it was
stopped; it gives 0.5473, 0.9995 and 1.0001 and is not used.

**Earlier and other measurements of the same events (all reported).**

- *Run layout with consecutive indices* (`rtstage.c`, which differs from
  `rtuni.c` only in how it chooses the indices, vd = 0..15 for its sixteen
  runs, w5 = 0..63 and 4,096 consecutive values of X2, and in the
  statistics it prints; fresh coins per outer step; 2^38.000
  trials, 1,024 outer steps; its counts equal the shipped program's on two
  contexts, `rtcheck.py`, seeds 5 and 11): stage-B share 0.101710, 0.5104 of
  p_B (per outer step 0.42 to 0.77 of p_B; largest context 0.989 p_B); rule
  A and the filter 1.00001 of 2^-11 (per run of 64 outer steps 0.9994 to
  1.0007); rule A 1.00008 of 2^-5; stage-C share 0.0033793. Consecutive X2
  values give a lower stage-B share than uniform ones, so this layout is
  not a sample of the run; Theorem 2 uses neither.
- *Review-agent run* (a uniform variant of `rtstage.c`; seeds 9101 to
  9108; 4,096 outer steps of 128 uniform X2 values, 2^35 trials, run once):
  stage B 0.5469 of p_B, rule A and the filter 0.99978 of 2^-11, rule A
  1.00013 of 2^-5.
- *The 41 replays of `class-filter` (Section 6),* 2,304 full batches and
  16,128 lanes each, one context per seed: stage B 0.566 of the M value
  (mean 259.9 of 459.1; runs 0.46 to 0.69), rule A and the filter 0.94 of
  2^-11 (mean 7.4 of 7.9; 1.78 on the public seed, which has the largest
  of the 41 totals, 14), rule A 1.023 +- 0.016 of 2^-5 (sd 50.4 over the
  41 runs; rule A alone is not part of (ii)). A run is 256 clustered
  contexts, so single runs do not resolve these margins.

**Scope and limitations of H1.** The factor F = 92,675,072 is assumed; it
is half of the exact model count 185,350,144 (margin 2.000), which the
organizer experiments do not measure. M is untested at probability 2^-100.5
(the R = 0 rate 185,350,144 * 2^-128);
it was compared with real trials on events of probability down to about
2^-38 per trial here (E1 part, E3 partial events) and down to about 2^-40
for one call by c66f230d; the full event is far below anything measured. M fails
inside one context (rule-A share varies by context); only averages over
contexts are measured. The constants, the class and rule A were chosen by
c66f230d to maximize a count of the same kind; S8 was chosen by us from the
exact per-member factors of all 524,288 class members. Recomputed for this
package, S8 is the best of all 8,992,320 sub-classes of 2^16 members given
by three independent conditions, each fixing one free bit of e1 or the XOR
of two (three of them describe S8 itself). The selection matters: the full
class with rule A and no sub-class already counts 144,123,339 over all 15
betas (1.555 F; betas outside T6 add under 32,000), so S8 supplies a
factor 1.29 of the margin 2.000: if S8's advantage under M were entirely
an artifact of this selection, S8 trials would have the class rate, and the
class count with rule A (1.555 F) is still at least F. The filter was chosen to
contain T6. A choice that is best under M says nothing about M and may
favour parameters where M overstates; the real-trial ratios above are the
check we have; the order of enumeration (Section 2) was not chosen with
any count. 37% of the S8 count (44% in the full class) comes from one
beta, 18b0e098. The trials of one outer step share its four coin words (outer
steps have independent coins); the trials of one context (outer step and
X2) differ only in Y4, and trials with the same outer step and member share
Y12 and w5, two of E1's inputs, over all 2^32 values of X2, while E1's a1
varies with Y1 and Y6; for part (i) independence is assumed. Part (ii) is
a first-moment statement: its run averages are estimated without bias from
two independent uniform samples of the run (8.2: 2^38 trials, stage B at
0.546 p_B, rule A with the filter at 1.00001 * 2^-11; 8.3: 2^39 trials,
0.54644 +- 0.00023 p_B and 0.99995 * 2^-11; asserted 0.60 p_B and 1.25 * 2^-11),
and the run has 2^100.5; no independence is assumed for it, and the
budgets follow from it by Theorem 2. The sample of 8.2 is 098e66f4's and
that of 8.3 is this package's; both run on the participant side; the organizer experiments see the stage events only
in 16,128 clustered lanes per run.

**Run selection.** No organizer-run count or frequency supports F, the
averages of H1 (ii) or the success probability. Every predicted observation
of Section 6 is an exact per-seed predicate, so no choice among runs can
make it pass; the rule-A, filter and stage-entry totals are reported for
information, every recorded replay of this version included (Section 6).
No parameter, version, seed or nonce was chosen on replay outcomes: S8, the
filter and F come from the model count, the stage tests from Lemma A and
the filter. In 098e66f4 the margins of (ii) and the budgets were set twice, and both
times before a measurement that is reported in full: in the first build
1.01 and 1.02 times the per-trial rates, before the run-layout measurement
of 8.2 (a 2^21-trial smoke test of its program before it, stage-B share
0.104, is not included); after our review, the batch-level stage-B form
(chosen after that measurement, with the margin 1.01 and budget 1.02 kept)
and 1.25 and 1.27 for stage C, before the preregistered uniform sample of
8.2 (two timing runs of 2^19 and 2^24 trials before it are not included;
the malformed-seed run is reported above). The stage-C change only
weakens (ii). The stage-B change replaces a per-trial bound by a bound on
the batch-level event that Theorem 2 needs, which is neither weaker nor
stronger, and lowers the stage-B budget from about 1.02 * 7 * 2^-5 = 0.2231
to 1.02 p_B = 0.2032 per batch; the measured run average is 0.1089 per
batch. This package set the stage-B margin a third time, to 0.60 p_B
(budget 0.61 p_B = 0.1216 per batch), after reading 098e66f4's sample and
before running its own; the plan of that sample fixed the value and the
rule that nothing is changed unless its bound is at most 0.60 p_B
(Section 8.3). The margin of the premise over the two sample means is
1.10 and 1.10.



### 8.3 This package's sample of the stage events (independent, preregistered)

**What is measured.** For outer step k, let Z_k be the share of its batches
that enter stage B (some distinct trial of the batch satisfies rule A),
counted over all 9,363 batches of each of its sampled values of X2. The
run average that H1 (ii) bounds is E Z_k, where the outer step (vd below
V, w5, and the four coin words vc, D3.d1, S15, S9) and X2 are uniform.
Z_k lies in [0, 1]. Outer steps drawn independently and uniformly, each
with independent uniform X2 values, therefore give independent,
identically distributed Z_k whose mean is exactly the run average. No
model is involved: this is sampling from the run's own index space.
The same holds for the per-trial share of rule A with the filter.

**Program and cross-check.** `sbmeas.c` (Appendix B) was written for this
package. It does not reuse 098e66f4's measuring code. It computes steps O,
M and Y from the proof text, and for every trial runs C2 forwards as a G
call, takes Y14 and tests rule A on h1 = ROR(Y14 ^ (Y3 + y), 16) (the
first two assignments of E3; Lemma A is not used). When rule A holds, it
runs D0, C1 and E1 forwards to c1 and tests the filter. Batches are
members 7j .. 7j + 6 in the member order of Section 3, and the last batch
holds members 65,534 and 65,535. `ref.py` (Appendix B) builds the 16
message words and both messages from the eight free words. It runs its
own forward 2-round compression of message A and reads h1 of E3 and c1 of
E1 from it. On 3,000 random cases it checked these against
`verifier/blake3.py` (both digests), checked that X3, X7, X11, X15 are the
constants, that X2 is the chosen word, that Y4 = y in both messages, that
Y3 and Y11 are the constants of Fact P, and that digest words 0, 2, 5 and
7 agree. All 3,000 cases passed. `crosscheck.py` runs all 65,536 members
of one complete drawn context through `ref.py`, checks every 64th digest
of A against `verifier/blake3.py`, and compares with `sbmeas --context`
the counts of rule A, rule A with the filter, the stage-B and stage-C
batches, and a hash over all 65,536 per-trial flags. On seeds 11, 12 and
13 it found 2091/36/956/35, 2127/29/981/29 and 2330/37/1118/37, all equal,
with equal flag hashes.

**Plan (preregistered).** Before the run, the program, `ref.py`,
`crosscheck.py`, the analysis `analyze.py` and the plan were fixed and
hashed (SHA-256 7b4f22ed...5c037b2, afcde01c...00bba1ce,
414f513f...6738d6, 48e43aff...47a042, e4d5b4e7...6c26c). The plan was
8 processes `./sbmeas 8192 128 SEED` with SEED = 3300001 .. 3300008:
65,536 outer steps with 128 uniform values of X2 each and all 65,536 S8
members, 2^39 trials and 78,542,536,704 batches. The analysis takes the
mean, the sample standard deviation and the empirical Bernstein bound at
delta = 2^-64 of the per-outer-step shares. The decision rule was to state
the stage-B part of H1 (ii) as 0.60 p_B with budget 0.61 p_B only if that
bound is at most 0.60 p_B, and otherwise to change nothing. Every run is
reported and none was repeated with other seeds. Before the plan was
fixed, one timing run of 4 outer steps with 16 values of X2 (seed 99,
0.559 of p_B) was made. It is not part of the sample. The randomness is
SplitMix64 seeded by SEED, a deterministic generator, not ideal coins.

**Results.**

| event | count | per-outer-step mean ratio +- s.e. (sd) | empirical Bernstein bound, delta = 2^-64 | min, max of one outer step | premise |
|---|---:|---:|---:|---:|---:|
| batch enters stage B | 8,552,141,053 | 0.54644 +- 0.00023 (0.0599) of p_B | 0.5567 p_B | 0.433, 0.879 | 0.60 p_B |
| rule A and filter (trial) | 268,423,012 | 0.99995 +- 0.00007 (0.0170) of 2^-11 | 4.29 * 2^-11 (not informative) | 0.927, 1.074 | 1.25 * 2^-11 |
| rule A (trial; not in (ii)) | 17,180,077,139 | 1.00001 +- 0.00003 of 2^-5 | | | |
| batch enters stage C | 265,630,783 | 0.0033820 per batch | | | budget 0.0043405 |

Per process (8,192 outer steps) the stage-B ratio lies between 0.5455 and
0.5476. The decision rule was met (0.5567 <= 0.60), so the package uses
0.60 p_B and 0.61 p_B. The mean agrees with 098e66f4's independent sample
(0.54629 +- 0.00047). The two samples differ in X2 values per outer step
(128 here, 256 there), and the per-outer-step means estimate the same run
average either way.

**Lemma C' (lower-tail Chernoff bound).** Let X_1, .., X_n be independent
random variables with values in [0, 1] and mu = E[X_1 + .. + X_n]. Then
for 0 < delta < 1, P(X_1 + .. + X_n <= (1 - delta) mu) <= exp(-delta^2 mu / 2).
*Proof.* For t > 0 and x in [0, 1], e^(-tx) <= 1 - x (1 - e^(-t))
(convexity), so E e^(-t X_k) <= exp(-(1 - e^(-t)) E X_k), and by
independence E e^(-t sum X_k) <= exp(-(1 - e^(-t)) mu). Markov's
inequality applied to e^(-t sum X_k) with t = -ln(1 - delta) gives
P(sum <= (1 - delta) mu) <= exp(-mu (delta + (1 - delta) ln(1 - delta))),
and (1 - delta) ln(1 - delta) >= -delta + delta^2 / 2 for 0 <= delta < 1.
QED.

**Consequence.** Let m be the run average of the stage-B share and s the
observed sum of the n = 65,536 shares Z_k. If m >= m0 = 0.60 p_B, then
mu = n m > s, and Lemma C' with (1 - delta) mu = s gives
P(sum <= s) <= exp(-(n m - s)^2 / (2 n m)). This is decreasing in m for
n m > s, so it is at most exp(-(n m0 - s)^2 / (2 n m0)) = exp(-31.2) < 3 * 10^-14.
In words: if the run average were 0.60 p_B or more, a uniform sample of
this size would show a mean as low as 0.54644 p_B with probability below
3 * 10^-14. The empirical Bernstein inequality of Maurer and Pontil
(2009, Theorem 4) applies to i.i.d. variables in [0, 1]. It states that,
with probability at least 1 - delta over the sample,
E Z <= mean + sqrt(2 V ln(2/delta) / n) + 7 ln(2/delta) / (3 (n - 1)),
where V is the unbiased sample variance. It gives the sharper bound
0.5567 p_B at delta = 2^-64. Lemma C' is proved above and does not depend on
the cited inequality. For the stage-C part, 1.25 * 2^-11 is 098e66f4's
premise and is unchanged. For this rare event the bounds for variables in
[0, 1] are not informative at this sample size: the empirical Bernstein
bound is 4.29 * 2^-11, and Lemma C' gives only exp(-0.80). The
per-outer-step mean, 0.99995 +- 0.00007 of 2^-11, agrees with 098e66f4's
sample (1.00001 +- 0.00009), which is the support that 098e66f4 gave for
this part.

**Scope and limitations of this sample.** The probabilities above are over
the sampler's random choices. They are not a proof about the run, because
the sampler is a seeded deterministic generator, the program is a
participant program, and the run was made on the participant side
only. The sample holds 2^39 of the run's 2^100.5 trials. It estimates
the run average by sampling from that same population, not by a model,
so no extrapolation in the sense of H1 (i) is involved. The value 0.60
was chosen after reading 098e66f4's sample (0.546 p_B), so the two samples
are not equally independent of the choice: 098e66f4's sample motivated
it, and this package's preregistered sample tested it. The margin of the
premise over the observed means is about 1.10. That is enough for Lemma
C' and the empirical Bernstein bound at this sample size, but it is much
smaller than the margin of 098e66f4's 1.01 p_B (about 1.85).

## 9. Charged time

Per X2 value (65,536 trials), fixed work:
9363 * 29 + 3 * 147 + 107 + 4 = 272,079 operations. (Stage A of every
batch; the batch loop is unrolled 64 times: 146 iterations of 64 batches
with pointer add, compare and branch, and a straight-line tail of 19
batches, charged 3 * 147; 107 is the middle step, 4 the block test.)
Stages B and C are out of line and are duplicated for each of the 83
batch positions of the unrolled body and the tail: each copy reads the
table words of its own position (its own load offsets from the pointer)
and its last instruction jumps directly back to the next position, so an
entry costs exactly the 73 and 112 operations of Section 5. The 83 copies
take under 83 * 185 instructions, well inside the code bound of Section
10.
Stages B and C are charged at their budgets, whatever the coins:
(E_B + 1) * 73 and (E_C + 1) * 112 operations for the run, the last entry
of each covering the halting entry.

- Fixed work: 272,079 * V * 2^64 = 4.15160 * N operations.
- Stage B: (E_B + 1) * 73 = 1.26769 * N (0.61 p_B * 9,363 / 65,536 * 73).
- Stage C: (E_C + 1) * 112 = 0.06945 * N (1.27 * 2^-11 * 112).
- Per outer step (vd, w5), V * 2^32 of them: the outer step with its
  random word (340), the build entry (at most 26) and the table build
  9,363 * 49: 459,153 operations per 2^48 trials, under 2^-29 per trial.
- Per value of vd: next value, end test and loop entry, under 2^6.
- The lists U and V (18,726 packed words) and the two budget registers:
  under 2^22 operations once.
- Step 3: at most once: the 9,363 batches of one X2 value recomputed with
  all stages and their lanes scanned, under 2^22 operations, and 2
  compressions.
- Preprocessing: 2^86 units, declared below.

    T = (272,079 * V * 2^64 + 73 (E_B + 1) + 112 (E_C + 1) + 459,153 * V * 2^32
         + 2^6 V + 2^22 + 2^22) / 430 + 2 + 2^86
      = 2^94.2416   (5.488742 operations per trial: 2^94.2368 without the
                     2^86 + 2 units, which add 0.0048)

time_log2 = 94.2416, claimed **94.25** (rounded up). `python3
experiments/s8stage.py --ledger` computes T in exact rational arithmetic.
The claim holds for any total up to 5.5209 operations per trial. Under
stricter readings: the budget registers kept in memory (load, subtract,
store, load the limit, compare, branch: 3 more operations per entry) give
94.26; stage A counted without the unrolling (3 loop operations per batch)
gives 94.35. (098e66f4, with the stage-B budget 1.02 p_B, gives 2^94.4491,
claimed 94.45; its first build, with the per-trial stage-B budget
1.02 * 2^-5 and stage C at 1.02 * 2^-11, gave 2^94.4924, claimed 94.50.)
The figures of this section were recomputed for this package by an
independent re-implementation of the formula in exact rational
arithmetic, which also reproduces 098e66f4's 2^94.449145 from its
constants; the shipped `--ledger` evaluates the same formula.

**Preprocessing (declared charge).** The program stores the six constants
of Fact P, eta, the rule-A words, the filter words, the stage-test words
and the S8 conditions. The constants were found by c66f230d with solver
searches and chosen with model counts; rule A, S8 and the filter were chosen
with counts of the same kind (S8 by us from the exact per-member factors of
all 524,288 class members, best of 8,992,320 candidate sub-classes); the
order of the construction and the staged batch were found by 60f94c5c.
This work is not reconstructed from run records. A declared upper bound
of 2^86 units (2^94.75 word operations) is charged for all of it,
098e66f4's (winglock's), c66f230d's, 60f94c5c's and this package's,
including every count and measurement of Section 8 (this package's sample
of Section 8.3 has 2^39 trials, under 2^47 word operations). It is more than 2^34 times c66f230d's own estimate of their
selection (below 2^60 operations, from running times on one desktop
machine and one graphics card), and more than 2^3.5 times ten years at
2^63 operations per second (over four times the peak rate of the fastest
listed supercomputer, about 2^61.3 FP64 operations per second), so it
exceeds any computation physically performed for this selection before the
submission date. This is a declared upper-bound charge, not a premise:
H1 does not depend on it, and no part of the success bound uses it. The
charge moves the scalar by 0.0048 (94.2368 without it). The stored values themselves need no search to check: Fact P, Lemma Q,
Lemma B and the stage-test words are finite computations repeated by the
self-test and the experiments.

## 10. Memory and advice

Search memory: code below 2^19 bytes, the lists U and V 2 * 9,363 * 32
bytes, the table 5 * 9,363 * 32 bytes, constants, budget registers and
temporaries below 2^12 bytes: below 2^21 bytes. For the preprocessing we
use no reported peak: every byte it stores is written by one of its charged
word operations, so it stored at most 32 * 2^94.75 = 2^99.75 bytes;
memory_log2_bytes = 100 is this bound and covers the search (the cost model
gives memory no scalar contribution). Advice: the six constants, eta, the
rule-A, stage-test and filter words and the S8 conditions, below 64 bytes
(nonuniform_advice_log2_bytes = 6). preprocessing_log2 = 86 as charged
above.

## Appendix A. The measuring programs of Section 8.2

`rtuni.c` (compiled with `cc -O3 -march=native`; run as `./rtuni 1024 256
SEED` for SEED = 20261101 .. 20261116). It computes the trials forwards
from the context with the lines of steps O, M, Y and T, the member list of
S8 and the batches of the algorithm, and tests rule A on h1 of E3 and the
filter on c1 of E1 of message A, exactly as the shipped program's forward
computation does (checked by `rtunicheck.py`).

```c
/* rtuni.c -- real-trial rates of the H1 (ii) events of v101 on a uniform sample of the run (steps O, M, Y, T of
   60f94c5c, S8, batches of seven consecutive members, a fresh random word per outer step).
   usage: rtuni NOUTER NX2 SEED
     NOUTER outer steps, each with vd uniform below V = 1,512,538, w5 uniform, fresh coins C0.c1, D3.d1, S15, S9, and
     NX2 values of X2 drawn uniformly (all from a SplitMix64 stream seeded by SEED); all 65,536 S8 members in the
     9,363 batches of the algorithm (members 7j..7j+6, the last word repeating member 65,535).
   Per trial (distinct members): A = rule A on h1 of E3, F = filter on c1 of E1, AF = both.
   Per batch: SB = some lane passes A (enters stage B), SC = some lane passes A and F (enters stage C).
   Per outer step k: rB_k = (share of its batches with SB) / p_B, rAF_k = (share of its trials with AF) / 2^-11,
   rA_k = (share with A) / 2^-5; sums and sums of squares printed (outer steps are independent, so the standard
   error of the mean ratio is sd / sqrt(NOUTER)).                                                                  */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef uint32_t u32; typedef uint64_t u64;
static inline u32 ror(u32 x,int r){ return (x>>r)|(x<<(32-r)); }
static inline u32 rol(u32 x,int r){ return (x<<r)|(x>>(32-r)); }
static const u32 IV[8]={0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
static const u32 X3=0x29d4fa98,X7=0xbee3af28,X11=0x44036000,X15=0x40c58500,W4=0x97475638,W13=0x0007c006;
static const u32 Y3=0x8127c181,Y11=0x7af77f38;
static u64 sm; static inline u64 rnd(void){ u64 z=(sm+=0x9E3779B97F4A7C15ULL); z=(z^(z>>30))*0xBF58476D1CE4E5B9ULL; z=(z^(z>>27))*0x94D049BB133111EBULL; return z^(z>>31); }
static u32 S8[65536];
static void members(void){
  int ord[16]={14,30,31,4,5,6,7,10,11,12,13,20,21,27,28,29};
  for(u32 i=0;i<65536;i++){ u32 e1=0x030c0303|0xc; for(int t=0;t<16;t++) if(i>>t&1) e1|=1u<<ord[t]; if(e1>>21&1) e1|=1u<<26; S8[i]=e1-Y3; }
}
static inline int ruleA(u32 h){ return !(h&1) && !((h>>16)&1) && !((h>>17)&1) && ((h>>1)&1) && (((h>>2)^(h>>3))&1); }
#define G1(a,d,c,b,x,y) do{ a=a+b+x; d=ror(d^a,16); c=c+d; b=ror(b^c,12); a=a+b+y; d=ror(d^a,8); c=c+d; b=ror(b^c,7);}while(0)
int main(int argc,char**argv){
  if(argc<4){ fprintf(stderr,"usage\n"); return 1; }
  long NO=atol(argv[1]), NX=atol(argv[2]); sm=strtoull(argv[3],0,10)*0x1234567ULL+77;
  const double PB=32052445611625.0/160855115169792.0;   /* p_B of --count */
  members();
  u32 K=IV[2]+IV[6], K2A=K+W4, K2D=ror(K2A^55,16), K2C=IV[2]+K2D, K2B=ror(IV[6]^K2C,12);
  static u32 tY12[65536], tCa[65536], tX6[65536], tX1[65536], tDd[65536];
  u64 cA=0,cF=0,cAF=0,bB=0,bC=0,nb=0,nt=0; double sB=0,sB2=0,sAF=0,sAF2=0,sA=0,sA2=0,maxB=0,maxAF=0;
  double cmaxB=0; /* largest stage-B share of one context (one X2 value) */
  for(long oi=0; oi<NO; oi++){
    u32 c0c=(u32)rnd(), d3d=(u32)rnd(), s15=(u32)rnd(), s9=(u32)rnd();   /* fresh coins for this outer step */
    u32 w5=(u32)rnd(), c0d=(u32)(rnd()%1512538ULL);
    u32 S2=K2A+K2B+w5, S14=ror(K2D^S2,8), S10=K2C+S14, S6=ror(K2B^S10,7);
    u32 d3a=rol(d3d,16)^S14, d3c=s9+d3d, d3b=X3-d3a, S4=rol(d3b,12)^d3c, S3=d3a-S4, X14=ror(d3d^X3,8), X9=d3c+X14, X4=ror(d3b^X9,7);
    u32 k3d=rol(s15,8)^S3, k3c=IV[3]+k3d, k3b=ror(IV[7]^k3c,12), S11=k3c+s15, S7=ror(k3b^S11,7), k3a=rol(k3d,16)^11;
    u32 w6=k3a-IV[3]-IV[7], w7=S3-k3a-k3b, X8=c0c-c0d, Cb=ror(X4^c0c,12), D2b=rol(X7,7)^X8, D2c=rol(D2b,12)^S7, X13=X8-D2c;
    for(u32 i=0;i<65536;i++){ u32 y=S8[i], Y8=rol(y,7)^Cb, Y12=Y8-c0c, Y0=rol(Y12,8)^c0d, ca=Y0-Cb-w6, X12=rol(c0d,16)^ca;
      u32 dc=X11-X12, db=ror(S6^dc,12), X6=ror(db^X11,7), dd=dc-S11, X1=rol(X12,8)^dd;
      tY12[i]=Y12; tCa[i]=ca; tX6[i]=X6; tX1[i]=X1; tDd[i]=dd; }
    u64 obB=0,obC=0,onb=0,oA=0,oAF=0,ont=0;
    for(long xi=0; xi<NX; xi++){
      u32 X2=(u32)rnd();
      u32 d2a=X2-D2b-W13, d2d=rol(X13,8)^X2, S13=rol(d2d,16)^d2a, S8v=D2c-d2d, w12=d2a-S2-S7;
      u32 k1c=s9-S13, k1d=k1c-IV[1], k1a=rol(k1d,16), k1b=ror(IV[5]^k1c,12), S1=rol(S13,8)^k1d, S5=ror(k1b^s9,7);
      u32 w2=k1a-IV[1]-IV[5], w3=S1-k1a-k1b;
      u32 k0b=rol(S4,7)^S8v, k0c=rol(k0b,12)^IV[4], k0d=k0c-IV[0], k0a=rol(k0d,16), S12=S8v-k0c, w0=k0a-IV[0]-IV[4];
      u64 xbB=0;
      for(u32 j=0;j<9363;j++){
        int anyA=0, anyAF=0;
        for(u32 l=0;l<7;l++){
          u32 i=7*j+l; if(i>65535) break;   /* repeated lanes of the last word: the same trial */
          u32 X0=tCa[i]-X4-w2, fd=rol(X15,8)^X0, fc=S10+fd, X10=fc+X15, fb=ror(S5^fc,12), X5=ror(fb^X10,7);
          u32 ga=rol(tDd[i],16)^S12, w10=ga-S1-S6;
          u32 a2=X2,b2=tX6[i],c2=X10,d2=X14; G1(a2,d2,c2,b2,w7,w0); u32 Y6=b2,Y14=d2;
          u32 e1=Y3+S8[i], h1=ror(Y14^e1,16); int A=ruleA(h1);
          u32 a=tX1[i],b=X5,c=X9,d=X13; G1(a,d,c,b,w3,w10); u32 Y1=a;
          u32 ea1=Y1+Y6+w12, ed1=ror(tY12[i]^ea1,16), ec1=Y11+ed1; int F=((ec1&0x00098188)==0x00008000);
          cA+=A; cF+=F; cAF+=A&F; anyA|=A; anyAF|=A&F; nt++; oA+=A; oAF+=A&F; ont++;
        }
        bB+=anyA; bC+=anyAF; obB+=anyA; obC+=anyAF; xbB+=anyA; nb++; onb++;
      }
      double xs=(double)xbB/9363; if(xs>cmaxB) cmaxB=xs;
    }
    double rB=(double)obB/onb/PB, rAF=(double)oAF/ont*2048.0, rA=(double)oA/ont*32.0;
    sB+=rB; sB2+=rB*rB; sAF+=rAF; sAF2+=rAF*rAF; sA+=rA; sA2+=rA*rA; if(rB>maxB)maxB=rB; if(rAF>maxAF)maxAF=rAF;
  }
  printf("{\"outer\":%ld,\"nx2\":%ld,\"seed\":%s,\"trials\":%llu,\"batches\":%llu,\"A\":%llu,\"F\":%llu,\"AF\":%llu,\"SB\":%llu,\"SC\":%llu,"
         "\"rB\":[%.9f,%.9f,%.6f],\"rAF\":[%.9f,%.9f,%.6f],\"rA\":[%.9f,%.9f],\"context_max_B\":%.5f}\n",
         NO,NX,argv[3],(unsigned long long)nt,(unsigned long long)nb,(unsigned long long)cA,(unsigned long long)cF,(unsigned long long)cAF,
         (unsigned long long)bB,(unsigned long long)bC,sB,sB2,maxB,sAF,sAF2,maxAF,sA,sA2,cmaxB);
  return 0;
}
```

`rtunicheck.py` (run from the measuring directory with the path of the
shipped `experiments/` as its second argument):

```python
"""Cross-check of rtuni.c against the shipped program's forward computation: one outer step and one X2 value drawn
as rtuni draws them (seed given), all 65,536 S8 members in the batches of the algorithm; counts A, F, AF, SB, SC."""
import sys, json, subprocess
sys.path.insert(0, sys.argv[2])
import s8stage as s
M = (1 << 64) - 1
class SM:
    def __init__(self, seed): self.s = (seed * 0x1234567 + 77) & M
    def __call__(self):
        self.s = (self.s + 0x9E3779B97F4A7C15) & M; z = self.s
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & M; z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & M; return (z ^ (z >> 31)) & M
seed = int(sys.argv[1])
r = SM(seed); c0c, d3d, s15, s9 = [r() & 0xffffffff for _ in range(4)]
w5 = r() & 0xffffffff; vd = r() % 1512538; X2 = r() & 0xffffffff
v = s.context([c0c, vd, d3d, s15, s9, w5, X2])
A = F = AF = SB = SC = 0
for j in range(s.NBATCH):
    anyA = anyAF = False
    for i in sorted(set(s.batch_members(j))):
        f = s.forward(v, s.member(i)); a, fl = f['ruleA'], f['filt']
        A += a; F += fl; AF += a and fl; anyA |= a; anyAF |= a and fl
    SB += anyA; SC += anyAF
py = dict(A=A, F=F, AF=AF, SB=SB, SC=SC)
c = json.loads(subprocess.run(['./rtuni', '1', '1', str(seed)], capture_output=True, text=True).stdout)
print(json.dumps({'seed': seed, 'vd': vd, 'w5': w5, 'X2': X2, 'python': py, 'c': {k: c[k] for k in py}, 'equal': all(py[k] == c[k] for k in py)}))
```

The preregistered analysis (`summarize.py`):

```python
import json, glob, math
pB = 32052445611625 / 160855115169792
R = [json.load(open(f)) for f in sorted(glob.glob('runs/r_*.json'))]
n = sum(r['outer'] for r in R); t = sum(r['trials'] for r in R); b = sum(r['batches'] for r in R)
out = {'runs': len(R), 'outer_steps': n, 'trials_log2': round(math.log2(t), 4), 'batches': b}
for k in ('rB', 'rAF', 'rA'):
    s = sum(r[k][0] for r in R); s2 = sum(r[k][1] for r in R)
    m = s / n; sd = math.sqrt((s2 - n * m * m) / (n - 1)); se = sd / math.sqrt(n)
    out[k] = {'mean': round(m, 5), 'sd_outer': round(sd, 5), 'se': round(se, 6), 'upper_99.9': round(m + 3.09 * se, 5),
              'per_run': [round(r[k][0] / r['outer'], 4) for r in R]}
    if len(R[0][k]) > 2: out[k]['max_outer'] = round(max(r[k][2] for r in R), 4)
A = sum(r['A'] for r in R); AF = sum(r['AF'] for r in R); SB = sum(r['SB'] for r in R); SC = sum(r['SC'] for r in R); F = sum(r['F'] for r in R)
out['pooled'] = {'A': A, 'F': F, 'AF': AF, 'SB': SB, 'SC': SC, 'A_ratio': round(A / t * 32, 5), 'F_ratio': round(F / t * 64, 5),
                 'AF_ratio': round(AF / t * 2048, 5), 'SB_share': round(SB / b, 6), 'SB_over_pB': round(SB / b / pB, 5),
                 'SC_share': round(SC / b, 7), 'SB_budget_share_used': round(SB / b / (1.02 * pB), 4),
                 'SC_over_budget': round(SC / b / (1.27 * 65536 / 9363 / 2048), 4)}
out['context_max_B_over_pB'] = round(max(r['context_max_B'] for r in R) / pB, 4)
print(json.dumps(out, indent=1))
```

## Appendix B. This package's measuring programs (Section 8.3)

Written for this package; they share no code with 098e66f4's programs.
The listings are the hashed files of the plan, except that the local path
of the repository checkout (one string in `ref.py`, two in
`crosscheck.py`) is shown here as `<repository root>`. `sbmeas.c` was
compiled with `gcc -O3 -march=native`.

The plan (`PLAN.md`):

```text
# Preregistered plan: stage-B share of the 098e66f search on a uniform sample

Fixed before the run (hashes in PLAN.sha256):
- program sbmeas.c (gcc -O3 -march=native), cross-checked against ref.py (forward 2-round
  compression; verifier/blake3.py digests) on three complete contexts (crosscheck.py seeds 11, 12, 13).
- run: 8 processes `./sbmeas 8192 128 SEED`, SEED = 3300001 .. 3300008, outputs out_SEED.txt.
  65,536 outer steps, 128 uniform X2 values each, all 65,536 S8 members: 2^39 trials.
- analysis analyze.py: per-outer-step shares, mean, sd, empirical Bernstein upper bound (delta 2^-64).
- decision: if the bound for the stage-B batch share is <= 0.60 p_B, the package states H1 (ii)
  stage-B part as 0.60 p_B with budget 0.61 p_B; otherwise no stage-B change is made.
  The stage-C part (1.25 * 2^-11, budget 1.27) is kept and its bound reported.
- every run is reported; no rerun with other seeds.
```

`sbmeas.c`:

```c
/* sbmeas.c -- independent measurement of the stage events of the 098e66f search
   (steps O, M, Y, T; sub-class S8; batches of seven consecutive members, the last
   batch holding members 65534 and 65535) on a uniform sample of the run.
   usage: sbmeas NOUTER NX2 SEED            -> one line per outer step + totals
          sbmeas --context c0..c6           -> per-member flags for one context (cross-check)
   Per outer step: vd uniform below V = 1512538, w5, C0.c1, D3.d1, S15, S9 uniform 32-bit
   words, then NX2 uniform values of X2; all from SplitMix64(SEED).
   Rule A is tested on h1 = ROR(Y14 ^ (Y3 + y), 16) of E3, read from a forward
   evaluation of C2; the filter on c1 of E1, read from forward C1 and E1.       */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef uint32_t u32; typedef uint64_t u64;
static inline u32 ror(u32 x, int r) { return (x >> r) | (x << (32 - r)); }
static inline u32 rol(u32 x, int r) { return (x << r) | (x >> (32 - r)); }
static const u32 IV[8] = {0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19};
#define X3 0x29d4fa98u
#define X7 0xbee3af28u
#define X11 0x44036000u
#define X15 0x40c58500u
#define W4 0x97475638u
#define W13 0x0007c006u
#define Y3 0x8127c181u
#define Y11 0x7af77f38u
#define VRANGE 1512538u
#define NMEM 65536
#define NB 9363
static u64 sm;
static u64 next64(void) { u64 z = (sm += 0x9E3779B97F4A7C15ull); z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ull; z = (z ^ (z >> 27)) * 0x94D049BB133111EBull; return z ^ (z >> 31); }
static u32 next32(void) { return (u32)(next64() >> 32); }
static u32 mem_y[NMEM];
static void members(void) {
  static const int ord[16] = {14, 30, 31, 4, 5, 6, 7, 10, 11, 12, 13, 20, 21, 27, 28, 29};
  for (int i = 0; i < NMEM; i++) { u32 e1 = 0x030c0303u | 0xcu;
    for (int t = 0; t < 16; t++) if ((i >> t) & 1) e1 |= 1u << ord[t];
    if ((e1 >> 21) & 1) e1 |= 1u << 26; mem_y[i] = e1 - Y3; }
}
typedef struct { u32 S2, S4, S6, S7, S9, S10, S11, S15, X4, X9, X13, X14, D2b1, D2c1, vb, vc, vd, w5, w6, w7; } Outer;
typedef struct { u32 w0, w2, w3, w12, S0, S1, S5, S12; } Mid;
static void outer(Outer *o, u32 vc, u32 vd, u32 D3d1, u32 S15, u32 S9, u32 w5) {
  u32 K = IV[2] + IV[6];
  u32 ka2 = K + W4, kd2 = ror(ka2 ^ 55, 16), kc2 = IV[2] + kd2, kb2 = ror(IV[6] ^ kc2, 12);
  u32 S2 = ka2 + kb2 + w5, S14 = ror(kd2 ^ S2, 8), S10 = kc2 + S14, S6 = ror(kb2 ^ S10, 7);
  u32 D3a1 = rol(D3d1, 16) ^ S14, D3c1 = S9 + D3d1, D3b1 = X3 - D3a1, S4 = rol(D3b1, 12) ^ D3c1;
  u32 S3 = D3a1 - S4, X14 = ror(D3d1 ^ X3, 8), X9 = D3c1 + X14, X4 = ror(D3b1 ^ X9, 7);
  u32 K3d1 = rol(S15, 8) ^ S3, K3c1 = IV[3] + K3d1, K3b1 = ror(IV[7] ^ K3c1, 12), S11 = K3c1 + S15;
  u32 S7 = ror(K3b1 ^ S11, 7), K3a1 = rol(K3d1, 16) ^ 11, w6 = K3a1 - IV[3] - IV[7], w7 = S3 - K3a1 - K3b1;
  u32 X8 = vc - vd, vb = ror(X4 ^ vc, 12), D2b1 = rol(X7, 7) ^ X8, D2c1 = rol(D2b1, 12) ^ S7, X13 = X8 - D2c1;
  Outer t = {S2, S4, S6, S7, S9, S10, S11, S15, X4, X9, X13, X14, D2b1, D2c1, vb, vc, vd, w5, w6, w7}; *o = t;
}
static void middle(const Outer *o, u32 X2, Mid *m) {
  u32 D2a1 = X2 - o->D2b1 - W13, D2d1 = rol(o->X13, 8) ^ X2, S13 = rol(D2d1, 16) ^ D2a1;
  u32 S8 = o->D2c1 - D2d1, w12 = D2a1 - o->S2 - o->S7;
  u32 K1c1 = o->S9 - S13, K1d1 = K1c1 - IV[1], K1a1 = rol(K1d1, 16), K1b1 = ror(IV[5] ^ K1c1, 12);
  u32 S1 = rol(S13, 8) ^ K1d1, S5 = ror(K1b1 ^ o->S9, 7), w2 = K1a1 - IV[1] - IV[5], w3 = S1 - K1a1 - K1b1;
  u32 K0b1 = rol(o->S4, 7) ^ S8, K0c1 = rol(K0b1, 12) ^ IV[4], K0d1 = K0c1 - IV[0], K0a1 = rol(K0d1, 16);
  u32 S12 = S8 - K0c1, S0 = rol(S12, 8) ^ K0d1, w0 = K0a1 - IV[0] - IV[4];
  Mid t = {w0, w2, w3, w12, S0, S1, S5, S12}; *m = t;
}
/* per-member table (step Y) */
static u32 T_va[NMEM], T_X6[NMEM], T_X1[NMEM], T_gd[NMEM], T_Y12[NMEM], T_gb[NMEM];
static void build(const Outer *o) {
  for (int i = 0; i < NMEM; i++) { u32 y = mem_y[i];
    u32 Y8 = rol(y, 7) ^ o->vb, Y12 = Y8 - o->vc, Y0 = rol(Y12, 8) ^ o->vd, va = Y0 - o->vb - o->w6, X12 = rol(o->vd, 16) ^ va;
    u32 gc = X11 - X12, gb = ror(o->S6 ^ gc, 12), X6 = ror(gb ^ X11, 7), gd = gc - o->S11, X1 = rol(X12, 8) ^ gd;
    T_va[i] = va; T_X6[i] = X6; T_X1[i] = X1; T_gd[i] = gd; T_Y12[i] = Y12; T_gb[i] = gb; }
}
static inline int ruleA(u32 h1) { return (h1 & 1) == 0 && ((h1 >> 16) & 3) == 0 && ((h1 >> 1) & 1) == 1 && (((h1 >> 2) ^ (h1 >> 3)) & 1); }
static inline int filt(u32 c1) { return (c1 & 0x00098188u) == 0x00008000u; }
/* evaluate member i in context (o, X2, m): bit0 = rule A, bit1 = filter (only computed when rule A holds) */
static inline int trial(const Outer *o, u32 X2, const Mid *m, int i) {
  u32 y = mem_y[i];
  u32 X0 = T_va[i] - o->X4 - m->w2;
  u32 fd = rol(X15, 8) ^ X0, fc = o->S10 + fd, X10 = fc + X15;
  /* C2 = G(X2, X6, X10, X14; w7, w0) forward */
  u32 X6 = T_X6[i];
  u32 a1 = X2 + X6 + o->w7, d1 = ror(o->X14 ^ a1, 16), c1 = X10 + d1, b1 = ror(X6 ^ c1, 12);
  u32 a2 = a1 + b1 + m->w0, Y14 = ror(d1 ^ a2, 8), Y10 = c1 + Y14, Y6 = ror(b1 ^ Y10, 7);
  u32 h1 = ror(Y14 ^ (Y3 + y), 16);
  if (!ruleA(h1)) return 0;
  u32 fb = ror(m->S5 ^ fc, 12), X5 = ror(fb ^ X10, 7);
  u32 ga = rol(T_gd[i], 16) ^ m->S12, w10 = ga - m->S1 - o->S6;
  /* C1 = G(X1, X5, X9, X13; w3, w10) forward to a2 = Y1 */
  u32 p1 = T_X1[i] + X5 + m->w3, q1 = ror(o->X13 ^ p1, 16), r1 = o->X9 + q1, s1 = ror(X5 ^ r1, 12), Y1 = p1 + s1 + w10;
  /* E1 = G(Y1, Y6, Y11, Y12; w12, w5) forward to c1 */
  u32 e_a1 = Y1 + Y6 + m->w12, e_d1 = ror(T_Y12[i] ^ e_a1, 16), e_c1 = Y11 + e_d1;
  return 1 | (filt(e_c1) << 1);
}
int main(int argc, char **argv) {
  members();
  if (argc == 9 && !strcmp(argv[1], "--context")) {
    u32 c[7]; for (int k = 0; k < 7; k++) c[k] = (u32)strtoul(argv[2 + k], 0, 0);
    Outer o; Mid m; outer(&o, c[0], c[1], c[2], c[3], c[4], c[5]); middle(&o, c[6], &m); build(&o);
    u64 h = 1469598103934665603ull; long nA = 0, nAF = 0, nB = 0, nC = 0;
    for (int j = 0; j < NB; j++) { int lo = 7 * j, hi = lo + 7 > NMEM ? NMEM : lo + 7, eb = 0, ec = 0;
      for (int i = lo; i < hi; i++) { int f = trial(&o, c[6], &m, i); h = (h ^ (u64)f) * 1099511628211ull;
        nA += f & 1; nAF += f == 3; eb |= f & 1; ec |= f == 3; }
      nB += eb; nC += ec; }
    printf("ruleA %ld ruleA_filter %ld stageB_batches %ld stageC_batches %ld flaghash %016llx\n", nA, nAF, nB, nC, (unsigned long long)h);
    return 0;
  }
  if (argc != 4) { fprintf(stderr, "usage\n"); return 2; }
  long nout = atol(argv[1]), nx2 = atol(argv[2]); sm = strtoull(argv[3], 0, 10);
  double sB = 0, sB2 = 0, sAF = 0, sAF2 = 0, sA = 0, sA2 = 0; u64 tB = 0, tC = 0, tA = 0, tAF = 0;
  for (long k = 0; k < nout; k++) {
    u32 vd; do vd = next32() & 0x1fffff; while (vd >= VRANGE);
    u32 w5 = next32(), vc = next32(), D3d1 = next32(), S15 = next32(), S9 = next32();
    Outer o; outer(&o, vc, vd, D3d1, S15, S9, w5); build(&o);
    u64 kB = 0, kC = 0, kA = 0, kAF = 0;
    for (long x = 0; x < nx2; x++) { u32 X2 = next32(); Mid m; middle(&o, X2, &m);
      for (int j = 0; j < NB; j++) { int lo = 7 * j, hi = lo + 7 > NMEM ? NMEM : lo + 7, eb = 0, ec = 0;
        for (int i = lo; i < hi; i++) { int f = trial(&o, X2, &m, i); kA += f & 1; kAF += f == 3; eb |= f & 1; ec |= f == 3; }
        kB += eb; kC += ec; } }
    double rb = (double)kB / ((double)nx2 * NB), raf = (double)kAF / ((double)nx2 * NMEM), ra = (double)kA / ((double)nx2 * NMEM);
    printf("%ld %.10f %.10f %.10f %llu %llu\n", k, rb, raf, ra, (unsigned long long)kB, (unsigned long long)kC);
    sB += rb; sB2 += rb * rb; sAF += raf; sAF2 += raf * raf; sA += ra; sA2 += ra * ra; tB += kB; tC += kC; tA += kA; tAF += kAF;
  }
  printf("TOTAL nout %ld nx2 %ld batches %llu stageB %llu stageC %llu trials %llu ruleA %llu ruleA_filter %llu sumB %.12f sumB2 %.12f sumAF %.12f sumAF2 %.12f sumA %.12f sumA2 %.12f\n",
         nout, nx2, (unsigned long long)(nout * nx2 * (u64)NB), (unsigned long long)tB, (unsigned long long)tC, (unsigned long long)(nout * nx2 * (u64)NMEM),
         (unsigned long long)tA, (unsigned long long)tAF, sB, sB2, sAF, sAF2, sA, sA2);
  return 0;
}
```

`ref.py` (independent reference; run as `python3 ref.py 1 3000`: 3,000 of 3,000 cases right):

```python
"""Independent reference for the stage-B / stage-C events of the 098e66f search.
Builds messages from the eight free words by steps O, M, Y, T (written from the
proof text), runs a forward 2-round compression of message A, and reads h1 of E3
and c1 of E1 from that forward computation. Cross-checked against
verifier/blake3.py (organizer code)."""
import struct, sys, os
M = 0xffffffff
IV = (0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19)
P = (2, 6, 3, 10, 7, 0, 4, 13, 1, 11, 12, 5, 9, 14, 15, 8)
def ror(x, r): return ((x >> r) | (x << (32 - r))) & M
def rol(x, r): return ror(x, 32 - r)
X3, X7, X11, X15 = 0x29d4fa98, 0xbee3af28, 0x44036000, 0x40c58500
W4, W13 = 0x97475638, 0x0007c006
K = (IV[2] + IV[6]) & M
Y3, Y11 = 0x8127c181, 0x7af77f38
ORDER = [14, 30, 31, 4, 5, 6, 7, 10, 11, 12, 13, 20, 21, 27, 28, 29]
def member(i):
    e1 = 0x030c0303 | 0xc
    for t, b in enumerate(ORDER):
        if (i >> t) & 1: e1 |= 1 << b
    if (e1 >> 21) & 1: e1 |= 1 << 26
    return (e1 - Y3) & M

def outer(vc, vd, D3d1, S15, S9, w5):
    o = {}
    ka2 = (K + W4) & M; kd2 = ror(ka2 ^ 55, 16); kc2 = (IV[2] + kd2) & M; kb2 = ror(IV[6] ^ kc2, 12)
    S2 = (ka2 + kb2 + w5) & M; S14 = ror(kd2 ^ S2, 8); S10 = (kc2 + S14) & M; S6 = ror(kb2 ^ S10, 7)
    D3a1 = rol(D3d1, 16) ^ S14; D3c1 = (S9 + D3d1) & M; D3b1 = (X3 - D3a1) & M; S4 = rol(D3b1, 12) ^ D3c1
    S3 = (D3a1 - S4) & M; X14 = ror(D3d1 ^ X3, 8); X9 = (D3c1 + X14) & M; X4 = ror(D3b1 ^ X9, 7)
    K3d1 = rol(S15, 8) ^ S3; K3c1 = (IV[3] + K3d1) & M; K3b1 = ror(IV[7] ^ K3c1, 12); S11 = (K3c1 + S15) & M
    S7 = ror(K3b1 ^ S11, 7); K3a1 = rol(K3d1, 16) ^ 11; w6 = (K3a1 - IV[3] - IV[7]) & M; w7 = (S3 - K3a1 - K3b1) & M
    X8 = (vc - vd) & M; vb = ror(X4 ^ vc, 12); D2b1 = rol(X7, 7) ^ X8; D2c1 = rol(D2b1, 12) ^ S7; X13 = (X8 - D2c1) & M
    o.update(locals()); del o['o']
    return o

def middle(o, X2):
    D2a1 = (X2 - o['D2b1'] - W13) & M; D2d1 = rol(o['X13'], 8) ^ X2; S13 = rol(D2d1, 16) ^ D2a1
    S8 = (o['D2c1'] - D2d1) & M; w12 = (D2a1 - o['S2'] - o['S7']) & M
    K1c1 = (o['S9'] - S13) & M; K1d1 = (K1c1 - IV[1]) & M; K1a1 = rol(K1d1, 16); K1b1 = ror(IV[5] ^ K1c1, 12)
    S1 = rol(S13, 8) ^ K1d1; S5 = ror(K1b1 ^ o['S9'], 7); w2 = (K1a1 - IV[1] - IV[5]) & M; w3 = (S1 - K1a1 - K1b1) & M
    K0b1 = rol(o['S4'], 7) ^ S8; K0c1 = rol(K0b1, 12) ^ IV[4]; K0d1 = (K0c1 - IV[0]) & M; K0a1 = rol(K0d1, 16)
    S12 = (S8 - K0c1) & M; S0 = rol(S12, 8) ^ K0d1; w0 = (K0a1 - IV[0] - IV[4]) & M; w1 = (S0 - K0a1 - K0b1) & M
    r = dict(locals()); del r['o']; return r

def words(o, m, y):
    vb, vc, vd = o['vb'], o['vc'], o['vd']
    Y8 = rol(y, 7) ^ vb; Y12 = (Y8 - vc) & M; Y0 = rol(Y12, 8) ^ vd; va = (Y0 - vb - o['w6']) & M; X12 = rol(vd, 16) ^ va
    gc = (X11 - X12) & M; gb = ror(o['S6'] ^ gc, 12); X6 = ror(gb ^ X11, 7); gd = (gc - o['S11']) & M; X1 = rol(X12, 8) ^ gd
    X0 = (va - o['X4'] - m['w2']) & M
    fd = rol(X15, 8) ^ X0; fc = (o['S10'] + fd) & M; X10 = (fc + X15) & M; fb = ror(m['S5'] ^ fc, 12)
    fa = rol(fd, 16) ^ o['S15']; w8 = (fa - m['S0'] - m['S5']) & M; w9 = (X0 - fa - fb) & M
    ga = rol(gd, 16) ^ m['S12']; w10 = (ga - m['S1'] - o['S6']) & M; w11 = (X1 - ga - gb) & M
    return [m['w0'], m['w1'], m['w2'], m['w3'], W4, o['w5'], o['w6'], o['w7'], w8, w9, w10, w11, m['w12'], W13, 0, 0]

def messages(w):
    A = struct.pack('<16I', *w)[:55]
    wb = list(w); wb[4] = (((K + W4) ^ 8) - K) & M; wb[5] = (w[5] + W4 - wb[4]) & M
    B = struct.pack('<16I', *wb)[:63]
    return A, B

def G(v, a, b, c, d, x, y, rec=None):
    v[a] = (v[a] + v[b] + x) & M; v[d] = ror(v[d] ^ v[a], 16); v[c] = (v[c] + v[d]) & M
    if rec is not None: rec.append((v[a], v[d], v[c]))
    v[b] = ror(v[b] ^ v[c], 12); v[a] = (v[a] + v[b] + y) & M; v[d] = ror(v[d] ^ v[a], 8)
    v[c] = (v[c] + v[d]) & M; v[b] = ror(v[b] ^ v[c], 7)

def forward(msg):
    """2-round root compression of a <=64-byte message; returns digest, X (after round 0), Y4, h1 of E3, c1 of E1."""
    w = list(struct.unpack('<16I', msg.ljust(64, b'\0')))
    v = list(IV) + list(IV[:4]) + [0, 0, len(msg), 11]
    rec = []
    sched = [(0, 4, 8, 12), (1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15), (0, 5, 10, 15), (1, 6, 11, 12), (2, 7, 8, 13), (3, 4, 9, 14)]
    X = None
    for rnd in range(2):
        for k, (a, b, c, d) in enumerate(sched):
            G(v, a, b, c, d, w[2 * k], w[2 * k + 1], rec)
            if rnd == 1 and k == 3: Yst = list(v)
        if rnd == 0: X = list(v)
        w = [w[i] for i in P]
    E1 = rec[8 + 5]; E3 = rec[8 + 7]
    dig = struct.pack('<8I', *[v[i] ^ v[i + 8] for i in range(8)])
    return dig, X, Yst, E3[1], E1[2]

def ruleA(h1): return (h1 & 1) == 0 and (h1 >> 16) & 1 == 0 and (h1 >> 17) & 1 == 0 and (h1 >> 1) & 1 == 1 and ((h1 >> 2) & 1) != ((h1 >> 3) & 1)
def filt(c1): return (c1 & 0x00098188) == 0x00008000

if __name__ == '__main__':
    sys.path.insert(0, '<repository root>')
    from verifier.blake3 import blake3
    import random
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    bad = 0; nA = 0; nAF = 0
    for t in range(n):
        cw = [rng.getrandbits(32) for _ in range(7)]
        o = outer(cw[0], cw[1], cw[2], cw[3], cw[4], cw[5]); m = middle(o, cw[6]); y = member(rng.randrange(1 << 16))
        w = words(o, m, y); A, B = messages(w)
        dA, XA, YA, h1, c1 = forward(A); dB, XB, YB, _, _ = forward(B)
        ok = dA == blake3(A, 2) and dB == blake3(B, 2) and XA == XB
        ok = ok and (XA[3], XA[7], XA[11], XA[15]) == (X3, X7, X11, X15) and XA[2] == cw[6]
        ok = ok and YA[4] == y and YB[4] == y and YA[3] == Y3 and YA[11] == Y11
        ok = ok and all(dA[4 * i:4 * i + 4] == dB[4 * i:4 * i + 4] for i in (0, 2, 5, 7))
        ok = ok and h1 == ror(YA[14] ^ ((Y3 + y) & M), 16)
        bad += not ok; nA += ruleA(h1); nAF += ruleA(h1) and filt(c1)
    print({'cases': n, 'bad': bad, 'ruleA': nA, 'ruleA_filter': nAF})
```

`crosscheck.py` (run for seeds 11, 12 and 13; all equal):

```python
"""Cross-check sbmeas --context against ref.py: every member of S8 in one context, rule A
and the filter read from a forward 2-round compression of message A (ref.forward), digests
of A also compared with verifier/blake3.py on every 64th member."""
import sys, subprocess
sys.path.insert(0, '<repository root>')
from verifier.blake3 import blake3
import ref, random
seed = int(sys.argv[1]); rng = random.Random(seed)
cw = [rng.getrandbits(32) for _ in range(7)]; cw[1] %= 1512538
o = ref.outer(*cw[:6]); m = ref.middle(o, cw[6])
h = 1469598103934665603; nA = nAF = nB = nC = 0; ver = 0
for j in range(9363):
    eb = ec = 0
    for i in range(7 * j, min(7 * j + 7, 65536)):
        w = ref.words(o, m, ref.member(i)); A, B = ref.messages(w)
        d, X, Y, h1, c1 = ref.forward(A)
        if i % 64 == 0: assert d == blake3(A, 2); ver += 1
        a = ref.ruleA(h1); f = 1 if a else 0
        if a and ref.filt(c1): f = 3
        h = ((h ^ f) * 1099511628211) % (1 << 64)
        nA += f & 1; nAF += f == 3; eb |= f & 1; ec |= f == 3
    nB += eb; nC += ec
py = 'ruleA %d ruleA_filter %d stageB_batches %d stageC_batches %d flaghash %016x' % (nA, nAF, nB, nC, h)
c = subprocess.run(['./sbmeas', '--context'] + [str(x) for x in cw], capture_output=True, text=True).stdout.strip()
print('seed', seed, 'context', ['%08x' % x for x in cw]); print('py', py); print('c ', c); print('verifier digests checked', ver, 'EQUAL' if py == c else 'MISMATCH')
```

`analyze.py` (the preregistered analysis):

```python
"""Analysis fixed before the preregistered run. Reads out_*.txt (one line per outer step:
k, share of batches entering stage B, share of trials with rule A and filter, share with rule A,
batches B, batches C). Outer steps are i.i.d. uniform over the run's outer steps (fresh coins, vd < V,
w5) with NX2 uniform X2 values each, so each per-outer-step share Z_k in [0, 1] is an unbiased estimate
of the run average. Empirical Bernstein bound (Maurer and Pontil 2009, Theorem 4): with probability at
least 1 - delta over the sample, E Z <= mean + sqrt(2 V ln(2/delta) / n) + 7 ln(2/delta) / (3 (n - 1)),
V the unbiased sample variance. delta = 2^-64."""
import glob, math, json
from fractions import Fraction
pB = Fraction(32052445611625, 160855115169792)
rows = []
for f in sorted(glob.glob('out_*.txt')):
    for line in open(f):
        if line.startswith('TOTAL'): continue
        p = line.split(); rows.append((float(p[1]), float(p[2]), float(p[3]), int(p[4]), int(p[5])))
n = len(rows); L = math.log(2 / 2.0 ** -64)
def stats(vals, unit):
    mu = sum(vals) / n; var = sum((v - mu) ** 2 for v in vals) / (n - 1)
    ub = mu + math.sqrt(2 * var * L / n) + 7 * L / (3 * (n - 1))
    return {'mean_over_unit': mu / unit, 'se_over_unit': math.sqrt(var / n) / unit, 'sd_over_unit': math.sqrt(var) / unit,
            'emp_bernstein_ub_over_unit_delta_2^-64': ub / unit, 'max_over_unit': max(vals) / unit, 'min_over_unit': min(vals) / unit}
res = {'outer_steps': n, 'stage_B_share_vs_pB': stats([r[0] for r in rows], float(pB)),
       'ruleA_filter_vs_2^-11': stats([r[1] for r in rows], 2.0 ** -11),
       'ruleA_vs_2^-5': stats([r[2] for r in rows], 2.0 ** -5),
       'batches_B': sum(r[3] for r in rows), 'batches_C': sum(r[4] for r in rows)}
res['accept_stageB_premise_0.60'] = res['stage_B_share_vs_pB']['emp_bernstein_ub_over_unit_delta_2^-64'] <= 0.60
res['stageC_inherited_premise_1.25_covered'] = res['ruleA_filter_vs_2^-11']['emp_bernstein_ub_over_unit_delta_2^-64'] <= 1.25
print(json.dumps(res, indent=1))
```
