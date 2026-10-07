# A branch-free sub-class search on the 55/63-byte half-collision of 2-round BLAKE3

The scalar below is `time_log2` under `collision-frontier-v5` (C = 430).

**Credits.** This package is built on submission c66f230d by Jbenisek
(co-author tekkac): the 55/63-byte length cancellation, the six pinned
constants, steps S1, T, S2, S3 and Lemmas L, H, S, F, Y, the class of Y4
(eta = 830303cf), rule A and Lemma N are theirs, restated here so that the
package is self-contained. The seven 36-bit lanes and the masked rotation
are from ticket 2bf40fb (tekkac). The complement propagation
(~gd = ~gc + S11) follows submission 8c81a219 (Th0rgal). Jbenisek, tekkac
and Th0rgal are co-authors of this submission. New here: the sub-class S8
of 65,536 members, the member order, the beta filter and Lemma B, the
single-rotation X6 identity, Lemma D and the branch-free 64-register batch
that computes the whole 128-bit residual of every trial in 224 operations
per seven trials, and an independent exact count of the model rate split
by member and by rule.

**Change from our previous version.** The previous version examined a
trial in full only after rule A, the beta filter and the word n of Lemma N
had passed, and capped the stages and the confirmations by budgets whose
sufficiency was assumed (two supporting heuristics). Here every trial is
computed to its full residual and tested, so there are no stages, no
budgets and no supporting heuristic: the time bound holds for every value
of the coins, and the only premise is H1, with the same statement and the
same trials. The constant selection is charged by a declared bound
instead of a predecessor's records (Section 9).

**Exact part.** For every choice of eight 32-bit words the construction gives
a 55-byte message A and a 63-byte message B whose complete 2-round digests
agree on digest words 0, 2, 5 and 7 (Theorem 1). One of the eight words is
the round-1 state word Y4; the search keeps Y4 in S8.

**Heuristic part.** The search runs N = V * 2^80 such pairs (V = 1,589,345,
N = 2^100.60), computes the remaining 128-bit residual R of each exactly
(Lemma D) and tests it against zero; there is no table, sort or lookup and
no other data-dependent branch. A trial is charged 32.07 operations (32.0600
counted). H1 assumes a trial is *good* (R = 0, rule A, beta filter) with
probability at least 2^26.4 * 2^-128. Under the seven-word model the exact
count of good trials is at least 185,350,144 * 2^-128, which is 2.093 times
2^26.4 (Section 8); `python3 experiments/s8search.py --count` recomputes
this integer. Total charged time is 2^96.8581, claimed 96.86. With the
uniform rate instead, the same search needs 2^127 trials and gives 123.25.
No full collision is exhibited.
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

## 2. The half-collision (c66f230d)

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

**Step S1 (context: vc, vd, S11, S4, X13, X14, w0).** Every line is one
assignment of the named call solved for its left side (Fact 1).

    K0:  ka = IV0 + IV4 + w0; kd = ROR(ka,16); kc = IV0 + kd; kb = ROR(IV4 ^ kc,12)
         S8 = ROL(S4,7) ^ kb; S12 = S8 - kc; S0 = ROL(S12,8) ^ kd; w1 = S0 - ka - kb
    D2:  X8 = vc - vd; tc = X8 - X13; td = tc - S8; tb = ROL(X7,7) ^ X8
         S7 = ROL(tb,12) ^ tc; X2 = ROL(X13,8) ^ td; ta = X2 - tb - W13; S13 = ROL(td,16) ^ ta
    K3:  mb = ROL(S7,7) ^ S11; mc = ROL(mb,12) ^ IV7; md = mc - IV3
         S15 = S11 - mc; S3 = ROL(S15,8) ^ md; ma = ROL(md,16) ^ 11
         w6 = ma - IV3 - IV7; w7 = S3 - ma - mb
    K2:  p = K + W4; q = ROR(p ^ 55,16); r = IV2 + q; u = ROR(IV6 ^ r,12)
    D3:  ea = S3 + S4; eb = X3 - ea; ec = ROL(eb,12) ^ S4                 (w14 = w15 = 0)
         ed = ROL(X14,8) ^ X3; S9 = ec - ed; S14 = ROL(ed,16) ^ ea; X9 = ec + X14; X4 = ROR(eb ^ X9,7)
    K2:  S10 = r + S14; S6 = ROR(u ^ S10,7); S2 = ROL(S14,8) ^ q; w5 = S2 - p - u
    D2:  w12 = ta - S2 - S7
    K1:  nc = S9 - S13; nd = nc - IV1; na = ROL(nd,16); nb = ROR(IV5 ^ nc,12)
         S1 = ROL(S13,8) ^ nd; S5 = ROR(nb ^ S9,7); w2 = na - IV1 - IV5; w3 = S1 - na - nb
    C0:  vb = ROR(X4 ^ vc,12)

**Step T (member y = Y4).**

    C0:  Y8 = ROL(y,7) ^ vb; Y12 = Y8 - vc; Y0 = ROL(Y12,8) ^ vd
         va = Y0 - vb - w6; X0 = va - X4 - w2; X12 = ROL(vd,16) ^ va
    D0:  fd = ROL(X15,8) ^ X0; fc = S10 + fd; X10 = fc + X15; fb = ROR(S5 ^ fc,12)
         X5 = ROR(fb ^ X10,7); fa = ROL(fd,16) ^ S15; w8 = fa - S0 - S5; w9 = X0 - fa - fb
    D1:  gc = X11 - X12; gb = ROR(S6 ^ gc,12); X6 = ROR(gb ^ X11,7); gd = gc - S11
         X1 = ROL(X12,8) ^ gd; ga = ROL(gd,16) ^ S12; w10 = ga - S1 - S6; w11 = X1 - ga - gb

**Step S2.** w4 = W4 in A and w4' = W4' in B; w5' = w5 + (W4 - W4') = w5 + delta,
that is w5 - 8 (Lemma L); w13 = W13 and w14 = w15 = 0 in both.
**Step S3.** A = first 55 bytes of LE(w0..w15); B = first 63 bytes of the
same words with w4', w5'.

**Lemma S/F/Y.** For every context and every y: K0, K1, K2 (length 55),
K3 map the initial state to (S0..S15); D2 and D3 map S to (X2, X7, X8, X13)
and (X3, X4, X9, X14); D0 and D1 map S to (X0, X5, X10, X15) and
(X1, X6, X11, X12); and C0 on (X0, X4, X8, X12; w2, w6) has values
va, vd, vc, vb and outputs (Y0, y, Y8, Y12). *Proof.* For each call, each
of its eight assignments is one line above solved for its left side, as
listed in order: K0 (ka, kd, kc, kb forwards; the other four by the lines
for w1, S0, S12, S8); D2 (tc, td, tb, S7, X2, ta, S13, w12); K3 (mb, mc,
md, S15, S3, ma, w6, w7); K2 (p, q, r, u, S10, S6, S2, w5); D3 (ea, eb, ec,
ed, S9, S14, X9, X4); K1 (nc, nd, na, nb, S1, S5, w2, w3); D0 (fd, fc, X10,
fb, X5, fa, w8, w9); D1 (gc, gb, X6, gd, X1, ga, w10, w11); C0 (X0, X12,
X8 = vc - vd, vb, va, Y0, Y12, Y8). Every name is assigned once and only
from earlier lines (S8 before D2; S7, S13 before K3, K1; S3 before D3; S14
before the rest of K2; X0, X12 before D0, D1). The full assignment-by-
assignment proof of c66f230d Section 4 is this list written out; the
lemmas are also checked on real messages by both experiments and the
self-test (Sections 5, 6). QED.

**Theorem 1.** For every context and every y, A and B are distinct
messages of 55 and 63 bytes whose complete 2-round digests agree on words
0, 2, 5, 7, and Y4 = y in both. *Proof.* Bytes 55..63 of the block are zero
(w13 top byte, w14, w15), so A and B are honest messages with these blocks.
By Lemmas S/F/Y round 0 on A leaves X with (X3, X7, X11, X15) the constants;
by Lemma L B has the same X; Lemma H gives the four digest words; C0 reads
only shared words, so Y4 = y in both. The lengths differ. QED. Distinct
eight-word inputs give distinct messages A (each input is a function of A).

## 3. Class, sub-class S8, rule A, the beta filter and the residual words

**Class (Lemma Q, c66f230d).** E3's first assignment is e1 = Y3 + Y4 (for B
Y3' + Y4, w15 = 0) and its second h1 = ROR(Y14 ^ e1, 16), so
eta = h1 ^ h1' = ROR(e1 ^ (e1 + DY3), 16) with DY3 = Y3' - Y3 = fdb77cfd is a
function of Y4. With eta = 830303cf, the class is the set of Y4 with
(e1 AND 03cf8303) = 030c0303: since (e ^ x) - e = 2((~e) AND x) - x, the
condition e1 ^ (e1 + DY3) = x = ROL(eta,16) = 03cf8303 reads
2((~e1) AND x) = DY3 + x = 01870000, which fixes the 13 bits of e1 on x
(bit 31 is not in x) and leaves 19 free; 524,288 members.

**Sub-class S8 (new).** S8 is the set of class members whose e1 = Y3 + Y4
also has bits 2 and 3 equal to 1 and bit 21 equal to bit 26: 2^16 = 65,536
members (three linear conditions on free bits of e1). Member number i,
0 <= i < 2^16, has e1 = 030c0303 | 0000000c with the bits of i placed at the
free positions in the order 14, 30, 31, 4, 5, 6, 7, 10, 11, 12, 13, 20,
21, 27, 28, 29, then bit 26 set equal to bit 21; Y4 = e1 - Y3. (The order
is that of our previous version; with a branch-free batch it does not
affect the cost.)

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

**Beta filter (new).** E1's a1 and d1 are shared by A and B, c1 = Y11 + d1
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

**Lemma D (residual words, new).** For a trial write (a1, d1, c1, b1, a2,
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
## 4. Algorithm

1. Draw one uniform 256-bit word; take S11, S4, X13, w0 from it.
2. For each (vc, vd) with vd < V = 1,589,345 (2^32 * V pairs): run the lines
   of S1 not reading X14 and set the packed constants of the pair. For
   each X14 in 0..2^32-1: run the per-X14 set-up (Section 5) and then the
   9,363 batches of S8 (seven consecutive member numbers per batch; the
   last batch holds members 65,534, 65,535 and repeats 65,535). Each batch
   computes D1, D3, D4, D6 of Lemma D for its seven trials and tests
   whether some lane has all four zero (one compare and branch).
3. If the test passes: take the first lane of the batch with R = 0,
   recompute that trial in scalar form from its member number, build A, B
   (S2, S3), evaluate both complete digests, compare, output the pair if
   they are equal, and halt in either case.
4. Halt with failure when all trials are done.

There are N = 2^32 * V * 2^32 * 2^16 = V * 2^80 trials, all distinct pairs
(they differ in vc, vd, X14 or Y4, each a function of A). Step 3 runs at
most once. A trial with R = 0 is a collision (Lemma H), and the first such
trial is found: its batch computes its D words exactly (Lemma D, Section 5).
Rule A and the filter are not tested by the algorithm; they only narrow the
event *good* of H1 to the part of R = 0 that the count of Section 8 covers.

## 5. The counted batch on a 64-register machine

A packed 256-bit word holds seven 36-bit lanes (offsets 0, 36, .., 216),
each representing a value modulo 2^32 with four guard bits. A rotation by
r is PROR = ((z >> r) AND A_r) OR ((z << (32 - r)) AND B_r), 5 operations,
reading only the low 32 bits of each lane. x - y with constant x is
(y XOR M) + (x + 1) (M = 2^32 - 1 per lane); subtracting a constant is
adding its negation. Every executed primitive (add, xor, and, or, shift,
compare, branch, load) counts 1; shift amounts and load offsets are
instruction fields. The machine model is the 256-bit word RAM of the cost
model with 64 registers. Every batch executes the same 224 operations.

| Part | Computes | Ops |
|---|---|---:|
| A | load U[j] = ROL(y,7) per lane (1); Y8, Y12 (2); Y0 (6); va, ~X12, X0, fd, X10, gc (6) | 15 |
| A | X6 = ROR(gc ^ S6, 19) ^ ROR(X11, 7) (one rotation) | 7 |
| A | C2: a1 (1), d1 (6), c1 (1), b1 (6), a2 (2), z = a2 ^ d1 (1) | 17 |
| B | Y14 = ROR(z,8), c2 of C2, Y6 (ROR 7) | 12 |
| B | fc, X5 (two rotations), ~gd = ~gc + S11 (2), X1 = ROL(~X12,8) ^ ~gd, ga | 27 |
| B | C1: a1 (2), d1 (6), c1 (1), b1 (6), Y1 = a1 + b1 + ga + (-S1 - S6) (3), Y13 (6), Y9 (1) | 25 |
| B | E1: a1 = Y1 + Y6 + w12 (2), d1 (6), c1 (1) | 9 |
| C | E1 for A and B: c1' (1), b1, b1' (6 each), a2, a2' (2 each), d2, d2' (6 each), c2, c2' (1 each) | 31 |
| C | a2 ^ a2', c2 ^ c2', d2 ^ d2' (3); ROR(b1 ^ b1' ^ c2 ^ c2', 7) (7) | 10 |
| D | load y (1); e1, e1' (2); h1 (6), h1' = h1 ^ eta (1); g1, g1' (2); f1, f1' (6 each) | 24 |
| D | w8 = ROL(fd,16) ^ S15 - S0 - S5 (7); e2, e2' (2 each); h2, h2' (6 each); g2, g2' (1 each) | 25 |
| R | g2 ^ g2' (1); D1 (1); D3 (2); D4 (xor 2, rotation 5, xor 1); D6 (xor 2) | 14 |
| R | OR of the four (3), AND M (1), add M and AND 2^32 (2), compare with 2^32 per lane and branch (2) | 8 |
| | **batch (A 39, B 73, C 41, D 49, R 22)** | **224** |

*Zero test.* After the AND, a lane holds T = D1 OR D3 OR D4 OR D6 below
2^32, and bit 32 of T + 2^32 - 1 is 1 iff T != 0; the word ANDed with
2^32 per lane equals the broadcast 2^32 iff no lane has R = 0, so the
branch to step 3 is taken iff some lane has R = 0.

*Lane bounds.* Static per-lane upper bounds for all inputs are tracked by
the program for every addition: below 5, 11, 13, 5 and 2 times 2^32 in
parts A, B, C, D, R, all below 2^36, so no carry leaves a lane; XOR, AND
and PROR read only the low 32 bits of lanes or mask the rest.

*Registers.* 47 resident registers: the 12 rotation masks A_r, B_r
(r = 24, 19, 16, 12, 8, 7), 11 other global constants (M, 2^32, Y11, Y11',
Y3, Y3', eta, ROL(X15, 8), X11 + 1, ROR(X11, 7), -X15), 23 per-pair or
per-X14 constants and the list pointer. With the live temporaries the
peak is 62 of 64, computed by the program's liveness count over the batch.
No constant is kept in memory. The per-X14 set-up runs between batches
when no temporaries are live, with the 17 free registers, and overwrites
only per-X14 registers.

*Per X14 value.* The lines of S1 that read X14 and the fourteen packed
constants that depend on X14 (vb, -vb - w6, -X4 - w2, S10 + X15, S6, X14,
S5, w3, X9, -S1 - S6, w12, -S0 - S5, w5, w5 + delta), from 14 values stored
per pair: 183 operations counted by the program (scalar add or subtract 2
with the mask, XOR 1, rotation 4, broadcast to 7 lanes 7, loop 4) plus 14
loads; charged 256. The batch loop is unrolled 8 times: 1,170 iterations of
8 batches (pointer add, compare, branch) and a straight-line tail of 3
batches; charged 3 * 1,171 operations. The S8 list holds two packed words
per batch (ROL(y,7) and y), 9,363 * 64 bytes.

*Self-test of the shipped program.* `python3 experiments/s8search.py
--selftest 2000 9`, run from the repository root, builds 2,000 batches
(contexts from SHAKE-256 of the seed; every fourth case is the last batch,
in every fifth each context word is 0, 2^32 - 1 or random), and for every
lane builds the trial's messages A, B by steps S1, T, S2, S3, compresses them
with the program's own 2-round compression and with `verifier/blake3.py
blake3(m, 2)`, and checks: digest words 0, 2, 5, 7 agree, Y4 = member in S8
for both, eta = 830303cf, each of the four packed words D1, D3, D4, D6
equals the XOR of the two digests on words 1, 3, 4, 6, and the packed T
equals their OR; and that the branch is taken exactly when some lane has
equal digests. Result: 14,000 of 14,000 lanes right with the verifier,
2,000 of 2,000 batches with the right branch, 224 operations (39, 73, 41,
49, 22 by part) in every case, static bounds 5, 11, 13, 5, 2 times 2^32,
peak 62 registers; an exhaustive pattern test of the zero test (all 128
zero/nonzero lane patterns, four words each, nonzero lanes random or a
single bit) right in 512 of 512; the per-X14 set-up is 183 operations and
gives the batch's constants in 50 of 50 cases; the 65,536 member numbers
give 65,536 distinct members of S8; Lemma B holds for 6 of 6 betas. Exit
status 0 only if all of these hold. No real lane with R = 0 occurs at this
size; the taken branch is covered by the pattern test.

## 6. Experiments (organizer-run)

`experiments/s8search.py`, standard library only, seeds expanded by
SHAKE-256, no BLAKE3 import in organizer mode.

- `half-collision`: per seed, seven context words and a member number i of
  S8; returns the pair of Theorem 1. Event: digest words 0, 2, 5, 7 agree
  (exact, all seeds). Observations: the counted batch holding member i:
  batch_ops 224, lanes_right 7 (four packed residual words equal to the
  forward computation), branches_right 1, member_in_s8 1 (predicted for
  every seed).
- `class-filter`: per seed, a context and nine consecutive batches (63
  members) of S8; returns the seed member's pair (same event). Observations
  per seed: members 63, in_s8 63, y4_equal 63, eta_equal 63, lanes_right
  63, branches_right 9, lemma_b 6 (predicted for every seed), and the
  counts rule_a_lanes, filter_lanes, filter_and_rule_a_lanes (rates near
  2^-5, 2^-6, 2^-11 per trial). Each seed is one context, whose members are
  not independent. Our dry runs (256 seeds each, public and a holdout
  seed): every pair right, every predicted observation as stated, rule A in
  441 and 502, the filter in 229 and 268, both in 6 and 9 of 16,128 lanes.

Observations are the program's own and untrusted; they check the
generator, the class and the counted batch against a forward computation of
real messages. They do not measure H1.

## 7. Success probability

The probability space is the random word of step 1.

**H1 (score-critical).** Over the coins, the N = V * 2^80 trials behave with
respect to "good" (R = 0, rule A and the beta filter) like independent
events of probability at least 2^26.4 * 2^-128 each, to the extent that the
probability that no trial is good is at most exp(-lambda) + 0.002 with
lambda = N * 2^26.4 * 2^-128 = 0.5000003.

If some trial is good, it has R = 0; the batch of the first trial with
R = 0 takes the branch (Section 5) and step 3 outputs a pair whose complete
digests it has compared, with lengths 55 and 63. There are no budgets and
no other premise, so under H1 the algorithm outputs a collision with
probability at least 1 - exp(-0.5000003) - 0.002 = 0.3914 >= 0.39. The time
of Section 9 holds for every value of the coins. Sensitivity: with rate
f * 2^-128 the same search reaches 0.39 only for f >= 2^26.393
(lambda >= 0.49758); with the uniform rate (f = 1) it needs 2^127 trials
(varying the seed words) and gives 123.25.
## 8. Evidence for H1

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

**How r is counted (shipped: `python3 experiments/s8search.py --count`).**
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
these outcomes no S8 solution violates rule A. 2^26.4 = 88,550,677 is
185,350,144 / 2.093. All 15 betas with k <= 14 and the same counter give
185,355,230.33 for S8 with rule A (162,263,084.49 for the full class without
rule; 144,123,339.49 with rule A).

*Checks of the count.* (i) Three counting programs agree exactly: our C
counter, the shipped Python port (`--count`: all 85 outcomes, 57 nonzero,
the six parts and 185,350,144 in about 2.5 minutes; `--count all` also
gives the same total without rule A), and a counter written independently
by another helper agent, which gives 183,119,872 for the four heaviest
betas in S8 with and without rule A (margin 2.068 from these four alone).
A fourth, sampling estimator written by our review agent (Monte Carlo over
(y, h1, g1) for E3 and (c1, b1) for E1, exact automaton over e2 and a2)
gives 185,477,038 +- 878,331 (ratio 1.0007 +- 0.0047), with all 57 nonzero
outcomes within noise and the 28 zero outcomes zero. Per member of S8 the
exact factor (all 15 betas, rule A) lies between 184.57M and 186.14M, so
every member is above 2^26.4. (ii) The full-class parts and outcome
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

**Real trials (participant measurements, C programs on steps S1/T).**
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

**Scope and limitations of H1.** The factor 2^26.4 is assumed; it is set
against the exact model count 185,350,144 (margin 2.093), which the
organizer experiments do not measure. M is untested at probability 2^-100.6;
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
betas (1.63 times 2^26.4; betas outside T6 add under 32,000), so S8
supplies a factor 1.29 of the margin 2.093. The filter was chosen to
contain T6. A choice that is best under M says nothing about M and may
favour parameters where M overstates; the real-trial ratios above are the
check we have. 37% of the S8 count (44% in the full class) comes from one
beta, 18b0e098. The trials of a run share four seed words and the trials of
one context differ only in Y4; independence is assumed.

## 9. Charged time

Per X14 value (65,536 trials):
9363 * 224 + 3 * 1171 + 256 = 2,101,081 operations, 32.0600 per trial,
charged 32.07. Every batch executes the same operations, so this is a bound
for every run; the only data-dependent work is step 3, at most once.

- Main loop: 32.07 * N operations, N = V * 2^80 = 2^100.6.
- Step 3: at most once, under 2^11 operations and 2 compressions.
- Per pair (vc, vd): the lines of S1 without X14, 14 stored values, the
  pair constants in seven lanes, the loop step: under 2^11 operations;
  2^32 * V pairs.
- The S8 list (18,726 packed words): under 2^22 operations once.
- Randomness: 1.
- Preprocessing: 2^88 units, declared below.

    T = (32.07 N + 2^32 V 2^11 + 2^22 + 2^11 + 1) / 430 + 2 + 2^88
      = 2^96.8581   (32.07 * 2^100.6 / 430 = 2^96.85496; the other operation
                     terms are below 2^55 units; 2^88 + 2 units)

time_log2 = 96.8581, claimed 96.86 (rounded up).

**Preprocessing (declared charge).** The program stores the six constants
of Fact P, eta, the rule-A words, the filter words and the S8 conditions.
The constants were found by c66f230d with solver searches and chosen with
model counts; rule A, S8 and the filter were chosen with counts of the same
kind (S8 by us from the exact per-member factors of all 524,288 class
members, best of 8,992,320 candidate sub-classes). We do not reconstruct
this work from run records. We charge a declared upper bound of 2^88 units
(2^96.75 word operations) for all of it, ours and c66f230d's, including
every count and measurement of Section 8. It is more than 2^36 times
c66f230d's own estimate of their selection (below 2^60 operations, from
running times on one desktop machine and one graphics card), and more than
2^7 times ten years of the fastest existing supercomputer at about 2^60.6
operations per second. The charge moves the scalar by 0.003 (96.855
without it). The stored values themselves need no search to check: Fact P,
Lemma Q and Lemma B are finite computations repeated by the self-test and
the experiments.

## 10. Memory and advice

Search memory: code below 2^19 bytes, the S8 list 9,363 * 64 bytes,
constants and temporaries below 2^12 bytes: below 2^21 bytes. For the
preprocessing we use no reported peak: every byte it stores is written by
one of its charged word operations, so it stored at most
32 * 2^96.75 = 2^101.75 bytes; memory_log2_bytes = 102 is this bound and
covers the search (the cost model gives memory no scalar contribution).
Advice: the six constants, eta, the rule-A and filter words and the S8
conditions, below 64 bytes (nonuniform_advice_log2_bytes = 6).
preprocessing_log2 = 88 as charged above.
