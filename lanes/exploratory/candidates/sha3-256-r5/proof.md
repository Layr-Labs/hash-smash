# SHA3-256 with 5 prefix rounds: Gray-order enumeration of two-round-affine cosets, time_log2 123.1760

## 1. Claim

Target `sha3-256-r5-prefix-v1` (organizer profile): SHA3-256 of FIPS 202 with "prefix rounds 0 through 4, inclusive,
in every sponge permutation" (not the last-round convention of Keccak-p); all-zero 1600-bit initial state; rate 1088
bits, capacity 512; "SHA3 domain suffix 01 followed by pad10*1; delimited suffix byte 0x06", standard little-endian
lane and bit encoding; the digest is the first 32 squeeze bytes; messages are distinct byte strings of bit length
below 2^64; reference `verifier/keccak.py:sha3_256`. Postcondition: "The two complete sha3-256-r5 sponge hashes agree
on all 256 output bits." The algorithm CAMP of Section 8 outputs two distinct 135-byte messages with equal digests.

| Quantity | Value |
|---|---|
| time_log2 (collision-frontier-v5, reference operation cost 1355, rounded up) | 123.1760 (Section 10) |
| success probability | at least 0.39 over the algorithm's coins, under premise H_coset (Sections 9 and 12) |
| memory | below 2^141 words of 256 bits, below 2^146 bytes (Section 11.1) |
| preprocessing (included in time) | at most 2^70 + 16 word operations, below 2^59.60 target compressions (Section 11.2) |
| nonuniform advice | none |

One premise is declared (Section 12): **H_coset**, first- and second-moment rate conditions on the digests of the
messages CAMP enumerates from independent uniform coset origins. The rate of equal-digest pairs is at least, and the
rates of two equal-digest pairs (sharing a candidate, or disjoint) are at most, the values of uniform digests; with
the Paley-Zygmund inequality this bounds the probability that a collision exists (Section 9). The mean and variance
of the 140-bit false-match count and the bad-triple rate are at most the values of uniform digests. No occupancy or
tail bound is assumed. Its evidence includes an organizer-executed reduced-width test (Sections 12.2 and 13).
Everything else is proved here: two-round affinity on every coset of W40, degree at most 4 before the last chi,
exactness of the Gray-order finite differences and of their initialization, correctness of the sparse-set table for
arbitrary initial memory, the duplicate-coset bound, the second-moment identity, and every operation count.

## 2. Notation and messages

A state is 25 little-endian 64-bit lanes S[x + 5y] (x, y in 0..4); bit z of lane k is state bit 64k + z. Round r
(r = 0..4) is theta, rho, pi, chi, iota with constant RC[r] as in the reference; P5 is rounds 0 to 4. XOR is
addition over F_2. For t in F_2^320 let u_k(t) (k = 0..4) be bits 64k to 64k + 63 of t.

**Messages.** M(t) = U || 0^40 || U || 0^15 (135 bytes) with U = LE64(u_0) || ... || LE64(u_4). The padding of the
profile appends 0x06 and the final bit 0x80, which share byte 135, so M(t) is one 136-byte block A(t): lanes 0 to 4
and lanes 10 to 14 hold u_0 .. u_4, lane 16 holds 0x86 * 2^56, all other lanes (and the capacity) are zero. H(M(t)) is
lanes 0 to 3 of P5(A(t)): one permutation call per message.

**Lemma 1 (messages).** t -> M(t) is injective, and every M(t) is a message of the target domain whose hash is the
first 32 bytes of P5(A(t)).

*Proof.* The first 40 bytes of M(t) are t in little-endian order. The block is the profile's padding of a 135-byte
string (135 = 136 - 1, so the suffix and the final bit fall in byte 135), absorbed into the zero state. QED.

**Pre-chi4 bits.** For a block A let b(A) in F_2^320 be row y = 0 after theta, rho and pi of round 4 applied to
rounds 0 to 3 of A: bits b_{x,z}, lane x = 0..4, bit z = 0..63. Digest lane x (x = 0..3), bit z, is
b_{x,z} XOR (NOT b_{x+1,z} AND b_{x+2,z}) XOR RC[4]_z [x = 0] (lane indices mod 5; RC[4] = 0x000000000000808B sets
bits 0, 1, 3, 7 and 15 of lane 0).

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

**Lemma 4 (degree).** For every t and r = 2..5, every bit of the state after rounds 0 to r - 1 of A(phi_t(u)) has
algebraic degree at most 2^(r-2) in u. Hence every bit of f_t has degree at most 4, for every outer coset.

*Proof.* r = 2 is Lemma 3 (degree at most 1). Theta, rho and pi are linear and iota adds a constant; a chi output bit
a XOR (1 XOR a') a'' has degree at most twice the largest degree of its inputs. So each round at most doubles the
degree. f_t is a linear map of the state after four rounds. QED.

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

**Constants (n = 40, D = 4).** P_D = 102,091; J_D = 396,800; sum of L(i) over 1 <= i < 2^40 is
sum_k C(40, k) min(4, k) = 4,398,046,499,540. |R(T)| is the number of runs of ones of T that do not start at bit 0, so
exactly C(j, r) C(40 - j, r) sets T of size j have |R(T)| = r (compositions of the j ones and the 40 - j zeros), and
V_D = sum over T of v_T = sum_{j=1..4} sum_r C(j, r) C(40 - j, r) sum_{k <= min(r, 4 - j)} C(r, k) = 131,731.

## 5. Key, cone and the per-point schedule

### 5.1 Machine and addressing convention

The organizer machine is a 256-bit word RAM. Every executed primitive other than a permutation call is one word
operation: load, store, AND, OR, XOR, NOT, add, subtract, shift, comparison, conditional branch (on a nonzero register),
register move and an independent uniform random 256-bit word. The machine has 64 registers; reading a register
costs nothing. The program is generated
straight-line code: the 2^40 Gray sites, the setup and the table steps are unrolled, so an address or constant fixed
at generation time is an immediate operand of its instruction and costs no operation. Generating and storing this code
is charged in ONCE (Section 11.2).

- **Immediate:** the FES record addresses of every Gray site, the current-value frame, the 144 intermediate tile
  words, every setup operand (working frames, scalar frame, coefficient and derivative records), the basis constants
  w_b in two-word form, the butterfly masks, the per-site candidate constants 256 i + e, and the region bases.
- **Computed at run time and charged:** the sparse, dense and identifier addresses (Section 7), the coset-record
  address in the leader step and in verification (shift, add, second-word add), and the candidate decoding in
  verification.

### 5.2 Key and cone

For a message with pre-chi4 bits b, key is the 140-bit word whose bit 4z + x (x = 0..3, z = 0..34) is
b_{x,z} XOR (NOT b_{x+1,z} AND b_{x+2,z}). By Section 2 it equals digest bit z of lane x XOR RC[4]_z [x = 0], so
messages with equal digests have equal keys. Its inputs are exactly the 175 cone bits B[x, z] = b_{x,z}, x = 0..4,
z = 0..34. Verification always uses the native 256-bit digest, iota included.

### 5.3 Vertical FES

A group processes 256 cosets (lanes c = 0..255) in lockstep. Plane word (x, z) holds b_{x,z} of lane c at bit c. Every
bit of every plane word has degree at most 4 in u (Lemma 4), and Lemmas 5 and 6 use only XORs, which act bitwise, so
FES with D = 4 runs on 175-word vectors: a derivative record tab[T] of 175 words for each 1 <= |T| <= 4, and the
current values x of 175 words.

The current values B[0, z] (z < 35) and B[1, z] (z < 4), 39 words, stay in registers; the other 136 are in memory. At
step i, with L = L(i), each plane costs one LOAD of tab[T_L] (top), LOAD, XOR, STORE for each of the L - 1 links, and
for the current value one XOR (retained) or LOAD, XOR, STORE (in memory). Per step

    136 (3L + 1) + 39 (3L - 1) = 525 L + 97,

and per group, with the sum of Section 4.3,

    Fv = 525 * 4,398,046,499,540 + 97 (2^40 - 1) = 175 (3 * 4,398,046,499,540 + 2^40 - 1) - 78 (2^40 - 1)
       = 2,415,627,040,152,675.

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

### 6.1 The cosets and the coins

Coset j (0 <= j < C = 256 G) has origin t_j = r_{j,0} + 2^256 (r_{j,1} AND (2^64 - 1)), where r_{j,0} and r_{j,1} are
two fresh independent uniform random 256-bit words drawn by the leader step of coset j (Section 6.2). These 2C words
are the algorithm's coins, and every probability below is over them, with the target fixed; the origins t_j are
independent and uniform on F_2^320, and nothing else is random. Group h (h < G) holds the cosets j = 256 h + c,
c = 0..255. The candidate (h, i, e) (Gray point i, emission index e = 16 l + tau, lane c = 16 tau + l) is the message
M(t_j XOR sum_b g(i)_b w_b) with j = 256 h + c; its identifier is cid = h 2^48 + 256 i + e < Q < 2^129.

**Lemma 7 (distinct messages).** Let DUP be the event that t_j XOR t_j' lies in span(W40) for some j < j'. Then
Pr[DUP] <= C(C, 2) 2^-280 < 2^-104, and outside DUP the Q = 2^48 G candidates are pairwise distinct messages.

*Proof.* For j < j', t_j XOR t_j' is uniform on F_2^320 and span(W40) has 2^40 elements (rank 40), so each pair
contributes exactly 2^-280; take the union bound over the C(C, 2) pairs. Outside DUP the C cosets t_j + span(W40) are
pairwise distinct, hence disjoint. Inside a coset, distinct i give distinct g(i) and, by rank 40, distinct parameters;
Lemma 1 gives distinct messages. QED.

### 6.2 Leader step (11 operations per coset, charged 544)

For lane c of group h: j = H8 OR c with H8 = h * 2^8 (1); the two random words r_{j,0} and r_{j,1} (2); r_{j,1} AND
(2^64 - 1) (1); the record address CSB + 2j (shift, add: 2); two STOREs of t_j into the global coset record with the
second-word add (3); two STOREs into the lane's working frame (2). This is 11 per coset. Group control (H8,
HB = h * 2^48, increment of h, compare with G, branch) is 5 per group. The ledger charges 544 per coset, an upper
bound for 11 + 5/256.

### 6.3 Direct evaluation (1174 + 2|S| per lane and point)

For each S with |S| <= 4 and each lane: LOAD the two working-frame words of t_j (2); XOR the |S| two-word basis
constants w_b, b in S (2|S|); initialize the 25 lanes (28: lanes 0..4 by three shifts and five 64-bit masks, five
copies into lanes 10..14, the padding lane 16 = 0x86 * 2^56, fourteen zero lanes); four rounds (242 each: theta
parities 20, D 25 with a 64-bit rotation costing two shifts, OR and AND, 4, application 25, rho 96 for the 24 nonzero
rotations, pi as register renaming, chi 75, iota 1); the linear step of round 4 (166); pack W0 = B0 | B1 << 64 |
B2 << 128 | B3 << 192 and V = B4 | B0 << 64 (8); two STOREs into the scalar frame (2). Total 1174 + 2|S|, and per
coset over all points 1174 P_D + 2 J_D.

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

    S_v = C (1174 P_D + 2 J_D + 544) + G (1282 * 175 * P_D + 700 J_D + 350 V_D + 175)
        = 42,266,008,514,916,720,505,101,877,555,898,880 + 31,786,235,884,063,797,347,906,359,573,584,375
        = 74,052,244,398,980,517,853,008,237,129,483,255.

## 7. Sparse-set table and verification

The table is a Briggs-Torczon sparse set over the 140-bit key: SPARSE[k] at word address 2^200 OR k (k < 2^140)
holds a dense index; DENSE[x] at 2^201 OR x and CID[x] at 2^202 OR x (x < Q) hold the key and the identifier of the
candidate that inserted it; a count register starts at zero and stays below Q. (Q is above 2^128, so an identifier and
a dense index do not fit together in one word.) HB = h 2^48 is a register set once per group. The probe of key k for
candidate cid = h 2^48 + 256 i + e executes exactly:

```
a = k OR 2^200;  x = LOAD [a]                    2   (x is arbitrary if the word was never written)
f = (x < count);  BRANCH                         2   bound test fails -> miss       (11 with the miss)
d = LOAD [x OR 2^201]                            2
f = (d == k);  BRANCH                            2   dense test fails -> miss       (15 with the miss)
hit:  cid' = LOAD [x OR 2^202]                   2   -> verification of cid' against cid (10)
miss: STORE [count OR 2^201] = k                 2
      STORE [count OR 2^202] = HB OR (256 i + e) 3
      STORE [a] = count                          1
      count = count + 1                          1
```

Every candidate costs at most 15 table operations, charged as 15 Q.

**Lemma 8 (sparse set, any initial memory).** At every probe: (a) DENSE[0..count) holds distinct keys, each written by
a miss; (b) for every key k that has missed, SPARSE[k] = x_k < count, DENSE[x_k] = k and CID[x_k] = cid_k, where
cid_k is the first candidate with key k; (c) the probe of k hits iff k has missed before, and then returns cid_k.

*Proof.* Induction over probes. If k has missed before, SPARSE[k] was written at that miss and is written only by
misses of k, of which there is one by (c); so x = x_k < count, DENSE[x_k] = k and CID[x_k] = cid_k: a hit returning
cid_k. If k has not missed, no entry of DENSE[0..count) equals k (each holds a key that missed), so whatever value the
sparse word has, either x >= count or DENSE[x] != k: a miss, which writes DENSE[count] = k, CID[count] and SPARSE[k]
and increments count, preserving (a) and (b). DENSE and CID are read only below count, at written words. QED.

No word is initialized and no initial content matters: Lemma 8 is the valid-access argument for the never-written
sparse array.

**Verification (at most 3554 operations: two permutation calls, 2 x 1355 = 2710, and at most 844 others).** The
verification count F is incremented, compared with R140 and branched on (3); the current identifier is
HB OR (256 i + e) (1). For each of the two identifiers: e = cid AND 255; i = (cid >> 8) AND (2^40 - 1);
c = ((e AND 15) << 4) OR (e >> 4); j = ((cid >> 48) << 8) OR c; the record address CSB + 2j; two LOADs of t_j with the
second-word add; g(i) = i XOR (i >> 1) (17 together); 40 unrolled tests of g(i) (shift, AND, compare, branch, and two
XORs of w_b when set: at most 240); the 28-operation lane initialization of Section 6.3; one permutation call
returning the native digest lanes 0..3. Then at most four compares and branches (8). Total at most
3 + 1 + 2 (17 + 240 + 28) + 8 = 582 <= 844.
If F reaches R140 the run stops (failure).

**Address map (words).** Coset records [2^90, 2^90 + 2C); work frames from 2^91 (fewer than 2^36 words); generated
code from 2^92 (fewer than 2^58 words); SPARSE [2^200, 2^200 + 2^140); DENSE [2^201, 2^201 + Q); CID
[2^202, 2^202 + Q). With 2C < 2^90 and Q < 2^129 the regions are disjoint and every address is below 2^203, a
representable 256-bit word.

## 8. The algorithm CAMP

```
Preprocessing (once, Section 11.2): generate the code, constants w_b and masks; check rank and the
  780 polarizations of Lemma 3; count = 0; F = 0.
For h = 0, 1, ..., G - 1:
  Setup (Section 6): leader step of the 256 cosets j = 256 h + c (two random words each); for every |S| <= 4
    the direct evaluations and the conversion; the transform; the phase conversion; the 175 point-zero loads.
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

Let G = 1,368,445,870,808,731,089,898,285, C = 256 G = 350,322,142,927,035,159,013,960,960 cosets and
Q = 2^48 G = 385,183,269,615,680,952,885,023,214,238,915,624,960 candidates. On the coins of Section 6.1 define

- X: the number of unordered pairs of candidates with equal digests;
- Y: the number of unordered pairs of candidates with equal keys;
- TRIPLE: a bad triple exists: candidates A, B, B' with A not in {B, B'}, digest(B) = digest(B'), key(A) = key(B)
  and digest(A) != digest(B).

**Lemma 9 (detection).** If X >= 1, neither DUP (Lemma 7) nor TRIPLE occurs and the run does not stop at the R140
cap, CAMP outputs a collision.

*Proof.* As X >= 1, two candidates have equal digests. Let B' be the first candidate in probe order that has an
earlier candidate B with the same digest, and k its key. By Lemma 8 the probe of B' hits and returns the first
candidate A0 with key k (A0 precedes or equals B). If digest(A0) = digest(B), the verification of A0 against B' finds
equal digests and CAMP outputs the two messages, which are distinct outside DUP (Lemma 7). Otherwise A0 != B, and A0
has the key of B and B' and a different digest: a bad triple, excluded outside TRIPLE. QED.

**Lemma 10 (second moment).** For candidates i < j let I_ij = 1 if their digests are equal. Let p2 be the mean of
Pr[I_e = 1] over the C(Q, 2) pairs e, p3 the mean of Pr[I_e = I_f = 1] over the 6 C(Q, 3) ordered pairs (e, f) of
distinct pairs sharing one candidate, and p4 the same mean over the 6 C(Q, 4) ordered pairs of disjoint pairs. Then
E[X] = C(Q, 2) p2, E[X^2] = E[X] + 6 C(Q, 3) p3 + 6 C(Q, 4) p4, and Pr[X >= 1] >= E[X]^2/E[X^2] if E[X] > 0.

*Proof.* X^2 is the sum of I_e I_f over ordered pairs (e, f); the terms e = f sum to X. Three candidates carry three
pairs, hence six ordered pairs of distinct pairs, each sharing one candidate; four candidates carry three perfect
matchings, hence six ordered pairs of disjoint pairs; every other ordered pair of distinct pairs spans three or four
candidates. By the Cauchy-Schwarz inequality, E[X] = E[X 1{X >= 1}] <= (E[X^2] Pr[X >= 1])^(1/2) (Paley-Zygmund). QED.

**Theorem.** Under H_coset (Section 12), CAMP outputs a collision with probability greater than 0.39 over its coins.

*Proof.* By Lemma 9 a failure lies in DUP, in {X = 0}, in TRIPLE or in the cap event. (i) Pr[DUP] <= C(C, 2) 2^-280
< 2^-104 (Lemma 7). (ii) By H_coset (a), p2 >= 2^-256, p3 <= 2^-512 and p4 <= 2^-512. Since m^2/(m + c) increases in
m > 0 and decreases in c, Lemma 10 gives Pr[X >= 1] >= mu^2/(mu + a3 + a4) with mu = Q(Q - 1)/2^257 =
0.6406575447816195084436..., a3 = Q(Q - 1)(Q - 2)/2^512 < 10^-38 and a4 = Q(Q - 1)(Q - 2)(Q - 3)/2^514 =
0.4104420896856128058548..., and the exact rational comparison (integer numerators) gives

    mu^2/(mu + a3 + a4) > 19993/51200 = 0.39 + 2/4096        (margin 9.7045901064505... 10^-26).

G is the least number of groups with this property. (iii) Every verification follows a hit, which pairs the probing
candidate with an earlier candidate of equal key, so the number of verifications is at most Y. With
r140 = ceil(Q(Q - 1)/2^141) = 53,223,746,514,659,818,003,504,472,938,913,294 and
R140 = r140 + ceil(sqrt(4096 r140)) = 53,223,746,514,659,832,768,478,760,896,431,256, H_coset (b) (E Y <= r140 and
Var Y <= r140) and Chebyshev's inequality give Pr(Y >= R140) <= Var Y/(R140 - r140)^2 <= 1/4096. (iv) By H_coset (c),
Pr[TRIPLE] <= Q(Q - 1)(Q - 2)/2^397 = 0.0001770491994638444... The failure probability is therefore below
(1 - 19993/51200) + 1/4096 + 2^-104 + 0.00017705 < 0.61, and by the exact comparison the success probability is
greater than 0.39006709. QED.

## 10. Cost ledger and certificate

All charges are word operations of Section 5.1; a permutation call is 1355 of them (it appears only in verification).

| term | value |
|---|---|
| FES, G Fv | 3,305,654,848,510,844,962,172,691,114,776,620,662,375 |
| chi and transpose, G * 4656 * 2^40 | 7,005,520,716,135,197,330,596,359,708,970,277,928,960 |
| setup, S_v (Section 6.5) | 74,052,244,398,980,517,853,008,237,129,483,255 |
| table, 15 Q | 5,777,749,044,235,214,293,275,348,213,583,734,374,400 |
| verification, 3554 R140 | 189,157,195,113,101,045,659,173,516,225,916,683,824 |
| preprocessing, ONCE = 2^70 + 16 | 1,180,591,620,717,411,303,440 |

    N = G Fv + G 4656 2^40 + S_v + 15 Q + 3554 R140 + ONCE
      = 16,278,155,856,238,756,613,402,017,182,511,090,436,254,

about 42.2608 operations per candidate. The time is N/1355 target compressions, and the integer certificate

    1355^10000 * 2^1231759 <= N^10000 < 1355^10000 * 2^1231760

gives log2(N/1355) = 123.1759839..., so time_log2 = 123.1760 (rounded up at the fourth decimal).

## 11. Memory, preprocessing and advice

### 11.1 Memory

SPARSE: 2^140 words (never initialized); DENSE and CID: Q words each; coset records: 2C words; work frames: scalar
frame 512, working frames 512, tile words 144, coefficient and derivative records 2 * 175 * P_D (fewer than 2^36 words
in all); generated code and its constants: fewer than 2^58 words. The regions are disjoint (Section 7), so memory is
below 2^140 + 2^130 + 2^90 + 2^36 + 2^58 < 2^141 words of 32 bytes, below 2^146 bytes.

### 11.2 Preprocessing: ONCE <= 2^70 + 16 operations

(a) **Code generation.** Each of the 2^40 Gray sites is decoded (its set bits and the record addresses of T_1..T_L)
in fewer than 2^14 operations and emits at most 525 * 4 + 97 + 4656 + 15 * 256 = 10,693 < 2^14 instructions; the
setup code (per point, transform pair, phase term and lane) has fewer than 2^46 instructions. At four words per
instruction the code is below 2^58 words and is generated in fewer than 2^60 operations.
(b) **Constants and certificate.** The two-word forms of w_b, the eight butterfly masks, rank 40 and the 780
polarizations of Lemma 3 (821 two-round evaluations): fewer than 2^25 operations.
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

The total is below 2^60 + 2^35 + 16 < 2^70 + 16 = ONCE, which is in N. In target compressions ONCE/1355 < 2^59.60;
the claim declares preprocessing_log2 = 59.6.

### 11.3 Advice

None. Every constant used by CAMP is produced by the procedures of Section 11.2, whose cost is in N.

## 12. Premise H_coset and evidence

**Statement (H_coset).** For the Q = 2^48 G candidates of Section 6.1 (C = 256 G cosets with independent uniform
origins; inside each coset the 2^40 Gray points of span(W40) in the fixed order), with X, Y, TRIPLE, p2, p3 and p4 as
in Section 9 and Lemma 10 and the probabilities over the coins:

- (a) pair and two-pair rates: p2 >= 2^-256, p3 <= 2^-512 and p4 <= 2^-512;
- (b) 140-bit keys: E[Y] <= Q(Q - 1)/2^141 and Var[Y] <= Q(Q - 1)/2^141;
- (c) bad triples: Pr[TRIPLE] <= Q(Q - 1)(Q - 2)/2^397.

Independent uniform 256-bit digests meet every bound. Only first and second moments of pair counts and a first
moment of triples enter: unlike an occupancy (Poisson-tail) premise, nothing about higher-order dependence is
assumed. Splitting the pairs into those inside one coset and those across two cosets, the class rates pW, pX >=
2^-256 and the class two-pair rates at most 2^-512 imply (a); the tests below measure pair rates by class. The premise
is used only in the Theorem of Section 9.

This is assumed, not proved. The concern it answers: on a coset every digest bit is a polynomial of degree at most 8
in the 40 inner variables (Lemma 4 and the last chi), so equal-digest pairs inside a coset could be rarer, or could
cluster, compared with uniform values; pairs from different cosets involve independent uniform origins.

### 12.1 GPU evidence

**Batches (preregistered, our runs; protocols, programs and raw results in Appendix A).** Each batch was fixed in a
protocol file hashed before its runs: sizes, statistics and the pass rule (every count of the tested inputs at least
expected - 4 sigma, sigma = sqrt(expected); no reruns). A GPU program computes real SHA3-256 digests of the messages
M(t) at the round count of the batch and was validated against the organizer reference before the runs. Each run has
2^30 messages in ncos complete cosets of dimension n. Field runs: independent uniform origins, as in CAMP, and n
random independent elements of span(W40); control runs: uniform origins and n random 320-bit directions; sequence
runs: the first n ordered vectors of W40 (the first 2^n Gray points of each coset of CAMP) at the deterministic
origins t_j = XOR(q_b : bit b of g(j)), j = 0..ncos - 1, of the protocols, where q_0, q_1, ... are the coordinate
vectors e_0, e_1, ... appended to the ordered basis of W40 whenever they raise the rank. Counts are exact numbers of
equal-key pairs: within-coset pairs with equal low 32 bits of digest lane L, expected ncos C(2^n, 2) 2^-32; global
pairs among all 2^30 messages with equal low 44 bits of lane L, expected C(2^30, 2) 2^-44 = 32,767.99997;
z = (count - expected)/sqrt(expected).

*Five rounds, the target* (batch R5: PREREG_R5.txt, SHA-256
0a98c8a57288c2403d3082da7484dac332eec8ded347a7666a9b7e30df109876; five-round digests, validated against the organizer
reference sha3_256(rounds=5) on 512 of 512 messages of the sequence):

| run | inputs | lane | within-coset pairs | expected | z | global pairs | z |
|---|---|---|---:|---:|---:|---:|---:|
| P1 | sequence, n = 20, j = 0..1023 | 0 | 130,774 | 131,071.875 | -0.82 | 32,882 | +0.63 |
| P2 | sequence, n = 20, j = 0..1023 | 3 | 130,530 | 131,071.875 | -1.50 | 32,926 | +0.87 |
| P3 | sequence, n = 24, j = 0..63 | 1 | 2,095,898 | 2,097,151.875 | -0.87 | 32,547 | -1.22 |
| P4 | sequence, n = 24, j = 0..63 | 2 | 2,096,787 | 2,097,151.875 | -0.25 | 32,836 | +0.38 |
| P5 | field, n = 20, 1024 cosets | 0 | 130,789 | 131,071.875 | -0.78 | 32,857 | +0.49 |
| P6 | control, n = 20, 1024 cosets | 0 | 130,646 | 131,071.875 | -1.18 | 32,555 | -1.18 |

Verdict under the preregistered rule: pass; every count lies within 1.5 sigma of its expectation (lowest z = -1.50).
P5 is direct evidence for the scope of H_coset (uniform origins, a subspace of span(W40)), with its control P6; P1 to
P4 use deterministic origins and bear only on the fixed order of the first 2^n Gray points.

*Six rounds, supporting context* (the same message construction and statistics on the sibling target sha3-256-r6;
PREREG.txt, SHA-256 67e381a2c0dececee0ce10a8ac4591304076a161259e1cb9045f2c87df54fa58; PREREG2.txt, SHA-256
3b49de9f7c931d51a66ec7f31c2b0c4e3227bc8047cfd25ab5f727207bc01b4c; PREREG3.txt, SHA-256
5f94fcd22a4d94dddeef79ebc91f47b858793804e7d47e6784862e46479efc6a; six-round digests validated against
sha3_256(rounds=6) on 2,048 of 2,048 digests for batches 1-2 and 512 of 512 for batch 3):

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

All three six-round batches pass: every count lies within 2.1 sigma of its expectation and none is below
expected - 1.4 sigma. The field and control runs of batches 1-2 (R, S) use uniform origins; batch 3 (D) uses the
deterministic origins.

### 12.2 Organizer-executed test

The two declared experiments (Section 13) test a reduced-width form of (a) at every organizer run, on the run's own
five-round digests: per experiment 2^17 digests, one group of 256 cosets whose origins come from the organizer's
trial seeds, the first 2^9 Gray points of each coset, projected to 16 and 24 digest bits (bits 0..3, resp. 0..5, of
lanes 0..3). For uniform values every expectation below is exact and the pass intervals are the expectation +- 4
standard deviations.

- Pair rates by class. The program stops (the experiment fails) unless each count lies in its interval: pairs inside
  one coset agreeing on 16 bits (33,488,896 pairs, expectation 511, interval [421, 601]); pairs across two cosets
  agreeing on 16 bits (130,560; [129115, 132005]) and on 24 bits (510; [420, 600]).
- Existence of an agreeing pair, the event that Lemma 10 bounds through the second moment. In hcoset-within16 each
  trial returns two of the 512 points of its own coset that agree on the 16 bits; in hcoset-cross16 a point a < 256 of
  its own coset and a point b >= 256 of the partner coset, whose origin is independent. The organizer recomputes both
  digests of every returned pair; the trials' message sets are disjoint, so for uniform values the successes are
  Binomial(256, P): P = 0.864841510863844 (expectation 221.40, pass interval [200, 243]) and P = 0.632121969489614
  (161.82, [131, 192]). Pair clustering, the dependence that (a) excludes, lowers these counts.

Scope: this is the organizer-executed part of the evidence. It reaches 16 and 24 bits, 2^17 digests per run and
9-dimensional sub-cosets, not 256 bits, complete cosets or Q messages, and it measures neither p3 nor p4 directly.

### 12.3 Sensitivity

If the pair rate falls short, p2 = (1 - eps) 2^-256 with p3 and p4 at their uniform values, the bound of the Theorem
holds with a larger number of groups: the least G for which mu^2/(mu + a3 + a4), with mu multiplied by 1 - eps,
exceeds 19993/51200 (exact integer comparison; G - 1 fails). time_log2 is the ledger of Section 10 at that G,
rounded up at the fourth decimal, each with its integer certificate; extra is its difference to the claim. The
success bound stays above 0.39 in every row; the claim is the row eps = 0.

| eps | least G | time_log2 | extra |
|---:|---:|---:|---:|
| 0 | 1,368,445,870,808,731,089,898,285 | 123.1760 | 0 |
| 0.01 | 1,384,373,245,213,260,043,797,082 | 123.1929 | 0.0169 |
| 0.05 | 1,455,259,709,442,371,143,193,342 | 123.2658 | 0.0898 |
| 0.10 | 1,564,832,508,157,840,178,133,804 | 123.3719 | 0.1959 |
| 0.25 | 2,230,849,474,545,121,805,338,724 | 123.8916 | 0.7156 |
| 1 - (19993/51200)^(1/2) = 0.375109... or more | none: the ratio tends to (1 - eps)^2 <= 19993/51200 | - | - |

**Scope and extrapolation.** The direct five-round evidence for the random-origin scope is the GPU field run P5 with
its control P6 (32-bit within-coset and 44-bit global projections of one digest lane, 2^30 messages, 20-dimensional
subspaces of span(W40)) and the organizer-executed test of Section 12.2; the six-round and deterministic-origin runs
are context. (a) extrapolates these pair-rate and existence measurements to the full 256-bit digest, to complete
40-dimensional cosets in Gray order, to C = 256 G cosets and to Q messages; (b) and (c) extrapolate the same pair-rate
measurements to the 140-bit key and to triples.

**Limits.** No proof is known. Image size and balance do not imply (a): a balanced linear map onto F_2^256 can be
injective on every translate of a campaign space, so its campaigns contain no collision at all. No such structure is
known for the native function and none is excluded by proof. No experiment measures p3, p4 or Var[Y] at 256 or 140
bits.

## 13. Experiments

`experiments/fes_campaign.py` (Python standard library) serves the two declared experiments, hcoset-within16 and
hcoset-cross16, whose checked event is that the two returned digests agree on bits 0..3 of lanes 0..3 (a 16-bit mask
event, not a collision). Each run executes the schedule of Sections 5 to 7 at a reduced size on the organizer's
trials, then the premise test of Section 12.2. The request must name one of the two experiments with its mask event.

- Once per run: the program's five-round SHA3-256 equals the organizer reference on M(0) and M(w_0 XOR w_39)
  (hard-coded known-answer digests), and its 24-round version equals hashlib.sha3_256 on both; rank(W40) = 40; the 780
  polarizations of Lemma 3 vanish. A failed check stops the program.
- Groups: trials 256g .. 256g + 255 form one group; its index is h = int(seed of the group's first trial, 16) mod G,
  and trial k is lane c = k mod 256 of the cosets j = 256 h + c of Section 6.1. The counted leader step draws the
  origin of lane c from two coin words of trial k (SHA-256 of the trial's seed and a counter), a reproducible
  stand-in for fresh coins.
- Reduced size: the first 2^9 Gray points of each coset (directions w_0..w_8), D = 4, all 175 planes, the full
  140-bit key and the sparse-set table of Section 7 with Q' = 2^17 candidates and the verification cap of the same
  formula (65).
- Every operation of the leader step, the setup schedule, the FES steps, chi and transpose, the table and
  verification runs through a counting machine (one call per primitive of Section 5.1, a random word included; a
  permutation call counted apart), and the program stops unless the executed counts equal the formulas above:
  525 L(i) + 97 per Gray step, 175 point-zero loads, 4656 per point, 11 / 15 / 10 table operations per candidate,
  11 per coset leader and 5 per group, 1174 + 2|S| per evaluation, 1282 per plane conversion, 4 * 175 J_D and
  2 * 175 V_D for transform and phase, at most 844 operations and two permutation calls per verification.
- Setup values of lanes 1..255 at points S other than the empty set come from a bit-sliced evaluation (not counted);
  the counted schedule of Section 6.3 runs on lane 0 at every point and, with the conversion of Section 6.4, on all
  lanes at the empty set, and must equal it. Never-written sparse words read as a fixed pseudo-random function of
  their address, half of them below 2 Q', so fresh keys often reach the dense test (an arbitrary initial memory); a
  read of a never-written work, dense, identifier or coset word stops the program.
- Beside the algorithm, not counted: at point i the message of lane i mod 256 is hashed natively and its 140 key bits
  are compared with the emitted key (key_mismatch); after the run the first candidate's key is probed again (a valid
  hit, 10 operations) and verified against the candidate (i, e) = (1, 5), with the reconstructed sources and digests
  compared with the native ones.
- Premise test, not counted. Key bit 4z + x is digest bit z of lane x (iota cancels in an equality), so key bits 0..15
  and 0..23 are the 16- and 24-bit projections of Section 12.2. The program counts pairs16_within, pairs16_cross and
  pairs24_cross over the group's 2^17 keys and stops unless each lies in its pass interval. Trial k (lane c) then
  returns the first repeat of key bits 0..15 among the 512 points of its own coset in Gray order (hcoset-within16), or
  the first point b >= 256 of coset c XOR 1, in Gray order, whose key bits 0..15 equal those of a point a < 256 of
  coset c, with that a (hcoset-cross16). Each returned pair is hashed natively and must agree on the mask; a trial
  without such a pair returns two nulls. (A full collision among 2^17 messages, probability below 2^-222, would be
  returned by trial 0 instead, without the test.)

Per trial the program reports 16 numbers, the same for all trials of a group: fes_ops = 1,026,592
(525 * 1,861 + 97 * 511); chi_transpose_ops = 2,383,872 (4656 * 512); table_ops = 11 (2^17 - m - x) + 15 x + 10 m
with x = in_range_mismatches and m = key_matches; leader_ops = 2,821 (11 * 256 + 5); evaluation_ops = 601,588;
conversion_ops = 224,350; transform_phase_ops = 763,700; verify_check_ops (at most 10 + 844); perm_calls = 2 + 2 m;
native_checks = 512; key_mismatch = 0; pairs16_within, pairs16_cross and pairs24_cross. The 175 point-zero loads and
the dense count 2^17 - m are checked inside the program. Nothing about cost is inferred from the runs.

## 14. Credits

- GPT Sol cloud: the two-round affine field and its certificate.
- GPT Sol local, with GPT Luna: the exact ledger of the route at six rounds (initialization, schedule, setup, table
  and success).
- GPT Luna: the five-round ledger and the random-origin correction (degree 4, the evaluation and verification
  constants, numerator, certificate and duplicate-coset bound); the second-moment premise and its number of groups.
- Grok: transpose and table code and executed operation counts.
- Bouillaguet, Chen, Cheng, Chou, Niederhagen, Shamir and Yang, CHES 2010: fast exhaustive search by Gray-code finite
  differences.
- Prior context on this track: rubenmarcus 91f1424d (degree-4 Gray-order finite differences, used there to solve connector
  equations); winglock ae9a4286 and d841dfb9 (grouped bitsliced birthday search with Gray-order affine updates).
- Jbenisek: the preregistered H_coset runs at five and six rounds, the kernel checks, the package and the experiment
  program with its premise test.

## Appendix A. H_coset evidence: protocols, programs and raw results

Verbatim copies (ASCII) of the files behind Section 12. SHA-256 of each protocol file, hashed before its runs:

| file | batch | SHA-256 |
|---|---|---|
| PREREG.txt | 1 (six rounds) | 67e381a2c0dececee0ce10a8ac4591304076a161259e1cb9045f2c87df54fa58 |
| PREREG2.txt | 2 (six rounds) | 3b49de9f7c931d51a66ec7f31c2b0c4e3227bc8047cfd25ab5f727207bc01b4c |
| PREREG3.txt | 3 (six rounds) | 5f94fcd22a4d94dddeef79ebc91f47b858793804e7d47e6784862e46479efc6a |
| PREREG_R5.txt | R5 (five rounds) | 0a98c8a57288c2403d3082da7484dac332eec8ded347a7666a9b7e30df109876 |

Expected values printed in the protocols are approximations; their stated formulas govern, and Section 12 uses the
exact formula values (for R5-R6, PREREG.txt prints 2147483616.0 where its formula gives 2,097,151.875).

### A.1 PREREG.txt

```text
PREREGISTRATION - H_coset evidence for the SHA3-256 r6 low-degree route (written 2026-10-09 before any main run)

Premise to support (H_coset): a campaign of N messages enumerated as whole cosets of the certified 2-round-affine field
W40 (research/sha3r6/lowdegree/RESULT.md) contains an equal-digest pair with probability at least the value for N
independent uniform 256-bit digests. Concern: the digest on a coset is a degree-16 function of the coset variables,
so pairs inside a coset or across cosets of one field could be rarer than uniform.

Program: hcoset.cu (real 6-round SHA3-256, organizer round function, 135-byte single block; GPU digests validated
2048/2048 against SOLCLOUD_12_INPUT_keccak.py sha3_256(rounds=6) before this file). Exact pair counts
(sum over equal-key runs of C(len,2)) on a projection of the digest: within-coset (low 32 bits of a digest lane,
pairs only inside one coset) and global (low KG bits of the lane, all messages).

Main runs (seeds fixed here; inputs from hc.py gen MODE SEED N NCOS):
  R1 field seed 1001, n=20, 1024 cosets, KG=44, lane 0     R2 same inputs, lane 3
  R3 ctrl  seed 1001, n=20, 1024 cosets, KG=44, lane 0     R4 same inputs, lane 3
  R5 field seed 1002, n=24, 64 cosets,  KG=44, lane 0      R6 ctrl seed 1002, n=24, 64 cosets, KG=44, lane 0
Expected under the uniform model: within32 = ncos * C(2^n,2) / 2^32 (R1-R4: 131071.97; R5-R6: 2147483616.0... per
formula), global = C(2^30,2) / 2^44 (32767.97). Sigma = sqrt(expected) (Poisson).

Pass criterion (one-sided, the premise only needs no deficit): for every field run R1, R2, R5 and both counts,
observed >= expected - 4 sigma. Report two-sided z for all runs, field and control. A field deficit beyond 4 sigma
on any count = H_coset NOT supported; reported as such, no reruns with other seeds.
Scope: this is evidence at 32- and 44-bit projections, not a proof for 256 bits; stated as such in any filing.
```

### A.2 PREREG2.txt

```text
PREREGISTRATION 2 - H_coset, second batch (written 2026-10-09 23:55, after batch 1 PASSED; same program hcoset.cu,
same pass rule). Purpose: cover the two digest lanes batch 1 did not test (1 and 2) and much larger cosets.

Runs (inputs from hc.py gen MODE SEED N NCOS; seeds fixed here):
  S1 field seed 2001, n=20, 1024 cosets, KG=44, lane 1     S2 same inputs, lane 2
  S3 ctrl  seed 2001, n=20, 1024 cosets, KG=44, lane 1     S4 same inputs, lane 2
  S5 field seed 2002, n=28, 4 cosets,    KG=44, lane 0     S6 same inputs, lane 2
  S7 ctrl  seed 2002, n=28, 4 cosets,    KG=44, lane 0
Expected (uniform digests): within32 = ncos * C(2^n,2) / 2^32  (S1-S4: 131071.97; S5-S7: 4 * C(2^28,2)/2^32 =
33554431.5); global = C(2^30,2)/2^44 = 32767.97. Sigma = sqrt(expected).
Pass (one-sided): every field count (S1, S2, S5, S6; both counts) >= expected - 4 sigma. Two-sided z reported for all.
A field deficit beyond 4 sigma on any count = H_coset NOT supported; reported as such; no reruns with other seeds.
```

### A.3 PREREG3.txt

```text
PREREGISTRATION 3 - H_coset on the DETERMINISTIC input sequence of D19 Section 6 (written 2026-10-10 00:36, before
any run of this mode; same program hcoset.cu, same pass rule as batches 1 and 2).

Sequence: ordered W40 basis (SOLCLOUD_16 Appendix B order, then c0..c4 of D17 section 9) extended by standard
coordinate vectors e_i = 1 << i (i increasing; bit 64k+b = bit b of source lane k) whenever they raise the rank;
q_0, q_1, ... the appended vectors; coset j has representative t_j = XOR(q_b : bit b of g(j) set), g(j) = j ^ (j>>1).
Inside a coset the points are t_j + span of the FIRST n ordered W40 vectors (the first 2^n Gray points of the route's
enumeration of that coset). Inputs: hc.py gen det SEED N NCOS (SEED only names the file; nothing is random).

Runs:
  D1 det 3001, n=20, cosets j = 0..1023, KG=44, lane 0      D2 same inputs, lane 3
  D3 det 3002, n=24, cosets j = 0..63,   KG=44, lane 1      D4 same inputs, lane 2
Expected (uniform digests): within32 = ncos * C(2^n,2) / 2^32 (D1-D2: 131071.875; D3-D4: 2097151.875 approx. by the
formula); global = C(2^30,2)/2^44 = 32767.97. Sigma = sqrt(expected).
Pass (one-sided): every count >= expected - 4 sigma. Two-sided z reported. A deficit beyond 4 sigma on any count =
H_coset NOT supported for the deterministic sequence; then the package uses random coset origins (batches 1-2) instead.
No reruns with other parameters.
```

### A.4 PREREG_R5.txt

```text
PREREGISTRATION R5 - H_coset at FIVE rounds (sha3-256-r5: prefix rounds 0-4), for the r5 low-degree line (D23).
Written 2026-10-10 01:55, before any 5-round count run. Same program hcoset.cu (rounds from HC_ROUNDS=5; GPU digests
validated 512/512 against the organizer sha3_256(rounds=5) on the deterministic sequence before this file), same
deterministic input sequence as PREREG3 (D19 Section 6 representatives; points t_j + span of the first n ordered W40
vectors), same pass rule.

Runs (HC_ROUNDS=5; inputs from hc.py gen det SEED N NCOS and hc.py gen field/ctrl SEED N NCOS):
  P1 det 4001, n=20, cosets j = 0..1023, KG=44, lane 0      P2 same inputs, lane 3
  P3 det 4002, n=24, cosets j = 0..63,   KG=44, lane 1      P4 same inputs, lane 2
  P5 field 4003 (random origins), n=20, 1024 cosets, lane 0  P6 ctrl 4003, n=20, 1024 cosets, lane 0
Expected (uniform digests): within32 = ncos * C(2^n,2) / 2^32 (n=20, 1024 cosets: 131071.875; n=24, 64 cosets:
2097151.875); global = C(2^30,2)/2^44 = 32767.97. Sigma = sqrt(expected).
Pass (one-sided): every field/det count >= expected - 4 sigma. Two-sided z reported. A deficit beyond 4 sigma on any
count = H_coset NOT supported at r5; reported as such; no reruns with other parameters.
```

### A.5 hcoset.cu

The GPU program: real SHA3-256 digests with the organizer round function (round count from HC_ROUNDS) and exact
pair counts (sorted keys, sum over runs of C(len, 2)). It enumerates the points of a coset in binary rather than
Gray order; the counts do not depend on the order.

```cpp
// H_coset test: real 6-round SHA3-256 (organizer round function, single 135-byte block, zero capacity) on messages
// enumerated as whole cosets: message lanes u = start_c ^ XOR_{j: bit j of p} dir_j, embedded as in cube_degree.py
// (u0..u4 in lanes 0-4 and 10-14, lane 16 = 0x86<<56). Counts exact equal-key pairs (sum over runs of C(len,2)):
//   within-coset at 32 bits (key = coset id << 32 | low 32 bits of digest lane L) and global at KG bits.
// usage: hcoset count <infile> <n> <ncos> <KG> <lane>     -> one JSON line
//        hcoset dump  <infile> <n> <ncos> <M> <outfile>    -> first M digests (4 lanes each), for validation
// infile: ncos*5 u64 starts then n*5 u64 directions (little endian).
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <vector>
#include <thrust/device_vector.h>
#include <thrust/sort.h>
#include <thrust/transform_reduce.h>
#include <thrust/iterator/counting_iterator.h>
typedef unsigned long long u64;

__constant__ u64 RC[6] = {0x0000000000000001ull, 0x0000000000008082ull, 0x800000000000808Aull,
                          0x8000000080008000ull, 0x000000000000808Bull, 0x0000000080000001ull};
__constant__ int NROUNDS = 6;   // set from the HC_ROUNDS environment variable (5 or 6)
__constant__ int RHO[25] = {0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39, 41, 45, 15, 21, 8, 18, 2, 61, 56, 14};
__constant__ u64 DIRS[64 * 5];

__device__ __forceinline__ u64 rotl(u64 x, int r) { return r == 0 ? x : (x << r) | (x >> (64 - r)); }

__device__ void digest(const u64 *starts, int n, u64 idx, u64 out[4]) {
    u64 c = idx >> n, p = idx & ((1ull << n) - 1), u[5];
    for (int k = 0; k < 5; k++) u[k] = starts[c * 5 + k];
    for (int j = 0; j < n; j++)
        if (p >> j & 1)
            for (int k = 0; k < 5; k++) u[k] ^= DIRS[j * 5 + k];
    u64 A[25], B[25], C[5], D[5];
    for (int k = 0; k < 25; k++) A[k] = 0;
    for (int k = 0; k < 5; k++) { A[k] = u[k]; A[10 + k] = u[k]; }
    A[16] = 0x86ull << 56;
    for (int r = 0; r < NROUNDS; r++) {
        for (int x = 0; x < 5; x++) C[x] = A[x] ^ A[x + 5] ^ A[x + 10] ^ A[x + 15] ^ A[x + 20];
        for (int x = 0; x < 5; x++) D[x] = C[(x + 4) % 5] ^ rotl(C[(x + 1) % 5], 1);
        for (int y = 0; y < 5; y++)
            for (int x = 0; x < 5; x++) B[y + 5 * ((2 * x + 3 * y) % 5)] = rotl(A[x + 5 * y] ^ D[x], RHO[x + 5 * y]);
        for (int y = 0; y < 5; y++)
            for (int x = 0; x < 5; x++)
                A[x + 5 * y] = B[x + 5 * y] ^ (~B[(x + 1) % 5 + 5 * y] & B[(x + 2) % 5 + 5 * y]);
        A[0] ^= RC[r];
    }
    for (int k = 0; k < 4; k++) out[k] = A[k];
}

__global__ void kkeys(const u64 *starts, int n, u64 base, u64 cnt, int lane, int mode, int KG, u64 *keys) {
    u64 g = blockIdx.x * (u64)blockDim.x + threadIdx.x;
    if (g >= cnt) return;
    u64 idx = base + g, d[4];
    digest(starts, n, idx, d);
    u64 v = d[lane];
    keys[g] = mode == 0 ? (((idx >> n) << 32) | (v & 0xffffffffull)) : (v & ((1ull << KG) - 1));
}

__global__ void kdump(const u64 *starts, int n, u64 cnt, u64 *out) {
    u64 g = blockIdx.x * (u64)blockDim.x + threadIdx.x;
    if (g >= cnt) return;
    digest(starts, n, g, out + 4 * g);
}

struct EqAt {
    const u64 *k; u64 d;
    __device__ u64 operator()(u64 i) const { return k[i] == k[i + d]; }
};

static u64 pairs(thrust::device_vector<u64> &v) {   // sum over runs of C(len,2), exact
    thrust::sort(v.begin(), v.end());
    u64 tot = 0, N = v.size();
    for (u64 d = 1; d < N; d++) {
        u64 c = thrust::transform_reduce(thrust::counting_iterator<u64>(0), thrust::counting_iterator<u64>(N - d),
                                         EqAt{thrust::raw_pointer_cast(v.data()), d}, 0ull, thrust::plus<u64>());
        if (!c) break;
        tot += c;
    }
    return tot;
}

int main(int argc, char **argv) {
    if (argc < 7) { fprintf(stderr, "usage: see header\n"); return 1; }
    const char *mode = argv[1];
    int n = atoi(argv[3]); u64 ncos = strtoull(argv[4], 0, 10);
    std::vector<u64> buf(ncos * 5 + n * 5);
    FILE *f = fopen(argv[2], "rb");
    if (!f || fread(buf.data(), 8, buf.size(), f) != buf.size()) { fprintf(stderr, "bad infile\n"); return 1; }
    fclose(f);
    cudaMemcpyToSymbol(DIRS, buf.data() + ncos * 5, n * 5 * 8);
    { const char *e = getenv("HC_ROUNDS"); int nr = e ? atoi(e) : 6; if (nr < 1 || nr > 6) nr = 6; cudaMemcpyToSymbol(NROUNDS, &nr, sizeof(int)); }
    thrust::device_vector<u64> starts(buf.begin(), buf.begin() + ncos * 5);
    const u64 *sp = thrust::raw_pointer_cast(starts.data());
    u64 total = ncos << n;
    if (mode[0] == 'd') {
        u64 M = strtoull(argv[5], 0, 10);
        thrust::device_vector<u64> out(4 * M);
        kdump<<<(M + 255) / 256, 256>>>(sp, n, M, thrust::raw_pointer_cast(out.data()));
        std::vector<u64> h(4 * M);
        thrust::copy(out.begin(), out.end(), h.begin());
        FILE *g = fopen(argv[6], "wb"); fwrite(h.data(), 8, h.size(), g); fclose(g);
        printf("{\"dumped\": %llu}\n", M);
        return 0;
    }
    int KG = atoi(argv[5]), lane = atoi(argv[6]);
    // within-coset, 32 bits, in batches of whole cosets (2^28 keys per batch)
    u64 per = 1ull << n, bc = (1ull << 28) / per; if (!bc) bc = 1;
    u64 within = 0;
    for (u64 c0 = 0; c0 < ncos; c0 += bc) {
        u64 nc = (c0 + bc <= ncos ? bc : ncos - c0), cnt = nc << n;
        thrust::device_vector<u64> v(cnt);
        kkeys<<<(cnt + 255) / 256, 256>>>(sp, n, c0 << n, cnt, lane, 0, KG, thrust::raw_pointer_cast(v.data()));
        within += pairs(v);
    }
    thrust::device_vector<u64> v(total);
    kkeys<<<(total + 255) / 256, 256>>>(sp, n, 0, total, lane, 1, KG, thrust::raw_pointer_cast(v.data()));
    u64 glob = pairs(v);
    cudaError_t e = cudaGetLastError();
    printf("{\"n\": %d, \"ncos\": %llu, \"lane\": %d, \"messages\": %llu, \"within32_pairs\": %llu, \"global_bits\": %d, "
           "\"global_pairs\": %llu, \"cuda\": \"%s\"}\n", n, ncos, lane, total, within, KG, glob, cudaGetErrorString(e));
    return 0;
}
```

### A.6 hc.py

Input generation (field, ctrl and det modes) and validation of the GPU digests against the organizer reference. It
imports W40 (the vectors of Section 3), rank and the organizer reference verifier/keccak.py (an identical copy,
SHA-256 95ce77dff0476301c05057e01296f3e3507c4926423257540cfc3e5fd36ee0ae) from a helper module.

```python
"""Driver for hcoset.cu (see PREREG.txt). usage: python hc.py gen MODE SEED N NCOS   -> in_<MODE>_<SEED>.bin
                                                 python hc.py validate MODE SEED N NCOS M (GPU dump vs organizer sha3_256)
MODE field: N random independent elements of span(W40) (cube_degree.W); MODE ctrl: N random 320-bit directions."""
import os, sys, random, struct, subprocess, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / 'lowdegree'))
import cube_degree as cd

HERE = pathlib.Path(__file__).resolve().parent
WSL_HERE = '/mnt/d/~~Projects/~HashSmash/workspace/research/sha3r6/hcoset'
BIN = '/root/hcoset_bin/hcoset'
MASK = (1 << 64) - 1

def det_reps(ncos):
    """D19 Section 6 sequence: extend the ordered W40 basis by standard coordinate vectors e_i = 1 << i (i increasing,
    bit 64k+b = bit b of source lane k) whenever they raise the rank; q_0, q_1, ... are the appended vectors;
    coset j has representative t_j = XOR(q_b : bit b of g(j) set), g(j) = j ^ (j >> 1)."""
    piv = {}
    def add(v):
        while v:
            b = v.bit_length() - 1
            if b in piv: v ^= piv[b]
            else: piv[b] = v; return True
        return False
    for w in cd.W: assert add(w)
    q, need = [], max(1, ncos.bit_length())
    for i in range(320):
        if add(1 << i): q.append(1 << i)
        if len(q) >= need: break
    reps = []
    for j in range(ncos):
        gj, t = j ^ (j >> 1), 0
        for b in range(need):
            if gj >> b & 1: t ^= q[b]
        reps.append(t)
    return reps

def gen(mode, seed, n, ncos):
    if mode == 'det':      # the deterministic D19 input sequence: first n ordered W40 directions, cosets j = 0..ncos-1
        d, starts = cd.W[:n], det_reps(ncos)
        words = [(s >> (64 * k)) & MASK for s in starts for k in range(5)] + [(v >> (64 * k)) & MASK for v in d for k in range(5)]
        p = HERE / f'in_{mode}_{seed}.bin'
        p.write_bytes(struct.pack(f'<{len(words)}Q', *words))
        return p, starts, d
    rng = random.Random(f'{mode}-{seed}')
    while True:
        if mode == 'field':
            d = []
            for _ in range(n):
                c = rng.getrandbits(40) or 1; v = 0
                for j in range(40):
                    if c >> j & 1: v ^= cd.W[j]
                d.append(v)
        else:
            d = [rng.getrandbits(320) for _ in range(n)]
        if cd.rank(d) == n: break
    starts = [rng.getrandbits(320) for _ in range(ncos)]
    words = [(s >> (64 * k)) & MASK for s in starts for k in range(5)] + [(v >> (64 * k)) & MASK for v in d for k in range(5)]
    p = HERE / f'in_{mode}_{seed}.bin'
    p.write_bytes(struct.pack(f'<{len(words)}Q', *words))
    return p, starts, d

def msg(starts, d, n, idx):
    c, p = idx >> n, idx & ((1 << n) - 1); m = starts[c]
    for j in range(n):
        if p >> j & 1: m ^= d[j]
    L = [0] * 25
    for k in range(5): L[k] = (m >> (64 * k)) & MASK; L[10 + k] = L[k]
    L[16] = 0x86 << 56
    return b''.join(l.to_bytes(8, 'little') for l in L[:17])[:135]

if __name__ == '__main__':
    cmd, mode, seed, n, ncos = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    p, starts, d = gen(mode, seed, n, ncos)
    if cmd == 'validate':
        M = int(sys.argv[6]); out = HERE / f'dump_{mode}_{seed}.bin'
        R = int(os.environ.get('HC_ROUNDS', '6'))
        subprocess.run(['wsl', '-d', 'Ubuntu', '--', 'env', f'HC_ROUNDS={R}', BIN, 'dump', f'{WSL_HERE}/{p.name}', str(n), str(ncos), str(M), f'{WSL_HERE}/{out.name}'], check=True)
        raw = out.read_bytes(); ok = 0
        for i in range(M):
            ok += raw[32 * i:32 * i + 32] == cd.kec.sha3_256(msg(starts, d, n, i), rounds=R)
        print(f'validate {mode} seed {seed}: {ok}/{M} GPU digests equal organizer sha3_256(rounds={R})')
        out.unlink()
    else:
        print(p)
```

### A.7 Raw results

One JSON line per run, as written by hcoset.cu.

#### main_results.jsonl (R1 to R6, in run order)

```text
{"n": 20, "ncos": 1024, "lane": 0, "messages": 1073741824, "within32_pairs": 131380, "global_bits": 44, "global_pairs": 33033, "cuda": "no error"}
{"n": 20, "ncos": 1024, "lane": 3, "messages": 1073741824, "within32_pairs": 130720, "global_bits": 44, "global_pairs": 32964, "cuda": "no error"}
{"n": 20, "ncos": 1024, "lane": 0, "messages": 1073741824, "within32_pairs": 131300, "global_bits": 44, "global_pairs": 32762, "cuda": "no error"}
{"n": 20, "ncos": 1024, "lane": 3, "messages": 1073741824, "within32_pairs": 130930, "global_bits": 44, "global_pairs": 32709, "cuda": "no error"}
{"n": 24, "ncos": 64, "lane": 0, "messages": 1073741824, "within32_pairs": 2097299, "global_bits": 44, "global_pairs": 32651, "cuda": "no error"}
{"n": 24, "ncos": 64, "lane": 0, "messages": 1073741824, "within32_pairs": 2098309, "global_bits": 44, "global_pairs": 32777, "cuda": "no error"}
```

#### main2_results.jsonl (S1 to S7, in run order)

```text
{"n": 20, "ncos": 1024, "lane": 1, "messages": 1073741824, "within32_pairs": 130589, "global_bits": 44, "global_pairs": 32932, "cuda": "no error"}
{"n": 20, "ncos": 1024, "lane": 2, "messages": 1073741824, "within32_pairs": 130672, "global_bits": 44, "global_pairs": 32606, "cuda": "no error"}
{"n": 20, "ncos": 1024, "lane": 1, "messages": 1073741824, "within32_pairs": 130638, "global_bits": 44, "global_pairs": 32925, "cuda": "no error"}
{"n": 20, "ncos": 1024, "lane": 2, "messages": 1073741824, "within32_pairs": 131237, "global_bits": 44, "global_pairs": 32715, "cuda": "no error"}
{"n": 28, "ncos": 4, "lane": 0, "messages": 1073741824, "within32_pairs": 33555785, "global_bits": 44, "global_pairs": 32648, "cuda": "no error"}
{"n": 28, "ncos": 4, "lane": 2, "messages": 1073741824, "within32_pairs": 33557768, "global_bits": 44, "global_pairs": 32736, "cuda": "no error"}
{"n": 28, "ncos": 4, "lane": 0, "messages": 1073741824, "within32_pairs": 33566477, "global_bits": 44, "global_pairs": 32926, "cuda": "no error"}
```

#### main3_results.jsonl (D1 to D4, in run order)

```text
{"n": 20, "ncos": 1024, "lane": 0, "messages": 1073741824, "within32_pairs": 131053, "global_bits": 44, "global_pairs": 32666, "cuda": "no error"}
{"n": 20, "ncos": 1024, "lane": 3, "messages": 1073741824, "within32_pairs": 131447, "global_bits": 44, "global_pairs": 32846, "cuda": "no error"}
{"n": 24, "ncos": 64, "lane": 1, "messages": 1073741824, "within32_pairs": 2095169, "global_bits": 44, "global_pairs": 32689, "cuda": "no error"}
{"n": 24, "ncos": 64, "lane": 2, "messages": 1073741824, "within32_pairs": 2095504, "global_bits": 44, "global_pairs": 32710, "cuda": "no error"}
```

#### r5_results.jsonl (P1 to P6, in run order)

```text
{"n": 20, "ncos": 1024, "lane": 0, "messages": 1073741824, "within32_pairs": 130774, "global_bits": 44, "global_pairs": 32882, "cuda": "no error"}
{"n": 20, "ncos": 1024, "lane": 3, "messages": 1073741824, "within32_pairs": 130530, "global_bits": 44, "global_pairs": 32926, "cuda": "no error"}
{"n": 24, "ncos": 64, "lane": 1, "messages": 1073741824, "within32_pairs": 2095898, "global_bits": 44, "global_pairs": 32547, "cuda": "no error"}
{"n": 24, "ncos": 64, "lane": 2, "messages": 1073741824, "within32_pairs": 2096787, "global_bits": 44, "global_pairs": 32836, "cuda": "no error"}
{"n": 20, "ncos": 1024, "lane": 0, "messages": 1073741824, "within32_pairs": 130789, "global_bits": 44, "global_pairs": 32857, "cuda": "no error"}
{"n": 20, "ncos": 1024, "lane": 0, "messages": 1073741824, "within32_pairs": 130646, "global_bits": 44, "global_pairs": 32555, "cuda": "no error"}
```

### A.8 z computation

Applied to each line of A.7, this gives the z columns of Section 12 (rounded to two decimals).

```python
from fractions import Fraction
from math import comb, sqrt


def z(r):    # r: one result line; expectations for uniform digests
    ew = Fraction(r['ncos'] * comb(1 << r['n'], 2), 1 << 32)
    eg = Fraction(comb(r['messages'], 2), 1 << r['global_bits'])
    return float(r['within32_pairs'] - ew) / sqrt(ew), float(r['global_pairs'] - eg) / sqrt(eg)
```
