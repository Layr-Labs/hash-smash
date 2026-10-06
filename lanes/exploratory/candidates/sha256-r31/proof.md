# SHA-256 reduced to 31 steps: a two-block ordinary collision in under 2^28.5 compressions

Track `sha256-r31-exploratory`, target `sha256-r31-prefix-v1`, cost model `collision-frontier-v5`
(one 31-step compression = 1 unit, any other 256-bit word operation = 1/2140), policy
`paired-lanes-v1`. This package states a concrete randomized algorithm with fixed parameters and
fixed advice. Its time bound is a sum of exact operation counts (Section 7); its success
probability follows from exact counts and two standard heuristics (Section 6). Organizer-checkable
evidence: 16 fresh colliding pairs found by this algorithm (certificates), and an organizer-run
experiment that re-checks all advice and produces a fresh collision for every organizer seed.

## 0. Claim

| Field | Value | Derivation |
| --- | --- | --- |
| time_log2 | 28.5 | Section 7: total < 2^28.17 (exact counts, 4x margin on advice construction) |
| success_probability | 0.55 | Section 6: lambda = 1.000, 1 - e^-1 = 0.632 |
| memory_log2_bytes | 31 | Section 7: < 2^30.9 bytes |
| preprocessing_log2 | 27 | Section 7: advice construction, P0, P2, P3 |
| nonuniform_advice_log2_bytes | 13 | Section 4: characteristic + 65 base points, < 8 KiB |

The attack is the two-block method of Mendel-Nad-Schlaffer [MNS13] with the 31-step
characteristic of Li-Liu-Wang [LLW24, Table 6] in block 2 and the matching framework of
Li-Liu-Wang-Dong-Sun [LLWDS24]: a table of A_-1 values, random first blocks looked up by A_-1,
and completion of W13..W15. [LLWDS24] reports 2^40.5 time with a 2^19.8-entry table. Changes:

1. Message-word conditions are the exact modular message-expansion conditions instead of the
   signed patterns of Table 6 (W8: 49408 admissible values instead of 2^13).
2. The W20 cancellation may split freely between sigma0(W5) and sigma1(W18); the completion picks
   W18 for the split W5 produced. Per table hit this raises the W5/completion probability from
   2^-19.09 (split fixed as in Table 6) to exactly 2^-12.6621.
3. Starting points come from our own search (no SAT solver, no published pair), and each base
   point is expanded into up to 2^17 variants through the free bits of E5..E8.
4. Memory is not scored, so the table is large (75675936 entries) and the first-block search short.

## 1. Target and notation

A message is M0||M1 (128 bytes); its padded form adds one identical third block for both
messages. Every block uses steps 0..30 with the standard constants, schedule and feed-forward,
from the standard IV. If f31(f31(IV,M0),M1) = f31(f31(IV,M0),M1') with M1 != M1', the third block
and the digests agree. CV = f31(IV,M0) = (A_-1,A_-2,A_-3,A_-4,E_-1,E_-2,E_-3,E_-4). Step i:

    E_i = A_{i-4} + E_{i-4} + S1(E_{i-1}) + IF(E_{i-1},E_{i-2},E_{i-3}) + K_i + W_i
    A_i = E_i - A_{i-4} + S0(A_{i-1}) + MAJ(A_{i-1},A_{i-2},A_{i-3})
    W_t = s1(W_{t-2}) + W_{t-7} + s0(W_{t-15}) + W_{t-16}  (t = 16..30)

Primes denote M1'. Operation weights in Section 7: 32-bit add/sub 2, rotation 4, shift 1,
and/or/xor 1, not 2, compare/branch 1, load/store 1, random word 1; so S0, S1 = 14, s0, s1 = 11,
IF, MAJ = 5. A 31-step compression costs 2140 such operations (cost model).

## 2. Characteristic

Table 6 of [LLW24] (eprint 2024/349, CC BY), rows with any condition; all other rows -4..30 are
'='. Columns: i, A_i, E_i, W_i; position k is bit 31-k; 'u' = (0,1), 'n' = (1,0) for (M1, M1').

    3  ================================ ==========================10==== ================================
    4  ================================ ============0===0=========01===0 ================================
    5  ===================n=unnnnnnn=n= 000111010001111110nu=11111unnnu1 ================nuuu=======0=uu=
    6  ========n======================u 101011=11==0n0==u11110==1110011n ==========u=====u===u======n===u
    7  ===u===n==n========n=========n=u un0u1100n=01u11111001u1=n110u10n =u=u=======n=====n=nu=n=====nun=
    8  =============================n== 1u01un0u0=1=1=11n=0=u0=001001u0= =u=nn==========u===u===u==1=====
    9  ================================ 01100001110=0=010===00=11101u0=1 ================u==========1=u==
    10 ================u============u== =1n1uuuuu0100=1un0=10unnnnnnn010 ================================
    11 ================================ =01u1010uu1==11100===1000001n=0= ================================
    12 ================================ ==110001=11====1n====0011110n=0= ================================
    13 ================================ ===0====01======1=============== ================================
    14 ================================ ================u===========0u== ================================
    15 ================================ ================0============1== ================================
    16 ================================ ================1============1== =============unnnunnnnnnnnnnnn==
    18 ================================ ================================ ==============1=n=0==========n==

The algorithm uses the signed differences of A_5..A_10 and E_5..E_16 as above, the fixed bits of
E_5..E_12, and only the modular message differences dW5 = fffff006, dW6 = 002087f1,
dW7 = 4fefb5fa, dW8 = 28011100, dW9 = 00008004, dW16 = 00008004, dW18 = ffff7ffc
(M1' = M1 + dW on words 5..9). Every check below evaluates the step equations for both messages;
the bit conditions in the E_3, E_4 and W rows are replaced by those checks and by Section 3.
As in the published complexities this track's frontier uses, the one-time search that produced
Table 6 is not charged; the table itself is part of the advice.

## 3. Exact message-word sets and the split probability

W_i enters every step additively, so only dW_i matters for the states. The expansion needs:

| Set | Condition | Exact size (of 2^32) |
| --- | --- | ---: |
| G16 | s1(W16+dW16) - s1(W16) = dW18 | 64 |
| V6 (W21) | s0(W6+dW6) - s0(W6) = -dW5 | 2^23 |
| V7 (W22) | s0(W7+dW7) - s0(W7) = -dW6 | 512 |
| V8 (W23) | s0(W8+dW8) - s0(W8) = -dW16 - dW7 | 49408 |
| V9 (W24) | s0(W9+dW9) - s0(W9) = -dW8 | 35921920 |
| split (W20) | s0(W5+dW5) - s0(W5) + s1(W18+dW18) - s1(W18) = 0 | see below |

W17, W19, W25..W30 then have no difference. V7, V8, G16 are built by a depth-first search over
the carry patterns of W + dW (2.2e5 nodes): for a fixed carry pattern the XOR difference is
fixed, the sign of each output bit of s0/s1 is a GF(2)-linear function of W and is unique when it
exists; 10 linear solves give exactly the sets above (cross-checked by exhaustive scans).
Split probability. For uniform W5 and a uniform offset b, let p_split be the probability that
some W16 in G16 makes W18 = s1(W16) + b satisfy the W20 condition. Exhaustively over all 2^32
offsets b and all W5 (via the counts of each value of s0(W5+dW5) - s0(W5)):
p_split = 2846011149340672 / 2^64 = 2^-12.6621. (With the split fixed as in Table 6: 2^-19.09.)

## 4. Advice

The advice is Table 6 (Section 2) and 65 base starting points, each given by E5..E12 and A5..A8
(12 words; listed as BASES in `experiments/complete.py`, which re-checks all of them, Section 8).
A base point satisfies, for both messages: the A-recurrence of steps 5..13 (A4..A1 by the
recurrence run backwards, A9..A12 forwards, with every A_i carrying its Table 6 difference),
the E-recurrence of steps 8..13 with W8, W9 entering through dW8, dW9, and W9 in V9.
Construction (charged in Section 7). The 65 base points are the output of one run (seed 777, 16
threads) of this procedure: (a) draw the 47 '=' bits of E5..E12 at random, keep the context if
the E-only parts of steps 8..13 hold and one of the 32 admissible A5 values (those with Table 6's
difference whose step-6 Sigma0 difference is completable by MAJ) gives W9 in V9; (b) up to 2^14
random A6 with Table 6's difference: step 7's MAJ choices fix 12 bits of A4; every A7 satisfying
step 8 is enumerated by a meet-in-the-middle over 2^10 MAJ choices and 2^10 Sigma0 sign choices
followed by a GF(2) solve; A7 is kept if step 6 is satisfiable on the low 13 bits; step 9 is
solved for A8 with A8's low 13 bits fixed through A4 = c - A8; each A8 gives A4, A3, full checks
of steps 6, 7, 9 and of steps 10..13; a success is a base point.

## 5. Algorithm (B = 65 base points from the advice, N = 188345456 first blocks)

P0 setup: G16, V7, V8 (Section 3), the GF(2) inverse of s1, lookup tables.
P2 variants: for each base point and each of the 2^17 settings of the 17 '=' bits of E5..E8,
keep A5..A8, recompute A4..A1 and keep the setting if it satisfies the base-point conditions of
Section 4. Result: 12800 starting points.
P3 table: for each starting point and W8 in V8: E4 = E8 - A4 - S1(E7) - IF(E7,E6,E5) - K8 - W8;
keep E4 if step 7 holds for both messages; step 6 then fixes E3 on the 7 bits of E5's difference
uniquely; for each W7 in V7 with E3 = E7 - A3 - S1(E6) - IF(E6,E5,E4) - K7 - W7 of that form (V7
bucketed by its low 6 bits) store (A_-1 = E3 - A3 + S0(A2) + MAJ(A2,A1,A0), starting point, W7,
W8), A0 = E4 - A4 + S0(A3) + MAJ(A3,A2,A1). Sort by A_-1. Result: 75675936 entries.
P4 first blocks: N times draw M0 (two fresh random words per block), CV = f31(IV,M0), look up
A_-1. Per hit: E2 = A_-2 + A2 - S0(A1) - MAJ(A1,A0,A_-1), W6 from step 6, require W6 in V6;
E1 = A_-3 + A1 - S0(A0) - MAJ(A0,A_-1,A_-2), W5 from step 5; E0 and W0..W4 from steps 0..4; for each
W16 in G16: W18 = s1(W16) + W11 + s0(W3) + W2, require the W20 split; then P5.
P5 completion: W14 = s1^-1(W16 - W9 - s0(W1) - W0); draw E13 (at most 2^18 draws) until E14 carries
Table 6's difference and steps 14..15 hold for both messages; draw E15 (at most 2^12) until steps
16..17 hold; W13, W15 from steps 13, 15. Output M0||M1, M0||M1' if f31(CV,M1) = f31(CV,M1').
Correctness: a returned pair is checked by both block-2 compressions; M1 != M1' as dW5 != 0.

## 6. Success probability

Under H1 the A_-1 of each first block is uniform, so hits per block have mean E/2^32 with
E = 75675936; per hit W6 is uniform (in V6 with probability 2^-9 exactly), and W5 and the
offset W11 + s0(W3) + W2 are uniform and independent, so the split succeeds with probability
p_split (Section 3); P5 then completes (H3). Expected successes:
lambda = N * E * 2^-9 * p_split / 2^32 = 188345456 * 75675936 * 2^-9 * 2^-12.6621 * 2^-32 = 1.0000.
Under H2, P(success) = 1 - exp(-lambda) = 0.632; the claim is 0.55.
Supporting run statistics (not used in the bound): 120 independent runs of exactly this algorithm
(same advice, N, fresh seeds) succeeded 71 times (Wilson 95% interval [0.50, 0.68]); observed/model
ratios: hits 1.0002, W6 passes 0.9978, split events 0.85; P5 succeeded in all 71 split events.

## 7. Charged work

Exact counts are properties of the advice (P2, P3) or of the parameters (P4); per-iteration
costs are upper bounds in word operations (Section 1 weights), divided by 2140.

| Phase | Exact count x bound (word operations) | Units |
| --- | --- | ---: |
| P4 first blocks | (N + 65536 counter slack) x (1 compression + 40) | 2^27.516 |
| P4 hits, P5 | 3.32e6 hits x 150; 6.5e3 W6 passes x 3000; <= 4 completions x 3.7e7 | 2^18.3 |
| P3 table | 632422400 W8 x 18; 74736320 E4 x 170; 272867840 W7 x 25; 75675936 entries x 60 | 2^23.98 |
| P2 variants | 8519680 settings x 290; 392192 full checks x 990 | 2^20.35 |
| P0 setup | 2^27.7 operations | 2^16.6 |
| Advice construction | counts below, x 4 margin | 2^26.42 |
| Total | | < 2^28.17 |

Advice construction counts (seed-777 run): 775163 E contexts x 1400; 5300384 A6 x 80; 330571
feasible A6 x 1000; 343304384 meet-in-the-middle steps x 25; 360527 GF(2) solves x 11000;
20961775 A7 x 80; 20961775 step-6 tests x 300; 74995 triples x 1000; 91611136 A8 x 227;
46108800 late checks x 100: 4.78e10 operations = 2^24.42 units, charged as 2^26.42. Without the
margin the total is 2^27.79. Memory: table and sort buffer 24 bytes per entry (2^30.76 bytes),
index 2^26 bytes, starting points < 2^21 bytes: < 2^30.9 bytes.

## 8. Experiment `completion` (organizer-executed)

`experiments/complete.py` embeds the 65 base points and the 16 certificate pairs. It first checks
every base point against the conditions of Section 4 (observation `advice_bases_valid`). For each
organizer trial it takes certificate pair (trial mod 16), recomputes CV and steps 0..12 of both
messages, checks them against Table 6 (`steps_0_12_follow_table6`), keeps W0..W12 and W14, runs
P5 with E13 and E15 drawn from the trial seed, and returns the new pair. A full collision in every
trial shows that P5 completes after a matched first block, independently of the original W13, W15.

## 9. Heuristic premises

H1 (score-critical): first-block chaining values are uniform, so hits per block have mean E/2^32
and W6, W5 and the W18 offset are uniform and independent at a hit.
H2 (score-critical): success events of distinct (first block, entry) pairs are rare and nearly
independent, so P(success) = 1 - exp(-lambda).
H3 (supporting): after a split event P5 succeeds within its caps (experiment `completion`).
Limitations: H1 and H2 are the usual heuristics of such attacks, supported here only by the run
statistics of Section 6; the advice-construction counts are reported by us (charged with margin).

## 10. Certificates

Sixteen pairs M0||M1, M0||M1' (128 bytes each) from distinct runs of Section 6 (same advice,
different random first blocks); the 32-step digests differ. Files are in `certificates/`.

- `s9000`: run seed 9000, 157385147 first blocks; digest `459cab7b99b4ef536a732db7eaba3697731ae581a5aef6dead4ef58d097e5163`
- `s9001`: run seed 9001, 180812414 first blocks; digest `847b6c4492bba72ea15029593eb2646d7a6f7e04bdc87e4c14013bc3f61ba82d`
- `s9002`: run seed 9002, 151641538 first blocks; digest `8319956a4767f028c8a4976aea859b2df53662f63ab8c0628884aaa79a0e8749`
- `s9003`: run seed 9003, 88887721 first blocks; digest `084192889f0baed477b5962f530d02578cce3588db1899494eaffc6f57f3c2ee`
- `s9004`: run seed 9004, 145738846 first blocks; digest `b3c9ee2e7387b783cae9ada0e007bfc5c26fa39fb1b70a58263730576d9a52b4`
- `s9006`: run seed 9006, 99007565 first blocks; digest `65a76b0381e68d5f453e0f62ad42fe46fb977dbb1269209555ad024dbbbadb39`
- `s9007`: run seed 9007, 45263971 first blocks; digest `225156f1d6397bd951e5cbf6c5804748385bbfa64f18223ae4dd47faaa15d188`
- `s9008`: run seed 9008, 163103178 first blocks; digest `35ae68731aecc140397914d145f5d257b1bbeceae8cb7601d759d59ee4083dbe`
- `s9009`: run seed 9009, 33231381 first blocks; digest `e8d8a810475be72ed0b665bee9a78bcc2902b63ed7752531f54d9504267ebb38`
- `s9012`: run seed 9012, 1871704 first blocks; digest `e4f48d5d5df42e8c0f909d6bbb003b78fbeb4e195610d572c5f503165470ed81`
- `s9013`: run seed 9013, 131444540 first blocks; digest `e9cd1be693d3cc0c56480869fa222f55573a70a7b6a92f8fef215e6c6523f1bf`
- `s9017`: run seed 9017, 65706317 first blocks; digest `c29ec08eea87dd5a83c93f236bee7386867514410f8dbb583eacf69bc9791a1f`
- `s9018`: run seed 9018, 86197556 first blocks; digest `7d109332946f83242b866b77830e3a775db2fbb1d5f3200810ec1aa1b51d8f40`
- `s9019`: run seed 9019, 151422929 first blocks; digest `9958e7b7db824aa254db32ec423242f1514355f5c2fee23e09828336927a838e`
- `s9020`: run seed 9020, 49782907 first blocks; digest `ee69e6172d67f5578c9ab6994f0571dcd6679e7ef6ea65d58079888e7067f636`
- `s9022`: run seed 9022, 54907 first blocks; digest `d17a4aade5f7060d659c3136bdac8863dadd5070744a49ca275e214f004ab3d7`

## 11. References

[MNS13] F. Mendel, T. Nad, M. Schlaffer, Improving Local Collisions: New Attacks on Reduced
SHA-256, EUROCRYPT 2013. [LLW24] Y. Li, F. Liu, G. Wang, New Records in Collision Attacks on SHA-2,
EUROCRYPT 2024, eprint 2024/349. [LLWDS24] Y. Li, F. Liu, G. Wang, X. Dong, S. Sun, The First
Practical Collision for 31-Step SHA-256, ASIACRYPT 2024.
