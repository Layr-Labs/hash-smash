# SHA-256 reduced to 38 steps: ordinary collision by the P1 row-16 claw of the P8 characteristic, found by a distinguished-point walk in 2^20 bytes

**Target:** `sha256-r38-prefix-v1` (SHA-256 steps 0..37 on every padded block, standard IV, FIPS 180-4 padding, feed-forward, all eight digest words), lane `exploratory`.
**Claim:** `time_log2 = 89.3032` target-compressions (exact 89.30319, rounded up), `memory_log2_bytes = 20.0691` (a declared upper bound of 1,100,000 bytes: the enumerated worst case over the program's control flow, Section 6, is 1,045,840 bytes, and the remaining 54,160 bytes are a declared margin), success probability at least 0.39, `preprocessing_log2 = 78.09276` (the allowances of Section 9, charged inside the time), advice 260 bytes (`nonuniform_advice_log2_bytes = 8.03`).
**Scalar:** `hashsmash-scalar-tm-v1`: `89.3032 + max(0, 20.0691 - 20) = 89.3723` (memory penalty 0.0691 bit; the declared memory bound is above one MiB by its margin).

This entry takes the second-block construction, the row-16 claw and the downstream probabilities of newjordan's `51613d1c` (the P1 sum-claw on dariolina's P8 characteristic `1a695f0b`, Section 2) and finds the claws with the memory-bounded walk program of the r39 lineage (our `19034ce3`, lamb356 `4487063`, Jbenisek `d90878ff`, dkuthoore `0b2616e3`) instead of a 2^28-byte table. Everything the bound uses is defined, derived or counted in this file and in `experiments/r38joint.py` (own code, standard library; P8 is read from the public proof of `1a695f0b` as data, as `51613d1c` does; no code of another participant is executed).

## 1. Target and output

The program outputs two distinct 128-byte messages `m = M0 || M1` and `m' = M0 || M1'` with a common first block `M0`. FIPS padding appends the same third block to both.

**Lemma 1.** Let `cv = F_38(IV, M0)`. If the second-block compressions of `M1` and `M1'` from `cv` end with equal state words `A34..A37, E34..E37`, the digests of `m` and `m'` are equal. *Proof.* The second block's output is `cv + (A37, A36, A35, A34, E37, E36, E35, E34)` for both, and the third block is identical. The program compares the eight output words of the two second-block compressions exactly (`step3b`) and then recomputes both complete 3-block digests (`digest_r38`) before it outputs anything, so every output is a collision of the target; `M1 != M1'` because the two members differ in `W7` (`D7 = 0x20000000`).

## 2. The construction (credited prior work)

**P8 and the P1 pair (`1a695f0b`, `51613d1c` Section 2).** P8 is a 38-step semi-free-start characteristic with the published pair `(PCV, PMX, PMY)` (data in `experiments/r38joint.py` [1]). Member x of the P1 pair takes `A0 = a0`, `A1 = a1` free and `A2..A15`, `E6..E15` from the published trace of `PMX`; member y the same with the trace of `PMY`. For a chaining value `cv`, `E0..E5` and `W0..W15` of each member follow from the step equations (`variantW`); `W10..W15` are the published words and `W0..W9` depend on `(cv, a0, a1)`. Setting `cv = PCV`, `a0 = A0`, `a1 = A1` of the published pair returns `PMX` and `PMY` exactly (asserted at import).

**Row 16 is a claw (`51613d1c` Section 2).** With `u := W1 = a1 + h(a0, cv)`, the row-16 word of member x is
`E16x = F(a0) + P(u)`, `P(u) = s0(u) - u`, `F(a0) = a0 - S0(a0) - MAJ(a0, a, b) - S1(E0) - CH(E0, e, f) + KF`, `E0 = a0 + E0base`,
with `(a, b, e, f) = (cv[0], cv[1], cv[4], cv[5])`, `E0base = cv[3] - S0(a) - MAJ(a, b, cv[2])`, `KF = k0 + Cc2 - cv[6] - K[1]`, `k0 = -S0(a) - MAJ(a,b,cv[2]) - cv[7] - S1(e) - CH(e,f,cv[6]) - K[0]`, `Cc2 = 0x7af32e15`. These are the step-0 and step-1 equations written out; `selftest` and experiment `r38-p8-claw` (trials 1..255) check `F(a0) + P(u) = E16x` against the real step-0..16 trace of the P1 pair on random `(cv, a0, u)`.
The row-16 pass set of P8 is `S160 = { H_j + o : j < 20, o in OFFS }` with the 20 heads `R16H` (`H_j = H_0 + t_j 2^13`, bits 0, 2, 10 of every head zero) and `OFFS = {0, 1, 4, 5, 1024, 1025, 1028, 1029}` (bits 0, 2, 10 of the sum free). A **claw** is a pair `(a0, u)` with `E16x in S160`; equivalently, for the head `H_j`,
`(F(a0) - t_j 2^13) - (H_0 - P(u)) in OFFS`   (the program's `claw_core` test).

**What a claw still has to pay (`51613d1c` Sections 6, 7, 9).** A claw is a *good pair* when the four post-filters hold on the real words of the two members: `C1: W8y - W8x = D8`, `C2: s0(W9y) - s0(W9x) = D9s`, `G: s0(W8y) - s0(W8x) = T8`, `F7: W7y - W7x = D7 and s0(W7y) - s0(W7x) = F7d` (the five constants are the published pair's differences, recomputed at import). `51613d1c` counts them exactly: `q_pf = P(C1 C2 G F7 | claw) = 57,726,359,870,197 x 287,309,824 / 2^90 = 2^-16.1877` for `a0` uniform in the window `R = 9` (`a0 in [9 x 2^26, 10 x 2^26)`) and `a1` uniform. A good pair is accepted (its two second blocks collide) with probability `q3r = q3_P1 x 2^32 / 160 = 2^-71.4010`, where `q3_P1 = 2^-96.0791 = 2^-96.0133 x 2^-0.0658` is the registered accepted-event rate of the P1 family on window `R = 9` (the A0-variant base over 128 + 400 seeds and the paired P1-minus-A0 difference, one-sided 99% lower bound `D_LB = -0.0658` over 36 seeds; `51613d1c` Section 9 and Appendices P, Q). Together one claw yields a collision with probability `q_pf x q3r = 2^-87.5887` at the exact rates. Section 5 reports the rates measured on this program's claws and Section 7 states the charged `p_claw = 2^-87.593798` (charged `q_pf = 2^-16.192770`); Section 9 states exactly how these numbers are inherited.

## 3. The walk and the program

**Points.** A point is a 29-bit word `v`. Let `r(y)` be the 32-bit word `y` with bits 0, 2 and 10 removed (29 bits). The walk step is
- side `s = bit 28 of v`. **A side** (`s = 0`): head index `j = bits 26..27` (one of the window's four heads `heads4`, Section 3 below), `a0 = (9 << 26) | bits 0..25` (window `R = 9`), image `y = F(a0) - t_{heads4[j]} 2^13`;
- **B side** (`s = 1`): `u = v' | mix4(v') << 28` with `v' = bits 0..27` and `mix4 = (v' >> 3) xor (v' >> 11) xor (v' >> 19) xor (v' >> 24) mod 16`, image `y = H_0 - P(u)`;
- next point `v_next = r(y)`; `v_next` is a distinguished point (DP) iff its low 6 bits are zero.

**Lemma 2 (what a cross-side collision is).** Let `x` be an A point and `y` a B point with `r(y_A) = r(y_B)`. Then `y_A xor y_B` lies in the span of `{1, 4, 1024}`, so `d = y_A - y_B = sum_k 2^k (a_k - b_k)` over `k in {0, 2, 10}` with `a_k, b_k` the free bits of the two images, and `(a0, u)` is a claw with head `heads4[j]` iff `d in OFFS` iff `a_k >= b_k` for all three `k`. The program tests `d` exactly on every cross-side collision (`claw_core`: `d & ~0x405 == 0`); the collisions that fail it (`notclaw`) are discarded. Under uniform free bits the pass probability is `(3/4)^3 = 27/64 = 0.4219` (measured 0.4214 over the 24 windows). No equality test on a quotient of the word does better than 3/4 per free bit, and the 29-bit quotient is the best choice among quotienting 0..3 of the free bits (DESIGN record; it is a design choice, not a premise: the program tests `d` exactly).

**Heads.** The 20 heads are partitioned into five subsets of four, `SUBSETS[s] = {4s, .., 4s+3}`. The attack (`--attack`) cycles the subsets, window `w` using `(start + w) mod 5` with `start` drawn once from the system's random source, so over any five consecutive windows every head is used once; with the per-subset claw yields equal (Section 5: the five subset means of distinct groups per window agree within 0.2%), the attack-wide mixture of the claws over the 160 row-16 passes is uniform, which is the mixture the inherited rates are pooled over. The measured windows use the same rule with `start = B mod 5` of their seed base `B` (`--windows`), so the 24 evaluation windows and the 48 G windows sample all five subsets (Section 5 reports the yield per subset and charges the subset-stratified bound). The A side of the point space (2^28 points) is then `(a0 in R = 9) x (4 heads)`, balanced against the 2^28 B points (cross-side share of collisions measured 0.5003).

**Why a0 stays in window R = 9.** `q_pf` is an exact count for `R = 9` and `q3_P1` is measured on `R = 9` (`51613d1c` refused to widen the window until it had measured the transfer, its A.23-A.28). The head bits enlarge the A side instead.

**The program (`experiments/r38joint.py`, sections [3]-[4]).** Per first block `M0` the program runs one WINDOW of `2^25` walk evaluations (`Attack.run_window`):
1. Two random 256-bit words give `M0` (16 words, 18 operations); one target compression gives `cv`; the constants of `F` (140) and of the post-filter chain (260).
2. The generator (`build_kernel`, `allocate`, `to_source`, section [2]) emits the two kernel images (bank A to bank B and B to A) of the 256-lane step: one record = XOR, AND, OR or NOT of 256-bit registers (bit `j` of the 256 points lives in plane `j`; rotations are renaming; constants of `cv` and of the four heads are folded; MAJ and CH with constant operands reduce to wires; a `MUX` selects the A or B image per lane; the DP plane is the OR of the six low output planes). The images have 1195 to 1270 records over the 24 windows and the organizer's PCV image (cap `KCAP = 1300`) and use at most 159 registers (cap 240; 64 fixed: two banks of 32 planes, the DP plane at 64). The generator is charged **at the cap `GCAP = 2^21 = 2,097,152` operations per window**, in `m.o` (Section 4). Verification: `r38-p8-claw` trial 0 (organizer sandbox) and `selftest` execute both images on 256 random lanes against the scalar step (0 mismatches, DP plane included); check mode asserts every claw found by the walk against the scalar maps.
3. The table is cleared (4 operations per word): `WORDS = 27,648` words of 32 bytes, six entries of 40 bits each; 256 trails start in the 256 lanes, trail `i` at point `i`.
4. Stage 1 (`Attack.iter1`): `2^17` iterations of the kernel; on a DP (`Attack.hit`): the lane is found (binary search), the 23 high bits `r` of the point are extracted (Horner over the planes), the word is `r x 27,648 >> 23` (four shifts and three adds), the check field is `chk = r mod 512` (the `r` values of one word form an interval of at most 304 values, so `(word, chk)` determines `r`: no false match). The six entries of the word are scanned: an entry with the same `chk` and a nonzero length is a MATCH (two trails ended at this DP): the pair `(id, len)` of both trails goes to a queue of 4096 pairs, and the stored entry is replaced only if the new trail is longer (keep-longer, dkuthoore `0b2616e3`); otherwise the DP is written to an empty entry of the word, or, if the word is full, to the entry selected by a rotating counter. The lane receives a new trail (next id, `insert_lane`). A trail older than 1280 iterations is cut by a scan every 512 iterations.
5. Stage 2 (`Attack.stage2`) when the queue holds 3840 pairs and at the end of the window: pairs run in lane pairs `(p, p + 128)`, 128 slots, continuous refill; the longer trail starts first and the shorter `len` difference iterations later (timing wheel of 2048 buckets); after each iteration the two states are compared (12 planes, then the other 17 for candidates); the first equal state gives the predecessors `(x, y)`; `x = y` (the shorter trail started on the longer one) is discarded (`degenerate`).
6. The claw (`Attack.claw`, `claw_core`, every operation counted): sides from bit 28 (same side: discarded, `same`); decode `(a0, j)` and `u`; `F(a0)`, `P(u)`, the exact test of Lemma 2 (`notclaw` on failure); `a1 = u - F + a0 + K2` (the claw equation); `C1` on `W8x, W8y`; `C2` on `W9`; `G`; `F7` (the words from the closed forms of the step equations, asserted against `variantW` in check mode); step 3b: both second blocks `W0..W15` from `(cv, a0, a1)`, two 38-step compressions (2 x 2728 charged), exact comparison of the eight words. On acceptance the two 3-block digests are recomputed (6 x 2728 + 1600 charged) and the messages are output.

The attack is the loop over first blocks (`--attack`): the 16 words of each window's first block are drawn from the operating system's random source (fresh algorithmic coins; `--seed` exists only for the measurements and experiments). Halts: a success, the window count `B_WINDOWS`, the charged-work budget `W_BUDGET` (Section 7), and a window ends when its trail counter `idc` reaches `2^20` (it peaks at 527,784 over the 24 windows).

## 4. Machine model and prices (declared once)

Counted 256-bit word RAM with 256 registers (8,192 bytes, counted), cost model `collision-frontier-v5`, unit the target compression = 2728 operations (`C` of `sha256-r38`). One operation each: XOR, AND, OR, NOT, move, shift, rotate, add, subtract, compare-and-set; a conditional branch is a compare and a branch (2); a load or a store is 3 (index shift, base add, access); a call and its return are 2. A kernel record (register-to-register XOR/AND/OR/NOT of 256-bit words) is one operation and is stored in 5 bytes (opcode and three 10-bit register fields; the price of `6b678689`, `0c1ef7c3`, `19034ce3`, `0b2616e3`). Every word operation of the program passes through the class `Mach` (one method = one charged primitive; `m.o` counts them); the kernel is charged `len(records)` per iteration; the program's own control flow that is not a `Mach` call (the six-entry scan loop and its flag tests, the keep-longer chain, the per-iteration cut-scan and halt tests, the initialisation of a stage-2 phase) is charged by explicit allowances in `m.o`: `CF_HIT = 16` per DP hit (an instrumented count found 14.3-15.7 decisions), `CF_ITER = 4` per iteration, `CF_PHASE = 1024` per stage-2 phase; the generator is charged the cap `GCAP = 2^21` per window (its own builder-call census, 2,880 calls at most over the 24 windows, each a handful of Python operations, is far below the cap; the cap is the charge). Memory is the inventory of Section 6, with the code charged as the full byte length of the shipped program. These are prices of the cost model, not probabilistic premises.

## 5. The exact ledger (24 pre-declared windows)

The cost of a window is `m.o` after the window; the program prints it (`--windows N --seed S --check --out f.json`). **The 24 evaluation windows were pre-declared** (three run sets of 8 windows, one per process) (seeds `B x 1000 + w`, `B in {20261024, 20261025, 20261026}`, `w = 0..7`; adoption rule: every window kept, none excluded; the declaration file names the program hash before the first run and is reproduced in Appendix B) and run in check mode (every claw asserted against the scalar maps, the real `E16x`, and the real words `W7, W8, W9` of both members; 0 failures; check mode adds no counted operation). Tuning before the declaration: 2 windows (seed 901) in each table policy, the selftests, and the four organizer-seed windows of `r38-window-small`.

Per window (Appendix A lists all 24): mean `637,106,459.3` operations (standard deviation `5,229,916`, largest `648,611,830`), mean `36,397.58` distinct claws (sd `192.6`), mean `36,278.38` distinct claw groups (sd `190.5`; two claws are in one group when they share `a0` or `u`), groups/claws `0.996725`. Per distinct claw: **`17,504.1` operations = 2^14.0954 = 6.416 compressions**.

| category (`Mach.cat`) | share of operations |
| --- | ---: |
| stage-1 walk (kernel records + DP plane test + loop) | 23.4% |
| stage-1 DP handlers (find lane, extract, table, queue, new trail) | 24.6% |
| stage 2 (kernel, launches, wheel, compares, merges, extraction) | 49.5% |
| claw decode, exact test, post-filters, step 3b | 1.8% |
| window setup (first block, constants, table clear, lanes) | 0.3% |
| generator (charged cap) | 0.3% |
| cut scan, run setup | 0.1% |

Events per window (means): hits 524257.4, matches 231892.6, pairs 231892.6, merges 231892.6, degenerate 9123.4, same 111307.6, cross 111461.6, claws 46965.9, notclaw 64495.7, c1 5862.6, c2 583.0, g 8.9, f7 0.5, step3b 0.5, trails 524257.4, cuts 3.8, slotfull 131062.7, s2iters 161574.3. The quotient's false positives (`notclaw`) are 0.579 of the cross-side collisions (Lemma 2: 1 - 27/64 = 0.578 expected); same-side collisions are discarded; re-discovered claws (raw minus distinct) are 0.225 of the raw claws and are not counted. Post-filter stage counts over the 24 windows: C1 140,703 of 1,127,181 raw claws (0.1248; 1/8 = 0.125 under H1-P1 of `51613d1c`), C2 13,993 of the C1 passes (0.0995; exact 53,096,854 / 2^29 = 0.0989), G 214 of the C2 passes (0.0153; exact 2^-5.948 = 0.0162), F7 11 of the G passes (exact 0.0669), step 3b 11, accepted 0 (expected `3.73e-21` over the 24 windows).

The G filter is CHARGED at the measured rate. Over the 72 windows (24 evaluation + 48 declared G-measurement windows), RAW counts (every claw event, rediscoveries included): G 755 of 41,929 C2 passes = 0.018007 against the exact G | C1 C2 = 57,726,359,870,197 / (53,096,854 x 2^26) = 0.0162004 of 51613d1c (z = 2.93); DISTINCT claws (each (a0, u) once per window, the furthest stage it reached): G 575 of 32,352 distinct C2 passes = 0.017773. One-sided 99% Wilson lower bounds (z = 2.326348): on the distinct counts 0.0161433 (plain n = 32,352); on the raw rate with n_eff = 32,491 (= 41,929 raw C2 passes x (1 - 0.22510), the rediscovery share of raw claws over the same windows) 0.0163690. The lower of the two, 0.0161433 (distinct-claw), replaces the exact rate in q_pf = P(C1 C2) x G x P(F7) = (53,096,854 / 2^32) x 0.0161433 x (287,309,824 / 2^32): the charged q_pf is 2^-16.192770 instead of the exact 2^-16.187672 (+0.0051 bit); p_claw = q_pf x q3r = 2^-87.593798. Per run set: seeds 20261024000..20261024007: raw C1 47185, C2 4710, G 65, F7 2; distinct C2 3630, G 53; seeds 20261025000..20261025007: raw C1 46629, C2 4629, G 82, F7 4; distinct C2 3529, G 63; seeds 20261026000..20261026007: raw C1 46889, C2 4654, G 67, F7 5; distinct C2 3560, G 53; seeds 20261027000..20261027015: raw C1 93780, C2 9215, G 192, F7 9; distinct C2 7144, G 146; seeds 20261028000..20261028015: raw C1 94200, C2 9286, G 170, F7 6; distinct C2 7230, G 126; seeds 20261029000..20261029015: raw C1 94599, C2 9435, G 179, F7 12; distinct C2 7259, G 134. **By head subset** (the 72 windows rotate through the five subsets, Section 3): subset 0 (heads 0-3): 14 windows, raw C2 8017, G 143 (0.0178); distinct C2 6192, G 100 (0.0161); subset 1 (heads 4-7): 15 windows, raw C2 8485, G 130 (0.0153); distinct C2 6573, G 98 (0.0149); subset 2 (heads 8-11): 15 windows, raw C2 8913, G 143 (0.0160); distinct C2 6834, G 120 (0.0176); subset 3 (heads 12-15): 14 windows, raw C2 8242, G 199 (0.0241); distinct C2 6374, G 147 (0.0231); subset 4 (heads 16-19): 14 windows, raw C2 8272, G 140 (0.0169); distinct C2 6379, G 110 (0.0172). The G rate of the walk's claws depends on the head subset (chi-square 14.4 on 4 df over the five subsets). The earlier filings measured head subset 0 in EVERY window (their `--windows` mode built each window as a fresh `Attack` whose first window takes subset 0) and found 0.0146 on distinct claws over 72 subset-0 windows, against 0.0161 on the 14 subset-0 windows here (consistent); the attack cycles all five subsets uniformly, and the pooled rate over the near-balanced 72 windows is the estimator of the attack-wide rate; the bound charged is the pooled one.

**F7.** Over the same 72 windows the F7 filter passed 38 of 755 raw G passes (0.0503; distinct claws 28 of 575) against the exact |F7| / 2^32 = 0.066895 (binomial z = -1.82, one-sided p about 0.034). F7 is charged at the exact rate. Unlike G, the F7 rate cannot depend on the law of (a0, a1) ALONE: W7y - W7x = D7 holds identically (checked on every claw in check mode), and W7x = c7(cv) - E3 - CH(E6, E5, E4) carries the chaining value word cv[0] additively (through E3 = A3 + cv[0] - S0(A2) - MAJ(A2, a1, a0)), so for ANY fixed (a0, a1) the word W7x is uniform over the first block's chaining values and the test s0(W7x + D7) - s0(W7x) = F7d passes with probability exactly |F7| / 2^32 averaged over cv (51613d1c Section 6 states the same). The residual premise is that cv[0] is not correlated with the event that (a0, a1) is a claw the walk found for this cv in a way that moves the F7 rate (cv[0] enters F and h non-linearly): a heuristic, not detected at the 99% level here, with the sensitivity below. The 72 windows are 72 chaining values, and the per-cv F7 rate is strongly overdispersed (51613d1c Appendix H: chi-square 564 on 23 df), so the binomial z overstates the evidence of a deficit (the overdispersion figure is cited from the public proof of 51613d1c, not re-measured here). A development check of the identity (not organizer-executed): 40 fixed (a0, a1) pairs x 5,000 random chaining values, F7 rate 0.06722, D7 on every draw. Sensitivity: charging the one-sided 99% Wilson lower bound 0.0348 instead would add 0.942 bit (time_log2 about 90.25).

The claim does not use the means as they stand. For each quantity it uses the most conservative of (i) the one-sided 99.9% Student-t bound over the 24 windows (23 degrees of freedom, 3.485 standard errors) and (ii) each of the three 8-window run sets' own one-sided 99% bounds (7 degrees of freedom, 2.998 standard errors): at most `mu+ = 645,297,157` operations per window, at least `c- = 36,127.96` distinct claws and `g- = 35,770.49` distinct groups per window, and a group-to-claw ratio of at least `r- = 0.996276` (`c- r- = 35,993.43`). Pooled 99.9% bounds: mu+ 640,826,879, g- 36,142.8, c- 36,260.6, r- 0.996491. Per-set 99% bounds: set 1 (seeds 20261024000..20261024007): mu+ 641,962,740, g- 36,221.6; set 2 (seeds 20261025000..20261025007): mu+ 640,910,650, g- 36,018.9; set 3 (seeds 20261026000..20261026007): mu+ 645,297,157, g- 36,057.9. **Head subsets (F-HEAD-YIELD of the 15b22a77 review):** the measured windows rotate through the five 4-head subsets from a seed-derived start, as the attack does; per subset: subset 0 (heads 0-3): 5 windows, mean groups 36268.6, one-sided 99% t lower bound 36045.0; subset 1 (heads 4-7): 6 windows, mean groups 36291.0, one-sided 99% t lower bound 36041.8; subset 2 (heads 8-11): 5 windows, mean groups 36304.6, one-sided 99% t lower bound 35770.5; subset 3 (heads 12-15): 4 windows, mean groups 36276.8, one-sided 99% t lower bound 35925.5; subset 4 (heads 16-19): 4 windows, mean groups 36240.5, one-sided 99% t lower bound 35804.8; balanced-cycle mean of the subset means 36276.3. The groups bound charged is `g- = 35,770.49` = min(pooled/per-set bound 36,018.9, smallest subset bound 35770.5). (The plain 99% pooled bounds, 2.500 standard errors, give time_log2 89.2743.) The declaration named one-sided 99% Student-t bounds; the bounds used are never less conservative than those (Appendix B, statistic note).

**Every window has a worst-case cost (R).** Every loop is bounded by a constant of the program: at most `2^17` stage-1 iterations (the window also ends when the trail ids reach `2^20`), each at most `KCAP + 11` kernel-and-loop operations plus at most 256 DP handlers (straight-line apart from the 23-plane extraction, the six-entry scan and the 20-plane insert; under 1,000 operations each including `CF_HIT`) and the cut scan (under 20,000): under `2^36`. At most `2^25` DP hits per window (one per lane per iteration), so at most `2^25` queued pairs and at most `2^25 / 3840 + 2^17 / 512 + 1 < 2^14` stage-2 phases; a phase runs at most `S2CAP = 2^17` iterations (hard cap; a pair needs at most `MAXS + CUTP = 1,792`, and `3840 / 128 x 1,792 = 53,760 < 2^17`, so the cap never fires in a correct run), each at most `KCAP + 3 + CF + 128 x (launches + merge + extraction + claw filters + step 3b with its two compressions, under 8,000) + 17,968` (the final-digest check of the first accepted pair, after which the phase ends) `< 2^20.1` operations. Hence the charged work of a window is at most `2^36 + 2^14 x 2^17 x 2^20.1 = 2^51.1 < R = 2^53` operations (the 15b22a77 text misstated its sum `2^14 x 2^17 x 2^21.7 = 2^52.7` as `< 2^52.1`); its distinct claws and groups are at most `2^25`.

## 6. Memory, by allocation inventory

**Rule: the peak is bounded over the program's CONTROL FLOW, not over its expected behaviour: every allocation of the attack path (`Attack.__init__`, `window_setup`, `stage2`, `step3b`) is charged at its ALLOCATED size, every container that can grow has a cap enforced in code (a halt before the cap is exceeded) or is bounded by an existing allocation, and the one output pair is charged**; the code is charged as the complete byte length of the shipped program; the kernel images at their cap. The predecessor `15b22a77` was refuted because stage 2 did not stop at the first accepted pair and could have retained up to 4,095 pairs; this program stops every loop at `s.success` and holds a single retained pair (`s.message`). The table is derived from the shipped source (allocation sites named; `tools/mem_inventory.py` of the development record asserts the allocation lines and computes it):

| allocation (source) | bytes |
| --- | ---: |
| register file `s.R=[0]*512` (Attack.__init__): 512 words x 32 B, ALLOCATED (the kernel uses at most 240; charged as allocated) | 16384 |
| lane array `s.LA=[0]*256`: 256 words x 32 B | 8192 |
| stage-1 save area `s.sav=[0]*32`: 32 words | 1024 |
| table `s.tab=[0]*P.WORDS`: 27648 words x 32 B (6 entries of 40 bits per word) | 884736 |
| queue `s.qw=[0]*(P.QCAP//4+1)`: 1025 words x 32 B | 32800 |
| stage-2 free-slot stack `free`: up to 128 entries, charged 128 words | 4096 |
| stage-2 pair maps `bid`, `nxt`: up to 128 entries each, charged 2 x 128 words | 8192 |
| stage-2 timing wheel `wh=[0]*(P.WHEEL//16)`: 128 words x 32 B | 4096 |
| two kernel images `s.ks`: KCAP 1300 records x 5 B x 2 (at the cap; the images have fewer records) | 13000 |
| program text: every byte of experiments/r38joint.py (machine code, routines, generator, P8 data, constants) | 42600 |
| per-window scalars and counters: cv 8, first block m0 16, F constants `s.co` 8, post-filter constants `s.pfc` 2 x 11, heads4 4, Mach counters `o`, `cat`, `blk`, `nest` (<= 40), `st` (<= 30), idc/it/cur/qn/rot/cv_id/success/messages (<= 12): 140 words, charged 256 words | 8192 |
| constants held by the program: K 38, IV 8, PCV/PMX/PMY 40, SAx/SAy/SEx/SEy 64, R16H 20, T20 20, OFFS 8, SUBSETS 20, D7/D8/D9s/T8/F7d 5, masks and Cc2/RTOP (<= 15): 238 32-bit words = 952 B; HIGHMASK 8 x 32 B + C_LOG8 32 B = 288 B; charged | 1536 |
| live temporaries of the deepest call chain stage2 -> claw -> claw_core -> step3b (Ws 32 words, the A/E dicts 2 x 20, the two outputs hx/hy 16, the filter words and locals; under 200 values), charged 256 words | 8192 |
| local register copies of the simulator during a kernel call (to_source locals r0..r239, at most 240 x 32 B; on the machine the records act on the register file itself; charged nevertheless) | 7680 |
| the one retained collision pair `s.message` (two 128-byte messages) with its two padded 192-byte copies and two 32-byte digests inside digest_r38: 704 B, charged | 1024 |
| module-level derived data held for the whole run: the P8 traces `_tx`, `_ty` (2 x (3 x 38 + 2 x 4) words = 976 B), `_Wx`, `_Wy` (128 B), `WIN_EXP` (4 x 14 numbers, 224 B), `EXPERIMENTS`, `B_WINDOWS`, `W_BUDGET` (31 B each), `ONES`, `M32`/`M20`/`M11`/`M9`/`M23`/`M40`/`M26`/`M28`/`M29`, the `P` class attributes (< 200 B): under 1,700 B, charged | 4096 |
| TOTAL | 1045840 |

The register file is allocated as `s.R=[0]*512` (two banks of 32 planes, the DP plane and up to 191 temporaries, 240 of which the kernel may use); the first filing of this program (eab3eea4) charged 256 words for it and was refuted for exactly that (F-MEM-512); the 512 allocated words are charged here. The code is charged as the complete byte length of `experiments/r38joint.py` (42,600 bytes): every instruction of the machine program, the routines, the generator, the P8 data and the constants are inside that text, above any 36-byte-per-instruction encoding of the executed instructions (the per-block census `Mach.blk` totals 7,213 operations over 26 blocks, for information). Growable containers and their caps (worst case over the control flow, not over expected behaviour): the kernel gate list is capped in code at GEN_MAX = 1,425 entries (G.emit halts); the queue is capped at QCAP = 4,096 pairs by the QFULL rule (a stage-2 phase runs at 3,840, at most 256 pushes per iteration) and by a hard halt in qpush; stage-2 pairs in flight are at most NSLOT = 128 (free/bid/nxt keyed by slot); at most ONE collision pair is retained (`s.message` is a single slot and every loop of stage 2, iter1 and run_window exits on s.success); Mach.cat/blk are keyed by the program's literal names (<= 40); s.st has fixed keys; the measurement containers s.distinct/s.dstage are created only when measure=True (never in --attack). Lifetimes: the attack loop (`main`, `--attack`) sets `A=None` before building the next window, so one window's allocations exist at a time; the kernel images are executed as their 5-byte records (the Python function `fn` that the simulator compiles from the records is the simulator's executor of those records, not a second copy of the program on the machine). Not at the peak: the generator scratch (gate list of at most GEN_MAX = 1,425 entries, last-use and register maps) exists in window_setup before `s.tab` is allocated (make_kernels precedes `s.tab=[0]*P.WORDS`) and is released when make_kernels returns; the measurement-only containers `s.distinct` (set) and `s.dstage` (dict) are allocated empty and never populated in --attack (measure=False): 2 words, inside the scalars allowance. Setup and the run share one peak: there is no solver, no search campaign and no preprocessing buffer. **Enumerated total 1,045,840 bytes = 2^19.99623 (2,736 bytes below 2^20). Declared bound: 1,100,000 bytes = 2^20.06907, charged as `memory_log2_bytes = 20.0691` (rounded up).** The 54,160-byte difference is a declared margin, not a measurement: it covers temporaries the enumeration may not name (interpreter frames, the boxing of integers and strings, the empty measurement-off containers, transient copies inside library calls). The declared figure is an upper bound on the peak, not the exact peak; the two predecessors of this filing were refuted for understating exact memory bounds (Section 11), and a bound is never understated here, which is why it is padded above 2^20 and pays 0.0691 bit of memory penalty rather than claiming the floor.

## 7. Success probability and time

`p_claw = q_pf x q3r = 2^-87.593798` with the charged `q_pf = 2^-16.192770` (Section 5) and `q3r = 2^-71.4010` (Section 2; Section 9 for the premises). **Claws are counted by groups.** Two claws of a window can share a trial only through a shared endpoint (`a0` or `u`); grouping the distinct claws of a window into connected components by shared endpoint (`count_groups`), one claw per group is one trial of the accepted event, and distinct groups have disjoint inputs `(a0, a1)`. Conditional on at least `G` distinct groups, the run succeeds with probability at least `1 - exp(-G p_claw)`. Set `G p_claw = lambda = -ln(0.60999) = 0.494313`, so `1 - exp(-lambda) = 0.390010` and `log2 G = 86.577294` (`p_claw = 2^-87.593798` from the charged `q_pf = 2^-16.192770` of Section 5 with the unrounded Wilson bound 0.0161433 and the exact rational `G | C1 C2`; all figures here are printed to the precision the ceiling needs). With the lower bound `g- = 35,770.49` groups per window and the margin `(1 + 2^-19)`,
`B = ceil(G (1 + 2^-19) / g-) = 3227292921399400871242 = 2^71.4508` windows (first blocks), where `g- = 35,770.49` is the lower of the pooled/per-set bound (36,018.9) and the smallest head-subset bound (35770.5; Section 5); `B` is the integer the shipped program holds (`B_WINDOWS`); it is the ceiling of the unrounded chain, and the printed 6-7-digit figures reproduce it to within 2 x 10^-6 relative (the success probability at this `B` is 0.3900099 and `log2 T` is unchanged at 4 decimals).

**Total work (Bernstein) and total groups (Hoeffding).** The windows are independent trials (fresh coins per window, H1 part (a)), each with charged work `W_j in [0, R]` and distinct groups in `[0, 2^25]`; `E[W_j] = mu <= mu+` and `E[groups] = g >= g-` is premise H1 part (b). Since `0 <= W_j <= R`, `Var(W_j) <= E[W_j^2] <= R mu <= R mu+`, and Bernstein's inequality with `t = 2^-20 B mu+` gives: the total work of `B` windows exceeds `B mu+ (1 + 2^-20)` with probability at most `exp(-t^2 / (2 (B R mu+ + R t / 3))) = exp(-2^-40 B mu+ / (2 R (1 + 2^-20/3))) = exp(-2^6.7)` (the leader's Lemma 3 form; a plain Hoeffding bound with `R = 2^46` would be vacuous at this `B`). By Hoeffding's inequality the total number of distinct groups falls below `B g- (1 - 2^-20) >= G` with probability at most `exp(-2 B (g- 2^-20)^2 / 2^50) = exp(-2^12.7)`.

**The budget.** `--attack` stops at a success, after `B_WINDOWS = B` windows, or as soon as its charged work reaches `W_BUDGET = floor(B mu+ (1 + 2^-20)) + 1 = 2082564932999596136475692503019` operations (checked before each window, 6 operations per window), whichever comes first; so its charged work is at most `W_BUDGET + R + 6 B` in every run. The time is
`T = (W_BUDGET + R + 6 B) / 2728 + 2^78.09276` target-compressions (the second term is the preprocessing allowance of Section 9, 0.0422% of the total), **`log2 T = 89.30319`, `time_log2 = 89.3032`** (rounded up; the plain means give 89.2644). By the union bound the unconditional success probability is at least `0.390010 - exp(-2^6.7) - exp(-2^12.7) > 0.39`.

Sensitivity: every bit of `log2 p_claw` moves `time_log2` one for one (Section 9 lists what each inherited number is and its registered margin); each +10% of operations per distinct claw is +0.138 bit.

## 8. Experiments (organizer sandbox)

Both declared experiments run in the organizer's Docker executor (20 s, 128 MiB); every number below is hard-asserted in the program, so a failure is an experiment error, not an observation.
- `r38-p8-claw`: trial 0 builds the kernel images for `PCV`, executes both images on 256 random lanes against the scalar step (`kernel_lanes = 512`, `kernel_bad = 0`, the DP plane included) and runs `claw_core` on the P8 pair (`a0 = A0`, the head of its `E16x`, `u = W1`): the exact claw test, C1, C2, G, F7 and step 3b all pass and the two second blocks collide (`accepted = 1`); trials 1..255: random `(cv, x, y)` of the walk's encoding: `F(a0) + P(u) = E16x` on the real trace, `W1 = u`, and `claw_iff_r16` (the program's test equals "the real `E16x` is a row-16 pass of P8 with the point's head").
- `r38-window-small`: trials 0..3 run four windows of `2^20` evaluations (4096 iterations) in check mode on the trial seeds; the frozen counts `WIN_EXP` (dp hits, matches, stage-2 iterations, merges, cross-side pairs, raw and distinct claws, groups, C1, C2, operations, kernel records, block census) are asserted for the organizer's trial seeds; every claw passes every check-mode assertion. The four organizer windows: seed 13353826..: 16437 hits, 888 matches, 185 raw / 184 distinct claws, 184 groups, C1 23, C2 3, 13544329 operations; seed 85299089..: 16343 hits, 862 matches, 178 raw / 175 distinct claws, 175 groups, C1 25, C2 0, 13535361 operations; seed 18362963..: 16203 hits, 904 matches, 185 raw / 183 distinct claws, 183 groups, C1 21, C2 2, 13466257 operations; seed 65056259..: 16335 hits, 933 matches, 198 raw / 193 distinct claws, 193 groups, C1 24, C2 4, 13618813 operations.
Both experiments were executed locally through the organizer's own executor before submission (reports in the development record); the organizer's run is the evidence.

## 9. Premises (declared in `claim.json`) and what is inherited

- **H1-walk-model** (score-critical). (a) The chaining value of a random first block is an independent random value for the maps `F` and the later events, so windows are independent trials. (b) The yield and the cost of a window are those measured on the real step function over the 24 pre-declared windows (Section 5; `mu+`, `c-`, `g-`, `r-`); the program cannot be run for `2^71.4508` windows. (c) A distinct claw group is a trial of the accepted event with probability `p_claw`, independent of the walk's yield. Support: the walk's inputs `(a0, u)` are uniform on the A-side window and on the B-side `u` set apart from the claw equation (part (d) below); the post-filter rates measured on this program's claws (Section 5) agree with the exact rates of `51613d1c` for C1 and C2, and G, measured below the exact rate, is charged at its lower bound.
- **H1-P1-postfilter-law** (score-critical, inherited from `51613d1c` Section 6 as a transfer premise). `q_pf = 2^-16.1877` is the exact count of `C1 C2 G F7` over `a0` uniform in `R = 9` and `a1` uniform over 2^32; it is taken as the rate for the claws this program finds for C1, C2 and F7, while G is charged at the lower bound measured on this program's claws (Section 5: charged `q_pf = 2^-16.192770`). Our claws have `a0 = (9 << 26) | 26 point bits` (uniform in the window by construction) and `a1 = u - h(a0, cv)` with `u` ranging over the `2^28`-element set `{v' | mix4(v') << 28}` of one chaining value; across chaining values `h(a0, cv)` is uniform, so `a1` is uniform over the attack. Disclosed: within one chaining value only `2^28` of the `2^32` values of `u` are reachable. Measured C1/C2/G/F7 stage rates over the 24 windows are in Section 5.
- **H2-P1-q3-transfer** (score-critical, inherited from `51613d1c` Section 9, its H2-P1 and H10 as a transfer premise; that the leader's `2^32 / 160` pooling is over the natural head mixture of its claws is taken from its Section 9 and not shown here: inherited, disclosed). `q3r = 2^-71.4010` is the probability that a good pair is accepted, from the registered `q3_model = 2^-96.0133` (A0-variant family; two one-sided 99% bounds, union 98%) and the paired P1-minus-A0 difference on window `R = 9`, one-sided 99% lower bound `D_LB = -0.0658` over 36 seeds (its margin against the point estimate `-0.0121` is 0.0537 bit). We did not re-measure the deep rows (the leader's tool is a C program run for 36 seeds x 2^28 samples; it is outside the organizer sandbox). **New in this program:** the row-16 pass of a claw is one of 4 heads x 8 offsets per window instead of all 160; the subsets rotate so the attack-wide mixture over the 160 passes is uniform, which is the mixture `51613d1c` measured (its q3 is pooled over S160 via `2^32 / 160`). The premise is that the accepted-event rate does not depend on which 4-head subset a window uses beyond this uniform mixture; `51613d1c` A.26 measured the only head/window dependence within reach (the `r16|all4` gate, 298 events: -0.116 +/- 0.167 between windows, consistent with zero) and declared the deeper transfer (its H10); we declare the same. Risk statement: a materially lower acceptance rate for some head subsets would raise `B` and `time_log2` one for one in `log2 q3r`.
- **H3-P1-within-cv** (supporting). Claws of one window that share no endpoint are independent trials of the accepted event (`51613d1c` H3-P1, measured there on 24 chaining values and on the forced-bit events of rows 17..21); we count one claw per endpoint-sharing group (`r-`), which removes the only dependence `51613d1c` found necessary to treat.
- **H4-allowances** (score-critical, inherited; the search and solver logs behind `A_C` and `A_S` are those quoted with their source hash in `51613d1c`'s public proof (its Appendix R.4) and are not re-supplied here: a disclosed limitation shared with the accepted leader, F-PREPROCESSING-EVIDENCE of the 15b22a77 review). `A_C = 2^78`, `A_S = 2^74` (the characteristic search behind P8 and its Step-1 solve, `51613d1c` Section 11 and its H4a/H4b with the published run logs) and `DEV = 2^70` compressions are charged in full inside `T`: `preprocessing_log2 = log2(2^78 + 2^74 + 2^70) = 78.09276`. Our own development (this program and its measurements: under 40 core-hours on a 14-core machine, under `2^50` operations) is far inside `DEV`.
- **H5-prices** (score-critical). The prices of Section 4; the 5-byte kernel record and 1 operation per record (`6b678689`, `0c1ef7c3`, `d90878ff`, `19034ce3`, `0b2616e3`); the generator charged at the cap.
- **H6-memory** (score-critical). The inventory of Section 6 is the peak; code is charged as the shipped program's full byte length.

## 10. Advice and preprocessing

Advice: the P8 chaining value and the two published blocks (40 words), the 20 heads, the five differences: 260 bytes, `log2 = 8.03`. Preprocessing: the allowances of H4 (`2^78.09276` compressions), charged inside `T`; this program has no table build, no solver and no precomputation of its own.

## 11. Disclosures and limitations

1. **The claw population is new.** The leader scans all `2^32` values of `u` and all 160 row-16 passes per chaining value; this program reaches `2^28` values of `u` per chaining value and 32 of the 160 passes per window (uniform over windows). The downstream rates `q_pf` and `q3r` are inherited as transfer premises (H1-P1, H2-P1); only the post-filter rates are re-measured here (Section 5). The deep acceptance rate was not re-measured; its registered margins are those of `51613d1c`. The G post-filter rate of this program's claws varies with the head subset by about 50% between subsets (Section 5), which shows that head-conditional rates of the later gates can differ; the claim relies on the attack cycling all five subsets uniformly so that the attack-wide rates are the uniform mixtures, and the deep rate is taken as the leader's pooled value (H2-P1 transfer premise), with the risk stated in its limitations.
2. **Re-discovered claws and the quotient.** 0.225 of the raw claws are re-discoveries of a claw already found in the window and are excluded from the count; 0.579 of the cross-side collisions are not claws (Lemma 2) and are discarded after an exact test. Both are costs the ledger pays, not events the claim uses.
3. **Stage 2 lane utilization** is about 63% (a pair occupies two lanes while the longer trail walks alone); stage 2 is 49.5% of the operations. A two-phase catch-up would lower the cost; it is not in this program.
4. **The generator is charged at a cap** (`2^21` per window, 0.3% of the work), not at an executed-operator count: this program has no WebAssembly generator; the cap is above its Python builder-call census by a factor over 728.
5. **Frozen counts.** `WIN_EXP` holds the four organizer-seed windows measured through the organizer's executor on the pinned image; the asserts fire only for those seeds.
6. **Five runs of the 24 declared seeds.** The first run used the declared program; a critic pass then found uncharged control flow (about 1.2% of the work), no stage-2 cap and no stop on trail-id saturation; the program was amended (the allowances of Section 4, `S2CAP`, the saturation stop, the masked length field) and the seeds re-run (run 2, eab3eea4); after that refutation, measurement bookkeeping and the trial-0 kernel check were added (run 3) and the lifetime release (run 4, 15b22a77): runs 1-4 produced identical claws, groups and DP hits in every window (all with head subset 0). Run 5 (this program) rotates the head subsets per window as the attack does (Section 3), so its claws differ from runs 1-4. The claim uses run 5; Appendix A lists run 4 as well. The shipped file equals the fifth-run program plus the two constants of Section 7 (Appendix B).
7. **Remaining costs.** `q3r` (2^-71.40) and `q_pf` (2^-16.19 exact, 2^-16.192770 charged) are the characteristic's; the walk's `2^14.0954` operations per claw against the table's `2^7.46` is the price of one MiB.
8. **Lineage.** This filing (r38d) is the r38c program with a padded memory declaration (Section 6: enumerated 1,045,840 bytes, declared 1,100,000); it supersedes `15b22a77` (refuted on F-MEM-RETAINED-PAIRS: stage 2 did not stop at the first accepted pair, so up to 4,095 output pairs could have been retained; now every loop exits on `s.success`, one pair is retained and charged, and every growable container has a code-enforced cap, Section 6) and `eab3eea4` (refuted on F-MEM-512: 256 register words charged where 512 are allocated). The 15b22a77 review's F-HEAD-YIELD is answered by the seed-rotated head subsets of the measured windows and the subset-stratified groups bound (Sections 3, 5, 7); its F-R-EXPONENT by the corrected sum in Section 5. Earlier changes: Changes: the allocation-based memory inventory of Section 6 (2^19.9436 -> the enumerated 2^19.99623, declared 2^20.0691 with a margin; the score pays its 0.0691-bit penalty); the G bound re-derived on distinct claws (Section 5; the judge's F-03); `r38-p8-claw` trial 0 now runs the 256-lane kernel comparison the proof had attributed to it (F-04); module-level derived data and the one-window-at-a-time lifetime of the attack loop are in the inventory; the 24 evaluation and 48 G-measurement seeds re-run on the amended program (Appendix A, B). The judge's material findings on the inherited deep rate (F-DEEP-EVIDENCE, F-01, F-EVAL-02), on independence and extrapolation (F-02, F-COST-EXTRAPOLATION, EXP-F2) and on participant-run full windows (F-EVAL-01, EXP-F1) are the disclosed limitations 1, 4 and this section's Section 9 statements: they are shared with the accepted leader and are not re-measurable in the sandbox. The measurement record of `q3_P1` is public in `51613d1c`'s proof (Appendices P and Q, with per-seed values and registrations; PR #1297 of the board).
9. **Seeds and amendments (EXP-F3).** The organizer trial seeds are reproducible from the manifest (no holdout nonce was used locally); the frozen counts were measured through the organizer's executor before the declaration. The evaluation seeds were declared before the first run and never changed; the program was amended three times after critic and judge passes (control-flow allowances and caps; measurement bookkeeping and the trial-0 kernel check; the lifetime release in the loops), each time re-running the same seeds and keeping the earlier runs in the record. The statistics are those declared (the most conservative of pooled 99.9% and per-set 99% bounds); the G rule was declared before the 48 G windows and amended once (distinct-claw accounting, more conservative) before this run.

## 12. Provenance and credit

- `51613d1c` (newjordan): the P1 sum-claw, the heads `R16H` and their mod-2^13 structure (credited there to `b561f523`/`db6b71d6`), the post-filter chain and its exact counts, the paired q3 measurement, the allowances; and its own credits: dariolina `1a695f0b` (P8), `db6b71d6`, ePrint 2026/1120 (the two-block A0-variant), `fb176310`/`9aaf71a2`.
- `0b2616e3` (dkuthoore): keep-longer, the batched handling, the r39 walk as accepted on the Pareto board; `19034ce3` (mitchuski) and `4487063` (lamb356): the program and its ledger; `d90878ff` (Jbenisek): the machine program and the whole-megabyte table; `38912d66` (sraiw) and dariolina (`21b6653a`, `2c48b18c`, `cfe5c4e2`, `4e396742`): the row-16 claw lineage; `6b678689`, `0c1ef7c3`: the 5-byte record price; geeknik `7c4da9b7`/`022fed5e`.
- The walk encoding of Section 3 (sides, head bits, the 29-bit quotient with the exact offset test), the bit-sliced kernel of the r38 claw maps and the bucketed six-entry table are this submission's own work, developed with the agentprivacy dual-agent harness.

## Appendix A. The 24 windows

Fifth run (r38c: the shipped program before its two constants were set; the claim's data; head subset per window as listed):

| window seed | head subset | distinct claws | groups | raw claws | cross | notclaw | operations | ops/claw | records | regs | gen calls | sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 20261024000 | 4 | 36301 | 36183 | 47008 | 112168 | 65160 | 639283880 | 17610.6 | 1238 | 152 | 2844 | 41 |
| 20261024001 | 0 | 36434 | 36321 | 47067 | 111295 | 64228 | 640655832 | 17584.0 | 1240 | 155 | 2842 | 40 |
| 20261024002 | 1 | 36598 | 36473 | 47092 | 111230 | 64138 | 636168117 | 17382.6 | 1224 | 145 | 2776 | 41 |
| 20261024003 | 2 | 36573 | 36444 | 47556 | 111946 | 64390 | 645112850 | 17639.0 | 1250 | 150 | 2802 | 37 |
| 20261024004 | 3 | 36587 | 36461 | 47622 | 112199 | 64577 | 630195335 | 17224.6 | 1204 | 144 | 2750 | 36 |
| 20261024005 | 4 | 36477 | 36355 | 47290 | 111308 | 64018 | 637007224 | 17463.3 | 1223 | 150 | 2828 | 36 |
| 20261024006 | 0 | 36544 | 36441 | 46878 | 111332 | 64454 | 634118552 | 17352.2 | 1220 | 149 | 2818 | 35 |
| 20261024007 | 1 | 36293 | 36158 | 46986 | 111364 | 64378 | 634356457 | 17478.8 | 1216 | 146 | 2776 | 35 |
| 20261025000 | 0 | 36286 | 36188 | 46884 | 110635 | 63751 | 638788535 | 17604.3 | 1240 | 159 | 2844 | 41 |
| 20261025001 | 1 | 36271 | 36157 | 46841 | 111710 | 64869 | 637529575 | 17576.8 | 1231 | 148 | 2778 | 40 |
| 20261025002 | 2 | 35957 | 35842 | 46192 | 110484 | 64292 | 633968613 | 17631.3 | 1224 | 148 | 2792 | 40 |
| 20261025003 | 3 | 36336 | 36234 | 46622 | 110803 | 64181 | 634035417 | 17449.2 | 1220 | 146 | 2778 | 36 |
| 20261025004 | 4 | 36568 | 36427 | 47142 | 112148 | 65006 | 643791971 | 17605.3 | 1253 | 155 | 2868 | 36 |
| 20261025005 | 0 | 36409 | 36301 | 47128 | 111389 | 64261 | 638203690 | 17528.7 | 1228 | 154 | 2824 | 36 |
| 20261025006 | 1 | 36683 | 36562 | 47442 | 112249 | 64807 | 634645645 | 17300.8 | 1215 | 146 | 2776 | 36 |
| 20261025007 | 2 | 36834 | 36714 | 47382 | 111807 | 64425 | 628786502 | 17070.8 | 1198 | 143 | 2746 | 35 |
| 20261026000 | 1 | 36370 | 36248 | 46858 | 111879 | 65021 | 634884596 | 17456.3 | 1217 | 146 | 2764 | 41 |
| 20261026001 | 2 | 36353 | 36233 | 47029 | 111758 | 64729 | 636688108 | 17514.0 | 1224 | 146 | 2778 | 39 |
| 20261026002 | 3 | 36241 | 36092 | 46794 | 111642 | 64848 | 630696346 | 17402.8 | 1197 | 146 | 2764 | 40 |
| 20261026003 | 4 | 36102 | 35997 | 46373 | 111232 | 64859 | 644919269 | 17863.8 | 1255 | 155 | 2870 | 37 |
| 20261026004 | 0 | 36203 | 36092 | 46600 | 110634 | 64034 | 648611830 | 17916.0 | 1270 | 157 | 2880 | 36 |
| 20261026005 | 1 | 36275 | 36148 | 46521 | 111424 | 64903 | 638412299 | 17599.2 | 1236 | 148 | 2798 | 36 |
| 20261026006 | 2 | 36408 | 36290 | 47065 | 111140 | 64075 | 628232080 | 17255.3 | 1195 | 143 | 2760 | 35 |
| 20261026007 | 3 | 36439 | 36320 | 46809 | 111302 | 64493 | 641462300 | 17603.7 | 1239 | 145 | 2788 | 35 |


Run 4, the 15b22a77 program (runs 1-3 are in the development record and equal it in claws, groups and DP hits): fourth run (the 15b22a77 program; head subset 0 in every measured window): mean 639,254,086 operations per window, 36424.71 distinct claws, 36305.62 groups; identical claws, groups and DP hits in every window: False.

| window seed | distinct claws | groups | operations (fourth run, the r38b program of 15b22a77; head subset 0 in every window) |
| --- | ---: | ---: | ---: |
| 20261024000 | 36347 | 36235 | 634889427 |
| 20261024001 | 36434 | 36321 | 640655832 |
| 20261024002 | 36112 | 35988 | 637787705 |
| 20261024003 | 36815 | 36671 | 649158244 |
| 20261024004 | 36452 | 36334 | 637210103 |
| 20261024005 | 36271 | 36152 | 635526123 |
| 20261024006 | 36544 | 36441 | 634118552 |
| 20261024007 | 36364 | 36253 | 635790337 |
| 20261025000 | 36286 | 36188 | 638788535 |
| 20261025001 | 36467 | 36345 | 642524495 |
| 20261025002 | 36116 | 35991 | 642729589 |
| 20261025003 | 36714 | 36600 | 638007762 |
| 20261025004 | 36547 | 36416 | 643471131 |
| 20261025005 | 36409 | 36301 | 638203690 |
| 20261025006 | 36183 | 36056 | 638882223 |
| 20261025007 | 36737 | 36616 | 630878055 |
| 20261026000 | 36440 | 36314 | 636829160 |
| 20261026001 | 36296 | 36174 | 638732290 |
| 20261026002 | 36540 | 36426 | 633095449 |
| 20261026003 | 36504 | 36395 | 642161825 |
| 20261026004 | 36203 | 36092 | 648611830 |
| 20261026005 | 36473 | 36343 | 643270583 |
| 20261026006 | 36498 | 36363 | 634023997 |
| 20261026007 | 36441 | 36320 | 646751136 |


## Appendix B. Declaration and program identity

# Pre-declaration of the 24 evaluation windows (written before the first run)

Date: 2026-10-24T17:01:59.357521Z
Program: pkg/r38joint.py, sha256 a8a83fab4709048fef6737e8478670330d5e736b9b8fd9ccd0c663bd222549c0, 38761 bytes (the shipped program may differ from this file only by the two
constants B_WINDOWS and W_BUDGET, which are set from this measurement; the diff will be printed in proof.md).
Parameters: class P as in the file (DPB 6, WIN 2^25, WORDS 27,648, BUCKET True, KEEP_LONGER True, MAXS 1280, CUTP 512, QCAP 4096,
NSLOT 128, WHEEL 2048, CMP1 12, KCAP 1300, RCAP 240, GCAP 2^21).
Command: three processes, `python3 -I pkg/r38joint.py --windows 8 --seed B --check --out runs/eval/win_B.json` for B in
20261024, 20261025, 20261026 (window seeds B*1000 + w, w = 0..7). Check mode asserts every claw.
Seeds (24): [20261024000, 20261024001, 20261024002, 20261024003, 20261024004, 20261024005, 20261024006, 20261024007, 20261025000, 20261025001, 20261025002, 20261025003, 20261025004, 20261025005, 20261025006, 20261025007, 20261026000, 20261026001, 20261026002, 20261026003, 20261026004, 20261026005, 20261026006, 20261026007]
Adoption rule: every window is kept; none is excluded for any reason. If a process is killed by the host, the
measurement is reported as incomplete and the run is NOT replaced. The claim uses, over the 24 windows: the one-sided 99%
Student-t upper bound of charged operations per window (mu+), the one-sided 99% lower bound of distinct claw groups per
window (g-), and the ratio bound r- = groups/claws as in 19034ce3; the time bound T = (W_BUDGET + R + 6 B) / 2728 with
B = ceil(G (1 + 2^-19) / g-) windows and W_BUDGET = floor(B mu+ (1 + 2^-20)) + 1. Tuning seeds used before this
declaration: 901 (2 windows, both table policies), 5, 11, 3 (selftests); organizer-seed windows (2^20) for WIN_EXP.
Design choices (bucketed table, keep-longer, window 2^25, DPB 6) were fixed from the simulator grid and the seed-901
measurement before this declaration.


## Amendment (written before the second run), 2026-10-24T17:40:15.372803+00:00
A judge-emulation critic pass on the first run's package found: Python control flow uncharged (about 15 decisions per DP hit,
the per-iteration halt tests, the stage-2 phase initialisation), no hard cap on stage-2 iterations, no stop when the trail
ids saturate, and the length field written unmasked. The program now charges CF_HIT = 16 per DP hit, CF_ITER = 4 per
iteration and CF_PHASE = 1024 per stage-2 phase, caps a stage-2 phase at S2CAP = 2^17 iterations, ends the window when
idc reaches 2^20, and masks the length to 11 bits. None of these change the walk, the table or the claws (the caps never
fire at the measured sizes); only the charged operations rise. The 24 declared seeds are re-run unchanged on this program
(LF line endings; sha256 b2d93c4bbbf6ef9d7e253d4deb17b467e3da428f07974b674edc346640d3c124, 39446 bytes). Adoption rule unchanged: all 24 kept. The first run's
results are kept in runs/eval_v1/ and reported beside the second in proof.md Appendix A. The claim uses the second run.
Also recorded: the first run's file on disk had CRLF line endings (sha256 bbed18f9...), the declaration hashed the same
text with LF line endings (a8a83fab...).

## Declaration of the G-rate measurement windows (written after the 24-window runs and before the first of the 48 G windows, 2026-10-24 ~18:30Z)
The G filter on the walk's claws measured 178 of 13,787 C2 passes over the 24 windows (0.0129; the inherited exact rate
is 0.016202; z = -3.1 on raw counts) and 15 of 2,147 on the two seed-901 tuning windows; a direct Monte Carlo of the
walk's (a0, u) population without claw conditioning (tools/gtest.py, 3 x 10^6 draws) gives G|C2 0.0163-0.0166 (uniform
u: 0.0162). To settle the walk's own rate, 48 further windows of the shipped program are run: three processes,
`--windows 16 --seed B --check` for B in 20261027, 20261028, 20261029 (seeds B*1000 + w, w = 0..15). Adoption rule: all
48 kept. Use: the pooled raw stage counts (c1, c2, g, f7) of these 48 windows together with the 24 evaluation windows
decide the charge: if the pooled G|C2 rate's one-sided 99% lower bound is below the exact 0.016202, q_pf is charged at the
exact C1 and C2 rates times that lower bound (and the F7 rate exact), otherwise the exact q_pf stands; either way the
measured rates are reported. These windows are NOT used for the yield/cost bounds (mu+, g-), which stay on the 24
declared windows. The lower bound is taken on effective trials n_eff = raw C2 passes x (1 - rediscovery share), since a
rediscovered claw repeats the same G outcome (critic finding R3).

Statistic note (recorded after the first run, before the claim was fixed): the original declaration named one-sided 99%
Student-t bounds; the claim uses, for each quantity, the most conservative of the pooled one-sided 99.9% bound and each
8-window run set's own one-sided 99% bound, which is never less conservative than the declared statistic.


## Amendment 2 (r38b, written before the third run), 2026-10-24T22:35:42+00:00Z
The first filing (eab3eea4, this program with B_WINDOWS/W_BUDGET set) was refuted on one fatal: the exact memory inventory
charged 256 register words while Attack.__init__ allocates 512 (F-MEM-512). The r38b program keeps the 512-word allocation
and charges it (rule: every allocation of the attack path charged at its allocated size). Two measurement-only changes
are made to the program: (a) the furthest post-filter stage reached by every DISTINCT claw is recorded (s.dstage, filled
only when measure=True, never in --attack) so that the G rate can be bounded on distinct claws (judge finding F-03);
(b) experiment r38-p8-claw trial 0 additionally executes both kernel images on 256 random lanes against the scalar step
(F-04). No charged operation changes (the frozen WIN_EXP counts hold unchanged on this program). Program sha256 f85c41a603f6fcec0413159182584284540bcc7cd3b1174ccb7f728625bb4151
(LF, 40,897 bytes). The 24 evaluation seeds and the 48 G-measurement seeds are re-run unchanged on this program; the
claim uses this third run; the second run's results are kept in runs/eval_v2 and runs/gwin_v2. Adoption rule unchanged:
every window kept. G charge rule, amended: the one-sided 99% Wilson lower bound is computed on DISTINCT claws (plain
counts of distinct C2 passes and distinct G passes) and on the raw counts with the rediscovery-corrected n_eff; the
LOWER of the two is charged when below the exact 0.016202; both are reported.


## Amendment 3 (r38b, written before the fourth run), 2026-10-24T23:14:19+00:00Z
A judge-emulation pass on the r38b package found two memory items under the F-MEM-512 precedent: module-level derived
data (the P8 traces, WIN_EXP, constants; under 1.7 KB) absent from the inventory, and a transient in the attack and
measurement loops where the next window's Attack is constructed while the previous one is still bound. The inventory
gains a 4,096 B row (total 1,027,581 B = 2^19.9709) and the loops now release the previous window (`A=None`) before
building the next; the measured path (window_setup, iter1, hit, stage2, claw) is byte-identical, charged operations are
unchanged (WIN_EXP holds). Program sha256 dfbefa07b752650f5acbaf1640e18f09ffe384942f84dadcaa8980de3163c99d (LF, 41,237 bytes). The 24 evaluation seeds and the 48 G seeds are
re-run unchanged on this program; the claim uses this fourth run; the third run is kept in runs/eval_v3, runs/gwin_v3.
Adoption rule unchanged. Printed precision: the G bound, q_pf, p_claw and log2 G are printed to 6-7 digits so that
B = ceil(G (1 + 2^-19) / g-) reproduces from the proof's own figures.


## Amendment 4 (r38c, written before the fifth run), 2026-10-25T00:41:46+00:00Z
15b22a77 (the r38b program) was refuted on F-MEM-RETAINED-PAIRS: stage 2 did not stop at the first accepted pair, so up
to 4,095 output pairs could have been retained in one phase. The r38c program: every loop of stage 2, iter1 and run_window
exits on s.success and exactly one collision pair is retained (s.message, a single slot); the kernel gate list is capped in
code (GEN_MAX = 1,425, G.emit halts), the queue has a hard halt at QCAP besides the QFULL rule; the measurement containers
are created only when measure=True (never in --attack). Head subsets: the attack cycles the five 4-head subsets from a
uniform random start; the measured windows (--windows) use subset (B + w) mod 5 for seed base B and window index w, so the
24 evaluation windows sample the five subsets (5, 6, 5, 4, 4 windows) and the 48 G windows (10, 10, 10, 9, 9); the groups
bound charged is the minimum of the pooled/per-set bound and the smallest per-subset one-sided 99% t bound. No charged
operation changes (WIN_EXP holds unchanged). Program sha256 cbadf05d1a1f5c7c78020b1795b0b6511a4209299fb4696bf367a17141c923d0 (LF, 42,549 bytes). The 24 evaluation seeds and the 48 G
seeds are re-run on this program (fifth run of the evaluation seeds; the claws found per window now depend on the subset,
so counts change); the fourth run is kept in runs/eval_v4 and runs/gwin_v4. Adoption rule unchanged: every window kept.


Erratum to Amendment 4 (2026-10-25T01:18:07+00:00Z, after the fifth run, text only): the per-subset window counts are [5, 6, 5, 4, 4] for the 24 evaluation windows and [9, 9, 10, 10, 10] for the 48 G windows (subsets 0..4); the amendment's '(10, 10, 10, 9, 9)' listed the G counts in the wrong order. Also recorded: runs 1-4 measured head subset 0 in every window (not 'restarting at subset 0 per process').


All hashes are of the file bytes with LF line endings. Shipped program `experiments/r38joint.py`: sha256 `861e6f22ec333db141a4ac57087fa656c39f921174037e35a32674e65a0363d8`, 42,600 bytes (the amendment's 41,237 bytes plus the 51 bytes of the two constants; the inventory charges the shipped length). Fifth-run program: sha256 `cbadf05d1a1f5c7c78020b1795b0b6511a4209299fb4696bf367a17141c923d0` (the hash in Amendment 4 above). The diff is the two lines
```
- B_WINDOWS=None; W_BUDGET=None   # set by the proof after the measurement (Section 7)
+ B_WINDOWS=3227292921399400871242; W_BUDGET=2082564932999596136475692503019   # proof.md Section 7, set from the 24 pre-declared windows
```
