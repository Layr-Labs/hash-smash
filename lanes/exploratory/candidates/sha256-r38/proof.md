# sha256-r38 P1 four-bucket transpose and direct address chain (score 91.43180)

**Ready status.** This package starts from Yukon submission `711c4bf8-5c69-4f9c-bd1b-fe983984a096`, replaces its P1 row-16 table with a seven-entry uniform reservoir, and uses the r38-specific common low-nine-bit identity of all twenty row-16 heads. It repairs the prior bucket7 package and all v2 review findings: the registered q3 list law differs from the online joint good-pair law, and the 256-bit machine requires explicit reductions for intended SHA-256 words. The final bounds are `time_log2=83.33780` and `memory_log2_bytes=28.094`, for scalar score `91.43180`, 0.51680 bit below the live incumbent.

The package is `submission_state: ready` for exploratory organizer and human review. A preregistered paired SMC study supports a separately charged 0.20-bit list-to-joint-law allowance; complete accepted-event transfer remains heuristic. The declared experiment archive executes the inherited corrected typed lowering and verifier together with the final transpose/address-chain checker and repriced ledger, while preserving explicit `MASK32` operations. The C1 top-bit AND is charged; the actual 3,178-operation Step-3b fixture is checked against the typed contract without double-counting; eight-operation SHA sigma expansions are certified; and a 128 MiB checkpoint degree scan reproduces all exact degrees under the whole-computation memory cap. Paired studies share initial randomness and may desynchronize after law-dependent rejection. A physical full `2^32` attack scan is absent, and H1, H2 and H3 remain disclosed score-critical premises.

Appendix A.18 is the final normative overlay for the transposed table, scan lowering, resource ledger, experiment transport and score. Appendix A.15 remains normative for the online q3 law, success reduction and disclosures except where A.18 replaces its table and resource arithmetic. Historical text is retained as lineage and is superseded where A.15 or A.18 says so.

# Historical parent proof: sha256-r38 P8/P1 flat table (SUPERSEDED; time 83.93719, memory 28.01141, score 91.94860)

This is a cost bound for the target sha256-r38-prefix-v1. It uses the characteristic P8 of dariolina's 1a695f0b (its cells, its 38-step semi-free-start pair and its accepted event), the two-block A0-variant procedure of ePrint 2026/1120 as used in our fb176310 (accepted) and 9aaf71a2, and our own **P1 sum-claw**, which finds the row-16 passes. Everything the bound uses is defined, counted or derived in this file and in `experiments/p1claw38.py` (own code, standard library; P8 is read from the public proof of 1a695f0b as data; no code of another participant is executed). The records behind the premises (registrations, per-seed values, resource reports) are in Appendices P, Q and R of this file.

Claim: time_log2 = 83.93719 (exact total N = 50,519,128,711,573,853,964,925,507,997 counted word operations = 2^83.93719 target compressions of C = 2,728 operations; the online work is charged at its hard cap V_MAX). Success probability at least 0.39. Memory 2^28.01141 bytes (the counted cell of A.13.3: this package's measured full-table C-port execution). Preprocessing 2^78.09276 (the allowances, inside the time). Score under hashsmash-scalar-tm-v1: 83.93719 + 8.01141 = 91.94860. The scan length is 2^32 words per chaining value throughout this proof (Section 3, Section 7, Appendix A.13); no 2^28 scan figure is binding. `python3 experiments/p1claw38.py ledger` prints every number of Sections 5 to 7; `selftest` runs the checks of Section 12.

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
    V += C + 75 + 2^23 x 5 + 2^26 x 45 + 2^32 x 593   (this chaining value's fixed work; the 75 is cv_begin, Section 5)
    table: 2^26 slots of 4 bytes, packed eight to a 256-bit word; reset every slot to SENT (all ones): 2^23 word stores, 5 each (store 1, address add 1, loop 3)
    for i = 0 .. 2^26 - 1: a0 := (9 << 26) | i; slot := top 26 bits of F(a0); store (i << 6) | (F(a0) mod 2^6) there (last write wins)
    for n = 0 .. 2^32 - 1: u := u0 + n mod 2^32;  P := s0(u) - u
        for each head H of R16H: W := H - P; for each window Wsub in (W, W + 1024):
            e := slot[top 26 bits of Wsub]; if (e - Wsub) AND 0x3a = 0: V += 3 if e = SENT, else V += 10
                if e != SENT: F := (slot << 6) | (e mod 2^6); if (F - Wsub) AND NOT 5 = 0: CLAW(a0 = (9 << 26) | (e >> 6), u, F)
            if Wsub mod 2^6 >= 59 (straddle; V += 23 once per head): the same with the next slot (V += 8 when not SENT)
    CLAW: a1 := u - F + Cc2 + k0 + a0; test C1, C2, G, F7 in turn (V += 7, 22, 29, 30 per stage reached)
        good pair: STEP 3B; if it accepts: output m = M0||M1, m' = M0||M1' (W0..W15 of the two members); final verification; halt
halt (failure)
```

**Step 3b** (`step3b`) on a good pair: Step 2 of both members (E0..E5, W0..W9), then rows 16..37 of both members; after each of rows 16..21 the tests of that row run, and the first failing test stops step 3b. The tests of row i: for A, E and W of row i (W not at rows 7, 8) the cell values on the fixed bits and the XOR difference on all 32 bits; the '+' pair of `PQE[i]`; every two-bit condition of `X2` closing at row i. If rows 16..21 pass, the eight output words of the two members are compared; step 3b accepts iff they are equal, so by Lemma 1 every accepted pair is a collision. Step 3b reads nothing beyond (cv, a0, a1) and the data of Section 2.

Distinct scan words. u runs over u0, u0 + 1, ..., u0 + 2^32 - 1 (mod 2^32), a permutation of all 2^32 words, which are distinct; at one u each a0 matches at most one of the 160 targets, and a1 = u - h(a0, cv); so the claws of one chaining value are distinct pairs (a0, a1). The organizer experiments report `distinct_pairs` = claws on every trial.

The procedure draws only its own N_CV first blocks; each costs one compression plus the 75 operations of cv_begin, inside the fixed part of every chaining value (hence inside V_MAX). No other first-block enumeration is executed, so none is charged.

## 4. Pricing (H5')

collision-frontier-v5, 256-bit word RAM; the unit costs of fb176310: load, store, add, sub, and, or, xor, not, shift, immediate, random word 1; compare-and-branch 2; S0, S1, s0, s1 8; CH 3; MAJ 4; one target compression C = 2,728. The table holds 2^26 four-byte slots packed eight to a 256-bit word (2^28 bytes). A packed load is index shift, lane and+shift, address add, 256-bit load, shift, and = 7 operations; a packed store is a read-modify-write = 11. Every work-counter add (V += k) is one operation and is counted. `run_claw` charges every operation of Section 3 at these costs through the counter `Mach`.

## 5. The exact ledger

Per chaining value, counted in `run_claw`. The ledger is an exact analytic count read from the code; it does not rest on the organizer runs' counted_ops, which are reduced-size observations.
- **Fixed:** cv_begin 75 (first-block words 30, claw scalars 38, u0 1, V add 1, cap test 2, loop 3) plus one compression C; table reset to SENT 2^23 x 5 (2^23 256-bit words: store 1, address add 1, loop 3); table build 2^26 x 45 (a0 1, E0 1, S0 8, MAJ 2, S1 8, CH 2, F 5, slot 1, entry 3, loop 3, packed store 11); per u 593 = 13 (u0 + n 1, s0 8, sub 1, loop 3) + 20 heads x (5 + 2 lookups x 12) (lookup: index 1, packed load 7, residue sub and 2, branch 2).
- **Variable, per u (expectations):** a head straddles with probability 5/2^6 (the low 6 bits of W are uniform: s0(u) mod 2^6 is uniform because it contains u's bits 18..23): 20 x (5/64) x (23 + 2 x 8 occ) = 51.7405. A lookup passes the residue test with probability 4/2^6, an occupied slot by its uniform tag and an empty one by SENT's tag: 40 x (4/64) x (3 + 7 occ) = 18.5621. occ = 1 - (1 - 2^-26)^(2^26) = 0.632121 (expected occupied fraction).
- **Claws:** 160 occ x 2^26 / 2^32 = 1.58030 per u. Post-filters per claw: 7 + 22/8 + 29 x P(C1 C2) + 30 x P(C1 C2 G) = 10.1145. A good pair (probability q_pf = 2^-16.1877 per claw, Section 6) runs step 3b, charged at its longest path, **3,014** operations (every test passing, counted by `selftest` on the P8 pair).

| quantity | value |
|---|---|
| per u: 593 + 51.7405 + 18.5621 + 1.58030 x (10.1145 + q_pf x 3,014) | 679.3504 |
| scan per claw, (593 + 70.3026) / 1.58030 | 419.732 |
| post-filters per claw | 10.115 |
| table reset and build per claw, (2^23 x 5 + 2^26 x 45) / (2^32 x 1.58030) | 0.451 |
| operations per claw (scan, post-filters, reset and build) | 430.297 |
| claws per good pair, 1 / q_pf | 74,641 |
| wbar = C + 75 + 2^23 x 5 + 2^26 x 45 + 2^32 x 679.3504, mean online work of one chaining value | 2.920850e12 |
| vmax = C + 75 + 2^23 x 5 + 2^26 x 45 + 2^32 x 249,933, maximum online work of one chaining value | 1,073,457,123,035,891 |
| N_CV (Section 7) | 16,994,757,457,699,444 |

249,933 = 593 + 20 x (23 + 2 x 10 + 2 x 8) + 80 x (7 + 22 + 29 + 30 + 3,014): every head straddling, every slot occupied, and at most 4 claws per head (one per window and slot), each reaching step 3b. The means use H1 (occupancy, uniform tags and table contents) and H1-P1 (stage rates); step 3b is charged at its maximum, so wbar bounds the mean from above.

  V_MAX = ceil((1 + 2^-16) x N_CV x wbar) = 49,639,890,185,593,212,744,045,250,682
  N = (2^78 + 2^74 + 2^70) x C + V_MAX + OVER + FIN = 50,519,128,711,573,853,964,925,507,997,  time_log2 = log2(N / C) = 83.93719.

OVER = vmax (Lemma 2). FIN = 6 C + 1,600: the two 3-block digests of m, m' and their assembly and comparison. The N_CV first blocks are inside V_MAX (Section 3). Appendix A lists the terms.

**Lemma 2 (the cap).** The cap test reads V at the start of every chaining value; at that moment V equals the online work executed so far (the fixed part is added when the chaining value starts, each variable segment adds its own cost). A chaining value started with V <= V_MAX adds at most vmax. Hence the executed online work is at most V_MAX + OVER for every execution.

**Lemma 3 (cap halt, derived).** Let W_j be the online work of chaining value j. The W_j are independent (H1: independent chaining values; u0 is a fresh random word), 0 <= W_j <= vmax and E[W_j] <= wbar. The procedure halts at a cap test only if sum_j W_j > V_MAX, i.e. exceeds its mean bound by t >= 2^-16 N_CV wbar. Var(W_j) <= E[W_j^2] <= vmax wbar, so Bernstein's inequality gives Pr[halt] <= exp(-t^2 / (2 (N_CV vmax wbar + vmax t / 3))) <= exp(-2^-32 N_CV wbar / (2 vmax (1 + 2^-16/3))) = exp(-87,483) < 2^-126,212. No variance premise beyond H1 and the deterministic bound vmax is used. When the procedure halts it outputs nothing (Lemma 1 covers every output).

## 6. The post-filter law q_pf (H1-P1)

Exact counts over all 2^32 values (own exhaustive program): P(C1) = 1/8; |C1 and C2| = 53,096,854 (C1, C2 read only a1); for a0 in the window R = 9 (top 6 bits of a0 equal to 9) the (a1 in C1 and C2)-summed count of G is 57,726,359,870,197, so P(C1 C2 G) = 57,726,359,870,197 / 2^58; |F7| = 287,309,824 and F7, averaged over a uniform chaining value, has probability |F7| / 2^32 for any law of (a0, a1). Hence q_pf = 57,726,359,870,197 x 287,309,824 / 2^90 = 2^-16.1877. H1-P1 is the premise that these rates hold for the claws the procedure finds (the claws' a1 = u - h(a0, cv) and the claws' a0 are the visible table entries, where last write wins). Support: the 24-chaining-value panel of Appendix H (the C port of the counted claw at the package's window R = 9, 2^26 slots, 2^22 scan words each): pooled stage rates C1 0.12499 (exact 1/8), C2|C1 2^-3.3371 (exact 2^-3.3379), G|C1C2 2^-5.9380 (exact 2^-5.9481), F7|C1C2G 0.06618 (|F7|/2^32 = 0.06689), claws/expected 0.9984 to 1.0008; the organizer experiments report the stage counts c1, c1c2, c1c2g, all4 as reproducible observations.

## 7. Success probability

Let X_j be the number of good pairs of chaining value j that step 3b accepts, and q3r the probability that a good pair is accepted.

- **H2-P1.** q3r >= q3_P1 x 2^32 / 160 = 2^-71.4010, q3_P1 = 2^-96.0791 = q3_model x 2^min(0, D_LB): q3_model = 2^-96.0133 is the registered accepted-event rate of the A0-variant good pairs before row 16 (Pr[row 16] = 160/2^32), and D_LB = -0.0658 is the registered one-sided 99% lower bound of the paired difference between the P1 family on this package's window and the A0-variant family (Section 9).
- **Expectation.** E[X_j] = 2^32 x c x q_pf x q3r with c >= 160 (2^26 occ - 1/64) / 2^32 claws per u (an entry equal to SENT is skipped; only the last candidate can produce it, with probability 1/64).
- **Within a chaining value (Lemma 4, derived; H3-P1).** For a fixed cv let Y(x) be the number of accepted good pairs at scan word x and J = sum over all 2^32 words x of Y(x). The scan reads x = u0 + n, n < 2^32, distinct, with u0 uniform; so E[X_j | cv] = 2^32 J / 2^32 = J and E[X_j (X_j - 1) | cv] = sum_n E[Y(Y-1)] + sum_{n != m} E[Y(u0+n) Y(u0+m)] <= 2^32 2^-32 (sum_x Y(x)(Y(x)-1) + sum_{x != y} Y(x) Y(y)) = J(J-1), because each ordered pair of distinct words occurs for at most 2^32 pairs (n, m), i.e. exactly once when n ranges over all 2^32 words. Hence E[X_j (X_j - 1)] / E[X_j] <= E[J(J-1)] / E[J], with no premise on the scan. **H3-P1** (Section 8) gives E[J(J-1)] <= 2^-7.5 E[J]. Bonferroni then gives Pr[X_j >= 1] >= E[X_j] - E[X_j(X_j - 1)]/2 >= (1 - 2^-8.5) E[X_j].
- **Across chaining values (H1).** Pr[some X_j >= 1] >= 1 - exp(-N_CV (1 - 2^-8.5) E[X_j]).
- **Bound.** N_CV is the least integer with 1 - exp(-N_CV (1 - 2^-8.5) E[X_j]) - 2^-60 >= 0.39 (exponentials at 90 digits): N_CV = 271,916,119,323,191,097. With Lemma 3, Pr[output a collision] >= 0.39 - 2^-126,212 >= 0.39 (the 2^-60 term absorbs it; `ledger` prints 0.39000000000000000072).

## 8. H3-P1: group independence within a chaining value

**Statement (the form of the accepted 44870635, H5-group-independence, applied to good pairs).** Good pairs of one chaining value that share no endpoint (neither a0 nor u) are independent trials of the accepted event, each with the probability q3r of H2-P1; good pairs sharing an endpoint form a group, of which one is counted. Consequence used: E[J(J-1)] <= 2^-7.5 E[J].
**Derivation of the consequence.** With K good pairs per chaining value over all 2^32 scan words (E[K] = 2^32 x 1.58030 x q_pf = 2^16.47) and independent trials of probability q3r, E[J(J-1) | K] = K(K-1) q3r^2 and E[J | K] = K q3r, so E[J(J-1)] / E[J] = q3r E[K(K-1)] / E[K]. K varies with the chaining value only through F7 (C1, C2, G do not read cv); with the measured per-chaining-value spread of the good-pair count (Appendix H: E[K^2]/E[K]^2 = 1.246), E[J(J-1)]/E[J] <= q3r E[K] x 1.246 = 2^-54.61, below 2^-7.5 by a factor 2^47.1; groups (pairs sharing an endpoint) only lower J.
**Support (Appendix H, own C port of the counted claw, 24 seed-drawn chaining values at the package's window R = 9, 2^26 slots, 2^22 scan words each).** Good pairs sharing an endpoint: 0 of 2124. Across chaining values (dispersion chi-square of the per-value counts against the pooled binomial rate, 23 degrees of freedom): C2|C1 (chi-square 27.3, p = 0.24) and G|C1C2 (chi-square 22.5, p = 0.49) are binomial; F7|C1C2G is overdispersed (chi-square 564.0, p = 1.6e-104), as F7 reads the chaining value, and that spread is the factor 1.246 above; C1 is mildly overdispersed (chi-square 45.9, p = 0.003) because C1 (the top three bits of a1 + cE5, a1 = u - h(a0, cv)) clusters in scan order: claws of nearby scan words share u's high bits (lag-1 joint rate 0.04570 against 0.01562 for independent claws). The clustering changes where good pairs occur in the scan, not their expected number per chaining value (u0 is uniform, so every word has the C1 rate 1/8, pooled 0.12499) nor the words of distinct good pairs; at the full 2^32-word scan it averages over 2^10 times more high-bit values of u than in the panel. **Measured on components of the accepted event (registered, Appendix H.2).** Part B of the 10-17 registration, run unchanged on 10-21: the forced-bit events B_t = ((E_t^x & m_t) == v_t) of rows 17..21 (the value-only cells of E17..E21, rates 2^-7, 2^-7, 2^-3, 2^-5, 2^-4), computed on the real compressions of both members of every good pair, ONE = every good pair of one chaining value over all 2^32 scan words (17,576; the registered target 20,000 exceeds what the chaining value has), MANY = 100 good pairs of each of 200 chaining values (20,000), all re-verified by an independent rebuild (0 and 0 bad): against N p_t the largest |z| is 2.43 (ONE) and 1.58 (MANY); ONE against MANY on rates, |z| at most 1.57; dispersion of E19, E20, E21 across the 200 chaining values chi-square 205.2, 190.2, 193.3 on 199 dof (two-sided p 0.734, 0.680, 0.798). The registered ONE-against-MANY formula (n1 - n2)/sqrt(n1 + n2) assumes equal sizes; applied to the unequal sizes it gives |z| up to 3.77, which is the size difference, not dependence (Appendix H.2). No within-chaining-value dependence of these components is detected. Not testable at any sample size and the premise: independence of the rows 17..37 event between good pairs of one chaining value (distinct (W0, W1); acceptance is a function of the pair's W0..W15).

## 9. The q3 of the P1 good pairs (H2-P1)

**The base q3_model = 2^-96.0133** (the A0-variant family on P8, our 9aaf71a2): the sum of two one-sided 99% lower bounds, each computed by the rule registered before its run, on real step-0..37 compressions with disjoint seeds: (i) the level of the printed-cell accepted event: 128 fresh seeds (7001..7128) of 2^28 samples, per-seed value L_s = prefix log2 + log2(exact/2^28), mean -96.3123, sd 0.5563, registered bound mean - t(0.99, 127) sd / sqrt(128) = -96.42816; (ii) the ratio of the relaxed accepted event (the printed row-18 relation E18 = E17 not imposed) to that event: 400 seeds (10001..10400), G = log2(sum Xk / sum X0) = 0.50537, jackknife SE 0.03867, registered bound G - 2.34 SE = 0.41488. Sum -96.01328, rounded down to -96.0133; by the union bound the sum holds with confidence at least 98%. (9aaf71a2 declared a joint linear-scale combination of the same runs, -95.8491, chosen after the runs; it appears in Appendix R.1 and is not used here.) Registrations, method and every per-seed value: Appendix Q (per-seed values) and Appendix R.1 (the two runs as recorded in 9aaf71a2).

**The P1 family, measured (registered, paired).** The same tool (`traillab`, our own C) with the late words W8, W9 drawn from a list of P1 good pairs (a0 uniform in the package's window [9 x 2^26, 10 x 2^26) conditioned on G, a1 uniform over the 53,096,854 values with C1 and C2, W9 = cW9 - a1 and W8 set together) instead of the A0-variant list, on the same seeds as the level run (i): a seed's prefix lineage does not depend on the late words, so each seed gives a paired difference Delta_s = L_s(P1) - L_s(A0). Registered statistic: D = mean Delta_s, D_LB = D - t(0.99, n-1) sd / sqrt(n).

| run (registration) | a0 window | seeds | D (bit) | sd(Delta) | D_LB (99%) | EXACT P1 / A0 |
|---|---|---|---:|---:|---:|---:|
| **R9 (PREREG_P1_Q3_R9, 2026-10-21; declared)** | [9 x 2^26, 10 x 2^26), this package | 36 (7001..7036) | -0.0121 | 0.1321 | **-0.0658** | 367,978 / 372,469 |
| A25 (PREREG_P1_Q3, 2026-10-17; partial, reported) | [0, 2^25) | 76 (7001..7076) | +0.0022 | 0.1347 | -0.0345 | 780,313 / 782,236 |

Every diagnostic is 0 in every seed of both runs. The package charges q3_P1 = q3_model + min(0, D_LB(R9)) = -96.0133 + (-0.0658) = **-96.0791**, so q3r = 2^-96.0791 x 2^32 / 160 = 2^-71.4010; the confidence of the product of the three registered bounds is at least 97% (union bound). Both families run the same step-3b predicate on S's words W10..W15 and differ only in the law of W0..W9; the paired runs measure that difference directly on the printed-cell event; the relaxation ratio (ii) is applied to the P1 family as measured on the A0 family (the relaxed bits are E17, E18 cells, read by both families alike). Registrations, the A25 run's stop and every per-seed value: Appendix P.

## 10. Memory (H6) and advice

The binding whole-computation peak is the author's self-contained Step-1 measurement `279,720 KB = 286,433,280 bytes = 2^28.0936238847...`, rounded upward to `memory_log2_bytes = 28.094`; Appendix R.4 quotes its provenance. The absent `2^27.7542` capped remeasurement is not used. The bucket7 online table subsystem is lower: the exact allocations total 268,468,224 bytes and two pinned full-scale native runs peaked at 270,151,680 and 269,668,352 bytes. Appendix A.15 states the complete binding memory and score. Advice inventory follows.
Advice inventory (bytes): A2..A15 and E6..E15 of both members, 48 words, 192; the cells of rows 16..21 (54 words) 216, their '+' pairs (6 words) 24 and the 35 two-bit conditions (4 bytes each) 140; the 20 heads of S160 80; 19 post-filter and claw constants 76; K and IV (46 words) 184: in all 912 bytes, under 2^10, inside the declared 2^13.

## 11. Allowances and development (H4a, H4b, H4c)

A_C = 2^78 (the characteristic search behind P8), A_S = 2^74 (its Step-1 solve) and DEV = 2^70 (all our development) are charged allowances: upper bounds charged in full. preprocessing = log2(2^78 + 2^74 + 2^70) = 78.09276. Support for A_C and A_S, in this file: (a) the published run log of P8's search (38 solver runs, 230,183 s listed; the author's total under 2^21 core-seconds, quoted with its source hash in Appendix R.4), which at our measured 3,797,484 SHA-256 compressions per second is 2^43.61 units, 34.4 bits under A_C; (b) our own measurements of the same kind of computation (Appendix R.2): a 39-step characteristic derived from scratch with the public tool of [LLW24] in 2^36.04 units and a 38-step pair from the published cells in 2^34.09 units, and the published figures, all at most 2^39.15 units. H4c (DEV): every code execution of this project (10-05 to 10-21), whether or not the procedure reads its output, ran on a 24-thread workstation with one GPU, a 12-thread server and one 32-vCPU cloud machine: at most 68 threads and one GPU for 17 days (1.4688 x 10^6 s), at most 2^40 word operations per thread-second and 2^47 per GPU-second, give at most 2^66.58 + 2^67.49 < 2^68.11 operations = 2^56.7 compressions, under DEV = 2^70 by a factor above 2^13; the recorded development of the A0-variant line is in Appendix R.3.

## 12. Checks

- `selftest`: the P8-pair constants; |S160| = 160; step 3b on the P8 pair accepts (rows 16..21 pass, outputs equal) in 3,014 operations; the counted post-filter chain against the real words (60,000 pairs, 0 mismatches); a run at 2^18 slots and 2^14 scan words: the claws equal an independent sorted-array search, all claws distinct, every claw's real E16 in S160, and the counted operations at most the per-u charge of Section 5 at that size; the ledger and the success bound.
- `p1-online-r38` (organizer): a reduced-size fixture run, not success-probability evidence: 8 seed-drawn chaining values at 2^16 slots and 2^12 scan words, the counted procedure including step 3b on every good pair, every claw checked against the reference search, the real E16 and the real-word post-filters; a pair is returned only if step 3b accepts (none is expected at this size); trial 8 runs step 3b on the P8 pair. `p1-q3-r38`: rows 16..21 counts of every claw at 2^16 slots and 2^13 words. Their counts are reproducible observations consistent with the premises; no rate is inferred from them.
- Development (C port, n0 = 2^22..2^26): claws equal the reference, 0 bad, occupancy 0.63216 and claws/expected 0.99898 at n0 = 2^26 with 2^20 scan words, scan 425.592 operations per u before the packed-access and counter costs (matching the straight-line count).

## Appendix A. The ledger, term by term

| term (operations) | value |
|---|---|
| allowance A_C = 2^78 x C | 824,487,408,977,177,097,149,612,032 |
| allowance A_S = 2^74 x C | 51,530,463,061,073,568,571,850,752 |
| allowance DEV = 2^70 x C | 3,220,653,941,317,098,035,740,672 |
| online work cap V_MAX (charged in full; includes the N_CV first blocks) | 50,420,431,722,137,969,961,783,108,126 |
| overshoot OVER (one chaining value at its maximum) | 1,073,457,123,035,891 |
| final verification FIN = 6 C + 1,600 | 17,968 |
| **N** | **50,519,128,711,573,853,964,925,507,997** |

N / C = 2^83.93719; score 91.94860.

## Appendix P. The paired P1 q3 runs (Section 9): registrations, runs, per-seed values

Tool: `traillab` (our own C; the tool of Appendix R.1) with one addition, a joint list variable (`--var "W8 pairlist W9 @FILE late"`: one list index per late redraw sets W8 and W9 together); regression before the 10-17 registration: the A0 baseline command reproduces the declared seed-7001 log except the thread count; regression before the 10-21 registration: the 10-21 build reproduces the 10-17 A25 seed-7001 log line for line. Model file `chi38p8_a1.txt` = `chi38p8.txt` with the line `except W7 W8 W9`. Lists: `gen_pairs.c` (own code; a1 uniform over the C1&C2 values enumerated exhaustively, a0 uniform in the window conditioned on G by rejection; with R = 0 it reproduces the 10-17 list `pairs25.txt`, SHA-256 6f0ab553...). The baseline per-seed logs are those of the declared level run (Appendix Q, seeds 7001..7128), paired by seed.

**The 10-17 registration** (`PREREG_P1_Q3.md`; SHA-256 and time recorded before its first seed: `efb3100bc19eaf52167cfdcd903dbd496182154d4eea68da070f42b92afc20ff  PREREG_P1_Q3.md
2026-10-17T14:05:12-06:00`), Part A (Part B was not run):

```text
# PREREG_P1_Q3: q3 of the A1-variant family (r38 P1, row-16 sum-claw with A1 free) and pass independence within one chaining value
Written 2026-10-17 (MDT) by the claw_place session on the coordinator's GO, BEFORE the first counted seed; hashed (SHA-256 recorded in prereg_hash.txt with the time) before the run script is started.
Nothing here stages, files or submits anything. Our own code only (traillab is ours; no rival code run, read for execution or compiled).

## 1. Quantity
q3_A1 = the average over the A1-variant family of Pr[accepted event | good pair], where
- a good pair is a chaining value CV1 and (a0, a1) with C1 (top three bits of E5 = a1 + cE5 equal 101b), C2 (W9x = cW9 - a1 in F9), G (W8x = X1(a1) - a0 in G'), and W7x in F7 (F7 enters through the late variable W7, uniform in F7, exactly as in the current attack); a0 uniform in a window [0, 2^LS) (the table of the claw, top bits fixed to 0), a1 uniform over the 53,096,854 values with C1 and C2;
- the event is the one of PREREG_Q3P8_B.md, unchanged: the printed-cell event of chi38p8.txt (rows 16..21 cells, '+' pairs, two-bit conditions, row 19 on signed differences, the relation E18 = E17 INCLUDED), and zero output difference after step 37.
The reference is the declared value of the current attack, q3_base = 2^-96.4282 (mean -96.3123, 128 seeds 7001..7128, PREREG_Q3P8_B.md, SHA-256 eb3310e43e0308e5658631226e09e9ab7d0403de9470dcd3b36545f9fee00f5a), whose per-seed logs are copied in base_logs/ (recomputed here: mean -96.3123, sd 0.5563, bound -96.42814).
The relaxation gain of the current filing (0.4149 bit, E18 = E17 not imposed) is NOT re-measured for the A1 family; it is assumed to transfer (it comes from the prefix lineages and the tail, which are the same objects); this is stated as an assumption in the result.

## 2. Tool and inputs (all hashed in out/hashes_A.txt before the first seed)
- `traillab_p1` = traillab with ONE addition (tl_diff.txt): a joint list variable. `--var "W8 pairlist W9 @FILE late"`: the file holds pairs (W8x, W9x) in hex; one list index is drawn per late redraw by the same single `tl_below` draw as a plain list on W8, and W8, W9 are set together. Everything else is the source of the tool of PREREG_Q3P8_B.md (smc.c, main.c, diff.c byte-identical; traillab.c and traillab.h differ by tl_diff.txt).
- Regression (done before this registration; development, not a counted seed): the baseline command of PREREG_Q3P8_B.md on seed 7001 with the unmodified sources and with traillab_p1 gives output identical to the declared seed_7001.log except the thread count in the header line (reg_diff_base.txt is that one line; traillab_p1 against the unmodified build: reg_diff_p1.txt, 0 lines); 23 s per seed with 8 threads, peak RSS 188 MB.
- `chi/chi38p8_a1.txt` = chi38p8.txt (c47e5ec6...) with the single line `except W7 W8 W9` (W9's printed cell is not a requirement of the path: only its modular difference and ds0(W9) are, and C2 keeps both).
- Lists `lists/pairs25.txt` (a0 window 2^25, n0 = 2^25) and `lists/pairs26.txt` (window 2^26): 1,048,576 pairs each from gen_pairs.c (a1 uniform over the C1&C2 values, a0 uniform in the window conditioned on G by rejection; acceptance 2^-5.995 and 2^-5.981, equal to the exact enumeration 2^-5.9959 and 2^-5.9806). SHA-256: pairs25 6f0ab553..., pairs26 87ebf10c...
- Model = family (famcheck.c, 200,000 draws per list, 0 failures): for every drawn sample the pair rebuilt by traillab (W0..W5 and the chaining value by inverse expansion and step inversion) has A1 = cW9 - W9, A0 = X1(A1) - W8 inside the window, A2..A15 equal to S's in both members, equal chaining values for x and y, and the scouts' construction variantW(CV, A0, A1) (own port) reproduces all 16 message words of both members.
- Development pilot (not counted): dev seed 31001, list 25, full configuration: all diagnostics 0, 23.2 s, peak RSS 192,748 kB.

## 3. Part A: the q3 runs
Command per seed s (one process per seed, one process at a time; the generator streams are indexed by the seed):
`window --chi chi/chi38p8_a1.txt --rows 22 37 --event out --np 8192 --mt 32768 --seeds s --threads 8 --autolist --var "W8 pairlist W9 @lists/pairsLS.txt late"`
Machine rules (coordinator): the cloud box root@108.61.192.253, own folder /root/p1q3, `prlimit --as=268435456` (2^28), `nice -n 10`, `ulimit -s 2048`, `MALLOC_ARENA_MAX=1`, 8 threads, one process at a time, the cores of the r39 tail run left alone (no pinning, no oversubscription), only own processes are started or stopped.
Runs: A25 = list 25, seeds 7001..7128 (the SAME seeds as the declared baseline run, deliberately: the prefix of a seed does not depend on the variant (its random streams and acceptance are independent of the late words), so the baseline and A1 values of a seed share the prefix lineage and the comparison is paired); then A26 = list 26, seeds 7001..7128. Execution order: A25 seeds ascending, then A26 seeds ascending.
Per-seed value L_s = prefix log2 P(rows 7..21) + log2(EXACT / samples) from the log (a dead seed or 0 EXACT counts as -128).
Diagnostics required 0 in every seed (prefix broken by redraw, y-anchor inconsistent, replay mismatches); a non-zero diagnostic in any seed of a run voids that run (reported, not replaced). No look at L values or EXACT counts before all seeds of a run are finished (only rc, diagnostics, timing and memory are monitored); no stopping rule other than the time limit below.
Time limit: the coordinator's 6 h from the GO (13:55 MDT): no new seed is started after 19:20 MDT; the seeds finished in ascending order are used and the run is reported as partial with its n (the one-sided bound then uses t(0.99, n-1)).

Statistics (per run X in {A25, A26}, n seeds):
- Declared stand-alone value q3_X = floor_4dec(mean L - t sd(L)/sqrt(n)), t = 2.3556 for n = 128 (exact quantile t(0.99,127) = 2.3561; the registered value is used, and the exact one is also printed), to be compared with the declared -96.4282.
- Paired difference D_X = mean over seeds of (L_s(X) - L_s(base)) with sd(Delta); D_X^LB = D_X - t sd(Delta)/sqrt(n), D_X^UB = D_X + t sd(Delta)/sqrt(n) (one-sided 99% each); halves 7001..7064 / 7065..7128.
Break-even factors (P1_TEST.md, exact ops): the gain of the claw over the current filter, in bit, for design d at table size n0 is g(d, n0); P1 keeps a gain iff D > -g.
  n0 = 2^25: D2 per-head straddle test, flat 32-bit words 1.179; D2 generic flat 0.993; D2 per-head packed 0.714; D2 generic packed 0.577.
  n0 = 2^26: 2.035; 1.866; 1.594; 1.467.
Decision rules (registered): for the best design of its size (per-head, flat): ALIVE iff D_X^LB > -g_best; DEAD iff D_X^UB < -g_best; otherwise INCONCLUSIVE. The projected r38 score for a design is 93.52785 - g(d, n0) - D_X^LB (declared, conservative) and 93.52785 - g(d, n0) - D_X (mean); it is reported for D2 at n0 = 2^25 (A25) and 2^26 (A26), flat and packed. (time_log2 of the package = 85.43385, score 93.52785, memory unchanged.)
```

Run A25 (cloud machine): files hashed at its start (`2026-10-17T20:05:20+00:00`):

```text
c90989f073c4015cb38d1e64108e0261adff2ca8a47541cab09bb93820ca5e66  traillab_p1
7b396bae063122610e2f277af8b2931d7a6829ff6251d468f4df0ad514f392a0  chi/chi38p8_a1.txt
6f0ab55333ffd1c832d49f9f2c421abf7e75a1463f30215adf602622058802fc  lists/pairs25.txt
87ebf10cc3086da1c5abce88933295075e74a71a33c782c69f3bf9c2b49846ee  lists/pairs26.txt
ff582e64e060db2807d85fbe31b054ef04eea26ed00b46dbcafb66b2c36a7138  sel_members.txt
efb3100bc19eaf52167cfdcd903dbd496182154d4eea68da070f42b92afc20ff  PREREG_P1_Q3.md
```

The run log ends at seed 7076 (`A25 seed 7076 rc=0 rss_kb=192952 2026-10-17T20:32:24+00:00`); seed 7077 has no complete log and A26 never started: the run was stopped on 2026-10-17 at 14:32 MDT, before its registered time limit, for a reason not recorded in the run directory, and the cloud machine was later removed. By the registered rule the seeds finished in ascending order are used, n = 76. Its per-seed L values were first computed on 2026-10-21 from the backed-up logs (no earlier analysis output of A25 exists). It is reported, not used in the charge (its window is [0, 2^25), not this package's).

**The 10-21 registration** (`PREREG_P1_Q3_R9.md`; SHA-256 and time recorded before its first seed: `63f36447ed45ca48fab6cdd0adc4bda52378166a4277f5c0b033a496ae9e44b3 *PREREG_P1_Q3_R9.md
2026-10-21T11:29:42-06:00`):

```text
# PREREG_P1_Q3_R9: paired q3 of the P1 family on the package's own a0 window (LS = 26, R = 9)
Written 2026-10-21 (MDT) before the first counted seed; its SHA-256 and the time are recorded in prereg_hash.txt before run_R9.sh starts. Own code only.

## Quantity
Delta_s = L_s(R9) - L_s(base) per seed s, where L_s = prefix log2 P(rows 7..21) + log2(EXACT / samples) from the traillab log, as in PREREG_P1_Q3.md (10-17, SHA-256 efb3100b...) Part A, with one change: the pair list is lists/pairs26r9.txt (1,048,576 pairs from gen_pairs.c LS = 26, seed 3, R = 9: a0 uniform in [9 x 2^26, 10 x 2^26) conditioned on G, a1 uniform over the C1&C2 values). L_s(base) is the declared 10-17 baseline log of the same seed (levers_1017/claw_place/p1_q3/base_logs/seed_s.log, A0-variant family, 196,608 selected variants).
Tool: traillab_p1 built from the 10-17 sources (byte-identical to the cloud copy that ran A25); regression before this registration (development, not a counted seed): seed 7001 on lists/pairs25.txt reproduces the 10-17 A25_7001.log line for line (out/regress_A25_7001.log). gen_pairs with R = 0 reproduces pairs25.txt (SHA-256 6f0ab553...).

## Run
Seeds 7001, 7002, ... ascending, one process at a time, the A25 command with the R9 list, 8 threads, nice 10, address-space cap 2^28. Hard time limit: no new seed is started 18 minutes after the first seed starts; the seeds finished in ascending order are used (n reported). No L value or EXACT count is looked at before the run ends; only rc, diagnostics and timing are monitored. A non-zero diagnostic in any seed voids the run.

## Statistic (registered)
D = mean Delta_s, sd over seeds, D_LB = D - t(0.99, n-1) sd / sqrt(n) (one-sided 99%). The package charges q3_P1 = q3_model + min(0, D_LB), q3_model = -96.0133 (the registered bound of 9aaf71a2's studies). The 10-17 partial A25 run (76 seeds, a0 window [0, 2^25)) is reported beside it, not pooled.
```

Run R9 (our workstation, WSL, 8 threads, nice 10, `prlimit --as=2^28`): files hashed at its start (`2026-10-21T11:29:46-06:00`):

```text
91751b9a854796626eef34f9db536350e7d94c150ba1c311f6a4240440660abc  traillab_p1
7b396bae063122610e2f277af8b2931d7a6829ff6251d468f4df0ad514f392a0  chi/chi38p8_a1.txt
98994e0a62c423e59a909373356ad7c95aff05ca364acd14241bb9ac18ff11e0  lists/pairs26r9.txt
63f36447ed45ca48fab6cdd0adc4bda52378166a4277f5c0b033a496ae9e44b3  PREREG_P1_Q3_R9.md
```

Run end: `time limit before seed 7037`. Seeds used n = 36, every diagnostic 0, peak resident set of a seed process 198,568 KiB (`/usr/bin/time -v`), under the cap 2^28.

Registered statistic: R9 D = -0.0121, sd 0.1321, t(0.99, 35) = 2.4377, D_LB = -0.0658; A25 D = +0.0022, sd 0.1347, t(0.99, 75) = 2.3771, D_LB = -0.0345.

Per seed (prefix log2 is shared by the pair; L = prefix_log2 + log2(exact / 2^28); Delta = L_P1 - L_A0):

```text
# R9: seed prefix_log2 exact_P1 exact_A0 L_P1 L_A0 Delta
7001 -81.3715 10412 10961 -96.0255 -95.9514 -0.0741
7002 -81.2237 10100 10634 -95.9216 -95.8473 -0.0743
7003 -83.0084 10909 10241 -97.5952 -97.6863 +0.0912
7004 -81.2120 10351 10754 -95.8745 -95.8194 -0.0551
7005 -81.5989 10208 9338 -96.2815 -96.4100 +0.1285
7006 -82.2860 10067 7820 -96.9887 -97.3530 +0.3644
7007 -81.5131 10370 10944 -96.1730 -96.0952 -0.0777
7008 -81.8333 10157 10129 -96.5231 -96.5271 +0.0040
7009 -81.0088 9947 10498 -95.7288 -95.6510 -0.0778
7010 -81.5667 10457 11613 -96.2145 -96.0632 -0.1513
7011 -81.4103 10243 9980 -96.0879 -96.1255 +0.0375
7012 -81.3556 9831 9642 -96.0925 -96.1205 +0.0280
7013 -82.1290 10291 9618 -96.7999 -96.8975 +0.0976
7014 -81.4070 10392 11402 -96.0638 -95.9300 -0.1338
7015 -81.6177 10511 10500 -96.2581 -96.2596 +0.0015
7016 -81.7261 9637 10178 -96.4917 -96.4129 -0.0788
7017 -81.7814 9898 9674 -96.5085 -96.5415 +0.0330
7018 -81.1822 10076 9640 -95.8836 -95.9474 +0.0638
7019 -81.4372 10290 10442 -96.1082 -96.0871 -0.0212
7020 -81.0970 10716 10744 -95.7095 -95.7058 -0.0038
7021 -81.3129 10628 8978 -95.9373 -96.1807 +0.2434
7022 -82.2707 10132 9334 -96.9641 -97.0824 +0.1184
7023 -81.1573 9913 10671 -95.8822 -95.7759 -0.1063
7024 -81.1519 10129 11133 -95.8457 -95.7093 -0.1364
7025 -82.0565 10451 12864 -96.7051 -96.4054 -0.2997
7026 -81.7341 10408 11518 -96.3887 -96.2425 -0.1462
7027 -81.0770 9932 9480 -95.7991 -95.8663 +0.0672
7028 -81.7966 10765 9340 -96.4025 -96.6074 +0.2049
7029 -81.9692 10429 10411 -96.6209 -96.6234 +0.0025
7030 -81.8644 10077 11262 -96.5656 -96.4052 -0.1604
7031 -81.8492 10120 9848 -96.5443 -96.5836 +0.0393
7032 -81.0318 10026 10254 -95.7403 -95.7079 -0.0324
7033 -80.8443 9718 11249 -95.5979 -95.3868 -0.2111
7034 -80.7981 10315 10835 -95.4656 -95.3947 -0.0710
7035 -81.8896 9735 9120 -96.6406 -96.7348 +0.0941
7036 -82.1805 10337 11420 -96.8450 -96.7012 -0.1437
# A25: seed prefix_log2 exact_P1 exact_A0 L_P1 L_A0 Delta
7001 -81.3715 10255 10961 -96.0475 -95.9514 -0.0961
7002 -81.2237 10134 10634 -95.9168 -95.8473 -0.0695
7003 -83.0084 10752 10241 -97.6161 -97.6863 +0.0702
7004 -81.2120 10263 10754 -95.8868 -95.8194 -0.0674
7005 -81.5989 10408 9338 -96.2535 -96.4100 +0.1565
7006 -82.2860 10174 7820 -96.9734 -97.3530 +0.3796
7007 -81.5131 10453 10944 -96.1615 -96.0952 -0.0662
7008 -81.8333 10291 10129 -96.5042 -96.5271 +0.0229
7009 -81.0088 9903 10498 -95.7352 -95.6510 -0.0842
7010 -81.5667 10513 11613 -96.2068 -96.0632 -0.1436
7011 -81.4103 10180 9980 -96.0969 -96.1255 +0.0286
7012 -81.3556 10076 9642 -96.0570 -96.1205 +0.0635
7013 -82.1290 10309 9618 -96.7974 -96.8975 +0.1001
7014 -81.4070 10544 11402 -96.0429 -95.9300 -0.1129
7015 -81.6177 10561 10500 -96.2512 -96.2596 +0.0084
7016 -81.7261 9558 10178 -96.5036 -96.4129 -0.0907
7017 -81.7814 9944 9674 -96.5018 -96.5415 +0.0397
7018 -81.1822 9871 9640 -95.9132 -95.9474 +0.0342
7019 -81.4372 10335 10442 -96.1019 -96.0871 -0.0149
7020 -81.0970 10700 10744 -95.7117 -95.7058 -0.0059
7021 -81.3129 10828 8978 -95.9104 -96.1807 +0.2703
7022 -82.2707 10146 9334 -96.9621 -97.0824 +0.1203
7023 -81.1573 9887 10671 -95.8860 -95.7759 -0.1101
7024 -81.1519 10167 11133 -95.8403 -95.7093 -0.1309
7025 -82.0565 10433 12864 -96.7076 -96.4054 -0.3022
7026 -81.7341 10529 11518 -96.3720 -96.2425 -0.1295
7027 -81.0770 9842 9480 -95.8123 -95.8663 +0.0541
7028 -81.7966 10626 9340 -96.4213 -96.6074 +0.1861
7029 -81.9692 10382 10411 -96.6274 -96.6234 -0.0040
7030 -81.8644 9896 11262 -96.5918 -96.4052 -0.1865
7031 -81.8492 10261 9848 -96.5243 -96.5836 +0.0593
7032 -81.0318 10231 10254 -95.7111 -95.7079 -0.0032
7033 -80.8443 9901 11249 -95.5709 -95.3868 -0.1842
7034 -80.7981 10236 10835 -95.4767 -95.3947 -0.0820
7035 -81.8896 9814 9120 -96.6290 -96.7348 +0.1058
7036 -82.1805 10291 11420 -96.8514 -96.7012 -0.1502
7037 -81.5903 9593 9109 -96.3625 -96.4372 +0.0747
7038 -82.0164 10177 10574 -96.7034 -96.6482 -0.0552
7039 -82.0059 9894 8447 -96.7336 -96.9617 +0.2281
7040 -82.6270 10814 10207 -97.2264 -97.3097 +0.0833
7041 -81.9544 10442 10134 -96.6043 -96.6475 +0.0432
7042 -82.2741 10663 10330 -96.8938 -96.9395 +0.0458
7043 -82.6407 9950 10059 -97.3602 -97.3445 -0.0157
7044 -80.4355 10068 10409 -95.1380 -95.0900 -0.0481
7045 -82.3630 10201 11770 -97.0466 -96.8402 -0.2064
7046 -81.6353 9787 9294 -96.3786 -96.4532 +0.0746
7047 -81.0005 10327 9730 -95.6664 -95.7523 +0.0859
7048 -82.6376 10130 12409 -97.3313 -97.0385 -0.2928
7049 -81.4655 11015 9077 -96.0383 -96.3175 +0.2792
7050 -81.6089 10067 8522 -96.3116 -96.5519 +0.2404
7051 -81.7793 11014 10786 -96.3522 -96.3824 +0.0302
7052 -81.4855 10492 9271 -96.1285 -96.3070 +0.1785
7053 -82.5840 10380 9961 -97.2425 -97.3019 +0.0594
7054 -81.1668 9675 9574 -95.9268 -95.9419 +0.0151
7055 -82.2990 9504 8608 -97.0847 -97.2275 +0.1429
7056 -82.3064 9795 11499 -97.0486 -96.8172 -0.2314
7057 -80.8095 10415 9895 -95.4631 -95.5370 +0.0739
7058 -81.0654 10435 11129 -95.7163 -95.6234 -0.0929
7059 -81.5981 10252 9695 -96.2745 -96.3551 +0.0806
7060 -81.6180 10819 9934 -96.2167 -96.3398 +0.1231
7061 -81.2075 10266 10783 -95.8819 -95.8110 -0.0709
7062 -82.0255 9784 9999 -96.7693 -96.7379 -0.0314
7063 -80.8514 10470 10990 -95.4974 -95.4275 -0.0699
7064 -81.5843 10261 9838 -96.2594 -96.3202 +0.0607
7065 -81.8012 10664 12344 -96.4207 -96.2097 -0.2111
7066 -82.2935 10623 10158 -96.9186 -96.9832 +0.0646
7067 -81.6483 10367 11042 -96.3086 -96.2176 -0.0910
7068 -81.6822 10816 11170 -96.2813 -96.2349 -0.0465
7069 -81.4176 10536 9738 -96.0546 -96.1682 +0.1136
7070 -81.7532 10503 10521 -96.3947 -96.3922 -0.0025
7071 -81.1694 10423 9811 -95.8219 -95.9092 +0.0873
7072 -81.9733 9602 8147 -96.7442 -96.9812 +0.2371
7073 -81.4528 10724 12212 -96.0642 -95.8768 -0.1875
7074 -81.3789 10417 10598 -96.0322 -96.0074 -0.0249
7075 -81.3163 9796 11188 -96.0583 -95.8666 -0.1917
7076 -81.3546 10458 10805 -96.0023 -95.9552 -0.0471
```

## Appendix H. The H3-P1 panel (Section 8)

### H.1 Post-filter panel

Own C port of the counted claw (`p1h3.c` = `p1claw.c` of the development runs plus uncounted statistics), window R = 9, 2^26 slots, 2^22 scan words, per-head two-window probing, one chaining value per seed (seeds 201..224, drawn from the seed by the port's xorshift); every claw checked against S160 and its real E16 (0 bad in every chaining value). Per chaining value: claws, claws/expected, c1, c1c2, c1c2g, all4 (good pairs), good pairs sharing a0 / sharing u, consecutive-claw pairs with C1 on both / pairs.

```text
201 6628654 0.99991 827510 81689 1318 128 0/0 302427/6628653
202 6630952 1.00034 827579 81945 1319 57 0/0 302899/6630951
203 6626709 0.99971 828260 82029 1327 58 0/0 302537/6626708
204 6624032 0.99936 828399 82123 1395 31 0/0 302744/6624031
205 6629301 1.00019 827356 81873 1345 112 0/0 302427/6629300
206 6617535 0.99837 826944 82326 1307 26 0/0 302146/6617534
207 6631055 1.00050 831255 81940 1351 149 0/0 303977/6631054
208 6632574 1.00032 827515 82299 1338 133 0/0 302252/6632573
209 6632019 1.00041 829099 81621 1320 123 0/0 303312/6632018
210 6630528 1.00034 831155 82701 1401 33 0/0 304514/6630527
211 6634502 1.00084 829229 82007 1278 30 0/0 302983/6634501
212 6629415 0.99993 827229 81883 1350 82 0/0 302001/6629414
213 6630076 1.00016 828498 82155 1384 53 0/0 302855/6630075
214 6625587 0.99950 827465 81391 1333 64 0/0 302148/6625586
215 6629162 0.99993 829059 81972 1365 185 0/0 303292/6629161
216 6625254 0.99930 826302 81516 1380 71 0/0 301815/6625253
217 6631400 1.00029 827845 82166 1313 147 0/0 302381/6631399
218 6627704 0.99978 828096 81756 1360 70 0/0 303083/6627703
219 6627623 0.99967 829233 82021 1301 145 0/0 303156/6627622
220 6629981 1.00025 828941 82357 1352 83 0/0 303101/6629980
221 6630931 1.00025 827999 81276 1325 130 0/0 302464/6630930
222 6629148 1.00008 829622 82322 1375 92 0/0 304229/6629147
223 6630633 1.00024 830893 82339 1259 58 0/0 304091/6630632
224 6625932 0.99968 829184 81997 1299 64 0/0 303065/6625931
```

Dispersion across the 24 chaining values (chi-square of the per-value counts against the pooled binomial rate, 23 degrees of freedom): C1 of claws 45.9 (p = 0.003), C2 of C1 27.3 (p = 0.243), G of C1C2 22.5 (p = 0.490), F7 of C1C2G 564.0 (p = 1.6e-104). Spread of the good-pair rate per claw: E[r^2]/E[r]^2 = 1.246 (r = all4/claws per chaining value; Poisson noise included, so an upper estimate).

### H.2 Part B: rows 17..21 forced-bit events within one chaining value (registered)

Registration of the run (SHA-256 and time recorded before the first counted pass: `da3a88cb4efe43e0c73100a0612b37cebeaa14605477d6c88edd74dcd8f917cb *PREREG_P1_PARTB_1021.md
2026-10-21T12:11:24-06:00`); Part B's text is Section 4 of PREREG_P1_Q3.md, reproduced in Appendix P.

```text
# PREREG_P1_PARTB_1021: Part B of PREREG_P1_Q3.md (10-17, SHA-256 efb3100b...), run on 2026-10-21
Written and hashed before the first counted pass. Part B was registered on 10-17 and never run (the cloud machine stopped during Part A). This run uses Part B's population, events, tests and decision rule UNCHANGED (PREREG_P1_Q3.md Section 4): ONE = cv seed 5001, 20,000 good pairs; MANY = cv seeds 6001..6200, 100 good pairs each; n0 = 2^25, window R = 0; tools p1pass.c (SHA-256 1327337a...) and p1ana.c (17d7e44d...), byte-identical to the 10-17 copies; every pass re-verified by p1ana (one failure voids the part).
Changes, all non-statistical: machine (our workstation, WSL, 8 threads, nice 10, prlimit --as=2^28) and date; time limit: each part under `timeout 1080` s (a part that times out is reported as not run).
Development before this text (not counted): one 500-pass run of p1pass on dev cv seed 31001 (timing, 6 s), analysed by p1ana (0 bad).
Tests (as registered): (i) each B_t count of ONE and of MANY against N p_t, z = (n - Np)/sqrt(Np(1-p)); (ii) ONE against MANY, z = (n1 - n2)/sqrt(n1 + n2); (iii) over-dispersion across the 200 chaining values of MANY for t = 19, 20, 21, chi2 = sum_i (n_i - 100p)^2/(100p(1-p)), 199 dof, two-sided p. Dependence DETECTED iff any |z| > 3.5 (15 tests) or any dispersion p < 0.001 or > 0.999.
```

Files hashed at the start (`2026-10-21T12:11:27-06:00`):

```text
1327337a2f59de317b87f6e68953346f99b9d0360786ba2dcf36eaa22b98e8f1  p1pass.c
17d7e44de5a8c9c2804529febbb28b6ffd1743ef99ab42715142d761ed37bd72  p1ana.c
a67db508dbd5a45de261d76c869413dcf62fabf8fa535ac62e073283c9937bed  sconsts.h
c47e5ec605a25ae03df29ada92f68c3462468262dc30730a1e201de335c8a14d  chi/chi38p8.txt
da3a88cb4efe43e0c73100a0612b37cebeaa14605477d6c88edd74dcd8f917cb  PREREG_P1_PARTB_1021.md
```

Run records: `ONE rc=0 132908 kB 2026-10-21T12:20:59-06:00; MANY rc=0 132716 kB 2026-10-21T12:30:40-06:00`.

Registered tests (p1ana output, `tests_B.txt`):

```text
ONE passes 17576 bad 0 | MANY passes 20000 bad 0, chaining values 200
E17: ONE 139 (exp 137.3, z +0.14) MANY 156 (exp 156.2, z -0.02) ONE-MANY z -0.99
E18: ONE 109 (exp 137.3, z -2.43) MANY 151 (exp 156.2, z -0.42) ONE-MANY z -2.60
E19: ONE 2244 (exp 2197.0, z +1.07) MANY 2504 (exp 2500.0, z +0.09) ONE-MANY z -3.77
E20: ONE 584 (exp 549.2, z +1.51) MANY 649 (exp 625.0, z +0.98) ONE-MANY z -1.85
E21: ONE 1125 (exp 1098.5, z +0.83) MANY 1304 (exp 1250.0, z +1.58) ONE-MANY z -3.63
E19 dispersion chi2 205.2 on 199 dof, two-sided p 0.734
E20 dispersion chi2 190.2 on 199 dof, two-sided p 0.680
E21 dispersion chi2 193.3 on 199 dof, two-sided p 0.798
max |z| 3.77; RESULT: DEPENDENCE DETECTED
```

ONE against MANY on rates, z = (n1/N1 - n2/N2) / sqrt(p(1-p)(1/N1 + 1/N2)): E17 +0.12, E18 -1.57, E19 +0.72, E20 +0.42, E21 -0.47.

## Appendix Q. Per-seed values of the base q3 runs (Section 9) and their registrations

- Level run, seeds 7001..7128: PREREG_Q3P8_B.md eb3310e43e0308e5658631226e09e9ab7d0403de9470dcd3b36545f9fee00f5a (hashed 2026-10-17 17:02:24 UTC; first seed 17:02:44 UTC); it references PREREG_Q3P8.md b1a2d290a3aad1b2c224be407ec9796e1fbf55d9ff2ea9bec9783aab76c0ae97. Tool traillab 17425aaa624561ceeb641977d72d86f6f4c1b8e57c6a05b7c82ad9ed1d12d485.
- Ratio run F2, seeds 10001..10400: PREREG_X1.md (Amendment 5) 628921f950e45c2c72f67c0d76af6011d664a4ca28ee0fe33813bde23f5dfd30 (hashed 2026-10-17 12:16:41 UTC; first seed 12:16:56 UTC).

Level: L_s = prefix_log2 + log2(exact_count / 2^28); registered bound mean(L) - t(0.99, 127) sd(L) / sqrt(128) = -96.42816. Ratio: G = log2(sum Xk / sum X0) = 0.50537, jackknife SE 0.03867, registered bound G - 2.34 SE = 0.41488.

~~~
# level run (PREREG_Q3P8_B): seed,prefix_log2,exact_count  (samples 2^28 per seed; L = prefix_log2 + log2(exact_count/2^28))
L,7001,-81.3715,10961
L,7002,-81.2237,10634
L,7003,-83.0084,10241
L,7004,-81.212,10754
L,7005,-81.5989,9338
L,7006,-82.286,7820
L,7007,-81.5131,10944
L,7008,-81.8333,10129
L,7009,-81.0088,10498
L,7010,-81.5667,11613
L,7011,-81.4103,9980
L,7012,-81.3556,9642
L,7013,-82.129,9618
L,7014,-81.407,11402
L,7015,-81.6177,10500
L,7016,-81.7261,10178
L,7017,-81.7814,9674
L,7018,-81.1822,9640
L,7019,-81.4372,10442
L,7020,-81.097,10744
L,7021,-81.3129,8978
L,7022,-82.2707,9334
L,7023,-81.1573,10671
L,7024,-81.1519,11133
L,7025,-82.0565,12864
L,7026,-81.7341,11518
L,7027,-81.077,9480
L,7028,-81.7966,9340
L,7029,-81.9692,10411
L,7030,-81.8644,11262
L,7031,-81.8492,9848
L,7032,-81.0318,10254
L,7033,-80.8443,11249
L,7034,-80.7981,10835
L,7035,-81.8896,9120
L,7036,-82.1805,11420
L,7037,-81.5903,9109
L,7038,-82.0164,10574
L,7039,-82.0059,8447
L,7040,-82.627,10207
L,7041,-81.9544,10134
L,7042,-82.2741,10330
L,7043,-82.6407,10059
L,7044,-80.4355,10409
L,7045,-82.363,11770
L,7046,-81.6353,9294
L,7047,-81.0005,9730
L,7048,-82.6376,12409
L,7049,-81.4655,9077
L,7050,-81.6089,8522
L,7051,-81.7793,10786
L,7052,-81.4855,9271
L,7053,-82.584,9961
L,7054,-81.1668,9574
L,7055,-82.299,8608
L,7056,-82.3064,11499
L,7057,-80.8095,9895
L,7058,-81.0654,11129
L,7059,-81.5981,9695
L,7060,-81.618,9934
L,7061,-81.2075,10783
L,7062,-82.0255,9999
L,7063,-80.8514,10990
L,7064,-81.5843,9838
L,7065,-81.8012,12344
L,7066,-82.2935,10158
L,7067,-81.6483,11042
L,7068,-81.6822,11170
L,7069,-81.4176,9738
L,7070,-81.7532,10521
L,7071,-81.1694,9811
L,7072,-81.9733,8147
L,7073,-81.4528,12212
L,7074,-81.3789,10598
L,7075,-81.3163,11188
L,7076,-81.3546,10805
L,7077,-80.6791,9328
L,7078,-80.8915,11047
L,7079,-81.4507,9590
L,7080,-82.0555,14439
L,7081,-80.9598,11567
L,7082,-81.7905,10128
L,7083,-81.679,10807
L,7084,-81.9692,9793
L,7085,-81.6493,10218
L,7086,-82.2675,12192
L,7087,-81.8574,10311
L,7088,-81.8021,10686
L,7089,-82.1201,10557
L,7090,-82.0163,10293
L,7091,-82.0332,9893
L,7092,-82.596,10243
L,7093,-81.966,9400
L,7094,-82.0325,10797
L,7095,-81.0504,10307
L,7096,-81.7908,11427
L,7097,-80.9781,9547
L,7098,-81.7915,10918
L,7099,-81.1962,10154
L,7100,-81.5516,11064
L,7101,-81.2837,10561
L,7102,-81.6309,10878
L,7103,-83.0446,7809
L,7104,-80.5101,11040
L,7105,-81.2544,10202
L,7106,-80.9157,11310
L,7107,-82.1957,11088
L,7108,-80.5423,10580
L,7109,-81.0267,10121
L,7110,-82.5614,13019
L,7111,-81.806,9196
L,7112,-80.6369,10583
L,7113,-81.8203,9696
L,7114,-81.6757,11446
L,7115,-81.3278,11038
L,7116,-82.0319,11295
L,7117,-81.8272,9505
L,7118,-81.5061,9582
L,7119,-81.2448,10519
L,7120,-82.0173,10523
L,7121,-81.6134,10193
L,7122,-81.1283,10174
L,7123,-81.7614,8065
L,7124,-82.6067,10212
L,7125,-81.5096,10874
L,7126,-81.5263,10348
L,7127,-82.6019,11354
L,7128,-82.0752,8305
# ratio run F2 (PREREG_X1 Amendment 5): seed,X0,Xk  (linear per-seed estimates x 2^96 of the base and relaxed events; dead seed = 0)
R,10001,0,0.9281277
R,10002,1.006835,1.006835
R,10003,0,0
R,10004,2.442087,2.442087
R,10005,0,0
R,10006,0.6885427,0.6885427
R,10007,0,0.7482195
R,10008,1.245815,2.294923
R,10009,0,1.183819
R,10010,1.862596,1.862596
R,10011,0,0
R,10012,1.151722,1.151722
R,10013,1.94911,2.479701
R,10014,1.325574,2.833167
R,10015,0,0
R,10016,0.8232038,0.8232038
R,10017,0.6216205,0.6216205
R,10018,0,0
R,10019,1.495375,1.495375
R,10020,0.6288989,1.459242
R,10021,1.571213,2.901789
R,10022,0,0
R,10023,0.9025339,1.785012
R,10024,2.00611,2.00611
R,10025,0,0.3887652
R,10026,0.7026895,0.7026895
R,10027,0.3110605,0.3110605
R,10028,0,0.951372
R,10029,1.429517,2.694451
R,10030,0,0.5839011
R,10031,1.341414,2.534174
R,10032,0,0
R,10033,0.5726884,2.013086
R,10034,0,0
R,10035,1.50335,1.50335
R,10036,0,0
R,10037,2.556076,2.556076
R,10038,0,0
R,10039,1.212667,1.212667
R,10040,2.064467,2.064467
R,10041,0,1.388778
R,10042,1.054881,1.708392
R,10043,0.4714009,0.4714009
R,10044,0.9854011,1.305656
R,10045,1.351585,2.391001
R,10046,2.249487,2.249487
R,10047,0,0.9651581
R,10048,0.7392302,0.7392302
R,10049,1.118467,1.118467
R,10050,0,0
R,10051,0,0
R,10052,0,0
R,10053,0,0
R,10054,0,0
R,10055,0,0
R,10056,0.7389259,1.218363
R,10057,0,1.07037
R,10058,1.886001,1.886001
R,10059,0,0
R,10060,1.570131,2.492149
R,10061,1.636427,1.636427
R,10062,0,0
R,10063,1.085199,1.085199
R,10064,0.8541374,0.8541374
R,10065,0,0
R,10066,2.885537,2.885537
R,10067,0.9890864,0.9890864
R,10068,0,0.8081806
R,10069,0,0
R,10070,1.052451,1.052451
R,10071,0,0.6342957
R,10072,0.5469453,0.5469453
R,10073,3.244172,3.244172
R,10074,1.279995,1.279995
R,10075,2.1942,2.1942
R,10076,1.020947,1.020947
R,10077,0,0
R,10078,3.151282,3.151282
R,10079,0,0
R,10080,0,0
R,10081,2.201495,2.89953
R,10082,0.5322888,1.337605
R,10083,0,0.8123574
R,10084,0,0
R,10085,2.64376,3.594222
R,10086,0,0.7097606
R,10087,0.7130816,1.124734
R,10088,1.391683,2.205282
R,10089,1.329652,1.329652
R,10090,0,0
R,10091,1.298209,1.298209
R,10092,0,0
R,10093,0,0
R,10094,0,0
R,10095,1.591822,1.959952
R,10096,3.2257,3.2257
R,10097,0,0.6350302
R,10098,0,0.970039
R,10099,0.6547256,1.521203
R,10100,1.154524,1.154524
R,10101,1.020515,1.583899
R,10102,0,0
R,10103,0.9602013,0.9602013
R,10104,0.7797537,1.716424
R,10105,1.538413,1.538413
R,10106,3.458623,5.426605
R,10107,2.434904,2.434904
R,10108,1.023864,2.370468
R,10109,0.9788162,1.630528
R,10110,0.7121826,1.808033
R,10111,0,1.930493
R,10112,1.639378,2.329072
R,10113,0.4325059,0.4325059
R,10114,2.794344,2.794344
R,10115,1.900645,2.916681
R,10116,0.7634711,2.406752
R,10117,0.5696623,0.5696623
R,10118,0,0
R,10119,0,0
R,10120,2.87533,3.38362
R,10121,1.796416,1.796416
R,10122,0,0.8290385
R,10123,0,0
R,10124,0.8308606,0.8308606
R,10125,2.060964,2.997765
R,10126,0.9226925,0.9226925
R,10127,2.332842,2.332842
R,10128,1.282092,2.54916
R,10129,0.8846184,1.6155
R,10130,0,0
R,10131,0,0
R,10132,2.3076,2.772958
R,10133,0.4514547,3.235425
R,10134,0,0
R,10135,0.8592967,0.8592967
R,10136,0,0.3811694
R,10137,0,0
R,10138,0,0
R,10139,0,0.6220679
R,10140,0.5361133,1.337548
R,10141,0.6334565,2.556449
R,10142,0.7898796,0.7898796
R,10143,1.265516,1.265516
R,10144,0.7144834,0.7144834
R,10145,0,0
R,10146,1.364234,1.364234
R,10147,1.272447,1.272447
R,10148,1.282024,1.282024
R,10149,1.014554,1.014554
R,10150,0,0
R,10151,2.364591,2.364591
R,10152,0.997314,0.997314
R,10153,0.898366,0.898366
R,10154,0,0
R,10155,2.316413,2.316413
R,10156,0,0
R,10157,1.609583,1.609583
R,10158,0.4877785,0.4877785
R,10159,0,0.4124104
R,10160,1.639941,1.639941
R,10161,0.645703,0.645703
R,10162,0.6496905,0.6496905
R,10163,1.175697,1.175697
R,10164,1.117999,1.117999
R,10165,1.990315,2.954545
R,10166,0,0.7581706
R,10167,0.45893,1.506102
R,10168,0.822564,1.512529
R,10169,0.9417453,0.9417453
R,10170,0.8425465,0.8425465
R,10171,0.6311242,1.893373
R,10172,0.8915027,0.8915027
R,10173,0.3543698,0.7273906
R,10174,1.550933,2.288198
R,10175,1.291029,1.291029
R,10176,1.588314,2.155809
R,10177,1.004757,2.561424
R,10178,0,1.485154
R,10179,0,1.579497
R,10180,0,0
R,10181,0.4121239,0.8725833
R,10182,0.6859813,0.6859813
R,10183,0,1.071299
R,10184,1.250952,1.250952
R,10185,1.015728,1.764917
R,10186,0.9319799,0.9319799
R,10187,0,0.9663574
R,10188,0.8575195,1.560736
R,10189,1.698156,1.698156
R,10190,0.7354357,0.7354357
R,10191,0,0
R,10192,0.9995321,0.9995321
R,10193,0,0
R,10194,0.5484237,0.5484237
R,10195,0,0
R,10196,0,0.8796423
R,10197,0.4949941,0.4949941
R,10198,0,0.8647544
R,10199,0.7214206,1.655423
R,10200,1.070582,1.070582
R,10201,0.869085,0.869085
R,10202,0.6591974,1.576126
R,10203,1.779813,1.779813
R,10204,2.702336,3.149586
R,10205,0,0
R,10206,0.9042895,1.829131
R,10207,0,0
R,10208,0,0
R,10209,0.3365096,0.3365096
R,10210,1.012305,1.012305
R,10211,0.5767287,0.5767287
R,10212,0,0
R,10213,0.6680543,0.6680543
R,10214,0.6922278,0.6922278
R,10215,0.9099687,1.420616
R,10216,0,1.38764
R,10217,0,0
R,10218,1.496756,1.496756
R,10219,0,0
R,10220,0.9929262,0.9929262
R,10221,0,0.6654608
R,10222,1.923922,1.923922
R,10223,0.7430274,1.21219
R,10224,0,0.5555327
R,10225,0,0.4499109
R,10226,0.8496979,0.8496979
R,10227,0,0
R,10228,2.269728,3.547865
R,10229,0,0
R,10230,1.94005,2.69329
R,10231,0.7683553,2.180666
R,10232,0,0
R,10233,1.958021,1.958021
R,10234,1.400893,1.400893
R,10235,0.7864194,1.795363
R,10236,1.055981,1.055981
R,10237,0,1.328123
R,10238,0.8052687,0.8052687
R,10239,0.656664,0.656664
R,10240,1.424754,1.424754
R,10241,0,0
R,10242,1.072733,1.072733
R,10243,0,0
R,10244,1.816788,2.488107
R,10245,0,0
R,10246,2.877305,2.877305
R,10247,0,0.6983921
R,10248,1.90508,1.90508
R,10249,3.109547,3.616943
R,10250,1.527085,2.03363
R,10251,1.018428,1.018428
R,10252,1.189139,1.596345
R,10253,2.12171,2.704482
R,10254,2.05652,2.05652
R,10255,1.780576,2.506531
R,10256,1.420919,1.420919
R,10257,0,0
R,10258,0,0
R,10259,0,1.443166
R,10260,0,0
R,10261,2.95313,2.95313
R,10262,1.794076,2.755849
R,10263,1.092247,1.092247
R,10264,1.456213,1.456213
R,10265,2.334258,2.334258
R,10266,1.210093,2.006017
R,10267,0.8712293,0.8712293
R,10268,0,0
R,10269,0.8064632,0.8064632
R,10270,1.860444,1.860444
R,10271,1.851992,2.791298
R,10272,1.722623,3.829385
R,10273,0,0
R,10274,0,0.8632901
R,10275,0,0
R,10276,0.7539742,0.7539742
R,10277,1.716739,1.716739
R,10278,1.106052,1.106052
R,10279,0.5252586,1.099981
R,10280,0.9213367,0.9213367
R,10281,0,0
R,10282,0,0
R,10283,0,0
R,10284,0,0
R,10285,2.187207,2.187207
R,10286,0.6482929,0.6482929
R,10287,0,0.6342823
R,10288,1.194657,2.577183
R,10289,0,0
R,10290,0,0
R,10291,0,0.8552015
R,10292,0.5968955,0.5968955
R,10293,0,0
R,10294,0.6249789,0.6249789
R,10295,0,0
R,10296,0.5325172,1.549792
R,10297,0.8903379,1.56663
R,10298,0.8646637,1.388403
R,10299,1.673583,1.673583
R,10300,0,0
R,10301,0.8582208,0.8582208
R,10302,0,0
R,10303,0,0
R,10304,1.566598,1.566598
R,10305,0,0.3820462
R,10306,1.923467,3.827455
R,10307,1.621908,2.13469
R,10308,1.144444,2.624871
R,10309,0.6941518,1.775121
R,10310,2.04408,2.765306
R,10311,1.011446,1.769069
R,10312,1.272745,1.272745
R,10313,0,0
R,10314,3.019173,3.575648
R,10315,2.327982,2.327982
R,10316,0.6296267,0.6296267
R,10317,1.577948,1.577948
R,10318,1.771852,1.771852
R,10319,0,0.4219317
R,10320,0,0
R,10321,1.728547,1.728547
R,10322,0,2.723642
R,10323,0,0.9323999
R,10324,0,0
R,10325,0.6485064,0.6485064
R,10326,0.5688346,1.57504
R,10327,0,0
R,10328,0,0
R,10329,1.51718,2.128316
R,10330,2.833669,2.833669
R,10331,0.711626,0.711626
R,10332,1.726907,1.726907
R,10333,3.083568,3.083568
R,10334,0,0
R,10335,0.6742766,0.6742766
R,10336,1.481735,3.825395
R,10337,1.532606,2.198957
R,10338,1.065839,1.756073
R,10339,2.267965,2.267965
R,10340,0,0.45208
R,10341,2.279857,3.116672
R,10342,1.068132,1.786737
R,10343,0,0
R,10344,0,1.41416
R,10345,0.9472289,1.703616
R,10346,1.281463,1.281463
R,10347,0,0.6487455
R,10348,1.08904,1.08904
R,10349,0,1.039966
R,10350,0.7064984,1.530331
R,10351,0,0
R,10352,2.816989,2.816989
R,10353,0,0.6575495
R,10354,0,0.7888445
R,10355,0.9892791,0.9892791
R,10356,0.611843,0.611843
R,10357,0.6763418,1.578131
R,10358,1.198657,1.198657
R,10359,1.540558,3.195618
R,10360,1.151237,1.151237
R,10361,1.692953,1.692953
R,10362,0,0
R,10363,0.9422333,0.9422333
R,10364,1.244869,1.244869
R,10365,0,0
R,10366,0,0.6058029
R,10367,1.231212,1.776718
R,10368,0.7100559,0.7100559
R,10369,1.334651,2.026511
R,10370,0,0
R,10371,0.9955977,1.519359
R,10372,0.806232,2.539254
R,10373,0,0
R,10374,0.6464383,0.6464383
R,10375,0,0
R,10376,3.111893,3.111893
R,10377,0.9036278,1.486385
R,10378,1.23934,1.23934
R,10379,0.8546721,0.8546721
R,10380,1.022096,1.753287
R,10381,0,0
R,10382,0,0
R,10383,0.9909144,0.9909144
R,10384,0,1.019004
R,10385,1.877494,1.877494
R,10386,2.059244,2.059244
R,10387,1.554703,1.554703
R,10388,0,0
R,10389,0,0
R,10390,1.594233,1.594233
R,10391,0,0
R,10392,0,1.4196
R,10393,0,1.519391
R,10394,0.9854348,0.9854348
R,10395,0.6165324,1.37731
R,10396,0,0.8508295
R,10397,0,0
R,10398,0,0
R,10399,2.015821,2.015821
R,10400,0,0.7052653
~~~

## Appendix R. Records of the A0-variant line (reproduced from the proof of our 9aaf71a2; section numbers inside refer to that proof; script sources omitted; in R.1 to R.3 the word procedure is replaced by procedure)

### R.1 The q3 runs of q3_model (9aaf71a2 Sections 7.4, 7.5, Appendices A.11, A.12)

### 7.4 The preregistered measurement of q3 (H2's declared value)

*Tool.* `traillab` (our own C program, written in this project with Claude Code; the tool that measured fb176310's declared value; not shipped: the experiment sources are limited to 65,536 bytes) estimates rates of a 38-step characteristic by sequential Monte Carlo on real compressions: every sample is a chaining value and W0..W15 of both members with the real message expansion, the state is replayed from the words (0 replay mismatches are required), rows 16..21 are the prefix (E-driven: E_t^x chosen, W_t from it, W0..W5 solved by the inverse expansion; 8,192 particles, 256 proposals per particle per row) and rows 22..37 the window, with the late words of the procedure redrawn for every window sample (W6 uniform, W7 uniform in F7, W8 from a list). For each window sample it counts EXACT (zero output difference after step 37). With `--autolist` the row-16 stage is exact: the tool enumerates the E16 values that pass row 16 under the prefix conditions (160 values, enumerated over 2^24 candidates; the same set as Section 6) and weights the stage 160/2^32. Its model of P8 is our transcription `chi38p8.txt` (the cells of Section 3; anchor row 15: S's rows 12..15 held); its prefix conditions are exactly the tests of rows 16..21 of the accepted event (cells, '+' pairs, two-bit conditions keyed at the larger row; row 19 signed only). Per seed, log2 q3 = prefix log2 P(rows 16..21) + log2 rate(EXACT) (the tool labels its prefix "rows 7..21", from the lowest row with a condition; rows 7..15 are held at S and pass with probability 1, so the prefix is rows 16..21). The tool reproduces fb176310's preregistered value exactly with the same seeds (2^-97.6619 for the published characteristic) and passed its validation suite (48 of 48 quick known-answer tests: exact counts of the row-16 sets and of F7, the flip tables, digests of the pairs).

*Preregistration of the declared run* (`PREREG_Q3P8_B.md`, Appendix A.12; written and hashed, SHA-256 eb3310e43e0308e5658631226e09e9ab7d0403de9470dcd3b36545f9fee00f5a, 2026-10-17 11:02:24 MDT, before the first seed, which started at 11:02:44 MDT): the quantity, the tool and the inputs of the earlier run below (binary 17425aaa..., `chi38p8.txt` c47e5ec6..., `sel_members.txt` ff582e64...); 128 fresh seeds 7001..7128, each 2^28 window samples (8,192 particles x 32,768), one process per seed (the generator streams are indexed by the seed, so a seed gives the same counts in one process or in a multi-seed process), W8 drawn from the list of the 196,608 selected variants (`--var "W8 a0list @sel_members.txt late"`), row 16 exact. Per-seed value L_s as above (a dead seed or 0 EXACT counts as -128); declared value q3_base = the one-sided 99% Student lower bound over the 128 values, mean - t sd / sqrt(128) with t = 2.3556 as registered, rounded down to 4 decimals (the seed is the cluster), over these 128 seeds only (the seeds of the earlier run are not pooled); halves 7001..7064 / 7065..7128; diagnostics required 0 (a non-zero diagnostic in any seed voids the run); no interim look, no stopping rule, all 128 seeds used. Use rule: if the run is not void and q3_base > -96.5755, the next filing uses q3_model = q3_base x 2^0.4149 (the gain of Section 7.5, unchanged); otherwise nothing changes.

*Results* (cloud machine, 2026-10-17 17:02:44 to 17:45:42 UTC; every diagnostic 0: prefix broken by the redraw 0, y-anchor inconsistent 0, replay mismatches 0; dead seeds 0; 1,326,458 EXACT events, at least 7,809 per seed):

| run | statistic (log2) | mean | seed sd | declared 99% lower bound | half 1 / half 2 |
|---|---|---:|---:|---:|---|
| **128 seeds 7001..7128 (declared)** | q3 (rows 16..21 prefix + EXACT) | -96.3123 | 0.5563 | **-96.4282** | -96.3328 / -96.2918 |
| 32 seeds 5001..5032 (earlier run, Appendix A.9) | q3 (rows 16..21 prefix + EXACT) | -96.3251 | 0.5774 | -96.5755 | -96.3137 / -96.3365 |

The 128 per-seed values, the script that computes the declared value from the logs and its output are in Appendix A.12. With the exact Student quantile t(0.99, 127) = 2.3561 (the registered value is 2.3556) the bound is -96.42816, which rounds down to the same -96.4282.

*The earlier run* (`PREREG_Q3P8.md`, Appendix A.9; hashed with its run script before its first seed, 2026-10-14 15:00:08 MDT): 32 fresh seeds 5001..5032 of the same tool, inputs and command, declared bound over its 32 values with t(0.99, 31) = 2.4528: mean -96.3251, bound -96.5755, 326,084 EXACT events, every diagnostic 0. It was repeated under an address-space cap of 2^28 bytes (Section 13.4) and every per-seed output is identical. The 128-seed run was registered after it, with the use rule above (its bound replaces the earlier one if it is higher); The 32 seeds are not used in the bound below (one multi-seed process; pooled with the 128 seeds the bound would move by +0.0075 bit).

*Estimator and bound (analysis of the registered run; the registered statistic, the Student bound of the mean of L_s, is 2^-96.4282 and stays in the table).* The value of a seed is an estimate of q3 that is unbiased on the linear scale: the prefix is the product of the stage means of a sequential Monte-Carlo sampler with a fixed schedule and multinomial resampling of equally weighted children (the stage-16 factor 160/2^32 is exact), the last factor is the fraction of the seed's 2^28 window samples with zero output difference, drawn from the resampled particles, and a seed whose population dies counts 0 (none of the 128 did). The quantity bounded is q3, so the statistic is the arithmetic mean of the 128 values 2^(L_s) (the mean of L_s is lower by the Jensen gap 0.1035 bit). Result: mean 2^-96.2088, coefficient of variation 0.3820, standard error 0.0487 bit; one-sided 99% Student lower bound (t = 2.3561) 2^-96.3285 (rounded down). Bootstrap-t 2^-96.3210, BCa 2^-96.3193 and the lognormal (Cox) interval 2^-96.3252 agree within 0.01 bit; the L_s are normal (Shapiro p = 0.72) and a simulated lognormal population with this spread gives the Student bound a coverage of 99.5%. The level is confirmed by estimators that do not share its seeds: the 400 seeds of Section 7.5 give 2^-96.2567 (standard error 0.072 bit) for the same event with a different sampler structure; the replica of Section 7.3 (a lower-bound estimator) has mean 2^-96.3095; 1a695f0b's estimator gave 2^-96.3683.

### 7.5 The relation E18 = E17 is not imposed: the measurement of the gain (F2)

**What changes.** Besides the cells, the accepted event of Section 6.1 used to impose the '+' relation of the printed row 18, E18 = E17 on bits 24, 23, 15 (mask 01808000; `PQ[18]`). This filing does not test it: the event uses `PQE`, which equals `PQ` except `PQE[18] = 0`. Every pair the earlier event accepts is still accepted (one test was removed), every accepted pair is still a collision (Lemma 6.1), and the cost does not rise: the counted path of step 3b loses the 4 operations of the removed test, 2,825 operations per row-16 pass instead of 2,829, and the ledger charges every row-16 pass at this longest path (Section 11).

**Why it adds collisions.** The output difference of E20 must vanish: dE20 = dE16 + dS1(E19) + dCH(E19, E18, E17) (dW18 = dW20 = 0 on the path). E19 differs at bits 24, 23, 15, and CH(E19, E18, E17) is then the same for both members at those bits exactly when E18 = E17 there; that is the printed relation. If E17[24,23] = 10 and E18[24,23] = 01 instead, dCH changes by -2^24 + 2^23 = -2^23, and dS1(E19), a signed sum of the nine powers 2^b, b in {31, 30, 22, 18, 17, 13, 12, 9, 4} (the sign of each is a bit of S1(E19x)), absorbs it through the other sign of its term 2^22, a change of 2^23. Example, one sample of the tool (it rebuilds every sample from the 16 message words and the chaining value and replays both members, Section 7.4): E16x = cb3ad724, E17x = 2b08cc08, E18x = 02dbd786, E18y = 02dfd796, E19x = e65badfa, E19y = e7db2dfa, E20x = E20y; dE16 = c03dee00, dS1(E19) = 404211f0, dCH = ff800010, and the three add to 0 mod 2^32 (checked in Python). The extra patterns need particular values of the E17 bits, which the printed row 17 leaves free, so the added mass differs from lineage to lineage; the gain below is the mean over the lineages that the sampler draws.

**Estimator and its check.** `traillab window --rows 17 21 --event out --relax NAME=OPS` (the tool of Section 7.4, binary 17425aaa...) proposes E17..E21 uniformly inside the union of the cell events of the printed set and of the named relaxation (the relaxation contains the printed set), builds every final sample from message words, replays both members, and counts on the SAME samples J0 = (zero output difference after step 37 and the printed cells and relations of rows 17..21) and Jk = (zero output difference and the relaxed cells of rows 17..21). Prefix and carrier are common, so q3(relaxed event) / q3(printed event) = sum_s w_s Jk_s / sum_s w_s J0_s with the seed weights w_s = 2^(prefix_s + carrier_s) printed on the "prefix log2 ... window carrier log2 ..." line of each seed. Check on a known answer, run first (V0, seeds 9001..9008, 2^27 final samples each): fb176310's law (chi38.txt) with the arm A of D250 (the four E19 patterns and the E20 tie) gives 1.9917 bit (jackknife SE 0.0835), against +2.0368 bit measured separately by paired prefix arms (D250, 32 seeds): 0.045 bit apart.

**Scan of the other relaxations of rows 17..21.** Nine more relaxations were measured alone on four seeds (9401..9404, 2^23 final samples each): the value-only cells of E17 (7 bits), E18 (5), E20 (5), E21 (3), the relations E17 = E16 and E20 = E19, the two-bit conditions of A17, E18 and E21. In every one the EXACT samples of the relaxation were exactly the EXACT samples of the printed set (J0 = Jk in every seed, 143 to 1,360 EXACT samples per arm; the added regions of E20 = E19 (half of the mass) and of E21 (7/8 of the mass) hold no EXACT sample among about 4 million samples per seed). Only the relation E18 = E17 adds collisions, and only through its bits 24 and 23 (in F2 the bits 24 and 23 alone give the same counts as all three, and bit 15 alone adds none; in the 19 seeds of the second launch of the earlier 32-seed design, bit 24 alone and bit 23 alone added none either).

**Preregistration and result (F2).** `PREREG_X1.md` (SHA-256 of the registered text and of the scripts in Appendix A.11), written before the first seed of the run, fixes: 400 fresh seeds 10001..10400, `--np 8192 --mt 2048` (2^24 final samples per seed), one process per seed, `prlimit --as=2^28`, `MALLOC_ARENA_MAX=1`, 2 MiB thread stacks, 8 threads, nice 10, on the cloud machine; the statistic G = log2(sum_s w_s Jk_s / sum_s w_s J0_s) with a delete-one-seed jackknife standard error over all 400 listed seeds (a seed whose population dies at a window stage is an entry with zero weight, not dropped); the rule: if LB99 = G - 2.34 SE exceeds 0.10 bit the declared gain is LB99 rounded down to 4 decimals. Three earlier launches of a first design (32 seeds at 2^27 samples each) preceded it: the first two crashed in the tool in the seed after the first dead seed (a defect of the tool, worked around by one process per seed), the third (one process per seed) was stopped after 19 seeds because the lineage lottery, not the sample count, limits the precision (its pooled gain over the 19 seeds was +0.75 bit, SE 0.37); the design was changed to many small seeds before any F2 seed was run, and the numbers of those launches are not used.
Result: of 400 seeds 306 had a live population (94 died at stage 20, as in the printed-cell runs), all diagnostics 0 (prefix broken by redraw, y-anchor inconsistent, replay mismatches); pooled J0 = 143169 and Jk = 203960 EXACT samples; **G = 0.5054 bit (ratio 1.420), jackknife SE 0.0387, LB99 = 0.4149 bit**; the unweighted pooled value is 0.5106. Seeds with J0 = 0 and Jk > 0: 53; with Jk = J0 > 0: 154; with Jk > J0 > 0: 99. The arm with bits 24 and 23 only has the same counts as the arm with all three bits (J0 143169, Jk 203960); the arm with bit 15 alone has Jk = J0 (143169 against 143169). Peak resident memory of a seed process: at most 219,048 KiB = 2^27.74 bytes under the cap 2^28.
**Declared gain 0.4149 bit.**

**Use.** log2 q3_model = log2 q3_base + log2 R, with q3_base the level of Section 7.4 (seeds 7001..7128) and R the ratio of this section (seeds 10001..10400). The two estimates come from different runs and seeds, so their errors are independent and the standard error of the sum is the root of the sum of squares. Estimate -96.2088 + 0.5054 = -95.7035; standard error sqrt(0.0487^2 + 0.0387^2) = 0.0622 bit; one-sided 99% lower bound -95.7035 - 2.34 x 0.0622 = -95.8491 (rounded down; 2.34 is t(0.99) at the about 300 effective degrees of freedom). **q3_model = 2^-95.8491.** Checks: a joint bootstrap over the seeds of both runs (200,000 draws) has its 1% quantile at -95.8467; in bootstrap worlds built on the observed seeds the rule covers 99.1%; the two separate 99% bounds multiplied (2^-96.3285 x 2^0.4149 = 2^-95.9136, confidence at least 98%) are shown for comparison; the 400 seeds of this section also estimate q3 of the relaxed event directly, 2^-95.7513 (standard error 0.060 bit, one-sided 99% Student bound 2^-95.8982). The H3 measurement of Section 13.5, the replica of Section 7.3 and its calibration are those of the printed-cell event, as before.

**Not covered.** (a) H3 was not re-measured on successes with E18 different from E17: its successes come from the replica, which does not propose them; the premise counts row-16 passes only. (b) The ratio is a ratio of two Monte-Carlo estimates of one tool over the lineages that tool draws (a few clusters per seed); its precision is that of the 400 seeds. (c) The extra patterns were measured with W8 from the 196,608 selected variants and the real message expansion, like q3 itself; no collision was built by the counted program in a run (none is expected at our scale). (d) The relaxations of other rows were measured on four seeds each (the scan above), at the power stated there.


### A.11 The shared-carrier measurement of Section 7.5: registration, scripts and counts

Files of the run, in the order they were written (SHA-256 recorded in `prereg_x1_hashes.txt` at the time of writing; the line after each file name is the hash of the file as it stands here; the registered text `PREREG_X1.md` is below with its amendments, each dated before the runs it governs; clock times are MDT, 2026-10-17):

```text
628921f950e45c2c72f67c0d76af6011d664a4ca28ee0fe33813bde23f5dfd30  PREREG_X1.md
516e6141e9bb080cfa5a274b739925056b8f6988356b44de58c0856872e3e035  run_x1.sh
e3f1f0c71f21ff46a8a2f663ee76f6a516a04589c95d12c9a3705d66960ce386  run_x1b.sh
d5ab95030d741acb66382787b09f4cb8d6d4d1298f11bf39cfb8594a0e6b4e57  run_x1c.sh
84127cca6451b33e29951f7ee77417f66725b225d8c8236037d2fb363497b41c  run_x1e.sh
572d9d25cb7b9281306649643b9e19b0f0a9a01012a37c0d38f641c7f2440a50  run_x2.sh
131f93f1f062581758c4375ab1e14e1508cac53d2a0d0b0560d30cd69863a4eb  anal_x1.py
f75225137f48d435c671089026f7407acc4e79d85cde20471546e78e3d12739a  anal_x2.py
```

The binary is the one of Appendix A.9 (SHA-256 17425aaa624561ceeb641977d72d86f6f4c1b8e57c6a05b7c82ad9ed1d12d485), the model file `chi38p8.txt` (c47e5ec6...), `chi38.txt` (0ad7712e...) and `sel_members.txt` (ff582e64...) those of Section 13.4, on the cloud machine in `/root/r38x`. `run_x1.sh` ran the stage-M part (its ratio-stage part was cancelled, see the amendments), `run_x1b.sh` ran V0 (its F1 launch crashed), `run_x1c.sh` and `run_x1e.sh` are the crashed and the stopped launches, `run_x2.sh` is F2.

#### A.11.1 The registered text with its amendments (`PREREG_X1.md`)

```text
# PREREG_X1: P8 value-cell relaxations of rows 17..21 by the shared-carrier ratio (written before any counted seed)

Written 2026-10-17 05:53 MDT (11:53 UTC) by the R38X session; the first run started 05:55:16 MDT. Nothing here stages, files or submits anything.

## Why

The package d7fdf556 (R38P8S, a0hoist38.py) already has the exact collision event of R37R: `row_check` returns True for every row >= 22 (a0hoist38.py line ~499),
step3b computes rows 16..37 and accepts iff the eight words A34..A37, E34..E37 of the two members are equal, and the preregistered q3 of Section 7.4 counts
"zero output difference after step 37" on the prefix of rows 16..21 (the log lines "cells rows 22..37 ... rate 0.5" and "EXACT" of Appendix A.9 show it).
D783-STACK (A: four E19 patterns + E20 tie, B: exact output event over the rows 22..37 cells) was measured on chi38 (fb176310's law). On P8 its B part is already in
the event and its A part is the identity: P8's row 19 is signed differences only (no value-only bit) and its E20 '+' pair is the tie. So no D783 factor transfers.
What the exact-event idea still allows for P8 is to stop checking value-only cells of rows 17..21 (the "last checked row" idea of R37R, applied to cells instead of rows):
a dropped cell adds mass to the prefix and may or may not keep colliding. Earlier tests (F2-1014-R38-P8-ROW20-21-RELAX: r20 -0.066 +- 0.162, r21 -0.027 +- 0.013;
F3-1014-R38-P8-ROW18-RELAX: +0.77 +- 0.70) used separate prefix arms and were limited by SMC noise (sd 0.3 to 1.4 per seed). This run uses the tool's own
shared-carrier mode, which counts the base cells and each relaxation on the SAME samples, so the prefix noise cancels in the ratio.

## Estimator (traillab, our own C; binary sha256 17425aaa624561ceeb641977d72d86f6f4c1b8e57c6a05b7c82ad9ed1d12d485, the one of Appendix A.9)

`window --rows a 21 --event out --relax "<name>=<ops>"`: the E-driven window stages a..21 propose E_t uniformly inside the union of the cell events of the base and of the named relaxation(s)
(the relaxations only drop conditions, so the base cells are contained in every relaxation); every final sample is checked against the base cells and against each relaxation
on rows a..21 and against "zero output difference after step 37". With J0 = samples that are EXACT and follow the base cells on rows a..21 and Jk = samples that are EXACT and follow relaxation k on rows a..21:
**q3(relaxation k) / q3(base) = Jk / J0** (same prefix, same carrier, the carrier mass cancels), so the gain in bits is log2(Jk / J0). Window rows a..21 carry the base cells of the printed model
(chi38p8.txt; rows 22..37 carry only the cell E22[29] = 0, which is not part of the counted event and is not tested here).

## Validation on a known answer (must pass before any P8 number is used)

V0: chi38.txt (fb176310's characteristic), `--rows 19 21`, relaxation A = "dropv E19 30040e32 ; dropv E20 20000000 ; lin E20[29]^E19[29]=0" (the arm of D250, research/prereg_D250_r38.md,
whose separately-run paired value is +2.0368 bit, 99% lower bound +1.9534). Seeds 9001..9008, np 8192, mt 16384 (2^27 final samples per seed), 8 threads.
Rule: V0 passes iff the pooled gain log2(sum JA / sum J0) is within 0.35 bit of +2.0368 (the jackknife standard error is reported). If it does not pass, the shared-carrier ratio is not used for P8 and the scan is void.

## Stage M, the mass screen (added 05:54 MDT, before any counted seed; the second smoke below motivated it)

Disclosed smoke 2 (P8, rows 18..21, arm r18v, seed 1, np 8192, mt 1024, 8,388,608 final samples, 328 EXACT): EVERY final sample follows the base cells ("cells rate 1.000000", J0 = Jk = 328),
although the carrier accepts E18 on the union of base and r18v: the relaxed-only E18 values die at rows 19..21, so the five value-only bits of E18 add no surviving mass in this seed.
Stage M runs each arm ALONE, seeds 9401..9404, np 8192, mt 1024 (2^23 final samples per seed), 8 threads, the flags below, and records the base fraction b = (final samples following the base cells) / (final samples)
and J0, Jk. It is a quick look only (about 5 minutes) and decides nothing: **all ratio runs below are executed for every arm whatever stage M shows** (about 40 minutes), because the closure criterion
is the one that uses the collisions themselves: Jk = J0 over all seeds (no EXACT sample outside the base cells) bounds the gain of the arm: with J0 EXACT samples and none outside, the relaxed-only EXACT share is below 3 / J0 (rule of three, 95%) of J0, i.e. under log2(1 + 3/J0) bit.

## The ratio stage (P8, chi38p8.txt, `--autolist`, `--var "W8 a0list @sel_members.txt late"`, event out, np 8192, mt 16384, 8 threads, seeds listed)

Relaxation ops are the tool's (README): dropv (value-only bits), dropq (a '+' relation to the row above), dropx2 (the two-bit conditions touching the named word). Masks come from chi38p8.txt:
E17 value-only 40421a80, E17 '+' to E16 00040010; E18 value-only 40421200, E18 '+' to E17 01808000; E20 value-only 01848010, E20 '+' to E19 20000000; E21 value-only 01808000; two-bit conditions touching A17 (7), E18 (4), E21 (3).

| run | rows | arms (name = ops) | seeds |
|---|---|---|---|
| R18a | 18..21 | r18v = dropv E18 40421200 | 9101..9116 |
| R18b | 18..21 | r18q = dropq E18 01808000 ; r18x = dropx2 E18 | 9101..9116 |
| R17a | 17..21 | r17v = dropv E17 40421a80 | 9201..9216 |
| R17b | 17..21 | r17q = dropq E17 00040010 ; r17x = dropx2 A17 | 9201..9216 |
| R2021 | 20..21 | r20v = dropv E20 01848010 ; r21v = dropv E21 01808000 ; r21x = dropx2 E21 ; r20q = dropq E20 20000000 | 9301..9316 |

Every listed seed is run and reported; none is dropped, replaced or rerun. Runs under `prlimit --as=268435456` with `MALLOC_ARENA_MAX=1` (the caps of the package's development record), `nice -n 10`,
at most 8 threads, on the cloud box; peak resident memory by `/usr/bin/time -v`. Order: stage M, R18a, R18b, R17a, R17b, R2021, V0 (V0 is needed only if some arm has Jk > J0).

## Statistic and rule

Per arm, per run: G = log2( sum_s Jk_s / sum_s J0_s ) over the seeds (ratio of sums; the seed is the cluster); SE = delete-one-seed jackknife standard error of G; LB99 = G - t(0.99, n-1) SE
(t = 2.998 for 8 seeds, 2.602 for 16). `anal_x1.py` (written with this file, unchanged afterwards) prints these from the logs.
An arm is **alive** iff LB99 > +0.10 bit. This screening run does not declare any q3 value. An alive arm is then bisected by subsets of its masks and confirmed by a second preregistered run of 32
fresh seeds before any program or proof change; a dead arm (LB99 <= 0.10) is recorded as "no gain seen at this power" with its G and SE, not as a proof of zero.
Diagnostics required 0: prefix broken by redraw, y-anchor inconsistent, replay mismatches; a nonzero diagnostic voids that seed (reported, not replaced).
Disclosed, not used: smoke run on chi38 (seed 1, np 2048, mt 1024): J0 30, JA 80.

## Amendment 1 (06:02 MDT, 12:02 UTC; after stage M and before any further counted seed)

Stage M was run as registered (seeds 9401..9404; logs out/M_*.log, hashes of the registered files in prereg_x1_hashes.txt). Result: for every arm except r18q the final samples that follow the printed
cells and the EXACT samples of the relaxation are the same samples in every seed (Jk = J0, per seed): r17v, r17q, r17x (window from row 17), r18v, r18x, r20v (cells rate 1.0000), r20q (cells rate 0.49..0.52, so the added
region has half of the mass, and ZERO EXACT samples among its ~4 million samples per seed) and r21v, r21x (cells rate 0.12..0.13, again zero EXACT in the added region). Those arms add no collision: closed as
"no extra EXACT sample seen" with Jk = J0 exactly; the gain bound is log2(1 + 3/J0) with J0 = 1,100 to 1,700 per arm over the four seeds, under 0.005 bit.
The one arm with extra EXACT samples is r18q (drop the '+' relation E18 = E17 on bits 24, 23, 15): seed 9403 had cells rate 0.309 and EXACT 69 (cells) against 295 (relaxation); seed 9404's population died at stage 20 and
seeds 9401, 9402 had no extra samples (the result depends on the E17 value of the lineage, because this run starts its window at row 18). A local debug build (scratchpad copy of the source with one print statement, same estimator; used only
to look at samples, no number from it is used) showed an extra EXACT sample with E17x = 2b08cc08 (bits 24, 23 = 1, 0), E18x = 02dbd786 (bits 24, 23 = 0, 1), E19x = e65badfa, E19y = e7db2dfa, E20x = E20y: delta E16 + delta S1(E19) + delta CH(E19, E18, E17) = 0 mod 2^32,
checked by hand with Python (the CH change -2^24 + 2^23 at bits 24 and 23 is absorbed by the other sign of one S1 term), so these are real collisions of the 38-step compression, rebuilt from the message words by the tool's replay.
R18a was started and stopped by the run owner after 4 minutes (arm r18v, closed by stage M); its partial log is not used. Runs R18b, R17a, R17b, R2021 are cancelled (their arms are closed by stage M).

**F1 (the declared measurement)**: `window --chi chi/chi38p8.txt --rows 17 21 --event out --np 8192 --mt 16384 --threads 8 --autolist --var "W8 a0list @sel_members.txt late"`, seeds 9501..9532 (32 fresh seeds, 2^27 final samples each),
arms (all subsets of the primary arm, same samples): **q18 = dropq E18 01808000 (primary)**, q18h = dropq E18 01800000, q18b15 = dropq E18 00008000, q18b24 = dropq E18 01000000, q18b23 = dropq E18 00800000.
Statistic: G = log2(sum Jk / sum J0) pooled over the seeds, delete-one-seed jackknife SE, LB99 = G - 2.4528 SE (anal_x1.py). The primary arm is the only one declared; a subset arm can only have a smaller G (it is contained in q18) and is reported for information.
Rule: if LB99(q18) > 0.10 bit the declared gain is floor_4dec(LB99(q18)) and the package may take q3_model = -96.5755 + that gain (the sum of two one-sided 99 percent bounds, stated as such); otherwise nothing changes.
**V0** (validation of the shared-carrier ratio on the known answer, chi38 arm A, seeds 9001..9008) is run after F1; the F1 number is used only if V0 passes (within 0.35 bit of +2.0368).
Diagnostics required 0 (prefix broken by redraw, y-anchor inconsistent, replay mismatches); a seed with a dead population is reported and counted in the pooled sums with its zero counts (it contributes J0 = Jk = 0 and is not replaced), and the count of dead seeds is stated.

## Amendment 2 (06:05 MDT; before the rerun, after the first F1 launch stopped)

The first F1 launch (06:02:27 MDT, 8 threads, `prlimit --as=268435456`) ended with SIGSEGV (rc 139) in seed 9504 after 69 s (peak resident memory 202,296 KiB): at window stage 19 every proposal is accepted
(2,097,152 of 2,097,152 records of 24 bytes, copied and sorted for the resampling) and the 8 default thread stacks of 8 MiB add 64 MiB of address space, so the 2^28 cap was hit. Its seeds 9501 and 9502 completed and seed 9503 died at stage 20
(389 of 2,097,152 proposals accepted at stage 20 in the neighbouring seeds); nothing from that log is used. The rerun is the identical command with `ulimit -s 2048` (2 MiB stacks, 16 MiB of address space for 8 threads), same cap, same 32 seeds;
the generator streams are indexed by (seed, stage, particle), so the seeds reproduce whatever the thread count, and the rerun is a continuation of the registered run, not a replacement of seeds. The rerun starts after V0 finishes (8 cores in use at a time).
Seeds whose population dies are reported and kept in the pooled sums as zero counts (as registered). The package-side statement "every development execution whose output is used ran under `prlimit --as=2^28`" holds for the rerun.

## Result of V0 and Amendment 3 (06:08 MDT; F1b is running, started 06:07:00)

V0 (chi38, arm A, seeds 9001..9008, all diagnostics 0): G = +1.9917 bit, jackknife SE 0.0835 (pooled J0 10,599, JA 42,154) against the separately run, paired value +2.0368 of D250: difference 0.045 bit < 0.35. **V0 passes**; the shared-carrier ratio is a valid estimator of the gain of a prefix relaxation.

**M2 (scouting; no number from it enters a package)**: whether anything else becomes droppable on top of q18. After F1b, nine single runs, each window rows 17..21, np 8192, mt 4096 (2^25 final samples per seed), 8 threads, seeds 9601..9608, `--autolist`, W8 list as above,
two arms per run: `base2 = dropq E18 01808000` and `base2+X`, X in {dropv E18 40421200, dropx2 E18, dropv E17 40421a80, dropq E17 00040010, dropx2 A17, dropv E20 01848010, dropq E20 20000000, dropv E21 01808000, dropx2 E21}
(the second arm is the ops of the first plus the ops of X, separated by ';'). Statistic G2 = log2(sum J(base2+X) / sum J(base2)) with the jackknife SE (anal_x1.py with `cells` read as base2 is NOT used; the two arm lines are compared by anal_pair.py written with this amendment).
An X with G2 > 0.1 and G2 > 3 SE is recorded as a lead, to be confirmed by a registered run before any use; the others are recorded as closed on top of q18 with their G2 and SE.

## Amendment 4 (06:09 MDT; after the second crash, before the rerun)

F1b (identical command, 2 MiB stacks) ended again with SIGSEGV (rc 139) in seed 9504, one minute after its start, with seed 9503 dead at stage 20 just before it, exactly as in the first F1 launch. The same thing did not happen in stage-M run M_r18q, where the dead seed was the last one.
So the crash is not memory: the tool crashes on the first seed AFTER a seed whose population died ("window stage 20: dead", then "seed N: no samples", then the next seed). (Our reading of the cause: the dead-seed return path frees the particle arrays; not investigated further; the tool is not part of any package.)
Remedy that changes no number: one process per seed (`--seeds s` for each s), same flags, same cap; the generator streams are indexed by (seed, stage, particle), so each seed gives the same counts in its own process (checked on seeds 9501 and 9502: 2661 / 2936 and 3717 EXACT in F1 and F1b, 6378 together, identical).
The M2 runner of Amendment 3 was started by mistake behind F1b and stopped after its first run (M2_r18v, finished, rc 0); everything of M2 is rerun per seed. F1 is rerun as F1c: seeds 9501..9532, one process per seed, then the logs are concatenated in seed order for anal_x1.py.
Dead seeds stay in the pooled sums with zero counts, as registered. The number of dead seeds is reported.

## Amendment 5 (06:16 MDT; F2 replaces F1c as the declared measurement; before any F2 seed)

What F1c showed in its first 14 seeds (log out/F1c.log, kept; stopped at the seed it had reached when this amendment was written, not for its value): the counts are dominated by one to three lineage clusters per seed.
A local debug build (scratchpad copy of the tool with a tally of the E17 and E18 bits 24, 23, 15 over the EXACT samples; no number from it is used) shows, in seed 9506 and in seed 9507, EXACT samples only of the pattern E17[24,23] = 10, E18[24,23] = 01 (all of them off the printed cells),
in seed 9501 only of printed-cell patterns (E17 = E18 on those bits: 01 and 11), in seed 9505 of both. The window carrier keeps only about 130 to 500 of 2,097,152 proposals at stage 20, so a seed has few distinct lineages and J0 (the printed-cell EXACT count) is 0 in some seeds
while Jk is large. The ratio of pooled counts is a ratio of heavy-tailed sums: its jackknife SE after 6 live seeds was 0.6 bit, and the final-sample noise is not the issue (about 5,000 EXACT samples per seed), the lineage lottery is. So many cheap seeds beat few expensive ones.
**F2 (the declared measurement)**: the same command as F1 with `--mt 2048` (2^24 final samples per seed), 400 fresh seeds 10001..10400, one process per seed, arms q18 (primary), q18h and q18b15 (information), same cap and flags, 8 threads.
Statistic (linear scale, which is the scale on which the estimate of a probability is unbiased): with w_s = 2^(prefix_s + carrier_s) (the two numbers printed on the "[s] prefix log2 ... window carrier log2 ..." line of seed s; w_s = 0 for a dead seed),
G = log2( sum_s w_s Jk_s / sum_s w_s J0_s ), delete-one-seed jackknife SE over all 400 listed seeds (dead seeds are entries with zero weight), LB99 = G - 2.34 SE (anal_x2.py, written with this amendment). The unweighted pooled value is printed for comparison.
Rule: if LB99(q18) > 0.10 bit the declared gain is floor_4dec(LB99(q18)); then q3_model = -96.5755 + declared gain (product of two one-sided 99% bounds, stated so). Otherwise nothing changes. Every listed seed is run; the number of dead seeds is stated; diagnostics must be 0.
M2 (scouting of compound relaxations) is dropped: it would need the same number of seeds and its arms are closed one by one by stage M.
```

#### A.11.2 `run_x1.sh`

(script omitted: not required for the record; the registered text and outputs are kept)

#### A.11.3 `run_x1b.sh`

(script omitted: not required for the record; the registered text and outputs are kept)

#### A.11.4 `run_x2.sh`

(script omitted: not required for the record; the registered text and outputs are kept)

#### A.11.5 `anal_x1.py`

(script omitted: not required for the record; the registered text and outputs are kept)

#### A.11.6 `anal_x2.py`

(script omitted: not required for the record; the registered text and outputs are kept)

#### A.11.7 Counts

V0 (chi38, arm A, seeds 9001..9008; per seed: J0 = EXACT samples on the printed cells of rows 19..21, JA = EXACT samples on the arm A): 9001: 1600 / 5139; 9002: 1210 / 5203; 9003: 1376 / 5624; 9004: 1515 / 4967; 9005: 1230 / 5419; 9006: 999 / 5391; 9007: 1228 / 5016; 9008: 1441 / 5395. Sums 10599 / 42154.

Stage M (P8, each arm alone, seeds 9401..9404, 2^23 final samples per seed; per arm J0 = Jk per seed, the arm r18q has the seeds listed as J0 / Jk, "dead" = the population died at stage 20):

```text
r18v  9401: 393/393  9402: 319/319  9403: 336/336  9404: 312/312
r18x  9401: 264/264  9402: 199/199  9403: 334/334  9404: 248/248
r17v  9401: 330/330  9402: 331/331  9403: 316/316  9404: 299/299
r17q  9401: 348/348  9402: 309/309  9403: 272/272  9404: 329/329
r17x  9401: 287/287  9402: 360/360  9403: 336/336  9404: 375/375
r20v  9401: 298/298  9402: 336/336  9403: 326/326  9404: 313/313
r20q  9401: 131/131  9402: 153/153  9403: 155/155  9404: 129/129
r21v  9401: 35/35  9402: 28/28  9403: 41/41  9404: 39/39
r21x  9401: 39/39  9402: 31/31  9403: 28/28  9404: 44/44
r18q  9401: 470/470  9402: 165/165  9403: 69/295   (seed 9404 dead)
```

F2 (seeds 10001..10400; per seed: log2 w = prefix + carrier, J0, Jq18; q18h and q18b15 are in the summary line above; a dead seed has no line):

```text
10001 -81.74 0 794
10002 -81.70 839 839
10004 -80.65 984 984
10006 -81.69 570 570
10007 -81.54 0 557
10008 -80.02 323 595
10009 -80.84 0 542
10010 -80.11 513 513
10012 -81.70 961 961
10013 -80.11 540 687
10014 -79.98 335 716
10016 -81.57 627 627
10017 -81.71 522 522
10019 -80.58 574 574
10020 -80.67 256 594
10021 -79.73 333 615
10023 -80.64 360 712
10024 -80.68 824 824
10025 -81.57 0 295
10026 -81.55 527 527
10027 -81.63 247 247
10028 -81.70 0 789
10029 -79.73 304 573
10030 -81.74 0 499
10031 -80.14 379 716
10033 -80.17 165 580
10035 -80.72 632 632
10037 -80.18 739 739
10039 -81.60 942 942
10040 -80.74 883 883
10041 -80.60 0 540
10042 -80.60 410 664
10043 -81.69 389 389
10044 -80.15 280 371
10045 -80.19 394 697
10046 -80.13 631 631
10047 -81.55 0 725
10048 -81.71 619 619
10049 -80.67 455 455
10056 -80.66 299 493
10057 -81.76 0 925
10058 -80.69 780 780
10060 -80.02 407 646
10061 -80.65 657 657
10063 -80.59 418 418
10064 -81.72 718 718
10066 -80.06 769 769
10067 -81.87 926 926
10068 -81.67 0 657
10070 -81.50 761 761
10071 -81.90 0 608
10072 -81.73 463 463
10073 -79.99 825 825
10074 -81.64 1019 1019
10075 -80.13 614 614
10076 -81.69 845 845
10078 -79.65 634 634
10081 -79.68 451 594
10082 -80.77 232 583
10083 -81.57 0 616
10085 -79.76 573 779
10086 -81.62 0 559
10087 -80.80 317 500
10088 -80.13 390 618
10089 -81.64 1060 1060
10091 -81.66 1048 1048
10095 -80.20 467 575
10096 -80.07 869 869
10097 -81.75 0 547
10098 -81.63 0 770
10099 -80.68 269 625
10100 -81.58 881 881
10101 -80.66 413 641
10103 -81.68 790 790
10104 -80.69 323 711
10105 -80.64 613 613
10106 -78.90 413 648
10107 -80.09 663 663
10108 -80.07 276 639
10109 -80.65 392 653
10110 -80.70 297 754
10111 -80.84 0 883
10112 -80.11 454 645
10113 -81.65 347 347
10114 -80.25 852 852
10115 -79.63 376 577
10116 -80.10 210 662
10117 -81.63 452 452
10120 -79.65 577 679
10121 -80.15 509 509
10122 -81.68 0 681
10124 -81.65 666 666
10125 -80.17 594 864
10126 -81.66 749 749
10127 -79.99 593 593
10128 -79.64 256 509
10129 -80.63 351 641
10132 -79.70 481 578
10133 -79.64 90 645
10135 -81.65 692 692
10136 -81.78 0 334
10139 -81.80 0 555
10140 -80.51 196 489
10141 -80.05 168 678
10142 -81.58 604 604
10143 -81.71 1063 1063
10144 -81.68 588 588
10146 -80.49 489 489
10147 -80.68 522 522
10148 -81.67 1048 1048
10149 -81.63 805 805
10151 -80.67 960 960
10152 -81.68 819 819
10153 -80.63 355 355
10155 -80.70 961 961
10157 -80.58 616 616
10158 -81.73 413 413
10159 -81.70 0 342
10160 -80.69 675 675
10161 -81.90 615 615
10162 -81.63 514 514
10163 -81.56 888 888
10164 -81.62 879 879
10165 -80.10 547 812
10166 -81.58 0 581
10167 -80.62 181 594
10168 -80.80 366 673
10169 -81.71 790 790
10170 -81.68 692 692
10171 -80.72 267 801
10172 -81.80 795 795
10173 -80.74 152 312
10174 -80.03 406 599
10175 -81.62 1018 1018
10176 -80.22 473 642
10177 -80.14 284 724
10178 -80.66 0 599
10179 -80.76 0 686
10181 -80.62 162 343
10182 -81.66 556 556
10183 -81.70 0 890
10184 -81.64 1001 1001
10185 -80.70 423 735
10186 -81.70 777 777
10187 -81.63 0 764
10188 -80.63 339 617
10189 -80.68 695 695
10190 -81.65 590 590
10192 -81.66 807 807
10194 -81.66 443 443
10196 -81.90 0 843
10197 -81.89 471 471
10198 -81.60 0 669
10199 -80.79 319 732
10200 -81.53 794 794
10201 -81.64 695 695
10202 -80.66 266 636
10203 -80.67 726 726
10204 -79.73 574 669
10206 -80.77 396 801
10209 -81.80 301 301
10210 -81.67 827 827
10211 -81.66 468 468
10213 -81.51 488 488
10214 -81.76 600 600
10215 -80.69 376 587
10216 -80.65 0 557
10218 -80.79 664 664
10220 -81.66 801 801
10221 -81.76 0 578
10222 -80.74 825 825
10223 -80.80 331 540
10224 -81.79 0 493
10225 -81.60 0 350
10226 -81.57 647 647
10228 -80.05 602 941
10230 -80.09 528 733
10231 -80.09 210 596
10233 -80.69 809 809
10234 -80.66 568 568
10235 -80.63 311 710
10236 -81.69 872 872
10237 -81.68 0 1089
10238 -81.43 554 554
10239 -81.62 516 516
10240 -80.58 545 545
10242 -80.83 489 489
10244 -79.73 387 530
10246 -79.64 575 575
10247 -81.70 0 580
10248 -80.69 788 788
10249 -79.75 668 777
10250 -80.07 410 546
10251 -81.73 862 862
10252 -80.64 476 639
10253 -80.16 608 775
10254 -80.11 567 567
10255 -80.11 493 694
10256 -80.68 584 584
10259 -81.53 0 1065
10261 -80.09 805 805
10262 -80.08 485 745
10263 -81.59 844 844
10264 -80.58 558 558
10265 -80.59 897 897
10266 -80.12 336 557
10267 -80.66 353 353
10269 -81.63 641 641
10270 -80.68 762 762
10271 -80.04 487 734
10272 -79.38 287 638
10274 -81.60 0 672
10276 -81.63 597 597
10277 -80.67 701 701
10278 -80.59 425 425
10279 -80.73 223 467
10280 -81.64 735 735
10285 -80.70 912 912
10286 -81.52 476 476
10287 -81.75 0 547
10288 -79.70 248 535
10291 -81.75 0 734
10292 -81.58 457 457
10294 -81.68 511 511
10296 -80.71 223 649
10297 -80.78 391 688
10298 -80.66 350 562
10299 -80.74 718 718
10301 -81.75 737 737
10304 -80.72 659 659
10305 -81.68 0 313
10306 -79.68 395 786
10307 -80.04 427 562
10308 -80.16 327 750
10309 -80.56 262 670
10310 -80.11 564 763
10311 -80.02 263 460
10312 -81.60 986 986
10314 -79.40 510 604
10315 -80.75 1005 1005
10316 -81.89 596 596
10317 -80.68 648 648
10318 -80.82 801 801
10319 -81.78 0 370
10321 -80.63 685 685
10322 -80.06 0 725
10323 -81.66 0 754
10325 -81.82 585 585
10326 -80.63 225 623
10329 -80.14 427 599
10330 -79.70 590 590
10331 -81.63 563 563
10332 -80.55 646 646
10333 -80.06 824 824
10335 -81.66 545 545
10336 -79.69 306 790
10337 -80.08 414 594
10338 -80.68 437 720
10339 -80.07 609 609
10340 -81.49 0 324
10341 -80.07 613 838
10342 -80.68 437 731
10344 -80.72 0 595
10345 -80.75 407 732
10346 -81.55 963 963
10347 -81.63 0 514
10348 -81.63 865 865
10349 -81.60 0 806
10350 -80.65 283 613
10352 -80.07 758 758
10353 -81.76 0 572
10354 -81.65 0 635
10355 -81.58 757 757
10356 -81.83 557 557
10357 -80.67 276 644
10358 -81.72 1013 1013
10359 -79.59 296 614
10360 -80.79 508 508
10361 -80.71 709 709
10363 -81.74 803 803
10364 -80.67 506 506
10366 -81.74 0 517
10367 -80.62 483 697
10368 -81.62 559 559
10369 -80.67 544 826
10371 -80.79 441 673
10372 -80.05 214 674
10374 -81.62 508 508
10376 -80.10 854 854
10377 -80.73 383 630
10378 -81.50 898 898
10379 -81.61 667 667
10380 -80.58 390 669
10383 -81.72 835 835
10384 -81.68 0 836
10385 -80.20 551 551
10386 -80.55 770 770
10387 -80.71 653 653
10390 -80.71 669 669
10392 -80.57 0 541
10393 -80.59 0 585
10394 -81.73 835 835
10395 -80.75 265 592
10396 -81.67 0 691
10399 -80.69 830 830
10400 -81.44 0 490
```

### A.12 The preregistered 128-seed measurement of q3 (Section 7.4): registration, run and analysis

Files, with their SHA-256 (`hashes.txt` of the run, written by the run script at its start on the cloud machine, `/root/r38q3b`; the preregistration is also hashed in `prereg_b_hashes.txt` at 11:02:24 MDT, before the first seed):

```text
17425aaa624561ceeb641977d72d86f6f4c1b8e57c6a05b7c82ad9ed1d12d485  traillab
c47e5ec605a25ae03df29ada92f68c3462468262dc30730a1e201de335c8a14d  chi/chi38p8.txt
ff582e64e060db2807d85fbe31b054ef04eea26ed00b46dbcafb66b2c36a7138  sel_members.txt
eb3310e43e0308e5658631226e09e9ab7d0403de9470dcd3b36545f9fee00f5a  PREREG_Q3P8_B.md
```

*Preregistration* (`PREREG_Q3P8_B.md`, written 2026-10-17 before the first seed of this run; the quantity, the tool and the inputs are those of `PREREG_Q3P8.md`, Appendix A.9):

```text
# Preregistration B: q3 of P8 for the printed-cell accepted event, 128 fresh seeds (written 2026-10-17 before the first seed of this run)

Quantity: the same as PREREG_Q3P8.md (research/day_1014/r38-p8/build, sha256 of that file in prereg_b_hashes.txt): q3 = the average over the 196,608
selected variants of Pr[accepted event | good pair], the event of chi38p8.txt (rows 16..21 cells, '+' pairs and two-bit conditions, row 19 on signed
differences, the relation E18 = E17 INCLUDED), outputs after step 37 equal.
Tool and inputs: the same files as PREREG_Q3P8.md, unchanged: traillab binary sha256 17425aaa624561ceeb641977d72d86f6f4c1b8e57c6a05b7c82ad9ed1d12d485,
chi/chi38p8.txt c47e5ec605a25ae03df29ada92f68c3462468262dc30730a1e201de335c8a14d, sel_members.txt ff582e64e060db2807d85fbe31b054ef04eea26ed00b46dbcafb66b2c36a7138.
Command per seed s (one process per seed, the documented workaround for the multi-seed 'window' crash after a dead seed; the generator streams
are indexed by seed, so a seed gives the same counts either way): window --chi chi/chi38p8.txt --rows 22 37 --event out --np 8192 --mt 32768
--seeds s --threads 4 --autolist --var "W8 a0list @sel_members.txt late". Machine: the cloud box, 2 seeds at a time (8 threads), nice 10.
Seeds: 128 fresh seeds 7001..7128 (never used for P8: earlier P8 runs used 3001-3032, 5001-5032, 9001-9008, 9401-9404, 9501-95xx, 10001-10400).
Per-seed value L_s = prefix log2 P(rows 7..21) + log2 rate(EXACT); a dead seed or 0 EXACT counts as -128.
Declared value: q3_base = floor_4dec( mean(L) - t sd(L) / sqrt(128) ), t = t(0.99, 127) = 2.3556 (one-sided 99% Student lower bound, the seed is the cluster),
over THESE 128 seeds only (the 32 seeds of PREREG_Q3P8 are not pooled). Diagnostics required 0 (prefix broken by redraw, y-anchor inconsistent,
replay mismatches); a non-zero diagnostic in any seed voids the run (reported, not replaced). No interim look at L values, no stopping rule; all 128 seeds are used.
Use: if the run is not void and q3_base > -96.5755, the next r38 filing uses q3_model = q3_base x 2^0.4149 (the F2 bound, unchanged); otherwise nothing changes.
```

*Run script* (`run.sh`, written by `launch_cloud.sh` on the cloud machine; two seeds at a time, 4 threads each, no `prlimit`; the model file, the list and the binary are those of Appendix A.9; the run took 2026-10-17 17:02:44 to 17:45:42 UTC):

(script omitted: not required for the record; the registered text and outputs are kept)

*Memory sampler* (`hwm.sh`, started separately at 17:16:09 UTC; it ended with the run, 17:45:42 UTC):

(script omitted: not required for the record; the registered text and outputs are kept)

The sampler recorded `time seed VmHWM_kB` lines for the processes of seeds 7041..7128 (88 seeds; the 40 earlier seeds were running or finished before it was started and are not in the record). Largest VmHWM per process, seed:KiB: 7041:182560 7042:181824 7043:182264 7044:183324 7045:182536 7046:184052 7047:182520 7048:181764 7049:182348 7050:182776 7051:182756 7052:182028 7053:182428 7054:181656 7055:183012 7056:182264 7057:183056 7058:193792 7059:183260 7060:182524 7061:182272 7062:184348 7063:181768 7064:184616 7065:182576 7066:183028 7067:182540 7068:184300 7069:188692 7070:186884 7071:184320 7072:190504 7073:182764 7074:182272 7075:183360 7076:182308 7077:183620 7078:191852 7079:184304 7080:184264 7081:183044 7082:184568 7083:183028 7084:182288 7085:181060 7086:184088 7087:183208 7088:182040 7089:184088 7090:183852 7091:182872 7092:182332 7093:183300 7094:181716 7095:184564 7096:184104 7097:183044 7098:182576 7099:181792 7100:184836 7101:183840 7102:182572 7103:183064 7104:182336 7105:182752 7106:183040 7107:183812 7108:182776 7109:182540 7110:182552 7111:183236 7112:183484 7113:181992 7114:185584 7115:182388 7116:182556 7117:182292 7118:182292 7119:183288 7120:184028 7121:187540 7122:183416 7123:183808 7124:182536 7125:183796 7126:182304 7127:184852 7128:184604. The largest is 193,792 KiB = 2^27.56 bytes; the largest sum of the two concurrent processes at one sample is 376,848 KiB = 2^28.52 bytes.

The log of the first seed (the same block for every seed; the full logs are the 128 files `seed_7001.log` .. `seed_7128.log` of the run):

```text
model p8: 38 steps, anchor row 15 (x and y rows 12..15 held), E-driven rows 16..21, lowest conditioned row 7
  conditions: 35 two-bit/linear (printed), 35 in the procedure model; 'except' words: W7 W8
  free word W6 (late): W6 rand late
  free word W7 (late): W7 fset s0 03bff800 late
  free word W8 (late): W8 a0list @/root/r38q3b/sel_members.txt late
WINDOW rows 22..37 event=out np 8192 m 256 mt2 1024 mw 256 mt 32768 threads 4 prefix-conditions cells
-- seed 7001
  init: 8192 particles, acceptance 1.000000 (rows 16..15)
  E16 set under the prefix conditions: 160 values (enumerated 2^24 candidates)
  stage 16 (E-driven, list of 160): accepted 2097152 of 2097152, log2 est -24.6781
  stage 17 (E-driven): forced  7 bits, accepted 1973 of 2097152, log2 est -41.7319
  stage 18 (E-driven): forced  7 bits, accepted 17035 of 2097152, log2 est -55.6757
  stage 19 (E-driven): forced  3 bits, accepted 2097152 of 2097152, log2 est -58.6757
  stage 20 (E-driven): forced  5 bits, accepted 1267 of 2097152, log2 est -74.3685
  stage 21 (E-driven): forced  4 bits, accepted 261604 of 2097152, log2 est -81.3715
[s7001] prefix log2 P(rows 7..21) = -81.3715
[s7001] samples 268435456 (late words redrawn per sample), prefix broken by redraw 0, y-anchor inconsistent 0, replay mismatches 0
[s7001]   cells          rows 22..37:    134215625  rate 4.999922e-01 (log2  -1.0000) 95% [4.9993e-01, 5.0005e-01]  with exact 10961
[s7001]   EXACT          zero output difference after the last step:        10961  rate 4.083291e-05 (log2 -14.5799) 95% [4.0076e-05, 4.1605e-05]
[s7001]   ratios to 'cells' (95% cluster-robust over particles; halves = particles split in two):
[s7001]     EXACT/cells = 0.00008 +- 0.00000  (log2 -13.5799)  halves 0.00008 +- 0.00000 | 0.00008 +- 0.00000
[s7001]   log2 P(rows 7..37, model cells) = prefix + log2 rate(cells) = -82.3715
[s7001]   time 38.0 s
== summary over 1 seed(s): EXACT/cells 0.00008 +- 0.00000
== summary: log2 P(rows 7..37, model cells) mean -82.3715, seed sd 0.0000 (seeds: -82.3715)
```

The declared value is computed from the 128 logs by `q3analysis_b.py` (the script of Appendix A.9 with 128 seeds, the registered t = 2.3556 and the halves 7001..7064 / 7065..7128; usage `python q3analysis_b.py seed_*.log`):

(script omitted: not required for the record; the registered text and outputs are kept)

```text
seeds 128 7001 .. 7128 | seeds with all diagnostics 0: 128 | EXACT events 1326458 min per seed 7809
mean -96.3123  seed sd 0.5563  one-sided 99% Student lower bound -96.428132  ->  q3_base = -96.4282
halves -96.3328 / -96.2918
per seed: -95.9514 -95.8473 -97.6863 -95.8194 -96.4100 -97.3530 -96.0952 -96.5271 -95.6510 -96.0632 -96.1255 -96.1205 -96.8975 -95.9300 -96.2596 -96.4129 -96.5415 -95.9474 -96.0871 -95.7058 -96.1807 -97.0824 -95.7759 -95.7093 -96.4054 -96.2425 -95.8663 -96.6074 -96.6234 -96.4052 -96.5836 -95.7079 -95.3868 -95.3947 -96.7348 -96.7012 -96.4372 -96.6482 -96.9617 -97.3097 -96.6475 -96.9395 -97.3445 -95.0900 -96.8402 -96.4532 -95.7523 -97.0385 -96.3175 -96.5519 -96.3824 -96.3070 -97.3019 -95.9419 -97.2275 -96.8172 -95.5370 -95.6234 -96.3551 -96.3398 -95.8110 -96.7379 -95.4275 -96.3202 -96.2097 -96.9832 -96.2176 -96.2349 -96.1682 -96.3922 -95.9092 -96.9812 -95.8768 -96.0074 -95.8666 -95.9552 -95.4917 -95.4601 -96.2234 -96.2378 -95.4621 -96.4844 -96.2793 -96.7117 -96.3305 -96.6939 -96.5255 -96.4187 -96.7542 -96.6869 -96.7610 -97.2736 -96.7676 -96.6342 -95.7191 -96.3106 -95.7573 -96.3771 -95.8864 -96.1180 -95.9172 -96.2218 -98.1137 -95.0796 -95.9378 -95.4504 -96.7590 -95.1732 -95.7216 -96.8931 -96.6392 -95.2674 -96.5771 -96.1931 -95.8976 -96.5685 -96.6127 -96.2800 -95.8841 -96.6560 -96.2981 -95.8157 -96.7839 -97.2887 -96.1010 -96.1892 -97.1310 -97.0554
```


### R.2 The characteristic search (H4a, H4b; 9aaf71a2 Appendix C)


**P8.** 1a695f0b Section 3.2 publishes the search that found P8 (quoted; participant-run): a signed-difference SAT model run over the 24 XOR patterns of weight 25 of the message shape, each with every known signed difference blocked, 38 solver runs with a limit of 10,800 s each (12 UNSAT in 8 to 22 s, 11 SAT in 2,514 to 9,890 s, 15 TIMEOUT at 10,800 s), each SAT solution through a value-level coupling check and an estimator; P8 = run SW_p08_k1 (4,714 s, coupling 662 s). The listed run times total 230,183 s = 2^17.81 s; the author bounds the whole search, S, the class data and all its development by one 10-core machine for less than 2^21 core-seconds. At the hash rate below (3,797,484 SHA-256 compressions per second, one thread) 2^21 core-seconds are 2^42.86 SHA-256 evaluations = 2^43.61 units, 34.4 bits under A_C = 2^78. The measurements below (from fb176310, for the published characteristic and for a 39-step characteristic) are the same kind of search; they put the allowance in the same range.

**Measured by us (fb176310 Appendix C, unchanged).**

**Part A. Published and measured cost of the same kind of search (the basis of A_C = 2^78).** Units are target compressions (one 38-step compression = 1 unit = 2728 word operations); a full 64-step SHA-256 evaluation is charged 64/38 units = 4,594.5 word operations, more than a target compression.

*Conversion.* Hash rate measured here: portable C SHA-256 compression (no SHA-NI, gcc -O2, one thread, AMD Ryzen 9 7900X, WSL2; checked on "abc", first words ba7816bf 8f01cfea), five runs of 2 x 10^7 compressions: 4,030,079, 4,022,282, 3,891,284, 4,013,036 and 3,797,484 per second; the slowest, 3,797,484 per second (2^21.86), is used for every conversion (a slower rate gives more evaluations, hence a larger cost). Solver CPU-seconds = wall seconds x threads (an upper bound: idle threads are counted). Figures in the table are log2.

| source | problem | stated cost | SHA-256 evaluations | units | word operations | bits under 2^78 units |
|---|---|---|---:|---:|---:|---:|
| Mendel, Nad, Schlaeffer 2013, Sect. 6.3 p.14 | 38-step SFS: characteristic and pair together | about 8 h on a single CPU, "about 2^37 SHA-256 evaluations" (hardware not named) | 37.00 | 37.75 | 49.17 | 40.25 |
| Mendel et al. 2013, Sect. 6.2 p.12 | 31-step SFS: characteristic and pair together | about 21 h, "about 2^38.4 SHA-256 evaluations" | 38.40 | 39.15 | 50.57 | 38.85 |
| Li, Liu, Wang 2024 (ePrint 2024/349), p.16 | 39-step SFS colliding pair given the characteristic | 120 s with 26 threads = 3,120 thread-seconds (hardware not named) | 33.46 | 34.22 | 45.63 | 43.78 |
| ours, 39-step characteristic | derived from scratch with the tool of [LLW24a] | 772.58 s wall x 12 threads (CryptoMiniSat) + 1,800.77 s x 1 (Kissat, no result) = 11,071.7 CPU-s | 35.29 | 36.04 | 47.46 | 41.96 |
| ours, 38-step pair (part B) | pair given the published cells, 4 calls, 3 without a model | 2,852.83 CPU-s | 33.33 | 34.09 | 45.50 | 43.91 |

Our 39-step characteristic derivation: the unmodified model scripts of github.com/Peace9911/sha_2_attack at commit 6a9f35fd (the account that hosts the authors' RIPEMD-160 tool of [LLW23]) were read before running (no network, no installs, writes only in the working directory); the STP query they emit was translated to CNF by our own converter (which rejects six mutated characteristics and accepts the published 39-step characteristic and rows 5..24 of the published 37-step one) and solved with CryptoMiniSat 5.11.21 on 12 threads: model found after 772.58 s wall (about 2.6 CPU-hours); Kissat 4.0.3 on the same file stopped at 1,800.77 s without a result. It is a window search (rows 8..26 with the message support fixed and the weights W 25, A 10, E at most 90 asserted) that finds a characteristic of the published weights, not the characteristic of Table 3 of [LZLLQZ26]; one run, one machine.

*Reading.* Every figure is far below 2^78 target compressions: the largest, 2^39.15 units (Mendel et al.'s 31-step figure), is 38.85 bits under it, and the 38-step figure of the same authors, 2^37.75 units, is 40.25 bits under; counted in word operations without the factor C, the largest is 2^50.57, 27.43 bits under 2^78. The 38-step characteristic of [LZLLQZ26] (two-block framework, dense rows 0..16) is a harder instance than those searches and no log of its search exists; the margin of 38.85 bits (a factor of about 2^39) is what A_C = 2^78 leaves for that difference and for failed and repeated searches.

**Part B. Our pair searches and sparse part.**

Participant-run here; programs written and run by Grok (xAI); not shipped (64 KiB source limit; the figures are not used in the ledger, which charges the allowance). SAT: one word operation = one propagation; otherwise one tick = one 32-bit add/sub, S0, S1, s0, s1, CH, MAJ or hash-set probe. Units = word operations / C. Totals include the calls without a model.

**38-step pair search, given the published cells.** Circuit: both 38-step chains with a shared chaining value, message masks on W7..W11, W15 (W16, W23, W25 expanded), every cell of Table 3, the 13 vertical links and the 47 two-bit conditions (W25[4] = W25[6], which holds on the published pair; Table 4 prints W25[9]); 110,437 variables, 383,913 clauses, satisfied by the published pair; one clause blocks the published (CV, M'). File a pins the 24 bits common to the 32 E16 words of the published list; file b selects one of the 32 words.

| call (time limit 900 s) | file | result | CPU s | propagations |
|---|---|---|---:|---:|
| Kissat 4.0.3 --sat --seed=2 --walkinitially=true | a | no model | 898.63 | 592,022,133 |
| CaDiCaL 2.1.3 --seed=1 | a | no model | 898.61 | 1,813,811,854 |
| Kissat 4.0.3 --sat --seed=4 --walkinitially=true | b | pair | 476.96 | 433,129,432 |
| CaDiCaL 2.1.3 --seed=4 | b | no model | 578.63 | 1,217,006,281 |
| total | | | 2,852.83 | 4,055,969,700 = 2^31.917 (2^20.504 units) |

The pair (38-step SHA-256 compression with feed-forward; recomputed by us with an independent step function checked against hashlib on "abc"; M' carries the published E16 word 482326fd, with a different CV and message):

```
CV     43058709 adfdbff7 b7e63568 b4e09527 3ef1b89a 18f03df1 7fd9bbaa 7f392ba4
M      33f3fd01 ab09628d 9971c77a 2f0148d3 442fd7d8 9acaf5c3 2fd3a6f8 a8740b40
       c91bb8b5 9e019239 04039fa1 0ce30b8d a18c515a 76a1e994 d28e48a0 9b5f6dbb
M'     33f3fd01 ab09628d 9971c77a 2f0148d3 442fd7d8 9acaf5c3 2fd3a6f8 88740b40
       cd5bb0b5 be019239 01028d0b 0ceb1f8d a18c515a 76a1e994 d28e48a0 9f1f65bb
digest 614d0b44 0d272005 713bab9e 4fc8e2a1 126b7229 bbb45050 0d592f10 cf2f96a9
```

Words that differ: 7..11, 15, 16, 23, 25 (dW16 = e0000000, dW23 = fe7f8000, dW25 = 20000000); A and E are equal from step 22.

**37-step analogue** (C = 2644; the same circuit on the 37-step characteristic, W15 pinned on the 24 common bits of its list): Kissat seed 2 pair A (135,356,424 propagations), Kissat seed 1 no model (167,052,440), CaDiCaL seed 1 pair B (494,307,286); total 796,716,150 = 2^29.570 (2^18.201 units). Digests: A 3c7353c7 46761dc9 8b3ce5a5 3c6530d2 d6e267fb f0f5b41e b8c21e9a 03b5b458, B 6c1e60a3 27a17426 dd5333ab 9f3317d4 00453b21 27264f97 2f2ea277 4a533513.

**38-step sparse part, from the support and the Section 4.1 rules only** (no table cell seeded; the published values used only as a checker):

| part | ticks | CPU s | result |
|---|---:|---:|---|
| message-difference signing, all 32 disturbance bits | 101,842,272 | 0.533 | bit 29 gives the published XOR masks; fe7f8000 among the 8 dW23 sums |
| sparse window rows 17..37, bits 28..31, all 8 dW23, both dW25 signs | 11,239,528 | 0.021 | the published dW23, dW25 close (22 conditions, rank 22) |
| total | 113,081,800 = 2^26.753 | 0.554 | |

**Not measured (the allowance A_C = 2^78):** deriving the dense signed characteristic of rows 0..16 with its two-bit conditions (the pair searches load those cells; a 37-step attempt with them unset, by SAT, step-6 cubes and a pattern beam, returned no model; of 4,614 message pairs realising the 38-step dW23, dW25 at CV = 0, none meets the zero window), and the authors' failed and repeated searches.


### R.3 Development computation and memory (H4c, H6; 9aaf71a2 Sections 13.4, 14, Appendix A.10)


Below 2 x 10^5 CPU-seconds in total (the shared-carrier runs of Section 7.5, about 2 x 10^4 CPU-seconds on the cloud machine, included; the exhaustive passes, the end-to-end runs, the q3 runs of Section 7.4 (about 2 x 32 x 90 s on 3 to 4 threads, and the 128-seed run, 128 seeds of about 40 s on 4 threads, about 2 x 10^4 CPU-seconds on the cloud machine), the replica's development and calibration, the H3 measurement, the program scans and the cloud checks of the hoisted programs), far inside the charge DEV = 2^70 (H4c). Machine: Windows 10 with Python 3.14 for the programs in Python, and an Ubuntu distribution under WSL2 (24 cores, 46 GB, gcc) for the programs in C; heavy jobs ran at reduced priority on at most 4 threads each.

*Memory of the development executions (H4c, H6).* The development executions that produce data the procedure uses are the exhaustive pass `p8fam` (lean version: the class descriptors and the list of the 196,608 selected variants), the end-to-end runs `e2ep8` (table-free version) with their exact checks, and the programs of Section 14 (c). Each of them was run under a hard address-space cap (2026-10-14 for the C programs and the q3 run, 2026-10-17 for the programs of the hoisted version) (`prlimit --as=N`: an allocation beyond N fails and the program stops), with its peak resident memory measured by `research/tools/memmeter` (Appendix A.10, `run_chain.sh` and `run_small.sh`). The caps are 2^27 = 134,217,728 bytes for the C filters and the Python programs and 2^28 = 268,435,456 bytes for `traillab`, whose model, particles and per-stage records need about 218 MiB over the 32 seeds (222,756 KiB). Every run exited with status 0 under its cap; the peaks are in Section 14 (c2), the largest being 222,756 KiB = 2^27.77 bytes.
- `p8fam` (lean): peak 69,496 KiB. Its class descriptors (`maxclasses.txt`, SHA-256 b7a3fc4e118c0871ef8b197f7967c84c95e97ec013062f6864b27a5f51903d26) and its list of the 196,608 selected variants (`sel_members.txt`, SHA-256 ff582e64e060db2807d85fbe31b054ef04eea26ed00b46dbcafb66b2c36a7138) are the inputs of the preregistered q3 run and of the end-to-end runs.
- The earlier preregistered q3 run (32 seeds, Appendix A.9): the same binary (SHA-256 17425aaa624561ceeb641977d72d86f6f4c1b8e57c6a05b7c82ad9ed1d12d485), model file `chi38p8.txt` (SHA-256 c47e5ec605a25ae03df29ada92f68c3462468262dc30730a1e201de335c8a14d), list and seeds 5001..5032 as in `PREREG_Q3P8.md`; the command differs from the preregistered one only in `--threads 3` instead of 4 (the tool's output does not depend on the thread count) and in the environment variable `MALLOC_ARENA_MAX=1` (one malloc arena, so that the address space stays under the cap). All 32 seeds completed under the cap 2^28 (peak 222,756 KiB = 2^27.77 bytes). Each of the 449 result lines (prefix estimate, sample counts, diagnostics, cell and EXACT counts and rates, ratios) and of the stage lines of the 32 seeds is identical to the run of 2026-10-14 15:00 (Appendix A.9), so mean -96.3251, seed sd 0.5774 and the declared bound -96.5755 of the earlier run (Section 7.4) are those of the repeat.
- `e2ep8` (table-free): three runs under the cap 2^27, peaks in Section 14 (c2); counts in Section 13.1 (repeat).
- The Python and C programs of Section 14 (c): run under the cap 2^27, exit status 0.
The same programs were also timed without a cap with `/usr/bin/time -v` at the time of the first runs; those peaks are in Section 14 (c).
- Evidence for H2, not a development execution of the procedure (Section 14 (c3)): the 128-seed q3 run of Section 7.4 (declared value; commands, hashes and scripts in Appendix A.12) ran on the cloud machine (Linux, gcc) without an address-space cap and without `MALLOC_ARENA_MAX`: one `traillab window` process per seed with 4 threads, two processes at a time, nice 10, about 40 s per seed (17:02:44 to 17:45:42 UTC), its binary, model file and list those of the earlier run. The peak resident set of every `traillab` process (VmHWM of /proc/PID/status, KiB) was sampled every 2 s by `hwm.sh` from 17:16:09 UTC, 13 minutes after the first seed started, so the record covers the processes of seeds 7041..7128 (88 of the 128) and not those of seeds 7001..7040: at most 193,792 KiB = 2^27.56 bytes per process (Section 14 (c3)).
- The runs of Section 7.5 (`traillab window`, shared-carrier mode: V0, the stage-M scan, F2; commands and scripts in Appendix A.11) ran on the cloud machine (Linux, gcc), 8 threads, nice 10, one process per seed, each under `prlimit --as=268435456` (2^28) with `MALLOC_ARENA_MAX=1` and `ulimit -s 2048`, peak resident memory by `/usr/bin/time -v` (maximum resident set size of the process, the wait4 component of memmeter): at most 219048 KiB = 2^27.74 bytes, every process exited with status 0 except that the two first launches of the registered run crashed in the tool after a dead seed (Section 7.5), which are not used.



**Peak memory: current binding treatment (H6).** The peak is the maximum over online, preprocessing and the development executions that produce data used by the procedure. Earlier versions relied on an absent `2^27.7542` capped Step-1 receipt and treated the online `2^28.01141` cell as binding. That reclassification was rejected and is withdrawn. This candidate uses the self-contained author measurement in (a), `279,720 KB = 286,433,280 bytes = 2^28.0936238847...`, rounded upward to `28.094`; Appendix A.15 is normative.
(a) The computations behind the advice (P8 and S), measured by their author (1a695f0b Section 11, quoted; single-threaded, sequential, peak of the summed resident memory sampled every 0.2 s): the Step-1 solve of P8 (Python model and Kissat) 279,720 KB = 286,433,280 bytes = 2^28.094; the signed search that found P8 at most 248,000 KB = 2^27.92; the class descriptors (`a0cls.c`) 2^25.14; the condition tables and the pair below 2^24. Largest: the Step-1 solve, 2^28.0936, which sets the claim 2^28.094.
(b) Measured by us (fb176310 Section 14; `/usr/bin/time -v`, single-threaded): Kissat 4.0.3 and CaDiCaL 2.1.3 on the 38-step pair-search circuits, 2^26.82 to 2^27.15; the characteristic-derivation instance of Appendix C part A, CaDiCaL 2^27.56, Kissat 2^27.49.
(c) Our development programs (Section 13.4) in the runs that produced the outputs used by the claim, each measured with `/usr/bin/time -v` (maximum resident set size; `memmeas.sh`), without an address-space cap (the programs of the hoisted version, `a0hoist38.py`, `sens.py` and the emulations, were run under caps only: (c2)):

```text
traillab window (q3 run configuration, one seed, 4 threads)   182,824 kB   (2^27.48 bytes)
p8fam (exhaustive pass over a0, 16 buckets)                     69,348 kB
python verify_r16p8.py (the 2^24 end-to-end run)                36,660 kB
python calq3.py (20 replicates)                                 19,580 kB
python h3gen.py (100 successes)                                 19,536 kB
python w7check.py                                               16,980 kB
python r16p8.py                                                 12,168 kB
p8hits (4 threads), f23, h3count, e2ep8 (2^22 first blocks, 4 threads)   8,020 kB, 7,948 kB, 7,976 kB, 7,684 kB
```

The organizer experiments peak at 65,536 KiB (`a0-online-r38`) and 26,776 KiB (`a0-q3-r38`) under Linux and Python 3.14 (the largest resident size of their process), inside the sandbox's 128 MiB.

(c2) The development programs, run under hard address-space caps (`prlimit --as=N`), peak resident memory by `research/tools/memmeter` (maximum of the child's wait4 ru_maxrss, the per-process VmHWM and the summed RSS of the process tree sampled every 10 ms; floor about 1.4 MB). `traillab` and the OpenMP programs ran on 3 threads with `MALLOC_ARENA_MAX=1`; everything ran under `nice` (10 for the programs of 2026-10-14, 19 for those of 2026-10-17). Appendix A.10 lists the scripts and the records.

| execution (capped run) | cap `--as` (bytes) | exit | peak resident KiB (memmeter) | log2 bytes |
|---|---|---:|---:|---:|
| `p8fam` (lean): exhaustive pass over a0, class descriptors, list of the 196,608 selected variants | 2^27 = 134,217,728 | 0 | 69,496 | 26.08 |
| `traillab window`, earlier preregistered q3 run (32 seeds): seeds 5001..5032, 3 threads, `MALLOC_ARENA_MAX=1` | 2^28 = 268,435,456 | 0 | 222,756 | 27.77 |
| `e2ep8` (table-free): seed 19, 2^22 first blocks, 3 threads | 2^27 = 134,217,728 | 0 | 7,700 | 22.91 |
| `e2ep8` (table-free): seed 23, 2^23 first blocks, 3 threads | 2^27 = 134,217,728 | 0 | 7,616 | 22.89 |
| `e2ep8` (table-free): seed 17, 2^24 first blocks, 3 threads | 2^27 = 134,217,728 | 0 | 7,716 | 22.91 |
| `a0hoist38.py` selftest | 2^27 = 134,217,728 | 0 | 53,700 | 25.71 |
| `a0hoist38.py` calibrate | 2^27 = 134,217,728 | 0 | 64,484 | 25.98 |
| `a0hoist38.py` ledger | 2^27 = 134,217,728 | 0 | 69,480 | 26.08 |
| `sens.py` | 2^27 = 134,217,728 | 0 | 54,668 | 25.74 |
| `emu2.py` a0-online-r38 (two organizer-request emulations) | 2^27 = 134,217,728 | 0 | 83,568 | 26.35 |
| `emu2.py` a0-q3-r38 (two organizer-request emulations) | 2^27 = 134,217,728 | 0 | 44,820 | 25.45 |
| `w7check.py` | 2^27 = 134,217,728 | 0 | 23,796 | 24.54 |
| `h3gen.py 99 100` | 2^27 = 134,217,728 | 0 | 23,624 | 24.53 |
| `calq3.py 2000 2020` | 2^27 = 134,217,728 | 0 | 24,768 | 24.60 |
| `verify_r16p8.py (seed 19, 2^22 first blocks)` | 2^27 = 134,217,728 | 0 | 27,304 | 24.74 |
| `verify_r16p8.py (seed 23, 2^23 first blocks)` | 2^27 = 134,217,728 | 0 | 32,008 | 24.97 |
| `verify_r16p8.py (seed 17, 2^24 first blocks)` | 2^27 = 134,217,728 | 0 | 41,596 | 25.34 |
| `p8hits` | 2^27 = 134,217,728 | 0 | 7,616 | 22.89 |
| `f23` | 2^27 = 134,217,728 | 0 | 7,596 | 22.89 |
| `h3count` | 2^27 = 134,217,728 | 0 | 7,548 | 22.88 |
| `r16p8.py` | 2^27 = 134,217,728 | 0 | 12,336 | 23.59 |
| `traillab window` shared-carrier runs of Section 7.5 (V0, stage M, F2; 8 threads, one process per seed, cloud machine; `/usr/bin/time -v` instead of memmeter) | 2^28 = 268,435,456 | 0 | 219,048 | 27.74 |

Largest: 222,756 KiB = 2^27.77 bytes, under a cap of 2^28 (`traillab`); the peaks of the other programs are lower. Every run completed under its cap.

(c3) The q3 measurements of Section 7.4 (Appendix A.12) are evidence for the probability premise H2: they estimate the success probability of the procedure and the procedure reads no data they produce, so, like the organizer experiments, they are not a phase of the procedure, not counted in H6 and not charged in DEV. The 128-seed run ran without an address-space cap. It ran on the cloud machine, one `traillab window` process per seed with 4 threads, two processes at a time, nice 10. `hwm.sh` (Appendix A.12) recorded the peak resident set of every `traillab` process (VmHWM in /proc/PID/status) every 2 s from 17:16:09 UTC, 13 minutes after the first seed started: its record covers the processes of seeds 7041..7128 (88 of the 128); the processes of seeds 7001..7040 were not sampled. Largest peak of one process: 193,792 KiB = 198,443,008 bytes = 2^27.56. Largest sum of the two concurrent processes at one sample: 376,848 KiB = 2^28.52. The seeds are independent runs of one program, so the run needs one process at a time and the memory of the execution is that of one process, 2^27.56 < 2^28.094. For comparison, one seed of the same configuration in one process measured 182,824 KB (2^27.48, (c)) and the 32-seed run of Section 7.4 in one process under the cap 222,756 KiB (2^27.77, (c2)).

Not measured by us: the memory of P8's search and Step-1 solve (the author's figures are used); the 12-thread solver runs of fb176310's Appendix C are timing evidence only.



Run in WSL (Ubuntu) on 2026-10-14 (`run_chain.sh` and the first part of `run_small.sh`) and on 2026-10-17 (`run_small_hoist.sh`). `prlimit --as=N` sets RLIMIT_AS, the virtual address space of the process and its children: an allocation beyond N fails. `research/tools/memmeter` runs the command and reports the peak resident memory (maximum of the child's wait4 ru_maxrss, the per-process VmHWM and the summed RSS of the process tree sampled every 10 ms) as JSON, with the exit status. The programs are the binaries and scripts of the construction (`p8fam_lean`, `traillab`, `e2ep8`, `a0hoist38.py` of this package, SHA-256 d874226f004ccb1bd5e8d398cfee4f2607858250f8c199cca3f4e250befb733b, and the evidence scripts of Appendix A); `traillab`, `chi38p8.txt`, `sel_members.txt` have the SHA-256 values of Section 13.4. `MALLOC_ARENA_MAX=1` limits the C library to one malloc arena (by default each thread reserves 64 MiB of address space). The resident memory of `traillab` is about 218 MiB over the 32 seeds with 3 threads (about 181 MiB for one seed); without the environment variable its address space exceeds 2^28 bytes (a one-seed test failed at the cap with a segmentation fault, and passed with it). The table of Section 14 (c2) lists the peaks.

(script omitted: not required for the record; the registered text and outputs are kept)

(script omitted: not required for the record; the registered text and outputs are kept)

(script omitted: not required for the record; the registered text and outputs are kept)

Records: for each run the memmeter JSON line (command, exit status, signal, wall and CPU seconds, ru_maxrss, tree VmHWM, tree summed RSS, peak bytes) is the last line of the run's output; the repeated q3 run compares equal to the earlier one on all 449 result and stage lines of its 32 seeds.



### R.4 The preprocessing report of 1a695f0b (quoted)

~~~
Verbatim lines of the public proof.md of 1a695f0b (dariolina, sha256-r38, 95.32358), read as a document; sha256 of that proof.md: a86eff8b38ab02389f3c1a87b63d35982b41396310490c94eb998baba263db53
L261: T = A_C + A_S + DEV + N_FB + (N_FB x 35 + V_MAX + OVER + PRE + FIN) / C + 6
L262:   A_C = 2^48, A_S = 2^50, DEV = 2^50 (Section 12, H4)
L290: preprocessing (single-threaded, sequential; peak of the summed resident memory of all processes of each computation):
L291:   Step-1 solve of P8 (joint.py: value-exact dense part and tail, Python model + Kissat): 279,720 KB = 2^28.094 (sampled every 0.2 s)
L292:   the signed search that found P8 (stepk.py + Kissat, same specification and seed): at most 248,000 KB = 2^27.92 over 2 h 20 min
L293:     (Python 152,868 KB and Kissat 80,816 to 88,096 KB resident together; stopped after the original 78-minute solve time)
L294:   the class descriptors (a0cls.c, 32 passes): 37,036 KB = 2^25.14; the condition tables and pair (mkvt.py, fromjoint.py): below 2^24
L295: preprocessing peak 2^28.094
L298: *Scope of the memory bound.* Peak memory covers code, advice, retained data, tables and working state of the whole computation: the online algorithm, the charged precomputation (class members, planes, the program) and the computations behind the advice and the allowances (the characteristic search, the Step-1 solve, the class descriptors, the condition tables), each run single-threaded and sequentially. The class descriptors are found in 32 passes over a hash of c7 (`a0cls.c`, at most 2^23 pairs resident). The online figure also covers the deep path's working state (two traces, about 6 KB) and M0, CV1.
L307: - **H4** allowances: the search for P8, S and its class data, and all development used one 10-core machine for less than 2^21 core-seconds in all; A_C = 2^48, A_S = 2^50, DEV = 2^50 hold at any rate up to 2^27 target compressions per core-second. A_C up to 2^84 changes the claim by less than 0.003 (sensitivity).
~~~

## A.13 Amendment: the ledger's scan length (2^28 -> 2^32 words per chaining value; SUPERSEDED HISTORY)

**Status.** A.15 supersedes all A.13 prices, memory and score rows. The 2^32 scan-length correction remains part of the final procedure; the old flat-table ledger and missing-memory-receipt treatment are nonbinding history.

This package is a derivative of `e4243e7a` (Jbenisek, sha256-r38, 92.05331) and of `a32131ff`
(0xplemonade, 91.97072), which supplies the counted memory cell.  **One** quantity in the ledger
changes.  Everything else -- the P1 sum-claw, the loader and the table, the entry format, the
2^26-candidate window `R = 9`, the post-filters, step 3b, the event, `q_pf`, the `q3_P1` transfer
on `R = 9`, the SENT correction, the allowances and the success proof -- is the parent's, and the
declared experiments are the parent's, unchanged.

### A.13.1 What changes

Section 3 of this proof specifies a scan of `2^28` distinct words `u = u0 + n` per chaining value,
and the ledger charges `U = 2^28`; but Section 7 already computes the good-pair count of one
chaining value **over all `2^32` scan words** (`E[K] = 2^32 x 1.58030 x q_pf = 2^16.47`).  The two
uses disagree, and the ledger's `2^28` charges the per-chaining-value fixed work -- the target
compression, `CVSET = 75`, the table reset `2^23 x 5` and the `2^26 x 45` table build -- 16 times
more often than the probability analysis assumes.

This package scans all `2^32` words (`n < 2^32`).  Nothing else in the procedure changes: for each
chaining value the same table is built from the same window, the same 40 lookups per word are made,
the same post-filters and step 3b run.  The scan work per word and the claws per word are
unchanged; only the number of scan words per chaining value, and hence the number of chaining
values needed for the same number of good pairs, changes.

An objection worth answering explicitly: `u` is a 32-bit word, so `u0 + n` for `n < 2^32` is a
permutation of all `2^32` values; distinct chaining values have distinct fresh `u0`, and within one
chaining value the `2^32` scan words are distinct by construction, exactly as in the parent's
`2^28`-word scan.  No word is scanned twice.

### A.13.2 What is charged, and what is not

The per-word work `per_u = 593 + 70.3026 + 16.0478 = 679.3504` is the parent's, unchanged, and now
multiplied by `2^32` instead of `2^28` per chaining value.  The table build, reset and per-chaining-
value constants are charged once per chaining value as before.  The cap, the overshoot (one
chaining value at its maximum) and the final verification are charged in full, and the Bernstein
exponent is recomputed.

### A.13.3 Superseded quantities

| quantity | parent | this package |
|---|---:|---:|
| scan words per chaining value | 2^28 | **2^32** |
| `per_u` (fixed + straddle/residue + claws) | 593 + 70.3026 + 16.0478 = 679.3504 | unchanged |
| `wbar` (mean online work per chaining value) | 1.854236e11 | **2.920850e12** |
| `N_CV` (first blocks) | 271,916,119,323,191,097 | **16,994,757,457,699,444** |
| good pairs per chaining value | 5,683.36 | 90,933.69 |
| `V_MAX` (online work cap, charged in full) | 50,420,431,722,137,969,961,783,108,126 | **49,639,890,185,593,212,744,045,250,682** |
| `OVER` (one chaining value at its maximum) | 67,093,940,669,171 | **1,073,457,123,035,891** |
| `N` | 51,299,670,248,117,604,819,480,998,721 | **50,519,128,711,573,853,964,925,507,997** |
| `time_log2` | 83.95931 | **83.93719** |
| counted memory cell | 2^28.094 (author Step-1 sample) | **2^28.01141** (as `a32131ff`) |
| scalar score | 92.05331 / 91.97072 | **91.94860** |

**Historical rejected memory row.** A.13 inherited `a32131ff`'s replacement of the author
`2^28.094` sample by an asserted `2^27.7542` capped remeasurement. The official review found that
receipt absent. A.15 withdraws the replacement and binds the self-contained 286,433,280-byte
author sample, rounded upward to 28.094. None of the A.13 memory or score values is used now.

### A.13.4 The success proof, recomputed by this package's own code

`python3 experiments/p1claw38.py ledger` prints `N_CV = 16994757457699444`,
`V_MAX = 49639890185593212744045250682`, `N = 505191287115738853964925507997`,
`time_log2 = 83.93719`, a Bernstein exponent of `5.3833e3` (the cap halts with probability at most
`2^-7766`) and a success lower bound of `0.390000000000000008`.  `python3
experiments/p1claw38.py selftest` passes end to end, including its count check on the reduced
fixture.  `E[K] = 2^32 x 1.58030 x 2^-16.1877 = 2^16.47` good pairs per chaining value, so
`E[J(J-1)]/E[J] <= q3r E[K] x 1.246 = 2^-53.8`, far below the `2^-7.5` the H5 argument needs.

### A.13.5 Withdrawal of the earlier A.13 of this candidate's first uploads

Two earlier uploads of this candidate (`1940d3b2`, cancelled; `389a2524` and `fd265f93`, both
refuted) replaced the table loader with a 2^28-candidate, four-bit-residue variant.  The paired
review refuted it on two grounds, both of which this section accepts:

* `lane_evaluability/F2-final-window-transfer-error` and `lane_cryptanalysis/F-WINDOW-INDEX`: a
  window fixed by the top four bits of `a0` to 9 is the interval `[9 x 2^28, 10 x 2^28)`, i.e. the
  top-six-bit windows 36..39, **not** 9..12; the `q3_P1` transfer measured in window `R = 9`
  therefore did not cover the loaded family, and a 64-window mean of the G rate is not a lower
  bound for that subset;
* `lane_cryptanalysis/F-SENT-4BIT`: with a four-bit residue the all-ones entry aliases `SENT`
  with probability 1/16 rather than 1/64, so `cpu_lo`'s correction would have had to be 1/16.

Both findings are moot here: this package keeps the parent's loader, its six-bit residue, its
`R = 9` window and its `1/64` SENT correction, so neither the window transfer nor the alias
correction is touched.  The `q3_P1` lower bound is used exactly as registered, on the same window
the procedure scans.

### A.13.6 Sensitivity

`time_log2` moves by one in the last place for a `2^-1.4e-5` relative change of `N`.  If the scan
length were left at `2^28` the claim would be the parent's `83.95931`; if the per-chaining-value
constants were dropped entirely it would be `83.9369`.  The value claimed is the value of the
procedure as specified, with every term charged in full.


## Appendix A.14. Seven-entry uniform-reservoir table v3 (SUPERSEDED HISTORY; nonbinding)

**Status.** Appendix A.15 supersedes every price, memory figure, score and readiness statement in A.14. A.14 remains only to preserve the development trail for the reservoir layout and polarity correction.

### A.14.1 Change from `711c4bf8`

The parent inserts `2^26` candidates into `2^26` single-entry slots and keeps the last write. Its expected retained fraction is `1 - e^-1 = 0.63212`. This historical v3 design used `2^23` buckets of one 256-bit word each and retains an exact uniform reservoir of at most seven entries in each bucket. The main table therefore remains exactly `2^28` bytes. No characteristic, message family, `a0` window, row-16 target, post-filter, accepted event, or step-3b predicate changes.

For a full-scale bucket, the build layout is seven 9-bit tags, seven 26-bit indices, and a 7-bit seen count: `7*9 + 7*26 + 7 = 252` bits. Four bits are spare. Once all candidates are inserted, an in-place pass converts it to the query layout: seven 10-bit lanes, each with a 9-bit tag and one validity/borrow-guard bit; seven 26-bit indices; a 3-bit retained count; and one spare bit: `7*10 + 7*26 + 3 = 255`. The corrected envelope charges 48 mean operations per bucket for this conversion, 64 in the deterministic maximum, and 5 operations per bucket for reset.

For the first seven arrivals to a bucket, the new entry fills the next lane. On arrival number `n > 7`, an exact independent draw `j` uniform on `{0,...,n-1}` replaces lane `j` iff `j < 7`. This is standard reservoir sampling, so conditional on a bucket's occupants every subset of size `min(n,7)` has equal probability. Fix candidate `i` and `F_i=f`. Under H1, the number `Y` of other candidates in its bucket is `Binomial(2^26-1,2^-23)`, independent of `i`, `f`, the post-filter/tail variables, and the reservoir coins. Candidate `i` is included with probability `E[min(1,7/(1+Y))]`, the same constant for every candidate and every `f`. Thus the reservoir is uniform thinning in first moment. Conditional rates such as `q_pf`, and the average `q3` of the registered uniform-`a0` P1 population, transfer unchanged under this expanded H1 premise. This is a declared heuristic independence statement about the SHA-derived map.

The exact draw uses a 128-by-128 byte table. For bound `n`, a uniform seven-bit value `x` is accepted when `x < floor(128/n)*n`; the table returns `x mod n`, and otherwise returns the rejection marker. The lowest acceptance probability for `8 <= n <= 127` is `65/128`. A fresh random 256-bit word supplies each seven-bit draw. The procedure aborts the chaining value before scanning if a bucket would receive arrival 128 or if one draw rejects 128 consecutive samples. An aborted chaining value cannot output a pair.

### A.14.2 Exact query

Let `q` be the low nine bits of a target and let `word` be one normalized bucket. Define seven-lane constants `QREP[q]`, `BADMASK`, `HIGHS`, and `ONES` as in `experiments/p1claw38.py`. The lookup computes

```text
d = word - QREP[q]
bad = d AND BADMASK
tmp = (bad OR HIGHS) - ONES
z = (NOT tmp) AND HIGHS AND word
```

The guard bit stops subtraction borrows at every ten-bit lane boundary. The base marker remains in `z` when the valid lane satisfies `((tag - q) mod 512) AND (511 AND NOT 5) = 0`, the low-tag differences `{0,1,4,5}`. For `q < 507`, that is the exact ordinary-bucket test. For `q >= 507`, the same low-tag residue can occur with the wrong full-word polarity in either the ordinary or adjacent bucket. The validity guard makes the high bit of each lane in `d` equal to the wrap polarity: it is set exactly when `tag >= q`. Therefore a straddling lookup applies

```text
ordinary bucket: z = z AND d
adjacent bucket: z = z AND (NOT d)
```

The ordinary filter costs one operation and the adjacent filter two. This removes full-word false markers without recomputing candidates. Both `Wsub` values of a row-16 head have the same low nine bits, so a straddling head pays six polarity operations in all.

The ordinary-bucket sequence is 15 word operations:

1. shift the target to the bucket index;
2. add the bucket base;
3. load the 256-bit bucket;
4. mask `q`;
5. add the `QREP` base and `q`;
6. load `QREP[q]`;
7. subtract it from the bucket;
8. mask `BADMASK`;
9. OR `HIGHS`;
10. subtract `ONES`;
11. NOT;
12. AND `HIGHS`;
13. AND the loaded word to remove invalid lanes;
14. compare with zero;
15. branch to the match handler.

These are the 15 base operations. On a straddle, each `Wsub` also performs the one-operation ordinary-polarity filter and two-operation adjacent-polarity filter described above.

The handler locates the highest marked lane with an executable three-decision tree (six charged compare/branch operations), extracts its tag and index, reconstructs `F` and `a0`, clears the marker, updates the counter, and compares/branches on the remaining marker mask. The body is inlined with the separately charged post-filter. These twelve operations after lane selection include one conservative spare, giving 18 per match. Every marked lane is processed. The interpreter exhausted all 127 nonempty marker subsets and obtained exactly `18*popcount(mask)` operations with correct descending-lane outputs. The static checker exhausted all `7*512*512 = 1,835,008` base lane cases and 35,840 `q=507..511` ordinary/adjacent polarity cases with zero mismatch. Its v3 source/result SHA-256 values are `222276174d44510fe3a89fe333be8d82a68c6b62697d575801ddd130d5b105cd` and `0032fe3964ac3c1cdc3dee481d1f25e13f35f5601d87daffc784718b44c379fd`. The declared reduced experiment also compares the complete emitted claw set with an independent sorted retained-entry search.

An independent C validation exhausted 529,408 contextual bucket cases across every low-nine-bit query and tag, both bucket roles, and top-of-word wrap. The unfiltered modular query produced 40 false markers; the polarity filters produced zero false markers, zero missed matches and zero mismatches. A separate real-P1 run built the full `2^26`-candidate table for a seed-derived 38-round chaining value and scanned `2^20` consecutive `u` words: 2,095,838 raw markers, 20,202 polarity rejections, 2,075,636 exact full-word claws, and zero residual contextual errors. The C source, static binary, report and result hashes are `c6e637efdd878edcc5ee4d54d645c6b5f1cbdb3604b1b88456d7f3269f7792b1`, `410be92750a41cfd976e2f9a36fc665e8e54863319073b12442a71437b5dc8e6`, `b2d07be96b2b1f8d8bc47d5c29b4d861483e8ba044014f3de40b5fbb84b124c8`, and `c9efbd5f23cb5beb86f7ae903bc4cd2fa9bc006b92288ee7fca5642e8fa1304a`. This validates contextual query correctness, not the 256-bit word-RAM instruction prices or rare-event probabilities.

### A.14.3 Retention, work, and caps

For one bucket, `X ~ Binomial(2^26,2^-23)`. Direct finite recurrence gives

```text
E[min(X,7)]                 = 6.33626861212226023369
retained fraction           = 0.79203357651528252921
expected retained entries   = 53,152,473.5697976892
claws per scan word         = 160*E[retained]/2^32
                             = 1.98008394128820632303
```

The post-filter mean remains `10.1145230224` operations per claw and `q_pf = 2^-16.1876724293`. With 40 ordinary bucket lookups per `u`, a straddle probability `5/512` for each of 20 heads, 18 operations per emitted match, and a longest-path step 3b of 3,014 operations,

```text
fixed per u                  = 13 + 20*5 + 40*15 = 713
straddle mean per u          = 20*(5/512)*(1 + 2*15 + 6) = 7.2265625
per_u                        = 775.9756342062506 operations
wbar                         = C + 75 + 2^23*(5+48)
                               + 2^26*80 + 2^32*per_u
                             = 3,338,603,279,555.705 operations
```

The independent build inventory is 46 common operations per insert, 10 extra for each initially filled lane, 2 per reservoir call, 16 per bounded-draw attempt including its cap counter, and 12 per replacement. Exact binomial sums give 13,956,390.43 reservoir calls, 14,389,032.51 draws, and 10,418,697.71 replacements per chaining value. The resulting mean is 59.6299 operations per insert before normalization, or 65.6299 when the 48-operation bucket pass is amortized; the ledger uses the larger bound 80 plus the separate 48-operation pass. The capped maximum is 2,108 operations for one insert, rounded up to 2,200, and normalization uses 64 in the maximum. The scan maximum lets all four queried buckets per head contain seven matches that reach the longest post-filter path and step 3b. Thus

```text
maximum claws per u          = 20*4*7 = 560
umax                         = 1,748,653 operations per u
vmax = OVER                  = 7,510,555,665,369,843 operations
```

Let `X` be one bucket's exact binomial population. The count-overflow union per chaining value is `2^23 Pr[X>=128] = 3.066e-97`. For arrival `n`, let `r_n = 1 - floor(128/n)n/128` be one table-draw rejection probability. The exact rejection-cap union is

```text
2^23 * sum_(n=8)^127 Pr[X>=n] * r_n^128
  = 7.752e-69 per chaining value.
```

Across all claimed chaining values the respective bounds are `4.16e-81 = 2^-267.02` and `1.06e-52 = 2^-172.67`. The procedure fails closed and restarts after either event. Both bounds, together with the Bernstein probability below `2^-1011`, fit inside the separately subtracted `2^-60` exceptional reserve. All work before an abort is covered by the 2,200-operation insertion maximum and the one-chaining-value overshoot.

For H3, the number of disjoint-endpoint groups is deterministically no larger than every possible match lane,

```text
G_max = 2^32 * 20 heads * 4 bucket probes/head * 7 lanes
      = 2,405,181,685,760.
q3r * G_max = 2^-30.2717 < 2^-7.5.
```

Under the stated H3 premise that disjoint groups are independent Bernoulli trials with common probability `q3r`, this gives `E[J(J-1)]/E[J] <= q3r G_max`; no second-moment measurement from the parent's different table is transferred. Using the resulting `1-2^-8.5` Bonferroni factor and all `U=2^32` distinct scan words, the least integer satisfying the complete lower bound is

```text
N_CV                         = 13,563,485,112,848,343
V_MAX                        = 45,283,786,845,168,593,848,856,595,641
Bernstein cap probability    < 2^-1012.620
success lower bound          = 0.3900000000000000081...
```

The allowances and final verification are inherited and charged in full. Therefore

```text
N = (2^78 + 2^74 + 2^70)*2728 + V_MAX + OVER + (6*2728 + 1600)
  = 46,163,025,371,155,672,168,279,186,908 ordinary operations
time_log2 = log2(N/2728) = 83.8070965043...
claim.time_log2              = 83.80710 (rounded upward)
```

### A.14.4 Memory and projected score

The main bucket table is `2^23 * 32 = 268,435,456` bytes, the same allocation size as the parent's packed table. The projection starts from the parent's measured full-table process peak, 270,565,376 bytes, then adds the two tables absent from that process:

```text
query broadcast: 512 * 32 bytes       = 16,384
exact-draw table: 128 * 128 bytes      = 16,384
projected peak                         = 270,598,144 bytes
log2(projected peak)                   = 28.0115767032...
claim.memory_log2_bytes                = 28.01158
projected scalar bound                 = 83.80710 + 8.01158
                                       = 91.81868
gain from parent score 91.94860        = 0.12992 bit
```

**Full-scale native table evidence.** A standalone static C harness allocated and touched the exact full-size table set: `2^23` 256-bit bucket words (`268,435,456` bytes), 512 256-bit query-broadcast words (`16,384` bytes), and the packed `128*128` rejection table (`16,384` bytes), totaling `268,468,224` declared bytes. It processed all `67,108,864` candidates through the 252-bit build layout, exact rejection-sampled reservoir replacement, and in-place conversion to the 255-bit guarded query layout. Its full validation pass recomputed the deterministic `F(index)` for every retained lane and checked bucket and tag placement, unique retained indices within a bucket, preservation through normalization, validity guards, the spare high bit, and both auxiliary tables.

Two executions in the pinned organizer image, with no network, a read-only mount, uid 65534, no capabilities, one CPU, and bounded memory/process resources, completed with zero validation or auxiliary-table errors, zero count-overflow aborts, and zero rejection-cap aborts. After memory and timing fields were removed, their complete output documents were byte-identical. Each processed `2^26` candidates and retained `53,152,689` entries; it made `13,956,175` reservoir calls, `14,389,751` draws and `10,418,557` replacements, with maximum bucket population 26 and checksums `240525f6b99f4683/fa4296a4dc3f2893`. The cgroup peaks were `270,151,680` and `269,668,352` bytes; the larger is `2^28.009194413` and lies 446,464 bytes below the declared `270,598,144`-byte bound.

The frozen harness source SHA-256 is `9e7672f309f6e2b4c558c01fd05485e075ee09d522f54aabaec6b5084f5e2262`, its byte-identical static binary is `3d4c47c2266ad8e72bea3b5db02dde90adf071da18a3fb023fc6604adfbe10d5`, and the evidence report SHA-256 is `d240f4c682ff25b00020200e1324970f1b74ef252d08f226ee0ca45e02c5a655`. The deterministic run document SHA-256 is `7f13736ff455800fb1039c8343ef77932de54f7efb441a97bef01df89ea2f52a`. The binary was never executed on the host.

This establishes the full-scale packing, allocation, normalization and table-process peak for the deterministic harness. Its `F(index)` generator is not the SHA construction, and the harness omits the full SHA traces, post-filters and proof advice. It therefore supplies no evidence for `q_pf`, `q3`, H3, collision success, or the claimed 15/18/80 word-RAM operation counts. The memory claim remains the more conservative parent-process projection plus both explicit tables, and at that historical v3 stage the complete-solver state had not yet been integrated; A.15 supersedes this limitation.

### A.14.5 Historical v3 evidence and obligations (superseded by A.15)

`p1-bucket7-r38` is the declared reduced organizer-Docker experiment. Four seed-drawn chaining values build the exact packed reservoir at `2^16` candidates and `2^13` buckets, normalize it, scan `2^12` distinct `u` words, and compare every polarity-filtered claw with an independent sorted search over the retained entries. It rebuilds the real `E16` and inherited post-filter flags for every claw. Trial 4 checks step 3b on the P8 pair; trial 5 exhausts the executable handler over all 127 nonempty marker subsets; trial 6 exhausts 35,840 `q=507..511` ordinary/adjacent polarity cases. No collision is expected at this size, and any returned messages are independently checked against the selected complete-hash target.

The final frozen organizer run used participant-source SHA-256 `1f2b96a47f1a03d9106039d84f8d58dcd57b92195b0be6b4be193dfb948e7dfd`. It replayed byte-identically in two fresh networkless containers. The four retained populations were 52,625, 52,146, 52,188, and 52,422. Their emitted claw counts were 11, 5, 5, and 6. Every count equaled the independent reference and the distinct-pair count; all retained-claw set, real-`E16`, and real-post-filter mismatch counts were zero. Trial 4 accepted the P8 pair and counted 3,014 step-3b operations. Trial 5 exhausted all 127 nonempty handler marker subsets with zero output or 18-operation count mismatches. Trial 6 covered all 35,840 polarity cases with zero mismatches. The trusted report has SHA-256 `efc7d9e100a54d131af06e2ba8ef96e4e7f10ebd0cf1d1dff236874efcb52af8`. These are structural observations at the declared reduced scale, not full-scale probability or native-cost evidence.

Historical v3 checklist: A.14 originally called for emitted query review, independent build/normalization review, a full-scale post-filter/group panel, and a simultaneous-state bound. A.15 supersedes that checklist: it integrates the completed panel, exact ordered query IR, conservative build/normalization inventories, and the explicit complete-online cap. Current limitations are stated only in A.15.7.

The shared benchmark base still contains `experiments/a0p38.py`, but the restored `711c4bf8` candidate supersedes its manifest with the two P1 experiments and does not declare that file. The candidate removes the stale undeclared source because current intake rejects additional participant programs. No active `claim.json` evidence reference points to either `a0p-*` experiment. The A0-variant statistical records used by H2 are reproduced in Appendices Q and R and inherited through the declared parent submissions; deleting the obsolete executable does not delete or reclassify that evidence.

## Appendix A.15. Binding bucket7 construction, corrected joint law and typed lowering

This appendix is normative. It supersedes every table price, memory figure,
score, q3-law description and readiness statement in Sections 3--10,
Appendices A and A.13, and the historical Appendix A.14. The target, the P8
data, the P1 family, the collision predicate, the registered list-law q3
evidence and the preprocessing allowances remain inherited. `ready` means
ready for exploratory review; it does not assert qualification or acceptance.

### A.15.1 The r38-specific common-query identity

The twenty row-16 heads in `R16H` have one common residue:

```text
len(R16H) = 20
{H mod 512 : H in R16H} = {0x120}.
```

For a scan word `u`, set `P = sigma0(u)-u` modulo `2^32` and
`W_H = H-P` modulo `2^32`. Every target has the same low nine bits,

```text
q = (0x120-P) mod 512.
```

The second target `W_H+1024` has the same low nine bits. One mask, one
straddle decision and one 256-bit `QREP[q]` load therefore serve all forty
ordinary probes. This identity uses the actual r38 head set; it is not a
generic bucket-table optimization.

The straddle frequency is exactly `5/512`. In the low nine output bits of
`sigma0(u)`, the `ROTR18` term maps input bits 18 through 26 bijectively to
output bits 0 through 8. Those bits occur in neither `u mod 512` nor the
low-nine-bit `ROTR7` and `SHR3` terms. Holding the other bits fixed and varying
bits 18 through 26 runs `P mod 512`, and therefore `q`, through all 512 values.
The complete `2^32` scan has exactly five straddle residues.

With `q` and `QREP[q]` present, an ordinary lookup costs 12 operations. An
adjacent lookup costs 14, including `ADD 1` and `AND (2^23-1)` for wraparound.
A straddle applies one polarity `AND` to each of 40 ordinary results and
`NOT` plus `AND` to each of 40 adjacent results, or 120 polarity operations.
The 19-operation handler includes the selector-leaf jump into the site's
inlined post-filter body.

### A.15.2 Explicit 32-bit semantics on the 256-bit machine

The benchmark's `ADD` and `SUB` are modulo `2^256`; a Python or C `uint32`
expression does not license an implicit 32-bit reduction. The binding lowering
therefore emits an `AND MASK32` at every boundary where an arithmetic result is
consumed as a SHA-256 word, enters a nonlinear word operation, or supplies a
32-bit table target.

Straight ADD/SUB chains may delay the mask until that boundary. This is exact:
for any integers `x,y`, reducing `x+y` or `x-y` after each operation and
reducing once after an uninterrupted ADD/SUB chain give the same residue
modulo `2^32`. The wide transient `P=sigma0(u)-u` is used only in `H-P`, whose
result is immediately masked; the intermediate `F` additions/subtractions are
likewise masked before any shift or table extraction. No shift, rotate,
comparison, address calculation or Boolean word operation consumes an
unreduced transient. The typed verifier checks this boundary placement and
the direct modulo-`2^32` formulas.

The build masks `E0` before `Sigma1(E0)` and masks the final `F(a0)` before
extracting its bucket and tag. The scan masks `u0+n`, masks every `H-P`, and
masks every `W+1024`. There are two such boundaries in the build prefix, two
in the scan prefix and 39 in each fully unrolled scan arm. The ordinary fixed
inventory consequently becomes

```text
scan prefix + ordinary arm       = 579 operations per u
straddle arm minus ordinary arm  = 681 operations
mean straddle work               = (5/512)*681.
```

The counted inline macros receive the same treatment. Post-filter segment
costs first receive the missing C1 top-bit AND, changing the unmasked
baseline to `8/22/29/30`, then gain `2/3/4/3` masks and become
`10/25/33/33`. C1's ten operations are three arithmetic operations plus
one a1 reduction, E5 add plus reduction, top-bit AND, compare, branch and
the work-counter add. The AND is separate from the E5 reduction. Step 2
materializes 32 modular outputs across two members; rounds 16 through 37
materialize `2*22*3=132`; the longest step-3b path is therefore
`3014+164=3178`. The CV-scalar setup receives a conservative 64-mask reserve
on top of its prior 39 operations, leaving 25 operations of slack even if
every old scalar operation required a reduction.

The Step-3b fixture explicitly charges the original e6 setup `500`, then
32 output masks; each paired round costs `100+6`; the last sixteen rounds
cost `1600+96` plus the 17-operation comparison. The P8 tests cost 296 and
the exit update costs one. Thus `500+32+22*(100+6)+296+17+1=3178`.
The frozen v2 source already had the equivalent 532/106 counters. Historical
3,014 refers to e6's unmasked fixture. V3 adds no further 164-operation
score charge. Its executable verifier inspects the actual fixture AST,
checks 1,025 post-filter inputs against real-word predicates and exact
segment counters, and executes the P8 pair to bind the fixture to the typed
`3178` contract. The stages charge `10/25/33/33` including counter updates.

All SHA sigma prices are now backed by eight legal 256-bit operations.
For BIG_S0 use rotations `a,b,c=2,13,22`; BIG_S1 uses `6,11,25`.
With zero-extended u32 input x, execute

```text
r0=ROTR256(x,a); r1=ROTR256(x,b); t=r0 XOR r1;
r2=ROTR256(x,c); y=t XOR r2;
z=y SHR 224; t=y XOR z; out=t AND MASK32.
```

SMALL_S0 uses `a,b=7,18` and replaces the third rotate by `x SHR 3`;
SMALL_S1 uses `17,19` and `x SHR 10`. Each list has exactly eight unit-cost
operations. A wide rotate of a u32 input has only a low piece and a wrapped
piece in the high 32 bits. The 224-bit fold moves that wrapped piece into
its 32-bit rotation position; the final AND deletes the high copy. Every
operation is GF(2)-linear. The verifier checks the instruction grammar,
unit prices, use-before-definition, constant shifts and MASK32, then checks
zero, every one of 32 basis vectors, and three edge values for each of four
sigmas. Equality on the basis certifies the full u32 domain. It also binds
each typed sigma macro's price to this expansion. Build and scan input
widths remain checked at their existing u32 boundaries. This proves the
cost-8 sigma contract, while post-filter and Step-3b internal cryptanalysis
remain inherited counted routines with the executed contracts above.

The executable regression includes the counterexample that invalidates the
old implicit-width lowering. For `u=0xffffffff`,

```text
sigma0(u)                 = 0x1fffffff
masked first-head target  = 0x2b02d320
masked target plus 1024   = 0x2b02d720.
```

Without the masks, the 256-bit subtraction retains a high carry and shifting
the target yields an out-of-table bucket. The verifier checks 164,160 target
cases, including this boundary, with zero mismatch against direct modulo-
`2^32` formulas. It also reconstructs every extra macro mask listed above.

### A.15.3 Correct online q3 law

Let `A` be the 53,096,854 values of `a1` satisfying `C1` and `C2`, and let
`R9` be the `2^26` values of `a0` in window 9. Define

```text
E = {(a1,a0) in A x R9 : G(a1,a0)}
g(a1) = #{a0 in R9 : G(a1,a0)}.
```

The online construction, before the independent `F7` average, samples
`(a1,a0)` uniformly in `A x R9` and conditions the pair on `G`. Its good-pair
law `P` is therefore uniform on the edges `E`; its `a1` marginal is
proportional to `g(a1)`.

The historical registered list generator used another law `Q`: choose `a1`
uniformly in `A`, then rejection-sample `a0` conditional on `G` for that fixed
`a1`. Thus

```text
P(a1,a0) = 1/|E|,
Q(a1,a0) = 1/(|A| g(a1)),
P/Q       = g(a1)/( |E|/|A| ).
```

These laws are not declared equal. Indeed, `|A|=53,096,854` is even while
`|E|=57,726,359,870,197` is odd, so `g` cannot be constant. The exhaustive
degree scanner embedded by hash in the experiment archive independently
reproduced

```text
|A|          = 53,096,854
|E|          = 57,726,359,870,197
min g(a1)    = 364,288
max g(a1)    = 1,798,400.
```

The worst-case density-ratio transfer would cost about 1.577 bits and is not
used. The binding H2 instead declares a separate 0.20-bit transfer allowance,
supported by the paired study below. This is a statistical heuristic, not an
identity or a theorem.

### A.15.4 Paired joint-law study and binding H2

`p1q3_joint.py` contains both exact samplers. The `P` sampler repeatedly draws
one uniform `a1` from `A` and one uniform `a0` from `R9`, restarting the whole
pair until `G`; the `Q` sampler holds a uniform `a1` fixed while rejection-
sampling `a0` until `G`. Each law uses a separately generated pool of 1,024
exact pairs. A paired sequential Monte Carlo replicate gives the two laws the
same initial seed and common prefix randomness, uses 64 particles and 96 tail proposals
per particle, and independently reconstructs every success through the
38-step relaxed semi-free-start event.

The source hash `9b243adfd8180dc62609b559f3c72b50171ff5574031a944679f1e0bd39de078`
was frozen before the counted study. The preregistration hash was
`a654b7c673963a0e1bc99c2de80f70ba08e0f1a58ba37b71d2b30dd7ab6dbce2`.
It excluded 48 earlier 48-tail scouts and one 96-tail timing scout, fixed 24
shards of 12 paired replicates, and required every shard and every rebuild to
be used. For shard `s`, it set

```text
R_s = log2(mean joint estimate / mean list estimate)
LB  = mean(R_s) - 2.4999*sd(R_s)/sqrt(24)
gate: LB >= -0.20 and zero rebuild failures.
```

The frozen result hash was
`78ced1280b359f81aae48c1b5d1fbfde31b4d8b480f210b697a2087b4c716bea`.
All 288 paired replicates completed with zero rebuild failures. The mean shard
ratio was `-0.01178256197`, its sample standard deviation was
`0.24631269890`, the preregistered one-sided 99% Student endpoint was
`-0.13747345694`, and the global pooled ratio was `-0.01638900427`. The
`-0.20` gate passed.

This study was designed after the law mismatch was found. The Student
calibration and extrapolation from finite seeded SMC runs to the deterministic
full SHA family remain part of score-critical H2. The two organizer-selected
public panels exercise the same correct sampler and verify all reconstructed
successes; their individual ratios are noisy supporting observations and are
not substituted for the preregistered bound.

The inherited registered list-law lower bound is `q3_Q >= 2^-96.0791`. After
the declared 0.20-bit law allowance, the binding online-joint bound is

```text
q3_P >= 2^-96.2791,
q0 = q3_P * 2^32/160 = 2^-71.6010280949...
```

The inherited level, relaxation-ratio and A0-to-P1 constructions retain their
stated joint confidence and limitations. The relaxation ratio was measured on
A0 and transferred to P1. The new law study addresses only `Q` versus `P`; it
does not turn any q3 premise into a proof.

The paired runs share the initial seed and prefix randomness. Tail choices
are path dependent: an `inF7` rejection skips the subsequent `e22` draw,
so later random positions, including later pool indices, may diverge.
There is no claim of an identical pool-index stream throughout the tail.

### A.15.5 Uniform-reservoir first moments

Let candidate `i` have bucket `B_i`, and let `S_i` indicate survival in the
seven-entry reservoir. Conditional on a bucket containing `n` occupants,
Algorithm R selects all occupants when `n<=7` and a uniform seven-subset when
`n>7`. The usual induction gives

```text
Pr[S_i=1 | bucket size n] = min(1,7/n).
```

Under H1 the bucket values are iid uniform and jointly independent of the P1
post-filter/tail labels, while the reservoir coins are fresh. For a fixed
candidate, the number `Y` of other bucket occupants is
`Binomial(2^26-1,2^-23)`, and

```text
rho = E[min(1,7/(1+Y))]
```

is common to every candidate and independent of every attached label. Hence
`E[S_i Z_i]=rho E[Z_i]` for any fixed good-pair or accepted-pair indicator
`Z_i`. This is a first-moment reduction. Reservoir membership is correlated
inside a bucket; no independent-retention claim is made.

The reduction preserves the online joint edge law `P`, not the historical
list law `Q`. Together with the 0.20-bit H2 allowance above, it supplies the
first moment used by the binding ledger. The exact transfer checker exhausts
small Algorithm-R distributions, every small ternary label assignment and
arbitrary correlated selected-set mixtures with rational arithmetic.

A frozen predeclared panel processed 200 real seed-derived chaining values,
the complete `2^26` build for each, and `2^20` scan words per value. It retained
10,631,835,913 entries and found 415,269,109 exact claws with zero structural
errors or cap aborts. Observed-to-exact cumulative-rate ratios were 1.000191
for C1, 0.999613 for C1-C2, 1.000054 for C1-C2-G and 0.998457 for all four
filters; every rate lay in its predeclared cluster-robust 99% interval. This
supports the first-moment extrapolation at its tested scale. It does not prove
the random-map premise or cover the full `2^32` scan or all `N_CV` values.

### A.15.6 H3 after correlated retention

For a fixed chaining value, expose the complete table, reservoir coins and
retained good-pair endpoint graph. Let `K` be its number of edges and `L` the
number of connected components under sharing an `a0` or `u` endpoint. Choose
one deterministic representative per component. Ignoring other members can
only reduce success, but the first-moment loss must be charged. H3 declares

```text
E[L] >= (1-2^-9) E[K].
```

Under the random-incidence form of H1/H1-P1, the mean good degrees at the two
endpoint types are `160*q_pf` and `1.9800839412882063*q_pf`. Every loss `K-L`
can be charged to an unordered edge pair sharing an endpoint. The incidence
forecast is

```text
(160+1.9800839412882063)*q_pf/2 = 0.00108507... < 2^-9.
```

Multiplying by the frozen panel's 1.271481 all-four spread gives
`0.00137965... < 2^-9`; the panel itself lost 3 representatives among 5,555,
or `0.000540...`. This supports the premise, but the panel scans only `2^20`
words per chaining value and does not directly test full-scan repeated-`a0`
incidence.

Every representative occupies one physical match lane, so deterministically

```text
L <= G_max = 2^32*20*4*7 = 2,405,181,685,760.
```

The eligible `plausible_not_refuted` parent's H3 premise is inherited only for
the unchanged P1 tail:
conditional on the exposed selection sigma-field, endpoint-disjoint
representatives have independent acceptance indicators with a common
probability `p>=q0`. Couple them to iid Bernoulli(`q0`) proxies. Conditional on
`L`, the proxy count `J0` satisfies

```text
E[J0|L]       = q0 L,
E[J0(J0-1)|L] = q0^2 L(L-1) <= q0^2 G_max L.
```

Averaging over the correlated table selection gives

```text
E[J0(J0-1)]/E[J0] <= q0 G_max
                   = 2^-30.4717450779... .
```

Bonferroni and the group-loss premise then give

```text
Pr[success in one CV]
 >= q0 E[K] (1-2^-9) (1-q0*G_max/2)
 >  q0 E[K] (1-2^-8.5).
```

The combined multiplicative factor is `0.998046874664...`, while
`1-2^-8.5` is `0.997237864135...`. This argument removes any need for
independent reservoir membership or the parent's measured 1.246 population
factor. It does not prove the two remaining H3 premises: full-event
independence/common probability for endpoint-disjoint pairs, and the `2^-9`
representative-loss extrapolation. The unchanged full-event premise was judged
plausible for parent submission `711c4bf8-5c69-4f9c-bd1b-fe983984a096`; this
appendix supplies the reduction needed for the changed table rather than
claiming a new independence experiment.

### A.15.7 Binding ledger and success amplification

With explicit reductions and the 0.20-bit q3-law allowance, the binding values
are

```text
retained per bucket                 6.33626861212226023369
claws per u                         1.98008394128820632303
post-filter mean per claw           13.53957415679178096
per_u                               650.16578565524589139
wbar                                2,798,254,094,578.4270344
umax                                1,848,140
vmax = OVER                         7,937,849,076,747,059
N_CV                                15,580,353,037,155,665
V_MAX                               43,598,451,930,628,831,379,450,820,912
Bernstein exponent                  below 2^-922.45
success lower bound                 0.3900000000000000018...
```

The mean formula is

```text
579 + (5/512)*681
+ claws_per_u * (19 + postfilter_mean + q_pf*3178).
```

Build work is charged at 80 mean operations per insert; reset plus
normalization costs `5+48` per bucket; CV setup is `2728+139`. The maximum
uses 2,200 operations per insert, `5+64` per bucket and the corrected maximum
per scan word. Count-cap and rejection-cap failure probabilities are included
in the global exception reserve, and the cap test still fails closed.

Charging all preprocessing, the online cap, one-CV overshoot and final
verification gives

```text
N = (2^78+2^74+2^70)*2728 + V_MAX + OVER + (6*2728+1600)
  = 44,477,690,456,616,336,992,284,789,395 operations
time_log2 = log2(N/2728)
          = 83.75344060461332866...
claim.time_log2 = 83.75345 (rounded upward).
```

The score from rounded claims is

```text
83.75345 + (28.094-20) = 91.84745,
```

which is 0.10115 bit below the parent score 91.94860. Applying the exact
worst-case density-ratio penalty instead of the declared study-backed 0.20-bit
allowance would give about 93.20680 and would not improve the parent.

### A.15.8 Complete lowering, memory and package execution

The organizer-executed certificate contains the complete typed build CFG,
normalization, both fully unrolled scan arms, all 120 handler/post-filter/
conditional-step3b sites, continuation contracts, ledger and aligned memory
map. It materializes 2,101 base IR operations and checks fill, replacement,
no-replacement, rejected-draw, cap, normalization, ordinary and straddle
paths. Its semantic suites cover all 16,256 rejection cells, 20,480 common-
head cases, 1,835,008 ordinary lane/tag/query cases, 17,920 adjacent cases,
all `2^23` adjacent addresses, 127 marker subsets and 128 normalization counts.

The exact table set is 268,468,224 bytes. The corrected source expands to at
most 10,916,032 bytes, so the executable cell is increased from 10 MiB to
11 MiB. The online layout is

| item | bytes |
|---|---:|
| table set | 268,468,224 |
| fully inlined executable reserve | 11,534,336 |
| bounded single-thread stack | 1,048,576 |
| advice, normalization metadata and constants | 65,536 |
| two traces, schedules, messages, counters and registers | 65,536 |
| allocator/runtime reserve | 4,194,304 |
| remaining messages, output, alignment and scratch | 917,504 |
| **online cap** | **286,294,016** |

The binding whole-computation peak remains the independently reported Step-1
peak, `279,720 KB = 286,433,280 bytes = 2^28.0936238847...`, rounded upward
to `memory_log2_bytes=28.094`. The corrected online cap has 139,264 bytes of
headroom. The absent `2^27.7542` receipt is not used.

V3's exact degree scan is also inside this whole-computation scope. It
stores one u32 rank checkpoint per 128 domain positions, exactly
`(2^32/128+1)*4=134,217,732` bytes, and recomputes at most 127 predicate
bits per endpoint. It stores no bitset and uses one thread. Rank and
wrapped-interval boundary tests run before the exhaustive pass. Two fresh
networkless pinned-container executions, with the complete container capped
at 286,433,280 bytes and a 1 MiB stack limit, reproduced the exact counts.
The measured process peaks were 131,072 and 130,692 KiB, both below the
binding peak. The static binary is below 1 MiB. The old 805,306,372-byte
bitset/prefix implementation is not part of the v3 construction or its
reproducible evidence path. All scanner work is covered by the unchanged
development allowance; v3 does not claim a resource-scope exclusion.

The single declared experiment program is a hash-checked LZMA transport for
the exact readable construction, q3 sampler, transfer checker, typed program,
typed verifier and exhaustive degree-scan C source. It is below intake's
65,536-byte aggregate source limit. The archive checks every constituent hash
before dispatch; the lowering experiment executes the decompressed typed
program and verifier rather than accepting stored output. The readable sources
are reproduced in A.16 for direct review.

The organizer entries have deliberately separated scopes:

- `p1-online-r38`, `p1-q3-r38` and `p1-bucket7-r38` check the construction,
  real SHA predicates and reduced table semantics.
- `p1-law-joint-a-r38` and `p1-law-joint-b-r38` exercise the correct online
  sampler and the historical list sampler with independent pools and rebuild
  every relaxed-event success.
- `p1-reservoir-transfer-r38` executes finite exact transfer identities.
- `p1-bucket7-lowering-r38` executes the complete typed lowering, explicit
  reduction checks, ledger and memory map.

No organizer event frequency is treated as an iid collision-probability
estimate. The lowering is an abstract complete word-RAM certificate, not a
physical `2^32` scan. H1, the registered/paired H2 extrapolations, and the two
stated H3 premises remain score-critical heuristics.

## Appendix A.16. Embedded-source inventory

The declared source contains a canonical JSON map of the exact Python modules,
compressed with LZMA only to fit the closed 65,536-byte source limit. The wrapper
checks every module SHA-256 before importing it in the isolated container. The
full untrusted source text is included in the trusted experiment report; it is
not duplicated here because doing so would duplicate the same evidence in the
bounded judge packet.

| module | SHA-256 | purpose |
|---|---|---|
| `p1claw` | `f8ae3bf1f295ab117b17c5daa773657344c9c2d968a126b6da5b69366dfa3853` | SHA-256 reference, P8/P1 data, reduced construction fixtures and actual Step-3b |
| `p1q3` | `9b243adfd8180dc62609b559f3c72b50171ff5574031a944679f1e0bd39de078` | correct joint-law and historical list-law diagnostic samplers |
| `program` | `f9a3932e875789528264d5cea70e3c64ad6185f51875821cd09d79ee23599d78` | remediation-v3 typed word-RAM program with explicit u32 boundaries |
| `verify` | `dbf5f1fbdc61bfab69079ae8996cdd38ab1c031f4c8b3d1dc83982331ed9bfc5` | CFG, semantic, body-charge, u32, ledger and memory checks |
| `transfer` | `a461a9e12098cd9b2bbec6029af28fe90011fccf49b197febfe7fd9d115f528c` | reservoir/H3 finite checker plus final block-4/address-chain checker |

For the bounded joint-law diagnostics, the final wrapper sets four replicates,
independently generated 256-pair pools, and the matching df=3 Student coefficient
4.5407, as declared in the experiment manifest. This does not alter the frozen 288-replicate study or the
binding 0.20-bit H2 allowance. The C degree scanner is reproduced by its compact
algorithm and records in A.17; it is not imported by participant Python. Appendix
A.18 gives the complete final construction, cost equations and limitations.

## Appendix A.17. Frozen joint-law study record

The historical preregistration and study results were frozen before the overlay was assembled and are reproduced verbatim. Section A.17.3 is the fresh v3 low-memory degree rerun. This makes the H2 transfer study reviewable without fetching citations. The SMC implementation itself is in A.16.2 and the exhaustive degree scanner is in A.16.6.

V3 coupling erratum: the preregistration below is reproduced verbatim to
preserve its original hash and timing. Its phrase "the same pool-index stream"
is too strong. Both laws start with the same seed and share prefix randomness;
law-dependent `inF7` rejection can skip an `e22` draw and desynchronize later
pool indices. The frozen source and study values are unchanged. The Student
statistic does not require identical later pool choices. Its calibration and
SMC transfer remain explicit heuristics.

### A.17.1 Preregistration

SHA-256 `a654b7c673963a0e1bc99c2de80f70ba08e0f1a58ba37b71d2b30dd7ab6dbce2`.

```text
# R38 P1 joint-law transfer study

Written 2026-10-22T12:07:11+02:00 before generating or running any study seed.
The 48-replicate `NT_R=48` scouts and the one `NT_R=96` timing scout are
development observations and are excluded.

## Frozen source and laws

`sources/p1q3_joint.py` SHA-256:
`9b243adfd8180dc62609b559f3c72b50171ff5574031a944679f1e0bd39de078`.

The historical list law first draws `a1` uniformly from the 53,096,854 values
passing C1 and C2, then draws `a0` uniformly from the R9 values passing G for
that fixed `a1`.  The online joint law draws `(a1,a0)` uniformly from
`(C1&C2) x R9`, then conditions the pair on G.  Both pools contain 1,024 exact
rejection samples.  Each paired SMC replicate uses the same prefix seed and
the same pool-index stream for both laws.  It uses 64 particles and 96 tail
proposals per particle.

## Frozen run

- 24 shards numbered 0 through 23.
- Each shard contains trials 0 through 11; later request trials do no work.
- Experiment ID: `p1-law-holdout-v1-shardNN-r38` with two-digit `NN`.
- Trial seed: SHA-256 of ASCII
  `r38-law-holdout-v1|shard=NN|trial=II`, with two-digit `NN` and `II`.
- Every shard must exit successfully with zero joint/list rebuild failures.
- Every completed shard is used; no replacement, stopping rule, or interim
  inspection is allowed.

## Frozen statistic and decision

For shard `s`, let `J_s` and `L_s` be the arithmetic means of its twelve
linear-scale joint-law and list-law SMC estimates.  Set
`R_s=log2(J_s/L_s)`; a zero numerator is `-128` and a zero denominator voids
the study.  Over all 24 `R_s`, compute the mean, sample standard deviation and
the one-sided 99% Student lower endpoint

```text
LB = mean(R_s) - 2.4999 * sd(R_s) / sqrt(24).
```

Also report the global pooled ratio
`log2(sum_s J_s / sum_s L_s)` and all shard values.  The 0.20-bit law-transfer
penalty is supported by this study only if `LB >= -0.20`, every rebuild count
is zero, and the exact degree scan independently reproduces
`|C1&C2|=53,096,854` and total incidence `57,726,359,870,197`.

This is a post-discovery remediation study.  Student calibration and transfer
from its finite seeded SMC population to the full deterministic SHA family
remain an explicitly declared heuristic even if the gate passes.
```

### A.17.2 Aggregated 24-shard result

SHA-256 `78ced1280b359f81aae48c1b5d1fbfde31b4d8b480f210b697a2087b4c716bea`.

```json
{
  "all_rebuild_failures": 0,
  "gate_floor": -0.2,
  "gate_pass": true,
  "global_pooled_log2_ratio": -0.016389004266560564,
  "mean_shard_log2_ratio": -0.011782561971074879,
  "paired_replicates": 288,
  "preregistered_shards": 24,
  "schema": "r38-p1-law-transfer-study-v1",
  "shard_log2_ratio_sd": 0.24631269889779223,
  "shards": [
    {
      "joint_attempts": 62314,
      "joint_failed": 0,
      "joint_log2": -96.05456519365323,
      "list_attempts": 78872,
      "list_failed": 0,
      "list_log2": -95.70377666103074,
      "ratio_log2": -0.3507885326224882,
      "shard": 0
    },
    {
      "joint_attempts": 60833,
      "joint_failed": 0,
      "joint_log2": -96.60190619913875,
      "list_attempts": 81701,
      "list_failed": 0,
      "list_log2": -96.55102932190667,
      "ratio_log2": -0.05087687723208473,
      "shard": 1
    },
    {
      "joint_attempts": 64586,
      "joint_failed": 0,
      "joint_log2": -95.92131985425588,
      "list_attempts": 83356,
      "list_failed": 0,
      "list_log2": -96.03242598354929,
      "ratio_log2": 0.11110612929340415,
      "shard": 2
    },
    {
      "joint_attempts": 63060,
      "joint_failed": 0,
      "joint_log2": -96.27706753140848,
      "list_attempts": 83413,
      "list_failed": 0,
      "list_log2": -96.51722079220262,
      "ratio_log2": 0.24015326079414487,
      "shard": 3
    },
    {
      "joint_attempts": 64458,
      "joint_failed": 0,
      "joint_log2": -96.27229415137457,
      "list_attempts": 81172,
      "list_failed": 0,
      "list_log2": -96.64744464949196,
      "ratio_log2": 0.37515049811739254,
      "shard": 4
    },
    {
      "joint_attempts": 63213,
      "joint_failed": 0,
      "joint_log2": -96.37483653835162,
      "list_attempts": 88715,
      "list_failed": 0,
      "list_log2": -96.19405768982968,
      "ratio_log2": -0.180778848521939,
      "shard": 5
    },
    {
      "joint_attempts": 65971,
      "joint_failed": 0,
      "joint_log2": -96.59294171345033,
      "list_attempts": 86153,
      "list_failed": 0,
      "list_log2": -96.5149456630171,
      "ratio_log2": -0.077996050433228,
      "shard": 6
    },
    {
      "joint_attempts": 63024,
      "joint_failed": 0,
      "joint_log2": -95.8334361173172,
      "list_attempts": 83071,
      "list_failed": 0,
      "list_log2": -95.7596242874167,
      "ratio_log2": -0.07381182990050676,
      "shard": 7
    },
    {
      "joint_attempts": 58876,
      "joint_failed": 0,
      "joint_log2": -96.42571821323716,
      "list_attempts": 84252,
      "list_failed": 0,
      "list_log2": -96.2010457050291,
      "ratio_log2": -0.22467250820805854,
      "shard": 8
    },
    {
      "joint_attempts": 64649,
      "joint_failed": 0,
      "joint_log2": -96.80113255913282,
      "list_attempts": 78083,
      "list_failed": 0,
      "list_log2": -96.90757835556981,
      "ratio_log2": 0.10644579643698653,
      "shard": 9
    },
    {
      "joint_attempts": 67075,
      "joint_failed": 0,
      "joint_log2": -96.16068959780391,
      "list_attempts": 85584,
      "list_failed": 0,
      "list_log2": -96.43419627533373,
      "ratio_log2": 0.2735066775298237,
      "shard": 10
    },
    {
      "joint_attempts": 62947,
      "joint_failed": 0,
      "joint_log2": -96.55242382994638,
      "list_attempts": 85097,
      "list_failed": 0,
      "list_log2": -96.54244820569326,
      "ratio_log2": -0.009975624253115612,
      "shard": 11
    },
    {
      "joint_attempts": 64133,
      "joint_failed": 0,
      "joint_log2": -96.5462979105128,
      "list_attempts": 86211,
      "list_failed": 0,
      "list_log2": -96.26653712340354,
      "ratio_log2": -0.27976078710926805,
      "shard": 12
    },
    {
      "joint_attempts": 67528,
      "joint_failed": 0,
      "joint_log2": -96.3601098488824,
      "list_attempts": 84285,
      "list_failed": 0,
      "list_log2": -96.41798402328801,
      "ratio_log2": 0.057874174405611614,
      "shard": 13
    },
    {
      "joint_attempts": 64649,
      "joint_failed": 0,
      "joint_log2": -96.73533156447006,
      "list_attempts": 87562,
      "list_failed": 0,
      "list_log2": -96.64642086393452,
      "ratio_log2": -0.08891070053553576,
      "shard": 14
    },
    {
      "joint_attempts": 62124,
      "joint_failed": 0,
      "joint_log2": -96.57098257611719,
      "list_attempts": 80336,
      "list_failed": 0,
      "list_log2": -96.03624293892618,
      "ratio_log2": -0.5347396371910096,
      "shard": 15
    },
    {
      "joint_attempts": 62842,
      "joint_failed": 0,
      "joint_log2": -96.73120194396981,
      "list_attempts": 81804,
      "list_failed": 0,
      "list_log2": -96.47896950606139,
      "ratio_log2": -0.25223243790841804,
      "shard": 16
    },
    {
      "joint_attempts": 64255,
      "joint_failed": 0,
      "joint_log2": -95.87921947283944,
      "list_attempts": 83714,
      "list_failed": 0,
      "list_log2": -95.820237679904,
      "ratio_log2": -0.05898179293544089,
      "shard": 17
    },
    {
      "joint_attempts": 66076,
      "joint_failed": 0,
      "joint_log2": -96.60799864860368,
      "list_attempts": 85856,
      "list_failed": 0,
      "list_log2": -96.50682198545391,
      "ratio_log2": -0.10117666314977218,
      "shard": 18
    },
    {
      "joint_attempts": 61166,
      "joint_failed": 0,
      "joint_log2": -96.40367850717863,
      "list_attempts": 80686,
      "list_failed": 0,
      "list_log2": -96.09978781834464,
      "ratio_log2": -0.30389068883398807,
      "shard": 19
    },
    {
      "joint_attempts": 60234,
      "joint_failed": 0,
      "joint_log2": -96.12981027040588,
      "list_attempts": 86594,
      "list_failed": 0,
      "list_log2": -96.43697360787355,
      "ratio_log2": 0.30716333746767094,
      "shard": 20
    },
    {
      "joint_attempts": 61780,
      "joint_failed": 0,
      "joint_log2": -96.54629108844382,
      "list_attempts": 78193,
      "list_failed": 0,
      "list_log2": -96.8321707827619,
      "ratio_log2": 0.2858796943180834,
      "shard": 21
    },
    {
      "joint_attempts": 66075,
      "joint_failed": 0,
      "joint_log2": -96.13589373270571,
      "list_attempts": 81050,
      "list_failed": 0,
      "list_log2": -96.3403616758626,
      "ratio_log2": 0.20446794315688493,
      "shard": 22
    },
    {
      "joint_attempts": 59304,
      "joint_failed": 0,
      "joint_log2": -95.8766549880369,
      "list_attempts": 84554,
      "list_failed": 0,
      "list_log2": -96.22071896804596,
      "ratio_log2": 0.34406398000905364,
      "shard": 23
    }
  ],
  "student_lower_log2_ratio": -0.13747345693986754,
  "student_t99_df23": 2.4999,
  "tail_proposals_per_particle": 96
}
```

### A.17.3 Exhaustive low-memory degree result

The source in A.16.6 has SHA-256 `6f5c3b0a32c06f6e8a01e855ea896fc9a9d3058a15d2a76e7f7baf374f4bf42e`.
It is compiled by `cc -O3 -static -std=c11 -Wall -Wextra -Werror` and
invoked with constants `df1a2d2b 88887ba8 8cb35ecd 08001a4c 0ff9ffdf
23206eab 82120040 11cdedb6`. The matching construction independently derives
these constants from the P8 pair.

The scanner streams the complete 2^32 G predicate domain into u32 rank
checkpoints every 128 positions and then exhausts every C1/C2 candidate.
It reconstructs rank tails directly and handles modular interval wrap exactly.
Its only domain-sized allocation is 134,217,732 bytes. Two fresh networkless
containers used the organizer-pinned image
`python:3.12.12-slim-bookworm@sha256:2986c55feb36e6cae00fa1fefb454283e4b33f35e75ff8bdd123b134130be301`,
one CPU, a 1 MiB stack, read-only mounts, no privileges, and a complete
286,433,280-byte memory/swap cap. Both completed successfully with the
byte-identical output below. Process max RSS was 131,072 and 130,692 KiB.
These are native-C evidence runs under the same pinned networkless isolation
policy, distinct from the seven organizer Python pair experiments. Their
counts are participant evidence, not organizer-verified collision events.

```json
{"global_g":68157440,"a1_count":53096854,"edge_count":57726359870197,"degree_min":364288,"degree_max":1798400}
```

Output SHA-256 `be74462c67db994cad7cf16df4f4a2debcdb355f1987ab828082320068a19396`.
The original 768 MiB scanner is superseded. No evidence-only memory exclusion
is used. The unchanged development allowance covers these exhaustive passes.

## Appendix A.18. Binding four-bucket transpose and direct physical-address chain

This appendix is the final normative overlay for the table representation, scan
lowering, operation ledger, code bound, memory map, experiment transport and
score. Appendix A.15 remains normative for the target, Algorithm R, the online
joint law, the `q3_P >= 2^-96.2791` allowance, the H3 reduction, preprocessing
charges and success amplification, except where the present appendix replaces
its table and resource arithmetic. All earlier prices and scores are historical.

The final claims are

```text
time_log2                 83.33780
memory_log2_bytes         28.094
normalized scalar score   91.43180
success probability       at least 0.39, under the unchanged disclosed premises
```

This is 0.51680 bit below the live incumbent score 91.94860. It is 0.41565 bit
below remediation v3's rounded score 91.84745. Neither comparison changes the
cryptanalytic event or its heuristic probability premises.

### A.18.1 Four logical buckets in four physical words

The build and uniform seven-entry reservoir are unchanged. After the build,
each aligned block of four logical bucket words is converted in place to four
256-bit words. If the block begins at logical bucket `4j`, physical word 0 holds
the tags for buckets `4j` and `4j+2`, word 1 holds the tags for buckets `4j+1`
and `4j+3`, and words 2 and 3 hold their payload spill. Thus the tag-word map is

```text
T(b) = b & ~2                         (relative 256-bit-word index).
```

Each logical bucket contributes seven lanes. A lane has a nine-bit tag and a
validity guard, so one seven-lane group occupies 70 bits. The second group
starts at bit 71; bit 70 is always one and absorbs a borrow from the first
packed subtraction. Each tag word therefore uses `70+1+70=141` tag bits.
The remaining capacity is

```text
4*256 - 2*141 = 742 bits,
```

while 28 exact payload indices need only `28*26=728` bits. No identifier is
lost or reconstructed heuristically. Twenty-six payloads lie in one word; two
cross a fixed word boundary. The worst extraction path needs at most 27 word
operations, and the ledger charges 28 on every emitted match.

Let the fourteen lane shifts be

```text
S = (0,10,...,60, 71,81,...,131).
```

For a tag word `X` and query `q`, define `Q=sum(q<<s,s in S)`,
`D=(X-Q) mod 2^256`, `H=sum(1<<(s+9))`, `O=sum(1<<s)`, and
`B=sum((0x1ff & ~5)<<s)`. The marker expression is

```text
Z = ~( ((D & B) | H) - O ) & H & X.
```

Intersecting with the selected seven-lane group gives exactly those valid lanes
whose modular tag difference is in `{0,1,4,5}`. Intersecting further with `D`
selects the ordinary, non-wrapping representative (`tag >= q`); intersecting
with `~D` selects the adjacent representative (`tag < q`). The validity guards
remove unused lanes. The separator is necessary: with group zero empty,
`q=1`, and group-one tag 1, omitting bit 70 propagates a borrow into group one
and erases its true marker; setting bit 70 stops that borrow.

The combined old normalization and new transpose is deliberately overcharged at
512 operations per four-bucket block. The old normalization used 192. The
additional unrolled mapping, including four source address/loads, 28 fixed tag
and payload moves, four stores and the block tail, is bounded by 256, for an
emitted upper bound of 448. The 64-operation gap is charged in both mean and
maximum ledgers. Four copied guard words reproduce the first transposed block
after the main table.

### A.18.2 Exact query plans and branch census

All twenty row-16 heads have low thirteen bits `0x1320`. Subtracting the common
`P=sigma0(u)-u` therefore leaves all heads with the same low nine-bit query and
the same bucket class modulo four. For one head, the complete word-RAM costs of
the transposed query are

| path | class 0 | class 1 | class 2 | class 3 |
|---|---:|---:|---:|---:|
| ordinary head | 12 | 12 | 25 | 25 |
| straddle head | 26 | 41 | 55 | 40 |

The costs include address formation/load, the seven-operation packed marker
core, any singleton-group mask, the ordinary/adjacent polarity operation, and
the compare/branch. The four straddle residues query both sides of the modular
tag boundary.

A complete exhaustive census of every u32 scan word used this loop, where all
arithmetic is u32:

```c
for (uint64_t ux = 0; ux < (UINT64_C(1) << 32); ++ux) {
    uint32_t u = (uint32_t)ux;
    uint32_t p = ror32(u,7) ^ ror32(u,18) ^ (u >> 3);
    uint32_t w = UINT32_C(0x4b02d320) - (p - u);
    ++count[(w & 511u) >= 507u][(w >> 9) & 3u];
}
```

A one-thread execution and an independent 14-thread execution were
byte-identical after removing the thread-count field:

```text
ordinary:  1,063,256,064 in each of classes 0,1,2,3
straddle:     10,485,760 in each of classes 0,1,2,3
sum:       4,294,967,296
```

The C source SHA-256 is
`99ee913034d5b690c1d9bcea8658a15e0a282d4dd99199d29836b9ff175121e0`;
the common JSON SHA-256 is
`15348cf0d60711e35129f1a9f84ce8abfb25dc88a89090feabe6b7e6c4c46ce0`.
These are disclosed participant full-domain runs, not organizer-recomputed
collision predicates. The loop above is the complete census algorithm.

### A.18.3 Direct physical tag-address chain

Write `B=2^23`. For every head delta `d`, `d` is divisible by sixteen. Hence,
including modular wrap,

```text
T((b+d) mod B) = (T(b)+d) mod B.
```

The eight class/path arms end their last physical query at offsets

```text
ordinary:  0,0,4,4
straddle:  1,3,5,4.
```

If the next head gap is `g` and the current arm ends at offset `e`, the next
head starts with the three priced primitives

```text
ADD     q_addr, q_addr, g-e
AND     q_addr, q_addr, B-1
LOAD256 q_word, q_addr
```

instead of the previous five primitives `ADD; AND; AND-map; ADD-base; LOAD256`.
The table begins at relative memory word zero, so the mask performs the physical
wrap and no base addition follows. Every `g-e` is positive; the minimum is 11.
Within-head queries may reach the four copied guards. The mask before the next
head returns to the main table. Existing marker handlers preserve `q_addr`
because an early match must already return to later queries in the same head.
Nineteen later heads save exactly `19*2=38` operations for every scan word.

A separate full-domain checker enumerated all `2^23` base buckets for ordinary
and straddle paths and all twenty heads. Its two independent runs reported

```text
head starts                 335,544,320
chained transitions         318,767,104
physical query addresses    754,974,720
represented buckets       1,006,632,960
guard addresses                       140
mismatches                              0
```

The checker source SHA-256 is
`c7b1dcdb6ffa55eb071f123ecf580d57abe291c6134bf812c6edf5c0079e6d0d`;
the one-thread and 14-thread result hashes are respectively
`0171b989f0da6821e6207be62eeb458fa575abb9fcd78997ab80ca9a1758b056`
and `566e690dbe412ef38b037939cc5dc0a993e15d1a07dddded5cf8bdc99994e78b`.
Again these records support the stated algebra; they are not treated as trusted
organizer output.

The resulting complete-u rows are

| path | class 0 | class 1 | class 2 | class 3 |
|---|---:|---:|---:|---:|
| ordinary | 267 | 267 | 527 | 527 |
| straddle | 547 | 847 | 1,127 | 827 |

For example a row is `24 + 20*head_cost + 3`: 24 common-prefix operations,
twenty head bodies linked by the physical-address recurrence, and three loop-
tail operations. Combining these rows with the exact census gives

```text
fixed = (507/512)*397 + (5/512)*837 = 401.296875 operations/u.
```

### A.18.4 Unchanged body charges and u32 semantics

The explicit reductions from remediation v3 remain binding. Every intended
32-bit arithmetic result is reduced with `AND MASK32` before it reaches a SHA
sigma, nonlinear Boolean function, shift, address, table target or comparison.
Only uninterrupted ADD/SUB chains may delay the reduction to their next such
boundary. The inherited typed verifier still reports zero CFG, use-before-
definition, semantic and u32-reduction mismatches across 164,160 target-width
cases. It also binds these unchanged body charges:

```text
match/payload handler                 28
post-filter C1                        10
post-filter C2                        25
post-filter G                         33
post-filter F7                        33
Step-3b                            3,178
continuation wrapper                  20
```

Step-3b is emitted once. A successful four-filter path sets a continuation
token, enters that shared body and returns through the explicit dispatcher. The
20 wrapper operations are charged only under `q_pf`; no call, return, mask or
branch is free. The source continues to check the actual P8 body at 3,178
operations and the C1 body at 10.

### A.18.5 Binding mean, maximum and success cap

All probability inputs are unchanged:

```text
retained mean per bucket r = 6.33626861212226023369028436855...
claws/u = 160*2^23*r/2^32
         = 1.98008394128820632302821386517...
P(C1)       = 1/8
P(C1,C2)    = 53,096,854 / 2^32
P(C1,C2,G)  = 57,726,359,870,197 / 2^58
q_pf        = P(C1,C2,G) * 287,309,824 / 2^32
PF          = 10 + 25*P(C1) + 33*P(C1,C2) + 33*P(C1,C2,G)
```

Thus

```text
per_u = 401.296875 + claws/u * (28 + PF + q_pf*(3178+20))
      = 483.63355606688710990103843907249...

wbar = 2728 + 139 + 2^23*5 + 2^21*512 + 2^26*80 + 16
       + 2^32*per_u
     = 2,083,674,703,422.46252554891789225...
```

The deterministic maximum uses the worst fixed row 1,127 and all
`20*4*7=560` possible markers:

```text
umax = 1127 + 560*(28+10+25+33+33+3178+20)
     = 1,864,247
vmax = 2728 + 139 + 2^23*5 + 2^21*512 + 2^26*2200 + 16
       + 2^32*umax
     = 8,007,028,651,854,659.
```

The H2 bound remains `q3_P >= 2^-96.2791`; the per-retained-good-pair value is
`q0=q3_P*2^32/160`. The H3 factor remains `1-2^-8.5`. The count-cap and bounded-
draw abort probabilities, the separate `2^-60` exception reserve and all
preprocessing charges are unchanged. The smallest integer meeting the same
success inequality is still

```text
N_CV = 15,580,353,037,155,665.
```

At `epsilon=2^-16`, the upward total-work cap is

```text
Vcap = ceil((1+epsilon)*N_CV*wbar)
     = 32,464,882,861,153,406,401,930,466,258,
```

and the final Bernstein negative-log2 exponent is
`680.9548289437285...`. Substitution in A.15's fail-closed success inequality
gives `0.3900000000000000018394...`, above 0.39. This remains conditional on
H1, the measured H2 transfer and the two explicitly stated H3 premises.

### A.18.6 Total computation and rounded score

Charge the characteristic search, Step-1 solve and all development in full,
then the online work cap, one-CV overshoot and final verification:

```text
N = (2^78+2^74+2^70)*2728
    + 32,464,882,861,153,406,401,930,466,258
    + 8,007,028,651,854,659
    + (6*2728+1600)
  = 33,344,121,387,140,981,194,339,542,341 operations.

time_log2 = log2(N/2728)
          = 83.33779116259960324600857204724...
claim.time_log2 = 83.33780                 (rounded upward).
```

The preprocessing claim remains `78.09276`. From the separately rounded
resource claims,

```text
83.33780 + max(0,28.094-20) = 91.43180.
```

### A.18.7 Static code, advice and online memory

Sharing only the rare Step-3b body leaves 360 conservative handler sites. The
prior transpose bound had 168,560 operation records. Eight class/path arms each
remove two address records at nineteen later-head sites, hence

```text
removed records       = 8*19*2 = 304
operation records     = 168,560-304 = 168,256
code upper bound      = 1,048,576 + 24*168,256
                      = 5,086,720 bytes.
```

This is below the 11,534,336-byte executable reserve. Allowing a separate u32
adjusted-gap immediate at every removed site gives an advice upper bound
`50,000+8*19*4=50,608` bytes, below the 65,536-byte reserve.

The exact aligned memory map is

| item | bytes |
|---|---:|
| main table plus four guards | 268,435,584 |
| QREP plus rejection table | 32,768 |
| padding to executable start | 3,968 |
| executable reserve | 11,534,336 |
| bounded single-thread stack | 1,048,576 |
| advice/metadata/constants | 65,536 |
| traces/messages/counters/registers | 65,536 |
| allocator/runtime reserve | 4,194,304 |
| output/alignment/scratch | 917,504 |
| **online cap** | **286,298,112** |

The executable starts at byte 268,472,320. The whole-computation peak remains
the disclosed Step-1 measurement, `279,720 KB = 286,433,280 bytes`, leaving
135,168 bytes of headroom. Its base-two logarithm is
`28.0936238847...`, rounded upward to `memory_log2_bytes=28.094`. The degree
scan described in A.17 remains below this same peak; no evidence-only memory
exclusion is introduced.

### A.18.8 Final experiment archive and limitations

The only declared participant source is `experiments/all_evidence_v4.py`, 65,111
bytes, SHA-256
`af4cecb84dc47aa430b7498e4b12d55597699bafb88603aa9cdb7bf1952ab31c`.
It verifies each embedded Python module hash before execution. The unchanged
module hashes are

```text
p1claw  f8ae3bf1f295ab117b17c5daa773657344c9c2d968a126b6da5b69366dfa3853
p1q3    9b243adfd8180dc62609b559f3c72b50171ff5574031a944679f1e0bd39de078
program  f9a3932e875789528264d5cea70e3c64ad6185f51875821cd09d79ee23599d78
verify   dbf5f1fbdc61bfab69079ae8996cdd38ab1c031f4c8b3d1dc83982331ed9bfc5
```

The transfer module adds the block-4 checker and has hash
`a461a9e12098cd9b2bbec6029af28fe90011fccf49b197febfe7fd9d115f528c`.
Comment-only and blank transfer lines are removed in transport; its executable
Python tokens and all earlier checks are unchanged. For the two bounded joint-law diagnostics only, the dispatcher sets four replicates, fresh 256-pair pools and the matching df=3 coefficient 4.5407 so every execution stays below the organizer timeout; the binding 288-replicate frozen study and its claimed allowance are unchanged and are not recomputed by these diagnostics. The C degree-scanner text is
no longer carried inside the executable archive, because it is not imported by
the Python runner; A.16.6 and A.17 continue to reproduce and bind it. This keeps
the executable source within the organizer's aggregate 65,536-byte limit.

In a pinned, networkless, one-CPU organizer container, the final lowering entry
returns exactly 256 rows and is byte-identical on replay. Its bounded numeric
observations include zero inherited CFG, semantic and u32 mismatches; zero new
block-4 mismatches; 1,572,864 exact representative tag/role checks; 112 payload
round trips; 57,344 structured packed entries; fixed work 401.296875; Step-3b
3,178; online cap 286,298,112; and code bound 5,086,720. The general marker and
address identities are proved above. The separate full-domain C runs add
coverage but remain participant evidence.

The final construction still has no physical execution of all `N_CV` chaining
values or all `2^32` scan words inside one attack run. Public-seed experiments
do not establish an iid collision probability. H1, H1-P1, the H2 law transfer
and both H3 premises remain score-critical heuristics with the limitations in
`claim.json`. `submission_state: ready` asks for exploratory review; it does not
assert mathematical proof, qualification, human acceptance or promotion.
