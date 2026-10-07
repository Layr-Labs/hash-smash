# sha256-r31: first-block matching with the W20 condition relaxed

## 1. Claim

Track `sha256-r31-exploratory`, target `sha256-r31-prefix-v1` (ordinary collision, SHA-256 steps
0..30 on every padded block, standard IV, FIPS padding, all eight digest words), cost model
`collision-frontier-v5` with C = 2140 (one 31-step compression = 1 unit, any other 256-bit word
operation = 1/2140 unit), review policy `paired-lanes-v1`, exploratory lane.

The scored program is the randomised algorithm A of Section 7. It tries N = 507,124,908,032 first blocks
(2^38.884). With probability at least 0.4 it outputs two distinct 128-byte messages with equal
sha256-r31 digests.

A uses the two-phase framework and the 31-step trail of Li, Liu, Wang, Dong and Sun (ASIACRYPT
2024). It makes one change. The trail realises dW20 = 0 with one fixed pair of sigma-differences
(W5 in a set of 2^14 words, W18 in a set of 2^25.34). A only requires that the two sigma-differences
cancel, which is exactly what dW20 = 0 means. For one matched record, this raises the post-match
acceptance probability from 2^-27 * 0.136 = 2^-29.88 to 2^-9 * 2^-12.662 = 2^-21.662. As a
result, a single starting solution (the one inside the published pair) gives a table of only 16896
records, and that table is enough.

| field | value | where |
|---|---|---|
| time_log2 | 39.65 | ledger 2^39.6429 plus slack, Section 9 |
| preprocessing_log2 | 38.33 | C0, C1 allowances and table work, Section 9 |
| success_probability | 0.4 | Section 8 |
| nonuniform_advice_log2_bytes | 11 | trail and starting solution, Section 11 |
| memory_log2_bytes | 32 | reported only, Section 11 |

Every premise the bound uses is declared as a heuristic in Section 10 (H1-H7), with its evidence.
The evidence includes:
- a 2^40.62-trial run of A's online loop (Section 8.2);
- an exhaustive and sampled computation of the relaxed acceptance probability (Section 8.1);
- one colliding pair found by that run, attached as a certificate;
- an organizer-executed completion experiment (`experiments/manifest.json`, Section 8.4).

## 2. Target, written out

All words are 32-bit; `+` and `-` are modulo 2^32; ROTR is right rotation.

    S0(x) = ROTR(x,2) ^ ROTR(x,13) ^ ROTR(x,22)      s0(x) = ROTR(x,7) ^ ROTR(x,18) ^ (x >> 3)
    S1(x) = ROTR(x,6) ^ ROTR(x,11) ^ ROTR(x,25)      s1(x) = ROTR(x,17) ^ ROTR(x,19) ^ (x >> 10)
    IF(x,y,z) = (x & y) ^ (~x & z)                   MAJ(x,y,z) = (x & y) ^ (x & z) ^ (y & z)

Schedule: W[0..15] are the block words (big-endian); W[t] = s1(W[t-2]) + W[t-7] + s0(W[t-15]) + W[t-16]
for t = 16..30. Constants K[0..30] are the first 31 FIPS 180-4 constants.

We write the compression in the one-register form used by the source papers. The incoming chaining
value (a,b,c,d,e,f,g,h) is renamed (A[-1],A[-2],A[-3],A[-4],E[-1],E[-2],E[-3],E[-4]). For i = 0..30:

    E[i] = A[i-4] + E[i-4] + S1(E[i-1]) + IF(E[i-1],E[i-2],E[i-3]) + K[i] + W[i]
    A[i] = E[i] - A[i-4] + S0(A[i-1]) + MAJ(A[i-1],A[i-2],A[i-3])

This is the standard step: E[i] = d + T1 and A[i] = T1 + T2. The output chaining value is
(a+A[30], b+A[29], c+A[28], d+A[27], e+E[30], f+E[29], g+E[28], h+E[27]). The IV is the standard
one, used once. A 128-byte message is followed by one FIPS padding block (0x80, zeros, bit length
1024), so it is hashed as three compressions. The digest is the final chaining value, big-endian.
This matches `verifier/hash_functions.py:digest` with ("sha256", 31).

## 3. Advice: the trail and the starting solution

A runs no trail search and no solver. It takes two fixed objects as nonuniform advice; both were
published by Li, Liu, Wang, Dong and Sun. A uses exactly one starting solution (N_start = 1).

(a) The signed 31-step trail of Section 4. Its provenance is pinned as follows. The authors' public
SAT/SMT implementation is github.com/Peace9911/sha_2_attack at commit
6a9f35fd8d8bdcc1a54dc6f170ed0038ebe5bb32. Its script `find_dc/find_dc_model_31_256.py` searches the
characteristic with message-difference positions {5,6,7,8,9,16,18}, steps 5..18, and objective
weight starting at 60 and decreasing until the STP/CryptoMiniSat query becomes unsatisfiable.
`find_dc/correct_dc_model_31_256.py` adds the value conditions. A does not run these programs; they
only identify the computation whose cost C0 charges.

(b) One starting solution S for steps 1..12. It is read off the published colliding pair: running
that pair's second block from its chaining value yields S. Copy P of S is

    A1..A12 : f36e6fcf b741c202 90c67413 fc7566c3 fa9053fb 11af5d4e 87f5120c 9180b607
              4f5af3a8 4b9e4fb8 83e817e6 2be31c3f
    E5..E12 : 1d1fa7dd afe878e7 4c97cbe5 946f8048 61c171d3 f02293fa aa270418 b1f7f9e8
    W9..W12 : eb830a58 66add94a 9669232d 45271fa5

Copy P' adds the modular differences of Section 4 (A5 fffff006, A6 ff800001, A7 0edfeffd,
A8 fffffffc, A10 00008004, E5 fffff006, E6 fff87fff, E7 4f880387, E8 44ff8804, E9 00000008,
E10 ef808008, E11 10bffff8, E12 ffff7ff8, W9 00008004). S satisfies every cell of rows 5..12 and
W9 in V9. Its step-8 and step-13 difference relations hold: E13 and A13 get difference 0.

Neither object is free. The cost model charges the construction of advice, including searches that
the submitted program does not run. We do not specify or re-run those searches. Instead we charge a
fixed construction allowance for each, as ledger lines C0 (the trail) and C1 (the starting solution)
in Section 9, under heuristics H1 and H2. Given the advice, every step of A below is fully specified
and deterministic apart from its coins.

## 4. The differential characteristic

Each cell describes one bit (bit 31 on the left) of a word in copy P and copy P':
`=` the bits are equal; `0` / `1` both bits equal that value; `u` the bit is 0 in P and 1 in P';
`n` the bit is 1 in P and 0 in P'. Rows are the step index i. Rows -4..2, 17 and 19..30 are all `=`
in every column and are not listed.

    i  | A[i]                             | E[i]                             | W[i]
    3  | ================================ | ==========================10==== | ================================
    4  | ================================ | ============0===0=========01===0 | ================================
    5  | ===================n=unnnnnnn=n= | 000111010001111110nu=11111unnnu1 | ================nuuu=======0=uu=
    6  | ========n======================u | 101011=11==0n0==u11110==1110011n | ==========u=====u===u======n===u
    7  | ===u===n==n========n=========n=u | un0u1100n=01u11111001u1=n110u10n | =u=u=======n=====n=nu=n=====nun=
    8  | =============================n== | 1u01un0u0=1=1=11n=0=u0=001001u0= | =u=nn==========u===u===u==1=====
    9  | ================================ | 01100001110=0=010===00=11101u0=1 | ================u==========1=u==
    10 | ================u============u== | =1n1uuuuu0100=1un0=10unnnnnnn010 | ================================
    11 | ================================ | =01u1010uu1==11100===1000001n=0= | ================================
    12 | ================================ | ==110001=11====1n====0011110n=0= | ================================
    13 | ================================ | ===0====01======1=============== | ================================
    14 | ================================ | ================u===========0u== | ================================
    15 | ================================ | ================0============1== | ================================
    16 | ================================ | ================1============1== | =============unnnunnnnnnnnnnnn==
    18 | ================================ | ================================ | ==============1=n=0==========n==

The table has 300 non-`=` cells: 180 value cells (`0`/`1`) and 120 signed-difference cells
(`u`/`n`). Per row, (A, E, W) cells are: 3:(0,2,0) 4:(0,5,0) 5:(10,31,7) 6:(2,25,5) 7:(6,30,10)
8:(1,25,7) 9:(0,25,3) 10:(2,29,0) 11:(0,24,0) 12:(0,19,0) 13:(0,4,0) 14:(0,3,0) 15:(0,2,0)
16:(0,2,17) 18:(0,0,4). Evaluating every one of the 300 cells on the published pair (certificate `published-31step-pair`, second block from its chaining value) gives zero violations.

Modular differences X' - X implied by the table and observed on the pair:

    W:  d5 = fffff006  d6 = 002087f1  d7 = 4fefb5fa  d8 = 28011100  d9 = 00008004
        d16 = 00008004 d18 = ffff7ffc  (every other W[t], t <= 30, has difference 0)
    A:  A5 fffff006  A6 ff800001  A7 0edfeffd  A8 fffffffc  A10 00008004
    E:  E5 fffff006  E6 fff87fff  E7 4f880387  E8 44ff8804  E9 00000008
        E10 ef808008 E11 10bffff8 E12 ffff7ff8 E14 00008004

The table is the published 31-step trail (ASIACRYPT 2024 presentation, slide 14), transcribed
cell by cell; rows 3 and 4 carry value conditions on E[3] and E[4] and are kept.

## 5. Exact difference requirements, and the relaxed W20 condition

5.1 Message expansion. In the second block only W5..W9 differ, by d5..d9. For t = 16..30, every
term not shown below has difference 0.

    t=16: W9 enters directly: dW16 = d9.
    t=18: s1(W16) term: dW18 = s1(W16+d9) - s1(W16). Need W16 in G16, so that dW18 = d18.
    t=20: s1(W18) and s0(W5) terms: need s1(W18+d18) - s1(W18) + s0(W5+d5) - s0(W5) = 0.   (R20)
    t=21: need s0(W6+d6) - s0(W6) = -d5 = 00000ffa                 (W6 in V6)
    t=22: need s0(W7+d7) - s0(W7) = -d6 = ffdf780f                 (W7 in V7)
    t=23: need s0(W8+d8) - s0(W8) = -(d9+d7) = b00fca02            (W8 in V8)
    t=24: need s0(W9+d9) - s0(W9) = -d8 = d7feef00                 (W9 in V9; true for S)
    t=25: d18 + d9 = 0.  t=17, 19, 26..30: no term has a difference.

The published trail satisfies R20 with one specific pair: s0-difference d0018020 for W5 (2^14
words) and s1-difference 2ffe7fe0 for W18 (2^25.34 words). A keeps R20 itself and lets the two
sigma-differences take any pair of values that cancels. R20 is exactly the requirement dW20 = 0.
W5 and W18 enter the state update only additively, through their modular differences d5 and d18,
and those stay the same. So the state conditions of the trail are untouched. The W-row cells of
Section 4 for W5 and W18 may then fail; they are not needed.

Set sizes, from enumerating all 2^32 words: |V6| = 2^23, |V7| = 512, |V8| = 49408, |V9| = 35921920,
|G16| = 64. G16 is the set of (h << 28) | lo with h = 0..15 and lo in {031bbffc, 064bbffe, 09b3bffd,
0ce3bfff}. s1 is an invertible GF(2)-linear map (rank 32).

5.2 Why an output pair collides. Suppose dW = d5..d9 at steps 5..9, d9 at step 16, d18 at step 18
and 0 elsewhere. Suppose also that the state differences of steps 5..17 follow the trail: the
modular differences of Section 4 and dE[i] = dA[i] = 0 from step 13 on, except dE14 = 00008004. Then
step 18 cancels dE14 against dW18, and steps 19..30 carry no difference. Both copies start the second
block from the same chaining value, so their outputs are equal. The padding block is shared, so the
digests are equal. For steps 0..13 these relations follow from the construction. W0..W8 are chosen
so that copy P reproduces S, the record and the derived E0..E2. S carries the trail's step 8..13
relations, and P2 checks F6 and F7. O5 checks steps 14..17 explicitly. O6 then re-hashes the output
pair, so any pair A outputs is a verified collision.

5.3 Size of the relaxed acceptance event. Let p5(c) be the fraction of 32-bit words w with
s0(w+d5) - s0(w) = c. We computed p5 exhaustively: 6,580,932 distinct values, each of probability
at most 2^-8. For a uniform c18, set W18(g) = s1(g) + c18 for each g in G16. Then

    P_any = Pr_{W5, c18 uniform, independent}[ exists g in G16 : s1(W18(g)+d18) - s1(W18(g)) = -(s0(W5+d5) - s0(W5)) ]
          = E_{c18}[ sum over the distinct values v of s1(W18(g)+d18) - s1(W18(g)) of p5(-v) ].

We estimated P_any with 268,435,452 (just under 2^28) uniform c18 samples, using the exact p5 table. The mean is
1.5431e-04 = 2^-12.662, the standard error is 4.56e-08, and the 99% lower bound is
2^-12.663 (Section 8.1). For comparison, the trail's own choice gives 2^-18 * 0.136 = 2^-20.88.

## 6. Preprocessing (charged)

P1 (sets). Scan all 2^32 words once and keep V7, V8 and G16. V6 and R20 are tested directly at
use time, so they need no table.

P2 (table). From S, for each W8 in V8:
  E4 = E8 - A4 - S1(E7) - IF(E7,E6,E5) - K[8] - W8.
  Keep W8 if the row-4 cells hold on E4 and if F7 holds:
  (E7'-E7) = (S1(E6')-S1(E6)) + (IF(E6',E5',E4) - IF(E6,E5,E4)) + d7.
  Then A0 = E4 - A4 + S0(A3) + MAJ(A3,A2,A1).
For each kept W8 and each W7 in V7:
  E3 = E7 - A3 - S1(E6) - IF(E6,E5,E4) - K[7] - W7.
  Keep W7 if the row-3 cells hold on E3 and if F6 holds:
  (E6'-E6) = (S1(E5')-S1(E5)) + (IF(E5',E4,E3) - IF(E5,E4,E3)) + d6.
  Then A[-1] = E3 - A3 + S0(A2) + MAJ(A2,A1,A0).
Store (A[-1]; A0, E3, E4, W7, W8). This gives 1632 kept W8 values and 16896 records with about 2,450
distinct keys. The published pair's own record is among them. The records are sorted by key, and a
2^24-bit bitmap is built on key >> 8.

## 7. Algorithm A (the scored program)

Parameters: N = 507,124,908,032 trials, completion caps L13 = 2^14 and L15 = 2^8.

O1 (first block). Trials come in groups of 2^24. For each group, A draws words 0..14 of M0 as fresh
uniform coins. Within the group, word 15 runs from 0 to 2^24 - 1. Compute
CV1 = compress31(IV, M0), which gives A[-4..-1] and E[-4..-1]. In the measured run (Section 8.2)
the coins came from a fixed seed (splitmix64, seed 31a7ed2026100701) so that it can be reproduced.

O2 (lookup). If bitmap bit (A[-1] >> 8) is clear, go to the next trial. Otherwise binary-search the
records with key A[-1].

O3 (derive). For each matching record:
  E0 = A0 + A[-4] - S0(A[-1]) - MAJ(A[-1],A[-2],A[-3])
  E1 = A1 + A[-3] - S0(A0) - MAJ(A0,A[-1],A[-2])
  E2 = A2 + A[-2] - S0(A1) - MAJ(A1,A0,A[-1])
  W[i] = E[i] - A[i-4] - E[i-4] - S1(E[i-1]) - IF(E[i-1],E[i-2],E[i-3]) - K[i]   for i = 0..6
W7 and W8 come from the record, and W9..W12 from S.

O4 (tests). Require W6 in V6. Then require some g in G16 with
  s1(W18(g)+d18) - s1(W18(g)) = -(s0(W5+d5) - s0(W5)), where W18(g) = s1(g) + W11 + s0(W3) + W2.
That is R20 with W16 = g. Take the first such g.

O5 (completion). Set W14 = s1^-1(g - W9 - s0(W1) - W0), so that W16 = g.
Up to L13 times:
  - draw E13 with bits 28, 23 = 0 and bits 22, 15 = 1 (the row-13 cells), other bits random;
  - set W13 = E13 - A9 - E9 - S1(E12) - IF(E12,E11,E10) - K[13];
  - compute E14 in both copies and require dE14 = 00008004;
  - require the step-15 sum A11 + E11 + S1(E14) + IF(E14,E13,E12) to agree in both copies.
  On success, up to L15 times:
  - draw E15 with bit 15 = 0 and bit 2 = 1, set W15 from the step-15 equation;
  - require dE16 = 0 and IF(E16,E15,E14) = IF(E16,E15,E14').
If both loops succeed, the step relations of Section 5.2 hold.

O6 (output). Form M1 = (W0..W15) and M1' = M1 + (d5..d9 at words 5..9). Hash M0||M1 and M0||M1'
under sha256-r31. If the digests are equal, output the pair and stop. If a check fails, continue with
the next record or trial. After N trials without output, output nothing. That is the only stopping
rule; nothing else is adaptive.

Lemma 7.1 (independence after a match). Fix a record and condition on A[-1] being its key.
- W6 = const - A[-2]. So W6 is a bijective function of A[-2].
- W5 = const - A[-3] + MAJ(A0,A[-1],A[-2]) - IF(E4,E3,E2). For fixed A[-2], W5 is a bijection of
  A[-3].
- W2 = (E2 - A[-2]) - E[-2] - S1(E1) - IF(E1,E0,E[-1]) - K[2], where E2 - A[-2] is constant. For
  fixed (A[-2], A[-3], A[-4], E[-1]), W2 is a bijection of E[-2].
- c18 = W11 + s0(W3) + W2. For fixed W3, c18 is a bijection of W2.
So if (A[-2], A[-3], A[-4], E[-1], E[-2]) are independent and uniform, then W6, W5 and c18 are
independent and uniform. This is pure algebra. The only premise is the distribution of CV1, which
is heuristic H3.

## 8. Success probability and the measurements behind it

Write rho = 16896 / 2^32 = 2^-17.958 for the expected number of matching records per trial, as in
H3(a). Under H3 and Lemma 7.1, the V6 test and the R20 test are independent for a matched record.
So the record passes O4 with probability q4 = (V6 rate) * (R20 rate); under the model this is
2^-9 * P_any. It then completes in O5 with probability kappa (H5). The expected number of successes per trial is
p = rho * q4 * kappa. A trial matches about 7.2 records sharing one key (at most 16). Their V6
outcomes are strongly shared, but their R20 outcomes are close to independent. Given one R20 pass,
the expected number of further R20 passes in the same trial is c = 296/292,413 = 0.0010. This was
measured by evaluating whole key clusters for 2.6 * 10^8 keys under the H3 model; the real-process
check in Section 8.2 found no trial with two R20 passes. By Bonferroni, one trial succeeds with
probability p1 >= p * (1 - c/2) >= p * (1 - 2^-8). Trials are independent under H3(c). So
  Pr[A outputs a collision] >= 1 - (1 - p1)^N >= 1 - exp(-N * p1).

Values used. Each factor is the smaller of the model value and the 99% lower bound measured in the
real run of Section 8.2, so the bound does not rest on the model alone:
- rho = 2^-17.9596;
- the V6 rate = 2^-9.0364;
- the R20 rate = 2^-12.8510. The model value is P_any = 2^-12.663, its 99% lower bound
  from Section 8.1;
- kappa = 0.99999 (lower bound, Section 8.3);
- the product of the V6 and R20 rates uses the independence of Lemma 7.1, checked in Section 8.2.
- p1 >= 1.0073e-12 = 2^-39.853;
- N = 507,124,908,032 gives N * p1 >= 0.5108, so the success probability is at least 0.4000 >= 0.4.

8.1 P_any. An exhaustive histogram of p5 (2^32 words) is combined with 268,435,452 sampled c18
values: mean 2^-12.662, standard error 4.56e-08, 99% lower bound 2^-12.663.

8.2 Run of the online loop. We ran O1-O6 exactly as specified, with 12 threads and seed
31a7ed2026100701, for a fixed 2701 seconds with no early stop. All counts:

    trials (first blocks)          1695634423904 = 2^40.625
    matched records                6658886  per trial 6658886/1695634423904 = 2^-17.958 (99% interval 2^-17.960 .. 2^-17.957)
    V6 passed                      12975  per record 12975/6658886 = 2^-9.003 (99% interval 2^-9.036 .. 2^-8.971)
    relaxed R20 test passed        982  per record 982/6658886 = 2^-12.727 (99% interval 2^-12.851 .. 2^-12.613)
    both tests passed              1  (expected 2.01)
    completion (wide caps)         982/982
    collisions found and verified  1
  synthetic matched records under H3 (Section 8.3), 5851119616 samples:
    V6 11427620/5851119616 = 2^-9.000 (99% interval 2^-9.001 .. 2^-8.999); R20 902232/5851119616 = 2^-12.663 (99% interval 2^-12.667 .. 2^-12.659); both 1760/5851119616 = 2^-21.665 (99% interval 2^-21.756 .. 2^-21.579)
    completion with caps L13, L15  902232/902232; second-block collisions from both-passing samples 1760/1760

Independence check on real record hits. A separate 200-second run of the same loop
(seed 3b7e1d2026100705) took the first matched record of each trial, so the samples are independent
across trials. It tallied the top 4 bits of W6, W5 and c18, and the V6 indicator. Lemma 7.1 predicts
that these words are independent and uniform. Chi-square independence tests:

    W6xW5   n = 19,008: chi2 = 240.0 on 225 df (z = +0.71)
    W6xc18  n = 19,008: chi2 = 213.4 on 225 df (z = -0.55)
    W5xc18  n = 19,008: chi2 = 189.4 on 225 df (z = -1.68)
    V6xW5   n = 19,008: chi2 = 6.1 on 15 df (z = -1.63)
    V6xc18  n = 19,008: chi2 = 13.6 on 15 df (z = -0.25)
    (same run: 34,808,528,912 trials, 19,008 key-matched trials, 137,709 records; trials with 0/1/2+ R20 passes: 18980/28/0)

An earlier 121-second run pooled every matched record (top 6 bits). Its W6 x W5 table
gave z = 10.50, while every other table passed. That is the expected artefact of pooling:
records of one trial share almost the same W6 (V6 outcomes cluster: 5.0 further V6 passes per V6
pass in the cluster model), so pooled samples are not independent. With one record per trial the
dependence disappears (above).

These are the per-record rates in the actual process. The relaxed test passed for
2^-12.727 of matched records (prediction 2^-12.662). The V6 test passed for
2^-9.003 (prediction 2^-9). Matched records per trial were 2^-17.958 (prediction
2^-17.958). The run found 1 collision, against 2.01 expected. It is attached as
certificate `relaxed-run-1`. 

8.3 Completion. O5 was attempted on every record that passed the relaxed test, whether or not V6
held, and succeeded in 982/982 cases in the run. A synthetic check that sampled
matched records under H3 gave 902232/902232 with the caps L13 and L15 exactly as in O5. We use kappa >= 0.99999.

8.4 Organizer-executed experiment `r31-completion`. For each organizer seed, `experiments/completion.py`
picks an accepted match: one of the 2 prefixes in the program, by trial index. It then runs
O5 with E13/E15 draws taken from SHAKE-256(seed) and returns the two messages. The organizer
re-hashes every returned pair. Locally, 256 of 256 seeds gave distinct full collisions in under 1
second.

## 9. Cost ledger (collision-frontier-v5, C = 2140)

Time is total work over all processors.

    C0  construction of the trail (advice), allowance (H1)                  2^38        = 274,877,906,944
    C1  construction of S (advice), allowance (H2)                          2^36        =  68,719,476,736
    P1  three 2^32 scans, <= 24 ops per word: 3*2^32*24/2140                2^27.107    =     144,503,573
    P2  table: 49408 + 1632*512 = 884,992 candidates, <= 64 ops each,
        plus sort and a 2^24-bit bitmap (2^16 word stores): < 2^26 ops     < 2^15      =          32,768
    O1-O2 per trial: 1 compression + <= 32 ops (counter, bitmap index and
        test, loop control; per-group PRNG amortised): N * (1 + 32/2140)  514,708,084,227
    O3-O4 per matched record (rho per trial): <= 400 ops; R20 test only
        after V6 passes (2^-9): <= 1600 ops: N*rho*(400 + 1600/512)/2140   375,807
    O5 per accepted match (p/kappa per trial): <= L13*80 + L13*L15*80 ops   94,715
    O6 hashing the output pair: 6 compressions                              6
    -------------------------------------------------------------------------------------------
    preprocessing C0+C1+P1+P2                                               343,741,920,021 = 2^38.3225
    total                                                                   858,450,474,776 = 2^39.6429

Claimed time_log2 = 39.65 and preprocessing_log2 = 38.33. 2^39.65 exceeds the
total by 4,208,863,830 units (2^31.97).

Per-trial work is charged as a full 31-step compression. The implementation used in Section 8.2
shares steps 0..14 across a group, so it does less work than this. No discount is taken.

## 10. Heuristics (every premise of the bound)

H1-trail-cost (score-critical). Constructing the trail of Section 4, which A receives as advice,
costs at most 2^38 units (ledger line C0).
- Evidence: a public re-run of the authors' open-source four-stage trail search for this trail
  (STP with CryptoMiniSat; solver Th0rgal, submission 25088ab7) used 29 calls and 16,580.78
  CPU-seconds, with stages 1-3 reproducing the published optima.
- That is 2^36.60 units at that report's conversion (2^22.58 units per CPU-second). A hardware
  ceiling of 6 instructions per cycle at 5.5 GHz gives 2^37.90.
- Limitation: the authors' original exploration may have covered more trails than the re-run.

H2-start-cost (score-critical). Constructing S, which A receives as advice, costs at most 2^36
units (ledger line C1).
- Evidence: the same report gives 178.4 CPU-seconds for one comparable starting-solution solve,
  which is 2^30.06 units.
- 2^36 covers 61 such solves. That is the whole set of about 54 starting points behind the
  authors' 2^19.8-record table, so choosing S among them is also covered.

H3-random-cv (score-critical). For the distinct first blocks of O1, the 31-step chaining values
behave as independent uniform 256-bit values. This gives:
  (a) rho records matched per trial in expectation;
  (b) through Lemma 7.1, independent uniform (W6, W5, c18) after a match;
  (c) independent trial outcomes.
- Evidence: the run's measured rates (Section 8.2) agree with (a) and (b) within their confidence
  intervals.
- The byte-level independence tests of (W6, W5, c18) on real matched records show no dependence.
- The synthetic check under the same premise reproduces the joint rate.

H4-pany (score-critical). A matched record passes the R20 test with probability at least
2^-12.8510. This is the smaller of two values:
- the model value P_any >= 2^-12.663: a sampled estimate of a fixed finite quantity, built on an
  exact histogram (Section 8.1);
- the 99% lower bound measured on the real process (Section 8.2).

H5-completion (score-critical). O5 succeeds within the caps L13 and L15 with probability at least
kappa = 0.99999 per accepted match.
- Evidence: 982/982 in the run, the synthetic check, and the organizer experiment
  `r31-completion`.

H6-op-counts (supporting). The per-trial, per-record and per-completion word-operation bounds of
Section 9 cover the specified loops. They are counts of the stated operations, with at least 2x
margin.

H7-memory (supporting). Peak memory is below 2^32 bytes.
- The online phase keeps under 2^22 bytes: 16896 records of 24 bytes, a 2 MiB bitmap, sets and code.
- C0/C1 solver memory is taken from the same public re-run: 2.13 GiB, or 2^31.09 bytes, with solver
  calls run one at a time.

Sensitivity:
- If the R20 rate were 2^-13 (instead of 2^-12.8510), the total would be
  2^39.734.
- If C0 cost 2^39, the total would be 2^40.044.
- If kappa were 0.5, the total would be 2^40.321.

## 11. Memory and advice

Advice:
- the trail table (300 conditioned cells; at most 2 bits per cell over 3 x 32 x 35 cells, which is
  under 1 KiB);
- S (22 words, 88 bytes);
- the constants d5..d18 and the program.
In all this is under 2^11 bytes. Its construction is charged as C0 and C1.

Memory (reported only) is covered by H7: below 2^32 bytes.

## 12. Certificates and checks

- `published-31step-pair`: the ASIACRYPT 2024 pair. It shows that the trail and S are sound.
- `relaxed-run-1`: found by the run of Section 8.2; digest e9b8143268fa37c0...; W5 outside V5: s0-difference d0027e1f, so only the relaxed R20 holds.
A reviewer can:
1. hash each certificate pair;
2. enumerate V6..V9 and G16;
3. rebuild the 16896-record table from S (Section 6);
4. recompute P_any from the p5 histogram;
5. recompute the ledger.

## 13. Sources and credit

- Y. Li, F. Liu, G. Wang, X. Dong, S. Sun, "The First Practical Collision for 31-Step SHA-256",
  ASIACRYPT 2024: the framework, the trail, the published pair and hence S.
- Y. Li, F. Liu, G. Wang, J. Shi, ePrint 2026/1080, Section 3: the framework restated.
- Y. Li, F. Liu, G. Wang, EUROCRYPT 2024 (ePrint 2024/349): the SAT/SMT tool.
- Th0rgal (submission 25088ab7): the solver re-run measurements used in H1, H2 and H7. Sharing
  steps 0..14 across first blocks that differ only in word 15 is also used in that package; we use
  it for speed only and do not discount for it.
- Our own contributions: the relaxed W20 condition and its probability; Lemma 7.1; the measured run
  and its certificates; and the completion experiment.
