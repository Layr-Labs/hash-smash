# SHA-256 reduced to 32 steps: ordinary collision by truncating the CRYPTO 2026 35-step attack

## 0. Claim, summary, verification checklist

Track `sha256-r32-exploratory`, profile `sha256-r32-prefix-v1`, `collision-frontier-v5`
(compression = 1 unit, word operation 1/2224).

| field | claimed | computed |
|---|---|---|
| time_log2 | 47.5 | 47.385 (§8) |
| preprocessing_log2 | 46.9 | 46.866 (§8) |
| memory_log2_bytes | 35 | 34.415 (§9) |
| success_probability | 0.39 | >= 0.512 (§7) |
| nonuniform_advice_log2_bytes | 13 | < 8 KB (§9) |

Summary. Collision of the complete 32-step hash (standard IV and padding, all 256 bits),
derived (not published) from the 35-step attack of Li, Liu, Wang, Shi (CRYPTO 2026, ePrint
2026/1080; "S"): conformance to S's characteristic through step 22 already collides 32 steps.
Our table TAB2 and exact Step-2 test give the first-block rate q (H1); second-block candidates
conform with p (H2). The total is dominated by a charged budget for S's unpublished
characteristic search (H3). Outputs are fully recomputed; only the success probability is
heuristic. No 32-step pair is known (no certificate). For reference, S's 35-step attack: 45
conditions, 2^27.415 valid tuples, 2^48.335 compressions; our attack phase (A+B, §8) is 2^45.66.
Novelty: we know of no published 32-step collision complexity; S (Sect. 3, Case-II) remarks that
a 32-step SFS attack could be converted to a collision but gives no complexity, and S's Tables
5-6 are a 32-step SFS characteristic and pair only. `sha256-r32-nominal-v2` is the organizer's
reference ID only.

Verification checklist:

1. Truncation: A/E rows 19-22 and W rows 23-34 are `=` (§2); Lemmas 1-2 (§3).
2. Conditions: 45 printed on steps 16-22 (§2) + necessary E16[29]=E17[29] (§6) = 46.
3. Sizes: TAB2 N = 1,396,774,912 = 2^30.379; P4 = 196,608 = 12 * 2^14 = 2^17.585 (§4).
4. H1 (§5): analytic q = 2^-45 * 214,235,406.8 = 2^-17.3254; measured 2^-17.3337, 99% lower
   bound 2^-17.3476; used 2^-17.36. Gain over S's 2^-20.92: TAB2 2^30.38 vs 2^29.18 tuples and
   exact Step-2 tests; C_35 control gives the same rate (§5, "Why q exceeds").
5. H2 (§6): cumulative rates 2^-3.000, 2^-14.999, 2^-21.002, 2^-28.15 vs predicted 2^-3, -15,
   -21, -28; p >= 2^-46 for 46 conditions.
6. r >= 2^-28.415 - 2^-49.3 = 2^-28.415 (1 - 2^-20) (§7).
7. s >= 2^-17.36 (1-2^-9.6) 2^-28.415 (1-2^-20) = 2^-45.777; T = 2^45.3; sT = 0.718;
   P >= 1 - e^-0.718 = 0.512 >= 0.39; cap K_max = 2^28.4 vs mean 2^27.98 valid tuples (§7).
8. Time: 2^45.400 + 2^43.036 + 6 + 2^36.5 + 2^35 + 2^46.865 (H3) = 2^47.385 <= 2^47.5 (§8).
9. Preprocessing: 2^36.5 + 2^35 + 2^46.865 = 2^46.866 <= 2^46.9 (§8).
10. Memory: 22,348,398,592 + 536,870,916 + 2^24 bytes = 2^34.415 <= 2^35 (§9).

## 1. Notation

32-bit words, + and - mod 2^32, FIPS 180-4 functions and message expansion. For CV = (a..h):
A[-1..-4] = (a,b,c,d), E[-1..-4] = (e,f,g,h), and

```
E[i] = A[i-4] + E[i-4] + Sigma1(E[i-1]) + IF(E[i-1],E[i-2],E[i-3]) + K[i] + W[i]
A[i] = E[i] - A[i-4] + Sigma0(A[i-1]) + MAJ(A[i-1],A[i-2],A[i-3])
```

C_32(CV,M) = CV + (A31,A30,A29,A28,E31,E30,E29,E28); steps 0..31 on every padded block from the
standard IV. Messages M0||M1 are 128 bytes; padding block P = 0x80000000, 14 zeros, 0x400.
Differences (S's notation, position k = bit 31-k): `n` x=0,x'=1; `u` x=1,x'=0; `=` equal;
`0`/`1` equal with that value. FL(X) = n/u mask; D(X) = sum_n 2^j - sum_u 2^j.
XOR-conformance at step i: the step equation on primed inputs (x' = x xor FL(x)) returns exactly
E[i] xor FL(E[i]) (resp. A). Sign values: bit 0 at `n`, 1 at `u`.

## 2. Characteristic (S, Fig. 6; all earlier rows are `=`)

```
 i nabla A[i]                       nabla E[i]                       nabla W[i]
 3 ================================ =====1=====011======0======0==== ================================
 4 ==n============================= ==n0=0=1===100=0==0=1===0==1=0=1 ==n=============================
 5 =====n===n===n=u====n===u==u==== 01011u001n=nuu=11000n=1=101u=100 =====u===u==========n===========
 6 ================================ 101n=0=1=1=n1111==n0u===n=0n=n=u ==n=============================
 7 ================================ 10u0=1=101==00=n==0=0===0==0=0=0 =======n=======u===u====u=1=u=u=
 8 ================================ uuu1=0=111=0=0=01=1=01==1==1=1=0 ============u=======uu==========
 9 ==========u====================u 11=10n0nuuu00n0u101=n11=u01u=unn ================================
10 ================================ un111111001001111=010u=u0+001100 ================================
11 ====n=========u=u=======u==n==== 1011n111100010u1u0111111u+nu1001 ================================
12 =un===u=n=======n=============== 001uuu11uuuuuuuu11n1000n1uuu1001 =====n===n==========u===========
13 ================================ =n1111uu1n00000u1u0=nnn01111010n ==u=============================
14 ==u============================= =0=100110000000=101=0000=110===0 ================================
15 ================================ =1====0011===u10001=011===0n===1 ================================
16 ================================ ======u=n====1==n=====0===01==== ================================
17 ================================ ======0=0====1==0==========1==== ================================
18 ================================ ==u===1=0=======1====1========== ================================
19 ================================ ==0============================= ================================
20 ================================ ==1============================= =====0=nn=====0=u=1=============
21 ================================ ================================ ================================
22 ================================ ================================ ==n=============================
23-34 all `=`                     (`+` in E10, E11 is undefined in S; read as `=`)
```

Two-bit conditions printed by S (X[a,b] = Y[c,d]: X[a]=Y[c], X[b]=Y[d]):

```
W4[1,8] != W4[12,25], W4[18] = W4[14], W5[0,1,30] = W5[28,18,9], W6[1,8] = W6[12,25], W6[18] != W6[14]
W7[22,13,23] != W7[18,9,8], W7[11,14,20] = W7[22,31,31], W8[0,14,21] = W8[28,25,6]
W8[31,23,30,15,22,8] != W8[27,2,15,26,7,4], W20[4,31] = W20[6,22], W20[31,30,25,21] != W20[1,0,16,14]
W22[4,31] = W22[6,22], W22[27] != W22[20]
E4[10] != E4[15], E5[3,21] = E5[8,8], E6[9,27,9,8] != E6[23,14,14,27], E6[1,1,23,6] = E6[6,15,10,25]
E7[21,10] != E7[3,15], E16[28,20,20,6] = E16[1,7,2,11], E16[30,28,10] != E16[12,10,29], E18[24] != E18[11]
E18[2] = E18[16]
A3[29] = A2[29], A3[29] != A5[29], A3[26,4] = A4[26,4], A3[22,18,16,11,7] != A4[22,18,16,11,7], A14[9] = A14[20]
A14[18,8] = A14[6,17], A13[30,25,23] = A14[30,25,23], A13[15] != A14[15], A13[29] != A15[29], A15[29] = A6[29]
```

Check on the pair of §10: all 362 non-`=` symbols and all `=` bits agree; 66 of 73 two-bit
conditions hold. The pair contradicts W20[4]=W20[6], W20[31]=W20[22] (dropped), both
E7 relations (read as `=`), A14[18,8]=A14[6,17] (read as !=), A15[29]=A6[29] (read as
A15[29]=A16[29], which absorbs A14[29] in MAJ at step 17). These readings only define the
precomputed sets; Steps 2-3 use exact equality tests.
Count on (A16, E16..E20, W20, W22): E16 7+7, E17 5, E18 5+2, E19 1, E20 1, W20 6+6, W22 1+3,
A16 1 = 45 (S's number); plus E16[29] = E17[29] (§6) = 46.

## 3. Truncation (ours)

Lemma 1. If A, E agree at steps 19..22 and W at 23..31, then C_32(CV,M) = C_32(CV,M').
Proof: (A[i],E[i]) is a function of (A[i-4..i-1], E[i-4..i-1], W[i]); induct over i = 23..31;
the feed-forward adds the common CV.
Lemma 2. If C_32(CV1,M1) = C_32(CV1,M1'), M1 != M1', then M0||M1 != M0||M1' have equal hashes
(same length, padding block and chaining value).
So conformance to §2 through step 22 and in W16..W31 gives a 32-step collision; S's Step-3
conditions are unchanged. The first block is compressed with C_32 (CV1 = C_32(IV,M0)); this does
not change the rate (C_35 control in §5). Our gain over S's rate comes from TAB2 and the exact
Step-2 test (§5, comparison paragraph).

## 4. Algorithm

Advice (S's starting solution), read from the x = M1' trajectory of S's pair (§10; Table 3's M1
is the xor-FL side) from CV1 = C_35(IV,M0); primed words are X xor FL(X):

```
A4..A13 = 98560dbb 633b16ba 9bcf7bbe f8677ad6 4a299906 44f24ab5 39781650 6422edc8 574542b8 0508c8f0
E8..E13 = f1cae594 d0e1b7b4 bf27d74c b78bbfd9 3fffd0f9 bf81c0f4      W12, W13 = 41b22a2c 6d12f88a
```

P1. L4: E4 with its single-bit conditions and E4[10] != E4[15] (131,072 of 2^18). L7: W7 with
its single-bit and six two-bit conditions (524,288 of 2^25).
P2. Each (E5,E6,E7) with its single-bit conditions (2^32): A3, A2, A1 from the A-equations of
steps 7, 6, 5; W9..W11 from E-equations 9..11; keep iff single-bit conditions on A1..A3,
W9..W11, two-bit conditions among known words, XOR-conformance of A 5..13, E 9..13: 10,240.
P3 (TAB2). Each kept combination and e4 in L4: A0, W8 from steps 4 (A), 8 (E); keep iff W8
conditions, two-bit conditions, XOR-conformance at steps 4 (A), 8 (E) (155,008 kept). Each such
pair and w7 in L7: E3 = E7 - A3 - w7 - Sigma1(E6) - IF(E6,E5,E4) - K7, A[-1] from step 3 (A);
keep iff E3 conditions, XOR-conformance at steps 3 (A), 7 (E), sigma0(W8') + W7' = sigma0(W8) +
W7 (zero W23 difference), remaining two-bit conditions. N = 1,396,774,912 16-byte records
(A[-1], three indices), bucketed in place by the top 27 bits of A[-1] (count pass, prefix sum,
placing pass; no sort buffer).
P4. E14 over its conditions (2^8), A14 conditions (12 left), E15 over its conditions (2^15),
A13[29] != A15[29]: 196,608 (W14,W15), 12 groups of 2^14 sharing W14 (S's count 2^17.585), all
XOR-conforming at steps 14-15; stored with sigma1 values and M0-free step-16 constants.

Main loop, T = ceil(2^45.3) trials:
1. Draw M0 uniformly (fresh random words); CV1 = C_32(IV,M0).
2. Step 2: for each record in the bucket with A[-1] = first word of CV1: E0..E2 from A-equations
   0..2, W0..W6 from E-equations. Accept (early abort, this order) iff (a) W4 sign value;
   (b) sigma0(W4') + W12' = sigma0(W4) + W12 (zero W19 diff.); (c) W5 sign values; (d) W6 sign
   value; (e) XOR-conformance of E 0..6 and A 0..2; (f) sigma0(W6') + W5' = sigma0(W6) + W5
   (zero W21 diff.); (g) (W13'-W13) + (sigma0(W5')-sigma0(W5)) + (W4'-W4) = D(W20).
3. Step 3, per valid tuple and P4 entry: M1 = (W0..W15), M1' = M1 xor FL(W); for i = 16..31
   with early abort require W'[i] = W[i] xor FL(W[i]) (and sign values at i = 20, 22), and for
   i <= 22 A'[i] = A[i] xor FL(A[i]), E'[i] = E[i] xor FL(E[i]). On success recompute both
   three-block hashes, compare 256 bits, output (M0||M1, M0||M1').
4. Stop after T trials or K_max = 2^28.4 Step-3 invocations. No restarts.

## 5. H1 `q-32step-matching-rate`: q >= 2^-17.36

Analytic. For a tuple t with A[-1] = a, the CV1 words b, c, d make E2 uniform (via b), E1 uniform
given b (via c), E0 uniform given b, c (via d). So W4 is uniform and independent of (E1, E2), W5
uniform and independent of (E2, W4), W6 = Y_t - E2 with Y_t = E6 - A2 - Sigma1(E5) -
IF(E5,E4,E3) - K6. Tests, predicted (measured in run 2):
(a) one bit of W4: 1/2 (0.5000); (b) sigma0 xor-diff of W4 is {11,22,26}, one sign pattern
cancels: 1/8 (0.1250); (c) three bits of W5: 1/8 (0.1250); (d) one bit of W6: 1/2 (0.5001);
(e) steps 0-4 E, 0-2 A: 1 (1.0000); step 5 depends on E2[29] only and step 6 is fixed per
tuple (0.6960, 0.4411); (f) sigma0 xor-diff of W6 {11,22,26} cancels D(W5): 1/8 (0.1246);
(g) sigma0 xor-diff of W5 {15,23,25} gives D(W20): 1/8 (0.1248).

Exact enumeration of TAB2: step 6 holds for all M0 or none (609,229,824 tuples, 43.6%, pass);
step 5 for exactly one e*(t) of E2[29]. P_t = Pr[E2[29] = e*(t), W6[29] = 0] over uniform E2:
q_pred = 2^-32 * 2^-1 * 2^-12 * sum_t ok6(t) P_t = 2^-45 * 214,235,406.8 = 2^-17.3254.
Check: predicted (e) given (d) 2 * 0.15338 = 0.3068, measured 0.3070 (1,675,075 / 5,456,132).

```c
ok6 = (E6 + (S1(E5^FL_E5)-S1(E5)) + (IF(E5^FL_E5,E4^FL_E4,E3)-IF(E5,E4,E3)) + D(W6)) == (E6^FL_E6)
ok5[e] = (E5 + (S1(E4^FL_E4)-S1(E4)) + (IF(E4^FL_E4,E3,e<<29)-IF(E4,E3,e<<29)) + D(W5)) == (E5^FL_E5)
e* = unique e with ok5[e]; y = Y_t mod 2^30; end = (y - e* 2^29) mod 2^30;
st = (end - 2^29 + 1) mod 2^30; P_t = |st - 2^29| / 2^30
```

Measured (our C code, not organizer-executed; xoshiro256** seeded by splitmix64 with s*1000 + 7919k
+ 104729R for seed s, thread k, step count R). TAB2 split in four parts by combination index mod 4.
Valid tuples (prediction): run 1 (seeds 11-14) 6,147 (6,269.6), 5,486 (5,405.5), 6,293 (6,341.6),
8,069 (8,135.2); run 2 (101-104, same predictions) 6,272, 5,309, 6,210, 8,268; run 3 (777, part 3,
2^30 - 4 trials) 1,921 (2,033.8, 2.5 s.d. low, kept); run 4 (15, part 3) 8,204. Each part run 2^32
- 4 trials. Pooled: 62,179 valid in 2^35.2 part-trials, q = 2^-17.3337, s.d. 0.41%, 99% one-sided
bounds 2^-17.3476 / 2^-17.3200, 0.58% below prediction (part z: -1.07, -0.15, -1.60, +0.14). 13
part-trials had 2 valid tuples, none 3. Controls (run 1 part 0): C_35 first blocks 6,355, uniform
CV1 6,415; only C_32 counts are used.

Why q exceeds S's published 2^-20.92 (by 2^3.56). S's TAB2 (Sect. 4) fixes A1..A13, E5..E13,
W9..W13 from its starting solution, re-enumerates only E5, E6, E7 (2^3, 2^4, 2^11 values) and then
W4, W7: 2^29.18 tuples, with sufficient bit conditions on W4..W6 in Step 2. Our P2 re-derives
A1..A3 from all 2^32 (E5,E6,E7) with single-bit conditions: 2^30.38 tuples; our Step 2 accepts
exactly the M0 that conform through step 6 with exact W19/W21 zero and W20 difference tests. The
C_35 control above gives the same rate as C_32, so the gain is from the table and the test, not
from truncation. W4..W6 affect later steps only via W19..W21 (tested) and additively in W22 with
fixed difference, so accepting more M0 does not change what Step 3 must achieve.
Assumptions: C_32(IV,M0) words act as uniform here; the (f) sign pattern is independent of the
W6/E2 conditioning.

## 6. H2 `step3-46-conditions`: p >= 2^-46

Pooled runs 1-4: 12,224,888,832 = 62,179 * 196,608 candidates. Predicted counts at stages
16-21: 1,528,111,104; 373,074; 5,829; 45.5; 2.8; 1.4.

```
stage (tests A_i, E_i)   conditions consumed              pred.  count          rate
16                       3 of E16's 14                    2^-3   1,528,108,551  2^-3.000
17                       other 11 of E16, A16             2^-15  373,324        2^-14.999
18                       E17 (5), E18[29]                 2^-21  5,823          2^-21.002
19                       other 6 of E18, E16[29]=E17[29]  2^-28  41             2^-28.15
20 (+ W20, 3 signs)      W20 signs (3), E19[29]=0         2^-32  5              2^-31.19
21                       E20[29]=1                        2^-33  4              2^-31.51
22+ (+ W22, W23..W31)    other W20 (9), W22 (4)           2^-46  0
```

Step 18: IF(E17,E16,E15) absorbs the E16, E15 differences, so E18'-E18 = A14'-A14 = -2^29,
conforming iff E18[29] = 1. Step 19: IF(E18,E17,E16) at bit 29 gives E17[29] in one computation and
E16[29] in the other; all other E19 differences total < 2^25 and cannot cancel 2^29, so E16[29] =
E17[29] is necessary (unprinted; the pair has it; 41 observed vs 45.5 with it, 91 without). Step
20: E19[29] = 0 absorbs E18[29]; D(E16) + D(W20) = 0xfe808000 + 0x017f8000 = 0. Step 21: E20[29]=1.
The other 13 conditions control carries of sigma1(W20) in W22 and sigma1(W22) in W24. Tail Monte
Carlo (2^21 samples, the pair's (W6,W7,W8) differences): W20 signs 2^-3.00, then W22 2^-7.94, then
W24 = W24' 2^-3.07: 2^-11.0 vs 2^-13 charged. W27-W29 cancel deterministically. Printed-condition
check (run 4, 1,612,972,032 candidates): E16+A16 49,332 (independence 49,224), +E17 1,514 (1,538),
+E18 9 (12.0). No full conformance observed or expected (2^33.5 candidates). S's pair (own tuple
and CV1) passes Steps 2-3 in every run.

## 7. Success probability

Trials are independent given the tables: P >= 1 - exp(-sT), s >= Pr[V >= 1] r (V = valid
tuples per trial). Pr[V >= 1] >= q - E[C(V,2)]; 13 same-part pairs in 4 * 2^32 part-trials =
2^-28.3 per trial, x2.5 for cross-part pairs: E[C(V,2)] <= 2^-27 = q 2^-9.6.
X = conforming P4 candidates, E[X] = 2^17.585 * 2^-46 = 2^-28.415. Candidates sharing W14 share
the 12 W20 conditions, charged once per group: E[C(X,2)] <= 12 C(2^14,2) 2^-12 (p 2^12)^2 +
C(196,608,2) p^2 = 2^-49.42 + 2^-57.83 <= 2^-49.3; r >= E[X] - E[C(X,2)] >= 2^-28.415 (1-2^-20).
log2 s >= -17.36 - 0.002 - 28.415 = -45.777; sT = 2^-0.477 = 0.718; P >= 0.512 >= 0.39.
Margin: q 2^0.1 lower and p 2^0.4 lower together give sT = 0.508, P = 0.398.
K_max: mean valid tuples <= T 2^-17.320 = 2^27.98; Pr[> 2^28.4] < exp(-0.338^2 2^27.98 / 3).

## 8. Time and H3, H4

Ops: load/store/logic/shift/compare/branch 1, add 2, rotation 4, Sigma/sigma 14; 2224 ops = 1 unit.

| term | derivation | log2 |
|---|---|---|
| A trials | 2^45.3 (1 + 160/2224); 160 >= 34 (M0) + 50 (lookup) + 0.3252 * 192 (Step 2) | 45.400 |
| B Step 3 | 2^28.4 (300 + 196,608 * 288) / 2224; 288 = 32 + 2048/8 (1/8 pass stage 16) | 43.036 |
| final check | 6 compressions | 2.585 |
| C P1-P4 | 1024 ops/iter (<= 6 eqs * 60 + 71 tests * 4 ~ 650) over 2^32 + 2^30.32 + 2 * 2^36.24 + small = 2^36.17; 2^30.32 = 10,240 * 2^17, 2^36.24 = 155,008 * 2^19 | 36.5 |
| D Step 1 (H4) | S's 2^34.3, unit unstated; 2^0.7 > 2476/2224 covers 35-step units | 35.0 |
| E search (H3) | 2,304 h * 3,600 * 2^35 / 2224 = 2^(22.984 + 35 - 11.119) | 46.865 |
| total | | 47.385 |

Step 2 per match: 160 ops, then 40, 40, 40, 1024 ops paid by fractions 1/2, 1/16, 1/128, 1/256
(§5): 186.8 <= 192; lookup 10.41 records/bucket at 4 ops. C+D+E = 2^46.866; A+B = 2^45.66.
H3 `trail-search-budget`: S gives no search time. S runs 8 minimisation tasks (Sect. 3 Model-1,
Model-2 in two phases, Model-3; Sect. 4 Steps 1-4), each a tightening series of solver calls.
Charged: 4 calls per task (our assumption) at the 72-hour per-call limit stated by the same
first three authors for the same tool (ePrint 2024/349, Sect. 4.3), one thread each: 2,304 h.
Model-3 and Step 1 share an objective but are charged twice; each task ends with a call
returning no solution. 2^35 ops per thread-second exceeds the peak of S's 2x EPYC 9354 (Zen 4:
<= 6 macro-ops, so <= 8 instructions per cycle; 3.8 GHz * 8 = 2^34.82). Unknowns: calls per task,
threads per call (each thread would count), starting t_r threshold (final A-weight 21).

```
search budget   2^44 units   1,152 h   2,304 h (charged)   4,608 h or 2^36 ops/s   9,216 h
total log2      46.06        47.06     47.38               48.15                   49.01
```

H4 `starting-solution-cost` (supporting): term D; the advice is S's single Step-1 solution.
Fallback: S's rate 2^-20.92 (T = 2^48.86) would give 2^49.28; not scored.

## 9. Memory and advice

TAB2 N * 16 = 22,348,398,592 bytes; offsets (2^27+1) * 4 = 536,870,916; other tables, code and
state < 2^24: total 2^34.415 -> 35. Advice < 8 KB -> 13.

## 10. S's 35-step pair (Table 3), recomputed

```
M0  = a8850273 c0f4a504 5d3ad7b5 6e5f5026 535cc256 e92ef7a5 436f70df 7d7e236a
      cadc14e8 d59ac191 6874f1ba 6b83960d f6dfe9de 6a013df2 f856b739 237894e8
M1  = c0008214 ae65f3bf e93c006a 5f195aa9 a4d6cd0f 21811cec ea897317 db9ec665
      6ec17218 5100da8a 0912e57b a96b2054 45f2222c 4d12f88a d2701ecc 140976d1
M1' = c0008214 ae65f3bf e93c006a 5f195aa9 84d6cd0f 25c114ec ca897317 da9fd6ef
      6ec97e18 5100da8a 0912e57b a96b2054 41b22a2c 6d12f88a d2701ecc 140976d1
```

35-step padded digests equal (8b32c7f0...18c51c5d). From CV1 = C_35(IV,M0): differences in
W{4-8,12,13,20,22}, A{4,5,9,11,12,14}, E{4-13,15,16,18}; C_32(CV1,M1) = C_32(CV1,M1') =
22b41993...0d403a72 (Lemma 1; SFS only, not claimed). 32-step padded digests differ
(97301898...25f3006e, 9a99b338...e5e83f16).
