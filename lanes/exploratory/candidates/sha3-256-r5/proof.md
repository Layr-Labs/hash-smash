# Five-round SHA3-256 collisions from a 2-round linearized connector and a 3-round trail

This exploratory package claims an ordinary-collision algorithm for the
`sha3-256-r5-prefix-v1` target with total charged time at most 2^56.6
target-permutation units under `collision-frontier-v5`, peak memory at most
2^32 bytes, and heuristic success probability at least 0.5.

The construction is the differential attack of Guo, Liao, Liu, Liu, Qiao and
Song, "Practical Collision Attacks against Round-Reduced SHA-3", Journal of
Cryptology 33 (2020) 228-270, IACR ePrint 2019/147 (cited below as GLL+20).
That paper reports a real 5-round SHA3-256 collision. This package does not
reuse that pair as a witness. The published messages are 1084 bits long,
not whole bytes, so they lie outside this target's byte-string domain
(Section 3). The algorithm below reruns the published construction for
135-byte messages. That fixes four more input bits than the authors fixed.
Every phase is charged, including the trail search that produced the
hard-coded trail core and every connector run, failed or not. The score rests
on four declared heuristics (Section 8). It is not a proof and it does not
include a target collision certificate. The certificate manifest is valid and
empty.

## 1. Exact target

H is the complete five-round SHA3-256 sponge of the organizer reference
`verifier/keccak.py:sha3_256(data, 5)`. The state has 1600 bits held as 25
little-endian 64-bit lanes A[x+5y], with x,y in 0..4. State bit (x,y,z) is bit
z of lane x+5y. Message byte i, bit j (LSB first) is state bit 8i+j of the
absorbed block, in lane floor(i/8). The rate is 1088 bits (17 lanes, 136
bytes) and the capacity is 512 bits. The initial state is all-zero. A byte
message m is padded with SHA3 domain suffix 01 and pad10*1. For a message of
exactly 135 bytes, the padded message is the single block m || 0x86. Each
absorbed block is XORed into lanes 0..16 and followed by rounds 0,1,2,3,4 of
Keccak-f[1600]. Every round is R = iota o chi o pi o rho o theta:

    C[x] = A[x,0]^A[x,1]^A[x,2]^A[x,3]^A[x,4]
    D[x] = C[x-1] ^ ROT64(C[x+1],1);   A[x,y] ^= D[x]
    B[y,2x+3y] = ROT64(A[x,y], rho[x,y])
    A[x,y] = B[x,y] ^ (~B[x+1,y] & B[x+2,y]);   A[0,0] ^= RC[i]

The rho offsets for rows y=0..4 and columns x=0..4 are
0 1 62 28 27 / 36 44 6 55 20 / 3 10 43 25 39 / 41 45 15 21 8 / 18 2 61 56 14.
RC[0..4] = 0x1, 0x8082, 0x800000000000808A, 0x8000000080008000, 0x808B.
These are the first five rounds (prefix reduction), not Keccak-p's last-round
convention. The digest is the 32 bytes LE64(A[0])||...||LE64(A[3]); no further
permutation is needed. An ordinary collision is two distinct byte strings with
equal 256-bit digests. Free-start, raw-permutation, and non-byte-aligned inputs
are excluded.

Let L = pi o rho o theta. It is linear over GF(2) and invertible, and iota
does not affect XOR differences. Following GLL+20 (Section 3.1), alpha_i is
the state difference entering round i, and beta_i = L(alpha_i) is the
difference entering chi in round i. So round i maps
alpha_i --L--> beta_i --chi--> alpha_{i+1}. Each 5-bit row of the chi input is
one S-box. "Active" means a nonzero row difference. DDT(din,dout) is the
5-bit S-box difference distribution table.

All algorithm messages are exactly 135 bytes. In the padded block, bits
1080..1087 (byte 135 = 0x86, LSB first) are fixed to 0,1,1,0,0,0,0,1, and
bits 1088..1599 (the capacity) are zero. Thus c+p = 512+8 = 520 bits of the
initial state are fixed, and 1080 bits are free. This differs from GLL+20,
which fixed only c+p = 512+4 = 516 bits: their padded block ended in the 4-bit
pattern 0,1,1,1, so their messages had 1084 bits (GLL+20 Section 3.2,
"r - 4 free bits" for SHA3-d).

## 2. Hard-coded data: trail core No. 3

The algorithm hard-codes GLL+20 trail core No. 3 (their Table 5, Table 9). It
gives the chi-input differences of rounds 2 and 3. Below, rows are y=0..4,
columns are x=0..4, and each lane is a 16-hex-digit 64-bit integer, most
significant digit first, with '-' meaning 0. This is the GLL+20 display
convention. The rows were recomputed from the published colliding pair
(Section 3) with the organizer round function and match the paper's table
character for character.

    beta2 (10 active S-boxes; w2 = 24)
    ---------------1|----------------|---------------4|----------------|----------------
    ---------------4|---------------4|---------------4|-----------2----|----------------
    2---------------|----------------|----------2-----|----------------|----------------
    2---------------|----------------|----------------|-----------2----|----------------
    ----------2----1|----------------|----------2-----|----------------|---------------1

    beta3 (9 active S-boxes; w3 = 19)
    ---------------1|----------------|---------------1|------4---------|----------------
    ----------------|----------------|---------------1|----------------|-----------4----
    ----------------|-------------1--|----------------|----------------|-----------4----
    ----------------|----------------|----------------|----------------|----------------
    ---------------1|-------------1--|----------------|------4---------|----------------

The connector target is Delta_SI = alpha2 = L^{-1}(beta2). It has 59 active
S-boxes, and its minimal backward weight is w1 = 127 (GLL+20 Table 5). In
round 4 the trail only needs the first 256 output bits of alpha5 to be zero.
The weight of the last three rounds is w2+w3+w4^d = 43 for the single core,
and 36.70 once the paper aggregates the multiple round-3/round-4 trails that
also give a digest collision (GLL+20 Table 6, footnote *). The brute-force
stage tests only digest equality, so no particular round-4 difference has to
be followed. The hard-coded data is 2*1600 bits, under 2^10 bytes, and its
search cost is charged in Section 6.

## 3. Verified source evidence and why it is not a certificate

GLL+20 Table 17 prints the following 5-round SHA3-256 collision. Each line
lists absorbed lanes 0..4, 5..9, 10..14 and 15..16; lanes 17..24 are zero.

    M1: FECA67BD2D3F021A BD10A64A4C2B774F F8EF6FF82DD21FC7 6F4BA4D964A78764 0F4FD1C92A24BC6E
        FB4B8C0A11C64088 EDA7B9EBC05F50A8 0A71DD08E7F1EB5B 5342D2AE78A8BFB5 6591A9B0CC2E7CE9
        52A3DD827F4EF6DC 9D89B18362B80DE4 FEA719A1875BFFF7 49A2B95AD7B7D147 B23784B72EB9260A
        187AEFD07295FD59 EE806366EF9D09FF
    M2: 16F97050842C2D17 A731EE935A43480A 6D8E356BDBD7CBE9 D62C0B356FFA158A 4FAD968080C7F8C8
        7C83B8E1C61BC5AB 7E3FCA22B5E29305 5888D4DBE848C840 236DE21CCEF77B8A 69D59EF589070E60
        E87FCD2BF2C6CCE1 B1E28B821FD93ABC AD5D6FB1860CB45C AB8FC7D1015975D5 24C6B737EE96CC23
        D3BFB5957965A447 EE31D3F5269F254F

These lanes were serialized little-endian into 200-byte states and passed to
the organizer's `verifier.keccak.permutation(state, rounds=5)` (prefix rounds
0..4, all-zero capacity). Both outputs begin with the same 32 bytes

    b440608b2e7c0165d64b3b93bbf84f340320be6833f1a3c6cb5a43334b7b42ab

that is, lanes 65017C2E8B6040B4 344FF8BB933B4BD6 C6A3F13368BE2003
AB427B4B33435ACB, matching the paper's printed digest. The paper's round
convention (rounds 0..4 from the zero state) therefore matches this target's
permutation. Tracing the pair's differences with the same round function
reproduces the trail exactly: #AS(beta1) = 59, beta2 and beta3 equal Section 2
bit for bit, and the first four lanes of alpha5 are zero. The message
difference has Hamming weight 525, and its byte 135 is zero.

These blocks are not padded byte strings. Byte 135 of both blocks is 0xEE.
Its upper nibble (bits 1084..1087 = 0,1,1,1) is the SHA3 suffix 01 followed by
pad10*1 with no zero bits. This is the padding of a 1084-bit message whose
last four bits (bits 1080..1083) are 0,1,1,1. A byte-string message padded to
one block ends in 0x86 (135 bytes) or 0x80 (shorter), never 0xEE. A
multi-block message would absorb this block into a nonzero chaining state.
As a check, replacing byte 135 by 0x86 in both blocks (the two 135-byte
prefixes) gives five-round digests that differ in 136 bits. The published pair
is therefore real evidence that the GLL+20 connector and trail work for the
1084-bit-input variant. It is not a collision for this target, and the
package contains no certificate.

## 4. The algorithm

The parameters are fixed in advance: K = 128 connector spaces, and a total
connector budget of B_c = 128 * 8 * 428.8 = 439,091.2 core-hour equivalents.
Section 6 converts B_c to 2^66.745 RAM primitives. The algorithm runs
Steps 0-3 below. It stops at the first verified collision, or when K spaces
have been enumerated, or when the connector budget is exhausted.

### Step 0 (preprocessing, run once): trail core

Hard-code beta2 and beta3 from Section 2. Compute alpha2 = L^{-1}(beta2) and
alpha3 = L^{-1}(beta3). Precompute the 1600x1600 GF(2) matrices of L and
L^{-1}, the 32x32 DDT, and, for every DDT entry, the affine solution set
V(din,dout) = {v : S(v)+S(v+din) = dout} written as 5-dim(V) linear equations.
Also precompute the 80 two-dimensional linearizable affine subspaces of the
S-box (GLL+20 Observation 1, Table 7) and, for each DDT-8 entry, its six
linearizable 2-dimensional subsets (Observation 2b). The work that originally
found the trail core is charged as preprocessing (Section 6.2).

### Step 1: one 2-round connector run (GLL+20 Sections 4.3, 4.5, 4.6)

The unknown is x, the 1600-bit chi0 input of the first message (x = L(S0),
where S0 is the initial state). Let y = chi0(x), z = L(y + RC0) be the chi1
input, and E_M be the value system over x.

1a. Choose beta1. For each of the 59 active S-boxes of alpha2, choose din
    uniformly among inputs that reach the given output difference with the
    best DDT probability. This gives beta1 and alpha1 = L^{-1}(beta1).
    Derive the second-round constraint B*z = t_B (Eq. 1). For each active
    S-box this is the set of 5-dim(V(din,dout)) equations of
    V(din,dout), with dim V = 1, 2, 3 for DDT entries 2, 4, 8.

1b. Choose beta0 with the target difference algorithm of Dinur et al.
    (GLL+20 Section 4.6). Keep a difference system E_Delta over beta0.
    Initialize it with: (i) for all 520 fixed initial-state bits, alpha0 =
    L^{-1}(beta0) is zero there (520 linear equations in beta0); (ii) rows
    of beta0 under non-active S-boxes of alpha1 are zero. For each active
    S-box of alpha1, add the 3 equations of a randomly chosen 2-dimensional
    affine subset of compatible input differences, keeping only consistent
    choices. Then, S-box by S-box, add 2 more equations to fix one specific
    din, and add to E_M the value equations of V(din,dout) on that S-box's
    five x-bits (Eq. 2, A1*x = t_A1). E_M starts with the 520 fixed-bit value
    equations of Eq. 3, A2*x = t_A2, which are rows of L^{-1} set equal to the
    fixed bits. The only difference from GLL+20 is that the fixed-bit set
    has 520 bits instead of 516.

1c. Set flags. Substitute z = L(y + RC0) in Eq. 1 to get B*L*(y+RC0) = t_B
    (Eq. 4). Set flag u_i = 1 when y_i has a nonzero coefficient there. The
    5-bit groups U_j mark which outputs of first-round S-box j must be
    linear in x.

1d. Linearize the first round (Algorithms 1-3 of GLL+20). Run preProcess:
    S-boxes whose marked outputs are already linear under E_M (DDT 2 or 4
    entries, DDT 8 entries whose single nonlinear output y1 is unmarked, or a
    linearizing subspace already implied by E_M) need no equation. For each
    other S-box with U_j != 0, try random linearizing equation sets (Eq. 5,
    A3*x = t_A3) and keep the first one consistent with E_M:
      - Non-active S-box: by Observation 3, fix 1 input bit if U_j has one
        marked bit or two cyclically adjacent marked bits, 2 bits if
        U_j != 11111 otherwise, and 3 non-adjacent bits (a full
        linearization) if U_j = 11111. For example, y0 = x0 + (x1+1)x2 is
        linear once x1 is fixed.
      - Active DDT-8 S-box: 4 of 5 outputs are already linear on V. If the
        nonlinear output is marked, add the one equation selecting one of
        the six linearizable subsets.
    The result is an affine map y_marked = L_chi0*x + t_chi0 (Eq. 6).
    Substitute it into Eq. 4 to get Eq. 7,
    B*L*L_chi0*x + B*L*(t_chi0 + RC0) = t_B. If Eq. 7 is consistent with
    E_M, add it. Otherwise retry 1d with fresh random choices up to a fixed
    counter, then restart from 1a with a new beta1.

1e. Output. Gaussian elimination of E_M (all of Eqs. 2, 3, 5, 7) gives
    x0 and a basis x-hat_1..x-hat_DF of its solution space. Map each to
    the message domain with S0 = L^{-1}(x). Bytes 0..134 of the absorbed
    block of L^{-1}(x0) form message M_0. The images of the basis vectors,
    restricted to lanes 0..16, form w_1..w_DF; their byte 135 and capacity
    are zero by Eq. 3. Delta is bytes 0..134 of alpha0 = L^{-1}(beta0).
    Every x in the space satisfies the round-0 S-box value conditions (Eq.
    2) and the round-1 conditions (Eq. 7). Hence, for every message M in
    the space, R_2(M) + R_2(M + Delta) = alpha2 deterministically. This is
    the connector property (GLL+20 Section 3.2).

All equation handling is incremental row reduction over GF(2). One 1601-bit
equation is seven 256-bit words. Each insertion reduces against at most 1600
pivots.

### Step 2: brute-force stage on one space (GLL+20 Section 3.2, Stage 2)

Enumerate all 2^DF messages M_0 + sum(c_k w_k) in Gray-code order. Each step
XORs one precomputed 17-lane basis image into M and forms M' = M + Delta with
17 lane XORs. Absorb both into zero states with byte 135 = 0x86 (lane 16 gets
0x86 << 56 XORed into its message value), and apply the five-round
permutation to each, one unit each. Compare lanes 0..3. On equality, run
Step 3.

### Step 3: verification

For a candidate (M, M'), check M != M' and recompute both digests with the
complete reference hash on the two 135-byte strings. Output the pair if all
256 digest bits agree; otherwise continue Step 2. M != M' always holds,
because Delta is nonzero on the rate. Alpha0 is nonzero, since a zero alpha0
would make beta0, and hence alpha1 and beta1, zero, contradicting the
nonzero alpha2. Alpha0 is zero on all 520 fixed bits, so its nonzero bits
are message bits 0..1079.

### Outer loop

Repeat Step 1 (with fresh random choices) and Step 2 until K = 128 spaces
have been enumerated, the connector budget B_c is spent, or a collision is
returned. Each run makes fresh random choices of beta1 (among
best-probability inputs of 59 active S-boxes), of the 2-dimensional
input-difference subsets in 1b, and of linearizing subspaces in 1d. Spaces may
overlap. Overlap does not affect correctness; it only lowers the number of
fresh pairs, which H2 covers. The algorithm halts within the charged budget
in every outcome.

## 5. Correctness and success probability

Any returned pair consists of two distinct 135-byte messages whose complete
5-round SHA3-256 digests were recomputed and agree on all 256 bits. This is an
ordinary collision in the target, whatever the heuristics say. The heuristics
affect only the probability of reaching that output within the budget.

Under H1 (Section 8), each successful connector run returns a space of
dimension DF >= 33. The expected connector cost per successful space is at
most 2 * 428.8 core-hours. The sum of 128 such costs has expectation at most
128 * 857.6 core-hours = B_c / 4. Markov's inequality on that nonnegative sum
gives Pr[budget exhausted before 128 spaces] <= 1/4. Markov needs no
independence assumption between runs.

Each space contributes at least 2^(DF-1) >= 2^32 distinct unordered pairs
{M, M+Delta}. A pair is counted twice if both members lie in the space.
Under H2, each such pair gives a digest collision with probability at least
q = 2^-37.7, and successes are close enough to independent that the count is
approximately Poisson. This q is the paper's 2^-36.70 halved. Over 128
spaces, the expected number of colliding pairs is at least
lambda = 128 * 2^32 * 2^-37.7 = 2^1.3 = 2.46, and

    Pr[no collision | 128 spaces] <= exp(-2.46) = 0.0852.

Hence Pr[success] >= 1 - 1/4 - 0.0852 = 0.66. The claim declares 0.5, which
leaves room for dependence among pairs that share a space. Within one space,
pairs share the 2-round connector conditions, and their round-2 values form
an affine family. GLL+20's one observed space (DF = 37, w = 36.70) contained
exactly one collision (GLL+20 Section 6.2), consistent with the Poisson
estimate there: an expected 0.6 to 1.2 collisions, depending on whether 2^36
or 2^37 pairs are counted, at 2^-36.70 per pair.
The number is algorithmic success probability over the random connector
choices. It is not confidence in the heuristics.

DF accounting. GLL+20 Eq. 10 estimates

    DF = sum_j DF_j^(1) - (c+p) - sum_j (5 - DF_j^(2)).

The first and last terms depend on the trail and the linearization, not on
which initial-state bits are fixed. Raising p from 4 to 8 adds four equations
to Eq. 3. That lowers DF by at most 4, from the measured 37 to at least 33,
provided the system stays consistent. The added fixed bits can only increase
the preProcess savings (GLL+20 Algorithm 3, lines 11 and 16, which benefit
from a larger Eq. 3), so DF can come out higher. Four more zero-difference
constraints are also added to E_Delta. The published pair happens to have
zero difference on all of byte 135 already (Section 3). This shows such
beta0 values exist for core No. 3 under the stronger condition.

## 6. Cost accounting under collision-frontier-v5

One five-round Keccak-f[1600] call costs 1 unit. Every other 256-bit word-RAM
primitive costs 1/1355 unit. The table lists every phase. Ordinary operations
are converted at 1/1355 in the total.

| Phase | Permutation calls | Ordinary RAM primitives |
| --- | ---: | ---: |
| 0. Trail-core search (charged preprocessing) | 0 | <= 2^64.0 |
| 0'. L, L^{-1}, DDT and subspace tables | 0 | <= 2^30 |
| 1. Connector runs, all successes and failures (budget B_c) | 0 | <= 2^66.745 |
| 2. Brute force over 128 spaces of dimension <= 33 | <= 2^41 | <= 2^48 |
| 3. Verification of candidates and output | <= 2^10 | <= 2^20 |

### 6.1 Converting the measured connector time

GLL+20 Table 6 reports T_c = 428.8 hours on one CPU core for the 5-round
SHA3-256 connector, including all failed random beta1 and linearization
attempts until success. Their footnote says CPU times are single-core; GPUs
were used only for the 6-round row. No operation count is published, so this
package converts core-hours to RAM primitives with a hardware-throughput
ceiling (H3). No core sustains more than 2^48 / 3600 = 7.8 * 10^10
primitive word operations per second. That is 15.6 operations per cycle at
5 GHz, which exceeds 4-wide retirement even if every micro-op were a 512-bit
vector operation counted as two 256-bit primitives, with fused memory
operands counted separately. Every load, store, branch and address
computation is an instruction and is counted, so memory traffic is covered.
Thus one core-hour is at most 2^48 primitives, or 2^48/1355 = 2^37.60 units.

The budget allows 8 * 428.8 core-hours per required space. H1 bounds the
expected cost per space for the byte-aligned (p = 8) connector by twice the
measured 428.8. The 8x budget turns that expectation into the 1/4 Markov
loss of Section 5. Then B_c = 128 * 8 * 428.8 = 439,091.2 core-hours
= 2^18.744, and

    connector primitives <= 2^18.744 * 2^48 = 2^66.745,  i.e.  <= 2^56.341 units.

As a consistency check rather than the charge: one mainLinearization attempt
handles at most about 3,700 equations (Eq. 2 <= 960, Eq. 3 = 520,
Eq. 5 <= 960, Eq. 7 <= 1,280). Each reduction against at most 1600 pivots
costs at most 1600 * 25 primitives (7-word XOR, loads, stores, test). That is
at most 2^27.2 primitives per attempt. The 2^58.74 primitives of one measured
run would then correspond to at most about 2^31.5 attempts, which is
compatible with the paper's retry loop.

### 6.2 Trail-core search (preprocessing)

GLL+20 Appendix C.2 describes the search that produced core No. 3.
KeccakTools TrailCoreInKernelAtC (aMaxWeight 60) generates "more than 3000"
in-kernel beta3 cores. For each core, at most C1 <= 2^36 forward extensions
(alpha4 -> beta4 with a digest-compatibility check) and at most C2 <= 2^35
backward extensions (beta2 compatible with L^{-1}(beta3), with #AS(alpha2)
and requirement checks) are traversed. This package charges at most 2^13
cores, at most 2^14 primitives per extension step (a 1600-bit linear layer
on 25 lane words plus per-S-box DDT checks and requirement tests), and at
most 2^62 primitives for the KeccakTools core generation (H4):

    2^13 * (2^36 + 2^35) * 2^14 + 2^62 = 2^63.585 + 2^62 <= 2^64.0 primitives
                                       = 2^53.60 units.

GPU acceleration in the paper changes wall time, not the operation count
charged here. Nothing else in the attack is advice. The trail core is
recomputable by this search, and the published colliding pair is never used
by the algorithm.

### 6.3 Brute force and verification

The algorithm enumerates at most 2^33 messages per space. If a connector
returns DF > 33, it enumerates only the subspace with the extra coordinates
fixed to 0, so the charge holds. Each message costs two
permutation calls and at most 256 primitives: 17 basis-lane loads and XORs,
17 XORs for M', 2 * 25 state initializations, the padding-lane XOR, four lane
comparisons with branches, the Gray-code counter and loop control, all with
operand loads and stores. Over 128 spaces this is

    calls <= 2 * 128 * 2^33 = 2^41,  primitives <= 128 * 2^33 * 2^8 = 2^48.

Lowering the enumeration to 2^32 per space would not change the claimed
scalar. Verification runs the complete reference hash twice per candidate. A match
on lanes 0..3 is already a full 256-bit digest match, so Step 3 runs once,
on the returned pair. The table budgets 2^10 calls anyway.

### 6.4 Total

    T <= 2^41 + 2^10 + (2^64.0 + 2^30 + 2^66.745 + 2^48 + 2^20) / 1355
      = 2^41 + 2^53.596 + 2^56.341 + (smaller terms)
      = 2^56.541 units  <  2^56.6.

The claim declares time_log2 = 56.6. Under the v5 prices, the connector is
about 87% of the total and the trail search about 13%. Brute force is
negligible: 2^41 units against 2^56.5. The charge is not the paper's
practical running time. It is a conservative envelope built from the
measured core-hours with stated margins:

- 2x on the per-space connector expectation (H1);
- a further 4x so that Markov's inequality gives a fixed budget (Section 5);
- 2x on the trail probability (H2);
- DF floor 33 rather than the formula's DF >= 33 possibly larger;
- counting 2^(DF-1) pairs per space;
- a 2^48 core-hour ceiling, about 4x above a realistic 4-wide 5 GHz core
  (2^46).

A central estimate without these margins is about 13 connector runs times
428.8 core-hours at 2^47 primitives per core-hour, about 2^49 units. This
package does not claim that figure.

### 6.5 Memory, preprocessing, advice

The connector keeps L and L^{-1} (2 * 1600 * 1600 bits = 640 KB), E_M and
E_Delta (each at most 4,000 rows of 1601 bits, under 1 MB), the DDT and
linearizable-subspace tables (under 64 KB), and the 33 basis images
(33 * 17 lanes). The trail search is a depth-first traversal over at most 2^36
extensions per core. Its stack and the kept extension lists are budgeted at
2^30 bytes (H4). Code and constants are budgeted at 2^24 bytes. The peak is
at most 2^30 + 2^24 + 2^22 < 2^31 bytes, and the claim declares 2^32.
preprocessing_log2 = 54 bounds the trail-search phase (2^53.6 units) plus
table setup. The hard-coded trail core is 400 bytes, and its construction is
charged in 6.2. nonuniform_advice_log2_bytes = 10 covers it with room to
spare. All of these are included in T.

## 7. Relation to the nominal reference and other literature

The required `baseline_improved` identifier names the organizer's nominal
128-bit reference. It is not an established attack or a security bound.
Generic birthday search costs about 2^128 units. The claimed 2^56.6 depends on
the heuristics below. Other published 5-round SHA3-256 results are theoretical
and higher: Dinur-Dunkelman-Shamir FSE 2013 internal differentials (2^115 for
5-round Keccak-256); Zhang-Hou-Liu EUROCRYPT 2023 conditional internal
differentials (2^105); Zhang-Hou-Liu CRYPTO 2024 probabilistic linearization
(2^96.67). Guo-Liu-Song-Tu (ASIACRYPT 2022, SAT-based connectors) report much
larger first-round degrees of freedom for SHA3-256 connecting trails (330-430
versus about 124). That supports, but does not prove, the view that
first-round degrees of freedom are not the binding constraint once the
connector is tuned. This package does not use their trails.

## 8. Declared heuristics and limitations

H1 (score-critical): byte-aligned connector. With p = 8, the GLL+20 2-round
connector for trail core No. 3 still succeeds by random beta1 and
linearization retries. Its expected cost per successful space is at most
2 * 428.8 core-hours of the authors' implementation, and it returns DF >= 33.
Evidence: the measured p = 4 run (T_c = 428.8 h, DF = 37), Eq. 10's linear
dependence on p, and the published pair showing core No. 3 is connectable with
zero difference on byte 135. Limitation: this package has not run the
connector, and the p = 4 figure is one reported run, not a mean. The extra
fixed bits may reduce the rate of consistent linearizations by more than 2x.
The score moves by log2 of any excess factor: 4x more connector cost adds
2 bits.

H2 (score-critical): trail probability. Over messages in connector spaces,
Pr[digest collision of (M, M+Delta)] >= 2^-37.7, and the count over 2^39
pairs is close to Poisson. Evidence: the paper's multi-trail estimate
2^-36.70 and its observation of one collision in one DF-37 space. Limitation:
one observation, and the pairs within a space are correlated. Each halving
of q needs twice as many spaces, adding 1 bit to the score.

H3 (score-critical): hardware conversion. One core-hour of the authors' CPU
is at most 2^48 v5 primitives (Section 6.1). Limitation: the paper does not
name the CPU model. The bound relies on clock frequency below about 5 GHz and
issue width below 16 primitive-equivalents per cycle.

H4 (supporting): trail-search cost. The Appendix C.2 search that yields
core No. 3 is bounded as in Section 6.2. Limitation: the paper gives
thresholds, not run times; "more than 3000" cores is bounded by 2^13 here.
This term is 2^53.6 units and changes the total by 0.2 bits.

Weaknesses a reviewer may raise: no byte-aligned collision has been
produced. The connector algorithm is specified at the level of GLL+20
Algorithms 1-3 and inherits their unpublished implementation choices, such
as the retry counter and the tie-breaking in beta1 selection. The cost
conversion rests on a reported wall time, not an operation count. All four
points are acknowledged in H1-H4. None affects the correctness of a returned
pair, which is checked with the complete reference hash.
