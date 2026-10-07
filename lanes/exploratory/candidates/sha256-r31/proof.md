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

Every computation of C is charged (Section 9). The z3 runs, the synthetic checks and search K are
charged from their measured retired instructions at measured per-instruction prices (Section 14):
19 word operations per instruction for z3, 13 for the synthetic checks, and for K 8 on its search
hot path and 10 on the rest of the process, with every multiply and floating-point instruction off
that path charged again at its full price. K's price is measured on the executable that ran
(Section 14.6); our previous filing charged K with an operation model instead. Our other own code is
charged with explicit operation counts. The analysis programs that formulated R20 before any search
ran are charged as well (Section 15). The complete source is in Appendices B and C.

| field | value | where |
|---|---|---|
| time_log2 | 36.64 | executed work of C plus replay, 2^36.6392, Section 9 |
| preprocessing_log2 | 36.64 | construction chain C, Section 9 |
| success_probability | 1 | deterministic replay, Section 3 |
| nonuniform_advice_log2_bytes | 9 | the stored 256-byte pair, Section 10 |
| memory_log2_bytes | 27.5 | measured peak over C (the z3 runs), Section 10 |

Our own change to the source attack is the relaxed W20 condition R20 (Section 6). The published
characteristic fixes the s0-difference of W5 and the s1-difference of W18. R20 only requires that
the two cancel, which is exactly dW20 = 0. The stored pair uses differences of 0ffd81e1 and
f0027e1f, not the characteristic's.

Heuristics are declared in Section 11:
- H1-public-characteristic, H2-op-accounting, H3-instruction-price and H5-chain-scope are
  score-critical;
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
    synthetic completion check, `r31sim3 1 20 5eed3 ... sim`: 500,284,109,323 instructions per run (3 runs)
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

The z3 runs, the synthetic checks and the K run are charged at the measured per-instruction prices
of Section 14 (H3). Our other own code is charged with the operation counts of H2. The analysis
programs of Section 15.2 are charged with operation bounds from their source (H2).

    z3 attempts 1-3: 2,721,814,602,106 instructions * 19 / 2140                      24,165,643,664
    synthetic completion checks: 3 runs * 500,284,109,323 instructions * 13 / 2140    9,117,327,226
    yield checks: 5 * (three 2^32 scans <= 24 ops/word + table <= 6.4e6 * 64 ops)      723,470,929
    V8 dump (one 2^32 scan, <= 24 ops/word) and c8 residue scan
        (300,000 * 49408 candidates, <= 8 ops each)                                 103,578,699
    pre-construction analysis (Section 15.2): 27,838,136,107,008 ops / 2140                     13,008,474,817
    Python model generation, verification and analysis: lump allowance       1,000,000,000
    K run, 15,640,902,198,904 retired instructions (Section 14.6, H3):
      search hot path: 12,436,504,580 passes * 1238 = 15,396,392,670,040 instr. * 8 / 2140
                                                                                  57,556,608,113
      remainder (table build, self-checks, bitmap hits, group set-up, completion, main thread):
        244,509,528,864 instructions * 10 / 2140                                      1,142,567,892
      in addition, heavy instructions off the hot path: 1,121,255,712 multiplies * 400
        + main-thread and library floating point, at most 710,000 instructions * 1024     209,920,246
    -------------------------------------------------------------------------------------------
    preprocessing (chain C)                                                  107,027,591,586 = 2^36.6392
    replay R                                                                 6.36
    total                                                                    107,027,591,592 = 2^36.6392

Claimed time_log2 = 36.64 and preprocessing_log2 = 36.64. Every term is the work actually executed
by C or by the analysis that formulated R20. Nothing is an expectation or a cap that went unused.

The Python lump covers every Python run in the chain and in the pre-construction analysis:
gen_s.py, check_s.py and analyze.py three times each, and two short inline scripts on S and on the V8
dump (Section 15.1). Re-runs of gen_s.py and check_s.py retire 220,935,601 and 211,710,075
instructions, most of it interpreter start-up. Even if every instruction were priced as a multiply
(400 operations), one such run would be 4.2e7 units, and the lump covers 23 of them.

The K run's retired-instruction count covers the whole K process: the set scans and table (P1, P2),
the self-checks, every group and the main thread. So its single priced block replaces the whole
operation-model block of our previous filing (101,185,639,958 units, with 1 compression + 32
operations per trial). The K term (58,909,096,251 units) is 55.0% of the total; the
instruction-priced lines (z3, synthetic checks, K) are 86.1%.

The K run was not lucky. Model value: with 132096 records, a V6 rate of 2^-9 and an R20 rate of
2^-12.66, a first success is expected after about 2^36.6 trials. K needed 2^36.531.

## 10. Memory and advice

The advice of R is the stored 256-byte pair; 9 is claimed. Peak memory over C was measured with
`/usr/bin/time -l` on every run: the largest maximum resident set size was 161,103,872 bytes (z3
attempt 2, 2^27.26), against 7,438,336 bytes for the K run. The claim of 27.5 covers it.

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
  charge of T units for it gives a total of 107,027,591,592 + T units. That stays below 2^39.15 (our
  earlier filing) for T up to 2^38.872, and below 2^40.4 for T up to 2^40.289.

H2-op-accounting (score-critical). For our own code other than search K (Appendix B), the
per-event charges of Section 9 bound the primitive word operations:
- yield checks: per scanned word 24, per table candidate 64;
- V8 dump: per scanned word 24; residue scan: per candidate 8;
- the pre-construction analysis programs (Section 15.2): the per-run bounds listed there, with
  floating-point operations at 400 and divisions at 1024.
Search K is no longer charged by an operation model; it is charged from its retired instructions
under H3 (Section 14.6).

H3-instruction-price (score-critical). For the z3 attempts, the synthetic completion checks and
search K, the per-instruction prices of Section 14 bound their primitive word operations: 19 per
retired instruction for z3, 13 for the synthetic checks, and for K 8 on the search hot path and 10
on the remainder of the process, with every multiply off the hot path charged again at 400 and the
main thread's floating point at 1024.
- Scope: the retired-instruction counts of Section 8 (macOS counters through `/usr/bin/time -l`).
- Evidence: the per-form costing of the AArch64 code (Appendix C.1), applied statically to the z3
  binary that ran and dynamically to callgrind instruction counts of the same z3 version and the
  same three committed models, and of the same synthetic-check source (Section 14). For K, the
  executed path of the executable that ran (Section 14.6), with its SIMD forms priced by their
  exact emulation on one 256-bit word (Appendix C.3, checked by C.4), and a callgrind cross-check
  of a Linux build of the same source.
- Premise for K's SIMD forms: a 128-bit vector register is one datum in one 256-bit word, as the
  v5 table already assumes for SIMD logic (cost 1). A lane-wise form (4-lane add, shifts, shift and
  accumulate, three-way XOR, bit select) is priced by its exact emulation on that word with lane
  masks; each emulation is checked against the lane-wise definition (Section 14.6). Forms without a
  checked emulation keep the v5 price of 16.
- Extrapolation: the dynamic mix comes from the Linux build of z3 4.15.4. It covers all of
  attempt 1 (the same search, step for step) and the first 28% and 39% of attempts 2 and 3 by
  rlimit count. The static mixes of the two builds agree (Section 14.3). The price doubles the worst
  per-form dynamic mean of 23 measured intervals to cover the unprofiled remainder and the build
  difference. K's hot path (98.44% of its instructions) is a fixed instruction sequence of the
  binary that ran, executed once per 8 trials; its price still doubles its per-form mean.
- Sensitivity: at 256 operations per instruction for z3 and the synthetic checks the total would
  be 2^39.074; at four times every charged price (z3, synthetic checks and K) it would be
  2^38.481; at the class prices of 50592e75 for z3 and the synthetic checks (25 and 17) it is
  2^36.7734. For K alone: under the flat SIMD price 16 of the v5 table (K at 23) the total
  would be 2^37.654; with every K instruction at 16 it would be 2^37.266; with each
  32-bit lane of a vector register in its own word (hot-path mean 7.32, price 15) it would be
  2^37.196; under the operation model of our previous filing it was 2^37.1195.

H4-memory (supporting). The measured maximum resident set sizes bound C's peak memory.

H5-chain-scope (score-critical). Every constant of C comes from the public characteristic, from
analysis, from the charged pre-construction analysis programs, or from the charged v3 runs before K
(Section 15.3). The earlier search runs that used the published starting solution produced rates
and pairs that C does not read, and they fixed no constant of C (Section 15.4). They are excluded.
- Scope: all computation on this target in our working directories and session records on
  2026-10-06 and 2026-10-07, listed in Section 15.1.
- Evidence: the agent transcript of the session that ran every command, the file times of the
  working directories, the commitments of Appendix A, and the package commit history.
- Extrapolation: the commitments are local (file timestamps and a local git history), not
  notarised.
- Sensitivity: if a reviewer charged the excluded search runs anyway, the 2^40.625-trial run alone
  would put the total at 2^40.733.

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
  sharing steps 0..14 across first blocks (we use this for speed only, with no discount).
- Ours: R20, the starting-solution model with the yield residue, chain C and its execution, the
  experiment, and the per-instruction price measurement of Section 14.

## 14. Per-instruction price: our own evidence

This section supports H3. It measures what one retired instruction of the charged programs costs
in primitive word operations. Apart from one re-run of K's table build (Section 14.6), it does not
re-run any charged call on the measurement machine.

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

### 14.4 Dynamic mix: callgrind on the same solver version and the same models

Valgrind does not run on macOS arm64 and we have no other instruction-level profiler there, so we
measured the mix on the Linux build of the same z3 version on the same machine: Debian bookworm arm64 in Docker, valgrind 3.19.0,
`valgrind --tool=callgrind --dump-instr=yes --dump-every-bb=8000000000 z3 -T:1200 -st s-modelN.smt2`
on the three committed models with their committed seeds. `cgmix.py` (Appendix C.2) maps every
executed instruction address to its disassembly and prices it with `a64ops.py`. Every executed
instruction was mapped except 3,932, which are priced at 1024.

Attempt 1 ran to completion under callgrind and repeated the macOS search exactly: the same model
(A1 = a651919f, ...), rlimit-count 249,602,816, 1,068,222 conflicts and 1,829,611 decisions as the
charged run. So the profile of attempt 1 is a profile of the very same search, executed by a
different build; that build retired 245,527,956,010 instructions against 261,276,415,067 on macOS.
Attempts 2 and 3 hit the 1200 s callgrind time limit. We profiled their first 361,089,420,698 and
308,853,516,577 instructions, which reached rlimit-count 341,226,376 of the charged run's 1,200,096,786
(28%) and 309,573,558 of 797,205,785 (39%).

| model | profiled instructions | intervals | heavy share | divide share | ordinary mean | per-form mean | class price |
|---|---|---|---|---|---|---|---|
| attempt 1 (complete) | 245,527,956,010 | 6 | 1.10-1.48% | 0.0000-0.0120% | 2.28-2.31 | 6.82-8.16 | 9.48-10.84 |
| attempt 2 (prefix) | 361,089,420,698 | 9 | 1.16-1.78% | 0.0000-0.0119% | 2.28-2.31 | 7.04-9.38 | 9.70-12.04 |
| attempt 3 (prefix) | 308,853,516,577 | 8 | 1.12-1.56% | 0.0000-0.0129% | 2.28-2.31 | 6.88-8.48 | 9.54-11.15 |

Here the class price of an interval is m_class = 5 (1 - h - d - u) + 400 h + 1024 d + 1024 u,
with h, d and u the heavy, divide and unmapped shares: every ordinary instruction is priced 5, about
2.2 times its measured dynamic mean of 2.28-2.31 operations. The per-form mean is the exact
dynamic average under the table of 14.2.

**Price.** m_z3 = ceil(2 * max over all 23 intervals of the per-form mean) = ceil(2 * 9.3833) = **19**.
The worst interval is one of attempt 2's (per-form mean 9.38333); the same interval has the
largest class price, 12.044. Our promoted filing 50592e75 priced z3 at the class
price, ceil(2 * 12.044) = 25, which also priced every ordinary instruction at 5 instead of its
measured 2.28-2.31; this filing prices every executed instruction by its form.
The factor 2 covers the unprofiled remainder of attempts 2 and 3 and the build difference. For
attempt 1 the profile is complete. The macOS build retired 6.4% more instructions for the same
search; if both builds execute the same multiplies and divides, its heavy share is the lower one.

### 14.5 The synthetic completion check

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

### 14.6 Search K: the executable that ran, priced by its executed path

K is charged from its retired instructions (Section 8: 15,640,902,198,904) at prices measured on the
executable that ran.

- **Executable.** `r31det3`, built from B.4 and B.5 with Apple clang,
  `cc -O3 -mcpu=apple-m4 -o r31det3 r31det3.c -lpthread`, at 13:04 KST, before K started at
  13:04:56, and not rebuilt since. SHA-256 2824a0f855c203d1ada6f99e5a25fa8aebd4f2feeee0a8a56776c311af4bce23.
  Disassembly: `xcrun llvm-objdump -d --no-show-raw-insn r31det3`.
- **Vectorised kernel.** clang compiled the 8-lane trial block of `worker` (the `j < LANES` loops of
  B.4) into NEON code: a 524-instruction block that handles 4 lanes, run twice per 8 trials. Its
  forms are 4-lane add, shift left, shift right and accumulate, three-way XOR and bit select. The
  v5 table of 14.2 charges every SIMD form other than logic at a flat 16 ("charged as shuffles").
  Under that table the hot path costs 11.13 operations per instruction, and doubled, 23: above the
  13.84 at which the measured count would equal the operation model of our previous filing. We
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
209,920,246 = **58,909,096,251** units. The operation model of our previous filing charged 101,185,639,958;
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

**Sensitivity** (total 107,027,591,592 = 2^36.6392):
- v5 table with its flat SIMD price 16 (K hot path 11.13, so 23 for all of K): 2^37.654;
- every K instruction at 16, heavy instructions as above: 2^37.266;
- twice the charged K prices (16 and 20): 2^37.270;
- without the factor 2 (4 on the hot path, 3 on the remainder): 2^36.173;
- each 32-bit lane in its own word (hot-path mean 7.32, price 15): 2^37.196;
- the operation model of our previous filing: 2^37.1195.

### 14.7 What this does not establish

- The dynamic profile is of the Linux build. The equal search transcript of attempt 1 and the equal
  static profiles support the transfer; they do not prove an identical instruction mix.
- The price is an operation count under our per-form table. A reviewer who prices some form higher
  can recompute the dynamic mean from the published scripts; the factor 2 is the reserve. At the
  class prices for z3 and the synthetic checks instead (25 and 17), the total is 2^36.7734.
- K's hot-path weights are exact: the path is a fixed instruction sequence of the executable that
  ran, executed once per pass, and the pass count is the run's trial counter divided by 8. The
  remainder (1.56%) is priced from per-form means of its code (exact for the table scan, static for
  the rest) with a margin, and every heavy instruction in it is counted from the source and charged
  in full.
- The SWAR prices count operations on one 256-bit word per 128-bit register, as the v5 table does
  for SIMD logic. If each 32-bit lane were instead put in its own word (`add.4s` 8, `usra.4s` 12,
  `eor3.16b` 8, a 128-bit load 4 loads), the hot-path mean would be 7.32, the doubled price 15, and
  the total 2^37.196: above the operation model of our previous filing (2^37.1195).
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
| 09:43-09:59 | pre-construction analysis: `analyze.py` (3 runs), `sets` (1), `table` (2), `joint` (1), `pany` (1). They formulated R20 and estimated its rate (`joint`, 09:48) | **charged**, Section 15.2 |
| 10:36-10:37 | `r31s` self-tests (3) and a 12 s test | excluded (published S) |
| 10:37-11:22 | relaxed search with the published S, 2^40.625 trials | excluded (published S), Section 15.4 |
| 10:44-11:35 | synthetic completion, independence and cluster runs with the published S (`r31sim`, `r31log`, `r31log2`, `r31clus`, `r31log3`); `pany2` (2 runs: 2^20 samples at 10:47, 2^28 samples at about 11:24) | `pany2` **charged** (15.2); the others excluded |
| 11:55-12:12 | K' runs with the published S (filing 3183e839, refuted) | excluded (published S) |
| 12:52-13:04 | chain C before K: z3 attempts 1-3, gen_s/check_s, yield checks (5), synthetic checks (3), V8 dump, c8 scan, inline Python on S and V8 | **charged**, Section 9 |
| 13:04-13:07 | search K | **charged**, Section 9 |
| 13:08-13:09 | instruction-count re-runs: `diag` (2), `r31sim3` (2), `v8dump`, `c8scan` | not charged: after the pair existed |
| 15:39-16:10 | v4 price measurements (Section 14) | not charged: after the pair existed |
| 10-08 03:59-04:10 | v6 K price measurements: `r31det3 1 0` on macOS, gcc build under callgrind (Section 14.6) | not charged: after the pair existed |

"Published S" means the runs used the published starting solution: S was derived from the published
collision in that work, so C cannot and does not use any of its outputs.

### 15.2 Charged pre-construction analysis (operation bounds from source)

These programs read only the characteristic and SHA-256 constants (and, for `table`, the published
starting solution). They ran exactly the times listed in 15.1. Operation bounds:

| program | work per run | operations per run |
|---|---|---|
| `sets` | 7 sets * 2^32 words * 48 | 1,443,109,011,456 |
| `table` (2 runs) | per run two 2^32 scans * 24 + 49408 * 512 pairs * 128 | 418,792,865,792 (both runs) |
| `joint` | 2^32 * 2 difference evaluations and hash inserts * 96 + 2^25 slots * 6,000 (two lookups, five floating-point operations) + top-5 scans | 1,027,302,490,112 |
| `pany` | h5 build 2^32 * 96 + 2^24 samples * 142,800 (64 candidates * 300 + 64 lookups with conversion, division and addition * 1,900 + 2,000) | 2,808,111,087,616 |
| `pany2` (2 runs: 2^20 and 2^28 samples) | per run h5 build 2^32 * 96, plus 79,100 per sample (64 * 300 + 64 * 900 + 2,300) | 22,140,820,652,032 (both runs) |
| total | | 27,838,136,107,008 |

Floating-point operations are priced at 400 and divisions at 1024, as in Section 14.2. The Python
`analyze.py` runs are in the Python lump of Section 9.

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
| group structure (2^24 trials share words 0..14) | Section 7.3 | public design (credited), used for speed only |
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
- Sensitivity: charging the 2^40.625-trial run anyway would add 2^40.625 * (1 + 32/2140) units and put
  the total at 2^40.733.

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

B.6 `r31sim3.c` (synthetic completion check, charged by instructions)

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

## Appendix C. Price scripts

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
