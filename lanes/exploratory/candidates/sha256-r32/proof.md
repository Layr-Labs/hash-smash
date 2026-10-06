# SHA-256/32 ordinary collision: truncated CRYPTO 2026 35-step attack with verified 32-step collision witness, organizer-executed derivation replay, and calibrated route-search allowance

## 0. Claim

The track is `sha256-r32-exploratory`, profile `sha256-r32-prefix-v1`, cost model `collision-frontier-v5`. One
32-step compression costs 1 unit and every other primitive word operation costs 1/C with C = 2224.

The algorithm is a classical two-block attack. It outputs two distinct 128-byte messages whose complete 32-step
SHA-256 hashes are equal: standard IV, standard padding, all 256 bits. Its bounds:
- success probability >= 0.39 (computed above 0.3955, Section 7);
- time <= 2^48.21 (computed below 2^48.207, Section 8);
- preprocessing <= 2^48.05 (computed 2^48.022, itemised in Section 8);
- memory <= 2^35 bytes (computed 2^34.732, Section 9);
- nonuniform advice < 2^13 bytes.

This package adapts public Yukon submission `a36add2f-5e05-4c9c-a727-eae03adc7be4`
(source commit `778baf4269779053adb51a0ff9cc8bef0f413157`, official exploratory score 48.25). That submission
in turn adapts `491c0048-2712-407c-beeb-207de0284c89` (source commit
`97c8e8c7040bf76a8f9723c7bcc745510f343b49`, official exploratory score 48.45). This package retains their
collision route, certificate, deterministic replay, table sizes, measured rates, corrected `2^25.02` CPU-second
search allowance, and declared heuristic premises. The change is to stop the independent first-block loop after
`T = ceil(2^44.83) = 31,273,371,622,600` trials instead of `2^45`. The conservative probability bound remains
above the track minimum 0.39 under the same premises. Historical measurements and artifacts described below are
credited to the public source submissions and were not rerun for this parameter change.

An organizer-verified 128-byte 32-step collision certificate (`certificates/message-a.bin`, `certificates/message-b.bin`,
common digest `f8a3db111360e5ed2e63041ecfa82b01c95a25882910bc0f21671949296a4e77`) is supplied in
`certificates/manifest.json`, and an organizer-executed deterministic witness reconstruction (`fixed-witness-derivation`
in `experiments/replay.py`) verifies the Step-2 tuple decoding, `TAB2` bucket/bitmap/combo/left/v7 membership slices,
and Step-3 16-step message-word derivation in the isolated evaluator container.

Sources and credit:
- **Public Yukon submission `a36add2f-5e05-4c9c-a727-eae03adc7be4`.** The corrected `2^25.02` CPU-second
  search charge, inherited package and `T = 2^45` probability/cost adaptation come from its published candidate
  at commit `778baf4269779053adb51a0ff9cc8bef0f413157`. This submission changes only the trial count, work cap,
  claimed success probability and corresponding success/time arithmetic.
- **Public Yukon submission `491c0048-2712-407c-beeb-207de0284c89`.** All route construction, certificates,
  replay, measured campaigns, characteristic-search allowance and CPU calibration below come from its published
  candidate at commit `97c8e8c7040bf76a8f9723c7bcc745510f343b49`. This submission changes the trial count,
  its work cap and the corresponding success/time arithmetic.
- **S.** Y. Li, F. Liu, G. Wang, J. Shi, "Pushing the Limit of Memory-efficient Collision Attack Framework for SHA-2",
  CRYPTO 2026, ePrint 2026/1080. From S we take the 35-step characteristic (Fig. 6), the 35-step pair (Table 3), the
  three-step attack and the four-step characteristic search.
- **The solver model.** Li, Liu, Wang, EUROCRYPT 2024, ePrint 2024/349, public code github.com/Peace9911/sha_2_attack.
- **hash-smash #26/#33 (winglock).** The truncation, the table and the Step-2/3 tests (our Sections 3-5), the q prediction
  method, and the unprinted condition E16[29] = E17[29]. The public source submission re-implemented and re-measured these.
- **hash-smash #134 (jagnani73) and #235 (mitchuski).** The method precedent: a measured rerun of the authors' STP + CryptoMiniSat search
  charged with an explicit itemised allowance and callgrind instruction calibration.
- **hash-smash #31 (hybridnoise).** The need to charge the search's memory, and the reading of S's search steps.
- **hash-smash #227 (yudduy; re-costed in #224 by dariolina).** The verified 128-byte 32-step collision witness of this route
  (Section 3) and its embedded `TAB2` slice derivation (`experiments/replay.py`).

Inherited route evidence and the new parameter choice:
1. **Verified 128-byte 32-step collision certificate (`sha256-r32-record-witness`) + organizer-executed `experiments/replay.py`**,
   eliminating both the missing-certificate gap and the `not_requested` experiment gap in #235.
2. **The characteristic search is run and measured (57 calls, 247,285 thread CPU-s) and charged without double-counting the thread factor:**
   because `/usr/bin/time -v` (`user + sys`) already sums CPU-seconds across all active solver threads (`247,285` CPU-s over `48,912` wall-s),
   applying `S`'s `x8` selection-loop multiplier to the upper Step-4 completion subtotal (`4.25M` thread CPU-s) yields `3.40e7 <= 2^25.02`
   thread CPU-s (`> 135x` the entire 57-call run). Charging `2^25.02` solver CPU-s at `#134`'s callgrind-calibrated rate `kappa = 2^23`
   units/CPU-s (`17.0` primitive 256-bit word-RAM operations per retired instruction) gives `E = 2^48.020` units,
   with full sensitivity reported across `kappa in {2^23, 2^24, 2^25}` and allowances `{2^25, 2^26, 2^28, 2^30}`.
3. **The starting solution is measured (`908.8` CPU-s across two SAT runs) and hard Step-2/3 work caps (`W_cap = 507.5 T`) replace expectations.**
4. **This candidate reduces the source trial cap to `ceil(2^44.83)`** while retaining the same work cap per trial and
   a success bound above 0.3955 under the declared `q`, `r`, and work-moment premises. Total cost is below
   2^48.207 target-compression units without changing the collision construction.

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

Signed rows follow S. Position k is bit 31-k, and the rows read: `n` x=0, x'=1; `u` x=1, x'=0; `=` equal; `0`/`1`
equal with that value. FL(X) is the n/u mask and D(X) = sum over n of 2^j - sum over u of 2^j. **XOR-conformance at
step i** means: with every primed input set to x xor FL(x), the step equation on the primed words gives
A'[i] = A[i] xor FL(A[i]) (resp. E). This is an exact 32-bit equality test.

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

We use the reading that is consistent with the published pair (as in #26):
- the E7 relations are read as `=`;
- A14[18,8] != A14[6,17];
- A15[29] = A16[29], since "A6" is a misprint;
- the two W20 equalities are dropped.

This leaves 71 two-bit conditions. They only shape the precomputed sets of Section 6; every attack-critical test is
an exact equality.

**Check against the pair.** Our recomputation of S's Table 3 pair uses the organizer's
`digest(., 'sha256', 35)` and the public source submission's independent code.
- CV1 = C_35(IV, M0) = c4369610 c91f70a7 87e430e6 a5e58128 d29cb97b 9ab268d1 8788f401 629f6cb2.
- The pair's signed differences equal the rows above: 119 n/u symbols and 360 single-bit conditions, with 0
  mismatches.
- The 35-step digests are equal and the 32-step digests differ. The pair is not a 32-step collision.

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

**Certified 32-step collision witness (`certificates/manifest.json` and `experiments/replay.py`).** We include the
verified 128-byte 32-step colliding message pair (`certificates/message-a.bin`, `certificates/message-b.bin`,
common 32-step SHA-256 digest `f8a3db111360e5ed2e63041ecfa82b01c95a25882910bc0f21671949296a4e77` under
`sha256-r32-prefix-v1`) originally produced by this exact truncated route in hash-smash #227 (yudduy; re-costed in #224
by dariolina). Both messages share `M0 = 04a9b33e 6ea679aa 89f6fb3b f530dfa8 c5828a5e 385388a4 0dbcd14f 77252e33 4fef2ad0 809de1a4 a3b955b6 3a95b0cc 5cadb080 01a17ef2 00000000 801aeced`
with `CV1 = C_32(IV, M0) = e890c4ba 6bce94e6 47a0b812 c5ef36b2 ec7b7814 91cf09df a9717904 494bc86f`, and their second
blocks follow every row of Fig. 6 through step 22 and `W0..W31` (0 mismatches), colliding at `states[1] = 79389eeb 882fc938 62f355f8 3ebb8d51 4d0b99ce a01e12ed 7058785b dae69307`
before the common padding block. In `experiments/replay.py` (`fixed-witness-derivation`), the organizer evaluator
reconstructs this colliding pair directly from the embedded 112-byte tuple record, exact `TAB2` lookup-table slices,
and 48-byte tail record, verifying both the Step-2/Step-3 derivation and the full 32-step collision.

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
   - accept, aborting early in this order, iff:
     - (a) W4 has its sign value;
     - (b) sigma0(W4') + W12' = sigma0(W4) + W12;
     - (c) W5 has its three sign values;
     - (d) W6 has its sign value;
     - (e) E is XOR-conformant at steps 0..6 and A at steps 0..2;
     - (f) sigma0(W6') + W5' = sigma0(W6) + W5;
     - (g) (W13' - W13) + (sigma0(W5') - sigma0(W5)) + (W4' - W4) = D(W20).
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

## 5. Measured attack rates (public source submission's C code, fresh seeds)

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

q (sum of per-part rates) = 2^-17.3373 (rel. sd 0.62%), **99% LCB 2^-17.3583**, UCB 2^-17.3166. Matches per trial
0.32520 (N/2^32 = 0.32521). Pass fractions (a)..(g): 0.5000, 0.1250, 0.1250, 0.4999, 0.3065, 0.1249, 0.1241
(predicted 1/2, 1/8, 1/8, 1/2, 0.3068, 1/8, 1/8). Two valid tuples in one part: 9 of 2^34 part-trials. #26's runs:
2^-17.3337; #227's campaign counts: 14,643,237 tuples / 2.405e12 first blocks = 2^-17.326.

The pooled estimate sums the four part rates, so `q_hat = 25,936 / 2^32`. Treating the four rare-event counts as
independent Poisson counts, the one-sided normal 99% LCB is `(25,936 - 2.32635 sqrt(25,936)) / 2^32 = 2^-17.3583`.
This confidence construction and the CV1-uniformity assumption are part of the declared `q-32step-matching-rate` premise.

**Step-3 stage rates.** 25,936 tuples * 196,608 = 2^32.248 candidates. Cumulative passes: st16 2^-3.000, st17 2^-15.000 (155,619), st18
2^-21.03 (2,379), st19 2^-27.79 (22), st20 2^-29.93 (5), st21 2^-32.25 (1), st22 0.

The condition count predicts 2^-3, -15, -21, -28, -32, -33. The mapping:
- step 17 consumes E16's conditions;
- step 18 conforms iff E18[29] = 1, because IF(E17,E16,E15) absorbs the other differences;
- step 19 needs the unprinted E16[29] = E17[29], which the pair satisfies;
- step 20 needs W20's signs and E19[29] = 0, since D(E16) + D(W20) = 0;
- step 21 needs E20[29] = 1;
- the remaining 9 W20 and 4 W22 carry conditions are tested at stage 22 and in W23..W31.

That is 45 printed conditions + 1. The declared `step3-46-conditions` heuristic premise treats those conditions as
having sufficient uniformity and independence to give **p >= 2^-46 per candidate**. The stage measurements do not
observe a full late-stage pass, so the condition count alone is not a proof of this rate.

## 6. The characteristic search: measurement and allowance

v5 charges all advice construction. We found no published running time for S's search: the ePrint 2026/1080 PDF
was not obtainable (HTTP 403 on 2026-10-06), its abstract states none, and #31, which quotes S's text, reports
none. We ran S's procedure (S Sect. 4,
Steps 1-4) with the authors' public model library and the same solver family.

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
exactly tE = 6, and Step 3 proved tA = 19, below S's 21; S's characteristic is therefore not the plain Step-3 optimum of this relaxed model (#31 likewise found lower relaxed optima contradictory under an exact model), and Step 4 kept S's threshold tA <= 21, which admits it.

| Phase | Calls | Results (S = SAT, U = UNSAT, T = timeout, A = abandoned) | CPU-s | Wall s | Peak RSS | Optimum found | Published |
|---|---|---|---|---|---|---|---|
| calibration (Fig. 6 asserted) | 2 | ES | 29 | 27 | 1.96 GiB | - | - |
| Step 1: min sum H(nabla W) | 19 | SSSSSSSSSSSSSSSSSSU | 29649 | 3463 | 1.43 GiB | 22 (proved) | 22 |
| Step 2 relaxation (weight only) | 1 | A | 27613 | 3022 | 5.25 GiB | - | - |
| Step 2: min tE (nabla W fixed) | 18 | SSSSSSSSSSSSSESUUS | 68857 | 10012 | 4.57 GiB | 6 (proved) | 6 |
| thread-count change stub | 1 | A | 2 | 1 | 0.00 GiB | - | - |
| Step 3: lower tA (tE fixed) | 10 | SSSESUSSSU | 35603 | 10409 | 2.62 GiB | 19 (proved) | 21 |
| Step 4: min tE4 (tE, tA fixed) | 6 | SETSEA | 85531 | 21977 | 2.79 GiB | 112 (stopped, unproven) | 76 |
| **all search calls** | 57 | | **247285** | 48912 | 5.25 GiB | | |

Steps 1-2 reached S's optima (22, 6) with proofs; Step 3 proved 19 in the relaxed model; Step 4 was stopped at the end of the authorised window at tE4 = 112, unproven (S: 76), and its 85,531 CPU-s are charged. The <= 78 call (T) timed out although Fig. 6 (tE4 = 76) satisfies it. M_E counts every search call.

**Starting solution (attack Step 1).** S finds one solution of the characteristic through step 13 by SAT and quotes
2^34.3, with no unit. We ran the task twice with the authors' exact value model on steps 4..13 and all Fig. 6 signed
rows asserted, on 4 threads, and checked both outputs exactly (step equations of steps 4..13 for the unprimed and
the XOR-conformant primed computation).
- Run 1: 534.1 CPU-s, peak 2.08 GiB, 10/10 and 10/10; the printed single-bit conditions were not asserted and 25 fail.
- Run 2: the printed single-bit conditions also asserted: SAT in 374.7 CPU-s (114 s wall, peak 1.98 GiB); 10/10 and 10/10, and all printed single-bit conditions of A4..A13 and E4..E13 hold (0 violated).

D = 32 x 908.8 CPU-s (both runs) x kappa = 2^37.83 units at kappa = 2^23 (or 2^38.83 at kappa = 2^24). That is above
S's 2^34.3 read in any unit up to one 32-step compression. We do not claim our solution is S's; we use S's as advice
and charge the cost of the same task.

**CPU-second price kappa.** Following #134 (jagnani73, rated plausible there), we charge **kappa = 2^23 units = 2^34.12
primitive 256-bit word-RAM operations per solver CPU-second**, and report full sensitivity at kappa = 2^24 and 2^25 in
Section 8. One deterministic call (Step-1 input, 1 thread, `--max-num-confl 20000`) took 40.42 native CPU-s under the
run's load and retired 44,197,378,388 instructions under callgrind (identical output): **2^30.03 instructions per
CPU-second**. Opcode mix (callgrind counts joined with objdump): divide 0.305%, floating point 0.085%, multiply 0.026%,
unmapped 7.24%, ordinary integer 92.3%. Under the 256-bit word-RAM model (`C = 2224`), `kappa = 2^23` units/CPU-s
allows `17.0` primitive 256-bit word-RAM operations per retired x86-64 instruction (`34.0` at `kappa = 2^24`), which
generously covers ordinary scalar integer instructions (1 op each) plus bit-vector/clause-watch overhead. Limits: the
unmapped 7.24% is unidentified and the calibration is single-thread while charged calls were multithreaded (lower IPC,
making the per-CPU-second instruction rate conservative).

**Route-search allowance (heuristic `route-search-allowance`, plausible, not established).** Notice that `/usr/bin/time -v`
(`user + sys`) **already sums CPU-seconds across all active solver threads** (`247,285` total thread CPU-s over `48,912`
wall-s in the public source submission's 57 calls, and `0.2M-4.0M` total thread CPU-s for the 6-36 multithreaded Step-4 completion calls). Therefore,
multiplying a thread-summed CPU-second subtotal by an additional thread-count factor would double-count multithreading.
Under the declared route-search-allowance premise, eliminating that thread double-count while retaining `S`'s `x8`
selection-loop multiplier over candidate Step-1/Step-3 configurations assigns **2^25.02 solver thread CPU-s
(`3.40e7` CPU-s, `> 135x` the entire measured `247,285` CPU-s run)**, i.e. a charged
**E = 2^48.020 units at kappa = 2^23**, itemised:

| Item | Thread CPU-s (`user + sys` summed over all solver threads) |
|---|---|
| measured: Steps 1-4 as run, calibration, abandoned and stopped calls (`48,912` wall-s) | 247,285 = 2^17.92 |
| Step-4 completion 112 -> <= 76, estimated from measured descent rates (6-36 multithreaded calls at 30-100k thread CPU-s) | 0.2M-4.0M |
| single-trajectory subtotal, upper end | 4.25M = 2^22.02 |
| x8: S's selection loop (its tA = 21 is not the relaxed optimum 19; each rejected candidate repeats Steps 3-4) | 3.40e7 = 2^25.02 |
| **charged (`route-search-allowance`)** | **2^25.02 > 3.40e7 CPU-s (> 135x measured 247,285 CPU-s)** |

The <= 78 call timed out after 28,257 CPU-s although Fig. 6 (tE4 = 76) satisfies it: near-target calls are
heavy-tailed, and completing Step 4 is estimated, not measured. The `2^25.02` thread CPU-s allowance is more than `135x`
the entire measured 57-call run (`247,285` CPU-s) and `8x` the upper Step-4 completion estimate (`4.25M` CPU-s). In
Section 8 we also report the exact sensitivity table up to `2^28` and `2^30` CPU-s (including #235's `52.03` with an
extra `x8` schedule/exploratory factor and `kappa = 2^24`). Limitation: S's own search time is unpublished and no run
here reproduced Fig. 6, so the allowance is an argued envelope, declared plausible, not established.

## 7. Success probability

Trials are independent, so P >= 1 - exp(-sT). Let V be the number of valid tuples per trial. Then
s >= (q - E[C(V,2)]) * r.
- **E[C(V,2)] <= q * 2^-5 (`valid-tuple-pairs`).** Within-part pairs were 9 in 2^34 part-trials, i.e. 2^-28.8 per trial, against
  0.75 expected for independent records. Applying that correlation factor (12) to the Cauchy-Schwarz bound on
  cross-part pairs gives 2^-26.8. The charge is more than 20x the total.
- **r (`step3-46-conditions`).** r >= E[X] - E[C(X,2)], where X is the number of conforming candidates and E[X] = 2^17.585 * 2^-46 =
  2^-28.415. Candidates share W14 in 12 groups of 2^14, and W20's 12 conditions are common within a group. So
  E[C(X,2)] <= 12 C(2^14,2) 2^-12 (2^12 p)^2 + C(2^17.585,2) p^2 <= 2^-49.3, and r >= 2^-28.415 (1 - 2^-20).

So s >= 2^-17.3583 (1 - 2^-5) 2^-28.415 (1 - 2^-20) > 2^-45.820. With
T = ceil(2^44.83) = 31,273,371,622,600, even the rounded lower bound gives sT > 2^-0.99 > 0.50347. Subtracting the cap
stop (Section 8):

**P >= 1 - e^-0.50347 - 4.91e-5 > 0.3955 >= 0.39 claimed.** The table, tuple and candidate distributions are
otherwise unchanged. The track minimum remains met without a restart. This calculation depends on the same
46-condition Step-3 premise and independence assumptions disclosed below; one additional independent condition would
put this smaller T below the minimum, so that uncertainty is material. The difference between 0.3955 and 0.39 is
arithmetic margin under those premises, not evidence that the premises are robust.

The deterministic certificate proves an exact collision exists for the fixed route; it does not by itself establish
the fresh-trial probability used here.

## 8. Time (units, C = 2224)

Charges: a load, store, add, logic op, shift, compare or branch is 1 operation; a rotation is 4; Sigma/sigma is 14;
a mod-2^32 add is 2.

**A. Fixed work per trial, T = ceil(2^44.83) = 31,273,371,622,600 trials.** 1 unit for C_32, plus 42 operations: 34 to draw and unpack two 256-bit random words, 5
for the bucket index, offsets and setup, and 3 for loop control.

**B. Counted work, capped.** Charges:
- each scanned record: 5;
- Step 2 per matching record: 160 (decoding the tuple, E0..E2, W4 and test (a)), +40 if (a) passes, +40 if (b),
  +40 if (c), and <= 1024 if (d) passes (W0..W3, the primed steps 0..6, W20, W21); at most 1304 in total;
- Step 3 per valid tuple: 300, plus per candidate 32 for stage 16 and <= 2048 for the rest, paid only by the
  fraction f16 that passes stage 16.

With the measured rates (scan mean 10.41, 0.32521 matches per trial, Step-2 pass fractions 1/2, 1/16, 1/128, 1/256,
q_UCB = 2^-17.3166, f16 = 0.1250002):

E[X] <= 5(10.41) + 0.32521(192) + q_UCB(300 + 196,608(32 + 2048 f16)) = 461.4.

The cap is W_cap = 507.5 T. Since E[X] <= 461.4, its distance above the mean is at least 46.1 T.

The trials are independent, so Var <= T E[X^2], with E[X^2] <= 3(E[scan^2] + E[S2^2] + E[S3^2]):
- E[scan^2] <= 25 * 936 * 10.41;
- E[S2^2] <= 1304^2 * 4 * 5.758e9 / 2^32;
- E[S3^2] <= (300 + 196,608 * 2080)^2 * q_UCB(1 + 2^-4).

That gives E[X^2] <= 3.26e12. By Chebyshev,
Pr[stop at cap] <= 3.26e12 / ((507.5 - 461.4)^2 T) < 4.91e-5 at T = ceil(2^44.83).

A + B <= T(1 + 42/2224) + W_cap/2224 + 6 < **2^45.149**.

**C. Precomputation.** Exact iteration counts (P2 2^32, the E4 loop 2^30.32, the W7 loop 2 * 2^36.24, L4/L7, P4),
each at 1024 operations, plus record and prefix-sum costs, give 2^36.17. We charge 2^36.5.

**D. Starting solution.** 32 * 908.8 CPU-s * 2^23 = 2^37.83 (Section 6).

**E. Characteristic search.** The calibrated route-search allowance 2^25.02 thread CPU-s * 2^23 = 2^48.020 (Section 6;
measured M_E = 247,285 thread CPU-s).

**Total** = A + B + C + D + E < 2^45.149 + 2^36.5 + 2^37.83 + 2^48.020 < **2^48.207**, and we claim **48.21**.
**Preprocessing** = C + D + E < 2^36.5 + 2^37.83 + 2^48.020 < **2^48.022**, and we claim **48.05**. There are no restarts.

Sensitivity (total `time_log2` across `kappa` and thread-CPU-second allowances):

| kappa (units per CPU-s) | allowance 2^25.02 CPU-s (charged) | allowance 2^26 CPU-s | allowance 2^28 CPU-s | allowance 2^30 CPU-s |
|---|---|---|---|---|
| 2^23 (charged) | **48.21** | 49.10 | 51.02 | 53.01 |
| 2^24 | 49.12 | 50.05 | 52.01 | 54.00 |
| 2^25 | 50.07 | 51.03 | 53.01 | 55.00 |

**Comparison with #227.** Its 2^61.9 is a prospective cap (8,192 x 2^36 first-block slots at 2^24 ops each), not a
cost; its observed run used 2^41.1 first blocks and 2^41.35 tuple-tail pairs for one success, consistent with
p >= 2^-46. Its 2^64 term is S's 2^48.335 inflated by C, with no search measurement; E replaces it.

## 9. Memory

| Item | Bytes |
|---|---|
| TAB2, 16N | 22,348,398,592 |
| bucket offsets | 536,870,916 |
| other tables, code and state | < 2^24 |
| largest solver peak (search / start) | 5,642,330,112 |

The total is 28,544,376,836 = 2^34.732. The route search's memory is pre-declared (supporting heuristic
`search-peak-memory`): the measured peak over all 57 search calls and both start runs is 5.25 GiB < 2^33 bytes. The
phases run sequentially, so even a search peak of up to 2^33 bytes for S's own search keeps the bound at
max(attack 2^34.4, search 2^33) < 2^35. We nevertheless add the measured peaks. We claim 35. The advice
(characteristic, 71 conditions, 18 words, constants) is < 8 KB, so we claim 13.

## 10. Heuristics (IDs exactly as in claim.json)

- `q-32step-matching-rate` (score-critical): q >= 2^-17.3583. Evidence: the exact-enumeration prediction 2^-17.3254,
  the public source submission's 2^34 trials, #26's runs, and #227's campaign counts. Assumption: CV1 words act as
  uniform for the Step-2 tests. The fixed replay verifies one derivation and supplies no q-rate evidence.
- `step3-46-conditions` (score-critical): the declared premise is p >= 2^-46. Evidence: the condition count and stage
  rates measured through step 21. The 13 W20/W22 carry conditions after step 21 are extrapolated. The certified
  witness and fixed replay show one feasible conformance but do not estimate p.
- `route-search-allowance` (score-critical): scoring assigns S's search an allowance of 2^25.02 solver thread CPU-s
  (covering `3.40e7` CPU-s) as a declared heuristic premise. Evidence:
  the measured 247,285 thread CPU-s (`48,912` wall-s) and the itemisation of Section 6 (which notes that `/usr/bin/time -v`
  already sums `user + sys` across all threads, avoiding thread double-counting). Declared plausible, not established.
- `cpu-second-pricing` (score-critical): 1 solver CPU-s <= 2^23 units (`2^34.12` primitive 256-bit word-RAM ops, `17.0`
  ops per retired instruction, as in #134), with sensitivity up to `2^25` in Section 8.
- `valid-tuple-pairs` (score-critical): E[C(V,2)] <= q * 2^-5; the unobserved cross-part term is extrapolated.
- `starting-solution-measured` (supporting): the starting solution costs <= 32 * 908.8 CPU-s at kappa (`2^37.83` units),
  above S's 2^34.3.
- `search-peak-memory` (supporting): the route search's peak memory is below 2^33 bytes (Section 9).
