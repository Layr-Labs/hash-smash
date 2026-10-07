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

Every computation of C is charged (Section 9), and so is every diagnostic run we made after the
commitment. Our own C program is charged from an instrumented trace: a counting twin of the search
loop (Section 7.1) counts every data-path operation per event class, and the executed event counts
come from the run. The Python and CryptoMiniSat process and the compilers are charged from
retired-instruction counters at 256 word operations per instruction, per phase (Section 7.1). The
complete source is in Appendix B and the commitments, written before the runs, are in Appendix A.

Changes from our previous filing fe9a898d (not_evaluable, no fatal finding):
- a second organizer experiment whose trusted event is checked on 256 distinct pairs of the
  connector space chosen by the organizer seeds: a 156-bit digest-XOR mask event that holds with
  probability 1 for pairs that follow the trail through round 2 and with probability 2^-156 for
  other pairs (Section 13);
- operation counts from an instrumented counting twin of phase D and per-phase instruction
  counters from an instrumented, byte-identical re-execution of phase B (Section 7.1);
- a memory inventory (Section 10);
- an explicit argument and a cited, bounded sensitivity for the trail search (Section 5.1), and the
  list of design constants that development fixed (Section 12).

| field | value | where |
|---|---|---|
| time_log2 | 37.95 | executed work of C, every diagnostic run and the replay, 2^37.9475, Section 9 |
| preprocessing_log2 | 37.95 | construction chain C, Section 9 |
| success_probability | 1 | deterministic replay, Section 3 |
| nonuniform_advice_log2_bytes | 11 | the stored 270-byte pair plus the 850-byte trail text, Section 10 |
| memory_log2_bytes | 29 | inventory of code, tables, files and advice, Section 10 |

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

Why the trail is algorithm text, and what charging its search would cost. The trail core is two
difference patterns of the permutation Keccak-f[1600] for rounds 2 and 3. It holds no message,
state value, connector, subspace or pair, and it does not depend on the message, the padding or
the capacity; GLL+20 use the same core for 5-round SHA3-224 and SHA3-256, and it has been public
since 2019. C reads it as a constant table, like the round constants and the chi DDT, and we count
its 850 bytes as nonuniform advice. Every object derived from it that is specific to our instance
(beta1, alpha1, beta0, the witness, the space, the index, the pair) is computed and charged in C.
We read the cost model's rule on "search omitted from the submitted program" as covering searches
whose outputs are specific to the submitted instance or run; a published characteristic of the
permutation is not such an output. This reading is a declared premise (H1).

Bounded sensitivity. GLL+20 do not report the cost of their search. A public package on this track
(Th0rgal, c48c3c23) runs its own trail search, which selects this same core, and charges it with a
hard cap of 485,271,104,148 units = 2^38.82 under that package's own operation accounting. If a
search of that size were added to our total, the total would be 2^39.45, still below the
current best public result. We have not run that search, we do not use its outputs, and its
number is a third-party report: we cite it only to bound the sensitivity, not as evidence for
our claim.

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

### 7.1 Instrumented counts and deterministic re-execution (diagnostics, charged)

Phase D counting twin. `r5count.c` (Appendix B.8, with `keccak_counted.h`, B.9) is the search loop
of `r5search.c` single-threaded, with every data-path operation routed through counting functions
in the organizer's convention (XOR, AND, OR, shift 1; NOT 2 for invert and mask; rotation 4 for two
shifts, OR and mask; compare-and-branch 2; ctz 24 and the basis address 4, since neither is a RAM
primitive). It counts per event class. Run on the chunk that contains the collision and on the
first 2^24 indices (Appendix C.5):

```
collision chunk [73685532672, +2^24):
pairs 16777216 rows 17978020 pass 2 coll 1 chunks 1 first 73686378480
ops pair 10166992843 row 450651306 pass 4806 chunk 538
per_event pair 606.0000 row 25.0668 pass 2403.0000 chunk 538.0000

first 2^24 indices:
pairs 16777216 rows 17978683 pass 1 coll 0 chunks 4 first 0
ops pair 10166992684 row 450668543 pass 2403 chunk 1502
per_event pair 606.0000 row 25.0668 pass 2403.0000 chunk 375.5000
```

So the traced constants are: 606 operations per enumerated pair (Gray step, Stage 1, loop
control; 53 fewer for the first pair of a chunk), 25 per round-2 row test plus 1 per row that
passes, 2403 per Stage-1 pass (both digests and the compare), and at most 1,538 per chunk
start (538 observed). The twin reproduces the collision at index 73686378480 and the same
pass count as `r5search` on that chunk. Memory traffic is not traced: we charge every data-path
operation two operand loads and one result store (a register-free RAM), so each traced operation
counts 4 word operations in the ledger.

Phase B instruction trace. `r5chain_instr.py` (Appendix B.10) is `r5chain.py` with one change: each
log line also records the process's retired-instruction and cycle counters
(`proc_pid_rusage`, `rusage_probe.py`, Appendix B.11). We re-executed phase B with the committed
label. It reproduced `space.txt` byte for byte and `connector.json` except the elapsed seconds, and
gave this per-phase trace (cumulative instructions):

```
0.2 P trail ok: alpha2 rows 59 seed64 a34682764a9fb0d2 | instr 5556873130 cycles 934278002 footprint 19497632 maxfootprint 19497632
3.6 B1 candidates 800000 min active 242 | instr 85029636786 cycles 14455732837 footprint 197739312 maxfootprint 200770352
7.2 B2 candidate 140 active rows 264 passes the prefilter after 141 tests | instr 178893511283 cycles 29347363647 footprint 192496432 maxfootprint 200770352
12.9 B3 attempt 0 w0 847 rank0 1324 lin 93 rank1 1417 E1 inconsistent 0 DF 58 | instr 279879501009 cycles 51839431396 footprint 197116720 maxfootprint 219775792
13.0 B4 exported DF 58 basis 48 beta0 in lin True alpha2 check 16 /16 | instr 281602690831 cycles 52385030097 footprint 197116720 maxfootprint 219775792
```

The re-execution itself is charged as a diagnostic (Section 9). The trace shows that phase B's
instructions are spread as 2% tables, 28% beta1 ordering, 33% prefilter, 36% SAT and space, 1%
export; the CryptoMiniSat call is the only part not written by us.

Reproducibility. C is deterministic given the committed label: anyone with the embedded source can
rerun phase B (13 s on one core) and the collision chunk of phase D (under 1 s on one core) and
obtain the same space, the same index and the same counters.

## 8. Why the output collides

Lemma 3 gives difference alpha2 after rounds 0-1 for every enumerated pair, Stage 1 certifies
alpha3 after round 2, and Stage 2 compares the two complete 5-round digests computed from the
round-0 chi inputs. The final pair was re-hashed from its bytes with `verifier/keccak.py`
(Section 4) and is the organizer-verified certificate.

## 9. Cost ledger (units of one 5-round permutation)

| line | count | units |
|---|---|---|
| phase B: retired instructions x 256 / 1355 (H3) | 284576788169 instr | 5.37651e+10 |
| compilation of r5search.c x 256 / 1355 (H3) | 558963823 instr | 1.05605e+08 |
| phase D: traced operations x 4 / 1355 (H2) | 73615736832 pairs, 78887653477 row tests, 4373 passes | 1.37531e+11 |
| output conversion and check | 1 | 1000 |
| scored replay (Section 3) | 1 | 2.23 |
| diagnostic: instrumented re-execution of phase B (H3) | 282494312169 instr | 5.33716e+10 |
| diagnostic: pool scan for the mask experiment (traced, H2) | 8589934592 pairs | 1.6048e+10 |
| diagnostic: counting-twin and single-thread chunk runs (<= 2 units/pair) | 100663296 pairs | 2.01327e+08 |
| diagnostic: 5 compilations, probe and inventory scripts (H3) | <= 21383113626 instr | 4.03991e+09 |
| **total** | | **2.65062e+11 = 2^37.9475** |

All counts are executed counts, not expectations, and include every failure, every prefilter test
and every thread's work. Phase D is charged from the traced constants of Section 7.1 and the
executed event counts of Section 7: data-path operations = 606 N + 25 (row tests) +
(rows passed) + 2403 (Stage-1 passes) + 1,538 (chunks), with N = 73615736832, row tests =
78887653477, rows passed = 5271921018, chunks <= N / 2^24 + 11; times 4 for memory traffic.
That is 1.868 units per enumerated pair on average. The output conversion (two dense
1600 x 1600 GF(2) matrix-vector products, under 400,000 word operations with memory traffic) and
the verifier check are charged 1,000 units.

Diagnostics are charged although none of them is needed to produce the pair: the instrumented
re-execution of phase B, the counting-twin and single-thread chunk runs, the scan that built the
experiment pool (Section 13), the compilations of the diagnostic programs, and the inventory and
probe scripts.

Cross-check: phase D retired 34526936856517 AArch64 instructions in total (Appendix C.3), that is
469 per pair including every load, store, branch and loop overhead of all threads, fewer than
the 606 traced data-path operations per pair.

Phase B and compilation are charged at 256 word operations per retired AArch64 instruction (H3).

## 10. Memory and advice

Inventory (bytes; `mem_inventory.py`, Appendix B.12, output in Appendix C.6). Code: Python
framework and CryptoMiniSat files mapped by the phase-B process 19909328, imported Python
module files 1268767, system libraries mapped from the OS 4129840, the r5search
binary 51128, our sources 35335. Tables (inside the process): L rows 380184, L^-1 rows
398360, affine-subspace table 871888, the 800,000-entry beta1 order 163200056 (estimate),
the SAT instance (inside the measured footprint). Intermediate files: linear_cache.txt 1251723, space.txt 18690, connector.json 2378, chain.log 317, search.out 601. Advice: the
stored pair 270 and the trail text 850. Measured peaks: phase B maximum RSS 224526336 (instrumented
re-execution 235700224) and lifetime maximum physical footprint 219775792; phase D maximum RSS 2015232 (binary, basis, 10 stacks).

Bound: phase B's RSS plus every code file, intermediate file and the advice, counted again even
where the RSS already contains them, is 262369451 bytes = 2^27.97, below 2^29, which we
claim. Phase D runs after phase B and needs less.

## 11. Heuristics

- H1-public-trail (score-critical). Trail core No. 3 (Appendix B.6, GLL+20 Table 9) is public
  algorithm text that C reads without charging its original search (Section 5.1 gives the argument).
  Its 850 bytes are counted as advice. Limitation: if the search must be charged, the bound rises by
  its cost; Section 5.1 cites a public executed search for this core capped at 2^38.82 units, which
  would give 2^39.45.
- H2-op-accounting (score-critical). For our C program the traced per-event constants of Section
  7.1, times 4 for memory traffic, bound its primitive word operations. Evidence: the counting twin
  executes the same loop on the committed space, reproduces the collision and the pass count, and
  counts in the organizer's convention; the event counts are executed counts. Limitation: the twin
  traces data-path operations, not memory accesses; the factor 4 (two loads and a store per
  operation) is our convention for a register-free RAM.
- H3-instruction-conversion (score-critical). For phase B (Python 3.12 with CryptoMiniSat), the
  diagnostic scripts and the compilers, 256 primitive 256-bit word operations per retired AArch64
  instruction bound the work; Section 7.1 gives the per-phase instruction trace. Evidence: every AArch64 integer, load/store and branch instruction acts on at most 128 bits
  of data and is emulated by a small constant number of 256-bit word operations; SIMD instructions
  act on at most 128 bits. Limitation: not verified by an instrumented emulation; the instruction
  counts come from the macOS kernel counters reported by `/usr/bin/time -l` on Apple M4 Pro.
- H4-chain-scope (score-critical). C covers all computation from the tables to the stored pair:
  every prefilter test, every SAT attempt, every thread's pairs, the conversion and the check.
  Development runs (Section 12) used other labels and seeds; C does not read any of their outputs
  and recomputes everything from the trail text and its committed seed. Development fixed only the
  design constants listed in Section 12.
- H5-memory (supporting). Peak memory over C is below 2^29 bytes (Section 10).

## 12. Development work (disclosed, not part of C)

Before writing the commitment we developed the code on this target with other labels and seeds.
Development fixed only these design constants, all visible in the committed source:
- the beta1 order (active rows of alpha1, then the choice tuple) and the linear prefilter;
- the SAT encoding, the DDT-2 bound 90, 8 hash constraints of 16 message bits, the conflict limit
  3,000,000, at most 8 attempts per candidate, and acceptance at DF >= 42;
- the export rule (drop the beta0 direction, keep 48 basis vectors), the round-2 row order, and the
  search parameters (10 threads, chunks of 2^24, cap 2^41, stop at the first collision).
No seed, witness, beta0, space, index or pair from development is an input of C. The two
target-specific facts that development revealed are recomputed and charged in C: that candidate
140 is the first in the order to pass the prefilter (141 tests), and that a witness with DF >= 42
exists (one SAT call). The constants change the cost of C, not whether it succeeds: for example,
without the DDT-2 bound our development witnesses had DF between 9 and 52, so acceptance would have
needed more attempts.

Development ran phase D on a development space for 2^28 + 2^25 pairs (17 Stage-1 passes, no
collision); no development run produced a collision. Its total work was about 7e12 retired
instructions: 3.37e12 measured for the two complete development chain runs, the rest estimated
from CPU time, almost all in early versions that called a difference-only SAT for every candidate
and used no DDT-2 bound. At 256 word operations per instruction this would be about 2^40.3 units.
We do not charge it, because it chose design constants rather than computing any part of the
output (H4); if it were charged, the total would be about 2^40.53.

## 13. Evidence and its status

What the organizer runner can check. The runner recomputes, for every returned message pair, the
5-round digest relation of the selected target (full collision, or digest XOR under a mask). It
cannot see the 2-round connector difference: three more rounds randomise it. A trusted event on a
fresh point of the space would need that point to pass the 24 round-2 conditions (2^-24 per pair)
before any digest bit becomes predictable, and pure Python evaluates about 10^4 pairs per second,
so no event on fresh points fits the 20-second budget. We therefore use two experiments.

- `r5-round2-mask` (`experiments/r5_round2_mask.py`, trusted event `digest-xor-mask`). If a pair has
  difference alpha3 after round 2, then beta3 = L(alpha3) is fixed, alpha4 is one of the 2^19
  row-wise outputs of beta3, and beta4 = L(alpha4) can be active in only 25 of the 64 rows of plane
  y = 0. Hence the digest XOR is zero on the 156 digest bits (lanes 0..3) of the other 39 rows, with
  probability 1; for a pair that does not follow the trail this has probability 2^-156. The mask is
  fc3c11bf7ec6e717fc3c11bf7ec6e717fc3c11bf7ec6e717fc3c11bf7ec6e717. The program rebuilds the connector space from the stored witness exactly as in the
  next experiment, and returns 256 distinct pairs of that space: the pool is every Stage-1 pass in
  the index range [0, 2^33) of the committed space (506 passes, found by an exhaustive
  diagnostic scan that is charged in Section 9), and the organizer seeds of the request determine a
  permutation of the pool that assigns one pool index to each trial. Locally 256 of 256 returned
  pairs satisfied the event. A trusted success certifies that the returned pair, a point of the
  rebuilt space, follows alpha0 -> alpha1 -> alpha2 -> alpha3, that is Lemma 3 and the round-2
  transition, on 256 distinct points chosen by the organizer seeds. The pool indices are ours, not
  fresh; the scan was exhaustive over its range.
- `r5-connector-replay` (`experiments/r5_connector_replay.py`, trusted event `full-collision`).
  It rebuilds the accepted space from the stored witness, beta0, beta1 and alpha1 with the
  committed linearisation seed (ranks 1324 -> 1417 -> 1542, DF 58) and derives the
  certificate pair from the stored Gray-code index; every trial returns that pair, so this
  experiment is a certificate check only. Each trial also draws a fresh point of the space from its
  seed and reports, as untrusted observations, the padding and the exact 2-round difference
  (256 of 256 locally).

Neither experiment makes a cost claim; the runner never infers attack cost.

Supporting only, not used in the bound: under the Markov model the per-pair success probability is
2^-24 (round 2) times 2^-13.2186 (rounds 3-4, exact sum over all 524,288 alpha4 compatible with
beta3; 192 nonzero terms, best single 2^-19), that is 2^-37.2186, so a run needs about 2^37.2 pairs
on average; GLL+20 give 2^-36.70 for this core. Our run needed 2^36.099 pairs, and the
pool scan saw 506 Stage-1 passes (model 512) and no collision in 2^33 pairs (model
expectation 0.054). A fresh run
needs at most our N pairs with probability 1 - exp(-N p) = 0.369 under this model.

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

- H1: if the trail search must be charged, the bound rises by that search's cost; with the public
  executed search cited in Section 5.1 the total would be about 2^39.45.
- H3: the factor 256 is a convention; the instruction-charged lines are 42.0% of the total, so
  even a factor 1024 would add 1.18 bits.
- H4: development runs are disclosed but not charged; Section 12 gives their size and lists the
  constants they fixed. Charged, they would give about 2^40.53.
- Commitment: the commitment is a local git commit, not an external notarisation. The chain is
  deterministic, so its outputs can be reproduced from the label and the source (Section 7.1), but
  that does not prove that no other run took place.
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

B.8 `r5count.c` (SHA-256 5fe27999db24097191e8b0d2f61b2ef90b2b5873b8a3339f456129f6a0c001da)

```c
/* Instrumented single-thread twin of r5search.c (same input, same enumeration and tests).
 * Every data-path operation of the search loop is counted through the macros of
 * keccak_counted.h and the row/loop macros below, per event class:
 *   K_PAIR  per enumerated pair (Gray step, Stage 1 rounds, loop control)
 *   K_ROW   per round-2 row test
 *   K_PASS  per Stage-1 pass (Stage 2: both digests and the compare)
 *   K_CHUNK per chunk start (x_lo from gray(lo))
 * ctz is not a primitive of the RAM model; it is charged 24 operations (6-step binary search,
 * 4 operations per step). Multiplication by 25 for the basis address is charged 4 (shifts, adds).
 * usage: r5count INPUT LO HI CHUNK_LOG2
 */
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef uint64_t u64;
#define ROL(a, n) (((n) == 0) ? (a) : (((a) << (n)) | ((a) >> (64 - (n)))))
enum { K_PAIR, K_ROW, K_PASS, K_CHUNK, NK };
static u64 OPS[NK];
/* functions, not macros, so that every operand expression is evaluated (and counted) once */
static inline u64 CX(int K, u64 a, u64 b) { OPS[K]++; return a ^ b; }
static inline u64 CA(int K, u64 a, u64 b) { OPS[K]++; return a & b; }
static inline u64 CO(int K, u64 a, u64 b) { OPS[K]++; return a | b; }
static inline u64 CN(int K, u64 a) { OPS[K] += 2; return ~a; }
static inline u64 CSHR(int K, u64 a, u64 n) { OPS[K]++; return a >> n; }
static inline u64 CSHL(int K, u64 a, u64 n) { OPS[K]++; return a << n; }
static inline u64 CROL(int K, u64 a, int n) { OPS[K] += 4; return ROL(a, n); }
static inline int CCMP(int K, int e) { OPS[K] += 2; return e; } /* compare and conditional branch */
static inline u64 CADD(int K, u64 a) { OPS[K]++; return a + 1; }
#include "keccak_counted.h"

static const u64 RC[5] = {0x0000000000000001ULL, 0x0000000000008082ULL, 0x800000000000808AULL,
                          0x8000000080008000ULL, 0x000000000000808BULL};
static u64 X0[25], B0[25];
static u64 (*BASIS)[25];
static int NBASIS, NCOND, CY[16], CZ[16];
static uint32_t CMASK[16];

static void read_lanes(FILE *f, u64 *v) {
    for (int l = 0; l < 25; l++)
        if (fscanf(f, "%" SCNx64, &v[l]) != 1) { fprintf(stderr, "bad input\n"); exit(1); }
}

static void digest_from_x_c(const u64 *x, u64 *dg) {
    u64 a[25], b[25];
    CHI_IOTA_C(x, a, RC[0], K_PASS);
    for (int r = 1; r < 5; r++) {
        THETA_RHOPI_C(a, b, K_PASS);
        CHI_IOTA_C(b, a, RC[r], K_PASS);
    }
    memcpy(dg, a, 4 * sizeof(u64));
}

int main(int argc, char **argv) {
    if (argc < 5) return 1;
    FILE *f = fopen(argv[1], "r");
    read_lanes(f, X0);
    read_lanes(f, B0);
    if (fscanf(f, "%d", &NBASIS) != 1) return 1;
    BASIS = calloc(NBASIS, sizeof *BASIS);
    for (int k = 0; k < NBASIS; k++) read_lanes(f, BASIS[k]);
    if (fscanf(f, "%d", &NCOND) != 1) return 1;
    for (int c = 0; c < NCOND; c++)
        if (fscanf(f, "%d %d %" SCNx32, &CY[c], &CZ[c], &CMASK[c]) != 3) return 1;
    fclose(f);
    u64 LO = strtoull(argv[2], 0, 0), HI = strtoull(argv[3], 0, 0), CH = 1ULL << atoi(argv[4]);
    u64 pairs = 0, pass = 0, coll = 0, rows = 0, chunks = 0, first = UINT64_MAX;
    u64 x[25], a[25], b[25];
    for (u64 lo = LO; lo < HI; lo += CH) {
        u64 hi = lo + CH < HI ? lo + CH : HI;
        chunks++;
        u64 g = lo ^ (lo >> 1);
        OPS[K_CHUNK] += 2;
        memcpy(x, X0, sizeof x);
        for (int k = 0; k < NBASIS; k++) {
            if (CCMP(K_CHUNK, (CA(K_CHUNK, CSHR(K_CHUNK, g, k), 1)) != 0))
                for (int l = 0; l < 25; l++) x[l] = CX(K_CHUNK, x[l], BASIS[k][l]);
            OPS[K_CHUNK] += 3; /* k++, compare, branch */
        }
        for (u64 i = lo; i < hi; i++) {
            if (CCMP(K_PAIR, i != lo)) {
                OPS[K_PAIR] += 24 + 4; /* ctz emulation, basis address */
                const u64 *bv = BASIS[__builtin_ctzll(i)];
                for (int l = 0; l < 25; l++) x[l] = CX(K_PAIR, x[l], bv[l]);
            }
            pairs = CADD(K_PAIR, pairs);
            CHI_IOTA_C(x, a, RC[0], K_PAIR);
            THETA_RHOPI_C(a, b, K_PAIR);
            CHI_IOTA_C(b, a, RC[1], K_PAIR);
            THETA_RHOPI_C(a, b, K_PAIR);
            int ok = 1;
            for (int c = 0; c < NCOND; c++) {
                OPS[K_ROW] += 3; /* c++, compare, branch */
                int y = CY[c], z = CZ[c];
                u64 v = CA(K_ROW, CSHR(K_ROW, b[5 * y], z), 1);
                v = CO(K_ROW, v, CSHL(K_ROW, CA(K_ROW, CSHR(K_ROW, b[5 * y + 1], z), 1), 1));
                v = CO(K_ROW, v, CSHL(K_ROW, CA(K_ROW, CSHR(K_ROW, b[5 * y + 2], z), 1), 2));
                v = CO(K_ROW, v, CSHL(K_ROW, CA(K_ROW, CSHR(K_ROW, b[5 * y + 3], z), 1), 3));
                v = CO(K_ROW, v, CSHL(K_ROW, CA(K_ROW, CSHR(K_ROW, b[5 * y + 4], z), 1), 4));
                rows++;
                if (!CCMP(K_ROW, CA(K_ROW, CSHR(K_ROW, (u64)CMASK[c], v), 1))) { ok = 0; break; }
                OPS[K_ROW]++; /* rowpass counter */
            }
            if (CCMP(K_PAIR, ok)) {
                pass++;
                u64 x2[25], d1[4], d2[4];
                for (int l = 0; l < 25; l++) x2[l] = CX(K_PASS, x[l], B0[l]);
                digest_from_x_c(x, d1);
                digest_from_x_c(x2, d2);
                int eq = 1;
                for (int l = 0; l < 4; l++) eq &= CCMP(K_PASS, d1[l] == d2[l]);
                if (eq) { coll++; if (i < first) first = i; }
            }
            OPS[K_PAIR] += 3 + 3; /* i++, i<hi compare+branch; (pairs & 4095)==0 and, compare, branch */
        }
    }
    printf("pairs %" PRIu64 " rows %" PRIu64 " pass %" PRIu64 " coll %" PRIu64 " chunks %" PRIu64 " first %" PRIu64 "\n",
           pairs, rows, pass, coll, chunks, first == UINT64_MAX ? 0 : first);
    printf("ops pair %" PRIu64 " row %" PRIu64 " pass %" PRIu64 " chunk %" PRIu64 "\n",
           OPS[K_PAIR], OPS[K_ROW], OPS[K_PASS], OPS[K_CHUNK]);
    printf("per_event pair %.4f row %.4f pass %.4f chunk %.4f\n", (double)OPS[K_PAIR] / pairs,
           (double)OPS[K_ROW] / rows, pass ? (double)OPS[K_PASS] / pass : 0.0, (double)OPS[K_CHUNK] / chunks);
    return 0;
}
```

B.9 `keccak_counted.h` (SHA-256 833068d3e4a7343c37853c8cc562000f6df2827ab03155e67468ece3cb3c566e)

```c
/* Counted twins of keccak_unrolled.h: every data-path operation goes through a counting macro.
   Convention of scripts/reference_operation_costs.py: XOR/AND/OR/shift 1, NOT 2 (invert and
   64-bit mask), rotation 4 (two shifts, OR, mask). */
#define THETA_RHOPI_C(a, b, K) do { \
    u64 c0 = CX(K, CX(K, CX(K, CX(K, a[0], a[5]), a[10]), a[15]), a[20]); \
    u64 c1 = CX(K, CX(K, CX(K, CX(K, a[1], a[6]), a[11]), a[16]), a[21]); \
    u64 c2 = CX(K, CX(K, CX(K, CX(K, a[2], a[7]), a[12]), a[17]), a[22]); \
    u64 c3 = CX(K, CX(K, CX(K, CX(K, a[3], a[8]), a[13]), a[18]), a[23]); \
    u64 c4 = CX(K, CX(K, CX(K, CX(K, a[4], a[9]), a[14]), a[19]), a[24]); \
    u64 d0 = CX(K, c4, CROL(K, c1, 1)); \
    u64 d1 = CX(K, c0, CROL(K, c2, 1)); \
    u64 d2 = CX(K, c1, CROL(K, c3, 1)); \
    u64 d3 = CX(K, c2, CROL(K, c4, 1)); \
    u64 d4 = CX(K, c3, CROL(K, c0, 1)); \
    b[0] = CROL(K, CX(K, a[0], d0), 0); \
    b[10] = CROL(K, CX(K, a[1], d1), 1); \
    b[20] = CROL(K, CX(K, a[2], d2), 62); \
    b[5] = CROL(K, CX(K, a[3], d3), 28); \
    b[15] = CROL(K, CX(K, a[4], d4), 27); \
    b[16] = CROL(K, CX(K, a[5], d0), 36); \
    b[1] = CROL(K, CX(K, a[6], d1), 44); \
    b[11] = CROL(K, CX(K, a[7], d2), 6); \
    b[21] = CROL(K, CX(K, a[8], d3), 55); \
    b[6] = CROL(K, CX(K, a[9], d4), 20); \
    b[7] = CROL(K, CX(K, a[10], d0), 3); \
    b[17] = CROL(K, CX(K, a[11], d1), 10); \
    b[2] = CROL(K, CX(K, a[12], d2), 43); \
    b[12] = CROL(K, CX(K, a[13], d3), 25); \
    b[22] = CROL(K, CX(K, a[14], d4), 39); \
    b[23] = CROL(K, CX(K, a[15], d0), 41); \
    b[8] = CROL(K, CX(K, a[16], d1), 45); \
    b[18] = CROL(K, CX(K, a[17], d2), 15); \
    b[3] = CROL(K, CX(K, a[18], d3), 21); \
    b[13] = CROL(K, CX(K, a[19], d4), 8); \
    b[14] = CROL(K, CX(K, a[20], d0), 18); \
    b[24] = CROL(K, CX(K, a[21], d1), 2); \
    b[9] = CROL(K, CX(K, a[22], d2), 61); \
    b[19] = CROL(K, CX(K, a[23], d3), 56); \
    b[4] = CROL(K, CX(K, a[24], d4), 14); \
} while (0)
#define CHI_IOTA_C(b, a, rc, K) do { \
    a[0] = CX(K, b[0], CA(K, CN(K, b[1]), b[2])); \
    a[1] = CX(K, b[1], CA(K, CN(K, b[2]), b[3])); \
    a[2] = CX(K, b[2], CA(K, CN(K, b[3]), b[4])); \
    a[3] = CX(K, b[3], CA(K, CN(K, b[4]), b[0])); \
    a[4] = CX(K, b[4], CA(K, CN(K, b[0]), b[1])); \
    a[5] = CX(K, b[5], CA(K, CN(K, b[6]), b[7])); \
    a[6] = CX(K, b[6], CA(K, CN(K, b[7]), b[8])); \
    a[7] = CX(K, b[7], CA(K, CN(K, b[8]), b[9])); \
    a[8] = CX(K, b[8], CA(K, CN(K, b[9]), b[5])); \
    a[9] = CX(K, b[9], CA(K, CN(K, b[5]), b[6])); \
    a[10] = CX(K, b[10], CA(K, CN(K, b[11]), b[12])); \
    a[11] = CX(K, b[11], CA(K, CN(K, b[12]), b[13])); \
    a[12] = CX(K, b[12], CA(K, CN(K, b[13]), b[14])); \
    a[13] = CX(K, b[13], CA(K, CN(K, b[14]), b[10])); \
    a[14] = CX(K, b[14], CA(K, CN(K, b[10]), b[11])); \
    a[15] = CX(K, b[15], CA(K, CN(K, b[16]), b[17])); \
    a[16] = CX(K, b[16], CA(K, CN(K, b[17]), b[18])); \
    a[17] = CX(K, b[17], CA(K, CN(K, b[18]), b[19])); \
    a[18] = CX(K, b[18], CA(K, CN(K, b[19]), b[15])); \
    a[19] = CX(K, b[19], CA(K, CN(K, b[15]), b[16])); \
    a[20] = CX(K, b[20], CA(K, CN(K, b[21]), b[22])); \
    a[21] = CX(K, b[21], CA(K, CN(K, b[22]), b[23])); \
    a[22] = CX(K, b[22], CA(K, CN(K, b[23]), b[24])); \
    a[23] = CX(K, b[23], CA(K, CN(K, b[24]), b[20])); \
    a[24] = CX(K, b[24], CA(K, CN(K, b[20]), b[21])); \
    a[0] = CX(K, a[0], (rc)); \
} while (0)
```

B.10 `r5chain_instr.py` (SHA-256 60e6fef4b4645c0f3fdb2b614c4a1daa90e1c749f3599c378dbc9947a5413deb)

```python
"""INSTRUMENTED twin of r5chain.py (diagnostic re-execution; identical except for the counters).

Construction chain C, phases P and B1-B4, for 5-round SHA3-256 (135-byte messages).

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


from rusage_probe import counters  # noqa: E402
C0 = counters()


def log(*a):
    ins, cyc, foot, maxfoot = counters()
    msg = " ".join(str(v) for v in a)
    msg += " | instr %d cycles %d footprint %d maxfootprint %d" % (ins - C0[0], cyc - C0[1], foot, maxfoot)
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

B.11 `rusage_probe.py` (SHA-256 c873e2cd261aa4c28df65fbded1236931416293cac334959482eade1facd7820)

```python
import ctypes, os
_lib = ctypes.CDLL("/usr/lib/libproc.dylib")
_buf = ctypes.create_string_buffer(512)


def counters():
    """(instructions, cycles, phys_footprint, lifetime_max_phys_footprint) of this process."""
    if _lib.proc_pid_rusage(os.getpid(), 4, _buf) != 0:
        raise OSError("proc_pid_rusage")
    q = lambda i: int.from_bytes(_buf.raw[16 + 8 * i:24 + 8 * i], "little")
    return q(29), q(30), q(7), q(28)


if __name__ == "__main__":
    a = counters()
    s = 0
    for i in range(10 ** 7):
        s += i
    b = counters()
    print(a, b, b[0] - a[0])
```

B.12 `mem_inventory.py` (SHA-256 10ae4226fe83c875adf54045ba1e284fa03a4729b1a2d732f105e1a941929c78)

```python
"""Memory inventory for construction C: code, tables, intermediate files and advice (bytes)."""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pycryptosat  # noqa: E402
import r5conn  # noqa: E402, F401  (imports r5core, builds the tables)
import r5core as K  # noqa: E402

inv = {}
mods = {}
for name, m in list(sys.modules.items()):
    f = getattr(m, "__file__", None)
    if f and os.path.isfile(f):
        mods[os.path.realpath(f)] = os.path.getsize(f)
lsof = subprocess.run(["lsof", "-p", str(os.getpid())], capture_output=True, text=True).stdout.split("\n")
mapped = {}
for ln in lsof:
    parts = ln.split()
    if len(parts) >= 9 and parts[3] == "txt" and os.path.isfile(parts[-1]):
        p = os.path.realpath(parts[-1])
        mapped[p] = os.path.getsize(p)
system = {p: s for p, s in mapped.items() if p.startswith("/System/") or p.startswith("/usr/lib/")}
own = {p: s for p, s in mapped.items() if p not in system}
inv["code_python_and_solver_mapped_files"] = sum(own.values())
inv["code_python_module_files"] = sum(s for p, s in mods.items() if p not in own)
inv["code_system_libraries_shared_by_os"] = sum(system.values())
inv["code_r5search_binary"] = os.path.getsize(os.path.join(HERE, "r5search"))
inv["code_our_sources"] = sum(os.path.getsize(os.path.join(HERE, f)) for f in
                              ("r5core.py", "r5conn.py", "r5chain.py", "r5search.c", "keccak_unrolled.h"))
inv["table_L_rows"] = sum(sys.getsizeof(v) for v in K.LROWS) + sys.getsizeof(K.LROWS)
inv["table_Linv_rows"] = sum(sys.getsizeof(v) for v in K.LINV) + sys.getsizeof(K.LINV)
inv["table_affine_subspaces"] = sum(sys.getsizeof(t) + sum(sys.getsizeof(e) for e in t[2]) + sys.getsizeof(t[3])
                                    for t in r5conn.AFFX) if hasattr(r5conn, "AFFX") else \
    sum(sys.getsizeof(t) + sum(sys.getsizeof(e) for e in t[2]) + sys.getsizeof(t[3]) for t in r5conn.AFF)
inv["table_beta1_order_list_estimate"] = 800000 * (sys.getsizeof((0, (0,) * 9)) + sys.getsizeof((0,) * 9) + 28) + \
    sys.getsizeof([0] * 800000)
files = {"linear_cache.txt": os.path.join(HERE, "linear_cache.txt")}
for f in ("space.txt", "connector.json", "chain.log", "search.out"):
    files[f] = os.path.join(HERE, "run1", f)
inv["intermediate_files"] = {k: os.path.getsize(v) for k, v in files.items()}
inv["advice_stored_pair"] = 270
inv["advice_trail_text"] = os.path.getsize(os.path.join(HERE, "trail_core3.txt"))
inv["phaseB_measured_max_rss"] = 235700224
inv["phaseB_measured_lifetime_max_phys_footprint"] = 219775792
inv["phaseD_measured_max_rss"] = 2015232
total_excl_system = (inv["code_python_and_solver_mapped_files"] + inv["code_python_module_files"] + inv["code_r5search_binary"]
                     + inv["code_our_sources"] + sum(inv["intermediate_files"].values()) + inv["advice_stored_pair"]
                     + inv["advice_trail_text"] + inv["phaseB_measured_max_rss"])
inv["total_peak_bound_excluding_os_shared_libraries"] = total_excl_system
inv["total_peak_bound_including_os_shared_libraries"] = total_excl_system + inv["code_system_libraries_shared_by_os"]
inv["mapped_own_files"] = own
print(json.dumps(inv, indent=1))
```

B.13 `r5passes.c` (SHA-256 cd8b771cdbbfe56b22b4196a2b9df87d1086282779dbbdcab3412ab464973a31)

```c
/* DIAGNOSTIC twin of r5search.c: identical search, but prints every Stage-1 pass index
 * ("PASS idx") and never stops early. Used only to build the organizer experiment's pool.
 *
 * Online stage for the 5-round SHA3-256 connector space.
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
                pthread_mutex_lock(&mu);
                printf("PASS %" PRIu64 "\n", i);
                pthread_mutex_unlock(&mu);
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

C.5 counting twin (`count-chunk.out`, `count-first.out`, `count-chunk-time.txt`)

```
pairs 16777216 rows 17978020 pass 2 coll 1 chunks 1 first 73686378480
ops pair 10166992843 row 450651306 pass 4806 chunk 538
per_event pair 606.0000 row 25.0668 pass 2403.0000 chunk 538.0000
pairs 16777216 rows 17978683 pass 1 coll 0 chunks 4 first 0
ops pair 10166992684 row 450668543 pass 2403 chunk 1502
per_event pair 606.0000 row 25.0668 pass 2403.0000 chunk 375.5000
        0.57 real         0.33 user         0.00 sys
             1769472  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
                 287  page reclaims
                   1  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   0  messages sent
                   0  messages received
                   0  signals received
                   2  voluntary context switches
                 182  involuntary context switches
          8585600442  instructions retired
          1314386790  cycles elapsed
             1294696  peak memory footprint
```

C.6 memory inventory (`mem_inventory.json`)

```
{
 "code_python_and_solver_mapped_files": 19909328,
 "code_python_module_files": 1268767,
 "code_system_libraries_shared_by_os": 4129840,
 "code_r5search_binary": 51128,
 "code_our_sources": 35335,
 "table_L_rows": 380184,
 "table_Linv_rows": 398360,
 "table_affine_subspaces": 871888,
 "table_beta1_order_list_estimate": 163200056,
 "intermediate_files": {
  "linear_cache.txt": 1251723,
  "space.txt": 18690,
  "connector.json": 2378,
  "chain.log": 317,
  "search.out": 601
 },
 "advice_stored_pair": 270,
 "advice_trail_text": 850,
 "phaseB_measured_max_rss": 235700224,
 "phaseB_measured_lifetime_max_phys_footprint": 219775792,
 "phaseD_measured_max_rss": 2015232,
 "total_peak_bound_excluding_os_shared_libraries": 258239611,
 "total_peak_bound_including_os_shared_libraries": 262369451
}
```

C.7 instrumented phase-B re-execution (`run1b-time.txt`)

```
       13.14 real        12.80 user         0.14 sys
           235700224  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
               17594  page reclaims
                  74  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   0  messages sent
                   0  messages received
                   0  signals received
                  13  voluntary context switches
                8547  involuntary context switches
        282494312169  instructions retired
         53016910946  cycles elapsed
           219775792  peak memory footprint
```

C.8 pool scan (`passes.out` summary lines, `passes-time.txt`)

```
pairs 8589934592 pass 506 coll 0
rowpass 536855424 67126848 8390806 2096813 524380 131489 32962 8250 2072 506

resource-guard: acquired task=claude-r5 label=r5 pass pool memory_free=45% required=0%
       19.78 real       175.71 user         1.14 sys
             1933312  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
                 319  page reclaims
                   1  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   0  messages sent
                   0  messages received
                   0  signals received
                   2  voluntary context switches
              252047  involuntary context switches
       3995680692835  instructions retired
        628900928778  cycles elapsed
             1474920  peak memory footprint
```
