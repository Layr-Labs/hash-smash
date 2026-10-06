# SHA-256/32 ordinary collision: truncated CRYPTO 2026 35-step attack with the characteristic search run until it output the published characteristic, measured

## 0. Claim

The track is `sha256-r32-exploratory`, profile `sha256-r32-prefix-v1`, cost model `collision-frontier-v5`. One
32-step compression costs 1 unit and every other primitive word operation costs 1/C with C = 2224.

The algorithm is a classical two-block attack. It outputs two distinct 128-byte messages whose complete 32-step
SHA-256 hashes are equal: standard IV, standard padding, all 256 bits. Its bounds:
- success probability >= 0.42 (computed 0.4326, Section 7);
- time <= 2^47.6 (computed 2^47.532, Section 8);
- preprocessing <= 2^47.2 (computed 2^47.181, itemised in Section 8);
- memory <= 2^35 bytes (computed 2^34.732, Section 9);
- nonuniform advice < 2^13 bytes.

The certificate is yudduy's #227 pair (credited), included only as organizer-verified corroboration that the
truncated route yields complete-target collisions; the score is the algorithm's charged work, not the pair.

Sources and credit:
- **S.** Y. Li, F. Liu, G. Wang, J. Shi, "Pushing the Limit of Memory-efficient Collision Attack Framework for SHA-2",
  CRYPTO 2026, ePrint 2026/1080: Fig. 6, Table 3, the three-step attack and the four-step characteristic search.
  The solver model is from Li, Liu, Wang, EUROCRYPT 2024 (ePrint 2024/349), github.com/Peace9911/sha_2_attack.
- **#26/#33 (winglock):** the truncation, the table and Step-2/3 tests, the q method and run data, E16[29] = E17[29];
  re-implemented and re-measured here. **#134 (jagnani73):** the measured-rerun method. **#31 (hybridnoise):** search
  memory must be charged; lower relaxed optima are contradictory. **#227 (yudduy):** the published
  32-step witness of this route, cited as corroboration only.

Provenance (r32 track): our earlier submission #296 ran 57 calls of S's search with a callgrind
calibration and charged the unfinished part as an allowance; #367 (Th0rgal) uses the same measured figures and
#377 (jackzampolin) adapts #367. This package continues the run until it outputs Fig. 6 (Section 6), and adopts
kappa = 2^23 (#367) and T = 2^45 (#377), each re-justified from our own data (Sections 6, 7).

## 1. Notation

Words are 32-bit and + is mod 2^32. Sigma0, Sigma1, sigma0, sigma1, IF and MAJ are as in FIPS 180-4.
W[i] = M[i] for i < 16, and W[i] = sigma1(W[i-2]) + W[i-7] + sigma0(W[i-15]) + W[i-16] for i >= 16.

For a chaining value CV = (a..h), put A[-1..-4] = (a,b,c,d) and E[-1..-4] = (e,f,g,h). Then

```
E[i] = A[i-4] + E[i-4] + Sigma1(E[i-1]) + IF(E[i-1],E[i-2],E[i-3]) + K[i] + W[i]
A[i] = E[i] - A[i-4] + Sigma0(A[i-1]) + MAJ(A[i-1],A[i-2],A[i-3])
```

C_R(CV,M) = CV + (A[R-1..R-4], E[R-1..R-4]). The target applies C_32 to every padded block. The messages are M0||M1
and M0||M1' (128 bytes each), so the third block is the common padding block P (80000000, 0..0, 00000400).

Signed rows (S): position k is bit 31-k; `n` x=0, x'=1; `u` x=1, x'=0; `=` equal; `0`/`1` equal with that value. FL(X) is the n/u mask and D(X) = sum over n of 2^j - sum over u of 2^j. **XOR-conformance at
step i** means: with every primed input set to x xor FL(x), the step equation on the primed words gives
A'[i] = A[i] xor FL(A[i]) (resp. E).

## 2. Characteristic (S, Fig. 6)

Unprimed values are S's M'_1. Rows 23..34 are all `=`.

```
  i   nabla A[i]                        nabla E[i]                        nabla W[i]
-4..-1 all =                            all =
 0-2  ================================  ================================  ================================
  3   ================================  =====1=====011======0======0====  ================================
  4   ==n=============================  ==n0=0=1===100=0==0=1===0==1=0=1  ==n=============================
  5   =====n===n===n=u====n===u==u====  01011u001n=nuu=11000n=1=101u=100  =====u===u==========n===========
  6   ================================  101n=0=1=1=n1111==n0u===n=0n=n=u  ==n=============================
  7   ================================  10u0=1=101==00=n==0=0===0==0=0=0  =======n=======u===u====u=1=u=u=
  8   ================================  uuu1=0=111=0=0=01=1=01==1==1=1=0  ============u=======uu==========
  9   ==========u====================u  11=10n0nuuu00n0u101=n11=u01u=unn  ================================
 10   ================================  un111111001001111=010u=u0=001100  ================================
 11   ====n=========u=u=======u==n====  1011n111100010u1u0111111u=nu1001  ================================
 12   =un===u=n=======n===============  001uuu11uuuuuuuu11n1000n1uuu1001  =====n===n==========u===========
 13   ================================  =n1111uu1n00000u1u0=nnn01111010n  ==u=============================
 14   ==u=============================  =0=100110000000=101=0000=110===0  ================================
 15   ================================  =1====0011===u10001=011===0n===1  ================================
 16   ================================  ======u=n====1==n=====0===01====  ================================
 17   ================================  ======0=0====1==0==========1====  ================================
 18   ================================  ==u===1=0=======1====1==========  ================================
 19   ================================  ==0=============================  ================================
 20   ================================  ==1=============================  =====0=nn=====0=u=1=============
 21   ================================  ================================  ================================
 22   ================================  ================================  ==n=============================
```

S prints `+` at two positions of E10 and E11. We write `=` there; both published messages agree on those bits. The
weights are tw = 22, tE = sum_{14..18} H(nabla E) = 6, tA = 21 and tE4 = sum_{4..18} H(nabla E) = 76.

Two-bit conditions printed by S (X[a,b] = Y[c,d] means X[a] = Y[c] and X[b] = Y[d]):

```
W4[1,8]!=W4[12,25] W4[18]=W4[14] W5[0,1,30]=W5[28,18,9] W6[1,8]=W6[12,25] W6[18]!=W6[14]
W7[22,13,23]!=W7[18,9,8] W7[11,14,20]=W7[22,31,31] W8[0,14,21]=W8[28,25,6] W8[31,23,30,15,22,8]!=W8[27,2,15,26,7,4]
W20[4,31]=W20[6,22] W20[31,30,25,21]!=W20[1,0,16,14] W22[4,31]=W22[6,22] W22[27]!=W22[20]
E4[10]!=E4[15] E5[3,21]=E5[8,8] E6[9,27,9,8]!=E6[23,14,14,27] E6[1,1,23,6]=E6[6,15,10,25] E7[21,10]!=E7[3,15]
E16[28,20,20,6]=E16[1,7,2,11] E16[30,28,10]!=E16[12,10,29] E18[24]!=E18[11] E18[2]=E18[16]
A3[29]=A2[29] A3[29]!=A5[29] A3[26,4]=A4[26,4] A3[22,18,16,11,7]!=A4[22,18,16,11,7] A14[9]=A14[20]
A14[18,8]=A14[6,17] A13[30,25,23]=A14[30,25,23] A13[15]!=A14[15] A13[29]!=A15[29] A15[29]=A6[29]
```

Pair-consistent reading (as in #26): E7 relations as `=`; A14[18,8] != A14[6,17]; A15[29] = A16[29] ("A6" is a
misprint); the two W20 equalities dropped. The 71 remaining two-bit conditions only shape the precomputed sets
(Section 4); every attack-critical test is an exact equality.

**Check against the pair** (organizer `digest(., 'sha256', 35)` and our code). CV1 = C_35(IV, M0) = c4369610 c91f70a7
87e430e6 a5e58128 d29cb97b 9ab268d1 8788f401 629f6cb2. The pair's signed differences equal the rows above (119 n/u
symbols, 360 single-bit conditions, 0 mismatches). It collides at 35 steps, not at 32.

M0 = a8850273 c0f4a504 5d3ad7b5 6e5f5026 535cc256 e92ef7a5 436f70df 7d7e236a cadc14e8 d59ac191 6874f1ba 6b83960d
f6dfe9de 6a013df2 f856b739 237894e8;
M1' = c0008214 ae65f3bf e93c006a 5f195aa9 84d6cd0f 25c114ec ca897317 da9fd6ef 6ec97e18 5100da8a 0912e57b a96b2054
41b22a2c 6d12f88a d2701ecc 140976d1;
M1 = M1' xor FL(W): words 4..8 are a4d6cd0f 21811cec ea897317 db9ec665 6ec17218, and words 12..13 are 45f2222c 4d12f88a.

## 3. Truncation to 32 steps

**Lemma 1.** If A[j] = A'[j] and E[j] = E'[j] for j = 19..22, and W[j] = W'[j] for j = 23..31, then
C_32(CV,M) = C_32(CV,M').

*Proof.* By induction on steps 23..31, every input of each step is equal. The feed-forward adds a common CV.

**Lemma 2.** With a common M0, M1 != M1', equal lengths, and C_32(CV1,M1) = C_32(CV1,M1'), the messages M0||M1 and
M0||M1' collide.

*Proof.* The padding block P is the same, and so is the chaining value entering it.

Rows 19..22 of A and E, and rows 23..31 of W, are `=` in Fig. 6. So a second block that conforms through step 22
and in W16..W31 gives a 32-step collision. The 35-step attack's conditions at steps 0..22 and the zero rows W23..W31
are exactly what is needed. Nothing is added. The rows W32..W34 are unused: W32 = sigma1(W30) + W25 +
sigma0(W17) + W16, W33 and W34 contain no difference term. The only change is CV1 = C_32(IV, M0), whose rate is
measured in Section 7.

**Independent instance (certificate and organizer experiment).** yudduy's #227 pair (credited; digest
f8a3db11...4e77) is our certificate `sha256-r32-route-corroboration-yudduy-227`: equal at 32 steps under
`digest(., 'sha256', 32)`, unequal at 31, 35 and 64. Experiment `fig6-conformance-replay` (organizer Docker run:
256/256 trials returned this full collision) recomputes its second block from CV1 = C_32(IV, M0) and reports
0 mismatches against all 86 embedded Fig. 6 rows (A, E -4..22; W0..31). Corroboration only, not our cost.

## 4. Algorithm

**Advice.** The advice is the unprimed values of the published pair from its 35-step CV1:

```
A4..A13 = 98560dbb 633b16ba 9bcf7bbe f8677ad6 4a299906 44f24ab5 39781650 6422edc8 574542b8 0508c8f0
E8..E13 = f1cae594 d0e1b7b4 bf27d74c b78bbfd9 3fffd0f9 bf81c0f4      W12, W13 = 41b22a2c 6d12f88a
```

Primed fixed words are X xor FL(X). fixX(i) means that X_i satisfies its printed single-bit conditions (0, 1,
n -> 0, u -> 1).

**P1.** L4 is every E4 with fixE(4) and E4[10] != E4[15]. L7 is every W7 with fixW(7) and its six two-bit
conditions.

**P2 (combinations).** For each (E5, E6, E7) with fixE(5..7):
- compute A3 = E7 - A7 + Sigma0(A6) + MAJ(A6,A5,A4), then A2 and A1 likewise from E6 and E5;
- compute W9..W11 from the E-equations of steps 9..11.

Keep the combination iff all of these hold:
- fixA(1..3) and fixW(9..11);
- XOR-conformance of A at steps 5..13 and of E at steps 9..13;
- the two-bit conditions among A1..A13, E5..E13 and W9..W13.

**P3 (TAB2).**
- E4 loop. For each combination and each E4 in L4, compute A0 = E4 - A4 + Sigma0(A3) + MAJ(A3,A2,A1) and
  W8 = E8 - A4 - E4 - Sigma1(E7) - IF(E7,E6,E5) - K8. Require fixW(8), fixA(0), XOR-conformance at A4 and E8, and the
  new two-bit conditions.
- W7 loop. For each W7 in L7, compute E3 = E7 - A3 - W7 - Sigma1(E6) - IF(E6,E5,E4) - K7 and
  A[-1] = E3 - A3 + Sigma0(A2) + MAJ(A2,A1,A0). Require fixE(3), fixA(-1), XOR-conformance at A3 and E7, and
  sigma0(W8') + W7' = sigma0(W8) + W7 (zero W23 difference).
- Storage. A record is 16 bytes: A[-1] and three indices. Records sit in one array bucketed by the top 27 bits of
  A[-1]. A counting pass gives the offsets, and a placing pass fills the array in place.

**P4 ((W14, W15) list).**
- Enumerate E14 with fixE(14). Compute A14 = E14 - A10 + Sigma0(A13) + MAJ(A13,A12,A11), and keep it if fixA(14) and
  its two-bit conditions with A13 hold.
- Then enumerate E15 with fixE(15). Keep it if fixA(15), A13[29] != A15[29], and XOR-conformance at steps 14 and 15
  hold.
- W14 and W15 follow from the E-equations.

**Main loop.** T trials and a work cap W_cap (Section 8). In each trial:
1. Draw M0 as 16 fresh uniform words and compute CV1 = C_32(IV, M0).
2. **Step 2.** Scan the bucket of CV1[0]. For each record with A[-1] = CV1[0]:
   - compute E0..E2 from the A-equations (A[-4..-1] from CV1) and W0..W6 from the E-equations;
   - accept, aborting early in this order, iff (a) W4 has its sign value; (b) sigma0(W4') + W12' = sigma0(W4) + W12;
     (c) W5 has its three sign values; (d) W6 has its sign value; (e) E is XOR-conformant at steps 0..6 and A at
     0..2; (f) sigma0(W6') + W5' = sigma0(W6) + W5; (g) (W13' - W13) + (sigma0(W5') - sigma0(W5)) + (W4' - W4) = D(W20).
3. **Step 3.** For each valid tuple and each P4 entry, set M1 = W0..W15 and M1' = M1 xor FL(W). For i = 16..31,
   with early abort:
   - require W'[i] = W[i] xor FL(W[i]) and the sign values of W20 and W22;
   - for i <= 22, also require XOR-conformance of A[i] and E[i]. Steps 14-15 depend only on the advice and the P4
     entry, so P4 stores per entry sigma1(W14), sigma1(W15) and the step-16 constants of both sides (6 words, built
     in P4 and charged in C). Stage 16 is then one addition and one test per side.
   If everything passes, recompute both full 3-block 32-step digests. If they are equal, output the pair and stop.
4. The algorithm adds its Step-2/3 operation charges (Section 8) to a counter and stops with failure if the counter
   exceeds W_cap. It also stops after T trials.

Every output is verified by recomputation, so correctness is unconditional.

## 5. Measured attack rates (our C code, fresh seeds)

This section reports participant runs on an i5-14400F with gcc -O3. The predicates are those of Section 4.

**Exact counts.** Every count equals the corresponding count in #26:
- L4 = 131,072 and L7 = 524,288;
- combinations = 10,240 of 2^32;
- (combination, E4) pairs = 155,008;
- N = |TAB2| = 1,396,774,912 = 2^30.3795;
- P4 = 196,608 = 12 * 2^14 = 2^17.585.

The 2^27-bucket layout has mean occupancy 10.41 and **maximum occupancy 936**. The A[-1] values repeat. Splitting
TAB2 into four parts by combination index mod 4, the sum over parts of sum_v c_v^2 (c_v = multiplicity of value v)
is 5.758e9.

**Self-test.** The published tuple is in TAB2, and with its 35-step CV1 it passes Step 2, reproducing
W0..W6 = M1'[0..6]. Its (W14, W15) is in P4. Exactly 1 of its 196,608 Step-3 candidates, the published one, passes
every stage.

**Analytic q.** For a fixed tuple, the CV1 words b, c, d make E2, E1, E0 successively uniform. So W4 and W5 are
uniform, and W6 = Y_t - E2 with Y_t = E6 - A2 - Sigma1(E5) - IF(E5,E4,E3) - K6.
Tests (a), (b), (c), (f), (g) pass with probability 1/2, 1/8, 1/8, 1/8, 1/8; step-6 conformance is a property of
the tuple and step-5 conformance depends only on E2[29].

Exact enumeration of TAB2 (#26's method, re-implemented): 609,229,824 tuples pass the step-6 test, and
sum_t Pr[E2[29] = e*(t), W6[29] = 0] = 214,235,406.9. So q_pred = 2^-45 * 214,235,406.9 = 2^-17.3254.

**Measured q.** Four runs, one per table part, each with 2^32 C_32 first blocks (seeds 2026001..4; #26 used other
seeds):

```
part   matches       valid   predicted
0      346,111,249   6,259   6,269.6
1      274,971,829   5,250   5,405.5
2      366,391,076   6,352   6,341.6
3      409,252,134   8,075   8,135.2
```

q (sum of per-part rates) = 2^-17.3373 (rel. sd 0.62%, Poisson); **99% LCB 2^-17.3583** = q - 2.326 sd (normal
approximation, 25,936 events), UCB 2^-17.3166. Matches per trial
0.32520 (N/2^32 = 0.32521). Pass fractions (a)..(g): 0.5000, 0.1250, 0.1250, 0.4999, 0.3065, 0.1249, 0.1241
(predicted 1/2, 1/8, 1/8, 1/2, 0.3068, 1/8, 1/8). Two valid tuples in one part: 9 of 2^34 part-trials. #26's runs:
2^-17.3337; #227's campaign counts: 14,643,237 tuples / 2.405e12 first blocks = 2^-17.326.

**Step-3 stage rates.** 25,936 tuples * 196,608 = 2^32.248 candidates. Cumulative passes: st16 2^-3.000, st17 2^-15.000 (155,619), st18
2^-21.03 (2,379), st19 2^-27.79 (22), st20 2^-29.93 (5), st21 2^-32.25 (1), st22 0.

The condition count predicts 2^-3, -15, -21, -28, -32, -33. Mapping: step 17 consumes E16's conditions; step 18
conforms iff E18[29] = 1 (IF(E17,E16,E15) absorbs the rest); step 19 needs the unprinted E16[29] = E17[29]; step 20
needs W20's signs and E19[29] = 0 (D(E16) + D(W20) = 0); step 21 needs E20[29] = 1; the remaining 9 W20 and 4 W22
carry conditions are tested at stage 22 and in W23..W31.

That is 45 printed conditions + 1, so **p = 2^-46 per candidate**.

## 6. The characteristic search, measured until it output Fig. 6

v5 charges all advice construction. No published running time for S's search was found (ePrint 2026/1080 PDF: HTTP
403 on 2026-10-06; the abstract states none; #31, which quotes S's text, reports none). We therefore ran S's
procedure ourselves until it produced S's characteristic.

**Tooling and model.** The authors' library Peace9911/sha_2_attack (commit 6a9f35f,
`configuration/unit_function_256.py` unmodified: signed-difference models of the step functions and expansion, and
the exact value model `sha2_value`), with STP 2.3.4 (sha d7008546) + CryptoMiniSat 5.11.21, called as
`stp model.cvc --cryptominisat --threads N` (the authors use 26). Each call ran under `/usr/bin/time -v` (user+system
CPU over all threads, peak RSS). We re-parametrised the authors' 31-step FunctionModel: steps 4..22, expansion
W16..W34, differences only in W4..W8, W12, W13, W20, W22, zero A/E differences at steps 0..3, zero A at 15..22, zero
E at 19..22, the authors' rule for exact sums (op2 = 1 for E at steps >= 19, op5 = 1 for A at >= 15), the 31-step
hard-coded weights removed, and the objective as `BVPLUS(12, difference bits) <= k`. Calibration: with every Fig. 6
row asserted the model is SAT (29 CPU-s), so it admits S's characteristic.

**Procedure.** S's Steps 1-4: (1) minimise tw; (2) with nabla W fixed, minimise tE; (3) with tE fixed, lower tA
until UNSAT; (4) with tE, tA fixed, minimise tE4. Each lowers a `<=` threshold until UNSAT; a call at its wall cap
(2-4 h) is charged and leaves the step unproven. Step 1 descended linearly; Steps 2-4 switched to bisection to fit
the window (calls stopped at the switch are charged). Our Step-1 optimum is a different weight-22 pattern from S's;
a relaxation fixing only the weight was abandoned after 50 min (charged). Steps 2-4 therefore fixed nabla W to S's
rows (conditioned on S's Step-1 output); Steps 3-4 ran concurrently under tE = 6, tA = 21. Step 2 then returned
exactly tE = 6, and Step 3 proved tA = 19, below S's 21; S's characteristic is therefore not the plain Step-3 optimum of this relaxed model (#31 likewise found lower relaxed optima contradictory under an exact model), and Step 4 kept S's threshold tA <= 21, which admits it. After the stop of the first window, Step 4 was resumed (8 h caps): a call at
<= 111 (6 threads) timed out, and a call at <= 76, S's weight, (8 threads) returned SAT.

| Phase | Calls | Results (S = SAT, U = UNSAT, T = timeout, A = abandoned) | CPU-s | Wall s | Peak RSS | Optimum found | Published |
|---|---|---|---|---|---|---|---|
| calibration (Fig. 6 asserted) | 2 | ES | 29 | 27 | 1.96 GiB | - | - |
| Step 1: min sum H(nabla W) | 19 | SSSSSSSSSSSSSSSSSSU | 29649 | 3463 | 1.43 GiB | 22 (proved) | 22 |
| Step 2 relaxation (weight only) | 1 | A | 27613 | 3022 | 5.25 GiB | - | - |
| Step 2: min tE (nabla W fixed) | 18 | SSSSSSSSSSSSSESUUS | 68857 | 10012 | 4.57 GiB | 6 (proved) | 6 |
| thread-count change stub | 1 | A | 2 | 1 | 0.00 GiB | - | - |
| Step 3: lower tA (tE fixed) | 10 | SSSESUSSSU | 35603 | 10409 | 2.62 GiB | 19 (proved) | 21 |
| Step 4: min tE4 (tE, tA fixed) | 8 | SETSESTA | 432105 | 72708 | 4.26 GiB | 76 (not proved) | 76 |
| **all search calls** | 59 | | **593858** | 99644 | 5.25 GiB | | |

Steps 1-2 reached S's optima (22, 6) with proofs; Step 3 proved 19 in the relaxed model (S keeps 21); Step 4 (tA <= 21) reached 76 = S's value. The <= 78 and <= 111 calls timed out although Fig. 6 satisfies them; they are charged. M_E counts every search call.

**Starting solution (attack Step 1).** S finds one solution through step 13 by SAT (quoted 2^34.3, no unit). We ran
the task twice (authors' exact value model on steps 4..13, Fig. 6 rows asserted, 4 threads) and checked both outputs
exactly (steps 4..13 hold unprimed and XOR-conformant primed, 10/10 each). Run 1: 534.1 CPU-s, 2.08 GiB, printed
single-bit conditions not asserted (25 fail). Run 2, with them asserted: SAT in 374.7 CPU-s (114 s wall, peak 1.98 GiB); 10/10 and 10/10, and all printed single-bit conditions of A4..A13 and E4..E13 hold (0 violated). D = 8 x 908.8 CPU-s x kappa =
2^35.83, above S's 2^34.3 in any unit up to one compression. Our solution is not claimed to be S's.

**CPU-second price kappa = 2^23 units = 2^34.12 primitive operations per CPU-second** (the value used in #367,
#377 and #134). Our calibration: one deterministic call (Step-1 input, 1 thread, `--max-num-confl 20000`) took 40.42
native CPU-s and retired 44,197,378,388 instructions under callgrind (identical output): **2^30.03 instructions per
CPU-second**, so kappa allows 17 primitive operations per instruction. Opcode mix (callgrind counts joined with
objdump): divide 0.305%, floating point 0.085%, multiply 0.026%, unmapped 7.24%, ordinary integer 92.3%. Pricing
ordinary and unmapped instructions at 5 operations and divide/multiply/floating point at 400 gives 6.6 <= 17.
The unmapped 7.24% are PLT stubs (endbr64 + indirect jmp pairs in 16-byte slots, matching the 3.7% call share),
i.e. ordinary instructions; the slack is 17/6.6 = 2.57x (1.36 bits). The call was repeated 3 times natively (40.42, 41.07,
41.10 CPU-s); it is single-thread while charged calls were multithreaded (lower IPC, conservative). The kappa = 2^24 row of Section 8 is the fallback.

**Result: the search outputs S's characteristic.** The <= 76 call returned (tw, tE, tA, tE4) = (22, 6, 21, 76), and
every signed row A0..A22, E0..E22, W0..W34 is identical to Fig. 6. So the measured run constructs exactly the
advice the attack uses, conditioned on S's nabla W (in the advice) and on S's thresholds tA <= 21 and
tE4 <= 76, whose blind re-derivation is priced in the margin below; 76 is not proved optimal. Peak 4.26 GiB. Fig. 6 is non-contradictory: S's 35-step pair and the #227 32-step pair both
conform to it (Sections 2, 3). The attack's q and p (Section 5) were measured for exactly this characteristic.

**Charge.** E = 32 x M_E x kappa, with M_E = 593,858 CPU-s over all 59 search calls (every call charged: the
calibration, the abandoned relaxation, stopped and timed-out calls, the 174,445 CPU-s final Step-4 call and its
172,129 CPU-s timed-out sibling). CPU-s already sum over threads, so no thread factor is charged. The margin 32
(heuristic `route-search-measured`) is a blind-rediscovery factor of about 8 times a residual safety factor 4:
- *Rediscovery (about 8 M_E).* The blind arm, a descent from <= 111, timed out after 172,129 CPU-s with no
  progress; the call that succeeded was aimed at S's 76. Priced from our ledger at the 8 h x 8-thread cap
  (230,400 CPU-s per call), a blind Step 4 at one tA level costs 1.2-1.6M CPU-s (the measured 432k plus 3-5
  descent calls and a stopping call). Re-deriving tA = 21 (Step 3's relaxed optimum is 19, which #31 found to be
  contradictory under the exact model) means Step 4 at three tA levels. With Steps 1-3 and the calibration, that
  is 3.8-5.0M CPU-s = 6.3-8.4 M_E.
- *Residual x4.* x2 for run-to-run variance of the parallel SAT portfolio (our concurrent Step-4 calls: one SAT,
  one timeout at similar CPU), and x2 for S's Sect. 3 exploratory models and the choice among weight-22 nabla W
  patterns (our own Step 1 found a different one).
Limitation: the rediscovery cost is priced from our ledger, not executed; S's own time is unpublished.

## 7. Success probability

Trials are independent, so P >= 1 - exp(-sT). Let V be the number of valid tuples per trial. Then
s >= (q - E[C(V,2)]) * r.
- **E[C(V,2)] <= q * 2^-5 (`valid-tuple-pairs`).** Within-part pairs were 9 in 2^34 part-trials, i.e. 2^-28.8 per trial, against
  0.75 expected for independent records. Applying that correlation factor (12) to the Cauchy-Schwarz bound on
  cross-part pairs gives 2^-26.8. The charge is more than 20x the total.
- **r (`step3-46-conditions`).** r >= E[X] - E[C(X,2)], where X is the number of conforming candidates and E[X] = 2^17.585 * 2^-46 =
  2^-28.415. Candidates share W14 in 12 groups of 2^14, and W20's 12 conditions are common within a group. So
  E[C(X,2)] <= 12 C(2^14,2) 2^-12 (2^12 p)^2 + C(2^17.585,2) p^2 <= 2^-49.3, and r >= 2^-28.415 (1 - 2^-20).

So s >= 2^-17.3583 (1 - 2^-5) 2^-28.415 (1 - 2^-20) = 2^-45.819. With T = 2^45.0 (as in #377), sT = 0.5668. Subtracting the cap
stop (Section 8):

**P >= 1 - e^-0.5668 - 4.4e-5 = 0.4326 >= 0.42 claimed.**

P >= 0.39 holds if s is 13% lower. Our fresh-seed q and #227's counts both exceed the q bound used.

## 8. Time (units, C = 2224)

Charges: a load, store, add, logic op, shift, compare or branch is 1 operation; a rotation is 4; Sigma/sigma is 14;
a mod-2^32 add is 2.

**A. Fixed work per trial, T = 2^45.0 trials.** 1 unit for C_32, plus 42 operations: 34 to draw and unpack two 256-bit random words, 5
for the bucket index, offsets and setup, and 3 for loop control.

**B. Counted work, capped.** Charges:
- each scanned record: 5;
- Step 2 per matching record: 160 (decoding the tuple, E0..E2, W4 and test (a)), +40 if (a) passes, +40 if (b),
  +40 if (c), and <= 1024 if (d) passes (W0..W3, the primed steps 0..6, W20, W21); at most 1304 in total;
- Step 3 per valid tuple: 300, plus per candidate 32 for stage 16 and <= 2048 for the rest, paid only by the
  fraction f16 that passes stage 16.

With the measured rates (scan mean 10.41, 0.32521 matches per trial, Step-2 pass fractions 1/2, 1/16, 1/128, 1/256,
q_UCB = 2^-17.3166, f16 = 0.1250002):

E[X] <= 5(10.41) + 0.32521(192) + q_UCB(300 + 196,608(32 + 2048 f16)) = 461.4; the cap is W_cap = 1.1 T E[X] =
507.5 T. Trials are independent, so Var <= T E[X^2], and E[X^2] <= 3(E[scan^2] + E[S2^2] + E[S3^2]) with
E[scan^2] <= 25 * 936 * 10.41, E[S2^2] <= 1304^2 * 4 * 5.758e9 / 2^32, E[S3^2] <= (300 + 196,608 * 2080)^2 *
q_UCB(1 + 2^-4), i.e. E[X^2] <= 3.26e12. By Chebyshev, Pr[stop at cap] <= 3.26e12 / (0.01 T E[X]^2) = 4.4e-5.

A + B <= T(1 + 42/2224) + W_cap/2224 + 6 = **2^45.319**.

**C. Precomputation.** Exact iteration counts (P2 2^32, the E4 loop 2^30.32, the W7 loop 2 * 2^36.24, L4/L7, P4),
each at 1024 operations, plus record and prefix-sum costs, give 2^36.17. We charge 2^36.5.

**D. Starting solution.** 8 * 908.8 CPU-s * 2^23 = 2^35.83 (Section 6), above S's 2^34.3.

**E. Characteristic search.** 32 * M_E * 2^23 = 2^47.180 (Section 6; M_E = 593,858 CPU-s measured).

**Total** = A + B + C + D + E = **2^47.532**, and we claim **47.6**. preprocessing = C + D + E = 2^47.181,
and we claim 47.2. There are no restarts.

Sensitivity (total time_log2):

| kappa (units per CPU-s) | margin 8 | margin 32 (charged) | margin 64 |
|---|---|---|---|
| 2^23 (charged) | 46.25 | 47.53 | 48.37 |
| 2^24 | 46.82 | 48.37 | 49.28 |
| 2^25 | 47.53 | 49.28 | 50.23 |

## 9. Memory

| Item | Bytes |
|---|---|
| TAB2, 16N | 22,348,398,592 |
| bucket offsets | 536,870,916 |
| other tables, code and state | < 2^24 |
| largest solver peak (search / start) | 5,642,330,112 |

The total is 28,544,376,836 = 2^34.732. The route search's memory is pre-declared (supporting heuristic
`search-peak-memory`): the measured peak over all 59 search calls and both start runs is 5.25 GiB < 2^33 bytes. The
phases run sequentially, so even a search peak of up to 2^33 bytes for S's own search keeps the bound at
max(attack 2^34.4, search 2^33) < 2^35. We nevertheless add the measured peaks. We claim 35. The advice
(characteristic, 71 conditions, 18 words, constants) is < 8 KB, so we claim 13.

## 10. Heuristics (IDs exactly as in claim.json)

- `q-32step-matching-rate` (score-critical): q >= 2^-17.3583. Evidence: the exact-enumeration prediction 2^-17.3254,
  our 2^34 trials, #26's runs and #227's campaign counts. Assumption: CV1 words act as uniform for the Step-2 tests.
- `step3-46-conditions` (score-critical): p >= 2^-46. Evidence: the condition count, stage rates measured through
  step 21, and the #227 instance (Section 3). The 13 W20/W22 carry conditions after step 21 are extrapolated (plausible, not
  established); the certificate pair and the replay experiment show a full conformance exists.
- `route-search-measured` (score-critical): constructing Fig. 6, given its nabla W, costs <= 32 x M_E
  solver CPU-s. Evidence: our run of S's procedure output Fig. 6 exactly (Section 6); the margin is itemised there.
- `cpu-second-pricing` (score-critical): 1 solver CPU-s <= 2^23 units. Evidence: Section 6.
- `valid-tuple-pairs` (supporting): E[C(V,2)] <= q * 2^-5.
- `starting-solution-measured` (supporting): the starting solution costs <= 8 * 908.8 CPU-s at kappa, above S's
  2^34.3.
- `search-peak-memory` (supporting): the route search's peak memory is below 2^33 bytes (Section 9).

Not claimed: a 32-step pair of our own (the certificate is #227's), or rigorous qualification. This package is a run of the agentprivacy
dual-agent harness (`hashsmash_mage` instance).
