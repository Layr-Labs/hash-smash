# SHA-256, 31 steps: the published two-block collision, fully charged

Track `sha256-r31-exploratory`, profile `sha256-r31-prefix-v1`, cost model
`collision-frontier-v5` (31-step compression = 1 unit, word operation = 1/2140).

## 0. Claim, summary and verification checklist

| Field | Value | Where derived |
| --- | ---: | --- |
| time_log2 | 46.3 | Section 7: log2 T = 46.273, rounded up |
| success_probability | 0.6 | Section 6: >= 1 - e^-1 - 2^-108 = 0.632 |
| preprocessing_log2 | 46.2 | Section 7: T0 + T1 + T_aux = 2^46.120 |
| memory_log2_bytes | 36 | Section 9: SAT processes (H4); attack phases < 2^28.3 |
| nonuniform_advice_log2_bytes | 12 | Section 9: stored characteristic < 2^12 bytes |

Summary. The published two-block attack of [LLWDS24] with the characteristic of
[LLW24] (Table 6). Phase 1 runs a starting-point SAT model and fills a table TAB
keyed by A[-1] until it holds D >= 2^19 distinct keys. Phase 2 computes CV1 =
f31(IV, M0(j)) for N = 2^42.88 first blocks, looks up A[-1], derives W0..W6 and
tests the W5, W6 conditions. Phase 3 (our exact routine) picks W13, W14, W15 and
accepts only a zero state difference after step 30. Every term is charged,
including the unpublished historical search that produced Table 6 (H1, T0 =
2^45.92, dominant). No novelty or improvement is claimed. The total exceeds the
published 2^40.5 because T0 is charged, the measured mean yield is 2^10.61 keys
per start, each start costs 2^34.5 (H3), and our exact count of the completion
step gives beta = 2.88, not gamma ~ 1.3.

Verification checklist:
1. Three certificate pairs collide at 31 rounds (organizer checker) (L63-82).
2. Table 6: 300 non-'=' symbols, weights 48/21/51, the dW values (L85-113).
3. Nine exact expansion equations (L115-129).
4. Exhaustive counts W5 2^14, W6 2^23 (Npro = 27), W7 512, W8 49408 (L132-143).
5. |G16| = 64, |S| = 584683520, 2^-2.877, beta = 2.88; 81473/81473 (L145-163).
6. Yield mean 2^10.613, corrected mean 1472.1 >= mu = 2^10.5 = 1448.2 (L165-185).
7. W6 uniform over A[-2], W5 over A[-3], c18 over E[-2], independent (L214-220).
8. p >= 2^(19-32-27-2.88) = 2^-42.88 = 1/N, Pr[fail] <= e^-1 (L220-223).
9. E[X] <= 132.5 Phase-3 calls, Pr[X >= 1024] < 2^-108 (L225-229).
10. Cost table: total 2^46.273, preprocessing 2^46.120 (L235-244).
11. E[N_start] <= (2^19 + 2^16)/2^10.5 = 407.3 by Wald (L250-253).
12. 460-start cap: total 2^46.295, preprocessing 2^46.144, success 0.615 (L254-266).
13. T0 = 32 calls x 72 h x 2^34.750 units/h = 2^45.920; why charged (L274-287).
14. Memory < 2^28.3 bytes for attack phases; 2^36 declared (L317-322).

Sources: [LLWDS24] Li, Liu, Wang, Dong, Sun, ASIACRYPT 2024 (framework, table of
2^19.8 solutions matched on A[-1], time 2^40.5, memory 2^19.8, practical run "1.2
hours with 64 threads", the pair; figures from the slides). [LLW24] Li, Liu,
Wang, EUROCRYPT 2024, ePrint 2024/349 (Table 6, its search in Section 4.2,
starting-point model T_model ~ 2^31.7, gamma ~ 1.3). [LLWS26] ePrint 2026/1080
(T_pre = N_start x (T_sat + enumeration)). [MNS13] Mendel, Nad, Schlaeffer,
EUROCRYPT 2013 (local collision in W5..W9, W16, W18; two-block idea). "Ours"
marks our derivations; estimates are rounded up.

## 1. Target and notation

FIPS 180-4 SHA-256 with standard IV and padding, W[t] = s1(W[t-2]) + W[t-7] +
s0(W[t-15]) + W[t-16] for t >= 16, steps t = 0..30, full feed-forward, full
256-bit digest; differences are M1' - M1 mod 2^32. Chaining input (a..h) =
(A[-1], A[-2], A[-3], A[-4], E[-1], E[-2], E[-3], E[-4]); step t computes

    E[t] = A[t-4] + E[t-4] + S1(E[t-1]) + IF(E[t-1],E[t-2],E[t-3]) + K[t] + W[t]
    A[t] = E[t] - A[t-4] + S0(A[t-1]) + MAJ(A[t-1],A[t-2],A[t-3])

## 2. Certificates

Pair 1 is the published pair, M0||M1 versus M0||M1' (128 bytes each):

    M0  = 8ce3f805 5c401aed 579e5f7f bc3116cb ca189b3c eb75f04c 958f0a0e 7760b082
          dcd5027d 32260ad6 7b12b659 eee66518 ad7f88dd f8ad20bb 7ae40ffd 21609249
    M1  = 9abdeb1b 1f195f41 5a7210c1 55614f13 a2269dd1 be888a61 359257d4 adf3737b
          9f0484a6 eb830a58 66add94a 9669232d 45271fa5 b8f69585 428bbce3 0703b904
    M1' = 9abdeb1b 1f195f41 5a7210c1 55614f13 a2269dd1 be887a67 35b2dfc5 fde32975
          c70595a6 eb838a5c 66add94a 9669232d 45271fa5 b8f69585 428bbce3 0703b904

Pairs 2 and 3 (ours) keep M0 and block-2 words 0..12 and set (W13, W14, W15) =
(97ff934d, e29b9609, cb3c8ffb) and (f6f375b0, 6557e9a0, dc90cec4) from our
Phase 3; M1' = M1 + (0,0,0,0,0, fffff006, 002087f1, 4fefb5fa, 28011100,
00008004, 0,...,0). Digests are in certificates/manifest.json (pair 1:
55fdfb37efcbd086e19c3de0f72596300a3acdf48da5b1d0450a592bb2869fcd). With the
organizer reference digest each pair is equal at 31 rounds and differs at 29,
30, 32, 64. CV1 = c0a93f38 23b02f67 2f718088 03dfb329 7eaa51b9 0e2dd226 107e021b
70b1ac59 is common and both messages get the same padding block. The pairs
validate Table 6 and our Phase 3; they are not attack runs and not costs.

## 3. The characteristic
### 3.1 Table 6 of [LLW24] (published; stored advice)

'=' equal bits, 'u' (M1 bit 0, M1' bit 1), 'n' (1, 0), '0'/'1' equal bits of
that value; MSB first; rows -4..-1 (chaining input) are all '='.

      i  dA                               dE                               dW
    0-2  ================================ ================================ ================================
      3  ================================ ==========================10==== ================================
      4  ================================ ============0===0=========01===0 ================================
      5  ===================n=unnnnnnn=n= 000111010001111110nu=11111unnnu1 ================nuuu=======0=uu=
      6  ========n======================u 101011=11==0n0==u11110==1110011n ==========u=====u===u======n===u
      7  ===u===n==n========n=========n=u un0u1100n=01u11111001u1=n110u10n =u=u=======n=====n=nu=n=====nun=
      8  =============================n== 1u01un0u0=1=1=11n=0=u0=001001u0= =u=nn==========u===u===u==1=====
      9  ================================ 01100001110=0=010===00=11101u0=1 ================u==========1=u==
     10  ================u============u== =1n1uuuuu0100=1un0=10unnnnnnn010 ================================
     11  ================================ =01u1010uu1==11100===1000001n=0= ================================
     12  ================================ ==110001=11====1n====0011110n=0= ================================
     13  ================================ ===0====01======1=============== ================================
     14  ================================ ================u===========0u== ================================
     15  ================================ ================0============1== ================================
     16  ================================ ================1============1== =============unnnunnnnnnnnnnnn==
     17  ================================ ================================ ================================
     18  ================================ ================================ ==============1=n=0==========n==
  19-30  all '=' in dA, dE and dW

300 non-'=' symbols (120 signed differences, 180 value conditions); sum H(dW) =
48, H(dA) = 21, H(dE) = 51. All three pairs satisfy all 300 symbols (ours).
dW5 = fffff006, dW6 = 002087f1, dW7 = 4fefb5fa, dW8 = 28011100, dW9 = dW16 =
00008004, dW18 = ffff7ffc, all other dW[t] = 0.

### 3.2 Exact conditions on the message words (ours)

    t=16: dW16 = dW9                                 (automatic)
    t=18: s1(W16 + 00008004) - s1(W16) = ffff7ffc    (gives dW18)
    t=20: s1(W18 + ffff7ffc) - s1(W18) = 2ffe7fe0    (cancels d s0(W5))
    t=21: s0(W6 + 002087f1) - s0(W6) = 00000ffa      (= -dW5)
    t=22: s0(W7 + 4fefb5fa) - s0(W7) = ffdf780f      (= -dW6)
    t=23: s0(W8 + 28011100) - s0(W8) = b00fca02      (= -(dW16 + dW7))
    t=24: s0(W9 + 00008004) - s0(W9) = d7feef00      (= -dW8)
    t=25: dW18 + dW9 = 0                             (automatic)
    W5:   s0(W5 + fffff006) - s0(W5) = d0018020      (this algorithm's t=20 split)

No other step t <= 30 has a message difference (t = 31 has d s0(W16), so 32
steps differ). The state part gives dA[t] = 0 for t >= 11 and dE[t] = 0 for
t >= 15, hence a zero final difference.

## 4. Exact counts and measurements (ours; counts exhaustive over 2^32 values)
### 4.1 Admissible message words

| Word | Equation | Count |
| --- | --- | ---: |
| W5 | s0(X + fffff006) - s0(X) = d0018020 | 16384 = 2^14 |
| W6 | s0(X + 002087f1) - s0(X) = 00000ffa | 8388608 = 2^23 |
| W7 | s0(X + 4fefb5fa) - s0(X) = ffdf780f | 512 = 2^9 |
| W8 | s0(X + 28011100) - s0(X) = b00fca02 | 49408 = 2^15.59 |
| W9 | s0(X + 00008004) - s0(X) = d7feef00 | 35921920 = 2^25.10 |

W5, W6 match the published 2^14, 2^23, so Npro = 18 + 9 = 27. For W7, W8
[LLW24] gives 2^27, 2^25; we use only our exact counts.

### 4.2 The completion step

After Phase 2, W0..W12 are fixed. With c16 = W9 + s0(W1) + W0 and c18 = W11 +
s0(W3) + W2: W16 = s1(W14) + c16, W18 = s1(W16) + c18. s1 is a bijection. The
W16 meeting t=18 form G16 = { h*2^28 + v : h = 0..15, v in {031bbffc, 064bbffe,
09b3bffd, 0ce3bfff} } (64 values); the W18 meeting t=20 number |G18| = 42467328.
Each x in G16 gives one W14 = s1^-1(x - c16), which meets t=20 iff s1(x) + c18
is in G18. So success depends only on c18; the good set S = {y - s1(x)} has
|S| = 584683520, and Pr[some W14 works] = 584683520/2^32 = 0.136132 = 2^-2.877.
W13, W15 cannot change this. We do not use gamma ~ 1.3: Table-6 bit conditions
on W16, W18 are necessary, not sufficient (2048 vs 5 W14 on the published output).

Simulation of Phase 3 (Section 5) on the published start and W5..W12, W0..W4
uniform (the Phase-2 output law, Section 6): 600000 outputs (seeds 200000 +
400000); 81473 had a good W14 (0.13579 vs 0.13613), at most 16 per output; all
81473 completed to zero state difference after step 30. Mean 4131 E13 and 15 W15
tries per good output (maxima 57431, 229; below the caps). Failure rate given a
good W14 < 3/81473 = 2^-14.7 (95%). We use beta = 2.88: 2^-2.88 = 0.13584 <
0.13613 x (1 - 2^-14.7) = 0.13612, so completion failures are inside beta.

### 4.3 Starting-point yield

A start fixes (A[1..12], E[5..12], W[9..12]); E4 = off8 - W8 with off8 = E8 -
A4 - S1(E7) - IF(E7,E6,E5) - K8, step 7 gives E3, and (E3, E4) must satisfy

    step 7: IF(E6',E5',E4) - IF(E6,E5,E4) = dE7 - (S1(E6') - S1(E6)) - dW7
    step 6: IF(E5',E4,E3) - IF(E5,E4,E3) = dE6 - (S1(E5') - S1(E5)) - dW6

Then A0 = E4 - A4 + S0(A3) + MAJ(A3,A2,A1), A[-1] = E3 - A3 + S0(A2) +
MAJ(A2,A1,A0). On the published start, W8 (49408) then W7 (512) give 2048 valid
(W8, E4), 16896 = 2^14.04 tuples and 2336 = 2^11.19 distinct A[-1].

Random-offset model: the equations depend on the start only through E5, E6, E7
(Table 6 fixes 31, 25, 30 bits), off8 and A1..A4. Keep E5..E7 at published
values, draw off8, A1..A4 uniform, enumerate exactly. 20000 samples (two seeds;
the published start reproduces 2048/16896/2336): mean 1565.9 = 2^10.613 keys,
SD 4318, SE 30.5, mean - 3 SE = 1474.3 = 2^10.526; 68.9% give 0 keys; 17.4%
reach 2336; 3.91 tuples per key. The 2^16 per-start cap removes < 2 keys per
start on average and collisions with existing keys (<= 2^19.17 of 2^32) remove a
fraction < 2^-12.8, so the corrected mean stays >= 1474.3 x (1 - 2^-12.8) - 2 =
1472.1 > mu = 2^10.5 = 1448.2.

## 5. The algorithm (framework published; routine, caps, stops ours)

Advice: Table 6 as stored data (its search charged as T0). Phase 0': one 2^32
scan each for the W7 and W8 lists and G16 (T_aux). Phase 1, until D >= 2^19: run
the [LLW24] starting-point SAT model (steps 5..12, W9 meets t=24) with the two
step-13 relations the start alone fixes (W13 has no difference, dA9 = 0): dE13 =
dE9 + dS1(E12) + dIF(E12,E11,E10) = 0 and dA13 = dE13 + dMAJ(A12,A11,A10) = 0;
randomised by a fresh uniform W12 (so starts are distinct), time-out
2^35 units; abandon time-outs and UNSAT calls. Reject the start if recomputed
dE13 or dA13 is nonzero (the published start passes). Enumerate W8 then W7
(Section 4.3); insert (A[-1], A0, E3, E4, W7, W8, start id) into TAB, at most 16
tuples per key and 2^16 new keys per start; D counts distinct keys. Only D is
credited; extra tuples are tested, not counted.

Phase 2, j < N = 2^42.88: CV1 = f31(IV, M0(j)) (two words hold j); look up
A[-1]; per tuple compute E0..E2 (A-equations), W5, W6 (E-equations of steps 5,
6), test both; if both hold compute W4, W0..W3 and run Phase 3.

Phase 3 (at most 1024 calls in total): (a) for x in G16, W14 = s1^-1(x - c16),
kept if s1(x) + c18 is in G18. (b) Per kept W14, E13 = o + r x 9e3779b9 (random
o, r < 2^16), W13 = E13 - c13; accept if dE14 = 00008004 and dE15 = 0. (c) Per
accepted E13, W15 = o' + q x 9e3779b9 (q < 2^10; <= 2^16 W15 per call); require
dE16 = dE17 = 0, compute both messages through step 30, accept only a zero state
difference; else return to Phase 2. Phase 4: output, confirm both digests.

## 6. Success probability

Independence at a hit (ours). H2: CV1 is uniform for distinct j. Fix a stored
tuple whose key equals A[-1]. W6 = (fixed terms) - A[-2] (via E2 = A2 + A[-2] -
S0(A1) - MAJ(A1,A0,A[-1])), uniform over A[-2]; W5 = (terms in A[-2]) - A[-3],
uniform over A[-3] for each A[-2]; W2 = (...) - E[-2] and W3 = (...) - E[-1], so
c18 is uniform over E[-2]. Hence Pr[W5] = 2^-18, Pr[W6] = 2^-9, Pr[c18 in S] =
0.13613, exact and independent. A[-1] hits one of D disjoint keys with
probability D/2^32; one tuple per key, D >= 2^19 by the stopping rule:

    p >= 2^19 x 2^-32 x 2^-27 x 2^-2.88 = 2^-42.88,   pN >= 1,
    Pr[no success] <= (1 - p)^N <= e^-1 = 0.368.

Cap. X = number of Phase-3 calls; each trial adds 0..16; with <= 2^19 + 2^16
keys, E[X] <= N x 16 x (2^19 + 2^16) x 2^-59 = 132.5. For Y = X/16 (independent
[0,1] summands, mean <= 8.29), Chernoff at (1+d)m = 64 gives Pr[X >= 1024] <
2^-108. A per-call E13/W15 cap exhaustion is a completion failure (inside beta).
Hence Pr[success] >= 1 - e^-1 - 2^-108 = 0.632 > 0.6. A shortfall factor f in p
gives 1 - e^-f >= 0.39 for f >= 0.495. A yield shortfall does not lower p (D is
enforced); it raises the Phase-1 cost.

## 7. Complexity (units: 31-step compressions; word operation = 1/2140)

| Term | Derivation | Value | log2 |
| --- | --- | ---: | ---: |
| T0 search (H1) | 2304 thread-h x 2^34.750 units/h | 2^45.920 | 45.920 |
| T1 Phase 1 (H3) | E[N_start] = 407.3 x (2^34.5 + 2^20) | 2^43.170 | 43.170 |
| T_aux scans | 3 x 2^32 x 32 ops / 2140 = 2^27.52 | 2^28 | 28.000 |
| T2 Phase 2 | 2^42.88 x (1 + 128/2140) | 2^42.964 | 42.964 |
| T3 Phase 3 | 1024 x 2^19.26 = 2^29.26 | 2^29.5 | 29.500 |
| T4 output | 6 compressions | 8 | 3.000 |
| Total T | sum | 2^46.273 | 46.3 (up) |
| Preprocessing | T0 + T1 + T_aux | 2^46.120 | 46.2 (up) |

Without T0: 2^44.071; D = 2^19 minimises T1 + T2 to within 0.001 bit. T1 is an
expected cost (see 'T1 accounting' below); all other terms are worst cases
under the caps.

- T1: per start 2^34.5 (H3) plus enumeration 49408 x 64 + 49408 x 512 x 64 +
  2^20 x 128 + 2^8 = 2^30.71 ops = 2^19.65 -> 2^20 units. New keys per start
  Z_s <= 2^16 with E[Z_s | past] >= 2^10.5 (H3); the stop leaves D < 2^19 +
  2^16, so by Wald's identity E[N_start] <= (2^19 + 2^16)/2^10.5 = 407.3.
- T1 accounting. time_log2 counts the Phase-1 term in expectation under H3,
  which is itself an average-cost premise (per-start SAT time is only bounded on
  average). Worst-case start count check (same claim): cap Phase 1 at 460
  starts and run Phase 2 with whatever D is reached. Then T1 <= 460 x (2^34.5 +
  2^20) = 2^43.346, total 2^46.295 <= 2^46.3, preprocessing 2^46.144 <= 2^46.2.
  Success: pN = min(D, 2^19)/2^19 =: x and 1 - e^-x >= 0.632 x on [0,1], so
  Pr[success] >= 0.632 E[min(S, 2^19)]/2^19 - 2^-108, S = keys after 460
  starts. In the Section 4.3 model (starts i.i.d., mean >= 1448.2, SD <= 4318,
  Z_s <= 2^16), E[S] - 2^19 >= 460 x 1448.2 - 2^19 = 141863 and SD(S) <= 4318 x
  sqrt(460) = 92611; the one-sided mean-variance (Scarf) bound E[(c - S)^+] <=
  (sqrt(sigma^2 + d^2) - d)/2 gives <= 13777, so E[min(S, 2^19)]/2^19 >=
  0.9737 and Pr[success] >= 0.632 x 0.9737 - 2^-108 = 0.615 > 0.6. (The
  Section 6 Phase-3 cap argument is unchanged, since D <= 2^19 + 2^16.)
- T2: one compression plus <= 128 ops per trial (counter 6; lookup in 2^21
  buckets with chains 31; loop 4; hit work 16 x 2^8 x 2^-12.83 = 0.57).
- T3: per call (a) 64 x 2^7.5, (b) 64 x 2^16 x 2^8, (c) 2^16 x 2^12 ops = 2^30.33
  ops = 2^19.26 units.

## 8. Heuristics (mirrored in claim.json)

H1 (score-critical): T0 is charged because the collision-frontier-v5
nonuniform_advice rule requires the construction of stored advice to be charged,
"including any search omitted from the submitted program". The historical search
of [LLW24] Section 4.2 that produced Table 6 used <= 32 calls of <= 72
single-thread hours (2304 h), at 2^34 ops per thread-second (calibrated
estimate, 4 ops/cycle at 4 GHz) = 2^22.937 units/s = 2^34.750 units/h; T0 =
2^(11.170 + 34.750) = 2^45.920. Calls: three minimisation stages (sum H(dW);
H(dA); H(dE) with value transitions on steps 7..10) each fix their optimum (48,
21, 51) by binary search over 0..255 in 8 calls, plus one repeat of stage 3 (the
reported repair): 4 x 8 = 32. Evidence: 72 h is the per-call time-out of [LLW24]
Section 4.3 for 64-bit SHA-512 (not a run time); SHA-256 has half the word size
and a fixed difference pattern; the related starting-point model solves in
~2^31.7. Limitations: unpublished, not measured; multi-threading or earlier
searches add hours; core ceiling ~2^35.8 ops/s.

H2 (score-critical): CV1 = f31(IV, M0(j)) is independent uniform for distinct j
(Section 6), and given a good W14 our completion succeeds with probability close
to 1 on every start Phase 1 produces. Evidence: exhaustive counts (Section 4);
81473/81473 completions (failure < 2^-14.7, inside beta); pairs 2 and 3.
Limitation: completion measured on one start, favourable for yield; a factor-2
shortfall still gives success >= 0.39.

H3 (score-critical): an accepted start costs on average <= 2^34.5 units
(including time-outs, UNSAT calls and filter rejections) and adds on average >=
mu = 2^10.5 new keys given earlier starts. Evidence: T_model ~ 2^31.7 "SHA-256
computations" (unit unstated) reads as 2^31.7 (31-step), 2^32.8 (x 64/31) or
2^33.64 (2^21 SHA-256/s at 2^22.937 units/s); 2^34.5 is a further factor 1.82.
Yield: Section 4.3. Limitations: average-cost premise (heavy-tailed SAT times;
model imported, not rerun); yield model may differ from SAT starts. Affects cost
only (in the 460-start check of Section 7 the yield model also enters success).

H4 (supporting): SAT/SMT processes use <= 2^36 bytes (unreported; instances of
<= 31 steps of 32-bit state). Affects memory only, which is not scored.

Sensitivity of time_log2 (rounded up; table size re-optimised for H3 rows):

| Premise | Values -> time_log2 |
| --- | --- |
| H1 budget (h) | 72 -> 44.23; 504 -> 44.91; 1000 -> 45.43; 5000 -> 47.22; 10000 -> 48.13 |
| H1 rate (ops/s) | 2^33 -> 45.56; 2^35 -> 47.11; 2^35.8 -> 47.84 |
| H3 cost per start | 2^32.8 -> 46.13; 2^34 -> 46.22; 2^35 -> 46.34; 2^36 -> 46.50 |
| H3 yield mu | 2^9.5 -> 46.41; 2^10 -> 46.34; 2^11 -> 46.22 |

## 9. Memory and advice

TAB <= 16 x (2^19 + 2^16) x 32 bytes = 2^28.17; index 2^21 x 8 = 2^24; starts
96 bytes each (2^12 starts: 2^18.6); lists 2^17.6; code and buffers < 2^20.
Total < 2^28.3 bytes; with H4, memory_log2_bytes = 36. Advice: Table 6 and three
thresholds, < 2^12 bytes; starts, lists and G16 are computed and charged.

Limitations: the search, Phase 1 and Phase 2 were not rerun; no experiment
manifest (counts and simulations are stated derivations with repeatable
procedures); the ASIACRYPT full text was unavailable; the score rests on H1.
