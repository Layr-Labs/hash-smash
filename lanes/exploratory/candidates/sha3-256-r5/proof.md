# Five-round SHA3-256: a byte-aligned GLL+20 connector attack with per-run hard caps

## 0. Claim

| Field | Value |
| --- | --- |
| target | `sha3-256-r5-prefix-v1`, ordinary collision, 135-byte messages |
| time_log2 | 53.7 (hard cap 2^53.6952 units on every random tape, Section 6) |
| success_probability | 0.40 (computed lower bound 0.4132 under H1-H3, Section 7) |
| memory_log2_bytes | 24 (computed data peak below 2^21 bytes, Section 8) |
| preprocessing_log2 | 20 (table setup and trail-constant check, at most 2^19.60 units) |
| nonuniform_advice_log2_bytes | 10 (the 400-byte trail core of Section 3) |
| certificates / experiments | none; this is an analytical package |

The algorithm is the 2-round connector plus 3-round trail attack of Guo, Liao,
Liu, Liu, Qiao and Song ("Practical collision attacks against round-reduced
SHA-3", Journal of Cryptology 33, 2020; IACR ePrint 2019/147; "GLL+20" below),
specified here for byte-string messages (8 fixed padding bits instead of the
paper's 4). Every random choice, order and retry counter is fixed in Section 4.
Every phase has a hard operation counter or a fixed loop bound. The time
bound therefore holds on every random tape. The three declared heuristics bear only on the
success probability. No collision was produced for this package.

## 1. Target, conventions and the message domain

The state is 25 lanes A[x,y] of 64 bits, lane index x+5y, bit z in 0..63.
State bit number 64(x+5y)+z. Message byte j, bit t (bit 0 least significant)
is state bit 8j+t; this is the standard little-endian Keccak encoding used by
`verifier/keccak.py`. A row is the 5 bits (x=0..4, y, z) for fixed (y,z), with
row index i = 64y+z (320 rows); its 5-bit value has bit x at position x.

One round is R_r = iota_r o chi o pi o rho o theta. We write L = pi o rho o theta
(linear, invertible) and chi row-wise: y_x = x_x XOR (NOT x_{x+1} AND x_{x+2}).
The target applies rounds r = 0,1,2,3,4 with round constants RC[0..4] =
0000000000000001, 0000000000008082, 800000000000808A, 8000000080008000,
000000000000808B, starting from the zero state. The digest is lanes 0..3
(state bits 0..255) after round 4.

All messages used are exactly 135 bytes. The padded block is M || 0x86 (SHA3
suffix 01, then pad10*1 inside one byte), so state bits 1080..1087 are fixed to
0,1,1,0,0,0,0,1 (bit 1080 first) and bits 1088..1599 (capacity) are zero. The
1080 message bits are free. In GLL+20's notation p = 8 (the paper used p = 4,
1084-bit messages). Both messages of the output pair are 135-byte strings with
the same last padded byte, so they are in the target domain, and they are
distinct because the message difference Delta is nonzero (Section 5).

Differences: round r maps alpha_r -L-> beta_r -chi-> alpha_{r+1}; alpha_0 is
the message difference (zero on bits 1080..1599). iota does not change
differences. #AS(s) is the number of rows of s with a nonzero value. DDT is the
5-bit chi difference table; for din != 0 and DDT(din,dout) > 0 the solution set
V(din,dout) = {x : S(x) XOR S(x XOR din) = dout} is an affine subspace of
dimension log2 DDT(din,dout) in {1,2,3}.

## 2. Sources and what is taken from them

GLL+20 (ePrint 2019/147 text) supplies:
- Sections 4.1-4.6: S-box linearization (Observations 1-4), Equations (1)-(11),
  Algorithms 1-3 (mainLinearization, basicLinearization, preProcess), the
  target-difference choice of beta_0, and the choice of beta_1.
- Table 5 and Table 9: trail core No. 3 (#AS 59-10-9-0, weights 127-24-19-0)
  and its probability 2^-36.70 "considering multiple trails of the last two
  rounds".
- Table 6, SHA3-256 row: connector time Tc = 428.8 hours on one CPU core,
  DF = 37, w = 36.70, brute-force time 45.6 hours; Table 17: the colliding pair.
  The text notes that only one collision was found in that space.

Our own checks (organizer `verifier.keccak.permutation`, 5 rounds, from the
printed 17 lanes of each Table 17 message, capacity zero):
- both messages give lanes 0..3 = 65017C2E8B6040B4 344FF8BB933B4BD6
  C6A3F13368BE2003 AB427B4B33435ACB (digest bytes b440608b...4b7b42ab);
- tracing the pair, beta_2 and beta_3 equal the Table 9 states of Section 3
  exactly; alpha_2 has 59 active rows; the pair's beta_4 differs from the
  printed beta_4 (another last-round trail; this is why the paper counts
  multiple trails of the last two rounds); alpha_5 is zero on lanes 0..3;
- the pair's difference is zero on byte 135, but both messages have byte
  135 = 0xEE (a 1084-bit message), so the pair itself is outside this target's
  byte-string domain. It is evidence for the trail core and the method, not a
  certificate.

Tu, Song, Wu, Guo, Weng and Xing, "Enhancing SAT solving to find (near)
collisions in 6-round SHA-3 variants" (ePrint 2026/2107), Section 5.2: with the
same permutation, rate 1088 and capacity 512 (SHAKE256), the measured hit rate
in connector spaces matched the multiple-trail estimate (4-round case: single
trail 2^-18, measured 2^-16 per pair, 59-74 collisions in each batch of 2^22
pairs), and a 5-round full-512-bit collision was found with a 2-round
connector plus 3-round trail.

Public Yukon submission 7deb1595 (solver Th0rgal) reports, through organizer
executed experiments, a byte-aligned (135-byte, p = 8) GLL+20-type 2-round
connector for trail core No. 3 (translated by 8 bit positions along z) with
DF = 36 on one base, accepted bases with DF 35, 27, 25, 26 and 24, three
certified 135-byte collisions, and a central per-pair collision-rate
estimate of 2^-37.219 (lower 95% value 2^-38.38). We use only these reported
facts: as evidence that p = 8 connectors with DF >= 33 exist for this trail
core, and to lower our trail-rate premise from the source's 2^-36.70 to
2^-37.22. None of that package's text, code, certificates or parameters is
used. Public submission
a7fb31c0 (solver rubenmarcus) first packaged a hard-capped GLL+20 attack for
this track; the idea of capping connector work by a counter and treating the
published trail core as a fixed constant is credited to it. The schedule,
heuristics, probability argument and all text here are ours.

## 3. Trail core No. 3 (the only advice)

Format of GLL+20 Table 9, reproduced verbatim: each line is one plane y = 0..4
(top to bottom); each field is lane x = 0..4 (left to right) as 16 hex digits,
most significant first (bit z = 63 leftmost); "-" is 0.

    beta_2 (weight w2 = 24, #AS 10)
    ---------------1|----------------|---------------4|----------------|----------------
    ---------------4|---------------4|---------------4|-----------2----|----------------
    2---------------|----------------|----------2-----|----------------|----------------
    2---------------|----------------|----------------|-----------2----|----------------
    ----------2----1|----------------|----------2-----|----------------|---------------1

    beta_3 (weight w3 = 19, #AS 9)
    ---------------1|----------------|---------------1|------4---------|----------------
    ----------------|----------------|---------------1|----------------|-----------4----
    ----------------|-------------1--|----------------|----------------|-----------4----
    ----------------|----------------|----------------|----------------|----------------
    ---------------1|-------------1--|----------------|------4---------|----------------

As (x,y,z) bit lists: beta_2 = (0,0,0) (2,0,2) (0,1,2) (1,1,2) (2,1,2)
(3,1,17) (0,2,61) (2,2,21) (0,3,61) (3,3,17) (0,4,0) (0,4,21) (2,4,21)
(4,4,0); beta_3 = (0,0,0) (2,0,0) (3,0,38) (2,1,0) (4,1,18) (1,2,8)
(4,2,18) (0,4,0) (1,4,8) (3,4,38).

Derived constants, recomputed in setup step P0.4: alpha_2 = L^-1(beta_2) has 59
active rows; the minimum reverse weight of alpha_2 is w1 = 127; every row of
beta_2 is DDT-compatible with the same row of L^-1(beta_3); SHA-256 of the
200-byte little-endian encodings: beta_2 39965c14...1fad8ca5, alpha_2
cad77082...9f31e9b5. The 3-round trail from alpha_2 (rounds 2, 3, 4) gives a
collision on lanes 0..3 with probability 2^-36.70 (GLL+20, Table 9 caption):
2^-24 for beta_2 -> L^-1(beta_3), and the remaining 2^-12.70 summed over
last-two-round trails ending with zero difference on the digest lanes.

The trail core is a constant of the algorithm text, like the round constants.
It is stored as two 200-byte states (400 bytes, advice 2^8.65 bytes, declared
as 2^10). No trail search is part of this algorithm; the published core is
used as given and its stated properties are re-verified in P0 at charged cost.

## 4. The algorithm

### 4.1 Data representation and the operation counter

Linear equations over GF(2) are bit vectors (coefficients plus a constant bit)
stored in 256-bit words: 7 words for the 1600 x-variables, 5 words for the
1080 difference variables. A system is kept in reduced echelon form with a
pivot table. Adding an equation means reducing it by the existing pivots; it
is redundant if it reduces to 0 = 0, inconsistent if it reduces to 0 = 1, and
otherwise becomes a new pivot on its least-index variable with a nonzero
coefficient (and is eliminated from the other pivot rows).
"Consistent with E" means that adding it to a copy of E is not inconsistent;
"implied by E" means that it reduces to 0 = 0.

Random choices use the RAM model's uniform random word primitive. A "uniform
random order" of a list is a Fisher-Yates shuffle with rejection sampling.

Every primitive operation executed in a connector run (Section 4.3), including
the operations that update and test the counter, is added to a run counter
before it executes, in blocks of at most 2^16 operations. The run stops as
soon as the counter would exceed b = 4.939776 x 10^17 primitive operations
(Section 6); a stopped run returns "no space".

### 4.2 Setup P0 (once; counter cap 2^30 primitive operations)

- P0.1 The 32x32 DDT; for each nonzero (din,dout) with DDT > 0, the canonical
  equations of V(din,dout): the reduced-echelon basis of the annihilator of
  its direction space, with constants evaluated at its least element.
- P0.2 Best inputs: for each nonzero dout, the list Best(dout) of din with
  maximal DDT(din,dout), increasing order.
- P0.3 Lists of affine subspaces of GF(2)^5, each listed in lexicographic
  order of its sorted element tuple:
  - Comp(dout): all 2-dimensional affine subspaces contained in
    {din : DDT(din,dout) > 0}. Each nonzero dout has at least 5 (checked).
  - Lin(U) for each nonzero 5-bit mask U: all affine subspaces W of the
    largest dimension d(U) such that each output bit of S marked by U is an
    affine function of the input on W. Exhaustive computation gives d(U) = 4
    for one marked bit (6 subspaces) or two cyclically adjacent marked bits (2),
    d(U) = 3 (4 to 36 subspaces) for the other U != 11111, and d(11111) = 2
    (the 80 linearizable subspaces of GLL+20 Observation 1).
  - Six(din,dout) for DDT(din,dout) = 8: the six 2-dimensional subspaces of
    V(din,dout) on which S is affine (Observation 2b); V(din,dout) itself has
    exactly one output bit k*(din,dout) that is not affine on it
    (Observation 4). For DDT = 2 or 4, S is affine on V (Observation 2a).
    These facts were checked exhaustively.
  - For each listed W (and each V) and each output bit k: an affine function
    f_{W,k}(x) = c XOR a.x equal to S_k on W, the lexicographically least such
    (a,c). Any agreeing function gives the same solution set below.
- P0.4 The 1600x1600 matrices of L and L^-1 (L^-1 by Gaussian elimination);
  the 1080-column matrix of the map d -> L(d, 0^520) from message differences
  to beta_0; the trail-constant checks of Section 3 (any mismatch aborts).
- The explicit work of P0.1-P0.4 is below 2^27 primitive operations (the
  dominant step, inverting L, is 1600 pivots x 1600 rows x 14 words); P0 runs
  under a counter capped at 2^30 and aborts if it would exceed it.

### 4.3 One connector run

A run repeats attempts A1-A6 until an attempt returns an accepted space or the
run counter stops it.

A1. beta_1. For each active row of alpha_2, in increasing row index, choose din
uniformly from Best(alpha_2 row); inactive rows are 0. Set alpha_1 =
L^-1(beta_1). (Then the round-1 conditions consume exactly w1 = 127 bits.)

A2. Difference system E_D over the 1080 message-difference bits d
(alpha_0 = (d, 0^520), beta_0 = L(alpha_0), linear in d):
- first, for each row where alpha_1 is zero (increasing row index), the 5
  equations "beta_0 row = 0"; if they are inconsistent the attempt fails;
- then, for each row where alpha_1 is nonzero, in increasing row index: take
  Comp(alpha_1 row) in a uniform random order and add the 3 equations of the
  first subspace consistent with E_D. If none is consistent, the attempt fails
  (go to A1).

A3. Fixing beta_0. For each row where alpha_1 is nonzero, in increasing row
index: take the 4 elements of the subspace chosen in A2 in a uniform random
order and add "beta_0 row = e" for the first element e consistent with E_D.
Such e exists whenever E_D is consistent, because the set of values of that
row allowed by E_D is a nonempty subset of the chosen subspace. After A3 every
row of beta_0 is fixed, so beta_0 is unique, d is unique, and
Delta = d (the 135-byte message difference).

A4. Value system E_M over x = L(S_0) in GF(2)^1600 (S_0 the initial state):
- Eq. (3): the 520 equations "(L^-1 x)_j = s_j" for j = 1080..1599, with s_j
  the fixed padding/capacity bits of Section 1;
- Eq. (2): for each active row of beta_0, in increasing row index, the
  equations of V(beta_0 row, alpha_1 row).
If E_M is inconsistent, the attempt fails (go to A1).

A5. Round-1 conditions. With y = chi(x) and z = L(y XOR RC0), where RC0 is
RC[0] in lane 0, for each active row of beta_1 take the equations a.z = c of
V(beta_1 row, alpha_2 row) and rewrite them as (L^T a).y = c XOR a.L(RC0).
These 127 equations are Eq. (4). The flag u_k = 1 if y_k has a nonzero
coefficient in some Eq. (4) equation; U_i is the 5-bit flag of row i.

A6. Linearization and acceptance (mainLinearization with cnt = 256). Repeat for
t = 1..256:
- Copy E' = E_M (as after A4).
- preProcess: for each row i with U_i != 0, in increasing row index:
  - beta_0 row active with DDT 2 or 4: use f_{V,k} for the marked bits.
  - beta_0 row active with DDT 8: if bit k* is not marked by U_i, use
    f_{V,k}; otherwise, if some W in Six (list order) has all its equations
    implied by E', use the first such W; otherwise put i on the list lsb.
  - beta_0 row inactive: if some W in Lin(U_i) (list order) has all its
    equations implied by E', use the first such W; otherwise put i on lsb.
- basicLinearization: for each i in lsb, in increasing row index, take the
  candidate list (Six for an active DDT-8 row, Lin(U_i) for an inactive row)
  in a uniform random order and add to E' the equations of the first W
  consistent with E'. If none is consistent, this t fails.
- Substitute y_k = f_{W,k}(x row) (with W the space used for row i, or V) into
  every Eq. (4) equation; this is Eq. (7). Add its 127 equations to E' in
  Eq. (4) order; if one is inconsistent, this t fails. Otherwise let
  DF = 1600 - rank(E'). If DF >= 33, return the accepted space:
  the reduced echelon form of E' (its solution set, an affine space of
  dimension DF) and Delta.
  Otherwise this t fails.
If all 256 values of t fail, the attempt fails (go to A1).

### 4.4 Brute force on one accepted space

B1. From the reduced echelon form of E', take x0 = the solution with all free
variables 0, and e_k = the homogeneous solution with the k-th free variable
(in increasing variable index) equal to 1 and the other free variables 0.
Map e_1..e_33 and x0 through L^-1 and keep the 1080 message bits:
m_1..m_33 and M_0 (at most 2^24 primitive operations). The map
x -> message is injective on the solution space because the 520 other bits of
L^-1 x are fixed, so the 2^33 messages below are distinct.

B2. Enumerate M in Gray-code order over c in {0,1}^33 (M = M_0 XOR sum c_k m_k,
one XOR of m_k per step). For each M compute the target digest of M and of
M XOR Delta (two 5-round calls) and compare the 256-bit digests. Each step
costs 2 units plus at most 128 primitive operations: Gray index (lowest set
bit of the step number by a 6-step mask/shift search, at most 30), M update
(5 loads, 5 XOR, 5 stores), M XOR Delta (15 likewise), forming the two input
states from M, M XOR Delta and the constant padding/capacity words (at most
20 loads, ORs and stores), one 256-bit compare and branch (4), loop control
(3): at most 87.

B3. On equality, recompute both hashes with the reference function on the two
135-byte strings (2 units) and output the pair.

### 4.5 Outer loop

Run setup P0 once. Then for run index 1..N with N = 40: execute one connector
run (Section 4.3) with fresh coins and a fresh counter; if it returns an
accepted space, run B1-B3 on it; stop at the first output pair. If all 40 runs
end without a pair, output failure.

## 5. Correctness of a returned pair

Let x satisfy the final E' of an accepted space and S_0 = L^-1 x. By Eq. (3)
S_0 is the padded block of a 135-byte message M (byte 135 = 0x86, capacity
zero). Let M' = M XOR Delta; it has the same last byte because Delta is zero
on bits 1080..1599.

Round 0. The input difference of chi is beta_0 = L(Delta, 0). For each active
row, x row is in V(beta_0 row, alpha_1 row) by Eq. (2), so its output
difference is alpha_1 row; inactive rows have zero difference. So the
difference after round 0 is alpha_1, and beta_1 = L(alpha_1) enters round 1.

Round 1. On the solution space each marked y_k equals f_{W,k}(x row) (x row is
in W or V by the added equations), so Eq. (7) is equivalent to Eq. (4) there:
z row is in V(beta_1 row, alpha_2 row) for every active row of beta_1. The
condition is symmetric in the pair (z, z XOR beta_1), so the difference after
round 1 is exactly alpha_2, for every element of the space.

Rounds 2-4 are the trail core; a pair is output only if the digests are equal,
and B3 rechecks it with the reference function. Delta != 0 because alpha_2 != 0
and the round function is a permutation. So any output pair is a valid
ordinary collision of two distinct 135-byte messages.

Each unordered pair {M, M XOR Delta} contains at most two enumerated messages,
so the 2^33 enumerated messages give at least 2^32 distinct pairs.

## 6. Time: hard caps on every random tape

Units: one 5-round permutation call = 1 unit; one primitive = 1/1355 unit.
Conversion constant R = 16 x 5 x 10^9 x 3600 = 2.88 x 10^14 primitive
operations per core-hour (H3). Source connector cost Tc = 428.8 core-hours.
N = 40 runs (Section 4.5).

- Per-run cap: b = 4 x Tc x R = 4.939776 x 10^17 primitives = 2^58.7772
  primitives = 2^48.3731 units. With block granularity a run executes at most
  b + 2^16 primitives.
- Connector total: 40 x (b + 2^16) primitives = 1.975910 x 10^19 = 2^64.0991
  primitives = 1.458236 x 10^16 units = 2^53.6951 units.
- Brute force: at most 40 accepted spaces, each at most
  2^33 x (2 + 128/1355) + 2^24/1355 units = 1.7991 x 10^10 = 2^34.0666 units;
  total at most 7.197 x 10^11 = 2^39.389 units.
- Setup P0: at most 2^30 primitives = 7.92 x 10^5 = 2^19.596 units.
- Final verification: 2 units.

Total T <= 1.458236 x 10^16 + 7.197 x 10^11 + 7.92 x 10^5 + 2 units
= 1.458308 x 10^16 units = 2^53.6952 < 2^53.7.

Every term is a counter or loop bound fixed in Section 4. No heuristic enters
this bound; the heuristics only decide how likely the caps are to suffice.

## 7. Success probability

Probability space: the algorithm's fresh uniform random words, for the fixed
target. Success event: the algorithm outputs two distinct 135-byte messages
with equal sha3-256-r5 digests (Section 5) within the caps of Section 6.

Runs are independent: each uses fresh coins, the target is fixed, and no state
passes between runs. Let p_b be the probability that one run returns an
accepted space before its counter stops it.

- H1 + H3 give a mean run cost (until acceptance) of at most
  E* = 2 x Tc x R = b / 2 primitives at p = 8. By Markov's inequality,
  p_b >= 1 - E*/b = 1/2.
- H2: given an accepted space, the brute force finds a collision with
  probability at least q_s = 1 - exp(-2^32 x 2^-37.22) = 1 - exp(-0.026830)
  = 0.026473.
- One run yields a collision with probability at least p_b q_s >= 0.013237.
- Pr[failure] <= (1 - 0.013237)^40 = exp(40 ln 0.986763) = exp(-0.53300)
  = 0.58684, so Pr[success] >= 0.41316 >= 0.40 (declared), above the lane
  minimum 0.39.

Sensitivity (time bound unchanged in every case): at the source's computed
rate 2^-36.70 success would be 0.533; at the public lower 95% value 2^-38.38
it would be 0.213; if the per-run rate p_b q_s were half of 0.013237 (for
example, mean run cost 4 x Tc x R instead of 2 x), 0.233.

## 8. Memory, preprocessing and advice

Peak memory: L, L^-1 and L^T (3 x 1600 rows x 7 words x 32 bytes = 1,075,200
bytes), E_M and E' (at most 1600 pivot rows x 7 words x 32 bytes = 358,400
bytes each), E_D (at most 1080 x 5 x 32 = 172,800 bytes), tables of P0 (under
65,536 bytes), the 33-vector message basis and working states (under 8,192
bytes) and the 400-byte trail core: 2,038,928 bytes, below 2^21. With code
(under 2^22 bytes for this linear algebra and Keccak) the peak is below 2^23
bytes. Declared 2^24. Runs keep nothing from earlier runs.

Preprocessing: P0, at most 2^19.6 units, declared 20 and also included in the
time bound. Nonuniform advice: the 400-byte trail core of Section 3, declared
2^10 bytes; it is a published constant that P0 re-verifies at charged cost.

## 9. Heuristics

H1-connector-p8 (score-critical). Statement: for this algorithm at p = 8, the
expected number of primitive operations of one connector run until it returns
an accepted space (DF >= 33) is at most 2 x Tc x R = 2.469888 x 10^17.
Evidence: GLL+20 Table 6 (Tc = 428.8 core-hours, DF = 37 at p = 4, same trail
core, same Algorithms 1-3); the DF estimate, Eq. (11), in which p enters
through the (c+p) term, so four extra fixed bits predict a loss of about 4
dimensions (37 -> 33) when the rest of the run is unchanged; and the public
byte-aligned report of Section 2 (DF 36 and 35 observed at p = 8 for this
trail core). Limitations: one source run, CPU model not given; the extra fixed
bits may lower the success rate of A2-A6 by more than the factor 2 allowed;
our retry counter (cnt = 256) and orders are explicit choices that the source
does not publish. The time bound does not depend on H1.

H2-trail-rate (score-critical). Statement: for an accepted space, the at least
2^32 distinct pairs it supplies behave, for rounds 2-4, as independent trials
with collision probability at least 2^-37.22 each, so the brute force succeeds
with probability at least 1 - exp(-2^32 x 2^-37.22) = 0.026473. Evidence:
GLL+20 Table 9 caption (2^-36.70 including multiple last-two-round trails) and
Table 6 (one collision found in a DF-37 space, as predicted); the public
byte-aligned report of Section 2 (three certified collisions; central rate
estimate 2^-37.219 for byte-aligned connector spaces of this trail core); ePrint 2026/2107 Section 5.2
(measured connector-space hit rates match the multiple-trail estimate). Our
trace of the Table 17 pair (Section 2) confirms the trail core and the digest
condition on the organizer permutation. We take the lower of the computed and
reported rates. Limitations: pairs inside one space are not independent;
values entering round 2 are constrained by the connector; the reported rate
rests on few events (its lower 95% value is 2^-38.38).

H3-op-conversion (score-critical). Statement: one core-hour of the source's
connector computation corresponds to at most R = 2.88 x 10^14 primitive
operations of this algorithm on the v5 word RAM; that is, an implementation of
Section 4.3 does no more primitive work per unit of progress than the source's
single core did, and that core executed at most 16 primitive-equivalent
operations per cycle at no more than 5 GHz. Evidence: a 4-wide retirement of
fused load+operate micro-operations on 512-bit registers is at most
4 x 4 = 16 256-bit operations per cycle; 5 GHz is above the sustained clock of
CPUs available to the source; Section 4 performs the same linear algebra on
256-bit words. Limitations: the source code and CPU are not public, so the
efficiency premise is not measured.

## 10. Weaknesses and counterevidence

- Nothing was executed for this package; there is no byte-aligned certificate.
- The SHA3-256 connector was the hardest case in GLL+20 (DF 37 against
  w = 36.70); the authors state that non-full linearization was essential.
  Four more fixed bits can only remove freedom.
- The public byte-aligned report also shows accepted bases with DF 24-27,
  below our threshold 33. So DF >= 33 is not guaranteed per accepted base; H1
  absorbs this through the factor 2 and Markov's inequality, and a shortfall
  lowers success, not the charged time.
- That report's measured trail rate (2^-37.219) is below the source's
  2^-36.70; we use the lower value, but its uncertainty is large.
- The conversion of core-hours to primitives is generous rather than
  measured (H3).
- This package does not beat the executed, certified byte-aligned results
  already public for this track; it is an independent analytical bound.

## 11. References

- J. Guo, G. Liao, G. Liu, M. Liu, K. Qiao, L. Song. Practical collision
  attacks against round-reduced SHA-3. Journal of Cryptology 33 (2020);
  IACR ePrint 2019/147.
- Y. Tu, L. Song, H. Wu, J. Guo, J. Weng, C. Xing. Enhancing SAT solving to
  find (near) collisions in 6-round SHA-3 variants. IACR ePrint 2026/2107.
- I. Dinur, O. Dunkelman, A. Shamir. New attacks on Keccak-224 and
  Keccak-256. FSE 2012 (target difference algorithm).
- NIST FIPS 202 (SHA-3 standard).
- Yukon submissions a7fb31c0 (rubenmarcus) and 7deb1595 (Th0rgal), credited in
  Section 2 for packaging and for reported facts only.
