# sha256-r38, the P8 two-block cost bound with the P1 sum-claw (time_log2 83.95905, memory 2^28.094, score 92.05305)

This is a cost bound for the target sha256-r38-prefix-v1. It uses the characteristic P8 of dariolina's 1a695f0b (its cells, its 38-step semi-free-start pair and its accepted event), the two-block A0-variant procedure of ePrint 2026/1120 as used in our fb176310 (accepted) and 9aaf71a2, and our own **P1 sum-claw**, which finds the row-16 passes. Everything the bound uses is defined, counted or derived in this file and in `experiments/p1claw38.py` (own code, standard library; P8 is read from the public proof of 1a695f0b as data; no code of another participant is executed). Credits are listed in the submission note.

Claim: time_log2 = 83.95905 (exact total N = 51,290,469,928,495,875,419,717,479,508 counted word operations = 2^83.95905 target compressions of C = 2,728 operations; the online work is charged at its hard cap V_MAX). Success probability at least 0.39. Memory 2^28.094 bytes. Preprocessing 2^78.09276 (the allowances, inside the time). Score under hashsmash-scalar-tm-v1: 83.95905 + 8.094 = 92.05305. `python3 experiments/p1claw38.py ledger` prints every number of Sections 5 to 7; `selftest` runs the checks of Section 12.

## 1. Target and output

SHA-256 steps 0..37 on every padded block, the standard IV once, FIPS 180-4 padding, feed-forward, all eight digest words. The procedure outputs two distinct 128-byte messages m = M0||M1 and m' = M0||M1' with a common first block M0 (FIPS padding appends the same third block).

**Lemma 1.** Let cv = F_38(IV, M0). If the second-block computations of M1 and M1' from cv end with equal state words A34..A37, E34..E37, the digests of m and m' are equal. *Proof:* the second-block output is cv plus (A37, A36, A35, A34, E37, E36, E35, E34), and the third block is the same for both. m != m' because M1 and M1' differ in W7. Every output is therefore a collision of the target.

## 2. Data and the P1 pair

- **P8 (1a695f0b, transcribed as data).** The 38-step semi-free-start pair (PCV, PMX, PMY), the cells of rows 7..37 (`CELLS`: for A, E, W the mask of fixed bits, their values and the XOR difference), the '+' pairs (`PQE`, the printed pairs except E18 = E17 at row 18) and the two-bit conditions (`X2`). S denotes the state words of the pair: A2..A15 and E6..E15 of member x (= PMX) and member y (= PMY). The program checks that PCV, PMX, PMY reproduce the pair and pass every test of rows 16..21 with equal outputs (Section 12).
- **The P1 pair.** For a chaining value cv and two free words a0, a1, both members take A0 = a0, A1 = a1, A2..A15 and E6..E15 from S; E0..E5 and W0..W15 follow from the step equations (`variantW_P1`). W10..W15 are S's words; W0..W9 depend on (cv, a0, a1); W0..W6 and E0..E5 are equal in the two members. With a0 = A0, a1 = A1 and cv = PCV this is the P8 pair.
- **Row 16.** W16 = s1(W14) + W9 + s0(W1) + W0, so E16 of member x is E16x = C16 + W0 + s0(W1). From the step equations of steps 0 and 1, W1 = u := a1 + h(a0, cv) and W0 + C16 = F(a0) := Cc2 + a0 + k0(cv) + h(a0, cv) (Cc2 = 0x7af32e15; k0, h are written out in `cv_consts`, `hfun`), hence **E16x = F(a0) + s0(u) - u**. S160 is the set of 160 words that pass every row-16 cell and condition of P8: 20 heads (`R16H`) times the 8 values of bits 0, 2, 10. A **claw** is a pair (a0, u) with E16x in S160; every claw is a row-16 pass of member x.
- **Post-filters.** For a claw, a1 = u - h(a0, cv). On the words of the two members: C1: W8y - W8x = D8 (tested as: the top three bits of E5 = a1 + cE5 are 101); C2: s0(W9y) - s0(W9x) = D9s; G: s0(W8y) - s0(W8x) = T8; F7: s0(W7y) - s0(W7x) = F7d (W9y - W9x = D9 and W7y - W7x = D7 always). The constants are those of the P8 pair. C1, C2 read only a1; G reads (a0, a1); F7 reads (a0, a1, cv). A **good pair** is a claw passing all four. The counted chain (`postfilters`) equals these definitions evaluated on the real words (`pf_ref`): 0 mismatches in `selftest` (60,000 pairs) and on every claw of `p1-online-r38`.

## 3. The procedure (fixed caps)

```text
input: N_CV, V_MAX; data: Section 2.   V = 0 (a register: the online operations executed so far)
for j = 1 .. N_CV:
    if V > V_MAX: halt (failure)
    draw M0 (two random 256-bit words, 16 fields); cv := F_38(IV, M0); the claw scalars of cv; u0 := random word
    V += C + 75 + 2^26 x 45 + 2^28 x 593        (this chaining value's fixed work; the 75 is cv_begin, Section 5)
    table: 2^26 slots of 4 bytes, packed eight to a 256-bit word, every slot = SENT (all ones)
    for i = 0 .. 2^26 - 1: a0 := (9 << 26) | i; slot := top 26 bits of F(a0); store (i << 6) | (F(a0) mod 2^6) there (last write wins)
    for n = 0 .. 2^28 - 1: u := u0 + n mod 2^32;  P := s0(u) - u
        for each head H of R16H: W := H - P; for each window Wsub in (W, W + 1024):
            e := slot[top 26 bits of Wsub]; if (e - Wsub) AND 0x3a = 0: V += 3 if e = SENT, else V += 10
                if e != SENT: F := (slot << 6) | (e mod 2^6); if (F - Wsub) AND NOT 5 = 0: CLAW(a0 = (9 << 26) | (e >> 6), u, F)
            if Wsub mod 2^6 >= 59 (straddle; V += 23 once per head): the same with the next slot (V += 8 when not SENT)
    CLAW: a1 := u - F + Cc2 + k0 + a0; test C1, C2, G, F7 in turn (V += 7, 22, 29, 30 per stage reached)
        good pair: STEP 3B; if it accepts: output m = M0||M1, m' = M0||M1' (W0..W15 of the two members); final verification; halt
halt (failure)
```

**Step 3b** (`step3b`) on a good pair: Step 2 of both members (E0..E5, W0..W9), then rows 16..37 of both members; after each of rows 16..21 the tests of that row run, and the first failing test stops step 3b. The tests of row i: for A, E and W of row i (W not at rows 7, 8) the cell values on the fixed bits and the XOR difference on all 32 bits; the '+' pair of `PQE[i]`; every two-bit condition of `X2` closing at row i. If rows 16..21 pass, the eight output words of the two members are compared; step 3b accepts iff they are equal, so by Lemma 1 every accepted pair is a collision. Step 3b reads nothing beyond (cv, a0, a1) and the data of Section 2.

Distinct scan words. u runs over u0, u0 + 1, ..., u0 + 2^28 - 1, which are distinct; at one u each a0 matches at most one of the 160 targets, and a1 = u - h(a0, cv); so the claws of one chaining value are distinct pairs (a0, a1). The organizer experiments report `distinct_pairs` = claws on every trial.

## 4. Pricing (H5')

collision-frontier-v5, 256-bit word RAM; the unit costs of fb176310: load, store, add, sub, and, or, xor, not, shift, immediate, random word 1; compare-and-branch 2; S0, S1, s0, s1 8; CH 3; MAJ 4; one target compression C = 2,728. The table holds 2^26 four-byte slots packed eight to a 256-bit word (2^28 bytes). A packed load is index shift, lane and+shift, address add, 256-bit load, shift, and = 7 operations; a packed store is a read-modify-write = 11. Every work-counter add (V += k) is one operation and is counted. `run_claw` charges every operation of Section 3 at these costs through the counter `Mach`.

## 5. The exact ledger

Per chaining value, counted in `run_claw`:
- **Fixed:** cv_begin 75 (first-block words 30, claw scalars 38, u0 1, V add 1, cap test 2, loop 3) plus one compression C; table build 2^26 x 45 (a0 1, E0 1, S0 8, MAJ 2, S1 8, CH 2, F 5, slot 1, entry 3, loop 3, packed store 11); per u 593 = 13 (u0 + n 1, s0 8, sub 1, loop 3) + 20 heads x (5 + 2 lookups x 12) (lookup: index 1, packed load 7, residue sub and 2, branch 2).
- **Variable, per u (expectations):** a head straddles with probability 5/2^6 (the low 6 bits of W are uniform: s0(u) mod 2^6 is uniform because it contains u's bits 18..23): 20 x (5/64) x (23 + 2 x 8 occ) = 51.7405. A lookup passes the residue test with probability 4/2^6, an occupied slot by its uniform tag and an empty one by SENT's tag: 40 x (4/64) x (3 + 7 occ) = 18.5621. occ = 1 - (1 - 2^-26)^(2^26) = 0.632121 (expected occupied fraction).
- **Claws:** 160 occ x 2^26 / 2^32 = 1.58030 per u. Post-filters per claw: 7 + 22/8 + 29 x P(C1 C2) + 30 x P(C1 C2 G) = 10.1145. A good pair (probability q_pf = 2^-16.1877 per claw, Section 6) runs step 3b, charged at its longest path, **3,014** operations (every test passing, counted by `selftest` on the P8 pair).

| quantity | value |
|---|---|
| per u: 593 + 51.7405 + 18.5621 + 1.58030 x (10.1145 + q_pf x 3,014) | 679.3504 |
| scan per claw, (593 + 70.3026) / 1.58030 | 419.732 |
| post-filters per claw | 10.115 |
| table build per claw, 2^26 x 45 / (2^28 x 1.58030) | 7.119 |
| operations per claw (scan, post-filters, build) | 436.965 |
| claws per good pair, 1 / q_pf | 74,641 |
| wbar = C + 75 + 2^26 x 45 + 2^28 x 679.3504, mean online work of one chaining value | 1.853816e11 |
| vmax = C + 75 + 2^26 x 45 + 2^28 x 249,933, maximum online work of one chaining value | 67,093,898,726,131 |
| N_CV (Section 7) | 231,845,170,969,091,846 |

249,933 = 593 + 20 x (23 + 2 x 10 + 2 x 8) + 80 x (7 + 22 + 29 + 30 + 3,014): every head straddling, every slot occupied, and at most 4 claws per head (one per window and slot), each reaching step 3b. The means use H1 (occupancy, uniform tags and table contents) and H1-P1 (stage rates); step 3b is charged at its maximum, so wbar bounds the mean from above.

  V_MAX = ceil((1 + 2^-16) x N_CV x wbar) = 42,980,494,904,638,086,816,851,623,386
  N = (2^78 + 2^74 + 2^70) x C + FB + V_MAX + OVER + FIN = 51,290,469,928,495,875,419,717,479,508,  time_log2 = log2(N / C) = 83.95905.

FB = N_FB x (C + 35) with N_FB = 2,689,372,601,475,987,602,319,909, the first-block count of the base ledger (35 = 30 for the first-block words + 5 control), is charged in full in addition (ruling 5d2a479a); the N_CV first blocks the procedure draws are also inside V_MAX. OVER = vmax (Lemma 2). FIN = 6 C + 1,600: the two 3-block digests of m, m' and their assembly and comparison. Appendix A lists the terms.

**Lemma 2 (the cap).** The cap test reads V at the start of every chaining value; at that moment V equals the online work executed so far (the fixed part is added when the chaining value starts, each variable segment adds its own cost). A chaining value started with V <= V_MAX adds at most vmax. Hence the executed online work is at most V_MAX + OVER for every execution.

**Lemma 3 (cap halt, derived).** Let W_j be the online work of chaining value j. The W_j are independent (H1: independent chaining values; u0 is a fresh random word), 0 <= W_j <= vmax and E[W_j] <= wbar. The procedure halts at a cap test only if sum_j W_j > V_MAX, i.e. exceeds its mean bound by t >= 2^-16 N_CV wbar. Var(W_j) <= E[W_j^2] <= vmax wbar, so Bernstein's inequality gives Pr[halt] <= exp(-t^2 / (2 (N_CV vmax wbar + vmax t / 3))) <= exp(-2^-32 N_CV wbar / (2 vmax (1 + 2^-16/3))) = exp(-74,574) < 2^-107,000. No variance premise beyond H1 and the deterministic bound vmax is used. When the procedure halts it outputs nothing (Lemma 1 covers every output).

## 6. The post-filter law q_pf (H1-P1)

Exact counts over all 2^32 values (own exhaustive program): P(C1) = 1/8; |C1 and C2| = 53,096,854 (C1, C2 read only a1); for a0 in the window R = 9 (top 6 bits of a0 equal to 9) the (a1 in C1 and C2)-summed count of G is 57,726,359,870,197, so P(C1 C2 G) = 57,726,359,870,197 / 2^58; |F7| = 287,309,824 and F7, averaged over a uniform chaining value, has probability |F7| / 2^32 for any law of (a0, a1). Hence q_pf = 57,726,359,870,197 x 287,309,824 / 2^90 = 2^-16.1877. H1-P1 is the premise that these rates hold for the claws the procedure finds (the claws' a1 = u - h(a0, cv) and the claws' a0 are the visible table entries, where last write wins). Development support (our C port `p1claw.c`): the stage rates C1 0.12501, C2|C1 2^-3.3379, G 2^-5.996 on real claws, the 36-chaining-value panel (claw/base ratio 0.991 to 1.124) and 294 good pairs, all passing C1, C2, G, F7. The organizer experiments report the stage counts c1, c1c2, c1c2g, all4 as reproducible observations.

## 7. Success probability

Let X_j be the number of good pairs of chaining value j that step 3b accepts, and q3r the probability that a good pair is accepted.

- **H2-P1.** q3r >= q3_model x 2^32 / 160 = 2^-71.1710, where q3_model = 2^-95.8491 is the success probability declared by 9aaf71a2 for its good pairs before row 16 (Pr[row 16] = 160/2^32 there). Section 9.
- **Expectation.** E[X_j] = 2^28 x c x q_pf x q3r with c >= 160 (2^26 occ - 1/64) / 2^32 claws per u (an entry equal to SENT is skipped; only the last candidate can produce it, with probability 1/64).
- **Within a chaining value (Lemma 4, derived; H3-P1).** For a fixed cv let Y(x) be the number of accepted good pairs at scan word x and J = sum over all 2^32 words x of Y(x). The scan reads x = u0 + n, n < 2^28, distinct, with u0 uniform; so E[X_j | cv] = 2^28 J / 2^32 and E[X_j (X_j - 1) | cv] = sum_n E[Y(Y-1)] + sum_{n != m} E[Y(u0+n) Y(u0+m)] <= 2^28 2^-32 (sum_x Y(x)(Y(x)-1) + sum_{x != y} Y(x) Y(y)) = 2^28 2^-32 J(J-1), because each ordered pair of distinct words occurs for at most 2^28 pairs (n, m). Hence E[X_j (X_j - 1)] / E[X_j] <= E[J(J-1)] / E[J], with no premise on the scan. **H3-P1** states E[J(J-1)] <= 2^-7.5 E[J]: given one accepted pair, a chaining value has on average at most 2^-7.5 others over all 2^32 scan words. Bonferroni then gives Pr[X_j >= 1] >= E[X_j] - E[X_j(X_j - 1)]/2 >= (1 - 2^-8.5) E[X_j].
- **Across chaining values (H1).** Pr[some X_j >= 1] >= 1 - exp(-N_CV (1 - 2^-8.5) E[X_j]).
- **Bound.** N_CV is the least integer with 1 - exp(-N_CV (1 - 2^-8.5) E[X_j]) - 2^-60 >= 0.39 (exponentials at 90 digits): N_CV = 231,845,170,969,091,846. With Lemma 3, Pr[output a collision] >= 0.39 + 3.5 x 10^-19 - 2^-107,000 >= 0.39.

## 8. H3-P1: what it requires and its support

E[J] = 2^32 x 1.58030 x 2^-16.1877 x q3r = 2^-54.70. If the accepted good pairs of one chaining value were independent given cv, E[J(J-1)]/E[J] would be about E[J] = 2^-54.70; H3-P1 allows positive dependence or per-chaining-value heterogeneity up to a factor 2^47.2 above that. It fails only if, given one accepted pair, the other good pairs of that chaining value over all 2^32 scan words (about 2^16.47 of them) are accepted, on average, with probability above 2^-23.97 each instead of 2^-71.2. Support: (i) the claws of one chaining value are distinct pairs (a0, a1) with distinct (W0, W1) = (a0 + c0(cv), u) (Section 3; `distinct_pairs` in both experiments); (ii) acceptance is a function of W0..W9 of the pair (rows 16..37 read only S's words and W16..W37, which W0..W15 fix), and of these W8 and W9 depend on (a0, a1) only; (iii) the one post-filter that reads the chaining value, F7, has measured per-chaining-value heterogeneity 1.254 (development, 36 chaining values); (iv) the organizer experiments report per chaining value the claws, stage counts and rows 16..21 counts. The full event (about 2^-71 per good pair) is not observable at any sample size; H3-P1 is declared as a premise.

## 9. The q3 transfer (H2-P1)

Rows 16..37 of both members read only S's words W10..W15 and W16..W37, which W0..W15 fix. For a fixed (a0, a1) the tests of rows 16..21 and the output comparison are, cell for cell, the accepted event that 9aaf71a2 prices; the P1 pair differs from 9aaf71a2's A0-variant only in the laws of W0..W9 (a1 is free instead of fixed). Ratio of the two families' q3: development measurement R = 1.0162, bootstrap 95% [0.9735, 1.0584] (512 SMC prefixes, not preregistered). H2-P1 takes R = 1. At R = 0.9735 the time is 83.99159 and the score 92.08559 (+0.033 bit).

## 10. Memory (H6) and advice

Online: the table 2^26 x 4 = 268,435,456 bytes (2^28), plus the advice below, the registers (64 x 32 bytes) and the scan state (under 1 KiB), in all below 2^28 + 2^14 bytes. Our C port of the claw at n0 = 2^26 ran with a peak resident set of 264,224 KiB = 2^28.011 bytes (`/usr/bin/time -v`). The claimed peak is the maximum over the counted phases: the Step-1 solve of P8, measured by its author at 279,720 KB = 2^28.094 bytes. Score 83.95905 + (28.094 - 20) = 92.05305.
Advice inventory (bytes): A2..A15 and E6..E15 of both members, 48 words, 192; the cells of rows 16..21 (54 words) 216, their '+' pairs (6 words) 24 and the 35 two-bit conditions (4 bytes each) 140; the 20 heads of S160 80; 19 post-filter and claw constants 76; K and IV (46 words) 184: in all 912 bytes, under 2^10, inside the declared 2^13.

## 11. Allowances and development (H4a, H4b, H4c)

A_C = 2^78 (the characteristic search of 1a695f0b), A_S = 2^74 (its Step-1 solve) and DEV = 2^70 (all our development) are charged in full; preprocessing = log2(2^78 + 2^74 + 2^70) = 78.09276. H4c: every code execution of this project (10-05 to 10-20), whether or not the procedure reads its output (exhaustive passes, C ports, q3 and ratio studies, the F7 measurement, checks, failed runs and reruns), ran on a 24-thread workstation with one GPU, a 12-thread server and one 32-vCPU cloud machine. At most 68 threads and one GPU for 16 days (1.3824 x 10^6 s), at most 2^40 word operations per thread-second and 2^47 per GPU-second, give at most 2^66.49 + 2^67.40 < 2^68.1 operations = 2^56.7 compressions, under DEV = 2^70 by a factor above 2^13. The recorded total of the runs behind this package is below 2.1 x 10^5 CPU-seconds.

## 12. Checks

- `selftest`: the P8-pair constants; |S160| = 160; step 3b on the P8 pair accepts (rows 16..21 pass, outputs equal) in 3,014 operations; the counted post-filter chain against the real words (60,000 pairs, 0 mismatches); a run at 2^18 slots and 2^14 scan words: the claws equal an independent sorted-array search, all claws distinct, every claw's real E16 in S160, and the counted operations at most the per-u charge of Section 5 at that size; the ledger and the success bound.
- `p1-online-r38` (organizer): 8 seed-drawn chaining values at 2^16 slots and 2^12 scan words, the counted procedure including step 3b on every good pair, every claw checked against the reference search, the real E16 and the real-word post-filters; a pair is returned only if step 3b accepts (none is expected at this size); trial 8 runs step 3b on the P8 pair. `p1-q3-r38`: rows 16..21 counts of every claw at 2^16 slots and 2^13 words. Their counts are reproducible observations consistent with the premises; no rate is inferred from them.
- Development (C port, n0 = 2^22..2^26): claws equal the reference, 0 bad, occupancy 0.63216 and claws/expected 0.99898 at n0 = 2^26 with 2^20 scan words, scan 425.592 operations per u before the packed-access and counter costs (matching the straight-line count).

## Appendix A. The ledger, term by term

| term (operations) | value |
|---|---|
| allowance A_C = 2^78 x C | 824,487,408,977,177,097,149,612,032 |
| allowance A_S = 2^74 x C | 51,530,463,061,073,568,571,850,752 |
| allowance DEV = 2^70 x C | 3,220,653,941,317,098,035,740,672 |
| first blocks FB = N_FB x (C + 35) | 7,430,736,497,878,153,745,209,908,567 |
| online work cap V_MAX (charged in full) | 42,980,494,904,638,086,816,851,623,386 |
| overshoot OVER = vmax | 67,093,898,726,131 |
| final verification FIN | 17,968 |
| **N** | **51,290,469,928,495,875,419,717,479,508** |

N / C = 2^83.95905; score 92.05305.
