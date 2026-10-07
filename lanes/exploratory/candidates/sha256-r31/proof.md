# sha256-r31: replay of a collision from our own fixed-seed construction (relaxed W20 matching)

## 1. Claim

Track `sha256-r31-exploratory`, target `sha256-r31-prefix-v1` (ordinary collision, SHA-256 steps
0..30 on every padded block, standard IV, FIPS padding, all eight digest words), cost model
`collision-frontier-v5` with C = 2140 (one 31-step compression = 1 unit, any other 256-bit word
operation = 1/2140 unit), review policy `paired-lanes-v1`, exploratory lane.

The scored program (Section 3) replays one stored pair of distinct 128-byte messages that collide
under sha256-r31. It uses no coins, so its success probability is 1.

We produced the stored pair ourselves, with construction K (Section 7). K was fixed in advance:
seed, program hash, trial order and stopping rule were all committed before it ran. It was executed
once and found its first collision at trial n* = 30,706,544,944 (2^34.838).

That was early. A first success so soon has probability about 0.030 for a fresh seed. So we do not
charge the executed work. We charge the worst case of K' instead. K' is K with hard caps: at most
N_B = 526,452,260,864 trials (2^38.938) and fixed caps on every inner event (Section 7). The executed
run stayed far inside every cap, so K' on the committed seed has exactly the same transcript.

The time and preprocessing fields are therefore per-run caps of K' (Section 9). They hold on every
run, with no probability premise. N_B is the smallest budget at which K' succeeds with probability
at least 0.41 on a fresh seed under the measured rates (Section 11, H5, supporting). The score is thus
an attack cost, not the luck of this run.

| field | value | where |
|---|---|---|
| time_log2 | 38.97 | cap of K' plus replay, 2^38.9595, Section 9 |
| preprocessing_log2 | 38.96 | cap of K', Section 9 |
| success_probability | 1 | deterministic replay, Section 3 |
| nonuniform_advice_log2_bytes | 9 | the stored 256-byte pair, Section 10 |
| memory_log2_bytes | 22.25 | measured peak of K, Section 10 |

K uses the two-phase framework and the 31-step trail of Li, Liu, Wang, Dong and Sun (ASIACRYPT
2024), with one change of ours: the relaxed W20 condition R20 (Section 5). The published trail fixes
one pair of sigma-differences for W5 and W18. R20 only asks that the two differences cancel, which
is exactly the requirement dW20 = 0. With R20, one starting solution, taken from the published pair,
is enough.

Heuristics are declared in Section 11:
- H1-public-text (score-critical): the published trail and pair are public algorithm text;
- H2-op-accounting (score-critical): the word-operation charges per capped event;
- H3-prospective-route (score-critical): earlier research runs are not part of the construction;
- H4-memory (supporting);
- H5-budget-rationale (supporting): why N_B gives success at least 0.41.
The probability analysis only motivates N_B. The time bound does not depend on it.

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

## 3. The scored program (replay)

R1. Read the stored advice: two 128-byte strings P and P' (Section 4).
R2. Compute sha256-r31(P) and sha256-r31(P'): three compressions each.
R3. If P != P' and the digests are equal, output (P, P'). Otherwise output nothing.

The organizer verifier confirms the relation for these bytes (certificate `relaxed-k-1`). R uses no
coins, so its probability space is a single point and the success probability is 1. Cost: 6
compressions + at most 768 word operations = 6.36 units.

## 4. The stored pair

    M0  : 116ea499 88c615bc d08e5d69 2e2c45e7 1e24036b 3c901634 bee5b003 edbd23bf
          c57b8553 14b16470 ad99b788 b5b33cfb 9830ebc8 988306cc 93a61b60 0040b130
    M1  : 1aeca717 7359f369 5e2ecdf3 52f74740 a81916cc 8090da83 b8c3557a 215af20a
          9ba486ee eb830a58 66add94a 9669232d 45271fa5 6c11cb6d 6912669a f2088f17
    M1' : 1aeca717 7359f369 5e2ecdf3 52f74740 a81916cc 8090ca89 b8e3dd6b 714aa804
          c3a597ee eb838a5c 66add94a 9669232d 45271fa5 6c11cb6d 6912669a f2088f17
    sha256-r31(M0||M1) = sha256-r31(M0||M1') = 3795d250ad2d59f1762ac359f66e1604aba83eb9d90a153756e8551d9bfdf5f9

M0 is our own first block, from trial n* = 30,706,544,944 of K. The second blocks differ in words 5..9 by
d5..d9. In this pair, s0(W5+d5) - s0(W5) = 0ffd7e1f and s1(W18+d18) - s1(W18) = f00281e1. These
are not the published trail's values (d0018020 and 2ffe7fe0), but they cancel. So this collision
exists only because of the relaxed condition R20.

## 5. Public inputs and the relaxed condition

5.1 The published pair and S. The ASIACRYPT 2024 pair (certificate `published-31step-pair`) is
public text. Running its second block from its chaining value (2 compressions, charged in Section 9
as line P0) gives the starting solution S, copy P:

    A1..A12 : f36e6fcf b741c202 90c67413 fc7566c3 fa9053fb 11af5d4e 87f5120c 9180b607
              4f5af3a8 4b9e4fb8 83e817e6 2be31c3f
    E5..E12 : 1d1fa7dd afe878e7 4c97cbe5 946f8048 61c171d3 f02293fa aa270418 b1f7f9e8
    W9..W12 : eb830a58 66add94a 9669232d 45271fa5

Copy P' adds the trail's modular differences: A5 fffff006, A6 ff800001, A7 0edfeffd, A8 fffffffc,
A10 00008004, E5 fffff006, E6 fff87fff, E7 4f880387, E8 44ff8804, E9 00000008, E10 ef808008,
E11 10bffff8, E12 ffff7ff8, W9 00008004.

5.2 The published trail (public text):

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
16:(0,2,17) 18:(0,0,4). Evaluating every one of the 300 cells on the published pair (second block from its chaining value) gives zero violations.

Modular differences X' - X implied by the table and observed on the pair:

    W:  d5 = fffff006  d6 = 002087f1  d7 = 4fefb5fa  d8 = 28011100  d9 = 00008004
        d16 = 00008004 d18 = ffff7ffc  (every other W[t], t <= 30, has difference 0)
    A:  A5 fffff006  A6 ff800001  A7 0edfeffd  A8 fffffffc  A10 00008004
    E:  E5 fffff006  E6 fff87fff  E7 4f880387  E8 44ff8804  E9 00000008
        E10 ef808008 E11 10bffff8 E12 ffff7ff8 E14 00008004

The table is the published 31-step trail (ASIACRYPT 2024 presentation, slide 14), transcribed
cell by cell; rows 3 and 4 carry value conditions on E[3] and E[4] and are kept.

5.3 Message expansion and R20. In the second block only W5..W9 differ, by d5..d9. For t = 16..30:

    t=16: dW16 = d9.
    t=18: need W16 in G16 = {w : s1(w+d9) - s1(w) = d18}, so that dW18 = d18.
    t=20: need s1(W18+d18) - s1(W18) + s0(W5+d5) - s0(W5) = 0.   (R20)
    t=21: need W6 in V6 = {w : s0(w+d6) - s0(w) = 00000ffa}.
    t=22: need W7 in V7 = {w : s0(w+d7) - s0(w) = ffdf780f}.
    t=23: need W8 in V8 = {w : s0(w+d8) - s0(w) = b00fca02}.
    t=24: need W9 in V9 (true for S).
    t=25: d18 + d9 = 0.  t=17, 19, 26..30: no term has a difference.

The trail meets R20 with s0-difference d0018020 for W5 and s1-difference 2ffe7fe0 for W18. K only
requires R20 itself. W5 and W18 enter the state update only additively, through d5 and d18, so the
state conditions of the trail are unaffected.

Set sizes (exhaustive over 2^32): |V6| = 2^23, |V7| = 512, |V8| = 49408, |G16| = 64. G16 is the
set of (h << 28) | lo with h = 0..15 and lo in {031bbffc, 064bbffe, 09b3bffd, 0ce3bfff}. s1 is
invertible (GF(2) rank 32).

## 6. Why an output of K collides

Steps 0..4 carry no difference. W0..W8 are chosen so that copy P reproduces S, the matched record
and the derived E0..E2. S carries the trail's difference relations for steps 5..13; P2 below checks
F6 and F7 on each record. K step K5 checks steps 14..17 explicitly. Step 18 cancels dE14 = 00008004
against dW18. Under R20, V6, V7, V8 and V9, steps 19..30 carry no difference. Both copies start the
second block from the same CV1, so their outputs are equal, and the shared padding block keeps the
digests equal. K re-hashes every candidate pair before storing it (K6). So correctness does not
depend on this argument: the stored pair is verified, by K and by the organizer.

## 7. Construction K (fixed before execution)

Commitment, made before the run and recorded in Section 8:
- seed = first 64 bits of SHA-256 of the ASCII text
  "yukon hashsmash sha256-r31 relaxed-W20 deterministic construction v2 2026-10-07",
  which is 953a88e705d6792e;
- the program's SHA-256;
- 12 threads and a wall-clock cap of 3000 s.

P1. Scan all 2^32 words once and keep V7, V8 and G16.

P2. From S, for each W8 in V8:
  E4 = E8 - A4 - S1(E7) - IF(E7,E6,E5) - K[8] - W8.
  Keep W8 if the row-4 cells hold on E4 and if
  (E7'-E7) = (S1(E6')-S1(E6)) + (IF(E6',E5',E4) - IF(E6,E5,E4)) + d7.
  Set A0 = E4 - A4 + S0(A3) + MAJ(A3,A2,A1).
For each kept W8 and each W7 in V7:
  E3 = E7 - A3 - S1(E6) - IF(E6,E5,E4) - K[7] - W7.
  Keep W7 if the row-3 cells hold on E3 and if
  (E6'-E6) = (S1(E5')-S1(E5)) + (IF(E5',E4,E3) - IF(E5,E4,E3)) + d6.
  Set A[-1] = E3 - A3 + S0(A2) + MAJ(A2,A1,A0).
Store the record (A[-1]; A0, E3, E4, W7, W8). This gives 16896 records with 2336 distinct keys.
They are sorted, and a 2^24-bit bitmap on key >> 8 is built.

K1 (trial order). Trial n has group g = n >> 24 and offset j = n mod 2^24.
- Group g's words 0..14 are fifteen successive outputs of splitmix64, seeded with
  seed XOR (g * 0x9e3779b97f4a7c15) XOR 0x5bd1e9955bd1e995, each truncated to 32 bits.
- Word 15 is j.
- Thread t processes groups t, t+12, t+24, ... in increasing order.
- Compute CV1 = compress31(IV, M0(n)).

K2. If bitmap bit (A[-1] >> 8) is set, recompute CV1 and binary-search the records with key A[-1].

K3. For each matching record:
  E0 = A0 + A[-4] - S0(A[-1]) - MAJ(A[-1],A[-2],A[-3])
  E1 = A1 + A[-3] - S0(A0) - MAJ(A0,A[-1],A[-2])
  E2 = A2 + A[-2] - S0(A1) - MAJ(A1,A0,A[-1])
  W[i] = E[i] - A[i-4] - E[i-4] - S1(E[i-1]) - IF(E[i-1],E[i-2],E[i-3]) - K[i]   for i = 0..6
W7 and W8 come from the record, and W9..W12 from S. Require W6 in V6.

K4. Require some g in G16 with s1(W18(g)+d18) - s1(W18(g)) = -(s0(W5+d5) - s0(W5)), where
W18(g) = s1(g) + W11 + s0(W3) + W2. Take the first such g.

K5 (completion). Set W14 = s1^-1(g - W9 - s0(W1) - W0). Completion coins come from splitmix64,
seeded with seed XOR (g_group * 0xd1b54a32d192ed03) XOR 0x2545f4914f6cdd1d.
Up to 2^22 times:
  - draw E13 and set W13 = E13 - A9 - E9 - S1(E12) - IF(E12,E11,E10) - K[13];
  - require dE14 = 00008004, dA13 = dA14 = 0, and equal step-15 sums in both copies.
  On success, up to 2^12 times:
  - draw E15 and set W15 from the step-15 equation;
  - require dE16 = 0 and IF(E16,E15,E14) = IF(E16,E15,E14').

K6. Form M1 and M1' = M1 + (d5..d9 at words 5..9). Hash M0||M1 and M0||M1' and store them if the
digests are equal.

Caps of K'. K' is K with these caps added; reaching any cap stops K' without output:
- trial indices n < N_B = 526,452,260,864;
- at most 60,000,000 bitmap hits, 8,000,000 matched records and 40,000 V6 passes;
- at most 64 completion attempts (accepted matches);
- per attempt, at most 2^22 E13 iterations and at most 2^16 E15 iterations in total.
On the committed seed every cap is far from binding (Section 8), so K and K' have the same
transcript.

Stopping rule. Let n* be the smallest trial index whose K6 stores a pair. A thread stops before any
group whose index exceeds n* >> 24, and checks every 2^20 trials whether its current group has
become unnecessary. Every group up to n* >> 24 is therefore processed completely, so n* is
determined by the seed alone. The thread interleaving only adds a little discarded work, and that
work is still charged. The cap was 3000 s; if it had been reached with no output, K would have
failed. It was not reached (Section 8).

## 8. Execution record

Commitment, written before the run (file `seed-commit.txt`):

    yukon hashsmash sha256-r31 relaxed-W20 deterministic construction v2 2026-10-07
    953a88e705d6792e38a9cf0307d7333fda0bbece899b356e92a1105f9f8c16ff
    seed64 953a88e705d6792e
    cab7a4c8a5c3b3b08edf9ced4f04fe7c6b2ce96a391d1418066e25188d38600d  r31det.c
    98858c6089388dfa44e0a487ade75ef46843751baedd4f35b457c0a37b9b6c27  sp.h
    committed 2026-10-07T11:56:06+0900
    --- recommit (binary rebuilt before any run)
    619dcf104c575efc3458cffadff67b18a83cb4594ea2736bd5ce0f9e385823e9  r31det.c
    committed 2026-10-07T11:57:05+0900

Started 12:11:19 KST, under the machine's resource-guard lease, 12 threads, nice 10.
Wall time 42 s of the 3000 s cap. `/usr/bin/time -l`: maximum resident set size 4,702,208 bytes, instructions retired 4,624,919,868,085, cycles 1,442,531,215,098; real 47.30 s, user 402.44 s, sys 3.54 s.

Hard counters, totals over all threads:
    groups started 1,831; trials executed 30,719,082,496 (2^34.8384)
    bitmap hits 892,385; key-matched trials 16,896; matched records 122,475
    V6 passes 240; R20 passes 1; completion attempts 1, successes 1
    E13 iterations 4,384; E15 iterations 7; groups aborted under the stopping rule 0
    first stored pair at trial n* = 30,706,544,944 (group 1830, offset 4239664); candidate pairs that verified 1

Trials per thread: 2566914048, 2566914048, 2566914048, 2566914048, 2566914048, 2566914048, 2566914048, 2550136832, 2550136832, 2550136832, 2550136832, 2550136832.
Trials actually needed for the minimal index are n*+1 = 30,706,544,945; the charged count is the larger executed total.

## 9. Cost ledger: per-run cap of K' (caps times per-event charges; H2 gives the charges)

    P0  derive S from the published pair: 2 compressions                       2
    P1  three 2^32 scans, <= 24 ops per word: 3*2^32*24/2140                  144,503,573
    P2  884,992 candidates, <= 64 ops each, plus sort and bitmap: < 2^26 ops   31,359
    S0  start-up self-checks: 2,000 kernel comparisons (2 compressions each)
        and one replay of the published match: <= 4,200 compressions             4,200
    K1  groups: N_B/2^24 + 12 = 31,391 * 1 unit (15 PRNG words + 15 rounds
        + 16 schedule constants <= 2140 ops)                                    31,391
    K1  trials: N_B = 526,452,260,864 * (1 compression + 32 ops)                       534,324,444,204
    K2  bitmap hits cap 60,000,000 * (1 compression + 64 ops)                     61,794,393
    K3  matched records cap 8,000,000 * 400 ops                                    1,495,327
    K4  V6 passes cap 40,000 * 1600 ops                                           29,907
    K5  64 attempts * ((2^22 + 2^16) * 160 + 200) ops                    20,383,539
    K6  candidate pairs hashed: 64 * (6 compressions + 64 ops)            386
    -------------------------------------------------------------------------------------------
    preprocessing (cap of K')                                                  534,552,718,280 = 2^38.9595
    R   replay                                                                  6.36
    total                                                                       534,552,718,287 = 2^38.9595

Claimed time_log2 = 38.97 and preprocessing_log2 = 38.96. Both are worst-case caps of
K' plus the replay, valid on every run. They are not expectations.

For reference, the executed run of K cost 31,323,916,707 units (2^34.867). That figure uses the
same charges and the hard counters of Section 8: 30,719,082,496 trials, 892,385 bitmap hits,
122,475 records, 240 V6 passes, 4,384 E13 and 7 E15 iterations. It lies far
below the cap and is not claimed. Each trial is charged as a full 31-step
compression, even though K1 shares steps 0..14 within a group. No discount is taken for that.

## 10. Memory and advice

The advice of R is the stored 256-byte pair (2^8 bytes; 9 is claimed). K's peak memory was measured
for the whole process with `/usr/bin/time -l`: maximum resident set size 4,702,208 bytes
(2^22.16). The claim of 22.25 covers it. The bulk is P1's set scan state and K's table
(16896 records, a 2 MiB bitmap).

## 11. Heuristics

H1-public-text (score-critical). The published 31-step trail and the published colliding pair of
Li, Liu, Wang, Dong and Sun are public algorithm text that K may use without charge. This follows
the same convention under which earlier submissions on this track reused the published trail.
- K derives S from the published pair, and charges that derivation (P0) and every operation it
  executes.
- The authors' original trail search and first-block search are not charged again.
- Pinned provenance: the authors' public implementation of the trail search is
  github.com/Peace9911/sha_2_attack at commit 6a9f35fd8d8bdcc1a54dc6f170ed0038ebe5bb32, script
  `find_dc/find_dc_model_31_256.py`.
- Sensitivity: if a reviewer charged the original trail and starting-solution work instead, the
  total would rise by that amount. At 2^38 (an estimate from a public re-run of that tool by another
  solver), the total would be 2^39.558.

H2-op-accounting (score-critical). The per-event charges of Section 9 bound the word operations of
the specified steps:
- per trial: at most 32 operations besides the compression (counter, bitmap index and test, loop
  control);
- per bitmap hit: one recomputed compression plus at most 64 operations (binary search);
- per record: at most 400 (the K3 formulas, about 160 counted);
- per V6 pass: at most 1600 (64 values of g, each two s1 and a few additions, about 25);
- per completion iteration: at most 160 (about 116 for E13 and 78 for E15 counted);
- per group: at most 2140.
The counts come from the program's hard counters (Section 8). The program performs nothing beyond
the specified steps.

H4-memory (supporting). The measured maximum resident set size of the single execution bounds K's
peak memory. It covers code, tables, sets, thread stacks and allocator state. R itself keeps under
2^10 bytes.

H3-prospective-route (score-critical). The construction charged is K', fully specified and executed
once with a committed seed. Earlier research runs are not summed into it; the same convention was
accepted for an earlier submission on this track. Disclosed:
- a fixed-seed, 2700-second run of the same matching loop: 2^40.625 trials, one collision, attached
  as certificate `relaxed-run-1`. It measured the rates used in H5;
- shorter diagnostic runs of 120-200 s each;
- model computations.
These determined K's design and N_B; K' does not depend on their outputs. If a reviewer summed them,
the total would be about 2^41.116.

H5-budget-rationale (supporting). The bound does not depend on this. On a fresh seed, K' succeeds
with probability at least 1 - exp(-N_B * p1) - P(any cap reached) >= 0.41 - 0.01 = 0.40, where
p1 >= 2^-39.860 per trial. p1 is the product of four factors:
- records per trial 2^-17.960;
- V6 per record 2^-9.036;
- R20 per record 2^-12.851;
- completion 0.995 (99% lower bound from 982/982 attempts in that run).
The first three are 99% lower bounds measured in the 2^40.625-trial run. The product also takes a
(1 - 2^-8) correction for records sharing a key. It uses Lemma A: given a matched record and a
uniform CV1, W6, W5 and c18 are independent, because W6 is a bijection of A[-2], W5 of A[-3], and
c18 of E[-2] (via W2). For the caps, Chernoff/Bernstein bounds make the bitmap, record and V6 caps
negligible (each is at least 4x its expectation). The accepted-match cap of 64 is covered by Markov:
at most 0.52/64 < 0.01.

## 12. Organizer-executed experiment and certificates

`experiments/r31-completion` runs a tighter variant of K5 with seed-derived coins on fixed accepted
matches: E13 and E15 respect the row-13 and row-15 cells, and the caps are 2^14 and 2^8. The matches
are the prefix of the stored pair and the other accepted matches listed in the program. The organizer
re-hashes every returned pair. Locally, the organizer intake ran it in the pinned Docker image:
status passed, 256/256 full collisions, 0 repeated pairs. The experiment shows that K5 completes on our accepted matches. The score itself does
not depend on any rate.

Certificates:
- `relaxed-k-1`: the stored pair, from K (trial n* = 30,706,544,944);
- `relaxed-run-1`: from an earlier fixed-seed run of the same matching loop (2^40.625 trials, no
  early stop). It also satisfies only R20, not the trail's W5/W18 values;
- `published-31step-pair`: the ASIACRYPT 2024 pair.

## 13. Sources and credit

- Y. Li, F. Liu, G. Wang, X. Dong, S. Sun, "The First Practical Collision for 31-Step SHA-256",
  ASIACRYPT 2024: the framework, the trail and the published pair.
- Y. Li, F. Liu, G. Wang, J. Shi, ePrint 2026/1080, Section 3: the framework restated.
- Y. Li, F. Liu, G. Wang, EUROCRYPT 2024 (ePrint 2024/349): the SAT/SMT tool.
- Public Yukon submissions on this track: reusing the published trail as public text, and sharing
  steps 0..14 across first blocks that differ only in word 15, both appear there. We use the second
  for speed only and take no discount for it.
- Ours: the relaxed W20 condition, construction K and its execution, and the completion experiment.
