# 5-round SHA3-256: byte-aligned two-block adaptation of the GLL+20 collision

Exploratory package: no byte-aligned pair computed, no certificate, no
experiment. [GLL+20] = J. Guo, G. Liao, G. Liu, M. Liu, K. Qiao, L. Song,
"Practical Collision Attacks against Round-Reduced SHA-3", J. Cryptology 33
(2020) 228-270, ePrint 2019/147. Accounting and p=8 adaptation follow the
compact charged restatement used on this track; heuristics H1-H8 are stated
once in Section 8.

## 0. Claim, summary, verification checklist

| Field | Value | Basis |
| --- | --- | --- |
| time_log2 | 50.3 | Section 6: computed 2^50.237, rounded up; a hard cap |
| success_probability | 0.44 | Section 5: 0.4415 >= 0.39 under H1-H4, H8 |
| memory_log2_bytes | 34 | Section 7 (reported, not scored) |
| preprocessing_log2 | 48.6 | Section 6: trail extensions 2^48.585, included in time |
| nonuniform_advice_log2_bytes | 0 | the trail search is run and charged |

Summary. [GLL+20] give a practical 5-round SHA3-256 collision: a 2-round linear
connector plus a 3-round trail (core No. 3). Their 1084-bit message is not a
byte string (p = 4 fixed padding bits; byte strings fix p >= 8). We redo the
attack at p = 8 on 271-byte messages M0||X with a uniformly random first block
M0. The algorithm runs a deterministic trail search (charged preprocessing),
then independent connector attempts, each with a fresh M0, under a hard work
cap of 23 mu, enumerating 2^32 pairs in each successful space (at most 1024)
with full sponge digests. The time is this cap, not an expected time; the
success probability is for the truncated algorithm. mu prices one successful
connector from the published 428.8 core-hours, f = 1.25 and 2^24.263 units/s
(paper G5 upper end: 2^22 full Keccak-f/s x 24/5; f = G7 p=8 slope only).

Verification checklist (each number is re-derivable from this file):

1. Message format: 271 = 136 + 135 bytes; final padded block X||0x86; fixed
   bits 8 + 512 = 520 (Section 1, Lemma 1).
2. Published inputs: SHA3-256 Tc = 428.8 h, DF = 37, Tb = 45.6 h; SHA3-224
   Tc = 11.7 h, DF = 83; core No. 3 weights 127-24-19-0 (Section 2).
3. Trail re-check on the Table 17 pair (hex in Section 3): equal digests,
   AS(alpha2) = 59, round-1 318 = 75x2 + 156x4 + 87x8, alpha0 = 0 on the
   lane-16 top byte (0xEE), C1 = 2^19, C2 = 2^31.70, 170 <= 188, 43 <= 55.
4. Outputs are distinct-message full collisions; pairs distinct (Lemma 2).
5. DF >= 33 = 37 - 4 by the rank fact (Section 4.1; H3).
6. p_pair = 2^-24 x 2^-13.219 = 2^-37.219, used as 2^-37.22 (Section 5).
7. s = 1 - exp(-2^32 x 2^-37.22) = 1 - exp(-0.02683) = 0.02647 (Section 5).
8. Pr[success] >= 1 - exp(-22 s) - (1-s)^1024 = 1 - 0.5585 - 1.2e-12 = 0.4415.
9. mu = f x Tc x R x 1.002 = 2^(0.322 + 20.558 + 24.263 + 0.003) = 2^45.146.
10. B_A = 23 mu = 2^49.670 (log2 23 = 4.524).
11. Trail extensions 3 x 2^47 = 2^48.585 (no unsupported 2^48 KeccakTools pad); leaves 169 <= 338 and 897 <= 1355 (6.1).
12. Enumeration 1024 x 2^32 x (2 + 128/1355) = 2^43.067 (Section 6).
13. Total 2^48.585 + 2^49.670 + 2^43.067 + 2^18 = 2^50.237 -> 50.3.
14. Without H8 (Markov only) the cost would be 2^52.42; not claimed (6.3).

## 1. Target and message format

sha3-256-r5-prefix-v1: FIPS 202 SHA3-256, rate 1088, capacity 512, all-zero
IV, rounds 0-4 of Keccak-f[1600] (theta, rho, pi, chi, iota with RC[0..4] =
0000000000000001, 0000000000008082, 800000000000808A, 8000000080008000,
000000000000808B) in every permutation call, padding 0x06 ... 0x80, digest =
lanes 0..3 (256 bits) of the state after the last call. Lane k = x + 5y holds
bits 64k..64k+63; block byte j sits in lane floor(j/8), bits 8(j mod 8)+0..7.

Messages M = M0||X, M0 a uniformly random 136-byte block, X 135 bytes; f5 =
5-round permutation: S0 = f5(M0 || 0^512), A = S0 XOR (X || 0x86 || 0^512),
H(M) = first 256 bits of f5(A). A pair shares M0 and differs in X; the 520
fixed bits of A hold known values S0 XOR (0x86 || 0^512); 1080 bits are free.

Lemma 1 [ours]. Every byte-string message fixes at least 8 bits of its final
padded block. Proof: if the message contributes u bytes to the final block,
0 <= u <= 135 (136 would force another block), and bytes u..135 are padding,
at least one byte. u = 135 gives exactly 0x86 in bits 56..63 of lane 16.
[GLL+20] fix only bits 60..63 of lane 16 (p = 4; 1084 free bits).

## 2. Published facts used [GLL+20]

Notation: L = pi o rho o theta; round i: alpha_{i-1} -L-> beta_{i-1} -chi->
alpha_i; chi acts on 320 rows (y, z), bit x of a row = bit z of lane x + 5y.

| ID | Fact (location in [GLL+20]) |
| --- | --- |
| G1 | Core No. 3 (Table 5, App. D): active S-boxes 59-10-9-0, weights w1-w2-w3-w4d 127-24-19-0; smallest w1 of the d = 256 cores (240, 195, 127); last 3 rounds 2^-36.70 with multiple trails. |
| G2 | Connector (Sec. 4.3, 4.6, Alg. 1-3): beta1 compatible with alpha2 = L^-1(beta2); linear difference system fixes beta0 (zero difference on the c+p fixed bits); linear value system E_M; every solution gives a pair reaching alpha2 with certainty. Attempts can fail; random beta1 picks are repeated; one pick plus one Alg. 1 call is bounded. |
| G3 | Table 6, SHA3-256: Tc = 428.8 single-core hours, DF = 37, weight 36.70, brute force Tb = 45.6 core-hours; exactly one collision found (Sec. 6.2, Table 17). |
| G4 | Eq. (10)/(11): DF = sum DF(1)_i - (c+p) - w1; Sec. 4.5: real DF usually higher (dependencies). |
| G5 | Speed: "around 2^20 ~ 2^22" Keccak per second (Table 6 note); 2^21 Keccak-f/s per core (Sec. 5.4). |
| G6 | Trail search (Sec. 5.2-5.5, App. C.2): KeccakTools TrailCoreInKernelAtC, aMaxWeight 60, over 3000 cores; forward if C1 <= 2^36, backward if C2 <= 2^35, AS(alpha2) <= 110; Req. (2) TDF > w1+w2+w3+w4d, TDF 124 (SHA3-256) / 188 (SHA3-224); Req. (3) w2+w3+w4d <= 55; GPU used in an unstated step; no time given. |
| G7 | Table 6, SHA3-224, same core and connector: Tc = 11.7 h, DF = 83, c + p = 452 (vs 516). |

## 3. Trail core No. 3 and our re-check [ours]

Nonzero lanes (hex, bit z = 2^z). beta2: 0:1 2:4 5:4 6:4 7:4 8:20000
10:2000000000000000 12:200000 15:2000000000000000 18:20000 20:200001 22:200000
24:1. beta3: 0:1 2:1 3:4000000000 7:1 9:40000 11:100 14:40000 20:1 21:100
23:4000000000. Active rows of beta3 as (y, z, input difference): (0,0,05)
(0,38,08) (1,0,04) (1,18,10) (2,8,02) (2,18,10) (4,0,01) (4,8,02) (4,38,08).

Published colliding pair ([GLL+20] Table 17) as padded 17-lane rate blocks,
lanes 0..16 as 64-bit hex (lanes 17..24, the capacity, are zero):

    M1  0-3: FECA67BD2D3F021A BD10A64A4C2B774F F8EF6FF82DD21FC7 6F4BA4D964A78764
        4-7: 0F4FD1C92A24BC6E FB4B8C0A11C64088 EDA7B9EBC05F50A8 0A71DD08E7F1EB5B
       8-11: 5342D2AE78A8BFB5 6591A9B0CC2E7CE9 52A3DD827F4EF6DC 9D89B18362B80DE4
      12-15: FEA719A1875BFFF7 49A2B95AD7B7D147 B23784B72EB9260A 187AEFD07295FD59
         16: EE806366EF9D09FF
    M2  0-3: 16F97050842C2D17 A731EE935A43480A 6D8E356BDBD7CBE9 D62C0B356FFA158A
        4-7: 4FAD968080C7F8C8 7C83B8E1C61BC5AB 7E3FCA22B5E29305 5888D4DBE848C840
       8-11: 236DE21CCEF77B8A 69D59EF589070E60 E87FCD2BF2C6CCE1 B1E28B821FD93ABC
      12-15: AD5D6FB1860CB45C AB8FC7D1015975D5 24C6B737EE96CC23 D3BFB5957965A447
         16: EE31D3F5269F254F

Each block used as the whole initial 1600-bit state, rounds 0-4 (Section 1):

| Check | Result |
| --- | --- |
| Digest lanes 0..3 | equal: 65017C2E8B6040B4 344FF8BB933B4BD6 C6A3F13368BE2003 AB427B4B33435ACB (as printed) |
| L(alpha2) = beta2, L(alpha3) = beta3 | exact |
| Active S-boxes alpha2 / beta2 / beta3 / alpha3 | 59 / 10 / 9 / 10 |
| chi weights rounds 2 / 3 / 4 | 127 (9 x DDT4, 50 x DDT8) / 24 / 19 |
| Round 1 | 318 active (75 x DDT2, 156 x DDT4, 87 x DDT8), 2 inactive |
| alpha0 on top byte of lane 16 | zero (both 0xEE), so beta0 meets p = 8 |
| Branching of beta3 | C1 = 2^19 <= 2^36, C2 = 2^31.70 <= 2^35 |
| Filters | AS(alpha2) 59 <= 110; 127+24+19 = 170 <= 188; 43 <= 55 |

The beta4 the pair actually follows differs from the listed one, consistent
with multi-trail clustering in rounds 4-5 (why H1 sums over all 2^19 alpha4).
The pair (1084-bit messages) is not a solution to this target.

## 4. Algorithm [ours, built on G1, G2, G6]

Parameters: K = 22, B_A = (K+1) mu = 23 mu, mu = 2^45.146 (Section 6),
M = 1024 spaces of 2^32 pairs.

P (preprocessing, trail search; deterministic version of G6).
1. Run TrailCoreInKernelAtC with aMaxWeight 60; list S.
2. For beta3 in S with C1 <= 2^36: depth-first over the active rows, keeping
   beta4 = L(alpha4) incrementally; keep beta3 if some leaf has every plane-0
   row of beta4 zero or in {10,14,15,18,1A,1C,1D,1E,1F} (inputs that can
   output exactly 0x10).
3. For kept beta3 with C2 <= 2^35: depth-first over beta2 compatible with
   alpha3 = L^-1(beta3), keeping alpha2 = L^-1(beta2); compute w2, AS(alpha2),
   w1 = 2 AS(alpha2) + N3 (N3 = rows equal to one of the 11 outputs of minimum
   reverse weight 3).
4. Keep cores with AS(alpha2) <= 110, w1+w2+w3 <= 188 (Req. (2) with the
   SHA3-224 threshold, which [GLL+20] effectively used: No. 3 has 170 > 124),
   w2+w3 <= 55.
5. Select minimum w1, then minimum w2+w3, then lexicographic (beta2, beta3), as
   a running minimum with no connector trials. H6: output is core No. 3.

A (connector attempts, hard budget; counter W_A of all primitives in A1-A3).
1. Fresh uniform M0; S0 = f5(M0||0); fixed-bit values F = S0[1080..1599] XOR
   (0x86 || 0^512).
2. One connector attempt (G2) for alpha2: one fresh beta1 pick, one Alg. 1
   call with fresh coins; variables the 1080 bits of X; zero difference on all
   520 fixed bits.
3. Success iff the systems are consistent and the affine space V of X has
   DF >= 33; output V and the common difference Delta != 0. DF < 33 = failure.
4. On success, if fewer than M spaces were enumerated, run E on (M0, V, Delta);
   on a collision output it and stop.
5. Stop with failure when W_A reaches B_A (abort the running attempt).

E (enumeration). Pick a 32-dimensional subspace W of the direction space D of V
with Delta not in W (if Delta in D, a complement of <Delta> inside a
33-dimensional subspace of D containing it; else any). For X in v + W in
Gray-code order: compute both second-block permutations for X and X XOR Delta,
compare 256 digest bits, output (M0||X, M0||(X XOR Delta)) on equality.

Correctness. Delta != 0, so messages are distinct 271-byte strings; outputs are
checked on true full-sponge 5-round digests, so each is an ordinary collision.

Lemma 2 [ours]. The 2^32 pairs {X, X XOR Delta}, X in v + W, are distinct, and
each reaches alpha2 after two rounds. Proof: equal pairs would give
Delta = X XOR X' in W, contradiction; the second part is G2's defining property
(no closure of V under Delta is needed). Counting 2^32 = 2^(33-1) pairs is the
conservative reading of [GLL+20]'s 2^DF convention.

Independence [ours, exact]: given the core, each attempt uses only its own M0
and coins, so costs, successes and collision events are i.i.d. The charge is
never exceeded: A is cut at B_A, E runs <= M times, P is fixed.

### 4.1 DF, scaling and difference side (evidence for H3, H4, H5)

- Rank fact: with all connector choices fixed, E_M is A x = t over GF(2);
  p = 4 -> 8 adds 4 rows (bits 56..59 of lane 16), so a consistent system loses
  at most 4 dimensions: 37 -> DF >= 33.
- G7 slope: DF 83 -> 37 over 64 more fixed bits = 0.72 per bit; 4 bits ->
  about 34.1. Tc ratio 428.8/11.7 = 36.65 = 2^5.196 over 64 bits = 2^0.0812 per
  bit; 4 bits -> 2^0.325 = 1.25.
- Eq. (10) is not the source of 37: with Table 2 bounds and our round-1
  histogram, sum DF(1) <= 75x1 + 156x2 + 87x3 + 2x5 = 658, so DF <= 658 - 516 -
  127 = 15. The extra >= 22 dimensions come from dependencies (Alg. 3 skips
  implied equations). We rely on the observed 37 and the rank fact.
- Difference slack (318 active S-boxes, 3 equations each, rank-10 inactive
  equations): 1084 - 10 - 954 = 120 at p = 4, 1080 - 10 - 954 = 116 at p = 8.

## 5. Success probability (H1, H2, H3, H4, H8)

Per pair (H1). After alpha2 (certain), a pair must pass round 3 (weight 24) and
reach in rounds 4-5 a beta4 whose active plane-0 rows d output exactly 0x10
(probability DDT[d][0x10]/32 each). Exact Markov sum over all 2^19 alpha4:

    DDT[a][b] = #{v : chi5(v) XOR chi5(v XOR a) = b},
        chi5(v)_i = v_i XOR (NOT v_{i+1} AND v_{i+2}), indices mod 5
    P45 = sum over (b_r) in prod_r {b : DDT[a_r][b] > 0} (9 rows of Section 3) of
          prod_r DDT[a_r][b_r]/32 * prod_{z: v_z != 0} DDT[v_z][0x10]/32,
          v_z = row (0, z) of beta4 = XOR_r L(row (y_r, z_r) = b_r)

Result P45 = 2^-13.219, so p_pair = 2^-37.219, used as 2^-37.22 (published
2^-36.70, not reproduced; we use the lower value). Check: in a 2^36-pair space
this predicts 0.43 collisions (published value 0.62); one was observed.

Per space (H2): s = 1 - exp(-2^32 p_pair) = 1 - exp(-0.02683) = 0.02647.

Theorem [ours, under H4: E[C] <= mu, and H8]. Pr[success] >= 1 - exp(-K s) -
(1-s)^M. Proof. Let S = successes completed within B_A; spaces collide
independently with probability s, and min(S, M) are enumerated, so
Pr[fail] = E[(1-s)^min(S,M)] <= E[(1-s)^S] + (1-s)^M.
- Equal-cost attempts (cost tau, q = tau/E[C]): n = floor(B_A/tau) >=
  (K+1)/q - 1 >= K/q, so E[(1-s)^S] = (1 - qs)^n <= exp(-K s).
- Exponential C: S is Poisson with mean B_A/E[C] >= K+1, so
  E[(1-s)^S] <= exp(-(K+1) s) <= exp(-K s).

K = 22: K s = 0.5824, exp(-0.5824) = 0.5585, (1-s)^1024 = 1.2e-12, so
Pr[success] >= 0.4415, claimed 0.44. H3 acts only through q (H4). Probability
space: the random M0's and connector coins.

## 6. Cost (collision-frontier-v5: 1 unit = one 5-round permutation = 1355 primitives)

| Term | Derivation | log2 units |
| --- | --- | --- |
| Trail extensions | 2^13 cores x (2^36 x 1/4 + 2^35 x 1) = 3 x 2^47 | 48.585 |
| KeccakTools generation | not charged (unpublished; prior 2^48 pad was unsupported — H6 limit) | — |
| T_trail (preprocessing) | extensions only = 3 x 2^47 | 48.585 |
| Tc | 428.8 h = 1,543,680 s | 20.558 (s) |
| f (H4) | 1.25 = G7 SHA3-224/256 slope over 4 extra fixed bits (sample-bias 1.6 moved to sensitivity) | 0.322 |
| R (H7) | 2^22 full Keccak-f/s (G5 upper) x 24/5 | 24.263 |
| First-block overhead | x 1.002 (<= 2 units per attempt vs ~2^14.2 for E_Delta) | 0.003 |
| mu | f Tc R x 1.002 | 45.146 |
| Phase A cap B_A | 23 mu | 49.670 |
| Enumeration | 1024 x 2^32 x (2 + 128/1355) | 43.067 |
| Subspace choice, output, bookkeeping | < 2^18 | 18 |
| Total T | sum | 50.237 -> 50.3 |

### 6.1 Leaf costs of step P (primitives)

- Tree upkeep: XOR one stored 7-word image (L or L^-1 of a row value) per
  child = 21; internal nodes <= leaves; with loop control <= 62 per leaf.
- Forward leaf: 5 plane-0 lanes 10; 9-minterm good mask 9x9+8 = 89; bad mask
  and branch 8; total 62+10+89+8 = 169 <= 338 = 1/4 unit.
- Backward leaf: lane extraction 50, row masks 20, AS popcounts 100, N3
  (11-minterm x 5 planes = 545, popcounts 100) 645, filter/minimum 20; total
  62+50+20+100+645+20 = 897 <= 1355 = 1 unit.
- Step P evaluates no Keccak-f (all linear maps via stored images).

### 6.2 Conversion R (H7 evidence)

R = 2^22 x 24/5 = 2^24.263 units/s: price one core-second of connector
wall-clock at the upper end of [GLL+20]'s quoted Keccak throughput (G5:
"around 2^20 ~ 2^22" full 24-round Keccak-f/s; Sec. 5.4 also 2^21), scaled
to 5-round units. Upper end charges more units per second (conservative for
the attacker's claim). Tc is wall-clock, so this bound covers linear algebra,
memory traffic and retries done in that time. Cross-checks: a speculative
5 GHz x 6 instr/cycle x 2 prim/instr / 1355 model gives 2^25.400 (1.14 bits
higher; would give ~51.4 with f = 1.25; not used); Tb at 2^38 permutations / 164,160 s = 2^20.68 units/s
(far below R). Connector work is GF(2) elimination on <= 1601-bit rows.

### 6.3 Sensitivity and fallback (same arithmetic; success kept >= 0.39)

| Change | time_log2 |
| --- | --- |
| f = 1 / 2 / 4 / 8 / 16 (H4; claimed f = 1.25) | 50.03 / 50.73 / 51.55 / 52.45 / 53.40 |
| R x2 / x4 / microarch 2^25.400 (H7) | 50.98 / 51.83 / 51.09 |
| T_trail +2^48 pad / 2^50 / 2^51 (H6) | 50.51 / 50.85 / 51.49 |
| p_pair 2^-37.5 (K = 23, P = 0.395) / 2^-38 (K = 32, P = 0.391) (H1) | 50.28 / 50.61 |
| DF = 32 (K = 44) / 31 (K = 88) (H3) | 50.96 / 51.79 | 51.13 / 51.89 |

K = 22 keeps P >= 0.39 for p_pair down to 2^-37.46. Fallback without H8 (Markov
only, not claimed): N = 50 spaces, abort at c N mu, c = 2.87; Pr >= 1 - 1/c -
(1-s)^50 = 0.390; T = 2^48.585 + 143.5 x 2^45.146 + 50 x 2^33.067 = 2^52.42

## 7. Memory

E_Delta, E_M (<= 1600 x 1601 bits each, ~320 KB total); E: 64 basis vectors;
P: row images < 40 KB, 11-level tree; assumed 2^34-byte KeccakTools allowance;
code < 2^24 bytes. Peak <= 2^34 bytes.

## 8. Declared heuristics (mirrored in claim.json)

- H1 (score-critical). Pairs from a successful p = 8 connector collide with
  probability >= 2^-37.22 (Markov, rounds 3-5). Evidence: our 2^19-term sum
  (Section 5), re-check (Section 3), published 2^-36.70 and one collision in
  2^36 pairs (G1, G3). Limits: no p = 8 experiment; round dependence.
- H2 (score-critical). Collision count in a 2^32-pair space is close to
  Poisson, s = 0.02647. Evidence: Section 5; independence across spaces is
  exact (Section 4). Limits: clustering would lower s; no clustering data.
- H3 (score-critical). Successful p = 8 attempts give DF >= 33. Evidence: rank
  fact on DF = 37; slope 0.72/bit predicts ~34 (4.1). Limits: one DF value per
  target; Eq. (10) gives only <= 15; a shortfall lowers q (absorbed by H4).
- H4 (score-critical). Expected work E[C] for one successful p = 8 attempt
  from fresh random first blocks, failures included, is <= f Tc, f = 1.25
  (536.0 core-hours), i.e. <= mu = 2^45.146 units with H7. Evidence: G3, G7
  slope 0.72 bit / ~2^0.0812 per bit over 4 bits -> 1.25; slack 116 (4.1).
  Limits: one run; two-point fit; never run at p = 8; sample-bias factor 1.6
  (median-unbiased 1/ln 2) is NOT folded into the claim — see sensitivity
  f = 2 -> 50.93; 90% one-sided from one exponential sample would need ~9.5.
- H5 (supporting). The difference system can still keep zero difference on the
  8 padding bits. Evidence: slack 120 -> 116; published beta0 already zero
  there (Section 3). Limits: counting argument only.
- H6 (score-critical). Step P's priced tree extensions cost <= 2^48.585 and
  output core No. 3. Evidence: leaf costs (6.1); No. 3 passes every filter
  (Section 3), smallest w1 of the d = 256 cores in Table 5. Limits: <= 2^13
  starting cores assumed; KeccakTools core-generation time is unpublished and
  is NOT charged (a prior 2^48 pad was unsupported fabrication — sensitivity
  restores it -> ~50.51); GPU used in an unstated published step; a core with
  smaller w1 might be selected (figures are for No. 3).
- H7 (score-critical). One core-second of the published connector is <= about
  2^24.263 units (G5 upper end x 24/5; estimate, not a proof). Evidence: 6.2.
  Limits: connector is linear algebra, not Keccak; throughput range is a quote.
- H8 (score-critical). Work per success C is a geometric number of i.i.d.
  attempt costs with tail no heavier than the equal-cost or exponential case.
  Evidence: G2 retry structure; i.i.d. attempts (Section 4). Limits: no
  attempt timings published; rare very long attempts would lower success;
  without H8 only the 2^52.42 fallback holds.

## 9. Not claimed

No pair, certificate or experiment; our checks (Sections 3-5) are offline, not
organizer-executed. No novelty beyond the p = 8 adaptation and its accounting.
baseline_improved is the required nominal reference ID, not a dominance claim.
