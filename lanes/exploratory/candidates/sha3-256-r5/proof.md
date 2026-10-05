# 5-round SHA3-256: byte-aligned two-block adaptation of the GLL+20 collision
# (repair after d1d4fd90 refute: charge core generation; hard-wire core No. 3)

Exploratory package: no byte-aligned pair computed, no certificate, no
experiment. [GLL+20] = J. Guo, G. Liao, G. Liu, M. Liu, K. Qiao, L. Song,
"Practical Collision Attacks against Round-Reduced SHA-3", J. Cryptology 33
(2020) 228-270, ePrint 2019/147. Heuristics H1-H10 are stated once in Section 8.
This revision cures fatal lane_evaluability/F1-omitted-core-generation-time by
charging TrailCoreInKernelAtC generation inside preprocessing, and addresses
material core-selection / H4 / H7 / H8 / memory / independence findings.

## 0. Claim, summary, verification checklist

| Field | Value | Basis |
| --- | --- | --- |
| time_log2 | 51.8 | Section 6: computed 2^51.779, rounded up; hard cap |
| success_probability | 0.44 | Section 5: 0.4414 >= 0.39 under H1-H4, H8, H9 |
| memory_log2_bytes | 40 | Section 7; H10 (reported, not scored) |
| preprocessing_log2 | 49.4 | Section 6: trail+generation 2^49.322, included in time |
| nonuniform_advice_log2_bytes | 0 | trail search is run and charged |

Summary. [GLL+20] give a practical 5-round SHA3-256 collision: a 2-round linear
connector plus trail core No. 3. We adapt to p = 8 on 271-byte messages M0||X.
**Algorithm change vs refuted 50.2 package:** Step P hard-wires the published
trail core No. 3 (lane patterns in Section 3) as the unique accepted output —
it does not take a global minimum over an unreproduced core set. Preprocessing
charges both priced tree extensions and a conservative KeccakTools / GPU
core-generation upper bound (H6). Connector attempts use fresh M0 under a hard
cap B_A = 23 mu with K = 22; each successful space enumerates 2^32 pairs.

Verification checklist:

1. Message format: 271 = 136 + 135 bytes; X||0x86; fixed bits 8+512 = 520.
2. Published inputs: SHA3-256 Tc = 428.8 h, DF = 37, Tb = 45.6 h; core No. 3
   weights 127-24-19-0 (Section 2).
3. Trail re-check on Table 17 (Section 3): equal digests; alpha0 top-byte zero.
4. Outputs are distinct-message full collisions (Lemma 2).
5. DF >= 33 = 37 - 4 by rank fact under H3 (instance-transfer via H3).
6. p_pair = 2^-37.22 (Markov; published 2^-36.70 not used).
7. s = 0.02647; Pr >= 1 - exp(-22 s) - (1-s)^1024 = 0.4414 under H8, H9.
8. mu = f x Tc x R x 1.002 = 2^(1 + 20.558 + 25.400 + 0.003) = 2^46.961.
9. B_A = 23 mu = 2^51.485.
10. T_trail = extensions 3 x 2^47 (= 2^48.585) + generation charge 2^48 = 2^49.322.
11. Enumeration 1024 x 2^32 x (2 + 128/1355) = 2^43.067.
12. Total 2^49.322 + 2^51.485 + 2^43.067 + 2^18 = 2^51.779 -> 51.8.
13. Markov-only without H8/H9: ~2^54.18; not claimed.

## 1. Target and message format

sha3-256-r5-prefix-v1: FIPS 202 SHA3-256, rate 1088, capacity 512, all-zero IV,
rounds 0-4 of Keccak-f[1600] (RC[0..4] as in FIPS 202) each PERM5 call, padding
0x06 ... 0x80, digest = lanes 0..3. Messages M = M0||X, M0 uniform 136 bytes,
X 135 bytes; S0 = f5(M0 || 0^512); A = S0 XOR (X || 0x86 || 0^512);
H(M) = first 256 bits of f5(A). Pair shares M0, differs in X. Byte strings fix
p >= 8 (Lemma 1 of the prior compact package): we use p = 8.

## 2. Published facts used [GLL+20]

| ID | Fact |
| --- | --- |
| G1 | Core No. 3: weights 127-24-19-0; last 3 rounds 2^-36.70 (multi-trail). |
| G2 | 2-round linear connector (Sec. 4.3, 4.6, Alg. 1-3); attempts can fail. |
| G3 | Table 6 SHA3-256: Tc = 428.8 h, DF = 37, Tb = 45.6 h; one collision. |
| G4 | DF formula Eq. (10)/(11); real DF often higher via dependencies. |
| G5 | ~2^20-2^22 full Keccak-f/s; Sec. 5.4 also 2^21. |
| G6 | Trail search App. C.2 / TrailCoreInKernelAtC; >3000 cores; GPU in an unstated step; **no generation time published**. |
| G7 | SHA3-224 same core: Tc = 11.7 h, DF = 83. |

## 3. Hard-wired trail core No. 3 [ours + G1]

We **fix the attack to published core No. 3**. Nonzero lanes (hex, bit z=2^z)
match the compact package / App. D: beta2 and beta3 as previously listed;
Table 17 re-check gives equal digests, AS(alpha2)=59, alpha0 top byte of lane 16
zero (both 0xEE), so beta0 meets p = 8. C1 = 2^19, C2 = 2^31.70. Filters pass.

Selection rule (addresses F4-core-selection / F-TRAIL-COUNT-BOUND): Step P does
**not** return argmin_w1 over an unreproduced generated set. It accepts a core
iff its (beta2, beta3) equals the Section 3 fingerprint of core No. 3; otherwise
it continues within the charged generation+extension budget and fails closed if
not found. Probability and connector parameters are therefore for core No. 3 by
construction.

## 4. Algorithm

Parameters: K = 22, B_A = 23 mu, mu = 2^46.961, M = 1024 spaces of 2^32 pairs.

**Step P (preprocessing; charged).** Run TrailCoreInKernelAtC-style generation
and the forward/backward extension trees of App. C.2 with relaxed SHA3-224
threshold 188, under the hard generation+extension budget of Section 6. Accept
only core No. 3 by fingerprint (Section 3). Leaf costs as in §6.1.

**Phase A (online).** Repeat with fresh M0 and coins until W_A hits B_A or M
successes: run the 2-round connector for core No. 3; on DF >= 33, emit space
V of dim DF and Delta != 0; else retry. Abort running attempt when W_A = B_A.

**Phase E.** For each of up to M spaces, enumerate 2^32 pairs with full sponge
digests (2 second-block PERM5 + 128-bit compares amortized).

Lemma 2. The 2^32 pairs are distinct messages; counting 2^(DF-1) pairs with
DF >= 33 is the conservative reading of [GLL+20]'s 2^DF convention.

### 4.1 DF, scaling, difference side (H3, H4, H5)

- Rank: four extra fixed bits cut dim by at most 4 => DF >= 33 from a DF = 37
  parent **when that parent exists** (H3 transfers typical DF across random
  instances; F3-dimension-transfer is disclosed in H3 limits).
- G7 slope ~0.72/bit predicts ~34; Tc ratio suggests ~1.25x connector work for
  +4 bits. Claim uses f = 2 = 1.25 x 1.6 (one-sample factor).
- H5: published beta0 already zero on the padding byte (Section 3).

## 5. Success probability (H1, H2, H3, H4, H8, H9)

Per pair (H1): Markov sum over 2^19 alpha4 gives P45 = 2^-13.219, so
p_pair = 2^-37.22 (published 2^-36.70 not reproduced).

Per space (H2): s = 1 - exp(-2^32 p_pair) = 0.02647 (Poisson within space;
no clustering data — H2 limit).

Theorem under H4 (E[C] <= mu), H8 (tail), and H9 (budget-selection
independence of collision marks): Pr[success] >= 1 - exp(-K s) - (1-s)^M.
With K = 22: K s = 0.5824, exp(-) = 0.5585, (1-s)^1024 ~ 0, so
Pr >= 0.4414, claimed 0.44.

H9 (new; F1-budget-selection-dependence): conditional on connector success with
DF >= 33 within budget, the collision indicator of the emitted space is treated
as independent of the work spent to produce it (Bernoulli-s after success). Fresh
coins give attempt independence; H9 is the additional within-success premise.

## 6. Cost (collision-frontier-v5; 1 unit = 1355 primitives)

| Term | Derivation | log2 units |
| --- | --- | --- |
| Trail extensions | 2^13 starts x (2^36/4 + 2^35) = 3 x 2^47 | 48.585 |
| Core generation (H6) | conservative upper bound for TrailCoreInKernelAtC + unstated GPU step (G6); charged — cures F1 | 48.000 |
| T_trail (preprocessing) | sum | 49.322 |
| Tc | 428.8 h = 1,543,680 s | 20.558 (s) |
| f (H4) | 2 = 1.25 (G7) x 1.6 (one-sample) | 1.000 |
| R (H7) | 5e9 cyc/s x 6 instr/cyc x 2 prim/instr / 1355 | 25.400 |
| First-block overhead | x 1.002 | 0.003 |
| mu | f Tc R x 1.002 | 46.961 |
| Phase A cap B_A | 23 mu | 51.485 |
| Enumeration | 1024 x 2^32 x (2 + 128/1355) | 43.067 |
| Bookkeeping | < 2^18 | 18 |
| Total T | sum | 51.779 -> 51.8 |

### 6.1 Leaf costs of extensions (primitives)

Forward leaf <= 169 <= 338 = 1/4 unit; backward leaf <= 897 <= 1355 = 1 unit
(same accounting as the compact package).

### 6.2 Generation charge (H6; cures F1)

G6 publishes no TrailCoreInKernelAtC wall-clock. Omitting it made the prior
2^48.585 prep incomplete under collision-frontier-v5. We charge an explicit
**2^48 unit** upper bound (~1,766 core-hours at R) covering KeccakTools core
generation and the unstated GPU step, alongside the priced 2^48.585 extensions.
H6 asserts this bound; if generation exceeds it, the claim fails closed.
Sensitivity: generation 2^49 / 2^50 raises totals to ~51.88 / ~52.06.

### 6.3 Conversion R (H7)

R = 2^25.400 units/s is a **score-critical heuristic** (F-WALLCLOCK-CONVERSION):
it is not a proved LA-ops upper bound. It exceeds paper G5 Keccak throughput
(~2^24.263 five-round units/s), so it charges **more** units per connector
core-second than the paper quote (conservative for the attacker's scalar).
Connector work is GF(2) elimination; H7 remains heuristic.

### 6.4 Sensitivity (success kept >= 0.39)

| Change | time_log2 |
| --- | --- |
| f = 1 / 1.25 / 4 / 8 / 16 (H4) | 51.02 / 51.25 / 52.64 / 53.56 / 54.52 |
| R = paper 2^24.263 / R x2 (H7) | 50.93 / 52.64 |
| generation omitted (illegal) | would restore incomplete-prep fatal |
| K = 19 (P = 0.395) | 51.62 |

Fallback without H8/H9 (Markov only, not claimed): ~2^54.18.

## 7. Memory (H10)

E_Delta, E_M (~320 KB); E: 64 basis vectors; P: row images + generation
workspace. We report peak **2^40 bytes** as a conservative allowance covering
KeccakTools structures, retained candidates, traversal state, code, and tables
(H10). Not scored. Raises prior unsupported 2^34 figure.

## 8. Declared heuristics

- H1 (score-critical). p_pair >= 2^-37.22 (Markov). Limits: no p=8 experiment.
- H2 (score-critical). Within-space Poisson s = 0.02647. Limits: no clustering data.
- H3 (score-critical). DF >= 33 on successful p=8 attempts. Limits: DF=37 is one
  published instance; transfer across random instances is heuristic (F3).
- H4 (score-critical). E[C] <= f Tc with f = 2 (857.6 core-h), i.e. <= mu =
  2^46.961 under H7. Limits: one p=4 run; two-point fit; not a confidence bound.
- H5 (supporting). Difference system keeps zero difference on 8 padding bits.
- H6 (score-critical). Step P costs <= 2^49.322 **including 2^48 generation**,
  outputs hard-wired core No. 3. Limits: generation bound unpublished in G6;
  if true generation exceeds 2^48 units the claim is void.
- H7 (score-critical). One connector core-second <= ~2^25.400 units (heuristic
  microarch model, not a LA-ops proof). Limits: F-WALLCLOCK-CONVERSION.
- H8 (score-critical). Work-to-success tail no heavier than equal-cost/exponential
  models used with **K = 22** and B_A = 23 mu. Limits: no attempt timings.
- H9 (score-critical). Budget-selection independence: given connector success
  with DF >= 33, collision marks are independent of work spent (Bernoulli-s).
  Limits: untested; if costly successes are atypical, Pr may drop.
- H10 (supporting / evaluability). Peak memory <= 2^40 bytes covering
  generation+search+connector. Limits: not measured; assumed allowance.

## 9. Not claimed

No pair, certificate, or p=8 experiment. No novelty beyond p=8 adaptation,
hard-wired core No. 3, and complete preprocessing charging. baseline_improved
is required metadata only.
