# sha3-256-r5: replay of a collision built by our own executed, committed construction

## 1. Claim

Track `sha3-256-r5-exploratory`, target `sha3-256-r5-prefix-v1`: ordinary collision of SHA3-256 with
Keccak-f[1600] rounds 0..4 on the single absorbed block, zero IV, rate 1088, capacity 512, suffix
0x06 with pad10*1, full 256-bit digest. Cost model `collision-frontier-v5` with C = 1355 (one 5-round
permutation = 1 unit, any other 256-bit word operation = 1/1355 unit). Review policy
`paired-lanes-v1`, exploratory lane.

The scored program (Section 3) replays one stored pair of distinct 135-byte messages that collide
under 5-round SHA3-256. It uses no coins, so its success probability is 1. The charged time is the
executed work of the one committed run of construction chain C that produced the pair, plus the
replay; it is not an expected or extrapolated cost.

We built the stored pair with construction chain C (Sections 5-7). Its only external input is the
published trail core No. 3 of Guo, Liao, Liu, Liu, Qiao and Song (GLL+20; J. Cryptology 33, 2020;
ePrint 2019/147, Table 9), which is a differential characteristic: two difference patterns
(beta2, beta3). It is not a collision and contains no message, state value, connector or
message pair. C does not read any published or third-party pair, connector, subspace or
difference beta0/beta1/alpha1. C works as follows:
- it computes the linear layer, its inverse and the chi tables itself;
- it enumerates and orders the 800,000 round-1 input differences beta1 itself, and filters them;
- it solves one joint CryptoMiniSat instance for a byte-padded witness pair that follows rounds 0
  and 1 (Section 5.4), from a seed committed in advance;
- it builds the affine connector space around that witness by linear algebra (Section 5.5);
- it enumerates that space with our C program until the first collision (Section 6).

Every computation of C is charged (Section 9). Our own C program is charged with explicit
operation counts per event. The Python and CryptoMiniSat process and the compiler are charged from
measured retired instructions at 256 word operations per instruction. The complete source is in
Appendix B and the commitments, written before the runs, are in Appendix A.

| field | value | where |
|---|---|---|
| time_log2 | 37.55 | executed work of C plus replay, 2^37.5491, Section 9 |
| preprocessing_log2 | 37.55 | construction chain C, Section 9 |
| success_probability | 1 | deterministic replay, Section 3 |
| nonuniform_advice_log2_bytes | 11 | the stored 270-byte pair plus the 850-byte trail text, Section 10 |
| memory_log2_bytes | 28 | measured peak over C, Section 10 |

Our own contributions over the source attack are the joint witness SAT instance with byte padding
and the witness-anchored linearisation (Section 5), which make the 2-round connector consistent by
construction for 8 fixed padding bits; with them a connector costs one SAT call instead of a search
over many failed attempts. The SAT instance also bounds the number of DDT-2 rows in round 0, which
raised the connector dimension from about 35 to about 60 in our development runs.

Heuristics are declared in Section 11: H1-public-trail, H2-op-accounting, H3-instruction-conversion
and H4-chain-scope are score-critical; H5-memory is supporting. No probability estimate enters the
bound: the charged work is the executed work.

## 2. Target, written out

State: 25 lanes A[x,y] of 64 bits, lane index x+5y; state bit 64(x+5y)+z is bit z of lane A[x,y];
lanes are read little-endian from the block. A row is (y,z) with row index r = 64y+z; its five bits
are x = 0..4. Round i (i = 0..4):

    theta: C[x] = XOR_y A[x,y];  D[x] = C[x-1] ^ ROT(C[x+1], 1);  A[x,y] ^= D[x]
    rho,pi: B[y, 2x+3y] = ROT(A[x,y], r[x,y])
    chi:   A[x,y] = B[x,y] ^ (~B[x+1,y] & B[x+2,y])
    iota:  A[0,0] ^= RC[i],  RC[0..4] = 1, 8082, 800000000000808a, 8000000080008000, 808b

with the standard rho offsets. A 135-byte message M is padded to the one rate block M || 0x86
(suffix 0x06 and the final 0x80 share byte 135), followed by 64 zero capacity bytes. So state bits
1080..1087 equal 0x86 (bits 1081, 1082, 1087 are 1) and bits 1088..1599 are 0 for every message:
520 fixed bits. One permutation is applied and the digest is lanes A[0,0..3,0] (256 bits). This is
`verifier/keccak.py:sha3_256(M, rounds=5)`; our implementation was checked against it on random
135-byte messages, and every output pair is re-checked with it.

Write L = pi o rho o theta (linear, invertible) and x = L(s) for the absorbed state s. Then round 0
is chi(x) ^ RC[0], and later rounds are chi(L(.)) ^ RC[i]. For a pair, alpha_i is the difference
entering round i, beta_i = L(alpha_i) the difference entering chi of round i.

## 3. The scored program (replay)

R1. Read the stored advice: two 135-byte strings P and P' (Section 4).
R2. Compute sha3-256-r5(P) and sha3-256-r5(P'): one permutation each.
R3. If P != P' and the digests are equal, output (P, P'). Otherwise output nothing.

The organizer verifier confirms the relation for these bytes (certificate `r5-exec-1`). R uses no
coins, so the success probability is 1. Cost: 2 permutations plus padding, absorption and one
256-bit compare, at most 300 word operations: 2.23 units.

## 4. The stored pair

    P  = 7d797fd42c855b48390d36fff44171bf3d66d05c6bae7b451f6fbf669945437542823604405bb5f8c5d4a0475605d7c2bfd9d85af0181a6ad15f6da7a14b7e6335e8f2bdcb1e3b5f59340cbc18115b1bfbaea3a2385e32cc502dbd11a2150bf1dbb28623234a0a67413c9a650256d1b85b27baab0174a0efab7fdb6aea9edfb2d865fa13f4a65f
    P' = 7ade819a165672852d9dbe62d98d11f570e4b55038d7e9743d6a9f854503d9eb48172199a058a44c6ed7c99229546262992df64463e7a2d7a3ac5461047c1cf22046f15c9bf8debd1b90da85d64a1257062500662387d4401bcf7234a9b95f69d2331116cd25c3497b0743adce0a275237571e7c849ee7b08c8014db56bbc799c9c06202a2b251
    sha3-256-r5(P) = sha3-256-r5(P') = 56ef19cf743229a41c1b23484d5adf5a4c33ddf18c979b55e9f6c595ccd79ac6

P and P' are the two messages of index 73686378480 of phase D (Section 6), that is, the first 135
bytes of L^-1(x) and L^-1(x ^ beta0) for the point x of the connector space at that Gray-code
index. Their XOR is alpha0 = L^-1(beta0) restricted to bytes 0..134; beta0 is stored in the
experiment program (`BETA0`).

## 5. Construction chain C, phase B (Python and CryptoMiniSat, `r5chain.py`)

### 5.1 Trail core No. 3 and the facts used

Appendix B.6 is the trail text as printed in GLL+20 Table 9 (beta2 and beta3, rows y = 0..4, lanes
x = 0..4, most significant hex digit first). C derives alpha3 = L^-1(beta3) and alpha2 =
L^-1(beta2) and checks: alpha3 lies in the CP-kernel (10 bits), and every active row of beta2 has a
DDT-compatible output in alpha3 with total weight 24 (phase P assertions). alpha2 has 114 bits in
59 active rows.

Lemma 1 (affine solution sets). For the 5-bit chi map S and d != 0, the set
V(d,o) = {v : S(v) ^ S(v ^ d) = o} is empty or an affine subspace of GF(2)^5 with
DDT[d][o] points (S is quadratic, so v -> S(v) ^ S(v ^ d) is affine). Hence a row transition
d -> o holds for value v exactly when v satisfies 5 - log2 DDT[d][o] affine equations. We checked
all 31 x 32 cases exhaustively; we also checked that S is affine on every V(d,o) with DDT 2 or 4.

Round-2 conditions (beta2 -> alpha3, used by phase D Stage 1), rows r = 64y+z:

| r | (y,z) | d | o | DDT |
|---|---|---|---|---|
| 0 | (0,0) | 1 | 1 | 8 |
| 2 | (0,2) | 4 | 4 | 8 |
| 66 | (1,2) | 7 | 4 | 2 |
| 81 | (1,17) | 8 | 8 | 8 |
| 149 | (2,21) | 4 | 4 | 8 |
| 189 | (2,61) | 1 | 1 | 8 |
| 209 | (3,17) | 8 | 8 | 8 |
| 253 | (3,61) | 1 | 1 | 8 |
| 256 | (4,0) | 17 | 1 | 4 |
| 277 | (4,21) | 5 | 4 | 4 |

### 5.2 Phase P and B1: tables and the beta1 order

C computes the 1600 rows of L (11 bits each) and of L^-1 (by Gauss-Jordan elimination), the chi
DDT, the sets V(d,o), and all 2,451 affine subspaces of GF(2)^5 with their defining equations and,
for each chi output bit, its affine form on the subspace if one exists.

beta1 is the round-1 chi input difference. For each of the 59 active rows of alpha2, C takes every
input difference of maximal DDT to that row's output (weight w1 = 127 in total). 50 rows have one
choice, 5 rows five and 4 rows four: 800,000 candidates. For each, alpha1 = L^-1(beta1). C sorts the
candidates by (number of active rows of alpha1, choice tuple). The minimum is 242 active rows.

### 5.3 Phase B2: linear prefilter

Necessary condition for a byte-aligned beta0: alpha0 = L^-1(beta0) must vanish on the 520 fixed
bits, beta0 must vanish on every inactive row of alpha1, and every active row r must still allow
an input difference d with DDT[d][alpha1|r] > 0. C builds the linear system of the first two
conditions in reduced row echelon form, projects its solution set onto each active row (an affine
set of 5-bit values), and tests the third. Candidates are tested in the B1 order; the first one that
passes goes to B3.

### 5.4 Phase B3: joint witness SAT (rounds 0 and 1, byte padding)

One CryptoMiniSat instance (pycryptosat 5.16.0, threads = 1, conflict limit 3,000,000) with:
- message bits s_0..s_1079 and difference bits alpha0_0..alpha0_1079 (the 520 fixed bits are
  constants: the padding values for s, zero for alpha0);
- x = L(s) and beta0 = L(alpha0) as 3,200 XOR clauses;
- round 0 for message 1: t_j = (NOT x_{j+1}) AND x_{j+2} within the row (chi(x)_j = x_j ^ t_j);
- for every inactive row of alpha1: beta0 = 0 on the row;
- for every active row: forbidden incompatible beta0 values, x' = x ^ beta0, the gates
  u_j = (NOT x'_{j+1}) AND x'_{j+2}, and the XOR clause beta0_j ^ t_j ^ u_j = alpha1_j, which says
  chi(x) ^ chi(x') = alpha1 on the row;
- E_1: for every active row r of beta1, the 5 - log2 DDT affine equations of V(beta1|r, alpha2|r) on
  y = L(chi(x) ^ RC[0]), written as XOR clauses over the chi(x) bits (127 equations);
- an indicator per active row that is forced true when the row uses a DDT-2 transition, and a
  sequential counter (Sinz 2005) bounding their number by 90;
- 8 random XOR constraints, each over 16 message bits drawn from the attempt's seeded generator,
  so that different attempts return different witnesses.

A solution is a 135-byte message pair (s, s ^ alpha0) whose round-0 output difference is alpha1
and whose round-1 chi input satisfies E_1, so its round-1 output difference is alpha2 (Lemma 1).

### 5.5 Phase B3/B4: the witness-anchored affine space

Variables: x (1600 bits). Equations, added in this order to a GF(2) system kept in reduced row
echelon form:
- E_pad: (L^-1 x)_j = c_j for the 520 fixed bits j = 1080..1599;
- E_0: for every active row r of beta0, x|r in V(beta0|r, alpha1|r) (w0 equations in total);
- linearisation: for every round-0 row r whose chi outputs occur in E_1 (in a seeded random order),
  let P_r be the projection of the current solution set onto the row. C chooses, uniformly with the
  attempt's seeded generator, an affine subspace W_r of maximal dimension with
  (i) W_r contains the witness value x*|r, (ii) W_r is contained in P_r, (iii) every chi output bit
  of the row that occurs in E_1 is an affine function on W_r; and adds the equations of W_r;
- E_1 linearised: each E_1 equation, with every chi output bit replaced by its affine form on W_r.

Lemma 2 (consistency). The witness x* = L(s*) satisfies every equation, so the system is consistent.
Proof: E_pad holds because s* is a padded block; E_0 because the witness pair has round-0 output
difference alpha1 (Lemma 1); the linearisation equations by (i); the linearised E_1 because on
W_r the affine forms equal the chi bits, x*|r lies in W_r, and x* satisfies E_1.

Lemma 3 (connector). For every solution x, the messages M = first 135 bytes of L^-1(x) and
M' = first 135 bytes of L^-1(x ^ beta0) are distinct 135-byte messages whose padded blocks are
L^-1(x) and L^-1(x ^ beta0), and the pair has state difference exactly alpha2 after rounds 0 and 1.
Proof: E_pad fixes the 520 bits of L^-1(x); alpha0 vanishes on them, so L^-1(x ^ beta0) has them
too; alpha0 != 0. E_0 and Lemma 1 give round-0 output difference alpha1, hence round-1 chi input
difference beta1. On the solution set every chi output bit used by E_1 equals its affine form
(each x|r lies in W_r), so E_1 holds for y = L(chi(x) ^ RC[0]); Lemma 1 gives output difference
alpha2.

The space is accepted when DF = 1600 - rank >= 42 (else the next attempt, up to 8; then the next
beta1 candidate). B4 writes x0 and a basis. If beta0 lies in the linear part, C drops one basis
vector whose free coordinate of beta0 is 1, so that each unordered pair {x, x ^ beta0} occurs once;
it keeps the first 48 remaining vectors. B4 also checks 16 seeded points of the space against
Lemma 3 by direct computation.

## 6. Construction chain C, phase D (our C program, `r5search.c`)

Index i in [0, 2^41) enumerates x_i = x0 ^ XOR_k gray(i)_k b_k, gray(i) = i ^ (i >> 1); the step
from i-1 to i XORs basis vector b_{ctz(i)}. The pair is {x_i, x_i ^ beta0}.

- Stage 1 (message 1 only): chi and iota of round 0 from x_i, round 1, theta-rho-pi of round 2;
  then the 10 round-2 rows of Section 5.1, most selective first (the DDT-2 row), each tested with
  its 32-bit membership mask, stopping at the first failure. By Lemma 3 and Lemma 1 a pass means
  the pair has difference alpha3 after round 2.
- Stage 2 (passes only): the remaining rounds for x_i and x_i ^ beta0 from their round-0 chi
  inputs; compare digest lanes 0..3.
- Threads: 10 threads take chunks of 2^24 consecutive indices from an atomic counter in increasing
  order. A thread starting a chunk computes x_lo directly from gray(lo). A collision sets a global
  stop flag; every thread checks it every 4,096 pairs and returns. Every thread counts its pairs,
  Stage-1 passes and per-row checks exactly; the program prints the sums.
- Output: the reported pair (index, x). Python converts it to the two messages with L^-1 and checks
  them with the organizer verifier.

## 7. Execution record

Commitments (Appendix A) were written and committed to a local git repository at
2026-10-07T14:17:49+09:00 (commit 6042a29cc641), before any run of C. The seed is the first 64 bits of
SHA-256 of the committed label, seed64 = a34682764a9fb0d2; it was not chosen.

Phase B (one process, `/usr/bin/time -l`, Appendix C):

```
0.2 P trail ok: alpha2 rows 59 seed64 a34682764a9fb0d2
3.7 B1 candidates 800000 min active 242
7.5 B2 candidate 140 active rows 264 passes the prefilter after 141 tests
13.1 B3 attempt 0 w0 847 rank0 1324 lin 93 rank1 1417 E1 inconsistent 0 DF 58
13.2 B4 exported DF 58 basis 48 beta0 in lin True alpha2 check 16 /16
```

The accepted space: beta1 candidate 140 (264 active rows of alpha1), witness attempt 0,
w0 = 847, rank(E_pad + E_0) = 1324, rank after linearisation 1417 (93 added
equations), final rank 1542, DF = 58; 16 of 16 seeded points satisfy Lemma 3.

Phase D (10 threads under our machine's resource guard, `/usr/bin/time -l`, Appendix C):

```
COLLISION idx 73686378480
pairs 73615736832 pass 4373 coll 1
rowpass 4600944330 575135585 71888865 17966163 4491052 1122867 280289 70088 17406 4373
best_idx 73686378480
best_x 006a6fd088acd020 8b3391c64078bb10 02c017033dd687cc 6b7fe75536eb327a e300026650ae9e9a 29985c6a82cd096c d18b59576e361309 201da627f3803d34 41ebde043731ff05 30edbe1e7b40dd5b 921ebd1e29cccf7f 04eed49f5aed4239 b335412bedc2850a 6b8c00099942ba7a abf1734ea57520c7 006d7e07c416f6ba b737d988ae6efaa1 d42b67e9b51f5a1d f879ed03756cc3b6 b75993d35bff3aa9 308597a621b5a339 c1035466c8216420 11b2f0cae5fc00d1 11adedf5dce82c6c d9f87defaf41aa19
```

So phase D evaluated N = 73615736832 = 2^36.099 pairs over all threads, with 4373
Stage-1 passes and 1 collision(s), in 177.54 s of wall time. The output pair is index
73686378480. That index is larger than N because ten threads work on consecutive chunks at once:
the collision lay in a chunk taken while other threads were still on earlier chunks, and the stop
flag ended every thread within 4,096 pairs. Not every index below it was evaluated; the charge is
the evaluated count N, which the threads count exactly.

Stage-1 pass rate: 4373 / N = 2^-24.005 (model 2^-24.000). The per-row check counts are
in the second line above.

## 8. Why the output collides

Lemma 3 gives difference alpha2 after rounds 0-1 for every enumerated pair, Stage 1 certifies
alpha3 after round 2, and Stage 2 compares the two complete 5-round digests computed from the
round-0 chi inputs. The final pair was re-hashed from its bytes with `verifier/keccak.py`
(Section 4) and is the organizer-verified certificate.

## 9. Cost ledger (units of one 5-round permutation)

| line | count | units |
|---|---|---|
| phase B: retired instructions x 256 / 1355 (H3) | 284576788169 instr | 5.38707e+10 |
| compilation of r5search.c x 256 / 1355 (H3) | 558963823 instr | 1.05605e+08 |
| phase D: enumerated pairs x 2 (H2) | 73615736832 pairs | 1.47231e+11 |
| phase D: Stage-1 passes x 10 | 4373 | 43730 |
| phase D: chunk set-ups x 8 | <= 4398 | 35184 |
| output conversion and check | 1 | 1000 |
| scored replay (Section 3) | 1 | 2.23 |
| **total** | | **2.01102e+11 = 2^37.5491** |

All counts are executed counts, not expectations, and include every failure, every prefilter test
and every thread's work. Phase D is charged per event (H2):
- per enumerated pair: 2 units = 2,710 word operations. Stage 1 has at most 590 data-path
  operations per pair in the organizer's counting convention (Gray step: index test, ctz and
  basis address 10 and XOR 25; round-0 chi and iota 101; round 1 271; round-2 theta-rho-pi 170;
  loop control, counters and the stop-flag test 13) plus 22 per row checked (bit extraction 18,
  mask test and branch 3, counter 1). We charge every data-path operation two operand loads and one
  result store, so a pair costs at most 4 (590 + 22 rbar) word operations, where rbar is the
  executed mean number of rows checked: rbar = 1.0716, giving 2454 < 2,710;
- per Stage-1 pass: 10 units (two digests of 1,185 data-path operations each, times 4, plus the
  25-lane XOR and compare: 9,600 operations = 7.1 units);
- per chunk: 8 units (x_lo from up to 48 basis vectors: at most 1,300 data-path operations,
  times 4); chunks <= N / 2^24 + 11.
- output: two applications of L^-1 as dense 1600 x 1600 GF(2) matrix-vector products (under
  400,000 word operations with memory traffic) and the verifier check: charged 1,000 units.

Cross-check: phase D retired 34526936856517 AArch64 instructions in total (Appendix C.3), that is
469 per pair including every load, store, branch and loop overhead of all threads. This is
below our count of 590 data-path operations per pair, and the 2-unit charge per pair corresponds
to 5.78 word operations per retired instruction of phase D.

Phase B and compilation are charged at 256 word operations per retired AArch64 instruction (H3).

## 10. Memory and advice

Measured peak resident set size: phase B 224526336 bytes, phase D 2015232 bytes. Both are below
2^28 bytes, which we claim. Advice: the stored pair (270 bytes) and the trail text (850 bytes), so
2^11 bytes.

## 11. Heuristics

- H1-public-trail (score-critical). Trail core No. 3 (Appendix B.6, GLL+20 Table 9) is public
  algorithm text that C reads without charging its original search. It is a difference pattern, not
  a collision, and holds no message, state value, connector or pair. Evidence: the cost model text on
  advice, and the passing r31 and a7fb31c0 packages that used the same convention for a published
  characteristic. Limitation: if a reviewer requires the trail search to be charged, the bound rises
  by that search's cost. Two public packages report executing such a search for this core; we have
  not run one and do not use their numbers as evidence.
- H2-op-accounting (score-critical). For our C program the per-event charges of Section 9 bound the
  primitive word operations, including memory traffic. Evidence: the operation counts follow the
  organizer's reference convention (`scripts/reference_operation_costs.py`: 271 per round, rotation
  as two shifts, OR and mask), Appendix B.4 and B.5 are the complete program, and the per-row check
  counts are executed counts. Limitation: the count is by inspection of the source, not by an
  instrumented RAM simulator; the factor 4 for memory traffic is our convention.
- H3-instruction-conversion (score-critical). For phase B (Python 3.12 with CryptoMiniSat) and
  the compiler, 256 primitive 256-bit word operations per retired AArch64 instruction bound the
  work. Evidence: every AArch64 integer, load/store and branch instruction acts on at most 128 bits
  of data and is emulated by a small constant number of 256-bit word operations; SIMD instructions
  act on at most 128 bits. Limitation: not verified by an instrumented emulation; the instruction
  counts come from the macOS kernel counters reported by `/usr/bin/time -l` on Apple M4 Pro.
- H4-chain-scope (score-critical). C covers all computation from the tables to the stored pair:
  every prefilter test, every SAT attempt, every thread's pairs, the conversion and the check.
  Development runs (Section 12) used other labels and seeds; C does not read any of their outputs
  and recomputes everything from the trail text and its committed seed.
- H5-memory (supporting). Peak memory over C is below 2^28 bytes (Section 10).

## 12. Development work (disclosed, not part of C)

Before writing the commitment we developed and tuned the code on the same target with other seeds.
The tuning fixed the prefilter, the DDT-2 bound 90, the hash constraints and the acceptance
threshold DF >= 42. These runs found the same first prefilter-passing candidate (index 140, which C
recomputes and charges), produced connector spaces with DF between 9 and 66, and ran phase D on a
development space for 2^28 + 2^25 pairs to test the program (17 Stage-1 passes, no collision). No
development run produced a collision. Their outputs are not inputs of C. Their total work was
about 7e12 retired instructions (measured for the two complete development chain runs, 3.37e12,
and estimated from CPU time for the shorter tests), almost all in early versions that called a
difference-only SAT for every candidate and used no DDT-2 bound.

## 13. Evidence and its status

- Organizer experiment `r5-connector-replay` (`experiments/r5_connector_replay.py`, stdlib only,
  deterministic, about 3 s for 256 trials). Once per run it rebuilds the accepted space from the
  stored witness, beta0, beta1 and alpha1 with the committed linearisation seed (ranks
  1324 -> 1417 -> 1542, DF 58) and derives the certificate pair from the stored
  Gray-code index. Each trial draws a fresh point of the space from its organizer seed and reports
  (as untrusted observations) whether both messages have the fixed padding and the pair has the
  exact 2-round difference alpha2; every trial returns the certificate pair, which the organizer
  checks as a full collision. Locally 256 of 256 fresh points satisfied Lemma 3. The experiment
  supports correctness of the connector and the certificate; it makes no cost or probability claim.
- Supporting only, not used in the bound: under the Markov model the per-pair success probability is
  2^-24 (round 2) times 2^-13.2186 (rounds 3-4, exact sum over all 524,288 alpha4 compatible with
  beta3; 192 nonzero terms, best single 2^-19), that is 2^-37.2186, so a run needs about 2^37.2
  pairs on average. GLL+20 give 2^-36.70 for this core. Our run needed 2^36.099 pairs.
  Under this model a fresh run needs at most that many pairs with probability
  1 - exp(-N p) = 0.369, so the executed count is below the model median; Section 15 discusses this. For comparison only, a
  prospective variant with a hard cap of N_cap pairs succeeds with probability 1 - exp(-N_cap p)
  under the model: N_cap = 2^36.20 gives 0.39 and 2^37.22 gives 0.63, that is 2^37.2 and 2^38.2
  units for phase D. We do not claim these: they rest on the model and on the connector succeeding
  for a fresh seed.

## 14. Credit

- Framework, trail core No. 3, the 2-round connector with non-full linearisation, the use of
  affine DDT solution sets: Guo, Liao, Liu, Liu, Qiao, Song (GLL+20), building on Dinur, Dunkelman
  and Shamir (FSE 2012), Qiao, Song, Liu, Guo (EUROCRYPT 2017) and Song, Liao, Guo (CRYPTO 2017).
- SAT for connector phases: Guo, Liu, Song, Tu (ASIACRYPT 2022) and Tu, Song, Wu, Guo, Weng, Xing
  (ePrint 2026/2107). Solver: CryptoMiniSat (Soos). Cardinality encoding: Sinz (CP 2005).
- Public byte-aligned packages on this track by Th0rgal and newjordan showed that the 0x86 byte
  domain works with this core and used a Stage-1 early-abort filter on the round-2 rows; tekkac's
  packages and their reviews showed that a seed selected after a run must be charged. We read them
  for structure and lessons; no text, code, number, difference or pair of theirs is used.
- Ours: the joint witness SAT with byte padding and the DDT-2 bound, the witness-anchored
  linearisation, the linear prefilter and order, the search program, the executed chain, the
  experiment, the ledger and this text.

## 15. Risks

- H1: if the trail search must be charged, the bound rises by that search's cost.
- H3: the factor 256 is a convention; phase B is 26.8% of the total, so even a factor 1024
  would add 0.85 bits.
- H4: development runs are disclosed but not charged; Section 12 gives their size.
- Single run: the charged work is that of the one committed run of C that produced the stored pair.
  No run of C was discarded or repeated (Appendix A), so no selection over runs entered the cost.
  It is not an estimate for a fresh run. Under the model of Section 13 a fresh run needs at most our
  N pairs with probability 0.369; at the model median (2^36.69 pairs) a fresh run would cost
  2^38.00 units and at the 90th percentile (2^38.42 pairs) 2^39.52 units.

## Appendix A. Commitments (written before the runs)

A.1 `c-commit.txt` (git commit 6042a29cc641, 2026-10-07T14:17:49+09:00):

```
yukon hashsmash sha3-256-r5 exec construction C 2026-10-07
a34682764a9fb0d2389276b831008023fe5c2431a31eafbc0a26f973673f843b
seed64 a34682764a9fb0d2
e042140cf7708a05d926c6f527ca2bdc7359a20857fb9570afed4650c8f4e17b  trail_core3.txt
96ef1a35c4b1827a243ce7b3a6fd31029d1b0198d1d9a02d66e43a87f4229ba3  r5core.py
076313ece15b7979a8499c45c332390dc4144ced7cecb2f94f169aade9954212  r5conn.py
a31ec1520421d85952c50b74b20bfdd2b3374196fd3f636ee594a7030bd451f9  r5chain.py
555c46975b3c2ade6e8c76c1167e6f3b40ad409d893112b1d6e2fe956ddb645f  r5search.c
257c736f4c06fe79feb798a98dec2da81bf89afb4111218ce6677eab978282e2  keccak_unrolled.h
e6c809e4685aca98513f76542e84ee8225978581b36b23e1a87afb29c564d349  r5search
toolchain: Python 3.12.2, pycryptosat 5.16.0 (CryptoMiniSat, threads=1), Apple clang 21.0.0 -O3 -mcpu=apple-m4, macOS on Apple M4 Pro
phase B: nice -n 10 /usr/bin/time -l python3 r5chain.py "yukon hashsmash sha3-256-r5 exec construction C 2026-10-07" run1   (stopping rules in the r5chain.py docstring)
phase D: nice -n 10 /usr/bin/time -l ./r5search run1/space.txt 0 0x20000000000 10 24 1   (10 threads, chunks of 2^24 indices dispensed in increasing order, all evaluated pairs counted, stop flag at the first collision, hard cap 2^41 pairs)
fallback: if phase D ends without a collision, phase B is rerun with label + ' fallback 1' and phase D repeated; every run is charged
output: the first collision reported by phase D (best_idx); messages = first 135 bytes of L^-1(x) and L^-1(x ^ beta0)
committed 2026-10-07T14:17:43+0900
```

## Appendix B. Source

B.1 `r5core.py` (SHA-256 96ef1a35c4b1827a243ce7b3a6fd31029d1b0198d1d9a02d66e43a87f4229ba3)

```python
"""Keccak-f[1600] pieces, GF(2) tools and the trail-core-3 constants for the r5 connector.

State convention: a 1600-bit Python int, bit 64*(x+5*y)+z is bit z of lane A[x,y]
(the verifier's little-endian lane order). Row r = 64*y + z holds bits x = 0..4.
"""
import os

RC = (0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
      0x8000000080008000, 0x000000000000808B)
RHO = (0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39,
       41, 45, 15, 21, 8, 18, 2, 61, 56, 14)
M64 = (1 << 64) - 1
NB = 1600
HERE = os.path.dirname(os.path.abspath(__file__))


def rot(v, n):
    n %= 64
    return ((v << n) | (v >> (64 - n))) & M64 if n else v


def to_lanes(s):
    return [(s >> (64 * i)) & M64 for i in range(25)]


def from_lanes(a):
    s = 0
    for i in range(25):
        s |= a[i] << (64 * i)
    return s


def theta_l(a):
    c = [a[x] ^ a[x + 5] ^ a[x + 10] ^ a[x + 15] ^ a[x + 20] for x in range(5)]
    d = [c[(x - 1) % 5] ^ rot(c[(x + 1) % 5], 1) for x in range(5)]
    return [a[i] ^ d[i % 5] for i in range(25)]


def rhopi_l(a):
    b = [0] * 25
    for y in range(5):
        for x in range(5):
            b[y + 5 * ((2 * x + 3 * y) % 5)] = rot(a[x + 5 * y], RHO[x + 5 * y])
    return b


def chi_l(b):
    return [b[i] ^ ((~b[(i % 5 + 1) % 5 + 5 * (i // 5)]) & b[(i % 5 + 2) % 5 + 5 * (i // 5)]) & M64
            for i in range(25)]


def L(s):
    return from_lanes(rhopi_l(theta_l(to_lanes(s))))


def chi(s):
    return from_lanes(chi_l(to_lanes(s)))


def rounds_from_chi_input(x, first_round, last_round):
    """x is the chi input of round first_round; returns the state after round last_round."""
    a = chi_l(to_lanes(x))
    a[0] ^= RC[first_round]
    for i in range(first_round + 1, last_round + 1):
        a = chi_l(rhopi_l(theta_l(a)))
        a[0] ^= RC[i]
    return from_lanes(a)


def perm5(s):
    a = to_lanes(s)
    for i in range(5):
        a = chi_l(rhopi_l(theta_l(a)))
        a[0] ^= RC[i]
    return from_lanes(a)


def bit(x, y, z):
    return 64 * (x + 5 * y) + z


def row_val(s, r):
    y, z = divmod(r, 64)
    v = 0
    for x in range(5):
        v |= ((s >> bit(x, y, z)) & 1) << x
    return v


def row_bits(r):
    y, z = divmod(r, 64)
    return [bit(x, y, z) for x in range(5)]


def chi5(v):
    o = 0
    for i in range(5):
        b = ((v >> i) & 1) ^ ((((v >> ((i + 1) % 5)) & 1) ^ 1) & ((v >> ((i + 2) % 5)) & 1))
        o |= b << i
    return o


CHI5 = [chi5(v) for v in range(32)]
DDT = [[0] * 32 for _ in range(32)]
VMASK = [[0] * 32 for _ in range(32)]
for _d in range(32):
    for _v in range(32):
        _o = CHI5[_v] ^ CHI5[_v ^ _d]
        DDT[_d][_o] += 1
        VMASK[_d][_o] |= 1 << _v


def popcount(v):
    return bin(v).count("1")


# ---------- affine subspaces of GF(2)^5 -----------------------------------------------------

def _span(vecs):
    sp = {0}
    for v in vecs:
        sp |= {u ^ v for u in sp}
    return sp


def _all_affine():
    # enumerate linear subspaces by spans of up to 5 vectors (dedupe by point mask)
    frontier = {1}
    dims = {1: 0}
    for _ in range(5):
        nxt = set()
        for m in frontier:
            pts = [v for v in range(32) if (m >> v) & 1]
            for v in range(32):
                if (m >> v) & 1:
                    continue
                nm = m
                for p in pts:
                    nm |= 1 << (p ^ v)
                if nm not in dims:
                    dims[nm] = dims[m] + 1
                    nxt.add(nm)
        frontier = nxt
    out = []
    for m, dm in dims.items():
        pts = [v for v in range(32) if (m >> v) & 1]
        seen = set()
        for a in range(32):
            am = 0
            for p in pts:
                am |= 1 << (p ^ a)
            if am in seen:
                continue
            seen.add(am)
            out.append((am, dm))
    return out


AFF = _all_affine()  # list of (point mask, dim); 2451 entries


def affine_eqs(mask):
    """Equations (u, k) with u.v = k on all points of the affine set `mask` (a basis of them)."""
    pts = [v for v in range(32) if (mask >> v) & 1]
    eqs = []
    span_u = {0}
    for u in range(1, 32):
        ks = {popcount(u & p) & 1 for p in pts}
        if len(ks) == 1 and u not in span_u:
            eqs.append((u, ks.pop()))
            span_u |= {w ^ u for w in span_u}
    return eqs


def affine_form(mask, fbit):
    """(g, c) with chi bit fbit = g.v ^ c on every point of mask, or None."""
    pts = [v for v in range(32) if (mask >> v) & 1]
    for g in range(32):
        c = ((CHI5[pts[0]] >> fbit) & 1) ^ (popcount(g & pts[0]) & 1)
        if all((((CHI5[p] >> fbit) & 1) ^ (popcount(g & p) & 1)) == c for p in pts):
            return g, c
    return None


# ---------- linear layer as row vectors ------------------------------------------------------

def _l_rows():
    """rows[j] = set of input bits (as int) whose XOR is output bit j of L."""
    cols = [L(1 << i) for i in range(NB)]
    rows = [0] * NB
    for i, cv in enumerate(cols):
        while cv:
            lb = cv & -cv
            j = lb.bit_length() - 1
            rows[j] |= 1 << i
            cv ^= lb
    return rows


def _invert(rows):
    """Rows of the inverse of the matrix given by rows (row j: output j = rows[j] . input)."""
    n = len(rows)
    aug = [(rows[j], 1 << j) for j in range(n)]
    piv = {}
    for j in range(n):
        a, b = aug[j]
        while a:
            hb = a.bit_length() - 1
            if hb in piv:
                pa, pb = piv[hb]
                a ^= pa
                b ^= pb
            else:
                piv[hb] = (a, b)
                break
    # back-substitute to identity
    order = sorted(piv)
    for hb in order:
        a, b = piv[hb]
        rest = a ^ (1 << hb)
        while rest:
            h2 = rest.bit_length() - 1
            pa, pb = piv[h2]
            a ^= pa
            b ^= pb
            rest = a ^ (1 << hb)
        piv[hb] = (a, b)
    # piv[i] = (e_i, combo) means input_i = XOR of outputs in combo
    return [piv[i][1] for i in range(n)]


def load_linear():
    path = os.path.join(HERE, "linear_cache.txt")
    if os.path.exists(path):
        with open(path) as f:
            parts = f.read().split()
        lr = [int(t, 16) for t in parts[:NB]]
        li = [int(t, 16) for t in parts[NB:2 * NB]]
        return lr, li
    lr = _l_rows()
    li = _invert(lr)
    with open(path, "w") as f:
        f.write("\n".join("%x" % v for v in lr + li))
    return lr, li


LROWS, LINV = load_linear()


def apply_rows(rows, s):
    out = 0
    for j, r in enumerate(rows):
        if popcount(r & s) & 1:
            out |= 1 << j
    return out


def Linv(s):
    return apply_rows(LINV, s)


# ---------- trail core No. 3 (GLL+20 Table 9, public text) ---------------------------------

def parse_trail(path=os.path.join(HERE, "trail_core3.txt")):
    lines = [ln.strip() for ln in open(path) if ln.strip()]
    assert len(lines) == 10

    def plane_block(block):
        s = 0
        for y, ln in enumerate(block):
            fields = ln.split("|")
            for x, fld in enumerate(fields):
                v = int(fld.replace("-", "0"), 16)
                s |= v << (64 * (x + 5 * y))
        return s
    return plane_block(lines[:5]), plane_block(lines[5:])


def active_rows(s):
    out = []
    for r in range(320):
        v = row_val(s, r)
        if v:
            out.append((r, v))
    return out


def in_kernel(s):
    a = to_lanes(s)
    return all((a[x] ^ a[x + 5] ^ a[x + 10] ^ a[x + 15] ^ a[x + 20]) == 0 for x in range(5))


PAD_BITS = {}
for _j in range(1080, NB):
    PAD_BITS[_j] = ((0x86 >> (_j - 1080)) & 1) if _j < 1088 else 0
```

B.2 `r5conn.py` (SHA-256 076313ece15b7979a8499c45c332390dc4144ced7cecb2f94f169aade9954212)

```python
"""Byte-aligned 2-round connector for 5-round SHA3-256 (135-byte messages), trail core No. 3.

witness_sat: one CryptoMiniSat instance over the message bits s, the message difference alpha0
  (both zero/fixed on the 520 padding and capacity bits), x = L(s), beta0 = L(alpha0) and the
  chi gates of round 0 for both messages. Its solutions are pairs whose round-0 output
  difference is alpha1 and whose round-1 chi input satisfies E_1 (so round 1 outputs alpha2).
anchored_space: the affine system E_pad + E_0 + non-full linearisation + linearised E_1 on x,
  with every linearisation subspace chosen to contain the witness, so the system is
  consistent by construction and every solution is a connector pair (Lemma in proof.md).
"""
import r5core as K
from pycryptosat import Solver

NB = 1600
B2, B3 = K.parse_trail()
A3 = K.Linv(B3)
A2 = K.Linv(B2)
A2_ROWS = K.active_rows(A2)
RC0 = K.RC[0]  # iota of round 0 touches lane 0


def place(r, v):
    y, z = divmod(r, 64)
    s = 0
    for x in range(5):
        if (v >> x) & 1:
            s |= 1 << K.bit(x, y, z)
    return s


def n_active(s):
    a = K.to_lanes(s)
    act = 0
    for y in range(5):
        act += K.popcount(a[5 * y] | a[5 * y + 1] | a[5 * y + 2] | a[5 * y + 3] | a[5 * y + 4])
    return act


# ---------------- GF(2) system in RREF -----------------------------------------------------

class Sys:
    """Rows are ints: bit 0 = constant, bit i+1 = variable i. Kept in reduced row echelon form."""

    def __init__(self):
        self.piv = {}
        self.pmask = 0
        self.bad = 0

    def reduce(self, row):
        t = row & self.pmask
        while t:
            lb = t & -t
            row ^= self.piv[lb.bit_length() - 1]
            t = row & self.pmask
        return row

    def add(self, row):
        row = self.reduce(row)
        if row == 0:
            return 0
        if row == 1:
            self.bad += 1
            return -1
        hb = row.bit_length() - 1
        m = 1 << hb
        for p, pr in self.piv.items():
            if pr & m:
                self.piv[p] = pr ^ row
        self.piv[hb] = row
        self.pmask |= m
        return 1

    def rank(self):
        return len(self.piv)

    def expr(self, var):
        b = var + 1
        if b in self.piv:
            return self.piv[b] ^ (1 << b)
        return 1 << b

    def copy(self):
        c = Sys()
        c.piv = dict(self.piv)
        c.pmask = self.pmask
        c.bad = self.bad
        return c


def row_eq(r, u, k):
    """Equation u . x|r = k as a system row."""
    bits = K.row_bits(r)
    row = k
    for x in range(5):
        if (u >> x) & 1:
            row ^= 1 << (bits[x] + 1)
    return row


def projection(sys_, r):
    """Point mask of the projection of the solution set onto row r of x."""
    ex = [sys_.expr(b) for b in K.row_bits(r)]
    mask = 0
    # value v is reachable iff for every mu with XOR of linear parts 0, mu.v = mu.c
    rel = []
    for mu in range(1, 32):
        acc = 0
        for x in range(5):
            if (mu >> x) & 1:
                acc ^= ex[x]
        if acc >> 1 == 0:
            rel.append((mu, acc & 1))
    for v in range(32):
        if all((K.popcount(mu & v) & 1) == c for mu, c in rel):
            mask |= 1 << v
    return mask


# precomputed affine subspaces with their equations and per-bit affine forms
AFF = []
for _m, _d in K.AFF:
    AFF.append((_m, _d, K.affine_eqs(_m), [K.affine_form(_m, b) for b in range(5)]))
AFF.sort(key=lambda t: -t[1])


class Connector:
    def __init__(self, beta1, alpha1):
        self.beta1 = beta1
        self.alpha1 = alpha1
        # E_1: for each active row of beta1, equations of V(beta1|r, alpha2|r) on y = L(a0)
        self.e1 = []
        for r in range(320):
            d = K.row_val(beta1, r)
            if not d:
                continue
            o = K.row_val(A2, r)
            assert K.DDT[d][o] > 0
            bits = K.row_bits(r)
            for u, k in K.affine_eqs(K.VMASK[d][o]):
                sset = 0
                for x in range(5):
                    if (u >> x) & 1:
                        sset ^= K.LROWS[bits[x]]
                # a0 = chi(x) ^ RC0 ; RC0 = bit 0 of lane 0 (only bit 0 set for round 0)
                const = k ^ (sset & 1)
                self.e1.append((sset, const))
        self.need = {}
        for sset, _ in self.e1:
            t = sset
            while t:
                lb = t & -t
                i = lb.bit_length() - 1
                lane, z = divmod(i, 64)
                x, y = lane % 5, lane // 5
                r = 64 * y + z
                self.need[r] = self.need.get(r, 0) | (1 << x)
                t ^= lb

    def base_system(self, beta0):
        S = Sys()
        for j in range(1080, NB):
            if S.add((K.LINV[j] << 1) | K.PAD_BITS[j]) < 0:
                return None, 0
        w0 = 0
        for r in range(320):
            d = K.row_val(beta0, r)
            if not d:
                continue
            o = K.row_val(self.alpha1, r)
            for u, k in K.affine_eqs(K.VMASK[d][o]):
                w0 += 1
                if S.add(row_eq(r, u, k)) < 0:
                    return None, w0
        return S, w0

    def add_e1(self, S, forms):
        bad = 0
        for sset, const in self.e1:
            row = const
            t = sset
            while t:
                lb = t & -t
                i = lb.bit_length() - 1
                lane, z = divmod(i, 64)
                x, y = lane % 5, lane // 5
                r = 64 * y + z
                g, c = forms[r][x]
                row ^= c
                bits = K.row_bits(r)
                for xx in range(5):
                    if (g >> xx) & 1:
                        row ^= 1 << (bits[xx] + 1)
                t ^= lb
            if S.add(row) < 0:
                bad += 1
        return bad


def space_of(S):
    """x0 and basis of the affine solution set of S."""
    x0 = 0
    for p, row in S.piv.items():
        if row & 1:
            x0 |= 1 << (p - 1)
    free = [v for v in range(NB) if not (S.pmask >> (v + 1)) & 1]
    basis = []
    for f in free:
        b = 1 << f
        fb = 1 << (f + 1)
        for p, row in S.piv.items():
            if row & fb:
                b |= 1 << (p - 1)
        basis.append(b)
    return x0, basis


def check_space(x0, basis, beta0, rng, n=8):
    """Sample points; check exact 2-round difference alpha2 and padding."""
    ok = 0
    for _ in range(n):
        x = x0
        for b in basis:
            if rng.getrandbits(1):
                x ^= b
        s = K.Linv(x)
        s2 = K.Linv(x ^ beta0)
        if s >> 1080 != (0x86) or s2 >> 1080 != 0x86:
            continue
        d = K.rounds_from_chi_input(x, 0, 1) ^ K.rounds_from_chi_input(x ^ beta0, 0, 1)
        if d == A2:
            ok += 1
    return ok


# ---------------- joint witness SAT (rounds 0 and 1, byte padding) -------------------------

def witness_sat(con, rng, thr=2, n_hash=0, confl=None, threads=1, n2max=None, hash_len=None):
    """Find s (135-byte padded block) and alpha0 (zero on the 520 fixed bits) such that the
    pair (s, s ^ alpha0) has round-0 output difference alpha1 and round-1 output difference
    alpha2. Returns (x, beta0) with x = L(s), or None."""
    kw = {"threads": threads}
    if confl:
        kw["confl_limit"] = confl
    S = Solver(**kw)
    vs = lambda i: 1 + i
    va = lambda i: 1081 + i
    vx = lambda j: 2161 + j
    vb = lambda j: 3761 + j
    vt = lambda j: 5361 + j
    vu = lambda j: 6961 + j
    for j in range(NB):
        lits = [vs(i) for i in range(1080) if (K.LROWS[j] >> i) & 1]
        const = 0
        t = K.LROWS[j] >> 1080
        i = 1080
        while t:
            if t & 1:
                const ^= K.PAD_BITS[i]
            t >>= 1
            i += 1
        S.add_xor_clause(lits + [vx(j)], bool(const))
        lits = [va(i) for i in range(1080) if (K.LROWS[j] >> i) & 1]
        S.add_xor_clause(lits + [vb(j)], False)

    def nb(j, k):
        lane, z = divmod(j, 64)
        x, y = lane % 5, lane // 5
        return 64 * (((x + k) % 5) + 5 * y) + z

    for j in range(NB):
        a, b = vx(nb(j, 1)), vx(nb(j, 2))
        t = vt(j)
        S.add_clause([-t, -a])
        S.add_clause([-t, b])
        S.add_clause([t, a, -b])
    for r in range(320):
        o = K.row_val(con.alpha1, r)
        bits = K.row_bits(r)
        if o == 0:
            for bb in bits:
                S.add_clause([-vb(bb)])
            continue
        for d in range(32):
            if K.DDT[d][o] < thr:
                S.add_clause([(-vb(bits[x]) if (d >> x) & 1 else vb(bits[x])) for x in range(5)])
    vxp = lambda j: 8561 + j
    for r in range(320):
        o = K.row_val(con.alpha1, r)
        if o == 0:
            continue
        bits = K.row_bits(r)
        for xx in range(5):
            j = bits[xx]
            S.add_xor_clause([vx(j), vb(j), vxp(j)], False)
        for xx in range(5):
            j = bits[xx]
            a, b = vxp(bits[(xx + 1) % 5]), vxp(bits[(xx + 2) % 5])
            u = vu(j)
            S.add_clause([-u, -a])
            S.add_clause([-u, b])
            S.add_clause([u, a, -b])
            # chi(x)_j ^ chi(x')_j = alpha1_j  <=>  b_j ^ t_j ^ u_j = alpha1_j
            S.add_xor_clause([vb(j), vt(j), vu(j)], bool((o >> xx) & 1))
    # E_1: sum over sset of chi(x)_i = const, chi(x)_i = x_i ^ t_i
    for sset, const in con.e1:
        lits = []
        t = sset
        while t:
            lb = t & -t
            i = lb.bit_length() - 1
            lits += [vx(i), vt(i)]
            t ^= lb
        S.add_xor_clause(lits, bool(const))
    if n2max is not None:
        nxt = 10161
        ev = []
        for r in range(320):
            o = K.row_val(con.alpha1, r)
            if o == 0:
                continue
            bits = K.row_bits(r)
            e = nxt
            nxt += 1
            ev.append(e)
            for d in range(32):
                if K.DDT[d][o] == 2:
                    S.add_clause([(-vb(bits[x]) if (d >> x) & 1 else vb(bits[x])) for x in range(5)] + [e])
        n, k = len(ev), n2max
        sv = [[nxt + i * k + j for j in range(k)] for i in range(n)]
        nxt += n * k
        S.add_clause([-ev[0], sv[0][0]])
        for j in range(1, k):
            S.add_clause([-sv[0][j]])
        for i in range(1, n):
            S.add_clause([-ev[i], sv[i][0]])
            S.add_clause([-sv[i - 1][0], sv[i][0]])
            for j in range(1, k):
                S.add_clause([-ev[i], -sv[i - 1][j - 1], sv[i][j]])
                S.add_clause([-sv[i - 1][j], sv[i][j]])
            S.add_clause([-ev[i], -sv[i - 1][k - 1]])
    for _ in range(n_hash):
        if hash_len:
            h = [vs(i) for i in rng.sample(range(1080), hash_len)]
        else:
            h = [vs(i) for i in range(1080) if rng.random() < 0.5]
        S.add_xor_clause(h, bool(rng.getrandbits(1)))
    sat, sol = S.solve()
    if sat is not True:
        return None
    s = 0
    a0 = 0
    for i in range(1080):
        if sol[vs(i)]:
            s |= 1 << i
        if sol[va(i)]:
            a0 |= 1 << i
    for i, v in K.PAD_BITS.items():
        s |= v << i
    return K.L(s), K.L(a0)


def anchored_space(con, x, beta0, rng):
    """Linear system around witness x; consistent by construction."""
    S, w0 = con.base_system(beta0)
    if S is None:
        return None
    rank0 = S.rank()
    S = S.copy()
    forms = {}
    nlin = 0
    rows = list(con.need)
    rng.shuffle(rows)
    for r in rows:
        nbits = con.need[r]
        v = K.row_val(x, r)
        P = projection(S, r)
        assert (P >> v) & 1
        best = None
        cands = []
        for m, dm, eqs, af in AFF:
            if best is not None and dm < best:
                break
            if not (m >> v) & 1 or m & ~P:
                continue
            if all(af[xx] is not None for xx in range(5) if (nbits >> xx) & 1):
                best = dm
                cands.append((m, eqs, af))
        m, eqs, af = rng.choice(cands)
        for u, k in eqs:
            rr = S.add(row_eq(r, u, k))
            assert rr >= 0
            nlin += rr
        forms[r] = af
    rank1 = S.rank()
    bad = con.add_e1(S, forms)
    return S, w0, rank0, nlin, rank1, bad


def export_space(path, S, beta0, max_basis=48):
    x0, basis = space_of(S)
    free = [v for v in range(NB) if not (S.pmask >> (v + 1)) & 1]
    # beta0 in the linear part?  then drop one free direction carrying it
    comb = 0
    for f, b in zip(free, basis):
        if (beta0 >> f) & 1:
            comb ^= b
    in_lin = comb == beta0
    if in_lin:
        drop = next(k for k, f in enumerate(free) if (beta0 >> f) & 1)
        basis = basis[:drop] + basis[drop + 1:]
    basis = basis[:max_basis]
    conds = []
    for r, d in K.active_rows(B2):
        y, z = divmod(r, 64)
        conds.append((K.DDT[d][K.row_val(A3, r)], y, z, K.VMASK[d][K.row_val(A3, r)]))
    conds.sort()
    with open(path, "w") as f:
        f.write(" ".join("%x" % v for v in K.to_lanes(x0)) + "\n")
        f.write(" ".join("%x" % v for v in K.to_lanes(beta0)) + "\n")
        f.write("%d\n" % len(basis))
        for b in basis:
            f.write(" ".join("%x" % v for v in K.to_lanes(b)) + "\n")
        f.write("%d\n" % len(conds))
        for _, y, z, m in conds:
            f.write("%d %d %x\n" % (y, z, m))
    return x0, basis, in_lin


INSET = [sum(1 << d for d in range(32) if K.DDT[d][o] > 0) for o in range(32)]


def diff_prefilter(a1):
    """Necessary condition for B2: with alpha0 zero on the 520 fixed bits and beta0 zero on the
    inactive rows of alpha1, every active row of beta0 can still take a compatible value."""
    S = Sys()
    for j in range(1080, NB):
        S.add(K.LINV[j] << 1)
    act = []
    for r in range(320):
        o = K.row_val(a1, r)
        if o == 0:
            for b in K.row_bits(r):
                S.add(1 << (b + 1))
        else:
            act.append((r, o))
    for r, o in act:
        if not projection(S, r) & INSET[o]:
            return False
    return True
```

B.3 `r5chain.py` (SHA-256 a31ec1520421d85952c50b74b20bfdd2b3374196fd3f636ee594a7030bd451f9)

```python
"""Construction chain C, phases P and B1-B4, for 5-round SHA3-256 (135-byte messages).

usage: python3 r5chain.py LABEL OUTDIR

seed64 = first 64 bits of SHA-256(LABEL). Every random choice below is drawn from
random.Random(seed64 + offset) with a fixed offset per use. Stopping rules:
  B2  beta1 candidates in the fixed order (active rows of alpha1, then choice tuple); a
      candidate goes to B3 when it passes the linear difference prefilter.
  B3  witness attempts a = 0, 1, ..., 7 on that beta1: joint CryptoMiniSat instance with at
      most 90 DDT-2 rows in round 0, 8 random XOR hash constraints of length 16, conflict
      limit 3e6; an attempt is accepted when its anchored space has DF >= 42.
      If all 8 fail, B2 resumes with the next candidate.
  B4  the accepted space is written to OUTDIR/space.txt for phase D (r5search).
"""
import hashlib
import itertools
import json
import os
import random
import sys
import time

T0 = time.time()
LABEL, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
SEED = int(hashlib.sha256(LABEL.encode()).hexdigest()[:16], 16)
LOG = open(os.path.join(OUT, "chain.log"), "w")


def log(*a):
    msg = " ".join(str(v) for v in a)
    print(msg)
    LOG.write("%.1f %s\n" % (time.time() - T0, msg))
    LOG.flush()


# Phase P: linear layer and its inverse are recomputed here (no cache).
cache = os.path.join(os.path.dirname(os.path.abspath(__file__)), "linear_cache.txt")
if os.path.exists(cache):
    os.remove(cache)
import r5core as K  # noqa: E402
import r5conn as C  # noqa: E402

assert K.in_kernel(C.A3)
assert sum(5 - (K.DDT[d][K.row_val(C.A3, r)].bit_length() - 1) for r, d in K.active_rows(C.B2)) == 24
log("P trail ok: alpha2 rows", len(C.A2_ROWS), "seed64 %016x" % SEED)

# Phase B1
base_b1 = 0
base_a1 = 0
multi = []
for r, o in C.A2_ROWS:
    m = max(K.DDT[d][o] for d in range(1, 32))
    ds = [d for d in range(1, 32) if K.DDT[d][o] == m]
    if len(ds) == 1:
        base_b1 ^= C.place(r, ds[0])
        base_a1 ^= K.Linv(C.place(r, ds[0]))
    else:
        multi.append([(C.place(r, d), K.Linv(C.place(r, d))) for d in ds])
order = []
for combo in itertools.product(*[range(len(m)) for m in multi]):
    a1 = base_a1
    for i, c in enumerate(combo):
        a1 ^= multi[i][c][1]
    order.append((C.n_active(a1), combo))
order.sort()
log("B1 candidates", len(order), "min active", order[0][0])


def cand(idx):
    a1, b1 = base_a1, base_b1
    for i, c in enumerate(order[idx][1]):
        a1 ^= multi[i][c][1]
        b1 ^= multi[i][c][0]
    return b1, a1


# Phases B2/B3
idx = 0
n_prefilter = 0
n_witness = 0
accepted = None
while accepted is None:
    b1, a1 = cand(idx)
    n_prefilter += 1
    if not C.diff_prefilter(a1):
        idx += 1
        continue
    log("B2 candidate", idx, "active rows", order[idx][0], "passes the prefilter after", n_prefilter, "tests")
    con = C.Connector(b1, a1)
    for a in range(8):
        n_witness += 1
        w = C.witness_sat(con, random.Random(SEED + 1 + a), thr=2, n_hash=8, hash_len=16,
                          confl=3000000, n2max=90)
        if w is None:
            log("B3 attempt", a, "no witness")
            continue
        x, b0 = w
        S, w0, r0, nl, r1, bad = C.anchored_space(con, x, b0, random.Random(SEED + 1001 + a))
        df = 1600 - S.rank()
        log("B3 attempt", a, "w0", w0, "rank0", r0, "lin", nl, "rank1", r1, "E1 inconsistent", bad, "DF", df)
        if df >= 42 and bad == 0:
            accepted = (idx, a, x, b0, b1, a1, S, df)
            break
    else:
        idx += 1

idx, a, x, b0, b1, a1, S, df = accepted
x0, basis, in_lin = C.export_space(os.path.join(OUT, "space.txt"), S, b0)
x0s, full_basis = C.space_of(S)
chk = C.check_space(x0s, full_basis, b0, random.Random(SEED + 77), n=16)
meta = {
    "label": LABEL, "seed64": "%016x" % SEED, "beta1_index": idx, "witness_attempt": a,
    "prefilter_tests": n_prefilter, "witness_sat_calls": n_witness, "DF": df,
    "beta0_in_linear_part": in_lin, "basis_exported": len(basis), "check_alpha2_16": chk,
    "x_witness": "%0400x" % x, "beta0": "%0400x" % b0, "beta1": "%0400x" % b1,
    "alpha1": "%0400x" % a1, "x0": "%0400x" % x0, "seconds": round(time.time() - T0, 1),
}
json.dump(meta, open(os.path.join(OUT, "connector.json"), "w"), indent=1)
log("B4 exported DF", df, "basis", len(basis), "beta0 in lin", in_lin, "alpha2 check", chk, "/16")
```

B.4 `r5search.c` (SHA-256 555c46975b3c2ade6e8c76c1167e6f3b40ad409d893112b1d6e2fe956ddb645f)

```c
/* Online stage for the 5-round SHA3-256 connector space.
 *
 * Input (text, hex lanes): x0[25], beta0[25], n, basis[n][25], m, then m lines "y z mask"
 * with the round-2 chi-input conditions (row value v must have bit v of mask set).
 * Pairs: index i in [lo, hi), x_i = x0 ^ sum_k gray(i)_k basis[k], partner x_i ^ beta0.
 * Stage 1: rounds 0-1 and theta-rho-pi of round 2 on x_i, test the condition rows.
 * Stage 2 (Stage-1 pass): both 5-round digests (lanes 0..3), compare.
 * Threads take chunks of 2^CHUNK_LOG2 indices in increasing order; all evaluated pairs are
 * counted. A found collision sets a stop flag; every thread checks it every 4096 pairs and
 * returns. The printed pair count is the exact number of pairs evaluated by all threads.
 *
 * usage: r5search INPUT LO HI THREADS CHUNK_LOG2 [stop_at_first=1]
 */
#include <inttypes.h>
#include <pthread.h>
#include <stdatomic.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef uint64_t u64;
#define ROL(a, n) (((n) == 0) ? (a) : (((a) << (n)) | ((a) >> (64 - (n)))))
#include "keccak_unrolled.h"

static const u64 RC[5] = {0x0000000000000001ULL, 0x0000000000008082ULL, 0x800000000000808AULL,
                          0x8000000080008000ULL, 0x000000000000808BULL};
static const int RHO[25] = {0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39,
                            41, 45, 15, 21, 8, 18, 2, 61, 56, 14};
static int PI_DST[25];

static u64 X0[25], B0[25];
static u64 (*BASIS)[25];
static int NBASIS;
static int NCOND;
static int CY[16], CZ[16];
static uint32_t CMASK[16];
static int STOP_FIRST = 1;

static atomic_ullong next_chunk;
static atomic_int stop_flag;
static u64 G_LO, G_HI, CHUNK;
static pthread_mutex_t mu = PTHREAD_MUTEX_INITIALIZER;
static u64 best_idx = UINT64_MAX;
static u64 best_x[25];
static u64 tot_pairs, tot_pass, tot_coll;
static u64 tot_rowpass[16];

static inline void theta_rhopi(const u64 *a, u64 *b) {
    u64 c[5], d[5];
    for (int x = 0; x < 5; x++) c[x] = a[x] ^ a[x + 5] ^ a[x + 10] ^ a[x + 15] ^ a[x + 20];
    for (int x = 0; x < 5; x++) d[x] = c[(x + 4) % 5] ^ ROL(c[(x + 1) % 5], 1);
    for (int i = 0; i < 25; i++) {
        u64 v = a[i] ^ d[i % 5];
        b[PI_DST[i]] = ROL(v, RHO[i]);
    }
}

static inline void chi_iota(const u64 *b, u64 *a, int rnd) {
    for (int y = 0; y < 25; y += 5)
        for (int x = 0; x < 5; x++)
            a[y + x] = b[y + x] ^ ((~b[y + (x + 1) % 5]) & b[y + (x + 2) % 5]);
    a[0] ^= RC[rnd];
}

/* digest lanes 0..3 after 5 rounds, starting from chi input x of round 0 */
static void digest_from_x(const u64 *x, u64 *dg) {
    u64 a[25], b[25];
    chi_iota(x, a, 0);
    for (int r = 1; r < 5; r++) {
        theta_rhopi(a, b);
        chi_iota(b, a, r);
    }
    memcpy(dg, a, 4 * sizeof(u64));
}

static inline u64 gray(u64 i) { return i ^ (i >> 1); }

static void *worker(void *arg) {
    (void)arg;
    u64 pairs = 0, pass = 0, coll = 0;
    u64 rowpass[16] = {0};
    u64 x[25], a[25], b[25];
    for (;;) {
        if (atomic_load(&stop_flag)) break;
        u64 ck = atomic_fetch_add(&next_chunk, 1);
        u64 lo = G_LO + ck * CHUNK;
        if (lo >= G_HI) break;
        u64 hi = lo + CHUNK;
        if (hi > G_HI) hi = G_HI;
        u64 g = gray(lo);
        memcpy(x, X0, sizeof x);
        for (int k = 0; k < NBASIS; k++)
            if ((g >> k) & 1)
                for (int l = 0; l < 25; l++) x[l] ^= BASIS[k][l];
        for (u64 i = lo; i < hi; i++) {
            if (i != lo) {
                const u64 *bv = BASIS[__builtin_ctzll(i)];
                for (int l = 0; l < 25; l++) x[l] ^= bv[l];
            }
            pairs++;
            CHI_IOTA(x, a, RC[0]);
            THETA_RHOPI(a, b);
            CHI_IOTA(b, a, RC[1]);
            THETA_RHOPI(a, b);
            int ok = 1;
            for (int c = 0; c < NCOND; c++) {
                int y = CY[c], z = CZ[c];
                unsigned v = (unsigned)(((b[5 * y] >> z) & 1) | (((b[5 * y + 1] >> z) & 1) << 1) |
                                        (((b[5 * y + 2] >> z) & 1) << 2) | (((b[5 * y + 3] >> z) & 1) << 3) |
                                        (((b[5 * y + 4] >> z) & 1) << 4));
                if (!((CMASK[c] >> v) & 1)) { ok = 0; break; }
                rowpass[c]++;
            }
            if (ok) {
                pass++;
                u64 x2[25], d1[4], d2[4];
                for (int l = 0; l < 25; l++) x2[l] = x[l] ^ B0[l];
                digest_from_x(x, d1);
                digest_from_x(x2, d2);
                if (d1[0] == d2[0] && d1[1] == d2[1] && d1[2] == d2[2] && d1[3] == d2[3]) {
                    coll++;
                    pthread_mutex_lock(&mu);
                    if (i < best_idx) { best_idx = i; memcpy(best_x, x, sizeof x); }
                    printf("COLLISION idx %" PRIu64 "\n", i);
                    fflush(stdout);
                    pthread_mutex_unlock(&mu);
                    if (STOP_FIRST) atomic_store(&stop_flag, 1);
                }
            }
            if ((pairs & 4095) == 0 && atomic_load(&stop_flag)) goto done;
        }
    }
done:
    pthread_mutex_lock(&mu);
    tot_pairs += pairs; tot_pass += pass; tot_coll += coll;
    for (int c = 0; c < 16; c++) tot_rowpass[c] += rowpass[c];
    pthread_mutex_unlock(&mu);
    return NULL;
}

static void read_lanes(FILE *f, u64 *v) {
    for (int l = 0; l < 25; l++)
        if (fscanf(f, "%" SCNx64, &v[l]) != 1) { fprintf(stderr, "bad input\n"); exit(1); }
}

int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage\n"); return 1; }
    for (int y = 0; y < 5; y++)
        for (int x = 0; x < 5; x++) PI_DST[x + 5 * y] = y + 5 * ((2 * x + 3 * y) % 5);
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("input"); return 1; }
    read_lanes(f, X0);
    read_lanes(f, B0);
    if (fscanf(f, "%d", &NBASIS) != 1 || NBASIS > 63) return 1;
    BASIS = calloc(NBASIS, sizeof *BASIS);
    for (int k = 0; k < NBASIS; k++) read_lanes(f, BASIS[k]);
    if (fscanf(f, "%d", &NCOND) != 1 || NCOND > 16) return 1;
    for (int c = 0; c < NCOND; c++)
        if (fscanf(f, "%d %d %" SCNx32, &CY[c], &CZ[c], &CMASK[c]) != 3) return 1;
    fclose(f);
    G_LO = strtoull(argv[2], 0, 0);
    G_HI = strtoull(argv[3], 0, 0);
    int T = atoi(argv[4]);
    CHUNK = 1ULL << atoi(argv[5]);
    if (argc > 6) STOP_FIRST = atoi(argv[6]);
    pthread_t th[64];
    for (int t = 0; t < T; t++) pthread_create(&th[t], 0, worker, 0);
    for (int t = 0; t < T; t++) pthread_join(th[t], 0);
    printf("pairs %" PRIu64 " pass %" PRIu64 " coll %" PRIu64 "\n", tot_pairs, tot_pass, tot_coll);
    printf("rowpass");
    for (int c = 0; c < NCOND; c++) printf(" %" PRIu64, tot_rowpass[c]);
    printf("\n");
    if (best_idx != UINT64_MAX) {
        printf("best_idx %" PRIu64 "\nbest_x", best_idx);
        for (int l = 0; l < 25; l++) printf(" %016" PRIx64, best_x[l]);
        printf("\n");
    }
    return 0;
}
```

B.5 `keccak_unrolled.h` (SHA-256 257c736f4c06fe79feb798a98dec2da81bf89afb4111218ce6677eab978282e2)

```c
#define THETA_RHOPI(a, b) do { \
    u64 c0 = a[0]^a[5]^a[10]^a[15]^a[20], c1 = a[1]^a[6]^a[11]^a[16]^a[21], c2 = a[2]^a[7]^a[12]^a[17]^a[22], c3 = a[3]^a[8]^a[13]^a[18]^a[23], c4 = a[4]^a[9]^a[14]^a[19]^a[24]; \
    u64 d0 = c4 ^ ROL(c1, 1), d1 = c0 ^ ROL(c2, 1), d2 = c1 ^ ROL(c3, 1), d3 = c2 ^ ROL(c4, 1), d4 = c3 ^ ROL(c0, 1); \
    b[0] = ROL(a[0] ^ d0, 0); \
    b[10] = ROL(a[1] ^ d1, 1); \
    b[20] = ROL(a[2] ^ d2, 62); \
    b[5] = ROL(a[3] ^ d3, 28); \
    b[15] = ROL(a[4] ^ d4, 27); \
    b[16] = ROL(a[5] ^ d0, 36); \
    b[1] = ROL(a[6] ^ d1, 44); \
    b[11] = ROL(a[7] ^ d2, 6); \
    b[21] = ROL(a[8] ^ d3, 55); \
    b[6] = ROL(a[9] ^ d4, 20); \
    b[7] = ROL(a[10] ^ d0, 3); \
    b[17] = ROL(a[11] ^ d1, 10); \
    b[2] = ROL(a[12] ^ d2, 43); \
    b[12] = ROL(a[13] ^ d3, 25); \
    b[22] = ROL(a[14] ^ d4, 39); \
    b[23] = ROL(a[15] ^ d0, 41); \
    b[8] = ROL(a[16] ^ d1, 45); \
    b[18] = ROL(a[17] ^ d2, 15); \
    b[3] = ROL(a[18] ^ d3, 21); \
    b[13] = ROL(a[19] ^ d4, 8); \
    b[14] = ROL(a[20] ^ d0, 18); \
    b[24] = ROL(a[21] ^ d1, 2); \
    b[9] = ROL(a[22] ^ d2, 61); \
    b[19] = ROL(a[23] ^ d3, 56); \
    b[4] = ROL(a[24] ^ d4, 14); \
} while (0)
#define CHI_IOTA(b, a, rc) do { \
    a[0] = b[0] ^ ((~b[1]) & b[2]); \
    a[1] = b[1] ^ ((~b[2]) & b[3]); \
    a[2] = b[2] ^ ((~b[3]) & b[4]); \
    a[3] = b[3] ^ ((~b[4]) & b[0]); \
    a[4] = b[4] ^ ((~b[0]) & b[1]); \
    a[5] = b[5] ^ ((~b[6]) & b[7]); \
    a[6] = b[6] ^ ((~b[7]) & b[8]); \
    a[7] = b[7] ^ ((~b[8]) & b[9]); \
    a[8] = b[8] ^ ((~b[9]) & b[5]); \
    a[9] = b[9] ^ ((~b[5]) & b[6]); \
    a[10] = b[10] ^ ((~b[11]) & b[12]); \
    a[11] = b[11] ^ ((~b[12]) & b[13]); \
    a[12] = b[12] ^ ((~b[13]) & b[14]); \
    a[13] = b[13] ^ ((~b[14]) & b[10]); \
    a[14] = b[14] ^ ((~b[10]) & b[11]); \
    a[15] = b[15] ^ ((~b[16]) & b[17]); \
    a[16] = b[16] ^ ((~b[17]) & b[18]); \
    a[17] = b[17] ^ ((~b[18]) & b[19]); \
    a[18] = b[18] ^ ((~b[19]) & b[15]); \
    a[19] = b[19] ^ ((~b[15]) & b[16]); \
    a[20] = b[20] ^ ((~b[21]) & b[22]); \
    a[21] = b[21] ^ ((~b[22]) & b[23]); \
    a[22] = b[22] ^ ((~b[23]) & b[24]); \
    a[23] = b[23] ^ ((~b[24]) & b[20]); \
    a[24] = b[24] ^ ((~b[20]) & b[21]); \
    a[0] ^= (rc); \
} while (0)
```

B.6 `trail_core3.txt` (SHA-256 e042140cf7708a05d926c6f527ca2bdc7359a20857fb9570afed4650c8f4e17b)

```
---------------1|----------------|---------------4|----------------|----------------
---------------4|---------------4|---------------4|-----------2----|----------------
2---------------|----------------|----------2-----|----------------|----------------
2---------------|----------------|----------------|-----------2----|----------------
----------2----1|----------------|----------2-----|----------------|---------------1
---------------1|----------------|---------------1|------4---------|----------------
----------------|----------------|---------------1|----------------|-----------4----
----------------|-------------1--|----------------|----------------|-----------4----
----------------|----------------|----------------|----------------|----------------
---------------1|-------------1--|----------------|------4---------|----------------
```

B.7 `p34.py` (SHA-256 bc600e959a253f03b92be3e9497c02185b065dfe44aed54f98f4f2d60867d22f)

```python
"""Exact P(zero 256-bit digest difference | difference alpha3 entering round 3), Markov model:
sum over every alpha4 compatible with beta3 of P(beta3 -> alpha4) * prod over plane-0 rows of
P(round-4 output difference vanishes on lanes x = 0..3)."""
import itertools, math
import r5core as K
b2, b3 = K.parse_trail()
rows = K.active_rows(b3)
PZ = [sum(1 for v in range(32) if ((K.CHI5[v] ^ K.CHI5[v ^ d]) & 0xF) == 0) / 32 for d in range(32)]
opts = []
for r, d in rows:
    lst = []
    for o in range(32):
        if K.DDT[d][o]:
            s = 0
            y, z = divmod(r, 64)
            for x in range(5):
                if (o >> x) & 1:
                    s |= 1 << K.bit(x, y, z)
            lst.append((K.DDT[d][o] / 32, K.to_lanes(K.L(s))[:5]))
    opts.append(lst)
total = 0.0
best = 0.0
nz = 0
for combo in itertools.product(*opts):
    p = 1.0
    lanes = [0] * 5
    for pr, ln in combo:
        p *= pr
        for i in range(5):
            lanes[i] ^= ln[i]
    act = lanes[0] | lanes[1] | lanes[2] | lanes[3] | lanes[4]
    q = 1.0
    while act and q:
        lb = act & -act
        z = lb.bit_length() - 1
        dv = sum(((lanes[x] >> z) & 1) << x for x in range(5))
        q *= PZ[dv]
        act ^= lb
    if q:
        nz += 1
        total += p * q
        best = max(best, p * q)
print("alpha4 combos", math.prod(len(o) for o in opts), "nonzero", nz)
print("P34 = 2^%.4f  best single = 2^%.4f" % (math.log2(total), math.log2(best)))
```

## Appendix C. Raw measurement records

C.1 phase B (`run1-time.txt`)

```
       13.39 real        13.12 user         0.13 sys
           224526336  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
               30654  page reclaims
                  76  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   0  messages sent
                   0  messages received
                   0  signals received
                   8  voluntary context switches
                4926  involuntary context switches
        284576788169  instructions retired
         52442733225  cycles elapsed
           216400712  peak memory footprint
```

C.2 compilation (`compile-time.txt`)

```
        0.72 real         0.13 user         0.29 sys
            61292544  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
                4273  page reclaims
                4433  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   0  messages sent
                   0  messages received
                   0  signals received
                1342  voluntary context switches
                1555  involuntary context switches
           558963823  instructions retired
           373666612  cycles elapsed
             2867584  peak memory footprint
```

C.3 phase D (`search-time.txt`)

```
resource-guard: acquired task=claude-r5 label=r5 attack memory_free=43% required=0%
      177.54 real      1620.95 user         6.68 sys
             2015232  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
                 305  page reclaims
                   1  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   0  messages sent
                   0  messages received
                   0  signals received
                   2  voluntary context switches
             1243041  involuntary context switches
      34526936856517  instructions retired
       5460270176716  cycles elapsed
             1540456  peak memory footprint
```

C.4 phase D start/stop (`phaseD-start.txt`)

```
guard free at 2026-10-07T14:26:14+0900
exit 0 at 2026-10-07T14:29:12+0900
```
