# sha256-r31: replay of a collision built entirely by our own committed construction; search K charged as a 7-lane SWAR word-RAM program

## 1. Claim

Track `sha256-r31-exploratory`, target `sha256-r31-prefix-v1` (ordinary collision, SHA-256 steps
0..30 on every padded block, standard IV, FIPS padding, all eight digest words), cost model
`collision-frontier-v5` with C = 2140 (one 31-step compression = 1 unit, any other 256-bit word
operation = 1/2140 unit), review policy `paired-lanes-v1`, exploratory lane.

The scored program (Section 3) replays one stored pair of distinct 128-byte messages that collide
under sha256-r31. It uses no coins, so its success probability is 1.

We built the stored pair with construction chain C (Section 7). Its only external input is the
published 31-step signed characteristic (Section 5). The characteristic is a table of difference and
value conditions; it is not a collision and contains no message words or state values. C does not
use any published colliding pair, starting solution or first block. C works as follows:
- it solves for its own starting solution S with z3, from a seed committed in advance (three
  attempts, all charged);
- it builds its own table;
- it runs its own first-block search K, again from a committed seed, until the first collision.

Every computation of C is charged (Section 9).
- The z3 runs are charged from their measured retired instructions at a per-instruction price taken
  from profiles of every executed instruction of the same solver on the same models (Section 14):
  callgrind for attempt 1, exp-bbv basic-block vectors for attempts 2 and 3. Every multiply,
  divide and floating-point form is priced by a checked emulation. The price is 7 word
  operations per instruction, with no safety factor; the few instructions exp-bbv does not report
  are charged at 1024 each.
- Search K is charged by an exact operation count (Sections 16 and 17). Its hit processing, group
  set-up and table build are written as an explicit program of the cost model's primitives (Section 16),
  with every load and store counted and no native 32-bit rotation. **Its trials are charged as a 7-lane
  SWAR program (Section 17): seven consecutive trials of one group share a 256-bit word, one 32-bit
  value per 36-bit lane, at 1,115 primitives per seven trials (159.3 per trial instead of 584.6), with 13 lane masks
  held in registers on a 32-register machine (Section 17.7).** The program reproduces the decisions
  of the executable that ran on 71,670,492 trials of the committed run, and it reproduces the
  stored pair. Its worst-path count for each event is multiplied by the run's own event counter.
- The synthetic completion checks are charged the same way, by exact counted replays of the three
  runs that reproduce their logged counters (Section 16.6). This corrects our earlier filings,
  which charged three equal runs.
- The analysis programs that formulated R20 before any search ran are counted the same way; their
  counted versions print exactly the originals' outputs (Section 15.2).
- Our other own code is charged with explicit operation counts.
- Runs that read the published colliding pair or the starting solution derived from it are not part of C
  and are not charged. Besides the relaxed-search, synthetic and K' runs of 10-07, these are the three
  `analyze.py` runs and the two runs of the yield program `table` of the pre-construction analysis,
  which our filings up to v9 had charged as part of C. No constant of C comes from any of them
  (Sections 15.1, 15.4).
The complete source is in Appendices B and C.

| field | value | where |
|---|---|---|
| time_log2 | 34.45 | executed work of C plus replay, 2^34.4275, Sections 9 and 17 |
| preprocessing_log2 | 34.45 | construction chain C, Sections 9 and 17 |
| success_probability | 1 | deterministic replay, Section 3 |
| nonuniform_advice_log2_bytes | 9 | the stored 256-byte pair, Section 10 |
| memory_log2_bytes | 29.5 | measured peak over C and the analysis (`joint`, 2^29.003 bytes), Section 10 |

Our own change to the source attack is the relaxed W20 condition R20 (Section 6). The published
characteristic fixes the s0-difference of W5 and the s1-difference of W18. R20 only requires that
the two cancel, which is exactly dW20 = 0. The stored pair uses differences of 0ffd81e1 and
f0027e1f, not the characteristic's.

Heuristics are declared in Section 11:
- H1-public-characteristic, H2-counted-programs, H3-heavy-tariffs, H5-chain-scope,
  H6-z3-build-transfer, H7-profile-reconstruction and H8-lumps-and-hand-bounds are score-critical;
- H4-memory is supporting.
No probability estimate enters the bound.

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

The organizer verifier confirms the relation for these bytes (certificate `relaxed-v3-1`). R uses no
coins, so the success probability is 1. Cost: 6 compressions + at most 768 word operations, which
is 6.36 units.

## 4. The stored pair

    M0  : e7f5ce55 1741facd 279a66b6 8a38d7c6 cc332e48 ed9dd62a 6b76b5f7 3aa91ac9
          1ca8034e b4a9ad70 5b8eeceb 50a7afad 07617b89 719682b5 394303d8 00459adb
    M1  : 1e2dbac8 05e61a5e cd7fcb49 9db00a7a 186cabb0 f7efd9c2 2a442578 023cd6eb
          f71d59bf 876b73db ed1499e4 7173c145 0ba5f907 b35ebf93 05848707 075e188d
    M1' : 1e2dbac8 05e61a5e cd7fcb49 9db00a7a 186cabb0 f7efc9c8 2a64ad69 522c8ce5
          1f1e6abf 876bf3df ed1499e4 7173c145 0ba5f907 b35ebf93 05848707 075e188d
    sha256-r31(M0||M1) = sha256-r31(M0||M1') = aea2562b20b12c5938046802bcc533817087f43c3e4ac864114c2abdd2249ee5

M0 is the first block of trial n* = 99,325,680,347 of K. Words 9..12 of M1 are those of our starting
solution S (Section 7.1).

## 5. The public characteristic (the only external input)

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
16:(0,2,17) 18:(0,0,4).

Modular differences X' - X implied by the table:

    W:  d5 = fffff006  d6 = 002087f1  d7 = 4fefb5fa  d8 = 28011100  d9 = 00008004
        d16 = 00008004 d18 = ffff7ffc  (every other W[t], t <= 30, has difference 0)
    A:  A5 fffff006  A6 ff800001  A7 0edfeffd  A8 fffffffc  A10 00008004
    E:  E5 fffff006  E6 fff87fff  E7 4f880387  E8 44ff8804  E9 00000008
        E10 ef808008 E11 10bffff8 E12 ffff7ff8 E14 00008004

The table is the published 31-step characteristic (ASIACRYPT 2024 presentation, slide 14), transcribed
cell by cell. Rows 3 and 4 carry value conditions on E[3] and E[4]; we keep them.

## 6. Exact difference requirements and the relaxed condition R20

In the second block only W5..W9 differ, by d5..d9. For t = 16..30:

    t=16: dW16 = d9.
    t=18: need W16 in G16 = {w : s1(w+d9) - s1(w) = d18}, so that dW18 = d18.
    t=20: need s1(W18+d18) - s1(W18) + s0(W5+d5) - s0(W5) = 0.   (R20)
    t=21: need W6 in V6 = {w : s0(w+d6) - s0(w) = 00000ffa}.
    t=22: need W7 in V7 = {w : s0(w+d7) - s0(w) = ffdf780f}.
    t=23: need W8 in V8 = {w : s0(w+d8) - s0(w) = b00fca02}.
    t=24: need W9 in V9 = {w : s0(w+d9) - s0(w) = d7feef00}.
    t=25: d18 + d9 = 0.  t=17, 19, 26..30: no term has a difference.

W5 and W18 enter the state update only additively, through d5 and d18. So R20 leaves the state
conditions of the characteristic unchanged.

Set sizes (exhaustive over 2^32): |V6| = 2^23, |V7| = 512, |V8| = 49408, |G16| = 64.

Why an output of K collides:
- Steps 0..4 carry no difference.
- K chooses W0..W8 so that copy P reproduces S, the matched table record and the derived E0..E2.
- S satisfies the step 5..13 relations by construction (Section 7.1), and the table checks F6 and F7.
- K5 checks steps 14..17.
- Step 18 cancels dE14 = 00008004 against dW18.
- Under R20 and V6..V9, steps 19..30 carry no difference.
- The two copies share CV1 and the padding block, so the digests are equal.
K6 re-hashes every candidate before storing it.

## 7. Construction chain C

7.1 Starting solution S (z3, committed seeds; Appendix A.1). The unknowns are copies P and P' of
A1..A12, E5..E12 and W9..W12, with W10..W12 equal in both copies. There are also existential
witnesses E3, E4, W7, W8. The constraints, generated by `gen_s.py` (Appendix B.1), are:
  (a) every cell of the characteristic on these words, as bit masks per copy;
  (b) the A-equation for i = 5..12 and the E-equation for i = 9..12 in both copies;
  (c) the step-8 relation (E8'-E8) = (S1(E7')-S1(E7)) + (IF(E7',E6',E5')-IF(E7,E6,E5)) + d8;
  (d) dE13 = 0 and dA13 = 0, i.e. the step-13 sums and MAJ(A12,A11,A10) agree in both copies;
  (e) W9 in V9;
  (f) a non-empty table: E8 and E7 equations through (E4, W8) and (E3, W7), F7, F6, the row-3 and
      row-4 cells, W8 in V8 and W7 in V7;
  (g) the yield residue: (E8 - A4 - S1(E7) - IF(E7,E6,E5) - K[8]) mod 2^20 = e730f.

The attempts (all charged in Section 9):
- Attempt 1 (seed 88108363) had (a)-(e). It was sat in 34 s, but the table was empty: F6/F7 had
  no solutions.
- Attempt 2 (seed 88108364) added (f). It was sat in 232 s, with a table of 224 records.
- We then found that row-4 survivors over V8 depend on c8 mod 2^20. A 300,000-sample scan
  (`c8scan.c`, B.3) found residue e730f, where 12352 of the 49408 values of V8 pass.
- Attempt 3 (seed 88108365) added (g). It was sat in 139 s. Its S has 132096 table records and is
  independently verified by `check_s.py` (B.2):

    A1..A12 : 1476a232 3b327cc5 38f76ff9 7d9cb534 066f93fe 4fdbe6b8
              ad2e79f6 0327eecc 53a8814f 200b1769 df4a7a71 cf7d7a3b
    E5..E12 : 1d1fa7dd adea7be7 4c97cbe5 943b8248 61d553d1 f02293fa aa370c18 f1e5b1ec
    W9..W12 : 876b73db ed1499e4 7173c145 0ba5f907
    copy P' : A' = A + dA, E' = E + dE, W9' = W9 + 00008004 (the characteristic's signed differences)

The characteristic's cells fix 31 of the 32 bits of E5 and 29 of E7, and most bits of E6 and E8.
So those words necessarily agree with any other solution, including the authors'. A1..A4 and the
remaining words come from z3 and differ from the published values.

7.2 Table. From S, run the two loops over V8 and V7 with the row-4 and row-3 cells and F7, F6 (the
P2 code in `r31det3.c`). This gives 132096 records; sort them and build a 2^24-bit bitmap.

7.3 First-block search K (`r31det3.c`, B.4; committed seed, Appendix A.2).
- K1. Trial n = g * 2^24 + j. Group g's words 0..14 are fifteen splitmix64 outputs seeded with
  seed XOR (g * 0x9e3779b97f4a7c15) XOR 0x5bd1e9955bd1e995. Word 15 = j. Thread t processes
  groups t, t+12, ...
- K2. If bitmap bit (A[-1] >> 8) is set, recompute CV1 and binary-search the records with key
  A[-1].
- K3. Derive E0..E2 and W0..W6 from CV1 and the record. W7 and W8 come from the record, and
  W9..W12 from S. Require W6 in V6.
- K4. Require some g in G16 that satisfies R20 with W18 = s1(g) + W11 + s0(W3) + W2.
- K5. Set W14 = s1^-1(g - W9 - s0(W1) - W0). Draw E13, at most 2^22 times, requiring dE14 = 00008004,
  dA13 = dA14 = 0 and equal step-15 sums. For each success, draw E15 at most 2^12 times, requiring
  dE16 = 0 and an equal IF(E16,E15,E14). Coins come from splitmix64 seeded per group.
- K6. Hash M0||M1 and M0||M1' and store the pair if the digests are equal.
- Stopping rule: n* is the smallest index with a stored pair. Groups beyond n* >> 24 are skipped
  or aborted. All groups up to it are completed. Cap: 1200 s.

## 8. Execution records

Starting solution (z3 4.15.4, single thread, `z3 -T:1800 -st`, `/usr/bin/time -l`):
    attempt 1: 261,276,415,067 instructions retired
    attempt 2: 1,572,256,055,396 instructions retired
    attempt 3: 888,282,131,643 instructions retired
    attempt 1 34.36 s; attempt 2 231.64 s; attempt 3 138.54 s
    the peak resident sets were 154,107,904, 161,103,872 and 153,944,064 bytes

Diagnostics before K, measured the same way (one representative run each; every run is charged):
    yield check (set scans + table, `r31det3 1 0` three times and `diag 1 0` twice):
        124,752,621,861 instructions per run (5 runs)
    synthetic completion checks, `r31sim3 1 20 5eed3 ... sim`, one with the S of each z3 attempt: run 1
        (attempt 1, no records) stopped with a segmentation fault at its first trial; runs 2 and 3
        completed 275,316,736 and 250,544,128 trials (Section 16.6); a re-run of run 3's command
        retires 500,284,109,323 instructions
    V8 dump: 51,663,872,491; c8 residue scan: 18,618,257,497 instructions (1 run each)
After K had stored the pair, the instruction counts above were measured by re-running `diag` twice,
`r31sim3` twice, `v8dump` and `c8scan` once each. Those re-runs could not influence the stored pair,
and we do not charge them (Section 15.1). The execution record of every run is the agent transcript
of the session that ran them; Section 15.1 lists them.

Search K: started 13:04:56 KST under the machine's resource-guard lease, 12 threads, nice 10.
    executable: `r31det3` built from B.4 and B.5 with `cc -O3 -mcpu=apple-m4 -o r31det3 r31det3.c -lpthread`
    at 13:04, SHA-256 2824a0f855c203d1ada6f99e5a25fa8aebd4f2feeee0a8a56776c311af4bce23 (Section 14.6)
    /usr/bin/time -l: real 139.76 s, user 1351.89 s; maximum resident set 7,438,336 bytes; 15,640,902,198,904 instructions retired
    groups 5,932; trials executed 99,492,036,640 (2^36.534); bitmap hits 58,831,394; key-matched trials 1,376,281
    matched records 3,061,666; V6 passes 5,992; R20 passes 1; completion attempts 1, E13 iterations 2,829, E15 iterations 19
    first stored pair at n* = 99,325,680,347 (group 5920, offset 4561627); aborted groups 4

## 9. Cost ledger (executed work of C)

The z3 runs are charged at the measured per-instruction price of Section 14 (H3). Search K and the
synthetic checks are charged by the operation counts of their counted programs (Section 16, H2).
The analysis programs of Section 15.2 are charged by the exact operation counts of their counted
versions (H2). Our other own code is charged with the operation counts of H2.

    z3 attempts 1-3 (Section 14.4, H3, H6, H7): 2,721,814,602,106 instructions * 7
        + (1024 - 7) * 1,989,181,169 final-interval instructions = 21,075,699,463,615 ops / 2140   9,848,457,694
    synthetic completion checks (Section 16.6, H2): exact counted replays,
        4,134,261,321,301 ops / 2140                                               1,931,897,814
    yield checks: 5 * (three 2^32 scans <= 24 ops/word + table <= 6.4e6 * 64 ops)        723,470,929
    V8 dump (one 2^32 scan, <= 24 ops/word) and c8 residue scan
        (300,000 * 49408 candidates, <= 8 ops each)                                   103,578,699
    pre-construction analysis (Section 15.2): 5,457,189,249,047 ops / 2140             2,550,088,435
    process launch and library calls of the yield checks, V8 dump and c8 scan (H8):
        4.1e8 instructions * 1024 = 419,840,000,000 ops / 2140                        196,186,916
    Python runs (H8): at most 50 invocations * 5e8 instructions * 12 = 3e11 ops / 2140   140,186,916
    K run (Section 16, H2), primitive operations of the counted program:
      search: 12,436,504,580 passes of 8 trials * 4,677                   58,165,531,920,660 ops
      group head, set-up and abort checks: 5,932 groups * 13,505                  80,111,660 ops
      bitmap hits: 58,831,394 * 1,642                                          96,601,148,948 ops
      key-matched hits 1,376,281 * 13, matched records 3,061,666 * 238,
        V6 passes 5,992 * 2,344, the R20 pass to the stored pair 2,533,318          763,146,727 ops
      table build (2^32 scan, records, sort, bitmap), s1 inverse, self-check  236,418,844,446 ops
      library calls and main thread: at most 10^8 instructions * 1024         102,400,000,000 ops
      K with scalar trials (Section 16): 58,601,795,172,441 ops / 2140          (27,384,016,436, superseded)
      K with 7-lane SWAR trials, v1 (Section 17.4): 19,231,975,790,235 ops / 2140  (8,986,904,575, superseded)
      K with 7-lane SWAR trials, v2 (Section 17.7): 16,289,718,740,169 ops / 2140    7,612,018,103
    -------------------------------------------------------------------------------------------
    preprocessing (chain C)                                                   23,105,885,506 = 2^34.4275
    replay R                                                                 6.36
    total (rounded up)                                                        23,105,885,513 = 2^34.4275

Claimed time_log2 = 34.45 and preprocessing_log2 = 34.45 (Section 17.7 gives the margin). Every term is the work actually executed
by C or by the analysis that formulated R20. The event counts are the run's own counters (Section 8).
Nothing is an expectation or a cap that went unused.

The Python runs (H8) are bounded with measured data. The session transcript shows at most 50 python3
invocations in the windows of the pre-construction analysis and of chain C (Section 15.1), including
file edits. Re-runs on the same machine retire 213,502,045 instructions for `python3 -c pass` (the
interpreter's start-up), 229,782,531 for gen_s.py, 267,571,748 for check_s.py and 463,159,626 for
analyze.py, so each is charged as 5e8. Complete callgrind profiles of CPython (Debian python3.11 in the
container of Section 14.4) running gen_s.py, check_s.py and an empty script give per-form means of
5.15, 4.60 and 5.65 (unmapped instructions at 1024). The price 12 is twice the largest.

Process launch and library calls are charged from measurements on the same machine (Appendix C.15).
An empty program retires about 11e6 instructions from start to exit. Library calls retire about:
- 9,300 instructions for a progress `printf`, 950 for `fprintf("%08x")`, 1,100 for `fscanf("%x")`;
- 147,000 for `fopen` and `fclose`, 90,000 for `pthread_create` and `join`;
- 11,300 for `usleep`, 5,000 for `access`, 190 for `clock_gettime`;
- 25e6 for `calloc` of 256 MB (zero-fill).
Each run's launch and calls, doubled, are below its charge:
- K: 10^8 instructions;
- each synthetic check: 3e7;
- the analysis programs: 5e8;
- the yield checks 1.5e8, the V8 dump 1.3e8 (49,408 lines written) and the c8 scan 1.3e8 (49,408
  values read).
All are charged at 1024 per instruction, above every tariff of the table (Section 14.2).

K's block covers the whole K process:
- the set scans and the table (P1, P2), with the sort and the bitmap;
- the s1 inverse and the self-checks;
- every group, every trial, every bitmap hit, the completion and the output.
Code that is not part of the algorithm (library calls for printing, threads, timing and
allocation, and the main thread's progress loop) is bounded by instruction count at the highest
per-instruction price of the v5 table (Section 16.3). The program is that of our previous filing
(f99530e8, 36,391,233,206 units) with the rotations and Boolean functions written as the exact
identities of Section 16.1: 582 instead of 775 primitives per trial. The K term is 63.6% of the
total. The instruction-priced line (z3) is 22.9%.

The K run was not lucky. Model value: with 132096 records, a V6 rate of 2^-9 and an R20 rate of
2^-12.66, a first success is expected after about 2^36.6 trials. K needed 2^36.531.

## 10. Memory and advice

The advice of R is the stored 256-byte pair; 9 is claimed.

Peak memory is taken over every run that is charged: chain C and the pre-construction analysis
(Section 15.1). It is the maximum resident set size reported by `/usr/bin/time -l`:
- for the z3 attempts and search K, as recorded during the charged runs (Section 8);
- for every other run, from a re-run of the same binary or script on the same inputs on the same
  machine (2026-10-08; not charged, Section 15.1).
The last column gives the largest allocation in each run's source, so that the measured figures can
be checked against the code.

| run | maximum resident set (bytes) | largest allocation in the source |
|---|---|---|
| z3 attempt 1 / 2 / 3 | 154,107,904 / 161,103,872 / 153,944,064 | solver memory (z3 reports 95 MB peak for attempt 1) |
| search K (`r31det3`, 12 threads) | 7,438,336 | records: malloc of 2^20 * 24 bytes (24 MiB, 132,096 used); bitmap 2 MiB |
| synthetic checks (`r31sim3`, run 3's command) | 5,799,936 | the same records and bitmap |
| yield checks: `r31det3 1 0` / `diag 1 0` | 5,832,704 / 5,816,320 | the same records and bitmap |
| V8 dump / c8 scan | 1,720,320 / 1,916,928 | c8 scan: static array of 60,000 words |
| `sets` / `table` (excluded since v10, Section 15.4) | 1,703,936 / 1,720,320 | `table`: static key array of 2^24 * 4 bytes (64 MiB, sparsely touched) |
| `joint` | **538,050,560** | two calloc'd hash tables of 2^25 entries * 8 bytes = 2^29 bytes |
| `pany` | 269,549,568 | one table of 2^25 * 8 bytes = 2^28 bytes |
| `pany2` (1 thread; 12 threads) | 269,615,104; 269,631,488 | one table of 2^28 bytes, plus thread stacks |
| Python: gen_s.py / check_s.py / analyze.py | 18,202,624 / 17,465,344 / 24,625,152 | interpreter |

The peak is `joint`'s 538,050,560 bytes = 2^29.003. It is its two hash tables of 2^25 entries of
two 32-bit words each (2^29 bytes), plus code, stack and allocator state. We claim
memory_log2_bytes = 29.5 (759,250,125 bytes). That is 1.41 times the measured peak, and above the
sum of the largest allocations in any single source: `joint`'s 2^29 bytes plus at most a few MiB.
Our earlier filings claimed 27.5 from the chain's runs only and missed the analysis programs. The
measurement programs of Appendix C (`kcount.c`, `scount.c`, `pcount.c`, the profilers) are not
charged runs. Their largest allocation, `pcount`'s copy of `joint`'s two tables, is the same 2^29
bytes.
Memory is reported only and does not enter the score.

## 11. Heuristics

H1-public-characteristic (score-critical). The published 31-step signed characteristic (the cell
table of Section 5 and the differences d5..d18) is public algorithm text, and C may use it without
charging its original discovery.
- It is a set of conditions, not a collision. It contains no message words, chaining values or
  state values.
- C uses no published colliding pair, starting solution or first block. S comes from our own z3
  runs, and the stored pair from our own K run.
- Provenance: Li, Liu, Wang, Dong and Sun (ASIACRYPT 2024). The authors' public search tool is
  Peace9911/sha_2_attack at commit 6a9f35fd8d8bdcc1a54dc6f170ed0038ebe5bb32.
- Sensitivity: the trail search is not executed or bounded by our own evidence in this filing. A
  charge of T units for it gives a total of 42,877,883,846 + T units. That stays below 2^39.15 (our
  earlier filing) for T up to 2^39.044, and below 2^40.4 for T up to 2^40.356.

H2-counted-programs (score-critical). The work of search K, of the three synthetic completion
checks and of the pre-construction analysis programs is the operation count of explicit programs
that compute the same results with v5 primitives, not the retired instructions of their executables.
- Statement: K is charged by the counted program of Section 16 (worst-path count per event times
  the run's event counters, Section 8). The synthetic checks are charged by exact counted replays
  (Section 16.6) and the analysis programs by the exact counts of counted versions (Section 15.2).
- Scope: the counted programs `kprog.py`, `kcount.c`, `scount.c` and `pcount.c` (Appendix C.6-C.9,
  C.13). They use only v5 primitives on values in their own 256-bit words. They count every load and
  store, use no native 32-bit rotation, and write Σ, σ, Ch and Maj as exact identities (Section 16.1).
  Their 64-bit products are explicit 385-primitive shift-and-add emulations, inside the count.
- Evidence: K's program agrees with `r31det3`'s trial block on every key and bitmap decision of
  71,670,492 trials, with `process_hit` on every counter, and with `build_table`, and it reproduces
  the stored pair with the run's 2,829 E13 and 19 E15 draws (16.4). The synthetic replays agree
  trial by trial with `r31sim3`'s own `process_sim` and reproduce the logged FINAL counters of
  runs 2 and 3; run 1's stop at its first trial is reproduced by a re-run (16.6). Each counted
  analysis program prints exactly the original's output (15.2).
- Extrapolation: none beyond the premise. Worst paths are charged for K's events (18
  binary-search steps, all 64 G16 candidates).
- Sensitivity:
  - with the forms of our previous filing (775 per trial), the total would be 2^35.5937;
  - with every rotation and mask written as the organizer's reference core writes them (1035 per
    trial), 2^35.8960;
  - with twice every K line, 2^36.032;
  - with twice the synthetic checks, 2^35.3831;
  - with the analysis programs at the hand bounds of our earlier filings, which also covered the two
    excluded `table` runs, 2^35.6344;
  - with K charged by its executable's instructions instead (Section 14.6), 2^36.115 (one 256-bit
    word per vector register) or 2^36.860 (one word per 32-bit lane).

H3-heavy-tariffs (score-critical). Every multiply, divide and floating-point instruction is priced
by an explicit emulation in v5 primitives. The ordinary forms are priced by the per-form rules of
`a64ops.py` (Section 14.2).
- Statement: the tariffs are the largest primitive counts of checked emulations, rounded up to a
  multiple of 8:
  - multiplies with 32-bit source operands: 210 (`mul32.py`);
  - 64-bit `mul`/`madd`/`msub`/`mneg` 392, `umulh` 392, `smulh` 408;
  - `udiv`/`sdiv` 360/384 (32-bit) and 712/736 (64-bit);
  - binary64 add or subtract 240, multiply 520, fused multiply-add 600, divide 824, square root 1008,
    compare 48, integer-to-double conversion 152, double-to-integer 24 (`heavy.py`).
  The counted programs of H2 use the same floating-point tariffs.
- Scope: the per-form pricing of z3's executed instructions (Section 14.4) and the floating-point
  operations of the counted analysis programs (Section 15.2).
- Evidence: Appendix C.11. Each emulation is branch-free where possible, with every data-dependent
  branch counted. Each is checked against the instruction's definition: Python integers for the
  integer forms; the host's IEEE binary64 arithmetic on AArch64, and exact fractions for the fused
  multiply-add, for the floating-point forms. The checks cover 20,000 integer and 100,000
  floating-point cases per form, with zeros, subnormals, infinities, NaNs and extreme exponents. For
  every form the largest observed count is within its tariff.
- Extrapolation: the largest count on the checked inputs is taken as the form's worst case.
  Every loop in these emulations has a fixed trip count, and the data-dependent branches select
  among a few fixed paths, so the checked inputs exercise every path.
- Sensitivity: with every heavy tariff doubled, the total would be 2^35.524; with the v5
  table's uniform 400 for every multiply and floating-point form and 1024 for divides, 2^35.442.

H4-memory (supporting). Peak memory over C and the pre-construction analysis is at most 2^29.5 bytes.
- Scope: every charged run (Section 15.1): the z3 attempts, search K, the synthetic checks, the yield
  checks, the V8 dump and c8 scan, the analysis programs and the Python runs.
- Evidence: the maximum resident set sizes of Section 10 (`/usr/bin/time -l`), recorded during the
  charged runs for z3 and K and from re-runs of the same binaries on the same inputs for the rest.
  The largest is `joint`, 538,050,560 bytes, which its source explains: 2^29 bytes of hash tables.
- Extrapolation: a re-run touches the same pages as the original run of the same deterministic
  program on the same input.
- Sensitivity: memory does not enter the score.

H5-chain-scope (score-critical). Every constant of C comes from the public characteristic, from
analysis, from the charged pre-construction analysis programs, or from the charged v3 runs before K
(Section 15.3). The earlier search runs that used the published starting solution produced rates
and pairs that C does not read, and they fixed no constant of C (Section 15.4). They are excluded.
  So are the three `analyze.py` runs and the two `table` runs of the pre-construction analysis, which
  read the published pair or the starting solution derived from it (Section 15.4).
- Scope: all computation on this target in our working directories and session records on
  2026-10-06 and 2026-10-07, listed in Section 15.1.
- Evidence: the agent transcript of the session that ran every command, the file times of the
  working directories, the commitments of Appendix A, and the package commit history.
- Extrapolation: the commitments are local (file timestamps and a local git history), not
  notarised.
- Sensitivity: if a reviewer charged the excluded search runs anyway, the 2^40.625-trial run alone
  would put the total at 2^40.682.

H6-z3-build-transfer (score-critical). The per-form mix measured on the Linux build of z3 4.15.4
(PyPI z3-solver 4.15.4.0, the same solver version) bounds the per-form mean of the macOS binary
that ran (Homebrew z3 4.15.4).
- Statement: the z3 price of Section 14.4 is charged on the macOS instruction counts of Section 8.
- Scope: z3 attempts 1-3.
- Evidence:
  - every profiled run repeats the charged search: the same model, rlimit-count, conflicts and
    decisions;
  - both builds have the same static profile (Section 14.3), and both compile about 90% of their
    multiply sites to 32-bit-operand forms;
  - the macOS build retires more instructions for the same searches (attempt 1: 261,276,415,067 against 245,527,956,010; attempt 2: 1,572,256,055,396 against 1,475,640,959,576; attempt 3: 888,282,131,643 against 834,226,129,830), with the same
    multiplies and divides in the source.
- Extrapolation: from the static agreement and the equal search statistics to the dynamic mix. The
  price is not scaled for the instruction ratios, which favour the macOS build.
- Sensitivity: with the z3 price doubled, the total would be 2^35.592; at the price of our previous
  filing (19), 2^35.758; at 256 operations per instruction, 2^38.386.

H7-profile-reconstruction (score-critical). The per-instruction profiles of z3 attempts 2 and 3
are reconstructed from exp-bbv superblock counts.
- Statement: attempts 2 and 3 are priced from exp-bbv basic-block vectors (Section 14.4). callgrind's
  own memory grows without bound on these runs. Each superblock is disassembled from the executable
  that ran: its instructions run from its start to the first control transfer, or 100 instructions.
  The superblock's count is the number of instructions executed in it.
- Scope: attempts 2 and 3. Attempt 1 is priced from its complete callgrind profile.
- Evidence: on attempt 1 the reconstruction agrees with the complete callgrind profile:
  - whole-run per-form mean 7.5717 against 7.5558 at v5 prices, and 5.0436 against 5.0356 at this
    filing's prices;
  - largest interval 5.3589 against 5.3503.
- Extrapolation and bounds:
  - a superblock whose count is not a multiple of its length (5.01% of the instructions) is
    charged at the largest per-instruction mean of any prefix ending at one of its branches, an upper
    bound for any mix of exits;
  - the last partial interval, which exp-bbv does not report (1,867,089,404 instructions), is charged at
    1024 per instruction, more than any tariff of the table (Section 14.2).
- Sensitivity: with the bounded superblocks charged at twice their bound and the final intervals at
  4096 per instruction, the total would be 2^35.412.

H8-lumps-and-hand-bounds (score-critical). Process launch, library calls and the Python runs are
charged by measured bounds, and three small diagnostic programs by hand bounds from their source.
- Statement:
  - each process's launch and library calls: the measured per-call instruction counts of Appendix
    C.15, doubled, at 1024 per instruction (Section 9, 15.2, 16.3, 16.6);
  - the Python runs: at most 50 invocations of at most 5e8 instructions at 12 per instruction
    (Section 9);
  - the yield checks, the V8 dump and the c8 residue scan: the hand bounds of Section 9 (24 per
    scanned word, 64 per table candidate, 8 per residue candidate).
- Scope: these lines of Section 9 (3.5% of the total).
- Evidence:
  - `libmeasure.c` and its output (Appendix C.15): every library call kind the runs make, timed by
    the process's retired-instruction counter; an empty program's launch at 11.4e6 instructions;
  - the re-run instruction counts of the Python scripts, and complete callgrind profiles of CPython
    running them (Section 9);
  - the hand bounds hold for counted programs of the same loops:
    - K's table scan costs 55 per word for its three tests, against the yield bound of 72 (three
      scans at 24);
    - the V8 dump's single test costs 24 per word, as in K's scan;
    - the c8 scan's inner step costs 5 primitives (load, subtract, AND, compare, add), plus loop
      control of 3 per 8 candidates when unrolled by 8, against the bound of 8.
- Extrapolation: the library counts are measured per call kind, not inside the original runs. The
  CPython price is measured on the Linux build of a neighbouring version (3.11 against 3.12) and
  doubled.
- Sensitivity: with ten times every launch and library bound, and twice the Python bound and the
  hand bounds, the total would be 2^35.500.

## 12. Organizer-executed experiment and certificates

`experiments/r31-completion` runs a variant of K5 on the accepted match of the stored pair, with
each trial's E13/E15 draws taken from that trial's organizer nonce through SHAKE-256. The
organizer re-hashes every returned pair. Locally, the organizer intake ran it in the pinned Docker
image: status passed, 256/256 full collisions, 0 repeated pairs. It shows that completion works from our own S and match for fresh per-trial
nonces. It supports no probability inference, and the score does not depend on it.

Certificate: `relaxed-v3-1`, the stored pair.

## 13. Sources and credit

- Y. Li, F. Liu, G. Wang, X. Dong, S. Sun, "The First Practical Collision for 31-Step SHA-256",
  ASIACRYPT 2024: the framework and the signed characteristic.
- Y. Li, F. Liu, G. Wang, J. Shi, ePrint 2026/1080, Section 3: the framework restated.
- Y. Li, F. Liu, G. Wang, EUROCRYPT 2024 (ePrint 2024/349): the SAT/SMT approach.
- Public Yukon submissions on this track: using the published characteristic as public text, and
  sharing steps 0..14 across first blocks. Since our previous filing, K's charge counts the work
  done: steps 0..14 are charged once per group, in the group set-up (Section 16.3).
- Ours: R20, the starting-solution model with the yield residue, chain C and its execution, the
  experiment, the per-instruction price measurement of Section 14, the counted programs of K, the
  synthetic checks and the analysis (Sections 15.2 and 16), and the 32-bit multiply emulations
  (Appendix C.11).

## 14. Per-instruction price: our own evidence

This section supports H3 for the z3 runs. It measures what one retired instruction of z3 costs in
primitive word operations. Sections 14.5 and 14.6 price the synthetic check's and search K's
executables in the same way; those were the charges of earlier filings and are now cross-checks,
because both are charged by counted programs (Section 16). Apart from one re-run of K's table build
(Section 14.6) and one re-run of synthetic run 1 (Section 16.6), this section does not re-run any
charged call on the measurement machine. The complete profiles of 14.4 re-run the z3 attempts on the
Linux build in Docker; like every measurement here, they came after the stored pair existed and are
not charged.

### 14.1 What ran

- z3: the Homebrew bottle of z3 4.15.4 for arm64 macOS, `/opt/homebrew/Cellar/z3/4.15.4/bin/z3`
  (SHA-256 ae6c8df33db9c9ae9a80b6044e77cd66529a141d8b25f0620f1e89b409594f48). The executable
  contains the whole solver; it links only the system libc++ and libSystem.
- The synthetic completion check: `r31sim3.c` (Appendix B.6), compiled with Apple clang
  `cc -O3 -mcpu=apple-m4`.
- Machine: Apple M4 Pro. Instruction counts are the `instructions retired` lines of
  `/usr/bin/time -l` (Section 8).

### 14.2 Per-form costing

`a64ops.py` (Appendix C.1) prices every AArch64 instruction form under the v5 primitive list. Every
program datum sits in its own 256-bit word. The main rules:
- every add, subtract, negate and left shift is followed by one AND that reduces the result to 32
  or 64 bits;
- a shifted register operand costs one more shift (and a mask for a left shift); an extended
  operand costs 1 (zero-extend) or 3 (sign-extend);
- an address costs one addition per added term, plus one for a scaled or extended index and one
  for a write-back; a load or store pair pays two accesses and two addresses;
- loads of 8-, 16- and 32-bit fields cost one more mask, sign-extending loads three more;
- signed conditional branches cost 3 (sign flips before the comparison), other branches 1-3;
  conditional selects and compares 2-5; bit counts and byte reversals 32;
- SIMD logic costs 1, other SIMD forms 16;
- multiply, multiply-add, high multiply, and all floating-point arithmetic, comparison and
  conversion cost 400 ("heavy": shift-and-add emulation of a 64 x 64 or 53 x 53 product is at most
  64 iterations of 5 primitives plus normalisation);
- new in this filing (H3): every multiply, divide and floating-point form that the charged runs
  execute is priced by an explicit emulation in v5 primitives, checked against the instruction's
  definition (Appendix C.11). Each tariff is the emulation's largest primitive count, rounded up to
  a multiple of 8:
  - multiplies with 32-bit source operands (`umull`, `smull`, `umaddl`, `smaddl`, `umsubl`, `smsubl`,
    `umnegl`, `smnegl`, and `mul`, `madd`, `msub`, `mneg` on w registers): 210 (`mul32.py`; 32
    shift-and-add steps);
  - 64-bit `mul`/`madd`/`msub`/`mneg` 392, `umulh` 392, `smulh` 408;
  - `udiv`/`sdiv` 360/384 on w registers and 712/736 on x registers (restoring division);
  - binary64: `fadd`/`fsub` 240, `fmul`/`fnmul` 520, `fmadd`/`fmsub`/`fnmadd`/`fnmsub` 600, `fdiv`
    824, `fsqrt` 1008, `fcmp`/`fcmpe` 48, `ucvtf`/`scvtf` 152, `fcvtzs`/`fcvtzu` 24 (`heavy.py`).
  These replace the v5 table's uniform 400 and 1024 for these forms;
- integer divide, floating-point divide and square root cost 1024 (restoring division, 64
  iterations of at most 8 primitives, plus normalisation);
- any form the table does not recognise costs 8 and is reported.

### 14.3 Static costing of the binaries

| executable | instructions | ordinary forms, mean operations | heavy share | divide share |
|---|---|---|---|---|
| z3 that ran (macOS Homebrew 4.15.4) | 2,645,113 | 2.125 | 0.306% | 0.025% |
| z3 Linux build (PyPI z3-solver 4.15.4.0, aarch64; SHA-256 bbea82f9...86ab8b0) | 3,619,201 | 2.100 | 0.357% | 0.028% |
| r31sim3 that ran (macOS), `simworker` with the inlined trial | 571 | 2.321 | 2.10% | 0.18% |
| r31sim3 that ran (macOS), `complete` | 208 | 2.226 | 1.92% | 0 |

The two z3 builds have the same static profile; the build that ran has the lower heavy share.

### 14.4 Dynamic mix: complete profiles of the same solver on the same models

Valgrind does not run on macOS arm64, and we have no other instruction-level profiler there. So we
measured the mix on the Linux build of the same z3 version on the same machine, in Debian bookworm
arm64 under Docker with valgrind 3.19.0, on the three committed models with their committed seeds.
Each run went to completion, and every profiled run repeated the charged macOS search: the same
model, rlimit-count, conflicts and decisions. Every executed instruction is priced by its form with
the table of 14.2 (heavy forms by the tariffs of `mul32.py` and `heavy.py`). An instruction that
cannot be mapped to the disassembly is priced at 1024.

- **Attempt 1: callgrind.** This is the complete profile of our earlier filings, re-priced here:
  `valgrind --tool=callgrind --dump-instr=yes --dump-every-bb=8000000000`, with `cgfull.py`
  (Appendix C.12).
- **Attempts 2 and 3: exp-bbv.** On these long runs callgrind's own memory grows without bound
  (doubling to more than 4 GB, while the solver itself stays under 170 MB), so we recorded
  basic-block vectors instead:
  `valgrind --tool=exp-bbv --vex-guest-chase=no --vex-guest-max-insns=100 --interval-size=2000000000`.
  - **Reconstruction.** For every superblock, exp-bbv reports per interval the number of
    instructions executed in it. `bbvmix.py` (Appendix C.12) disassembles each superblock from the
    executable that ran: from its start to the first control transfer, or 100 instructions. When
    the count is a multiple of that length, it divides the count into entries and prices each
    instruction.
  - **Ambiguous superblocks.** A count that is not a multiple of the length means the superblock
    sometimes ran past a branch. It is charged at the largest per-instruction mean of any prefix
    ending at one of its branches, an upper bound for any mix of exits (5.01% of the
    instructions).
  - **Final interval.** exp-bbv does not report the last, partial interval; those instructions are
    charged at 1024 each (below).
  - **Intervals.** We report the counts in groups of 20 intervals (4e10 instructions), the size of
    callgrind's intervals.
  - **Check on attempt 1.** We ran exp-bbv on attempt 1 as well. Its reconstruction gives a
    whole-run mean of 5.0436 against callgrind's exact 5.0356 (7.5717 against 7.5558 at v5 prices),
    and a largest interval of 5.3589 against 5.3503.

| attempt | method | rlimit-count, conflicts, decisions (= macOS) | Linux instructions | macOS instructions (charged) | intervals | per-form mean, whole run | largest interval mean | at v5 prices: whole / largest |
|---|---|---|---|---|---|---|---|---|
| 1 | callgrind | 249,602,816; 1,068,222; 1,829,611 | 245,527,956,010 | 261,276,415,067 | 6 | 5.0356 | 5.3503 | 7.5558 / 8.1576 |
| 2 | exp-bbv | 1,200,096,786; 5,096,968; 8,121,313 | 1,475,640,959,576 | 1,572,256,055,396 | 37 | 5.2230 | 5.9655 | 7.9144 / 9.3134 |
| 3 | exp-bbv | 797,205,785; 2,818,639; 5,235,640 | 834,226,129,830 | 888,282,131,643 | 21 | 5.2745 | 5.7319 | 8.0114 / 8.8894 |

Multiplies and other heavy instructions are 1.32% of the executed instructions of attempt 1,
and 99.0% of them are 32-bit-operand multiplies (`umull`, `umaddl`, and `madd` on w
registers), mostly index and hash arithmetic. Floating point is 0.0085% of the instructions.

**Price.** The maximum is taken over the intervals of the complete profiles, and also over 23
callgrind intervals of the prefixes of attempts 2 and 3. These come from our v4 measurements (the first
361e9 and 309e9 instructions) and from this filing's interrupted callgrind run of attempt 2 (its first
248e9). They cover the same instructions with other interval boundaries. The largest of all is 6.0054
(attempt 2, callgrind prefix of this filing's interrupted run, interval 4; the largest complete-profile interval is 5.9655). So
m_z3 = ceil(6.0054) = **7**, charged on the macOS instruction counts. The final partial intervals of attempts 2 and 3
(1,867,089,404 Linux instructions) are charged at 1024 per instruction instead, scaled by the macOS to
Linux instruction ratio where that ratio exceeds 1:

    z3 = 7 * 2,721,814,602,106 + (1024 - 7) * 1,989,181,169 = 21,075,699,463,615 ops = 9,848,457,694 units

The integer ceiling over the largest interval is kept as a reserve. With the largest interval mean
itself the total would be 2^35.277; with each attempt at its own whole-run mean, 2^35.242.

**Build difference.** The macOS build retires more instructions for the same search (attempt 1: 261,276,415,067 against 245,527,956,010; attempt 2: 1,572,256,055,396 against 1,475,640,959,576; attempt 3: 888,282,131,643 against 834,226,129,830). The
multiplies and divides are the same source operations in both builds, and both compile about 90% of
their multiply sites to 32-bit-operand forms (static multiply instructions: macOS 6,072 of 6,837,
Linux 10,405 of 11,543). With more instructions and the same heavy operations, the macOS per-form
mean is at most the Linux one (H6).

### 14.5 The synthetic completion check (cross-check)

In this filing the synthetic checks are charged by their exact counted replays (Section 16.6). The
measurement below priced them in our earlier filings (at 13 per instruction on three runs of
500,284,109,323 instructions; Section 16.6 corrects that run count) and is kept as a cross-check.


The same procedure on `r31sim3.c` compiled with gcc 12 -O3 in the container, with collection
switched on after the table build (`--instr-atstart=no`, then `callgrind_control -i on` when the
kernel check is printed), for 60 s of the trial loop:
- Linux build, 52,111,782,338 instructions over 39,059,456 trials (1334 per trial): heavy share 0.654%, divide share 0.0720%, ordinary mean 3.06, per-form mean 6.39, class price 8.32.

The heavy instructions of a trial are fixed by the source: four splitmix64 draws (two 64-bit
multiplies each), one 64-bit remainder (a divide and a multiply-subtract), and in `complete` one draw
per E13 or E15 iteration. Both compilers emit one AArch64 instruction for each. The macOS build
retires 1499 instructions per trial (Section 8: 500,284,109,323 instructions, of which
the table build takes at most 124,752,621,861, over 250,544,128 trials), against 1334 in
the Linux build. With the same heavy instructions per trial, the macOS heavy share is the lower one,
so we keep the Linux shares (scale factor max(1, 1334/1499) = 1.000) and take
m_sim = ceil(2 * per-form mean) = ceil(2 * 6.3887) = **13** (the class price 8.32 gave 17 in 50592e75), charged on all instructions of each run, including the table
build.

### 14.6 Search K: the executable that ran, priced by its executed path (cross-check)

This subsection was the K charge of filing e0259cf5 (58,909,096,251 units, total 2^36.6392).
In this filing it is a cross-check only, and the K charge is the counted program of Section 16
(27,384,016,436 units). Below, "K charge" means the charge of filing e0259cf5. It prices K's
retired instructions (Section 8: 15,640,902,198,904) at prices measured on the executable that ran.

- **Executable.** `r31det3`, built from B.4 and B.5 with Apple clang,
  `cc -O3 -mcpu=apple-m4 -o r31det3 r31det3.c -lpthread`, at 13:04 KST, before K started at
  13:04:56, and not rebuilt since. SHA-256 2824a0f855c203d1ada6f99e5a25fa8aebd4f2feeee0a8a56776c311af4bce23.
  Disassembly: `xcrun llvm-objdump -d --no-show-raw-insn r31det3`.
- **Vectorised kernel.** clang compiled the 8-lane trial block of `worker` (the `j < LANES` loops of
  B.4) into NEON code: a 524-instruction block that handles 4 lanes, run twice per 8 trials. Its
  forms are 4-lane add, shift left, shift right and accumulate, three-way XOR and bit select. The
  v5 table of 14.2 charges every SIMD form other than logic at a flat 16 ("charged as shuffles").
  Under that table the hot path costs 11.13 operations per instruction, and doubled, 23: above the
  13.84 at which the measured count would equal the operation model of filing 33599d41. We
  price these forms by their exact emulation instead (below).

**Executed path.** With no bitmap hit, one pass over 8 trials executes a fixed instruction sequence
(`kpath.py`, Appendix C.5):

| block of `worker` | instructions | executions per pass |
|---|---|---|
| 0x100002b14-0x100002b60 pass set-up | 20 | 1 |
| 0x100002b64-0x100003390 NEON block, 4 lanes | 524 | 2 |
| 0x100003394-0x1000033a4 | 5 | 1 |
| 0x10000348c-0x1000034a8 bitmap test, per lane | 8 | 8 |
| 0x100003460-0x100003488 lane loop, per lane | 11 | 8 |
| 0x100002ae0-0x100002b10 trial counter, stop check, next pass | 13 | 1 |
| total per pass | 1238 | |

K executed 99,492,036,640 trials, so 12,436,504,580 passes and 15,396,392,670,040 instructions on this
path: 98.44% of the 15,640,902,198,904 retired. The path has no multiply, divide or
floating-point instruction. The remaining 244,509,528,864 instructions (1.56%) are:
- the table build and self-checks before the search: 124,755,608,685 instructions when the same
  executable runs `r31det3 1 0` (re-measured with `/usr/bin/time -l` on 2026-10-08; not charged,
  Section 15.1). Its common path is 29 scalar instructions per scanned word (0x1000009dc-0x100000a64
  of `main`), and 2^32 * 29 = 124,554,051,584 is 99.84% of that count;
- 119,753,920,179 instructions of bitmap-hit processing (58,831,394 hits, about 2,036 instructions
  each: a 31-step compression, a binary search over 132,096 records, the record loop), group
  set-up, the one completion and the main thread.

**Prices for the SIMD forms.** As in 14.2, a 128-bit vector register is one datum in one 256-bit
word; this is why SIMD logic costs 1 there. A lane-wise form is then computed on that word with lane
masks (SWAR), using v5 primitives only. L is the mask of all bits of each lane except its top bit, H
the mask of the top bits, M the lane mask for the shift, R the low 128 bits.

| form | emulation on one 256-bit word | operations | price |
|---|---|---|---|
| `add.4s`, `add.2d` | ((x & L) + (y & L)) ^ ((x ^ y) & H) | 6 | 6 |
| `shl.4s #k` | (x << k) & M | 2 | 2 |
| `ushr.4s #k` | (x >> k) & M | 2 | 2 |
| `usra.4s #k` | d + ((x >> k) & M), lane add as above | 8 | 8 |
| `eor3.16b` | x ^ y ^ z | 2 | 2 |
| `bcax.16b` | x ^ (y & ~z) | 3 | 3 |
| `bsl.16b` | ((n ^ m) & d) ^ m | 3 | 3 |
| `bic.16b` | x & ~y | 2 | 2 |
| `dup.4s` / `dup.2d` from a general register | w, (w << 32) & R, ... joined by OR | 9 / 3 | 11 |
| lane insert / extract (`mov.s`, `ins`, `umov`) | (v & ~lane) or ((w << 32i) & R); (v >> 32i) & 0xffffffff | 4 / 2 | 4 |
| `and`, `orr`, `eor`, `mov`, `movi` | as in 14.2 | 1 | 1 |

Other SIMD forms keep the v5 price of 16 (in this binary: `uzp1`, `ext`, `cmeq`), and scalar forms
are unchanged (`swar.py`, Appendix C.3). The lane add needs no final mask: (x & L) + (y & L) cannot
carry out of a lane. `swar_check.py` (Appendix C.4) runs each emulation with counted primitives and
compares it with the lane-wise definition on 2000 random inputs per form. Every form matches, at no
more than the listed price:

```
add.4s         emulation ops  6  priced  6  ok
add.2d         emulation ops  6  priced  6  ok
shl.4s         emulation ops  2  priced  2  ok
ushr.4s        emulation ops  2  priced  2  ok
usra.4s        emulation ops  8  priced  8  ok
eor3.16b       emulation ops  2  priced  2  ok
bcax.16b       emulation ops  3  priced  3  ok
bsl.16b        emulation ops  3  priced  3  ok
bic.16b        emulation ops  2  priced  2  ok
dup.4s         emulation ops  9  priced 11  ok
dup.2d         emulation ops  3  priced 11  ok
mov.s(extract) emulation ops  2  priced  4  ok
mov.s(insert)  emulation ops  4  priced  4  ok
```

**Prices of the K run.**

| part | instructions | per-form mean | price |
|---|---|---|---|
| search hot path | 15,396,392,670,040 | 3.9031 (11.1300 under the v5 table) | ceil(2 * 3.9031) = **8** |
| remainder | 244,509,528,864 | ordinary instructions: 2.8621 on the table-scan path (exact), 2.1796 over the hit-processing code and 2.7860 over the group set-up code (static) | **10** |
| heavy instructions off the hot path | 1,121,255,712 multiplies | | **400** each, in addition |
| main thread and library floating point | at most 710,000 | | **1024** each, in addition |

The factor 2 is kept although the path is costed on the executable that ran. The remainder price
10 is above twice every ordinary-instruction mean of its code. The heavy instructions are charged
again in full. The executable has 94 (`kpath.py` lists their addresses): 82 multiplies and 12
floating-point instructions, the latter all in `main`. The multiplies off the hot path, counted from
the source and the run's counters:
- group set-up: 33 per group (its code has 32: 15 splitmix64 draws of two multiplies and the two
  seed products; we count one more), times 5,932 groups, plus one per thread at start: 195,768;
- bitmap hits: at most 18 binary-search steps over 132,096 records, one 24-byte index product
  each, plus one for the lookup: 19 * 58,831,394 = 1,117,796,486;
- record loop: one per matched record, 3,061,666; completion draws: 2 * (2,829 + 19) = 5,696;
- table build: one per stored record, 132,096; self-check: 2000 blocks * 16 draws * 2 = 64,000.
The main thread after the table build runs its once-per-second loop (at most 200 passes of 31
instructions, with the 12 floating-point instructions), the summaries over the 12 thread counters
(with the remaining multiply) and seven progress lines through `printf` and `log2` (at most 10^5
library instructions each). We charge all of it, at most 710,000 instructions, at 1024 each.

K charge: ceil(15,396,392,670,040 * 8 / 2140) + ceil(244,509,528,864 * 10 / 2140) +
ceil((1,121,255,712 * 400 + 710,000 * 1024) / 2140) = 57,556,608,113 + 1,142,567,892 +
209,920,246 = **58,909,096,251** units. The operation model of filing 33599d41 charged 101,185,639,958;
the break-even price of the measured count is 13.84 operations per instruction.

**Cross-check on a Linux build (callgrind).** The gcc 12.2 `-O3` build of the same source in the
Debian bookworm arm64 container of 14.4, valgrind 3.19.0 callgrind with `--dump-instr=yes`, ran
`r31det3 1 100000 dfafc947679ebe06`: the committed seed on one thread, so groups 0, 1, 2, ... in
order. It was dumped after the table build and at exit after 27 groups (451,936,264 trials, 267,333
bitmap hits, 13,844 records, 18 V6 passes); `cgmix.py` (C.2) priced the dumps:
- table build: 134,520,943,302 instructions, per-form mean 2.8224 (v5 table), 2.7704 (SWAR prices);
- search: 86,680,445,856 instructions, 191.8 per trial (the macOS executable: 157.2 per trial over
  the whole run, 154.75 on the hot path); per-form mean 8.0863 under the v5 table, 2.2488 under the
  SWAR prices.
gcc also vectorises the kernel; it writes rotations as shift, shift and OR, so its mix differs from
clang's. Under the v5 table this build alone would price K at ceil(2 * 8.0863) = 17, also above the
break-even. A clang build with the macOS instruction set cannot run under valgrind 3.19, which
rejects `eor3`; this is why the price rests on the executable that ran rather than on a profile.

**Sensitivity of the charge of filing e0259cf5** (its total 107,027,591,592 = 2^36.6392):
- v5 table with its flat SIMD price 16 (K hot path 11.13, so 23 for all of K): 2^37.654;
- every K instruction at 16, heavy instructions as above: 2^37.266;
- twice the charged K prices (16 and 20): 2^37.270;
- without the factor 2 (4 on the hot path, 3 on the remainder): 2^36.173;
- each 32-bit lane in its own word (hot-path mean 7.32, price 15): 2^37.196;
- the operation model of filing 33599d41: 2^37.1195.

### 14.7 What this does not establish

- The dynamic profiles are of the Linux build (H6). The equal search statistics of every attempt
  and the equal static profiles support the transfer; they do not prove an identical instruction
  mix. Attempts 2 and 3 are reconstructed from basic-block vectors (H7), checked against callgrind
  on attempt 1.
- The price is an operation count under our per-form table. A reviewer who prices some form higher
  can recompute the means from the published scripts. With every multiply at the v5 table's 400,
  the total would be 2^35.442; at twice the price, 2^35.592.
- K is not charged by this section. Its executable-priced charge (14.6) needs the premise that a
  128-bit register is one 256-bit word. With each 32-bit lane in its own word instead (`add.4s` 8,
  `usra.4s` 12, `eor3.16b` 8, a 128-bit load 4 loads), the hot-path mean would be 7.32, the doubled
  price 15, and the total 2^37.196. The counted program of Section 16 does not need that premise:
  each 32-bit value is in its own word, and it costs 584.6 operations per trial against 1133 for the
  executable's instructions under that reading.
- The measurement runs of this section, like the post-K re-runs of Section 8, came after the stored
  pair existed and fixed nothing in C. They are not charged.

## 15. Development record and the origin of every constant of C

### 15.1 Every computation on this target (2026-10-06 to 2026-10-08, KST)

The record is the agent transcript of the session that ran every command, cross-checked with
the file times of the working directories and the package commit history (commits a7d3eaa 11:37,
e13dab2 12:17, 61428b0 13:14).

| time | computation | status in v4 |
|---|---|---|
| 10-06 | three exploratory solver studies of other methods (a cut model, a meet-in-the-middle verifier model, a z-elimination model) | excluded: no output or constant used by C |
| 09:43-09:59 | pre-construction analysis: `sets` (1), `joint` (1), `pany` (1). They formulated R20 and estimated its rate (`joint`, 09:48) | **charged**, Section 15.2 |
| 09:43-09:59 | `analyze.py` (3 runs) on the published 31-step pair: digest, characteristic and per-row checks, the modular differences, the published tuple; `table` (2 runs), which counts the table records of the starting solution derived from that pair | excluded (published pair and S), Section 15.4; charged up to v9 |
| 10:36-10:37 | `r31s` self-tests (3) and a 12 s test | excluded (published S) |
| 10:37-11:22 | relaxed search with the published S, 2^40.625 trials | excluded (published S), Section 15.4 |
| 10:44-11:35 | synthetic completion, independence and cluster runs with the published S (`r31sim`, `r31log`, `r31log2`, `r31clus`, `r31log3`); `pany2` (2 runs: 2^20 samples at 10:47, 2^28 samples at about 11:24) | `pany2` **charged** (15.2); the others excluded |
| 11:55-12:12 | K' runs with the published S (filing 3183e839, refuted) | excluded (published S) |
| 12:52-13:04 | chain C before K: z3 attempts 1-3, gen_s/check_s, yield checks (5), synthetic checks (3), V8 dump, c8 scan, inline Python on S and V8 | **charged**, Section 9 |
| 13:04-13:07 | search K | **charged**, Section 9 |
| 13:08-13:09 | instruction-count re-runs: `diag` (2), `r31sim3` (2), `v8dump`, `c8scan` | not charged: after the pair existed |
| 15:39-16:10 | v4 price measurements (Section 14) | not charged: after the pair existed |
| 10-08 03:59-04:10 | v6 K price measurements: `r31det3 1 0` on macOS, gcc build under callgrind (Section 14.6) | not charged: after the pair existed |
| 10-08 09:05-09:30 | v7 counted program of K: `kprog.py` (2 runs) and `kcount` (validation, Section 16.4) | not charged: after the pair existed |
| 10-08 13:30-13:40 | v9 memory measurements: `/usr/bin/time -l` re-runs of `joint`, `pany`, `pany2`, `sets`, `table`, `r31det3 1 0`, `diag 1 0`, `r31sim3`, `v8dump`, `c8scan`, gen_s.py, check_s.py and analyze.py (Section 10) | not charged: after the pair existed |
| 10-08 10:03-12:59 | v8 measurements: exp-bbv profiles of z3 attempts 1-3 (Docker; callgrind runs of attempts 2 and 3 stopped by memory); `kprog.py` (3 runs) and `kcount`; counted analysis programs `pcount` (6 runs) and re-runs of `sets`, `table`, `joint`, `pany`, `pany2 1 20` for the output comparison (15.2); counted synthetic replays `scount` (3 runs) and one re-run of synthetic run 1 (16.6) | not charged: after the pair existed |

"Published S" means the runs used the published starting solution: S was derived from the published
collision in that work, so C cannot and does not use any of its outputs.

### 15.2 Charged pre-construction analysis (exact operation counts)

These programs read only the characteristic and SHA-256 constants. They ran exactly the times listed in
15.1; their source is in Appendix C.10, which also lists `table`, an excluded run since this filing.
Our previous filings charged them by hand bounds from the source (27,838,136,107,008 operations).
This filing counts them exactly. `pcount.c` (Appendix C.9) writes each program in the counted
primitives of Section 16.1, runs it on the same inputs (and, for `pany2`, the same thread count and
per-thread streams), and prints the program's own output lines. Every output is identical to the
original's. We re-ran `sets`, `joint`, `pany` and `pany2 1 20` (and the excluded `table`) for the comparison; the
2^28-sample `pany2` run is compared with its saved output. Floating-point operations are charged at
the tariffs of their checked emulations (Section 14.2, H3): conversion 152, addition 240,
multiplication 520, comparison 48, division 824, square root 1008.

| program | runs (Section 15.1) | counted operations |
|---|---|---|
| `sets` | 1 | 461,151,205,710 |
| `joint` | 1 | 644,688,249,115 |
| `pany` | 1 | 569,745,544,349 |
| `pany2 1 20` (2^20 samples) | 1 | 410,842,675,669 |
| `pany2 12 28` (12 threads, 268,435,452 samples) | 1 | 2,858,761,574,204 |
| process launch and library calls of the 5 runs (measured, H8; the bound set for 7 runs is kept): at most 5e8 instructions at 1024 | | 512,000,000,000 |
| total | | 5,457,189,249,047 |

The counted programs differ from the originals only in how they reach the same values:
- rotations, Σ, σ, Ch and Maj as in Section 16.1;
- the hash index k * 2654435761 >> 7 as shift-and-add over the 19 set bits of the constant;
- `pany` and `pany2` add the integer counts returned by the hash lookups in an integer register and
  convert the sum once. The originals add the converted counts (`pany`: count / 2^32) in double
  precision. Every partial sum is an integer multiple of the same power of two, below 2^53 of it,
  so every addition is exact and the result is bit-identical. The printed means, standard errors and
  bounds confirm it.

The excluded `table` runs (2 * 158,924,192,620 = 317,848,385,240 operations, 148,527,283 units) are no
longer charged. The Python lump of Section 9 keeps its bound of 50 invocations, although the three
`analyze.py` runs are now excluded.

### 15.3 Constants of C and where they come from

| constant | value | origin |
|---|---|---|
| characteristic cells and d5..d18 | Section 5 | public text (H1) |
| R20 | Section 6 | analysis of the schedule equation for W20; formulated and rated by `joint` and `pany` (charged) before any search ran |
| C6, C7, C8, the V9 target, G16 condition | Section 6 | the cancellation equations for W18 and W21..W24, from the characteristic |
| V6, V7, V8, V9, G16 | sets | recomputed exhaustively by K's P1 (charged) |
| S model constraints (a)-(e) | Section 7.1 | the characteristic and the step equations |
| constraint (f) | Section 7.1 | analysis of attempt 1's empty table (attempt 1 charged) |
| constraint (g), residue e730f mod 2^20 | Section 7.1 | V8 dump and c8 scan of v3 (charged) |
| z3 seeds 88108363..65, K seed | Appendix A | hashes of committed strings |
| table and bitmap layout (2^24-bit bitmap on A[-1] >> 8, records sorted by key) | Section 7.2 | design choice, no measured input |
| group structure (2^24 trials share words 0..14) | Section 7.3 | public design (credited); steps 0..14 are charged once per group |
| E13/E15 draw caps 2^22 and 2^12, 12 threads, wall cap 1200 s | Section 7.3 | not binding: K used 2,829 and 19 draws and 140 s |

### 15.4 Why the excluded runs fixed nothing in C

- Outputs. The excluded runs produced rates and pairs from the published starting solution. C reads
  none of their files; its inputs are the characteristic, the committed seeds, and the outputs of its
  own charged steps (Appendix A records the hashes of every input).
- Caps. K's stored pair is the same for every E13 cap of at least 2,829, every E15 cap of at least
  19, any thread count, and any wall cap of at least 140 s; removing the caps altogether gives the
  same pair. So no cap value influences C, whatever motivated it.
- Rates. The measured rates of the excluded runs appear only in the "not lucky" remark of Section 9,
  which no bound uses.
- R20 itself predates every search: `joint` evaluated the union bound of the relaxed condition at
  09:48, and the first relaxed search started at 10:37.
- `analyze.py` and `table`. `analyze.py` read the published 31-step pair and printed its digests, the
  check of the characteristic on it, the per-row cell counts, the modular differences of W, A and E,
  checks of the step formulas for E0..E2, W0..W6 and W13, and the pair's tuple A-1..A4, E5..E8.
  `table` embedded that tuple and printed, for this starting solution, the sizes of V7 and V8, the
  (W8, E4) survivors, the table tuples, and whether the published record appears. C takes no value
  from these lines:
  - the cell counts and the modular differences of Section 5 are functions of the signed table
    itself (each `u` adds 2^bit and each `n` subtracts it; for example the W5 row gives fffff006);
  - the step formulas follow from the step equations of Section 2;
  - V6..V9 and G16 come from `sets` and are recomputed exhaustively by K's P1;
  - R20 was formulated and rated by `joint` and `pany`, which read only the characteristic;
  - the table and bitmap layout is a design choice, and K's record buffer (2^20 records) is not binding:
    K built its own table of 132,096 records from its own S;
  - `check_s.py` (B.2, part of C) contains one published value, A1 = f36e6fcf, only to print whether
    our S differs from the published starting solution. It does, and no value of C depends on the
    comparison.
  Charging the five runs anyway would add the 148,527,283 units of `table` (the `analyze.py` runs are
  within the Python lump) and give the v9 total of 2^35.3245.
- Sensitivity: charging the 2^40.625-trial run anyway would add 2^40.625 * (1 + 32/2140) units and put
  the total at 2^40.682.

## 16. Search K and the synthetic checks as counted word-RAM programs (H2)

This section supports the K line of Section 9, and 16.6 the synthetic-check line. K is charged as the
operation count of an explicit program for the cost model's own machine. The program computes what `r31det3` (B.4) computes,
trial by trial and event by event, and it is checked against `r31det3` itself (16.4). The charge
multiplies each event's worst-path count by the run's own counter of that event (Section 8).
Nothing is priced per CPU instruction, except code outside the algorithm (16.3, last row).

### 16.1 Machine and conventions

- Primitives of collision-frontier-v5, 1 each: 256-bit load or store, addition or subtraction mod
  2^256, AND, OR, XOR, NOT, shift, comparison, conditional branch. Every 32- or 64-bit value of the
  program sits in its own 256-bit word.
- Registers and memory. ALU operands are registers, and the only immediates are shift counts. Every
  other operand is loaded from memory, and each load is counted. This covers round constants, group
  values, record fields, schedule words, table entries and bitmap words. Every store is counted as
  well.
  - Four registers hold 2^32-1, the bitmap base, 63 and 1 for the whole run.
  - The straight-line code of one trial needs at most 22 registers at once. `kprog.py` computes
    the largest live set.
  - With the loop variables, the program fits a 32-register machine.
- Masks. A value is reduced to 32 bits (AND with 2^32-1) before it enters a right shift or a
  comparison, or is stored as a 32-bit word. Addition, AND, OR, XOR, NOT and left shifts never move
  bits from above position 31 into positions 0..31. So the low 32 bits of every value equal the
  word that the C source computes.
- Rotations. There is no native 32-bit rotate. For a reduced word v, dup(v) = v | (v << 32) holds
  two copies of v, so bits 0..31 of dup(v) >> n are ROTR(v, n) for 0 < n < 32. One dup serves the
  three rotations of a Σ or σ, and the next mask removes the bits above 31:
  - Σ0, Σ1 = (d >> n1) ^ (d >> n2) ^ (d >> n3) with d = dup(v): 7 primitives each;
  - σ0, σ1 = (d >> n1) ^ (d >> n2) ^ (v >> n3): 7 each, 5 when d is already at hand.
- Boolean functions, as exact identities:
  - Ch(e,f,g) = g ^ (e & (f ^ g)): 3 primitives;
  - Maj(a,b,c) = b ^ ((a ^ b) & (b ^ c)): in step t, b ^ c is the a ^ b of step t-1, so Maj costs
    3 (and 4 as (a & b) | (c & (a | b)) where no previous value is at hand).
- 64-bit products (splitmix64 draws, group seeds) are emulated by branch-free shift-and-add:
  acc += (a << i) & -((b >> i) & 1) for i = 0..63, then a mask. That is 385 primitives per product.
- Loops with a fixed trip count are straight-line code and pay nothing for control. Loops with a
  data-dependent trip count pay their counter, comparison and branch.
- Groups. Every subexpression that depends only on words 0..14 of a group is computed once, in the
  group set-up, and charged there. This is K's own structure (Section 7.3, K1): the trial block of
  `worker` reads the group's state after step 14 and its schedule constants m16, m18, m20 and
  c17..c30.

Our previous filing (f99530e8) used the same machine with rotations written as
(v >> n) | (v << (32 - n)) and the Boolean functions in the forms of the organizer's
`verifier/hash_functions.py`; that program cost 775 per trial and is kept as a checked variant
(16.5).

### 16.2 One trial: 582 primitives

`kprog.py` (Appendix C.6) generates the trial as straight-line code, from x = word 15 to the bitmap
test, and emits it as C (`klane_opt.h`). Steps 15..30 cost 451, the twelve schedule words that
depend on x cost 122 (with one dup of x shared by σ1 in w17 and σ0 in w30), and the bitmap test
costs 9:
- shift right by 8 and by 6;
- add the bitmap base;
- load the 64-bit bitmap word;
- AND 63, variable shift, AND 1;
- compare;
- branch.
The breakdown by primitive is:

| add | AND | OR | XOR | shift left | shift right | load | compare | branch | total |
|---|---|---|---|---|---|---|---|---|---|
| 117 | 73 | 41 | 143 | 41 | 129 | 36 | 1 | 1 | 582 |

There is no branch inside the trial other than the bitmap test, so 582 is the count of every trial.
Step 15 costs 6: every term except x is a group value, so E15 = (U15 + x) & (2^32-1) and
A15 = (V15 + x) & (2^32-1). Steps 16..18 read the group's state words with one load each; the group
set-up also stores a ^ b and e ^ f for their Maj and Ch. From step 19 on, all eight state words are
per-trial values. The round constant and the schedule word are added separately, except at steps
29 and 30, where the group constant includes the round constant (and IV[0] at step 30, so that the
step-30 sum is the key IV[0] + A30). E30 is not computed, because the key does not need it.

A pass of 8 trials costs 8 * 582 + 21 = 4,677. The 21 cover:
- eight increments of x;
- the trial counter: two loads, an add and a store;
- the test base & 0xfffff = 0: a load, an AND, a comparison and a branch;
- the pass loop: an add, two loads, a comparison and a branch.
`kcount.c` (Appendix C.7) executes the pass and measures 4,677 for every pass.

### 16.3 Every event of the K run

| event | count in the run (Section 8) | primitives per event, worst path | ops |
|---|---|---|---|
| pass of 8 trials | 12,436,504,580 | 4,677 | 58,165,531,920,660 |
| group: loop head 12, set-up 13,349, 16 abort checks of 9 | 5,932 | 13,505 | 80,111,660 |
| bitmap hit: copy of the block, compress31 (counted), binary search of 18 steps, key test | 58,831,394 | 1,642 | 96,601,148,948 |
| key-matched hit: counter, final loop test | 1,376,281 | 13 | 17,891,653 |
| matched record: loop test, E0..E2, W0..W6, stores, V6 test | 3,061,666 | 238 | 728,676,508 |
| V6 pass: W5 target, c18, all 64 G16 candidates | 5,992 | 2,344 | 14,045,248 |
| R20 pass to the stored pair: completion (2,829 E13 and 19 E15 draws), two digests (6 compressions, counted), comparisons, output | 1 | 2,533,318 | 2,533,318 |
| table P1: 2^32 words, 55 each, plus stores | 1 | | 236,223,301,254 |
| table P2 (49,408 W8 and their W7 loops), merge sort of 132,096 records, bitmap | 1 | | 164,304,912 |
| s1 inverse and its 1000-value check | 1 | | 608,280 |
| self-check, 2000 blocks | 1 | | 30,630,000 |
| library calls and the main thread (below) | | | 102,400,000,000 |
| K | | | 58,601,795,172,441 |

K = ceil(58,601,795,172,441 / 2140) = **27,384,016,436** units.

Notes on the table:
- Worst paths. The binary search over n = 132,096 records takes at most floor(log2 n) + 1 = 18
  steps of 12 primitives each, the same on either branch, and the charge assumes 18. The V6 pass is
  charged as if all 64 G16 candidates were tried (36 each). The trial count is the run's trial
  counter divided by 8. Each group is charged 16 abort checks, although the 4 aborted groups ran
  fewer.
- Deterministic parts. The table build, the s1 inverse, the self-check and the R20 pass read only
  fixed inputs: S, the committed seed and the stored trial. Their counts are those of the counted
  program executing on the same inputs, so they are the counts of the path that ran. The R20 pass
  draws the same 2,829 E13 and 19 E15 values as the run.
- Sort. `r31det3` sorts with the C library's `qsort`. The counted program sorts with a bottom-up
  merge sort (81,135,912 primitives) and produces the same key order.
- Multiplies. The counted program has no multiply other than the emulated 64-bit products. Index
  products (record address 6r, as (r << 2) + (r << 1)) are shifts and adds.
- Outside the algorithm. Process launch and library calls are not part of the algorithm, but they
  ran, so they are charged:
  - formatted output (progress lines, the stored pair, the index line, the table and self-check
    messages) and log2;
  - fopen, malloc and calloc;
  - pthread create, join and mutex;
  - sleep, clock_gettime and access;
  - argument parsing.
  The main thread also runs its once-per-second loop (at most 140 passes in a 140 s run). Measured on
  the same machine (Appendix C.15), launch is about 11.4e6 instructions, and the calls of this run
  total less than 4.2e6. Twice their sum is below the 10^8 instructions we charge at 1024 each, more
  than any tariff of the table (Section 14.2; H8).

### 16.4 Validation against the executable's source

`kprog.py`:
- for 20,000 random choices of words 0..14 and x, the key of the generated trial equals word 0 of
  the organizer reference core's 31-step compression (`verifier/hash_functions.py`, `_compress`),
  in each of the three variants (582, 775 and 1035 primitives);
- every trial executes exactly the variant's count;
- on 2000 of them, setting the tested bitmap bit turns the decision from miss to hit.

`kcount.c` includes `r31det3.c` (B.4) and `sp_own.h` (B.5) unchanged and uses the committed seed
dfafc947679ebe06. It checks the following.
- Table: V7, V8 and G16 equal those of `build_table`. The 132,096 records are the same multiset in
  the same key order, and the 2^24-bit bitmap is identical. The s1-inverse columns are identical,
  and all 2000 self-check blocks agree.
- Trials. Groups 0, 1, 2 and 3 run in full, and group 5920 runs up to its stored pair: 71,670,492
  trials in all. For every trial, the counted trial's key equals the key of `worker`'s trial block,
  copied verbatim into `ref_key`. The bitmap decisions are identical. Every trial costs 582, and
  every pass 4,677. Every 1024th trial is also run in the 775 and 1035 variants, with the same key.
- Hits. Each of the 42,583 bitmap hits is processed twice: by `r31det3`'s own `process_hit`, and by
  the counted hit processing on the same record order. In every group they agree on every counter.
- Stored pair. In group 5920 the counted program stops at n = 99,325,680,347 with the stored pair
  of Section 4. It makes 2,829 E13 and 19 E15 draws, as the run did.
- Worst paths. The observed maxima are the worst paths charged in 16.3. The binary search reached
  18 steps, and 8 of the 9 V6 passes tried all 64 candidates.

| group | trials | bitmap hits | key-matched | records | V6 passes | R20 | E13 / E15 draws | pair |
|---|---|---|---|---|---|---|---|---|
| 0 | 16,777,216 | 9,958 | 224 | 447 | 3 | 0 | 0 / 0 | |
| 1 | 16,777,216 | 9,931 | 245 | 561 | 4 | 0 | 0 / 0 | |
| 2 | 16,777,216 | 10,069 | 260 | 575 | 0 | 0 | 0 / 0 | |
| 3 | 16,777,216 | 9,971 | 251 | 526 | 0 | 0 | 0 / 0 | |
| 5920 (to n*) | 4,561,628 | 2,654 | 57 | 133 | 2 | 1 | 2,829 / 19 | stored pair |

The full output of both programs is in Appendix C.8.

### 16.5 Comparison and sensitivity

- Per trial the counted program costs 584.6 primitives (582 + 21/8). The executable that ran
  retires 154.75 instructions per trial on its hot path. Priced with each 32-bit lane in its own
  word, those come to 1133 per trial (mean 7.32); under the SWAR prices of Section 14.6, 604.
- Forms of our previous filing. With rotations as two shifts and an OR and the Boolean functions in
  the reference core's forms (775 per trial, `klane.h`, checked in 16.4), K would be 36,356,896,376
  units and the total 2^35.5937.
- Reference-core conventions. With every rotation written as the organizer's reference core writes
  it (mask, shift, shift, OR, mask: five primitives), and T1, T2 and every schedule word masked as
  there (1035 per trial, `klane_ref.h`), K would be 48,444,713,912 units and the total 2^35.8960.
- Library calls. With ten times the library bound (10^9 instructions at 1024), the total would be
  2^35.3339.
- The counts are exact for the program, so no safety factor is applied.

### 16.6 The synthetic completion checks as counted replays

The three synthetic completion checks (Sections 8 and 15.1, before K) ran `r31sim3 1 20 5eed3 sim3-coll.txt sim`
(B.6), each with the S of the z3 attempt just finished. A synthetic run is deterministic: one worker
thread draws its coins from a stream seeded by the seed and the thread index, and counts trials in
batches of 2^16 until the 20 s wall cap. A run that completed N trials therefore executed exactly the
first N trials of that stream.

| run | S | records | trials (logged FINAL line) | what happened |
|---|---|---|---|---|
| 1 | attempt 1 | 0 | none | segmentation fault at the first trial: with no records, r % nrec indexes far outside the table. A re-run on 2026-10-08 ends with signal 11 after 124,642,769,780 instructions. |
| 2 | attempt 2 | 224 | 275,316,736 | completed; FINAL v6=538099 joint=42381 both=88 comp=42381/42381 coll=88 |
| 3 | attempt 3 | 132,096 | 250,544,128 | completed; FINAL v6=489532 joint=38874 both=64 comp=38874/38874 coll=64 |

Correction. Our earlier filings (50592e75 and later, including f99530e8) charged the synthetic checks as three runs of 500,284,109,323
instructions each, the count of one re-run of run 3's command. The runs differed: run 1 stopped at its
first trial, and run 2 completed 9.9% more trials than run 3. The factor 2 of those filings' price
covered the difference. This filing charges each run by its exact counted replay instead.

`scount.c` (Appendix C.13) writes `r31sim3`'s s1 inverse, table build, self-check and trial loop in
the counted primitives of Section 16.1, with the code of `kcount.c` for the first three. It includes
`r31sim3.c` unchanged and, for each run, is built with that run's S. It replays N trials of the
run's stream and checks two things:
- trial by trial, the counted `process_sim` and `r31sim3`'s own `process_sim` on the same draws agree
  on every counter;
- the replayed counters equal the run's logged FINAL line.
The trial loop indexes the records in the order the run's own `qsort` left them; the counted merge
sort produces the same multiset and key order, and a trial picks its record by index. The 64-bit
remainder r % nrec is a branch-free restoring division (64 steps of 9 primitives).

| run | s1 inverse, table, self-check | trial loop (counted replay) | per trial | library calls and process launch (3e7 instructions at 1024, H8) | total |
|---|---|---|---|---|---|
| 1 | 236,317,808,502 | first trial: at most 10,000 | | 30,720,000,000 | 267,037,818,502 |
| 2 | 236,255,568,814 | 1,745,020,550,020 | 6338.23 | 30,720,000,000 | 2,011,996,118,834 |
| 3 | 236,418,844,446 | 1,588,088,539,519 | 6338.56 | 30,720,000,000 | 1,855,227,383,965 |
| all three | | | | | 4,134,261,321,301 |

Synthetic checks: ceil(4,134,261,321,301 / 2140) = **1,931,897,814** units.

Validation output (Appendix C.14): both replays reproduce their run's FINAL counters exactly:
- run 2: trials=275316736 rechits=275316736 v6=538099 joint=42381 both=88 comp=42381/42381 coll=88;
- run 3: trials=250544128 rechits=250544128 v6=489532 joint=38874 both=64 comp=38874/38874 coll=64.

## 17. Search K's trials as a 7-lane SWAR word-RAM program (H2)

This section replaces only the pass term of Section 16.3. Everything else in K (group set-up, bitmap hits,
key-matched hits, records, V6 passes, the R20 pass, the table build, the s1 inverse, the self-check and the
library bound) keeps the charges and event counts of Section 16.3. The run, its event counters and the stored pair
are unchanged.

### 17.1 Why a SWAR program is the right price

The cost model's machine has 256-bit words, and Section 16 charges K as an explicit program on that machine that
makes the same decisions as the executable that ran (H2). Section 16 puts each 32-bit value in its own 256-bit
word, using 32 of the 256 bits. The trials of one group differ only in message word 15 (x = j, Section 7.3 K1), so
seven consecutive trials can share one word: lane l occupies bits 36l..36l+35 and holds trial j+l. The program
below computes, for every trial, the same key IV[0] + A30 and the same bitmap decision as Section 16's trial, and
it hands each hit to Section 16's hit processing with the same j. It is the same algorithm on the same machine with
a different data layout; the r32 track's qualified packages price first-block evaluation the same way (7-lane
36-bit guard-bit SWAR, Th0rgal f310d44f; 8-lane SWAR, 10506300).

### 17.2 One pass of 7 trials: 1,322 primitives

`swar7_k.py` (Appendix D) generates the pass as straight-line code from Section 16's trial structure
(`kprog.gen_lane` of f99530e8, Appendix C.6 there, sha256 c0c4453a...f8e7), line by line, and counts it with an
interpreter that charges every primitive. Conventions are those of Section 16.1 with these changes:
- **Lanes.** Each value is a 256-bit word with seven 36-bit lanes; bits 252..255 are never used. Group values and
  round constants are lane-broadcast once per group (below) and read with one counted load per use, exactly where
  the scalar trial loads them.
- **Rotations and shifts.** A 32-bit rotation inside a lane is ((v >> r) & LO_r) | ((v << (32-r)) & HI_r): five ALU
  primitives and two counted mask loads. A sigma shift is (v >> k) & SHR_k: two ALU primitives and one load. Both
  read only bits 0..31 of their own lane, so they are exact whatever the guard bits hold. All 22 lane masks are
  loaded at every use (none is register-resident).
- **Guard bits instead of masks.** E and A are masked with M7 (2^32-1 in every lane) as in the scalar trial. The
  twelve schedule words, T1, T2 and the key are left unmasked: every one of the 116 additions has a static per-lane
  upper bound, the largest is 10 (2^32-1) < 2^36, so no carry leaves a lane or reaches bit 252. The interpreter also
  checks every lane against its bound on every executed operation.
- **Bitmap test.** Per lane: t = KEY >> (36l+8), ((t >> 6) & M18) + BM, load the 64-bit bitmap word,
  (word >> (t & 63)) & 1, compare, branch: 10 primitives. M18 is loaded once per pass.
- **Loop control, 16 per pass.** X += (7,...,7) (load, add); trial counter (two loads, add, store); abort test
  ((base+6) & 0xfffff) < 7 (load, AND, load, compare, branch), which fires after the pass containing each trial
  k 2^20, 16 times per group as in the run; pass loop (add, two loads, compare, branch).

| component | add | AND | OR | XOR | NOT | shl | shr | load | store | cmp | br | **total** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| steps 15..30 | 98 | 284 | 90 | 105 | 15 | 90 | 90 | 205 | - | - | - | **977** |
| 12 schedule words | 18 | 60 | 24 | 24 | - | 24 | 36 | 72 | - | - | - | **258** |
| 7 bitmap tests | 7 | 21 | - | - | - | - | 21 | 8 | - | 7 | 7 | **71** |
| loop control | 3 | 1 | - | - | - | - | - | 7 | 1 | 2 | 2 | **16** |
| **pass of 7 trials** | 126 | 366 | 114 | 129 | 15 | 114 | 147 | 292 | 1 | 9 | 9 | **1,322** |

That is 188.857 per trial, against 582 + 21/8 = 584.6 in Section 16.2. The largest live set is 26 registers
(including X, the pass base and the four fixed registers), within a 32-register machine.

**Per group.** 2^24 = 7 * 2,396,745 + 1, so each group ends with one tail pass at base 2^24 - 1 in which only lane 0
is tested; no trial outside the run's trial set is ever tested. The tail pass executes 1,252 primitives and is
charged 1,322. The group also builds 59 broadcast vectors (24 group values, 9 round constants, 22 masks, 4 loop
vectors; each a load, four shift/OR doublings and a store, 10) and initialises X and the base: 592. Section 17 uses
the group values of the 775-variant trial (f99530e8), whose set-up is 13,697 rather than 13,505; the difference
(192 per group) is charged as well.

**Per hit.** Recovering j = base + l for Section 16's hit processing costs 3.

### 17.3 Validation

`swar7_k.py` checks, on 800 random groups (random words 0..14): 6,400 full passes and 800 tail passes, i.e. 45,600
lane trials, at bases 0, 2^24 - 8, 2^24 - 15 (the last full pass), 2^20 - 3 (straddling an abort checkpoint),
2^23 - 1, random bases and the tail pass. For every lane:
- the key equals word 0 of our own FIPS 180-4 31-step compression with feed-forward: 0 mismatches;
- the key equals word 0 of the organizer core's `_compress(..., 31)`: 0 mismatches;
- the key, the bitmap decision and the 775-primitive count equal those of the scalar trial of f99530e8's
  `kprog.py` (verbatim, sha256 c0c4453a...f8e7) on the same bitmap: 0 mismatches;
- bitmap decisions: 0 mismatches over 22,779 hits; in 7,200 forced-hit checks the tested bit of one lane is set and
  that lane's decision becomes 1 every time;
- every full pass executes exactly 1,322 primitives and every tail pass 1,252; all 6,400 abort-test and pass-loop
  decisions are correct; no lane ever exceeds its static bound and bits 252..255 are never set;
- one full group is enumerated: 2,396,745 full passes, 1 tail pass, 16 abort firings, 16,777,216 trials.
The scalar trial was itself checked against `r31det3`'s own trial block on 71,670,492 trials of the committed run
(Section 16.4), so the SWAR pass makes the executable's decisions transitively. The full output is in Appendix D.

### 17.4 Ledger

Run facts (Section 8): 5,932 groups, 99,492,036,640 = 5,928 * 2^24 + 36,700,192 trials; the 4 aborted groups ran
k * 2^20 + 8 trials each. Every group, including the aborted ones, is charged in full:
5,932 * ceil(2^24 / 7) = 5,932 * 2,396,746 = 14,217,497,272 passes. (Stopping the aborted groups at their own
checkpoints would give 14,213,153,172.) The SWAR program's abort checkpoint fires at or before the run's, so it
tests a subset of the run's trials and the run's hit counters remain upper bounds.

```
K (Section 16.3)                         58,601,795,172,441
 - scalar passes 12,436,504,580 * 4,677  -58,165,531,920,660
 + SWAR passes 14,217,497,272 * 1,322    +18,795,531,393,584
 + broadcast 5,932 * 592                 +         3,511,744
 + set-up difference 5,932 * 192         +         1,138,944
 + lane index 58,831,394 hits * 3        +       176,494,182
 = K ops                                  19,231,975,790,235
K units = ceil(19,231,975,790,235 / 2140) = 8,986,904,575
total = 42,877,883,846 - 27,384,016,436 + 8,986,904,575 = 24,480,771,985 = 2^34.51093
```

### 17.5 Claim margin and sensitivity

For the v1 pass (superseded by v2, Section 17.7), the claim 34.53 covered the strictest masking convention:

| change to the SWAR pass | ops per pass | total |
|---|---|---|
| as counted | 1,322 | 2^34.5109 |
| every T1, T2, schedule word and the key also masked with M7, as the reference core does | 1,365 | 2^34.5277 |
| claim break-even | 1,371 | 2^34.52999 |
| masks register-resident (not claimed) | 1,082 | 2^34.4138 |
| twice the pass cost | 2,644 | 2^34.9532 |
| scalar trials of Section 16 (the previous filing) | 4,677 per 8 | 2^35.3195 |

The 8-lane 32-bit variant (carry-isolated additions) costs 2,114 per 8 trials (264.25 per trial) and is not used.

### 17.7 Version 2: register-resident masks on a 32-register machine (claimed)

v1 loads every lane mask at every use. v2 (`swar7_k_v2.py`, Appendix D2) keeps masks in registers where an exact
liveness analysis of the straight-line pass shows that they fit in 32 registers.

- **Register count.** For straight-line code the number of registers needed equals the maximum number of
  simultaneously live values, which `live_profile` computes at every instruction. We use the strict convention that
  a destination never reuses the register of a source that dies at the same instruction. Always counted: X, the pass
  base, the four fixed registers (M7, bitmap base, 63, 1) and every resident mask.
- **Schedule first.** v1's order allows only 7 resident masks (max live 26). v2 computes the 12 schedule words before
  step 15 (order 17, 19, 22, 21, 24, 26, 28, 23, 25, 27, 30, 29) and spills each round addend once to a scratch word
  (12 stores and 12 reloads, +24 operations, each counted as one primitive like every other fixed-address memory
  operation).
- **Resident masks.** 13 masks for the whole run: the 12 Sigma0/Sigma1 masks (LO/HI for r = 2, 13, 22, 6, 11, 25) and
  LO17. HI17, LO19, HI19 and SHR10 are loaded once per pass and held through the schedule phase. The five sigma0 masks
  are still loaded at each use. The maximum live count is exactly 32 (reached at 44 program points); any further
  residency needs 33 or more.
- **Pass cost.** 1,322 - 231 avoided mask loads + 24 spill operations = **1,115** per 7 trials (159.3 per trial):
  schedule 237, steps 15..30 791, bitmap tests 71, loop 16. The tail pass is 1,045 and is charged 1,115.
- **Extra charges.** 13 per group (loading the resident masks) and 13 per bitmap hit (reloading them after the hit
  processing, which may use every register).
- **Validation.** The same 800 groups, 45,600 lane trials as v1: keys equal FIPS, the organizer core and kprog's scalar
  trial (0 mismatches); bitmap decisions 0 mismatches (22,779 hits, 7,200 forced); every abort and loop decision
  correct; every pass exactly 1,115. The variant that also masks T1, T2, every schedule word and the key (1,158 =
  1,115 + 43) is validated as well.

```
K (Section 16.3)                         58,601,795,172,441
 - scalar passes 12,436,504,580 * 4,677  -58,165,531,920,660
 + SWAR passes 14,217,497,272 * 1,115    +15,852,509,458,280
 + broadcast 5,932 * 592                 +         3,511,744
 + set-up difference 5,932 * 192         +         1,138,944
 + lane index 58,831,394 hits * 3        +       176,494,182
 + resident masks: 5,932 * 13 + 58,831,394 * 13   +   764,885,238
 = K ops                                  16,289,718,740,169
K units = ceil(16,289,718,740,169 / 2140) = 7,612,018,103
total = 42,877,883,846 - 27,384,016,436 + 7,612,018,103 = 23,105,885,513 = 2^34.427541
```

We claim **34.45**, which also covers the strictest masking convention:

| v2 pass | ops per pass | total |
|---|---|---|
| as counted | 1,115 | 2^34.42754 |
| T1, T2, schedule words and key also masked | 1,158 | 2^34.44527 |
| claim break-even | 1,169 | 2^34.44977 |
| v1 (all masks loaded at use) | 1,322 | 2^34.5109 (34.53 claimed in 0404f1a6) |
| twice the v2 pass | 2,230 | 2^34.8287 |
| scalar trials of Section 16 | 4,677 per 8 | 2^35.3195 |

The register bound has no slack under the strict convention (one register under the usual reuse convention). A
reviewer who rejects the residency gets v1's 2^34.5109.

### 17.6 Premise added to H2

H2 now also covers this layout: K's trial work is the primitive count of a program on the cost model's 256-bit
machine that makes the same decisions as the executable, here with seven trials per word. What remains uncounted
is the same as in Section 16: nothing inside the algorithm. The SWAR pass was validated against the scalar trial,
the organizer core and FIPS, not directly against `r31det3`; that link is the scalar trial's validation in 16.4.

## Appendix A. Commitments (written before each run)

A.1 Starting solution (`s-commit.txt`):

    yukon hashsmash sha256-r31 v3 own starting solution z3 seed 2026-10-07
    85406d4bf2ab97c155757e390d049427b8207ff0f682302e846b3be9f9dd09dc
    z3seed 88108363
    18e202187316bb3e64fa537899807215b1df9cb95ea4659169b03096054ad830  gen_s.py
    b3f87650423b955026eb4c988ad5c4256fb5a7224cc9b1ce1fbfc0525ba45ca1  s-model.smt2
    Z3 version 4.15.4 - 64 bit
    timeout 1800 s, single thread, nice 10; retries: next seed = previous + 1, all charged
    committed 2026-10-07T12:52:04+0900
    --- attempt 2 (model revised: non-empty-table constraints added; attempt 1 charged)
    z3seed 88108364
    0fa9d132dc3b61857f93a82de2e13435322bd97311b7ed13848b69d58164ab34  gen_s.py
    db9092903f0a188c6b273db4ce398142ed0d200fb9e2d9f399dad675f01d7256  s-model2.smt2
    committed 2026-10-07T12:54:02+0900
    --- attempt 3 (added: c8 residue 0xe730f mod 2^20 from a 300,000-sample residue scan, c8scan.c)
    z3seed 88108365
    0c1d4552ed54f6b286582fe2c75de7a45d798b3a6c950fa908fb67f43406693b  gen_s.py
    3d6908694c4a70ebd4f807d9a69beff810b96ca28e972ba3aaa7aab22f3953c7  s-model3.smt2
    3e3024772745620766174f45e3e1e6eb374b8eca55da3a72a6e47cb363b2c6eb  c8scan.c
    committed 2026-10-07T13:01:11+0900

A.2 Search K (`k-commit.txt`):

    yukon hashsmash sha256-r31 v3 construction K seed 2026-10-07
    dfafc947679ebe068755d5a362a5b23a74abc983460706350de93b10729410bf
    seed64 dfafc947679ebe06
    29f4a1900e293efd2459cac87ed197c8176f20b763b92663da19dea3c3140d3e  r31det3.c
    84003700c7015677e60700dc5c044d1c6e7c0acc652e6bf12d536f9aa5084437  sp_own.h
    82607ffd5cee1fb1495d5192ed0ac3dc373fb27588e92b575fc84c5f960f3ff9  s-out3.txt
    threads 12, wall cap 1200 s, stop at the first collision by trial index (groups up to n*>>24 completed)
    committed 2026-10-07T13:04:56+0900

## Appendix B. Source

B.1 `gen_s.py` (model generator; attempt 3 = all constraints; attempts 1 and 2 used subsets (a)-(e) and (a)-(f))

```python
"""Emit the SMT-LIB2 model whose solutions are starting solutions S for the 31-step trail.

Inputs are the trail cells (public characteristic) and SHA-256 constants only.
Unknowns: copy P and copy P' of A1..A12, E5..E12, W9..W12 (P' of W10..W12 equals P).
"""
import sys

K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
     0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7]
EQ = "=" * 32
CH_A = {5: "===================n=unnnnnnn=n=", 6: "========n======================u", 7: "===u===n==n========n=========n=u",
        8: "=============================n==", 10: "================u============u=="}
CH_E = {5: "000111010001111110nu=11111unnnu1", 6: "101011=11==0n0==u11110==1110011n", 7: "un0u1100n=01u11111001u1=n110u10n",
        8: "1u01un0u0=1=1=11n=0=u0=001001u0=", 9: "01100001110=0=010===00=11101u0=1", 10: "=1n1uuuuu0100=1un0=10unnnnnnn010",
        11: "=01u1010uu1==11100===1000001n=0=", 12: "==110001=11====1n====0011110n=0="}
CH_W = {9: "================u==========1=u=="}
ROW3 = "==========================10===="
ROW4 = "============0===0=========01===0"
D6, D7 = 0x002087f1, 0x4fefb5fa
C7, C8 = 0xffdf780f, 0xb00fca02
D8, D9 = 0x28011100, 0x00008004
NEG_D8 = (-D8) & 0xFFFFFFFF


def h(x):
    return f"#x{x & 0xFFFFFFFF:08x}"


def masks(row):
    m_eq = m_fix = v_fix = m_u = m_n = 0
    for k, c in enumerate(row):
        b = 1 << (31 - k)
        if c == "=":
            m_eq |= b
        elif c in "01":
            m_fix |= b
            if c == "1":
                v_fix |= b
        elif c == "u":
            m_u |= b
        elif c == "n":
            m_n |= b
    return m_eq, m_fix, v_fix, m_u, m_n


def cells(x, xp, row):
    m_eq, m_fix, v_fix, m_u, m_n = masks(row)
    out = []
    if m_fix:
        out += [f"(= (bvand {x} {h(m_fix)}) {h(v_fix)})", f"(= (bvand {xp} {h(m_fix)}) {h(v_fix)})"]
    if m_u:
        out += [f"(= (bvand {x} {h(m_u)}) #x00000000)", f"(= (bvand {xp} {h(m_u)}) {h(m_u)})"]
    if m_n:
        out += [f"(= (bvand {x} {h(m_n)}) {h(m_n)})", f"(= (bvand {xp} {h(m_n)}) #x00000000)"]
    if m_eq:
        out += [f"(= (bvand (bvxor {x} {xp}) {h(m_eq)}) #x00000000)"]
    return out


def S0(x): return f"(bvxor ((_ rotate_right 2) {x}) ((_ rotate_right 13) {x}) ((_ rotate_right 22) {x}))"
def S1(x): return f"(bvxor ((_ rotate_right 6) {x}) ((_ rotate_right 11) {x}) ((_ rotate_right 25) {x}))"
def s0(x): return f"(bvxor ((_ rotate_right 7) {x}) ((_ rotate_right 18) {x}) (bvlshr {x} #x00000003))"
def IF(x, y, z): return f"(bvxor (bvand {x} {y}) (bvand (bvnot {x}) {z}))"
def MAJ(x, y, z): return f"(bvxor (bvand {x} {y}) (bvand {x} {z}) (bvand {y} {z}))"


def main(seed, exclude_a1):
    L = ["(set-logic QF_BV)", f"(set-option :random-seed {seed})", f"(set-option :sat.random_seed {seed})", f"(set-option :smt.random_seed {seed})"]
    names = []
    for c in ("", "p"):
        names += [f"A{i}{c}" for i in range(1, 13)] + [f"E{i}{c}" for i in range(5, 13)]
    names += ["W9", "W10", "W11", "W12", "W9p", "E3", "E4", "W7", "W8"]
    for n in names:
        L.append(f"(declare-fun {n} () (_ BitVec 32))")
    A = lambda i, c="": f"A{i}{c}"
    E = lambda i, c="": f"E{i}{c}"
    Wn = lambda i, c="": ("W9p" if (i == 9 and c == "p") else f"W{i}")
    asserts = []
    for i in range(1, 13):
        asserts += cells(A(i), A(i, "p"), CH_A.get(i, EQ))
    for i in range(5, 13):
        asserts += cells(E(i), E(i, "p"), CH_E[i])
    asserts += cells("W9", "W9p", CH_W[9])
    for c in ("", "p"):
        for i in range(5, 13):  # A-equation
            asserts.append(f"(= {A(i, c)} (bvadd (bvsub {E(i, c)} {A(i - 4, c)}) {S0(A(i - 1, c))} {MAJ(A(i - 1, c), A(i - 2, c), A(i - 3, c))}))")
        for i in range(9, 13):  # E-equation
            asserts.append(f"(= {E(i, c)} (bvadd {A(i - 4, c)} {E(i - 4, c)} {S1(E(i - 1, c))} {IF(E(i - 1, c), E(i - 2, c), E(i - 3, c))} {h(K[i])} {Wn(i, c)}))")
    # step-8 difference relation (A4, E4 carry no difference; dW8 = d8)
    asserts.append(f"(= (bvsub {E(8, 'p')} {E(8)}) (bvadd (bvsub {S1(E(7, 'p'))} {S1(E(7))}) (bvsub {IF(E(7, 'p'), E(6, 'p'), E(5, 'p'))} {IF(E(7), E(6), E(5))}) {h(D8)}))")
    # step 13: dE13 = 0 and dA13 = 0
    asserts.append(f"(= (bvadd {A(9, 'p')} {E(9, 'p')} {S1(E(12, 'p'))} {IF(E(12, 'p'), E(11, 'p'), E(10, 'p'))}) (bvadd {A(9)} {E(9)} {S1(E(12))} {IF(E(12), E(11), E(10))}))")
    asserts.append(f"(= {MAJ(A(12, 'p'), A(11, 'p'), A(10, 'p'))} {MAJ(A(12), A(11), A(10))})")
    # W9 in V9
    asserts.append(f"(= (bvsub {s0('W9p')} {s0('W9')}) {h(NEG_D8)})")
    # non-empty table: some (W8, E4) and (W7, E3) pass the P2 filters (copy-P equations; E3, E4 carry no difference)
    asserts += cells("E4", "E4", ROW4) + cells("E3", "E3", ROW3)
    asserts.append(f"(= {E(8)} (bvadd {A(4)} E4 {S1(E(7))} {IF(E(7), E(6), E(5))} {h(K[8])} W8))")
    asserts.append(f"(= {E(7)} (bvadd {A(3)} E3 {S1(E(6))} {IF(E(6), E(5), 'E4')} {h(K[7])} W7))")
    asserts.append(f"(= (bvsub {E(7, 'p')} {E(7)}) (bvadd (bvsub {S1(E(6, 'p'))} {S1(E(6))}) (bvsub {IF(E(6, 'p'), E(5, 'p'), 'E4')} {IF(E(6), E(5), 'E4')}) {h(D7)}))")
    asserts.append(f"(= (bvsub {E(6, 'p')} {E(6)}) (bvadd (bvsub {S1(E(5, 'p'))} {S1(E(5))}) (bvsub {IF(E(5, 'p'), 'E4', 'E3')} {IF(E(5), 'E4', 'E3')}) {h(D6)}))")
    asserts.append(f"(= (bvsub {s0('(bvadd W8 ' + h(D8) + ')')} {s0('W8')}) {h(C8)})")
    asserts.append(f"(= (bvsub {s0('(bvadd W7 ' + h(D7) + ')')} {s0('W7')}) {h(C7)})")
    # yield: c8 = E8 - A4 - S1(E7) - IF(E7,E6,E5) - K8 in the residue class mod 2^20 that maximises row-4 passes over V8
    asserts.append(f"(= (bvand (bvsub (bvsub (bvsub (bvsub {E(8)} {A(4)}) {S1(E(7))}) {IF(E(7), E(6), E(5))}) {h(K[8])}) #x000fffff) #x000e730f)")
    if exclude_a1 is not None:
        asserts.append(f"(not (= A1 {h(exclude_a1)}))")
    for a in asserts:
        L.append(f"(assert {a})")
    L.append("(check-sat)")
    L.append("(get-value (" + " ".join(names) + "))")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    seed = int(sys.argv[1])
    ex = int(sys.argv[2], 16) if len(sys.argv) > 2 else None
    sys.stdout.write(main(seed, ex))
```

B.2 `check_s.py` (independent verification of S; also writes `sp_own.h`)

```python
import re, sys, json
sys.path.insert(0, ".")
from gen_s import K, CH_A, CH_E, CH_W, EQ, D8, D9
M = 0xFFFFFFFF
R = lambda x, n: ((x >> n) | (x << (32 - n))) & M
S0 = lambda x: R(x, 2) ^ R(x, 13) ^ R(x, 22)
S1 = lambda x: R(x, 6) ^ R(x, 11) ^ R(x, 25)
s0 = lambda x: R(x, 7) ^ R(x, 18) ^ (x >> 3)
IF = lambda x, y, z: (x & y) ^ (~x & z & M)
MAJ = lambda x, y, z: (x & y) ^ (x & z) ^ (y & z)
v = {k: int(x, 16) for k, x in re.findall(r"\((\w+) #x([0-9a-f]{8})\)", open(sys.argv[1] if len(sys.argv)>1 else "s-out.txt").read())}
A = {c: {i: v[f"A{i}{c}"] for i in range(1, 13)} for c in ("", "p")}
E = {c: {i: v[f"E{i}{c}"] for i in range(5, 13)} for c in ("", "p")}
W = {"": {9: v["W9"], 10: v["W10"], 11: v["W11"], 12: v["W12"]}}
W["p"] = {9: v["W9p"], 10: v["W10"], 11: v["W11"], 12: v["W12"]}
def cell_ok(x, xp, row):
    for k, ch in enumerate(row):
        b = 31 - k; a, bp = (x >> b) & 1, (xp >> b) & 1
        ok = {"=": a == bp, "0": a == 0 and bp == 0, "1": a == 1 and bp == 1, "u": a == 0 and bp == 1, "n": a == 1 and bp == 0}[ch]
        if not ok: return False
    return True
bad = 0
for i in range(1, 13): bad += not cell_ok(A[""][i], A["p"][i], CH_A.get(i, EQ))
for i in range(5, 13): bad += not cell_ok(E[""][i], E["p"][i], CH_E[i])
bad += not cell_ok(W[""][9], W["p"][9], CH_W[9])
for c in ("", "p"):
    for i in range(5, 13):
        bad += A[c][i] != (E[c][i] - A[c][i - 4] + S0(A[c][i - 1]) + MAJ(A[c][i - 1], A[c][i - 2], A[c][i - 3])) & M
    for i in range(9, 13):
        bad += E[c][i] != (A[c][i - 4] + E[c][i - 4] + S1(E[c][i - 1]) + IF(E[c][i - 1], E[c][i - 2], E[c][i - 3]) + K[i] + W[c][i]) & M
bad += ((E["p"][8] - E[""][8]) & M) != ((S1(E["p"][7]) - S1(E[""][7]) + IF(E["p"][7], E["p"][6], E["p"][5]) - IF(E[""][7], E[""][6], E[""][5]) + D8) & M)
bad += ((A["p"][9] + E["p"][9] + S1(E["p"][12]) + IF(E["p"][12], E["p"][11], E["p"][10])) & M) != ((A[""][9] + E[""][9] + S1(E[""][12]) + IF(E[""][12], E[""][11], E[""][10])) & M)
bad += MAJ(A["p"][12], A["p"][11], A["p"][10]) != MAJ(A[""][12], A[""][11], A[""][10])
bad += ((s0(W["p"][9]) - s0(W[""][9])) & M) != ((-D8) & M)
bad += ((W["p"][9] - W[""][9]) & M) != D9
print("violations", bad)
pub_A1 = 0xf36e6fcf  # check only: differs from the published starting solution?
print("A1..A4", [f"{A[''][i]:08x}" for i in range(1, 5)], "differs from published A1:", A[""][1] != pub_A1)
# C header: index i+4 for i=-4..30 like the original layout; only 1..12 (A) and 5..12 (E) are used
def arr(d, lo, hi):
    return ",".join(f"0x{d.get(i, 0):08x}u" for i in range(-4, 31))
hdr = ["/* own starting solution S from z3 (seed 88108363); unused entries 0 */",
       "static const uint32_t SPA_A[35]={" + arr(A[""], 1, 12) + "};", "static const uint32_t SPA_E[35]={" + arr(E[""], 5, 12) + "};",
       "static const uint32_t SPB_A[35]={" + arr(A["p"], 1, 12) + "};", "static const uint32_t SPB_E[35]={" + arr(E["p"], 5, 12) + "};",
       "static const uint32_t S_W[31]={" + ",".join(f"0x{W[''].get(i, 0):08x}u" for i in range(31)) + "};"]
open("sp_own.h", "w").write("\n".join(hdr) + "\n")
json.dump({"A": A[""], "Ap": A["p"], "E": E[""], "Ep": E["p"], "W": W[""], "W9p": W["p"][9]}, open("S.json", "w"), indent=1)
```

B.3 `c8scan.c` and `v8dump.c` (residue scan over V8)

```c
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
int main(){ static uint32_t V[60000]; int n=0; FILE*f=fopen("v8.txt","r"); unsigned x; while(fscanf(f,"%x",&x)==1) V[n++]=x&0xfffff; fclose(f);
  uint32_t cm=(1u<<19)|(1u<<15)|(1u<<5)|(1u<<4)|1u, va=(1u<<4);
  uint64_t st=0x1234567ull; int best=0; uint32_t br=0; int hist[8]={0};
  for(int t=0;t<300000;t++){ st^=st<<13; st^=st>>7; st^=st<<17; uint32_t r=(uint32_t)st&0xfffff; int c=0;
    for(int i=0;i<n;i++){ uint32_t e=(r-V[i])&0xfffff; c+=((e&cm)==va); }
    if(c>best){best=c;br=r;} }
  printf("best residue %05x pass %d of %d\n",br,best,n); return 0; }
```

```c
#include <stdio.h>
#include <stdint.h>
static inline uint32_t R(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
static inline uint32_t s0(uint32_t x){return R(x,7)^R(x,18)^(x>>3);}
int main(){ uint32_t w=0; FILE*f=fopen("v8.txt","w"); do{ if((uint32_t)(s0(w+0x28011100u)-s0(w))==0xb00fca02u) fprintf(f,"%08x\n",w); w++; }while(w); fclose(f); return 0; }
```

B.4 `r31det3.c` (table P1/P2 and search K)

```c
// sha256-r31 relaxed-W20 first-block search from the published starting solution.
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <time.h>
#include <unistd.h>
#include <stdatomic.h>
#include "sp_own.h"

static const uint32_t K[31]={0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
 0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
 0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
 0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351};
static const uint32_t IV[8]={0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
#define R(x,n) (((x)>>(n))|((x)<<(32-(n))))
#define BS0(x) (R(x,2)^R(x,13)^R(x,22))
#define BS1(x) (R(x,6)^R(x,11)^R(x,25))
#define s0(x) (R(x,7)^R(x,18)^((x)>>3))
#define s1(x) (R(x,17)^R(x,19)^((x)>>10))
#define IF(x,y,z) (((x)&(y))^(~(x)&(z)))
#define MAJ(x,y,z) (((x)&(y))^((x)&(z))^((y)&(z)))
#define D5 0xfffff006u
#define D6 0x002087f1u
#define D7 0x4fefb5fau
#define D8 0x28011100u
#define D9 0x00008004u
#define D18 0xffff7ffcu
#define C6 0x00000ffau
#define C7 0xffdf780fu
#define C8 0xb00fca02u
#define IDX(i) ((i)+4)
#define AA(i) SPA_A[IDX(i)]
#define EA(i) SPA_E[IDX(i)]
#define AB(i) SPB_A[IDX(i)]
#define EB(i) SPB_E[IDX(i)]

typedef struct { uint32_t key, A0, E3, E4, W7, W8; } rec_t;
static rec_t *recs; static int nrec;
static uint64_t *bitmap; /* 2^24 bits on key>>8 */
static uint32_t G16[64]; static int ng16;
static uint32_t s1inv_col[32];

static void compress31(const uint32_t cv[8], const uint32_t m[16], uint32_t out[8]) {
  uint32_t W[31]; for(int t=0;t<16;t++) W[t]=m[t];
  for(int t=16;t<31;t++) W[t]=s1(W[t-2])+W[t-7]+s0(W[t-15])+W[t-16];
  uint32_t a=cv[0],b=cv[1],c=cv[2],d=cv[3],e=cv[4],f=cv[5],g=cv[6],h=cv[7];
  for(int t=0;t<31;t++){ uint32_t T1=h+BS1(e)+IF(e,f,g)+K[t]+W[t]; uint32_t T2=BS0(a)+MAJ(a,b,c);
    h=g; g=f; f=e; e=d+T1; d=c; c=b; b=a; a=T1+T2; }
  out[0]=cv[0]+a; out[1]=cv[1]+b; out[2]=cv[2]+c; out[3]=cv[3]+d; out[4]=cv[4]+e; out[5]=cv[5]+f; out[6]=cv[6]+g; out[7]=cv[7]+h;
}
static void digest(const uint32_t m0[16], const uint32_t m1[16], uint32_t out[8]) {
  uint32_t cv[8], cv2[8], pad[16]={0}; pad[0]=0x80000000u; pad[15]=1024;
  compress31(IV,m0,cv); compress31(cv,m1,cv2); compress31(cv2,pad,out);
}
static uint32_t s1inv(uint32_t y){ uint32_t x=0; for(int k=0;k<32;k++) if(y>>k&1) x^=s1inv_col[k]; return x; }
static void build_s1inv(void){
  uint32_t val[32], comb[32]; for(int i=0;i<32;i++){ uint32_t b=1u<<i; val[i]=s1(b); comb[i]=b; }
  for(int k=0;k<32;k++){ int p=-1; for(int i=k;i<32;i++) if(val[i]>>k&1){p=i;break;}
    if(p<0){fprintf(stderr,"s1 singular\n");exit(1);} uint32_t tv=val[k],tc=comb[k]; val[k]=val[p];comb[k]=comb[p];val[p]=tv;comb[p]=tc;
    for(int i=0;i<32;i++) if(i!=k && (val[i]>>k&1)){ val[i]^=val[k]; comb[i]^=comb[k]; } }
  for(int k=0;k<32;k++) s1inv_col[k]=comb[k];
  for(int t=0;t<1000;t++){ uint32_t y=(uint32_t)(t*2654435761u+12345); if(s1(s1inv(y))!=y){fprintf(stderr,"s1inv bad\n");exit(1);} }
}
static int cmprec(const void*a,const void*b){ uint32_t x=((const rec_t*)a)->key,y=((const rec_t*)b)->key; return x<y?-1:x>y; }
static void build_table(void){
  static uint32_t V7[1024],V8[65536]; int n7=0,n8=0; uint32_t w=0;
  do{ if((uint32_t)(s0(w+D8)-s0(w))==C8) V8[n8++]=w; if((uint32_t)(s0(w+D7)-s0(w))==C7) V7[n7++]=w;
      if((uint32_t)(s1(w+D9)-s1(w))==D18) G16[ng16++]=w; w++; }while(w!=0);
  uint32_t cm4=0,va4=0,cm3=0,va3=0; const char*r4="============0===0=========01===0",*r3="==========================10====";
  for(int k=0;k<32;k++){ uint32_t b=1u<<(31-k); if(r4[k]!='='){cm4|=b; if(r4[k]=='1')va4|=b;} if(r3[k]!='='){cm3|=b; if(r3[k]=='1')va3|=b;} }
  uint32_t lhs7=(EB(7)-EA(7))-(BS1(EB(6))-BS1(EA(6)))-D7, lhs6=(EB(6)-EA(6))-(BS1(EB(5))-BS1(EA(5)))-D6;
  recs=malloc(sizeof(rec_t)*(1<<20)); nrec=0;
  for(int i=0;i<n8;i++){ uint32_t W8=V8[i]; uint32_t E4=EA(8)-AA(4)-BS1(EA(7))-IF(EA(7),EA(6),EA(5))-K[8]-W8;
    if((E4&cm4)!=va4) continue; if((uint32_t)(IF(EB(6),EB(5),E4)-IF(EA(6),EA(5),E4))!=lhs7) continue;
    uint32_t A0=E4-AA(4)+BS0(AA(3))+MAJ(AA(3),AA(2),AA(1));
    for(int j=0;j<n7;j++){ uint32_t W7=V7[j]; uint32_t E3=EA(7)-AA(3)-BS1(EA(6))-IF(EA(6),EA(5),E4)-K[7]-W7;
      if((E3&cm3)!=va3) continue; if((uint32_t)(IF(EB(5),E4,E3)-IF(EA(5),E4,E3))!=lhs6) continue;
      uint32_t Am1=E3-AA(3)+BS0(AA(2))+MAJ(AA(2),AA(1),A0);
      recs[nrec++]=(rec_t){Am1,A0,E3,E4,W7,W8}; } }
  qsort(recs,nrec,sizeof(rec_t),cmprec);
  bitmap=calloc(1<<18,8); for(int i=0;i<nrec;i++){ uint32_t b=recs[i].key>>8; bitmap[b>>6]|=1ull<<(b&63); }
  fprintf(stderr,"V7=%d V8=%d G16=%d records=%d\n",n7,n8,ng16,nrec);
}

typedef struct { uint64_t trials, keyhits, recs, v6, joint, both, comp_try, comp_ok, coll, it13, it15, overshoot, bmhits, groups; } ctr_t;
static ctr_t ctrs[64];
static atomic_int stop_flag; static atomic_int live_threads; static pthread_mutex_t out_mu=PTHREAD_MUTEX_INITIALIZER;
static FILE *outf; static atomic_uint_fast64_t total_coll;

static uint64_t sm(uint64_t *s){ uint64_t z=(*s+=0x9e3779b97f4a7c15ull); z=(z^(z>>30))*0xbf58476d1ce4e5b9ull; z=(z^(z>>27))*0x94d049bb133111ebull; return z^(z>>31); }

/* returns 1 if completion found; fills W[0..15] */
static int complete(uint32_t W[16], uint32_t g, uint64_t *rs, ctr_t *cc){
  uint32_t W14=s1inv(g-W[9]-s0(W[1])-W[0]); W[14]=W14;
  if((uint32_t)(s1(W14)+W[9]+s0(W[1])+W[0])!=g) return 0;
  uint32_t b13=AA(9)+EA(9)+BS1(EA(12))+IF(EA(12),EA(11),EA(10))+K[13];
  uint32_t b13b=AB(9)+EB(9)+BS1(EB(12))+IF(EB(12),EB(11),EB(10))+K[13];
  if(b13!=b13b) return 0;
  for(int t=0;t<(1<<22);t++){
    cc->it13++; uint32_t E13=(uint32_t)sm(rs); uint32_t W13=E13-b13;
    uint32_t A13=E13-AA(9)+BS0(AA(12))+MAJ(AA(12),AA(11),AA(10));
    uint32_t A13b=E13-AB(9)+BS0(AB(12))+MAJ(AB(12),AB(11),AB(10)); if(A13!=A13b) return 0;
    uint32_t E14=AA(10)+EA(10)+BS1(E13)+IF(E13,EA(12),EA(11))+K[14]+W14;
    uint32_t E14b=AB(10)+EB(10)+BS1(E13)+IF(E13,EB(12),EB(11))+K[14]+W14;
    if((uint32_t)(E14b-E14)!=0x8004u) continue;
    uint32_t A14=E14-AA(10)+BS0(A13)+MAJ(A13,AA(12),AA(11)), A14b=E14b-AB(10)+BS0(A13)+MAJ(A13,AB(12),AB(11));
    if(A14!=A14b) continue;
    uint32_t f15=AA(11)+EA(11)+BS1(E14)+IF(E14,E13,EA(12))+K[15], f15b=AB(11)+EB(11)+BS1(E14b)+IF(E14b,E13,EB(12))+K[15];
    if(f15!=f15b) continue;
    for(int u=0;u<(1<<12);u++){
      cc->it15++; uint32_t E15=(uint32_t)sm(rs); uint32_t W15=E15-f15;
      uint32_t E16=AA(12)+EA(12)+BS1(E15)+IF(E15,E14,E13)+K[16]+g, E16b=AB(12)+EB(12)+BS1(E15)+IF(E15,E14b,E13)+K[16]+g+D9;
      if(E16!=E16b) continue;
      uint32_t A15=E15-AA(11)+BS0(A14)+MAJ(A14,A13,AA(12));
      uint32_t f17=A13+E13+BS1(E16)+IF(E16,E15,E14), f17b=A13+E13+BS1(E16)+IF(E16,E15,E14b); (void)A15;
      if(f17!=f17b) continue;
      W[13]=W13; W[15]=W15; return 1; } }
  return 0;
}

static int process_hit(int tid, const uint32_t m0[16], uint64_t *rs, int verbose){ int found=0;
  ctr_t *c=&ctrs[tid]; c->bmhits++; uint32_t cv[8]; compress31(IV,m0,cv);
  int lo=0,hi=nrec; while(lo<hi){int mid=(lo+hi)/2; if(recs[mid].key<cv[0]) lo=mid+1; else hi=mid;}
  if(lo>=nrec || recs[lo].key!=cv[0]) return 0;
  c->keyhits++;
  for(int r=lo;r<nrec && recs[r].key==cv[0];r++){
    const rec_t *q=&recs[r]; c->recs++;
    uint32_t a[35],e[35];
    a[IDX(-1)]=cv[0];a[IDX(-2)]=cv[1];a[IDX(-3)]=cv[2];a[IDX(-4)]=cv[3];e[IDX(-1)]=cv[4];e[IDX(-2)]=cv[5];e[IDX(-3)]=cv[6];e[IDX(-4)]=cv[7];
    a[IDX(0)]=q->A0; for(int i=1;i<=12;i++) a[IDX(i)]=AA(i); e[IDX(3)]=q->E3; e[IDX(4)]=q->E4; for(int i=5;i<=12;i++) e[IDX(i)]=EA(i);
#define Ax(i) a[IDX(i)]
#define Ex(i) e[IDX(i)]
    Ex(0)=Ax(0)+Ax(-4)-BS0(Ax(-1))-MAJ(Ax(-1),Ax(-2),Ax(-3));
    Ex(1)=Ax(1)+Ax(-3)-BS0(Ax(0))-MAJ(Ax(0),Ax(-1),Ax(-2));
    Ex(2)=Ax(2)+Ax(-2)-BS0(Ax(1))-MAJ(Ax(1),Ax(0),Ax(-1));
    uint32_t W[16]; for(int i=0;i<=6;i++) W[i]=Ex(i)-Ax(i-4)-Ex(i-4)-BS1(Ex(i-1))-IF(Ex(i-1),Ex(i-2),Ex(i-3))-K[i];
    W[7]=q->W7; W[8]=q->W8; for(int i=9;i<=12;i++) W[i]=S_W[i]; W[13]=W[14]=W[15]=0;
    int v6=((uint32_t)(s0(W[6]+D6)-s0(W[6]))==C6);
    if(!v6) continue;
    c->v6++;
    uint32_t tgt=0u-(uint32_t)(s0(W[5]+D5)-s0(W[5])); uint32_t c18=W[11]+s0(W[3])+W[2];
    int gsel=-1; for(int k=0;k<ng16;k++){ uint32_t w18=s1(G16[k])+c18; if((uint32_t)(s1(w18+D18)-s1(w18))==tgt){gsel=k;break;} }
    if(gsel<0) continue;
    c->joint++; c->both++;
    c->comp_try++;
    uint32_t Wc[16]; memcpy(Wc,W,sizeof W);
    if(!complete(Wc,G16[gsel],rs,c)) { if(verbose) fprintf(stderr,"completion failed\n"); continue; }
    c->comp_ok++;
    uint32_t Wb[16]; memcpy(Wb,Wc,sizeof Wc); Wb[5]+=D5; Wb[6]+=D6; Wb[7]+=D7; Wb[8]+=D8; Wb[9]+=D9;
    uint32_t h1[8],h2[8]; digest(m0,Wc,h1); digest(m0,Wb,h2);
    if(memcmp(h1,h2,32)==0 && memcmp(Wc,Wb,64)!=0){
      c->coll++; atomic_fetch_add(&total_coll,1); found=1;
      pthread_mutex_lock(&out_mu);
      fprintf(outf,"COLLISION tid=%d\nM0 ",tid); for(int i=0;i<16;i++) fprintf(outf,"%08x",m0[i]);
      fprintf(outf,"\nM1 "); for(int i=0;i<16;i++) fprintf(outf,"%08x",Wc[i]);
      fprintf(outf,"\nM1b "); for(int i=0;i<16;i++) fprintf(outf,"%08x",Wb[i]);
      fprintf(outf,"\nDIGEST "); for(int i=0;i<8;i++) fprintf(outf,"%08x",h1[i]); fprintf(outf,"\n"); fflush(outf);
      pthread_mutex_unlock(&out_mu);
    } else if(verbose) fprintf(stderr,"digest mismatch\n");
    if(found) return 1;
  }
  return found;
}

static uint64_t seed_base; static double time_limit;
#define LANES 8
static int NTH; static _Atomic uint64_t best_n = UINT64_MAX;
static void *worker(void *arg){
  int tid=(int)(intptr_t)arg; ctr_t *c=&ctrs[tid]; atomic_fetch_add(&live_threads,1);
  uint32_t m[16];
  for(uint64_t g=(uint64_t)tid; ; g+=(uint64_t)NTH){
    uint64_t bn=atomic_load(&best_n);
    if(atomic_load(&stop_flag)) break;
    if(bn!=UINT64_MAX && g > (bn>>24)) break;
    c->groups++; uint64_t rs=seed_base ^ (g*0x9e3779b97f4a7c15ull) ^ 0x5bd1e9955bd1e995ull;
    for(int i=0;i<15;i++) m[i]=(uint32_t)sm(&rs);
    uint64_t crs=seed_base ^ (g*0xd1b54a32d192ed03ull) ^ 0x2545f4914f6cdd1dull; /* completion coins */
    uint32_t a=IV[0],b=IV[1],cc=IV[2],d=IV[3],e=IV[4],f=IV[5],gg=IV[6],h=IV[7];
    for(int t=0;t<15;t++){ uint32_t T1=h+BS1(e)+IF(e,f,gg)+K[t]+m[t]; uint32_t T2=BS0(a)+MAJ(a,b,cc); h=gg; gg=f; f=e; e=d+T1; d=cc; cc=b; b=a; a=T1+T2; }
    const uint32_t m16=s1(m[14])+m[9]+s0(m[1])+m[0], m18=s1(m16)+m[11]+s0(m[3])+m[2], m20=s1(m18)+m[13]+s0(m[5])+m[4];
    const uint32_t c17=m[10]+s0(m[2])+m[1], c19=m[12]+s0(m[4])+m[3], c21=m[14]+s0(m[6])+m[5], c22=s1(m20)+s0(m[7])+m[6];
    const uint32_t c23=m16+s0(m[8])+m[7], c24=s0(m[9])+m[8], c25=m18+s0(m[10])+m[9], c26=s0(m[11])+m[10];
    const uint32_t c27=m20+s0(m[12])+m[11], c28=s0(m[13])+m[12], c29=s0(m[14])+m[13], c30=m[14];
    int aborted=0;
    for(uint32_t base=0; base < (1u<<24); base+=LANES){
      uint32_t key[LANES];
      for(int j=0;j<LANES;j++){
        uint32_t x=base+(uint32_t)j;
        uint32_t w17=s1(x)+c17, w19=s1(w17)+c19, w21=s1(w19)+c21, w22=c22+x, w23=s1(w21)+c23, w24=s1(w22)+w17+c24;
        uint32_t w25=s1(w23)+c25, w26=s1(w24)+w19+c26, w27=s1(w25)+c27, w28=s1(w26)+w21+c28, w29=s1(w27)+w22+c29, w30=s1(w28)+w23+s0(x)+c30;
        uint32_t A=a,B=b,C=cc,D=d,E=e,F=f,G=gg,H=h,T1,T2;
#define RND(w,k) T1=H+BS1(E)+IF(E,F,G)+(k)+(w); T2=BS0(A)+MAJ(A,B,C); H=G; G=F; F=E; E=D+T1; D=C; C=B; B=A; A=T1+T2;
        RND(x,K[15]) RND(m16,K[16]) RND(w17,K[17]) RND(m18,K[18]) RND(w19,K[19]) RND(m20,K[20]) RND(w21,K[21]) RND(w22,K[22])
        RND(w23,K[23]) RND(w24,K[24]) RND(w25,K[25]) RND(w26,K[26]) RND(w27,K[27]) RND(w28,K[28]) RND(w29,K[29]) RND(w30,K[30])
        key[j]=IV[0]+A;
      }
      for(int j=0;j<LANES;j++){ uint32_t bi=key[j]>>8; if(bitmap[bi>>6]>>(bi&63)&1){ uint32_t mm[16]; memcpy(mm,m,60); mm[15]=base+(uint32_t)j;
          if(process_hit(tid,mm,&crs,0)){ uint64_t n=(g<<24)|(uint64_t)(base+(uint32_t)j); uint64_t cur=atomic_load(&best_n);
            while(n<cur && !atomic_compare_exchange_weak(&best_n,&cur,n)){}
            pthread_mutex_lock(&out_mu); fprintf(outf,"INDEX n=%llu group=%llu j=%u\n",(unsigned long long)n,(unsigned long long)g,base+(uint32_t)j); fflush(outf); pthread_mutex_unlock(&out_mu); } } }
      c->trials+=LANES;
      if((base & 0xfffff)==0){ uint64_t bb=atomic_load(&best_n); if(atomic_load(&stop_flag) || (bb!=UINT64_MAX && g > (bb>>24))){ aborted=1; break; } }
    }
    if(aborted) { c->overshoot++; break; }
  }
  atomic_fetch_sub(&live_threads,1);
  return NULL;
}
static void selftest(void){
  /* kernel check: compare fast key against compress31 for random blocks */
  uint64_t r2=7; for(int t=0;t<2000;t++){ uint32_t m[16]; for(int i=0;i<16;i++) m[i]=(uint32_t)sm(&r2);
    uint32_t a=IV[0],b=IV[1],cc=IV[2],d=IV[3],e=IV[4],f=IV[5],g=IV[6],h=IV[7];
    for(int s=0;s<15;s++){ uint32_t T1=h+BS1(e)+IF(e,f,g)+K[s]+m[s]; uint32_t T2=BS0(a)+MAJ(a,b,cc); h=g; g=f; f=e; e=d+T1; d=cc; cc=b; b=a; a=T1+T2; }
    const uint32_t m16=s1(m[14])+m[9]+s0(m[1])+m[0], m18=s1(m16)+m[11]+s0(m[3])+m[2], m20=s1(m18)+m[13]+s0(m[5])+m[4];
    const uint32_t c17=m[10]+s0(m[2])+m[1], c19=m[12]+s0(m[4])+m[3], c21=m[14]+s0(m[6])+m[5], c22=s1(m20)+s0(m[7])+m[6];
    const uint32_t c23=m16+s0(m[8])+m[7], c24=s0(m[9])+m[8], c25=m18+s0(m[10])+m[9], c26=s0(m[11])+m[10];
    const uint32_t c27=m20+s0(m[12])+m[11], c28=s0(m[13])+m[12], c29=s0(m[14])+m[13], c30=m[14];
    uint32_t x=m[15];
    uint32_t w17=s1(x)+c17, w19=s1(w17)+c19, w21=s1(w19)+c21, w22=c22+x, w23=s1(w21)+c23, w24=s1(w22)+w17+c24;
    uint32_t w25=s1(w23)+c25, w26=s1(w24)+w19+c26, w27=s1(w25)+c27, w28=s1(w26)+w21+c28, w29=s1(w27)+w22+c29, w30=s1(w28)+w23+s0(x)+c30;
    uint32_t A=a,B=b,C=cc,D=d,E=e,F=f,G=g,H=h,T1,T2;
    RND(x,K[15]) RND(m16,K[16]) RND(w17,K[17]) RND(m18,K[18]) RND(w19,K[19]) RND(m20,K[20]) RND(w21,K[21]) RND(w22,K[22])
    RND(w23,K[23]) RND(w24,K[24]) RND(w25,K[25]) RND(w26,K[26]) RND(w27,K[27]) RND(w28,K[28]) RND(w29,K[29]) RND(w30,K[30])
    uint32_t ref[8]; compress31(IV,m,ref); if(ref[0]!=IV[0]+A){fprintf(stderr,"KERNEL MISMATCH\n");exit(3);} }
  fprintf(stderr,"kernel check OK\n");
}

int main(int argc,char**argv){
  int nth=argc>1?atoi(argv[1]):1; time_limit=argc>2?atof(argv[2]):10; seed_base=argc>3?strtoull(argv[3],0,16):0x7231a5ed2026u;
  const char*outp=argc>4?argv[4]:"collisions.txt";
  outf=stderr; build_s1inv(); build_table(); selftest();
  if(time_limit<=0) return 0;
  outf=fopen(outp,"a");
  pthread_t th[64]; struct timespec t0,t1; clock_gettime(CLOCK_MONOTONIC,&t0);
  NTH=nth;
  for(int i=0;i<nth;i++) pthread_create(&th[i],0,worker,(void*)(intptr_t)i);
  double last=0;
  while(1){ sleep(1); clock_gettime(CLOCK_MONOTONIC,&t1); double el=(t1.tv_sec-t0.tv_sec)+(t1.tv_nsec-t0.tv_nsec)*1e-9;
    int fin = el>=time_limit || access("STOP",F_OK)==0 || (el>2 && atomic_load(&live_threads)==0);
    if(el-last>=30 || fin){ last=el; ctr_t s={0}; for(int i=0;i<nth;i++){ s.trials+=ctrs[i].trials; s.keyhits+=ctrs[i].keyhits; s.recs+=ctrs[i].recs; s.v6+=ctrs[i].v6; s.joint+=ctrs[i].joint; s.both+=ctrs[i].both; s.comp_try+=ctrs[i].comp_try; s.comp_ok+=ctrs[i].comp_ok; s.coll+=ctrs[i].coll; }
      printf("t=%.0f trials=%llu (2^%.3f) rate=%.3e/s keyhits=%llu rechits=%llu v6=%llu joint=%llu both=%llu comp=%llu/%llu coll=%llu\n",el,
        (unsigned long long)s.trials, s.trials? __builtin_log2((double)s.trials):0.0, s.trials/el,(unsigned long long)s.keyhits,(unsigned long long)s.recs,(unsigned long long)s.v6,(unsigned long long)s.joint,(unsigned long long)s.both,(unsigned long long)s.comp_ok,(unsigned long long)s.comp_try,(unsigned long long)s.coll);
      fflush(stdout); }
    if(fin) break; }
  atomic_store(&stop_flag,1); for(int i=0;i<nth;i++) pthread_join(th[i],0);
  ctr_t s={0}; for(int i=0;i<nth;i++){ s.trials+=ctrs[i].trials; s.keyhits+=ctrs[i].keyhits; s.recs+=ctrs[i].recs; s.v6+=ctrs[i].v6; s.joint+=ctrs[i].joint; s.both+=ctrs[i].both; s.comp_try+=ctrs[i].comp_try; s.comp_ok+=ctrs[i].comp_ok; s.coll+=ctrs[i].coll; }
  { uint64_t i13=0,i15=0,ov=0,bm=0,gr=0; for(int i=0;i<nth;i++){i13+=ctrs[i].it13; i15+=ctrs[i].it15; ov+=ctrs[i].overshoot; bm+=ctrs[i].bmhits; gr+=ctrs[i].groups;} uint64_t bn=atomic_load(&best_n);
    printf("DET best_n=%llu it13=%llu it15=%llu aborted_groups=%llu bitmap_hits=%llu groups=%llu\n",(unsigned long long)bn,(unsigned long long)i13,(unsigned long long)i15,(unsigned long long)ov,(unsigned long long)bm,(unsigned long long)gr);
    for(int i=0;i<nth;i++) printf("THREAD %d trials=%llu\n",i,(unsigned long long)ctrs[i].trials); }
  printf("FINAL trials=%llu keyhits=%llu rechits=%llu v6=%llu joint=%llu both=%llu comp=%llu/%llu coll=%llu\n",(unsigned long long)s.trials,(unsigned long long)s.keyhits,(unsigned long long)s.recs,(unsigned long long)s.v6,(unsigned long long)s.joint,(unsigned long long)s.both,(unsigned long long)s.comp_ok,(unsigned long long)s.comp_try,(unsigned long long)s.coll);
  return 0;
}
```

B.5 `sp_own.h` (S as compiled into K)

```c
/* own starting solution S from z3 (seed 88108363); unused entries 0 */
static const uint32_t SPA_A[35]={0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x1476a232u,0x3b327cc5u,0x38f76ff9u,0x7d9cb534u,0x066f93feu,0x4fdbe6b8u,0xad2e79f6u,0x0327eeccu,0x53a8814fu,0x200b1769u,0xdf4a7a71u,0xcf7d7a3bu,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t SPA_E[35]={0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x1d1fa7ddu,0xadea7be7u,0x4c97cbe5u,0x943b8248u,0x61d553d1u,0xf02293fau,0xaa370c18u,0xf1e5b1ecu,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t SPB_A[35]={0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x1476a232u,0x3b327cc5u,0x38f76ff9u,0x7d9cb534u,0x066f8404u,0x4f5be6b9u,0xbc0e69f3u,0x0327eec8u,0x53a8814fu,0x200b976du,0xdf4a7a71u,0xcf7d7a3bu,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t SPB_E[35]={0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x1d1f97e3u,0xade2fbe6u,0x9c1fcf6cu,0xd93b0a4cu,0x61d553d9u,0xdfa31402u,0xbaf70c10u,0xf1e531e4u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
static const uint32_t S_W[31]={0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x876b73dbu,0xed1499e4u,0x7173c145u,0x0ba5f907u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u,0x00000000u};
```

B.6 `r31sim3.c` (synthetic completion check; charged by its counted replays, Section 16.6)

```c
// sha256-r31 relaxed-W20 first-block search from the published starting solution.
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <time.h>
#include <unistd.h>
#include <stdatomic.h>
#include "sp_own.h"

static const uint32_t K[31]={0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
 0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
 0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
 0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351};
static const uint32_t IV[8]={0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
#define R(x,n) (((x)>>(n))|((x)<<(32-(n))))
#define BS0(x) (R(x,2)^R(x,13)^R(x,22))
#define BS1(x) (R(x,6)^R(x,11)^R(x,25))
#define s0(x) (R(x,7)^R(x,18)^((x)>>3))
#define s1(x) (R(x,17)^R(x,19)^((x)>>10))
#define IF(x,y,z) (((x)&(y))^(~(x)&(z)))
#define MAJ(x,y,z) (((x)&(y))^((x)&(z))^((y)&(z)))
#define D5 0xfffff006u
#define D6 0x002087f1u
#define D7 0x4fefb5fau
#define D8 0x28011100u
#define D9 0x00008004u
#define D18 0xffff7ffcu
#define C6 0x00000ffau
#define C7 0xffdf780fu
#define C8 0xb00fca02u
#define IDX(i) ((i)+4)
#define AA(i) SPA_A[IDX(i)]
#define EA(i) SPA_E[IDX(i)]
#define AB(i) SPB_A[IDX(i)]
#define EB(i) SPB_E[IDX(i)]

typedef struct { uint32_t key, A0, E3, E4, W7, W8; } rec_t;
static rec_t *recs; static int nrec;
static uint64_t *bitmap; /* 2^24 bits on key>>8 */
static uint32_t G16[64]; static int ng16;
static uint32_t s1inv_col[32];

static void compress31(const uint32_t cv[8], const uint32_t m[16], uint32_t out[8]) {
  uint32_t W[31]; for(int t=0;t<16;t++) W[t]=m[t];
  for(int t=16;t<31;t++) W[t]=s1(W[t-2])+W[t-7]+s0(W[t-15])+W[t-16];
  uint32_t a=cv[0],b=cv[1],c=cv[2],d=cv[3],e=cv[4],f=cv[5],g=cv[6],h=cv[7];
  for(int t=0;t<31;t++){ uint32_t T1=h+BS1(e)+IF(e,f,g)+K[t]+W[t]; uint32_t T2=BS0(a)+MAJ(a,b,c);
    h=g; g=f; f=e; e=d+T1; d=c; c=b; b=a; a=T1+T2; }
  out[0]=cv[0]+a; out[1]=cv[1]+b; out[2]=cv[2]+c; out[3]=cv[3]+d; out[4]=cv[4]+e; out[5]=cv[5]+f; out[6]=cv[6]+g; out[7]=cv[7]+h;
}
static void digest(const uint32_t m0[16], const uint32_t m1[16], uint32_t out[8]) {
  uint32_t cv[8], cv2[8], pad[16]={0}; pad[0]=0x80000000u; pad[15]=1024;
  compress31(IV,m0,cv); compress31(cv,m1,cv2); compress31(cv2,pad,out);
}
static uint32_t s1inv(uint32_t y){ uint32_t x=0; for(int k=0;k<32;k++) if(y>>k&1) x^=s1inv_col[k]; return x; }
static void build_s1inv(void){
  uint32_t val[32], comb[32]; for(int i=0;i<32;i++){ uint32_t b=1u<<i; val[i]=s1(b); comb[i]=b; }
  for(int k=0;k<32;k++){ int p=-1; for(int i=k;i<32;i++) if(val[i]>>k&1){p=i;break;}
    if(p<0){fprintf(stderr,"s1 singular\n");exit(1);} uint32_t tv=val[k],tc=comb[k]; val[k]=val[p];comb[k]=comb[p];val[p]=tv;comb[p]=tc;
    for(int i=0;i<32;i++) if(i!=k && (val[i]>>k&1)){ val[i]^=val[k]; comb[i]^=comb[k]; } }
  for(int k=0;k<32;k++) s1inv_col[k]=comb[k];
  for(int t=0;t<1000;t++){ uint32_t y=(uint32_t)(t*2654435761u+12345); if(s1(s1inv(y))!=y){fprintf(stderr,"s1inv bad\n");exit(1);} }
}
static int cmprec(const void*a,const void*b){ uint32_t x=((const rec_t*)a)->key,y=((const rec_t*)b)->key; return x<y?-1:x>y; }
static void build_table(void){
  static uint32_t V7[1024],V8[65536]; int n7=0,n8=0; uint32_t w=0;
  do{ if((uint32_t)(s0(w+D8)-s0(w))==C8) V8[n8++]=w; if((uint32_t)(s0(w+D7)-s0(w))==C7) V7[n7++]=w;
      if((uint32_t)(s1(w+D9)-s1(w))==D18) G16[ng16++]=w; w++; }while(w!=0);
  uint32_t cm4=0,va4=0,cm3=0,va3=0; const char*r4="============0===0=========01===0",*r3="==========================10====";
  for(int k=0;k<32;k++){ uint32_t b=1u<<(31-k); if(r4[k]!='='){cm4|=b; if(r4[k]=='1')va4|=b;} if(r3[k]!='='){cm3|=b; if(r3[k]=='1')va3|=b;} }
  uint32_t lhs7=(EB(7)-EA(7))-(BS1(EB(6))-BS1(EA(6)))-D7, lhs6=(EB(6)-EA(6))-(BS1(EB(5))-BS1(EA(5)))-D6;
  recs=malloc(sizeof(rec_t)*(1<<20)); nrec=0;
  for(int i=0;i<n8;i++){ uint32_t W8=V8[i]; uint32_t E4=EA(8)-AA(4)-BS1(EA(7))-IF(EA(7),EA(6),EA(5))-K[8]-W8;
    if((E4&cm4)!=va4) continue; if((uint32_t)(IF(EB(6),EB(5),E4)-IF(EA(6),EA(5),E4))!=lhs7) continue;
    uint32_t A0=E4-AA(4)+BS0(AA(3))+MAJ(AA(3),AA(2),AA(1));
    for(int j=0;j<n7;j++){ uint32_t W7=V7[j]; uint32_t E3=EA(7)-AA(3)-BS1(EA(6))-IF(EA(6),EA(5),E4)-K[7]-W7;
      if((E3&cm3)!=va3) continue; if((uint32_t)(IF(EB(5),E4,E3)-IF(EA(5),E4,E3))!=lhs6) continue;
      uint32_t Am1=E3-AA(3)+BS0(AA(2))+MAJ(AA(2),AA(1),A0);
      recs[nrec++]=(rec_t){Am1,A0,E3,E4,W7,W8}; } }
  qsort(recs,nrec,sizeof(rec_t),cmprec);
  bitmap=calloc(1<<18,8); for(int i=0;i<nrec;i++){ uint32_t b=recs[i].key>>8; bitmap[b>>6]|=1ull<<(b&63); }
  fprintf(stderr,"V7=%d V8=%d G16=%d records=%d\n",n7,n8,ng16,nrec);
}

typedef struct { uint64_t trials, keyhits, recs, v6, joint, both, comp_try, comp_ok, coll; } ctr_t;
static ctr_t ctrs[64];
static atomic_int stop_flag; static pthread_mutex_t out_mu=PTHREAD_MUTEX_INITIALIZER;
static FILE *outf; static atomic_uint_fast64_t total_coll;

static uint64_t sm(uint64_t *s){ uint64_t z=(*s+=0x9e3779b97f4a7c15ull); z=(z^(z>>30))*0xbf58476d1ce4e5b9ull; z=(z^(z>>27))*0x94d049bb133111ebull; return z^(z>>31); }

/* returns 1 if completion found; fills W[0..15] */
static int complete(uint32_t W[16], uint32_t g, uint64_t *rs){
  uint32_t W14=s1inv(g-W[9]-s0(W[1])-W[0]); W[14]=W14;
  if((uint32_t)(s1(W14)+W[9]+s0(W[1])+W[0])!=g) return 0;
  uint32_t b13=AA(9)+EA(9)+BS1(EA(12))+IF(EA(12),EA(11),EA(10))+K[13];
  uint32_t b13b=AB(9)+EB(9)+BS1(EB(12))+IF(EB(12),EB(11),EB(10))+K[13];
  if(b13!=b13b) return 0;
  for(int t=0;t<(1<<14);t++){
    uint32_t E13=((uint32_t)sm(rs) & ~0x10c08000u) | 0x00408000u; uint32_t W13=E13-b13;
    uint32_t A13=E13-AA(9)+BS0(AA(12))+MAJ(AA(12),AA(11),AA(10));
    uint32_t A13b=E13-AB(9)+BS0(AB(12))+MAJ(AB(12),AB(11),AB(10)); if(A13!=A13b) return 0;
    uint32_t E14=AA(10)+EA(10)+BS1(E13)+IF(E13,EA(12),EA(11))+K[14]+W14;
    uint32_t E14b=AB(10)+EB(10)+BS1(E13)+IF(E13,EB(12),EB(11))+K[14]+W14;
    if((uint32_t)(E14b-E14)!=0x8004u) continue;
    uint32_t A14=E14-AA(10)+BS0(A13)+MAJ(A13,AA(12),AA(11)), A14b=E14b-AB(10)+BS0(A13)+MAJ(A13,AB(12),AB(11));
    if(A14!=A14b) continue;
    uint32_t f15=AA(11)+EA(11)+BS1(E14)+IF(E14,E13,EA(12))+K[15], f15b=AB(11)+EB(11)+BS1(E14b)+IF(E14b,E13,EB(12))+K[15];
    if(f15!=f15b) continue;
    for(int u=0;u<(1<<8);u++){
      uint32_t E15=((uint32_t)sm(rs) & ~0x00008004u) | 0x00000004u; uint32_t W15=E15-f15;
      uint32_t E16=AA(12)+EA(12)+BS1(E15)+IF(E15,E14,E13)+K[16]+g, E16b=AB(12)+EB(12)+BS1(E15)+IF(E15,E14b,E13)+K[16]+g+D9;
      if(E16!=E16b) continue;
      uint32_t A15=E15-AA(11)+BS0(A14)+MAJ(A14,A13,AA(12));
      uint32_t f17=A13+E13+BS1(E16)+IF(E16,E15,E14), f17b=A13+E13+BS1(E16)+IF(E16,E15,E14b); (void)A15;
      if(f17!=f17b) continue;
      W[13]=W13; W[15]=W15; return 1; } }
  return 0;
}

static void process_hit(int tid, const uint32_t m0[16], uint64_t *rs, int verbose){
  ctr_t *c=&ctrs[tid]; uint32_t cv[8]; compress31(IV,m0,cv);
  int lo=0,hi=nrec; while(lo<hi){int mid=(lo+hi)/2; if(recs[mid].key<cv[0]) lo=mid+1; else hi=mid;}
  if(lo>=nrec || recs[lo].key!=cv[0]) return;
  c->keyhits++;
  for(int r=lo;r<nrec && recs[r].key==cv[0];r++){
    const rec_t *q=&recs[r]; c->recs++;
    uint32_t a[35],e[35];
    a[IDX(-1)]=cv[0];a[IDX(-2)]=cv[1];a[IDX(-3)]=cv[2];a[IDX(-4)]=cv[3];e[IDX(-1)]=cv[4];e[IDX(-2)]=cv[5];e[IDX(-3)]=cv[6];e[IDX(-4)]=cv[7];
    a[IDX(0)]=q->A0; for(int i=1;i<=12;i++) a[IDX(i)]=AA(i); e[IDX(3)]=q->E3; e[IDX(4)]=q->E4; for(int i=5;i<=12;i++) e[IDX(i)]=EA(i);
#define Ax(i) a[IDX(i)]
#define Ex(i) e[IDX(i)]
    Ex(0)=Ax(0)+Ax(-4)-BS0(Ax(-1))-MAJ(Ax(-1),Ax(-2),Ax(-3));
    Ex(1)=Ax(1)+Ax(-3)-BS0(Ax(0))-MAJ(Ax(0),Ax(-1),Ax(-2));
    Ex(2)=Ax(2)+Ax(-2)-BS0(Ax(1))-MAJ(Ax(1),Ax(0),Ax(-1));
    uint32_t W[16]; for(int i=0;i<=6;i++) W[i]=Ex(i)-Ax(i-4)-Ex(i-4)-BS1(Ex(i-1))-IF(Ex(i-1),Ex(i-2),Ex(i-3))-K[i];
    W[7]=q->W7; W[8]=q->W8; for(int i=9;i<=12;i++) W[i]=S_W[i]; W[13]=W[14]=W[15]=0;
    int v6=((uint32_t)(s0(W[6]+D6)-s0(W[6]))==C6);
    uint32_t tgt=0u-(uint32_t)(s0(W[5]+D5)-s0(W[5])); uint32_t c18=W[11]+s0(W[3])+W[2];
    int gsel=-1; for(int k=0;k<ng16;k++){ uint32_t w18=s1(G16[k])+c18; if((uint32_t)(s1(w18+D18)-s1(w18))==tgt){gsel=k;break;} }
    if(v6) c->v6++;
    if(gsel<0) continue;
    c->joint++; if(v6) c->both++;
    c->comp_try++;
    uint32_t Wc[16]; memcpy(Wc,W,sizeof W);
    if(!complete(Wc,G16[gsel],rs)) { if(verbose) fprintf(stderr,"completion failed\n"); continue; }
    c->comp_ok++;
    if(!v6) continue;
    uint32_t Wb[16]; memcpy(Wb,Wc,sizeof Wc); Wb[5]+=D5; Wb[6]+=D6; Wb[7]+=D7; Wb[8]+=D8; Wb[9]+=D9;
    uint32_t h1[8],h2[8]; digest(m0,Wc,h1); digest(m0,Wb,h2);
    if(memcmp(h1,h2,32)==0 && memcmp(Wc,Wb,64)!=0){
      c->coll++; atomic_fetch_add(&total_coll,1);
      pthread_mutex_lock(&out_mu);
      fprintf(outf,"COLLISION tid=%d\nM0 ",tid); for(int i=0;i<16;i++) fprintf(outf,"%08x",m0[i]);
      fprintf(outf,"\nM1 "); for(int i=0;i<16;i++) fprintf(outf,"%08x",Wc[i]);
      fprintf(outf,"\nM1b "); for(int i=0;i<16;i++) fprintf(outf,"%08x",Wb[i]);
      fprintf(outf,"\nDIGEST "); for(int i=0;i<8;i++) fprintf(outf,"%08x",h1[i]); fprintf(outf,"\n"); fflush(outf);
      pthread_mutex_unlock(&out_mu);
    } else if(verbose) fprintf(stderr,"digest mismatch\n");
  }
}

static uint64_t seed_base; static double time_limit;

static void process_sim(int tid, const rec_t *q, const uint32_t cv[8], uint64_t *rs){
  ctr_t *c=&ctrs[tid]; c->recs++;
  uint32_t a[35],e[35];
  a[IDX(-1)]=cv[0];a[IDX(-2)]=cv[1];a[IDX(-3)]=cv[2];a[IDX(-4)]=cv[3];e[IDX(-1)]=cv[4];e[IDX(-2)]=cv[5];e[IDX(-3)]=cv[6];e[IDX(-4)]=cv[7];
  a[IDX(0)]=q->A0; for(int i=1;i<=12;i++) a[IDX(i)]=AA(i); e[IDX(3)]=q->E3; e[IDX(4)]=q->E4; for(int i=5;i<=12;i++) e[IDX(i)]=EA(i);
  Ex(0)=Ax(0)+Ax(-4)-BS0(Ax(-1))-MAJ(Ax(-1),Ax(-2),Ax(-3));
  Ex(1)=Ax(1)+Ax(-3)-BS0(Ax(0))-MAJ(Ax(0),Ax(-1),Ax(-2));
  Ex(2)=Ax(2)+Ax(-2)-BS0(Ax(1))-MAJ(Ax(1),Ax(0),Ax(-1));
  uint32_t W[16]; for(int i=0;i<=6;i++) W[i]=Ex(i)-Ax(i-4)-Ex(i-4)-BS1(Ex(i-1))-IF(Ex(i-1),Ex(i-2),Ex(i-3))-K[i];
  W[7]=q->W7; W[8]=q->W8; for(int i=9;i<=12;i++) W[i]=S_W[i]; W[13]=W[14]=W[15]=0;
  int v6=((uint32_t)(s0(W[6]+D6)-s0(W[6]))==C6);
  uint32_t tgt=0u-(uint32_t)(s0(W[5]+D5)-s0(W[5])); uint32_t c18=W[11]+s0(W[3])+W[2];
  int gsel=-1; for(int k=0;k<ng16;k++){ uint32_t w18=s1(G16[k])+c18; if((uint32_t)(s1(w18+D18)-s1(w18))==tgt){gsel=k;break;} }
  if(v6) c->v6++;
  if(gsel<0) return;
  c->joint++; if(v6) c->both++;
  c->comp_try++;
  uint32_t Wc[16]; memcpy(Wc,W,sizeof W);
  if(!complete(Wc,G16[gsel],rs)) return;
  c->comp_ok++;
  if(!v6) return;
  /* full check of the second block from this (synthetic) chaining value */
  uint32_t Wb[16]; memcpy(Wb,Wc,sizeof Wc); Wb[5]+=D5; Wb[6]+=D6; Wb[7]+=D7; Wb[8]+=D8; Wb[9]+=D9;
  uint32_t o1[8],o2[8]; compress31(cv,Wc,o1); compress31(cv,Wb,o2);
  if(memcmp(o1,o2,32)==0) c->coll++;
}
static void *simworker(void *arg){
  int tid=(int)(intptr_t)arg; uint64_t rs=seed_base^(0x51ed27ull*(uint64_t)(tid+1)); ctr_t *c=&ctrs[tid];
  while(!atomic_load(&stop_flag)){
    for(int it=0;it<(1<<16);it++){
      uint64_t r=sm(&rs); const rec_t *q=&recs[(uint32_t)(r%(uint64_t)nrec)];
      uint32_t cv[8]; cv[0]=q->key; uint64_t r2=sm(&rs), r3=sm(&rs), r4=sm(&rs);
      cv[1]=(uint32_t)(r>>32); cv[2]=(uint32_t)r2; cv[3]=(uint32_t)(r2>>32); cv[4]=(uint32_t)r3; cv[5]=(uint32_t)(r3>>32); cv[6]=(uint32_t)r4; cv[7]=(uint32_t)(r4>>32);
      process_sim(tid,q,cv,&rs); }
    c->trials+=1<<16; }
  return NULL;
}

#define LANES 8
static void *worker(void *arg){
  int tid=(int)(intptr_t)arg; uint64_t rs=seed_base^(0x1000193ull*(uint64_t)(tid+1)); ctr_t *c=&ctrs[tid];
  uint32_t m[16];
  while(!atomic_load(&stop_flag)){
    for(int i=0;i<15;i++) m[i]=(uint32_t)sm(&rs);
    uint32_t a=IV[0],b=IV[1],cc=IV[2],d=IV[3],e=IV[4],f=IV[5],g=IV[6],h=IV[7];
    for(int t=0;t<15;t++){ uint32_t T1=h+BS1(e)+IF(e,f,g)+K[t]+m[t]; uint32_t T2=BS0(a)+MAJ(a,b,cc); h=g; g=f; f=e; e=d+T1; d=cc; cc=b; b=a; a=T1+T2; }
    const uint32_t m16=s1(m[14])+m[9]+s0(m[1])+m[0], m18=s1(m16)+m[11]+s0(m[3])+m[2], m20=s1(m18)+m[13]+s0(m[5])+m[4];
    const uint32_t c17=m[10]+s0(m[2])+m[1], c19=m[12]+s0(m[4])+m[3], c21=m[14]+s0(m[6])+m[5], c22=s1(m20)+s0(m[7])+m[6];
    const uint32_t c23=m16+s0(m[8])+m[7], c24=s0(m[9])+m[8], c25=m18+s0(m[10])+m[9], c26=s0(m[11])+m[10];
    const uint32_t c27=m20+s0(m[12])+m[11], c28=s0(m[13])+m[12], c29=s0(m[14])+m[13], c30=m[14];
    for(uint32_t base=0; base < (1u<<24); base+=LANES){
      uint32_t key[LANES];
      for(int j=0;j<LANES;j++){
        uint32_t x=base+(uint32_t)j;
        uint32_t w17=s1(x)+c17, w19=s1(w17)+c19, w21=s1(w19)+c21, w22=c22+x, w23=s1(w21)+c23, w24=s1(w22)+w17+c24;
        uint32_t w25=s1(w23)+c25, w26=s1(w24)+w19+c26, w27=s1(w25)+c27, w28=s1(w26)+w21+c28, w29=s1(w27)+w22+c29, w30=s1(w28)+w23+s0(x)+c30;
        uint32_t A=a,B=b,C=cc,D=d,E=e,F=f,G=g,H=h,T1,T2;
#define RND(w,k) T1=H+BS1(E)+IF(E,F,G)+(k)+(w); T2=BS0(A)+MAJ(A,B,C); H=G; G=F; F=E; E=D+T1; D=C; C=B; B=A; A=T1+T2;
        RND(x,K[15]) RND(m16,K[16]) RND(w17,K[17]) RND(m18,K[18]) RND(w19,K[19]) RND(m20,K[20]) RND(w21,K[21]) RND(w22,K[22])
        RND(w23,K[23]) RND(w24,K[24]) RND(w25,K[25]) RND(w26,K[26]) RND(w27,K[27]) RND(w28,K[28]) RND(w29,K[29]) RND(w30,K[30])
        key[j]=IV[0]+A;
      }
      for(int j=0;j<LANES;j++){ uint32_t bi=key[j]>>8; if(bitmap[bi>>6]>>(bi&63)&1){ uint32_t mm[16]; memcpy(mm,m,60); mm[15]=base+(uint32_t)j; process_hit(tid,mm,&rs,0);} }
      c->trials+=LANES;
      if((base & 0xfffff)==0 && atomic_load(&stop_flag)) break;
    }
  }
  return NULL;
}

static void selftest(void){
  /* kernel check: compare fast key against compress31 for random blocks */
  uint64_t r2=7; for(int t=0;t<2000;t++){ uint32_t m[16]; for(int i=0;i<16;i++) m[i]=(uint32_t)sm(&r2);
    uint32_t a=IV[0],b=IV[1],cc=IV[2],d=IV[3],e=IV[4],f=IV[5],g=IV[6],h=IV[7];
    for(int s=0;s<15;s++){ uint32_t T1=h+BS1(e)+IF(e,f,g)+K[s]+m[s]; uint32_t T2=BS0(a)+MAJ(a,b,cc); h=g; g=f; f=e; e=d+T1; d=cc; cc=b; b=a; a=T1+T2; }
    const uint32_t m16=s1(m[14])+m[9]+s0(m[1])+m[0], m18=s1(m16)+m[11]+s0(m[3])+m[2], m20=s1(m18)+m[13]+s0(m[5])+m[4];
    const uint32_t c17=m[10]+s0(m[2])+m[1], c19=m[12]+s0(m[4])+m[3], c21=m[14]+s0(m[6])+m[5], c22=s1(m20)+s0(m[7])+m[6];
    const uint32_t c23=m16+s0(m[8])+m[7], c24=s0(m[9])+m[8], c25=m18+s0(m[10])+m[9], c26=s0(m[11])+m[10];
    const uint32_t c27=m20+s0(m[12])+m[11], c28=s0(m[13])+m[12], c29=s0(m[14])+m[13], c30=m[14];
    uint32_t x=m[15];
    uint32_t w17=s1(x)+c17, w19=s1(w17)+c19, w21=s1(w19)+c21, w22=c22+x, w23=s1(w21)+c23, w24=s1(w22)+w17+c24;
    uint32_t w25=s1(w23)+c25, w26=s1(w24)+w19+c26, w27=s1(w25)+c27, w28=s1(w26)+w21+c28, w29=s1(w27)+w22+c29, w30=s1(w28)+w23+s0(x)+c30;
    uint32_t A=a,B=b,C=cc,D=d,E=e,F=f,G=g,H=h,T1,T2;
    RND(x,K[15]) RND(m16,K[16]) RND(w17,K[17]) RND(m18,K[18]) RND(w19,K[19]) RND(m20,K[20]) RND(w21,K[21]) RND(w22,K[22])
    RND(w23,K[23]) RND(w24,K[24]) RND(w25,K[25]) RND(w26,K[26]) RND(w27,K[27]) RND(w28,K[28]) RND(w29,K[29]) RND(w30,K[30])
    uint32_t ref[8]; compress31(IV,m,ref); if(ref[0]!=IV[0]+A){fprintf(stderr,"KERNEL MISMATCH\n");exit(3);} }
  fprintf(stderr,"kernel check OK\n");
}

int main(int argc,char**argv){
  int nth=argc>1?atoi(argv[1]):1; time_limit=argc>2?atof(argv[2]):10; seed_base=argc>3?strtoull(argv[3],0,16):0x7231a5ed2026u;
  const char*outp=argc>4?argv[4]:"collisions.txt";
  outf=stderr; build_s1inv(); build_table(); selftest();
  if(time_limit<=0) return 0;
  outf=fopen(outp,"a");
  pthread_t th[64]; struct timespec t0,t1; clock_gettime(CLOCK_MONOTONIC,&t0);
  int simmode=argc>5 && strcmp(argv[5],"sim")==0;
  for(int i=0;i<nth;i++) pthread_create(&th[i],0,simmode?simworker:worker,(void*)(intptr_t)i);
  double last=0;
  while(1){ sleep(1); clock_gettime(CLOCK_MONOTONIC,&t1); double el=(t1.tv_sec-t0.tv_sec)+(t1.tv_nsec-t0.tv_nsec)*1e-9;
    int fin = el>=time_limit || access("STOP",F_OK)==0;
    if(el-last>=30 || fin){ last=el; ctr_t s={0}; for(int i=0;i<nth;i++){ s.trials+=ctrs[i].trials; s.keyhits+=ctrs[i].keyhits; s.recs+=ctrs[i].recs; s.v6+=ctrs[i].v6; s.joint+=ctrs[i].joint; s.both+=ctrs[i].both; s.comp_try+=ctrs[i].comp_try; s.comp_ok+=ctrs[i].comp_ok; s.coll+=ctrs[i].coll; }
      printf("t=%.0f trials=%llu (2^%.3f) rate=%.3e/s keyhits=%llu rechits=%llu v6=%llu joint=%llu both=%llu comp=%llu/%llu coll=%llu\n",el,
        (unsigned long long)s.trials, s.trials? __builtin_log2((double)s.trials):0.0, s.trials/el,(unsigned long long)s.keyhits,(unsigned long long)s.recs,(unsigned long long)s.v6,(unsigned long long)s.joint,(unsigned long long)s.both,(unsigned long long)s.comp_ok,(unsigned long long)s.comp_try,(unsigned long long)s.coll);
      fflush(stdout); }
    if(fin) break; }
  atomic_store(&stop_flag,1); for(int i=0;i<nth;i++) pthread_join(th[i],0);
  ctr_t s={0}; for(int i=0;i<nth;i++){ s.trials+=ctrs[i].trials; s.keyhits+=ctrs[i].keyhits; s.recs+=ctrs[i].recs; s.v6+=ctrs[i].v6; s.joint+=ctrs[i].joint; s.both+=ctrs[i].both; s.comp_try+=ctrs[i].comp_try; s.comp_ok+=ctrs[i].comp_ok; s.coll+=ctrs[i].coll; }
  printf("FINAL trials=%llu keyhits=%llu rechits=%llu v6=%llu joint=%llu both=%llu comp=%llu/%llu coll=%llu\n",(unsigned long long)s.trials,(unsigned long long)s.keyhits,(unsigned long long)s.recs,(unsigned long long)s.v6,(unsigned long long)s.joint,(unsigned long long)s.both,(unsigned long long)s.comp_ok,(unsigned long long)s.comp_try,(unsigned long long)s.coll);
  return 0;
}
```

## Appendix C. Price scripts and the counted programs

C.1 `a64ops.py` (per-form costing of AArch64 instructions)

```python
"""Primitive-operation cost of AArch64 instructions under the collision-frontier-v5 primitive list.

v5 primitives: 256-bit load/store, add/sub mod 2^256, AND/OR/XOR/NOT, shift/rotate, comparison,
conditional branch, uniform random word. Every program datum sits in its own 256-bit word.
Rules (per instruction):
  - every add/sub/neg and every left shift is followed by one AND to reduce mod 2^32 or 2^64 (+1 mask);
  - a shifted register operand costs +1 shift (+1 mask when it is lsl), an extended one +1 (uxt) or +3 (sxt);
  - a memory address costs 1 per added term (+1 scaled index, +1 extend, +1 writeback); pairs pay 2 addresses;
  - multiply, multiply-add, FP arithmetic, compare, conversion and SIMD multiply/FP cost 400 (shift-and-add
    emulation of a 64x64 or 53x53 product is at most 64 iterations of 5 primitives);
  - integer divide, FP divide and square root cost 1024 (restoring division, 64 iterations of at most 8 plus
    normalisation);
  - anything not recognised costs 8 and is reported.
"""
import collections
import json
import re
import sys

HEAVY_DIV = re.compile(r'^(udiv|sdiv|fdiv|fsqrt|frecpe|frsqrte|frecps|frsqrts|frecpx)$')
HEAVY_MUL = re.compile(r'^(mul|madd|msub|mneg|smull|umull|smaddl|umaddl|smsubl|umsubl|smnegl|umnegl|smulh|umulh|'
                       r'pmull2?|smull2?|umull2?|smlal2?|umlal2?|smlsl2?|umlsl2?|sqdmull2?|sqdmulh|sqrdmulh|mla|mls)$')
HEAVY_FP = re.compile(r'^(fadd|fsub|fmul|fnmul|fmadd|fmsub|fnmadd|fnmsub|fmla|fmls|fmulx|fabd|fmax|fmin|fmaxnm|'
                      r'fminnm|fmaxv|fminv|fmaxnmv|fminnmv|faddp|fcmp|fcmpe|fccmp|fccmpe|fcmeq|fcmge|fcmgt|fcmle|'
                      r'fcmlt|facge|facgt|fcvt[a-z]*|scvtf|ucvtf|frint[a-z]*|fjcvtzs|bfcvt[a-z0-9]*)$')
SIGNED_COND = {'lt', 'le', 'gt', 'ge', 'mi', 'pl', 'vs', 'vc'}
VEC = re.compile(r'\bv\d+\.(16b|8b|8h|4h|4s|2s|2d|1d|1q|b|h|s|d)\b')
NOPS = {'nop', 'hint', 'bti', 'paciasp', 'autiasp', 'pacibsp', 'autibsp', 'pacia', 'autia', 'pacib', 'autib',
        'paciza', 'autiza', 'xpaclri', 'xpaci', 'dmb', 'dsb', 'isb', 'prfm', 'prfum', 'yield', 'csdb', 'sb',
        'pssbb', 'ssbb', 'clrex', 'esb', 'retaa', 'retab'}


def split_ops(s):
    out, depth, cur = [], 0, ''
    for ch in s:
        if ch in '[{':
            depth += 1
        elif ch in ']}':
            depth -= 1
        if ch == ',' and depth == 0:
            out.append(cur.strip())
            cur = ''
        else:
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out


def addr_cost(ops):
    joined = ', '.join(ops)
    m = re.search(r'\[([^\]]*)\](!?)', joined)
    if not m:
        return 1 if re.search(r'0x[0-9a-f]+', joined) else 0   # literal (pc-relative)
    inner = [t.strip() for t in m.group(1).split(',')]
    c = 0
    if len(inner) >= 2:
        c += 1                                       # base + offset / base + index
        if len(inner) >= 3:
            ext = inner[2]
            if ext.startswith('lsl'):
                c += 1
            elif ext.startswith('sxt'):
                c += 3 + (1 if '#' in ext else 0)
            elif ext.startswith('uxt'):
                c += 1 + (1 if '#' in ext else 0)
    if m.group(2) == '!':
        c += 1                                       # pre-index writeback
    tail = joined[m.end():].strip()
    if tail.startswith(','):
        c += 2                                       # post-index writeback (add + mask)
    return c


def operand_mod(ops):
    """Cost of a shifted or extended last operand."""
    if not ops:
        return 0
    last = ops[-1]
    if re.match(r'^(lsl|lsr|asr|ror)\b', last):
        k = last.split()[0]
        return {'lsl': 2, 'lsr': 1, 'asr': 4, 'ror': 4}[k]
    if re.match(r'^(uxt[bhwx])', last):
        return 1 + (2 if '#' in last else 0)
    if re.match(r'^(sxt[bhwx])', last):
        return 3 + (2 if '#' in last else 0)
    return 0


def cost(mn, ops):
    """Return (operations, class): class is 'div', 'heavy', 'ordinary' or 'unknown'."""
    base = mn.split('.')[0]
    cond = mn.split('.')[1] if mn.startswith('b.') else None
    vec = any(VEC.search(o) for o in ops) or ('.' in mn and cond is None)
    if HEAVY_DIV.match(base):
        return 1024, 'div'
    if HEAVY_MUL.match(base) or HEAVY_FP.match(base):
        return 400, 'heavy'
    if vec and base in ('fabs', 'fneg', 'frecpe', 'frsqrte'):
        return 400, 'heavy'
    if base in NOPS:
        return 1, 'ordinary'
    # loads and stores
    if re.match(r'^(ldr|ldur|ldtr|ldapr|ldapur)$', base):
        sz = ops[0][0] if ops else 'x'
        return (1 if sz in 'xqdsbh' and sz != 'w' else 2) + addr_cost(ops[1:]), 'ordinary'
    if re.match(r'^(ldrb|ldrh|ldurb|ldurh|ldtrb|ldtrh|ldaprb|ldaprh)$', base):
        return 2 + addr_cost(ops[1:]), 'ordinary'
    if re.match(r'^(ldrsb|ldrsh|ldrsw|ldursb|ldursh|ldursw)$', base):
        return 4 + addr_cost(ops[1:]), 'ordinary'
    if re.match(r'^(str|stur|strb|strh|sturb|sturh|sttr|stlur|stlurb|stlurh)$', base):
        return 1 + addr_cost(ops[1:]), 'ordinary'
    if re.match(r'^(ldp|stp|ldnp|stnp|ldpsw)$', base):
        return 2 + 1 + addr_cost(ops[2:]) + (4 if base == 'ldpsw' else 0), 'ordinary'
    if re.match(r'^(ld[1-4]r?|st[1-4])$', base):
        n = max(1, len(re.findall(r'v\d+', ops[0]) if ops else []))
        return n * 16 + addr_cost(ops[1:]), 'ordinary'   # element-wise structure loads, charged as shuffles
    if re.match(r'^(ldxr|ldaxr|stxr|stlxr|ldar|stlr|ldxrb|ldaxrb|stxrb|stlxrb|ldxrh|ldaxrh|stxrh|stlxrh|ldarb|'
                 r'stlrb|ldarh|stlrh|ldxp|ldaxp|stxp|stlxp|cas|casa|casl|casal|casb|casab|caslb|casalb|cash|casah|'
                 r'caslh|casalh|casp|caspa|caspl|caspal|ldadd|ldadda|ldaddl|ldaddal|ldaddb|ldaddalb|ldaddh|ldaddalh|'
                 r'ldclr|ldclral|ldclra|ldclrl|ldset|ldsetal|ldseta|ldsetl|ldeor|ldeoral|swp|swpa|swpl|swpal|swpb|'
                 r'swpalb|swph|swpalh|ldaddlb|ldaddab|ldsetalb|ldclralb|stadd|staddl|stset|stclr|stsetl|stclrl)$',
                 base):
        return 6 + addr_cost(ops[1:]), 'ordinary'
    if vec:
        if re.match(r'^(and|orr|eor|bic|orn|not|mvn|bsl|bit|bif|mov|movi|mvni)$', base):
            return 1, 'ordinary'
        if re.match(r'^(add|sub|cmeq|cmhi|cmhs|cmge|cmgt|cmle|cmlt|cmtst|neg|abs|umax|umin|smax|smin|addp|uaddl2?|'
                     r'uaddw2?|usubl2?|ushr|sshr|shl|ushl|sshl|ushll2?|sshll2?|xtn2?|uqxtn2?|sqxtn2?|shrn2?|uzp[12]|zip[12]|'
                     r'trn[12]|ext|uhadd|urhadd|uqadd|uqsub|sqadd|sqsub|sli|sri|usra|ssra|dup|fneg|fabs|fmov|cnt|rev64|rev32|rev16)$',
                     base):
            return 16, 'ordinary'
        return 16, 'ordinary'   # remaining SIMD forms (tbl, ins, umov, addv, ...) charged as shuffles
    w = bool(ops) and ops[0].startswith('w')
    if base in ('add', 'adds', 'sub', 'subs'):
        return 2 + operand_mod(ops), 'ordinary'
    if base in ('cmp', 'cmn'):
        return 2 + operand_mod(ops), 'ordinary'
    if base in ('neg', 'negs'):
        return 2 + operand_mod(ops), 'ordinary'
    if base in ('adc', 'adcs', 'sbc', 'sbcs', 'ngc', 'ngcs'):
        return 4, 'ordinary'
    if base in ('and', 'ands', 'orr', 'eor', 'tst'):
        return 1 + operand_mod(ops), 'ordinary'
    if base in ('bic', 'bics', 'orn', 'eon', 'mvn'):
        return 3 + operand_mod(ops), 'ordinary'
    if base in ('mov', 'movz', 'movn'):
        return 1 + (1 if base == 'movn' else 0), 'ordinary'
    if base == 'movk':
        return 3, 'ordinary'
    if base in ('adr', 'adrp'):
        return 1, 'ordinary'
    if base in ('lsr',):
        return 1, 'ordinary'
    if base in ('lsl',):
        return 2, 'ordinary'
    if base in ('asr', 'ror'):
        return 4, 'ordinary'
    if base in ('ubfx', 'uxtb', 'uxth', 'uxtw'):
        return 2, 'ordinary'
    if base in ('ubfiz', 'ubfm'):
        return 3, 'ordinary'
    if base in ('sbfx', 'sbfiz', 'sbfm', 'sxtb', 'sxth', 'sxtw'):
        return 4, 'ordinary'
    if base in ('bfi', 'bfxil', 'bfm', 'bfc'):
        return 5, 'ordinary'
    if base == 'extr':
        return 4, 'ordinary'
    if base in ('csel', 'fcsel'):
        return 3, 'ordinary'
    if base in ('cset', 'csetm'):
        return 2, 'ordinary'
    if base in ('csinc', 'csinv', 'csneg', 'cinc', 'cinv', 'cneg'):
        return 4, 'ordinary'
    if base in ('ccmp', 'ccmn'):
        return 5, 'ordinary'
    if base in ('clz', 'cls', 'rbit', 'rev', 'rev16', 'rev32', 'cnt', 'ctz', 'abs'):
        return 32, 'ordinary'
    if base == 'b' and cond is None:
        return 1, 'ordinary'
    if cond is not None:
        return 3 if cond in SIGNED_COND else 2, 'ordinary'
    if base in ('bl', 'blr', 'ret', 'blraa', 'blraaz', 'braa', 'braaz'):
        return 3, 'ordinary'
    if base == 'br':
        return 2, 'ordinary'
    if base in ('cbz', 'cbnz'):
        return 2, 'ordinary'
    if base in ('tbz', 'tbnz'):
        return 3, 'ordinary'
    if base in ('fmov',):
        return 1, 'ordinary'
    if base in ('fabs', 'fneg'):
        return 2, 'ordinary'
    return 8, 'unknown'


LINE = re.compile(r'^\s*([0-9a-f]+):\s+(\S+)(?:\s+(.*))?$')


def parse(path, with_addr=False):
    """Parse llvm-objdump -d --no-show-raw-insn output into {function: [(addr, mn, ops)]}."""
    funcs = collections.OrderedDict()
    cur = None
    for line in open(path, errors='replace'):
        line = line.rstrip('\n')
        if line.endswith('>:'):
            cur = line.split('<', 1)[1].rsplit('>', 1)[0]
            funcs.setdefault(cur, [])
            continue
        if cur is None or not line.strip():
            continue
        if with_addr:
            m = LINE.match(line)
            if not m:
                continue
            a, mn, rest = int(m.group(1), 16), m.group(2), m.group(3) or ''
        else:
            parts = line.strip().split(None, 1)
            a, mn, rest = None, parts[0], parts[1] if len(parts) > 1 else ''
        rest = rest.split('//')[0]
        rest = re.sub(r'\s*<[^>]*>\s*$', '', rest).strip()
        funcs[cur].append((a, mn, split_ops(rest) if rest else []))
    return funcs


def summarize(name, insns, weights=None):
    n = tot = heavy = div = unk = 0
    cls_n = collections.Counter()
    unk_mn = collections.Counter()
    form = collections.Counter()
    for i, (a, mn, ops) in enumerate(insns):
        wgt = weights[i] if weights else 1
        c, cls = cost(mn, ops)
        n += wgt
        cls_n[cls] += wgt
        tot += c * wgt
        form[mn.split('.')[0]] += wgt
        if cls == 'unknown':
            unk_mn[mn] += wgt
    ordn = cls_n['ordinary'] + cls_n['unknown']
    ord_ops = tot - 400 * cls_n['heavy'] - 1024 * cls_n['div']
    return dict(name=name, insns=n, heavy=cls_n['heavy'], div=cls_n['div'], unknown=cls_n['unknown'],
                mean_all=round(tot / n, 4) if n else None,
                mean_ordinary=round(ord_ops / ordn, 4) if ordn else None,
                heavy_share=round(cls_n['heavy'] / n, 6) if n else None,
                div_share=round(cls_n['div'] / n, 6) if n else None,
                top_forms=form.most_common(12), unknown_top=unk_mn.most_common(10))


if __name__ == '__main__':
    funcs = parse(sys.argv[1])
    print(json.dumps(summarize('WHOLE-BINARY', [i for v in funcs.values() for i in v])))
```

C.2 `cgmix.py` (dynamic mix from callgrind instruction counts; v6 adds the `r31det3.gcc` entry)

```python
"""Dynamic per-form cost from callgrind --dump-instr=yes --compress-pos=no --compress-strings=no dumps.

usage: cgmix.py BINDIR DUMP [DUMP ...]
Each dump is one interval; prints per-dump and pooled summaries as JSON lines.
Positions of shared objects are object-relative virtual addresses; the z3 executable is non-PIE.
"""
import collections
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a64ops import cost, split_ops  # noqa: E402

OBJ_FILE = {
    '/usr/local/bin/z3': 'z3.elf',
    'r31sim3.lin': 'r31sim3.lin',
    'r31det3.gcc': 'r31det3.gcc',
    'libstdc++.so.6.0.30': 'libstdc++.so.6',
    'libc.so.6': 'libc.so.6',
    'libm.so.6': 'libm.so.6',
    'libgcc_s.so.1': 'libgcc_s.so.1',
    'ld-linux-aarch64.so.1': 'ld-linux-aarch64.so.1',
}


def objkey(ob):
    for k, v in OBJ_FILE.items():
        if ob.endswith(k):
            return v
    return None


def read_dump(path):
    counts = collections.defaultdict(collections.Counter)
    ob, skip = None, False
    for line in open(path):
        if line.startswith('ob='):
            ob = line[3:].strip()
            continue
        if line.startswith('calls='):
            skip = True
            continue
        if line.startswith('0x'):
            if skip:
                skip = False
                continue
            a, c = line.split()[:2]
            counts[ob][int(a, 16)] += int(c)
    return counts


LINE = re.compile(r'^\s*([0-9a-f]+):\s+(\S+)(?:\s+(.*))?$')


def disasm(binpath, wanted):
    out = {}
    p = subprocess.Popen(['xcrun', 'llvm-objdump', '-d', '--no-show-raw-insn', binpath],
                         stdout=subprocess.PIPE, text=True, errors='replace')
    for line in p.stdout:
        m = LINE.match(line)
        if not m:
            continue
        a = int(m.group(1), 16)
        if a not in wanted:
            continue
        rest = (m.group(3) or '').split('//')[0]
        rest = re.sub(r'\s*<[^>]*>\s*$', '', rest).strip()
        out[a] = (m.group(2), split_ops(rest) if rest else [])
    p.wait()
    return out


def main():
    bindir, dumps = sys.argv[1], sys.argv[2:]
    per = [(d, read_dump(d)) for d in dumps]
    wanted = collections.defaultdict(set)
    for _, cnt in per:
        for ob, c in cnt.items():
            k = objkey(ob or '')
            if k:
                wanted[k].update(c)
            if 'z3.elf' in wanted or any(objkey(o or '') == 'z3.elf' for o in cnt):
                wanted['z3.elf'].update(a for a in c if a >= 0x400000)
    dis = {k: disasm(os.path.join(bindir, k), w) for k, w in wanted.items()}
    pooled = collections.defaultdict(collections.Counter)
    rows = []
    for name, cnt in per + [('POOLED', None)]:
        if cnt is None:
            cnt = pooled
        tot_i = tot_ops = 0
        cls = collections.Counter()
        by_obj = collections.Counter()
        unmapped = 0
        forms = collections.Counter()
        for ob, c in cnt.items():
            k = objkey(ob or '')
            for a, n in c.items():
                if name != 'POOLED':
                    pooled[ob][a] += n
                tot_i += n
                by_obj[k or ob] += n
                ins = dis.get(k, {}).get(a) if k else None
                if ins is None and a >= 0x400000 and 'z3.elf' in dis:
                    ins = dis['z3.elf'].get(a)   # callgrind can tag executable code run from a library frame
                if ins is None:
                    unmapped += n
                    cls['unmapped'] += n
                    continue
                o, cl = cost(ins[0], ins[1])
                cls[cl] += n
                tot_ops += o * n
                forms[ins[0]] += n
        mapped = tot_i - unmapped
        ordn = cls['ordinary'] + cls['unknown']
        ord_ops = tot_ops - 400 * cls['heavy'] - 1024 * cls['div']
        rows.append(dict(
            dump=os.path.basename(name), instr=tot_i, unmapped=unmapped,
            heavy_share=cls['heavy'] / mapped, div_share=cls['div'] / mapped, unknown_share=cls['unknown'] / mapped,
            m_dyn=tot_ops / mapped, ord_mean=ord_ops / ordn,
            m_class=5 * (1 - (cls['heavy'] + cls['div']) / mapped) + 400 * cls['heavy'] / mapped + 1024 * cls['div'] / mapped,
            obj_share={str(k): round(v / tot_i, 5) for k, v in by_obj.most_common()},
            top_forms=[(f, round(v / mapped, 4)) for f, v in forms.most_common(10)]))
    for r in rows:
        print(json.dumps(r))


if __name__ == '__main__':
    main()
```

C.3 `swar.py` (SIMD prices by exact emulation on one 256-bit word)

    e5b8ea421d4f9280f5af4a394bfa147df806c1d5f84dc0f750c6e0fbe7aa2602  swar.py

```python
"""SIMD per-form prices by SWAR emulation (alternative to the flat 16 of the v5 table).

A 128-bit register is one datum in one 256-bit word, as the v5 table already assumes for SIMD logic.
Lane-wise forms are priced by the SWAR programs checked in swar_check.py. Forms not listed keep their
v5 price. Scalar forms are unchanged.
"""
import re

import a64ops

SWAR = {'add': 6, 'shl': 2, 'ushr': 2, 'usra': 8, 'eor3': 2, 'bcax': 3, 'bsl': 3, 'bic': 2,
        'and': 1, 'orr': 1, 'eor': 1, 'mov': 1, 'movi': 1, 'dup': 11, 'ins': 4, 'umov': 4}
LANE = re.compile(r'\bv\d+(\.[bhsd])?\[\d+\]')


def cost(mn, ops):
    c, cl = a64ops.cost(mn, ops)
    base = mn.split('.')[0]
    cond = mn.split('.')[1] if mn.startswith('b.') else None
    vec = any(a64ops.VEC.search(o) for o in ops) or ('.' in mn and cond is None) or any(LANE.search(o) for o in ops)
    if not vec or cl != 'ordinary':
        return c, cl
    if base in ('mov', 'ins', 'umov') and any(LANE.search(o) for o in ops):
        return 4, cl
    if base in SWAR:
        return (max if base == 'bic' else min)(c, SWAR[base]), cl
    return c, cl
```

C.4 `swar_check.py` (check of every emulation against the lane-wise definition)

    6b97348f11896eaab98149c05682665157218ecd1e6f22d520e1051a6618f85c  swar_check.py

```python
"""Check that each SIMD form of the K hot path has a 256-bit-word program of the stated length.

A 128-bit register is one datum in one 256-bit word (as the v5 table already assumes for SIMD logic).
Each emulation below uses only v5 primitives (add mod 2^256, AND/OR/XOR/NOT, shifts) on such words;
`ops` counts them. Constants (lane masks) are immediates, as in the scalar rules.
"""
import random

import swar
W = (1 << 256) - 1
R128 = (1 << 128) - 1
def rep(v, bits):
    return sum(v << (bits * i) for i in range(128 // bits))
class C:
    n = 0
def op(v):
    C.n += 1
    return v & W
def NOT(a): return op(~a)
def AND(a, b): return op(a & b)
def OR(a, b): return op(a | b)
def XOR(a, b): return op(a ^ b)
def ADD(a, b): return op(a + b)
def SHL(a, k): return op(a << k)
def SHR(a, k): return op(a >> k)

def add_lanes(x, y, bits):
    L, H = rep((1 << (bits - 1)) - 1, bits), rep(1 << (bits - 1), bits)
    return XOR(ADD(AND(x, L), AND(y, L)), AND(XOR(x, y), H))
def shl_lanes(x, k, bits):
    return AND(SHL(x, k), rep(((1 << bits) - 1) ^ ((1 << k) - 1), bits))
def ushr_lanes(x, k, bits):
    return AND(SHR(x, k), rep((1 << (bits - k)) - 1, bits))
def usra_lanes(d, x, k, bits):
    return add_lanes(d, ushr_lanes(x, k, bits), bits)
def eor3(a, b, c): return XOR(XOR(a, b), c)
def bcax(a, b, c): return XOR(a, AND(b, NOT(c)))
def bsl(d, n, m): return XOR(AND(XOR(n, m), d), m)
def bic(a, b): return AND(a, NOT(b))
def dup32(w):
    r = w
    for k in (32, 64, 96):
        r = OR(r, AND(SHL(w, k), R128))
    return r
def dup64(x):
    return OR(x, AND(SHL(x, 64), R128))
def ext32(v, lane):
    return AND(SHR(v, 32 * lane), 0xffffffff)
def ins32(v, w, lane):
    return OR(AND(v, R128 ^ (0xffffffff << (32 * lane))), AND(SHL(w, 32 * lane), R128))
def ref(f, xs, bits):
    m = (1 << bits) - 1
    out = 0
    for i in range(128 // bits):
        out |= (f(*[(x >> (bits * i)) & m for x in xs]) & m) << (bits * i)
    return out

STATED = {name: swar.SWAR[name.split('.')[0]] for name in
          ('add.4s', 'add.2d', 'shl.4s', 'ushr.4s', 'usra.4s', 'eor3.16b', 'bcax.16b', 'bsl.16b', 'bic.16b',
           'dup.4s', 'dup.2d')}
STATED['mov.s(insert)'] = STATED['mov.s(extract)'] = swar.SWAR['ins']
random.seed(1)
worst = {}
for _ in range(2000):
    x, y, z = (random.getrandbits(128) for _ in range(3))
    w = random.getrandbits(32)
    k = random.randrange(1, 32)
    cases = {
        'add.4s': (lambda: add_lanes(x, y, 32), ref(lambda a, b: a + b, (x, y), 32)),
        'add.2d': (lambda: add_lanes(x, y, 64), ref(lambda a, b: a + b, (x, y), 64)),
        'shl.4s': (lambda: shl_lanes(x, k, 32), ref(lambda a: a << k, (x,), 32)),
        'ushr.4s': (lambda: ushr_lanes(x, k, 32), ref(lambda a: a >> k, (x,), 32)),
        'usra.4s': (lambda: usra_lanes(y, x, k, 32), ref(lambda d, a: d + (a >> k), (y, x), 32)),
        'eor3.16b': (lambda: eor3(x, y, z), x ^ y ^ z),
        'bcax.16b': (lambda: bcax(x, y, z), x ^ (y & ~z & R128)),
        'bsl.16b': (lambda: bsl(z, x, y), (z & x) | (~z & y & R128)),
        'bic.16b': (lambda: bic(x, y), x & ~y & R128),
        'dup.4s': (lambda: dup32(w), rep(w, 32)),
        'dup.2d': (lambda: dup64(x & ((1 << 64) - 1)), rep(x & ((1 << 64) - 1), 64)),
        'mov.s(extract)': (lambda: ext32(x, k % 4), (x >> (32 * (k % 4))) & 0xffffffff),
        'mov.s(insert)': (lambda: ins32(x, w, k % 4), (x & ~(0xffffffff << (32 * (k % 4))) & R128) | (w << (32 * (k % 4)))),
    }
    for name, (f, want) in cases.items():
        C.n = 0
        got = f()
        assert got == want, name
        worst[name] = max(worst.get(name, 0), C.n)
for name, n in worst.items():
    assert n <= STATED[name], (name, n, STATED[name])
    print(f"{name:14s} emulation ops {n:2d}  priced {STATED[name]:2d}  ok")
```

C.5 `kpath.py` (executed path and per-form means of K's executable)

    ddad93f78c8d2fdef7529264a93b630f3a2dd1a4c4a75b48e13bc81f03f4d4c6  kpath.py

```python
"""Per-form cost of the executed paths of the K binary that ran (macOS r31det3, sha256 2824a0f8...).

usage: xcrun llvm-objdump -d --no-show-raw-insn r31det3 > r31det3.dis; python3 kpath.py r31det3.dis
Prints, for the search hot path (one pass of the 8-lane block with no bitmap hit) and for the common
path of the table scan (one scanned word), the instruction count and the mean price under the v5
table (a64ops.cost) and under the SWAR SIMD prices (swar.cost).
"""
import json
import re
import sys

import a64ops
import swar

# (first address, last address, executions per pass)
PATHS = {
    'search, per 8 trials': [(0x100002b14, 0x100002b60, 1), (0x100002b64, 0x100003390, 2),
                             (0x100003394, 0x1000033a4, 1), (0x10000348c, 0x1000034a8, 8),
                             (0x100003460, 0x100003488, 8), (0x100002ae0, 0x100002af4, 1),
                             (0x100002af8, 0x100002b10, 1)],
    'table scan, per word': [(0x1000009dc, 0x100000a08, 1), (0x100000a18, 0x100000a30, 1),
                             (0x100000a40, 0x100000a64, 1)],
}
# code regions run off the hot path: static (unweighted) mean over every instruction of the region
REGIONS = {'bitmap-hit processing, completion and hashing (inlined in worker)': (0x1000034ac, 0x100004e9c),
           'worker outside the search hot path': (0x100002254, 0x100002adc)}
LINE = re.compile(r'^\s*([0-9a-f]+):\s+(\S+)(?:\s+(.*))?$')


def main():
    ins = {}
    for line in open(sys.argv[1]):
        m = LINE.match(line)
        if m:
            rest = (m.group(3) or '').split(';')[0].split('//')[0]
            rest = re.sub(r'\s*<[^>]*>\s*$', '', rest).strip()
            ins[int(m.group(1), 16)] = (m.group(2), a64ops.split_ops(rest) if rest else [])
    addrs = sorted(ins)
    for name, path in PATHS.items():
        n = v5 = sw = 0
        for lo, hi, k in path:
            for a in addrs:
                if lo <= a <= hi:
                    mn, ops = ins[a]
                    n += k
                    v5 += k * a64ops.cost(mn, ops)[0]
                    sw += k * swar.cost(mn, ops)[0]
        print(json.dumps(dict(path=name, instructions=n, v5_ops=v5, v5_mean=round(v5 / n, 4),
                              swar_ops=sw, swar_mean=round(sw / n, 4))))
    for name, (lo, hi) in REGIONS.items():
        sel = [ins[a] for a in addrs if lo <= a <= hi]
        priced = [(swar.cost(mn, ops), a64ops.cost(mn, ops)[0]) for mn, ops in sel]
        ordinary = [c for (c, cl), _ in priced if cl == 'ordinary']
        print(json.dumps(dict(region=name, instructions=len(sel), heavy=len(sel) - len(ordinary),
                              v5_mean=round(sum(v for _, v in priced) / len(sel), 4),
                              swar_mean=round(sum(c for (c, _), _ in priced) / len(sel), 4),
                              swar_ordinary_mean=round(sum(ordinary) / len(ordinary), 4))))
    heavy = [(a, ins[a][0]) for a in addrs if a64ops.cost(*ins[a])[1] != 'ordinary']
    print(json.dumps(dict(heavy_instructions=[f'{a:x} {mn}' for a, mn in heavy])))


if __name__ == '__main__':
    main()
```

C.6 `kprog.py` (one trial of K as straight-line primitives in three variants; checker against the organizer reference core; emits `klane_opt.h`, `klane.h`, `klane_ref.h`, `gval.h`)

    975f61dfa55f2bf3b0e55f1091f048fb6a7ab6d26f574b6b4ae305b2ed366f4c  kprog.py

Run as `python3 kprog.py --opt --emit`, `python3 kprog.py --emit` and `python3 kprog.py --ref --emit` next to
`ref_hash_functions.py`, a copy of the organizer's `verifier/hash_functions.py` (official repository at b809171).
The generated files are:

    514fa8ab8a461e4a41080efa27b4ba2a3b499eeedf0a2d2346e6562835d040f5  ref_hash_functions.py (copy of verifier/hash_functions.py)
    bd8467d25fac96becfe5234ee66afbc21a2c9d4d15eec9978f794f58c15f12a4  klane_opt.h (generated, --opt: 582 per trial, charged)
    0489879c3bb505ce5fb61af292cd5bfe56eba0d5b29753aaa1445aad0de3c8f9  klane.h (generated: 775 per trial)
    0ed04363d74953d244551f6cb37bb69b8779cfaa94b61adf85e5977f7e0359dd  klane_ref.h (generated, --ref: 1035 per trial)
    8a50b804634b8d94d228520372342212f400e74db5a08d9b3a14a70640cc13d8  gval.h (generated)

```python
"""Search K's per-trial work as an explicit straight-line program of 256-bit word-RAM primitives.

One lane = one trial of r31det3's worker loop (B.4): from x = message word 15 to the bitmap test
on key = IV[0] + A30.  The program is generated here as a list of primitives, executed by a counting
interpreter, checked against the organizer reference core, and emitted as C for the large-scale
check against r31det3 itself (kcount.c).  Three variants: --opt (charged, klane_opt.h: dup
rotations and the identities of OptProg), the default (klane.h: rotations as two shifts and an OR,
Boolean functions in the reference core's forms) and --ref (klane_ref.h, below).

Primitives (collision-frontier-v5): 256-bit load/store, add/sub mod 2^256, AND/OR/XOR/NOT, shift,
comparison, conditional branch.  Every value sits in its own 256-bit word.  Operands are registers;
the only immediates are shift counts.  Group values (everything that depends on words 0..14 only)
and round constants are loaded from fixed addresses, one load per use.  Registers M (2^32-1),
BM (bitmap base address, 0), C63 (63) and C1 (1) are loaded once per thread.

Masking: a value is reduced to 32 bits (AND with M) before it enters a right shift or a comparison.
Addition, AND, OR, XOR and NOT never move bits above position 31 into positions 0..31, so the low
32 bits of every value equal the 32-bit word the C source computes.  A 32-bit rotation of a clean
value is (v >> n) | (v << (32 - n)): three primitives, with garbage above bit 31 that the next mask
removes.  --ref prices every rotation as the organizer reference core writes it
(mask, shift, shift, OR, mask: five primitives) and masks T1, T2 and every schedule word as it does.
"""
import random
import sys

import ref_hash_functions as hf

MASK = 0xffffffff
MOD = 1 << 256
K = hf.SHA256_K
IV = hf.IV["sha256"]


def rotr(v, n):
    return ((v >> n) | (v << (32 - n))) & MASK


def bs0(v): return rotr(v, 2) ^ rotr(v, 13) ^ rotr(v, 22)
def bs1(v): return rotr(v, 6) ^ rotr(v, 11) ^ rotr(v, 25)
def sg0(v): return rotr(v, 7) ^ rotr(v, 18) ^ (v >> 3)
def sg1(v): return rotr(v, 17) ^ rotr(v, 19) ^ (v >> 10)
def ch(e, f, g): return ((e & f) ^ (~e & g)) & MASK
def maj(a, b, c): return (a & b) ^ (a & c) ^ (b & c)


def group_values(m):
    """Values that depend only on words 0..14 (computed once per group; kcount.c counts that set-up)."""
    a, b, c, d, e, f, g, h = IV
    for t in range(15):
        t1 = (h + bs1(e) + ch(e, f, g) + K[t] + m[t]) & MASK
        t2 = (bs0(a) + maj(a, b, c)) & MASK
        a, b, c, d, e, f, g, h = (t1 + t2) & MASK, a, b, c, (d + t1) & MASK, e, f, g
    m16 = (sg1(m[14]) + m[9] + sg0(m[1]) + m[0]) & MASK
    m18 = (sg1(m16) + m[11] + sg0(m[3]) + m[2]) & MASK
    m20 = (sg1(m18) + m[13] + sg0(m[5]) + m[4]) & MASK
    p15 = (h + bs1(e) + ch(e, f, g) + K[15]) & MASK
    q15 = (bs0(a) + maj(a, b, c)) & MASK
    G = {
        "U15": (d + p15) & MASK, "V15": (p15 + q15) & MASK,
        "a": a, "b": b, "c": c, "e": e, "f": f, "ab": a & b,
        "P16": (g + K[16] + m16) & MASK, "P17": (f + K[17]) & MASK, "P18": (e + K[18] + m18) & MASK,
        "KW20": (K[20] + m20) & MASK,
        "c17": (m[10] + sg0(m[2]) + m[1]) & MASK, "c19": (m[12] + sg0(m[4]) + m[3]) & MASK,
        "c21": (m[14] + sg0(m[6]) + m[5]) & MASK, "c22": (sg1(m20) + sg0(m[7]) + m[6]) & MASK,
        "c23": (m16 + sg0(m[8]) + m[7]) & MASK, "c24": (sg0(m[9]) + m[8]) & MASK,
        "c25": (m18 + sg0(m[10]) + m[9]) & MASK, "c26": (sg0(m[11]) + m[10]) & MASK,
        "c27": (m20 + sg0(m[12]) + m[11]) & MASK, "c28": (sg0(m[13]) + m[12]) & MASK,
        "c29k": (sg0(m[14]) + m[13] + K[29]) & MASK, "c30k": (m[14] + K[30] + IV[0]) & MASK,
        "axb": a ^ b, "exf": e ^ f,
    }
    for t in (19, 21, 22, 23, 24, 25, 26, 27, 28):
        G[f"K{t}"] = K[t]
    return G


GROUP_NAMES = list(group_values([0] * 15))


class Prog:
    def __init__(self, ref=False):
        self.ref = ref
        self.ops = []
        self.n = 0

    def emit(self, op, *src):
        self.n += 1
        d = f"v{self.n}"
        self.ops.append((op, d) + src)
        return d

    def ld(self, name): return self.emit("ld", name)
    def add(self, a, b): return self.emit("add", a, b)
    def and_(self, a, b): return self.emit("and", a, b)
    def or_(self, a, b): return self.emit("or", a, b)
    def xor(self, a, b): return self.emit("xor", a, b)
    def not_(self, a): return self.emit("not", a)
    def shr(self, a, n): return self.emit("shr", a, n)
    def shl(self, a, n): return self.emit("shl", a, n)
    def mask(self, a): return self.and_(a, "M")

    def rotr(self, v, n):
        if self.ref:
            t = self.mask(v)
            return self.mask(self.or_(self.shl(t, 32 - n), self.shr(t, n)))
        return self.or_(self.shr(v, n), self.shl(v, 32 - n))

    def bs0(self, v): return self.xor(self.xor(self.rotr(v, 2), self.rotr(v, 13)), self.rotr(v, 22))
    def bs1(self, v): return self.xor(self.xor(self.rotr(v, 6), self.rotr(v, 11)), self.rotr(v, 25))
    def sg0(self, v): return self.xor(self.xor(self.rotr(v, 7), self.rotr(v, 18)), self.shr(v, 3))
    def sg1(self, v): return self.xor(self.xor(self.rotr(v, 17), self.rotr(v, 19)), self.shr(v, 10))
    def ch(self, e, f, g): return self.xor(self.and_(e, f), self.and_(self.not_(e), g))
    def maj(self, a, b, c): return self.xor(self.xor(self.and_(a, b), self.and_(a, c)), self.and_(b, c))
    def refmask(self, v): return self.mask(v) if self.ref else v


def gen_lane(ref=False):
    """One trial: x -> key = IV[0] + A30 -> bitmap test.  Returns the program."""
    P = Prog(ref)
    x = "x"
    w = {}

    def sched(t):
        if t == 17: w[17] = P.mask(P.add(P.sg1(x), P.ld("c17")))
        elif t == 19: w[19] = P.mask(P.add(P.sg1(w[17]), P.ld("c19")))
        elif t == 21: w[21] = P.mask(P.add(P.sg1(w[19]), P.ld("c21")))
        elif t == 22: w[22] = P.mask(P.add(P.ld("c22"), x))
        elif t == 23: w[23] = P.mask(P.add(P.sg1(w[21]), P.ld("c23")))
        elif t == 24: w[24] = P.mask(P.add(P.add(P.sg1(w[22]), w[17]), P.ld("c24")))
        elif t == 25: w[25] = P.mask(P.add(P.sg1(w[23]), P.ld("c25")))
        elif t == 26: w[26] = P.mask(P.add(P.add(P.sg1(w[24]), w[19]), P.ld("c26")))
        elif t == 27: w[27] = P.mask(P.add(P.sg1(w[25]), P.ld("c27")))
        elif t == 28: w[28] = P.mask(P.add(P.add(P.sg1(w[26]), w[21]), P.ld("c28")))
        elif t == 29: w[29] = P.refmask(P.add(P.add(P.sg1(w[27]), w[22]), P.ld("c29k")))
        elif t == 30: w[30] = P.refmask(P.add(P.add(P.add(P.sg1(w[28]), w[23]), P.sg0(x)), P.ld("c30k")))

    # round 15: every term but x is a group value
    E = P.mask(P.add(P.ld("U15"), x))
    A = P.mask(P.add(P.ld("V15"), x))
    # round 16: B=a C=b D=c F=e G=f H=g (group values)
    s1 = P.bs1(E)
    c = P.xor(P.and_(E, P.ld("e")), P.and_(P.not_(E), P.ld("f")))
    T1 = P.refmask(P.add(P.add(P.ld("P16"), s1), c))
    s0 = P.bs0(A)
    mj = P.xor(P.xor(P.and_(A, P.ld("a")), P.and_(A, P.ld("b"))), P.ld("ab"))
    T2 = P.refmask(P.add(s0, mj))
    E16, A16 = P.mask(P.add(P.ld("c"), T1)), P.mask(P.add(T1, T2))
    # round 17: B=A15 C=a D=b F=E15 G=e H=f
    sched(17)
    s1 = P.bs1(E16)
    c = P.xor(P.and_(E16, E), P.and_(P.not_(E16), P.ld("e")))
    T1 = P.refmask(P.add(P.add(P.add(P.ld("P17"), s1), c), w[17]))
    s0 = P.bs0(A16)
    la = P.ld("a")
    mj = P.xor(P.xor(P.and_(A16, A), P.and_(A16, la)), P.and_(A, la))
    T2 = P.refmask(P.add(s0, mj))
    E17, A17 = P.mask(P.add(P.ld("b"), T1)), P.mask(P.add(T1, T2))
    # round 18: B=A16 C=A15 D=a F=E16 G=E15 H=e
    s1 = P.bs1(E17)
    c = P.ch(E17, E16, E)
    T1 = P.refmask(P.add(P.add(P.ld("P18"), s1), c))
    T2 = P.refmask(P.add(P.bs0(A17), P.maj(A17, A16, A)))
    E18, A18 = P.mask(P.add(P.ld("a"), T1)), P.mask(P.add(T1, T2))
    st = [A18, A17, A16, A, E18, E17, E16, E]  # A B C D E F G H entering round 19
    key = None
    for t in range(19, 31):
        Aa, Bb, Cc, Dd, Ee, Ff, Gg, Hh = st
        if t != 20:
            sched(t)
        if t == 20: kw = P.ld("KW20")
        elif t in (29, 30): kw = w[t]
        else: kw = P.add(P.ld(f"K{t}"), w[t])
        T1 = P.refmask(P.add(P.add(P.add(Hh, P.bs1(Ee)), P.ch(Ee, Ff, Gg)), kw))
        T2 = P.refmask(P.add(P.bs0(Aa), P.maj(Aa, Bb, Cc)))
        if t == 30:
            key = P.mask(P.add(T1, T2))  # IV[0] is folded into c30k; E30 is not needed
        else:
            st = [P.mask(P.add(T1, T2)), Aa, Bb, Cc, P.mask(P.add(Dd, T1)), Ee, Ff, Gg]
    # bitmap test: bit (key >> 8) of the 2^24-bit bitmap stored in 64-bit words at address BM
    bi = P.shr(key, 8)
    addr = P.add("BM", P.shr(bi, 6))
    word = P.emit("ldx", addr)
    bit = P.and_(P.emit("shrv", word, P.and_(bi, "C63")), "C1")
    hit = P.emit("cmp", bit)
    P.emit("br", hit)
    P.key, P.hit = key, hit
    return P


class OptProg(Prog):
    """--opt: the same values with fewer primitives, every step an identity on 256-bit words.

    dup(v) = v | (v << 32) holds two copies of a reduced word; bits 0..31 of dup(v) >> n are
    ROTR(v, n) for 0 < n < 32, so one dup serves the three rotations of a Sigma or sigma
    (2 + 3 shifts + 2 XOR = 7 instead of 11 or 9).  Ch(e,f,g) = g ^ (e & (f ^ g)) (3).
    Maj(a,b,c) = b ^ ((a ^ b) & (b ^ c)), where b ^ c is the previous step's a ^ b (3).
    """

    def dup(self, v): return self.or_(v, self.shl(v, 32))
    def bs0(self, v):
        d = self.dup(v)
        return self.xor(self.xor(self.shr(d, 2), self.shr(d, 13)), self.shr(d, 22))
    def bs1(self, v):
        d = self.dup(v)
        return self.xor(self.xor(self.shr(d, 6), self.shr(d, 11)), self.shr(d, 25))
    def sg0d(self, d, v): return self.xor(self.xor(self.shr(d, 7), self.shr(d, 18)), self.shr(v, 3))
    def sg1d(self, d, v): return self.xor(self.xor(self.shr(d, 17), self.shr(d, 19)), self.shr(v, 10))
    def sg0(self, v): return self.sg0d(self.dup(v), v)
    def sg1(self, v): return self.sg1d(self.dup(v), v)
    def ch(self, e, f, g): return self.xor(g, self.and_(e, self.xor(f, g)))


def gen_lane_opt():
    P = OptProg(False)
    x = "x"
    dx = P.dup(x)
    w = {}

    def sched(t):
        if t == 17: w[17] = P.mask(P.add(P.sg1d(dx, x), P.ld("c17")))
        elif t == 19: w[19] = P.mask(P.add(P.sg1(w[17]), P.ld("c19")))
        elif t == 21: w[21] = P.mask(P.add(P.sg1(w[19]), P.ld("c21")))
        elif t == 22: w[22] = P.mask(P.add(P.ld("c22"), x))
        elif t == 23: w[23] = P.mask(P.add(P.sg1(w[21]), P.ld("c23")))
        elif t == 24: w[24] = P.mask(P.add(P.add(P.sg1(w[22]), w[17]), P.ld("c24")))
        elif t == 25: w[25] = P.mask(P.add(P.sg1(w[23]), P.ld("c25")))
        elif t == 26: w[26] = P.mask(P.add(P.add(P.sg1(w[24]), w[19]), P.ld("c26")))
        elif t == 27: w[27] = P.mask(P.add(P.sg1(w[25]), P.ld("c27")))
        elif t == 28: w[28] = P.mask(P.add(P.add(P.sg1(w[26]), w[21]), P.ld("c28")))
        elif t == 29: w[29] = P.add(P.add(P.sg1(w[27]), w[22]), P.ld("c29k"))
        elif t == 30: w[30] = P.add(P.add(P.add(P.sg1(w[28]), w[23]), P.sg0d(dx, x)), P.ld("c30k"))

    E = P.mask(P.add(P.ld("U15"), x))
    A = P.mask(P.add(P.ld("V15"), x))
    # step 16: B=a C=b D=c F=e G=f H=g
    c = P.xor(P.ld("f"), P.and_(E, P.ld("exf")))
    T1 = P.add(P.add(P.ld("P16"), P.bs1(E)), c)
    la = P.ld("a")
    xab = P.xor(A, la)                                   # A15 ^ a: B ^ C of step 17
    T2 = P.add(P.bs0(A), P.xor(la, P.and_(xab, P.ld("axb"))))
    E16, A16 = P.mask(P.add(P.ld("c"), T1)), P.mask(P.add(T1, T2))
    # step 17: B=A15 C=a D=b F=E15 G=e H=f
    sched(17)
    le = P.ld("e")
    c = P.xor(le, P.and_(E16, P.xor(E, le)))
    T1 = P.add(P.add(P.add(P.ld("P17"), P.bs1(E16)), c), w[17])
    x2 = P.xor(A16, A)
    T2 = P.add(P.bs0(A16), P.xor(A, P.and_(x2, xab)))
    xab = x2
    E17, A17 = P.mask(P.add(P.ld("b"), T1)), P.mask(P.add(T1, T2))
    # step 18: B=A16 C=A15 D=a F=E16 G=E15 H=e
    T1 = P.add(P.add(P.ld("P18"), P.bs1(E17)), P.ch(E17, E16, E))
    x2 = P.xor(A17, A16)
    T2 = P.add(P.bs0(A17), P.xor(A16, P.and_(x2, xab)))
    xab = x2
    E18, A18 = P.mask(P.add(P.ld("a"), T1)), P.mask(P.add(T1, T2))
    st = [A18, A17, A16, A, E18, E17, E16, E]
    key = None
    for t in range(19, 31):
        Aa, Bb, Cc, Dd, Ee, Ff, Gg, Hh = st
        if t != 20:
            sched(t)
        if t == 20: kw = P.ld("KW20")
        elif t in (29, 30): kw = w[t]
        else: kw = P.add(P.ld(f"K{t}"), w[t])
        T1 = P.add(P.add(P.add(Hh, P.bs1(Ee)), P.ch(Ee, Ff, Gg)), kw)
        x2 = P.xor(Aa, Bb)
        T2 = P.add(P.bs0(Aa), P.xor(Bb, P.and_(x2, xab)))
        xab = x2
        if t == 30:
            key = P.mask(P.add(T1, T2))
        else:
            st = [P.mask(P.add(T1, T2)), Aa, Bb, Cc, P.mask(P.add(Dd, T1)), Ee, Ff, Gg]
    bi = P.shr(key, 8)
    addr = P.add("BM", P.shr(bi, 6))
    word = P.emit("ldx", addr)
    bit = P.and_(P.emit("shrv", word, P.and_(bi, "C63")), "C1")
    hit = P.emit("cmp", bit)
    P.emit("br", hit)
    P.key, P.hit = key, hit
    P.mode = "opt"
    return P


def run(P, G, x, mem):
    """Counting interpreter: 256-bit words, returns (key, hit, ops)."""
    R = {"x": x, "M": MASK, "BM": 0, "C63": 63, "C1": 1}
    ops = 0
    for op in P.ops:
        o, d, *s = op
        ops += 1
        if o == "ld": R[d] = G[s[0]]
        elif o == "add": R[d] = (R[s[0]] + R[s[1]]) % MOD
        elif o == "and": R[d] = R[s[0]] & R[s[1]]
        elif o == "or": R[d] = R[s[0]] | R[s[1]]
        elif o == "xor": R[d] = R[s[0]] ^ R[s[1]]
        elif o == "not": R[d] = (MOD - 1) ^ R[s[0]]
        elif o == "shr": R[d] = R[s[0]] >> s[1]
        elif o == "shl": R[d] = (R[s[0]] << s[1]) % MOD
        elif o == "shrv": R[d] = R[s[0]] >> R[s[1]]
        elif o == "ldx": R[d] = mem.get(R[s[0]], 0)
        elif o == "cmp": R[d] = int(R[s[0]] != 0)
        elif o == "br": R[d] = None
        else: raise ValueError(o)
    return R[P.key], R[P.hit], ops


def max_live(P):
    """Registers needed by the straight-line lane (interval colouring = maximum live set)."""
    last = {}
    for i, (o, d, *s) in enumerate(P.ops):
        for v in s:
            if isinstance(v, str) and v.startswith("v"):
                last[v] = i
    live, peak = set(), 0
    for i, (o, d, *s) in enumerate(P.ops):
        if d in last:
            live.add(d)
        peak = max(peak, len(live) + 1)  # +1: x stays live until its last use
        for v in s:
            if isinstance(v, str) and last.get(v) == i:
                live.discard(v)
    return peak


def histogram(P):
    h = {}
    for o, *_ in P.ops:
        h[o] = h.get(o, 0) + 1
    return h


C_OP = {"add": "ADD", "and": "AND", "or": "OR", "xor": "XOR", "shr": "SHR", "shl": "SHL",
        "shrv": "SHR", "not": "NOT"}


def emit_c(P, fname):
    out = [f"/* generated by kprog.py --{getattr(P, 'mode', 'ref' if P.ref else 'plain')}: {len(P.ops)} primitives per trial */",
           f"static inline int {fname}(const gval_t *G, W x, const uint64_t *bm, uint32_t *keyout) {{"]
    for o, d, *s in P.ops:
        if o == "ld": out.append(f"  W {d} = LD(G->{s[0]});")
        elif o in ("not",): out.append(f"  W {d} = NOT({s[0]});")
        elif o in ("shr", "shl"): out.append(f"  W {d} = {C_OP[o]}({s[0]}, {s[1]});")
        elif o == "ldx": out.append(f"  W {d} = LDX(bm, {s[0]});")
        elif o == "cmp": out.append(f"  W {d} = CMPNZ({s[0]});")
        elif o == "br": out.append(f"  BR(); *keyout = (uint32_t){P.key}; return (int){s[0]};")
        else: out.append(f"  W {d} = {C_OP[o]}({s[0]}, {s[1]});")
    out.append("}")
    return "\n".join(out) + "\n"


def main():
    ref = "--ref" in sys.argv
    opt = "--opt" in sys.argv
    P = gen_lane_opt() if opt else gen_lane(ref)
    mode = "opt" if opt else "ref" if ref else "plain"
    n = len(P.ops)
    rng = random.Random(20261008)
    trials = 20000
    for i in range(trials):
        m = [rng.getrandbits(32) for _ in range(15)]
        x = rng.getrandbits(24)
        G = group_values(m)
        bi_mem = {}
        key, hit, ops = run(P, G, x, bi_mem)
        block = b"".join(v.to_bytes(4, "big") for v in m + [x])
        want = hf._compress("sha256", tuple(IV), block, 31)[0]
        assert key == want, (i, hex(key), hex(want))
        assert ops == n
        # bitmap path: set the tested bit and check the decision flips
        if i < 2000:
            bi = key >> 8
            mem = {bi >> 6: 1 << (bi & 63)}
            k2, h2, _ = run(P, G, x, mem)
            assert (k2, h2, hit) == (key, 1, 0)
    print(f"mode {mode}: {n} primitives per trial, {trials} trials match the "
          f"organizer reference core (word 0 of compress31), registers needed {max_live(P)}")
    print("histogram", dict(sorted(histogram(P).items())))
    if "--emit" in sys.argv:
        name = {"opt": "klane_opt", "ref": "klane_ref", "plain": "klane"}[mode]
        with open(f"{name}.h", "w") as fh:
            fh.write(emit_c(P, name))
        with open("gval.h", "w") as fh:
            fh.write("/* generated by kprog.py: group values read by the lane program */\n"
                     "typedef struct { uint32_t " + ", ".join(GROUP_NAMES) + "; } gval_t;\n")


if __name__ == "__main__":
    main()
```

C.7 `kcount.c` (search K as a counted program: table, group set-up, trials, hit processing, completion; validation against `r31det3.c`)

    9541ae71e67da67a2084012a0e09622c9cf9fcfae1717919452aed2fc10d1a0e  kcount.c
    29f4a1900e293efd2459cac87ed197c8176f20b763b92663da19dea3c3140d3e  r31det3.c (B.4, unchanged)
    84003700c7015677e60700dc5c044d1c6e7c0acc652e6bf12d536f9aa5084437  sp_own.h (B.5, unchanged)

Build and run in a directory with `r31det3.c`, `sp_own.h` and the four generated headers:
`cc -O2 -o kcount kcount.c -lpthread && ./kcount` (Apple clang 21, 12 threads for the 2^32 scan; about 10 s).

```c
/* kcount.c: search K (r31det3.c, B.4) as a counted program of 256-bit word-RAM primitives.

   Every primitive goes through one function or macro below and adds 1 to OPS (the 64-bit multiply
   is emulated with counted primitives).  Values are 256-bit words held here in 128-bit integers:
   the program reduces a value to 32 or 64 bits before every right shift and comparison, and +, -, AND, OR,
   XOR, NOT and left shifts never move bits above position 127 into positions 0..63, so every
   observable result equals the 256-bit one.  Fixed-count loops are straight-line code in the
   counted program and pay nothing; data-dependent loops pay their counter, comparison and branch.

   r31det3.c is included unchanged: its build_table, process_hit and worker kernel are the reference
   that every counted result is compared with.  The charged trial is klane_opt (kprog.py --opt);
   klane and klane_ref (the other two variants) are run on every 1024th trial with the same key.
   Sigma, sigma, Ch and Maj use the identities of Section 16.1: dup(v) = v | v << 32 serves the
   three rotations, Ch = g ^ (e & (f ^ g)), Maj = (a & b) | (c & (a | b)).

   cc -O2 -o kcount kcount.c -lpthread
   ./kcount            table, self-checks, search validation, per-event counts */
#define main r31det3_main
#include "r31det3.c"
#undef main
#include <assert.h>

typedef unsigned __int128 W;
static __thread uint64_t OPS;
/* one primitive each; functions, so the count is sequenced whatever the operand nesting */
static inline W ADD(W a, W b) { OPS++; return a + b; }
static inline W SUB(W a, W b) { OPS++; return a - b; }
static inline W AND(W a, W b) { OPS++; return a & b; }
static inline W OR(W a, W b)  { OPS++; return a | b; }
static inline W XOR(W a, W b) { OPS++; return a ^ b; }
static inline W NOT(W a)      { OPS++; return ~a; }
static inline W SHR(W a, int n) { OPS++; return a >> n; }
static inline W SHL(W a, int n) { OPS++; return a << n; }
static inline W LD(W v)       { OPS++; return v; }
static inline W LDX(const uint64_t *bm, W a) { OPS++; return (W)bm[(uint64_t)a]; }
static inline W CMPNZ(W a)    { OPS++; return a != 0; }
static inline W CMPEQ(W a, W b) { OPS++; return a == b; }
static inline W CMPLT(W a, W b) { OPS++; return a < b; }
#define ST(dst,v) do { W st_v_ = (v); OPS++; (dst) = st_v_; } while (0)
#define BR()     (OPS++)
static const W M = 0xffffffffu, M64 = 0xffffffffffffffffull, BM = 0, C63 = 63, C1 = 1;
static inline W MSK(W a) { return AND(a, M); }

#include "gval.h"
#include "klane.h"
#include "klane_ref.h"
#include "klane_opt.h"

/* 64 x 64 -> low 64 bits by shift-and-add, branch-free: acc += (a << i) & -(b >> i & 1); 6 per bit + mask */
static W mul64_c(W a, W b) {
  W acc = 0;
  for (int i = 0; i < 64; i++) { W bit = AND(SHR(b, i), C1); W sel = SUB(0, bit); acc = ADD(acc, AND(SHL(a, i), sel)); }
  return AND(acc, M64);
}
/* splitmix64 as sm() of B.4; state in memory */
static W sm_c(uint64_t *s) {
  W z = AND(ADD(LD(*s), LD(0x9e3779b97f4a7c15ull)), M64); ST(*s, (uint64_t)z);
  z = XOR(z, SHR(z, 30)); z = mul64_c(z, LD(0xbf58476d1ce4e5b9ull));
  z = XOR(z, SHR(z, 27)); z = mul64_c(z, LD(0x94d049bb133111ebull));
  return XOR(z, SHR(z, 31));
}

/* v clean (reduced to 32 bits).  dup(v) = v | v << 32 holds two copies, so bits 0..31 of
   dup(v) >> n are ROTR(v, n); one dup serves the three rotations of a Sigma or sigma. */
static W dup_c(W v) { return OR(v, SHL(v, 32)); }
static W bs0_c(W v) { W d = dup_c(v); return XOR(XOR(SHR(d, 2), SHR(d, 13)), SHR(d, 22)); }
static W bs1_c(W v) { W d = dup_c(v); return XOR(XOR(SHR(d, 6), SHR(d, 11)), SHR(d, 25)); }
static W sg0d_c(W d, W v) { return XOR(XOR(SHR(d, 7), SHR(d, 18)), SHR(v, 3)); }
static W sg1d_c(W d, W v) { return XOR(XOR(SHR(d, 17), SHR(d, 19)), SHR(v, 10)); }
static W sg0_c(W v) { return sg0d_c(dup_c(v), v); }
static W sg1_c(W v) { return sg1d_c(dup_c(v), v); }
static W ch_c(W e, W f, W g) { return XOR(g, AND(e, XOR(f, g))); }
static W maj_c(W a, W b, W c) { return OR(AND(a, b), AND(c, OR(a, b))); }

/* compress31 of B.4: chaining value and block in memory, schedule stored, output stored */
static void compress31_c(const uint32_t cv[8], const uint32_t m[16], uint32_t out[8]) {
  uint32_t Wm[31];
  for (int t = 16; t < 31; t++) {
    const uint32_t *p2 = t - 2 < 16 ? &m[t - 2] : &Wm[t - 2], *p7 = t - 7 < 16 ? &m[t - 7] : &Wm[t - 7];
    W v = MSK(ADD(ADD(ADD(sg1_c(LD(*p2)), LD(*p7)), sg0_c(LD(m[t - 15]))), LD(m[t - 16])));
    ST(Wm[t], (uint32_t)v);
  }
  W a = LD(cv[0]), b = LD(cv[1]), c = LD(cv[2]), d = LD(cv[3]), e = LD(cv[4]), f = LD(cv[5]), g = LD(cv[6]), h = LD(cv[7]);
  for (int t = 0; t < 31; t++) {
    W w = LD(t < 16 ? m[t] : Wm[t]);
    W T1 = ADD(ADD(ADD(ADD(h, bs1_c(e)), ch_c(e, f, g)), LD(K[t])), w);
    W T2 = ADD(bs0_c(a), maj_c(a, b, c));
    h = g; g = f; f = e; e = MSK(ADD(d, T1)); d = c; c = b; b = a; a = MSK(ADD(T1, T2));
  }
  W r[8] = {a, b, c, d, e, f, g, h};
  for (int i = 0; i < 8; i++) ST(out[i], (uint32_t)MSK(ADD(LD(cv[i]), r[i])));
}

/* ---------------- table build (build_table of B.4), counted ---------------- */
typedef struct { uint64_t lo, hi, ops; uint32_t *v7, *v8, *g16; int n7, n8, ng; } p1_t;
static void *p1_worker(void *arg) {
  p1_t *p = arg; OPS = 0; p->n7 = p->n8 = p->ng = 0;
  W rD8 = LD(D8), rC8 = LD(C8), rD7 = LD(D7), rC7 = LD(C7), rD9 = LD(D9), rD18 = LD(D18);
  for (uint64_t w64 = p->lo; w64 < p->hi; w64++) {
    W w = (W)w64;                                       /* loop register, clean */
    W dw = dup_c(w), s0w = sg0d_c(dw, w), s1w = sg1d_c(dw, w);
    W d8 = MSK(SUB(sg0_c(MSK(ADD(w, rD8))), s0w));
    W hit8 = CMPEQ(d8, rC8); BR(); if (hit8) { ST(p->v8[p->n8], (uint32_t)w); p->n8 = (int)ADD(p->n8, C1); }
    W d7 = MSK(SUB(sg0_c(MSK(ADD(w, rD7))), s0w));
    W hit7 = CMPEQ(d7, rC7); BR(); if (hit7) { ST(p->v7[p->n7], (uint32_t)w); p->n7 = (int)ADD(p->n7, C1); }
    W d9 = MSK(SUB(sg1_c(MSK(ADD(w, rD9))), s1w));
    W hit9 = CMPEQ(d9, rD18); BR(); if (hit9) { ST(p->g16[p->ng], (uint32_t)w); p->ng = (int)ADD(p->ng, C1); }
    W nw = MSK(ADD(w, C1)); (void)nw; W more = CMPNZ(nw); BR(); (void)more;  /* w++ until it wraps to 0 */
  }
  p->ops = OPS; return NULL;
}

static rec_t *recs_c; static int nrec_c; static uint64_t *bitmap_c; static uint32_t G16_c[64]; static int ng16_c;
static uint32_t s1inv_col_c[32];

static uint64_t ops_p1, ops_p2, ops_sort, ops_bitmap, ops_s1inv, ops_selftest;

static void msort_c(rec_t *a, rec_t *tmp, int n) {
  /* bottom-up merge sort on key; per element moved: 2 key loads, compare, branch, 6 loads, 6 stores,
     2 index increments, loop compare and branch */
  for (int width = 1; width < n; width = (int)ADD(SHL(width, 1), 0)) {
    for (int lo = 0; lo < n; lo += 2 * width) {
      int mid = lo + width < n ? lo + width : n, hi = lo + 2 * width < n ? lo + 2 * width : n;
      OPS += 6;                                       /* mid, hi: two adds, two compares, two selects */
      int i = lo, j = mid, k = lo;
      while (k < hi) {
        int takeleft;
        if (i < mid && j < hi) { W ki = LD(a[i].key), kj = LD(a[j].key); takeleft = (int)CMPLT(kj, ki) == 0; BR(); }
        else { OPS += 2; takeleft = i < mid; }
        rec_t *s = takeleft ? &a[i] : &a[j];
        tmp[k] = (rec_t){(uint32_t)LD(s->key), (uint32_t)LD(s->A0), (uint32_t)LD(s->E3), (uint32_t)LD(s->E4), (uint32_t)LD(s->W7), (uint32_t)LD(s->W8)};
        OPS += 6;                                     /* six stores */
        if (takeleft) i = (int)ADD(i, C1); else j = (int)ADD(j, C1);
        k = (int)ADD(k, C1); OPS += 4;                /* i < mid, j < hi, k < hi compares and branch */
      }
      OPS += 3;                                       /* lo += 2*width, compare, branch */
    }
    memcpy(a, tmp, sizeof(rec_t) * n); OPS += 12ull * n;  /* copy back: 6 loads + 6 stores each */
    OPS += 2;
  }
}

static int cmpall(const void *p, const void *q) { return memcmp(p, q, sizeof(rec_t)); }
static void build_table_c(void) {
  static uint32_t V7c[1024], V8c[65536];
  /* P1: 2^32 scan in 12 slices */
  enum { NT = 12 }; p1_t sl[NT]; pthread_t th[NT];
  static uint32_t v7s[NT][1024], v8s[NT][65536], g16s[NT][64];
  for (int i = 0; i < NT; i++) {
    sl[i].lo = (1ull << 32) * i / NT; sl[i].hi = (1ull << 32) * (i + 1) / NT;
    sl[i].v7 = v7s[i]; sl[i].v8 = v8s[i]; sl[i].g16 = g16s[i];
    pthread_create(&th[i], 0, p1_worker, &sl[i]);
  }
  int n7 = 0, n8 = 0; ng16_c = 0; ops_p1 = 0;
  for (int i = 0; i < NT; i++) {
    pthread_join(th[i], 0); ops_p1 += sl[i].ops;
    memcpy(V7c + n7, sl[i].v7, 4 * sl[i].n7); n7 += sl[i].n7;
    memcpy(V8c + n8, sl[i].v8, 4 * sl[i].n8); n8 += sl[i].n8;
    memcpy(G16_c + ng16_c, sl[i].g16, 4 * sl[i].ng); ng16_c += sl[i].ng;
  }
  ops_p1 -= (NT - 1) * 6;                             /* the six constant loads are paid once */
  /* P2 */
  OPS = 0;
  uint32_t cm4 = 0, va4 = 0, cm3 = 0, va3 = 0; const char *r4 = "============0===0=========01===0", *r3 = "==========================10====";
  for (int k = 0; k < 32; k++) { uint32_t b = 1u << (31 - k); if (r4[k] != '=') { cm4 |= b; if (r4[k] == '1') va4 |= b; } if (r3[k] != '=') { cm3 |= b; if (r3[k] == '1') va3 |= b; } }
  OPS += 4 * 32 * 4;                                  /* the two row masks: 32 cells, at most 4 primitives each, both rows (loose) */
  W lhs7 = MSK(SUB(SUB(SUB(LD(EB(7)), LD(EA(7))), SUB(bs1_c(LD(EB(6))), bs1_c(LD(EA(6))))), LD(D7)));
  W lhs6 = MSK(SUB(SUB(SUB(LD(EB(6)), LD(EA(6))), SUB(bs1_c(LD(EB(5))), bs1_c(LD(EA(5))))), LD(D6)));
  rec_t *rc = malloc(sizeof(rec_t) * (1 << 20)); int nr = 0;
  W e8 = LD(EA(8)), a4 = LD(AA(4)), e7 = LD(EA(7)), e6 = LD(EA(6)), e5 = LD(EA(5)), eb6 = LD(EB(6)), eb5 = LD(EB(5));
  W a3 = LD(AA(3)), a2 = LD(AA(2)), a1 = LD(AA(1)), k8 = LD(K[8]), k7 = LD(K[7]);
  W base4 = MSK(SUB(SUB(SUB(e8, a4), bs1_c(e7)), ch_c(e7, e6, e5)));          /* loop-invariant part of E4 */
  W bs0a3 = bs0_c(a3), maja3 = maj_c(a3, a2, a1), bs0a2 = bs0_c(a2), bs1e6 = bs1_c(e6);
  W rcm4 = LD(cm4), rva4 = LD(va4), rcm3 = LD(cm3), rva3 = LD(va3);
  for (int i = 0; i < n8; i++) {
    OPS += 3;                                         /* i < n8, branch, i++ */
    W W8 = LD(V8c[i]);
    W E4 = MSK(SUB(SUB(base4, k8), W8));
    W ok4 = CMPEQ(AND(E4, rcm4), rva4); BR(); if (!ok4) continue;
    W d7 = MSK(SUB(ch_c(eb6, eb5, E4), ch_c(e6, e5, E4)));
    W ok7 = CMPEQ(d7, lhs7); BR(); if (!ok7) continue;
    W A0 = MSK(ADD(ADD(SUB(E4, a4), bs0a3), maja3));
    W b3 = MSK(SUB(SUB(SUB(e7, a3), bs1e6), ch_c(e6, e5, E4)));               /* E3 without K[7], W7 */
    W maj2 = maj_c(a2, a1, A0);
    for (int j = 0; j < n7; j++) {
      OPS += 3;
      W W7 = LD(V7c[j]);
      W E3 = MSK(SUB(SUB(b3, k7), W7));
      W ok3 = CMPEQ(AND(E3, rcm3), rva3); BR(); if (!ok3) continue;
      W d6 = MSK(SUB(ch_c(eb5, E4, E3), ch_c(e5, E4, E3)));
      W ok6 = CMPEQ(d6, lhs6); BR(); if (!ok6) continue;
      W Am1 = MSK(ADD(ADD(SUB(E3, a3), bs0a2), maj2));
      rc[nr] = (rec_t){(uint32_t)Am1, (uint32_t)A0, (uint32_t)E3, (uint32_t)E4, (uint32_t)W7, (uint32_t)W8};
      OPS += 6; nr = (int)ADD(nr, C1);                /* six stores, count */
    }
    OPS += 1;                                         /* final j compare */
  }
  OPS += 1;
  ops_p2 = OPS;
  /* sort */
  OPS = 0; rec_t *tmp = malloc(sizeof(rec_t) * nr); msort_c(rc, tmp, nr); free(tmp); ops_sort = OPS;
  recs_c = rc; nrec_c = nr;
  /* bitmap: 2^18 zero stores, then one bit per record */
  OPS = 0; bitmap_c = calloc(1 << 18, 8); OPS += 1u << 18;
  for (int i = 0; i < nr; i++) {
    OPS += 3;
    W b = SHR(LD(rc[i].key), 8); W wi = SHR(b, 6); W addr = ADD(BM, wi);
    W word = LDX(bitmap_c, addr); W bit = SHL(C1, (int)AND(b, C63));
    bitmap_c[(uint64_t)addr] = (uint64_t)OR(word, bit); OPS++;
  }
  ops_bitmap = OPS;
  /* compare with r31det3's build_table (called before) */
  assert(n7 == 512 && n8 == 49408 && ng16_c == ng16 && nr == nrec);
  for (int i = 0; i < ng16; i++) assert(G16_c[i] == G16[i]);
  assert(memcmp(bitmap_c, bitmap, 8u << 18) == 0);
  for (int i = 0; i < nr; i++) { assert(recs_c[i].key == recs[i].key); if (i) assert(recs_c[i - 1].key <= recs_c[i].key); }
  /* same multiset of records: sort copies by all fields */
  rec_t *x1 = malloc(sizeof(rec_t) * nr), *x2 = malloc(sizeof(rec_t) * nr);
  memcpy(x1, recs, sizeof(rec_t) * nr); memcpy(x2, recs_c, sizeof(rec_t) * nr);
  qsort(x1, nr, sizeof(rec_t), cmpall); qsort(x2, nr, sizeof(rec_t), cmpall); assert(memcmp(x1, x2, sizeof(rec_t) * nr) == 0);
  free(x1); free(x2);
}

/* build_s1inv of B.4, counted (pivot search branches on data that is fixed: s1 itself) */
static void build_s1inv_c(void) {
  OPS = 0;
  uint32_t val[32], comb[32];
  for (int i = 0; i < 32; i++) { W b = SHL(C1, i); ST(val[i], (uint32_t)MSK(sg1_c(b))); ST(comb[i], (uint32_t)b); }
  for (int k = 0; k < 32; k++) {
    int p = -1;
    for (int i = k; i < 32; i++) { OPS += 3; W bit = AND(SHR(LD(val[i]), k), C1); BR(); if (bit) { p = i; break; } }
    BR();
    uint32_t tv = (uint32_t)LD(val[k]), tc = (uint32_t)LD(comb[k]);
    ST(val[k], (uint32_t)LD(val[p])); ST(comb[k], (uint32_t)LD(comb[p])); ST(val[p], tv); ST(comb[p], tc);
    for (int i = 0; i < 32; i++) {
      OPS += 2; W bit = AND(SHR(LD(val[i]), k), C1); W ne = CMPNZ(i != k); BR(); BR();
      if (i != k && bit) { ST(val[i], (uint32_t)XOR(LD(val[i]), LD(val[k]))); ST(comb[i], (uint32_t)XOR(LD(comb[i]), LD(comb[k]))); }
      (void)ne;
    }
  }
  for (int k = 0; k < 32; k++) ST(s1inv_col_c[k], (uint32_t)LD(comb[k]));
  for (int t = 0; t < 1000; t++) {                    /* the 1000-value self-check */
    OPS += 3; W y = MSK(ADD(mul64_c(LD((uint32_t)t), LD(2654435761u)), LD(12345u)));
    assert((uint32_t)y == (uint32_t)(t * 2654435761u + 12345));
    W xx = 0;
    for (int k = 0; k < 32; k++) { W bit = AND(SHR(y, k), C1); xx = XOR(xx, AND(LD(s1inv_col_c[k]), SUB(0, bit))); }
    W back = MSK(sg1_c(MSK(xx))); W ok = CMPEQ(back, y); BR(); assert(ok);
  }
  for (int k = 0; k < 32; k++) assert(s1inv_col_c[k] == s1inv_col[k]);
  ops_s1inv = OPS;
}
static W s1inv_c(W y) {
  W xx = 0;
  for (int k = 0; k < 32; k++) { W bit = AND(SHR(y, k), C1); xx = XOR(xx, AND(LD(s1inv_col_c[k]), SUB(0, bit))); }
  return MSK(xx);
}

/* group set-up of worker (B.4), counted; returns m[0..14], group values, completion coins */
static void gvalues_from_words(const uint32_t m[15], gval_t *G);
static void gsetup_c(uint64_t g, uint32_t m[15], gval_t *G, uint64_t *crs) {
  OPS += 3;                                           /* groups counter: load, add, store */
  uint64_t rs = (uint64_t)XOR(XOR(LD(seed_base), mul64_c(g, LD(0x9e3779b97f4a7c15ull))), LD(0x5bd1e9955bd1e995ull)); OPS++;
  for (int i = 0; i < 15; i++) ST(m[i], (uint32_t)AND(sm_c(&rs), M));
  ST(*crs, (uint64_t)XOR(XOR(LD(seed_base), mul64_c(g, LD(0xd1b54a32d192ed03ull))), LD(0x2545f4914f6cdd1dull)));
  gvalues_from_words(m, G);
}

/* ---------------- hit processing (process_hit, complete of B.4), counted ---------------- */
typedef struct { uint64_t bmhits, keyhits, recs, v6, joint, comp_ok, coll, it13, it15;
                 uint64_t maxH, maxR, maxV, maxKx, segVfound, opsC, bsearch_max; uint32_t M1[16], M1b[16]; } hstat_t;

static int complete_c(uint32_t Wv[16], W g, uint64_t *rs, hstat_t *hs) {
  W W9 = LD(Wv[9]), W1 = LD(Wv[1]), W0 = LD(Wv[0]);
  W s0W1 = sg0_c(W1);
  W W14 = s1inv_c(MSK(SUB(SUB(SUB(g, W9), s0W1), W0))); ST(Wv[14], (uint32_t)W14);
  W chk = CMPEQ(MSK(ADD(ADD(ADD(sg1_c(W14), W9), s0W1), W0)), g); BR(); if (!chk) return 0;
#define LA(i) LD(AA(i))
#define LE(i) LD(EA(i))
#define LAB(i) LD(AB(i))
#define LEB(i) LD(EB(i))
  W b13 = MSK(ADD(ADD(ADD(ADD(LA(9), LE(9)), bs1_c(LE(12))), ch_c(LE(12), LE(11), LE(10))), LD(K[13])));
  W b13b = MSK(ADD(ADD(ADD(ADD(LAB(9), LEB(9)), bs1_c(LEB(12))), ch_c(LEB(12), LEB(11), LEB(10))), LD(K[13])));
  W eq = CMPEQ(b13, b13b); BR(); if (!eq) return 0;
  for (int t = 0; t < (1 << 22); t++) {
    OPS += 3;                                         /* t < 2^22, branch, t++ */
    hs->it13++; OPS += 3;
    W E13 = AND(sm_c(rs), M); W W13 = MSK(SUB(E13, b13));
    W A13 = MSK(ADD(ADD(SUB(E13, LA(9)), bs0_c(LA(12))), maj_c(LA(12), LA(11), LA(10))));
    W A13b = MSK(ADD(ADD(SUB(E13, LAB(9)), bs0_c(LAB(12))), maj_c(LAB(12), LAB(11), LAB(10))));
    W e1 = CMPEQ(A13, A13b); BR(); if (!e1) return 0;
    W E14 = MSK(ADD(ADD(ADD(ADD(ADD(LA(10), LE(10)), bs1_c(E13)), ch_c(E13, LE(12), LE(11))), LD(K[14])), W14));
    W E14b = MSK(ADD(ADD(ADD(ADD(ADD(LAB(10), LEB(10)), bs1_c(E13)), ch_c(E13, LEB(12), LEB(11))), LD(K[14])), W14));
    W e2 = CMPEQ(MSK(SUB(E14b, E14)), LD(0x8004u)); BR(); if (!e2) continue;
    W A14 = MSK(ADD(ADD(SUB(E14, LA(10)), bs0_c(A13)), maj_c(A13, LA(12), LA(11))));
    W A14b = MSK(ADD(ADD(SUB(E14b, LAB(10)), bs0_c(A13)), maj_c(A13, LAB(12), LAB(11))));
    W e3 = CMPEQ(A14, A14b); BR(); if (!e3) continue;
    W f15 = MSK(ADD(ADD(ADD(ADD(LA(11), LE(11)), bs1_c(E14)), ch_c(E14, E13, LE(12))), LD(K[15])));
    W f15b = MSK(ADD(ADD(ADD(ADD(LAB(11), LEB(11)), bs1_c(E14b)), ch_c(E14b, E13, LEB(12))), LD(K[15])));
    W e4 = CMPEQ(f15, f15b); BR(); if (!e4) continue;
    for (int u = 0; u < (1 << 12); u++) {
      OPS += 3;
      hs->it15++; OPS += 3;
      W E15 = AND(sm_c(rs), M); W W15 = MSK(SUB(E15, f15));
      W E16 = MSK(ADD(ADD(ADD(ADD(ADD(LA(12), LE(12)), bs1_c(E15)), ch_c(E15, E14, E13)), LD(K[16])), g));
      W E16b = MSK(ADD(ADD(ADD(ADD(ADD(ADD(LAB(12), LEB(12)), bs1_c(E15)), ch_c(E15, E14b, E13)), LD(K[16])), g), LD(D9)));
      W e5 = CMPEQ(E16, E16b); BR(); if (!e5) continue;
      W A15 = MSK(ADD(ADD(SUB(E15, LA(11)), bs0_c(A14)), maj_c(A14, A13, LA(12)))); (void)A15;
      W f17 = MSK(ADD(ADD(ADD(A13, E13), bs1_c(E16)), ch_c(E16, E15, E14)));
      W f17b = MSK(ADD(ADD(ADD(A13, E13), bs1_c(E16)), ch_c(E16, E15, E14b)));
      W e6 = CMPEQ(f17, f17b); BR(); if (!e6) continue;
      ST(Wv[13], (uint32_t)W13); ST(Wv[15], (uint32_t)W15); return 1;
    }
    OPS += 1;
  }
  return 0;
}

static void digest_c(const uint32_t m0[16], const uint32_t m1[16], uint32_t out[8]) {
  uint32_t cv[8], cv2[8], pad[16] = {0}; OPS += 16; pad[0] = 0x80000000u; pad[15] = 1024;   /* 16 stores */
  compress31_c(IV, m0, cv); compress31_c(cv, m1, cv2); compress31_c(cv2, pad, out);
}

/* rec address: base + 6*r (records are six words) */
#define RADDR(r) ADD(ADD(SHL((W)(r), 2), SHL((W)(r), 1)), 0)

/* RT: the sorted record table; the search check passes r31det3's own (qsort) order so that the
   record loop visits equal-key records in the same order */
static const rec_t *RT;
static int hit_c(const uint32_t m[15], uint32_t x, uint64_t *rs, hstat_t *hs) {
  uint64_t o0 = OPS;
  hs->bmhits++; OPS += 3;
  uint32_t mm[16]; for (int i = 0; i < 15; i++) ST(mm[i], (uint32_t)LD(m[i])); ST(mm[15], x);
  uint32_t cv[8]; compress31_c(IV, mm, cv);
  W key = LD(cv[0]);
  W lo = 0, hi = LD(nrec_c); OPS++;                    /* lo = 0 */
  int it = 0;
  while (1) {
    W c = CMPLT(lo, hi); BR(); if (!c) break;
    it++;
    W mid = SHR(ADD(lo, hi), 1);
    W addr = RADDR(mid); (void)addr;
    W k = LD(RT[(int)mid].key);
    W lt = CMPLT(k, key); BR();
    if (lt) lo = ADD(mid, C1); else hi = OR(mid, 0);
  }
  if ((uint64_t)it > hs->bsearch_max) hs->bsearch_max = it;
  W out = CMPLT(lo, LD(nrec_c)); BR();
  int found = 0;
  if (out) { W addr = RADDR(lo); (void)addr; W k = LD(RT[(int)lo].key); W e = CMPEQ(k, key); BR(); found = (int)e; }
  /* worst path of this segment: 18 iterations (n = 132096 < 2^18), each 12 primitives on either branch */
  uint64_t segH = OPS - o0 + (uint64_t)(18 - it) * 12;
  if (segH > hs->maxH) hs->maxH = segH;
  if (!found) return 0;
  hs->keyhits++; OPS += 3;
  int ret = 0;
  for (int r = (int)lo; ; r++) {
    uint64_t r0 = OPS;
    W c1 = CMPLT((W)r, LD(nrec_c)); BR(); if (!c1) { if (OPS - r0 > hs->maxKx) hs->maxKx = OPS - r0; break; }
    W addr = RADDR(r); (void)addr; W kr = LD(RT[r].key); W c2 = CMPEQ(kr, key); BR();
    if (!c2) { if (OPS - r0 > hs->maxKx) hs->maxKx = OPS - r0; break; }
    OPS += 1;                                         /* r++ */
    const rec_t *q = &RT[r]; hs->recs++; OPS += 3;
    W Am1 = LD(cv[0]), Am2 = LD(cv[1]), Am3 = LD(cv[2]), Am4 = LD(cv[3]), Em1 = LD(cv[4]), Em2 = LD(cv[5]), Em3 = LD(cv[6]), Em4 = LD(cv[7]);
    W A0 = LD(q->A0), A1 = LD(AA(1)), A2 = LD(AA(2));
    W E0 = MSK(SUB(SUB(ADD(A0, Am4), bs0_c(Am1)), maj_c(Am1, Am2, Am3)));
    W E1 = MSK(SUB(SUB(ADD(A1, Am3), bs0_c(A0)), maj_c(A0, Am1, Am2)));
    W E2 = MSK(SUB(SUB(ADD(A2, Am2), bs0_c(A1)), maj_c(A1, A0, Am1)));
    W E3 = LD(q->E3), E4 = LD(q->E4), E5 = LD(EA(5)), E6 = LD(EA(6));
    W Ex[11] = {Em4, Em3, Em2, Em1, E0, E1, E2, E3, E4, E5, E6};   /* index i+4 */
    W Ax[7] = {Am4, Am3, Am2, Am1, A0, A1, A2};                    /* index i+4 */
    uint32_t Wv[16];
    for (int i = 0; i <= 6; i++) {
      W v = MSK(SUB(SUB(SUB(SUB(SUB(Ex[i + 4], Ax[i]), Ex[i]), bs1_c(Ex[i + 3])), ch_c(Ex[i + 3], Ex[i + 2], Ex[i + 1])), LD(K[i])));
      ST(Wv[i], (uint32_t)v);
    }
    ST(Wv[7], (uint32_t)LD(q->W7)); ST(Wv[8], (uint32_t)LD(q->W8));
    for (int i = 9; i <= 12; i++) ST(Wv[i], (uint32_t)LD(S_W[i]));
    ST(Wv[13], 0u); ST(Wv[14], 0u); ST(Wv[15], 0u);
    W W6 = LD(Wv[6]);
    W d6 = MSK(SUB(sg0_c(MSK(ADD(W6, LD(D6)))), sg0_c(W6)));
    W v6 = CMPEQ(d6, LD(C6)); BR();
    uint64_t segR = OPS - r0; if (segR > hs->maxR) hs->maxR = segR;
    if (!v6) continue;
    uint64_t v0 = OPS;
    hs->v6++; OPS += 3;
    W W5 = LD(Wv[5]);
    W tgt = MSK(SUB(0, MSK(SUB(sg0_c(MSK(ADD(W5, LD(D5)))), sg0_c(W5)))));
    W c18 = ADD(ADD(LD(Wv[11]), sg0_c(LD(Wv[3]))), LD(Wv[2]));
    int gsel = -1;
    for (int k = 0; ; k++) {
      W c = CMPLT((W)k, LD(ng16_c)); BR(); if (!c) break;
      W gaddr = ADD(0, (W)k); W gk = LD(G16_c[(int)gaddr]);
      W w18 = MSK(ADD(sg1_c(gk), c18));
      W d = MSK(SUB(sg1_c(MSK(ADD(w18, LD(D18)))), sg1_c(w18)));
      W e = CMPEQ(d, tgt); BR();
      if (e) { gsel = k; break; }
      OPS += 1;                                       /* k++ */
    }
    uint64_t segV = OPS - v0;
    if (gsel < 0) { if (segV > hs->maxV) hs->maxV = segV; }     /* all 64 candidates tried: the worst path */
    else hs->segVfound = segV;
    if (gsel < 0) continue;
    uint64_t c0 = OPS;
    hs->joint++; OPS += 9;                            /* joint, both, comp_try counters */
    uint32_t Wc[16]; for (int i = 0; i < 16; i++) ST(Wc[i], (uint32_t)LD(Wv[i]));
    int ok = complete_c(Wc, LD(G16_c[gsel]), rs, hs);
    if (!ok) { hs->opsC += OPS - c0; continue; }
    hs->comp_ok++; OPS += 3;
    uint32_t Wb[16]; for (int i = 0; i < 16; i++) ST(Wb[i], (uint32_t)LD(Wc[i]));
    const uint32_t dd[5] = {D5, D6, D7, D8, D9};
    for (int i = 0; i < 5; i++) ST(Wb[5 + i], (uint32_t)MSK(ADD(LD(Wb[5 + i]), LD(dd[i]))));
    uint32_t h1[8], h2[8]; digest_c(mm, Wc, h1); digest_c(mm, Wb, h2);
    int same = 1, diff = 0;
    for (int i = 0; i < 8; i++) { W e = CMPEQ(LD(h1[i]), LD(h2[i])); BR(); same &= (int)e; }
    for (int i = 0; i < 16; i++) { W e = CMPEQ(LD(Wc[i]), LD(Wb[i])); BR(); diff |= !(int)e; }
    if (same && diff) {
      hs->coll++; OPS += 3; ret = 1;
      memcpy(hs->M1, Wc, 64); memcpy(hs->M1b, Wb, 64); OPS += 16 + 16 + 16 + 8;  /* output: 56 words written */
    }
    hs->opsC += OPS - c0;
    if (ret) return 1;
  }
  return ret;
}

/* ---------------- reference: worker's lane block of B.4, verbatim ---------------- */
typedef struct { uint32_t a, b, cc, d, e, f, gg, h, m16, m18, m20, c17, c19, c21, c22, c23, c24, c25, c26, c27, c28, c29, c30; } refg_t;
static void ref_group(uint64_t g, uint32_t m[15], refg_t *R, uint64_t *crs) {
  uint64_t rs = seed_base ^ (g * 0x9e3779b97f4a7c15ull) ^ 0x5bd1e9955bd1e995ull;
  for (int i = 0; i < 15; i++) m[i] = (uint32_t)sm(&rs);
  *crs = seed_base ^ (g * 0xd1b54a32d192ed03ull) ^ 0x2545f4914f6cdd1dull;
  uint32_t a = IV[0], b = IV[1], cc = IV[2], d = IV[3], e = IV[4], f = IV[5], gg = IV[6], h = IV[7];
  for (int t = 0; t < 15; t++) { uint32_t T1 = h + BS1(e) + IF(e, f, gg) + K[t] + m[t]; uint32_t T2 = BS0(a) + MAJ(a, b, cc); h = gg; gg = f; f = e; e = d + T1; d = cc; cc = b; b = a; a = T1 + T2; }
  const uint32_t m16 = s1(m[14]) + m[9] + s0(m[1]) + m[0], m18 = s1(m16) + m[11] + s0(m[3]) + m[2], m20 = s1(m18) + m[13] + s0(m[5]) + m[4];
  *R = (refg_t){a, b, cc, d, e, f, gg, h, m16, m18, m20,
    m[10] + s0(m[2]) + m[1], m[12] + s0(m[4]) + m[3], m[14] + s0(m[6]) + m[5], s1(m20) + s0(m[7]) + m[6],
    m16 + s0(m[8]) + m[7], s0(m[9]) + m[8], m18 + s0(m[10]) + m[9], s0(m[11]) + m[10],
    m20 + s0(m[12]) + m[11], s0(m[13]) + m[12], s0(m[14]) + m[13], m[14]};
}
static uint32_t ref_key(const refg_t *R, uint32_t x) {
  const uint32_t a = R->a, b = R->b, cc = R->cc, d = R->d, e = R->e, f = R->f, gg = R->gg, h = R->h;
  const uint32_t m16 = R->m16, m18 = R->m18, m20 = R->m20, c17 = R->c17, c19 = R->c19, c21 = R->c21, c22 = R->c22;
  const uint32_t c23 = R->c23, c24 = R->c24, c25 = R->c25, c26 = R->c26, c27 = R->c27, c28 = R->c28, c29 = R->c29, c30 = R->c30;
  uint32_t w17=s1(x)+c17, w19=s1(w17)+c19, w21=s1(w19)+c21, w22=c22+x, w23=s1(w21)+c23, w24=s1(w22)+w17+c24;
  uint32_t w25=s1(w23)+c25, w26=s1(w24)+w19+c26, w27=s1(w25)+c27, w28=s1(w26)+w21+c28, w29=s1(w27)+w22+c29, w30=s1(w28)+w23+s0(x)+c30;
  uint32_t A=a,B=b,C=cc,D=d,E=e,F=f,G=gg,H=h,T1,T2;
  RND(x,K[15]) RND(m16,K[16]) RND(w17,K[17]) RND(m18,K[18]) RND(w19,K[19]) RND(m20,K[20]) RND(w21,K[21]) RND(w22,K[22])
  RND(w23,K[23]) RND(w24,K[24]) RND(w25,K[25]) RND(w26,K[26]) RND(w27,K[27]) RND(w28,K[28]) RND(w29,K[29]) RND(w30,K[30])
  return IV[0]+A;
}

/* ---------------- search validation on whole groups ---------------- */
typedef struct { uint64_t g; uint32_t jend; int tid; hstat_t hs; ctr_t ref; uint64_t trials, lane_ops_min, lane_ops_max, lane_ref_ops,
                 lane_plain_ops, gsetup_ops, ghead_ops, abort_ops, aborts, pass_ops_min, pass_ops_max, refhits, found_ref, found_c; uint32_t refM1[16]; } gv_t;
/* worker's loop control (B.4), counted.  Group head: g += NTH, load best_n and stop_flag, test both,
   g > best_n >> 24, base = 0.  Abort check (at base & 0xfffff == 0, 16 times per group): two loads,
   shift, two compares, three branches.  Pass tail: trials += 8 (load, add, store), the base test
   (and, compare, branch), the pass loop (compare, branch). */
static uint64_t stop_dummy, best_dummy = UINT64_MAX;
static void group_head_c(uint64_t g) {
  W gn = ADD((W)g, LD(12)); (void)gn;
  W bn = LD(best_dummy); W sf = LD(stop_dummy); W c1 = CMPNZ(sf); BR(); W c2 = CMPEQ(bn, (W)UINT64_MAX); BR();
  W c3 = CMPLT(SHR(bn, 24), (W)g); BR(); (void)c1; (void)c2; (void)c3;
  W base = AND((W)0, M); (void)base;                 /* base = 0 */
}
static void abort_check_c(uint64_t g) {
  W sf = LD(stop_dummy); W c1 = CMPNZ(sf); BR(); W bn = LD(best_dummy); W c2 = CMPEQ(bn, (W)UINT64_MAX); BR();
  W c3 = CMPLT(SHR(bn, 24), (W)g); BR(); (void)c1; (void)c2; (void)c3;
}
static uint64_t trial_ctr;
static int pass_tail_c(W base) {
  ST(trial_ctr, (uint64_t)ADD(LD(trial_ctr), LD(8)));
  W t = CMPEQ(AND(base, LD(0xfffff)), 0); BR();
  W more = CMPLT(ADD(base, LD(8)), LD(1u << 24)); BR(); (void)more;
  return (int)t;
}

static void *gval_worker(void *arg) {
  gv_t *v = arg; OPS = 0;
  uint32_t m[15], mr[15]; gval_t G; refg_t R; uint64_t crs, crs_ref;
  uint64_t o0 = OPS; group_head_c(v->g); v->ghead_ops = OPS - o0;
  o0 = OPS; gsetup_c(v->g, m, &G, &crs); v->gsetup_ops = OPS - o0;
  ref_group(v->g, mr, &R, &crs_ref);
  assert(memcmp(m, mr, 60) == 0 && crs == crs_ref);
  v->lane_ops_min = v->pass_ops_min = UINT64_MAX;
  memset(&ctrs[v->tid], 0, sizeof(ctr_t));
  uint64_t crs_c = crs; int done = 0;
  for (uint32_t base = 0; base < v->jend && !done; base += 8) {
    uint64_t p0 = OPS, hitops = 0;
    W x = (W)base;
    for (int j = 0; j < 8; j++) {
      uint32_t xi = (uint32_t)x;
      if (xi >= v->jend) { done = 1; break; }
      uint32_t kc, kr = ref_key(&R, xi), kref;
      uint64_t l0 = OPS;
      int hit = klane_opt(&G, x, bitmap_c, &kc);
      uint64_t lo = OPS - l0;
      if (lo < v->lane_ops_min) v->lane_ops_min = lo;
      if (lo > v->lane_ops_max) v->lane_ops_max = lo;
      if ((xi & 1023) == 0) {
        uint64_t r0 = OPS; (void)klane_ref(&G, x, bitmap_c, &kref); v->lane_ref_ops = OPS - r0; OPS = r0; assert(kref == kr);
        r0 = OPS; (void)klane(&G, x, bitmap_c, &kref); v->lane_plain_ops = OPS - r0; OPS = r0; assert(kref == kr);
      }
      assert(kc == kr);
      uint32_t bi = kr >> 8; int hit_ref = (int)(bitmap[bi >> 6] >> (bi & 63) & 1);
      assert(hit == hit_ref);
      v->trials++;
      if (hit) {
        uint32_t mm[16]; memcpy(mm, mr, 60); mm[15] = xi;
        int fr = process_hit(v->tid, mm, &crs_ref, 0);
        uint64_t h0 = OPS;
        int fc = hit_c(m, xi, &crs_c, &v->hs);
        hitops += OPS - h0;
        assert(fr == fc);
        if (fr) { v->found_ref = xi; v->found_c = xi; done = 1; break; }
      }
      x = ADD(x, C1);
    }
    if (done) break;
    int chk = pass_tail_c((W)base);
    uint64_t po = OPS - p0 - hitops;
    if (chk) { uint64_t a0 = OPS; abort_check_c(v->g); v->abort_ops = OPS - a0; v->aborts++; }
    if (po < v->pass_ops_min) v->pass_ops_min = po;
    if (po > v->pass_ops_max) v->pass_ops_max = po;
  }
  v->ref = ctrs[v->tid];
  return NULL;
}

int main(int argc, char **argv) {
  seed_base = 0xdfafc947679ebe06ull;                  /* committed seed of K (Appendix A.2) */
  outf = stderr;
  build_s1inv(); build_table();                       /* r31det3's own table: the reference */
  build_table_c();
  printf("table: V7=512 V8=49408 G16=%d records=%d identical to build_table (sets, records, bitmap)\n", ng16_c, nrec_c);
  printf("ops P1 %llu (%.4f per word)  P2 %llu  sort %llu  bitmap %llu\n", (unsigned long long)ops_p1, ops_p1 / 4294967296.0,
         (unsigned long long)ops_p2, (unsigned long long)ops_sort, (unsigned long long)ops_bitmap);
  build_s1inv_c();
  printf("ops s1inv+check %llu\n", (unsigned long long)ops_s1inv);
  /* selftest of B.4, counted: 2000 blocks: 16 draws, group values, lane, compress31, compare */
  {
    OPS = 0; uint64_t r2 = 7;
    for (int t = 0; t < 2000; t++) {
      OPS += 3;                                       /* t < 2000, branch, t++ */
      uint32_t mb[16]; for (int i = 0; i < 16; i++) ST(mb[i], (uint32_t)AND(sm_c(&r2), M));
      gval_t G; gvalues_from_words(mb, &G);
      uint32_t kc; (void)klane_opt(&G, LD(mb[15]), bitmap_c, &kc);
      uint32_t ref[8]; compress31_c(IV, mb, ref);
      W ok = CMPEQ(LD(ref[0]), kc); BR(); assert(ok);
    }
    ops_selftest = OPS;
    printf("ops selftest %llu (2000 blocks)\n", (unsigned long long)ops_selftest);
  }
  /* search validation: groups 0..3 in full, group 5920 up to its stored pair */
  RT = recs;
  uint64_t groups[] = {0, 1, 2, 3, 5920}; int ng = 5;
  gv_t v[5]; pthread_t th[5];
  for (int i = 0; i < ng; i++) { memset(&v[i], 0, sizeof v[i]); v[i].g = groups[i]; v[i].jend = groups[i] == 5920 ? 4561628u : (1u << 24); v[i].tid = 20 + i; pthread_create(&th[i], 0, gval_worker, &v[i]); }
  uint64_t T = 0, H = 0, maxH = 0, maxR = 0, maxV = 0, maxKx = 0, bsm = 0;
  for (int i = 0; i < ng; i++) {
    pthread_join(th[i], 0);
    ctr_t *r = &v[i].ref; hstat_t *h = &v[i].hs;
    printf("group %llu: trials %llu, lane ops %llu..%llu (plain %llu, ref-style %llu), set-up %llu ops; hits %llu/%llu keyhits %llu/%llu recs %llu/%llu v6 %llu/%llu joint %llu/%llu it13 %llu/%llu it15 %llu/%llu coll %llu/%llu\n",
      (unsigned long long)v[i].g, (unsigned long long)v[i].trials, (unsigned long long)v[i].lane_ops_min, (unsigned long long)v[i].lane_ops_max,
      (unsigned long long)v[i].lane_plain_ops, (unsigned long long)v[i].lane_ref_ops, (unsigned long long)v[i].gsetup_ops,
      (unsigned long long)h->bmhits, (unsigned long long)r->bmhits, (unsigned long long)h->keyhits, (unsigned long long)r->keyhits,
      (unsigned long long)h->recs, (unsigned long long)r->recs, (unsigned long long)h->v6, (unsigned long long)r->v6,
      (unsigned long long)h->joint, (unsigned long long)r->joint, (unsigned long long)h->it13, (unsigned long long)r->it13,
      (unsigned long long)h->it15, (unsigned long long)r->it15, (unsigned long long)h->coll, (unsigned long long)r->coll);
    assert(h->bmhits == r->bmhits && h->keyhits == r->keyhits && h->recs == r->recs && h->v6 == r->v6 && h->joint == r->joint &&
           h->it13 == r->it13 && h->it15 == r->it15 && h->coll == r->coll);
    printf("  pass ops %llu..%llu (8 lanes + loop), group head %llu, abort check %llu x %llu, V6 found-path %llu\n",
      (unsigned long long)v[i].pass_ops_min, (unsigned long long)v[i].pass_ops_max, (unsigned long long)v[i].ghead_ops,
      (unsigned long long)v[i].abort_ops, (unsigned long long)v[i].aborts, (unsigned long long)h->segVfound);
    T += v[i].trials; H += h->bmhits;
    if (h->maxH > maxH) maxH = h->maxH;
    if (h->maxR > maxR) maxR = h->maxR;
    if (h->maxV > maxV) maxV = h->maxV;
    if (h->maxKx > maxKx) maxKx = h->maxKx;
    if (h->bsearch_max > bsm) bsm = h->bsearch_max;
    if (h->coll) {
      printf("stored pair reproduced: n = %llu\nM1  ", (unsigned long long)((v[i].g << 24) | v[i].found_c));
      for (int j = 0; j < 16; j++) printf("%08x", h->M1[j]);
      printf("\nM1' "); for (int j = 0; j < 16; j++) printf("%08x", h->M1b[j]);
      printf("\ncompletion segment (R20 pass to stored pair): %llu ops\n", (unsigned long long)h->opsC);
    }
  }
  printf("validated trials %llu, bitmap hits %llu; worst paths: bitmap hit %llu (binary search <= 18, observed max %llu), key-matched hit %llu (counter + final loop test), record %llu, V6 pass %llu (64 candidates)\n",
         (unsigned long long)T, (unsigned long long)H, (unsigned long long)maxH, (unsigned long long)bsm, (unsigned long long)(3 + maxKx),
         (unsigned long long)maxR, (unsigned long long)maxV);
  return 0;
}

/* group values from given words 0..14 (the counted body of gsetup_c after the draws) */
#define LM(i) LD(m[i])
#define SG(field, v) ST(G->field, (uint32_t)MSK(v))
static void gvalues_from_words(const uint32_t m[15], gval_t *G) {
  W a = LD(IV[0]), b = LD(IV[1]), c = LD(IV[2]), d = LD(IV[3]), e = LD(IV[4]), f = LD(IV[5]), gg = LD(IV[6]), h = LD(IV[7]);
  for (int t = 0; t < 15; t++) {
    W T1 = ADD(ADD(ADD(ADD(h, bs1_c(e)), ch_c(e, f, gg)), LD(K[t])), LD(m[t]));
    W T2 = ADD(bs0_c(a), maj_c(a, b, c));
    h = gg; gg = f; f = e; e = MSK(ADD(d, T1)); d = c; c = b; b = a; a = MSK(ADD(T1, T2));
  }
  W m16 = MSK(ADD(ADD(ADD(sg1_c(LM(14)), LM(9)), sg0_c(LM(1))), LM(0)));
  W m18 = MSK(ADD(ADD(ADD(sg1_c(m16), LM(11)), sg0_c(LM(3))), LM(2)));
  W m20 = MSK(ADD(ADD(ADD(sg1_c(m18), LM(13)), sg0_c(LM(5))), LM(4)));
  W p15 = ADD(ADD(ADD(h, bs1_c(e)), ch_c(e, f, gg)), LD(K[15]));
  W q15 = ADD(bs0_c(a), maj_c(a, b, c));
  SG(U15, ADD(d, p15)); SG(V15, ADD(p15, q15));
  ST(G->a, (uint32_t)a); ST(G->b, (uint32_t)b); ST(G->c, (uint32_t)c); ST(G->e, (uint32_t)e); ST(G->f, (uint32_t)f);
  ST(G->ab, (uint32_t)AND(a, b)); ST(G->axb, (uint32_t)XOR(a, b)); ST(G->exf, (uint32_t)XOR(e, f));
  SG(P16, ADD(ADD(gg, LD(K[16])), m16)); SG(P17, ADD(f, LD(K[17]))); SG(P18, ADD(ADD(e, LD(K[18])), m18));
  SG(KW20, ADD(LD(K[20]), m20));
  SG(c17, ADD(ADD(LM(10), sg0_c(LM(2))), LM(1))); SG(c19, ADD(ADD(LM(12), sg0_c(LM(4))), LM(3)));
  SG(c21, ADD(ADD(LM(14), sg0_c(LM(6))), LM(5))); SG(c22, ADD(ADD(sg1_c(m20), sg0_c(LM(7))), LM(6)));
  SG(c23, ADD(ADD(m16, sg0_c(LM(8))), LM(7))); SG(c24, ADD(sg0_c(LM(9)), LM(8)));
  SG(c25, ADD(ADD(m18, sg0_c(LM(10))), LM(9))); SG(c26, ADD(sg0_c(LM(11)), LM(10)));
  SG(c27, ADD(ADD(m20, sg0_c(LM(12))), LM(11))); SG(c28, ADD(sg0_c(LM(13)), LM(12)));
  SG(c29k, ADD(ADD(sg0_c(LM(14)), LM(13)), LD(K[29]))); SG(c30k, ADD(ADD(LM(14), LD(K[30])), LD(IV[0])));
  ST(G->K19, (uint32_t)LD(K[19])); ST(G->K21, (uint32_t)LD(K[21])); ST(G->K22, (uint32_t)LD(K[22])); ST(G->K23, (uint32_t)LD(K[23]));
  ST(G->K24, (uint32_t)LD(K[24])); ST(G->K25, (uint32_t)LD(K[25])); ST(G->K26, (uint32_t)LD(K[26])); ST(G->K27, (uint32_t)LD(K[27]));
  ST(G->K28, (uint32_t)LD(K[28]));
}
```

C.8 Output of the K validation runs (2026-10-08)

`kprog.py` in its three variants:

```
mode opt: 582 primitives per trial, 20000 trials match the organizer reference core (word 0 of compress31), registers needed 22
histogram {'add': 117, 'and': 73, 'br': 1, 'cmp': 1, 'ld': 35, 'ldx': 1, 'or': 41, 'shl': 41, 'shr': 128, 'shrv': 1, 'xor': 143}
mode plain: 775 primitives per trial, 20000 trials match the organizer reference core (word 0 of compress31), registers needed 20
histogram {'add': 117, 'and': 117, 'br': 1, 'cmp': 1, 'ld': 37, 'ldx': 1, 'not': 15, 'or': 114, 'shl': 114, 'shr': 128, 'shrv': 1, 'xor': 129}
mode ref: 1035 primitives per trial, 20000 trials match the organizer reference core (word 0 of compress31), registers needed 20
histogram {'add': 117, 'and': 377, 'br': 1, 'cmp': 1, 'ld': 37, 'ldx': 1, 'not': 15, 'or': 114, 'shl': 114, 'shr': 128, 'shrv': 1, 'xor': 129}
```

`./kcount`, standard output:

```
table: V7=512 V8=49408 G16=64 records=132096 identical to build_table (sets, records, bitmap)
ops P1 236223301254 (55.0000 per word)  P2 81321704  sort 81135912  bitmap 1847296
ops s1inv+check 608280
ops selftest 30630000 (2000 blocks)
group 0: trials 16777216, lane ops 582..582 (plain 775, ref-style 1035), set-up 13349 ops; hits 9958/9958 keyhits 224/224 recs 447/447 v6 3/3 joint 0/0 it13 0/0 it15 0/0 coll 0/0
  pass ops 4677..4677 (8 lanes + loop), group head 12, abort check 9 x 16, V6 found-path 0
group 1: trials 16777216, lane ops 582..582 (plain 775, ref-style 1035), set-up 13349 ops; hits 9931/9931 keyhits 245/245 recs 561/561 v6 4/4 joint 0/0 it13 0/0 it15 0/0 coll 0/0
  pass ops 4677..4677 (8 lanes + loop), group head 12, abort check 9 x 16, V6 found-path 0
group 2: trials 16777216, lane ops 582..582 (plain 775, ref-style 1035), set-up 13349 ops; hits 10069/10069 keyhits 260/260 recs 575/575 v6 0/0 joint 0/0 it13 0/0 it15 0/0 coll 0/0
  pass ops 4677..4677 (8 lanes + loop), group head 12, abort check 9 x 16, V6 found-path 0
group 3: trials 16777216, lane ops 582..582 (plain 775, ref-style 1035), set-up 13349 ops; hits 9971/9971 keyhits 251/251 recs 526/526 v6 0/0 joint 0/0 it13 0/0 it15 0/0 coll 0/0
  pass ops 4677..4677 (8 lanes + loop), group head 12, abort check 9 x 16, V6 found-path 0
group 5920: trials 4561628, lane ops 582..582 (plain 775, ref-style 1035), set-up 13349 ops; hits 2654/2654 keyhits 57/57 recs 133/133 v6 2/2 joint 1/1 it13 2829/2829 it15 19/19 coll 1/1
  pass ops 4677..4677 (8 lanes + loop), group head 12, abort check 9 x 5, V6 found-path 1656
stored pair reproduced: n = 99325680347
M1  1e2dbac805e61a5ecd7fcb499db00a7a186cabb0f7efd9c22a442578023cd6ebf71d59bf876b73dbed1499e47173c1450ba5f907b35ebf9305848707075e188d
M1' 1e2dbac805e61a5ecd7fcb499db00a7a186cabb0f7efc9c82a64ad69522c8ce51f1e6abf876bf3dfed1499e47173c1450ba5f907b35ebf9305848707075e188d
completion segment (R20 pass to stored pair): 2533318 ops
validated trials 71670492, bitmap hits 42583; worst paths: bitmap hit 1642 (binary search <= 18, observed max 18), key-matched hit 13 (counter + final loop test), record 238, V6 pass 2344 (64 candidates)
```

`./kcount`, standard error (printed by `r31det3.c`'s own `build_table` and `process_hit`):

```
V7=512 V8=49408 G16=64 records=132096
COLLISION tid=24
M0 e7f5ce551741facd279a66b68a38d7c6cc332e48ed9dd62a6b76b5f73aa91ac91ca8034eb4a9ad705b8eeceb50a7afad07617b89719682b5394303d800459adb
M1 1e2dbac805e61a5ecd7fcb499db00a7a186cabb0f7efd9c22a442578023cd6ebf71d59bf876b73dbed1499e47173c1450ba5f907b35ebf9305848707075e188d
M1b 1e2dbac805e61a5ecd7fcb499db00a7a186cabb0f7efc9c82a64ad69522c8ce51f1e6abf876bf3dfed1499e47173c1450ba5f907b35ebf9305848707075e188d
DIGEST aea2562b20b12c5938046802bcc533817087f43c3e4ac864114c2abdd2249ee5
```

C.9 `pcount.c` (the pre-construction analysis programs as counted programs, Section 15.2) and its runs

    2f1d1b37bdbffe70ccc97744d6786495d3cba445b46257a87d5e782722e2b953  pcount.c

`cc -O2 -o pcount pcount.c -lpthread -lm`, then `./pcount sets`, `table`, `joint`, `pany`, `pany2-1-20` and
`pany2-12-28`. Output of each (its standard output, then the count on standard error) and the comparison with the
original program:

```
== sets
W5 modular=16384 signed+modular=16384
W6 modular=8388608 signed+modular=8388608
W7 modular=512 signed+modular=512
W8 modular=49408 signed+modular=8192
W9 modular=35921920 signed+modular=33554432
W16 modular=64 signed+modular=64
W18 modular=42467328 signed+modular=33554432
OPS sets 461151205710
identical to the output of the original program (re-run)
== table
published record present: A-1=c0a93f38 E3=9f3c306a E4=60e73dda A0=7535928e
V7 512 V8 49408
V8 size 49408, (W8,E4) survivors 1632, tuples 16896
OPS table 158924192620
identical to the output of the original program (re-run)
== joint
distinct sigma0-diff values for d5: 6580932 ; sigma1-diff values for d18: 758851
P(W5 in V5)=2^-18.000 ; single-g joint=2^-18.104 ; 64-g union bound joint=2^-12.104 ; strict*0.136=2^-20.877
top sigma0-diff for d5 (count):
  08017e20 16777252 p18(-c)=2^-61.90
  080181e0 16777252 p18(-c)=2^-61.90
  07ff7e20 16777220 p18(-c)=2^-61.90
  07ff81e0 16777220 p18(-c)=2^-61.90
  08007e20 16777220 p18(-c)=2^-61.90
OPS joint 644688249115
identical to the output of the original program (re-run)
== pany
|G16|=64
P_any(joint, 64 g)=2^-12.662 ; P(strict G18 exists g)=0.1360 ; strict P=2^-20.878
OPS pany 569745544349
identical to the output of the original program (re-run)
== pany2-1-20
|G16|=64 samples=2^20 mean=1.536128e-04 (2^-12.6684) se=7.276e-07 99%LCB=1.517385e-04 (2^-12.6861) 99%UCB=2^-12.6509 max_term_bound=2.500e-01
OPS pany2-1-20 410842675669
identical to the output of the original program (re-run)
== pany2-12-28
|G16|=64 samples=2^27 mean=1.543086e-04 (2^-12.6619) se=4.564e-08 99%LCB=1.541910e-04 (2^-12.6630) 99%UCB=2^-12.6608 max_term_bound=2.500e-01
OPS pany2-12-28 2858761574204
identical to the saved output of the original run (pany2.out)
```

```c
/* pcount.c: the pre-construction analysis programs (sets, table x2, joint, pany, pany2 x2;
   proof Section 15.2) as counted programs of 256-bit word-RAM primitives.

   Each function computes what the original program computes and prints the same line(s) in the
   same format, so its output can be compared with a re-run of the original.  Primitives as in
   kcount.c: one count each; values reduced to 32 or 64 bits before every right shift and
   comparison; rotations via dup(v) = v | v << 32.  Multiplication by the hash constant
   2654435761 = 0x9e3779b1 is shift-and-add over its 19 set bits.  Floating-point operations are
   charged at the tariffs of the checked emulations of heavy.py (Appendix C.11): conversion 152,
   addition 240, multiplication 520, comparison 48, division 824, square root 1008.

   pany and pany2 sum the integer counts returned by the hash lookups in an integer register and
   convert the sum once.  The original adds the converted counts (pany: count / 2^32) in double
   precision; every partial sum is an integer multiple of the same power of two below 2^53 of it,
   so each addition is exact and the result is bit-identical.

   cc -O2 -o pcount pcount.c -lpthread -lm
   ./pcount <program>     program: sets | table | joint | pany | pany2-1-20 | pany2-12-28 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <pthread.h>

typedef unsigned __int128 W;
static __thread uint64_t OPS;
static inline W ADD(W a, W b) { OPS++; return a + b; }
static inline W SUB(W a, W b) { OPS++; return a - b; }
static inline W AND(W a, W b) { OPS++; return a & b; }
static inline W OR(W a, W b)  { OPS++; return a | b; }
static inline W XOR(W a, W b) { OPS++; return a ^ b; }
static inline W NOT(W a)      { OPS++; return ~a; }
static inline W SHR(W a, int n) { OPS++; return a >> n; }
static inline W SHL(W a, int n) { OPS++; return a << n; }
static inline W LD(W v)       { OPS++; return v; }
static inline W CMPEQ(W a, W b) { OPS++; return a == b; }
static inline W CMPLT(W a, W b) { OPS++; return a < b; }
static inline W CMPNZ(W a)    { OPS++; return a != 0; }
#define ST(dst,v) do { W st_v_ = (v); OPS++; (dst) = st_v_; } while (0)
#define BR()     (OPS++)
static const W M = 0xffffffffu, M64 = 0xffffffffffffffffull, C1 = 1;
static inline W MSK(W a) { return AND(a, M); }
/* floating point at the tariffs of heavy.py (Appendix C.11): each is the largest primitive count of the
   checked binary64 emulation, rounded up to a multiple of 8 */
#define T_CVTF 152
#define T_FADD 240
#define T_FMUL 520
#define T_FCMP 48
#define T_FDIV 824
#define T_FSQRT 1008
static inline double FCVT(W a) { OPS += T_CVTF; return (double)(uint64_t)a; }
static inline double FADD(double a, double b) { OPS += T_FADD; return a + b; }
static inline double FMUL(double a, double b) { OPS += T_FMUL; return a * b; }
static inline int FCMPGT(double a, double b) { OPS += T_FCMP; return a > b; }

static inline W dup_c(W v) { return OR(v, SHL(v, 32)); }
static inline W s0d(W d, W v) { return XOR(XOR(SHR(d, 7), SHR(d, 18)), SHR(v, 3)); }
static inline W s1d(W d, W v) { return XOR(XOR(SHR(d, 17), SHR(d, 19)), SHR(v, 10)); }
static inline W s0c(W v) { return s0d(dup_c(v), v); }
static inline W s1c(W v) { return s1d(dup_c(v), v); }
static inline W S0c(W v) { W d = dup_c(v); return XOR(XOR(SHR(d, 2), SHR(d, 13)), SHR(d, 22)); }
static inline W S1c(W v) { W d = dup_c(v); return XOR(XOR(SHR(d, 6), SHR(d, 11)), SHR(d, 25)); }
static inline W IFc(W x, W y, W z) { return XOR(z, AND(x, XOR(y, z))); }
static inline W MAJc(W a, W b, W c) { return OR(AND(a, b), AND(c, OR(a, b))); }

/* reference (uncounted) for checks */
static inline uint32_t R(uint32_t x, int n) { return (x >> n) | (x << (32 - n)); }
static inline uint32_t s0(uint32_t x) { return R(x, 7) ^ R(x, 18) ^ (x >> 3); }
static inline uint32_t s1(uint32_t x) { return R(x, 17) ^ R(x, 19) ^ (x >> 10); }

/* k * 0x9e3779b1 mod 2^32, then >> (32 - HB): shift-and-add over the constant's set bits */
#define HB 25
#define HS (1u << HB)
static inline W hsh_c(W k) {
  const uint32_t C = 2654435761u; W acc = k;           /* bit 0 */
  for (int b = 1; b < 32; b++) if (C >> b & 1) acc = ADD(acc, SHL(k, b));
  return SHR(MSK(acc), 32 - HB);
}
typedef struct { uint32_t k; uint32_t c; } E;
/* table of 2^25 entries of two words at base address 0: entry i at 2i */
static inline W EADDR(W i) { return ADD(SHL(i, 1), 0); }
static void add_c(E *h, uint64_t *n, W k) {
  W i = hsh_c(k);
  for (;;) {
    W a = EADDR(i); (void)a; W c = LD(h[(uint32_t)i].c); W nz = CMPNZ(c); BR();
    if (!nz) break;
    W kk = LD(h[(uint32_t)i].k); W eq = CMPEQ(kk, k); BR();
    if (eq) break;
    i = AND(ADD(i, C1), LD(HS - 1));
  }
  W a = EADDR(i); (void)a; W c = LD(h[(uint32_t)i].c); W z = CMPNZ(c); BR();
  if (!z) { ST(h[(uint32_t)i].k, (uint32_t)k); if (n) { ST(*n, (uint64_t)ADD(LD(*n), C1)); } }
  ST(h[(uint32_t)i].c, (uint32_t)ADD(c, C1));
}
static W get_c(const E *h, W k) {
  W i = hsh_c(k);
  for (;;) {
    W a = EADDR(i); (void)a; W c = LD(h[(uint32_t)i].c); W nz = CMPNZ(c); BR();
    if (!nz) return 0;
    W kk = LD(h[(uint32_t)i].k); W eq = CMPEQ(kk, k); BR();
    if (eq) return c;
    i = AND(ADD(i, C1), LD(HS - 1));
  }
}
#define LOOPW(w) do { W nw_ = MSK(ADD((w), C1)); W more_ = CMPNZ(nw_); BR(); (void)more_; } while (0)

/* ---------------- sets ---------------- */
static uint64_t run_sets(void) {
  OPS = 0;
  struct { const char *name; int sig; uint32_t d, c; const char *row; } S[] = {
   {"W5",0,0xfffff006,0xd0018020,"================nuuu=======0=uu="},
   {"W6",0,0x002087f1,0x00000ffa,"==========u=====u===u======n===u"},
   {"W7",0,0x4fefb5fa,0xffdf780f,"=u=u=======n=====n=nu=n=====nun="},
   {"W8",0,0x28011100,0xb00fca02,"=u=nn==========u===u===u==1====="},
   {"W9",0,0x00008004,0xd7feef00,"================u==========1=u=="},
   {"W16",1,0x00008004,0xffff7ffc,"=============unnnunnnnnnnnnnnn=="},
   {"W18",1,0xffff7ffc,0x2ffe7fe0,"==============1=n=0==========n=="}};
  uint32_t cm[7], va[7], vb[7], xm[7]; uint64_t cnt[7] = {0}, both[7] = {0};
  for (int i = 0; i < 7; i++) {
    cm[i] = va[i] = vb[i] = xm[i] = 0;
    for (int k = 0; k < 32; k++) { uint32_t b = 1u << (31 - k); char c = S[i].row[k]; OPS += 6;  /* cell test, at most 5 primitives */
      if (c == '=') continue; cm[i] |= b; if (c == '1') { va[i] |= b; vb[i] |= b; } else if (c == 'u') { vb[i] |= b; xm[i] |= b; } else if (c == 'n') { va[i] |= b; xm[i] |= b; } }
  }
  W rd[7], rc[7]; for (int i = 0; i < 7; i++) { rd[i] = LD(S[i].d); rc[i] = LD(S[i].c); }
  uint32_t w32 = 0;
  do {
    W w = (W)w32, d = dup_c(w), s0w = s0d(d, w), s1w = s1d(d, w);
    for (int i = 0; i < 7; i++) {
      W wp = MSK(ADD(w, rd[i]));
      W diff = MSK(SUB(S[i].sig ? s1c(wp) : s0c(wp), S[i].sig ? s1w : s0w));
      W mod = CMPEQ(diff, rc[i]); BR();
      if (mod) {
        ST(cnt[i], (uint64_t)ADD(LD(cnt[i]), C1));
        W ok = CMPEQ(XOR(w, wp), LD(xm[i])); BR();
        if (ok) { ok = CMPEQ(AND(w, LD(cm[i])), LD(va[i])); BR(); }
        if (ok) { ok = CMPEQ(AND(wp, LD(cm[i])), LD(vb[i])); BR(); }
        if (ok) ST(both[i], (uint64_t)ADD(LD(both[i]), C1));
      }
    }
    LOOPW(w);
    w32++;
  } while (w32 != 0);
  for (int i = 0; i < 7; i++) printf("%s modular=%llu signed+modular=%llu\n", S[i].name, (unsigned long long)cnt[i], (unsigned long long)both[i]);
  return OPS;
}

/* ---------------- table (run twice) ---------------- */
static void masks_t(const char *row, uint32_t *cm, uint32_t *va) { *cm = *va = 0; for (int k = 0; k < 32; k++) { uint32_t b = 1u << (31 - k); char c = row[k]; OPS += 5; if (c == '=') continue; *cm |= b; if (c == '1' || c == 'n') *va |= b; } }
static uint64_t run_table(void) {
  OPS = 0;
  W A1 = LD(0xf36e6fcf), A2 = LD(0xb741c202), A3 = LD(0x90c67413), A4 = LD(0xfc7566c3);
  W E5 = LD(0x1d1fa7dd), E6 = LD(0xafe878e7), E7 = LD(0x4c97cbe5), E8 = LD(0x946f8048);
  W E5p = MSK(ADD(E5, LD(0xfffff006))), E6p = MSK(ADD(E6, LD(0xfff87fff))), E7p = MSK(ADD(E7, LD(0x4f880387)));
  W d6 = LD(0x002087f1), d7 = LD(0x4fefb5fa), d8 = LD(0x28011100), K7 = LD(0xab1c5ed5), K8 = LD(0xd807aa98);
  W C8 = LD(0xb00fca02u), C7 = LD(0xffdf780fu);
  uint32_t cm4, va4, cm3, va3; masks_t("============0===0=========01===0", &cm4, &va4); masks_t("==========================10====", &cm3, &va3);
  static uint32_t V7[1024], V8[65536]; int n7 = 0, n8 = 0;
  uint32_t w32 = 0;
  do {
    W w = (W)w32, d = dup_c(w), s0w = s0d(d, w);
    W h8 = CMPEQ(MSK(SUB(s0c(MSK(ADD(w, d8))), s0w)), C8); BR(); if (h8) { ST(V8[n8], w32); n8 = (int)ADD(n8, C1); }
    W h7 = CMPEQ(MSK(SUB(s0c(MSK(ADD(w, d7))), s0w)), C7); BR(); if (h7) { ST(V7[n7], w32); n7 = (int)ADD(n7, C1); }
    LOOPW(w); w32++;
  } while (w32 != 0);
  uint64_t nE4 = 0, nT = 0, nk = 0;
  W lhs = MSK(SUB(SUB(SUB(E7p, E7), SUB(S1c(E6p), S1c(E6))), d7));
  W lhs6 = MSK(SUB(SUB(SUB(E6p, E6), SUB(S1c(E5p), S1c(E5))), d6));
  W base4 = MSK(SUB(SUB(SUB(SUB(E8, A4), S1c(E7)), IFc(E7, E6, E5)), K8));
  W bs0a3 = S0c(A3), maja = MAJc(A3, A2, A1), bs0a2 = S0c(A2), bs1e6 = S1c(E6);
  W rcm4 = LD(cm4), rva4 = LD(va4), rcm3 = LD(cm3), rva3 = LD(va3), pw8 = LD(0x9f0484a6u), pw7 = LD(0xadf3737bu);
  for (int i = 0; i < n8; i++) {
    OPS += 3; W W8 = LD(V8[i]);
    W E4 = MSK(SUB(base4, W8));
    W ok = CMPEQ(AND(E4, rcm4), rva4); BR();
    if (ok) { ok = CMPEQ(MSK(SUB(IFc(E6p, E5p, E4), IFc(E6, E5, E4))), lhs); BR(); }
    if (!ok) continue;
    nE4 = (uint64_t)ADD(nE4, C1);
    W A0 = MSK(ADD(ADD(SUB(E4, A4), bs0a3), maja));
    W b3 = MSK(SUB(SUB(SUB(SUB(E7, A3), bs1e6), IFc(E6, E5, E4)), K7));
    W maj2 = MAJc(A2, A1, A0);
    for (int j = 0; j < n7; j++) {
      OPS += 3; W W7 = LD(V7[j]);
      W E3 = MSK(SUB(b3, W7));
      W ok3 = CMPEQ(AND(E3, rcm3), rva3); BR();
      if (ok3) { ok3 = CMPEQ(MSK(SUB(IFc(E5p, E4, E3), IFc(E5, E4, E3))), lhs6); BR(); }
      if (!ok3) continue;
      nT = (uint64_t)ADD(nT, C1);
      W Am1 = MSK(ADD(ADD(SUB(E3, A3), bs0a2), maj2));
      W room = CMPLT(nk, LD(1u << 24)); BR(); if (room) { nk = (uint64_t)ADD(nk, C1); OPS++; (void)Am1; }  /* keys[nk++] = Am1 */
      W p1 = CMPEQ(W8, pw8); BR(); if (p1) { W p2 = CMPEQ(W7, pw7); BR();
        if (p2) printf("published record present: A-1=%08x E3=%08x E4=%08x A0=%08x\n", (uint32_t)Am1, (uint32_t)E3, (uint32_t)E4, (uint32_t)A0); }
    }
    OPS += 1;
  }
  printf("V7 %d V8 %d\n", n7, n8);
  printf("V8 size %llu, (W8,E4) survivors %llu, tuples %llu\n", (unsigned long long)n8, (unsigned long long)nE4, (unsigned long long)nT);
  return OPS;
}

/* ---------------- joint ---------------- */
static uint64_t run_joint(void) {
  OPS = 0;
  E *h5 = calloc(HS, sizeof(E)), *h18 = calloc(HS, sizeof(E)); uint64_t n5 = 0, n18 = 0;
  OPS += 2ull * HS * 2;                                  /* zeroing both tables: one store per word */
  W d5 = LD(0xfffff006u), d18 = LD(0xffff7ffcu);
  uint32_t w32 = 0;
  do {
    W w = (W)w32, d = dup_c(w);
    add_c(h5, &n5, MSK(SUB(s0c(MSK(ADD(w, d5))), s0d(d, w))));
    add_c(h18, &n18, MSK(SUB(s1c(MSK(ADD(w, d18))), s1d(d, w))));
    LOOPW(w); w32++;
  } while (w32 != 0);
  printf("distinct sigma0-diff values for d5: %llu ; sigma1-diff values for d18: %llu\n", (unsigned long long)n5, (unsigned long long)n18);
  double single = 0, unionb = 0, strict = 0; W c5 = LD(0xd0018020u);
  const double sc = 1.0 / 4294967296.0;
  for (uint32_t i = 0; i < HS; i++) {
    OPS += 3; W a = EADDR(i); (void)a; W c = LD(h5[i].c); W nz = CMPNZ(c); BR();
    if (!nz) continue;
    W k = LD(h5[i].k);
    double p5 = FMUL(FCVT(c), sc);
    double p18 = FMUL(FCVT(get_c(h18, MSK(SUB(0, k)))), sc);
    single = FADD(single, FMUL(p5, p18));
    double u = FMUL(64, p18);
    double m = FCMPGT(u, 1) ? 1 : u; OPS += 1;
    unionb = FADD(unionb, FMUL(p5, m));
    W ec = CMPEQ(k, c5); BR(); if (ec) strict = p5;
  }
  printf("P(W5 in V5)=2^%.3f ; single-g joint=2^%.3f ; 64-g union bound joint=2^%.3f ; strict*0.136=2^%.3f\n", log2(strict), log2(single), log2(unionb), log2(strict * 0.1361322));
  printf("top sigma0-diff for d5 (count):\n");
  for (int t = 0; t < 5; t++) {
    uint32_t best = 0, bk = 0;
    for (uint32_t i = 0; i < HS; i++) { OPS += 3; W a = EADDR(i); (void)a; W c = LD(h5[i].c); W gt = CMPLT((W)best, c); BR(); if (gt) { best = (uint32_t)c; bk = i; OPS += 2; } }
    W g18 = get_c(h18, MSK(SUB(0, LD(h5[bk].k))));
    printf("  %08x %u p18(-c)=2^%.2f\n", h5[bk].k, best, log2(((double)(uint64_t)g18 + 1e-9) / 4294967296.0)); OPS += T_CVTF + T_FADD + T_FDIV;
    ST(h5[bk].c, 0u);
  }
  free(h5); free(h18);
  return OPS;
}

/* ---------------- pany ---------------- */
static uint64_t run_pany(void) {
  OPS = 0;
  E *h5 = calloc(HS, sizeof(E)); OPS += 2ull * HS;
  W d5 = LD(0xfffff006u), d16 = LD(0x00008004u), d18 = LD(0xffff7ffcu);
  uint32_t w32 = 0;
  do { W w = (W)w32; add_c(h5, NULL, MSK(SUB(s0c(MSK(ADD(w, d5))), s0c(w)))); LOOPW(w); w32++; } while (w32 != 0);
  uint32_t G[64]; int ng = 0; w32 = 0;
  do { W w = (W)w32; W hit = CMPEQ(MSK(SUB(s1c(MSK(ADD(w, d16))), s1c(w))), d18); BR();
       if (hit) { ST(G[ng], w32); ng = (int)ADD(ng, C1); } LOOPW(w); w32++; } while (w32 != 0);
  printf("|G16|=%d\n", ng);
  const int N = 1 << 24; double acc = 0; uint64_t accs = 0; W mc5 = LD((uint32_t)(0u - 0xd0018020u));
  const double sc = 1.0 / 4294967296.0;
  uint64_t st = 0x9e3779b97f4a7c15ull;
  for (int t = 0; t < N; t++) {
    OPS += 3;
    st = (uint64_t)XOR(st, AND(SHL(st, 13), M64)); st = (uint64_t)XOR(st, SHR(st, 7)); st = (uint64_t)XOR(st, AND(SHL(st, 17), M64));
    W c18 = MSK(SHR(st, 16));
    uint32_t v[64]; int nv = 0; W strictf = 0;
    for (int g = 0; g < 64; g++) {
      W W18 = MSK(ADD(s1c(LD(G[g])), c18));
      W x = MSK(SUB(s1c(MSK(ADD(W18, d18))), s1c(W18)));
      int dupf = 0;
      for (int j = 0; ; j++) { W more = CMPLT((W)j, (W)nv); BR(); if (!more) break; W eq = CMPEQ(LD(v[j]), x); BR(); if (eq) { dupf = 1; break; } OPS++; }
      BR(); if (!dupf) { ST(v[nv], (uint32_t)x); nv = (int)ADD(nv, C1); }
      W s = CMPEQ(x, mc5); BR(); if (s) strictf = OR(strictf, C1);
    }
    W psum = 0;
    for (int j = 0; ; j++) { W more = CMPLT((W)j, (W)nv); BR(); if (!more) break; psum = ADD(psum, get_c(h5, MSK(SUB(0, LD(v[j]))))); OPS++; }
    acc = FADD(acc, FMUL(FCVT(psum), sc));
    accs = (uint64_t)ADD(accs, strictf);
  }
  printf("P_any(joint, 64 g)=2^%.3f ; P(strict G18 exists g)=%.4f ; strict P=2^%.3f\n", log2(acc / N), (double)accs / N, log2((double)accs / N * pow(2, -18)));
  OPS += 2 * T_CVTF + 2 * T_FDIV + T_FMUL;           /* acc / N, accs / N, the 2^-18 product (log2 and pow are library calls) */
  free(h5);
  return OPS;
}

/* ---------------- pany2 ---------------- */
static E *P2h5; static uint32_t P2G[64]; static int P2NS, P2NT; static double P2sum[64], P2sum2[64]; static uint64_t P2ops[64];
static void *pany2_work(void *a) {
  int t = (int)(intptr_t)a; OPS = 0;
  uint64_t st = (uint64_t)XOR(LD(0x243f6a8885a308d3ull), AND(ADD(0, (W)((uint64_t)(t + 1) * 0x9e3779b97f4a7c15ull)), M64));
  OPS += 385;                                           /* (t+1) * 0x9e3779b97f4a7c15: one emulated 64-bit product */
  double S = 0, S2 = 0; const double sc = 1.0 / 4294967296.0;
  W d18 = LD(0xffff7ffcu);
  for (long n = 0; n < P2NS / P2NT; n++) {
    OPS += 3;
    st = (uint64_t)XOR(st, AND(SHL(st, 13), M64)); st = (uint64_t)XOR(st, SHR(st, 7)); st = (uint64_t)XOR(st, AND(SHL(st, 17), M64));
    W c18 = MSK(SHR(st, 20));
    uint32_t v[64]; int nv = 0;
    for (int g = 0; g < 64; g++) {
      W W18 = MSK(ADD(s1c(LD(P2G[g])), c18));
      W x = MSK(SUB(s1c(MSK(ADD(W18, d18))), s1c(W18)));
      int dupf = 0;
      for (int j = 0; ; j++) { W more = CMPLT((W)j, (W)nv); BR(); if (!more) break; W eq = CMPEQ(LD(v[j]), x); BR(); if (eq) { dupf = 1; break; } OPS++; }
      BR(); if (!dupf) { ST(v[nv], (uint32_t)x); nv = (int)ADD(nv, C1); }
    }
    W psum = 0;
    for (int j = 0; ; j++) { W more = CMPLT((W)j, (W)nv); BR(); if (!more) break; psum = ADD(psum, get_c(P2h5, MSK(SUB(0, LD(v[j]))))); OPS++; }
    double p = FMUL(FCVT(psum), sc);
    S = FADD(S, p); S2 = FADD(S2, FMUL(p, p));
  }
  P2sum[t] = S; P2sum2[t] = S2; P2ops[t] = OPS; return NULL;
}
static uint64_t run_pany2(int NT, int lg) {
  OPS = 0; P2NT = NT; P2NS = 1 << lg;
  P2h5 = calloc(HS, sizeof(E)); OPS += 2ull * HS;
  W d5 = LD(0xfffff006u), d9 = LD(0x00008004u), d18 = LD(0xffff7ffcu); int ng = 0;
  uint32_t w32 = 0;
  do { W w = (W)w32, d = dup_c(w);
       add_c(P2h5, NULL, MSK(SUB(s0c(MSK(ADD(w, d5))), s0d(d, w))));
       W hit = CMPEQ(MSK(SUB(s1c(MSK(ADD(w, d9))), s1d(d, w))), d18); BR();
       if (hit) { ST(P2G[ng], w32); ng = (int)ADD(ng, C1); }
       LOOPW(w); w32++; } while (w32 != 0);
  uint32_t mxc = 0;
  for (uint32_t i = 0; i < HS; i++) { OPS += 3; W a = EADDR(i); (void)a; W c = LD(P2h5[i].c); W gt = CMPLT((W)mxc, c); BR(); if (gt) { mxc = (uint32_t)c; OPS++; } }
  uint64_t main_ops = OPS;
  pthread_t th[64]; for (int i = 0; i < NT; i++) pthread_create(&th[i], 0, pany2_work, (void *)(intptr_t)i);
  for (int i = 0; i < NT; i++) pthread_join(th[i], 0);
  OPS = main_ops; for (int i = 0; i < NT; i++) OPS += P2ops[i] + 3;
  double S = 0, S2 = 0; for (int i = 0; i < NT; i++) { S = FADD(S, P2sum[i]); S2 = FADD(S2, P2sum2[i]); }
  double n = (double)(P2NS / P2NT) * P2NT, m = S / n, var = S2 / n - m * m, se = sqrt(var / n);
  OPS += T_CVTF + T_FMUL + 3 * T_FDIV + 2 * T_FMUL + T_FADD + T_FSQRT + 4 * T_FADD;  /* n, m, var, se, the bounds */
  printf("|G16|=%d samples=2^%d mean=%.6e (2^%.4f) se=%.3e 99%%LCB=%.6e (2^%.4f) 99%%UCB=2^%.4f max_term_bound=%.3e\n", ng, (int)log2(n), m, log2(m), se, m - 2.576 * se, log2(m - 2.576 * se), log2(m + 2.576 * se), 64.0 * mxc / 4294967296.0);
  free(P2h5);
  return OPS;
}

int main(int argc, char **argv) {
  if (argc < 2) return 64;
  const char *p = argv[1]; uint64_t ops;
  if (!strcmp(p, "sets")) ops = run_sets();
  else if (!strcmp(p, "table")) ops = run_table();
  else if (!strcmp(p, "joint")) ops = run_joint();
  else if (!strcmp(p, "pany")) ops = run_pany();
  else if (!strcmp(p, "pany2-1-20")) ops = run_pany2(1, 20);
  else if (!strcmp(p, "pany2-12-28")) ops = run_pany2(12, 28);
  else return 64;
  fprintf(stderr, "OPS %s %llu\n", p, (unsigned long long)ops);
  return 0;
}
```

C.10 Source of the pre-construction analysis programs as they ran (Section 15.1)

    999b9ced77d5c434a8d11e8d947229953f227046ee58beb72a675e001d3f0232  sets.c
    28d358b8076ae9f8521e3a546108c18f6745fe516d8c146f074b41cf7722c20e  table.c
    072bb3f309c0a5d85b1f58f53ee8768ecdf1a344280a6323ce8b4429866f020b  joint.c
    23142bfdadf3f75b378205b58c9d0a756a8eb0fb92d008b326ebfe1a07d25ae1  pany.c
    c3af3e22af5b9a8069b2e5e1a1653354d93eb8b06813e8dd3ab732405b9ebeca  pany2.c

Each was compiled with `cc -O2` (`pany2` with `cc -O3 -mcpu=apple-m4 ... -lpthread -lm`). `table` ran twice; its
first run preceded the one-line diagnostic `printf` of the inner loop. Since this filing `table` is an excluded run
(it embeds the published starting point, Section 15.4); its source and its counted version in `pcount.c` are
listed for completeness and are not charged.

`sets.c`:

```c
#include <stdio.h>
#include <stdint.h>
#include <string.h>
static inline uint32_t R(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
static inline uint32_t s0(uint32_t x){return R(x,7)^R(x,18)^(x>>3);}
static inline uint32_t s1(uint32_t x){return R(x,17)^R(x,19)^(x>>10);}
typedef struct {const char*name; int sig; uint32_t d,c; const char*row;} Spec;
static void masks(const char*row,uint32_t*cm,uint32_t*va,uint32_t*vb,uint32_t*xm){
  *cm=*va=*vb=*xm=0;
  for(int k=0;k<32;k++){uint32_t b=1u<<(31-k);char c=row[k];
    if(c=='=')continue; *cm|=b;
    if(c=='1'){*va|=b;*vb|=b;} else if(c=='u'){*vb|=b;*xm|=b;} else if(c=='n'){*va|=b;*xm|=b;}}
}
int main(void){
  Spec S[]={
   {"W5",0,0xfffff006,0xd0018020,"================nuuu=======0=uu="},
   {"W6",0,0x002087f1,0x00000ffa,"==========u=====u===u======n===u"},
   {"W7",0,0x4fefb5fa,0xffdf780f,"=u=u=======n=====n=nu=n=====nun="},
   {"W8",0,0x28011100,0xb00fca02,"=u=nn==========u===u===u==1====="},
   {"W9",0,0x00008004,0xd7feef00,"================u==========1=u=="},
   {"W16",1,0x00008004,0xffff7ffc,"=============unnnunnnnnnnnnnnn=="},
   {"W18",1,0xffff7ffc,0x2ffe7fe0,"==============1=n=0==========n=="},
  };
  int n=7; uint64_t cm_cnt[7]={0}, both[7]={0};
  uint32_t cm[7],va[7],vb[7],xm[7];
  for(int i=0;i<n;i++) masks(S[i].row,&cm[i],&va[i],&vb[i],&xm[i]);
  uint32_t w=0;
  do{
    for(int i=0;i<n;i++){
      uint32_t wp=w+S[i].d;
      uint32_t diff = S[i].sig? (s1(wp)-s1(w)) : (s0(wp)-s0(w));
      int mod = diff==S[i].c;
      if(mod){cm_cnt[i]++;
        if(((w^wp)==xm[i]) && ((w&cm[i])==va[i]) && ((wp&cm[i])==vb[i])) both[i]++;}
    }
    w++;
  }while(w!=0);
  for(int i=0;i<n;i++) printf("%s modular=%llu signed+modular=%llu\n",S[i].name,(unsigned long long)cm_cnt[i],(unsigned long long)both[i]);
  return 0;
}
```

`table.c`:

```c
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
static inline uint32_t R(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
static inline uint32_t s0(uint32_t x){return R(x,7)^R(x,18)^(x>>3);}
static inline uint32_t S0(uint32_t x){return R(x,2)^R(x,13)^R(x,22);}
static inline uint32_t S1(uint32_t x){return R(x,6)^R(x,11)^R(x,25);}
static inline uint32_t IF(uint32_t x,uint32_t y,uint32_t z){return (x&y)^(~x&z);}
static inline uint32_t MAJ(uint32_t x,uint32_t y,uint32_t z){return (x&y)^(x&z)^(y&z);}
static void masks(const char*row,uint32_t*cm,uint32_t*va){*cm=*va=0;for(int k=0;k<32;k++){uint32_t b=1u<<(31-k);char c=row[k];if(c=='=')continue;*cm|=b;if(c=='1'||c=='n')*va|=b;}}
int main(void){
  /* starting point of the published pair (copy A values; primes = copy B) */
  uint32_t A1=0xf36e6fcf,A2=0xb741c202,A3=0x90c67413,A4=0xfc7566c3;
  uint32_t E5=0x1d1fa7dd,E6=0xafe878e7,E7=0x4c97cbe5,E8=0x946f8048;
  uint32_t dE5=0xfffff006,dE6=0xfff87fff,dE7=0x4f880387; /* modular, B-A */
  uint32_t E5p=E5+dE5,E6p=E6+dE6,E7p=E7+dE7;
  uint32_t d6=0x002087f1,d7=0x4fefb5fa,d8=0x28011100;
  uint32_t K7=0xab1c5ed5,K8=0xd807aa98;
  uint32_t cm4,va4,cm3,va3; masks("============0===0=========01===0",&cm4,&va4); masks("==========================10====",&cm3,&va3);
  uint64_t nW8=0,nE4=0,nT=0;
  static uint32_t V7[1024],V8[65536]; int n7=0,n8=0;
  uint32_t w=0;
  do{ if((uint32_t)(s0(w+d8)-s0(w))==0xb00fca02u) V8[n8++]=w;
      if((uint32_t)(s0(w+d7)-s0(w))==0xffdf780fu) V7[n7++]=w;
      w++; }while(w!=0);
  nW8=n8;
  uint32_t lhs=(E7p-E7)-(S1(E6p)-S1(E6))-d7;
  uint32_t lhs6=(E6p-E6)-(S1(E5p)-S1(E5))-d6;
  static uint32_t keys[1<<24]; uint64_t nk=0;
  for(int i=0;i<n8;i++){ uint32_t W8=V8[i];
    uint32_t E4=E8-A4-S1(E7)-IF(E7,E6,E5)-K8-W8;
    if(((E4&cm4)==va4) && ((uint32_t)(IF(E6p,E5p,E4)-IF(E6,E5,E4))==lhs)){ nE4++;
      uint32_t A0=E4-A4+S0(A3)+MAJ(A3,A2,A1);
      for(int j=0;j<n7;j++){ uint32_t W7=V7[j];
        uint32_t E3=E7-A3-S1(E6)-IF(E6,E5,E4)-K7-W7;
        if(((E3&cm3)==va3) && ((uint32_t)(IF(E5p,E4,E3)-IF(E5,E4,E3))==lhs6)){ nT++;
          uint32_t Am1=E3-A3+S0(A2)+MAJ(A2,A1,A0); if(nk<(1u<<24)) keys[nk++]=Am1; if(W8==0x9f0484a6u && W7==0xadf3737bu) printf("published record present: A-1=%08x E3=%08x E4=%08x A0=%08x\n",Am1,E3,E4,A0); }
      }
    }
  }
  printf("V7 %d V8 %d\n",n7,n8);
  printf("V8 size %llu, (W8,E4) survivors %llu, tuples %llu\n",(unsigned long long)nW8,(unsigned long long)nE4,(unsigned long long)nT);
  return 0;
}
```

`joint.c`:

```c
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <math.h>
static inline uint32_t R(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
static inline uint32_t s0(uint32_t x){return R(x,7)^R(x,18)^(x>>3);}
static inline uint32_t s1(uint32_t x){return R(x,17)^R(x,19)^(x>>10);}
#define HB 25
#define HS (1u<<HB)
typedef struct {uint32_t k; uint32_t c;} E;
static E *h5,*h18; static uint64_t n5=0,n18=0;
static inline uint32_t hsh(uint32_t k){return (k*2654435761u)>>(32-HB);}
static void add(E*h,uint64_t*n,uint32_t k){uint32_t i=hsh(k);while(h[i].c && h[i].k!=k) i=(i+1)&(HS-1); if(!h[i].c){h[i].k=k;(*n)++;} h[i].c++;}
static uint32_t get(E*h,uint32_t k){uint32_t i=hsh(k);while(h[i].c){if(h[i].k==k)return h[i].c;i=(i+1)&(HS-1);}return 0;}
int main(void){
  h5=calloc(HS,sizeof(E)); h18=calloc(HS,sizeof(E));
  uint32_t d5=0xfffff006u,d18=0xffff7ffcu; uint32_t w=0;
  do{ add(h5,&n5,(uint32_t)(s0(w+d5)-s0(w))); add(h18,&n18,(uint32_t)(s1(w+d18)-s1(w))); w++; }while(w!=0);
  printf("distinct sigma0-diff values for d5: %llu ; sigma1-diff values for d18: %llu\n",(unsigned long long)n5,(unsigned long long)n18);
  double single=0, unionb=0, strict=0; uint32_t c5=0xd0018020u;
  for(uint32_t i=0;i<HS;i++) if(h5[i].c){ uint32_t c=h5[i].k; double p5=h5[i].c/4294967296.0; double p18=get(h18,(uint32_t)(0u-c))/4294967296.0;
     single+=p5*p18; double u=64*p18; unionb+=p5*(u>1?1:u); if(c==c5) strict=p5; }
  printf("P(W5 in V5)=2^%.3f ; single-g joint=2^%.3f ; 64-g union bound joint=2^%.3f ; strict*0.136=2^%.3f\n",log2(strict),log2(single),log2(unionb),log2(strict*0.1361322));
  printf("top sigma0-diff for d5 (count):\n"); 
  for(int t=0;t<5;t++){uint32_t best=0,bk=0;for(uint32_t i=0;i<HS;i++) if(h5[i].c>best){best=h5[i].c;bk=i;} printf("  %08x %u p18(-c)=2^%.2f\n",h5[bk].k,best,log2((get(h18,0u-h5[bk].k)+1e-9)/4294967296.0)); h5[bk].c=0;}
  return 0;
}
```

`pany.c`:

```c
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <math.h>
static inline uint32_t R(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
static inline uint32_t s0(uint32_t x){return R(x,7)^R(x,18)^(x>>3);}
static inline uint32_t s1(uint32_t x){return R(x,17)^R(x,19)^(x>>10);}
#define HB 25
#define HS (1u<<HB)
typedef struct {uint32_t k; uint32_t c;} E;
static E *h5; 
static inline uint32_t hsh(uint32_t k){return (k*2654435761u)>>(32-HB);}
static void add(E*h,uint32_t k){uint32_t i=hsh(k);while(h[i].c && h[i].k!=k) i=(i+1)&(HS-1); if(!h[i].c){h[i].k=k;} h[i].c++;}
static uint32_t get(E*h,uint32_t k){uint32_t i=hsh(k);while(h[i].c){if(h[i].k==k)return h[i].c;i=(i+1)&(HS-1);}return 0;}
static uint64_t st=0x9e3779b97f4a7c15ull; static inline uint32_t rnd(void){st^=st<<13;st^=st>>7;st^=st<<17;return (uint32_t)(st>>16);}
int main(void){
  h5=calloc(HS,sizeof(E)); uint32_t d5=0xfffff006u,d16=0x00008004u,d18=0xffff7ffcu; uint32_t w=0;
  do{ add(h5,(uint32_t)(s0(w+d5)-s0(w))); w++; }while(w!=0);
  uint32_t G[64]; int ng=0; w=0;
  do{ if((uint32_t)(s1(w+d16)-s1(w))==d18) G[ng++]=w; w++; }while(w!=0);
  printf("|G16|=%d\n",ng);
  const int N=1<<24; double acc=0, accs=0; uint32_t c5=0xd0018020u;
  for(int t=0;t<N;t++){ uint32_t c18=rnd(); uint32_t v[64]; int nv=0; int strict=0;
    for(int g=0;g<64;g++){ uint32_t W18=s1(G[g])+c18; uint32_t x=(uint32_t)(s1(W18+d18)-s1(W18)); int dup=0; for(int j=0;j<nv;j++) if(v[j]==x){dup=1;break;} if(!dup) v[nv++]=x; if(x==(uint32_t)(0u-c5)) strict=1; }
    double p=0; for(int j=0;j<nv;j++) p+=get(h5,(uint32_t)(0u-v[j]))/4294967296.0;
    acc+=p; accs+=strict; }
  printf("P_any(joint, 64 g)=2^%.3f ; P(strict G18 exists g)=%.4f ; strict P=2^%.3f\n",log2(acc/N),accs/N,log2(accs/N*pow(2,-18)));
  return 0;
}
```

`pany2.c`:

```c
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <math.h>
#include <pthread.h>
static inline uint32_t R(uint32_t x,int n){return (x>>n)|(x<<(32-n));}
static inline uint32_t s0(uint32_t x){return R(x,7)^R(x,18)^(x>>3);}
static inline uint32_t s1(uint32_t x){return R(x,17)^R(x,19)^(x>>10);}
#define HB 25
#define HS (1u<<HB)
typedef struct {uint32_t k; uint32_t c;} E;
static E *h5; static uint32_t G[64]; static int NS; static int NT;
static inline uint32_t hsh(uint32_t k){return (k*2654435761u)>>(32-HB);}
static void add(uint32_t k){uint32_t i=hsh(k);while(h5[i].c && h5[i].k!=k) i=(i+1)&(HS-1); if(!h5[i].c){h5[i].k=k;} h5[i].c++;}
static uint32_t get(uint32_t k){uint32_t i=hsh(k);while(h5[i].c){if(h5[i].k==k)return h5[i].c;i=(i+1)&(HS-1);}return 0;}
static double sum[64],sum2[64]; static double mx=0;
static void *work(void*a){ int t=(int)(intptr_t)a; uint64_t st=0x243f6a8885a308d3ull^(uint64_t)(t+1)*0x9e3779b97f4a7c15ull; double S=0,S2=0;
  for(long n=0;n<NS/NT;n++){ st^=st<<13;st^=st>>7;st^=st<<17; uint32_t c18=(uint32_t)(st>>20); uint32_t v[64]; int nv=0;
    for(int g=0;g<64;g++){ uint32_t W18=s1(G[g])+c18; uint32_t x=s1(W18+0xffff7ffcu)-s1(W18); int dup=0; for(int j=0;j<nv;j++) if(v[j]==x){dup=1;break;} if(!dup) v[nv++]=x; }
    double p=0; for(int j=0;j<nv;j++) p+=get(0u-v[j]); p/=4294967296.0; S+=p; S2+=p*p; }
  sum[t]=S; sum2[t]=S2; return NULL; }
int main(int argc,char**argv){ NT=atoi(argv[1]); NS=1<<atoi(argv[2]);
  h5=calloc(HS,sizeof(E)); uint32_t w=0; int ng=0;
  do{ add(s0(w+0xfffff006u)-s0(w)); if(s1(w+0x00008004u)-s1(w)==0xffff7ffcu) G[ng++]=w; w++; }while(w!=0);
  uint32_t mxc=0; for(uint32_t i=0;i<HS;i++) if(h5[i].c>mxc) mxc=h5[i].c;
  pthread_t th[64]; for(int i=0;i<NT;i++) pthread_create(&th[i],0,work,(void*)(intptr_t)i); for(int i=0;i<NT;i++) pthread_join(th[i],0);
  double S=0,S2=0; for(int i=0;i<NT;i++){S+=sum[i];S2+=sum2[i];} double n=(double)(NS/NT)*NT; double m=S/n, var=S2/n-m*m, se=sqrt(var/n);
  printf("|G16|=%d samples=2^%d mean=%.6e (2^%.4f) se=%.3e 99%%LCB=%.6e (2^%.4f) 99%%UCB=2^%.4f max_term_bound=%.3e\n",ng,(int)log2(n),m,log2(m),se,m-2.576*se,log2(m-2.576*se),log2(m+2.576*se),64.0*mxc/4294967296.0);
  return 0; }
```

C.11 `mul32.py` and `heavy.py` (explicit emulations of the heavy forms, the tariffs of Section 14.2, H3)

    fd968fc4700bf0c60f42702ff324c3be07a496db9f8dafbb91b28cb919434abd  mul32.py
    6fdfd03de6e6bea80da921e2b3e08a0dabfa1589ef9716911c87e1b5965a2554  heavy.py

`mul32.py` emulates the multiplies with 32-bit source operands; `heavy.py` emulates the 64-bit multiplies, the
divides and the binary64 forms, and gives the per-form price used by `cgfull.py` and `bbvmix.py` (`cost`).
Run directly, each checks its emulations against the instruction's definition and prints the largest count.

```python
"""Price of AArch64 multiplies whose multiplier is a 32-bit register, by exact emulation.

A 64 x 64 product needs 64 shift-and-add steps (the v5 table's 400).  When both source operands are
32-bit registers (umull, smull, umaddl, smaddl, umsubl, smsubl, umnegl, smnegl, and mul, madd,
msub, mneg on w registers), the multiplier has 32 bits, so 32 steps suffice.  Each emulation below
uses v5 primitives only (one count each) and is branch-free:

    step i: bit = (b >> i) & 1; sel = 0 - bit; acc = acc + ((a << i) & sel)      6 primitives

The signed forms use sext(a) * sext(b) = ua*ub - 2^32 (a31*ub + b31*ua) mod 2^64.
`cost(mn, ops)` returns PRICE32 for these forms and defers to a64ops.cost otherwise.
Run directly, it checks every emulation against the instruction's definition on random and edge
inputs and prints the largest primitive count of each.
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a64ops  # noqa: E402

PRICE32 = 210
M32, M64 = (1 << 32) - 1, (1 << 64) - 1
ALWAYS32 = {'umull', 'smull', 'umaddl', 'smaddl', 'umsubl', 'smsubl', 'umnegl', 'smnegl'}
BYDEST = {'mul', 'madd', 'msub', 'mneg'}


def is_mul32(mn, ops):
    base = mn.split('.')[0]
    if base in ALWAYS32:
        return True
    return base in BYDEST and bool(ops) and (ops[0].startswith('w') or ops[0] == 'wzr')


def cost(mn, ops):
    if is_mul32(mn, ops):
        return PRICE32, 'heavy'
    return a64ops.cost(mn, ops)


class Ctr:
    def __init__(self):
        self.n = 0

    def op(self, v):
        self.n += 1
        return v % (1 << 256)


def umul32(c, a, b):
    """zext(a) * zext(b), 64-bit result."""
    a = c.op(a & M32)
    b = c.op(b & M32)
    acc = 0
    for i in range(32):
        bit = c.op(c.op(b >> i) & 1)
        sel = c.op(0 - bit)
        acc = c.op(acc + c.op(c.op(a << i) & sel))
    return acc                                      # < 2^64 already


def smul32(c, a, b):
    ua, ub = a & M32, b & M32
    p = umul32(c, a, b)
    a31 = c.op(c.op(ua >> 31) & 1)
    b31 = c.op(c.op(ub >> 31) & 1)
    t1 = c.op(c.op(ub << 32) & c.op(0 - a31))
    t2 = c.op(c.op(ua << 32) & c.op(0 - b31))
    return c.op(c.op(c.op(p - t1) - t2) & M64)


EMUL = {
    'umull':  lambda c, a, b, x: umul32(c, a, b),
    'umaddl': lambda c, a, b, x: c.op(c.op(x + umul32(c, a, b)) & M64),
    'umsubl': lambda c, a, b, x: c.op(c.op(x - umul32(c, a, b)) & M64),
    'umnegl': lambda c, a, b, x: c.op(c.op(0 - umul32(c, a, b)) & M64),
    'smull':  lambda c, a, b, x: smul32(c, a, b),
    'smaddl': lambda c, a, b, x: c.op(c.op(x + smul32(c, a, b)) & M64),
    'smsubl': lambda c, a, b, x: c.op(c.op(x - smul32(c, a, b)) & M64),
    'smnegl': lambda c, a, b, x: c.op(c.op(0 - smul32(c, a, b)) & M64),
    'mul.w':  lambda c, a, b, x: c.op(umul32(c, a, b) & M32),
    'madd.w': lambda c, a, b, x: c.op(c.op(x + umul32(c, a, b)) & M32),
    'msub.w': lambda c, a, b, x: c.op(c.op(x - umul32(c, a, b)) & M32),
    'mneg.w': lambda c, a, b, x: c.op(c.op(0 - umul32(c, a, b)) & M32),
}


def sx(v):
    v &= M32
    return v - (1 << 32) if v >> 31 else v


DEF = {
    'umull':  lambda a, b, x: ((a & M32) * (b & M32)) & M64,
    'umaddl': lambda a, b, x: (x + (a & M32) * (b & M32)) & M64,
    'umsubl': lambda a, b, x: (x - (a & M32) * (b & M32)) & M64,
    'umnegl': lambda a, b, x: (-(a & M32) * (b & M32)) & M64,
    'smull':  lambda a, b, x: (sx(a) * sx(b)) & M64,
    'smaddl': lambda a, b, x: (x + sx(a) * sx(b)) & M64,
    'smsubl': lambda a, b, x: (x - sx(a) * sx(b)) & M64,
    'smnegl': lambda a, b, x: (-sx(a) * sx(b)) & M64,
    'mul.w':  lambda a, b, x: (a * b) & M32,
    'madd.w': lambda a, b, x: (x + a * b) & M32,
    'msub.w': lambda a, b, x: (x - a * b) & M32,
    'mneg.w': lambda a, b, x: (-a * b) & M32,
}


def main():
    rng = random.Random(20261008)
    edge = [0, 1, 2, M32, M32 - 1, 1 << 31, (1 << 31) - 1, 0x9e3779b1]
    worst = 0
    for name, f in EMUL.items():
        mx = 0
        cases = [(a, b) for a in edge for b in edge] + [(rng.getrandbits(32), rng.getrandbits(32)) for _ in range(3000)]
        for a, b in cases:
            x = rng.getrandbits(64) if not name.endswith('.w') else rng.getrandbits(32)
            c = Ctr()
            got = f(c, a, b, x)
            assert got == DEF[name](a, b, x), (name, a, b, x)
            mx = max(mx, c.n)
        worst = max(worst, mx)
        print(f"{name:7s} emulation ops {mx:3d}  priced {PRICE32}  ok ({len(cases)} inputs)")
    assert worst <= PRICE32
    print(f"all forms match their definition; largest emulation {worst} <= {PRICE32}")


if __name__ == '__main__':
    main()
```

Output of `python3 mul32.py`:

```
umull   emulation ops 194  priced 210  ok (3064 inputs)
umaddl  emulation ops 196  priced 210  ok (3064 inputs)
umsubl  emulation ops 196  priced 210  ok (3064 inputs)
umnegl  emulation ops 196  priced 210  ok (3064 inputs)
smull   emulation ops 207  priced 210  ok (3064 inputs)
smaddl  emulation ops 209  priced 210  ok (3064 inputs)
smsubl  emulation ops 209  priced 210  ok (3064 inputs)
smnegl  emulation ops 209  priced 210  ok (3064 inputs)
mul.w   emulation ops 195  priced 210  ok (3064 inputs)
madd.w  emulation ops 196  priced 210  ok (3064 inputs)
msub.w  emulation ops 196  priced 210  ok (3064 inputs)
mneg.w  emulation ops 196  priced 210  ok (3064 inputs)
all forms match their definition; largest emulation 209 <= 210
```

```python
"""Heavy AArch64 instructions reduced to collision-frontier-v5 primitives: explicit counted emulations.

Each emulation computes the instruction's result from its operand registers using only v5 primitives
on 256-bit words (addition/subtraction mod 2^256, AND/OR/XOR, shifts, comparison, conditional branch),
counting every primitive.  A data-dependent branch costs 1; fixed-count loops are unrolled and cost
nothing for control; select(c, a, b) is (a & -c) | (b & ~-c), four primitives.  Floating point is
IEEE 754 binary64 with round-to-nearest-even, as AArch64 executes it with the default FPCR: NaN
operands propagate quieted, invalid operations give the default NaN.

Run directly, it checks every emulation against the host (AArch64 hardware through Python integers
and floats; exact fractions for the fused multiply-add) on random and edge inputs and prints the
largest primitive count of each form.  TARIFF is that maximum rounded up to a multiple of 8; `cost`
prices a form by TARIFF (32-bit-operand multiplies by mul32.py) and defers to a64ops otherwise.
"""
import math
import os
import random
import struct
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a64ops  # noqa: E402
import mul32  # noqa: E402

MOD = 1 << 256
M32, M64 = (1 << 32) - 1, (1 << 64) - 1
FRAC, IMPL, EXPM = (1 << 52) - 1, 1 << 52, 0x7ff
DNAN, QBIT, SIGN = 0x7ff8000000000000, 1 << 51, 1 << 63
B = 4096                                        # exponent offset: every exponent below is kept non-negative


class C:
    def __init__(self):
        self.n = 0

    def _(self, v):
        self.n += 1
        return v % MOD

    def add(self, a, b): return self._(a + b)
    def sub(self, a, b): return self._(a - b)
    def and_(self, a, b): return self._(a & b)
    def or_(self, a, b): return self._(a | b)
    def xor(self, a, b): return self._(a ^ b)
    def shl(self, a, k): return self._(a << k)
    def shr(self, a, k): return self._(a >> k)

    def lt(self, a, b):
        self.n += 1
        return int(a < b)

    def eq(self, a, b):
        self.n += 1
        return int(a == b)

    def br(self, cond):
        self.n += 1
        return bool(cond)

    def sel(self, c01, a, b):
        m = self.sub(0, c01)
        return self.or_(self.and_(a, m), self.and_(b, self.xor(m, MOD - 1)))


# ---------------- integer multiply and divide ----------------
def umul(c, a, b, steps):
    acc = 0
    for i in range(steps):
        bit = c.and_(c.shr(b, i), 1)
        acc = c.add(acc, c.and_(c.shl(a, i), c.sub(0, bit)))
    return acc


def e_mul64(c, a, b, x, kind):
    p = umul(c, c.and_(a, M64), c.and_(b, M64), 64)
    if kind == 'mul':
        return c.and_(p, M64)
    if kind == 'madd':
        return c.and_(c.add(x, p), M64)
    if kind == 'msub':
        return c.and_(c.sub(x, p), M64)
    return c.and_(c.sub(0, p), M64)              # mneg


def e_umulh(c, a, b):
    return c.shr(umul(c, c.and_(a, M64), c.and_(b, M64), 64), 64)


def e_smulh(c, a, b):
    ua, ub = c.and_(a, M64), c.and_(b, M64)
    p = umul(c, ua, ub, 64)
    a63, b63 = c.and_(c.shr(ua, 63), 1), c.and_(c.shr(ub, 63), 1)
    p = c.sub(p, c.shl(c.and_(ub, c.sub(0, a63)), 64))
    p = c.sub(p, c.shl(c.and_(ua, c.sub(0, b63)), 64))
    return c.and_(c.shr(c.and_(p, (1 << 128) - 1), 64), M64)


def udivq(c, a, n, bits):
    rem = q = 0
    for i in range(bits - 1, -1, -1):
        rem = c.or_(c.shl(rem, 1), c.and_(c.shr(a, i), 1))
        ge = c.xor(c.lt(rem, n), 1)
        rem = c.sub(rem, c.and_(n, c.sub(0, ge)))
        q = c.or_(c.shl(q, 1), ge)
    return q, rem


def e_div(c, a, b, bits, signed):
    m = M64 if bits == 64 else M32
    a, b = c.and_(a, m), c.and_(b, m)
    if c.br(c.eq(b, 0)):
        return 0
    if not signed:
        return udivq(c, a, b, bits)[0]
    sa, sb = c.and_(c.shr(a, bits - 1), 1), c.and_(c.shr(b, bits - 1), 1)
    ua = c.sel(sa, c.and_(c.sub(0, a), m), a)
    ub = c.sel(sb, c.and_(c.sub(0, b), m), b)
    q = udivq(c, ua, ub, bits)[0]
    return c.and_(c.sel(c.xor(sa, sb), c.sub(0, q), q), m)


# ---------------- binary64 core ----------------
def unpack(c, x):
    return c.and_(c.shr(x, 63), 1), c.and_(c.shr(x, 52), EXPM), c.and_(x, FRAC)


def finite_parts(c, e, f):
    """(m, E): value = m * 2^(E - B - 1075); subnormals use exponent field 1"""
    z = c.eq(e, 0)
    return c.sel(z, f, c.or_(f, IMPL)), c.add(c.sel(z, 1, e), B)


def top_bit(c, m, steps):
    """index of the highest set bit of m (m > 0), binary search over the given step sizes"""
    t, top = m, 0
    for k in steps:
        hi = c.lt(0, c.shr(t, k))
        t = c.sel(hi, c.shr(t, k), t)
        top = c.sel(hi, c.add(top, k), top)
    return top


def round_pack(c, s, m, E, steps):
    """correctly rounded binary64 of (-1)^s * m * 2^(E - B - 1075), m > 0 (m may carry a sticky bit in
    its lowest position, at least two bits below the rounding position)"""
    t = top_bit(c, m, steps)
    lsb = c.sub(c.add(t, E), 52)                     # exponent (offset) of the result's unit in the last place
    lsb = c.sel(c.lt(lsb, B + 1 - 0), B + 1, lsb)    # subnormal floor: unit 2^-1074 is offset exponent B + 1
    if c.br(c.lt(lsb, c.add(E, 1))):                 # lsb <= E: exact (left shift by E - lsb >= 0)
        q = c.shl(m, c.sub(E, lsb))
    else:
        sh = c.sub(lsb, E)                           # >= 1
        if c.br(c.lt(250, sh)):
            q, r, st = 0, 0, c.lt(0, m)
        else:
            q = c.shr(m, sh)
            r = c.and_(c.shr(m, c.sub(sh, 1)), 1)
            st = c.lt(0, c.and_(m, c.sub(c.shl(1, c.sub(sh, 1)), 1)))
        q = c.add(q, c.and_(r, c.or_(st, c.and_(q, 1))))
    if c.br(c.eq(c.shr(q, 53), 1)):
        q, lsb = c.shr(q, 1), c.add(lsb, 1)
    if c.br(c.lt(q, IMPL)):                          # subnormal (or zero)
        return c.or_(c.shl(s, 63), q)
    be = c.sub(lsb, B)                               # biased exponent of the result
    if c.br(c.lt(2046, be)):
        return c.or_(c.shl(s, 63), 0x7ff0000000000000)
    return c.or_(c.or_(c.shl(s, 63), c.shl(be, 52)), c.and_(q, FRAC))


def nan_of(c, a, ea, fa, b=None, eb=None, fb=None, x=None, ex=None, fx=None):
    """AArch64 NaN propagation (default FPCR): the first signalling NaN operand, else the first quiet NaN
    operand, quieted; None if no operand is a NaN"""
    ops = [(v, e, f) for v, e, f in ((a, ea, fa), (b, eb, fb), (x, ex, fx)) if v is not None]
    isnan = [c.and_(c.eq(e, EXPM), c.lt(0, f)) for v, e, f in ops]
    anynan = 0
    for k in isnan:
        anynan = c.or_(anynan, k)
    if not c.br(anynan):
        return None
    for (v, e, f), k in zip(ops, isnan):          # signalling NaNs first
        if c.br(c.and_(k, c.eq(c.and_(f, QBIT), 0))):
            return c.or_(v, QBIT)
    for (v, e, f), k in zip(ops, isnan):
        if c.br(k):
            return c.or_(v, QBIT)
    return None


S56 = (32, 16, 8, 4, 2, 1)
S112 = (64, 32, 16, 8, 4, 2, 1)
S256 = (128, 64, 32, 16, 8, 4, 2, 1)


def e_fadd(c, a, b, negb=False):
    sa, ea, fa = unpack(c, a)
    sb, eb, fb = unpack(c, b)
    n = nan_of(c, a, ea, fa, b, eb, fb)
    if n is not None:
        return n
    if negb:
        sb = c.xor(sb, 1)
    ia, ib = c.eq(ea, EXPM), c.eq(eb, EXPM)
    if c.br(c.or_(ia, ib)):
        if c.br(c.and_(c.and_(ia, ib), c.xor(sa, sb))):
            return DNAN
        return c.or_(c.shl(c.sel(ia, sa, sb), 63), 0x7ff0000000000000)
    ma, xa = finite_parts(c, ea, fa)
    mb, xb = finite_parts(c, eb, fb)
    big = c.lt(c.or_(c.shl(xa, 60), ma), c.or_(c.shl(xb, 60), mb))
    s1, x1, m1 = c.sel(big, sb, sa), c.sel(big, xb, xa), c.sel(big, mb, ma)
    s2, x2, m2 = c.sel(big, sa, sb), c.sel(big, xa, xb), c.sel(big, ma, mb)
    m1, m2 = c.shl(m1, 3), c.shl(m2, 3)
    d = c.sub(x1, x2)
    if c.br(c.lt(60, d)):
        m2 = c.lt(0, m2)
    else:
        st = c.lt(0, c.and_(m2, c.sub(c.shl(1, d), 1)))
        m2 = c.or_(c.shr(m2, d), st)
    m = c.sel(c.xor(s1, s2), c.sub(m1, m2), c.add(m1, m2))
    if c.br(c.eq(m, 0)):
        return c.shl(c.and_(s1, s2), 63)
    return round_pack(c, s1, m, c.sub(x1, 3), S56)


def e_fmul(c, a, b, neg=False):
    sa, ea, fa = unpack(c, a)
    sb, eb, fb = unpack(c, b)
    n = nan_of(c, a, ea, fa, b, eb, fb)
    if n is not None:
        return n
    s = c.xor(sa, sb)
    if neg:
        s = c.xor(s, 1)
    ia, ib = c.eq(ea, EXPM), c.eq(eb, EXPM)
    za, zb = c.eq(c.and_(a, SIGN - 1), 0), c.eq(c.and_(b, SIGN - 1), 0)
    if c.br(c.or_(ia, ib)):
        if c.br(c.or_(za, zb)):
            return DNAN
        return c.or_(c.shl(s, 63), 0x7ff0000000000000)
    if c.br(c.or_(za, zb)):
        return c.shl(s, 63)
    ma, xa = finite_parts(c, ea, fa)
    mb, xb = finite_parts(c, eb, fb)
    p = umul(c, ma, mb, 53)
    return round_pack(c, s, p, c.sub(c.add(xa, xb), B + 1075), S112)


def e_fma(c, a, b, x, nega=False, negx=False):
    """x + a*b, one rounding (fmadd); fmsub x - a*b; fnmadd -x - a*b; fnmsub -x + a*b"""
    sa, ea, fa = unpack(c, a)
    sb, eb, fb = unpack(c, b)
    sx, ex, fx = unpack(c, x)
    ia, ib, ix = c.eq(ea, EXPM), c.eq(eb, EXPM), c.eq(ex, EXPM)
    za, zb = c.eq(c.and_(a, SIGN - 1), 0), c.eq(c.and_(b, SIGN - 1), 0)
    # AArch64: (inf * 0) + qNaN is the default NaN; otherwise NaN operands propagate (a, b, then x in Arm order
    # for FMADD Rd = Ra + Rn*Rm: the addend is checked first)
    if c.br(c.and_(c.or_(c.and_(ia, zb), c.and_(ib, za)), c.and_(ix, c.lt(0, fx)))):
        return DNAN
    n = nan_of(c, x, ex, fx, a, ea, fa, b, eb, fb)
    if n is not None:
        return n
    if nega:
        sa = c.xor(sa, 1)
    if negx:
        sx = c.xor(sx, 1)
    sp = c.xor(sa, sb)
    if c.br(c.or_(ia, ib)):
        if c.br(c.or_(za, zb)):
            return DNAN
        if c.br(c.and_(ix, c.xor(sx, sp))):
            return DNAN
        return c.or_(c.shl(sp, 63), 0x7ff0000000000000)
    if c.br(ix):
        return c.or_(c.shl(sx, 63), 0x7ff0000000000000)
    zx = c.eq(c.and_(x, SIGN - 1), 0)
    if c.br(c.or_(za, zb)):
        if c.br(zx):
            return c.shl(c.and_(sp, sx), 63)
        return c.or_(c.shl(sx, 63), c.and_(x, SIGN - 1))
    ma, xa = finite_parts(c, ea, fa)
    mb, xb = finite_parts(c, eb, fb)
    P = umul(c, ma, mb, 53)
    EP = c.sub(c.add(xa, xb), B + 1075)              # P * 2^(EP - B - 1075)
    if c.br(zx):
        return round_pack(c, sp, P, EP, S112)
    mx, EX = finite_parts(c, ex, fx)
    D = 140
    if c.br(c.lt(c.add(EP, D), EX)):                 # x far above the product: the product is only a sticky bit
        tx, tp, E = c.shl(mx, D), c.lt(0, P), c.sub(EX, D)
    elif c.br(c.lt(c.add(EX, D), EP)):               # product far above x: x is only a sticky bit
        tp, tx, E = c.shl(P, 3), c.lt(0, mx), c.sub(EP, 3)
    elif c.br(c.lt(EX, EP)):
        tp, tx, E = c.shl(P, c.sub(EP, EX)), mx, EX
    else:
        tp, tx, E = P, c.shl(mx, c.sub(EX, EP)), EP
    big = c.lt(tp, tx)
    s = c.sel(big, sx, sp)
    m = c.sel(c.xor(sp, sx), c.sel(big, c.sub(tx, tp), c.sub(tp, tx)), c.add(tp, tx))
    if c.br(c.eq(m, 0)):
        return c.shl(c.and_(sp, sx), 63)
    return round_pack(c, s, m, E, S256)


def e_fdiv(c, a, b):
    sa, ea, fa = unpack(c, a)
    sb, eb, fb = unpack(c, b)
    n = nan_of(c, a, ea, fa, b, eb, fb)
    if n is not None:
        return n
    s = c.xor(sa, sb)
    ia, ib = c.eq(ea, EXPM), c.eq(eb, EXPM)
    za, zb = c.eq(c.and_(a, SIGN - 1), 0), c.eq(c.and_(b, SIGN - 1), 0)
    if c.br(c.or_(c.and_(ia, ib), c.and_(za, zb))):
        return DNAN
    if c.br(c.or_(ia, zb)):
        return c.or_(c.shl(s, 63), 0x7ff0000000000000)
    if c.br(c.or_(ib, za)):
        return c.shl(s, 63)
    ma, xa = finite_parts(c, ea, fa)
    mb, xb = finite_parts(c, eb, fb)
    ta, tb = top_bit(c, ma, S56), top_bit(c, mb, S56)
    ma, mb = c.shl(ma, c.sub(52, ta)), c.shl(mb, c.sub(52, tb))   # both in [2^52, 2^53)
    q, rem = 0, ma
    for _ in range(57):                              # 57 quotient bits of ma/mb
        ge = c.xor(c.lt(rem, mb), 1)
        rem = c.sub(rem, c.and_(mb, c.sub(0, ge)))
        q = c.or_(c.shl(q, 1), ge)
        rem = c.shl(rem, 1)
    q = c.or_(c.shl(q, 1), c.lt(0, rem))             # sticky
    E = c.sub(c.add(c.add(c.sub(xa, xb), ta), B + 1075), c.add(tb, 57))
    return round_pack(c, s, q, E, S56)


def e_fsqrt(c, a):
    s, e, f = unpack(c, a)
    n = nan_of(c, a, e, f)
    if n is not None:
        return n
    if c.br(c.eq(c.and_(a, SIGN - 1), 0)):
        return a
    if c.br(s):
        return DNAN
    if c.br(c.eq(e, EXPM)):
        return a
    m, X = finite_parts(c, e, f)
    t = top_bit(c, m, S56)
    m = c.shl(m, c.sub(52, t))                       # [2^52, 2^53), value m * 2^(X - t + 52 - B - 1075 - 52)
    X = c.sub(c.add(X, t), 52)
    odd = c.and_(c.add(X, 1), 1)                     # make (X - B - 1075) even; B and 1075 parity: B even, 1075 odd
    m = c.sel(odd, c.shl(m, 1), m)
    X = c.sel(odd, c.sub(X, 1), X)
    R = c.shl(m, 60)                                 # root of R has 57 bits
    root = rem = 0
    for i in range(56, -1, -1):
        rem = c.or_(c.shl(rem, 2), c.and_(c.shr(R, 2 * i), 3))
        trial = c.or_(c.shl(root, 2), 1)
        ge = c.xor(c.lt(rem, trial), 1)
        rem = c.sub(rem, c.and_(trial, c.sub(0, ge)))
        root = c.or_(c.shl(root, 1), ge)
    root = c.or_(c.shl(root, 1), c.lt(0, rem))
    # sqrt(m * 2^(X-B-1075)) = sqrt(m * 2^60) * 2^((X-B-1075-60)/2) = root/2 * 2^(...); root has one sticky bit appended
    # value = root * 2^((X - B - 1075 - 60)/2 - 1); the exponent is halved with an even offset 2^20
    E = c.add(c.shr(c.sub(c.add(X, 1 << 20), B + 1075 + 60), 1), B + 1075 - 1 - (1 << 19))
    return round_pack(c, 0, root, E, S56)


def e_fcmp(c, a, b):
    sa, ea, fa = unpack(c, a)
    sb, eb, fb = unpack(c, b)
    if c.br(c.or_(c.and_(c.eq(ea, EXPM), c.lt(0, fa)), c.and_(c.eq(eb, EXPM), c.lt(0, fb)))):
        return 0b0011
    if c.br(c.and_(c.eq(c.and_(a, SIGN - 1), 0), c.eq(c.and_(b, SIGN - 1), 0))):
        return 0b0110
    ka = c.sel(sa, c.and_(c.xor(a, M64), M64), c.or_(a, SIGN))
    kb = c.sel(sb, c.and_(c.xor(b, M64), M64), c.or_(b, SIGN))
    if c.br(c.eq(ka, kb)):
        return 0b0110
    return c.sel(c.lt(ka, kb), 0b1000, 0b0010)


def e_cvtf(c, v, signed, bits, fbits=0):
    m = M64 if bits == 64 else M32
    v = c.and_(v, m)
    s = 0
    if signed:
        s = c.and_(c.shr(v, bits - 1), 1)
        v = c.sel(s, c.and_(c.sub(0, v), m), v)
    if c.br(c.eq(v, 0)):
        return 0
    return round_pack(c, s, v, B + 1075 - fbits, S112)


def e_fcvtz(c, a, signed, bits):
    s, e, f = unpack(c, a)
    if c.br(c.and_(c.eq(e, EXPM), c.lt(0, f))):
        return 0
    hi = (1 << (bits - 1)) - 1 if signed else (1 << bits) - 1
    if c.br(c.lt(e, 1023)):                           # |a| < 1 (and zeros, subnormals)
        return 0
    m = c.or_(f, IMPL)
    if c.br(c.lt(1022 + bits, e)):                    # |a| >= 2^bits (or inf): saturate
        if c.br(s):
            return ((1 << (bits - 1)) if signed else 0)
        return hi
    k = c.sub(e, 1075)                                # value = m * 2^(e - 1075)
    if c.br(c.lt(e, 1075)):
        mag = c.shr(m, c.sub(1075, e))
    else:
        mag = c.shl(m, k)
    if c.br(s):
        if not signed:
            return 0
        if c.br(c.lt(1 << (bits - 1), mag)):
            return 1 << (bits - 1)
        return c.and_(c.sub(0, mag), (1 << bits) - 1)
    if c.br(c.lt(hi, mag)):
        return hi
    return mag


# ---------------- reference and checks ----------------
def bits(x): return struct.unpack('<Q', struct.pack('<d', x))[0]
def flt(b): return struct.unpack('<d', struct.pack('<Q', b))[0]


def rnd_double(rng):
    r = rng.random()
    if r < 0.05:
        return rng.choice([0, SIGN, 0x7ff0000000000000, 0xfff0000000000000, DNAN, 0x7ff0000000000001 | QBIT,
                           1, SIGN | 1, FRAC, IMPL, 0x7fefffffffffffff, 0x3ff0000000000000, 0xbff0000000000000])
    if r < 0.15:
        return (rng.getrandbits(1) << 63) | rng.getrandbits(52)            # subnormal
    if r < 0.25:
        return (rng.getrandbits(1) << 63) | (rng.choice([1, 2, 2045, 2046, 1023, 1022]) << 52) | rng.getrandbits(52)
    if r < 0.45:
        return (rng.getrandbits(1) << 63) | (rng.randint(1000, 1050) << 52) | rng.getrandbits(52)
    return rng.getrandbits(64) & ~(0 if rng.random() < 0.5 else 0)


def ref_fma(a, b, x):
    A, Bv, X = flt(a), flt(b), flt(x)
    if any(math.isnan(v) or math.isinf(v) for v in (A, Bv, X)):
        return None
    exact = Fraction(A) * Fraction(Bv) + Fraction(X)
    if exact == 0:
        # sign of an exact zero: (+0) unless both product and addend are negative-signed zeros/round to -0
        sp = (a >> 63) ^ (b >> 63)
        if A * Bv == 0 and X == 0:
            return ((sp & (x >> 63)) << 63)
        return 0
    try:
        return bits(float(exact))
    except OverflowError:
        return 0x7ff0000000000000 | ((1 << 63) if exact < 0 else 0)


def check():
    rng = random.Random(20261008)
    worst = {}

    def run(name, f, args, want):
        c = C()
        got = f(c, *args)
        if want is not None:
            assert got == want, (name, [hex(a) for a in args], hex(got), hex(want))
        worst[name] = max(worst.get(name, 0), c.n)

    N = 20000
    for _ in range(N):
        a, b, x = rng.getrandbits(64), rng.getrandbits(64), rng.getrandbits(64)
        if rng.random() < 0.2:
            a, b = rng.choice([0, 1, M64, 1 << 63, M64 - 1]), rng.choice([0, 1, M64, 1 << 63, 2])
        run('mul64', lambda c, a, b, x: e_mul64(c, a, b, x, 'madd'), (a, b, x), (x + a * b) & M64)
        run('mul64', lambda c, a, b, x: e_mul64(c, a, b, x, 'msub'), (a, b, x), (x - a * b) & M64)
        run('umulh', e_umulh, (a, b), (a * b) >> 64)
        sa = a - (1 << 64) if a >> 63 else a
        sb = b - (1 << 64) if b >> 63 else b
        run('smulh', e_smulh, (a, b), ((sa * sb) >> 64) & M64)
        for nb in (32, 64):
            m = (1 << nb) - 1
            ua, ub = a & m, (b & m) >> rng.randint(0, nb - 1)
            run(f'udiv{nb}', lambda c, a, b: e_div(c, a, b, nb, False), (ua, ub), (ua // ub) if ub else 0)
            ia = ua - (1 << nb) if ua >> (nb - 1) else ua
            ib = ub - (1 << nb) if ub >> (nb - 1) else ub
            q = 0 if ib == 0 else (abs(ia) // abs(ib)) * (1 if (ia < 0) == (ib < 0) else -1)
            run(f'sdiv{nb}', lambda c, a, b: e_div(c, a, b, nb, True), (ua, ub), q & m)
    for _ in range(N * 5):
        a, b, x = rnd_double(rng), rnd_double(rng), rnd_double(rng)
        A, Bv = flt(a), flt(b)
        run('fadd', lambda c, a, b: e_fadd(c, a, b), (a, b), bits(A + Bv))
        run('fadd', lambda c, a, b: e_fadd(c, a, b, negb=True), (a, b), bits(A - Bv))
        run('fmul', lambda c, a, b: e_fmul(c, a, b), (a, b), bits(A * Bv))
        if Bv != 0 or math.isnan(A) or math.isnan(Bv):
            want = bits(A / Bv) if Bv != 0 else None
        else:
            want = None
        run('fdiv', e_fdiv, (a, b), want)
        run('fsqrt', e_fsqrt, (a,), (bits(math.sqrt(A)) if A >= 0 or A == 0 else None) if not math.isnan(A) else None)
        run('fma', e_fma, (a, b, x), ref_fma(a, b, x))
        cmpw = 0b0011 if (math.isnan(A) or math.isnan(Bv)) else (0b0110 if A == Bv else (0b1000 if A < Bv else 0b0010))
        run('fcmp', e_fcmp, (a, b), cmpw)
        for nb in (32, 64):
            v = rng.getrandbits(nb)
            run('cvtf', lambda c, v: e_cvtf(c, v, False, nb), (v,), bits(float(v)))
            sv = v - (1 << nb) if v >> (nb - 1) else v
            run('cvtf', lambda c, v: e_cvtf(c, v, True, nb), (v,), bits(float(sv)))
            fb = rng.randint(1, nb)
            run('cvtf', lambda c, v: e_cvtf(c, v, False, nb, fb), (v,), bits(float(Fraction(v, 1 << fb))))
            if not math.isnan(A):
                t = math.trunc(A) if not math.isinf(A) else (1 << 70 if A > 0 else -(1 << 70))
                hi_s, lo_s = (1 << (nb - 1)) - 1, -(1 << (nb - 1))
                run('fcvtz', lambda c, a: e_fcvtz(c, a, True, nb), (a,), max(lo_s, min(hi_s, t)) & ((1 << nb) - 1))
                run('fcvtz', lambda c, a: e_fcvtz(c, a, False, nb), (a,), max(0, min((1 << nb) - 1, t)))
    return worst


TARIFF = {'mul64': 392, 'umulh': 392, 'smulh': 408, 'udiv32': 360, 'sdiv32': 384, 'udiv64': 712, 'sdiv64': 736,
          'fadd': 240, 'fmul': 520, 'fma': 600, 'fdiv': 824, 'fsqrt': 1008, 'fcmp': 48, 'cvtf': 152, 'fcvtz': 24}


def cost(mn, ops):
    base = mn.split('.')[0]
    if mul32.is_mul32(mn, ops):
        return mul32.PRICE32, 'heavy'
    w = 'x' if ops and ops[0].startswith('x') else 'w'
    if base in ('mul', 'madd', 'msub', 'mneg'):
        return TARIFF['mul64'], 'heavy'
    if base in ('umulh', 'smulh'):
        return TARIFF[base], 'heavy'
    if base in ('udiv', 'sdiv'):
        return TARIFF[f"{base}{'64' if w == 'x' else '32'}"], 'div'
    fp = {'fadd': 'fadd', 'fsub': 'fadd', 'fmul': 'fmul', 'fnmul': 'fmul', 'fmadd': 'fma', 'fmsub': 'fma',
          'fnmadd': 'fma', 'fnmsub': 'fma', 'fdiv': 'fdiv', 'fsqrt': 'fsqrt', 'fcmp': 'fcmp', 'fcmpe': 'fcmp',
          'ucvtf': 'cvtf', 'scvtf': 'cvtf', 'fcvtzs': 'fcvtz', 'fcvtzu': 'fcvtz'}
    if base in fp and ops and ops[0][0] in 'dxw':
        return TARIFF[fp[base]], ('div' if base in ('fdiv', 'fsqrt') else 'heavy')
    return a64ops.cost(mn, ops)


if __name__ == '__main__':
    w = check()
    for k in sorted(w):
        print(f"{k:7s} largest emulation {w[k]:5d}  tariff {TARIFF[k]:5d}  {'ok' if w[k] <= TARIFF[k] else 'EXCEEDED'}")
        assert w[k] <= TARIFF[k]
    print("every emulation matches its reference on all checked inputs and stays within its tariff")
```

Output of `python3 heavy.py`:

```
cvtf    largest emulation   150  tariff   152  ok
fadd    largest emulation   233  tariff   240  ok
fcmp    largest emulation    48  tariff    48  ok
fcvtz   largest emulation    24  tariff    24  ok
fdiv    largest emulation   820  tariff   824  ok
fma     largest emulation   596  tariff   600  ok
fmul    largest emulation   514  tariff   520  ok
fsqrt   largest emulation  1004  tariff  1008  ok
mul64   largest emulation   388  tariff   392  ok
sdiv32  largest emulation   382  tariff   384  ok
sdiv64  largest emulation   734  tariff   736  ok
smulh   largest emulation   401  tariff   408  ok
udiv32  largest emulation   356  tariff   360  ok
udiv64  largest emulation   708  tariff   712  ok
umulh   largest emulation   387  tariff   392  ok
every emulation matches its reference on all checked inputs and stays within its tariff
```

C.12 `cgfull.py` and `bbvmix.py` (pricing of complete profiles) and the profiles of Section 14.4

    4446cbd4ace6eb2f59e4cfe2fe3c6585465d1d823418ca5d40090dd449005d4b  cgfull.py
    8635f28f7d879a62ef4c957f9eebec5439e2b7d8457ad14f4f20daaffed8570a  bbvmix.py
    3b77db5f1a1284da476a7db857e443500b7afd19ce0df2fe4e3d235c070fff3c  run3.sh (attempt 1, callgrind)
    7d303d10558a31cbe4f42e957265887e07c4aa089590580f781ccd1478a9c999  runbbv.sh (attempts 1-3, exp-bbv)

Both use `read_dump`, `disasm` and `objkey` of `cgmix.py` (C.2) and `cost` of `a64ops.py` (C.1) and `heavy.py`
(C.11). The profiles ran in `debian:bookworm-slim` with valgrind 3.19.0 and PyPI z3-solver 4.15.4.0 (z3 SHA-256
bbea82f99718e57d...), one container per run. Attempt 1's callgrind profile is the complete profile of our v4
measurements (run with `-T:1200`, which it did not reach); attempts 2 and 3 are exp-bbv profiles, and attempt 1
was also profiled with exp-bbv as the check of Section 14.4:

```sh
#!/bin/sh
# runs inside the container; /w is the scratch dir
cd /w/out
for i in 1 2 3; do
  m=/w/s-model.smt2; [ $i -gt 1 ] && m=/w/s-model$i.smt2
  valgrind --tool=callgrind --dump-instr=yes --dump-line=no --compress-strings=no --compress-pos=no \
    --dump-every-bb=8000000000 --callgrind-out-file=m$i.out z3 -T:1200 -st $m > m$i.z3 2> m$i.vg &
done
wait
```

```sh
#!/bin/sh
# inside the container: basic-block vectors of z3 attempt $1 over the whole run (committed model and seed)
i=$1
cd /w/bbv
date -u +%FT%TZ > b$i.start
nice -n 10 valgrind --tool=exp-bbv --vex-guest-chase=no --vex-guest-max-insns=100 --interval-size=2000000000 \
  --bb-out-file=b$i.bb --pc-out-file=b$i.pc z3 -st /w/s-model$i.smt2 > b$i.z3 2> b$i.vg
echo "exit $?" > b$i.done; date -u +%FT%TZ >> b$i.done
```

```python
"""Complete-run per-form cost from callgrind interval dumps (--dump-instr=yes, uncompressed).

usage: cgfull.py BINDIR OUT.json DUMP [DUMP ...]
For each dump (one interval) and for the whole run: executed instructions, mapped instructions,
primitive operations under a64ops.cost (unmapped instructions priced at 1024), the heavy and
divide instructions by mnemonic and register width.  Writes one JSON object.
"""
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a64ops import cost  # noqa: E402
import heavy  # noqa: E402
from cgmix import read_dump, disasm, objkey  # noqa: E402


def width(ops):
    return 'w' if ops and re.match(r'^w\d+$|^wzr$', ops[0]) else 'x' if ops and re.match(r'^x\d+$|^xzr$', ops[0]) else 'v'


def main():
    bindir, outp, dumps = sys.argv[1], sys.argv[2], sys.argv[3:]
    per = [(d, read_dump(d)) for d in dumps]
    wanted = collections.defaultdict(set)
    for _, cnt in per:
        for ob, c in cnt.items():
            k = objkey(ob or '')
            if k:
                wanted[k].update(c)
            wanted['z3.elf'].update(a for a in c if a >= 0x400000)
    dis = {k: disasm(os.path.join(bindir, k), w) for k, w in wanted.items() if os.path.exists(os.path.join(bindir, k))}
    rows = []
    tot = collections.Counter()
    heavy_all = collections.Counter()
    for name, cnt in per:
        r = collections.Counter()
        hv = collections.Counter()
        for ob, c in cnt.items():
            k = objkey(ob or '')
            for a, n in c.items():
                ins = dis.get(k, {}).get(a) if k else None
                if ins is None and a >= 0x400000 and 'z3.elf' in dis:
                    ins = dis['z3.elf'].get(a)
                r['instr'] += n
                if ins is None:
                    r['unmapped'] += n
                    r['ops'] += 1024 * n
                    r['ops8'] += 1024 * n
                    continue
                o, cl = cost(ins[0], ins[1])
                r['ops'] += o * n
                h8 = heavy.cost(ins[0], ins[1])
                r['ops8'] += h8[0] * n
                if h8[1] in ('heavy', 'div'):
                    r['opsH'] += h8[0] * n
                r[cl] += n
                if cl in ('heavy', 'div'):
                    hv[f"{ins[0]}.{width(ins[1])}"] += n
        r['mean'] = r['ops'] / r['instr']
        r['mean8'] = r['ops8'] / r['instr']
        rows.append(dict(dump=os.path.basename(name), **{k: v for k, v in r.items()},
                         heavy_forms=dict(hv.most_common(12))))
        for k in ('instr', 'unmapped', 'ops', 'ops8', 'opsH', 'heavy', 'div', 'ordinary', 'unknown'):
            tot[k] += r[k]
        heavy_all.update(hv)
    whole = dict(tot)
    whole['mean'] = tot['ops'] / tot['instr']
    whole['max_interval_mean'] = max(r['mean'] for r in rows)
    whole['mean8'] = tot['ops8'] / tot['instr']
    whole['max_interval_mean8'] = max(r['mean8'] for r in rows)
    whole['heavy_forms'] = dict(heavy_all.most_common(30))
    json.dump(dict(intervals=rows, whole=whole), open(outp, 'w'), indent=1)
    print(json.dumps({k: whole[k] for k in ('instr', 'unmapped', 'heavy', 'div', 'mean', 'max_interval_mean', 'mean8', 'max_interval_mean8')}))


if __name__ == '__main__':
    main()
```

```python
"""Per-form cost of a complete run from exp-bbv basic-block vectors.

usage: bbvmix.py BINDIR PREFIX OUT.json [GROUP]
PREFIX.pc lists every superblock (id, start address, function); PREFIX.bb has one line per interval of
2e9 executed instructions with the instructions executed in each superblock.  With
--vex-guest-chase=no and --vex-guest-max-insns=100, a superblock is the straight run of instructions
from its start up to and including the first control transfer, or 100 instructions.  This script
disassembles each superblock from the executable that ran, checks that every count is a multiple of
its length (entries x length), and prices every executed instruction with heavy.cost (32-bit-operand
multiplies by mul32.py, the other heavy forms by their checked emulations, the rest by a64ops).
Intervals are reported in groups of GROUP (default 20, i.e. 4e10 instructions).
"""
import bisect
import collections
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a64ops  # noqa: E402
import heavy  # noqa: E402
from cgmix import disasm  # noqa: E402

UNCOND = re.compile(r'^(b|bl|br|blr|ret|retaa|retab|braa|brab|blraa|blrab|svc|hvc|brk|udf|eret)$')
CF = re.compile(r'^(b|bl|br|blr|ret|retaa|retab|braa|brab|blraa|blrab|cbz|cbnz|tbz|tbnz|svc|hvc|brk|udf|eret)$|^b\.')
LIBS = ['ld-linux-aarch64.so.1', 'libstdc++.so.6', 'libm.so.6', 'libgcc_s.so.1', 'libc.so.6']


def symbols(path):
    out = {}
    for extra in (['-D'], []):
        p = subprocess.run(['xcrun', 'llvm-nm', '--defined-only'] + extra + [path], capture_output=True, text=True)
        for line in p.stdout.splitlines():
            f = line.split()
            if len(f) == 3 and f[1] in 'TtWwi':
                out.setdefault(f[2].split('@')[0], int(f[0], 16))
    return out


def main():
    bindir, prefix, outp = sys.argv[1], sys.argv[2], sys.argv[3]
    group = int(sys.argv[4]) if len(sys.argv) > 4 else 20
    pcs = {}
    for line in open(prefix + '.pc'):
        f = line.rstrip('\n').split(':')
        if f[0] == 'F':
            pcs[int(f[1])] = (int(f[2], 16), f[3] if len(f) > 3 else '')
    # library bases from blocks that start exactly at a known function entry
    bases = {}
    syms = {lib: symbols(os.path.join(bindir, lib)) for lib in LIBS}
    votes = collections.defaultdict(collections.Counter)
    for bid, (addr, fn) in pcs.items():
        if addr >= 0x4000000:
            for lib in LIBS:
                if fn in syms[lib]:
                    votes[lib][addr - syms[lib][fn]] += 1
    for lib in LIBS:
        if votes[lib]:
            bases[lib] = votes[lib].most_common(1)[0][0]

    def owner(addr):
        if addr < 0x4000000:
            return 'z3.elf', addr
        best = None
        for lib, b in bases.items():
            if addr >= b and (best is None or b > bases[best]):
                best = lib
        return (best, addr - bases[best]) if best else (None, addr)

    wanted = collections.defaultdict(set)
    loc = {}
    for bid, (addr, fn) in pcs.items():
        ob, off = owner(addr)
        loc[bid] = (ob, off)
        if ob:
            wanted[ob].update(off + 4 * i for i in range(100))
    dis = {ob: disasm(os.path.join(bindir, ob), w) for ob, w in wanted.items()}
    blocks = {}
    for bid, (ob, off) in loc.items():
        ins = []
        if ob:
            for i in range(100):
                d = dis[ob].get(off + 4 * i)
                if d is None:
                    break
                ins.append(d)
                if CF.match(d[0]):
                    break
        full = list(ins)                             # the run through conditional branches, for counts that are
        if ob and ins and not UNCOND.match(ins[-1][0]):  # not a multiple of the block length (bounded, see below)
            for i in range(len(ins), 100):
                d = dis[ob].get(off + 4 * i)
                if d is None:
                    break
                full.append(d)
                if UNCOND.match(d[0]):
                    break
        blocks[bid] = (ob, ins, full)
    rows, cur = [], collections.Counter()
    tot = collections.Counter()
    bad = collections.Counter()
    heavyforms = collections.Counter()
    nint = 0

    def flush():
        if cur['instr']:
            r = dict(cur)
            r['mean'] = r['ops5'] / r['instr']
            r['mean8'] = r['ops8'] / r['instr']
            rows.append(r)
            for k in ('instr', 'ops5', 'ops8', 'opsB', 'opsH', 'unmapped', 'nondiv', 'heavy'):
                tot[k] += cur[k]
            cur.clear()

    for line in open(prefix + '.bb'):
        if not line.startswith('T'):
            continue
        nint += 1
        for tok in line[1:].split():
            if not tok.startswith(':'):
                continue
            _, bid, cnt = tok.split(':')
            bid, cnt = int(bid), int(cnt)
            ob, ins, full = blocks.get(bid, (None, [], []))
            cur['instr'] += cnt
            if not ins:
                cur['unmapped'] += cnt
                cur['ops5'] += 1024 * cnt
                cur['ops8'] += 1024 * cnt
                bad['unmapped_blocks'] += 1
                continue
            L = len(ins)
            if cnt % L:
                # the superblock ran past a conditional branch: its count mixes partial and full runs, so every
                # counted instruction is charged at the largest price in the run through to the next unconditional
                # transfer (an upper bound)
                cur['nondiv'] += cnt
                bad[bid] += 1
                best5 = best8 = 0.0
                acc5 = acc8 = 0
                for k, (mn, ops) in enumerate(full, 1):      # any mix of runs that leave at a branch of the
                    acc5 += a64ops.cost(mn, ops)[0]           # superblock: bounded by the largest prefix mean
                    acc8 += heavy.cost(mn, ops)[0]
                    if k == len(full) or CF.match(mn):
                        best5, best8 = max(best5, acc5 / k), max(best8, acc8 / k)
                cur['ops5'] += best5 * cnt
                cur['ops8'] += best8 * cnt
                cur['opsB'] += best8 * cnt
                cur['opsH'] += sum(heavy.cost(mn, ops)[0] for mn, ops in full
                                   if heavy.cost(mn, ops)[1] in ('heavy', 'div')) / len(full) * cnt
                continue
            e = cnt / L
            for mn, ops in ins:
                c5, cl = a64ops.cost(mn, ops)
                c8, cl8 = heavy.cost(mn, ops)
                cur['ops5'] += c5 * e
                cur['ops8'] += c8 * e
                if cl8 in ('heavy', 'div'):
                    cur['opsH'] += c8 * e
                if cl in ('heavy', 'div'):
                    cur['heavy'] += e
                    heavyforms[mn + '.' + (ops[0][0] if ops else '')] += e
        if nint % group == 0:
            flush()
    flush()
    whole = dict(tot)
    whole['mean'] = tot['ops5'] / tot['instr']
    whole['mean8'] = tot['ops8'] / tot['instr']
    whole['max_interval_mean'] = max(r['mean'] for r in rows)
    whole['max_interval_mean8'] = max(r['mean8'] for r in rows)
    whole['bbv_intervals'] = nint
    m = re.search(r'Total instructions: (\d+)', open(prefix + '.vg').read())
    whole['total_instructions'] = int(m.group(1)) if m else None
    whole['tail'] = whole['total_instructions'] - tot['instr'] if m else None
    whole['blocks'] = len(pcs)
    whole['nondiv_blocks'] = sum(1 for k in bad if k != 'unmapped_blocks')
    whole['bases'] = {k: hex(v) for k, v in bases.items()}
    whole['heavy_forms'] = {k: round(v) for k, v in heavyforms.most_common(40)}
    json.dump(dict(intervals=rows, whole=whole), open(outp, 'w'), indent=1)
    print(json.dumps({k: whole[k] for k in ('instr', 'total_instructions', 'tail', 'unmapped', 'nondiv', 'mean', 'mean8',
                                            'max_interval_mean', 'max_interval_mean8', 'bbv_intervals', 'blocks',
                                            'nondiv_blocks', 'bases')}))


if __name__ == '__main__':
    main()
```

Per-interval results (instructions; per-form mean at this filing's prices; at the v5 table's prices). exp-bbv
intervals are groups of 20 reported intervals of 2e9 instructions; the final partial interval is not reported
by exp-bbv and is charged separately (Section 14.4):

| run | interval | instructions | per-form mean | at v5 prices |
|---|---|---|---|---|
| z3 attempt 1 (callgrind) | 1 | 40,087,099,456 | 4.6482 | 6.8188 |
| z3 attempt 1 (callgrind) | 2 | 41,189,100,762 | 5.3079 | 8.0692 |
| z3 attempt 1 (callgrind) | 3 | 41,095,860,245 | 4.8733 | 7.2452 |
| z3 attempt 1 (callgrind) | 4 | 41,026,080,417 | 5.1882 | 7.8455 |
| z3 attempt 1 (callgrind) | 5 | 41,602,060,040 | 5.3503 | 8.1576 |
| z3 attempt 1 (callgrind) | 6 | 40,527,755,090 | 4.8289 | 7.1670 |
| z3 attempt 1 (callgrind) | whole (reported) | 245,527,956,010 | 5.0356 | 7.5558 |
| z3 attempt 2 (exp-bbv) | 1 | 40,000,000,001 | 4.7780 | 7.0691 |
| z3 attempt 2 (exp-bbv) | 2 | 40,000,000,000 | 5.3008 | 8.0500 |
| z3 attempt 2 (exp-bbv) | 3 | 40,000,000,000 | 5.1344 | 7.7263 |
| z3 attempt 2 (exp-bbv) | 4 | 40,000,000,000 | 5.9655 | 9.3134 |
| z3 attempt 2 (exp-bbv) | 5 | 40,000,000,000 | 5.4644 | 8.3682 |
| z3 attempt 2 (exp-bbv) | 6 | 40,000,000,000 | 5.4418 | 8.3240 |
| z3 attempt 2 (exp-bbv) | 7 | 40,000,000,000 | 4.9266 | 7.3503 |
| z3 attempt 2 (exp-bbv) | 8 | 40,000,000,000 | 5.3962 | 8.2331 |
| z3 attempt 2 (exp-bbv) | 9 | 40,000,000,000 | 5.2972 | 8.0475 |
| z3 attempt 2 (exp-bbv) | 10 | 40,000,000,000 | 5.0592 | 7.5922 |
| z3 attempt 2 (exp-bbv) | 11 | 40,000,000,000 | 5.2870 | 8.0332 |
| z3 attempt 2 (exp-bbv) | 12 | 40,000,000,000 | 5.7628 | 8.9414 |
| z3 attempt 2 (exp-bbv) | 13 | 40,000,000,000 | 5.5809 | 8.5920 |
| z3 attempt 2 (exp-bbv) | 14 | 40,000,000,000 | 5.2601 | 7.9840 |
| z3 attempt 2 (exp-bbv) | 15 | 40,000,000,000 | 5.5605 | 8.5525 |
| z3 attempt 2 (exp-bbv) | 16 | 40,000,000,000 | 5.5914 | 8.6146 |
| z3 attempt 2 (exp-bbv) | 17 | 40,000,000,000 | 4.9348 | 7.3578 |
| z3 attempt 2 (exp-bbv) | 18 | 40,000,000,000 | 5.5484 | 8.5217 |
| z3 attempt 2 (exp-bbv) | 19 | 40,000,000,000 | 5.3130 | 8.0788 |
| z3 attempt 2 (exp-bbv) | 20 | 40,000,000,000 | 4.9997 | 7.4999 |
| z3 attempt 2 (exp-bbv) | 21 | 40,000,000,000 | 5.2239 | 7.9147 |
| z3 attempt 2 (exp-bbv) | 22 | 40,000,000,000 | 5.2799 | 8.0264 |
| z3 attempt 2 (exp-bbv) | 23 | 40,000,000,000 | 4.9143 | 7.3402 |
| z3 attempt 2 (exp-bbv) | 24 | 40,000,000,000 | 4.6353 | 6.8312 |
| z3 attempt 2 (exp-bbv) | 25 | 40,000,000,000 | 5.1514 | 7.7914 |
| z3 attempt 2 (exp-bbv) | 26 | 40,000,000,000 | 5.6506 | 8.7243 |
| z3 attempt 2 (exp-bbv) | 27 | 40,000,000,000 | 5.5787 | 8.5862 |
| z3 attempt 2 (exp-bbv) | 28 | 40,000,000,000 | 5.3848 | 8.2247 |
| z3 attempt 2 (exp-bbv) | 29 | 40,000,000,000 | 5.1583 | 7.8028 |
| z3 attempt 2 (exp-bbv) | 30 | 40,000,000,000 | 5.1456 | 7.7840 |
| z3 attempt 2 (exp-bbv) | 31 | 40,000,000,000 | 5.2138 | 7.8952 |
| z3 attempt 2 (exp-bbv) | 32 | 40,000,000,000 | 4.9993 | 7.4930 |
| z3 attempt 2 (exp-bbv) | 33 | 40,000,000,000 | 4.4958 | 6.5473 |
| z3 attempt 2 (exp-bbv) | 34 | 40,000,000,000 | 5.0463 | 7.5878 |
| z3 attempt 2 (exp-bbv) | 35 | 40,000,000,000 | 4.8708 | 7.2403 |
| z3 attempt 2 (exp-bbv) | 36 | 40,000,000,000 | 5.0106 | 7.5232 |
| z3 attempt 2 (exp-bbv) | 37 | 34,000,000,000 | 4.8302 | 7.1554 |
| z3 attempt 2 (exp-bbv) | whole (reported) | 1,474,000,000,001 | 5.2230 | 7.9144 |
| z3 attempt 3 (exp-bbv) | 1 | 40,000,000,001 | 4.6831 | 6.8935 |
| z3 attempt 3 (exp-bbv) | 2 | 40,000,000,000 | 5.2492 | 7.9556 |
| z3 attempt 3 (exp-bbv) | 3 | 40,000,000,000 | 5.2211 | 7.9049 |
| z3 attempt 3 (exp-bbv) | 4 | 40,000,000,000 | 5.3019 | 8.0643 |
| z3 attempt 3 (exp-bbv) | 5 | 40,000,000,000 | 5.4663 | 8.3745 |
| z3 attempt 3 (exp-bbv) | 6 | 40,000,000,000 | 5.5393 | 8.5136 |
| z3 attempt 3 (exp-bbv) | 7 | 40,000,000,000 | 4.9825 | 7.4571 |
| z3 attempt 3 (exp-bbv) | 8 | 40,000,000,000 | 5.3763 | 8.2091 |
| z3 attempt 3 (exp-bbv) | 9 | 40,000,000,000 | 5.4559 | 8.3536 |
| z3 attempt 3 (exp-bbv) | 10 | 40,000,000,000 | 5.2972 | 8.0591 |
| z3 attempt 3 (exp-bbv) | 11 | 40,000,000,000 | 5.1981 | 7.8519 |
| z3 attempt 3 (exp-bbv) | 12 | 40,000,000,000 | 5.4615 | 8.3647 |
| z3 attempt 3 (exp-bbv) | 13 | 40,000,000,000 | 5.2352 | 7.9392 |
| z3 attempt 3 (exp-bbv) | 14 | 40,000,000,000 | 5.7319 | 8.8894 |
| z3 attempt 3 (exp-bbv) | 15 | 40,000,000,000 | 5.2499 | 7.9688 |
| z3 attempt 3 (exp-bbv) | 16 | 40,000,000,000 | 5.2374 | 7.9360 |
| z3 attempt 3 (exp-bbv) | 17 | 40,000,000,000 | 4.9158 | 7.3135 |
| z3 attempt 3 (exp-bbv) | 18 | 40,000,000,000 | 5.2550 | 7.9741 |
| z3 attempt 3 (exp-bbv) | 19 | 40,000,000,000 | 5.1329 | 7.7452 |
| z3 attempt 3 (exp-bbv) | 20 | 40,000,000,000 | 5.3607 | 8.1904 |
| z3 attempt 3 (exp-bbv) | 21 | 34,000,000,000 | 5.4386 | 8.3282 |
| z3 attempt 3 (exp-bbv) | whole (reported) | 834,000,000,001 | 5.2745 | 8.0114 |
| z3 attempt 1 (exp-bbv, check) | 1 | 40,000,000,001 | 4.6503 | 6.8293 |
| z3 attempt 1 (exp-bbv, check) | 2 | 40,000,000,000 | 5.3036 | 8.0634 |
| z3 attempt 1 (exp-bbv, check) | 3 | 40,000,000,000 | 4.8577 | 7.2116 |
| z3 attempt 1 (exp-bbv, check) | 4 | 40,000,000,000 | 5.2501 | 7.9665 |
| z3 attempt 1 (exp-bbv, check) | 5 | 40,000,000,000 | 5.3331 | 8.1242 |
| z3 attempt 1 (exp-bbv, check) | 6 | 40,000,000,000 | 4.8352 | 7.1736 |
| z3 attempt 1 (exp-bbv, check) | 7 | 4,000,000,000 | 5.3589 | 8.1880 |
| z3 attempt 1 (exp-bbv, check) | whole (reported) | 244,000,000,001 | 5.0436 | 7.5717 |

C.13 `scount.c` (the synthetic completion check as a counted program, replayed exactly; Section 16.6)

    57d1f683e00854e1ba3bc0c7dbd4da65dd57952b5c0e228f03f79805759c9b72  scount.c
    bd7e1281a7edbfd8b587a1d30d2345dc127182bd406dd8e28c213e0cc21ed906  r31sim3.c (B.6, unchanged)
    d273c909ecab18fcad5cc3768c5b0d181f7cb3f4d9792f885b32b2a501a474de  sp_own.h of attempt 1 (written by check_s.py, B.2, from the attempt's z3 model)
    bb76cf1d3700dac3039e0c43f317110c0de75d24b3f5884af783ab0f5092dae8  sp_own.h of attempt 2 (written by check_s.py, B.2, from the attempt's z3 model)
    84003700c7015677e60700dc5c044d1c6e7c0acc652e6bf12d536f9aa5084437  sp_own.h of attempt 3 (written by check_s.py, B.2, from the attempt's z3 model)

Each run is built in a directory holding its `sp_own.h`, `r31sim3.c`, `scount.c` and the generated headers of C.6:
`cc -O2 -o scount scount.c -lpthread`, then `./scount 0` (run 1), `./scount 275316736` (run 2) and
`./scount 250544128` (run 3).

```c
/* scount.c: the synthetic completion check (r31sim3.c, B.6) as a counted program of 256-bit
   word-RAM primitives, replayed exactly.

   The primitives, helpers, table build, s1 inverse and self-check are those of kcount.c (C.7).
   r31sim3.c is included unchanged as the reference.  A synthetic run is deterministic: one worker
   thread whose coin stream is seeded by the seed and the thread index, trials in batches of 2^16.
   A run with N trials therefore executes exactly the first N trials of that stream, so replaying
   N = the run's logged trial count reproduces it; the replay checks every counter of the run's
   FINAL line and, trial by trial, the counters of r31sim3's own process_sim on the same draws.

   The trial loop indexes the records in the order the run's own qsort left them (the same multiset
   and key order as the counted merge sort; equal keys may sit in a different order, and a trial picks
   its record by index).  The 64-bit remainder r % nrec is computed by branch-free restoring division (64 steps of 9
   primitives).  cc -O2 -I S2 -o scount2 scount.c -lpthread (S2/sp_own.h: attempt 2's S)
   ./scount2 275316736 */
#define main r31det3_main
#include "r31sim3.c"
#undef main
#include <assert.h>

typedef unsigned __int128 W;
static __thread uint64_t OPS;
/* one primitive each; functions, so the count is sequenced whatever the operand nesting */
static inline W ADD(W a, W b) { OPS++; return a + b; }
static inline W SUB(W a, W b) { OPS++; return a - b; }
static inline W AND(W a, W b) { OPS++; return a & b; }
static inline W OR(W a, W b)  { OPS++; return a | b; }
static inline W XOR(W a, W b) { OPS++; return a ^ b; }
static inline W NOT(W a)      { OPS++; return ~a; }
static inline W SHR(W a, int n) { OPS++; return a >> n; }
static inline W SHL(W a, int n) { OPS++; return a << n; }
static inline W LD(W v)       { OPS++; return v; }
static inline W LDX(const uint64_t *bm, W a) { OPS++; return (W)bm[(uint64_t)a]; }
static inline W CMPNZ(W a)    { OPS++; return a != 0; }
static inline W CMPEQ(W a, W b) { OPS++; return a == b; }
static inline W CMPLT(W a, W b) { OPS++; return a < b; }
#define ST(dst,v) do { W st_v_ = (v); OPS++; (dst) = st_v_; } while (0)
#define BR()     (OPS++)
static const W M = 0xffffffffu, M64 = 0xffffffffffffffffull, BM = 0, C63 = 63, C1 = 1;
static inline W MSK(W a) { return AND(a, M); }

#include "gval.h"
#include "klane.h"
#include "klane_ref.h"
#include "klane_opt.h"

/* 64 x 64 -> low 64 bits by shift-and-add, branch-free: acc += (a << i) & -(b >> i & 1); 6 per bit + mask */
static W mul64_c(W a, W b) {
  W acc = 0;
  for (int i = 0; i < 64; i++) { W bit = AND(SHR(b, i), C1); W sel = SUB(0, bit); acc = ADD(acc, AND(SHL(a, i), sel)); }
  return AND(acc, M64);
}
/* splitmix64 as sm() of B.4; state in memory */
static W sm_c(uint64_t *s) {
  W z = AND(ADD(LD(*s), LD(0x9e3779b97f4a7c15ull)), M64); ST(*s, (uint64_t)z);
  z = XOR(z, SHR(z, 30)); z = mul64_c(z, LD(0xbf58476d1ce4e5b9ull));
  z = XOR(z, SHR(z, 27)); z = mul64_c(z, LD(0x94d049bb133111ebull));
  return XOR(z, SHR(z, 31));
}

/* v clean (reduced to 32 bits).  dup(v) = v | v << 32 holds two copies, so bits 0..31 of
   dup(v) >> n are ROTR(v, n); one dup serves the three rotations of a Sigma or sigma. */
static W dup_c(W v) { return OR(v, SHL(v, 32)); }
static W bs0_c(W v) { W d = dup_c(v); return XOR(XOR(SHR(d, 2), SHR(d, 13)), SHR(d, 22)); }
static W bs1_c(W v) { W d = dup_c(v); return XOR(XOR(SHR(d, 6), SHR(d, 11)), SHR(d, 25)); }
static W sg0d_c(W d, W v) { return XOR(XOR(SHR(d, 7), SHR(d, 18)), SHR(v, 3)); }
static W sg1d_c(W d, W v) { return XOR(XOR(SHR(d, 17), SHR(d, 19)), SHR(v, 10)); }
static W sg0_c(W v) { return sg0d_c(dup_c(v), v); }
static W sg1_c(W v) { return sg1d_c(dup_c(v), v); }
static W ch_c(W e, W f, W g) { return XOR(g, AND(e, XOR(f, g))); }
static W maj_c(W a, W b, W c) { return OR(AND(a, b), AND(c, OR(a, b))); }

/* compress31 of B.4: chaining value and block in memory, schedule stored, output stored */
static void compress31_c(const uint32_t cv[8], const uint32_t m[16], uint32_t out[8]) {
  uint32_t Wm[31];
  for (int t = 16; t < 31; t++) {
    const uint32_t *p2 = t - 2 < 16 ? &m[t - 2] : &Wm[t - 2], *p7 = t - 7 < 16 ? &m[t - 7] : &Wm[t - 7];
    W v = MSK(ADD(ADD(ADD(sg1_c(LD(*p2)), LD(*p7)), sg0_c(LD(m[t - 15]))), LD(m[t - 16])));
    ST(Wm[t], (uint32_t)v);
  }
  W a = LD(cv[0]), b = LD(cv[1]), c = LD(cv[2]), d = LD(cv[3]), e = LD(cv[4]), f = LD(cv[5]), g = LD(cv[6]), h = LD(cv[7]);
  for (int t = 0; t < 31; t++) {
    W w = LD(t < 16 ? m[t] : Wm[t]);
    W T1 = ADD(ADD(ADD(ADD(h, bs1_c(e)), ch_c(e, f, g)), LD(K[t])), w);
    W T2 = ADD(bs0_c(a), maj_c(a, b, c));
    h = g; g = f; f = e; e = MSK(ADD(d, T1)); d = c; c = b; b = a; a = MSK(ADD(T1, T2));
  }
  W r[8] = {a, b, c, d, e, f, g, h};
  for (int i = 0; i < 8; i++) ST(out[i], (uint32_t)MSK(ADD(LD(cv[i]), r[i])));
}

/* ---------------- table build (build_table of B.4), counted ---------------- */
typedef struct { uint64_t lo, hi, ops; uint32_t *v7, *v8, *g16; int n7, n8, ng; } p1_t;
static void *p1_worker(void *arg) {
  p1_t *p = arg; OPS = 0; p->n7 = p->n8 = p->ng = 0;
  W rD8 = LD(D8), rC8 = LD(C8), rD7 = LD(D7), rC7 = LD(C7), rD9 = LD(D9), rD18 = LD(D18);
  for (uint64_t w64 = p->lo; w64 < p->hi; w64++) {
    W w = (W)w64;                                       /* loop register, clean */
    W dw = dup_c(w), s0w = sg0d_c(dw, w), s1w = sg1d_c(dw, w);
    W d8 = MSK(SUB(sg0_c(MSK(ADD(w, rD8))), s0w));
    W hit8 = CMPEQ(d8, rC8); BR(); if (hit8) { ST(p->v8[p->n8], (uint32_t)w); p->n8 = (int)ADD(p->n8, C1); }
    W d7 = MSK(SUB(sg0_c(MSK(ADD(w, rD7))), s0w));
    W hit7 = CMPEQ(d7, rC7); BR(); if (hit7) { ST(p->v7[p->n7], (uint32_t)w); p->n7 = (int)ADD(p->n7, C1); }
    W d9 = MSK(SUB(sg1_c(MSK(ADD(w, rD9))), s1w));
    W hit9 = CMPEQ(d9, rD18); BR(); if (hit9) { ST(p->g16[p->ng], (uint32_t)w); p->ng = (int)ADD(p->ng, C1); }
    W nw = MSK(ADD(w, C1)); (void)nw; W more = CMPNZ(nw); BR(); (void)more;  /* w++ until it wraps to 0 */
  }
  p->ops = OPS; return NULL;
}

static rec_t *recs_c; static int nrec_c; static uint64_t *bitmap_c; static uint32_t G16_c[64]; static int ng16_c;
static uint32_t s1inv_col_c[32];

static uint64_t ops_p1, ops_p2, ops_sort, ops_bitmap, ops_s1inv, ops_selftest;

static void msort_c(rec_t *a, rec_t *tmp, int n) {
  /* bottom-up merge sort on key; per element moved: 2 key loads, compare, branch, 6 loads, 6 stores,
     2 index increments, loop compare and branch */
  for (int width = 1; width < n; width = (int)ADD(SHL(width, 1), 0)) {
    for (int lo = 0; lo < n; lo += 2 * width) {
      int mid = lo + width < n ? lo + width : n, hi = lo + 2 * width < n ? lo + 2 * width : n;
      OPS += 6;                                       /* mid, hi: two adds, two compares, two selects */
      int i = lo, j = mid, k = lo;
      while (k < hi) {
        int takeleft;
        if (i < mid && j < hi) { W ki = LD(a[i].key), kj = LD(a[j].key); takeleft = (int)CMPLT(kj, ki) == 0; BR(); }
        else { OPS += 2; takeleft = i < mid; }
        rec_t *s = takeleft ? &a[i] : &a[j];
        tmp[k] = (rec_t){(uint32_t)LD(s->key), (uint32_t)LD(s->A0), (uint32_t)LD(s->E3), (uint32_t)LD(s->E4), (uint32_t)LD(s->W7), (uint32_t)LD(s->W8)};
        OPS += 6;                                     /* six stores */
        if (takeleft) i = (int)ADD(i, C1); else j = (int)ADD(j, C1);
        k = (int)ADD(k, C1); OPS += 4;                /* i < mid, j < hi, k < hi compares and branch */
      }
      OPS += 3;                                       /* lo += 2*width, compare, branch */
    }
    memcpy(a, tmp, sizeof(rec_t) * n); OPS += 12ull * n;  /* copy back: 6 loads + 6 stores each */
    OPS += 2;
  }
}

static int cmpall(const void *p, const void *q) { return memcmp(p, q, sizeof(rec_t)); }
static void build_table_c(void) {
  static uint32_t V7c[1024], V8c[65536];
  /* P1: 2^32 scan in 12 slices */
  enum { NT = 12 }; p1_t sl[NT]; pthread_t th[NT];
  static uint32_t v7s[NT][1024], v8s[NT][65536], g16s[NT][64];
  for (int i = 0; i < NT; i++) {
    sl[i].lo = (1ull << 32) * i / NT; sl[i].hi = (1ull << 32) * (i + 1) / NT;
    sl[i].v7 = v7s[i]; sl[i].v8 = v8s[i]; sl[i].g16 = g16s[i];
    pthread_create(&th[i], 0, p1_worker, &sl[i]);
  }
  int n7 = 0, n8 = 0; ng16_c = 0; ops_p1 = 0;
  for (int i = 0; i < NT; i++) {
    pthread_join(th[i], 0); ops_p1 += sl[i].ops;
    memcpy(V7c + n7, sl[i].v7, 4 * sl[i].n7); n7 += sl[i].n7;
    memcpy(V8c + n8, sl[i].v8, 4 * sl[i].n8); n8 += sl[i].n8;
    memcpy(G16_c + ng16_c, sl[i].g16, 4 * sl[i].ng); ng16_c += sl[i].ng;
  }
  ops_p1 -= (NT - 1) * 6;                             /* the six constant loads are paid once */
  /* P2 */
  OPS = 0;
  uint32_t cm4 = 0, va4 = 0, cm3 = 0, va3 = 0; const char *r4 = "============0===0=========01===0", *r3 = "==========================10====";
  for (int k = 0; k < 32; k++) { uint32_t b = 1u << (31 - k); if (r4[k] != '=') { cm4 |= b; if (r4[k] == '1') va4 |= b; } if (r3[k] != '=') { cm3 |= b; if (r3[k] == '1') va3 |= b; } }
  OPS += 4 * 32 * 4;                                  /* the two row masks: 32 cells, at most 4 primitives each, both rows (loose) */
  W lhs7 = MSK(SUB(SUB(SUB(LD(EB(7)), LD(EA(7))), SUB(bs1_c(LD(EB(6))), bs1_c(LD(EA(6))))), LD(D7)));
  W lhs6 = MSK(SUB(SUB(SUB(LD(EB(6)), LD(EA(6))), SUB(bs1_c(LD(EB(5))), bs1_c(LD(EA(5))))), LD(D6)));
  rec_t *rc = malloc(sizeof(rec_t) * (1 << 20)); int nr = 0;
  W e8 = LD(EA(8)), a4 = LD(AA(4)), e7 = LD(EA(7)), e6 = LD(EA(6)), e5 = LD(EA(5)), eb6 = LD(EB(6)), eb5 = LD(EB(5));
  W a3 = LD(AA(3)), a2 = LD(AA(2)), a1 = LD(AA(1)), k8 = LD(K[8]), k7 = LD(K[7]);
  W base4 = MSK(SUB(SUB(SUB(e8, a4), bs1_c(e7)), ch_c(e7, e6, e5)));          /* loop-invariant part of E4 */
  W bs0a3 = bs0_c(a3), maja3 = maj_c(a3, a2, a1), bs0a2 = bs0_c(a2), bs1e6 = bs1_c(e6);
  W rcm4 = LD(cm4), rva4 = LD(va4), rcm3 = LD(cm3), rva3 = LD(va3);
  for (int i = 0; i < n8; i++) {
    OPS += 3;                                         /* i < n8, branch, i++ */
    W W8 = LD(V8c[i]);
    W E4 = MSK(SUB(SUB(base4, k8), W8));
    W ok4 = CMPEQ(AND(E4, rcm4), rva4); BR(); if (!ok4) continue;
    W d7 = MSK(SUB(ch_c(eb6, eb5, E4), ch_c(e6, e5, E4)));
    W ok7 = CMPEQ(d7, lhs7); BR(); if (!ok7) continue;
    W A0 = MSK(ADD(ADD(SUB(E4, a4), bs0a3), maja3));
    W b3 = MSK(SUB(SUB(SUB(e7, a3), bs1e6), ch_c(e6, e5, E4)));               /* E3 without K[7], W7 */
    W maj2 = maj_c(a2, a1, A0);
    for (int j = 0; j < n7; j++) {
      OPS += 3;
      W W7 = LD(V7c[j]);
      W E3 = MSK(SUB(SUB(b3, k7), W7));
      W ok3 = CMPEQ(AND(E3, rcm3), rva3); BR(); if (!ok3) continue;
      W d6 = MSK(SUB(ch_c(eb5, E4, E3), ch_c(e5, E4, E3)));
      W ok6 = CMPEQ(d6, lhs6); BR(); if (!ok6) continue;
      W Am1 = MSK(ADD(ADD(SUB(E3, a3), bs0a2), maj2));
      rc[nr] = (rec_t){(uint32_t)Am1, (uint32_t)A0, (uint32_t)E3, (uint32_t)E4, (uint32_t)W7, (uint32_t)W8};
      OPS += 6; nr = (int)ADD(nr, C1);                /* six stores, count */
    }
    OPS += 1;                                         /* final j compare */
  }
  OPS += 1;
  ops_p2 = OPS;
  /* sort */
  OPS = 0; rec_t *tmp = malloc(sizeof(rec_t) * nr); msort_c(rc, tmp, nr); free(tmp); ops_sort = OPS;
  recs_c = rc; nrec_c = nr;
  /* bitmap: 2^18 zero stores, then one bit per record */
  OPS = 0; bitmap_c = calloc(1 << 18, 8); OPS += 1u << 18;
  for (int i = 0; i < nr; i++) {
    OPS += 3;
    W b = SHR(LD(rc[i].key), 8); W wi = SHR(b, 6); W addr = ADD(BM, wi);
    W word = LDX(bitmap_c, addr); W bit = SHL(C1, (int)AND(b, C63));
    bitmap_c[(uint64_t)addr] = (uint64_t)OR(word, bit); OPS++;
  }
  ops_bitmap = OPS;
  /* compare with r31det3's build_table (called before) */
  assert(n7 == 512 && n8 == 49408 && ng16_c == ng16 && nr == nrec);
  for (int i = 0; i < ng16; i++) assert(G16_c[i] == G16[i]);
  assert(memcmp(bitmap_c, bitmap, 8u << 18) == 0);
  for (int i = 0; i < nr; i++) { assert(recs_c[i].key == recs[i].key); if (i) assert(recs_c[i - 1].key <= recs_c[i].key); }
  /* same multiset of records: sort copies by all fields */
  rec_t *x1 = malloc(sizeof(rec_t) * nr), *x2 = malloc(sizeof(rec_t) * nr);
  memcpy(x1, recs, sizeof(rec_t) * nr); memcpy(x2, recs_c, sizeof(rec_t) * nr);
  qsort(x1, nr, sizeof(rec_t), cmpall); qsort(x2, nr, sizeof(rec_t), cmpall); assert(memcmp(x1, x2, sizeof(rec_t) * nr) == 0);
  free(x1); free(x2);
}

/* build_s1inv of B.4, counted (pivot search branches on data that is fixed: s1 itself) */
static void build_s1inv_c(void) {
  OPS = 0;
  uint32_t val[32], comb[32];
  for (int i = 0; i < 32; i++) { W b = SHL(C1, i); ST(val[i], (uint32_t)MSK(sg1_c(b))); ST(comb[i], (uint32_t)b); }
  for (int k = 0; k < 32; k++) {
    int p = -1;
    for (int i = k; i < 32; i++) { OPS += 3; W bit = AND(SHR(LD(val[i]), k), C1); BR(); if (bit) { p = i; break; } }
    BR();
    uint32_t tv = (uint32_t)LD(val[k]), tc = (uint32_t)LD(comb[k]);
    ST(val[k], (uint32_t)LD(val[p])); ST(comb[k], (uint32_t)LD(comb[p])); ST(val[p], tv); ST(comb[p], tc);
    for (int i = 0; i < 32; i++) {
      OPS += 2; W bit = AND(SHR(LD(val[i]), k), C1); W ne = CMPNZ(i != k); BR(); BR();
      if (i != k && bit) { ST(val[i], (uint32_t)XOR(LD(val[i]), LD(val[k]))); ST(comb[i], (uint32_t)XOR(LD(comb[i]), LD(comb[k]))); }
      (void)ne;
    }
  }
  for (int k = 0; k < 32; k++) ST(s1inv_col_c[k], (uint32_t)LD(comb[k]));
  for (int t = 0; t < 1000; t++) {                    /* the 1000-value self-check */
    OPS += 3; W y = MSK(ADD(mul64_c(LD((uint32_t)t), LD(2654435761u)), LD(12345u)));
    assert((uint32_t)y == (uint32_t)(t * 2654435761u + 12345));
    W xx = 0;
    for (int k = 0; k < 32; k++) { W bit = AND(SHR(y, k), C1); xx = XOR(xx, AND(LD(s1inv_col_c[k]), SUB(0, bit))); }
    W back = MSK(sg1_c(MSK(xx))); W ok = CMPEQ(back, y); BR(); assert(ok);
  }
  for (int k = 0; k < 32; k++) assert(s1inv_col_c[k] == s1inv_col[k]);
  ops_s1inv = OPS;
}
static W s1inv_c(W y) {
  W xx = 0;
  for (int k = 0; k < 32; k++) { W bit = AND(SHR(y, k), C1); xx = XOR(xx, AND(LD(s1inv_col_c[k]), SUB(0, bit))); }
  return MSK(xx);
}

/* group set-up of worker (B.4), counted; returns m[0..14], group values, completion coins */
static void gvalues_from_words(const uint32_t m[15], gval_t *G);
static void gsetup_c(uint64_t g, uint32_t m[15], gval_t *G, uint64_t *crs) {
  OPS += 3;                                           /* groups counter: load, add, store */
  uint64_t rs = (uint64_t)XOR(XOR(LD(seed_base), mul64_c(g, LD(0x9e3779b97f4a7c15ull))), LD(0x5bd1e9955bd1e995ull)); OPS++;
  for (int i = 0; i < 15; i++) ST(m[i], (uint32_t)AND(sm_c(&rs), M));
  ST(*crs, (uint64_t)XOR(XOR(LD(seed_base), mul64_c(g, LD(0xd1b54a32d192ed03ull))), LD(0x2545f4914f6cdd1dull)));
  gvalues_from_words(m, G);
}

/* rec address: base + 6*r (records are six words) */
#define RADDR(r) ADD(ADD(SHL((W)(r), 2), SHL((W)(r), 1)), 0)

/* ---------------- the synthetic check, counted ---------------- */
typedef struct { uint64_t recs, v6, joint, both, comp_try, comp_ok, coll; } sstat_t;

/* r % n, branch-free restoring division over the 64 bits of r */
static W urem64_c(W r, W n) {
  W rem = 0;
  for (int i = 63; i >= 0; i--) {
    rem = OR(SHL(rem, 1), AND(SHR(r, i), C1));
    W ge = XOR(CMPLT(rem, n), C1);
    rem = SUB(rem, AND(n, SUB(0, ge)));
  }
  return rem;
}

static int complete_sim_c(uint32_t Wv[16], W g, uint64_t *rs) {
  W W9 = LD(Wv[9]), W1 = LD(Wv[1]), W0 = LD(Wv[0]);
  W s0W1 = sg0_c(W1);
  W W14 = s1inv_c(MSK(SUB(SUB(SUB(g, W9), s0W1), W0))); ST(Wv[14], (uint32_t)W14);
  W chk = CMPEQ(MSK(ADD(ADD(ADD(sg1_c(W14), W9), s0W1), W0)), g); BR(); if (!chk) return 0;
#define LA(i) LD(AA(i))
#define LE(i) LD(EA(i))
#define LAB(i) LD(AB(i))
#define LEB(i) LD(EB(i))
  W b13 = MSK(ADD(ADD(ADD(ADD(LA(9), LE(9)), bs1_c(LE(12))), ch_c(LE(12), LE(11), LE(10))), LD(K[13])));
  W b13b = MSK(ADD(ADD(ADD(ADD(LAB(9), LEB(9)), bs1_c(LEB(12))), ch_c(LEB(12), LEB(11), LEB(10))), LD(K[13])));
  W eq = CMPEQ(b13, b13b); BR(); if (!eq) return 0;
  W m13 = LD(~0x10c08000u & 0xffffffffu), o13 = LD(0x00408000u), m15 = LD(~0x00008004u & 0xffffffffu), o15 = LD(0x00000004u);
  for (int t = 0; t < (1 << 14); t++) {
    OPS += 3;
    W E13 = OR(AND(sm_c(rs), m13), o13); W W13 = MSK(SUB(E13, b13));
    W A13 = MSK(ADD(ADD(SUB(E13, LA(9)), bs0_c(LA(12))), maj_c(LA(12), LA(11), LA(10))));
    W A13b = MSK(ADD(ADD(SUB(E13, LAB(9)), bs0_c(LAB(12))), maj_c(LAB(12), LAB(11), LAB(10))));
    W e1 = CMPEQ(A13, A13b); BR(); if (!e1) return 0;
    W E14 = MSK(ADD(ADD(ADD(ADD(ADD(LA(10), LE(10)), bs1_c(E13)), ch_c(E13, LE(12), LE(11))), LD(K[14])), W14));
    W E14b = MSK(ADD(ADD(ADD(ADD(ADD(LAB(10), LEB(10)), bs1_c(E13)), ch_c(E13, LEB(12), LEB(11))), LD(K[14])), W14));
    W e2 = CMPEQ(MSK(SUB(E14b, E14)), LD(0x8004u)); BR(); if (!e2) continue;
    W A14 = MSK(ADD(ADD(SUB(E14, LA(10)), bs0_c(A13)), maj_c(A13, LA(12), LA(11))));
    W A14b = MSK(ADD(ADD(SUB(E14b, LAB(10)), bs0_c(A13)), maj_c(A13, LAB(12), LAB(11))));
    W e3 = CMPEQ(A14, A14b); BR(); if (!e3) continue;
    W f15 = MSK(ADD(ADD(ADD(ADD(LA(11), LE(11)), bs1_c(E14)), ch_c(E14, E13, LE(12))), LD(K[15])));
    W f15b = MSK(ADD(ADD(ADD(ADD(LAB(11), LEB(11)), bs1_c(E14b)), ch_c(E14b, E13, LEB(12))), LD(K[15])));
    W e4 = CMPEQ(f15, f15b); BR(); if (!e4) continue;
    for (int u = 0; u < (1 << 8); u++) {
      OPS += 3;
      W E15 = OR(AND(sm_c(rs), m15), o15); W W15 = MSK(SUB(E15, f15));
      W E16 = MSK(ADD(ADD(ADD(ADD(ADD(LA(12), LE(12)), bs1_c(E15)), ch_c(E15, E14, E13)), LD(K[16])), g));
      W E16b = MSK(ADD(ADD(ADD(ADD(ADD(ADD(LAB(12), LEB(12)), bs1_c(E15)), ch_c(E15, E14b, E13)), LD(K[16])), g), LD(D9)));
      W e5 = CMPEQ(E16, E16b); BR(); if (!e5) continue;
      W A15 = MSK(ADD(ADD(SUB(E15, LA(11)), bs0_c(A14)), maj_c(A14, A13, LA(12)))); (void)A15;
      W f17 = MSK(ADD(ADD(ADD(A13, E13), bs1_c(E16)), ch_c(E16, E15, E14)));
      W f17b = MSK(ADD(ADD(ADD(A13, E13), bs1_c(E16)), ch_c(E16, E15, E14b)));
      W e6 = CMPEQ(f17, f17b); BR(); if (!e6) continue;
      ST(Wv[13], (uint32_t)W13); ST(Wv[15], (uint32_t)W15); return 1;
    }
    OPS += 1;
  }
  return 0;
}

static void process_sim_c(const rec_t *q, const uint32_t cv[8], uint64_t *rs, sstat_t *st) {
  st->recs++; OPS += 3;
  W Am1 = LD(cv[0]), Am2 = LD(cv[1]), Am3 = LD(cv[2]), Am4 = LD(cv[3]), Em1 = LD(cv[4]), Em2 = LD(cv[5]), Em3 = LD(cv[6]), Em4 = LD(cv[7]);
  W A0 = LD(q->A0), A1 = LD(AA(1)), A2 = LD(AA(2));
  W E0 = MSK(SUB(SUB(ADD(A0, Am4), bs0_c(Am1)), maj_c(Am1, Am2, Am3)));
  W E1 = MSK(SUB(SUB(ADD(A1, Am3), bs0_c(A0)), maj_c(A0, Am1, Am2)));
  W E2 = MSK(SUB(SUB(ADD(A2, Am2), bs0_c(A1)), maj_c(A1, A0, Am1)));
  W E3 = LD(q->E3), E4 = LD(q->E4), E5 = LD(EA(5)), E6 = LD(EA(6));
  W Ex[11] = {Em4, Em3, Em2, Em1, E0, E1, E2, E3, E4, E5, E6};
  W Ax[7] = {Am4, Am3, Am2, Am1, A0, A1, A2};
  uint32_t Wv[16];
  for (int i = 0; i <= 6; i++) {
    W v = MSK(SUB(SUB(SUB(SUB(SUB(Ex[i + 4], Ax[i]), Ex[i]), bs1_c(Ex[i + 3])), ch_c(Ex[i + 3], Ex[i + 2], Ex[i + 1])), LD(K[i])));
    ST(Wv[i], (uint32_t)v);
  }
  ST(Wv[7], (uint32_t)LD(q->W7)); ST(Wv[8], (uint32_t)LD(q->W8));
  for (int i = 9; i <= 12; i++) ST(Wv[i], (uint32_t)LD(S_W[i]));
  ST(Wv[13], 0u); ST(Wv[14], 0u); ST(Wv[15], 0u);
  W W6 = LD(Wv[6]);
  W v6 = CMPEQ(MSK(SUB(sg0_c(MSK(ADD(W6, LD(D6)))), sg0_c(W6))), LD(C6));
  W W5 = LD(Wv[5]);
  W tgt = MSK(SUB(0, MSK(SUB(sg0_c(MSK(ADD(W5, LD(D5)))), sg0_c(W5)))));
  W c18 = ADD(ADD(LD(Wv[11]), sg0_c(LD(Wv[3]))), LD(Wv[2]));
  int gsel = -1;
  for (int k = 0; ; k++) {
    W c = CMPLT((W)k, LD(ng16_c)); BR(); if (!c) break;
    W gaddr = ADD(0, (W)k); W gk = LD(G16_c[(int)gaddr]);
    W w18 = MSK(ADD(sg1_c(gk), c18));
    W d = MSK(SUB(sg1_c(MSK(ADD(w18, LD(D18)))), sg1_c(w18)));
    W e = CMPEQ(d, tgt); BR();
    if (e) { gsel = k; break; }
    OPS += 1;
  }
  BR(); if (v6) { st->v6++; OPS += 3; }
  BR(); if (gsel < 0) return;
  st->joint++; OPS += 3; BR(); if (v6) { st->both++; OPS += 3; }
  st->comp_try++; OPS += 3;
  uint32_t Wc[16]; for (int i = 0; i < 16; i++) ST(Wc[i], (uint32_t)LD(Wv[i]));
  int ok = complete_sim_c(Wc, LD(G16_c[gsel]), rs); BR();
  if (!ok) return;
  st->comp_ok++; OPS += 3;
  BR(); if (!v6) return;
  uint32_t Wb[16]; for (int i = 0; i < 16; i++) ST(Wb[i], (uint32_t)LD(Wc[i]));
  const uint32_t dd[5] = {D5, D6, D7, D8, D9};
  for (int i = 0; i < 5; i++) ST(Wb[5 + i], (uint32_t)MSK(ADD(LD(Wb[5 + i]), LD(dd[i]))));
  uint32_t o1[8], o2[8]; compress31_c(cv, Wc, o1); compress31_c(cv, Wb, o2);
  int same = 1;
  for (int i = 0; i < 8; i++) { W e = CMPEQ(LD(o1[i]), LD(o2[i])); BR(); same &= (int)e; }
  if (same) { st->coll++; OPS += 3; }
}

/* the synthetic run's worker (simworker of B.6), counted, for exactly N trials */
static uint64_t sim_ops; static sstat_t sim_st; static uint64_t sim_N;
static void *sim_counted(void *arg) {
  (void)arg; OPS = 0;
  uint64_t rs = (uint64_t)XOR(LD(seed_base), mul64_c(LD(0x51ed27u), C1));  /* tid 0: 0x51ed27 * 1 */
  W rn = LD(nrec_c);
  for (uint64_t b = 0; b < sim_N >> 16; b++) {
    for (int it = 0; it < (1 << 16); it++) {
      OPS += 3;                                         /* it < 2^16, branch, it++ */
      W r = sm_c(&rs);
      W idx = urem64_c(r, rn);
      const rec_t *q = &recs[(uint32_t)idx]; W a = RADDR(idx); (void)a;   /* records in the run's (qsort) order */
      uint32_t cv[8]; ST(cv[0], (uint32_t)LD(q->key));
      W r2 = sm_c(&rs), r3 = sm_c(&rs), r4 = sm_c(&rs);
      ST(cv[1], (uint32_t)SHR(r, 32)); ST(cv[2], (uint32_t)AND(r2, M)); ST(cv[3], (uint32_t)SHR(r2, 32));
      ST(cv[4], (uint32_t)AND(r3, M)); ST(cv[5], (uint32_t)SHR(r3, 32)); ST(cv[6], (uint32_t)AND(r4, M)); ST(cv[7], (uint32_t)SHR(r4, 32));
      process_sim_c(q, cv, &rs, &sim_st);
    }
    OPS += 3 + 3 + 3;                                   /* trials += 2^16; stop flag load, test, branch; batch loop */
  }
  sim_ops = OPS; return NULL;
}
/* reference: simworker's batch loop of B.6, verbatim, for exactly N trials */
static uint64_t ref_N;
static void *sim_ref(void *arg) {
  int tid = 0; uint64_t rs = seed_base ^ (0x51ed27ull * (uint64_t)(tid + 1)); ctr_t *c = &ctrs[tid]; (void)arg;
  for (uint64_t b = 0; b < ref_N >> 16; b++) {
    for (int it = 0; it < (1 << 16); it++) {
      uint64_t r = sm(&rs); const rec_t *q = &recs[(uint32_t)(r % (uint64_t)nrec)];
      uint32_t cv[8]; cv[0] = q->key; uint64_t r2 = sm(&rs), r3 = sm(&rs), r4 = sm(&rs);
      cv[1] = (uint32_t)(r >> 32); cv[2] = (uint32_t)r2; cv[3] = (uint32_t)(r2 >> 32); cv[4] = (uint32_t)r3; cv[5] = (uint32_t)(r3 >> 32); cv[6] = (uint32_t)r4; cv[7] = (uint32_t)(r4 >> 32);
      process_sim(tid, q, cv, &rs); }
    c->trials += 1 << 16; }
  return NULL;
}

int main(int argc, char **argv) {
  seed_base = 0x5eed3;                                  /* r31sim3 1 20 5eed3 ... sim */
  outf = fopen("/dev/null", "w");
  uint64_t N = argc > 1 ? strtoull(argv[1], 0, 10) : 0;
  build_s1inv(); build_table();
  build_table_c();
  printf("table: records=%d identical to build_table; ops P1 %llu P2 %llu sort %llu bitmap %llu\n", nrec_c, (unsigned long long)ops_p1,
         (unsigned long long)ops_p2, (unsigned long long)ops_sort, (unsigned long long)ops_bitmap);
  build_s1inv_c();
  printf("ops s1inv+check %llu\n", (unsigned long long)ops_s1inv);
  {
    OPS = 0; uint64_t r2 = 7;
    for (int t = 0; t < 2000; t++) {
      OPS += 3;
      uint32_t mb[16]; for (int i = 0; i < 16; i++) ST(mb[i], (uint32_t)AND(sm_c(&r2), M));
      gval_t G; gvalues_from_words(mb, &G);
      uint32_t kc; (void)klane_opt(&G, LD(mb[15]), bitmap_c, &kc);
      uint32_t ref[8]; compress31_c(IV, mb, ref);
      W ok = CMPEQ(LD(ref[0]), kc); BR(); assert(ok);
    }
    ops_selftest = OPS;
    printf("ops selftest %llu (2000 blocks)\n", (unsigned long long)ops_selftest);
  }
  if (N == 0 || nrec == 0) { printf("no trial loop replayed (N=%llu, records=%d)\n", (unsigned long long)N, nrec); return 0; }
  sim_N = ref_N = N;
  pthread_t a, b; pthread_create(&a, 0, sim_counted, 0); pthread_create(&b, 0, sim_ref, 0); pthread_join(a, 0); pthread_join(b, 0);
  ctr_t *c = &ctrs[0];
  printf("replay of %llu trials: counted recs=%llu v6=%llu joint=%llu both=%llu comp=%llu/%llu coll=%llu ; reference recs=%llu v6=%llu joint=%llu both=%llu comp=%llu/%llu coll=%llu\n",
    (unsigned long long)N, (unsigned long long)sim_st.recs, (unsigned long long)sim_st.v6, (unsigned long long)sim_st.joint, (unsigned long long)sim_st.both,
    (unsigned long long)sim_st.comp_ok, (unsigned long long)sim_st.comp_try, (unsigned long long)sim_st.coll,
    (unsigned long long)c->recs, (unsigned long long)c->v6, (unsigned long long)c->joint, (unsigned long long)c->both,
    (unsigned long long)c->comp_ok, (unsigned long long)c->comp_try, (unsigned long long)c->coll);
  assert(sim_st.recs == c->recs && sim_st.v6 == c->v6 && sim_st.joint == c->joint && sim_st.both == c->both &&
         sim_st.comp_try == c->comp_try && sim_st.comp_ok == c->comp_ok && sim_st.coll == c->coll);
  printf("FINAL-equivalent trials=%llu rechits=%llu v6=%llu joint=%llu both=%llu comp=%llu/%llu coll=%llu\n", (unsigned long long)N,
    (unsigned long long)sim_st.recs, (unsigned long long)sim_st.v6, (unsigned long long)sim_st.joint, (unsigned long long)sim_st.both,
    (unsigned long long)sim_st.comp_ok, (unsigned long long)sim_st.comp_try, (unsigned long long)sim_st.coll);
  printf("ops trial loop %llu (%.2f per trial)\n", (unsigned long long)sim_ops, (double)sim_ops / N);
  return 0;
}


#define LM(i) LD(m[i])
#define SG(field, v) ST(G->field, (uint32_t)MSK(v))
static void gvalues_from_words(const uint32_t m[15], gval_t *G) {
  W a = LD(IV[0]), b = LD(IV[1]), c = LD(IV[2]), d = LD(IV[3]), e = LD(IV[4]), f = LD(IV[5]), gg = LD(IV[6]), h = LD(IV[7]);
  for (int t = 0; t < 15; t++) {
    W T1 = ADD(ADD(ADD(ADD(h, bs1_c(e)), ch_c(e, f, gg)), LD(K[t])), LD(m[t]));
    W T2 = ADD(bs0_c(a), maj_c(a, b, c));
    h = gg; gg = f; f = e; e = MSK(ADD(d, T1)); d = c; c = b; b = a; a = MSK(ADD(T1, T2));
  }
  W m16 = MSK(ADD(ADD(ADD(sg1_c(LM(14)), LM(9)), sg0_c(LM(1))), LM(0)));
  W m18 = MSK(ADD(ADD(ADD(sg1_c(m16), LM(11)), sg0_c(LM(3))), LM(2)));
  W m20 = MSK(ADD(ADD(ADD(sg1_c(m18), LM(13)), sg0_c(LM(5))), LM(4)));
  W p15 = ADD(ADD(ADD(h, bs1_c(e)), ch_c(e, f, gg)), LD(K[15]));
  W q15 = ADD(bs0_c(a), maj_c(a, b, c));
  SG(U15, ADD(d, p15)); SG(V15, ADD(p15, q15));
  ST(G->a, (uint32_t)a); ST(G->b, (uint32_t)b); ST(G->c, (uint32_t)c); ST(G->e, (uint32_t)e); ST(G->f, (uint32_t)f);
  ST(G->ab, (uint32_t)AND(a, b)); ST(G->axb, (uint32_t)XOR(a, b)); ST(G->exf, (uint32_t)XOR(e, f));
  SG(P16, ADD(ADD(gg, LD(K[16])), m16)); SG(P17, ADD(f, LD(K[17]))); SG(P18, ADD(ADD(e, LD(K[18])), m18));
  SG(KW20, ADD(LD(K[20]), m20));
  SG(c17, ADD(ADD(LM(10), sg0_c(LM(2))), LM(1))); SG(c19, ADD(ADD(LM(12), sg0_c(LM(4))), LM(3)));
  SG(c21, ADD(ADD(LM(14), sg0_c(LM(6))), LM(5))); SG(c22, ADD(ADD(sg1_c(m20), sg0_c(LM(7))), LM(6)));
  SG(c23, ADD(ADD(m16, sg0_c(LM(8))), LM(7))); SG(c24, ADD(sg0_c(LM(9)), LM(8)));
  SG(c25, ADD(ADD(m18, sg0_c(LM(10))), LM(9))); SG(c26, ADD(sg0_c(LM(11)), LM(10)));
  SG(c27, ADD(ADD(m20, sg0_c(LM(12))), LM(11))); SG(c28, ADD(sg0_c(LM(13)), LM(12)));
  SG(c29k, ADD(ADD(sg0_c(LM(14)), LM(13)), LD(K[29]))); SG(c30k, ADD(ADD(LM(14), LD(K[30])), LD(IV[0])));
  ST(G->K19, (uint32_t)LD(K[19])); ST(G->K21, (uint32_t)LD(K[21])); ST(G->K22, (uint32_t)LD(K[22])); ST(G->K23, (uint32_t)LD(K[23]));
  ST(G->K24, (uint32_t)LD(K[24])); ST(G->K25, (uint32_t)LD(K[25])); ST(G->K26, (uint32_t)LD(K[26])); ST(G->K27, (uint32_t)LD(K[27]));
  ST(G->K28, (uint32_t)LD(K[28]));
}
```

C.14 Output of the synthetic replays and of the re-run of synthetic run 1

Run 1, `./scount` (standard output, then standard error):

```
table: records=0 identical to build_table; ops P1 236223301254 P2 63006824 sort 0 bitmap 262144
ops s1inv+check 608280
ops selftest 30630000 (2000 blocks)
no trial loop replayed (N=0, records=0)
```

```
V7=512 V8=49408 G16=64 records=0
```

Run 2, `./scount` (standard output, then standard error):

```
table: records=224 identical to build_table; ops P1 236223301254 P2 702792 sort 61656 bitmap 264832
ops s1inv+check 608280
ops selftest 30630000 (2000 blocks)
replay of 275316736 trials: counted recs=275316736 v6=538099 joint=42381 both=88 comp=42381/42381 coll=88 ; reference recs=275316736 v6=538099 joint=42381 both=88 comp=42381/42381 coll=88
FINAL-equivalent trials=275316736 rechits=275316736 v6=538099 joint=42381 both=88 comp=42381/42381 coll=88
ops trial loop 1745020550020 (6338.23 per trial)
```

```
V7=512 V8=49408 G16=64 records=224
```

Run 3, `./scount` (standard output, then standard error):

```
table: records=132096 identical to build_table; ops P1 236223301254 P2 81321704 sort 81135912 bitmap 1847296
ops s1inv+check 608280
ops selftest 30630000 (2000 blocks)
replay of 250544128 trials: counted recs=250544128 v6=489532 joint=38874 both=64 comp=38874/38874 coll=64 ; reference recs=250544128 v6=489532 joint=38874 both=64 comp=38874/38874 coll=64
FINAL-equivalent trials=250544128 rechits=250544128 v6=489532 joint=38874 both=64 comp=38874/38874 coll=64
ops trial loop 1588088539519 (6338.56 per trial)
```

```
V7=512 V8=49408 G16=64 records=132096
```

Re-run of run 1's command with attempt 1's S (`cc -O3 -mcpu=apple-m4`, `/usr/bin/time -l ./r31sim3 1 20 5eed3 /dev/null sim`):

```
exit status 139 (signal 11, segmentation fault)
standard error:
V7=512 V8=49408 G16=64 records=0
kernel check OK
        5.48 real         5.15 user         0.01 sys
             1900544  maximum resident set size
        124642769780  instructions retired
```

C.15 `libmeasure.c` (retired instructions per library call and per process launch, Section 9, H8)

    84f4d465f50dc9bdf4fa69c31c4a23beff90d2ad3e955489cba1b319fc3347b3  libmeasure.c

`cc -O2 -o libmeasure libmeasure.c -lpthread -lm && ./libmeasure` on the machine that ran C (Apple M4 Pro, the
same macOS and libraries). An empty program (`int main(void){return 0;}`, `/usr/bin/time -l`) retires
11,017,339, 10,583,825 and 10,732,894 instructions in three runs. Output:

```
empty loop                                 17 instructions per call (1000 calls)
printf progress line                     9292 instructions per call (1000 calls)
fprintf %08x                              944 instructions per call (10000 calls)
fprintf short line                       2513 instructions per call (10000 calls)
fflush                                    356 instructions per call (1000 calls)
fopen+fclose                           146511 instructions per call (200 calls)
malloc 24 MB + free                      1794 instructions per call (50 calls)
calloc 256 MB + free                 24967525 instructions per call (20 calls)
pthread_create+join                     90350 instructions per call (200 calls)
mutex lock+unlock                          80 instructions per call (10000 calls)
sleep(0)                                 8327 instructions per call (1000 calls)
usleep(1000)                            11270 instructions per call (200 calls)
clock_gettime                             190 instructions per call (10000 calls)
access                                   4977 instructions per call (1000 calls)
atoi+atof+strtoull                        182 instructions per call (10000 calls)
log2                                       57 instructions per call (10000 calls)
sqrt                                       12 instructions per call (10000 calls)
pow                                        52 instructions per call (10000 calls)
fscanf %x                                1094 instructions per call (10000 calls)
counter read only (overhead)             5848 instructions per call (1 calls)
```

```c
/* libmeasure.c: retired instructions per library call, on the machine and libraries that ran C.
   Each call kind used by the charged programs runs N times; the process's retired-instruction counter
   (proc_pid_rusage, RUSAGE_INFO_V4) is read before and after, and the per-call mean is printed.
   cc -O2 -o libmeasure libmeasure.c -lpthread -lm */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <unistd.h>
#include <pthread.h>
#include <libproc.h>
#include <sys/resource.h>

static uint64_t instr(void) {
  struct rusage_info_v4 ri;
  proc_pid_rusage(getpid(), RUSAGE_INFO_V4, (rusage_info_t *)&ri);
  return ri.ri_instructions;
}
static void *thr(void *a) { return a; }
static volatile double sink; static volatile uint64_t isink;

#define MEASURE(name, N, body) do { uint64_t t0 = instr(); for (int i_ = 0; i_ < (N); i_++) { body; } uint64_t t1 = instr(); \
  printf("%-34s %10.0f instructions per call (%d calls)\n", name, (double)(t1 - t0) / (N), (N)); } while (0)

int main(void) {
  FILE *dn = fopen("/dev/null", "w");
  uint64_t u = 123456789012ull; double d = 1.234e5;
  MEASURE("empty loop", 1000, isink += 1);
  MEASURE("printf progress line", 1000, fprintf(dn, "t=%.0f trials=%llu (2^%.3f) rate=%.3e/s keyhits=%llu rechits=%llu v6=%llu joint=%llu both=%llu comp=%llu/%llu coll=%llu\n",
          d, (unsigned long long)u, log2((double)u), d / 3.0, (unsigned long long)u, (unsigned long long)u, (unsigned long long)u,
          (unsigned long long)u, (unsigned long long)u, (unsigned long long)u, (unsigned long long)u, (unsigned long long)u));
  MEASURE("fprintf %08x", 10000, fprintf(dn, "%08x", (unsigned)u));
  MEASURE("fprintf short line", 10000, fprintf(dn, "V7=%d V8=%d G16=%d records=%d\n", 512, 49408, 64, 132096));
  MEASURE("fflush", 1000, fflush(dn));
  MEASURE("fopen+fclose", 200, { FILE *f = fopen("/dev/null", "a"); fclose(f); });
  MEASURE("malloc 24 MB + free", 50, { void *p = malloc(24u << 20); isink += (uintptr_t)p; free(p); });
  MEASURE("calloc 256 MB + free", 20, { void *p = calloc(1u << 25, 8); isink += (uintptr_t)p; free(p); });
  MEASURE("pthread_create+join", 200, { pthread_t t; pthread_create(&t, 0, thr, 0); pthread_join(t, 0); });
  { pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER; MEASURE("mutex lock+unlock", 10000, { pthread_mutex_lock(&m); pthread_mutex_unlock(&m); }); }
  MEASURE("sleep(0)", 1000, sleep(0));
  MEASURE("usleep(1000)", 200, usleep(1000));
  { struct timespec ts; MEASURE("clock_gettime", 10000, clock_gettime(CLOCK_MONOTONIC, &ts)); }
  MEASURE("access", 1000, isink += access("STOP", F_OK));
  MEASURE("atoi+atof+strtoull", 10000, { isink += atoi("12"); sink = atof("20"); isink += strtoull("dfafc947679ebe06", 0, 16); });
  MEASURE("log2", 10000, sink = log2(d + isink));
  MEASURE("sqrt", 10000, sink = sqrt(d + isink));
  MEASURE("pow", 10000, sink = pow(2.0, -18.0 + (isink & 1)));
  { FILE *w = fopen("libmeasure_hex.txt", "w"); for (int i = 0; i < 10000; i++) fprintf(w, "%08x\n", (unsigned)(i * 2654435761u)); fclose(w);
    FILE *f = fopen("libmeasure_hex.txt", "r"); unsigned x;
    MEASURE("fscanf %x", 10000, { if (fscanf(f, "%x", &x) == 1) isink += x; }); fclose(f); }
  MEASURE("counter read only (overhead)", 1, { (void)0; });
  return 0;
}
```

Python runs: `/usr/bin/time -l` instruction counts on the same machine (Python 3.12.2): `python3 -c pass`
213,502,045; `python3 gen_s.py 88108365` 229,782,531; `python3 check_s.py s-out3.txt` 267,571,748; `python3
check_s.py s-out.txt` 241,028,997; `python3 analyze.py` 463,159,626. Per-form means of complete callgrind profiles of
Debian python3.11 in the container of Section 14.4 (`pyprof.py`, below): gen_s.py 5.1482, check_s.py 4.5983,
`-c pass` 5.6497 (unmapped instructions at 1024).

    5bee48cc29ddb16514b52957b82dde02218c9ba750c0b2f5080fd6267fd4691f  pyprof.py

```python
"""Per-form mean of complete callgrind profiles of CPython runs (objects mapped by file name in BINDIR).
usage: pyprof.py BINDIR DUMP [DUMP ...]"""
import collections, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a64ops, heavy  # noqa: E402
from cgmix import read_dump, disasm  # noqa: E402


def main():
    bindir, dumps = sys.argv[1], sys.argv[2:]
    for dpath in dumps:
        cnt = read_dump(dpath)
        tot = ops8 = ops5 = unm = 0
        for ob, c in cnt.items():
            name = os.path.basename(ob or '')
            path = os.path.join(bindir, name)
            dis = disasm(path, set(c)) if name and os.path.exists(path) else {}
            for a, n in c.items():
                tot += n
                ins = dis.get(a)
                if ins is None:
                    unm += n
                    ops8 += 1024 * n
                    ops5 += 1024 * n
                    continue
                ops8 += heavy.cost(ins[0], ins[1])[0] * n
                ops5 += a64ops.cost(ins[0], ins[1])[0] * n
        print(f"{os.path.basename(dpath)}: instructions {tot:,}, unmapped {unm:,}, per-form mean {ops8 / tot:.4f} (v5 prices {ops5 / tot:.4f})")


if __name__ == '__main__':
    main()
```

## Appendix D. `swar7_k.py` and its output

sha256 c000c93ba2434f0f93b574fd5f42489f7329249aeacba6d09d89d9c63c985c18  swar7_k.py

Run as `python3 -I swar7_k.py` next to `kprog_extracted.py` (Appendix C.6 of f99530e8, verbatim) and the organizer's
`verifier/hash_functions.py`. It is a participant tool; it is not an organizer experiment.

```python
"""Search K of jungjipdo's sha256-r31 package (f99530e8), rewritten as a SWAR word-RAM program.

One pass = 7 consecutive trials j..j+6 of the SAME group (lanes differ only in message word 15).
Every 32-bit value lives in a 36-bit lane of a 256-bit word (lane l = bits 36l..36l+35, 7*36 = 252;
bits 252..255 unused).  Group values (anything that depends only on words 0..14) are lane-broadcast
once per group and loaded from memory, one counted load per use, exactly where kprog.py (proof
Appendix C.6) loads the scalar group value.

Primitives (collision-frontier-v5), 1 each: 256-bit load/store, add/sub mod 2^256, AND/OR/XOR/NOT,
whole-word shift, comparison, conditional branch.  Conventions copied from proof Section 16.1:
  * ALU operands are registers; the only immediates are shift counts.  Every other operand is a
    counted load (group values, round constants, lane masks, loop constants, bitmap words).
  * Four registers are fixed for the whole run: M7 (2^32-1 in every lane; replaces kprog's M),
    BM (bitmap base), C63, C1.  Everything else -- including all 22 rotation/shift lane masks --
    is loaded at EVERY use (conservative; a register-resident variant is reported as sensitivity).
  * Fixed-count loops are straight line; data-dependent loops pay counter, comparison, branch.

Lane soundness (checked statically for every op and dynamically on every executed op):
  * A per-lane rotation is ((v >> r) & LO_r) | ((v << (32-r)) & HI_r): 5 ALU ops.  The masks take
    lane bits r..31 and 0..r-1 of the SAME lane only, so it is exact whenever the low 32 bits of
    each lane are right, whatever the 4 guard bits hold.  sigma's plain shift is (v >> k) & SHR_k.
  * Every add requires (static upper bound of lane a) + (bound of lane b) <= 2^36-1, so no carry
    ever leaves a lane (or reaches bits 252..255).  Hence the low 32 bits of every lane equal the
    32-bit value the C source computes.  The schedule words, T1, T2 and the key are therefore NOT
    masked (their bounds stay < 2^36); E and A are masked with M7 (as in kprog) because later sums
    need them clean.

Run:  python3 -I swar7_k.py            (validation + counts + ledger; ~1-2 min)
      python3 -I swar7_k.py --quick    (fewer trials)
"""
import importlib.util
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MASK = 0xffffffff
W256 = (1 << 256) - 1

# ----------------------------------------------------------------------------------------------
# FIPS 180-4 reference (written here, independent of the package)
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]
IV = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]


def rotr(v, n): return ((v >> n) | (v << (32 - n))) & MASK
def bs0(v): return rotr(v, 2) ^ rotr(v, 13) ^ rotr(v, 22)
def bs1(v): return rotr(v, 6) ^ rotr(v, 11) ^ rotr(v, 25)
def sg0(v): return rotr(v, 7) ^ rotr(v, 18) ^ (v >> 3)
def sg1(v): return rotr(v, 17) ^ rotr(v, 19) ^ (v >> 10)
def ch(e, f, g): return ((e & f) ^ (~e & g)) & MASK
def maj(a, b, c): return (a & b) ^ (a & c) ^ (b & c)


def compress31(state, m):
    """FIPS 180-4 compression reduced to steps 0..30, with feed-forward."""
    w = list(m)
    for t in range(16, 31):
        w.append((sg1(w[t - 2]) + w[t - 7] + sg0(w[t - 15]) + w[t - 16]) & MASK)
    a, b, c, d, e, f, g, h = state
    for t in range(31):
        t1 = (h + bs1(e) + ch(e, f, g) + K[t] + w[t]) & MASK
        t2 = (bs0(a) + maj(a, b, c)) & MASK
        a, b, c, d, e, f, g, h = (t1 + t2) & MASK, a, b, c, (d + t1) & MASK, e, f, g
    return [(x + y) & MASK for x, y in zip(state, (a, b, c, d, e, f, g, h))]


def group_values(m):
    """Same set as kprog.group_values (words 0..14 only); cross-checked against it below."""
    a, b, c, d, e, f, g, h = IV
    for t in range(15):
        t1 = (h + bs1(e) + ch(e, f, g) + K[t] + m[t]) & MASK
        t2 = (bs0(a) + maj(a, b, c)) & MASK
        a, b, c, d, e, f, g, h = (t1 + t2) & MASK, a, b, c, (d + t1) & MASK, e, f, g
    m16 = (sg1(m[14]) + m[9] + sg0(m[1]) + m[0]) & MASK
    m18 = (sg1(m16) + m[11] + sg0(m[3]) + m[2]) & MASK
    m20 = (sg1(m18) + m[13] + sg0(m[5]) + m[4]) & MASK
    p15 = (h + bs1(e) + ch(e, f, g) + K[15]) & MASK
    q15 = (bs0(a) + maj(a, b, c)) & MASK
    return {
        "U15": (d + p15) & MASK, "V15": (p15 + q15) & MASK,
        "a": a, "b": b, "c": c, "e": e, "f": f, "ab": a & b,
        "P16": (g + K[16] + m16) & MASK, "P17": (f + K[17]) & MASK, "P18": (e + K[18] + m18) & MASK,
        "KW20": (K[20] + m20) & MASK,
        "c17": (m[10] + sg0(m[2]) + m[1]) & MASK, "c19": (m[12] + sg0(m[4]) + m[3]) & MASK,
        "c21": (m[14] + sg0(m[6]) + m[5]) & MASK, "c22": (sg1(m20) + sg0(m[7]) + m[6]) & MASK,
        "c23": (m16 + sg0(m[8]) + m[7]) & MASK, "c24": (sg0(m[9]) + m[8]) & MASK,
        "c25": (m18 + sg0(m[10]) + m[9]) & MASK, "c26": (sg0(m[11]) + m[10]) & MASK,
        "c27": (m20 + sg0(m[12]) + m[11]) & MASK, "c28": (sg0(m[13]) + m[12]) & MASK,
        "c29k": (sg0(m[14]) + m[13] + K[29]) & MASK, "c30k": (m[14] + K[30] + IV[0]) & MASK,
    }


GROUP_NAMES = list(group_values([0] * 15))
KNAMES = [f"K{t}" for t in (19, 21, 22, 23, 24, 25, 26, 27, 28)]
ROT_AMOUNTS = (2, 13, 22, 6, 11, 25, 7, 18, 17, 19)
SHR_AMOUNTS = (3, 10)


# ----------------------------------------------------------------------------------------------
class Layout:
    """Lane geometry.  mode 'w36x7': 7 lanes of 36 bits (guard bits); 'w32x8': 8 lanes of 32 bits
    (no guard bits, lane-isolated add ((x&L)+(y&L)) ^ ((x^y)&H))."""

    def __init__(self, mode):
        self.mode = mode
        self.lanes, self.width = {"w36x7": (7, 36), "w32x8": (8, 32)}[mode]
        self.lane_max = (1 << self.width) - 1

    def bcast(self, v):
        return sum((v & ((1 << self.width) - 1)) << (self.width * l) for l in range(self.lanes))

    def lanes_of(self, x):
        return [(x >> (self.width * l)) & self.lane_max for l in range(self.lanes)]

    def constants(self):
        c = {"M7": self.bcast(MASK)}
        for r in ROT_AMOUNTS:
            lo = (1 << (32 - r)) - 1
            c[f"LO{r}"] = self.bcast(lo)
            c[f"HI{r}"] = self.bcast(MASK ^ lo)
        for k in SHR_AMOUNTS:
            c[f"SHR{k}"] = self.bcast((1 << (32 - k)) - 1)
        c["L31"] = self.bcast(0x7fffffff)
        c["H31"] = self.bcast(0x80000000)
        c["M18"] = (1 << 18) - 1
        c["M20"] = (1 << 20) - 1
        c["INCV"] = self.bcast(self.lanes)
        c["CL"] = self.lanes                     # scalar lane count (7 or 8)
        c["LIMIT"] = 1 << 24
        for t in range(64):
            c[f"K{t}"] = self.bcast(K[t])
        return c


class Prog:
    """Straight-line SWAR program.  Each op: (section, op, dst, srcs, kind).  Static lane bound
    tracking: self.bnd[reg] = upper bound of every lane's value (as an integer < 2^width)."""

    def __init__(self, lay):
        self.lay = lay
        self.ops = []
        self.n = 0
        self.sec = "?"
        self.bnd = {"X": (1 << 25) - 1, "M7": MASK, "BM": 0, "C63": 63, "C1": 1}

    def emit(self, op, *src, kind="", bnd=None):
        self.n += 1
        d = f"v{self.n}"
        self.ops.append((self.sec, op, d, src, kind))
        if bnd is not None:
            self.bnd[d] = bnd
        return d

    # --- loads
    def ldg(self, name):                       # lane-broadcast group value / round constant
        return self.emit("ld", name, kind="group" if not name.startswith("K") else "kconst", bnd=MASK)

    def ldm(self, name):                       # lane mask / constant
        return self.emit("ld", name, kind="mask", bnd=self.lay.lane_max)

    # --- ALU
    def add(self, a, b):
        if self.lay.mode == "w36x7":
            s = self.bnd[a] + self.bnd[b]
            assert s <= self.lay.lane_max, ("lane overflow possible", self.sec, a, b, s)
            return self.emit("add", a, b, bnd=s)
        # w32x8: lane-isolated add, 6 ALU + 2 mask loads
        L, H = self.ldm("L31"), self.ldm("H31")
        s = self.emit("add", self.emit("and", a, L, bnd=0), self.emit("and", b, L, bnd=0), bnd=0)
        hb = self.emit("and", self.emit("xor", a, b, bnd=0), H, bnd=0)
        return self.emit("xor", s, hb, bnd=MASK)

    def _bits(self, b): return (1 << b.bit_length()) - 1
    def and_(self, a, b): return self.emit("and", a, b, bnd=min(self._bits(self.bnd[a]), self._bits(self.bnd[b])))
    def or_(self, a, b): return self.emit("or", a, b, bnd=max(self._bits(self.bnd[a]), self._bits(self.bnd[b])))
    def xor(self, a, b): return self.emit("xor", a, b, bnd=max(self._bits(self.bnd[a]), self._bits(self.bnd[b])))
    def not_(self, a): return self.emit("not", a, bnd=self.lay.lane_max)

    def mask(self, a):
        if self.lay.mode == "w32x8":
            return a                          # lanes are exactly 32 bits: nothing to reduce
        return self.emit("and", a, "M7", bnd=MASK)

    def rotr(self, v, r):
        lo = self.emit("and", self.emit("shr", v, r), self.ldm(f"LO{r}"), bnd=0)
        hi = self.emit("and", self.emit("shl", v, 32 - r), self.ldm(f"HI{r}"), bnd=0)
        return self.emit("or", lo, hi, bnd=MASK)

    def shr32(self, v, k):
        return self.emit("and", self.emit("shr", v, k), self.ldm(f"SHR{k}"), bnd=(1 << (32 - k)) - 1)

    def bs0(self, v): return self.xor(self.xor(self.rotr(v, 2), self.rotr(v, 13)), self.rotr(v, 22))
    def bs1(self, v): return self.xor(self.xor(self.rotr(v, 6), self.rotr(v, 11)), self.rotr(v, 25))
    def sg0(self, v): return self.xor(self.xor(self.rotr(v, 7), self.rotr(v, 18)), self.shr32(v, 3))
    def sg1(self, v): return self.xor(self.xor(self.rotr(v, 17), self.rotr(v, 19)), self.shr32(v, 10))

    def ch(self, e, f, g):
        return self.xor(self.and_(e, f), self.and_(self.not_(e), g))

    def maj(self, a, b, c):
        return self.xor(self.xor(self.and_(a, b), self.and_(a, c)), self.and_(b, c))


def gen_pass(mode, tail=False, refmask=False):
    """One pass: SWAR trial (steps 15..30 + 12 schedule words) -> per-lane bitmap tests -> loop
    control.  Structure follows kprog.gen_lane line by line; differences are only the lane
    primitives (masked rotations/shifts) and the dropped masks that the lane bounds make
    unnecessary (schedule words, key).  tail=True: final pass of a group (only lane 0 is a real
    trial) -- we nevertheless charge it as a full pass."""
    lay = Layout(mode)
    P = Prog(lay)
    x = "X"
    w = {}
    rm = (lambda v: P.mask(v)) if refmask else (lambda v: v)   # sensitivity: mask as kprog/ref

    def sched(t):
        P.sec = "schedule"
        if t == 17: w[17] = rm(P.add(P.sg1(x), P.ldg("c17")))
        elif t == 19: w[19] = rm(P.add(P.sg1(w[17]), P.ldg("c19")))
        elif t == 21: w[21] = rm(P.add(P.sg1(w[19]), P.ldg("c21")))
        elif t == 22: w[22] = rm(P.add(P.ldg("c22"), x))
        elif t == 23: w[23] = rm(P.add(P.sg1(w[21]), P.ldg("c23")))
        elif t == 24: w[24] = rm(P.add(P.add(P.sg1(w[22]), w[17]), P.ldg("c24")))
        elif t == 25: w[25] = rm(P.add(P.sg1(w[23]), P.ldg("c25")))
        elif t == 26: w[26] = rm(P.add(P.add(P.sg1(w[24]), w[19]), P.ldg("c26")))
        elif t == 27: w[27] = rm(P.add(P.sg1(w[25]), P.ldg("c27")))
        elif t == 28: w[28] = rm(P.add(P.add(P.sg1(w[26]), w[21]), P.ldg("c28")))
        elif t == 29: w[29] = rm(P.add(P.add(P.sg1(w[27]), w[22]), P.ldg("c29k")))
        elif t == 30: w[30] = rm(P.add(P.add(P.add(P.sg1(w[28]), w[23]), P.sg0(x)), P.ldg("c30k")))
        P.sec = "rounds"

    P.sec = "rounds"
    # round 15
    E = P.mask(P.add(P.ldg("U15"), x))
    A = P.mask(P.add(P.ldg("V15"), x))
    # round 16
    s1 = P.bs1(E)
    c = P.xor(P.and_(E, P.ldg("e")), P.and_(P.not_(E), P.ldg("f")))
    T1 = rm(P.add(P.add(P.ldg("P16"), s1), c))
    s0 = P.bs0(A)
    mj = P.xor(P.xor(P.and_(A, P.ldg("a")), P.and_(A, P.ldg("b"))), P.ldg("ab"))
    T2 = rm(P.add(s0, mj))
    E16, A16 = P.mask(P.add(P.ldg("c"), T1)), P.mask(P.add(T1, T2))
    # round 17
    sched(17)
    s1 = P.bs1(E16)
    c = P.xor(P.and_(E16, E), P.and_(P.not_(E16), P.ldg("e")))
    T1 = rm(P.add(P.add(P.add(P.ldg("P17"), s1), c), w[17]))
    s0 = P.bs0(A16)
    la = P.ldg("a")
    mj = P.xor(P.xor(P.and_(A16, A), P.and_(A16, la)), P.and_(A, la))
    T2 = rm(P.add(s0, mj))
    E17, A17 = P.mask(P.add(P.ldg("b"), T1)), P.mask(P.add(T1, T2))
    # round 18
    s1 = P.bs1(E17)
    c = P.ch(E17, E16, E)
    T1 = rm(P.add(P.add(P.ldg("P18"), s1), c))
    T2 = rm(P.add(P.bs0(A17), P.maj(A17, A16, A)))
    E18, A18 = P.mask(P.add(P.ldg("a"), T1)), P.mask(P.add(T1, T2))
    st = [A18, A17, A16, A, E18, E17, E16, E]
    key = None
    for t in range(19, 31):
        Aa, Bb, Cc, Dd, Ee, Ff, Gg, Hh = st
        if t != 20:
            sched(t)
        if t == 20: kw = P.ldg("KW20")
        elif t in (29, 30): kw = w[t]
        else: kw = P.add(P.ldg(f"K{t}"), w[t])
        T1 = rm(P.add(P.add(P.add(Hh, P.bs1(Ee)), P.ch(Ee, Ff, Gg)), kw))
        T2 = rm(P.add(P.bs0(Aa), P.maj(Aa, Bb, Cc)))
        if t == 30:
            key = rm(P.add(T1, T2))             # not masked: the lane extraction below masks
        else:
            st = [P.mask(P.add(T1, T2)), Aa, Bb, Cc, P.mask(P.add(Dd, T1)), Ee, Ff, Gg]

    # per-lane bitmap tests (scalar): key_l bits 8..31 = bitmap bit index
    P.sec = "bitmap"
    m18 = P.ldm("M18")                          # once per pass, register-resident for 7 tests
    hits = []
    nl = 1 if tail else lay.lanes
    for l in range(nl):
        t = P.emit("shr", key, lay.width * l + 8)
        wi = P.emit("and", P.emit("shr", t, 6), m18)
        addr = P.emit("add", "BM", wi)
        word = P.emit("ldx", addr)
        bit = P.emit("and", P.emit("shrv", word, P.emit("and", t, "C63")), "C1")
        h = P.emit("cmp", bit)
        P.emit("br", h, kind=f"lane{l}")
        hits.append(h)

    # loop control (cf. proof 16.2: 21 for a pass of 8)
    P.sec = "loop"
    P.emit("addX", "X", P.ldm("INCV"))                          # X += (L,L,..,L): 2
    P.emit("st", "CTR", P.emit("add", P.emit("ldc", "CTR"), P.ldm("CL")))   # trial counter: 4
    if not tail:
        # abort test after the pass containing k*2^20:  ((base+6) & 0xfffff) < 7   : 5
        a = P.emit("and", "B6", P.ldm("M20"))
        P.emit("br", P.emit("cmplt", a, P.ldm("CL")), kind="abort")
        # pass loop: B6 += L; continue while B6 < 2^24                             : 5
        P.emit("addB", "B6", P.ldm("CL"))
        P.emit("br", P.emit("cmplt", "B6", P.ldm("LIMIT")), kind="loop")
    P.key, P.hits = key, hits
    return P


def run(P, G, X, B6, bitmap, consts, check=True):
    """Counting interpreter on 256-bit words.  G: lane-broadcast group values.  Returns
    (key word, per-lane hit list, ops, branch outcomes, new X, new B6, ctr increment)."""
    lay = P.lay
    R = {"X": X, "M7": consts["M7"], "BM": 0, "C63": 63, "C1": 1, "B6": B6}
    mem = {"CTR": 0}
    ops = 0
    br = {}
    lmax = lay.lane_max
    for sec, o, d, s, kind in P.ops:
        ops += 1
        if o == "ld":
            nm = s[0]
            R[d] = G[nm] if nm in G else consts[nm]
        elif o == "ldc": R[d] = mem[s[0]]
        elif o == "st": mem[s[0]] = R[s[1]]
        elif o == "add": R[d] = (R[s[0]] + R[s[1]]) & W256
        elif o == "addX": R["X"] = (R["X"] + R[s[1]]) & W256
        elif o == "addB": R["B6"] = (R["B6"] + R[s[1]]) & W256
        elif o == "and": R[d] = R[s[0]] & R[s[1]]
        elif o == "or": R[d] = R[s[0]] | R[s[1]]
        elif o == "xor": R[d] = R[s[0]] ^ R[s[1]]
        elif o == "not": R[d] = W256 ^ R[s[0]]
        elif o == "shr": R[d] = R[s[0]] >> s[1]
        elif o == "shl": R[d] = (R[s[0]] << s[1]) & W256
        elif o == "shrv": R[d] = R[s[0]] >> R[s[1]]
        elif o == "ldx": R[d] = bitmap(R[s[0]])
        elif o == "cmp": R[d] = int(R[s[0]] != 0)
        elif o == "cmplt": R[d] = int(R[s[0]] < R[s[1]])
        elif o == "br": br[kind] = R[s[0]]
        else: raise ValueError(o)
        if check and lay.mode == "w36x7" and o in ("add", "and", "or", "xor") and sec in ("rounds", "schedule"):
            v = R[d]
            # dynamic soundness: value within the statically bounded lanes, nothing above bit 251
            assert v >> (lay.lanes * lay.width) == 0, (sec, o, d)
            if d in P.bnd and P.bnd[d]:
                for lv in lay.lanes_of(v):
                    assert lv <= P.bnd[d], (sec, o, d, lv, P.bnd[d])
    return R[P.key], [R[h] for h in P.hits], ops, br, R["X"], R["B6"], mem["CTR"]


def histogram(P, sections=None):
    h = {}
    for sec, o, *_ in P.ops:
        if sections and sec not in sections:
            continue
        o = {"addX": "add", "addB": "add", "ldc": "ld", "cmplt": "cmp", "shrv": "shr"}.get(o, o)
        h[o] = h.get(o, 0) + 1
    return h


def by_section(P):
    h = {}
    for sec, o, d, s, kind in P.ops:
        h[sec] = h.get(sec, 0) + 1
    return h


def mask_loads(P, sections=None):
    return sum(1 for sec, o, d, s, kind in P.ops
               if o == "ld" and kind == "mask" and (sections is None or sec in sections)
               and (s[0].startswith(("LO", "HI", "SHR", "L31", "H31"))))


def max_live(P):
    """Largest set of simultaneously live values (registers) in the straight-line pass, plus the
    long-lived registers X, B6 and the 4 fixed ones."""
    last = {}
    for i, (sec, o, d, s, kind) in enumerate(P.ops):
        for v in s:
            if isinstance(v, str) and v.startswith("v"):
                last[v] = i
    last[P.key] = max(last.get(P.key, 0), len(P.ops))
    live, peak = set(), 0
    for i, (sec, o, d, s, kind) in enumerate(P.ops):
        if d in last:
            live.add(d)
        peak = max(peak, len(live))
        for v in s:
            if isinstance(v, str) and last.get(v) == i:
                live.discard(v)
    return peak + 2 + 4


# ----------------------------------------------------------------------------------------------
def bcast_cost(lay):
    """Ops to build one lane-broadcast vector from a scalar group value already stored by the
    group set-up: load, shift/OR doubling, store."""
    if lay.mode == "w36x7":
        # v | v<<36 ; b1 | b1<<72 ; b2 | b1<<144 ; b3 | v<<216   (8 ALU) + load + store
        return 10
    # v | v<<32 ; | <<64 ; | <<128   (6 ALU) + load + store
    return 8


def bcast_emulate(lay, v):
    if lay.mode == "w36x7":
        b1 = v | (v << 36); b2 = b1 | (b1 << 72); b3 = b2 | (b1 << 144); b4 = b3 | (v << 216)
        return b4 & W256
    b1 = v | (v << 32); b2 = b1 | (b1 << 64); b3 = b2 | (b2 << 128)
    return b3 & W256


def load_ref_modules():
    """Organizer core (repo/verifier/hash_functions.py, sha256 514fa8ab...) and kprog.py (extracted
    verbatim from the proof, sha256 c0c4453a...), both optional."""
    hf = kp = None
    for p in (os.path.join(HERE, "..", "repo", "verifier", "hash_functions.py"),
              os.path.join(HERE, "ref_hash_functions.py")):
        if os.path.exists(p):
            spec = importlib.util.spec_from_file_location("ref_hash_functions", p)
            hf = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(hf)
            sys.modules["ref_hash_functions"] = hf
            break
    kpath = os.path.join(HERE, "kprog_extracted.py")
    if hf is not None and os.path.exists(kpath):
        spec = importlib.util.spec_from_file_location("kprog_extracted", kpath)
        kp = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(kp)
    return hf, kp


class Bitmap:
    """Pseudo-random 2^24-bit bitmap in 64-bit words (dense, so ~half the tests hit), with an
    optional set of forced bits.  Shared by the SWAR program and kprog's scalar program."""

    def __init__(self, seed):
        self.seed = seed
        self.forced = {}

    def __call__(self, addr):
        x = (addr * 0x9e3779b97f4a7c15 + self.seed) & ((1 << 64) - 1)
        x ^= x >> 31; x = (x * 0xbf58476d1ce4e5b9) & ((1 << 64) - 1); x ^= x >> 29
        return x | self.forced.get(addr, 0)

    def get(self, addr, default=0):           # kprog.run uses mem.get(addr, 0)
        return self(addr)


def validate(mode, n_groups, passes_per_group, seed, hf, kp, log, refmask=False):
    lay = Layout(mode)
    L = lay.lanes
    P = gen_pass(mode, refmask=refmask)
    PT = gen_pass(mode, tail=True, refmask=refmask) if (1 << 24) % L else None
    consts = lay.constants()
    kprog_P = kp.gen_lane(False) if kp else None
    rng = random.Random(seed)
    stats = dict(trials=0, passes=0, tail_passes=0, mism_key=0, mism_hit=0, mism_org=0, mism_kprog=0,
                 hits=0, forced=0, gv_mism=0, ops=set(), tail_ops=set(), aborts_ok=0, loop_ok=0)
    full_last = ((1 << 24) // L - 1) * L if (1 << 24) % L else (1 << 24) - L
    for gi in range(n_groups):
        m = [rng.getrandbits(32) for _ in range(15)]
        gv = group_values(m)
        kgv = kp.group_values(m) if kp else None
        if kp and any(kgv[nm] != gv[nm] for nm in GROUP_NAMES):
            stats["gv_mism"] += 1
        G = {nm: bcast_emulate(lay, v) for nm, v in gv.items()}
        for nm in G:
            assert G[nm] == lay.bcast(gv[nm])
        bm = Bitmap(rng.getrandbits(64))
        bases = [0, full_last, full_last - L, (1 << 20) - 3, (1 << 23) - 1]
        while len(bases) < passes_per_group:
            bases.append(rng.randrange(0, full_last + 1))
        bases = bases[:passes_per_group]
        if PT is not None:
            bases.append(full_last + L)          # tail pass: j = 2^24-1 (+6 non-trial lanes)
        for base in bases:
            tail = base + L > (1 << 24)
            prog = PT if tail else P
            X = sum((base + l) << (lay.width * l) for l in range(L))
            # force a hit on a random lane sometimes, to exercise both branch outcomes
            bm.forced = {}
            key_w, hits, ops, br, Xn, B6n, ctr = run(prog, G, X, base + L - 1, bm, consts)
            (stats["tail_ops"] if tail else stats["ops"]).add(ops)
            stats["tail_passes" if tail else "passes"] += 1
            assert ctr == L
            assert Xn == sum((base + L + l) << (lay.width * l) for l in range(L))
            if not tail:
                contains = any(((base + l) & 0xfffff) == 0 for l in range(L))
                stats["aborts_ok"] += int(br["abort"] == int(contains))
                nxt = base + L
                stats["loop_ok"] += int(br["loop"] == int(nxt + L - 1 < (1 << 24)))
            for l, h in enumerate(hits):
                j = base + l
                assert j < (1 << 24)
                lane_key = (key_w >> (lay.width * l)) & MASK
                ref = compress31(IV, m + [j])[0]
                stats["mism_key"] += int(lane_key != ref)
                if hf is not None:
                    blk = b"".join(v.to_bytes(4, "big") for v in m + [j])
                    stats["mism_org"] += int(hf._compress("sha256", tuple(IV), blk, 31)[0] != lane_key)
                bi = ref >> 8
                want = (bm(bi >> 6) >> (bi & 63)) & 1
                stats["mism_hit"] += int(h != want)
                stats["hits"] += h
                if kprog_P is not None:
                    kk, kh, kops = kp.run(kprog_P, kgv, j, bm)
                    stats["mism_kprog"] += int(kk != lane_key or kh != h or kops != 775)
                stats["trials"] += 1
            # forced-hit check on one lane: set its bit, decision must flip to 1 on that lane only
            l = rng.randrange(len(hits))
            lane_key = (key_w >> (lay.width * l)) & MASK
            bi = lane_key >> 8
            bm.forced = {bi >> 6: 1 << (bi & 63)}
            _, hits2, _, _, _, _, _ = run(prog, G, X, base + L - 1, bm, consts, check=False)
            stats["forced"] += 1
            stats["mism_hit"] += int(hits2[l] != 1)
            bm.forced = {}
    log(f"[{mode}] groups {n_groups}, full passes {stats['passes']}, tail passes {stats['tail_passes']}, "
        f"lane trials checked {stats['trials']}")
    log(f"[{mode}]   key vs own FIPS compress31: mismatches {stats['mism_key']}; vs organizer _compress: "
        f"{stats['mism_org'] if hf else 'n/a'}; vs kprog scalar trial (key, decision, 775 ops): "
        f"{stats['mism_kprog'] if kp else 'n/a'}; bitmap decisions: {stats['mism_hit']} "
        f"(hits {stats['hits']}, forced-hit checks {stats['forced']}); group values vs kprog: {stats['gv_mism']}")
    log(f"[{mode}]   ops per full pass observed {sorted(stats['ops'])}, tail {sorted(stats['tail_ops'])}; "
        f"abort-test decisions right {stats['aborts_ok']}/{stats['passes']}, loop decisions right "
        f"{stats['loop_ok']}/{stats['passes']}")
    bad = stats["mism_key"] + stats["mism_org"] + stats["mism_kprog"] + stats["mism_hit"] + stats["gv_mism"]
    bad += (stats["passes"] - stats["aborts_ok"]) + (stats["passes"] - stats["loop_ok"])
    assert len(stats["ops"]) == 1
    return stats, bad


def group_schedule_check(L):
    """Pass/abort schedule of one group, enumerated: passes, trials, abort-check firings."""
    passes = fires = trials = 0
    base = 0
    while base + L <= (1 << 24):            # full passes (loop exits when next B6 >= 2^24)
        passes += 1; trials += L
        if ((base + L - 1) & 0xfffff) < L:
            fires += 1
        base += L
    tail = 0
    if base < (1 << 24):
        tail = 1; trials += (1 << 24) - base
    return passes, tail, fires, trials


HIT_EXTRA = 3        # per bitmap hit: j = B6 - (L-1-l) for the hit lane (load constant, sub) + 1 spare


def ledger(P_ops, gextra, log, label, L=7, quiet=False):
    import math
    T_RUN = 99_492_036_640
    GROUPS, ABORTED = 5_932, 4
    HITS = 58_831_394
    G24 = 1 << 24
    K_OPS_OLD = 77_877_239_059_898
    PASS8_OLD = 12_436_504_580 * 6_221
    TOTAL_OLD = 84_509_728_547
    K_UNITS_OLD = 36_391_233_206
    full_groups = GROUPS - ABORTED
    rem = T_RUN - full_groups * G24
    assert rem == ABORTED * 8 + 35 * (1 << 20)
    if L == 8:
        passes = T_RUN // 8                        # = the run's own count, 12,436,504,580
        passes_tight = passes
    else:
        per_group = -(-G24 // L)                   # 2,396,746 passes incl. the tail pass
        passes = GROUPS * per_group                # every group (also the 4 aborted) charged in full
        passes_tight = full_groups * per_group + 5 * (1 << 20) + ABORTED  # sum floor(k*2^20/7)+1, sum k=35
    new_pass_ops = passes * P_ops
    k_ops = K_OPS_OLD - PASS8_OLD + new_pass_ops + GROUPS * gextra + HITS * HIT_EXTRA
    k_units = -(-k_ops // 2140)
    total = TOTAL_OLD - K_UNITS_OLD + k_units
    lg = math.log2(total)
    c2 = math.ceil(lg * 100) / 100
    c3 = math.ceil(lg * 1000) / 1000
    if not quiet:
        log(f"[{label}] run: {GROUPS} groups = {full_groups} complete + {ABORTED} aborted "
            f"(aborted groups' trials {rem - 0:,} = 4*8 + 35*2^20 beyond the complete ones)")
        log(f"[{label}] passes of {L} charged: {passes:,} (tight count, aborted groups stopping at "
            f"the same checkpoints: {passes_tight:,})")
        log(f"[{label}] pass ops {passes:,} x {P_ops} = {new_pass_ops:,}; per-group broadcast "
            f"{GROUPS} x {gextra} = {GROUPS * gextra:,}; hit lane index {HITS:,} x {HIT_EXTRA} = {HITS * HIT_EXTRA:,}")
        log(f"[{label}] K ops {K_OPS_OLD:,} - {PASS8_OLD:,} + {new_pass_ops:,} + {GROUPS * gextra:,} "
            f"+ {HITS * HIT_EXTRA:,} = {k_ops:,}")
        log(f"[{label}] K units ceil(/2140) = {k_units:,} (was {K_UNITS_OLD:,})")
        log(f"[{label}] total {TOTAL_OLD:,} - {K_UNITS_OLD:,} + {k_units:,} = {total:,} = 2^{lg:.6f}"
            f" -> smallest claim >= : {c2:.2f} / {c3:.3f}")
    return dict(passes=passes, k_ops=k_ops, k_units=k_units, total=total, log2=lg)


def main():
    quick = "--quick" in sys.argv
    out = []

    def log(s):
        print(s, flush=True)
        out.append(s)

    hf, kp = load_ref_modules()
    log(f"organizer core loaded: {hf is not None}; kprog (verbatim from proof C.6) loaded: {kp is not None}")
    if kp:
        assert len(kp.gen_lane(False).ops) == 775
    results = {}
    for mode in ("w36x7", "w32x8"):
        lay = Layout(mode)
        P = gen_pass(mode)
        n = len(P.ops)
        sec = by_section(P)
        log(f"[{mode}] ops per pass of {lay.lanes} trials: {n}  by section {sec}  "
            f"per trial {n / lay.lanes:.3f}")
        log(f"[{mode}]   primitive histogram {dict(sorted(histogram(P).items()))}")
        for s_ in ("rounds", "schedule", "bitmap", "loop"):
            log(f"[{mode}]     {s_:9s} {dict(sorted(histogram(P, (s_,)).items()))}")
        if mode == "w36x7":
            adds = [P.bnd[d] for sec_, o, d, s_, k in P.ops if o == "add" and sec_ in ("rounds", "schedule")]
            log(f"[{mode}]   static lane bounds: largest bound of any add result {max(adds):,} = "
                f"{max(adds) / (MASK):.2f} x (2^32-1) <= 2^36-1 = {(1 << 36) - 1:,} (asserted for all {len(adds)} adds)")
        ml = mask_loads(P)
        log(f"[{mode}]   of which rotation/shift/add lane-mask loads {ml}; with those masks "
            f"register-resident: {n - ml} ({(n - ml) / lay.lanes:.3f}/trial); max live values "
            f"(incl. X, B6 and 4 fixed regs) {max_live(P)}")
        if (1 << 24) % lay.lanes:
            PT = gen_pass(mode, tail=True)
            log(f"[{mode}]   tail pass (lane 0 only) {len(PT.ops)} ops; charged as a full pass")
        g_extra = (len(GROUP_NAMES) + len(KNAMES) + 22 + 4) * bcast_cost(lay) + 2
        log(f"[{mode}]   per-group broadcast: ({len(GROUP_NAMES)} group values + {len(KNAMES)} round "
            f"constants + 22 masks + 4 loop vectors) x {bcast_cost(lay)} + 2 (X, B6 init) = {g_extra}")
        results[mode] = (n, g_extra, lay.lanes, ml)
        ng, ppg = ((800, 8) if mode == "w36x7" else (120, 8)) if not quick else ((60, 6) if mode == "w36x7" else (15, 6))
        stats, bad = validate(mode, ng, ppg, 0x5eed31 + (mode == "w32x8"), hf, kp, log)
        log(f"[{mode}]   total mismatches/failures: {bad}")
        assert bad == 0
    p, t, f, tr = group_schedule_check(7)
    log(f"[w36x7] one full group enumerated: {p:,} full passes + {t} tail pass, {f} abort-check firings, "
        f"{tr:,} trials")
    assert (p, t, f, tr) == (2396745, 1, 16, 1 << 24)
    n7, g7, _, ml7 = results["w36x7"]
    n8, g8, _, ml8 = results["w32x8"]
    log(f"per trial: w36x7 {n7 / 7:.3f}, w32x8 {n8 / 8:.3f}, scalar (kprog) {6221 / 8:.3f}")
    log("== main ledger (w36x7) ==")
    r = ledger(n7, g7, log, "w36x7")
    log("== comparison: 8-lane 32-bit variant ==")
    ledger(n8, g8, log, "w32x8", L=8)
    log("== sensitivities (w36x7) ==")
    s1 = ledger(n7 - ml7, g7, log, "", quiet=True)
    log(f"masks register-resident ({n7 - ml7}/pass): total {s1['total']:,} = 2^{s1['log2']:.6f}")
    Pr = gen_pass("w36x7", refmask=True)
    stats, bad = validate("w36x7", 40 if not quick else 5, 4, 77, hf, kp, lambda s_: None, refmask=True)
    assert bad == 0 and stats["ops"] == {len(Pr.ops)}
    s2 = ledger(len(Pr.ops), g7, log, "", quiet=True)
    log(f"every T1, T2, schedule word and key masked as kprog/ref ({len(Pr.ops)}/pass): total "
        f"{s2['total']:,} = 2^{s2['log2']:.6f}")
    for extra in (100, 300):
        s3 = ledger(n7 + extra, g7, log, "", quiet=True)
        log(f"+{extra} ops per pass ({n7 + extra}): 2^{s3['log2']:.6f}")
    s4 = ledger(2 * n7, g7, log, "", quiet=True)
    log(f"twice the pass cost ({2 * n7}): 2^{s4['log2']:.6f}")
    import math
    for target in (math.ceil(r['log2'] * 100) / 100, 36.0, 36.30):
        lo_, hi_ = n7, 100000
        while lo_ < hi_:
            mid = (lo_ + hi_ + 1) // 2
            if ledger(mid, g7, log, "", quiet=True)["log2"] <= target: lo_ = mid
            else: hi_ = mid - 1
        log(f"break-even: total stays <= 2^{target:.2f} up to {lo_} ops per 7-trial pass ({lo_ / 7:.1f}/trial)")
    with open(os.path.join(HERE, "swar7_k_output.txt"), "w") as fh:
        fh.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
```

Output of the full run:

```text
organizer core loaded: True; kprog (verbatim from proof C.6) loaded: True
[w36x7] ops per pass of 7 trials: 1322  by section {'rounds': 977, 'schedule': 258, 'bitmap': 71, 'loop': 16}  per trial 188.857
[w36x7]   primitive histogram {'add': 126, 'and': 366, 'br': 9, 'cmp': 9, 'ld': 285, 'ldx': 7, 'not': 15, 'or': 114, 'shl': 114, 'shr': 147, 'st': 1, 'xor': 129}
[w36x7]     rounds    {'add': 98, 'and': 284, 'ld': 205, 'not': 15, 'or': 90, 'shl': 90, 'shr': 90, 'xor': 105}
[w36x7]     schedule  {'add': 18, 'and': 60, 'ld': 72, 'or': 24, 'shl': 24, 'shr': 36, 'xor': 24}
[w36x7]     bitmap    {'add': 7, 'and': 21, 'br': 7, 'cmp': 7, 'ld': 1, 'ldx': 7, 'shr': 21}
[w36x7]     loop      {'add': 3, 'and': 1, 'br': 2, 'cmp': 2, 'ld': 7, 'st': 1}
[w36x7]   static lane bounds: largest bound of any add result 42,949,672,950 = 10.00 x (2^32-1) <= 2^36-1 = 68,719,476,735 (asserted for all 116 adds)
[w36x7]   of which rotation/shift/add lane-mask loads 240; with those masks register-resident: 1082 (154.571/trial); max live values (incl. X, B6 and 4 fixed regs) 26
[w36x7]   tail pass (lane 0 only) 1252 ops; charged as a full pass
[w36x7]   per-group broadcast: (24 group values + 9 round constants + 22 masks + 4 loop vectors) x 10 + 2 (X, B6 init) = 592
[w36x7] groups 800, full passes 6400, tail passes 800, lane trials checked 45600
[w36x7]   key vs own FIPS compress31: mismatches 0; vs organizer _compress: 0; vs kprog scalar trial (key, decision, 775 ops): 0; bitmap decisions: 0 (hits 22779, forced-hit checks 7200); group values vs kprog: 0
[w36x7]   ops per full pass observed [1322], tail [1252]; abort-test decisions right 6400/6400, loop decisions right 6400/6400
[w36x7]   total mismatches/failures: 0
[w32x8] ops per pass of 8 trials: 2114  by section {'rounds': 1633, 'schedule': 384, 'bitmap': 81, 'loop': 16}  per trial 264.250
[w32x8]   primitive histogram {'add': 127, 'and': 687, 'br': 10, 'cmp': 10, 'ld': 517, 'ldx': 8, 'not': 15, 'or': 114, 'shl': 114, 'shr': 150, 'st': 1, 'xor': 361}
[w32x8]     rounds    {'add': 98, 'and': 548, 'ld': 401, 'not': 15, 'or': 90, 'shl': 90, 'shr': 90, 'xor': 301}
[w32x8]     schedule  {'add': 18, 'and': 114, 'ld': 108, 'or': 24, 'shl': 24, 'shr': 36, 'xor': 60}
[w32x8]     bitmap    {'add': 8, 'and': 24, 'br': 8, 'cmp': 8, 'ld': 1, 'ldx': 8, 'shr': 24}
[w32x8]     loop      {'add': 3, 'and': 1, 'br': 2, 'cmp': 2, 'ld': 7, 'st': 1}
[w32x8]   of which rotation/shift/add lane-mask loads 472; with those masks register-resident: 1642 (205.250/trial); max live values (incl. X, B6 and 4 fixed regs) 26
[w32x8]   per-group broadcast: (24 group values + 9 round constants + 22 masks + 4 loop vectors) x 8 + 2 (X, B6 init) = 474
[w32x8] groups 120, full passes 960, tail passes 0, lane trials checked 7680
[w32x8]   key vs own FIPS compress31: mismatches 0; vs organizer _compress: 0; vs kprog scalar trial (key, decision, 775 ops): 0; bitmap decisions: 0 (hits 3843, forced-hit checks 960); group values vs kprog: 0
[w32x8]   ops per full pass observed [2114], tail []; abort-test decisions right 960/960, loop decisions right 960/960
[w32x8]   total mismatches/failures: 0
[w36x7] one full group enumerated: 2,396,745 full passes + 1 tail pass, 16 abort-check firings, 16,777,216 trials
per trial: w36x7 188.857, w32x8 264.250, scalar (kprog) 777.625
== main ledger (w36x7) ==
[w36x7] run: 5932 groups = 5928 complete + 4 aborted (aborted groups' trials 36,700,192 = 4*8 + 35*2^20 beyond the complete ones)
[w36x7] passes of 7 charged: 14,217,497,272 (tight count, aborted groups stopping at the same checkpoints: 14,213,153,172)
[w36x7] pass ops 14,217,497,272 x 1322 = 18,795,531,393,584; per-group broadcast 5932 x 592 = 3,511,744; hit lane index 58,831,394 x 3 = 176,494,182
[w36x7] K ops 77,877,239,059,898 - 77,367,494,992,180 + 18,795,531,393,584 + 3,511,744 + 176,494,182 = 19,305,455,467,228
[w36x7] K units ceil(/2140) = 9,021,240,873 (was 36,391,233,206)
[w36x7] total 84,509,728,547 - 36,391,233,206 + 9,021,240,873 = 57,139,736,214 = 2^35.733775 -> smallest claim >= : 35.74 / 35.734
== comparison: 8-lane 32-bit variant ==
[w32x8] run: 5932 groups = 5928 complete + 4 aborted (aborted groups' trials 36,700,192 = 4*8 + 35*2^20 beyond the complete ones)
[w32x8] passes of 8 charged: 12,436,504,580 (tight count, aborted groups stopping at the same checkpoints: 12,436,504,580)
[w32x8] pass ops 12,436,504,580 x 2114 = 26,290,770,682,120; per-group broadcast 5932 x 474 = 2,811,768; hit lane index 58,831,394 x 3 = 176,494,182
[w32x8] K ops 77,877,239,059,898 - 77,367,494,992,180 + 26,290,770,682,120 + 2,811,768 + 176,494,182 = 26,800,694,055,788
[w32x8] K units ceil(/2140) = 12,523,688,812 (was 36,391,233,206)
[w32x8] total 84,509,728,547 - 36,391,233,206 + 12,523,688,812 = 60,642,184,153 = 2^35.819603 -> smallest claim >= : 35.82 / 35.820
== sensitivities (w36x7) ==
masks register-resident (1082/pass): total 55,545,250,539 = 2^35.692945
every T1, T2, schedule word and key masked as kprog/ref (1365/pass): total 57,425,414,898 = 2^35.740970
+100 ops per pass (1422): 2^35.750453
+300 ops per pass (1622): 2^35.783241
twice the pass cost (2644): 2^35.940056
break-even: total stays <= 2^35.74 up to 1359 ops per 7-trial pass (194.1/trial)
break-even: total stays <= 2^36.00 up to 3064 ops per 7-trial pass (437.7/trial)
break-even: total stays <= 2^36.30 up to 5455 ops per 7-trial pass (779.3/trial)
```

## Appendix D2. `swar7_k_v2.py` and its output

sha256 29bc6cc88d676d756ddcd29dbc9e09560df15ab2fd5593c591df76e79b1cb745  swar7_k_v2.py

Run as `python3 -I swar7_k_v2.py` next to `kprog_extracted.py` and the organizer's `verifier/hash_functions.py`.

```python
"""Search K of jungjipdo's sha256-r31 package (f99530e8), rewritten as a SWAR word-RAM program.

One pass = 7 consecutive trials j..j+6 of the SAME group (lanes differ only in message word 15).
Every 32-bit value lives in a 36-bit lane of a 256-bit word (lane l = bits 36l..36l+35, 7*36 = 252;
bits 252..255 unused).  Group values (anything that depends only on words 0..14) are lane-broadcast
once per group and loaded from memory, one counted load per use, exactly where kprog.py (proof
Appendix C.6) loads the scalar group value.

Primitives (collision-frontier-v5), 1 each: 256-bit load/store, add/sub mod 2^256, AND/OR/XOR/NOT,
whole-word shift, comparison, conditional branch.  Conventions copied from proof Section 16.1:
  * ALU operands are registers; the only immediates are shift counts.  Every other operand is a
    counted load (group values, round constants, lane masks, loop constants, bitmap words).
  * Four registers are fixed for the whole run: M7 (2^32-1 in every lane; replaces kprog's M),
    BM (bitmap base), C63, C1.  Everything else -- including all 22 rotation/shift lane masks --
    is loaded at EVERY use (conservative; a register-resident variant is reported as sensitivity).
  * Fixed-count loops are straight line; data-dependent loops pay counter, comparison, branch.

Lane soundness (checked statically for every op and dynamically on every executed op):
  * A per-lane rotation is ((v >> r) & LO_r) | ((v << (32-r)) & HI_r): 5 ALU ops.  The masks take
    lane bits r..31 and 0..r-1 of the SAME lane only, so it is exact whenever the low 32 bits of
    each lane are right, whatever the 4 guard bits hold.  sigma's plain shift is (v >> k) & SHR_k.
  * Every add requires (static upper bound of lane a) + (bound of lane b) <= 2^36-1, so no carry
    ever leaves a lane (or reaches bits 252..255).  Hence the low 32 bits of every lane equal the
    32-bit value the C source computes.  The schedule words, T1, T2 and the key are therefore NOT
    masked (their bounds stay < 2^36); E and A are masked with M7 (as in kprog) because later sums
    need them clean.

Run:  python3 -I swar7_k_v2.py            (validation + counts + ledger; ~1-2 min)
      python3 -I swar7_k.py --quick    (fewer trials)
"""
import importlib.util
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MASK = 0xffffffff
W256 = (1 << 256) - 1

# ----------------------------------------------------------------------------------------------
# FIPS 180-4 reference (written here, independent of the package)
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]
IV = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]


def rotr(v, n): return ((v >> n) | (v << (32 - n))) & MASK
def bs0(v): return rotr(v, 2) ^ rotr(v, 13) ^ rotr(v, 22)
def bs1(v): return rotr(v, 6) ^ rotr(v, 11) ^ rotr(v, 25)
def sg0(v): return rotr(v, 7) ^ rotr(v, 18) ^ (v >> 3)
def sg1(v): return rotr(v, 17) ^ rotr(v, 19) ^ (v >> 10)
def ch(e, f, g): return ((e & f) ^ (~e & g)) & MASK
def maj(a, b, c): return (a & b) ^ (a & c) ^ (b & c)


def compress31(state, m):
    """FIPS 180-4 compression reduced to steps 0..30, with feed-forward."""
    w = list(m)
    for t in range(16, 31):
        w.append((sg1(w[t - 2]) + w[t - 7] + sg0(w[t - 15]) + w[t - 16]) & MASK)
    a, b, c, d, e, f, g, h = state
    for t in range(31):
        t1 = (h + bs1(e) + ch(e, f, g) + K[t] + w[t]) & MASK
        t2 = (bs0(a) + maj(a, b, c)) & MASK
        a, b, c, d, e, f, g, h = (t1 + t2) & MASK, a, b, c, (d + t1) & MASK, e, f, g
    return [(x + y) & MASK for x, y in zip(state, (a, b, c, d, e, f, g, h))]


def group_values(m):
    """Same set as kprog.group_values (words 0..14 only); cross-checked against it below."""
    a, b, c, d, e, f, g, h = IV
    for t in range(15):
        t1 = (h + bs1(e) + ch(e, f, g) + K[t] + m[t]) & MASK
        t2 = (bs0(a) + maj(a, b, c)) & MASK
        a, b, c, d, e, f, g, h = (t1 + t2) & MASK, a, b, c, (d + t1) & MASK, e, f, g
    m16 = (sg1(m[14]) + m[9] + sg0(m[1]) + m[0]) & MASK
    m18 = (sg1(m16) + m[11] + sg0(m[3]) + m[2]) & MASK
    m20 = (sg1(m18) + m[13] + sg0(m[5]) + m[4]) & MASK
    p15 = (h + bs1(e) + ch(e, f, g) + K[15]) & MASK
    q15 = (bs0(a) + maj(a, b, c)) & MASK
    return {
        "U15": (d + p15) & MASK, "V15": (p15 + q15) & MASK,
        "a": a, "b": b, "c": c, "e": e, "f": f, "ab": a & b,
        "P16": (g + K[16] + m16) & MASK, "P17": (f + K[17]) & MASK, "P18": (e + K[18] + m18) & MASK,
        "KW20": (K[20] + m20) & MASK,
        "c17": (m[10] + sg0(m[2]) + m[1]) & MASK, "c19": (m[12] + sg0(m[4]) + m[3]) & MASK,
        "c21": (m[14] + sg0(m[6]) + m[5]) & MASK, "c22": (sg1(m20) + sg0(m[7]) + m[6]) & MASK,
        "c23": (m16 + sg0(m[8]) + m[7]) & MASK, "c24": (sg0(m[9]) + m[8]) & MASK,
        "c25": (m18 + sg0(m[10]) + m[9]) & MASK, "c26": (sg0(m[11]) + m[10]) & MASK,
        "c27": (m20 + sg0(m[12]) + m[11]) & MASK, "c28": (sg0(m[13]) + m[12]) & MASK,
        "c29k": (sg0(m[14]) + m[13] + K[29]) & MASK, "c30k": (m[14] + K[30] + IV[0]) & MASK,
    }


GROUP_NAMES = list(group_values([0] * 15))
KNAMES = [f"K{t}" for t in (19, 21, 22, 23, 24, 25, 26, 27, 28)]
ROT_AMOUNTS = (2, 13, 22, 6, 11, 25, 7, 18, 17, 19)
SHR_AMOUNTS = (3, 10)


# ----------------------------------------------------------------------------------------------
class Layout:
    """Lane geometry.  mode 'w36x7': 7 lanes of 36 bits (guard bits); 'w32x8': 8 lanes of 32 bits
    (no guard bits, lane-isolated add ((x&L)+(y&L)) ^ ((x^y)&H))."""

    def __init__(self, mode):
        self.mode = mode
        self.lanes, self.width = {"w36x7": (7, 36), "w32x8": (8, 32)}[mode]
        self.lane_max = (1 << self.width) - 1

    def bcast(self, v):
        return sum((v & ((1 << self.width) - 1)) << (self.width * l) for l in range(self.lanes))

    def lanes_of(self, x):
        return [(x >> (self.width * l)) & self.lane_max for l in range(self.lanes)]

    def constants(self):
        c = {"M7": self.bcast(MASK)}
        for r in ROT_AMOUNTS:
            lo = (1 << (32 - r)) - 1
            c[f"LO{r}"] = self.bcast(lo)
            c[f"HI{r}"] = self.bcast(MASK ^ lo)
        for k in SHR_AMOUNTS:
            c[f"SHR{k}"] = self.bcast((1 << (32 - k)) - 1)
        c["L31"] = self.bcast(0x7fffffff)
        c["H31"] = self.bcast(0x80000000)
        c["M18"] = (1 << 18) - 1
        c["M20"] = (1 << 20) - 1
        c["INCV"] = self.bcast(self.lanes)
        c["CL"] = self.lanes                     # scalar lane count (7 or 8)
        c["LIMIT"] = 1 << 24
        for t in range(64):
            c[f"K{t}"] = self.bcast(K[t])
        return c


class Prog:
    """Straight-line SWAR program.  Each op: (section, op, dst, srcs, kind).  Static lane bound
    tracking: self.bnd[reg] = upper bound of every lane's value (as an integer < 2^width)."""

    def __init__(self, lay):
        self.lay = lay
        self.ops = []
        self.n = 0
        self.sec = "?"
        self.bnd = {"X": (1 << 25) - 1, "M7": MASK, "BM": 0, "C63": 63, "C1": 1}
        self.res = {}            # mask name -> register currently holding it (no load needed)
        self.glob = []           # masks resident for the whole run (loaded once per group)
        self.membnd = {}         # bound of values stored to scratch memory

    def emit(self, op, *src, kind="", bnd=None):
        self.n += 1
        d = f"v{self.n}"
        self.ops.append((self.sec, op, d, src, kind))
        if bnd is not None:
            self.bnd[d] = bnd
        return d

    # --- loads
    def ldg(self, name):                       # lane-broadcast group value / round constant
        if name in self.res:
            return self.res[name]
        return self.emit("ld", name, kind="group" if not name.startswith("K") else "kconst", bnd=MASK)

    def ldm(self, name):                       # lane mask / constant
        if name in self.res:
            return self.res[name]
        return self.emit("ld", name, kind="mask", bnd=self.lay.lane_max)

    def make_global(self, names):
        for nm in names:
            self.glob.append(nm)
            self.res[nm] = "R:" + nm
            self.bnd["R:" + nm] = MASK if not nm.startswith(("LO", "HI", "SHR")) else self.lay.lane_max

    def region_load(self, names):
        """Load masks once at a region start; they stay in registers until their last use."""
        for nm in names:
            if nm not in self.res:
                self.res[nm] = self.emit("ld", nm, kind="mask" if nm.startswith(("LO", "HI", "SHR")) else "group",
                                         bnd=self.lay.lane_max if nm.startswith(("LO", "HI", "SHR")) else MASK)

    def region_end(self, names):
        for nm in names:
            if nm in self.res and not self.res[nm].startswith("R:"):
                del self.res[nm]

    def spill(self, name, v):
        self.membnd[name] = self.bnd[v]
        self.emit("st", name, v)

    def reload(self, name):
        return self.emit("ldc", name, bnd=self.membnd[name])

    # --- ALU
    def add(self, a, b):
        if self.lay.mode == "w36x7":
            s = self.bnd[a] + self.bnd[b]
            assert s <= self.lay.lane_max, ("lane overflow possible", self.sec, a, b, s)
            return self.emit("add", a, b, bnd=s)
        # w32x8: lane-isolated add, 6 ALU + 2 mask loads
        L, H = self.ldm("L31"), self.ldm("H31")
        s = self.emit("add", self.emit("and", a, L, bnd=0), self.emit("and", b, L, bnd=0), bnd=0)
        hb = self.emit("and", self.emit("xor", a, b, bnd=0), H, bnd=0)
        return self.emit("xor", s, hb, bnd=MASK)

    def _bits(self, b): return (1 << b.bit_length()) - 1
    def and_(self, a, b): return self.emit("and", a, b, bnd=min(self._bits(self.bnd[a]), self._bits(self.bnd[b])))
    def or_(self, a, b): return self.emit("or", a, b, bnd=max(self._bits(self.bnd[a]), self._bits(self.bnd[b])))
    def xor(self, a, b): return self.emit("xor", a, b, bnd=max(self._bits(self.bnd[a]), self._bits(self.bnd[b])))
    def not_(self, a): return self.emit("not", a, bnd=self.lay.lane_max)

    def mask(self, a):
        if self.lay.mode == "w32x8":
            return a                          # lanes are exactly 32 bits: nothing to reduce
        return self.emit("and", a, "M7", bnd=MASK)

    def rotr(self, v, r):
        lo = self.emit("and", self.emit("shr", v, r), self.ldm(f"LO{r}"), bnd=0)
        hi = self.emit("and", self.emit("shl", v, 32 - r), self.ldm(f"HI{r}"), bnd=0)
        return self.emit("or", lo, hi, bnd=MASK)

    def shr32(self, v, k):
        return self.emit("and", self.emit("shr", v, k), self.ldm(f"SHR{k}"), bnd=(1 << (32 - k)) - 1)

    def bs0(self, v): return self.xor(self.xor(self.rotr(v, 2), self.rotr(v, 13)), self.rotr(v, 22))
    def bs1(self, v): return self.xor(self.xor(self.rotr(v, 6), self.rotr(v, 11)), self.rotr(v, 25))
    def sg0(self, v): return self.xor(self.xor(self.rotr(v, 7), self.rotr(v, 18)), self.shr32(v, 3))
    def sg1(self, v): return self.xor(self.xor(self.rotr(v, 17), self.rotr(v, 19)), self.shr32(v, 10))

    def ch(self, e, f, g):
        return self.xor(self.and_(e, f), self.and_(self.not_(e), g))

    def maj(self, a, b, c):
        return self.xor(self.xor(self.and_(a, b), self.and_(a, c)), self.and_(b, c))


CFG = dict(glob=[], sched_first=False, res_sched=[], res_round=[], t2_first=False,
           sched_order=(17, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30))


def gen_pass(mode, tail=False, refmask=False, cfg=None):
    """One pass: SWAR trial (steps 15..30 + 12 schedule words) -> per-lane bitmap tests -> loop
    control.  Structure follows kprog.gen_lane line by line; differences are only the lane
    primitives (masked rotations/shifts) and the dropped masks that the lane bounds make
    unnecessary (schedule words, key).  tail=True: final pass of a group (only lane 0 is a real
    trial) -- we nevertheless charge it as a full pass."""
    lay = Layout(mode)
    P = Prog(lay)
    x = "X"
    w = {}
    rm = (lambda v: P.mask(v)) if refmask else (lambda v: v)   # sensitivity: mask as kprog/ref
    cfg = dict(CFG, **(cfg or {}))
    P.cfg = cfg
    P.make_global(cfg["glob"])
    SF = cfg["sched_first"]
    kwv = {}

    def sched(t, force=False):
        if SF and not force:
            return
        P.sec = "schedule"
        if t == 17: w[17] = rm(P.add(P.sg1(x), P.ldg("c17")))
        elif t == 19: w[19] = rm(P.add(P.sg1(w[17]), P.ldg("c19")))
        elif t == 21: w[21] = rm(P.add(P.sg1(w[19]), P.ldg("c21")))
        elif t == 22: w[22] = rm(P.add(P.ldg("c22"), x))
        elif t == 23: w[23] = rm(P.add(P.sg1(w[21]), P.ldg("c23")))
        elif t == 24: w[24] = rm(P.add(P.add(P.sg1(w[22]), w[17]), P.ldg("c24")))
        elif t == 25: w[25] = rm(P.add(P.sg1(w[23]), P.ldg("c25")))
        elif t == 26: w[26] = rm(P.add(P.add(P.sg1(w[24]), w[19]), P.ldg("c26")))
        elif t == 27: w[27] = rm(P.add(P.sg1(w[25]), P.ldg("c27")))
        elif t == 28: w[28] = rm(P.add(P.add(P.sg1(w[26]), w[21]), P.ldg("c28")))
        elif t == 29: w[29] = rm(P.add(P.add(P.sg1(w[27]), w[22]), P.ldg("c29k")))
        elif t == 30: w[30] = rm(P.add(P.add(P.add(P.sg1(w[28]), w[23]), P.sg0(x)), P.ldg("c30k")))
        P.sec = "rounds"

    if SF:
        # phase 1: all 12 schedule words first; the round addends are spilled to scratch memory
        P.sec = "schedule"
        P.region_load(cfg["res_sched"])
        for t in cfg["sched_order"]:
            sched(t, force=True)
            P.sec = "schedule"
            if t in (17, 29, 30): a_ = w[t]
            else: a_ = P.add(P.ldg(f"K{t}"), w[t])
            P.spill(f"S{t}", a_)
        P.region_end(cfg["res_sched"])
        w.clear()
    P.sec = "rounds"
    P.region_load(cfg["res_round"])
    # round 15
    E = P.mask(P.add(P.ldg("U15"), x))
    A = P.mask(P.add(P.ldg("V15"), x))
    # round 16
    s1 = P.bs1(E)
    c = P.xor(P.and_(E, P.ldg("e")), P.and_(P.not_(E), P.ldg("f")))
    T1 = rm(P.add(P.add(P.ldg("P16"), s1), c))
    s0 = P.bs0(A)
    mj = P.xor(P.xor(P.and_(A, P.ldg("a")), P.and_(A, P.ldg("b"))), P.ldg("ab"))
    T2 = rm(P.add(s0, mj))
    E16, A16 = P.mask(P.add(P.ldg("c"), T1)), P.mask(P.add(T1, T2))
    # round 17
    sched(17)
    s1 = P.bs1(E16)
    c = P.xor(P.and_(E16, E), P.and_(P.not_(E16), P.ldg("e")))
    T1 = rm(P.add(P.add(P.add(P.ldg("P17"), s1), c), P.reload("S17") if SF else w[17]))
    s0 = P.bs0(A16)
    la = P.ldg("a")
    mj = P.xor(P.xor(P.and_(A16, A), P.and_(A16, la)), P.and_(A, la))
    T2 = rm(P.add(s0, mj))
    E17, A17 = P.mask(P.add(P.ldg("b"), T1)), P.mask(P.add(T1, T2))
    # round 18
    s1 = P.bs1(E17)
    c = P.ch(E17, E16, E)
    T1 = rm(P.add(P.add(P.ldg("P18"), s1), c))
    T2 = rm(P.add(P.bs0(A17), P.maj(A17, A16, A)))
    E18, A18 = P.mask(P.add(P.ldg("a"), T1)), P.mask(P.add(T1, T2))
    st = [A18, A17, A16, A, E18, E17, E16, E]
    key = None
    for t in range(19, 31):
        Aa, Bb, Cc, Dd, Ee, Ff, Gg, Hh = st
        if t != 20:
            sched(t)
        if cfg["t2_first"]:
            T2 = rm(P.add(P.bs0(Aa), P.maj(Aa, Bb, Cc)))
        if t == 20: kw = P.ldg("KW20")
        elif SF: kw = P.reload(f"S{t}")
        elif t in (29, 30): kw = w[t]
        else: kw = P.add(P.ldg(f"K{t}"), w[t])
        T1 = rm(P.add(P.add(P.add(Hh, P.bs1(Ee)), P.ch(Ee, Ff, Gg)), kw))
        if not cfg["t2_first"]:
            T2 = rm(P.add(P.bs0(Aa), P.maj(Aa, Bb, Cc)))
        if t == 30:
            key = rm(P.add(T1, T2))             # not masked: the lane extraction below masks
        else:
            st = [P.mask(P.add(T1, T2)), Aa, Bb, Cc, P.mask(P.add(Dd, T1)), Ee, Ff, Gg]

    P.region_end(cfg["res_round"])
    # per-lane bitmap tests (scalar): key_l bits 8..31 = bitmap bit index
    P.sec = "bitmap"
    m18 = P.ldm("M18")                          # once per pass, register-resident for 7 tests
    hits = []
    nl = 1 if tail else lay.lanes
    for l in range(nl):
        t = P.emit("shr", key, lay.width * l + 8)
        wi = P.emit("and", P.emit("shr", t, 6), m18)
        addr = P.emit("add", "BM", wi)
        word = P.emit("ldx", addr)
        bit = P.emit("and", P.emit("shrv", word, P.emit("and", t, "C63")), "C1")
        h = P.emit("cmp", bit)
        P.emit("br", h, kind=f"lane{l}")
        hits.append(h)

    # loop control (cf. proof 16.2: 21 for a pass of 8)
    P.sec = "loop"
    P.emit("addX", "X", P.ldm("INCV"))                          # X += (L,L,..,L): 2
    P.emit("st", "CTR", P.emit("add", P.emit("ldc", "CTR"), P.ldm("CL")))   # trial counter: 4
    if not tail:
        # abort test after the pass containing k*2^20:  ((base+6) & 0xfffff) < 7   : 5
        a = P.emit("and", "B6", P.ldm("M20"))
        P.emit("br", P.emit("cmplt", a, P.ldm("CL")), kind="abort")
        # pass loop: B6 += L; continue while B6 < 2^24                             : 5
        P.emit("addB", "B6", P.ldm("CL"))
        P.emit("br", P.emit("cmplt", "B6", P.ldm("LIMIT")), kind="loop")
    P.key, P.hits = key, hits
    return P


def run(P, G, X, B6, bitmap, consts, check=True):
    """Counting interpreter on 256-bit words.  G: lane-broadcast group values.  Returns
    (key word, per-lane hit list, ops, branch outcomes, new X, new B6, ctr increment)."""
    lay = P.lay
    R = {"X": X, "M7": consts["M7"], "BM": 0, "C63": 63, "C1": 1, "B6": B6}
    for nm in P.glob:
        R["R:" + nm] = G[nm] if nm in G else consts[nm]
    mem = {"CTR": 0}
    ops = 0
    br = {}
    lmax = lay.lane_max
    for sec, o, d, s, kind in P.ops:
        ops += 1
        if o == "ld":
            nm = s[0]
            R[d] = G[nm] if nm in G else consts[nm]
        elif o == "ldc": R[d] = mem[s[0]]
        elif o == "st": mem[s[0]] = R[s[1]]
        elif o == "add": R[d] = (R[s[0]] + R[s[1]]) & W256
        elif o == "addX": R["X"] = (R["X"] + R[s[1]]) & W256
        elif o == "addB": R["B6"] = (R["B6"] + R[s[1]]) & W256
        elif o == "and": R[d] = R[s[0]] & R[s[1]]
        elif o == "or": R[d] = R[s[0]] | R[s[1]]
        elif o == "xor": R[d] = R[s[0]] ^ R[s[1]]
        elif o == "not": R[d] = W256 ^ R[s[0]]
        elif o == "shr": R[d] = R[s[0]] >> s[1]
        elif o == "shl": R[d] = (R[s[0]] << s[1]) & W256
        elif o == "shrv": R[d] = R[s[0]] >> R[s[1]]
        elif o == "ldx": R[d] = bitmap(R[s[0]])
        elif o == "cmp": R[d] = int(R[s[0]] != 0)
        elif o == "cmplt": R[d] = int(R[s[0]] < R[s[1]])
        elif o == "br": br[kind] = R[s[0]]
        else: raise ValueError(o)
        if check and lay.mode == "w36x7" and o in ("add", "and", "or", "xor") and sec in ("rounds", "schedule"):
            v = R[d]
            # dynamic soundness: value within the statically bounded lanes, nothing above bit 251
            assert v >> (lay.lanes * lay.width) == 0, (sec, o, d)
            if d in P.bnd and P.bnd[d]:
                for lv in lay.lanes_of(v):
                    assert lv <= P.bnd[d], (sec, o, d, lv, P.bnd[d])
    return R[P.key], [R[h] for h in P.hits], ops, br, R["X"], R["B6"], mem["CTR"]


def histogram(P, sections=None):
    h = {}
    for sec, o, *_ in P.ops:
        if sections and sec not in sections:
            continue
        o = {"addX": "add", "addB": "add", "ldc": "ld", "cmplt": "cmp", "shrv": "shr"}.get(o, o)
        h[o] = h.get(o, 0) + 1
    return h


def by_section(P):
    h = {}
    for sec, o, d, s, kind in P.ops:
        h[sec] = h.get(sec, 0) + 1
    return h


def mask_loads(P, sections=None):
    return sum(1 for sec, o, d, s, kind in P.ops
               if o == "ld" and kind == "mask" and (sections is None or sec in sections)
               and (s[0].startswith(("LO", "HI", "SHR", "L31", "H31"))))


def live_profile(P, reuse=False):
    """Registers in use at every instruction of the straight-line pass (interval colouring of a
    straight-line program = maximum overlap).  strict (reuse=False): the destination never shares a
    register with a source that dies at that instruction; reuse=True: it may.  Always added: X, B6,
    the 4 fixed registers and the run-resident masks."""
    last = {}
    for i, (sec, o, d, s, kind) in enumerate(P.ops):
        for v in s:
            if isinstance(v, str) and v.startswith("v"):
                last[v] = i
    last[P.key] = max(last.get(P.key, 0), len(P.ops))
    live, prof = set(), []
    fixed = 2 + 4 + len(P.glob)
    for i, (sec, o, d, s, kind) in enumerate(P.ops):
        dying = {v for v in s if isinstance(v, str) and last.get(v) == i}
        if reuse:
            n = len(live) + (1 if (d in last and not dying) else 0)
        else:
            n = len(live) + (1 if d in last else 0)
        prof.append(n + fixed)
        live -= dying
        if d in last:
            live.add(d)
    return prof


def max_live(P, reuse=False):
    return max(live_profile(P, reuse))


# ----------------------------------------------------------------------------------------------
def bcast_cost(lay):
    """Ops to build one lane-broadcast vector from a scalar group value already stored by the
    group set-up: load, shift/OR doubling, store."""
    if lay.mode == "w36x7":
        # v | v<<36 ; b1 | b1<<72 ; b2 | b1<<144 ; b3 | v<<216   (8 ALU) + load + store
        return 10
    # v | v<<32 ; | <<64 ; | <<128   (6 ALU) + load + store
    return 8


def bcast_emulate(lay, v):
    if lay.mode == "w36x7":
        b1 = v | (v << 36); b2 = b1 | (b1 << 72); b3 = b2 | (b1 << 144); b4 = b3 | (v << 216)
        return b4 & W256
    b1 = v | (v << 32); b2 = b1 | (b1 << 64); b3 = b2 | (b2 << 128)
    return b3 & W256


def load_ref_modules():
    """Organizer core (repo/verifier/hash_functions.py, sha256 514fa8ab...) and kprog.py (extracted
    verbatim from the proof, sha256 c0c4453a...), both optional."""
    hf = kp = None
    for p in (os.path.join(HERE, "..", "repo", "verifier", "hash_functions.py"),
              os.path.join(HERE, "ref_hash_functions.py")):
        if os.path.exists(p):
            spec = importlib.util.spec_from_file_location("ref_hash_functions", p)
            hf = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(hf)
            sys.modules["ref_hash_functions"] = hf
            break
    kpath = os.path.join(HERE, "kprog_extracted.py")
    if hf is not None and os.path.exists(kpath):
        spec = importlib.util.spec_from_file_location("kprog_extracted", kpath)
        kp = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(kp)
    return hf, kp


class Bitmap:
    """Pseudo-random 2^24-bit bitmap in 64-bit words (dense, so ~half the tests hit), with an
    optional set of forced bits.  Shared by the SWAR program and kprog's scalar program."""

    def __init__(self, seed):
        self.seed = seed
        self.forced = {}

    def __call__(self, addr):
        x = (addr * 0x9e3779b97f4a7c15 + self.seed) & ((1 << 64) - 1)
        x ^= x >> 31; x = (x * 0xbf58476d1ce4e5b9) & ((1 << 64) - 1); x ^= x >> 29
        return x | self.forced.get(addr, 0)

    def get(self, addr, default=0):           # kprog.run uses mem.get(addr, 0)
        return self(addr)


def validate(mode, n_groups, passes_per_group, seed, hf, kp, log, refmask=False, cfg=None):
    lay = Layout(mode)
    L = lay.lanes
    P = gen_pass(mode, refmask=refmask, cfg=cfg)
    PT = gen_pass(mode, tail=True, refmask=refmask, cfg=cfg) if (1 << 24) % L else None
    consts = lay.constants()
    kprog_P = kp.gen_lane(False) if kp else None
    rng = random.Random(seed)
    stats = dict(trials=0, passes=0, tail_passes=0, mism_key=0, mism_hit=0, mism_org=0, mism_kprog=0,
                 hits=0, forced=0, gv_mism=0, ops=set(), tail_ops=set(), aborts_ok=0, loop_ok=0)
    full_last = ((1 << 24) // L - 1) * L if (1 << 24) % L else (1 << 24) - L
    for gi in range(n_groups):
        m = [rng.getrandbits(32) for _ in range(15)]
        gv = group_values(m)
        kgv = kp.group_values(m) if kp else None
        if kp and any(kgv[nm] != gv[nm] for nm in GROUP_NAMES):
            stats["gv_mism"] += 1
        G = {nm: bcast_emulate(lay, v) for nm, v in gv.items()}
        for nm in G:
            assert G[nm] == lay.bcast(gv[nm])
        bm = Bitmap(rng.getrandbits(64))
        bases = [0, full_last, full_last - L, (1 << 20) - 3, (1 << 23) - 1]
        while len(bases) < passes_per_group:
            bases.append(rng.randrange(0, full_last + 1))
        bases = bases[:passes_per_group]
        if PT is not None:
            bases.append(full_last + L)          # tail pass: j = 2^24-1 (+6 non-trial lanes)
        for base in bases:
            tail = base + L > (1 << 24)
            prog = PT if tail else P
            X = sum((base + l) << (lay.width * l) for l in range(L))
            # force a hit on a random lane sometimes, to exercise both branch outcomes
            bm.forced = {}
            key_w, hits, ops, br, Xn, B6n, ctr = run(prog, G, X, base + L - 1, bm, consts)
            (stats["tail_ops"] if tail else stats["ops"]).add(ops)
            stats["tail_passes" if tail else "passes"] += 1
            assert ctr == L
            assert Xn == sum((base + L + l) << (lay.width * l) for l in range(L))
            if not tail:
                contains = any(((base + l) & 0xfffff) == 0 for l in range(L))
                stats["aborts_ok"] += int(br["abort"] == int(contains))
                nxt = base + L
                stats["loop_ok"] += int(br["loop"] == int(nxt + L - 1 < (1 << 24)))
            for l, h in enumerate(hits):
                j = base + l
                assert j < (1 << 24)
                lane_key = (key_w >> (lay.width * l)) & MASK
                ref = compress31(IV, m + [j])[0]
                stats["mism_key"] += int(lane_key != ref)
                if hf is not None:
                    blk = b"".join(v.to_bytes(4, "big") for v in m + [j])
                    stats["mism_org"] += int(hf._compress("sha256", tuple(IV), blk, 31)[0] != lane_key)
                bi = ref >> 8
                want = (bm(bi >> 6) >> (bi & 63)) & 1
                stats["mism_hit"] += int(h != want)
                stats["hits"] += h
                if kprog_P is not None:
                    kk, kh, kops = kp.run(kprog_P, kgv, j, bm)
                    stats["mism_kprog"] += int(kk != lane_key or kh != h or kops != 775)
                stats["trials"] += 1
            # forced-hit check on one lane: set its bit, decision must flip to 1 on that lane only
            l = rng.randrange(len(hits))
            lane_key = (key_w >> (lay.width * l)) & MASK
            bi = lane_key >> 8
            bm.forced = {bi >> 6: 1 << (bi & 63)}
            _, hits2, _, _, _, _, _ = run(prog, G, X, base + L - 1, bm, consts, check=False)
            stats["forced"] += 1
            stats["mism_hit"] += int(hits2[l] != 1)
            bm.forced = {}
    log(f"[{mode}] groups {n_groups}, full passes {stats['passes']}, tail passes {stats['tail_passes']}, "
        f"lane trials checked {stats['trials']}")
    log(f"[{mode}]   key vs own FIPS compress31: mismatches {stats['mism_key']}; vs organizer _compress: "
        f"{stats['mism_org'] if hf else 'n/a'}; vs kprog scalar trial (key, decision, 775 ops): "
        f"{stats['mism_kprog'] if kp else 'n/a'}; bitmap decisions: {stats['mism_hit']} "
        f"(hits {stats['hits']}, forced-hit checks {stats['forced']}); group values vs kprog: {stats['gv_mism']}")
    log(f"[{mode}]   ops per full pass observed {sorted(stats['ops'])}, tail {sorted(stats['tail_ops'])}; "
        f"abort-test decisions right {stats['aborts_ok']}/{stats['passes']}, loop decisions right "
        f"{stats['loop_ok']}/{stats['passes']}")
    bad = stats["mism_key"] + stats["mism_org"] + stats["mism_kprog"] + stats["mism_hit"] + stats["gv_mism"]
    bad += (stats["passes"] - stats["aborts_ok"]) + (stats["passes"] - stats["loop_ok"])
    assert len(stats["ops"]) == 1
    return stats, bad


def group_schedule_check(L):
    """Pass/abort schedule of one group, enumerated: passes, trials, abort-check firings."""
    passes = fires = trials = 0
    base = 0
    while base + L <= (1 << 24):            # full passes (loop exits when next B6 >= 2^24)
        passes += 1; trials += L
        if ((base + L - 1) & 0xfffff) < L:
            fires += 1
        base += L
    tail = 0
    if base < (1 << 24):
        tail = 1; trials += (1 << 24) - base
    return passes, tail, fires, trials


HIT_EXTRA = 3        # per bitmap hit: j = B6 - (L-1-l) for the hit lane (load constant, sub) + 1 spare

S12 = ["LO6", "HI6", "LO11", "HI11", "LO25", "HI25", "LO2", "HI2", "LO13", "HI13", "LO22", "HI22"]
V2CFG = dict(sched_first=True,
             glob=S12 + ["LO17"],                                   # resident for the whole run
             res_sched=["HI17", "LO19", "HI19", "SHR10"],           # loaded once per pass, phase 1
             res_round=[],
             sched_order=(17, 19, 22, 21, 24, 26, 28, 23, 25, 27, 30, 29))
# per group: load the 13 run-resident masks into registers (they are also rebuilt per group, v1)
V2_GROUP_EXTRA = len(V2CFG["glob"])
# per bitmap hit: hit processing may need every register -> reload the 13 resident masks after it
V2_HIT_EXTRA = len(V2CFG["glob"])


def ledger_v2(P_ops, log, label, quiet=False, extras=True):
    """Ledger on the CURRENT base (jungjipdo's 35.32 package), formula given by the coordinator,
    plus (extras=True) our own v2 extras: 13 mask loads per group and 13 reloads per bitmap hit."""
    import math
    GROUPS, HITS, PASSES = 5_932, 58_831_394, 14_217_497_272
    k_ops = (58_601_795_172_441 - 58_165_531_920_660 + PASSES * P_ops + GROUPS * 592 + HITS * 3
             + GROUPS * 192)
    if extras:
        k_ops += GROUPS * V2_GROUP_EXTRA + HITS * V2_HIT_EXTRA
    k_units = -(-k_ops // 2140)
    total = 42_877_883_846 - 27_384_016_436 + k_units
    lg = math.log2(total)
    if not quiet:
        log(f"[{label}] P={P_ops}: K ops {k_ops:,} -> K units {k_units:,}; total {total:,} = 2^{lg:.6f}"
            f" -> claim >= {math.ceil(lg * 100) / 100:.2f} / {math.ceil(lg * 1000) / 1000:.3f}")
    return dict(k_ops=k_ops, k_units=k_units, total=total, log2=lg)


def main():
    quick = "--quick" in sys.argv
    out = []

    def log(s):
        print(s, flush=True)
        out.append(s)

    hf, kp = load_ref_modules()
    log(f"organizer core loaded: {hf is not None}; kprog (verbatim from proof C.6) loaded: {kp is not None}")
    mode = "w36x7"
    P1 = gen_pass(mode)                       # v1 layout (CFG defaults)
    P = gen_pass(mode, cfg=V2CFG)
    n = len(P.ops)
    log(f"v1 pass: {len(P1.ops)} ops, max live strict {max_live(P1)} / reuse {max_live(P1, True)}")
    log(f"v2 config: {V2CFG}")
    log(f"v2 pass: {n} ops ({n / 7:.3f}/trial)  by section {by_section(P)}")
    log(f"v2   primitive histogram {dict(sorted(histogram(P).items()))}")
    for s_ in ("schedule", "rounds", "bitmap", "loop"):
        log(f"v2     {s_:9s} {dict(sorted(histogram(P, (s_,)).items()))}")
    prof = live_profile(P)
    log(f"v2   registers: max live strict {max(prof)} (dst never reuses a dying source), reuse "
        f"{max_live(P, True)}; includes X, B6, M7, BM, C63, C1 and {len(P.glob)} run-resident masks; "
        f"program points at 32: {sum(1 for v in prof if v == 32)}")
    assert max(prof) <= 32
    log(f"v2   remaining lane-mask loads per pass {mask_loads(P)}; scratch stores "
        f"{sum(1 for o in P.ops if o[1] == 'st')} (12 schedule addends + CTR), reloads "
        f"{sum(1 for o in P.ops if o[1] == 'ldc')} (12 addends + CTR)")
    PT = gen_pass(mode, tail=True, cfg=V2CFG)
    log(f"v2   tail pass {len(PT.ops)} ops (charged as full); max live {max_live(PT)}")
    ng, ppg = (800, 8) if not quick else (60, 6)
    stats, bad = validate(mode, ng, ppg, 0x5eed31, hf, kp, log, cfg=V2CFG)
    log(f"v2   total mismatches/failures: {bad}")
    assert bad == 0 and stats["ops"] == {n}
    Pr = gen_pass(mode, refmask=True, cfg=V2CFG)
    stats, bad = validate(mode, 40 if not quick else 5, 4, 77, hf, kp, lambda s_: None, refmask=True, cfg=V2CFG)
    assert bad == 0 and stats["ops"] == {len(Pr.ops)}
    log(f"v2 refmask variant (T1, T2, schedule words, key masked): {len(Pr.ops)} ops = P + "
        f"{len(Pr.ops) - n}, max live {max_live(Pr)}, validated (0 mismatches)")
    log("== ledger on the current base (35.32 package) ==")
    import math
    for extras in (False, True):
        tag = "coordinator formula" if not extras else "+ v2 extras (13/group, 13/hit)"
        r1 = ledger_v2(n, log, f"{tag}, P", extras=extras)
        r2 = ledger_v2(n + 43, log, f"{tag}, P+43", extras=extras)
    r0 = ledger_v2(1322, log, "reference: v1 P=1322, coordinator formula", extras=False)
    with open(os.path.join(HERE, "swar7_k_v2_output.txt"), "w") as fh:
        fh.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
```

Output:

```text
organizer core loaded: True; kprog (verbatim from proof C.6) loaded: True
v1 pass: 1322 ops, max live strict 26 / reuse 25
v2 config: {'sched_first': True, 'glob': ['LO6', 'HI6', 'LO11', 'HI11', 'LO25', 'HI25', 'LO2', 'HI2', 'LO13', 'HI13', 'LO22', 'HI22', 'LO17'], 'res_sched': ['HI17', 'LO19', 'HI19', 'SHR10'], 'res_round': [], 'sched_order': (17, 19, 22, 21, 24, 26, 28, 23, 25, 27, 30, 29)}
v2 pass: 1115 ops (159.286/trial)  by section {'schedule': 237, 'rounds': 791, 'bitmap': 71, 'loop': 16}
v2   primitive histogram {'add': 126, 'and': 366, 'br': 9, 'cmp': 9, 'ld': 66, 'ldx': 7, 'not': 15, 'or': 114, 'shl': 114, 'shr': 147, 'st': 13, 'xor': 129}
v2     schedule  {'add': 27, 'and': 60, 'ld': 30, 'or': 24, 'shl': 24, 'shr': 36, 'st': 12, 'xor': 24}
v2     rounds    {'add': 89, 'and': 284, 'ld': 28, 'not': 15, 'or': 90, 'shl': 90, 'shr': 90, 'xor': 105}
v2     bitmap    {'add': 7, 'and': 21, 'br': 7, 'cmp': 7, 'ld': 1, 'ldx': 7, 'shr': 21}
v2     loop      {'add': 3, 'and': 1, 'br': 2, 'cmp': 2, 'ld': 7, 'st': 1}
v2   registers: max live strict 32 (dst never reuses a dying source), reuse 31; includes X, B6, M7, BM, C63, C1 and 13 run-resident masks; program points at 32: 44
v2   remaining lane-mask loads per pass 9; scratch stores 13 (12 schedule addends + CTR), reloads 13 (12 addends + CTR)
v2   tail pass 1045 ops (charged as full); max live 32
[w36x7] groups 800, full passes 6400, tail passes 800, lane trials checked 45600
[w36x7]   key vs own FIPS compress31: mismatches 0; vs organizer _compress: 0; vs kprog scalar trial (key, decision, 775 ops): 0; bitmap decisions: 0 (hits 22779, forced-hit checks 7200); group values vs kprog: 0
[w36x7]   ops per full pass observed [1115], tail [1045]; abort-test decisions right 6400/6400, loop decisions right 6400/6400
v2   total mismatches/failures: 0
v2 refmask variant (T1, T2, schedule words, key masked): 1158 ops = P + 43, max live 32, validated (0 mismatches)
== ledger on the current base (35.32 package) ==
[coordinator formula, P] P=1115: K ops 16,288,953,854,931 -> K units 7,611,660,680; total 23,105,528,090 = 2^34.427519 -> claim >= 34.43 / 34.428
[coordinator formula, P+43] P=1158: K ops 16,900,306,237,627 -> K units 7,897,339,364; total 23,391,206,774 = 2^34.445247 -> claim >= 34.45 / 34.446
[+ v2 extras (13/group, 13/hit), P] P=1115: K ops 16,289,718,740,169 -> K units 7,612,018,103; total 23,105,885,513 = 2^34.427541 -> claim >= 34.43 / 34.428
[+ v2 extras (13/group, 13/hit), P+43] P=1158: K ops 16,901,071,122,865 -> K units 7,897,696,787; total 23,391,564,197 = 2^34.445269 -> claim >= 34.45 / 34.446
[reference: v1 P=1322, coordinator formula] P=1322: K ops 19,231,975,790,235 -> K units 8,986,904,575; total 24,480,771,985 = 2^34.510930 -> claim >= 34.52 / 34.511
```
