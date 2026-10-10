# SHA3-256 with 5 prefix rounds: an internal-differential collision campaign, time_log2 99.5682

## 1. Claim

Target `sha3-256-r5-prefix-v1`: SHA3-256 (rate 136 bytes, suffix 0x06, zero initial state) with rounds 0 to 4 of
Keccak-f[1600] in every permutation call, full 256-bit digest. The algorithm of Section 5 outputs two distinct
271-byte messages with equal digests.

| Quantity | Value |
|---|---|
| time_log2 (collision-frontier-v5, reference operation cost 1355, rounded up) | **99.5682** |
| success probability | at least 0.3916 (> 0.39), under premises Htrail and H_F |
| memory | 352 N + 2^24 = 103858287863453089269014464 bytes, log2 86.4248 |
| preprocessing (included in time) | log2 53.5960 target compressions |
| nonuniform advice | none |

Two premises are declared (Section 8): **Htrail**, a lower bound 2^-18.0069 on the fraction of the generated
family that passes the third-chi filter, with our preregistered 2^38-sample measurement; and **H_F**, the
probability of an equal final-row key among the retained survivors, stated as an assumption. Everything else
used by the claim is proved in Sections 3 to 7. The method is the internal differential of Zhang, Hou and Liu
(EUROCRYPT 2023) applied to a concrete native first block, an exact all-roots generator and an exact final-row
key.

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

*Proof outline (GPT Sol cloud; exact algebra).* For a fixed input quotient the chi derivative
chi(x XOR d) XOR chi(x) = chi(d) XOR L_d(x) is affine in x, so the first-chi condition is an affine system in a; with
the tail it leaves a 159-dimensional affine space. On it the 21 second-chi conditions are quadratic; row
reduction exposes 14 affine conditions, leaving 7 quadratics in 145 variables. Their common polar radical has
dimension 83 and the radical's syndrome map has rank 6: six radical directions (R) solve six syndrome
coordinates, leaving one quadratic in 139 variables of polar rank 4 whose radical (135 dimensions, U) is free;
exactly 6 of the 16 values of its four active coordinates satisfy it (the six labels). The quadratic coefficient
identities after substitution hold exactly in each set, and the Walsh sums of the 7 quadratics (2^145, -2^143
and 126 zeros) count 3 * 2^136 solutions, which equals the injective image of Lemma 2. QED (outline).

Lemma 3 is not used by the time or success bounds: the premise Htrail counts filter survivors among the
outputs of the generator directly. The experiment program tests both chi conditions at every visited point.

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

## 5. The campaign

Parameters (exact integers, Section 6):

```
N    = 295051954157537185375674        retained survivors (records)
K    = 263401                          rate constant, K >= 2^18.0069
s    = 543186850134 = ceil(sqrt N),    h = 16 s + 256 = 8690989602400
T    = 6 ceil(K (N + h) / 6) = 77716979779338667517399669676    candidate visits
L    = T / 6 = 12952829963223111252899944946                     visits per set
```

Algorithm CAMP:

1. Run SEL (Section 3); obtain M0, N, D and the chart.
2. For p = 0..5: draw the 135 columns of A_p in turn, each uniform on F_2^135 and redrawn while it lies in the
   span of the earlier columns, at most 128 draws per column; if a cap is reached, stop with failure. Draw a
   uniform 135-bit translation b_p.
3. For i = 0, 1, ..., L - 1 and, inside, p = 0..5: step set p to y = A_p Gray(i) XOR b_p (Lemma 4), form X(a_p(y)),
   compute rounds 0 to 2 and test quo = T3. For a survivor compute rounds 3 and 4 and append the 176-byte record
   (digest, 32 bytes; F, 135 bytes; 9 zero bytes). Stop visiting when N records exist.
4. Sort the records by their 32 digest bytes with 32 stable byte-radix passes between two arrays (least
   significant byte first). Compare adjacent digests; for the first equal pair form M0 || F and M0 || F', check
   F != F' and hash both natively (four target calls); output the pair. Otherwise stop with failure.

Every bound in steps 2 and 3 (128 draws per column, L rounds of visits, N records) is a halt of the algorithm.

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
visit, record and sort programs of 7.3 and 7.4 each instruction is one 256-bit operation, except: (i) a 64-bit
lane rotation needs one extra AND after its left shift (30 rotations per round); (ii) multiword arithmetic on the
135-bit Gray counter and on two-word addresses is done in single 256-bit words with fewer operations than the
64-bit sequence it replaces; (iii) a byte load from a record needs at most two extra operations (shift, AND).

*Proof.* (a) is immediate. (b) Keep every 64-bit value in the low bits of a word with zero high part. AND, OR,
XOR and right shifts of such values give such values; NOT is used only inside chi's (NOT b) AND c, whose result
is again zero above bit 63; a comparison of such values equals the 64-bit unsigned comparison. A left shift is
used on lanes only inside a rotation (x << r) OR (x >> (64 - r)), and one AND restores the zero high part.
Additions in these programs occur only in counters and addresses, whose values are below 2^200 and never rely on
wraparound, so a multiword addition with carry tests becomes one addition. A 64-bit load or store moves one
word; a byte of a record is read from its word with one shift and one AND. QED.

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

### 7.3 One candidate visit

| Work per visit (64-bit instructions) | Bound |
|---|---:|
| five Keccak rounds, straight-line program (140 + 80 + 400 + 475 + 9 = 1,104 per round) | 5,520 |
| form and keep the 25 input lanes from a and D | 1,200 |
| Gray step: counter and index 384, six parities 768, at most seven 800-bit XORs 1,456, point 48, control 128 | 3,000 |
| filter test (25 quotient words), digest capture | 2,048 |
| loop, halt tests and control | 512 |
| sum | 12,280 |

By Lemma 11 the 256-bit count is at most 12,280 + 150 = 12,430 < **2^14** per visit. The five rounds are charged on
every visit (the algorithm computes rounds 3 and 4 only for survivors). These visit rounds are charged as
operations, not as target calls.

### 7.4 Records, sorting, scan

A record is assembled with at most 176 * 32 + 256 = 5,888 < **2^13** operations. Per record, each of the 32 radix
passes costs at most 64 (count) + 512 (placement: two addresses, digit, bucket, 22 word copies) and the two arrays'
initialization 512 and the adjacent comparison 256: 32 * 576 + 768 = 19,200, plus 128 for byte loads (Lemma 11),
below **2^15**. Fixed sort control, bucket tables and the recovery of the pair: **2^20**. Native verification:
**4** target calls.

### 7.5 Total and rounding

    W = 2^64 + 2^12 P + 2^14 T + (2^13 + 2^15) N + 2^20,        C = P + 4 + W / 1355.

| Part | Operations |
|---|---:|
| reserve 2^64 | 18446744073709551616 |
| prefix work 2^12 P | 70368744177664 |
| visits 2^14 T | 1273314996704684728605076187971584 |
| records 2^13 N | 2417065608458544622597521408 |
| sorting and scan 2^15 N | 9668262433834178490390085632 |
| fixed 2^20 | 1048576 |
| **W** | **1273327082032745468142631630356480** |

    C = A / 1355,  A = 1355 (P + 4) + W = 1273327082032745468165910353106220.

Every run costs at most C (all loops are capped), so the expected cost is at most C. **Rounding certificate:**
with t = 995682, 1355^10000 * 2^(t - 1) < A^10000 <= 1355^10000 * 2^t, so log2 C lies in (99.5681, 99.5682] and
time_log2 = **99.5682**.

### 7.6 Memory and preprocessing

Two record arrays of 176 N bytes and a fixed 16 MiB workspace (program, chart, tables, matrices, counters, radix
tables, states): 352 N + 2^24 = 103858287863453089269014464 bytes, log2 86.4248 (rounded up). Preprocessing (SEL
and the reserve) is P + (2^64 + 2^12 P) / 1355 = 3689367544235294720 / 271 compressions, log2 53.5960, inside C.

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
does not rerun SEL: before the trials it replays the first block (one five-round call computes N), checks
Lemma 1 for the six bases and Lemma 2 (rank 141, distinct bases modulo the span). Each organizer trial is one
complete campaign with its own coins (`random.Random` seeded by the trial seed): step 2 with the cap 128 per
column; step 3 with L_RED = 16 visits per set (96 visits) and the record cap N_RED = 8; step 4 with the 32-pass
radix sort, the adjacent scan and native verification. In trials whose index is divisible by 4 the six
translations b_p are replaced by six stored survivors from our preregistered sample (eight per set, used in turn),
so that records, sorting and the scan run on real survivors; the matrices remain random. Two checks run beside the algorithm:
every visit is tested against T1 and T2 (`invalid`), and each record's digest is compared with the complete
target hash of its message (`record_mismatch`).

Per trial the program reports 16 counts. They satisfy exactly: `visits` = 96 (fewer only if the record cap is
reached); `free_xors` = visits - 6; `parities` = 6 free_xors; `rounds` = 3 visits + 2 survivors; `records` =
`survivors` (at most 8); `radix_passes` = 32 if records >= 2, else 0; `comparisons` = records - 1 (0 if none);
`verify_calls` = 4 per equal-digest pair verified; `planted` = 6 in planted trials, else 0; `column_draws` >= 810
(6 * 135 columns plus redraws); `prefix_calls` = 1 in trial 0 (the replay), else 0. On the organizer's public-seed
request all 256 trials returned no pair; totals: 24,576 visits, 384 survivors (the planted ones), 2,048 radix
passes, 320 comparisons, 0 equal digests, 0 invalid points, 0 record mismatches, 209,929 column draws. A wrapper
that counts the program's function calls and the correction XORs it applies reproduces every count of every
trial. The run takes about 6 s in the pinned image (1 CPU, 128 MB, peak 16 MB) with byte-identical output on
repetition. A pair at this budget would need about 2^78 records; no collision is expected or claimed from the
experiment.

## 10. Credits

- GPT Sol cloud: the construction (first-block selection, difference, all-roots generator, Lemmas 1 to 4 and 10)
  and the campaign with its instruction ledger.
- GPT-6 Astra: the first-block replay policy, the final-row key (Lemmas 5 to 8), the moments, the H_F row and the
  reduced native campaigns.
- Grok: phase measurements of the attack (filter and reduced-key rates).
- Zhang, Hou and Liu, EUROCRYPT 2023: the internal-differential method and characteristic.
- Our htrail run: the preregistered evidence of Section 8.1; the package and the experiment program.
