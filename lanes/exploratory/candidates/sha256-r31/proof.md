# SHA-256, 31 prefix rounds: the published two-block collision attack, re-derived and fully charged

Track `sha256-r31-exploratory`, target `sha256-r31-prefix-v1`, cost model
`collision-frontier-v5` (C = 2140 word operations per target compression),
review policy `paired-lanes-v1`. This package is a DRAFT.

## 0. Summary and provenance

Declared bounds (derived in Sections 6-9):

| Field | Value | Meaning |
| --- | ---: | --- |
| time_log2 | 46.3 | all charged work, including the historical search that produced the characteristic (Section 8) |
| success_probability | 0.6 | stopping rules of Sections 5 and 6, under heuristics H2 and H3 |
| memory_log2_bytes | 36 | declared cap for the SAT/SMT processes (heuristic H4); attack phases use < 2^28.3 bytes |
| preprocessing_log2 | 46.2 | characteristic search + Phase 1 + one-time scans |
| nonuniform_advice_log2_bytes | 12 | the characteristic of Section 3.1 as stored data (its search is charged) |

The score is dominated by the characteristic-search charge of heuristic H1
(Section 8): without it the attack phases cost 2^44.07. Our total is higher
than the published time complexity 2^40.5 for four stated reasons: the search
that produced the characteristic is charged (Section 8); our measurement of the
starting-point yield over random starting points gives a mean of only 2^10.61
distinct table keys per start (Section 4.3); each start is charged at a
conservative average SAT cost (Section 7.1); and our exact count of the
completion step gives a failure exponent of 2.88, not the published 1.3
(Section 4.5). We claim no novelty and no improvement.

What is published and what is ours:

- PUBLISHED [LLWDS24]: the attack framework (two blocks, a pre-computed table of
  2^19.8 solutions matched on A[-1]), time 2^40.5, memory 2^19.8, the practical
  run "1.2 hours with 64 threads", the characteristic, and the colliding pair in
  Section 2. Yingxin Li, Fukang Liu, Gaoli Wang, Xiaoyang Dong, Siwei Sun, "The
  First Practical Collision for 31-Step SHA-256", ASIACRYPT 2024, LNCS 15490,
  pp. 237-266, Springer 2025, doi:10.1007/978-981-96-0941-3_8. All figures used
  here are from the authors' conference slides (slides 13-15); we did not have
  the full text.
- PUBLISHED [LLW24]: the 31-step characteristic (Table 6, reproduced in Section
  3.1), its SAT/SMT search procedure (Section 4.2), the starting-point model and
  its cost T_model ~ 2^31.7, the statement that one starting point leaves about
  2^11 valid (W7, W8), and gamma ~ 1.3 from 100 tests. Yingxin Li, Fukang Liu,
  Gaoli Wang, "New Records in Collision Attacks on SHA-2", EUROCRYPT 2024, LNCS
  14651, pp. 158-186; IACR ePrint 2024/349.
- PUBLISHED [LLWS26]: the general cost formula of the framework, including the
  pre-processing cost T_pre = N_start x (T_sat + enumeration) (Section 3). Li,
  Liu, Wang, Shi, "Pushing the Limit of Memory-efficient Collision Attack
  Framework for SHA-2", IACR ePrint 2026/1080.
- PUBLISHED [MNS13]: the local collision in W5..W9, W16, W18 and the two-block
  idea. Mendel, Nad, Schlaeffer, "Improving Local Collisions: New Attacks on
  Reduced SHA-256", EUROCRYPT 2013, LNCS 7881, pp. 262-278.
- OURS (each item labelled "derivation" where it appears): re-verification of the
  pair; the check that the pair meets all 300 conditions of Table 6; the exact
  admissible sets and starting-point yields (Section 4), including a yield
  experiment over 20000 random starting-point offsets (Section 4.3); the exact
  count of the completion step and our completion routine with its simulation
  (Section 4.5); two fresh colliding pairs produced by that routine (Section 2);
  the independence argument and stopping rules (Section 6); all operation counts;
  the characteristic-search budget (Section 8, heuristic H1). Every estimate
  shows its arithmetic and is rounded up.

## 1. Target

Messages are byte strings. SHA-256 per FIPS 180-4 with the standard IV, standard
padding (0x80, zeros to 56 mod 64, 64-bit big-endian bit length), message
expansion W[t] = s1(W[t-2]) + W[t-7] + s0(W[t-15]) + W[t-16] (mod 2^32) for
t >= 16, constants K[0..30], and the compression function reduced to step
indices t = 0..30 (31 steps), followed by the full feed-forward of all eight
words. The digest is the full 256-bit chaining value after the last block,
big-endian. Notation follows [LLW24]: the chaining input of a block is
(a,b,c,d,e,f,g,h) = (A[-1], A[-2], A[-3], A[-4], E[-1], E[-2], E[-3], E[-4]),
and step t computes

    E[t] = A[t-4] + E[t-4] + S1(E[t-1]) + IF(E[t-1],E[t-2],E[t-3]) + K[t] + W[t]
    A[t] = E[t] - A[t-4] + S0(A[t-1]) + MAJ(A[t-1],A[t-2],A[t-3])

with S0(x) = x>>>2 ^ x>>>13 ^ x>>>22, S1(x) = x>>>6 ^ x>>>11 ^ x>>>25,
s0(x) = x>>>7 ^ x>>>18 ^ x>>3, s1(x) = x>>>17 ^ x>>>19 ^ x>>10,
IF(x,y,z) = (x&y) ^ (~x&z), MAJ(x,y,z) = (x&y) ^ (x&z) ^ (y&z). This is the
usual T1/T2 update rewritten (E[t] = d + T1, A[t] = T1 + T2). After step 30 the
working state (A[30],A[29],A[28],A[27],E[30],E[29],E[28],E[27]) is added
word-wise to the chaining input. Differences are M1' minus M1 modulo 2^32.

## 2. Certificates

Certificate 1 is the published pair, 128 bytes each, M0||M1 and M0||M1'
(big-endian words, as printed on the [LLWDS24] slides):

    M0  = 8ce3f805 5c401aed 579e5f7f bc3116cb ca189b3c eb75f04c 958f0a0e 7760b082
          dcd5027d 32260ad6 7b12b659 eee66518 ad7f88dd f8ad20bb 7ae40ffd 21609249
    M1  = 9abdeb1b 1f195f41 5a7210c1 55614f13 a2269dd1 be888a61 359257d4 adf3737b
          9f0484a6 eb830a58 66add94a 9669232d 45271fa5 b8f69585 428bbce3 0703b904
    M1' = 9abdeb1b 1f195f41 5a7210c1 55614f13 a2269dd1 be887a67 35b2dfc5 fde32975
          c70595a6 eb838a5c 66add94a 9669232d 45271fa5 b8f69585 428bbce3 0703b904

Certificates 2 and 3 (our derivation) keep M0 and words 0..12 of the second block
and replace (W13, W14, W15) with outputs of our completion routine (Section 5,
Phase 3); M1' = M1 + (0,0,0,0,0, fffff006, 002087f1, 4fefb5fa, 28011100,
00008004, 0, ..., 0) as for certificate 1:

    cert 2: (W13, W14, W15) = (97ff934d, e29b9609, cb3c8ffb), digest 2cfb4eea...7e58a31
    cert 3: (W13, W14, W15) = (f6f375b0, 6557e9a0, dc90cec4), digest 5223f5c4...5c0d46d

Files: certificates/message_a.bin, message_b.bin (cert 1), message_a2.bin,
message_b2.bin (cert 2), message_a3.bin, message_b3.bin (cert 3); raw bytes, 128
each; the full expected digests are in certificates/manifest.json.

Derivation (our re-verification) with the organizer reference
`verifier/hash_functions.py: digest(message, "sha256", rounds)`: for each of the
three pairs the two 31-round digests are equal; at 29, 30, 32 and 64 rounds they
differ (control); 64 rounds reproduce Python hashlib SHA-256. Certificate 1 has
digest 55fdfb37efcbd086e19c3de0f72596300a3acdf48da5b1d0450a592bb2869fcd.

Why the full hash collides: CV1 = f31(IV, M0) =
c0a93f38 23b02f67 2f718088 03dfb329 7eaa51b9 0e2dd226 107e021b 70b1ac59 is common;
f31(CV1, M1) = f31(CV1, M1') (for certificate 1 this is ff558659 2977dd01 54638843
35f8de84 a3336841 f4f476f2 7c571548 f7025605, the "hash" printed on the slides);
both messages are 128 bytes, so they get the same padding block. Certificates 2
and 3 are not fresh attack runs: they reuse the published Phase-2 output and only
show that our Phase 3 works. None of the certificates is used as a cost.

## 3. The characteristic

### 3.1 Table 6 of [LLW24] (published data, reprinted on the [LLWDS24] slides)

Symbols, most significant bit first: '=' equal bits, 'u' M1 bit 0 and M1' bit 1,
'n' M1 bit 1 and M1' bit 0, '0'/'1' equal bits with that value. Rows -4..-1 are
the chaining input.

      i  dA                               dE                               dW
     -4  ================================ ================================
     -3  ================================ ================================
     -2  ================================ ================================
     -1  ================================ ================================
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

The table has 300 non-'=' symbols: 120 signed differences and 180 value
conditions. Derivation (our check, independent tracer of Section 1): all three
certificate pairs satisfy all 300 symbols, and the signed differences of the
published pair are exactly the 120 'u'/'n' symbols. Weights (our count of 'u'/'n'):
sum H(dW) = 48, sum H(dA) = 21, sum H(dE) = 51. Modular message differences:
dW5 = fffff006, dW6 = 002087f1, dW7 = 4fefb5fa, dW8 = 28011100, dW9 = 00008004,
dW16 = 00008004, dW18 = ffff7ffc; every other dW[t], t = 0..30, is 0.

### 3.2 Exact conditions in the message expansion (our derivation)

Only modular differences of W enter the state update, so the exact requirements on
the message words are the following equations (d f(X) means f(X') - f(X)):

    t=16: dW16 = dW9                                   (automatic)
    t=18: s1(W16 + 00008004) - s1(W16) = ffff7ffc      (gives dW18)
    t=20: s1(W18 + ffff7ffc) - s1(W18) = 2ffe7fe0      (cancels d s0(W5))
    t=21: s0(W6 + 002087f1) - s0(W6) = 00000ffa       (= -dW5)
    t=22: s0(W7 + 4fefb5fa) - s0(W7) = ffdf780f       (= -dW6)
    t=23: s0(W8 + 28011100) - s0(W8) = b00fca02       (= -(dW16 + dW7))
    t=24: s0(W9 + 00008004) - s0(W9) = d7feef00       (= -dW8)
    t=25: dW18 + dW9 = 0                               (automatic)
    W5:   s0(W5 + fffff006) - s0(W5) = d0018020        (a choice of this algorithm)

At t = 20 the framework only needs d s0(W5) + d s1(W18) = 0. This algorithm fixes
the split d s0(W5) = d0018020, hence d s1(W18) = 2ffe7fe0 (the values of the
published pair); other splits are not used. All counts below therefore hold for
this algorithm, not for the framework in general.

At t = 17, 19 and 26..30 no term has a difference. At t = 31 the term s0(W16)
has a difference, which is why the pair does not collide at 32 steps. The state
part of the characteristic gives dA[t] = 0 for t >= 11 and dE[t] = 0 for t >= 15,
so the final state has no difference.

## 4. Exact counts and measured yields (our derivation)

All counts in 4.1 and 4.5 are exhaustive over 2^32 values, with the differences of
Section 3. Procedure for a reviewer to repeat: for each 32-bit X, evaluate the
stated equation and count; a C loop over 2^32 values takes seconds.

### 4.1 Admissible message words

| Word | Equation (Section 3.2) | Admissible values |
| --- | --- | ---: |
| W5 | s0(X + fffff006) - s0(X) = d0018020 | 16384 = 2^14 |
| W6 | s0(X + 002087f1) - s0(X) = 00000ffa | 8388608 = 2^23 |
| W7 | s0(X + 4fefb5fa) - s0(X) = ffdf780f | 512 = 2^9 |
| W8 | s0(X + 28011100) - s0(X) = b00fca02 | 49408 = 2^15.59 |
| W9 | s0(X + 00008004) - s0(X) = d7feef00 | 35921920 = 2^25.10 |

The W5 and W6 counts equal the published 2^14 and 2^23 ([LLW24] Section 4.2), so
the conditions on (W4, W5, W6) number Npro = 18 + 9 = 27 (W4 has none). [LLW24]
gives 2^27 and 2^25 for W7 and W8; under the exact equations we find 2^9 and
2^15.59. We use our counts and do not rely on the published W7/W8 figures.

### 4.2 Yield of the published starting point

A starting point fixes (A[1..12], E[5..12], W[9..12]) for both messages. For
fixed values, step 8 gives E4 = E8 - A4 - S1(E7) - IF(E7,E6,E5) - K8 - W8, and
step 7 gives E3 = E7 - A3 - S1(E6) - IF(E6,E5,E4) - K7 - W7. Exactly two
state conditions involve (E3, E4), from steps 6 and 7 (step 5 gives dE5 = dW5
automatically, and E3, E4 carry no difference):

    step 7:  IF(E6',E5',E4) - IF(E6,E5,E4) = dE7 - (S1(E6') - S1(E6)) - dW7
    step 6:  IF(E5',E4,E3)  - IF(E5,E4,E3) = dE6 - (S1(E5') - S1(E5)) - dW6

where all right-hand terms are fixed by the starting point. Then
A0 = E4 - A4 + S0(A3) + MAJ(A3,A2,A1) and
A[-1] = E3 - A3 + S0(A2) + MAJ(A2,A1,A0). Enumeration on the starting point of
the published pair (W8 over its 49408 admissible values, then W7 over its 512):

- valid (W8, E4): 2048 = 2^11 (1632 if the Table-6 bit conditions on E4 are
  used instead of the exact equation);
- valid tuples (W7, W8, E3, E4): 16896 = 2^14.04, between 0 and 64 per (W8, E4);
- distinct A[-1] among them: 2336 = 2^11.19;
- the published pair's (W7, W8) is among them, with its A0 and A[-1].

[LLW24] Section 4.2 states that "Experiments suggest that there are 2^11 valid
(W7,W8) left" per starting point. Under our exact equations the published start
has 2^14.04 valid (W7, W8) tuples, so the published 2^11 is not the same quantity
as either of our counts, and we do not use it. One starting point cannot fill a
table of about 2^19 keys; the table needs many starting points (Section 5).

### 4.3 Yield over random starting points (experiment)

The published starting point is the one that produced the published pair, so its
yield may be biased upward. To measure the population of starting points we use
the following model. The step-6/7 equations of Section 4.2 depend on the start
only through E5, E6, E7 (and their primed values), and Table 6 fixes 31, 25 and
30 of their 32 bits. The start enters the enumeration otherwise only through
off8 = E8 - A4 - S1(E7) - IF(E7,E6,E5) - K8 (so E4 = off8 - W8), through
off7 = E7 - A3 - S1(E6) - K7, and through A1..A4 in the key computation. Table 6
puts no condition on A1..A4, and A4 enters off8 additively. Model: E5, E6, E7 at
the published values; off8, A1, A2, A3, A4 independent and uniform; then the exact
enumeration of Section 4.2.

Procedure (repeatable): for each sample, draw (off8, A1, A2, A3, A4), run the
W8 pass and the W7 pass of Section 4.2 with the exact equations, and count the
distinct A[-1]. Results (our derivation, 20000 samples from two seeds of 10000;
the published start, used as a control, reproduces 2048 / 16896 / 2336 exactly):

- mean distinct A[-1] per start: 1565.9 = 2^10.613; standard deviation 4318;
  standard error 30.5; mean minus three standard errors 1474.3 = 2^10.526;
- 68.9% of samples give no key at all; the maximum is 82016 (2 of 20000 samples
  exceed 2^16);
- mean tuples per start 6124 = 2^12.58 (3.91 tuples per distinct key);
- only 17.4% of samples reach the published start's 2336 keys.

So the published start is favourable, and the per-start mean is about half of
what one start suggests. We use the premise value mu = 2^10.5 = 1448 new
distinct keys per accepted start (heuristic H3). It lies below the mean minus
three standard errors. Capping each start at 2^16 inserted keys (Section 5)
removes less than 2 keys per start on average in this sample, and collisions
with keys already in the table remove a fraction below 2^-12.8; both are inside
the gap between 1474.3 and 1448.

### 4.4 Table-size convention

The table TAB is keyed by A[-1]. For the success analysis we count only the
number D of distinct keys, which the algorithm itself counts. Tuples sharing a
key differ in (A0, E3, E4, W7, W8) and give correlated tests after one hit, so we
never count them as extra independent chances. We store up to 16 tuples per key
and test all of them on a hit. That can only help, and its cost is charged
(Section 7.2). Phase 1 stops as soon as D >= 2^19 (Section 5), so D >= 2^19
holds deterministically and only the number of starts is random.

### 4.5 The completion step (Phase 3)

After Phase 2, W[0..12] are fixed. Write c16 = W9 + s0(W1) + W0 and
c18 = W11 + s0(W3) + W2. Then W16 = s1(W14) + c16 and W18 = s1(W16) + c18;
W13 and W15 do not enter W16 or W18.

Derivation (exhaustive): s1 is a bijection on 32-bit words (no collisions among
all 2^32 images). The set G16 of W16 values satisfying the t=18 equation has
exactly 64 elements:

    G16 = { h*2^28 + v : h = 0..15, v in {031bbffc, 064bbffe, 09b3bffd, 0ce3bfff} }

(the published pair has W16 = 064bbffe). The set G18 of W18 values satisfying
the t=20 equation has 42467328 = 2^25.34 elements. Since s1 is a bijection,
every x in G16 gives exactly one W14 = s1^-1(x - c16). That W14 also satisfies t=20
iff s1(x) + c18 lies in G18. Whether any W14 works therefore depends only on c18,
and the set S of good c18 values is {y - s1(x) : x in G16, y in G18}. Our
exhaustive count gives |S| = 584683520, so

    Pr[ some W14 satisfies t=18 and t=20 ] = 584683520 / 2^32 = 0.136132 = 2^-2.877

for uniform c18. No choice of W13 or W15 can change this. With the split of
Section 3.2, Phase 3 of this algorithm succeeds with probability at most 0.1361
per Phase-2 output; in the [LLWS26] notation this algorithm has beta >= 2.877.
The published gamma ~ 1.3 from 100 tests ([LLW24]) does not describe this
algorithm's completion step under uniform c18. We do not know what the published
tests measured. One possibility is that they counted only the Table-6 bit
conditions on W16 and W18: these are necessary but not sufficient, since on the
published Phase-2 output 2048 W14 values meet them but only 5 meet the exact
equations. We do not use gamma ~ 1.3.

The rest of Phase 3 depends on the starting point. With W14 fixed, dE14 and dE15
depend only on E13 (W13 = E13 - c13 for a known c13). dE16 and dE17 then depend
on W15. Derivation (simulation of our routine, Section 5, Phase 3, with the
enumeration rule stated there): we use the published starting point and W5..W12,
with W0..W4 drawn uniformly at random. This is the Phase-2 output distribution by
Section 6.1, because only c16 and c18 enter Phase 3. Results:

- 600000 simulated outputs (two independent seeds, 200000 + 400000);
- 81473 had at least one W14 meeting the exact equations (0.13579, against the
  exact 0.13613), with at most 16 such W14;
- all 81473 were completed to a zero state difference after step 30;
- E13 tries: mean 561 per simulated output, averaged over all outputs including
  the 86% with no good W14 (which need none); that is about 561 / 0.1358 = 4131
  per output with a good W14. Maximum 57431 in one output, over all its W14;
- W15 tries: mean 2.0 per simulated output (about 15 per output with a good W14);
  maximum 229 in the 400000-run batch.

The cost of Phase 3 (Section 7.3) uses only the caps, not these means. The
completion failure rate given a good W14 is below 3/81473 = 2^-14.7 (rule of
three, 95%). On the published Phase-2 output there are 5 good W14 values. The
routine produced certificates 2 and 3 from two of them, and further fresh pairs
from W14 = 428bbce3.

We use beta = 2.88 > 2.877. Then 2^-2.88 = 0.1358 < 0.13613 * (1 - 2^-14.7), so
completion failures are already inside beta. The extension to other starting
points is part of H2.

## 5. The attack algorithm

The framework is that of [LLWDS24]/[LLWS26]. The completion routine, the
stopping rules and all caps are ours.

Advice (charged, Section 8). The characteristic of Section 3.1 is stored data
(< 2^12 bytes, Section 9). It is not recomputed. The cost model requires the
search that produced it to be charged even though the program omits it; Section 8
charges that historical search under heuristic H1. Because the attack only reads
the stored characteristic, no part of the attack can fail for lack of it.

Phase 0' - one-time scans (charged as T_aux). Compute the admissible lists of W7
(512 values) and W8 (49408 values) and the 64-element set G16, each by one scan
over 2^32 values.

Phase 1 - starting points and table. Repeat until D >= 2^19:

- Run the [LLW24] starting-point SAT model, which solves for (A[1..12], E[5..12],
  W[9..12]) satisfying the characteristic on steps 5..12 (W9 must satisfy t=24).
  We add to the model the two step-13 relations that the start alone determines
  (W13 has no difference and dA9 = 0): dE13 = dE9 + dS1(E12) + dIF(E12,E11,E10)
  = 0, and dA13 = dE13 + dMAJ(A12,A11,A10) = 0. Each call is randomised by fixing
  a fresh uniformly random value of W12 in the model, so the starting points are
  distinct. Each call runs under a time-out of 2^35 units; a call that times out
  or is unsatisfiable is abandoned and a new call with a fresh W12 is made. Its
  cost is charged (H3).
- Filter (essentially free): recompute dE13 and dA13 from the returned words for
  both messages and discard the start if either is nonzero. The published start
  passes (dE13 = dA13 = 0).
- For each accepted start, enumerate the 49408 admissible W8 and keep those whose
  E4 meets the step-7 equation of Section 4.2. For each kept (W8, E4), enumerate
  the 512 admissible W7 and keep those whose E3 meets the step-6 equation.
  Compute A0 and A[-1], and insert (A[-1], A0, E3, E4, W7, W8, s) into TAB keyed by
  A[-1], with at most 16 tuples per key and at most 2^16 new keys per start.
  Update the distinct-key count D. Store each start (24 words, message 1; the
  message-2 values follow by adding the fixed modular differences).

Phase 2 - matching. For j = 0, 1, ..., N - 1 with N = 2^42.88: take the first
block M0(j) (two message words hold the counter j, the other words are fixed) and
compute CV1 = f31(IV, M0(j)). Look up A[-1] in TAB. For each stored tuple under
that key, compute E0, E1, E2 from the A-equations of steps 0..2:
E[i] = A[i] + A[i-4] - S0(A[i-1]) - MAJ(A[i-1],A[i-2],A[i-3]). Then compute W5
and W6 from the E-equations of steps 5 and 6, and test the W5 and W6 equations
of Section 3.2. If both hold, compute W4 and W0..W3 from the E-equations of steps
4 and 0..3, and run Phase 3.

Phase 3 - completion (exact). (a) For each x in G16, set W14 = s1^-1(x - c16)
and keep it if s1(x) + c18 satisfies the t=20 equation. (b) For each kept W14,
draw a uniformly random offset o and try E13 = o + r * 9e3779b9 for
r = 0, 1, ..., 2^16 - 1 (distinct values, since the multiplier is odd); set
W13 = E13 - c13. Accept E13 if the two-message step 14 gives dE14 = 00008004 and
the step-15 constant gives dE15 = 0. (c) For each accepted E13, draw a fresh
uniformly random offset o' and try W15 = o' + q * 9e3779b9 for q = 0, ..., 2^10 - 1,
at most 2^16 W15 values in total per invocation. Require dE16 = 0 and
IF(E16,E15,E14') = IF(E16,E15,E14), i.e. dE17 = 0. Then compute both messages
through step 30 and accept only if the state difference after step 30 is zero
(the exact final check). If every option is exhausted, return to Phase 2. Phase 3
is invoked at most 1024 times in total.

Phase 4 - output. Output M0||M1 and M0||M1' and confirm both full 3-block digests
(6 compressions). Only pairs that passed the exact check of Phase 3(c) reach this
phase.

## 6. Success probability

### 6.1 Independence at a hit (our derivation)

Heuristic H2 treats CV1 = f31(IV, M0(j)) for distinct j as independent uniform
256-bit values. Fix a stored tuple, with A[-1] equal to its key. The following
identities come from Section 5, Phase 2:

- W6 = (terms fixed by the tuple and start) - A[-2], since
  E2 = A2 + A[-2] - S0(A1) - MAJ(A1,A0,A[-1]) and W6 = E6 - A2 - E2 - S1(E5) -
  IF(E5,E4,E3) - K6. So W6 is uniform over A[-2].
- W5 = (terms depending on A[-2]) - A[-3], since
  E1 = A1 + A[-3] - S0(A0) - MAJ(A0,A[-1],A[-2]) and W5 = E5 - A1 - E1 - ...
  So W5 is uniform over A[-3] for every A[-2].
- W3 = (...) - E[-1] and W2 = (...) - E[-2], so c18 = W11 + s0(W3) + W2 is
  uniform over E[-2] for every (A[-2], A[-3], E[-1]).

Hence, for each matched tuple:

    Pr[W5 ok] = 2^14/2^32 = 2^-18,  Pr[W6 ok] = 2^-9,  Pr[c18 in S] = 0.13613,

and these probabilities are exact and independent. Phase 3 then completes with the
probability measured in Section 4.5.

### 6.2 Per-trial success and stopping rule

A[-1] matches one of the D keys with probability D/2^32. Different keys are
disjoint events for one CV1. Counting one tuple per key, and with D >= 2^19 by
the Phase-1 stopping rule:

    p >= D * 2^-32 * 2^-27 * 2^-2.88 >= 2^(19 - 61.88) = 2^-42.88.

With N = 2^42.88 independent trials, pN >= 1 and

    Pr[no success] <= (1 - p)^N <= exp(-pN) <= exp(-1) = 0.368.

### 6.3 Caps

Let X be the number of Phase-3 invocations. One CV1 matches at most one key, and
each key holds at most 16 tuples, so each trial adds between 0 and 16 to X. The
table has at most 2^19 + 2^16 keys (the stopping rule overshoots by at most one
start's 2^16 keys), so E[X] <= N * 16 * (2^19 + 2^16) * 2^-32 * 2^-27 = 132.5.
The trials are independent under H2. For Y = X/16, a sum of independent [0,1]
variables with mean at most 8.29, the Chernoff bound
Pr[Y >= (1+d) m] <= (e^d / (1+d)^(1+d))^m with (1+d) m = 64 gives
Pr[X >= 1024] < 2^-108. With the measured 3.9 (random starts) or 7.2 (published start) tuples per
key instead of 16, the mean is smaller still. The per-invocation caps on E13 and W15 were never reached in
the simulation (Section 4.5); a cap exhaustion counts as a completion failure,
which is already inside beta.

### 6.4 Claim

Pr[success] >= 1 - exp(-1) - 2^-108 > 0.632 - 10^-30 > 0.6 under H2 and H3.
If p were short by a factor f (for example worse completion on other starting
points), the success probability would be 1 - exp(-f). It stays >= 0.39 for
f >= 0.495 (e.g. f = 1/2 gives 1 - exp(-0.5) = 0.3935), so the 0.39 floor
tolerates a factor-2 shortfall. A shortfall in the per-start yield does not
lower p, because D >= 2^19 is enforced; it raises the expected Phase-1 cost
instead (Section 7.1).

## 7. Cost of the attack phases (units: one 31-step compression = 1; other word operations 1/2140)

### 7.1 Phase 1 and one-time scans

Starting points (heuristic H3). [LLW24] gives T_model ~ 2^31.7 per starting point
in "SHA-256 computations", without stating the benchmark. Readings: in 31-step
compressions, 2^31.7; if the unit is full 64-step SHA-256, 2^31.75 * 64/31 =
2^32.8; if the authors' SHA-256 benchmark ran at only 2^21 per second and the
solver time is converted at our rate of Section 8 (2^22.937 units per second),
2^31.7 / 2^21 * 2^22.937 = 2^33.64. We charge an average of 2^34.5 units per
accepted start. This covers the slowest reading with a further factor of
2^0.86 = 1.82 for abandoned (timed-out or unsatisfiable) calls, starts rejected
by the step-13 filter, and the two added step-13 relations. This average is a
premise (H3), not a bound.

Per-start enumeration (our bound). The W8 pass costs 49408 * (<= 64 operations).
The W7 pass costs at most 49408 * 512 * (<= 64 operations) if every W8 survived
(2048 survive on the measured start). Insertion and distinct-key counting cost
<= 2^20 tuples * 2 * 64 operations. The step-13 filter costs <= 2^8. In total
<= 2^30.71 operations = 2^19.65 units, so we charge 2^20.

Number of starts. Let Z_s be the number of new distinct keys that accepted start
s adds. Under H3, E[Z_s | earlier starts] >= mu = 2^10.5 (Section 4.3). Phase 1
stops at the first start at which D >= 2^19, and Z_s <= 2^16, so the final D is
below 2^19 + 2^16. By Wald's identity (optional stopping for the bounded
increments Z_s), the expected number of accepted starts is

    E[N_start] <= (2^19 + 2^16) / 2^10.5 = 407.3,

    T1 = E[N_start] * (2^34.5 + 2^20) <= 407.3 * 2^34.5001 = 2^43.170 (expected).

One-time scans: 3 * 2^32 values * <= 32 operations = 2^38.58 operations =
2^27.52 units, so T_aux <= 2^28.

### 7.2 Phase 2 (our bound)

Per trial: one compression (1 unit) plus at most 128 word operations. These cover
the counter and block update (<= 6), call overhead and reading A[-1] (<= 8),
the hash index into 2^21 buckets (3), and the bucket probe. The expected occupancy
is at most (2^19 + 2^16)/2^21 = 0.28 keys per bucket; we allow <= 20 operations
with chain handling. Loop control takes <= 4. Hit work: a hit occurs with
probability at most (2^19 + 2^16)/2^32 = 2^-12.83 per trial and costs at most
16 tuples * <= 2^8 operations (E0..E2, W5, W6 and the two s0 tests), i.e.
<= 0.57 operations per trial on average. The sum is below 42, so 128 is generous:

    T2 <= N * (1 + 128/2140) = 2^42.88 * 1.0599 = 2^42.964.

### 7.3 Phase 3 and Phase 4

Per invocation:

- step (a): 64 * (s1, s1^-1 as 32 conditional XORs, the test) <= 64 * 2^7.5 =
  2^13.5 operations;
- step (b): at most 64 kept W14 * 2^16 E13 tries * <= 2^8 operations (the
  two-message step 14 and the step-15 constants) = 2^30 operations;
- step (c): at most 2^16 W15 tries * <= 2^12 operations (the filters, plus the
  two-message expansion and steps 15..30 when the filters pass) = 2^28 operations.

The total is <= 2^30.33 operations = 2^19.26 units per invocation, and 1024
invocations cost <= 2^29.26. We charge T3 = 2^29.5. Phase 4 costs T4 <= 8 units.

## 8. The characteristic search (heuristic H1, score-critical)

The attack reads Table 6 as stored advice. The cost model requires all
construction of advice to be charged, "including any search omitted from the
submitted program". The object charged here is therefore the historical
SAT/SMT search of [LLW24] that produced Table 6, not a hypothetical re-run. Its
run time is not published. We charge it with an explicit budget model:

- Calls. [LLW24] Section 4.2 has three minimisation stages (sum H(dW) over
  differences in W5..W9, W16, W18; then sum H(dA) subject to dA[11..30] = 0 and
  dE[15..30] = 0; then sum H(dE) with value transitions on steps 7..10). Each
  stage establishes its optimum (48, 21, 51) with a satisfiable call at the
  optimum and an unsatisfiable or timed-out call one below. A binary search over
  thresholds 0..255 does both in 8 calls. [LLW24] also report a repair: a
  characteristic found without value transitions was invalid, and stage 3 was run
  again with them. We charge one full repeat of stage 3. Total: 4 stage runs * 8 =
  32 calls.
- Time per call. Every call is charged at 72 single-thread hours. 72 hours is the
  per-call time-out [LLW24] Section 4.3 uses in its 31-step SHA-512 search ("If
  the solver cannot output a solution in a reasonable time, e.g., 72 hours,
  increase t_r"). It is a time-out, not a measured run time. Charging every call
  at the cap, including the quick calls far from the optimum, is the margin for
  calls that were not recorded.
- Conversion. We value one thread-second at 2^34 primitive word operations, i.e.
  2^34 / 2140 = 2^22.937 units per second and 2^34.750 units per thread-hour.
  This is a calibrated estimate, not an upper bound: it corresponds to 4
  primitive operations per cycle at 4 GHz. CDCL SAT and SMT solvers spend most of
  their time in unit propagation over watch lists, which is limited by memory
  latency; their sustained rate of primitive operations is typically well below
  this. The hardware ceiling of a current core is higher, about 2^35.8 (10
  retired instructions per cycle at 6 GHz); we did not measure a solver.

    T0 = 32 * 72 * 2^34.750 = 2304 * 2^34.750 = 2^(11.170 + 34.750) = 2^45.920 units.

H1 is the premise that the historical search producing Table 6 used at most 2304
single-thread hours, each worth at most 2^34 primitive operations. Evidence: the
three stages run over a fixed difference pattern; the SHA-256 instance has
32-bit words, half the SHA-512 word size for which [LLW24] treat 72 hours as the
time-out; and the related starting-point SAT model, which includes value
transitions for steps 5..12, solves in about 2^31.7. Limitations: this is an
estimate, not a measurement; we did not rerun the open-source tool cited by
[LLW24], and no SAT solver was available to us. If the authors ran a
multi-threaded solver, 72 wall-clock hours would be more thread-hours. Searches
over other local-collision positions or other characteristics before Table 6,
and the authors' later experiments, are not counted.

Sensitivity (total time_log2 with all other terms unchanged):

| Search budget S (thread-hours) | 72 | 504 | 1000 | 2304 | 5000 | 10000 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| log2 T0 | 40.92 | 43.73 | 44.72 | 45.92 | 47.04 | 48.04 |
| time_log2 (rounded up) | 44.23 | 44.91 | 45.43 | 46.28 | 47.22 | 48.13 |

| Rate (operations per thread-second), S = 2304 | 2^33 | 2^34 | 2^35 | 2^35.8 |
| --- | ---: | ---: | ---: | ---: |
| time_log2 (rounded up) | 45.56 | 46.28 | 47.11 | 47.84 |

## 9. Totals, memory and advice

    T = T0 + T1 + T_aux + T2 + T3 + T4
      <= 2^45.920 + 2^43.170 + 2^28 + 2^42.964 + 2^29.5 + 8
       = 2^46.273   ->  time_log2 = 46.3 (rounded up)

    preprocessing = T0 + T1 + T_aux = 2^46.120  ->  46.2 (rounded up)

T1 is an expected cost (Section 7.1); every other term is a worst case under the
stated caps. Without T0 the attack phases cost 2^44.071. The table target
D = 2^19 minimises T1 + T2 to within 0.001 bits.

Sensitivity to H3 (total time_log2 rounded up, table size re-optimised): average cost per
accepted start 2^32.8 -> 46.13, 2^34 -> 46.22, 2^34.5 -> 46.28 (claimed),
2^35 -> 46.34, 2^36 -> 46.50; mean yield mu = 2^9.5 -> 46.41, 2^10 -> 46.34,
2^11 -> 46.22.

Memory for the attack phases (our bound):

- TAB: at most 16 * (2^19 + 2^16) tuples of 7 words, packed into 32 bytes each:
  2^28.17 bytes;
- index: 2^21 buckets of 8 bytes, 2^24 bytes;
- starting points: 96 bytes each (about 407 expected; 2^12 starts would take
  2^18.6 bytes); admissible lists 2^17.6 bytes; G16 256 bytes;
- code, constants, CV1 and messages: < 2^20 bytes.

The total is < 2^28.3 bytes. The SAT/SMT processes of Phase 1 (and of the
historical search) have unreported memory. Under heuristic H4 we declare 2^36
bytes (64 GiB) for them, so memory_log2_bytes = 36. Memory is not scored.

Advice: the characteristic of Section 3.1 (300 symbols; < 2^12 bytes as stored
text) and the three thresholds. Their search is charged in T0. Starting points,
G16 and the admissible lists are computed in the run and charged in T1 and T_aux.
So nonuniform_advice_log2_bytes = 12. The stored published pair is used only as a
certificate.

## 10. Heuristics (mirrored in claim.json)

H1 (score-critical): the historical search that produced Table 6 used at most 32
solver calls of at most 72 single-thread hours each (2304 thread-hours), valued
at 2^34 primitive operations per thread-second (a calibrated estimate):
T0 = 2^45.92 units; Section 8.

H2 (score-critical): CV1 = f31(IV, M0(j)) behaves as an independent uniform
256-bit value for distinct j. Under this, Section 6.1 makes the W5, W6 and c18
probabilities exact. Completion given a good W14 succeeds with probability close
to 1 on every starting point Phase 1 produces; this was measured only on the
published starting point (81473/81473), which is a favourable start for yield
(Section 4.3).

H3 (score-critical): an accepted starting point costs on average at most 2^34.5
units, including abandoned calls; and, conditioned on earlier starts, it adds on
average at least mu = 2^10.5 new distinct keys, as in the random-offset model of
Section 4.3 (measured 2^10.613, three-standard-error lower bound 2^10.526).

H4 (supporting): the SAT/SMT processes use at most 2^36 bytes. Memory is not
scored.

## 11. Limitations

- We re-state and re-derive a published attack. We did not re-run the
  characteristic search, Phase 1 or Phase 2.
- No experiment manifest is declared. Our exhaustive counts, the yield
  experiment and the Phase-3 simulation are derivations with stated procedures.
  The organizer only checks the three certificates.
- The ASIACRYPT 2024 full text was not available. The framework and figures come
  from the slides, [LLW24] and [LLWS26].
- Our failure exponent beta = 2.88 differs from the published gamma ~ 1.3 for the
  reason given in Section 4.5. Our W7/W8 admissible counts differ from the
  published ones (Section 4.1).
- The starting-point SAT model and its cost T_model are imported from [LLW24]
  and not reproduced here; H3 states the premise we rely on.
- The yield model of Section 4.3 keeps the 10 free bits of E5, E6, E7 at the
  published values and treats off8 and A1..A4 as uniform. A starting point from
  the SAT model may differ from this model.
- Completion was measured on one starting point only (H2).
- The score depends mainly on H1. Section 8 gives the score for other budgets and
  rates.

## 12. Why this claim is not lowered to the replay accounting (our derivation)

A replay-style accounting of this attack charges the fixed published pair at the
published headline: all historical work, including the characteristic search, is
assumed to lie below 2^40.75 units, i.e. within a factor 2^0.25 = 1.189 of
2^40.5. We do not adopt it, because the data reproduced in this proof do not
support it. All figures below are our own quantities:

1. Phase 1 at the published table size. With our measured mean of 2^10.61
   distinct keys per start (Section 4.3), a table of 2^19.8 keys needs 2^9.19
   starts, i.e. 2^9.19 * 2^31.7 = 2^40.89 in the unit of T_model. Matching at
   2^19.8 keys with the published gamma 1.3 costs 2^(32 - 19.8 + 27 + 1.3) =
   2^40.5 compressions. The sum is 2^41.71, before the characteristic search, the
   T_model unit and any unsuccessful run. Counting every tuple instead (2^12.58
   per start, which needs a correlation bound we do not have) gives 2^7.22 starts,
   2^38.92, and a sum of 2^40.92.
2. Our exact count of Section 4.5 gives 2^-2.877 for this algorithm's completion
   step, not 2^-1.3. At 2^19.8 keys the expected matching work for success
   1 - 1/e is then 2^(32 - 19.8 + 27 + 2.877) = 2^42.08.
3. The characteristic-search time is not published (Section 8). The reported
   1.2 hours on 64 threads (76.8 thread-hours) is one realisation that the
   publisher followed with further experiments. At the rate of Section 8
   (2^34.75 units per thread-hour) those 76.8 thread-hours alone are 2^41.01
   units.

Lower variants of our own algorithm, all with the same heuristics (columns: T0;
T1 + T2 after re-optimising the table size; total time_log2, which also adds
T_aux + T3 + T4 <= 2^30):

| Variant | T0 | T1 + T2 | Total |
| --- | ---: | ---: | ---: |
| This claim (success >= 0.6, D = 2^19, 407 starts expected) | 2^45.920 | 2^44.071 | 46.28 |
| Stop at success 0.39 (pN = 0.4943), 296 starts | 2^45.920 | 2^43.598 | 46.19 |
| ... and 2^31.75 per start (T_model in 31-step units, no failures), 698 starts | 2^45.920 | 2^42.148 | 46.03 |
| ... and every stored tuple counted (2^12.58 per start), 328 starts | 2^45.920 | 2^41.083 | 45.97 |
| Last row with T0 omitted | 0 | 2^41.083 | 41.09 |

Stopping at success 0.39 is justified (1 - exp(-0.4943) = 0.39000) but is not
used: it gains 0.09 bits and removes the factor-2 tolerance of Section 6.4. The
T_model unit is not stated by the source, so the 31-step reading without failures
is not justified. Counting every tuple needs a bound on the pairwise correlation
of tuples that share an A[-1] key, which we have not derived. Even the last row,
which drops the characteristic search that the cost model requires to be charged,
is not below 2^41. We therefore keep time_log2 = 46.3.
