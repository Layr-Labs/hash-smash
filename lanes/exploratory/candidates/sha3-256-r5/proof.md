# SHA3-256 with 5 prefix rounds: an internal-differential collision campaign, time_log2 87.0814

## 1. Claim

Target `sha3-256-r5-prefix-v1`: SHA3-256 (rate 136 bytes, suffix 0x06, zero initial state) with rounds 0 to 4 of
Keccak-f[1600] in every permutation call, full 256-bit digest. The algorithm of Section 5 outputs two distinct
271-byte messages with equal digests.

| Quantity | Value |
|---|---|
| time_log2 (collision-frontier-v5, reference operation cost 1355, rounded up) | **87.0814** |
| success probability | at least 0.3916 (> 0.39), under premises Htrail and H_F |
| memory | 352 N + 3456 R + 2^25 + 2^24 = 103858287863840618650106688 bytes, log2 86.4248 (Section 7.6) |
| preprocessing (included in time) | log2 53.5960 target compressions |
| nonuniform advice | none |

Two premises are declared (Section 8): **Htrail**, a lower bound 2^-18.0069 on the fraction of the generated
family that passes the third-chi filter, with our preregistered 2^38-sample measurement; and **H_F**, the
probability of an equal final-row key among the retained survivors, stated as an assumption. Everything else
used by the claim is proved in Sections 3 to 7. The method is the internal differential of Zhang, Hou and Liu
(EUROCRYPT 2023) applied to a concrete native first block, an exact all-roots generator and an exact final-row
key.

**Changes from 9223524c.** This entry is our 9223524c (scored 99.5682) with one change: the visit. 9223524c paid
for five scalar rounds at every candidate visit (2^14 operations). Here the third-chi filter is computed by a
bit-sliced Gray-code finite-difference walk (Section 4.4): on the chart the filter is 18 bits of degree at most
8 in the visit variable, so 256 visits share one word step of 675 operations, and only the retained survivors
are re-evaluated natively. The step visits the same parameters as 9223524c, keeps the same survivors in the
same order and stops at the same record (Lemma 4c), so the family, the generator, the key, the parameters N, K
and T, the success bound and both premises are unchanged; the premise texts of Section 8 are word for word
those of 9223524c. To make the filter exact we now use the two chi conditions of Lemma 3 at every chart point,
and we prove them by an exact certificate that the program recomputes at every run. The finite-difference visit
and its price were found by our grid-wave-4 scout G1 and confirmed by an independent checker, who reproduced
the price, the certificate and the filter at every visit of its test walks.

## 2. Notation

A state is 25 little-endian 64-bit lanes, lane index x + 5y. P5 is rounds 0 to 4 (theta, rho, pi, chi, iota
with constants RC[0..4]). For a lane s write lo(s) and hi(s) for its low and high 32-bit halves. The quotient of
a state S is the 800-bit vector quo(S) with 32-bit words quo(S)_j = lo(S_j) XOR hi(S_j). Theta, rho and pi
commute with rotating every lane by 32, so the quotient after the linear layer is the image of the quotient
under the same linear layer on 32-bit lanes; chi acts on rows of five bits; iota adds lo(RC) XOR hi(RC) to
quotient word 0.

Messages have 271 bytes: M = M0 || F with a 136-byte first block M0 and a 135-byte fragment F. Padding appends
0x86 at byte 271, so M is absorbed as two blocks and costs two permutation calls:
H(M) = first 32 bytes of P5(N XOR (F || 0x86 || 0^64)), where N = P5(M0 || 0^64).

For a in F_2^800 (32-bit words a_j) and the fixed difference D below, X(a) is the state with lanes
X(a)_j = (a_j XOR D_j) + 2^32 a_j. Thus quo(X(a)) = D, and hi(X(a)_j) = a_j.

## 3. The first block

**First block.** M0 = LE64(7258270406) || 0^128 bytes, that is the bytes `c6 6a a0 b0 01 00 00 00` followed by
128 zero bytes. N = P5(M0 || 0^64) (one call; hex, lane bytes in order):

```
b85cdafa5e44fb0ee93a3544fc132e5b0a925a59bea6556515cdf8598c24d55f320742e487061f9f9fa11f51352873f14a48d65ad770
7452d6ae6fe7f170c957b0654c5fec43e64f2566d671abfdf66993d02463091d506d7ca112d1bc8b972a70111d615937a9aad60af6a8
73d337aad8c7cfb5ac5715ffbff8c3ef2e215269541f8d57584573c2d6c8bbc8f7f77da3313e0e37d716b8687fd55ceeb7d9f295b91d
f2129938ebf7a8574f9792866f6ff112fee7fddbdfa2f8739250f7cb14b3e53371c53310dcd3
```

**Difference.** D, as an 800-bit integer whose bit 32j + i is bit i of word j (hex, most significant first):

```
16ad23d6e386b80f4521c90cf820d13ae51925207bae0cc85fb628e66bc63f219522977e158d710829e96acf8c87e8132f599f1d897a
556ee0cdaf583d26cfe8f784cff55865f78aa43a9feef7124f0e8c2fdfb5b724f6605d99dba5c86dd18751f7efae
```

**Lemma 1 (tail).** Coordinates 536 to 799 of a and D (word 16 bits 24 to 31 and words 17 to 24) determine
bytes 131, 135 and 136 to 199 of X(a). For every chart value a of Section 4, X(a) XOR N is zero on bytes 136
to 199 and equals 0x86 at bytes 131 and 135. Hence X(a) = N XOR (F || 0x86 || 0^64) with F the first 135
bytes of X(a) XOR N, X(a) is the second permutation input of the message M0 || F, and P5(X(a)) gives H(M0 || F).

*Proof.* Byte 131 is the low half of lane 16 at bits 24 to 31 (coordinates 536 to 543 of a XOR D), byte 135
its high half (coordinates 536 to 543 of a); bytes 136 to 199 are lanes 17 to 24. All 141 chart directions are
zero on coordinates 536 to 799 (they are stored as 536-bit vectors), so every chart value has the tail of its
base, and the six bases have the same tail. The displayed equalities for the six bases are checked by direct
computation (`setup()` of the experiment program computes N with one call and checks them). The last sentence
is the definition of the sponge for two blocks. QED.

**Selection procedure SEL (preprocessing, charged in Section 7).** The constants above are the output of this
deterministic procedure; its cost is charged in full and none of its output is treated as free advice.

1. For i = 0, 1, ..., 2^34 - 1: compute N(i) = P5(LE64(i) || 0^128 || 0^64) (one target call) and the 27
   affine parity checks that decide whether the 264 tail coordinates admit a difference in the fixed point-plane
   family (542 independent affine conditions on D, Table 9 family of the method); at most 2^12 operations per i.
2. For each of the first 130 indices that pass (hard cap): form the common first-chi restrictions of its
   21-dimensional difference fiber (at most 2^40 operations); compute k1 for every difference of the reduced
   fiber in canonical reflected-Gray order (at most 2^21 differences, at most 2^30 operations each) and keep the
   first minimizer; discard the index if the minimum exceeds 389; otherwise solve the first-value system and test
   at most the first 1,024 feasible selector assignments for a second-chi root (at most 2^29 operations each).
3. Keep the first index with a root; build the chart of Section 4 and its tables (at most 2^40 operations).

On [0, 2^34) step 1 passes exactly 130 indices and the procedure returns i = 7258270406 with k1 = 385 (an
exhaustive finite computation by GPT Sol cloud, repeated in full). The scan does not stop at the first success:
all 2^34 calls are charged. After SEL the first block is fixed: every message of the campaign shares M0, so N is
computed once and kept, and the campaign makes no further first-block call.

## 4. The family, its generator and the final-row key

### 4.1 The chart

For a set label p in {0..5} and y in F_2^135,

    a_p(y) = B_p XOR U y XOR R c_p(y),
    c_p(y)_k = CON_{p,k} XOR <LIN_{p,k}, y> XOR sum over {i,j} in Q_k of y_i y_j     (k = 0..5),

with 135 free directions U, six correction directions R, six bases B_p, six-bit constants CON_p, 135-bit linear
parts LIN_{p,k} and one shared set of quadratic pairs (675 pairs {i,j}, each with the set of k it belongs to).
All of them are the constant CHART of `experiments/campaign.py` (12,792 bytes, SHA-256
f59bd3cacef864a191bd5c30337690a76a4c62c2b24e9c39caba75d5f28a5a45). The family is
Fam = { M0 || F(a_p(y)) : p, y }, F(a) the first 135 bytes of X(a) XOR N.

**Lemma 2 (distinct messages).** The 141 directions U and R are linearly independent and the six bases are
distinct modulo their span. Hence (p, y) -> a_p(y) is injective, a -> F(a) is injective (hi(X(a)_j) = a_j and X(a)
= N XOR (F || 0x86 || 0^64)), and Fam has exactly |Fam| = 6 * 2^135 distinct valid 271-byte messages.

*Proof.* If a_p(y) = a_p'(y'), then B_p XOR B_p' lies in the span of U and R, so p = p'; then
U (y XOR y') = R (c_p(y) XOR c_p(y')) and independence gives y = y'. Independence and the six base differences are
checked by elimination in `setup()` of the program at every run. Validity of each message is Lemma 1. QED.

**Lemma 3 (the generator returns roots; all of them).** Every a_p(y) satisfies the first two chi conditions
quo(round 0 of X(a)) = T1 and quo(rounds 0..1 of X(a)) = T2 (T1, T2, T3 below), and the six sets contain all of
the 3 * 2^136 solutions a with the tail of Lemma 1.

*Proof of the two chi conditions (exact certificate; `chart_certificate()` of the experiment program repeats it at
every run).* For a fixed input quotient the chi derivative chi(x XOR d) XOR chi(x) = chi(d) XOR L_d(x), with
L_d(x)_i = x_j d_k XOR d_j x_k (j, k the next two lanes of lane i's row), is affine in x. Let
S_p = {B_p XOR U y XOR R t : y in F_2^135, t in F_2^6}, which contains the chart (t = c_p(y)), and write Lin for
theta, rho and pi on 32-bit words. (i) X(a) has quotient D for every a, so the round-0 quotient is an affine
function of a; it equals T1 at B_p and at B_p XOR v for each of the 141 directions v (142 native evaluations),
hence on all of S_p. (ii) So on S_p the second chi receives the quotient e1 = Lin(T1), and the round-1 quotient
is chi(e1) XOR L_e1(x1) plus the quotient of RC[1] on word 0, where x1 = Lin(l0) XOR const are the low halves
entering the second chi, l0 = chi(x0) XOR const the low halves after round 0 and x0 = Lin(a) XOR const the low
halves entering the first chi. It is therefore a polynomial q1 of degree at most 2 on S_p, with constant alpha
(its value at B_p), linear coefficients lambda_v = q1(B_p XOR v) XOR alpha, and, for directions u != v (800-bit
vectors), quadratic coefficient L_e1(Lin(P(Lin u, Lin v))) with P(d, d')_i = d_j d'_k XOR d'_j d_k the polar form
of chi. Write mu_k for the linear coefficient of t_k. The
program computes all of them and checks, in each of the six sets: no quadratic coefficient involves t;
alpha XOR sum_k CON_{p,k} mu_k = T2; lambda_u = sum_k LIN_{p,k,u} mu_k for every u < 135; and the coefficient of
y_u y_v equals sum_k m_{uv,k} mu_k, where m_{uv} is the mask of {u, v} among the chart's 675 pairs (0 if absent).
Substituting t = c_p(y) then leaves exactly the constant T2. QED for the two chi conditions.

*Outline of the second part (GPT Sol cloud; exact algebra).* The first-chi condition is an affine system in a;
with the tail it leaves a 159-dimensional affine space. On it the 21 second-chi conditions are quadratic; row
reduction exposes 14 affine conditions, leaving 7 quadratics in 145 variables. Their common polar radical has
dimension 83 and the radical's syndrome map has rank 6: six radical directions (R) solve six syndrome
coordinates, leaving one quadratic in 139 variables of polar rank 4 whose radical (135 dimensions, U) is free;
exactly 6 of the 16 values of its four active coordinates satisfy it (the six labels). The quadratic coefficient
identities after substitution hold exactly in each set, and the Walsh sums of the 7 quadratics (2^145, -2^143
and 126 zeros) count 3 * 2^136 solutions, which equals the injective image of Lemma 2. QED (outline).

The two chi conditions are used by Lemma 4a (they make the finite-difference filter exact). The second part
(that the six sets hold all roots) is not used by the time or success bounds: the premise Htrail counts filter
survivors among the outputs of the generator directly. The experiment program also tests both chi conditions at
every visited point.

Targets (32-bit words, lanes 0 to 24):

```
T1 = 746a0114 b8e201a0 6240005a 6d5804fd 858c0255 f46a0116 b8f201e0 6642005a 6d5804f5 858c0255 f46a0116 b8e201e0 6242005a
     6d5804f5 858c0255 f46a0156 b8e201e0 6242005a 6d5800f5 858c0255 f46a0116 b8e201e0 6246005a 6d5804f5 858e0257
T2 = 80008080 00000001 00000000 00000000 00008000 80000000 00000000 00000000 00000000 00008000 00000080 00000001 00000000
     00000000 00000000 00000000 00000000 00000000 00000000 00000000 00008000 00000000 00000000 00000000 00000000
T3 = 0000000a 00000000 00000000 00000000 00000000 00000008 00000008 00000400 00000000 00000000 00000002 00000000 00000000
     00000000 00000000 00000000 00000008 00000400 00000000 00000000 00000000 00000000 00000000 00000000 00000000
```

A visited message is a **survivor** if quo(rounds 0..2 of X(a)) = T3 (the third-chi filter).

### 4.2 Incremental generation

**Lemma 4 (Gray step).** For a quadratic c and a fixed v, c(y XOR v) XOR c(y) = c(v) XOR c(0) XOR <pol(v), y>, where
pol(v) = sum over pairs {i,j} of c with v_j = 1 of e_i, plus those with v_i = 1 of e_j. So if y and y XOR v are
consecutive visits, a_p(y XOR v) = a_p(y) XOR U v XOR R delta with delta_k = c_{p,k}(v) XOR c_{p,k}(0) XOR
<pol_k(v), y>.

*Proof.* Expand y_i y_j for y XOR v; the linear and constant parts cancel except at v. QED.

With y_i = A Gray(i) XOR b, consecutive visits differ by one column v = A e_t (t = index of the lowest set bit of
i). A step is one free-direction XOR (U v, prepared once per column), six parities <pol_k(v), y> and at most six
correction XORs. Every visit of a set is a distinct parameter, so (Lemma 2) all visited messages are distinct.
The campaign no longer forms the visits this way (Section 4.4 replaces the scalar visit); the experiment program
uses this walk for its direct filter.

### 4.3 The final-row key

**Lemma 5 (the quotient before the last chi).** For a survivor, the quotient of lanes 0 to 4 just before the
fifth chi is d(q) = d_0 XOR sum_i q_i d_i for a unique q in F_2^16, with the 160-bit vectors (bit 32x + z = lane x,
bit z; hex, most significant first)

```
d_0 = 000f8080220040601404a0301803a0000400018a
d_1 .. d_16 =
0000000000800000000000000000000000000002 0000000002000000000000000000000000000008 000a000000000000000000000000000000000020
0000000020000000000000000000000000000080 0000000000000020000000000000000000008000 0000000000000040000000000000000000010000
8000000000000000080000000000000000020000 0000000000000000000000100000000004000000 0000000000004000000000000000004000000000
0008000000000000000000000001000000000000 0040000000000000000000000008000000000000 4000000000000020000000000800000000000000
8000000000000000000000001000000000000000 0000000000000020000000002000000000000000 0000800000000000000020000000000000000000
0002000000000000000080000000000000000000
```

*Proof.* A survivor has quotient T3 after round 2, so the input quotient of the fourth chi is the fixed vector
e = L(T3) (L = theta, rho, pi on 32-bit lanes). For each row, chi(x XOR e_row) XOR chi(x) = chi(e_row) XOR
L_{e_row}(x) with L_{e_row} linear, so the output quotient lies in chi(e) XOR Im(L_e), an affine space; iota adds
the constant 0x00008000 to word 0, and the next linear layer followed by the projection on lanes 0 to 4 maps this
space onto d_0 XOR span(d_1 .. d_16) (computed; the 16 directions have rank 16, so q is unique). As a native
check, for 48 survivors the quotient computed with the organizer permutation lies in this affine space and the
digest equals the formula of Lemma 6. QED.

Let v be the high halves of lanes 0 to 4 before the fifth chi and, at bit position z in 0..31, let v_z and
d_z(q) be the five-bit row words. Write pi(x) = chi(x) mod 16 (lanes 0 to 3) and
f_d(v) = (pi(v), pi(v XOR d)).

**Lemma 6 (sufficient key).** Define J(q, v) = (q, f_{d_0(q)}(v_0), ..., f_{d_31(q)}(v_31)). Two survivors with
equal J have equal 256-bit digests.

*Proof.* The digest is lanes 0 to 3 after the fifth chi and iota RC[4]. At position z its high-half bits are
pi(v_z) and its low-half bits are pi(v_z XOR d_z(q)) (the low halves are v XOR d(q)); iota adds the same constant to
both digests. QED.

**Lemma 7 (exact image and power sums).** Let n_d = |Im f_d| and s_d^(r) = sum_x |f_d^-1(x)|^r. Exhausting the 32
inputs gives every fiber size 1 or 2 and

| d (decimal) | n_d | s_d^(2) |
|---|---:|---:|
| 0 | 16 | 64 |
| 2, 4 | 24 | 48 |
| 16, 20 | 26 | 44 |
| 6, 18, 22, 24, 26 | 28 | 40 |
| 17, 21 | 30 | 36 |
| 28, 29, 30, 31 | 31 | 34 |
| all other d | 32 | 32 |

Since q is part of J and the 32 positions are independent coordinates of v,
M = |Im J| = sum_q prod_z n_{d_z(q)} and S_r = sum_q prod_z s^(r)_{d_z(q)} over all 2^176 pairs (q, v):

```
M  = 797743755349369243205560562155577038185745612800                    (log2 159.1265)
S2 = 105380798010570215759974880593685063616344969780962598584320        (log2 196.0694)
S3 = 927315958145491365253041251768890317427775387965071092617314304000
S4 = 42474191474907196166763404678579985197638539554508653564265037484261376000
S5 = 6484172743866708697210043141956907926179600576775238640841688666325742280387854336
```

with S_1 = 2^176. Positions 0, 2, 9, 10, 11, 12, 20, 21 and 24 have d_z(q) = 0 for every q. *Proof.* Direct
enumeration of 2^16 * 32 local products. QED.

**Lemma 8 (degree bound).** If f has degree d as a function of a, then f(a_p(y)) has degree at most
min(2d, d + 6) in y. The bits of v (after four chi layers, d = 16) have degree at most 22 in y and the bits of q
(an affine function of a value after three chi layers, d = 8) at most 14.

*Proof.* Treat the six corrections c_k as new variables t_k: a degree-d polynomial in a becomes one of degree at
most d in (y, t), and a monomial with s of the t_k becomes, after substituting the quadratics c_k(y), a
polynomial of degree at most d + s with s <= min(d, 6). Each chi layer at most doubles the degree and the linear
layers do not raise it. QED. GPT-6 Astra's cube sums show these bounds are attained (22 for all 160 bits of
v, 14 for 15 bits of q and 13 for the remaining one) in each set; we use this only as background for H_F.

### 4.4 The filter by finite differences

**Lemma 4a (the filter is 18 planes of degree at most 8).** Let e = Lin(T2) and, at a chart point, let x be the
low halves of the lanes entering the third chi. By Lemma 3 that chi receives the quotient e, so bit z of quotient
word i after round 2 is chi(e)_i XOR L_e(x)_i at bit z, plus the quotient of RC[2] on word 0. Exactly 19 of these
bits depend on x, at positions 32 i + z = 103, 111, 127, 135, 143, 159, 163, 170, 202, 291, 385, 417, 449, 483,
490, 522, 586, 611 and 618; bits 490 and 618 are the same function (the bit of x in lane 16 at z = 10, constant
0) and T3 asks 0 of both; every other bit is a constant equal to the bit of T3. So a visit is a survivor if and
only if the 18 plane values g_h = (bit h) XOR (bit h of T3), h over the first 18 positions, are all 0. Moreover,
let Q3(a) = chi(e) XOR L_e(x(a)) plus the quotient of RC[2] on word 0, where x(a) is computed from X(a) by the
native rounds 0 and 1 and theta, rho and pi, for every a; then each g_h(a_p(y)) is a bit of Q3(a_p(y)) XOR T3 on
the chart and has degree at most 8 in y.

*Proof.* The formula is the chi identity of Lemma 3's proof with d = e. The positions, the constants and the
duplicate are read off e and T3; `filter_planes()` of the program derives them and asserts every constant bit at
every run. Q3 has degree at most 4 in a for every a (two chi layers; the linear layers and a -> X(a) do not raise
degree), so Lemma 8 with d = 4 gives degree at most min(8, 10) = 8 in y; on the chart Q3 is the round-2 quotient
by Lemma 3. QED.

**Lemma 4b (finite-difference walk; Bouillaguet, Chen, Cheng, Chou, Niederhagen, Shamir and Yang, CHES 2010).**
Let f: F_2^m -> F_2 have degree at most 8 and z_k = Gray(k) = k XOR (k >> 1). Call the coordinates m, ..., m + 6
virtual (f does not depend on them) and let k* = k + (2^7 - 1) 2^m, which has at least 8 set bits for k >= 1.
For a set S of coordinates with 1 <= |S| <= 8 put T[S] = (D_S f)(x_S), the derivative in the directions e_s
(s in S) at x_S = (sigma(S) >> 1) AND NOT S, sigma(S) = sum of 2^s over s in S (T[S] = 0 if S has a virtual
coordinate), and V = f(0). For k = 1, 2, ..., 2^m - 1 let S_1, ..., S_8 be the sets of the lowest 1, ..., 8 set
bits of k* and do T[S_j] <- T[S_j] XOR T[S_(j+1)] for j = 7, 6, ..., 1, then V <- V XOR T[S_1]. After step k,
V = f(z_k). The initial values use only the coefficients of degree at most 8, which the Moebius transform gives
exactly from the values of f on the down-set {z : wt(z) <= 8}: T[S] = XOR of coef(S + W) over W inside x_S with
|S| + |W| <= 8, and V = coef(0).

*Proof.* D_S f does not depend on the coordinates in S; it is constant if |S| = 8 and 0 if S has a virtual
coordinate, so those entries never change and the virtual levels change nothing. Fix a real S with largest
element mu, |S| < 8. The steps whose lowest |S| set bits are S are tau_t = sigma(S) + t 2^(mu+1), t = 0, 1, ...,
and T[S] is written only at them. For a < 2^(mu+1), Gray(a + t 2^(mu+1)) = Gray(a) XOR (t mod 2) 2^mu XOR
2^(mu+1) Gray(t). We show, by induction on t and downward on |S| within a step, that after its update at tau_t,
T[S] = (D_S f)(z_(tau_t - 1)). At t = 0 the next level contains a virtual coordinate, so T[S] keeps its initial
value; z_(sigma - 1) and Gray(sigma) differ only in the lowest element of S, and Gray(sigma) with the bits of S
cleared is x_S. For t >= 1 the next set bit of tau_t is nu = mu + 1 + b, b the lowest set bit of t; S' = S + {nu}
is the next level, already updated at this step to (D_S' f)(z_(tau_t - 1)), and
z_(tau_t - 1) XOR z_(tau_(t-1) - 1) = e_mu XOR e_nu. As e_mu and e_nu lie in S' and e_mu in S,
(D_S f)(z_(tau_t - 1)) = (D_S f)(z_(tau_(t-1) - 1)) XOR (D_S' f)(z_(tau_t - 1)), which is the update. Then
V XOR T[S_1] = f(z_(k-1)) XOR (D_(e_s) f)(z_(k-1)) = f(z_k), s the lowest set bit of k. Finally (D_S f)(x) is the
XOR of coef(S + W) over W inside x outside S, and coef(S) depends only on the values at the subsets of S. QED.

**Lemma 4c (lanes and blocks).** For 0 <= c' < 256 and c = c' XOR 255 (k mod 2),
Gray(256 k + c') = 256 Gray(k) XOR Gray(c). So the visits of set p with index below 256 J are, block by block,
y = A_p (256 Gray(k) XOR Gray(c)) XOR b_p for k = 0, ..., J - 1 and lanes c = 0, ..., 255. For each lane and plane
the value at block k is f_(p,c,h)(Gray(k)) with f_(p,c,h)(z) = g_h(a_p(A_p (256 z XOR Gray(c)) XOR b_p)), of degree
at most 8 in z (Lemma 4a; z -> y is affine), and all lanes take the same steps of Lemma 4b. With lane c in bit c of
a 256-bit word, one word XOR makes a step for all 256 lanes.

*Proof.* (256 k + c') >> 1 = 128 k + (c' >> 1) with no common bits, so Gray(256 k + c') = 256 Gray(k) XOR
128 (k mod 2) XOR Gray(c'), and Gray(c' XOR 255) = Gray(c') XOR 128. QED.

## 5. The campaign

Parameters (exact integers, Section 6):

```
N    = 295051954157537185375674        retained survivors (records)
K    = 263401                          rate constant, K >= 2^18.0069
s    = 543186850134 = ceil(sqrt N),    h = 16 s + 256 = 8690989602400
T    = 6 ceil(K (N + h) / 6) = 77716979779338667517399669676    candidate visits
L    = T / 6 = 12952829963223111252899944946                     visits per set
J    = ceil(L / 256) = 50596992043840278331640410                blocks per set (256 J - L = 14, J - 1 < 2^86)
```

Algorithm CAMP:

1. Run SEL (Section 3); obtain M0, N, D and the chart.
2. For p = 0..5: draw the 135 columns of A_p in turn, each uniform on F_2^135 and redrawn while it lies in the
   span of the earlier columns, at most 128 draws per column; if a cap is reached, stop with failure. Draw a
   uniform 135-bit translation b_p.
3. For p = 0..5 build the tables of Lemma 4b for the 18 planes and the 256 lanes (lane c in bit c of each word;
   walk point z in F_2^86; visit y = A_p (256 z XOR Gray(c)) XOR b_p): evaluate the planes at every lane and every
   z of weight at most 8 (chart formula, three native rounds; the T3 bits are XORed in, so a survivor is a lane
   whose 18 V words all hold 0), apply the Moebius transform on the down-set and fill T and V. Then for
   k = 0, 1, ..., J - 1: if k >= 1, make word step k of every set (Lemma 4b on all 18 planes; Section 7.3); take the
   surviving lanes of block k in the order of the index i = 256 k + c' (c = c' XOR 255 (k mod 2)), then p; skip
   i >= L; re-evaluate each natively (y, a_p(y), rounds 0 to 4, quo = T3 after round 2) and append the 176-byte
   record (digest, 32 bytes; F, 135 bytes; 9 zero bytes). Stop visiting when N records exist.
4. Sort the records by their 32 digest bytes with 32 stable byte-radix passes between two arrays (least
   significant byte first). Compare adjacent digests; for the first equal pair form M0 || F and M0 || F', check
   F != F' and hash both natively (four target calls); output the pair. Otherwise stop with failure.

Every bound in steps 2 and 3 (128 draws per column, J blocks, i < L, N records) is a halt of the algorithm.

By Lemmas 3, 4a, 4b and 4c, step 3 finds exactly the visits i < L of each set that pass the third-chi filter and
takes them in the order (i, then p) of 9223524c's step 3, which visited y = A_p Gray(i) XOR b_p for i = 0..L - 1.
So on the same coins it appends the same records in the same order and stops at the same record: Sections 6 and
8 apply to it unchanged.

## 6. Success

**Lemma 9 (setup).** Step 2 fails with probability at most
eps = 6 sum_{k=0..134} 2^(-128 (135 - k)) < 2^-124, and on success each A_p is uniform on GL(135, 2),
independently over p.

*Proof.* Column k is redrawn only while it lies in the span of k independent columns, which has 2^k of the
2^135 values, so its 128 draws all fail with probability 2^(-128 (135 - k)); a union bound over columns and sets
gives eps. Conditional on success, column k is uniform on the complement of the span of columns 0..k-1, so
every ordered basis, that is every invertible matrix, has the same probability prod_k (2^135 - 2^k)^-1. QED.

**Lemma 10 (survivor supply).** Let G_p be the number of survivors in set p, G = sum G_p and |Fam| = 6 * 2^135.
Given setup, the number X of survivors among the T visits has mean mu = T G / |Fam| and variance at most mu. If
G >= |Fam| / K, then Pr(X >= N | setup) >= (mu0 - N + 1)^2 / (mu0 + (mu0 - N + 1)^2) with mu0 = T / K.

*Proof.* For fixed p, y -> A_p y XOR b_p is a uniform invertible affine map, which is 2-transitive: each visited
parameter is uniform and each pair of distinct visits is a uniform pair of distinct parameters. So the count in
set p is that of L draws without replacement from 2^135 items of which G_p are survivors: mean L G_p / 2^135,
variance at most the mean. The six sets are independent. Cantelli's inequality for X <= N - 1 gives
Pr(X < N) <= mu / (mu + (mu - N + 1)^2), which decreases in mu for mu > N - 1, and mu >= mu0 >= N + h. QED.

**Premise H_F** (Section 8.2) gives, conditional on setup and X >= N, an equal-J pair among the first N
survivors with probability at least B_F, the exact four-moment Bonferroni bound of the uniform-original-key model:

```
B_F = m1 - m2 + m3 - m4 = 0.3932291666...  > 393/1000
(m1, m2, m3, m4) = (0.500000000000, 0.125000000000, 0.020833333333, 0.002604166667)
```

where m_j = E[binom(C, j)] for the number C of equal-J pairs among N records whose original 176-bit keys (q, v) are
independent and uniform: m_j = sum over simple graphs with j edges and no isolated vertex on n labelled vertices
of C(N, n) prod over components of p_size, with p_r = S_r / 2^(176 r). N is the least integer with
N^2 S_2 >= 2^352.

**Theorem (success).** Under Htrail and H_F, CAMP outputs a collision with probability at least

    (1 - eps) * supply * B_F = 0.391699092088... > 0.39,

with supply = (mu0 - N + 1)^2 / (mu0 + (mu0 - N + 1)^2) = 0.996108949416..., mu0 = T / K. A compact
certificate: setup >= (2^50 - 1)/2^50, supply >= 255/256 (because (mu0 - N + 1)^2 >= 255 mu0), B_F > 393/1000,
and (2^50 - 1)/2^50 * 255/256 * 393/1000 = 22566411832846692789 / 57646075230342348800 > 39/100.

*Proof.* Setup (Lemma 9), then supply (Lemma 10 with Htrail, which gives G >= |Fam| 2^-18.0069 >= |Fam| / K), then
the key event conditional on both (H_F); an equal-J pair has equal digests (Lemma 6), so the adjacent scan finds an
equal-digest pair; the two records are distinct visits, hence distinct messages (Lemma 2), and their digests are
the target hashes (Lemma 1). No independence between supply and the key event is used. QED.

## 7. Cost

### 7.1 Machine

The organizer machine is a 256-bit word RAM; one P5 call costs one unit and any other primitive operation 1/1355.
The ledger counts instructions of a 64-bit program (64-bit Boolean, shift, add, compare, branch, move, load, store,
one random bit). **Lemma 11 (word conversion).** (a) Any such instruction costs at most two 256-bit operations:
the operation on zero-extended values, then an AND with 2^64 - 1 (this reproduces 64-bit wraparound). (b) In the
survivor and set-up programs of 7.3 and the record and sort programs of 7.4 each instruction is one 256-bit
operation, except: (i) a 64-bit lane rotation needs one extra AND after its left shift (30 rotations per round);
(ii) multiword arithmetic on the Gray counters and on two-word addresses is done in single 256-bit words with
fewer operations than the 64-bit sequence it replaces; (iii) a byte load from a record needs at most two extra
operations (shift, AND).

*Proof.* (a) is immediate. (b) Keep every 64-bit value in the low bits of a word with zero high part. AND, OR,
XOR and right shifts of such values give such values; NOT is used only inside chi's (NOT b) AND c, whose result
is again zero above bit 63; a comparison of such values equals the 64-bit unsigned comparison. A left shift is
used on lanes only inside a rotation (x << r) OR (x >> (64 - r)), and one AND restores the zero high part.
Additions in these programs occur only in counters and addresses, whose values are below 2^200 and never rely on
wraparound, so a multiword addition with carry tests becomes one addition. A 64-bit load or store moves one
word; a byte of a record is read from its word with one shift and one AND. QED.

The word step of 7.3 is a program of the 256-bit machine itself and is counted in its operations (one per load,
store, Boolean operation, addition, shift, comparison or branch); so are the 800-bit vector operations of the
chart formula in 7.3 (three or four words per vector).

### 7.2 Preprocessing and selection

| Component (64-bit instructions) | Bound |
|---|---:|
| common first-chi preparation, 130 prefixes | 130 * 2^40 |
| difference scoring, 130 * 2^21 differences | 130 * 2^51 |
| selector branches, 130 * 1024 | 130 * 2^39 |
| step 2 of CAMP: at most 6 * 135 * 128 column draws, each at most 2^12 (135 random bits, reduction by at most 135 pivots of three words) | 6 * 135 * 128 * 2^12 |
| chart, derivative tables, global code, workspace | 2^40 |
| sum | 292949480482799616 |

At most two 256-bit operations per instruction (Lemma 11) gives 585898960965599232 < 2^64: the reserve **2^64**.
Each of the 2^34 prefixes costs one target call and at most 2^12 operations (27 parity rows over nine 32-bit
pieces, folds and control: 3,855 instructions, no rotation): **P = 2^34** calls and **2^12 P** operations.

### 7.3 The visit

**Word step.** One block k >= 1 of all six sets (Lemma 4b on the 18 planes, 256 lanes per word). The low table
holds, for each w < 2^16, the address of a high-table row and eight partial row addresses; the high table holds
eight partial row addresses for each number q <= 8 of low bits used; both are scaled to word addresses (row times
108 plus the table base), and plane h of set p sits at offset 18 p + h of its row. The experiment program performs
exactly these operations, counts them and asserts the total at every step:

| Operation of the 256-bit machine | Count |
|---|---:|
| loop: k* + 1, compare with the bound, branch | 3 |
| w = k* AND (2^16 - 1); test w = 0, branch | 3 |
| low-table row (shift, add); load of the high-table row address | 3 |
| eight chain rows: per level two address adds, two loads, one add | 40 |
| per set: clear the accumulator; survivor test (compare with all ones, branch) | 6 x 3 |
| per set and plane: deepest level (address add, load) 2; seven levels (address add, load, XOR, store) 28; V (address add, load, XOR, store) 4; OR into the accumulator 1 | 6 x 18 x 35 |
| **sum** | **3,847** |

When w = 0, once per 2^16 steps, the high table is rebuilt for H = k* >> 16 (a scan of at most 77 bit positions
at 4 operations, 8 hits at 3, 36 entries at 6, and 1: at most 549 < 2^10 operations), less than one operation per
step. A block thus costs at most 3,848 <= 6 x 675 operations. **We charge 675 operations per word step of one
set** and 6 J word steps in all (block 0 needs no step; its survivor test is inside the charge). The visit rounds
are charged as operations, not as target calls.

**Retained survivors.** At most N lanes are re-evaluated (step 3): by Lemmas 3, 4a and 4b each of them passes the
third-chi filter and becomes a record. The lanes skipped because i >= L, at most 84, are inside the fixed 2^20 of
7.4.

| Work per retained survivor (256-bit operations; rounds by Lemma 11) | Bound |
|---|---:|
| lane extraction from the six masks, order (i, p), test i < L, record count | 384 |
| y = A_p Gray(i) XOR b_p: at most 94 column XORs | 376 |
| U y: at most 135 directions of three words | 1,485 |
| c_p(y): six linear parities 108; quadratic part 135 x 22 and six parities 102 | 3,180 |
| R c_p(y) and the base | 36 |
| form and keep the 25 input lanes from a and D | 1,200 |
| rounds 0 to 4 (5 x 1,104 + 150 rotation ANDs) | 5,670 |
| filter self-check (25 quotient words), digest capture | 2,048 |
| control | 512 |
| sum | 14,891 |

This is below **2^14** per retained survivor.

**Set-up of the tables** (once, after step 2): 6 x 256 x E down-set evaluations, E = sum over w <= 8 of
C(86, w) = 58940770586, each at most 10,317 < 2^14 operations (y 376, U y 1,485, c_p(y) 3,180, R and base 36,
lanes 1,200, rounds 0 to 2 3,402, the 18 plane bits into the lane words 126, control 512); the Moebius
transform, at most E (86 x 8 + 8 x 2^8) operations per set; the table fill, at most 2^12 E per set (at most 26
terms per row); zeroing all rows, at most 2 x 108 R with R = sum over j <= 8 of C(93, j) = 112132334357; the low
table, 2^23. The total is 1485733379652123896 < **2^61**.

### 7.4 Records, sorting, scan

A record is assembled with at most 176 * 32 + 256 = 5,888 < **2^13** operations. Per record, each of the 32 radix
passes costs at most 64 (count) + 512 (placement: two addresses, digit, bucket, 22 word copies) and the two arrays'
initialization 512 and the adjacent comparison 256: 32 * 576 + 768 = 19,200, plus 128 for byte loads (Lemma 11),
below **2^15**. Fixed sort control, bucket tables and the recovery of the pair: **2^20**. Native verification:
**4** target calls.

### 7.5 Total and rounding

    W = 2^64 + 2^12 P + 2^61 + 675 * 6 J + (2^14 + 2^13 + 2^15) N + 2^20,        C = P + 4 + W / 1355.

| Part | Operations |
|---|---:|
| reserve 2^64 | 18446744073709551616 |
| prefix work 2^12 P | 70368744177664 |
| table set-up 2^61 | 2305843009213693952 |
| word steps 675 * 6 J | 204917817777553127243143660500 |
| retained survivors 2^14 N | 4834131216917089245195042816 |
| records 2^13 N | 2417065608458544622597521408 |
| sorting and scan 2^15 N | 9668262433834178490390085632 |
| fixed 2^20 | 1048576 |
| **W** | **221837277057515597052994782164** |

    C = A / 1355,  A = 1355 (P + 4) + W = 221837277057515620331717531904.

Every run costs at most C (all loops are capped), so the expected cost is at most C. **Rounding certificate:**
with t = 870814, 1355^10000 * 2^(t - 1) < A^10000 <= 1355^10000 * 2^t, so log2 C lies in (87.0813, 87.0814] and
time_log2 = **87.0814**.

### 7.6 Memory and preprocessing

Two record arrays of 176 N bytes, the derivative tables (R rows of 108 words of 32 bytes: 3,456 R bytes), the low
table (2^25 bytes) and a fixed 16 MiB workspace (program, chart, high table, matrices, counters, radix tables,
states): 352 N + 3456 R + 2^25 + 2^24 = 103858287863840618650106688 bytes, log2 86.4248 (rounded up).
Preprocessing (SEL and the reserve) is P + (2^64 + 2^12 P) / 1355 = 3689367544235294720 / 271 compressions, log2
53.5960, inside C.

## 8. Premises and evidence

### 8.1 Htrail

**Statement.** G >= |Fam| * 2^-18.0069, where G counts the messages of Fam (all six sets, all y) that pass the
third-chi filter. Since K = 263401 satisfies K^10000 >= 2^180069, this gives G >= |Fam| / K.

**Evidence (preregistered, our run).** The protocol (sample size, generators, statistic, gates, decision rule) was
fixed and hashed before the main run. 2^38 = 274,877,906,944 parameters (p, y) uniform on the six sets, from two
independent generators (SHA-256 counter mode and PCG64), each evaluated through the chart and the native rounds:
1,048,456 survivors, rate 3.814261e-06 = 2^-18.0002. One-sided 1 - 10^-6 Clopper-Pearson interval
[2^-18.0069, 2^-17.9935]; Chernoff-KL lower bound 2^-18.0076. Generators agree (z = -1.01), the six sets agree
(chi-square 0.65, 5 degrees of freedom), every recorded survivor was re-evaluated with the organizer
permutation (0 false positives), no sample failed the first two chi conditions. A control target (an arbitrary
18-bit residual pattern) gave 2^-18.0024, and the 2^18-bin residual histogram is flat (chi-square 260,369 on
262,143 degrees of freedom). An independent recount on 2^28 fresh samples gave 1,004 survivors (2^-18.028),
consistent (p = 0.55). GPT-6 Astra's 128 reduced campaigns of Section 8.2 saw 48,863 survivors in 12,884,901,888
visits (2^-18.0085). On another difference of the same characteristic (k1 = 413) Grok measured 1,025 filter
passes in 2^28 trials (2^-17.9986).

**Limits.** Statistical: the bound holds at confidence 1 - 10^-6 if the generators behave as uniform independent
sources. The 18 residual conditions have degree up to 8 on the chart, so no exact count is available; the proved
range is 0 <= G/|Fam| <= 33292289/33554432 (minimum-weight bound).

### 8.2 H_F

**Statement.** Conditional on successful setup and on at least N survivors among the T visits of CAMP, the first
N survivors in visiting order contain two with equal J (Lemma 6) with probability at least B_F (Section 6).

This is the collision probability that independent uniform 176-bit keys (q, v) would give after the exact
compression of Lemmas 6 and 7; it is assumed, not proved, for the deterministic native campaign. It does not
assume that the keys are uniform on 2^176 values (Fam has only 6 * 2^135 elements); it asserts a lower bound on a
finite event.

**Evidence.**
- Our preregistered reduced-width test on real survivors of Fam (PREREG.txt sha256 f67e52c0..., recorded before the main run and
  before any key statistic): 9,439,466 survivors from the Htrail sampler; equal-pair counts of the sufficient key projected to
  k = 16, 24, 28, 32, 36, 40 bits in four predeclared bit orders match C(n,2) 2^-k (ratios 0.89 to 1.11, every one-sided
  1 - 10^-6 interval contains 1; at k = 32: 10,493 / 10,434 / 10,406 pairs against 10,373 predicted); keys of uniformly random
  messages of the same length, the control, give the same; verdict SUPPORTS at every width tested (k = 44 descriptive only).
- Exact model computation (Lemma 7 and Section 6): M, S_2 .. S_5, N and B_F are exact; at 1/sqrt(p_2) records
  the four factorial moments are those of a Poisson(1/2) count to 12 digits.
- GPT-6 Astra's reduced native campaigns: 128 campaigns of the actual sampler (six random invertible affine maps,
  2^24 Gray visits per set, the actual filter), 12,884,901,888 visits, 48,863 survivors; equal-pair counts of
  key projections among the first 256 survivors of each campaign: q (16 bits) 62, v (16 bits) 62, q8+v8 72,
  digest prefix (16 bits) 73, against 63.75 expected for uniform values; 12-bit v 991 against 1020; 20- and 24-bit
  projections 0 to 3 pairs against 3.98 and 0.25; pooled over all survivors, 24-bit projections 54 to 86 pairs
  against 71.15.
- Grok's reduced-width measurements on the attack sampler of another difference of the same characteristic
  (k1 = 413): final-key pair rates at 12 to 24 bits within 0.9965 to 1.0009 of 2^-b on 2^20 messages.
- Lemma 8: the key bits have degree up to 22 (v) and 14 (q) in the 135 parameters, and on each set 312 survivors
  span a graph of affine dimension 311 (GPT-6 Astra), so no key combination is affine on the survivors.

**Limits.** All measurements are at reduced width or on short projections; none tests a 159-bit image. A
structure that makes J injective on the survivors (possible by cardinality) would make the event impossible; no
such structure is known, and none is excluded by proof.

## 9. Experiment

`experiments/campaign.py` (Python standard library) runs CAMP at a reduced budget on the organizer's trials. It
does not rerun SEL. Before the trials it replays the first block (one five-round call computes N), checks Lemma 1
for the six bases and Lemma 2 (rank 141, distinct bases modulo the span), computes the certificate of Lemma 3 for
the six sets, derives the planes of Lemma 4a (asserting every constant bit of the third-chi quotient), and runs a
start-up comparison of Lemma 4b at the production degree bound: set 0 with the matrix and translation drawn by
random.Random(4242), one lane, 2^12 walk points, tables built only from the 3,797 points of Gray weight at most 8;
all 4,096 values are compared with the direct filter (299 of them come from the degree bound alone) and every
chain row with its colex value. Each organizer trial is one complete campaign with its own coins (`random.Random`
seeded by the trial seed): step 2 with the cap 128 per column; step 3 at reduced width, 2 lanes and 8 blocks per
set with a low split of 2 bits instead of 16, which are exactly the Gray indices 0 to 15 that 9223524c's
experiment visited (16 visits per set, 96 per trial), with the record cap N_RED = 8; step 4 with the 32-pass radix
sort, the adjacent scan and native verification. At this width the down-set holds every visit, so the tables come
from the direct filter of all 96 visits and the 7 word steps reproduce them. In trials whose index is divisible by
4 the six translations b_p are replaced by six stored survivors from our preregistered sample (eight per set, used
in turn), so that records, sorting and the scan run on real survivors; the matrices remain random. Checks beside
the algorithm: every visit's 18 planes and verdict against the direct filter (`fes_mismatch`), the first two chi
conditions at every visit (`invalid`), and each record's digest against the complete target hash of its message
(`record_mismatch`).

Per trial the program reports 16 counts. They satisfy exactly: `visits` = `downset_points` = 96; `rounds` =
3 downset_points + 5 survivors; `word_steps` = 42 (7 steps of six sets); `step_ops` = 7 x 3,847 + 273 = 27,202
(the counted steps and one rebuild of the high table); `records` = `survivors` (at most 8); `radix_passes` = 32 if
records >= 2, else 0; `comparisons` = records - 1 (0 if none); `verify_calls` = 4 per equal-digest pair verified;
`planted` = 6 in planted trials, else 0; `column_draws` >= 810 (6 x 135 columns plus redraws); `prefix_calls` = 1
in trial 0 (the replay), else 0; `invalid` = `fes_mismatch` = `record_mismatch` = 0. On the organizer's
public-seed request all 256 trials returned no pair; totals: 24,576 visits, 384 survivors (the planted ones), 2,048
radix passes, 320 comparisons, 0 invalid points, 0 FES mismatches, 0 record mismatches, 209,874 column draws.
On the same request we ran 9223524c's program beside this one: in all 256 trials both produce the same records in
the same order and the same values of the ten counts they share. Outside the organizer run we also drove this
program's `fes_init` and `fes_step` at the production width (256 lanes, 2^16 word steps, low split 10) over the
2^24 visits i < 2^24 of set 0 with the coins of random.Random(4242), tables built only from the 10,035,968 visits
whose walk point has Gray weight at most 8, and compared every visit with 9223524c's own direct filter: 0
differences in the 18 planes and in the verdicts, the same 72 survivors, and no visit off the two chi conditions,
off bit 618 = bit 490 or off a constant bit of T3. The run takes about 3 s in the pinned image (1 CPU, 128 MB,
peak 19 MB) with byte-identical output on repetition. A pair at this budget would need about 2^78 records; no
collision is expected or claimed from the experiment.

## 10. Credits

- GPT Sol cloud: the construction (first-block selection, difference, all-roots generator, Lemmas 1 to 4 and 10)
  and the campaign with its instruction ledger.
- GPT-6 Astra: the first-block replay policy, the final-row key (Lemmas 5 to 8), the moments, the H_F row and the
  reduced native campaigns.
- Grok: phase measurements of the attack (filter and reduced-key rates).
- Zhang, Hou and Liu, EUROCRYPT 2023: the internal-differential method and characteristic.
- Bouillaguet, Chen, Cheng, Chou, Niederhagen, Shamir and Yang, CHES 2010: the Gray-code finite-difference
  enumeration of Lemma 4b.
- Our grid-wave-4 scout G1: the finite-difference visit for this entry, its price and the exact certificate of
  Lemma 3's chi conditions; an independent checker of ours reproduced the price, the certificate and the filter at
  every visit of its test walks.
- Our htrail run: the preregistered evidence of Section 8.1; the package and the experiment program.
