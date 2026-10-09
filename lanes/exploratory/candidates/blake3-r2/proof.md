# The chunk counter with special frames, a 64-seed frame inverse and shared class landings for 2-round BLAKE3

The scalar below is `time_log2` under `collision-frontier-v5`. Memory is a
separately reported resource bound.

This exploratory package targets blake3-r2-prefix-v1 and claims time_log2 =
84.2073. It is a DISTINCT attack path on the chunk-counter construction of our
earlier entries, filed to record that path at its own price, which is worse
than the price of the ordinary counter search on the same construction. Nothing
in it lowers or replaces an earlier claim. Every construction, lemma, count
and charge that the claim uses is stated in this document with its proof,
including the free positions of the joint roots used by Lemma GC (A7). The
premises are declared in A11; the credit is in A14.

The text has two parts. PART A (Sections A1 to A15) is new: the special-frame
chart, its 64-seed inverse, the exact uniform frame sampler, the one-candidate
catalog query, the shared class landings (one admitted frame base serves m = 11
fresh queries), the halts, the charged time and the premises. PART B (Sections
1 to 8) is copied from the text of our whole-class chunk-counter package,
without the remarks that this path does not use: the exact compression, Lemma
L, Fact P, Lemma H, the root-instance construction that the two declared
experiments run (Sections 4 to 6), the tree lemma (Section 7) and the counter
construction with its per-trial counter solve (Section 8). Part B is the common
part of the two paths.

**Exact part.** For every choice of its free words, the counter construction
(Section 8) outputs two complete messages F || A and F || B of 1024 t + 55 and
1024 t + 63 bytes whose last-chunk chaining values agree on words 0, 2, 5 and
7, with the chunk counter t solved per trial; by the tree lemma (Section 7) a
pair whose last-chunk chaining values agree on all eight words is an ordinary
collision of two complete messages. This path draws the free words in a
different way from the ordinary search: it first draws an exact uniform
SPECIAL FRAME, a point of the restricted chart of A4 on which the class landing
of Y4 is an input rather than a rejected output (A5: the frame equation, its
64-seed inverse and the exact sampler of Lemma S); it then runs m = 11 fresh
one-candidate queries on that
frame (A7), each of which draws one record of an exact canonical catalog of E1
outcomes, orients it, inverts the counter construction to the unique candidate
that the record and the drawn prefix allow, and fully certifies that one
candidate. The sampler's law, the query's yield identity, its per-query cap of
sigma13/104 (about 1/104), the cluster retention bound for the shared frame
and every charge are proved in A4 to A10.

**Heuristic part.** The price needs a positive lower bound on the actual mean
number of full valid collisions per query on the special chart. No such bound
is proved. It is declared (heuristic H1-special-full-mean, A11) as the
transfer, at ratio theta0 = 1, of the ordinary first-moment lower of the
chunk-counter construction, (2^21 - 1) * 98,937,639,497 / 2^149 per trial,
itself a declared premise. A second premise is declared: the actual mean frame
multiplicity on the priced chart is at least 1 (H2-frame-balance). Under the
two, the algorithm of A9 succeeds with probability above 0.39.

**Advice and preprocessing.** The selected constants are fixed nonuniform
advice: the 76-byte record ADV stated in full in A3. The algorithm reads ADV
and does not search for it; the analysis uses ADV only through properties of
ADV itself (Lemma UA, A3), and no premise states that any procedure returns
ADV. The selection procedure SEL that found the selected words of ADV is
written out in A10 and charged in full as preprocessing: every run in it halts
at a stated cap, so its cost is at most S_old = 8,882,224,365,081,579,520
machine units by construction; it is not a premise. The algorithm halts within
the time bound of A10, below 2^84.20721704 target-compression units, so below
2^84.2073. No full 2-round collision is exhibited, and the search is far
beyond feasible computation.

## A1. Scope, status and what is new

*Same as the ordinary chunk-counter search.* The messages, the target, the tree
lemma, the counter construction of Section 8 with its per-trial counter
t = ROL(K0.d1,16) XOR K0.a1, the class of eta (Lemma Q: the 524,288 words Y4
with ((Y3 + Y4) AND 03cf8303) = 030c0303; GPT Sol's C13), the cube Q* of
beta* = 18b0e098, the six listed E1 outcomes S (A3), the six constants and the
machine (430 machine units per target compression) are the same.

*Different.* The ordinary search walks outer steps of 2^21 trials, filters
them exactly and solves a joint system per passing step. This path walks no
outer steps. It samples special frames exactly, reuses each one for m = 11
queries, and each query certifies at most one candidate. Its success mean is a
mean on the special chart, which the ordinary premise does not supply (A11).

*Status.* This is a draft record of a distinct path. Its price, 84.2073, is
above the price of the ordinary counter search on the same construction; it is
filed to record the path and its premises, not as an improvement.

## A2. The common part

The counter construction is Section 8, steps CO, CT and CS, with Lemma CT,
Theorem C, Lemma IP and Lemma F; the tree lemma is Lemma TR of Section 7. Three
facts of Part B are used below.

1. (Theorem C) For every choice of the seven outer words C0.d1, D2.a1, D2.b1,
   S11, S4, X9, w6, of a member y of the class and of a word c1, steps CO and
   CT give t; when t is not 0, step CS gives two distinct complete messages
   whose last-chunk chaining values agree on words 0, 2, 5 and 7; in the
   compression of A, E1.c1 = c1, and c1 in Q* gives beta = beta*.
2. (Lemma IP) For fixed outer words and y, c1 -> E3.h1 and c1 -> t are
   permutations of the 32-bit words; at most one member of Q* has t = 0, and
   that trial is invalid.
3. (Lemma TR) Equal last-chunk chaining values give equal digests of the two
   complete messages.

Part A also uses Section 3 (Fact P, the constants of 3.2 and the residual of
3.3), Lemma Q, step CO of Section 8 and the certificate of the outer filter of
Section 8. Part B also contains the material that the copied experiments cite
(Sections 1, 4, 6.1 and 6.5 and Lemma Q2).

## A3. The success event and the advice record

Fix flags 3 (Section 8, the line for K3.d1), the class C13 of Lemma Q, Q* of
beta* = 18b0e098, and the set S of six E1 outcomes, the tau values

    175020a0, 185020a0, 275020a0, 285020a0, 385020a0, 685020a0

(the set GPT Sol calls the selected 005f set; the outcome 675020a0 and the
seven outcomes of beta* with bit 14 of tau set are not counted). A trial of
Section 8 is a *full valid hit* when (i) t is not 0; (ii) c1 is in Q*; (iii)
the XOR differences between A and B of E1's a output and c output are tau and
eps = 6e21be55 for a tau in S; and (iv) the two last-chunk chaining values
agree on all eight words, that is R = 0 for the residual of 3.3 taken on the
last-chunk compression. By Lemma TR every full valid hit is an ordinary
collision of the two complete messages F || A and F || B.

Proof that (iii) and (iv) are the right conditions: by the proof of Lemma V
(A7), R = 0 is the conjunction of four XOR-difference equations on E1 and E3 (with eta = 830303cf
for every member of the class); for beta = beta* and eps = 6e21be55 the
condition eta = eps XOR ROL(beta XOR eps, 1) holds, since 6e21be55 XOR
ROL(18b0e098 XOR 6e21be55, 1) = 830303cf. A full valid hit is exactly the event
that the certification of A7 tests on the complete reconstructed pair, so its
definition is not used anywhere in an approximate form.

**The advice record ADV (fixed nonuniform advice).** The algorithm takes these
19 words as advice, fixed before it runs: 4 bytes each, 76 bytes in all, below
2^7 bytes (nonuniform_advice_log2_bytes = 7).

    ADV[0..5]    X3 X7 X11 X15 W4 W13 = 29d4fa98 bee3af28 44036000
                 40c58500 97475638 0007c006                (Section 3.2)
    ADV[6]       eta = 830303cf                            (Section 6.1)
    ADV[7]       beta* = 18b0e098                          (A3)
    ADV[8..9]    mask and value of Q* = 0e09818b 02008000  (Section 8)
    ADV[10..15]  the six taus of S = 175020a0 185020a0 275020a0
                 285020a0 385020a0 685020a0                (A3)
    ADV[16]      eps = 6e21be55                            (A3)
    ADV[17..18]  the two q of the b domain = 00000000 80000000 (A5)

The other fixed values used with ADV (Y3, Y11, DY3, DY11, K2's first values,
the class mask 03cf8303 and value 030c0303) are computed from ADV and the
standard IV by the exact steps of this document; the catalog is built from ADV
by the algorithm and charged in A10.

**Lemma UA (what the analysis uses of ADV).** The algorithm of A9 reads ADV
and does not search for it. Every property of ADV that the certification of
A7 and the bounds of A5 to A10 use is a statement about the stated words of
ADV, proved in this document:
(a) Fact P for the six constants, the zero top byte of W13 and W4 - W4' = -8,
    a finite computation displayed in Section 3.2;
(b) Lemma Q: eta gives the class C13 of 2^19 words (Section 6.1);
(c) eta = eps XOR ROL(beta* XOR eps, 1) (above);
(d) Q* = {c : (c AND 0e09818b) = 02008000} has 2^21 members with bit 31 free,
    0e09818b = ROL(beta*, 12), and c1 in Q* gives beta = beta* (Section 8,
    the cube Q*; Theorem C (iv));
(e) the two q give |B| = 2, so A = rbar_C * 2^84 (A5, the frame count);
(f) the catalog built from ADV has one record per hit and the T31 involution
    (Lemmas CAT and T31, A7);
(g) the catalog count Ncan = 13 * 2^27 and its build within 2^46 units
    (Lemma CAT and Lemma T31, A7); the cap of at most 32 selected full valid
    hits per physical context (Lemma GC, A7), which gives p* = sigma13 / 104;
    and the law of the priced sampler (Lemma S, A5).
Declared: H1 and H2 (A11), premises about ADV and its chart. None of these
refers to how ADV was found, and no step assumes that a procedure returns ADV.

Proof. Success (A9) uses the sampler law of (g) with H2, Lemma AR with the cap
of (g), the yield identity of A7 (which uses (f) and the count of (g)) and H1.
The ledger (A10) uses the budgets, the unit charges, the catalog charge of (g)
and the capped charge of SEL, which is a cost bound and states nothing about
ADV. The
certification (A7) uses (a) to (e) through Lemma CT, Theorem C, Lemma V and
Lemma TR, so for this ADV every certified pair is an ordinary collision. QED.

## A4. The special-frame chart and its class equation (GPT Sol AV 11.1)

Notation of Part A: b = D2.b1, z = C0.b1, f = w6, h = C0.d1 (not E3.h1),
j = S4 and g = D2.a1, outer words of Section 8, except inside Lemma V, Lemma
GC with the joint-root block that follows it, and the certification of A7,
which name E3's values h, g, f and E and an E1 outcome j there;
IVk is IV[k]; X3, X7, X11, X15, W4 and W13 are the constants of ADV.

**The special-frame chart (GPT Sol AV 8.2, PROVED).** For any words b, h, z,
f and j compute, in this order, the 17 chart formulas

    X8 = ROL7(X7) XOR b;          S7 = X8 XOR ROL12(b);
    K3.a1 = IV3 + IV7 + f;        K3.d1 = ROR16(K3.a1 XOR 3);
    K3.c1 = IV3 + K3.d1;          K3.b1 = ROR12(IV7 XOR K3.c1);
    S11 = ROL7(S7) XOR K3.b1;     S15 = S11 - K3.c1;
    S3 = ROL8(S15) XOR K3.d1;     X4 = ROL12(z) XOR (X8 + h);
    D3.a1 = S3 + j;               D3.b1 = X3 - D3.a1;
    X9 = ROL7(X4) XOR D3.b1;      C0.a1 = ROL16(h) XOR (X11 - S11);
    Y0 = C0.a1 + z + f;           Y12 = ROR8(Y0 XOR h);
    y = ROR7((Y12 + X8 + h) XOR z).

Run step CO of Section 8 on the outer words C0.d1 = h, D2.a1 = g (any word),
D2.b1 = b, S11, S4 = j, X9, w6 = f and the member y. It reproduces every
displayed name: C0.c1 = X8 + h; C0.b1 = ROR12(X4 XOR C0.c1) = z; D2.c1 =
ROL12(b) XOR S7 = X8, so X13 = X8 - D2.c1 = 0; X12 = ROL16(h) XOR C0.a1 =
X11 - S11, so D1.c1 = X11 - X12 = S11 and D1.d1 = D1.c1 - S11 = 0; and the
lines of step CO for Y8, Y12, Y0 and C0.a1 are the last three formulas read
backwards. Conversely an outer context with X13 = D1.d1 = 0 gives back
(b, h, z, f, j) as (D2.b1, C0.d1, C0.b1, w6, S4), and those lines force S11,
X9 and y. So the chart is a bijection between the words (b, h, z, f, j) and
the outer contexts with X13 = D1.d1 = 0, for every g; y depends on neither j
nor g. A *base* is (b, h, z, f); it is *admitted* when the computed y is in
the class C13 (Lemma Q), and then, with any j and g, it is an outer context of
Section 8 with its member y. On the chart put

    D = X8,  K = X11 - S11,  u = z + f,  V = (ROL7(y) XOR z) - D.

**Lemma AF (the frame equation; GPT Sol AV 11.1, PROVED).** For a prescribed
member y of the class, the whole class equation of the special frame is

    (ROL16(h) XOR K) + u = ROL8(V - h) XOR h.            (AV-FRAME)

Proof (checked here against the lines of step CO and step Y). D1.d1 = 0 gives
D1.c1 = S11, so X12 = X11 - S11 = K and C0.a1 = ROL16(h) XOR K. Then
Y0 = C0.a1 + z + f, and Y0 = ROL(Y12,8) XOR h gives Y12 = ROR8(Y0 XOR h). With
C0.c1 = X8 + h the line Y12 = Y8 - C0.c1 gives Y8 = Y12 + D + h, and
Y8 = ROL(y,7) XOR z gives ROL7(y) = (Y12 + D + h) XOR z, that is
Y12 = V - h. Substituting into Y0 = ROL8(Y12) XOR h gives AV-FRAME, and each
step is reversible, so a solution h returns the prescribed y. Once h is found,
every word j completes the chart. QED.

So the class member is an INPUT of the frame, not a rejected output.

## A5. The 64-seed frame inverse and the exact uniform frame sampler

**Lemma AI (GPT Sol AV 11.2, PROVED).** Let c_i be the carry into bit i of
(ROL16(h) XOR K) + u and beta_i the borrow into bit i of V - h. Guess the six
byte seams c8, c16, c24, beta8, beta16, beta24 (c0 = beta0 = 0). For depth
t = 0..7, at the four positions i = t + 8k (k = 0..3, indices mod 32), put
D_i = K_i XOR u_i XOR c_i XOR V_(i-8) XOR beta_(i-8). The word equation forces
h_i XOR h_(i-8) XOR h_(i-16) = D_i, whose unique solution is
h_i = D_i XOR D_(i-16) XOR D_(i-24), because (1 + x + x^2)(1 + x^2 + x^3) = 1
modulo x^4 + 1 (x one byte). Update c_(i+1) = maj(h_(i-16) XOR K_i, u_i, c_i)
and beta_(i+1) = maj(NOT V_i, h_i, beta_i); after depth 7 keep a seed only if
the carries and borrows leaving bytes 0, 1, 2 equal the guessed seams. Every
real root has its unique six seams and survives; every surviving seed is a
complete root; distinct seeds give distinct h. Hence the number of roots

    R_frame(b, z, f, y) = #{h solving AV-FRAME} satisfies 0 <= R_frame <= 64,

and for fixed (b, z, f) the sum over all 2^32 words y is exactly 2^32.
R_frame is not constant: with S11 = X11 and z = -f (K = u = 0) the two words
017f0180 and 00800080 give the same V, so some targets have no root and some
have several (AV 11.2).

*The frame count.* The priced chart uses b in B = {q - W13 : q in {0,
80000000}} (two values; GPT Sol AV 8.1, 21.1). Put

    rbar_C = E over (b in B, z, f, y in C13) of R_frame,
    A = A_C13(B) = sum over b in B, z, f, y in C13 of R_frame = rbar_C * 2^84.

By Lemma AF and the chart, A is the number of admitted bases (b, h, z, f) with
b in B, and the direct-chart landing share is p_land = A / (|B| 2^96) =
rbar_C * 2^-13. Lemma S below proves rbar_C <= 8 and A <= 2^87. A positive
lower bound on rbar_C of useful size is not proved; the mean is a premise
(H2-frame-balance).

**The class in bits (GPT Sol AV 17.1, PROVED).** Write y_i for bit i of y.
With Y3 = 8127c181, y is in C13 exactly when

    y0 = 0, y1 = 1;  y8 = y7, y9 = 1 XOR y7;  y15 = 1 XOR y14;
    y16 = y17 = y19 = 0, y18 = 1;  y22 = y23 = y24 = y21, y25 = 1 XOR y21,

thirteen independent affine equations. Proof, with c_i the carry into bit i of
Y3 + y, whose bits on the mask 03cf8303 Lemma Q fixes to 030c0303: bits 0 and
1 give y0 = 0, y1 = 1 and c2 = 0; c7 = 0 and c8 = y7, so bits 8 and 9 give
y8 = y7, y9 = 1 XOR y7 and c10 = 0; c14 = 0 and c15 = y14, so bit 15 gives
y15 = 1 XOR y14 and c16 = 1; bits 16 to 18 give y16 = y17 = 0, y18 = 1 and
c19 = 1; bit 19 gives y19 = 0 and c20 = 0; bit 20 of Y3 is 0, so c21 = 0 and
c22 = y21; bits 22 to 24 keep that carry and force their y bits to y21; bit
25 gives y25 = 1 XOR y21. QED. In the bytes Wk of w = ROL7(y), with Wk_i bit
i of Wk, this reads: W0_7 = 0; W1_0 = 1, W1_7 = W1_6; W2_0 = p := 1 XOR W1_6,
W2_6 = 1 XOR W2_5, W2_7 = 0; and W3 = M_e := 02 OR (r * f0) OR (e << 3), with
r = 1 XOR W0_0 and e = y20 (r * f0 is the byte f0 when r = 1, else 0). So W0
has seven free bits, W1 six, W2 five, and e is the one free bit of W3.

**Projection inverse (GPT Sol AV 17.2, PROVED).** Fix b, h, f and the low byte
z0 of z; put D = X8, K = X11 - S11 (the chart, flags 3), L = (ROL16(h) XOR K)
+ f, T = D + h and v0 = (L + z0) AND ff. For a prescribed low part W of w,
start from Z = z0 and repeat

    Rtmp = ((W XOR Z) - T) mod 2^32;
    V = ((h XOR ROL8(Rtmp)) AND ffffff00) OR v0;
    Z = (V - L) mod 2^32.

After k <= 3 updates the low 8 + 8k bits of Z and of V are those of z and of
Y0 = L + z for every z with low byte z0 whose w agrees with W on its low 8k
bits; for k = 3 that z is unique. Proof: by the chart Y0 = L + z and
w XOR z = Y12 + T with Y12 = ROR8(Y0 XOR h), so z solves
Y0 = ROL8((w XOR z) - T) XOR h, whose low byte is v0. If Z has its true low k
bits, the subtraction and XOR give the true low k
bits of Rtmp, ROL8 lifts them into positions 8 to k + 7, the low byte is
replaced by v0, and subtracting L gives the true low k + 8 bits of the next Z;
the same argument gives uniqueness byte by byte. QED.

**Byte completion (GPT Sol AV 25.1, PROVED).** Fix b, h, f, z0 and bytes W0,
W1 obeying their class bits, let W01 = W0 OR (W1 << 8), and run two updates
with W = W01; they give the true low 24 bits of z and of V. In this paragraph
a name with a byte index (T2, T3, L3, h0, h3, R2, R3, z2, z3, v3, w3, W2) is
byte k of the word T, L, h, R, z, V or w, and the suffix _i is bit i. Put

    BR16 = [((W01 XOR Z) AND ffff) < (T AND ffff)];
    BZ24 = [(V AND ffffff) < (L AND ffffff)];
    z2 = byte 2 of Z;   R3 = v0 XOR h0,

the true borrows into bit 16 of (w XOR z) - T and into bit 24 of V - L. The
class bit W3_0 = 0 forces the borrow br into bit 24 of (w XOR z) - T:

    br = (T3 XOR R3 XOR h3 XOR p XOR z2 XOR T2 XOR BR16 XOR L3 XOR BZ24) AND 1.

For each e in {0, 1} compute

    P3 = (T3 + R3 + br) mod 256;   z3 = P3 XOR M_e;
    v3 = (z3 + L3 + BZ24) mod 256;   R2 = v3 XOR h3;
    N2 = R2 + T2 + BR16 (0 to 511);   W2 = (N2 mod 256) XOR z2,

and keep the completion only if floor(N2 / 256) = br and W2_0 = p,
W2_6 = 1 XOR W2_5, W2_7 = 0; then z = (Z AND ffffff) OR (z3 << 24).

Proof. R = ((w XOR z) - T) mod 2^32 is Y12 and V = Y0 = ROL8(R) XOR h = L + z,
so byte k of R is byte k + 1 of V XOR byte k + 1 of h, indices mod 4. The two
updates fix every displayed lower quantity. At byte 3,
w3 = ((T3 + R3 + br) mod 256) XOR z3 and z3 = ((h3 XOR R2) - L3 - BZ24) mod 256,
with br the borrow into bit 24; the low bit of R2 is
p XOR z2_0 XOR T2_0 XOR BR16, since bit 16 of w is W2_0 = p; so w3_0 = 0 is the
displayed equation for br. Given br and W3 = M_e, reversing the two byte
additions and XORs gives the displayed z3, v3, R2 and W2, and
floor(N2 / 256) = br closes the carry of the branch. Distinct e give
distinct z3. Conversely every base with y in C13 has its own e = y20, borrow
and completion. So at fixed (b, h, f, z0, W0, W1) there are at most two
admitted bases, one for each e, and the procedure returns exactly those. QED.

**Lemma S (the priced sampler; GPT Sol AV 25.2, PROVED).** A proposal draws
independently, from disjoint coin fields, the q bit, h and f (32 bits each),
z0 (8 bits), the seven free bits of W0, the six of W1 and e: 87 bits, so
D13 = 2^87 equally likely tuples. It runs the byte completion for its e (every
failed check is a charged failure, with no retry), computes y by the chart and
admits the base when y is in C13. Then (i) every admitted base (b, h, z, f)
comes from exactly one tuple: q from b, its own h, f and z0, the bytes W0 and
W1 of its w = ROL7(y), and e = y20; (ii) the base of an admitted proposal is
exactly uniform on the A admitted bases, independently of which proposals are
admitted; (iii) a proposal is admitted with probability A / 2^87 = rbar_C / 8;
(iv) A <= 2^87 and rbar_C <= 8. Proof. (i) is the converse part of the byte
completion with the uniqueness of the projection inverse. So the admitted
tuples are in bijection with the A admitted bases, which gives (ii) and (iii),
and they are at most the 2^87 tuples, which gives (iv). QED. The price runs
four independent proposals per batch on the four lanes of A6.

## A6. Four lanes on the word RAM

**Spaced lanes (GPT Sol AV 21.1, PROVED).** Four 32-bit lanes at offsets 0,
64, 128, 192, with M = sum of (ffffffff << 64k) and G = sum of (1 << (64k +
32)) over k = 0..3. Lane addition is (A + B) AND M (largest digit 2^33 - 2, no
carry crosses a spacer); lane subtraction is ((A OR G) - B) AND M (each 64-bit
digit lies in 1 .. 2^33 - 1, no borrow between lanes); a lane rotation by
0 < r < 32 is ((A << r) OR (A >> (32 - r))) AND M, four primitive operations.
Two fresh 256-bit coins per batch supply the four proposals of Lemma S on
disjoint bits (4 * 87 = 348 bits used). A lane zero flag is
(((X OR G) - repeatedOne) AND (NOT X)) AND repeatedBit31.

| Batch item, four lanes (GPT Sol AV 25.3) | Units |
|---|---:|
| Two coins, W01 and e assembly | 64 |
| q records, K, L, T, v0, Z setup | 48 |
| Two projection updates (14 each), true borrows (16), byte completion | 160 |
| Computed y, class test and lane zero flags | 32 |
| All 20 payload writes, branches, addresses, control, spills | 192 |
| Total 496, charged | 512 |

A projection update is 14 lane operations (XOR, guarded subtraction, rotation
by 8, XOR, AND, OR, guarded subtraction); the guarded 16- and 24-bit
comparisons give the true borrows in at most 16 more; byte sums never exceed
511, so no carry crosses a spacer; r * f0 is formed as (G8 - r) AND f0 in every
lane, with G8 the sum of (256 << 64k), never as an unguarded 0 - r. At most 16
live registers, with packed b, L and T saved in paid scratch; 4096 once for
packed constants (inside the 8192 metadata of A10). Admitted lanes are
serialized in fixed order and the first N admitted bases are kept; surplus is
discarded without inspecting its values, so the kept bases are iid uniform
(Lemma S). The price charges the fixed batch budget Bsam of A9, not an
expected work per base.

## A7. The one-candidate catalog query

**Lemma CAT (the local E1 catalog; GPT Sol answer AK auxiliary 1 and 2, AV
22.1, 31.1).** For message A write c = E1.c1, b_E1 = E1.b1, a = E1.a2 and
d = E1.d1 = c - Y11, with Y11 = 7af77f38, DY11 = Y11' - Y11 = 0a08818b,
beta = beta* = 18b0e098, Bc = ROL12(beta) = 0e09818b and delta = -8. For c in
Q*, step CT and the proof of Theorem C (iv) give on message B the same E1.a1
and E1.d1, the c value c + DY11 = c XOR Bc, b_E1 XOR beta in place of b_E1,
and a + Delta(s) in place of a, with s = b_E1 AND beta and
Delta(s) = beta - 2 s - 8, since (b_E1 XOR beta) - b_E1 = beta - 2 s. With
z_local = E1.d2 = ROR8(d XOR a), the XOR differences between A and B of E1's a
and c outputs are

    tau = a XOR (a + Delta(s)),
    epsilon = (c + z_local) XOR ((c + DY11) + (z_local XOR ROR8(tau))).

A *record* is (c, z_local, s, tau) with c in Q*, tau one of the seven outcomes
175020a0, 185020a0, 275020a0, 285020a0, 385020a0, 675020a0 and 685020a0,
epsilon = eps, and tau = a XOR (a + Delta(s)) for a = d XOR ROL8(z_local). As
(a XOR tau) - a = tau - 2 (a AND tau), the last condition is a AND tau =
p(s) := (tau - Delta(s)) / 2, where s is *compatible* with tau when
tau - Delta(s) is even and p(s) has no bit outside tau. Every selected full
valid hit of A3 has exactly one record: c, a and b_E1 determine
s = b_E1 AND beta, z_local = ROR8((c - Y11) XOR a) and
tau = a XOR (a + beta - 2 s - 8), and its epsilon is eps.

*Count.* For each tau and compatible s a bit-serial recurrence over i = 0 to
31 counts the pairs (c, z_local): at bit i choose c_i (fixed on the cube bits
of Q*) and z_i (bit i of z_local), carrying the borrow of c - Y11 and the
carry cy of c + z_local; with rho = ROR8(tau) and kappa = Bc XOR rho XOR eps
(kappa_0 = 0) the carry of the second sum is cy XOR kappa_i, and the next
carries cn = maj(c_i, z_i, cy) and
cn' = maj(c_i XOR Bc_i, z_i XOR rho_i, cy XOR kappa_i) must satisfy
cn XOR cn' = kappa_(i+1) for i < 31, which is equivalent to epsilon = eps;
where tau has bit i set, impose d_i XOR z_((i-8) mod 32) = p(s)_i, since
a = d XOR ROL8(z_local). The bits z29 and z31, read at bits 5 and 7, where every tau has a set
bit, are guessed at the start and enforced at their own positions; at most
five z bits are pending at any time. The recurrence gives this finite exact
count, the same for every compatible s of a row:

| tau | compatible s | pairs per s | records |
|---|---:|---:|---:|
| 175020a0 | 16 | 2^24 | 2^28 |
| 185020a0 | 32 | 2^25 | 2^30 |
| 275020a0 | 8 | 2^25 | 2^28 |
| 285020a0 | 16 | 2^26 | 2^30 |
| 385020a0 | 32 | 2^24 | 2^29 |
| 675020a0 | 8 | 2^23 | 2^26 |
| 685020a0 | 16 | 2^24 | 2^28 |

So there are 53 * 2^26 records, and without 675020a0, which is not in S,
Nsel = 52 * 2^26 = 13 * 2^28 selected records. *Build.* The recurrence has at
most 4 guess seeds, 32 slices, 4 carry and borrow tags, 2^5 pending states and
4 bit pairs: at most 2^16 transitions per (tau, s), at most 2^23 units at 128
units per transition, and the 128 compatible pairs with their enumeration fit
2^31. Backward continuation counts then emit every record once, without
rejection or duplicate, at most 2^13 units per record for the depth-32
traversal and the store of one 256-bit word (c, z_local, full s, tau index):
53 * 2^26 * 2^13 + 2^31 < 2^46. QED.

**Lemma T31 (GPT Sol AV 31.1, PROVED).** The map

    c -> c XOR 80000000,  d -> d XOR 80000000,  a -> a XOR 80000000,
    z_local, s, tau unchanged                                      (T31)

is a fixed-point-free involution of the selected catalog. Proof. Bit 31 of the
cube mask 0e09818b is free, so c XOR 80000000 is in Q* with c, and changing c
by 2^31 changes d by 2^31. In the record's exact eps equation
(c + z_local) XOR ((c + DY11) + (z_local XOR ROR8(tau))) = eps both sums change
by 2^31 and their XOR is unchanged; likewise a XOR (a + beta - 2 s - 8) is
unchanged when both terms change by 2^31. This holds with carries and modular
wrap, not only for record counts. QED.

Keep from each pair the representative with bit 31 of c equal to 0:
Ncan = 13 * 2^27 = 1,744,830,464 canonical records. They are emitted by the
recurrence of Lemma CAT with c31 = 0 and the row 675020a0 skipped, within its
2^46 charge, and a compact layout (8 units per record; 8 Ncan < 2^34) is
charged once at 2^34 more. At one 256-bit slot per record the catalog is
13 * 2^32 bytes, below 2^36.

**Counts (GPT Sol AV 22.1).** Let V = (b, h, z, f) be uniform on the A
admitted bases. For a word j, a word g and c in Q*, let A_good(V, j, g, c) = 1
exactly when the physical context is a full valid hit of A3. Put

    G(V, j) = sum over g (2^32) and c in Q* (2^21) of A_good,
    G(V)    = sum over j of G(V, j),
    p_raw(V) = G(V) / 2^85,     mu_raw = E_V p_raw(V).

mu_raw is the actual mean of the raw special-chart query: one fresh (j, g, c)
on a uniform admitted base; it counts nonzero-counter selected full valid hits
only. Lemma GC gives at most 32 good c for every (V, j, g), so
G(V, j) <= 32 * 2^32, G(V) <= 2^69 and p_raw(V) <= 2^-16.

**Lemma GC (the guard cap; GPT Sol AV 12).** For every physical outer context
(the seven outer words and y fixed), at most 32 words c1 in Q* give a selected
full valid hit.

Proof. (1) By Lemma IP (a), c1 -> h = E3.h1 is a permutation, so distinct
hits of one context have distinct h. (2) A hit with outcome j satisfies J1 of
Lemma V, where E3.g1 = Y9 + h (step CT), that is
(Y9 + h) XOR (Y9 + (h XOR eta)) = theta_j: h witnesses condition (1)_j of the
outer filter (Section 8) for the context's Y9, so j lies in the mask of Y9
under (1). By the certificate of Section 8 that mask is one of twelve, each
inside {275020a0}, {175020a0, 675020a0}, {285020a0, 385020a0} or
{185020a0, 385020a0, 685020a0}; within S these sets have 1, 1, 2 and 3
outcomes. (3) For one outcome j of S, the h of every hit with outcome j is a
joint root of j that satisfies (G7) (Lemma V and Lemma G7 below), and by Lemma
FP below one context has at most 2^|F_j| such words, F_j = {13, 15, 30} for
175020a0, 185020a0 and 685020a0 and F_j = {9, 13, 15, 30} for 275020a0,
285020a0 and 385020a0. So the four sets have at most 16, 8, 16 + 16 = 32 and
8 + 16 + 8 = 32 hits, and a context at most 32. QED.

**Joint roots (the names of this block).** x[i] is bit i of a word x, bit 0 the
lowest, and maj is the majority of three bits. Fix a physical outer context:
Q = Y9, y its member, e1 = Y3 + y, omega = e1 + w8 and omega' = omega + DY3
(Y9 and w8 names of step CO). For an outcome j of S put sigma = sigma_j,
theta = theta_j, tau = tau_j and mu = ROR(eta XOR eps, 8) = 9aed22bd, and for a
word h put g = Q + h, f = ROR(y XOR g, 12), e2 = omega + f and
h2 = ROR(h XOR e2, 8); with E3.h1 = h these are E3.g1, E3.f1, E3.e2 and E3's d
output on A (step CT, w15 = 0). h is a *joint root* of j when

    (J1)  (Q + h) XOR (Q + (h XOR eta)) = theta,
    (J2)  (omega + f) XOR (omega' + (f XOR sigma)) = eps,
    (J3)  (g + h2) XOR ((g XOR theta) + (h2 XOR mu)) = tau.

These are J1 to J3 of Lemma V with E = e2 and E - f = omega, so E3.h1 of every
full valid hit with outcome j is a joint root of j. By (J1) theta is fixed by
h, and then so is the left side of (J3); the six values of tau differ, so no
word is a joint root of two outcomes.

**Lemma CB (carry bits; PROVED).** Let x' = x XOR dx and z' = z XOR dz, let r
be a word, let k[i] and k'[i] be the carries into bit i of x + z and of
x' + z' (k[0] = k'[0] = 0), and put dk = dx XOR dz XOR r. (a)
(x + z) XOR (x' + z') = r exactly when k'[i] = k[i] XOR dk[i] for every i.
(b) If k'[i] = k[i] XOR dk[i] at a bit i < 31, then

    k'[i+1] XOR k[i+1] = (dx XOR r)[i] x[i] XOR (dz XOR r)[i] z[i]
                         XOR (dx XOR dz)[i] k[i] XOR maj(dx[i], dz[i], dk[i]).

So where (dz XOR r)[i] = 1, given x[i] and k[i], exactly one value of z[i]
gives k'[i+1] = k[i+1] XOR dk[i+1]; where it is 0, z[i] does not enter that
test.

Proof. (a) Bit i of the XOR of the two sums is dx[i] XOR dz[i] XOR k[i] XOR
k'[i]. (b) Over GF(2), maj(p, q, t) = pq XOR qt XOR tp; expanding
maj(x[i] XOR dx[i], z[i] XOR dz[i], k[i] XOR dk[i]) XOR maj(x[i], z[i], k[i])
gives x[i] (dz XOR dk)[i] XOR z[i] (dx XOR dk)[i] XOR k[i] (dx XOR dz)[i] XOR
maj(dx[i], dz[i], dk[i]), and dz XOR dk = dx XOR r, dx XOR dk = dz XOR r. QED.

For (J1) (x = Q, dx = 0, z = h, dz = eta, r = theta) the carries u1 and u1' of
the two sums satisfy u1' = u1 XOR gamma with gamma = eta XOR theta, and h[i]
enters the test into bit i + 1 with the coefficient gamma[i]. For (J2)
(x = omega, x' = omega', z = f, dz = sigma, r = eps) the carries u2 and u2'
satisfy u2' = u2 XOR chi with chi = omega XOR omega' XOR sigma XOR eps, and
f[k] enters the test into bit k + 1 with the coefficient (sigma XOR eps)[k];
put lambda = (sigma XOR eps) AND 7fffffff. Bit k = (i + 20) mod 32 of f is
f[k] = y[i] XOR g[i] = y[i] XOR Q[i] XOR h[i] XOR u1[i]. So, given u1[i] and
u2[k], at most one value of h[i] passes when i < 31 and gamma[i] = 1, or when
lambda[k] = 1: position i is then *prescribed by a carry*.

*Finite facts (each checked here exactly).* Every member of the class has
y[0] = 0, y[1] = 1 and bits 16 to 19 of y equal to 0, 0, 1, 0 (all 2^19
members of Lemma Q), and e1[22] = e1[23] = 0 (Lemma Q). On every row of S:
tau[0] = tau[1] = 0, theta[0] = theta[1] = 1, gamma[i] = 0 for i = 0, 1, 2,
4, 5 and 6, gamma[18] = gamma[19] = 1, gamma[20] = 0, sigma[0] = 0,
sigma[20] = sigma[21] = 1 and lambda[0] = lambda[22] = lambda[25] = 1, and
lambda[23] = 1 exactly when gamma[3] = 0. Also eps[0] = 1, eps[20] = 0,
eps[21] = 1, mu[0] = 1, mu[1] = 0, eta[3] = eta[6] = eta[7] = eta[9] = 1 and
eta[10] = eta[18] = eta[19] = 0; DY3 = fdb77cfd is odd, so chi[0] = 0. The
masks:

| tau | gamma | lambda | prescribed by a carry, positions 7 to 31 |
|---|---|---|---|
| 175020a0 | 000c0200 | 72d98ea5 | 8, 9, 10, 12, 14, 17, 18, 19, 21, 22, 23, 27, 28, 31 |
| 185020a0 | 000c0288 | 7a598ea5 | 7, 8, 9, 10, 12, 14, 17, 18, 19, 21, 22, 23, 27, 28, 31 |
| 275020a0 | 000c0080 | 5ad98ea5 | 7, 8, 10, 12, 14, 17, 18, 19, 21, 22, 23, 27, 28, 31 |
| 285020a0 | 000c0008 | 52598ea5 | 8, 10, 12, 14, 17, 18, 19, 21, 22, 23, 27, 28, 31 |
| 385020a0 | 000c0188 | 4a598ea5 | 7, 8, 10, 12, 14, 17, 18, 19, 21, 22, 23, 27, 28, 31 |
| 685020a0 | 000c0608 | 32598ea5 | 8, 9, 10, 12, 14, 17, 18, 19, 21, 22, 23, 27, 28, 31 |

The low rows are 175020a0 and 275020a0 (gamma[3] = 0), the high rows the other
four (gamma[3] = 1).

*The phase equations and the parity (exact counts of the class).* Every joint
root h of an outcome of S, for y in the class, satisfies

    h[0] = 0,  h[1] = 1,  h[2] = 1 XOR e1[2],  h[10] = e1[2],
    h[16] = h[17] = 0,  h[11] = 1 XOR h[3],
    h[24] = h[3] XOR h[12] XOR e1[21],                              (PHASE)
    h[6] XOR h[13] XOR h[25] = e1[21].                              (P*)

Both are read off exact counts. The number N3_j of quadruples (y, h, Y9, w8),
y in the class, for which h is a joint root of j (the E3 conditions of the
proof of Lemma V) is a sum of nonnegative integers over an exact enumeration of
submasks, through (x XOR m) - x = m - 2 (x AND m) modulo 2^32 and a carry
recurrence with two states, in coordinates of E3 that are a bijection of the
counted quadruples; nothing is sampled. Split by the pattern of h on bits 0 to
3, 6 to 13, 16, 17, 24 and 25 and by the phase (e1[2], e1[21], e1[26]), every
cell with a nonzero count satisfies (PHASE); the eight phases hold 88, 88,
108, 132, 108, 132, 88 and 88 patterns, in the order e1[2] + 2 e1[21] +
4 e1[26]. Split by the phase and by h[6] XOR h[13] XOR h[25], every phase holds
a_j * 2^49 quadruples with the parity e1[21] and none with the other, with
a_j = 24, 16, 4, 24, 32 and 6 for the rows 175, 185, 275, 285, 385 and 685,
and the cells add up to N3_j = a_j * 2^52. A joint root adds at least 1 to the
cell of its pattern, so a cell of count 0 holds none: (PHASE) and (P*) hold for
every joint root, pointwise, and drop no member and no root. Each line of
(PHASE) and (P*) is also checked exhaustively for every row of S in A15.

**Lemma J0 (PROVED from (PHASE)).** Every joint root of an outcome of S has
Q[0] = Q[1] = 0, g[0] = 0, g[1] = 1 and h2[0] = 0, that is h[8] = e2[8].

Proof. h[0] = 0 and h[1] = 1 by (PHASE), and u1[0] = 0. Lemma CB (b) for (J1)
at bit 0 (theta[0] = 1, gamma[0] = 0, eta[0] = 1) requires Q[0] = gamma[1] =
0; then u1[1] = Q[0] AND h[0] = 0, and at bit 1 (theta[1] = 1, gamma[1] = 0,
eta[1] = 1) it requires Q[1] XOR u1[1] = gamma[2] = 0, so Q[1] = 0. Hence
g[0] = 0 and g[1] = 1. Both sums of (J3) have carry 0 into bit 0. At bit 0,
g + h2 adds 0 and h2[0], with sum bit h2[0] and carry 0; (g XOR theta) +
(h2 XOR mu) adds 1 and h2[0] XOR 1, with sum bit h2[0] and carry
1 XOR h2[0]. At bit 1 the first sum adds 1, h2[1] and 0, with sum bit
1 XOR h2[1]; the second adds g[1] XOR theta[1] = 0, h2[1] XOR mu[1] = h2[1] and
1 XOR h2[0], with sum bit h2[1] XOR 1 XOR h2[0]. (J3) requires the XOR of the
two sum bits, h2[0], to be tau[1] = 0. QED.

Since e2[8] = omega[8] XOR f[8] XOR u2[8] and f[8] = y[20] XOR Q[20] XOR h[20]
XOR u1[20], Lemma J0 is the guard h[20] = h[8] XOR omega[8] XOR u2[8] XOR
y[20] XOR Q[20] XOR u1[20], which reads bits of h below 20 only (u2[8] reads
f[0] to f[7], that is bits 12 to 19).

*Constants and guards.* For y in the class, every joint root of an outcome j
of S has the following values; positions 0 to 6 are fixed by the context.

(a) The carry u2[22] is the same for all joint roots of j in the context. By
Lemma J0 and y[0] = 0, y[1] = 1, f[20] = f[21] = 0, so bits 20 and 21 of (J2)
read only omega[20..22], omega'[20..22], sigma, eps and the carry u2[20], with
u2'[20] = u2[20] XOR chi[20] (Lemma CB (a)). Over all 64 values of those six
bits of omega and omega' and both values of u2[20], the values of u2[20] that
pass the tests into bits 21 and 22 give a single u2[22] (finite check here, on
every row of S).
(b) f[22] is prescribed by its carry (lambda[22] = 1). On the low rows
lambda[23] = 1 and f[23] is prescribed; on the high rows Lemma CB at bit 3
(gamma[3] = 1, eta[3] = 1, theta[3] = 0, gamma[4] = 0) gives
h[3] = 1 XOR u1[3], so f[23] = 1 XOR Q[3] XOR y[3]. Bits 22 and 23 of (J2)
then give u2[24].
(c) h[0] = 0, h[1] = 1 and u1[2] = maj(Q[1], h[1], u1[1]) = 0;
h[2] = y[2] XOR f[22] XOR Q[2], and the context has no joint root of j unless
h[2] = 1 XOR e1[2]; u1[3] = maj(h[2], Q[2], 0), h[3] = y[3] XOR f[23] XOR Q[3]
XOR u1[3] and u1[4] = maj(h[3], Q[3], u1[3]); h[10] = e1[2] and
h[11] = 1 XOR h[3]. At bit 9 (eta[9] = 1) the test of (J1) into bit 10 reads
Q[9] XOR u1[9] = gamma[10] when gamma[9] = 0 and h[9] XOR u1[9] XOR 1 =
gamma[10] when gamma[9] = 1; so if gamma[10] = 0, either u1[9] = Q[9] or
h[9] differs from u1[9], and in both cases u1[10] = Q[9] and
u1[11] = maj(h[10], Q[10], Q[9]). If gamma[10] = 1 (685020a0), the test at
bit 10 (eta[10] = 0, gamma[11] = 0) gives h[10] = Q[10] and u1[11] = Q[10].
Then u1[12] = maj(h[11], Q[11], u1[11]).
(d) f[0] is prescribed with u2[0] = 0 (lambda[0] = 1), and
u2[1] = maj(omega[0], f[0], 0); h[12] = y[12] XOR f[0] XOR Q[12] XOR u1[12],
u1[13] = maj(h[12], Q[12], u1[12]) and h[24] = h[3] XOR h[12] XOR e1[21]
(PHASE).
(e) Bit 16 of h2 is 0, so e2[24] = h[24] and f[24] = h[24] XOR omega[24] XOR
u2[24]; then h[4] = y[4] XOR f[24] XOR Q[4] XOR u1[4] and
u1[5] = maj(h[4], Q[4], u1[4]), and bit 24 of (J2) must pass. f[25] is
prescribed (lambda[25] = 1), u2[26] = maj(omega[25], f[25], u2[25]) and
h[5] = y[5] XOR f[25] XOR Q[5] XOR u1[5].
(f) On the low rows: if omega[1] = u2[1], the carry u2[2] is omega[1], f[2] is
prescribed (lambda[2] = 1) and e2[2] = omega[2] XOR f[2] XOR omega[1];
otherwise the context has no joint root of j if chi[2] = 1, and
e2[2] = omega[2] XOR chi[3] if chi[2] = 0. Then h[26] = 1 XOR h[2] XOR e2[2]
XOR Q[26] XOR Q[25], f[26] = h[26] XOR omega[26] XOR u2[26], and
h[6] = f[26] XOR y[6] XOR gamma[7], since at bit 6 (eta[6] = 1, gamma[6] = 0)
(J1) requires Q[6] XOR u1[6] = gamma[7]; position 25 has the guard
h[25] = h[6] XOR h[13] XOR e1[21] (P*). On the high rows: h[25] = e2[1], with
e2[1] = omega[1] XOR f[1] XOR u2[1] and f[1] = y[13] XOR Q[13] XOR h[13] XOR
u1[13]; with (P*), h[6] = h[13] XOR h[25] XOR e1[21] = y[13] XOR Q[13] XOR
u1[13] XOR omega[1] XOR u2[1] XOR e1[21], in which h[13] cancels, so h[6] is
fixed by (c) and (d), and position 25 has the guard
h[25] = h[6] XOR h[13] XOR e1[21]. Bit 18 of h2 is 0, so h[26] = e2[26], which
bit 6 and u2[26] fix: a constant of the row.
(g) h[16] = h[17] = 0 (PHASE); Lemma CB at bits 18 and 19 (eta[18] =
eta[19] = 0, gamma[18] = gamma[19] = 1, gamma[20] = 0) gives h[18] =
1 XOR Q[18] and h[19] = Q[19]; and if gamma[7] = 1, then u1[7] = h[6] by
the test at bit 6 and the test at bit 7 gives h[7] = 1 XOR gamma[8] XOR h[6].
On every row h[29] = 1 XOR e2[29] (bit 21 of h2 is 1), where e2[29] reads bits
2 to 9 of h, and h[20] is set by Lemma J0.

The bit values of h2 used in (e) to (g) (h2[16] = 0, h2[18] = 0 and
h2[21] = 1), h[25] = e2[1] on the high rows and the low-row value of h[26] in
(f) are facts of (J3) on the class; each is checked exhaustively for every row
of S in A15, as is the conclusion of Lemma FP itself.

**Lemma G7 (PROVED).** Write Cc = C2.c1 and Cb = C2.b1 (names of step CO) and
Z = (Y14 + Cc) XOR Cb. Every selected full valid hit, with E3.h1 = h, has

    a22  = h[6] XOR e1[22] XOR Cc[22] XOR Cb[22],
    a23  = maj(h[6] XOR e1[22], Cc[22], a22),
    h[7] = e1[23] XOR 1 XOR Cc[23] XOR Cb[23] XOR a23.                (G7)

Proof. Step CT read backwards (Lemma IP) gives Y14 = ROL(h, 16) XOR e1 and
E1.b1 = ROR(ROR(Z, 7) XOR c1, 12), so for every bit p of beta* the pattern
s = E1.b1 AND beta* has s[p] = Z[(p + 19) mod 32] XOR c1[(p + 12) mod 32].
The hit's E1 gives beta*, its tau in S and eps, so s is compatible with tau
(Lemma CAT). Over the 2,048 submasks of beta* the criterion of Lemma CAT
admits 16, 32, 8, 16, 32 and 16 patterns for the rows 175, 185, 275, 285, 385
and 685, the counts of Lemma CAT, and every one has s[3] = s[4] = 1 (finite
enumeration here). Q* fixes c1[15] = 1 and c1[16] = 0, so Z[22] =
s[3] XOR 1 = 0 and Z[23] = s[4] = 1. Bits 22 and 23 of Y14 are h[6] XOR e1[22]
and h[7] XOR e1[23]. Bit 22 of Y14 + Cc is Z[22] XOR Cb[22] = Cb[22]; with the
carry a22 into bit 22 this gives a22 as stated, and the carry into bit 23 is
a23. Bit 23 of Y14 + Cc is Z[23] XOR Cb[23] = 1 XOR Cb[23], which gives h[7].
QED. The right side of (G7) reads the context and h[6] only.

**Lemma FP (the free positions; PROVED from the facts above).** Call a
position i >= 7 *free* for the outcome j when it is not prescribed by a carry
and holds none of these constants and guards: (PHASE) at 10, 11, 16, 17 and
24; (d) at 12; (g) at 18 and 19, and at 7 when gamma[7] = 1; Lemma J0 at 20;
(P*) at 25; (f) at 26; and h[29] = 1 XOR e2[29] at 29. By the table above the
free positions are {7, 13, 15, 30} for 175020a0 and 685020a0, {13, 15, 30} for
185020a0, {9, 13, 15, 30} for 275020a0 and 385020a0 and {7, 9, 13, 15, 30} for
285020a0; with (G7) position 7 is prescribed on every row, and the free
positions F_j are {13, 15, 30} for 175020a0, 185020a0 and 685020a0 and
{9, 13, 15, 30} for the other three. They depend on the outcome, not on the
context. For every context, the joint roots of j that satisfy (G7) are at most
2^|F_j|.

Proof. Let h and h' be two such roots of one context that agree on F_j.
Positions 0 to 6 hold constants of the context ((a) to (f)), so h and h' agree
there. Let them agree below a position i >= 7. Then u1[i] is the same for
both, and so is u2[k], k = (i + 20) mod 32: for k >= 22 it follows from u2[22],
the same by (a), and from f[22] to f[k-1], which bits 2 to i - 1 of h fix;
for k <= 19 it follows from u2[0] = 0 and from f[0] to f[k-1], which bits 12
to i - 1 fix. If i is in F_j, h[i] = h'[i] by hypothesis. If i is prescribed
by a carry, Lemma CB leaves at most one value. Otherwise i holds a constant or
a guard, whose value reads only the context and bits below i: (G7) reads
h[6]; (c), (d) and (PHASE) read bits 3, 10, 11 and 12; Lemma J0 reads h[8],
u2[8] and u1[20]; (P*) reads bits 6 and 13; (f) reads bits 2 and 6 and e2[2]
(bits 12 to 14) or e2[26] (bits 2 to 6); and position 29 reads e2[29] (bits 2
to 9). So h[i] = h'[i], and by induction h = h'. The map
h -> (h[i] for i in F_j) is one to one on these roots. QED.

**Lemma K (the target equation; GPT Sol AV 2, 8.1, PROVED).** Take an
admitted base, q with b = q - W13, words j and c, and put d = c - Y11,
u = ROL16(d) XOR Y12, D = D2.c1 (= X8), U = D - q and B_j = ROL7(j). For
g = D2.a1 put S(g) = g XOR ROL16(g + q). For a word S, with the names of step
CO for this base and j, put

    d1(S) = S9 - S - IV1;   a1(S) = ROL16(d1(S));
    b1(S) = ROR12(IV5 XOR (S9 - S));   S1(S) = ROL8(S) XOR d1(S);
    S5(S) = ROR7(b1(S) XOR S9);   X0(S) = C0.a1 - X4 - a1(S) + IV1 + IV5;
    d0(S) = ROL8(X15) XOR X0(S);   c0(S) = S10 + d0(S);
    x(S) = ROR7(ROR12(S5(S) XOR c0(S)) XOR (c0(S) + X15));
    aC(S) = X1 + x(S) + S1(S) - a1(S) - b1(S);
    bC(S) = ROR12(x(S) XOR (X9 + ROR16(X13 XOR aC(S))));
    F_j(S) = X1 + x(S) - a1(S) - b1(S) + bC(S) - S6,

and R_j(g) = U - (ROL12(B_j XOR (U - g)) XOR IV4). Then (i) for every g,
step CO gives Y1 + w12 = R_j(g) - S2 - S7 + F_j(S(g)); (ii) for a word a, the
trial (base, j, g, c) has E1.a2 = a exactly when
R_j(g) = k + S2 + S7 - F_j(S(g)), with k = u - (ROL12(a - u - w5) XOR c);
(iii) R_j is a permutation with inverse
R_j^-1(r) = U - (B_j XOR ROR12((U - r) XOR IV4)); (iv) for q in
{0, 80000000}, S(g) takes exactly the 2^16 values
S = (s16 OR (s16 << 16)) XOR ROL16(q), each on 2^16 words g. So for each such
S at most one g has S(g) = S and E1.a2 = a, namely
R_j^-1(k + S2 + S7 - F_j(S)) when it satisfies S(g) = S, and every such g has
its unique S.

Proof. (i) With X13 = 0, step CO gives D2.d1 = X2 = g + q,
S13 = ROL16(g + q) XOR g = S(g), S8 = D - (g + q) = U - g,
K0.b1 = B_j XOR S8, K0.c1 = ROL12(K0.b1) XOR IV4, S12 = S8 - K0.c1, and, with
D1.d1 = 0, D1.a1 = S12. With S = S13 its lines for K1.c1, K1.d1, K1.a1, K1.b1,
w2, X0, D0.d1, D0.c1, D0.b1, X10, X5, S1, S5, w3, C1.a1, C1.d1, C1.c1 and
C1.b1 give K1.d1 = d1(S), K1.a1 = a1(S), K1.b1 = b1(S), S1 = S1(S),
S5 = S5(S), X0 = X0(S), D0.d1 = d0(S), D0.c1 = c0(S), X5 = x(S),
C1.a1 = aC(S) and C1.b1 = bC(S); then w10 = D1.a1 - S1 - S6 gives
Y1 = C1.a1 + C1.b1 + w10 = F_j(S) + S12, and w12 = g - S2 - S7, so
Y1 + w12 = F_j(S) + (U - g) - (ROL12(B_j XOR (U - g)) XOR IV4) + g - S2 - S7.
(ii) In step CT, E1.a1 = u, Y6 = u - Y1 - w12, E1.b1 = ROR12(Y6 XOR c) and
E1.a2 = u + E1.b1 + w5, so E1.a2 = a exactly when
Y6 = ROL12(a - u - w5) XOR c, that is Y1 + w12 = k; apply (i). (iii) R_j is a
composition of translations, XORs and a rotation; solve for g. (iv) Adding 0
or 80000000 is an XOR with it, so S(g) = g XOR ROL16(g) XOR ROL16(q), and for
the halves (gh, gl) of g, g XOR ROL16(g) = (gh XOR gl) * 00010001. QED.

**One query (GPT Sol AV 22.2, 25.4, 31.2, 31.3, PROVED).** Draw ONE fresh
uniform 256-bit word with disjoint fields: a 27-bit canonical low index, a
16-bit prefix-image index s16, the 29 free bits of t = S3 + j (all bits but
27, 28 and 31) and eight four-bit digits; 104 bits in all. Take the first
digit r < 13; if none of the eight is below 13 the query fails, with no retry.
Read the canonical record (c, z_local, s, tau) at index (r << 27) OR
low_index, with a = (c - Y11) XOR ROL8(z_local), and put

    d = c - Y11;   u = ROL16(d) XOR Y12;   Cb = a - u + K2.a1 + K2.b1.

*The cone (GPT Sol AV 15.1, 16.1).* For a word j, the lines of step CO that
vary with j are, in order (D1.c1 = S11 on the chart):

    a3 = D3.a1 = S3 + j;   b3 = D3.b1 = X3 - a3;   X9 = ROL7(X4) XOR b3;
    c3 = D3.c1 = ROL12(b3) XOR j;   X14 = X9 - c3;
    d3 = D3.d1 = ROL8(X14) XOR X3;   S9 = c3 - d3;   S14 = ROL16(d3) XOR a3;
    S10 = K2.c1 + S14;   S2 = ROL8(S14) XOR K2.d1;   S6 = ROR7(K2.b1 XOR S10);
    D1.b1 = ROR12(S6 XOR S11);   X6 = ROR7(D1.b1 XOR X11);
    w5 = S2 - K2.a1 - K2.b1.

Substituting, S2 = x XOR ROL8(a3) XOR ROL24(X3) XOR K2.d1 with
x = X14 = (ROL7(X4) XOR b3) - (ROL12(b3) XOR j), and
b_E1 := a - u - w5 = Cb - S2.

*Three-hole completion of j (GPT Sol AV 22.3, 25.4).* With bits 27, 28 and 31
of t set to 0, for i = 3, 4, 7 in this order compute S2 from t (j = t - S3)
and set bit i + 24 of t to bit i of (Cb - S2) XOR s; then j = t - S3. Bit i
of S2 is x_i XOR t_(i+24) XOR (ROL24(X3) XOR K2.d1)_i, and x_i reads t only
through bit i + 20 (b3 = X3 - t, bit i of ROL12(b3) is bit i + 20 of b3, and
j = t - S3); so setting bit i + 24 toggles bit i of S2, and with it bit i of
b_E1 = Cb - S2, and changes no lower bit of S2 and no bit already set. Every
choice of the 29 bits has exactly one completion, after which bits 3, 4 and 7
of b_E1, the bits of beta below bit 8, equal those of s. So j is uniform on
the 2^29 words with that property, an event of probability 1/8 for every base
and record, and the j of a hit is the completion of its own 29 bits.

*Orientation (GPT Sol AV 31.2).* Under T31, u changes by XOR 00008000, so Cb
and b_E1 change by 2^31 plus or minus 2^15: their low 15 bits are unchanged
and bit 15 of b_E1 is toggled. The completion reads only bits 3, 4 and 7, so
both orientations use the same j and the same 29 free bits. Put
m15 = ((b_E1 XOR s) >> 15) AND 1; when m15 = 1, apply T31 to (c, d, a) in the
query's scratch (never the catalog) and recompute u and b_E1. This picks the
unique orientation with bit 15 of b_E1 equal to bit 15 of s. Every selected
full valid hit already satisfies that condition, and its canonical pair, its
29 free bits and its prefix index are unique, so the procedure recovers
exactly that hit; nothing is asserted about the other orientation.

Then reject unless b_E1 AND beta = s; with k = u - (ROL12(b_E1) XOR c),
S = (s16 OR (s16 << 16)) XOR ROL16(q) and target = k + S2 + S7 - F_j(S)
(F_j(S) computed directly at the one point S, no table), put

    g = R_j^-1(target) = U - (B_j XOR ROR12((U - target) XOR IV4));

keep g only if g XOR ROL16(g + q) = S; then certify the candidate (below),
rejecting a wrong outcome, class, cube, q, pin or t = 0. By Lemma K this g is
the only word with prefix image S for which the trial has E1.a2 = a, so at
most ONE candidate is certified per query.

**Yield and cap (GPT Sol AV 31.3, PROVED).** With sigma13 = 1 - (3/16)^8 =
4,294,960,735 / 2^32, every r in 0..12 has probability sigma13 / 13 and every
canonical record sigma13 / Ncan, independent of the prefix and free-bit
fields. Every full valid hit has its unique canonical record (Lemmas CAT and
T31 and the orientation), its unique prefix S (Lemma K) and the 29 free bits
of its t, and the query that draws these three certifies it, so the success
probability of one query on base V is

    p(V) = sigma13 * G(V) / (13 * 2^27 * 2^16 * 2^29)
         = sigma13 * G(V) / (13 * 2^72),
    E p = kappa * mu_raw,  kappa = sigma13 * 8192 / 13 = 630.15288352966...,
    p(V) <= p* = sigma13 / 104,

the cap from G(V) <= 2^69 (Lemma GC).

**Lemma V (the certificate of a root; from the text of our counter search,
restated).** Fix a trial of Section 8 with c1 in Q* and an outcome j of beta*,
and let h be E3.h1 on A. Put sigma_j = tau_j XOR ROR(tau_j, 1),
theta_j = ROL(sigma_j, 12), mu = ROR(eta XOR eps, 8), and let g = E3.g1,
f = E3.f1, E = E3.e2 on A. The trial has R = 0 with E1 outcome j exactly when
E1 on A and on B gives the XOR differences tau_j and eps = 6e21be55 of its a
and c outputs and

    J1: g XOR (Y9 + (h XOR eta)) = theta_j;
    J2: E XOR ((E - f) + DY3 + (f XOR sigma_j)) = eps;
    J3: H2 = ROR(h XOR E, 8),
        (g + H2) XOR ((g XOR theta_j) + (H2 XOR mu)) = tau_j,

all sums normalized modulo 2^32.

Proof. Write tau, eps and beta for the XOR differences between A and B of E1's
a output, c output and first-half b value, and eta, psi, tau' and eps' for
those of E3's first-half d and b values and its c and a outputs. beta = beta*
because c1 is in Q* (Theorem C (iv)), and eta = 830303cf (Theorem C (iii)). By
3.3, R is formed from o[1] = Z[1] XOR Z[9], o[3] = Z[3] XOR Z[11],
o[4] = Z[4] XOR Z[12] and o[6] = Z[6] XOR Z[14], where Z[1], Z[6], Z[11] and
Z[12] are the a, b, c and d outputs of E1 and Z[3], Z[4], Z[9] and Z[14] those
of E3. The first two values of E1 are the same for A and B, so its d and b
outputs differ by ROR(tau, 8) and ROR(beta XOR eps, 7); by the last three
assignments of E3, its b and d outputs differ by ROR(psi XOR tau', 7) and
ROR(eta XOR eps', 8). So R = 0 exactly when tau' = tau, eps' = eps,
psi = tau XOR ROR(tau, 1) and eta = eps XOR ROL(beta XOR eps, 1); for outcome
j the last holds (A3). With h' = h XOR eta, g' = Y9 + h' and
f' = ROR(y XOR g', 12), psi = f XOR f' = ROR(g XOR g', 12), so psi = sigma_j
exactly when J1 holds. Then f' = f XOR sigma_j, and E3's a output on B is
(omega + DY3) + f' with omega = E - f, so eps' = eps exactly when J2 holds.
Then E3's d output on B is ROR(h XOR eta XOR E XOR eps, 8) = H2 XOR mu and
g' = g XOR theta_j, so tau' = tau_j exactly when J3 holds. QED.

**Complete certification (GPT Sol AV 38.1, PROVED).** Reconstruct the ordinary
inputs by the 17 formulas of the chart (A4) and evaluate all 77 CO and 16 CT
assignments of Section 8 in their printed order, modulo 2^32. Test the eight
obligations

    y in C13;  c in Q*;  t != 0;  q in {0, 80000000};
    X13 = 0;  D1.d1 = 0;  actual E1.a2 = a;  (actual E1.b1 AND beta) = s.

The record row, c and its orientation are already fixed by the paid catalog
dispatch. With d = c - Y11, the last two tests and the catalog give the ACTUAL
E1 values

    a_B = a - 8 + beta - 2 s;
    c2_A = c + ROR8(d XOR a);   c2_B = c + DY11 + ROR8(d XOR a_B),

since b1_B = b1_A XOR beta, (b1_A XOR beta) - b1_A = beta - 2 s, and the first
E1 a and d values agree on both sides. So the record identities give the
actual E1 differences tau and eps = 6e21be55, not a locally compatible
pattern. Then test J1, J2 and J3 on the actual E3 values h = E3.h1, g = E3.g1,
f = E3.f1, E = E3.e2.

Proof. Lemma CT gives every assignment, constant pin, normal form and the
actual c; the cube and the class give beta* and eta and Theorem C's agreement
on chaining-value words 0, 2, 5 and 7. With the actual E1 differences, Lemma V
turns J1 to J3 into R = 0, so all eight last-chunk chaining-value words agree;
with t != 0, Lemma TR makes the pair an ordinary collision of two complete
messages. Conversely every full valid hit passes all the tests. Literal
padding, the lengths 55 and 63, flags 3, the second counter word 0 and the
round-0 pins follow from Lemma CT, Theorem C and the message construction, and
need no per-candidate forward compression. After a hit the two messages are
materialized and hashed once, inside the 2^38 term of A10; no failed candidate
receives a forward hash or a message materialization. QED.

**Query charge (GPT Sol AV 38.2, 38.3, PROVED).** Every query is charged its
full cap, including digit failure, compatibility or target failure, t = 0 and
failed certification:

| Query item, complete query | Units |
|---|---:|
| Fresh coin, index and field extraction | 128 |
| Record decode, d, a, u, Cb, b_E1, beta test and k | 64 |
| The cone of 14 j-varying words | 512 |
| Direct F_j(S) point evaluation | 512 |
| R inverse, target and prefix checks | 64 |
| Three-hole j completion | 256 |
| Dispatch | 64 |
| T31 orientation | 32 |
| Complete certification | 1536 |
| Total, C38 | 3168 |

Every unit is a primitive operation, load, store, mask or branch, with at most
16 registers (GPT Sol AV 16.1, 22.4, 25.4, 28.2, 31.4, 38.2). Coin: one coin,
six field extractions, at most 48 operations for the eight digits, two for the
index, at most 16 for the prefix and t deposits and 32 for inputs and
dispatch: 105 <= 128. Record and target words: one record load, at most 8
field extractions and the seven formulas d, a, u, Cb, b_E1, the beta test and
k, with c, d, a, u and s kept in registers: at most 48 <= 64. Cone: 14
formulas at <= 12 units with their loads and stores (168), plus 256 for j
addressing, cache loads, spills and control: 424 <= 512. F_j(S): the 12
formulas of Lemma K, each with at most six operands and two rotations, at most
32 units each: 384 <= 512. R inverse, target and prefix test: at most 30
operations and 12 operand loads: <= 64. Three-hole completion: three
recomputations of S2 from t at <= 56 each, plus 64 for setup, masks and
stores: 232 <= 256. The orientation block is m15 (3 units), the mask m15 << 31
(1), three XORs on c, d, a (3), the mask m15 << 15 and the XOR on u (2) and
b_E1 recomputed (3): 12 primitive units, plus 10 for five computed scratch
addresses and stores and 3 of dispatch, 25 <= 32.

*Certification ledger (GPT Sol AV 38.2).* All named values sit in fixed query scratch
slots. A normalized two-operand sum or difference costs 8 (four addressed-load
primitives, one arithmetic operation, one AND with the 32-bit mask, two
addressed-store primitives); a single-operand 32-bit rotation costs 8 (two
loads, four shift/OR/mask, two stores); a three-operand sum or difference, or
a two-operand XOR or rotation, costs 11. Every constant operand is charged as
an addressed load. The 23 CO lines at 8 are, in printed order, C0.c1, K3.c1,
S15, D3.a1, D3.b1, X13, X14, S9, Y12, K1.c1, K1.d1, K1.a1, S10, D0.c1, X10,
D1.c1, D1.d1, S8, S12, C1.c1, C2.c1, K0.d1, Y9 (K1.a1 the lone rotation); the
other 54 CO lines (16 three-operand sums or differences, 38 XORs or rotations)
cost 11: CO = 23 * 8 + 54 * 11 = 778. In CT, E1.d1, Y14 and E3.g1 cost 8,
eleven lines cost 11, E3.h1 costs 15 (normalized before its rotation) and
E3.e2 costs 14: CT = 24 + 121 + 15 + 14 = 174, and CO + CT = 952. The 17
chart formulas cost 8 for the four sums or differences K3.c1, S15, D3.a1 and
D3.b1; 11 for X8, S7, K3.a1, K3.d1, K3.b1, S11, S3, X9, Y0 and Y12; 15 for
X4 and C0.a1 (a sum or difference inside an XOR with a rotation); and 18 for
y: 4 * 8 + 10 * 11 + 2 * 15 + 18 = 190 <= 192.

| Certification item | Units |
|---|---:|
| The 17 special-chart formulas (literal total 190) | 192 |
| All 77 CO and 16 CT assignments | 952 |
| Eight legality and record tests, <= 16 each | 128 |
| J1, J2, J3, <= 48 each (literal 20, 24, 32) | 144 |
| Inputs, constants, mask/base, restoration, dispatch (literal 92) | 96 |
| Subtotal | 1512 |
| Certification cap | 1536 |

The interface pays nine initial-word copies (36), four K2 constant writes (8),
four fixed message-word writes (8), mask and base setup (8) and 32 units of
restore, dispatch and return. One CO/CT line uses at most four operands, the
mask and address or rotation scratch; J3 has at most 14 live values with mask,
pointers and counters, so 16 registers suffice, every scratch read and write
is paid, and no free spill or SIMD instruction is assumed. Each admitted base
also pays 1024 units once for its j-independent cache: the 14 chart formulas
without j and X12, X1 = ROL8(X12), C0.c1, w7, U and Y3 + y, at most 20
formulas at <= 18 units (360), with constant loads and stores, <= 1024.

## A8. Shared class landings: m queries on one frame

By the chart (A4) y does not depend on j, so one admitted base supports all
2^32 words j and the class test is paid once per base. The dependence between
queries on one base is handled exactly, with no independence premise:

**Lemma AR (cluster retention; GPT Sol AV 28.3, 31.5, PROVED).** Let m queries
use one base V with independent fresh coins. Then, with p* = sigma13 / 104
and a = 1 - p*,

    q_m = E_V[1 - (1 - p(V))^m] >= (E p / p*) (1 - a^m)
        = 65536 * mu_raw * (1 - a^m).

Proof. For fixed m the map p -> 1 - (1 - p)^m is concave on [0, p*] and is 0
at 0, so it lies above its chord: 1 - (1 - p)^m >= (p / p*)(1 - a^m) for
0 <= p <= p*. Apply it at p = p(V) <= p* and average over V. Finally
kappa / p* = (sigma13 * 8192 / 13) * (104 / sigma13) = 65536. QED.

The sigma13 factor cancels in the ratio and remains in a. Within one query the
hit count is a 0/1 indicator, so no within-query factorial moment enters.

**The choice m = 11 (GPT Sol AV 38.3, PROVED, recomputed).** For C = 3168,
B = 1024 + 1024 / r0 and P = 104 / sigma13, the large-run coefficient
f(m) = (C m + B) / (1 - a^m) changes sign of f(m+1) - f(m) where
T_m = a^m (P + m + B/C) crosses P; T_m strictly decreases. With sigma13 = n/d,
n = 4,294,960,735, d = 2^32, b = B/C = 2048/3168 at r0 = 1, the integer
comparison of (104 d - n)^m * (104 d * 3168 + (3168 m + 2048) n) with
(104 d)^m * 104 d * 3168 gives "greater" at m = 10 and "less" at m = 11
(recomputed here in exact integers), so m = 11 is the global integer minimum
of that coefficient. The finite budgets below use their actual ceilings.

## A9. The algorithm and its halts

Inputs fixed in advance: mu0 = (2^21 - 1) * 98,937,639,497 / 2^149 (the
declared lower on mu_raw, H1), r0 = 1 (the declared lower on rbar_C, H2),
m = 11, a = 1 - sigma13 / 104. Budgets:

    N    = ceil(1 / (131072 * mu0 * (1 - a^11)))
         = 260,247,967,857,566,502,269,693;
    s    = 8 + ceil_sqrt(64 + 16 N) = 2,040,580,183,613;
    Bsam = ceil(2 (N + s) / r0) = 520,495,935,719,214,164,906,612.

1. Read the advice record ADV of A3 (not computed here; the selection
   procedure SEL that found it is charged in full in A10). Build the canonical
   catalog once (at most 2^46 units) and its compact layout (at most 2^34),
   the query metadata (2^16) and the packed sampler/record metadata (8192).
2. Run at most Bsam sampler batches of four proposals (A5, A6). Stream at most
   four admitted bases at a time; keep the first N admitted bases in
   chronological order; for each kept base pay its 1024-unit cache and run 11
   queries (A7), each with its own fresh coin.
3. Stop with the pair at the first certified full valid hit. Halt with failure
   when Bsam batches are spent or N bases have run their 11 queries.

*Success (GPT Sol AV 28.3, 31.5; PROVED from H1 and H2).* By Lemma S and H2
the 4 Bsam proposals are iid, each admitted with probability rbar_C / 8 >=
r0 / 8, so the admitted count has mean at least N + s, and the Chernoff lower
tail gives Pr(fewer than N admitted) <= exp(-s^2 / (2(N + s))) <= exp(-8),
since s >= L + sqrt(L^2 + 2 N L) for L = 8. Given N admitted bases, they are
iid uniform on the A admitted bases (Lemma S), so the probability
that none of their 11-query clusters hits is (1 - q_11)^N <= exp(-N q_11) <=
exp(-1/2), using N q_11 >= N * 65536 * mu0 * (1 - a^11) >= 1/2. Hence

    success >= 1 - exp(-1/2) - exp(-8) = 0.39313... > 0.39.

## A10. Charged time

Every rejected proposal, catalog failure, failed query, query certification,
base cache, once-only build and the final messages are charged at their
budgets, and the selection procedure SEL below at its cap S_old:

    O = S_old + 2^46 + 2^34 + 2^16 + 8192
        + 512 Bsam + (1024 + 3168 * 11) N + 8,
    T <= O / 430 + 2^38,

with 2^38 target compressions for the two final messages (each below 2^42
bytes). The exact pieces:

    2^46 + 2^34 + 2^16 + 8192 + 8 = 70,385,924,120,584
    512 Bsam                      = 266,493,919,088,237,652,432,185,344
    35,872 N                      = 9,335,615,102,986,625,569,418,427,296
    O without S_old               = 9,602,109,022,074,933,607,774,733,224
    S_old                         = 8,882,224,365,081,579,520

Then

    430 T <= O_without + S_old + 430 * 2^38
          = 9,602,109,030,957,276,170,356,298,664 =: NUM,
    log2 T <= 84.2072170302.

**Claim and integer check.** time_log2 = 84.2073, the bound rounded UP at the
fourth decimal. Exactly, 430^10000 * 2^842072 < NUM^10000 < 430^10000 *
2^842073: the right inequality gives T^10000 < 2^(84.2073 * 10000), and the
left one shows that 84.2072 would be too low. (Both sides have 929,555 bits;
recomputed here in Python integers.) The once-only part,
(S_old + 2^46 + 2^34 + 2^16 + 8192) / 430, is below 2^54.1975 target
compressions and is included in T: preprocessing_log2 = 55.

**The selection procedure SEL.** The words ADV[0..16] of A3 (the six
constants, eta, beta*, the mask and value of the cube of beta*, the six taus of
S and eps) were found by a solver search and one count per model, which the
algorithm of A9 does not contain. This section writes that search as a
procedure, SEL, and charges its whole cost as preprocessing, included in T.
The cost model charges any search omitted from the algorithm; SEL is that
search, and its whole capped cost is charged. The charge is a bound by
construction: every search of SEL runs over a range stated here, and every run
of a program in SEL halts as soon as it has executed a stated number of
primitive word operations, its cap, or holds 2^34 bytes; a run that halts so
returns nothing, and SEL goes on. Operations are machine units, 430 to the
target compression. SEL runs two programs of the participant that are not in
the package: the solver kissat, on instances made by a generator of the
participant, and an exact counter, which computes in integer arithmetic the
part of one beta in the rate of the class of a given eta (the counter that
gives 67,633,152 * 2^11 for S in H1 (i)); a run of the counter whose part
would be 2^192 or more counts as one that reaches its cap.

*Step 1, the pinned call (solver runs).* For each of the 116 runs of the
participant's solver log for this search (51 runs for the lengths 55 and 63,
the other 65 for nine other variants of the instance; bounds 97 to 118; logged
seeds), build the instance of the run and run kissat on it with the logged
seed, the two together under a cap of 2^56 operations. For the lengths 55 and
63 the instance is: the call C3 for both messages with equal b and d outputs,
the two words w4 related as the length cancellation prescribes for the XOR 8
of the lengths, the top byte of word 13 zero, E1 and E3 for both messages, a
zero residual, and a bound on the number of bit positions, bit 31 excepted, at
which a difference is active in six additions of E1 and E3. A run that finds a
model returns six constants X3, X7, X11, X15, W4, W13 and the values of a
solution, among them its Y4 and its beta. Cost: at most 116 * 2^56 < 2^62.86
operations.

*Step 2, the constants, the class and beta* (one count per model).* For each
model of step 1, compute Y3 and Y3' by C3 from its constants, its class
eta = ROR((Y3 + Y4) XOR (Y3' + Y4), 16) from the Y4 of its solution and its
beta from the c1 of its solution, and with the counter the part of that beta
in the rate of the class of that eta, with a cap of 2^52. Output the six
constants, the eta and the beta of the model with the largest part, the first
in the order of the log if parts are equal. Cost: at most
116 * (2^52 + 2^10) < 2^58.86 operations.

*Step 3, the cube, the outcomes and S.* With DY11 = Y11' - Y11 for the output
of step 2, form the mask ROL(beta, 12) AND 7fffffff and the value
(ROL(beta, 12) - DY11) / 2 of the cube of the words c1 that give beta (proof of
Theorem C (iv)), and the outcomes (tau, eps) of beta whose count in step 2 is
not zero; for beta* these are fourteen, all with eps = 6e21be55. Then, for each
of the 16,383 nonempty sets S of these outcomes, compute in integers the
numerator O(S) of the ledger of our ordinary counter search with the outcome
set S (entry 415e792c: an integer formula in the counts of step 2, the exact
share of the outer filter for S and the solver caps for S), and output the S
with the least O(S), the first in increasing order of its mask if two are
equal. Step 3 and the bookkeeping of SEL run under a cap of 2^50 operations.

ADV is the output of SEL restricted to its words: the constants, eta and beta*
of step 2, the mask, the value and eps of step 3 and the taus of its S. The two
q of ADV[17..18] are selected by no search: they are the two words q with
g + q = g XOR q for every word g (Lemma K (iv)), since
g + q = (g XOR q) + 2 (g AND q) modulo 2^32, which equals g XOR q for every g
exactly when q has no bit below bit 31.

**The bound.** Steps 1 to 3 cost at most

    S_old = 116 * 2^56 + 116 * (2^52 + 2^10) + 2^50 = 8,882,224,365,081,579,520

operations, below 2^62.946 (in integers S_old^1000 < 2^62946), and so below
2^54.198 target compressions (S_old^1000 < 430^1000 * 2^54198). The whole of
S_old is in T. It bounds SEL as defined, whatever the two programs do inside
and whatever they return, because every run halts at its cap and every loop has
the range stated. SEL is not a premise of this package, and no heuristic is
declared for it.

*What rests on records.* The bound rests on no record. That SEL returns
exactly the words of ADV[0..16] rests on the participant's records: for S, on
an exact comparison of the 16,383 sets; for the rest, on the participant's
solver log, by which the run for the lengths 55 and 63 with bound 104 and seed
506 found these constants after 4,770 seconds, with a solution of class
830303cf and beta 18b0e098, and on an exact integer recount, by the
participant's counter on the whole class of each instance, of all 65 distinct
instances that the runs of the log returned with a model, in which these
constants have the part 71,698,432, the largest, and the next is 13,107,200.
Every run of the log stopped within 9,010.5 seconds on one processor core and
every recount within 320 seconds. The log does not fix every instance: some
runs excluded pairs that runs finished before them had found, and 32 runs were
stopped from outside without a record of the cause. So the records certify a
historical run of the solver, not a replay with operation caps, and the
generator of the instances, the solver log and the counter are not in the
package. If a record were wrong, SEL could return other words or none; its
cost would stay within the bound, and the analysis uses only the stated words
of ADV (Lemma UA).

*Memory.* Streaming keeps at most four admitted bases; the canonical catalog is
13 * 2^32 bytes at one 256-bit slot per record, below 2^36 bytes; with
scratch, the search holds fewer than 2^38 bytes. Every program run of SEL halts
when it holds 2^34 bytes, and SEL runs one program at a time; its own data stay
below 2^20 bytes. The output, the two messages of a found pair with their
digests, takes fewer than 2^43 bytes. Held at once, these total below
2^43 + 2^38 + 2^35 < 2^44: memory_log2_bytes = 44.

## A11. Premises and their evidence status

| Item | Status | Where |
|---|---|---|
| Counter construction, tree lemma, counter solve, t = 0 rule | PROVED, exact | Sections 7, 8 (Part B) |
| Special-frame chart, frame equation, 64-seed inverse, R_frame <= 64 | PROVED | A4, A5 |
| Class bits, projection inverse, byte completion; exact uniform sampler admitting with probability rbar_C / 8; A <= 2^87, rbar_C <= 8 | PROVED (Lemma S) | A5 |
| Four-lane batch <= 512 units | PROVED | A6 |
| Local E1 catalog: unique record per hit, 13 * 2^28 selected records, build <= 2^46 | PROVED (Lemma CAT; its table is a finite exact count) | A7 |
| T31 involution, canonical catalog of 13 * 2^27 records, orientation | PROVED | A7 |
| At most 32 hits per context | PROVED (Lemma GC; free positions by Lemmas CB, J0, G7 and FP; (PHASE), (P*) and the bit facts used checked exhaustively) | A7, A15 |
| Target equation, one candidate per prefix image | PROVED (Lemma K) | A7 |
| Query yield identity, cap p* = sigma13/104 | PROVED | A7 |
| Lemma V and the local complete certification | PROVED | A7 |
| Complete query <= 3168 units, certification <= 1536, base cache <= 1024 | PROVED, block by block | A7 |
| Cluster retention q_m >= 65536 mu_raw (1 - a^m), m = 11 | PROVED | A8 |
| Halts, underfill, success > 0.39 given H1, H2 | PROVED | A9 |
| H1-special-full-mean: mu_raw >= mu0 | DECLARED, score-critical; partial-event evidence only | A11.1 |
| H2-frame-balance: rbar_C13 >= 1 on the two-q, flag-3 chart | DECLARED, score-critical; measured near 1 | A11.2 |
| Advice record ADV (76 bytes) and the properties of ADV that the analysis uses (Lemma UA) | STATED in A3; (a) to (g) proved here | A3 |
| Selection procedure SEL, every run capped; cost <= S_old, charged in T | PROVED bound by construction; not a premise | A10 |

**A11.1 H1-special-full-mean (score-critical).** mu_raw >= mu0 =
(2^21 - 1) * 98,937,639,497 / 2^149 (about 2^-91.474), on exactly the chart of
A4 to A7: flags 3, q in {0, 80000000}, class C13, Q*, outcomes S. It has three
parts. (i) The ordinary first-moment lower of the chunk-counter construction:
mu_ordinary >= (2^21 - 1) * 98,937,639,497 / (2^21 * 2^128), five sevenths of
the model's conditional count of the six outcomes on the class, rounded down;
declared, not proved, in the ordinary counter search, and declared here anew.
(ii) Transfer at theta0 = 1: mu_special >= theta0 * mu_ordinary, where
mu_special = mu_raw. (iii) Its weakest aggregate form (GPT Sol AV 26.4, 27.2):
G * 2^179 >= theta0 * A * T1, where T1 counts actual ordinary full valid hits
and G actual special ones. With H the partial pass event (the outer filter of
Section 8) and n(O) the number of hitting c in Q* of an outer context O,
n(O) <= 32 (Lemma GC) and n(O) = 0 off H (Lemma F); hence
mu_i = Pr_i(H) * E_i[n | H] / 2^21 for each law i, and the ratio
mu_special / mu_ordinary is the product of the pass-share ratio and the
conditional tail ratio; the participant measurements of A12 concern the first
factor only. A proof-only lower is ZERO: the special
chart is a fraction pi = A / 2^179 <= 2^-92 of the ordinary coordinate space
(Lemma S), and the complement can hold all the ordinary mass: Lemma GC caps
its mean only at 2^-16, far above mu0. So H1 is a physical premise, not a
consequence of the chart's uniformity.

**A11.2 H2-frame-balance (score-critical).** rbar_C13 >= r0 = 1 on b = q -
W13, q in {0, 80000000}, flags 3. Proved: rbar_C <= 8 (Lemma S) and, for every
(b, z, f), the sum over all y of R_frame is 2^32 (Lemma AI). A full weighted
class balance over C13 is not proved.

## A12. Measured evidence (participant measurements, untrusted)

These are participant measurements on the participant's own hardware and code;
the organizer has not run them, and they are not a proof. They are cited from
the participant's files fifties/rates/RATES.md and
fifties/av11/results_main_table.txt.

*Frame landing and multiplicity (results_main_table.txt).* With n about 1.7 * 10^13 (q =
0) and 2.66 * 10^13 (q = 80000000) samples per q, flag 11: p_land on C13 =
1.220717e-4 and 1.220675e-4, both 2^-13.0000; rbar = 1.00000 for C13 and C15
at both q; P(R_frame = 0) = 0.2970; largest R_frame seen 10; combined C13
p_land = 1.220692e-4 (2^-13.0000). These rows are for the ROOT flags 11, not
the flags 3 of this path.

*Partial events, special against ordinary (RATES.md).* Independent check,
flags 3, frames from a rejection sampler with the first 150 confirmed as roots:
filter pass share on special frames with b uniform 0.00099148 (se 5.0e-7)
against ordinary 0.00099155 (se 9.6e-8) and the exact share 0.00099146, ratio
0.99993; with b fixed at q = 0 and q = 80000000, 0.00099085 and 0.00099091 (se
9.9e-7). Filter condition (2) on special frames 0.0544168 (se 3.6e-6) against
exact 0.0544161. Main runs (ordinary fresh, special fresh, special j-reuse):
E3 condition (1) 0.0276844 / 0.0276860 / 0.0276813; filter pass 0.0009916 /
0.0009940 / 0.0009920; pre-check pass 0.0002481 / 0.0002482 / 0.0002481;
j-reuse design effects 1.0000 within 2e-4; sampler rbar 1.0000066 and
0.9999983. Relaxed-solver roots: 5 in 100,000 passing steps in each
population; with (G7) and the pre-check, 1 in 100,000 in each.

*Limits.* They measure a PARTIAL pass event, not the full valid hit (about
2^-91 per trial, unobservable); the solver counts are sparse (mean 5e-5, se
about 2.6e-5 and 2.2e-5); the pre-check runs used fresh random C/B words, not
the physical ones; the main special run has b over all 32-bit words, not the
two q values; and the j-reuse cluster law is not the catalog query's law. They
motivate H1 and H2; they do not prove them.

## A13. Open items

Every step of Part A is stated and proved in this document. The table of
Lemma CAT is the output of the finite recurrence stated there, and the bit
facts of the joint roots in A7 are checked by the program of A15, which uses
the public solver kissat. That SEL returns the
words of ADV rests on the participant's records (A10); its charge does not.
The submitted
program does not implement or run this path; no implementation of the frame
inverse, the sampler or the query has been run by the organizer, and the unit
allowances of A5 to A7 are operation bounds, not counts of an implementation.

## A14. Credit

- GPT Sol (OpenAI): the path of Part A with its lemmas, ledgers and price
  (answer AV; the local E1 catalog of answer AK; the joint-solver counts of
  answers AO to AX), restated here.
- The participant: Lemma V, the arrangement, the selection procedure SEL, the
  check of A15, the exact recomputation and the integer check, and the
  measurement runs of A12.
- Part B: our earlier chunk-counter texts, which keep their own credits.

## A15. The exhaustive check of the joint-root facts

The program below checks, for each outcome of S, every bit fact of A7 on which
Lemma FP rests: the lines of (PHASE) and (P*), h2[0] = 0 (Lemma J0),
h2[16] = 0, h2[18] = 0, h2[21] = 1, h[25] = e2[1] on the high rows and the
value of h[26] on the low rows. For each it writes a CNF of (J1), (J2) and
(J3) on 32-bit words Q, w8, e1 and h, with the class condition
(e1 AND 03cf8303) = 030c0303, y = e1 - Y3, and the negation of the fact, and
runs the solver kissat on it. Every addition is an exact ripple-carry adder
modulo 2^32 and every XOR an exact Tseitin XOR, so UNSAT means that the fact
holds for every word Q = Y9, every w8, every member y and every joint root, a
superset of the physical contexts. The program also checks the conclusion of
Lemma FP directly: two distinct joint roots of one context, both meeting (G7)
with Cc and Cb free words, equal on F_j, give UNSAT; and, as a control, that
joint roots exist (SAT). Run with kissat 4.0.3 as `python3 -B jrcheck.py`, it
printed UNSAT for all 90 facts and caps and SAT for the six controls, and
"ALL AS STATED", in about 3 seconds.

```python
#!/usr/bin/env python3
# Exhaustive check of the joint-root facts of proof.md A7 (Lemma FP) with a SAT solver.
# For each outcome of S and each fact: CNF of (J1), (J2), (J3), the class condition on
# e1 = Y3 + y and the NEGATION of the fact; "UNSAT" means the fact holds for every word
# Q = Y9, every w8, every member y and every joint root h. "cap": two DISTINCT joint roots
# of one context, both meeting (G7) (Cc, Cb free words), equal on F_j. "exists": no
# negation (a joint root exists; SAT expected). Needs kissat on PATH. Run: python3 -B jrcheck.py
import os, subprocess, tempfile
M = 0xffffffff
def ror(x, r): return ((x >> r) | (x << (32 - r))) & M
ETA, EPS, Y3, DY3 = 0x830303cf, 0x6e21be55, 0x8127c181, 0xfdb77cfd
MU = ror(ETA ^ EPS, 8)

class CNF:
    def __init__(s): s.n, s.cl = 1, [[1]]                   # variable 1 is TRUE
    def new(s): s.n += 1; return s.n
    def word(s): return [s.new() for _ in range(32)]
    def const(s, v): return [1 if v >> i & 1 else -1 for i in range(32)]
    def xor(s, a, b):
        if abs(a) == 1: return -b if a == 1 else b
        if abs(b) == 1: return -a if b == 1 else a
        c = s.new(); s.cl += [[-a, -b, -c], [a, b, -c], [a, -b, c], [-a, b, c]]; return c
    def maj(s, a, b, c):
        o = s.new()
        s.cl += [[-a, -b, o], [-a, -c, o], [-b, -c, o], [a, b, -o], [a, c, -o], [b, c, -o]]
        return o
    def add(s, x, y):
        out, k = [], -1
        for i in range(32):
            out.append(s.xor(s.xor(x[i], y[i]), k))
            if i < 31: k = s.maj(x[i], y[i], k)
        return out
    def xw(s, x, y): return [s.xor(a, b) for a, b in zip(x, y)]
    def eq(s, x, v): s.cl += [[x[i]] if v >> i & 1 else [-x[i]] for i in range(32)]
    def X(s, *ls):
        v = ls[0]
        for l in ls[1:]: v = s.xor(v, l)
        return v
    def solve(s):
        with tempfile.NamedTemporaryFile("w", suffix=".cnf", delete=False) as f:
            f.write("p cnf %d %d\n" % (s.n, len(s.cl)))
            f.writelines(" ".join(map(str, c)) + " 0\n" for c in s.cl)
        r = subprocess.run(["kissat", "--time=600", f.name], capture_output=True, text=True).stdout
        os.unlink(f.name)
        return "UNSAT" if "s UNSATISFIABLE" in r else "SAT" if "s SATISFIABLE" in r else "UNKNOWN"

def context(c):
    Q, w8, e1 = c.word(), c.word(), c.word()
    c.cl += [[e1[i]] if 0x030c0303 >> i & 1 else [-e1[i]] for i in range(32) if 0x03cf8303 >> i & 1]
    return Q, w8, e1

def root(c, tau, Q, w8, e1, h):
    sg = tau ^ ror(tau, 1); th = ror(sg, 20)
    y = c.add(e1, c.const(-Y3 & M)); om = c.add(e1, w8); omp = c.add(om, c.const(DY3))
    g = c.add(Q, h)
    c.eq(c.xw(g, c.add(Q, c.xw(h, c.const(ETA)))), th)                        # (J1)
    f = [c.xor(y[(i + 12) % 32], g[(i + 12) % 32]) for i in range(32)]          # ROR(y XOR g, 12)
    e2 = c.add(om, f)
    c.eq(c.xw(e2, c.add(omp, c.xw(f, c.const(sg)))), EPS)                      # (J2)
    h2 = [c.xor(h[(i + 8) % 32], e2[(i + 8) % 32]) for i in range(32)]         # ROR(h XOR e2, 8)
    c.eq(c.xw(c.add(g, h2), c.add(c.xw(g, c.const(th)), c.xw(h2, c.const(MU)))), tau)  # (J3)
    return e2, h2

def g7(c, h, e1, Cc, Cb):
    x = c.xor(h[6], e1[22]); a22 = c.X(x, Cc[22], Cb[22]); a23 = c.maj(x, Cc[22], a22)
    r = c.X(e1[23], 1, Cc[23], Cb[23], a23); c.cl += [[-h[7], r], [h[7], -r]]

FACTS = {  # name: literal that is TRUE when the fact holds
    "h0=0": lambda c, h, e1, Q, e2, h2: -h[0],
    "h1=1": lambda c, h, e1, Q, e2, h2: h[1],
    "h2=1^e1_2": lambda c, h, e1, Q, e2, h2: c.X(h[2], e1[2]),
    "h10=e1_2": lambda c, h, e1, Q, e2, h2: -c.X(h[10], e1[2]),
    "h11=1^h3": lambda c, h, e1, Q, e2, h2: c.X(h[11], h[3]),
    "h16=0": lambda c, h, e1, Q, e2, h2: -h[16],
    "h17=0": lambda c, h, e1, Q, e2, h2: -h[17],
    "h24": lambda c, h, e1, Q, e2, h2: -c.X(h[24], h[3], h[12], e1[21]),
    "P*": lambda c, h, e1, Q, e2, h2: -c.X(h[6], h[13], h[25], e1[21]),
    "h2_0=0": lambda c, h, e1, Q, e2, h2: -h2[0],
    "h2_16=0": lambda c, h, e1, Q, e2, h2: -h2[16],
    "h2_18=0": lambda c, h, e1, Q, e2, h2: -h2[18],
    "h2_21=1": lambda c, h, e1, Q, e2, h2: h2[21],
}
LOW = {"h26(low)": lambda c, h, e1, Q, e2, h2: -c.X(h[26], 1, h[2], e2[2], Q[26], Q[25])}
HIGH = {"h25=e2_1(high)": lambda c, h, e1, Q, e2, h2: -c.X(h[25], e2[1])}
F = {0x175020a0: (13, 15, 30), 0x185020a0: (13, 15, 30), 0x685020a0: (13, 15, 30),
     0x275020a0: (9, 13, 15, 30), 0x285020a0: (9, 13, 15, 30), 0x385020a0: (9, 13, 15, 30)}
bad = 0
for tau in F:
    facts = dict(FACTS, **(LOW if tau in (0x175020a0, 0x275020a0) else HIGH))
    for name, fn in facts.items():
        c = CNF(); Q, w8, e1 = context(c); h = c.word(); e2, h2 = root(c, tau, Q, w8, e1, h)
        c.cl.append([-fn(c, h, e1, Q, e2, h2)]); r = c.solve(); bad += r != "UNSAT"
        print("%08x %-15s %s" % (tau, name, r))
    c = CNF(); Q, w8, e1 = context(c); Cc, Cb, h, hp = c.word(), c.word(), c.word(), c.word()
    root(c, tau, Q, w8, e1, h); root(c, tau, Q, w8, e1, hp); g7(c, h, e1, Cc, Cb); g7(c, hp, e1, Cc, Cb)
    c.cl += [p for i in F[tau] for p in ([-h[i], hp[i]], [h[i], -hp[i]])]
    c.cl.append(c.xw(h, hp)); r = c.solve(); bad += r != "UNSAT"
    print("%08x %-15s %s" % (tau, "cap", r))
    c = CNF(); Q, w8, e1 = context(c); h = c.word(); root(c, tau, Q, w8, e1, h); r = c.solve()
    bad += r != "SAT"; print("%08x %-15s %s" % (tau, "exists", r))
print("ALL AS STATED" if bad == 0 else "%d CHECKS DIFFER" % bad)
```

# PART B. The common construction

The following Sections 1 to 8 are copied from the text of our whole-class
chunk-counter search; remarks that this path does not use, participant checks
and references to the later sections of that text are removed.

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

*The same compression in a last chunk.* Sections 7 and 8 and Part A use the same
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
are written to. Arithmetic is modulo 2^32. The submitted program has steps O
and M in `outer` and `middle`, step Y in `member`, step T in `trial`.

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
here on "member" means a member of the sub-class.

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
of its trials has a zero residual. Rule A belongs to the root instance; the
path of Part A does not use it.

**6.4 The root instance and the two declared experiments.** Sections 4 to 6
build the *root instance* of the construction: its messages are single chunks
of 55 and 63 bytes, and the colliding compression is the root compression, with
counter 0 and flags 11 (Section 1). The claim of this package is made for the
*counter instance* of Sections 7 and 8 and Part A, whose messages have
1024 t + 55 and 1024 t + 63 bytes and whose colliding compression is that of
the last chunk, with counter t and flags 3. The two instances share the six
constants, Fact P, Lemmas L and H, the class and Lemma N; the sub-class, rule
A, Lemma A and the machine of 6.5 belong to the root instance and the program,
not to the path of Part A. The instances differ in the
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

- `half-collision` runs one trial of 6.1 per organizer seed: the seven words of
  a context and a member number are taken from the seed, and steps O, M, Y, T,
  S2 and S3 of Section 4 build the pair. Lemma T predicts that every pair
  agrees on digest words 0, 2, 5 and 7.
- `residual-search` runs a search of the root instance at toy scale: per
  organizer seed one context, then the members of the sub-class in the order of
  their numbers from a member number taken from the seed, at most all 131,072
  of them, stopping at the first trial whose residual (3.3) has a zero low byte
  in digest word 1. For the same context it also evaluates the four counted
  pieces of 6.5 on the program's machine and returns their counts as
  observations.

Neither experiment runs the counter construction or its batch, and neither
measures a rate of the counter search. A search of the root instance over all
contexts is not part of the claim, and this text defines no loops, ranges or
budgets for it.

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
  holds the constant STAGE_2_BUDGET; in the root instance its value has no
  influence on any output.
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
operations. Nine words
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
at 17 registers.

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

*The count in the submitted program.* The program of the two declared
experiments, experiments/halfsearch.py, contains the four pieces, the counter
construction of Section 8, the counter batch of our ordinary counter search,
and the machine that counts them, a packed word being one integer with seven
36-bit lanes. The
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
these agree with this section. The same command also runs a self-test of the
ordinary counter batch, reported under the key `counter` of the same line, and
the exit status is 0 only if that part passes as well. With N = 2,000 and
seed 1 it reports 14,000 of 14,000 lanes right and the counts of the tables
above in every case.

In the declared experiment `residual-search` the same program evaluates, per
organizer seed, one outer step, the table words of one list word, one middle
step and one batch, for that seed's context and the list position of the first
member tried, and returns the operations and loads of the two stages of the
batch, its number of right lanes and whether a lane satisfied rule A as
observations. The organizer's runner records observations as untrusted and does
not recompute them. The self-test and these observations therefore show what
the program in the package counts, and that its lanes agree with the program's
own compression of the real messages. They are a participant check, not an
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

So an outer step has 2^21 or 2^21 - 1 valid trials; the rule t != 0 drops at
most one trial in 2^21.

*The length of the messages.* Within one outer step the 2^21 members of Q* give
2^21 different values of t below 2^32 (Lemma IP). A pair found by the search
has messages of 1024 t + 55 and 1024 t + 63 bytes, shorter than 2^42 bytes. A
small t cannot be chosen: it is the value of a permutation of c1 at the member
that the search finds.

**The outer filter.** Number the seven outcomes of beta* whose tau ends in 5020a0
j = 1 to 7: 175020a0, 185020a0, 275020a0, 285020a0, 385020a0, 675020a0 and
685020a0, the program's `CTR_TAUS`. The set S lists six of them, S = {1, 2, 3,
4, 5, 7}: all but 675020a0 (j = 6). In the hexadecimal masks below, with bit
j - 1 for outcome j, S is 5f. Beta* has seven more outcomes on the class, the
same seven with bit 14 of tau set; S does not list them either.
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
of E3 is Y3 for A and Y3' for B (Fact P). The conditions of R = 0 (proof of
Lemma V, A7) give that the XOR difference of E3's first-half b values is
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

about 0.00099145731 = 2^-9.978162. Let pi_E be the share of the 2^32
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
pairs of masks m and n with m AND n AND 5f not zero is 2,129,896. So the
number of pairs that pass
for S is 7,936 * 1,082,016 * 2,129,896 = 18,289,159,183,466,496 (the
participant's arithmetic on the table; GPT Sol's answer AW 3 gives the same
279,070,422,111 and 233,715,456).

