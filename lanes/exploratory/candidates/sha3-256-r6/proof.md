# SHA3-256 with 6 prefix rounds: Gray-order enumeration of two-round-affine cosets with an eight-bit digest filter, time_log2 122.13256

## 1. Claim

Target `sha3-256-r6-prefix-v1` (organizer profile): SHA3-256 of FIPS 202 with "prefix rounds 0 through 5, inclusive,
in every sponge permutation" (not the last-round convention of Keccak-p); all-zero 1600-bit initial state; rate 1088
bits, capacity 512; "SHA3 domain suffix 01 followed by pad10*1; delimited suffix byte 0x06", standard little-endian
lane and bit encoding; the digest is the first 32 squeeze bytes; messages are distinct byte strings of bit length
below 2^64; reference `verifier/keccak.py:sha3_256`. Postcondition: "The two complete sha3-256-r6 sponge hashes agree
on all 256 output bits." The algorithm CAMP-F of Section 8 outputs two distinct 135-byte messages with equal digests.

| Quantity | Value |
|---|---|
| time_log2 (collision-frontier-v5, reference operation cost 1626, rounded up) | 122.13256 (Section 10) |
| success probability | at least 0.39 over CAMP-F's fresh coins (random coset origins and a 128-bit table tag), under premise H_coset (Section 9) |
| memory | below 2^144 words of 256 bits, below 2^149 bytes (Section 11.1) |
| preprocessing (included in time) | at most 2^70 + 16 word operations, below 2^59.34 target compressions (Section 11.2) |
| nonuniform advice | none |

**The route.** CAMP-F enumerates Q = 2^48 G messages: G groups of 256 cosets of the 40-dimensional field span(W40),
each coset in its Gray order (Section 6.1). Inside a group a plane-major Gray-order finite-difference enumeration
(Section 5.5) computes, for all 256 cosets at once, the ten pre-chi bit planes (x, z), x = 0..4, z in {0, 1}, and from
them the eight digest bits z = 0 and z = 1 of lanes 0 to 3 of every message. A message is a *survivor* if these eight
bits are all zero, which holds for one message in 256. The lane of every survivor is extracted from the filter word
(Section 5.6) and appended to a list. Each list is processed in batches of 256 survivors by a bit-sliced kernel
(Section 5.7; its instructions are counted by executing it, Appendix C) that computes the 140-bit key of every
survivor, and the key is probed in the value-masked table of Section 7. Only survivors are probed: two messages with
equal digests have equal filter bits, so a colliding pair consists of two survivors with probability 2^-8, and
CAMP-F examines 16 times as many messages as the earlier candidate-major schedule while probing a sixteenth of that
number of candidates.

CAMP-F is randomized: every coset origin is fresh randomness, drawn with the cost model's primitive "independent
uniform random 256-bit word" (Section 6.1), as is the 128-bit table tag (Section 7); every probability in this
document is over these coins for the fixed target.
One premise is declared (Section 12): **H_coset**, that over these coins the survivor counts and the occupancy,
key-match and triple bounds of Section 9 hold for the messages CAMP-F enumerates (the bounds that independent uniform
digests would give). Everything else is proved or executed here: two-round affinity on every coset of W40, degree at
most 8 before the last chi, exactness of the Gray-order finite differences and of their initialization, the equality
of the filter word with the digest-bit test (Lemma 11), the extraction and list structure (an executed check,
Appendix D), the batch kernel (executed on survivors of random cosets, every table word compared with the key of the
reference hash, Appendix C), correctness of the value-masked table for any initial memory (up to tag events of
probability 2^-128, in the failure budget), the duplicate-coset bound, and every operation count (the kernel's from its
executed program, the others by the formulas of Sections 5 to 7). Section 12 gives the premise's evidence:
reduced-width tests that the organizer executes (the declared experiments), preregistered GPU counts of 32- to 64-bit
digest projections of up to 2^34 messages (Appendix A: protocols with their hashes, programs, raw counts and
validation printouts), the survivor measurements of Section 12.4 (Appendix E), and the effect of a pair-rate shortfall
on the claim.

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

Sections 5.3 and 5.4 and Section 7 up to its subsection 7.1 describe the *reference schedule*: a candidate-major schedule
in which every message is probed. The declared experiments of Section 13 execute it at a reduced size through a
counting machine. The claim does not use its cost. The reference schedule and the filtered route share the machine
(5.1), the key (5.2), the setup and its cost S_g (Section 6), the table and the verification mechanics (Section 7) and
the six-round evaluation, so the experiments exercise those shared parts; they do not execute the plane-major FES, the
filter word, the extraction, the lists or the batch kernel of CAMP-F, which are defined in Sections 5.5 to 5.7 and
counted in Section 10 (Appendices B to D hold the programs that check them). The algorithm CAMP-F of the claim is
defined by Sections 5.5 to 5.7, 7.1 and 8.

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

### 5.3 Candidate-major FES (reference schedule)

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

### 5.4 Record transposes and the key in the word (reference schedule; the butterfly is also used by Section 6.3)

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

### 5.5 The filter and the plane-major FES

**Survivors.** The eight *filter bits* of a message are the digest bits z = 0 and z = 1 of the lanes x = 0, 1, 2, 3.
A message is a *survivor* if all eight are zero. Two messages with equal digests have equal filter bits, so both are
survivors or neither is.

**Planes.** Let p = (x, z) with x = 0..4 and z in {0, 1}: ten of the 175 planes of Section 5.2. For a group (the
cosets j = 256 h + c, lane c) and a Gray point g(i), the *plane word* P_p(i) is the 256-bit word whose bit c is the
pre-chi bit b_{x,z} of the message (h, c, i). After the setup, the transform and the phase conversion (Sections 6.3
and 6.4) the memory holds, for these ten planes, the value x_p = P_p(0) and the records tab_p[T] (1 <= |T| <= 8), each
a 256-bit word with bit c for lane c: these are the records of Lemma 6 with V = F_2^256. By Lemmas 5 and 6, running
the FES of Section 4.2 on these words gives x_p = P_p(i) after step i, for every i < 2^40; no transpose is made
(Section 5.3's candidate-major words are another arrangement of the same bits). The setup is charged in full
(S_g of Section 6.5, which produces all 175 planes) although only these ten planes are used.

**The filter word.** For a fixed z let b_0 .. b_4 be the plane words P_{x,z}(i), indices modulo 5, and

    k_x = b_x XOR b_{x+2} XOR (b_{x+1} AND b_{x+2})     (x = 0, 1, 2, 3)  =  b_x XOR (NOT b_{x+1} AND b_{x+2}).

**Lemma 11 (filter word).** Bit c of k_x is the digest bit z of lane x of the message (h, c, i), XOR 1 if x = 0 and
z = 0 (RC[5] = 0x0000000080000001, Section 2). Hence, with a_0 = (k_0 XOR 1^256) OR k_1 OR k_2 OR k_3 for z = 0 and
a_1 = k_0 OR k_1 OR k_2 OR k_3 for z = 1 (1^256 the all-ones word), the word s = NOT (a_0 OR a_1) has bit c equal to 1
exactly when the message (h, c, i) is a survivor.

*Proof.* The first claim is the digest formula of Section 2 with NOT u AND v = v XOR (u AND v). Bit c of a_z is 1
iff one of the four digest bits z of the message is 1, and s has bit c set iff none of the eight is. QED.

**Passes.** The ten planes are processed in two passes over the same Gray points, each pass keeping five planes: pass A
the planes (x, 0), pass B the planes (x, 1), x = 0..4. A *FES block* is 2^16 consecutive Gray points. For each block, in
this order: pass A, then pass B.

- *Pass A at a point i* (the point 0 of the first block is the initial state): the FES step of Section 4.2 on each of
  its five planes, then u = b_{x+1} AND b_{x+2}, w = b_x XOR b_{x+2}, k_x = w XOR u for x = 0..3 (12 operations),
  k_0 XOR 1^256 (1), three ORs (3) giving a_0, and a STORE of a_0 into the accumulator word ACC[i mod 2^16] at an
  address that is an immediate of the site (1): 17 operations. Registers: the five current values x_p, the 55 records
  of the sets CR_11 of the five planes (11 each) and three temporaries: 63. The two temporaries of the FES step are
  reused by the filter.
- *Pass B at a point i*: the FES step on its five planes, the 12 + 3 operations giving a_1, a LOAD of ACC[i mod 2^16]
  (1), OR (1) and NOT (1) giving s: 18 operations, then the extraction of Section 5.6. Registers: five values, 50
  records (CR_10, ten each) and at most eight temporaries (u, w, a_1 and the five of Section 5.6): 63, and the register that holds the constant 1
  for the returns of Section 5.6: 64.
- *Cached sets.* CR_K is the set of the K records T (1 <= |T| <= 8) with the largest saving, ordered by the function
  savings40 of Appendix B (the number of operations that holding T in a register saves over the whole sequence),
  ties by the smaller bit mask. A step costs, per plane, 1 + [top not in CR] + the sum over its links of 1 (in CR), 2
  (not in CR, last change) or 3 (not in CR, otherwise), as in Section 5.3, and the STORE of a record is omitted at its
  last change (Lemma 5b, which is a statement about one word sequence and holds for every plane).
- *Count.* One plane over the 2^40 - 1 steps costs F(CR) = (K + 1) + (N1 - tops) + N1 + 3 links - 2 links_CR - U with
  N1 = 2^40 - 1 and the other terms as in Section 5.3 for the set CR (the function fes of Appendix B, which gives
  Fc = 18,794,671,433,175 for the 60-record set of Section 5.3). Here F_A = F(CR_11) = 21,440,371,287,364 and F_B = F(CR_10) =
  21,577,810,240,833.
- *Blocks.* At the start of a pass in a block the pass LOADs the records of CR and the current values of its five
  planes (5 (K + 1) LOADs) and at its end STOREs them (5 (K + 1) STOREs); the first block's LOADs are the
  (K + 1) per plane already in F. The block loop costs 8 per pass and block (counter, compare, branch, the base
  addresses). There are 2^24 blocks per pass and group. The records not held in registers stay in memory between
  blocks and between the two passes; the planes of the two passes have disjoint records.

Per group the FES of the ten planes costs 5 (F_A + 2^24 * 2 * 12) + 5 (F_B + 2^24 * 2 * 11) + 2 * 2^24 * 8; the
filter test costs 2^40 (17 + 18) (Section 10).

### 5.6 Extraction, survivor lists and identifiers

**Lists.** A *list block* is 2^30 consecutive Gray points: block I (0 <= I < 2^10) holds the points i with
I 2^30 <= i < (I + 1) 2^30, and off = i - I 2^30 is the *offset* of the point. The survivors of lane c in block I of
group h, in increasing i, form the *list* (h, I, c). Put

    ell = h 2^18 + I 2^8 + c,        base(ell) = 2^127 + ell 2^24,

and let entry q (0 <= q < 2^24) of the list be the word at address base(ell) + q (a *slot*), holding the offset off of
the q-th survivor. The slot addresses of all lists are below 2^127 + 2^126, since ell < G 2^18 and
G 2^42 < 2^126. The *identifier* of the survivor in slot a is nu = a (< 2^128); the probe order of CAMP-F (group, list
block, lane, entry) is the order of nu, so identifiers increase in probe order, as Lemma 8 requires.

**Pointer cells.** Lane c has a word at the address 2^128 + 2^c (c < 128) or 2^129 + 2^(c - 128) (c >= 128) that
holds the address of the next free slot of its current list. At the start of a list block they are set to
base(ell) for the 256 lanes: the register Lbase = 2^127 + (h 2^18 + I 2^8) 2^24 is formed once (2 operations), and
each lane costs an ADD of the immediate c 2^24 and a STORE (2 operations): 514 per block, charged as 3 per list.

**Extraction.** After the filter word s of pass B at the point i of block I (off = i - I 2^30 is an immediate of the
site), the code below runs. The bodies are out of line (a branch on a nonzero register enters them and each ends with
a branch on a register that is known to be nonzero, 1 operation, back to the site).

    s_lo = s AND (2^128 - 1)       1
    BR s_lo -> LOW                 1       (taken when s_lo != 0; LOW is the body below)
    s_hi = s SHR 128               1
    BR s_hi -> HIGH                1       (taken when s_hi != 0)
    LOW:   repeat while s_lo != 0:
             n = NOT s_lo; n = n + 1; l = s_lo AND n       3     (l: the lowest set bit of s_lo)
             a = l OR 2^128                                 1     (the pointer cell of the lane is the word at a)
             p = LOAD [a]; m = MOVI off; STORE [p] = m      3     (append the offset: off = i - I 2^30)
             p = p + 1; STORE [a] = p                       2
             s_lo = s_lo XOR l; BR s_lo -> LOW              2     = 11 per set bit, then 1 to return
    HIGH:  the same with s_hi, a = l OR 2^129                     11 per set bit, then 1 to return

A word s costs 4 operations and, per set bit, 11 plus 1 for the return of its half, at most 12: at most
4 + 12 (number of set bits). Lane c = (index of the bit) in the low half and c = 128 + (index) in the high half; the
cell address a is the pointer cell of that lane. Registers: s, s_lo, s_hi, n, l, a, p, m: at most eight, and the register that holds the constant 1 of the returns
(Section 5.5).

**Lemma 12 (extraction).** For every filter word s the code appends off to the list of every lane c whose bit of s is
1, once, and to no other list, and executes at most 4 + 12 popcount(s) operations.

*Proof.* NOT s_lo + 1 is -s_lo in 256-bit arithmetic, so l = s_lo AND -s_lo is the lowest set bit of s_lo, a power of two
2^e with e < 128; the cell address a = 2^128 OR 2^e (or 2^129 OR 2^e) is the cell of lane e (resp. 128 + e). The body
appends off at the slot a points to, advances the pointer, clears the bit and repeats until s_lo = 0. QED.

Appendix D executes this code one counted instruction at a time on 20,000 random filter words (mean 1 set bit) and
compares every list with the set bits (all equal; the executed counts never exceed 4 + 12 popcount).

**End of a list block.** For the 256 lanes in the order c = 0..255, the list (h, I, c) is processed (Section 5.7),
then the next block starts. The control of a list costs at most 24 operations: a LOAD of the pointer cell (1), the list start (ADD, 1),
n = pointer - start (1), a branch on n (1; an empty list ends here), the survivor count Sc = Sc + n (1) with its
comparison against S_cap and a branch (2; the halt of Section 8), the test of n mod 256 (2), the coset record of
j = 256 h + c (index, address, two LOADs with the second-word add: 6) and its copy with I into the three words that the
block-preparation code reads (3), the LOAD of the tag word and the OR that form v (2), the end pointer of the batch
loop (3) and the pointer P (1). The padding itself (a SUB, a LOAD of the last entry, a register move, then a STORE and
an ADD per pad slot) is charged apart, at its worst case of 2 * 255 + 3 operations.

**Capacity.** A list has room for 2^24 entries, four times the expected 2^22. If a list had 2^24 or more entries the
surplus would be written into the slots of the next list; this event is counted as a failure of the run in Section 9
(it has probability 2^-300 per list under H_coset(d)). Whatever the slots contain, an output of CAMP-F is two messages
that verification (Section 7.1) has recomputed and compared, so no event of this kind can produce a false output.

### 5.7 The batch survivor kernel

A list (h, I, c) with n entries is processed in ceil(n / 256) *batches* of 256 consecutive entries. If n is not a
multiple of 256 the list is first padded: the last entry is copied into the following slots (a LOAD, then a STORE and an
ADD per slot: at most 255 slots, 2 * 255 + 3 operations), so that the last batch is full. A *pad lane* is a lane that
probes a copy; it carries the message of the last entry again (Section 7.1 and Lemma 9 show that this changes nothing
but the count of tag passes, which has the deterministic bound 255 per list).

**What the kernel computes.** The kernel is a straight-line program of 48,175 instructions on 256-bit words, with the
loop control of 5 more per batch (the load of the tag word, the addition that forms the identifier register, the pointer
increment, the end test and the branch). One run takes the pointer P to the first of 256 slots and processes the 256
survivors of one list together, one per bit position:

1. *Indices.* The 256 offsets are loaded (ADD, LOAD per slot) and transposed by a butterfly network with a chosen
   order of the eight stages (Section 5.4, with the known-zero masks of the upper bits folded) into the 30 index planes
   (plane b: bit c = bit b of the offset of survivor c); the Gray bits are the planes u_b = ind_b XOR ind_{b+1} for
   b < 29 and u_29 = ind_29 (the Gray code of the offset within the block).
2. *Parameter planes.* The parameter of survivor c is t_j XOR w(g(I 2^30)) XOR sum_b g(lo)_b w_b, where g(I 2^30) and
   g(lo) are Gray codes within their parts (g(i) = g(I 2^30) XOR g(lo) for i = I 2^30 + lo). Plane k (k < 320) of the
   parameters is the XOR of the u_b with bit k of w_b set, XOR the broadcast bit k of the *block base*
   t_j XOR w(g(I 2^30)). The block base is formed once per list by the block-preparation code (47 instructions: the
   Gray code of I 2^30, five byte lookups in the ten byte tables of Section 11.2, two words) and its bits are
   broadcast by the prelude, which also computes the nodes that depend only on the block base (hoisted out of the
   batch loop; K_blk = 47 + 3 + the prelude = 2647 instructions per list).
3. *Rounds.* Rounds 0 to 4 and the linear part of round 5 act on the planes word by word (each word operation acts
   on the 256 survivors), with the polarity of every value tracked so that NOT is free, XOR/AND/OR/NOT/shift
   instructions and common subexpressions shared.
4. *Key.* The chi of round 5 on row 0, lanes 0 to 3, slices z = 0..34 gives the 140 digest bits of every survivor as
   140 planes (bit 4z + x of the key row) with the polarity constant pat absorbed; one more row (143) is the marker.
5. *Probe.* A second butterfly network transposes the 256 key rows into one word per survivor; as each word k_c is
   produced it is probed with the 6 operations of the miss path of Section 7 (LOAD, XOR with v, SHR 128, branch, STORE,
   v + 1), the probes of the batch in the order of the lanes. The table address is k_c = keyword(message) XOR pat with
   keyword = sum 2^(4z + x) (digest bit z of lane x) + 2^143: an injective function of the 140-bit key with bit 143
   set, so Lemmas 8 and 9 hold for it as for the key word of Section 5.2.

The register file is the 64 registers of Section 5.1, four of them reserved (the pointer P, the identifier register v
and two temporaries), the rest allocated by a Belady schedule with spills to memory (counted: STOREs and LOADs of
spill words are instructions of the program). Every address in the program is an immediate relocated by a constant
base chosen at generation time, except P + offset for the slot loads and the table address. The program and the
program that builds it are listed in Appendix C; its run prints K_batch and K_blk and executes the kernel:

- the program builds the kernel for 2^30-point blocks (transposition stage order found by a search of 300 swaps with
  a fixed seed), prints its instruction counts (48,175 instructions + 5 loop control = K_batch = 48180; K_blk =
  2647), then *executes* it, instruction by instruction on Python integers, on 48 batches (12,288 survivors) of 12
  random cosets with random block indices I and 256 distinct random offsets per batch (the first batch of the first
  block contains offset 0 and the first batch of the second block offset 2^30 - 1), counts every executed instruction,
  and compares the table: for every survivor the word at keyword(M) XOR pat, M computed by the reference hash of
  Section 2 (ref.py), must equal the tag plus the identifier of the survivor's slot. The printout shows 0 wrong table
  words, and 48,180 executed instructions per batch, equal to K_batch.

The kernel includes the key rows of the eight filter bits, which are constant for survivors; they are not removed.

## 6. Outer cosets and setup

### 6.1 The cosets: fresh random origins

Coset j (0 <= j < C = 256 G) has origin t_j, drawn by the leader step (Section 6.2) from two fresh calls r_0, r_1 of the
cost model's primitive "independent uniform random 256-bit word": t_j = r_0 + (r_1 mod 2^64) 2^256. The C origins are
therefore independent and uniform on F_2^320. With the table tag r of Section 7 (one further fresh draw, independent of
them) they are CAMP-F's coins, and every probability below is over them, for the fixed target. Group h (h < G) holds
the cosets j = 256 h + c, c = 0..255. The message (h, c, i) (lane c, Gray point i) is
M(t_j XOR sum_b g(i)_b w_b) with j = 256 h + c; its reference identifier is cid = h 2^48 + c 2^40 + i < 2^128 (coset-major).
Inside each coset the enumeration is the fixed Gray order of span(W40). The reference schedule probes the candidates in increasing cid
(group by group, inside a group lane by lane, inside a lane in Gray order), so cid is also the number of candidates
probed before it; CAMP-F probes the survivors of a group list block by list block, and its identifiers are the slot
addresses of Section 5.6 (cid is the value that Section 7.1 decodes from them).

**Lemma 7 (distinct messages).** Let D be the event that the C cosets t_j + span(W40) are pairwise distinct. On D the
Q = 2^48 G messages are pairwise distinct, and Pr[not D] <= C(C, 2) 2^-280 = 6.27906826519e-30 (G, C and Q as in Section 9).

*Proof.* Distinct cosets of span(W40) are disjoint. Inside a coset, distinct i give distinct g(i) and, by rank 40,
distinct parameters; Lemma 1 gives distinct messages. For j < j' the sum t_j XOR t_j' is uniform on F_2^320 (t_j' is
uniform and independent of t_j), so the two cosets coincide with probability |span(W40)|/2^320 = 2^-280; the union
bound over the C(C, 2) pairs gives the bound. QED.

The event not D (a duplicate coset) is counted as a failure in Section 9; no duplicate rejection is performed.

### 6.2 Leader step (11 operations per coset, 5 per group)

For lane c of group h: j = H8 OR c with H8 = h * 2^8 (1); two random words r_0, r_1 (2); r_1 AND (2^64 - 1) (1); the
record address CSB + 2j (shift, add: 2); two STOREs of t_j into the global coset record with the second-word add (3);
two STOREs into the lane's working frame (2). This is 11 operations per coset. Group control is 5 per group: H8 = h * 2^8 before the leader step (1), the list-block register
Lbase = 2^127 + h 2^42 (1), and after the last list block h = h + 1 (1), its compare with G (1) and the branch (1).
S_v (Section 6.5) charges exactly these 11 C + 5 G operations. (In the reference schedule the five are H8, the
identifier cid = h * 2^48 after the record transposes (Section 5.4) and, after the last lane, h = cid >> 48 (cid is then
(h + 1) 2^48), its compare with G and the branch, and the table register v = r 2^128 + cid adds 3 per group.) In CAMP-F
the register v is formed per list (Section 7.1).

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
    S_v = G S_g = 132,356,406,391,353,953,446,737,044,479,447,515,539.

The FES, the filter, the extraction, the kernel and the tag passes of CAMP-F are charged in their own rows of Section 10;
the record transposes (7,800 P_D) and the frame copies (2 P_D per lane) of the reference schedule are not used by CAMP-F.

## 7. Value-masked table and verification

The text up to Section 7.1 describes the table and the verification of the reference schedule, which the declared
experiments execute (its identifier is cid, its verification at most 2756 operations, its tag passes 2760 operations
each, and R140 = 41,080,884,464,398,111,069,785,063,816,008,882 is its cap); Section 7.1 gives the identifier, the
verification and the charges of CAMP-F.

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
at most 2760 operations beyond the 6 of a miss (4 + 2756 with its verification, or 8 for a false pass): the filed ledger
of the reference schedule charges 2760 (R140 + FP); CAMP-F's charges are in Section 7.1. The probe uses the key word's register and s besides v: the two temporaries of
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

### 7.1 The table and the verification in CAMP-F

CAMP-F uses the table of this section unchanged, with these differences.

- **Identifiers.** The identifier of a probe is the slot address nu of Section 5.6 (below 2^128), including the slots
  of pad lanes. The register v = r 2^128 + nu is formed at the start of each list (a LOAD of the tag word and an OR
  with the first slot address) and v increases by 1 per probe, in the order of the lanes of a batch and of the
  batches of a list, which is the order of nu. The probe is the one of the box above; the kernel executes its miss path
  (6 operations per probe) and the tag-pass, hit and false-pass paths are the code of the box.
- **The earlier survivor of a hit.** From the stored identifier s (a slot address) the code decodes (j, i) in 13
  operations instead of the 8 of the box: lo = LOAD [s] (1); ell = (s AND (2^127 - 1)) SHR 24 (2); c = ell AND 255 (1);
  I = (ell SHR 8) AND (2^10 - 1) (2); h = ell SHR 18 (1); j = (h SHL 8) OR c (2); the record address CSB + 2j (2);
  i = (I SHL 30) OR lo (2). The remaining 50 operations for the earlier candidate (two LOADs of t_j, g(i), the byte
  tables, the five lanes) are those of the box: 63 operations in all instead of 58.
- **The current survivor.** Its Gray point is no longer an immediate of the site, so the current candidate is decoded
  from v exactly as the earlier one: s = v AND (2^128 - 1) (1), the 13 operations above, then the 50 others: 64
  operations instead of 19.
- **Registers.** The kernel's registers are live at a probe, so verification saves all 64 registers (64 STOREs) and
  restores them (64 LOADs) instead of the 61 + 61 of the box.
- **Distinct messages.** After the four digest comparisons succeed, the code compares the two parameters it built (two
  words each): two XORs, an OR and a branch (4 operations); equal parameters mean that a pad lane met its original (or
  the same message twice), the pass is a miss of the verification and is counted in F, and no output is made.

Verification therefore costs at most 5 (the count F) + 128 (all registers) + 63 (earlier survivor) + 64 (current survivor)
+ 2542 (two six-round evaluations) + 8 (digest compares and branches) + 4 (distinct messages) = 2814 operations,
charged as 2816 = VER, and a tag pass 4 + 2816 = 2820 operations beyond the 6 of a miss (a false pass costs 8, less).
The verification still uses at most 34 + 4 + 1 = 39 registers after the spill. The run stops when F reaches
R + FP + 255 L (Section 8), with R, FP and L as in Section 9.

An output of CAMP-F is a pair of parameters that verification has built from slots and coset records, evaluated with
the six rounds and found to have equal digests and different parameters; it is a collision of the target whatever the
contents of the slots were.

**Address map of CAMP-F (words).** Survivor slots [2^127, 2^127 + 2^126); pointer cells 2^128 + 2^c and 2^129 + 2^c
(c < 128); coset records [2^130, 2^130 + 2C); the work region (frames, plane and coefficient records, accumulators,
the kernel's regions, spill words, byte tables, the words of F, Sc and h, the tag word) from 2^131, fewer than 2^36
words; generated code from 2^132; SPARSE [2^143, 2^144). The regions are disjoint and every address is below 2^144.

## 8. The algorithm CAMP-F

```
Preprocessing (once, Section 11.2): generate the code (Section 11.2 (a)), the batch kernel (Appendix C), the constants
  w_b, masks and byte tables; check rank and the 780 polarizations of Lemma 3; h = 0; F = 0; Sc = 0; draw the tag r
  and store r 2^128.
Group h (repeated):
  Setup (Section 6): leader step of the 256 cosets j = 256 h + c, each origin t_j from two fresh random words; the
    transpose of the origins into 320 bitplanes; for every |S| <= 8, in order of increasing |S|, the constant-folded
    bit-sliced evaluation of the 256 lanes into A[S]; the transform; the phase conversion.
  For I = 0 .. 2^10 - 1 (list block, Gray points I 2^30 .. (I + 1) 2^30 - 1):
    set the 256 pointer cells to base(h 2^18 + I 2^8 + c) (Section 5.6)
    For each FES block of 2^16 points (2^14 per list block):
      pass A (planes (x, 0)): FES steps, filter test, STORE a_0 (Section 5.5)
      pass B (planes (x, 1)): FES steps, filter test, s; for every point extract the lanes of the set bits of s and
        append the offset to their lists (Section 5.6)
    For c = 0 .. 255: for the list (h, I, c) with n entries (n = 0: nothing): Sc = Sc + n, stop with failure if
      Sc > S_cap; pad to a multiple of 256, v = r 2^128 + (first slot address); for each batch of 256: run the kernel
      (Section 5.7): the 256 survivors in lane order are probed (Section 7, 7.1); a false pass adds 1 to F; on a hit
      with identifier s: verification of s against the current survivor (7.1); if the digests are equal and the
      parameters differ, output the two messages and stop; if F reached R + FP + 255 L, stop with failure.
  h = h + 1; if h = G, stop with failure.
```

Every bound (G groups, 2^10 list blocks, 256 lanes, 2^40 points, S_cap survivors, R + FP + 255 L tag passes) is a halt of
the algorithm. The survivors of a group are processed list block by list block; a survivor is probed once, a pad lane
once more; so the operation count of Section 10 is an upper bound for every run (the data-dependent parts are bounded
by S_cap, by L and by the caps: each row of Section 10 says by which).

## 9. Success

Let G = 19,293,989,054,611,038,904,195,207 (groups), C = 256 G = 4,939,261,197,980,425,959,473,972,992 cosets, Q = 2^48 G = 5,430,775,119,802,293,950,487,074,653,139,781,025,792 messages (the Gray points of the cosets),
S = 2^40 G = 21,213,965,311,727,710,744,090,135,363,827,269,632 (the expected number of survivors, one message in 256), S_cap = S + ceil(S/2^20) = 21,213,985,542,941,577,671,914,865,369,220,644,864,
L = 2^18 G = 5,057,803,466,731,956,182,501,348,343,808 lists, lambda = Q(Q - 1)/2^265 = 0.4974790409522713587270874 (the expected number of unordered pairs of survivors with
equal digests) and T40 = sum_{k=0..40} lambda^k / k!. The messages are the M(t_j XOR sum_b g(i)_b w_b) of Section 6.1,
j < C, 0 <= i < 2^40; the *survivors* are those whose eight filter bits (Section 5.5) are zero; the *probed
candidates* are the survivors in probe order (group, list block, lane, Gray point) together with the pad lanes of
Section 5.7, each of which probes a copy of the last survivor of its list.

**Lemma 7 (Section 6.1).** With G, C and Q as above, on D (the C cosets t_j + span(W40) are pairwise distinct) the Q
messages are pairwise distinct, and Pr[not D] <= C(C, 2) 2^-280 = 6.27906826519e-30. The event not D is counted as a failure;
no duplicate rejection is performed.

**Lemma 9 (detection).** Suppose D holds; the survivors contain two with equal digests; no list has 2^24 or more
entries; the run does not stop at S_cap or at the cap R + FP + 255 L; the first survivor C* in probe order that has an
earlier survivor with the same digest has a key word k* with tau(k*) != r (Lemma 8); and there is no bad triple:
survivors A, B, C, A not in {B, C}, with digest(B) = digest(C), key(A) = key(B) and digest(A) != digest(B). Then
CAMP-F outputs a collision.

*Proof.* Let B be an earlier survivor with the digest of C = C* and k = k* the key word of both (pad lanes follow
their original in probe order and copy its key, so the first probe of any key word k is that of a real survivor). By
Lemma 8 the probe of C hits and returns the first probed candidate A0 with key word k; A0 is a survivor that
precedes or equals B. If digest(A0) = digest(B), verification of A0 against C finds equal digests and different
parameters (the messages are distinct on D, Lemma 7) and CAMP-F outputs them. Otherwise A0 != B has the key of B and C
and a different digest: a bad triple. QED.

**Random variables.** Over the coins (the origins t_j) let F1 be the event that no two survivors have equal digests;
X the number of unordered pairs of survivors with equal 140-bit keys; Y the number of bad triples of Lemma 9; S_r the
number of survivors. Let mu = Q(Q - 1)/2^149 = 4.13289417844e+34 (a pair of messages are both survivors with equal key with
probability 2^-148), r_X = ceil(mu) = 41,328,941,784,374,359,033,570,814,416,443,766, the Chebyshev parameter kappa = 19345871228983, and
R = r_X + ceil(sqrt(kappa r_X)) = 41,328,941,785,268,531,492,211,003,827,071,250. Over the tag r (Section 7), Z is the number of probed candidates whose key
word k has tau(k) = r, and FP = 2^100. The deterministic bound on the tag passes of pad lanes is 255 L = 1,289,739,884,016,648,826,537,843,827,671,040, and
the cap of the run is R + FP + 255 L = 42,619,949,319,885,408,548,150,344,357,947,666.

**Premise H_coset (Section 12).** Conditioned on D: (a) Pr[F1 | D] <= 1/T40 + 2^-100; (b) E[X | D] <= mu and
Var[X | D] <= mu; (c) E[Y | D] <= Q(Q - 1)(Q - 2)/2^405 = 0.00193837239010629242; (d) Var[S_r | D] <= S, and each list
has fewer than 2^24 entries with probability at least 1 - 2^-300.

These are the bounds that independent uniform 256-bit digests of the Q distinct messages give: (a) the number of
survivors is Binomial(Q, 2^-8) and, given N_b survivors, no two share a digest with probability
prod_{k < N_b} (1 - k 2^-248) <= exp(-N_b (N_b - 1) 2^-249); at N_b = S this is exp(-lambda) up to a relative 2^-120
and exp(-lambda) <= 1/T40; the fluctuation of N_b (variance S) changes the mean of the exponential by a relative 2^-125
at most; the term 2^-100 covers both; (b) the survivor keys (140 digest bits, eight of them fixed) are uniform on 2^132 values, the pair indicators
pairwise independent (two pairs sharing a survivor agree with probability 2^-264), so Var X <= E X = C(Q, 2) 2^-148 =
mu; (c) C(Q, 2) 2^-264 (Q - 2) 2^-140 = Q(Q - 1)(Q - 2)/2^405 (B and C survivors with equal digests, A any message
whose key equals the key of B, which has the eight filter bits zero); (d) the binomial law. H_coset asserts these
bounds for CAMP-F's randomized enumeration; it is not proved.

**Theorem.** Over CAMP-F's fresh coins and under H_coset, CAMP-F outputs a collision with probability greater than 0.39.

*Proof.* If D holds, F1 fails, X < R, Y = 0, Z < FP, tau(k*) != r, S_r <= S_cap and no list reaches 2^24 entries, then
CAMP-F outputs a collision: on D the messages are distinct (Lemma 7); F counts tag passes, and a pass reads either a
written word, pairing the probing survivor with an earlier survivor of equal key (at most X such passes) or a pad lane
with its original (at most 255 L), or a never-written word whose tag is r (at most Z), so F stays below
R + FP + 255 L and the cap never stops the run; the survivor counter never exceeds S_cap; Lemma 9 applies. Hence

    Pr[failure] <= Pr[not D] + Pr[F1 | D] + Pr[X >= R | D] + Pr[Y >= 1 | D] + Pr[Z >= FP] + Pr[tau(k*) = r]
                    + Pr[S_r > S_cap | D] + Pr[a list reaches 2^24 entries | D].

(0) Pr[not D] <= C(C, 2) 2^-280 = 6.279068265e-30 (Lemma 7, proved).
(i) Pr[F1 | D] <= 1/T40 + 2^-100 by (a): 1/T40 = 0.6080616276, 2^-100 = 7.888609052e-31.
(ii) By (b) and Chebyshev's inequality, as R - mu >= ceil(sqrt(kappa r_X)) >= sqrt(kappa mu):
Pr[X >= R | D] <= Var[X | D]/(R - mu)^2 <= mu/(kappa mu) = 1/kappa = 5.169061595e-14.
(iii) Pr[Y >= 1 | D] <= E[Y | D] <= Q(Q - 1)(Q - 2)/2^405 = 0.001938372390 by (c) and Markov's inequality.
(iv) For fixed origins Z is a sum of at most S_cap + 255 L indicators (the probed candidates), each of probability 2^-128
over r, so Pr[Z >= FP] <= (S_cap + 255 L) 2^-128/FP = 4.918239348e-32 by Markov's inequality. (v) The origins fix k*, so
Pr[tau(k*) = r] = 2^-128 = 2.938735877e-39.
(vi) By (d) and Chebyshev's inequality, as S_cap - S = ceil(S/2^20): Pr[S_r > S_cap | D] <= S/(S_cap - S)^2 = 5.182961373e-26.
(vii) By (d) and the union bound over the L lists: L 2^-300 = 2.482922995e-60.
The exact rational comparison of the nine terms (integer numerators, program of Appendix B) gives

    sum = 0.6099999999999999999999999829266595851002 < 61/100,

G is the least group count for which this holds with this kappa (G - 1 gives a bound of at least 61/100; the program
checks it). Hence the success probability over the coins is greater than 0.3900000000000000000000000170. QED.

The bound is that of the earlier schedule with three changes: the number of messages is 16 times larger, the digest
pairs counted are those of survivors (lambda is Q(Q - 1)/2^265), and the bad-triple term (c) is 16 times larger,
because a survivor's key has 132 free bits instead of 140 while the survivors are 1/16 as many as the earlier candidates;
G is larger by the factor 1.003 that this term and the new terms (vi) and (vii) cost.

## 10. Cost ledger and certificate

All charges are word operations of Section 5.1; no permutation call is made (verification evaluates the six rounds
in word operations, Section 7). G, Q, S_cap, L and R are those of Section 9; the program of Appendix B computes every
row (it is the only source of the numbers below) and prints the same table.

| term | value |
|---|---|
| setup, G S_g (Section 6.5; S_g = 6,859,981,417,877) | 132,356,406,391,353,953,446,737,044,479,447,515,539 |
| FES, pass A, 5 G (F_A + 2^24 * 2 * 12) (Section 5.5) | 2,068,390,288,656,613,528,876,608,001,190,022,767,180 |
| FES, pass B, 5 G (F_B + 2^24 * 2 * 11) | 2,081,645,779,981,935,229,803,888,369,345,911,845,475 |
| FES block control, G * 2 * 2^24 * 8 | 5,179,190,749,933,523,130,881,380,704,059,392 |
| filter test, G 2^40 (17 + 18) | 742,488,785,910,469,876,043,154,737,733,954,437,120 |
| extraction, 4 G 2^40 + 12 (S_cap + 2^38) (Section 5.6) | 339,423,687,762,209,775,039,338,929,184,491,700,224 |
| batch kernel, ceil((S_cap + 255 L)/256) K_batch, K_batch = 48180 (Section 5.7) | 3,992,781,105,963,035,681,145,784,401,580,733,829,120 |
| lists, L (K_blk + 24 + 513 + 3), K_blk = 2647 | 16,119,219,648,474,744,353,631,797,171,716,096 |
| tag passes, 2820 (R + 2^100 + 255 L) (Section 7.1) | 120,188,257,082,076,852,105,783,971,089,412,418,120 |
| preprocessing, ONCE = 2^70 + 16 | 1,180,591,620,717,411,303,440 |

    N = G S_g + 5 G (F_A + 2^24 * 24) + 5 G (F_B + 2^24 * 22) + G 2^25 * 8 + 35 G 2^40 + (4 G 2^40 + 12 (S_cap + 2^38))
        + ceil((S_cap + 255 L)/256) K_batch + L (K_blk + 540) + 2820 (R + 2^100 + 255 L) + (2^70 + 16)
      = 9,477,295,610,158,093,305,909,371,588,499,261,591,706,

about 1.745109 operations per message of the Q enumerated, 16 times that per candidate-equivalent of the earlier
schedule (27.92 against its 29.456; the rows per message: setup 0.024372, FES 0.380865 + 0.383305, filter 0.136719,
extraction 0.062500, kernel 0.735214, tag passes 0.022131). Each data-dependent row is charged at its halt:
the survivor counter S_cap bounds the extraction per survivor (12; the halt is tested at the end of a list block, which
can add at most 256 * 2^30 = 2^38 survivors) and the kernel batches (at most one batch per 256
survivors plus one ragged batch per list, hence ceil((S_cap + 255 L)/256)); the lists are L, each at its worst case
(24 control operations, 513 for the pad, 3 for its pointer cell and list-block register); the tag passes are at the cap of the run, each at
the worst of the hit path (4 + 2816) and the false pass (8). The time is N/1626 target compressions, and the integer
certificate

    1626^100000 * 2^12213255 <= N^100000 < 1626^100000 * 2^12213256

gives log2(N/1626) = 122.1325595967..., so time_log2 = 122.13256 (rounded up at the fifth decimal). It is 0.07283 bit below
the filed value 122.20540 (N = 9968023424991292613601158421224940979606).

## 11. Memory, preprocessing and advice

### 11.1 Memory

SPARSE: the key words lie in [2^143, 2^144), 2^140 of them used (never initialized); survivor slots: addresses in
[2^127, 2^127 + 2^126), of which fewer than S_cap + 255 L < 2^125 words are written; pointer cells: 512 words; coset
records: 2C words (the retained random origins); work: working frames 512, bitplanes 320, transpose words 3, input words
320, round buffers 5 * 1,600, D words 320, coefficient and derivative records 2 * 175 * P_D, the accumulators ACC
(2^16), the kernel's mask planes, hoisted words and spill words (fewer than 2^27), 61 spill words of the hit path, the
byte tables 2,560, the words that hold F, Sc and h, and the tag word (fewer than 2^36 words in all); generated code and
its constants: fewer than 2^62 words (here fewer than 2^52). The regions are disjoint (Section 7.1) and every address is
below 2^144, so memory is below 2^144 words of 32 bytes, below 2^149 bytes.

### 11.2 Preprocessing: ONCE = 2^70 + 16 operations

(a) **Code generation.** Each of the 2^40 sites (Gray step i) is decoded (the set bits of i, the frame addresses of
T_1..T_L of the ten planes and their cache and last-change flags, the offset of the site) in fewer than 2^14 operations
and emits at most 297 instructions: the FES steps of the ten planes (at most 10 (1 + 3 * 7 + 1) = 230), the filter of the
two passes (35) and the extraction with its two out-of-line bodies (at most 32); the setup code (leader step, transpose,
every point with the NOT pattern of w(S) and the folded rounds, transform pairs and phase terms) has one instruction per
operation of S_g, fewer than 2^43, each generated in at most 16 operations; the folding pattern of the setup rounds (the
same at every point) and the verification rounds (1,271 instructions per message, a rotation counted as its four) come
from one symbolic pass over the 1,600 state words of each round and over the 25 lanes, fewer than 2^25 operations; the
verification code and the batch kernel are generated once (item (f)). In all fewer than 2^50 instructions; at four words
per instruction the code is below 2^52 words and is generated in fewer than 2^56 operations.
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
(d) **One-time control.** h = 0, F = 0, Sc = 0, the register that holds the constant 1, the tag r (the low half of
one random word) and the stored word r 2^128, at most 16 operations.
(e) **Byte tables.** For each of the ten tables (b, k), b = 0..4, k = 0, 1: one zero STORE for v = 0, then each
entry v = 1..255 from entry v - 2^j (j the lowest set bit of v) by LOAD, XOR with the immediate word k of w_{8b+j}
and STORE: 10 (1 + 255 * 3) = 7,660.

(f) **The batch kernel.** The kernel program of Section 5.7 (48,175 instructions, its block-preparation code and its
prelude) is produced by the program of Appendix C: it builds the dependence graph of rounds 0 to 5 on bit-sliced planes
with the polarity rule, searches the stage order of the index transposition (300 swaps, fixed seed), and schedules and
allocates registers. That program performs fewer than 2^28 elementary steps (it runs in 5 seconds), each emulated in
fewer than 2^14 word operations: fewer than 2^42 operations. The pointer cells are written at run time (Section 5.6) and
the accumulators need no initialization.

The total is below 2^56 + 2^42 + 2^35 + 16 + 7,660 < 2^70 + 16 = ONCE, which is in N. In target compressions
ONCE/1626 < 2^59.34; the claim declares preprocessing_log2 = 59.34.

### 11.3 Advice

None. Every constant used by CAMP-F is produced by the procedures of Section 11.2, whose cost is in N.

## 12. Premise H_coset and evidence

**Statement.** Let the C = 256 G coset origins t_j be CAMP-F's coins: independent and uniform on F_2^320 (Section 6.1).
For the Q messages they generate, with the fixed Gray enumeration of span(W40) inside each coset and CAMP-F's order
(groups h = 0..G - 1, list blocks, cosets j = 256 h + c, Gray points g(i)), with the *survivors* of Section 5.5 (the
messages whose eight filter bits are zero), and with F1, X, Y, S_r and D as in Sections 6.1 and 9, assume over the
coins: (a) Pr[F1 | D] <= 1/T40 + 2^-100 (no two survivors share a digest); (b) E[X | D] <= Q(Q - 1)/2^149 and
Var[X | D] <= Q(Q - 1)/2^149 (equal 140-bit keys of survivors); (c) E[Y | D] <= Q(Q - 1)(Q - 2)/2^405 (bad triples of
survivors); (d) Var[S_r | D] <= S, and each of the L lists receives fewer than 2^24 survivors with probability at
least 1 - 2^-300. These are the values for independent uniform digests of distinct messages (Section 9). Success is then
a probability over CAMP-F's fresh coins; nothing is assumed about the randomness of the fixed target beyond (a) to (d).

This is assumed, not proved. The concerns it answers: on a coset every digest bit is a polynomial of degree at most 16
in the 40 inner variables (Lemma 4 and the last chi), so equal-digest pairs inside a coset, or across random cosets,
could be rarer than for uniform values; and the eight filter bits are digest bits of the same degree, so the
survivors could be distributed differently from a uniform 1/256 sample (their number, their other digest bits, their
pair collisions, their gaps in Gray order). Section 12.4 tests that second concern.

### 12.1 GPU evidence

The runs of this subsection are on unfiltered digests (all messages of their inputs); Section 12.4 tests the survivors.

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
a complete coset of CAMP-F) or 1024 cosets of dimension 24 (the first 24 ordered W40 vectors), at six rounds (W1, W2)
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

The declared experiments hcoset-within16 and hcoset-cross16 (Section 13) test a reduced-width form of (a) and (b), and
hcoset-filter8 one of (d) and of the survivor pair rate, at every organizer run, on the run's own six-round digests: per experiment 2^17 digests, one group of 256 cosets whose
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

- Survivors (hcoset-filter8). On a group of the same size (2^17 messages) the program takes the survivors, the points
  whose digest bits z = 0 and z = 1 of lanes 0..3 are all zero, and stops unless their number lies in [422, 602]
  (Binomial(2^17, 2^-8): expectation 512, standard deviation 22.6, expectation +- 4 sd) and the number of pairs of
  survivors that agree on the next eight digest bits (z = 2 and 3 of lanes 0..3) lies within 4 sd of C(n, 2)/256 (n
  the number of survivors; for uniform values each pair agrees with probability 2^-8 and the indicators are
  pairwise independent). The three pair counts above are checked too. Trial t returns the t-th such pair, so the two
  survivors agree on 16 digest bits (the mask of the other experiments) and the organizer recomputes both digests; the
  interval guarantees at least 273 pairs, so all 256 trials return one. Digests are also checked natively for the eight
  zero bits.

Run locally on the requests that the organizer's runner builds from its public seed, the two experiments give 224 and
165 successes and the group counts (pairs16_within, pairs16_cross, pairs24_cross) = (513, 131,526, 500) and (485,
130,615, 519), all inside their intervals; two runs of each are byte-identical. hcoset-filter8 gives, on the request that the runner builds
for it, 501 survivors (expectation 512) and 465 survivor pairs on eight more bits (expectation C(501, 2)/256 = 489.3),
all 256 trials return a pair, and two runs are byte-identical. Scope: this is the organizer-executed
part of the evidence. It reaches 16 and 24 bits, 2^17 digests per run (about 512 survivors) and 9-dimensional sub-cosets, not 256 bits,
complete cosets or Q messages, and it does not measure the key-match variance or triples at 140 bits.

### 12.3 Sensitivity

Suppose the pair-collision rate of CAMP-F's messages is (1 - eps) of uniform: the expected number of equal-digest pairs
is (1 - eps) lambda (survivor pairs), and (a) becomes Pr[F1 | D] <= 1/T40((1 - eps) lambda) + 2^-100, with
T40(x) = sum_{k<=40} x^k/k!; (b), (c) and (d) keep their values (a lower pair rate does not raise them). For each eps the table gives the success bound of
Section 9 at this N (G and kappa as in Section 9; exact rational comparison with the printed value), and the least G at
which the failure bound, with the same kappa, is again below 61/100 (exact comparison; G - 1 fails), with the ledger
N of Section 10 at that G and the integer E of its certificate 1626^100000 2^(E - 1) <= N^100000 <
1626^100000 2^E, so time_log2 = E/100000 (rounded up at the fifth decimal); extra is that time_log2 minus the claim,
close to -(1/2) log2(1 - eps) in every row. Only the row eps = 0 is claimed.

| eps | success at this N | least G | N at that G | E | time_log2 | extra |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | > 0.39 | 19,293,989,054,611,038,904,195,207 | 9,477,295,610,158,093,305,909,371,588,499,261,591,706 | 12,213,256 | 122.13256 | 0 |
| 0.01 | > 0.386967 | 19,392,141,617,293,258,998,012,002 | 9,526,104,497,730,635,322,705,212,351,144,083,185,936 | 12,213,998 | 122.13998 | 0.00742 |
| 0.05 | > 0.374685 | 19,800,340,687,090,852,486,370,883 | 9,729,156,701,265,196,678,518,943,167,820,880,862,350 | 12,217,040 | 122.17040 | 0.03784 |
| 0.1 | > 0.358985 | 20,348,933,684,837,214,985,025,430 | 10,002,209,988,811,213,955,704,598,344,930,212,147,188 | 12,221,034 | 122.21034 | 0.07778 |
| 0.25 | > 0.309471 | 22,317,875,662,332,828,497,064,510 | 10,983,770,912,008,581,606,441,003,450,386,460,289,448 | 12,234,539 | 122.34539 | 0.21283 |

**Scope and extrapolation.** The evidence covers projections of at most 64 digest bits: 32-bit within-coset and 44-bit
global projections of single lanes on 2^30 messages (batches 1 to 3), 36- to 64-bit projections of single lanes and
of two-lane projections on 2^34 messages (batch W), and the organizer-executed 16- and 24-bit tests on 2^17 messages
per run (Section 12.2); sub-cosets of dimension 9 to 34 of span(W40); random origins (batches 1, 2 and W and the
organizer-executed tests) and fixed origins (batch 3). No count shows a pair deficit beyond the preregistered
thresholds. The premise extrapolates to the full 256-bit digest and its 140-bit key, to complete 40-dimensional
cosets, to C = 256 G random cosets and to Q messages, and, for the survivors, as stated in Section 12.4: the full 256-bit collision event, the key-match variance and the
triple bound are not measured; they are the premise, and the table above gives the effect of a shortfall in the pair
rate.

**Limits.** No proof is known. Image size and balance do not imply the premise: a balanced linear map onto F_2^256 can
be injective on every translate of a campaign space, so its campaigns contain no collision at all. No such structure is
known for the native function and none is excluded by proof. The GPU batches are our runs; the organizer executes the
tests of Section 12.2.

### 12.4 Survivor measurements (our GPU runs, not preregistered)

Appendix E holds the GPU scan program (scan.cu), the analysis program (analyze.cpp), the check scripts and the
raw report lines of every run quoted here. No protocol was hashed before these runs and no pass rule was fixed; the
numbers are reported with their z values, run by run.

**What was run.** For 2^16 = 65,536 cosets of span(W40) with random origins (five 64-bit words from a mixing function of the
run seed, not the attack's random-word primitive), scan.cu computes the digests (lanes 0 to 3) of the messages at the
first 2^18 Gray points of each coset (mode P, the order of CAMP-F inside a coset), or at 2^18 Gray positions drawn
independently and uniformly from the 2^40 positions of each coset (mode R, a control; positions repeat with small
probability): 2^34 = 17,179,869,184 messages per run, six rounds (the target) or 24 rounds (SHA3-256, a control).
The filter takes the 8-bit value formed by digest bits z1 and z2 of lanes 0..3 and keeps the messages whose value
equals a chosen bucket; bucket 0 with (z1, z2) = (0, 1) is the filter of CAMP-F. The GPU digest code agrees with the
reference ref.py on 2,601 test vectors at 6 and 24 rounds (0 mismatches; gen_vec.py in Appendix E). analyze.cpp
reports, for the survivors of a run (about 2^26): (1) the survivor count against 2^26 (z); (2) the bias of each of the
248 other digest bits (z per bit; the expected number of bits with |z| > 3 is 0.67); (3) the parity bias of 30,628
pairs of bits; (4) the number of pairs of survivors with equal projections (17 projections at each of 16, 24 and 32
bits: top and low bits of each lane, a cross-lane projection, random projections of the key bits and of all bits),
compared with the uniform expectation (z for all pairs, for pairs in different cosets, and for pairs in one coset);
(5) the 256-bucket histogram of every coset (variance of the per-coset z of the bucket count, expectation 1, and the
number of cosets with |z| > 3, expectation 176.9); (6) the gaps between consecutive survivors of a coset in Gray
order against a Bernoulli null, and the number of survivors at exact Gray distance d for 17 values of d.

| run | rounds | mode | filter (z1, z2), bucket | survivors (z) | worst bit bias (|z| > 3) | worst pair parity (|z| > 4) | worst pair-rate |z|: 16, 24, 32 bits | per-coset var of z (cosets with |z| > 3) | gap chi-square z |
|---|---:|---|---|---:|---:|---:|---|---:|---:|
| P6 | 6 | P | (0, 1), 0 | 67,112,067 (+0.39) | 3.23 (1) | 4.22 (2) | 1.91, 2.10, 1.94 | 1.0009 (178) | -0.98 |
| P24 | 24 | P | (0, 1), 0 | 67,110,599 (+0.21) | 2.50 (0) | 4.72 (1) | 1.93, 2.16, 2.42 | 0.9995 (175) | +3.32 |
| P24c | 24 | P | (0, 1), 0, other seed | 67,112,823 (+0.48) | 2.94 (0) | 4.09 (1) | 1.52, 2.12, 1.89 | 0.9991 (177) | -0.58 |
| P6c | 6 | P | (0, 1), 255 | 67,098,147 (-1.31) | 3.21 (1) | 4.69 (1) | 2.66, 1.84, 1.55 | 1.0028 (180) | -0.48 |
| P6b | 6 | P | (17, 34), 165 | 67,098,141 (-1.31) | 2.51 (0) | 4.22 (2) | not used (1) | 0.9999 (196) | +2.03 |
| R6 | 6 | R | (0, 1), 0 | 67,099,676 (-1.12) | 3.39 (1) | 4.29 (1) | 1.42, 3.74, 1.28 | 1.0025 (178) | - |
| R24 | 24 | R | (0, 1), 0 | 67,112,197 (+0.41) | 3.22 (2) | 4.48 (3) | 1.70, 1.27, 2.09 | 1.0033 (206) | - |

(1) The projection table of P6b was computed with projections that contain its filter bits and is not used.

Reading. The survivor counts are within 1.31 sigma of 2^26 in all seven runs; the 6-round and 24-round runs and the
Gray-prefix and random-position runs agree; the per-bit bias statistic has sum z^2 between 213.6 and 290.8 against
248 degrees of freedom and five bits with |z| > 3 over 1,736 tests (4.7 expected); no pair-collision rate of survivors
at 16 to 32 bits deviates by more than 2.66 sigma in a Gray-prefix run (one projection of R6 at 24 bits reaches 3.74
among 51); the gap histogram of P24 differs from the Bernoulli null at z = 3.32 and the repeat of that run with another
seed (P24c) does not (z = -0.58); survivors at Gray distances 1 to 8 and 65,536 stay within 2.71 sigma of the
expectation in every Gray-prefix run (Appendix E).
In the random-position runs the 32-bit within-coset counts are small numbers (expectation 8) and include repeated
positions of the sampler; they are not used.

**What was not measured.** Survivors of complete cosets (2^32 per coset) or of more than 2^18 of the 2^40 points; more
than 65,536 cosets, or origins from the attack's random primitive; collision rates of survivors beyond 32-bit
projections (the premise needs the 132 free key bits and the 248 digest bits); the key-match variance, the bad-triple
rate or any full-digest collision among survivors; list counts at 2^30-point scale; the dependence between the 256
lanes of one group. These are the premise (a) to (d). The organizer-executed experiment hcoset-filter8 (Section 12.2)
tests the survivor count and the survivor pair rate on 8 further bits, at reduced size, on every run.

## 13. Experiments

`experiments/fes_campaign.py` (Python standard library) serves the four declared experiments. Each run executes the
reference schedule (Sections 5.3, 5.4, 6 and 7, which share with CAMP-F the setup, the table and the verification
mechanics; see the introduction of Section 5) at a reduced size on the organizer's trials. fes-campaign-reduced checks the event of the
claim (two distinct messages with equal 256-bit digests; none expected at this size); hcoset-within16 and
hcoset-cross16 then run the premise test of Section 12.2, whose checked event is that the two returned digests agree
on bits 0..3 of lanes 0..3 (a 16-bit mask event, not a collision); hcoset-filter8 runs the survivor test of
Section 12.2 with the same checked event for pairs of survivors. The request must name one of the three experiments
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
- Survivor test, in hcoset-filter8, not counted. Event bits 0..7 of a key are the eight filter bits (the digest bit z = 0
  of lane 0 is the key bit XOR 1, since RC[5] has bit 0 set), so a survivor is a point whose event bits 0..7 equal 1.
  The program takes the survivors among the group's 2^17 keys (key index 256 i + c: lane c, Gray point i), stops unless
  their number lies in [422, 602] and the number of pairs agreeing on event bits 8..15 lies within 4 sd of
  C(n, 2)/256, and returns the t-th pair (sorted by the value of event bits 8..15, then by index) in trial t; both
  digests of a returned pair are checked natively for the eight zero bits and for the mask.

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
once_ops = 7,666 (control 6: h, F, the tag, r 2^128 and v; byte tables 7,660) without reporting it. hcoset-filter8 reports the same 13 and, in place of the three pair counts, survivors8 and pairs8_survivors.
No trial of
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
  the kernel checks, the schedule levers, the package and the experiment program with its premise tests; the filtered
  route (filter, extraction, batch kernel) and its survivor measurements.

**Changes from the filed package (time_log2 122.20540).** The candidate-major FES, the record transposes and the key rows
of every message are replaced by the filtered route of Sections 5.5 to 5.7: the plane-major FES of ten planes in two
passes of five, the filter word, the extraction of the survivors' lanes, per-lane lists and a batch kernel that
computes the keys of 256 survivors at a time; only survivors are probed, and 16 times as many messages are
enumerated. The setup, the value-masked table, the false-pass halt, the Chebyshev verification cap and the structure
of the premise are kept; the verification decodes slot identifiers and saves all 64 registers; G rises by a factor
1.003 (a larger bad-triple term and the new terms); the premise gains the survivor part (d). The ledger falls from
29.456 to 27.92 operations per candidate-equivalent (0.07283 bit).

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

## Appendix B. The ledger program

`ledger_s6f.py` (Python standard library only) computes every row of Section 10, the failure terms of Section 9, the
least G, the certificate and the table of Section 12.3. Its printout follows the listing; the numbers of Sections 9, 10
and 12.3 are copied from it. The two constants KB and KBLK are those printed by the program of Appendix C.

#### ledger_s6f.py (9501 bytes, SHA-256 cbb8cdf3edaf015b8b9a086a1266da0370c03c706374d2baa5afa7448cb5c622)

```python
"""Exact integer ledger of the filtered route (proof.md Sections 5.5 to 10). Standard library only. Run: python -B ledger_s6f.py
Rows per group of 256 cosets (Gray points 2^40): setup S_g (unchanged), plane-major FES of the 10 filter planes in two passes of 5
planes (pass A: 11 cached records per plane, pass B: 10), the filter test, the extraction of the lane of every set bit, the
survivor lists and the batch kernel (operation counts of the executed kernel program, Appendix C), the table, the tag passes
and the one-time preprocessing. Constants KB, KBLK are the two numbers that the program of Appendix C prints for B = 30."""
import sys
from math import comb, isqrt
from fractions import Fraction as Fr
from decimal import Decimal, getcontext

sys.dont_write_bytecode = True
getcontext().prec = 60
D, NDIR = 8, 40
B = 30                       # list block: 2^B Gray points
KB, KBLK = 48180, 2647       # kernel program, Appendix C: instructions of one batch of 256 (loop control included), per list prelude
FB = 16                      # FES block: 2^FB Gray points
KA_REG, KB_REG = 11, 10      # cached records per plane in pass A, pass B
PLANES_PER_PASS = 5

# ---- fast exhaustive search counts (Section 5.3 formula, any set CR of cached records) ----
def savings40(T, n=NDIR):
    m = T.bit_length() - 1
    if T.bit_count() < D:
        u = (1 << (n - 1 - m)) - 1 if m <= n - 2 else 0
        return 2 * u - 1
    return (1 << (n - 1 - m)) - 1


def cache_set(K, n=NDIR):    # the K records of largest saving (ties by smallest mask)
    cand = [T for T in range(1, 1 << 12) if 1 <= T.bit_count() <= D]
    cand.sort(key=lambda T: (-savings40(T, n), T))
    return set(cand[:K])


def fes(n, CR):              # operations of one FES pass over the 2^n - 1 steps of one word sequence
    N1 = (1 << n) - 1
    links_total = sum(comb(n, k) * min(D, k) for k in range(1, n + 1)) - N1
    links_CR = tops_CR = 0
    for T in CR:
        m = T.bit_length() - 1
        if T.bit_count() < D:
            links_CR += ((1 << (n - 1 - m)) - 1) if m <= n - 2 else 0
            tops_CR += 1
        else:
            tops_CR += (1 << (n - 1 - m)) if m <= n - 1 else 0
    U_all = sum(comb(n - 1, k) for k in range(1, D))
    U_unc = U_all - sum(1 for T in CR if T.bit_count() < D and T.bit_length() - 1 <= n - 2)
    return (len(CR) + 1) + N1 + (N1 - tops_CR) + 3 * links_total - 2 * links_CR - U_unc

# the reference set of the earlier schedule (60 records) gives the number that the declared experiments assert
REF60 = set(range(1, 32)) | {32 | t for t in range(3, 32)}
assert fes(40, REF60) == 18794671433175
F_A, F_B = fes(40, cache_set(KA_REG)), fes(40, cache_set(KB_REG))

# ---- setup S_g (Section 6.5) ----
P_D = sum(comb(40, j) for j in range(D + 1))
J_D = sum(j * comb(40, j) for j in range(1, D + 1))
V_D = sum(comb(j, r) * comb(40 - j, r) * sum(comb(r, k) for k in range(min(r, D - j) + 1))
          for j in range(1, D + 1) for r in range(min(j, 40 - j) + 1))
POP = 4592341856
assert (P_D, J_D, V_D) == (100146724, 772459520, 282214108)
S_G = 2821 + 13616 + 62022 * P_D + 2 * POP + 700 * J_D + 350 * V_D
assert S_G == 6859981417877

# ---- per-point and per-block operation counts (Sections 5.5 to 5.7) ----
FILT_A, FILT_B = 17, 18      # pass A: 12 + 3 OR + XOR with the all-ones word (iota) + STORE; pass B: 12 + 3 OR + LOAD, OR, NOT
EXTR_PT, EXTR_SV = 4, 12     # per point: AND, BR, SHR, BR; per survivor: 10 (low half) / 11 (high half) + 1 return jump
BLK_CTRL = 8                 # per pass and FES block
LIST_CTRL, PAD_MAX_OPS, CELL_INIT = 24, 2 * 255 + 3, 3   # per list: control (incl. survivor counter), pad stores, pointer cell
PASS_EXTRA = 4               # tag pass beyond the miss: 4 (+ verification), Section 7
VER = 2816                   # Section 7: verification bound
PASS = PASS_EXTRA + VER
ONCE = (1 << 70) + 16
FP = 1 << 100
KCH = 19345871228983
NBLK = 1 << (NDIR - FB)      # FES blocks per pass and group
LISTS_PER_GROUP = 256 << (NDIR - B)


def sizes(g):
    q = g << 48
    S = g << 40
    Scap = S + (-(-S >> 20))
    L = g * LISTS_PER_GROUP
    return q, S, Scap, L


def r_cap(q, kappa=KCH):     # verification cap, Section 9: r = ceil(mu), R = r + ceil(sqrt(kappa r)), mu = Q(Q - 1)/2^149
    r = -(-(q * (q - 1)) // (1 << 149))
    s = isqrt(kappa * r)
    return r + s + (s * s < kappa * r)


def rows(g):
    q, S, Scap, L = sizes(g)
    padmax = 255 * L
    cap = r_cap(q) + FP + padmax
    batches = -(-(Scap + 255 * L) // 256)
    return [
        ('setup, G S_g (Section 6.5)', g * S_G),
        ('FES pass A, G * 5 (F_A + 2^24 * 2 * 12)', g * PLANES_PER_PASS * (F_A + NBLK * 2 * (KA_REG + 1))),
        ('FES pass B, G * 5 (F_B + 2^24 * 2 * 11)', g * PLANES_PER_PASS * (F_B + NBLK * 2 * (KB_REG + 1))),
        ('FES block control, G * 2 * 2^24 * 8', g * 2 * NBLK * BLK_CTRL),
        ('filter test, G 2^40 (17 + 18)', (g << 40) * (FILT_A + FILT_B)),
        ('extraction, G 2^40 * 4 + 12 (S_cap + 2^38)', (g << 40) * EXTR_PT + EXTR_SV * (Scap + (1 << 38))),
        ('batch kernel, ceil((S_cap + 255 L)/256) K_B', batches * KB),
        ('lists, L (K_blk + 24 + 513 + 3)', L * (KBLK + LIST_CTRL + PAD_MAX_OPS + CELL_INIT)),
        ('tag passes, 2820 (R + 2^100 + 255 L)', PASS * cap),
        ('ONCE', ONCE),
    ]


def ledger(g):
    return sum(v for _, v in rows(g))


def fail_terms(g, eps=Fr(0), kappa=KCH):     # the failure terms of Section 9, exact
    q, S, Scap, L = sizes(g)
    c = g << 8
    lam = (1 - eps) * Fr(q * (q - 1), 1 << 265)
    t, term = Fr(0), Fr(1)
    for k in range(41):
        if k:
            term = term * lam / k
        t += term
    return [('no duplicate coset: C(C, 2) 2^-280', Fr(c * (c - 1) // 2, 1 << 280)),
            ('no full collision among survivors: 1/T40', 1 / t),
            ('slack of that bound: 2^-100', Fr(1, 1 << 100)),
            ('key matches (Chebyshev): 1/kappa', Fr(1, kappa)),
            ('bad triples (Markov): Q(Q-1)(Q-2)/2^405', Fr(q * (q - 1) * (q - 2), 1 << 405)),
            ('tag events Z (Markov): (S_cap + 255 L)/2^228', Fr(Scap + 255 * L, 1 << 228)),
            ('tag at the detecting key: 2^-128', Fr(1, 1 << 128)),
            ('survivor count above S_cap (Chebyshev)', Fr(S, (Scap - S) ** 2)),
            ('a list over capacity: L 2^-300', L * Fr(1, 1 << 300))]


def bound(g, eps=Fr(0), kappa=KCH):
    return sum(v for _, v in fail_terms(g, eps, kappa))


def least_g(eps=Fr(0), kappa=KCH):
    lo, hi = 1 << 80, 1 << 85
    assert bound(hi, eps, kappa) < Fr(61, 100) <= bound(lo, eps, kappa)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if bound(mid, eps, kappa) < Fr(61, 100):
            hi = mid
        else:
            lo = mid
    return hi


def cert(N, K=100000):
    a, b = N ** K, 1626 ** K
    E = (a // b).bit_length()
    assert (b << (E - 1)) <= a < (b << E)
    return E


def l2(N):
    return (Decimal(N).ln() - Decimal(1626).ln()) / Decimal(2).ln()


if __name__ == '__main__':
    print('F_A (K = 11) =', format(F_A, ','), ' F_B (K = 10) =', format(F_B, ','), ' S_g =', format(S_G, ','))
    G = least_g()
    q, S, Scap, L = sizes(G)
    print('G =', G)
    print('Q = 2^48 G =', q)
    print('S = 2^40 G =', S, ' S_cap =', Scap, ' lists L =', L, ' pad bound 255 L =', 255 * L)
    print('r =', -(-(q * (q - 1)) // (1 << 149)), ' R =', r_cap(q), ' cap R + 2^100 + 255 L =', r_cap(q) + FP + 255 * L)
    N = ledger(G)
    for name, v in rows(G):
        print(f'  {name}: {v:,}')
    print('N =', format(N, ','))
    print('N =', N)
    E = cert(N)
    print(f'certificate 1626^100000 * 2^{E - 1} <= N^100000 < 1626^100000 * 2^{E}   claim {E // 100000}.{E % 100000:05d}')
    print('log2(N/1626) =', l2(N), ' N per message Q =', Decimal(N) / Decimal(q))
    b = bound(G)
    print('failure sum < 61/100:', b < Fr(61, 100), ' G least:', bound(G - 1) >= Fr(61, 100))
    s = 1 - b
    print('success >', Decimal(s.numerator) / Decimal(s.denominator))
    for name, v in fail_terms(G):
        print('  failure term %-52s %s' % (name, '%.6e' % (Decimal(v.numerator) / Decimal(v.denominator))))
    print('failure sum =', Decimal(b.numerator) / Decimal(b.denominator))
    print('| eps | success at this N | least G | N at that G | E | time_log2 | extra |')
    for e_ in (Fr(1, 100), Fr(5, 100), Fr(10, 100), Fr(25, 100)):
        g2 = least_g(e_)
        N2 = ledger(g2)
        E2 = cert(N2)
        s2 = 1 - bound(G, e_)
        print('| %s | > %s | %s | %s | %s | %d.%05d | %.5f |' % (float(e_), (Decimal(s2.numerator) / Decimal(s2.denominator)).quantize(Decimal('0.000001'), rounding='ROUND_DOWN'),
              format(g2, ','), format(N2, ','), format(E2, ','), E2 // 100000, E2 % 100000, (E2 - E) / 100000))
    work = 512 + 320 + 3 + 320 + 8000 + 320 + 2 * 175 * P_D + 2560 + 2 + (1 << 16) + (1 << 27) + 61
    instr = (1 << 40) * 297 + S_G + (1 << 17)
    print('address and size checks: slots below 2^127 + 2^126:', G << 42 < 1 << 126, ' slots written below 2^125:',
          Scap + 255 * L < 1 << 125, ' work words', work, '< 2^36:', work < 1 << 36, ' instructions', instr, '< 2^50:', instr < 1 << 50,
          ' generation', (1 << 40) * (2 ** 14 + 4 * 297) + 16 * S_G + 2 ** 25, '< 2^56:',
          (1 << 40) * (2 ** 14 + 4 * 297) + 16 * S_G + 2 ** 25 < 1 << 56)
    assert G << 42 < 1 << 126 and Scap + 255 * L < 1 << 125 and work < 1 << 36 and instr < 1 << 50
    N_FILED = 9968023424991292613601158421224940979606
    print('gain over the filed N (bits):', l2(N_FILED) - l2(N), ' N < N_FILED:', N < N_FILED)
```

#### python -B ledger_s6f.py (output)

```
F_A (K = 11) = 21,440,371,287,364  F_B (K = 10) = 21,577,810,240,833  S_g = 6,859,981,417,877
G = 19293989054611038904195207
Q = 2^48 G = 5430775119802293950487074653139781025792
S = 2^40 G = 21213965311727710744090135363827269632  S_cap = 21213985542941577671914865369220644864  lists L = 5057803466731956182501348343808  pad bound 255 L = 1289739884016648826537843827671040
r = 41328941784374359033570814416443766  R = 41328941785268531492211003827071250  cap R + 2^100 + 255 L = 42619949319885408548150344357947666
  setup, G S_g (Section 6.5): 132,356,406,391,353,953,446,737,044,479,447,515,539
  FES pass A, G * 5 (F_A + 2^24 * 2 * 12): 2,068,390,288,656,613,528,876,608,001,190,022,767,180
  FES pass B, G * 5 (F_B + 2^24 * 2 * 11): 2,081,645,779,981,935,229,803,888,369,345,911,845,475
  FES block control, G * 2 * 2^24 * 8: 5,179,190,749,933,523,130,881,380,704,059,392
  filter test, G 2^40 (17 + 18): 742,488,785,910,469,876,043,154,737,733,954,437,120
  extraction, G 2^40 * 4 + 12 (S_cap + 2^38): 339,423,687,762,209,775,039,338,929,184,491,700,224
  batch kernel, ceil((S_cap + 255 L)/256) K_B: 3,992,781,105,963,035,681,145,784,401,580,733,829,120
  lists, L (K_blk + 24 + 513 + 3): 16,119,219,648,474,744,353,631,797,171,716,096
  tag passes, 2820 (R + 2^100 + 255 L): 120,188,257,082,076,852,105,783,971,089,412,418,120
  ONCE: 1,180,591,620,717,411,303,440
N = 9,477,295,610,158,093,305,909,371,588,499,261,591,706
N = 9477295610158093305909371588499261591706
certificate 1626^100000 * 2^12213255 <= N^100000 < 1626^100000 * 2^12213256   claim 122.13256
log2(N/1626) = 122.132559596724019079442014830650140342090143630320377636348  N per message Q = 1.74510919732266725698645909874563347536541000960227335428200
failure sum < 61/100: True  G least: True
success > 0.390000000000000000000000017073340414899774259646577065486508
  failure term no duplicate coset: C(C, 2) 2^-280                   6.279068e-30
  failure term no full collision among survivors: 1/T40             6.080616e-01
  failure term slack of that bound: 2^-100                          7.888609e-31
  failure term key matches (Chebyshev): 1/kappa                     5.169062e-14
  failure term bad triples (Markov): Q(Q-1)(Q-2)/2^405              1.938372e-03
  failure term tag events Z (Markov): (S_cap + 255 L)/2^228         4.918239e-32
  failure term tag at the detecting key: 2^-128                     2.938736e-39
  failure term survivor count above S_cap (Chebyshev)               5.182961e-26
  failure term a list over capacity: L 2^-300                       2.482923e-60
failure sum = 0.609999999999999999999999982926659585100225740353422934513492
| eps | success at this N | least G | N at that G | E | time_log2 | extra |
| 0.01 | > 0.386967 | 19,392,141,617,293,258,998,012,002 | 9,526,104,497,730,635,322,705,212,351,144,083,185,936 | 12,213,998 | 122.13998 | 0.00742 |
| 0.05 | > 0.374685 | 19,800,340,687,090,852,486,370,883 | 9,729,156,701,265,196,678,518,943,167,820,880,862,350 | 12,217,040 | 122.17040 | 0.03784 |
| 0.1 | > 0.358985 | 20,348,933,684,837,214,985,025,430 | 10,002,209,988,811,213,955,704,598,344,930,212,147,188 | 12,221,034 | 122.21034 | 0.07778 |
| 0.25 | > 0.309471 | 22,317,875,662,332,828,497,064,510 | 10,983,770,912,008,581,606,441,003,450,386,460,289,448 | 12,234,539 | 122.34539 | 0.21283 |
address and size checks: slots below 2^127 + 2^126: True  slots written below 2^125: True  work words 35185648762 < 2^36: True  instructions 333414934998421 < 2^50: True  generation 19430378059520336 < 2^56: True
gain over the filed N (bits): 0.072832020527048239322099965166713466411482024297938921134  N < N_FILED: True
```

## Appendix C. The batch kernel: generator, executed counts

Run `python -B kernel_report.py 30 12` with the files below in one folder (w40.txt is the list of Section 3, one 80-digit
hexadecimal number per line, most significant digit first). The program builds the kernel for 2^30-point list blocks,
prints its instruction counts and executes it on 12,288 survivors (Section 5.7). The files kern.py, tr.py, trsearch.py,
kernel2.py, sched.py, run.py and run2.py build and execute it; ref.py is the reference Keccak.

#### ref.py (2430 bytes, SHA-256 4873e159bc5257d5e4186db58f782958346069722c386c7bf3964c48ab3438fc)

```python
"""Reference Keccak-f[1600] (rounds 0..r-1), message map M(t) = U || 0^40 || U || 0^15 and the vectors w_0..w_39 (file w40.txt:
proof.md Section 3, one 80-digit hexadecimal number per word, most significant digit first)."""
import hashlib, random, pathlib

M64 = (1 << 64) - 1
RC = (0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000, 0x000000000000808B,
      0x0000000080000001, 0x8000000080008081, 0x8000000000008009, 0x000000000000008A, 0x0000000000000088,
      0x0000000080008009, 0x000000008000000A, 0x000000008000808B, 0x800000000000008B, 0x8000000000008089,
      0x8000000000008003, 0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
      0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008)
RHO = (0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39, 41, 45, 15, 21, 8, 18, 2, 61, 56, 14)
HERE = pathlib.Path(__file__).resolve().parent
W40 = [int(h, 16) for h in (HERE / 'w40.txt').read_text().split()]
KAT = ((0, '75f9117eb56131a655b34d93115a9781b7899716653c9b79f80902a99e3399f6'),
       (W40[0] ^ W40[39], 'f3025c162a37654390d8b807a6970cbae2a22b8e745218666f323f572066b8f2'))


def keccak_f(L, rounds, want_b=False):
    L = list(L)
    b = None
    for r in range(rounds):
        C = [L[x] ^ L[x + 5] ^ L[x + 10] ^ L[x + 15] ^ L[x + 20] for x in range(5)]
        D = [C[x - 1] ^ ((C[(x + 1) % 5] << 1 | C[(x + 1) % 5] >> 63) & M64) for x in range(5)]
        B = [0] * 25
        for i in range(25):
            x, y, s = i % 5, i // 5, RHO[i]
            v = L[i] ^ D[x]
            B[y + 5 * ((2 * x + 3 * y) % 5)] = (v << s | v >> (64 - s)) & M64
        if r == rounds - 1:
            b = B[0:5]
        L = [B[i] ^ (~B[i - i % 5 + (i + 1) % 5] & B[i - i % 5 + (i + 2) % 5]) for i in range(25)]
        L[0] ^= RC[r]
    return (L, b) if want_b else L


def sha3_256(msg, rounds=6):
    p = bytearray(msg) + b'\x06'
    p += bytes(-len(p) % 136)
    p[-1] |= 0x80
    L = [0] * 25
    for o in range(0, len(p), 136):
        for k in range(17):
            L[k] ^= int.from_bytes(p[o + 8 * k:o + 8 * k + 8], 'little')
        L = keccak_f(L, rounds)
    return b''.join(v.to_bytes(8, 'little') for v in L[:4])


def message(t):
    u = t.to_bytes(40, 'little')
    return u + bytes(40) + u + bytes(15)


def lanes(t):
    u = [(t >> 64 * k) & M64 for k in range(5)]
    return u + [0] * 5 + u + [0, 0x86 << 56] + [0] * 8
```

#### kern.py (5715 bytes, SHA-256 d9f8fd12e241510c7d73a285b0f3775d83c8c5c7d4f235e249b4e9149c067b34)

```python
"""Graph builder for the batch survivor kernel (rounds 0-5 + chi6 cone), polarity-tracked bit-sliced Keccak.
Word = 256 lanes.  Node ops: IN (fixed memory word), INP (memory word at P+imm), MOVI, XOR, AND, OR, NOT, XORI, ANDI, SHL, SHR.
Value = (node, pol): true value = stored(node) ^ pol*ONES ; node None = constant (pol = 0/1)."""
import sys, itertools
sys.dont_write_bytecode = True
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ref
RHO = ref.RHO
RC = ref.RC
ONES = (1 << 256) - 1


class Graph:
    def __init__(s):
        s.op = []; s.a = []; s.b = []; s.imm = []; s.S = []
        s.cse = {}
    def new(s, op, a=None, b=None, imm=None, S=None):
        n = len(s.op)
        s.op.append(op); s.a.append(a); s.b.append(b); s.imm.append(imm)
        s.S.append(S if S is not None else frozenset([n]))
        return n
    def xv(s, va, vb):
        na, pa = va; nb, pb = vb; p = pa ^ pb
        if na is None: return (nb, p)
        if nb is None: return (na, p)
        S = s.S[na] ^ s.S[nb]
        if not S: return (None, p)
        n = s.cse.get(S)
        if n is None:
            n = s.new('XOR', na, nb, S=S); s.cse[S] = n
        return (n, p)


def an_simple(g, flipc, b1, b2):
    """true value (~b1) & b2 ; local choices only"""
    (n1, p1), (n2, p2) = b1, b2
    if n2 is None:
        if p2 == 0: return (None, 0)
        return (n1, p1 ^ 1)
    if n1 is None:
        return (None, 0) if p1 == 1 else (n2, p2)
    if n1 == n2:
        if p1 == p2: return (None, 0)
        return (n1, 1) if (p1, p2) == (0, 1) else (n1, 0)
    if (p1, p2) == (1, 0):
        return (g.new('AND', n1, n2), 0)
    if (p1, p2) == (0, 1):
        return (g.new('OR', n1, n2), 1)
    if (p1, p2) == (0, 0):
        u = g.new('OR', n1, n2)
        return g.xv((u, 0), (n1, 0))
    u = g.new('AND', n1, n2)                  # (1,1): s1 ^ (s1&s2)
    return g.xv((u, 0), (n1, 0))


import random as _random
TIE = {'rng': None}

def chi_row(g, bs, need, flipc, plan=True):
    """outputs o_i = b_i ^ (~b_{i+1} & b_{i+2}) for i in need ; bs = 5 Vals"""
    ok = all(v[0] is not None for v in bs) and len({v[0] for v in bs}) == 5
    if not ok or not plan:
        return {i: g.xv(bs[i], an_simple(g, flipc, bs[(i + 1) % 5], bs[(i + 2) % 5])) for i in need}
    pol = [v[1] for v in bs]
    cands = []
    for F in range(32):
        q = [pol[j] ^ ((F >> j) & 1) for j in range(5)]
        cost = bin(F).count('1') + sum(1 for i in need if q[(i + 1) % 5] == q[(i + 2) % 5])
        cands.append((cost, F))
    mc = min(c for c, _ in cands)
    opts = [F for c, F in cands if c == mc]
    F = opts[0] if TIE['rng'] is None else TIE['rng'].choice(opts)
    use = list(bs)
    for j in range(5):
        if (F >> j) & 1:
            n, p = bs[j]
            f = flipc.get(n)
            if f is None:
                f = g.new('NOT', n); flipc[n] = f
            use[j] = (f, p ^ 1)
    return {i: g.xv(bs[i], an_simple(g, flipc, use[(i + 1) % 5], use[(i + 2) % 5])) for i in need}


def build_rounds(g, planes, plan=True, last_need=(0, 1, 2, 3), nz=35, rounds=6, full_need=(0, 1, 2, 3, 4)):
    """planes: list of 320 Vals, plane 64*x+z = bit z of u_x.  returns key Vals [(x,z)]"""
    Z = (None, 0)
    A = [[Z] * 64 for _ in range(25)]
    for x in range(5):
        for z in range(64):
            A[x][z] = planes[64 * x + z]; A[x + 10][z] = planes[64 * x + z]
    for z in (57, 58, 63): A[16][z] = (None, 1)
    flipc = {}
    X = g.xv
    for r in range(rounds):
        C = [[None] * 64 for _ in range(5)]
        for z in range(64):
            for x in range(5):
                v = A[x][z]
                for y in range(1, 5): v = X(v, A[x + 5 * y][z])
                C[x][z] = v
        D = [[X(C[(x - 1) % 5][z], C[(x + 1) % 5][(z - 1) % 64]) for z in range(64)] for x in range(5)]
        B = [[Z] * 64 for _ in range(25)]
        for z in range(64):
            for i in range(25):
                x, y = i % 5, i // 5
                B[y + 5 * ((2 * x + 3 * y) % 5)][(z + RHO[i]) % 64] = X(A[i][z], D[x][z])
        if r == rounds - 1:
            Bf = B; break
        A2 = [[Z] * 64 for _ in range(25)]
        for z in range(64):
            for row in range(0, 25, 5):
                o = chi_row(g, [B[row + k][z] for k in range(5)], full_need, flipc, plan)
                for k in range(5): A2[row + k][z] = o[k]
        for z in range(64):
            if (RC[r] >> z) & 1:
                n, p = A2[0][z]; A2[0][z] = (n, p ^ 1)
        A = A2
    keys = {}
    for z in range(nz):
        o = chi_row(g, [Bf[k][z] for k in range(5)], list(last_need), flipc, plan)
        for x in last_need: keys[(x, z)] = o[x]
    return keys


def live_nodes(g, outs):
    seen = set(); st = [n for n in outs if n is not None]
    while st:
        n = st.pop()
        if n in seen: continue
        seen.add(n)
        for c in (g.a[n], g.b[n]):
            if c is not None: st.append(c)
    return seen


def evaluate(g, vals, order=None):
    """vals: dict node->int for IN-like nodes ; evaluates every node in creation order (children have lower ids)"""
    v = {}
    for n in range(len(g.op)):
        op = g.op[n]
        if n in vals: v[n] = vals[n]; continue
        a = g.a[n]; b = g.b[n]
        if op == 'XOR': v[n] = v[a] ^ v[b]
        elif op == 'AND': v[n] = v[a] & v[b]
        elif op == 'OR': v[n] = v[a] | v[b]
        elif op == 'NOT': v[n] = v[a] ^ ONES
        elif op == 'XORI': v[n] = v[a] ^ g.imm[n]
        elif op == 'ANDI': v[n] = v[a] & g.imm[n]
        elif op == 'SHL': v[n] = (v[a] << g.imm[n]) & ONES
        elif op == 'SHR': v[n] = v[a] >> g.imm[n]
        elif op == 'MOVI': v[n] = g.imm[n]
        else: raise Exception(op)
    return v
```

#### tr.py (3244 bytes, SHA-256 9e51f7b6c01368b670ff6a6b1e5c94818880a41191c99a8f2dd2ece74b5647ee)

```python
"""Butterfly bit-matrix transpose on 256-bit words with known-zero mask tracking (exact bit-level folding)."""
import sys
sys.dont_write_bytecode = True
from kern import ONES

def msk(s):
    m = 0
    for c in range(256):
        if not (c & s): m |= 1 << c
    return m
MASKS = {1 << b: msk(1 << b) for b in range(8)}

class Tr:
    def __init__(s, g):
        s.g = g
    # a word is (node, mask) ; node None => zero
    def shr(s, w, k):
        n, m = w; m2 = m >> k
        if n is None or not m2: return (None, 0)
        return (s.g.new('SHR', n, imm=k), m2)
    def shl(s, w, k):
        n, m = w; m2 = (m << k) & ONES
        if n is None or not m2: return (None, 0)
        return (s.g.new('SHL', n, imm=k), m2)
    def andi(s, w, k):
        n, m = w; m2 = m & k
        if n is None or not m2: return (None, 0)
        if m2 == m: return w
        return (s.g.new('ANDI', n, imm=k), m2)
    def xor(s, a, b):
        if a[0] is None: return b
        if b[0] is None: return a
        return (s.g.new('XOR', a[0], b[0]), a[1] | b[1])
    def pairX(s, Ak, Ad, sh):
        M = MASKS[sh]
        t = s.andi(s.xor(s.shr(Ak, sh), Ad), M)
        if t[0] is None: return Ak, Ad
        return s.xor(Ak, s.shl(t, sh)), s.xor(Ad, t)
    def pairD(s, Ak, Ad, sh):
        M = MASKS[sh]; H = (M << sh) & ONES
        a1 = s.andi(Ak, ONES ^ H); a2 = s.shl(s.andi(Ad, M), sh)
        d1 = s.andi(Ad, ONES ^ M); d2 = s.andi(s.shr(Ak, sh), M)
        return s.xor(a1, a2), s.xor(d1, d2)
    def pair(s, Ak, Ad, sh):
        g = s.g
        n0 = len(g.op)
        r1 = s.pairX(Ak, Ad, sh); c1 = len(g.op) - n0
        del_ = lambda: [lst.__delitem__(slice(n0, None)) for lst in (g.op, g.a, g.b, g.imm, g.S)]
        del_()
        r2 = s.pairD(Ak, Ad, sh); c2 = len(g.op) - n0
        del_()
        # NOTE: counts are of built nodes (incl. nodes later dead); choose cheaper then rebuild for real
        return (s.pairX if c1 <= c2 else s.pairD)(Ak, Ad, sh)
    def transpose(s, rows, order=(0, 1, 2, 3, 4, 5, 6, 7), blocked=True):
        """rows: 256 words; returns new rows with new[j] bit r = rows[r] bit j. 'order' = stage bit order."""
        R = list(rows)
        def stage(b, lo=0, hi=256):
            d = 1 << b
            for k in range(lo, hi):
                if not (k & d):
                    R[k], R[k + d] = s.pair(R[k], R[k + d], d)
        if blocked:
            low = [b for b in order if b < 6]
            for blk in range(4):
                for b in low: stage(b, 64 * blk, 64 * blk + 64)
            for b in order:
                if b >= 6: stage(b)
        else:
            for b in order: stage(b)
        return R

if __name__ == '__main__':
    import random
    from kern import Graph, evaluate
    g = Graph(); T = Tr(g)
    rng = random.Random(1)
    rows_in = [rng.getrandbits(40) for _ in range(256)]
    rows = [(g.new('IN', imm=('M', r)), (1 << 40) - 1) for r in range(256)]
    out = T.transpose(rows)
    vals = {rows[r][0]: rows_in[r] for r in range(256)}
    v = evaluate(g, vals)
    ok = True
    for j in range(40):
        exp = 0
        for r in range(256):
            if (rows_in[r] >> j) & 1: exp |= 1 << r
        n, m = out[j]
        ok &= (v[n] == exp)
    print('transpose ok', ok)
```

#### trsearch.py (1898 bytes, SHA-256 63707b781205433da4c9047ad027f25def84424770091cd871664b14afcf1959)

```python
import sys, random, itertools, time
sys.dont_write_bytecode = True
from kern import Graph, live_nodes, ONES
from tr import Tr

def tr_count(masks, sig, wanted):
    """masks: list of 256 initial masks (0 = zero row); sig = stage bit order; returns live ALU op count for wanted output rows"""
    g = Graph(); T = Tr(g)
    R = [(g.new('IN', imm=('M', r)), m) if m else (None, 0) for r, m in enumerate(masks)]
    for b in sig:
        d = 1 << b
        for k in range(256):
            if not (k & d):
                R[k], R[k + d] = T.pair(R[k], R[k + d], d)
    outs = [R[j][0] for j in wanted if R[j][0] is not None]
    live = live_nodes(g, outs)
    return sum(1 for n in live if g.op[n] != 'IN')

def search(masks, wanted, iters=300, seed=1, start=None):
    rng = random.Random(seed)
    sig = list(start or range(8))
    best = tr_count(masks, sig, wanted); bs = list(sig)
    cur = best; cs = list(sig)
    for it in range(iters):
        s = list(cs)
        i, j = rng.sample(range(8), 2); s[i], s[j] = s[j], s[i]
        c = tr_count(masks, s, wanted)
        if c <= cur:
            cur, cs = c, s
            if c < best: best, bs = c, list(s)
    return best, bs

if __name__ == '__main__':
    which = sys.argv[1]
    t0 = time.time()
    if which == 'u':
        for B in (16, 20, 24, 32, 40):
            masks = [(1 << B) - 1] * 256
            base = tr_count(masks, list(range(8)), list(range(B)))
            best, bs = search(masks, list(range(B)), iters=150)
            print('B', B, 'identity', base, 'best', best, bs, '%.0fs' % (time.time() - t0), flush=True)
    else:
        masks = [ONES if r < 140 else 0 for r in range(256)]
        masks[143] = ONES
        base = tr_count(masks, list(range(8)), list(range(256)))
        best, bs = search(masks, list(range(256)), iters=150)
        print('out identity', base, 'best', best, bs, '%.0fs' % (time.time() - t0))
```

#### kernel2.py (5096 bytes, SHA-256 3d51bf885866b62da92ea27447137a6ff070fbfc18949f8e52545df328c97ab0)

```python
"""Streaming build of the batch survivor kernel (slice-pipelined rounds, depth-first butterfly transposes)."""
import sys, time
sys.dont_write_bytecode = True
from kern import *
from kern import chi_row
from tr import Tr, MASKS
import sched

W40 = ref.W40


class StreamTr:
    """incremental depth-first butterfly transpose.  Rows are fed in increasing VIRTUAL index v; virtual bit m is actual row bit sig[m]
    (stage m exchanges row bit sig[m] with column bit sig[m]).  f(v) = actual row index."""
    def __init__(s, T, probe_cb=None, sig=None):
        s.T = T; s.stack = []; s.probe_cb = probe_cb; s.sig = list(sig or range(8)); s.nfed = 0
    def f(s, v):
        r = 0
        for m in range(8):
            if (v >> m) & 1: r |= 1 << s.sig[m]
        return r
    def feed(s, w):
        grp = [w]; m = 0
        s.nfed += 1
        while s.stack and s.stack[-1][0] == m:
            _, left = s.stack.pop()
            grp = s.merge(left, grp, m)
            m += 1
        s.stack.append((m, grp))
    def merge(s, left, right, m):
        d = 1 << m; sh = 1 << s.sig[m]
        last = (m == 7)
        for k in range(d):
            left[k], right[k] = s.T.pair(left[k], right[k], sh)
            if last and s.probe_cb:
                s.probe_cb(s.f(k), left[k]); s.probe_cb(s.f(k + d), right[k])
        return left + right
    def result(s):
        """list indexed by actual row"""
        grp = s.stack[0][1]
        out = [None] * 256
        for v in range(256): out[s.f(v)] = grp[v]
        return out


class Theta:
    def __init__(s, g):
        s.g = g; s.b = [[None] * 64 for _ in range(25)]; s.Cprev = None; s.pend = None
    def _C(s, A):
        X = s.g.xv; C = []
        for x in range(5):
            v = A[x]
            for y in range(1, 5): v = X(v, A[x + 5 * y])
            C.append(v)
        return C
    def _emit(s, z, A, C, Cm1):
        X = s.g.xv
        D = [X(C[(x - 1) % 5], Cm1[(x + 1) % 5]) for x in range(5)]
        for i in range(25):
            x, y = i % 5, i // 5
            s.b[y + 5 * ((2 * x + 3 * y) % 5)][(z + RHO[i]) % 64] = X(A[i], D[x])
    def push(s, z, A):
        C = s._C(A)
        if z == 0:
            s.pend = (A, C)
        else:
            s._emit(z, A, C, s.Cprev)
        s.Cprev = C
    def finish(s):
        A, C = s.pend
        s._emit(0, A, C, s.Cprev)


def build(B=40, plan=True, variant='u', sig_in=None, sig_out=None, nz=35, z0=0):
    g = Graph(); T = Tr(g)
    Zv = (None, 0)
    # ---- u transpose
    st = StreamTr(T, sig=sig_in)
    mskB = (1 << B) - 1
    for v in range(256):
        st.feed((g.new('INP', imm=st.f(v)), mskB))
    iw = st.result()
    g.m_u = len(g.op)
    ipl = [(iw[b][0], 0) for b in range(B)]
    u = [g.xv(ipl[b], ipl[b + 1]) for b in range(B - 1)] + [ipl[B - 1]]
    planes = {}
    def getp(k):
        p = planes.get(k)
        if p is None:
            v = (None, 0)
            for b in range(B):
                if (W40[b] >> k) & 1: v = g.xv(v, u[b])
            m = (g.new('IN', imm=('M', k)), 0)
            p = g.xv(v, m); planes[k] = p
        return p
    flipc = {}
    full = (0, 1, 2, 3, 4)
    # ---- round 0 theta
    th = Theta(g)
    for z in range(64):
        A = [Zv] * 25
        for x in range(5):
            A[x] = getp(64 * x + z); A[x + 10] = A[x]
        if z in (57, 58, 63): A[16] = (None, 1)
        th.push(z, A)
    th.finish(); bcur = th.b
    for r in range(5):
        th = Theta(g)
        for z in range(64):
            A = [None] * 25
            for row in range(0, 25, 5):
                o = chi_row(g, [bcur[row + k][z] for k in range(5)], full, flipc, plan)
                for k in range(5): A[row + k] = o[k]
            if (RC[r] >> z) & 1:
                n, p = A[0]; A[0] = (n, p ^ 1)
            th.push(z, A)
        th.finish(); bcur = th.b
    # ---- final chi (row 0, slices < nz) + out transpose
    g.m_k = len(g.op)
    probes = []
    def probe_cb(c, w):
        probes.append(g.new('PROBE', w[0], imm=c))
    stt = StreamTr(T, probe_cb=probe_cb)
    pattern = 0
    for z in range(z0, nz):
        o = chi_row(g, [bcur[k][z] for k in range(5)], [0, 1, 2, 3], flipc, plan)
        for x in range(4):
            n, p = o[x]
            r = 4 * (z - z0) + x
            if p: pattern |= 1 << r
            stt.feed((n, ONES))
    g.m_f = len(g.op)
    for r in range(4 * (nz - z0), 256):
        if r == 143: stt.feed((g.new('MOVI', imm=ONES), ONES))
        else: stt.feed((None, 0))
    return g, probes, pattern


def make_order(g, outs):
    live = live_nodes(g, outs)
    leaf = ('IN', 'INP', 'MOVI')
    return [n for n in sorted(live) if g.op[n] not in leaf]


if __name__ == '__main__':
    B = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    t0 = time.time()
    g, outs, pat = build(B)
    order = make_order(g, outs)
    from collections import Counter
    c = Counter(g.op[n] for n in order)
    print('B', B, 'live non-leaf', len(order), dict(c), 'build %.1fs' % (time.time() - t0))
    prog, st = sched.allocate(g, order)
    print(st, 'total instrs', len(prog), 'per surv %.2f' % (len(prog) / 256))
```

#### sched.py (4987 bytes, SHA-256 67e51838be09190e94d57c70430e6eb586db66d198a75a1ef9f281852dddc948)

```python
"""Register allocation (Belady, 64 registers minus 4 reserved) -> explicit instruction list.
Leaves: IN (LDI, 1 op), INP (ADD+LD, 2 ops), MOVI (1 op).  Spills: STORE once per value evicted with a future use, reload 1 op."""
import sys
sys.dont_write_bytecode = True
INF = 1 << 60
RES_P, RES_VB, RES_T1, RES_T2 = 0, 1, 2, 3
FIRST = 4
MBASE = 1 << 20      # per-block mask planes
SPILL = 1 << 24
BND = 1 << 26        # per-block hoisted (batch-uniform) nodes


def addr_of_in(imm):
    kind, k = imm
    if kind == 'M': return MBASE + k
    raise Exception(imm)


CLEAN_BONUS = 0

def allocate(g, order, nreg=64, make_prog=True, leafaddr=None, must_store=None, gen_in=False):
    """order: execution order of nodes (non-leaf; IN nodes included only with gen_in).  returns (prog, stats)"""
    leafaddr = leafaddr or {}
    must_store = must_store or {}
    uses = {}
    for i, n in enumerate(order):
        for c in (g.a[n], g.b[n]):
            if c is not None: uses.setdefault(c, []).append(i)
    ptr = {n: 0 for n in uses}
    def nxt(n, i):
        u = uses.get(n)
        if u is None: return INF
        p = ptr[n]
        while p < len(u) and u[p] < i: p += 1
        ptr[n] = p
        return u[p] if p < len(u) else INF
    regs = {}
    free = list(range(nreg - 1, FIRST - 1, -1))
    inmem = set()
    prog = []
    st = {'LOAD': 0, 'STORE': 0, 'ALU': 0, 'ADDR': 0, 'PROBE': 0}
    emit = prog.append if make_prog else (lambda x: None)
    def is_leaf(n):
        op = g.op[n]
        return n in leafaddr or op in ('INP', 'MOVI') or (op == 'IN' and not gen_in)
    def get_reg(i, excl):
        if free: return free.pop()
        best = None; bn = None
        for n, r in regs.items():
            if n in excl: continue
            nu = nxt(n, i)
            sc = nu + (CLEAN_BONUS if (n in inmem or is_leaf(n)) and nu < INF else 0)
            if best is None or sc > best: best = sc; bn = n
        r = regs.pop(bn)
        best = nxt(bn, i)
        if best < INF and bn not in inmem and not is_leaf(bn):
            emit(('STI', must_store.get(bn, SPILL + bn), r)); st['STORE'] += 1; inmem.add(bn)
        return r
    def load(n, i, excl):
        r = get_reg(i, excl)
        op = g.op[n]
        if n in leafaddr:
            emit(('LDI', r, leafaddr[n])); st['LOAD'] += 1
        elif not is_leaf(n):
            assert n in inmem, ('reload of unsaved', n, op)
            emit(('LDI', r, must_store.get(n, SPILL + n))); st['LOAD'] += 1
        elif op == 'IN':
            emit(('LDI', r, addr_of_in(g.imm[n]))); st['LOAD'] += 1
        elif op == 'INP':
            emit(('ADDI', RES_T1, RES_P, g.imm[n])); emit(('LD', r, RES_T1)); st['LOAD'] += 1; st['ADDR'] += 1
        else:
            emit(('MOVI', r, g.imm[n])); st['ALU'] += 1
        regs[n] = r
        return r
    for i, n in enumerate(order):
        a, b = g.a[n], g.b[n]
        ra = regs.get(a) if a is not None else None
        excl = {a, b}
        if a is not None and ra is None: ra = load(a, i, excl)
        rb = None
        if b is not None:
            rb = regs.get(b)
            if rb is None: rb = load(b, i, excl)
        for c in (a, b):
            if c is not None and c in regs and nxt(c, i + 1) == INF:
                free.append(regs.pop(c))
        op = g.op[n]
        if op == 'PROBE':
            c = g.imm[n]
            emit(('ADDI', RES_T2, RES_VB, c))          # v = PT + c = TAG + P + c   (id = tag + survivor slot address)
            emit(('LD', RES_T1, ra)); emit(('XOR', RES_T1, RES_T1, RES_T2)); emit(('SHRI', RES_T1, RES_T1, 128))
            emit(('BRNZ', RES_T1)); emit(('ST', ra, RES_T2))
            st['PROBE'] += 6
            continue
        rd = get_reg(i + 1, set(x for x in (a, b) if x is not None and x in regs))
        if op == 'IN' and gen_in:        # per-block broadcast of bit k of the scalar base (words in RES_P, RES_VB; zero in RES_T2)
            k = g.imm[n][1]
            src = RES_P if k < 256 else RES_VB
            kk = k if k < 256 else k - 256
            emit(('SHLI', RES_T1, src, 255 - kk)); emit(('SHRI', RES_T1, RES_T1, 255)); emit(('SUB', rd, RES_T2, RES_T1))
            st['ALU'] += 3
        else:
            if op == 'XOR': emit(('XOR', rd, ra, rb))
            elif op == 'AND': emit(('AND', rd, ra, rb))
            elif op == 'OR': emit(('OR', rd, ra, rb))
            elif op == 'NOT': emit(('NOT', rd, ra))
            elif op == 'XORI': emit(('XORI', rd, ra, g.imm[n]))
            elif op == 'ANDI': emit(('ANDI', rd, ra, g.imm[n]))
            elif op == 'SHL': emit(('SHLI', rd, ra, g.imm[n]))
            elif op == 'SHR': emit(('SHRI', rd, ra, g.imm[n]))
            else: raise Exception(op)
            st['ALU'] += 1
        regs[n] = rd
        if n in must_store:
            emit(('STI', must_store[n], rd)); st['STORE'] += 1; inmem.add(n)
            if nxt(n, i + 1) == INF: free.append(regs.pop(n))
        elif nxt(n, i + 1) == INF:
            raise Exception('dead result')
    return prog, st
```

#### run.py (3910 bytes, SHA-256 50b4e9f43b799d2f4bdad85ef4646c8cc23ee51410cbf71a4f95a9fb7171ceb2)

```python
"""Execute the generated straight-line batch program on 256-bit words, count executed ops, check keys against ref.py."""
import sys, random, time, json
sys.dont_write_bytecode = True
from kern import ref, ONES
import kernel2, sched
from collections import Counter
M = ONES
W40 = ref.W40
TAGADDR = 1 << 22
END = 1 << 40

def gray(i): return i ^ (i >> 1)

def msg(t, i):
    u = gray(i); m = t
    for b in range(40):
        if (u >> b) & 1: m ^= W40[b]
    return m

def keyword(m):
    L = ref.keccak_f(ref.lanes(m), 6)
    w = 0
    for z in range(35):
        for x in range(4):
            kb = ((L[x] >> z) & 1) ^ (1 if (x == 0 and (ref.RC[5] >> z) & 1) else 0)
            if kb: w |= 1 << (4 * z + x)
    return w | (1 << 143)

def execute(prog, R, mem, cnt):
    GARB = (1 << 255) | 12345
    for ins in prog:
        o = ins[0]; cnt[o] += 1
        if o == 'XOR': R[ins[1]] = R[ins[2]] ^ R[ins[3]]
        elif o == 'AND': R[ins[1]] = R[ins[2]] & R[ins[3]]
        elif o == 'OR': R[ins[1]] = R[ins[2]] | R[ins[3]]
        elif o == 'NOT': R[ins[1]] = R[ins[2]] ^ M
        elif o == 'XORI': R[ins[1]] = R[ins[2]] ^ ins[3]
        elif o == 'ANDI': R[ins[1]] = R[ins[2]] & ins[3]
        elif o == 'SHLI': R[ins[1]] = (R[ins[2]] << ins[3]) & M
        elif o == 'SHRI': R[ins[1]] = R[ins[2]] >> ins[3]
        elif o == 'LDI': R[ins[1]] = mem[ins[2]]
        elif o == 'LD': R[ins[1]] = mem.get(R[ins[2]], GARB)
        elif o == 'STI': mem[ins[1]] = R[ins[2]]
        elif o == 'ST': mem[R[ins[1]]] = R[ins[2]]
        elif o == 'ADDI': R[ins[1]] = (R[ins[2]] + ins[3]) & M
        elif o == 'ADD': R[ins[1]] = (R[ins[2]] + R[ins[3]]) & M
        elif o == 'SUB': R[ins[1]] = (R[ins[2]] - R[ins[3]]) & M
        elif o == 'MOVI': R[ins[1]] = ins[2]
        elif o == 'BRNZ':
            if R[ins[1]] == 0: cnt['BRNZ_zero'] += 1
        elif o == 'BRX': pass
        else: raise Exception(o)

def validate(prog, pattern, B, nbatch, seed=1):
    rng = random.Random(seed)
    TAG = 0xABCDEF123456789 << 128
    mem = {TAGADDR: TAG}
    cnt = Counter()
    bad = 0; nsurv = 0
    for bi in range(nbatch):
        t = rng.getrandbits(320)
        I = rng.getrandbits(40 - B) if B < 40 else 0
        lo = rng.sample(range(1 << B), 256) if B >= 9 else [rng.getrandbits(B) for _ in range(256)]
        if bi == 0: lo[0] = 0
        if bi == 1: lo[0] = (1 << B) - 1
        ids = [(I << B) | l for l in lo]
        base = msg(t, I << B)
        P = (1 << 30) + 256 * bi
        for c in range(256): mem[P + c] = lo[c]
        for k in range(320): mem[sched.MBASE + k] = M if (base >> k) & 1 else 0
        R = [0] * 64; R[sched.RES_P] = P
        # prologue: PT = P + TAG
        execute([('LDI', sched.RES_T1, TAGADDR), ('ADD', sched.RES_VB, sched.RES_P, sched.RES_T1)], R, mem, cnt)
        execute(prog, R, mem, cnt)
        # epilogue (loop control)
        execute([('ADDI', sched.RES_P, sched.RES_P, 256), ('SUB', sched.RES_T1, sched.RES_P, sched.RES_T2), ('BRX', sched.RES_T1)], R, mem, cnt)
        for c in range(256):
            m = msg(t, ids[c])
            kw = keyword(m) ^ pattern
            v = mem.get(kw)
            if v != TAG + P + c: bad += 1
            nsurv += 1
    return bad, nsurv, cnt

if __name__ == '__main__':
    B = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    nb = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    t0 = time.time()
    g, outs, pat = kernel2.build(B)
    order = kernel2.make_order(g, outs)
    prog, st = sched.allocate(g, order)
    print('B', B, 'prog len', len(prog), st, 'build+alloc %.1fs' % (time.time() - t0), flush=True)
    bad, ns, cnt = validate(prog, pat, B, nb)
    print('validated survivors', ns, 'bad', bad, 'misses(BRNZ nonzero) ok:', cnt['BRNZ_zero'], 'zero-branches', 'time %.1fs' % (time.time() - t0))
    tot = sum(cnt.values()) - cnt['BRNZ_zero']
    print('executed ops per batch', tot / nb, 'per survivor', tot / nb / 256)
```

#### run2.py (6960 bytes, SHA-256 d5fb59ef5f24f0dd86f3b34a9af77d6c496a3955e5d7d51b087e6718739f5c91)

```python
"""Batch kernel with per-block hoisting of batch-uniform nodes.  Executes: block prep (base message), block prelude (mask broadcast + uniform
nodes), then the batch kernel (u-transpose, planes, rounds, out-transpose, probes), counting every executed instruction."""
import sys, random, time, json
sys.dont_write_bytecode = True
from kern import ref, ONES, live_nodes
import kernel2, sched
from run import gray, msg, keyword, execute, W40, TAGADDR
from collections import Counter
M = ONES
LEAF = ('IN', 'INP', 'MOVI')
TB = 1 << 21          # byte tables of W40: TB + 512*b + 256*word + v
BASEADDR = 1 << 23
TADDR = 1 << 23 | 16  # coset origin words


def classify(g, outs):
    live = live_nodes(g, outs)
    uni = {}
    for n in sorted(live):
        op = g.op[n]
        if op in ('IN', 'MOVI'): uni[n] = True
        elif op in ('INP', 'PROBE'): uni[n] = False
        else: uni[n] = all(uni[c] for c in (g.a[n], g.b[n]) if c is not None)
    return live, uni


def split(g, outs, hoist=True):
    live, uni = classify(g, outs)
    if not hoist:
        order = [n for n in sorted(live) if g.op[n] not in LEAF]
        ins = sorted(n for n in live if g.op[n] == 'IN')
        return order, ins, {n: sched.MBASE + g.imm[n][1] for n in ins}, {}, {'mneed': len(ins)}
    batch = [n for n in sorted(live) if g.op[n] not in LEAF and not uni[n]]
    boundary = set(); mneed = set()
    for n in batch:
        for c in (g.a[n], g.b[n]):
            if c is None: continue
            if g.op[c] == 'IN': mneed.add(c)
            elif uni[c] and g.op[c] != 'MOVI': boundary.add(c)
    need = set(boundary); st = list(boundary)
    while st:
        n = st.pop()
        for c in (g.a[n], g.b[n]):
            if c is not None and uni[c] and g.op[c] != 'MOVI' and c not in need:
                need.add(c); st.append(c)
    ins = set()
    for n in need:
        for c in (g.a[n], g.b[n]):
            if c is not None and g.op[c] == 'IN': ins.add(c)
    pre = sorted(need | ins | mneed)
    must = {n: sched.BND + n for n in boundary}
    for n in mneed: must[n] = sched.MBASE + g.imm[n][1]
    leafaddr = {n: sched.BND + n for n in boundary}
    return batch, pre, must, leafaddr, {'boundary': len(boundary), 'mneed': len(mneed), 'uniform_alu': sum(1 for n in need)}


def block_prep_prog(B):
    """base = t ^ w(g(I<<B)) from memory words (t_lo, t_hi, I) -> BASEADDR, BASEADDR+1"""
    T1, T2 = sched.RES_T1, sched.RES_T2
    R_I, R_G, R_B0, R_B1, R_Q, R_A, R_X = 8, 9, 10, 11, 12, 13, 14
    p = [('LDI', R_I, TADDR + 2), ('SHLI', R_I, R_I, B), ('SHRI', R_G, R_I, 1), ('XOR', R_G, R_G, R_I),
         ('LDI', R_B0, TADDR), ('LDI', R_B1, TADDR + 1)]
    for b in range(5):
        if b == 0: p.append(('ANDI', R_Q, R_G, 255))
        else:
            p.append(('SHRI', R_Q, R_G, 8 * b)); p.append(('ANDI', R_Q, R_Q, 255))
        for w, R_B in ((0, R_B0), (1, R_B1)):
            p.append(('ADDI', R_A, R_Q, TB + 512 * b + 256 * w)); p.append(('LD', R_X, R_A)); p.append(('XOR', R_B, R_B, R_X))
    p.append(('STI', BASEADDR, R_B0)); p.append(('STI', BASEADDR + 1, R_B1))
    return p


def tables(mem):
    for b in range(5):
        for v in range(256):
            w0 = 0; w1 = 0
            for j in range(8):
                if (v >> j) & 1:
                    x = W40[8 * b + j]
                    w0 ^= x & ((1 << 256) - 1); w1 ^= x >> 256
            mem[TB + 512 * b + v] = w0; mem[TB + 512 * b + 256 + v] = w1


def validate(batch_prog, pre_prog, pattern, B, nblocks, nb_per_block, seed=1):
    rng = random.Random(seed)
    TAG = 0xABCDEF123456789 << 128
    mem = {TAGADDR: TAG}; tables(mem)
    cb = Counter(); cp = Counter(); cq = Counter(); cg = Counter()
    bad = 0; nsurv = 0; Pn = 0
    prep = block_prep_prog(B)
    for bl in range(nblocks):
        t = rng.getrandbits(320)
        I = rng.getrandbits(40 - B) if B < 40 else 0
        mem[TADDR] = t & ((1 << 256) - 1); mem[TADDR + 1] = t >> 256; mem[TADDR + 2] = I
        R = [0] * 64
        execute(prep, R, mem, cq)
        base_chk = t ^ 0
        # prelude: load base words, zero
        R = [0] * 64
        execute([('LDI', sched.RES_P, BASEADDR), ('LDI', sched.RES_VB, BASEADDR + 1), ('MOVI', sched.RES_T2, 0)] if False else
                [('LDI', sched.RES_P, BASEADDR), ('LDI', sched.RES_VB, BASEADDR + 1), ('MOVI', sched.RES_T2, 0)], R, mem, cp)
        execute(pre_prog, R, mem, cp)
        for bi in range(nb_per_block):
            lo = rng.sample(range(1 << B), 256) if B >= 9 else [rng.getrandbits(B) for _ in range(256)]
            if bl == 0 and bi == 0: lo[0] = 0
            if bl == 1 and bi == 0: lo[0] = (1 << B) - 1
            ids = [(I << B) | l for l in lo]
            P = (1 << 30) + 256 * Pn; Pn += 1
            Rg = [0] * 64; Rg[20] = P            # gather executed as real instructions: MOVI imm; ST [p]; ADDI p
            for c in range(256):
                execute([('MOVI', 21, lo[c]), ('ST', 20, 21), ('ADDI', 20, 20, 1)], Rg, mem, cg)
            R = [0] * 64; R[sched.RES_P] = P
            execute([('LDI', sched.RES_T1, TAGADDR), ('ADD', sched.RES_VB, sched.RES_P, sched.RES_T1)], R, mem, cb)
            execute(batch_prog, R, mem, cb)
            execute([('ADDI', sched.RES_P, sched.RES_P, 256), ('SUB', sched.RES_T1, sched.RES_P, sched.RES_T2), ('BRX', sched.RES_T1)], R, mem, cb)
            for c in range(256):
                kw = keyword(msg(t, ids[c])) ^ pattern
                if mem.get(kw) != TAG + P + c: bad += 1
                nsurv += 1
    return bad, nsurv, cb, cp, cq, cg


def tot(c): return sum(v for k, v in c.items() if k != 'BRNZ_zero')

def make(B, sig_in=None, hoist=True, nreg=64, plan=True, z0=0):
    g, outs, pat = kernel2.build(B, plan=plan, sig_in=sig_in, z0=z0)
    batch, pre, must, leafaddr, info = split(g, outs, hoist)
    bprog, bst = sched.allocate(g, batch, nreg=nreg, leafaddr=leafaddr)
    pprog, pst = sched.allocate(g, pre, nreg=nreg, must_store=must, gen_in=True)
    return g, bprog, bst, pprog, pst, pat, info


if __name__ == '__main__':
    B = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    hoist = (sys.argv[2] != '0') if len(sys.argv) > 2 else True
    nblocks = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    sig = {16: [6, 4, 7, 5, 2, 3, 0, 1], 20: [6, 7, 5, 4, 2, 3, 0, 1], 24: [6, 7, 5, 4, 3, 0, 2, 1], 32: [6, 7, 5, 0, 2, 1, 4, 3], 40: [7, 6, 4, 5, 3, 0, 1, 2]}.get(B)
    t0 = time.time()
    g, bprog, bst, pprog, pst, pat, info = make(B, sig, hoist)
    print('B', B, 'hoist', hoist, 'batch prog', len(bprog), bst, '| prelude prog', len(pprog), pst, info, 'alloc %.1fs' % (time.time() - t0), flush=True)
    bad, ns, cb, cp, cq, cg = validate(bprog, pprog, pat, B, nblocks, 2)
    nbat = ns // 256
    print('validated survivors', ns, 'bad', bad, 'probe-nonzero-branch flags (zero count must be 0):', cb['BRNZ_zero'], 'time %.1fs' % (time.time() - t0))
    print('executed per batch', tot(cb) / nbat, ' per block: prep', tot(cq) / nblocks, 'prelude', tot(cp) / nblocks)
```

#### kernel_report.py (2017 bytes, SHA-256 bb30c3be5089ba4e8e059392757e14118deed4a84e41bcbe198dc7553ddc6d2f)

```python
"""Builds the batch survivor kernel for list blocks of 2^B Gray points, executes it on survivors of random cosets, and prints the
instruction counts that the ledger uses (proof.md Section 5.7 and Appendix C).  Run: python -B kernel_report.py [B] [blocks]
Files: kern.py, tr.py, trsearch.py, kernel2.py, sched.py, run.py, run2.py, ref.py, w40.txt in one folder."""
import sys, json, time
sys.dont_write_bytecode = True
import run2, trsearch, sched
from collections import Counter

B = int(sys.argv[1]) if len(sys.argv) > 1 else 30
NBLK = int(sys.argv[2]) if len(sys.argv) > 2 else 12
t0 = time.time()
masks = [(1 << B) - 1] * 256
cost, sig = trsearch.search(masks, list(range(B)), iters=300, seed=2)
g, bprog, bst, pprog, pst, pat, info = run2.make(B, sig, True)
K_batch = len(bprog) + 5                                   # + LDI tag, ADD, ADDI, SUB, BRX of the loop over batches
K_block = len(run2.block_prep_prog(B)) + 3 + len(pprog)    # block prep + 3 loads of the base + hoisted prelude
print('B', B, 'index transpose input order', sig, 'transpose ops', cost)
print('batch program instructions', len(bprog), bst)
print('K_batch =', K_batch, ' K_block =', K_block, ' prelude', pst, 'hoisted', info, '(%.1fs)' % (time.time() - t0), flush=True)
bad, ns, cb, cp, cq, cg = run2.validate(bprog, pprog, pat, B, NBLK, 4, seed=77)
nb = ns // 256
print('validation: survivors', ns, 'batches', nb, 'wrong table words', bad)
print('executed per batch (with loop control)', run2.tot(cb) / nb, ' per block: prep', run2.tot(cq) / NBLK, ' prelude', run2.tot(cp) / NBLK)
print('executed gather (3 per index word, not used by the ledger: the lists are filled by the extraction)', run2.tot(cg) / ns)
print('opcode mix per batch', dict(sorted(Counter({k: v // nb for k, v in cb.items() if k != 'BRNZ_zero'}).items())))
print('probe branches with a zero test word:', cb['BRNZ_zero'], ' (%.1fs)' % (time.time() - t0))
assert bad == 0 and run2.tot(cb) / nb == K_batch
print(json.dumps({'B': B, 'K_batch': K_batch, 'K_block': K_block}))
```

#### python -B kernel_report.py 30 12 (output)

```
B 30 index transpose input order [6, 7, 5, 2, 3, 1, 4, 0] transpose ops 920
batch program instructions 48175 {'LOAD': 7382, 'STORE': 6100, 'ALU': 32901, 'ADDR': 256, 'PROBE': 1536}
K_batch = 48180  K_block = 2647  prelude {'LOAD': 221, 'STORE': 773, 'ALU': 1603, 'ADDR': 0, 'PROBE': 0} hoisted {'boundary': 450, 'mneed': 317, 'uniform_alu': 855} (3.1s)
validation: survivors 12288 batches 48 wrong table words 0
executed per batch (with loop control) 48180.0  per block: prep 47.0  prelude 2600.0
executed gather (3 per index word, not used by the ledger: the lists are filled by the extraction) 3.0
opcode mix per batch {'ADD': 1, 'ADDI': 513, 'AND': 3136, 'ANDI': 907, 'BRNZ': 256, 'BRX': 1, 'LD': 512, 'LDI': 7127, 'NOT': 944, 'OR': 3275, 'SHLI': 907, 'SHRI': 1051, 'ST': 256, 'STI': 6100, 'SUB': 1, 'XOR': 23193}
probe branches with a zero test word: 0  (5.7s)
{"B": 30, "K_batch": 48180, "K_block": 2647}
```

## Appendix D. Checks of the filter, the extraction and the identifier

`route_check.py` (with ref.py and w40.txt of Appendix C) checks, on real six-round hashes and by executing the code
of Sections 5.5 and 5.6 one counted instruction at a time: (1) the filter formulas on the pre-chi planes equal the
digest-bit test; (2) the extraction appends every set bit of 20,000 random filter words to the list of its lane and
never exceeds 4 + 12 operations per set bit; (3) the slot identifier decodes to the coset and Gray point in 13
instructions (Section 7.1).

#### route_check.py (6552 bytes, SHA-256 877e84eb8e170218ea1cc228dbd38ff706a66cffa5ef59533424a74e0b4755d6)

```python
"""Checks of the filter route (proof.md Sections 5.5 to 5.7), run with ref.py and w40.txt in the same folder:
python -B route_check.py.   (1) the filter formulas on the pre-chi planes equal the digest-bit test on real six-round hashes;
(2) the extraction program, executed one counted instruction at a time on random filter words, appends every set bit to the
list of its lane and costs at most 4 + 12 per set bit per word; (3) the survivor identifier of Section 5.6 decodes to the
coset and Gray point in 13 instructions."""
import sys, random
sys.dont_write_bytecode = True
import ref

M256 = (1 << 256) - 1
M128 = (1 << 128) - 1
rng = random.Random(20261011)

# ---------------------------------------------------------------- (1) filter formulas
def planes(msgs):
    """10 plane words (x, z), x = 0..4, z = 0, 1: bit c = pre-chi bit b[x] bit z of message c; and the survivor predicate"""
    P = {(x, z): 0 for x in range(5) for z in (0, 1)}
    surv = 0
    for c, t in enumerate(msgs):
        L, b = ref.keccak_f(ref.lanes(t), 6, want_b=True)
        for x in range(5):
            for z in (0, 1):
                P[(x, z)] |= ((b[x] >> z) & 1) << c
        if all(((L[x] >> z) & 1) == 0 for x in range(4) for z in (0, 1)):
            surv |= 1 << c
    return P, surv


def acc_of(b, z):
    """pass A (z = 0) / pass B (z = 1) accumulator: k_x = b_x ^ b_{x+2} ^ (b_{x+1} & b_{x+2}) is the chi output; the digest bit is
    k_x, except k_0 at z = 0 where iota adds 1 (RC[5] = 0x80000001): then the accumulator uses NOT k_0.  3 ops per k, 3 ORs."""
    k = []
    for x in range(4):
        u = b[(x + 1) % 5] & b[(x + 2) % 5]
        w = b[x] ^ b[(x + 2) % 5]
        k.append(w ^ u)
    if z == 0:
        k[0] ^= M256                      # 1 extra operation (XOR with the all-ones word)
    return k[0] | k[1] | k[2] | k[3]


def check_filter(nwords=48):
    nsurv = 0
    for _ in range(nwords):
        P, surv = planes([rng.getrandbits(320) for _ in range(256)])
        a0 = acc_of([P[(x, 0)] for x in range(5)], 0)
        a1 = acc_of([P[(x, 1)] for x in range(5)], 1)
        s = (a0 | a1) ^ M256
        assert s == surv, 'filter word differs from the digest test'
        nsurv += bin(s).count('1')
    print('(1) filter word = digest-bit test on %d messages: equal; survivors %d (expected %.1f)' % (256 * nwords, nsurv, nwords))

# ---------------------------------------------------------------- (2) extraction
CLO, CHI = 1 << 128, 1 << 129
SLOT0 = 1 << 127


def extract(s, i, mem, cnt):
    """one filter word s (256-bit) at point i; every executed instruction adds 1 to cnt[0]"""
    def tick(k=1): cnt[0] += k
    lo = s & M128; tick()                 # AND
    tick()                                # BR lo (taken when nonzero)
    hi = s >> 128; tick()                 # SHR
    tick()                                # BR hi
    for reg, base in ((lo, CLO), (hi, CHI)):
        if reg == 0:
            continue
        while reg:
            n = reg ^ M256; tick()                      # NOT
            n = (n + 1) & M256; tick()                  # ADDI
            l = reg & n; tick()                         # AND: lowest set bit
            a = l | base; tick()                        # OR: address of the lane's pointer cell
            p = mem[a]; tick()                          # LOAD
            m = i; tick()                               # MOVI (the point's index is an immediate of its site)
            mem[p] = m; tick()                          # STORE into the list
            p += 1; tick()                              # ADDI
            mem[a] = p; tick()                          # STORE the pointer
            reg ^= l; tick()                            # XOR: clear the bit
            tick()                                      # BR reg (loop)
        tick()                                          # return jump of the out-of-line body


def check_extraction(npts=20000):
    cell = {}
    for c in range(256):
        cell[((CLO if c < 128 else CHI) | (1 << (c % 128)))] = SLOT0 + (c << 24)
    mem = dict(cell)
    expect = [[] for _ in range(256)]
    cnt = [0]
    worst = 0
    bits_total = 0
    for i in range(npts):
        s = 0
        for c in range(256):
            if rng.random() < 1 / 256: s |= 1 << c
        before = cnt[0]
        extract(s, i, mem, cnt)
        k = bin(s).count('1')
        bits_total += k
        worst = max(worst, cnt[0] - before - (4 + 12 * k))
        assert cnt[0] - before <= 4 + 12 * k
        for c in range(256):
            if (s >> c) & 1: expect[c].append(i)
    for c in range(256):
        a = (CLO if c < 128 else CHI) | (1 << (c % 128))
        base = SLOT0 + (c << 24)
        got = [mem[base + q] for q in range(mem[a] - base)]
        assert got == expect[c], 'list of lane %d' % c
    print('(2) extraction: %d words, %d set bits appended to their lane lists exactly; instructions %.3f per word '
          '(bound 4 + 12 per set bit: %.3f); never above the bound' % (npts, bits_total, cnt[0] / npts, 4 + 12 * bits_total / npts))

# ---------------------------------------------------------------- (3) identifier
def check_identifier(B=30, trials=2000):
    CAPB = 6                              # positions per list below 2^(B - CAPB)
    for _ in range(trials):
        h = rng.getrandbits(85)
        I = rng.getrandbits(40 - B)
        c = rng.getrandbits(8)
        pos = rng.getrandbits(B - CAPB)
        lo = rng.getrandbits(B)
        l = (h << (48 - B)) + (I << 8) + c
        nu = SLOT0 + (l << (B - CAPB)) + pos
        assert nu < 1 << 128
        mem = {nu: lo}
        ops = 0
        x = mem[nu]; ops += 1                                          # LOAD the Gray offset
        ll = (nu & ((1 << 127) - 1)) >> (B - CAPB); ops += 2          # AND, SHR
        cc = ll & 255; ops += 1
        II = (ll >> 8) & ((1 << (40 - B)) - 1); ops += 2
        hh = ll >> (48 - B); ops += 1
        j = (hh << 8) | cc; ops += 2
        addr = (j << 1) + 7; ops += 2                                  # record address CSB + 2j (CSB an immediate)
        i = (II << B) | x; ops += 2 + 0 + 0                            # SHL, OR
        # ops so far: 1 + 2 + 1 + 2 + 1 + 2 + 2 + 2 = 13 (the 'cc' and 'II' steps include their shifts, counted above)
        assert j == ((h << 8) | c) and i == ((I << B) | lo) and ops == 13, (ops,)
    print('(3) identifier: 13 instructions decode (coset j, Gray point i) on %d random identifiers' % trials)


if __name__ == '__main__':
    check_filter()
    check_extraction()
    check_identifier()
```

#### python -B route_check.py (output)

```
(1) filter word = digest-bit test on 12288 messages: equal; survivors 41 (expected 48.0)
(2) extraction: 20000 words, 19991 set bits appended to their lane lists exactly; instructions 15.785 per word (bound 4 + 12 per set bit: 15.995); never above the bound
(3) identifier: 13 instructions decode (coset j, Gray point i) on 2000 random identifiers
```

## Appendix E. Survivor measurements: programs and raw lines

The GPU programs below produced the runs of Section 12.4 (compiled with nvcc, one RTX 3090). `scan run <P|R> <rounds>
<log2 cosets> <log2 points> <seed> <z1> <z2> <bucket> <prefix>` writes the 256-bucket histogram of every coset and the
survivors; `analyze <prefix> <z1> <z2> <bucket> <P|R>` writes the report. The runs were
`scan run P 6 16 18 20261011 0 1 0 P6`, `scan run R 6 16 18 20261012 0 1 0 R6`, `scan run P 24 16 18 20261013 0 1 0 P24`,
`scan run R 24 16 18 20261014 0 1 0 R24`, `scan run P 6 16 18 20261015 17 34 165 P6b`,
`scan run P 6 16 18 20261016 0 1 255 P6c` and `scan run P 24 16 18 20261017 0 1 0 P24c`, each followed by
`analyze` with the same filter and mode (the meta line of each report below gives the parameters).

#### scan.cu (8899 bytes, SHA-256 e3e45f9e0c57194df9be66f2ac186a38b7e5278459dbfc4509d4aaaa12e11643)

```cuda
// scan.cu - k=8 key-bit filter on the real r6 message stream (W40 cosets, Gray order / random positions, random origins)
// usage: scan test <vectors.txt> | scan run <mode P|R> <rounds 6|24> <log2NC> <log2NI> <seed> <z1> <z2> <bucket> <outprefix>
// filter: digest bits (lane L=0..3, z in {z1,z2}) -> 8-bit value f = sum bit(L,z1)<<L | bit(L,z2)<<(4+L); survivor iff f == bucket
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <string>
#include <vector>
typedef unsigned long long u64;
typedef unsigned int u32;
__constant__ u64 d_RC[24];
__constant__ int d_RHO[25];
__constant__ u64 d_W[40][5];
static const u64 H_RC[24] = {0x0000000000000001ULL,0x0000000000008082ULL,0x800000000000808AULL,0x8000000080008000ULL,0x000000000000808BULL,
 0x0000000080000001ULL,0x8000000080008081ULL,0x8000000000008009ULL,0x000000000000008AULL,0x0000000000000088ULL,
 0x0000000080008009ULL,0x000000008000000AULL,0x000000008000808BULL,0x800000000000008BULL,0x8000000000008089ULL,
 0x8000000000008003ULL,0x8000000000008002ULL,0x8000000000000080ULL,0x000000000000800AULL,0x800000008000000AULL,
 0x8000000080008081ULL,0x8000000000008080ULL,0x0000000080000001ULL,0x8000000080008008ULL};
static const int H_RHO[25] = {0,1,62,28,27,36,44,6,55,20,3,10,43,25,39,41,45,15,21,8,18,2,61,56,14};
static u64 h_W[40][5];
static u64* d_T; // byte tables [5][256][5]

__device__ __forceinline__ u64 rotl(u64 x, int s){ return s ? (x<<s)|(x>>(64-s)) : x; }

template<int ROUNDS>
__device__ __forceinline__ void keccak_digest(const u64 u[5], u64 dg[4]) {
  u64 L[25];
#pragma unroll
  for (int i=0;i<25;i++) L[i]=0;
#pragma unroll
  for (int i=0;i<5;i++){ L[i]=u[i]; L[10+i]=u[i]; }
  L[16] = 0x86ULL<<56;
#pragma unroll
  for (int r=0;r<ROUNDS;r++){
    u64 C[5], D[5], B[25];
#pragma unroll
    for (int x=0;x<5;x++) C[x]=L[x]^L[x+5]^L[x+10]^L[x+15]^L[x+20];
#pragma unroll
    for (int x=0;x<5;x++) D[x]=C[(x+4)%5]^rotl(C[(x+1)%5],1);
#pragma unroll
    for (int i=0;i<25;i++){ int x=i%5,y=i/5; B[y+5*((2*x+3*y)%5)] = rotl(L[i]^D[x], d_RHO[i]); }
#pragma unroll
    for (int i=0;i<25;i++){ int r5=i-i%5; L[i]=B[i]^(~B[r5+(i+1)%5]&B[r5+(i+2)%5]); }
    L[0]^=d_RC[r];
  }
  dg[0]=L[0];dg[1]=L[1];dg[2]=L[2];dg[3]=L[3];
}

__device__ __forceinline__ u64 smix(u64 x){ x+=0x9E3779B97F4A7C15ULL; x=(x^(x>>30))*0xBF58476D1CE4E5B9ULL; x=(x^(x>>27))*0x94D049BB133111EBULL; return x^(x>>31); }
__device__ __forceinline__ void origin_of(u64 seed, u32 c, u64 o[5]){ for(int k=0;k<5;k++) o[k]=smix(seed*0x100000001B3ULL ^ ((u64)c<<8) ^ (u64)(k+1)*0xABCDEF12345ULL); }

struct Rec { u32 coset; u32 pad; u64 idx; u64 d[4]; };

template<int ROUNDS>
__global__ void scan_kernel(int mode, int segs, u64 seed, int z1, int z2, int bucket, u32* hist, Rec* surv, u64* nsurv, u64 cap,
                            u64* samp, u64* nsamp, u64 sampcap, const u64* T) {
  __shared__ u32 sh[256];
  for (int i=threadIdx.x;i<256;i+=blockDim.x) sh[i]=0;
  __syncthreads();
  u32 c = blockIdx.x / segs, seg = blockIdx.x % segs;
  u64 o[5]; origin_of(seed, c, o);
  u64 t[5];
  u64 s0 = (u64)seg*4096 + (u64)threadIdx.x*16;
  if (mode==0) {
    u64 g = s0 ^ (s0>>1);
    for(int k=0;k<5;k++) t[k]=o[k];
    for (int b=0;b<40;b++) if ((g>>b)&1) for(int k=0;k<5;k++) t[k]^=d_W[b][k];
  }
  for (int e=0;e<16;e++){
    u64 i;
    if (mode==0) {
      i = s0+e;
      if (e>0) { int b=__ffsll(i)-1; for(int k=0;k<5;k++) t[k]^=d_W[b][k]; }
    } else {
      i = smix(seed ^ 0x5555ULL ^ ((u64)blockIdx.x<<24) ^ ((u64)threadIdx.x<<8) ^ (u64)e*0x9E37ULL) & ((1ULL<<40)-1);
      u64 g = i ^ (i>>1);
      for(int k=0;k<5;k++) t[k]=o[k];
      for (int by=0;by<5;by++){ u32 v=(g>>(8*by))&255; const u64* p=T+((by*256+v)*5); for(int k=0;k<5;k++) t[k]^=__ldg(p+k); }
    }
    u64 dg[4];
    keccak_digest<ROUNDS>(t, dg);
    u32 f=0;
    for (int L=0;L<4;L++){ f |= (u32)((dg[L]>>z1)&1)<<L; f |= (u32)((dg[L]>>z2)&1)<<(4+L); }
    atomicAdd(&sh[f],1u);
    if ((int)f==bucket) {
      u64 pos=atomicAdd((unsigned long long*)nsurv,1ULL);
      if (pos<cap){ Rec r; r.coset=c; r.pad=0; r.idx=i; r.d[0]=dg[0];r.d[1]=dg[1];r.d[2]=dg[2];r.d[3]=dg[3]; surv[pos]=r; }
    }
    if ((smix(i*0x9E3779B97F4A7C15ULL ^ ((u64)c<<41) ^ seed ^ 0x77ULL)>>54)==0) {   // unfiltered pseudo-random 1/1024 subsample
      u64 pos=atomicAdd((unsigned long long*)nsamp,1ULL);
      if (pos<sampcap){ samp[pos*4+0]=dg[0];samp[pos*4+1]=dg[1];samp[pos*4+2]=dg[2];samp[pos*4+3]=dg[3]; }
    }
  }
  __syncthreads();
  for (int i=threadIdx.x;i<256;i+=blockDim.x) atomicAdd(&hist[(size_t)c*256+i], sh[i]);
}

__global__ void vec_kernel(const u64* tin, u64* out, int n) {
  int j=blockIdx.x*blockDim.x+threadIdx.x; if(j>=n) return;
  u64 t[5]; for(int k=0;k<5;k++) t[k]=tin[j*5+k];
  u64 dg[4];
  keccak_digest<6>(t,dg); for(int k=0;k<4;k++) out[(j*2+0)*4+k]=dg[k];
  keccak_digest<24>(t,dg); for(int k=0;k<4;k++) out[(j*2+1)*4+k]=dg[k];
}

static void load_w(const char* path){
  FILE* f=fopen(path,"r"); if(!f){perror("w40");exit(1);}
  char s[200];
  for(int b=0;b<40;b++){ if(fscanf(f,"%199s",s)!=1){fprintf(stderr,"w40 read\n");exit(1);} if(strlen(s)!=80){fprintf(stderr,"bad len\n");exit(1);}
    for(int k=0;k<5;k++){ char part[17]; memcpy(part,s+80-16*(k+1),16); part[16]=0; h_W[b][k]=strtoull(part,0,16);} }
  fclose(f);
}
static void parse_t(const char* s, u64 t[5]){ for(int k=0;k<5;k++){ char part[17]; memcpy(part,s+80-16*(k+1),16); part[16]=0; t[k]=strtoull(part,0,16);} }

int main(int argc,char**argv){
  cudaMemcpyToSymbol(d_RC,H_RC,sizeof H_RC); cudaMemcpyToSymbol(d_RHO,H_RHO,sizeof H_RHO);
  load_w("w40.txt"); cudaMemcpyToSymbol(d_W,h_W,sizeof h_W);
  std::string cmd=argv[1];
  if(cmd=="test"){
    FILE* f=fopen(argv[2],"r"); char line[1024]; std::vector<u64> tv; std::vector<int> rd; std::vector<std::string> lines;
    // vectors file produced by gen_vec.py: "t_hex" per line (80 hex)
    while(fgets(line,sizeof line,f)){ if(strlen(line)<80) continue; u64 t[5]; parse_t(line,t); for(int k=0;k<5;k++) tv.push_back(t[k]); }
    int n=tv.size()/5; u64 *dt,*dout; cudaMalloc(&dt,tv.size()*8); cudaMalloc(&dout,(size_t)n*8*8);
    cudaMemcpy(dt,tv.data(),tv.size()*8,cudaMemcpyHostToDevice);
    vec_kernel<<<(n+127)/128,128>>>(dt,dout,n); std::vector<u64> out((size_t)n*8); cudaMemcpy(out.data(),dout,out.size()*8,cudaMemcpyDeviceToHost);
    for(int j=0;j<n;j++){ for(int r=0;r<2;r++){ for(int k=0;k<4;k++) printf("%016llx",out[(j*2+r)*4+k]); printf(r?"\n":" "); } }
    return 0;
  }
  int mode = argv[2][0]=='R'; int rounds=atoi(argv[3]); int lNC=atoi(argv[4]); int lNI=atoi(argv[5]); u64 seed=strtoull(argv[6],0,10);
  int z1=atoi(argv[7]), z2=atoi(argv[8]), bucket=atoi(argv[9]); std::string pre=argv[10];
  u64 NC=1ULL<<lNC, NI=1ULL<<lNI; int segs=NI/4096;
  // byte tables
  std::vector<u64> T(5*256*5);
  for(int by=0;by<5;by++) for(int v=0;v<256;v++){ u64 a[5]={0,0,0,0,0}; for(int j=0;j<8;j++) if((v>>j)&1) for(int k=0;k<5;k++) a[k]^=h_W[8*by+j][k]; for(int k=0;k<5;k++) T[(by*256+v)*5+k]=a[k]; }
  cudaMalloc(&d_T,T.size()*8); cudaMemcpy(d_T,T.data(),T.size()*8,cudaMemcpyHostToDevice);
  u64 total=NC*NI; u64 cap=(u64)(total/256.0*1.05)+100000; u64 sampcap=(u64)(total/1024.0*1.1)+100000;
  u32* d_hist; cudaMalloc(&d_hist,NC*256*4); cudaMemset(d_hist,0,NC*256*4);
  Rec* d_surv; cudaMalloc(&d_surv,cap*sizeof(Rec)); u64* d_samp; cudaMalloc(&d_samp,sampcap*32);
  u64* d_cnt; cudaMalloc(&d_cnt,16); cudaMemset(d_cnt,0,16);
  size_t nblocks=NC*segs;
  // launch in chunks (grid dim limit fine for 2^31)
  if(rounds==6) scan_kernel<6><<<nblocks,256>>>(mode,segs,seed,z1,z2,bucket,d_hist,d_surv,d_cnt,cap,d_samp,d_cnt+1,sampcap,d_T);
  else scan_kernel<24><<<nblocks,256>>>(mode,segs,seed,z1,z2,bucket,d_hist,d_surv,d_cnt,cap,d_samp,d_cnt+1,sampcap,d_T);
  cudaError_t e=cudaDeviceSynchronize(); if(e!=cudaSuccess){fprintf(stderr,"cuda err %s\n",cudaGetErrorString(e));return 1;}
  u64 cnt[2]; cudaMemcpy(cnt,d_cnt,16,cudaMemcpyDeviceToHost);
  printf("scanned %llu survivors %llu (expected %.1f) samples %llu cap %llu/%llu\n",total,cnt[0],total/256.0,cnt[1],cap,sampcap);
  if(cnt[0]>cap||cnt[1]>sampcap){fprintf(stderr,"overflow\n");return 2;}
  std::vector<Rec> hs(cnt[0]); cudaMemcpy(hs.data(),d_surv,cnt[0]*sizeof(Rec),cudaMemcpyDeviceToHost);
  std::vector<u64> sp(cnt[1]*4); cudaMemcpy(sp.data(),d_samp,cnt[1]*32,cudaMemcpyDeviceToHost);
  std::vector<u32> hh(NC*256); cudaMemcpy(hh.data(),d_hist,NC*256*4,cudaMemcpyDeviceToHost);
  FILE* fo=fopen((pre+".surv").c_str(),"wb"); fwrite(hs.data(),sizeof(Rec),hs.size(),fo); fclose(fo);
  fo=fopen((pre+".samp").c_str(),"wb"); fwrite(sp.data(),32,cnt[1],fo); fclose(fo);
  fo=fopen((pre+".hist").c_str(),"wb"); fwrite(hh.data(),4,hh.size(),fo); fclose(fo);
  FILE* fm=fopen((pre+".meta").c_str(),"w"); fprintf(fm,"mode %d rounds %d NC %llu NI %llu seed %llu z1 %d z2 %d bucket %d nsurv %llu nsamp %llu\n",mode,rounds,NC,NI,seed,z1,z2,bucket,cnt[0],cnt[1]); fclose(fm);
  return 0;
}
```

#### analyze.cpp (17632 bytes, SHA-256 a7db929f7bdf5439a9becba8894eaa9c74780726947ae79b36d3ed3c70ebc884)

```cpp
// analyze.cpp - uniformity tests of k=8 filter survivors.  usage: analyze <prefix> <z1> <z2> <bucket> <mode P|R> [nthreads]
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <cmath>
#include <vector>
#include <string>
#include <algorithm>
#include <thread>
#include <mutex>
#include <atomic>
typedef unsigned long long u64; typedef unsigned int u32;
struct Rec { u32 coset; u32 pad; u64 idx; u64 d[4]; };
static int NT = 8;
static std::mutex pm;

static void transpose64(u64 a[64]) {   // a[r] bit c  -> a[c] bit r
  int j = 32; u64 m = 0x00000000FFFFFFFFULL;
  for (; j; j >>= 1, m ^= (m << j)) {
    for (int k = 0; k < 64; k = ((k | j) + 1) & ~j) {
      u64 t = ((a[k] >> j) ^ a[k | j]) & m;   // standard: swap block
      a[k] ^= (t << j); a[k | j] ^= t;
    }
  }
}
template<class F> static void parfor(size_t n, F f) {
  std::atomic<size_t> nx(0); std::vector<std::thread> th;
  for (int t = 0; t < NT; t++) th.emplace_back([&]() { for (;;) { size_t i = nx.fetch_add(1); if (i >= n) break; f(i); } });
  for (auto& x : th) x.join();
}
static std::vector<char> ex;   // excluded (filtered) bit
static double zbin(double obs, double mean, double var) { return (obs - mean) / sqrt(var); }

struct Proj { std::string name; int m; std::vector<int> bits; };
static u32 extract(const u64 d[4], const std::vector<int>& bits) { u32 v = 0; for (size_t q = 0; q < bits.size(); q++) { int j = bits[q]; v |= (u32)((d[j >> 6] >> (j & 63)) & 1) << q; } return v; }
static double count_pairs_sorted(std::vector<u64>& a) { std::sort(a.begin(), a.end()); double P = 0; size_t i = 0, n = a.size(); while (i < n) { size_t j = i; while (j < n && a[j] == a[i]) j++; double c = j - i; P += c * (c - 1) / 2; i = j; } return P; }

int main(int argc, char** argv) {
  std::string pre = argv[1]; int z1 = atoi(argv[2]), z2 = atoi(argv[3]), bucket = atoi(argv[4]); char mode = argv[5][0]; if (argc > 6) NT = atoi(argv[6]);
  ex.assign(256, 0); for (int L = 0; L < 4; L++) { ex[L * 64 + z1] = 1; ex[L * 64 + z2] = 1; }
  // meta
  u64 NC, NI, nsurv, nsamp; { FILE* f = fopen((pre + ".meta").c_str(), "r"); char buf[512]; fgets(buf, 512, f); fclose(f);
    int md, rd, zz1, zz2, bk; u64 seed; sscanf(buf, "mode %d rounds %d NC %llu NI %llu seed %llu z1 %d z2 %d bucket %d nsurv %llu nsamp %llu", &md, &rd, &NC, &NI, &seed, &zz1, &zz2, &bk, &nsurv, &nsamp); printf("meta: %s", buf); }
  size_t N = nsurv;
  std::vector<Rec> S(N); { FILE* f = fopen((pre + ".surv").c_str(), "rb"); if (fread(S.data(), sizeof(Rec), N, f) != N) { fprintf(stderr, "short\n"); return 1; } fclose(f); }
  double total = (double)NC * NI, p = 1.0 / 256;
  printf("== 1. survivor count: N=%zu expected %.1f z=%.2f\n", N, total * p, (N - total * p) / sqrt(total * p * (1 - p)));
  // filter sanity: all survivors have the bucket value
  { size_t bad = 0; for (size_t i = 0; i < N; i++) { u32 f = 0; for (int L = 0; L < 4; L++) { f |= (u32)((S[i].d[L] >> z1) & 1) << L; f |= (u32)((S[i].d[L] >> z2) & 1) << (4 + L); } if ((int)f != bucket) bad++; } printf("   filter check: %zu survivors with wrong bucket\n", bad); }
  // ---- 2. columns
  size_t W = N / 64 + 1; std::vector<std::vector<u64>> col(256, std::vector<u64>(W, 0));
  parfor(4, [&](size_t L) {
    u64 a[64];
    for (size_t b = 0; b < W; b++) {
      for (int r = 0; r < 64; r++) { size_t i = b * 64 + r; a[r] = i < N ? S[i].d[L] : 0; }
      transpose64(a);   // a[c] bit r = record r bit c
      for (int c = 0; c < 64; c++) col[L * 64 + c][b] = a[c];
    }
  });
  std::vector<int> act; for (int j = 0; j < 256; j++) if (!ex[j]) act.push_back(j);
  std::vector<double> zb(256, 0);
  for (int j : act) { u64 s = 0; for (u64 w : col[j]) s += __builtin_popcountll(w); zb[j] = (s - N / 2.0) / (sqrt((double)N) / 2); }
  { double mx = 0, ss = 0; int n3 = 0, mj = 0; double kmx = 0; double ks = 0; int kn = 0, kn3 = 0;
    for (int j : act) { double a = fabs(zb[j]); ss += zb[j] * zb[j]; if (a > mx) { mx = a; mj = j; } if (a > 3) n3++;
      if ((j >> 6) < 4 && (j & 63) <= 34) { kn++; ks += zb[j] * zb[j]; if (a > kmx) kmx = a; if (a > 3) kn3++; } }
    printf("== 2. per-bit bias over %zu non-filter digest bits: max|z|=%.2f (lane %d bit %d), #|z|>3: %d (exp %.2f), sum z^2=%.1f (dof %zu, z=%.2f)\n", act.size(), mx, mj >> 6, mj & 63, n3, act.size() * 0.0027, ss, act.size(), (ss - act.size()) / sqrt(2.0 * act.size()));
    printf("   key-remaining bits (lane<4,z<=34): n=%d max|z|=%.2f #|z|>3: %d sum z^2=%.1f (dof %d, z=%.2f)\n", kn, kmx, kn3, ks, kn, (ks - kn) / sqrt(2.0 * kn));
    // 5 most extreme
    std::vector<int> o = act; std::sort(o.begin(), o.end(), [&](int a, int b) { return fabs(zb[a]) > fabs(zb[b]); });
    printf("   top bits:"); for (int q = 0; q < 5; q++) printf(" (L%d,z%d)=%.2f", o[q] >> 6, o[q] & 63, zb[o[q]]); printf("\n");
    printf("   relative bias resolution: 1 sigma = %.2e of probability\n", 0.5 / sqrt((double)N)); }
  // pair parity
  { std::vector<double> mxz(act.size(), 0), ssz(act.size(), 0); std::vector<int> n4(act.size(), 0); std::vector<std::pair<double, std::pair<int, int>>> best(act.size());
    parfor(act.size(), [&](size_t ia) {
      double mx = 0, ss = 0; int n4l = 0; std::pair<int, int> bp = { 0, 0 };
      for (size_t ib = ia + 1; ib < act.size(); ib++) { const u64* A = col[act[ia]].data(); const u64* B = col[act[ib]].data(); u64 s = 0; for (size_t w = 0; w < W; w++) s += __builtin_popcountll(A[w] ^ B[w]);
        double z = (s - N / 2.0) / (sqrt((double)N) / 2); ss += z * z; if (fabs(z) > mx) { mx = fabs(z); bp = { act[ia], act[ib] }; } if (fabs(z) > 4) n4l++; }
      mxz[ia] = mx; ssz[ia] = ss; n4[ia] = n4l; best[ia] = { mx, bp }; });
    double ss = 0, mx = 0; int n4t = 0; std::pair<int, int> bp = { 0, 0 }; for (size_t i = 0; i < act.size(); i++) { ss += ssz[i]; n4t += n4[i]; if (mxz[i] > mx) { mx = mxz[i]; bp = best[i].second; } }
    double npairs = act.size() * (act.size() - 1) / 2.0;
    printf("== 3. pair-parity bias over %.0f bit pairs: max|z|=%.2f at (L%d,z%d)-(L%d,z%d); #|z|>4: %d (exp %.2f); sum z^2 = %.1f (dof %.0f, z=%.2f)\n", npairs, mx, bp.first >> 6, bp.first & 63, bp.second >> 6, bp.second & 63, n4t, npairs * 6.3e-5, ss, npairs, (ss - npairs) / sqrt(2 * npairs)); }
  col.clear(); col.shrink_to_fit();
  // ---- 4. projections
  std::vector<Proj> P; std::vector<int> keyrem, allrem;
  for (int j : act) { allrem.push_back(j); if ((j >> 6) < 4 && (j & 63) <= 34) keyrem.push_back(j); }
  for (int m : { 16, 24, 32 }) {
    for (int L = 0; L < 4; L++) { Proj q; q.name = "laneTop L" + std::to_string(L); q.m = m; for (int z = 64 - m; z < 64; z++) q.bits.push_back(L * 64 + z); P.push_back(q); }
    for (int L = 0; L < 4; L++) { Proj q; q.name = "laneLow L" + std::to_string(L); q.m = m; int n = 0; for (int z = 2; n < m; z++) { q.bits.push_back(L * 64 + z); n++; } P.push_back(q); }
    { Proj q; q.name = "cross z2.."; q.m = m; for (int z = 2; (int)q.bits.size() < m; z++) for (int L = 0; L < 4 && (int)q.bits.size() < m; L++) q.bits.push_back(L * 64 + z); P.push_back(q); }
    for (int s = 0; s < 4; s++) { Proj q; q.name = "keyRand s" + std::to_string(s); q.m = m; std::vector<int> v = keyrem; u64 x = 12345 + 777 * s + m; for (int i = (int)v.size() - 1; i > 0; i--) { x = x * 6364136223846793005ULL + 1442695040888963407ULL; std::swap(v[i], v[(x >> 33) % (i + 1)]); } v.resize(m); q.bits = v; P.push_back(q); }
    for (int s = 0; s < 4; s++) { Proj q; q.name = "allRand s" + std::to_string(s); q.m = m; std::vector<int> v = allrem; u64 x = 54321 + 991 * s + m; for (int i = (int)v.size() - 1; i > 0; i--) { x = x * 6364136223846793005ULL + 1442695040888963407ULL; std::swap(v[i], v[(x >> 33) % (i + 1)]); } v.resize(m); q.bits = v; P.push_back(q); }
  }
  double Wc = 0; { std::vector<u64> nc(NC, 0); for (size_t i = 0; i < N; i++) nc[S[i].coset]++; for (u64 n : nc) Wc += (double)n * (n - 1) / 2; }
  double CN = (double)N * (N - 1) / 2;
  printf("== 4. pair collision rates on projections (N=%zu, all-pairs %.4g, within-coset pairs %.4g)\n", N, CN, Wc);
  printf("   %-16s %2s | zAll   obs/exp(all)  | zCross  obs/exp  | zWithin(obs vs exp)\n", "projection", "m");
  std::vector<std::string> lines(P.size()); std::vector<double> zall(P.size()), zcr(P.size()), zwi(P.size());
  parfor(P.size(), [&](size_t q) {
    const Proj& pr = P[q]; int m = pr.m; double M = std::pow(2.0, m);
    std::vector<u64> keyed(N); std::vector<u32> val(N);
    for (size_t i = 0; i < N; i++) { val[i] = extract(S[i].d, pr.bits); keyed[i] = ((u64)S[i].coset << 32) | val[i]; }
    double within = count_pairs_sorted(keyed);
    double all;
    if (m <= 24) { std::vector<u32> cnt((size_t)1 << m, 0); for (size_t i = 0; i < N; i++) cnt[val[i]]++; all = 0; for (u32 c : cnt) all += (double)c * (c - 1) / 2; }
    else { std::vector<u64> v2(val.begin(), val.end()); all = count_pairs_sorted(v2); }
    double cross = all - within;
    double eAll = CN / M, eCr = (CN - Wc) / M, eWi = Wc / M;
    double za = (all - eAll) / sqrt(eAll * (1 - 1 / M)), zc = (cross - eCr) / sqrt(eCr * (1 - 1 / M)), zw = eWi >= 5 ? (within - eWi) / sqrt(eWi * (1 - 1 / M)) : 0.0 / 0.0;
    zall[q] = za; zcr[q] = zc; zwi[q] = zw;
    char b[300]; snprintf(b, 300, "   %-16s %2d | %6.2f %9.6f | %6.2f %9.6f | %6.2f (%.0f vs %.1f)", pr.name.c_str(), m, za, all / eAll, zc, cross / eCr, zw, within, eWi); lines[q] = b; });
  for (auto& l : lines) puts(l.c_str());
  for (int m : { 16, 24, 32 }) { double sa = 0, sc = 0, sw = 0; int n = 0, nbig = 0, nw = 0; double mx = 0; for (size_t q = 0; q < P.size(); q++) if (P[q].m == m) { n++; sa += zall[q]; sc += zcr[q]; if (!std::isnan(zwi[q])) { sw += zwi[q]; nw++; } mx = std::max(mx, fabs(zcr[q])); if (fabs(zcr[q]) > 3) nbig++; }
    printf("   m=%d: %d projections, mean zAll %.2f, mean zCross %.2f, mean zWithin %.2f, max|zCross| %.2f, #|zCross|>3: %d\n", m, n, sa / n, sc / n, sw / n, mx, nbig); }
  // unfiltered sample baseline on identical projections
  if (nsamp) { std::vector<u64> Sd(nsamp * 4); FILE* f = fopen((pre + ".samp").c_str(), "rb"); if (fread(Sd.data(), 32, nsamp, f) != nsamp) { fprintf(stderr, "short samp\n"); return 1; } fclose(f);
    // unfiltered sample baseline (projection bits overlapping filter bits are not special here)
    printf("== 4b. unfiltered pseudo-random 1/1024 subsample of the same stream (n=%llu): collision-rate z on the same projections\n", nsamp);
    double CNs = (double)nsamp * (nsamp - 1) / 2; std::vector<double> zs(P.size());
    parfor(P.size(), [&](size_t q) { const Proj& pr = P[q]; int m = pr.m; double M = std::pow(2.0, m); std::vector<u64> v(nsamp); for (size_t i = 0; i < nsamp; i++) v[i] = extract(&Sd[i * 4], pr.bits);
      double all = count_pairs_sorted(v); double e = CNs / M; zs[q] = (all - e) / sqrt(e * (1 - 1 / M)); });
    for (int m : { 16, 24, 32 }) { double sa = 0, mx = 0; int n = 0; for (size_t q = 0; q < P.size(); q++) if (P[q].m == m) { n++; sa += zs[q]; mx = std::max(mx, fabs(zs[q])); } printf("   m=%d: mean z %.2f max|z| %.2f over %d projections\n", m, sa / n, mx, n); }
    // per-bit bias of the unfiltered sample (sanity of the stream)
    double mxb = 0, ss = 0; int cnt = 0; for (int j = 0; j < 256; j++) { u64 s = 0; for (size_t i = 0; i < nsamp; i++) s += (Sd[i * 4 + (j >> 6)] >> (j & 63)) & 1; double z = (s - nsamp / 2.0) / (sqrt((double)nsamp) / 2); mxb = std::max(mxb, fabs(z)); ss += z * z; cnt++; }
    printf("   unfiltered per-bit bias: max|z| %.2f, sum z^2 %.1f (dof 256, z=%.2f)\n", mxb, ss, (ss - 256) / sqrt(512.0)); }
  // ---- 5. coset histogram analysis
  { std::vector<u32> H(NC * 256); FILE* f = fopen((pre + ".hist").c_str(), "rb"); if (fread(H.data(), 4, H.size(), f) != H.size()) { fprintf(stderr, "short hist\n"); return 1; } fclose(f);
    double mu = (double)NI / 256; double chiall = 0; double zc_sum2 = 0, zmin = 1e9, zmax = -1e9; u64 n3 = 0;
    std::vector<double> tot(256, 0);
    for (u64 c = 0; c < NC; c++) { double chi = 0; for (int b = 0; b < 256; b++) { double h = H[c * 256 + b]; chi += (h - mu) * (h - mu) / mu; tot[b] += h; }
      chiall += chi; double zc = (H[c * 256 + bucket] - mu) / sqrt(mu * (1 - p)); zc_sum2 += zc * zc; zmin = std::min(zmin, zc); zmax = std::max(zmax, zc); if (fabs(zc) > 3) n3++; }
    double dof = (double)NC * 255;
    printf("== 5. per-coset 256-bucket histograms (NC=%llu cosets x %llu scanned): sum chi2 over cosets = %.0f, dof %.0f, z=%.2f\n", NC, NI, chiall, dof, (chiall - dof) / sqrt(2 * dof));
    printf("   bucket %d per-coset count: var of z = %.4f (expect ~1), min z %.2f max z %.2f, #|z|>3: %llu (exp %.1f)\n", bucket, zc_sum2 / NC, zmin, zmax, n3, NC * 0.0027);
    double mut = total / 256, chit = 0; for (int b = 0; b < 256; b++) chit += (tot[b] - mut) * (tot[b] - mut) / mut;
    printf("   pooled 256-bucket chi2 = %.1f (dof 255, z=%.2f); bucket %d pooled rate / 2^-8 = %.6f\n", chit, (chit - 255) / sqrt(510.0), bucket, tot[bucket] / mut);
    // survivors per coset across the whole scan, and extrapolated full-coset survivors
    double rate = tot[bucket] / total; printf("   pooled bucket rate %.6e; full-coset (2^40) expected survivors %.4g\n", rate, rate * 1099511627776.0);
  }
  // ---- 6. gap / batch analysis (Gray-prefix mode only)
  if (mode == 'P') {
    std::vector<std::pair<u64, u64>> key(N); for (size_t i = 0; i < N; i++) key[i] = { S[i].coset, S[i].idx }; std::sort(key.begin(), key.end());
    // gaps inside the window only (edge gaps unobservable): truncation biases mean gap low, so compare against a synthetic Bernoulli(1/256) null with identical windows
    std::vector<double> gaps; gaps.reserve(N); for (size_t i = 1; i < N; i++) if (key[i].first == key[i - 1].first) gaps.push_back((double)(key[i].second - key[i - 1].second));
    std::vector<double> sg; sg.reserve(N + 1000000); { u64 x = 88172645463325252ULL; auto rnd = [&]() { x ^= x << 13; x ^= x >> 7; x ^= x << 17; return x; };
      for (u64 c = 0; c < NC; c++) { long pos = -1; bool have = false; long last = 0; for (;;) { double u = (rnd() >> 11) * (1.0 / 9007199254740992.0); long g = 1 + (long)floor(log(1 - u) / log(1 - p)); pos = (have ? last : 0) + (have ? g : g - 1); if (pos >= (long)NI) break; if (have) sg.push_back((double)(pos - last)); have = true; last = pos; } } }
    auto stat = [&](const std::vector<double>& v, double& mean, double& var, std::vector<double>& ob) { double G = v.size(); mean = 0; double m2 = 0; for (double g : v) { mean += g; m2 += g * g; } mean /= G; var = m2 / G - mean * mean; ob.assign(24, 0); for (double g : v) ob[std::min(23, (int)floor(log2(g)))]++; };
    double m1, v1, m0, v0; std::vector<double> o1, o0; stat(gaps, m1, v1, o1); stat(sg, m0, v0, o0);
    double G1 = gaps.size(), G0 = sg.size();
    printf("== 6. Gray-order gaps between consecutive survivors in a coset (prefix scan, window 2^18): n=%.0f mean %.3f var/mean^2 %.4f ; synthetic Bernoulli null (same windows) n=%.0f mean %.3f var/mean^2 %.4f ; mean diff z=%.2f\n", G1, m1, v1 / (m1 * m1), G0, m0, v0 / (m0 * m0), (m1 - m0) / sqrt(v1 / G1 + v0 / G0));
    double chi = 0; int nb = 0; for (int b2 = 0; b2 < 24; b2++) if (o1[b2] + o0[b2] > 20) { double a2 = o1[b2] * sqrt(G0 / G1), c2 = o0[b2] * sqrt(G1 / G0); chi += (a2 - c2) * (a2 - c2) / (o1[b2] + o0[b2]); nb++; }
    printf("   log2-binned gap two-sample chi2 real vs null = %.1f over %d bins (z=%.2f)\n", chi, nb, (chi - (nb - 1)) / sqrt(2.0 * (nb - 1)));
    double g1 = 0, g10 = 0; for (double g : gaps) if (g == 1) g1++; for (double g : sg) if (g == 1) g10++; printf("   gap==1 (adjacent Gray points both survive): real %.4g/ %.0f = %.6f, null %.6f (geometric 2^-8 = %.6f) z=%.2f\n", g1, G1, g1 / G1, g10 / G0, p, (g1 / G1 - g10 / G0) / sqrt(p * (1 - p) * (1 / G1 + 1 / G0)));
    // lag-k autocorrelation of the survivor indicator inside windows (k=1..16, and k=2^j): count pairs of survivors at exact distance d vs null
    { const int ds[] = { 1, 2, 3, 4, 5, 6, 7, 8, 16, 32, 64, 128, 256, 1024, 4096, 16384, 65536 }; double mxz = 0; int ndl = 0;
      for (int d : ds) { double cnt = 0, pairs = 0; size_t i = 0; while (i < N) { size_t j = i; while (j < N && key[j].first == key[i].first) j++; size_t q = i; for (size_t a = i; a < j; a++) { while (q < j && key[q].second < key[a].second + d) q++; if (q < j && key[q].second == key[a].second + d) cnt++; } pairs += (double)NI - d; i = j; }
        // expected: sum over cosets of (NI-d) p^2 ; pairs counted per coset window
        double e = (double)NC * ((double)NI - d) * p * p; double z = (cnt - e) / sqrt(e); mxz = std::max(mxz, fabs(z)); ndl++; if (d <= 8 || d == 65536) printf("   survivors at exact Gray distance %d: %.0f vs %.1f (z=%.2f)\n", d, cnt, e, z); }
      printf("   distance-d pair counts over %d distances: max|z|=%.2f\n", ndl, mxz); }
    // batches of 256 consecutive survivors in a coset
    std::vector<double> spans; size_t i = 0; while (i < N) { size_t j = i; while (j < N && key[j].first == key[i].first) j++; for (size_t s = i; s + 256 <= j; s += 256) spans.push_back((double)(key[s + 255].second - key[s].second)); i = j; }
    double sm = 0, s2 = 0, smin = 1e30, smax = 0; for (double s : spans) { sm += s; s2 += s * s; smin = std::min(smin, s); smax = std::max(smax, s); } double nB = spans.size(); sm /= nB; double sv = s2 / nB - sm * sm;
    printf("   batches of 256 consecutive survivors of one coset: n=%.0f span(Gray points) mean %.0f (expect %.0f), sd %.0f (expect %.0f), min %.0f max %.0f\n", nB, sm, 255 / p, sqrt(sv), sqrt(255.0) / p, smin, smax);
    // survivors per 2^18 scan per coset
    printf("   NOTE: full coset has 2^40 points -> ~2^32 survivors per bucket; a 256-batch spans ~65k Gray points and is released in survivor order.\n");
  }
  return 0;
}
```

#### gen_vec.py (1126 bytes, SHA-256 9776b015ca3cefe6a1c4115853c7647788beac522fcb5db1bed3342fe388a4b1)

```python
"""Cross-check scan.cu keccak against r6push/structure/ref.py: python3 gen_vec.py gen > vec_in.txt ; scan test vec_in.txt > vec_out.txt ; python3 gen_vec.py check"""
import sys, random
sys.dont_write_bytecode = True
sys.path.insert(0, r'/mnt/d/~~Projects/~HashSmash/workspace/research/r6push/structure')
import ref
rng = random.Random(7)
ts = [0, ref.W40[0] ^ ref.W40[39]] + [rng.getrandbits(320) for _ in range(2000)]
# Gray-order points of the real stream
og = rng.getrandbits(320)
for i in list(range(1, 300)) + [rng.getrandbits(40) for _ in range(300)]:
    g = i ^ (i >> 1); t = og
    for b in range(40):
        if (g >> b) & 1: t ^= ref.W40[b]
    ts.append(t)
if sys.argv[1] == 'gen':
    print('\n'.join('%080x' % t for t in ts))
else:
    out = open('vec_out.txt').read().split('\n')
    bad = 0
    for t, line in zip(ts, out):
        a, b = line.split()
        for r, h in ((6, a), (24, b)):
            L = ref.keccak_f(ref.lanes(t), r)
            d = ''.join('%016x' % v for v in L[:4])
            if d != h: bad += 1
    print('vectors', len(ts), 'mismatch', bad)
    L = ref.keccak_f(ref.lanes(ts[0]), 6)
```

#### gen_vec.py check (GPU digests against ref.py)

```
vectors 2601 mismatch 0
```

#### P6.report.txt (the per-projection rows of section 4 are omitted; its summary lines are kept)

```
meta: mode 0 rounds 6 NC 65536 NI 262144 seed 20261011 z1 0 z2 1 bucket 0 nsurv 67112067 nsamp 16776679
== 1. survivor count: N=67112067 expected 67108864.0 z=0.39
   filter check: 0 survivors with wrong bucket
== 2. per-bit bias over 248 non-filter digest bits: max|z|=3.23 (lane 3 bit 35), #|z|>3: 1 (exp 0.67), sum z^2=221.1 (dof 248, z=-1.21)
   key-remaining bits (lane<4,z<=34): n=132 max|z|=2.75 #|z|>3: 0 sum z^2=100.4 (dof 132, z=-1.94)
   top bits: (L3,z35)=3.23 (L2,z28)=-2.75 (L3,z54)=2.71 (L0,z3)=-2.42 (L3,z38)=2.28
   relative bias resolution: 1 sigma = 6.10e-05 of probability
== 3. pair-parity bias over 30628 bit pairs: max|z|=4.22 at (L0,z52)-(L2,z3); #|z|>4: 2 (exp 1.93); sum z^2 = 30430.1 (dof 30628, z=-0.80)
== 4. pair collision rates on projections (N=67112067, all-pairs 2.252e+15, within-coset pairs 3.436e+10)
   projection        m | zAll   obs/exp(all)  | zCross  obs/exp  | zWithin(obs vs exp)
   m=16: 17 projections, mean zAll -0.20, mean zCross -0.20, mean zWithin -0.03, max|zCross| 1.91, #|zCross|>3: 0
   m=24: 17 projections, mean zAll 0.27, mean zCross 0.27, mean zWithin -0.07, max|zCross| 2.10, #|zCross|>3: 0
   m=32: 17 projections, mean zAll -0.04, mean zCross -0.04, mean zWithin 0.10, max|zCross| 1.94, #|zCross|>3: 0
== 4b. unfiltered pseudo-random 1/1024 subsample of the same stream (n=16776679): collision-rate z on the same projections
   m=16: mean z -0.29 max|z| 2.53 over 17 projections
   m=24: mean z -0.34 max|z| 2.22 over 17 projections
   m=32: mean z 0.25 max|z| 2.73 over 17 projections
   unfiltered per-bit bias: max|z| 2.73, sum z^2 245.7 (dof 256, z=-0.46)
== 5. per-coset 256-bucket histograms (NC=65536 cosets x 262144 scanned): sum chi2 over cosets = 16714218, dof 16711680, z=0.44
   bucket 0 per-coset count: var of z = 1.0009 (expect ~1), min z -3.95 max z 4.60, #|z|>3: 178 (exp 176.9)
   pooled 256-bucket chi2 = 245.4 (dof 255, z=-0.43); bucket 0 pooled rate / 2^-8 = 1.000048
   pooled bucket rate 3.906436e-03; full-coset (2^40) expected survivors 4.295e+09
== 6. Gray-order gaps between consecutive survivors in a coset (prefix scan, window 2^18): n=67046531 mean 255.738 var/mean^2 0.9964 ; synthetic Bernoulli null (same windows) n=67039192 mean 255.765 var/mean^2 0.9960 ; mean diff z=-0.61
   log2-binned gap two-sample chi2 real vs null = 6.4 over 12 bins (z=-0.98)
   gap==1 (adjacent Gray points both survive): real 2.621e+05/ 67046531 = 0.003909, null 0.003909 (geometric 2^-8 = 0.003906) z=-0.04
   survivors at exact Gray distance 1: 262085 vs 262143.0 (z=-0.11)
   survivors at exact Gray distance 2: 262555 vs 262142.0 (z=0.81)
   survivors at exact Gray distance 3: 261955 vs 262141.0 (z=-0.36)
   survivors at exact Gray distance 4: 263039 vs 262140.0 (z=1.76)
   survivors at exact Gray distance 5: 262472 vs 262139.0 (z=0.65)
   survivors at exact Gray distance 6: 261060 vs 262138.0 (z=-2.11)
   survivors at exact Gray distance 7: 262705 vs 262137.0 (z=1.11)
   survivors at exact Gray distance 8: 263523 vs 262136.0 (z=2.71)
   survivors at exact Gray distance 65536: 196009 vs 196608.0 (z=-1.35)
   distance-d pair counts over 17 distances: max|z|=2.71
   batches of 256 consecutive survivors of one coset: n=229559 span(Gray points) mean 65043 (expect 65280), sd 4055 (expect 4088), min 47839 max 84790
   NOTE: full coset has 2^40 points -> ~2^32 survivors per bucket; a 256-batch spans ~65k Gray points and is released in survivor order.
```

#### P24.report.txt (the per-projection rows of section 4 are omitted; its summary lines are kept)

```
meta: mode 0 rounds 24 NC 65536 NI 262144 seed 20261013 z1 0 z2 1 bucket 0 nsurv 67110599 nsamp 16782499
== 1. survivor count: N=67110599 expected 67108864.0 z=0.21
   filter check: 0 survivors with wrong bucket
== 2. per-bit bias over 248 non-filter digest bits: max|z|=2.50 (lane 1 bit 63), #|z|>3: 0 (exp 0.67), sum z^2=222.3 (dof 248, z=-1.15)
   key-remaining bits (lane<4,z<=34): n=132 max|z|=2.33 #|z|>3: 0 sum z^2=114.8 (dof 132, z=-1.06)
   top bits: (L1,z63)=2.50 (L0,z46)=2.34 (L1,z29)=-2.33 (L0,z15)=2.31 (L3,z6)=2.29
   relative bias resolution: 1 sigma = 6.10e-05 of probability
== 3. pair-parity bias over 30628 bit pairs: max|z|=4.72 at (L0,z58)-(L1,z62); #|z|>4: 1 (exp 1.93); sum z^2 = 30504.7 (dof 30628, z=-0.50)
== 4. pair collision rates on projections (N=67110599, all-pairs 2.252e+15, within-coset pairs 3.436e+10)
   projection        m | zAll   obs/exp(all)  | zCross  obs/exp  | zWithin(obs vs exp)
   m=16: 17 projections, mean zAll 0.05, mean zCross 0.05, mean zWithin 0.31, max|zCross| 1.93, #|zCross|>3: 0
   m=24: 17 projections, mean zAll 0.46, mean zCross 0.46, mean zWithin 0.56, max|zCross| 2.16, #|zCross|>3: 0
   m=32: 17 projections, mean zAll -0.32, mean zCross -0.32, mean zWithin -0.17, max|zCross| 2.42, #|zCross|>3: 0
== 4b. unfiltered pseudo-random 1/1024 subsample of the same stream (n=16782499): collision-rate z on the same projections
   m=16: mean z 0.05 max|z| 2.03 over 17 projections
   m=24: mean z -0.13 max|z| 1.32 over 17 projections
   m=32: mean z -0.23 max|z| 1.79 over 17 projections
   unfiltered per-bit bias: max|z| 3.12, sum z^2 235.6 (dof 256, z=-0.90)
== 5. per-coset 256-bucket histograms (NC=65536 cosets x 262144 scanned): sum chi2 over cosets = 16709468, dof 16711680, z=-0.38
   bucket 0 per-coset count: var of z = 0.9995 (expect ~1), min z -4.57 max z 4.13, #|z|>3: 175 (exp 176.9)
   pooled 256-bucket chi2 = 255.8 (dof 255, z=0.04); bucket 0 pooled rate / 2^-8 = 1.000026
   pooled bucket rate 3.906351e-03; full-coset (2^40) expected survivors 4.295e+09
== 6. Gray-order gaps between consecutive survivors in a coset (prefix scan, window 2^18): n=67045063 mean 255.745 var/mean^2 0.9960 ; synthetic Bernoulli null (same windows) n=67039192 mean 255.765 var/mean^2 0.9960 ; mean diff z=-0.44
   log2-binned gap two-sample chi2 real vs null = 26.6 over 12 bins (z=3.32)
   gap==1 (adjacent Gray points both survive): real 2.629e+05/ 67045063 = 0.003921, null 0.003909 (geometric 2^-8 = 0.003906) z=1.04
   survivors at exact Gray distance 1: 262854 vs 262143.0 (z=1.39)
   survivors at exact Gray distance 2: 261763 vs 262142.0 (z=-0.74)
   survivors at exact Gray distance 3: 262653 vs 262141.0 (z=1.00)
   survivors at exact Gray distance 4: 263225 vs 262140.0 (z=2.12)
   survivors at exact Gray distance 5: 261871 vs 262139.0 (z=-0.52)
   survivors at exact Gray distance 6: 262195 vs 262138.0 (z=0.11)
   survivors at exact Gray distance 7: 261639 vs 262137.0 (z=-0.97)
   survivors at exact Gray distance 8: 262655 vs 262136.0 (z=1.01)
   survivors at exact Gray distance 65536: 196014 vs 196608.0 (z=-1.34)
   distance-d pair counts over 17 distances: max|z|=2.12
   batches of 256 consecutive survivors of one coset: n=229693 span(Gray points) mean 65053 (expect 65280), sd 4066 (expect 4088), min 47937 max 86484
   NOTE: full coset has 2^40 points -> ~2^32 survivors per bucket; a 256-batch spans ~65k Gray points and is released in survivor order.
```

#### P24c.report.txt (the per-projection rows of section 4 are omitted; its summary lines are kept)

```
meta: mode 0 rounds 24 NC 65536 NI 262144 seed 20261017 z1 0 z2 1 bucket 0 nsurv 67112823 nsamp 16775770
== 1. survivor count: N=67112823 expected 67108864.0 z=0.48
   filter check: 0 survivors with wrong bucket
== 2. per-bit bias over 248 non-filter digest bits: max|z|=2.94 (lane 3 bit 36), #|z|>3: 0 (exp 0.67), sum z^2=249.9 (dof 248, z=0.08)
   key-remaining bits (lane<4,z<=34): n=132 max|z|=2.48 #|z|>3: 0 sum z^2=135.4 (dof 132, z=0.21)
   top bits: (L3,z36)=2.94 (L3,z55)=2.71 (L1,z60)=-2.52 (L1,z26)=-2.48 (L0,z31)=-2.42
   relative bias resolution: 1 sigma = 6.10e-05 of probability
== 3. pair-parity bias over 30628 bit pairs: max|z|=4.09 at (L2,z21)-(L2,z25); #|z|>4: 1 (exp 1.93); sum z^2 = 30625.0 (dof 30628, z=-0.01)
== 4. pair collision rates on projections (N=67112823, all-pairs 2.252e+15, within-coset pairs 3.436e+10)
   projection        m | zAll   obs/exp(all)  | zCross  obs/exp  | zWithin(obs vs exp)
   m=16: 17 projections, mean zAll -0.36, mean zCross -0.36, mean zWithin 0.09, max|zCross| 1.52, #|zCross|>3: 0
   m=24: 17 projections, mean zAll 0.15, mean zCross 0.15, mean zWithin -0.01, max|zCross| 2.12, #|zCross|>3: 0
   m=32: 17 projections, mean zAll 0.01, mean zCross 0.01, mean zWithin 0.08, max|zCross| 1.89, #|zCross|>3: 0
== 4b. unfiltered pseudo-random 1/1024 subsample of the same stream (n=16775770): collision-rate z on the same projections
   m=16: mean z -0.11 max|z| 1.60 over 17 projections
   m=24: mean z -0.08 max|z| 1.48 over 17 projections
   m=32: mean z -0.03 max|z| 1.83 over 17 projections
   unfiltered per-bit bias: max|z| 3.03, sum z^2 235.6 (dof 256, z=-0.90)
== 5. per-coset 256-bucket histograms (NC=65536 cosets x 262144 scanned): sum chi2 over cosets = 16724820, dof 16711680, z=2.27
   bucket 0 per-coset count: var of z = 0.9991 (expect ~1), min z -4.13 max z 4.13, #|z|>3: 177 (exp 176.9)
   pooled 256-bucket chi2 = 267.8 (dof 255, z=0.57); bucket 0 pooled rate / 2^-8 = 1.000059
   pooled bucket rate 3.906480e-03; full-coset (2^40) expected survivors 4.295e+09
== 6. Gray-order gaps between consecutive survivors in a coset (prefix scan, window 2^18): n=67047287 mean 255.736 var/mean^2 0.9963 ; synthetic Bernoulli null (same windows) n=67039192 mean 255.765 var/mean^2 0.9960 ; mean diff z=-0.66
   log2-binned gap two-sample chi2 real vs null = 8.3 over 12 bins (z=-0.58)
   gap==1 (adjacent Gray points both survive): real 2.621e+05/ 67047287 = 0.003910, null 0.003909 (geometric 2^-8 = 0.003906) z=0.05
   survivors at exact Gray distance 1: 262149 vs 262143.0 (z=0.01)
   survivors at exact Gray distance 2: 262916 vs 262142.0 (z=1.51)
   survivors at exact Gray distance 3: 261557 vs 262141.0 (z=-1.14)
   survivors at exact Gray distance 4: 262009 vs 262140.0 (z=-0.26)
   survivors at exact Gray distance 5: 262209 vs 262139.0 (z=0.14)
   survivors at exact Gray distance 6: 262006 vs 262138.0 (z=-0.26)
   survivors at exact Gray distance 7: 262632 vs 262137.0 (z=0.97)
   survivors at exact Gray distance 8: 262531 vs 262136.0 (z=0.77)
   survivors at exact Gray distance 65536: 196642 vs 196608.0 (z=0.08)
   distance-d pair counts over 17 distances: max|z|=1.51
   batches of 256 consecutive survivors of one coset: n=229703 span(Gray points) mean 65050 (expect 65280), sd 4058 (expect 4088), min 47963 max 87890
   NOTE: full coset has 2^40 points -> ~2^32 survivors per bucket; a 256-batch spans ~65k Gray points and is released in survivor order.
```

#### P6c.report.txt (the per-projection rows of section 4 are omitted; its summary lines are kept)

```
meta: mode 0 rounds 6 NC 65536 NI 262144 seed 20261016 z1 0 z2 1 bucket 255 nsurv 67098147 nsamp 16774289
== 1. survivor count: N=67098147 expected 67108864.0 z=-1.31
   filter check: 0 survivors with wrong bucket
== 2. per-bit bias over 248 non-filter digest bits: max|z|=3.21 (lane 3 bit 40), #|z|>3: 1 (exp 0.67), sum z^2=213.6 (dof 248, z=-1.54)
   key-remaining bits (lane<4,z<=34): n=132 max|z|=2.26 #|z|>3: 0 sum z^2=106.9 (dof 132, z=-1.55)
   top bits: (L3,z40)=-3.21 (L0,z62)=-2.36 (L3,z47)=2.27 (L3,z26)=2.26 (L3,z31)=1.97
   relative bias resolution: 1 sigma = 6.10e-05 of probability
== 3. pair-parity bias over 30628 bit pairs: max|z|=4.69 at (L1,z37)-(L3,z39); #|z|>4: 1 (exp 1.93); sum z^2 = 30717.2 (dof 30628, z=0.36)
== 4. pair collision rates on projections (N=67098147, all-pairs 2.251e+15, within-coset pairs 3.435e+10)
   projection        m | zAll   obs/exp(all)  | zCross  obs/exp  | zWithin(obs vs exp)
   m=16: 17 projections, mean zAll -0.69, mean zCross -0.69, mean zWithin -0.01, max|zCross| 2.66, #|zCross|>3: 0
   m=24: 17 projections, mean zAll -0.12, mean zCross -0.12, mean zWithin -0.37, max|zCross| 1.84, #|zCross|>3: 0
   m=32: 17 projections, mean zAll 0.25, mean zCross 0.25, mean zWithin -0.02, max|zCross| 1.55, #|zCross|>3: 0
== 4b. unfiltered pseudo-random 1/1024 subsample of the same stream (n=16774289): collision-rate z on the same projections
   m=16: mean z 0.25 max|z| 3.06 over 17 projections
   m=24: mean z 0.11 max|z| 2.36 over 17 projections
   m=32: mean z 0.01 max|z| 1.37 over 17 projections
   unfiltered per-bit bias: max|z| 2.46, sum z^2 234.6 (dof 256, z=-0.95)
== 5. per-coset 256-bucket histograms (NC=65536 cosets x 262144 scanned): sum chi2 over cosets = 16709426, dof 16711680, z=-0.39
   bucket 255 per-coset count: var of z = 1.0028 (expect ~1), min z -3.98 max z 4.10, #|z|>3: 180 (exp 176.9)
   pooled 256-bucket chi2 = 252.5 (dof 255, z=-0.11); bucket 255 pooled rate / 2^-8 = 0.999840
   pooled bucket rate 3.905626e-03; full-coset (2^40) expected survivors 4.294e+09
== 6. Gray-order gaps between consecutive survivors in a coset (prefix scan, window 2^18): n=67032611 mean 255.791 var/mean^2 0.9961 ; synthetic Bernoulli null (same windows) n=67039192 mean 255.765 var/mean^2 0.9960 ; mean diff z=0.59
   log2-binned gap two-sample chi2 real vs null = 8.7 over 12 bins (z=-0.48)
   gap==1 (adjacent Gray points both survive): real 2.616e+05/ 67032611 = 0.003903, null 0.003909 (geometric 2^-8 = 0.003906) z=-0.60
   survivors at exact Gray distance 1: 261621 vs 262143.0 (z=-1.02)
   survivors at exact Gray distance 2: 261690 vs 262142.0 (z=-0.88)
   survivors at exact Gray distance 3: 262356 vs 262141.0 (z=0.42)
   survivors at exact Gray distance 4: 263174 vs 262140.0 (z=2.02)
   survivors at exact Gray distance 5: 262720 vs 262139.0 (z=1.13)
   survivors at exact Gray distance 6: 262873 vs 262138.0 (z=1.44)
   survivors at exact Gray distance 7: 261534 vs 262137.0 (z=-1.18)
   survivors at exact Gray distance 8: 262099 vs 262136.0 (z=-0.07)
   survivors at exact Gray distance 65536: 196902 vs 196608.0 (z=0.66)
   distance-d pair counts over 17 distances: max|z|=2.02
   batches of 256 consecutive survivors of one coset: n=229559 span(Gray points) mean 65059 (expect 65280), sd 4066 (expect 4088), min 46998 max 87024
   NOTE: full coset has 2^40 points -> ~2^32 survivors per bucket; a 256-batch spans ~65k Gray points and is released in survivor order.
```

#### P6b.report.txt (the per-projection rows of section 4 are omitted; its summary lines are kept)

```
meta: mode 0 rounds 6 NC 65536 NI 262144 seed 20261015 z1 17 z2 34 bucket 165 nsurv 67098141 nsamp 16782452
== 1. survivor count: N=67098141 expected 67108864.0 z=-1.31
   filter check: 0 survivors with wrong bucket
== 2. per-bit bias over 248 non-filter digest bits: max|z|=2.51 (lane 0 bit 60), #|z|>3: 0 (exp 0.67), sum z^2=241.2 (dof 248, z=-0.31)
   key-remaining bits (lane<4,z<=34): n=132 max|z|=2.29 #|z|>3: 0 sum z^2=142.6 (dof 132, z=0.65)
   top bits: (L0,z60)=2.51 (L0,z63)=2.32 (L1,z58)=-2.30 (L1,z33)=2.29 (L0,z21)=2.26
   relative bias resolution: 1 sigma = 6.10e-05 of probability
== 3. pair-parity bias over 30628 bit pairs: max|z|=4.22 at (L2,z14)-(L2,z45); #|z|>4: 2 (exp 1.93); sum z^2 = 30415.9 (dof 30628, z=-0.86)
== 4. pair collision rates on projections (N=67098141, all-pairs 2.251e+15, within-coset pairs 3.435e+10)
   projection        m | zAll   obs/exp(all)  | zCross  obs/exp  | zWithin(obs vs exp)
   m=16: 17 projections, mean zAll 43608.19, mean zCross 43607.86, mean zWithin 170.34, max|zCross| 185335.32, #|zCross|>3: 4
   m=24: 17 projections, mean zAll 2725.82, mean zCross 2725.80, mean zWithin 10.78, max|zCross| 11585.65, #|zCross|>3: 4
   m=32: 17 projections, mean zAll 340.74, mean zCross 340.74, mean zWithin 0.92, max|zCross| 727.14, #|zCross|>3: 8
== 4b. unfiltered pseudo-random 1/1024 subsample of the same stream (n=16782452): collision-rate z on the same projections
   m=16: mean z 0.51 max|z| 1.96 over 17 projections
   m=24: mean z -0.11 max|z| 1.97 over 17 projections
   m=32: mean z -0.17 max|z| 2.36 over 17 projections
   unfiltered per-bit bias: max|z| 3.11, sum z^2 248.4 (dof 256, z=-0.33)
== 5. per-coset 256-bucket histograms (NC=65536 cosets x 262144 scanned): sum chi2 over cosets = 16711308, dof 16711680, z=-0.06
   bucket 165 per-coset count: var of z = 0.9999 (expect ~1), min z -3.69 max z 4.45, #|z|>3: 196 (exp 176.9)
   pooled 256-bucket chi2 = 243.3 (dof 255, z=-0.52); bucket 165 pooled rate / 2^-8 = 0.999840
   pooled bucket rate 3.905626e-03; full-coset (2^40) expected survivors 4.294e+09
== 6. Gray-order gaps between consecutive survivors in a coset (prefix scan, window 2^18): n=67032605 mean 255.791 var/mean^2 0.9961 ; synthetic Bernoulli null (same windows) n=67039192 mean 255.765 var/mean^2 0.9960 ; mean diff z=0.60
   log2-binned gap two-sample chi2 real vs null = 20.5 over 12 bins (z=2.03)
   gap==1 (adjacent Gray points both survive): real 2.629e+05/ 67032605 = 0.003921, null 0.003909 (geometric 2^-8 = 0.003906) z=1.11
   survivors at exact Gray distance 1: 262860 vs 262143.0 (z=1.40)
   survivors at exact Gray distance 2: 261784 vs 262142.0 (z=-0.70)
   survivors at exact Gray distance 3: 261499 vs 262141.0 (z=-1.25)
   survivors at exact Gray distance 4: 261939 vs 262140.0 (z=-0.39)
   survivors at exact Gray distance 5: 261878 vs 262139.0 (z=-0.51)
   survivors at exact Gray distance 6: 261893 vs 262138.0 (z=-0.48)
   survivors at exact Gray distance 7: 261741 vs 262137.0 (z=-0.77)
   survivors at exact Gray distance 8: 262299 vs 262136.0 (z=0.32)
   survivors at exact Gray distance 65536: 196296 vs 196608.0 (z=-0.70)
   distance-d pair counts over 17 distances: max|z|=1.40
   batches of 256 consecutive survivors of one coset: n=229547 span(Gray points) mean 65061 (expect 65280), sd 4058 (expect 4088), min 47864 max 83790
   NOTE: full coset has 2^40 points -> ~2^32 survivors per bucket; a 256-batch spans ~65k Gray points and is released in survivor order.
```

#### R6.report.txt (the per-projection rows of section 4 are omitted; its summary lines are kept)

```
meta: mode 1 rounds 6 NC 65536 NI 262144 seed 20261012 z1 0 z2 1 bucket 0 nsurv 67099676 nsamp 16774750
== 1. survivor count: N=67099676 expected 67108864.0 z=-1.12
   filter check: 0 survivors with wrong bucket
== 2. per-bit bias over 248 non-filter digest bits: max|z|=3.39 (lane 3 bit 33), #|z|>3: 1 (exp 0.67), sum z^2=218.8 (dof 248, z=-1.31)
   key-remaining bits (lane<4,z<=34): n=132 max|z|=3.39 #|z|>3: 1 sum z^2=127.6 (dof 132, z=-0.27)
   top bits: (L3,z33)=3.39 (L2,z59)=-2.90 (L0,z22)=2.54 (L0,z19)=2.40 (L3,z23)=2.38
   relative bias resolution: 1 sigma = 6.10e-05 of probability
== 3. pair-parity bias over 30628 bit pairs: max|z|=4.29 at (L0,z45)-(L2,z23); #|z|>4: 1 (exp 1.93); sum z^2 = 30757.1 (dof 30628, z=0.52)
== 4. pair collision rates on projections (N=67099676, all-pairs 2.251e+15, within-coset pairs 3.435e+10)
   projection        m | zAll   obs/exp(all)  | zCross  obs/exp  | zWithin(obs vs exp)
   m=16: 17 projections, mean zAll -0.24, mean zCross -0.24, mean zWithin -0.15, max|zCross| 1.42, #|zCross|>3: 0
   m=24: 17 projections, mean zAll 0.16, mean zCross 0.16, mean zWithin 0.02, max|zCross| 3.74, #|zCross|>3: 1
   m=32: 17 projections, mean zAll 0.36, mean zCross 0.35, mean zWithin 3.31, max|zCross| 1.28, #|zCross|>3: 0
== 4b. unfiltered pseudo-random 1/1024 subsample of the same stream (n=16774750): collision-rate z on the same projections
   m=16: mean z 0.41 max|z| 1.78 over 17 projections
   m=24: mean z -0.28 max|z| 2.99 over 17 projections
   m=32: mean z -0.03 max|z| 1.67 over 17 projections
   unfiltered per-bit bias: max|z| 3.42, sum z^2 293.5 (dof 256, z=1.66)
== 5. per-coset 256-bucket histograms (NC=65536 cosets x 262144 scanned): sum chi2 over cosets = 16715774, dof 16711680, z=0.71
   bucket 0 per-coset count: var of z = 1.0025 (expect ~1), min z -4.45 max z 4.10, #|z|>3: 178 (exp 176.9)
   pooled 256-bucket chi2 = 275.5 (dof 255, z=0.91); bucket 0 pooled rate / 2^-8 = 0.999863
   pooled bucket rate 3.905715e-03; full-coset (2^40) expected survivors 4.294e+09
```

#### R24.report.txt (the per-projection rows of section 4 are omitted; its summary lines are kept)

```
meta: mode 1 rounds 24 NC 65536 NI 262144 seed 20261014 z1 0 z2 1 bucket 0 nsurv 67112197 nsamp 16778983
== 1. survivor count: N=67112197 expected 67108864.0 z=0.41
   filter check: 0 survivors with wrong bucket
== 2. per-bit bias over 248 non-filter digest bits: max|z|=3.22 (lane 3 bit 12), #|z|>3: 2 (exp 0.67), sum z^2=290.8 (dof 248, z=1.92)
   key-remaining bits (lane<4,z<=34): n=132 max|z|=3.22 #|z|>3: 1 sum z^2=131.7 (dof 132, z=-0.02)
   top bits: (L3,z12)=-3.22 (L0,z52)=3.04 (L2,z48)=-2.98 (L1,z46)=-2.97 (L3,z54)=2.95
   relative bias resolution: 1 sigma = 6.10e-05 of probability
== 3. pair-parity bias over 30628 bit pairs: max|z|=4.48 at (L0,z12)-(L0,z40); #|z|>4: 3 (exp 1.93); sum z^2 = 30377.2 (dof 30628, z=-1.01)
== 4. pair collision rates on projections (N=67112197, all-pairs 2.252e+15, within-coset pairs 3.436e+10)
   projection        m | zAll   obs/exp(all)  | zCross  obs/exp  | zWithin(obs vs exp)
   m=16: 17 projections, mean zAll 0.01, mean zCross 0.01, mean zWithin -0.01, max|zCross| 1.70, #|zCross|>3: 0
   m=24: 17 projections, mean zAll 0.06, mean zCross 0.06, mean zWithin 0.27, max|zCross| 1.27, #|zCross|>3: 0
   m=32: 17 projections, mean zAll -0.28, mean zCross -0.28, mean zWithin 2.00, max|zCross| 2.09, #|zCross|>3: 0
== 4b. unfiltered pseudo-random 1/1024 subsample of the same stream (n=16778983): collision-rate z on the same projections
   m=16: mean z 0.12 max|z| 2.30 over 17 projections
   m=24: mean z 0.15 max|z| 1.48 over 17 projections
   m=32: mean z 0.58 max|z| 3.09 over 17 projections
   unfiltered per-bit bias: max|z| 3.56, sum z^2 262.2 (dof 256, z=0.27)
== 5. per-coset 256-bucket histograms (NC=65536 cosets x 262144 scanned): sum chi2 over cosets = 16717598, dof 16711680, z=1.02
   bucket 0 per-coset count: var of z = 1.0033 (expect ~1), min z -4.16 max z 4.29, #|z|>3: 206 (exp 176.9)
   pooled 256-bucket chi2 = 227.7 (dof 255, z=-1.21); bucket 0 pooled rate / 2^-8 = 1.000050
   pooled bucket rate 3.906444e-03; full-coset (2^40) expected survivors 4.295e+09
```

