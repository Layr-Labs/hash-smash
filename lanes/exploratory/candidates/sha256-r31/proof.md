# SHA-256 reduced to 31 steps: a two-block ordinary collision in under 2^28 compressions

Track `sha256-r31-exploratory`, target `sha256-r31-prefix-v1`, cost model `collision-frontier-v5`
(one 31-step compression = 1 unit, any other 256-bit word operation = 1/2140), policy
`paired-lanes-v1`. This package specifies a concrete randomized algorithm, its parameters, its
charged work and its success probability. Evidence: exact enumerations (Section 3), 200 independent
full executions of the algorithm at the stated parameters (Section 6), and 8 fresh colliding pairs
found by those executions (Section 9, organizer-verified certificates).

## 0. Claim

| Field | Value | Derivation |
| --- | --- | --- |
| time_log2 | 28 | Section 7: largest charged run 2^27.44, mean 2^27.31 |
| success_probability | 0.5 | Section 6: model 1-exp(-lambda) = 0.59; observed 129/200 |
| memory_log2_bytes | 33 | Section 7: peak < 2^33 bytes |
| preprocessing_log2 | 27 | Section 7: phases P0-P3, included in time |
| nonuniform_advice_log2_bytes | 11 | Section 2: the characteristic, < 2 KiB |

The attack is the two-block method of Mendel-Nad-Schlaffer [MNS13] with the 31-step
characteristic of Li-Liu-Wang [LLW24, Table 6] in block 2 and the matching framework of
Li-Liu-Wang-Dong-Sun [LLWDS24] (table of A_{-1} values, first-block search, W13..W15 completion).
[LLWDS24] reports 2^40.5 time with a 2^19.8-entry table. Four changes give the improvement:

1. Message-word conditions are the exact modular message-expansion conditions, not the signed
   patterns of Table 6. W8 then has 49408 admissible values instead of 2^13.
2. The cancellation in W20 may split freely between sigma0(W5) and sigma1(W18): the completion
   picks W18 for whatever split W5 produced. Per table hit this raises the W5/completion success
   from 2^-19.09 (fixed split) to 2^-12.663.
3. Starting points come from a dedicated search (no SAT solver, no published pair): about 2^18.5
   units per base point, each multiplied by about 191 free-bit variants.
4. Memory is not scored, so the table holds about 2^27.3 entries and the first-block search is short.

## 1. Target and notation

A message is M0||M1 (128 bytes); its padded form adds one identical third block for both messages.
Every block uses steps 0..30 with the standard constants, schedule and feed-forward, starting from
the standard IV. If f31(f31(IV,M0),M1) = f31(f31(IV,M0),M1') with M1 != M1', the third block and
the digests agree. Write CV = f31(IV,M0) = (A_-1,A_-2,A_-3,A_-4,E_-1,E_-2,E_-3,E_-4). Step i:

    E_i = A_{i-4} + E_{i-4} + S1(E_{i-1}) + IF(E_{i-1},E_{i-2},E_{i-3}) + K_i + W_i
    A_i = E_i - A_{i-4} + S0(A_{i-1}) + MAJ(A_{i-1},A_{i-2},A_{i-3})
    W_t = s1(W_{t-2}) + W_{t-7} + s0(W_{t-15}) + W_{t-16}  (t = 16..30)

Primes denote M1'. Word-operation weights used in Section 7: 32-bit add/sub 2, rotation 4,
shift 1, and/or/xor 1, not 2, compare/branch 1, load/store 1, random word 1; hence S0, S1 = 14,
s0, s1 = 11, IF, MAJ = 5. A 31-step compression costs 2140 such operations (cost model).

## 2. Characteristic (the only nonuniform input)

Table 6 of [LLW24] (eprint 2024/349, CC BY), rows with any condition; all other rows -4..30 are
'=' (no difference, no condition). Columns: row i, then the A_i, E_i and W_i rows; string
position k is bit 31-k; 'u' = (0,1) and 'n' = (1,0) for (M1, M1'), '0'/'1' fixed values.

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

The algorithm uses: the signed differences of A_5..A_10 and E_5..E_16 exactly as above; the fixed
bits of E_5..E_12 (their 47 '=' bits are chosen at random); and only the modular message
differences dW5 = fffff006, dW6 = 002087f1, dW7 = 4fefb5fa, dW8 = 28011100, dW9 = 00008004,
dW16 = 00008004, dW18 = ffff7ffc (M1' = M1 + dW on words 5..9). Every step check below is a direct
evaluation of the step equations for both messages, so no hand-derived condition list is relied on;
the bit conditions in the E_3, E_4 and W rows are replaced by checks of steps 6..7 and Section 3.
Like the published complexities this track's frontier uses, the time excludes the one-time search
that produced Table 6 (no published figure); the table itself is charged as advice (< 2^11 bytes).

## 3. Exact message-word sets

W_i enters every step additively, so only dW_i matters for the states; the expansion needs
dW_t = 0 for t = 19..30 except the cancellations below (W17, W19, W25..W30 are automatic):

| Event | Condition | Exact count over 2^32 |
| --- | --- | ---: |
| G16 | s1(W16+dW16) - s1(W16) = dW18 | 64 |
| V6 (W21) | s0(W6+dW6) - s0(W6) = -dW5 | 2^23 |
| V7 (W22) | s0(W7+dW7) - s0(W7) = -dW6 | 512 |
| V8 (W23) | s0(W8+dW8) - s0(W8) = -dW16 - dW7 | 49408 |
| V9 (W24) | s0(W9+dW9) - s0(W9) = -dW8 | 35921920 |
| split (W20) | s0(W5+dW5) - s0(W5) = -(s1(W18+dW18) - s1(W18)) | see below |

V7, V8 and G16 are built without a 2^32 scan: for each carry pattern of W + dW (depth-first over
bit positions, 2.2e5 nodes in total) the XOR difference is fixed, the sign of every output bit of
s0/s1 is then a GF(2)-linear function of W, and the signs are unique when they exist; 10 small
linear solves give exactly the lists above (cross-checked against an exhaustive scan).
Split event: for uniform W5 and a uniform offset b, the probability that some W16 in G16 makes
W18 = s1(W16) + b satisfy the W20 condition is 2^-12.663 (Monte Carlo, 2^30 trials, 165534 events;
the expected number of such W16 is 2^-12.105, the deficit is clustering among the 64 candidates).
With the split fixed as in Table 6 the same event has probability 2^-19.09.

## 4. Algorithm (parameters B = 128 base points, N = 8.0e7 first blocks)

P0 setup. Build G16, V7, V8 (Section 3), the GF(2) inverse of s1, the 32 values of A5 that have
Table 6's signed difference and a step-6 Sigma0 difference completable by MAJ (scan of 2^22),
and hash tables of the signed subset sums used in P1.
P1 base points. Repeat until B base points exist (16 workers, 8 each; at most 4 extra at the end):
 a. E context: E5..E12 = Table 6 bits + 47 random free bits; keep it if the E-only parts of steps
    8..13 hold for both messages and a listed A5 gives W9 = c9 - A5 in V9 (c9 depends on E only).
 b. Up to 2^14 random A6 with Table 6's difference: (i) look up the step-7 MAJ choices, which fix
    12 bits of A4; (ii) enumerate every A7 satisfying step 8: meet-in-the-middle over the 2^10 MAJ
    choices and 2^10 Sigma0 sign choices, then a GF(2) solve of the linear constraints;
    (iii) keep A7 if step 6 is satisfiable on the low 13 bits; (iv) solve step 9 for A8 with A8's
    low 13 bits fixed by A4 = c - A8 (same method); (v) for each A8: A4 = c - A8, A3 from step 7,
    full checks of steps 6, 7, 9; A9..A12 from steps 9..12; check steps 10..13 and A10's difference.
    A success gives a base point (A1..A12, E5..E12, W9..W12).
P2 variants. For each base point, all 2^17 settings of the free bits of E5..E8 with A5..A8 fixed;
recompute A4..A1; keep settings passing A-steps 5..13, E-steps 8..13 (both messages) and V9.
P3 table. For each starting point and each W8 in V8: E4 = c8 - W8; keep E4 if step 7 holds; step 6
then fixes E3 on the 7 bits of E5's difference uniquely; for each W7 in V7 with E3 = c7 - W7 of
that form (V7 bucketed by its low 6 bits) store (A_-1 = E3 - A3 + S0(A2) + MAJ(A2,A1,A0),
starting point, W7, W8). Radix-sort by A_-1 (12-byte entries).
P4 first blocks. N times: draw a random M0 (two fresh random words per block), CV = f31(IV, M0),
look up A_-1. For each hit: E2 and W6 from A_-2 (require V6); E1, W5 from A_-3; E0 and W0..W4;
for each W16 in G16: W18 = s1(W16) + W11 + s0(W3) + W2, require the W20 split; then P5.
P5 completion. W14 = s1^{-1}(W16 - W9 - s0(W1) - W0). Draw E13 (at most 2^18 tries) until E14 has
Table 6's difference and steps 14..15 hold; draw E15 (at most 2^12 tries) until steps 16..17 hold;
set W13, W15 from the step equations. Return M0||M1, M0||M1' if f31(CV,M1) = f31(CV,M1').

## 5. Correctness

A returned pair is checked by computing both block-2 compressions; M1 != M1' because dW5 != 0;
the common third block then gives equal 256-bit digests. Nothing else is assumed for correctness.

## 6. Success probability

Per first block the number of table hits is E/2^32 (E = table entries). Per hit, W6 is uniform and
lies in V6 with probability 2^-9 exactly; then W5 and the offset W11 + s0(W3) + W2 are uniform and
independent, so the split event has probability 2^-12.663 (Section 3); P5 then succeeds (observed
in every case, caps never reached). Hence lambda = N * E * 2^-53.663 expected successes and
P(success) = 1 - exp(-lambda) for these rare, nearly independent events (Poisson).

| Quantity (200 runs) | Observed | Model |
| --- | ---: | ---: |
| table hits / (N_used * E / 2^32) | 0.9998 | 1 |
| W6 passes / (hits * 2^-9) | 0.9999 | 1 |
| split events / (W6 passes * 2^-12.663) | 1.15 | 1 |
| completions / split events | 129/129 | 1 |
| successes | 129/200 | 0.59 |

Mean E = 2^27.28 gives lambda = 0.91. The Wilson 95% interval for the observed rate is [0.58, 0.71].
The claimed 0.5 lies below both the model and the observed lower bound.

## 7. Charged work

Iteration counts are the counters of each run; per-iteration costs are upper bounds in word
operations (Section 1 weights), divided by 2140. The full budget N is charged even when a run
stops early.

| Phase | Per-iteration bound (word ops) | Mean units | Max units |
| --- | --- | ---: | ---: |
| P4 first blocks | 1 compression + 40 | 2^26.28 | 2^26.28 |
| P1 base points | E context 1400; A6 80; feasible A6 1000; MITM step 25; GF(2) solve 11000; A7 80; step-6 test 300; triple 1000; A8 227; late checks 100 | 2^25.52 | 2^25.86 |
| P2 variants | setting 290; full check 990 | 2^21.32 | 2^21.35 |
| P3 table | W8 18; kept E4 170; W7 candidate 25; entry (sort, index) 60 | 2^25.02 | 2^25.38 |
| P4 hits, P5 | hit 150; W6 pass 3000; split 200; E13 try 140; E15 try 80 | 2^17.76 | 2^18.79 |
| P0 setup, verification | 2^27.7 operations + 8 compressions | 2^16.6 | 2^16.6 |
| Total | | 2^27.31 | 2^27.44 |

time_log2 = 28 leaves 0.56 bits of slack over the most expensive of the 200 runs. Memory: the
table and its sort buffer (24 bytes per entry, at most 2^27.89 entries), the index (2^26 bytes) and
the starting points (< 2^22 bytes): < 2^33 bytes. Preprocessing (P0..P3) is < 2^27 units.

## 8. Heuristic premises

H1 (score-critical): chaining values of random first blocks are uniform; A_-1 is independent of
the table and A_-2, A_-3 make W6, W5 uniform and independent. Supported by the hit and W6 rates.
H2 (score-critical): the split probability 2^-12.663 measured for uniform W5 and offset applies to
the attack's W5 and W11 + s0(W3) + W2. Supported by the observed split rate.
H3 (supporting): P5 succeeds whenever a split event occurs (all observed cases, no cap reached).
H4 (score-critical): base-point cost and yield per base point (counts in Section 7) are as measured
over the 200 runs; the totals over B = 128 base points concentrate (max/mean in Section 7).
H5 (score-critical): successes are rare and nearly independent, so 1 - exp(-lambda) applies.
Limitations: all premises are empirical; the characteristic's own search cost is not charged; the
measurements were made by us (the certificates are the organizer-checkable part).

## 9. Certificates

Each pair is M0||M1 and M0||M1' (128 bytes), from a different run of Section 6, with a
different random first block; the 32-step digests differ. Files are in `certificates/`.

- `run5000` (seed 5000, 36529611 first blocks before success): digest `28fe5869e88069641c453e2ff58fafff387af7ceb8c4929aa90df99723d6cfda`
- `run5001` (seed 5001, 47090310 first blocks before success): digest `7289402d7c5b65c6c731ec2f65bdc7ea0f758433341663693655cb6967595363`
- `run5002` (seed 5002, 1977899 first blocks before success): digest `8ffadaeba54b0d7ce9561003e663698c00ff6ef7607aa67bc56981ca5dc87a31`
- `run5003` (seed 5003, 57596996 first blocks before success): digest `b652f7b50e602df0e91b9c63a09502746d615e788daff639c3e867328ac07509`
- `run5005` (seed 5005, 51007530 first blocks before success): digest `bba0339a6aa90c81d705e73c77227ab3286d0c4742ee7c4a4a121ca3f140c9cb`
- `run5007` (seed 5007, 33938640 first blocks before success): digest `14142657e4f5602bc835cdcf7e1181aafce7dd5f3382aa0324deff5f6eb92300`
- `run5008` (seed 5008, 20915273 first blocks before success): digest `2c30c4bdc2487752923eb50475682e868f663f52258dd073275c4221a6f20faf`
- `run5010` (seed 5010, 27616941 first blocks before success): digest `7caa9489273d6cc0ae6e24565d1253ec325daae25a178b49e26c81685c7f33f9`

## 10. References

[MNS13] F. Mendel, T. Nad, M. Schlaffer, Improving Local Collisions: New Attacks on Reduced
SHA-256, EUROCRYPT 2013. [LLW24] Y. Li, F. Liu, G. Wang, New Records in Collision Attacks on SHA-2,
EUROCRYPT 2024, eprint 2024/349 (Table 6, Section 4.2). [LLWDS24] Y. Li, F. Liu, G. Wang, X. Dong,
S. Sun, The First Practical Collision for 31-Step SHA-256, ASIACRYPT 2024.
