# sha256-r31: replay of a collision built by our own chain on the published characteristic (local-search family + SWAR online)

Cost model collision-frontier-v5, C = 2140. Logarithms are base 2 and costs are in units.

## 1. Claim

**time_log2 = 31.61** (ledger 2^31.6008 = 3,256,770,328 units, rounded up). preprocessing_log2 = 31.61,
success probability 1 (the replay R), memory 2^34.9 bytes, nonuniform advice 2^9 bytes (the stored pair).

- The scored program R (Section 3) replays one stored pair. The pair is a two-block 31-step collision that our own
  construction chain C built (Sections 7-8). The claimed time is all work that C executed, plus R.
- C has one external input: the published 31-step signed characteristic of Li, Liu, Wang, Dong and Sun (ASIACRYPT
  2024). We use it as public algorithm text without charging its discovery (heuristic H1, the same premise as the
  promoted r31 record 50592e75). C uses its A and E signed rows 5..12 and the modular message differences d5..d9,
  d16 and d18. C does not use the characteristic's 180 value cells, any published pair, starting point or first
  block.
- **Luck does not lower the claim below a luck-free charge.** The online phase found the pair after 109,081,798
  trials (2^26.70), early against the rate model's 1/q = 2^30.23 (heuristic H6). Its trial cap N = 2,522,586,633 was
  computed by phase A before the online phase started. The online phase is charged at the larger of two amounts:
  - (a) the counted SWAR program over the full cap N, 3.764e8 units. This is luck-free under H2, H6 and H7.
  - (b) the retired instructions of the run that executed, at price 5, 4.221e8 units. This is the realized work, and
    it grows with the realized count.

  Term (b) binds here, so (a) is a floor for this term. The hit path is charged at its global caps. Under the same
  rule, a run of typical length (1/q trials) would have given about 2^32.85, and a run reaching N 2^33.56 (Section 9).
- C's success is also realized. Key 1 succeeded within N, which under H6 has model probability 1 - e^-2 = 0.86. Had
  it failed, the pre-registered continuation rule would have added a charged run with key 2. R succeeds with
  probability 1 given C's output.
- Every process of C is charged, and so are the conversion checks made before the freeze (Section 15). Of the work
  done after the pair existed, we also charge the official-verifier check and a re-measurement of the conversion
  checks. The other post-hoc work is not part of C, and nothing in C reads it:
  - the price measurement (Section 14);
  - the package checks;
  - the recomputation of the pair's differences in Section 4;
  - the location of the found trial in the key-1 stream (Section 4);
  - the measurements of the rate-model factors (H6, Section 16);
  - two runs of `sets_swar`, a counted re-implementation of S prepared for a later accounting (Section 15).
- All sources are in Appendix B, the run records in Appendix C and the pre-registration in Appendix A.

## 2. Target

sha256-r31-prefix-v1: SHA-256 steps 0..30 on every padded block, standard IV used once, FIPS padding, full feed-forward,
all eight digest words. Messages are two blocks (128 bytes), M0||M1 and M0||M1'. They share the first block M0, and
M1' = M1 + DW word-wise. DW = (d5, d6, d7, d8, d9) in words 5..9 and zero elsewhere.

## 3. The scored program (replay)

R1. Read the stored advice: the two 128-byte strings P and P' (Section 4).
R2. Compute sha256-r31(P) and sha256-r31(P'). The padded messages are three blocks, so this is three compressions
    each.
R3. If P != P' and the digests are equal, output (P, P'). Otherwise output nothing.

R uses no coins, so its success probability is 1. Its cost is 6 compressions plus at most 768 word operations, which
is 6.36 units. The organizer verifier confirms the relation for these bytes (certificate `v8-pair`).

## 4. The stored pair

    M0  : f228b816 3644ca7a 31ea7f59 478c7d72 9d064d1e f874313c cdfe9b17 7fd7577d
          2ebc719d c82b3e50 e9c595c2 d2e670aa 88bbefaa 946f6e50 1b4b6b5e 2408ef77
    M1  : 94012921 4476294f c880eda8 67b6a3a7 e1e22aa3 c8a2b743 9ac56136 06b457fb
          63f1956c 912a6919 6b02539a 6319a5f3 6c6a82a1 297ce0d8 65acf487 962b7beb
    M1' : 94012921 4476294f c880eda8 67b6a3a7 e1e22aa3 c8a2a749 9ae5e927 56a40df5
          8bf2a66c 912ae91d 6b02539a 6319a5f3 6c6a82a1 297ce0d8 65acf487 962b7beb
    sha256-r31(M0||M1) = sha256-r31(M0||M1') = fba0ac8bb06058083f0632d7b10ccc26efa87d13991bb8e88d65e04f58d4ffa3

M0 is lane 1 of SWAR batch 15,645,968 of the online phase's AES-128-CTR stream under key 1. That batch was run by
thread 15,645,968 mod 12 = 8. The organizer experiment re-derives M0 from the key with a pure-Python AES-128
(Section 12). The 12 threads had evaluated 109,081,798 trials in total when the run stopped. Threads advance at
different speeds, so the global index 7 x 15,645,968 + 1 of this trial exceeds that count.

M1 is built from three things:
- that trial's chaining value;
- a table record of starting point 233 (0-based, of 483);
- that starting point's second completion (j = 467) and the completion's E13/W14/W15 draws (Section 7, O).

It was the only completion call of the whole run.

What the pair satisfies (recomputed from the two messages):
- Every A row and every E row of the characteristic's signed-difference cells, for all steps 0..30, exactly.
- The modular differences of every W row: d5..d9 in words 5..9, d16 = d9 at step 16, d18 at step 18, and 0
  elsewhere.
- In XOR form, W5, W8 and W18 carry their modular difference with a different carry pattern than the published
  signed W cells. Every message word enters the state update additively, so only the modular differences matter
  there. The XOR form matters only through the schedule's s0(W5), s0(W8) and s1(W18) terms, and Section 6 tests
  exactly those (the step-20 condition and V8).
- 148 of the characteristic's 180 value cells. Those cells are not imposed by C.

## 5. The public characteristic (the only external input)

The cell table below is the published 31-step characteristic (ASIACRYPT 2024 presentation, slide 14) as transcribed
cell by cell in the promoted filing 50592e75 (jungjipdo, Section 5 of its proof). We use that transcription verbatim
(`pubchar_table.txt`, Appendix B).

Cell notation:
- `=`: the bits are equal.
- `0` / `1`: both bits equal that value.
- `u`: the bit is 0 in P and 1 in P'.
- `n`: the bit is 1 in P and 0 in P'.

Rows -4..2, 17 and 19..30 are all `=` and are not listed.

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

The table has 300 non-`=` cells: 120 signed (`u`/`n`) and 180 value cells.

Phase C0 (`pubchar.py`) converts it into the counterexample text format that phase C1 parses. It writes every value
cell as `=` (no difference). Phase C1 (`cglue char`) derives two things from it:
- the message differences
  `dW5..dW9 = fffff006 002087f1 4fefb5fa 28011100 00008004`, `d16 = 00008004`, `d18 = ffff7ffc`;
- the signed masks of A5..A12 and E5..E12 (`c.txt`, Appendix C).

These are exactly the modular differences listed in 50592e75's Section 5.

## 6. Exact difference requirements

In the second block only W5..W9 differ, by d5..d9. For t = 16..30 (the same derivation as 50592e75's Section 6):

    t=16: dW16 = d9.
    t=18: need W16 in G16 = {w : s1(w+d9) - s1(w) = d18}, so that dW18 = d18.
    t=20: need s1(W18+d18) - s1(W18) + s0(W5+d5) - s0(W5) = 0            (the step-20 condition)
    t=21: need W6 in V6 = {w : s0(w+d6) - s0(w) = -d5 = 00000ffa}.
    t=22: need W7 in V7 = {w : s0(w+d7) - s0(w) = -d6 = ffdf780f}.
    t=23: need W8 in V8 = {w : s0(w+d8) - s0(w) = -d7 - d9 = b00fca02}.
    t=24: need W9 in V9 = {w : s0(w+d9) - s0(w) = -d8 = d7feef00}.
    t=25: d18 + d9 = 0.   t = 17, 19, 26..30: no term has a difference.

The step-20 condition only asks that the two s-function differences cancel. That is jungjipdo's R20, and our v5 had
it independently as a class split. Every message word enters the state update only additively, so this relaxation
leaves every state condition unchanged.

Phase S computes these sets exhaustively over 2^32 (Appendix C):
|V6| = 2^23, |V7| = 512, |V8| = 49,408, |V9| = 35,921,920, |G16| = 64. |V6|, |V7|, |V8| and |G16| equal 50592e75's.

Why an output of O collides:
- Steps 0..4 carry no difference.
- O sets W0..W8 so that copy P reaches the starting point's A1..A4 and E5..E8 from the trial's chaining value
  through the matched record (E3, E4).
- The starting point satisfies the step 5..13 relations of both copies by construction (model M, phase A re-checks
  every condition, including the signed rows).
- W6 is tested against V6, and W7, W8 lie in V7 and V8 by construction of the record.
- The step-20 condition is tested over G16.
- The completion has three steps:
  1. It picks W14 so that W16 = s1(W14) + W9 + s0(W1) + W0 lies in G16 and meets the step-20 condition.
  2. It draws E13, at most 2^16 times per W14, and requires E14' - E14 = 00008004 (= -d18) and equal step-15 sums.
     Step 18 then cancels dE14 against dW18.
  3. It draws W15, at most 2^16 times in total with at most 16 full candidates, and requires dE16 = 0 and an equal
     IF(E16, E15, E14).
- Under these conditions steps 19..30 carry no difference.
- The two copies share CV1 and the padding block, so the digests are equal.

O re-hashes every candidate from the IV before it outputs it.

## 7. Construction chain C (one execution of `run_v8.sh OUT 1`, Appendix B)

| # | phase | program | what it computes |
|---|---|---|---|
| C0 | characteristic text | `pubchar.py` (Python) | the cell table -> counterexample text (replaces a characteristic search; no solver) |
| C1 | rows + model M | `cglue char` (C) | signed masks and differences (`c.txt`); model M (`m.cvc`, after USCMig f94a3f75) with the signed rows A5..A12, E5..E12 as hints |
| S | exact sets | `sets` (C, 12 threads, one pass over 2^32) | V6 (as a count), V7, V8, V9 (count), G16 |
| M | starting point | STP 2.4.1 + CryptoMiniSat 5.14.7, one call, default seed | A1..A4, E3..E12 of copy P satisfying model M (both copies, exact step equations, V7/V8/V9 conditions, dA10 = -d18, dA11 = dA12 = 0, dE13 = dA13 = 0, signed rows) |
| C3 | parse | `cglue sp` (C) | the starting point's 14 words |
| L | local search | `ls2 c.txt sets.txt sp.txt 64 S 2` (C) | USCMig's move set; details below the table |
| A | tables, rate model, cap | `tabm ... 2 200 4194304 0076364172617465` (C) | details below the table |
| O | online + completion | `v6on ADV KEY` (C, 12 threads) | details below the table |

Details for L, A and O:
- **L (local search).** USCMig's move set flips 1-2 bits of A5..A8 and E5..E12 and derives A1..A4. It keeps a new
  starting point when every exact and signed condition holds and its table is non-empty. It runs breadth first for 64
  expansions with 2 completions per starting point, giving 483 starting points and 5,704,080 table tuples.
- **A (tables, rate model, cap).** Per starting point it re-checks every condition, builds the tuple table
  (E3, E4, key) and finds 2 completions (BFS over 1-/2-bit changes of E9..E12, distinct W11, at most 200 nodes).
  The rate model is q = T x |V6|/2^32 x 2^-32 x p20, where p20 = 1,282 / 2^22 seeded samples. It sets
  q = 2^-30.2323 and N = 2/q = 2,522,586,633 (rounded up to a multiple of 7).
- **O (online and completion).** Each 7-trial batch draws sixteen 256-bit words under the key; each word is two
  AES-128-CTR blocks. Lane l's message word i is bits [36l, 36l+32) of word i. The steps are:
  1. CV1 word 0 is looked up in the full 2^32-bit key bitmap.
  2. On a match, binary search finds the records with that key.
  3. W0..W8 are derived from CV1 and the record.
  4. W6 is tested against V6.
  5. The step-20 condition is tested over G16 for each completion.
  6. The capped completion draws E13, W14 and W15.
  7. Every candidate is re-hashed.

  The run stops at the first verified pair or at N. It has global caps on key matches, tuple tests, W6 passes and
  completion calls.

The design constants are byte-identical to the driver line of our earlier chain (filing 6d554419), which ran on our
own characteristic 8_14:
- NEXP = 64 and J = 2 (L);
- T11 = 200, MCS = 2^22 and the rate-model seed 0076364172617465 (A).

The thread count is 12, the pre-registered machine limit; v7 used 15. It sets the scheduling, and which completion
coin stream (AES-CTR domain 1 + thread id) a trial's completion uses. v8's programs differ from v7's only in the two
thread-count lines.

Section 15 shows that none of these constants is load-bearing for the stored pair. The pair is the same for every
NEXP from 24 to 64, every T11 >= 200, and every MCS and seed that give N >= 109,521,783.

Filing 6d554419 was refuted on findings about three things:
- its in-chain characteristic search, whose seven model constants it took uncharged;
- its unshipped programs;
- its use of the development-selected 8_14 configuration together with these design constants without charging
  their selection (F-P2-COST-OMISSION).

C runs no characteristic search: like the promoted record 50592e75, it takes the published characteristic as public
algorithm text (H1). It ships every program (Appendix B). Section 15 gives, for each design constant, the evidence that
it did not select the stored pair.

The online key is k = 1: the first 16 bytes of SHA-256("sha256-r31-v8 online key 1"), that is
bf6b900804436c1fa167048b448f358e. The pre-registration (Appendix A) fixed every constant, the key rule and the
continuation rule before any chain process ran. Under the continuation rule, a run reaching N without a pair goes on
with key k + 1, and every such run is charged. Key 1 succeeded, so no other key was run.

## 8. Execution records

Every process of C ran under `/usr/bin/time -l` (macOS counters). Each record holds the retired instructions, the
wall time and the maximum RSS, in OUT/ledger_runs.tsv (Appendix C):

| phase | start (UTC) | exit | retired instructions | wall (s) | max RSS (bytes) |
|---|---|---:|---:|---:|---:|
| C0 | 2026-10-08T07:53:43Z | 0 | 200,191,633 | 0.01 | 9,994,240 |
| C1 | 2026-10-08T07:53:43Z | 0 | 17,193,583 | 0.00 | 1,802,240 |
| S | 2026-10-08T07:55:43Z | 0 | 184,954,807,110 | 1.23 | 2,834,432 |
| M | 2026-10-08T07:55:44Z | 0 | 315,870,919,550 | 30.22 | 228,261,888 |
| C3 | 2026-10-08T07:56:15Z | 0 | 13,318,419 | 0.00 | 1,540,096 |
| L | 2026-10-08T07:56:15Z | 0 | 240,400,504,458 | 7.10 | 19,857,408 |
| A | 2026-10-08T07:56:22Z | 0 | 19,919,547,288 | 1.26 | 8,749,056 |
| O | 2026-10-08T07:56:23Z | 0 | 185,766,459,621 | 2.17 | 814,366,720 |

Online counters (END line of v6on):
`END batches 15583114 trials 109081798 kmatch 54474 tuptests 145709 w6pass 291 r20tests 37194 accepts 1 compl_calls 1 e13 4140 w15 13 tails 1 found 1 stop 1`

The model value of the online phase is about 1/q = 2^30.23 trials. The run found its pair after 2^26.70 trials,
which is early: under the rate model a key-1 success within this many trials had probability about 8%. The claim
charges the online phase at the larger of the SWAR program at the full cap N (term (a), luck-free) and the native
run's instructions (term (b)). Term (b) binds; it is the realized work and grows with the realized count (Section 1).

## 9. Cost ledger (executed work of C)

| term | basis | units | log2 | share |
|---|---|---:|---:|---:|
| M | 315870919550 instr x 7 | 1,033,222,634.04 | 29.945 | 31.73% |
| L | 240400504458 instr x 5 | 561,683,421.63 | 29.065 | 17.25% |
| S | 184954807110 instr x 5 | 432,137,399.79 | 28.687 | 13.27% |
| O | max(cap N = 2522586633 trials = 360369519 batches x 2235 ops = 3.764e+08 units; native run, 180672018863 instr x 5) = the latter (realized 109081798 trials) | 422,130,885.19 | 28.653 | 12.96% |
| DEVSHA | 883434924 instr x 400 (the freeze hashing: 2 hash-list and 6 single-file shasum runs) | 165,128,023.18 | 27.299 | 5.07% |
| DEVPY | 873920176 instr x 400 (vpair.py x2 (official-verifier check of the pair, re-measurement)) | 163,349,565.61 | 27.283 | 5.02% |
| DEVPY | 592889844 instr x 400 (pchar.py x2 (conversion check, re-measurement)) | 110,820,531.59 | 26.724 | 3.40% |
| DEVPY | 592077591 instr x 400 (pubchar.py x3 (two conversion checks before the freeze, one re-measurement)) | 110,668,708.60 | 26.722 | 3.40% |
| DEVPY | 413621536 instr x 400 (inline print of c.json x2) | 77,312,436.64 | 26.204 | 2.37% |
| A | 19919547288 instr x 5 | 46,540,998.34 | 25.472 | 1.43% |
| C0 | 200191633 instr x 400 | 37,418,996.82 | 25.157 | 1.15% |
| DRV | 3e+09 instr x 25 | 35,046,728.97 | 25.063 | 1.08% |
| HP | hit path at its caps K 5008628, T 13404930, W 30269, A 64 | 30,047,093.79 | 24.841 | 0.92% |
| DRVSHA | 100764691 instr x 400 (the driver's shasum run) | 18,834,521.68 | 24.167 | 0.58% |
| OSETUP | 5094440758 instr x 5 | 11,902,898.97 | 23.505 | 0.37% |
| DEVC | 35037410 instr x 16 (cglue char x2 (conversion check, re-measurement)) | 261,961.94 | 17.999 | 0.01% |
| C1 | 17193583 instr x 16 | 128,550.15 | 16.972 | 0.00% |
| C3 | 13318419 instr x 17 | 105,800.52 | 16.691 | 0.00% |
| B | 2^24 word clears + 8 ops/tuple | 29,163.48 | 14.832 | 0.00% |
| R | replay of the stored pair | 6.36 | 2.669 | 0.00% |
| **total** | | 3,256,770,328 | **31.6008** | |
claim (rounded up to 0.01): 31.61 ; max RSS 814366720 (2^29.601)

Notes on the terms:
- **Instruction-priced lines** are retired instructions times the per-instruction price of the program class (H3,
  Section 14):
  - the solver at 7 (the price rule's 6.5, raised to cover its unmeasured uncovered remainder; Section 14);
  - our C programs at 5, except cglue char at 16 and cglue sp at 17;
  - every Python process at 400, that is, every instruction priced as a multiply.
- **O** is the larger of two amounts (H2):
  - the counted SWAR batch (2,235 primitives per 7 trials; the organizer experiment executes it) times the
    360,369,519 batches of the cap N;
  - the instructions the online process retired outside its setup, at price 5.

  The latter is larger.
- **HP** is the hit path at its global caps:
  - each key match is 1 unit plus 512 ops;
  - each tuple test is 512 ops;
  - each W6 pass is 1,024 + 2 x 64 x 128 ops;
  - each of the 64 completion calls is charged at its full draw caps (64 x 2^16 E13 tries and 2^16 W15 tries at
    160 ops each), plus 512 ops for each of the 64 G16 elements (the s1-inverse of a kept element is a 32-step loop)
    and 35 units for at most 16 candidate re-hashes.
- **DEVPY and DEVC** are the conversion checks run before the freeze, and the official-verifier check and
  re-measurement runs made after the pair existed. The pre-freeze runs and the first vpair.py run were not measured:
  each repetition is charged at the measured instruction count of one identical re-run (dev_runs.tsv, Appendix C).
- **DRV** is an allowance of 3e9 instructions at 25. It covers:
  - the driver `run_v8.sh`;
  - `/usr/bin/time` and `nice`;
  - the small tools (grep, awk, tail, date, mkdir, sleep, sysctl, cut);
  - the lock and load polls;
  - the shell commands that extracted the cell table before the freeze.

  Measured on this machine, a small tool retires 1.05-1.27e7 instructions and `/usr/bin/time` + `nice` about 2e7.
  The driver started about 102 such processes (plus 8 `nice` + `/usr/bin/time` pairs), plus 4 lock polls while S
  waited for the shared lock. With the table-extraction commands (about 11 processes) the estimate is about 1.7e9.
  **DRVSHA** is the driver's one `shasum` (a Perl script) run, measured at 100,764,691 instructions and priced at 400
  like Python. **DEVSHA** is the freeze hashing before the chain: two runs over the hash list (139,423,389
  instructions each) and six single-file `shasum` runs (100,764,691 each), measured by identical re-runs and priced
  at 400.
- **B** is the bitmap build: 2^24 word clears plus 8 ops per tuple. **R** is the replay.

The pre-registration states that the claim is the realized executed work. The cap charge of O and HP is more than
that, never less.

Sensitivities (each changes only the stated line):

| change | total |
|---|---:|
| none (the claim) | 2^31.6008 |
| online at its realized counts (counted-SWAR-equivalent batches of the realized trials, realized hit path) instead of the charge above | 2^31.3935 |
| online at one compression + 32 ops per trial for all N = 2522586633 trials | 2^32.3290 |
| online native instructions extrapolated to the cap N (1656 instructions per trial, price 5) | 2^33.5523 |
| solver price doubled (7 -> 14) | 2^31.9983 |
| every C price doubled (S, L, A, C1, C3, v6on setup, native online) | 2^32.1396 |
| every Python process at 1024 per instruction instead of 400 | 2^31.9103 |
| driver allowance x 10 (3e10 instructions at 25) | 2^31.7342 |
| H1: the characteristic's discovery charged at T = 2^32 units | 2^32.8142 |
| H5: the two NEXP frontier runs of v7's development charged (4.39e12 instructions at 5) | 2^33.6542 |
| H5: v7's whole economics study charged (20 runs, 6.59e12 instructions at 5) | 2^34.1180 |
| the post-hoc measurement runs charged at 7 (about 6.9e12 instructions; Section 15) | 2^34.5882 |
| H5: the 2026-10-07 known-answer checks MW and MU charged (4.44e11 instructions at 7) | 2^32.1332 |
| H5: the whole 2026-10-07 in-chain design attempt charged (6.82e11 instructions at 7) | 2^32.3535 |
| H5: all of our earlier computation on this target charged (at most about 2^41.31) | 2^41.3102 |

## 10. Memory and advice

Peak memory over C was measured with `/usr/bin/time -l` on every process. The largest maximum resident set size was
814,366,720 bytes (the online process, which holds the 2^29-byte key bitmap). That is 2^29.601.

While the online process runs, phase A's 485 files (483 tables, advlist.txt and rate.txt) and the chain's other
intermediate files stay on disk. Those
retained precomputed data take 155,110,151 bytes. RSS plus retained data is 969,476,871 bytes = 2^29.853, and the
real-machine figure. The time prices assume the cost model's word-RAM layout, in which every datum occupies its own
256-bit word. Under that layout every datum of at least one byte grows at most 32-fold. So memory is at most
32 x 969,476,871 bytes = 2^34.853, and the claim is 34.9. Memory is reported only and does not enter the
score.

The advice of R is the stored 256-byte pair (2^8 bytes); 9 is claimed as a rounded-up bound, as in 50592e75. The published characteristic is not
advice. It is public algorithm text (H1), shipped as part of C's source (`pubchar_table.txt`, Appendix B) and counted
with the code.

## 11. Heuristics

**H1-public-characteristic (score-critical).** The published 31-step signed characteristic of Li, Liu, Wang, Dong and Sun (ASIACRYPT 2024; the cell table of proof.md Section 5, as transcribed in the promoted filing 50592e75) is public algorithm text that C may use without charging its original discovery. C uses only its signed-difference cells (rows A5..A12 and E5..E12 as hints of model M and checks of phases L and A) and the modular message differences d5..d9, d16, d18 that those cells imply. It is a table of difference and bit conditions, not a collision or a solution; C does not use its value cells.

- Scope: The characteristic only. No published colliding pair, starting point or first block, and none of the characteristic's 180 value cells, is used anywhere in C. The stored pair follows every A and E signed row and every W modular difference of the characteristic (proof.md Section 4).
- Limitations: The trail search is not executed or bounded by our own evidence in this filing; the cell table is the transcription of the presentation slide in 50592e75, and we did not re-check it against the paper (the stored pair verifies, so the cells C uses are consistent). A charge of T units adds T to the 3,256,770,328-unit total: the rounded claim holds for T up to 2.08e+07 units; the total stays below 2^32 for T up to 1.03e+09 units and below 2^34 for T up to 1.39e+10 units.
- Support: The characteristic is printed in the cited publication and is the only external input of the promoted r31 record 50592e75, which uses it under the same premise. Every value-level object in C (the starting point, the local-search family, the tables, the first block and the completion) is computed and charged by C itself (proof.md Sections 7-9).

**H2-op-accounting (score-critical).** The online phase O is charged at the larger of (a) the counted 7-lane x 36-bit SWAR batch (experiments/v8check.py Swar.batch; same op sequence and count as swar31.py), 2,235 primitives per 7 trials, times the 360,369,519 batches of its pre-computed trial cap N = 2,522,586,633, and (b) the 180,672,018,863 instructions its process retired outside the setup, at price 5. Its hit path is charged at its global caps with the per-event bounds of proof.md Section 9 (each key match 1 unit + 512 ops; each tuple test 512; each W6 pass 1,024 + 2 x 64 x 128; each of the 64 completion calls at its full draw caps, plus 512 ops per G16 element and 35 units). The bitmap build is charged at 2^24 word clears + 8 ops per tuple.

- Scope: Phase O of the chain (one execution, key 1) and its bitmap build.
- Limitations: The executed program v6on evaluates each trial with a scalar 31-step compression; the SWAR batch is a different implementation of the same per-trial test (key = chaining-value word 0), and term (b) charges what actually ran. Term (a) counts each batch's 16 first-block words as 16 uniform-random-word primitives; v6on derived them by AES-128-CTR under the public pre-registered key (two AES blocks per word), whose instructions are charged in term (b). The rate model and N treat these words as uniform (H6). The validity of the pair does not depend on this, and term (b) is the larger term. Extrapolating the native count to all N trials at price 5 gives 2^33.56 (proof.md Section 9).
- Support: The organizer experiment is designed to execute the counted SWAR batch on every trial (its Swar.batch is the charged program: the same op sequence and count as swar31.py's, with the key extracted by a single-lane mask and the bitmap probe computed), compare all 7 lanes' key and full chaining value with a scalar compression, and run the probe; it had not been executed by the organizer at filing time, and the local runs are participant evidence. Its trial 0 re-derives the stored M0 from the pre-registered key-1 AES-CTR stream (batch 15,645,968, lane 1). The 2,235 count is derived from the source in proof.md Section 12. The native online loop's price was measured by coverage on a bounded segment of the same binary and table (raw 3.074 per instruction, Section 14).

**H3-instruction-price (score-critical).** Primitive 256-bit word operations per retired AArch64 instruction bound the work of the instruction-priced processes: the solver run of phase M at 7 (the rule's 6.5 raised to cover its unmeasured uncovered-remainder mix); sets, ls2, tabm and the v6on setup and native online loop at 5; cglue char at 16 and cglue sp at 17; every Python and Perl (shasum) process at 400; the driver allowance of 3e9 instructions (an estimate, not a measurement; our count is about 1.7e9) at 25.

- Scope: The retired-instruction counts of proof.md Section 8 (macOS counters through /usr/bin/time -l) of every process of C and of the charged checks.
- Limitations: The prices come from coverage-instrumented runs of the same sources on the same inputs (proof.md Section 14), not from traces of the uninstrumented binaries. The native online loop was measured on a bounded segment of 1,835,008 trials. Python and the driver allowance are not measured; they are priced at 400 and 25. Doubling every solver price or every C price, or pricing Python at 1024, gives the sensitivities of proof.md Section 9.
- Support: Per-form costing uses jungjipdo's table a64ops_jj: ordinary forms 1 to 6 primitives plus address and operand-modifier terms, SIMD forms 16, multiply and floating-point arithmetic, compare and conversion 400, divide and square root 1024, and forms it does not recognise 1024. It runs over the executed basic blocks of instrumented builds with identical output (model-M solution and local-search family compared). Each price is the measured raw price times 1.15, rounded up to 0.5, and never below the prices of our filing 6d554419. Instructions outside the covered code are priced at 4, with the guard-callback length read from the disassembled runtime (11, plus a 3-instruction stub for the solver's dylib). Measured raw prices: solver 5.514, sets 3.910, ls2 3.216, tabm 3.766, v6on setup 3.732, v6on online loop 3.074; 1.15 x raw is at most the charged price for every program (solver 6.34 against the rule's 6.5; the solver is charged 7). Python is priced as if every instruction were a multiply.

**H4-memory (supporting).** Peak memory over C, counting the online process's resident set and the retained on-disk precomputed data, and allowing every datum its own 256-bit word as in the priced word-RAM layout, is at most 2^34.9 bytes.

- Scope: All processes of C.
- Limitations: Resident set size is the operating system's measure of touched pages.
- Support: The largest measured maximum resident set size was 814,366,720 bytes (the online process, which holds the 2^29-byte key bitmap); phase A's tables and the other intermediate files retained on disk take 155,110,151 bytes; together 2^29.853 on the real machine. Under the word-RAM layout every datum of at least one byte grows at most 32-fold: 2^34.853.

**H5-chain-scope (score-critical).** Every input of C is the published characteristic (H1), the output of a charged process of C, or one of five design constants (NEXP = 64, J = 2, T11 = 200, MCS = 2^22, rate seed 0076364172617465) carried over byte-identically from our v7 chain on our own characteristic 8_14 and pre-registered (proof.md Appendix A). None of these constants selected the stored pair: within the ranges of proof.md Section 15 the pair is unchanged (J >= 2 is needed; invariance in J is not claimed). NEXP did not lower the charge: the projected luck-free total is lowest at NEXP = 40, not at the reused 64. J's effect on the charge is not analysed. Every process of C, and everything before it that used the published cell table, is charged. Our earlier computation on this target never used the published cell table. It ran our own characteristics and search models; some of their checks fixed constants equal to quantities of the published characteristic (proof.md Section 15). Apart from the carried-over programs and constants, C reads none of it, and it is excluded.

- Scope: All computation on this target in our working directories and session records, listed in proof.md Sections 8 and 15.
- Limitations: The design constants (NEXP = 64, J = 2, T11 = 200, MCS = 2^22, the rate seed 0076364172617465) are byte-identical to the driver line of our earlier chain (filing 6d554419, on our own characteristic 8_14) and were fixed before any computation on the published characteristic. In that development NEXP = 64 was chosen as the SWAR-cost optimum of a measured 8_14 frontier (two 400-expansion ls2 runs, 4.39e12 instructions) and J = 2 in the same economics study; charging those two runs gives 2^33.66, the whole study 2^34.12. On the published characteristic 64 is not the optimum: the projected luck-free total over NEXP = 24..64 is 2^31.53..2^31.58, lowest at 40 (proof.md Section 15), and every NEXP in [24, 64] gives the same pair. The records are local and not notarised. If a reviewer charged all of our earlier computation on this target anyway, the total would be at most about 2^41.3.
- Support: The hash list of the pre-registration (proof.md Appendix A) is dated 07:53:38Z, and the first chain process started at 07:53:43Z; all 22 listed hashes still match the shipped files. Before the freeze, the only computation that used the published cell table was the conversion check (output files 07:52:45Z; charged as DEVPY and DEVC) and the shell commands that extracted and displayed the cell table (charged in DRV). Section 15 gives, for each constant, why the pair does not depend on it. The pair is the same for every NEXP in [24, 64], since breadth-first local search gives a prefix family and the pair's starting point 233 is added by expansion 24. It is the same for every T11 >= 200, since every starting point reached J = 2. It is the same for every MCS and seed with N >= 109,521,783, about 23 times below the computed N, since these set only the cap. The online key is re-derived by the organizer experiment.

**H6-rate-model (supporting).** Phase A's rate model q = T x |V6|/2^32 x 2^-32 x p20 (p20 from 2^22 seeded samples) is not an overestimate of the per-trial success rate of the online phase. Its cap N = 2/q therefore gives model success at least 1 - e^-2 for one key, and term (a) of H2 is, under H7, a luck-free online charge.

- Scope: The cap N, the hit-path caps and term (a) of the online charge; not the validity of the pair, which is verified, and not term (b).
- Limitations: The key-match factor assumes a uniform chaining-value word 0; the online words come from AES-128-CTR under a public key. If q overestimated the rate by a factor X, term (a) would rise to X x 3.764e8 units: it stays below the charged term (b) for X up to 1.12, and X = 2 gives 2^31.75.
- Support: Every factor was measured after the run on 2^30 synthetic key-matched trials with the shipped complete() and test_trial() (its success branch replaced by a counter; post/pcomp.diff, proof.md Section 16). Tuples per key match: 2.6777, equal to T/#keys. W6 pass: 2^-9.0008. Step-20 pass: 2^-11.6545 against p20 = 2^-11.6758. Completion success: 1,741 of 1,741. Accepts per key match: 2^-19.2343 against the model's 2^-19.2548. The online run's own counters agree: 54,474 key matches against 54,102 expected, and 291 W6 passes against 284.6.

**H7-packed-word-pricing (score-critical).** Under collision-frontier-v5 a word-RAM program that evaluates seven trials' 31-step compressions in 7 x 36-bit lanes of 256-bit words is charged by its counted primitives (2,235 per 7 trials, 0.149 units per trial); the model prices every 256-bit word operation at 1/C and does not restrict operand packing.

- Scope: Term (a) of the online charge, the luck-free floor. The claimed total depends on it through the max: term (b), the executed native run at about 3.9 units per trial, binds only because term (a) is priced under H7. Without H7, term (a) at one compression + 32 ops per trial over N binds instead.
- Limitations: The same packing premise is used by other filings on this track and on sha256-r32; we cite no organizer ruling. Without it, the luck-free online charge at one compression + 32 ops per trial would give 2^32.33 at the cap N (proof.md Section 9).
- Support: The cost model's computation_model prices word operations at 1/C per 256-bit word. The counted program is executable and checked lane by lane against scalar compressions in the organizer experiment; the 2,235 count is derived from the source in proof.md Section 12.


## 12. Organizer-executed experiment and certificate

- `certificates/`: the stored pair (`v8-pair`). The official verifier gives equal digests.
- `experiments/v8check.py` (`v8-pair-and-swar-batch`, stdlib only):
  - **Trial 0** returns the stored pair. It also re-derives M0 from the pre-registered online key: the first 16 bytes
    of SHA-256("sha256-r31-v8 online key 1"). A pure-Python FIPS-197 AES-128, self-tested on the C.1 vector, runs in
    v6on's batch layout: word i of batch b is AES_k(32b+2i) || AES_k(32b+2i+1), and lane l is bits [36l, 36l+32).
    The check is batch 15,645,968, lane 1. The observation `m0_from_online_key_stream` reports the result. This ties
    the stored pair to the pre-registered key-1 run.
  - **Every trial** runs the counted SWAR batch of `swar31.py`, the program behind term (a) of H2. It runs on 16
    pseudo-random 256-bit words derived from the organizer seed by SHAKE-256, in place of v6on's AES-CTR words, which
    the cost model's RAND primitive stands for. It compares all 7 lanes' key and full chaining value with a scalar
    31-step compression. It then runs the batch's bitmap probe against a per-trial synthetic bitmap that holds the
    scalar keys of lanes 0..3 only.
  - The executed online program v6on evaluates the same per-trial key, chaining-value word 0, with a scalar
    compression. It is charged by its instructions, term (b).

  Local run of 256 trials (0.22 s): the pair collides under the official verifier and `m0_from_online_key_stream`
  is true. Every trial reports 2,235 counted primitives (rand 16, load 47, add 263, and 792, or 246, xor 308, shift 543,
  cmp 7, branch 13; 56 registers), 7/7 lanes equal and 7/7 probes correct. The experiment makes no probability or
  cost inference.

The 2,235 count is input-independent, because the batch has no data-dependent branch. It follows from the source:

| part | primitives |
|---|---:|
| prologue: 16 rand + 16 and (lane masks) + 8 IV loads | 40 |
| schedule t = 16..30: 15 x (sigma1 14 + sigma0 14 + 3 add + 1 and) | 480 |
| rounds t = 0..30: 31 x (Sigma1 17 + Ch 4 + 1 K load + 4 add + Sigma0 17 + Maj 5 + 1 add + 2 add + 2 and) | 1,643 |
| feed-forward of word 0: load, add, and | 3 |
| key extraction: 7 x (shift, and with the single-lane mask) | 14 |
| bitmap probe: 7 x (shift, load, and, shift, and, cmp, branch) | 49 |
| batch control | 6 |
| **total** | **2,235** |

A ROTR is 2 shifts, 2 ands and 1 or. Every lane operand stays below 2^32 after its mask, and a sum of at most 7 lane
words stays below 2^35, inside the 36-bit lane, so no carry crosses lanes.

## 13. Sources and credit

- **Cryptanalysis and characteristic:** Li, Liu, Wang, Dong, Sun (ASIACRYPT 2024) and Li, Liu, Wang (EUROCRYPT
  2024), with [MNS13].
- **The cell-table transcription, the replay-chain framing and R20:** jungjipdo (50592e75, promoted); also the
  per-form AArch64 price table `a64ops_jj` behind our prices.
- **Model M, the local-search move set and completions:** USCMig (f94a3f75).
- **Fresh first block per trial, flat charge and global caps:** jagnani73 (654cb3d2).
- **SWAR online:** Th0rgal (f310d44f); the 7 x 36 packing is from tekkac.
- **Model generator:** STP model conventions from Peace9911/sha_2_attack.
- **Solvers:** STP 2.4.1 and CryptoMiniSat 5.14.7.
- Everything else is our own work. `cglue`, `sets`, `ls2`, `tabm` and `v6on` (with their headers) are carried over
  from our filing 6d554419, changed only in the thread count of `sets` and `v6on`. `pubchar.py`, `run_v8.sh`, the
  ledger, the price scripts and the experiment are new.

## 14. Per-instruction prices (H3): our own evidence

Method (our filing 6d554419's, re-run on the exact v8 inputs after the pair existed; not part of C and not charged):

1. Coverage-instrumented builds of the solver and of each priced C program ran on the same input as in C, with identical output (`pc8/run.sh`, Appendix B; the model-M solution and the local-search family were compared and are identical).
2. `covprice.py` (solver) and `covprice2.py` (our C programs, which call the guard by its symbol name) price every executed instruction of the instrumented code with jungjipdo's per-form table `a64ops_jj`.
3. raw = (ops + 4 U) / plain, where plain = the retired instructions of the charged run and U = the instrumented run's instructions outside the covered code, priced at 4: U = instrumented total - (covered + instrumentation + callback x guard calls). The callback length is read from the disassembly of the counter runtime (libcov.c, Appendix B): 11 instructions on its fast path, linked statically into the C builds, plus a 3-instruction stub for the solver, whose runtime is a dylib.
4. The price is 1.15 x raw, rounded up to 0.5, and never below the price used in 6d554419.

| program | plain instructions | covered instructions | ops | heavy (mul/FP) | raw | 1.15 x raw | price |
|---|---:|---:|---:|---:|---:|---:|---:|
| m | 315,870,919,550 | 400,414,116,621 | 1,419,526,207,536 | 1,343,181,163 | 5.514 | 6.341 | 6.5 (rule; charged 7) |
| sets | 184,940,161,017 | 240,696,363,707 | 601,607,799,064 | 0 | 3.910 | 4.496 | 5 |
| ls2 | 240,400,504,458 | 308,271,255,182 | 631,980,636,601 | 10,431 | 3.216 | 3.698 | 5 |
| tabm | 19,919,547,288 | 22,027,398,722 | 53,473,729,668 | 5,380 | 3.766 | 4.330 | 5 |
| v6on | 5,094,440,758 | 5,757,433,033 | 12,136,262,345 | 5,122 | 3.732 | 4.292 | 5 |
| c1 | 17,193,583 | 886,020 | 9,781,218 | 20,030 | 13.558 | 15.592 | 16 |
| c3 | 13,318,419 | 17,796 | 36,202 | 0 | 14.445 | 16.612 | 17 |
| v6on online loop (bounded segment) | 3,040,617,187 | 3,102,759,588 | 8,985,114,704 | 2,304 | 3.074 | 3.535 | 5 |

Inputs of U (instrumented runs; pc8/*_cov.time and *_price.json, post/o*_cov.time and o*_price.json):

| run | instrumented total | covered | instrumentation | guard calls | callback | U |
|---|---:|---:|---:|---:|---:|---:|
| m | 1,640,915,921,282 | 400,414,116,621 | 135,968,727,816 | 73,141,539,917 | 14 | 80,551,518,007 |
| sets | 941,069,276,467 | 240,696,363,707 | 103,079,565,021 | 51,539,807,503 | 11 | 30,355,465,206 |
| ls2 | 860,014,388,441 | 308,271,255,182 | 77,585,149,277 | 39,899,769,630 | 11 | 35,260,518,052 |
| tabm | 84,840,144,744 | 22,027,398,722 | 8,818,957,196 | 4,419,124,766 | 11 | 5,383,416,400 |
| v6on | 28,119,449,713 | 5,757,433,033 | 2,715,265,806 | 1,629,793,657 | 11 | 1,719,020,647 |
| c1 | 59,345,163 | 886,020 | 378,707 | 204,220 | 11 | 55,834,016 |
| c3 | 48,170,936 | 17,796 | 9,471 | 5,108 | 11 | 48,087,481 |
| v6on setup + loop (post/ol) | 33,748,888,181 | 8,860,192,692 | 3,062,736,306 | 1,817,291,475 | 11 | 1,835,752,958 |
| v6on setup only (post/os) | 28,146,051,476 | 5,757,433,104 | 2,715,265,827 | 1,629,793,668 | 11 | 1,745,622,197 |

Calibrating the callback on ls2 instead (as 6d554419 did) gives 11.884 instructions per call; that would leave sets with a negative remainder, so it overstates the callback and is not used. sets was measured with its single-thread build (`sets1`, same loop body) at 184,940,161,017 plain instructions. The v6on setup was priced from a setup-only coverage run. The native online loop was priced separately, by `post/online_price.sh` (Appendix B). That script ran a copy of the v8 table directory with the trial cap reduced to 1,835,008 trials (262,144 batches), with one worker thread and a measurement key, both instrumented and plain, each with and without the loop, and took differences. The loop's raw price is 3.074 per instruction (1657 instructions per trial; the loop includes the AES-128-CTR instructions, aese/aesmc, which the per-form table prices at 16 each). That is below the charged 5. Python is not measured: every Python and Perl (shasum) instruction is charged at 400 (as a multiply). The driver allowance is 3e9 instructions at 25, about 1.8 times our estimate of 1.7e9 (Section 9).

The solver's uncovered remainder U (instructions outside the instrumented code, mostly library code) is not mix-measured. The solver is therefore charged at 7.0 rather than the rule's 6.5. 7.0 covers a raw price of 6.087, which holds even if every U instruction cost 6.24 (the covered code's own mean is 3.55).

The comments in r31.h ("No multiply, divide or floating point anywhere") and ls2.c ("development measurement only")
date from v7. tabm and v6on use floating point and division in setup and rate-model code, which the table counts as
heavy, and ls2 is phase L.

## 15. Development record and scope (H5)

**Timeline of all computation on the published characteristic.**
- 07:52:45Z: our first computation on the published cell table, the conversion check. It ran pubchar.py -> pchar.py -> an inline print ->
  cglue char into a scratch directory, and its output files carry that time. The pre-registration's wording "07:4xZ"
  was an estimate written before we looked.
- 07:53:12Z: the last edit of run_v8.sh (paths and key format; its constants line is byte-identical to v7's driver).
- 07:53:38Z: the freeze. The hash list is dated then, and every hash in it still matches the shipped files.
- 07:53:43Z onwards: the chain (Section 8).
- After the pair existed:
  - the official-verifier check (vpair.py, twice);
  - one re-run of the conversion check, to measure it;
  - the location of the found trial (post/findtrial.c);
  - the price measurements (Section 14);
  - the rate-model measurement (Section 16);
  - package checks.

The conversion checks and the verifier checks are charged as DEVPY and DEVC. The pre-freeze runs themselves were not
measured, so each is charged with the measured count of an identical re-run. Everything else before the chain that
used the cell table is charged too: the freeze's own hashing as DEVSHA, and the shell commands that extracted the cell table in DRV.

**Departure from pre-registration rule 1.** Rule 1 says every process run on the published characteristic is charged.
After the pair existed, measurement runs used the chain's inputs; nothing in C reads them, and none is charged:
- the price measurement (pc8: instrumented re-runs of M, S, L, A, the O setup, C1 and C3, plus the plain
  single-thread `sets1`): 3.74e12 retired instructions;
- the online-loop price runs: 7.5e10;
- the rate-model measurement (pcomp, with two smoke runs): 8.2e11;
- the trial location (findtrial): 1.72e10;
- a scan of every batch up to the found one without the early stop (allscan, below): 1.87e11;
- two runs of `sets_swar`, a counted SWAR re-implementation of S prepared for a later accounting: about 2e12;
- the experiment's local runs.

This follows the promoted 50592e75, which leaves price measurements and work after the pair uncharged. If these runs
(about 6.9e12 instructions) were charged at the solver's price of 7, they would add about 2.3e10 units, giving about
2^34.6.

The pc8 script's last loop (the C-program pricing) was re-run by hand at 08:07Z with covprice2.py, after covprice.py
had not found the C programs' guard symbol. The shipped script shows that loop as it was finally run.

**Earlier computation on this target** never used the published cell table. It ran on our own characteristics and
search models:
- v5 (unsubmitted): aK11_78 and aK12_77;
- the r31w development characteristics;
- filing 6d554419 (v7): its 15 SAT characteristics, including 8_14, which differs from the published characteristic
  in its A, E and W rows;
- after that filing's refutation, an in-chain characteristic-search design attempt (2026-10-07 20:08-20:42Z, 6.82e11
  instructions of solver smoke runs and checks of characteristic-search models).
  - Its two known-answer checks used constants equal to quantities of the published characteristic. The check
    "MW" fixed the published trail's message-difference weights (17, 2, 48), 2.28e11 instructions. The check "MU"
    fixed all seven [LLW24] generator values, 2.16e11.
  - As in all of v7's work, these are the generator's weight literals, not the cell table.
  - Nothing in that attempt ran on the cell table, and C reads none of its output.
  - Charging the two checks at the solver price 7 would add 1.45e9 units (about 2^32.13); charging the whole
    attempt, 2.23e9 units (about 2^32.35).

C reads none of that computation's outputs, apart from the carried-over design constants and programs below. Its
programs are v7's except for the thread count (one code line and one comment line in each of `sets.c` and `v6on.c`). The files new in v8 are pubchar.py, run_v8.sh, the ledger and price scripts, and the experiment.

**Origin and influence of every constant of C.** The stored pair is the first verified pair of the key-1 run. Only
one completion call happened in the whole run, so no earlier accept consumed completion coins. The run is a race of
12 threads, so batches below the found one could have been left unevaluated when it stopped. A post-hoc scan
therefore re-ran every batch 0..15,645,968 (109,521,783 trials) with the shipped test_trial() and complete(), without
the early stop (`post/allscan.diff`, Appendix B). It found exactly one accept and one verified pair, the stored pair
(j = 467, batch 15,645,968, lane 1, thread 8; Appendix C). So the stored pair is the lowest-index accept of the key-1
stream, independent of thread scheduling. It uses:
- starting point 233 (0-based), which local search added between expansions 17 and 24 (Appendix C: 198 starting
  points after 16 expansions, 240 after 24);
- that starting point's second completion (j = 467);
- trial lane 1 of batch 15,645,968, run by thread 8.

| constant | value | origin | influence on the stored pair |
|---|---|---|---|
| published characteristic | Section 5 | public (H1) | defines the target trail |
| NEXP (L) | 64 | v7 driver line; chosen on 8_14 as the SWAR-cost optimum of a measured frontier (below) | Local search is breadth first and deterministic, so a smaller NEXP gives a prefix of the same family. Every NEXP from 24 to 64 contains starting point 233 and its two completions. A smaller family has fewer accepts, so it still has no earlier completion call. The pair is the same for every NEXP in [24, 64]; only the charged L work and the cap N change. |
| J (completions per starting point) | 2 | v7 driver line | The pair uses the second completion, so J >= 2 is needed. J = 2 was fixed in v7 and was not chosen on this characteristic. |
| T11 (BFS limit per starting point) | 200 | v7 driver line | The BFS order is deterministic. Every starting point reached J = 2 within 200 nodes (966 = 2 x 483 completions), so any T11 >= 200 gives the same completions. |
| MCS, rate seed | 2^22, 0076364172617465 | v7 code | They set only the estimate p20 and hence the cap N. Any N >= 7 x 15,645,969 = 109,521,783 trials, about 23 times below the computed N, reaches the same pair. |
| thread count | 12 | pre-registered machine limit | It sets which thread runs a batch, and hence the completion coin stream (domain 1 + thread id). It was fixed in the pre-registration, before the run. |
| online key | SHA-256("sha256-r31-v8 online key 1") | pre-registered rule | fixes the first-block stream (Section 12 re-derives M0 from it) |

So none of the design constants selected the stored pair. Changing them within the ranges above changes only how much
charged work L, A and O do; the pair stays the same.

How they were chosen, on 8_14 in v7's development (its economics study):
- NEXP = 64 by a measured-frontier optimisation over two 400-expansion ls2 runs (4.39e12 instructions). Every stop
  between 48 and 400 expansions was within 0.2 bits of the optimum.
- J = 2 in the same study, which also ran J = 0 and J = 64 at 48 expansions.
- T11 = 200, MCS = 2^22 and the seed as design values.

On the published characteristic the reused NEXP gave the claim no advantage. The table projects the luck-free total
(term (a) in place of the realized term (b)) for each NEXP from L's own log and fam.txt (Appendix C): L in proportion
to its tail count, A to its starting points, the cap N = 2/q from the prefix family's tuple count with p20 unchanged,
and every other line as charged.

| NEXP | starting points | tuples | cap N | luck-free total |
|---:|---:|---:|---:|---:|
| 8 | 147 | 2,007,360 | 7,168,139,230 | 2^31.655 |
| 16 | 198 | 2,560,192 | 5,620,295,653 | 2^31.585 |
| 24 | 240 | 2,938,304 | 4,897,054,890 | 2^31.569 |
| 32 | 291 | 3,464,736 | 4,152,996,351 | 2^31.553 |
| 40 | 355 | 4,413,264 | 3,260,406,807 | 2^31.528 |
| 48 | 400 | 4,948,752 | 2,907,609,026 | 2^31.539 |
| 56 | 409 | 5,049,680 | 2,849,494,620 | 2^31.569 |
| 64 | 483 | 5,704,080 | 2,522,586,633 | 2^31.580 |

The minimum is at NEXP = 40; the reused 64 is 0.05 bits above it, and every NEXP from 24 to 64 yields the same pair. So, whatever motivated the v7 value, NEXP selected neither the pair nor a lower charge on this characteristic. J = 2, T11, MCS and the seed are design constants fixed before any computation on the published characteristic. The pair needs J >= 2, and J's effect on the charge is not analysed; the charged-anyway sensitivities of Section 9 cover it. Choosing NEXP inside the chain over these eight values would have added seven A runs on the prefixes, 196,570,676 units.

Two sensitivities:
- Charging the two frontier runs at price 5 would add 1.026e10 units, giving about 2^33.66.
- Charging the whole economics study (20 runs, 6.59e12 instructions) would add 1.54e10 units, giving about
  2^34.12.

**Sensitivity.** If a reviewer charged all of our earlier computation on this target anyway, the total would be at most
about 2^41.31. That bound is the sum of three ledgers, which may overlap:
- the v7 whole-development ledger, 2^40.72;
- v5's strict-model grid, 2^39.6;
- v7's evidence runs at their caps, 2^36.2.

## 16. Rate model (H6) and its measured factors

Phase A's rate model is q = T x |V6|/2^32 x 2^-32 x p20, with p20 = 1,282 / 2^22 from 2^22 seeded samples of the
step-20 condition. It sets the cap N = 2/q and the hit-path caps. It is not needed for the validity of the pair, which
is verified. It enters the claim only through term (a) of the online charge. We measured every factor after the pair
existed, with `post/pcomp.c` (Appendix B). That program is v6on.c with the online loop replaced by synthetic
key-matched trials. complete() is unchanged. test_trial() is unchanged except its success branch: a successful
completion is counted (csucc) and the loop continues, instead of re-hashing from the IV and stopping. The caps are
disabled.
- CV1[0] is a uniformly drawn distinct table key, which is its law given a bitmap hit;
- CV1[1..7] are uniform, from AES-CTR coins.

Over 2^30 = 1,073,741,824 such trials:

| factor | model | measured |
|---|---|---|
| tuples per key match | T / #keys = 5,704,080 / 2,130,185 = 2.6777 | 2.6777 (2,875,209,082 tuple tests) |
| W6 in V6 per tuple | 2^-9 | 2^-9.0008 (5,612,488 passes) |
| step-20 condition per W6 pass | p20 = 2^-11.6758 | 2^-11.6545 (1,741 accepts) |
| completion success per accept | 1 (not in q) | 1,741 / 1,741 (one-sided 99% lower bound 0.9974) |
| accepts per key match | 2^-19.2548 | 2^-19.2343 |

The model's tuples-per-key-match and step-20 values are at or below their measured values; step-20 is 1.5% below,
within one standard error of the 1,741 accepts (2.4%). The W6 model value 2^-9 is 0.06% above its measured 2^-9.0008,
which is consistent with exact. The product, accepts per key match, is 1.4% below its measurement. In interval terms,
q overestimates the per-trial rate by at most X = 1.03 (one-sided 95%) or 1.07 (99.9%). Both are below the X = 1.12
at which term (a) would bind (below). The key-match factor (#keys / 2^32) assumes a uniform CV1[0]. The online run's counters agree:
- 54,474 key matches against 109,081,798 x 2,130,185 / 2^32 = 54,102 expected (+1.6 standard deviations);
- 291 W6 passes against 145,709 x 2^-9 = 284.6 expected (+0.4 standard deviations).

With q confirmed, the model success of one key within N is 1 - e^-2 = 0.86. A q overestimate by a factor X would
raise term (a) to X times 3.764e8 units. Term (a) stays below the claimed term (b) for X up to 1.12; X = 2 gives 2^31.75.

## Appendix A. Pre-registration (written before the first chain process)

# sha256-r31 v8: pre-registration (written before any chain run on the published characteristic)

Written 2026-10-08 07:53Z. The hash list HASHES.txt (sources, binaries, the solver binary and library) was written
with this file; HASHES.sha256 records its own hash.

## Chain (one execution; `src/run_v8.sh OUT k`)
- C0 `pubchar.py`: the published LLWDS24 31-step signed characteristic (cell table `pubchar_table.txt`, 300 cells,
  120 signed) -> counterexample text. It replaces the characteristic search; no solver call.
- C1 `cglue char` (v7 code): signed rows, modular differences, model M (USCMig f94a3f75, full hints A5-12, E5-12).
- S `sets` (v7 code, 12 threads instead of 15): V6/V7/V8/G16 over 2^32.
- M STP 2.4.1 + CryptoMiniSat 5.14.7, one call, default seed.
- C3 `cglue sp`; L `ls2 ... 64 S 2` (v7 constants); A `tabm ... 2 200 4194304 0076364172617465` (v7 constants).
- O `v6on` (v7 code, 12 threads instead of 15), key k = first 16 bytes of SHA-256("sha256-r31-v8 online key k"),
  k = 1, 2, ... ; trial cap N computed by A; first verified pair stops the run.
- Design constants are those of the v7 chain (fixed on our own characteristic 8_14, before this file); none is
  chosen on the published characteristic.

## Rules
- Every process run on the published characteristic is logged in OUT/ledger_runs.tsv (retired instructions from
  /usr/bin/time -l) and charged, including failures and repeats. The development conversion check (pubchar.py ->
  pchar.py -> cglue char into scratch/, 07:4xZ) is also charged.
- If O reaches N with no pair, run O again with key k+1 on the same prefix (charged), until a pair is found.
- If a phase before O fails, record the failure (charged); a revised chain is then pre-registered as an addendum and
  everything it runs is charged too.
- The claim is the realized executed work of all runs (deterministic replay of the stored pair, success 1).


HASHES.txt (SHA-256 of every source, binary and the solver; TOOLS = the solver install prefix):

```
8cde995f502bc609e976ad8a5405e186e8aa9defa9551b0267a3d0efc2e01a5a  src/cglue.c
af212da0b3a170a15e38945491dcabbdc34cef4a07a89b5e2da4a8f704d4b1ef  src/ls2.c
f234d307da9c2b233f21c207796aa6f93bb60329af5c1ebe3407458be4da7e4b  src/pubchar.py
e843ac07bd0de9d5e19095ef478fe7ca0fd0415c10c81bc93a645c0280ee3e27  src/pubchar_table.txt
25f0dfd2f3becaca823ff49598d5b4c7254e8c219ad0505c93add76c6aa49c17  src/r31.h
7f44674b055e36797cf0db9fa63e20dac0865a819a5e346bdf0f483131f7a317  src/run_v8.sh
2023eda9ffa2a261fed8a1ce03f5fb8c61394939aa5a9bca260f8dcf94ab1237  src/sets.c
6d523b77ce8fd9ea91696d348e25fda19033c26e409c8526a8826c1271f139bf  src/swar31.py
f6a2ebcd444e37df0cc360b34f3ef660b1c33eaf0ee6d3972120fd786e3fce6c  src/swar_vm.py
c5d12e3830e713cc5d954d55e63da8834e4ac71ce9aea01c3d482be47c31c155  src/tabm.c
25a184af5d5a643f659f1ec7cff7022d47fa51e84c1b13b34326e8bc285b5d2b  src/v6aes.h
b7584e005ee3cc995f0abb223872fe19cd5dbaae9b8b2197b726e6408ea981e6  src/v6io.h
9f68d85348108a8fa5523b6caa228553a6cb88618c2e1cb64bfe6605c0bf8263  src/v6on.c
86a443c90747a08859891ef1a773f3744f4dc7e157d1bc5c772c781b24730e4f  src/vpair.py
a8162b8eab946e17a61f29b23636e82880fb2610dfb927aaa6c2d02119d35dee  bin/cglue
213302661e3ff9621fef9bd79c9bad5c409259e15ae12cd2028e09a85b2259bc  bin/ls2
338648e6839b5102788d8e305cddd930d6cacb56125dcb4263feb25c35b4d31c  bin/sets
60149e4e4ec4e2994132d1e2d2bb50a4d8f8165d11a8217bd35a726d32191699  bin/tabm
2b0e70e772a875ffa76027650cc656dba8863bd7b40169a7837454eea26d98a8  bin/v6on
d6f546f13d3c1366cd3609c09c68b5bb6e8ad4f155e1d53850fcbb48624527b6  TOOLS/bin/stp_simple
3d0821c8a60e0f682d33d6ef056d55af1120f5b2127406119280d1482d1e953f  TOOLS/lib/libgmp.10.dylib
17647857915d7b6b5c33654967f9f581a42bfba9be5634e7b7da2433ea70ed43  PREREG.md
```

SHA-256(HASHES.txt) = cacfd9302792a19a9e3962bdbb3edd0d284f0603f9a04c37e5f0a0bda71e9fcc, recorded at 2026-10-08T07:53:38Z. That is the hash of the file as written, with the solver's absolute install prefix; the text printed here, with TOOLS substituted, hashes to bd291b3c7c3d57369f1a1874e3b2451465da6d1c142ad2bacd7b9ab87e3cbb5d.


## Appendix B. Source

Build: `clang -O2 -o cglue cglue.c; clang -O2 -o sets sets.c -lpthread; clang -O2 -o ls2 ls2.c; clang -O2 -o tabm tabm.c; clang -O2 -mcpu=apple-m1 -o v6on v6on.c -lpthread` (Apple clang, arm64). Solver: STP 2.4.1 (`stp_simple`) with CryptoMiniSat 5.14.7, built from upstream sources. The instrumented C binaries of the price measurement were built from the same sources with `-fsanitize-coverage=trace-pc-guard` against libcov; their exact flags were not recorded. Their SHA-256 are listed in Appendix C. Each instrumented run's output equals the plain run's byte for byte (sets.txt, c.txt, m.cvc, the model-M solution, sp.txt, fam.txt, the 483 table files and rate.txt; advlist.txt up to its directory prefix).

Path abbreviations: absolute directory prefixes are replaced by placeholders in the printed text: V8 = the v8 work directory; V6B = the v6 (v7 chain) work directory; HSO = a checkout of the official HashSmash repository (its verifier/ is imported by vpair.py and swar_vm.py); R31W = the price-tool directory; TOOLS = the solver install prefix; HST = its parent tool directory; WS = the session workspace (heavy-job lock only). The SHA-256 in each heading is of the original file, as pre-registered in HASHES.txt; where a placeholder was substituted, the heading also gives the SHA-256 of the printed text.

### pubchar_table.txt (SHA-256 e843ac07bd0de9d5)

```
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
```

### pubchar.py (SHA-256 f234d307da9c2b23)

```
"""v8 phase C0: the published 31-step signed characteristic (LLWDS24, ASIACRYPT 2024; cell table
pubchar_table.txt) -> the counterexample text format that phase C1 (cglue char) parses, in place of a solver call.
Cells: '=' equal, '0'/'1' equal with that value, 'u' (x, x') = (0, 1), 'n' (1, 0). Only the signed-difference
cells enter the chain; the value cells ('0'/'1') are written as '=' (no difference): every value relation that the
attack needs is enforced exactly by model M (both copies) and by the table and online tests.
Encoding of the LLW24 model (as pchar.py reads it): (v, d) = (0, 0) '=', (1, 1) 'u', (0, 1) 'n'.
Usage: python3 pubchar.py pubchar_table.txt OUT_P.txt"""
import sys

M32 = 0xFFFFFFFF


def main(inp, outp):
    rows = {}
    for line in open(inp):
        if "|" not in line:
            continue
        i, a, e, w = [s.strip() for s in line.split("|")]
        rows[int(i)] = (a, e, w)
        assert len(a) == len(e) == len(w) == 32 and set(a + e + w) <= set("=01un"), line
    out = []
    ncell = nsign = 0
    for var, col in (("x", 0), ("y", 1), ("w", 2)):
        for step in range(0, 31):
            row = rows.get(step, ("=" * 32,) * 3)[col]
            for k, ch in enumerate(row):
                bit = 31 - k
                d = 1 if ch in "un" else 0
                v = 1 if ch == "u" else 0
                ncell += ch != "="
                nsign += d
                out.append("ASSERT( %s%s_%d_%d = 0b%d );" % (var, "v", step, bit, v))
                out.append("ASSERT( %s%s_%d_%d = 0b%d );" % (var, "d", step, bit, d))
    out.append("Invalid.")
    open(outp, "w").write("\n".join(out) + "\n")
    sys.stderr.write("C0: %d non-= cells, %d signed-difference cells\n" % (ncell, nsign))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
```

### run_v8.sh (SHA-256 7f44674b055e3679; printed text SHA-256 5608e2039ed38b88)

```
#!/bin/bash
# v8 chain driver for sha256-r31 (published characteristic, H1). Every phase runs under /usr/bin/time -l; its retired
# instructions, wall time and max RSS go to OUT/ledger_runs.tsv. Every run is charged, including failed ones.
# Heavy phases take the machine-wide heavy-job lock (shared with another session) and release it after the phase.
# Usage: run_v8.sh OUTDIR KEYINDEX [FROM]   (KEYINDEX k: online key = first 16 bytes of SHA-256("sha256-r31-v8 online key k"))
set -u
D=$1; KI=$2; FROM=${3:-C0}
S=V8
LOCK="WS/research/heavy.lock"
export DYLD_LIBRARY_PATH=TOOLS/lib
export PYTHONHASHSEED=0
STP=TOOLS/bin/stp_simple
NEXP=64; J=2; T11=200; MCS=4194304; ASEED=0076364172617465; OSETUP=100000000000
KEY=$(printf 'sha256-r31-v8 online key %s' "$KI" | shasum -a 256 | cut -c1-32)
mkdir -p "$D/adv"
ON=0
lock() { until mkdir "$LOCK" 2>/dev/null; do sleep 30; done; while [ "$(sysctl -n vm.loadavg | awk '{print int($2)}')" -gt 12 ]; do sleep 20; done; }
unlock() { rmdir "$LOCK" 2>/dev/null; }
run() {   # run PHASE HEAVY(0/1) STDOUT STDERR CMD...
    local ph=$1 hv=$2 o=$3 e=$4; shift 4
    [ "$ph" = "$FROM" ] && ON=1
    [ $ON = 1 ] || return 0
    [ "$hv" = 1 ] && lock
    local t0; t0=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    nice -n 10 /usr/bin/time -l "$@" > "$o" 2> "$e"
    local rc=$?
    [ "$hv" = 1 ] && unlock
    local ins rss real
    ins=$(grep "instructions retired" "$e" | tail -1 | awk '{print $1}')
    rss=$(grep "maximum resident set size" "$e" | tail -1 | awk '{print $1}')
    real=$(grep " real " "$e" | tail -1 | awk '{print $1}')
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$ph" "$t0" "$rc" "$ins" "$real" "$rss" "$*" >> "$D/ledger_runs.tsv"
    if [ $rc -ne 0 ]; then echo "FAIL phase $ph rc $rc" >> "$D/RESULT.txt"; exit 1; fi
}
run C0 0 "$D/c0.log" "$D/c0.err" python3 "$S/src/pubchar.py" "$S/src/pubchar_table.txt" "$D/p.out"
run C1 0 "$D/c1.log" "$D/c1.err" "$S/bin/cglue" char "$D/p.out" "$D/c.txt" "$D/m.cvc"
[ -f "$D/c.txt" ] && read -r d5 d6 d7 d8 d9 d18 < "$D/c.txt"
run S  1 "$D/s.log" "$D/s.err" "$S/bin/sets" "$d5" "$d6" "$d7" "$d8" "$d9" "$d18" "$D/sets.txt"
run M  1 "$D/m.out" "$D/m.err" "$STP" "$D/m.cvc"
run C3 0 "$D/c3.log" "$D/c3.err" "$S/bin/cglue" sp "$D/m.out" "$D/sp.txt"
run L  1 "$D/l.out" "$D/l.log" "$S/bin/ls2" "$D/c.txt" "$D/sets.txt" "$D/sp.txt" $NEXP S $J "$D/fam.txt"
run A  1 "$D/a.out" "$D/a.log" "$S/bin/tabm" "$D/c.txt" "$D/fam.txt" "$D/sets.txt" "$D/adv" $J $T11 $MCS $ASEED
[ "$KI" = "-" ] && { echo "prefix done" >> "$D/RESULT.txt"; exit 0; }
ON=0; FROM=O
run O  1 "$D/on_$KI.txt" "$D/on_$KI.err" "$S/bin/v6on" "$D/adv" "$KEY" "$D/on_$KI.pairs" "$OSETUP"
echo "online done key index $KI key $KEY" >> "$D/RESULT.txt"
```

### r31.h (SHA-256 25f0dfd2f3becaca)

```
/* r31v6 common definitions: SHA-256 step functions (FIPS 180-4), 31-step compression, helpers.
   No multiply, divide or floating point anywhere in the r31v6 programs (checked on the binaries). */
#ifndef R31_H
#define R31_H
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef uint32_t u32;
typedef uint64_t u64;

#define ROR(x, n) (((x) >> (n)) | ((x) << (32 - (n))))
#define BS0(x) (ROR(x, 2) ^ ROR(x, 13) ^ ROR(x, 22))
#define BS1(x) (ROR(x, 6) ^ ROR(x, 11) ^ ROR(x, 25))
#define SS0(x) (ROR(x, 7) ^ ROR(x, 18) ^ ((x) >> 3))
#define SS1(x) (ROR(x, 17) ^ ROR(x, 19) ^ ((x) >> 10))
#define IFF(x, y, z) (((x) & (y)) ^ (~(x) & (z)))
#define MAJ(x, y, z) (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))

static const u32 KK[64] = {
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82f5, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2};
static const u32 IV0[8] = {0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
                           0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19};

/* 31-step compression with feed-forward (reference, scalar) */
static inline void f31(const u32 cv[8], const u32 m[16], u32 out[8]) {
    u32 w[31];
    for (int t = 0; t < 16; t++) w[t] = m[t];
    for (int t = 16; t < 31; t++) w[t] = SS1(w[t - 2]) + w[t - 7] + SS0(w[t - 15]) + w[t - 16];
    u32 a = cv[0], b = cv[1], c = cv[2], d = cv[3], e = cv[4], f = cv[5], g = cv[6], h = cv[7];
    for (int t = 0; t < 31; t++) {
        u32 t1 = h + BS1(e) + IFF(e, f, g) + KK[t] + w[t];
        u32 t2 = BS0(a) + MAJ(a, b, c);
        h = g; g = f; f = e; e = d + t1; d = c; c = b; b = a; a = t1 + t2;
    }
    out[0] = cv[0] + a; out[1] = cv[1] + b; out[2] = cv[2] + c; out[3] = cv[3] + d;
    out[4] = cv[4] + e; out[5] = cv[5] + f; out[6] = cv[6] + g; out[7] = cv[7] + h;
}

/* differences of the sigma functions for an additive input difference */
static inline u32 ds0(u32 x, u32 d) { return SS0(x + d) - SS0(x); }
static inline u32 ds1(u32 x, u32 d) { return SS1(x + d) - SS1(x); }

/* splitmix64 without multiplication is not possible; r31v6 uses xorshift128+ style generators built
   from shifts/xors/adds only (all primitive operations of the cost model). */
typedef struct { u64 s0, s1; } rng_t;
static inline u64 rng_next(rng_t *r) {
    u64 x = r->s0, y = r->s1;
    r->s0 = y;
    x ^= x << 23;
    r->s1 = x ^ y ^ (x >> 17) ^ (y >> 26);
    return r->s1 + y;
}
/* seed from a 64-bit value by a fixed number of xorshift rounds (no multiplications) */
static inline void rng_seed(rng_t *r, u64 seed, u64 stream) {
    r->s0 = seed ^ 0x6a09e667f3bcc908ULL;
    r->s1 = stream ^ 0xbb67ae8584caa73bULL;
    if (!r->s0 && !r->s1) r->s1 = 1;
    for (int i = 0; i < 32; i++) rng_next(r);
}

static inline u32 hexarg(const char *s) { return (u32)strtoul(s, NULL, 16); }
#endif
```

### v6io.h (SHA-256 b7584e005ee3cc99)

```
/* v6 I/O helpers for the charged C phases: no libc formatting or parsing (no printf/scanf/strtoul), no multiply,
   divide or floating point. Files are read whole with fread and written whole with fwrite; numbers are parsed and
   printed by shift/add/compare code that the coverage price measurement sees. */
#ifndef V6IO_H
#define V6IO_H
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { char *p; size_t n, cap; } ob_t;     /* output buffer */
static void ob_grow(ob_t *b, size_t add) {
    if (b->n + add + 1 <= b->cap) return;
    size_t c = b->cap ? b->cap : 4096;
    while (c < b->n + add + 1) c += c;
    b->p = realloc(b->p, c); if (!b->p) { fputs("io: oom\n", stderr); exit(3); } b->cap = c;
}
static inline void ob_put(ob_t *b, const char *s, size_t l) { ob_grow(b, l); memcpy(b->p + b->n, s, l); b->n += l; b->p[b->n] = 0; }
static inline void ob_s(ob_t *b, const char *s) { size_t l = 0; while (s[l]) l++; ob_put(b, s, l); }
static inline void ob_c(ob_t *b, char c) { ob_grow(b, 1); b->p[b->n++] = c; b->p[b->n] = 0; }
static inline void ob_hex8(ob_t *b, uint32_t x) {           /* %08x */
    static const char H[16] = "0123456789abcdef"; char t[8];
    for (int i = 7; i >= 0; i--) { t[i] = H[x & 15]; x >>= 4; }
    ob_put(b, t, 8);
}
static inline void ob_u64(ob_t *b, uint64_t x) {            /* %llu, by subtraction of powers of ten */
    static const uint64_t P10[20] = {10000000000000000000ULL, 1000000000000000000ULL, 100000000000000000ULL,
        10000000000000000ULL, 1000000000000000ULL, 100000000000000ULL, 10000000000000ULL, 1000000000000ULL,
        100000000000ULL, 10000000000ULL, 1000000000ULL, 100000000ULL, 10000000ULL, 1000000ULL, 100000ULL, 10000ULL,
        1000ULL, 100ULL, 10ULL, 1ULL};
    int started = 0;
    for (int k = 0; k < 20; k++) {
        char d = '0';
        while (x >= P10[k]) { x -= P10[k]; d++; }
        if (d != '0' || started || k == 19) { ob_c(b, d); started = 1; }
    }
}
static inline void ob_i(ob_t *b, int x) { if (x < 0) { ob_c(b, '-'); x = -x; } ob_u64(b, (uint64_t)x); }
static int ob_write(const ob_t *b, const char *path) {
    FILE *f = fopen(path, "w"); if (!f) return -1;
    size_t w = b->n ? fwrite(b->p, 1, b->n, f) : 0; fclose(f); return w == b->n ? 0 : -1;
}

typedef struct { const char *p, *e; } ib_t;               /* input cursor over a whole file */
static char *slurp(const char *path, size_t *len) {
    FILE *f = fopen(path, "r"); if (!f) return NULL;
    size_t cap = 1 << 16, n = 0; char *buf = malloc(cap);
    for (;;) {
        if (n + 65536 + 1 > cap) { cap += cap; buf = realloc(buf, cap); if (!buf) { fclose(f); return NULL; } }
        size_t r = fread(buf + n, 1, 65536, f); n += r; if (r < 65536) break;
    }
    fclose(f); buf[n] = 0; if (len) *len = n; return buf;
}
static inline void ib_ws(ib_t *c) { while (c->p < c->e && (*c->p == ' ' || *c->p == '\n' || *c->p == '\t' || *c->p == '\r')) c->p++; }
static inline int ib_tok(ib_t *c, char *out, int max) {    /* next whitespace-delimited token */
    ib_ws(c); int l = 0;
    while (c->p < c->e && !(*c->p == ' ' || *c->p == '\n' || *c->p == '\t' || *c->p == '\r')) { if (l + 1 < max) out[l++] = *c->p; c->p++; }
    out[l] = 0; return l;
}
static inline int hexval(char ch) {
    if (ch >= '0' && ch <= '9') return ch - '0';
    if (ch >= 'a' && ch <= 'f') return ch - 'a' + 10;
    if (ch >= 'A' && ch <= 'F') return ch - 'A' + 10;
    return -1;
}
static inline int ib_hex(ib_t *c, uint32_t *x) {           /* %x (optional 0x prefix) */
    ib_ws(c); uint32_t v = 0; int n = 0;
    if (c->p + 1 < c->e && c->p[0] == '0' && (c->p[1] == 'x' || c->p[1] == 'X')) c->p += 2;
    while (c->p < c->e) { int h = hexval(*c->p); if (h < 0) break; v = (v << 4) | (uint32_t)h; c->p++; n++; }
    *x = v; return n > 0;
}
static inline int ib_u64(ib_t *c, uint64_t *x) {           /* %llu: x*10 = (x<<3)+(x<<1) */
    ib_ws(c); uint64_t v = 0; int n = 0;
    while (c->p < c->e && *c->p >= '0' && *c->p <= '9') { v = (v << 3) + (v << 1) + (uint64_t)(*c->p - '0'); c->p++; n++; }
    *x = v; return n > 0;
}
static inline int ib_int(ib_t *c, int *x) {
    ib_ws(c); int neg = 0; if (c->p < c->e && *c->p == '-') { neg = 1; c->p++; }
    uint64_t v; if (!ib_u64(c, &v)) return 0; *x = neg ? -(int)v : (int)v; return 1;
}
#endif
```

### v6aes.h (SHA-256 25a184af5d5a643f)

```
/* v6 shared: AES-128-CTR (ARMv8 crypto extension) and the SWAR-batch message layout. */
#ifndef V6AES_H
#define V6AES_H
#include <arm_neon.h>
/* ---------------- AES-128 (FIPS-197) with the ARMv8 crypto extension ---------------- */
static const uint8_t SBOX[256] = {
    0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
    0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
    0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
    0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
    0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
    0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
    0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
    0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16};
static uint8x16_t RK[11];
static void aes_expand(const uint8_t key[16]) {
    uint8_t w[176]; static const uint8_t rcon[10] = {1, 2, 4, 8, 16, 32, 64, 128, 27, 54};
    memcpy(w, key, 16);
    for (int i = 4; i < 44; i++) {
        uint8_t t[4]; memcpy(t, w + 4 * (i - 1), 4);
        if (i % 4 == 0) { uint8_t x = t[0]; t[0] = SBOX[t[1]] ^ rcon[i / 4 - 1]; t[1] = SBOX[t[2]]; t[2] = SBOX[t[3]]; t[3] = SBOX[x]; }
        for (int k = 0; k < 4; k++) w[4 * i + k] = w[4 * (i - 4) + k] ^ t[k];
    }
    for (int r = 0; r < 11; r++) RK[r] = vld1q_u8(w + 16 * r);
}
static inline uint8x16_t aes_enc(uint8x16_t b) {
    for (int r = 0; r < 9; r++) b = vaesmcq_u8(vaeseq_u8(b, RK[r]));
    return veorq_u8(vaeseq_u8(b, RK[9]), RK[10]);
}
/* counter block: bytes 0..7 = lo (little-endian), 8..15 = hi; output as two little-endian u64 */
static inline void aes_ctr(u64 lo, u64 hi, u64 out[2]) {
    uint64x2_t in = {lo, hi};
    uint8x16_t o = aes_enc(vreinterpretq_u8_u64(in));
    uint64x2_t r = vreinterpretq_u64_u8(o);
    out[0] = vgetq_lane_u64(r, 0); out[1] = vgetq_lane_u64(r, 1);
}
/* the 7 first blocks of SWAR batch b */
static void gen_batch(u64 b, u32 m[7][16]) {
    for (int i = 0; i < 16; i++) {
        u64 L[5];
        aes_ctr(32 * b + 2 * i, 0, L); aes_ctr(32 * b + 2 * i + 1, 0, L + 2); L[4] = 0;
        for (int l = 0; l < 7; l++) {
            int pos = 36 * l, idx = pos >> 6, off = pos & 63;
            u64 v = L[idx] >> off;
            if (off > 32) v |= L[idx + 1] << (64 - off);
            m[l][i] = (u32)v;
        }
    }
}
typedef struct { u64 dom, ctr, buf[2]; int left; } coin_t;
static inline u64 coin64(coin_t *c) {
    if (!c->left) { aes_ctr(c->ctr++, c->dom, c->buf); c->left = 2; }
    return c->buf[--c->left];
}

#endif
```

### cglue.c (SHA-256 8cde995f502bc609)

```
/* v6 phases C1 and C3 in C (cglue): byte-identical replacements of the Python glue
     C1:  cglue char P_OUT C_TXT M_CVC   = pchar.py (STP counterexample -> signed rows, modular differences)
                                           + prep.py char (C_TXT) + mgen.py (model M, full hints; M_CVC)
     C3:  cglue sp M_OUT SP_TXT          = prep.py sp (model-M solution -> A1..A4 E3..E12)
   mgen.py: model M after USCMig (package f94a3f75). No libc formatting/parsing, no multiply/divide/float.
   Acceptance: outputs byte-identical (sha256) to the Python programs on the same input. */
#include <stdarg.h>
#include "v6io.h"

static const uint32_t K[16] = {0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4,
    0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174};

static int ends_invalid(const char *t, size_t n) {   /* text.rstrip().endswith("Invalid.") */
    while (n && (t[n - 1] == ' ' || t[n - 1] == '\n' || t[n - 1] == '\t' || t[n - 1] == '\r')) n--;
    return n >= 8 && !memcmp(t + n - 8, "Invalid.", 8);
}
static int isdig(char c) { return c >= '0' && c <= '9'; }
static int iswc(char c) { return isdig(c) || (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '_'; }

/* ---------------- expression builders of mgen.py (strings in an arena) ---------------- */
static char *AR; static size_t AN, ACAP = (size_t)1 << 28;
static char *keep(const ob_t *b) { if (AN + b->n + 1 > ACAP) exit(4); char *r = AR + AN; memcpy(r, b->p, b->n); r[b->n] = 0; AN += b->n + 1; return r; }
static char *cat(int n, ...) { ob_t b = {0}; va_list ap; va_start(ap, n); for (int i = 0; i < n; i++) ob_s(&b, va_arg(ap, const char *)); va_end(ap); char *r = keep(&b); free(b.p); return r; }
static char *C(uint32_t x) { ob_t b = {0}; ob_s(&b, "0hex"); ob_hex8(&b, x); char *r = keep(&b); free(b.p); return r; }
static char *I(int x) { ob_t b = {0}; ob_i(&b, x); char *r = keep(&b); free(b.p); return r; }
static char *ror(const char *x, int n) { return cat(8, "(", x, "[", I(n - 1), ":0] @ ", x, "[31:", cat(2, I(n), "])")); }
static char *shr(const char *x, int n) { ob_t z = {0}; for (int i = 0; i < n; i++) ob_c(&z, '0'); char *zs = keep(&z); free(z.p); return cat(7, "(0bin", zs, " @ ", x, "[31:", I(n), "])"); }
static char *xor3(const char *a, const char *b, const char *d) { return cat(7, "BVXOR(BVXOR(", a, ", ", b, "), ", d, ")"); }
static char *S0(const char *x) { return xor3(ror(x, 2), ror(x, 13), ror(x, 22)); }
static char *S1(const char *x) { return xor3(ror(x, 6), ror(x, 11), ror(x, 25)); }
static char *s0(const char *x) { return xor3(ror(x, 7), ror(x, 18), shr(x, 3)); }
static char *IF(const char *x, const char *y, const char *z) { return cat(9, "((", x, " & ", y, ") | (~", x, " & ", z, "))"); }
static char *MAJ(const char *x, const char *y, const char *z) { return cat(13, "((", x, " & ", y, ") | (", x, " & ", z, ") | (", y, " & ", z, "))"); }
static char *add(int n, ...) {
    ob_t b = {0}; ob_s(&b, "BVPLUS(32, "); va_list ap; va_start(ap, n);
    for (int i = 0; i < n; i++) { if (i) ob_s(&b, ", "); ob_s(&b, va_arg(ap, const char *)); }
    va_end(ap); ob_s(&b, ")"); char *r = keep(&b); free(b.p); return r;
}
static char *sub(const char *a, const char *b) { return cat(5, "BVSUB(32, ", a, ", ", b, ")"); }
static ob_t DECL, ASRT; static int ndecl, nasrt;
static char *var(const char *n) { if (ndecl++) ob_c(&DECL, '\n'); ob_s(&DECL, n); ob_s(&DECL, " : BITVECTOR(32);"); return (char *)n; }
static void eq(const char *a, const char *b) { if (nasrt++) ob_c(&ASRT, '\n'); ob_s(&ASRT, "ASSERT("); ob_s(&ASRT, a); ob_s(&ASRT, " = "); ob_s(&ASRT, b); ob_s(&ASRT, ");"); }
static char *define(const char *n, const char *e) { var(n); eq(n, e); return (char *)n; }
static char *nmi(const char *p, int t) { return cat(2, p, I(t)); }

int main(int argc, char **argv) {
    AR = malloc(ACAP);
    if (argc == 5 && !strcmp(argv[1], "char")) {
        size_t n; char *t = slurp(argv[2], &n);
        if (!t || !ends_invalid(t, n)) { fputs("P: model not satisfiable / no counterexample\n", stderr); return 1; }
        /* pchar.py: ASSERT( ([xyw])([vd])_(\d+)_(\d+) = 0b([01]) ); */
        static unsigned char V[4][32][32], D[4][32][32];   /* power-of-two strides (no multiply) */
        for (const char *p = t; (p = strstr(p, "ASSERT( ")) != NULL; ) {
            p += 8;
            const char *q = p; int var_ = q[0] == 'x' ? 0 : q[0] == 'y' ? 1 : q[0] == 'w' ? 2 : -1;
            if (var_ < 0 || (q[1] != 'v' && q[1] != 'd') || q[2] != '_') continue;
            int kind = q[1] == 'v'; q += 3;
            int st = 0, nd = 0; while (isdig(*q)) { st = (st << 3) + (st << 1) + (*q - '0'); q++; nd++; }
            if (!nd || *q != '_') continue; q++;
            int bit = 0; nd = 0; while (isdig(*q)) { bit = (bit << 3) + (bit << 1) + (*q - '0'); q++; nd++; }
            if (!nd || strncmp(q, " = 0b", 5)) continue; q += 5;
            if (*q != '0' && *q != '1') continue;
            int val = *q - '0'; q++;
            if (strncmp(q, " );", 3)) continue;
            if (st < 31 && bit < 32) { if (kind) V[var_][st][bit] = (unsigned char)val; else D[var_][st][bit] = (unsigned char)val; }
            else if (st >= 31) { /* steps outside 0..30 are never read by pchar.py */ }
        }
        /* rows and modular differences */
        static char rows[4][32][64]; uint32_t diff[4][32];
        for (int v = 0; v < 3; v++) for (int s = 0; s < 31; s++) {
            uint32_t dd = 0;
            for (int b = 31; b >= 0; b--) {
                char c;
                if (!D[v][s][b]) c = '=';
                else if (V[v][s][b]) { c = 'u'; dd += (uint32_t)1 << b; }
                else { c = 'n'; dd -= (uint32_t)1 << b; }
                rows[v][s][31 - b] = c;
            }
            rows[v][s][32] = 0; diff[v][s] = dd;
        }
        uint32_t dw[16]; for (int s = 0; s < 16; s++) dw[s] = diff[2][s];
        uint32_t d18 = diff[2][18];
        /* prep.py char */
        ob_t o = {0};
        for (int s = 5; s <= 9; s++) { ob_hex8(&o, dw[s]); ob_c(&o, ' '); }
        ob_hex8(&o, d18); ob_c(&o, '\n');
        uint32_t um[2][13], nmk[2][13];
        for (int ae = 0; ae < 2; ae++) for (int s = 5; s <= 12; s++) {
            uint32_t u = 0, m = 0;
            for (int i = 0; i < 32; i++) { if (rows[ae][s][i] == 'u') u |= (uint32_t)1 << (31 - i); if (rows[ae][s][i] == 'n') m |= (uint32_t)1 << (31 - i); }
            um[ae][s] = u; nmk[ae][s] = m;
            ob_c(&o, ae ? 'E' : 'A'); ob_i(&o, s); ob_c(&o, ' '); ob_hex8(&o, u); ob_c(&o, ' '); ob_hex8(&o, m); ob_c(&o, '\n');
        }
        if (ob_write(&o, argv[3])) return 1;
        /* mgen.py */
        char *A[13], *E[13], *Ap[13], *Ep[13], *W[13];
        for (int s = 1; s <= 4; s++) A[s] = Ap[s] = var(nmi("A", s));
        for (int s = 3; s <= 12; s++) E[s] = var(nmi("E", s));
        Ep[3] = E[3]; Ep[4] = E[4];
        for (int s = 5; s <= 12; s++) A[s] = define(nmi("A", s), add(3, sub(E[s], A[s - 4]), S0(A[s - 1]), MAJ(A[s - 1], A[s - 2], A[s - 3])));
        Ep[5] = define("Ep5", add(2, E[5], C(dw[5])));
        Ep[6] = define("Ep6", add(4, E[6], sub(S1(Ep[5]), S1(E[5])), sub(IF(Ep[5], E[4], E[3]), IF(E[5], E[4], E[3])), C(dw[6])));
        Ep[7] = define("Ep7", add(4, E[7], sub(S1(Ep[6]), S1(E[6])), sub(IF(Ep[6], Ep[5], E[4]), IF(E[6], E[5], E[4])), C(dw[7])));
        Ep[8] = define("Ep8", add(4, E[8], sub(S1(Ep[7]), S1(E[7])), sub(IF(Ep[7], Ep[6], Ep[5]), IF(E[7], E[6], E[5])), C(dw[8])));
        for (int s = 5; s <= 8; s++) Ap[s] = define(nmi("Ap", s), add(3, sub(Ep[s], Ap[s - 4]), S0(Ap[s - 1]), MAJ(Ap[s - 1], Ap[s - 2], Ap[s - 3])));
        W[7] = define("W7", sub(sub(sub(sub(sub(E[7], A[3]), E[3]), S1(E[6])), IF(E[6], E[5], E[4])), C(K[7])));
        W[8] = define("W8", sub(sub(sub(sub(sub(E[8], A[4]), E[4]), S1(E[7])), IF(E[7], E[6], E[5])), C(K[8])));
        for (int s = 9; s <= 12; s++)
            W[s] = define(nmi("W", s), sub(sub(sub(sub(sub(E[s], A[s - 4]), E[s - 4]), S1(E[s - 1])), IF(E[s - 1], E[s - 2], E[s - 3])), C(K[s])));
        for (int s = 9; s <= 12; s++) {
            Ep[s] = define(nmi("Ep", s), add(7, Ap[s - 4], Ep[s - 4], S1(Ep[s - 1]), IF(Ep[s - 1], Ep[s - 2], Ep[s - 3]), C(K[s]), W[s], C(s == 9 ? dw[9] : 0)));
            Ap[s] = define(nmi("Ap", s), add(3, sub(Ep[s], Ap[s - 4]), S0(Ap[s - 1]), MAJ(Ap[s - 1], Ap[s - 2], Ap[s - 3])));
        }
        eq(sub(s0(add(2, W[7], C(dw[7]))), s0(W[7])), C(0u - dw[6]));
        eq(sub(s0(add(2, W[8], C(dw[8]))), s0(W[8])), C(0u - dw[7] - dw[9]));
        eq(sub(s0(add(2, W[9], C(dw[9]))), s0(W[9])), C(0u - dw[8]));
        eq(sub(Ap[10], A[10]), C(0u - d18));
        eq(Ap[11], A[11]);
        eq(Ap[12], A[12]);
        eq(add(4, A[9], E[9], S1(E[12]), IF(E[12], E[11], E[10])), add(4, Ap[9], Ep[9], S1(Ep[12]), IF(Ep[12], Ep[11], Ep[10])));
        eq(sub(MAJ(A[12], A[11], A[10]), A[9]), sub(MAJ(Ap[12], Ap[11], Ap[10]), Ap[9]));
        for (int ae = 0; ae < 2; ae++) for (int s = 5; s <= 12; s++) {
            const char *X = ae ? E[s] : A[s], *Xp = ae ? Ep[s] : Ap[s];
            uint32_t u = um[ae][s], m = nmk[ae][s], em = 0xFFFFFFFFu ^ u ^ m;
            eq(cat(7, "(BVXOR(", X, ", ", Xp, ") & ", C(em), ")"), C(0));
            if (u) { eq(cat(5, "(", X, " & ", C(u), ")"), C(0)); eq(cat(5, "(", Xp, " & ", C(u), ")"), C(u)); }
            if (m) { eq(cat(5, "(", X, " & ", C(m), ")"), C(m)); eq(cat(5, "(", Xp, " & ", C(m), ")"), C(0)); }
        }
        ob_t mo = {0}; ob_put(&mo, DECL.p, DECL.n); ob_c(&mo, '\n'); ob_put(&mo, ASRT.p, ASRT.n);
        ob_s(&mo, "\nQUERY(FALSE);\nCOUNTEREXAMPLE;\n");
        return ob_write(&mo, argv[4]) ? 1 : 0;
    }
    if (argc == 4 && !strcmp(argv[1], "sp")) {
        size_t n; char *t = slurp(argv[2], &n);
        if (!t || !ends_invalid(t, n)) { fputs("M: no solution\n", stderr); return 1; }
        static const char *names[14] = {"A1", "A2", "A3", "A4", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10", "E11", "E12"};
        uint32_t val[14]; int got[14] = {0};
        for (const char *p = t; (p = strstr(p, "ASSERT( ")) != NULL; ) {   /* ASSERT\( (\w+) = 0x([0-9A-Fa-f]+) \); */
            p += 8; const char *q = p; int l = 0; while (iswc(q[l])) l++;
            if (!l || strncmp(q + l, " = 0x", 5)) continue;
            const char *h = q + l + 5; uint32_t v = 0; int nh = 0; while (hexval(h[nh]) >= 0) { v = (v << 4) | (uint32_t)hexval(h[nh]); nh++; }
            if (!nh || strncmp(h + nh, " );", 3)) continue;
            for (int k = 0; k < 14; k++) if ((int)strlen(names[k]) == l && !strncmp(names[k], q, (size_t)l)) { val[k] = v; got[k] = 1; }
        }
        ob_t o = {0};
        for (int k = 0; k < 14; k++) { if (!got[k]) { fputs("M: missing value\n", stderr); return 1; } if (k) ob_c(&o, ' '); ob_hex8(&o, val[k]); }
        ob_c(&o, '\n');
        return ob_write(&o, argv[3]) ? 1 : 0;
    }
    fputs("usage: cglue char P_OUT C_TXT M_CVC | cglue sp M_OUT SP_TXT\n", stderr);
    return 2;
}
```

### sets.c (SHA-256 2023eda9ffa2a261)

```
/* r31v6 phase S: exact sets by enumeration of all 2^32 words (12 threads, one pass; passes 2-3 disabled: the
   attack tests the step-20 condition directly, no class list is needed).
   Usage: sets dW5 dW6 dW7 dW8 dW9 d18 OUT
   pass 1: V7 = {w : ds0_{dW7}(w) = -dW6}, V8 = {w : ds0_{dW8}(w) = -dW7 - dW9}, G16 = {x : ds1_{dW9}(x) = d18} (listed);
           |V6| = |{w : ds0_{dW6}(w) = -dW5}|, |V9| = |{w : ds0_{dW9}(w) = -dW8}| (counted);
           presence bitmap B of -ds1_{d18}(y) over all y (2^32 bits).
   pass 2: classes = {a = ds0_{dW5}(x) : B[a]} with H5(a) = |{x : ds0_{dW5}(x) = a}|.
   pass 3: H18(-a) = |{y : ds1_{d18}(y) = -a}| for every class a.
   Requires d18 + dW9 = 0 (dW25 = 0). */
#include "r31.h"
#include <pthread.h>
#include <stdatomic.h>

#define NT 12
#define LMAX (1u << 22)
#define CS (1u << 16)          /* class hash slots */
#define CMAX (1u << 14)        /* max classes */

static u32 dW5, dW6, dW7, dW8, dW9, d18;
static _Atomic u64 *B;          /* 2^32-bit presence bitmap */
static int pass;
static u32 ckey[CS]; static unsigned char cuse[CS];
static u32 clist[CMAX]; static u32 ncl;

static inline u32 cslot(u32 a) { return (a ^ (a >> 15) ^ (a << 9) ^ (a >> 23)) & (CS - 1); }
static inline int cfind(u32 a) {   /* slot+1 of class a, 0 if absent */
    u32 i = cslot(a);
    while (cuse[i]) { if (ckey[i] == a) return (int)i + 1; i = (i + 1) & (CS - 1); }
    return 0;
}

typedef struct {
    int id; u64 n6, n9;
    u32 *v7, *v8, *g16; u32 n7, n8, n16;
    u32 *seen; u32 nseen;        /* pass 2: distinct class values seen by this thread */
    u64 *cnt5, *cnt18;
    int overflow;
} job_t;

static void *work(void *p) {
    job_t *j = p;
    u64 lo = ((u64)j->id << 32) / NT, hi = ((u64)(j->id + 1) << 32) / NT;
    if (pass == 1) {
        u32 t7 = -dW6, t8 = -dW7 - dW9, t6 = -dW5, t9 = -dW8;
        for (u64 xx = lo; xx < hi; xx++) {
            u32 x = (u32)xx;
            if (ds0(x, dW6) == t6) j->n6++;
            if (ds0(x, dW9) == t9) j->n9++;
            if (ds0(x, dW7) == t7) { if (j->n7 < LMAX) j->v7[j->n7] = x; j->n7++; }
            if (ds0(x, dW8) == t8) { if (j->n8 < LMAX) j->v8[j->n8] = x; j->n8++; }
            if (ds1(x, dW9) == d18) { if (j->n16 < LMAX) j->g16[j->n16] = x; j->n16++; }
        }
    } else if (pass == 2) {
        for (u64 xx = lo; xx < hi; xx++) {
            u32 a = ds0((u32)xx, dW5);
            if ((atomic_load_explicit(&B[a >> 6], memory_order_relaxed) >> (a & 63)) & 1) {
                u32 i = cslot(a);
                for (;;) {
                    if (j->cnt5[i] == 0) {
                        if (j->nseen >= CMAX) { j->overflow = 1; break; }
                        j->seen[j->nseen++] = a; j->cnt5[i] = ((u64)j->nseen << 40) | 1; break;
                    }
                    if (j->seen[(j->cnt5[i] >> 40) - 1] == a) { j->cnt5[i]++; break; }
                    i = (i + 1) & (CS - 1);
                }
            }
        }
    } else {
        for (u64 xx = lo; xx < hi; xx++) {
            u32 a = -ds1((u32)xx, d18);
            int s = cfind(a);
            if (s) j->cnt18[s - 1]++;
        }
    }
    return NULL;
}

static void run(job_t *J) {
    pthread_t th[NT];
    for (int t = 0; t < NT; t++) pthread_create(&th[t], NULL, work, &J[t]);
    for (int t = 0; t < NT; t++) pthread_join(th[t], NULL);
}

int main(int argc, char **argv) {
    if (argc != 8) { fprintf(stderr, "usage\n"); return 2; }
    dW5 = hexarg(argv[1]); dW6 = hexarg(argv[2]); dW7 = hexarg(argv[3]); dW8 = hexarg(argv[4]);
    dW9 = hexarg(argv[5]); d18 = hexarg(argv[6]);
    if ((u32)(d18 + dW9) != 0) { fprintf(stderr, "S: d18 + dW9 != 0\n"); return 1; }
    job_t *J = calloc(NT, sizeof(job_t));
    for (int t = 0; t < NT; t++) {
        J[t].id = t; J[t].v7 = malloc(4u * LMAX); J[t].v8 = malloc(4u * LMAX); J[t].g16 = malloc(4u * LMAX);
        J[t].seen = malloc(4u * CMAX); J[t].cnt5 = calloc(CS, 8); J[t].cnt18 = calloc(CS, 8);
    }
    pass = 1; run(J);
#if 0
    static u64 h5[CS], h18[CS];
    for (int t = 0; t < NT; t++) {
        if (J[t].overflow) { fprintf(stderr, "S: class overflow\n"); return 1; }
        for (u32 i = 0; i < CS; i++) if (J[t].cnt5[i]) {
            u32 a = J[t].seen[(J[t].cnt5[i] >> 40) - 1];
            u64 n = J[t].cnt5[i] & ((1ULL << 40) - 1);
            int s = cfind(a);
            if (!s) {
                if (ncl >= CMAX) { fprintf(stderr, "S: too many classes\n"); return 1; }
                u32 k = cslot(a);
                while (cuse[k]) k = (k + 1) & (CS - 1);
                cuse[k] = 1; ckey[k] = a; clist[ncl++] = a; s = (int)k + 1;
            }
            h5[s - 1] += n;
        }
    }
    pass = 3; run(J);
    for (int t = 0; t < NT; t++) for (u32 i = 0; i < CS; i++) h18[i] += J[t].cnt18[i];
#endif
    u64 n6 = 0, n9 = 0, n7 = 0, n8 = 0, n16 = 0;
    for (int t = 0; t < NT; t++) {
        n6 += J[t].n6; n9 += J[t].n9; n7 += J[t].n7; n8 += J[t].n8; n16 += J[t].n16;
        if (J[t].n7 > LMAX || J[t].n8 > LMAX || J[t].n16 > LMAX) { fprintf(stderr, "S: list overflow\n"); return 1; }
    }
    FILE *f = fopen(argv[7], "w");
    fprintf(f, "d %08x %08x %08x %08x %08x %08x\n", dW5, dW6, dW7, dW8, dW9, d18);
    fprintf(f, "n6 %llu\nn9 %llu\n", (unsigned long long)n6, (unsigned long long)n9);
    fprintf(f, "V7 %llu\n", (unsigned long long)n7);
    for (int t = 0; t < NT; t++) for (u32 i = 0; i < J[t].n7; i++) fprintf(f, "%08x\n", J[t].v7[i]);
    fprintf(f, "V8 %llu\n", (unsigned long long)n8);
    for (int t = 0; t < NT; t++) for (u32 i = 0; i < J[t].n8; i++) fprintf(f, "%08x\n", J[t].v8[i]);
    fprintf(f, "G16 %llu\n", (unsigned long long)n16);
    for (int t = 0; t < NT; t++) for (u32 i = 0; i < J[t].n16; i++) fprintf(f, "%08x\n", J[t].g16[i]);
    fclose(f);
    fprintf(stderr, "S: |V6| %llu |V7| %llu |V8| %llu |V9| %llu |G16| %llu\n", (unsigned long long)n6,
            (unsigned long long)n7, (unsigned long long)n8, (unsigned long long)n9, (unsigned long long)n16);
    return 0;
}
```

### ls2.c (SHA-256 af212da0b3a170a1)

```
/* STUDY-3 (economics), local search with USCMig's move set (package f94a3f75, Section 6), development measurement only.
   The SP is parametrised by its twelve state words F = (A5..A8, E5..E12) of copy P; A1..A4 are DERIVED from F
   (steps 8,7,6,5 inverted). This differs from work/sha256-r31/src/ls.c, which flipped A1..A4/E3..E8 directly and so
   perturbed A5..A8 and the whole tail at once.
   Usage: ls2 CHAR.txt SETS.txt SP14.txt NEXP MODE JCOMP OUT.txt
     SP14: A1 A2 A3 A4 E3 E4 E5 .. E12 (hex, copy P);  MODE: S = signed rows A5..A12/E5..E12 enforced (tab.c-compatible),
     X = exact conditions only (modular dE5..dE8 of the base, (P3), the W9 condition, dA10 = -d18, dA11 = dA12 = 0,
     dE13 = dA13 = 0, >= 1 tuple);  JCOMP: completions per kept SP (BFS over 1-/2-bit flips of E9..E12, <= 200 nodes,
     distinct W11; 0 = skip).
   Node expansion (USCMig): every 1-/2-bit flip inside one of the first eight words, then one bit in each of two
   different first-eight words; skip seen nodes (first eight words); prefilter (P3) and dA9 = dA9(base); repair: the
   candidate's E9..E12 as inherited, else every 1-/2-bit flip inside one of E9..E12, else one bit in each of two of
   them; keep if >= 1 tuple. Breadth first, NEXP expansions.
   Output: per SP "A1..A4 E3..E12 tuples completions" (E3,E4 = first tuple). Counters on stderr. */
#include "r31.h"

static u32 dw[16], d18;
static u32 um[2][13], nm[2][13];
static u32 *V7, *V8; static u64 n7, n8;
static u32 h7[1024]; static unsigned char u7[1024];
static u32 *h8; static unsigned char *u8_; static u32 h8m;
static int MODE_S;
static u32 dEb[13], dA9b;
static u64 c_cand, c_head, c_tail, c_rep, c_tup, c_kept, c_compev;

static int sgn_ok(int ae, int t, u32 x, u32 xp) {
    if (um[ae][t] == 0xFFFFFFFFu && nm[ae][t] == 0xFFFFFFFFu) return 1;
    u32 d = x ^ xp;
    if (d != (um[ae][t] | nm[ae][t])) return 0;
    if ((x & um[ae][t]) != 0 || (xp & um[ae][t]) != um[ae][t]) return 0;
    if ((x & nm[ae][t]) != nm[ae][t] || (xp & nm[ae][t]) != 0) return 0;
    return 1;
}
static int in7(u32 x) { u32 i = (x ^ (x >> 11) ^ (x >> 21)) & 1023; while (u7[i]) { if (h7[i] == x) return 1; i = (i + 1) & 1023; } return 0; }
static int in8(u32 x) { u32 i = (x ^ (x >> 13) ^ (x >> 23)) & h8m; while (u8_[i]) { if (h8[i] == x) return 1; i = (i + 1) & h8m; } return 0; }
static u32 *readlist(FILE *f, const char *tag, u64 *n) {
    char buf[64]; unsigned long long m;
    if (fscanf(f, "%63s %llu", buf, &m) != 2 || strcmp(buf, tag)) { fprintf(stderr, "L2: bad sets file at %s\n", tag); exit(1); }
    u32 *v = malloc(4 * (m + 1));
    for (u64 i = 0; i < m; i++) { unsigned x; if (fscanf(f, "%x", &x) != 1) exit(1); v[i] = x; }
    *n = m; return v;
}
typedef struct { u32 A[13], E[13], Ap[13], Ep[13], W[16]; } st_t;

/* F -> A1..A4, both copies of steps 5..8; returns 1 if the head conditions hold */
static int head(st_t *s) {
    u32 *A = s->A, *E = s->E, *Ap = s->Ap, *Ep = s->Ep;
    A[4] = E[8] - A[8] + BS0(A[7]) + MAJ(A[7], A[6], A[5]);
    A[3] = E[7] - A[7] + BS0(A[6]) + MAJ(A[6], A[5], A[4]);
    A[2] = E[6] - A[6] + BS0(A[5]) + MAJ(A[5], A[4], A[3]);
    A[1] = E[5] - A[5] + BS0(A[4]) + MAJ(A[4], A[3], A[2]);
    for (int t = 1; t <= 4; t++) Ap[t] = A[t];
    for (int t = 5; t <= 8; t++) Ep[t] = E[t] + dEb[t];
    if ((u32)(Ep[8] - E[8]) != (u32)((BS1(Ep[7]) - BS1(E[7])) + (IFF(Ep[7], Ep[6], Ep[5]) - IFF(E[7], E[6], E[5])) + dw[8])) return 0;
    for (int t = 5; t <= 8; t++) Ap[t] = Ep[t] - Ap[t - 4] + BS0(Ap[t - 1]) + MAJ(Ap[t - 1], Ap[t - 2], Ap[t - 3]);
    if (MODE_S) for (int t = 5; t <= 8; t++) if (!sgn_ok(0, t, A[t], Ap[t]) || !sgn_ok(1, t, E[t], Ep[t])) return 0;
    u32 dE9 = (Ap[5] - A[5]) + (Ep[5] - E[5]) + (BS1(Ep[8]) - BS1(E[8])) + (IFF(Ep[8], Ep[7], Ep[6]) - IFF(E[8], E[7], E[6])) + dw[9];
    u32 dA9 = dE9 - (Ap[5] - A[5]) + (BS0(Ap[8]) - BS0(A[8])) + (MAJ(Ap[8], Ap[7], Ap[6]) - MAJ(A[8], A[7], A[6]));
    return dA9 == dA9b;
}
static int tail_ok(st_t *s) {
    u32 *A = s->A, *E = s->E, *Ap = s->Ap, *Ep = s->Ep, *W = s->W;
    c_tail++;
    for (int t = 9; t <= 12; t++) {
        A[t] = E[t] - A[t - 4] + BS0(A[t - 1]) + MAJ(A[t - 1], A[t - 2], A[t - 3]);
        W[t] = E[t] - A[t - 4] - E[t - 4] - BS1(E[t - 1]) - IFF(E[t - 1], E[t - 2], E[t - 3]) - KK[t];
        Ep[t] = Ap[t - 4] + Ep[t - 4] + BS1(Ep[t - 1]) + IFF(Ep[t - 1], Ep[t - 2], Ep[t - 3]) + KK[t] + W[t] + (t == 9 ? dw[9] : 0);
        Ap[t] = Ep[t] - Ap[t - 4] + BS0(Ap[t - 1]) + MAJ(Ap[t - 1], Ap[t - 2], Ap[t - 3]);
        if (MODE_S && (!sgn_ok(0, t, A[t], Ap[t]) || !sgn_ok(1, t, E[t], Ep[t]))) return 0;
    }
    return ds0(W[9], dw[9]) == (u32)-dw[8] && (u32)(Ap[10] - A[10]) == (u32)-d18 && Ap[11] == A[11] && Ap[12] == A[12] &&
        (u32)(A[9] + E[9] + BS1(E[12]) + IFF(E[12], E[11], E[10])) == (u32)(Ap[9] + Ep[9] + BS1(Ep[12]) + IFF(Ep[12], Ep[11], Ep[10])) &&
        (u32)(MAJ(A[12], A[11], A[10]) - A[9]) == (u32)(MAJ(Ap[12], Ap[11], Ap[10]) - Ap[9]);
}
/* USCMig repair order */
static int repair(st_t *s) {
    if (tail_ok(s)) return 1;
    u32 base[4] = {s->E[9], s->E[10], s->E[11], s->E[12]};
    for (int w = 0; w < 4; w++) for (int b1 = 0; b1 < 32; b1++) for (int b2 = b1; b2 < 32; b2++) {
        for (int k = 0; k < 4; k++) s->E[9 + k] = base[k];
        s->E[9 + w] ^= (1u << b1) | (b2 != b1 ? 1u << b2 : 0);
        if (tail_ok(s)) return 1;
    }
    for (int w1 = 0; w1 < 4; w1++) for (int w2 = w1 + 1; w2 < 4; w2++) for (int b1 = 0; b1 < 32; b1++) for (int b2 = 0; b2 < 32; b2++) {
        for (int k = 0; k < 4; k++) s->E[9 + k] = base[k];
        s->E[9 + w1] ^= 1u << b1; s->E[9 + w2] ^= 1u << b2;
        if (tail_ok(s)) return 1;
    }
    for (int k = 0; k < 4; k++) s->E[9 + k] = base[k];
    return 0;
}
static u32 first_e3, first_e4;
static u64 tuples(const st_t *s) {
    const u32 *A = s->A, *E = s->E, *Ep = s->Ep;
    c_tup++;
    u32 c8 = E[8] - A[4] - BS1(E[7]) - IFF(E[7], E[6], E[5]) - KK[8];
    u32 R7 = (Ep[7] - E[7]) - (BS1(Ep[6]) - BS1(E[6])) - dw[7];
    u32 R6 = (Ep[6] - E[6]) - (BS1(Ep[5]) - BS1(E[5])) - dw[6];
    u64 nt = 0;
    for (u64 i = 0; i < n8; i++) {
        u32 e4 = c8 - V8[i];
        if ((u32)(IFF(Ep[6], Ep[5], e4) - IFF(E[6], E[5], e4)) != R7) continue;
        u32 c7 = E[7] - A[3] - BS1(E[6]) - IFF(E[6], E[5], e4) - KK[7];
        for (u64 k = 0; k < n7; k++) {
            u32 e3 = c7 - V7[k];
            if ((u32)(IFF(Ep[5], e4, e3) - IFF(E[5], e4, e3)) == R6) { if (!nt) { first_e3 = e3; first_e4 = e4; } nt++; }
        }
    }
    return nt;
}
/* completions: BFS over 1-/2-bit flips of E9..E12 (all 128-bit pairs), <= 200 nodes, distinct W11, cap J */
static int completions(const st_t *s0, int J) {
    if (J <= 0) return 0;
    enum { QN = 4096, HS = 1 << 16 };
    static u32 Q[QN][4], hs[HS][4], ws[HS]; static unsigned char hu[HS], wu[HS];
    memset(hu, 0, sizeof hu); memset(wu, 0, sizeof wu);
    int qh = 0, qt = 0, nc = 0, nodes = 0;
    st_t s = *s0;
    #define HN(c) (((c)[0] ^ ((c)[1] >> 7) ^ ((c)[1] << 11) ^ ((c)[2] >> 3) ^ ((c)[2] << 19) ^ ((c)[3] >> 13) ^ ((c)[3] << 5)) & (HS - 1))
    u32 c0[4] = {s.E[9], s.E[10], s.E[11], s.E[12]};
    { u32 h = HN(c0); hu[h] = 1; memcpy(hs[h], c0, 16); }
    tail_ok(&s);
    { u32 x = s.W[11], h = (x ^ (x >> 16) ^ (x << 5)) & (HS - 1); wu[h] = 1; ws[h] = x; }
    nc = 1; memcpy(Q[qt++], c0, 16);
    while (qh < qt && nc < J && nodes < 200) {
        u32 base[4]; memcpy(base, Q[qh++], 16); nodes++;
        for (int b1 = 0; b1 < 128 && nc < J; b1++) for (int b2 = b1; b2 < 128 && nc < J; b2++) {
            u32 c[4]; memcpy(c, base, 16);
            c[b1 >> 5] ^= 1u << (b1 & 31);
            if (b2 != b1) c[b2 >> 5] ^= 1u << (b2 & 31);
            st_t t = *s0; t.E[9] = c[0]; t.E[10] = c[1]; t.E[11] = c[2]; t.E[12] = c[3];
            c_compev++;
            if (!tail_ok(&t)) continue;
            u32 h = HN(c); int isnew = 1;
            while (hu[h]) { if (!memcmp(hs[h], c, 16)) { isnew = 0; break; } h = (h + 1) & (HS - 1); }
            if (!isnew) continue;
            hu[h] = 1; memcpy(hs[h], c, 16);
            if (qt < QN) memcpy(Q[qt++], c, 16);
            u32 x = t.W[11], g = (x ^ (x >> 16) ^ (x << 5)) & (HS - 1); int wn = 1;
            while (wu[g]) { if (ws[g] == x) { wn = 0; break; } g = (g + 1) & (HS - 1); }
            if (wn) { wu[g] = 1; ws[g] = x; nc++; }
        }
    }
    return nc;
}

typedef struct { u32 F[12]; u32 a14[14]; u64 nt; int nc; } sp_t;
static sp_t *SP; static u32 nsp, capsp;
static u32 *hk; static u32 hkm;
static u32 keyh(const u32 *F) { u32 h = 0x9e3779b9u; for (int i = 0; i < 8; i++) { h ^= F[i]; h = ROR(h, 7) + (h << 3); } return h; }
static int seen(const u32 *F) { u32 i = keyh(F) & hkm; while (hk[i]) { if (!memcmp(SP[hk[i] - 1].F, F, 32)) return 1; i = (i + 1) & hkm; } return 0; }
static int add_sp(const st_t *s, u64 nt, int nc) {
    u32 F[12]; for (int t = 5; t <= 8; t++) F[t - 5] = s->A[t]; for (int t = 5; t <= 12; t++) F[t - 1] = s->E[t];
    u32 i = keyh(F) & hkm;
    while (hk[i]) { if (!memcmp(SP[hk[i] - 1].F, F, 32)) return 0; i = (i + 1) & hkm; }
    if (nsp >= capsp) return 0;
    memcpy(SP[nsp].F, F, 48);
    for (int t = 1; t <= 4; t++) SP[nsp].a14[t - 1] = s->A[t];
    SP[nsp].a14[4] = first_e3; SP[nsp].a14[5] = first_e4;
    for (int t = 5; t <= 12; t++) SP[nsp].a14[t + 1] = s->E[t];
    SP[nsp].nt = nt; SP[nsp].nc = nc; nsp++; hk[i] = nsp; c_kept++; return 1;
}
static void fromF(const u32 *F, st_t *s) { memset(s, 0, sizeof *s); for (int t = 5; t <= 8; t++) s->A[t] = F[t - 5]; for (int t = 5; t <= 12; t++) s->E[t] = F[t - 1]; }

int main(int argc, char **argv) {
    if (argc != 8) { fprintf(stderr, "usage\n"); return 2; }
    FILE *f = fopen(argv[1], "r"); unsigned v[6];
    if (fscanf(f, "%x %x %x %x %x %x", &v[0], &v[1], &v[2], &v[3], &v[4], &v[5]) != 6) return 1;
    for (int t = 0; t < 5; t++) dw[5 + t] = v[t];
    d18 = v[5];
    for (int i = 0; i < 16; i++) { char nmn[16]; unsigned a, b; if (fscanf(f, "%15s %x %x", nmn, &a, &b) != 3) return 1; int ae = nmn[0] == 'E', t = atoi(nmn + 1); um[ae][t] = a; nm[ae][t] = b; }
    fclose(f);
    f = fopen(argv[2], "r"); char buf[64]; unsigned long long n6, n9;
    if (fscanf(f, "%63s %x %x %x %x %x %x", buf, &v[0], &v[1], &v[2], &v[3], &v[4], &v[5]) != 7) return 1;
    if (fscanf(f, "%63s %llu %63s %llu", buf, &n6, buf, &n9) != 4) return 1;
    V7 = readlist(f, "V7", &n7); V8 = readlist(f, "V8", &n8); fclose(f);
    if (n7 > 512) { fprintf(stderr, "L2: |V7| > 512 unsupported\n"); return 1; }
    for (u64 k = 0; k < n7; k++) { u32 x = V7[k], i = (x ^ (x >> 11) ^ (x >> 21)) & 1023; while (u7[i]) i = (i + 1) & 1023; u7[i] = 1; h7[i] = x; }
    h8m = (1u << 18) - 1; h8 = calloc(h8m + 1, 4); u8_ = calloc(h8m + 1, 1);
    for (u64 k = 0; k < n8; k++) { u32 x = V8[k], i = (x ^ (x >> 13) ^ (x >> 23)) & h8m; while (u8_[i]) i = (i + 1) & h8m; u8_[i] = 1; h8[i] = x; }
    long NEXP = atol(argv[4]); MODE_S = argv[5][0] == 'S'; int J = atoi(argv[6]);
    capsp = 1u << 20; SP = calloc(capsp, sizeof(sp_t)); hkm = (1u << 22) - 1; hk = calloc(hkm + 1, 4);
    /* base SP: forward from A1..A4, E3..E12 */
    f = fopen(argv[3], "r"); unsigned s14[14];
    for (int i = 0; i < 14; i++) if (fscanf(f, "%x", &s14[i]) != 1) return 1;
    fclose(f);
    st_t b; memset(&b, 0, sizeof b);
    for (int t = 1; t <= 4; t++) b.A[t] = b.Ap[t] = s14[t - 1];
    for (int t = 3; t <= 12; t++) b.E[t] = s14[t + 1];
    for (int t = 5; t <= 8; t++) b.A[t] = b.E[t] - b.A[t - 4] + BS0(b.A[t - 1]) + MAJ(b.A[t - 1], b.A[t - 2], b.A[t - 3]);
    b.Ep[3] = b.E[3]; b.Ep[4] = b.E[4];
    b.Ep[5] = b.E[5] + dw[5];
    b.Ep[6] = b.E[6] + (BS1(b.Ep[5]) - BS1(b.E[5])) + (IFF(b.Ep[5], b.E[4], b.E[3]) - IFF(b.E[5], b.E[4], b.E[3])) + dw[6];
    b.Ep[7] = b.E[7] + (BS1(b.Ep[6]) - BS1(b.E[6])) + (IFF(b.Ep[6], b.Ep[5], b.E[4]) - IFF(b.E[6], b.E[5], b.E[4])) + dw[7];
    b.Ep[8] = b.E[8] + (BS1(b.Ep[7]) - BS1(b.E[7])) + (IFF(b.Ep[7], b.Ep[6], b.Ep[5]) - IFF(b.E[7], b.E[6], b.E[5])) + dw[8];
    for (int t = 5; t <= 8; t++) dEb[t] = b.Ep[t] - b.E[t];
    for (int t = 5; t <= 8; t++) b.Ap[t] = b.Ep[t] - b.Ap[t - 4] + BS0(b.Ap[t - 1]) + MAJ(b.Ap[t - 1], b.Ap[t - 2], b.Ap[t - 3]);
    u32 dE9 = (b.Ap[5] - b.A[5]) + (b.Ep[5] - b.E[5]) + (BS1(b.Ep[8]) - BS1(b.E[8])) + (IFF(b.Ep[8], b.Ep[7], b.Ep[6]) - IFF(b.E[8], b.E[7], b.E[6])) + dw[9];
    dA9b = dE9 - (b.Ap[5] - b.A[5]) + (BS0(b.Ap[8]) - BS0(b.A[8])) + (MAJ(b.Ap[8], b.Ap[7], b.Ap[6]) - MAJ(b.A[8], b.A[7], b.A[6]));
    u32 F0[12]; for (int t = 5; t <= 8; t++) F0[t - 5] = b.A[t]; for (int t = 5; t <= 12; t++) F0[t - 1] = b.E[t];
    st_t s; fromF(F0, &s);
    if (!head(&s) || !tail_ok(&s)) { fprintf(stderr, "L2: base SP invalid in mode %c\n", argv[5][0]); return 1; }
    for (int t = 1; t <= 4; t++) if (s.A[t] != b.A[t]) { fprintf(stderr, "L2: inversion mismatch\n"); return 1; }
    u64 nt0 = tuples(&s);
    add_sp(&s, nt0, completions(&s, J));
    fprintf(stderr, "L2: base tuples %llu completions %d dA9 %08x\n", (unsigned long long)nt0, SP[0].nc, dA9b);
    u32 qh = 0; long ex;
    for (ex = 0; ex < NEXP && qh < nsp; ex++) {
        u32 base[12]; memcpy(base, SP[qh].F, 48); qh++;
        for (int pass = 0; pass < 2; pass++)
        for (int w1 = 0; w1 < 8; w1++) for (int w2 = (pass ? w1 + 1 : w1); w2 < (pass ? 8 : w1 + 1); w2++)
        for (int b1 = 0; b1 < 32; b1++) for (int b2 = (pass ? 0 : b1); b2 < 32; b2++) {
            u32 F[12]; memcpy(F, base, 48);
            F[w1] ^= 1u << b1;
            if (pass || b2 != b1) F[w2] ^= 1u << b2;
            c_cand++;
            if (seen(F)) continue;
            st_t t; fromF(F, &t);
            if (!head(&t)) continue;
            c_head++;
            if (!repair(&t)) continue;
            c_rep++;
            u64 nt = tuples(&t);
            if (!nt) continue;
            add_sp(&t, nt, completions(&t, J));
        }
        if ((ex & 7) == 7) fprintf(stderr, "L2: exp %ld sps %u cand %llu head %llu rep %llu tup %llu tails %llu\n", ex + 1, nsp,
                                   (unsigned long long)c_cand, (unsigned long long)c_head, (unsigned long long)c_rep,
                                   (unsigned long long)c_tup, (unsigned long long)c_tail);
    }
    f = fopen(argv[7], "w"); u64 tot = 0, totc = 0;
    for (u32 i = 0; i < nsp; i++) {
        for (int k = 0; k < 14; k++) fprintf(f, "%08x ", SP[i].a14[k]);
        fprintf(f, "%llu %d\n", (unsigned long long)SP[i].nt, SP[i].nc); tot += SP[i].nt; totc += SP[i].nc;
    }
    fclose(f);
    fprintf(stderr, "L2: END expansions %ld sps %u tuples %llu completions %llu cand %llu head %llu rep %llu tupcalls %llu "
            "tails %llu compevals %llu\n", ex, nsp, (unsigned long long)tot, (unsigned long long)totc,
            (unsigned long long)c_cand, (unsigned long long)c_head, (unsigned long long)c_rep, (unsigned long long)c_tup,
            (unsigned long long)c_tail, (unsigned long long)c_compev);
    return 0;
}
```

### tabm.c (SHA-256 c5d12e3830e713cc)

```
/* v6 phase A (tabm): r31v6 phase T (tab.c) over every starting point (SP) of the local-search family, plus the family
   rate model and the online trial cap N, computed inside the algorithm.
   Usage: tabm CHAR.txt FAM.txt SETS.txt ADVDIR J T11 MCS SEED
     CHAR.txt: "dw5 dw6 dw7 dw8 dw9 d18" then 16 lines "name umask nmask" (A5..A12, E5..E12; signed rows)
     FAM.txt:  ls2 output, one SP per line: A1 A2 A3 A4 E3 .. E12 (14 hex words, copy P) then two counters (ignored)
     J: max completions per SP (distinct W11); T11: max BFS nodes expanded per SP; MCS: Monte-Carlo samples of the
     family rate model; SEED: 64-bit hex (design constant) of the rate-model sampler.
   v6 freeze 2: all parsing/printing by v6io.h and the tuple sort by an own merge sort (no libc formatting, no qsort).
   Per SP exactly as tab.c: check every exact and signed condition (abort if one fails), table of tuples (e3, e4) with
   key, completions by BFS over 1-/2-bit changes of E9..E12 (distinct W11, caps J and T11), advice file
   ADVDIR/NNNN.txt in tab.c's format. ADVDIR/advlist.txt lists them.
   Rate model (only for the cap N): q = T * p6 * 2^-32 * p20, T = total tuples, p6 = |V6| / 2^32,
   p20 = H / MCS where each sample draws an SP with probability proportional to its tuple count (index uniform in
   [0, T) by rejection sampling, no division), a uniform W5 and a
   uniform r = SS0(W3) + W2, and tests the step-20 condition for that SP's completions and every W16 in G16.
   N = ceil(2 / q), rounded up to a multiple of 7 (one SWAR batch = 7 trials). Written to ADVDIR/rate.txt. */
#include "r31.h"
#include "v6io.h"
#include <math.h>

static u32 dw[16], d18;
static u32 um[2][13], nm[2][13];
static int sgn_ok(int ae, int t, u32 x, u32 xp) {
    if (um[ae][t] == 0xFFFFFFFFu && nm[ae][t] == 0xFFFFFFFFu) return 1;
    u32 d = x ^ xp;
    if (d != (um[ae][t] | nm[ae][t])) return 0;
    if ((x & um[ae][t]) != 0 || (xp & um[ae][t]) != um[ae][t]) return 0;
    if ((x & nm[ae][t]) != nm[ae][t] || (xp & nm[ae][t]) != 0) return 0;
    return 1;
}
static u32 *readlist(ib_t *f, const char *tag, u64 *n) {
    char buf[64]; u64 m;
    if (!ib_tok(f, buf, 64) || strcmp(buf, tag) || !ib_u64(f, &m)) { fputs("A: bad sets file\n", stderr); exit(1); }
    u32 *v = malloc(4 * (m + 1));
    for (u64 i = 0; i < m; i++) { u32 x; if (!ib_hex(f, &x)) exit(1); v[i] = x; }
    *n = m; return v;
}
typedef struct { u32 key, e3, e4, pad_; } tup_t;   /* 16 bytes: indexing by shifts (no multiply) */
static int tless(const tup_t *x, const tup_t *y) {   /* (key, e4, e3) order of tab.c's qsort comparator */
    if (x->key != y->key) return x->key < y->key;
    if (x->e4 != y->e4) return x->e4 < y->e4;
    return x->e3 < y->e3;
}
static tup_t *TMPS;
static void msort(tup_t *a, u64 n) {   /* bottom-up merge sort (keys are distinct triples, so the order is that of qsort) */
    for (u64 w = 1; w < n; w += w) {
        for (u64 lo = 0; lo < n; lo += w + w) {
            u64 mid = lo + w < n ? lo + w : n, hi = lo + w + w < n ? lo + w + w : n, i = lo, j = mid, k = lo;
            while (i < mid && j < hi) TMPS[k++] = tless(&a[j], &a[i]) ? a[j++] : a[i++];
            while (i < mid) TMPS[k++] = a[i++];
            while (j < hi) TMPS[k++] = a[j++];
        }
        memcpy(a, TMPS, sizeof(tup_t) * n);
    }
}
#define STEPS9_12(A, E, Ap, Ep, W) do { \
    for (int t = 9; t <= 12; t++) { \
        A[t] = E[t] - A[t - 4] + BS0(A[t - 1]) + MAJ(A[t - 1], A[t - 2], A[t - 3]); \
        W[t] = E[t] - A[t - 4] - E[t - 4] - BS1(E[t - 1]) - IFF(E[t - 1], E[t - 2], E[t - 3]) - KK[t]; } \
    for (int t = 9; t <= 12; t++) { \
        Ep[t] = Ap[t - 4] + Ep[t - 4] + BS1(Ep[t - 1]) + IFF(Ep[t - 1], Ep[t - 2], Ep[t - 3]) + KK[t] + W[t] + (t == 9 ? dw[9] : 0); \
        Ap[t] = Ep[t] - Ap[t - 4] + BS0(Ap[t - 1]) + MAJ(Ap[t - 1], Ap[t - 2], Ap[t - 3]); } } while (0)
#define COMP_OK(A, E, Ap, Ep, W) ( ds0(W[9], dw[9]) == (u32)-dw[8] && (u32)(Ap[10] - A[10]) == (u32)-d18 && \
    Ap[11] == A[11] && Ap[12] == A[12] && \
    (u32)(A[9] + E[9] + BS1(E[12]) + IFF(E[12], E[11], E[10])) == (u32)(Ap[9] + Ep[9] + BS1(Ep[12]) + IFF(Ep[12], Ep[11], Ep[10])) && \
    (u32)(MAJ(A[12], A[11], A[10]) - A[9]) == (u32)(MAJ(Ap[12], Ap[11], Ap[10]) - Ap[9]) )

static u64 n7, n8, n16, n6;
static u32 *V7, *V8, *G16;
static tup_t *T;
/* BFS state (reused across SPs) */
static u32 *Q, *hs, *ws; static unsigned char *hu, *wu;
static const u32 qcap = 1u << 20, hsz = 1u << 22, wsz = 1u << 16;

/* one SP: returns tuples, fills W11 of its completions (nc), writes the advice file */
static u64 one_sp(const unsigned s[14], const char *path, int J, long T11, u32 *W11out, int *ncout) {
    u32 A[13], E[13], Ap[13], Ep[13], W[16];
    memset(A, 0, sizeof A); memset(E, 0, sizeof E); memset(Ap, 0, sizeof Ap); memset(Ep, 0, sizeof Ep);
    for (int t = 1; t <= 4; t++) A[t] = Ap[t] = s[t - 1];
    for (int t = 3; t <= 12; t++) E[t] = s[t + 1];
    Ep[3] = E[3]; Ep[4] = E[4];
    for (int t = 5; t <= 8; t++) A[t] = E[t] - A[t - 4] + BS0(A[t - 1]) + MAJ(A[t - 1], A[t - 2], A[t - 3]);
    Ep[5] = E[5] + dw[5];
    Ep[6] = E[6] + (BS1(Ep[5]) - BS1(E[5])) + (IFF(Ep[5], E[4], E[3]) - IFF(E[5], E[4], E[3])) + dw[6];
    Ep[7] = E[7] + (BS1(Ep[6]) - BS1(E[6])) + (IFF(Ep[6], Ep[5], E[4]) - IFF(E[6], E[5], E[4])) + dw[7];
    Ep[8] = E[8] + (BS1(Ep[7]) - BS1(E[7])) + (IFF(Ep[7], Ep[6], Ep[5]) - IFF(E[7], E[6], E[5])) + dw[8];
    for (int t = 5; t <= 8; t++) Ap[t] = Ep[t] - Ap[t - 4] + BS0(Ap[t - 1]) + MAJ(Ap[t - 1], Ap[t - 2], Ap[t - 3]);
    int bad = 0;
    for (int t = 5; t <= 8; t++) bad |= !sgn_ok(0, t, A[t], Ap[t]) || !sgn_ok(1, t, E[t], Ep[t]);
    STEPS9_12(A, E, Ap, Ep, W);
    int sigok = 1;
    for (int t = 9; t <= 12; t++) sigok &= sgn_ok(0, t, A[t], Ap[t]) && sgn_ok(1, t, E[t], Ep[t]);
    if (bad || !COMP_OK(A, E, Ap, Ep, W) || !sigok) { fprintf(stderr, "A: starting point %s fails (bad %d sig %d)\n", path, bad, sigok); exit(1); }

    /* table of tuples (tab.c) */
    u32 c8 = E[8] - A[4] - BS1(E[7]) - IFF(E[7], E[6], E[5]) - KK[8];
    u32 R7 = (Ep[7] - E[7]) - (BS1(Ep[6]) - BS1(E[6])) - dw[7];
    u32 R6 = (Ep[6] - E[6]) - (BS1(Ep[5]) - BS1(E[5])) - dw[6];
    u64 cap = 1u << 24, nt = 0;
    for (u64 i = 0; i < n8; i++) {
        u32 e4 = c8 - V8[i];
        if ((u32)(IFF(Ep[6], Ep[5], e4) - IFF(E[6], E[5], e4)) != R7) continue;
        u32 c7 = E[7] - A[3] - BS1(E[6]) - IFF(E[6], E[5], e4) - KK[7];
        u32 a0 = e4 - A[4] + BS0(A[3]) + MAJ(A[3], A[2], A[1]);
        u32 kb = BS0(A[2]) + MAJ(A[2], A[1], a0) - A[3];
        for (u64 k = 0; k < n7; k++) {
            u32 e3 = c7 - V7[k];
            if ((u32)(IFF(Ep[5], e4, e3) - IFF(E[5], e4, e3)) != R6) continue;
            if (nt >= cap) { fprintf(stderr, "A: tuple cap\n"); exit(1); }
            T[nt].key = e3 + kb; T[nt].e3 = e3; T[nt].e4 = e4; nt++;
        }
    }
    msort(T, nt);

    /* completions (tab.c BFS) */
    u32 C9[64], C10[64], C11[64], C12[64];
    if (J > 64) J = 64;
    memset(hu, 0, hsz); memset(wu, 0, wsz);
    u32 qh = 0, qt = 0; int nc = 0; long tries11 = 0;
    #define NODE_NEW(e9, e10, e11, e12) ({ u32 _h = ((e9) ^ ((e10) >> 7) ^ ((e10) << 11) ^ ((e11) >> 3) ^ ((e11) << 19) ^ ((e12) >> 13) ^ ((e12) << 5)) & (hsz - 1); int _n = 1; \
        while (hu[_h]) { u32 *_p = hs + 4 * _h; if (_p[0] == (e9) && _p[1] == (e10) && _p[2] == (e11) && _p[3] == (e12)) { _n = 0; break; } _h = (_h + 1) & (hsz - 1); } \
        if (_n) { hu[_h] = 1; u32 *_p = hs + 4 * _h; _p[0] = (e9); _p[1] = (e10); _p[2] = (e11); _p[3] = (e12); } _n; })
    #define W11_NEW(x) ({ u32 _h = ((x) ^ ((x) >> 16) ^ ((x) << 5)) & (wsz - 1); int _n = 1; \
        while (wu[_h]) { if (ws[_h] == (x)) { _n = 0; break; } _h = (_h + 1) & (wsz - 1); } if (_n) { wu[_h] = 1; ws[_h] = (x); } _n; })
    NODE_NEW(E[9], E[10], E[11], E[12]); W11_NEW(W[11]);
    C9[0] = E[9]; C10[0] = E[10]; C11[0] = E[11]; C12[0] = E[12]; W11out[0] = W[11]; nc = 1;
    Q[0] = E[9]; Q[1] = E[10]; Q[2] = E[11]; Q[3] = E[12]; qt = 1;
    while (qh < qt && nc < J && tries11 < T11) {
        u32 base[4]; memcpy(base, Q + 4 * qh, 16); qh++; tries11++;
        for (int b1 = 0; b1 < 128 && nc < J; b1++) for (int b2 = b1; b2 < 128 && nc < J; b2++) {
            u32 c[4]; memcpy(c, base, 16);
            c[b1 >> 5] ^= 1u << (b1 & 31);
            if (b2 != b1) c[b2 >> 5] ^= 1u << (b2 & 31);
            u32 a[13], e[13], ap[13], ep[13], w[16];
            memcpy(a, A, sizeof a); memcpy(e, E, sizeof e); memcpy(ap, Ap, sizeof ap); memcpy(ep, Ep, sizeof ep);
            e[9] = c[0]; e[10] = c[1]; e[11] = c[2]; e[12] = c[3];
            STEPS9_12(a, e, ap, ep, w);
            if (!COMP_OK(a, e, ap, ep, w)) continue;
            int ok = 1;
            for (int t = 9; t <= 12 && ok; t++) ok = sgn_ok(0, t, a[t], ap[t]) && sgn_ok(1, t, e[t], ep[t]);
            if (!ok || !NODE_NEW(c[0], c[1], c[2], c[3])) continue;
            if (qt < qcap) { memcpy(Q + 4 * qt, c, 16); qt++; }
            if (W11_NEW(w[11])) { C9[nc] = c[0]; C10[nc] = c[1]; C11[nc] = c[2]; C12[nc] = c[3]; W11out[nc] = w[11]; nc++; }
        }
    }
    *ncout = nc;

    static ob_t o; o.n = 0;
    ob_s(&o, "DW"); for (int t = 5; t <= 9; t++) { ob_c(&o, ' '); ob_hex8(&o, dw[t]); } ob_c(&o, ' '); ob_hex8(&o, d18); ob_c(&o, '\n');
    ob_s(&o, "SP");
    for (int t = 1; t <= 4; t++) { ob_c(&o, ' '); ob_hex8(&o, A[t]); }
    for (int t = 3; t <= 8; t++) { ob_c(&o, ' '); ob_hex8(&o, E[t]); }
    ob_s(&o, "\nG16 "); ob_u64(&o, n16); ob_c(&o, '\n');
    for (u64 x = 0; x < n16; x++) { ob_hex8(&o, G16[x]); ob_c(&o, '\n'); }
    ob_s(&o, "COMP "); ob_i(&o, nc); ob_c(&o, '\n');
    for (int j = 0; j < nc; j++) { ob_hex8(&o, C9[j]); ob_c(&o, ' '); ob_hex8(&o, C10[j]); ob_c(&o, ' '); ob_hex8(&o, C11[j]); ob_c(&o, ' '); ob_hex8(&o, C12[j]); ob_c(&o, '\n'); }
    ob_s(&o, "TUP "); ob_u64(&o, nt); ob_c(&o, '\n');
    for (u64 i = 0; i < nt; i++) { ob_hex8(&o, T[i].key); ob_c(&o, ' '); ob_hex8(&o, T[i].e3); ob_c(&o, ' '); ob_hex8(&o, T[i].e4); ob_c(&o, '\n'); }
    if (ob_write(&o, path)) { fputs("A: cannot write advice\n", stderr); exit(1); }
    return nt;
}

int main(int argc, char **argv) {
    if (argc != 9) { fprintf(stderr, "usage: tabm CHAR FAM SETS ADVDIR J T11 MCS SEED\n"); return 2; }
    char tk_[64];
    ib_t cf; { size_t l; char *b = slurp(argv[1], &l); if (!b) return 1; cf.p = b; cf.e = b + l; }
    u32 v[6];
    for (int t = 0; t < 6; t++) if (!ib_hex(&cf, &v[t])) return 1;
    for (int t = 0; t < 5; t++) dw[5 + t] = v[t];
    d18 = v[5];
    for (int i = 0; i < 16; i++) {
        u32 a, b;
        if (!ib_tok(&cf, tk_, 64) || !ib_hex(&cf, &a) || !ib_hex(&cf, &b)) return 1;
        int ae = tk_[0] == 'E', t = tk_[1] - '0'; if (tk_[2]) t = (t << 3) + (t << 1) + (tk_[2] - '0');
        um[ae][t] = a; nm[ae][t] = b;
    }
    ib_t sf; { size_t l; char *b = slurp(argv[3], &l); if (!b) return 1; sf.p = b; sf.e = b + l; }
    if (!ib_tok(&sf, tk_, 64)) return 1;
    for (int t = 0; t < 6; t++) if (!ib_hex(&sf, &v[t])) return 1;
    for (int t = 0; t < 5; t++) if (dw[5 + t] != v[t]) { fputs("A: sets/char mismatch\n", stderr); return 1; }
    u64 a9;
    if (!ib_tok(&sf, tk_, 64) || !ib_u64(&sf, &n6) || !ib_tok(&sf, tk_, 64) || !ib_u64(&sf, &a9)) return 1;
    V7 = readlist(&sf, "V7", &n7); V8 = readlist(&sf, "V8", &n8); G16 = readlist(&sf, "G16", &n16);
    int J, T11i, MCSi; u64 seed;
    { ib_t c = {argv[5], argv[5] + strlen(argv[5])}; ib_int(&c, &J); }
    { ib_t c = {argv[6], argv[6] + strlen(argv[6])}; ib_int(&c, &T11i); }
    { ib_t c = {argv[7], argv[7] + strlen(argv[7])}; ib_int(&c, &MCSi); }
    { ib_t c = {argv[8], argv[8] + strlen(argv[8])}; u32 hi, lo; char t8[9]; memcpy(t8, argv[8], 8); t8[8] = 0;
      ib_t c1 = {t8, t8 + 8}; ib_hex(&c1, &hi); ib_t c2 = {argv[8] + 8, argv[8] + strlen(argv[8])}; ib_hex(&c2, &lo); (void)c;
      seed = ((u64)hi << 32) | lo; }
    long T11 = T11i, MCS = MCSi;
    T = malloc(sizeof(tup_t) * (1u << 24)); TMPS = malloc(sizeof(tup_t) * (1u << 24));
    Q = malloc(16u * qcap); hs = calloc(hsz, 16); hu = calloc(hsz, 1); ws = calloc(wsz, 4); wu = calloc(wsz, 1);

    int capsp = 1 << 16, nsp = 0;
    u64 *nts = malloc(8 * capsp); u32 (*W11)[64] = malloc(sizeof(*W11) * capsp); int *ncs = malloc(sizeof(int) * capsp);
    ib_t fl; { size_t l; char *b = slurp(argv[2], &l); if (!b) return 1; fl.p = b; fl.e = b + l; }
    static ob_t lst; lst.n = 0;
    u32 s[14]; u64 x1;
    u64 tot = 0, totc = 0;
    for (;;) {
        int k = 0;
        for (; k < 14; k++) if (!ib_hex(&fl, &s[k])) break;
        if (k == 0) break;
        if (k != 14 || !ib_u64(&fl, &x1) || !ib_u64(&fl, &x1)) { fputs("A: bad family line\n", stderr); return 1; }
        if (nsp >= capsp) { fputs("A: too many SPs\n", stderr); return 1; }
        static ob_t pth; pth.n = 0; ob_s(&pth, argv[4]); ob_c(&pth, '/');
        { int x = nsp; char d4[4]; static const int P[4] = {1000, 100, 10, 1}; for (int q = 0; q < 4; q++) { char dd = '0'; while (x >= P[q]) { x -= P[q]; dd++; } d4[q] = dd; } ob_put(&pth, d4, 4); }
        ob_s(&pth, ".txt");
        unsigned su[14]; for (int q = 0; q < 14; q++) su[q] = s[q];
        nts[nsp] = one_sp(su, pth.p, J, T11, W11[nsp], &ncs[nsp]);
        ob_s(&lst, pth.p); ob_c(&lst, '\n');
        tot += nts[nsp]; totc += (u64)ncs[nsp]; nsp++;
    }
    { static ob_t lp; lp.n = 0; ob_s(&lp, argv[4]); ob_s(&lp, "/advlist.txt"); if (ob_write(&lst, lp.p)) return 1; }
    /* family rate model: SP drawn with probability nt/T (64-bit draw mod T; bias < T / 2^64) */
    u64 *cum = malloc(8 * (nsp + 1)); cum[0] = 0;
    for (int i = 0; i < nsp; i++) cum[i + 1] = cum[i] + nts[i];
    rng_t rm; rng_seed(&rm, seed, 2);
    u64 tmask = 1; while (tmask < tot) tmask += tmask; tmask -= 1;
    u64 hits = 0;
    for (long smp = 0; smp < MCS; smp++) {
        u64 u;   /* uniform in [0, tot) by rejection from the next power of two (no division) */
        do { u = rng_next(&rm) & tmask; } while (u >= tot);
        int lo = 0, hi = nsp;            /* first i with cum[i+1] > u */
        while (lo < hi) { int mid = (lo + hi) >> 1; if (cum[mid + 1] > u) hi = mid; else lo = mid + 1; }
        u32 w5 = (u32)rng_next(&rm), r = (u32)rng_next(&rm);
        u32 ta = -ds0(w5, dw[5]);
        int hit = 0;
        for (int j = 0; j < ncs[lo] && !hit; j++)
            for (u64 x = 0; x < n16; x++)
                if (ds1(SS1(G16[x]) + W11[lo][j] + r, d18) == ta) { hit = 1; break; }
        hits += (u64)hit;
    }
    if (!hits) { fprintf(stderr, "A: no step-20 hit in the rate model\n"); return 1; }
    /* q = tot * (n6/2^32) * 2^-32 * hits/MCS ; N = ceil(2/q) rounded up to a multiple of 7 */
    long double q = (long double)tot * ((long double)n6 / 4294967296.0L) / 4294967296.0L * ((long double)hits / (long double)MCS);
    long double Nf = 2.0L / q;
    u64 N = (u64)ceill(Nf);
    N = (N + 6) / 7 * 7;
    char lpath[4096]; snprintf(lpath, sizeof lpath, "%s/rate.txt", argv[4]);   /* one formatted line (a few hundred libc instructions) */
    FILE *f = fopen(lpath, "w");
    fprintf(f, "sps %d tuples %llu completions %llu mcs %ld hits %llu n6 %llu log2q %.6f NCAP %llu\n", nsp,
            (unsigned long long)tot, (unsigned long long)totc, MCS, (unsigned long long)hits, (unsigned long long)n6,
            (double)log2l(q), (unsigned long long)N);
    fclose(f);
    fprintf(stderr, "A: sps %d tuples %llu completions %llu hits %llu/%ld log2q %.4f NCAP %llu (2^%.4f)\n", nsp,
            (unsigned long long)tot, (unsigned long long)totc, (unsigned long long)hits, MCS, (double)log2l(q),
            (unsigned long long)N, (double)log2l((long double)N));
    return 0;
}
```

### v6on.c (SHA-256 9f68d85348108a8f)

```
/* v6 phase O + H: online first-block search on real chaining values, exact acceptance tests, capped completion.
   Derived from r31on2.c (r31v6). Changes for v6 (all fixed in DEVPLAN.md before any evidence run):
     - every trial's first block = 16 fresh pseudo-random words from AES-128-CTR under the run's key (no xorshift
       words, no counter word, no grouping): batch b (7 trials, the SWAR batch) uses 16 256-bit words
       R_i = AES_k(ctr 32b+2i) || AES_k(ctr 32b+2i+1) (little-endian limbs), and lane l's word i is bits
       [36l, 36l+32) of R_i -- exactly the words the counted SWAR batch (swar31.py) draws and masks;
     - full 2^32-bit key bitmap (only exact key matches leave the batch);
     - trial cap N = NCAP of phase A (ADVDIR/rate.txt), read here, never given;
     - global caps on every hit-path event (key matches, tuple tests, W6 passes, completion calls), computed here from
       N and the table; exceeding any cap aborts the run (= failure). The run is charged at the caps;
     - completion coins also from AES-128-CTR (domain 1 + thread).
   Usage: v6on ADVDIR AESKEY_HEX32 OUT.txt [SETUP_BUDGET]  (SETUP_BUDGET: retired-instruction budget of the setup, checked
          before the workers start; exceeded = abort = failure;  env V6_THREADS: worker threads, default 12;
          env V6_CAPMULT: multiply phase A's N (pre-registered stage 2 only); env V6_SETUP_ONLY: stop after loading/merging/bitmap/self-tests -- used to measure the setup instructions)
   Output: START line, at most one PAIR line (M0, M1, M1' as 16 hex words each), END line with all counters.
   Self-tests at start: AES-128 FIPS-197 C.1 vector; f31 == reference on 1000 blocks. */
#include "r31.h"
#include <pthread.h>
#include <libproc.h>
#include <sys/resource.h>
#include <unistd.h>
#include <stdatomic.h>

#include "v6aes.h"
#include "v6io.h"

/* ---------------- family (advice files of phase A) ---------------- */
static int NT = 12;
static u32 dw[16], d18;
typedef struct { u32 A[13], E[13], Ap[13], Ep[13]; int c0, nc; } spd_t;
static spd_t *SPD; static int nspd;
static u32 *G16; static int n16;
static int nc;
static u32 (*CA)[13], (*CE)[13], (*CAp)[13], (*CEp)[13], (*CW)[16];
static u32 *W11j;
static u64 ntup, nkeys; static u32 *tk, *te3, *te4, *tsp;
static u64 *bmp;                                 /* 2^32-bit bitmap on the key */
static u64 NCAP, NBATCH;
static u64 KCAP, TCAP, WCAP, ACAP = 64;
static atomic_ullong g_k, g_t, g_w, g_a;
static atomic_int stop_flag;
static u32 s1inv_basis[32];
static pthread_mutex_t mu = PTHREAD_MUTEX_INITIALIZER;
static FILE *out;

typedef struct {
    int id; u64 batches, trials, kmatch, tuptests, w6pass, r20tests, accepts, compl_calls, e13, w15, tails, found;
} th_t;

static u32 s1inv(u32 y) { u32 x = 0; for (int i = 0; i < 32; i++) if ((y >> i) & 1) x ^= s1inv_basis[i]; return x; }
static void build_s1inv(void) {
    u32 rows[32], inv[32];
    for (int r = 0; r < 32; r++) { rows[r] = 0; inv[r] = 1u << r; }
    for (int i = 0; i < 32; i++) { u32 col = SS1(1u << i); for (int r = 0; r < 32; r++) if ((col >> r) & 1) rows[r] |= 1u << i; }
    for (int c = 0; c < 32; c++) {
        int p = c; while (!((rows[p] >> c) & 1)) p++;
        u32 t = rows[c]; rows[c] = rows[p]; rows[p] = t; t = inv[c]; inv[c] = inv[p]; inv[p] = t;
        for (int r = 0; r < 32; r++) if (r != c && ((rows[r] >> c) & 1)) { rows[r] ^= rows[c]; inv[r] ^= inv[c]; }
    }
    for (int r = 0; r < 32; r++) { s1inv_basis[r] = 0; }
    for (int r = 0; r < 32; r++) for (int c = 0; c < 32; c++) if ((inv[c] >> r) & 1) s1inv_basis[r] |= 1u << c;
    rng_t r; rng_seed(&r, 99, 99);
    for (int k = 0; k < 1000; k++) { u32 x = (u32)rng_next(&r); if (s1inv(SS1(x)) != x) { fprintf(stderr, "O: s1inv\n"); exit(1); } }
}
static int over(atomic_ullong *c, u64 cap) {
    if (atomic_fetch_add(c, 1) + 1 > cap) { int z = 0; atomic_compare_exchange_strong(&stop_flag, &z, 3); return 1; }
    return 0;
}

/* capped completion of an accepted prefix (r31on2.c, coins from AES-CTR); returns 1 and fills m1 on success */
static int complete(th_t *T, coin_t *rg, const u32 cv[8], const u32 p[13], u32 a5class, int j, u32 m1[16]) {
    const u32 *Ac = CA[j], *Ec = CE[j], *Apc = CAp[j], *Epc = CEp[j];
    u32 t20 = -a5class;
    u32 c16 = p[9] + SS0(p[1]) + p[0];
    u32 c18 = p[11] + SS0(p[3]) + p[2];
    u32 kept[64]; int nk = 0;
    for (int x = 0; x < n16; x++) if (ds1(SS1(G16[x]) + c18, d18) == t20) kept[nk++] = s1inv(G16[x] - c16);
    if (!nk) return 0;
    int r0 = (int)(coin64(rg) & 63); while (r0 >= nk) r0 -= nk;
    u32 c13 = Ac[9] + Ec[9] + BS1(Ec[12]) + IFF(Ec[12], Ec[11], Ec[10]) + KK[13];
    u32 need14 = -d18;
    u64 w15t = 0; int tails = 0;
    for (int kk = 0; kk < nk; kk++) {
        int ki = r0 + kk; if (ki >= nk) ki -= nk;
        u32 w14 = kept[ki];
        for (u32 r = 0; r < (1u << 16); r++) {
            u32 e13 = (u32)coin64(rg); T->e13++;
            u32 e14 = Ac[10] + Ec[10] + BS1(e13) + IFF(e13, Ec[12], Ec[11]) + KK[14] + w14;
            u32 e14p = Apc[10] + Epc[10] + BS1(e13) + IFF(e13, Epc[12], Epc[11]) + KK[14] + w14;
            if ((u32)(e14p - e14) != need14) continue;
            u32 c15 = Ac[11] + Ec[11] + BS1(e14) + IFF(e14, e13, Ec[12]) + KK[15];
            u32 c15p = Apc[11] + Epc[11] + BS1(e14p) + IFF(e14p, e13, Epc[12]) + KK[15];
            if (c15 != c15p) continue;
            u32 w16 = SS1(w14) + c16;
            for (int q = 0; q < 1024; q++) {
                if (w15t >= (1u << 16) || tails >= 16) return 0;
                u32 w15 = (u32)coin64(rg); w15t++; T->w15++;
                u32 e15 = c15 + w15;
                u32 e16 = Ac[12] + Ec[12] + BS1(e15) + IFF(e15, e14, e13) + KK[16] + w16;
                u32 e16p = Apc[12] + Epc[12] + BS1(e15) + IFF(e15, e14p, e13) + KK[16] + w16 + dw[9];
                if (e16 != e16p || IFF(e16, e15, e14p) != IFF(e16, e15, e14)) continue;
                u32 m[16], mp[16], h0[8], h1[8];
                for (int t = 0; t < 13; t++) m[t] = p[t];
                m[13] = e13 - c13; m[14] = w14; m[15] = w15;
                for (int t = 0; t < 16; t++) mp[t] = m[t] + dw[t];
                tails++; T->tails++;
                f31(cv, m, h0); f31(cv, mp, h1);
                if (!memcmp(h0, h1, 32)) { memcpy(m1, m, 64); return 1; }
            }
        }
    }
    return 0;
}

static void test_trial(th_t *T, coin_t *rg, const u32 m0[16], const u32 cv[8]) {
    u32 am1 = cv[0], am2 = cv[1], am3 = cv[2], am4 = cv[3], em1 = cv[4], em2 = cv[5], em3 = cv[6], em4 = cv[7];
    u64 lo = 0, hi = ntup;
    while (lo < hi) { u64 mid = lo + ((hi - lo) >> 1); if (tk[mid] < am1) lo = mid + 1; else hi = mid; }
    if (lo >= ntup || tk[lo] != am1) { fprintf(stderr, "O: bitmap/table mismatch\n"); exit(1); }
    for (u64 i = lo; i < ntup && tk[i] == am1; i++) {
        T->tuptests++;
        if (over(&g_t, TCAP)) return;
        const spd_t *SS = &SPD[tsp[i]]; const u32 *A = SS->A, *E = SS->E;
        u32 e3 = te3[i], e4 = te4[i];
        u32 a0 = e4 - A[4] + BS0(A[3]) + MAJ(A[3], A[2], A[1]);
        if ((u32)(e3 - A[3] + BS0(A[2]) + MAJ(A[2], A[1], a0)) != am1) { fprintf(stderr, "O: key mismatch\n"); exit(1); }
        u32 e2 = A[2] + am2 - BS0(A[1]) - MAJ(A[1], a0, am1);
        u32 w6 = E[6] - A[2] - e2 - BS1(E[5]) - IFF(E[5], e4, e3) - KK[6];
        if (ds0(w6, dw[6]) != (u32)-dw[5]) continue;
        T->w6pass++;
        if (over(&g_w, WCAP)) return;
        u32 e1 = A[1] + am3 - BS0(a0) - MAJ(a0, am1, am2);
        u32 e0 = a0 + am4 - BS0(am1) - MAJ(am1, am2, am3);
        u32 p[13];
        p[6] = w6;
        p[5] = E[5] - A[1] - e1 - BS1(e4) - IFF(e4, e3, e2) - KK[5];
        p[4] = e4 - a0 - e0 - BS1(e3) - IFF(e3, e2, e1) - KK[4];
        p[3] = e3 - am1 - em1 - BS1(e2) - IFF(e2, e1, e0) - KK[3];
        p[2] = e2 - am2 - em2 - BS1(e1) - IFF(e1, e0, em1) - KK[2];
        p[1] = e1 - am3 - em3 - BS1(e0) - IFF(e0, em1, em2) - KK[1];
        p[0] = e0 - am4 - em4 - BS1(em1) - IFF(em1, em2, em3) - KK[0];
        p[7] = E[7] - A[3] - e3 - BS1(E[6]) - IFF(E[6], E[5], e4) - KK[7];
        p[8] = E[8] - A[4] - e4 - BS1(E[7]) - IFF(E[7], E[6], E[5]) - KK[8];
        u32 a5 = ds0(p[5], dw[5]), ta = -a5;
        u32 r = SS0(p[3]) + p[2];
        for (int j = SS->c0; j < SS->c0 + SS->nc; j++) {
            u32 c18 = W11j[j] + r;
            int hit = 0;
            for (int x = 0; x < n16; x++) { T->r20tests++; if (ds1(SS1(G16[x]) + c18, d18) == ta) { hit = 1; break; } }
            if (!hit) continue;
            T->accepts++;
            if (over(&g_a, ACAP)) return;
            for (int t = 9; t <= 12; t++) p[t] = CW[j][t];
            u32 m1[16];
            T->compl_calls++;
            if (complete(T, rg, cv, p, a5, j, m1)) {
                u32 c1[8], h0[8], h1[8], m1p[16];
                f31(IV0, m0, c1);
                for (int t = 0; t < 16; t++) m1p[t] = m1[t] + dw[t];
                f31(c1, m1, h0); f31(c1, m1p, h1);
                if (memcmp(h0, h1, 32) || !memcmp(m1, m1p, 64)) continue;
                pthread_mutex_lock(&mu);
                int z = 0;
                if (atomic_compare_exchange_strong(&stop_flag, &z, 1)) {
                    fprintf(out, "PAIR M0");
                    for (int t = 0; t < 16; t++) fprintf(out, " %08x", m0[t]);
                    fprintf(out, " M1"); for (int t = 0; t < 16; t++) fprintf(out, " %08x", m1[t]);
                    fprintf(out, " M1p"); for (int t = 0; t < 16; t++) fprintf(out, " %08x", m1p[t]);
                    fprintf(out, " j %d\n", j); fflush(out);
                    T->found++;
                }
                pthread_mutex_unlock(&mu);
                return;
            }
        }
    }
}

static void *worker(void *arg) {
    th_t *T = arg;
    coin_t rg = {1 + (u64)T->id, 0, {0, 0}, 0};
    u32 m[7][16];
    for (u64 b = (u64)T->id; b < NBATCH; b += (u64)NT) {
        if (atomic_load(&stop_flag)) break;
        gen_batch(b, m);
        T->batches++;
        for (int l = 0; l < 7; l++) {
            u32 cv[8];
            f31(IV0, m[l], cv);
            T->trials++;
            u32 k = cv[0];
            if ((bmp[k >> 6] >> (k & 63)) & 1) {
                T->kmatch++;
                if (over(&g_k, KCAP)) break;
                test_trial(T, &rg, m[l], cv);
            }
        }
    }
    return NULL;
}

int main(int argc, char **argv) {
    if (argc != 4 && argc != 5) { fprintf(stderr, "usage: v6on ADVDIR AESKEY OUT [SETUP_BUDGET]\n"); return 2; }
    if (getenv("V6_THREADS")) { const char *z = getenv("V6_THREADS"); ib_t c = {z, z + strlen(z)}; ib_int(&c, &NT); }
    if (NT < 1 || NT > 64) return 2;
    /* AES self-test (FIPS-197 C.1) */
    {
        uint8_t k[16], p[16], o[16], e[16] = {0x69,0xc4,0xe0,0xd8,0x6a,0x7b,0x04,0x30,0xd8,0xcd,0xb7,0x80,0x70,0xb4,0xc5,0x5a};
        for (int i = 0; i < 16; i++) { k[i] = (uint8_t)i; p[i] = (uint8_t)(0x11 * i); }
        aes_expand(k); vst1q_u8(o, aes_enc(vld1q_u8(p)));
        if (memcmp(o, e, 16)) { fprintf(stderr, "O: AES self-test fails\n"); return 1; }
    }
    uint8_t key[16];
    if (strlen(argv[2]) != 32) { fprintf(stderr, "O: key must be 32 hex digits\n"); return 2; }
    for (int i = 0; i < 16; i++) { int h1 = hexval(argv[2][2 * i]), h0 = hexval(argv[2][2 * i + 1]); if (h1 < 0 || h0 < 0) return 2; key[i] = (uint8_t)((h1 << 4) | h0); }
    aes_expand(key);

    char path[4096], tag[16]; u32 v[16];
    snprintf(path, sizeof path, "%s/rate.txt", argv[1]);
    { size_t l; char *rt = slurp(path, &l); if (!rt) { fputs("O: no rate.txt\n", stderr); return 1; }
      char *q = strstr(rt, "NCAP "); if (!q) return 1; ib_t c = {q + 5, rt + l}; if (!ib_u64(&c, &NCAP)) return 1; free(rt); }
    if (getenv("V6_CAPMULT")) { const char *z = getenv("V6_CAPMULT"); ib_t c = {z, z + strlen(z)}; u64 m = 0; ib_u64(&c, &m); u64 n0 = NCAP; NCAP = 0; for (u64 i = 0; i < m; i++) NCAP += n0; }   /* pre-registered stage 2 only (N = 4/q) */
    if (NCAP == 0 || NCAP % 7) { fprintf(stderr, "O: bad NCAP\n"); return 1; }
    NBATCH = NCAP / 7;

    snprintf(path, sizeof path, "%s/advlist.txt", argv[1]);
    ib_t lf; { size_t l; char *b = slurp(path, &l); if (!b) { fputs("O: no advlist\n", stderr); return 1; } lf.p = b; lf.e = b + l; }
    int cap_sp = 1 << 16; SPD = calloc(cap_sp, sizeof(spd_t));
    u64 capc = 1u << 18, capt = 1u << 26;
    CA = malloc(sizeof *CA * capc); CE = malloc(sizeof *CE * capc); CAp = malloc(sizeof *CAp * capc); CEp = malloc(sizeof *CEp * capc);
    CW = malloc(sizeof *CW * capc); W11j = malloc(4 * capc);
    typedef struct { u32 k, e3, e4, sp; } trec_t;
    trec_t *TR = malloc(sizeof(trec_t) * capt);
    nc = 0; ntup = 0; n16 = 0;
    int maxnc = 0;
    while (ib_tok(&lf, path, 4096) > 0) {
        if (nspd >= cap_sp) { fprintf(stderr, "O: too many SPs\n"); return 1; }
        size_t fl_; char *fb = slurp(path, &fl_);
        if (!fb) { fputs("O: cannot open advice\n", stderr); return 1; }
        ib_t F = {fb, fb + fl_}, *f = &F;
        if (!ib_tok(f, tag, 16)) return 1;
        for (int i = 0; i < 6; i++) if (!ib_hex(f, &v[i])) return 1;
        if (nspd == 0) { for (int t = 0; t < 5; t++) dw[5 + t] = v[t]; d18 = v[5]; }
        for (int t = 0; t < 5; t++) if (dw[5 + t] != v[t] || d18 != v[5]) { fprintf(stderr, "O: differences differ\n"); return 1; }
        spd_t *S = &SPD[nspd];
        u32 *A = S->A, *E = S->E, *Ap = S->Ap, *Ep = S->Ep;
        if (!ib_tok(f, tag, 16)) return 1;
        for (int i = 0; i < 10; i++) if (!ib_hex(f, &v[i])) return 1;
        for (int t = 1; t <= 4; t++) A[t] = Ap[t] = v[t - 1];
        for (int t = 3; t <= 8; t++) E[t] = v[t + 1];
        Ep[3] = E[3]; Ep[4] = E[4];
        for (int t = 5; t <= 8; t++) A[t] = E[t] - A[t - 4] + BS0(A[t - 1]) + MAJ(A[t - 1], A[t - 2], A[t - 3]);
        Ep[5] = E[5] + dw[5];
        Ep[6] = E[6] + (BS1(Ep[5]) - BS1(E[5])) + (IFF(Ep[5], E[4], E[3]) - IFF(E[5], E[4], E[3])) + dw[6];
        Ep[7] = E[7] + (BS1(Ep[6]) - BS1(E[6])) + (IFF(Ep[6], Ep[5], E[4]) - IFF(E[6], E[5], E[4])) + dw[7];
        Ep[8] = E[8] + (BS1(Ep[7]) - BS1(E[7])) + (IFF(Ep[7], Ep[6], Ep[5]) - IFF(E[7], E[6], E[5])) + dw[8];
        for (int t = 5; t <= 8; t++) Ap[t] = Ep[t] - Ap[t - 4] + BS0(Ap[t - 1]) + MAJ(Ap[t - 1], Ap[t - 2], Ap[t - 3]);
        u64 n;
        if (!ib_tok(f, tag, 16) || !ib_u64(f, &n)) return 1;
        if (nspd == 0) { n16 = (int)n; G16 = malloc(4 * (n16 + 1)); }
        if ((int)n != n16 || n16 > 64) { fprintf(stderr, "O: G16 differs or > 64\n"); return 1; }
        for (int i = 0; i < (int)n; i++) { if (!ib_hex(f, &v[0])) return 1; if (nspd == 0) G16[i] = v[0]; else if (G16[i] != v[0]) { fprintf(stderr, "O: G16 differs\n"); return 1; } }
        if (!ib_tok(f, tag, 16) || !ib_u64(f, &n)) return 1;
        S->c0 = nc; S->nc = (int)n; if ((int)n > maxnc) maxnc = (int)n;
        if (nc + n > capc) { fprintf(stderr, "O: too many completions\n"); return 1; }
        for (int j = nc; j < nc + (int)n; j++) {
            u32 e9, e10, e11, e12;
            if (!ib_hex(f, &e9) || !ib_hex(f, &e10) || !ib_hex(f, &e11) || !ib_hex(f, &e12)) return 1;
            u32 *a = CA[j], *e = CE[j], *ap = CAp[j], *ep = CEp[j], *w = CW[j];
            memcpy(a, A, 52); memcpy(e, E, 52); memcpy(ap, Ap, 52); memcpy(ep, Ep, 52);
            e[9] = e9; e[10] = e10; e[11] = e11; e[12] = e12;
            for (int t = 9; t <= 12; t++) {
                a[t] = e[t] - a[t - 4] + BS0(a[t - 1]) + MAJ(a[t - 1], a[t - 2], a[t - 3]);
                w[t] = e[t] - a[t - 4] - e[t - 4] - BS1(e[t - 1]) - IFF(e[t - 1], e[t - 2], e[t - 3]) - KK[t];
            }
            for (int t = 9; t <= 12; t++) {
                ep[t] = ap[t - 4] + ep[t - 4] + BS1(ep[t - 1]) + IFF(ep[t - 1], ep[t - 2], ep[t - 3]) + KK[t] + w[t] + (t == 9 ? dw[9] : 0);
                ap[t] = ep[t] - ap[t - 4] + BS0(ap[t - 1]) + MAJ(ap[t - 1], ap[t - 2], ap[t - 3]);
            }
            int ok = ds0(w[9], dw[9]) == (u32)-dw[8] && (u32)(ap[10] - a[10]) == (u32)-d18 && ap[11] == a[11] && ap[12] == a[12] &&
                (u32)(a[9] + e[9] + BS1(e[12]) + IFF(e[12], e[11], e[10])) == (u32)(ap[9] + ep[9] + BS1(ep[12]) + IFF(ep[12], ep[11], ep[10])) &&
                (u32)(MAJ(a[12], a[11], a[10]) - a[9]) == (u32)(MAJ(ap[12], ap[11], ap[10]) - ap[9]);
            if (!ok) { fprintf(stderr, "O: completion %d of SP %d fails\n", j, nspd); return 1; }
            W11j[j] = w[11];
        }
        nc += (int)n;
        if (!ib_tok(f, tag, 16) || !ib_u64(f, &n)) return 1;
        if (ntup + n > capt) { fprintf(stderr, "O: too many tuples\n"); return 1; }
        for (u64 i = 0; i < n; i++) {
            u32 k, a3, a4;
            if (!ib_hex(f, &k) || !ib_hex(f, &a3) || !ib_hex(f, &a4)) return 1;
            u32 a0 = a4 - A[4] + BS0(A[3]) + MAJ(A[3], A[2], A[1]);
            if ((u32)(a3 - A[3] + BS0(A[2]) + MAJ(A[2], A[1], a0)) != k) { fprintf(stderr, "O: stored key wrong\n"); return 1; }
            TR[ntup].k = k; TR[ntup].e3 = a3; TR[ntup].e4 = a4; TR[ntup].sp = (u32)nspd; ntup++;
        }
        free(fb);
        nspd++;
    }
    {   /* merge all tuples by key (counting sort on the top 16 bits, insertion sort per bucket); build the bitmap */
        u64 *cnt = calloc(65537, 8);
        for (u64 i = 0; i < ntup; i++) cnt[(TR[i].k >> 16) + 1]++;
        for (int b = 0; b < 65536; b++) cnt[b + 1] += cnt[b];
        trec_t *T2 = malloc(sizeof(trec_t) * (ntup + 1));
        u64 *pos = malloc(8 * 65536); memcpy(pos, cnt, 8 * 65536);
        for (u64 i = 0; i < ntup; i++) T2[pos[TR[i].k >> 16]++] = TR[i];
        for (int b = 0; b < 65536; b++)
            for (u64 i = cnt[b] + 1; i < cnt[b + 1]; i++) { trec_t x = T2[i]; u64 k = i; while (k > cnt[b] && T2[k - 1].k > x.k) { T2[k] = T2[k - 1]; k--; } T2[k] = x; }
        tk = malloc(4 * (ntup + 1)); te3 = malloc(4 * (ntup + 1)); te4 = malloc(4 * (ntup + 1)); tsp = malloc(4 * (ntup + 1));
        bmp = calloc(1ull << 26, 8);
        if (!bmp) { fprintf(stderr, "O: bitmap alloc\n"); return 1; }
        nkeys = 0;
        for (u64 i = 0; i < ntup; i++) {
            tk[i] = T2[i].k; te3[i] = T2[i].e3; te4[i] = T2[i].e4; tsp[i] = T2[i].sp;
            if (i && tk[i] < tk[i - 1]) { fprintf(stderr, "O: merge not sorted\n"); return 1; }
            if (!i || tk[i] != tk[i - 1]) nkeys++;
            u32 kb = tk[i]; bmp[kb >> 6] |= 1ULL << (kb & 63);
        }
        free(T2); free(TR); free(cnt); free(pos);
    }
    /* global caps (4x the uniform-CV expectation, plus 4096): key matches, tuple tests, W6 passes; 64 completion calls */
    KCAP = (u64)((long double)NCAP * (long double)nkeys / 4294967296.0L * 4.0L) + 4096;
    TCAP = (u64)((long double)NCAP * (long double)ntup / 4294967296.0L * 4.0L) + 4096;
    WCAP = (u64)((long double)NCAP * (long double)ntup / 4294967296.0L / 512.0L * 4.0L) + 4096;
    build_s1inv();
    for (int k = 0; k < 1000; k++) {   /* f31 self-test against an independent straight-line evaluation */
        rng_t r; rng_seed(&r, 77, k); u32 m[16], c1[8];
        for (int t = 0; t < 16; t++) m[t] = (u32)rng_next(&r);
        f31(IV0, m, c1);
        u32 w[31]; for (int t = 0; t < 16; t++) w[t] = m[t];
        for (int t = 16; t < 31; t++) w[t] = SS1(w[t - 2]) + w[t - 7] + SS0(w[t - 15]) + w[t - 16];
        u32 s[8]; memcpy(s, IV0, 32);
        for (int t = 0; t < 31; t++) { u32 t1 = s[7] + BS1(s[4]) + IFF(s[4], s[5], s[6]) + KK[t] + w[t], t2 = BS0(s[0]) + MAJ(s[0], s[1], s[2]);
            s[7] = s[6]; s[6] = s[5]; s[5] = s[4]; s[4] = s[3] + t1; s[3] = s[2]; s[2] = s[1]; s[1] = s[0]; s[0] = t1 + t2; }
        for (int t = 0; t < 8; t++) if ((u32)(IV0[t] + s[t]) != c1[t]) { fprintf(stderr, "O: f31 self-test fails\n"); return 1; }
    }
    {   /* setup budget, enforced in shipped code: retired instructions of this process so far (no worker thread yet) */
        struct rusage_info_v4 ri; u64 sb = 0; if (argc > 4) { ib_t c = {argv[4], argv[4] + strlen(argv[4])}; ib_u64(&c, &sb); }
        if (proc_pid_rusage(getpid(), RUSAGE_INFO_V4, (rusage_info_t *)&ri) != 0) { fprintf(stderr, "O: rusage\n"); return 1; }
        fprintf(stderr, "O: setup instructions %llu budget %llu\n", (unsigned long long)ri.ri_instructions, (unsigned long long)sb);
        if (sb && ri.ri_instructions > sb) { fprintf(stderr, "O: setup budget exceeded\n"); return 125; }
    }
    if (getenv("V6_SETUP_ONLY")) { fprintf(stderr, "O: setup only: sps %d tuples %llu keys %llu\n", nspd, (unsigned long long)ntup, (unsigned long long)nkeys); return 0; }
    out = fopen(argv[3], "a");
    fprintf(out, "START ncap %llu batches %llu sps %d tuples %llu keys %llu completions %d maxnc %d n16 %d KCAP %llu TCAP %llu WCAP %llu ACAP %llu threads %d\n",
            (unsigned long long)NCAP, (unsigned long long)NBATCH, nspd, (unsigned long long)ntup, (unsigned long long)nkeys, nc, maxnc, n16,
            (unsigned long long)KCAP, (unsigned long long)TCAP, (unsigned long long)WCAP, (unsigned long long)ACAP, NT);
    fflush(out);
    th_t *T = calloc(NT, sizeof(th_t)); pthread_t th[64];
    for (int t = 0; t < NT; t++) { T[t].id = t; pthread_create(&th[t], NULL, worker, &T[t]); }
    for (int t = 0; t < NT; t++) pthread_join(th[t], NULL);
    th_t S = {0};
    for (int t = 0; t < NT; t++) {
        S.batches += T[t].batches; S.trials += T[t].trials; S.kmatch += T[t].kmatch; S.tuptests += T[t].tuptests;
        S.w6pass += T[t].w6pass; S.r20tests += T[t].r20tests; S.accepts += T[t].accepts; S.compl_calls += T[t].compl_calls;
        S.e13 += T[t].e13; S.w15 += T[t].w15; S.tails += T[t].tails; S.found += T[t].found;
    }
    fprintf(out, "END batches %llu trials %llu kmatch %llu tuptests %llu w6pass %llu r20tests %llu accepts %llu compl_calls %llu "
            "e13 %llu w15 %llu tails %llu found %llu stop %d\n",
            (unsigned long long)S.batches, (unsigned long long)S.trials, (unsigned long long)S.kmatch, (unsigned long long)S.tuptests,
            (unsigned long long)S.w6pass, (unsigned long long)S.r20tests, (unsigned long long)S.accepts,
            (unsigned long long)S.compl_calls, (unsigned long long)S.e13, (unsigned long long)S.w15, (unsigned long long)S.tails,
            (unsigned long long)S.found, atomic_load(&stop_flag));
    fclose(out);
    return atomic_load(&stop_flag) == 1 ? 0 : 1;
}
```

### swar31.py (SHA-256 6d523b77ce8fd9ea; printed text SHA-256 0b496bfaa84047cd)

```
#!/usr/bin/env python3
"""v6 counted online batch (SWAR, 7 lanes x 36 bits) for sha256-r31, cost model collision-frontier-v5 (C = 2140).

This is the program whose primitive count is charged for phase O. It is swar_vm.py (STUDY-2; packing precedent
tekkac blake3 7x36, Th0rgal f310d44f) with four v6 changes, all of which only ADD counted primitives:
  1. the 16 random 256-bit words are drawn per batch (16 RAND) and masked to the lanes' low 32 bits (16 AND);
     lane l's message word i = bits [36l, 36l+32) of draw i -- the same words v6on/v6dump derive from AES-CTR;
  2. every round constant K_t is LOADED from memory (31 LOAD) instead of being an immediate;
  3. the IV is LOADED into the 8 state registers (8 LOAD) and IV word 0 again for the feed-forward (1 LOAD);
  4. the key probe is into the full 2^32-bit bitmap = 2^24 words of 256 bits: per lane
     addr = key >> 8 (shift), LOAD, bit = key & 255 (and), word >> bit (shift), & 1 (and), compare, branch = 7.
Early abort: only CV word 0 (the key A[-1]) is formed and extracted; a lane whose bitmap bit is set leaves the batch
to the scalar hit path (charged separately in H: one full compression call + capped hit work).
Every primitive executed is ticked; mask constants are resident registers (23), schedule ring 16, state 8, temps 8.

Usage:
  python3 swar31.py count                 -> exact ops per batch, units per trial (json)
  python3 swar31.py check KEYHEX B0 NB    -> reads `v6dump KEYHEX B0 NB` on stdin; checks SWAR keys == native keys
                                             for every lane, and (every 16th batch) all 8 SWAR CV words against the
                                             official verifier's _compress(sha256, IV, block, 31)
"""
import json
import struct
import sys

sys.path.insert(0, "V6B/src")
import swar_vm as sv  # noqa: E402  (counted SwarMachine primitives; hs-official reference)

C = 2140
L, W = 7, 36
MASK32 = sv.MASK32


def batch(m, draws, full=False):
    """one counted batch: draws = 16 raw 256-bit integers (the RAND outputs). Returns lane keys (and full CVs)."""
    ct = m.ct
    R = []
    for i in range(16):
        ct.tick("rand")                     # independent uniform 256-bit word
        R.append(m.maskM(draws[i]))         # 1 and
    w = list(R)
    st = []
    for j in range(8):
        m.LOAD(); st.append(m._pack_const(sv.IV[j]))   # IV word into a state register
    a, b, c, d, e, f, g, h = st

    def Wi(i):
        if i < 16:
            return w[i]
        s1 = m.sig1(w[(i - 2) % 16])
        s0 = m.sig0(w[(i - 15) % 16])
        t = m.ADD(m.ADD(s1, w[(i - 7) % 16]), m.ADD(s0, w[(i - 16) % 16]))
        t = m.maskM(t)
        w[i % 16] = t
        return t

    for i in range(31):
        wi = Wi(i)
        s1 = m.BS1(e)
        ch = m.CH(e, f, g)
        m.LOAD(); k = m._pack_const(sv.K[i])                      # round constant from memory
        t1 = m.ADD(m.ADD(m.ADD(h, s1), m.ADD(ch, wi)), k)
        s0 = m.BS0(a)
        mj = m.MAJ(a, b, c)
        t2 = m.ADD(s0, mj)
        newe = m.maskM(m.ADD(d, t1))
        newa = m.maskM(m.ADD(t1, t2))
        h, g, f, e, d, c, b, a = g, f, e, newe, c, b, a, newa
    m.LOAD(); iv0 = m._pack_const(sv.IV[0])
    out0 = m.maskM(m.ADD(iv0, a))
    keys = []
    for l in range(L):
        k = m.AND(m.SHR(out0, W * l), m.M)
        keys.append(k & MASK32)
        # bitmap probe (2^32 bits in 2^24 256-bit words); values not needed for the count
        m.SHR(k, 8); m.LOAD(); m.AND(k, 255); m.SHR(0, 0); m.AND(0, 1); m.CMP(); m.BR()
    for _ in range(6):                      # batch control: counter add, compare, branch, stop-flag load/cmp/branch
        ct.tick("branch")
    if not full:
        return keys, None
    # (verification only, not part of the counted early-abort batch): full CV from the same registers
    fullcv = [[0] * 8 for _ in range(L)]
    for j, x in enumerate((a, b, c, d, e, f, g, h)):
        o = (x + m._pack_const(sv.IV[j]))
        for l in range(L):
            fullcv[l][j] = ((o >> (W * l)) & MASK32)
    return keys, fullcv


def count():
    m = sv.SwarMachine(L, W)
    assert m.n_mask_regs + 16 + 8 + 8 <= 64
    keys, _ = batch(m, [0] * 16)
    ops = m.ct.total()
    return {"batch_ops": ops, "by_category": dict(m.ct.c), "per_trial_ops": ops / L, "units_per_trial": ops / L / C,
            "registers": m.n_mask_regs + 16 + 8 + 8}


def check(keyhex, b0, nb):
    src = sys.stdin.buffer
    nlanes = nkey = nfull = bad = 0
    ops0 = None
    for bi in range(nb):
        raw = src.read(512 + 224)
        if len(raw) != 736:
            raise SystemExit("short input at batch %d" % bi)
        limbs = struct.unpack("<64Q", raw[:512])
        cvs = struct.unpack("<56I", raw[512:])
        draws = [limbs[4 * i] | (limbs[4 * i + 1] << 64) | (limbs[4 * i + 2] << 128) | (limbs[4 * i + 3] << 192)
                 for i in range(16)]
        m = sv.SwarMachine(L, W)
        full = (bi % 16 == 0)
        keys, fcv = batch(m, draws, full)
        if ops0 is None:
            ops0 = m.ct.total()
        elif m.ct.total() != ops0:
            raise SystemExit("op count varies")
        for l in range(L):
            nlanes += 1
            if keys[l] != cvs[8 * l]:
                bad += 1
            else:
                nkey += 1
            if full:
                blk = b"".join(struct.pack(">I", (draws[i] >> (W * l)) & MASK32) for i in range(16))
                ref = sv.hf._compress("sha256", sv.IV, blk, 31)
                if list(ref) != fcv[l] or list(ref) != list(cvs[8 * l:8 * l + 8]):
                    bad += 1
                nfull += 1
    print(json.dumps({"key": keyhex, "b0": b0, "nb": nb, "lanes": nlanes, "keys_equal": nkey, "full_checked_vs_verifier": nfull,
                      "mismatches": bad, "batch_ops": ops0}))
    return bad


if __name__ == "__main__":
    if sys.argv[1] == "count":
        print(json.dumps(count(), indent=1))
    else:
        sys.exit(1 if check(sys.argv[2], int(sys.argv[3]), int(sys.argv[4])) else 0)
```

### swar_vm.py (SHA-256 f6a2ebcd444e37df; printed text SHA-256 3fe1a2004618d680)

```
#!/usr/bin/env python3
"""
Counted SWAR VM for one reduced-step SHA-256 collision *trial*.

Model (collision-frontier-v5, accepted precedent: tekkac blake3 7x36, Th0rgal r32 online):
  - 256-bit word RAM, 64 registers.
  - One call of the target (reduced-step) compression = 1 unit.
  - Every other 256-bit word primitive = 1/C units.
      C = reference_operation_cost: sha256-r31 -> 2140, sha256-r32 -> 2224.
  - Primitives (each executed instance counts 1): load, store,
    add/sub mod 2^256, and/or/xor/not, shift/rotation, compare, branch,
    independent uniform random 256-bit word.
  - Immediates and shift amounts are instruction fields (free operands).
  - Resident constants (masks) are loaded ONCE at program start-up and live in
    registers for the life of the run; their one-time load is amortized over
    billions of batches and is reported separately, NOT charged per batch.

SWAR packing: L lanes of W bits inside one 256-bit word. Default 7 lanes x 36
bits => 7*36 = 252 <= 256. Low 32 bits of each lane hold the lane's 32-bit word;
the top (W-32)=4 bits are guard bits that absorb carries of up to 2^(W-32)-1 = 15
lane-bounded 32-bit addends before any carry could cross the lane boundary.

This file is a measurement/study artifact. It is NOT an attack program and never
submits. It executes the reduced compression in SWAR, counts every primitive, and
checks bit-for-bit equality against the official verifier reference on >=10,000
lanes.
"""
from __future__ import annotations
import argparse, os, struct, sys, json
from dataclasses import dataclass, field

HS = "HSO"
sys.path.insert(0, os.path.abspath(HS))
from verifier import hash_functions as hf  # reference only; never executed as "the compression unit"

MASK32 = (1 << 32) - 1
IV = hf.IV["sha256"]
K = hf.SHA256_K

# round schedule of rotations/shifts (exact FIPS 180-4)
BS1_ROT = (6, 11, 25)
BS0_ROT = (2, 13, 22)
SIG0_ROT = (7, 18); SIG0_SHR = 3
SIG1_ROT = (17, 19); SIG1_SHR = 10


class Counter:
    """Primitive-op counter, bucketed by category."""
    __slots__ = ("c",)
    def __init__(self):
        self.c = {k: 0 for k in
                  ("rand", "load", "store", "add", "and", "or", "xor", "not",
                   "shift", "cmp", "branch")}
    def tick(self, k, n=1):
        self.c[k] += n
    def total(self):
        return sum(self.c.values())


class SwarMachine:
    """
    Operates on packed 256-bit words represented as Python ints.
    Every primitive method increments the counter. Lane width W, L lanes.
    Masks for rotations/shifts are RESIDENT registers (built once at init,
    not counted per use).
    """
    def __init__(self, lanes=7, width=36, counter=None):
        self.L = lanes
        self.W = width
        assert lanes * width <= 256
        assert width - 32 >= 1
        self.ct = counter or Counter()
        # resident packed mask: 32 one-bits in each lane's low 32 bits
        self.M = self._pack_const(MASK32)
        # resident rotate masks: for each rotate amount r used, m_lo[r], m_hi[r]
        self.rot_lo = {}
        self.rot_hi = {}
        for r in set(BS1_ROT + BS0_ROT + SIG0_ROT + SIG1_ROT):
            lo = (MASK32 >> r)              # bits that stay after >>r
            hi = (MASK32 << (32 - r)) & MASK32  # bits wrapped to top, kept in 32-bit lane
            self.rot_lo[r] = self._pack_const(lo)
            self.rot_hi[r] = self._pack_const(hi)
        # resident shr masks for sigma shifts
        self.shr_mask = {}
        for k in (SIG0_SHR, SIG1_SHR):
            self.shr_mask[k] = self._pack_const(MASK32 >> k)
        # count of resident mask registers (for the 64-register budget report)
        self.n_mask_regs = 1 + 2 * len(self.rot_lo) + len(self.shr_mask)

    # ---- packing helpers (not counted; test scaffolding) ----
    def _pack_const(self, v32):
        out = 0
        for l in range(self.L):
            out |= (v32 & MASK32) << (self.W * l)
        return out
    def pack(self, lane_words):
        assert len(lane_words) == self.L
        out = 0
        for l, v in enumerate(lane_words):
            out |= (v & MASK32) << (self.W * l)
        return out
    def unpack(self, packed):
        return [ (packed >> (self.W * l)) & MASK32 for l in range(self.L) ]
    def max_lane_val(self, packed):
        return max((packed >> (self.W * l)) & ((1 << self.W) - 1) for l in range(self.L))

    # ---- counted primitives ----
    def RAND(self):
        self.ct.tick("rand")
        # independent uniform 256-bit word
        return int.from_bytes(os.urandom(32), "little")
    def AND(self, a, b):
        self.ct.tick("and"); return a & b
    def OR(self, a, b):
        self.ct.tick("or"); return a | b
    def XOR(self, a, b):
        self.ct.tick("xor"); return a ^ b
    def ADD(self, a, b):
        self.ct.tick("add"); return (a + b) & ((1 << 256) - 1)
    def SHR(self, a, k):
        self.ct.tick("shift"); return a >> k
    def SHL(self, a, k):
        self.ct.tick("shift"); return (a << k) & ((1 << 256) - 1)
    def LOAD(self):
        self.ct.tick("load")
    def STORE(self):
        self.ct.tick("store")
    def CMP(self):
        self.ct.tick("cmp")
    def BR(self):
        self.ct.tick("branch")

    # ---- SWAR composite ops ----
    def maskM(self, x):
        return self.AND(x, self.M)
    def ROTR(self, x, r):
        # ((x>>r)&m_lo) | ((x<<(32-r))&m_hi)   : 2 shift + 2 and + 1 or = 5 ops
        lo = self.AND(self.SHR(x, r), self.rot_lo[r])
        hi = self.AND(self.SHL(x, 32 - r), self.rot_hi[r])
        return self.OR(lo, hi)
    def SHR32(self, x, k):
        # (x>>k)&mask : 1 shift + 1 and = 2 ops
        return self.AND(self.SHR(x, k), self.shr_mask[k])
    def sig0(self, x):
        # ROTR7 ^ ROTR18 ^ SHR3 : 5+5+2 + 2 xor = 14
        return self.XOR(self.XOR(self.ROTR(x, 7), self.ROTR(x, 18)), self.SHR32(x, 3))
    def sig1(self, x):
        # ROTR17 ^ ROTR19 ^ SHR10 : 5+5+2 + 2 xor = 14
        return self.XOR(self.XOR(self.ROTR(x, 17), self.ROTR(x, 19)), self.SHR32(x, 10))
    def BS1(self, x):
        # ROTR6 ^ ROTR11 ^ ROTR25 : 5+5+5 + 2 xor = 17
        return self.XOR(self.XOR(self.ROTR(x, 6), self.ROTR(x, 11)), self.ROTR(x, 25))
    def BS0(self, x):
        # ROTR2 ^ ROTR13 ^ ROTR22 : 17
        return self.XOR(self.XOR(self.ROTR(x, 2), self.ROTR(x, 13)), self.ROTR(x, 22))
    def CH(self, e, f, g):
        # (e&f) ^ ((e^M)&g) : 2 and + 2 xor = 4  (e<2^32 so e^M == ~e within lane)
        return self.XOR(self.AND(e, f), self.AND(self.XOR(e, self.M), g))
    def MAJ(self, a, b, c):
        # (a&b)^(a&c)^(b&c) : 3 and + 2 xor = 5
        return self.XOR(self.XOR(self.AND(a, b), self.AND(a, c)), self.AND(b, c))

    def Kconst(self, i):
        return self._pack_const(K[i])  # broadcast constant; an immediate operand, not counted


def swar_compress(mach: SwarMachine, blocks, rounds, early_abort=True):
    """
    Execute the reduced r-step SHA-256 compression on L lanes at once.
    blocks: list of L lists of 16 32-bit words (one fresh first block per lane).
    Returns the lane chaining values. If early_abort, only CV word 0 (the table
    key A[-1]) is formed and extracted; CV words 1..7 are left as full packed
    words (computed but not individually extracted) -- matching 'compute only the
    CV words the key needs'.
    Counting of RAND is done by the caller (randomness phase), this routine counts
    schedule + rounds + feed-forward + extraction.
    """
    m = mach
    L, W = m.L, m.W
    # schedule window W[0..15] resident; expansion overwrites a 16-slot ring.
    w = [m.pack([blocks[l][i] for l in range(L)]) for i in range(16)]
    iv = [m._pack_const(IV[j]) for j in range(8)]
    a, b, c, d, e, f, g, h = (iv[0], iv[1], iv[2], iv[3], iv[4], iv[5], iv[6], iv[7])

    def Wi(i):
        if i < 16:
            return w[i % 16]
        # expand into ring slot
        s1 = m.sig1(w[(i - 2) % 16])
        s0 = m.sig0(w[(i - 15) % 16])
        t = m.ADD(m.ADD(s1, w[(i - 7) % 16]), m.ADD(s0, w[(i - 16) % 16]))  # 3 add
        t = m.maskM(t)  # 1 and
        w[i % 16] = t
        return t

    for i in range(rounds):
        wi = Wi(i)
        s1 = m.BS1(e)
        ch = m.CH(e, f, g)
        t1 = m.ADD(m.ADD(m.ADD(h, s1), m.ADD(ch, wi)), m.Kconst(i))  # h+s1+ch+W+K : 4 add
        s0 = m.BS0(a)
        mj = m.MAJ(a, b, c)
        t2 = m.ADD(s0, mj)  # part of a_new
        newe = m.maskM(m.ADD(d, t1))         # 1 add + 1 and
        newa = m.maskM(m.ADD(t1, t2))        # 1 add + 1 and  (t2 already summed s0+mj=1 add)
        h, g, f, e, d, c, b, a = g, f, e, newe, c, b, a, newa

    # feed-forward + extract
    keys = []
    out0 = m.maskM(m.ADD(iv[0], a))  # 1 add + 1 and
    for l in range(L):
        k = m.AND(m.SHR(out0, W * l), m.M)  # extract lane key: 1 shift + 1 and
        keys.append((k >> 0) & MASK32)
    if not early_abort:
        outs = [out0]
        for j, st in enumerate((b, c, d, e, f, g, h), start=1):
            outs.append(m.maskM(m.ADD(iv[j], st)))
        full = []
        for l in range(L):
            lane = []
            for o in outs:
                lane.append(m.AND(m.SHR(o, W * l), m.M) & MASK32)
            full.append(lane)
        return keys, full
    return keys, None


def ref_cv(block_words, rounds):
    blk = b"".join(struct.pack(">I", x) for x in block_words)
    st = hf._compress("sha256", IV, blk, rounds)
    return st


def filter_probe_ops(mach: SwarMachine):
    """Per-lane membership probe into a 2^22-bit Bloom/filter on the key.
    addr = key>>6 (shift), load filter word, bit = key&63 (and), test = word>>bit
    (shift), isset = test&1 (and), compare, branch. = 7 ops/lane, honest upper
    bound (a direct table binary-search is only taken on the rare filter hit)."""
    L = mach.L
    for _ in range(L):
        mach.SHR(0, 6)   # address
        mach.LOAD()
        mach.AND(0, 63)  # bit index
        mach.SHR(0, 0)   # word>>bit
        mach.AND(0, 1)
        mach.CMP()
        mach.BR()


def run(lanes, width, rounds, trials_check, early_abort, control_reserve, verbose):
    C = {31: 2140, 32: 2224}[rounds]
    # ---------- correctness: verify >= trials_check lanes bit-exact ----------
    checked = 0
    mism = 0
    rng = __import__("random").Random(20261007)
    batch = lanes
    nb = (trials_check + batch - 1) // batch
    for _ in range(nb):
        blocks = [[rng.getrandbits(32) for _ in range(16)] for _ in range(lanes)]
        mach = SwarMachine(lanes, width)  # fresh (don't accumulate check-counts)
        keys, full = swar_compress(mach, blocks, rounds, early_abort=False)
        for l in range(lanes):
            ref = ref_cv(blocks[l], rounds)
            if full[l][0] != ref[0]:
                mism += 1
            for j in range(8):
                if full[l][j] != ref[j]:
                    mism += 1; break
            checked += 1
    assert mism == 0, f"SWAR mismatch vs verifier on {mism} lanes"

    # ---------- cost: one steady-state batch, dominant no-key-hit path ----------
    mach = SwarMachine(lanes, width)
    assert mach.n_mask_regs + 16 + 8 + 8 <= 64, \
        f"register budget exceeded: masks {mach.n_mask_regs} + 16 sched + 8 state + 8 temp"
    ct = mach.ct
    # randomness: 16 fresh 256-bit words give L fresh 512-bit blocks (disjoint lane slices)
    rand_blocks = []
    draws = []
    for _ in range(16):
        r = mach.RAND()
        r = mach.maskM(r)   # 1 and to zero guard bits
        draws.append(r)
    # reinterpret the 16 masked draws as L lane-blocks (bit-slicing, free)
    blocks = [[(draws[i] >> (width * l)) & MASK32 for i in range(16)] for l in range(lanes)]
    keys, _ = swar_compress(mach, blocks, rounds, early_abort=early_abort)
    filter_probe_ops(mach)
    # loop/control reserve per batch (outer batch counter incr+cmp+branch, flag check)
    for _ in range(control_reserve):
        ct.tick("branch")

    batch_ops = ct.total()
    per_trial_ops = batch_ops / lanes
    units_per_trial = per_trial_ops / C

    report = {
        "rounds": rounds, "C": C, "lanes": lanes, "width_bits": width,
        "guard_bits": width - 32,
        "register_budget": {
            "mask_regs": mach.n_mask_regs, "schedule_regs": 16,
            "state_regs": 8, "temp_regs_reserved": 8,
            "total": mach.n_mask_regs + 16 + 8 + 8, "limit": 64,
        },
        "ops_by_category_per_batch": dict(ct.c),
        "batch_ops": batch_ops,
        "per_trial_ops": round(per_trial_ops, 4),
        "units_per_trial": round(units_per_trial, 6),
        "early_abort": early_abort,
        "lanes_checked_bit_exact": checked,
        "control_reserve": control_reserve,
    }
    if verbose:
        print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=31, choices=(31, 32))
    ap.add_argument("--lanes", type=int, default=7)
    ap.add_argument("--width", type=int, default=36)
    ap.add_argument("--check", type=int, default=10000)
    ap.add_argument("--no-early-abort", action="store_true")
    ap.add_argument("--control-reserve", type=int, default=6)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    run(a.lanes, a.width, a.rounds, a.check, not a.no_early_abort,
        a.control_reserve, not a.quiet)
```

### ledger_v8.py (SHA-256 2a4e532b385c87d0)

```
"""v8 claim ledger (sha256-r31, collision-frontier-v5, C = 2140): realized executed work of the chain.
Every logged run (ledger_runs.tsv: phase, start, rc, retired instructions, wall, max RSS, command) is charged at its
retired instructions x the per-instruction price of its program class (PRICES); the online phase is charged by the
counted SWAR batch per executed batch plus per-event operation bounds for every hit-path event v6on counted; the
conversion checks before the freeze and the verifier checks are charged as DEV rows, each repetition at the measured
count of one identical re-run.
Usage: python3 ledger_v8.py RUNDIR [solver_price] [cap]   (cap: the online phase at its trial cap N and the hit path at
its global caps, instead of the realized counts)"""
import json, math, re, sys
C = 2140.0
PRICES = {"C0": 400.0, "DEVPY": 400.0, "C1": 16.0, "DEVC": 16.0, "S": 5.0, "M": 7.0, "C3": 17.0, "L": 5.0, "A": 5.0}
SWAR_BATCH = 2235                       # counted primitives per 7-lane batch (swar31.py; organizer experiment)
EV = {"kmatch": 512, "tuptest": 512, "w6pass": 1024, "r20test": 128, "e13": 160, "w15": 160}
OSETUP_PRICE = 5.0
DRIVER = (3e9, 25.0)                    # driver allowance: 3e9 instructions x 25 (bash, time, nice, small tools, lock/load polls, pre-freeze table extraction; estimate 1.6e9)
DRVSHA = 100764691                      # the driver's one shasum (Perl) run, measured, priced at 400 like Python
DEVSHA = (2 * 139423389 + 6 * 100764691) # the freeze hashing before the chain: 2 hash-list runs + 6 single-file shasum runs (measured re-runs), at 400
REPLAY = 6.36


def main(d, solver_price=None, cap=False):
    pr = dict(PRICES)
    if solver_price is not None:
        pr["M"] = float(solver_price)
    rows = []
    for line in open(d + "/ledger_runs.tsv"):
        ph, t0, rc, ins, real, rss, cmd = line.rstrip("\n").split("\t")
        if ph == "O":
            continue
        rows.append((ph, "%s instr x %g" % (ins, pr[ph]), int(ins) * pr[ph] / C, int(rss)))
    for line in open(d + "/dev_runs.tsv") if __import__("os").path.exists(d + "/dev_runs.tsv") else []:
        ph, ins, rss, what = line.rstrip("\n").split("\t")
        rows.append((ph, "%s instr x %g (%s)" % (ins, pr[ph], what), int(ins) * pr[ph] / C, int(rss)))
    on = []
    for line in open(d + "/ledger_runs.tsv"):
        f = line.rstrip("\n").split("\t")
        if f[0] == "O":
            on.append(f)
    for f in on:
        ki = re.search(r"on_(\S+)\.txt", f[6]) or re.search(r"on_(\S+)\.pairs", f[6])
        k = ki.group(1)
        st = "".join(open("%s/on_%s.%s" % (d, k, x)).read() for x in ("txt", "err", "pairs"))
        end = re.search(r"END (.*)", st).group(1)
        g = lambda key: int(re.search(r"\b" + key + r" (\d+)", end).group(1))
        nb, ntr = g("batches"), g("trials")
        setup = int(re.search(r"setup instructions (\d+)", st).group(1))
        s = re.search(r"START (.*)", st).group(1)
        n16 = int(re.search(r"n16 (\d+)", s).group(1)); ntup = int(re.search(r"tuples (\d+)", s).group(1))
        if cap:
            ncap = int(re.search(r"ncap (\d+)", s).group(1))
            nbc = int(re.search(r"batches (\d+)", s).group(1))
            gs = lambda key: int(re.search(r"\b" + key + r" (\d+)", s).group(1))
            swar_cap = nbc * SWAR_BATCH / C
            native = (int(f[3]) - setup) * OSETUP_PRICE / C
            if swar_cap >= native:
                rows.append(("O" if k == "1" else "O%s" % k, "max(cap N = %d trials = %d batches x %d ops; native run %d instr x %g) = the former (realized %d trials)" % (ncap, nbc, SWAR_BATCH, int(f[3]) - setup, OSETUP_PRICE, ntr), swar_cap, int(f[5])))
            else:
                rows.append(("O" if k == "1" else "O%s" % k, "max(cap N = %d trials = %d batches x %d ops = %.4g units; native run, %d instr x %g) = the latter (realized %d trials)" % (ncap, nbc, SWAR_BATCH, swar_cap, int(f[3]) - setup, OSETUP_PRICE, ntr), native, int(f[5])))
            comp_call = (n16 * (1 << 16) * EV["e13"] + (1 << 16) * EV["w15"] + n16 * 512) / C + 16 * 2 + 3
            hcap = (gs("KCAP") * (1 + EV["kmatch"] / C) + gs("TCAP") * EV["tuptest"] / C
                    + gs("WCAP") * (EV["w6pass"] + gs("maxnc") * n16 * EV["r20test"]) / C + gs("ACAP") * comp_call)
            rows.append(("HP" if k == "1" else "HP%s" % k, "hit path at its caps K %d, T %d, W %d, A %d" % (gs("KCAP"), gs("TCAP"), gs("WCAP"), gs("ACAP")), hcap, 0))
        else:
          rows.append(("O" if k == "1" else "O%s" % k, "%d batches x %d ops (%d trials)" % (nb, SWAR_BATCH, ntr), nb * SWAR_BATCH / C, int(f[5])))
        hp = (g("kmatch") * (1 + EV["kmatch"] / C) + g("tuptests") * EV["tuptest"] / C
              + g("w6pass") * (EV["w6pass"] + int(re.search(r"maxnc (\d+)", s).group(1)) * n16 * EV["r20test"]) / C + g("e13") * EV["e13"] / C + g("w15") * EV["w15"] / C
              + g("compl_calls") * (n16 * 512 / C + 35) + g("tails") * 6.0)
        if not cap: rows.append(("HP" if k == "1" else "HP%s" % k, "realized hit path: kmatch %d, tuples %d, w6 %d, calls %d, e13 %d, w15 %d, tails %d" % (
            g("kmatch"), g("tuptests"), g("w6pass"), g("compl_calls"), g("e13"), g("w15"), g("tails")), hp, 0))
        rows.append(("OSETUP" if k == "1" else "OSETUP%s" % k, "%d instr x %g" % (setup, OSETUP_PRICE), setup * OSETUP_PRICE / C, 0))
        rows.append(("B" if k == "1" else "B%s" % k, "2^24 word clears + 8 ops/tuple", ((1 << 24) + 8 * ntup) / C, 0))
    rows.append(("DRV", "%.3g instr x %g" % DRIVER, DRIVER[0] * DRIVER[1] / C, 0))
    rows.append(("DRVSHA", "%d instr x 400 (the driver's shasum run)" % DRVSHA, DRVSHA * 400 / C, 0))
    rows.append(("DEVSHA", "%d instr x 400 (the freeze hashing: 2 hash-list and 6 single-file shasum runs)" % DEVSHA, DEVSHA * 400 / C, 0))
    rows.append(("R", "replay of the stored pair", REPLAY, 0))
    tot = sum(r[2] for r in rows)
    print("| term | basis | units | log2 | share |")
    print("|---|---|---:|---:|---:|")
    for n, b, u, _ in sorted(rows, key=lambda r: -r[2]):
        print("| %s | %s | %s | %.3f | %.2f%% |" % (n, b, format(round(u, 2), ",.2f"), math.log2(u) if u > 0 else float("-inf"), 100 * u / tot))
    print("| **total** | | %s | **%.4f** | |" % (format(int(math.ceil(tot)), ","), math.log2(tot)))
    print("claim (rounded up to 0.01): %.2f ; max RSS %d (2^%.3f)" % (math.ceil(math.log2(tot) * 100) / 100,
          max(r[3] for r in rows), math.log2(max(r[3] for r in rows))))
    return tot


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != "-" else None, len(sys.argv) > 3 and sys.argv[3] == "cap")
```

### pc8/run.sh (price measurement) (SHA-256 edf7976e142f4a8c; printed text SHA-256 b91f0098fc211473)

```
#!/bin/bash
# v8 price measurement (post-hoc, not part of the chain; the pair already exists): coverage-instrumented runs of the
# solver on the exact v8 model M and of every charged C program on the exact v8 inputs, then covprice (a64ops_jj).
set -u
cd V8/pc8
LOCK="WS/research/heavy.lock"
until mkdir "$LOCK" 2>/dev/null; do sleep 30; done
trap 'rmdir "$LOCK" 2>/dev/null' EXIT
R=V8/run/c1; PC=V6B/pc; CP=R31W/price/covprice.py
read -r d5 d6 d7 d8 d9 d18 < $R/c.txt
# solver on model M
DYLD_LIBRARY_PATH=R31W/price/prefix-cov/lib:TOOLS/lib COV_OUT=m.cov nice -n 10 /usr/bin/time -l -o m_cov.time R31W/price/prefix-cov/bin/stp_simple $R/m.cvc > m_cov.out 2>&1
python3 $CP m.cov m_price.json > m_price.log 2>&1
cmp <(grep "ASSERT" m_cov.out | sort) <(grep "ASSERT" $R/m.out | sort) && echo "M cov output identical" >> run.log
COV_OUT=c1.cov /usr/bin/time -l -o c1_cov.time $PC/cglue_cov char $R/p.out x_c.txt x_m.cvc
COV_OUT=c3.cov /usr/bin/time -l -o c3_cov.time $PC/cglue_cov sp $R/m.out x_sp.txt
mkdir -p xadv; COV_OUT=tabm.cov nice -n 10 /usr/bin/time -l -o tabm_cov.time $PC/tabm_cov $R/c.txt $R/fam.txt $R/sets.txt V8/pc8/xadv 2 200 4194304 0076364172617465
V6_SETUP_ONLY=1 COV_OUT=v6on.cov nice -n 10 /usr/bin/time -l -o v6on_cov.time $PC/v6on_cov $R/adv 000102030405060708090a0b0c0d0e0f /dev/null
COV_OUT=ls2.cov nice -n 10 /usr/bin/time -l -o ls2_cov.time $PC/ls2_cov $R/c.txt $R/sets.txt $R/sp.txt 64 S 2 x_fam.txt 2> ls2_cov.err
cmp x_fam.txt $R/fam.txt && echo "L cov output identical" >> run.log
COV_OUT=sets.cov nice -n 10 /usr/bin/time -l -o sets_cov.time $PC/sets1_cov $d5 $d6 $d7 $d8 $d9 $d18 x_sets.txt
nice -n 10 /usr/bin/time -l -o sets1_plain.time $PC/sets1_plain $d5 $d6 $d7 $d8 $d9 $d18 x_sets1p.txt
for b in c1 c3 tabm v6on ls2 sets; do python3 $PC/covprice2.py $b.cov ${b}_price.json > ${b}_price.log 2>&1; done
echo done >> run.log
```

### covprice.py (solver) (SHA-256 25af7db46ee67b8b; printed text SHA-256 d1bdda42c88c816a)

```
"""r31v6 price measurement: dynamic AArch64 instruction mix of a coverage-instrumented solver run.
Input: COV file ("module offset count" per executed guard, from libcov.dylib) written by an instrumented run.
Each executed guard's region is the run of instructions from its guard call to the next guard call of the same
function (the instructions before a function's first guard call belong to that first guard). Instrumentation
(the guard call, the `mov x0, xN` / `adrp x0` + `add x0, x0` that load its argument) is counted separately.
Every other instruction is priced with a64ops_jj.cost (jungjipdo's per-form table, 50592e75 Appendix C.1; reused
with credit). Output: absolute dynamic counts per class (ordinary / heavy = multiply and FP / divide / unknown),
the ordinary ops, the instrumentation count and the callback count, for the price formula of PRICE.md.
Usage: python3 covprice.py COV OUT.json"""
import collections
import json
import re
import subprocess
import sys

sys.path.insert(0, "R31W/src")
import a64ops_jj as a64  # noqa: E402

LINE = re.compile(r"^([0-9a-f]{8,16})\t(\S+)(?:\t(.*))?$")
GUARD = "symbol stub for: ___sanitizer_cov_trace_pc_guard"


def text_vmaddr(path):
    out = subprocess.run(["otool", "-l", path], capture_output=True, text=True).stdout.split("\n")
    for i, l in enumerate(out):
        if l.strip() == "segname __TEXT":
            for k in range(i, i + 4):
                if "vmaddr" in out[k]:
                    return int(out[k].split()[1], 16)
    raise SystemExit("no __TEXT in " + path)


def is_instr_arg(mn, ops):
    """instruction that only prepares the guard argument x0 right before the guard call"""
    if not ops or ops[0] != "x0":
        return False
    return mn in ("mov", "adrp") or (mn == "add" and len(ops) >= 2 and ops[1] == "x0")


def regions(path):
    """{return_address: [n_insn, ordinary_ops, heavy, div, unknown, instr]} for every guard call of the module."""
    txt = subprocess.run(["otool", "-tV", path], capture_output=True, text=True).stdout.split("\n")
    funcs, cur = [], None
    for line in txt:
        m = LINE.match(line)
        if not m:
            if line.endswith(":") and not line.startswith("("):
                cur = []
                funcs.append(cur)
            continue
        if cur is None:
            cur = []
            funcs.append(cur)
        a, mn, rest = int(m.group(1), 16), m.group(2), m.group(3) or ""
        guard = mn == "bl" and GUARD in rest and "_init" not in rest
        rest = rest.split(";")[0].strip()
        cur.append((a, mn, a64.split_ops(rest) if rest else [], guard))
    R = {}
    unguarded = 0
    for f in funcs:
        gi = [i for i, x in enumerate(f) if x[3]]
        if not gi:
            unguarded += len(f)
            continue
        instr = set()
        for i in gi:
            instr.add(i)
            k = i - 1
            if k >= 0 and is_instr_arg(f[k][1], f[k][2]):
                instr.add(k)
                if f[k][1] == "add" and k - 1 >= 0 and f[k - 1][1] == "adrp" and f[k - 1][2][:1] == ["x0"]:
                    instr.add(k - 1)
        bounds = gi + [len(f)]
        for j, i in enumerate(gi):
            lo = 0 if j == 0 else i + 1
            hi = bounds[j + 1]
            st = [0, 0, 0, 0, 0, 0]
            for k in range(lo, hi):
                if k in instr:
                    st[5] += 1
                    continue
                c, cls = a64.cost(f[k][1], f[k][2])
                st[0] += 1
                if cls == "heavy":
                    st[2] += 1
                elif cls == "div":
                    st[3] += 1
                else:
                    st[1] += c
                    if cls == "unknown":
                        st[4] += 1
            if j == 0:
                st[5] += 1          # the first guard call itself lies before lo..hi only when lo = 0 (counted above)
                st[5] -= 1
            R[f[i][0] + 4] = st
    return R, unguarded


def callback_len(path):
    txt = subprocess.run(["otool", "-tV", path], capture_output=True, text=True).stdout.split("\n")
    n, on = 0, False
    for line in txt:
        if line.startswith("___sanitizer_cov_trace_pc_guard:"):
            on = True
            continue
        if on:
            if LINE.match(line):
                n += 1
            else:
                break
    return n


def main(cov, outp):
    per_mod = collections.defaultdict(list)
    for line in open(cov):
        mod, off, cnt = line.rsplit(None, 2)
        per_mod[mod].append((int(off, 16), int(cnt)))
    T = dict(insn=0, ordinary_ops=0, heavy=0, div=0, unknown=0, instr=0, guard_calls=0, missing=0, missing_calls=0)
    mods = {}
    for mod, lst in per_mod.items():
        R, ung = regions(mod)
        base = text_vmaddr(mod)
        mt = dict(insn=0, heavy=0, div=0, guard_calls=0, regions=len(R), unguarded_static=ung)
        for off, cnt in lst:
            st = R.get(base + off)
            if st is None:
                T["missing"] += 1
                T["missing_calls"] += cnt
                continue
            T["insn"] += cnt * st[0]
            T["ordinary_ops"] += cnt * st[1]
            T["heavy"] += cnt * st[2]
            T["div"] += cnt * st[3]
            T["unknown"] += cnt * st[4]
            T["instr"] += cnt * st[5]
            T["guard_calls"] += cnt
            mt["insn"] += cnt * st[0]
            mt["heavy"] += cnt * st[2]
            mt["div"] += cnt * st[3]
            mt["guard_calls"] += cnt
        mods[mod] = mt
    cb = callback_len("R31W/price/prefix-cov/lib/libcov.dylib")
    T["callback_insn_per_call"] = cb + 3          # + the 3-instruction stub (adrp, ldr, br)
    T["callback_insn"] = T["guard_calls"] * (cb + 3)
    ordn = T["insn"] - T["heavy"] - T["div"]
    T["ordinary_mean"] = T["ordinary_ops"] / ordn if ordn else None
    T["mean_all_covered"] = (T["ordinary_ops"] + 400 * T["heavy"] + 1024 * T["div"]) / T["insn"] if T["insn"] else None
    T["heavy_share_covered"] = T["heavy"] / T["insn"] if T["insn"] else None
    T["est_instrumented_total"] = T["insn"] + T["instr"] + T["callback_insn"]
    T["modules"] = mods
    json.dump(T, open(outp, "w"), indent=1)
    print(json.dumps({k: v for k, v in T.items() if k != "modules"}, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
```

### covprice2.py (C programs: guard symbol name differs) (SHA-256 5d2ee2f608cebc82; printed text SHA-256 f074bc219d7ab171)

```
"""r31v6 price measurement: dynamic AArch64 instruction mix of a coverage-instrumented solver run.
Input: COV file ("module offset count" per executed guard, from libcov.dylib) written by an instrumented run.
Each executed guard's region is the run of instructions from its guard call to the next guard call of the same
function (the instructions before a function's first guard call belong to that first guard). Instrumentation
(the guard call, the `mov x0, xN` / `adrp x0` + `add x0, x0` that load its argument) is counted separately.
Every other instruction is priced with a64ops_jj.cost (jungjipdo's per-form table, 50592e75 Appendix C.1; reused
with credit). Output: absolute dynamic counts per class (ordinary / heavy = multiply and FP / divide / unknown),
the ordinary ops, the instrumentation count and the callback count, for the price formula of PRICE.md.
Usage: python3 covprice.py COV OUT.json"""
import collections
import json
import re
import subprocess
import sys

sys.path.insert(0, "R31W/src")
import a64ops_jj as a64  # noqa: E402

LINE = re.compile(r"^([0-9a-f]{8,16})\t(\S+)(?:\t(.*))?$")
GUARD = "___sanitizer_cov_trace_pc_guard"


def text_vmaddr(path):
    out = subprocess.run(["otool", "-l", path], capture_output=True, text=True).stdout.split("\n")
    for i, l in enumerate(out):
        if l.strip() == "segname __TEXT":
            for k in range(i, i + 4):
                if "vmaddr" in out[k]:
                    return int(out[k].split()[1], 16)
    raise SystemExit("no __TEXT in " + path)


def is_instr_arg(mn, ops):
    """instruction that only prepares the guard argument x0 right before the guard call"""
    if not ops or ops[0] != "x0":
        return False
    return mn in ("mov", "adrp") or (mn == "add" and len(ops) >= 2 and ops[1] == "x0")


def regions(path):
    """{return_address: [n_insn, ordinary_ops, heavy, div, unknown, instr]} for every guard call of the module."""
    txt = subprocess.run(["otool", "-tV", path], capture_output=True, text=True).stdout.split("\n")
    funcs, cur = [], None
    for line in txt:
        m = LINE.match(line)
        if not m:
            if line.endswith(":") and not line.startswith("("):
                cur = []
                funcs.append(cur)
            continue
        if cur is None:
            cur = []
            funcs.append(cur)
        a, mn, rest = int(m.group(1), 16), m.group(2), m.group(3) or ""
        guard = mn == "bl" and GUARD in rest and "_init" not in rest
        rest = rest.split(";")[0].strip()
        cur.append((a, mn, a64.split_ops(rest) if rest else [], guard))
    R = {}
    unguarded = 0
    for f in funcs:
        gi = [i for i, x in enumerate(f) if x[3]]
        if not gi:
            unguarded += len(f)
            continue
        instr = set()
        for i in gi:
            instr.add(i)
            k = i - 1
            if k >= 0 and is_instr_arg(f[k][1], f[k][2]):
                instr.add(k)
                if f[k][1] == "add" and k - 1 >= 0 and f[k - 1][1] == "adrp" and f[k - 1][2][:1] == ["x0"]:
                    instr.add(k - 1)
        bounds = gi + [len(f)]
        for j, i in enumerate(gi):
            lo = 0 if j == 0 else i + 1
            hi = bounds[j + 1]
            st = [0, 0, 0, 0, 0, 0]
            for k in range(lo, hi):
                if k in instr:
                    st[5] += 1
                    continue
                c, cls = a64.cost(f[k][1], f[k][2])
                st[0] += 1
                if cls == "heavy":
                    st[2] += 1
                elif cls == "div":
                    st[3] += 1
                else:
                    st[1] += c
                    if cls == "unknown":
                        st[4] += 1
            if j == 0:
                st[5] += 1          # the first guard call itself lies before lo..hi only when lo = 0 (counted above)
                st[5] -= 1
            R[f[i][0] + 4] = st
    return R, unguarded


def callback_len(path):
    txt = subprocess.run(["otool", "-tV", path], capture_output=True, text=True).stdout.split("\n")
    n, on = 0, False
    for line in txt:
        if line.startswith("___sanitizer_cov_trace_pc_guard:"):
            on = True
            continue
        if on:
            if LINE.match(line):
                n += 1
            else:
                break
    return n


def main(cov, outp):
    per_mod = collections.defaultdict(list)
    for line in open(cov):
        mod, off, cnt = line.rsplit(None, 2)
        per_mod[mod].append((int(off, 16), int(cnt)))
    T = dict(insn=0, ordinary_ops=0, heavy=0, div=0, unknown=0, instr=0, guard_calls=0, missing=0, missing_calls=0)
    mods = {}
    for mod, lst in per_mod.items():
        R, ung = regions(mod)
        base = text_vmaddr(mod)
        mt = dict(insn=0, heavy=0, div=0, guard_calls=0, regions=len(R), unguarded_static=ung)
        for off, cnt in lst:
            st = R.get(base + off)
            if st is None:
                T["missing"] += 1
                T["missing_calls"] += cnt
                continue
            T["insn"] += cnt * st[0]
            T["ordinary_ops"] += cnt * st[1]
            T["heavy"] += cnt * st[2]
            T["div"] += cnt * st[3]
            T["unknown"] += cnt * st[4]
            T["instr"] += cnt * st[5]
            T["guard_calls"] += cnt
            mt["insn"] += cnt * st[0]
            mt["heavy"] += cnt * st[2]
            mt["div"] += cnt * st[3]
            mt["guard_calls"] += cnt
        mods[mod] = mt
    cb = callback_len("R31W/price/prefix-cov/lib/libcov.dylib")
    T["callback_insn_per_call"] = cb + 3          # + the 3-instruction stub (adrp, ldr, br)
    T["callback_insn"] = T["guard_calls"] * (cb + 3)
    ordn = T["insn"] - T["heavy"] - T["div"]
    T["ordinary_mean"] = T["ordinary_ops"] / ordn if ordn else None
    T["mean_all_covered"] = (T["ordinary_ops"] + 400 * T["heavy"] + 1024 * T["div"]) / T["insn"] if T["insn"] else None
    T["heavy_share_covered"] = T["heavy"] / T["insn"] if T["insn"] else None
    T["est_instrumented_total"] = T["insn"] + T["instr"] + T["callback_insn"]
    T["modules"] = mods
    json.dump(T, open(outp, "w"), indent=1)
    print(json.dumps({k: v for k, v in T.items() if k != "modules"}, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
```

### a64ops_jj.py (jungjipdo's per-form table, 50592e75 Appendix C.1) (SHA-256 072c96cb62c8b53a)

```
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

### price.py (price rule) (SHA-256 5d702ffef34685fd; printed text SHA-256 6352eeb30a0fce49)

```
"""v8 per-instruction prices (post-hoc measurement on the exact v8 inputs; method of our filing 6d554419).
For each priced program: ops = ordinary + 400 heavy (multiply, FP) + 1024 (divide, unknown) over the executed basic
blocks of a coverage-instrumented build of the same source on the same input (covprice.py, jungjipdo's a64ops_jj
per-form table); for our C programs also U = instructions outside our code (dyld, libc, kernel) = measured
instrumented total - (covered + instrumentation + cb x guard calls), cb calibrated on ls2, priced at 4.
raw = (ops + 4 U) / plain retired instructions of the run that was charged; price = 1.15 x raw rounded up to 0.5,
never below the price of filing 6d554419 (solver 6, C 5, cglue char 12, cglue sp 17).
Usage: python3 price.py PC8DIR LEDGER_RUNS.tsv OUT.json"""
import json, math, re, sys
d, lr, outp = sys.argv[1:4]
ins = {l.split("\t")[0]: int(l.split("\t")[3]) for l in open(lr)}
on = open(lr.replace("ledger_runs.tsv", "on_1.err")).read()
setup = int(re.search(r"setup instructions (\d+)", on).group(1))
def meas(b):
    return int(re.search(r"(\d+)\s+instructions retired", open("%s/%s_cov.time" % (d, b)).read()).group(1))
def js(b):
    return json.load(open("%s/%s_price.json" % (d, b)))
jl = js("ls2"); cb = (meas("ls2") - jl["insn"] - jl["instr"]) / jl["guard_calls"]
sets_plain = int(re.search(r"(\d+)\s+instructions retired", open(d + "/sets1_plain.time").read()).group(1))
plain = {"m": ins["M"], "c1": ins["C1"], "c3": ins["C3"], "sets": sets_plain, "ls2": ins["L"], "tabm": ins["A"], "v6on": setup}
floor = {"m": 6.0, "c1": 12.0, "c3": 17.0, "sets": 5.0, "ls2": 5.0, "tabm": 5.0, "v6on": 5.0}
rows = []; urows = []; out = {}
CB_STATIC, CB_DYLIB = 11.0, 14.0   # guard-callback length by disassembly of libcov: 11-instruction fast path (static in the C builds); + 3-instruction stub for the solver's dylib
for b in ["m", "sets", "ls2", "tabm", "v6on", "c1", "c3"]:
    j = js(b)
    ops = j["ordinary_ops"] + 400 * j["heavy"] + 1024 * j["div"] + 1024 * j["unknown"]
    cbx = CB_DYLIB if b == "m" else CB_STATIC
    U = max(0.0, meas(b) - (j["insn"] + j["instr"] + cbx * j["guard_calls"]))
    urows.append("| %s | %s | %s | %s | %s | %g | %s |" % (b, format(meas(b), ","), format(j["insn"], ","), format(j["instr"], ","),
                 format(j["guard_calls"], ","), cbx, format(int(U), ",")))
    raw = (ops + 4 * U) / plain[b]
    pr = max(floor[b], math.ceil(1.15 * raw * 2) / 2)
    out[b] = pr
    rows.append("| %s | %s | %s | %s | %s | %.3f | %.3f | %s |" % (b, format(plain[b], ","), format(j["insn"], ","), format(int(ops), ","),
                format(j["heavy"], ","), raw, 1.15 * raw, ("%g (rule; charged 7)" % pr) if b == "m" else ("%g" % pr)))
# the native online loop: a bounded segment (post/online_price.sh), loop = (setup + loop) - (setup only)
P8 = "V8/post"
def jp(n): return json.load(open("%s/%s_price.json" % (P8, n)))
def mp(n): return int(re.search(r"(\d+)\s+instructions retired", open("%s/%s.time" % (P8, n)).read()).group(1))
jo, js_ = jp("ol"), jp("os")
lops = (jo["ordinary_ops"] + 400 * jo["heavy"] + 1024 * (jo["div"] + jo["unknown"])) - (js_["ordinary_ops"] + 400 * js_["heavy"] + 1024 * (js_["div"] + js_["unknown"]))
Uo = max(0.0, mp("ol_cov") - (jo["insn"] + jo["instr"] + CB_STATIC * jo["guard_calls"])); Us = max(0.0, mp("os_cov") - (js_["insn"] + js_["instr"] + CB_STATIC * js_["guard_calls"]))
for n_, j_, lab in (("ol", jo, "v6on setup + loop (post/ol)"), ("os", js_, "v6on setup only (post/os)")):
    urows.append("| %s | %s | %s | %s | %s | %g | %s |" % (lab, format(mp(n_ + "_cov"), ","), format(j_["insn"], ","), format(j_["instr"], ","),
                 format(j_["guard_calls"], ","), CB_STATIC, format(int(max(0.0, mp(n_ + "_cov") - (j_["insn"] + j_["instr"] + CB_STATIC * j_["guard_calls"]))), ",")))
lU = max(0.0, Uo - Us)
lplain = mp("ol_plain") - mp("os_plain")
lraw = (lops + 4 * lU) / lplain
lpr = max(5.0, math.ceil(1.15 * lraw * 2) / 2)
rows.append("| v6on online loop (bounded segment) | %s | %s | %s | %s | %.3f | %.3f | %g |" % (format(lplain, ","), format(jo["insn"] - js_["insn"], ","), format(int(lops), ","),
            format(jo["heavy"] - js_["heavy"], ","), lraw, 1.15 * lraw, lpr))
out["v6on_loop"] = lpr
txt = ["Method (our filing 6d554419's, re-run on the exact v8 inputs after the pair existed; not part of C and not charged):",
       "",
       "1. Coverage-instrumented builds of the solver and of each priced C program ran on the same input as in C, with identical "
       "output (`pc8/run.sh`, Appendix B; the model-M solution and the local-search family were compared and are identical).",
       "2. `covprice.py` (solver) and `covprice2.py` (our C programs, which call the guard by its symbol name) price every "
       "executed instruction of the instrumented code with jungjipdo's per-form table `a64ops_jj`.",
       "3. raw = (ops + 4 U) / plain, where plain = the retired instructions of the charged run and U = the instrumented "
       "run's instructions outside the covered code, priced at 4: U = instrumented total - (covered + instrumentation + "
       "callback x guard calls). The callback length is read from the disassembly of the counter runtime (libcov.c, "
       "Appendix B): 11 instructions on its fast path, linked statically into the C builds, plus a 3-instruction stub "
       "for the solver, whose runtime is a dylib.",
       "4. The price is 1.15 x raw, rounded up to 0.5, and never below the price used in 6d554419.",
       "",
       "| program | plain instructions | covered instructions | ops | heavy (mul/FP) | raw | 1.15 x raw | price |",
       "|---|---:|---:|---:|---:|---:|---:|---:|"] + rows + [
       "",
       "Inputs of U (instrumented runs; pc8/*_cov.time and *_price.json, post/o*_cov.time and o*_price.json):",
       "",
       "| run | instrumented total | covered | instrumentation | guard calls | callback | U |",
       "|---|---:|---:|---:|---:|---:|---:|"] + urows + [
       "",
       "Calibrating the callback on ls2 instead (as 6d554419 did) gives %.3f instructions per call; that would leave sets "
       "with a negative remainder, so it overstates the callback and is not used. sets was measured with its single-thread build "
       "(`sets1`, same loop body) at %s plain instructions. The v6on setup was priced from a setup-only coverage run. "
       "The native online loop was priced separately, by `post/online_price.sh` (Appendix B). That script ran a copy of the "
       "v8 table directory with the trial cap reduced to 1,835,008 trials (262,144 batches), with one worker thread and a "
       "measurement key, both instrumented and plain, each with and without the loop, and took differences. "
       "The loop's raw price is %.3f per instruction (%.0f instructions per trial; the loop includes the AES-128-CTR "
       "instructions, aese/aesmc, which the per-form table prices at 16 each). That is below the charged 5. Python is not "
       "measured: every Python and Perl (shasum) instruction is charged at 400 (as a multiply). The driver allowance is 3e9 "
       "instructions at 25, about 1.8 times our estimate of 1.7e9 (Section 9)." % (cb, format(sets_plain, ","), lraw, lplain / 1835008)]
# The solver's uncovered remainder U is priced at 4 per instruction, but its mix is not measured. The solver is charged
# at 7.0, which covers U at up to 6.24 per instruction (the covered code's own mean is 3.55).
M_CHARGED = max(out["m"], 7.0)
txt.append("")
txt.append("The solver's uncovered remainder U (instructions outside the instrumented code, mostly library code) is not "
           "mix-measured. The solver is therefore charged at 7.0 rather than the rule's 6.5. 7.0 covers a raw price of "
           "6.087, which holds even if every U instruction cost 6.24 (the covered code's own mean is 3.55).")
json.dump({"M": M_CHARGED, "C": out, "text": "\n".join(txt)}, open(outp, "w"), indent=1)
print("\n".join(txt))
```

### pchar.py (v7 parser, run in the pre-freeze conversion check) (SHA-256 2ff5eca0f2098260)

```
"""r31v6 phase P output parser: STP counterexample of cfind.py's model -> characteristic JSON.
Signed rows bit 31..0: '=' equal, 'u' (x, x') = (0, 1), 'n' (1, 0); modular differences x' - x.
Encoding of the LLW24 model: (v, d) = (0, 0) '=', (1, 1) 'u', (0, 1) 'n'.
Usage: python3 pchar.py STP_OUTPUT OUT.json"""
import json
import re
import sys

M = 0xFFFFFFFF


def main(inp, outp):
    v, d = {}, {}
    txt = open(inp).read()
    if not txt.rstrip().endswith("Invalid."):
        raise SystemExit("P: model not satisfiable / no counterexample")
    for m in re.finditer(r"ASSERT\( ([xyw])([vd])_(\d+)_(\d+) = 0b([01]) \);", txt):
        var, kind, step, bit, val = m.group(1), m.group(2), int(m.group(3)), int(m.group(4)), int(m.group(5))
        (v if kind == "v" else d)[(var, step, bit)] = val
    rows, diff = {}, {}
    for var, name in (("x", "A"), ("y", "E"), ("w", "W")):
        for step in range(0, 31):
            s, dd = "", 0
            for bit in range(31, -1, -1):
                dv, vv = d.get((var, step, bit), 0), v.get((var, step, bit), 0)
                if dv == 0:
                    s += "="
                elif vv == 1:
                    s += "u"; dd += 1 << bit
                else:
                    s += "n"; dd -= 1 << bit
            rows["%s%d" % (name, step)] = s
            diff["%s%d" % (name, step)] = dd & M
    hw = lambda r: sum(c != "=" for c in r)
    out = {"rows": rows, "diff": diff,
           "dw": [diff["W%d" % t] for t in range(16)], "d18": diff["W18"], "d16": diff["W16"],
           "hwE": sum(hw(rows["E%d" % t]) for t in range(5, 19)),
           "hwA": sum(hw(rows["A%d" % t]) for t in range(5, 11)),
           "hwE5": hw(rows["E5"]), "hwE6": hw(rows["E6"])}
    json.dump(out, open(outp, "w"), indent=1, sort_keys=True)
    print("P: hwE %d hwA %d hwE5 %d hwE6 %d dW5..9 %s d18 %08x" % (
        out["hwE"], out["hwA"], out["hwE5"], out["hwE6"], " ".join("%08x" % x for x in out["dw"][5:10]), out["d18"]))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
```

### vpair.py (official-verifier check of the pair; charged as DEVPY) (SHA-256 86a443c90747a088; printed text SHA-256 8d2b65caceae4da0)

```
"""v6 E-V: check every PAIR line with the official verifier (hs-official/verifier, digest(.., 'sha256', 31)).
Usage: python3 vpair.py OUT.txt [...]; prints one line per pair, exit 1 on any mismatch."""
import struct, sys
sys.path.insert(0, "HSO")
from verifier.hash_functions import digest
bad = 0; n = 0
for fn in sys.argv[1:]:
    for line in open(fn):
        if not line.startswith("PAIR"):
            continue
        t = line.split()
        m0 = [int(x, 16) for x in t[2:18]]; m1 = [int(x, 16) for x in t[19:35]]; m1p = [int(x, 16) for x in t[36:52]]
        a = struct.pack(">32I", *(m0 + m1)); b = struct.pack(">32I", *(m0 + m1p))
        da, db = digest(a, "sha256", 31), digest(b, "sha256", 31)
        ok = a != b and da == db
        n += 1; bad += not ok
        print("%s %s msgA %s msgB %s digest %s" % (fn, "OK" if ok else "FAIL", a.hex(), b.hex(), da.hex()))
print("pairs %d failures %d" % (n, bad))
sys.exit(1 if bad else 0)
```

### libcov.c (coverage counter runtime of the instrumented builds) (SHA-256 e3bae38e020efa22)

```
/* r31v6 price measurement: basic-block execution counter for -fsanitize-coverage=trace-pc-guard builds.
   Every guard gets a global index; the callback counts executions (64-bit) and records the return address of
   the guard call (first execution). At exit it writes "module offset count" for every executed guard
   (offset = return address - module load address) to $COV_OUT. Not used by any charged run. */
#include <dlfcn.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#define MAXG (1u << 23)
static uint64_t cnt[MAXG];
static uintptr_t pcs[MAXG];
static uint32_t ng;
void __sanitizer_cov_trace_pc_guard_init(uint32_t *start, uint32_t *stop) {
    if (start == stop || *start) return;
    for (uint32_t *x = start; x < stop; x++) { if (ng + 1 >= MAXG) { fprintf(stderr, "cov: too many guards\n"); exit(3); } *x = ++ng; }
}
void __sanitizer_cov_trace_pc_guard(uint32_t *guard) {
    uint32_t g = *guard;
    cnt[g]++;
    if (!pcs[g]) pcs[g] = (uintptr_t)__builtin_return_address(0);
}
__attribute__((destructor)) static void dump(void) {
    const char *fn = getenv("COV_OUT");
    if (!fn) return;
    FILE *f = fopen(fn, "w");
    for (uint32_t g = 1; g <= ng; g++) if (cnt[g]) {
        Dl_info di;
        if (dladdr((void *)pcs[g], &di) && di.dli_fname)
            fprintf(f, "%s %lx %llu\n", di.dli_fname, (unsigned long)(pcs[g] - (uintptr_t)di.dli_fbase), (unsigned long long)cnt[g]);
        else fprintf(f, "? %lx %llu\n", (unsigned long)pcs[g], (unsigned long long)cnt[g]);
    }
    fclose(f);
}
```

### build_cov.sh (instrumented solver build) (SHA-256 a55f8d46225e73af; printed text SHA-256 cbdc0b63179e3bea)

```
#!/bin/bash
# r31v6 price measurement build: CryptoMiniSat 5.14.7 (+ its CaDiCaL/CaDiBack sources already fetched by the
# 2026-10-07 build) and STP 2.4.1, same options as tools/build.sh, plus -fsanitize-coverage=trace-pc-guard,no-prune
# and the counter runtime libcov.dylib. No downloads (FETCHCONTENT_FULLY_DISCONNECTED).
set -euo pipefail
R=R31W/price; P=$R/prefix-cov; T=HST; J=8
export PATH="$T/shim:$T/prefix/bin:$HOME/.local/bin:$PATH"; export PKG_CONFIG_PATH="$T/prefix/lib/pkgconfig"
COV="-fsanitize-coverage=trace-pc-guard,no-prune"
LNK="-L$P/lib -lcov -Wl,-rpath,$P/lib"
cd $R/src/cryptominisat && rm -rf build-cov && mkdir build-cov && cd build-cov
cmake -DENABLE_ASSERTIONS=OFF -DBUILD_SHARED_LIBS=OFF -DSTATIC_BINARY=OFF -DNOCADICAL=ON -DCMAKE_BUILD_TYPE=Release \
  -DFETCHCONTENT_FULLY_DISCONNECTED=ON -DFETCHCONTENT_SOURCE_DIR_CADICAL=$R/src/deps/cadical-src \
  -DFETCHCONTENT_SOURCE_DIR_CADIBACK=$R/src/deps/cadiback-src \
  -DCMAKE_C_FLAGS="$COV" -DCMAKE_CXX_FLAGS="$COV" -DCMAKE_EXE_LINKER_FLAGS="$LNK" -DCMAKE_SHARED_LINKER_FLAGS="$LNK" \
  -DCMAKE_PREFIX_PATH="$T/prefix" -DCMAKE_INSTALL_PREFIX="$P" .. > ../cmake-cov.log 2>&1
cmake --build . -j$J > ../build-cov.log 2>&1 && cmake --install . >> ../build-cov.log 2>&1
echo "[$(date -u +%H:%M:%SZ)] cms done"
cd $R/src/stp && rm -rf build-cov && mkdir build-cov && cd build-cov
cmake -DCMAKE_BUILD_TYPE=Release -DONLY_SIMPLE=ON -DSTP_ALLOCATOR=system -DBISON_EXECUTABLE="$T/prefix/bin/bison" \
  -DCMAKE_PREFIX_PATH="$P;$T/prefix" -Dcryptominisat5_DIR="$P/lib/cmake/cryptominisat5" -DCMAKE_INSTALL_PREFIX="$P" \
  -DENABLE_TESTING=OFF -DENABLE_PYTHON_INTERFACE=OFF \
  -DCMAKE_C_FLAGS="$COV" -DCMAKE_CXX_FLAGS="$COV" -DCMAKE_EXE_LINKER_FLAGS="$LNK" -DCMAKE_SHARED_LINKER_FLAGS="$LNK" .. > ../cmake-cov.log 2>&1
cmake --build . -j$J > ../build-cov.log 2>&1 && cmake --install . >> ../build-cov.log 2>&1
echo "[$(date -u +%H:%M:%SZ)] stp done"; ls -la $P/bin $P/lib
```

### sets1.c (single-thread sets used for the sets price) (SHA-256 b4ad61fcd80f4fe5)

```
/* r31v6 phase S: exact sets by enumeration of all 2^32 words (15 threads, one pass; passes 2-3 disabled: the
   attack tests the step-20 condition directly, no class list is needed).
   Usage: sets dW5 dW6 dW7 dW8 dW9 d18 OUT
   pass 1: V7 = {w : ds0_{dW7}(w) = -dW6}, V8 = {w : ds0_{dW8}(w) = -dW7 - dW9}, G16 = {x : ds1_{dW9}(x) = d18} (listed);
           |V6| = |{w : ds0_{dW6}(w) = -dW5}|, |V9| = |{w : ds0_{dW9}(w) = -dW8}| (counted);
           presence bitmap B of -ds1_{d18}(y) over all y (2^32 bits).
   pass 2: classes = {a = ds0_{dW5}(x) : B[a]} with H5(a) = |{x : ds0_{dW5}(x) = a}|.
   pass 3: H18(-a) = |{y : ds1_{d18}(y) = -a}| for every class a.
   Requires d18 + dW9 = 0 (dW25 = 0). */
#include "../src/r31.h"
#include <pthread.h>
#include <stdatomic.h>

#define NT 1
#define LMAX (1u << 22)
#define CS (1u << 16)          /* class hash slots */
#define CMAX (1u << 14)        /* max classes */

static u32 dW5, dW6, dW7, dW8, dW9, d18;
static _Atomic u64 *B;          /* 2^32-bit presence bitmap */
static int pass;
static u32 ckey[CS]; static unsigned char cuse[CS];
static u32 clist[CMAX]; static u32 ncl;

static inline u32 cslot(u32 a) { return (a ^ (a >> 15) ^ (a << 9) ^ (a >> 23)) & (CS - 1); }
static inline int cfind(u32 a) {   /* slot+1 of class a, 0 if absent */
    u32 i = cslot(a);
    while (cuse[i]) { if (ckey[i] == a) return (int)i + 1; i = (i + 1) & (CS - 1); }
    return 0;
}

typedef struct {
    int id; u64 n6, n9;
    u32 *v7, *v8, *g16; u32 n7, n8, n16;
    u32 *seen; u32 nseen;        /* pass 2: distinct class values seen by this thread */
    u64 *cnt5, *cnt18;
    int overflow;
} job_t;

static void *work(void *p) {
    job_t *j = p;
    u64 lo = ((u64)j->id << 32) / NT, hi = ((u64)(j->id + 1) << 32) / NT;
    if (pass == 1) {
        u32 t7 = -dW6, t8 = -dW7 - dW9, t6 = -dW5, t9 = -dW8;
        for (u64 xx = lo; xx < hi; xx++) {
            u32 x = (u32)xx;
            if (ds0(x, dW6) == t6) j->n6++;
            if (ds0(x, dW9) == t9) j->n9++;
            if (ds0(x, dW7) == t7) { if (j->n7 < LMAX) j->v7[j->n7] = x; j->n7++; }
            if (ds0(x, dW8) == t8) { if (j->n8 < LMAX) j->v8[j->n8] = x; j->n8++; }
            if (ds1(x, dW9) == d18) { if (j->n16 < LMAX) j->g16[j->n16] = x; j->n16++; }
        }
    } else if (pass == 2) {
        for (u64 xx = lo; xx < hi; xx++) {
            u32 a = ds0((u32)xx, dW5);
            if ((atomic_load_explicit(&B[a >> 6], memory_order_relaxed) >> (a & 63)) & 1) {
                u32 i = cslot(a);
                for (;;) {
                    if (j->cnt5[i] == 0) {
                        if (j->nseen >= CMAX) { j->overflow = 1; break; }
                        j->seen[j->nseen++] = a; j->cnt5[i] = ((u64)j->nseen << 40) | 1; break;
                    }
                    if (j->seen[(j->cnt5[i] >> 40) - 1] == a) { j->cnt5[i]++; break; }
                    i = (i + 1) & (CS - 1);
                }
            }
        }
    } else {
        for (u64 xx = lo; xx < hi; xx++) {
            u32 a = -ds1((u32)xx, d18);
            int s = cfind(a);
            if (s) j->cnt18[s - 1]++;
        }
    }
    return NULL;
}

static void run(job_t *J) {
    pthread_t th[NT];
    for (int t = 0; t < NT; t++) pthread_create(&th[t], NULL, work, &J[t]);
    for (int t = 0; t < NT; t++) pthread_join(th[t], NULL);
}

int main(int argc, char **argv) {
    if (argc != 8) { fprintf(stderr, "usage\n"); return 2; }
    dW5 = hexarg(argv[1]); dW6 = hexarg(argv[2]); dW7 = hexarg(argv[3]); dW8 = hexarg(argv[4]);
    dW9 = hexarg(argv[5]); d18 = hexarg(argv[6]);
    if ((u32)(d18 + dW9) != 0) { fprintf(stderr, "S: d18 + dW9 != 0\n"); return 1; }
    job_t *J = calloc(NT, sizeof(job_t));
    for (int t = 0; t < NT; t++) {
        J[t].id = t; J[t].v7 = malloc(4u * LMAX); J[t].v8 = malloc(4u * LMAX); J[t].g16 = malloc(4u * LMAX);
        J[t].seen = malloc(4u * CMAX); J[t].cnt5 = calloc(CS, 8); J[t].cnt18 = calloc(CS, 8);
    }
    pass = 1; run(J);
#if 0
    static u64 h5[CS], h18[CS];
    for (int t = 0; t < NT; t++) {
        if (J[t].overflow) { fprintf(stderr, "S: class overflow\n"); return 1; }
        for (u32 i = 0; i < CS; i++) if (J[t].cnt5[i]) {
            u32 a = J[t].seen[(J[t].cnt5[i] >> 40) - 1];
            u64 n = J[t].cnt5[i] & ((1ULL << 40) - 1);
            int s = cfind(a);
            if (!s) {
                if (ncl >= CMAX) { fprintf(stderr, "S: too many classes\n"); return 1; }
                u32 k = cslot(a);
                while (cuse[k]) k = (k + 1) & (CS - 1);
                cuse[k] = 1; ckey[k] = a; clist[ncl++] = a; s = (int)k + 1;
            }
            h5[s - 1] += n;
        }
    }
    pass = 3; run(J);
    for (int t = 0; t < NT; t++) for (u32 i = 0; i < CS; i++) h18[i] += J[t].cnt18[i];
#endif
    u64 n6 = 0, n9 = 0, n7 = 0, n8 = 0, n16 = 0;
    for (int t = 0; t < NT; t++) {
        n6 += J[t].n6; n9 += J[t].n9; n7 += J[t].n7; n8 += J[t].n8; n16 += J[t].n16;
        if (J[t].n7 > LMAX || J[t].n8 > LMAX || J[t].n16 > LMAX) { fprintf(stderr, "S: list overflow\n"); return 1; }
    }
    FILE *f = fopen(argv[7], "w");
    fprintf(f, "d %08x %08x %08x %08x %08x %08x\n", dW5, dW6, dW7, dW8, dW9, d18);
    fprintf(f, "n6 %llu\nn9 %llu\n", (unsigned long long)n6, (unsigned long long)n9);
    fprintf(f, "V7 %llu\n", (unsigned long long)n7);
    for (int t = 0; t < NT; t++) for (u32 i = 0; i < J[t].n7; i++) fprintf(f, "%08x\n", J[t].v7[i]);
    fprintf(f, "V8 %llu\n", (unsigned long long)n8);
    for (int t = 0; t < NT; t++) for (u32 i = 0; i < J[t].n8; i++) fprintf(f, "%08x\n", J[t].v8[i]);
    fprintf(f, "G16 %llu\n", (unsigned long long)n16);
    for (int t = 0; t < NT; t++) for (u32 i = 0; i < J[t].n16; i++) fprintf(f, "%08x\n", J[t].g16[i]);
    fclose(f);
    fprintf(stderr, "S: |V6| %llu |V7| %llu |V8| %llu |V9| %llu |G16| %llu\n", (unsigned long long)n6,
            (unsigned long long)n7, (unsigned long long)n8, (unsigned long long)n9, (unsigned long long)n16);
    return 0;
}
```

### post/online_price.sh (native online loop price) (SHA-256 6e113cc7ff4dd62b; printed text SHA-256 f26cefdc463f1d20)

```
#!/bin/bash
# post-hoc price measurement of v6on's native online loop (not part of C): the same binaries on a copy of the v8 table
# directory whose trial cap is reduced to 1,835,008 trials (262,144 SWAR batches), one worker thread, a measurement key.
# (1) instrumented build (coverage), setup only and setup + loop; (2) the plain binary, setup only and setup + loop.
# Loop price = (ops(setup+loop) - ops(setup)) / (plain(setup+loop) - plain(setup)).
set -u
cd V8/post
LOCK="WS/research/heavy.lock"
until mkdir "$LOCK" 2>/dev/null; do sleep 30; done
trap 'rmdir "$LOCK" 2>/dev/null' EXIT
PC=V6B/pc
KEY=$(printf 'sha256-r31-v8 price measurement' | shasum -a 256 | cut -c1-32)
export V6_THREADS=1
V6_SETUP_ONLY=1 COV_OUT=os.cov /usr/bin/time -l -o os_cov.time $PC/v6on_cov advp $KEY /dev/null 2> os_cov.err
COV_OUT=ol.cov nice -n 10 /usr/bin/time -l -o ol_cov.time $PC/v6on_cov advp $KEY ol_cov.out 2> ol_cov.err
V6_SETUP_ONLY=1 /usr/bin/time -l -o os_plain.time ../bin/v6on advp $KEY /dev/null 2> os_plain.err
nice -n 10 /usr/bin/time -l -o ol_plain.time ../bin/v6on advp $KEY ol_plain.out 2> ol_plain.err
python3 $PC/covprice2.py os.cov os_price.json > os_price.log 2>&1
python3 $PC/covprice2.py ol.cov ol_price.json > ol_price.log 2>&1
echo done > online_price.done
```

### post/findtrial.c (locates the found trial in the key-1 stream) (SHA-256 5af2d3e53107f0bf)

```
/* post-hoc (not part of C): find the SWAR batch b and lane l of v6on's key-1 stream whose first block equals M0.
   Uses the shipped v6aes.h (AES-128-CTR layout of v6on). Usage: findtrial KEYHEX32 M0_word0..word15 (hex) MAXB */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef uint32_t u32; typedef uint64_t u64;
#include "../src/v6aes.h"
int main(int argc, char **argv) {
    if (argc != 19) { fprintf(stderr, "usage\n"); return 2; }
    uint8_t key[16]; for (int i = 0; i < 16; i++) { unsigned x; sscanf(argv[1] + 2 * i, "%2x", &x); key[i] = (uint8_t)x; }
    aes_expand(key);
    u32 m0[16]; for (int i = 0; i < 16; i++) m0[i] = (u32)strtoul(argv[2 + i], NULL, 16);
    u64 maxb = strtoull(argv[18], NULL, 10);
    u32 m[7][16];
    for (u64 b = 0; b < maxb; b++) {
        gen_batch(b, m);
        for (int l = 0; l < 7; l++) if (m[l][0] == m0[0] && !memcmp(m[l], m0, 64)) { printf("FOUND batch %llu lane %d trial_index %llu thread %llu\n", (unsigned long long)b, l, (unsigned long long)(7 * b + l), (unsigned long long)(b % 12)); return 0; }
    }
    printf("NOT FOUND below %llu\n", (unsigned long long)maxb); return 1;
}
```

### post/pcomp.diff (the rate-model measurement program = v6on.c with this diff) (SHA-256 ecb8b85bedd3e4e6)

```
0a1,5
> /* post-hoc MEASUREMENT program (not part of C, not charged): v6on.c with the online loop replaced by synthetic
>    key-matched trials, to measure the rate-model factors conditional on a key match:
>    cv[0] = a uniformly drawn distinct table key (the law of CV1[0] given a bitmap hit), cv[1..7] uniform (AES-CTR coins);
>    test_trial() and complete() unchanged; caps disabled; a successful complete() is counted (csucc) instead of output.
>    Usage: pcomp ADVDIR KEYHEX32 OUT.txt (env PT_N = synthetic trials, V6_THREADS). */
17c22
< #include "r31.h"
---
> #include "../src/r31.h"
24,25c29,30
< #include "v6aes.h"
< #include "v6io.h"
---
> #include "../src/v6aes.h"
> #include "../src/v6io.h"
47c52
<     int id; u64 batches, trials, kmatch, tuptests, w6pass, r20tests, accepts, compl_calls, e13, w15, tails, found;
---
>     int id; u64 batches, trials, kmatch, tuptests, w6pass, r20tests, accepts, compl_calls, e13, w15, tails, found, csucc;
156c161,162
<             if (complete(T, rg, cv, p, a5, j, m1)) {
---
>             if (complete(T, rg, cv, p, a5, j, m1)) { T->csucc++; continue; }
>             if (0) {
178a185
> static u32 *ukeys; static u64 nukeys, PT_N;
180a188,199
>     if (PT_N) {
>         coin_t rs = {100 + (u64)T->id, 0, {0, 0}, 0}, rg2 = {1 + (u64)T->id, 0, {0, 0}, 0};
>         for (u64 n = (u64)T->id; n < PT_N; n += (u64)NT) {
>             u32 cv[8], m0[16] = {0};
>             u64 r = coin64(&rs);
>             cv[0] = ukeys[(u64)(((unsigned __int128)r * nukeys) >> 64)];
>             for (int i = 1; i < 8; i++) cv[i] = (u32)coin64(&rs);
>             T->trials++; T->kmatch++;
>             test_trial(T, &rg2, m0, cv);
>         }
>         return NULL;
>     }
323a343,346
>     KCAP = TCAP = WCAP = ACAP = ~0ULL;
>     if (getenv("PT_N")) { PT_N = strtoull(getenv("PT_N"), NULL, 10);
>         ukeys = malloc(4 * (ntup + 1)); nukeys = 0;
>         for (u64 i = 0; i < ntup; i++) if (i == 0 || tk[i] != tk[i - 1]) ukeys[nukeys++] = tk[i]; }
354c377
<         S.w6pass += T[t].w6pass; S.r20tests += T[t].r20tests; S.accepts += T[t].accepts; S.compl_calls += T[t].compl_calls;
---
>         S.w6pass += T[t].w6pass; S.r20tests += T[t].r20tests; S.accepts += T[t].accepts; S.compl_calls += T[t].compl_calls; S.csucc += T[t].csucc;
362a386
>     fprintf(out, "PCOMP trials %llu nukeys %llu tuptests %llu w6pass %llu accepts %llu compl_calls %llu csucc %llu e13 %llu w15 %llu\n", (unsigned long long)S.trials, (unsigned long long)nukeys, (unsigned long long)S.tuptests, (unsigned long long)S.w6pass, (unsigned long long)S.accepts, (unsigned long long)S.compl_calls, (unsigned long long)S.csucc, (unsigned long long)S.e13, (unsigned long long)S.w15);
364c388
<     return atomic_load(&stop_flag) == 1 ? 0 : 1;
---
>     return 0;
```

### post/allscan.diff (the no-early-stop scan = v6on.c with this diff) (SHA-256 9ca8e2f703aaa632)

```
0a1,5
> /* post-hoc MEASUREMENT program (not part of C, not charged): v6on.c without the early stop. Every batch b < NBATCH (from
>    the cap in ADVDIR/rate.txt) is evaluated on thread b mod NT exactly as in the online phase (same key stream, same
>    per-thread completion coin streams), every accept is completed, and every verified pair is printed with its batch
>    and lane. Used to show that the stored pair is the only accept among all batches up to the found one.
>    Usage: allscan ADVDIR KEYHEX32 OUT.txt (V6_THREADS = 12). */
17c22
< #include "r31.h"
---
> #include "../src/r31.h"
24,25c29,30
< #include "v6aes.h"
< #include "v6io.h"
---
> #include "../src/v6aes.h"
> #include "../src/v6io.h"
47c52
<     int id; u64 batches, trials, kmatch, tuptests, w6pass, r20tests, accepts, compl_calls, e13, w15, tails, found;
---
>     int id; u64 batches, trials, kmatch, tuptests, w6pass, r20tests, accepts, compl_calls, e13, w15, tails, found; u64 curb; int curl;
164c169
<                 if (atomic_compare_exchange_strong(&stop_flag, &z, 1)) {
---
>                 if (1) { (void)z;
169c174
<                     fprintf(out, " j %d\n", j); fflush(out);
---
>                     fprintf(out, " j %d batch %llu lane %d thread %d\n", j, (unsigned long long)T->curb, T->curl, T->id); fflush(out);
188c193
<             u32 cv[8];
---
>             u32 cv[8]; T->curb = b; T->curl = l;
```


## Appendix C. Run records

ledger_runs.tsv (phase, start, exit, retired instructions, wall s, max RSS, command):

```
C0	2026-10-08T07:53:43Z	0	200191633	0.01	9994240	python3 V8/src/pubchar.py V8/src/pubchar_table.txt V8/run/c1/p.out
C1	2026-10-08T07:53:43Z	0	17193583	0.00	1802240	V8/bin/cglue char V8/run/c1/p.out V8/run/c1/c.txt V8/run/c1/m.cvc
S	2026-10-08T07:55:43Z	0	184954807110	1.23	2834432	V8/bin/sets fffff006 002087f1 4fefb5fa 28011100 00008004 ffff7ffc V8/run/c1/sets.txt
M	2026-10-08T07:55:44Z	0	315870919550	30.22	228261888	TOOLS/bin/stp_simple V8/run/c1/m.cvc
C3	2026-10-08T07:56:15Z	0	13318419	0.00	1540096	V8/bin/cglue sp V8/run/c1/m.out V8/run/c1/sp.txt
L	2026-10-08T07:56:15Z	0	240400504458	7.10	19857408	V8/bin/ls2 V8/run/c1/c.txt V8/run/c1/sets.txt V8/run/c1/sp.txt 64 S 2 V8/run/c1/fam.txt
A	2026-10-08T07:56:22Z	0	19919547288	1.26	8749056	V8/bin/tabm V8/run/c1/c.txt V8/run/c1/fam.txt V8/run/c1/sets.txt V8/run/c1/adv 2 200 4194304 0076364172617465
O	2026-10-08T07:56:23Z	0	185766459621	2.17	814366720	V8/bin/v6on V8/run/c1/adv bf6b900804436c1fa167048b448f358e V8/run/c1/on_1.pairs 100000000000
```

dev_runs.tsv (charged checks outside the chain driver; each row is the measured count of one identical re-run times the number of repetitions; the pre-freeze runs and the first vpair.py run were not measured):

```
DEVPY	592077591	9912320	pubchar.py x3 (two conversion checks before the freeze, one re-measurement)
DEVPY	592889844	11550720	pchar.py x2 (conversion check, re-measurement)
DEVPY	413621536	10174464	inline print of c.json x2
DEVPY	873920176	15958016	vpair.py x2 (official-verifier check of the pair, re-measurement)
DEVC	35037410	1818624	cglue char x2 (conversion check, re-measurement)
```

c.txt (phase C1: d5..d9 d18, then signed masks u n of A5..A12, E5..E12):

```
fffff006 002087f1 4fefb5fa 28011100 00008004 ffff7ffc
A5 00000400 000013fa
A6 00000001 00800000
A7 10000001 01201004
A8 00000000 00000004
A9 00000000 00000000
A10 00008004 00000000
A11 00000000 00000000
A12 00000000 00000000
E5 00001022 0000201c
E6 00008000 00080001
E7 90080408 40800081
E8 49000804 04008000
E9 00000008 00000000
E10 0f810400 200083f8
E11 10c00000 00000008
E12 00000000 00008008
```

S summary (stderr of sets, and the header of sets.txt):

```
S: |V6| 8388608 |V7| 512 |V8| 49408 |V9| 35921920 |G16| 64
d fffff006 002087f1 4fefb5fa 28011100 00008004 ffff7ffc
n6 8388608
n9 35921920
```
sets.txt SHA-256 e2a274cde7e3f95ee8324a7818fd485f2cd055af0bc43e2fd57cb33d4d515664; V7 and G16 lists:

```
V7 512 001cd28a 001cd28b 001cd29a 001cd29b 001cd2aa 001cd2ab 001cd2ba 001cd2bb 001cd2ca 001cd2cb 001cd2da 001cd2db 001cd2ea 001cd2eb 001cd2fa 001cd2fb 003cd28a 003cd28b 003cd29a 003cd29b 003cd2aa 003cd2ab 003cd2ba 003cd2bb 003cd2ca 003cd2cb 003cd2da 003cd2db 003cd2ea 003cd2eb 003cd2fa 003cd2fb 021cd68a 021cd68b 021cd69a 021cd69b 021cd6aa 021cd6ab 021cd6ba 021cd6bb 021cd6ca 021cd6cb 021cd6da 021cd6db 021cd6ea 021cd6eb 021cd6fa 021cd6fb 023cd68a 023cd68b 023cd69a 023cd69b 023cd6aa 023cd6ab 023cd6ba 023cd6bb 023cd6ca 023cd6cb 023cd6da 023cd6db 023cd6ea 023cd6eb 023cd6fa 023cd6fb 0494538a 0494538b 0494539a 0494539b 049453aa 049453ab 049453ba 049453bb 049453ca 049453cb 049453da 049453db 049453ea 049453eb 049453fa 049453fb 04b4538a 04b4538b 04b4539a 04b4539b 04b453aa 04b453ab 04b453ba 04b453bb 04b453ca 04b453cb 04b453da 04b453db 04b453ea 04b453eb 04b453fa 04b453fb 0694578a 0694578b 0694579a 0694579b 069457aa 069457ab 069457ba 069457bb 069457ca 069457cb 069457da 069457db 069457ea 069457eb 069457fa 069457fb 06b4578a 06b4578b 06b4579a 06b4579b 06b457aa 06b457ab 06b457ba 06b457bb 06b457ca 06b457cb 06b457da 06b457db 06b457ea 06b457eb 06b457fa 06b457fb 215af20a 215af20b 215af21a 215af21b 215af22a 215af22b 215af23a 215af23b 215af24a 215af24b 215af25a 215af25b 215af26a 215af26b 215af27a 215af27b 217af20a 217af20b 217af21a 217af21b 217af22a 217af22b 217af23a 217af23b 217af24a 217af24b 217af25a 217af25b 217af26a 217af26b 217af27a 217af27b 235af60a 235af60b 235af61a 235af61b 235af62a 235af62b 235af63a 235af63b 235af64a 235af64b 235af65a 235af65b 235af66a 235af66b 235af67a 235af67b 237af60a 237af60b 237af61a 237af61b 237af62a 237af62b 237af63a 237af63b 237af64a 237af64b 237af65a 237af65b 237af66a 237af66b 237af67a 237af67b 25d2730a 25d2730b 25d2731a 25d2731b 25d2732a 25d2732b 25d2733a 25d2733b 25d2734a 25d2734b 25d2735a 25d2735b 25d2736a 25d2736b 25d2737a 25d2737b 25f2730a 25f2730b 25f2731a 25f2731b 25f2732a 25f2732b 25f2733a 25f2733b 25f2734a 25f2734b 25f2735a 25f2735b 25f2736a 25f2736b 25f2737a 25f2737b 27d2770a 27d2770b 27d2771a 27d2771b 27d2772a 27d2772b 27d2773a 27d2773b 27d2774a 27d2774b 27d2775a 27d2775b 27d2776a 27d2776b 27d2777a 27d2777b 27f2770a 27f2770b 27f2771a 27f2771b 27f2772a 27f2772b 27f2773a 27f2773b 27f2774a 27f2774b 27f2775a 27f2775b 27f2776a 27f2776b 27f2777a 27f2777b 881dd28a 881dd28b 881dd29a 881dd29b 881dd2aa 881dd2ab 881dd2ba 881dd2bb 881dd2ca 881dd2cb 881dd2da 881dd2db 881dd2ea 881dd2eb 881dd2fa 881dd2fb 883dd28a 883dd28b 883dd29a 883dd29b 883dd2aa 883dd2ab 883dd2ba 883dd2bb 883dd2ca 883dd2cb 883dd2da 883dd2db 883dd2ea 883dd2eb 883dd2fa 883dd2fb 8a1dd68a 8a1dd68b 8a1dd69a 8a1dd69b 8a1dd6aa 8a1dd6ab 8a1dd6ba 8a1dd6bb 8a1dd6ca 8a1dd6cb 8a1dd6da 8a1dd6db 8a1dd6ea 8a1dd6eb 8a1dd6fa 8a1dd6fb 8a3dd68a 8a3dd68b 8a3dd69a 8a3dd69b 8a3dd6aa 8a3dd6ab 8a3dd6ba 8a3dd6bb 8a3dd6ca 8a3dd6cb 8a3dd6da 8a3dd6db 8a3dd6ea 8a3dd6eb 8a3dd6fa 8a3dd6fb 8c95538a 8c95538b 8c95539a 8c95539b 8c9553aa 8c9553ab 8c9553ba 8c9553bb 8c9553ca 8c9553cb 8c9553da 8c9553db 8c9553ea 8c9553eb 8c9553fa 8c9553fb 8cb5538a 8cb5538b 8cb5539a 8cb5539b 8cb553aa 8cb553ab 8cb553ba 8cb553bb 8cb553ca 8cb553cb 8cb553da 8cb553db 8cb553ea 8cb553eb 8cb553fa 8cb553fb 8e95578a 8e95578b 8e95579a 8e95579b 8e9557aa 8e9557ab 8e9557ba 8e9557bb 8e9557ca 8e9557cb 8e9557da 8e9557db 8e9557ea 8e9557eb 8e9557fa 8e9557fb 8eb5578a 8eb5578b 8eb5579a 8eb5579b 8eb557aa 8eb557ab 8eb557ba 8eb557bb 8eb557ca 8eb557cb 8eb557da 8eb557db 8eb557ea 8eb557eb 8eb557fa 8eb557fb a95bf20a a95bf20b a95bf21a a95bf21b a95bf22a a95bf22b a95bf23a a95bf23b a95bf24a a95bf24b a95bf25a a95bf25b a95bf26a a95bf26b a95bf27a a95bf27b a97bf20a a97bf20b a97bf21a a97bf21b a97bf22a a97bf22b a97bf23a a97bf23b a97bf24a a97bf24b a97bf25a a97bf25b a97bf26a a97bf26b a97bf27a a97bf27b ab5bf60a ab5bf60b ab5bf61a ab5bf61b ab5bf62a ab5bf62b ab5bf63a ab5bf63b ab5bf64a ab5bf64b ab5bf65a ab5bf65b ab5bf66a ab5bf66b ab5bf67a ab5bf67b ab7bf60a ab7bf60b ab7bf61a ab7bf61b ab7bf62a ab7bf62b ab7bf63a ab7bf63b ab7bf64a ab7bf64b ab7bf65a ab7bf65b ab7bf66a ab7bf66b ab7bf67a ab7bf67b add3730a add3730b add3731a add3731b add3732a add3732b add3733a add3733b add3734a add3734b add3735a add3735b add3736a add3736b add3737a add3737b adf3730a adf3730b adf3731a adf3731b adf3732a adf3732b adf3733a adf3733b adf3734a adf3734b adf3735a adf3735b adf3736a adf3736b adf3737a adf3737b afd3770a afd3770b afd3771a afd3771b afd3772a afd3772b afd3773a afd3773b afd3774a afd3774b afd3775a afd3775b afd3776a afd3776b afd3777a afd3777b aff3770a aff3770b aff3771a aff3771b aff3772a aff3772b aff3773a aff3773b aff3774a aff3774b aff3775a aff3775b aff3776a aff3776b aff3777a aff3777b
G16 64 031bbffc 064bbffe 09b3bffd 0ce3bfff 131bbffc 164bbffe 19b3bffd 1ce3bfff 231bbffc 264bbffe 29b3bffd 2ce3bfff 331bbffc 364bbffe 39b3bffd 3ce3bfff 431bbffc 464bbffe 49b3bffd 4ce3bfff 531bbffc 564bbffe 59b3bffd 5ce3bfff 631bbffc 664bbffe 69b3bffd 6ce3bfff 731bbffc 764bbffe 79b3bffd 7ce3bfff 831bbffc 864bbffe 89b3bffd 8ce3bfff 931bbffc 964bbffe 99b3bffd 9ce3bfff a31bbffc a64bbffe a9b3bffd ace3bfff b31bbffc b64bbffe b9b3bffd bce3bfff c31bbffc c64bbffe c9b3bffd cce3bfff d31bbffc d64bbffe d9b3bffd dce3bfff e31bbffc e64bbffe e9b3bffd ece3bfff f31bbffc f64bbffe f9b3bffd fce3bfff
```

Full `/usr/bin/time -l` output of every chain process (machine: Apple M5 Pro, 5 performance + 10 efficiency cores, 48 GiB; macOS counters):

C0:
```
        0.01 real         0.01 user         0.00 sys
             9994240  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
                1578  page reclaims
                  18  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   0  messages sent
                   0  messages received
                   0  signals received
                   0  voluntary context switches
                  35  involuntary context switches
           200191633  instructions retired
            74949647  cycles elapsed
             6242568  peak memory footprint
```

C1:
```
        0.00 real         0.00 user         0.00 sys
             1802240  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
                 277  page reclaims
                   1  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   0  messages sent
                   0  messages received
                   0  signals received
                   0  voluntary context switches
                  10  involuntary context switches
            17193583  instructions retired
             6697829  cycles elapsed
             1360208  peak memory footprint
```

S:
```
        1.23 real        10.31 user         0.02 sys
             2834432  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
                 351  page reclaims
                   1  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   0  messages sent
                   0  messages received
                   0  signals received
                   2  voluntary context switches
                4784  involuntary context switches
        184954807110  instructions retired
         43705220262  cycles elapsed
             2704128  peak memory footprint
```

M:
```
       30.22 real        29.84 user         0.26 sys
           228261888  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
               65795  page reclaims
                 199  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   0  messages sent
                   0  messages received
                   0  signals received
                   2  voluntary context switches
                9944  involuntary context switches
        315870919550  instructions retired
        132141137957  cycles elapsed
           224805416  peak memory footprint
```

C3:
```
        0.00 real         0.00 user         0.00 sys
             1540096  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
                 261  page reclaims
                   1  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   0  messages sent
                   0  messages received
                   0  signals received
                   0  voluntary context switches
                   6  involuntary context switches
            13318419  instructions retired
             4991272  cycles elapsed
             1081656  peak memory footprint
```

L:
```
        7.10 real         6.68 user         0.03 sys
            19857408  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
                1379  page reclaims
                   1  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   0  messages sent
                   0  messages received
                   0  signals received
                   1  voluntary context switches
                3141  involuntary context switches
        240400504458  instructions retired
         28812136977  cycles elapsed
            19464576  peak memory footprint
```

A:
```
        1.26 real         0.89 user         0.04 sys
             8749056  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
                 701  page reclaims
                   1  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   0  messages sent
                   0  messages received
                   0  signals received
                 127  voluntary context switches
                 496  involuntary context switches
         19919547288  instructions retired
          4035005692  cycles elapsed
             8372656  peak memory footprint
```

O:
```
        2.17 real        18.87 user         0.08 sys
           814366720  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
               49874  page reclaims
                   1  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   0  messages sent
                   0  messages received
                   0  signals received
                   0  voluntary context switches
                9228  involuntary context switches
        185766459621  instructions retired
         80917552268  cycles elapsed
           814384112  peak memory footprint
```

sp.txt (phase M -> C3: A1..A4 E3..E12 of copy P):

```
27421179 85d5f711 1061a703 8fc93dd6 f233c6eb 03e04fd6 3d3ea35d a8a97e07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec
```

ls2 log (phase L):

```
L2: base tuples 18432 completions 2 dA9 00000000
L2: exp 8 sps 147 cand 263168 head 9781 rep 3245 tup 3246 tails 55566995
L2: exp 16 sps 198 cand 526336 head 19364 rep 6565 tup 6566 tails 108295798
L2: exp 24 sps 240 cand 789504 head 28937 rep 9857 tup 9858 tails 161291424
L2: exp 32 sps 291 cand 1052672 head 38530 rep 12965 tup 12966 tails 215980134
L2: exp 40 sps 355 cand 1315840 head 48194 rep 15760 tup 15761 tails 273105256
L2: exp 48 sps 400 cand 1579008 head 57882 rep 18656 tup 18657 tails 329472923
L2: exp 56 sps 409 cand 1842176 head 67509 rep 21309 tup 21310 tails 387123338
L2: exp 64 sps 483 cand 2105344 head 77037 rep 24498 tup 24499 tails 440028299
L2: END expansions 64 sps 483 tuples 5704080 completions 966 cand 2105344 head 77037 rep 24498 tupcalls 24499 tails 440028299 compevals 2934783
```

tabm (phase A):

```
A: sps 483 tuples 5704080 completions 966 hits 1282/4194304 log2q -30.2323 NCAP 2522586633 (2^31.2323)
sps 483 tuples 5704080 completions 966 mcs 4194304 hits 1282 n6 8388608 log2q -30.232257 NCAP 2522586633
```

v6on (phase O, key 1):

```
O: setup instructions 5094440758 budget 100000000000
        2.17 real        18.87 user         0.08 sys
           814366720  maximum resident set size
                   0  average shared memory size
                   0  average unshared data size
                   0  average unshared stack size
               49874  page reclaims
                   1  page faults
                   0  swaps
                   0  block input operations
                   0  block output operations
                   0  messages sent
                   0  messages received
                   0  signals received
                   0  voluntary context switches
                9228  involuntary context switches
        185766459621  instructions retired
         80917552268  cycles elapsed
           814384112  peak memory footprint
START ncap 2522586633 batches 360369519 sps 483 tuples 5704080 keys 2130185 completions 966 maxnc 2 n16 64 KCAP 5008628 TCAP 13404930 WCAP 30269 ACAP 64 threads 12
PAIR M0 f228b816 3644ca7a 31ea7f59 478c7d72 9d064d1e f874313c cdfe9b17 7fd7577d 2ebc719d c82b3e50 e9c595c2 d2e670aa 88bbefaa 946f6e50 1b4b6b5e 2408ef77 M1 94012921 4476294f c880eda8 67b6a3a7 e1e22aa3 c8a2b743 9ac56136 06b457fb 63f1956c 912a6919 6b02539a 6319a5f3 6c6a82a1 297ce0d8 65acf487 962b7beb M1p 94012921 4476294f c880eda8 67b6a3a7 e1e22aa3 c8a2a749 9ae5e927 56a40df5 8bf2a66c 912ae91d 6b02539a 6319a5f3 6c6a82a1 297ce0d8 65acf487 962b7beb j 467
END batches 15583114 trials 109081798 kmatch 54474 tuptests 145709 w6pass 291 r20tests 37194 accepts 1 compl_calls 1 e13 4140 w15 13 tails 1 found 1 stop 1
```

Post-hoc location of the found trial (post/findtrial.c on the key-1 stream; stdout and retired instructions):

```
FOUND batch 15645968 lane 1 trial_index 109521777 thread 8
17213732803  instructions retired
```

Post-hoc scan of every batch 0..15,645,968 without the early stop (post/allscan, cap 109,521,783 trials, 12 threads):

```
PAIR M0 f228b816 ... j 467 batch 15645968 lane 1 thread 8
END batches 15645969 trials 109521783 kmatch 54692 tuptests 146260 w6pass 294 r20tests 37578 accepts 1 compl_calls 1 e13 4140 w15 13 tails 1 found 1 stop 0
186574667509  instructions retired
```

Native online loop price run (post/online_price.sh; cap 1,835,008 trials, 1 thread, measurement key):

```
os_cov: 28146051476 instructions retired, 1.15 real
ol_cov: 33748888181 instructions retired, 1.41 real
os_plain: 5014168124 instructions retired, 0.30 real
ol_plain: 8054785311 instructions retired, 0.56 real
END batches 262144 trials 1835008 kmatch 890 tuptests 2304 w6pass 6 r20tests 768 accepts 0 compl_calls 0 e13 0 w15 0 tails 0 found 0 stop 0
```

Rate-model measurement (post/pcomp, 2^30 synthetic key-matched trials, 10 threads):

```
END batches 0 trials 1073741824 kmatch 1073741824 tuptests 2875209082 w6pass 5612488 r20tests 718341150 accepts 1741 compl_calls 1741 e13 7333673 w15 28180 tails 1741 found 0 stop 0
PCOMP trials 1073741824 nukeys 2130185 tuptests 2875209082 w6pass 5612488 accepts 1741 compl_calls 1741 csucc 1741 e13 7333673 w15 28180
```

Instrumented binaries of the price measurement (SHA-256, first 16 hex):

```
8b629abfab57250e  cglue_cov
602657c5c77871ea  sets1_cov
09a03975e98ae4aa  sets1_plain
48eee8617f0a9277  ls2_cov
426449dd24f6e936  tabm_cov
e898673894964197  v6on_cov
609dce4ddc612733  stp_simple (instrumented)
```

fam.txt (phase L output: 483 starting points, A1..A4 E3..E12, tuples, completions; SHA-256 557f040e83536b0d976c002a123ae6f2bc9dc4860944f06f17bf187a77f3a039):

```
27421179 85d5f711 1061a703 8fc93dd6 da9d2da3 a03060ce 3d3ea35d a8a97e07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
c959f23d 85c7f711 105a2703 8fd1bdd6 d5b2ade3 a583248e 3d3ea35d a8a97e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 21504 2
07460f79 85d5f711 9061a703 0fc93dd6 5a9d2da3 203060ce 3d3ea35d a8a97e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
26421179 85d5f711 1061a703 8fc93dd6 d99d2da3 a13060ce 3c3ea35d a8a97e07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
a7421179 65d5f731 1061a703 8fc93dd6 58575d23 c03058ce 3d3ea35d 88a97e27 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 10240 2
27421179 85d4f711 1061a703 8fc93dd6 db1d29a3 a03060ce 3d3ea35d a8a87e07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
27421179 85d6f711 1061a703 8fc93dd6 da171ff3 883611de 3d3ea35d a8aa7e07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 6400 2
27621179 85b4f711 1061a703 8fc93dd6 cb1dada3 a03060ce 3d3ea35d a8887e07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
27621179 85b5f711 1061a703 8fc93dd6 ca9da9a3 a03060ce 3d3ea35d a8897e07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
175f11d9 85b9f711 105da703 8fc53dd6 daa12da3 a03060ce 3d3ea35d a8a97e07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
573b0f58 85a9f711 103da703 8fb53dd6 dac12da3 a03060ce 3d3ea35d a8a97e07 6a96fb85 9428c259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
674e0ef8 85d5f711 1041a703 8fb93dd6 dabd2da3 a03060ce 3d3ea35d a8a97e07 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
06460f79 85d5f711 9061a703 0fc93dd6 599d2da3 213060ce 3c3ea35d a8a97e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
07460f79 85d4f711 9061a703 0fc93dd6 5b1d29a3 203060ce 3d3ea35d a8a87e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
07660f79 85b5f711 9061a703 0fc93dd6 4a9da9a3 203060ce 3d3ea35d a8897e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
37630fd9 85b9f711 905da703 0fc53dd6 5aa12da3 203060ce 3d3ea35d a8a97e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
474a10f8 85d5f711 9041a703 0fb93dd6 5abd2da3 203060ce 3d3ea35d a8a97e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
29421979 87d5f711 1061a703 8fc93dd6 c6a4e5a3 9e3060ce 3d3eab5d aaa97e07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 8704 2
26421179 85d4f711 1061a703 8fc93dd6 da1d29a3 a13060ce 3c3ea35d a8a87e07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
26621179 85b5f711 1061a703 8fc93dd6 c99da9a3 a13060ce 3c3ea35d a8897e07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
28421179 87d5f711 1061a703 8fc93dd6 c5a4eda3 9f3060ce 3c3ea35d aaa97e07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 9216 2
1f420f79 85d5f511 1061a703 8fc93dd6 83d44f2b 601704de 353ea35d a8a97c07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
664e0ef8 85d5f711 1041a703 8fb93dd6 d9bd2da3 a13060ce 3c3ea35d a8a97e07 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
175f11d9 85b8f711 105da703 8fc53dd6 db2129a3 a03060ce 3d3ea35d a8a87e07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
674e0ef8 85d4f711 1041a703 8fb93dd6 db3d29a3 a03060ce 3d3ea35d a8a87e07 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
175f11d9 85bbf711 105da703 8fc53dd6 d3239f73 883611de 3d3ea35d a8ab7e07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 11008 2
175f11d9 8599f711 105da703 8fc53dd6 caa1a9a3 a03060ce 3d3ea35d a8897e07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
672e0ef8 85b5f711 1041a703 8fb93dd6 cabda9a3 a03060ce 3d3ea35d a8897e07 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
195f11d9 87b9f711 105da703 8fc53dd6 c6a8eda3 9e3060ce 3d3ea35d aaa97e07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 9216 2
c859f23d 85c7f711 105a2703 8fd1bdd6 d4b2ade3 a683248e 3c3ea35d a8a97e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 21504 2
4959f23d 65c7f731 105a2703 8fd1bdd6 786adc2b a82411d6 3d3ea35d 88a97e27 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 4096 2
c959f83d 85c7f811 105a2703 8fd1bdd6 b5b32ce7 a5832392 3d3ea35d a8a97f07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 17408 2
c958f83d 85c6f811 105a2703 8fd1bdd6 b63228e7 a5832392 3d3ea35d a8a87f07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 17408 2
c959f83d 85a7f811 105a2703 8fd1bdd6 a5d2a8e7 a5832392 3d3ea35d a8897f07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 17408 2
c958f23d 85c6f711 105a2703 8fd1bdd6 d631a9e3 a583248e 3d3ea35d a8a87e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 21504 2
c95ef23d 85c8f711 105a2703 8fd1bdd6 d531a1a3 a581248e 3d3ea35d a8aa7e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 18432 2
c958f23d 85a6f711 105a2703 8fd1bdd6 c6522de3 a583248e 3d3ea35d a8887e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 21504 2
c959f23d 85a7f711 105a2703 8fd1bdd6 c5d329e3 a583248e 3d3ea35d a8897e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 21504 2
394ef19d 85dbf711 10662703 8fcdbdd6 d5a6ade3 a583248e 3d3ea35d a8a97e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 21504 2
795aef1c 85dbf711 10462703 8fbdbdd6 d5c6ade3 a583248e 3d3ea35d a8a97e07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c19 b16399ec 21504 2
0955f1bd 85b7f711 105a2703 8fc1bdd6 d5b2ade3 a583248e 3d3ea35d a8a97e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 21504 2
cb59fa3d 87c7f711 105a2703 8fd1bdd6 d9ba65e3 a383248e 3d3eab5d aaa97e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 10240 2
c859f83d 85c7f811 105a2703 8fd1bdd6 b4b32ce7 a6832392 3c3ea35d a8a97f07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 17408 2
c858f23d 85c6f711 105a2703 8fd1bdd6 d531a9e3 a683248e 3c3ea35d a8a87e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 21504 2
c859f23d 85a7f711 105a2703 8fd1bdd6 c4d329e3 a683248e 3c3ea35d a8897e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 21504 2
ca59f23d 87c7f711 105a2703 8fd1bdd6 d6ba6de3 a483248e 3c3ea35d aaa97e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 10752 2
c159f03d 85c7f511 105a2703 8fd1bdd6 9db1ade3 25832696 353ea35d a8a97c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 17920 2
0855f1bd 85b7f711 105a2703 8fc1bdd6 d4b2ade3 a683248e 3c3ea35d a8a97e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 21504 2
394ef79d 85dbf811 10662703 8fcdbdd6 b5a72ce7 a5832392 3d3ea35d a8a97f07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 17408 2
0955f7bd 85b7f811 105a2703 8fc1bdd6 b5b32ce7 a5832392 3d3ea35d a8a97f07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 17408 2
394df19d 85daf711 10662703 8fcdbdd6 d625a9e3 a583248e 3d3ea35d a8a87e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 21504 2
0954f1bd 85b6f711 105a2703 8fc1bdd6 d631a9e3 a583248e 3d3ea35d a8a87e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 21504 2
394cf19d 85ddf711 10662703 8fcdbdd6 d4a6a5a3 a581248e 3d3ea35d a8ab7e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 27136 2
396ef19d 85bbf711 10662703 8fcdbdd6 c5c729e3 a583248e 3d3ea35d a8897e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 21504 2
0955f1bd 8597f711 105a2703 8fc1bdd6 c5d329e3 a583248e 3d3ea35d a8897e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 21504 2
3b4ef19d 87dbf711 10662703 8fcdbdd6 d9ae6de3 a383248e 3d3ea35d aaa97e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 10752 2
0575d977 85963711 9021e703 0f895dd6 7bdb0d23 207040ce 3d3ea35d a8a97e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa273c18 b16399ec 12288 2
87460f79 65d5f731 9061a703 0fc93dd6 d8575d23 403058ce 3d3ea35d 88a97e27 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 10240 2
07460f79 85d6f711 9061a703 0fc93dd6 5a171ff3 083611de 3d3ea35d a8aa7e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 6400 2
07660f79 85b4f711 9061a703 0fc93dd6 4b1dada3 203060ce 3d3ea35d a8887e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
77371158 85a9f711 903da703 0fb53dd6 5ac12da3 203060ce 3d3ea35d a8a97e07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
09461779 87d5f711 9061a703 0fc93dd6 46a4e5a3 1e3060ce 3d3eab5d aaa97e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 8704 2
06460f79 85d4f711 9061a703 0fc93dd6 5a1d29a3 213060ce 3c3ea35d a8a87e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
06660f79 85b5f711 9061a703 0fc93dd6 499da9a3 213060ce 3c3ea35d a8897e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
08460f79 87d5f711 9061a703 0fc93dd6 45a4eda3 1f3060ce 3c3ea35d aaa97e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 9216 2
ff460d79 85d5f511 9061a703 0fc93dd6 03d44f2b e01704de 353ea35d a8a97c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
464a10f8 85d5f711 9041a703 0fb93dd6 59bd2da3 213060ce 3c3ea35d a8a97e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
37630fd9 85b8f711 905da703 0fc53dd6 5b2129a3 203060ce 3d3ea35d a8a87e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
474a10f8 85d4f711 9041a703 0fb93dd6 5b3d29a3 203060ce 3d3ea35d a8a87e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
37630fd9 85bbf711 905da703 0fc53dd6 53239f73 083611de 3d3ea35d a8ab7e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 11008 2
37630fd9 8599f711 905da703 0fc53dd6 4aa1a9a3 203060ce 3d3ea35d a8897e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
472a10f8 85b5f711 9041a703 0fb93dd6 4abda9a3 203060ce 3d3ea35d a8897e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
39630fd9 87b9f711 905da703 0fc53dd6 46a8eda3 1e3060ce 3d3ea35d aaa97e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 9216 2
a6421179 65d5f731 1061a703 8fc93dd6 57575d23 c13058ce 3c3ea35d 88a97e27 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 10240 2
28421779 87d5f811 1061a703 8fc93dd6 86dd8c30 5f1701dc 3c3ea35d aaa97f07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 7168 2
28420f79 87d5f511 1061a703 8fc93dd6 85a3eda4 9f3062d0 3c3ea35d aaa97c07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 2048 2
26421179 85d6f711 1061a703 8fc93dd6 d9171ff3 893611de 3c3ea35d a8aa7e07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 6400 2
26621179 85b4f711 1061a703 8fc93dd6 ca1dada3 a13060ce 3c3ea35d a8887e07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
28421179 87d4f711 1061a703 8fc93dd6 c624e9a3 9f3060ce 3c3ea35d aaa87e07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 9216 2
28621179 87b5f711 1061a703 8fc93dd6 b5a569a3 9f3060ce 3c3ea35d aa897e07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 9216 2
1e420f79 85d5f511 1061a703 8fc93dd6 82d44f2b 611704de 343ea35d a8a97c07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
165f19d9 85b9f711 105da703 8fc53dd6 d9a125a3 a13060ce 3c3eab5d a8a97e07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 17408 2
664e0ef8 85d4f711 1041a703 8fb93dd6 da3d29a3 a13060ce 3c3ea35d a8a87e07 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
662e0ef8 85b5f711 1041a703 8fb93dd6 c9bda9a3 a13060ce 3c3ea35d a8897e07 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
185f11d9 87b9f711 105da703 8fc53dd6 c5a8eda3 9f3060ce 3c3ea35d aaa97e07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 9216 2
684e0ef8 87d5f711 1041a703 8fb93dd6 c5c4eda3 9f3060ce 3c3ea35d aaa97e07 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 9216 2
a7421779 65d5f831 1061a703 8fc93dd6 3857dc27 c0305fd2 3d3ea35d 88a97f27 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 8192 2
a7421779 65d4f831 1061a703 8fc93dd6 37d7d7e7 c0305fd2 3d3ea35d 88a87f27 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 8192 2
a7621779 65b5f831 1061a703 8fc93dd6 28575827 c0305fd2 3d3ea35d 88897f27 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 8192 2
a7421179 65d4f731 1061a703 8fc93dd6 57d75923 c03058ce 3d3ea35d 88a87e27 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 10240 2
a7421179 65d6f731 1061a703 8fc93dd6 6fd15033 a736115e 3d3ea35d 88aa7e27 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 9472 2
a7621179 65b4f731 1061a703 8fc93dd6 47d7dd23 c03058ce 3d3ea35d 88887e27 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 10240 2
a7621179 65b5f731 1061a703 8fc93dd6 4857d923 c03058ce 3d3ea35d 88897e27 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 10240 2
975f11d9 65b9f731 105da703 8fc53dd6 585b5d23 c03058ce 3d3ea35d 88a97e27 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 10240 2
d73b0f58 65a9f731 103da703 8fb53dd6 587b5d23 c03058ce 3d3ea35d 88a97e27 6a96fb85 9428c259 41e433d3 f00ad3fb aa270c18 b16399ec 10240 2
e74e0ef8 65d5f731 1041a703 8fb93dd6 58775d23 c03058ce 3d3ea35d 88a97e27 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 10240 2
86460f79 65d5f731 9061a703 0fc93dd6 d7575d23 413058ce 3c3ea35d 88a97e27 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 10240 2
87461579 65d5f831 9061a703 0fc93dd6 b857dc27 40305fd2 3d3ea35d 88a97f27 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 8192 2
87460f79 65d4f731 9061a703 0fc93dd6 d7d75923 403058ce 3d3ea35d 88a87e27 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 10240 2
87660f79 65b5f731 9061a703 0fc93dd6 c857d923 403058ce 3d3ea35d 88897e27 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 10240 2
b7630fd9 65b9f731 905da703 0fc53dd6 d85b5d23 403058ce 3d3ea35d 88a97e27 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 10240 2
c74a10f8 65d5f731 9041a703 0fb93dd6 d8775d23 403058ce 3d3ea35d 88a97e27 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c18 b16399ec 10240 2
a9421979 67d5f731 1061a703 8fc93dd6 645f1523 be3058ce 3d3eab5d 8aa97e27 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 5184 2
a6421779 65d5f831 1061a703 8fc93dd6 3757dc27 c1305fd2 3c3ea35d 88a97f27 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 8192 2
a6421179 65d4f731 1061a703 8fc93dd6 56d75923 c13058ce 3c3ea35d 88a87e27 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 10240 2
a6621179 65b5f731 1061a703 8fc93dd6 4757d923 c13058ce 3c3ea35d 88897e27 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 10240 2
a8421179 67d5f731 1061a703 8fc93dd6 635f1d23 bf3058ce 3c3ea35d 8aa97e27 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 5120 2
9f420f79 65d5f531 1061a703 8fc93dd6 40525c2b a83413de 353ea35d 88a97c27 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 7680 2
e64e0ef8 65d5f731 1041a703 8fb93dd6 57775d23 c13058ce 3c3ea35d 88a97e27 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 10240 2
975f17d9 65b9f831 105da703 8fc53dd6 385bdc27 c0305fd2 3d3ea35d 88a97f27 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 8192 2
975f11d9 65b8f731 105da703 8fc53dd6 57db5923 c03058ce 3d3ea35d 88a87e27 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 10240 2
e74e0ef8 65d4f731 1041a703 8fb93dd6 57f75923 c03058ce 3d3ea35d 88a87e27 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 10240 2
975f11d9 65bbf731 105da703 8fc53dd6 775553f3 a83611de 3d3ea35d 88ab7e27 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 4864 2
975f11d9 6599f731 105da703 8fc53dd6 485bd923 c03058ce 3d3ea35d 88897e27 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 10240 2
e72e0ef8 65b5f731 1041a703 8fb93dd6 4877d923 c03058ce 3d3ea35d 88897e27 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 10240 2
995f11d9 67b9f731 105da703 8fc53dd6 64631d23 be3058ce 3d3ea35d 8aa97e27 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 5120 2
27621179 85b6f711 1061a703 8fc93dd6 c8179ff3 883611de 3d3ea35d a88a7e07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 10496 2
573b0f58 85a8f711 103da703 8fb53dd6 db4129a3 a03060ce 3d3ea35d a8a87e07 6a96fb85 9428c259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
29421979 87d4f711 1061a703 8fc93dd6 c724e1a3 9e3060ce 3d3eab5d aaa87e07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 6400 2
1f420f79 85d4f511 1061a703 8fc93dd6 84534aeb 601704de 353ea35d a8a87c07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
175f11d9 85baf711 105da703 8fc53dd6 da1b1ff3 883611de 3d3ea35d a8aa7e07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 6400 2
674e0ef8 85d6f711 1041a703 8fb93dd6 da371ff3 883611de 3d3ea35d a8aa7e07 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 6400 2
175f11d9 8598f711 105da703 8fc53dd6 cb21ada3 a03060ce 3d3ea35d a8887e07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
672e0ef8 85b4f711 1041a703 8fb93dd6 cb3dada3 a03060ce 3d3ea35d a8887e07 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
195f11d9 87b8f711 105da703 8fc53dd6 c728e9a3 9e3060ce 3d3ea35d aaa87e07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 9216 2
573b0f58 85aaf711 103da703 8fb53dd6 da3b1ff3 883611de 3d3ea35d a8aa7e07 6a96fb85 9428c259 41e433d3 f00ad3fb aa270c18 b16399ec 6400 2
06460f79 85d6f711 9061a703 0fc93dd6 59171ff3 093611de 3c3ea35d a8aa7e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 6400 2
07660f79 85b6f711 9061a703 0fc93dd6 48179ff3 083611de 3d3ea35d a88a7e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 10496 2
37630fd9 85baf711 905da703 0fc53dd6 5a1b1ff3 083611de 3d3ea35d a8aa7e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 6400 2
474a10f8 85d6f711 9041a703 0fb93dd6 5a371ff3 083611de 3d3ea35d a8aa7e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c18 b16399ec 6400 2
29421979 87d6f711 1061a703 8fc93dd6 d61ed833 863611de 3d3eab5d aaaa7e07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 2048 2
26621179 85b6f711 1061a703 8fc93dd6 c7179ff3 893611de 3c3ea35d a88a7e07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 10496 2
28421179 87d6f711 1061a703 8fc93dd6 d51edff3 873611de 3c3ea35d aaaa7e07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 3200 2
1f420f79 85d6f511 1061a703 8fc93dd6 a2161feb 883613de 353ea35d a8aa7c07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 12032 2
664e0ef8 85d6f711 1041a703 8fb93dd6 d9371ff3 893611de 3c3ea35d a8aa7e07 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 6400 2
175f11d9 859af711 105da703 8fc53dd6 c81b9ff3 883611de 3d3ea35d a88a7e07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 10496 2
672e0ef8 85b6f711 1041a703 8fb93dd6 c8379ff3 883611de 3d3ea35d a88a7e07 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 10496 2
195f11d9 87baf711 105da703 8fc53dd6 d622dff3 863611de 3d3ea35d aaaa7e07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 3200 2
573b0f58 8588f711 103da703 8fb53dd6 cb41ada3 a03060ce 3d3ea35d a8887e07 6a96fb85 9428c259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
06660f79 85b4f711 9061a703 0fc93dd6 4a1dada3 213060ce 3c3ea35d a8887e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
37630fd9 8598f711 905da703 0fc53dd6 4b21ada3 203060ce 3d3ea35d a8887e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
472a10f8 85b4f711 9041a703 0fb93dd6 4b3dada3 203060ce 3d3ea35d a8887e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
29621979 87b4f711 1061a703 8fc93dd6 b72565a3 9e3060ce 3d3eab5d aa887e07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 8448 2
28621179 87b4f711 1061a703 8fc93dd6 b6256da3 9f3060ce 3c3ea35d aa887e07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 9216 2
1f620f79 85b4f511 1061a703 8fc93dd6 7473ceeb 601704de 353ea35d a8887c07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
662e0ef8 85b4f711 1041a703 8fb93dd6 ca3dada3 a13060ce 3c3ea35d a8887e07 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
195f11d9 8798f711 105da703 8fc53dd6 b7296da3 9e3060ce 3d3ea35d aa887e07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 9216 2
573b0f58 8589f711 103da703 8fb53dd6 cac1a9a3 a03060ce 3d3ea35d a8897e07 6a96fb85 9428c259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
29621979 87b5f711 1061a703 8fc93dd6 b6a561a3 9e3060ce 3d3eab5d aa897e07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 6656 2
1f620f79 85b5f511 1061a703 8fc93dd6 73f4cb2b 601704de 353ea35d a8897c07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
175f11d9 859bf711 105da703 8fc53dd6 c79b9c73 883611de 3d3ea35d a88b7e07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 6912 2
195f11d9 8799f711 105da703 8fc53dd6 b6a969a3 9e3060ce 3d3ea35d aa897e07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 9216 2
195f17d9 87b9f811 105da703 8fc53dd6 87e18c30 5e1701dc 3d3ea35d aaa97f07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 7168 2
195f0fd9 87b9f511 105da703 8fc53dd6 86a7eda4 9e3062d0 3d3ea35d aaa97c07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 2048 2
195f11d9 87bbf711 105da703 8fc53dd6 cf2b5f73 863611de 3d3ea35d aaab7e07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 5504 2
0f5f0fd9 85b9f511 105da703 8fc53dd6 83d84f2b 601704de 353ea35d a8a97c07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
573b0f58 85abf711 103da703 8fb53dd6 d3439f73 883611de 3d3ea35d a8ab7e07 6a96fb85 9428c259 41e433d3 f00ad3fb aa270c18 b16399ec 11008 2
593b0f58 87a9f711 103da703 8fb53dd6 c6c8eda3 9e3060ce 3d3ea35d aaa97e07 6a96fb85 9428c259 41e433d3 f00ad3fb aa270c18 b16399ec 9216 2
563b1758 85a9f711 103da703 8fb53dd6 d9c125a3 a13060ce 3c3eab5d a8a97e07 6a96fb85 9428c259 41e433d3 f00ad3fb aa270c18 b16399ec 17408 2
593b0d58 87a9f511 103da703 8fb53dd6 86c7eda4 9e3062d0 3d3ea35d aaa97c07 6a96fb85 9428c259 41e433d3 f00ad3fb aa270c18 b16399ec 2048 2
593b0f58 87a8f711 103da703 8fb53dd6 c748e9a3 9e3060ce 3d3ea35d aaa87e07 6a96fb85 9428c259 41e433d3 f00ad3fb aa270c18 b16399ec 9216 2
573b0f58 858bf711 103da703 8fb53dd6 c7bb9c73 883611de 3d3ea35d a88b7e07 6a96fb85 9428c259 41e433d3 f00ad3fb aa270c18 b16399ec 6912 2
593b0f58 87abf711 103da703 8fb53dd6 cf4b5f73 863611de 3d3ea35d aaab7e07 6a96fb85 9428c259 41e433d3 f00ad3fb aa270c18 b16399ec 5504 2
593b0f58 8789f711 103da703 8fb53dd6 b6c969a3 9e3060ce 3d3ea35d aa897e07 6a96fb85 9428c259 41e433d3 f00ad3fb aa270c18 b16399ec 9216 2
77371158 85a8f711 903da703 0fb53dd6 5b4129a3 203060ce 3d3ea35d a8a87e07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
77371158 85abf711 903da703 0fb53dd6 53439f73 083611de 3d3ea35d a8ab7e07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c18 b16399ec 11008 2
77371158 8589f711 903da703 0fb53dd6 4ac1a9a3 203060ce 3d3ea35d a8897e07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
79371158 87a9f711 903da703 0fb53dd6 46c8eda3 1e3060ce 3d3ea35d aaa97e07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c18 b16399ec 9216 2
573b1d58 85a9f811 103da703 8fb53dd6 b44a1fa7 a0305fd2 3d3eab5d a8a97f07 6a96fb85 9428c259 41e433d3 f00ad3fb aa270c18 b16399ec 1280 2
583b0f58 87a9f711 103da703 8fb53dd6 c5c8eda3 9f3060ce 3c3ea35d aaa97e07 6a96fb85 9428c259 41e433d3 f00ad3fb aa270c18 b16399ec 9216 2
4f3b0d58 85a9f511 103da703 8fb53dd6 83f84f2b 601704de 353ea35d a8a97c07 6a96fb85 9428c259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
694e16f8 87d5f711 1041a703 8fb93dd6 c6c4e5a3 9e3060ce 3d3eab5d aaa97e07 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 8704 2
5f4e0cf8 85d5f511 1041a703 8fb93dd6 83f44f2b 601704de 353ea35d a8a97c07 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
0475d977 85963711 9021e703 0f895dd6 7adb0d23 217040ce 3c3ea35d a8a97e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa273c18 b16399ec 12288 2
08461579 87d5f811 9061a703 0fc93dd6 06dd8c30 df1701dc 3c3ea35d aaa97f07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 7168 2
08460d79 87d5f511 9061a703 0fc93dd6 05a3eda4 1f3062d0 3c3ea35d aaa97c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 2048 2
08460f79 87d4f711 9061a703 0fc93dd6 4624e9a3 1f3060ce 3c3ea35d aaa87e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 9216 2
08660f79 87b5f711 9061a703 0fc93dd6 35a569a3 1f3060ce 3c3ea35d aa897e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 9216 2
fe460d79 85d5f511 9061a703 0fc93dd6 02d44f2b e11704de 343ea35d a8a97c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
366317d9 85b9f711 905da703 0fc53dd6 59a125a3 213060ce 3c3eab5d a8a97e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 17408 2
464a10f8 85d4f711 9041a703 0fb93dd6 5a3d29a3 213060ce 3c3ea35d a8a87e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
462a10f8 85b5f711 9041a703 0fb93dd6 49bda9a3 213060ce 3c3ea35d a8897e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
38630fd9 87b9f711 905da703 0fc53dd6 45a8eda3 1f3060ce 3c3ea35d aaa97e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 9216 2
484a10f8 87d5f711 9041a703 0fb93dd6 45c4eda3 1f3060ce 3c3ea35d aaa97e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c18 b16399ec 9216 2
0575d977 85953711 9021e703 0f895dd6 7c5b0923 207040ce 3d3ea35d a8a87e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa273c18 b16399ec 12288 2
09461779 87d4f711 9061a703 0fc93dd6 4724e1a3 1e3060ce 3d3eab5d aaa87e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 6400 2
ff460d79 85d4f511 9061a703 0fc93dd6 04534aeb e01704de 353ea35d a8a87c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
39630fd9 87b8f711 905da703 0fc53dd6 4728e9a3 1e3060ce 3d3ea35d aaa87e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 9216 2
0515d977 85763711 9021e703 0f895dd6 6bdb8923 207040ce 3d3ea35d a8897e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa273c18 b16399ec 12288 2
09661779 87b5f711 9061a703 0fc93dd6 36a561a3 1e3060ce 3d3eab5d aa897e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 6656 2
ff660d79 85b5f511 9061a703 0fc93dd6 f3f4cb2b e01704de 353ea35d a8897c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
37630fd9 859bf711 905da703 0fc53dd6 479b9c73 083611de 3d3ea35d a88b7e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 6912 2
39630fd9 8799f711 905da703 0fc53dd6 36a969a3 1e3060ce 3d3ea35d aa897e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 9216 2
3512d9d7 857a3711 901de703 0f855dd6 7bdf0d23 207040ce 3d3ea35d a8a97e07 6a96fb85 9438c259 41e033d3 f00ad3fb aa270c18 b16399ec 12288 2
396315d9 87b9f811 905da703 0fc53dd6 07e18c30 de1701dc 3d3ea35d aaa97f07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 7168 2
39630dd9 87b9f511 905da703 0fc53dd6 06a7eda4 1e3062d0 3d3ea35d aaa97c07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 2048 2
39630fd9 87bbf711 905da703 0fc53dd6 4f2b5f73 063611de 3d3ea35d aaab7e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 5504 2
2f630dd9 85b9f511 905da703 0fc53dd6 03d84f2b e01704de 353ea35d a8a97c07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
494a18f8 87d5f711 9041a703 0fb93dd6 46c4e5a3 1e3060ce 3d3eab5d aaa97e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c18 b16399ec 8704 2
3f4a0ef8 85d5f511 9041a703 0fb93dd6 03f44f2b e01704de 353ea35d a8a97c07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
29421f79 87d5f811 1061a703 8fc93dd6 b029dfb0 a43410dc 3d3eab5d aaa97f07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 6912 2
29421f79 87d4f811 1061a703 8fc93dd6 b5215c70 a43410dc 3d3eab5d aaa87f07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 8704 2
29621f79 87b5f811 1061a703 8fc93dd6 a4a0dcb0 a43410dc 3d3eab5d aa897f07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 8960 2
29421779 87d5f511 1061a703 8fc93dd6 86a3e5a4 9e3062d0 3d3eab5d aaa97c07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 2048 2
29421779 87d4f511 1061a703 8fc93dd6 8723e1a4 9e3062d0 3d3eab5d aaa87c07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 2048 2
29621779 87b5f511 1061a703 8fc93dd6 76a461a4 9e3062d0 3d3eab5d aa897c07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 2048 2
09461d79 87d5f811 9061a703 0fc93dd6 3029dfb0 243410dc 3d3eab5d aaa97f07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 6912 2
09461579 87d5f511 9061a703 0fc93dd6 06a3e5a4 1e3062d0 3d3eab5d aaa97c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 2048 2
21421779 87d5f511 1061a703 8fc93dd6 98285fab 863413de 353eab5d aaa97c07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 9088 2
694e1cf8 87d5f811 1041a703 8fb93dd6 b049dfb0 a43410dc 3d3eab5d aaa97f07 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 6912 2
694e14f8 87d5f511 1041a703 8fb93dd6 86c3e5a4 9e3062d0 3d3eab5d aaa97c07 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 2048 2
694e16f8 87d4f711 1041a703 8fb93dd6 c744e1a3 9e3060ce 3d3eab5d aaa87e07 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 6400 2
692e16f8 87b5f711 1041a703 8fb93dd6 b6c561a3 9e3060ce 3d3eab5d aa897e07 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 6656 2
28421779 87d4f811 1061a703 8fc93dd6 875c87f0 5f1701dc 3c3ea35d aaa87f07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 7168 2
28420f79 87d4f511 1061a703 8fc93dd6 8623e9a4 9f3062d0 3c3ea35d aaa87c07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 2048 2
1e420f79 85d4f511 1061a703 8fc93dd6 83534aeb 611704de 343ea35d a8a87c07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
165f19d9 85b8f711 105da703 8fc53dd6 da2121a3 a13060ce 3c3eab5d a8a87e07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 12800 2
185f11d9 87b8f711 105da703 8fc53dd6 c628e9a3 9f3060ce 3c3ea35d aaa87e07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 9216 2
684e0ef8 87d4f711 1041a703 8fb93dd6 c644e9a3 9f3060ce 3c3ea35d aaa87e07 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 9216 2
28621779 87b5f811 1061a703 8fc93dd6 76fd0830 5f1701dc 3c3ea35d aa897f07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 7168 2
28620f79 87b5f511 1061a703 8fc93dd6 75a469a4 9f3062d0 3c3ea35d aa897c07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 2048 2
1e620f79 85b5f511 1061a703 8fc93dd6 72f4cb2b 611704de 343ea35d a8897c07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
165f19d9 8599f711 105da703 8fc53dd6 c9a1a1a3 a13060ce 3c3eab5d a8897e07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 13312 2
185f11d9 8799f711 105da703 8fc53dd6 b5a969a3 9f3060ce 3c3ea35d aa897e07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 9216 2
682e0ef8 87b5f711 1041a703 8fb93dd6 b5c569a3 9f3060ce 3c3ea35d aa897e07 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 9216 2
20420f79 87d5f511 1061a703 8fc93dd6 6edc0f2b 5f1704de 343ea35d aaa97c07 6a96fb85 943cc259 41e433d3 f00ad3fb aa270c18 b16399ec 9216 2
185f17d9 87b9f811 105da703 8fc53dd6 86e18c30 5f1701dc 3c3ea35d aaa97f07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 7168 2
684e14f8 87d5f811 1041a703 8fb93dd6 86fd8c30 5f1701dc 3c3ea35d aaa97f07 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 7168 2
185f0fd9 87b9f511 105da703 8fc53dd6 85a7eda4 9f3062d0 3c3ea35d aaa97c07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 2048 2
684e0cf8 87d5f511 1041a703 8fb93dd6 85c3eda4 9f3062d0 3c3ea35d aaa97c07 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 2048 2
185f11d9 87bbf711 105da703 8fc53dd6 ce2b5f73 873611de 3c3ea35d aaab7e07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 5504 2
5e4e0cf8 85d5f511 1041a703 8fb93dd6 82f44f2b 611704de 343ea35d a8a97c07 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
0f5f0fd9 85b8f511 105da703 8fc53dd6 84574aeb 601704de 353ea35d a8a87c07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
5f4e0cf8 85d4f511 1041a703 8fb93dd6 84734aeb 601704de 353ea35d a8a87c07 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
0f5f0fd9 85bbf511 105da703 8fc53dd6 9b229f6b 883613de 353ea35d a8ab7c07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 18176 2
0f5f0fd9 8599f511 105da703 8fc53dd6 73f8cb2b 601704de 353ea35d a8897c07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
5f2e0cf8 85b5f511 1041a703 8fb93dd6 7414cb2b 601704de 353ea35d a8897c07 6a96fb85 942cc259 41e433d3 f00ad3fb aa270c18 b16399ec 18432 2
115f0fd9 87b9f511 105da703 8fc53dd6 6fe00f2b 5e1704de 353ea35d aaa97c07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 9216 2
195f17d9 87b8f811 105da703 8fc53dd6 886087f0 5e1701dc 3d3ea35d aaa87f07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 7168 2
195f0fd9 87b8f511 105da703 8fc53dd6 8727e9a4 9e3062d0 3d3ea35d aaa87c07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 2048 2
165f19d9 85bbf711 105da703 8fc53dd6 d89b1c73 893611de 3c3eab5d a8ab7e07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 4096 2
195f17d9 87bbf811 105da703 8fc53dd6 af2bdf70 a43610dc 3d3ea35d aaab7f07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 4480 2
195f11d9 879bf711 105da703 8fc53dd6 c3a35c73 863611de 3d3ea35d aa8b7e07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 3456 2
195f17d9 8799f811 105da703 8fc53dd6 78010830 5e1701dc 3d3ea35d aa897f07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 7168 2
195f0fd9 8799f511 105da703 8fc53dd6 76a869a4 9e3062d0 3d3ea35d aa897c07 6a96fb85 9438c259 41e433d3 f00ad3fb aa270c18 b16399ec 2048 2
4859f23d 65c7f731 105a2703 8fd1bdd6 776adc2b a92411d6 3c3ea35d 88a97e27 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 4096 2
c858f83d 85c6f811 105a2703 8fd1bdd6 b53228e7 a6832392 3c3ea35d a8a87f07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 17408 2
c859f83d 85a7f811 105a2703 8fd1bdd6 a4d2a8e7 a6832392 3c3ea35d a8897f07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 17408 2
ca59f83d 87c7f811 105a2703 8fd1bdd6 b6baece7 a4832392 3c3ea35d aaa97f07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 19456 2
ca59f03d 87c7f511 105a2703 8fd1bdd6 96b96de4 a4832690 3c3ea35d aaa97c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 16896 2
c85ef23d 85c8f711 105a2703 8fd1bdd6 d431a1a3 a681248e 3c3ea35d a8aa7e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 18432 2
c858f23d 85a6f711 105a2703 8fd1bdd6 c5522de3 a683248e 3c3ea35d a8887e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 21504 2
ca58f23d 87c6f711 105a2703 8fd1bdd6 d73969e3 a483248e 3c3ea35d aaa87e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 10752 2
ca59f23d 87a7f711 105a2703 8fd1bdd6 c6dae9e3 a483248e 3c3ea35d aa897e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 10752 2
c059f03d 85c7f511 105a2703 8fd1bdd6 9cb1ade3 26832696 343ea35d a8a97c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 17920 2
c259f23d 87c7f711 105a2703 8fd1bdd6 deba6de4 24832498 343ea35d aaa97e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 4352 2
384ef99d 85dbf711 10662703 8fcdbdd6 d4a6a5e3 a683248e 3c3eab5d a8a97e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 20480 2
0855f7bd 85b7f811 105a2703 8fc1bdd6 b4b32ce7 a6832392 3c3ea35d a8a97f07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 17408 2
0854f1bd 85b6f711 105a2703 8fc1bdd6 d531a9e3 a683248e 3c3ea35d a8a87e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 21504 2
0855f1bd 8597f711 105a2703 8fc1bdd6 c4d329e3 a683248e 3c3ea35d a8897e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 21504 2
3a4ef19d 87dbf711 10662703 8fcdbdd6 d6ae6de3 a483248e 3c3ea35d aaa97e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 10752 2
0a55f1bd 87b7f711 105a2703 8fc1bdd6 d6ba6de3 a483248e 3c3ea35d aaa97e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 10752 2
4958f23d 65c6f731 105a2703 8fd1bdd6 77ead7eb a82411d6 3d3ea35d 88a87e27 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 4096 2
495ef23d 65c8f731 105a2703 8fd1bdd6 2eadada3 c581248e 3d3ea35d 88aa7e27 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 22528 2
4958f23d 65a6f731 105a2703 8fd1bdd6 67eb5beb a82411d6 3d3ea35d 88887e27 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 4096 2
4959f23d 65a7f731 105a2703 8fd1bdd6 686b582b a82411d6 3d3ea35d 88897e27 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 4096 2
b94ef19d 65dbf731 10662703 8fcdbdd6 785edc2b a82411d6 3d3ea35d 88a97e27 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 4096 2
f95aef1c 65dbf731 10462703 8fbdbdd6 787edc2b a82411d6 3d3ea35d 88a97e27 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c19 b16399ec 4096 2
8955f1bd 65b7f731 105a2703 8fc1bdd6 786adc2b a82411d6 3d3ea35d 88a97e27 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 4096 2
4b59fa3d 67c7f731 105a2703 8fd1bdd6 7472942b a62411d6 3d3eab5d 8aa97e27 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 2304 2
4858f23d 65c6f731 105a2703 8fd1bdd6 76ead7eb a92411d6 3c3ea35d 88a87e27 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 4096 2
4859f23d 65a7f731 105a2703 8fd1bdd6 676b582b a92411d6 3c3ea35d 88897e27 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 4096 2
4a59f23d 67c7f731 105a2703 8fd1bdd6 73729c2b a72411d6 3c3ea35d 8aa97e27 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 2048 2
4159f03d 65c7f531 105a2703 8fd1bdd6 4069dc23 a82413d6 353ea35d 88a97c27 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 4608 2
8855f1bd 65b7f731 105a2703 8fc1bdd6 776adc2b a92411d6 3c3ea35d 88a97e27 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 4096 2
b94df19d 65daf731 10662703 8fcdbdd6 77ded7eb a82411d6 3d3ea35d 88a87e27 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 4096 2
8954f1bd 65b6f731 105a2703 8fc1bdd6 77ead7eb a82411d6 3d3ea35d 88a87e27 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 4096 2
b94cf19d 65ddf731 10662703 8fcdbdd6 675cd4f3 b02758de 3d3ea35d 88ab7e27 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 13440 2
b96ef19d 65bbf731 10662703 8fcdbdd6 685f582b a82411d6 3d3ea35d 88897e27 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 4096 2
8955f1bd 6597f731 105a2703 8fc1bdd6 686b582b a82411d6 3d3ea35d 88897e27 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 4096 2
bb4ef19d 67dbf731 10662703 8fcdbdd6 74669c2b a62411d6 3d3ea35d 8aa97e27 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 2048 2
c95ef83d 85c8f811 105a2703 8fd1bdd6 b53220a7 a5812392 3d3ea35d a8aa7f07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 2336 2
c958f83d 85a6f811 105a2703 8fd1bdd6 a651ace7 a5832392 3d3ea35d a8887f07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 17408 2
cb5a003d 87c7f811 105a2703 8fd1bdd6 b0415fa8 a42410d4 3d3eab5d aaa97f07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 14464 2
c159f23d 85c7f611 105a2703 8fd1bdd6 7db22ee7 2583259a 353ea35d a8a97d07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 8704 2
394df79d 85daf811 10662703 8fcdbdd6 b62628e7 a5832392 3d3ea35d a8a87f07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 17408 2
0954f7bd 85b6f811 105a2703 8fc1bdd6 b63228e7 a5832392 3d3ea35d a8a87f07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 17408 2
394cf79d 85ddf811 10662703 8fcdbdd6 b4a724a7 a5812392 3d3ea35d a8ab7f07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 11584 2
396ef79d 85bbf811 10662703 8fcdbdd6 a5c6a8e7 a5832392 3d3ea35d a8897f07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 17408 2
0955f7bd 8597f811 105a2703 8fc1bdd6 a5d2a8e7 a5832392 3d3ea35d a8897f07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 17408 2
3b4ef79d 87dbf811 10662703 8fcdbdd6 b9aeece7 a3832392 3d3ea35d aaa97f07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 19456 2
c95ef83d 85a8f811 105a2703 8fd1bdd6 a551a4a7 a5812392 3d3ea35d a88a7f07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 11040 2
cb59003d 87c6f811 105a2703 8fd1bdd6 b538dca8 a42410d4 3d3eab5d aaa87f07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 5488 2
c85ef83d 85c8f811 105a2703 8fd1bdd6 b43220a7 a6812392 3c3ea35d a8aa7f07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 2336 2
c858f83d 85a6f811 105a2703 8fd1bdd6 a551ace7 a6832392 3c3ea35d a8887f07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 17408 2
ca58f83d 87c6f811 105a2703 8fd1bdd6 b739e8e7 a4832392 3c3ea35d aaa87f07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 19456 2
c158f23d 85c6f611 105a2703 8fd1bdd6 7e312aa7 2583259a 353ea35d a8a87d07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 8704 2
0854f7bd 85b6f811 105a2703 8fc1bdd6 b53228e7 a6832392 3c3ea35d a8a87f07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 17408 2
394bf79d 85dcf811 10662703 8fcdbdd6 b52620a7 a5812392 3d3ea35d a8aa7f07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 2336 2
095af7bd 85b8f811 105a2703 8fc1bdd6 b53220a7 a5812392 3d3ea35d a8aa7f07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 2336 2
396df79d 85baf811 10662703 8fcdbdd6 a645ace7 a5832392 3d3ea35d a8887f07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 17408 2
0954f7bd 8596f811 105a2703 8fc1bdd6 a651ace7 a5832392 3d3ea35d a8887f07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 17408 2
3b4df79d 87daf811 10662703 8fcdbdd6 ba2de8e7 a3832392 3d3ea35d aaa87f07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 19456 2
cb5a003d 87a7f811 105a2703 8fd1bdd6 a4b85ca8 a42410d4 3d3eab5d aa897f07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 5760 2
ca59f83d 87a7f811 105a2703 8fd1bdd6 a6da68e7 a4832392 3c3ea35d aa897f07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 19456 2
c159f23d 85a7f611 105a2703 8fd1bdd6 6dd1aae7 2583259a 353ea35d a8897d07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 8704 2
0855f7bd 8597f811 105a2703 8fc1bdd6 a4d2a8e7 a6832392 3c3ea35d a8897f07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 17408 2
396cf79d 85bdf811 10662703 8fcdbdd6 a4c6a0a7 a5812392 3d3ea35d a88b7f07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 2880 2
3b6ef79d 87bbf811 10662703 8fcdbdd6 a9ce68e7 a3832392 3d3ea35d aa897f07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 19456 2
c95ef23d 85a8f711 105a2703 8fd1bdd6 c55225a3 a581248e 3d3ea35d a88a7e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 27136 2
7959ef1c 85daf711 10462703 8fbdbdd6 d645a9e3 a583248e 3d3ea35d a8a87e07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c19 b16399ec 21504 2
cb58fa3d 87c6f711 105a2703 8fd1bdd6 da3961e3 a383248e 3d3eab5d aaa87e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 5888 2
c158f03d 85c6f511 105a2703 8fd1bdd6 9e30a9e3 25832696 353ea35d a8a87c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 17920 2
394bf19d 85dcf711 10662703 8fcdbdd6 d525a1a3 a581248e 3d3ea35d a8aa7e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 18432 2
095af1bd 85b8f711 105a2703 8fc1bdd6 d531a1a3 a581248e 3d3ea35d a8aa7e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 18432 2
396df19d 85baf711 10662703 8fcdbdd6 c6462de3 a583248e 3d3ea35d a8887e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 21504 2
0954f1bd 8596f711 105a2703 8fc1bdd6 c6522de3 a583248e 3d3ea35d a8887e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 21504 2
3b4df19d 87daf711 10662703 8fcdbdd6 da2d69e3 a383248e 3d3ea35d aaa87e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 10752 2
7957ef1c 85dcf711 10462703 8fbdbdd6 d545a1a3 a581248e 3d3ea35d a8aa7e07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c19 b16399ec 18432 2
cb5efa3d 87c8f711 105a2703 8fd1bdd6 d6355933 8e2758de 3d3eab5d aaaa7e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 6144 2
c85ef23d 85a8f711 105a2703 8fd1bdd6 c45225a3 a681248e 3c3ea35d a88a7e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 27136 2
ca5ef23d 87c8f711 105a2703 8fd1bdd6 d63961a3 a481248e 3c3ea35d aaaa7e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 9216 2
c15ef03d 85c8f511 105a2703 8fd1bdd6 922ca12b 902762de 353ea35d a8aa7c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 16384 2
085af1bd 85b8f711 105a2703 8fc1bdd6 d431a1a3 a681248e 3c3ea35d a8aa7e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 18432 2
396bf19d 85bcf711 10662703 8fcdbdd6 c54625a3 a581248e 3d3ea35d a88a7e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 27136 2
095af1bd 8598f711 105a2703 8fc1bdd6 c55225a3 a581248e 3d3ea35d a88a7e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 27136 2
3b4bf19d 87dcf711 10662703 8fcdbdd6 d92d61a3 a381248e 3d3ea35d aaaa7e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 9216 2
7939ef1c 85baf711 10462703 8fbdbdd6 c6662de3 a583248e 3d3ea35d a8887e07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c19 b16399ec 21504 2
cb58fa3d 87a6f711 105a2703 8fd1bdd6 ca59e5e3 a383248e 3d3eab5d aa887e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 10240 2
ca58f23d 87a6f711 105a2703 8fd1bdd6 c759ede3 a483248e 3c3ea35d aa887e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 10752 2
c158f03d 85a6f511 105a2703 8fd1bdd6 8e512de3 25832696 353ea35d a8887c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 17920 2
0854f1bd 8596f711 105a2703 8fc1bdd6 c5522de3 a683248e 3c3ea35d a8887e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 21504 2
3b6df19d 87baf711 10662703 8fcdbdd6 ca4dede3 a383248e 3d3ea35d aa887e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 10752 2
793aef1c 85bbf711 10462703 8fbdbdd6 c5e729e3 a583248e 3d3ea35d a8897e07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c19 b16399ec 21504 2
cb59fa3d 87a7f711 105a2703 8fd1bdd6 c9dae1e3 a383248e 3d3eab5d aa897e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 5888 2
c159f03d 85a7f511 105a2703 8fd1bdd6 8dd229e3 25832696 353ea35d a8897c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 17920 2
396cf19d 85bdf711 10662703 8fcdbdd6 c4c721a3 a581248e 3d3ea35d a88b7e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 18432 2
3b6ef19d 87bbf711 10662703 8fcdbdd6 c9cee9e3 a383248e 3d3ea35d aa897e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 10752 2
3b4eef9d 87dbf511 10662703 8fcdbdd6 99ad6de4 a3832690 3d3ea35d aaa97c07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 16896 2
3b4cf19d 87ddf711 10662703 8fcdbdd6 d8ae65a3 a381248e 3d3ea35d aaab7e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 13568 2
314eef9d 85dbf511 10662703 8fcdbdd6 9da5ade3 25832696 353ea35d a8a97c07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 17920 2
334ef19d 87dbf711 10662703 8fcdbdd6 e1ae6de4 23832498 353ea35d aaa97e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 4352 2
7958ef1c 85ddf711 10462703 8fbdbdd6 d4c6a5a3 a581248e 3d3ea35d a8ab7e07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c19 b16399ec 27136 2
7b5aef1c 87dbf711 10462703 8fbdbdd6 d9ce6de3 a383248e 3d3ea35d aaa97e07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c19 b16399ec 10752 2
785af71c 85dbf711 10462703 8fbdbdd6 d4c6a5e3 a683248e 3c3eab5d a8a97e07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c19 b16399ec 20480 2
7b5aed1c 87dbf511 10462703 8fbdbdd6 99cd6de4 a3832690 3d3ea35d aaa97c07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c19 b16399ec 16896 2
7b59ef1c 87daf711 10462703 8fbdbdd6 da4d69e3 a383248e 3d3ea35d aaa87e07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c19 b16399ec 10752 2
7938ef1c 85bdf711 10462703 8fbdbdd6 c4e721a3 a581248e 3d3ea35d a88b7e07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c19 b16399ec 18432 2
7b58ef1c 87ddf711 10462703 8fbdbdd6 d8ce65a3 a381248e 3d3ea35d aaab7e07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c19 b16399ec 13568 2
7b3aef1c 87bbf711 10462703 8fbdbdd6 c9eee9e3 a383248e 3d3ea35d aa897e07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c19 b16399ec 10752 2
795afd1c 85dbf811 10462703 8fbdbdd6 b5c724e7 a5832392 3d3eab5d a8a97f07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c19 b16399ec 12672 2
785af51c 85dbf811 10462703 8fbdbdd6 b4c72ce7 a6832392 3c3ea35d a8a97f07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c19 b16399ec 17408 2
7a5aef1c 87dbf711 10462703 8fbdbdd6 d6ce6de3 a483248e 3c3ea35d aaa97e07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c19 b16399ec 10752 2
715aed1c 85dbf511 10462703 8fbdbdd6 9dc5ade3 25832696 353ea35d a8a97c07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c19 b16399ec 17920 2
735aef1c 87dbf711 10462703 8fbdbdd6 e1ce6de4 23832498 353ea35d aaa97e07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c19 b16399ec 4352 2
0b55f9bd 87b7f711 105a2703 8fc1bdd6 d9ba65e3 a383248e 3d3eab5d aaa97e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 10240 2
0155efbd 85b7f511 105a2703 8fc1bdd6 9db1ade3 25832696 353ea35d a8a97c07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 17920 2
c359fa3d 87c7f711 105a2703 8fd1bdd6 e1ba65e4 23832498 353eab5d aaa97e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 4224 2
cb59f83d 87c7f511 105a2703 8fd1bdd6 99b965e4 a3832690 3d3eab5d aaa97c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 16896 2
cb58f83d 87c6f511 105a2703 8fd1bdd6 9a3861e4 a3832690 3d3eab5d aaa87c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 8448 2
cb59f83d 87a7f511 105a2703 8fd1bdd6 89d9e1e4 a3832690 3d3eab5d aa897c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 8448 2
c359f83d 87c7f511 105a2703 8fd1bdd6 983fdfa3 862413d6 353eab5d aaa97c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 8896 2
c358fa3d 87c6f711 105a2703 8fd1bdd6 e23961e4 23832498 353eab5d aaa87e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 2048 2
c359fa3d 87a7f711 105a2703 8fd1bdd6 d1dae1e4 23832498 353eab5d aa897e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 2048 2
0355f9bd 87b7f711 105a2703 8fc1bdd6 e1ba65e4 23832498 353eab5d aaa97e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 4224 2
0b55ffbd 87b7f811 105a2703 8fc1bdd6 b0415fa8 a42410d4 3d3eab5d aaa97f07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 14464 2
0b55f7bd 87b7f511 105a2703 8fc1bdd6 99b965e4 a3832690 3d3eab5d aaa97c07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 16896 2
0b54f9bd 87b6f711 105a2703 8fc1bdd6 da3961e3 a383248e 3d3eab5d aaa87e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 5888 2
0b55f9bd 8797f711 105a2703 8fc1bdd6 c9dae1e3 a383248e 3d3eab5d aa897e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 5888 2
c059f23d 85c7f611 105a2703 8fd1bdd6 7cb22ee7 2683259a 343ea35d a8a97d07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 8704 2
384eff9d 85dbf811 10662703 8fcdbdd6 b4a724e7 a6832392 3c3eab5d a8a97f07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 12672 2
3a4ef79d 87dbf811 10662703 8fcdbdd6 b6aeece7 a4832392 3c3ea35d aaa97f07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 19456 2
0a55f7bd 87b7f811 105a2703 8fc1bdd6 b6baece7 a4832392 3c3ea35d aaa97f07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 19456 2
ca58f03d 87c6f511 105a2703 8fd1bdd6 973869e4 a4832690 3c3ea35d aaa87c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 16896 2
c058f03d 85c6f511 105a2703 8fd1bdd6 9d30a9e3 26832696 343ea35d a8a87c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 17920 2
c258f23d 87c6f711 105a2703 8fd1bdd6 df3969e4 24832498 343ea35d aaa87e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 4352 2
384df99d 85daf711 10662703 8fcdbdd6 d525a1e3 a683248e 3c3eab5d a8a87e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 11776 2
3a4df19d 87daf711 10662703 8fcdbdd6 d72d69e3 a483248e 3c3ea35d aaa87e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 10752 2
0a54f1bd 87b6f711 105a2703 8fc1bdd6 d73969e3 a483248e 3c3ea35d aaa87e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 10752 2
ca59f03d 87a7f511 105a2703 8fd1bdd6 86d9e9e4 a4832690 3c3ea35d aa897c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 16896 2
c059f03d 85a7f511 105a2703 8fd1bdd6 8cd229e3 26832696 343ea35d a8897c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 17920 2
c259f23d 87a7f711 105a2703 8fd1bdd6 cedae9e4 24832498 343ea35d aa897e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 4352 2
386ef99d 85bbf711 10662703 8fcdbdd6 c4c721e3 a683248e 3c3eab5d a8897e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 11776 2
3a6ef19d 87bbf711 10662703 8fcdbdd6 c6cee9e3 a483248e 3c3ea35d aa897e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 10752 2
0a55f1bd 8797f711 105a2703 8fc1bdd6 c6dae9e3 a483248e 3c3ea35d aa897e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 10752 2
c259f03d 87c7f511 105a2703 8fd1bdd6 9eb96de3 24832696 343ea35d aaa97c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c19 b16399ec 8960 2
324ef19d 87dbf711 10662703 8fcdbdd6 deae6de4 24832498 343ea35d aaa97e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 4352 2
0255f1bd 87b7f711 105a2703 8fc1bdd6 deba6de4 24832498 343ea35d aaa97e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 4352 2
3a4eef9d 87dbf511 10662703 8fcdbdd6 96ad6de4 a4832690 3c3ea35d aaa97c07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 16896 2
0a55efbd 87b7f511 105a2703 8fc1bdd6 96b96de4 a4832690 3c3ea35d aaa97c07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 16896 2
3a4cf19d 87ddf711 10662703 8fcdbdd6 d5ae65a3 a481248e 3c3ea35d aaab7e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 13568 2
0055efbd 85b7f511 105a2703 8fc1bdd6 9cb1ade3 26832696 343ea35d a8a97c07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 17920 2
314ef19d 85dbf611 10662703 8fcdbdd6 7da62ee7 2583259a 353ea35d a8a97d07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 8704 2
0155f1bd 85b7f611 105a2703 8fc1bdd6 7db22ee7 2583259a 353ea35d a8a97d07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 8704 2
314def9d 85daf511 10662703 8fcdbdd6 9e24a9e3 25832696 353ea35d a8a87c07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 17920 2
0154efbd 85b6f511 105a2703 8fc1bdd6 9e30a9e3 25832696 353ea35d a8a87c07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 17920 2
314cef9d 85ddf511 10662703 8fcdbdd6 91a1a56b 902762de 353ea35d a8ab7c07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 22784 2
316eef9d 85bbf511 10662703 8fcdbdd6 8dc629e3 25832696 353ea35d a8897c07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 17920 2
0155efbd 8597f511 105a2703 8fc1bdd6 8dd229e3 25832696 353ea35d a8897c07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c19 b16399ec 17920 2
334eef9d 87dbf511 10662703 8fcdbdd6 a1ad6de3 23832696 353ea35d aaa97c07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 8960 2
3b4cf79d 87ddf811 10662703 8fcdbdd6 af335f68 a42610d4 3d3ea35d aaab7f07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 16064 2
3b4def9d 87daf511 10662703 8fcdbdd6 9a2c69e4 a3832690 3d3ea35d aaa87c07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 16896 2
334df19d 87daf711 10662703 8fcdbdd6 e22d69e4 23832498 353ea35d aaa87e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 4352 2
384cf99d 85ddf711 10662703 8fcdbdd6 c8a29d73 912758de 3c3eab5d a8ab7e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 12288 2
3b4cef9d 87ddf511 10662703 8fcdbdd6 98ad65a4 a3812690 3d3ea35d aaab7c07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 16896 2
3b6cf19d 87bdf711 10662703 8fcdbdd6 c8cee1a3 a381248e 3d3ea35d aa8b7e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 9216 2
334cf19d 87ddf711 10662703 8fcdbdd6 e0ae65a4 23812498 353ea35d aaab7e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 3968 2
3b6eef9d 87bbf511 10662703 8fcdbdd6 89cde9e4 a3832690 3d3ea35d aa897c07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 16896 2
336ef19d 87bbf711 10662703 8fcdbdd6 d1cee9e4 23832498 353ea35d aa897e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c19 b16399ec 4352 2
8575d977 65963731 9021e703 0f895dd6 b718fda3 407038ce 3d3ea35d 88a97e27 6a96fb85 943cc259 41f433d3 f00ad3fb aa273c18 b16399ec 12288 2
0515d977 85753711 9021e703 0f895dd6 6c5b8d23 207040ce 3d3ea35d a8887e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa273c18 b16399ec 12288 2
0775e177 87963711 9021e703 0f895dd6 67e2c523 1e7040ce 3d3eab5d aaa97e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa273c18 b16399ec 6656 2
0475d977 85953711 9021e703 0f895dd6 7b5b0923 217040ce 3c3ea35d a8a87e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa273c18 b16399ec 12288 2
0415d977 85763711 9021e703 0f895dd6 6adb8923 217040ce 3c3ea35d a8897e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa273c18 b16399ec 12288 2
0675d977 87963711 9021e703 0f895dd6 66e2cd23 1f7040ce 3c3ea35d aaa97e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa273c18 b16399ec 6144 2
fd75d777 85963511 9021e703 0f895dd6 22ebeca3 88806fd6 353ea35d a8a97c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa273c18 b16399ec 2048 2
3512d9d7 85793711 901de703 0f855dd6 7c5f0923 207040ce 3d3ea35d a8a87e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa273c18 b16399ec 12288 2
3512d9d7 855a3711 901de703 0f855dd6 6bdf8923 207040ce 3d3ea35d a8897e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa273c18 b16399ec 12288 2
3712d9d7 877a3711 901de703 0f855dd6 67e6cd23 1e7040ce 3d3ea35d aaa97e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa273c18 b16399ec 6144 2
87461579 65d4f831 9061a703 0fc93dd6 b7d7d7e7 40305fd2 3d3ea35d 88a87f27 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 8192 2
87661579 65b5f831 9061a703 0fc93dd6 a8575827 40305fd2 3d3ea35d 88897f27 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 8192 2
87460f79 65d6f731 9061a703 0fc93dd6 efd15033 2736115e 3d3ea35d 88aa7e27 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 9472 2
87660f79 65b4f731 9061a703 0fc93dd6 c7d7dd23 403058ce 3d3ea35d 88887e27 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 10240 2
f7371158 65a9f731 903da703 0fb53dd6 d87b5d23 403058ce 3d3ea35d 88a97e27 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c18 b16399ec 10240 2
89461779 67d5f731 9061a703 0fc93dd6 e45f1523 3e3058ce 3d3eab5d 8aa97e27 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 5184 2
86461579 65d5f831 9061a703 0fc93dd6 b757dc27 41305fd2 3c3ea35d 88a97f27 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 8192 2
86460f79 65d4f731 9061a703 0fc93dd6 d6d75923 413058ce 3c3ea35d 88a87e27 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 10240 2
86660f79 65b5f731 9061a703 0fc93dd6 c757d923 413058ce 3c3ea35d 88897e27 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 10240 2
88460f79 67d5f731 9061a703 0fc93dd6 e35f1d23 3f3058ce 3c3ea35d 8aa97e27 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 5120 2
7f460d79 65d5f531 9061a703 0fc93dd6 c0525c2b 283413de 353ea35d 88a97c27 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 7680 2
c64a10f8 65d5f731 9041a703 0fb93dd6 d7775d23 413058ce 3c3ea35d 88a97e27 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c18 b16399ec 10240 2
b76315d9 65b9f831 905da703 0fc53dd6 b85bdc27 40305fd2 3d3ea35d 88a97f27 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 8192 2
b7630fd9 65b8f731 905da703 0fc53dd6 d7db5923 403058ce 3d3ea35d 88a87e27 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 10240 2
c74a10f8 65d4f731 9041a703 0fb93dd6 d7f75923 403058ce 3d3ea35d 88a87e27 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c18 b16399ec 10240 2
b7630fd9 65bbf731 905da703 0fc53dd6 f75553f3 283611de 3d3ea35d 88ab7e27 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 4864 2
b7630fd9 6599f731 905da703 0fc53dd6 c85bd923 403058ce 3d3ea35d 88897e27 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 10240 2
c72a10f8 65b5f731 9041a703 0fb93dd6 c877d923 403058ce 3d3ea35d 88897e27 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c18 b16399ec 10240 2
b9630fd9 67b9f731 905da703 0fc53dd6 e4631d23 3e3058ce 3d3ea35d 8aa97e27 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 5120 2
77371158 85aaf711 903da703 0fb53dd6 5a3b1ff3 083611de 3d3ea35d a8aa7e07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c18 b16399ec 6400 2
09461779 87d6f711 9061a703 0fc93dd6 561ed833 063611de 3d3eab5d aaaa7e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 2048 2
06660f79 85b6f711 9061a703 0fc93dd6 47179ff3 093611de 3c3ea35d a88a7e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 10496 2
08460f79 87d6f711 9061a703 0fc93dd6 551edff3 073611de 3c3ea35d aaaa7e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 3200 2
ff460d79 85d6f511 9061a703 0fc93dd6 22161feb 083613de 353ea35d a8aa7c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 12032 2
464a10f8 85d6f711 9041a703 0fb93dd6 59371ff3 093611de 3c3ea35d a8aa7e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c18 b16399ec 6400 2
37630fd9 859af711 905da703 0fc53dd6 481b9ff3 083611de 3d3ea35d a88a7e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 10496 2
472a10f8 85b6f711 9041a703 0fb93dd6 48379ff3 083611de 3d3ea35d a88a7e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c18 b16399ec 10496 2
39630fd9 87baf711 905da703 0fc53dd6 5622dff3 063611de 3d3ea35d aaaa7e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 3200 2
77371158 8588f711 903da703 0fb53dd6 4b41ada3 203060ce 3d3ea35d a8887e07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
09661779 87b4f711 9061a703 0fc93dd6 372565a3 1e3060ce 3d3eab5d aa887e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 8448 2
08660f79 87b4f711 9061a703 0fc93dd6 36256da3 1f3060ce 3c3ea35d aa887e07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 9216 2
ff660d79 85b4f511 9061a703 0fc93dd6 f473ceeb e01704de 353ea35d a8887c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
462a10f8 85b4f711 9041a703 0fb93dd6 4a3dada3 213060ce 3c3ea35d a8887e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
39630fd9 8798f711 905da703 0fc53dd6 37296da3 1e3060ce 3d3ea35d aa887e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 9216 2
76371958 85a9f711 903da703 0fb53dd6 59c125a3 213060ce 3c3eab5d a8a97e07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c18 b16399ec 17408 2
79370f58 87a9f511 903da703 0fb53dd6 06c7eda4 1e3062d0 3d3ea35d aaa97c07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c18 b16399ec 2048 2
79371158 87a8f711 903da703 0fb53dd6 4748e9a3 1e3060ce 3d3ea35d aaa87e07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c18 b16399ec 9216 2
77371158 858bf711 903da703 0fb53dd6 47bb9c73 083611de 3d3ea35d a88b7e07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c18 b16399ec 6912 2
79371158 87abf711 903da703 0fb53dd6 4f4b5f73 063611de 3d3ea35d aaab7e07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c18 b16399ec 5504 2
79371158 8789f711 903da703 0fb53dd6 36c969a3 1e3060ce 3d3ea35d aa897e07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c18 b16399ec 9216 2
77371f58 85a9f811 903da703 0fb53dd6 344a1fa7 20305fd2 3d3eab5d a8a97f07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c18 b16399ec 1280 2
78371158 87a9f711 903da703 0fb53dd6 45c8eda3 1f3060ce 3c3ea35d aaa97e07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c18 b16399ec 9216 2
6f370f58 85a9f511 903da703 0fb53dd6 03f84f2b e01704de 353ea35d a8a97c07 6a96fb85 9428c259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
09461d79 87d4f811 9061a703 0fc93dd6 35215c70 243410dc 3d3eab5d aaa87f07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 8704 2
09661d79 87b5f811 9061a703 0fc93dd6 24a0dcb0 243410dc 3d3eab5d aa897f07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 8960 2
09461579 87d4f511 9061a703 0fc93dd6 0723e1a4 1e3062d0 3d3eab5d aaa87c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 2048 2
09661579 87b5f511 9061a703 0fc93dd6 f6a461a4 1e3062d0 3d3eab5d aa897c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 2048 2
01461579 87d5f511 9061a703 0fc93dd6 18285fab 063413de 353eab5d aaa97c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 9088 2
494a1ef8 87d5f811 9041a703 0fb93dd6 3049dfb0 243410dc 3d3eab5d aaa97f07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c18 b16399ec 6912 2
494a16f8 87d5f511 9041a703 0fb93dd6 06c3e5a4 1e3062d0 3d3eab5d aaa97c07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c18 b16399ec 2048 2
494a18f8 87d4f711 9041a703 0fb93dd6 4744e1a3 1e3060ce 3d3eab5d aaa87e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c18 b16399ec 6400 2
492a18f8 87b5f711 9041a703 0fb93dd6 36c561a3 1e3060ce 3d3eab5d aa897e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c18 b16399ec 6656 2
08461579 87d4f811 9061a703 0fc93dd6 075c87f0 df1701dc 3c3ea35d aaa87f07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 7168 2
08460d79 87d4f511 9061a703 0fc93dd6 0623e9a4 1f3062d0 3c3ea35d aaa87c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 2048 2
fe460d79 85d4f511 9061a703 0fc93dd6 03534aeb e11704de 343ea35d a8a87c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
366317d9 85b8f711 905da703 0fc53dd6 5a2121a3 213060ce 3c3eab5d a8a87e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 12800 2
38630fd9 87b8f711 905da703 0fc53dd6 4628e9a3 1f3060ce 3c3ea35d aaa87e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 9216 2
484a10f8 87d4f711 9041a703 0fb93dd6 4644e9a3 1f3060ce 3c3ea35d aaa87e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c18 b16399ec 9216 2
08661579 87b5f811 9061a703 0fc93dd6 f6fd0830 df1701dc 3c3ea35d aa897f07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 7168 2
08660d79 87b5f511 9061a703 0fc93dd6 f5a469a4 1f3062d0 3c3ea35d aa897c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 2048 2
fe660d79 85b5f511 9061a703 0fc93dd6 f2f4cb2b e11704de 343ea35d a8897c07 6a96fb85 943cc259 41f433d3 f00ad3fb aa270c18 b16399ec 18432 2
366317d9 8599f711 905da703 0fc53dd6 49a1a1a3 213060ce 3c3eab5d a8897e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 13312 2
38630fd9 8799f711 905da703 0fc53dd6 35a969a3 1f3060ce 3c3ea35d aa897e07 6a96fb85 9438c259 41f433d3 f00ad3fb aa270c18 b16399ec 9216 2
482a10f8 87b5f711 9041a703 0fb93dd6 35c569a3 1f3060ce 3c3ea35d aa897e07 6a96fb85 942cc259 41f433d3 f00ad3fb aa270c18 b16399ec 9216 2
```

m.cvc (model M as solved; SHA-256 b91308037057271b395195936d03d681f08cb1185f8d622305d65167eb783bee):

```
A1 : BITVECTOR(32);
A2 : BITVECTOR(32);
A3 : BITVECTOR(32);
A4 : BITVECTOR(32);
E3 : BITVECTOR(32);
E4 : BITVECTOR(32);
E5 : BITVECTOR(32);
E6 : BITVECTOR(32);
E7 : BITVECTOR(32);
E8 : BITVECTOR(32);
E9 : BITVECTOR(32);
E10 : BITVECTOR(32);
E11 : BITVECTOR(32);
E12 : BITVECTOR(32);
A5 : BITVECTOR(32);
A6 : BITVECTOR(32);
A7 : BITVECTOR(32);
A8 : BITVECTOR(32);
A9 : BITVECTOR(32);
A10 : BITVECTOR(32);
A11 : BITVECTOR(32);
A12 : BITVECTOR(32);
Ep5 : BITVECTOR(32);
Ep6 : BITVECTOR(32);
Ep7 : BITVECTOR(32);
Ep8 : BITVECTOR(32);
Ap5 : BITVECTOR(32);
Ap6 : BITVECTOR(32);
Ap7 : BITVECTOR(32);
Ap8 : BITVECTOR(32);
W7 : BITVECTOR(32);
W8 : BITVECTOR(32);
W9 : BITVECTOR(32);
W10 : BITVECTOR(32);
W11 : BITVECTOR(32);
W12 : BITVECTOR(32);
Ep9 : BITVECTOR(32);
Ap9 : BITVECTOR(32);
Ep10 : BITVECTOR(32);
Ap10 : BITVECTOR(32);
Ep11 : BITVECTOR(32);
Ap11 : BITVECTOR(32);
Ep12 : BITVECTOR(32);
Ap12 : BITVECTOR(32);
ASSERT(A5 = BVPLUS(32, BVSUB(32, E5, A1), BVXOR(BVXOR((A4[1:0] @ A4[31:2]), (A4[12:0] @ A4[31:13])), (A4[21:0] @ A4[31:22])), ((A4 & A3) | (A4 & A2) | (A3 & A2))));
ASSERT(A6 = BVPLUS(32, BVSUB(32, E6, A2), BVXOR(BVXOR((A5[1:0] @ A5[31:2]), (A5[12:0] @ A5[31:13])), (A5[21:0] @ A5[31:22])), ((A5 & A4) | (A5 & A3) | (A4 & A3))));
ASSERT(A7 = BVPLUS(32, BVSUB(32, E7, A3), BVXOR(BVXOR((A6[1:0] @ A6[31:2]), (A6[12:0] @ A6[31:13])), (A6[21:0] @ A6[31:22])), ((A6 & A5) | (A6 & A4) | (A5 & A4))));
ASSERT(A8 = BVPLUS(32, BVSUB(32, E8, A4), BVXOR(BVXOR((A7[1:0] @ A7[31:2]), (A7[12:0] @ A7[31:13])), (A7[21:0] @ A7[31:22])), ((A7 & A6) | (A7 & A5) | (A6 & A5))));
ASSERT(A9 = BVPLUS(32, BVSUB(32, E9, A5), BVXOR(BVXOR((A8[1:0] @ A8[31:2]), (A8[12:0] @ A8[31:13])), (A8[21:0] @ A8[31:22])), ((A8 & A7) | (A8 & A6) | (A7 & A6))));
ASSERT(A10 = BVPLUS(32, BVSUB(32, E10, A6), BVXOR(BVXOR((A9[1:0] @ A9[31:2]), (A9[12:0] @ A9[31:13])), (A9[21:0] @ A9[31:22])), ((A9 & A8) | (A9 & A7) | (A8 & A7))));
ASSERT(A11 = BVPLUS(32, BVSUB(32, E11, A7), BVXOR(BVXOR((A10[1:0] @ A10[31:2]), (A10[12:0] @ A10[31:13])), (A10[21:0] @ A10[31:22])), ((A10 & A9) | (A10 & A8) | (A9 & A8))));
ASSERT(A12 = BVPLUS(32, BVSUB(32, E12, A8), BVXOR(BVXOR((A11[1:0] @ A11[31:2]), (A11[12:0] @ A11[31:13])), (A11[21:0] @ A11[31:22])), ((A11 & A10) | (A11 & A9) | (A10 & A9))));
ASSERT(Ep5 = BVPLUS(32, E5, 0hexfffff006));
ASSERT(Ep6 = BVPLUS(32, E6, BVSUB(32, BVXOR(BVXOR((Ep5[5:0] @ Ep5[31:6]), (Ep5[10:0] @ Ep5[31:11])), (Ep5[24:0] @ Ep5[31:25])), BVXOR(BVXOR((E5[5:0] @ E5[31:6]), (E5[10:0] @ E5[31:11])), (E5[24:0] @ E5[31:25]))), BVSUB(32, ((Ep5 & E4) | (~Ep5 & E3)), ((E5 & E4) | (~E5 & E3))), 0hex002087f1));
ASSERT(Ep7 = BVPLUS(32, E7, BVSUB(32, BVXOR(BVXOR((Ep6[5:0] @ Ep6[31:6]), (Ep6[10:0] @ Ep6[31:11])), (Ep6[24:0] @ Ep6[31:25])), BVXOR(BVXOR((E6[5:0] @ E6[31:6]), (E6[10:0] @ E6[31:11])), (E6[24:0] @ E6[31:25]))), BVSUB(32, ((Ep6 & Ep5) | (~Ep6 & E4)), ((E6 & E5) | (~E6 & E4))), 0hex4fefb5fa));
ASSERT(Ep8 = BVPLUS(32, E8, BVSUB(32, BVXOR(BVXOR((Ep7[5:0] @ Ep7[31:6]), (Ep7[10:0] @ Ep7[31:11])), (Ep7[24:0] @ Ep7[31:25])), BVXOR(BVXOR((E7[5:0] @ E7[31:6]), (E7[10:0] @ E7[31:11])), (E7[24:0] @ E7[31:25]))), BVSUB(32, ((Ep7 & Ep6) | (~Ep7 & Ep5)), ((E7 & E6) | (~E7 & E5))), 0hex28011100));
ASSERT(Ap5 = BVPLUS(32, BVSUB(32, Ep5, A1), BVXOR(BVXOR((A4[1:0] @ A4[31:2]), (A4[12:0] @ A4[31:13])), (A4[21:0] @ A4[31:22])), ((A4 & A3) | (A4 & A2) | (A3 & A2))));
ASSERT(Ap6 = BVPLUS(32, BVSUB(32, Ep6, A2), BVXOR(BVXOR((Ap5[1:0] @ Ap5[31:2]), (Ap5[12:0] @ Ap5[31:13])), (Ap5[21:0] @ Ap5[31:22])), ((Ap5 & A4) | (Ap5 & A3) | (A4 & A3))));
ASSERT(Ap7 = BVPLUS(32, BVSUB(32, Ep7, A3), BVXOR(BVXOR((Ap6[1:0] @ Ap6[31:2]), (Ap6[12:0] @ Ap6[31:13])), (Ap6[21:0] @ Ap6[31:22])), ((Ap6 & Ap5) | (Ap6 & A4) | (Ap5 & A4))));
ASSERT(Ap8 = BVPLUS(32, BVSUB(32, Ep8, A4), BVXOR(BVXOR((Ap7[1:0] @ Ap7[31:2]), (Ap7[12:0] @ Ap7[31:13])), (Ap7[21:0] @ Ap7[31:22])), ((Ap7 & Ap6) | (Ap7 & Ap5) | (Ap6 & Ap5))));
ASSERT(W7 = BVSUB(32, BVSUB(32, BVSUB(32, BVSUB(32, BVSUB(32, E7, A3), E3), BVXOR(BVXOR((E6[5:0] @ E6[31:6]), (E6[10:0] @ E6[31:11])), (E6[24:0] @ E6[31:25]))), ((E6 & E5) | (~E6 & E4))), 0hexab1c5ed5));
ASSERT(W8 = BVSUB(32, BVSUB(32, BVSUB(32, BVSUB(32, BVSUB(32, E8, A4), E4), BVXOR(BVXOR((E7[5:0] @ E7[31:6]), (E7[10:0] @ E7[31:11])), (E7[24:0] @ E7[31:25]))), ((E7 & E6) | (~E7 & E5))), 0hexd807aa98));
ASSERT(W9 = BVSUB(32, BVSUB(32, BVSUB(32, BVSUB(32, BVSUB(32, E9, A5), E5), BVXOR(BVXOR((E8[5:0] @ E8[31:6]), (E8[10:0] @ E8[31:11])), (E8[24:0] @ E8[31:25]))), ((E8 & E7) | (~E8 & E6))), 0hex12835b01));
ASSERT(W10 = BVSUB(32, BVSUB(32, BVSUB(32, BVSUB(32, BVSUB(32, E10, A6), E6), BVXOR(BVXOR((E9[5:0] @ E9[31:6]), (E9[10:0] @ E9[31:11])), (E9[24:0] @ E9[31:25]))), ((E9 & E8) | (~E9 & E7))), 0hex243185be));
ASSERT(W11 = BVSUB(32, BVSUB(32, BVSUB(32, BVSUB(32, BVSUB(32, E11, A7), E7), BVXOR(BVXOR((E10[5:0] @ E10[31:6]), (E10[10:0] @ E10[31:11])), (E10[24:0] @ E10[31:25]))), ((E10 & E9) | (~E10 & E8))), 0hex550c7dc3));
ASSERT(W12 = BVSUB(32, BVSUB(32, BVSUB(32, BVSUB(32, BVSUB(32, E12, A8), E8), BVXOR(BVXOR((E11[5:0] @ E11[31:6]), (E11[10:0] @ E11[31:11])), (E11[24:0] @ E11[31:25]))), ((E11 & E10) | (~E11 & E9))), 0hex72be5d74));
ASSERT(Ep9 = BVPLUS(32, Ap5, Ep5, BVXOR(BVXOR((Ep8[5:0] @ Ep8[31:6]), (Ep8[10:0] @ Ep8[31:11])), (Ep8[24:0] @ Ep8[31:25])), ((Ep8 & Ep7) | (~Ep8 & Ep6)), 0hex12835b01, W9, 0hex00008004));
ASSERT(Ap9 = BVPLUS(32, BVSUB(32, Ep9, Ap5), BVXOR(BVXOR((Ap8[1:0] @ Ap8[31:2]), (Ap8[12:0] @ Ap8[31:13])), (Ap8[21:0] @ Ap8[31:22])), ((Ap8 & Ap7) | (Ap8 & Ap6) | (Ap7 & Ap6))));
ASSERT(Ep10 = BVPLUS(32, Ap6, Ep6, BVXOR(BVXOR((Ep9[5:0] @ Ep9[31:6]), (Ep9[10:0] @ Ep9[31:11])), (Ep9[24:0] @ Ep9[31:25])), ((Ep9 & Ep8) | (~Ep9 & Ep7)), 0hex243185be, W10, 0hex00000000));
ASSERT(Ap10 = BVPLUS(32, BVSUB(32, Ep10, Ap6), BVXOR(BVXOR((Ap9[1:0] @ Ap9[31:2]), (Ap9[12:0] @ Ap9[31:13])), (Ap9[21:0] @ Ap9[31:22])), ((Ap9 & Ap8) | (Ap9 & Ap7) | (Ap8 & Ap7))));
ASSERT(Ep11 = BVPLUS(32, Ap7, Ep7, BVXOR(BVXOR((Ep10[5:0] @ Ep10[31:6]), (Ep10[10:0] @ Ep10[31:11])), (Ep10[24:0] @ Ep10[31:25])), ((Ep10 & Ep9) | (~Ep10 & Ep8)), 0hex550c7dc3, W11, 0hex00000000));
ASSERT(Ap11 = BVPLUS(32, BVSUB(32, Ep11, Ap7), BVXOR(BVXOR((Ap10[1:0] @ Ap10[31:2]), (Ap10[12:0] @ Ap10[31:13])), (Ap10[21:0] @ Ap10[31:22])), ((Ap10 & Ap9) | (Ap10 & Ap8) | (Ap9 & Ap8))));
ASSERT(Ep12 = BVPLUS(32, Ap8, Ep8, BVXOR(BVXOR((Ep11[5:0] @ Ep11[31:6]), (Ep11[10:0] @ Ep11[31:11])), (Ep11[24:0] @ Ep11[31:25])), ((Ep11 & Ep10) | (~Ep11 & Ep9)), 0hex72be5d74, W12, 0hex00000000));
ASSERT(Ap12 = BVPLUS(32, BVSUB(32, Ep12, Ap8), BVXOR(BVXOR((Ap11[1:0] @ Ap11[31:2]), (Ap11[12:0] @ Ap11[31:13])), (Ap11[21:0] @ Ap11[31:22])), ((Ap11 & Ap10) | (Ap11 & Ap9) | (Ap10 & Ap9))));
ASSERT(BVSUB(32, BVXOR(BVXOR((BVPLUS(32, W7, 0hex4fefb5fa)[6:0] @ BVPLUS(32, W7, 0hex4fefb5fa)[31:7]), (BVPLUS(32, W7, 0hex4fefb5fa)[17:0] @ BVPLUS(32, W7, 0hex4fefb5fa)[31:18])), (0bin000 @ BVPLUS(32, W7, 0hex4fefb5fa)[31:3])), BVXOR(BVXOR((W7[6:0] @ W7[31:7]), (W7[17:0] @ W7[31:18])), (0bin000 @ W7[31:3]))) = 0hexffdf780f);
ASSERT(BVSUB(32, BVXOR(BVXOR((BVPLUS(32, W8, 0hex28011100)[6:0] @ BVPLUS(32, W8, 0hex28011100)[31:7]), (BVPLUS(32, W8, 0hex28011100)[17:0] @ BVPLUS(32, W8, 0hex28011100)[31:18])), (0bin000 @ BVPLUS(32, W8, 0hex28011100)[31:3])), BVXOR(BVXOR((W8[6:0] @ W8[31:7]), (W8[17:0] @ W8[31:18])), (0bin000 @ W8[31:3]))) = 0hexb00fca02);
ASSERT(BVSUB(32, BVXOR(BVXOR((BVPLUS(32, W9, 0hex00008004)[6:0] @ BVPLUS(32, W9, 0hex00008004)[31:7]), (BVPLUS(32, W9, 0hex00008004)[17:0] @ BVPLUS(32, W9, 0hex00008004)[31:18])), (0bin000 @ BVPLUS(32, W9, 0hex00008004)[31:3])), BVXOR(BVXOR((W9[6:0] @ W9[31:7]), (W9[17:0] @ W9[31:18])), (0bin000 @ W9[31:3]))) = 0hexd7feef00);
ASSERT(BVSUB(32, Ap10, A10) = 0hex00008004);
ASSERT(Ap11 = A11);
ASSERT(Ap12 = A12);
ASSERT(BVPLUS(32, A9, E9, BVXOR(BVXOR((E12[5:0] @ E12[31:6]), (E12[10:0] @ E12[31:11])), (E12[24:0] @ E12[31:25])), ((E12 & E11) | (~E12 & E10))) = BVPLUS(32, Ap9, Ep9, BVXOR(BVXOR((Ep12[5:0] @ Ep12[31:6]), (Ep12[10:0] @ Ep12[31:11])), (Ep12[24:0] @ Ep12[31:25])), ((Ep12 & Ep11) | (~Ep12 & Ep10))));
ASSERT(BVSUB(32, ((A12 & A11) | (A12 & A10) | (A11 & A10)), A9) = BVSUB(32, ((Ap12 & Ap11) | (Ap12 & Ap10) | (Ap11 & Ap10)), Ap9));
ASSERT((BVXOR(A5, Ap5) & 0hexffffe805) = 0hex00000000);
ASSERT((A5 & 0hex00000400) = 0hex00000000);
ASSERT((Ap5 & 0hex00000400) = 0hex00000400);
ASSERT((A5 & 0hex000013fa) = 0hex000013fa);
ASSERT((Ap5 & 0hex000013fa) = 0hex00000000);
ASSERT((BVXOR(A6, Ap6) & 0hexff7ffffe) = 0hex00000000);
ASSERT((A6 & 0hex00000001) = 0hex00000000);
ASSERT((Ap6 & 0hex00000001) = 0hex00000001);
ASSERT((A6 & 0hex00800000) = 0hex00800000);
ASSERT((Ap6 & 0hex00800000) = 0hex00000000);
ASSERT((BVXOR(A7, Ap7) & 0hexeedfeffa) = 0hex00000000);
ASSERT((A7 & 0hex10000001) = 0hex00000000);
ASSERT((Ap7 & 0hex10000001) = 0hex10000001);
ASSERT((A7 & 0hex01201004) = 0hex01201004);
ASSERT((Ap7 & 0hex01201004) = 0hex00000000);
ASSERT((BVXOR(A8, Ap8) & 0hexfffffffb) = 0hex00000000);
ASSERT((A8 & 0hex00000004) = 0hex00000004);
ASSERT((Ap8 & 0hex00000004) = 0hex00000000);
ASSERT((BVXOR(A9, Ap9) & 0hexffffffff) = 0hex00000000);
ASSERT((BVXOR(A10, Ap10) & 0hexffff7ffb) = 0hex00000000);
ASSERT((A10 & 0hex00008004) = 0hex00000000);
ASSERT((Ap10 & 0hex00008004) = 0hex00008004);
ASSERT((BVXOR(A11, Ap11) & 0hexffffffff) = 0hex00000000);
ASSERT((BVXOR(A12, Ap12) & 0hexffffffff) = 0hex00000000);
ASSERT((BVXOR(E5, Ep5) & 0hexffffcfc1) = 0hex00000000);
ASSERT((E5 & 0hex00001022) = 0hex00000000);
ASSERT((Ep5 & 0hex00001022) = 0hex00001022);
ASSERT((E5 & 0hex0000201c) = 0hex0000201c);
ASSERT((Ep5 & 0hex0000201c) = 0hex00000000);
ASSERT((BVXOR(E6, Ep6) & 0hexfff77ffe) = 0hex00000000);
ASSERT((E6 & 0hex00008000) = 0hex00000000);
ASSERT((Ep6 & 0hex00008000) = 0hex00008000);
ASSERT((E6 & 0hex00080001) = 0hex00080001);
ASSERT((Ep6 & 0hex00080001) = 0hex00000000);
ASSERT((BVXOR(E7, Ep7) & 0hex2f77fb76) = 0hex00000000);
ASSERT((E7 & 0hex90080408) = 0hex00000000);
ASSERT((Ep7 & 0hex90080408) = 0hex90080408);
ASSERT((E7 & 0hex40800081) = 0hex40800081);
ASSERT((Ep7 & 0hex40800081) = 0hex00000000);
ASSERT((BVXOR(E8, Ep8) & 0hexb2ff77fb) = 0hex00000000);
ASSERT((E8 & 0hex49000804) = 0hex00000000);
ASSERT((Ep8 & 0hex49000804) = 0hex49000804);
ASSERT((E8 & 0hex04008000) = 0hex04008000);
ASSERT((Ep8 & 0hex04008000) = 0hex00000000);
ASSERT((BVXOR(E9, Ep9) & 0hexfffffff7) = 0hex00000000);
ASSERT((E9 & 0hex00000008) = 0hex00000000);
ASSERT((Ep9 & 0hex00000008) = 0hex00000008);
ASSERT((BVXOR(E10, Ep10) & 0hexd07e7807) = 0hex00000000);
ASSERT((E10 & 0hex0f810400) = 0hex00000000);
ASSERT((Ep10 & 0hex0f810400) = 0hex0f810400);
ASSERT((E10 & 0hex200083f8) = 0hex200083f8);
ASSERT((Ep10 & 0hex200083f8) = 0hex00000000);
ASSERT((BVXOR(E11, Ep11) & 0hexef3ffff7) = 0hex00000000);
ASSERT((E11 & 0hex10c00000) = 0hex00000000);
ASSERT((Ep11 & 0hex10c00000) = 0hex10c00000);
ASSERT((E11 & 0hex00000008) = 0hex00000008);
ASSERT((Ep11 & 0hex00000008) = 0hex00000000);
ASSERT((BVXOR(E12, Ep12) & 0hexffff7ff7) = 0hex00000000);
ASSERT((E12 & 0hex00008008) = 0hex00008008);
ASSERT((Ep12 & 0hex00008008) = 0hex00000000);
QUERY(FALSE);
COUNTEREXAMPLE;
```

