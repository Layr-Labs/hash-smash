# SHA-256 reduced to 38 steps: ordinary collision by the P1 row-16 claw of the P8 characteristic, found by a distinguished-point walk in 2^20 bytes

**Target:** `sha256-r38-prefix-v1` (SHA-256 steps 0..37 on every padded block, standard IV, FIPS 180-4 padding, feed-forward, all eight digest words), lane `exploratory`.
**Claim:** `time_log2 = 89.5906` target-compressions (exact 89.59051, rounded up), `memory_log2_bytes = 19.9436` (1,008,373 bytes, exact by construction, under 2^20 = 1,048,576), success probability at least 0.39, `preprocessing_log2 = 78.09276` (the allowances of Section 9, charged inside the time), advice 260 bytes (`nonuniform_advice_log2_bytes = 8.03`).
**Scalar:** `hashsmash-scalar-tm-v1`: `89.5906 + max(0, 19.9436 - 20) = 89.5906`. The peak memory is below one MiB, so there is no memory penalty.

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

**What a claw still has to pay (`51613d1c` Sections 6, 7, 9).** A claw is a *good pair* when the four post-filters hold on the real words of the two members: `C1: W8y - W8x = D8`, `C2: s0(W9y) - s0(W9x) = D9s`, `G: s0(W8y) - s0(W8x) = T8`, `F7: W7y - W7x = D7 and s0(W7y) - s0(W7x) = F7d` (the five constants are the published pair's differences, recomputed at import). `51613d1c` counts them exactly: `q_pf = P(C1 C2 G F7 | claw) = 57,726,359,870,197 x 287,309,824 / 2^90 = 2^-16.1877` for `a0` uniform in the window `R = 9` (`a0 in [9 x 2^26, 10 x 2^26)`) and `a1` uniform. A good pair is accepted (its two second blocks collide) with probability `q3r = q3_P1 x 2^32 / 160 = 2^-71.4010`, where `q3_P1 = 2^-96.0791 = 2^-96.0133 x 2^-0.0658` is the registered accepted-event rate of the P1 family on window `R = 9` (the A0-variant base over 128 + 400 seeds and the paired P1-minus-A0 difference, one-sided 99% lower bound `D_LB = -0.0658` over 36 seeds; `51613d1c` Section 9 and Appendices P, Q). Together one claw yields a collision with probability `q_pf x q3r = 2^-87.5887` at the exact rates. Section 5 reports the rates measured on this program's claws and Section 7 states the charged `p_claw = 2^-87.8906` (charged `q_pf = 2^-16.4896`); Section 9 states exactly how these numbers are inherited.

## 3. The walk and the program

**Points.** A point is a 29-bit word `v`. Let `r(y)` be the 32-bit word `y` with bits 0, 2 and 10 removed (29 bits). The walk step is
- side `s = bit 28 of v`. **A side** (`s = 0`): head index `j = bits 26..27` (one of the window's four heads `heads4`, Section 3 below), `a0 = (9 << 26) | bits 0..25` (window `R = 9`), image `y = F(a0) - t_{heads4[j]} 2^13`;
- **B side** (`s = 1`): `u = v' | mix4(v') << 28` with `v' = bits 0..27` and `mix4 = (v' >> 3) xor (v' >> 11) xor (v' >> 19) xor (v' >> 24) mod 16`, image `y = H_0 - P(u)`;
- next point `v_next = r(y)`; `v_next` is a distinguished point (DP) iff its low 6 bits are zero.

**Lemma 2 (what a cross-side collision is).** Let `x` be an A point and `y` a B point with `r(y_A) = r(y_B)`. Then `y_A xor y_B` lies in the span of `{1, 4, 1024}`, so `d = y_A - y_B = sum_k 2^k (a_k - b_k)` over `k in {0, 2, 10}` with `a_k, b_k` the free bits of the two images, and `(a0, u)` is a claw with head `heads4[j]` iff `d in OFFS` iff `a_k >= b_k` for all three `k`. The program tests `d` exactly on every cross-side collision (`claw_core`: `d & ~0x405 == 0`); the collisions that fail it (`notclaw`) are discarded. Under uniform free bits the pass probability is `(3/4)^3 = 27/64 = 0.4219` (measured 0.4221 over the 24 windows). No equality test on a quotient of the word does better than 3/4 per free bit, and the 29-bit quotient is the best choice among quotienting 0..3 of the free bits (DESIGN record; it is a design choice, not a premise: the program tests `d` exactly).

**Heads.** The 20 heads are partitioned into five subsets of four, `SUBSETS[s] = {4s, .., 4s+3}`; window `w` (1-based, per process) uses subset `(w - 1) mod 5`, so over any five consecutive windows every head is used once. The A side of the point space (2^28 points) is then `(a0 in R = 9) x (4 heads)`, balanced against the 2^28 B points (cross-side share of collisions measured 0.4996).

**Why a0 stays in window R = 9.** `q_pf` is an exact count for `R = 9` and `q3_P1` is measured on `R = 9` (`51613d1c` refused to widen the window until it had measured the transfer, its A.23-A.28). The head bits enlarge the A side instead.

**The program (`experiments/r38joint.py`, sections [3]-[4]).** Per first block `M0` the program runs one WINDOW of `2^25` walk evaluations (`Attack.run_window`):
1. Two random 256-bit words give `M0` (16 words, 18 operations); one target compression gives `cv`; the constants of `F` (140) and of the post-filter chain (260).
2. The generator (`build_kernel`, `allocate`, `to_source`, section [2]) emits the two kernel images (bank A to bank B and B to A) of the 256-lane step: one record = XOR, AND, OR or NOT of 256-bit registers (bit `j` of the 256 points lives in plane `j`; rotations are renaming; constants of `cv` and of the four heads are folded; MAJ and CH with constant operands reduce to wires; a `MUX` selects the A or B image per lane; the DP plane is the OR of the six low output planes). The images have 1216 to 1270 records (cap `KCAP = 1300`) and use at most 160 registers (cap 240; 64 fixed: two banks of 32 planes, the DP plane at 64). The generator is charged **at the cap `GCAP = 2^21 = 2,097,152` operations per window**, in `m.o` (Section 4). Verification: `selftest` and `r38-p8-claw` trial 0 execute the images on 256 random lanes against the scalar step (0 mismatches); check mode asserts every claw found by the walk against the scalar maps.
3. The table is cleared (4 operations per word): `WORDS = 27,648` words of 32 bytes, six entries of 40 bits each; 256 trails start in the 256 lanes, trail `i` at point `i`.
4. Stage 1 (`Attack.iter1`): `2^17` iterations of the kernel; on a DP (`Attack.hit`): the lane is found (binary search), the 23 high bits `r` of the point are extracted (Horner over the planes), the word is `r x 27,648 >> 23` (four shifts and three adds), the check field is `chk = r mod 512` (the `r` values of one word form an interval of at most 304 values, so `(word, chk)` determines `r`: no false match). The six entries of the word are scanned: an entry with the same `chk` and a nonzero length is a MATCH (two trails ended at this DP): the pair `(id, len)` of both trails goes to a queue of 4096 pairs, and the stored entry is replaced only if the new trail is longer (keep-longer, dkuthoore `0b2616e3`); otherwise the DP is written to an empty entry of the word, or, if the word is full, to the entry selected by a rotating counter. The lane receives a new trail (next id, `insert_lane`). A trail older than 1280 iterations is cut by a scan every 512 iterations.
5. Stage 2 (`Attack.stage2`) when the queue holds 3840 pairs and at the end of the window: pairs run in lane pairs `(p, p + 128)`, 128 slots, continuous refill; the longer trail starts first and the shorter `len` difference iterations later (timing wheel of 2048 buckets); after each iteration the two states are compared (12 planes, then the other 17 for candidates); the first equal state gives the predecessors `(x, y)`; `x = y` (the shorter trail started on the longer one) is discarded (`degenerate`).
6. The claw (`Attack.claw`, `claw_core`, every operation counted): sides from bit 28 (same side: discarded, `same`); decode `(a0, j)` and `u`; `F(a0)`, `P(u)`, the exact test of Lemma 2 (`notclaw` on failure); `a1 = u - F + a0 + K2` (the claw equation); `C1` on `W8x, W8y`; `C2` on `W9`; `G`; `F7` (the words from the closed forms of the step equations, asserted against `variantW` in check mode); step 3b: both second blocks `W0..W15` from `(cv, a0, a1)`, two 38-step compressions (2 x 2728 charged), exact comparison of the eight words. On acceptance the two 3-block digests are recomputed (6 x 2728 + 1600 charged) and the messages are output.

The attack is the loop over first blocks (`--attack`): the 16 words of each window's first block are drawn from the operating system's random source (fresh algorithmic coins; `--seed` exists only for the measurements and experiments). Halts: a success, the window count `B_WINDOWS`, the charged-work budget `W_BUDGET` (Section 7), and a window ends when its trail counter `idc` reaches `2^20` (it peaks at 527,650 over the 24 windows).

## 4. Machine model and prices (declared once)

Counted 256-bit word RAM with 256 registers (8,192 bytes, counted), cost model `collision-frontier-v5`, unit the target compression = 2728 operations (`C` of `sha256-r38`). One operation each: XOR, AND, OR, NOT, move, shift, rotate, add, subtract, compare-and-set; a conditional branch is a compare and a branch (2); a load or a store is 3 (index shift, base add, access); a call and its return are 2. A kernel record (register-to-register XOR/AND/OR/NOT of 256-bit words) is one operation and is stored in 5 bytes (opcode and three 10-bit register fields; the price of `6b678689`, `0c1ef7c3`, `19034ce3`, `0b2616e3`). Every word operation of the program passes through the class `Mach` (one method = one charged primitive; `m.o` counts them); the kernel is charged `len(records)` per iteration; the program's own control flow that is not a `Mach` call (the six-entry scan loop and its flag tests, the keep-longer chain, the per-iteration cut-scan and halt tests, the initialisation of a stage-2 phase) is charged by explicit allowances in `m.o`: `CF_HIT = 16` per DP hit (an instrumented count found 14.3-15.7 decisions), `CF_ITER = 4` per iteration, `CF_PHASE = 1024` per stage-2 phase; the generator is charged the cap `GCAP = 2^21` per window (its own builder-call census, 2,880 calls at most over the 24 windows, each a handful of Python operations, is far below the cap; the cap is the charge). Memory is the inventory of Section 6, with the code charged as the full byte length of the shipped program. These are prices of the cost model, not probabilistic premises.

## 5. The exact ledger (24 pre-declared windows)

The cost of a window is `m.o` after the window; the program prints it (`--windows N --seed S --check --out f.json`). **The 24 evaluation windows were pre-declared** (three run sets of 8 windows, one per process) (seeds `B x 1000 + w`, `B in {20261024, 20261025, 20261026}`, `w = 0..7`; adoption rule: every window kept, none excluded; the declaration file names the program hash before the first run and is reproduced in Appendix B) and run in check mode (every claw asserted against the scalar maps, the real `E16x`, and the real words `W7, W8, W9` of both members; 0 failures; check mode adds no counted operation). Tuning before the declaration: 2 windows (seed 901) in each table policy, the selftests, and the four organizer-seed windows of `r38-window-small`.

Per window (Appendix A lists all 24): mean `639,254,086.4` operations (standard deviation `4,805,920`, largest `649,158,244`), mean `36,424.71` distinct claws (sd `182.2`), mean `36,305.62` distinct claw groups (sd `180.3`; two claws are in one group when they share `a0` or `u`), groups/claws `0.996731`. Per distinct claw: **`17,550.0` operations = 2^14.0992 = 6.433 compressions**.

| category (`Mach.cat`) | share of operations |
| --- | ---: |
| stage-1 walk (kernel records + DP plane test + loop) | 23.5% |
| stage-1 DP handlers (find lane, extract, table, queue, new trail) | 24.5% |
| stage 2 (kernel, launches, wheel, compares, merges, extraction) | 49.4% |
| claw decode, exact test, post-filters, step 3b | 1.7% |
| window setup (first block, constants, table clear, lanes) | 0.3% |
| generator (charged cap) | 0.3% |
| cut scan, run setup | 0.1% |

Events per window (means): hits 524197.7, matches 231826.7, pairs 231826.7, merges 231826.7, degenerate 9107.6, same 111439.3, cross 111279.8, claws 46971.5, notclaw 64308.3, c1 5869.5, c2 574.5, g 7.4, f7 0.4, step3b 0.4, trails 524197.7, cuts 4.1, slotfull 131036.2, s2iters 161337.8. The quotient's false positives (`notclaw`) are 0.578 of the cross-side collisions (Lemma 2: 1 - 27/64 = 0.578 expected); same-side collisions are discarded; re-discovered claws (raw minus distinct) are 0.225 of the raw claws and are not counted. Post-filter stage counts over the 24 windows: C1 140,867 of 1,127,315 raw claws (0.1250; 1/8 = 0.125 under H1-P1 of `51613d1c`), C2 13,787 of the C1 passes (0.0979; exact 53,096,854 / 2^29 = 0.0989), G 178 of the C2 passes (0.0129; exact 2^-5.948 = 0.0162), F7 9 of the G passes (exact 0.0669), step 3b 9, accepted 0 (expected `3.93e-21` over the 24 windows).

The G filter is CHARGED at the measured rate: over the 72 windows (24 evaluation + 48 declared G-measurement windows) the walk's claws pass G in 608 of 41,595 C2 passes (0.01462 against the exact 0.016202 of 51613d1c, z = -2.56 on raw counts); the one-sided 99% Wilson lower bound 0.01314, taken on n_eff = 32,233 effective trials (the raw C2 count less the 22.5% of raw claws that are rediscoveries of a claw already found in the window, which repeat the same G outcome), replaces the exact rate in q_pf, so the charged q_pf is 2^-16.4896 instead of 2^-16.1877 (+0.3019 bit). Per run set: seeds 20261024000..20261024007: C1 46703, C2 4466, G 53, F7 1; seeds 20261025000..20261025007: C1 47261, C2 4665, G 48, F7 3; seeds 20261026000..20261026007: C1 46903, C2 4656, G 77, F7 5; seeds 20261027000..20261027015: C1 93906, C2 9117, G 153, F7 4; seeds 20261028000..20261028015: C1 94832, C2 9225, G 133, F7 2; seeds 20261029000..20261029015: C1 94057, C2 9466, G 144, F7 13.

The claim does not use the means as they stand. For each quantity it uses the most conservative of (i) the one-sided 99.9% Student-t bound over the 24 windows (23 degrees of freedom, 3.485 standard errors) and (ii) each of the three 8-window run sets' own one-sided 99% bounds (7 degrees of freedom, 2.998 standard errors): at most `mu+ = 646,492,421` operations per window, at least `c- = 36,188.45` distinct claws and `g- = 36,070.01` distinct groups per window, and a group-to-claw ratio of at least `r- = 0.996412` (`c- r- = 36,058.63`). Pooled 99.9% bounds: mu+ 642,672,886, g- 36,177.4, c- 36,295.1, r- 0.996529. Per-set 99% bounds: set 1 (seeds 20261024000..20261024007): mu+ 643,331,814, g- 36,085.6; set 2 (seeds 20261025000..20261025007): mu+ 643,457,371, g- 36,070.0; set 3 (seeds 20261026000..20261026007): mu+ 646,492,421, g- 36,182.9. (The plain 99% pooled bounds, 2.500 standard errors, give time_log2 89.5741.)

**Every window has a worst-case cost (R).** Every loop is bounded by a constant of the program: at most `2^17` stage-1 iterations (the window also ends when the trail ids reach `2^20`), each at most `KCAP + 11` kernel-and-loop operations plus at most 256 DP handlers (straight-line apart from the 23-plane extraction, the six-entry scan and the 20-plane insert; under 1,000 operations each including `CF_HIT`) and the cut scan (under 20,000): under `2^36`. At most `2^25` DP hits per window (one per lane per iteration), so at most `2^25` queued pairs and at most `2^25 / 3840 + 2^17 / 512 + 1 < 2^14` stage-2 phases; a phase runs at most `S2CAP = 2^17` iterations (hard cap; a pair needs at most `MAXS + CUTP = 1,792`, and `3840 / 128 x 1,792 = 53,760 < 2^17`, so the cap never fires in a correct run), each at most `KCAP + 3 + CF + 128 x (launches + merge + extraction + claw filters + step 3b + the final digests 6 x 2728 + 1600, under 18,000)` `< 2^21.7` operations. Hence the charged work of a window is at most `2^36 + 2^14 x 2^17 x 2^21.7 < 2^52.1 < R = 2^53` operations; its distinct claws and groups are at most `2^25`.

## 6. Memory, exact by construction

Bytes, including everything the program holds at its peak (`tools/mem_inventory.py` of the development record computes this table from the shipped file):

| item | bytes |
| --- | ---: |
| register file 256 x 32 B | 8192 |
| two kernel images, KCAP 1300 records x 5 B x 2 | 13000 |
| program text (every byte of experiments/r38joint.py; code, routines, generator, constants) | 39497 |
| table: WORDS 27648 x 32 B (6 entries of 40 bits per word) | 884736 |
| lane array LA, 256 words | 8192 |
| stage-1 save area, 32 words | 1024 |
| queue, QCAP 4096 pairs x 8 B | 32800 |
| pair slots bid and nxt, 2 x 128 words | 8192 |
| timing wheel, 2048 buckets x 2 B | 4096 |
| free-slot stack, 128 words | 4096 |
| constants, counters and per-window scalars (cv, heads, pf constants, idc, it, rot, qn), 128 words | 4096 |
| advice: P8 chaining value and two blocks (40 words), heads R16H (20 words), the five differences D7 D8 D9s T8 F7d | 260 |
| first block M0 and the two second blocks under construction, 48 words | 192 |

The code is charged as the complete byte length of `experiments/r38joint.py` (39,497 bytes): every instruction of the machine program, the routines, the generator, the P8 data and the constants are inside that text, so the figure is above any 36-byte-per-instruction encoding of the executed instructions (the per-block census `Mach.blk` of executed straight-line passes totals 7,213 operations over 26 blocks, for information). The generator's scratch (the gate list and the allocation, under 200 KB in Python; on the machine the gate list is at most `KCAP` records of 5 bytes plus a last-use table) is built before the table is cleared and lies inside the table region; it adds nothing to the peak. Setup and the run share one peak: there is no solver, no search campaign and no preprocessing buffer. **Total 1,008,373 bytes = 2^19.9436; 40,203 bytes spare below 2^20.**

## 7. Success probability and time

`p_claw = q_pf x q3r = 2^-87.8906` with the charged `q_pf = 2^-16.4896` (Section 5) and `q3r = 2^-71.4010` (Section 2; Section 9 for the premises). **Claws are counted by groups.** Two claws of a window can share a trial only through a shared endpoint (`a0` or `u`); grouping the distinct claws of a window into connected components by shared endpoint (`count_groups`), one claw per group is one trial of the accepted event, and distinct groups have disjoint inputs `(a0, a1)`. Conditional on at least `G` distinct groups, the run succeeds with probability at least `1 - exp(-G p_claw)`. Set `G p_claw = lambda = -ln(0.60999) = 0.494313`, so `1 - exp(-lambda) = 0.390010` and `log2 G = 86.8741`. With the 99% lower bound `g- = 36,070.01` groups per window and the margin `(1 + 2^-19)`,
`B = ceil(G (1 + 2^-19) / g-) = 3931537570268723126847 = 2^71.7356` windows (first blocks).

**Total work (Bernstein) and total groups (Hoeffding).** The windows are independent trials (fresh coins per window, H1 part (a)), each with charged work `W_j in [0, R]` and distinct groups in `[0, 2^25]`; `E[W_j] = mu <= mu+` and `E[groups] = g >= g-` is premise H1 part (b). Since `0 <= W_j <= R`, `Var(W_j) <= E[W_j^2] <= R mu <= R mu+`, and Bernstein's inequality with `t = 2^-20 B mu+` gives: the total work of `B` windows exceeds `B mu+ (1 + 2^-20)` with probability at most `exp(-t^2 / (2 (B R mu+ + R t / 3))) = exp(-2^-40 B mu+ / (2 R (1 + 2^-20/3))) = exp(-2^7.0)` (the leader's Lemma 3 form; a plain Hoeffding bound with `R = 2^46` would be vacuous at this `B`). By Hoeffding's inequality the total number of distinct groups falls below `B g- (1 - 2^-20) >= G` with probability at most `exp(-2 B (g- 2^-20)^2 / 2^50) = exp(-2^13.0)`.

**The budget.** `--attack` stops at a success, after `B_WINDOWS = B` windows, or as soon as its charged work reaches `W_BUDGET = floor(B mu+ (1 + 2^-20)) + 1 = 2541711665391306710115363635867` operations (checked before each window, 6 operations per window), whichever comes first; so its charged work is at most `W_BUDGET + R + 6 B` in every run. The time is
`T = (W_BUDGET + R + 6 B) / 2728 + 2^78.09276` target-compressions (the second term is the preprocessing allowance of Section 9, 0.0346% of the total), **`log2 T = 89.59051`, `time_log2 = 89.5906`** (rounded up; the plain means give 89.5649). By the union bound the unconditional success probability is at least `0.390010 - exp(-2^7.0) - exp(-2^13.0) > 0.39`.

Sensitivity: every bit of `log2 p_claw` moves `time_log2` one for one (Section 9 lists what each inherited number is and its registered margin); each +10% of operations per distinct claw is +0.138 bit.

## 8. Experiments (organizer sandbox)

Both declared experiments run in the organizer's Docker executor (20 s, 128 MiB); every number below is hard-asserted in the program, so a failure is an experiment error, not an observation.
- `r38-p8-claw`: trial 0 builds the kernel images for `PCV` and runs `claw_core` on the P8 pair (`a0 = A0`, the head of its `E16x`, `u = W1`): the exact claw test, C1, C2, G, F7 and step 3b all pass and the two second blocks collide (`accepted = 1`); trials 1..255: random `(cv, x, y)` of the walk's encoding: `F(a0) + P(u) = E16x` on the real trace, `W1 = u`, and `claw_iff_r16` (the program's test equals "the real `E16x` is a row-16 pass of P8 with the point's head").
- `r38-window-small`: trials 0..3 run four windows of `2^20` evaluations (4096 iterations) in check mode on the trial seeds; the frozen counts `WIN_EXP` (dp hits, matches, stage-2 iterations, merges, cross-side pairs, raw and distinct claws, groups, C1, C2, operations, kernel records, block census) are asserted for the organizer's trial seeds; every claw passes every check-mode assertion. The four organizer windows: seed 13353826..: 16437 hits, 888 matches, 185 raw / 184 distinct claws, 184 groups, C1 23, C2 3, 13544329 operations; seed 85299089..: 16343 hits, 862 matches, 178 raw / 175 distinct claws, 175 groups, C1 25, C2 0, 13535361 operations; seed 18362963..: 16203 hits, 904 matches, 185 raw / 183 distinct claws, 183 groups, C1 21, C2 2, 13466257 operations; seed 65056259..: 16335 hits, 933 matches, 198 raw / 193 distinct claws, 193 groups, C1 24, C2 4, 13618813 operations.
Both experiments were executed locally through the organizer's own executor before submission (reports in the development record); the organizer's run is the evidence.

## 9. Premises (declared in `claim.json`) and what is inherited

- **H1-walk-model** (score-critical). (a) The chaining value of a random first block is an independent random value for the maps `F` and the later events, so windows are independent trials. (b) The yield and the cost of a window are those measured on the real step function over the 24 pre-declared windows (Section 5; `mu+`, `c-`, `g-`, `r-`); the program cannot be run for `2^71.7356` windows. (c) A distinct claw group is a trial of the accepted event with probability `p_claw`, independent of the walk's yield. Support: the walk's inputs `(a0, u)` are uniform on the A-side window and on the B-side `u` set apart from the claw equation (part (d) below); the post-filter rates measured on this program's claws (Section 5) agree with the exact rates of `51613d1c` for C1 and C2, and G, measured below the exact rate, is charged at its lower bound.
- **H1-P1-postfilter-law** (score-critical, inherited from `51613d1c` Section 6 as a transfer premise). `q_pf = 2^-16.1877` is the exact count of `C1 C2 G F7` over `a0` uniform in `R = 9` and `a1` uniform over 2^32; it is taken as the rate for the claws this program finds for C1, C2 and F7, while G is charged at the lower bound measured on this program's claws (Section 5: charged `q_pf = 2^-16.4896`). Our claws have `a0 = (9 << 26) | 26 point bits` (uniform in the window by construction) and `a1 = u - h(a0, cv)` with `u` ranging over the `2^28`-element set `{v' | mix4(v') << 28}` of one chaining value; across chaining values `h(a0, cv)` is uniform, so `a1` is uniform over the attack. Disclosed: within one chaining value only `2^28` of the `2^32` values of `u` are reachable. Measured C1/C2/G/F7 stage rates over the 24 windows are in Section 5.
- **H2-P1-q3-transfer** (score-critical, inherited from `51613d1c` Section 9, its H2-P1 and H10 as a transfer premise). `q3r = 2^-71.4010` is the probability that a good pair is accepted, from the registered `q3_model = 2^-96.0133` (A0-variant family; two one-sided 99% bounds, union 98%) and the paired P1-minus-A0 difference on window `R = 9`, one-sided 99% lower bound `D_LB = -0.0658` over 36 seeds (its margin against the point estimate `-0.0121` is 0.0537 bit). We did not re-measure the deep rows (the leader's tool is a C program run for 36 seeds x 2^28 samples; it is outside the organizer sandbox). **New in this program:** the row-16 pass of a claw is one of 4 heads x 8 offsets per window instead of all 160; the subsets rotate so the attack-wide mixture over the 160 passes is uniform, which is the mixture `51613d1c` measured (its q3 is pooled over S160 via `2^32 / 160`). The premise is that the accepted-event rate does not depend on which 4-head subset a window uses beyond this uniform mixture; `51613d1c` A.26 measured the only head/window dependence within reach (the `r16|all4` gate, 298 events: -0.116 +/- 0.167 between windows, consistent with zero) and declared the deeper transfer (its H10); we declare the same. Risk statement: a materially lower acceptance rate for some head subsets would raise `B` and `time_log2` one for one in `log2 q3r`.
- **H3-P1-within-cv** (supporting). Claws of one window that share no endpoint are independent trials of the accepted event (`51613d1c` H3-P1, measured there on 24 chaining values and on the forced-bit events of rows 17..21); we count one claw per endpoint-sharing group (`r-`), which removes the only dependence `51613d1c` found necessary to treat.
- **H4-allowances** (score-critical, inherited). `A_C = 2^78`, `A_S = 2^74` (the characteristic search behind P8 and its Step-1 solve, `51613d1c` Section 11 and its H4a/H4b with the published run logs) and `DEV = 2^70` compressions are charged in full inside `T`: `preprocessing_log2 = log2(2^78 + 2^74 + 2^70) = 78.09276`. Our own development (this program and its measurements: under 40 core-hours on a 14-core machine, under `2^50` operations) is far inside `DEV`.
- **H5-prices** (score-critical). The prices of Section 4; the 5-byte kernel record and 1 operation per record (`6b678689`, `0c1ef7c3`, `d90878ff`, `19034ce3`, `0b2616e3`); the generator charged at the cap.
- **H6-memory** (score-critical). The inventory of Section 6 is the peak; code is charged as the shipped program's full byte length.

## 10. Advice and preprocessing

Advice: the P8 chaining value and the two published blocks (40 words), the 20 heads, the five differences: 260 bytes, `log2 = 8.03`. Preprocessing: the allowances of H4 (`2^78.09276` compressions), charged inside `T`; this program has no table build, no solver and no precomputation of its own.

## 11. Disclosures and limitations

1. **The claw population is new.** The leader scans all `2^32` values of `u` and all 160 row-16 passes per chaining value; this program reaches `2^28` values of `u` per chaining value and 32 of the 160 passes per window (uniform over windows). The downstream rates `q_pf` and `q3r` are inherited as transfer premises (H1-P1, H2-P1); only the post-filter rates are re-measured here (Section 5). The deep acceptance rate was not re-measured; its registered margins are those of `51613d1c`.
2. **Re-discovered claws and the quotient.** 0.225 of the raw claws are re-discoveries of a claw already found in the window and are excluded from the count; 0.578 of the cross-side collisions are not claws (Lemma 2) and are discarded after an exact test. Both are costs the ledger pays, not events the claim uses.
3. **Stage 2 lane utilization** is about 63% (a pair occupies two lanes while the longer trail walks alone); stage 2 is 49.4% of the operations. A two-phase catch-up would lower the cost; it is not in this program.
4. **The generator is charged at a cap** (`2^21` per window, 0.3% of the work), not at an executed-operator count: this program has no WebAssembly generator; the cap is above its Python builder-call census by a factor over 728.
5. **Frozen counts.** `WIN_EXP` holds the four organizer-seed windows measured through the organizer's executor on the pinned image; the asserts fire only for those seeds.
6. **Two runs of the 24 declared seeds.** The first run used the declared program; a critic pass then found uncharged control flow (about 1.2% of the work), no stage-2 cap and no stop on trail-id saturation; the program was amended (the allowances of Section 4, `S2CAP`, the saturation stop, the masked length field; the walk, the table and the claws are unchanged) and the same 24 seeds were run again: identical claws, groups and DP hits in every window, operations up by the allowances. The claim uses the second run; Appendix A lists both. The shipped file equals the second-run program plus the two constants of Section 7 (Appendix B).
7. **Remaining costs.** `q3r` (2^-71.40) and `q_pf` (2^-16.19) are the characteristic's; the walk's `2^14.0992` operations per claw against the table's `2^7.46` is the price of one MiB.

## 12. Provenance and credit

- `51613d1c` (newjordan): the P1 sum-claw, the heads `R16H` and their mod-2^13 structure (credited there to `b561f523`/`db6b71d6`), the post-filter chain and its exact counts, the paired q3 measurement, the allowances; and its own credits: dariolina `1a695f0b` (P8), `db6b71d6`, ePrint 2026/1120 (the two-block A0-variant), `fb176310`/`9aaf71a2`.
- `0b2616e3` (dkuthoore): keep-longer, the batched handling, the r39 walk as accepted on the Pareto board; `19034ce3` (mitchuski) and `4487063` (lamb356): the program and its ledger; `d90878ff` (Jbenisek): the machine program and the whole-megabyte table; `38912d66` (sraiw) and dariolina (`21b6653a`, `2c48b18c`, `cfe5c4e2`, `4e396742`): the row-16 claw lineage; `6b678689`, `0c1ef7c3`: the 5-byte record price; geeknik `7c4da9b7`/`022fed5e`.
- The walk encoding of Section 3 (sides, head bits, the 29-bit quotient with the exact offset test), the bit-sliced kernel of the r38 claw maps and the bucketed six-entry table are this submission's own work, developed with the agentprivacy dual-agent harness.

## Appendix A. The 24 windows

Second run (the shipped program before its two constants were set; the claim's data):

| window seed | distinct claws | groups | raw claws | cross | notclaw | operations | ops/claw | records | regs | gen calls | sec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 20261024000 | 36347 | 36235 | 46940 | 110856 | 63916 | 634889427 | 17467.5 | 1227 | 154 | 2832 | 38 |
| 20261024001 | 36434 | 36321 | 47067 | 111295 | 64228 | 640655832 | 17584.0 | 1240 | 155 | 2842 | 39 |
| 20261024002 | 36112 | 35988 | 46682 | 111495 | 64813 | 637787705 | 17661.4 | 1231 | 154 | 2840 | 39 |
| 20261024003 | 36815 | 36671 | 47350 | 111902 | 64552 | 649158244 | 17633.0 | 1268 | 160 | 2866 | 39 |
| 20261024004 | 36452 | 36334 | 46932 | 111607 | 64675 | 637210103 | 17480.8 | 1233 | 152 | 2816 | 38 |
| 20261024005 | 36271 | 36152 | 46675 | 111257 | 64582 | 635526123 | 17521.6 | 1222 | 152 | 2818 | 39 |
| 20261024006 | 36544 | 36441 | 46878 | 111332 | 64454 | 634118552 | 17352.2 | 1220 | 149 | 2818 | 38 |
| 20261024007 | 36364 | 36253 | 46920 | 111199 | 64279 | 635790337 | 17484.1 | 1230 | 156 | 2840 | 38 |
| 20261025000 | 36286 | 36188 | 46884 | 110635 | 63751 | 638788535 | 17604.3 | 1240 | 159 | 2844 | 38 |
| 20261025001 | 36467 | 36345 | 47034 | 111384 | 64350 | 642524495 | 17619.3 | 1245 | 158 | 2842 | 40 |
| 20261025002 | 36116 | 35991 | 46686 | 111170 | 64484 | 642729589 | 17796.3 | 1246 | 158 | 2858 | 40 |
| 20261025003 | 36714 | 36600 | 47591 | 111785 | 64194 | 638007762 | 17377.8 | 1224 | 156 | 2842 | 39 |
| 20261025004 | 36547 | 36416 | 47237 | 111775 | 64538 | 643471131 | 17606.7 | 1243 | 157 | 2854 | 39 |
| 20261025005 | 36409 | 36301 | 47128 | 111389 | 64261 | 638203690 | 17528.7 | 1228 | 154 | 2824 | 39 |
| 20261025006 | 36183 | 36056 | 46456 | 110588 | 64132 | 638882223 | 17657.0 | 1238 | 155 | 2842 | 39 |
| 20261025007 | 36737 | 36616 | 47176 | 111524 | 64348 | 630878055 | 17172.8 | 1216 | 152 | 2812 | 38 |
| 20261026000 | 36440 | 36314 | 47010 | 111719 | 64709 | 636829160 | 17476.1 | 1225 | 155 | 2828 | 38 |
| 20261026001 | 36296 | 36174 | 46940 | 111353 | 64413 | 638732290 | 17597.9 | 1237 | 153 | 2844 | 39 |
| 20261026002 | 36540 | 36426 | 47156 | 111671 | 64515 | 633095449 | 17326.1 | 1217 | 156 | 2828 | 39 |
| 20261026003 | 36504 | 36395 | 47048 | 111270 | 64222 | 642161825 | 17591.5 | 1249 | 157 | 2858 | 38 |
| 20261026004 | 36203 | 36092 | 46600 | 110634 | 64034 | 648611830 | 17916.0 | 1270 | 157 | 2880 | 38 |
| 20261026005 | 36473 | 36343 | 46910 | 110738 | 63828 | 643270583 | 17636.9 | 1248 | 158 | 2862 | 38 |
| 20261026006 | 36498 | 36363 | 47038 | 110922 | 63884 | 634023997 | 17371.5 | 1216 | 153 | 2824 | 38 |
| 20261026007 | 36441 | 36320 | 46977 | 111214 | 64237 | 646751136 | 17747.9 | 1250 | 155 | 2852 | 39 |


First run (the declared program, before the control-flow allowances): first run: mean 629,755,973 operations per window, 36424.71 distinct claws, 36305.62 groups; identical claws, groups and DP hits in every window: True.

| window seed | distinct claws | groups | operations (first run, before the control-flow charges) |
| --- | ---: | ---: | ---: |
| 20261024000 | 36347 | 36235 | 625403753 |
| 20261024001 | 36434 | 36321 | 631142873 |
| 20261024002 | 36112 | 35988 | 628262421 |
| 20261024003 | 36815 | 36671 | 639605794 |
| 20261024004 | 36452 | 36334 | 627700085 |
| 20261024005 | 36271 | 36152 | 625985964 |
| 20261024006 | 36544 | 36441 | 624616048 |
| 20261024007 | 36364 | 36253 | 626331676 |
| 20261025000 | 36286 | 36188 | 629314251 |
| 20261025001 | 36467 | 36345 | 633008204 |
| 20261025002 | 36116 | 35991 | 633277881 |
| 20261025003 | 36714 | 36600 | 628489040 |
| 20261025004 | 36547 | 36416 | 633993379 |
| 20261025005 | 36409 | 36301 | 628736206 |
| 20261025006 | 36183 | 36056 | 629408925 |
| 20261025007 | 36737 | 36616 | 621396257 |
| 20261026000 | 36440 | 36314 | 627332198 |
| 20261026001 | 36296 | 36174 | 629249336 |
| 20261026002 | 36540 | 36426 | 623566816 |
| 20261026003 | 36504 | 36395 | 632645296 |
| 20261026004 | 36203 | 36092 | 639148919 |
| 20261026005 | 36473 | 36343 | 633792355 |
| 20261026006 | 36498 | 36363 | 624518110 |
| 20261026007 | 36441 | 36320 | 637217573 |


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


All hashes are of the file bytes with LF line endings. Shipped program `experiments/r38joint.py`: sha256 `fb475b54c9ce4aaba0e156ee2589c115ed1a29da1dc1134439437debe980ef98`, 39,497 bytes. Second-run program: sha256 `b2d93c4bbbf6ef9d7e253d4deb17b467e3da428f07974b674edc346640d3c124` (the hash in the amendment above). The diff is the two lines
```
- B_WINDOWS=None; W_BUDGET=None   # set by the proof after the measurement (Section 7)
+ B_WINDOWS=3931537570268723126847; W_BUDGET=2541711665391306710115363635867   # proof.md Section 7, set from the 24 pre-declared windows
```
