# sha256-r31: replay of a collision built entirely by our own committed construction

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
- The z3 runs are charged as the runs of the Linux build of the same solver version on the same models, which
  print byte-identical models and search statistics (H6): the per-form total of every executed instruction, from
  callgrind for attempt 1 and exp-bbv basic-block vectors for attempts 2 and 3 (Section 14.4). Every multiply,
  divide and floating-point form is priced by a checked emulation; the few instructions exp-bbv does not report
  cost 1024 each. Their kernel work is bounded from measured page faults, system calls, launches and CPU time (H9).
- Search K is charged by an exact operation count (Sections 16 and 17). Its hit processing, group
  set-up and table build are the counted program of Section 16, with every load and store counted
  and no native 32-bit rotation. Its trials are counted as a 7-lane SWAR program (Section 17): seven
  consecutive trials of a group share one 256-bit word, one 32-bit value per 36-bit lane, on the
  cost model's word RAM with 64 registers. Replayed over every group of the run, the counted program
  takes the same key and bitmap decision as the executable's own trial block on all 99,492,036,640
  trials, reproduces every counter of the run's log and reproduces the stored pair. The worst-path
  count of each hit event is multiplied by the run's own counter of that event.
- The synthetic completion checks are charged the same way, by exact counted replays of the three
  runs that reproduce their logged counters (Sections 16.6 and 18). This corrects our earlier filings,
  which charged three equal runs.
- The analysis programs that formulated R20 before any search ran are counted the same way; their
  counted versions print exactly the originals' outputs (Sections 15.2 and 19).
- The five yield checks before K ran K's own table build (`r31det3 1 0`, `diag 1 0`). They are
  charged by its counted program (Section 18.6).
- Our other own code is charged with explicit operation counts.
- Runs that read the published colliding pair or the starting solution derived from it are not part of C
  and are not charged. Besides the relaxed-search, synthetic and K' runs of 10-07, these are the three
  `analyze.py` runs and the two runs of the yield program `table` of the pre-construction analysis,
  which our filings up to v9 had charged as part of C. No constant of C comes from any of them
  (Sections 15.1, 15.4).
The complete source is in Appendices B to F; a few files that no charge of this filing needs are cited there by
SHA-256 with the earlier filing that embeds them.

| field | value | where |
|---|---|---|
| time_log2 | 33.914 | executed work of C plus replay, 2^33.9116, Section 9 |
| preprocessing_log2 | 33.914 | construction chain C, Section 9 |
| success_probability | 1 | deterministic replay, Section 3 |
| nonuniform_advice_log2_bytes | 9 | the stored 256-byte pair, Section 10 |
| memory_log2_bytes | 29.5 | measured peak over C and the analysis (`joint`, 2^29.003 bytes), Section 10 |

Our own change to the source attack is the relaxed W20 condition R20 (Section 6). The published
characteristic fixes the s0-difference of W5 and the s1-difference of W18. R20 only requires that
the two cancel, which is exactly dW20 = 0. The stored pair uses differences of 0ffd81e1 and
f0027e1f, not the characteristic's.

Heuristics are declared in Section 11:
- H1-public-characteristic, H2-counted-programs, H3-heavy-tariffs, H5-chain-scope,
  H6-z3-build-transfer, H7-profile-reconstruction, H8-lumps-and-hand-bounds and H9-z3-kernel-work are
  score-critical;
- H4-memory is supporting.
No probability estimate enters the bound.

**History of this line.** v10 (089b597d, 35.32); v11 (028aa8d0, 34.38) counts K's trials as a 7-lane SWAR program
(Section 17; the layout is Th0rgal's, f310d44f, first applied to this K by Meganpark980320's 0404f1a6; ours is
independent); v12b (d93038bc, 34.233), v13 (f397b3d1, 34.134) and v14 (89bc1467, 34.033) re-counted the other lines.
Each re-count undone is a sensitivity (H2).

**What changed from v14 (this filing, v15).** C's z3 step is charged as the profiled runs of the Linux build of the
same solver version, which print byte-identical models and statistics (H6), at the per-form total of every user-space
instruction: 7,112,930,424 units against v14's 8,577,511,235. Their kernel work is a new line (H9): 20,331,287,862
instructions at 6, 57,003,611 units. The total falls from 2^34.0321 to 2^33.9116; the claim 33.914 keeps a reserve
for the `-T` limit and the split-execution bound together (H6, H7). v14's charge is the fallback of H6.

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

The z3 runs are charged by the per-form totals of their profiled Linux runs (Section 14.4; H3, H6, H7) and
their kernel work by H9. Search K is charged
by the operation counts of its counted programs (Sections 16, 17 and 18, H2), and the synthetic checks
and the yield checks by theirs (Sections 16.6 and 18, H2).
The analysis programs of Section 15.2 are charged by the exact operation counts of their counted
versions (Sections 15.2 and 19, H2). Our other own code is charged with the operation counts of H2.

    z3 attempts 1-3 (Section 14.4, H3, H6, H7): per-form totals of the Linux runs, 1,236,374,141,020
        + 7,681,645,125,235 + 4,391,752,289,750 + 1024 * 1,867,089,404 = 15,221,671,105,701 ops / 2140   7,112,930,424
    z3 kernel work (H9): 20,331,287,862 instructions * 6 = 121,987,727,172 ops / 2140      57,003,611
    synthetic completion checks (Sections 16.6 and 18, H2): exact counted replays,
        902,467,916,687 ops / 2140                                                 421,713,980
    yield checks (Section 18.6, H2): 5 table builds of K's counted program, P1 as SWAR,
        and diag's two loops (2 runs * 2 * 81,321,704): 280,487,774,846 ops / 2140              131,069,054
    V8 dump (one 2^32 scan, <= 24 ops/word) and c8 residue scan
        (300,000 * 49408 candidates, <= 8 ops each)                                   103,578,699
    pre-construction analysis (Sections 15.2, 19): 2,590,547,428,027 ops / 2140        1,210,536,182
    process launch and library calls of the yield checks, V8 dump and c8 scan (H8):
        4.1e8 instructions * 1024 = 419,840,000,000 ops / 2140                        196,186,916
    Python runs (H8): at most 50 invocations * 5e8 instructions * 12 = 3e11 ops / 2140   140,186,916
    K run (Sections 16 and 17, H2), primitive operations of the counted program:
      search: 14,213,153,175 passes of 7 trials (SWAR, Section 17) * 1,000         14,213,153,175,000 ops
      group head, set-up, lane broadcast, 17 events and their register saves:
        5,932 groups * 16,151                                                    95,807,732 ops
      bitmap hits: 58,831,394 * (1,642 + 2 lane index + 128 register save)        104,249,230,168 ops
      key-matched hits 1,376,281 * 13, matched records 3,061,666 * 238,
        V6 passes 5,992 * 2,344, the R20 pass to the stored pair 2,533,318          763,146,727 ops
      table build (SWAR 2^32 scan, records, sort, bitmap), s1 inverse, self-check  56,032,497,606 ops
      library calls and main thread: at most 10^8 instructions * 1024         102,400,000,000 ops
      K: 14,476,693,857,233 ops / 2140                                              6,764,810,214
    full 31-step compressions inside the counted programs, at one unit each (16.7):
        58,849,704 compressions * (2140 - 1377) = 44,902,324,152 ops / 2140           20,982,395
    -------------------------------------------------------------------------------------------
    preprocessing (chain C)                                                   16,158,998,391 = 2^33.9116
    replay R                                                                 6.36
    total (rounded up)                                                        16,158,998,398 = 2^33.9116

Claimed time_log2 = 33.914 and preprocessing_log2 = 33.914. Every term is the work actually executed
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
per-instruction price of the v5 table (Section 16.3). The program is v10's (Section 16) with its
trial passes written for seven trials per 256-bit word (Section 17): 1,000 primitives per pass of
7 trials (142.9 per trial) instead of 4,677 per pass of 8 (584.6 per trial). The K term is
41.9% of the total. The z3 lines are 44.4%.

The K run was not lucky. Model value: with 132096 records, a V6 rate of 2^-9 and an R20 rate of
2^-12.66, a first success is expected after about 2^36.65 trials. K needed 2^36.531.

## 10. Memory and advice

The advice of R is the stored 256-byte pair; 9 is claimed.

Peak memory is taken over every run that is charged: chain C and the pre-construction analysis
(Section 15.1). It is the maximum resident set size reported by `/usr/bin/time -l`:
- for the z3 attempts (C's macOS runs; the native Linux runs peak at most 161,607,680, C.15) and search K, as recorded during the runs (Section 8);
- for every other run, from a re-run of the same binary or script on the same inputs on the same
  machine (2026-10-08; not charged, Section 15.1).
The last column gives the largest allocation in each run's source, so that the measured figures can
be checked against the code.

| run | maximum resident set (bytes) | largest allocation in the source |
|---|---|---|
| z3 attempt 1 / 2 / 3 | 154,107,904 / 161,103,872 / 153,944,064; native Linux runs (C.15) 107,638,784 / 161,607,680 / 133,640,192 | solver memory (z3 reports 95 MB peak for attempt 1) |
| search K (`r31det3`, 12 threads) | 7,438,336 | records: malloc of 2^20 * 24 bytes (24 MiB, 132,096 used); bitmap 2 MiB |
| synthetic checks (`r31sim3`, run 3's command) | 5,799,936 | the same records and bitmap |
| yield checks: `r31det3 1 0` / `diag 1 0` | 5,832,704 / 5,816,320 | the same records and bitmap |
| V8 dump / c8 scan | 1,720,320 / 1,916,928 | c8 scan: static array of 60,000 words |
| `sets` / `table` (`table` excluded since v10, Section 15.4) | 1,703,936 / 1,720,320 | `table`: static key array of 2^24 * 4 bytes (64 MiB, sparsely touched) |
| `joint` | **538,050,560** | two calloc'd hash tables of 2^25 entries * 8 bytes = 2^29 bytes |
| `pany` | 269,549,568 | one table of 2^25 * 8 bytes = 2^28 bytes |
| `pany2` (1 thread; 12 threads) | 269,615,104; 269,631,488 | one table of 2^28 bytes, plus thread stacks |
| Python: gen_s.py / check_s.py / analyze.py | 18,202,624 / 17,465,344 / 24,625,152 | interpreter |

The peak is `joint`'s 538,050,560 bytes = 2^29.003. It is its two hash tables of 2^25 entries of
two 32-bit words each (2^29 bytes), plus code, stack and allocator state. We claim
memory_log2_bytes = 29.5 (759,250,125 bytes). That is 1.41 times the measured peak, and above the
sum of the largest allocations in any single source: `joint`'s 2^29 bytes plus at most a few MiB.
Our earlier filings claimed 27.5 from the chain's runs only and missed the analysis programs. The
measurement programs of Appendices C to F (`kcount.c`, `scount.c`, `pcount.c`, `kswar.c`,
`scount12.c`, `p1swar.c`, `pcount13.c`, the profilers) are not charged runs. Their largest allocation, `pcount`'s copy of `joint`'s two tables, is the same 2^29
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
  charge of T units for it gives a total of 16,158,998,398 + T units. That stays below 2^39.15 (our
  earlier filing) for T up to 2^39.111, and below 2^40.4 for T up to 2^40.383.

H2-counted-programs (score-critical). The work of search K, of the three synthetic completion
checks, of the five yield checks and of the pre-construction analysis programs is the operation count
of explicit programs that compute the same results with v5 primitives, not the retired instructions
of their executables.
- Statement: K's trial passes are charged by the SWAR pass of Section 17 (1,000 primitives per pass
  of 7 trials) times the passes K executed, and its other events by the worst-path counts of
  Section 16.3 times the run's event counters (Section 8). Its table build is charged with the SWAR
  scan of Section 18.5. The synthetic checks are charged by exact counted replays, whose trial loops
  are those of Section 18. The yield checks are charged by the count of K's table build (Section
  18.6). The analysis programs are charged by the exact counts of counted versions (Sections 15.2
  and 19).
- Scope: the counted programs `kprog.py` and `kcount.c` (Appendix C.6-C.8), `scount.c` and `pcount.c`
  (C.9, C.13; cited by SHA-256, their outputs embedded), `kswar.py` and `kswar.c` (Appendix D), `scount12.c` and `p1swar.c` (Appendix E), and
  `pcount13.c` (Appendix F). They
  use only v5 primitives, count every load and store, use no native 32-bit rotation, and write Σ, σ,
  Ch and Maj as exact identities (Sections 16.1 and 17.1). Products by a variable are explicit
  385-primitive shift-and-add emulations. Products by a constant of the program text are
  shift-and-add over the constant's non-adjacent form. Both are inside the count. The SWAR pass of
  K runs on the cost model's word RAM with 64 registers, the machine of the promoted blake3-r2
  package 52bb50ee (Section 17.1); the SWAR loops of Section 18 fit 32. The cost model fixes the
  primitives, not a register count.
- Evidence:
  - The SWAR pass of K, replayed over every group that K executed (99,492,036,640 trials in
    14,213,153,175 passes), takes the same key and bitmap decision on every trial as
    `r31det3`'s own trial block and as v10's counted scalar trial.
  - Its counted hit processing agrees with `r31det3`'s `process_hit` on every counter of every
    group. The summed counters equal the run's FINAL and DET lines, and group 5920 reproduces the
    stored pair (Section 17.4). `kswar.py` checks 21,000 lanes against the organizer reference
    core, asserts a static per-lane bound below 2^36 for every addition and counts the live
    registers.
  - The executable that ran evaluated K's trials packed four to a 128-bit NEON register, retiring
    154.75 instructions per trial on its hot path (Section 14.6).
  - The synthetic replays of `scount12.c` check every trial against `r31sim3`'s own draws, record
    index and candidate loop, and reproduce the logged FINAL counters of runs 2 and 3. Run 1's stop
    at its first trial is reproduced by a re-run (16.6). The constant products are checked on 10^6
    values, the remainder on 2 * 10^6 values against C's, and the theorem's condition is asserted
    for each run (Section 18).
  - The SWAR scan's V7, V8 and G16 lists equal those of `build_table`'s loop word for word (18.5).
    Each counted analysis program prints exactly the original's output (15.2, 19). Every sample of
    `pany` and `pany2` is checked against the original's list of distinct values (19).
- Full 31-step compressions inside the counted programs are charged at least one unit each (16.7).
- Extrapolation: none for K's trials or the synthetic trials, which are all replayed. Worst paths
  are charged for K's hit events (18 binary-search steps, all 64 G16 candidates). Every out-of-line
  path of K's SWAR loop is charged a store and reload of all 64 registers. For the yield checks, the
  S of attempt 3 gives the largest table-build count of the three (C.8, C.14), and it is charged for
  all five runs.
- Sensitivity:
  - with v10's scalar trials of K (582 per lane, 584.6 per trial), the total would be 2^35.0948;
  - with K's SWAR pass but every constant loaded at each use (1,292 per pass, and 8 for loop control with its
    constants loaded too), 2^34.079;
  - with K's pass on v10's 32-register machine (1,236 + 8 per pass), 2^34.050;
  - the claim of 33.914 holds for any pass of up to 1,004 primitives;
  - with v11's synthetic trial loops, 2^34.020; with the P1 scan at v10's 55 per word
    everywhere, 2^33.978; with the yield checks at v10's hand bounds, 2^33.964;
  - with v12's counts of the analysis programs (Section 15.2), 2^34.027; with twice the analysis
    programs, 2^34.016;
  - with twice the pass, 2^34.408; with twice every K line, 2^34.416;
  - with twice the synthetic checks, 2^33.949; with twice the yield checks, 2^33.923;
  - with K charged by its executable's instructions instead (Section 14.6), 2^35.991 (one 256-bit
    word per vector register) or 2^36.788 (one word per 32-bit lane).

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
- Sensitivity: with every heavy tariff doubled (z3's totals with their heavy part doubled and the unreported
  instructions at 2048; the analysis line doubled as a bound for its floating-point forms), the total would be
  2^34.344; with the v5 table's uniform 400 for every multiply and floating-point form and 1024 for
  divides on z3, 2^34.173, or 2^34.260 with the analysis line doubled too.

H4-memory (supporting). Peak memory over C and the pre-construction analysis is at most 2^29.5 bytes.
- Scope: every charged run (Section 15.1): the z3 attempts, search K, the synthetic checks, the yield
  checks, the V8 dump and c8 scan, the analysis programs and the Python runs.
- Evidence: the maximum resident set sizes of Section 10 (`/usr/bin/time -l`), recorded during C's
  runs for z3 (macOS) and K and from re-runs of the same binaries on the same inputs for the rest.
  The largest is `joint`, 538,050,560 bytes, which its source explains: 2^29 bytes of hash tables.
- Extrapolation: a re-run touches the same pages as the original run of the same deterministic
  program on the same input.
- Sensitivity: memory does not enter the score.

H5-chain-scope (score-critical). Every constant of C comes from the public characteristic, from
analysis, from the charged pre-construction analysis programs, or from the charged v3 runs before K
(Section 15.3). The excluded runs, which used the published starting solution or studied other
methods, fixed no constant of C (Section 15.4).
- Scope: all computation on this target in our working directories and session records from
  2026-10-06 (our first run on it) to 2026-10-08, listed in Section 15.1.
- Evidence:
  - what each excluded run produced (Section 15.4); none of their files is an input of C;
  - the seeds are fixed functions of the committed strings of Appendix A (z3: the first 32 bits of the string's
    SHA-256 AND 0x0fffffff, 88108363, retries +1; K: the first 64 bits), so no seed was chosen after a run;
  - the organizer's repository holds our filing 50592e75 (commit 2ab2d36, 2026-10-07 07:15 UTC, 3 h after K
    started) with these commitments, this stored pair and the same list of runs and exclusions;
  - K is a single committed run of typical length: 2^36.531 trials against 2^36.65 expected from charged sources
    only (Section 9). Had the shortest of k runs been kept, a run this long would have probability 0.40^k;
  - closure: C re-executed from its committed inputs alone reproduces its outputs. The Linux z3 runs print S
    byte-identical from the committed models (C.12), and the replays of K from S reproduce the stored pair
    (Sections 16.4, 17.4). That S is not the published one (`check_s.py`, B.2);
  - the agent transcript, the file times, the commitments of Appendix A and the package commit history.
- Extrapolation: the commitments are local (file timestamps and a local git history), not notarised.
- Sensitivity: charging every excluded search and synthetic run anyway, at the counted cost per trial of K and
  of the synthetic checks (145.5 and 1,716 primitives) on their logged counters (1.944e12 trials, 6.79e9 samples; `r31log2` and
  `r31clus` bounded by their caps at the relaxed search's and `r31sim`'s per-thread rates), with the two `table` runs, gives 2^37.164, below the promoted record
  2^37.22 (50592e75); with the three 10-06 solver studies too (1,860 s of z3 at the macOS rate, 6 per instruction),
  2^37.494. That run alone at 1 + 32/2140 units per trial, the other lines as claimed: 2^40.660.

H6-z3-build-transfer (score-critical). C's z3 step is charged as the runs of the Linux build of the same solver
version (PyPI z3-solver 4.15.4.0) on the same models, an equivalent program for the macOS runs that C used.
- Statement: the z3 line of Section 9 is the per-form total of every user-space instruction of the three Linux runs
  (14.4), not the macOS count at a price: as H2 does for K, a cheaper implementation of the same search (the macOS
  build retires 6.4-6.6% more instructions).
- Scope: z3 attempts 1-3.
- Evidence:
  - on each model the Linux runs' output is byte-identical to the macOS run's: the model (`sat` and every
    assignment) and all 30 non-timing statistics, rlimit-count, conflicts and decisions among them (`cmpz3.py`,
    Appendix C.12); fresh native runs of the same binary give the same output again;
  - every instruction of the profiled runs is priced (H3, H7), libraries and dynamic loader included.
- Extrapolation: a different binary of the same solver version computes the same S by the same search. The time
  limit differs (`-T:1800` on macOS, never fired; `-T:1200` for attempt 1, none for 2 and 3); it does not change the
  search, and without it attempt 1 retires 0.21% fewer instructions (245,008,900,614 against 245,527,956,010).
- Sensitivity: with that 0.21% added to attempts 2 and 3, the total would be 2^33.9127; with the macOS
  counts (kernel included) at the Linux runs' exact means, 2^33.947; fallback, the macOS counts at 6 as in our
  filing 89bc1467 (passed review as 14741493), 2^34.0321; at v13's 7, 2^34.133; with both z3 lines doubled, 2^34.441.
  With the split-execution bound of H7 too, 2^33.9137, within the claim.

H7-profile-reconstruction (score-critical). The per-instruction profiles of z3 attempts 2 and 3
are reconstructed from exp-bbv superblock counts.
- Statement: attempts 2 and 3 are priced from exp-bbv basic-block vectors (14.4; callgrind's memory grows without
  bound on them). Each superblock is disassembled from the executable that ran (to the first control transfer, or
  100 instructions), and its count is priced as whole executions plus at most one partial one.
- Scope: attempts 2 and 3. Attempt 1 is priced from its complete callgrind profile.
- Evidence:
  - exp-bbv counts every executed instruction. `bbvmix.py` checks the cumulative counts: at each of the 1,276
    reported interval ends of the three runs at most one superblock has a partial execution (`max_open` 1), the one
    the boundary splits; every other count is whole executions of the disassembled superblock;
  - on attempt 1 the reconstruction gives a mean of 5.0370 against callgrind's exact 5.0356.
- Extrapolation: the last partial interval, which exp-bbv does not report (1,867,089,404 instructions), is charged at
  1024 per instruction, more than any tariff of the table (Section 14.2).
- Sensitivity: with every interval that holds a split execution charged at the largest prefix mean of its run to
  the next unconditional transfer (v14's bound, 5.01% of the instructions), the total would be 2^33.9126,
  and with the `-T` item of H6 too 2^33.9137, both within the claim; at twice that bound and the final intervals at 4096 per instruction, 2^34.157.

H8-lumps-and-hand-bounds (score-critical). Process launch, library calls and the Python runs are
charged by measured bounds, and two small diagnostic programs by hand bounds from their source.
- Statement:
  - each process's launch and library calls: the measured per-call instruction counts of Appendix
    C.15, doubled, at 1024 per instruction (Section 9, 15.2, 16.3, 16.6);
  - the Python runs: at most 50 invocations of at most 5e8 instructions at 12 per instruction
    (Section 9);
  - the V8 dump and the c8 residue scan: the hand bounds of Section 9 (24 per scanned word, 8 per
    residue candidate). The yield checks are counted since v12 (H2, Section 18.6).
- Scope: these lines of Section 9 (4.8% of the total).
- Evidence:
  - `libmeasure.c` and its output (Appendix C.15): every library call kind the runs make, timed by
    the process's retired-instruction counter; an empty program's launch at 11.4e6 instructions;
  - the re-run instruction counts of the Python scripts, and complete callgrind profiles of CPython
    running them (Section 9);
  - the hand bounds hold for counted programs of the same loops:
    - the V8 dump's single test costs 24 per word in the scalar form of K's scan (C.7), and
      13.00 for all three tests in the SWAR scan of Section 18.5;
    - the c8 scan's inner step costs 5 primitives (load, subtract, AND, compare, add), plus loop
      control of 3 per 8 candidates when unrolled by 8, against the bound of 8.
- Extrapolation: the library counts are measured per call kind, not inside the original runs. The
  CPython price is measured on the Linux build of a neighbouring version (3.11 against 3.12) and
  doubled.
- Sensitivity: with ten times every launch and library bound, and twice the Python bound and the
  hand bounds, the total would be 2^34.299.

H9-z3-kernel-work (score-critical). The kernel work of the three Linux z3 runs is at most 20,331,287,862
instructions, charged at 6 primitives each (57,003,611 units).
- Statement: each page fault costs 2 * 10,528 (map, first touch and unmap of a fresh 16 KB page), each system call
  2 * 131,222 (open and close, the costliest kind measured), each process 2 * 11,017,339 (C.15's launch), and
  each CPU-second 2 * 21,282,912 (timer and scheduling work on a thread that only computes): 2,691,584,738 for the
  events, 17,639,703,124 for 414.41 CPU-seconds.
- Scope: the kernel side of z3 attempts 1-3 (Section 9); their user-space instructions are all in Section 14.4.
- Evidence:
  - native runs of the same binary on the same models, with identical outputs (Appendix C.15): GNU `time -v` counts
    23,732, 38,684 and 31,164 minor page faults, no major ones, and 41.54, 223.64 and 149.23 CPU-seconds;
    `strace -f -C` counts 356, 486 and 403 system calls; under valgrind the guests execute
    650, 1,008 and 838 `svc` (C.12), and the larger count is charged;
  - `kmeasure.c` (Appendix C.15) on the machine that ran C, with C.15's counter of user and kernel instructions;
  - our filing 89bc1467 charged the macOS counts, which include the kernel's instructions (C.15: the counter read
    alone retires 5,848), at 6 per instruction, and review accepted that charge (resubmission 14741493).
- Extrapolation: the doubled macOS counts per event and per CPU-second bound the Linux kernel's (a 16 KB page
  against Linux's 4 KB; the per-CPU-second figure, which varied threefold, is the largest of three runs); the
  kernel's instructions average at most 6 primitives, the price v14 applied to them and review accepted. The kernel
  is not profiled; under the table of 14.2 any mix of forms costing at most 8 stays below 8.8, and at z3's
  non-heavy mean of 2.24 a mean above 8.8 would need more than 3.1% heavy forms.
- Sensitivity: the claim holds up to 8.8 primitives per kernel instruction alone, 6.35 together with the `-T` and
  split-execution items of H6 and H7. Without this line the total
  is 2^33.9065; at 1024 per kernel instruction (as H8 prices launches), 2^34.5884, above the v14
  fallback. Remark (not claimed): virtual-memory work is not a word-RAM operation; zeroing the 93,580 faulted pages
  would take 256 operations each.

## 12. Organizer-executed experiment and certificates

`experiments/r31-completion` runs a variant of K5 on the accepted match of the stored pair, with
each trial's E13/E15 draws taken from that trial's organizer nonce through SHAKE-256. The
organizer re-hashes every returned pair. Our local run of the organizer's intake ran it in the pinned Docker
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
- Th0rgal, submission f310d44f (sha256-r32): seven independent trials in the 36-bit lanes of a
  256-bit word with 4 guard bits, one 256-bit addition per lane addition, and the rotation as two
  shifts, two masks and an OR. Section 17 uses this layout.
- Meganpark980320, submission 0404f1a6: the first public application of the 7-lane technique to
  this search K, on our v10. Section 17 is an independent implementation from our v10 program.
- The promoted blake3-r2 package (submission 52bb50ee): the 64-register machine with resident lane
  masks and a liveness count (its proof Section 5). Section 17 uses the same machine.
- Ours: R20, the starting-solution model with the yield residue, chain C and its execution, the
  experiment, the profiles and pricing of the z3 runs (Section 14), the counted programs of K, the
  synthetic checks and the analysis (Sections 15.2, 16, 17 and 18), the merged σ masks and the
  full-run replay of Section 17, and the 32-bit multiply emulations (Appendix C.11).
- T. Granlund and P. L. Montgomery, "Division by invariant integers using multiplication", PLDI 1994,
  Theorem 4.2: the reciprocal remainder of Section 18.2.

## 14. Pricing the z3 runs: our own evidence

This section supports H3, H6 and H7 for the z3 runs: it prices every executed instruction of the Linux build's
runs on the three models in primitive word operations. Sections 14.5 and 14.6 price the synthetic check's and search K's
executables in the same way; those were the charges of earlier filings and are now cross-checks,
because both are charged by counted programs (Section 16). Apart from one re-run of K's table build
(Section 14.6) and one re-run of synthetic run 1 (Section 16.6), this section re-runs no charged call on the
measurement machine except the Linux z3 runs of 14.4, which are the charge of C's z3 step. The complete profiles of 14.4 re-run the z3 attempts on the
Linux build in Docker after the stored pair existed; they fixed nothing in C, and since v15 their per-form totals
are the charge of C's z3 step (H6).

### 14.1 What ran

- z3: the Homebrew bottle of z3 4.15.4 for arm64 macOS, `/opt/homebrew/Cellar/z3/4.15.4/bin/z3`
  (SHA-256 ae6c8df33db9c9ae9a80b6044e77cd66529a141d8b25f0620f1e89b409594f48). The executable
  contains the whole solver; it links only the system libc++ and libSystem.
- The synthetic completion check: `r31sim3.c` (Appendix B.6), compiled with Apple clang
  `cc -O3 -mcpu=apple-m4`.
- Machine: Apple M4 Pro. The macOS instruction counts of Section 8 are the `instructions retired` lines of
  `/usr/bin/time -l`; the charged z3 counts are those of the Linux runs (14.4).

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
- in `a64ops.py` every multiply and floating-point form costs 400 and integer divide, floating-point
  divide and square root 1024, the v5 table's uniform prices (shift-and-add and restoring emulations;
  now the sensitivity of H3);
- new in v8 (H3): every multiply, divide and floating-point form that the charged runs
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
- any form the table does not recognise costs 8 and is reported.

### 14.3 Static costing of the binaries

The two z3 builds have the same static profile: ordinary forms 2.125 and 2.100 operations on average, heavy share
0.306% and 0.357% (macOS 2,645,113 instructions, Linux 3,619,201; the table is in filing 89bc1467).

### 14.4 The charged z3 runs: complete profiles of the Linux build on the same models

Valgrind does not run on macOS arm64. Since v15, C's z3 step is charged as the runs of the Linux build of the same
z3 version (PyPI z3-solver 4.15.4.0, SHA-256 bbea82f99718e57d...) under Docker with valgrind 3.19.0, on the three
committed models (H6). Each Linux run prints byte-identical output to the macOS run that C used, the model and all
30 non-timing statistics (`cmpz3.py`, C.12): the same S by the same search. Every executed instruction is priced by
its form (14.2; heavy forms by `mul32.py` and `heavy.py`); an instruction that cannot be mapped costs 1024.

- **Attempt 1: callgrind**, the complete profile of our earlier filings:
  `valgrind --tool=callgrind --dump-instr=yes --dump-every-bb=8000000000`, priced by `cgfull.py` (Appendix C.12).
- **Attempts 2 and 3: exp-bbv.** On these long runs callgrind's own memory grows without bound (more than 4 GB,
  while the solver stays under 170 MB), so we recorded basic-block vectors:
  `valgrind --tool=exp-bbv --vex-guest-chase=no --vex-guest-max-insns=100 --interval-size=2000000000`.
  `bbvmix.py` (Appendix C.12) disassembles each superblock from the executable that ran and prices every executed
  instruction: each superblock's whole-run count is whole executions plus at most one partial one (H7), priced
  exactly (`ops8_exact`). The last partial interval, which exp-bbv does not report, is charged at 1024 per
  instruction. These runs are single-threaded (without `-T`, the native runs make no `clone`). On attempt 1,
  exp-bbv gives a mean of 5.0370 against callgrind's 5.0356.
- **Unrecognised forms** (8 each, C.12): `mrs` of the thread pointer, scalar `ushr`, a few others, and `svc` (H9).

| attempt | method | rlimit-count, conflicts, decisions (= macOS) | Linux instructions | per-form total (ops) | mean |
|---|---|---|---|---|---|
| 1 | callgrind | 249,602,816; 1,068,222; 1,829,611 | 245,527,956,010 | 1,236,374,141,020 | 5.0356 |
| 2 | exp-bbv | 1,200,096,786; 5,096,968; 8,121,313 | 1,474,000,000,001 + 1,640,959,575 unreported | 7,681,645,125,235 | 5.2114 |
| 3 | exp-bbv | 797,205,785; 2,818,639; 5,235,640 | 834,000,000,001 + 226,129,829 unreported | 4,391,752,289,750 | 5.2659 |

    z3 = 1,236,374,141,020 + 7,681,645,125,235 + 4,391,752,289,750 + 1024 * 1,867,089,404
       = 15,221,671,105,701 ops = 7,112,930,424 units

Multiplies and other heavy instructions are 1.32% of the executed instructions of attempt 1, 99.0% of them
32-bit-operand multiplies (`umull`, `umaddl`, `madd` on w registers), mostly index and hash arithmetic; floating
point is 0.0085%. Library code is 0.8-1.5% of the instructions.

**The macOS charge (v14; the fallback of H6).** Our filing 89bc1467 charged the macOS runs (261,276,415,067,
1,572,256,055,396 and 888,282,131,643 instructions) at 6 each, the ceiling of the largest whole-run mean with split
executions at their bound (5.2745), plus 1018 each on the tails scaled to macOS (1,989,181,169):
8,577,511,235 units, total 2^34.0321. The macOS counts include the kernel's instructions.

### 14.5 The synthetic completion check (cross-check)

Charged by exact counted replays (16.6, 18); our earlier filings priced their instructions at 13 (callgrind of a gcc
build, per-form mean 6.3887; filing 089b597d, Section 14.5), not used here.

### 14.6 Search K: the executable that ran, priced by its executed path (cross-check)

Filing e0259cf5 charged K by `r31det3`'s executed NEON path (154.75 instructions per trial; table build re-measured
at 124,755,608,685; a gcc build under callgrind, 191.8 per trial). With this filing's other lines that would give
2^35.991, or 2^36.788 with one word per 32-bit lane (H2); scripts and tables in filings e0259cf5 and 089b597d.

### 14.7 What this does not establish

- The charged z3 runs are of the Linux build (H6), an equivalent program with identical outputs; attempts 2 and 3
  are reconstructed (H7); the kernel work is bounded from counted events, not profiled (H9). The counts are those of
  the runs under valgrind, which ran the same binary and libraries with the library variants that valgrind's
  environment selected; no native Linux instruction count exists (the container exposes no counters).
- The price is an operation count under our per-form table. A reviewer who prices some form higher
  can recompute the totals from the published scripts. With the v5 table's 400 for every multiply and
  floating-point form and 1024 for divides, the total would be 2^34.173; with both z3 lines doubled, 2^34.441.
- K is not charged here; its executable-priced charge (14.6) needs a 128-bit register to be one 256-bit word.
- The runs of this section came after the stored pair existed and fixed nothing in C. The Linux z3 runs are charged
  as C's z3 step (H6); the others, like the post-K re-runs of Section 8, are not charged.

## 15. Development record and the origin of every constant of C

### 15.1 Every computation on this target (2026-10-06 to 2026-10-08, KST)

The record is the agent transcript of the session that ran every command, cross-checked with
the file times of the working directories and the package commit history (commits a7d3eaa 10-07 11:37,
e13dab2 12:17, 61428b0 13:14).

| time | computation | status |
|---|---|---|
| 10-06 | three exploratory solver studies of other methods (a cut model, a meet-in-the-middle verifier model, a z-elimination model) | excluded: no output or constant used by C |
| 10-07 09:43-09:59 | pre-construction analysis: `sets` (1), `joint` (1), `pany` (1). They formulated R20 and estimated its rate (`joint`, 09:48) | **charged**, Section 15.2 |
| 10-07 09:43-09:59 | `analyze.py` (3 runs) on the published 31-step pair: digest, characteristic and per-row checks, the modular differences, the published tuple; `table` (2 runs), which counts the table records of the starting solution derived from that pair | excluded (published pair and S), Section 15.4; charged up to v9 |
| 10-07 10:36-10:37 | `r31s` self-tests (3) and a 12 s test | excluded (published S) |
| 10-07 10:37-11:22 | relaxed search with the published S, 2^40.625 trials | excluded (published S), Section 15.4 |
| 10-07 10:44-11:35 | synthetic completion, independence and cluster runs with the published S (`r31sim`, `r31log`, `r31log2`, `r31clus`, `r31log3`); `pany2` (2 runs: 2^20 samples at 10:47, 2^28 samples at about 11:24) | `pany2` **charged** (15.2); the others excluded |
| 10-07 11:55-12:12 | K' runs with the published S (filing 3183e839, refuted) | excluded (published S) |
| 10-07 12:52-13:04 | chain C before K: z3 attempts 1-3, gen_s/check_s, yield checks (5), synthetic checks (3), V8 dump, c8 scan, inline Python on S and V8 | **charged**, Section 9 (z3 by the Linux runs of its models, H6) |
| 10-07 13:04-13:07 | search K | **charged**, Section 9 |
| 10-07 13:08-13:09 | instruction-count re-runs: `diag` (2), `r31sim3` (2), `v8dump`, `c8scan` | not charged: after the pair existed |
| 10-07 15:39-16:10 | v4 price measurements (Section 14) | attempt 1's callgrind run is **charged** as C's z3 attempt 1 (H6); the rest not charged |
| 10-08 03:59-04:10 | v6 K price measurements (Section 14.6) | not charged: after the pair existed |
| 10-08 09:05-09:30 | v7: `kprog.py`, `kcount` (16.4) | not charged: after the pair existed |
| 10-08 10:03-12:59 | v8 measurements: exp-bbv profiles of z3 attempts 1-3 (callgrind runs of attempts 2 and 3 stopped by memory); `kprog.py`, `kcount`; `pcount` and the original analysis programs (15.2); `scount` and one re-run of synthetic run 1 (16.6) | the exp-bbv runs of attempts 2 and 3 are **charged** as C's z3 attempts 2 and 3 (H6); the rest not charged |
| 10-08 13:30-13:40 | v9 memory measurements: `/usr/bin/time -l` re-runs of the programs of Section 10 | not charged: after the pair existed |
| 10-08 14:49-15:23 | v11: `kswar.py`, `kswar` (17.4) | not charged: after the pair existed |
| 10-08 15:07-15:35 | v12: `scount12`, `p1swar` (18) | not charged: after the pair existed |
| 10-08 15:44-16:10 | v13: `pcount13` (19) | not charged: after the pair existed |
| 10-08 16:29-16:33 | v13: standalone `scount12` (E.3) | not charged: after the pair existed |
| 10-08 17:12-17:21 | v14: `bbvmix.py` (C.12) | not charged: after the pair existed |
| 10-08 17:32-18:10 | v15: native Linux runs of z3 attempts 1-3 under `strace` and GNU `time` (C.15); `bbvmix.py` v15; `kmeasure` | their events and CPU time bound H9; not charged themselves |

"Published S" means the runs used the published starting solution: S was derived from the published
collision in that work, so C cannot and does not use any of its outputs.

### 15.2 Charged pre-construction analysis (exact operation counts)

These programs read only the characteristic and SHA-256 constants. They ran exactly the times listed in
15.1; their source is in Appendix C.10, which also lists `table`, an excluded run since v10.
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

Since v13 these five runs are charged by the counts of Section 19 (`pcount13.c`), in all
2,590,547,428,027 operations; the table above gives the counts of v10 to v12.

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

- Outputs. With the published starting solution: the relaxed search (1,695,634,423,904 trials) printed counters and
  one collision; the K' runs (30,719,082,496 trials) one collision; `r31log`, `r31log2`, `r31log3` (87,473,258,560
  trials, a 150 s cap, 34,808,528,912) independence and cluster statistics; `r31sim`, `r31clus` (5,851,119,616
  samples, a 110 s cap) synthetic rates; short tests (1,432,354,832 trials). The 10-06 solver studies of other
  methods (1,860 s of z3) timed out, but for a wiring check that returned the published block. C reads none of their
  files: its inputs are the characteristic, the committed seeds and its own charged steps' outputs (Appendix A).
- Caps. K's stored pair is the same for every E13 cap of at least 2,829, every E15 cap of at least
  19, any thread count, and any wall cap of at least 140 s; removing the caps altogether gives the
  same pair. So no cap value influences C, whatever motivated it.
- Rates. The "not lucky" remark of Section 9 uses charged sources only: V6's density 2^-9 = |V6|/2^32 (`sets`)
  and R20's rate 2^-12.66 (`pany`). The excluded runs' measured rates agree and enter no bound.
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
  within the Python lump) and give 2^33.9248 (v9's ledger gave 2^35.3245).
- Sensitivity: charging all of them anyway gives 2^37.164, below the promoted record 2^37.22, and
  2^37.494 with the solver studies (H5).

## 16. Search K and the synthetic checks as counted word-RAM programs (H2)

This section supports the K line of Section 9, and 16.6 the synthetic-check line. Since v11 the passes
of 8 trials of 16.2 are replaced in the charge by the SWAR pass of Section 17 (7 trials per pass).
16.1-16.5 still define one trial, and give the hit, group, table and library counts that are charged.
They also give v10's charge, which is now a sensitivity. K is charged as the
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

### 16.2 One trial: 582 primitives (v10's charge, a sensitivity since v11)

`kprog.py --opt` (Appendix C.6) generates v10's trial as straight-line code from x = word 15 to the bitmap test
and emits it as C (`klane_opt.h`): steps 15..30 cost 451, the twelve schedule words that depend on x 122, and the
bitmap test 9 (two shifts, the base add, the bitmap load, AND 63, a variable shift, AND 1, compare, branch). There
is no other branch in the trial. A pass of 8 trials costs 8 * 582 + 21 = 4,677 (eight increments of x, the trial
counter, the checkpoint test and the pass loop), and `kcount.c` (C.7) measures 4,677 for every pass. Section 17
counts the same steps, schedule words and group values seven trials per word.

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

K = ceil(58,601,795,172,441 / 2140) = **27,384,016,436** units. This was v10's K line; Section 17.5 gives this
filing's, with the first and third rows replaced and the second extended.

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

The per-group counters (groups 0..3 and 5920 up to n*: 9,958, 9,931, 10,069, 9,971 and 2,654 bitmap hits) are
repeated by `./kswar sample 96` with the SWAR pass (17.4), and printed in full by `./kswar run` in D.4.

### 16.5 Comparison and sensitivity

- Per trial the counted program costs 584.6 primitives (582 + 21/8). The executable that ran
  retires 154.75 instructions per trial on its hot path. Priced with each 32-bit lane in its own
  word, those come to 1133 per trial (mean 7.32); under the SWAR prices of Section 14.6, 604.
- Forms of our previous filing. With rotations as two shifts and an OR and the Boolean functions in
  the reference core's forms (775 per trial, `klane.h`, checked in 16.4), K would be 36,272,603,691
  units and the total 2^35.4104 (with the table build of Section 18.5).
- Reference-core conventions. With every rotation written as the organizer's reference core writes
  it (mask, shift, shift, OR, mask: five primitives), and T1, T2 and every schedule word masked as
  there (1035 per trial, `klane_ref.h`), K would be 48,360,421,226 units and the total 2^35.7492.
- Library calls. With ten times the library bound (10^9 instructions at 1024), the total would be
  2^33.9496.
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

Synthetic checks: ceil(4,134,261,321,301 / 2140) = **1,931,897,814** units (v10, v11).

The S that runs 1 and 2 used (attempt 3's is in Section 7.1 and B.5); `sp_own.h` holds these words at the
positions of B.5, every other entry 0:

    attempt 1 (sp_own.h SHA-256 d273c909ecab18fc...):
      A1..A12   a651919f b369ed0a 8daec52d f314fffd fad053ff 17b7a470 abba92b4 b1da8117 a98ea05c 940d0662 52115d5b cacc07c3
      E5..E12   1d1fa7dd af887be7 4cd7cae5 943bc249 61d503d1 f02293fa aa2f0419 716dd9ec
      A'1..A'12 a651919f b369ed0a 8daec52d f314fffd fad04405 1737a471 ba9a82b1 b1da8113 a98ea05c 940d8666 52115d5b cacc07c3
      E'5..E'12 1d1f97e3 af80fbe6 9c5fce6c d93b4a4d 61d503d9 dfa31402 baef0411 716d59e4
      W9..W12   954a6452 23729d61 729f7187 e487401b
    attempt 2 (sp_own.h SHA-256 bb76cf1d3700dac3...):
      A1..A12   27b2cdda 908475f9 6713f605 6ef50cd4 052fb3fe 26d2f758 05247996 067cd8a4 9ae3df3d 5fe16d10 3ecb74eb 4f191e18
      E5..E12   1d1fa7dd afab78e7 4c97cbe5 942b8248 61c103d1 7026b3fa 2a3f2c1d f179f1e9
      A'1..A'12 27b2cdda 908475f9 6713f605 6ef50cd4 052fa404 2652f759 14046993 067cd8a0 9ae3df3d 5fe1ed14 3ecb74eb 4f191e18
      E'5..E'12 1d1f97e3 afa3f8e6 9c1fcf6c d92b0a4c 61c103d9 5fa73402 3aff2c15 f17971e1
      W9..W12   7ee742db 8a341efa 199601ee 99915ff1

Since v12 the trial-loop column and the P1 part of the first column are re-counted (Section 18.4,
18.5); the synthetic line of Section 9 is 421,713,980 units. The values above are those of v10 and v11.

Validation output (Appendix C.14): both replays reproduce their run's FINAL counters exactly:
- run 2: trials=275316736 rechits=275316736 v6=538099 joint=42381 both=88 comp=42381/42381 coll=88;
- run 3: trials=250544128 rechits=250544128 v6=489532 joint=38874 both=64 comp=38874/38874 coll=64.

### 16.7 Full compressions at one unit each

The cost model charges one selected-round target compression one unit. Our counted programs evaluate some full
31-step compressions themselves, with `compress31_c` of C.7 and C.13, at 1,377 primitives each:
- one per bitmap hit of K (58,831,394), and six in K's R20 pass;
- 2,000 in each self-check of the table build: K's, the three synthetic runs' and the five yield checks' (18,000);
- two per collision check of the synthetic runs, 2 * (88 + 64) = 304.
That is 58,849,704 in all. So that none of them costs less than one unit, each is charged the difference,
2140 - 1377 = 763 primitives: 44,902,324,152 operations, 20,982,395 units, on their own line of Section 9.
The trial passes of K and the synthetic checks evaluate steps of a compression from shared or synthetic state,
not target compressions, and stay counted. Without this line the total would be 2^33.9097.

## 17. Search K's trial passes as a 7-lane SWAR program (H2)

This section supports the K line of Section 9 since v11. The passes of 8 trials of Section 16.2 (4,677
primitives each) are replaced by passes of 7 trials in one 256-bit word (1,000 primitives each). The
hit processing, group set-up, table build and library lines of Section 16.3 are unchanged, except for
the additions listed in 17.5.

### 17.1 Machine and layout

- Primitives and conventions as in Section 16.1. A 256-bit word holds seven 36-bit lanes, lane l at
  bits 36l..36l+35 (l = 0..6); bits 252..255 stay 0. A lane holds a value below 2^36 whose low 32
  bits are the 32-bit word of the C source; its top 4 bits are guard bits. Lane l of the pass at b
  holds trial x = b + l of the group, so a pass covers seven consecutive trials in `r31det3`'s order,
  and the lanes' bitmap decisions are taken in lane order.
- Registers. The machine is the cost model's 256-bit word RAM with 64 registers. This is the machine
  of the promoted blake3-r2 package (submission 52bb50ee, proof Section 5, "The counted pieces on a
  64-register machine"), which states: "The machine model is the 256-bit word RAM of the cost model
  with 64 registers". Its "44 registers are resident during the batches", among them its 10 rotation
  masks, and "with the live temporaries the peak is 57 of 64 (the program's liveness count ...)". The
  cost model collision-frontier-v5 lists primitive operations and fixes no register count. Our v10
  program assumed 32 registers. Here:
  - 35 registers are resident for a whole group:
    - the 32-bit lane mask M7;
    - the twelve rotation masks of Σ0 and Σ1, and the masks of the merged σ forms (LO17, HI19, LO10,
      LO3, HI7, LO18, HI18);
    - the scalar test constants: 2^24 - 1, 63, 1 and the bitmap base;
    - the group values a, KW20 and K19, K21..K28.
    They are loaded once per group, and that is charged in the group set-up.
  - 6 loop registers: X (the seven trial indices), SEVEN7 (7 in every lane), the trial counter, the
    countdown to the next event, the constant 7 and the address of the group values.
  - The pass's own values need at most 23 registers at once. `kswar.py` computes the largest live set
    of the straight-line pass, and 35 + 6 + 23 = 64.
  - `kswar.py` chooses the resident set: constants in order of uses per pass, each kept while the
    pass still fits 64 registers. Every other group value is loaded at each use, 24 loads per pass.
  - Every out-of-line path is charged 128 for storing all 64 registers at its start and reloading
    them at its end. The out-of-line paths are a bitmap hit and an event. So the hit processing of
    Section 16 runs with the registers it had in v10.
- Lane arithmetic (Th0rgal, f310d44f). A lane addition is one 256-bit addition. `kswar.py` keeps a
  static per-lane bound for every addition and asserts that it is below 2^36, so no carry leaves a
  lane. The largest bound in the pass is 9 (2^32 - 1), the sum that gives the key; the largest lane
  value met in the checks is 0x79babd6c9. E and A of every step and the schedule words w17..w28 are
  reduced to 32 bits (AND M7) when they are formed. T1, T2, w29, w30 and the key's sum use the guard
  bits.
- Rotations: ROTR(v, r) = ((v >> r) & LO_r) ^ ((v << (32 - r)) & HI_r), 5 primitives, where LO_r keeps
  lane bits 0..31-r and HI_r keeps lane bits 32-r..31. It reads only bits 0..31 of each lane, whatever
  the guard bits hold. Σ0 and Σ1 are three rotations and two XORs, 17 primitives.
- Merged masks. Take an input whose guard bits are 0. Then v >> r holds v's bits r..31 at lane bits
  0..31-r and zeros at 32-r..35-r. And v << (32 - r) holds v's bits 0..r-1 at lane bits 32-r..31 and
  zeros at 28-r..31-r. So one mask can serve two shifted copies whose correct and zero regions cover
  all of it:
  - σ1(v) = ((v >> 17 ^ v >> 19) & LO17) ^ ((v << 15 ^ v << 13) & HI19) ^ ((v >> 10) & LO10): 12;
  - σ0(v) = ((v >> 3 ^ v >> 7) & LO3) ^ ((v << 25) & HI7) ^ ((v >> 18) & LO18) ^ ((v << 14) & HI18): 13.
  `merged()` in `kswar.py` checks the regions bit by bit, and `sg0`/`sg1` assert that every input is
  reduced.
- Ch(e,f,g) = g ^ (e & (f ^ g)) and Maj with the carried a ^ b, as in Section 16.1 (3 each). Both are
  bitwise, so they are exact in every lane.
- Bitmap test, lane by lane. First the index bits of all lanes: ks = (key >> 8) & M24x7, 3 with the
  load of M24x7. Then for lane l:
  - bi = (ks >> 36l) & (2^24 - 1): 1 for lanes 0 and 6, otherwise 2;
  - the address base + (bi >> 6): 2;
  - the load of the 64-bit bitmap word: 1;
  - (word >> (bi & 63)) & 1: 3;
  - compare and branch: 2.
  That is 71 for the seven lanes.

### 17.2 One pass: 995 primitives

`kswar.py` (Appendix D.1) generates the pass from v10's trial (`kprog.py --opt`, the same steps,
schedule words, group values and identities) with every 32-bit operation made a lane operation. It
emits C (`kswar7.h`), and `kswar.c` executes it with a counter. Steps 15..30 and the twelve schedule
words cost 924, the seven bitmap tests 71:

| add | AND | XOR | shift left | shift right | load | load (bitmap) | variable shift | compare | branch | total |
|---|---|---|---|---|---|---|---|---|---|---|
| 123 | 309 | 257 | 114 | 140 | 24 | 7 | 7 | 7 | 7 | 995 |

Of these, Σ0 and Σ1 (15 each) take 510, σ1 (11) 132 and σ0 13. There is no branch in the pass other
than the seven bitmap tests, so 995 is the count of every pass. Loop control adds 5: the countdown to
the next event (compare, branch, subtract), X += SEVEN7 and the trial counter += 7. A pass of 7 trials
therefore costs 1,000, or 142.9 per trial, against 584.6 per trial in v10.

### 17.3 Groups, events and the passes that ran

- Group set-up: v10's group head and set-up (12 + 13,349, Section 16.3); the broadcast of the 35 group
  values to seven lanes (8 each: load, three shift-OR doublings, store; 280); one load of each resident
  value (charged for all 35); the loop registers (4). In all 13,680.
- Events. `r31det3` runs its abort check after the pass at base k * 2^20, that is after trial
  k * 2^20 + 7 (k = 0..15). The SWAR loop keeps a countdown to the next event trial. The pass that
  contains that trial branches out of line: the same lane tests run with the abort check after that
  lane, and the countdown is set to the next event. The last event is the group's last trial. The
  pass at 2^24 - 1 has one valid lane; it is computed and charged in full. A full group has 17
  events, 295 primitives in all (the 16 abort checks of Section 16.3 included), plus 128 each for the
  registers, 2,471.
- The passes that ran. A group with T trials needs ceil(T / 7) passes. The run's log gives each
  thread's trial count, and thread t ran groups t, t + 12, ... (B.4). Every group has 2^24 trials,
  except that a thread's last group, if aborted, stopped after the pass at its abort check, after
  k * 2^20 + 8 trials:

| thread | trials (log) | full groups | groups | aborted group: trials |
|---|---|---|---|---|
| 0 | 8,287,944,704 | 494 | 0..5916 | |
| 1 | 8,287,944,704 | 494 | 1..5917 | |
| 2 | 8,287,944,704 | 494 | 2..5918 | |
| 3 | 8,297,381,896 | 494 | 3..5919 | 5931: 9 * 2^20 + 8 |
| 4 | 8,287,944,704 | 494 | 4..5920 | |
| 5 | 8,349,810,696 | 497 | 5..5957 | 5969: 11 * 2^20 + 8 |
| 6 | 8,290,041,864 | 494 | 6..5922 | 5934: 2 * 2^20 + 8 |
| 7 | 8,318,353,416 | 495 | 7..5935 | 5947: 13 * 2^20 + 8 |
| 8 | 8,271,167,488 | 493 | 8..5912 | |
| 9 | 8,271,167,488 | 493 | 9..5913 | |
| 10 | 8,271,167,488 | 493 | 10..5914 | |
| 11 | 8,271,167,488 | 493 | 11..5915 | |

  So the groups that ran are 0..5920 and 5921, 5922, 5923, 5933, 5935, 5945, 5957 in full, and 5931,
  5934, 5947, 5969 aborted. That is 5,932 groups and 99,492,036,640 trials, as in Section 8; 4
  aborted, as in its DET line. The passes are
  5,928 * ceil(2^24 / 7) + ceil(9,437,192 / 7) + ceil(2,097,160 / 7) + ceil(13,631,496 / 7) +
  ceil(11,534,344 / 7) = 14,207,910,288 + 5,242,887 = **14,213,153,175**. Without the split by group,
  (99,492,036,640 + 6 * 5,932) / 7 = 14,213,153,176 bounds the count.

### 17.4 Validation

`kswar.py` (output in D.4):
- 3,000 groups, of which 64 have words 0..14 drawn from all-zero and all-one words and the others are
  random. Lane 0 starts at edge values (0, 1, 7, 2^20 - 3, 2^20 + 1, 2^23 - 1, 2^24 - 15, 2^24 - 8,
  2^24 - 7) or at random. For all 21,000 lanes the key equals word 0 of the organizer reference
  core's 31-step compression, and the key and decision equal those of `kprog.py --opt`.
- On 1,000 passes, setting the bit tested by one lane turns exactly the lanes that test that bit to
  hits.
- Every addition stays within its static bound, and every pass executes exactly 995 primitives.

`kswar.c` (Appendix D.3) includes `kcount.c` with only its `main` renamed, and through it `r31det3.c`
and `sp_own.h` unchanged, with the committed seed. Per group it runs, on the same trials:
- v10's counted group set-up, compared with `r31det3`'s own;
- the counted broadcast;
- the SWAR pass;
- for every trial, `r31det3`'s own trial block (`ref_key`, verbatim) and v10's counted scalar trial
  (`klane_opt`). The SWAR lane's key must equal both, and its bitmap decision both decisions;
- for every bitmap hit, `r31det3`'s `process_hit` and kcount's counted `hit_c`, which must agree on
  every counter of the group.
The variant with every constant loaded (`kswar7_ld`) is run on the passes whose first trial is a
multiple of 2^18 and must give the same keys and decisions.

`./kswar run` replays every group that K executed, with the trials of Section 17.3. All
99,492,036,640 trials of the run pass these checks, in 14,213,153,175 passes. The summed counters equal
the run's FINAL and DET lines (Section 8):
- trials 99,492,036,640, bitmap hits 58,831,394, key-matched trials 1,376,281;
- matched records 3,061,666, V6 passes 5,992, R20 passes 1, completions 1/1, collisions 1;
- E13 draws 2,829, E15 draws 19, aborted groups 4, groups 5,932.
Group 5920 runs to its end, as it did in the run, and stores the pair of Section 4 at
n* = 99,325,680,347. Every pass costs 995 and every loop control at most 5. Every group set-up costs
13,680, the events of a group at most 295, and the lane index of a hit at most 2. `./kswar sample 96`
also runs v10's check (groups 0..3 in full and 5920 up to its stored pair), now with the SWAR pass,
together with groups 4..95. Its per-group counters equal those of Section 16.4. The outputs are in
D.4.

So the validation covers every trial of the execution. It is not a sample of it.

### 17.5 The K line

| event | count in the run (Section 8) | primitives per event | ops |
|---|---|---|---|
| pass of 7 trials: SWAR pass 995, loop control 5 | 14,213,153,175 | 1,000 | 14,213,153,175,000 |
| group: head and set-up 13,361, broadcast and resident loads 315, loop registers 4, 17 events 295, their register saves 17 * 128 | 5,932 | 16,151 | 95,807,732 |
| bitmap hit: as in 16.3 (1,642), lane index 2, register save and reload 128 | 58,831,394 | 1,772 | 104,249,230,168 |
| key-matched hits, matched records, V6 passes, the R20 pass (16.3) | | | 763,146,727 |
| table build with the SWAR scan of 18.5, s1 inverse, self-check | | | 56,032,497,606 |
| library calls and the main thread (16.3) | | | 102,400,000,000 |
| K | | | 14,476,693,857,233 |

K = ceil(14,476,693,857,233 / 2140) = **6,764,810,214** units, against v10's 27,384,016,436 (v11: 6,849,102,900).

### 17.6 Sensitivity

H2 (Section 11) lists the totals with v10's scalar passes, with every constant loaded at each use (1,292 per
pass), on a 32-register machine (1,236 per pass), with twice the pass and with twice every K line, and the
largest pass for which the claim holds. The counts are exact for the program, and the replay covers every pass
that ran, so no safety factor is applied.

## 18. The synthetic trial loops, the table scan and the yield checks re-counted (H2)

This section supports the synthetic-check and yield-check lines of Section 9 and the table-build row
of K (17.5) since v12. Each re-count is an exact counted program for the same computation, checked
against the program that ran.

### 18.1 splitmix64 with its constants as program text

`sm()` of B.4 and B.6 multiplies by the fixed constants bf58476d1ce4e5b9 and 94d049bb133111eb. In the
256-bit word RAM, z * c mod 2^64 is the sum of +-(z << i) over the non-adjacent form of c, then an AND
with 2^64 - 1. Every term is below 2^128, and the AND removes everything above bit 63. Each constant
has 23 nonzero digits, so a product costs 45 primitives: one shift per digit (none at
bit 0), one addition or subtraction per digit after the first, and the mask. v10 used the general
385-primitive product for these. The digits are part of the program text, like the shift counts.
A draw costs 101 primitives instead of v10's 783: two constant loads and two
385-primitive products, plus the same 11 other primitives. The self-check line of E.3 prints 781 for v10,
which leaves out the two loads. `scount12.c` checks both products against C's 64-bit
products on 10^6 values (all single-bit values and their complements, 0, 2^64 - 1, and pseudo-random
values) and 1,000 draws against `sm()`.

### 18.2 r % nrec by a reciprocal

The trial picks its record as r % nrec for a 64-bit draw r. Granlund and Montgomery (PLDI 1994,
Theorem 4.2) prove the following. Take N = 64, d = nrec, l = ceil(log2 d) and m = ceil(2^(N+l) / d),
so that 2^(N+l) <= m d <= 2^(N+l) + 2^l. Then floor(r / d) = floor(r m / 2^(N+l)) for every
0 <= r < 2^N. So r mod d = r - q d with q = (r m) >> (N + l); r m < 2^130 fits a 256-bit word.
- Once per run, the counted program computes l by a loop, m by a restoring division of the
  (65 + l)-bit dividend (9 per bit), and the non-adjacent digits of m and of d into lists in memory.
  It asserts the theorem's condition on m and d.
- Per trial, the two products are loops over the digit lists. Each digit costs a load of its
  position, a variable shift, an addition or subtraction, and the loop's counter, compare and
  branch; then come the shift by N + l and the subtraction. Run 3 (d = 132096; m has 11
  digits, d 2) costs 93 primitives. Run 2 (d = 224; m 23 digits, d
  2) costs 165. v10's restoring division cost 576.
- `scount12.c` checks the remainder against C's % on 2 * 10^6 values per run: powers of two,
  2^k - 1, multiples of d and their neighbours, 2^64 - 1, and pseudo-random values.

### 18.3 The 64 G16 candidates, seven per word

For each trial, `process_sim` tries k = 0..63 and stops at the first k with
s1(w18 + D18) - s1(w18) = tgt, where w18 = s1(G16[k]) + c18. The counted program does this as follows.
- Once per run it stores s1(G16[k]) in ten words, seven candidates per word in the lanes of
  Section 17.1.
- Per trial it broadcasts c18 and tgt to the seven lanes (13). It then tests one word at a time:
  - w18 = (S1G_j + c18) & M7 and its sum with D18, both reduced;
  - σ1 of each (12 each, Section 17.1);
  - the test, as s1(w18 + D18) XOR ((s1(w18) + tgt) & M7). Adding 2^32 - 1 sets bit 32 of a lane
    exactly when that lane misses;
  - an AND with the bit-32 lane mask, a compare and a branch.
- The tenth word holds candidate 63 alone, and its other lanes are forced to miss. The first word
  with a zero lane holds the first k, and that lane is read off in lane order. So the result is the
  same k as `process_sim`'s loop, or none.
- A word costs 37 primitives (39 for the tenth, with its forced lanes). A trial without a match
  costs 391 for the candidates, against about 2,300 in v10. The six loop constants are loaded once per trial, and the loop's live values
  fit 32 registers.

### 18.4 The replays

`scount12.c` (Appendix E.1) copies the lines it needs from `scount.c` verbatim (the primitives, the σ, Ch and
Maj helpers, `compress31_c`, `s1inv_c` and the reference loop `sim_ref`) and includes `r31sim3.c` unchanged; it
reads `r31sim3`'s own table, whose build is charged in the table part of the synthetic line (16.6, 18.5). The
verbatim block has one added line, the alias of `s1inv_col_c` to `r31sim3`'s columns. The once-per-run
set-up of 18.2 (the division for m and the digit lists) is charged by the formulas in `gm_setup_c`: 1,777 and
1,875 primitives. For each run it is built with that run's S (attempt 2's and attempt 3's
`sp_own.h`). Its trial loop is `scount.c`'s with 18.1-18.3 in place. On every trial it also runs
`r31sim3`'s own `sm`, `r % nrec` and candidate loop on a shadow copy of the state. It asserts the
same four draws, the same record index and the same candidate. The reference thread runs
`r31sim3`'s `simworker` loop verbatim for the same N trials, and the counters of both must agree.

| run | trials | trial loop (counted replay) | per trial | v10 / v11 |
|---|---|---|---|---|
| 2 | 275,316,736 | 345,802,476,470 | 1,256.02 | 1,745,020,550,020 (6338.23) |
| 3 | 250,544,128 | 296,672,248,975 | 1,184.11 | 1,588,088,539,519 (6338.56) |

Both replays reproduce their run's FINAL line, with 0 mismatches of draws, index or candidate on every
trial (output in E.3).

### 18.5 The table scan P1 as a 7-lane SWAR program

P1 tests every 32-bit word w three times, in B.4's order, and appends w to V8, V7 and G16:
s0(w + D8) - s0(w) = C8, s0(w + D7) - s0(w) = C7 and s1(w + D9) - s1(w) = D18. `p1swar.c` (Appendix
E.2) runs seven consecutive words per batch in the lanes of Section 17.1.
- σ0(w) and σ1(w) are computed once per batch, and each test as in 18.3. The three miss
  indicators are combined with ANDs, then a compare and a branch.
- A batch without a hit costs 91 primitives, 13.0 per word against 55 in the scalar
  scan of C.7.
- A batch with a hit (25946 of 613,566,757) reads its lanes in word order and its tests in B.4's
  order, so each list is appended in B.4's order.
- The last batch starts at 2^32 - 7, and its first three lanes, already scanned, are forced to miss.
- 12 slices are run as in C.7, and their lists are joined in slice order.
The lists equal those of B.4's loop word for word (512, 49,408 and 64 words). The scan costs
55,836,954,414 primitives, 13.0006 per word, against 236,223,301,254.

The scan replaces the P1 count in four table builds:
- K's: 56,032,497,606 with the s1 inverse, P2, sort, bitmap and self-check of C.8;
- the three synthetic runs': 55,931,461,662, 55,869,221,974 and 56,032,497,606.

### 18.6 The yield checks

The five yield checks before K (Sections 8 and 15.1) ran `r31det3 1 0` three times and `diag 1 0`
twice. `r31det3` with a time limit of 0 runs `build_s1inv`, `build_table` and `selftest`, and returns:
this is exactly the prefix of K that its counted program counts, the table-build row of 17.5.
`diag.c` is `r31det3.c` with two more loops in `build_table`, which repeat P2's loops over V8 and V7
with counters in place of record stores. Each costs at most P2's count. `diag.c` (SHA-256
acefeab6fe10b923e062968ce4074aafb9003b14cf3f74938e4e2c1f91cb691e) is `r31det3.c` with these two lines added:

```diff
--- r31det3.c
+++ diag.c
@@ -79,6 +79,8 @@
       if((E3&cm3)!=va3) continue; if((uint32_t)(IF(EB(5),E4,E3)-IF(EA(5),E4,E3))!=lhs6) continue;
       uint32_t Am1=E3-AA(3)+BS0(AA(2))+MAJ(AA(2),AA(1),A0);
       recs[nrec++]=(rec_t){Am1,A0,E3,E4,W7,W8}; } }
+  { int l1=0; for(int i=0;i<n8;i++){ uint32_t W8=V8[i]; uint32_t E4=EA(8)-AA(4)-BS1(EA(7))-IF(EA(7),EA(6),EA(5))-K[8]-W8; if((E4&cm4)!=va4) continue; l1++; if((uint32_t)(IF(EB(6),EB(5),E4)-IF(EA(6),EA(5),E4))!=lhs7) continue; } fprintf(stderr,"loop1 row4-pass=%d\n",l1);
+    int r3=0,f6=0,f7=0; for(int i=0;i<n8;i++){ uint32_t W8=V8[i]; uint32_t E4=EA(8)-AA(4)-BS1(EA(7))-IF(EA(7),EA(6),EA(5))-K[8]-W8; if((E4&cm4)!=va4) continue; if((uint32_t)(IF(EB(6),EB(5),E4)-IF(EA(6),EA(5),E4))!=lhs7) continue; f7++; for(int j=0;j<n7;j++){ uint32_t W7=V7[j]; uint32_t E3=EA(7)-AA(3)-BS1(EA(6))-IF(EA(6),EA(5),E4)-K[7]-W7; if((E3&cm3)!=va3) continue; r3++; if((uint32_t)(IF(EB(5),E4,E3)-IF(EA(5),E4,E3))==lhs6) f6++; } } fprintf(stderr,"F7-pass=%d row3-pass=%d F6-pass=%d\n",f7,r3,f6); }
   qsort(recs,nrec,sizeof(rec_t),cmprec);
   bitmap=calloc(1<<18,8); for(int i=0;i<nrec;i++){ uint32_t b=recs[i].key>>8; bitmap[b>>6]|=1ull<<(b&63); }
   fprintf(stderr,"V7=%d V8=%d G16=%d records=%d\n",n7,n8,ng16,nrec);
```
 The table build depends on
S only through P2, the sort and the bitmap. Their counts are largest for attempt 3's S (C.8, C.14:
P2 81,321,704, 63,006,824 and 702,792 for attempts 3, 1 and 2), so attempt 3's are charged for every
run, whichever S it used:

    5 * 56,032,497,606 + 2 * 2 * 81,321,704 = 280,487,774,846 ops = 131,069,054 units

v10 and v11 charged a hand bound of 723,470,929 units. The launch and library calls of these runs
stay in the H8 lump of Section 9.

### 18.7 Sensitivity

H2 (Section 11) lists the totals with each re-count of this section undone, with twice the synthetic checks and
with twice the yield checks.

## 19. The pre-construction analysis programs re-counted (H2)

This section supports the analysis line of Section 9 since v13. `pcount13.c` (Appendix F.1) writes the
five charged runs of Section 15.2 with the forms of Sections 17 and 18. It prints the same lines as
`pcount.c` (C.9) and as the originals, and those lines are compared byte for byte.

### 19.1 What changes

`pcount13.c` copies the primitives, floating-point tariffs and σ helpers of `pcount.c` (C.9) verbatim; its
probing and printing are those of C.9's `add_c`, `get_c` and `run_*`. Each change below is an identity on the
same values:
- The 2^32 scans run seven consecutive words per batch, in the lanes of Section 17.1, with σ0 and σ1
  as there. A difference x - y mod 2^32 is ((x OR 2^32) - y) AND M7, and a test x - y = c is read in
  bit 32 of (x XOR ((y + c) AND M7)) + (2^32 - 1). The last batch starts at 2^32 - 7, and its first
  three lanes, already scanned, are skipped.
- The hash index (k * 0x9e3779b1 mod 2^32) >> 7 is shift-and-add over the constant's 11 non-adjacent digits (+1 at
  bits 0, 9, 22, 29, 31; -1 at 4, 6, 11, 15, 19, 25): 22 primitives scalar instead of 38. In seven lanes each term is
  (k AND (2^(32-b) - 1)) << b, positive and negative terms are summed apart and joined as ((P + 6 * 2^32) - N) AND
  M7 (below 11 * 2^32 < 2^36), then shifted and masked: 34 for seven keys. Both are checked on 10^6 keys.
- Insertions. The keys and indices of a batch are read off lane by lane (1 or 2 primitives each).
  They are inserted with C.9's probing code in the original order: word order, and for `joint` each
  table in word order. So each table, and every floating-point sum that `joint` takes over its
  slots, is the original's. `joint` builds its two tables in two threads, each counted.
- Samples (`pany`, `pany2`).
  - The 64 candidates are computed seven per word (10 words). The words s1(G16[k]) are formed once
    per run.
  - For candidate g, its value is broadcast and compared with every earlier word. In its own word the
    lanes from g on are forced unequal. Bit 32 of (x XOR y) + (2^32 - 1) is 0 exactly when x = y, so
    g is new iff no earlier candidate equals it.
  - psum adds get(-x) of the new candidates, with the NAF hash. The original adds the same counts
    over its list of distinct values, and integer addition does not depend on the order. So psum,
    and every floating-point operation on it, is the same.
  - `pany`'s strict flag is the OR of seven-lane equality tests against mc5.
  - Every sample is also checked, uncounted, against the original's own distinct list, count and
    psum: 0 mismatches.
- `sets` and the separate G16 scan of `pany` run in 12 slices. Their lists are joined in slice
  order, as in C.7. The counted program is the single-thread program: the slices only finish the
  count sooner, and the constants that every slice loads are counted once, as one thread loads them.
- Registers (64, Section 17.1): a scan holds at most 26 constants (lane, σ and hash masks, its differences),
  4 loop registers and about 10 live words, `sets` 14 more constants; a sample holds its ten candidate words,
  15 constants and about 15 live values. Every constant is loaded, and counted, once per run or per sample.

### 19.2 Counts and outputs

| program | v10-v12b (C.9) | this filing (`pcount13`) | ratio |
|---|---|---|---|
| `sets` | 461,151,205,710 | 108,037,853,099 | 4.27 |
| `joint` | 644,688,249,115 | 267,852,965,723 | 2.41 |
| `pany` | 569,745,544,349 | 209,345,560,218 | 2.72 |
| `pany2 1 20` | 410,842,675,669 | 148,843,827,942 | 2.76 |
| `pany2 12 28` | 2,858,761,574,204 | 1,344,467,221,045 | 2.13 |
| process launch and library calls (unchanged) | 512,000,000,000 | 512,000,000,000 | |
| total | 5,457,189,249,047 | 2,590,547,428,027 | |

Every program's standard output is byte-identical to the output of `pcount.c` (C.9), which is
identical to the original program's. The comparison output:

```
sets identical
joint identical
pany identical
pany2-1-20 identical
pany2-12-28 identical
```

The analysis line of Section 9 is ceil(2,590,547,428,027 / 2140) = **1,210,536,182** units. With v12's counts
the total would be 2^34.027; with twice these counts, 2^34.016.

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

`r31sim3.c` is `r31det3.c` (B.4) with the changes below; applying the diff to B.4 gives the file with SHA-256
bd7e1281a7edbfd8b587a1d30d2345dc127182bd406dd8e28c213e0cc21ed906 (`diff -u r31det3.c r31sim3.c`).

```diff
--- r31det3.c
+++ r31sim3.c
@@ -84,22 +84,22 @@
   fprintf(stderr,"V7=%d V8=%d G16=%d records=%d\n",n7,n8,ng16,nrec);
 }
 
-typedef struct { uint64_t trials, keyhits, recs, v6, joint, both, comp_try, comp_ok, coll, it13, it15, overshoot, bmhits, groups; } ctr_t;
+typedef struct { uint64_t trials, keyhits, recs, v6, joint, both, comp_try, comp_ok, coll; } ctr_t;
 static ctr_t ctrs[64];
-static atomic_int stop_flag; static atomic_int live_threads; static pthread_mutex_t out_mu=PTHREAD_MUTEX_INITIALIZER;
+static atomic_int stop_flag; static pthread_mutex_t out_mu=PTHREAD_MUTEX_INITIALIZER;
 static FILE *outf; static atomic_uint_fast64_t total_coll;
 
 static uint64_t sm(uint64_t *s){ uint64_t z=(*s+=0x9e3779b97f4a7c15ull); z=(z^(z>>30))*0xbf58476d1ce4e5b9ull; z=(z^(z>>27))*0x94d049bb133111ebull; return z^(z>>31); }
 
 /* returns 1 if completion found; fills W[0..15] */
-static int complete(uint32_t W[16], uint32_t g, uint64_t *rs, ctr_t *cc){
+static int complete(uint32_t W[16], uint32_t g, uint64_t *rs){
   uint32_t W14=s1inv(g-W[9]-s0(W[1])-W[0]); W[14]=W14;
   if((uint32_t)(s1(W14)+W[9]+s0(W[1])+W[0])!=g) return 0;
   uint32_t b13=AA(9)+EA(9)+BS1(EA(12))+IF(EA(12),EA(11),EA(10))+K[13];
   uint32_t b13b=AB(9)+EB(9)+BS1(EB(12))+IF(EB(12),EB(11),EB(10))+K[13];
   if(b13!=b13b) return 0;
-  for(int t=0;t<(1<<22);t++){
-    cc->it13++; uint32_t E13=(uint32_t)sm(rs); uint32_t W13=E13-b13;
+  for(int t=0;t<(1<<14);t++){
+    uint32_t E13=((uint32_t)sm(rs) & ~0x10c08000u) | 0x00408000u; uint32_t W13=E13-b13;
     uint32_t A13=E13-AA(9)+BS0(AA(12))+MAJ(AA(12),AA(11),AA(10));
     uint32_t A13b=E13-AB(9)+BS0(AB(12))+MAJ(AB(12),AB(11),AB(10)); if(A13!=A13b) return 0;
     uint32_t E14=AA(10)+EA(10)+BS1(E13)+IF(E13,EA(12),EA(11))+K[14]+W14;
@@ -109,8 +109,8 @@
     if(A14!=A14b) continue;
     uint32_t f15=AA(11)+EA(11)+BS1(E14)+IF(E14,E13,EA(12))+K[15], f15b=AB(11)+EB(11)+BS1(E14b)+IF(E14b,E13,EB(12))+K[15];
     if(f15!=f15b) continue;
-    for(int u=0;u<(1<<12);u++){
-      cc->it15++; uint32_t E15=(uint32_t)sm(rs); uint32_t W15=E15-f15;
+    for(int u=0;u<(1<<8);u++){
+      uint32_t E15=((uint32_t)sm(rs) & ~0x00008004u) | 0x00000004u; uint32_t W15=E15-f15;
       uint32_t E16=AA(12)+EA(12)+BS1(E15)+IF(E15,E14,E13)+K[16]+g, E16b=AB(12)+EB(12)+BS1(E15)+IF(E15,E14b,E13)+K[16]+g+D9;
       if(E16!=E16b) continue;
       uint32_t A15=E15-AA(11)+BS0(A14)+MAJ(A14,A13,AA(12));
@@ -120,10 +120,10 @@
   return 0;
 }
 
-static int process_hit(int tid, const uint32_t m0[16], uint64_t *rs, int verbose){ int found=0;
-  ctr_t *c=&ctrs[tid]; c->bmhits++; uint32_t cv[8]; compress31(IV,m0,cv);
+static void process_hit(int tid, const uint32_t m0[16], uint64_t *rs, int verbose){
+  ctr_t *c=&ctrs[tid]; uint32_t cv[8]; compress31(IV,m0,cv);
   int lo=0,hi=nrec; while(lo<hi){int mid=(lo+hi)/2; if(recs[mid].key<cv[0]) lo=mid+1; else hi=mid;}
-  if(lo>=nrec || recs[lo].key!=cv[0]) return 0;
+  if(lo>=nrec || recs[lo].key!=cv[0]) return;
   c->keyhits++;
   for(int r=lo;r<nrec && recs[r].key==cv[0];r++){
     const rec_t *q=&recs[r]; c->recs++;
@@ -138,20 +138,20 @@
     uint32_t W[16]; for(int i=0;i<=6;i++) W[i]=Ex(i)-Ax(i-4)-Ex(i-4)-BS1(Ex(i-1))-IF(Ex(i-1),Ex(i-2),Ex(i-3))-K[i];
     W[7]=q->W7; W[8]=q->W8; for(int i=9;i<=12;i++) W[i]=S_W[i]; W[13]=W[14]=W[15]=0;
     int v6=((uint32_t)(s0(W[6]+D6)-s0(W[6]))==C6);
-    if(!v6) continue;
-    c->v6++;
     uint32_t tgt=0u-(uint32_t)(s0(W[5]+D5)-s0(W[5])); uint32_t c18=W[11]+s0(W[3])+W[2];
     int gsel=-1; for(int k=0;k<ng16;k++){ uint32_t w18=s1(G16[k])+c18; if((uint32_t)(s1(w18+D18)-s1(w18))==tgt){gsel=k;break;} }
+    if(v6) c->v6++;
     if(gsel<0) continue;
-    c->joint++; c->both++;
+    c->joint++; if(v6) c->both++;
     c->comp_try++;
     uint32_t Wc[16]; memcpy(Wc,W,sizeof W);
-    if(!complete(Wc,G16[gsel],rs,c)) { if(verbose) fprintf(stderr,"completion failed\n"); continue; }
+    if(!complete(Wc,G16[gsel],rs)) { if(verbose) fprintf(stderr,"completion failed\n"); continue; }
     c->comp_ok++;
+    if(!v6) continue;
     uint32_t Wb[16]; memcpy(Wb,Wc,sizeof Wc); Wb[5]+=D5; Wb[6]+=D6; Wb[7]+=D7; Wb[8]+=D8; Wb[9]+=D9;
     uint32_t h1[8],h2[8]; digest(m0,Wc,h1); digest(m0,Wb,h2);
     if(memcmp(h1,h2,32)==0 && memcmp(Wc,Wb,64)!=0){
-      c->coll++; atomic_fetch_add(&total_coll,1); found=1;
+      c->coll++; atomic_fetch_add(&total_coll,1);
       pthread_mutex_lock(&out_mu);
       fprintf(outf,"COLLISION tid=%d\nM0 ",tid); for(int i=0;i<16;i++) fprintf(outf,"%08x",m0[i]);
       fprintf(outf,"\nM1 "); for(int i=0;i<16;i++) fprintf(outf,"%08x",Wc[i]);
@@ -159,55 +159,81 @@
       fprintf(outf,"\nDIGEST "); for(int i=0;i<8;i++) fprintf(outf,"%08x",h1[i]); fprintf(outf,"\n"); fflush(outf);
       pthread_mutex_unlock(&out_mu);
     } else if(verbose) fprintf(stderr,"digest mismatch\n");
-    if(found) return 1;
   }
-  return found;
 }
 
 static uint64_t seed_base; static double time_limit;
-#define LANES 8
-static int NTH; static _Atomic uint64_t best_n = UINT64_MAX;
-static void *worker(void *arg){
-  int tid=(int)(intptr_t)arg; ctr_t *c=&ctrs[tid]; atomic_fetch_add(&live_threads,1);
-  uint32_t m[16];
-  for(uint64_t g=(uint64_t)tid; ; g+=(uint64_t)NTH){
-    uint64_t bn=atomic_load(&best_n);
-    if(atomic_load(&stop_flag)) break;
-    if(bn!=UINT64_MAX && g > (bn>>24)) break;
-    c->groups++; uint64_t rs=seed_base ^ (g*0x9e3779b97f4a7c15ull) ^ 0x5bd1e9955bd1e995ull;
+
+static void process_sim(int tid, const rec_t *q, const uint32_t cv[8], uint64_t *rs){
+  ctr_t *c=&ctrs[tid]; c->recs++;
+  uint32_t a[35],e[35];
+  a[IDX(-1)]=cv[0];a[IDX(-2)]=cv[1];a[IDX(-3)]=cv[2];a[IDX(-4)]=cv[3];e[IDX(-1)]=cv[4];e[IDX(-2)]=cv[5];e[IDX(-3)]=cv[6];e[IDX(-4)]=cv[7];
+  a[IDX(0)]=q->A0; for(int i=1;i<=12;i++) a[IDX(i)]=AA(i); e[IDX(3)]=q->E3; e[IDX(4)]=q->E4; for(int i=5;i<=12;i++) e[IDX(i)]=EA(i);
+  Ex(0)=Ax(0)+Ax(-4)-BS0(Ax(-1))-MAJ(Ax(-1),Ax(-2),Ax(-3));
+  Ex(1)=Ax(1)+Ax(-3)-BS0(Ax(0))-MAJ(Ax(0),Ax(-1),Ax(-2));
+  Ex(2)=Ax(2)+Ax(-2)-BS0(Ax(1))-MAJ(Ax(1),Ax(0),Ax(-1));
+  uint32_t W[16]; for(int i=0;i<=6;i++) W[i]=Ex(i)-Ax(i-4)-Ex(i-4)-BS1(Ex(i-1))-IF(Ex(i-1),Ex(i-2),Ex(i-3))-K[i];
+  W[7]=q->W7; W[8]=q->W8; for(int i=9;i<=12;i++) W[i]=S_W[i]; W[13]=W[14]=W[15]=0;
+  int v6=((uint32_t)(s0(W[6]+D6)-s0(W[6]))==C6);
+  uint32_t tgt=0u-(uint32_t)(s0(W[5]+D5)-s0(W[5])); uint32_t c18=W[11]+s0(W[3])+W[2];
+  int gsel=-1; for(int k=0;k<ng16;k++){ uint32_t w18=s1(G16[k])+c18; if((uint32_t)(s1(w18+D18)-s1(w18))==tgt){gsel=k;break;} }
+  if(v6) c->v6++;
+  if(gsel<0) return;
+  c->joint++; if(v6) c->both++;
+  c->comp_try++;
+  uint32_t Wc[16]; memcpy(Wc,W,sizeof W);
+  if(!complete(Wc,G16[gsel],rs)) return;
+  c->comp_ok++;
+  if(!v6) return;
+  /* full check of the second block from this (synthetic) chaining value */
+  uint32_t Wb[16]; memcpy(Wb,Wc,sizeof Wc); Wb[5]+=D5; Wb[6]+=D6; Wb[7]+=D7; Wb[8]+=D8; Wb[9]+=D9;
+  uint32_t o1[8],o2[8]; compress31(cv,Wc,o1); compress31(cv,Wb,o2);
+  if(memcmp(o1,o2,32)==0) c->coll++;
+}
+static void *simworker(void *arg){
+  int tid=(int)(intptr_t)arg; uint64_t rs=seed_base^(0x51ed27ull*(uint64_t)(tid+1)); ctr_t *c=&ctrs[tid];
+  while(!atomic_load(&stop_flag)){
+    for(int it=0;it<(1<<16);it++){
+      uint64_t r=sm(&rs); const rec_t *q=&recs[(uint32_t)(r%(uint64_t)nrec)];
+      uint32_t cv[8]; cv[0]=q->key; uint64_t r2=sm(&rs), r3=sm(&rs), r4=sm(&rs);
+      cv[1]=(uint32_t)(r>>32); cv[2]=(uint32_t)r2; cv[3]=(uint32_t)(r2>>32); cv[4]=(uint32_t)r3; cv[5]=(uint32_t)(r3>>32); cv[6]=(uint32_t)r4; cv[7]=(uint32_t)(r4>>32);
+      process_sim(tid,q,cv,&rs); }
+    c->trials+=1<<16; }
+  return NULL;
+}
+
+#define LANES 8
+static void *worker(void *arg){
+  int tid=(int)(intptr_t)arg; uint64_t rs=seed_base^(0x1000193ull*(uint64_t)(tid+1)); ctr_t *c=&ctrs[tid];
+  uint32_t m[16];
+  while(!atomic_load(&stop_flag)){
     for(int i=0;i<15;i++) m[i]=(uint32_t)sm(&rs);
-    uint64_t crs=seed_base ^ (g*0xd1b54a32d192ed03ull) ^ 0x2545f4914f6cdd1dull; /* completion coins */
-    uint32_t a=IV[0],b=IV[1],cc=IV[2],d=IV[3],e=IV[4],f=IV[5],gg=IV[6],h=IV[7];
-    for(int t=0;t<15;t++){ uint32_t T1=h+BS1(e)+IF(e,f,gg)+K[t]+m[t]; uint32_t T2=BS0(a)+MAJ(a,b,cc); h=gg; gg=f; f=e; e=d+T1; d=cc; cc=b; b=a; a=T1+T2; }
+    uint32_t a=IV[0],b=IV[1],cc=IV[2],d=IV[3],e=IV[4],f=IV[5],g=IV[6],h=IV[7];
+    for(int t=0;t<15;t++){ uint32_t T1=h+BS1(e)+IF(e,f,g)+K[t]+m[t]; uint32_t T2=BS0(a)+MAJ(a,b,cc); h=g; g=f; f=e; e=d+T1; d=cc; cc=b; b=a; a=T1+T2; }
     const uint32_t m16=s1(m[14])+m[9]+s0(m[1])+m[0], m18=s1(m16)+m[11]+s0(m[3])+m[2], m20=s1(m18)+m[13]+s0(m[5])+m[4];
     const uint32_t c17=m[10]+s0(m[2])+m[1], c19=m[12]+s0(m[4])+m[3], c21=m[14]+s0(m[6])+m[5], c22=s1(m20)+s0(m[7])+m[6];
     const uint32_t c23=m16+s0(m[8])+m[7], c24=s0(m[9])+m[8], c25=m18+s0(m[10])+m[9], c26=s0(m[11])+m[10];
     const uint32_t c27=m20+s0(m[12])+m[11], c28=s0(m[13])+m[12], c29=s0(m[14])+m[13], c30=m[14];
-    int aborted=0;
     for(uint32_t base=0; base < (1u<<24); base+=LANES){
       uint32_t key[LANES];
       for(int j=0;j<LANES;j++){
         uint32_t x=base+(uint32_t)j;
         uint32_t w17=s1(x)+c17, w19=s1(w17)+c19, w21=s1(w19)+c21, w22=c22+x, w23=s1(w21)+c23, w24=s1(w22)+w17+c24;
         uint32_t w25=s1(w23)+c25, w26=s1(w24)+w19+c26, w27=s1(w25)+c27, w28=s1(w26)+w21+c28, w29=s1(w27)+w22+c29, w30=s1(w28)+w23+s0(x)+c30;
-        uint32_t A=a,B=b,C=cc,D=d,E=e,F=f,G=gg,H=h,T1,T2;
+        uint32_t A=a,B=b,C=cc,D=d,E=e,F=f,G=g,H=h,T1,T2;
 #define RND(w,k) T1=H+BS1(E)+IF(E,F,G)+(k)+(w); T2=BS0(A)+MAJ(A,B,C); H=G; G=F; F=E; E=D+T1; D=C; C=B; B=A; A=T1+T2;
         RND(x,K[15]) RND(m16,K[16]) RND(w17,K[17]) RND(m18,K[18]) RND(w19,K[19]) RND(m20,K[20]) RND(w21,K[21]) RND(w22,K[22])
         RND(w23,K[23]) RND(w24,K[24]) RND(w25,K[25]) RND(w26,K[26]) RND(w27,K[27]) RND(w28,K[28]) RND(w29,K[29]) RND(w30,K[30])
         key[j]=IV[0]+A;
       }
-      for(int j=0;j<LANES;j++){ uint32_t bi=key[j]>>8; if(bitmap[bi>>6]>>(bi&63)&1){ uint32_t mm[16]; memcpy(mm,m,60); mm[15]=base+(uint32_t)j;
-          if(process_hit(tid,mm,&crs,0)){ uint64_t n=(g<<24)|(uint64_t)(base+(uint32_t)j); uint64_t cur=atomic_load(&best_n);
-            while(n<cur && !atomic_compare_exchange_weak(&best_n,&cur,n)){}
-            pthread_mutex_lock(&out_mu); fprintf(outf,"INDEX n=%llu group=%llu j=%u\n",(unsigned long long)n,(unsigned long long)g,base+(uint32_t)j); fflush(outf); pthread_mutex_unlock(&out_mu); } } }
+      for(int j=0;j<LANES;j++){ uint32_t bi=key[j]>>8; if(bitmap[bi>>6]>>(bi&63)&1){ uint32_t mm[16]; memcpy(mm,m,60); mm[15]=base+(uint32_t)j; process_hit(tid,mm,&rs,0);} }
       c->trials+=LANES;
-      if((base & 0xfffff)==0){ uint64_t bb=atomic_load(&best_n); if(atomic_load(&stop_flag) || (bb!=UINT64_MAX && g > (bb>>24))){ aborted=1; break; } }
+      if((base & 0xfffff)==0 && atomic_load(&stop_flag)) break;
     }
-    if(aborted) { c->overshoot++; break; }
   }
-  atomic_fetch_sub(&live_threads,1);
   return NULL;
 }
+
 static void selftest(void){
   /* kernel check: compare fast key against compress31 for random blocks */
   uint64_t r2=7; for(int t=0;t<2000;t++){ uint32_t m[16]; for(int i=0;i<16;i++) m[i]=(uint32_t)sm(&r2);
@@ -234,11 +260,11 @@
   if(time_limit<=0) return 0;
   outf=fopen(outp,"a");
   pthread_t th[64]; struct timespec t0,t1; clock_gettime(CLOCK_MONOTONIC,&t0);
-  NTH=nth;
-  for(int i=0;i<nth;i++) pthread_create(&th[i],0,worker,(void*)(intptr_t)i);
+  int simmode=argc>5 && strcmp(argv[5],"sim")==0;
+  for(int i=0;i<nth;i++) pthread_create(&th[i],0,simmode?simworker:worker,(void*)(intptr_t)i);
   double last=0;
   while(1){ sleep(1); clock_gettime(CLOCK_MONOTONIC,&t1); double el=(t1.tv_sec-t0.tv_sec)+(t1.tv_nsec-t0.tv_nsec)*1e-9;
-    int fin = el>=time_limit || access("STOP",F_OK)==0 || (el>2 && atomic_load(&live_threads)==0);
+    int fin = el>=time_limit || access("STOP",F_OK)==0;
     if(el-last>=30 || fin){ last=el; ctr_t s={0}; for(int i=0;i<nth;i++){ s.trials+=ctrs[i].trials; s.keyhits+=ctrs[i].keyhits; s.recs+=ctrs[i].recs; s.v6+=ctrs[i].v6; s.joint+=ctrs[i].joint; s.both+=ctrs[i].both; s.comp_try+=ctrs[i].comp_try; s.comp_ok+=ctrs[i].comp_ok; s.coll+=ctrs[i].coll; }
       printf("t=%.0f trials=%llu (2^%.3f) rate=%.3e/s keyhits=%llu rechits=%llu v6=%llu joint=%llu both=%llu comp=%llu/%llu coll=%llu\n",el,
         (unsigned long long)s.trials, s.trials? __builtin_log2((double)s.trials):0.0, s.trials/el,(unsigned long long)s.keyhits,(unsigned long long)s.recs,(unsigned long long)s.v6,(unsigned long long)s.joint,(unsigned long long)s.both,(unsigned long long)s.comp_ok,(unsigned long long)s.comp_try,(unsigned long long)s.coll);
@@ -246,9 +272,6 @@
     if(fin) break; }
   atomic_store(&stop_flag,1); for(int i=0;i<nth;i++) pthread_join(th[i],0);
   ctr_t s={0}; for(int i=0;i<nth;i++){ s.trials+=ctrs[i].trials; s.keyhits+=ctrs[i].keyhits; s.recs+=ctrs[i].recs; s.v6+=ctrs[i].v6; s.joint+=ctrs[i].joint; s.both+=ctrs[i].both; s.comp_try+=ctrs[i].comp_try; s.comp_ok+=ctrs[i].comp_ok; s.coll+=ctrs[i].coll; }
-  { uint64_t i13=0,i15=0,ov=0,bm=0,gr=0; for(int i=0;i<nth;i++){i13+=ctrs[i].it13; i15+=ctrs[i].it15; ov+=ctrs[i].overshoot; bm+=ctrs[i].bmhits; gr+=ctrs[i].groups;} uint64_t bn=atomic_load(&best_n);
-    printf("DET best_n=%llu it13=%llu it15=%llu aborted_groups=%llu bitmap_hits=%llu groups=%llu\n",(unsigned long long)bn,(unsigned long long)i13,(unsigned long long)i15,(unsigned long long)ov,(unsigned long long)bm,(unsigned long long)gr);
-    for(int i=0;i<nth;i++) printf("THREAD %d trials=%llu\n",i,(unsigned long long)ctrs[i].trials); }
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

C.3-C.5 `swar.py`, `swar_check.py`, `kpath.py` (the cross-check of Section 14.6 only)

Published in full, with their output and SHA-256, in filing 089b597d (Appendix C.3-C.5). No charge of this filing uses them.

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
(per-group lines omitted: they are those of Section 16.4 and of D.4's `./kswar sample 96`; SHA-256 of the omitted lines df092c8721d207b9dd1d1ce6b84f4f730f2c9359d3798b25cc477a42d59e28f3)
validated trials 71670492, bitmap hits 42583; worst paths: bitmap hit 1642 (binary search <= 18, observed max 18), key-matched hit 13 (counter + final loop test), record 238, V6 pass 2344 (64 candidates)
```

`./kcount`, standard error (printed by `r31det3.c`'s own `build_table` and `process_hit`):

```
V7=512 V8=49408 G16=64 records=132096
COLLISION tid=24
M0 e7f5ce551741facd279a66b68a38d7c6cc332e48ed9dd62a6b76b5f73aa91ac91ca8034eb4a9ad705b8eeceb50a7afad07617b89719682b5394303d800459adb
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

`pcount.c` (SHA-256 above) is published in full in filings 089b597d, 028aa8d0 and 2954243d (Appendix C.9). Since
v13 the analysis is charged by `pcount13.c` (Section 19, Appendix F), which copies its primitives, tariffs and
σ helpers verbatim; the outputs above are the baseline that `pcount13`'s outputs are compared with.

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

C.12 `cgfull.py`, `bbvmix.py` and `cmpz3.py` (pricing and outputs of the charged z3 runs, Section 14.4)

    4446cbd4ace6eb2f59e4cfe2fe3c6585465d1d823418ca5d40090dd449005d4b  cgfull.py
    bd6a20bd4668c79c68ba12c485431fc31f12a36badae279a9231951ca58f6427  bbvmix.py (v15: exact totals)
    ed07becd07f54088b431d17a2ec4adc16e88ddade5fef293df26298cd41158cd  cmpz3.py (H6)
    3b77db5f1a1284da476a7db857e443500b7afd19ce0df2fe4e3d235c070fff3c  run3.sh (attempt 1, callgrind)
    7d303d10558a31cbe4f42e957265887e07c4aa089590580f781ccd1478a9c999  runbbv.sh (attempts 1-3, exp-bbv)

Both use `read_dump`, `disasm` and `objkey` of `cgmix.py` (C.2) and `cost` of `a64ops.py` (C.1) and `heavy.py`
(C.11). The profiles ran in `debian:bookworm-slim` with valgrind 3.19.0 and PyPI z3-solver 4.15.4.0 (z3 SHA-256
bbea82f99718e57d...), one container per run. Attempt 1's callgrind profile is the complete profile of our v4
measurements (`run3.sh`, embedded in filing f397b3d1: the callgrind command of Section 14.4 with `--dump-line=no
--compress-strings=no --compress-pos=no` and `z3 -T:1200 -st`, a limit it did not reach); attempts 2 and 3 are
exp-bbv profiles, and attempt 1 was also profiled with exp-bbv as the check of Section 14.4 (`runbbv.sh`, embedded in
filing 89bc1467: the exp-bbv command of Section 14.4 with `z3 -st s-model<i>.smt2`, one container per attempt).

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
from its start up to and including the first control transfer, or 100 instructions, and exp-bbv counts
every executed instruction.  So a count is entries x length, except where an interval boundary splits
one execution.  This script disassembles each superblock from the executable that ran and prices every
executed instruction with heavy.cost (32-bit-operand multiplies by mul32.py, the other heavy forms by
their checked emulations, the rest by a64ops); `mean8` charges a non-multiple count at a bound (below).
`max_open` (v14) is the most superblocks mid-execution at an interval end; the exact totals (v15: `ops8_exact`,
`opsH_exact` heavy part, `ops5_exact` v5 prices) price each whole-run count as whole executions plus one partial.
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
    run, part, opn = collections.Counter(), collections.Counter(), set()
    max_open = 0

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
            run[bid] += cnt
            part[bid] = (part[bid] + cnt) % L
            (opn.add if part[bid] else opn.discard)(bid)
            if cnt % L:
                # an interval boundary split an execution (max_open): every counted instruction is charged at the
                # largest prefix mean of the run through to the next unconditional transfer, at least the
                # superblock's own mean, so the whole-run sum stays an upper bound
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
        max_open = max(max_open, len(opn))
        if nint % group == 0:
            flush()
    flush()
    ex, lib, unk = collections.Counter(), [0, 0], collections.Counter()
    for bid, n in run.items():
        ob, ins, _ = blocks[bid]
        k, r = divmod(n, len(ins))
        for j, (mn, ops) in enumerate(ins):
            m = k + (j < r)                          # executions of the j-th instruction
            c8, cl8 = heavy.cost(mn, ops)
            c5, cl5 = a64ops.cost(mn, ops)
            ex['ops8'] += m * c8
            ex['ops5'] += m * c5
            if cl8 in ('heavy', 'div'):
                ex['opsH'] += m * c8
            if 'unknown' in (cl8, cl5):
                unk[mn] += m
            if ob != 'z3.elf':
                lib[0] += m
                lib[1] += m * c8
    exact = ex['ops8']
    whole = dict(tot)
    whole['mean'] = tot['ops5'] / tot['instr']
    whole['mean8'] = tot['ops8'] / tot['instr']
    whole['max_interval_mean'] = max(r['mean'] for r in rows)
    whole['max_interval_mean8'] = max(r['mean8'] for r in rows)
    whole['bbv_intervals'] = nint
    whole['ops8_exact'] = exact + 1024 * tot['unmapped']
    whole['opsH_exact'] = ex['opsH']
    whole['ops5_exact'] = ex['ops5'] + 1024 * tot['unmapped']
    whole['unknown'] = sum(unk.values())
    whole['unknown_forms'] = dict(unk.most_common())
    whole['mean8_exact'] = whole['ops8_exact'] / tot['instr']
    whole['meanH'] = tot['opsH'] / tot['instr']
    whole['max_open'] = max_open
    whole['lib_instr'] = lib[0] / tot['instr']
    whole['lib_ops8'] = lib[1] / exact
    m = re.search(r'Total instructions: (\d+)', open(prefix + '.vg').read())
    whole['total_instructions'] = int(m.group(1)) if m else None
    whole['tail'] = whole['total_instructions'] - tot['instr'] if m else None
    whole['blocks'] = len(pcs)
    whole['nondiv_blocks'] = sum(1 for k in bad if k != 'unmapped_blocks')
    whole['bases'] = {k: hex(v) for k, v in bases.items()}
    whole['heavy_forms'] = {k: round(v) for k, v in heavyforms.most_common(40)}
    json.dump(dict(intervals=rows, whole=whole), open(outp, 'w'), indent=1)
    print(json.dumps({k: round(whole[k], 6) if isinstance(whole[k], float) else whole[k]
                      for k in ('instr', 'total_instructions', 'tail', 'unmapped', 'nondiv', 'bbv_intervals', 'mean8',
                                'mean8_exact', 'max_open', 'lib_instr', 'lib_ops8', 'ops8_exact', 'opsH_exact', 'ops5_exact',
                                'unknown')}))


if __name__ == '__main__':
    main()
```

`bbvmix.py` v15 on the same files (intervals identical to v13's); printed summaries (`ops8_exact`: the charged
total; `mean8`: split executions at their bound; `ops5_exact`: v5 prices; `opsH_exact`: heavy part):

    b2 (attempt 2): {"instr": 1474000000001, "total_instructions": 1475640959576, "tail": 1640959575, "unmapped": 42, "nondiv": 78695909951, "bbv_intervals": 737, "mean8": 5.223001, "mean8_exact": 5.211428, "max_open": 1, "lib_instr": 0.007903, "lib_ops8": 0.003465, "ops8_exact": 7681645125235, "opsH_exact": 4379758913758, "ops5_exact": 11644603098469, "unknown": 155105772}
    b3 (attempt 3): {"instr": 834000000001, "total_instructions": 834226129830, "tail": 226129829, "unmapped": 42, "nondiv": 36908576100, "bbv_intervals": 417, "mean8": 5.27454, "mean8_exact": 5.26589, "max_open": 1, "lib_instr": 0.009764, "lib_ops8": 0.004227, "ops8_exact": 4391752289750, "opsH_exact": 2519381228610, "ops5_exact": 6672603507748, "unknown": 107294550}

b1 (attempt 1, the exp-bbv check) prints 122 intervals, `max_open` 1, `mean8_exact` 5.037013. Unrecognised forms
(`unknown_forms`): `svc` 650, 1,008, 838 (b1-b3); `mrs` 42.5e6, 149.1e6, 103.6e6; scalar `ushr` 1.5e6, 6.0e6, 3.7e6;
`movi`, `cmge`, `msr` under 2,400 each.

Inputs and outputs (SHA-256, first 16 hex digits): b1.bb 6f6535acd326adbb, b1.pc 435885391d1f6794, b2.bb
ea5c75e82bfe8950, b2.pc e82343e8c15927b5, b3.bb ee250f3111600cdd, b3.pc 599396344344bcb1; b1mix.json
d17341ac5c788dc1, b2mix.json b5e6a297d2a400d0, b3mix.json 50f818dcb10eec5b.

`cmpz3.py`, run on the macOS outputs that C used (`s-out.txt`, `s-out2.txt`, `s-out3.txt`, SHA-256 92455b249d3e631f,
6651e3ce619a8472, 82607ffd5cee1fb1) against the Linux outputs: callgrind `m1.z3` (7fb43a43481f2cf4), exp-bbv `b1-3.z3`
(e69558184223cdbd, 5ab00155cb52b440, 1616bbb3cd2e4659) and the native runs of C.15 `n1-3.z3` (72ffd2f7b6f996eb,
dba07881a67f96bd, c9a5d6db5f1ff435):

```
s-out.txt model sha256 d290cf64d6f113da 30 statistics; rlimit-count 249602816 conflicts 1068222 decisions 1829611
  m1.z3 model identical statistics identical
  b1.z3 model identical statistics identical
  n1.z3 model identical statistics identical
s-out2.txt model sha256 d89d18f19200ca1a 30 statistics; rlimit-count 1200096786 conflicts 5096968 decisions 8121313
  b2.z3 model identical statistics identical
  n2.z3 model identical statistics identical
s-out3.txt model sha256 b515679ced41c8c9 30 statistics; rlimit-count 797205785 conflicts 2818639 decisions 5235640
  b3.z3 model identical statistics identical
  n3.z3 model identical statistics identical
```

```python
"""Compare z3 outputs: the model (everything before the statistics) byte for byte, and every statistic except
memory, allocation and time.  usage: cmpz3.py MACOS_OUT LINUX_OUT [LINUX_OUT ...]"""
import hashlib
import re
import sys

VOLATILE = {'max-memory', 'memory', 'num-allocs', 'time', 'total-time'}


def parse(path):
    t = open(path).read()
    i = t.index('(:')
    return t[:i], dict(re.findall(r':([a-z0-9-]+)\s+([0-9.]+)', t[i:]))


mm, ms = parse(sys.argv[1])
keys = sorted(k for k in ms if k not in VOLATILE)
print(sys.argv[1], 'model sha256', hashlib.sha256(mm.encode()).hexdigest()[:16], len(keys), 'statistics;',
      'rlimit-count', ms['rlimit-count'], 'conflicts', ms['sat-conflicts'], 'decisions', ms['sat-decisions'])
for path in sys.argv[2:]:
    lm, ls = parse(path)
    diff = [k for k in sorted(set(ms) | set(ls)) if k not in VOLATILE and ms.get(k) != ls.get(k)]
    print(' ', path, 'model identical' if lm == mm else 'MODEL DIFFERS', 'statistics identical' if not diff else diff)
```

C.13 `scount.c` (the synthetic completion check as a counted program, replayed exactly; Section 16.6)

    57d1f683e00854e1ba3bc0c7dbd4da65dd57952b5c0e228f03f79805759c9b72  scount.c
    bd7e1281a7edbfd8b587a1d30d2345dc127182bd406dd8e28c213e0cc21ed906  r31sim3.c (B.6, unchanged)
    d273c909ecab18fcad5cc3768c5b0d181f7cb3f4d9792f885b32b2a501a474de  sp_own.h of attempt 1 (written by check_s.py, B.2, from the attempt's z3 model)
    bb76cf1d3700dac3039e0c43f317110c0de75d24b3f5884af783ab0f5092dae8  sp_own.h of attempt 2 (written by check_s.py, B.2, from the attempt's z3 model)
    84003700c7015677e60700dc5c044d1c6e7c0acc652e6bf12d536f9aa5084437  sp_own.h of attempt 3 (written by check_s.py, B.2, from the attempt's z3 model)

Each run is built in a directory holding its `sp_own.h`, `r31sim3.c`, `scount.c` and the generated headers of C.6:
`cc -O2 -o scount scount.c -lpthread`, then `./scount 0` (run 1), `./scount 275316736` (run 2) and
`./scount 250544128` (run 3).

`scount.c` (SHA-256 above) is published in full in filings 089b597d, 028aa8d0 and d93038bc (Appendix C.13). Its table
build, s1 inverse and self-check are the code of `kcount.c` (C.7); their counts for each run are in C.14. Since v13
`scount12.c` (E.1) copies the lines of it that the trial loop needs verbatim.

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

C.15 `libmeasure.c` and `kmeasure.c` (retired instructions per library call, per process launch and per kernel event; Section 9, H8, H9)

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

`kmeasure.c` (H9; SHA-256 578914f43177b6ef...), `cc -O2 -o kmeasure kmeasure.c && nice -n 10 ./kmeasure` on the same
machine, 2026-10-08 18:10, while other jobs ran. Output:

```
page: map, first touch, unmap             10528 per event (16384 pages of 16384 bytes)
page: map, first touch, unmap              8871 per event (16384 pages of 16384 bytes)
page: map, first touch, unmap              8995 per event (16384 pages of 16384 bytes)
mmap 128 MB PROT_NONE + munmap             6794 per event (200)
mmap 132 KB + munmap                       6664 per event (1000)
mprotect 128 KB to read-write              2041 per event (900)
madvise 8 MB MADV_FREE                     2064 per event (1000)
open + close                             131222 per event (1000)
pread 4 KB                                 5129 per event (1000)
write 64 bytes                            42639 per event (1000)
fstat                                      3547 per event (1000)
getrlimit                                  1361 per event (1000)
sigaction                                  1554 per event (1000)
sigprocmask                                1350 per event (1000)
getentropy 16 bytes                        6045 per event (1000)
getppid                                    1118 per event (1000)
busy loop (3 per iteration): 6.12 s CPU, 19343317 kernel instructions per CPU-second
busy loop (3 per iteration): 6.06 s CPU, 6890553 kernel instructions per CPU-second
busy loop (3 per iteration): 6.12 s CPU, 21282912 kernel instructions per CPU-second
```

```c
/* kmeasure.c: retired instructions, user and kernel (proc_pid_rusage, as in libmeasure.c), per operating-system
   event of the kinds the Linux z3 runs make, and the kernel work charged to a thread that only computes (timer
   interrupts, scheduling) per CPU-second.  cc -O2 -o kmeasure kmeasure.c */
#include <fcntl.h>
#include <libproc.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/mman.h>
#include <sys/random.h>
#include <sys/resource.h>
#include <sys/stat.h>
#include <time.h>
#include <unistd.h>

static uint64_t instr(void) {
  struct rusage_info_v4 ri;
  proc_pid_rusage(getpid(), RUSAGE_INFO_V4, (rusage_info_t *)&ri);
  return ri.ri_instructions;
}
static uint64_t spin(uint64_t n) {
  uint64_t x = 1;
  for (uint64_t i = 0; i < n; i++) { x = x * 6364136223846793005ull + 1442695040888963407ull; __asm__ volatile("" : "+r"(x)); }
  return x;
}
static volatile uint64_t isink;
#define MEASURE(name, N, body) do { uint64_t t0 = instr(); for (int i_ = 0; i_ < (N); i_++) { body; } uint64_t t1 = instr(); \
  printf("%-36s %10.0f per event (%d)\n", name, (double)(t1 - t0) / (N), (N)); } while (0)

int main(void) {
  size_t pg = (size_t)getpagesize(), big = (size_t)256 << 20, mb128 = (size_t)128 << 20;
  char buf[4096]; struct stat st; struct rlimit rl; sigset_t ss; struct sigaction sa = {0};
  int fd = open("kmeasure.c", O_RDONLY), dn = open("/dev/null", O_WRONLY);
  for (int r = 0; r < 3; r++) {                 /* map, first touch of every page, unmap: per page */
    uint64_t t0 = instr();
    char *p = mmap(0, big, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANON, -1, 0);
    for (size_t i = 0; i < big; i += pg) p[i] = 1;
    munmap(p, big);
    printf("%-36s %10.0f per event (%zu pages of %zu bytes)\n", "page: map, first touch, unmap", (double)(instr() - t0) / (big / pg), big / pg, pg);
  }
  MEASURE("mmap 128 MB PROT_NONE + munmap", 200, { void *q = mmap(0, mb128, PROT_NONE, MAP_PRIVATE | MAP_ANON, -1, 0); munmap(q, mb128); });
  MEASURE("mmap 132 KB + munmap", 1000, { void *q = mmap(0, 135168, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANON, -1, 0); munmap(q, 135168); });
  { char *q = mmap(0, mb128, PROT_NONE, MAP_PRIVATE | MAP_ANON, -1, 0);
    MEASURE("mprotect 128 KB to read-write", 900, mprotect(q + (size_t)i_ * 135168, 135168, PROT_READ | PROT_WRITE)); munmap(q, mb128); }
  { char *q = mmap(0, (size_t)8 << 20, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANON, -1, 0);
    MEASURE("madvise 8 MB MADV_FREE", 1000, madvise(q, (size_t)8 << 20, MADV_FREE)); munmap(q, (size_t)8 << 20); }
  MEASURE("open + close", 1000, close(open("/dev/null", O_RDONLY)));
  MEASURE("pread 4 KB", 1000, isink += pread(fd, buf, sizeof buf, 0));
  MEASURE("write 64 bytes", 1000, isink += write(dn, buf, 64));
  MEASURE("fstat", 1000, isink += fstat(fd, &st));
  MEASURE("getrlimit", 1000, isink += getrlimit(RLIMIT_STACK, &rl));
  MEASURE("sigaction", 1000, isink += sigaction(SIGUSR1, &sa, 0));
  MEASURE("sigprocmask", 1000, isink += sigprocmask(SIG_BLOCK, 0, &ss));
  MEASURE("getentropy 16 bytes", 1000, isink += getentropy(buf, 16));
  MEASURE("getppid", 1000, isink += getppid());
  uint64_t t0 = instr(); isink = spin(1000000); uint64_t t1 = instr(); isink = spin(2000000); uint64_t t2 = instr();
  uint64_t per = ((t2 - t1) - (t1 - t0)) / 1000000;  /* loop instructions per iteration; counter overhead cancels */
  for (int r = 0; r < 3; r++) {
    struct timespec a, b; clock_gettime(CLOCK_THREAD_CPUTIME_ID, &a);
    uint64_t s0 = instr(); isink = spin(6000000000ull); uint64_t s1 = instr();
    clock_gettime(CLOCK_THREAD_CPUTIME_ID, &b);
    double cpu = (b.tv_sec - a.tv_sec) + (b.tv_nsec - a.tv_nsec) / 1e9, extra = (double)(s1 - s0) - (double)per * 6e9;
    printf("busy loop (%llu per iteration): %.2f s CPU, %.0f kernel instructions per CPU-second\n", (unsigned long long)per, cpu, extra / cpu);
  }
  return 0;
}
```

Native Linux runs (H9; the binary of 14.4, `/usr/bin/time -v strace -f -C z3 [-T:1200] -st s-model<i>.smt2` in
Docker, `runkern.sh` SHA-256 c77f44f291626ef8; outputs compared in C.12). Attempts 1-3: system calls 356, 486, 403
(brk 231, 391, 310); minor page faults 23,732, 38,684, 31,164, major 0; maximum resident set 105,116, 157,820,
130,508 KB; CPU-seconds 41.54, 223.64, 149.23.

## Appendix D. The SWAR pass of search K (Section 17)

D.1 `kswar.py` (the pass as straight-line 256-bit primitives; checks; emits `kswar7.h`, `kswar7_all_loaded.h`, `gval7.h`)

    bed94bc80ee88bc0e75d5b1df7fc99e3f1178145f372a68b4d3180ea4fe05990  kswar.py

Run as `python3 kswar.py --emit` next to `kprog.py` (C.6) and `ref_hash_functions.py`. The generated files are:

    fa91c3a8618e829add0675f90319e8217a095a2abac2cc893b09a589707c1520  kswar7.h (generated: the charged pass, 995 primitives)
    7d91402608c7abd2826b5582ee9a9d0347e86e6f21db99600f611a6a3488a4d8  kswar7_all_loaded.h (generated: every constant loaded, 1,292)
    26e6fe09731cc11b39924ce28cc42375ae87e7e4a766513932c358de742f4212  gval7.h (generated: lane masks and the broadcast group values)

```python
"""Search K's trial pass as a 7-lane 36-bit SWAR program of 256-bit word-RAM primitives.

Seven consecutive trials of one group, x = b .. b+6, sit in the lanes of one 256-bit word: lane l is
bits 36l .. 36l+35, a 32-bit value and 4 guard bits (bits 252..255 are unused and stay 0).  The pass
computes in every lane what the scalar trial of kprog.py --opt computes (v10 Appendix C.6): steps 15..30
from x to key = IV[0] + A30.  It then tests each lane's key against the 2^24-bit bitmap with scalar
primitives, in lane order, so the decisions are taken for the same trials in the same order as r31det3.

Machine: collision-frontier-v5 primitives, 1 each, on the 256-bit word RAM with 64 registers (the
machine of blake3-r2, 52bb50ee).  The loop registers, the lane masks, the scalar test constants and the
group values listed by choose_resident() are registers for the whole group; every other operand is
loaded with one counted load per use.  max_live() checks that the pass fits 64 registers.

Lane arithmetic (7 lanes of 36 bits with 4 guard bits: Th0rgal, f310d44f):
- an addition of lanes is one 256-bit addition; every addition has a static per-lane bound, asserted
  below 2^36, so no carry leaves a lane;
- a rotation by r reads bits 0..31 of each lane: ((v >> r) & LO_r) ^ ((v << (32 - r)) & HI_r), 5
  primitives; Sigma0 and Sigma1 are three rotations and two XORs, 17;
- sigma1: the right parts of ROTR17 and ROTR19 share the mask LO17 and their left parts share HI19, and
  SHR10 is (v >> 10) & LO10: 12 primitives.  sigma0: SHR3 and the right part of ROTR7 share LO3: 13.
  A shared mask is exact because the input's guard bits are 0 (merged() checks the bit regions);
- Ch(e,f,g) = g ^ (e & (f ^ g)) and Maj(a,b,c) = b ^ ((a ^ b) & (b ^ c)), with b ^ c the a ^ b of the
  previous step, as in the scalar program;
- E and A of every step and the schedule words that later enter sigma1 are reduced (AND M7).
"""
import random
import sys

import kprog
import ref_hash_functions as hf

LANES, LB = 7, 36
MOD = 1 << 256
M32 = 0xffffffff
LANE_TOP = (1 << LB) - 1
K = hf.SHA256_K
IV = hf.IV["sha256"]


def rep(v):
    return sum(v << (LB * l) for l in range(LANES))


def lo(r):
    return rep((1 << (32 - r)) - 1)                  # lane bits 0 .. 31-r


def hi(r):
    return rep(((1 << r) - 1) << (32 - r))           # lane bits 32-r .. 31


CONST = {"M7": rep(M32), "M24x7": rep((1 << 24) - 1), "SEVEN7": rep(7), "IDX7": sum(l << (LB * l) for l in range(LANES)),
         "M24": (1 << 24) - 1, "C63": 63, "C1": 1, "BM": 0}
for _r in (2, 13, 22, 6, 11, 25):
    CONST[f"LO{_r}"], CONST[f"HI{_r}"] = lo(_r), hi(_r)
CONST.update({"HI7": hi(7), "LO18": lo(18), "HI18": hi(18), "LO3": lo(3),
              "LO17": lo(17), "HI19": hi(19), "LO10": lo(10)})


def merged(terms, mask_lo, mask_hi):
    """Check that one mask serves several shifted copies of a word with zero guard bits.

    terms: list of ('R', r) for v >> r or ('L', r) for v << (32 - r); the mask keeps lane bits
    mask_lo..mask_hi.  For a lane whose guard bits are 0, v >> r holds v's bits r..31 at 0..31-r,
    zeros at 32-r..35-r and the next lane's bits above; v << (32-r) holds v's bits 0..r-1 at
    32-r..31, the guard-bit zeros of the previous lane at 28-r..31-r and other bits elsewhere.
    The shared mask is exact iff every term is correct or zero on every kept bit and keeps all of
    its own correct bits."""
    for kind, r in terms:
        if kind == "R":
            good, zero = range(0, 32 - r), range(32 - r, 36 - r)
        else:
            good, zero = range(32 - r, 32), range(28 - r, 32 - r)
        keep = range(mask_lo, mask_hi + 1)
        assert set(good) <= set(keep), (terms, kind, r)
        assert all(p in good or p in zero for p in keep), (terms, kind, r)


merged([("R", 17), ("R", 19)], 0, 14)
merged([("L", 17), ("L", 19)], 13, 31)
merged([("R", 3), ("R", 7)], 0, 28)


class SwarProg:
    """Straight-line program on 256-bit words; values are names, constants are register names."""

    def __init__(self, resident=()):
        self.ops = []
        self.n = 0
        self.resident = set(resident)
        self.bound = {}                     # name -> per-lane upper bound (clean when <= M32)
        for c in CONST:
            self.bound[c] = M32
        self.bound["X"] = M32
        self.uses = {}

    def emit(self, op, *src, bound=None):
        self.n += 1
        d = f"v{self.n}"
        self.ops.append((op, d) + src)
        if bound is not None:
            self.bound[d] = bound
        return d

    def ld(self, name):
        self.uses[name] = self.uses.get(name, 0) + 1
        if name in self.resident:
            self.bound[name] = M32
            return name
        return self.emit("ld", name, bound=M32)

    def k(self, name):
        """A constant operand: a resident register, or one counted load."""
        self.uses[name] = self.uses.get(name, 0) + 1
        if name in self.resident:
            return name
        return self.emit("ld", name, bound=M32)

    def clean(self, v):
        assert self.bound.get(v, MOD) <= M32, v

    def add(self, a, b):
        bd = self.bound[a] + self.bound[b]
        assert bd <= LANE_TOP, ("lane overflow", a, b, bd)
        return self.emit("add", a, b, bound=bd)

    def xor(self, a, b):
        bd = M32 if (self.bound.get(a, MOD) <= M32 and self.bound.get(b, MOD) <= M32) else None
        return self.emit("xor", a, b, bound=bd)

    def and_(self, a, b):
        bd = M32 if (self.bound.get(a, MOD) <= M32 or self.bound.get(b, MOD) <= M32) else None
        return self.emit("and", a, b, bound=bd)

    def andm(self, a, mask):
        return self.emit("and", a, self.k(mask), bound=M32)

    def shr(self, a, n): return self.emit("shr", a, n)
    def shl(self, a, n): return self.emit("shl", a, n)
    def mask(self, v): return self.andm(v, "M7")

    def rot(self, v, r):
        return [self.andm(self.shr(v, r), f"LO{r}"), self.andm(self.shl(v, 32 - r), f"HI{r}")]

    def xor_all(self, terms):
        acc = terms[0]
        for t in terms[1:]:
            acc = self.xor(acc, t)
        return acc

    def bs0(self, v): return self.xor_all(self.rot(v, 2) + self.rot(v, 13) + self.rot(v, 22))
    def bs1(self, v): return self.xor_all(self.rot(v, 6) + self.rot(v, 11) + self.rot(v, 25))

    def sg1(self, v):
        self.clean(v)
        r = self.andm(self.xor(self.shr(v, 17), self.shr(v, 19)), "LO17")
        l = self.andm(self.xor(self.shl(v, 15), self.shl(v, 13)), "HI19")
        s = self.andm(self.shr(v, 10), "LO10")
        return self.xor(self.xor(r, l), s)

    def sg0(self, v):
        self.clean(v)
        r = self.andm(self.xor(self.shr(v, 3), self.shr(v, 7)), "LO3")
        l7 = self.andm(self.shl(v, 25), "HI7")
        r18 = self.andm(self.shr(v, 18), "LO18")
        l18 = self.andm(self.shl(v, 14), "HI18")
        return self.xor_all([r, l7, r18, l18])

    def ch(self, e, f, g): return self.xor(g, self.and_(e, self.xor(f, g)))


def gen_pass(resident=()):
    """One pass: X (lanes x = b+l, clean) -> KEY -> seven scalar bitmap tests."""
    P = SwarProg(resident)
    X = "X"
    w = {}

    def sched(t):
        if t == 17: w[17] = P.mask(P.add(P.sg1(X), P.ld("c17")))
        elif t == 19: w[19] = P.mask(P.add(P.sg1(w[17]), P.ld("c19")))
        elif t == 21: w[21] = P.mask(P.add(P.sg1(w[19]), P.ld("c21")))
        elif t == 22: w[22] = P.mask(P.add(P.ld("c22"), X))
        elif t == 23: w[23] = P.mask(P.add(P.sg1(w[21]), P.ld("c23")))
        elif t == 24: w[24] = P.mask(P.add(P.add(P.sg1(w[22]), w[17]), P.ld("c24")))
        elif t == 25: w[25] = P.mask(P.add(P.sg1(w[23]), P.ld("c25")))
        elif t == 26: w[26] = P.mask(P.add(P.add(P.sg1(w[24]), w[19]), P.ld("c26")))
        elif t == 27: w[27] = P.mask(P.add(P.sg1(w[25]), P.ld("c27")))
        elif t == 28: w[28] = P.mask(P.add(P.add(P.sg1(w[26]), w[21]), P.ld("c28")))
        elif t == 29: w[29] = P.add(P.add(P.sg1(w[27]), w[22]), P.ld("c29k"))
        elif t == 30: w[30] = P.add(P.add(P.add(P.sg1(w[28]), w[23]), P.sg0(X)), P.ld("c30k"))

    # step 15: every term but x is a group value
    E = P.mask(P.add(P.ld("U15"), X))
    A = P.mask(P.add(P.ld("V15"), X))
    # step 16: B=a C=b D=c F=e G=f H=g
    c = P.xor(P.ld("f"), P.and_(E, P.ld("exf")))
    T1 = P.add(P.add(P.ld("P16"), P.bs1(E)), c)
    la = P.ld("a")
    xab = P.xor(A, la)
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
            key = P.mask(P.add(T1, T2))       # IV[0] is folded into c30k; E30 is not needed
        else:
            st = [P.mask(P.add(T1, T2)), Aa, Bb, Cc, P.mask(P.add(Dd, T1)), Ee, Ff, Gg]
    P.n_hash = len(P.ops)
    # bitmap test of each lane, in lane order: bit (key >> 8) of the bitmap in 64-bit words at BM
    ks = P.andm(P.shr(key, 8), "M24x7")
    P.hits = []
    for l in range(LANES):
        if l == 0: bi = P.andm(ks, "M24")
        elif l == LANES - 1: bi = P.shr(ks, LB * l)            # the top lane: nothing above it
        else: bi = P.andm(P.shr(ks, LB * l), "M24")
        addr = P.emit("add", P.k("BM"), P.shr(bi, 6))           # scalar address arithmetic
        word = P.emit("ldx", addr)
        bit = P.and_(P.emit("shrv", word, P.and_(bi, P.k("C63"))), P.k("C1"))
        hit = P.emit("cmp", bit)
        P.emit("br", hit)
        P.hits.append(hit)
    P.key = key
    return P


def run(P, G, x0, mem):
    """Counting interpreter on 256-bit words.  G: scalar group values (kprog.group_values); lanes
    hold x0 .. x0+6.  Returns (lane keys, lane hits, ops, largest lane value of any addition)."""
    R = dict(CONST)
    for name, v in G.items():
        R[name] = rep(v)
    R["X"] = sum((x0 + l) << (LB * l) for l in range(LANES))
    ops, top = 0, 0
    for op in P.ops:
        o, d, *s = op
        ops += 1
        if o == "ld": R[d] = R[s[0]]
        elif o == "add":
            R[d] = (R[s[0]] + R[s[1]]) % MOD
            if P.bound.get(d) is not None:     # a lane addition (the address additions are scalar)
                assert R[d] >> (LB * LANES) == 0
                top = max(top, max((R[d] >> (LB * l)) & LANE_TOP for l in range(LANES)))
        elif o == "and": R[d] = R[s[0]] & R[s[1]]
        elif o == "or": R[d] = R[s[0]] | R[s[1]]
        elif o == "xor": R[d] = R[s[0]] ^ R[s[1]]
        elif o == "shr": R[d] = R[s[0]] >> s[1]
        elif o == "shl": R[d] = (R[s[0]] << s[1]) % MOD
        elif o == "shrv": R[d] = R[s[0]] >> R[s[1]]
        elif o == "ldx": R[d] = mem.get(R[s[0]], 0)
        elif o == "cmp": R[d] = int(R[s[0]] != 0)
        elif o == "br": pass
        else: raise ValueError(o)
    keys = [(R[P.key] >> (LB * l)) & M32 for l in range(LANES)]
    return keys, [R[h] for h in P.hits], ops, top


LOOP_REGS = 6          # X, SEVEN7, the trial counter, the countdown, the constant 7, the group-value pointer


def max_live(P):
    """Registers needed: resident registers + loop registers + the largest live set of the pass."""
    last = {}
    for i, (o, d, *s) in enumerate(P.ops):
        for v in s:
            if isinstance(v, str) and v.startswith("v"):
                last[v] = i
    live, peak = set(), 0
    for i, (o, d, *s) in enumerate(P.ops):
        if d in last:
            live.add(d)
        peak = max(peak, len(live))
        for v in s:
            if isinstance(v, str) and last.get(v) == i:
                live.discard(v)
    return len(P.resident) + LOOP_REGS + peak, peak


def choose_resident(nreg=64):
    """Constants by uses per pass, most used first, while the pass fits nreg registers."""
    base = gen_pass(())
    order = sorted(base.uses, key=lambda n: (-base.uses[n], n))
    chosen = []
    for name in order:
        trial = gen_pass(chosen + [name])
        if max_live(trial)[0] <= nreg:
            chosen.append(name)
    return chosen


def histogram(P):
    h = {}
    for o, *_ in P.ops:
        h[o] = h.get(o, 0) + 1
    return h


C_OP = {"add": "VADD", "and": "VAND", "or": "VOR", "xor": "VXOR", "shr": "VSHR", "shl": "VSHL"}


def cname(v, P):
    if v == "X": return "X"
    if v in CONST: return f"K_{v}"
    if v in P.resident: return f"G7->{v}"
    return v


def emit_c(P, fname):
    out = [f"/* generated by kswar.py: {len(P.ops)} primitives per pass of 7 trials "
           f"({P.n_hash} to the key, {len(P.ops) - P.n_hash} for the seven bitmap tests); "
           f"resident: {' '.join(sorted(P.resident))} */",
           f"static inline void {fname}(const gval7_t *G7, V X, const uint64_t *bm, V *keyout, int hit[7]) {{"]
    hi_ = 0
    for o, d, *s in P.ops:
        a = [cname(x, P) if isinstance(x, str) else x for x in s]
        if o == "ld":
            src = f"K_{s[0]}" if s[0] in CONST else f"G7->{s[0]}"
            out.append(f"  V {d} = VLD({src});")
        elif o in ("shr", "shl"): out.append(f"  V {d} = {C_OP[o]}({a[0]}, {a[1]});")
        elif o == "shrv": out.append(f"  V {d} = VSHRV({a[0]}, {a[1]});")
        elif o == "ldx": out.append(f"  V {d} = VLDX(bm, {a[0]});")
        elif o == "cmp": out.append(f"  int {d} = VCMPNZ({a[0]});")
        elif o == "br": out.append(f"  VBR(); hit[{hi_}] = {a[0]};"); hi_ += 1
        else: out.append(f"  V {d} = {C_OP[o]}({a[0]}, {a[1]});")
    out.append(f"  *keyout = {cname(P.key, P)};")
    out.append("}")
    return "\n".join(out) + "\n"


def main():
    nreg = 64
    resident = choose_resident(nreg)
    P = gen_pass(resident)
    regs, peak = max_live(P)
    scalar = kprog.gen_lane_opt()
    rng = random.Random(20261008)
    groups = 3000
    top = 0
    edge = [0, 1, 7, (1 << 20) - 3, (1 << 20) + 1, (1 << 23) - 1, (1 << 24) - 15, (1 << 24) - 8, (1 << 24) - 7]
    for i in range(groups):
        m = [rng.getrandbits(32) for _ in range(15)]
        if i < 64:
            m = [(0xffffffff if (i >> (j % 6)) & 1 else 0) for j in range(15)]   # extreme words
        G = kprog.group_values(m)
        x0 = edge[i % len(edge)] if i < 2 * len(edge) else rng.randrange(0, (1 << 24) - 6)
        keys, hits, ops, t = run(P, G, x0, {})
        top = max(top, t)
        assert ops == len(P.ops)
        for l in range(LANES):
            x = x0 + l
            block = b"".join(v.to_bytes(4, "big") for v in m + [x])
            want = hf._compress("sha256", tuple(IV), block, 31)[0]
            assert keys[l] == want, (i, l, hex(keys[l]), hex(want))
            ks, hs, _ = kprog.run(scalar, G, x, {})
            assert (ks, hs) == (keys[l], hits[l] == 1), (i, l)
        assert hits == [0] * LANES
        if i < 1000:                       # set the bit tested by one lane: exactly that decision flips
            l = rng.randrange(LANES)
            bi = keys[l] >> 8
            mem = {bi >> 6: 1 << (bi & 63)}
            k2, h2, _, _ = run(P, G, x0, mem)
            want_h = [int(((keys[j] >> 8) >> 6) == (bi >> 6) and ((keys[j] >> 8) & 63) == (bi & 63)) for j in range(LANES)]
            assert k2 == keys and h2 == want_h and h2[l] == 1, (i, l)
    h = histogram(P)
    print(f"pass: {len(P.ops)} primitives per 7 trials ({P.n_hash} steps 15..30 and schedule, "
          f"{len(P.ops) - P.n_hash} bitmap tests); {groups} random groups x 7 lanes match the organizer "
          f"reference core and kprog.py --opt (key and decision); largest lane value of any addition "
          f"{top:#x} < 2^36")
    print(f"registers: {regs} of {nreg} ({len(P.resident)} resident, {LOOP_REGS} loop, peak live {peak})")
    print("resident:", " ".join(resident))
    print("histogram", dict(sorted(h.items())))
    unres = gen_pass(())
    print(f"variant with every constant loaded at each use: {len(unres.ops)} per pass "
          f"(registers {max_live(unres)[0]})")
    if "--emit" in sys.argv:
        with open("kswar7.h", "w") as fh:
            fh.write(emit_c(P, "kswar7"))
        with open("kswar7_all_loaded.h", "w") as fh:
            fh.write(emit_c(unres, "kswar7_ld"))
        names = list(kprog.GROUP_NAMES)
        with open("gval7.h", "w") as fh:
            fh.write("/* generated by kswar.py: the group values broadcast to seven lanes */\n"
                     "typedef struct { V " + ", ".join(names) + "; } gval7_t;\n")
            for c, v in CONST.items():
                limbs = [(v >> (64 * j)) & ((1 << 64) - 1) for j in range(4)]
                fh.write(f"static const V K_{c} = {{{{" + ", ".join(f"0x{x:016x}ull" for x in limbs) + "}};\n")


if __name__ == "__main__":
    main()
```

D.2 `w256.h` (256-bit words as four 64-bit limbs; one count per primitive)

    6e642a27d4f9b888501169aa9597a47fd97053f495d8fce53c4823d784703c33  w256.h

```c
/* w256.h: 256-bit words as four 64-bit limbs, with one count per primitive (OPS of kcount.c). */
typedef struct { uint64_t w[4]; } V;

static inline V v_add(V a, V b) {
  V r; unsigned __int128 c = 0;
  for (int i = 0; i < 4; i++) { c += (unsigned __int128)a.w[i] + b.w[i]; r.w[i] = (uint64_t)c; c >>= 64; }
  return r;
}
static inline V v_sub(V a, V b) {
  V r; unsigned __int128 br = 0;
  for (int i = 0; i < 4; i++) { unsigned __int128 d = (unsigned __int128)a.w[i] - b.w[i] - br; r.w[i] = (uint64_t)d; br = (d >> 64) & 1; }
  return r;
}
static inline V v_shr(V a, int n) {
  V r = {{0, 0, 0, 0}}; int q = n >> 6, s = n & 63;
  for (int i = 0; i + q < 4; i++) {
    uint64_t lo = a.w[i + q] >> s, hi = (s && i + q + 1 < 4) ? a.w[i + q + 1] << (64 - s) : 0;
    r.w[i] = lo | hi;
  }
  return r;
}
static inline V v_shl(V a, int n) {
  V r = {{0, 0, 0, 0}}; int q = n >> 6, s = n & 63;
  for (int i = 3; i - q >= 0; i--) {
    uint64_t hi = a.w[i - q] << s, lo = (s && i - q - 1 >= 0) ? a.w[i - q - 1] >> (64 - s) : 0;
    r.w[i] = hi | lo;
  }
  return r;
}
static inline V v_of(uint64_t x) { V r = {{x, 0, 0, 0}}; return r; }
static inline int v_nz(V a) { return (a.w[0] | a.w[1] | a.w[2] | a.w[3]) != 0; }

static inline V VADD(V a, V b) { OPS++; return v_add(a, b); }
static inline V VSUB(V a, V b) { OPS++; return v_sub(a, b); }
static inline V VAND(V a, V b) { OPS++; V r; for (int i = 0; i < 4; i++) r.w[i] = a.w[i] & b.w[i]; return r; }
static inline V VOR(V a, V b)  { OPS++; V r; for (int i = 0; i < 4; i++) r.w[i] = a.w[i] | b.w[i]; return r; }
static inline V VXOR(V a, V b) { OPS++; V r; for (int i = 0; i < 4; i++) r.w[i] = a.w[i] ^ b.w[i]; return r; }
static inline V VSHR(V a, int n) { OPS++; return v_shr(a, n); }
static inline V VSHL(V a, int n) { OPS++; return v_shl(a, n); }
static inline V VSHRV(V a, V n) { OPS++; return v_shr(a, (int)n.w[0]); }
static inline V VLD(V v) { OPS++; return v; }
static inline V VLDX(const uint64_t *bm, V a) { OPS++; return v_of(bm[a.w[0]]); }
static inline int VCMPNZ(V a) { OPS++; return v_nz(a); }
static inline void VBR(void) { OPS++; }
```

D.3 `kswar.c` (the passes counted and checked against `r31det3.c` and `kcount.c`)

    22c360a853ff61eff01a98164a832869478b520d321d57a83dc680e7876837c1  kswar.c
    9541ae71e67da67a2084012a0e09622c9cf9fcfae1717919452aed2fc10d1a0e  kcount.c (C.7, unchanged)
    d7bab364ff5e38f27c3f283dc8e58f0657a5b1a8abe2f98723f0903cab2a792b  kcount_lib.c (kcount.c with main renamed by the sed line in kswar.c)
    29f4a1900e293efd2459cac87ed197c8176f20b763b92663da19dea3c3140d3e  r31det3.c (B.4, unchanged)
    84003700c7015677e60700dc5c044d1c6e7c0acc652e6bf12d536f9aa5084437  sp_own.h (B.5, unchanged)

Build and run with the generated headers of C.6 and D.1: `cc -O2 -o kswar kswar.c -lpthread`, then
`./kswar sample 96` and `./kswar run` (Apple clang 21, 12 threads; 31.45 s and 25.8 min).

```c
/* kswar.c: search K's trial passes as the 7-lane SWAR program of kswar.py (kswar7.h), counted, and
   checked against r31det3.c (B.4) and the scalar counted program of kcount.c (C.7).

   kcount_lib.c is kcount.c with its main renamed, so that its counted table, group set-up and hit
   processing and the r31det3.c it includes are available here unchanged:
     sed 's/^int main(int argc, char \*\*argv) {$/int kcount_main(int argc, char **argv) {/' kcount.c > kcount_lib.c

   A group runs the trials r31det3 runs, in the same order: batches of 7 consecutive trials, lane l of
   the batch at b being trial b + l.  For every trial the SWAR lane's key and bitmap decision are
   compared with r31det3's own trial block (ref_key, verbatim in kcount.c) and with the counted scalar
   trial klane_opt (v10's charged program); every bitmap hit is processed by r31det3's process_hit and
   by kcount.c's counted hit_c, which must agree on every counter.

   Loop control of a pass (counted): the countdown to the next event (cd = cd - 7, compare, branch),
   X += SEVEN7, trials += 7.  Events are the 16 checkpoints of r31det3 (after trial k * 2^20 + 7, where
   r31det3 runs its abort check) and the group's last trial; the event batch runs the same lane tests
   with the abort check after the event lane.  Event handling is charged per group.

   cc -O2 -o kswar kswar.c -lpthread
   ./kswar sample N   groups 0..N-1 in full and group 5920 up to its stored pair (the v10 check, extended)
   ./kswar run        every group of the K run with the trials it executed (Section 8 and the per-thread
                      counts of its log): groups 0..5920, 5921, 5922, 5923, 5933, 5935, 5945 and 5957 in full,
                      and the four aborted groups 5931, 5934, 5947, 5969 up to their abort (k * 2^20 + 8
                      trials, k = 9, 2, 13, 11); the summed counters must equal the run's FINAL and DET lines.
   12 worker threads; each group's counters are compared with r31det3's on that group. */
#include "kcount_lib.c"
#include "w256.h"
#include "gval7.h"
#include "kswar7.h"
#include "kswar7_all_loaded.h"

static const W CSEVEN = 7;

/* broadcast of one group value to the seven lanes: load, three shift-OR doublings (lanes 0-1, 0-3,
   0-6; lane 3 is written twice with the same value), store: 8 primitives */
static V bcast_c(uint32_t v) {
  V x = VLD(v_of(v));
  V r1 = VOR(x, VSHL(x, 36)), r2 = VOR(r1, VSHL(r1, 72));
  V r3 = VOR(r2, VSHL(r2, 108)); OPS++;               /* the store */
  return r3;
}
static void gval7_c(const gval_t *G, gval7_t *G7) {
#define B7(f) G7->f = bcast_c(G->f)
  B7(U15); B7(V15); B7(a); B7(b); B7(c); B7(e); B7(f); B7(ab); B7(P16); B7(P17); B7(P18); B7(KW20);
  B7(c17); B7(c19); B7(c21); B7(c22); B7(c23); B7(c24); B7(c25); B7(c26); B7(c27); B7(c28); B7(c29k); B7(c30k);
  B7(axb); B7(exf); B7(K19); B7(K21); B7(K22); B7(K23); B7(K24); B7(K25); B7(K26); B7(K27); B7(K28);
#undef B7
  OPS += 35;                                          /* resident registers: one load per group (charged for all 35) */
}
static uint32_t lane32(V v, int l) { return (uint32_t)(v_shr(v, 36 * l).w[0] & 0xffffffffu); }

typedef struct { uint64_t g; uint32_t jend; int tid; hstat_t hs; ctr_t ref; uint64_t trials, batches, pass_min, pass_max,
                 ld_min, ld_max, ctl_min, ctl_max, group_ops, event_ops, events, hitx_ops, found, nfound; int full; } sv_t;

static void *swar_worker(void *arg) {
  sv_t *v = arg; OPS = 0;
  uint32_t m[15], mr[15]; gval_t G; gval7_t G7; refg_t R; uint64_t crs, crs_ref;
  uint64_t g0 = OPS;
  group_head_c(v->g); gsetup_c(v->g, m, &G, &crs);
  ref_group(v->g, mr, &R, &crs_ref);
  assert(memcmp(m, mr, 60) == 0 && crs == crs_ref);
  gval7_c(&G, &G7);
  /* loop registers: X = lanes 0..6 (one load), trials = 0, cd = 8 trials to the first event, 16 events left */
  V X = VLD(K_IDX7);
  W trials = LD(0), cd = LD(8), ev = LD(17);
  v->group_ops = OPS - g0;
  v->pass_min = v->ld_min = v->ctl_min = UINT64_MAX;
  memset(&ctrs[v->tid], 0, sizeof(ctr_t));
  uint64_t crs_c = crs; int done = 0;
  for (uint32_t b = 0; b < v->jend && !done; b += 7) {
    uint64_t c0 = OPS, ev_ops = 0;
    W nev = CMPLT(CSEVEN, cd); BR();                       /* cd = trials up to and including the next event trial */
    int elane = -1;
    if (nev) cd = SUB(cd, CSEVEN);
    else {                                             /* out of line: the event lane, abort check, next event */
      uint64_t e0 = OPS;
      W el = SUB(cd, C1); elane = (int)(uint64_t)el;
      ev = SUB(ev, C1); W last = CMPEQ(ev, 0); BR();
      if (!last) { abort_check_c(v->g); W nx = CMPEQ(ev, C1); BR(); cd = ADD(SUB(cd, CSEVEN), nx ? LD((1u << 20) - 8) : LD(1u << 20)); }
      else trials = ADD(SUB(trials, CSEVEN), ADD(el, C1));  /* the end batch counts only its valid lanes */
      uint32_t et = b + (uint32_t)elane;
      assert((last && et == (1u << 24) - 1) || (!last && (et & 0xfffff) == 7));
      ev_ops = OPS - e0; v->event_ops += ev_ops; v->events++;
    }
    uint64_t ctl = OPS - c0 - ev_ops;
    V KEY; int hit[7];
    uint64_t p0 = OPS;
    kswar7(&G7, X, bitmap_c, &KEY, hit);
    uint64_t po = OPS - p0;
    if (po < v->pass_min) v->pass_min = po;
    if (po > v->pass_max) v->pass_max = po;
    if ((b & 0x3ffff) == 0) {                          /* every 2^18/7th batch: the all-loaded variant, same keys and decisions */
      V K2; int h2[7]; uint64_t l0 = OPS; kswar7_ld(&G7, X, bitmap_c, &K2, h2); uint64_t lo_ = OPS - l0; OPS = l0;
      if (lo_ < v->ld_min) v->ld_min = lo_;
      if (lo_ > v->ld_max) v->ld_max = lo_;
      assert(memcmp(&K2, &KEY, sizeof(V)) == 0 && memcmp(h2, hit, sizeof hit) == 0);
    }
    for (int l = 0; l < 7 && !done; l++) {
      uint32_t x = b + (uint32_t)l;
      if (x >= v->jend) break;                         /* past the group's last trial (the end batch) */
      uint32_t kr = ref_key(&R, x), ks = lane32(KEY, l), kc;
      uint64_t s0_ = OPS; int hc = klane_opt(&G, (W)x, bitmap_c, &kc); OPS = s0_;
      uint32_t bi = kr >> 8; int hit_ref = (int)(bitmap[bi >> 6] >> (bi & 63) & 1);
      assert(ks == kr && kc == kr && hit[l] == hit_ref && hc == hit_ref);
      v->trials++;
      if (hit[l]) {
        uint64_t h0 = OPS;
        W xe = l == 0 ? AND((W)X.w[0], M) : (W)lane32(VAND(VSHR(X, 36 * l), K_M7), 0);   /* x of lane l: 1 or 2 */
        assert((uint32_t)xe == x);
        v->hitx_ops += OPS - h0;
        uint32_t mm[16]; memcpy(mm, mr, 60); mm[15] = x;
        int fr = process_hit(v->tid, mm, &crs_ref, 0);
        int fc = hit_c(m, x, &crs_c, &v->hs);
        assert(fr == fc);
        if (fr) { v->found = x; v->nfound++; if (!v->full) done = 1; }
      }
    }
    uint64_t t0 = OPS;
    X = VADD(X, K_SEVEN7); trials = ADD(trials, CSEVEN);
    ctl += OPS - t0;
    if (ctl < v->ctl_min) v->ctl_min = ctl;
    if (ctl > v->ctl_max) v->ctl_max = ctl;
    v->batches++;
  }
  v->ref = ctrs[v->tid];
  return NULL;
}

static sv_t *JOBS; static int NJOBS; static _Atomic int NEXT;
static void *pool_worker(void *arg) {
  int tid = 20 + (int)(intptr_t)arg;
  for (;;) { int i = atomic_fetch_add(&NEXT, 1); if (i >= NJOBS) break; JOBS[i].tid = tid; swar_worker(&JOBS[i]); }
  return NULL;
}

int main(int argc, char **argv) {
  if (argc < 2) return 64;
  int full = !strcmp(argv[1], "run");
  seed_base = 0xdfafc947679ebe06ull;                  /* committed seed of K (Appendix A.2) */
  outf = fopen("kswar-collisions.txt", "w");
  build_s1inv(); build_table();
  build_table_c();
  printf("table: records=%d, bitmap identical to build_table\n", nrec_c);
  build_s1inv_c();
  RT = recs;
  if (full) {
    static const uint64_t extra_full[] = {5921, 5922, 5923, 5933, 5935, 5945, 5957};
    static const uint64_t ab_g[] = {5931, 5934, 5947, 5969}; static const uint32_t ab_k[] = {9, 2, 13, 11};
    NJOBS = 5921 + 7 + 4; JOBS = calloc(NJOBS, sizeof(sv_t)); int n = 0;
    for (uint64_t g = 0; g <= 5920; g++) { JOBS[n].g = g; JOBS[n].jend = 1u << 24; JOBS[n].full = 1; n++; }
    for (int i = 0; i < 7; i++) { JOBS[n].g = extra_full[i]; JOBS[n].jend = 1u << 24; JOBS[n].full = 1; n++; }
    for (int i = 0; i < 4; i++) { JOBS[n].g = ab_g[i]; JOBS[n].jend = (ab_k[i] << 20) + 8; JOBS[n].full = 1; n++; }
  } else {
    int NG = argc > 2 ? atoi(argv[2]) : 4;
    NJOBS = NG + 1; JOBS = calloc(NJOBS, sizeof(sv_t));
    for (int i = 0; i < NG; i++) { JOBS[i].g = (uint64_t)i; JOBS[i].jend = 1u << 24; }
    JOBS[NG].g = 5920; JOBS[NG].jend = 4561628u;
  }
  pthread_t th[12]; for (int w = 0; w < 12; w++) pthread_create(&th[w], 0, pool_worker, (void *)(intptr_t)w);
  for (int w = 0; w < 12; w++) pthread_join(th[w], 0);
  uint64_t T = 0, P = 0, pmin = UINT64_MAX, pmax = 0, cmin = UINT64_MAX, cmax = 0, gmax = 0, emax = 0, lmin = UINT64_MAX, lmax = 0, xmax = 0, ab = 0;
  hstat_t S = {0}; ctr_t RS = {0};
  for (int i = 0; i < NJOBS; i++) {
    sv_t *v = &JOBS[i]; ctr_t *r = &v->ref; hstat_t *h = &v->hs;
    assert(h->bmhits == r->bmhits && h->keyhits == r->keyhits && h->recs == r->recs && h->v6 == r->v6 && h->joint == r->joint &&
           h->it13 == r->it13 && h->it15 == r->it15 && h->coll == r->coll && v->trials == v->jend);
    if (v->g < 4 || v->g >= 5920)
      printf("group %llu: trials %llu, batches %llu, pass %llu..%llu, control %llu..%llu, set-up %llu, events %llu (%llu ops); "
             "hits %llu/%llu keyhits %llu/%llu recs %llu/%llu v6 %llu/%llu joint %llu/%llu it13 %llu/%llu it15 %llu/%llu coll %llu/%llu\n",
        (unsigned long long)v->g, (unsigned long long)v->trials, (unsigned long long)v->batches,
        (unsigned long long)v->pass_min, (unsigned long long)v->pass_max, (unsigned long long)v->ctl_min, (unsigned long long)v->ctl_max,
        (unsigned long long)v->group_ops, (unsigned long long)v->events, (unsigned long long)v->event_ops,
        (unsigned long long)h->bmhits, (unsigned long long)r->bmhits, (unsigned long long)h->keyhits, (unsigned long long)r->keyhits,
        (unsigned long long)h->recs, (unsigned long long)r->recs, (unsigned long long)h->v6, (unsigned long long)r->v6,
        (unsigned long long)h->joint, (unsigned long long)r->joint, (unsigned long long)h->it13, (unsigned long long)r->it13,
        (unsigned long long)h->it15, (unsigned long long)r->it15, (unsigned long long)h->coll, (unsigned long long)r->coll);
    T += v->trials; P += v->batches; if (v->jend != (1u << 24) && v->g != 5920) ab++;
    S.bmhits += h->bmhits; S.keyhits += h->keyhits; S.recs += h->recs; S.v6 += h->v6; S.joint += h->joint; S.comp_ok += h->comp_ok;
    S.coll += h->coll; S.it13 += h->it13; S.it15 += h->it15;
    RS.bmhits += r->bmhits; RS.keyhits += r->keyhits; RS.recs += r->recs; RS.v6 += r->v6; RS.joint += r->joint; RS.comp_try += r->comp_try;
    RS.comp_ok += r->comp_ok; RS.coll += r->coll; RS.it13 += r->it13; RS.it15 += r->it15;
    if (v->pass_min < pmin) pmin = v->pass_min;
    if (v->pass_max > pmax) pmax = v->pass_max;
    if (v->ctl_min < cmin) cmin = v->ctl_min;
    if (v->ctl_max > cmax) cmax = v->ctl_max;
    if (v->ld_min < lmin) lmin = v->ld_min;
    if (v->ld_max > lmax) lmax = v->ld_max;
    if (v->group_ops > gmax) gmax = v->group_ops;
    if (v->event_ops > emax) emax = v->event_ops;
    if (h->bmhits && (v->hitx_ops + h->bmhits - 1) / h->bmhits > xmax) xmax = (v->hitx_ops + h->bmhits - 1) / h->bmhits;
    if (h->coll) {
      printf("stored pair reproduced in group %llu: n = %llu\nM1  ", (unsigned long long)v->g, (unsigned long long)((v->g << 24) | v->found));
      for (int j = 0; j < 16; j++) printf("%08x", h->M1[j]);
      printf("\nM1' "); for (int j = 0; j < 16; j++) printf("%08x", h->M1b[j]);
      printf("\n");
    }
  }
  printf("groups %d, trials %llu in %llu batches; every key and bitmap decision equal to r31det3's trial block and to klane_opt; "
         "every group's hit counters equal to process_hit's\n", NJOBS, (unsigned long long)T, (unsigned long long)P);
  printf("counted: bitmap_hits=%llu keyhits=%llu rechits=%llu v6=%llu joint=%llu comp=%llu coll=%llu it13=%llu it15=%llu\n",
         (unsigned long long)S.bmhits, (unsigned long long)S.keyhits, (unsigned long long)S.recs, (unsigned long long)S.v6,
         (unsigned long long)S.joint, (unsigned long long)S.comp_ok, (unsigned long long)S.coll, (unsigned long long)S.it13, (unsigned long long)S.it15);
  printf("pass %llu..%llu, all-loaded pass %llu..%llu, loop control %llu..%llu, group set-up with broadcast %llu (max), events per group %llu ops (max), lane index per hit <= %llu\n",
         (unsigned long long)pmin, (unsigned long long)pmax, (unsigned long long)lmin, (unsigned long long)lmax,
         (unsigned long long)cmin, (unsigned long long)cmax, (unsigned long long)gmax, (unsigned long long)emax, (unsigned long long)xmax);
  if (full) {
    /* the run's own log (Section 8): FINAL and DET lines */
    assert(T == 99492036640ull && S.keyhits == 1376281 && S.recs == 3061666 && S.v6 == 5992 && S.joint == 1 && RS.comp_try == 1 &&
           S.comp_ok == 1 && S.coll == 1 && S.it13 == 2829 && S.it15 == 19 && S.bmhits == 58831394 && ab == 4 && NJOBS == 5932);
    printf("equal to the K run's log: FINAL trials=99492036640 keyhits=1376281 rechits=3061666 v6=5992 joint=1 both=1 comp=1/1 coll=1; "
           "DET it13=2829 it15=19 aborted_groups=4 bitmap_hits=58831394 groups=5932\n");
  }
  return 0;
}
```

D.4 Output (2026-10-08)

`python3 kswar.py --emit`:

```
pass: 995 primitives per 7 trials (924 steps 15..30 and schedule, 71 bitmap tests); 3000 random groups x 7 lanes match the organizer reference core and kprog.py --opt (key and decision); largest lane value of any addition 0x79babd6c9 < 2^36
registers: 64 of 64 (35 resident, 6 loop, peak live 23)
resident: M7 HI11 HI13 HI2 HI22 HI25 HI6 LO11 LO13 LO2 LO22 LO25 LO6 HI19 LO10 LO17 BM C1 C63 M24 a HI18 HI7 K19 K21 K22 K23 K24 K25 K26 K27 K28 KW20 LO18 LO3
histogram {'add': 123, 'and': 309, 'br': 7, 'cmp': 7, 'ld': 24, 'ldx': 7, 'shl': 114, 'shr': 140, 'shrv': 7, 'xor': 257}
variant with every constant loaded at each use: 1292 per pass (registers 30)
```

`./kswar sample 96` (groups 0..95 and group 5920 up to n*; 1,615,174,364 trials, all checks passed, the stored pair
reproduced): its standard output has SHA-256 cdb33c77bbe62403993c52afa91e77cde78d7be4745d81ff45e7f5048848acce; the full replay below covers the same groups.

`./kswar run`, standard output (per-group lines for groups 0..3 and every group from 5920 on):

```
table: records=132096, bitmap identical to build_table
group 0: trials 16777216, batches 2396746, pass 995..995, control 4..5, set-up 13680, events 17 (295 ops); hits 9958/9958 keyhits 224/224 recs 447/447 v6 3/3 joint 0/0 it13 0/0 it15 0/0 coll 0/0
group 1: trials 16777216, batches 2396746, pass 995..995, control 4..5, set-up 13680, events 17 (295 ops); hits 9931/9931 keyhits 245/245 recs 561/561 v6 4/4 joint 0/0 it13 0/0 it15 0/0 coll 0/0
group 2: trials 16777216, batches 2396746, pass 995..995, control 4..5, set-up 13680, events 17 (295 ops); hits 10069/10069 keyhits 260/260 recs 575/575 v6 0/0 joint 0/0 it13 0/0 it15 0/0 coll 0/0
group 3: trials 16777216, batches 2396746, pass 995..995, control 4..5, set-up 13680, events 17 (295 ops); hits 9971/9971 keyhits 251/251 recs 526/526 v6 0/0 joint 0/0 it13 0/0 it15 0/0 coll 0/0
group 5920: trials 16777216, batches 2396746, pass 995..995, control 4..5, set-up 13680, events 17 (295 ops); hits 9963/9963 keyhits 217/217 recs 474/474 v6 2/2 joint 1/1 it13 2829/2829 it15 19/19 coll 1/1
stored pair reproduced in group 5920: n = 99325680347
M1  1e2dbac805e61a5ecd7fcb499db00a7a186cabb0f7efd9c22a442578023cd6ebf71d59bf876b73dbed1499e47173c1450ba5f907b35ebf9305848707075e188d
M1' 1e2dbac805e61a5ecd7fcb499db00a7a186cabb0f7efc9c82a64ad69522c8ce51f1e6abf876bf3dfed1499e47173c1450ba5f907b35ebf9305848707075e188d
groups 5932, trials 99492036640 in 14213153175 batches; every key and bitmap decision equal to r31det3's trial block and to klane_opt; every group's hit counters equal to process_hit's
counted: bitmap_hits=58831394 keyhits=1376281 rechits=3061666 v6=5992 joint=1 comp=1 coll=1 it13=2829 it15=19
pass 995..995, all-loaded pass 1292..1292, loop control 4..5, group set-up with broadcast 13680 (max), events per group 295 ops (max), lane index per hit <= 2
equal to the K run's log: FINAL trials=99492036640 keyhits=1376281 rechits=3061666 v6=5992 joint=1 both=1 comp=1/1 coll=1; DET it13=2829 it15=19 aborted_groups=4 bitmap_hits=58831394 groups=5932
```

The lines of groups 5921-5969 are omitted here; SHA-256 of the full output 2a69f288a025b2db50c48a6800281452c9a883437f4c49b716b43af5f0551876.

`./kswar run`, the pair written by `r31det3.c`'s own `process_hit` (`kswar-collisions.txt`):

```
COLLISION tid=30
M0 e7f5ce551741facd279a66b68a38d7c6cc332e48ed9dd62a6b76b5f73aa91ac91ca8034eb4a9ad705b8eeceb50a7afad07617b89719682b5394303d800459adb
M1 1e2dbac805e61a5ecd7fcb499db00a7a186cabb0f7efd9c22a442578023cd6ebf71d59bf876b73dbed1499e47173c1450ba5f907b35ebf9305848707075e188d
M1b 1e2dbac805e61a5ecd7fcb499db00a7a186cabb0f7efc9c82a64ad69522c8ce51f1e6abf876bf3dfed1499e47173c1450ba5f907b35ebf9305848707075e188d
DIGEST aea2562b20b12c5938046802bcc533817087f43c3e4ac864114c2abdd2249ee5
```

## Appendix E. The counted programs of Section 18

E.1 `scount12.c` (the synthetic trial loop re-counted, replayed exactly)

    5c42490685acad61bc74d50a2a16bcfc839b4f45e5ba8cbdc5ee48996827b7dd  scount12.c (v13: standalone; v12's version 71077ceb2e9d2a5c... included scount.c)
    57d1f683e00854e1ba3bc0c7dbd4da65dd57952b5c0e228f03f79805759c9b72  scount.c (C.13; the lines named in E.1's header are copied verbatim)
    bb76cf1d3700dac3039e0c43f317110c0de75d24b3f5884af783ab0f5092dae8  sp_own.h of run 2 (attempt 2's S)
    84003700c7015677e60700dc5c044d1c6e7c0acc652e6bf12d536f9aa5084437  sp_own.h of run 3 (attempt 3's S; B.5)

Built in a directory with `r31sim3.c` (B.6), the run's `sp_own.h`, `gval7.h` (D.1) and `w256.h` (D.2):
`cc -O2 -o scount12 scount12.c -lpthread`, then `./scount12 275316736` (run 2) and `./scount12 250544128` (run 3).

```c
/* scount12.c (v13, standalone): the trial loop of the synthetic completion check (r31sim3.c, B.6) re-counted and
   replayed exactly.

   The lines between the two markers are copied verbatim from scount.c (C.13, SHA-256
   57d1f683e00854e1ba3bc0c7dbd4da65dd57952b5c0e228f03f79805759c9b72): lines 16-40 (r31sim3.c included unchanged, the
   primitives), 47-59 (mul64_c, sm_c), 61-71 (the sigma, Ch and Maj helpers), 73-90 (compress31_c), 250-254 (s1inv_c),
   266-270 (RADDR, sstat_t), 401-413 (sim_ref: r31sim3's simworker loop, verbatim) and 288-291 (the LA, LE, LAB, LEB
   load macros).  s1inv_c reads r31sim3's own
   s1-inverse columns (the alias before it), and the trial loop reads r31sim3's own table (records, G16); their builds
   are charged on separate lines of the ledger (Sections 16.6, 18.5).

   The trial loop is scount.c's sim_counted with three changes, each an exact identity (proof Section 18):
   splitmix64's constant products as shift-and-add over the constants' non-adjacent forms; r % nrec by Granlund and
   Montgomery's reciprocal (PLDI 1994, Theorem 4.2), its condition asserted per run; the 64 G16 candidates seven per
   word, first match kept.  Every trial is checked, uncounted, against r31sim3's own draws, remainder and candidate
   loop, and the reference thread's counters must equal the counted ones.

   cc -O2 -o scount12 scount12.c -lpthread, next to r31sim3.c, the run's sp_own.h, w256.h and gval7.h; then
   ./scount12 275316736 (run 2, attempt 2's S) and ./scount12 250544128 (run 3, attempt 3's S) */
/* ---- verbatim from scount.c ---- */
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
#define s1inv_col_c s1inv_col
static W s1inv_c(W y) {
  W xx = 0;
  for (int k = 0; k < 32; k++) { W bit = AND(SHR(y, k), C1); xx = XOR(xx, AND(LD(s1inv_col_c[k]), SUB(0, bit))); }
  return MSK(xx);
}

/* rec address: base + 6*r (records are six words) */
#define RADDR(r) ADD(ADD(SHL((W)(r), 2), SHL((W)(r), 1)), 0)

/* ---------------- the synthetic check, counted ---------------- */
typedef struct { uint64_t recs, v6, joint, both, comp_try, comp_ok, coll; } sstat_t;

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
#define LA(i) LD(AA(i))
#define LE(i) LD(EA(i))
#define LAB(i) LD(AB(i))
#define LEB(i) LD(EB(i))
/* ---- end of the lines from scount.c ---- */

#include "w256.h"
#include "gval7.h"

static V v_or_bit(V a, int bit) { a.w[bit >> 6] |= 1ull << (bit & 63); return a; }

/* ---------------- splitmix64 with its constants as program text ---------------- */
typedef struct { int n; int8_t sg[66]; uint8_t at[66]; } nafc_t;   /* digits from the top */
static nafc_t NAF1, NAF2, NAFG;
static void naf_of(uint64_t c, nafc_t *o) {
  int8_t d[66] = {0}; int len = 0; unsigned __int128 x = c;
  while (x) { int z = 0; if (x & 1) { z = 2 - (int)(x & 3); x -= (unsigned __int128)(__int128)z; } d[len++] = (int8_t)z; x >>= 1; }
  o->n = 0; for (int i = len - 1; i >= 0; i--) if (d[i]) { o->sg[o->n] = d[i]; o->at[o->n] = (uint8_t)i; o->n++; }
  assert(o->sg[0] == 1);
}
/* z * c mod 2^64: the top digit is +1; every other digit costs a shift (none at bit 0) and an add or subtract */
static W mulk_c(W z, const nafc_t *k) {
  W acc = k->at[0] ? SHL(z, k->at[0]) : z;
  for (int j = 1; j < k->n; j++) { W t = k->at[j] ? SHL(z, k->at[j]) : z; acc = k->sg[j] > 0 ? ADD(acc, t) : SUB(acc, t); }
  return AND(acc, M64);
}
static W smk_c(uint64_t *s) {
  W z = AND(ADD(LD(*s), LD(0x9e3779b97f4a7c15ull)), M64); ST(*s, (uint64_t)z);
  z = XOR(z, SHR(z, 30)); z = mulk_c(z, &NAF1);
  z = XOR(z, SHR(z, 27)); z = mulk_c(z, &NAF2);
  return XOR(z, SHR(z, 31));
}

/* ---------------- r mod d (Granlund-Montgomery), digit lists in memory ---------------- */
static uint8_t GMP[70], GMN[70], GDP[24], GDN[24]; static int nGMP, nGMN, nGDP, nGDN, GML;
static void gm_setup_c(uint64_t d) {
  /* l = ceil(log2 d): smallest l with 2^l >= d */
  int l = 0; for (;;) { W p = SHL(C1, l); W ge = CMPLT(p, (W)d); BR(); if (!ge) break; l = (int)ADD(l, C1); }
  /* m = ceil(2^(64+l) / d): restoring division of a (65+l)-bit dividend, 9 per bit, then the rounding (3) */
  OPS += 9ull * (65 + l) + 3;
  unsigned __int128 two = (unsigned __int128)1 << (64 + l), m = two / d + (two % d != 0);
  assert(m * d >= two && m * d <= two + ((unsigned __int128)1 << l));   /* the theorem's condition */
  /* non-adjacent digits of m and of d into the lists: per bit a test, a shift and a branch; per digit a store */
  nafc_t t;
  int8_t dm[70] = {0}; int len = 0; unsigned __int128 x = m;
  while (x) { int z = 0; OPS += 4; if (x & 1) { z = 2 - (int)(x & 3); x -= (unsigned __int128)(__int128)z; OPS += 2; } dm[len++] = (int8_t)z; x >>= 1; }
  nGMP = nGMN = 0; for (int i = 0; i < len; i++) { if (dm[i] > 0) { GMP[nGMP++] = (uint8_t)i; OPS++; } else if (dm[i] < 0) { GMN[nGMN++] = (uint8_t)i; OPS++; } }
  naf_of(d, &t); nGDP = nGDN = 0;
  for (int j = 0; j < t.n; j++) { OPS += 5; if (t.sg[j] > 0) GDP[nGDP++] = t.at[j]; else GDN[nGDN++] = t.at[j]; }
  GML = 64 + l;
  ST(GML, GML); ST(nGMP, nGMP); ST(nGMN, nGMN); ST(nGDP, nGDP); ST(nGDN, nGDN);
}
/* one list: acc +-= r << pos[j] for j < n, in 256-bit words (r m < 2^130); per digit: load the position,
   variable shift, add or subtract, loop counter, compare, branch (6); the count n is loaded once (1) */
static V addlist_c(V acc, V r, const uint8_t *pos, int n, int neg) {
  W rn = LD(n);
  for (int j = 0; ; j = (int)ADD(j, C1)) {
    W more = CMPLT((W)j, rn); BR(); if (!more) break;
    V sh = VSHL(r, (int)LD(pos[j]));
    acc = neg ? VSUB(acc, sh) : VADD(acc, sh);
  }
  return acc;
}
static W urem_gm_c(W r) {
  V rv = v_of((uint64_t)r), z = v_of(0);
  V q = VSHR(addlist_c(addlist_c(z, rv, GMP, nGMP, 0), rv, GMN, nGMN, 1), (int)LD(GML));
  V qd = addlist_c(addlist_c(z, q, GDP, nGDP, 0), q, GDN, nGDN, 1);
  V rem = VSUB(rv, qd);
  assert(rem.w[1] == 0 && rem.w[2] == 0 && rem.w[3] == 0);
  return (W)rem.w[0];
}

/* ---------------- the 64 G16 candidates, seven per word ---------------- */
static V S1G[10], PAD10, D18x7, B32x7;
static void g16_setup_c(void) {
  for (int j = 0; j < 10; j++) {
    V acc = v_of(0);
    for (int l = 0; l < 7; l++) {
      int k = 7 * j + l; if (k >= ng16) break;
      W s = MSK(sg1_c(LD(G16[k])));                  /* s1(G16[k]) */
      acc = VOR(acc, VSHL(v_of((uint64_t)s), 36 * l));
    }
    S1G[j] = acc; OPS++;                               /* store */
  }
  assert(ng16 == 64);
  V p = v_of(0); for (int l = 1; l < 7; l++) p = v_or_bit(p, 36 * l + 32);
  PAD10 = p; D18x7 = v_of(0); B32x7 = v_of(0);
  for (int l = 0; l < 7; l++) { D18x7 = v_add(D18x7, v_shl(v_of(D18), 36 * l)); B32x7 = v_or_bit(B32x7, 36 * l + 32); }
  OPS += 3 * 8;                                        /* PAD10, D18x7, B32x7: built and stored once (generous) */
}
static V sg1x7(V v) {                                  /* Section 17.1: 12 primitives, v's guard bits 0 */
  V r = VAND(VXOR(VSHR(v, 17), VSHR(v, 19)), K_LO17);
  V l = VAND(VXOR(VSHL(v, 15), VSHL(v, 13)), K_HI19);
  V s = VAND(VSHR(v, 10), K_LO10);
  return VXOR(VXOR(r, l), s);
}
static V bcast7(W v) { V x = v_of((uint64_t)v); V r1 = VOR(x, VSHL(x, 36)), r2 = VOR(r1, VSHL(r1, 72)); return VOR(r2, VSHL(r2, 108)); }
/* first k with s1(s1(G16[k]) + c18 + D18) - s1(s1(G16[k]) + c18) = tgt, or -1 */
static int g16_c(W c18, W tgt) {
  /* six constants into registers for the loop: M7, LO17, HI19, LO10, D18x7, B32x7 */
  OPS += 6;
  V C18 = bcast7(MSK(c18)), TGT = bcast7(tgt);
  for (int j = 0; j < 10; j++) {
    V w18 = VAND(VADD(VLD(S1G[j]), C18), K_M7);
    V wp = VAND(VADD(w18, D18x7), K_M7);
    V a = sg1x7(wp), b = sg1x7(w18);
    V t = VAND(VADD(b, TGT), K_M7);
    V u = VADD(VXOR(t, a), K_M7);                      /* bit 32 of a lane: 1 iff the lane's difference is not tgt */
    if (j == 9) u = VOR(u, VLD(PAD10));
    V fz = VAND(u, B32x7);
    int all = !VCMPNZ(VXOR(fz, B32x7)); VBR();
    if (all) continue;
    for (int l = 0; ; l++) {                           /* the first zero lane */
      V sh = VSHR(fz, 36 * l + 32); W bit = AND((W)sh.w[0], C1); BR();
      if (!bit) return 7 * j + l;
      OPS += 1;
    }
  }
  return -1;
}

/* ---------------- complete and process_sim of B.6 with the new draws and candidate loop ---------------- */
static int complete12_c(uint32_t Wv[16], W g, uint64_t *rs) {
  W W9 = LD(Wv[9]), W1 = LD(Wv[1]), W0 = LD(Wv[0]);
  W s0W1 = sg0_c(W1);
  W W14 = s1inv_c(MSK(SUB(SUB(SUB(g, W9), s0W1), W0))); ST(Wv[14], (uint32_t)W14);
  W chk = CMPEQ(MSK(ADD(ADD(ADD(sg1_c(W14), W9), s0W1), W0)), g); BR(); if (!chk) return 0;
  W b13 = MSK(ADD(ADD(ADD(ADD(LA(9), LE(9)), bs1_c(LE(12))), ch_c(LE(12), LE(11), LE(10))), LD(K[13])));
  W b13b = MSK(ADD(ADD(ADD(ADD(LAB(9), LEB(9)), bs1_c(LEB(12))), ch_c(LEB(12), LEB(11), LEB(10))), LD(K[13])));
  W eq = CMPEQ(b13, b13b); BR(); if (!eq) return 0;
  W m13 = LD(~0x10c08000u & 0xffffffffu), o13 = LD(0x00408000u), m15 = LD(~0x00008004u & 0xffffffffu), o15 = LD(0x00000004u);
  for (int t = 0; t < (1 << 14); t++) {
    OPS += 3;
    W E13 = OR(AND(smk_c(rs), m13), o13); W W13 = MSK(SUB(E13, b13));
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
      W E15 = OR(AND(smk_c(rs), m15), o15); W W15 = MSK(SUB(E15, f15));
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

static uint64_t gsel_mismatch;
static void process12_c(const rec_t *q, const uint32_t cv[8], uint64_t *rs, sstat_t *st) {
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
  int gsel = g16_c(c18, tgt);
  {                                                    /* shadow: r31sim3's own loop, uncounted */
    int gr = -1; uint32_t c = (uint32_t)c18, tg = (uint32_t)tgt;
    for (int k = 0; k < ng16; k++) { uint32_t w18 = s1(G16[k]) + c; if ((uint32_t)(s1(w18 + D18) - s1(w18)) == tg) { gr = k; break; } }
    if (gr != gsel) gsel_mismatch++;
  }
  BR(); if (v6) { st->v6++; OPS += 3; }
  BR(); if (gsel < 0) return;
  st->joint++; OPS += 3; BR(); if (v6) { st->both++; OPS += 3; }
  st->comp_try++; OPS += 3;
  uint32_t Wc[16]; for (int i = 0; i < 16; i++) ST(Wc[i], (uint32_t)LD(Wv[i]));
  int ok = complete12_c(Wc, LD(G16[gsel]), rs); BR();
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

static uint64_t s12_ops, s12_setup_ops, draw_mismatch, idx_mismatch; static sstat_t s12_st; static uint64_t s12_N;
static void *sim12_counted(void *arg) {
  (void)arg; OPS = 0;
  uint64_t rs = (uint64_t)XOR(LD(seed_base), mul64_c(LD(0x51ed27u), C1));  /* tid 0: 0x51ed27 * 1, as scount.c */
  uint64_t shadow = seed_base ^ 0x51ed27ull;
  (void)LD(nrec);                                     /* as scount.c */
  uint64_t o0 = OPS; gm_setup_c((uint64_t)nrec); g16_setup_c(); s12_setup_ops = OPS - o0;
  for (uint64_t b = 0; b < s12_N >> 16; b++) {
    for (int it = 0; it < (1 << 16); it++) {
      OPS += 3;                                         /* it < 2^16, branch, it++ */
      W r = smk_c(&rs);
      W idx = urem_gm_c(r);
      uint64_t rr = sm(&shadow); if ((uint64_t)r != rr) draw_mismatch++;
      if ((uint64_t)idx != rr % (uint64_t)nrec) idx_mismatch++;
      const rec_t *q = &recs[(uint32_t)idx]; W a = RADDR(idx); (void)a;
      uint32_t cv[8]; ST(cv[0], (uint32_t)LD(q->key));
      W r2 = smk_c(&rs), r3 = smk_c(&rs), r4 = smk_c(&rs);
      if ((uint64_t)r2 != sm(&shadow) || (uint64_t)r3 != sm(&shadow) || (uint64_t)r4 != sm(&shadow)) draw_mismatch++;
      ST(cv[1], (uint32_t)SHR(r, 32)); ST(cv[2], (uint32_t)AND(r2, M)); ST(cv[3], (uint32_t)SHR(r2, 32));
      ST(cv[4], (uint32_t)AND(r3, M)); ST(cv[5], (uint32_t)SHR(r3, 32)); ST(cv[6], (uint32_t)AND(r4, M)); ST(cv[7], (uint32_t)SHR(r4, 32));
      process12_c(q, cv, &rs, &s12_st);
      shadow = rs;                                      /* completion draws, if any, came from the same stream */
    }
    OPS += 3 + 3 + 3;                                   /* trials += 2^16; stop flag load, test, branch; batch loop */
  }
  s12_ops = OPS; return NULL;
}

int main(int argc, char **argv) {
  seed_base = 0x5eed3;                                  /* r31sim3 1 20 5eed3 ... sim */
  outf = fopen("/dev/null", "w");
  uint64_t N = argc > 1 ? strtoull(argv[1], 0, 10) : 0;
  naf_of(0xbf58476d1ce4e5b9ull, &NAF1); naf_of(0x94d049bb133111ebull, &NAF2); naf_of(0x9e3779b97f4a7c15ull, &NAFG);
  /* the constant products against the general one and against plain C, on 10^6 values including edges */
  {
    uint64_t z = 1; W o0 = OPS; uint64_t mx1 = 0, mx2 = 0;
    for (int i = 0; i < 1000000; i++) {
      uint64_t x = i < 64 ? (1ull << i) : i < 128 ? ~(1ull << (i - 64)) : i == 128 ? 0 : i == 129 ? ~0ull : (z = z * 6364136223846793005ull + 1442695040888963407ull);
      W a0 = OPS; W p1 = mulk_c(x, &NAF1); uint64_t c1 = OPS - a0; a0 = OPS; W p2 = mulk_c(x, &NAF2); uint64_t c2 = OPS - a0;
      assert((uint64_t)p1 == x * 0xbf58476d1ce4e5b9ull && (uint64_t)p2 == x * 0x94d049bb133111ebull);
      if (c1 > mx1) mx1 = c1; if (c2 > mx2) mx2 = c2;
    }
    OPS = o0;
    uint64_t s0 = 12345, s1_ = 12345; uint64_t a0 = OPS; for (int i = 0; i < 1000; i++) assert((uint64_t)smk_c(&s0) == sm(&s1_)); uint64_t dc = (OPS - a0) / 1000; OPS = a0;
    printf("constant products: %d and %d nonzero digits, %llu and %llu primitives (general product 385); 10^6 values equal; splitmix64 draw %llu (v10: %d)\n",
           NAF1.n, NAF2.n, (unsigned long long)mx1, (unsigned long long)mx2, (unsigned long long)dc, 5 + 6 + 2 * 385);
  }
  build_s1inv(); build_table();
  printf("table: records=%d (r31sim3's own build_table)\n", nrec);
  if (N == 0 || nrec == 0) { printf("no trial loop replayed (N=%llu, records=%d)\n", (unsigned long long)N, nrec); return 0; }
  /* the remainder against C's on edge and random values */
  {
    uint64_t o0 = OPS; gm_setup_c((uint64_t)nrec); OPS = o0; uint64_t z = 7, mx = 0;
    for (int i = 0; i < 2000000; i++) {
      uint64_t x = i < 64 ? (1ull << i) : i < 128 ? (1ull << (i - 64)) - 1 : i < 1128 ? (uint64_t)nrec * (uint64_t)(i - 128) + (uint64_t)(i % 3) - 1 :
                   i == 1128 ? ~0ull : (z = z * 6364136223846793005ull + 1442695040888963407ull);
      uint64_t a0 = OPS; W r = urem_gm_c(x); uint64_t c = OPS - a0; if (c > mx) mx = c;
      assert((uint64_t)r == x % (uint64_t)nrec);
    }
    OPS = o0;
    printf("remainder mod %d: m has %d+%d digits, d %d+%d; 2*10^6 values equal to C's %%; %llu primitives (v10: 576)\n", nrec,
           nGMP, nGMN, nGDP, nGDN, (unsigned long long)mx);
  }
  ref_N = s12_N = N;
  pthread_t a, b; pthread_create(&a, 0, sim12_counted, 0); pthread_create(&b, 0, sim_ref, 0); pthread_join(a, 0); pthread_join(b, 0);
  ctr_t *c = &ctrs[0];
  printf("replay of %llu trials: counted recs=%llu v6=%llu joint=%llu both=%llu comp=%llu/%llu coll=%llu ; reference recs=%llu v6=%llu joint=%llu both=%llu comp=%llu/%llu coll=%llu\n",
    (unsigned long long)N, (unsigned long long)s12_st.recs, (unsigned long long)s12_st.v6, (unsigned long long)s12_st.joint, (unsigned long long)s12_st.both,
    (unsigned long long)s12_st.comp_ok, (unsigned long long)s12_st.comp_try, (unsigned long long)s12_st.coll,
    (unsigned long long)c->recs, (unsigned long long)c->v6, (unsigned long long)c->joint, (unsigned long long)c->both,
    (unsigned long long)c->comp_ok, (unsigned long long)c->comp_try, (unsigned long long)c->coll);
  assert(s12_st.recs == c->recs && s12_st.v6 == c->v6 && s12_st.joint == c->joint && s12_st.both == c->both &&
         s12_st.comp_try == c->comp_try && s12_st.comp_ok == c->comp_ok && s12_st.coll == c->coll);
  assert(draw_mismatch == 0 && idx_mismatch == 0 && gsel_mismatch == 0);
  printf("per trial: draws, record index and gsel equal to r31sim3's own on every trial (0 mismatches)\n");
  printf("FINAL-equivalent trials=%llu rechits=%llu v6=%llu joint=%llu both=%llu comp=%llu/%llu coll=%llu\n", (unsigned long long)N,
    (unsigned long long)s12_st.recs, (unsigned long long)s12_st.v6, (unsigned long long)s12_st.joint, (unsigned long long)s12_st.both,
    (unsigned long long)s12_st.comp_ok, (unsigned long long)s12_st.comp_try, (unsigned long long)s12_st.coll);
  printf("ops trial loop %llu (%.2f per trial), of which once-per-run set-up %llu\n", (unsigned long long)s12_ops, (double)s12_ops / N,
         (unsigned long long)s12_setup_ops);
  return 0;
}
```

E.2 `p1swar.c` (the table scan P1 as a 7-lane SWAR program)

    54a361d542c962c0206a57a698fc67ade8c9af9f2612ad93104b3c151fd23018  p1swar.c

`cc -O2 -o p1swar p1swar.c -lpthread && ./p1swar`, next to `kcount_lib.c` (D.3) and the headers of C.6 and D.1.

```c
/* p1swar.c: the 2^32 scan P1 of build_table (B.4) as a 7-lane SWAR program, counted, checked against the scan.

   P1 tests every 32-bit word w three times, in this order, and appends w to V8, V7 and G16:
     s0(w + D8) - s0(w) = C8,   s0(w + D7) - s0(w) = C7,   s1(w + D9) - s1(w) = D18.
   Here seven consecutive words w = 7b .. 7b+6 sit in the 36-bit lanes of one word (proof Section 17.1: masks,
   merged sigma forms; every input is reduced).  A test x - y = c (mod 2^32) is x XOR ((y + c) AND M7) = 0, and
   adding 2^32 - 1 sets bit 32 of a lane exactly when its difference is not 0.  The three indicators are ANDed;
   if every lane of every test is a miss, the batch costs the straight-line count; otherwise the batch's lanes
   are read in order (word order, then test order as in B.4) and the hits appended.  The last batch starts at
   2^32 - 7 and its first three lanes, already scanned, are forced to miss.

   kcount_lib.c: kcount.c with main renamed (see kswar.c).  12 slices as in kcount.c.
   cc -O2 -o p1swar p1swar.c -lpthread && ./p1swar */
#include "kcount_lib.c"
#include "w256.h"
#include "gval7.h"

static V v_bit(V a, int bit) { a.w[bit >> 6] |= 1ull << (bit & 63); return a; }
static V rep7(uint32_t c) { V r = v_of(0); for (int l = 0; l < 7; l++) r = v_add(r, v_shl(v_of(c), 36 * l)); return r; }
static V D8x7, C8x7, D7x7, C7x7, D9x7, D18x7, B32x7, PAD3;
static V sg1x7(V v) {
  V r = VAND(VXOR(VSHR(v, 17), VSHR(v, 19)), K_LO17);
  V l = VAND(VXOR(VSHL(v, 15), VSHL(v, 13)), K_HI19);
  V s = VAND(VSHR(v, 10), K_LO10);
  return VXOR(VXOR(r, l), s);
}
static V sg0x7(V v) {
  V r = VAND(VXOR(VSHR(v, 3), VSHR(v, 7)), K_LO3);
  V l7 = VAND(VSHL(v, 25), K_HI7), r18 = VAND(VSHR(v, 18), K_LO18), l18 = VAND(VSHL(v, 14), K_HI18);
  return VXOR(VXOR(VXOR(r, l7), r18), l18);
}
/* bit 32 of each lane: 1 iff x != (y + c) mod 2^32 in that lane */
static V ind(V x, V y, V c) { return VADD(VXOR(x, VAND(VADD(y, c), K_M7)), K_M7); }

typedef struct { uint64_t b0, b1, ops, nobatch_min, nobatch_max, hitbatches; int last; uint32_t *v7, *v8, *g16; int n7, n8, ng; } ps_t;
static void *ps_worker(void *arg) {
  ps_t *p = arg; OPS = 0; p->n7 = p->n8 = p->ng = 0; p->nobatch_min = UINT64_MAX;
  V st = v_of(p->b0 * 7); st = VOR(st, VSHL(st, 36)); st = VOR(st, VSHL(st, 72)); st = VOR(st, VSHL(st, 108));
  V X = VADD(VLD(K_IDX7), st);                         /* lanes 7 b0 + l: the slice start broadcast, plus 0..6 */
  W cnt = LD(p->b1 - p->b0 + (uint64_t)p->last);
  for (uint64_t b = p->b0; b < p->b1 + (uint64_t)p->last; b++) {
    uint64_t o0 = OPS;
    int last = (b == p->b1);
    if (last) X = VLD(v_add(rep7(0xfffffff9u), K_IDX7));  /* lanes 2^32 - 7 .. 2^32 - 1 */
    V s0w = sg0x7(X), s1w = sg1x7(X);
    V u8 = ind(sg0x7(VAND(VADD(X, D8x7), K_M7)), s0w, C8x7);
    V u7 = ind(sg0x7(VAND(VADD(X, D7x7), K_M7)), s0w, C7x7);
    V u9 = ind(sg1x7(VAND(VADD(X, D9x7), K_M7)), s1w, D18x7);
    V f = VAND(VAND(VAND(u8, u7), u9), B32x7);
    if (last) f = VOR(f, VLD(PAD3));
    int miss = !VCMPNZ(VXOR(f, B32x7)); VBR();
    if (!miss) {
      p->hitbatches++;
      for (int l = 0; l < 7; l++) {                      /* lanes in word order, tests in B.4's order */
        V x8 = VSHR(u8, 36 * l + 32), x7 = VSHR(u7, 36 * l + 32), x9 = VSHR(u9, 36 * l + 32);
        uint32_t w = (uint32_t)(v_shr(X, 36 * l).w[0] & 0xffffffffu);
        if (last && l < 3) { OPS += 2; continue; }       /* the lane test of the last batch */
        W h8 = CMPEQ(AND((W)x8.w[0], C1), 0); BR(); if (h8) { ST(p->v8[p->n8], w); p->n8 = (int)ADD(p->n8, C1); OPS += 2; }
        W h7 = CMPEQ(AND((W)x7.w[0], C1), 0); BR(); if (h7) { ST(p->v7[p->n7], w); p->n7 = (int)ADD(p->n7, C1); OPS += 2; }
        W h9 = CMPEQ(AND((W)x9.w[0], C1), 0); BR(); if (h9) { ST(p->g16[p->ng], w); p->ng = (int)ADD(p->ng, C1); OPS += 2; }
      }
    }
    X = VADD(X, K_SEVEN7); cnt = SUB(cnt, C1); W more = CMPNZ(cnt); BR(); (void)more;
    if (miss && !last) { uint64_t c = OPS - o0; if (c < p->nobatch_min) p->nobatch_min = c; if (c > p->nobatch_max) p->nobatch_max = c; }
  }
  p->ops = OPS; return NULL;
}

/* uncounted reference: B.4's own loop body over the same words */
typedef struct { uint64_t lo, hi; uint32_t *v7, *v8, *g16; int n7, n8, ng; } pr_t;
static void *pr_worker(void *arg) {
  pr_t *p = arg; p->n7 = p->n8 = p->ng = 0;
  for (uint64_t x = p->lo; x < p->hi; x++) { uint32_t w = (uint32_t)x;
    if ((uint32_t)(s0(w + D8) - s0(w)) == C8) p->v8[p->n8++] = w;
    if ((uint32_t)(s0(w + D7) - s0(w)) == C7) p->v7[p->n7++] = w;
    if ((uint32_t)(s1(w + D9) - s1(w)) == D18) p->g16[p->ng++] = w; }
  return NULL;
}

int main(void) {
  D8x7 = rep7(D8); C8x7 = rep7(C8); D7x7 = rep7(D7); C7x7 = rep7(C7); D9x7 = rep7(D9); D18x7 = rep7(D18);
  B32x7 = v_of(0); for (int l = 0; l < 7; l++) B32x7 = v_bit(B32x7, 36 * l + 32);
  PAD3 = v_of(0); for (int l = 0; l < 3; l++) PAD3 = v_bit(PAD3, 36 * l + 32);
  enum { NT = 12 };
  const uint64_t NB = (1ull << 32) / 7;                /* 613,566,756 full batches, then the last (4 new words) */
  static uint32_t v7s[NT][1024], v8s[NT][65536], g16s[NT][64], r7[NT][1024], r8[NT][65536], rg[NT][64];
  ps_t sl[NT]; pr_t rf[NT]; pthread_t th[NT], tr[NT];
  for (int i = 0; i < NT; i++) {
    memset(&sl[i], 0, sizeof sl[i]);
    sl[i].b0 = NB * i / NT; sl[i].b1 = NB * (i + 1) / NT; sl[i].last = i == NT - 1;
    sl[i].v7 = v7s[i]; sl[i].v8 = v8s[i]; sl[i].g16 = g16s[i];
    rf[i].lo = 7 * sl[i].b0; rf[i].hi = i == NT - 1 ? (1ull << 32) : 7 * sl[i].b1; rf[i].v7 = r7[i]; rf[i].v8 = r8[i]; rf[i].g16 = rg[i];
    pthread_create(&th[i], 0, ps_worker, &sl[i]);
  }
  for (int i = 0; i < NT; i++) pthread_join(th[i], 0);
  for (int i = 0; i < NT; i++) pthread_create(&tr[i], 0, pr_worker, &rf[i]);
  for (int i = 0; i < NT; i++) pthread_join(tr[i], 0);
  uint64_t ops = 0, hb = 0, mn = UINT64_MAX, mx = 0; int n7 = 0, n8 = 0, ng = 0;
  for (int i = 0; i < NT; i++) {
    assert(sl[i].n7 == rf[i].n7 && sl[i].n8 == rf[i].n8 && sl[i].ng == rf[i].ng);
    assert(!memcmp(sl[i].v7, rf[i].v7, 4 * sl[i].n7) && !memcmp(sl[i].v8, rf[i].v8, 4 * sl[i].n8) && !memcmp(sl[i].g16, rf[i].g16, 4 * sl[i].ng));
    ops += sl[i].ops; hb += sl[i].hitbatches; n7 += sl[i].n7; n8 += sl[i].n8; ng += sl[i].ng;
    if (sl[i].nobatch_min < mn) mn = sl[i].nobatch_min;
    if (sl[i].nobatch_max > mx) mx = sl[i].nobatch_max;
  }
  ops += 16;                                            /* the 16 lane constants, loaded once (the slices share them) */
  printf("P1 as 7-lane SWAR: V7=%d V8=%d G16=%d, each list equal word for word to B.4's loop; batches %llu (%llu with a hit); "
         "batch without a hit %llu..%llu primitives; ops %llu (%.4f per word; scalar P1 of C.7: 236223301254, 55 per word)\n",
         n7, n8, ng, (unsigned long long)(NB + 1), (unsigned long long)hb, (unsigned long long)mn, (unsigned long long)mx,
         (unsigned long long)ops, ops / 4294967296.0);
  assert(n7 == 512 && n8 == 49408 && ng == 64);
  return 0;
}
```

E.3 Output (2026-10-08)

`./scount12 275316736` (run 2):

```
constant products: 23 and 23 nonzero digits, 45 and 45 primitives (general product 385); 10^6 values equal; splitmix64 draw 101 (v10: 781)
table: records=224 (r31sim3's own build_table)
remainder mod 224: m has 22+1 digits, d 1+1; 2*10^6 values equal to C's %; 165 primitives (v10: 576)
replay of 275316736 trials: counted recs=275316736 v6=538099 joint=42381 both=88 comp=42381/42381 coll=88 ; reference recs=275316736 v6=538099 joint=42381 both=88 comp=42381/42381 coll=88
per trial: draws, record index and gsel equal to r31sim3's own on every trial (0 mismatches)
FINAL-equivalent trials=275316736 rechits=275316736 v6=538099 joint=42381 both=88 comp=42381/42381 coll=88
ops trial loop 345802476470 (1256.02 per trial), of which once-per-run set-up 1777
```

`./scount12 250544128` (run 3):

```
constant products: 23 and 23 nonzero digits, 45 and 45 primitives (general product 385); 10^6 values equal; splitmix64 draw 101 (v10: 781)
table: records=132096 (r31sim3's own build_table)
remainder mod 132096: m has 6+5 digits, d 2+0; 2*10^6 values equal to C's %; 93 primitives (v10: 576)
replay of 250544128 trials: counted recs=250544128 v6=489532 joint=38874 both=64 comp=38874/38874 coll=64 ; reference recs=250544128 v6=489532 joint=38874 both=64 comp=38874/38874 coll=64
per trial: draws, record index and gsel equal to r31sim3's own on every trial (0 mismatches)
FINAL-equivalent trials=250544128 rechits=250544128 v6=489532 joint=38874 both=64 comp=38874/38874 coll=64
ops trial loop 296672248975 (1184.11 per trial), of which once-per-run set-up 1875
```

`./p1swar`:

```
P1 as 7-lane SWAR: V7=512 V8=49408 G16=64, each list equal word for word to B.4's loop; batches 613566757 (25946 with a hit); batch without a hit 91..91 primitives; ops 55836954414 (13.0006 per word; scalar P1 of C.7: 236223301254, 55 per word)
```

## Appendix F. The analysis programs re-counted (Section 19)

F.1 `pcount13.c`

    1a330a93b174874cf50d86a477fce4cd851639d487fbce8263d2fe04a177c78c  pcount13.c
    2f1d1b37bdbffe70ccc97744d6786495d3cba445b46257a87d5e782722e2b953  pcount.c (C.9, unchanged)

Built next to `w256.h` (D.2) and `gval7.h` (D.1): `cc -O2 -o pcount13 pcount13.c -lpthread -lm`. `pcount.c` is cited by
its SHA-256 above; lines 19-70, 73-74 and 80-82 of it are copied into `pcount13.c`, and the whole file is published in
filings 089b597d, 028aa8d0 and 2954243d (Appendix C.9).

```c
/* pcount13.c: the pre-construction analysis programs (sets, joint, pany, pany2; proof Section 15.2) re-counted with
   the 7-lane SWAR forms of Sections 17-18, printing the same lines as pcount.c (C.9) and as the originals.

   The primitives, floating-point tariffs, sigma helpers and table entry are lines of pcount.c (C.9), copied below
   verbatim; the probing (add_ci, get_cn) and the printing are those of C.9's add_c, get_c and run_* functions.

   What changes, each an exact identity on the same values:
   - The 2^32 scans run seven consecutive words per batch in the 36-bit lanes of Section 17.1 (sigma forms and
     masks as there; a difference x - y mod 2^32 is ((x | 2^32) - y) & M7; a test x - y = c is read in bit 32
     of ((x XOR ((y + c) & M7)) + (2^32 - 1))).  The last batch starts at 2^32 - 7 and its first three lanes,
     already scanned, are skipped.
   - The hash index (k * 0x9e3779b1 mod 2^32) >> 7 is shift-and-add over the 11 non-adjacent digits of the
     constant (19 set bits in C.9): lane-wise, each term is (k AND (2^(32-b) - 1)) << b, the positive and the
     negative terms are summed apart and joined as (P + 6 * 2^32 - N) AND M7; scalar, 22 primitives instead of 38.
   - Every table insertion happens in the original order (word order; for joint, each table in word order), so
     the tables, and the slot-order floating-point sums read from them, are the originals'.
   - Per sample (pany, pany2): the 64 candidates are computed seven per word; a candidate is new iff no earlier
     candidate equals it (compared seven at a time against its broadcast); psum adds the counts of the new ones.
     The original adds the counts over its list of distinct values, so the integer psum, and every floating-point
     operation on it, is the same.  Each sample is also checked, uncounted, against the original's distinct list.
   Floating-point operations are charged and evaluated exactly as in C.9.

   cc -O2 -o pcount13 pcount13.c -lpthread -lm;  ./pcount13 sets | joint | pany | pany2-1-20 | pany2-12-28 */
/* ---- verbatim from pcount.c (C.9, SHA-256 2f1d1b37bdbffe70ccc97744d6786495d3cba445b46257a87d5e782722e2b953),
        lines 19-70, 73-74 and 80-82: the primitives, floating-point tariffs, sigma helpers, table entry ---- */
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

#define HB 25
#define HS (1u << HB)
typedef struct { uint32_t k; uint32_t c; } E;
/* table of 2^25 entries of two words at base address 0: entry i at 2i */
static inline W EADDR(W i) { return ADD(SHL(i, 1), 0); }
/* ---- end of the lines from pcount.c ---- */
#include <assert.h>
#include <stdatomic.h>
#include "w256.h"
#include "gval7.h"

static V v_bit(V a, int bit) { a.w[bit >> 6] |= 1ull << (bit & 63); return a; }
static V rep7(uint64_t c) { V r = v_of(0); for (int l = 0; l < 7; l++) r = v_add(r, v_shl(v_of(c), 36 * l)); return r; }
static V B32x7, M25x7, NFIX, PAD9, FORCE[7], LOWm[32];
static const int HP[] = {9, 22, 29, 31}, HN[] = {4, 6, 11, 15, 19, 25};   /* with +1 at bit 0: 0x9e3779b1 */
static void consts13(void) {
  B32x7 = v_of(0); for (int l = 0; l < 7; l++) B32x7 = v_bit(B32x7, 36 * l + 32);
  M25x7 = rep7((1u << HB) - 1); NFIX = rep7(6ull << 32);
  PAD9 = v_of(0); for (int l = 1; l < 7; l++) PAD9 = v_bit(PAD9, 36 * l + 32);
  for (int l = 0; l < 7; l++) { FORCE[l] = v_of(0); for (int q = l; q < 7; q++) FORCE[l] = v_bit(FORCE[l], 36 * q + 32); }
  for (int b = 1; b < 32; b++) LOWm[b] = rep7((1ull << (32 - b)) - 1);
  int64_t chk = 1; for (int i = 0; i < 4; i++) chk += 1ll << HP[i]; for (int i = 0; i < 6; i++) chk -= 1ll << HN[i];
  assert((uint32_t)chk == 2654435761u);
}
static V sg1x7(V v) {
  V r = VAND(VXOR(VSHR(v, 17), VSHR(v, 19)), K_LO17);
  V l = VAND(VXOR(VSHL(v, 15), VSHL(v, 13)), K_HI19);
  V s = VAND(VSHR(v, 10), K_LO10);
  return VXOR(VXOR(r, l), s);
}
static V sg0x7(V v) {
  V r = VAND(VXOR(VSHR(v, 3), VSHR(v, 7)), K_LO3);
  V l7 = VAND(VSHL(v, 25), K_HI7), r18 = VAND(VSHR(v, 18), K_LO18), l18 = VAND(VSHL(v, 14), K_HI18);
  return VXOR(VXOR(VXOR(r, l7), r18), l18);
}
static V dsub7(V a, V b) { return VAND(VSUB(VOR(a, B32x7), b), K_M7); }
static V ind7(V x, V y, V c) { return VADD(VXOR(x, VAND(VADD(y, c), K_M7)), K_M7); }
static V hash7(V k) {                                  /* lanes: (k * 0x9e3779b1 mod 2^32) >> 7 */
  V P = k;
  for (int i = 0; i < 4; i++) P = VADD(P, VSHL(VAND(k, LOWm[HP[i]]), HP[i]));
  V N = VSHL(VAND(k, LOWm[HN[0]]), HN[0]);
  for (int i = 1; i < 6; i++) N = VADD(N, VSHL(VAND(k, LOWm[HN[i]]), HN[i]));
  return VAND(VSHR(VAND(VSUB(VADD(P, NFIX), N), K_M7), 32 - HB), M25x7);
}
static W hshn_c(W k) {                                 /* scalar, 22 primitives */
  W acc = k;
  for (int i = 0; i < 4; i++) acc = ADD(acc, SHL(k, HP[i]));
  for (int i = 0; i < 6; i++) acc = SUB(acc, SHL(k, HN[i]));
  return SHR(MSK(acc), 32 - HB);
}
static W lane_c(V v, int l) {                          /* lane l of a clean word: 1 (lanes 0 and 6) or 2 */
  if (l == 0) return AND((W)v.w[0] | ((W)v.w[1] << 64), M);
  if (l == 6) { V s = VSHR(v, 216); return (W)s.w[0]; }
  V s = VSHR(v, 36 * l); return AND((W)s.w[0] | ((W)s.w[1] << 64), M);
}
/* add_c and get_c of C.9 from a given index */
static void add_ci(E *h, uint64_t *n, W k, W i) {
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
static W get_cn(const E *h, W k) {
  W i = hshn_c(k);
  for (;;) {
    W a = EADDR(i); (void)a; W c = LD(h[(uint32_t)i].c); W nz = CMPNZ(c); BR();
    if (!nz) return 0;
    W kk = LD(h[(uint32_t)i].k); W eq = CMPEQ(kk, k); BR();
    if (eq) return c;
    i = AND(ADD(i, C1), LD(HS - 1));
  }
}
static inline uint32_t hsh_ref(uint32_t k) { return (uint32_t)(k * 2654435761u) >> (32 - HB); }

/* the batch loop over 2^32 words: lanes 7b + l; the last batch at 2^32 - 7 */
#define NB ((1ull << 32) / 7)
static V X0(uint64_t b) {                              /* the first batch of a slice: broadcast 7b, plus 0..6 */
  V st = v_of(7 * b); st = VOR(st, VSHL(st, 36)); st = VOR(st, VSHL(st, 72)); st = VOR(st, VSHL(st, 108));
  return VADD(VLD(K_IDX7), st);
}
static V XLAST(void) { return VLD(v_add(rep7(0xfffffff9u), K_IDX7)); }
#define BATCH_TAIL() do { X = VADD(X, K_SEVEN7); cnt = SUB(cnt, C1); W more_ = CMPNZ(cnt); BR(); (void)more_; } while (0)

/* ---------------- sets ---------------- */
typedef struct { uint64_t b0, b1; int last; uint64_t ops, cnt[7], both[7]; } sl_t;
static uint32_t S_d[7], S_c[7], S_cm[7], S_va[7], S_vb[7], S_xm[7]; static int S_sig[7];
static void *sets_worker(void *arg) {
  sl_t *p = arg; OPS = 0;
  OPS += 26;                                            /* resident lane masks and constants, loaded once */
  V D[7], Cc[7]; for (int i = 0; i < 7; i++) { D[i] = VLD(rep7(S_d[i])); Cc[i] = VLD(rep7(S_c[i])); }
  V X = X0(p->b0); W cnt = LD(p->b1 - p->b0 + (uint64_t)p->last);
  for (uint64_t b = p->b0; b < p->b1 + (uint64_t)p->last; b++) {
    int last = b == p->b1; if (last) X = XLAST();
    V s0w = sg0x7(X), s1w = sg1x7(X), U[7], WP[7];
    for (int i = 0; i < 7; i++) { WP[i] = VAND(VADD(X, D[i]), K_M7); U[i] = ind7(S_sig[i] ? sg1x7(WP[i]) : sg0x7(WP[i]), S_sig[i] ? s1w : s0w, Cc[i]); }
    V f = U[0]; for (int i = 1; i < 7; i++) f = VAND(f, U[i]);
    int miss = !VCMPNZ(VXOR(VAND(f, B32x7), B32x7)); VBR();
    if (!miss) {
      for (int i = 0; i < 7; i++) {
        int any = VCMPNZ(VXOR(VAND(U[i], B32x7), B32x7)); VBR();
        if (!any) continue;
        for (int l = last ? 3 : 0; l < 7; l++) {
          V sh = VSHR(U[i], 36 * l + 32); W miss_l = AND((W)sh.w[0], C1); BR();
          if (miss_l) continue;
          ST(p->cnt[i], (uint64_t)ADD(LD(p->cnt[i]), C1));
          W w = lane_c(X, l), wp = lane_c(WP[i], l);
          W ok = CMPEQ(XOR(w, wp), LD(S_xm[i])); BR();
          if (ok) { ok = CMPEQ(AND(w, LD(S_cm[i])), LD(S_va[i])); BR(); }
          if (ok) { ok = CMPEQ(AND(wp, LD(S_cm[i])), LD(S_vb[i])); BR(); }
          if (ok) ST(p->both[i], (uint64_t)ADD(LD(p->both[i]), C1));
        }
      }
    }
    BATCH_TAIL();
  }
  p->ops = OPS; return NULL;
}
static uint64_t run_sets13(void) {
  OPS = 0;
  struct { const char *name; int sig; uint32_t d, c; const char *row; } S[] = {
   {"W5",0,0xfffff006,0xd0018020,"================nuuu=======0=uu="},
   {"W6",0,0x002087f1,0x00000ffa,"==========u=====u===u======n===u"},
   {"W7",0,0x4fefb5fa,0xffdf780f,"=u=u=======n=====n=nu=n=====nun="},
   {"W8",0,0x28011100,0xb00fca02,"=u=nn==========u===u===u==1====="},
   {"W9",0,0x00008004,0xd7feef00,"================u==========1=u=="},
   {"W16",1,0x00008004,0xffff7ffc,"=============unnnunnnnnnnnnnnn=="},
   {"W18",1,0xffff7ffc,0x2ffe7fe0,"==============1=n=0==========n=="}};
  for (int i = 0; i < 7; i++) {
    uint32_t cm = 0, va = 0, vb = 0, xm = 0;
    for (int k = 0; k < 32; k++) { uint32_t b = 1u << (31 - k); char c = S[i].row[k]; OPS += 6;
      if (c == '=') continue; cm |= b; if (c == '1') { va |= b; vb |= b; } else if (c == 'u') { vb |= b; xm |= b; } else if (c == 'n') { va |= b; xm |= b; } }
    S_d[i] = S[i].d; S_c[i] = S[i].c; S_cm[i] = cm; S_va[i] = va; S_vb[i] = vb; S_xm[i] = xm; S_sig[i] = S[i].sig;
  }
  uint64_t main_ops = OPS;
  enum { NT = 12 }; sl_t sl[NT]; pthread_t th[NT];
  for (int i = 0; i < NT; i++) { memset(&sl[i], 0, sizeof sl[i]); sl[i].b0 = NB * i / NT; sl[i].b1 = NB * (i + 1) / NT; sl[i].last = i == NT - 1;
    pthread_create(&th[i], 0, sets_worker, &sl[i]); }
  uint64_t cnt[7] = {0}, both[7] = {0}, ops = main_ops;
  for (int i = 0; i < NT; i++) { pthread_join(th[i], 0); ops += sl[i].ops; for (int k = 0; k < 7; k++) { cnt[k] += sl[i].cnt[k]; both[k] += sl[i].both[k]; } }
  ops -= (NT - 1) * 14;                                 /* the 14 lane constants are loaded once */
  for (int i = 0; i < 7; i++) printf("%s modular=%llu signed+modular=%llu\n", S[i].name, (unsigned long long)cnt[i], (unsigned long long)both[i]);
  return ops;
}

/* ---------------- the d5 / d18 table builds and the G16 scans ---------------- */
/* build one table in word order: which = 5 (s0, d5) or 18 (s1, d18); with g16 != NULL also the G16 test of pany2
   (s1(w + d9) - s1(w) = d18) in the same loop, as pany2's loop does */
typedef struct { E *h; uint64_t *n; int which; uint32_t *g16; int ng; uint64_t ops; } bd_t;
static void *build_worker(void *arg) {
  bd_t *p = arg; OPS = 0;
  OPS += 26;                                            /* resident lane masks and constants, loaded once */
  V Dd = VLD(rep7(p->which == 5 ? 0xfffff006u : 0xffff7ffcu)), D9 = VLD(rep7(0x00008004u)), D18 = VLD(rep7(0xffff7ffcu));
  V X = X0(0); W cnt = LD(NB + 1);
  for (uint64_t b = 0; b <= NB; b++) {
    int last = b == NB; if (last) X = XLAST();
    V sw = p->which == 5 ? sg0x7(X) : sg1x7(X);
    V wp = VAND(VADD(X, Dd), K_M7);
    V k = dsub7(p->which == 5 ? sg0x7(wp) : sg1x7(wp), sw);
    V ix = hash7(k);
    V u16 = v_of(0); int g16hit = 0;
    if (p->g16) {
      V s1w = sg1x7(X);
      u16 = ind7(sg1x7(VAND(VADD(X, D9), K_M7)), s1w, D18);
      g16hit = VCMPNZ(VXOR(VAND(u16, B32x7), B32x7)); VBR();
    }
    for (int l = last ? 3 : 0; l < 7; l++) {
      W kl = lane_c(k, l), il = lane_c(ix, l);
      uint32_t w = (uint32_t)(7 * b + l); if (last) w = 0xfffffff9u + (uint32_t)l;
      uint32_t ref = p->which == 5 ? (uint32_t)(s0(w + 0xfffff006u) - s0(w)) : (uint32_t)(s1(w + 0xffff7ffcu) - s1(w));
      assert((uint32_t)kl == ref && (uint32_t)il == hsh_ref(ref));
      add_ci(p->h, p->n, kl, il);
      if (g16hit) {
        V sh = VSHR(u16, 36 * l + 32); W miss_l = AND((W)sh.w[0], C1); BR();
        if (!miss_l) { ST(p->g16[p->ng], w); p->ng = (int)ADD(p->ng, C1); }
      }
    }
    BATCH_TAIL();
  }
  p->ops = OPS; return NULL;
}
/* pany's separate G16 scan: s1(w + d16) - s1(w) = d18, 12 slices; hits joined in slice order */
typedef struct { uint64_t b0, b1; int last; uint64_t ops; uint32_t g[64]; int ng; } gs_t;
static void *g16_worker(void *arg) {
  gs_t *p = arg; OPS = 0;
  OPS += 26;                                            /* resident lane masks and constants, loaded once */
  V D16 = VLD(rep7(0x00008004u)), D18 = VLD(rep7(0xffff7ffcu));
  V X = X0(p->b0); W cnt = LD(p->b1 - p->b0 + (uint64_t)p->last);
  for (uint64_t b = p->b0; b < p->b1 + (uint64_t)p->last; b++) {
    int last = b == p->b1; if (last) X = XLAST();
    V u = ind7(sg1x7(VAND(VADD(X, D16), K_M7)), sg1x7(X), D18);
    int any = VCMPNZ(VXOR(VAND(u, B32x7), B32x7)); VBR();
    if (any) for (int l = last ? 3 : 0; l < 7; l++) {
      V sh = VSHR(u, 36 * l + 32); W miss_l = AND((W)sh.w[0], C1); BR();
      if (!miss_l) { ST(p->g[p->ng], (uint32_t)lane_c(X, l)); p->ng = (int)ADD(p->ng, C1); }
    }
    BATCH_TAIL();
  }
  p->ops = OPS; return NULL;
}

/* ---------------- per-sample candidates, dedup and psum ---------------- */
static V S1G[10];
static void s1g_setup_c(const uint32_t *G, int ng) {
  assert(ng == 64);
  for (int j = 0; j < 10; j++) {
    V acc = v_of(0);
    for (int l = 0; l < 7 && 7 * j + l < 64; l++) acc = VOR(acc, VSHL(v_of((uint64_t)MSK(s1c(LD(G[7 * j + l])))), 36 * l));
    S1G[j] = acc; OPS++;
  }
}
static V bcast7(W v) { V x = v_of((uint64_t)v); V r1 = VOR(x, VSHL(x, 36)), r2 = VOR(r1, VSHL(r1, 72)); return VOR(r2, VSHL(r2, 108)); }
static _Atomic uint64_t sample_mismatch;
/* returns psum; *strict (when non-NULL) = some candidate equals mc5 */
static W sample13(const E *h5, W c18, const uint32_t *G, W mc5, W *strict) {
  OPS += 6 + 7 + (strict ? 1 : 0);                      /* load M7, LO17, HI19, LO10, D18x7, B32x7; the seven FORCE masks; MC5x7 */
  V D18 = rep7(0xffff7ffcu), C18 = bcast7(c18), Xw[10], MC = strict ? bcast7(mc5) : v_of(0);
  V sacc = B32x7;
  for (int j = 0; j < 10; j++) {
    V w18 = VAND(VADD(VLD(S1G[j]), C18), K_M7);
    V wp = VAND(VADD(w18, D18), K_M7);
    Xw[j] = dsub7(sg1x7(wp), sg1x7(w18));
    if (strict) { V u = VADD(VXOR(Xw[j], MC), K_M7); if (j == 9) u = VOR(u, VLD(PAD9)); sacc = VAND(sacc, u); }
  }
  if (strict) *strict = CMPNZ((W)VCMPNZ(VXOR(VAND(sacc, B32x7), B32x7)));
  W psum = 0; int nnew = 0;
  for (int g = 0; g < 64; g++) {
    int j = g / 7, l = g % 7;
    W xg = lane_c(Xw[j], l);
    int dup = 0;
    if (g > 0) {
      V XG = bcast7(xg), acc = v_of(0);
      int first = 1;
      for (int q = 0; q <= j; q++) {
        if (q == j && l == 0) break;
        V u = VADD(VXOR(XG, Xw[q]), K_M7);
        if (q == j) u = VOR(u, FORCE[l]);
        acc = first ? u : VAND(acc, u); first = 0;
      }
      dup = VCMPNZ(VXOR(VAND(acc, B32x7), B32x7));
    }
    VBR();
    if (!dup) { psum = ADD(psum, get_cn(h5, MSK(SUB(0, xg)))); nnew++; }
  }
  {                                                     /* shadow: the original's distinct list, uncounted */
    uint32_t v[64]; int nv = 0; uint64_t ps = 0; int st = 0;
    for (int g = 0; g < 64; g++) { uint32_t w18 = s1(G[g]) + (uint32_t)c18, x = s1(w18 + 0xffff7ffcu) - s1(w18);
      int d = 0; for (int q = 0; q < nv; q++) if (v[q] == x) { d = 1; break; } if (!d) v[nv++] = x; if (x == (uint32_t)mc5) st = 1; }
    for (int q = 0; q < nv; q++) { uint32_t key = 0u - v[q], i = hsh_ref(key); while (h5[i].c && h5[i].k != key) i = (i + 1) & (HS - 1); ps += h5[i].c; }
    if (ps != (uint64_t)psum || nv != nnew || (strict && (W)st != *strict)) atomic_fetch_add(&sample_mismatch, 1);
  }
  return psum;
}

/* ---------------- joint ---------------- */
static uint64_t run_joint13(void) {
  OPS = 0;
  E *h5 = calloc(HS, sizeof(E)), *h18 = calloc(HS, sizeof(E)); uint64_t n5 = 0, n18 = 0;
  OPS += 2ull * HS * 2;
  bd_t a = {h5, &n5, 5, NULL, 0, 0}, b = {h18, &n18, 18, NULL, 0, 0}; pthread_t ta, tb;
  pthread_create(&ta, 0, build_worker, &a); pthread_create(&tb, 0, build_worker, &b); pthread_join(ta, 0); pthread_join(tb, 0);
  OPS += a.ops + b.ops;
  printf("distinct sigma0-diff values for d5: %llu ; sigma1-diff values for d18: %llu\n", (unsigned long long)n5, (unsigned long long)n18);
  double single = 0, unionb = 0, strict = 0; W c5 = LD(0xd0018020u);
  const double sc = 1.0 / 4294967296.0;
  for (uint32_t i = 0; i < HS; i++) {
    OPS += 3; W ad = EADDR(i); (void)ad; W c = LD(h5[i].c); W nz = CMPNZ(c); BR();
    if (!nz) continue;
    W k = LD(h5[i].k);
    double p5 = FMUL(FCVT(c), sc);
    double p18 = FMUL(FCVT(get_cn(h18, MSK(SUB(0, k)))), sc);
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
    for (uint32_t i = 0; i < HS; i++) { OPS += 3; W ad = EADDR(i); (void)ad; W c = LD(h5[i].c); W gt = CMPLT((W)best, c); BR(); if (gt) { best = (uint32_t)c; bk = i; OPS += 2; } }
    W g18 = get_cn(h18, MSK(SUB(0, LD(h5[bk].k))));
    printf("  %08x %u p18(-c)=2^%.2f\n", h5[bk].k, best, log2(((double)(uint64_t)g18 + 1e-9) / 4294967296.0)); OPS += T_CVTF + T_FADD + T_FDIV;
    ST(h5[bk].c, 0u);
  }
  free(h5); free(h18);
  return OPS;
}

/* ---------------- pany ---------------- */
static uint64_t run_pany13(void) {
  OPS = 0;
  E *h5 = calloc(HS, sizeof(E)); OPS += 2ull * HS;
  bd_t a = {h5, NULL, 5, NULL, 0, 0}; build_worker(&a);
  enum { NT = 12 }; gs_t sl[NT]; pthread_t th[NT];
  for (int i = 0; i < NT; i++) { memset(&sl[i], 0, sizeof sl[i]); sl[i].b0 = NB * i / NT; sl[i].b1 = NB * (i + 1) / NT; sl[i].last = i == NT - 1;
    pthread_create(&th[i], 0, g16_worker, &sl[i]); }
  uint32_t G[64]; int ng = 0; uint64_t gops = 0;
  for (int i = 0; i < NT; i++) { pthread_join(th[i], 0); gops += sl[i].ops; for (int k = 0; k < sl[i].ng; k++) G[ng++] = sl[i].g[k]; }
  gops -= (NT - 1) * 2;
  OPS = 2ull * HS + a.ops + gops;
  printf("|G16|=%d\n", ng);
  const int N = 1 << 24; double acc = 0; uint64_t accs = 0; W mc5 = LD((uint32_t)(0u - 0xd0018020u));
  const double sc = 1.0 / 4294967296.0;
  uint64_t st = 0x9e3779b97f4a7c15ull;
  s1g_setup_c(G, ng);
  for (int t = 0; t < N; t++) {
    OPS += 3;
    st = (uint64_t)XOR(st, AND(SHL(st, 13), M64)); st = (uint64_t)XOR(st, SHR(st, 7)); st = (uint64_t)XOR(st, AND(SHL(st, 17), M64));
    W c18 = MSK(SHR(st, 16));
    W strictf = 0;
    W psum = sample13(h5, c18, G, mc5, &strictf);
    acc = FADD(acc, FMUL(FCVT(psum), sc));
    accs = (uint64_t)ADD(accs, strictf);
  }
  printf("P_any(joint, 64 g)=2^%.3f ; P(strict G18 exists g)=%.4f ; strict P=2^%.3f\n", log2(acc / N), (double)accs / N, log2((double)accs / N * pow(2, -18)));
  OPS += 2 * T_CVTF + 2 * T_FDIV + T_FMUL;
  free(h5);
  return OPS;
}

/* ---------------- pany2 ---------------- */
static E *Q2h5; static uint32_t Q2G[64]; static int Q2NS, Q2NT; static double Q2sum[64], Q2sum2[64]; static uint64_t Q2ops[64];
static void *pany2_work13(void *a) {
  int t = (int)(intptr_t)a; OPS = 0;
  uint64_t st = (uint64_t)XOR(LD(0x243f6a8885a308d3ull), AND(ADD(0, (W)((uint64_t)(t + 1) * 0x9e3779b97f4a7c15ull)), M64));
  OPS += 385;
  double S = 0, S2 = 0; const double sc = 1.0 / 4294967296.0;
  for (long n = 0; n < Q2NS / Q2NT; n++) {
    OPS += 3;
    st = (uint64_t)XOR(st, AND(SHL(st, 13), M64)); st = (uint64_t)XOR(st, SHR(st, 7)); st = (uint64_t)XOR(st, AND(SHL(st, 17), M64));
    W c18 = MSK(SHR(st, 20));
    W psum = sample13(Q2h5, c18, Q2G, 0, NULL);
    double p = FMUL(FCVT(psum), sc);
    S = FADD(S, p); S2 = FADD(S2, FMUL(p, p));
  }
  Q2sum[t] = S; Q2sum2[t] = S2; Q2ops[t] = OPS; return NULL;
}
static uint64_t run_pany2_13(int NT, int lg) {
  OPS = 0; Q2NT = NT; Q2NS = 1 << lg;
  Q2h5 = calloc(HS, sizeof(E)); OPS += 2ull * HS;
  bd_t a = {Q2h5, NULL, 5, Q2G, 0, 0}; build_worker(&a);
  int ng = a.ng; OPS = 2ull * HS + a.ops;
  uint32_t mxc = 0;
  for (uint32_t i = 0; i < HS; i++) { OPS += 3; W ad = EADDR(i); (void)ad; W c = LD(Q2h5[i].c); W gt = CMPLT((W)mxc, c); BR(); if (gt) { mxc = (uint32_t)c; OPS++; } }
  s1g_setup_c(Q2G, ng);
  uint64_t main_ops = OPS;
  pthread_t th[64]; for (int i = 0; i < NT; i++) pthread_create(&th[i], 0, pany2_work13, (void *)(intptr_t)i);
  for (int i = 0; i < NT; i++) pthread_join(th[i], 0);
  OPS = main_ops; for (int i = 0; i < NT; i++) OPS += Q2ops[i] + 3;
  double S = 0, S2 = 0; for (int i = 0; i < NT; i++) { S = FADD(S, Q2sum[i]); S2 = FADD(S2, Q2sum2[i]); }
  double n = (double)(Q2NS / Q2NT) * Q2NT, m = S / n, var = S2 / n - m * m, se = sqrt(var / n);
  OPS += T_CVTF + T_FMUL + 3 * T_FDIV + 2 * T_FMUL + T_FADD + T_FSQRT + 4 * T_FADD;
  printf("|G16|=%d samples=2^%d mean=%.6e (2^%.4f) se=%.3e 99%%LCB=%.6e (2^%.4f) 99%%UCB=2^%.4f max_term_bound=%.3e\n", ng, (int)log2(n), m, log2(m), se, m - 2.576 * se, log2(m - 2.576 * se), log2(m + 2.576 * se), 64.0 * mxc / 4294967296.0);
  free(Q2h5);
  return OPS;
}

int main(int argc, char **argv) {
  if (argc < 2) return 64;
  consts13();
  { /* the hash forms against C's product on 10^6 keys */
    uint64_t z = 1, o0 = OPS, mx = 0, mx7 = 0;
    for (int i = 0; i < 1000000; i++) {
      z = z * 6364136223846793005ull + 1442695040888963407ull;
      uint32_t k = i < 32 ? (1u << i) : i == 32 ? 0 : i == 33 ? 0xffffffffu : (uint32_t)z ^ (uint32_t)(z >> 32);
      uint64_t a0 = OPS; W h = hshn_c(k); if (OPS - a0 > mx) mx = OPS - a0;
      assert((uint32_t)h == hsh_ref(k));
      if (i % 7 == 6) { V kk = v_of(0); uint32_t ks[7]; for (int l = 0; l < 7; l++) { ks[l] = k ^ (uint32_t)(l * 0x9e3779b9u); kk = v_add(kk, v_shl(v_of(ks[l]), 36 * l)); }
        uint64_t h0 = OPS; V hv = hash7(kk); mx7 = OPS - h0; for (int l = 0; l < 7; l++) assert((uint32_t)(v_shr(hv, 36 * l).w[0] & ((1u << HB) - 1)) == hsh_ref(ks[l])); }
    }
    OPS = o0;
    fprintf(stderr, "hash: scalar %llu primitives (C.9: 38), seven lanes %llu; 10^6 keys equal\n", (unsigned long long)mx, (unsigned long long)mx7);
  }
  const char *p = argv[1]; uint64_t ops;
  if (!strcmp(p, "sets")) ops = run_sets13();
  else if (!strcmp(p, "joint")) ops = run_joint13();
  else if (!strcmp(p, "pany")) ops = run_pany13();
  else if (!strcmp(p, "pany2-1-20")) ops = run_pany2_13(1, 20);
  else if (!strcmp(p, "pany2-12-28")) ops = run_pany2_13(12, 28);
  else return 64;
  fprintf(stderr, "OPS %s %llu\n", p, (unsigned long long)ops);
  if (strcmp(p, "sets") && strcmp(p, "joint")) fprintf(stderr, "samples checked against the original's distinct list: %llu mismatches\n", (unsigned long long)sample_mismatch);
  assert(sample_mismatch == 0);
  return 0;
}
```

F.2 Output (2026-10-08)

`./pcount13 sets`, standard error (its standard output is byte-identical to C.9's output of `sets`):

```
hash: scalar 22 primitives (C.9: 38), seven lanes 34; 10^6 keys equal
OPS sets 108037853099
        6.42 real        39.24 user         0.37 sys
```

`./pcount13 joint`, standard error (its standard output is byte-identical to C.9's output of `joint`):

```
hash: scalar 22 primitives (C.9: 38), seven lanes 34; 10^6 keys equal
OPS joint 267852965723
       93.39 real       125.53 user         3.65 sys
```

`./pcount13 pany`, standard error (its standard output is byte-identical to C.9's output of `pany`):

```
hash: scalar 22 primitives (C.9: 38), seven lanes 34; 10^6 keys equal
OPS pany 209345560218
samples checked against the original's distinct list: 0 mismatches
      154.14 real       119.55 user         2.70 sys
```

`./pcount13 pany2-1-20`, standard error (its standard output is byte-identical to C.9's output of `pany2-1-20`):

```
hash: scalar 22 primitives (C.9: 38), seven lanes 34; 10^6 keys equal
OPS pany2-1-20 148843827942
samples checked against the original's distinct list: 0 mismatches
      100.34 real        76.61 user         2.04 sys
```

`./pcount13 pany2-12-28`, standard error (its standard output is byte-identical to C.9's output of `pany2-12-28`):

```
hash: scalar 22 primitives (C.9: 38), seven lanes 34; 10^6 keys equal
OPS pany2-12-28 1344467221045
samples checked against the original's distinct list: 0 mismatches
      173.43 real       663.47 user         7.86 sys
```
