# SHA3-256 with 6 prefix rounds: Gray-order enumeration of two-round-affine cosets, time_log2 122.20540

## 1. Claim

Target `sha3-256-r6-prefix-v1` (organizer profile): SHA3-256 of FIPS 202 with "prefix rounds 0 through 5, inclusive,
in every sponge permutation" (not the last-round convention of Keccak-p); all-zero 1600-bit initial state; rate 1088
bits, capacity 512; "SHA3 domain suffix 01 followed by pad10*1; delimited suffix byte 0x06", standard little-endian
lane and bit encoding; the digest is the first 32 squeeze bytes; messages are distinct byte strings of bit length
below 2^64; reference `verifier/keccak.py:sha3_256`. Postcondition: "The two complete sha3-256-r6 sponge hashes agree
on all 256 output bits." The algorithm CAMP of Section 8 outputs two distinct 135-byte messages with equal digests.

| Quantity | Value |
|---|---|
| time_log2 (collision-frontier-v5, reference operation cost 1626, rounded up) | 122.20540 (Section 10) |
| success probability | at least 0.39 over CAMP's fresh coins (random coset origins and a 128-bit table tag), under premise H_coset (Section 9) |
| memory | below 2^144 words of 256 bits, below 2^149 bytes (Section 11.1) |
| preprocessing (included in time) | at most 2^70 + 16 word operations, below 2^59.34 target compressions (Section 11.2) |
| nonuniform advice | none |

CAMP is randomized: every coset origin is fresh randomness, drawn with the cost model's primitive "independent uniform
random 256-bit word" (Section 6.1), as is the 128-bit table tag (Section 7); every probability in this document is
over these coins for the fixed target.
One premise is declared (Section 12): **H_coset**, that over these coins the occupancy, key-match and triple bounds of
Section 9 hold for the messages CAMP enumerates (the bounds that independent uniform digests would give). Everything
else is proved here: two-round affinity on every coset of W40, degree at most 8 before the last chi, exactness of the
Gray-order finite differences and of their initialization, correctness of the value-masked table for any initial
memory (up to tag events of probability 2^-128, in the failure budget), the duplicate-coset bound, and every
operation count. Section 12 gives the premise's evidence: reduced-width tests that the organizer executes (the declared experiments), preregistered GPU counts of 32- to 64-bit digest
projections of up to 2^34 messages (Appendix A: protocols with their hashes, programs, raw counts and validation
printouts), and the effect of a pair-rate shortfall on the claim.

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
operation: load, store, AND, OR, XOR, NOT, add, subtract, shift, comparison, conditional branch (on a nonzero register),
register move and the independent uniform random 256-bit word. The machine has 64 registers; reading a register
costs nothing. The program of one group is generated straight-line code: the setup, the record transposes, and for
every coset lane c = 0..255 the copy of its records into the frame followed by one site per Gray step i (the FES
step, chi, the probe and, on the hit path, the verification inline) are unrolled, so an address or constant fixed at
generation time is an immediate operand of its instruction and costs no operation. Every group runs the same code.
Generating and storing this code is charged in ONCE (Section 11.2).

- **Immediate:** the frame addresses of the records at every Gray step, the candidate-major record words of each
  frame copy, the spill words, every setup operand (working frames, bitplanes, transpose words, input words, round
  buffers, D words, coefficient and derivative records), the NOT pattern of w(S) at every setup point and the
  constant words of the folded setup rounds (Section 6.3), the basis constants w_b in two-word form, the butterfly
  masks, the constant rows of the record transposes, the key mask (Section 5.4), at each site the two words of
  sum_b g(i)_b w_b of its Gray step, the constant lanes of the folded verification rounds (Section 7), the byte-table
  bases, the words that hold F and h, the tag word and the region bases.
- **Computed at run time and charged:** the two random words of each coset origin (Section 6.2), the coset-record
  address in the leader step and, for both candidates, in verification (shifts, AND, OR, add, second-word add), the
  decoding of the earlier candidate and its byte-table addresses in verification. The table address costs nothing:
  the key word is its own address (Section 7).

### 5.2 Key and cone

For a message with pre-chi6 bits b, key is the word whose bit 36x + z (x = 0..3, z = 0..34; 140 bits, the highest
bit 142) is b_{x,z} XOR (NOT b_{x+1,z} AND b_{x+2,z}), all other bits zero. By Section 2 it equals digest bit z of
lane x XOR RC[5]_z [x = 0], so messages with equal digests have equal keys. Its inputs are exactly the 175 cone bits
B[x, z] = b_{x,z}, x = 0..4, z = 0..34. Verification always uses the native 256-bit digest, iota included.

### 5.3 Candidate-major FES

A group processes 256 cosets (lanes c = 0..255), one after the other. For y in F_2^175 (bits y_{x,z}, x = 0..4,
z = 0..34) let W(y) be the 256-bit word with bit 36x + z equal to y_{x,z} and bit 180 + z equal to y_{0,z} (a copy of
lane 0 in the block x = 5); its other 46 bits are zero. W is linear over F_2. For lane c of group h (coset
j = 256 h + c, origin t = t_j) let F_c(u) = W(f_t(u)) XOR 2^143, u in F_2^40.

**Lemma 5c (candidate-major FES).** F_c has degree at most 8, and the records of Lemma 6 for F_c are
tab_c[T] = W(tab[T] of f_t) for 1 <= |T| <= 8 and x = W(f_t(0)) XOR 2^143. FES on these words gives
x = F_c(g(i)) after step i.

*Proof.* Every bit of F_c is a bit of f_t or a constant, of degree at most 8 by Lemma 4. Lemmas 5 and 6 hold for
any F_2-vector space V (Section 4.1), here V = F_2^256. The normal form of F_c is W applied to that of f_t plus the
constant 2^143 in a_{}; tab[T] with |T| >= 1 is an XOR of coefficients a_S with |S| >= 1, so it is W(tab[T] of f_t),
and x = a_{} = W(f_t(0)) XOR 2^143. Lemma 5 gives the last claim. QED.

**Registers.** The 60 records of the cached set CR, the 31 nonempty subsets of {0..4} and the 29 subsets of {0..5}
that contain 5 other than {5}, {0, 5} and {1, 5}, are held in registers for a whole lane, with x, the table register
v (Section 7) and two temporaries: 64 registers. The group index h and the verification count F are stored to fixed
words right after the leader step (2), and h is loaded back once after the record transposes for the group control
(1): 3 operations per group. F stays in its word (Section 7). The setup (Section 6.3) has all 64 registers.

**Lemma 5b (last change).** Let 1 <= |T| <= 7 and m = max T. (a) tab[T] is changed exactly at the steps
i = s_T + k 2^(m+1) with 1 <= k < 2^(39 - m), so at least once iff m <= 38. (b) It is read only at those steps and,
as the top, at i = s_T, which precedes them. Hence after its last change in a lane it is never read again, and
omitting the STORE of that change alters no value that is used. A record with |T| = 8 is never changed.

*Proof.* (a) is (B) of Lemma 5 with j = |T| < 8, restricted to i < 2^40; as 2^m <= s_T < 2^(m+1), s_T + k 2^(m+1) <
2^40 iff k < 2^(39 - m). (b) Step i reads tab[T] only as T_{L(i)}(i) or as a link T_j(i) with j < L(i), and a link
use is a change by (B). If T = T_{L(i)}(i) with |T| < 8, then L(i) = popcount(i) = |T| and the set bits of i are T,
so i = s_T. QED.

**Per lane:** the P_D candidate-major words of lane c (Section 5.4) are copied into a fixed frame, LOAD and STORE
each (2 P_D = 200,293,448), so the FES code addresses the frame by immediates; then 60 LOADs of the cached records
and one LOAD of x (61). **Per step i**, with L = L(i) and shapes T_1 .. T_L: the top tab[T_L] costs one LOAD unless
T_L is in CR (a register); each link T_j, j = L - 1 down to 1, costs one XOR into its register if T_j is in CR and
otherwise LOAD, XOR and STORE, with the STORE omitted at the last change of tab[T_j] (i + 2^(max T_j + 1) >= 2^40,
Lemma 5b); then x = x XOR v (1). So step i costs 1 + [T_L not in CR] + the sum over its links of 1 (in CR), 2 (not
in CR, last change) or 3 (not in CR, otherwise).

**Count.** Over the 2^40 - 1 steps of a lane, every T in CR (|T| <= 6) is the top exactly once, at i = s_T, so
2^40 - 1 - 60 tops are LOADed, and a link 2^(39 - max T) - 1 times (Lemma 5b); the links number
sum L - (2^40 - 1) = 7,696,552,680,161 in all, those of CR number sum over CR of (2^(39 - max T) - 1) =
5 * 2^39 + 29 * 2^34 - 60 = 3,246,995,275,716. Every record of CR is changed, and
U = sum_{k=1..7} C(39, k) - 60 = 19,311,427 records outside CR are changed at least once (Lemma 5b (a)), each losing
one STORE. Per lane

    Fc = 61 + (2^40 - 1 - 60) + (2^40 - 1) + 3 (sum L - (2^40 - 1)) - 2 * 3,246,995,275,716 - U
       = 18,794,671,433,175,

17.0937 per candidate, and per group F_g = 256 Fc + 3 = 4,811,435,886,892,803.

### 5.4 Record transposes and the key in the word

A butterfly on rows k and k + d of a bit matrix (row k a 256-bit word) with column shift s is

    t = ((A_k >> s) XOR A_{k+d}) AND mask_s;  A_k = A_k XOR (t << s);  A_{k+d} = A_{k+d} XOR t     [6 ALU]

with mask_s the ones in the low half of every 2s-bit block. For k with bit b clear (d = 2^b in the row index of the
stage) and s = 2^b it exchanges row-index bit b with column-index bit b: for every column c with bit b clear, the bits
(k, c + s) and (k + d, c) are swapped and all others kept. After the stages b = 0..7 on a 256 x 256 matrix the bit
(r, c) has moved to (c, r).

**Record transposes (7,800 per record).** After the phase conversion (Section 6.4) every record (A[{}] and each
tab[T]) is 175 plane words, bit c for lane c. Its transpose is a 256 x 256 matrix whose row 36x + z is plane (x, z)
(x <= 4, z <= 34), row 180 + z plane (0, z) again (210 rows LOADed), and whose other 46 rows are constants set by one
MOV each: zero, except row 143 of A[{}], the all-ones word. Four 64 x 64 blocks, rows 64g .. 64g + 63, run the six
stages s = 1..32 exactly as the blocks of the transpose of Section 6.3 (rows 0 and 1 in two fixed words): 66 to
load (a LOAD or a MOV per row), 198 + 5 * 196 = 1,178 for the stages, 66 to store, 1,310 per block. Then stages s = 64 and 128 on the 256 words
as memory pairs, 10 each (2,560). In all 4 * 1,310 + 2,560 = 7,800 per record, 7,800 P_D = 781,144,447,200 per
group. Word c of the result is W(record of lane c), and XOR 2^143 for A[{}]: by Lemma 5c these are the records of
F_c, which the frame copy of lane c reads.

**Lemma 5d (the key in 6 operations).** For the word w = F_c(u) let
y = w XOR (w >> 72) XOR ((w >> 36) AND (w >> 72)) and k = y AND KEYMASK, KEYMASK = sum_{x<4} (2^35 - 1) 2^(36x)
XOR 2^143. Then k = key + 2^143 for the message M(phi_t(u)), with key as in Section 5.2.

*Proof.* Bit 36x + z of w >> 36 is bit 36(x + 1) + z of w, and of w >> 72 bit 36(x + 2) + z. For x = 0..3 and
z <= 34 these are b_{x+1,z} and b_{x+2,z} (for x = 3, bit 180 + z = b_{0,z} = b_{5 mod 5,z}), so bit 36x + z of y is
b_{x,z} XOR b_{x+2,z} XOR (b_{x+1,z} AND b_{x+2,z}) = b_{x,z} XOR (NOT b_{x+1,z} AND b_{x+2,z}). Bit 143 of w is 1
(the constant of F_c) and bit 215 = 143 + 72 is 0, so bit 143 of y is 1. KEYMASK keeps exactly these bits. QED.

At every Gray point (point zero included) the six operations SHR, SHR, AND, XOR, XOR, AND form the key word in the
two temporaries; no key transpose is needed. Per group: 6 * 2^48 for the key words.

## 6. Outer cosets and setup

### 6.1 The cosets: fresh random origins

Coset j (0 <= j < C = 256 G) has origin t_j, drawn by the leader step (Section 6.2) from two fresh calls r_0, r_1 of the
cost model's primitive "independent uniform random 256-bit word": t_j = r_0 + (r_1 mod 2^64) 2^256. The C origins are
therefore independent and uniform on F_2^320. With the table tag r of Section 7 (one further fresh draw, independent of
them) they are CAMP's coins, and every probability below is over them, for the fixed target. Group h (h < G) holds
the cosets j = 256 h + c, c = 0..255. The candidate (h, c, i) (lane c, Gray point i) is the message
M(t_j XOR sum_b g(i)_b w_b) with j = 256 h + c; its identifier is cid = h 2^48 + c 2^40 + i < 2^128 (coset-major).
Inside each coset the enumeration is the fixed Gray order of span(W40). CAMP probes the candidates in increasing cid
(group by group, inside a group lane by lane, inside a lane in Gray order), so cid is also the number of candidates
probed before it.

**Lemma 7 (distinct messages).** Let D be the event that the C cosets t_j + span(W40) are pairwise distinct. On D the
Q = 2^48 G candidates are pairwise distinct messages, and Pr[not D] <= C(C, 2) 2^-280 = 2.4380...e-32 < 2.5e-32.

*Proof.* Distinct cosets of span(W40) are disjoint. Inside a coset, distinct i give distinct g(i) and, by rank 40,
distinct parameters; Lemma 1 gives distinct messages. For j < j' the sum t_j XOR t_j' is uniform on F_2^320 (t_j' is
uniform and independent of t_j), so the two cosets coincide with probability |span(W40)|/2^320 = 2^-280; the union
bound over the C(C, 2) pairs gives the bound. QED.

The event not D (a duplicate coset) is counted as a failure in Section 9; no duplicate rejection is performed.

### 6.2 Leader step (11 operations per coset, 5 per group)

For lane c of group h: j = H8 OR c with H8 = h * 2^8 (1); two random words r_0, r_1 (2); r_1 AND (2^64 - 1) (1); the
record address CSB + 2j (shift, add: 2); two STOREs of t_j into the global coset record with the second-word add (3);
two STOREs into the lane's working frame (2). This is 11 operations per coset. Group control is 5 per group:
H8 = h * 2^8 before the leader step, the identifier cid = h * 2^48 after the record transposes (Section 5.4), and
after the last lane the next index h = cid >> 48 (cid is then (h + 1) 2^48), its compare with G and the branch. S_v
(Section 6.5) charges exactly these 11 C + 5 G operations. The table register v = r 2^128 + cid
(Section 7) adds 3 per group: a LOAD of the tag word and an OR once cid is formed, and an AND that clears the tag
before the next index is read. Section 10 charges them as 3 G; the one-group experiment forms v in its one-time
control.

### 6.3 Bit-sliced evaluation (13,616 per group, 62,022 + 2 popcount(w(S)) per point)

The 256 lanes of a group are evaluated together at every S with |S| <= 8, the points in order of increasing |S|.
State word (l, z) holds bit z of lane l of the state of lane c at bit c, so the word operations below apply
theta, rho, pi, chi and iota to the 256 states at once (each acts bit by bit). Let w(S) = XOR of w_b over b in S;
the lane-c input at point S is A(t_j XOR w(S)) (Section 4), and w(S) is fixed in the generated code.

- **Transpose (13,616 per group).** The two working-frame words of the 256 origins become 320 bitplanes, bit c of
  plane k = bit k of t_j, by the butterfly of Section 5.4. First words: four blocks of 64 rows. A block keeps rows
  2..63 in registers and rows 0 and 1 in two fixed words (load: 62 LOADs and two LOAD, STORE pairs, 66); in stages
  s = 1..32 a pair in registers costs 6, a pair whose row k is in its word 8 (LOAD, 6 ALU, STORE) and the pair
  (0, 1) 12 (one spill word), so stage 1 costs 12 + 31 * 6 = 198 and stages 2..32 cost 2 * 8 + 30 * 6 = 196 each
  (1,178); storing the 64 plane words costs 62 STOREs and two LOAD, STORE pairs (66): 1,310 per block. Then stages
  s = 64 and 128 run on the 256 plane words as memory pairs, 10 each (2,560). Second words (below 2^64): four
  64 x 64 blocks the same way, block 0 stored into planes 256..319 (1,310) and block g = 1..3 shifted left by 64g
  and ORed into them (66 + 1,178 + 62 * 4 + 2 * 5 = 1,502). Total 4 * 1,310 + 2,560 + 1,310 + 3 * 1,502 = 13,616,
  with 62 row registers and two scratch registers.
- **Input (2 popcount(w(S)) per point).** Bit z of lane l < 5 is LOADed from plane k = 64 l + z; if bit k of w(S)
  is 1, its first LOAD (round 0) is followed by NOT and a STORE into its input word, which later LOADs of k read.
- **Constant folding.** In A(t) lanes 10..14 equal lanes 0..4, lane 16 is the padding 0x86 * 2^56 and the other
  lanes are zero (Section 2), the same in every lane c and at every point. Code generation therefore follows each of
  the 1,600 state words through rounds 0 to 4 and the round-5 linear step as a known constant (the zero word or the
  all-ones word, an immediate) or a data word, and emits an operation only when its result is not fixed: XOR with
  the zero word, AND with the all-ones word and v XOR v are not emitted, XOR with the all-ones word is one NOT, AND
  with the zero word gives the zero word. A data word is LOADed once per slice that reads it, theta's D words that
  are data are STOREd once, and a round STOREs each new data word once, into its own buffer (one 1,600-word buffer
  per round); round 0 reads lanes 10..14 from the words of lanes 0..4. No constant word is stored or loaded, and the
  pattern does not depend on S (w(S) only inverts data words): one code serves all points, input LOADs as above.
- **Rounds 0 to 4 (57,802 per point).** A round with data parities forms theta's D words slice by slice, slice 63
  first: the column parities of slice z (LOADs and XORs), then D[x][z] = C[x - 1][z] XOR C[x + 1][z - 1] and its
  STORE; the data parities of slice 63 stay in registers until D[x][63] (no wrap words). Then for each slice z: the
  rho-pi source words and D words (LOAD), their XOR, chi (NOT, AND, XOR), iota as one NOT of lane 0 when bit z of
  RC[r] is 1, and the STOREs. A round on 1,600 data words costs 64 * 45 + 320 * 2 = 3,520 for the D words and
  64 * 175 = 11,200 for the slices, plus the popcount of RC[r] (5, 3, 5 for r = 2, 3, 4): 14,725, 14,723 and 14,725
  for rounds 2, 3 and 4. In round 0 every column parity is constant (lanes x and x + 10 cancel), so theta adds
  constants: 640 LOADs, 668 NOTs, 314 XORs and 356 STOREs, 1,978. Round 1: 3,282 LOADs, 3,225 XORs, 1,674 NOTs,
  1,600 ANDs and 1,870 STOREs, 11,651. Rounds 0 to 4 cost 1,978 + 11,651 + 14,725 + 14,723 + 14,725 = 57,802. At
  most 28 values are live at once in any round (11, 28, 28, 28, 28; 16 in the linear step), within the 64 registers.
- **Round-5 linear step (4,220 per point).** The D words as above (3,520), then for each of the 175 planes (x, z),
  z <= 34: LOAD the source word, LOAD the D word, XOR, STORE into the coefficient record A[S] (4 * 175).

**Lemma 10 (bit-sliced setup).** After the setup steps of point S, bit c of plane word p of A[S] is f_t(e_S)_p for
the origin t = t_j of lane c; so A[S] = f(e_S) as Lemma 6 requires, for all 256 lanes.

*Proof.* A stage with d = s = 2^b exchanges row-index bit b with column-index bit b (Section 5.4), so the eight
stages on the 256 first words and the six stages on each 64-row block of second words, shifted by 64g (rows
c = 64g .. 64g + 63), leave bit k of t_j at bit c of plane k. Bit k of t_j XOR w(S) is that bit inverted when bit k
of w(S) is 1, so the input LOADs give lanes 0..4 of A(t_j XOR w(S)) in bit c; lanes 10..14 equal them and the
other lanes are the constants of A(t), the same in every lane c. Theta, rho and pi are the D step and the fixed
source addresses, chi and iota are bitwise (NOT of a lane-0 word is XOR with bit z of RC[r] in every lane), so the
unfolded round maps the state of every lane to its next state. Folding replaces an operation by its value where an
operand is the zero or all-ones word known at generation time (x XOR 0 = x, x AND 1 = x, x AND 0 = 0, x XOR 1 =
NOT x, x XOR x = 0, constants combine to constants), which changes no word; every word that the code LOADs was
STOREd earlier at the same point or is a bitplane. So each folded round computes the same 1,600 words, and the
linear step stores the bits b_{x,z} (z <= 34) of round 5. QED.

Over all points the input NOTs number pop_D = sum over |S| <= 8 of popcount(w(S)). Bit k of w(S) is 1 iff
|S & B_k| is odd, with B_k = {b : bit k of w_b is 1} and m_k = |B_k|, so pop_D = sum over k = 0..319 of
sum_{j odd, j <= 8} C(m_k, j) sum_{l <= 8 - j} C(40 - m_k, l) = 4,592,341,856.

### 6.4 Transform and phase

The truncated transform of Lemma 6 on the coefficient records costs two LOADs, XOR and STORE per pair (j, S) and
plane: 4 * 175 * J_D. The phase conversion writes the derivative records tab[T] (a frame disjoint from the
coefficient records) with v_T LOADs, v_T - 1 XORs and one STORE per plane: 2 * 175 * V_D. After both, the
coefficient record A[{}] is the current-value frame x = f(0).

**Valid access.** Every work word is written before it is read: the working frames by the leader step, the bitplanes
by the transpose (planes 256..319 by its block 0 before blocks 1..3 OR into them; the transpose words by each block
before it reads them), the input word of a plane by its first LOAD at a point whose w(S) inverts it (only then is it
read), the D words and round buffers by the generated code of the same point before any of its LOADs reads them (a
constant word is an immediate and is never read), A[S] by the linear step of point S (the transform reads only such
records), tab[T] by the phase conversion before the record transposes, the candidate-major records by the record
transposes before any frame copy, the frame of lane c by its copy before the FES of lane c, which reads no frame word
after its last change (Lemma 5b), and the spill words by verification before it reloads them; the next group's setup
rewrites the frames before reading them. The coset record of j is written by the leader step before any candidate of
coset j exists. The byte tables and the tag word are written in preprocessing, and the words of F and h right after
each leader step, before they are read (Sections 5.3 and 7).

### 6.5 Setup total

Per group: the leader step and group control 11 * 256 + 5 = 2,821 (Section 6.2), the transpose 13,616, the points
(57,802 + 4,220) P_D + 2 pop_D = 62,022 P_D + 2 pop_D, the transform 700 J_D and the phase 350 V_D:

    S_g = 2,821 + 13,616 + 62,022 P_D + 2 * 4,592,341,856 + 700 J_D + 350 V_D = 6,859,981,417,877,
    S_v = G S_g = 8,247,412,837,104,405,531,505,322,063,763,056,554.

The record transposes (7,800 P_D, Section 5.4), the frame copies (2 P_D per lane) and the FES (F_g, Section 5.3) are
charged in their own rows of Section 10.

## 7. Value-masked table and verification

The table is a direct table over the 140-bit key whose words carry a tag; there is no second array. The key word
k = key + 2^143 (Lemma 5d) is its own address: SPARSE[key] is the word at address k, in [2^143, 2^144). The tag r
is the low 128 bits of one call of the random-word primitive in preprocessing, fresh and independent of the origins
and of the initial memory, and the word r 2^128 is stored in the work region (Section 11.2). The identifier
cid = h 2^48 + c 2^40 + i (Section 6.1) of the current candidate runs through 0, 1, ..., Q - 1 in probe order; the
main loop holds v = r 2^128 + cid in one register, so cid is the low half of v. Every word the table writes is the
current v. The probe of the key word k (in one temporary) executes exactly, in the other temporary s:

```
s = LOAD [k];  s = s XOR v;  s = s >> 128;  BRANCH s   4   (s is arbitrary if the word was never written)
miss (s != 0):  STORE [k] = v;  v = v + 1              2   tags differ                         (6)
tag pass (s = 0):  s = LOAD [k];  s = (s < v);  BRANCH s           3
hit (s = 1):  s = LOAD [k];  s = s AND (2^128 - 1)     2   s: the stored identifier
              verification of s against cid, then v = v + 1           1                       (10)
false pass (s = 0):  STORE [k] = v;  s = LOAD [Fw];  s = s + 1;  STORE [Fw] = s;
                     s = (s == R140 + FP);  BRANCH s;  v = v + 1      7   stop if s = 1 (13)   (14)
```

On a tag pass the loaded word and v have equal high halves, so s < v holds iff the stored identifier is below cid.
A probe that misses costs 6 operations, charged as 6 Q. The verification count F, kept in its word Fw, counts every
tag pass, verified or false, and the run stops when F reaches R140 + FP, so a run has at most R140 + FP passes, each
at most 2760 operations beyond the 6 of a miss (4 + 2756 with its verification, or 8 for a false pass): Section 10
charges 2760 (R140 + FP). The probe uses the key word's register and s besides v: the two temporaries of
Section 5.3.

**Lemma 8 (value-masked table, any initial memory).** For an address a let tau(a) be the high half (bits 128 to 255)
of the word that a holds before the run. If the key word k of candidate cid has tau(k) != r, the probe of cid passes
the tag test iff some candidate x < cid has key word k, and then it returns the first such candidate.

*Proof.* Only probes of key word k read or write word k, and each write stores r 2^128 plus the writer's identifier.
Induction over these probes: if no candidate before cid has key word k, the word was never written, its tag
tau(k) != r, and the probe misses and stores r 2^128 + cid. Otherwise the first such candidate x0 stored
r 2^128 + x0 at its miss, and every later probe of k reads that word, passes with stored identifier x0 < cid and
returns x0 without a write, so the word keeps x0. QED.

A never-written word passes the 128-bit tag test with probability 2^-128 over the fresh r, whatever the initial
memory: r is independent of the memory and of the origins, which fix every key. Let Z be the number of candidates
whose key word k has tau(k) = r; for every fixed choice of origins E[Z] = Q 2^-128 < 1 over r, and only these
candidates can pass at a never-written word. Such a pass takes the false-pass path, which writes the word, or goes to
verification with an identifier s < cid of an earlier candidate, whose coset record exists, so verification reads
only written words and finds different digests or a true collision. The cap R140 + FP, with the allowance
FP = 2^100, halts every run after at most R140 + FP passes; Section 9 counts Z >= FP and the tag event at the
detecting key as failures. No word of SPARSE is initialized.

**Verification (at most 2754 operations: two six-round evaluations, 2 x 1271 = 2542, and at most 212 others;
charged as 2756, the bound that the experiment program asserts).** The verification count F is LOADed from its
word, incremented, STOREd, compared with R140 + FP and branched on (5). Then the 61 FES registers of the lane (the 60
cached records and x) are STOREd to fixed spill words (61) and LOADed back at the end (61); v stays in its register.
The generated code of the six rounds has at most 34 values live at once (a rotation's two temporaries included,
computed by the program from its code; a constant lane is an immediate), the first digest adds 4 during the second
evaluation and the message preambles hold fewer than one round, so verification uses at most 34 + 4 + 1 = 39 of the
64 registers.

- **The earlier candidate (58)**, a run-time identifier s: i = s AND (2^40 - 1) (1); j = ((s >> 48) << 8) OR
  ((s >> 40) AND 255) and the record address CSB + 2j (7); two LOADs of t_j with the second-word add (3);
  g(i) = i XOR (i >> 1) (2); for each byte b = 0..4 of g(i), q = (g >> 8b) AND 255 (one operation for b = 0)
  and from each of the two tables TB_{b,0} and TB_{b,1} the add of its base, a LOAD and
  an XOR into word 0, resp. 1, of t_j (8 per byte, 7 for byte 0: 39); lanes 0..4 (6: lanes 0..2 by two shifts and
  three 64-bit masks, lane 3 by one shift, the first word >> 192 being below 2^64, and lane 4 is the second word
  itself, below 2^64).
- **The current candidate (19).** Its probe runs in the code generated for lane c and Gray step i (Section 11.2), so the two
  words of sum_b g(i)_b w_b are immediates there. The rebuild is cid = v AND (2^128 - 1) (1), the record address as
  above (7), two LOADs with the second-word add (3), two XORs with the immediate words (2) and the lanes as above
  (6).
- **The six rounds (1271 per message).** Lanes 10..14 are the registers of lanes 0..4, and the fourteen zero lanes
  and the padding lane 16 = 0x86 * 2^56 are immediates. The rounds run as code generated once with the folding rule
  of Section 6.3 on 64-bit lanes: an operation is emitted only when its result is not fixed by the constants, a
  constant operand is an immediate, NOT of a lane is XOR with the immediate 2^64 - 1, and the rotation of a data
  lane costs two shifts, OR and AND (4). A round of data lanes costs 242 (theta parities 20, D 25 with one rotation
  each, application 25, rho 96 for the 24 nonzero rotations, pi as register renaming, chi 75, iota 1). In round 0
  every column parity is constant (lanes x and x + 10 cancel): 9 rotations (36), 17 XORs, 5 NOTs and 9 ANDs, 67;
  round 1: 29 rotations (116), 70 XORs, 25 NOTs and 25 ANDs, 236; rounds 2 to 5: 242 each. In all 1271, no
  permutation call, giving the native digest lanes 0..3. Folding changes no lane (the argument of Lemma 10 on 64-bit
  lanes), and the pattern is the same for every message.

Then at most four compares and branches (8) and the reload (61). Total at most 5 + 61 + 58 + 19 + 8 + 61 = 212
besides the two six-round evaluations. If F reaches R140 + FP the run stops (failure); on equal digests the two
parameters that verification built give the two output messages.
The byte tables TB_{b,k} (b = 0..4, k = 0, 1) hold for each byte value v word k of the XOR of w_{8b+j} over the set
bits j of v; the ten tables (2,560 words) are written once in preprocessing (Section 11.2).

**Address map (words).** Coset records [2^130, 2^130 + 2C); the work region (frames, plane and candidate-major
records, the lane frame, spill words, byte tables, the words of F and h, the tag word) from 2^131, fewer than 2^36
words; generated code from 2^132, fewer than 2^62 words; SPARSE [2^143, 2^144). The regions are disjoint and every
address is below 2^144.

## 8. The algorithm CAMP

```
Preprocessing (once, Section 11.2): generate the code, constants w_b, masks and byte tables; check rank and the
  780 polarizations of Lemma 3; h = 0; F = 0; draw the tag r and store r 2^128.
Group h (repeated):
  Setup (Section 6): leader step of the 256 cosets j = 256 h + c, each origin t_j drawn from two fresh random
    words; the transpose of the origins into 320 bitplanes; for every |S| <= 8, in order of increasing |S|, the
    constant-folded bit-sliced evaluation of the 256 lanes into A[S]; the transform; the phase conversion.
  Record transposes (Section 5.4): every record into 256 candidate-major words, one per lane.
  cid = h 2^48; v = r 2^128 + cid (Section 6.2).
  For c = 0..255 (lane c, coset j = 256 h + c):
    copy the records of lane c into the frame; load the 60 cached records and x (Section 5.3)
    for i = 0, 1, ..., 2^40 - 1 (Gray point i; candidate (h, c, i), identifier cid):
      if i >= 1: FES step i on the frame and registers (Section 5.3)
      key word k from x in 6 operations (Lemma 5d)
      probe k (Section 7; a false pass adds 1 to F); on a hit with s: verification of s against cid;
        if the digests are equal, output the two messages and stop; if F reached R140 + FP, stop with failure
  h = (v AND (2^128 - 1)) >> 48; if h = G, stop with failure.
```

Every bound (G groups, 256 lanes, 2^40 sites, R140 + FP tag passes) is a halt of the algorithm, and every candidate is probed
exactly once; F counts every tag pass, verified or false (Section 7), so the operation count of Section 10 is an
upper bound for every run.

## 9. Success

Let G = 1,202,250,025,869,134,545,910,402, C = 256 G = 307,776,006,622,498,443,753,062,912 cosets,
Q = 2^48 G = 338,403,298,031,900,219,834,956,980,958,854,643,712 candidates, lambda = Q(Q - 1)/2^257 =
0.4944931595636236108406620045... and T40 = sum_{k=0..40} lambda^k / k!.

**Lemma 9 (detection).** Suppose D holds (Lemma 7), the candidates contain two with equal digests, the run does not
stop at the cap R140 + FP, the first candidate C* in probe order that has an earlier candidate with the same digest
has a key word k* with tau(k*) != r (Lemma 8), and there is no bad triple: candidates A, B, C, A not in {B, C}, with
digest(B) = digest(C), key(A) = key(B) and digest(A) != digest(B). Then CAMP outputs a collision.

*Proof.* Let C = C*, B an earlier candidate with the same digest, and k = k* its key word. By Lemma 8 (tau(k) != r)
the probe of C hits and returns the first candidate A0 with key k (A0 precedes or equals B). If
digest(A0) = digest(B), the verification of A0 against C finds equal digests and CAMP outputs the two messages, which
are distinct on D (Lemma 7). Otherwise A0 != B; A0 has the key of B and C and a different digest, a bad triple. QED.

**Random variables.** Over CAMP's coins (the origins t_j), let F1 be the event that no two of the Q candidates have
equal digests, X the number of unordered pairs of candidates with equal 140-bit keys, and Y the number of bad triples
of Lemma 9. Let mu140 = Q(Q - 1)/2^141, r140 = ceil(mu140) = 41,080,884,463,506,626,072,264,787,223,246,591, the
Chebyshev parameter kappa = 19,345,871,228,983 and R140 = r140 + ceil(sqrt(kappa r140)) =
41,080,884,464,398,111,069,785,063,816,008,882. Over the tag r (Section 7), Z is the number of candidates whose key
word k has tau(k) = r, and FP = 2^100.

**Premise H_coset (Section 12).** Conditioned on D: (a) Pr[F1 | D] <= 1/T40; (b) E[X | D] <= mu140 and
Var[X | D] <= mu140; (c) E[Y | D] <= lambda (Q - 2)/2^140 = 0.000120059210262853... .

These are the bounds that independent uniform 256-bit digests of the Q distinct candidates give: (a) the probability
of no equal pair is prod_{k=1}^{Q-1} (1 - k 2^-256) <= exp(-lambda) <= 1/T40 (T40 is a partial sum of exp(lambda));
(b) the keys (140 digest bits XOR constants) are then uniform and the pair indicators pairwise independent (two pairs
sharing a candidate agree with probability 2^-280), so Var X <= E X = mu140; (c) C(Q, 2) (Q - 2) 2^-256 2^-140 =
lambda (Q - 2)/2^140. H_coset asserts these three bounds for CAMP's randomized enumeration; it is not proved.

**Theorem.** Over CAMP's fresh coins and under H_coset, CAMP outputs a collision with probability greater than 0.39.

*Proof.* If D holds, F1 fails, X < R140, Y = 0, Z < FP and tau(k*) != r, then CAMP outputs a collision: on D the
candidates are distinct messages (Lemma 7); F counts tag passes, and a pass reads either a written word, pairing the
probing candidate with an earlier candidate of equal key (at most X such passes), or a never-written word whose tag
is r (at most Z), so F stays below R140 + FP and the cap never stops the run; Lemma 9 applies. Hence

    Pr[failure] <= Pr[not D] + Pr[F1 | D] + Pr[X >= R140 | D] + Pr[Y >= 1 | D] + Pr[Z >= FP] + Pr[tau(k*) = r].

(0) Pr[not D] <= C(C, 2) 2^-280 = 2.4380395092434897...e-32 (Lemma 7, proved).
(i) Pr[F1 | D] <= 1/T40 by (a).
(ii) By (b) and Chebyshev's inequality, as R140 - mu140 >= ceil(sqrt(kappa r140)) >= sqrt(kappa mu140):
Pr[X >= R140 | D] <= Var[X | D]/(R140 - mu140)^2 <= mu140/(kappa mu140) = 1/kappa.
(iii) Pr[Y >= 1 | D] <= E[Y | D] <= lambda (Q - 2)/2^140 by (c) and Markov's inequality.
(iv) For fixed origins Z is a sum of Q indicators, each of probability 2^-128 over r, so Pr[Z >= FP] <= Q 2^-128/FP
= Q/2^228 by Markov's inequality. (v) The origins fix k*, so Pr[tau(k*) = r] = 2^-128.
The exact rational comparison of the six terms (integer numerators) gives

    C(C, 2) 2^-280 + 1/T40 + 1/kappa + lambda (Q - 2)/2^140 + Q/2^228 + 2^-128
      = 0.6099999999999999999999999999538768109... < 61/100,

G is the least group count for which this holds at this kappa (G - 1 gives a bound of at least 61/100), and kappa
is the least parameter for which it holds at this G (kappa - 1 gives at least 61/100). Hence the success
probability over the coins is greater than 0.3900000000000000000000000000461. QED.

## 10. Cost ledger and certificate

All charges are word operations of Section 5.1; no permutation call is made (verification evaluates the six rounds
in word operations, Section 7).

| term | value |
|---|---|
| FES, G F_g = G (256 Fc + 3) (Section 5.3) | 5,784,548,919,484,554,723,801,663,653,478,616,636,806 |
| record transposes, G 7,800 P_D (Section 5.4) | 939,130,931,853,730,804,407,603,991,019,774,400 |
| frame copies, G 512 P_D (Section 5.3) | 61,645,517,578,091,047,673,935,031,205,400,576 |
| key words, 6 Q (Lemma 5d) | 2,030,419,788,191,401,319,009,741,885,753,127,862,272 |
| setup, S_v = G S_g (Section 6.5) | 8,247,412,837,104,405,531,505,322,063,763,056,554 |
| table, 6 Q + 3 G (Sections 6.2 and 7) | 2,030,419,788,191,404,925,759,819,493,156,765,593,478 |
| tag passes and their verification, 2760 (R140 + 2^100) (Section 7) | 113,386,739,837,395,416,465,754,907,033,031,352,080 |
| preprocessing, ONCE = 2^70 + 16 | 1,180,591,620,717,411,303,440 |

    N = G F_g + G (7800 + 512) P_D + G S_g + 12 Q + 3 G + 2760 (R140 + 2^100) + ONCE
      = 9,968,023,424,991,292,613,601,158,421,224,940,979,606,

about 29.4560 operations per candidate (FES 17.0937, key 6, table 6, tag passes 0.3351, setup, transposes and
copies 0.0273). The time is N/1626 target compressions, and the integer certificate

    1626^100000 * 2^12220539 <= N^100000 < 1626^100000 * 2^12220540

gives log2(N/1626) = 122.2053916..., so time_log2 = 122.20540 (rounded up at the fifth decimal).

## 11. Memory, preprocessing and advice

### 11.1 Memory

SPARSE: the key words lie in [2^143, 2^144), 2^140 of them used (never initialized); coset records: 2C words (the
retained random origins); work: working frames 512, bitplanes 320, transpose words 3, input words 320, round buffers
5 * 1,600, D words 320, coefficient and derivative records 2 * 175 * P_D, candidate-major records 256 P_D, the lane
frame P_D, 61 spill words, the byte tables 2,560, the words that hold F and h, and the tag word, which every group
reuses (fewer than 2^36 words in all); generated code and its constants: fewer than 2^62 words. The regions are
disjoint (Section 7) and every address is below 2^144, so memory is below 2^144 words of 32 bytes, below 2^149
bytes.

### 11.2 Preprocessing: ONCE = 2^70 + 16 operations

(a) **Code generation.** Each of the 256 * 2^40 = 2^48 sites (lane c, Gray step i) is decoded (the set bits of i,
the frame addresses of T_1..T_L and their cache and last-change flags, the two words of sum_b g(i)_b w_b) in fewer
than 2^14 operations and emits at most 2,804 instructions: the FES step (at most 1 + 3 * 7 + 1 = 23), the key (6),
the probe with its tag-pass, hit and false-pass paths (6 + 3 + 3 + 7 = 19) and, on the hit path, the verification
inline (at most 2,756); the setup code (leader step, transpose, every point with the NOT pattern of w(S) and the
folded rounds, transform pairs and phase terms), the record transposes and the frame copies have one instruction per
operation of S_g + 7,800 P_D + 512 P_D, fewer than 2^43, each generated in at most 16 operations; the folding pattern
of the setup rounds (the same at every point) and the verification rounds (1,271 instructions per message, a
rotation counted as its four) come from one symbolic pass over the 1,600 state words of each round and over the 25
lanes, fewer than 2^25 operations. In all fewer than 2^60 instructions; at four words per instruction the code is
below 2^62 words and is generated in fewer than 2^63 operations.
(b) **Constants and certificate.** The two-word forms of w_b, the eight butterfly masks, rank 40 and the 780
polarizations of Lemma 3 (821 two-round evaluations): fewer than 2^25 operations.
(c) **The search that produced W40.** Step 1: the linear parts of the 1600 coordinates before the chi
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
(d) **One-time control.** h = 0, F = 0, the tag r (the low half of one random word) and the stored word r 2^128,
at most 16 operations.
(e) **Byte tables.** For each of the ten tables (b, k), b = 0..4, k = 0, 1: one zero STORE for v = 0, then each
entry v = 1..255 from entry v - 2^j (j the lowest set bit of v) by LOAD, XOR with the immediate word k of w_{8b+j}
and STORE: 10 (1 + 255 * 3) = 7,660.

The total is below 2^63 + 2^35 + 16 + 7,660 < 2^70 + 16 = ONCE, which is in N. In target compressions
ONCE/1626 < 2^59.34; the claim declares preprocessing_log2 = 59.34.

### 11.3 Advice

None. Every constant used by CAMP is produced by the procedures of Section 11.2, whose cost is in N.

## 12. Premise H_coset and evidence

**Statement.** Let the C = 256 G coset origins t_j be CAMP's coins: independent and uniform on F_2^320 (Section 6.1).
For the Q messages they generate, with the fixed Gray enumeration of span(W40) inside each coset and CAMP's order
(groups h = 0..G - 1, cosets j = 256 h + c, Gray points g(i)), and with F1, X, Y and D as in Sections 6.1 and 9,
assume over the coins: (a) Pr[F1 | D] <= 1/T40 (no full collision); (b) E[X | D] <= Q(Q - 1)/2^141 and
Var[X | D] <= Q(Q - 1)/2^141 (equal 140-bit keys); (c) E[Y | D] <= lambda (Q - 2)/2^140 (bad triples). These are the
values for independent uniform digests of distinct messages (Section 9). Success is then a probability over CAMP's
fresh coins; nothing is assumed about the randomness of the fixed target beyond (a) to (c).

This is assumed, not proved. The concern it answers: on a coset every digest bit is a polynomial of degree at most 16
in the 40 inner variables (Lemma 4 and the last chi), so equal-digest pairs inside a coset, or across random cosets,
could be rarer than for uniform values.

### 12.1 GPU evidence

**Batches 1 to 3 (preregistered, our runs; Appendix A holds every text, program and raw count).** Three batches at six
rounds, each fixed in a protocol file hashed before its runs (PREREG.txt, SHA-256
67e381a2c0dececee0ce10a8ac4591304076a161259e1cb9045f2c87df54fa58; PREREG2.txt, SHA-256
3b49de9f7c931d51a66ec7f31c2b0c4e3227bc8047cfd25ab5f727207bc01b4c; PREREG3.txt, SHA-256
5f94fcd22a4d94dddeef79ebc91f47b858793804e7d47e6784862e46479efc6a): sizes, statistics and the pass rule (every count of
the tested inputs at least expected - 4 sigma, sigma = sqrt(expected); no reruns). The GPU program computes real
six-round SHA3-256 digests of the messages M(t) (validated against the organizer reference sha3_256(rounds=6) on
2,048 of 2,048 digests for batches 1-2 and 512 of 512 for batch 3). Each run has 2^30 messages in ncos complete
cosets of dimension n. Field runs (batches 1-2): uniform random origins, n random independent elements of span(W40);
control runs (batches 1-2): uniform random origins, n random 320-bit directions; fixed-origin runs (batch 3): origins
XOR(q_b : bit b of g(j) set) for j = 0..ncos - 1, q_0, q_1, ... the coordinate vectors that extend the ordered W40
basis (an earlier fixed choice of origins), with the first n ordered vectors of W40 (the first 2^n Gray points
of each coset). **Random origins:** all runs of batches 1 and 2 drew their coset origins uniformly at random
(Appendix A.2, hc.py gen); they are the direct evidence for the premise as stated over random origins. Batch 3 shows
that even fixed origins give no deficit. Counts are exact
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
| D1 | fixed origins, n = 20, j = 0..1023 | 0 | 131,053 | 131,071.875 | -0.05 | 32,666 | -0.56 |
| D2 | fixed origins, n = 20, j = 0..1023 | 3 | 131,447 | 131,071.875 | +1.04 | 32,846 | +0.43 |
| D3 | fixed origins, n = 24, j = 0..63 | 1 | 2,095,169 | 2,097,151.875 | -1.37 | 32,689 | -0.44 |
| D4 | fixed origins, n = 24, j = 0..63 | 2 | 2,095,504 | 2,097,151.875 | -1.14 | 32,710 | -0.32 |

Verdict under the preregistered rule: all three batches pass. Over 17 runs, all four digest lanes and cosets of 2^20,
2^24 and 2^28 messages, every count lies within 2.1 sigma of its expectation, no count is below expected - 1.4 sigma,
and field, control and fixed-origin runs agree. A fourth preregistered batch at five rounds (Appendix A, context only)
also passes, including one more random-origin run.

**Batch W (preregistered, our runs; Appendix A.5).** One protocol, PREREG_W.txt (SHA-256
9cf0977ec63ac39f391a26d6a2913ab846fd7853c1595a8a54d47078fe8b4573), fixed six runs before their inputs were generated:
2^34 messages each, uniform random coset origins, one coset of dimension 34 (the first 34 ordered W40 vectors, 1/64 of
a complete coset of CAMP) or 1024 cosets of dimension 24 (the first 24 ordered W40 vectors), at six rounds (W1, W2)
and at five rounds (W4, W5, context), with random-direction controls W3 (six rounds) and W6 (five rounds). A second
GPU program, hcw.cu (the digest code of hcoset.cu with a bucketed pair count), gives the exact number of
equal-projection pairs among all 2^34 messages for the widths K = 36, 40, ..., 64 of six projections: the low K bits
of each digest lane (L0 to L3) and two two-lane projections (X01: the low ceil(K/2) bits of lane 0 interleaved with
the low floor(K/2) bits of lane 1; X23 the same for lanes 2 and 3). Expected for uniform digests:
E(K) = C(2^34, 2)/2^K, from 2,147,483,647.9 at K = 36 to 8.0 at K = 64; sigma = sqrt(E (1 - 2^-K)), the exact
standard deviation of a pair count of uniform values. Pass rule (one-sided; no reruns): every count of W1, W2, W4 and
W5 has z >= -4 where E >= 1000, and an exact Poisson lower tail of at least 3.17e-5 where E < 1000 (K = 60, 64).
Before the runs the GPU digests and keys were checked against the organizer reference at both round counts (1,536 of
1,536, recorded in PREREG_W.txt); Appendix A.6 repeats the check on the run inputs.

| run | rounds | inputs (2^34 messages, random origins) | counts | lowest z | highest z |
|---|---:|---|---:|---:|---:|
| W1 | 6 | 1 coset, first 34 W40 vectors | 48 | -2.45 (L1, K = 56) | +2.16 (L3, K = 48) |
| W2 | 6 | 1024 cosets, first 24 W40 vectors | 48 | -3.14 (X23, K = 36) | +2.12 (L3 and X23, K = 64) |
| W3 | 6 | control: 1 coset, 34 random directions | 48 | -2.63 (X23, K = 56) | +2.48 (L2, K = 44) |
| W4 | 5 | as W1 | 48 | -1.77 (X23, K = 44) | +2.26 (X01, K = 52) |
| W5 | 5 | as W2 | 48 | -1.26 (L0, K = 40) | +2.12 (L0, K = 64) |

Verdict under the preregistered rule: pass. None of the 240 counts lies beyond 4 sigma; the lowest, z = -3.14 (W2,
X23, K = 36), is a relative deficit of 6.8e-5 of about 2^31 expected pairs. W6 was stopped by us at 20 minutes of run
time without a result line (Appendix A.5, w.log); it is a control, outside the pass rule, reported and not replaced.

### 12.2 Organizer-executed tests

The declared experiments hcoset-within16 and hcoset-cross16 (Section 13) test a reduced-width form of (a) and (b) at
every organizer run, on the run's own six-round digests: per experiment 2^17 digests, one group of 256 cosets whose
origins come from the trials' coins (the organizer's seeds), the first 2^9 Gray points of each coset, projected to 16
and 24 digest bits (bits 0..3, resp. 0..5, of lanes 0..3). For uniform values every expectation below is exact and the
pass intervals are the expectation +- 4 standard deviations.

- Pair rates by class. The program stops (the experiment fails) unless each count lies in its interval: pairs inside
  one coset agreeing on 16 bits (33,488,896 pairs, expectation 511, interval [421, 601]); pairs across two cosets
  agreeing on 16 bits (8,556,380,160 pairs, expectation 130,560, [129115, 132005]) and on 24 bits (expectation 510,
  [420, 600]). Pair indicators of uniform values are pairwise independent, so each variance is n p (1 - p) exactly.
- Existence of an agreeing pair, the event that (a) bounds at full width. In hcoset-within16 each trial returns two of
  the 512 points of its own coset that agree on the 16 bits; in hcoset-cross16 a point a < 256 of its own coset and a
  point b >= 256 of the partner coset, whose origin is independent. The organizer recomputes both digests of every
  returned pair; the trials' message sets are disjoint, so for uniform values the successes are Binomial(256, P):
  P = 1 - prod_{i<512} (1 - i/2^16) = 0.864841510863844 (expectation 221.40, standard deviation 5.47, pass interval
  [200, 243]) and P = 0.632121969489614 (exact, from the occupancy law of one set; 161.82, 7.72, [131, 192]). A pair
  deficit or clustering, the dependence that (a) excludes, lowers these counts.

Run locally on the requests that the organizer's runner builds from its public seed, the two experiments give 224 and
165 successes and the group counts (pairs16_within, pairs16_cross, pairs24_cross) = (513, 131,526, 500) and (485,
130,615, 519), all inside their intervals; two runs of each are byte-identical. Scope: this is the organizer-executed
part of the evidence. It reaches 16 and 24 bits, 2^17 digests per run and 9-dimensional sub-cosets, not 256 bits,
complete cosets or Q messages, and it does not measure the key-match variance or triples at 140 bits.

### 12.3 Sensitivity

Suppose the pair-collision rate of CAMP's messages is (1 - eps) of uniform: the expected number of equal-digest pairs
is (1 - eps) lambda, and (a) becomes Pr[F1 | D] <= 1/T40((1 - eps) lambda), with T40(x) = sum_{k<=40} x^k/k!; (b) and
(c) keep their values (a lower pair rate does not raise them). For each eps the table gives the success bound of
Section 9 at this N (G and kappa unchanged; exact rational comparison with the printed value), and the least G at
which the failure bound, with the same kappa, is again below 61/100 (exact comparison; G - 1 fails), with the ledger
N of Section 10 at that G and the integer E of its certificate 1626^100000 2^(E - 1) <= N^100000 <
1626^100000 2^E, so time_log2 = E/100000 (rounded up at the fifth decimal); extra is that time_log2 minus the claim,
close to -(1/2) log2(1 - eps) in every row. Only the row eps = 0 is claimed.

| eps | success at this N | least G | N at that G | E | time_log2 | extra |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | > 0.39 | 1,202,250,025,869,134,545,910,402 | 9,968,023,424,991,292,613,601,158,421,224,940,979,606 | 12,220,540 | 122.20540 | 0 |
| 0.01 | > 0.386976 | 1,208,310,394,929,860,051,769,630 | 10,018,845,206,089,194,308,871,081,338,828,082,370,250 | 12,221,273 | 122.21273 | 0.00733 |
| 0.05 | > 0.374732 | 1,233,502,149,326,011,439,979,945 | 10,230,163,047,342,688,945,116,631,266,561,318,805,595 | 12,224,285 | 122.24285 | 0.03745 |
| 0.10 | > 0.359083 | 1,267,326,018,839,002,222,734,854 | 10,514,046,877,797,671,357,079,304,349,897,207,883,082 | 12,228,234 | 122.28234 | 0.07694 |
| 0.25 | > 0.309746 | 1,388,387,996,102,778,879,505,654 | 11,531,591,273,288,144,502,182,601,976,442,545,313,682 | 12,241,561 | 122.41561 | 0.21021 |

**Scope and extrapolation.** The evidence covers projections of at most 64 digest bits: 32-bit within-coset and 44-bit
global projections of single lanes on 2^30 messages (batches 1 to 3), 36- to 64-bit projections of single lanes and
of two-lane projections on 2^34 messages (batch W), and the organizer-executed 16- and 24-bit tests on 2^17 messages
per run (Section 12.2); sub-cosets of dimension 9 to 34 of span(W40); random origins (batches 1, 2 and W and the
organizer-executed tests) and fixed origins (batch 3). No count shows a pair deficit beyond the preregistered
thresholds. The premise extrapolates to the full 256-bit digest and its 140-bit key, to complete 40-dimensional
cosets, to C = 256 G random cosets and to Q messages: the full 256-bit collision event, the key-match variance and the
triple bound are not measured; they are the premise, and the table above gives the effect of a shortfall in the pair
rate.

**Limits.** No proof is known. Image size and balance do not imply the premise: a balanced linear map onto F_2^256 can
be injective on every translate of a campaign space, so its campaigns contain no collision at all. No such structure is
known for the native function and none is excluded by proof. The GPU batches are our runs; the organizer executes the
tests of Section 12.2.

## 13. Experiments

`experiments/fes_campaign.py` (Python standard library) serves the three declared experiments. Each run executes the
schedule of Sections 5 to 7 at a reduced size on the organizer's trials. fes-campaign-reduced checks the event of the
claim (two distinct messages with equal 256-bit digests; none expected at this size); hcoset-within16 and
hcoset-cross16 then run the premise test of Section 12.2, whose checked event is that the two returned digests agree
on bits 0..3 of lanes 0..3 (a 16-bit mask event, not a collision). The request must name one of the three experiments
with its event.

- Once per run: the program's six-round SHA3-256 equals the organizer reference on M(0) and M(w_0 XOR w_39)
  (hard-coded known-answer digests), and its 24-round version equals hashlib.sha3_256 on both; rank(W40) = 40; the 780
  polarizations of Lemma 3 vanish. A failed check stops the program.
- Groups: trials 256g .. 256g + 255 form one group; its index is h = int(seed of the group's first trial, 16) mod G,
  and trial k is lane c = k mod 256 of the cosets j = 256 h + c of Section 6.1. The leader step draws the origin t_j
  of lane c from the trial's own coins: its two random words (one counted RAND each) are the two halves of SHAKE-256
  of the trial's seed. This seed expansion only makes the run reproducible; it is not the attack's randomness, which
  is the fresh random-word primitive of Section 6.2.
- Reduced size: the first 2^9 Gray points of each coset (directions w_0..w_8), D = 8, all 175 planes, the full
  140-bit key and the value-masked table of Section 7 with Q' = 2^17 candidates and the verification cap of the same
  formula without the allowance FP (4,398,396).
- Every operation of the leader step, the setup schedule, the record transposes, the frame copies, the FES, the key,
  the table and verification runs through a counting machine (one call per primitive of Section 5.1; no permutation
  call; the generated code of the folded rounds runs one instruction, one primitive, at a time), and the program
  stops unless the executed counts equal the formulas above: 11 per coset leader and 5 per group; 13,616 for the
  transpose; at every point 1,978 + 2 popcount(w(S)) for round 0 with the input, 11,651, 14,725, 14,723 and 14,725
  for rounds 1 to 4 and 4,220 for the linear step, with the popcount sum 13,530 of the formula of Section 6.3 at
  n = 9; 4 * 175 J_D and 2 * 175 V_D for transform and phase; 7,800 per record transpose (511 records); per lane
  2 * 511 for the frame copy, the step count of Section 5.3 at every Gray step and Fc = 3,301 (the formula of
  Section 5.3 at n = 9); 3 per group for h and F; 6 per candidate for the key; 6 / 14 / 10 table operations per
  candidate (each probe; a false pass counts in F, 13 when it stops the run at the cap); 7,660 for the byte tables;
  in verification 5 for F, 61 and 61 for the spill and reload, 58 for the earlier and 19 for the current candidate,
  67, 236, 242, 242, 242 and 242 for the six folded rounds of each, and at most 2756 operations per verification. It
  also checks Fc = 18,794,671,433,175 and pop_D = 4,592,341,856 at n = 40, and the register peaks of its generated
  code (Sections 6.3 and 7).
- The counted bit-sliced setup of Section 6.3 runs on all 256 lanes at all 511 points. The bitplanes must equal the
  origins bit for bit, and every coefficient record must equal, on every lane, an independent evaluation that is not
  counted (rounds 0 and 1 by Lemma 3 (b), then rounds 2 to 4 and the linear step); the candidate-major current
  values of every lane must equal the planes (Lemma 5c). Never-written sparse
  words read as a fixed pseudo-random function of their address, either a word of at least 2^255 or h 2^48 plus a
  value below 2 Q', so their high half (0 or at least 2^127) never equals the run's tag, an odd value below 2^127
  formed from h, and every fresh key takes the 6-operation miss; a read of a never-written work or coset word, or of
  a frame word after its last change (Lemma 5b), stops the program.
- Beside the algorithm, not counted: at point i the message of lane i mod 256 is hashed natively and its 140 key bits,
  with bit 143 set, are compared with the emitted key word (key_mismatch); after the run the first candidate's key is
  probed again (a valid hit, 10 operations) and verified against the candidate (c, i) = (80, 1), with the
  reconstructed sources and digests compared with the native ones.
- Also beside the algorithm, in fes-campaign-reduced: own_pairs16, the number of unordered pairs of the trial's own
  512 candidates whose emitted keys agree on event bits 0..15 (bits 0..3 of digest lanes 0..3). Uniform digests give
  C(512, 2)/2^16 = 1.996 per trial and 511 per 256 trials; a local 256-trial request gave 527 (z = +0.71).
- Premise test, in hcoset-within16 and hcoset-cross16, not counted. Key bit 36x + z is digest bit z of lane x (RC[5]
  cancels in an equality); event bit 4z + x is that key bit, so event bits 0..15 and 0..23 are the 16- and 24-bit
  projections of Section 12.2. The program counts pairs16_within, pairs16_cross and pairs24_cross over the group's 2^17
  keys and stops unless each lies in its pass interval. Trial k (lane c) then returns the first repeat of event bits
  0..15 among the 512 points of its own coset in Gray order (hcoset-within16), or the first point b >= 256 of coset
  c XOR 1, in Gray order, whose event bits 0..15
  equal those of a point a < 256 of coset c, with that a (hcoset-cross16). Each returned pair is hashed natively and
  must agree on the mask; a trial without such a pair returns two nulls. A full collision among 2^17 messages
  (probability below 2^-222) would be returned by trial 0 instead, without the test.

In fes-campaign-reduced the program reports 16 numbers per trial: own_pairs16 (its own coset), and 15 that are the
same for all trials of a group: fes_ops = 845,059 (256 * 3,301 + 3); buffer_reads = 261,632 (the frame copies,
256 * 2 * 511); chi_transpose_ops = 4,772,232 (the key, 6 * 2^17, and the record transposes, 7,800 * 511);
table_ops = 6 (2^17 - x - m) + 14 x + 10 m with x = in_range_mismatches (false tag passes) and
m = key_matches; sparse_inserts = 2^17 - m; leader_ops = 2,821 (11 * 256 + 5); setup_group_ops = 13,616 (the
transpose); setup_point_ops = 31,720,302 (62,022 * 511 + 2 * 13,530); transform_phase_ops = 2,419,200;
verify_check_ops (at most 10 + 2756; 2,758 here); perm_calls = 0; native_checks = 512; key_mismatch = 0. In
hcoset-within16 and
hcoset-cross16 it reports, the same for all trials of the group, these 15 without buffer_reads and sparse_inserts
(checked inside the program) and pairs16_within, pairs16_cross and pairs24_cross. The program also asserts
once_ops = 7,666 (control 6: h, F, the tag, r 2^128 and v; byte tables 7,660) without reporting it. No trial of
fes-campaign-reduced returns a pair: a 256-bit collision among 2^17 messages has probability below 2^-222. Nothing
about cost is inferred from the runs, and the premise tests are evidence at 16 and 24 bits, not at 256 bits.

## 14. Credits

- GPT Sol cloud: the two-round affine field and its certificate.
- GPT Sol local and GPT Luna: the exact ledger (initialization, schedule, setup, table and success) and the check
  of the schedule savings (D83).
- Grok: transpose and table code, executed operation counts, the schedule savings of jobs 64, 67, 70 and 72
  (constant folding, the verification schedule, the Chebyshev parameter, the schedule savings) and the executed
  bit-sliced setup of job 69.
- Bouillaguet, Chen, Cheng, Chou, Niederhagen, Shamir and Yang, CHES 2010: fast exhaustive search by Gray-code finite
  differences.
- Th0rgal (76ccfa1c): the earlier remark that the digest's degree in a 32-bit counter is at most 32 (prior context).
- rubenmarcus (91f1424d, sha3-256-r5): earlier use of degree-4 Gray-order finite differences in this contest, there to solve connector equations (prior context).
- Jbenisek, with the daydream panel (compiler and accountant voices, our agents): the preregistered H_coset runs,
  the kernel checks, the schedule levers, the package and the experiment program with its premise tests.

**Changes from edaff0da.** This package is our edaff0da (time_log2 122.55792) with the plane-major FES and the
key transpose replaced by the candidate-major schedule of Sections 5.3 and 5.4: each record is transposed once per
group into one word per coset lane (7,800 operations per record), every lane runs FES on vector words with 60 cached
records, and the key is formed in the word in 6 operations, so no buffer and no per-point transpose remain;
identifiers are coset-major and the key words lie in [2^143, 2^144). The table, the false-pass halt, G, kappa, Q,
R140, the failure sum and the premise H_coset are unchanged. The candidate-major route was found by our r6-push grid
scout and checked by its checker; GPT Luna (D107) worked out the exact ledger.

## Appendix A. H_coset evidence: preregistrations, programs and raw counts

Everything below is copied byte for byte from our working files; for each text the SHA-256 is that of the
file, which equals the SHA-256 of the lines of its block, each ending in LF (the one exception, w_analysis.txt in
A.5, is marked there). Internal labels inside the texts
(D17, D19, D23, SOLCLOUD_12, SOLCLOUD_16) name our working notes: "D19 Section 6" is the fixed choice of origins
of batch 3 described in Section 12, the W40 order is that of Section 3, and SOLCLOUD_12_INPUT_keccak.py is a
byte-identical copy of the organizer reference verifier/keccak.py (SHA-256
95ce77dff0476301c05057e01296f3e3507c4926423257540cfc3e5fd36ee0ae).

### A.1 Preregistrations

Each protocol was written and hashed before any count run of its batch. Decimal expectations quoted inside the
texts are approximations; the stated formula ncos C(2^n, 2)/2^32 governs (PREREG.txt misprints the n = 24 value
as 2147483616.0; the formula gives 2,097,151.875). The z values of A.3 use the exact formulas.

**PREREG.txt** (SHA-256 67e381a2c0dececee0ce10a8ac4591304076a161259e1cb9045f2c87df54fa58, recorded in PREREG.sha256 when written):

```
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

**PREREG2.txt** (SHA-256 3b49de9f7c931d51a66ec7f31c2b0c4e3227bc8047cfd25ab5f727207bc01b4c, recorded in PREREG2.sha256 when written):

```
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

**PREREG3.txt** (SHA-256 5f94fcd22a4d94dddeef79ebc91f47b858793804e7d47e6784862e46479efc6a, recorded in PREREG3.sha256 when written):

```
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

**PREREG_R5.txt** (SHA-256 0a98c8a57288c2403d3082da7484dac332eec8ded347a7666a9b7e30df109876, recorded in PREREG_R5.sha256 when written):

```
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

### A.2 GPU program and driver

hcoset.cu computes real SHA3-256 digests (organizer round function, rounds from HC_ROUNDS, default 6) of the
135-byte one-block messages M(t) for t = origin_c XOR (subset sum of the n directions), and counts exact
equal-key pairs (sum of C(len, 2) over equal keys after a sort). hc.py writes the inputs: for MODE field and
ctrl the origins are rng.getrandbits(320) with rng = random.Random("MODE-SEED"), uniform random 320-bit
origins; MODE det writes the fixed origins of batch 3. hc.py imports from our working folder cube_degree.W (the
ordered W40 list of Section 3, checked equal), cube_degree.rank (GF(2) rank) and cube_degree.kec (the organizer
verifier/keccak.py above).

**hcoset.cu** (SHA-256 28c40823a37afd1d22fb487b5ab77622c2036e5bc6763a330d83d1a9f66069f8):

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

**hc.py** (SHA-256 9ba0863a64aaaf87399a0f4b48d8ea595b28d43bb0ecf63436501fac5f1967ea):

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

### A.3 Run scripts, raw result lines and z

Each run script appends one JSON line per run to its result file, in the order of its lines. Expected values
for uniform digests: within = ncos C(2^n, 2)/2^32 (pairs inside one coset, low 32 bits of digest lane L);
global = C(2^30, 2)/2^44 = 32,767.99997 (all 2^30 messages, low 44 bits of lane L); z = (count -
expected)/sqrt(expected).

**batch 1 (PREREG.txt), six rounds**: run_main.sh and main_results.jsonl (SHA-256 39fa7d2af4638d3bdeeceb45eb0cf844261f3796f2c4f8c00b4131b96c1e17fc).

```sh
#!/bin/bash
B=/root/hcoset_bin/hcoset; D="/mnt/d/~~Projects/~HashSmash/workspace/research/sha3r6/hcoset"
O="$D/main_results.jsonl"; date >> "$D/main.log"
$B count "$D/in_field_1001.bin" 20 1024 44 0 >> "$O"
$B count "$D/in_field_1001.bin" 20 1024 44 3 >> "$O"
$B count "$D/in_ctrl_1001.bin" 20 1024 44 0 >> "$O"
$B count "$D/in_ctrl_1001.bin" 20 1024 44 3 >> "$O"
$B count "$D/in_field_1002.bin" 24 64 44 0 >> "$O"
$B count "$D/in_ctrl_1002.bin" 24 64 44 0 >> "$O"
date >> "$D/main.log"
```

```
{"n": 20, "ncos": 1024, "lane": 0, "messages": 1073741824, "within32_pairs": 131380, "global_bits": 44, "global_pairs": 33033, "cuda": "no error"}
{"n": 20, "ncos": 1024, "lane": 3, "messages": 1073741824, "within32_pairs": 130720, "global_bits": 44, "global_pairs": 32964, "cuda": "no error"}
{"n": 20, "ncos": 1024, "lane": 0, "messages": 1073741824, "within32_pairs": 131300, "global_bits": 44, "global_pairs": 32762, "cuda": "no error"}
{"n": 20, "ncos": 1024, "lane": 3, "messages": 1073741824, "within32_pairs": 130930, "global_bits": 44, "global_pairs": 32709, "cuda": "no error"}
{"n": 24, "ncos": 64, "lane": 0, "messages": 1073741824, "within32_pairs": 2097299, "global_bits": 44, "global_pairs": 32651, "cuda": "no error"}
{"n": 24, "ncos": 64, "lane": 0, "messages": 1073741824, "within32_pairs": 2098309, "global_bits": 44, "global_pairs": 32777, "cuda": "no error"}
```

| run | inputs | n, cosets | lane | within | expected | z | global | z |
|---|---|---|---:|---:|---:|---:|---:|---:|
| R1 | field 1001, random origins | 20, 1024 | 0 | 131,380 | 131,071.875 | +0.85 | 33,033 | +1.46 |
| R2 | field 1001, random origins | 20, 1024 | 3 | 130,720 | 131,071.875 | -0.97 | 32,964 | +1.08 |
| R3 | ctrl 1001, random origins | 20, 1024 | 0 | 131,300 | 131,071.875 | +0.63 | 32,762 | -0.03 |
| R4 | ctrl 1001, random origins | 20, 1024 | 3 | 130,930 | 131,071.875 | -0.39 | 32,709 | -0.33 |
| R5 | field 1002, random origins | 24, 64 | 0 | 2,097,299 | 2,097,151.875 | +0.10 | 32,651 | -0.65 |
| R6 | ctrl 1002, random origins | 24, 64 | 0 | 2,098,309 | 2,097,151.875 | +0.80 | 32,777 | +0.05 |

**batch 2 (PREREG2.txt), six rounds**: run_main2.sh and main2_results.jsonl (SHA-256 c1f127c8880d3b90d3c61a47c3381a8a04e8a1f1e506ceb0e89dc4b8c714ba4b).

```sh
#!/bin/bash
B=/root/hcoset_bin/hcoset; D="/mnt/d/~~Projects/~HashSmash/workspace/research/sha3r6/hcoset"
O="$D/main2_results.jsonl"; date >> "$D/main2.log"
$B count "$D/in_field_2001.bin" 20 1024 44 1 >> "$O"
$B count "$D/in_field_2001.bin" 20 1024 44 2 >> "$O"
$B count "$D/in_ctrl_2001.bin" 20 1024 44 1 >> "$O"
$B count "$D/in_ctrl_2001.bin" 20 1024 44 2 >> "$O"
$B count "$D/in_field_2002.bin" 28 4 44 0 >> "$O"
$B count "$D/in_field_2002.bin" 28 4 44 2 >> "$O"
$B count "$D/in_ctrl_2002.bin" 28 4 44 0 >> "$O"
date >> "$D/main2.log"
```

```
{"n": 20, "ncos": 1024, "lane": 1, "messages": 1073741824, "within32_pairs": 130589, "global_bits": 44, "global_pairs": 32932, "cuda": "no error"}
{"n": 20, "ncos": 1024, "lane": 2, "messages": 1073741824, "within32_pairs": 130672, "global_bits": 44, "global_pairs": 32606, "cuda": "no error"}
{"n": 20, "ncos": 1024, "lane": 1, "messages": 1073741824, "within32_pairs": 130638, "global_bits": 44, "global_pairs": 32925, "cuda": "no error"}
{"n": 20, "ncos": 1024, "lane": 2, "messages": 1073741824, "within32_pairs": 131237, "global_bits": 44, "global_pairs": 32715, "cuda": "no error"}
{"n": 28, "ncos": 4, "lane": 0, "messages": 1073741824, "within32_pairs": 33555785, "global_bits": 44, "global_pairs": 32648, "cuda": "no error"}
{"n": 28, "ncos": 4, "lane": 2, "messages": 1073741824, "within32_pairs": 33557768, "global_bits": 44, "global_pairs": 32736, "cuda": "no error"}
{"n": 28, "ncos": 4, "lane": 0, "messages": 1073741824, "within32_pairs": 33566477, "global_bits": 44, "global_pairs": 32926, "cuda": "no error"}
```

| run | inputs | n, cosets | lane | within | expected | z | global | z |
|---|---|---|---:|---:|---:|---:|---:|---:|
| S1 | field 2001, random origins | 20, 1024 | 1 | 130,589 | 131,071.875 | -1.33 | 32,932 | +0.91 |
| S2 | field 2001, random origins | 20, 1024 | 2 | 130,672 | 131,071.875 | -1.10 | 32,606 | -0.89 |
| S3 | ctrl 2001, random origins | 20, 1024 | 1 | 130,638 | 131,071.875 | -1.20 | 32,925 | +0.87 |
| S4 | ctrl 2001, random origins | 20, 1024 | 2 | 131,237 | 131,071.875 | +0.46 | 32,715 | -0.29 |
| S5 | field 2002, random origins | 28, 4 | 0 | 33,555,785 | 33,554,431.875 | +0.23 | 32,648 | -0.66 |
| S6 | field 2002, random origins | 28, 4 | 2 | 33,557,768 | 33,554,431.875 | +0.58 | 32,736 | -0.18 |
| S7 | ctrl 2002, random origins | 28, 4 | 0 | 33,566,477 | 33,554,431.875 | +2.08 | 32,926 | +0.87 |

**batch 3 (PREREG3.txt), six rounds**: run_main3.sh and main3_results.jsonl (SHA-256 d86b4fedfe8dfaaa6dec16353148fb2ac9e9f73229acffaf57341fe6c85a94c4).

```sh
#!/bin/bash
B=/root/hcoset_bin/hcoset; D="/mnt/d/~~Projects/~HashSmash/workspace/research/sha3r6/hcoset"
O="$D/main3_results.jsonl"; date >> "$D/main3.log"
$B count "$D/in_det_3001.bin" 20 1024 44 0 >> "$O"
$B count "$D/in_det_3001.bin" 20 1024 44 3 >> "$O"
$B count "$D/in_det_3002.bin" 24 64 44 1 >> "$O"
$B count "$D/in_det_3002.bin" 24 64 44 2 >> "$O"
date >> "$D/main3.log"
```

```
{"n": 20, "ncos": 1024, "lane": 0, "messages": 1073741824, "within32_pairs": 131053, "global_bits": 44, "global_pairs": 32666, "cuda": "no error"}
{"n": 20, "ncos": 1024, "lane": 3, "messages": 1073741824, "within32_pairs": 131447, "global_bits": 44, "global_pairs": 32846, "cuda": "no error"}
{"n": 24, "ncos": 64, "lane": 1, "messages": 1073741824, "within32_pairs": 2095169, "global_bits": 44, "global_pairs": 32689, "cuda": "no error"}
{"n": 24, "ncos": 64, "lane": 2, "messages": 1073741824, "within32_pairs": 2095504, "global_bits": 44, "global_pairs": 32710, "cuda": "no error"}
```

| run | inputs | n, cosets | lane | within | expected | z | global | z |
|---|---|---|---:|---:|---:|---:|---:|---:|
| D1 | det 3001, fixed origins | 20, 1024 | 0 | 131,053 | 131,071.875 | -0.05 | 32,666 | -0.56 |
| D2 | det 3001, fixed origins | 20, 1024 | 3 | 131,447 | 131,071.875 | +1.04 | 32,846 | +0.43 |
| D3 | det 3002, fixed origins | 24, 64 | 1 | 2,095,169 | 2,097,151.875 | -1.37 | 32,689 | -0.44 |
| D4 | det 3002, fixed origins | 24, 64 | 2 | 2,095,504 | 2,097,151.875 | -1.14 | 32,710 | -0.32 |

**batch R5 (PREREG_R5.txt), FIVE rounds, context only**: run_r5.sh and r5_results.jsonl (SHA-256 ca3a763a9b5a6567233848f8bf95908a9cf3aac1dab1712e88e70e5407054fad).

```sh
#!/bin/bash
export HC_ROUNDS=5
B=/root/hcoset_bin/hcoset; D="/mnt/d/~~Projects/~HashSmash/workspace/research/sha3r6/hcoset"
O="$D/r5_results.jsonl"; date >> "$D/r5.log"
$B count "$D/in_det_4001.bin" 20 1024 44 0 >> "$O"
$B count "$D/in_det_4001.bin" 20 1024 44 3 >> "$O"
$B count "$D/in_det_4002.bin" 24 64 44 1 >> "$O"
$B count "$D/in_det_4002.bin" 24 64 44 2 >> "$O"
$B count "$D/in_field_4003.bin" 20 1024 44 0 >> "$O"
$B count "$D/in_ctrl_4003.bin" 20 1024 44 0 >> "$O"
date >> "$D/r5.log"
```

```
{"n": 20, "ncos": 1024, "lane": 0, "messages": 1073741824, "within32_pairs": 130774, "global_bits": 44, "global_pairs": 32882, "cuda": "no error"}
{"n": 20, "ncos": 1024, "lane": 3, "messages": 1073741824, "within32_pairs": 130530, "global_bits": 44, "global_pairs": 32926, "cuda": "no error"}
{"n": 24, "ncos": 64, "lane": 1, "messages": 1073741824, "within32_pairs": 2095898, "global_bits": 44, "global_pairs": 32547, "cuda": "no error"}
{"n": 24, "ncos": 64, "lane": 2, "messages": 1073741824, "within32_pairs": 2096787, "global_bits": 44, "global_pairs": 32836, "cuda": "no error"}
{"n": 20, "ncos": 1024, "lane": 0, "messages": 1073741824, "within32_pairs": 130789, "global_bits": 44, "global_pairs": 32857, "cuda": "no error"}
{"n": 20, "ncos": 1024, "lane": 0, "messages": 1073741824, "within32_pairs": 130646, "global_bits": 44, "global_pairs": 32555, "cuda": "no error"}
```

| run | inputs | n, cosets | lane | within | expected | z | global | z |
|---|---|---|---:|---:|---:|---:|---:|---:|
| P1 | det 4001, fixed origins | 20, 1024 | 0 | 130,774 | 131,071.875 | -0.82 | 32,882 | +0.63 |
| P2 | det 4001, fixed origins | 20, 1024 | 3 | 130,530 | 131,071.875 | -1.50 | 32,926 | +0.87 |
| P3 | det 4002, fixed origins | 24, 64 | 1 | 2,095,898 | 2,097,151.875 | -0.87 | 32,547 | -1.22 |
| P4 | det 4002, fixed origins | 24, 64 | 2 | 2,096,787 | 2,097,151.875 | -0.25 | 32,836 | +0.38 |
| P5 | field 4003, random origins | 20, 1024 | 0 | 130,789 | 131,071.875 | -0.78 | 32,857 | +0.49 |
| P6 | ctrl 4003, random origins | 20, 1024 | 0 | 130,646 | 131,071.875 | -1.18 | 32,555 | -1.18 |

Random-origin runs (R1-R6, S1-S7 at six rounds; P5 at five rounds): 14 runs, 28 counts, z from
-1.33 to +2.08. All 23 runs: z from -1.50 to +2.08; every count is above expected - 4 sigma, the preregistered pass rule.

### A.4 Validation of the GPU digests

Before the count runs, hc.py validate dumped GPU digests and compared each with the organizer reference
sha3_256(message, rounds=R) of verifier/keccak.py: 2,048 of 2,048 equal at six rounds before batch 1 (recorded
in PREREG.txt), 512 of 512 equal at six rounds on the fixed-origin inputs before batch 3, and 512 of 512 equal at
five rounds before batch R5 (recorded in PREREG_R5.txt), with 256 of 256 still equal at six rounds. The batch 3
and six-round R5 checks are recorded in our result notes, not in a hashed file; the validation printouts were
not kept; Appendix A.6 repeats the checks on the input files of the count runs and keeps the printout. These are our
runs; the organizer has not executed them.

### A.5 Batch W: protocol, programs, raw counts and z

Files of our working folder for batch W. hw.py gen writes the inputs: MODE rord takes 320-bit origins
rng.getrandbits(320) with rng = random.Random("W-MODE-SEED"), uniform random origins, and the first n ordered W40
vectors; MODE ctrl draws n random 320-bit directions of rank n, then the origins, from the same generator. hw.py
imports cube_degree as in A.2. hcw.cu computes the six- or five-round digests and counts the exact equal-projection
pairs of the six projections in 2^b passes over the top b key bits. W_HASHES.sha256, written after the runs, lists
the SHA-256 of PREREG_W.txt, hcw.cu, hw.py, run_w.sh, w_results.jsonl and w_analysis.txt as given here.

**PREREG_W.txt** (SHA-256 9cf0977ec63ac39f391a26d6a2913ab846fd7853c1595a8a54d47078fe8b4573, recorded in PREREG_W.sha256
before the inputs were generated):

```
PREREGISTRATION W (lane-hcoset-wide) - H_coset, wider and larger, RANDOM coset origins, rounds 6 and 5.
Written 2026-10-10 02:28 (local clock), before any count run of this batch and before its inputs were generated.

Aim: the judges' material finding on e641788b (F-FULL-SCALE-EXTRAPOLATION: "Agreement of low-width projected pair
counts on at most 2^30 messages does not establish independent uniform 256-bit outputs over the vastly larger
campaign"). This batch is 16x larger (2^34 messages per run, was 2^30), wider (every width K = 36..64 in steps of 4,
up to a whole 64-bit digest lane and 64-bit joint projections of two lanes; was 32 and 44 bits of one lane), uses
random coset origins (the refiled design), puts 2^34 messages in ONE 34-dimensional coset (1/64 of a complete
40-dimensional coset; was at most 28 dims) for within-coset pairs, and 1024 cosets of 24 dims for across-coset pairs.

Program: hcw.cu in this folder (a copy of research/sha3r6/hcoset/hcoset.cu digest(), rounds and rotation offsets as
compile-time constants; new bucketed width ladder; the original is not edited). Checks done before this file:
 - digests 1536/1536 equal the organizer sha3_256(rounds=6) and 1536/1536 equal sha3_256(rounds=5)
   (SOL6Cloud/SOLCLOUD_12_INPUT_keccak.py) at the batch geometry: n=34 one coset (indices 0..511 and
   2^33+12345..+511, rord seed 9001) and n=24 x 1024 cosets (coset 1000, ctrl seed 9002); the 6 GPU keys of the same
   messages equal an independent pure-Python derivation from the organizer digests (1536/1536 at each round count).
 - end to end: GPU bucketed ladder (b=3, 8 passes) EQUAL to exact numpy pair counts over 2^20 GPU digests, all
   6 projections x 8 widths (rounds 6 rord seed 9003; rounds 5 ctrl seed 9003).
 - timing: one full-size pass on throwaway seed 9004 (rord, n=34, rounds 6) took 4.1 s; its partial counts were
   discarded unread. Seeds 9001-9004 are not used below.

Inputs: python hw.py gen MODE SEED N NCOS. rord = random 320-bit origins + the first N ordered W40 vectors
(cube_degree.W, the route's direction order); ctrl = random 320-bit origins + N random 320-bit directions (rank N).
Message embedding as hcoset.cu / cube_degree.py (u0..u4 in lanes 0-4 and 10-14, lane 16 = 0x86<<56).

Projections (top K bits of a 64-bit key): L0..L3 = low K bits of digest lane 0..3; X01 = low ceil(K/2) bits of
lane 0 with low floor(K/2) bits of lane 1 (bit-interleaved); X23 = the same for lanes 2 and 3.
Count: exact number of equal-projection pairs (sum over equal runs of C(len,2)) over all 2^34 messages; bucketed by
the top b=6 key bits (64 passes; pairs at K >= 6 never straddle buckets).

Runs (all 2^34 messages, b=6, widths 36,40,44,48,52,56,60,64), in this order, one GPU job:
  W1 rounds 6  rord 5101  n=34  1 coset          W4 rounds 5  rord 5104  n=34  1 coset
  W2 rounds 6  rord 5102  n=24  1024 cosets      W5 rounds 5  rord 5105  n=24  1024 cosets
  W3 rounds 6  ctrl 5103  n=34  1 coset          W6 rounds 5  ctrl 5106  n=34  1 coset

Expected under independent uniform digests: E(K) = C(2^34,2) / 2^K = 2^(67-K) - 2^(33-K):
K=36 2147483647.9, 40 134217728.0, 44 8388608.0, 48 524288.0, 52 32768.0, 56 2048.0, 60 128.0, 64 8.0.
Sigma = sqrt(E (1 - 2^-K)), the exact standard deviation of the pair count under that model (pair indicators are
pairwise independent).

Pass rule (one-sided; the premise needs no pair deficit): for EVERY rord (field) count, W1 W2 W4 W5, all 6
projections and 8 widths: z = (observed - E)/sigma >= -4 when E >= 1000; for E < 1000 (K = 60, 64) the exact
Poisson lower tail P(X <= observed) >= 3.17e-5 (the one-sided 4-sigma level). Any field failure = H_coset NOT
supported at that round count; reported as such; no reruns, no other seeds or parameters. A run is valid only if
every projection kept exactly 2^34 keys and no bucket overflowed; an invalid run is reported, not replaced.
Reported: two-sided z for all 288 counts (field and control); any |z| > 4 excess is reported as an anomaly (an excess
does not contradict the premise's direction). Control runs W3 W6 calibrate the method; they do not enter the rule.

Power and scope (stated now): K=64 (E=8) cannot fail the rule (P(X=0) = 3.4e-4); K=60 fails only below about 87
pairs. The decisive counts are K <= 56: a 4-sigma relative deficit is 8.6e-5 at K=36, 3.5e-4 at K=40, 1.4e-3 at
K=44, 5.5e-3 at K=48, 2.2% at K=52, 8.8% at K=56. This is projection evidence (at most 64 bits, 2^34 messages,
34-dimensional sub-cosets, random origins), not a proof for 256-bit digests or complete 40-dimensional cosets.
```

**hcw.cu** (SHA-256 ef34e1357728c086abd7aa90fde9d8964acbd4f1b32b610c4dd1d0e974add032):

```cpp
// hcw.cu - lane-hcoset-wide: wider and larger H_coset pair-count test (a COPY; research/sha3r6/hcoset/hcoset.cu is
// not edited). digest() is hcoset.cu's digest (organizer round function: theta, rho+pi, chi, iota with RC[r]; single
// 135-byte block, zero capacity; message lanes u = start_c ^ XOR_{j: bit j of p} dir_j placed in lanes 0-4 and 10-14,
// lane 16 = 0x86<<56), with the round count and the rotation offsets made compile-time constants.
// Keys (64-bit; a width-K projection is the top K bits of a key):
//   P0..P3 (L0..L3): bit-reversed digest lane 0..3          -> top K bits = the low K bits of that lane
//   P4 (X01): bit-interleave of the low 32 bits of lanes 0 and 1 (lane0 b0, lane1 b0, lane0 b1, lane1 b1, ...)
//   P5 (X23): the same for lanes 2 and 3                    -> top K bits = ceil(K/2) bits of one lane, floor(K/2) of the other
// ladder: pass p = 0..2^b-1 computes every digest of the campaign and keeps, per key, those whose top b bits equal p;
// each kept set is radix-sorted and the exact number of equal-prefix pairs (sum over equal runs of C(len,2)) is counted
// at every width K >= b (pairs at width K never straddle two passes).
// usage: hcw dump   <infile> <n> <ncos> <M> <outfile> [base]      digests of messages base..base+M-1 (4 lanes each)
//        hcw keys   <infile> <n> <ncos> <M> <outfile> [base]      the 6 keys of the same messages
//        hcw ladder <infile> <n> <ncos> <b> <w1,w2,...> [maxpass]  -> one JSON line
// rounds from env HC_ROUNDS (5 or 6 only). infile: ncos*5 u64 starts then n*5 u64 directions (little endian).
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <cmath>
#include <vector>
#include <string>
#include <chrono>
#include <algorithm>
#include <cub/cub.cuh>
typedef unsigned long long u64;
#define NP 6

__constant__ u64 RC[6] = {0x0000000000000001ull, 0x0000000000008082ull, 0x800000000000808Aull,
                          0x8000000080008000ull, 0x000000000000808Bull, 0x0000000080000001ull};
__constant__ u64 DIRS[64 * 5];

__host__ __device__ constexpr int rho(int i) {
    return i == 0 ? 0 : i == 1 ? 1 : i == 2 ? 62 : i == 3 ? 28 : i == 4 ? 27 : i == 5 ? 36 : i == 6 ? 44 : i == 7 ? 6 :
           i == 8 ? 55 : i == 9 ? 20 : i == 10 ? 3 : i == 11 ? 10 : i == 12 ? 43 : i == 13 ? 25 : i == 14 ? 39 :
           i == 15 ? 41 : i == 16 ? 45 : i == 17 ? 15 : i == 18 ? 21 : i == 19 ? 8 : i == 20 ? 18 : i == 21 ? 2 :
           i == 22 ? 61 : i == 23 ? 56 : 14;
}

__device__ __forceinline__ u64 rotl(u64 x, int r) { return r == 0 ? x : (x << r) | (x >> (64 - r)); }

template <int NR>
__device__ __forceinline__ void digest(const u64 *starts, int n, u64 idx, u64 out[4]) {
    u64 c = idx >> n, p = idx & ((1ull << n) - 1), u[5];
#pragma unroll
    for (int k = 0; k < 5; k++) u[k] = starts[c * 5 + k];
    for (int j = 0; j < n; j++)
        if (p >> j & 1)
#pragma unroll
            for (int k = 0; k < 5; k++) u[k] ^= DIRS[j * 5 + k];
    u64 A[25], B[25], C[5], D[5];
#pragma unroll
    for (int k = 0; k < 25; k++) A[k] = 0;
#pragma unroll
    for (int k = 0; k < 5; k++) { A[k] = u[k]; A[10 + k] = u[k]; }
    A[16] = 0x86ull << 56;
#pragma unroll
    for (int r = 0; r < NR; r++) {
#pragma unroll
        for (int x = 0; x < 5; x++) C[x] = A[x] ^ A[x + 5] ^ A[x + 10] ^ A[x + 15] ^ A[x + 20];
#pragma unroll
        for (int x = 0; x < 5; x++) D[x] = C[(x + 4) % 5] ^ rotl(C[(x + 1) % 5], 1);
#pragma unroll
        for (int y = 0; y < 5; y++)
#pragma unroll
            for (int x = 0; x < 5; x++) B[y + 5 * ((2 * x + 3 * y) % 5)] = rotl(A[x + 5 * y] ^ D[x], rho(x + 5 * y));
#pragma unroll
        for (int y = 0; y < 5; y++)
#pragma unroll
            for (int x = 0; x < 5; x++)
                A[x + 5 * y] = B[x + 5 * y] ^ (~B[(x + 1) % 5 + 5 * y] & B[(x + 2) % 5 + 5 * y]);
        A[0] ^= RC[r];
    }
#pragma unroll
    for (int k = 0; k < 4; k++) out[k] = A[k];
}

__device__ __forceinline__ u64 spread(u64 x) {   // bit m of a 32-bit x -> bit 2m
    x = (x | (x << 16)) & 0x0000FFFF0000FFFFull;
    x = (x | (x << 8)) & 0x00FF00FF00FF00FFull;
    x = (x | (x << 4)) & 0x0F0F0F0F0F0F0F0Full;
    x = (x | (x << 2)) & 0x3333333333333333ull;
    x = (x | (x << 1)) & 0x5555555555555555ull;
    return x;
}

__device__ __forceinline__ void mkkeys(const u64 d[4], u64 k[NP]) {
    u64 r0 = __brevll(d[0]), r1 = __brevll(d[1]), r2 = __brevll(d[2]), r3 = __brevll(d[3]);
    k[0] = r0; k[1] = r1; k[2] = r2; k[3] = r3;
    k[4] = (spread(r0 >> 32) << 1) | spread(r1 >> 32);
    k[5] = (spread(r2 >> 32) << 1) | spread(r3 >> 32);
}

template <int NR>
__global__ void kdump(const u64 *starts, int n, u64 base, u64 cnt, int keys, u64 *out) {
    u64 g = blockIdx.x * (u64)blockDim.x + threadIdx.x;
    if (g >= cnt) return;
    u64 d[4];
    digest<NR>(starts, n, base + g, d);
    if (!keys) { for (int k = 0; k < 4; k++) out[4 * g + k] = d[k]; }
    else { u64 kk[NP]; mkkeys(d, kk); for (int j = 0; j < NP; j++) out[NP * g + j] = kk[j]; }
}

// every thread runs the same number of iterations (total is a multiple of the grid size), so full-warp ballots are safe
template <int NR>
__global__ void kpass(const u64 *starts, int n, u64 total, u64 pass, int b, u64 *buf, u64 cap, u64 *cnt) {
    const u64 stride = (u64)gridDim.x * blockDim.x;
    const unsigned lid = threadIdx.x & 31;
    for (u64 idx = blockIdx.x * (u64)blockDim.x + threadIdx.x; idx < total; idx += stride) {
        u64 d[4], k[NP];
        digest<NR>(starts, n, idx, d);
        mkkeys(d, k);
#pragma unroll
        for (int j = 0; j < NP; j++) {
            bool m = b ? ((k[j] >> (64 - b)) == pass) : true;
            unsigned bal = __ballot_sync(0xffffffffu, m);
            if (bal) {
                int leader = __ffs(bal) - 1;
                u64 base = 0;
                if ((int)lid == leader) base = atomicAdd(&cnt[j], (u64)__popc(bal));
                base = __shfl_sync(0xffffffffu, base, leader);
                if (m) {
                    u64 pos = base + __popc(bal & ((1u << lid) - 1u));
                    if (pos < cap) buf[(u64)j * cap + pos] = k[j];
                }
            }
        }
    }
}

// histogram of common-prefix length L = clz(k[i] ^ k[i+d]) (64 = equal), only L >= minw recorded
__global__ void kclz(const u64 *k, u64 N, u64 d, int minw, u64 *hist) {
    __shared__ u64 sh[65];
    for (int i = threadIdx.x; i < 65; i += blockDim.x) sh[i] = 0;
    __syncthreads();
    const u64 stride = (u64)gridDim.x * blockDim.x;
    for (u64 i = blockIdx.x * (u64)blockDim.x + threadIdx.x; i + d < N; i += stride) {
        u64 x = k[i] ^ k[i + d];
        int L = x ? __clzll((long long)x) : 64;
        if (L >= minw) atomicAdd(&sh[L], 1ull);
    }
    __syncthreads();
    for (int i = threadIdx.x; i < 65; i += blockDim.x) if (sh[i]) atomicAdd(&hist[i], sh[i]);
}

#define CK(x) do { cudaError_t e_ = (x); if (e_ != cudaSuccess) { fprintf(stderr, "CUDA %s at %d: %s\n", #x, __LINE__, cudaGetErrorString(e_)); exit(2); } } while (0)

template <int NR>
static int ladder(const u64 *sp, int n, u64 ncos, int b, const std::vector<int> &widths, u64 maxpass, int nr) {
    auto t0 = std::chrono::steady_clock::now();
    u64 total = ncos << n;
    if (total & (total - 1)) { fprintf(stderr, "messages must be a power of two\n"); return 1; }
    if (total < 256) { fprintf(stderr, "too few messages\n"); return 1; }
    int minw = 64;
    for (int w : widths) { if (w < b || w > 64 || w < 1) { fprintf(stderr, "width %d invalid for b=%d\n", w, b); return 1; } minw = std::min(minw, w); }
    u64 mean = total >> b;
    u64 cap = mean + std::max<u64>(4096, (u64)(16.0 * sqrt((double)mean)));
    if (cap >= (1ull << 31)) { fprintf(stderr, "bucket too large; raise b\n"); return 1; }
    u64 *buf, *alt, *cnt, *hist; void *tmp = nullptr; size_t tmpb = 0;
    CK(cudaMalloc(&buf, (size_t)NP * cap * 8)); CK(cudaMalloc(&alt, (size_t)cap * 8));
    CK(cudaMalloc(&cnt, NP * 8)); CK(cudaMalloc(&hist, 65 * 8));
    { cub::DoubleBuffer<u64> db(buf, alt); CK(cub::DeviceRadixSort::SortKeys(nullptr, tmpb, db, (int)cap, 0, 64)); }
    CK(cudaMalloc(&tmp, tmpb));
    std::vector<std::vector<u64>> pairs(NP, std::vector<u64>(widths.size(), 0));
    std::vector<u64> kept(NP, 0);
    bool overflow = false;
    u64 npass = b ? (1ull << b) : 1;
    if (maxpass && maxpass < npass) npass = maxpass;
    int threads = 256;
    u64 blocks = std::min<u64>(total / threads, 1ull << 16);
    for (u64 p = 0; p < npass; p++) {
        CK(cudaMemset(cnt, 0, NP * 8));
        kpass<NR><<<(unsigned)blocks, threads>>>(sp, n, total, p, b, buf, cap, cnt);
        CK(cudaGetLastError());
        u64 hc[NP];
        CK(cudaMemcpy(hc, cnt, NP * 8, cudaMemcpyDeviceToHost));
        for (int j = 0; j < NP; j++) {
            if (hc[j] > cap) overflow = true;
            kept[j] += hc[j];
            u64 N = std::min(hc[j], cap);
            cub::DoubleBuffer<u64> db(buf + (u64)j * cap, alt);
            CK(cub::DeviceRadixSort::SortKeys(tmp, tmpb, db, (int)N, 0, 64 - b));
            const u64 *s = db.Current();
            for (u64 d = 1; d < N; d++) {
                CK(cudaMemset(hist, 0, 65 * 8));
                kclz<<<1024, 256>>>(s, N, d, minw, hist);
                CK(cudaGetLastError());
                u64 hh[65];
                CK(cudaMemcpy(hh, hist, 65 * 8, cudaMemcpyDeviceToHost));
                u64 any = 0;
                for (int L = minw; L <= 64; L++) any += hh[L];
                if (!any) break;
                for (size_t w = 0; w < widths.size(); w++)
                    for (int L = widths[w]; L <= 64; L++) pairs[j][w] += hh[L];
            }
        }
    }
    CK(cudaDeviceSynchronize());
    double secs = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
    const char *pn[NP] = {"L0", "L1", "L2", "L3", "X01", "X23"};
    printf("{\"rounds\": %d, \"n\": %d, \"ncos\": %llu, \"messages\": %llu, \"b\": %d, \"passes\": %llu, \"widths\": [", nr, n, ncos, total, b, npass);
    for (size_t w = 0; w < widths.size(); w++) printf("%s%d", w ? ", " : "", widths[w]);
    printf("], \"kept\": [");
    for (int j = 0; j < NP; j++) printf("%s%llu", j ? ", " : "", kept[j]);
    printf("], \"pairs\": {");
    for (int j = 0; j < NP; j++) {
        printf("%s\"%s\": [", j ? ", " : "", pn[j]);
        for (size_t w = 0; w < widths.size(); w++) printf("%s%llu", w ? ", " : "", pairs[j][w]);
        printf("]");
    }
    printf("}, \"overflow\": %s, \"seconds\": %.1f, \"cuda\": \"%s\"}\n", overflow ? "true" : "false", secs, cudaGetErrorString(cudaGetLastError()));
    return overflow ? 3 : 0;
}

template <int NR>
static int dumpk(const u64 *sp, int n, u64 ncos, u64 M, u64 base, int keys, const char *outf) {
    u64 total = ncos << n;
    if (base + M > total) { fprintf(stderr, "range past the campaign\n"); return 1; }
    int per = keys ? NP : 4;
    u64 *out; CK(cudaMalloc(&out, (size_t)per * M * 8));
    kdump<NR><<<(unsigned)((M + 255) / 256), 256>>>(sp, n, base, M, keys, out);
    CK(cudaGetLastError());
    std::vector<u64> h((size_t)per * M);
    CK(cudaMemcpy(h.data(), out, (size_t)per * M * 8, cudaMemcpyDeviceToHost));
    FILE *g = fopen(outf, "wb");
    if (!g) { fprintf(stderr, "cannot write %s\n", outf); return 1; }
    fwrite(h.data(), 8, h.size(), g); fclose(g);
    printf("{\"dumped\": %llu, \"base\": %llu, \"keys\": %d}\n", M, base, keys);
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 7) { fprintf(stderr, "usage: see header\n"); return 1; }
    const char *mode = argv[1];
    int n = atoi(argv[3]); u64 ncos = strtoull(argv[4], 0, 10);
    if (n < 1 || n > 40 || ncos < 1) { fprintf(stderr, "bad n/ncos\n"); return 1; }
    std::vector<u64> buf(ncos * 5 + n * 5);
    FILE *f = fopen(argv[2], "rb");
    if (!f || fread(buf.data(), 8, buf.size(), f) != buf.size()) { fprintf(stderr, "bad infile\n"); return 1; }
    fclose(f);
    CK(cudaMemcpyToSymbol(DIRS, buf.data() + ncos * 5, n * 5 * 8));
    const char *e = getenv("HC_ROUNDS");
    int nr = e ? atoi(e) : 6;
    if (nr != 5 && nr != 6) { fprintf(stderr, "HC_ROUNDS must be 5 or 6\n"); return 1; }
    u64 *sp; CK(cudaMalloc(&sp, ncos * 5 * 8));
    CK(cudaMemcpy(sp, buf.data(), ncos * 5 * 8, cudaMemcpyHostToDevice));
    if (!strcmp(mode, "dump") || !strcmp(mode, "keys")) {
        u64 M = strtoull(argv[5], 0, 10), base = argc > 7 ? strtoull(argv[7], 0, 10) : 0;
        int keys = mode[0] == 'k';
        return nr == 6 ? dumpk<6>(sp, n, ncos, M, base, keys, argv[6]) : dumpk<5>(sp, n, ncos, M, base, keys, argv[6]);
    }
    if (!strcmp(mode, "ladder")) {
        int b = atoi(argv[5]);
        if (b < 0 || b > 16) { fprintf(stderr, "bad b\n"); return 1; }
        std::vector<int> widths;
        std::string ws(argv[6]); size_t pos = 0;
        while (pos < ws.size()) { size_t q = ws.find(',', pos); if (q == std::string::npos) q = ws.size(); widths.push_back(atoi(ws.substr(pos, q - pos).c_str())); pos = q + 1; }
        u64 maxpass = argc > 7 ? strtoull(argv[7], 0, 10) : 0;
        return nr == 6 ? ladder<6>(sp, n, ncos, b, widths, maxpass, nr) : ladder<5>(sp, n, ncos, b, widths, maxpass, nr);
    }
    fprintf(stderr, "unknown mode\n");
    return 1;
}
```

**hw.py** (SHA-256 62a37307c0067d44da0bcc15db9c5ceb482ccd89f8f29ac0edff00ef2981da0c):

```python
"""Driver for hcw.cu (lane-hcoset-wide). Inputs, validation against the organizer, and the verdict table.
usage: python hw.py gen MODE SEED N NCOS        -> in_<MODE>_<SEED>.bin
       python hw.py validate R                  GPU digests and keys vs organizer sha3_256(rounds=R) (3 x 512 messages)
       python hw.py pipecheck R MODE            GPU ladder counts vs numpy exact counts over 2^20 GPU digests
       python hw.py analyze RESULTS.jsonl       observed vs expected, z, verdict by PREREG_W rule
MODE rord: random 320-bit coset origins, directions = first N ordered W40 vectors (cube_degree.W, the route's order);
     ctrl: random 320-bit coset origins, N random 320-bit directions (rank N)."""
import os, sys, math, json, random, struct, subprocess, pathlib
import numpy as np
sys.path.insert(0, r'D:\~~Projects\~HashSmash\workspace\research\sha3r6\lowdegree')
import cube_degree as cd            # W (40 ordered W40 vectors), rank, kec (organizer SOLCLOUD_12_INPUT_keccak.py)

HERE = pathlib.Path(__file__).resolve().parent
WSL_HERE = '/mnt/d/~~Projects/~HashSmash/workspace/research/lanes/lane-hcoset-wide'
BIN = WSL_HERE + '/hcw'
MASK = (1 << 64) - 1
PROJ = ['L0', 'L1', 'L2', 'L3', 'X01', 'X23']

def gen(mode, seed, n, ncos):
    rng = random.Random(f'W-{mode}-{seed}')
    if mode == 'rord':
        d = cd.W[:n]
    elif mode == 'ctrl':
        while True:
            d = [rng.getrandbits(320) for _ in range(n)]
            if cd.rank(d) == n: break
    else:
        raise SystemExit('mode must be rord or ctrl')
    assert cd.rank(d) == n
    starts = [rng.getrandbits(320) for _ in range(ncos)]
    words = [(s >> (64 * k)) & MASK for s in starts for k in range(5)] + [(v >> (64 * k)) & MASK for v in d for k in range(5)]
    p = HERE / f'in_{mode}_{seed}.bin'
    p.write_bytes(struct.pack(f'<{len(words)}Q', *words))
    return p, starts, d

def msg(starts, d, n, idx):          # identical to research/sha3r6/hcoset/hc.py msg()
    c, p = idx >> n, idx & ((1 << n) - 1); m = starts[c]
    for j in range(n):
        if p >> j & 1: m ^= d[j]
    L = [0] * 25
    for k in range(5): L[k] = (m >> (64 * k)) & MASK; L[10 + k] = L[k]
    L[16] = 0x86 << 56
    return b''.join(l.to_bytes(8, 'little') for l in L[:17])[:135]

def brev(x): return int(f'{x:064b}'[::-1], 2)
def spread(x):
    o = 0
    for m in range(32): o |= ((x >> m) & 1) << (2 * m)
    return o
def pykeys(lanes):                   # independent (pure Python) derivation of the 6 keys from the 4 digest lanes
    r = [brev(v) for v in lanes]
    return r + [(spread(r[0] >> 32) << 1) | spread(r[1] >> 32), (spread(r[2] >> 32) << 1) | spread(r[3] >> 32)]

def gpu(R, *args):
    subprocess.run(['wsl', '-d', 'Ubuntu', '--', 'env', f'HC_ROUNDS={R}', BIN, *map(str, args)], check=True)

def validate(R):
    cases = [('rord', 9001, 34, 1, 0), ('rord', 9001, 34, 1, (1 << 33) + 12345), ('ctrl', 9002, 24, 1024, 1000 * (1 << 24) + 777)]
    M = 512; okd = okk = tot = 0
    for mode, seed, n, ncos, base in cases:
        p, starts, d = gen(mode, seed, n, ncos)
        od, ok_ = HERE / f'v_dump_{seed}.bin', HERE / f'v_keys_{seed}.bin'
        gpu(R, 'dump', f'{WSL_HERE}/{p.name}', n, ncos, M, f'{WSL_HERE}/{od.name}', base)
        gpu(R, 'keys', f'{WSL_HERE}/{p.name}', n, ncos, M, f'{WSL_HERE}/{ok_.name}', base)
        rd, rk = od.read_bytes(), ok_.read_bytes()
        for i in range(M):
            ref = cd.kec.sha3_256(msg(starts, d, n, base + i), rounds=R)
            okd += rd[32 * i:32 * i + 32] == ref
            lanes = [int.from_bytes(ref[8 * k:8 * k + 8], 'little') for k in range(4)]
            gk = list(struct.unpack('<6Q', rk[48 * i:48 * i + 48]))
            okk += gk == pykeys(lanes)
            tot += 1
        od.unlink(); ok_.unlink(); p.unlink()
    print(f'validate rounds={R}: digests {okd}/{tot} equal organizer sha3_256(rounds={R}); keys {okk}/{tot} equal Python keys of the organizer digests')

def np_brev(x):
    LUT = np.array([int(f'{i:08b}'[::-1], 2) for i in range(256)], dtype=np.uint8)
    return np.ascontiguousarray(LUT[x.view(np.uint8).reshape(-1, 8)][:, ::-1]).view(np.uint64).reshape(-1)
def np_spread(x):
    x = x.astype(np.uint64)
    for s, m in ((16, 0x0000FFFF0000FFFF), (8, 0x00FF00FF00FF00FF), (4, 0x0F0F0F0F0F0F0F0F), (2, 0x3333333333333333), (1, 0x5555555555555555)):
        x = (x | (x << np.uint64(s))) & np.uint64(m)
    return x

def pipecheck(R, mode):
    n, ncos, b = 16, 16, 3
    widths = [12, 16, 20, 24, 28, 32, 40, 64]
    p, starts, d = gen(mode, 9003, n, ncos)
    M = ncos << n; od = HERE / 'pc_dump.bin'
    gpu(R, 'dump', f'{WSL_HERE}/{p.name}', n, ncos, M, f'{WSL_HERE}/{od.name}', 0)
    D = np.frombuffer(od.read_bytes(), dtype=np.uint64).reshape(-1, 4)
    r = [np_brev(D[:, k].copy()) for k in range(4)]
    K = r + [(np_spread(r[0] >> np.uint64(32)) << np.uint64(1)) | np_spread(r[1] >> np.uint64(32)),
             (np_spread(r[2] >> np.uint64(32)) << np.uint64(1)) | np_spread(r[3] >> np.uint64(32))]
    ref = {}
    for j, nm in enumerate(PROJ):
        ref[nm] = []
        for w in widths:
            _, c = np.unique(K[j] >> np.uint64(64 - w), return_counts=True)
            ref[nm].append(int((c.astype(np.int64) * (c.astype(np.int64) - 1) // 2).sum()))
    out = subprocess.run(['wsl', '-d', 'Ubuntu', '--', 'env', f'HC_ROUNDS={R}', BIN, 'ladder', f'{WSL_HERE}/{p.name}', str(n), str(ncos), str(b),
                          ','.join(map(str, widths))], check=True, capture_output=True, text=True).stdout
    g = json.loads(out.strip().splitlines()[-1])
    same = all(g['pairs'][nm] == ref[nm] for nm in PROJ) and g['kept'] == [M] * 6 and not g['overflow']
    print(f'pipecheck rounds={R} {mode}: GPU ladder (b={b}, {g["passes"]} passes) vs numpy on {M} GPU digests: {"EQUAL" if same else "DIFFERENT"}')
    print('  numpy', json.dumps(ref)); print('  gpu  ', json.dumps(g['pairs']))
    od.unlink(); p.unlink()

def expected(N, K): return N * (N - 1) / 2 / 2.0 ** K

def pois_lower(obs, lam):            # P(X <= obs), X ~ Poisson(lam), for small lam
    s, t = 0.0, math.exp(-lam)
    for k in range(obs + 1):
        s += t; t *= lam / (k + 1)
    return min(1.0, s)

def analyze(path):
    rows = [json.loads(l) for l in open(path) if l.strip().startswith('{')]
    TH = 3.167e-5                    # one-sided 4-sigma normal tail
    worst, fail, allz = None, [], []
    for row in rows:
        tag, kind = row.get('tag', '?'), row.get('kind', '?')
        N = row['messages']
        print(f"## {tag} ({kind}) rounds={row['rounds']} n={row['n']} ncos={row['ncos']} N=2^{int(math.log2(N))} b={row['b']} {row['seconds']} s  kept_ok={row['kept'] == [N] * 6}  overflow={row['overflow']}")
        print('| width | expected | ' + ' | '.join(PROJ) + ' |')
        print('|---|---|' + '---|' * len(PROJ))
        for wi, K in enumerate(row['widths']):
            E = expected(N, K); sd = math.sqrt(E * (1 - 2.0 ** -K)); cells = []
            for nm in PROJ:
                o = row['pairs'][nm][wi]; z = (o - E) / sd
                if E >= 1000:
                    pl = 0.5 * math.erfc(-z / math.sqrt(2))
                else:
                    pl = pois_lower(o, E)
                cells.append(f'{o} ({z:+.2f})')
                allz.append((z, tag, nm, K, E, o))
                if kind != 'ctrl' and pl < TH: fail.append((tag, nm, K, o, E, z, pl))
            print(f'| {K} | {E:.2f} | ' + ' | '.join(cells) + ' |')
        print()
    lo = min(allz); hi = max(allz)
    print(f'counts: {len(allz)}; lowest z {lo[0]:+.2f} ({lo[1]} {lo[2]} K={lo[3]}); highest z {hi[0]:+.2f} ({hi[1]} {hi[2]} K={hi[3]})')
    fz = [a for a in allz if any(r.get('tag') == a[1] and r.get('kind') != 'ctrl' for r in rows)]
    flo = min(fz); fhi = max(fz)
    print(f'field counts: {len(fz)}; lowest z {flo[0]:+.2f} ({flo[1]} {flo[2]} K={flo[3]}); highest z {fhi[0]:+.2f} ({fhi[1]} {fhi[2]} K={fhi[3]}); |z|>4: {sum(abs(a[0]) > 4 for a in allz)}')
    invalid = [r.get('tag') for r in rows if r['kept'] != [r['messages']] * 6 or r['overflow'] or r['cuda'] != 'no error']
    print(f'runs: {len(rows)}; invalid runs: {invalid or "none"}')
    # EXPLORATORY (not in the preregistered rule): per width, Stouffer z over L0..L3 (lanes are uncorrelated under the
    # uniform model) of the field runs, and of the control runs, to show any width trend.
    print('exploratory Stouffer z over L0..L3 per width (field runs | control runs):')
    for wi, K in enumerate(rows[0]['widths']):
        out = []
        for want_ctrl in (False, True):
            zz = [ (r['pairs'][nm][wi] - expected(r['messages'], K)) / math.sqrt(expected(r['messages'], K)) for r in rows
                   if (r.get('kind') == 'ctrl') == want_ctrl for nm in PROJ[:4]]
            out.append(f'{sum(zz) / math.sqrt(len(zz)):+.2f} (m={len(zz)})' if zz else '-')
        print(f'  K={K}: {out[0]} | {out[1]}')
    v = 'FAIL ' + json.dumps(fail) if fail else 'PASS'
    if invalid: v += ' (INCOMPLETE: invalid runs ' + json.dumps(invalid) + ', reported, not replaced)'
    print('VERDICT: ' + v)

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'gen':
        print(gen(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))[0])
    elif cmd == 'validate':
        validate(int(sys.argv[2]))
    elif cmd == 'pipecheck':
        pipecheck(int(sys.argv[2]), sys.argv[3])
    elif cmd == 'analyze':
        analyze(sys.argv[2])
```

**run_w.sh** (SHA-256 c84135cab4b43c2be2be67573e8609b5eb24b63eab7def1faa20b7e432691d0e), its log **w.log** (SHA-256
62b3007bdbf63fd1fe129bbe1dbcd9372ae3ca98c47dab1b82346f13d047b3c6) and **cap_w6.sh** (SHA-256 14fb4bc9746c89ca5de843bb691dbb051a73e5bb822f86f60fa86a2980d66b5d),
which stopped W6 at 20 minutes of run time (rc=143):

```sh
#!/bin/bash
# Batch W per PREREG_W.txt: six ladder runs, sequential, one GPU job.
D="/mnt/d/~~Projects/~HashSmash/workspace/research/lanes/lane-hcoset-wide"
B="$D/hcw"; O="$D/w_results.jsonl"; L="$D/w.log"
WID="36,40,44,48,52,56,60,64"
run() {  # tag kind rounds seed n ncos
  echo "$(date '+%F %T') start $1" >> "$L"
  HC_ROUNDS=$3 "$B" ladder "$D/in_$2_$4.bin" $5 $6 6 "$WID" 2>> "$L" | sed "s/^{/{\"tag\": \"$1\", \"kind\": \"$2\", /" >> "$O"
  echo "$(date '+%F %T') end $1 rc=${PIPESTATUS[0]}" >> "$L"
}
run W1 rord 6 5101 34 1
run W2 rord 6 5102 24 1024
run W3 ctrl 6 5103 34 1
run W4 rord 5 5104 34 1
run W5 rord 5 5105 24 1024
run W6 ctrl 5 5106 34 1
echo "$(date '+%F %T') done" >> "$L"
```

```
2026-10-10 02:27:19 start W1
2026-10-10 02:31:26 end W1 rc=0
2026-10-10 02:31:26 start W2
2026-10-10 02:38:35 end W2 rc=0
2026-10-10 02:38:35 start W3
2026-10-10 02:42:29 end W3 rc=0
2026-10-10 02:42:29 start W4
2026-10-10 02:46:43 end W4 rc=0
2026-10-10 02:46:43 start W5
2026-10-10 02:52:09 end W5 rc=0
2026-10-10 02:52:09 start W6
2026-10-10 03:12:11 end W6 rc=143
2026-10-10 03:12:11 done
```

```sh
#!/bin/bash
# stop my own W6 hcw process (pid given) once it reaches the 20-minute run cap; touches no other process
P=$1
E=$(ps -o etimes= -p "$P" | tr -d ' ')
echo "pid $P elapsed ${E:-gone} s: $(ps -o args= -p "$P")"
while [ -n "$E" ] && [ "$E" -lt 1200 ]; do sleep 2; E=$(ps -o etimes= -p "$P" | tr -d ' '); done
if [ -n "$E" ]; then kill "$P"; echo "stopped pid $P at $E s (20-minute run cap)"; else echo "pid $P finished before the cap"; fi
date '+%F %T'
```

**w_results.jsonl** (SHA-256 270f2042b09f6c58d2d4c9610dc08eb02235dc8f6fa32316291cd86b50454d79), the raw result lines,
one per completed run in run order:

```
{"tag": "W1", "kind": "rord", "rounds": 6, "n": 34, "ncos": 1, "messages": 17179869184, "b": 6, "passes": 64, "widths": [36, 40, 44, 48, 52, 56, 60, 64], "kept": [17179869184, 17179869184, 17179869184, 17179869184, 17179869184, 17179869184], "pairs": {"L0": [2147434141, 134208200, 8387828, 523286, 32513, 1969, 110, 7], "L1": [2147535368, 134227743, 8384488, 524498, 32909, 1937, 131, 5], "L2": [2147495205, 134220252, 8389761, 524389, 32941, 1974, 141, 8], "L3": [2147463719, 134227938, 8391034, 525849, 32880, 2036, 137, 6], "X01": [2147561746, 134240843, 8389303, 525102, 32929, 1991, 138, 7], "X23": [2147437452, 134216325, 8391241, 523784, 32786, 2017, 122, 12]}, "overflow": false, "seconds": 246.6, "cuda": "no error"}
{"tag": "W2", "kind": "rord", "rounds": 6, "n": 24, "ncos": 1024, "messages": 17179869184, "b": 6, "passes": 64, "widths": [36, 40, 44, 48, 52, 56, 60, 64], "kept": [17179869184, 17179869184, 17179869184, 17179869184, 17179869184, 17179869184], "pairs": {"L0": [2147391126, 134219152, 8388132, 524335, 32757, 2027, 120, 5], "L1": [2147519764, 134236548, 8391176, 524695, 32747, 2115, 127, 6], "L2": [2147400372, 134206586, 8387739, 524340, 32629, 2052, 128, 7], "L3": [2147533470, 134234197, 8391670, 523136, 32866, 2067, 139, 14], "X01": [2147511997, 134222584, 8391874, 525322, 33026, 2037, 128, 3], "X23": [2147338230, 134207618, 8389594, 523780, 33084, 2012, 129, 14]}, "overflow": false, "seconds": 429.1, "cuda": "no error"}
{"tag": "W3", "kind": "ctrl", "rounds": 6, "n": 34, "ncos": 1, "messages": 17179869184, "b": 6, "passes": 64, "widths": [36, 40, 44, 48, 52, 56, 60, 64], "kept": [17179869184, 17179869184, 17179869184, 17179869184, 17179869184, 17179869184], "pairs": {"L0": [2147450433, 134215578, 8387195, 524255, 33139, 2095, 133, 7], "L1": [2147539278, 134216888, 8390532, 525375, 32548, 2066, 130, 10], "L2": [2147473446, 134230335, 8395803, 524576, 32680, 2047, 111, 9], "L3": [2147419567, 134212722, 8387285, 525100, 32433, 2062, 138, 11], "X01": [2147434882, 134219744, 8389355, 525588, 32910, 2055, 119, 6], "X23": [2147458088, 134209328, 8387741, 523796, 32443, 1929, 107, 5]}, "overflow": false, "seconds": 234.0, "cuda": "no error"}
{"tag": "W4", "kind": "rord", "rounds": 5, "n": 34, "ncos": 1, "messages": 17179869184, "b": 6, "passes": 64, "widths": [36, 40, 44, 48, 52, 56, 60, 64], "kept": [17179869184, 17179869184, 17179869184, 17179869184, 17179869184, 17179869184], "pairs": {"L0": [2147509921, 134218375, 8391319, 524512, 32672, 1999, 127, 10], "L1": [2147478047, 134228182, 8392201, 524727, 32675, 2035, 128, 11], "L2": [2147484523, 134213465, 8392227, 524137, 32769, 2040, 135, 5], "L3": [2147421184, 134217090, 8393502, 524849, 32774, 2056, 122, 4], "X01": [2147423629, 134219174, 8389791, 523909, 33178, 2060, 139, 10], "X23": [2147420853, 134209010, 8383468, 524025, 32696, 2062, 125, 5]}, "overflow": false, "seconds": 253.2, "cuda": "no error"}
{"tag": "W5", "kind": "rord", "rounds": 5, "n": 24, "ncos": 1024, "messages": 17179869184, "b": 6, "passes": 64, "widths": [36, 40, 44, 48, 52, 56, 60, 64], "kept": [17179869184, 17179869184, 17179869184, 17179869184, 17179869184, 17179869184], "pairs": {"L0": [2147455537, 134203112, 8389161, 525678, 32644, 2068, 143, 14], "L1": [2147472522, 134209194, 8388726, 525060, 32796, 2059, 122, 12], "L2": [2147463007, 134215142, 8389302, 524310, 32658, 2023, 141, 13], "L3": [2147515738, 134206629, 8390098, 524860, 32929, 2011, 125, 8], "X01": [2147542449, 134227319, 8388920, 523836, 32594, 2063, 150, 10], "X23": [2147490038, 134230469, 8391239, 524649, 32779, 2050, 138, 11]}, "overflow": false, "seconds": 325.3, "cuda": "no error"}
```

**w_analysis.txt** (output of hw.py analyze w_results.jsonl): the observed count and its z for every run, projection
and width. The file's SHA-256 is 2f102e94f4dfa00a2accc8d005621f1e33c5d92fac6b54e86dec40866ec8fdff; it begins with a
UTF-8 byte-order mark and ends its lines in CR LF, so it is shown without the mark and with LF line ends (SHA-256 of
the text below: 16ef971004d5d0aad25f07d24f339269b58f30c383e605ae9d65ad55384d83e9). The Stouffer lines at the end are exploratory and outside the preregistered rule.

```
## W1 (rord) rounds=6 n=34 ncos=1 N=2^34 b=6 246.6 s  kept_ok=True  overflow=False
| width | expected | L0 | L1 | L2 | L3 | X01 | X23 |
|---|---|---|---|---|---|---|---|
| 36 | 2147483647.88 | 2147434141 (-1.07) | 2147535368 (+1.12) | 2147495205 (+0.25) | 2147463719 (-0.43) | 2147561746 (+1.69) | 2147437452 (-1.00) |
| 40 | 134217727.99 | 134208200 (-0.82) | 134227743 (+0.86) | 134220252 (+0.22) | 134227938 (+0.88) | 134240843 (+2.00) | 134216325 (-0.12) |
| 44 | 8388608.00 | 8387828 (-0.27) | 8384488 (-1.42) | 8389761 (+0.40) | 8391034 (+0.84) | 8389303 (+0.24) | 8391241 (+0.91) |
| 48 | 524288.00 | 523286 (-1.38) | 524498 (+0.29) | 524389 (+0.14) | 525849 (+2.16) | 525102 (+1.12) | 523784 (-0.70) |
| 52 | 32768.00 | 32513 (-1.41) | 32909 (+0.78) | 32941 (+0.96) | 32880 (+0.62) | 32929 (+0.89) | 32786 (+0.10) |
| 56 | 2048.00 | 1969 (-1.75) | 1937 (-2.45) | 1974 (-1.64) | 2036 (-0.27) | 1991 (-1.26) | 2017 (-0.69) |
| 60 | 128.00 | 110 (-1.59) | 131 (+0.27) | 141 (+1.15) | 137 (+0.80) | 138 (+0.88) | 122 (-0.53) |
| 64 | 8.00 | 7 (-0.35) | 5 (-1.06) | 8 (+0.00) | 6 (-0.71) | 7 (-0.35) | 12 (+1.41) |

## W2 (rord) rounds=6 n=24 ncos=1024 N=2^34 b=6 429.1 s  kept_ok=True  overflow=False
| width | expected | L0 | L1 | L2 | L3 | X01 | X23 |
|---|---|---|---|---|---|---|---|
| 36 | 2147483647.88 | 2147391126 (-2.00) | 2147519764 (+0.78) | 2147400372 (-1.80) | 2147533470 (+1.08) | 2147511997 (+0.61) | 2147338230 (-3.14) |
| 40 | 134217727.99 | 134219152 (+0.12) | 134236548 (+1.62) | 134206586 (-0.96) | 134234197 (+1.42) | 134222584 (+0.42) | 134207618 (-0.87) |
| 44 | 8388608.00 | 8388132 (-0.16) | 8391176 (+0.89) | 8387739 (-0.30) | 8391670 (+1.06) | 8391874 (+1.13) | 8389594 (+0.34) |
| 48 | 524288.00 | 524335 (+0.06) | 524695 (+0.56) | 524340 (+0.07) | 523136 (-1.59) | 525322 (+1.43) | 523780 (-0.70) |
| 52 | 32768.00 | 32757 (-0.06) | 32747 (-0.12) | 32629 (-0.77) | 32866 (+0.54) | 33026 (+1.43) | 33084 (+1.75) |
| 56 | 2048.00 | 2027 (-0.46) | 2115 (+1.48) | 2052 (+0.09) | 2067 (+0.42) | 2037 (-0.24) | 2012 (-0.80) |
| 60 | 128.00 | 120 (-0.71) | 127 (-0.09) | 128 (+0.00) | 139 (+0.97) | 128 (+0.00) | 129 (+0.09) |
| 64 | 8.00 | 5 (-1.06) | 6 (-0.71) | 7 (-0.35) | 14 (+2.12) | 3 (-1.77) | 14 (+2.12) |

## W3 (ctrl) rounds=6 n=34 ncos=1 N=2^34 b=6 234.0 s  kept_ok=True  overflow=False
| width | expected | L0 | L1 | L2 | L3 | X01 | X23 |
|---|---|---|---|---|---|---|---|
| 36 | 2147483647.88 | 2147450433 (-0.72) | 2147539278 (+1.20) | 2147473446 (-0.22) | 2147419567 (-1.38) | 2147434882 (-1.05) | 2147458088 (-0.55) |
| 40 | 134217727.99 | 134215578 (-0.19) | 134216888 (-0.07) | 134230335 (+1.09) | 134212722 (-0.43) | 134219744 (+0.17) | 134209328 (-0.73) |
| 44 | 8388608.00 | 8387195 (-0.49) | 8390532 (+0.66) | 8395803 (+2.48) | 8387285 (-0.46) | 8389355 (+0.26) | 8387741 (-0.30) |
| 48 | 524288.00 | 524255 (-0.05) | 525375 (+1.50) | 524576 (+0.40) | 525100 (+1.12) | 525588 (+1.80) | 523796 (-0.68) |
| 52 | 32768.00 | 33139 (+2.05) | 32548 (-1.22) | 32680 (-0.49) | 32433 (-1.85) | 32910 (+0.78) | 32443 (-1.80) |
| 56 | 2048.00 | 2095 (+1.04) | 2066 (+0.40) | 2047 (-0.02) | 2062 (+0.31) | 2055 (+0.15) | 1929 (-2.63) |
| 60 | 128.00 | 133 (+0.44) | 130 (+0.18) | 111 (-1.50) | 138 (+0.88) | 119 (-0.80) | 107 (-1.86) |
| 64 | 8.00 | 7 (-0.35) | 10 (+0.71) | 9 (+0.35) | 11 (+1.06) | 6 (-0.71) | 5 (-1.06) |

## W4 (rord) rounds=5 n=34 ncos=1 N=2^34 b=6 253.2 s  kept_ok=True  overflow=False
| width | expected | L0 | L1 | L2 | L3 | X01 | X23 |
|---|---|---|---|---|---|---|---|
| 36 | 2147483647.88 | 2147509921 (+0.57) | 2147478047 (-0.12) | 2147484523 (+0.02) | 2147421184 (-1.35) | 2147423629 (-1.30) | 2147420853 (-1.36) |
| 40 | 134217727.99 | 134218375 (+0.06) | 134228182 (+0.90) | 134213465 (-0.37) | 134217090 (-0.06) | 134219174 (+0.12) | 134209010 (-0.75) |
| 44 | 8388608.00 | 8391319 (+0.94) | 8392201 (+1.24) | 8392227 (+1.25) | 8393502 (+1.69) | 8389791 (+0.41) | 8383468 (-1.77) |
| 48 | 524288.00 | 524512 (+0.31) | 524727 (+0.61) | 524137 (-0.21) | 524849 (+0.77) | 523909 (-0.52) | 524025 (-0.36) |
| 52 | 32768.00 | 32672 (-0.53) | 32675 (-0.51) | 32769 (+0.01) | 32774 (+0.03) | 33178 (+2.26) | 32696 (-0.40) |
| 56 | 2048.00 | 1999 (-1.08) | 2035 (-0.29) | 2040 (-0.18) | 2056 (+0.18) | 2060 (+0.27) | 2062 (+0.31) |
| 60 | 128.00 | 127 (-0.09) | 128 (+0.00) | 135 (+0.62) | 122 (-0.53) | 139 (+0.97) | 125 (-0.27) |
| 64 | 8.00 | 10 (+0.71) | 11 (+1.06) | 5 (-1.06) | 4 (-1.41) | 10 (+0.71) | 5 (-1.06) |

## W5 (rord) rounds=5 n=24 ncos=1024 N=2^34 b=6 325.3 s  kept_ok=True  overflow=False
| width | expected | L0 | L1 | L2 | L3 | X01 | X23 |
|---|---|---|---|---|---|---|---|
| 36 | 2147483647.88 | 2147455537 (-0.61) | 2147472522 (-0.24) | 2147463007 (-0.45) | 2147515738 (+0.69) | 2147542449 (+1.27) | 2147490038 (+0.14) |
| 40 | 134217727.99 | 134203112 (-1.26) | 134209194 (-0.74) | 134215142 (-0.22) | 134206629 (-0.96) | 134227319 (+0.83) | 134230469 (+1.10) |
| 44 | 8388608.00 | 8389161 (+0.19) | 8388726 (+0.04) | 8389302 (+0.24) | 8390098 (+0.51) | 8388920 (+0.11) | 8391239 (+0.91) |
| 48 | 524288.00 | 525678 (+1.92) | 525060 (+1.07) | 524310 (+0.03) | 524860 (+0.79) | 523836 (-0.62) | 524649 (+0.50) |
| 52 | 32768.00 | 32644 (-0.69) | 32796 (+0.15) | 32658 (-0.61) | 32929 (+0.89) | 32594 (-0.96) | 32779 (+0.06) |
| 56 | 2048.00 | 2068 (+0.44) | 2059 (+0.24) | 2023 (-0.55) | 2011 (-0.82) | 2063 (+0.33) | 2050 (+0.04) |
| 60 | 128.00 | 143 (+1.33) | 122 (-0.53) | 141 (+1.15) | 125 (-0.27) | 150 (+1.94) | 138 (+0.88) |
| 64 | 8.00 | 14 (+2.12) | 12 (+1.41) | 13 (+1.77) | 8 (+0.00) | 10 (+0.71) | 11 (+1.06) |

counts: 240; lowest z -3.14 (W2 X23 K=36); highest z +2.48 (W3 L2 K=44)
field counts: 192; lowest z -3.14 (W2 X23 K=36); highest z +2.26 (W4 X01 K=52); |z|>4: 0
runs: 5; invalid runs: none
exploratory Stouffer z over L0..L3 per width (field runs | control runs):
  K=36: -0.89 (m=16) | -0.56 (m=4)
  K=40: +0.18 (m=16) | +0.20 (m=4)
  K=44: +1.78 (m=16) | +1.10 (m=4)
  K=48: +1.40 (m=16) | +1.49 (m=4)
  K=52: -0.18 (m=16) | -0.75 (m=4)
  K=56: -1.66 (m=16) | +0.86 (m=4)
  K=60: +0.62 (m=16) | +0.00 (m=4)
  K=64: +0.62 (m=16) | +0.88 (m=4)
VERDICT: PASS
```

### A.6 GPU digest checks on the run inputs

gpu_validate_s6g.py (below) re-runs the checks of A.4 on the input files of the count runs, after all count runs:
for each file the GPU binary dumps 512 digests (hcw also its six projection keys) at the stated message indices, and
each is compared with the organizer reference verifier/keccak.py sha3_256(message, rounds=R) of the same message.
File times show that the hcoset binary checked here was built on 2026-10-10 at 01:55:12, 8 seconds after the last
change of the hcoset.cu of A.2 and before batch R5 (01:55:56), after batches 1 to 3 had run (2026-10-09 23:40 to
2026-10-10 00:37); the build that ran batches 1 to 3 was not kept, and its checks are those of A.4. The hcw binary
(built at 02:24:57) is the one that ran batch W (02:27 to 03:12). The printout, verbatim:

```
GPU digest re-validation, 2026-10-10 06:02 (local clock); organizer reference verifier/keccak.py sha256 95ce77dff0476301c05057e01296f3e3507c4926423257540cfc3e5fd36ee0ae
hcoset binary sha256 911096f0a08566ff21513f445506a9c175fe9fbc544f84c46d79f5fabd75c3b3, hcoset.cu sha256 28c40823a37afd1d22fb487b5ab77622c2036e5bc6763a330d83d1a9f66069f8
hcw binary sha256 514d71d742d92afcfce353bc9330cc50cf2430c87d5ddd03aee38a5d187d77bb, hcw.cu sha256 ef34e1357728c086abd7aa90fde9d8964acbd4f1b32b610c4dd1d0e974add032
batch 1  hcoset rounds=6 in_field_1001.bin (n=20, 1024 cosets, sha256 ae25659fe1787dd6): messages 0..511: 512/512 GPU digests equal organizer sha3_256(rounds=6)
batch 1  hcoset rounds=6 in_ctrl_1001.bin (n=20, 1024 cosets, sha256 d4ce2391e9a900de): messages 0..511: 512/512 GPU digests equal organizer sha3_256(rounds=6)
batch 1  hcoset rounds=6 in_field_1002.bin (n=24, 64 cosets, sha256 02b3e135c0b50faf): messages 0..511: 512/512 GPU digests equal organizer sha3_256(rounds=6)
batch 1  hcoset rounds=6 in_ctrl_1002.bin (n=24, 64 cosets, sha256 48709b11f389be48): messages 0..511: 512/512 GPU digests equal organizer sha3_256(rounds=6)
batch 2  hcoset rounds=6 in_field_2001.bin (n=20, 1024 cosets, sha256 469aeb54fcb3097c): messages 0..511: 512/512 GPU digests equal organizer sha3_256(rounds=6)
batch 2  hcoset rounds=6 in_ctrl_2001.bin (n=20, 1024 cosets, sha256 4d257597424bc506): messages 0..511: 512/512 GPU digests equal organizer sha3_256(rounds=6)
batch 2  hcoset rounds=6 in_field_2002.bin (n=28, 4 cosets, sha256 8d624daa72be49a1): messages 0..511: 512/512 GPU digests equal organizer sha3_256(rounds=6)
batch 2  hcoset rounds=6 in_ctrl_2002.bin (n=28, 4 cosets, sha256 fd191b6dca98502f): messages 0..511: 512/512 GPU digests equal organizer sha3_256(rounds=6)
batch 3  hcoset rounds=6 in_det_3001.bin (n=20, 1024 cosets, sha256 a80bc01f218d0615): messages 0..511: 512/512 GPU digests equal organizer sha3_256(rounds=6)
batch 3  hcoset rounds=6 in_det_3002.bin (n=24, 64 cosets, sha256 fb0b86df4f169ba9): messages 0..511: 512/512 GPU digests equal organizer sha3_256(rounds=6)
batch R5 hcoset rounds=5 in_det_4001.bin (n=20, 1024 cosets, sha256 a80bc01f218d0615): messages 0..511: 512/512 GPU digests equal organizer sha3_256(rounds=5)
batch R5 hcoset rounds=5 in_det_4002.bin (n=24, 64 cosets, sha256 fb0b86df4f169ba9): messages 0..511: 512/512 GPU digests equal organizer sha3_256(rounds=5)
batch R5 hcoset rounds=5 in_field_4003.bin (n=20, 1024 cosets, sha256 873ecab65c578fef): messages 0..511: 512/512 GPU digests equal organizer sha3_256(rounds=5)
batch R5 hcoset rounds=5 in_ctrl_4003.bin (n=20, 1024 cosets, sha256 8917acd85ef6d2eb): messages 0..511: 512/512 GPU digests equal organizer sha3_256(rounds=5)
batch W  hcw rounds=6 W1 in_rord_5101.bin (n=34, 1 cosets, sha256 461e3cd2f1813046): messages 0..511: 512/512 GPU digests equal organizer sha3_256(rounds=6); 512/512 GPU keys equal the six projections of the organizer digests
batch W  hcw rounds=6 W1 in_rord_5101.bin (n=34, 1 cosets, sha256 461e3cd2f1813046): messages 8589946937..8589947448: 512/512 GPU digests equal organizer sha3_256(rounds=6); 512/512 GPU keys equal the six projections of the organizer digests
batch W  hcw rounds=6 W2 in_rord_5102.bin (n=24, 1024 cosets, sha256 c516ca6aec7a9e47): messages 16777216777..16777217288: 512/512 GPU digests equal organizer sha3_256(rounds=6); 512/512 GPU keys equal the six projections of the organizer digests
batch W  hcw rounds=6 W3 in_ctrl_5103.bin (n=34, 1 cosets, sha256 b3614685b0fc3638): messages 0..511: 512/512 GPU digests equal organizer sha3_256(rounds=6); 512/512 GPU keys equal the six projections of the organizer digests
batch W  hcw rounds=5 W4 in_rord_5104.bin (n=34, 1 cosets, sha256 56366cd3bd2973f1): messages 0..511: 512/512 GPU digests equal organizer sha3_256(rounds=5); 512/512 GPU keys equal the six projections of the organizer digests
batch W  hcw rounds=5 W4 in_rord_5104.bin (n=34, 1 cosets, sha256 56366cd3bd2973f1): messages 8589946937..8589947448: 512/512 GPU digests equal organizer sha3_256(rounds=5); 512/512 GPU keys equal the six projections of the organizer digests
batch W  hcw rounds=5 W5 in_rord_5105.bin (n=24, 1024 cosets, sha256 dc30ac34bec88ab9): messages 16777216777..16777217288: 512/512 GPU digests equal organizer sha3_256(rounds=5); 512/512 GPU keys equal the six projections of the organizer digests
total: 10752/10752 digests equal
```

**gpu_validate_s6g.py** (SHA-256 f8713e1771b1777a7e8cd435b63730ed26b02370345389d1a612a68d33783512):

```python
"""Dev tool (not shipped): re-run the GPU-versus-organizer digest checks of the H_coset batches on the exact input files
of the count runs, and print the lines that proof.md Appendix A.6 keeps verbatim. Read-only on the inputs, the GPU
binaries and the live organizer checkout; the GPU dumps go to a fresh temporary directory that is removed after.
For each input file: the GPU binary dumps 512 digests (hcw: also the six projection keys) at the given message index
base, and each is compared with the organizer reference verifier/keccak.py sha3_256(message, rounds=R) of the same
message, built from the file's origins and directions exactly as the drivers hc.py and hw.py build it.
Run in WSL: python3 -B gpu_validate_s6g.py"""
import sys, os, struct, hashlib, subprocess, tempfile, shutil, datetime, importlib.util

sys.dont_write_bytecode = True
KEC = '/root/hashsmash/yukon/hashsmash_S6/verifier/keccak.py'
spec = importlib.util.spec_from_file_location('okec', KEC)
okec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(okec)
HC_DIR = '/mnt/d/~~Projects/~HashSmash/workspace/research/sha3r6/hcoset'
W_DIR = '/mnt/d/~~Projects/~HashSmash/workspace/research/lanes/lane-hcoset-wide'
HC_BIN, W_BIN = '/root/hcoset_bin/hcoset', W_DIR + '/hcw'
MASK, M = (1 << 64) - 1, 512


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def load(path, n, ncos):  # ncos * 5 u64 origins, then n * 5 u64 directions, little-endian
    raw = open(path, 'rb').read()
    assert len(raw) == 8 * 5 * (ncos + n), path
    w = struct.unpack(f'<{5 * (ncos + n)}Q', raw)
    v = [sum(w[5 * k + j] << 64 * j for j in range(5)) for k in range(ncos + n)]
    return v[:ncos], v[ncos:]


def msg(starts, d, n, idx):   # as hc.py / hw.py msg(): coset idx >> n, point = XOR of directions at the set bits
    c, p = idx >> n, idx & ((1 << n) - 1)
    m = starts[c]
    for j in range(n):
        if p >> j & 1:
            m ^= d[j]
    L = [0] * 25
    for k in range(5):
        L[k] = (m >> (64 * k)) & MASK
        L[10 + k] = L[k]
    L[16] = 0x86 << 56
    return b''.join(x.to_bytes(8, 'little') for x in L[:17])[:135]


def brev(x):
    return int(f'{x:064b}'[::-1], 2)


def spread(x):
    o = 0
    for m in range(32):
        o |= ((x >> m) & 1) << (2 * m)
    return o


def pykeys(lanes):        # as hw.py pykeys(): L0..L3 bit-reversed lanes, X01 and X23 interleaved halves
    r = [brev(v) for v in lanes]
    return r + [(spread(r[0] >> 32) << 1) | spread(r[1] >> 32), (spread(r[2] >> 32) << 1) | spread(r[3] >> 32)]


def gpu(binary, rounds, *args):
    subprocess.run(['env', f'HC_ROUNDS={rounds}', binary, *map(str, args)], check=True, stdout=subprocess.DEVNULL)


tmp = tempfile.mkdtemp(prefix='s6g-gpuval-')
try:
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    print(f'GPU digest re-validation, {now} (local clock); organizer reference verifier/keccak.py sha256 {sha(KEC)}')
    print(f'hcoset binary sha256 {sha(HC_BIN)}, hcoset.cu sha256 {sha(HC_DIR + "/hcoset.cu")}')
    print(f'hcw binary sha256 {sha(W_BIN)}, hcw.cu sha256 {sha(W_DIR + "/hcw.cu")}')
    tot_ok = tot = 0
    for tag, rounds, f, n, ncos in (('batch 1', 6, 'in_field_1001.bin', 20, 1024), ('batch 1', 6, 'in_ctrl_1001.bin', 20, 1024),
                                    ('batch 1', 6, 'in_field_1002.bin', 24, 64), ('batch 1', 6, 'in_ctrl_1002.bin', 24, 64),
                                    ('batch 2', 6, 'in_field_2001.bin', 20, 1024), ('batch 2', 6, 'in_ctrl_2001.bin', 20, 1024),
                                    ('batch 2', 6, 'in_field_2002.bin', 28, 4), ('batch 2', 6, 'in_ctrl_2002.bin', 28, 4),
                                    ('batch 3', 6, 'in_det_3001.bin', 20, 1024), ('batch 3', 6, 'in_det_3002.bin', 24, 64),
                                    ('batch R5', 5, 'in_det_4001.bin', 20, 1024), ('batch R5', 5, 'in_det_4002.bin', 24, 64),
                                    ('batch R5', 5, 'in_field_4003.bin', 20, 1024), ('batch R5', 5, 'in_ctrl_4003.bin', 20, 1024)):
        p = f'{HC_DIR}/{f}'
        starts, d = load(p, n, ncos)
        out = f'{tmp}/dump.bin'
        gpu(HC_BIN, rounds, 'dump', p, n, ncos, M, out)
        raw = open(out, 'rb').read()
        ok = sum(raw[32 * i:32 * i + 32] == okec.sha3_256(msg(starts, d, n, i), rounds=rounds) for i in range(M))
        os.unlink(out)
        tot_ok, tot = tot_ok + ok, tot + M
        print(f'{tag:8s} hcoset rounds={rounds} {f} (n={n}, {ncos} cosets, sha256 {sha(p)[:16]}): messages 0..{M - 1}: '
              f'{ok}/{M} GPU digests equal organizer sha3_256(rounds={rounds})')
    for tag, rounds, f, n, ncos, base in (('W1', 6, 'in_rord_5101.bin', 34, 1, 0), ('W1', 6, 'in_rord_5101.bin', 34, 1, (1 << 33) + 12345),
                                          ('W2', 6, 'in_rord_5102.bin', 24, 1024, 1000 * (1 << 24) + 777),
                                          ('W3', 6, 'in_ctrl_5103.bin', 34, 1, 0),
                                          ('W4', 5, 'in_rord_5104.bin', 34, 1, 0), ('W4', 5, 'in_rord_5104.bin', 34, 1, (1 << 33) + 12345),
                                          ('W5', 5, 'in_rord_5105.bin', 24, 1024, 1000 * (1 << 24) + 777)):
        p = f'{W_DIR}/{f}'
        starts, d = load(p, n, ncos)
        od, ok_ = f'{tmp}/dump.bin', f'{tmp}/keys.bin'
        gpu(W_BIN, rounds, 'dump', p, n, ncos, M, od, base)
        gpu(W_BIN, rounds, 'keys', p, n, ncos, M, ok_, base)
        rd, rk = open(od, 'rb').read(), open(ok_, 'rb').read()
        okd = okk = 0
        for i in range(M):
            ref = okec.sha3_256(msg(starts, d, n, base + i), rounds=rounds)
            okd += rd[32 * i:32 * i + 32] == ref
            lanes = [int.from_bytes(ref[8 * k:8 * k + 8], 'little') for k in range(4)]
            okk += list(struct.unpack('<6Q', rk[48 * i:48 * i + 48])) == pykeys(lanes)
        os.unlink(od)
        os.unlink(ok_)
        tot_ok, tot = tot_ok + okd, tot + M
        print(f'batch W  hcw rounds={rounds} {tag} {f} (n={n}, {ncos} cosets, sha256 {sha(p)[:16]}): messages {base}..{base + M - 1}: '
              f'{okd}/{M} GPU digests equal organizer sha3_256(rounds={rounds}); {okk}/{M} GPU keys equal the six projections '
              f'of the organizer digests')
    print(f'total: {tot_ok}/{tot} digests equal')
finally:
    shutil.rmtree(tmp)
```
