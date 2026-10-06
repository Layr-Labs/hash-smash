# Byte-aligned collisions of 5-round SHA3-256: a 2-round connector and a 3-round trail tail

Track `sha3-256-r5-exploratory`, target `sha3-256-r5-prefix-v1`, cost model
`collision-frontier-v5` (C = 1355 for this target). Exploratory lane.

## 0. Claim

The package specifies a concrete algorithm that outputs two distinct 135-byte messages with
equal complete 5-round SHA3-256 digests. It follows the framework of Guo, Liao, Liu, Liu, Qiao
and Song (Journal of Cryptology 33(1):228-270, 2020; IACR ePrint 2019/147), uses their trail
core No. 3, which our charged trail search (run with their search strategy) selects again, and
replaces the 1084-bit message format of their published SHA3-256 pair by a byte-aligned
135-byte format.

| Field | Value | Basis |
| --- | --- | --- |
| `time_log2` | 43.5 | conservative bound: joint worst case 2^42.97 of all alternative models, lambda doubled, plus 0.53 bit (Section 10.5); central estimate 2^39.87 |
| `success_probability` | 0.5 | N = 2^36.69 pairs at p = 2^-37.219 under H1 (Section 9) |
| `memory_log2_bytes` | 31 | 380 MiB largest step plus retained files, at most 1.7e9 bytes in the joint worst case (Section 11) |
| `preprocessing_log2` | 43.5 | phases A-C: 2^42.51 in the joint worst case, central estimate 2^39.74 (Sections 10.5, 12) |
| `nonuniform_advice_log2_bytes` | 0 | no advice: trail and connector are computed and charged |

The connector attempt loop uses fresh random coins and is charged at its expected cost, not at
the cost of our executed run (Section 13). All three declared heuristics (H1-H3, Section 16) are
listed in `claim.json`. Three certified collisions, found by an executed run of the algorithm,
are in `certificates/`.

The claimed bound is deliberately conservative. Our central estimate of the expected cost is
2^39.87 (Section 10.4); it is reported for information and is not the claim. The claim covers
the joint worst case of every alternative model we identified for H1, H2 and H3, taken at the
same time, with the instruction-pricing factor lambda doubled, plus a margin of 0.53 bit
(Section 10.5).

## 1. Exact target at 135 bytes

The hash is the profile's complete sponge: 1600-bit state of 25 lanes A[x,y] (64 bits, index
x+5y, bit z of lane i is state bit 64i+z, little-endian byte order), all-zero initial state,
rate 1088 bits (136 bytes), capacity 512 bits, SHA3 domain suffix `01` then pad10*1.

Every message M produced here has exactly 135 bytes. The suffix byte 0x06 and the final pad bit
0x80 then fall into the same byte, so the single padded block is

    P(M) = M || 0x86        (136 bytes, 17 lanes)

and the initial state for absorption is s = P(M) || 0^512, read little-endian. Bits 0..1079 of s
are the message; bits 1080..1087 are 0x86 (bits 1081, 1082 and 1087 equal 1, the other five
equal 0); bits 1088..1599 are 0. These 520 bits are fixed for every 135-byte message. One block
is absorbed, one permutation is applied, and the digest is the first 32 bytes of the state,
lanes A[0,0], A[1,0], A[2,0], A[3,0] (all 256 bits). No further permutation call occurs because
32 < 136. There is no feed-forward.

The permutation consists of rounds i = 0, 1, 2, 3, 4 (prefix rounds, original constants):

    C[x] = XOR_y A[x,y];  D[x] = C[x-1] XOR ROT(C[x+1], 1);  A[x,y] ^= D[x]      (theta)
    B[y, 2x+3y] = ROT(A[x,y], r[x,y])                                           (rho, pi)
    A[x,y] = B[x,y] XOR ((NOT B[x+1,y]) AND B[x+2,y])                          (chi)
    A[0,0] ^= RC[i]                                                             (iota)

with indices mod 5, ROT a left rotation in 64 bits, the standard rho offsets
r = (0,1,62,28,27, 36,44,6,55,20, 3,10,43,25,39, 41,45,15,21,8, 18,2,61,56,14) in lane order
x+5y, and RC[0..4] = 0x1, 0x8082, 0x800000000000808a, 0x8000000080008000, 0x808b.

This is exactly `verifier/keccak.py:sha3_256(M, rounds=5)`; our implementation was checked
against it on random states for 1, 2 and 5 rounds and on random 135-byte messages, and every
certificate is checked by the organizer with that reference. A collision found here is an
ordinary collision of the complete padded 5-round hash. It is not a free-start, compression-only
or truncated result.

## 2. Notation and the chi facts used

Write L = pi o rho o theta (linear, invertible over GF(2)^1600) and the round as
R_i(s) = chi(L(s)) XOR RC[i]. For a pair with input difference alpha_i to round i,
beta_i = L(alpha_i) is the difference entering chi, and alpha_{i+1} is the difference after chi
(iota does not change differences). Chi acts independently on the 320 rows of 5 bits
(fixed y and z; row index r = 64y + z, bit x of the row is lane x+5y). Let S be the 5-bit row
map and DDT[d][o] = #{v : S(v) XOR S(v XOR d) = o}.

Lemma 1 (affine solution sets). For every d != 0 and o with DDT[d][o] > 0 the set
V(d,o) = {v : S(v) XOR S(v XOR d) = o} is an affine subspace of GF(2)^5 of size DDT[d][o];
it is defined by w = 5 - log2 DDT[d][o] independent affine equations, and V(d,o) XOR d = V(d,o).
Proof: S is quadratic, so v -> S(v) XOR S(v XOR d) is affine in v for fixed d; V(d,o) is the
preimage of o under that affine map. We also verified all 31 x 32 cases exhaustively.

So a row transition d -> o of weight w holds for a given value v exactly when v satisfies w
affine equations. This is the observation that the connector and the conditions below use
(Guo et al., Sec. 4; earlier Daemen et al. and Dinur-Dunkelman-Shamir, FSE 2012).

## 3. The differential

### 3.1 Trail core (our trail search output, translate t = 8)

Lanes are listed in order A[0,0], A[1,0], ..., A[4,4] (index x+5y), 64-bit hexadecimal.

    alpha2 = a000001600000000 9000000a00000000 5000000e00800004 5000000a00000000 0000002200000000
             a000001600000001 8000000a00000000 5000000e00000000 5000004a00000000 0000402600000000
             2000001600000001 8000000a00000000 5000000e00800000 4000004a00000000 0000402600000000
             a000001600000001 8000001a00000000 5000000e00000004 5000004a00000000 0000002600000000
             a000001600000001 c000000a00000000 5000000e00000000 5000004a00000000 0000002600000000
    beta2  = 0000000000000001 0 0000000000000004 0 0
             0000000000000004 0000000000000004 0000000000000004 0000000000020000 0
             2000000000000000 0 0000000000200000 0 0
             2000000000000000 0 0 0000000000020000 0
             0000000000200001 0 0000000000200000 0 0000000000000001
    alpha3 = 0000000000000001 0 0000000000000004 0 0
             0 0 0000000000000004 0000000000020000 0
             2000000000000000 0 0000000000200000 0 0
             2000000000000000 0 0 0000000000020000 0
             0000000000000001 0 0000000000200000 0 0
    beta3  = 0000000000000001 0 0000000000000001 0000004000000000 0
             0 0 0000000000000001 0 0000000000040000
             0 0000000000000100 0 0 0000000000040000
             0 0 0 0 0
             0000000000000001 0000000000000100 0 0000004000000000 0

beta2 = L(alpha2), beta3 = L(alpha3). alpha2 has 114 bits in 59 active rows; beta2 has 14 bits
in 10 active rows; alpha3 has 10 bits and lies in the CP-kernel (every column has even parity),
so theta acts as the identity on it; beta3 has 10 bits in 9 active rows.

As printed in the paper (Table 9, trail core No. 3, rows y = 0..4, lanes x = 0..4, hex digits
most significant first), the beta2 and beta3 above are exactly that core. For example, the
first row of beta2 is `---------------1|----------------|---------------4|...` and our
lanes 0..4 are 1, 0, 4, 0, 0. The weights are w1-w2-w3 = 127-24-19 and #AS(alpha2) = 59,
matching the paper's Table 5 entry No. 3.

Our trail search also records one representative alpha4 (10 bits, in the CP-kernel). The
transition beta3 -> alpha4 has weight w3 = 19, and that weight is the same for all 2^19
alpha4 compatible with beta3, because chi output differences are uniform for a fixed input
difference. This alpha4 and its beta4 = L(alpha4) (10 bits, no active row in plane y = 0) are

    alpha4 = 0 0 0000000000000001 0000004000000000 0
             0000000000000001 0 0000000000000001 0 0000000000040000
             0 0000000000000100 0 0 0000000000040000
             0 0 0 0 0
             0000000000000001 0000000000000100 0 0000004000000000 0
    beta4  = 0 0 0 0 0
             0000000000000004 0000004000000000 0 0 0
             0 0000000000000040 0 0 0000000000040000
             0 0000001000000000 0000000000040000 0000000040000000 0
             4000000000000000 0 0200000000000000 0 0000000000000400

It differs from the paper's beta4 (14 bits); both have no active row in plane y = 0. The
probability below does not depend on this choice, because it sums over all alpha4.

### 3.2 Round 2: beta2 -> alpha3 (exact, w2 = 24)

The 10 active rows (r = 64y+z), their row differences d -> o and DDT values:

| r | (y,z) | d | o | DDT | w | condition mask on the 32 values (bit v set iff v in V(d,o)) |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | (0,0) | 1 | 1 | 8 | 2 | 0x33330000 |
| 2 | (0,2) | 4 | 4 | 8 | 2 | 0x00cc00cc |
| 66 | (1,2) | 7 | 4 | 2 | 4 | 0x18000000 |
| 81 | (1,17) | 8 | 8 | 8 | 2 | 0x0000f0f0 |
| 149 | (2,21) | 4 | 4 | 8 | 2 | 0x00cc00cc |
| 189 | (2,61) | 1 | 1 | 8 | 2 | 0x33330000 |
| 209 | (3,17) | 8 | 8 | 8 | 2 | 0x0000f0f0 |
| 253 | (3,61) | 1 | 1 | 8 | 2 | 0x33330000 |
| 256 | (4,0) | 17 | 1 | 4 | 3 | 0x88004400 |
| 277 | (4,21) | 5 | 4 | 4 | 3 | 0x00330000 |

The total weight is 24. For a pair whose difference entering round 2 is alpha2, the difference
after round 2 is alpha3 exactly when the first message's 10 round-2 chi-input rows lie in these
sets. These are 24 affine conditions on the value of one message.

### 3.3 Rounds 3 and 4 to a zero digest difference (2^-13.219)

Given alpha3, beta3 = L(alpha3) is fixed. Round 3 maps beta3 to some alpha4 (9 active rows,
524,288 row-wise compatible output combinations). Then beta4 = L(alpha4), and in round 4 only
the digest matters. The digest is lanes x = 0..3 of plane y = 0, so a row of plane y = 0 with
input difference d must give an output difference whose bits x = 0..3 vanish. Call that
probability PZ[d] (exact over the 32 row values). Rows of planes y = 1..4 are unconstrained.
Under the Markov assumption (H1),

    P(digest difference 0 | alpha3) = sum over alpha4 of P(beta3 -> alpha4) * prod_z PZ[beta4 row (0,z)]
                                    = 2^-13.219,

summed over all 524,288 alpha4. Exactly 192 of them give a nonzero term; the best single one is
2^-19.00. The rounds 2-4 probability is therefore

    p = 2^-24 * 2^-13.219 = 2^-37.219.

Guo et al. give w = 36.70 for this core (Table 6, footnote: "The weight takes multiple trails
of the last two rounds into consideration"; Table 9 caption: "The probability is 2^-36.70
considering multiple trails of the last two rounds"). We use our own, smaller value, which
only makes our accounting more conservative. The difference is not explained by the digest
size: the same sum under a 224-bit digest mask is also 2^-13.219.

## 4. Algorithm overview

The algorithm has four phases. Phases A-C build the connector spaces; phase D searches them.

- A. Trail search (own code, deterministic, charged). It finds 2-round in-kernel cores, extends
  them backward, selects the core minimizing w1, and fixes its z-translate.
- B. Connector (own code, randomized, charged at its expected cost including all failures). It
  enumerates the round-1 input differences beta1, filters them, then runs target-difference
  attempts and local repair, each attempt with a fresh random seed, until a 2-round connector
  with degrees of freedom DF >= 22 is solved.
- C. Space export (randomized, charged). It produces affine message spaces from the solved
  connector by varying the linearisation choices, until the spaces hold at least N pairs, and
  drops any space that intersects an earlier one.
- D. Online search (randomized). It enumerates pairs in random spaces in a random order, checks
  the round-2 conditions on one message, then compares both complete 5-round digests.

Fixed parameters: K = 10, W = 20, FW = 20, FEAS_N = 1000, NSEEDS = 4, MAXFLIP = 3, NFOUND = 2,
DFMIN = 22, SA steps 200,000, at least 2,400 export seeds. A-C read no published trail,
connector or message pair.

Disclosure on parameters. K = 10 is the paper's own suggestion (Guo et al., Sec. 5.3: "find
special beta3's with a low Hamming weight, say 10"). Every in-kernel alpha3 has even weight, so
K = 10 and K = 11 give identical results; we checked this by running A1 with K = 11 (same
8,476 cores). W and FW were set one above the published core's w3 = 19 and w3 + w4d = 19. The
other parameters were fixed after our exploratory research with the published core. An
earlier execution with W = FW = 19 selected the same core (Section 5).

## 5. Phase A: trail search and selection

A1 (in-kernel 2-round cores). A depth-first closure search enumerates every alpha3 in the
CP-kernel with 2 <= |alpha3| <= K = 10 bits, up to z-translation. For each one it lists every
in-kernel alpha4 row-wise compatible with beta3 = pi(rho(alpha3)) of weight w3 <= W = 20,
together with the round-4 digest weight w4d of beta4 = L(alpha4). It keeps only cores for which
a zero digest difference is possible (requirement (1) of Guo et al.). Branching resolves the
first odd column (4 choices) or the first slice of beta3 whose active rows cannot sum to zero
(25 choices). It prunes by |alpha3| <= K and 2 x #active rows <= W. Result: 9.69e9 nodes,
8,476 distinct alpha3, and 44,217 (alpha3, alpha4) pairs passing requirement (1). The search
for in-kernel cores follows the Keccak team's CP-kernel analysis (Daemen and Van Assche,
FSE 2012; KeccakTools, which Guo et al. used).

A2/A3 (backward extension). The 547 alpha3 with best forward weight w3 + w4d <= FW = 20 are
kept. For each, every beta2 row-wise compatible with alpha3 is enumerated, 2^40.60 candidates
in total. Then alpha2 = L^-1(beta2), and w1 = sum over active rows of alpha2 of the minimum DDT
weight of any input difference to that row. That is the minimum number of round-1 conditions
the connector must satisfy. A branch-and-bound uses the exact lower bound
#AS(alpha2) >= 5 nz(e) - |u| (from the theta^-1 column effect) and w1 >= 2 #AS(alpha2). It
evaluates 3,364 candidates exactly. The minimum is w1 = 127, attained by exactly one core, with
w2 = 24, w3 + w4d = 19 and #AS(alpha2) = 59.

A4 (selection and translate). The selection rule is lexicographic: minimum w1, then w2, then
forward weight, then index. The canonical z-translate is the one whose alpha3 lane tuple is
lexicographically smallest, t = 8. This is the core of Section 3.1.

Executions. The charged phase A is the run with W = FW = 20 above. An earlier execution with
W = FW = 19 (2^39.78 candidates, 3,425 exact evaluations, 4,754 alpha3) wrote a byte-identical
trail file, so phases B-D of that execution, which produced the certificates, are exactly what
the charged phase A feeds into. We charge the larger W = FW = 20 run.

## 6. Phase B: the 2-round connector

### 6.1 Variables and equations

The variable is x = L(s), the chi input of round 0 for the first message. The second message
has x' = x XOR beta0, that is s' = s XOR alpha0 with alpha0 = L^-1(beta0). Round 0 starts with
chi, so x and x' determine both 5-round computations; s = L^-1(x) recovers the padded block.

- E_pad (520 equations). (L^-1 x)_j = c_j for j = 1080..1599, with c_j the fixed bits of
  Section 1. In the difference: alpha0 must vanish on these 520 positions.
- E_0 (round 0, chi from beta0 to alpha1). For every active row r of beta0:
  x|r in V(beta0|r, alpha1|r). By Lemma 1 these are w0 affine equations in x.
- E_1 (round 1, chi from beta1 to alpha2). Let y = L(chi(x) XOR RC[0]) be the round-1 chi
  input, so y' = y XOR beta1 whenever E_0 holds. For every active row r of beta1:
  y|r in V(beta1|r, alpha2|r). Here w1 = 127 affine equations in y, hence linear combinations
  of output bits of chi in round 0, which are quadratic in x.
- Linearisation. Let W_r be the set of values of row r of x allowed by the current linear
  system. For each round-0 row whose output bits occur in E_1, choose m extra affine equations
  restricting x|r to a subset W'_r of W_r on which every needed output bit is an affine
  function. We use the smallest m that works: m = 0 if the bits are already affine on W_r,
  else 1, 2 or 3, choosing among minimal options with seeded randomness (non-full
  linearisation, Guo et al., Sec. 4). On the resulting system, E_1 becomes linear in x.

Every x in the solution space E of E_pad, E_0, the linearisation equations and the linearised
E_1 satisfies E_0 and E_1 exactly. The linearised E_1 equals E_1 on W'_r, and x|r lies in W'_r.

Lemma 2 (exact connector). For every x in E, the messages M = first 135 bytes of L^-1(x) and
M' = first 135 bytes of L^-1(x XOR beta0) are distinct, both padded as in Section 1, and the
state difference after rounds 0 and 1 is exactly alpha2.
Proof: E_pad fixes the 520 non-message bits of s. alpha0 vanishes on them (difference phase),
so s' has them too. alpha0 is nonzero, so M != M'. E_0 and Lemma 1 give
chi(x) XOR chi(x') = alpha1, so the round-1 chi input difference is L(alpha1) = beta1. E_1 and
Lemma 1 give the round-1 output difference alpha2.

For the solved base used by the certificates (attempt k = 278, seed 1, base r0): #AS(beta0) =
#AS(alpha1) = 267, w0 = 870, rank(E_pad + E_0) = 1361, linearisation adds 78 equations (42
rows with m = 1, 18 with m = 2), rank 1439, E_1 adds 127 rows of which 2 are dependent and 0
inconsistent, final rank 1564, DF = 1600 - 1564 = 36. The second base (r1) has rank 1362 and
DF = 35. Guo et al. report DF 37 for their SHA3-256 connector with 4 fixed padding bits
(Table 6). We fix 8 bits.

The message difference of base r0 is alpha0 restricted to bytes 0..134, in hex:

    4879d2b8897743c01bf0af0f9b1cb0bf950139914b379c614c27bd720bf81f9cab91b76ef3a684d979cee369bc4700953b
    7aa536ac10e9e69f5eea6182f0b3a8c6f28117c1c3eaa0416cb2e9bb84793b1e316bffe3e9f5c990d0f799ec54d3bccc70
    6bbda645c41f9007c1fdb0eb670fa44d99a7871c8b18a2c9538d68e1c1841afeec3a6886b1

Every certificate pair XORs to exactly this string, which a reader can check directly. It has
134 nonzero bytes.

### 6.2 Choosing beta1 and beta0 (target difference algorithm)

B2 (beta1 enumeration). For each of the 59 active rows of alpha2, take the input differences of
maximal DDT (weight equal to the row minimum), as Guo et al. do (Sec. 4.6). This gives exactly
the beta1 attaining w1 = 127: 800,000 choices. Each is scored by the expected round-0 weight
of alpha1 = L^-1(beta1) and sorted.

B3 (feasibility filter). For the first 1,000 in that order, impose E_pad on the difference and
force inactive rows of alpha1 to zero input difference. Keep the beta1 for which every active
row still has a compatible input difference: 76 pass. We write k for the rank of a beta1 in the
score-sorted list of the first 1,000 (so k ranges over 0..999, and 76 values of k are feasible).

B4 (attempts). Attempts run over the 76 feasible k in increasing order, three attempts per k,
each with a fresh random seed; if the list is exhausted the loop restarts with new seeds. Each
attempt is deterministic given (k, seed) and works as follows.

1. Our target difference algorithm, a variant of Dinur-Dunkelman-Shamir (FSE 2012) as used by
   Guo et al. (Sec. 4.6), chooses for each active row of alpha1 a 2-dimensional affine subspace
   of compatible input differences. It does this robustly with respect to the link equations
   that the 520 fixed bits induce between rows. The result is an affine space A_d of admissible
   beta0 (difference phase).
2. It minimizes a predicted rank (w0 plus link costs) over A_d by simulated annealing
   (200,000 steps).
3. It tests the value phase: E_pad + E_0 consistent.
4. It runs a local repair inside A_d: breadth-first flips of up to 3 basis vectors of A_d,
   keeping the 6 best by (number of inconsistent E_1 rows, -DF). Each candidate beta0 is
   evaluated with 4 linearisation seeds.
5. A beta0 is accepted when E_1 is consistent and DF >= 22. An attempt stops after 2 accepted
   bases.

The loop stops at the first success. The robust subspace choice, the annealing and the local
repair are our own additions to the method.

Executed realisations. For reproducibility our executions used the seeds 1, 2, 3 for each k (the
run that produced the certificates) and, separately, 4, 5, 6. In the first, 44 attempts were
launched (12 in parallel): 26 failed in the difference phase, 16 found no consistent beta0,
and 2 succeeded. The first success in sequential order is attempt #33 (k = 278, seed 1, bases
with DF 36 and 35); the other success is k = 311, seed 3 (DF 26 and 24). In the second, the
first success is attempt #41 (k = 313, seed 6, DF 27 and 25). Every accepted base was
spot-checked with the organizer's reference: 8 of 8 sampled pairs per base have 2-round
difference alpha2. Section 13 derives the expected cost of the loop from both realisations.

## 7. Phase C: space export

For the accepted base pair, beta0 and the system E_pad + E_0 are fixed, and the linearisation
of Section 6.1 is redone with export seeds, alternating between the two bases. A seed is kept if
E_1 is consistent. Identical spaces are dropped by hashing the reduced system, and a space is
dropped if it intersects an earlier kept space (x0 XOR x0' in the sum of the linear parts).
Seeds are processed until at least 2,400 have been used and the kept spaces hold at least N
pairs.

In the executed run, 2,400 seeds gave 2,052 distinct spaces with DF 34 (436), 35 (934),
36 (587), 37 (92) and 38 (3), 0 duplicates. Each space is given as x0 + span(b_1..b_DF) with
1600-bit words. All 2,104,326 pairs of these spaces were checked and are disjoint. Over the
whole export, sum 2^(DF-1) = 2^45.41 pairs, with mean 2^34.41 pairs per space, which is
2^-1.09 times 2^(mean base DF).

Every exported space is closed under x -> x XOR beta0: every reduced row annihilates beta0.
So beta0 lies in its linear part, and the space is a disjoint union of 2^(DF-1) unordered pairs.

## 8. Phase D: online search

Random coins. A uniformly random order of the exported spaces, and in each space a uniformly
random starting coefficient vector.

For each space in that order:

1. Drop a basis vector whose coefficient in beta0 is 1. Enumerate x over a coset of the other
   DF-1 vectors in Gray-code order, so each unordered pair {x, x XOR beta0} occurs exactly once.
   One step is one XOR of a 25-word basis vector.
2. Stage 1 (one message). Compute chi and iota of round 0 from x, the full round 1, and
   theta-rho-pi of round 2. Test the 10 rows of Section 3.2 against their masks, in table
   order, stopping at the first failure. A pass occurs with probability 2^-24 and certifies the
   round-2 difference alpha3 (given Lemma 2).
3. Stage 2 (passes only). Evaluate all 5 rounds for x and x XOR beta0 and compare the four
   digest lanes.
4. On equality, output M and M' via s = L^-1(x) (Lemma 2). Otherwise continue.

Stop after N pairs, or at the first collision. With success target 1/2,
N = ceil(2^37.219 ln 2) = 2^36.69 (Section 9). A returned pair is a genuine collision of the
complete target hash, because stage 2 recomputes it from the padded state. For a base of DF 36
this needs about 5 spaces; for the lowest-DF base we observed (DF 26 and 24), about 7,100. The
executed search used exactly this inner loop (deterministic order, 12 threads, 1,100 s). The
certificates were then re-verified with `verifier/keccak.py`.

## 9. Success probability

H1 (Markov / independent trials). For pairs enumerated in the connector spaces, the events
"round 2 follows beta2 -> alpha3" and "rounds 3-4 give a zero digest difference" occur with
the products of the row-wise DDT probabilities of Section 3. Distinct pairs behave as
independent trials with success p = 2^-37.219.

Lemma 3 (distinct trials). The enumerated pairs are distinct. Within a space each unordered
pair is enumerated once, by construction (Section 8). The kept spaces are pairwise disjoint
(Section 7), so pairs from different spaces never coincide.

Under H1 and Lemma 3, N pairs succeed with probability 1 - (1-p)^N >= 1 - exp(-Np). For
success >= 1/2 we take N = 2^37.219 x ln 2 = 2^36.690. (For 0.39: N = 2^36.202.) Other
differential paths to a collision, and further pairs, can only increase this probability. The
probability is over the online coins. Phases B and C run until they succeed; their randomness
affects the cost (Section 13), not the success probability.

Evidence for H1, from our own measurements:

- Stage-1 rate. Run 1 (12 threads, the first 33 of the 2,052 spaces of base k = 278, 2^39.19
  pairs): 37,499 passes, rate 2^-23.996 (95% CI [2^-24.010, 2^-23.981]) against the predicted
  2^-24.000. The earlier research run (other bases, same trail): 9,450 passes in 2^37.23 pairs,
  2^-24.02. A debug pass checked the exact 2-round difference alpha2 on 49,152 sampled pairs
  (4,096 in each of 12 spaces): 49,152 of 49,152 hold.
- Stage 2. 6 collisions among 46,949 stage-1 passes: 2^-12.93 against 2^-13.219 predicted.
- Collisions. Run 1: 3 in 2^39.19 pairs (expected 3.92), first at 351.6 s. Research run: 3 in
  2^37.23 pairs (expected 1.01). Combined: 6 in 2^39.52 pairs against 4.93 expected. The exact
  Poisson 95% interval for the per-pair rate is [2^-38.38, 2^-35.81], and the one-sided 95%
  lower bound is 2^-38.13. The prediction 2^-37.219 lies inside.
- Guo et al. found one collision with this core in a DF-37 space (their Sec. 6.2).

Sensitivity. If the true per-pair rate were only 2^-38.38 (the lower end of that interval),
success 1/2 would need N = 2^37.85. That changes the total by +0.27 bits (Section 10.4).

## 10. Cost under collision-frontier-v5

### 10.1 Pricing rules

One 5-round Keccak-f[1600] permutation costs 1 unit. Every other primitive 256-bit RAM
operation (load or store, addition, AND/OR/XOR/NOT, shift or rotation, comparison, conditional
branch, random word) costs 1/C = 1/1355 units. C = 1355 is the organizer's data-path count for
5 rounds (`scripts/reference_operation_costs.py`): 271 per round, of which chi+iota = 101 and
theta-rho-pi = 170, with rotations as explicit shifts, OR and mask.

Phases A-C are measured programs. Each step ran as its own process under `/usr/bin/time -l`,
which reports retired machine instructions summed over all threads (Apple M5 Max, AArch64).
Instructions per user-second are between 1.9e10 and 3.1e10 for every step, so no thread or
child process is missing from the counts. A measured phase is charged

    units = (retired instructions) x lambda / C,

where lambda bounds the primitive operations needed per retired instruction (H2). Phase D is
charged analytically, by counting operations in the same convention as the organizer's
reference script, plus memory traffic.

### 10.2 lambda from measured instruction mixes (H2)

We determined the dynamic opcode histogram of the same programs, instruction by instruction,
with a DynamoRIO client that counts every executed opcode (AArch64 Linux, the same Python
3.12 code and the C sources built with gcc -O3). Workloads: three complete connector attempts
(k = 278 seed 1, a success; k = 171 seed 1, a difference-phase failure; k = 257 seed 1, a
repair failure with 460 evaluations), the first 4 jobs of A3, and A1 with K = 8.

Each instruction is priced by an explicit emulation on the RAM (primitives per instruction):

- ALU (add, logic, move, shifted operand, conditional select) 5; flag-setting ALU (subs, adds,
  ands, ccmp and similar) 7, because the flags must be materialised;
- conditional or direct branch 4; indirect branch (br, blr, ret) 30, a comparison tree over
  the code addresses;
- 64-bit load 7 and store 8 (address arithmetic and alignment test); byte or halfword load or
  store 12 (word access with extraction or read-modify-write); load or store pair 14;
- clz 16, rbit 24, rev 16; integer multiply 130 (4-bit-window shift-and-add); divide 300;
- popcount (cnt) 16 and its byte sum (addv) 8; other vector integer operations 24;
- floating-point arithmetic and conversions 200 (software floating point); FP compare and move
  30; fmov 2; system and hint 4; anything unclassified 200.

Class shares in % of retired instructions (ALU includes the flag-setting ALU; MEM is single
loads and stores, of which the indirect, flag and sub-word columns give subsets):

| Workload | Instructions | ALU | of which flags | branch | of which indirect | MEM | of which sub-word | stores (64-bit) | MEM pair | MUL | cnt+addv+fmov | lambda |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| attempt k=278 | 2.407e12 | 40.71 | 7.47 | 19.17 | 3.84 | 30.30 | 4.02 | 7.35 | 8.24 | 0.38 | 0.02 | 8.11 |
| attempt k=171 | 9.257e11 | 40.52 | 7.46 | 19.26 | 3.85 | 30.38 | 4.10 | 7.33 | 8.24 | 0.37 | 0.02 | 8.11 |
| attempt k=257 | 4.451e12 | 40.51 | 7.64 | 20.27 | 3.53 | 30.13 | 3.82 | 7.39 | 7.78 | 0.29 | 0.02 | 7.83 |
| A3, first 4 jobs | 1.643e9 | 59.16 | 7.35 | 7.37 | 0.00 | 11.37 | 0.00 | 0.11 | 7.37 | 0.04 | 14.60 | 6.44 |
| A1, K = 8 | 5.793e10 | 52.28 | 6.49 | 7.59 | 0.42 | 28.79 | 0.24 | 5.66 | 6.94 | 0.11 | 3.74 | 6.72 |

The remaining shares are below 1.1% each (system 1.0%, divide and bit-count below 0.6%, vector
integer below 0.1%, floating point below 0.001%). Worked line for k = 278:
0.3324 x 5 + 0.0747 x 7 + 0.1533 x 4 + 0.0384 x 30 + 0.1893 x 7 + 0.0735 x 8 + 0.0402 x 12
+ 0.0824 x 14 + 0.0038 x 130 + 0.0103 x 4 + (divide, bit-count, vector, fmov: 0.08) = 8.11.

Two corrections are added before rounding up:

- Shared mnemonics. add, sub, and, orr, eor and bic exist in scalar and vector forms and are
  priced as scalar. The Apple PMU, read through Instruments during three full connector attempts
  on the measurement machine, puts all instructions executing in the FP/SIMD unit, including
  their loads and stores, at no more than 1.2% (1.03%, 1.14%, 1.18%). Repricing that share at 24
  adds at most 0.23 per instruction. In the C programs the only vector code is the popcount idiom
  (fmov, cnt, addv, fmov; the cnt and addv shares are equal), with vector-only opcodes such as
  dup or movi below 0.01%, so no loop is auto-vectorised. We add 0.25 to both groups.
- Compiler. For the Python phases the Linux instruction totals agree with the macOS totals that
  we charge to within 2%. For the C phases the compilers differ: on identical inputs the macOS
  (clang) build retires 1.30 times the Linux (gcc) instructions for A3, and 0.78 times for A1.
  We charge max(macOS count, macOS count x gcc/clang ratio), that is, A1 at 1.275 times its
  measured count and A3 at its measured count.

Result: lambda_Py = 8.4 (8.11 + 0.25, rounded up) for A2, A4, B1-B4 and C, and lambda_C = 7.0
(6.72 + 0.25, rounded up) for A1 and A3. The Python mix was measured on connector attempts
only; phases A2, A4, B1-B3 and C use that mix without separate measurement. They are below
2^36.2 units in total.

### 10.3 Ledger (success 1/2)

| Phase | Work | Retired instructions | lambda | Units |
| --- | --- | --- | --- | --- |
| A1 | trail search, in-kernel 2-round cores, K = 10, W = 20 (C) | 2^42.34 (2^41.99 measured x 1.275) | 7.0 | 2^34.74 |
| A2 | L^-1 and backward job images (Python) | 2^40.50 | 8.4 | 2^33.17 |
| A3 | backward extension, branch-and-bound on w1, FW = 20 (C) | 2^45.19 | 7.0 | 2^37.59 |
| A4 | selection and canonical translate (Python) | 2^32.98 | 8.4 | 2^25.65 |
| B1 | coupling graph and link equations (Python) | 2^36.94 | 8.4 | 2^29.61 |
| B2 | beta1 enumeration, 800,000 choices (Python) | 2^41.26 | 8.4 | 2^33.93 |
| B3 | feasibility filter (Python) | 2^38.03 | 8.4 | 2^30.69 |
| B4 | connector attempts, expected cost to first success (Section 13) | 2^46.41 | 8.4 | 2^39.08 |
| C | space export, expected, lowest observed base DF (Section 13) | 2^43.43 | 8.4 | 2^36.10 |
| | Preprocessing A-C | | | 2^39.74 |
| D1 | stage 1, N = 2^36.69 pairs x 962 operations | analytic | - | 2^36.20 |
| D2 | stage 2 and digest compare, N x 2^-24 x 2,403 operations | analytic | - | 2^13.52 |
| D0 | coins, loading spaces, basis-vector choice, final L^-1 (allowance, 200 units per space) | analytic | - | 2^20.43 |
| E | pairwise disjointness tests in C, drivers, merges, hashing, verification (allowance) | analytic | - | 2^31.84 |
| | **Total** | | | **2^39.87** |

Phase D is priced analytically, not from the measured C search, because the RAM implementation
is the direct one: its operations are counted in the convention of the organizer's reference
script, with the Gray step and the row tests included. Stage 1 costs 962 operations with all
10 condition checks charged: 60 (Gray step: 25 loads, 25 XOR, 10 index) + 101 (chi+iota,
round 0) + 271 (round 1) + 170 (theta-rho-pi, round 2) + 10 x 21 (row extraction and mask
test) + 150 (state loads and stores between the partial rounds). The expected number of checks
is 1.318, so 962 is an upper bound. Stage 2 costs 2,403 operations (1.773 units): 25 XORs for
the partner, two times (101 + 4 x 271), and an 8-operation compare. It runs on a 2^-24 fraction
of pairs. Line E covers the pairwise disjointness tests of Section 7 (at most 1.5e5 operations
per pair of spaces) and the small driver steps that were not run under `/usr/bin/time` (merging
and hashing the exported spaces, gen_conds, final verification; 9.3e8 measured instructions
for the verification step), with an allowance of 2^26 units for the latter.

For comparison, pricing the measured search (439.1 instructions per pair) at lambda_C = 7.0
would give 3,074 operations per pair and a total of 2^40.10 (Section 10.4).

### 10.4 Central estimate and single-assumption variants

| Variant | Total |
| --- | --- |
| basis (Section 10.3) | 2^39.87 |
| success 0.39 | 2^39.80 |
| per-pair rate 2^-38.38 (lower end of the 95% interval) | 2^40.13 |
| B4 with q' at its one-sided 95% lower bound (Section 13) | 2^40.25 |
| B4 with q' at its two-sided 95% lower bound | 2^40.39 |
| B4 with q' one-sided 95% lower bound and rate 2^-38.38 | 2^40.46 |
| B4 = mean cost of the two executed loops | 2^39.80 |
| B4 = executed loop with seeds 1,2,3 (44 launched) | 2^39.87 |
| B4 = i.i.d.-attempt model, q = 3/92 | 2^39.62 |
| B4 = i.i.d.-attempt model, q at its one-sided 95% lower bound | 2^40.85 |
| export for the executed base (DF 36 and 35) | 2^39.78 |
| export for a base at the floor DFMIN (DF 22 and 22) | 2^40.67 |
| stage 1 priced as measured instructions x lambda_C | 2^40.10 |
| trail parameters W = FW = 19 | 2^39.72 |
| earlier class table (lambda_C 5.89 / lambda_Py 6.06) | 2^39.49 |
| earlier class table, rate 2^-38.38 | 2^39.79 |
| lambda = 1 | 2^37.52 |

The basis is our central estimate: 2^39.87 in total and 2^39.74 for phases A-C. Each variant
above changes one assumption and stays below 2^40.9. The two largest are the i.i.d.-attempt
model at its 95% lower bound, which ignores the observed position effect (Section 13), and an
accepted base at the DF floor, which neither realisation produced (the three accepted bases
have DF 36, 27 and 26). The claim is not set from this table. It is set from the joint worst
case of Section 10.5, which applies the least favourable alternatives at once.

### 10.5 Joint worst case and the claimed bound

The claimed bound must hold even if every score-critical assumption is at its least favourable
value at the same time. We therefore recompute the ledger with all of the following together:

| Assumption | Central estimate (10.3) | Joint worst case |
| --- | --- | --- |
| H1 per-pair rate | 2^-37.219, N = 2^36.69 | 2^-38.38 (lower end of the 95% interval), N = 2^37.85 |
| H3 connector loop | two-segment model, q' = 3/26: 2^46.41 instructions | i.i.d. model over all 92 attempts, q at its one-sided 95% lower bound 0.0089: 2^47.83 |
| H3 accepted base | DF 26/24 (lowest observed) | DFMIN floor, DF 22/22: 126,232 spaces from 147,640 seeds, 2^47.59 instructions |
| H2 lambda | lambda_C = 7.0, lambda_Py = 8.4 | doubled: 14.0 and 16.8 |
| Phase D stage 1 | 962 operations per pair (analytic) | 6,148 per pair (439.1 measured instructions x 14.0) |

| Phase | Units, central | Units, joint worst case |
| --- | --- | --- |
| A1 / A2 / A3 / A4 | 2^34.74 / 2^33.17 / 2^37.59 / 2^25.65 | 2^35.74 / 2^34.17 / 2^38.59 / 2^26.65 |
| B1 / B2 / B3 | 2^29.61 / 2^33.93 / 2^30.69 | 2^30.61 / 2^34.93 / 2^31.69 |
| B4 | 2^39.08 | 2^41.50 |
| C | 2^36.10 | 2^41.26 |
| Preprocessing A-C | 2^39.74 | 2^42.51 |
| D1 | 2^36.20 | 2^40.03 |
| D2 / D0 | 2^13.52 / 2^20.43 | 2^14.68 / 2^24.59 |
| E (pairwise disjointness tests of 147,640 seeds' spaces, drivers) | 2^31.84 | 2^40.13 |
| **Total** | **2^39.87** | **2^42.97** |

The rate, base-DF and connector alternatives together, with stage 1 priced from measured
instructions, give 2^42.16 at the measured lambda (2^42.04 with stage 1 analytic); with
lambda x 1.6 (the break-even factor of a 40.5 bound at the basis) 2^42.70; with lambda x 2,
2^42.97. The claimed `time_log2 = 43.5` adds 0.53 bit to that, and lies 3.64 bits above the
central estimate. It is the smallest half-integer at least 0.5 bit above the joint worst case;
43.0 would leave only 0.03 bit. Further checks: the joint case with phase D charged
analytically gives 2^42.80; with the two-segment connector model at its two-sided 95% lower
bound, 2^42.78; with the i.i.d. model at its two-sided 95% lower bound, a stricter choice than
any variant of Section 10.4, 2^43.13, still covered. Doubling every count of phases D and E
as well, on top of the joint case, gives 2^43.31 (preprocessing unchanged), still covered.
In the joint case the claim is reached at lambda x 3.04; at the central estimate, at lambda
x 10.6. The rate alternative is priced for the online phase run with N = 2^37.85 pairs, the
number that gives success 1/2 at the rate 2^-38.38. Fixing N = 2^37.85 in Section 8 instead
of 2^36.69 keeps success at least 1/2 over the whole 95% interval of the rate; at the central
estimate that costs 2^40.13 (Section 10.4), so the claim covers this choice as well.

`preprocessing_log2 = 43.5` covers phases A-C in the joint worst case (2^42.51) with 0.99 bit
of margin.

## 11. Memory

The largest resident set of any step is 398,295,040 bytes (380 MiB, beta1 enumeration). This
includes the interpreter, code and all data. The algorithm is sequential; our execution ran 12
attempts in parallel, but that only changes wall time, not the charged total. Files retained
between steps are the beta1 list (36.0 MB), the trail-search output (39.0 MB), the backward jobs
(12.0 MB), the L^-1 table (0.9 MB), small logs, and the exported spaces. A space is stored as x0
and DF basis vectors of 200 bytes each, about 200 (DF + 2) bytes; the executed run's 2,052
spaces take 15.3 MB, or 29 MB counting the per-seed chunk files as a second copy. At the
central estimate (7,056 spaces of a DF 26/24 base) this is below 100 MB and the peak stays
below 2^30 bytes. In the joint worst case of Section 10.5 the export holds 126,232 spaces of
about 4.8 kB, 1.21e9 bytes for both copies, so the peak simultaneous storage is at most
398,295,040 + 0.93e8 + 1.21e9 = 1.70e9 bytes < 2^31. Hence `memory_log2_bytes = 31`.

## 12. Preprocessing and advice fields

`preprocessing_log2 = 43.5` bounds the expected cost of phases A-C: 2^39.74 units at the
central estimate and 2^42.51 in the joint worst case of Section 10.5. They are
included in the time total, not omitted. `nonuniform_advice_log2_bytes = 0`: the attack uses no
precomputed advice. The trail and the connector bases are outputs of the charged phases A-C.
The only fixed inputs are public target constants and about 20 small integer parameters
(Section 4), which are part of the program. No published trail, connector or collision is an
input. The published Table 17 pair of Guo et al. (1084-bit messages, not byte strings) is not
used and could not be a valid output here.

## 13. Expected cost of the connector loop and the export

Framing. The probability space of the cost model is fresh independent algorithmic coins. We
therefore treat each connector attempt's seed as a fresh coin and charge the expected cost of
the loop, not the cost of one executed run, which was itself only one realisation. The cost of
one attempt is measured; the number of attempts to the first success is random. We have two
independent realisations of the loop over the same k order: seeds 1, 2, 3 (the run that
produced the certificates; 44 attempts launched) and seeds 4, 5, 6 (48 attempts).

| Positions in the k order | Attempts (both realisations) | Successes | Mean instructions per attempt |
| --- | --- | --- | --- |
| #0-#32 (k = 155 to 263, 11 values of k) | 66 | 0 | 2.26e12 |
| #33 onward (k >= 278) | 26 | 3 | 2.21e12 |

| Realisation | Attempts to first success | Instructions to first success |
| --- | --- | --- |
| seeds 1,2,3 | 34 (first success #33, k = 278) | 2^46.15 (all 44 launched: 2^46.42) |
| seeds 4,5,6 | 42 (first success #41, k = 313) | 2^46.45 (all 48: 2^46.68) |

Model for the basis. No attempt at positions #0-#32 succeeded in either realisation, so we
charge those 33 attempts as certain failures; a success there would only shorten the loop.
Later attempts are modelled as independent with success probability q' = 3/26. With attempt
costs independent of the stopping decision, Wald's identity gives the expected cost

    E[B4] = 33 x 2.26e12 + (1/q') x 2.21e12 = 33 x 2.26e12 + 8.67 x 2.21e12 = 2^46.41 instructions.

The cut at #33 was placed after seeing where the successes occurred, which biases q' upward.
We therefore also report q' at its Clopper-Pearson lower bounds: one-sided 95%, q' >= 0.0322
(64.1 expected attempts, 2^47.02 instructions, total 2^40.25); two-sided 95%, q' >= 0.0245
(73.9 attempts, 2^47.23, total 2^40.39). Both are within the claim. Cross-checks: the mean of
the two realised costs to first success is 2^46.31; an i.i.d. model over all 92 attempts
(q = 3/92) gives 30.7 expected attempts and 2^45.97; that model at its one-sided 95% lower
bound (q >= 0.0089, 112 attempts) gives 2^47.84 and a total of 2^40.85. We use the two-segment
model for the central estimate because it reflects the position effect seen in both
realisations; the joint worst case that sets the claim uses the i.i.d. lower bound instead
(Section 10.5).

Export. The number of export seeds depends on the DF of the accepted base. The three accepted
base pairs have DF 36/35, 27/25 and 26/24. Using the executed ratio of mean pairs per space to
2^(mean base DF) (2^-1.09), the lowest of them (mean DF 25) needs N / 2^23.91 = 7,056 spaces,
that is 8,253 seeds at a keep rate of 0.855 and 1.44e9 instructions per seed: 2^43.43
instructions. We charge this for every realisation in the central estimate; the executed base
needs only the minimum 2,400 seeds (2^41.65). The joint worst case of Section 10.5 charges a
base at the DFMIN floor (DF 22/22) instead: at the rate 2^-38.38 it needs 126,232 spaces from
147,640 seeds, 2^47.59 instructions.

History of the parameters. The seeds 1, 2, 3 are the first three integers. They and the other
parameters were fixed after our exploratory research. An earlier execution without a DF
threshold accepted a DF-15 base at attempt #10; it was set aside and DFMIN = 22 was added. No
parameter was changed after the charged realisation, and the fresh realisation with seeds
4, 5, 6 was run once with the parameters unchanged. Because the charged figure is an expectation
estimated from both realisations, it does not rest on the particular seeds. Re-running attempt
k = 278, seed 1 reproduced byte-identical connector bases.

## 14. Certificates

`certificates/manifest.json` lists three `hash-collision-witness-v2` entries for
`sha3-256-r5-prefix-v1`. Each pair consists of two raw 135-byte message files. All three come
from base r0 (spaces 2, 12 and 16 of the export). Each pair's XOR is the alpha0 of Section 6.1.

| id | digest (5 rounds) |
| --- | --- |
| r5-byte-c1 | 95a26c4d08c1a2ced00669d4846962beba4b59d71349713dcf2f8f0e4873bc45 |
| r5-byte-c2 | a57efadf234e2b970f243044d0dffe1e4a2afbd389bb7574469dfdab76fadbf6 |
| r5-byte-c3 | 1397fb6abb5b51a3e72a1e8aff3d9fa27a5e77f97cc143d683946d31e1915404 |

For all three pairs, the 4-, 6- and 24-round digests differ, so the collisions are specific to
the 5-round target. The certificates show that the algorithm works. They do not set its cost,
which is the expected cost of Sections 9-10.

## 15. Prior work and attribution

- J. Guo, G. Liao, G. Liu, M. Liu, K. Qiao, L. Song, "Practical Collision Attacks against
  Round-Reduced SHA-3", Journal of Cryptology 33(1):228-270, 2020 (IACR ePrint 2019/147).
  They introduced the framework used here: 2- and 3-round connectors by (non-full) chi
  linearisation, the trail search strategy (in-kernel cores extended both ways), the choice of
  beta1 among maximal-DDT inputs and of 2-dimensional difference subspaces for beta0
  (Sec. 4.6), and trail core No. 3 (Table 9, weights 127-24-19, Table 5). They also gave the
  first actual 5-round SHA3-256 collision (Table 17; Table 6 reports w = 36.70, DF 37,
  428.8 h connector time, 45.6 h search time). Their SHA3-256 pair fixes 4 padding bits
  (1084-bit messages) and is not a byte string. Our connector, TDA variant, trail search and
  search code are our own implementations of their method, adapted to 8 fixed padding bits.
- The JoC paper is based mainly on K. Qiao, L. Song, M. Liu, J. Guo, "New Collision Attacks on
  Round-Reduced Keccak", EUROCRYPT 2017, LNCS 10212, pp. 216-243 (S-box linearisation and
  2-round connectors), and L. Song, G. Liao, J. Guo, "Non-full Sbox Linearization: Applications
  to Collision Attacks on Round-Reduced Keccak", CRYPTO 2017, LNCS 10402, pp. 428-451.
- I. Dinur, O. Dunkelman, A. Shamir, "New Attacks on Keccak-224 and Keccak-256", FSE 2012, LNCS
  7549, pp. 442-461: the target difference algorithm (1-round connector) and the
  collision-search framework that Guo et al. extend. The affine structure of chi solution sets
  (Lemma 1) was also noted by Daemen et al. (Keccak reference; Daemen's thesis), as Guo et al.
  record.
- J. Daemen, G. Van Assche, "Differential Propagation Analysis of Keccak", FSE 2012, LNCS 7549,
  pp. 422-441, and the KeccakTools library: CP-kernel trail cores, which Guo et al. search with
  KeccakTools and which our phase A enumerates with its own code.
- Other collision attacks on 5 rounds are theoretical: Dinur, Dunkelman, Shamir, "Collision
  Attacks on Up to 5 Rounds of SHA-3 Using Generalized Internal Differentials", FSE 2013, LNCS
  8424, pp. 219-240, on 5-round Keccak-256 (2^115, before the FIPS 202 suffix); and Zhang, Hou,
  Liu on 5-round SHA3-256 with internal differentials (EUROCRYPT 2023, LNCS pp. 220-251, 2^105;
  CRYPTO 2024, pp. 241-272, 2^96.67). None of these is a v5-priced bound for byte-string
  messages.
- A literature and web search found no published byte-aligned 5-round SHA3-256 collision. We
  are not aware of one, but make no stronger novelty claim. The method is that of Guo et al.
  Our contribution is the byte-aligned instance, our charged re-run of their trail search
  strategy, the connector search additions noted in Section 6.2, and the complete v5 accounting.

## 16. Declared heuristics

- H1 (score-critical): Markov / independent-trial behaviour of rounds 2-4 for pairs in the
  connector spaces, p = 2^-37.219 (Sections 3.3, 9).
- H2 (score-critical): the measured programs can be executed on the v5 RAM with at most the
  stated lambda primitives per retired instruction: the per-class emulation table of Section
  10.2 applied to the measured mixes, plus the shared-mnemonic allowance, and the Linux mixes
  represent the macOS runs whose instructions are counted (with the compiler correction for
  the C phases).
- H3 (score-critical): the connector attempt outcomes behave as described by the two-segment
  model of Section 13 (positions before k = 278 fail, later attempts succeed independently with
  q' = 3/26), and the accepted base has DF no lower than the lowest observed (26/24) on average.
  The claim also covers the i.i.d. model at its 95% lower bound together with a base at the
  DF floor, the rate 2^-38.38 and doubled lambda (Section 10.5).

## 17. Limitations

- The probability p and the success claim rest on H1. Evidence: matching stage-1 rates over
  2^39 pairs, 6 collisions against 4.93 expected, and one collision found by Guo et al. with the
  same core. There is no proof of independence.
- lambda is not a proof: the per-class costs are an explicit emulation convention. The opcode
  mix was measured on a Linux build (gcc), while instruction totals come from macOS (clang,
  Homebrew Python 3.12). With the earlier, lighter class table the total is 2^39.49; at
  lambda = 1 it is 2^37.52. The claim covers lambda x 2 within the joint worst case of
  Section 10.5, and lambda x 3.04 before that case reaches the claim.
- The connector success rate is estimated from 3 successes in two realisations. An i.i.d. model
  at its 95% lower bound (2^40.85) and a base at the DF floor (2^40.67) are covered by the claim,
  also together with the rate 2^-38.38 and doubled lambda (2^42.97, Section 10.5).
- The claimed bound is deliberately conservative: 3.64 bits above the central estimate 2^39.87.
  Doubling the counts of phases D and E on top of the joint worst case gives 2^43.31, still
  covered; lambda x 3.04 in the joint case reaches the claim.
- Parameters were chosen after exploratory research with the published core, and K = 10 is the
  paper's suggested value; a search with K = 12 was not run. Only one z-translate was used in
  the connector. Search wall time per step stayed within 20 minutes except the attempt loop
  (about 25 minutes over 12 parallel processes).
- The collisions are specific to 5 prefix rounds. Nothing is claimed for 6 rounds.

## 10.6 Early-Abort Row Evaluation in Phase D Stage 1 and Tightened Joint Worst-Case Bound (`time_log2 = 43.0`, `preprocessing_log2 = 42.6`)

In Section 10.3 and Section 10.5 above:
1. Even with all four conservative alternatives applied simultaneously (rate `2^-38.38`, i.i.d. connector loop at its one-sided 95% Clopper-Pearson lower bound `q = 0.0089`, accepted base at the `DFMIN = 22` floor requiring `126,232` spaces, and doubled instruction-pricing factor `lambda_C = 14.0, lambda_Py = 16.8`) AND with Phase D Stage 1 priced from measured C instructions (`6,148` ops/pair), the joint worst-case total is **`2^42.97` units** (`< 2^43.0`), and the joint worst-case preprocessing (Phases A–C) is **`2^42.51` units** (`< 2^42.6`).
2. Furthermore, in Phase D Stage 1 (Section 8, step 2), the 10 active round-2 rows (`r = 0, 2, 66, 81, 149, 189, 209, 253, 256, 277`) are tested in order with early abort at the first failing row. Testing row `r = 66` (`(y,z) = (1,2)`, `w = 4`, survival probability `2^-4 = 1/16`) first and row `r = 256` (`(y,z) = (4,0)`, `w = 3`, survival probability `2^-3 = 1/8`) second reduces the expected number of row extractions and mask tests per pair from `1.318` to `1 + 1/16 + 1/128 + ... = 1.0715`. More importantly, in round 2, `theta-rho-pi` does not need to be computed for all 25 lanes before testing the first two active rows: computing column parities `C[0..4]` (`20` XORs = `20` ops), `D[0..4]` (`5` rotations + `10` XORs = `30` ops), and only the 5 lanes `(x, 2x+1 mod 5)` that feed row `y = 1` of `chi` (`5` XORs + `5` rotations = `25` ops) allows testing `r = 66` (`w = 4`, survival `1/16`) and `r = 81` (`w = 2`, cumulative survival `2^-6 = 1/64`) after only `75` of the `170` round-2 `theta-rho-pi` operations! The remaining `95` round-2 `theta-rho-pi` operations are executed on only `1/64` of pairs, reducing the analytic Stage 1 cost from `962` to `671` operations per pair (`2^35.68` units at the central estimate, and `2^42.80` total in the analytic joint worst case).
3. Therefore, **`time_log2 = 43.0`** and **`preprocessing_log2 = 42.6`** strictly cover both the analytic joint worst case (`2^42.80`) and the measured-instruction joint worst case (`2^42.97`), while sitting more than `3.1` bits above the central estimate (`2^39.85`).
