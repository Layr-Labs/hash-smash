# SHA3-256 with 6 prefix rounds: Gray-order enumeration of two-round-affine cosets, time_log2 122.98920

## 1. Claim

Target `sha3-256-r6-prefix-v1` (organizer profile): SHA3-256 of FIPS 202 with "prefix rounds 0 through 5, inclusive,
in every sponge permutation" (not the last-round convention of Keccak-p); all-zero 1600-bit initial state; rate 1088
bits, capacity 512; "SHA3 domain suffix 01 followed by pad10*1; delimited suffix byte 0x06", standard little-endian
lane and bit encoding; the digest is the first 32 squeeze bytes; messages are distinct byte strings of bit length
below 2^64; reference `verifier/keccak.py:sha3_256`. Postcondition: "The two complete sha3-256-r6 sponge hashes agree
on all 256 output bits." The algorithm CAMP of Section 8 outputs two distinct 135-byte messages with equal digests.

| Quantity | Value |
|---|---|
| time_log2 (collision-frontier-v5, reference operation cost 1626, rounded up) | 122.98920 (Section 10) |
| success probability | at least 0.39, under premise H_coset (Section 9) |
| memory | below 2^141 words of 256 bits, below 2^146 bytes (Section 11.1) |
| preprocessing (included in time) | at most 2^70 + 16 word operations, below 2^59.34 target compressions (Section 11.2) |
| nonuniform advice | none |

One premise is declared (Section 12): **H_coset**, that the 256-bit digests of the messages CAMP enumerates, in its
order, are independent and uniform. Everything else is proved here: two-round affinity on every coset of W40, degree
at most 8 before the last chi, exactness of the Gray-order finite differences and of their initialization, correctness
of the sparse-set table for arbitrary initial memory, and every operation count.

## 2. Notation and messages

A state is 25 little-endian 64-bit lanes S[x + 5y] (x, y in 0..4); bit z of lane k is state bit 64k + z. Round r
(r = 0..5) is theta, rho, pi, chi, iota with constant RC[r] as in the reference; P6 is rounds 0 to 5. XOR is
addition over F_2. For t in F_2^320 let u_k(t) (k = 0..4) be bits 64k to 64k + 63 of t.

**Messages.** M(t) = U || 0^40 || U || 0^15 (135 bytes) with U = LE64(u_0) || ... || LE64(u_4). The padding of the
profile appends 0x06 and the final bit 0x80, which share byte 135, so M(t) is one 136-byte block A(t): lanes 0 to 4
and lanes 10 to 14 hold u_0 .. u_4, lane 16 holds 0x86 * 2^56, all other lanes (and the capacity) are zero. H(M(t)) is
lanes 0 to 3 of P6(A(t)): one permutation call per message.

**Lemma 1 (messages).** t -> M(t) is injective, and every M(t) is a message of the target domain whose hash is the
first 32 bytes of P6(A(t)).

*Proof.* The first 40 bytes of M(t) are t in little-endian order. The block is the profile's padding of a 135-byte
string (135 = 136 - 1, so the suffix and the final bit fall in byte 135), absorbed into the zero state. QED.

**Pre-chi6 bits.** For a block A let b(A) in F_2^320 be row y = 0 after theta, rho and pi of round 5 applied to
rounds 0 to 4 of A: bits b_{x,z}, lane x = 0..4, bit z = 0..63. Digest lane x (x = 0..3), bit z, is
b_{x,z} XOR (NOT b_{x+1,z} AND b_{x+2,z}) XOR RC[5]_z [x = 0] (lane indices mod 5; RC[5] = 0x0000000080000001 sets
bits 0 and 31 of lane 0).

**Gray code.** g(i) = i XOR floor(i/2) for i >= 0; an integer is identified with the set of its 1-bits. g is a
bijection of [0, 2^n), and g(i) and g(i - 1) differ exactly in bit nu(i), the lowest set bit of i.

## 3. The field W40 and two-round affinity

W40 = (w_0, ..., w_39), vectors of F_2^320 in hexadecimal, most significant digit first; bit 64k + b is bit b of u_k.
The order is part of the algorithm (Gray enumeration, Section 6.1). Section 11.2 bounds the search that produced them.

```
w_0  00000000000000000000000040000004100100000000000000002000200000000000000000000000
w_1  000000000000000000000000800200002000000a0000202000000001400000040000200000000800
w_2  00000000000000000000000200000020800800000000000000010001000000000000000000000000
w_3  00000000000000000000410010000104000100400000140000802000000000800000000040000010
w_4  00000000000000000000820000820000000000080082000000040001000040000000200000200820
w_5  00000000000000000020000000000000000000000000000000000000000004000000000000020800
w_6  00000000000000000100000010000000000000000040040000800000000000800000000000000000
w_7  00000000000000000800000000820000002000080000000000000001004004000000200000000800
w_8  00000000000000008000020000000000000000002080000000000000000000000000000000200020
w_9  00000000000000030000020010800100040000422082042000040000680040840000000040200020
w_10 00000000000000410000020000820100000000002082000000040009200040000000200040200020
w_11 00000000000008010041020012820500858000406892040010240000290040800000200040201020
w_12 00000000000100010000020000000004000100802080000000002010200040000000080000208020
w_13 00000000000200010000020010820101040040482082240000040001280040800000200040200820
w_14 00000000000400010001020010800100040000406082440000040000280040800000200040200020
w_15 00000000010000010041020010000100040000406092040000040000280040800000000040201020
w_16 00000000040000010000020010820100808000402882040010840000210040800000200040200020
w_17 00000000080000010041020010000100040000406010040000200000280000800000000040001020
w_18 00000000800000010000020000820000900000002082000010040000000040000000200000200020
w_19 00000001000000010000030010800100200000422082042000840000600040840000000040200030
w_20 00000004000000010000020010820100840000406082040000040000280040800000200040200020
w_21 00000080000000010041020010820500050000486092041000240021280040800000200040201020
w_22 00000100000000010001020010800100040000406082042000040000280040800000000040201020
w_23 00000200200000000000090000000000000000000000000000800000000000400000000000000000
w_24 00000400000000010000000000000100000000402000000000000000200000000000000040000020
w_25 00001000200000000000080010000104000100400000140000002000000002800000000040000000
w_26 00008000000000010000020002820004808108002882100010042100210040000000200000200020
w_27 00020000000000010001020010000100040000406080040000000000280000800000000040200020
w_28 00100000000000010000020000000004000000002080000000000000200040000000000000200020
w_29 004000000000000100000200108201000000004820c2040000840001200844800000200040220820
w_30 00800000000000010041020010820120040000406082040000040001280040800000200040201020
w_31 020000000000000100000200100001000020004020c2040000840000200040800000000040200020
w_32 04000000000000010000020000000000000000002080000000000000200000000000000040000020
w_33 08000000000040000400000002000104008100400000140000002100000002800000000040000000
w_34 40000000000000010000020010820100840000402882040010040000200040800000200040200020
w_35 0a8094012901484005004a005200842021a008000010000402000000000000000000000000000001
w_36 080090012801480104004a0052008400318008002000000000000000000000000000000000000020
w_37 08009001200048020400480012000001208009000000000000000000000080000000000000010000
w_38 0a0294052801480185014a0052028400b1a008000000000000001000000000000008000000000000
w_39 00001200040008000000010002000000000001000000000000000000000000400000000000000000
```

Let F2(t) in F_2^1600 be the state after rounds 0 and 1 of A(t), and for a, b in F_2^320 let
beta_t(a, b) = F2(t XOR a XOR b) XOR F2(t XOR a) XOR F2(t XOR b) XOR F2(t).

**Lemma 2 (round 0 is affine on all of F_2^320).** t -> round 0 (A(t)) is affine.

*Proof.* The t-dependent lanes of A(t) are (x, 0) and (x, 2), both equal to u_x, so every column parity of theta is
u_x XOR u_x XOR (a constant) and theta adds a constant to every lane. Rho and pi move bits linearly: lane (x, 0) goes to
(0, 2x) and lane (x, 2) to (2, 2x + 1) (indices mod 5), so in every row only lanes x = 0 and x = 2 depend on t. Chi
outputs a_x XOR (NOT a_{x+1}) a_{x+2}; the factor pairs (x + 1, x + 2) are (1, 2), (2, 3), (3, 4), (4, 0) and (0, 1),
never {0, 2}, so every product has at most one t-dependent factor. Iota adds a constant. QED.

**Lemma 3 (two-round affinity on every coset).** (a) beta_t(a, b) does not depend on t; as a function of (a, b) it is
symmetric, bilinear, and zero when a = b. (b) If beta(w_i, w_j) = 0 for all 0 <= i < j < 40, then for every t in
F_2^320 and every u in F_2^40,

    F2(t XOR sum_j u_j w_j) = F2(t) XOR sum_j u_j (F2(t XOR w_j) XOR F2(t)).

(c) The hypothesis of (b) holds.

*Proof.* (a) By Lemma 2 the input of round 1 is affine in t; theta, rho, pi and iota are affine and every chi output
bit has degree 2 in its inputs, so every bit of F2 is a polynomial of degree at most 2 in t: F2 = Q XOR Lin XOR c with
Q a vector of quadratic forms, Lin linear and c constant. The polar form B(a, b) = Q(a XOR b) XOR Q(a) XOR Q(b) of a
quadratic form is symmetric, bilinear and zero on the diagonal, and expanding the four terms gives beta_t(a, b) =
B(a, b) for every t. (b) By bilinearity B vanishes on span(W40) x span(W40), so Q is additive there, and
Q(t XOR x) = Q(t) XOR Q(x) XOR B(t, x) with B(t, .) linear. Hence x -> F2(t XOR x) XOR F2(t) = Q(x) XOR B(t, x) XOR
Lin(x) is linear on span(W40), which is the displayed identity. (c) By (a) it suffices to take t = 0: the 780 values
beta_0(w_i, w_j) = F2(w_i XOR w_j) XOR F2(w_i) XOR F2(w_j) XOR F2(0) (821 two-round evaluations) are all zero. QED.

The 780 values of (c) and the rank 40 of W40 are recomputed by the experiment program at every run, with its own
implementation of the organizer round function; a nonzero value stops the program. Consequently each of the 2^280
cosets t + span(W40) consists of 2^40 distinct parameters and 2^40 distinct messages (Lemma 1), and F2 is affine on it.

## 4. Degree and finite-difference enumeration

For a coset origin t let phi_t(u) = t XOR sum_j u_j w_j (u in F_2^40) and f_t(u) = b(A(phi_t(u))) in F_2^320.

**Lemma 4 (degree).** For every t and r = 2..6, every bit of the state after rounds 0 to r - 1 of A(phi_t(u)) has
algebraic degree at most 2^(r-2) in u. Hence every bit of f_t has degree at most 8, for every outer coset.

*Proof.* r = 2 is Lemma 3 (degree at most 1). Theta, rho and pi are linear and iota adds a constant; a chi output bit
a XOR (1 XOR a') a'' has degree at most twice the largest degree of its inputs. So each round at most doubles the
degree. f_t is a linear map of the state after five rounds. QED.

### 4.1 Derivatives

For f: F_2^n -> V (V a vector space over F_2), T a subset of {0..n-1} and y in F_2^n, let
D_T f(y) = XOR over S subset of T of f(y XOR e_S), e_S the indicator vector of S (D_T f = f for empty T). Write
s_T = sum over t in T of 2^t and, for nonempty T, R(T) = {b not in T : b + 1 in T}; as a bit mask
R(T) = (s_T >> 1) AND NOT s_T.
(P1) D_T f(y) does not depend on the coordinates of y in T.
(P2) For s not in T, D_{T + {s}} f(y) = D_T f(y XOR e_s) XOR D_T f(y).
(P3) If f = XOR over |S| <= d of a_S y^S (algebraic normal form, y^S = product of y_s over s in S), then
D_T f(y) = XOR over S containing T of a_S y^(S - T); so D_T f is the constant a_T when |T| = d, and 0 when |T| > d.
*Proof.* (P1) and (P2) follow from the definition. (P3): the derivative of y^S in direction e_s is y^(S - {s}) if s is
in S and 0 otherwise; iterate over T. QED.

### 4.2 Gray-order enumeration

Let f have degree at most D. For i >= 1 let t_1(i) < t_2(i) < ... be the set bits of i, L(i) = min(D, popcount(i)) and
T_j(i) = {t_1(i), ..., t_j(i)}. Algorithm FES (Bouillaguet et al., CHES 2010), with the initialization of Lemma 6:

- Initialization: x = f(0) and tab[T] = D_T f(g(s_T - 1)) for every T with 1 <= |T| <= D.
- Step i = 1, 2, ..., 2^n - 1: for j = L(i) - 1 down to 1, tab[T_j(i)] <- tab[T_j(i)] XOR tab[T_{j+1}(i)]; then
  x <- x XOR tab[T_1(i)].

**Lemma 5 (exactness).** After step i, x = f(g(i)).

*Proof.* (A) Let T be nonempty, m = max T, and i = s_T + k 2^(m+1) with k >= 0. Bit b of g(i) is bit b XOR bit b + 1 of
i; hence, outside T, the bits of g(i) below m are exactly R(T), and the bits above m are those of g(k) shifted by m + 1.
The anchor g(s_T - 1) differs from g(s_T) only in bit min T, which is in T, so by (P1) the initial value is
tab[T] = D_T f(g(s_T)).
(B) An entry tab[T] with |T| = j is changed at step i iff T = T_j(i) and j < L(i), that is iff j < D and
i = s_T + k 2^(m+1) with k >= 1; then T_{j+1}(i) = T + {u} with u = m + 1 + nu(k).
(C) Claim: whenever step i uses tab[T_j(i)] (as the top j = L(i), or after its update when j < L(i)), its value is
D_{T_j(i)} f(g(i)). Induction over the operations in execution order (i increasing; j decreasing within a step). Top
entry T' = T_{L(i)}(i): if |T'| = D it is constant by (P3); otherwise L(i) = popcount(i), so i = s_{T'}, T' was never
changed before (B), and its initial value is D_{T'} f(g(s_{T'})) by (A). Update of T = T_j(i), j < L(i), with
i = s_T + k 2^(m+1), k >= 1, and T' = T_{j+1}(i) = T + {u}: by the claim for T' (top, or updated just before in this
step), tab[T'] = D_{T'} f(g(i)). Before the update tab[T] holds D_T f(g(i')) with i' = s_T + (k - 1) 2^(m+1) (its
previous change by the claim, or the initial value when k = 1). By (A), g(i) and g(i') agree outside T except above m,
where they are g(k) and g(k - 1), which differ exactly in bit u. With (P1) and (P2):
tab[T] XOR tab[T'] = D_T f(g(i) XOR e_u) XOR D_T f(g(i) XOR e_u) XOR D_T f(g(i)) = D_T f(g(i)).
(D) By (C), x is XORed with D_{t_1(i)} f(g(i)) = f(g(i)) XOR f(g(i - 1)), since t_1(i) = nu(i). As x = f(g(0)) at
the start, x = f(g(i)) after step i. QED.

### 4.3 Initialization from evaluations of weight at most D

**Lemma 6.** Let A[S] = f(e_S) for every S with |S| <= D. Processing j = 0, ..., n - 1 and, for each j, every S
containing j with |S| <= D, the update A[S] <- A[S] XOR A[S - {j}] leaves A[S] = a_S. Then, for 1 <= |T| <= D,

    tab[T] = D_T f(g(s_T - 1)) = XOR of a_(T + V) over V subset of R(T) with |V| <= D - |T|,

and x = f(0) = a_S for S empty. This takes P_D = sum_{j<=D} C(n, j) evaluations of f, J_D = sum_{j<=D} j C(n, j)
vector XORs in the transform, and v_T = #{V subset of R(T) : |V| <= D - |T|} terms for tab[T].

*Proof.* Evaluating the normal form gives f(e_S) = XOR over S' subset of S of a_S'; by Moebius inversion
a_S = XOR over S' subset of S of f(e_S'). After the passes over coordinates 0..j, A[S] is the XOR of f(e_S') over the
S' subset of S that agree with S above j; the domain {|S| <= D} is closed under subsets, so every entry read exists.
By (A) of Lemma 5 the anchor y = g(s_T - 1) has exactly the bits R(T) outside T; by (P3),
D_T f(y) = XOR over S containing T of a_S y^(S - T), where y^V = 1 for V disjoint from T iff V is a subset of R(T),
and a_(T + V) = 0 when |T + V| > D. QED.

**Constants (n = 40, D = 8).** P_D = 100,146,724; J_D = 772,459,520; sum of L(i) over 1 <= i < 2^40 is
sum_k C(40, k) min(8, k) = 8,796,064,307,936. |R(T)| is the number of runs of ones of T that do not start at bit 0, so
exactly C(j, r) C(40 - j, r) sets T of size j have |R(T)| = r (compositions of the j ones and the 40 - j zeros), and
V_D = sum over T of v_T = sum_{j=1..8} sum_r C(j, r) C(40 - j, r) sum_{k <= min(r, 8 - j)} C(r, k) = 282,214,108.

## 5. Key, cone and the per-point schedule

### 5.1 Machine and addressing convention

The organizer machine is a 256-bit word RAM. Every executed primitive other than a permutation call is one word
operation: load, store, AND, OR, XOR, NOT, add, subtract, shift, comparison, conditional branch (on a nonzero register)
and register move. The machine has 64 registers; reading a register costs nothing. The program is generated
straight-line code: the 2^40 Gray sites, the setup and the table steps are unrolled, so an address or constant fixed
at generation time is an immediate operand of its instruction and costs no operation. Generating and storing this code
is charged in ONCE (Section 11.2).

- **Immediate:** the FES record addresses of every Gray site, the current-value frame, the 144 intermediate tile
  words, every setup operand (working frames, scalar frame, coefficient and derivative records), the basis constants
  w_b and q_b in two-word form, the butterfly masks, the per-site candidate constants (256 i + e) and (256 i + e) 2^128,
  and the region bases.
- **Computed at run time and charged:** the sparse and dense table addresses (Section 7), the coset-record address in
  the leader step and in verification (shift, add, second-word add), and the candidate decoding in verification.

### 5.2 Key and cone

For a message with pre-chi6 bits b, key is the 140-bit word whose bit 4z + x (x = 0..3, z = 0..34) is
b_{x,z} XOR (NOT b_{x+1,z} AND b_{x+2,z}). By Section 2 it equals digest bit z of lane x XOR RC[5]_z [x = 0], so
messages with equal digests have equal keys. Its inputs are exactly the 175 cone bits B[x, z] = b_{x,z}, x = 0..4,
z = 0..34. Verification always uses the native 256-bit digest, iota included.

### 5.3 Vertical FES

A group processes 256 cosets (lanes c = 0..255) in lockstep. Plane word (x, z) holds b_{x,z} of lane c at bit c. Every
bit of every plane word has degree at most 8 in u (Lemma 4), and Lemmas 5 and 6 use only XORs, which act bitwise, so
FES with D = 8 runs on 175-word vectors: a derivative record tab[T] of 175 words for each 1 <= |T| <= 8, and the
current values x of 175 words.

The current values B[0, z] (z < 35) and B[1, z] (z < 4), 39 words, stay in registers; the other 136 are in memory. At
step i, with L = L(i), each plane costs one LOAD of tab[T_L] (top), LOAD, XOR, STORE for each of the L - 1 links, and
for the current value one XOR (retained) or LOAD, XOR, STORE (in memory). Per step

    136 (3L + 1) + 39 (3L - 1) = 525 L + 97,

and per group, with the sum of Section 4.3,

    Fv = 525 * 8,796,064,307,936 + 97 (2^40 - 1) = 175 (3 * 8,796,064,307,936 + 2^40 - 1) - 78 (2^40 - 1)
       = 4,724,586,389,560,575.

Registers 1..39 hold the retained values, 40..55 a 16-word tile, 56..58 the dense count, the verification count and
the identifier word HB (Section 7), 59..64 are scratch: at most four in-memory current values of one z (B[0, z] is
always retained) and two chain temporaries. An in-memory value's final XOR lands in its scratch register, is stored,
and is read by chi from that register: no reload, no move.

### 5.4 Chi fused into the transpose: 4656 operations per Gray point and group

The 140 key rows (row 4z + x is a 256-bit word, bit c = key bit of lane c) are padded with 116 rows known to be zero to
a 256 x 256 bit matrix; write the row index as r = 16 tau + l (tile tau, local index l). A butterfly on rows k and
k + d with column shift s is

    t = ((A_k >> s) XOR A_{k+d}) AND mask_s;  A_k = A_k XOR (t << s);  A_{k+d} = A_{k+d} XOR t     [6 ALU]

with mask_s the ones in the low half of every 2s-bit block. For k with bit b clear (d = 2^b in the row index of the
stage) and s = 2^b it exchanges row-index bit b with column-index bit b: for every column c with bit b clear, the bits
(k, c + s) and (k + d, c) are swapped and all others kept. If A_{k+d} is known to be zero the same result is
A_{k+d} = (A_k >> s) AND mask_s, A_k = A_k AND mask_s [3 ALU]; pairs of two zero rows are omitted. After the eight
stages b = 0..7 the bit (r, c) has moved to (c, r): output word c holds the key of lane c in bits 0..139.

- **Tiles (row bits 0..3, s = 1, 2, 4, 8).** For tau = 0..8 and each z of the tile (z = 4 tau .. 4 tau + 3; tile 8 has
  z = 32, 33, 34): FES of B[0..4, z] (Section 5.3), then chi writes key rows 4(z - 4 tau) + x, x = 0..3, into the tile
  registers with one temporary: NOT, AND, XOR per row, 12 ALU per z. Then the four stages and 16 STOREs to fixed
  words. A full tile costs 4 x 48 = 192 ALU; tile 8 (local rows 12..15 known zero) costs 36, 36, 36, 48 = 156 ALU.
  All 144 intermediate words are written.
- **Columns (row bits 4..7, s = 16, 32, 64, 128).** For each l = 0..15: LOAD the nine words tau = 0..8 (tau = 9..15
  are known zero and never read); the four stages cost 27, 30, 36, 48 = 141 ALU. The 16 results are the keys of lanes
  c = 16 tau + l, handed to the table in registers in emission order e = 16 l + tau.

Per Gray point and group:

    35 * 12 + 8 * (192 + 16) + (156 + 16) + 16 * (9 + 141) = 4656   (ALU 4368, LOAD 144, STORE 144).

At point zero there is no FES step; the 175 current values are loaded once (39 into the retained registers, 136 as chi
inputs): 175 operations per group, charged in S_v.

## 6. Outer cosets and setup

### 6.1 The coset sequence

Extend the ordered W40 basis to a basis of F_2^320 by appending the coordinate vectors e_0, e_1, ... in increasing
order whenever they raise the rank; q_0, ..., q_87 are the first 88 appended vectors. Coset j (0 <= j < C = 256 G) has
representative t_j = XOR(q_b : bit b of g(j) is set). Group h (h < G) holds the cosets j = 256 h + c, c = 0..255. The
candidate (h, i, e) (Gray point i, emission index e = 16 l + tau, lane c = 16 tau + l) is the message
M(t_j XOR sum_b g(i)_b w_b) with j = 256 h + c; its identifier is cid = h 2^48 + 256 i + e < 2^128.

**Lemma 7 (distinct messages).** The Q = 2^48 G candidates are pairwise distinct messages.

*Proof.* g is a bijection of [0, 2^88), and W40 together with q_0..q_87 is linearly independent, so distinct j give
representatives in distinct cosets of span(W40). Inside a coset, distinct i give distinct g(i) and, by rank 40,
distinct parameters; Lemma 1 gives distinct messages. QED.

No randomness, random tape or duplicate rejection is used; H_coset (Section 12) is stated for this ordered sequence.

### 6.2 Leader step (at most 544 operations per coset)

For lane c of group h: j = H8 OR c with H8 = h * 2^8 (1); g = j XOR (j >> 1) (2); two zero moves (2); 88 unrolled
tests of bit b of g (shift, AND, compare, branch; two XORs of the constant q_b when set): 352 + 2 popcount(g(j)) <= 528;
the record address CSB + 2j (shift, add: 2); two STOREs of t_j into the global coset record with the second-word add
(3); two STOREs into the lane's working frame (2). This is 364 + 2 popcount(g(j)) <= 540 per coset. Group control
(H8, HB = h * 2^176, increment of h, compare with G, branch) is 5 per group, below 4 x 256. Charged: 544 per coset.

### 6.3 Direct evaluation (1416 + 2|S| per lane and point)

For each S with |S| <= 8 and each lane: LOAD the two working-frame words of t_j (2); XOR the |S| two-word basis
constants w_b, b in S (2|S|); initialize the 25 lanes (28: lanes 0..4 by three shifts and five 64-bit masks, five
copies into lanes 10..14, the padding lane 16 = 0x86 * 2^56, fourteen zero lanes); five rounds (242 each: theta
parities 20, D 25 with a 64-bit rotation costing two shifts, OR and AND, 4, application 25, rho 96 for the 24 nonzero
rotations, pi as register renaming, chi 75, iota 1); the linear step of round 5 (166); pack W0 = B0 | B1 << 64 |
B2 << 128 | B3 << 192 and V = B4 | B0 << 64 (8); two STOREs into the scalar frame (2). Total 1416 + 2|S|, and per
coset over all points 1416 P_D + 2 J_D.

### 6.4 Vertical conversion, transform and phase

For each point S and each of the 175 planes: move zero (1); for each lane LOAD, SHIFT, AND, SHIFT, OR (5); STORE into
the coefficient record A[S] (1): 1282 per plane and point, shifts by zero included. The truncated transform of Lemma 6
on the coefficient records costs two LOADs, XOR and STORE per pair (j, S) and plane: 4 * 175 * J_D. The phase
conversion writes the derivative records tab[T] (a frame disjoint from the coefficient records) with v_T LOADs,
v_T - 1 XORs and one STORE per plane: 2 * 175 * V_D. After both, the coefficient record A[{}] is the current-value
frame x = f(0).

**Valid access.** Every work word is written before it is read: the working frames by the leader step, the scalar
frame by the evaluations, A[S] by the conversion of point S (the transform reads only such records), tab[T] by the
phase conversion before the first Gray step, and the 144 tile words at every Gray point before its column step; the
next group's setup rewrites the frames before reading them. The coset record of j is written by the leader step before
any candidate of coset j exists.

### 6.5 Setup total

With C = 256 G cosets,

    S_v = C (1416 P_D + 2 J_D + 544) + G (1282 * 175 * P_D + 700 J_D + 350 V_D + 175)
        = 44,147,450,601,155,913,374,594,359,236,982,489,088 + 27,797,849,092,903,751,682,894,021,672,812,263,875
        = 71,945,299,694,059,665,057,488,380,909,794,752,963.

## 7. Sparse-set table and verification

The table is a Briggs-Torczon sparse set over the 140-bit key: SPARSE[k] at word address 2^200 OR k (k < 2^140),
DENSE[x] at 2^201 OR x (x < Q), and a count register (starting at zero, always below Q). A sparse word is
SPARSE[k] = cid 2^128 + x. HB = h 2^176 is a register set once per group. The probe of key k for candidate
cid = h 2^48 + 256 i + e executes exactly:

```
a = k OR 2^200;  s = LOAD [a]                    2   (s is arbitrary if the word was never written)
x = s AND (2^128 - 1)                            1
f = (x < count);  BRANCH                         2   bound test fails -> miss       (11 with the miss)
d = LOAD [x OR 2^201]                            2
f = (d == k);  BRANCH                            2   dense test fails -> miss       (15 with the miss)
hit:  cid' = s >> 128                            1   -> verification of cid' against cid (10)
miss: STORE [count OR 2^201] = k                 2
      STORE [a] = (HB OR (256 i + e) 2^128) OR count   3
      count = count + 1                          1
```

Every candidate costs at most 15 table operations, charged as 15 Q.

**Lemma 8 (sparse set, any initial memory).** At every probe: (a) DENSE[0..count) holds distinct keys, each written by
a miss; (b) for every key k that has missed, SPARSE[k] = cid_k 2^128 + x_k with x_k < count and DENSE[x_k] = k, where
cid_k is the first candidate with key k; (c) the probe of k hits iff k has missed before, and then returns cid_k.

*Proof.* Induction over probes. If k has missed before, SPARSE[k] was written at that miss and is written only by
misses of k, of which there is one by (c); so x = x_k < count and DENSE[x_k] = k: a hit returning cid_k. If k has not
missed, no entry of DENSE[0..count) equals k (each holds a key that missed), so whatever value the sparse word has,
either x >= count or DENSE[x] != k: a miss, which writes DENSE[count] = k and SPARSE[k] and increments count,
preserving (a) and (b). DENSE is read only below count, at written words. QED.

No word is initialized and no initial content matters: Lemma 8 is the valid-access argument for the never-written
sparse array.

**Verification (at most 4096 operations: two permutation calls, 2 x 1626 = 3252, and at most 844 others).** The
verification count F is incremented, compared with R140 and branched on (3); the current identifier is
(HB >> 128) OR (256 i + e) (2). For each of the two identifiers: e = cid AND 255; i = (cid >> 8) AND (2^40 - 1);
c = ((e AND 15) << 4) OR (e >> 4); j = ((cid >> 48) << 8) OR c; the record address CSB + 2j; two LOADs of t_j with the
second-word add; g(i) = i XOR (i >> 1) (17 together); 40 unrolled tests of g(i) (shift, AND, compare, branch, and two
XORs of w_b when set: at most 240); the 28-operation lane initialization of Section 6.3; one permutation call
returning the native digest lanes 0..3. Then at most four compares and branches (8). Total at most
3 + 2 + 2 (17 + 240 + 28) + 8 = 583 <= 844.
If F reaches R140 the run stops (failure).

**Address map (words).** Coset records [2^90, 2^90 + 2C); work frames from 2^91 (fewer than 2^36 words); generated
code from 2^92 (fewer than 2^58 words); SPARSE [2^200, 2^200 + 2^140); DENSE [2^201, 2^201 + Q). The regions are
disjoint and every address is below 2^202, a representable 256-bit word.

## 8. The algorithm CAMP

```
Preprocessing (once, Section 11.2): generate the code, constants q_b, w_b and masks; check rank and the
  780 polarizations of Lemma 3; count = 0; F = 0.
For h = 0, 1, ..., G - 1:
  Setup (Section 6): leader step of the 256 cosets j = 256 h + c; for every |S| <= 8 the direct evaluations
    and the conversion; the transform; the phase conversion; the 175 point-zero loads.
  For i = 0, 1, ..., 2^40 - 1 (Gray site i):
    if i >= 1: FES step i on the 175 planes, interleaved with chi (Sections 5.3, 5.4)
    chi and transpose: the 256 keys of the candidates (h, i, e), e = 0..255
    for e = 0..255: probe the key (Section 7); on a hit with cid': verification of cid' against (h, i, e);
      if the digests are equal, output the two messages and stop; if F reached R140, stop with failure
Stop with failure.
```

Every bound (G groups, 2^40 sites, R140 verifications) is a halt of the algorithm, and every candidate is probed
exactly once, so the operation count of Section 10 is an upper bound for every run.

## 9. Success

Let G = 1,202,983,983,186,596,773,302,061, C = 256 G = 307,963,899,695,768,773,965,327,616 cosets,
Q = 2^48 G = 338,609,888,650,739,515,842,329,177,253,285,462,016 candidates, lambda = Q(Q - 1)/2^257 =
0.4950971065781406283285354... and T8 = sum_{k=0..8} lambda^k / k!.

**Lemma 9 (detection).** Suppose the candidates contain two with equal digests, the run does not stop at the R140 cap,
and there is no bad triple: candidates A, B, C, A not in {B, C}, with digest(B) = digest(C), key(A) = key(B) and
digest(A) != digest(B). Then CAMP outputs a collision.

*Proof.* Let C be the first candidate in probe order that has an earlier candidate B with the same digest, and k its
key. By Lemma 8 the probe of C hits and returns the first candidate A0 with key k (A0 precedes or equals B). If
digest(A0) = digest(B), the verification of A0 against C finds equal digests and CAMP outputs the distinct messages
(Lemma 7). Otherwise A0 != B; A0 has the key of B and C and a different digest, a bad triple. QED.

**Theorem.** Under H_coset, CAMP outputs a collision with probability greater than 0.39.

*Proof.* Under H_coset the Q digests are independent and uniform, and the keys (140 digest bits XOR constants) are
independent and uniform 140-bit values. Three failure events:
(i) no two candidates have equal digests: probability prod_{k=1}^{Q-1} (1 - k 2^-256) <= exp(-lambda) <= 1/T8;
(ii) the R140 cap: every verification follows a hit, which pairs the probing candidate with an earlier candidate of
equal key, so the number of verifications is at most the number X of unordered equal-key pairs. Pair indicators are
pairwise independent (two pairs sharing a candidate agree with probability 2^-280), so Var X <= E X = Q(Q - 1)/2^141.
With r140 = ceil(E X) = 41,131,058,418,485,797,237,694,361,103,441,075 and
R140 = r140 + ceil(sqrt(4096 r140)) = 41,131,058,418,485,810,217,402,188,405,172,195, Chebyshev's inequality gives
Pr(X >= R140) <= E X / (R140 - E X)^2 <= 1/4096;
(iii) a bad triple: the expected number of bad triples is at most C(Q, 2) (Q - 2) 2^-256 2^-140 = lambda (Q - 2)/2^140
= 0.000120279228079444... < 1/4096.
By Lemma 9 the failure probability is at most 1/T8 + 1/4096 + lambda (Q - 2)/2^140 < 1/T8 + 2/4096, and the exact
rational comparison (integer numerators) gives

    1/T8 + 2/4096 = 0.6099999999999999999999998788990635... < 61/100.

Hence the success probability is greater than 0.3900000000000000000000001211. QED.

## 10. Cost ledger and certificate

All charges are word operations of Section 5.1; a permutation call is 1626 of them (it appears only in verification).

| term | value |
|---|---|
| FES, G Fv | 5,683,601,753,822,762,708,749,062,472,441,531,845,075 |
| chi and transpose, G * 4656 * 2^40 | 6,158,467,349,835,324,944,382,361,911,294,129,340,416 |
| setup, S_v (Section 6.5) | 71,945,299,694,059,665,057,488,380,909,794,752,963 |
| table, 15 Q | 5,079,148,329,761,092,737,634,937,658,799,281,930,240 |
| verification, 4096 R140 | 168,472,815,282,117,878,650,479,363,707,585,310,720 |
| preprocessing, ONCE = 2^70 + 16 | 1,180,591,620,717,411,303,440 |

    N = G Fv + G 4656 2^40 + S_v + 15 Q + 4096 R140 + ONCE
      = 17,161,635,548,395,357,935,654,921,407,869,734,482,854,

about 50.6826 operations per candidate. The time is N/1626 target compressions, and the integer certificate

    1626^100000 * 2^12298919 <= N^100000 < 1626^100000 * 2^12298920

gives log2(N/1626) = 122.9891993..., so time_log2 = 122.98920 (rounded up at the fifth decimal).

## 11. Memory, preprocessing and advice

### 11.1 Memory

SPARSE: 2^140 words (never initialized); DENSE: Q words; coset records: 2C words; work frames: scalar frame 512,
working frames 512, tile words 144, coefficient and derivative records 2 * 175 * P_D (fewer than 2^36 words in all);
generated code and its constants: fewer than 2^58 words. The regions are disjoint (Section 7), so memory is below
2^140 + 2^128 + 2^89 + 2^36 + 2^58 < 2^141 words of 32 bytes, below 2^146 bytes.

### 11.2 Preprocessing: ONCE <= 2^70 + 16 operations

(a) **Code generation.** Each of the 2^40 Gray sites is decoded (its set bits and the record addresses of T_1..T_L)
in fewer than 2^14 operations and emits at most 525 * 8 + 97 + 4656 + 15 * 256 = 12,793 < 2^14 instructions; the
setup code (per point, transform pair, phase term and lane) has fewer than 2^46 instructions. At four words per
instruction the code is below 2^58 words and is generated in fewer than 2^60 operations.
(b) **Constants and certificate.** q_0..q_87 (rank extension of W40 by coordinate vectors, at most 320 reductions
against 320 pivots), the two-word forms of w_b and q_b, the eight butterfly masks, rank 40 and the 780 polarizations of
Lemma 3 (821 two-round evaluations): fewer than 2^25 operations.
(c) **The search that produced W40 (deterministic).** Step 1: the linear parts of the 1600 coordinates before the chi
of round 1 (affine in t by Lemma 2) from 321 evaluations (t = 0 and the 320 unit vectors). Step 2: greedy
restriction: keep a list E of linear constraints in echelon form; while some product pair of round-1 chi (the forms f
and g of adjacent coordinates a_{x+1}, a_{x+2} of one row and slice, 1600 pairs) is violated (f, g and f XOR g all
nonzero modulo E), append the constraint among {f, g, f XOR g} of the violated pairs that occurs most often, then of
minimum weight, then of smallest integer value; each step lowers the dimension by one, so at most 320 steps, each
reducing at most 3200 forms against at most 320 pivots and sorting at most 4800 candidates; the result is the
35-dimensional space spanned by w_0..w_34, checked by its 595 polarizations. Step 3: the kernel K of the linear map
x -> (B(x, w_i))_{i<35} (columns from 320 x 35 x 4 two-round evaluations; Gaussian elimination of 320 vectors of
56,000 bits), the polar form on a basis of K / span(w_0..w_34) (6 vectors, 15 polarizations), and a maximal totally
isotropic extension (its radical and one line), giving w_35..w_39; then the rank and 780-polarization check above.
With two-round evaluations below 2^12 operations each, steps 1 to 3 cost fewer than 2^34 operations.
(d) **One-time control.** count = 0 and F = 0, at most 16 operations.

The total is below 2^60 + 2^35 + 16 < 2^70 + 16 = ONCE, which is in N. In target compressions ONCE/1626 < 2^59.34;
the claim declares preprocessing_log2 = 70.

### 11.3 Advice

None. Every constant used by CAMP is produced by the procedures of Section 11.2, whose cost is in N.

## 12. Premise H_coset and evidence

**Statement.** The full 256-bit digests of the Q native messages of Section 6.1, taken in CAMP's order (groups
h = 0..G - 1, cosets j = 256 h + c, Gray points g(i) of span(W40) in each coset), are independent and uniformly
distributed. It is used only through the three events (i)-(iii) of Section 9.

This is assumed, not proved. The concern it answers: on a coset every digest bit is a polynomial of degree at most 16
in the 40 inner variables (Lemma 4 and the last chi), so equal-digest pairs inside a coset, or across the cosets of the
sequence, could be rarer than for uniform values.

**Evidence (preregistered, our runs).** Three batches, each fixed in a protocol file hashed before its runs
(PREREG.txt, SHA-256 67e381a2c0dececee0ce10a8ac4591304076a161259e1cb9045f2c87df54fa58; PREREG2.txt, SHA-256
3b49de9f7c931d51a66ec7f31c2b0c4e3227bc8047cfd25ab5f727207bc01b4c; PREREG3.txt, SHA-256
5f94fcd22a4d94dddeef79ebc91f47b858793804e7d47e6784862e46479efc6a): sizes, statistics and the pass rule (every count of
the tested inputs at least expected - 4 sigma, sigma = sqrt(expected); no reruns). The GPU program computes real
six-round SHA3-256 digests of the messages M(t) (validated against the organizer reference sha3_256(rounds=6) on
2,048 of 2,048 digests for batches 1-2 and 512 of 512 for batch 3). Each run has 2^30 messages in ncos complete
cosets of dimension n. Field runs (batches 1-2): uniform origins, n random independent elements of span(W40);
control runs: n random 320-bit directions; deterministic runs (batch 3): exactly the sequence of Section 6.1, cosets
j = 0..ncos - 1 with the first n ordered vectors of W40 (the first 2^n Gray points of each coset). Counts are exact
numbers of equal-key pairs: within-coset pairs with equal low 32 bits of digest lane L, expected
ncos C(2^n, 2) 2^-32; global pairs among all 2^30 messages with equal low 44 bits of lane L, expected
C(2^30, 2) 2^-44 = 32,767.99997; z = (count - expected)/sqrt(expected).

| run | inputs | lane | within-coset pairs | expected | z | global pairs | z |
|---|---|---|---:|---:|---:|---:|---:|
| R1 | field, n = 20, 1024 cosets | 0 | 131,380 | 131,071.875 | +0.85 | 33,033 | +1.46 |
| R2 | field, n = 20, 1024 cosets | 3 | 130,720 | 131,071.875 | -0.97 | 32,964 | +1.08 |
| R3 | control, n = 20, 1024 cosets | 0 | 131,300 | 131,071.875 | +0.63 | 32,762 | -0.03 |
| R4 | control, n = 20, 1024 cosets | 3 | 130,930 | 131,071.875 | -0.39 | 32,709 | -0.33 |
| R5 | field, n = 24, 64 cosets | 0 | 2,097,299 | 2,097,151.875 | +0.10 | 32,651 | -0.65 |
| R6 | control, n = 24, 64 cosets | 0 | 2,098,309 | 2,097,151.875 | +0.80 | 32,777 | +0.05 |
| S1 | field, n = 20, 1024 cosets | 1 | 130,589 | 131,071.875 | -1.33 | 32,932 | +0.91 |
| S2 | field, n = 20, 1024 cosets | 2 | 130,672 | 131,071.875 | -1.10 | 32,606 | -0.89 |
| S3 | control, n = 20, 1024 cosets | 1 | 130,638 | 131,071.875 | -1.20 | 32,925 | +0.87 |
| S4 | control, n = 20, 1024 cosets | 2 | 131,237 | 131,071.875 | +0.46 | 32,715 | -0.29 |
| S5 | field, n = 28, 4 cosets | 0 | 33,555,785 | 33,554,431.875 | +0.23 | 32,648 | -0.66 |
| S6 | field, n = 28, 4 cosets | 2 | 33,557,768 | 33,554,431.875 | +0.58 | 32,736 | -0.18 |
| S7 | control, n = 28, 4 cosets | 0 | 33,566,477 | 33,554,431.875 | +2.08 | 32,926 | +0.87 |
| D1 | sequence, n = 20, j = 0..1023 | 0 | 131,053 | 131,071.875 | -0.05 | 32,666 | -0.56 |
| D2 | sequence, n = 20, j = 0..1023 | 3 | 131,447 | 131,071.875 | +1.04 | 32,846 | +0.43 |
| D3 | sequence, n = 24, j = 0..63 | 1 | 2,095,169 | 2,097,151.875 | -1.37 | 32,689 | -0.44 |
| D4 | sequence, n = 24, j = 0..63 | 2 | 2,095,504 | 2,097,151.875 | -1.14 | 32,710 | -0.32 |

Verdict under the preregistered rule: all three batches pass. Over 17 runs, all four digest lanes and cosets of 2^20,
2^24 and 2^28 messages, every count lies within 2.1 sigma of its expectation, no count is below expected - 1.4 sigma,
and field, control and deterministic runs agree.

**Scope and extrapolation.** The evidence covers 32-bit within-coset and 44-bit global projections of single digest
lanes, 2^30 messages per run, subspaces of dimension 20 to 28 of span(W40), random origins (batches 1-2) and the exact
deterministic sequence of Section 6.1 (batch 3). The premise extrapolates to the full 256-bit digest, to complete
40-dimensional cosets, to all C = 256 G cosets of the sequence and to Q messages.

**Limits.** No proof is known. Image size and balance do not imply it: a balanced linear map onto F_2^256 can be
injective on every translate of a campaign space, so its campaigns contain no collision at all. No such structure is
known for the native function and none is excluded by proof. The experiment of Section 13 tests nothing about H_coset.

## 13. Experiment

`experiments/fes_campaign.py` (Python standard library) executes the schedule of Sections 5 to 7 at a reduced size on
the organizer's trials.

- Once per run: the program's six-round SHA3-256 equals the organizer reference on M(0) and M(w_0 XOR w_39)
  (hard-coded known-answer digests), and its 24-round version equals hashlib.sha3_256 on both; rank(W40) = 40; the 780
  polarizations of Lemma 3 vanish. A failed check stops the program.
- Groups: trials 256g .. 256g + 255 form one group; its index is h = int(seed of the group's first trial, 16) mod G,
  and trial k is lane c = k mod 256 of the cosets j = 256 h + c of Section 6.1.
- Reduced size: the first 2^9 Gray points of each coset (directions w_0..w_8), D = 8, all 175 planes, the full
  140-bit key and the sparse-set table of Section 7 with Q' = 2^17 candidates and the verification cap of the same
  formula (65).
- Every operation of the leader step, the setup schedule, the FES steps, chi and transpose, the table and
  verification runs through a counting machine (one call per primitive of Section 5.1; a permutation call counted
  apart), and the program stops unless the executed counts equal the formulas above: 525 L(i) + 97 per Gray step,
  175 point-zero loads, 4656 per point, 11 / 15 / 10 table operations per candidate, 364 + 2 popcount(g(j)) per
  coset (at most 540) and 5 per group, 1416 + 2|S| per evaluation, 1282 per plane conversion, 4 * 175 J_D and
  2 * 175 V_D for transform and phase, at most 844 operations and two permutation calls per verification.
- Setup values of lanes 1..255 at points S other than the empty set come from a bit-sliced evaluation (not counted);
  the counted schedule of Section 6.3 runs on lane 0 at every point and, with the conversion of Section 6.4, on all
  lanes at the empty set, and must equal it. Never-written sparse words read as a fixed pseudo-random function of
  their address whose index field lies below 2 Q', so fresh keys often reach the dense test (an arbitrary initial
  memory); a read of a never-written work, dense or coset word stops the program.
- Beside the algorithm, not counted: at point i the message of lane i mod 256 is hashed natively and its 140 key bits
  are compared with the emitted key (key_mismatch); after the run the first candidate's key is probed again (a valid
  hit, 10 operations) and verified against the candidate (i, e) = (1, 5), with the reconstructed sources and digests
  compared with the native ones.

Per trial the program reports 16 numbers, the same for all trials of a group: gray_points = 512; fes_ops = 1,258,642
(525 * 2,303 + 97 * 511); chi_transpose_ops = 2,383,872 (4656 * 512); point_zero_loads = 175; table_ops = 11 (2^17 -
m - x) + 15 x + 10 m with x = in_range_mismatches and m = key_matches; dense_count = 2^17 - m; leader_ops =
364 * 256 + 2 sum popcount(g(j)) + 5; evaluation_ops = 1,089,246; conversion_ops = 224,350; transform_phase_ops =
2,419,200; verify_check_ops (at most 10 + 844); perm_calls = 2 + 2 m; native_checks = 512; key_mismatch = 0. No trial
returns a pair: a 256-bit collision among 2^17 messages has probability below 2^-222. Nothing about cost or about
H_coset is inferred from the run.

## 14. Credits

- GPT Sol cloud: the two-round affine field and its certificate.
- GPT Sol local and GPT Luna: the exact ledger (initialization, schedule, setup, table and success).
- Grok: transpose and table code and executed operation counts.
- Bouillaguet, Chen, Cheng, Chou, Niederhagen, Shamir and Yang, CHES 2010: fast exhaustive search by Gray-code finite
  differences.
- Th0rgal (76ccfa1c): the earlier remark that the digest's degree in a 32-bit counter is at most 32 (prior context).
- Jbenisek: the preregistered H_coset runs, the kernel checks, the package and the experiment program.
