# Byte-aligned two-block adaptation of the GLL+20 5-round SHA3-256 collision attack

Status: DRAFT exploratory estimate. No byte-aligned colliding pair has been
computed. The scalar 51.8 is a heuristic, fully charged bound on the total work
of a hard-budgeted algorithm under collision-frontier-v5. It is built from one
published attack plus our own adaptation and accounting. Every heuristic is
declared in Section 9 and in claim.json. Labels used below:

- [GLL+20] marks published facts, from J. Guo, G. Liao, G. Liu, M. Liu, K. Qiao
  and L. Song, "Practical Collision Attacks against Round-Reduced SHA-3",
  Journal of Cryptology 33 (2020), pp. 228-270; full version IACR ePrint
  2019/147. Section, table and algorithm numbers refer to the ePrint version.
- [ours] marks our own derivations and computations. Each is stated in full here.

## 0. Claim summary

| Field | Value | Basis |
| --- | --- | --- |
| time_log2 | 51.8 | Section 7.4: computed 51.779, rounded up |
| success_probability | 0.44 | Section 6: 0.4418 under H1-H4 and H8 |
| memory_log2_bytes | 34 | Section 8 (memory is not scored) |
| preprocessing_log2 | 49.4 | Section 7.1: trail search 2^49.322, included in time |
| nonuniform_advice_log2_bytes | 0 | No advice; the trail search is run and charged |

Short version:

- [GLL+20] gives a practical collision for 5-round SHA3-256: a 2-round linear
  connector followed by a 3-round differential trail (trail core No. 3).
- Their message has 1084 bits, so it is not a byte string. Its padded block
  fixes only p = 4 bits. Every byte-string message fixes at least p = 8 bits of
  its final block, so we redo the attack at p = 8 inside a two-block message
  with a random first block.
- The algorithm has a hard work budget. It runs independent connector attempts,
  each with a fresh first block, until it has spent 23 times the charged
  expected cost of one successful connector, and enumerates 2^32 pairs in each
  successful connector space.
- The time is a budget that the algorithm never exceeds, not an expected time.
  The success probability 0.44 is computed for that truncated algorithm.
- The connector cost is priced from the published 428.8 core-hours with a
  slowdown factor f = 2, and core-seconds are converted generously (H7). The
  trail search is run and charged as preprocessing.

## 1. Target and message format

Target profile sha3-256-r5-prefix-v1 is FIPS 202 SHA3-256, defined as follows:

- Rate 1088 bits, capacity 512 bits, all-zero initial state.
- Each permutation call runs rounds 0,1,2,3,4 of Keccak-f[1600], i.e.
  theta, rho, pi, chi, iota with round constants RC[0..4] =
  0000000000000001, 0000000000008082, 800000000000808A, 8000000080008000,
  000000000000808B.
- Padding is the SHA-3 suffix 01 then pad10*1. For byte strings this means
  appending the delimited byte 0x06, zero bytes, and 0x80 OR-ed into the last
  byte of the block.
- The digest is the first 256 state bits after the final permutation: lanes
  A[0..3], little-endian. Since 256 < 1088, no extra squeeze call is needed.

Lane k = x + 5y holds bits 64k..64k+63 of the state. The absorbed block uses
little-endian lanes, so block byte j sits in lane floor(j/8) at bits
8(j mod 8)..8(j mod 8)+7.

Our messages have the form M = M0 || X, with:

- M0 a 136-byte first block, drawn uniformly at random.
- X a 135-byte string.

A message has 271 bytes and 271 = 136 + 135. The second padded block is
X || 0x86, because the single padding byte is 0x06 OR 0x80. Hashing is then:

    S0  = f5(M0 || 0^512)                 (first 5-round permutation)
    A   = S0 XOR (X || 0x86 || 0^512)     (second absorbed state)
    H(M) = first 256 bits of f5(A).

The two messages of a pair share M0 and differ only in X. So
H(M0||X) = H(M0||X') exactly when the first 256 bits of
f5(S0 XOR (X||0x86||0)) and f5(S0 XOR (X'||0x86||0)) agree.

Lemma 1 [ours]: any byte-string message fixes at least 8 bits of its final padded block.

Proof. The final block always contains the padding. Let the message
contribute u bytes to its final block. Then 0 <= u <= 135, because a full
136-byte final chunk would force a further padding block. The bytes u..135
are fixed by the padding, which is at least one byte, i.e. 8 bits. Equality
u = 135 gives exactly the 8 fixed bits 0x86 at bits 56..63 of lane 16.

In [GLL+20] the message has 1084 bits. Only 4 bits are fixed there (bits
60..63 of lane 16, value 0111 in bit order, so the top nibble of lane 16 is
0xE); they write p = 4. In both settings the 512 capacity bits are also fixed.
So the attacker controls 1084 bits at p = 4 and 1080 bits at p = 8. In our
setting the 520 fixed bits of A hold the known values S0 XOR (0x86 || 0^512),
not zeros.

## 2. The published attack used here [GLL+20]

Notation follows [GLL+20]:

- L = pi o rho o theta is the linear part of a round.
- chi acts on 320 rows of 5 bits. A row is an "S-box", indexed by plane y and
  slice z. Row convention used throughout: bit x of the 5-bit row value (y, z)
  is bit z of lane x + 5y.
- iota does not affect XOR differences.
- A round-i transition is written alpha_{i-1} -L-> beta_{i-1} -chi-> alpha_i.
  Here alpha_0 is the difference of the initial states and alpha_2 is the
  difference after two rounds.

Facts used from [GLL+20]:

- (G1) Trail core No. 3 (Table 5 and Appendix D) is the triple
  (beta2, beta3, beta4). It is used for 5-round SHA3-224 and SHA3-256.
  - Active S-boxes per state (alpha2, beta2, beta3, beta4 digest part):
    59-10-9-0.
  - Weights w1-w2-w3-w4d: 127-24-19-0.
  - Table 5 lists three d = 256 cores for b = 1600, with w1 = 240, 195 and
    127. No. 3 has the smallest w1.
  - The paper gives the probability of the last three rounds as 2^-36.70,
    "considering multiple trails of the last two rounds". The core is
    reproduced in Section 3.
- (G2) The 2-round connector (Sections 4.3 and 4.6, Algorithms 1-3).
  - Pick a beta1 compatible with alpha2 = L^-1(beta2) of best weight
    (w1 = 127). This fixes alpha1 = L^-1(beta1).
  - A linear "difference system" E_Delta then fixes beta0, keeping the
    difference zero on all c + p fixed bits.
  - A linear "value system" E_M on the round-1 chi input x is built from:
    - the c + p fixed-bit equations;
    - the input affine subspaces of the active round-1 S-boxes;
    - linearisation equations that make the needed round-1 chi outputs affine
      ("full" and "non-full" linearisation);
    - the affine conditions on the round-2 chi inputs that force beta1 -> alpha2.
  - Every solution x of E_M gives a message pair that reaches alpha2 after two
    rounds with certainty.
  - Algorithms 1 and 2 "do not succeed all the time"; the paper repeats random
    picks of beta1 "until the main procedure succeeds" (Section 4.3).
    Algorithm 1 has a bounded counter and Algorithm 2 loops over finite lists,
    so one pick plus one call of Algorithm 1 is a bounded computation.
- (G3) Table 6, row "SHA3-256": connecting time Tc = 428.8 hours on one CPU
  core (footnote: single-core times unless stated); returned dimension DF = 37;
  weight 36.70; brute-force time Tb = 45.6 core-hours. The authors found
  exactly one collision in that space (Section 6.2). Table 17 gives the pair.
- (G4) DF estimate, Eq. (10)/(11):
  DF = sum_i DF(1)_i - (c+p) - w1. Section 4.5 says the real value is usually
  higher, because the equations have dependencies.
- (G5) Speed statements: "Usual computers evaluate around 2^20 ~ 2^22 full
  Keccak evaluations per second" (Table 6 footnote); "of order 2^21 Keccak-f
  evaluations per second on a single CPU core" (Section 5.4).
- (G6) Trail search (Sections 5.2, 5.3, Appendix C.2).
  - Starting cores beta3 come from KeccakTools' TrailCoreInKernelAtC with
    aMaxWeight 60; they obtained "more than 3000".
  - For each core with forward branching C1 <= 2^36, all forward extensions are
    enumerated and the core is kept if some beta4 allows a zero digest
    difference (Requirement (1)).
  - For survivors with backward branching C2 <= 2^35, all backward extensions
    beta2 are enumerated; if AS(alpha2) <= 110 they "check whether this trail
    core is practical".
  - Requirement (2) is TDF > w1 + w2 + w3 + w4d with TDF = 640 - (c+p)
    (Table 3: 124 for SHA3-256, 188 for SHA3-224). Requirement (3) is
    w2 + w3 + w4d <= 55.
  - Section 5.4 says their GPU Keccak-f "v1" code was used to search for
    differential trails, and Section 5.5 says the listed cores were obtained
    "with the help of GPU". No search time is reported.
- (G7) Table 6, row "SHA3-224", same trail core No. 3 and same connector:
  Tc = 11.7 hours, DF = 83. For SHA3-224, c = 448 and p = 4 (the padded block
  in their Table 16 has top nibble 0xE in lane 17, its last rate lane), so
  c + p = 452, against 516 for SHA3-256.

## 3. Trail core No. 3 and our re-check of the published pair [ours]

Nonzero lanes of the [GLL+20] trail core No. 3, as 64-bit hex lane values with
bit z = 2^z:

    beta2: lane0=0000000000000001 lane2=0000000000000004
           lane5=0000000000000004 lane6=0000000000000004
           lane7=0000000000000004 lane8=0000000000020000
           lane10=2000000000000000 lane12=0000000000200000
           lane15=2000000000000000 lane18=0000000000020000
           lane20=0000000000200001 lane22=0000000000200000
           lane24=0000000000000001
    beta3: lane0=0000000000000001 lane2=0000000000000001
           lane3=0000004000000000 lane7=0000000000000001
           lane9=0000000000040000 lane11=0000000000000100
           lane14=0000000000040000 lane20=0000000000000001
           lane21=0000000000000100 lane23=0000004000000000

The published colliding pair ([GLL+20] Table 17) as padded 17-lane rate
blocks, lanes 0..16 as 64-bit hex values; lanes 17..24 (capacity) are zero:

    M1  0:FECA67BD2D3F021A  1:BD10A64A4C2B774F  2:F8EF6FF82DD21FC7  3:6F4BA4D964A78764
        4:0F4FD1C92A24BC6E  5:FB4B8C0A11C64088  6:EDA7B9EBC05F50A8  7:0A71DD08E7F1EB5B
        8:5342D2AE78A8BFB5  9:6591A9B0CC2E7CE9 10:52A3DD827F4EF6DC 11:9D89B18362B80DE4
       12:FEA719A1875BFFF7 13:49A2B95AD7B7D147 14:B23784B72EB9260A 15:187AEFD07295FD59
       16:EE806366EF9D09FF
    M2  0:16F97050842C2D17  1:A731EE935A43480A  2:6D8E356BDBD7CBE9  3:D62C0B356FFA158A
        4:4FAD968080C7F8C8  5:7C83B8E1C61BC5AB  6:7E3FCA22B5E29305  7:5888D4DBE848C840
        8:236DE21CCEF77B8A  9:69D59EF589070E60 10:E87FCD2BF2C6CCE1 11:B1E28B821FD93ABC
       12:AD5D6FB1860CB45C 13:AB8FC7D1015975D5 14:24C6B737EE96CC23 15:D3BFB5957965A447
       16:EE31D3F5269F254F

Applying rounds 0-4 (formulas of Section 1, RC[0..4]) to each block, as the
whole initial state, we obtain:

- Equal digests in both cases. Lanes 0..3 of the output, as 64-bit values:
  65017C2E8B6040B4 344FF8BB933B4BD6 C6A3F13368BE2003 AB427B4B33435ACB, the
  digest printed in [GLL+20]. This confirms the round convention and the round
  constants.
- The pair's differences satisfy L(alpha2) = beta2 and L(alpha3) = beta3
  exactly.
- The beta4 the pair actually follows differs from the listed one, which fits
  the multiple-trail clustering in rounds 4-5.
- Active S-box counts: alpha2 59, beta2 10, beta3 9, alpha3 10.
- Exact chi weights:
  - round 2: 127, with DDT entries 9x4 and 50x8;
  - round 3: 24;
  - round 4: 19.

  These match (G1). The minimum reverse weight of alpha2, summed over its 59
  active rows, is also 127 (each nonzero 5-bit output difference has minimum
  reverse weight 2 or 3; 11 of the 31 values have 3).
- Round 1 has 318 active S-boxes, with DDT entries 75x2, 156x4 and 87x8. Only
  2 S-boxes are inactive.
- alpha0 is zero on the capacity. It is also zero on all 8 bits of the top
  byte of lane 16, where both messages hold 0xEE. So this published connector's
  difference beta0 already meets the p = 8 difference constraint.
- Branching numbers of core No. 3's beta3 (used in Section 7.1): C1 = 2^19
  compatible alpha4 and C2 = 2^31.70 compatible beta2, both below the caps
  2^36 and 2^35 of (G6). AS(alpha2) = 59 <= 110, w1+w2+w3+w4d = 170 <= 188,
  w2+w3+w4d = 43 <= 55.

The pair is not a solution to this target, because its 1084-bit messages are
not byte strings. We do not claim it as one. We use it only as evidence about
the trail and the connector.

## 4. Algorithm [ours, built on (G1)-(G2), (G6)]

Parameters: K = 22, connector budget B_A = (K+1) * mu = 23 * mu with
mu = 2^46.961 units (Section 7.2), enumeration cap M = 1024 spaces of 2^32
pairs.

P. Preprocessing: trail search. A deterministic version of the (G6) search.
   1. Run KeccakTools TrailCoreInKernelAtC with aMaxWeight 60, as in [GLL+20].
      Call the output list S.
   2. For each beta3 in S with C1 <= 2^36: enumerate all compatible alpha4 by
      a depth-first tree over the active rows of beta3, maintain
      beta4 = L(alpha4) incrementally, and test the digest condition: every
      plane-0 row of beta4 is 0 or one of the 9 values
      {10,14,15,18,1A,1C,1D,1E,1F} (hex) that can output exactly 0x10. Keep
      beta3 if some leaf passes.
   3. For each kept beta3 with C2 <= 2^35: enumerate all beta2 compatible with
      alpha3 = L^-1(beta3) by a depth-first tree, maintain alpha2 = L^-1(beta2)
      incrementally, and compute w2, AS(alpha2) and w1 (the minimum reverse
      weight of alpha2).
   4. Filter. Keep (beta2, beta3) when AS(alpha2) <= 110,
      w1 + w2 + w3 <= 188 and w2 + w3 <= 55. This is Requirement (2) with the
      SHA3-224 threshold of Table 3 (188) instead of the SHA3-256 threshold
      (124), and Requirement (3). Under the SHA3-256 threshold, core No. 3
      (sum 170) would be rejected; under 188 it passes. This relaxation is what
      [GLL+20] effectively did, because they used No. 3 for SHA3-256.
   5. Selection rule. Among kept cores, take the minimum w1; break ties by
      minimum w2 + w3, then by the smallest beta2 and then beta3 in
      lexicographic lane order. This runs as a running minimum during step 3,
      with no connector trials. Our heuristic H6 is that the rule outputs core
      No. 3. Set alpha2 = L^-1(beta2).

A. Connector attempts with a hard budget. Keep a work counter W_A, initially 0,
   that counts every primitive operation of steps A1-A3 (step E is counted
   separately, Section 7.3). Repeat:
   1. Draw a fresh uniformly random 136-byte block M0. Compute
      S0 = f5(M0||0). The 520 fixed bits of A now have known values
      F = (bits 1080..1599 of S0) XOR (0x86 || 0^512).
   2. Run one attempt of the connector (G2) for the target difference alpha2:
      one fresh random pick of beta1 and one call of Algorithm 1 with fresh
      random choices.
      - Variables: the 1080 free bits X of A.
      - Fixed: the 520 bits with values F, and the difference must be zero on
        all of them.
   3. The attempt succeeds when the linear systems are consistent and the
      returned affine space V of X values has dimension DF >= 33. The output is
      V and the common nonzero 1080-bit difference Delta. An attempt with
      DF < 33 counts as failed.
   4. If it succeeds and fewer than M spaces have been enumerated, run step E
      on (M0, V, Delta). On a collision, output it and stop.
   5. Stop with failure as soon as W_A reaches B_A. The attempt in progress is
      aborted.

E. Enumeration of one space. Let D be the direction space of V and v a base
   point. Choose a 32-dimensional subspace W of D with Delta not in W. Such a
   subspace exists: if Delta is in D, take a complement of <Delta> inside a
   33-dimensional subspace of D that contains it; otherwise take any
   32-dimensional subspace. For each X in v + W in Gray-code order (2^32
   values):
   - compute the two second-block permutations for X and X XOR Delta;
   - compare the 256 digest bits;
   - on equality, output (M0 || X, M0 || (X XOR Delta)).

The algorithm stops at the first collision or when the budget runs out. It
never exceeds the charged work: phase A is cut at B_A, at most M = 1024 spaces
are enumerated, and step P is a fixed computation.

Correctness of any output. The two messages are distinct 271-byte strings,
because Delta != 0. The check compares the true digests computed through
the full sponge: first block, then second block with its 0x86 padding byte,
using the selected 5-round permutation, with no free-start or truncation.
So every output is an ordinary full 256-bit collision of the target.

Lemma 2 [ours]: the 2^32 enumerated pairs {X, X XOR Delta}, for X in v + W,
are pairwise distinct. By (G2), each one reaches alpha2 after two rounds of the
second permutation.

Proof. Suppose two different X, X' in v + W gave the same unordered pair.
Then X' = X XOR Delta, so Delta = X XOR X' would lie in W, which contradicts
the choice of W. The second statement is the defining property of a connector
solution in (G2): for every solution x of E_M, the pair (x, x + beta0) has
difference alpha2 after two rounds. In message coordinates this pair is
(X, X XOR Delta). This needs no claim that V is closed under adding Delta.
Counting 2^32 = 2^(33-1) pairs from a space of dimension 33 is also the
conservative reading of [GLL+20]'s convention, which counts 2^DF.

Independence across attempts [ours]. Given the fixed core from step P, each
attempt uses only its own fresh M0 and fresh coins. So the attempts, their
costs, their success events and the collision events in their spaces are
i.i.d. across attempts. This is exact, not a heuristic.

## 5. Degrees of freedom at p = 8 (H3) and connector scaling (H4)

Rank fact [ours]. Fix all choices of the connector. E_M is then a linear system
A x = t over GF(2), and its solution set is empty or an affine space of
dimension 1600 - rank(A). Moving from p = 4 to p = 8 makes 4 more bits fixed
(bits 56..59 of lane 16), which adds 4 rows to A. Rank grows by at most 4, so
whenever the enlarged system is consistent its dimension is at least the
p = 4 dimension minus 4.

Applied to the published SHA3-256 connector (DF = 37, from (G3)), this gives
DF >= 33 for a successful p = 8 connector built with the same structure.

Scaling evidence from (G7) [ours, arithmetic on published data]. The same core
No. 3 and the same connector were run at c + p = 452 (SHA3-224) and
c + p = 516 (SHA3-256):

- DF fell from 83 to 37: 46 dimensions for 64 extra fixed bits, about 0.72 per
  bit, below the at most 1 per bit of the rank fact. Extrapolating 4 more bits
  gives DF of about 37 - 2.9 = 34.1, consistent with DF >= 33.
- Tc rose from 11.7 h to 428.8 h, a factor 36.65 = 2^5.196, i.e. 2^0.0812 per
  fixed bit on a log-linear fit. For 4 more bits this predicts a factor
  2^0.325 = 1.25. The growth may be steeper close to the degrees-of-freedom
  limit than a two-point fit shows. This is why H4 charges f = 2, not 1.25
  (Section 7.2), and why Section 7.5 shows f up to 16.

The unrefined formula (G4) is not the source of the 37 [ours]. Use Table 2 of
[GLL+20] with our round-1 histogram from Section 3:

- DF(1) <= 1 for each of the 75 DDT-2 S-boxes;
- DF(1) <= 2 for each of the 156 DDT-4 S-boxes;
- DF(1) <= 3 for each of the 87 DDT-8 S-boxes;
- DF(1) <= 5 for each of the 2 inactive S-boxes.

The sum of DF(1) is therefore at most 658, and Eq. (10) gives DF <= 658 - 516
- 127 = 15, whereas the observed value is 37. The extra 22 or more dimensions
come from linear dependencies, mainly between the fixed-bit equations and the
S-box equations. preProcess (Algorithm 3) uses these on purpose: when a
linearisation equation is already implied by E_M, nothing is added. So we take
DF = 33 from the observed 37 and the rank fact, not from Eq. (10).

The remaining uncertainty is declared as H3: the DF of different p = 8
connector attempts from different first blocks varies, and [GLL+20] reports
one DF value per target. An attempt with DF < 33 counts as failed (Section 4),
so a DF shortfall lowers the attempt success rate q, which H4 must absorb;
it does not silently remove a space from the success count.

Difference side [ours]. Take the pair's round-1 activity pattern from
Section 3 (318 active and 2 inactive S-boxes). Count the free difference bits,
subtract the rank of the 10 equations "inactive S-box input difference = 0"
(computed as 10), and subtract 3 equations per active S-box, which is (G2)'s
choice of a 2-dimensional affine input-difference subset:

- p = 4: 1084 - 10 - 3*318 = 120 dimensions of slack;
- p = 8: 1080 - 10 - 954 = 116 dimensions of slack.

Losing 4 of about 120 slack dimensions is minor. The published beta0 already
meets the p = 8 difference constraint (Section 3). This supports H5.

## 6. Success probability (H1, H2, H3, H4, H8)

Per-pair probability (H1). A pair from a connector space reaches alpha2 with
certainty (G2), and then needs to:

- (a) pass round 3: beta2 -> alpha3 = L^-1(beta3), of weight 24;
- (b) reach, in rounds 4-5, a beta4 whose plane-0 rows give an output
  difference with bits x = 0..3 equal to zero (lanes 0..3 are the digest). An
  inactive row gives 0. An active row with input difference d must output
  exactly 0x10, which happens with probability DDT[d][0x10]/32.

[ours] We computed the Markov-model probability of the rounds 4-5 part
exactly. With alpha3 fixed, the sum covers all 2^19 alpha4:

    P45 = sum over alpha4 compatible with beta3 of
          Pr[beta3 -> alpha4] * prod over active rows d of plane y=0 in
          L(alpha4) of DDT[d][0x10]/32.

The 9 active rows of beta3, as (y, z, input difference in hex), are:

    (0,0,05) (0,38,08) (1,0,04) (1,18,10) (2,8,02) (2,18,10) (4,0,01)
    (4,8,02) (4,38,08)

Procedure (enough to re-run it without other material):

    DDT[a][b] = #{v in 0..31 : chi5(v) XOR chi5(v XOR a) = b}
        where chi5(v)_i = v_i XOR (NOT v_{i+1} AND v_{i+2}), indices mod 5
    for each active row r = (y, z, a):
        options[r] = [(b, DDT[a][b]/32) for b in 0..31 if DDT[a][b] > 0]
        for each option b: img[r][b] = L(state with row (y,z) = b, else 0)
            where L = pi o rho o theta (offsets and formulas of Section 1)
    P45 = 0
    for each choice (b_r) in the product of options (2^19 = 524288 tuples):
        beta4 = XOR of img[r][b_r];  pr = product of the chosen probabilities
        q = 1
        for z in 0..63:  v = row (0, z) of beta4
            if v != 0: q = q * DDT[v][0x10] / 32
        P45 = P45 + pr * q

Results:

- P45 = 2^-13.219.
- So p_pair = 2^-24 * 2^-13.219 = 2^-37.219. We use 2^-37.22.
- This is lower than the published 2^-36.70 by about 0.5 bit. We did not
  reproduce the published 36.70 and do not know which additional trails or
  rounds it includes. We use our own value throughout, since it is the lower
  probability.

Sanity check: [GLL+20] found one collision in a DF = 37 space, i.e. 2^36
pairs. Our value predicts 0.43 expected collisions and theirs 0.62. Both are
consistent with the observed single collision.

Per-space success (H2). A successful attempt's space yields 2^32 pairs, each
colliding with probability p_pair. Assuming the collision count within a space
is roughly Poisson (weak clustering), the space contains a collision with
probability

    s = 1 - exp(-2^32 * 2^-37.22) = 1 - exp(-0.02682) = 0.02650.

Theorem [ours, under H4 and H8]. Let q be an attempt's success probability and
E[C] the expected work to obtain one successful attempt, including failed
attempts and first-block overhead. Assume E[C] <= mu (H4), and the attempt
structure of H8. Then the algorithm of Section 4 succeeds with probability at
least 1 - exp(-K*s) - (1-s)^M = 1 - exp(-0.5830) - 1.1e-12 = 0.4418.

Proof.

- Let S be the number of successful attempts completed within B_A. By the
  independence statement in Section 4 and H2, the spaces collide
  independently, each with probability s. The algorithm enumerates the first
  min(S, M) of them, so

      Pr[fail] = E[(1-s)^min(S,M)] <= E[(1-s)^S] + (1-s)^M,

  because (1-s)^min(a,M) <= (1-s)^a + (1-s)^M for every a.
- Equal-cost case of H8. Every attempt costs the same tau, so q = tau/E[C] and
  tau/q <= mu. Then n = floor(B_A/tau) attempts complete within B_A, with
  n >= floor((K+1)/q) >= (K+1)/q - 1 >= K/q, since q <= 1. Each attempt
  independently succeeds and contains a collision with probability q*s, so

      E[(1-s)^S] = (1 - q*s)^n <= exp(-n*q*s) <= exp(-K*s).

- Exponential case of H8. The work per success C is exponential with mean
  E[C] <= mu. Then S is Poisson with mean B_A/E[C] >= K+1, and
  E[(1-s)^S] = exp(-s*B_A/E[C]) <= exp(-(K+1)*s) <= exp(-K*s).
- With K = 22 and s = 0.02650, exp(-0.5830) = 0.5582. With M = 1024,
  (1-s)^1024 = 1.1e-12. So Pr[success] >= 0.4418, reported as 0.44.

Conditions on H3. A space with DF < 33 is not counted as a success, so H3
enters only through q, i.e. through H4.

The probability space is:

- the random first blocks M0 and the connector's random choices;
- the enumeration order, which does not matter.

## 7. Cost accounting (collision-frontier-v5; one 5-round permutation = 1 unit)

The reference cost is C = 1355 word operations (256-bit word RAM primitives)
per unit. A 1600-bit state occupies 7 words.

### 7.1 Trail search, charged as preprocessing (H6)

Leaf costs [ours, itemised for step P]:

- Tree maintenance. For each active row and each allowed row value, a
  precomputed 1600-bit image under L (step 2) or L^-1 (step 3) is stored, at
  most 11 rows x 31 values x 7 words. Moving to a child node XORs one image
  into the running state: 7 loads, 7 XORs, 7 stores = 21 primitives. Each
  active row has at least 2 options, so internal nodes are at most as many as
  leaves. With loop control and a running weight sum (at most 10 per node),
  this is at most 62 primitives per leaf.
- Forward leaf (step 2). Extract the 5 plane-0 lanes (at most 10 primitives).
  The 64-bit mask of "good" rows, those equal to one of the 9 allowed values,
  is a 9-minterm Boolean function of the 5 lanes, at most 9*9 + 8 = 89
  primitives. "Bad" = (OR of the 5 lanes) AND NOT good, 6 primitives, then one
  compare and branch. Total at most 62 + 10 + 89 + 8 = 169 <= 338 primitives =
  1/4 unit.
- Backward leaf (step 3).
  - Lane extraction: 25 lanes at 2 primitives each, 50.
  - Row-activity masks: 4 ORs per plane, 20.
  - AS(alpha2): popcount by shifts, masks and adds, at most 20 per 64-bit
    mask, 100.
  - w1 = 2*AS(alpha2) + N3, where N3 counts rows whose value is one of the 11
    outputs of minimum reverse weight 3 (Section 3). N3 needs an 11-minterm
    function per plane, at most 11*9 + 10 = 109, so 545 for 5 planes, plus
    5 popcounts, 100.
  - Filter compare and running-minimum update: 20.
  - Total at most 62 + 50 + 20 + 100 + 645 + 20 = 897 <= 1355 primitives =
    1 unit.

Search extent:

- At most 2^13 starting cores. [GLL+20] reports "more than 3000"; we assume at
  most 2^13 = 8192 (part of H6).
- At most 2^36 forward leaves and at most 2^35 backward leaves per core (the
  caps of (G6)).
- Extension total: 2^13 * (2^36 * 1/4 + 2^35 * 1) = 2^13 * 3 * 2^34 = 3 * 2^47
  = 2^48.585 units.

Starting-core generation: KeccakTools in-kernel generation with aMaxWeight 60.
No cost is published. We charge an explicit allowance of 2^48 units, which is
about 1,770 core-hours at the H7 conversion rate, or 4 times the whole published
SHA3-256 connecting time. This allowance is unsupported by any published figure
and is part of H6. Section 7.5 gives the sensitivity.

GPU use in the published search. [GLL+20] used GPU Keccak-f code during trail
search (G6), without saying in which step. Step P evaluates no Keccak-f: all
linear maps are applied through precomputed images, and every operation is
counted above. If the published search needed GPU work that step P omits, step
P might not find core No. 3; that risk is part of H6.

Selection. The running minimum of step 5 is included in the backward-leaf cost.
No connector trials are run on candidate cores.

    T_trail = 3 * 2^47 + 2 * 2^47 = 5 * 2^47 = 2^49.322 units,
    charged as 2^49.33; preprocessing_log2 = 49.4.

### 7.2 Connector work (H4, H7, H8)

Published time. Tc = 428.8 core-hours = 1,543,680 s = 2^20.558 s.

Slowdown factor (H4): f = 2 = 1.25 x 1.6.

- 1.25 is the p = 4 -> p = 8 scaling extrapolated from (G7) (Section 5).
- 1.6 covers the fact that Tc is a single observed run. For one exponential
  sample, the median-unbiased estimate of the mean is the sample divided by
  ln 2, i.e. 1.443 Tc. We round this up to 1.6.

This is a central estimate, not a confidence bound. A 90% one-sided bound from
one exponential sample would need a factor 1/(-ln 0.9) = 9.5; Section 7.5 shows
f = 4, 8 and 16.

Conversion of core-seconds to units (H7, an estimate, not an upper bound).
R = 5e9 cycles/s x 6 instructions/cycle x 2 primitives per instruction / 1355
= 6e10 / 1355 = 2^25.400 units per core-second.

- 6 instructions per cycle at 5 GHz is above what 2017-2019 desktop cores
  sustain, even counting macro-fused compare-and-branch pairs.
- 2 primitives per instruction on average fits the connector's work. Algorithms
  1-3 of [GLL+20] are Gaussian elimination and consistency checks of GF(2)
  systems with rows of at most 1601 bits (7 words). Their inner loop is word
  loads, XORs and stores, compares and branches: 1 primitive each, 2 for a
  load-op instruction. Costlier instructions (popcount, bit scan for pivot
  search, 64-bit rotations inside 256-bit words) occur about once per row
  operation, against at least 7 word XORs per row operation.
- Calibration 1, Keccak speed (G5). At most 2^22 Keccak-f[1600] per
  core-second is at most 2^22 x 24 rounds x 271 primitives per round =
  2^34.67 primitives per second for the paper's own optimised code. R stands
  for 6e10 = 2^35.80 primitives per second, 2.2 times more.
- Calibration 2, the paper's brute-force stage (G3). Enumerating the DF = 37
  space needs at most 2^38 five-round permutations, done in Tb = 45.6
  core-hours = 164,160 s. That is at most 2^20.68 permutations (units) per
  core-second, 2^4.7 below R.
- Both calibrations show that the authors' code on their hardware ran at well
  below the throughput that R charges for.

Expected work per successful attempt, charged:

    mu = f * Tc * R * 1.002 = 2^(1 + 20.558 + 25.400 + 0.003) = 2^46.961 units.

The factor 1.002 covers the per-attempt first-block overhead: one permutation
plus 17 random words, at most 2 units = 2,710 primitives. One attempt rebuilds
and solves E_Delta, with more than 1,500 equations in 1,600 unknowns
(Section 4.6 of [GLL+20]). Gaussian elimination of such a system is about
1500^2/2 row operations of at least 21 primitives each, about 2^24.6
primitives = 2^14.2 units. So the overhead is below 2^-13 of an attempt, and
we charge 2^-9.

Phase A budget: B_A = 23 * mu = 2^(46.961 + 4.524) = 2^51.485 units. This is a
hard cap enforced by the algorithm (Section 4), so no tail term remains.

### 7.3 Everything else

- Enumeration: at most M = 1024 spaces. Each space has 2^32 pairs, each with 2
  permutations plus at most 128 primitives. The primitives cover the Gray-code
  step (one 1600-bit basis vector XOR, 7 words), building the partner state
  (7 XORs), absorbing into S0, comparing the 256 digest bits, and loop
  control. That is 2^32 * (2 + 128/1355) = 2^33.067 units per space, and at
  most 2^43.067 units in total.
- Finding the complement W in a space: one Gaussian elimination on at most 64
  vectors of 1600 bits, under 2^20 primitives, which is negligible and counted
  in the 2^18 below.
- Output, final re-check and bookkeeping: under 2^18 units.

### 7.4 Total

    T = T_trail + B_A + M * 2^33.067 + 2^18
      = 2^49.322 + 2^51.485 + 2^43.067 + 2^18
      = 2^51.779  ->  claimed time_log2 = 51.8.

For context only: the expected-time figure that charges 22 expected connectors
with no budget truncation would be 2^51.72, and an earlier version of this
draft with f = 1, R = 2^24.815 and no truncation gave 2^50.08. We do not claim
either figure.

### 7.5 Sensitivity [ours, same arithmetic]

Unless stated, K = 22, success probability 0.4418 and the other inputs are as
in the base case.

| Change | time_log2 |
| --- | --- |
| Base case | 51.78 |
| f = 1 / 1.25 (H4) | 51.02 / 51.25 |
| f = 4 / 8 / 16 (H4) | 52.64 / 53.56 / 54.53 |
| Conversion R x2 / x4 (H7) | 52.64 / 53.56 |
| R = 2^24.815 / 2^24.263 (H7) | 51.32 / 50.93 |
| Trail search 2^48 / 2^50 / 2^51 (H6) | 51.61 / 51.93 / 52.27 |
| p_pair 2^-36.70: K = 22 gives P = 0.564; K = 14 gives P = 0.41 (H1) | 51.30 at K = 14 |
| p_pair 2^-37.5: K = 22 gives P = 0.382, below 0.39; K = 23 gives P = 0.395 (H1) | 51.83 at K = 23 |
| p_pair 2^-38: K = 22 gives P = 0.289; K = 32 gives P = 0.391 (H1) | 52.22 at K = 32 |
| DF = 32 (K = 44) / DF = 31 (K = 88), same P (H3) | 52.61 / 53.52 |

The success margin at K = 22 covers a p_pair as low as 2^-37.46.

### 7.6 Fallback without H8

If only the expectation E[C] <= mu (H4) is granted, Markov's inequality is the
only tail bound. Build N spaces sequentially and abort when phase A work
exceeds c * N * mu. Then Pr[success] >= 1 - 1/c - (1-s)^N. The cheapest choice
reaching 0.39 is N = 50, c = 2.866, i.e. 143.3 mu, giving
T = 2^49.322 + 143.3 * 2^46.961 + 50 * 2^33.067 = 2^54.18. This is the
conservative alternative if H8 is rejected. We do not claim it.

## 8. Memory

- Connector: the systems E_Delta and E_M are each at most 1600 x 1601 bits,
  about 320 KB in total, plus working copies.
- Enumeration: at most 64 basis vectors and two states.
- Trail search: the precomputed row images (under 40 KB), tree depth of at
  most 11 levels, and the running minimum.
- Allowance for KeccakTools core generation and its output list: 2^34 bytes
  (assumed, not measured).
- Code: under 2^24 bytes.

Peak memory is therefore at most 2^34 bytes. This is a reported metric only.

## 9. Declared heuristics (mirrored in claim.json)

- H1 (score-critical). Per-pair probability: every candidate pair in a
  connector space collides with probability at least 2^-37.22. This is a
  Markov-model trail probability, with alpha3 fixed and all alpha4 summed.
  - Evidence: Sections 3 and 6, and (G1)/(G3).
  - Limitations: rounds 3-5 are treated as independent. No p = 8 experiment
    exists. Sensitivity in Section 7.5.
- H2 (score-critical). Weak clustering within a space: the collision count in
  a space of 2^32 pairs is close to Poisson, so s = 1 - exp(-2^32 p_pair).
  - Evidence: Section 6, and the published single-collision observation.
  - Limitations: if collisions cluster, s is smaller. Independence across
    spaces is exact by construction (Section 4).
- H3 (score-critical). Successful p = 8 connector attempts give DF >= 33.
  - Evidence: Section 5: the rank fact, the published DF = 37, and the (G7)
    slope of 0.72 per bit, which predicts DF of about 34.
  - Limitations: one published DF sample per target, and Eq. (10) is not
    predictive. A DF shortfall shows up as a lower q and must be absorbed by
    H4.
- H4 (score-critical). The expected work E[C] to obtain one successful p = 8
  attempt (consistent system, DF >= 33) from fresh random first blocks,
  including all failed attempts, is at most f * Tc with f = 2, i.e. at most
  857.6 core-hours, i.e. at most mu = 2^46.961 units with H7.
  - Evidence: (G3); the (G7) scaling of 1.25 for 4 bits; the factor 1.6 for a
    single-run estimate; the Section 5 difference-side slack; the published
    beta0 already being p = 8 compatible.
  - Limitations: Tc is a single run. A two-point fit may understate growth near
    the DF limit. Nobody has run the connector at p = 8 or with random fixed
    values. Not a confidence bound. Sensitivity f = 4 / 8 / 16 gives 52.64 /
    53.56 / 54.53.
- H5 (supporting). The difference system stays solvable with zero difference on
  all 8 padding bits.
  - Evidence: Sections 3 and 5.
- H6 (score-critical). The trail search of step P costs at most 2^49.322 units
  and its selection rule returns trail core No. 3.
  - Evidence: Section 7.1, where the extension cost of 2^48.585 is itemised.
    Core No. 3 passes every filter of step P (Section 3). No. 3 has the
    smallest w1 among the d = 256 cores listed in Table 5 of [GLL+20], and
    [GLL+20] used it for their two tightest targets.
  - Limitations: the bound assumes at most 2^13 starting cores and charges an
    unsupported allowance of 2^48 units for KeccakTools generation. The
    published search used GPU Keccak-f code in an unstated step. A core with
    smaller w1 might exist and be selected; our cost and probability figures
    are for No. 3 only.
- H7 (score-critical). One core-second of the published connector
  implementation corresponds to at most about 2^25.400 units. This is an
  estimate, not a proven bound.
  - Evidence: Section 7.2, the machine-level allowance plus two calibrations
    from the paper's own timings.
  - Limitations: the CPU model and instruction mix are unpublished. Sensitivity
    x2 / x4 gives 52.64 / 53.56.
- H8 (score-critical). Attempt structure. The work per successful attempt C is
  a sum of a geometric number of attempt costs, and its tail is no heavier than
  in the equal-cost or exponential cases of Section 6.
  - Evidence: the retry structure of (G2). Attempts are i.i.d. by construction
    (Section 4). When q is small, a compound-geometric sum of bounded i.i.d.
    costs is close to exponential. When q is large, it is less dispersed.
  - Limitations: no attempt-level timings are published. If attempt costs are
    very unequal (rare very long attempts), the count of successes within B_A
    is more dispersed and the probability lower. Without H8 the Markov-only
    fallback gives 54.18 (Section 7.6).

## 10. What is not claimed

- No colliding byte-aligned pair, and no certificate. The certificate manifest
  is empty.
- No experiment manifest. Our numerical checks (Sections 3, 5 and 6) are offline
  computations, described completely so they can be re-derived. They are not
  organizer-executed evidence.
- No novelty beyond the p = 8 two-block adaptation and its accounting. The
  method, trail and connector are those of [GLL+20].
- The published 1084-bit pair is not a solution to this target.
- The baseline_improved identifier sha3-256-r5-nominal-v2 is the required
  nominal reference ID. It is not a claim of Pareto dominance.
