# A staged S8 search on the 55/63-byte half-collision of 2-round BLAKE3 in
the swapped order S2K, with X14 = 0, the sampled premises of 52bb50ee and
the near-premise budgets of 5266c5ce

The scalar below is `time_log2` under `collision-frontier-v5` (C = 430).

**Credits.** This package is built on submissions of Jbenisek, Subflatus3
and leech1996, which are public and AI-screened; 52bb50ee is promoted;
5266c5ce and 1d5e54ce are in review. From
Jbenisek's c66f230d (co-author tekkac): the 55/63-byte length cancellation,
the six pinned constants, Lemmas L and H, the class of Y4 (eta = 830303cf),
rule A and Lemma N. From Jbenisek's 60f94c5c: the three-level construction
(steps O, M, Y and T of Section 2: an outer step of six words, the middle
word X2, the member y), a table built once per outer step and reused by
the inner loops, and the **staged batch**: a cheap rule-A test for every
batch, the rest of the batch only for batches in which some lane passes,
and a budget on the number of such batches that halts the run. From
Subflatus3's 52bb50ee (94.25): the stage-B part of H1 (ii) stated as a run
average supported by a preregistered uniform sample, with the lower-tail
Chernoff bound (Lemma C') and the empirical Bernstein bound as the decision
rule, and their independent 2^39-trial sample of the 098e66f4
configuration (Section 8.2). From Subflatus3's 1d5e54ce (94.167, built on
our 21252124): sampling single uniform batches of the run instead of whole
outer steps (Lemma U there), which we use for both stage events of the new
order. From leech1996's 5266c5ce (94.24): budgets
just above the premises (delta = 1/6000 in Theorem 2). Building
member-dependent values once per outer step was first published by
Th0rgal in df8bd46d. The seven 36-bit lanes and the masked rotation are
from ticket 2bf40fb (tekkac); the complement propagation follows 8c81a219
(Th0rgal). Jbenisek, tekkac, Th0rgal, Subflatus3 and leech1996 are
co-authors of this submission. Ours (18a7fc52, d26a3c5f, 2bb5d604,
098e66f4, 21252124): the sub-class S8, the beta filter and Lemma B, Lemmas
D and D', the exact S8 count, the block accumulator, the branch-free
64-register residual computation (stage C), the beta filter as the stage-B
test, a fresh random word per outer step, the exact model values of the two
stage events, the Chernoff bound on the budgets (Theorem 2) and D3.d1 = X3
(X14 = 0). New in this version: the loop order S2K (a table over X2
instead of over members, batches of seven X2 values of one member whose
C2.a1 share the low half, Lemma A3), pass-flag stage tests (Lemmas A3, F2),
Y9 and Y13 moved from stage B to stage C, one-operation budget counts with
a halt test per group, and a preregistered per-batch uniform sample of this
order. We do not use the sub-class, the eight-condition rule, the E1 test
stage or the budget premises of 60f94c5c.

**Change from our previous version (21252124, 94.1982).** The trials, the
event good, S8, N, the count, F and lambda are unchanged; the order in
which the trials are batched and the counted pieces change, and the two
stage events were measured again on the new batching.

- **Order S2K (new).** In 21252124 a batch held seven consecutive members
  of one context (outer step and X2). Here a batch holds one member and
  seven values of X2: for a member with c = X6 + w7 and a group g < 9,363,
  lane l at position i < 2^16 is the trial with C2.a1 = (7g + l) 2^16 + i,
  so C2.d1 = ROR(C2.a1, 16) = i 2^16 + 7g + l needs one addition per batch
  and no rotation, and the six bits of C2.d1 that rule A reads are constant
  for 256 consecutive positions, which folds the rule-A comparison into one
  constant K' (Lemma A3). The step-M words of every X2 come from a table
  built once per outer step (2^32 + 2^16 packed words, 94 operations each).
  Stage A falls from 28 to 19 operations per batch, stage B from 73 to 66;
  stage C rises from 112 to 119 (it now computes Y1, Y13, Y9 itself).
- **Premises of H1 (ii) measured on the new order.** The stage-B share
  depends on which trials share a batch, so 21252124's sample (0.53912 p_B
  in its order) does not apply. A preregistered uniform sample of 2^38
  trials of the new order (one uniform batch per unit, Section 8.2) gives
  0.57650 p_B, and the preregistered decision rule (52bb50ee's two tests on
  a grid) sets the premise 0.5766 p_B; the same sample gives rule A with the
  filter at 0.99987 * 2^-11 and the premise 1.002 * 2^-11 (21252124: 1.25).
  Budgets are 6001/6000 times the premises (5266c5ce's delta).
- **Review findings on 21252124 carried over**: the corrected H1 (i)
  sentence on X14 = 0 (Section 8.1), the run lists and replay counts, and the
  deeper E1/E3 events now measured with D3.d1 = X3 against random D3.d1 on
  2^38 and 2^36 trials (Section 8.1).

The charge per trial falls from 5.3253 (21252124), 5.4887 (52bb50ee) and
5.4682 (5266c5ce) to 3.8600, and the claim from 94.1982, 94.25 and 94.24 to
**93.7358**.

**Exact part.** For every choice of eight 32-bit words the construction gives
a 55-byte message A and a 63-byte message B whose complete 2-round digests
agree on digest words 0, 2, 5 and 7 (Theorem 1). One of the eight words is
the round-1 state word Y4; the search keeps Y4 in S8. The batches of the
order S2K cover every trial exactly once (Section 4). The stage tests are
exact: stage A passes a lane iff its trial satisfies rule A (Lemma A3),
stage B iff it satisfies rule A and the filter (Lemma F2), and stage C
computes the residual exactly (Lemmas D, D'). Given H1 (ii), a budget halts
the run with probability below exp(-6.9 * 10^6) (stage B) and exp(-2.0 * 10^5)
(stage C) (Theorem 2, a Chernoff bound over independent outer steps; no
independence inside an outer step, a member, a group or a batch is used).

**Heuristic part.** The search runs N = V * 2^80 pairs (V = 1,512,538,
N = 2^100.53). H1 (i) assumes a trial is *good* (R = 0, rule A, beta
filter) with probability at least F * 2^-128, F = 92,675,072 = 2^26.4657,
half of the exact model count 185,350,144 (Section 8; `python3
experiments/s8stage.py --count` recomputes this integer). H1 (ii) states
two run averages: the share of batches (of the order S2K) entering stage B
is at most 0.5766 p_B (p_B = 0.1992628, its exact value under the model M),
and the rate of rule A with the filter is at most 1.002 * 2^-11; both values
were set by a preregistered decision rule from a uniform sample fixed by
its preregistration. Total charged time 2^93.735734, claimed 93.7358 (rounded
up). With the uniform rate instead, the same search needs 2^127 trials and
gives about 120.2. No full collision is exhibited.

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

**The construction (60f94c5c, Section 4 there).** Eight free words: the
six words of an *outer step* (vc, vd, D3.d1, S15, S9, w5), where vc = C0.c1
and vd = C0.d1 are the third and second values of the round-1 call C0 and
D3.d1 is the second value of D3; the *middle word* X2; and the *member*
y = Y4. For a call, a1, d1, c1, b1 are its first four values (Fact 1). Every
line is one assignment of the named call solved for its left side;
w4 = W4, w13 = W13, w14 = w15 = 0. All statements of this section hold for
every value of the eight words. The algorithm of Section 4 fixes
D3.d1 = X3, so that X14 = ROR(D3.d1 ^ X3, 8) = 0 and X9 = D3.c1 + X14 = D3.c1
in every outer step (as in 21252124).

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

**Sub-class S8 (ours, 2bb5d604).** S8 is the set of class members whose e1 = Y3 + Y4
also has bits 2 and 3 equal to 1 and bit 21 equal to bit 26: 2^16 = 65,536
members (three linear conditions on free bits of e1). Member number i,
0 <= i < 2^16, has e1 = 030c0303 | 0000000c with the bits of i placed at the
free positions in the order 14, 30, 31, 4, 5, 6, 7, 10, 11, 12, 13, 20,
21, 27, 28, 29, then bit 26 set equal to bit 21; Y4 = e1 - Y3. (The order
is that of 2bb5d604, fixed before any stage measurement and not changed
since. In the order S2K of Section 4 a batch holds one member, so the member
order no longer decides which trials share a batch.)

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

**Beta filter (ours, 2bb5d604).** E1's a1 and d1 are shared by A and B, c1 = Y11 + d1
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

**Lemma D (residual words, ours).** For a trial write (a1, d1, c1, b1, a2,
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

**Lemma D' (test words, ours).** With P = a2 ^ a2', the word
W4 = (f1 ^ f1') ^ P ^ ROR(P, 1) equals ROL(D4, 7) ^ D1, so R = 0 iff
D1 = D3 = W4 = D6 = 0. *Proof.* d1 is shared, so d2 ^ d2' =
ROR(d1 ^ a2, 8) ^ ROR(d1 ^ a2', 8) = ROR(P, 8) and ROL(D4, 7) =
f1 ^ f1' ^ g2 ^ g2' ^ ROR(P, 1); XOR with D1 = P ^ g2 ^ g2' gives W4. The map
(D1, D4) -> (D1, ROL(D4, 7) ^ D1) is invertible. QED. Also
e2' = e1' + f1' + w8 = (e1 + w8) + f1' + DY3 with DY3 = Y3' - Y3, and
w8 = fa - S0 - S5 with fa = ROL(fd, 16) ^ S15 (D0, step T).


**Lemma A3 (stage-A test with a folded constant, new).** For 32-bit words
a2, d1 put z = a2 ^ d1, j = (d1 >> 24) AND 15 and

    K' = (d1 AND 00000300) + F(j),   F(j) = 2^26 + (1 - j_0) 2^24 + j_1 2^25 + (j_2 XOR j_3) 2^27

(j_k the bits of j, that is bits 24 + k of d1). Then z satisfies the five
conditions of Lemma A (z8 = 1, z9 = 1, z24 = 0, z25 = 1, z26 != z27) iff
bits 8, 9, 24, 25 and 27 of s = (a2 + K') mod 2^32 are all 1. *Proof.* K'
has no bits below 8, so no carry enters bit 8, and s_8 = a2_8 XOR d1_8 =
z8. If z8 = 1 no carry leaves bit 8 (a2_8 and K'_8 = d1_8 differ), so
s_9 = z9, and if z9 = 1 no carry leaves bit 9; K' is 0 on bits 10..23, so
no carry reaches bit 24. Then s_24 = a2_24 XOR (1 - d1_24) = 1 - z24, and a
carry leaves bit 24 only if a2_24 = 1 and d1_24 = 0, i.e. z24 = 1; if
z24 = 0, s_25 = a2_25 XOR d1_25 = z25, and a carry leaves bit 25 only if
a2_25 = d1_25 = 1, i.e. z25 = 0. If z25 = 1, bit 26 receives no carry and
K'_26 = 1, so s_26 = 1 - a2_26 and the carry into bit 27 is a2_26; with
K'_27 = d1_26 XOR d1_27, s_27 = a2_27 XOR d1_26 XOR d1_27 XOR a2_26 =
z26 XOR z27. So if all five conditions hold, the five bits of s are 1; and
if the five bits of s are 1, the argument read in order (s_8 = z8 = 1,
s_9 = z9 = 1, s_24 = 1 - z24 = 1, s_25 = z25 = 1, s_27 = z26 XOR z27 = 1)
gives the five conditions. QED. Lemma A3 was also checked exhaustively
(all 64 patterns of the six bits of d1 and all 2^20 values of bits 8..27 of
a2, each with four fillings of the other bits: `lemmaA3_check.c`, no
disagreement in 2^28 cases) and the shipped self-test repeats it on 16,384
constructed cases.

*Use in stage A.* In the order S2K (Section 4) a lane holds the trial with
C2.a1 = r 2^16 + i (r = 7g + l < 2^16), so C2.d1 = ROR(C2.a1, 16) =
i 2^16 + r: its bits 8, 9 are those of r and its bits 24..27 are bits 8..11
of i, constant for the 256 positions i of a block. The stage-A register is
Z = T1 + X6K + b1 with T1 = X2 + w7 + w0 (table word, below 2^32),
X6K = X6 + K' (member register plus the block's constant) and b1 = C2.b1;
since C2.a2 = C2.a1 + b1 + w0 and C2.a1 = X2 + X6 + w7, Z = C2.a2 + K'
(mod 2^32), and Z < 2^36. With ALLA = 0B000300 (bits 8, 9, 24, 25, 27),
pA = (Z AND ALLA) + (2^32 - ALLA) has bit 32 equal to 1 iff Z AND ALLA =
ALLA (Z AND ALLA <= ALLA < 2^28), i.e. iff the trial satisfies rule A
(Lemmas A, A3), and pA < 2^33.

**Lemma F2 (stage-B test, new).** Let KF = MF AND NOT VF = 00090188 (bits
3, 7, 8, 16, 19). Then (c1 AND MF) = VF iff ((c1 + KF) mod 2^32) AND MF =
MF. *Proof.* Write s = c1 + KF. KF has no bits below 3, so s_3 = 1 - c1_3,
with a carry out of bit 3 iff c1_3 = 1. If c1_3 = 0, bits 4..6 receive no
carry and are those of c1, and the same argument gives s_7 = 1 - c1_7 and
then s_8 = 1 - c1_8 (each without carry when the bit of c1 is 0), s_15 =
c1_15 (KF_15 = 0, no carry), s_16 = 1 - c1_16, s_19 = 1 - c1_19. So when
c1 passes the filter (bits 3, 7, 8, 16, 19 zero and bit 15 one) the six
bits of s are 1; conversely if they are 1, reading the bits in increasing
order gives c1_3 = 0 (no carry in), hence no carry out, c1_7 = 0, ..., and
c1_15 = 1, c1_16 = c1_19 = 0. QED. (Also checked on 3 * 2^20 cases by
`lemma_check.py`, no disagreement.) The stage-B register is C1K = D1 +
(Y11 + KF) = c1 + KF (mod 2^32); pF = (C1K AND MF) + (2^32 - MF) has bit
32 equal to 1 iff the trial passes the filter, and xF = pF AND xA (xA from
stage A: bits 32 only) has bit 32 of a lane equal to 1 iff the lane passes
rule A and the filter.

**Stage decisions.** With B32 the word holding 2^32 in every lane,
xA = pA AND B32 holds exactly the seven bits 32; the compare-and-branch of
stage A (xA against 0) is taken iff some lane passes rule A, and that of
stage B (xF against 0) iff some lane passes rule A and the filter. In the
last group of a member (g = 9,362) B32 holds 2^32 only in lanes 0 and 1,
the two distinct trials of that group, so lanes 2..6 (which repeat trials of
group 0, Section 4) take no part in either decision.

## 4. Algorithm

Constants: V = 1,512,538 values of vd; N = V * 2^80 = 2^100.5285 trials in
V * 2^64 * 9,363 batches; p_B = 32,052,445,611,625 / 160,855,115,169,792 =
0.1992628 (Section 8.2); premises theta_B = 0.5766 and theta_C = 1.002 of
H1 (ii) (Section 8.2) and the budgets (the factor 6001/6000 is from
5266c5ce)

    E_B = ceil(theta_B * 6001/6000 * p_B * V * 2^64 * 9,363) = 30,020,253,184,127,225,509,418,523,375 = 2^94.5999
    E_C = ceil(theta_C * 6001/6000 * N * 2^-11)            = 894,779,639,186,168,792,987,371,257 = 2^89.5317

*Order S2K.* Fix an outer step and a member y, and let c = X6 + w7 (X6 from
step Y, w7 from step O). For a group g < 9,363, a lane l < 7 and a position
i < 2^16 put r = 7g + l and

    C2.a1 = r 2^16 + i,   X2 = (C2.a1 - c) mod 2^32,   C2.d1 = ROR(C2.a1, 16) = i 2^16 + r

(C2.a1 = X2 + X6 + w7 by step T, and X14 = 0, so C2.d1 = ROR(C2.a1, 16)).
For r < 2^16 the map (r, i) -> X2 is a bijection onto all 2^32 values, so
the groups g < 9,362 (r up to 65,533) and lanes 0, 1 of the last group
(r = 65,534, 65,535) hold every trial of the member exactly once; lanes 2..6
of the last group are given r - 2^16 = 0..4, i.e. they repeat the trials of
lanes 0..4 of group 0 at the same position, and they are masked out of both
stage decisions (Section 3). A *batch* is (outer step, member, group,
position); there are 2^16 * 9,363 * 2^16 = 9,363 * 2^32 batches per outer
step, as in 21252124; 9,362 of every 9,363 hold seven distinct trials and
the rest two.

1. Once: the list of the 65,536 members of S8 in the order of Section 3,
   the 256 block constants F_b = F(b AND 15) and G_b = 2^32 + 1 - F_b
   (Lemma A3), the words D0 = (0, 1, .., 6), DLAST = (65,534, 65,535, 0, 1,
   2, 3, 4) and B32_01 (2^32 in lanes 0, 1); the budget registers cB = E_B,
   cC = E_C.
2. For each vd < V and each w5 in 0..2^32-1 (an *outer step*): draw one
   fresh uniform 256-bit word and take vc, S15, S9 from its 32-bit words 0
   to 2; set D3.d1 = X3 (so X14 = 0); run step O. Build the *X2 table*: for
   a = 0, 1, .., 2^32 + 2^16 - 1 the table word T[a], whose lane l holds, for
   X2 = (a + l 2^16) mod 2^32, the eight words -w2, X2 + w7 + w0, S5, w3,
   S12, w12 - S1 - S6, -S1 - S6 and -S0 - S5 of step M. Then for each member
   y: the member step (step Y for y, c = X6 + w7, the member registers).
   Then for each group g = 0, .., 9,362:
   - halt the run with failure if cB < 2^16 or cC < 2^16;
   - set the group registers from the lanes r of C2.d1 at i = 0 (7g + l; the
     last group DLAST, and B32 := B32_01 for it) and the accumulator acc to
     all ones;
   - for each position i = 0, .., 65,535 (before positions 256 b, b < 256,
     the block constants F_b, G_b enter two registers) run the batch whose
     lane l is the trial (vd, w5, X2 = ((7g + l) 2^16 + i - c) mod 2^32, y),
     reading the table word a = base_g + i, base_g = (7g 2^16 - c) mod 2^32
     (a < 2^32 + 2^16). Every batch runs stage A. If some lane passes rule A,
     the batch subtracts 1 from cB and runs stage B. If some lane passes rule
     A and the filter, it subtracts 1 from cC and runs stage C, which
     computes the words D1, D3, W4, D6 of Lemmas D and D' for all seven lanes
     and ANDs a per-lane indicator into acc (bit 32 of a lane stays 1 iff
     none of that lane's trials so far has all four words zero);
   - after the group, one test: is bit 32 of some lane of acc zero (compare
     and branch)? If so, step 3.
3. Recompute the 2^16 batches of this group with all three stages and take
   the first lane with all four words zero (under 2^25 operations),
   recompute that trial in scalar form from (vd, w5, X2, y) (steps O, M, Y,
   T), build A, B (S2, S3), evaluate both complete digests, compare, output
   the pair if they are equal, and halt in either case.
4. Halt with failure when all trials are done.

There are N = V * 2^32 * 2^16 * 2^32 trials, the same as in 21252124, all
distinct pairs for every value of the coins (vc, S15, S9 of each outer
step) (Theorem 1: two trials differ in vd, w5, X2 or y, and each is a value
of the forward computation of A). Step 3 runs at most once. Each group has
at most 2^16 entries of each stage and starts only if both registers hold
at least 2^16, so at most E_B batches complete stage B and at most E_C
complete stage C, and the registers never go below 0.

**Completeness.** Let a trial be good (R = 0, rule A, filter). It is held
by a lane that takes part in the decisions (lanes 0, 1 of the last group, or
a lane of another group), so its batch enters stage B (Lemma A3) and stage
C (Lemma F2), stage C computes its four words exactly (Lemmas D, D',
Section 5) and its indicator clears bit 32 of its lane of acc, which the
AND keeps cleared to the end of the group. So, unless a budget has halted
the run before, the block test of its group (or of an earlier one) is
taken, and step 3 outputs a pair with equal complete digests (R = 0 is
equality of the two digests, Lemmas H, D'). A trial with R = 0 that is not
good is found only if its batch reaches stage C; Section 7 does not count
it.

**What the shipped program holds.** It contains the counted pieces (the
outer step with its random word, the table entry and one table word, the
member step, the end of a group and the set-up of the next, the block
update, the three stages of a batch with both budget registers, the block
test), the member list, the block constants, and the ledger with E_B and
E_C. The loops over vd, w5, a, y, g, b and i and step 3 are defined by this
text; their counts are in Section 9.

## 5. The counted pieces on a 64-register machine

A packed 256-bit word holds seven 36-bit lanes (offsets 0, 36, .., 216),
each representing a value modulo 2^32 with four guard bits. A rotation by
r is PROR = ((z >> r) AND A_r) OR ((z << (32 - r)) AND B_r), 5 operations,
reading only the low 32 bits of each lane. x - y with constant x is
(y XOR M) + (x + 1) (M = 2^32 - 1 per lane); subtracting a constant is
adding its negation. Every executed primitive (add, xor, and, or, shift,
compare, branch, load, store, random word) counts 1; shift amounts, load
offsets and branch targets are instruction fields. The machine model is the
256-bit word RAM of the cost model with 64 registers.

**The batch in three stages.** The loads are the eight words of the table
entry a (at offsets 8 i + q from the group's pointer, instruction fields in
the unrolled group body); every other operand is a register. Every
execution of a stage executes the same operations.

| Stage | Computes | Ops |
|---|---|---:|
| A | load -w2 (1); X0 = XA + (-w2), fd = X0 ^ ROL(X15,8) (2); c1 = fd + E = X10 + C2.d1 (E = S10 + X15 + C2.d1) (1); E = E + 2^16 for the next position (1) | 5 |
| A | C2: b1 = ROR(X6 ^ c1, 12) (6); load X2 + w7 + w0 (1); Z = (X2 + w7 + w0) + X6K + b1 = C2.a2 + K' (2) | 9 |
| A | rule-A test (Lemma A3): tA = Z AND ALLA, pA = tA + (2^32 - ALLA), xA = pA AND B32 (3); compare with 0, branch (2) | 5 |
| B | budget: cB = cB - 1 (1) | 1 |
| B | C2.d1 = E + (-S10 - X15 - 2^16) (1); C2.a2 = Z + nKp, nKp = 2^33 - K' (1); z = a2 ^ d1 (1); X10 = fd + (S10 + X15) (1) | 4 |
| B | Y14 = ROR(z,8) (5), Y10 = c1 + Y14 (1), Y6 = ROR(b1 ^ Y10,7) (6); fc = X10 + (-X15) (1); load S5 (1); X5 = ROR(ROR(fc ^ S5,12) ^ X10,7) (12) | 26 |
| B | load w3 (1); C1: a1 = X1 + X5 + w3 (2), d1 = ROR(a1 ^ X13,16) (6), c1 = d1 + X9 (1), b1 = ROR(c1 ^ X5,12) (6) | 16 |
| B | load S12 (1); ga = R ^ S12 (1); sY = a1 + b1 + ga = Y1 + S1 + S6 (2); load w12 - S1 - S6 (1); E1: a1 = sY + Y6 + (w12 - S1 - S6) (2); d1 = ROR(a1 ^ Y12,16) (6); C1K = d1 + (Y11 + KF) (1) | 14 |
| B | test of rule A and the filter (Lemma F2): wF = C1K AND MF, pF = wF + (2^32 - MF), xF = pF AND xA (3); compare with 0, branch (2) | 5 |
| C | budget: cC = cC - 1 (1); E1 for A and B: c1, c1' (1 each), b1, b1' (6 each), a2, a2' (2 each), d2, d2' (6 each), c2, c2' (1 each) | 33 |
| C | P = a2 ^ a2', Q = c2 ^ c2' (2); ROR(b1 ^ b1' ^ Q, 7) (7) | 9 |
| C | load -S1 - S6 (1); Y1 = sY + (-S1 - S6) (1); Y13 = ROR(C1.d1 ^ Y1,8) (6); Y9 = C1.c1 + Y13 (1) | 9 |
| C | h1 = ROR(Y14 ^ e1,16) (6; e1 = y + Y3 is a member register), h1' = h1 ^ eta (1); g1, g1' (2); f1, f1' (6 each) | 21 |
| C | fa = ROL(fd,16) ^ S15 (6); load -S0 - S5 (1); e1 + w8 = e1 + fa + (-S0 - S5) (2); e2 (1), e2' (+ DY3, 2); h2, h2' (6 each); g2, g2' (1 each) | 26 |
| C | D1 = P ^ g2 ^ g2' (2); D3 = e2 ^ e2' ^ Q (2); W4 = ROR(P,1) ^ P ^ f1 ^ f1' (8); D6 (xor 2) | 14 |
| C | OR of the four (3), AND M (1), indicator u = T + M (1), acc = acc AND u (1); jump to the next position (1) | 7 |
| | **stage A 19, stage B 66, stage C 119** (parts 42 + 56 + 21) | |

ALLA = 0B000300, MF = 00098188, KF = 00090188 in every lane. The stage-A
branch is taken (to the out-of-line stages B and C of this position) iff
some lane passes rule A; the stage-B branch falls through to stage C iff
some lane passes rule A and the filter, and otherwise jumps to the next
position. The lines of steps M, Y and T that the batch evaluates are those
of Section 2 with the table and member words in place of their names:
XA + (-w2) = va - X4 - w2 = X0, R ^ S12 = ROL(gd,16) ^ S12 = ga, sY +
(w12 - S1 - S6) + Y6 = Y1 + Y6 + w12, and X6, X1, Y12, y as they stand; w9
and w11 are not needed for R. Compared with 21252124, stage A no longer
rotates C2.a1 (C2.d1 comes from E) and tests Z instead of z (Lemma A3);
stage B recomputes C2.d1, C2.a2, z and X10 (4 operations) and no longer
computes Y1, Y13 and Y9, which stage C now computes (C1.d1 and C1.c1 stay in
registers from stage B).

*Indicator and block test.* After the AND in stage C, a lane holds
T = D1 OR D3 OR W4 OR D6 below 2^32, and bit 32 of u = T + 2^32 - 1 is 1
iff T != 0. acc starts at all ones in every group and every stage C sets
acc = acc AND u. After the last position of a group, acc AND (2^32 per
lane) equals the broadcast 2^32 iff every lane of every batch that ran
stage C had T != 0, so the branch to step 3 (load 2^32, AND, compare,
branch: 4 operations per group) is taken iff some trial of a batch of the
group that ran stage C has R = 0 (Lemma D'; in the last group this includes
lanes 2..6, which repeat real trials).

*The block update (4 operations per 256 positions).* Load F_b, X6K = X6R +
F_b; load G_b, nKp = NR + G_b. With X6R = X6 + (D AND 0300) and NR =
(D AND 0300) XOR M = 2^32 - 1 - (D AND 0300) (group set-up), X6K = X6 + K'
and nKp = 2^33 - K' for the K' of Lemma A3 of every lane at the 256
positions of block b (C2.d1 bits 8, 9 are those of D = r, bits 24..27 are
b AND 15).

*The group set-up (14 operations; last group 12).* Budget halt test: cB and
cC each compared with 2^16 (an immediate) and a branch to the halt (4);
acc = all ones (load, 1); load the lanes D = (7g + l) from the D slot
(last group: load DLAST, and load B32_01 into B32; 1 + 1); E = D + (S10 +
X15) (1); load 0300 (1), DM = D AND 0300 (1), X6R = X6 + DM (1), NR = DM
XOR M (1); except in the last group, load 7, D + 7, store into the D slot
(3).

*The group end (7 operations; after the last group 1).* The table pointer
p = 8 base_g (8 words per table entry) becomes (p + 7 * 2^19) AND
(2^35 - 1) = 8 base_{g+1} (2; the X2 table occupies word addresses 0 to
8 (2^32 + 2^16) - 1, entry a at words 8a to 8a + 7, so p is the absolute
address of entry base_g); the group counter is loaded, incremented,
stored and compared with 9,362, and a branch selects the next group's code
(the last group's prologue loads DLAST and B32_01 instead) (5). After the
last group of a member B32 is restored (load, 1).

*Budgets.* cB and cC are registers holding E_B and E_C at the start of the
run; an entry of stage B or C subtracts 1 (1 operation); before each group
the run halts with failure if either holds less than 2^16. A group has at
most 2^16 entries of each stage, so no register goes below 0, stage B is
completed at most E_B times and stage C at most E_C times, and the run halts
only after more than E_B - 2^16 (or E_C - 2^16) entries.

*Lane bounds.* Static per-lane upper bounds for all inputs are tracked by
the program for every addition: below 4.0, 7.0, 9.0, 6.0 and 2.0 times 2^32
in stage A, stage B, the E1 part of stage C, its E3 part and the residual
part, 1.0 and 1.98 times 2^32 in the group set-up and the block update and
6.0 times 2^32 in the table word, all below 2^36, so no carry leaves a lane
(E grows by 2^16 per position and stays below 2^33 + 2^17 in a group); XOR,
AND and PROR read only the low 32 bits of lanes or mask the rest. Table
words and member registers are reduced below 2^32 when they are formed.

*Registers.* 47 registers are resident during the batches: the 10 rotation
masks A_r, B_r (r = 16, 12, 8, 7, 1), 8 global constants (M, ROL(X15,8),
-X15, Y11, Y11', Y11 + KF, eta, DY3), 6 constants of the stage tests and of
E (ALLA, 2^32 - ALLA, B32, MF, 2^32 - MF, 2^16), 7 per outer step (S10 +
X15, X13, X9, S15, w5, w5 + delta, -S10 - X15 - 2^16; X14 = 0 needs none),
7 per member (XA = va - X4, X6, X1, R = ROL(gd,16), Y12, y, e1 = y + Y3), 6
per group and block (E, X6R, NR, X6K, nKp, the table pointer), acc and the
two budget registers. With the live temporaries the peak is 62 of 64 (the
program's liveness count over the path group end, group set-up, block
update, all three stages and block test; the other paths are prefixes of
it). The table build uses at most 37 registers, the scalar member and outer
steps fewer.

**The X2 table (per outer step).** Entry (29 operations): the ten masks for
rotations by 24, 20, 16, 12 and 7, M, 1 and six IV-derived constants, the
nine words of step O that step M reads, the X2 word (lanes l 2^16 - 1) are
loaded, and the pointer is reset. Each table word (94 operations): X2 = X2 +
1 per lane, AND M (2); the 21 lines of step M in all seven lanes; the eight
words -w2, X2 + w7 + w0, S5, w3, S12, w12 - S1 - S6, -S1 - S6, -S0 - S5
reduced below 2^32 and stored (8 stores); next word, compare, branch (3).
2^32 + 2^16 words per outer step (the last 2^16 repeat the first, so that a
group's 2^16 consecutive entries never wrap).

**The member step (per member, 112 operations, scalar).** Load y from the
member list and nine scalar words stored by step O (10); the lines of step
Y in scalar form (each 32-bit addition or subtraction counted 2 with its
mask, rotation 4, XOR 1); c = X6 + w7 and the pointer 8 ((-c) mod 2^32) of
group 0; e1 = y + Y3; the seven member registers XA, X6, X1, R, Y12, y, e1,
each broadcast to seven lanes (7 operations each); the D slot := D0 (load,
store) and the group counter := 0 (store); next member (3).

**The outer step (274 operations).** One fresh uniform 256-bit word (1) and
its words 0 to 2 as vc, S15, S9 (AND; shift and AND twice: 5); D3.d1 = X3
is an instruction constant (so ROL(D3.d1,16) is one too, X14 = 0 is not
computed and X9 = D3.c1); step O in scalar form (as above); the nine
packed words of the table entry and the seven per-outer batch registers,
each broadcast to seven lanes and stored (8 operations each); the nine
scalar words of the member step (C0.b1, -C0.c1, C0.d1, -C0.b1 - w6,
ROL(C0.d1,16), S6, -S11, -X4, w7), computed and stored; the next-w5 loop
step and two stores (6); the loads of the seven per-outer registers of the
batch (7). (21252124: 318.)

*Self-test of the shipped program.* `python3 experiments/s8stage.py
--selftest 2000 9`, run from the repository root, builds 2,000 cases (the
context words from SHAKE-256 of the seed, then D3.d1 = X3 as in the
algorithm; the random word of the outer step holding the three coin words
in words 0 to 2 and random words 3 to 7; a member number (every seventh case
0 or 65,535), a group (every fourth case the last group, every ninth group
0) and a position (every sixth case 0, 65,535 or the first of a block); in
every fifth case each context word is 0, 2^32 - 1 or random before D3.d1 is
set). Each case runs the counted outer step from the random word, the
member step, for g > 0 the end of group g - 1 from base_{g-1}, the set-up
of group g, the block update of the position's block, the table entry and
the counted table word at the position (from the previous word's X2 lanes),
the three stages of the batch (stages B and C computed whatever the
decisions, the accumulator changed only as in the staged flow) and the
block test, and after the last group its end. It checks: the outer step
takes exactly the three coin words from the random word, D3.d1 = X3 and
X14 = 0, and every word it stores equals step O; the member registers equal
step Y and c, the pointer equals 8 base_g; E, X6R, NR and the stored next D
equal their definitions, X6K = X6 + K' and nKp = 2^33 - K' in every lane;
the table word equals step M for the seven X2 values; E - (S10 + X15) =
ROR(C2.a1, 16) and C2.a1 = r 2^16 + i in every lane; and for every lane it
builds the trial's messages A, B by steps O, M, Y, T, S2, S3, compresses
them with the program's own 2-round compression and with
`verifier/blake3.py blake3(m, 2)`, and checks: X3, X7, X11, X15 after round
0 are the constants, digest words 0, 2, 5, 7 agree, Y4 = member in S8 for
both, eta = 830303cf; bit 32 of pA is 1 iff h1 of E3 satisfies rule A; bit
32 of xF is 1 iff the lane takes part in the decisions and satisfies rule A
and the filter on c1 of E1; the four packed words equal D1, D3,
ROL(D4, 7) ^ D1 and D6 computed from the XOR of the two digests on words 1,
3, 4, 6, the packed T equals their OR, and bit 32 of the lane's indicator
is 1 iff the digests differ; both decisions equal 'some lane taking part
passes'; and the block test is taken exactly when some lane of a batch that
ran stage C has equal digests. Result (run for this package): 14,000 of
14,000 lanes right with the verifier, 14,000 of 14,000 flags right, 2,000
of 2,000 decision pairs, block tests, piece checks and group-operation
counts right (500 last-group cases); 19, 66 and 119 operations in every
execution of stages A, B and C (parts 19, 66, 42 + 56 + 21), 4 in every
block update and block test, 14 / 7 (12 / 1 in the last group) in every
group set-up and end; 274, 112, 94 and 29 operations in every outer step,
member step, table word and table entry; static bounds as above; peaks of
62 and 37 registers (47 resident); about 4 s. Pattern tests on constructed
words: the indicator and the block test (blocks of 1, 2 and 3 batches, all
128 zero/nonzero lane patterns, twice) 768 of 768; the stage-A test (all
128 patterns of lanes passing rule A, each lane with a random C2.d1 and its
K', passing lanes with the five conditions on z set, failing lanes with one
of them violated or random, guard bits random, twice) 256 of 256; the
stage-B test (all 16,384 pairs of rule-A and filter patterns of the seven
lanes) 16,384 of 16,384; Lemma A3 on 16,384 constructed cases (all 64 x 64
patterns of the six bits of d1 and a2, four fillings) with no disagreement;
the budget registers (a register holding E = 2^16 k + r, k < 3, r = 0, 1,
2^16 - 1, decremented per entry with 2^16 or a random number of entries per
group and tested before each group, never goes below 0, completes at most E
entries and halts only when fewer than 2^16 remain) right. The 65,536
member numbers give 65,536 distinct members of S8; Lemma B holds for 6 of 6
betas. Exit status 0 only if all of these hold, and only if
`verifier/blake3.py` was imported. No real lane with R = 0 occurs at this
size; the taken branch is covered by the pattern tests. Runs: a development
self-test of 200 cases (with `--ledger`) on a draft of the program, before
its class-filter observations were cut to 16 (output not kept); the
2,000-case self-test on the program before its PREMISE line was set (SHA-256
3aef733e...e27518); and the 2,000-case self-test on the shipped program,
with output identical byte for byte (the self-test does not read the
premises).

*Broken copies.* Six deliberately broken copies of the shipped program
fail the self-test (`--selftest 50 9`, exit status 1): the block constant F
without its 2^26 term (stage-A patterns 30 of 256 right, flags 336 of 350);
stage B recovering C2.d1 without the 2^16 correction (0 of 350 lanes right);
the group set-up forming X6R without bits 8, 9 of D, so that K' misses them
(86 of 350 lanes and 330 flags right, piece and group checks failing); the
last group keeping B32, so that lanes 2..6 are not masked (12 of 50 piece
checks fail); the table word X2 + w7 + w0 without w0 (0 of 350 lanes right);
and the global KF without bit 19 (stage-B patterns 2,105 of 16,384 right). A
seventh copy, which changes only the batch constant Y11 + KF (KF without bit
19), passes the 50-case self-test, because the stage-B pattern test builds
its words with KF itself and none of the 350 real lanes with rule A passed
the other five filter bits; it fails the 2,000-case self-test (13,993 of
14,000 flags and 1,993 of 2,000 decisions right). An organizer class-filter
run would very likely catch it as well: at the rate of the 2,000-case run (7
wrong flags in 14,000 lanes) a run of 16,128 lanes expects about 8 wrong
flags, and one wrong flag fails the prediction flags_right 63. The program
was not changed after this finding, because the preregistration allows only
the PREMISE line to change. All seven scripts, outputs and hashes are kept.

## 6. Experiments (organizer-run)

`experiments/s8stage.py`, standard library only, seeds expanded by
SHAKE-256, no BLAKE3 import in organizer mode.

- `half-collision`: per seed, the context words (vc, vd, S15, S9, w5, X2;
  D3.d1 = X3 as in the algorithm) and a member number of S8; returns the
  pair of Theorem 1. Event: digest words 0, 2, 5, 7 agree (exact, all
  seeds). Observations: the program locates the batch of the order S2K that
  holds this trial (C2.a1 = X2 + X6 + w7 = r 2^16 + i, g = floor(r / 7)) and
  runs the counted outer step (from a 256-bit word whose words 0 to 2 are
  the three coin words), the member step, the end of group g - 1 (g > 0) and
  the set-up of group g, the block update, the table entry and table word of
  the position, the three stages of the batch and the block test:
  stage_a_ops 19, stage_b_ops 66, stage_c_ops 119, block_test_ops 4,
  outer_ops 274, table_word_ops 94, member_ops 112, block_ops 4,
  group_ops_right 1 (set-up, block test and ends with the counts of
  Section 5), pieces_right 1 (every word the pieces leave equals the
  construction), lanes_right 7 (four packed words and the indicator equal to
  the forward computation), flags_right 7 (both stage flags equal rule A,
  and rule A with the filter, of the forward computation), decisions_right
  1, tests_right 1, member_in_s8 1 (predicted for every seed).
- `class-filter`: per seed, the context words and member as above, a group
  g < 9,362 and nine consecutive positions 256 b + 252 .. 256 b + 260
  (b < 255, both from SHAKE-256 of the seed), so that the run crosses a block
  boundary and makes two block updates; the nine batches (63 trials: seven
  values of X2 per position) run in the staged flow with the block test,
  after the counted pieces; returns the pair of lane 0 of the first batch
  (same event). Observations per seed: trials 63, y4_equal 63, eta_equal
  63, lanes_right 63, flags_right 63, decisions_right 9, tests_right 1,
  pieces_right 1, group_ops_right 1, block_updates 2, lemma_b 6 (predicted
  for every seed), and the counts rule_a_lanes, filter_lanes,
  filter_and_rule_a_lanes (rates near 2^-5, 2^-6, 2^-11 per trial),
  stage_b_batches and stage_c_batches (at most the first and the third count
  of the seed). Each seed is one outer step and member, whose trials are not
  independent. The expected totals per run of 256 seeds under M are 504, 252
  and 7.9 lanes and 459.1 and 7.9 batches; rule A clusters, so no per-run
  range is predicted. The premise of H1 (ii) is a run average; the
  stage-B ratio of one run (stage_b_batches / 459.1) has expectation about
  0.5765 and a standard deviation of about 0.067 (each seed is one member
  and nine consecutive positions, so its batches are clustered), so about
  half of all runs show a ratio above 0.5766, and ratios between about 0.40
  and 0.75 are consistent with H1 (ii); one run is not evidence for or
  against it.

Coverage: the organizer experiments almost never reach the last group
(half-collision: probability 2^-15 per seed; class-filter uses g < 9,362),
so the masking of lanes 2..6 in the last group is tested by the self-test
(500 of its 2,000 cases are last-group cases) and by a broken copy
(Section 5), not by these experiments.

*Replays (preregistered; participant-run local replays using the
repository's `experiments/runner.py`).* Before any replay of the shipped
program (SHA-256 6543e741...0377eb1), the program, the harness (unchanged from
21252124 and 098e66f4: it runs `experiments/runner.py` of the repository
with `verifier/blake3.py` as digest; 1185392d...24b9bde) and the list of 41
nonces (the public seed, and holdout_nonce = the first 32 hex digits of
SHA-256 of 'blake3-r2-v103 replay NN', NN = 01 to 40; our own nonces, not
organizer holdouts; list 1f4d8eb5...887e10) were fixed and hashed (list of
hashes and UTC time 2026-10-07T21:46:45Z, SHA-256 b6ca4f73...138411),
and all 41 runs were then made one after another; no other replay of the
shipped program was made. In every run both experiments have 256 of 256
successes, no repeated pair, and every predicted observation exact for every
seed. Totals of 16,128 lanes per run: rule A 330 to 629 (mean 512.3, sd
67.1, above the binomial value because of clustering), filter 218 to 281
(mean 252.4), both 2 to 16 (mean 7.7, sd 3.0); batches entering stage B 186
to 318 of 2,304 (mean 269.2, sd 31.0) and stage C 2 to 16 (mean 7.6), never
more than the lanes with both; on the public seed 466, 238, 8, 226 and 8. As
ratios to M over the 41 runs (standard error from the run-to-run sd):
batches entering stage B 0.586 +- 0.011 of 459.1, rule A and the filter
0.973 +- 0.059 of 7.875, rule A 1.016 +- 0.021 of 504. These agree with the
uniform sample of Section 8.2 (0.5765 and 0.99987); one run of 256 clustered
seeds cannot resolve the margins of (ii). One execution of class-filter
takes 1.35 to 1.42 s on our machine, half-collision under 0.25 s (the 41
runs took 2 min 14 s, 2026-10-07T21:46:59Z to 21:49:13Z, 1-minute load at
most 2.4). Before the program was final, two
development runs of the runner were made on a draft: the first was rejected
by the runner because class-filter returned 25 observations (the limit is
16; the program was changed to return the 16 above), the second (holdout
nonce = first 32 hex digits of SHA-256 of 'blake3-r2-v103 dev 01', on the
draft that differs from the shipped program only in the PREMISE line of the
ledger) gave 256 of 256 in both experiments with every predicted
observation exact (totals 546, 214, 10, 289, 10).

Observations are the program's own and untrusted; they check the
generator, the class, the order S2K, the stage tests and the counted pieces
against a forward computation of real messages. They do not measure H1.

## 7. Success probability

The probability space is the V * 2^32 random words of step 2, one per outer
step, independent and uniform (each supplies vc, S15 and S9; D3.d1 = X3 is
fixed). Outer step k (k = 1, .., V * 2^32) is a fixed pair (vd, w5), and
all its trials, its batches in the order S2K, its stage decisions and
residuals are a function of that pair and its own random word r_k.

**H1 (score-critical; the only premise).** Over the random words of the
algorithm:

(i) the N = V * 2^80 trials behave with respect to "good" (R = 0, rule A
and the beta filter) like independent events of probability at least
F * 2^-128 each, F = 92,675,072 (half of the exact count 185,350,144 of
Section 8; 2^26.4657), to the extent that the probability that no trial is
good is at most exp(-lambda) + 0.002 with lambda = N * F * 2^-128 =
0.4980001; and

(ii) averaged over the V * 2^64 * 9,363 batches of the run in the order
S2K of Section 4, the probability that a batch has a trial taking part in
its decisions that satisfies rule A (and so enters stage B) is at most
theta_B p_B with theta_B = 0.5766, and averaged over the N trials, the
probability that a trial satisfies rule A and passes the filter is at most
theta_C 2^-11 with theta_C = 1.002. Under the same seven-word model M that
gives the count of (i), with the distinct trials of a batch independent as
in (i), these probabilities are exactly p_B = (9,362 (1 - (31/32)^7) + 1 -
(31/32)^2) / 9,363 = 0.1992628 and 2^-11 (Section 8.2: 2^27 of the 2^32
words h1 satisfy rule A, 2^26 of the 2^32 words c1 pass the filter, h1 and
c1 = d1 + Y11 are independent uniform words of M, and for each member and
position 9,362 groups give batches of seven distinct trials and the last
group one of two). The value of theta_B lies below 1 because rule A
clusters (trials that share C2's inputs or their low halves); theta_B and
theta_C are not values of M: they were set by the preregistered decision
rule of Section 8.2 (52bb50ee's two tests on a grid) from a uniform sample
of 2^38 trials of this order whose runs, seeds and analysis were fixed by
its preregistration, and no other run was used to set them.

Part (ii) is a statement about first moments only. It says nothing about
how passing trials are distributed inside a batch, a group, a member or an
outer step; rule A is known to cluster, and nothing below depends on the
contrary.

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
then P(S_B > E_B - 2^16) <= exp(-6.9 * 10^6) and P(S_C > E_C - 2^16) <=
exp(-2.0 * 10^5).

*Proof.* Write S_B = sum over k of S_k, S_k the number of batches of outer
step k that enter stage B. S_k is a function of r_k, so S_1, S_2, .. are
independent, and 0 <= S_k <= m = 9,363 * 2^32, the number of batches of an
outer step. By Lemma A3 and the masking of Section 3 a batch enters stage B
iff one of the trials taking part in its decisions satisfies rule A, so
E S_B is the sum over all V * 2^64 * 9,363 batches of the probability of
this event, at most theta_B p_B V 2^64 9,363 by H1 (ii). Put X_k = S_k / m
and mu_H = theta_B p_B V 2^64 9,363 / m = 7.464 * 10^14. E_B - 2^16 = (1 + delta)
mu_H m with delta = 1.66667 * 10^-4 (just below 1/6000, 5266c5ce), so Lemma C gives
P(S_B > E_B - 2^16) <= P(sum X_k >= (1 + delta) mu_H) <= exp(-delta^2 mu_H
/ 3) = exp(-6.91 * 10^6). For stage C, a batch enters only if one of its trials
satisfies rule A and the filter (Lemma F2), so S_k is at most the number of
such trials of outer step k (a union bound, valid for any dependence between
the trials of a batch; the repeated lanes of the last group take no part)
and E S_C <= theta_C * 2^-11 * N by H1 (ii); mu_H = theta_C 2^-11 N / m =
2.225 * 10^13, E_C - 2^16 = (1 + delta) mu_H m gives delta = 1.66667 * 10^-4, and the bound
is exp(-2.06 * 10^5). QED. (`python3 experiments/s8stage.py --ledger` prints
E_B, E_C, mu_H, delta and both exponents.)

**Success.** The run with budgets executes exactly as the run without them
until it halts at a group's budget test, and that test halts only when a
register holds less than 2^16, i.e. after more than E_B - 2^16 entries of
stage B or more than E_C - 2^16 of stage C; so no budget halt occurs if
S_B <= E_B - 2^16 and S_C <= E_C - 2^16. If moreover some trial is good, the
completeness argument of Section 4 shows that step 3 outputs a pair of
distinct messages of 55 and 63 bytes with equal complete digests. So, under
H1,

    P(success) >= 1 - (exp(-lambda) + 0.002) - exp(-6.9 * 10^6) - exp(-2.0 * 10^5)
               >= 1 - exp(-0.4980001) - 0.002 - 10^-80000 = 0.39025 >= 0.39.

The time of Section 9 holds for every value of the coins: stage B and
stage C are charged at their budgets. Sensitivity: with a good-trial rate
f * 2^-128 the same search reaches 0.39 only for f >= 2^26.4645 (lambda >=
0.49758); with the uniform rate (f = 1) it needs 2^127 trials and gives
about 120.2.

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
the six parts and 185,350,144 in about 2 minutes; `--count all` also
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
count was rerun on the shipped program of this version with identical output.

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
unsubmitted branch-free draft in this order, `rt2l.c`, a C program whose
event counts equal those of the
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
made in the order of 2bb5d604 with random D3.d1. The stages and the batching
do not change which trials are run or their residuals, only which are
examined together; a fresh random word per outer step changes the coin words
from one per run to one set per outer step, which the measurements of 8.2
use.

**With D3.d1 = X3 (21252124 and this version).** The table above has D3.d1
random. With D3.d1 = X3, X14 = 0 in every trial, so C2 runs with d = 0 and
C2.d1 = ROR(a1, 16); C2's outputs Y2, Y6, Y10 and Y14 (Y6 enters E1, Y14
enters E3) still vary with X2, X6 and X10, but no longer with a coin in the
d input. X9 = D3.c1 = S9 + X3 varies only with the coin S9; D3.a1, D3.b1,
S4, S3, X4 and the words derived from them vary with w5 and S9. Within one
outer step these words were fixed in the random-D3.d1 configuration as
well; what changes is that X14 no longer varies across outer steps and that
X9 and X4 no longer depend on a separate coin. A review of 21252124 noted
that the E3 checks had not been repeated in this configuration. The
preregistered sample of Section 8.2 (`rtuni4.c`) therefore counts, on every
trial, all events of the table above, in the algorithm's configuration
(2^38 trials, mode fixed) and in a control with random D3.d1 (2^36, mode
rand), both in the order S2K:

| event | D3.d1 = X3 (2^38) | random D3.d1 (2^36) | ratio +- Poisson s.e. (understates the error of clustered events) |
|---|---:|---:|---:|
| rule A (model 2^-5) | 2^-5.0000 | 2^-5.0000 | 1.0000 +- 0.0000 |
| filter (model 2^-6) | 2^-6.0000 | 2^-6.0000 | 1.0000 +- 0.0000 |
| rule A and filter (model 2^-11) | 2^-11.0002 | 2^-10.9999 | 0.9998 +- 0.0002 |
| beta in T6 (model 2^-8.8301) | 2^-8.8301 | 2^-8.8301 | 1.0000 +- 0.0001 |
| beta in T6 and rule A | 2^-13.8303 | 2^-13.8300 | 0.9998 +- 0.0005 |
| low 12 bits of n zero | 2^-10.9275 | 2^-10.9272 | 0.9998 +- 0.0002 |
| beta in T6 and low 8 bits of n zero | 2^-15.4467 | 2^-15.4462 | 0.9996 +- 0.0009 |
| E3: g1 ^ g1' = ROL(psi,12), tau 285020a0 | 2^-14.0002 | 2^-14.0004 | 1.0002 +- 0.0005 |
| low 16 bits of D1 and of D3 zero | 2^-30.50 (181) | 2^-30.22 (55) | 0.82 +- 0.13 |

The E1 events and the 2^-14 E3 event (which involves Y14 through h1 and
Y9 through g1) keep the rates of random D3.d1 within their standard errors
(ratios 0.9996 to 1.0002) and agree with the values of the table above
(2^-8.8299, 2^-13.8300, 2^-10.9277, 2^-15.4461, 2^-14.0004). The 2^-30 event
on the low halves of the digest differences D1 and D3 (which involves E1 and
E3 to the end of both calls) has 181 hits with D3.d1 = X3 against 55 in the
smaller control: ratio 0.82 +- 0.13, 1.4 standard errors below 1. Pooled
with the random-D3.d1 counts of the table above (73 and 79 hits in
2^36.585 trials each; 207 hits in 2^38.0 trials, rate 2^-30.31) the ratio
is 0.87 +- 0.09. This is consistent with equal rates at this sample size;
we report it as the weakest of these checks (even a factor 0.82 at this
level would lie inside the margin 2.000 of F, but H1 (i) does not rely on
that). The E1-part ratio (1.0086) and the per-outcome 2^-38 E3 partial
events were not repeated with D3.d1 = X3; H1 (i) assumes they keep their
rates.

The configuration also changes how rule A clusters inside a batch of the
order S2K: in the same preregistered sample the stage-B share is 0.5765 p_B
with D3.d1 = X3 (2^38 trials) and 0.6320 p_B with random D3.d1 (2^36
trials; 0.6319 to 0.6320 in each of the 8 control runs), while the
per-trial rule-A rate is equal (ratio 1.0000 +- 0.0000 in the table above).
This is a second-moment difference (rule-A outcomes of the trials of a
batch coincide more often with D3.d1 = X3); part (ii) measures it directly
in the algorithm's configuration, and H1 (i) assumes it does not extend to
the 2^-128 event good. The rare events of
the table are counted per trial, so their ratios are first-moment
comparisons of the same kind as for rule A.

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
trials enters stage B with probability 1 - (31/32)^7 = 0.1992775 and a
batch of the last group (two distinct trials) with 1 - (31/32)^2; for each
member and position there are 9,362 groups of the first kind and one of the
second, so the share over all batches of the run under M is p_B =
(9,362 (1 - (31/32)^7) + 1 - (31/32)^2) / 9,363 = 32,052,445,611,625 /
160,855,115,169,792 = 0.1992628 (the same value as in 21252124's order).
`python3 experiments/s8stage.py --count` enumerates the 64 + 64 patterns
and prints the integers 2^27, 2^26 and 2^53 and the fraction p_B next to the
count of 8.1; `--ledger` uses the same fraction. H1 (ii) asserts theta_B =
0.5766 times p_B and theta_C = 1.002 times 2^-11 as run averages; the budgets
are 6001/6000 times these (5266c5ce).

**What a uniform sample measures.** Draw an outer step uniformly (vd
uniform below V, w5 uniform, fresh coins vc, S15, S9; D3.d1 = X3), a member
y uniformly from S8, a group g uniformly below 9,363 and a position i
uniformly below 2^16. This is one batch of the run drawn uniformly from the
V * 2^64 * 9,363 batches, so the indicator b that it enters stage B has
mean exactly the run average that H1 (ii) bounds, and x = c / 7, with c
(0 to 7) the number of its trials taking part in the decisions that satisfy
rule A and the filter, has mean exactly (65,536 / 65,541) times the run's
per-trial rate of rule A with the filter (a uniform batch holds
65,536 / 9,363 distinct trials on average). Independent draws give i.i.d.
variables in [0, 1]: this is sampling from the run's own index space, not a
model. (Sampling single batches rather than whole outer steps follows
Subflatus3's 1d5e54ce, Lemma U there, for 21252124's order; the bounds below
follow 52bb50ee.)

**Lemma C' (lower-tail Chernoff bound; stated and proved in 52bb50ee).**
Let X_1, .., X_n be independent random variables with values in [0, 1] and
mu = E[X_1 + .. + X_n]. Then for 0 < delta < 1,
P(X_1 + .. + X_n <= (1 - delta) mu) <= exp(-delta^2 mu / 2). *Proof.* For
t > 0 and x in [0, 1], e^(-tx) <= 1 - x (1 - e^(-t)) (convexity), so
E e^(-t X_k) <= exp(-(1 - e^(-t)) E X_k), and by independence
E e^(-t sum X_k) <= exp(-(1 - e^(-t)) mu). Markov's inequality applied to
e^(-t sum X_k) with t = -ln(1 - delta) gives P(sum <= (1 - delta) mu) <=
exp(-mu (delta + (1 - delta) ln(1 - delta))), and
(1 - delta) ln(1 - delta) >= -delta + delta^2 / 2 for 0 <= delta < 1. QED.
*Consequence.* If the run average m is at least m0 and S is the observed
sum of n shares with S < n m0, then P(sum <= S) <= exp(-(n m - S)^2 /
(2 n m)), which is decreasing in m for n m > S, so at most
exp(-(n m0 - S)^2 / (2 n m0)). The empirical Bernstein inequality (Maurer
and Pontil 2009, Theorem 4; cited, not proved; Lemma C' does not depend on
it) gives, for i.i.d. variables in [0, 1] with unbiased sample variance V,
E Z <= mean + sqrt(2 V ln(2/delta) / n) + 7 ln(2/delta) / (3 (n - 1)) with
probability at least 1 - delta over the sample.

**The sample of this version (participant measurement, `rtuni4.c`,
Appendix A; preregistered).** `rtuni4.c` draws units as above (nine
SplitMix64 draws per unit; in mode rand also D3.d1, as a control) and
computes the distinct trials of each batch forwards with the formulas of
21252124's `rtuni2.c` (steps O, M, Y, T, C2, C1, E1, rule A on h1 of E3,
the filter on c1 of E1), together with the E1 and E3 events of Section 8.1.
Before any run of the sample, the counted program (the shipped program
with the placeholder PREMISE = (101/100, 5/4); it differs from the shipped
program only in that line), `rtuni4.c` and its binary, the cross-check
`rtunicheck4.py`, the analysis `summarize4.py`, the seed rule
`make_seeds4.py`, the launcher and the plan were fixed and hashed
(preregistration SHA-256 e2247e2b...1f4d, frozen 2026-10-07T21:29:56Z);
the seeds were then computed by the frozen rule (SHA-256 of
'blake3-r2-v103 S2K holdout NN', NN = 01..32, and 'blake3-r2-v103 S2K
control NN', NN = 01..08, first 16 hex digits; all 40 SplitMix64 streams
checked disjoint from each other and from every earlier stream). The seeds
are a fixed function of strings stated in the preregistration and leave no
choice; the protection against selection is that the preregistration fixes
the runs, the analysis and the decision rule, and that every run is
reported. Plan: 32
runs `./rtuni4 unit 1227227136 SEED fixed` (2^38.0 trials) and 8 runs in
mode rand (2^36.0 trials, H1 (i) comparison only), started by the frozen
launcher with nice -n 10, at most 8 at once and only while the 1-minute load
average was at most 12. Decision rule (fixed before the runs, `summarize4.py`;
delta = 2^-64):

- stage B: theta_B is the smallest k/10,000, 5,500 <= k <= 10,100, such
  that the empirical Bernstein bound on E b is at most theta_B p_B and the
  Lemma C' exponent at theta_B p_B is at least 20; if none passes, no
  stage-B premise ships for this order (STOP);
- stage C: theta_C is the smallest k/1,000, 1,001 <= k <= 1,249, such that
  the empirical Bernstein bound on E x is at most theta_C (65,536/65,541)
  2^-11 and the Lemma C' exponent there is at least 20; if none passes,
  theta_C = 1.25 (21252124's premise, whose evidence is per trial and so
  does not depend on the order);
- budgets 6001/6000 times the premises; STOP if any run is missing.

Both tests are monotone in theta, so the smallest passing grid value is an
upper confidence bound rounded up to the grid, with error probabilities
2^-64 (empirical Bernstein) and e^-20 (Lemma C') and no multiplicity cost.
The grid floors were set from the pilot below (0.573 to 0.577 p_B) and from
21252124's stage-C estimate (1.00007); a floor below the true mean only
makes the premise larger. Before the plan was fixed, one timing run of
2^24 trials and four cross-check runs were made (two versions of
`rtunicheck4.py`, each on 30,000 units, seed 5, mode fixed, and on 5,000
units, seed 6, mode rand; listed in Run selection); they are not part of
the sample. The first version (SHA-256 6e14e03e...dfc2) made the
comparisons below without the counted pieces. The frozen version compared,
unit by unit, the
drawn words, the stage-B flag, c and the counts of all nine events of
30,000 units (seed 5, mode fixed, 4 of them in the last group) and 5,000
units (seed 6, mode rand) with the forward computation of real messages by
the counted program (the shipped program before its PREMISE line was set,
SHA-256 3aef733e...e27518), and ran every tenth fixed unit (3,000) through
its counted pieces (outer step, member step, group set-up, block update,
three stages): all equal. All 40 runs are reported; none was repeated or
restarted.

| event (mode fixed: 32 runs, 39,271,268,352 units, 2^38.0 trials) | count | unit mean +- s.e. | empirical Bernstein (2^-64) | Lemma C' at the premise | premise | budget |
|---|---:|---:|---:|---:|---:|---:|
| batch enters stage B | 4,511,294,105 batches | 0.576501 +- 0.000008 of p_B | 0.576577 p_B | exp(-66.8) at 0.5766 p_B | **0.5766 p_B** | 0.5766961 p_B |
| rule A and filter (x = c/7 per batch) | 134,199,681 trials | 0.99987 +- 0.00009 of 2^-11 | 1.00070 | exp(-43.6) at 1.002 | **1.002 * 2^-11** | 1.002167 * 2^-11 |
| batch enters stage C (not in (ii)) | 132,565,944 batches | 0.0033756 per batch | | | | 0.0034250 per batch |
| rule A (trial; not in (ii)) | 8,590,086,370 | 1.00002 of 2^-5 | | | | |
| filter (trial; not in (ii)) | 4,294,895,028 | 0.99998 of 2^-6 | | | | |

**Decision.** All 40 runs were present (started 2026-10-07T21:30:03Z to
21:43:04Z, all ended with exit status 0 by 21:44:58Z; 1-minute load at most
6.4 at every start). The stage-B grid value 0.5765 fails the empirical
Bernstein test (0.576577 > 0.5765) and 0.5766 passes both tests (Lemma C'
exponent 66.8), so theta_B = 0.5766. For stage C, 1.001 passes the empirical
Bernstein test but its Lemma C' exponent is 12.3, and 1.002 passes both
(43.6), so theta_C = 1.002. No STOP condition occurred. The budgets are
0.5766 * 6001/6000 = 0.5766961 p_B and 1.002 * 6001/6000 = 1.002167 * 2^-11.
Per run (2^33 trials each) the stage-B share lies between 0.5764 and 0.5766
p_B and the rate of rule A with the filter between 0.9986 and 1.0006 of
2^-11; the largest c of one batch was 4. The 4,192,357 units in the last
group (about 1/9,363) hold two distinct trials each, as the run's last
groups do. The control (mode rand, 8 runs, 2^36.0 trials) is used only in
Section 8.1; with random D3.d1 the stage-B share of this order is 0.6320
p_B, rule A with the filter 1.00005 * 2^-11.

**Other orders and earlier samples (reported, not used).** The stage-B
share depends on which trials share a batch. In 21252124's order (seven
consecutive members of one context) it is 0.53912 +- 0.00022 p_B
(21252124's preregistered 2^36-trial sample; Subflatus3's per-batch sample
of that order in 1d5e54ce, 2^34 batches, 0.53929), and with random D3.d1
0.546 (098e66f4, 52bb50ee, 21252124's control). The order S2K has a higher
share (about 0.577 p_B) because its batches mix seven contexts, and a
cheaper stage A: per trial, stage A and stage B together cost 2.714 +
1.08356 here against 4.000 + 1.247 in 21252124 (Section 9).

**The pilot (exploratory, disclosed; not used for any premise).** Before
this version's program existed, the order was chosen with `rtpilot.c` (an
audit program with the formulas of `rtuni2.c`; SHA-256 6b5eaaf0...e4f41c,
then c9cedcf0...c31a after adding the stride-9,363 batching; SplitMix64
seeds 1, 2 and 3, streams SEED * 0x2545F4914F6CDD1D + 103; D3.d1 = X3). It
measured the stage-B share of four batchings of the same trial set:
21252124's order 0.5403 +- 0.0011 p_B (2^28 trials); a swapped order with
seven consecutive low halves of C2.a1 per batch 0.5850 +- 0.0012 (2^28);
the order of this version (seven consecutive high halves) 0.5729 +- 0.0031
(2^27.8) and 0.5773 +- 0.0015 (2^29.8); seven high halves with stride 9,363
1.0073 (2^29.8); and three tiny timing runs (2^22, 2^22 and 2^21.8 trials). The order S2K was
chosen after these runs, for its operation count and its share. The
premise rests only on the preregistered sample above, whose runs, seeds,
analysis and decision rule were fixed by its preregistration.

**Scope and limitations of H1.** The factor F = 92,675,072 is assumed; it
is half of the exact model count 185,350,144 (margin 2.000), which the
organizer experiments do not measure. M is untested at probability 2^-100.5
(the R = 0 rate 185,350,144 * 2^-128); it was compared with real trials on
events of probability down to about 2^-38 per trial here (E1 part, E3
partial events; and 2^-30 with D3.d1 = X3, Section 8.1) and down to about
2^-40 for one call by c66f230d; the full event is far below anything
measured. M fails inside one context (rule-A share varies by context); only
averages are measured. The constants, the class and rule A were chosen by
c66f230d to maximize a count of the same kind; S8 was chosen by us from the
exact per-member factors of all 524,288 class members. Recomputed for an
earlier version, S8 is the best of all 8,992,320 sub-classes of 2^16
members given by three independent conditions, each fixing one free bit of
e1 or the XOR of two (three of them describe S8 itself). The selection
matters: the full class with rule A and no sub-class already counts
144,123,339 over all 15 betas (1.555 F; betas outside T6 add under 32,000),
so S8 supplies a factor 1.29 of the margin 2.000: if S8's advantage under M
were entirely an artifact of this selection, S8 trials would have the class
rate, and the class count with rule A (1.555 F) is still at least F. The
filter was chosen to contain T6. A choice that is best under M says nothing
about M and may favour parameters where M overstates; the real-trial ratios
of 8.1 are the check we have; the order of enumeration (Section 2) and the
batching (Section 4) were not chosen with any count of good trials (the
batching changes which trials are examined together, not which are run).
37% of the S8 count (44% in the full class) comes from one beta, 18b0e098.
The trials of one outer step share its three coin words (outer steps have
independent coins; D3.d1 = X3 in all of them); trials of one context (outer
step and X2) differ only in Y4, and trials with the same outer step and
member share Y12 and w5, two of E1's inputs, over all 2^32 values of X2,
while E1's a1 varies with Y1 and Y6; for part (i) independence is assumed.
Part (ii) is a first-moment statement: its run averages are estimated
without bias from a uniform sample of 2^38 trials of this order (stage B at
0.57650 p_B against the asserted 0.5766 p_B, a margin of 1.00017; rule A
with the filter at 0.99987 * 2^-11 against 1.002 * 2^-11), and the run has
2^100.5; no independence is assumed for it, and the budgets follow from it
by Theorem 2. The sample's probabilities are over a seeded generator's
choices, the program is a participant program and all samples ran on the
participant side; the organizer experiments see the stage events only in
16,128 clustered lanes per run.

**Run selection.** No organizer-run count or frequency supports F, the
averages of H1 (ii) or the success probability. Every predicted observation
of Section 6 is an exact per-seed predicate, so no choice among runs can
make it pass; the rule-A, filter and stage-entry totals are reported for
information, every replay of the shipped program included (Section 6). No
parameter, version, seed or nonce was chosen on replay outcomes: S8, the
filter and F come from the model count, the stage tests from Lemma A and the
filter, D3.d1 = X3 from the operation count (21252124). The order S2K was
chosen after the exploratory pilot above and from the operation count; the
premises theta_B and theta_C were set by the preregistered decision rule
from the preregistered sample only, and nothing was changed after the
sample except the PREMISE line of the program (from the placeholder
(101/100, 5/4) to (2883/5000, 501/500)); the budget factor 6001/6000 is
5266c5ce's and was fixed in the program before the sample. All runs made for
this version: (a) the op audit that proposed the order (prototype programs
s8stage_v103a, _v103s and _v103k: a development self-test of 50, 40 and 40
cases and a 2,000-case self-test each, all lanes right; exhaustive checks of
Lemmas A2/F2 (3 * 2^20 cases each) and A3 (2^28 cases); five broken
prototype copies, all failing (one of them started twice: the first start
stopped with a module-not-found error before any test); the exact-ledger
script) and its pilot (above); (b) a per-batch sampler of 21252124's order
(`rtuni3.c`) that was written and checked but never used for a sample: five
context identities against 21252124's `rtuni2.c` (5 tiny rtuni2 runs), unit
cross-checks against 21252124's program (50 and 20,000 units, seed 5, D3.d1
= X3; 5,000 units, seed 6, random D3.d1), one 2^24-trial timing run (0.5411
p_B, 1.0172) and one test of its analysis script; (c) for this version
before the preregistration: on a draft of the program, a 200-case
development self-test with `--ledger` and the first runner development run
of Section 6 (rejected by the runner; outputs not kept); on the counted
program 3aef733e...e27518, the second runner development run (dev01, kept)
and the 2,000-case self-test; the `rtuni4` timing run `rtuni4 unit 2396745 1
fixed` (2^24 trials, 0.5772 p_B, 1.0052 * 2^-11), four cross-check runs of
`rtuni4` (`rtunicheck4.py` in two versions, first 6e14e03e...dfc2 without
the counted pieces, then the frozen one; each on 30,000 units seed 5 fixed
and 5,000 units seed 6 rand; all equal) and one test of `summarize4.py` on
the timing run's output; (d) the 40 runs of the preregistered sample; (e) on
the shipped program: `--ledger`, the stricter-reading ledgers, the
2,000-case self-test, the seven broken copies (and the seventh at 2,000
cases), `--count` (output identical to 21252124's except one removed
informational field) and the 41 preregistered replays of Section 6; and,
after the package was built, by two review agents, the 2,000-case self-test
and `--ledger` once each per agent (outputs identical), and once
`summarize4.py` on the stored run outputs (identical). No run was discarded
or selected, and none was repeated except the restarted broken prototype
copy in (a).

## 9. Charged time

Per outer step (vd, w5), 2^48 trials, fixed work:

    274 + 29 + (2^32 + 2^16) * 94 + 2^16 * (112 + 9,362 * 25 + 17 + 9,363 * (256 * 4 + 2^16 * 19))
      = 765,109,217,591,599 operations

(the outer step with its random word; the table entry and 2^32 + 2^16
table words; per member the member step, 9,362 groups with set-up, block
test and end (14 + 4 + 7) and the last group (12 + 4 + 1), and in every
group 256 block updates and stage A of 2^16 batches). Every group body is
straight-line code: the 2^16 positions are unrolled (each position reads its
own table words at its own offsets from the group's pointer), and stages B
and C are out of line and duplicated for each position, each copy's last
instruction jumping to the next position, so an entry costs exactly the 66
and 119 operations of Section 5 and no loop operation is executed inside a
group. The group body takes under 2^16 * 210 instructions (well inside the
code bound of Section 10); all groups and members run the same body (only
the pointer, the registers and, in the last group, B32 differ). Stages B
and C are charged at their budgets, whatever the coins: E_B * 66 and
E_C * 119 operations for the run (a group starts only if 2^16 entries are
left, so no entry beyond the budget is executed).

- Fixed work: 765,109,217,591,599 * V * 2^32 = 2.71821 * N operations
  (stage A 2.71449, block updates 0.00223, table 0.00143, groups, members and
  outer steps 5.5 * 10^-5 per trial).
- Stage B: E_B * 66 = 1.08356 * N (0.5766 * 6001/6000 * p_B * 9,363 / 65,536 * 66).
- Stage C: E_C * 119 = 0.05823 * N (1.002 * 6001/6000 * 2^-11 * 119).
- Per value of vd: next value, end test and loop entry, under 2^6.
- The member list (65,536 words), the block constants (512 words), D0,
  DLAST, B32_01 and the two budget registers: under 2^22 operations once.
- Step 3: at most once: the 2^16 batches of one group recomputed with all
  stages (204 operations each) and their lanes scanned, under 2^25
  operations, and 2 compressions.
- Preprocessing: 2^86 units, declared below.

    T = (765,109,217,591,599 * V * 2^32 + 66 E_B + 119 E_C + 2^6 V + 2^22 + 2^25) / 430 + 2 + 2^86
      = 2^93.735734 (3.860004 operations per trial: 2^93.7289 without the
                2^86 + 2 units, which add 0.0068)

time_log2 = 93.735734, claimed **93.7358** (rounded up at the fourth
decimal). `python3 experiments/s8stage.py --ledger` computes T in exact
rational arithmetic. The claim holds for any total up to 3.86018 operations
per trial. Under stricter readings: the budget registers kept in memory
(load, subtract, store: 2 more operations per entry) give 2^93.7483; a loop
over the 256 positions of a block (pointer add, compare, branch: 3
operations per batch) instead of the unrolled group body gives
2^93.8870. For comparison, 21252124 (the same trials in its order,
stages of 28, 73 and 112 operations) gives 2^94.198131.

**Preprocessing (declared charge).** The program stores the six constants
of Fact P, eta, the rule-A words, the filter words, the stage-test words,
the block constants and the S8 conditions. The constants were found by
c66f230d with solver searches and chosen with model counts; rule A, S8 and
the filter were chosen with counts of the same kind (S8 by us from the
exact per-member factors of all 524,288 class members, best of 8,992,320
candidate sub-classes); the order of the construction and the staged batch
were found by 60f94c5c, the loop order S2K by us (with the pilot of Section
8.2), and the premise and budget conventions by 52bb50ee and 5266c5ce. We
do not reconstruct this work from run records. We charge a declared upper
bound of 2^86 units (2^94.75 word operations) for all of it, ours,
c66f230d's, 60f94c5c's, 52bb50ee's and 5266c5ce's, including every count
and measurement of Section 8 (the samples of Section 8.2 included). It is
more than 2^34 times c66f230d's own estimate of their
selection (below 2^60 operations, from running times on one desktop machine
and one graphics card), and more than 2^3.5 times ten years at 2^63
operations per second (over four times the peak rate of the fastest listed
supercomputer, about 2^61.3 FP64 operations per second), so it exceeds any
computation physically performed for this selection before the submission
date. This is a declared upper-bound charge, not a premise: H1 does not
depend on it, and no part of the success bound uses it. The charge moves
the scalar by 0.0068. The stored values themselves need no search to
check: Fact P, Lemma Q, Lemma B, Lemma A3's constants and the stage-test
words are finite computations repeated by the self-test and the
experiments.

## 10. Memory and advice

Search memory: the X2 table of an outer step, (2^32 + 2^16) * 8 * 32 bytes
(under 2^41 bytes); code below 2^28 bytes (the unrolled group body with its
2^16 out-of-line copies of stages B and C); the member list, block
constants, constants, the stored words of step O, budget registers and
temporaries below 2^20 bytes: below 2^42 bytes in all. For the
preprocessing we use no reported peak: every byte it stores is written by
one of its charged word operations, so it stored at most 32 * 2^94.75 =
2^99.75 bytes; memory_log2_bytes = 100 is this bound and covers the search
(the cost model gives memory no scalar contribution). Advice: the six
constants, eta, the rule-A, stage-test and filter words, the block-constant
rule and the S8 conditions, below 64 bytes (nonuniform_advice_log2_bytes =
6). preprocessing_log2 = 86 as charged above.

## Appendix A. The measuring programs of Section 8.2

These are the preregistered files (SHA-256: rtuni4.c 4bbd2090...b8263,
rtunicheck4.py 75d45d2d...f2a7, summarize4.py 9dd193a4...aaa23; the binary
fdb899c5...db76, the seed rule make_seeds4.py d3b5ae59...d520 and the
launcher run_holdout4.sh 3feebe35...b218 are listed in the frozen
preregistration, SHA-256 e2247e2b...1f4d). `rtuni4.c` is compiled with `cc -O3
-march=native` and run as `./rtuni4 unit 1227227136 SEED fixed` (32 seeds)
and `./rtuni4 unit 1227227136 SEED rand` (8 seeds). It computes the trials
forwards with the lines of steps O, M, Y and T, the member list of S8 and
the batches of the order S2K, and tests rule A on h1 of E3 and the filter
on c1 of E1 of message A, exactly as the counted program's forward
computation does (checked by `rtunicheck4.py`, which also runs every tenth
unit through the counted pieces; it imported the counted program
3aef733e...e27518, the shipped program before its PREMISE line was set,
which differs from the shipped program only in that line, although its
docstring below says 'the shipped program'). Its per-trial formulas are
those of 21252124's `rtuni2.c` and v101's `rt2l.c`.

```c
/* rtuni4.c -- uniform per-batch sample of the H1 (ii) stage events of v103 in the order S2K (D3.d1 = X3, X14 = 0),
   with E1 and E3 partial events for H1 (i).  Per-trial formulas are those of rtuni3.c / rtuni2.c (v102: steps O, M, Y,
   T of 60f94c5c, C2, C1, E1, rule A on h1 of E3, the filter on c1 of E1) and rt2l.c (v101: E3 events G and D16).

   Unit = one batch of the run, drawn uniformly: fresh coins C0.c1, D3.d1 (used only in MODE rand), S15, S9, then w5,
   vd uniform below V = 1,512,538, member m < 2^16, group g < 9,363, position i < 2^16 -- nine SplitMix64 draws, in
   this order.  Lane l (l < 7; in the last group g = 9,362 only l < 2, the distinct trials) is the trial with
   X2 = ((7g + l) 2^16 + i - X6_m - w7) mod 2^32, i.e. C2.a1 = (7g + l) 2^16 + i.  Units are i.i.d.;
   b = 1{some lane satisfies rule A} (the batch enters stage B), c = number of lanes with rule A and the filter (0..7).
   Events per trial: A rule A, F filter, AF both, T6 beta in T6, T6A, N12 (low 12 bits of the Lemma N word zero),
   T6N8 (beta in T6 and low 8 bits of n zero), G (E3: g1 ^ g1' = ROL(psi,12), psi = tau ^ ROR(tau,1), tau = 285020a0),
   D16 (low 16 bits of the digest differences D1 and D3 zero).

   usage: rtuni4 unit NUNITS SEED MODE   -> one JSON line of sums          (MODE fixed | rand)
          rtuni4 dump NUNITS SEED MODE   -> one line per unit (for rtunicheck4.py)
   SEED is decimal; the stream starts at SEED * 0x1234567 + 77 (mod 2^64), as in rtuni2 and rtuni3.                */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef uint32_t u32; typedef uint64_t u64;
static inline u32 ror(u32 x,int r){ return (x>>r)|(x<<(32-r)); }
static inline u32 rol(u32 x,int r){ return (x<<r)|(x>>(32-r)); }
static const u32 IV[8]={0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
static const u32 X3=0x29d4fa98,X7=0xbee3af28,X11=0x44036000,X15=0x40c58500,W4=0x97475638,W13=0x0007c006;
static const u32 Y3=0x8127c181,Y3P=0x7edf3e7e,Y11=0x7af77f38,Y11P=0x850000c3,ETA=0x830303cf;
static const u32 T6[6]={0x18b0e098,0x18b1a098,0x18d0e098,0x18d1a098,0x18b3e098,0x18d3e098};
static inline int inT6(u32 b){ for(int i=0;i<6;i++) if(b==T6[i]) return 1; return 0; }
static u64 sm; static inline u64 rnd(void){ u64 z=(sm+=0x9E3779B97F4A7C15ULL); z=(z^(z>>30))*0xBF58476D1CE4E5B9ULL; z=(z^(z>>27))*0x94D049BB133111EBULL; return z^(z>>31); }
static u32 S8[65536];
static void members(void){
  int ord[16]={14,30,31,4,5,6,7,10,11,12,13,20,21,27,28,29};
  for(u32 i=0;i<65536;i++){ u32 e1=0x030c0303|0xc; for(int t=0;t<16;t++) if(i>>t&1) e1|=1u<<ord[t]; if(e1>>21&1) e1|=1u<<26; S8[i]=e1-Y3; }
}
static inline int ruleA(u32 h){ return !(h&1) && !((h>>16)&1) && !((h>>17)&1) && ((h>>1)&1) && (((h>>2)^(h>>3))&1); }
#define G1(a,d,c,b,x,y) do{ a=a+b+x; d=ror(d^a,16); c=c+d; b=ror(b^c,12); a=a+b+y; d=ror(d^a,8); c=c+d; b=ror(b^c,7);}while(0)
static u32 K2A,K2B,K2C,K2D,DELTA,PSI_R;
typedef struct { u32 c0c,c0d,s15,w5,S2,S6,S10,S11,S7,S4,X4,X9,X13,X14,w6,w7,Cb,D2b,D2c,s9; } Outer;
typedef struct { u32 X2,w0,w2,w3,w12,S0,S1,S5,S12; } Ctx;
typedef struct { u32 y,Y12,ca,X6,dd,X1; } Mem;
typedef struct { u64 A,F,AF,T6,T6A,N12,T6N8,G,D16,nt; } Cnt;
static inline void outer_draw(Outer*o,int fixed){   /* rtuni2's per-outer-step draws and words, same order */
  u32 c0c=(u32)rnd(), d3r=(u32)rnd(), s15=(u32)rnd(), s9=(u32)rnd();
  u32 d3d=fixed?X3:d3r;
  u32 w5=(u32)rnd(), c0d=(u32)(rnd()%1512538ULL);
  u32 S2=K2A+K2B+w5, S14=ror(K2D^S2,8), S10=K2C+S14, S6=ror(K2B^S10,7);
  u32 d3a=rol(d3d,16)^S14, d3c=s9+d3d, d3b=X3-d3a, S4=rol(d3b,12)^d3c, S3=d3a-S4, X14=ror(d3d^X3,8), X9=d3c+X14, X4=ror(d3b^X9,7);
  u32 k3d=rol(s15,8)^S3, k3c=IV[3]+k3d, k3b=ror(IV[7]^k3c,12), S11=k3c+s15, S7=ror(k3b^S11,7), k3a=rol(k3d,16)^11;
  u32 w6=k3a-IV[3]-IV[7], w7=S3-k3a-k3b, X8=c0c-c0d, Cb=ror(X4^c0c,12), D2b=rol(X7,7)^X8, D2c=rol(D2b,12)^S7, X13=X8-D2c;
  o->c0c=c0c; o->c0d=c0d; o->s15=s15; o->w5=w5; o->S2=S2; o->S6=S6; o->S10=S10; o->S11=S11; o->S7=S7; o->S4=S4; o->X4=X4;
  o->X9=X9; o->X13=X13; o->X14=X14; o->w6=w6; o->w7=w7; o->Cb=Cb; o->D2b=D2b; o->D2c=D2c; o->s9=s9;
}
static inline void ctx_of(const Outer*o,u32 X2,Ctx*x){   /* step M for one X2 (rtuni2's per-X2 words, and S0) */
  u32 d2a=X2-o->D2b-W13, d2d=rol(o->X13,8)^X2, S13=rol(d2d,16)^d2a, S8v=o->D2c-d2d, w12=d2a-o->S2-o->S7;
  u32 k1c=o->s9-S13, k1d=k1c-IV[1], k1a=rol(k1d,16), k1b=ror(IV[5]^k1c,12), S1=rol(S13,8)^k1d, S5=ror(k1b^o->s9,7);
  u32 w2=k1a-IV[1]-IV[5], w3=S1-k1a-k1b;
  u32 k0b=rol(o->S4,7)^S8v, k0c=rol(k0b,12)^IV[4], k0d=k0c-IV[0], k0a=rol(k0d,16), S12=S8v-k0c, w0=k0a-IV[0]-IV[4];
  u32 S0=rol(S12,8)^k0d;
  x->X2=X2; x->w0=w0; x->w2=w2; x->w3=w3; x->w12=w12; x->S0=S0; x->S1=S1; x->S5=S5; x->S12=S12;
}
static inline void mem_of(const Outer*o,u32 m,Mem*v){    /* step Y for member m (rtuni2's table row) */
  u32 y=S8[m], Y8=rol(y,7)^o->Cb, Y12=Y8-o->c0c, Y0=rol(Y12,8)^o->c0d, ca=Y0-o->Cb-o->w6, X12=rol(o->c0d,16)^ca;
  u32 dc=X11-X12, db=ror(o->S6^dc,12), X6=ror(db^X11,7), dd=dc-o->S11, X1=rol(X12,8)^dd;
  v->y=y; v->Y12=Y12; v->ca=ca; v->X6=X6; v->dd=dd; v->X1=X1;
}
/* one trial: rtuni2's inner-loop body, then E1 and E3 of both messages as rt2l.c; returns 1 for rule A, 2 for the filter */
static inline int trial(const Outer*o,const Ctx*x,const Mem*v,Cnt*c){
  u32 X0=v->ca-o->X4-x->w2, fd=rol(X15,8)^X0, fc=o->S10+fd, X10=fc+X15, fb=ror(x->S5^fc,12), X5=ror(fb^X10,7);
  u32 ga=rol(v->dd,16)^x->S12, w10=ga-x->S1-o->S6, w8=(rol(fd,16)^o->s15)-x->S0-x->S5;
  u32 a2=x->X2,b2=v->X6,c2=X10,d2=o->X14; G1(a2,d2,c2,b2,o->w7,x->w0); u32 Y6=b2,Y14=d2;
  u32 e1=Y3+v->y, h1=ror(Y14^e1,16); int A=ruleA(h1);
  u32 a=v->X1,b=X5,cc=o->X9,d=o->X13; G1(a,d,cc,b,x->w3,w10); u32 Y1=a,Y9=cc;
  u32 ea1=Y1+Y6+x->w12, ed1=ror(v->Y12^ea1,16), ec1=Y11+ed1; int F=((ec1&0x00098188)==0x00008000);
  u32 ec1p=Y11P+ed1, eb1=ror(Y6^ec1,12), eb1p=ror(Y6^ec1p,12), ea2=ea1+eb1+o->w5, ea2p=ea1+eb1p+o->w5+DELTA;
  u32 ec2=ec1+ror(ed1^ea2,8), ec2p=ec1p+ror(ed1^ea2p,8), beta=eb1^eb1p, eps=ec2^ec2p, n=eps^rol(beta^eps,1)^ETA;
  u32 e1p=Y3P+v->y, h1p=h1^ETA, g1=Y9+h1, g1p=Y9+h1p, f1=ror(v->y^g1,12), f1p=ror(v->y^g1p,12);
  u32 e2=e1+f1+w8, e2p=e1p+f1p+w8, h2=ror(h1^e2,8), h2p=ror(h1p^e2p,8), g2=g1+h2, g2p=g1p+h2p;
  u32 D1=(ea2^ea2p)^(g2^g2p), D3=(e2^e2p)^eps;
  int t6=inT6(beta); c->T6+=t6; c->T6A+=t6&A; c->N12+=((n&0xfff)==0); c->T6N8+=t6&((n&0xff)==0);
  c->G+=((g1^g1p)==PSI_R); c->D16+=((D1&0xffff)==0)&&((D3&0xffff)==0);
  c->A+=A; c->F+=F; c->AF+=A&F; c->nt++;
  return A|(F<<1);
}
int main(int argc,char**argv){
  if(argc<5){ fprintf(stderr,"usage: rtuni4 unit|dump NUNITS SEED MODE\n"); return 1; }
  int dump=!strcmp(argv[1],"dump"), unit=!strcmp(argv[1],"unit");
  if(!(dump||unit)){ fprintf(stderr,"usage\n"); return 1; }
  const char*seeds=argv[3], *mode=argv[4];
  if(strcmp(mode,"fixed") && strcmp(mode,"rand")){ fprintf(stderr,"mode\n"); return 1; }
  int fixed=!strcmp(mode,"fixed");
  sm=strtoull(seeds,0,10)*0x1234567ULL+77;
  members();
  u32 K=IV[2]+IV[6]; DELTA=W4-(((K+W4)^8)-K); K2A=K+W4; K2D=ror(K2A^55,16); K2C=IV[2]+K2D; K2B=ror(IV[6]^K2C,12);
  { u32 tau=0x285020a0, psi=tau^ror(tau,1); PSI_R=rol(psi,12); }
  Cnt c; memset(&c,0,sizeof c); Outer o; Ctx x; Mem v;
  long NU=atol(argv[2]); u64 SB=0,SC=0,C1=0,C2=0,cmax=0,last=0;
  for(long u=0;u<NU;u++){
    outer_draw(&o,fixed);
    u32 m=(u32)(rnd()&0xffff), g=(u32)(rnd()%9363ULL), i=(u32)(rnd()&0xffff);
    mem_of(&o,m,&v);
    u32 cK=v.X6+o.w7; int nl=(g==9362)?2:7; int aA=0; u64 k=0; Cnt c0=c;
    for(int l=0;l<nl;l++){
      u32 X2=((7*g+(u32)l)<<16)+i-cK;
      ctx_of(&o,X2,&x);
      int r=trial(&o,&x,&v,&c); aA|=r&1; k+=(r==3);
    }
    SB+=aA; SC+=(k>0); C1+=k; C2+=k*k; if(k>cmax) cmax=k; last+=(g==9362);
    if(dump) printf("%u %u %u %u %u %u %d %llu %llu %llu %llu %llu %llu %llu %llu %llu\n",o.c0c,o.c0d,o.w5,m,g,i,aA,(unsigned long long)k,
                    (unsigned long long)(c.A-c0.A),(unsigned long long)(c.F-c0.F),(unsigned long long)(c.T6-c0.T6),(unsigned long long)(c.T6A-c0.T6A),
                    (unsigned long long)(c.N12-c0.N12),(unsigned long long)(c.T6N8-c0.T6N8),(unsigned long long)(c.G-c0.G),(unsigned long long)(c.D16-c0.D16));
  }
  if(!dump)
    printf("{\"units\":%ld,\"seed\":%s,\"mode\":\"%s\",\"trials\":%llu,\"SB\":%llu,\"SC\":%llu,\"C1\":%llu,\"C2\":%llu,\"cmax\":%llu,\"lastgroup\":%llu,"
           "\"A\":%llu,\"F\":%llu,\"AF\":%llu,\"T6\":%llu,\"T6A\":%llu,\"N12\":%llu,\"T6N8\":%llu,\"G\":%llu,\"D16\":%llu}\n",NU,seeds,mode,
           (unsigned long long)c.nt,(unsigned long long)SB,(unsigned long long)SC,(unsigned long long)C1,(unsigned long long)C2,
           (unsigned long long)cmax,(unsigned long long)last,(unsigned long long)c.A,(unsigned long long)c.F,(unsigned long long)c.AF,
           (unsigned long long)c.T6,(unsigned long long)c.T6A,(unsigned long long)c.N12,(unsigned long long)c.T6N8,
           (unsigned long long)c.G,(unsigned long long)c.D16);
  return 0;
}
```

```python
"""Cross-check of rtuni4 (unit and dump modes) against the shipped program's forward computation of real messages.
Draws NUNITS units exactly as rtuni4 draws them (SplitMix64 from SEED * 0x1234567 + 77: C0.c1, D3.d1, S15, S9, w5,
vd mod V, m = low 16 bits, g mod 9,363, i = low 16 bits), builds the batch's distinct trials in the order S2K
(X2 = ((7g + l) 2^16 + i - X6_m - w7) mod 2^32), computes both messages and their 2-round compressions with
s8stage.trial_words / s8stage.trace, and compares, unit by unit, the drawn words, the stage-B flag, c and the per-unit
counts of A, F, T6, T6A, N12, T6N8, G and D16 with `rtuni4 dump NUNITS SEED MODE`; in mode fixed, every tenth unit is
also run through the counted program (s8stage.Case: outer step, member step, group set-up, block update, the three
stages of the batch at position i) and its two stage decisions are compared with (b, c > 0).
usage: python3 rtunicheck4.py NUNITS SEED MODE DIR_OF_s8stage.py"""
import sys, json, subprocess
sys.path.insert(0, sys.argv[4])
import s8stage as s
M = (1 << 64) - 1; M32 = 0xffffffff
class SM:
    def __init__(self, seed): self.s = (seed * 0x1234567 + 77) & M
    def __call__(self):
        self.s = (self.s + 0x9E3779B97F4A7C15) & M; z = self.s
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & M; z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & M; return (z ^ (z >> 31)) & M
nu, seed, mode = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
tau = 0x285020a0; PSI_R = s.rol(tau ^ s.ror(tau, 1), 12)
r = SM(seed)
lines = subprocess.run(['./rtuni4', 'dump', str(nu), str(seed), mode], capture_output=True, text=True).stdout.split('\n')
bad = 0; tot = dict(units=0, SB=0, C1=0, A=0, AF=0, G=0, lastgroup=0); prog_n = prog_bad = 0
for u in range(nu):
    c0c, d3r, s15, s9 = [r() & M32 for _ in range(4)]
    w5 = r() & M32; vd = r() % 1512538; m = r() & 0xffff; g = r() % s.NBATCH; i = r() & 0xffff
    d3d = s.X3 if mode == 'fixed' else d3r
    o = s.outer([c0c, vd, d3d, s15, s9, w5]); y = s.member(m)
    c = (s.member_vals(o, y)['X6'] + o['w7']) & M32
    ev = dict(A=0, F=0, T6=0, T6A=0, N12=0, T6N8=0, G=0, D16=0); anyA = 0; k = 0
    for l in range(2 if g == s.NBATCH - 1 else 7):
        X2 = (((7 * g + l) << 16) + i - c) & M32
        v = s.middle(o, X2)
        A_, B_, w, wp = s.trial_words(v, y); ta, tb = s.trace(w, 55), s.trace(wp, 63)
        h1 = ta[(1, 'E3')][1]; a = int(s.ruleA_h1(h1)); E1a, E1b = ta[(1, 'E1')], tb[(1, 'E1')]
        f = int((E1a[2] & s.MF) == s.VF); beta = E1a[3] ^ E1b[3]; eps = E1a[6] ^ E1b[6]; n = eps ^ s.rol(beta ^ eps, 1) ^ s.ETA
        t6 = int(beta in s.T6); D1 = ta['digest'][1] ^ tb['digest'][1]; D3 = ta['digest'][3] ^ tb['digest'][3]
        ev['A'] += a; ev['F'] += f; ev['T6'] += t6; ev['T6A'] += t6 & a; ev['N12'] += (n & 0xfff) == 0
        ev['T6N8'] += t6 & ((n & 0xff) == 0); ev['G'] += (ta[(1, 'E3')][2] ^ tb[(1, 'E3')][2]) == PSI_R
        ev['D16'] += (D1 & 0xffff) == 0 and (D3 & 0xffff) == 0
        anyA |= a; k += a & f
    exp = [c0c, vd, w5, m, g, i, anyA, k] + [int(ev[e]) for e in ('A', 'F', 'T6', 'T6A', 'N12', 'T6N8', 'G', 'D16')]
    got = [int(t) for t in lines[u].split()]
    if got != exp: bad += 1
    if mode == 'fixed' and u % 10 == 0:
        cs = s.Case([c0c, vd, s.X3, s15, s9, w5, 0], m, g); out = cs.batch(i, True)[3]
        prog_n += 1; prog_bad += not (cs.ok and out['decA'] == bool(anyA) and out['decB'] == (k > 0))
    tot['units'] += 1; tot['SB'] += anyA; tot['C1'] += k; tot['A'] += ev['A']; tot['AF'] += k; tot['G'] += ev['G']
    tot['lastgroup'] += g == s.NBATCH - 1
summ = json.loads(subprocess.run(['./rtuni4', 'unit', str(nu), str(seed), mode], capture_output=True, text=True).stdout)
sum_ok = all(summ[k] == tot[k] for k in ('SB', 'C1', 'A', 'AF', 'G', 'lastgroup')) and summ['units'] == nu
print(json.dumps({'nunits': nu, 'seed': seed, 'mode': mode, 'totals': tot, 'mismatches': bad, 'unit_mode_sums_equal': sum_ok,
                  'program_units': prog_n, 'program_mismatches': prog_bad, 'equal': bad == 0 and sum_ok and prog_bad == 0}))
```

```python
"""Analysis of the v103 S2K sample (fixed before the runs).  usage: python3 summarize4.py RUNDIR SEEDS4.txt
Run files RUNDIR/NN.json, one line of `rtuni4 unit U SEED MODE` each (NN = hKK fixed, cKK control).
Unit k = one uniform batch of the run in the order S2K: b_k = 1{batch enters stage B} in {0,1}; x_k = c_k / 7 in [0,1],
c_k = trials of the batch with rule A and the filter (at most 7 distinct trials).  Units are i.i.d.; E b_k = run
stage-B share, E x_k = KAP * (run per-trial rate of rule A and filter), KAP = 65,536 / 65,541 exactly.
Bounds, delta = 2^-64: empirical Bernstein (Maurer and Pontil 2009, Thm 4)
  E <= mean + sqrt(2 Vn ln(2/delta) / n) + 7 ln(2/delta) / (3 (n - 1)),  Vn = unbiased sample variance;
Lemma C' (lower-tail Chernoff, [0,1] variables): P(sum <= S) <= exp(-(n theta' - S)^2 / (2 n theta')) for n theta' > S.
Decision (fixed runs only; all runs present, else STOP):
  stage B: premise theta_B = smallest k/10000, 5500 <= k <= 10100, with EB_B <= theta_B p_B and the Lemma C' exponent
  at theta' = theta_B p_B >= 20.  If none passes: STOP (no stage-B premise ships for the order S2K).
  stage C: premise theta_C = smallest k/1000, 1001 <= k <= 1249, with EB_x <= theta_C KAP 2^-11 and the Lemma C'
  exponent at theta' = theta_C KAP 2^-11 >= 20.  If none passes: 5/4 (v102's premise; the trial set is the same).
  Budgets: premise * 6001/6000 each.  Both tests are monotone in theta, so the smallest passing grid value keeps the
  error probabilities at 2^-64 (EB) and e^-20 (Lemma C') with no multiplicity cost.
Also reported (H1 (i), not part of the decision): pooled rates of the per-trial events in mode fixed and mode rand
(control) and their ratio with a Poisson standard error."""
import json, glob, math, sys, os
from fractions import Fraction as Fr
rundir, seedsf = sys.argv[1], sys.argv[2]
pB = Fr(32052445611625, 160855115169792); KAP = Fr(65536, 65541)
L = 65 * math.log(2)
seeds = {}
for line in open(seedsf):
    if line.strip() and not line.startswith('#'):
        nn, sd, mode = line.split(); seeds[nn] = (sd, mode)
R = {'fixed': [], 'rand': []}
for nn, (sd, mode) in sorted(seeds.items()):
    f = os.path.join(rundir, nn + '.json')
    if os.path.exists(f):
        r = json.load(open(f)); assert r['mode'] == mode and str(r['seed']) == sd, f; R[mode].append(r)
F = R['fixed']
n = sum(r['units'] for r in F); t = sum(r['trials'] for r in F)
SB = sum(r['SB'] for r in F); C1 = sum(r['C1'] for r in F); C2 = sum(r['C2'] for r in F); SC = sum(r['SC'] for r in F)
def eb(S1, S2, n):
    m = S1 / n; v = (S2 - n * m * m) / (n - 1)
    return m, v, m + math.sqrt(2 * v * L / n) + 7 * L / (3 * (n - 1))
def chern(S, n, th):
    mu = n * th
    return (mu - S) ** 2 / (2 * mu) if S < mu else 0.0
pBf = float(pB); kf = float(KAP)
mB, vB, ebB = eb(SB, SB, n); mX, vX, ebX = eb(C1 / 7, C2 / 49, n)
nf = sum(1 for v in seeds.values() if v[1] == 'fixed')
complete = len(F) == nf and len(R['rand']) == len(seeds) - nf
out = {'runs_fixed': len(F), 'runs_rand': len(R['rand']), 'complete': complete, 'units': n, 'trials': t,
       'trials_log2': round(math.log2(t), 4),
       'stageB': {'SB': SB, 'mean_over_pB': round(mB / pBf, 6), 'se_over_pB': round(math.sqrt(vB / n) / pBf, 7),
                  'emp_bernstein_2^-64_over_pB': round(ebB / pBf, 6),
                  'per_run_over_pB': [round(r['SB'] / r['units'] / pBf, 5) for r in F]},
       'stageC': {'C1': C1, 'C2': C2, 'SC': SC, 'rate_over_2^-11': round(C1 / t * 2048, 6),
                  'unit_mean_over_KAP_2^-11': round(mX / kf * 2048, 6), 'se': round(math.sqrt(vX / n) / kf * 2048, 7),
                  'emp_bernstein_2^-64_over_2^-11': round(ebX / kf * 2048, 6),
                  'per_run_over_2^-11': [round(r['C1'] / r['trials'] * 2048, 4) for r in F]}}
EV = ('A', 'F', 'AF', 'T6', 'T6A', 'N12', 'T6N8', 'G', 'D16')
ext = {}
for mode in ('fixed', 'rand'):
    tt = sum(r['trials'] for r in R[mode]); ext[mode] = {'trials': tt, **{e: sum(r[e] for r in R[mode]) for e in EV}}
for e in EV:
    a, ta, b, tb = ext['fixed'][e], ext['fixed']['trials'], ext['rand'][e], ext['rand']['trials']
    if a and b and ta and tb:
        ratio = (a / ta) / (b / tb)
        ext[e + '_fixed_log2'] = round(math.log2(a / ta), 4); ext[e + '_rand_log2'] = round(math.log2(b / tb), 4)
        ext[e + '_ratio'] = [round(ratio, 4), round(ratio * math.sqrt(1 / a + 1 / b), 4)]
out['h1i_events'] = ext
thB = None
for k in range(5500, 10101):
    th = k / 10000
    if ebB <= th * pBf and chern(SB, n, th * pBf) >= 20: thB = Fr(k, 10000); break
thC = None
for k in range(1001, 1250):
    th = k / 1000
    if ebX <= th * kf / 2048 and chern(C1 / 7, n, th * kf / 2048) >= 20: thC = Fr(k, 1000); break
stop = (not complete) or thB is None
tC = thC if thC else Fr(5, 4)
out['decision'] = {'STOP': stop, 'stageB_premise': str(thB) if thB else None,
                   'stageB_budget': str(thB * Fr(6001, 6000)) if thB else None,
                   'stageB_chern_exp_at_premise': round(chern(SB, n, float(thB) * pBf), 2) if thB else None,
                   'stageC_premise': str(tC), 'stageC_from_sample': thC is not None, 'stageC_budget': str(tC * Fr(6001, 6000)),
                   'stageC_chern_exp_at_premise': round(chern(C1 / 7, n, float(tC) * kf / 2048), 2),
                   'program_line': 'PREMISE = (Fraction(%d, %d), Fraction(%d, %d))' % (
                       (thB or Fr(0)).numerator, (thB or Fr(1)).denominator, tC.numerator, tC.denominator)}
print(json.dumps(out, indent=1))
```
