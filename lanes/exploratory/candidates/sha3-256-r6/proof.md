# SHA3-256 round 6: row-pair embedding, affine round-0/round-1 front and compact checkpoint search

## 1. Claim and resources

This package prices an ordinary distinguished-point birthday search for two distinct 128-byte one-block messages with the same `sha3-256-r6-prefix-v1` digest. It claims no weakness in full SHA3-256 and no reduction in the number of digest evaluations: it is the generic parallel collision search of van Oorschot and Wiener over a fixed injective message family, with a cheaper exact bit-sliced evaluation of the 6-round digest. Under the single score-critical premise H1 in Section 6, one bounded attempt succeeds with probability at least 0.39.

The exact ledger has N = 33797633225719388998745785472209513824203 word operations. One target compression costs C = 1626, so `log2(N/C) = 123.96693447468814163389365490924481577883485936618855671176356093771089791987983618582984260271022669059274892817288695107414705062485335516083693301353214361237157979804079661932995760548115569245375372615560184843296808127712766117343128158395940228235323824` and the upward-rounded claim is **123.96694**. Peak memory is 1012019 bytes, below 2^20, so `memory_log2_bytes = 20` and the scalar memory term is zero. Preprocessing is 1153085472499881472 word operations (an explicit upper bound, Section 5), i.e. 2^49.33309 target compressions, declared upward as `preprocessing_log2 = 50`. There is no nonuniform advice. Every `*_log2` field in claim.json uses the target-compression unit.

This package is a credited derivative of this account's package `221b1d6d` (25374 straight-line operations, claim 123.96734) and, through it, of `a739029e` (25380 straight-line operations, claim 123.96768), `6a4df23e` (25385 straight-line operations, claim 123.96796), `f911a9de` (Jbenisek; 25390 straight-line operations, claim 123.96824) and the row-pair package `d2be26f2` (mpjunior92; 25439 straight-line operations, claim 123.97101). It keeps that package's embedding rule, D0 target, row-1/lane-15/row-2 constant rule, emitters, search controller, table, distinguished-point rule, batch bound Tb, trail capacity U, replay procedure and whole success certificate (the controller bytes and hash are identical; constants live in the data image). Relative to `a739029e`, six changes lower the cost. First, the free row-0 lane constants K_0..K_4 are planned by a different pass-1 run (`np_plank`, seed 34): its chosen bit vector is another point of the same bounded search, it changes the lane constants and therefore the whole embedding, and the entire chain is re-derived in that embedding by the package's unchanged tools. That chain reaches model value 12766 after pass 1, 10609 after pass 2, 12762 after the joint ILS, 12762 after the pair polish and 12759 after the pass-5 two-column joint local search. Second, five further plateau-drift passes (`np_ils6`, seeds 7001, 7002, 7006, 8002 and 8007) reach model values 12758, 12755, 12753, 12753 and 12752; in this embedding the last four emit at 25377, 25374, 25373 and 25371 operations. Third, a second joint iterated local search (`np_ils2`, seed 57, 6000 iterations, kick bound 3) starts from the pass-10 plan at model value 12752 and reaches another 12752 state whose emission is 25370 operations. Fourth, a further equal-cost drift (`np_ils6`, seed 8105, 108 iterations, kick bound 10) from the pass-10 plan reaches a 12752 state whose emission is 25369 operations. Fifth, two longer drifts with the same kick-and-repair search (`np_ils7`, Appendix B, the record variant that also writes every accepted state) reach lower model values and a cheaper emission: seed 9206 over 6000 iterations with kick bound 10 from the pass-12 plan reaches a 12751 state, plan `c179ec0c9593d0d7a4ea7d67326cafbcc2f4c1290f568caf4496f7cda5b83044`; seed 9406 over 4000 iterations with kick bound 31 from that plan drifts through 12750 states and its accepted state at iteration 3273 emits at 25368 operations. Sixth, a further long drift (`np_ils7`, Appendix B) starting from the pass-14 run's accepted state at iteration 3301 (plan `75eb45ab0d3871c3fd7bf27d5a7336d766b413aaf56af8b610d99bd3f8d5e920`), seed 9712 over 1000 iterations with kick bound 31, reaches a cheaper emission: its accepted state at iteration 20 emits at 25367 operations, which is selected. The straight line now has 25367 operations, BSTEP falls to 25386 and the claim falls to 123.96694.

## 2. Target and chain function

Write the 256-bit point as four little-endian 64-bit lanes u0..u3 and define the pivot lane

`P(u) = rotl(u0,28) xor rotl(u1,35) xor rotl(u2,4) xor rotl(u3,50)`  (64-bit left rotations).

The one-block message m(u) has 16 lanes in standard Keccak lane order (lane index x+5y). Lanes 0..3 are `K_x xor u_x`, lane 4 is `K_4 xor P(u)`, lanes 10..13 are `K_(10+x) xor u_x`, lane 14 is `K_14 xor P(u)`, and lanes 5..9 and 15 are the constants K_5..K_9, K_15. SHA3 padding of a 128-byte message gives absorbed lane 16 = `8000000000000006`; lanes 17..24 are the zero capacity. The map u -> m(u) is injective because lanes 0..3 return u. Define `g(u) = SHA3-256-r6(m(u)) xor PD`. Equal values of g at different points are equal digests of different messages because the common constant PD cancels.

The 25 absorbed lane constants (lanes 16..24 are padding and capacity) are:

`e1b7df8ea4d2e657 eed9b2d94e1b97ee 2ecd28a7bf211bae bc9cf607fc15efdb 2c5f06084c30b5ab fffffffffffffffe 7ffffffffffffff9 ffffffffffffffff ffffffffffffffff ffffffffffffffff d3db44a86d608acc 276bde4268d22582 08049acb2407d21f 27ba3fb5908ec912 40c420c1fe5c2e8c 0000000000000001 8000000000000006 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000`

PD is `9f93d39fe94a1d82 42d22cc4d0a640e4 606c2c6096b5e27c 202c00200611a218`; it is the polarity of the emitted digest planes, and both normative emitters derive it again and reject a mismatch.

### 2.1 Why rounds 0 and 1 are cheap

The linear part of the message lives only in rows y=0 and y=2, with lane (x,2) equal to lane (x,0) up to a constant. Write `L_x` for the linear part of lane (x,0) (so `L_4 = P`).

1. **Round-0 theta is constant.** Every column x contains the two variable lanes (x,0) and (x,2) with identical linear parts, so every column parity is constant and theta adds only constants.
2. **Round-0 chi is affine.** pi moves lane (x,y) to row 2x+3y, position y. Lane (x,0) therefore lands at position 0 of row 2x and lane (x,2) at position 2 of row 2x+1 (mod 5). Every chi row has non-constant inputs only at positions 0 and 2. chi multiplies only the pairs of positions (X+1, X+2), and {0,2} is not such a pair, so every round-0 chi output is an affine function of u.
3. **Constants.** Row-1 lanes are set so that position 1 of every round-0 chi row is the constant 0; then output position 0 is `a0 xor a2` and output position 4 is constant. Positions 3 and 4 come from lane 15, the padding lane and the capacity, shifted by the round-0 theta effect D0 of the constants. The row-0 constants K_0..K_4 are free in this rule (lane 10+x then follows from K_x); this package fixes them by the planned row-0 polarity of Section 3. The other constants are solved (Appendix B, `np_consts.c`) so that `D0 = (~1, ~PAD, ~0, ~0, ~0)`; this target has even total parity, as every theta effect must. It makes every position-3 input equal to one and every position-4 input equal to one except at four (row, bit) positions (one bit of row 2 and the three set bits of PAD in row 4). Output position 1 is then a complemented copy of position 2, output position 2 equals position 2, output position 4 is constant, and output position 3 is constant except at those four positions, where it is a complemented copy of position 0 (`1 xor a0`).
4. **Round-1 theta is half constant.** The round-1 column parity of column 2 is `C1[2](w) = xor_x L_x[w - r(x,2)]` plus a constant, with rotation offsets r(x,2) = 3, 10, 43, 25, 39. The pivot lane `L_4 = P` is exactly the solution of `C1[2] = const` (it sets `L_4[z] = xor_(x<4) L_x[z + 39 - r(x,2)]`), so C1[2] is constant, and C1[1] (the complemented copies) is constant as well. Column 0 carries `a0 xor a2` and its parity C1[0] is non-constant. Column 3 has non-constant parity only at the four exceptional bits. Consequently the round-1 theta effects D1[0] and D1[3] are constant, D1[2] is constant except at those few bits, D1[1] = C1[0] and D1[4] = C1[3] xor rotl(C1[0],1) are non-constant, and after round-1 theta column 3 is constant except at four bits. pi maps column 3 to one position of every round-1 chi row, so almost every round-1 row has a constant input and needs at most three AND/OR gates instead of five. The four exceptional bits fall in four distinct rows (row 2 bit 43 and row 3 bits 57, 59, 60 of the round-1 chi layer), which keep five gates: `316*3 + 4*5 = 968`.

The emitted round-0/round-1 segment has 968 AND/OR gates (a 39.5% cut, not a halving) (the six-lane incumbent has 1600) and 3258 operations in total (d2be26f2: 3293). These structural statements are explanatory only: the emitter tracks every affine form exactly (Section 3), and the executed checks of Section 7 compare the emitted program bit for bit with scalar SHA3-256-r6 of m(u).

## 3. Bit-sliced register step

One 256-bit register word carries one bit plane for 256 walks. Inputs are the 256 planes of u in registers 0..255; outputs are the 256 digest planes in the same registers.

**Front segment (rounds 0 and 1).** The emitter starts from 256 affine input planes and builds the 64 pivot planes as three XORs each. Every value is a pair (node, polarity); an XOR of two affine nodes is first looked up by its exact 256-bit linear form, so identical forms are shared and constant results fold away. A complemented copy costs nothing because only the polarity bit changes. In the final emission the complement of an already complemented node returns the node itself, so no redundant double NOT is emitted; record and kmap modes disable this fold and keep the measured tables, masks and plans identical to their pre-canonicalization values. Round-0 chi uses the generic exact row builder (`_row_choice`): every round-0 row is affine and costs only the XORs its linear terms need.

**Chained-chi rows and the polarity plan.** Rounds 1 to 4 build every row whose five inputs are distinct non-constant nodes with the exhaustively verified 1024-entry chained-chi table (checksum c8fa4bd9170966dc): for an input polarity pattern p and a chosen output polarity target t it gives the cheapest complement subset, chaining order and mixed-term selection, with 10 to 15 operations. Round-1 rows with exactly one constant input (316 of the 320 rows, Section 2.1) are built from a second exhaustive table: for each of the 160 row types (constant position, constant value, polarities of the four variable inputs) and each of the 32 output-polarity targets, the cheapest chained-row decision (complement subset, chaining order, mixed-term selection), found by emitting all 15872 decisions of each type on a scratch graph and counting live operations (np_emit record mode; ties broken as in the chained table). The plan stores the chosen decision of each such row explicitly (line `D 1`), so the Python emitter needs no table. Round 0 and any remaining row use the generic exact row builder. The plan also fixes the target t of every full row in rounds 1..4 and optional complement bits on the theta column parities (CN) and theta effects (DN) of rounds 2..5. **Planned row-0 polarity (new here).** Every value before round-1 chi is affine in u, and the row-0 constants enter only through the constant (polarity) parts: flipping bit z of K_x (with lane 10+x following) flips a fixed set of round-1 chi-input polarities, i.e. XORs a fixed mask into the pattern or one-constant row type of about 40 round-1 rows, and changes nothing else in the graph. The bounded phase `np_emit kmap` (Appendix B) records these 320 masks by rebuilding rounds 0-1 once per bit; the planner `np_plank.c` (the d2be26f2 planner plus one move kind) adds a move that applies one mask, priced exactly by the round-1 table costs at the current targets, in every stage that moves round-1 targets and in the final coordinate descent, and prints the chosen bit vector (line `KX`). `np_consts` then applies those bits to the incumbent K_0..K_4 and derives the other constants by the unchanged rule. Pass 1: `np_plank` seed 34, next-round weight 6/16, T0 = 2, 90000000 moves per stage (final printed value 12766). Pass 2 (unchanged `np_plan`, round 1 fixed at the recorded polarities): seed 19, 200000000 moves per stage over rounds 2..5 (final printed value 10609). Pass 3 is a joint iterated local search (`np_ils2`, Appendix B) over the round-1 targets and the pass-2 model: from the pass-2 plan it repeatedly applies one random kick (a target change in rounds 1..4, a CN or DN flip, or a five-row kick on one z-slice), runs a full coordinate descent over the 320 round-1 targets, the round 2..4 targets and all CN/DN bits, and accepts a non-increasing result, for 6000 iterations at seed 51 and kick bound 3 (start and final printed model value 12762). Pass 4 is an exhaustive same-round target-pair polish (`np_pair`, Appendix B): from the pass-3 plan it tries every joint change of two round-1 rows to any of their 32 target values (all six ordered pairs of the four full rows) and repeats after a full coordinate descent (final printed model value 12762). Pass 5 is a seeded kick-and-repair search (`np_ils4`, Appendix B): each iteration applies one random kick (a target change in rounds 1..4, a CN or DN flip, a five-row column kick or an XOR target change) and repairs exactly the two output columns touched by it with the exact two-column joint window optimizer, which minimizes over the targets, CN and DN of an adjacent column pair jointly with the costs of every consuming row whose pattern touches the window columns; only strict improvements are accepted, the best plan is kept, and the seed is fixed (xorshift, seed 4001, 75 iterations, kick bound 10, start 12762, final printed model value 12759). Pass 6 (`np_ils6`, Appendix B) is the same kick-and-repair search with the repaired window widened from ±2 to ±3 and equal-cost moves accepted: from the pass-5 plan, seed 7001 over 500 iterations drifts along equal-cost states from model value 12759 to 12758 (start 12759, final printed model value 12758). Pass 7 (`np_ils6`, Appendix B) starts from the pass-6 plan with seed 7002 over 500 iterations: it drifts along equal-cost states from model value 12758 and reaches model value 12755 (start 12758, final printed model value 12755); in this embedding that plan emits at 25377 operations. Pass 8 (`np_ils6`, Appendix B) starts from the pass-7 plan with seed 7006 over 500 iterations: it drifts along equal-cost states from model value 12755 and reaches model value 12753 (start 12755, final printed model value 12753). Pass 9 (`np_ils6`, Appendix B) starts from the pass-8 plan with seed 8002 over 500 iterations: it drifts along equal-cost states from model value 12753 to another 12753 state, plan `c0b99119e295962e489db2db76fb8c1fc76c37a1c56a569ee48e165399836570` (start 12753, final printed model value 12753), which emits at 25373 operations. Pass 10 (`np_ils6`, Appendix B) starts from the pass-9 plan with seed 8007 over 500 iterations: it drifts from model value 12753 to model value 12752, plan `f03f82e1c62afb6c39b1a54fded635ecfd1b2266ca508fa5ae849eb577e66118` (start 12753, final printed model value 12752), which emits at 25371 operations. Pass 11 (`np_ils2`, Appendix B) is a second joint iterated local search: from the pass-10 plan, seed 57 over 6000 iterations with kick bound 3, it repeatedly applies one random kick, runs a full coordinate descent over the 320 round-1 targets, the round 2..4 targets and all CN/DN bits, and accepts a non-increasing result, reaching another model-value-12752 state, plan `8b050381bb8e5079cc89ab825463a7901f5ded95b432ce97988fdcf2cf873088` (start 12752, final printed model value 12752), which emits at 25370 operations. Pass 12 (`np_ils6`, Appendix B) is a further equal-cost drift from the pass-10 plan: seed 8105 over 108 iterations with kick bound 10 starts from model value 12752 and reaches another 12752 state, plan `5d4a5898b423c2099f84be358f5493429323ba8152f4a0333bb25a0527bf68b5` (start 12752, final printed model value 12752), which emits at 25369 operations. Pass 13 (`np_ils7`, Appendix B) is a longer plateau drift in the same embedding: seed 9206 over 6000 iterations with kick bound 10 starts from the pass-12 plan (model value 12752) and reaches a 12751 state, plan `c179ec0c9593d0d7a4ea7d67326cafbcc2f4c1290f568caf4496f7cda5b83044` (start 12752, final printed model value 12751), which emits at 25372 operations. Pass 14 (`np_ils7`, Appendix B) starts from that 12751 plan with seed 9406 over 4000 iterations and kick bound 31: it drifts through lower model values (final printed model value 12750), writing every accepted state to a dump directory; its accepted state at iteration 3273, plan `0b114a32ed91c9129207a51b227e14660f1f80af3b867773284a141c544c6ae3` (start 12751), emits at 25368 operations. Pass 15 (`np_ils7`, Appendix B) starts from the pass-14 run's accepted state at iteration 3301, plan `75eb45ab0d3871c3fd7bf27d5a7336d766b413aaf56af8b610d99bd3f8d5e920` (start 12750) with seed 9712 over 1000 iterations and kick bound 31: it drifts through lower model values (final printed model value 12750), writing every accepted state to a dump directory; its accepted state at iteration 20, plan `c06833ea87f90cba1cbec2ec91f30f9fd35d7ed701cbef089a3cfc0369c1bdfd` (start 12750), emits at 25367 operations and is selected. The model prices the 320 round-1 rows, the full rows of rounds 2..4, the 64 last-round rows and the CN/DN NOTs. Both normative emitters re-emit the selected plan at 25367 operations: the round-0/1 segment is 3259 and rounds 2..5 are 6556, 6579, 6538 and 2435. The model value alone does not fix the emission: the pass-7, pass-8, pass-9, pass-10, pass-11, pass-12, pass-13, pass-14 and pass-15 plans have model values 12755, 12753, 12753, 12752, 12752, 12752, 12751, 12750 and 12750 while their realized counts are 25377, 25374, 25373, 25371, 25370, 25369, 25372, 25368 and 25367 (the pass-14 run's final state realizes 25371, its iteration-3273 state 25368; the pass-15 run's final state realizes 25370); the cheapest emission is selected. The `NOT (NOT x)` canonicalization is active in emission mode only, so every recorded table, mask and plan is the pre-canonicalization artifact, and the search never underestimates the realized count. The plan text is in Appendix D, SHA-256 `c06833ea87f90cba1cbec2ec91f30f9fd35d7ed701cbef089a3cfc0369c1bdfd`.

**Last round.** Only the four digest lanes of row 0 are formed.

| segment | XOR | AND | OR | NOT | total |
|---|---:|---:|---:|---:|---:|
| rounds 0-1 (front) | 2112 | 502 | 466 | 179 | 3259 |
| round 2 | 4811 | 810 | 790 | 145 | 6556 |
| round 3 | 4820 | 832 | 768 | 159 | 6579 |
| round 4 | 4807 | 831 | 769 | 131 | 6538 |
| round 5 (four digest lanes) | 2176 | 144 | 112 | 3 | 2435 |
| **straight line** | 18726 | 3119 | 2905 | 617 | **25367** |

The emitted straight-line register program has 25367 operations. Lowest-free last-use allocation names registers 0..1925 (peak 1926). It contains 309 14-bit, 16297 25-bit and 8761 36-bit encoded records, 16298 with destination equal to the first operand. Its stored size is 90894 bytes and SHA-256 is `879dbcc6d6c7bddd7db69e2039a0faf8cdb867234d64b234107b94aa41b81340`.

### 3.1 Registers and code encoding (machine conventions H_reg and H_code)

These conventions are unchanged from the incumbent package; only the measured numbers differ.

**Registers.** Input and digest plane j use register j. Each other value receives the lowest free register allowed by its last use. Values in registers above 255 are dead between steps and may be reused by handlers. The straight line uses registers 0 through 1925; persistent search state begins at register 1932 (as in d2be26f2). The declared file has 1943 words, or 62176 bytes, all included in Section 5.

**H_reg (declared machine convention, role supporting in claim.json).** The cost model and target profile fix no register count. This package uses the 256-bit word RAM of collision-frontier-v5 with the declared register file above. An operation on register operands costs one word operation, with no load or store. Every load and store in the assembled other code is an explicit charged word operation. H_reg affects the time and memory ledgers, not the success bound.

**Sensitivity of H_reg (quantified).** Every emitted straight-line and prefilter record reads at most two register operands and writes one. Every non-PERM controller word has at most two semantic register reads and one write; PERM reads and rewrites seven packed state words, 14 accesses, below 3C. Charging each register access as a separate load or store makes every ordinary instruction cost at most 4 word operations and every PERM at most 4C. Applying the same factor to preprocessing gives `N_RAM <= 4N`, hence `time_log2_RAM <= 125.96693447468814163389365490924481577883485936618855671176356093771089791987983618582984260271022669059274892817288695107414705062485335516083693301353214361237157979804079661932995760548115569245375372615560184843296808127712766117343128158395940228235323824`, exactly 2 above the claimed model, with memory unchanged.

**H_code (declared code-memory charging convention, role supporting in claim.json).** Each straight-line instruction has register operands only. Bits 0..1 give XOR, AND, OR or NOT and bit 2 flags destination equal to the first operand. With that flag, NOT carries one 11-bit register and a binary operation carries two; without it, NOT carries destination and source while a binary operation carries destination and two sources. Commutative operations swap operands when the destination equals the second. Records are packed without padding in a little-endian bit stream: 90894 bytes. The separate prefilter is a 15-OR chain from digest planes 240..255 into register 1936 (49 bytes, SHA-256 `88ad15d4b5a89d38385fdb42179b15636e53cafe9cc5ed670c5a56b5bb849543`). The other code (setup, loop control, handlers, restart, replay and output) is 1016 fixed 8-byte instruction words followed by 12 32-byte literal words, 8512 bytes, SHA-256 `c656b0c5f89238d20788f98274790cf0f755a6ff7ce11addd55bb08ec762fb5e`. A word has a 5-bit opcode, one literal flag, three 11-bit register fields and a 25-bit immediate or literal index. Each assembled operation is charged as the word operation it performs, except PERM at C.

## 4. Search, table, and controller

The search is the incumbent's compact checkpoint search, byte for byte except the two scalar message-formation routines. The attempt starts 256 walks from `rho + trail_number`. It advances all walks through the step, applies the 15-OR prefilter, and handles exact distinguished points with probability `712 * 2^-121`. The table has 18600 256-bit words and 93000 slots; each word has five 51-bit slots (written bit and 50 endpoint bits) and the word and slot position encode the trail number. The 256 live walks use one packed word apiece: low 128 bits are the start step and high 128 bits are the positional trail number.

On a prefilter hit the 125-operation hit handler forms the exact distinguished-point mask and continues the batch loop when it is zero. Only when it is nonzero do 256 stores copy the carried planes to a scratch matrix, charged indexed loops gather or replace one lane per distinguished point, and 256 fixed loads restore the planes; that cost is part of the 2893-operation per-DP handler. A matching endpoint starts the final replay. Replay measures the stored trail while keeping every `G = ceil(LRC/(S-1)) = 2107889139913890569390211303440`-th point in the now-free table, advances the other trail to alignment, locates the merge segment by checkpoints, then lock-steps only that segment.

**Scalar evaluation.** Replay evaluates g with the scalar routine `eval_f`: seven loads of the constant state words, then `state0 ^= u` (lanes 0..3), extraction of u0..u3 (six operations), the pivot `P` by four rotations of three operations each, three XORs and one 64-bit mask, `state1 ^= P` (lane 4), `state2 ^= u << 128` (lanes 10, 11), `state3 ^= u >> 128` (lanes 12, 13) and `state3 ^= P << 128` (lane 14), then PERM, a load of PD and one XOR. Its charged cost is `e = C + 40 = 1666` (the incumbent's six-lane routine cost C + 29). `output_message` is the same message formation plus a return (38 operations).

With `e = 1666`, at most one replay costs `(2e+17)LRC + (3e+20)G + 17*nck + e + 93 = 131306883637006639297473720649711215510` operations, where LRC = 39204630113258450700088540032663552 and nck = S-1 = 18599.

The controller permits at most HMAX = 44384159803516906822519431956004865 prefilter hits and aborts on hit 44384159803516906822519431956004866; that abort value is a checked controller literal and the input to F5 below. Setup initializes `remaining = Tb = 1325958336173754933667940744388673536`. Every continuation path executes `remaining -= 1`, branches to the step only while the result is nonzero, and otherwise reaches HALT. The exact-byte experiment starts `remaining` at three, supplies only no-DP prefilter results, requires exactly two back-edges, and then requires the charged-limit HALT.

## 5. Exact operation and memory ledgers

`BSTEP = 25367 + 15 + 2 + 2 = 25386`: the straight line, the prefilter ORs, its compare and branch, and the count-down subtract and conditional back-edge.

| term | word operations |
|---|---:|
| main work `Tb * BSTEP` | 33660778322106942746094343737050866384896 |
| one replay (Section 4) | 131306883637006639297473720649711215510 |
| hit, DP, probe, restart, setup, cap and final-halt paths | 5548019975439613352814929036436342325 |
| preprocessing (upper bound, below) | 1153085472499881472 |
| **N** | **33797633225719388998745785472209513824203** |

The path term is the incumbent's carried bound for these paths, `5548019975439613352814929036434245173`, plus an explicit allowance of `2^21`. The carried bound decomposes as `125*HIT_ABORT + 92744*(2893 + 2835 + 24*18600) + 1477691`: at most HIT_ABORT = 44384159803516906822519431956004866 hits at 125 operations each (the hit handler), at most U-256 = 92744 handled distinguished points each charged the per-DP handler (2893: save, lowest-set-bit isolation and clear from charged primitive operations, gather, record, insert, restore), one restart (2835) and a full linear probe of all 18600 table words (24 operations per word), and a remainder of 1477691 covering setup (750162) and the final match, halt and output paths. All of these paths are byte-identical to the incumbent's controller; the only one that touches message formation is the final output, which calls `output_message` twice and therefore costs 22 more operations than before, far below the allowance.

**Preprocessing.** The attack's construction consists exactly of the bounded freestanding C phases of Appendix B, run alone and sequentially under an address-space cap of 1048576 bytes; their inputs are the closed-form rules of Section 2.1 (the D0 target, the incumbent row-0 constants) and their own outputs. Their measured running time is 14305.94 s in total, essentially all of it the fifteen search passes (the two planner passes, the two ILS passes, the pair polish, the two-column joint local search, the five plateau-drift searches, the narrow drift stop and the three long drift searches). The same 2^60 charge also covers this package's design-time seed selection: multi-seed campaigns in the search passes (the pass-1 and pass-2 seeds, the pass-3 campaign, the pass-5 seeds, the pass-11 seed, the pass-6, pass-7, pass-8, pass-9, pass-10 and pass-12 equal-cost-state harvests and the pass-13, pass-14 and pass-15 drifts with their harvested states) and refinement drifts from the selected plan; the pass-4 polish is exhaustive and seedless; under 2^20 s of CPU time in all. The ledger charges `2^60` word operations for these phases: a deliberately generous bound (a 2^36 operations-per-second rate would need more than 2^24 seconds). Design-time experiments that led to choosing the embedding rule are analysis, not phases of the attack: none of their outputs is an input to it, since the constants follow from the stated rule via `np_consts` and the plan from `np_plan`, the pass-3 ILS, the pass-4 pair polish, the pass-5 joint search, the pass-6, pass-7, pass-8, pass-9 and pass-10 plateau-drift searches, the pass-11 second ILS, the pass-12 narrow drift, the pass-13, pass-14 and pass-15 longer drifts and the emission rule. The dumping walks inspect equal-cost states, but their dumps are not inputs: the selected plan is the pass-15 output, re-derived from the recorded pass-10 plan by passes 12, 13, 14 and 15; the harvest walks also fixed the pass-12, pass-13, pass-14 and pass-15 iteration budgets at design time. The ledger also keeps the incumbent's inherited campaign charge `163967893034496`, which covers the construction of the chained-chi table and the controller design used here (that campaign ran under the same 1 MiB cap). Total `1153085472499881472` word operations, `log2(prep/C) = 49.333094`, declared as `preprocessing_log2 = 50`. This bound changes N only in its twenty-third significant digit.

**Search memory.**

| region | bytes |
|---|---:|
| data image | 512 |
| online stack | 0 |
| other code and literal pool (H_code) | 8512 |
| packed walk words | 8192 |
| prefilter (H_code) | 49 |
| register file | 62176 |
| replay checkpoints (alias table) | 0 |
| step program (H_code) | 90894 |
| table | 595200 |
| transpose scratch | 8192 |
| **search total** | **773727** |

The online controller uses link registers and zero stack. Replay checkpoints alias the table after a match, when the ordinary endpoint table is no longer needed.

**Construction memory.** Each phase ran as its own process from the construction directory of Appendix C, and every phase except the pass-13 and pass-14 drifts was launched under `prlimit --as=1048576 --stack=131072` and timed with `/usr/bin/time -v`; the two long drifts ran concurrently as part of a six-way burst without a wrapper (the pass-15 drift ran inside the same burst but under the wrapper, so its wall time also includes contention), so their recorded wall time is the difference between the driver's start and final-write timestamps, includes contention and has no `wrapper_maxrss_bytes`. The charged peak is `max(VmHWM, image + stack reserve) + retained input/output bytes`, with VmHWM read by every program itself from `/proc/self/status` at exit; the long drifts report 675840, 684032 and 684032 bytes, and their image plus stack reserve (946607 bytes) is below the `prlimit` cap. Appendix C also lists `wrapper_maxrss_bytes` where recorded, the peak of the measuring wrapper (`/usr/bin/time` around `prlimit`, before `exec`); it is outside the charged process and is not part of the attack. The pass-3 ILS reads `plan2.txt` and writes `plan3.txt` (SHA-256 `7c3ea42cc24ae1698a25d672ff818c9848d852241eabd71147d04e449e7260c6`); the pass-4 pair polish reads `plan3.txt` and writes `plan4.txt` (SHA-256 `7c3ea42cc24ae1698a25d672ff818c9848d852241eabd71147d04e449e7260c6`); the pass-5 joint local search reads `plan4.txt` and writes `plan5.txt` (SHA-256 `0ac906c912451ecbd85244feeb18ed2769d667dfa0644025dcd0082c1670103b`); the pass-6, pass-7, pass-8, pass-9 and pass-10 plateau-drift searches read `plan5.txt`, `drift7001.txt`, `drift7002.txt`, `drift7006.txt` and `drift8002.txt` and write `drift7001.txt`, `drift7002.txt`, `drift7006.txt`, `drift8002.txt` and `drift8007.txt` (SHA-256 `5c855ef2fb1bbbe1870c5fde7991c9f867b65e6751ecb183dd7c4ee129ecb866`, `c2447ca36a437dc5136f29d9f5991d5b475e3c92f55e4948bf0aedd66b7e8c60`, `3394c9007d1e267b5a1ff0961847380dbfbbad5d6c80198812d5d1cc60f18e63`, `c0b99119e295962e489db2db76fb8c1fc76c37a1c56a569ee48e165399836570`, `f03f82e1c62afb6c39b1a54fded635ecfd1b2266ca508fa5ae849eb577e66118`); the pass-11 second ILS reads `pi2.txt` and `drift8007.txt` and writes `drift0057.txt` (SHA-256 `8b050381bb8e5079cc89ab825463a7901f5ded95b432ce97988fdcf2cf873088`); the pass-12 narrow drift reads `pi2.txt` and `drift8007.txt` and writes `drift8105.txt` (SHA-256 `5d4a5898b423c2099f84be358f5493429323ba8152f4a0333bb25a0527bf68b5`); the pass-13 long drift reads `pi2.txt` and `drift8105.txt` and writes `drift9206.txt` (SHA-256 `c179ec0c9593d0d7a4ea7d67326cafbcc2f4c1290f568caf4496f7cda5b83044`); the pass-14 long drift reads `pi2.txt` and `drift9206.txt` and writes every accepted state into `dump9406/`, of which the accepted states at iterations 3273 and 3301 are retained as `drift9406.txt` and `drift9406_3301.txt` (SHA-256 `0b114a32ed91c9129207a51b227e14660f1f80af3b867773284a141c544c6ae3` and `75eb45ab0d3871c3fd7bf27d5a7336d766b413aaf56af8b610d99bd3f8d5e920`; the other dump states are transient working data, not inputs to any phase); the pass-15 long drift reads `pi2.txt` and `drift9406_3301.txt` and writes every accepted state into `dump9712/`, of which the accepted state at iteration 20 is retained as `drift9712.txt` (SHA-256 `c06833ea87f90cba1cbec2ec91f30f9fd35d7ed701cbef089a3cfc0369c1bdfd`; the other dump states are transient working data, not inputs to any phase); the step emission then reads the constants with `drift9712.txt` as the plan.

| sequential construction phase | image bytes | stack reserve | measured VmHWM | retained input/output | charged peak | seconds |
|---|---:|---:|---:|---:|---:|---:|
| lane constants (incumbent row-0 rule) | 42871 | 131072 | 49152 | 425 | 174368 | 0.00 |
| round-1 record and one-constant row table | 708007 | 131072 | 401408 | 52129 | 891208 | 0.40 |
| row-0 polarity map | 708007 | 131072 | 335872 | 75602 | 914681 | 0.14 |
| polarity planner with row-0 moves, pass 1 | 690951 | 131072 | 544768 | 131449 | 953472 | 260.32 |
| lane constants (planned row-0 polarity) | 42871 | 131072 | 45056 | 1316 | 175259 | 0.00 |
| round-1 record under the pass-1 plan | 708007 | 131072 | 401408 | 56701 | 895780 | 0.34 |
| polarity planner, pass 2 (rounds 2-5, round 1 fixed) | 321455 | 131072 | 294912 | 60844 | 513371 | 446.62 |
| joint ILS over round-1 targets and the pass-2 plan | 382802 | 131072 | 303104 | 60844 | 574718 | 342.63 |
| exhaustive round-1 target-pair polish | 352637 | 131072 | 270336 | 60844 | 544553 | 33.97 |
| joint two-column local search (pass 5) | 813663 | 131072 | 675840 | 60844 | 1005579 | 32.59 |
| plateau-drift two-column local search (pass 6) | 813887 | 131072 | 675840 | 60844 | 1005803 | 288.39 |
| plateau-drift two-column local search (pass 7) | 813887 | 131072 | 675840 | 60844 | 1005803 | 293.98 |
| plateau-drift two-column local search (pass 8) | 813887 | 131072 | 675840 | 60844 | 1005803 | 284.30 |
| plateau-drift two-column local search (pass 9) | 813887 | 131072 | 679936 | 60844 | 1005803 | 265.48 |
| plateau-drift two-column local search (pass 10) | 813887 | 131072 | 675840 | 60844 | 1005803 | 303.47 |
| second joint ILS over round-1 targets and the pass-10 plan | 382802 | 131072 | 307200 | 60844 | 574718 | 334.19 |
| narrow plateau-drift stop (pass 12) | 813887 | 131072 | 675840 | 60844 | 1005803 | 64.29 |
| long plateau drift (pass 13) | 815535 | 131072 | 675840 | 60844 | 1007451 | 3633.87 |
| long plateau drift (pass 14) | 815535 | 131072 | 684032 | 65412 | 1012019 | 6089.75 |
| long plateau drift (pass 15) | 815535 | 131072 | 684032 | 60844 | 1007451 | 1631.20 |
| step emission | 708007 | 131072 | 663552 | 95887 | 934966 | 0.01 |
| controller and prefilter emission | 30655 | 131072 | 45056 | 8561 | 170288 | 0.00 |

Construction peaks at 1012019 bytes and search at 773727 bytes. The claimed peak is their maximum, **1012019 bytes**, below 2^20.

## 6. Probability space, H1, and success

The real attempt samples one uniform 256-bit rho. Everything afterward is deterministic. H1 is the following single aggregate comparison:

H1 is one premise. Let A_g be this bounded attempt on the fixed deterministic walk g. In the real algorithm's probability space, only the fresh uniform word r is random. Let F be a uniformly random function on 256-bit values, independent of r, and let P_F = Pr_(r,F)[A_F succeeds] for the same attempt with each g evaluation replaced by lazy sampling from F. H1 asserts only the aggregate comparison Pr_r[A_g succeeds] >= P_F. Appendix A proves P_F >= 0.39. The following clauses are properties of comparator F used by that proof, not additional premises about g: outputs at distinct fresh inputs are uniform and independent; its iterates have the random-mapping first-collision law; a fresh output satisfies the exact distinguished-point predicate with its stated probability independently of prior collision bookkeeping; and after any lazy-sampling history, a fresh input maps to any fixed earlier output with probability 2^-256. H1 assigns no per-history conditional probability to deterministic g because the history determines r and hence all later g outputs. The aggregate success comparison is the only heuristic step.

### Lazy-sampling order and first coincidence

Let `M = 2^256`, `L = 256`, `theta = 712 / 2^121`, `q = 1-theta`, and `E = L*Tb`. Comparator F starts undefined. Evaluations are ordered first by batch and then by lane. A fresh input is one not queried earlier in that order; it receives a new independent uniform image and stores it. A repeated input returns its stored image and consumes no new random value. For bookkeeping, attach an independent candidate image `V_t` to every evaluation position and use it exactly when that position's input is fresh. Its DP indicator is Bernoulli(theta), independently across t.

This also proves the restart domination used by F2. A fresh-input DP uses one Bernoulli indicator. A DP returned at a repeated input was already the endpoint of the earlier trail that first exposed it, so the table lookup finds that record and enters replay instead of consuming a new trail number. Thus the number of DP restarts is at most the number of DP indicators among `V_1..V_E`.

Outside the start part of F4, every queried input before the first image coincidence is fresh. If the first m images are distinct, the next fresh uniform image avoids them with probability `1-m/M`. Hence `pi_e = product_(m=0)^(e-1)(1-m/M)` is the exact no-coincidence probability through e fresh evaluations, and the first coincidence is a stopping time with mass `pi_(e-1)*(e-1)/M = pi_(e-1)-pi_e`. In particular `1-pi_e >= B(e) = 1-exp(-e(e-1)/(2M))`, using `1-x <= exp(-x)` term by term. No independence is asserted for the fixed target g.

### Conditional DP-tail lemma

Suppose the first coincidence occurs at evaluation t with earlier partner s. The two trails then follow a common functional-graph path. Let l be the number of further evaluations on that path before its first DP. Without conditioning on firstness, `Pr[l>=j]=q^j`. Firstness reveals that the preceding images were distinct, so the following comparison controls the conditioning rather than assuming independence.

Given the first `m=t-1` DP indicators, with fewer than U ones outside F2, images are uniform within the `theta*M` DP values and the `(1-theta)*M` non-DP values. Comparing their without-replacement products with `pi_m` bounds the relative deviation by

`Delta = U*E/M + E^2*theta/(2M) + U^2/(2*theta*M) = 5.4533062764251491470095373418931247360122632654733671223983927457219700157819766912873779723310149476577043667003831512957230587019009536571716994382022471910112359550561797752808988764044943820224719E-34`.

Appendix A checks `Delta < 2^-109`. The upper product ratio is `(1-E/M)^(-U) = 1.0000000000000000000000000000000002726301621773591511517191645631968685404080640696878517072889918802069767925173701693764597790205097319758373780398409025808778435642707328862701945274277581961927645` and the Bayes ratio is at most `R=(1-E/M)^(-U)/(1-Delta) = 1.0000000000000000000000000000000008179607898198740658526728987525097882007052900561730562656607259066431124041736972533003008046582210148551527107344484086510313086140581362812808572324402777108526801 <= 1+2^-108`. This requires the checked nonempty DP and non-DP partitions and `E/M <= 1/2`.

The Bayes calculation uses a masked filtration: it reveals the equality structure and the indicators of other walks but integrates over the DP indicators on the suffix currently selected by the common path. This is a probability calculation over comparator F; the operational run may already have exposed that suffix.

For the base case, write the first coincidence as `V_t=V_s`, `s<t`, with s on the older walk A. Evaluations of one continuing lane occur 256 indices apart. Therefore A evaluates each later common-path point first: its relevant indices are `s+256, s+2*256, ...`, all before B reaches the same respective points at `t+256, t+2*256, ...`. The tail length l is the first `k>=1` with `xi_(s+256k)=1`. For every fixed completion of these suffix indicators, the equality `V_t=V_s` has probability exactly `1/M`; fresh `V_t` is uniform after `V_s` is fixed. The event that `(t,s)` is the first pair differs between indicator completions only through D, the distinctness of `V_1..V_(t-1)`. The product bounds above place `Pr[D | indicators]` between `pi_m*(1-Delta)` and `pi_m*(1-E/M)^(-U)`. Bayes' formula thus bounds the conditional law of A's masked suffix by R times its iid Bernoulli(theta) law, proving `Pr[l>=j | first pair (t,s), masked history] <= R*q^j`.

The induction invariant is the same likelihood-ratio bound R for the masked suffix of the older trail at every later merge. Suppose the common path enters a point p whose continuation belongs to a third trail C, first evaluated at index u. The filtration records p and the merge equality but withholds the indicators `xi_(u+256), xi_(u+2*256), ...` of C's selected continuation. At the fresh evaluation that created the merge, equality with fixed p has conditional probability exactly `1/M` for every completion of those withheld indicators. That common factor cancels in Bayes' numerator and denominator. No new firstness event is imposed after `(t,s)`, so the distinct-prefix ratio R is not multiplied. This proves the inductive step. Repeating it over every merge preserves `Pr[l>=j] <= R*q^j`; a DP ends the path and can only shorten l.

The excess `R-1 <= 2^-108` adds at most `2^-108` to a bin sum whose weights total at most one and at most `2^-108*F6` to the replay-tail subtraction. These enter once as `FL = 2^-108*(1+F6)`. This product-comparison and masked-suffix argument follows the structure published by credited entry `20eb70ca-366a-4fbd-9594-4fa85f158a0b` and is re-derived here with this package's U, E, theta and LRC.

For bin `j = 1..J`, the common tail l lies in `((j-1)W,jW]` with iid reference mass `q^((j-1)W)-q^(jW)`. Put `n_j = L*(Tb-jW)`. If the first coincidence occurs among those `n_j` positions, the tail finishes by the deadline. The covered term is therefore

`Pcov = sum_(j=1)^J (q^((j-1)W)-q^(jW))*B(n_j)`.

Here `J = 61854`, `W = 633825300114114700748351602688`, and `J*W = LRC = 39204630113258450700088540032663552`. The experiment asserts that equality and recomputes every term in order.

### Failure bounds F2 through F6

F1 is the covered event counted by `Pcov`. The remaining named terms are upper bounds subtracted from it.

- F2, table exhaustion. The restart domination above gives `X <= Binomial(E,theta)` with mean `mu = E*theta = 90911.8219814300537109375000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000`. Starting the `(U-L+1)`-st replacement trail needs at least `k=U-L=92744` such fresh DP outputs. For `k>mu`, the exponential-moment Chernoff bound is `Pr[X>=k] <= exp(-mu+k*(1+ln(mu/k)))`. Appendix A asserts its strict precondition.
- F3, a coincidence within one trail. If a trail has geometric length A, then a union bound over its input pairs is `A*(A-1)/(2M)`. Since `E[A*(A-1)/2]=q/theta^2 <= 1/theta^2`, at most U trails contribute `F3=U/(theta^2*M)`.
- F4, starts/replay boundaries and endpoint aliases. The U starts are fixed distinct translations of rho. Comparing them with at most E exposed inputs and images, plus the four selected replay boundary values, gives the explicit union bound `2*U*(E+4)/M = 5.4526032435471830230343832912639366275923689142961314587863202347118983689293825552691994999341855538039161012748058010613080158258338244056104718669593534971616435361644296834007783481013120763236657E-34 <= 2^-90`. Replay otherwise re-evaluates already exposed trail points and creates no new F sample. For aliases, conditioning on the DP predicate leaves the low 50 stored bits uniform. Fewer than `U*(U-1)/2` pairs therefore contribute less than `U^2*2^-51`.
- F5, hit-cap abort. Let X' count steps in which at least one fresh input has a 16-bit-prefilter image. Conditional on every prior adaptive choice, its one-step probability is at most `1-(1-2^-16)^256 = 0.00389866021631819777212921699057604228934907591347168173766934280389107431763886868964603102771424503147662168070206359168124436875563141323855886959184928433004874414589474610857484934350677083543632 < 2^-8`. Outside F4, a hit not counted by X' requires a repeated input and therefore occurs only after the first coincidence. Outside F6 the attempt stops within LRC later steps, so `hits <= X'+LRC`. Abort at hit 44384159803516906822519431956004866 therefore requires `X' >= h-LRC = 5179529690258456122430891923341314`. For the supermartingale `exp(s*X'_t-(exp(s)-1)*t/256)`, multiplicative Chernoff with `mu'=Tb/256=5179524750678730209640393532768256.00000000` and `delta=9.536743164062500000000000003861358128924700975250345118698451486303657888206937888329881958222834143571875498896875807411310101256276564883007339962182114854057958741866616089905443747602967950E-7>2^-20` gives exponent `-mu'*delta^2/(2+delta) = -2355374036092164233315.6298372126397293502850487704264466298685017655594979025667042548433997237016794469251118091236642105967763978569439521257431398894485124113252314609966301552294685041300260454366`. This is below `-1000*ln(2)`, so F5 is safely rounded up to `2^-1000`.
- F6, replay-cap refusal for the first-collision pair. Define an evaluation's age as its position in its current trail. Before the first coincidence, `Pr[age>=a] <= q^(a-1)`. Put `g(a)=min(1,q^(LRC+1-a))`. Summation by parts gives `E[g(age)] <= q^LRC + LRC*theta*q^LRC = G6`, where `G6=0.00031667909426037105941508320214937060199154109117358893263827061925923399740035084155734768296066160736452070007565526017915969197254168193964689892970815481258300740805731394400598576251592025327473506`. For a first-collision pair with ages a and b, refusal is bounded by `g(max(a,b)) <= g(a)+g(b)`, producing `2*G6`. Given fewer than U DPs, the distinct-prefix conditioning costs `(1-E/M)^(-U)`. Summing first-collision mass telescopes because `(t-1)*pi_(t-1)/M=pi_(t-1)-pi_t`. Finally `ln(1-x)>=-x-x^2` for `0<=x<=1/2` gives `1-pi_E <= 1-exp(-E^2/(2M)-E^3/(3M^2)) = 0.39197738796240174026269689679162809178335059558866342738985263399843128558663918161304509101245262829684350600623096875328734024718557078930609888907136331575878305125119026094673472946673255326244082`. Hence `F6=2*G6*(1-exp(-E^2/(2M)-E^3/(3M^2)))*(1-E/M)^(-U)`.

The conditioning lemma contributes `2^-108*(1+F6)` after the same lazy-sampling exposure, and `2^-60` covers all numerical approximation and bin-boundary rounding. A union bound gives

`P_F >= Pcov - F2 - F3 - 2^-90 - U^2/2^51 - F5 - F6 - 2^-108*(1+F6) - 2^-60`.

Every exponential and logarithm is evaluated with 200-digit Decimal arithmetic. The certificate counts at most 3962752 final-scale rounded operations. Recurrence multipliers lie in `[0,1]`; all other probability-scale intermediates are below four; integer products through `E^2` are exact and the only larger power is divided by `M^2`. The subtraction `q=1-theta` has absolute error below `1e-199`; on the live domain `q>1/2`, logarithm propagation and multiplication by `LRC<1e36` remain below `2e-163`. The audited `1e-140` final-scale allowance per counted operation is therefore conservative. Its accumulated bound is `3.962752E-134 < 2^-200`, strictly below the subtracted `2^-60` numerical term. Appendix A records 200-digit values and outward intervals by moving every endpoint one representable value outward. Its computed comparator-F bound is `0.39000000083297832218182518858987050679688137049021269065978753904866744482080022033782053734016026473489127221889034980598706700011875266565836780577125735073281058080645700971565330113085300125471478`, a margin of `8.3297832218182518858987050679688137049021269065978753904866744482080022033782053734016026473489127221889034980598706700011875266565836780577125735073281058080645700971565330113085300125471478E-10` above 0.39. The outward-rounded lower endpoint is `0.39000000083297832218182518858987050679688137049021269065978753904866744482080022033782053734016026473489127221889034980598706700011875266565836780577125735073281058080645700971565330113085300125471477 >= 0.39`; the preceding allowed Tb grid point is `0.38999999970405103831799711012993292851780650713135186412010880704062044388718787195857532220359102323044901767831255498318342240183288410329464520407329347348490504134052422314995409777910418983778432 < 0.39`.

Support for H1 is positive and specific. The algorithm is the parallel collision search of Paul C. van Oorschot and Michael J. Wiener, "Parallel Collision Search with Cryptanalytic Applications", Journal of Cryptology 12(1):1-28, 1999, DOI 10.1007/PL00003816. Generic entries in this track use the same random-function premise. The row-pair affine embedding of Section 2 is an injection from points to messages and separates circuit savings from the generic collision law; Section 6.1 prices a hazard deficit and reports reduced-scale tests. A collision-hazard deficit can be priced by scaling the comparator hazard and rerunning Appendix A. The emitted-program, scalar target, table, restart and replay checks test consistency of the exact program used by the ledger.


### 6.1 Sensitivity of H1 for the row-pair chain

The row-pair embedding makes rounds 0 and 1 almost affine in u, so the generic random-function law rests on the remaining rounds: four full nonlinear rounds and the final chi, of algebraic degree up to 32 in u. A collision-hazard deficit is priced as follows. If the true first-collision hazard of g were `(1-eps)` times the comparator's, the covered term behaves as `1-exp(-(1-eps)E^2/2M)`, and restoring the certified 0.39 needs `E` and hence the main work scaled by `(1-eps)^(-1/2)`. That adds `-0.5*log2(1-eps)` to time_log2: 0.0073 bits for eps = 1% and 0.074 bits for eps = 10%. The certificate has no slack for a deficit (margin 8.3e-10), so the claim is exactly as strong as H1.

As reduced-scale evidence (not an organizer experiment; reported by d2be26f2 for its chain, which differs from this one only in lane constants), the scalar chain g was evaluated on 2^20 inputs in each of three families, counting colliding pairs in three 32-bit output windows (bits 0..31, 112..143, 224..255; 128 pairs expected per window): uniform random u: 130, 120, 119 pairs; u varying only in u0: 126, 120, 132; distinct weight-3 points: 122, 121, 119. Every count is within one standard deviation of a random function, including for points that vary only in u0 and for distinct weight-3 points, where an affine front would be most likely to show structure. This tests consistency only; it does not reach birthday scale.

## 7. Organizer experiments

`experiments/compact.py` contains compressed source text, not prebuilt program bytes. It runs the normative Python step emitter (an independent implementation of the same construction as `np_emit.c`; both produce the SHA-256 above) on the stated constants and plan, checks operation count, register peak, byte length and hash, and checks that the step's register peak does not reach the controller's persistent registers. It re-derives the 1024-entry chained-chi table with its exhaustive 32-input truth check and checksum. It parses the exact emitted stream and executes two chained bit-sliced steps on eight lanes against scalar SHA3-256-r6 of m(u) (`message_for` in the support module implements Section 2 independently of the emitter). It assembles the controller, checks its size, hash and literal pool, runs `eval_f` against the scalar chain on four full-width points, and exercises gather/setwalk, restart packing, every slot probe position, replay success, replay refusal and the all-no-DP charged-limit halt, plus every field boundary of both encodings. The `success-certificate` experiment additionally recomputes Appendix A at 200-digit precision and checks the plan binding. Each response row returns the projected 12-bit pair derived from the first request seed when one exists among 68 points, otherwise the failed-trial null pair.

Local runs of both experiment ids and `--self-test` passed; both bounded C emitters reproduce the same step bytes as the Python emitter.

## 8. Credit

This package is a credited derivative of `221b1d6d` (25374 operations) and, through it, of `a739029e` (25380 operations), `6a4df23e` (25385 operations), `f911a9de` (Jbenisek) and `d2be26f2` (mpjunior92), whose row-pair embedding, C1[2] pivot lane, staged polarity planner, emitters, controller, certificate and bounded construction are reused; its own lineage credits `f9b654c6-23d2-4df5-9e7b-803c46b43553` (0xplemonade), `20eb70ca-366a-4fbd-9594-4fa85f158a0b`, `d258ba65-054d-4098-bbac-0b974fee36c8`, `3509abf0-ecab-457b-8d5d-ea8aec5d5e8c` and `911bffce-8e7a-4502-90ab-c69a473fff48`. The planned row-0 polarity (the `kmap` phase, the row-0 move of `np_plank.c` and the KX input of `np_consts.c`) is the leader `f911a9de`'s contribution. The joint iterated local search `np_ils2.c`, the exhaustive target-pair polish `np_pair.c`, the kick-and-repair two-column joint local search `np_ils4.c`, the plateau-drift variant `np_ils6.c` and the `NOT (NOT x)` canonicalization are contributions of that lineage (leader packages `6a4df23e` and `a739029e`); the dump-writing variant `np_ils7.c` used here is this package's instrumented copy of that `np_ils6.c` (Appendix B). New here: a further pass-1 basin (`np_plank`, seed 34) whose planned row-0 polarity defines a different embedding, the full re-derivation of the chain in that embedding (passes 2 through 12 through the package's unchanged tools), five plateau-drift passes (`np_ils6`, seeds 7001, 7002, 7006, 8002 and 8007) reaching model values 12758, 12755, 12753, 12753 and 12752 with emissions 25381, 25377, 25374, 25373 and 25371, a second joint ILS (`np_ils2`, seed 57) reaching model value 12752 with emission 25370, a narrow drift (`np_ils6`, seed 8105, 108 iterations) reaching model value 12752 with emission 25369, and three longer drifts (`np_ils7`, seeds 9206, 9406 and 9712) reaching model values 12751, 12750 and 12750 with a selected intermediate emission of 25367, yielding the 25367-operation step. The d2be26f2 sources were run as published (built from its Appendix B). Credit is not endorsement.

## Appendix A. Outward-rounded success certificate

The certificate is the incumbent's, unchanged except for the plan binding.

```json
{
 "computed_bound": "0.39000000083297832218182518858987050679688137049021269065978753904866744482080022033782053734016026473489127221889034980598706700011875266565836780577125735073281058080645700971565330113085300125471478",
 "computed_previous": "0.38999999970405103831799711012993292851780650713135186412010880704062044388718787195857532220359102323044901767831255498318342240183288410329464520407329347348490504134052422314995409777910418983778432",
 "covered_success": {
  "lower": "0.39026331172952838124627563602059655204753983679928666789240345748437719719340950331790050255058207989655624448868284381521381499496605127956630825613966758544672456604342953964221862635595419413188901",
  "upper": "0.39026331172952838124627563602059655204753983679928666789240345748437719719340950331790050255058207989655624448868284381521381499496605127956630825613966758544672456604342953964221862635595419413188903"
 },
 "failure_intervals": {
  "endpoint_alias": {
   "lower": "0.0000038409275759931915672495961189270019531249999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999",
   "upper": "0.0000038409275759931915672495961189270019531250000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001"
  },
  "hit_cap_F5": {
   "lower": "9.3326361850321887899008954472381716961709144637170802462171433979596691097577563445444032709788110235959498993032424262421548752135403239484152081720393075623441066613832515027399507598590183151110048E-302",
   "upper": "9.3326361850321887899008954472381716961709144637170802462171433979596691097577563445444032709788110235959498993032424262421548752135403239484152081720393075623441066613832515027399507598590183151110050E-302"
  },
  "lemma_conditioning": {
   "lower": "3.0822529276436877636627719019139768856221085002424637934448000204427951434042801056887098101184405503777941268476758958328526368914990811970221991030816208204415704040790419790844091894922685747186988E-33",
   "upper": "3.0822529276436877636627719019139768856221085002424637934448000204427951434042801056887098101184405503777941268476758958328526368914990811970221991030816208204415704040790419790844091894922685747186990E-33"
  },
  "numeric_rounding": {
   "lower": "8.6736173798840354720596224069595336914062499999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999E-19",
   "upper": "8.6736173798840354720596224069595336914062500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001E-19"
  },
  "replay_cap_F6": {
   "lower": "0.00024826208838095891388188359586761104462409055556067766015941095897697378192003992639258315620087815941800759846207355109483094851303797094948660988135432277097519164432933936654679825175369936243414448",
   "upper": "0.00024826208838095891388188359586761104462409055556067766015941095897697378192003992639258315620087815941800759846207355109483094851303797094948660988135432277097519164432933936654679825175369936243414450"
  },
  "self_coincidence_F3": {
   "lower": "0.000011197034645345442494634515843959096073728064638303244539830829440727180911501073096831208180785254387072339351092033834111854563817699785380633758363842949122585532129781593233177629087236460042923872",
   "upper": "0.000011197034645345442494634515843959096073728064638303244539830829440727180911501073096831208180785254387072339351092033834111854563817699785380633758363842949122585532129781593233177629087236460042923874"
  },
  "start_replay_collision": {
   "lower": "8.0779356694631608874161005084957309918536338955163955688476562499999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999E-28",
   "upper": "8.0779356694631608874161005084957309918536338955163955688476562500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001E-28"
  },
  "table_exhaustion_F2": {
   "lower": "1.0845947760649144940926695351702801549563547913565816663485043039749637942632031481046019708952716488051873639714487686751220065149046225530832859216356924708979316386767682267723439815484293091380264E-8",
   "upper": "1.0845947760649144940926695351702801549563547913565816663485043039749637942632031481046019708952716488051873639714487686751220065149046225530832859216356924708979316386767682267723439815484293091380266E-8"
  }
 },
 "hit_abort": 44384159803516906822519431956004866,
 "hit_limit": 44384159803516906822519431956004865,
 "key_bits": 50,
 "margin_above_target": "8.3297832218182518858987050679688137049021269065978753904866744482080022033782053734016026473489127221889034980598706700011875266565836780577125735073281058080645700971565330113085300125471478E-10",
 "parameters": {
  "DK": 10,
  "DPLO": 145,
  "DT": 712,
  "HF": 111,
  "HIT_ABORT": 44384159803516906822519431956004866,
  "HMAX": 44384159803516906822519431956004865,
  "J": 61854,
  "LRC": 39204630113258450700088540032663552,
  "NR": 6,
  "PFLO": 240,
  "PFN": 16,
  "S": 18600,
  "SB": 15,
  "Tb": 1325958336173754933667940744388673536,
  "U": 93000,
  "W": 633825300114114700748351602688
 },
 "plan_sha256": "c06833ea87f90cba1cbec2ec91f30f9fd35d7ed701cbef089a3cfc0369c1bdfd",
 "preconditions": {
  "available_gt_mean": true,
  "bins_cover_replay_cap": true,
  "conditioning_delta_lt_2^-109": true,
  "conditioning_ratio_le_1_plus_2^-108": true,
  "dp_partition_nonempty": true,
  "evaluation_fraction_le_half": true,
  "fresh_hit_delta_gt_2^-20": true,
  "fresh_hit_threshold_gt_mean": true,
  "fresh_step_probability_lt_2^-8": true,
  "hit_threshold_equals_abort_minus_lrc": true,
  "replay_cap_below_deadline": true,
  "start_replay_bound_le_2^-90": true,
  "table_has_initial_walks": true
 },
 "probability_inputs": {
  "age_g6": "0.00031667909426037105941508320214937060199154109117358893263827061925923399740035084155734768296066160736452070007565526017915969197254168193964689892970815481258300740805731394400598576251592025327473506",
  "available_restarts": 92744,
  "coincidence_upper": "0.39197738796240174026269689679162809178335059558866342738985263399843128558663918161304509101245262829684350600623096875328734024718557078930609888907136331575878305125119026094673472946673255326244082",
  "conditioning_delta": "5.4533062764251491470095373418931247360122632654733671223983927457219700157819766912873779723310149476577043667003831512957230587019009536571716994382022471910112359550561797752808988764044943820224719E-34",
  "conditioning_dp_term": "1.3944613874130371994082473323433114887988333919254993873893403138718550952729897238732723707563421699438202247191011235955056179775280898876404494382022471910112359550561797752808988764044943820224719E-34",
  "conditioning_inflation": "1.0000000000000000000000000000000002726301621773591511517191645631968685404080640696878517072889918802069767925173701693764597790205097319758373780398409025808778435642707328862701945274277581961927645",
  "conditioning_partition_term": "1.33254326723852043608409836391784493344937196342475333962232954342378322244884721113520881835986817772095325285164335582521744072437286376953125E-34",
  "conditioning_ratio": "1.0000000000000000000000000000000008179607898198740658526728987525097882007052900561730562656607259066431124041736972533003008046582210148551527107344484086510313086140581362812808572324402777108526801",
  "conditioning_start_term": "2.726301621773591511517191645631968313764057910123114395386722888426331698060139756278896783214804599992930889129638671875E-34",
  "evaluations": 339445334060481263018992830563500425216,
  "fresh_hit_delta": "9.536743164062500000000000003861358128924700975250345118698451486303657888206937888329881958222834143571875498896875807411310101256276564883007339962182114854057958741866616089905443747602967950E-7",
  "fresh_hit_mean_upper": "5179524750678730209640393532768256.00000000",
  "fresh_hit_threshold": 5179529690258456122430891923341314,
  "fresh_step_probability_exact": "0.00389866021631819777212921699057604228934907591347168173766934280389107431763886868964603102771424503147662168070206359168124436875563141323855886959184928433004874414589474610857484934350677083543632",
  "fresh_step_probability_upper": "0.00390625",
  "hit_chernoff_exponent": "-2355374036092164233315.6298372126397293502850487704264466298685017655594979025667042548433997237016794469251118091236642105967763978569439521257431398894485124113252314609966301552294685041300260454366",
  "mean_dp": "90911.8219814300537109375000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
  "prefilter_bits": 16,
  "start_replay_union_bound": "5.4526032435471830230343832912639366275923689142961314587863202347118983689293825552691994999341855538039161012748058010613080158258338244056104718669593534971616435361644296834007783481013120763236657E-34",
  "theta_denominator_bits": 121,
  "theta_numerator": 712
 },
 "round": 6,
 "rounding": "200-digit Decimal; every interval moved one representable value outward",
 "rounding_audit": {
  "accumulated_absolute_bound": "3.962752E-134",
  "accumulated_lt_2^-200": true,
  "charged_numeric_term": "8.67361737988403547205962240695953369140625E-19",
  "operation_bound": 3962752,
  "per_operation_absolute_bound": "1E-140",
  "precision_digits": 200
 },
 "schema": "hashsmash-random-function-success-v1",
 "target": "0.39",
 "trails": 93000,
 "union_lower": "0.39000000083297832218182518858987050679688137049021269065978753904866744482080022033782053734016026473489127221889034980598706700011875266565836780577125735073281058080645700971565330113085300125471477"
}
```

## Appendix B. Bounded construction sources

Build: `gcc -O2 -mpopcnt -static -nostdlib -ffreestanding -fno-stack-protector -fno-builtin -fno-pie -no-pie`. Phases: `np_consts constants0.txt`; `np_emit record spec_zero.txt plan_input.txt` (incumbent constants plus an empty plan; also builds the one-constant row table); `np_emit kmap spec_zero.txt kmap.txt` (row-0 polarity masks); `np_plank plan_input.txt 90000000 2 34 6 plan1.txt K:kmap.txt > pass1.out`; `np_consts consts.txt pass1.out` (applies the KX line); `np_emit record spec1.txt pi2.txt` (constants plus the pass-1 plan); `np_plan pi2.txt 200000000 2 19 6 plan2.txt plan1.txt` (pass 2); `np_ils2 pi2.txt plan2.txt 6000 51 3 plan3.txt` (pass 3); `np_pair pi2.txt plan3.txt s1 plan4.txt` (pass 4, exhaustive same-round target-pair polish); `np_ils4 pi2.txt plan4.txt 75 4001 10 plan5.txt` (pass 5, exact two-column joint local search); `np_ils6 pi2.txt plan5.txt 500 7001 10 drift7001.txt` (pass 6, plateau-drift two-column joint local search); `np_ils6 pi2.txt drift7001.txt 500 7002 10 drift7002.txt` (pass 7, plateau drift from the pass-6 plan); `np_ils6 pi2.txt drift7002.txt 500 7006 10 drift7006.txt` (pass 8, plateau drift from the pass-7 plan); `np_ils6 pi2.txt drift7006.txt 500 8002 10 drift8002.txt` (pass 9, plateau drift from the pass-8 plan); `np_ils6 pi2.txt drift8002.txt 500 8007 10 drift8007.txt` (pass 10, plateau drift from the pass-9 plan); `np_ils7 pi2.txt drift8105.txt 6000 9206 10 drift9206.txt dump9206` (pass 13, long plateau drift, dumping every accepted state); `np_ils7 pi2.txt drift9206.txt 4000 9406 31 drift9406.txt dump9406` (pass 14, long plateau drift from the pass-13 plan; the iteration-3273 state emits 25368 operations); `np_ils7 pi2.txt drift9406_3301.txt 1000 9712 31 drift9712.txt dump9712` (pass 15, long plateau drift from the pass-14 plan state at iteration 3301; the selected plan is `dump9712/acc_20.txt`); `np_emit emit specF.txt step.bin` (constants plus the final plan; the `NOT (NOT x)` fold is active only in this mode, since the record and kmap modes disable it and therefore reproduce the pre-canonicalization tables, masks and plans bit for bit); `np_ctl controller.bin prefilter.bin`.

### rt.h

```c
/* Minimal freestanding x86-64 Linux runtime for bounded construction phases. */
#ifndef RT_H
#define RT_H
typedef unsigned long size_t;
typedef unsigned char uint8_t; typedef signed short int16_t; typedef unsigned short uint16_t; typedef unsigned int uint32_t; typedef int int32_t;
typedef unsigned long uint64_t; typedef long int64_t;
#define NULL ((void*)0)
static long rt_sys3(long n, long a, long b, long c) {
  long r; __asm__ volatile ("syscall" : "=a"(r) : "a"(n), "D"(a), "S"(b), "d"(c) : "rcx", "r11", "memory"); return r;
}
static void rt_exit(int code) { rt_sys3(231, code, 0, 0); for (;;) {} }
void *memset(void *d, int c, size_t n) { unsigned char *p = d; while (n--) *p++ = (unsigned char)c; return d; }
void *memcpy(void *d, const void *s, size_t n) { unsigned char *p = d; const unsigned char *q = s; while (n--) *p++ = *q++; return d; }
int memcmp(const void *a, const void *b, size_t n) { const unsigned char *p = a, *q = b; for (; n; n--, p++, q++) if (*p != *q) return *p - *q; return 0; }
static size_t rt_strlen(const char *s) { size_t n = 0; while (s[n]) n++; return n; }
static int rt_streq(const char *a, const char *b) { while (*a && *a == *b) { a++; b++; } return *a == *b; }
static void rt_write(int fd, const void *buf, size_t n) { const char *p = buf; while (n) { long w = rt_sys3(1, fd, (long)p, (long)n); if (w <= 0) rt_exit(3); p += w; n -= (size_t)w; } }
static void rt_puts(const char *s) { rt_write(1, s, rt_strlen(s)); }
static void rt_putl(long v) { char b[24]; int i = 23; b[i] = 0; int neg = v < 0; unsigned long u = neg ? (unsigned long)(-v) : (unsigned long)v; do { b[--i] = (char)('0' + u % 10); u /= 10; } while (u); if (neg) b[--i] = '-'; rt_puts(b + i); }
static void fail(const char *m) { rt_write(2, "error: ", 7); rt_write(2, m, rt_strlen(m)); rt_write(2, "\n", 1); rt_exit(2); }
/* whole-file read into a caller buffer; returns length */
static long rt_read_file(const char *path, char *buf, long cap) {
  long fd = rt_sys3(2, (long)path, 0, 0); if (fd < 0) fail("open input");
  long n = 0; for (;;) { long r = rt_sys3(0, fd, (long)(buf + n), cap - n); if (r < 0) fail("read"); if (!r) break; n += r; if (n >= cap) fail("input too large"); }
  rt_sys3(3, fd, 0, 0); buf[n] = 0; return n;
}
static long rt_create(const char *path) { long fd = rt_sys3(2, (long)path, 01 | 0100 | 01000, 0644); if (fd < 0) fail("create output"); return fd; }
/* buffered output */
static char rt_ob[16384]; static long rt_on; static long rt_ofd = -1;
static void rt_flush(void) { if (rt_on) { rt_write((int)rt_ofd, rt_ob, (size_t)rt_on); rt_on = 0; } }
static void rt_putc(int c) { if (rt_on == (long)sizeof rt_ob) rt_flush(); rt_ob[rt_on++] = (char)c; }
static void rt_putsf(const char *s) { while (*s) rt_putc(*s++); }
static void rt_putulf(unsigned long u) { char b[24]; int i = 23; b[i] = 0; do { b[--i] = (char)('0' + u % 10); u /= 10; } while (u); rt_putsf(b + i); }
static void rt_putlf(long v) { char b[24]; int i = 23; b[i] = 0; int neg = v < 0; unsigned long u = neg ? (unsigned long)(-v) : (unsigned long)v; do { b[--i] = (char)('0' + u % 10); u /= 10; } while (u); if (neg) b[--i] = '-'; rt_putsf(b + i); }
/* tokenizer */
static const char *rt_p;
static void rt_skip(void) { while (*rt_p == ' ' || *rt_p == '\n' || *rt_p == '\t' || *rt_p == '\r') rt_p++; }
static long rt_long(void) { rt_skip(); int neg = 0; if (*rt_p == '-') { neg = 1; rt_p++; } if (*rt_p < '0' || *rt_p > '9') fail("integer expected"); long v = 0; while (*rt_p >= '0' && *rt_p <= '9') v = v * 10 + (*rt_p++ - '0'); return neg ? -v : v; }
static unsigned long rt_ulong(void) { rt_skip(); if (*rt_p < '0' || *rt_p > '9') fail("integer expected"); unsigned long v = 0; while (*rt_p >= '0' && *rt_p <= '9') v = v * 10 + (unsigned long)(*rt_p++ - '0'); return v; }
static int rt_hexval(int c) { if (c >= '0' && c <= '9') return c - '0'; c |= 32; if (c >= 'a' && c <= 'f') return c - 'a' + 10; fail("hex digit"); return 0; }
static unsigned long rt_hex64(void) { rt_skip(); unsigned long v = 0; int n = 0; while ((*rt_p >= '0' && *rt_p <= '9') || ((*rt_p | 32) >= 'a' && (*rt_p | 32) <= 'f')) { v = v * 16 + (unsigned long)rt_hexval(*rt_p++); n++; } if (!n || n > 16) fail("hex lane"); return v; }
static int rt_word(char *w, int cap) { rt_skip(); int n = 0; while (*rt_p && *rt_p != ' ' && *rt_p != '\n' && *rt_p != '\t' && *rt_p != '\r') { if (n + 1 >= cap) fail("token too long"); w[n++] = *rt_p++; } w[n] = 0; return n; }
/* report VmHWM (bytes) of this process on stderr as "vmhwm <bytes>" */
__attribute__((used)) static void rt_report_vmhwm(void) {
  static char st[4096]; long fd = rt_sys3(2, (long)"/proc/self/status", 0, 0); if (fd < 0) return;
  long n = rt_sys3(0, fd, (long)st, sizeof st - 1); rt_sys3(3, fd, 0, 0); if (n <= 0) return; st[n] = 0;
  for (long i = 0; i + 6 < n; i++) if (st[i] == 'V' && st[i+1] == 'm' && st[i+2] == 'H' && st[i+3] == 'W' && st[i+4] == 'M' && st[i+5] == ':') {
    long j = i + 6, v = 0; while (st[j] == ' ' || st[j] == '\t') j++; while (st[j] >= '0' && st[j] <= '9') v = v * 10 + (st[j++] - '0');
    char b[48]; int k = 47; b[k] = 0; b[--k] = '\n'; unsigned long u = (unsigned long)v * 1024; do { b[--k] = (char)('0' + u % 10); u /= 10; } while (u);
    const char *p = "vmhwm "; rt_write(2, p, 6); rt_write(2, b + k, rt_strlen(b + k)); return; }
}
int main(int argc, char **argv);
__asm__(".globl _start\n_start:\n xor %rbp,%rbp\n mov (%rsp),%rdi\n lea 8(%rsp),%rsi\n and $-16,%rsp\n call main\n push %rax\n push %rax\n call rt_report_vmhwm\n pop %rax\n pop %rax\n mov %eax,%edi\n mov $231,%eax\n syscall\n");
#endif
```

### np_consts.c

```c
/* Bounded derivation of the 25 absorbed lane constants of the row-pair embedding.
 * Rule: theta-0 column-effect target D0 = (~1, ~PAD, ~0, ~0, ~0); lane 15 = 1; row-1 lanes = D0
 * (so every round-0 chi row sees constant 0 at position 1); row-0 lanes = fixed K0; row-2 lanes
 * complete the column parities C0 that produce D0.  usage: np_consts <out> [kx-file]
 * kx-file: the planner output line "KX b0..b319"; bit b flips bit b%64 of K0[b/64] (the planned row-0 polarity). */
#include "rt.h"
static const uint64_t PAD = 0x8000000000000006UL;
static uint64_t K0[5] = {0x91b7584a2265b1f5UL, 0xcd613e30d8f16adfUL, 0x1027c4d1c386bbc4UL, 0x1e2feb89414c343cUL, 0xc2ce6f447ed4d57bUL};
static char kxbuf[4096];
typedef struct { uint64_t m[5]; int v; int used; } Row;
static Row piv[320];
static int top(const uint64_t m[5]) { for (int w = 4; w >= 0; w--) if (m[w]) return 64 * w + 63 - __builtin_clzl(m[w]); return -1; }
static uint64_t rotl(uint64_t v, int k) { k &= 63; return k ? (v << k) | (v >> (64 - k)) : v; }
int main(int argc, char **argv) {
  if (argc != 2 && argc != 3) fail("usage");
  if (argc == 3) { long n = rt_read_file(argv[2], kxbuf, sizeof kxbuf - 1); const char *q = 0;
    for (long i = 0; i + 3 <= n; i++) if (kxbuf[i] == 'K' && kxbuf[i + 1] == 'X' && kxbuf[i + 2] == ' ') { q = kxbuf + i + 3; break; }
    if (!q) fail("no KX line");
    for (int b = 0; b < 320; b++) { if (q[b] != '0' && q[b] != '1') fail("KX width"); if (q[b] == '1') K0[b >> 6] ^= 1UL << (b & 63); } }
  uint64_t D0[5] = {~1UL, ~PAD, ~0UL, ~0UL, ~0UL};
  for (int x = 0; x < 5; x++) for (int z = 0; z < 64; z++) {
    uint64_t m[5] = {0, 0, 0, 0, 0}; int a = 64 * ((x + 4) % 5) + z, b = 64 * ((x + 1) % 5) + ((z + 63) & 63);
    m[a >> 6] |= 1UL << (a & 63); m[b >> 6] |= 1UL << (b & 63); int v = (int)((D0[x] >> z) & 1);
    for (;;) { int h = top(m); if (h < 0) { if (v) fail("D0 not in image"); break; }
      if (piv[h].used) { for (int w = 0; w < 5; w++) m[w] ^= piv[h].m[w]; v ^= piv[h].v; }
      else { for (int w = 0; w < 5; w++) piv[h].m[w] = m[w]; piv[h].v = v; piv[h].used = 1; break; } }
  }
  uint64_t sol[5] = {0, 0, 0, 0, 0};
  for (int h = 0; h < 320; h++) if (piv[h].used) {
    int par = piv[h].v;
    for (int w = 0; w < 5; w++) { uint64_t rest = piv[h].m[w] & sol[w]; if (w == (h >> 6)) rest &= ~(1UL << (h & 63)); par ^= __builtin_popcountl(rest) & 1; }
    if (par) sol[h >> 6] |= 1UL << (h & 63);
  }
  for (int x = 0; x < 5; x++) if ((sol[(x + 4) % 5] ^ rotl(sol[(x + 1) % 5], 1)) != D0[x]) fail("theta check");
  uint64_t lane[25] = {0};
  uint64_t A03 = 1;
  for (int x = 0; x < 5; x++) { lane[x] = K0[x]; lane[x + 5] = D0[x]; }
  for (int x = 0; x < 5; x++) lane[x + 10] = sol[x] ^ K0[x] ^ D0[x] ^ (x == 0 ? A03 : 0) ^ (x == 1 ? PAD : 0);
  lane[15] = A03; lane[16] = PAD;
  rt_ofd = rt_create(argv[1]);
  for (int l = 0; l < 25; l++) { for (int s = 60; s >= 0; s -= 4) rt_putc("0123456789abcdef"[(lane[l] >> s) & 15]); rt_putc(l == 24 ? '\n' : ' '); }
  rt_flush();
  return 0;
}
```

### np_emit.c

```c
/* Bounded C emitter for the row-pair SHA3-256 r6 bit-sliced step.
 * Mirrors the normative Python emitter (newstep.py) node for node.
 * usage: np_emit record <spec> <plan-input-out>
 *        np_emit emit   <spec> <step-binary-out>
 * spec: line 1 = 25 hex lanes; following lines = plan text (T r hex / CN r hex / DN r hex).
 */
#include "rt.h"
#include "chained_table.h"

#define NC (-1)
#define ROUNDS 6
#define MAXSEG 8400
enum { O_IN, O_XOR, O_AND, O_OR, O_NOT };
static const uint64_t RC[24] = {1ULL,32898ULL,9223372036854808714ULL,9223372039002292224ULL,32907ULL,2147483649ULL,
 9223372039002292353ULL,9223372036854808585ULL,138ULL,136ULL,2147516425ULL,2147483658ULL,2147516555ULL,
 9223372036854775947ULL,9223372036854808713ULL,9223372036854808579ULL,9223372036854808578ULL,9223372036854775936ULL,
 32778ULL,9223372039002259466ULL,9223372039002292353ULL,9223372036854808704ULL,2147483649ULL,9223372039002292232ULL};
static const int RHO[25] = {0,1,62,28,27,36,44,6,55,20,3,10,43,25,39,41,45,15,21,8,18,2,61,56,14};
static const int PIVOT_ROT[4] = {28, 35, 4, 50};

typedef struct { int n; int p; } V;
typedef struct {
  int count, inputs, affine;
  uint8_t op[MAXSEG]; int16_t a[MAXSEG], b[MAXSEG]; uint8_t k[MAXSEG], has[MAXSEG];
} Graph;
static Graph G[ROUNDS - 1];              /* segment s uses G[s]; s=0 holds rounds 0..1 */
#define MAXAFF 4000
static uint64_t LIN[MAXAFF][4];      /* affine forms for segment 0 */
static int16_t ctab[16384], ftab[8192];
static Graph *g;

static uint32_t hmix(uint64_t x) { x ^= x >> 33; x *= 0xff51afd7ed558ccdULL; x ^= x >> 33; x *= 0xc4ceb9fe1a85ec53ULL; x ^= x >> 33; return (uint32_t)x; }
static int new_node(int op, int a, int b) {
  int n = g->count++;
  if (n >= MAXSEG || (g->affine && n >= MAXAFF)) fail("segment node capacity");
  g->op[n] = (uint8_t)op; g->a[n] = (int16_t)a; g->b[n] = (int16_t)b; g->k[n] = 0; g->has[n] = 0;
  return n;
}
static int scratch_mode; static int record_mode; static uint16_t touched[256]; static int ntouched;
static void reset(Graph *gr, int inputs, int affine) {
  g = gr; g->count = 0; g->inputs = inputs; g->affine = affine;
  if (scratch_mode) { for (int i = 0; i < ntouched; i++) ctab[touched[i]] = -1; ntouched = 0; }
  else { memset(ctab, 0xff, sizeof ctab); memset(ftab, 0xff, sizeof ftab); }
  for (int j = 0; j < inputs; j++) {
    int n = new_node(O_IN, 0, 0);
    if (affine) {
      memset(LIN[n], 0, 32); LIN[n][j >> 6] = 1ULL << (j & 63); g->has[n] = 1;
      uint32_t h = hmix(LIN[n][0] ^ hmix(LIN[n][1]) ^ ((uint64_t)hmix(LIN[n][2]) << 32) ^ hmix(LIN[n][3] + 7)) & 8191;
      while (ftab[h] >= 0) h = (h + 1) & 8191;
      ftab[h] = (int16_t)n;
    }
  }
}
static uint32_t fhash(const uint64_t m[4]) { return hmix(m[0] ^ hmix(m[1]) ^ ((uint64_t)hmix(m[2]) << 32) ^ hmix(m[3] + 7)) & 8191; }
static int find_form(const uint64_t m[4]) {
  uint32_t h = fhash(m);
  while (ftab[h] >= 0) { int n = ftab[h]; if (!memcmp(LIN[n], m, 32)) return n; h = (h + 1) & 8191; }
  return -1;
}
static void add_form(int n) { uint32_t h = fhash(LIN[n]); while (ftab[h] >= 0) h = (h + 1) & 8191; ftab[h] = (int16_t)n; }
static int cons(int op, int a, int b, int *created) {
  if (op != O_NOT && a > b) { int t = a; a = b; b = t; }
  uint32_t h = hmix(((uint64_t)op << 40) ^ ((uint64_t)(a + 1) << 20) ^ (uint64_t)(b + 1)) & 16383;
  while (ctab[h] >= 0) { int n = ctab[h]; if (g->op[n] == op && g->a[n] == a && g->b[n] == b) { if (created) *created = 0; return n; } h = (h + 1) & 16383; }
  int n = new_node(op, a, b); ctab[h] = (int16_t)n; if (scratch_mode) { if (ntouched >= 256) fail("scratch"); touched[ntouched++] = (uint16_t)h; } if (created) *created = 1; return n;
}
static V mk(int n, int p) { V v = { n, p & 1 }; return v; }
static V xorv(V l, V r) {
  if (l.n == NC) return mk(r.n, r.p ^ l.p);
  if (r.n == NC) return mk(l.n, l.p ^ r.p);
  if (l.n == r.n) return mk(NC, l.p ^ r.p);
  if (g->affine && g->has[l.n] && g->has[r.n]) {
    uint64_t m[4]; for (int i = 0; i < 4; i++) m[i] = LIN[l.n][i] ^ LIN[r.n][i];
    int k = g->k[l.n] ^ g->k[r.n];
    if (!(m[0] | m[1] | m[2] | m[3])) return mk(NC, k ^ l.p ^ r.p);
    int e = find_form(m);
    if (e >= 0) return mk(e, k ^ l.p ^ r.p ^ g->k[e]);
    int n = cons(O_XOR, l.n, r.n, NULL);
    g->k[n] = (uint8_t)k; memcpy(LIN[n], m, 32); g->has[n] = 1; add_form(n);
    return mk(n, l.p ^ r.p);
  }
  return mk(cons(O_XOR, l.n, r.n, NULL), l.p ^ r.p);
}
static V complement(V v) {
  if (v.n == NC) return v;
  if (!record_mode && g->op[v.n] == O_NOT) return mk(g->a[v.n], v.p);
  int created; int out = cons(O_NOT, v.n, 0, &created);
  if (created && g->affine && g->has[v.n]) { memcpy(LIN[out], LIN[v.n], 32); g->has[out] = 1; g->k[out] = g->k[v.n] ^ 1; }
  return mk(out, v.p ^ 1);
}
static V and_value(V l, V r, int select) {
  if (l.n == NC) return l.p ? r : mk(NC, 0);
  if (r.n == NC) return r.p ? l : mk(NC, 0);
  if (l.n == r.n) return l.p == r.p ? l : mk(NC, 0);
  if (!l.p && !r.p) return mk(cons(O_AND, l.n, r.n, NULL), 0);
  if (l.p && r.p) return mk(cons(O_OR, l.n, r.n, NULL), 1);
  int plain = !l.p ? l.n : r.n, other = !l.p ? r.n : l.n;
  if (select) { V neg = complement(mk(plain, 0)); return mk(cons(O_OR, neg.n, other, NULL), 1); }
  int term = cons(O_AND, plain, other, NULL);
  return xorv(mk(plain, 0), mk(term, 0));
}
static int term_cost(V a, V b) { if (a.n == NC || b.n == NC || a.n == b.n) return 0; return (a.p ^ 1) == b.p ? 1 : 2; }
static void row_choice(const V row[5], int need, int *bsub, int *btrick) {
  int distinct = 1;
  for (int x = 0; x < 5; x++) { if (row[x].n == NC) distinct = 0; for (int y = x + 1; y < 5; y++) if (row[x].n == row[y].n) distinct = 0; }
  int have = 0, wc = 0;
  for (int trick = -1; trick < (distinct ? 5 : 0); trick++) {
    if (trick >= 0 && (!((need >> trick) & 1) || !((need >> ((trick + 1) % 5)) & 1))) continue;
    for (int subset = 0; subset < 32; subset++) {
      V v[5]; memcpy(v, row, sizeof v); int cost = 0;
      for (int x = 0; x < 5; x++) if ((subset >> x) & 1) { if (row[x].n == NC) cost = 1 << 29; else { v[x].p ^= 1; cost += 1; } }
      for (int x = 0; x < 5; x++) {
        if (!((need >> x) & 1)) continue;
        if (x == trick) {
          int k = (trick + 1) % 5; V left = v[(k + 1) % 5], right = v[(k + 2) % 5];
          if ((left.p ^ 1) == right.p) { V s = mk(v[k].n, v[k].p ^ (left.p ^ 1)); cost += term_cost(s, v[(x + 2) % 5]); }
          else cost += 1;
        } else cost += term_cost(v[(x + 1) % 5], v[(x + 2) % 5]);
      }
      if (!have || cost < wc) { have = 1; wc = cost; *bsub = subset; *btrick = trick; }
    }
  }
}
static void emit_planned_row(const V row[5], int subset, int trick, const int sel[5], int need, V out[5]) {
  V v[5]; memcpy(v, row, sizeof v);
  for (int x = 0; x < 5; x++) if ((subset >> x) & 1) v[x] = complement(v[x]);
  int k = (trick + 1) % 5;
  if (trick >= 0) {
    V first = mk(v[(k + 1) % 5].n, v[(k + 1) % 5].p ^ 1);
    V t = and_value(first, v[(k + 2) % 5], sel[k]); out[k] = xorv(v[k], t);
  }
  for (int x = 0; x < 5; x++) {
    if (!((need >> x) & 1) || (trick >= 0 && x == k)) continue;
    V first = (x == trick) ? out[k] : v[(x + 1) % 5]; first.p ^= 1;
    V t = and_value(first, v[(x + 2) % 5], sel[x]); out[x] = xorv(v[x], t);
  }
}
static void emit_chained_row(const V row[5], int subset, int tricks, int selected, V out[5]) {
  V v[5]; memcpy(v, row, sizeof v);
  for (int x = 0; x < 5; x++) if ((subset >> x) & 1) v[x] = complement(v[x]);
  int start = 0; while ((tricks >> start) & 1) start++;
  for (int i = 0; i < 5; i++) {
    int x = ((start - i) % 5 + 5) % 5;
    V first = ((tricks >> x) & 1) ? out[(x + 1) % 5] : v[(x + 1) % 5]; first.p ^= 1;
    V t = and_value(first, v[(x + 2) % 5], (selected >> x) & 1); out[x] = xorv(v[x], t);
  }
}
/* plan */
static uint8_t TG[ROUNDS][320], CNB[ROUNDS][320], DNB[ROUNDS][320];
static uint64_t K[25];
static uint8_t rec_full[320], rec_pat[320], rec_kind[320], rec_type[320];
static uint16_t DEC1[320]; static int have_dec1;
static uint8_t CTC[160][32]; static uint16_t CTD[160][32];
static V state[1600], nxt[1600], column[320], delta[320]; static uint8_t hc[320], hd[320];
static const uint8_t *CNr, *DNr;
static void makec(int x, int z) {
  V v = state[64 * x + z];
  for (int y = 1; y < 5; y++) v = xorv(v, state[64 * (x + 5 * y) + z]);
  if (CNr[64 * x + z]) v = complement(v);
  column[64 * x + z] = v; hc[64 * x + z] = 1;
}
static V maked(int x, int z) {
  int i = 64 * x + z;
  if (!hd[i]) {
    int lx = (x + 4) % 5, lz = z, rx = (x + 1) % 5, rz = (z + 63) & 63;
    if (!hc[64 * lx + lz]) makec(lx, lz);
    if (!hc[64 * rx + rz]) makec(rx, rz);
    V v = xorv(column[64 * lx + lz], column[64 * rx + rz]);
    if (DNr[i]) v = complement(v);
    delta[i] = v; hd[i] = 1;
  }
  return delta[i];
}
static void build_round(int r) {
  int last = r == ROUNDS - 1;
  static const uint8_t zero[320];
  CNr = r >= 2 ? CNB[r] : zero; DNr = r >= 2 ? DNB[r] : zero;
  memset(hc, 0, sizeof hc); memset(hd, 0, sizeof hd);
  if (!last) {
    for (int x = 0; x < 5; x++) makec(x, 63);
    for (int z = 0; z < 64; z++) { if (z < 63) for (int x = 0; x < 5; x++) makec(x, z); for (int x = 0; x < 5; x++) maked(x, z); }
  }
  memcpy(nxt, state, sizeof state);
  int need = last ? 15 : 31;
  for (int yo = 0; yo < (last ? 1 : 5); yo++) for (int z = 0; z < 64; z++) {
    V row[5], out[5];
    for (int xo = 0; xo < 5; xo++) { int y = xo, x = (3 * yo + xo) % 5, zz = (z - RHO[x + 5 * y]) & 63; row[xo] = xorv(state[64 * (x + 5 * y) + zz], maked(x, zz)); }
    int full = 1;
    for (int i = 0; i < 5; i++) { if (row[i].n == NC) full = 0; for (int j = i + 1; j < 5; j++) if (row[i].n == row[j].n) full = 0; }
    int pattern = 0; for (int i = 0; i < 5; i++) pattern |= row[i].p << i;
    if (record_mode && r == 1) {
      int ri = 64 * yo + z, nnc = 0, c = -1, distinct = 1;
      for (int i = 0; i < 5; i++) if (row[i].n == NC) { nnc++; c = i; }
      for (int i = 0; i < 5; i++) for (int j = i + 1; j < 5; j++) if (row[i].n != NC && row[i].n == row[j].n) distinct = 0;
      rec_full[ri] = (uint8_t)full; rec_pat[ri] = (uint8_t)pattern;
      rec_kind[ri] = (uint8_t)(full ? 1 : (nnc == 1 && distinct) ? 2 : 0);
      if (rec_kind[ri] == 2) { int pp = 0, k = 0; for (int i = 0; i < 5; i++) if (i != c) pp |= row[i].p << k++; rec_type[ri] = (uint8_t)(32 * c + 16 * row[c].p + pp); }
    }
    if (full && !last && r >= 1) {
      const unsigned char *e = CHT[32 * pattern + TG[r][64 * yo + z]];
      emit_chained_row(row, e[1], e[2], e[3], out);
    } else if (r == 1 && have_dec1 && DEC1[64 * yo + z] != 0xFFFF) {
      int d = DEC1[64 * yo + z];
      emit_chained_row(row, d & 31, (d >> 5) & 31, (d >> 10) & 31, out);
    } else {
      int subset = 0, trick = -1; row_choice(row, need, &subset, &trick);
      V v[5]; memcpy(v, row, sizeof v);
      for (int x = 0; x < 5; x++) if ((subset >> x) & 1) v[x].p ^= 1;
      int sel[5] = {0, 0, 0, 0, 0};
      if (trick >= 0) { int k = (trick + 1) % 5; V left = v[(k + 1) % 5], right = v[(k + 2) % 5];
        sel[k] = ((left.p ^ 1) != right.p) ? (v[(trick + 2) % 5].p ^ 1 ^ v[k].p) : 0; }
      emit_planned_row(row, subset, trick, sel, need, out);
    }
    for (int xo = 0; xo < (last ? 4 : 5); xo++) nxt[64 * (xo + 5 * yo) + z] = out[xo];
  }
  for (int z = 0; z < 64; z++) nxt[z].p ^= (int)((RC[r] >> z) & 1);
  memcpy(state, nxt, sizeof state);
}
static int16_t OUTS[ROUNDS][1600]; static int NOUT[ROUNDS]; static uint8_t POL[1600];
static void embedding(void) {
  for (int l = 0; l < 25; l++) for (int z = 0; z < 64; z++) state[64 * l + z] = mk(NC, (int)((K[l] >> z) & 1));
  V nodes[320];
  for (int x = 0; x < 4; x++) for (int z = 0; z < 64; z++) nodes[64 * x + z] = mk(64 * x + z, 0);
  for (int z = 0; z < 64; z++) { V v = mk(NC, 0); for (int x = 0; x < 4; x++) v = xorv(v, mk(64 * x + ((z - PIVOT_ROT[x]) % 64 + 64) % 64, 0)); nodes[256 + z] = v; }
  for (int x = 0; x < 5; x++) for (int z = 0; z < 64; z++) { V n = nodes[64 * x + z];
    int bases[2] = {0, 10};
    for (int bi = 0; bi < 2; bi++) { int l = bases[bi] + x; state[64 * l + z] = mk(n.n, n.p ^ (int)((K[l] >> z) & 1)); } }
}
static void build_all(void) {
  reset(&G[0], 256, 1); embedding(); build_round(0); build_round(1);
  for (int q = 0; q < 1600; q++) { OUTS[0][q] = (int16_t)state[q].n; POL[q] = (uint8_t)state[q].p; } NOUT[0] = 1600;
  for (int r = 2; r < ROUNDS; r++) {
    int s = r - 1; reset(&G[s], 1600, 0);
    for (int q = 0; q < 1600; q++) state[q] = mk(OUTS[s - 1][q] != NC ? q : NC, POL[q]);
    build_round(r);
    int n = (r == ROUNDS - 1) ? 256 : 1600;
    for (int q = 0; q < n; q++) OUTS[s][q] = (int16_t)state[q].n;
    for (int q = 0; q < 1600; q++) POL[q] = (uint8_t)state[q].p;
    NOUT[s] = n;
  }
}
/* allocation (mirrors allocate_segments) */
#define NREGS 1936
static uint8_t live[MAXSEG]; static int16_t lastu[MAXSEG], regof[MAXSEG], outidx[MAXSEG];
static int input_regs[1600]; static uint8_t busy[NREGS];
static int final_last[1600];
static int peak = 256, mixc[4];
static int outf; static uint64_t acc; static int used; static long nbytes, nops;
static void emit_word(int op, int d, int a, int b) {
  if (d == b && op != 3) { int t = a; a = b; b = t; }
  uint64_t word; int width;
  if (d == a) { word = (uint64_t)op | 4 | ((uint64_t)a << 3); width = op == 3 ? 14 : 25; if (op != 3) word |= (uint64_t)b << 14; }
  else { word = (uint64_t)op | ((uint64_t)d << 3) | ((uint64_t)a << 14); width = op == 3 ? 25 : 36; if (op != 3) word |= (uint64_t)b << 25; }
  acc |= word << used; used += width;
  while (used >= 8) { if (outf) rt_putc((int)(acc & 255)); nbytes++; acc >>= 8; used -= 8; }
  nops++;
}
static void liveness(Graph *gr, int s) {
  memset(live, 0, (size_t)gr->count);
  for (int q = 0; q < NOUT[s]; q++) if (OUTS[s][q] >= 0) live[OUTS[s][q]] = 1;
  for (int i = gr->count - 1; i >= gr->inputs; i--) if (live[i]) { live[gr->a[i]] = 1; if (gr->op[i] != O_NOT) live[gr->b[i]] = 1; }
}
static void allocate(void) {
  Graph *fg = &G[ROUNDS - 2]; int fs = ROUNDS - 2;
  liveness(fg, fs);
  for (int i = 0; i < 1600; i++) final_last[i] = 0;
  for (int i = fg->inputs; i < fg->count; i++) if (live[i]) { if (fg->a[i] < 1600) final_last[fg->a[i]] = i; if (fg->op[i] != O_NOT && fg->b[i] < 1600) final_last[fg->b[i]] = i; }
  for (int i = 0; i < 256; i++) input_regs[i] = i;
  for (int s = 0; s < ROUNDS - 1; s++) {
    Graph *gr = &G[s]; int first = gr->inputs, final = (s == ROUNDS - 2);
    liveness(gr, s);
    for (int i = 0; i < gr->count; i++) { lastu[i] = 0; outidx[i] = -1; }
    for (int i = first; i < gr->count; i++) if (live[i]) { lastu[gr->a[i]] = (int16_t)i; if (gr->op[i] != O_NOT) lastu[gr->b[i]] = (int16_t)i; }
    for (int q = 0; q < NOUT[s]; q++) { int n = OUTS[s][q]; if (n < 0) fail("constant state output"); if (outidx[n] >= 0) fail("shared state output"); outidx[n] = (int16_t)q; lastu[n] = 32767; }
    memset(busy, 0, sizeof busy);
    for (int i = 0; i < first; i++) { regof[i] = (int16_t)input_regs[i]; if (lastu[i]) busy[input_regs[i]] = 1; }
    for (int idx = first; idx < gr->count; idx++) {
      if (!live[idx]) continue;
      int op = gr->op[idx], a = gr->a[idx], b = gr->b[idx];
      int sa = regof[a], sb = op == O_NOT ? 0 : regof[b];
      if (lastu[a] == idx) busy[regof[a]] = 0;
      if (op != O_NOT && b != a && lastu[b] == idx) busy[regof[b]] = 0;
      int dest = -1;
      if (final && outidx[idx] >= 0) { dest = outidx[idx]; if (busy[dest]) fail("digest destination busy"); }
      else {
        for (int ph = 0; ph < NREGS; ph++) {
          if (busy[ph]) continue;
          if (!final && s == ROUNDS - 3 && ph < 256 && outidx[idx] >= 0) { int si = outidx[idx]; if (OUTS[fs][ph] < final_last[si]) continue; }
          if (final && ph < 256 && OUTS[fs][ph] < lastu[idx]) continue;
          dest = ph; break;
        }
        if (dest < 0) fail("register exhausted");
      }
      busy[dest] = 1; regof[idx] = (int16_t)dest; if (dest + 1 > peak) peak = dest + 1;
      int code = op == O_XOR ? 0 : op == O_AND ? 1 : op == O_OR ? 2 : 3;
      emit_word(code, dest, sa, sb); mixc[code]++;
    }
    for (int q = 0; q < NOUT[s]; q++) input_regs[q] = regof[OUTS[s][q]];
    int nb = 0; for (int i = 0; i < NREGS; i++) nb += busy[i];
    if (nb != NOUT[s]) fail("boundary mismatch");
  }
  if (used) { if (outf) rt_putc((int)acc); nbytes++; }
}
/* one-constant chi-row table: type = 32*c + 16*v + p (p = polarities of the four variable positions in order) */
static void build_ctable(void) {
  memset(ctab, 0xff, sizeof ctab); memset(ftab, 0xff, sizeof ftab); scratch_mode = 1; ntouched = 0;
  for (int ty = 0; ty < 160; ty++) for (int t = 0; t < 32; t++) { CTC[ty][t] = 255; CTD[ty][t] = 0xFFFF; }
  static uint8_t bestk[160][32][5];
  for (int ty = 0; ty < 160; ty++) {
    int c = ty / 32, v = (ty / 16) & 1, p = ty & 15;
    for (int subset = 0; subset < 32; subset++) { if ((subset >> c) & 1) continue;
      for (int tricks = 0; tricks < 31; tricks++) for (int sel = 0; sel < 32; sel++) {
        reset(&G[1], 4, 0);
        V row[5], out[5]; int k = 0;
        for (int x = 0; x < 5; x++) { if (x == c) row[x] = mk(NC, v); else { row[x] = mk(k, (p >> k) & 1); k++; } }
        emit_chained_row(row, subset, tricks, sel, out);
        int bad = 0; for (int x = 0; x < 5; x++) if (out[x].n == NC) bad = 1;
        if (bad) continue;
        memset(live, 0, (size_t)g->count);
        for (int x = 0; x < 5; x++) live[out[x].n] = 1;
        for (int i = g->count - 1; i >= 4; i--) if (live[i]) { live[g->a[i]] = 1; if (g->op[i] != O_NOT) live[g->b[i]] = 1; }
        int cost = 0; for (int i = 4; i < g->count; i++) cost += live[i];
        int tgt = 0; for (int x = 0; x < 5; x++) tgt |= out[x].p << x;
        uint8_t cand[5] = {(uint8_t)cost, (uint8_t)__builtin_popcount((unsigned)tricks), (uint8_t)__builtin_popcount((unsigned)subset), (uint8_t)subset, (uint8_t)tricks};
        int better = CTC[ty][tgt] == 255;
        if (!better) { for (int q = 0; q < 5; q++) { if (cand[q] != bestk[ty][tgt][q]) { better = cand[q] < bestk[ty][tgt][q]; break; } if (q == 4) better = sel < (CTD[ty][tgt] >> 10); } }
        if (better) { memcpy(bestk[ty][tgt], cand, 5); CTC[ty][tgt] = (uint8_t)cost; CTD[ty][tgt] = (uint16_t)(subset | (tricks << 5) | (sel << 10)); }
      } }
  }
  scratch_mode = 0; ntouched = 0;
}
static char specbuf[16384];
static void read_spec(const char *path) {
  rt_read_file(path, specbuf, sizeof specbuf - 1); rt_p = specbuf;
  for (int l = 0; l < 25; l++) K[l] = rt_hex64();
  char kind[16]; static char hex[1400];
  while (rt_word(kind, sizeof kind)) {
    if (rt_streq(kind, "nr") || rt_streq(kind, "chained")) { rt_long(); continue; }
    int r = (int)rt_long(); if (r < 0 || r >= ROUNDS) fail("plan round");
    rt_word(hex, sizeof hex);
    if (rt_streq(kind, "T")) { if (rt_strlen(hex) != 640) fail("T width"); for (int i = 0; i < 320; i++) TG[r][i] = (uint8_t)(rt_hexval(hex[2 * i]) * 16 + rt_hexval(hex[2 * i + 1])); }
    else if (rt_streq(kind, "D")) { if (r != 1 || rt_strlen(hex) != 1280) fail("D width"); have_dec1 = 1;
      for (int i = 0; i < 320; i++) DEC1[i] = (uint16_t)((rt_hexval(hex[4 * i]) * 16 + rt_hexval(hex[4 * i + 1])) | ((rt_hexval(hex[4 * i + 2]) * 16 + rt_hexval(hex[4 * i + 3])) << 8)); }
    else if (rt_streq(kind, "CN") || rt_streq(kind, "DN")) { if (rt_strlen(hex) != 80) fail("CN/DN width"); uint8_t *dst = rt_streq(kind, "CN") ? CNB[r] : DNB[r];
      for (int i = 0; i < 40; i++) { int byte = rt_hexval(hex[2 * i]) * 16 + rt_hexval(hex[2 * i + 1]); for (int bt = 0; bt < 8; bt++) dst[8 * i + bt] = (uint8_t)((byte >> bt) & 1); } }
    else fail("plan keyword");
  }
}
int main(int argc, char **argv) {
  if (argc != 4) fail("usage: np_emit record|emit|kmap spec out");
  if (rt_streq(argv[1], "kmap")) { /* round-1 input-polarity change of each row-0 constant bit (lane x and lane 10+x move together) */
    record_mode = 1; read_spec(argv[2]); rt_ofd = rt_create(argv[3]);
    static uint8_t bk[320], bp[320];
    for (int b = -1; b < 320; b++) {
      if (b >= 0) { K[b >> 6] ^= 1UL << (b & 63); K[10 + (b >> 6)] ^= 1UL << (b & 63); }
      reset(&G[0], 256, 1); embedding(); build_round(0); build_round(1);
      if (b < 0) { for (int i = 0; i < 320; i++) { bk[i] = rec_kind[i]; bp[i] = rec_kind[i] == 1 ? rec_pat[i] : rec_type[i]; } continue; }
      int n = 0; for (int i = 0; i < 320; i++) { int p = rec_kind[i] == 1 ? rec_pat[i] : rec_type[i]; if (rec_kind[i] != bk[i]) fail("kind moved"); if (p != bp[i]) n++; }
      rt_putlf(n);
      for (int i = 0; i < 320; i++) { int p = rec_kind[i] == 1 ? rec_pat[i] : rec_type[i]; if (p != bp[i]) { rt_putc(' '); rt_putlf(i); rt_putc(' '); rt_putlf(p ^ bp[i]); } }
      rt_putc('\n');
      K[b >> 6] ^= 1UL << (b & 63); K[10 + (b >> 6)] ^= 1UL << (b & 63);
    }
    rt_flush(); return 0; }
  record_mode = rt_streq(argv[1], "record");
  read_spec(argv[2]);
  if (!record_mode) build_all();
  rt_ofd = rt_create(argv[3]);
  if (record_mode) {
    rt_putlf(ROUNDS); rt_putc('\n');
    for (int p = 0; p < 32; p++) for (int t = 0; t < 32; t++) { rt_putlf(CHT[32 * p + t][0]); rt_putc(t == 31 ? '\n' : ' '); }
    for (int p = 0; p < 32; p++) { rt_putlf(LASTC[p]); rt_putc(p == 31 ? '\n' : ' '); }
    for (int R = 0; R < 5; R++) for (int zp = 0; zp < 64; zp++) for (int P = 0; P < 5; P++) {
      int X = (3 * R + P) % 5, z = ((zp - RHO[X + 5 * P]) % 64 + 64) % 64;
      rt_putlf(X + 5 * P); rt_putc(' '); rt_putlf(z); rt_putc(P == 4 ? '\n' : ' '); }
    for (int i = 0; i < 24; i++) { rt_putulf(RC[i]); rt_putc(i == 23 ? '\n' : ' '); }
    build_ctable();
    reset(&G[0], 256, 1); embedding(); build_round(0); build_round(1);
    for (int q = 0; q < 1600; q++) { rt_putlf(state[q].p); rt_putc(q == 1599 ? '\n' : ' '); }
    for (int i = 0; i < 320; i++) { rt_putlf(rec_kind[i]); rt_putc(' '); rt_putlf(rec_kind[i] == 1 ? rec_pat[i] : rec_kind[i] == 2 ? rec_type[i] : 0); rt_putc('\n'); }
    for (int ty = 0; ty < 160; ty++) { for (int t = 0; t < 32; t++) { rt_putlf(CTC[ty][t]); rt_putc(' '); } for (int t = 0; t < 32; t++) { rt_putlf(CTD[ty][t]); rt_putc(t == 31 ? '\n' : ' '); } }
    rt_flush();
    return 0;
  }
  outf = 1;
  allocate();
  rt_flush();
  rt_puts("operations "); rt_putl(nops); rt_puts(" bytes "); rt_putl(nbytes); rt_puts(" peak "); rt_putl(peak);
  rt_puts(" mix "); for (int i = 0; i < 4; i++) { rt_putl(mixc[i]); rt_puts(" "); } rt_puts("\n");
  return 0;
}
```

### np_plan.c

```c
/* Bounded staged simulated-annealing polarity planner (freestanding).
 * usage: np_plan <plan-input> <iterations-per-stage> <T0> <seed> <next-weight> <plan-out> */
#include "rt.h"
static double rt_expneg(double x) { /* exp(x) for x <= 0 */
  if (x < -700) return 0; int n = 0; while (x < -0.5) { x *= 0.5; n++; }
  double t = 1, s = 1; for (int i = 1; i < 20; i++) { t *= x / i; s += t; }
  while (n--) s *= s; return s; }
static long rt_atol(const char *s) { long v = 0; int neg = 0; if (*s == '-') { neg = 1; s++; } while (*s >= '0' && *s <= '9') v = v * 10 + (*s++ - '0'); return neg ? -v : v; }
static double rt_atof(const char *s) { double v = 0, f = 1; int dot = 0; while (*s) { if (*s == '.') dot = 1; else { if (dot) { f /= 10; v += (*s - '0') * f; } else v = v * 10 + (*s - '0'); } s++; } return v; }
static char inbuf[65536];
static int COST[32][32], LAST[32], SRCL[320][5], SRCZ[320][5];
static int MINC[32];
static uint64_t RC[24];
static int base1[1600], full1[320], pat1[320]; static int CTC[160][32], CTD[160][32];
static int r1c(int i, int t){ if (full1[i] == 1) return COST[pat1[i]][t]; if (full1[i] == 2) return CTC[pat1[i]][t] == 255 ? 1000 : CTC[pat1[i]][t]; return 0; }
static int R; static int anymove=0;
static uint64_t rs = 88172645463325252ULL;
static uint64_t rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
// state
static int tgt[8][320], cn[8][320], dn[8][320];
static int out[8][1600], pc[8][320], pd[8][320], pat[8][320];
static int dst_row[1600], dst_pos[1600]; // lane-bit (l,z) -> row,pos in next round chi
static long total;
static int stage = 99; static int WN = 16; // rounds <= stage use exact target cost; stage+1 uses MINC; later 0
static int rowcost(int r, int i){
  if (r > stage + 1) return 0;
  if (r == 1) return 16*r1c(i, tgt[1][i]);
  int w = (r == stage + 1) ? WN : 16;
  if (r == R-1) return w*(i < 64 ? LAST[pat[r][i]] : 0);
  if (r == stage + 1) return w*MINC[pat[r][i]];
  return 16*COST[pat[r][i]][tgt[r][i]];
}
static int calc_pat(int r, int i){
  int p = 0;
  for (int P = 0; P < 5; P++){ int l = SRCL[i][P], z = SRCZ[i][P]; p |= (out[r-1][64*l+z] ^ pd[r][64*(l%5)+z]) << P; }
  return p;
}
static void set_out_row(int r, int i){
  int y = i/64, z = i%64, t = tgt[r][i];
  for (int x = 0; x < 5; x++){ int l = x+5*y; out[r][64*l+z] = ((t>>x)&1) ^ (l==0 ? (int)((RC[r]>>z)&1) : 0); }
}
static void full_eval(void){
  memcpy(out[1], base1, sizeof base1);
  for (int i = 0; i < 320; i++) if (full1[i]) set_out_row(1, i);
  total = 0;
  for (int i = 0; i < 320; i++) total += rowcost(1, i);
  for (int r = 2; r < R; r++){
    for (int x = 0; x < 5; x++) for (int z = 0; z < 64; z++){ int v = cn[r][64*x+z]; for (int y = 0; y < 5; y++) v ^= out[r-1][64*(x+5*y)+z]; pc[r][64*x+z] = v; }
    for (int x = 0; x < 5; x++) for (int z = 0; z < 64; z++){ pd[r][64*x+z] = pc[r][64*((x+4)%5)+z] ^ pc[r][64*((x+1)%5)+((z+63)&63)] ^ dn[r][64*x+z]; if (r <= stage+1) total += 16*(cn[r][64*x+z] + dn[r][64*x+z]); }
    for (int i = 0; i < 320; i++){ pat[r][i] = calc_pat(r, i); total += rowcost(r, i); }
    if (r < R-1) for (int i = 0; i < 320; i++) set_out_row(r, i);
  }
}
// affected rows in round r (r>=2) by a pd flip at (X,z): lanes (X,y) bit z
static int aff[400], naff, mark[320], stamp = 1;
static void add_aff(int i){ if (mark[i] != stamp){ mark[i] = stamp; aff[naff++] = i; } }
static void pd_flip_rows(int r, int X, int z){ for (int y = 0; y < 5; y++) add_aff(dst_row[64*(X+5*y)+z]); }
// apply pd change at (X,z) in round r (toggle)
static void toggle_pd(int r, int X, int z){ pd[r][64*X+z] ^= 1; pd_flip_rows(r, X, z); }
static void toggle_pc(int r, int x, int z){ pc[r][64*x+z] ^= 1; toggle_pd(r, (x+1)%5, z); toggle_pd(r, (x+4)%5, (z+1)&63); }
// recompute affected rows' cost; returns delta
static long settle(int r){
  long d = 0;
  for (int k = 0; k < naff; k++){ int i = aff[k]; int old = rowcost(r, i); pat[r][i] = calc_pat(r, i); d += rowcost(r, i) - old; }
  return d;
}
// change target of (r,i) to t; returns delta; modifies state
static long change_target(int r, int i, int t){
  long d = -rowcost(r, i);
  int old[5]; int y = i/64, z = i%64;
  for (int x = 0; x < 5; x++) old[x] = out[r][64*(x+5*y)+z];
  tgt[r][i] = t; d += rowcost(r, i);
  set_out_row(r, i);
  if (r+1 < R){
    stamp++; naff = 0;
    for (int x = 0; x < 5; x++){ int l = x+5*y; if (out[r][64*l+z] != old[x]){ add_aff(dst_row[64*l+z]); toggle_pc(r+1, x, z); } }
    d += settle(r+1);
  }
  return d;
}
static long flip_cn(int r, int idx){ stamp++; naff = 0; cn[r][idx] ^= 1; long d = (r<=stage+1) ? (cn[r][idx] ? 16 : -16) : 0; toggle_pc(r, idx/64, idx%64); return d + settle(r); }
static long flip_dn(int r, int idx){ stamp++; naff = 0; dn[r][idx] ^= 1; long d = (r<=stage+1) ? (dn[r][idx] ? 16 : -16) : 0; toggle_pd(r, idx/64, idx%64); return d + settle(r); }
int main(int argc, char **argv){
  if (argc != 7 && argc != 8) fail("usage: np_plan input iters T0 seed weight out [pass1-plan]");
  long iters = rt_atol(argv[2]); double T0 = rt_atof(argv[3]); rs ^= (uint64_t)rt_atol(argv[4]) * 2654435761ULL; WN = (int)rt_atol(argv[5]);
  rt_read_file(argv[1], inbuf, sizeof inbuf - 1); rt_p = inbuf;
  R = (int)rt_long(); if (R != 6) fail("rounds");
  for (int p = 0; p < 32; p++) for (int t = 0; t < 32; t++) COST[p][t] = (int)rt_long();
  for (int p = 0; p < 32; p++) LAST[p] = (int)rt_long();
  for (int i = 0; i < 320; i++) for (int P = 0; P < 5; P++){ SRCL[i][P] = (int)rt_long(); SRCZ[i][P] = (int)rt_long(); }
  for (int i = 0; i < 24; i++) RC[i] = rt_ulong();
  for (int i = 0; i < 1600; i++) base1[i] = (int)rt_long();
  for (int i = 0; i < 320; i++){ full1[i] = (int)rt_long(); pat1[i] = (int)rt_long(); }
  for (int ty = 0; ty < 160; ty++){ for (int t = 0; t < 32; t++) CTC[ty][t] = (int)rt_long(); for (int t = 0; t < 32; t++) CTD[ty][t] = (int)rt_long(); }
  static char keep[4096]; int nkeep = 0;
  if (argc == 8){ /* pass 2: round 1 fixed at the actual polarities; keep the pass-1 round-1 plan lines */
    for (int i = 0; i < 320; i++) full1[i] = 0;
    rt_read_file(argv[7], inbuf, sizeof inbuf - 1);
    for (const char *q = inbuf; *q; ){ const char *e = q; while (*e && *e != '\n') e++;
      if ((q[0] == 'T' || q[0] == 'D') && q[1] == ' ' && q[2] == '1' && q[3] == ' '){ if (nkeep + (e - q) + 2 > (int)sizeof keep) fail("keep"); memcpy(keep + nkeep, q, (size_t)(e - q)); nkeep += (int)(e - q); keep[nkeep++] = '\n'; }
      q = *e ? e + 1 : e; }
    keep[nkeep] = 0; }
  for (int i = 0; i < 320; i++) for (int P = 0; P < 5; P++){ dst_row[64*SRCL[i][P]+SRCZ[i][P]] = i; dst_pos[64*SRCL[i][P]+SRCZ[i][P]] = P; }
  for (int p = 0; p < 32; p++){ MINC[p] = 99; for (int t = 0; t < 32; t++) if (COST[p][t] < MINC[p]) MINC[p] = COST[p][t]; }
  // greedy init
  for (int i = 0; i < 320; i++){ int b = 0; for (int t = 0; t < 32; t++) if (r1c(i, t) < r1c(i, b)) b = t; tgt[1][i] = b; }
  for (int r = 2; r < R-1; r++){ full_eval(); for (int i = 0; i < 320; i++){ int p = pat[r][i], b = 0; for (int t = 0; t < 32; t++) if (COST[p][t] < COST[p][b]) b = t; tgt[r][i] = b; } }
  full_eval();
  long cur, best;
  static int btgt[8][320], bcn[8][320], bdn[8][320];
  for (int st = 1; st <= R-2 + 1; st++){
    int final = (st == R-1);
    stage = final ? 99 : st;
    int rlo = final ? 1 : st, rhi = final ? R-2 : st;      // target rounds being moved
    int clo = final ? 2 : st+1, chi = final ? R-1 : st+1;   // cn/dn rounds being moved
    // greedy targets for round st+1 (used next stage) are set after
    full_eval(); cur = total; best = cur;
    memcpy(btgt, tgt, sizeof tgt); memcpy(bcn, cn, sizeof cn); memcpy(bdn, dn, sizeof dn);
    long N = final ? iters : iters;
    double T0s = final ? T0 * 0.2 : T0;
    for (long it = 0; it < N; it++){
      double T = 16*(T0s * rt_expneg(-5.5 * (double)it / N) + 0.03);
      int kind = rnd() % 10; long d; int r, i, old;
      if (kind < 6){
        r = rlo + rnd() % (rhi - rlo + 1); i = rnd() % 320;
        if (r == 1 && !full1[i]) continue;
        old = tgt[r][i]; int t = old ^ (1 + (int)(rnd() % 31));
        d = change_target(r, i, t);
        if (d <= 0 || (double)(rnd() % 1000000) / 1e6 < rt_expneg(-d / T)) cur += d; else change_target(r, i, old);
      } else {
        r = clo + rnd() % (chi - clo + 1); i = rnd() % 320;
        if (kind < 8){ d = flip_cn(r, i); if (d <= 0 || (double)(rnd() % 1000000) / 1e6 < rt_expneg(-d / T)) cur += d; else flip_cn(r, i); }
        else { d = flip_dn(r, i); if (d <= 0 || (double)(rnd() % 1000000) / 1e6 < rt_expneg(-d / T)) cur += d; else flip_dn(r, i); }
      }
      if (cur < best){ best = cur; memcpy(btgt, tgt, sizeof tgt); memcpy(bcn, cn, sizeof cn); memcpy(bdn, dn, sizeof dn); }
    }
    memcpy(tgt, btgt, sizeof tgt); memcpy(cn, bcn, sizeof cn); memcpy(dn, bdn, sizeof dn);
    full_eval();
    if (total != best) fail("stage mismatch");
    if (!final && st+1 <= R-2){ for (int k = 0; k < 320; k++){ int p = pat[st+1][k], b = 0; for (int t = 0; t < 32; t++) if (COST[p][t] < COST[p][b]) b = t; tgt[st+1][k] = b; } }
    stage = 99; full_eval();
    rt_puts("stage "); rt_putl(st); rt_puts(" exact-total "); rt_putl(total/16); rt_puts("\n");
  }
  stage = 99; full_eval(); cur = total; best = total;
  /* exact coordinate-descent polish over all targets and complement bits */
  for (int sweep = 0; sweep < 20; sweep++){ long imp = 0;
    for (int r = 1; r < R-1; r++) for (int i = 0; i < 320; i++){ if (r == 1 && !full1[i]) continue;
      int old = tgt[r][i], bt = old; long bd = 0;
      for (int t = 0; t < 32; t++){ if (t == old) continue; long d = change_target(r, i, t); if (d < bd){ bd = d; bt = t; } change_target(r, i, old); }
      if (bt != old){ change_target(r, i, bt); imp += bd; } }
    for (int r = 2; r < R; r++) for (int i = 0; i < 320; i++){ long d = flip_cn(r, i); if (d < 0) imp += d; else flip_cn(r, i); d = flip_dn(r, i); if (d < 0) imp += d; else flip_dn(r, i); }
    if (!imp) break; }
  full_eval();
  rt_puts("final "); rt_putl(total/16); rt_puts("\n");
  rt_ofd = rt_create(argv[6]);
  rt_putsf("nr 6\nchained 1\n");
  if (nkeep) rt_putsf(keep);
  for (int r = nkeep ? 2 : 1; r < R-1; r++){ rt_putsf("T "); rt_putlf(r); rt_putc(' ');
    for (int i = 0; i < 320; i++){ int v = tgt[r][i]; rt_putc("0123456789abcdef"[v >> 4]); rt_putc("0123456789abcdef"[v & 15]); } rt_putc('\n'); }
  if (!nkeep) { rt_putsf("D 1 ");
  for (int i = 0; i < 320; i++){ int d = full1[i] == 2 ? CTD[pat1[i]][tgt[1][i]] : 0xFFFF; int lo = d & 255, hi = (d >> 8) & 255;
    rt_putc("0123456789abcdef"[lo >> 4]); rt_putc("0123456789abcdef"[lo & 15]); rt_putc("0123456789abcdef"[hi >> 4]); rt_putc("0123456789abcdef"[hi & 15]); }
  rt_putc('\n'); }
  for (int r = 2; r < R; r++) for (int kind = 0; kind < 2; kind++){ rt_putsf(kind ? "DN " : "CN "); rt_putlf(r); rt_putc(' ');
    for (int byte = 0; byte < 40; byte++){ int v = 0; for (int b = 0; b < 8; b++) v |= (kind ? dn[r][8*byte+b] : cn[r][8*byte+b]) << b; rt_putc("0123456789abcdef"[v >> 4]); rt_putc("0123456789abcdef"[v & 15]); } rt_putc('\n'); }
  rt_flush();
  return 0;
}
```

### np_plank.c

The d2be26f2 planner `np_plan.c` with the row-0 move (functions `kdelta`/`kflip`, option `K:<kmap>`). Pass 2 uses `np_plan.c` unchanged.

```c
/* Bounded staged simulated-annealing polarity planner (freestanding).
 * With K:<kmap> (pass 1) it also moves the row-0 constant bits: each move XORs one recorded mask into the round-1 row patterns.
 * usage: np_plank <plan-input> <iterations-per-stage> <T0> <seed> <next-weight> <plan-out> [K:<kmap> | <pass1-plan>] */
#include "rt.h"
static double rt_expneg(double x) { /* exp(x) for x <= 0 */
  if (x < -700) return 0; int n = 0; while (x < -0.5) { x *= 0.5; n++; }
  double t = 1, s = 1; for (int i = 1; i < 20; i++) { t *= x / i; s += t; }
  while (n--) s *= s; return s; }
static long rt_atol(const char *s) { long v = 0; int neg = 0; if (*s == '-') { neg = 1; s++; } while (*s >= '0' && *s <= '9') v = v * 10 + (*s++ - '0'); return neg ? -v : v; }
static double rt_atof(const char *s) { double v = 0, f = 1; int dot = 0; while (*s) { if (*s == '.') dot = 1; else { if (dot) { f /= 10; v += (*s - '0') * f; } else v = v * 10 + (*s - '0'); } s++; } return v; }
static char inbuf[65536];
static int COST[32][32], LAST[32], SRCL[320][5], SRCZ[320][5];
static int MINC[32];
static uint64_t RC[24];
static int base1[1600], full1[320], pat1[320]; static int CTC[160][32], CTD[160][32];
static int r1c(int i, int t){ if (full1[i] == 1) return COST[pat1[i]][t]; if (full1[i] == 2) return CTC[pat1[i]][t] == 255 ? 1000 : CTC[pat1[i]][t]; return 0; }
static int R; static int anymove=0;

static uint64_t rs = 88172645463325252ULL;
static uint64_t rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
// state
static int tgt[8][320], cn[8][320], dn[8][320];
static int out[8][1600], pc[8][320], pd[8][320], pat[8][320];
static int KN[320], KR[320][64], KM[320][64], kx[320], bkx[320], kmode=0; static char kbuf[200000];
static long kdelta(int b){ long d=0; for(int k=0;k<KN[b];k++){int i=KR[b][k]; int t=tgt[1][i]; int o=r1c(i,t); pat1[i]^=KM[b][k]; d+=16*(r1c(i,t)-o);} return d; }
static void kflip(int b){ for(int k=0;k<KN[b];k++) pat1[KR[b][k]]^=KM[b][k]; kx[b]^=1; }
static int dst_row[1600], dst_pos[1600]; // lane-bit (l,z) -> row,pos in next round chi
static long total;
static int stage = 99; static int WN = 16; // rounds <= stage use exact target cost; stage+1 uses MINC; later 0
static int rowcost(int r, int i){
  if (r > stage + 1) return 0;
  if (r == 1) return 16*r1c(i, tgt[1][i]);
  int w = (r == stage + 1) ? WN : 16;
  if (r == R-1) return w*(i < 64 ? LAST[pat[r][i]] : 0);
  if (r == stage + 1) return w*MINC[pat[r][i]];
  return 16*COST[pat[r][i]][tgt[r][i]];
}
static int calc_pat(int r, int i){
  int p = 0;
  for (int P = 0; P < 5; P++){ int l = SRCL[i][P], z = SRCZ[i][P]; p |= (out[r-1][64*l+z] ^ pd[r][64*(l%5)+z]) << P; }
  return p;
}
static void set_out_row(int r, int i){
  int y = i/64, z = i%64, t = tgt[r][i];
  for (int x = 0; x < 5; x++){ int l = x+5*y; out[r][64*l+z] = ((t>>x)&1) ^ (l==0 ? (int)((RC[r]>>z)&1) : 0); }
}
static void full_eval(void){
  memcpy(out[1], base1, sizeof base1);
  for (int i = 0; i < 320; i++) if (full1[i]) set_out_row(1, i);
  total = 0;
  for (int i = 0; i < 320; i++) total += rowcost(1, i);
  for (int r = 2; r < R; r++){
    for (int x = 0; x < 5; x++) for (int z = 0; z < 64; z++){ int v = cn[r][64*x+z]; for (int y = 0; y < 5; y++) v ^= out[r-1][64*(x+5*y)+z]; pc[r][64*x+z] = v; }
    for (int x = 0; x < 5; x++) for (int z = 0; z < 64; z++){ pd[r][64*x+z] = pc[r][64*((x+4)%5)+z] ^ pc[r][64*((x+1)%5)+((z+63)&63)] ^ dn[r][64*x+z]; if (r <= stage+1) total += 16*(cn[r][64*x+z] + dn[r][64*x+z]); }
    for (int i = 0; i < 320; i++){ pat[r][i] = calc_pat(r, i); total += rowcost(r, i); }
    if (r < R-1) for (int i = 0; i < 320; i++) set_out_row(r, i);
  }
}
// affected rows in round r (r>=2) by a pd flip at (X,z): lanes (X,y) bit z
static int aff[400], naff, mark[320], stamp = 1;
static void add_aff(int i){ if (mark[i] != stamp){ mark[i] = stamp; aff[naff++] = i; } }
static void pd_flip_rows(int r, int X, int z){ for (int y = 0; y < 5; y++) add_aff(dst_row[64*(X+5*y)+z]); }
// apply pd change at (X,z) in round r (toggle)
static void toggle_pd(int r, int X, int z){ pd[r][64*X+z] ^= 1; pd_flip_rows(r, X, z); }
static void toggle_pc(int r, int x, int z){ pc[r][64*x+z] ^= 1; toggle_pd(r, (x+1)%5, z); toggle_pd(r, (x+4)%5, (z+1)&63); }
// recompute affected rows' cost; returns delta
static long settle(int r){
  long d = 0;
  for (int k = 0; k < naff; k++){ int i = aff[k]; int old = rowcost(r, i); pat[r][i] = calc_pat(r, i); d += rowcost(r, i) - old; }
  return d;
}
// change target of (r,i) to t; returns delta; modifies state
static long change_target(int r, int i, int t){
  long d = -rowcost(r, i);
  int old[5]; int y = i/64, z = i%64;
  for (int x = 0; x < 5; x++) old[x] = out[r][64*(x+5*y)+z];
  tgt[r][i] = t; d += rowcost(r, i);
  set_out_row(r, i);
  if (r+1 < R){
    stamp++; naff = 0;
    for (int x = 0; x < 5; x++){ int l = x+5*y; if (out[r][64*l+z] != old[x]){ add_aff(dst_row[64*l+z]); toggle_pc(r+1, x, z); } }
    d += settle(r+1);
  }
  return d;
}
static long flip_cn(int r, int idx){ stamp++; naff = 0; cn[r][idx] ^= 1; long d = (r<=stage+1) ? (cn[r][idx] ? 16 : -16) : 0; toggle_pc(r, idx/64, idx%64); return d + settle(r); }
static long flip_dn(int r, int idx){ stamp++; naff = 0; dn[r][idx] ^= 1; long d = (r<=stage+1) ? (dn[r][idx] ? 16 : -16) : 0; toggle_pd(r, idx/64, idx%64); return d + settle(r); }
int main(int argc, char **argv){
  if (argc != 7 && argc != 8) fail("usage: np_plan input iters T0 seed weight out [pass1-plan]");
  long iters = rt_atol(argv[2]); double T0 = rt_atof(argv[3]); rs ^= (uint64_t)rt_atol(argv[4]) * 2654435761ULL; WN = (int)rt_atol(argv[5]);
  rt_read_file(argv[1], inbuf, sizeof inbuf - 1); rt_p = inbuf;
  R = (int)rt_long(); if (R != 6) fail("rounds");
  for (int p = 0; p < 32; p++) for (int t = 0; t < 32; t++) COST[p][t] = (int)rt_long();
  for (int p = 0; p < 32; p++) LAST[p] = (int)rt_long();
  for (int i = 0; i < 320; i++) for (int P = 0; P < 5; P++){ SRCL[i][P] = (int)rt_long(); SRCZ[i][P] = (int)rt_long(); }
  for (int i = 0; i < 24; i++) RC[i] = rt_ulong();
  for (int i = 0; i < 1600; i++) base1[i] = (int)rt_long();
  for (int i = 0; i < 320; i++){ full1[i] = (int)rt_long(); pat1[i] = (int)rt_long(); }
  for (int ty = 0; ty < 160; ty++){ for (int t = 0; t < 32; t++) CTC[ty][t] = (int)rt_long(); for (int t = 0; t < 32; t++) CTD[ty][t] = (int)rt_long(); }
  static char keep[4096]; int nkeep = 0;
  if (argc == 8 && argv[7][0]==75 && argv[7][1]==58){ kmode=1; rt_read_file(argv[7]+2, kbuf, sizeof kbuf - 1); rt_p=kbuf; for(int b=0;b<320;b++){KN[b]=(int)rt_long(); if(KN[b]>64) fail("kn"); for(int k=0;k<KN[b];k++){KR[b][k]=(int)rt_long(); KM[b][k]=(int)rt_long();}} rt_p=0; argc=7; }
  if (argc == 8){ /* pass 2: round 1 fixed at the actual polarities; keep the pass-1 round-1 plan lines */
    for (int i = 0; i < 320; i++) full1[i] = 0;
    rt_read_file(argv[7], inbuf, sizeof inbuf - 1);
    for (const char *q = inbuf; *q; ){ const char *e = q; while (*e && *e != '\n') e++;
      if ((q[0] == 'T' || q[0] == 'D') && q[1] == ' ' && q[2] == '1' && q[3] == ' '){ if (nkeep + (e - q) + 2 > (int)sizeof keep) fail("keep"); memcpy(keep + nkeep, q, (size_t)(e - q)); nkeep += (int)(e - q); keep[nkeep++] = '\n'; }
      q = *e ? e + 1 : e; }
    keep[nkeep] = 0; }
  for (int i = 0; i < 320; i++) for (int P = 0; P < 5; P++){ dst_row[64*SRCL[i][P]+SRCZ[i][P]] = i; dst_pos[64*SRCL[i][P]+SRCZ[i][P]] = P; }
  for (int p = 0; p < 32; p++){ MINC[p] = 99; for (int t = 0; t < 32; t++) if (COST[p][t] < MINC[p]) MINC[p] = COST[p][t]; }
  // greedy init
  for (int i = 0; i < 320; i++){ int b = 0; for (int t = 0; t < 32; t++) if (r1c(i, t) < r1c(i, b)) b = t; tgt[1][i] = b; }
  for (int r = 2; r < R-1; r++){ full_eval(); for (int i = 0; i < 320; i++){ int p = pat[r][i], b = 0; for (int t = 0; t < 32; t++) if (COST[p][t] < COST[p][b]) b = t; tgt[r][i] = b; } }
  full_eval();
  long cur, best;
  static int btgt[8][320], bcn[8][320], bdn[8][320];
  for (int st = 1; st <= R-2 + 1; st++){
    int final = (st == R-1);
    stage = final ? 99 : st;
    int rlo = final ? 1 : st, rhi = final ? R-2 : st;      // target rounds being moved
    int clo = final ? 2 : st+1, chi = final ? R-1 : st+1;   // cn/dn rounds being moved
    // greedy targets for round st+1 (used next stage) are set after
    full_eval(); cur = total; best = cur;
    memcpy(btgt, tgt, sizeof tgt); memcpy(bcn, cn, sizeof cn); memcpy(bdn, dn, sizeof dn);
    long N = final ? iters : iters;
    double T0s = final ? T0 * 0.2 : T0;
    for (long it = 0; it < N; it++){
      double T = 16*(T0s * rt_expneg(-5.5 * (double)it / N) + 0.03);
      int kind = rnd() % 10; long d; int r, i, old;
      if (kmode && rlo == 1 && (rnd() & 7) == 0){ int b = (int)(rnd() % 320); d = kdelta(b); if (d <= 0 || (double)(rnd() % 1000000) / 1e6 < rt_expneg(-d / T)){ cur += d; kx[b]^=1; } else { for(int k=0;k<KN[b];k++) pat1[KR[b][k]]^=KM[b][k]; }
        if (cur < best){ best = cur; memcpy(btgt, tgt, sizeof tgt); memcpy(bcn, cn, sizeof cn); memcpy(bdn, dn, sizeof dn); memcpy(bkx,kx,sizeof kx);} continue; }
      if (kind < 6){
        r = rlo + rnd() % (rhi - rlo + 1); i = rnd() % 320;
        if (r == 1 && !full1[i]) continue;
        old = tgt[r][i]; int t = old ^ (1 + (int)(rnd() % 31));
        d = change_target(r, i, t);
        if (d <= 0 || (double)(rnd() % 1000000) / 1e6 < rt_expneg(-d / T)) cur += d; else change_target(r, i, old);
      } else {
        r = clo + rnd() % (chi - clo + 1); i = rnd() % 320;
        if (kind < 8){ d = flip_cn(r, i); if (d <= 0 || (double)(rnd() % 1000000) / 1e6 < rt_expneg(-d / T)) cur += d; else flip_cn(r, i); }
        else { d = flip_dn(r, i); if (d <= 0 || (double)(rnd() % 1000000) / 1e6 < rt_expneg(-d / T)) cur += d; else flip_dn(r, i); }
      }
      if (cur < best){ best = cur; memcpy(btgt, tgt, sizeof tgt); memcpy(bcn, cn, sizeof cn); memcpy(bdn, dn, sizeof dn); memcpy(bkx,kx,sizeof kx); }
    }
    memcpy(tgt, btgt, sizeof tgt); memcpy(cn, bcn, sizeof cn); memcpy(dn, bdn, sizeof dn);
    for(int b=0;b<320;b++) if(kx[b]!=bkx[b]) kflip(b);
    full_eval();
    if (total != best) fail("stage mismatch");
    if (!final && st+1 <= R-2){ for (int k = 0; k < 320; k++){ int p = pat[st+1][k], b = 0; for (int t = 0; t < 32; t++) if (COST[p][t] < COST[p][b]) b = t; tgt[st+1][k] = b; } }
    stage = 99; full_eval();
    rt_puts("stage "); rt_putl(st); rt_puts(" exact-total "); rt_putl(total/16); rt_puts("\n");
  }
  stage = 99; full_eval(); cur = total; best = total;
  /* exact coordinate-descent polish over all targets and complement bits */
  for (int sweep = 0; sweep < 20; sweep++){ long imp = 0;
    for (int r = 1; r < R-1; r++) for (int i = 0; i < 320; i++){ if (r == 1 && !full1[i]) continue;
      int old = tgt[r][i], bt = old; long bd = 0;
      for (int t = 0; t < 32; t++){ if (t == old) continue; long d = change_target(r, i, t); if (d < bd){ bd = d; bt = t; } change_target(r, i, old); }
      if (bt != old){ change_target(r, i, bt); imp += bd; } }
    for (int r = 2; r < R; r++) for (int i = 0; i < 320; i++){ long d = flip_cn(r, i); if (d < 0) imp += d; else flip_cn(r, i); d = flip_dn(r, i); if (d < 0) imp += d; else flip_dn(r, i); }
    if (kmode) for (int b = 0; b < 320; b++){ long d = kdelta(b); if (d < 0){ kx[b]^=1; imp += d; } else for(int k=0;k<KN[b];k++) pat1[KR[b][k]]^=KM[b][k]; }
    if (!imp) break; }
  full_eval();
  rt_puts("final "); rt_putl(total/16); rt_puts("\n"); if (kmode){ static char kb[330]; for(int b=0;b<320;b++) kb[b]=(char)(48+kx[b]); kb[320]=10; kb[321]=0; rt_puts("KX "); rt_puts(kb); }
  rt_ofd = rt_create(argv[6]);
  rt_putsf("nr 6\nchained 1\n");
  if (nkeep) rt_putsf(keep);
  for (int r = nkeep ? 2 : 1; r < R-1; r++){ rt_putsf("T "); rt_putlf(r); rt_putc(' ');
    for (int i = 0; i < 320; i++){ int v = tgt[r][i]; rt_putc("0123456789abcdef"[v >> 4]); rt_putc("0123456789abcdef"[v & 15]); } rt_putc('\n'); }
  if (!nkeep) { rt_putsf("D 1 ");
  for (int i = 0; i < 320; i++){ int d = full1[i] == 2 ? CTD[pat1[i]][tgt[1][i]] : 0xFFFF; int lo = d & 255, hi = (d >> 8) & 255;
    rt_putc("0123456789abcdef"[lo >> 4]); rt_putc("0123456789abcdef"[lo & 15]); rt_putc("0123456789abcdef"[hi >> 4]); rt_putc("0123456789abcdef"[hi & 15]); }
  rt_putc('\n'); }
  for (int r = 2; r < R; r++) for (int kind = 0; kind < 2; kind++){ rt_putsf(kind ? "DN " : "CN "); rt_putlf(r); rt_putc(' ');
    for (int byte = 0; byte < 40; byte++){ int v = 0; for (int b = 0; b < 8; b++) v |= (kind ? dn[r][8*byte+b] : cn[r][8*byte+b]) << b; rt_putc("0123456789abcdef"[v >> 4]); rt_putc("0123456789abcdef"[v & 15]); } rt_putc('\n'); }
  rt_flush();
  return 0;
}
```

### np_ils2.c

```c
/* Iterated local search over the pass-2 polarity plan (freestanding).
 * Starts from an existing pass-2 plan, then repeats: random kick + full
 * coordinate descent over all targets and CN/DN bits; keeps improvements.
 * usage: np_ils <plan-input> <start-plan> <iters> <seed> <maxkick> <out> */
#include "rt.h"
static long rt_atol(const char *s) { long v = 0; int neg = 0; if (*s == '-') { neg = 1; s++; } while (*s >= '0' && *s <= '9') v = v * 10 + (*s++ - '0'); return neg ? -v : v; }
static char inbuf[65536];
static int COST[32][32], LAST[32], SRCL[320][5], SRCZ[320][5];
static int MINC[32];
static uint64_t RC[24];
static int base1[1600], full1[320], pat1[320]; static int CTC[160][32], CTD[160][32];
static int r1c(int i, int t){ if (full1[i] == 1) return COST[pat1[i]][t]; if (full1[i] == 2) return CTC[pat1[i]][t] == 255 ? 1000 : CTC[pat1[i]][t]; return 0; }
static int R;
static uint64_t rs = 88172645463325252ULL;
static uint64_t rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static int tgt[8][320], cn[8][320], dn[8][320];
static int out[8][1600], pc[8][320], pd[8][320], pat[8][320];
static int dst_row[1600], dst_pos[1600];
static long total;
static int stage = 99, WN = 16;
static int btgt[8][320], bcn[8][320], bdn[8][320];
static int rowcost(int r, int i){
  if (r > stage + 1) return 0;
  if (r == 1) return 16*r1c(i, tgt[1][i]);
  int w = (r == stage + 1) ? WN : 16;
  if (r == R-1) return w*(i < 64 ? LAST[pat[r][i]] : 0);
  if (r == stage + 1) return w*MINC[pat[r][i]];
  return 16*COST[pat[r][i]][tgt[r][i]];
}
static int calc_pat(int r, int i){
  int p = 0;
  for (int P = 0; P < 5; P++){ int l = SRCL[i][P], z = SRCZ[i][P]; p |= (out[r-1][64*l+z] ^ pd[r][64*(l%5)+z]) << P; }
  return p;
}
static void set_out_row(int r, int i){
  int y = i/64, z = i%64, t = tgt[r][i];
  for (int x = 0; x < 5; x++){ int l = x+5*y; out[r][64*l+z] = ((t>>x)&1) ^ (l==0 ? (int)((RC[r]>>z)&1) : 0); }
}
static void full_eval(void){
  memcpy(out[1], base1, sizeof base1);
  for (int i = 0; i < 320; i++) if (full1[i]) set_out_row(1, i);
  total = 0;
  for (int i = 0; i < 320; i++) total += rowcost(1, i);
  for (int r = 2; r < R; r++){
    for (int x = 0; x < 5; x++) for (int z = 0; z < 64; z++){ int v = cn[r][64*x+z]; for (int y = 0; y < 5; y++) v ^= out[r-1][64*(x+5*y)+z]; pc[r][64*x+z] = v; }
    for (int x = 0; x < 5; x++) for (int z = 0; z < 64; z++){ pd[r][64*x+z] = pc[r][64*((x+4)%5)+z] ^ pc[r][64*((x+1)%5)+((z+63)&63)] ^ dn[r][64*x+z]; if (r <= stage+1) total += 16*(cn[r][64*x+z] + dn[r][64*x+z]); }
    for (int i = 0; i < 320; i++){ pat[r][i] = calc_pat(r, i); total += rowcost(r, i); }
    if (r < R-1) for (int i = 0; i < 320; i++) set_out_row(r, i);
  }
}
static int aff[400], naff, mark[320], stamp = 1;
static void add_aff(int i){ if (mark[i] != stamp){ mark[i] = stamp; aff[naff++] = i; } }
static void pd_flip_rows(int r, int X, int z){ for (int y = 0; y < 5; y++) add_aff(dst_row[64*(X+5*y)+z]); }
static void toggle_pd(int r, int X, int z){ pd[r][64*X+z] ^= 1; pd_flip_rows(r, X, z); }
static void toggle_pc(int r, int x, int z){ pc[r][64*x+z] ^= 1; toggle_pd(r, (x+1)%5, z); toggle_pd(r, (x+4)%5, (z+1)&63); }
static long settle(int r){
  long d = 0;
  for (int k = 0; k < naff; k++){ int i = aff[k]; int old = rowcost(r, i); pat[r][i] = calc_pat(r, i); d += rowcost(r, i) - old; }
  return d;
}
static long change_target(int r, int i, int t){
  long d = -rowcost(r, i);
  int old[5]; int y = i/64, z = i%64;
  for (int x = 0; x < 5; x++) old[x] = out[r][64*(x+5*y)+z];
  tgt[r][i] = t; d += rowcost(r, i);
  set_out_row(r, i);
  if (r+1 < R){
    stamp++; naff = 0;
    for (int x = 0; x < 5; x++){ int l = x+5*y; if (out[r][64*l+z] != old[x]){ add_aff(dst_row[64*l+z]); toggle_pc(r+1, x, z); } }
    d += settle(r+1);
  }
  return d;
}
static long flip_cn(int r, int idx){ stamp++; naff = 0; cn[r][idx] ^= 1; long d = (r<=stage+1) ? (cn[r][idx] ? 16 : -16) : 0; toggle_pc(r, idx/64, idx%64); return d + settle(r); }
static long flip_dn(int r, int idx){ stamp++; naff = 0; dn[r][idx] ^= 1; long d = (r<=stage+1) ? (dn[r][idx] ? 16 : -16) : 0; toggle_pd(r, idx/64, idx%64); return d + settle(r); }
/* full coordinate descent: targets of rounds 2..R-2 and all CN/DN bits */
static long descent(void){
  long imp_all = 0;
  for (int sweep = 0; sweep < 60; sweep++){ long imp = 0;
    for (int r = 1; r < R-1; r++) for (int i = 0; i < 320; i++){
      int old = tgt[r][i], bt = old; long bd = 0;
      for (int t = 0; t < 32; t++){ if (t == old) continue; long d = change_target(r, i, t); if (d < bd){ bd = d; bt = t; } change_target(r, i, old); }
      if (bt != old){ change_target(r, i, bt); imp += bd; } }
    for (int r = 2; r < R; r++) for (int i = 0; i < 320; i++){ long d = flip_cn(r, i); if (d < 0) imp += d; else flip_cn(r, i); d = flip_dn(r, i); if (d < 0) imp += d; else flip_dn(r, i); }
    imp_all += imp;
    if (!imp) break; }
  return imp_all;
}
static char planbuf[65536];
static char keep[4096]; static int nkeep;
static void load_start(const char *path){
  long n = rt_read_file(path, planbuf, sizeof planbuf - 1);
  (void)n;
  int i = 0;
  while (planbuf[i]){
    int s = i; while (planbuf[i] && planbuf[i] != '\n') i++;
    int e = i; /* [s,e) line */
    if (e > s){
      char k0 = planbuf[s], k1 = s+1 < e ? planbuf[s+1] : 0, k2 = s+2 < e ? planbuf[s+2] : 0;
      int isT = (k0 == 'T' && k1 == ' '), isC = (k0 == 'C' && k1 == 'N' && k2 == ' '), isDn = (k0 == 'D' && k1 == 'N' && k2 == ' '), isD = (k0 == 'D' && k1 == ' ');
      if (isT || isC || isDn || isD){
        int p = s + (isT ? 2 : 3);
        int r = 0; while (p < e && planbuf[p] >= '0' && planbuf[p] <= '9') r = r*10 + (planbuf[p++]-'0');
        while (p < e && planbuf[p] == ' ') p++;
        if (isD){
          /* round-1 decisions are regenerated from CTD for the current targets */
        } else if (isT){
          int want = 320; int at = 0;
          while (p < e && at < want){ tgt[r][at++] = rt_hexval(planbuf[p])*16 + rt_hexval(planbuf[p+1]); p += 2; }
          if (at != want) fail("T width");
        } else {
          int bits[320]; int at = 0;
          while (p < e && at < 320){ int byte = rt_hexval(planbuf[p])*16 + rt_hexval(planbuf[p+1]); p += 2; for (int b = 0; b < 8; b++) bits[at++] = (byte >> b) & 1; }
          if (at != 320) fail("CN/DN width");
          for (int q = 0; q < 320; q++){ if (isC) cn[r][q] = bits[q]; else dn[r][q] = bits[q]; }
        }
      }
    }
    if (planbuf[i]) i++;
  }
}
/* pair-flip polish over the CN/DN bits of each round (bits 0..319 CN, 320..639 DN) */
static long bit_toggle(int r, int b){
  if (b < 320){ cn[r][b] ^= 1; toggle_pc(r, b/64, b%64); return (r <= stage+1) ? (cn[r][b] ? 16 : -16) : 0; }
  int idx = b - 320; dn[r][idx] ^= 1; toggle_pd(r, idx/64, idx%64); return (r <= stage+1) ? (dn[r][idx] ? 16 : -16) : 0;
}
static long pair_polish(void){
  long imp_all = 0;
  for (int sweep = 0; sweep < 6; sweep++){ long imp = 0;
    for (int r = 2; r < R; r++){
      for (int i = 0; i < 640; i++) for (int j = i+1; j < 640; j++){
        stamp++; naff = 0; long d = bit_toggle(r, i) + bit_toggle(r, j); d += settle(r);
        if (d < 0) imp += d;
        else { stamp++; naff = 0; bit_toggle(r, i); bit_toggle(r, j); settle(r); } } }
    imp_all += imp;
    if (!imp) break;
    descent(); }
  return imp_all;
}
static long triple_polish(int r){
  long imp = 0;
  for (int i = 0; i < 640; i++) for (int j = i+1; j < 640; j++) for (int k = j+1; k < 640; k++){
    stamp++; naff = 0; long d = bit_toggle(r, i) + bit_toggle(r, j) + bit_toggle(r, k); d += settle(r);
    if (d < 0) imp += d;
    else { stamp++; naff = 0; bit_toggle(r, i); bit_toggle(r, j); bit_toggle(r, k); settle(r); } }
  return imp;
}
/* cross pair polish: target change of round r row i (to any other value) combined
 * with one CN/DN bit flip in round cr; keeps the best combined improvement. */
static long cross_polish(int r, int cr){
  long imp = 0;
  for (int i = 0; i < 320; i++){
    int old = tgt[r][i];
    for (int t = 0; t < 32; t++){ if (t == old) continue;
      long d0 = change_target(r, i, t);
      long bd = 0; int bb = -1;
      for (int b = 0; b < 640; b++){
        stamp++; naff = 0; long d1 = bit_toggle(cr, b); d1 += settle(cr);
        long d = d0 + d1;
        if (d < bd){ bd = d; bb = b; }
        stamp++; naff = 0; bit_toggle(cr, b); settle(cr);
      }
      if (bb >= 0){ stamp++; naff = 0; bit_toggle(cr, bb); settle(cr); imp += bd; }
      else change_target(r, i, old);
    }
  }
  return imp;
}
int main(int argc, char **argv){
  if (argc != 7) fail("usage: np_ils plan-input start-plan iters seed maxkick out");
  long iters = rt_atol(argv[3]); rs ^= (uint64_t)rt_atol(argv[4]) * 2654435761ULL; int maxkick = (int)rt_atol(argv[5]);
  rt_read_file(argv[1], inbuf, sizeof inbuf - 1); rt_p = inbuf;
  R = (int)rt_long(); if (R != 6) fail("rounds");
  for (int p = 0; p < 32; p++) for (int t = 0; t < 32; t++) COST[p][t] = (int)rt_long();
  for (int p = 0; p < 32; p++) LAST[p] = (int)rt_long();
  for (int i = 0; i < 320; i++) for (int P = 0; P < 5; P++){ SRCL[i][P] = (int)rt_long(); SRCZ[i][P] = (int)rt_long(); }
  for (int i = 0; i < 24; i++) RC[i] = rt_ulong();
  for (int i = 0; i < 1600; i++) base1[i] = (int)rt_long();
  for (int i = 0; i < 320; i++){ full1[i] = (int)rt_long(); pat1[i] = (int)rt_long(); }
  for (int ty = 0; ty < 160; ty++){ for (int t = 0; t < 32; t++) CTC[ty][t] = (int)rt_long(); for (int t = 0; t < 32; t++) CTD[ty][t] = (int)rt_long(); }
  for (int i = 0; i < 320; i++) { /* keep full1: round 1 participates in the cost */ }
  for (int i = 0; i < 320; i++) for (int P = 0; P < 5; P++){ dst_row[64*SRCL[i][P]+SRCZ[i][P]] = i; dst_pos[64*SRCL[i][P]+SRCZ[i][P]] = P; }
  for (int p = 0; p < 32; p++){ MINC[p] = 99; for (int t = 0; t < 32; t++) if (COST[p][t] < MINC[p]) MINC[p] = COST[p][t]; }
  load_start(argv[2]);
  full_eval();
  long start = total;
  if (maxkick < -100){
    int code = -maxkick - 100; int rr = code / 10; int cr = code % 10;
    long st = total;
    long im = cross_polish(rr, cr); descent(); full_eval();
    rt_puts("cross T"); rt_putl(rr); rt_puts(" CN"); rt_putl(cr); rt_puts(" imp "); rt_putl(im/16);
    rt_puts(" "); rt_putl(st/16); rt_puts(" -> "); rt_putl(total/16); rt_puts("\n");
    iters = 0;
  } else if (maxkick < 0){
    int rr = -maxkick; long st = total;
    triple_polish(rr); descent(); full_eval();
    rt_puts("triple r"); rt_putl(rr); rt_puts(" "); rt_putl(st/16); rt_puts(" -> "); rt_putl(total/16); rt_puts("\n");
    iters = 0;
  } else {
  pair_polish(); full_eval();
  if (total != start){ rt_puts("pairpolish "); rt_putl(start/16); rt_puts(" -> "); rt_putl(total/16); rt_puts("\n"); start = total; }
  }
  long best = total;
  memcpy(btgt, tgt, sizeof tgt); memcpy(bcn, cn, sizeof cn); memcpy(bdn, dn, sizeof dn);
  rt_puts("start "); rt_putl(start/16); rt_puts("\n");
  for (long it = 0; it < iters; it++){
    int k = 1 + (int)(rnd() % (unsigned)maxkick);
    if ((rnd() & 15) == 0) k += (int)(rnd() % (unsigned)(4*maxkick)); /* occasional large kick */
    for (int m = 0; m < k; m++){
      int kind = (int)(rnd() % 4);
      if (kind == 0){ int r = 1 + (int)(rnd() % (unsigned)(R-2)); int i = (int)(rnd() % 320); int nv = (int)(rnd() % 32); change_target(r, i, nv); }
      else if (kind == 1) flip_cn(2 + (int)(rnd() % (unsigned)(R-2)), (int)(rnd() % 320));
      else if (kind == 2) flip_dn(2 + (int)(rnd() % (unsigned)(R-2)), (int)(rnd() % 320));
      else { int r = 1 + (int)(rnd() % (unsigned)(R-2)); int z = (int)(rnd() % 64);
        for (int y = 0; y < 5; y++){ int i = 64*y + z; int nv = (int)(rnd() % 32); change_target(r, i, nv); } }
    }
    full_eval();
    descent();
    full_eval();
    if (total <= best){
      if (total < best){ best = total; rt_puts("ils "); rt_putl(it); rt_puts(" best "); rt_putl(best/16); rt_puts("\n"); rt_flush(); }
      memcpy(btgt, tgt, sizeof tgt); memcpy(bcn, cn, sizeof cn); memcpy(bdn, dn, sizeof dn);
    } else {
      memcpy(tgt, btgt, sizeof tgt); memcpy(cn, bcn, sizeof cn); memcpy(dn, bdn, sizeof dn);
    }
  }
  full_eval();
  rt_puts("final "); rt_putl(total/16); rt_puts("\n");
  rt_ofd = rt_create(argv[6]);
  rt_putsf("nr 6\nchained 1\n");
  rt_putsf("T 1 ");
  for (int i = 0; i < 320; i++){ int v = tgt[1][i]; rt_putc("0123456789abcdef"[v >> 4]); rt_putc("0123456789abcdef"[v & 15]); } rt_putc('\n');
  rt_putsf("D 1 ");
  for (int i = 0; i < 320; i++){ int v = full1[i] == 1 ? 0xFFFF : CTD[pat1[i]][tgt[1][i]];
    rt_putc("0123456789abcdef"[(v >> 4) & 15]); rt_putc("0123456789abcdef"[v & 15]);
    rt_putc("0123456789abcdef"[(v >> 12) & 15]); rt_putc("0123456789abcdef"[(v >> 8) & 15]); } rt_putc('\n');
  for (int r = 2; r < R-1; r++){ rt_putsf("T "); rt_putlf(r); rt_putc(' ');
    for (int i = 0; i < 320; i++){ int v = tgt[r][i]; rt_putc("0123456789abcdef"[v >> 4]); rt_putc("0123456789abcdef"[v & 15]); } rt_putc('\n'); }
  for (int r = 2; r < R; r++) for (int kind = 0; kind < 2; kind++){ rt_putsf(kind ? "DN " : "CN "); rt_putlf(r); rt_putc(' ');
    for (int byte = 0; byte < 40; byte++){ int v = 0; for (int b = 0; b < 8; b++) v |= (kind ? dn[r][8*byte+b] : cn[r][8*byte+b]) << b; rt_putc("0123456789abcdef"[v >> 4]); rt_putc("0123456789abcdef"[v & 15]); } rt_putc('\n'); }
  rt_flush();
  return 0;
}
```

### np_pair.c

`np_pair.c` uses the `np_ils2.c` search core (parser, cost model, coordinate descent) with a new `main`: mode `sN` exhaustively tries every same-round target pair of round N (all ordered row pairs and all 32 by 32 target values), mode `aN` every adjacent-round pair (round N, round N+1), keeps the best joint change and repeats after a full coordinate descent, then writes the plan. Build with the command above; the recorded run is `np_pair plan_input2.txt plan3b.txt s1 plan4.txt`.

```c
/* Iterated local search over the pass-2 polarity plan (freestanding).
 * Starts from an existing pass-2 plan, then repeats: random kick + full
 * coordinate descent over all targets and CN/DN bits; keeps improvements.
 * usage: np_ils <plan-input> <start-plan> <iters> <seed> <maxkick> <out> */
#include "rt.h"
static long rt_atol(const char *s) { long v = 0; int neg = 0; if (*s == '-') { neg = 1; s++; } while (*s >= '0' && *s <= '9') v = v * 10 + (*s++ - '0'); return neg ? -v : v; }
static char inbuf[65536];
static int COST[32][32], LAST[32], SRCL[320][5], SRCZ[320][5];
static int MINC[32];
static uint64_t RC[24];
static int base1[1600], full1[320], pat1[320]; static int CTC[160][32], CTD[160][32];
static int r1c(int i, int t){ if (full1[i] == 1) return COST[pat1[i]][t]; if (full1[i] == 2) return CTC[pat1[i]][t] == 255 ? 1000 : CTC[pat1[i]][t]; return 0; }
static int R;
static uint64_t rs = 88172645463325252ULL;
static uint64_t rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static int tgt[8][320], cn[8][320], dn[8][320];
static int out[8][1600], pc[8][320], pd[8][320], pat[8][320];
static int dst_row[1600], dst_pos[1600];
static long total;
static int stage = 99, WN = 16;
static int btgt[8][320], bcn[8][320], bdn[8][320];
static int rowcost(int r, int i){
  if (r > stage + 1) return 0;
  if (r == 1) return 16*r1c(i, tgt[1][i]);
  int w = (r == stage + 1) ? WN : 16;
  if (r == R-1) return w*(i < 64 ? LAST[pat[r][i]] : 0);
  if (r == stage + 1) return w*MINC[pat[r][i]];
  return 16*COST[pat[r][i]][tgt[r][i]];
}
static int calc_pat(int r, int i){
  int p = 0;
  for (int P = 0; P < 5; P++){ int l = SRCL[i][P], z = SRCZ[i][P]; p |= (out[r-1][64*l+z] ^ pd[r][64*(l%5)+z]) << P; }
  return p;
}
static void set_out_row(int r, int i){
  int y = i/64, z = i%64, t = tgt[r][i];
  for (int x = 0; x < 5; x++){ int l = x+5*y; out[r][64*l+z] = ((t>>x)&1) ^ (l==0 ? (int)((RC[r]>>z)&1) : 0); }
}
static void full_eval(void){
  memcpy(out[1], base1, sizeof base1);
  for (int i = 0; i < 320; i++) if (full1[i]) set_out_row(1, i);
  total = 0;
  for (int i = 0; i < 320; i++) total += rowcost(1, i);
  for (int r = 2; r < R; r++){
    for (int x = 0; x < 5; x++) for (int z = 0; z < 64; z++){ int v = cn[r][64*x+z]; for (int y = 0; y < 5; y++) v ^= out[r-1][64*(x+5*y)+z]; pc[r][64*x+z] = v; }
    for (int x = 0; x < 5; x++) for (int z = 0; z < 64; z++){ pd[r][64*x+z] = pc[r][64*((x+4)%5)+z] ^ pc[r][64*((x+1)%5)+((z+63)&63)] ^ dn[r][64*x+z]; if (r <= stage+1) total += 16*(cn[r][64*x+z] + dn[r][64*x+z]); }
    for (int i = 0; i < 320; i++){ pat[r][i] = calc_pat(r, i); total += rowcost(r, i); }
    if (r < R-1) for (int i = 0; i < 320; i++) set_out_row(r, i);
  }
}
static int aff[400], naff, mark[320], stamp = 1;
static void add_aff(int i){ if (mark[i] != stamp){ mark[i] = stamp; aff[naff++] = i; } }
static void pd_flip_rows(int r, int X, int z){ for (int y = 0; y < 5; y++) add_aff(dst_row[64*(X+5*y)+z]); }
static void toggle_pd(int r, int X, int z){ pd[r][64*X+z] ^= 1; pd_flip_rows(r, X, z); }
static void toggle_pc(int r, int x, int z){ pc[r][64*x+z] ^= 1; toggle_pd(r, (x+1)%5, z); toggle_pd(r, (x+4)%5, (z+1)&63); }
static long settle(int r){
  long d = 0;
  for (int k = 0; k < naff; k++){ int i = aff[k]; int old = rowcost(r, i); pat[r][i] = calc_pat(r, i); d += rowcost(r, i) - old; }
  return d;
}
static long change_target(int r, int i, int t){
  long d = -rowcost(r, i);
  int old[5]; int y = i/64, z = i%64;
  for (int x = 0; x < 5; x++) old[x] = out[r][64*(x+5*y)+z];
  tgt[r][i] = t; d += rowcost(r, i);
  set_out_row(r, i);
  if (r+1 < R){
    stamp++; naff = 0;
    for (int x = 0; x < 5; x++){ int l = x+5*y; if (out[r][64*l+z] != old[x]){ add_aff(dst_row[64*l+z]); toggle_pc(r+1, x, z); } }
    d += settle(r+1);
  }
  return d;
}
static long flip_cn(int r, int idx){ stamp++; naff = 0; cn[r][idx] ^= 1; long d = (r<=stage+1) ? (cn[r][idx] ? 16 : -16) : 0; toggle_pc(r, idx/64, idx%64); return d + settle(r); }
static long flip_dn(int r, int idx){ stamp++; naff = 0; dn[r][idx] ^= 1; long d = (r<=stage+1) ? (dn[r][idx] ? 16 : -16) : 0; toggle_pd(r, idx/64, idx%64); return d + settle(r); }
/* full coordinate descent: targets of rounds 2..R-2 and all CN/DN bits */
static long descent(void){
  long imp_all = 0;
  for (int sweep = 0; sweep < 60; sweep++){ long imp = 0;
    for (int r = 1; r < R-1; r++) for (int i = 0; i < 320; i++){
      int old = tgt[r][i], bt = old; long bd = 0;
      for (int t = 0; t < 32; t++){ if (t == old) continue; long d = change_target(r, i, t); if (d < bd){ bd = d; bt = t; } change_target(r, i, old); }
      if (bt != old){ change_target(r, i, bt); imp += bd; } }
    for (int r = 2; r < R; r++) for (int i = 0; i < 320; i++){ long d = flip_cn(r, i); if (d < 0) imp += d; else flip_cn(r, i); d = flip_dn(r, i); if (d < 0) imp += d; else flip_dn(r, i); }
    imp_all += imp;
    if (!imp) break; }
  return imp_all;
}
static char planbuf[65536];
static char keep[4096]; static int nkeep;
static void load_start(const char *path){
  long n = rt_read_file(path, planbuf, sizeof planbuf - 1);
  (void)n;
  int i = 0;
  while (planbuf[i]){
    int s = i; while (planbuf[i] && planbuf[i] != '\n') i++;
    int e = i; /* [s,e) line */
    if (e > s){
      char k0 = planbuf[s], k1 = s+1 < e ? planbuf[s+1] : 0, k2 = s+2 < e ? planbuf[s+2] : 0;
      int isT = (k0 == 'T' && k1 == ' '), isC = (k0 == 'C' && k1 == 'N' && k2 == ' '), isDn = (k0 == 'D' && k1 == 'N' && k2 == ' '), isD = (k0 == 'D' && k1 == ' ');
      if (isT || isC || isDn || isD){
        int p = s + (isT ? 2 : 3);
        int r = 0; while (p < e && planbuf[p] >= '0' && planbuf[p] <= '9') r = r*10 + (planbuf[p++]-'0');
        while (p < e && planbuf[p] == ' ') p++;
        if (isD){
          /* round-1 decisions are regenerated from CTD for the current targets */
        } else if (isT){
          int want = 320; int at = 0;
          while (p < e && at < want){ tgt[r][at++] = rt_hexval(planbuf[p])*16 + rt_hexval(planbuf[p+1]); p += 2; }
          if (at != want) fail("T width");
        } else {
          int bits[320]; int at = 0;
          while (p < e && at < 320){ int byte = rt_hexval(planbuf[p])*16 + rt_hexval(planbuf[p+1]); p += 2; for (int b = 0; b < 8; b++) bits[at++] = (byte >> b) & 1; }
          if (at != 320) fail("CN/DN width");
          for (int q = 0; q < 320; q++){ if (isC) cn[r][q] = bits[q]; else dn[r][q] = bits[q]; }
        }
      }
    }
    if (planbuf[i]) i++;
  }
}
/* pair-flip polish over the CN/DN bits of each round (bits 0..319 CN, 320..639 DN) */
static long bit_toggle(int r, int b){
  if (b < 320){ cn[r][b] ^= 1; toggle_pc(r, b/64, b%64); return (r <= stage+1) ? (cn[r][b] ? 16 : -16) : 0; }
  int idx = b - 320; dn[r][idx] ^= 1; toggle_pd(r, idx/64, idx%64); return (r <= stage+1) ? (dn[r][idx] ? 16 : -16) : 0;
}
static long pair_polish(void){
  long imp_all = 0;
  for (int sweep = 0; sweep < 6; sweep++){ long imp = 0;
    for (int r = 2; r < R; r++){
      for (int i = 0; i < 640; i++) for (int j = i+1; j < 640; j++){
        stamp++; naff = 0; long d = bit_toggle(r, i) + bit_toggle(r, j); d += settle(r);
        if (d < 0) imp += d;
        else { stamp++; naff = 0; bit_toggle(r, i); bit_toggle(r, j); settle(r); } } }
    imp_all += imp;
    if (!imp) break;
    descent(); }
  return imp_all;
}
static long triple_polish(int r){
  long imp = 0;
  for (int i = 0; i < 640; i++) for (int j = i+1; j < 640; j++) for (int k = j+1; k < 640; k++){
    stamp++; naff = 0; long d = bit_toggle(r, i) + bit_toggle(r, j) + bit_toggle(r, k); d += settle(r);
    if (d < 0) imp += d;
    else { stamp++; naff = 0; bit_toggle(r, i); bit_toggle(r, j); bit_toggle(r, k); settle(r); } }
  return imp;
}
/* cross pair polish: target change of round r row i (to any other value) combined
 * with one CN/DN bit flip in round cr; keeps the best combined improvement. */
static long cross_polish(int r, int cr){
  long imp = 0;
  for (int i = 0; i < 320; i++){
    int old = tgt[r][i];
    for (int t = 0; t < 32; t++){ if (t == old) continue;
      long d0 = change_target(r, i, t);
      long bd = 0; int bb = -1;
      for (int b = 0; b < 640; b++){
        stamp++; naff = 0; long d1 = bit_toggle(cr, b); d1 += settle(cr);
        long d = d0 + d1;
        if (d < bd){ bd = d; bb = b; }
        stamp++; naff = 0; bit_toggle(cr, b); settle(cr);
      }
      if (bb >= 0){ stamp++; naff = 0; bit_toggle(cr, bb); settle(cr); imp += bd; }
      else change_target(r, i, old);
    }
  }
  return imp;
}
/* Exhaustive same-round and adjacent-round target-pair polish. */
static long best_same(int r, int *bi, int *ba, int *bj, int *bb){
  long bd = 0; *bi = -1; *bj = -1;
  for (int i = 0; i < 320; i++){
    if (r == 1 && !full1[i]) continue;
    int oi = tgt[r][i];
    for (int a = 0; a < 32; a++){ if (a == oi) continue;
      long d0 = change_target(r, i, a);
      for (int j = i+1; j < 320; j++){
        if (r == 1 && !full1[j]) continue;
        int oj = tgt[r][j];
        for (int b = 0; b < 32; b++){ if (b == oj) continue;
          long d = d0 + change_target(r, j, b);
          if (d < bd){ bd = d; *bi = i; *ba = a; *bj = j; *bb = b; }
          change_target(r, j, oj);
        }
      }
      change_target(r, i, oi);
    }
  }
  return bd;
}
static long best_adj(int r, int *bi, int *ba, int *bj, int *bb){
  long bd = 0; *bi = -1; *bj = -1;
  for (int i = 0; i < 320; i++){
    if (r == 1 && !full1[i]) continue;
    int oi = tgt[r][i];
    for (int a = 0; a < 32; a++){ if (a == oi) continue;
      long d0 = change_target(r, i, a);
      for (int j = 0; j < 320; j++){
        int oj = tgt[r+1][j];
        for (int b = 0; b < 32; b++){ if (b == oj) continue;
          long d = d0 + change_target(r+1, j, b);
          if (d < bd){ bd = d; *bi = i; *ba = a; *bj = j; *bb = b; }
          change_target(r+1, j, oj);
        }
      }
      change_target(r, i, oi);
    }
  }
  return bd;
}
static long polish_same(int r){
  long imp = 0;
  for (int it = 0; it < 500; it++){
    int i = 0, a = 0, j = 0, b = 0;
    long d = best_same(r, &i, &a, &j, &b);
    if (d >= 0) break;
    change_target(r, i, a); change_target(r, j, b); imp += d;
    descent(); full_eval();
    rt_puts("same r"); rt_putl(r); rt_puts(" imp "); rt_putl(d/16); rt_puts(" total "); rt_putl(total/16); rt_puts("\n"); rt_flush();
  }
  return imp;
}
static long polish_adj(int r){
  long imp = 0;
  for (int it = 0; it < 500; it++){
    int i = 0, a = 0, j = 0, b = 0;
    long d = best_adj(r, &i, &a, &j, &b);
    if (d >= 0) break;
    change_target(r, i, a); change_target(r+1, j, b); imp += d;
    descent(); full_eval();
    rt_puts("adj r"); rt_putl(r); rt_puts(" imp "); rt_putl(d/16); rt_puts(" total "); rt_putl(total/16); rt_puts("\n"); rt_flush();
  }
  return imp;
}
int main(int argc, char **argv){
  if (argc != 5) fail("usage: np_pair plan-input start-plan mode out");
  rt_read_file(argv[1], inbuf, sizeof inbuf - 1); rt_p = inbuf;
  R = (int)rt_long(); if (R != 6) fail("rounds");
  for (int p = 0; p < 32; p++) for (int t = 0; t < 32; t++) COST[p][t] = (int)rt_long();
  for (int p = 0; p < 32; p++) LAST[p] = (int)rt_long();
  for (int i = 0; i < 320; i++) for (int P = 0; P < 5; P++){ SRCL[i][P] = (int)rt_long(); SRCZ[i][P] = (int)rt_long(); }
  for (int i = 0; i < 24; i++) RC[i] = rt_ulong();
  for (int i = 0; i < 1600; i++) base1[i] = (int)rt_long();
  for (int i = 0; i < 320; i++){ full1[i] = (int)rt_long(); pat1[i] = (int)rt_long(); }
  for (int ty = 0; ty < 160; ty++){ for (int t = 0; t < 32; t++) CTC[ty][t] = (int)rt_long(); for (int t = 0; t < 32; t++) CTD[ty][t] = (int)rt_long(); }
  for (int i = 0; i < 320; i++) for (int P = 0; P < 5; P++){ dst_row[64*SRCL[i][P]+SRCZ[i][P]] = i; dst_pos[64*SRCL[i][P]+SRCZ[i][P]] = P; }
  for (int p = 0; p < 32; p++){ MINC[p] = 99; for (int t = 0; t < 32; t++) if (COST[p][t] < MINC[p]) MINC[p] = COST[p][t]; }
  load_start(argv[2]);
  full_eval();
  long start = total;
  const char *mode = argv[3];
  if (rt_streq(mode, "all")){
    for (int r = 1; r < R-1; r++){ polish_same(r); full_eval(); }
    for (int r = 1; r < R-2; r++){ polish_adj(r); full_eval(); }
  } else if (mode[0] == 's'){
    int r = mode[1] - '0';
    if (r < 1 || r > R-2) fail("same round");
    polish_same(r); full_eval();
  } else if (mode[0] == 'a'){
    int r = mode[1] - '0';
    if (r < 1 || r > R-3) fail("adj round");
    polish_adj(r); full_eval();
  } else fail("mode");
  rt_puts("start "); rt_putl(start/16); rt_puts("\n");
  rt_puts("final "); rt_putl(total/16); rt_puts("\n");
  rt_ofd = rt_create(argv[4]);
  rt_putsf("nr 6\nchained 1\n");
  rt_putsf("T 1 ");
  for (int i = 0; i < 320; i++){ int v = tgt[1][i]; rt_putc("0123456789abcdef"[v >> 4]); rt_putc("0123456789abcdef"[v & 15]); } rt_putc('\n');
  rt_putsf("D 1 ");
  for (int i = 0; i < 320; i++){ int v = full1[i] == 1 ? 0xFFFF : CTD[pat1[i]][tgt[1][i]];
    rt_putc("0123456789abcdef"[(v >> 4) & 15]); rt_putc("0123456789abcdef"[v & 15]);
    rt_putc("0123456789abcdef"[(v >> 12) & 15]); rt_putc("0123456789abcdef"[(v >> 8) & 15]); } rt_putc('\n');
  for (int r = 2; r < R-1; r++){ rt_putsf("T "); rt_putlf(r); rt_putc(' ');
    for (int i = 0; i < 320; i++){ int v = tgt[r][i]; rt_putc("0123456789abcdef"[v >> 4]); rt_putc("0123456789abcdef"[v & 15]); } rt_putc('\n'); }
  for (int r = 2; r < R; r++) for (int kind = 0; kind < 2; kind++){ rt_putsf(kind ? "DN " : "CN "); rt_putlf(r); rt_putc(' ');
    for (int byte = 0; byte < 40; byte++){ int v = 0; for (int b = 0; b < 8; b++) v |= (kind ? dn[r][8*byte+b] : cn[r][8*byte+b]) << b; rt_putc("0123456789abcdef"[v >> 4]); rt_putc("0123456789abcdef"[v & 15]); } rt_putc('\n'); }
  rt_flush();
  return 0;
}

```

### np_ils4.c

`np_ils4.c` is the exact two-column joint window optimizer of `np_col2.c` (targets, CN and DN of an adjacent column pair optimized jointly with the costs of every consuming row whose pattern touches the window) wrapped in a seeded kick-and-repair search: each iteration applies a random kick over rounds 1..4, repairs only the two touched output columns with the exact window optimizer, and accepts only a strict improvement of the model total, keeping the best plan. Build with the command above; the recorded run is `np_ils4 plan_input2.txt plan4.txt 75 4001 10 plan5.txt` (the plan copied to `start.txt`, as for the other passes).

```c
/* Exact joint TWO-column optimization: targets + CN + DN of two adjacent output
 * columns (zA, zB=zA+1) of round r, w.r.t. own row costs and every round-r1
 * consumer row whose pattern touches columns zA, zB or zC=zA+2.
 * Frame: phiA = pd[r1][.,zA], pcA = pc[r1][.,zA], phiB = pd[r1][.,zB],
 * pcB = pc[r1][.,zB] are free; targets enter per row as u = t ^ phi.
 * dnA[x] = phiA[x] ^ pcA[(x+4)%5] ^ pc_old[(x+1)%5,zA-1]
 * dnB[x] = phiB[x] ^ pcB[(x+4)%5] ^ pcA[(x+1)%5]
 * Consumers: A-only/B-only/C-only tables, one AB cross, one BC, up to two AC,
 * no ABC (asserted).  DP over 5 rows per (phi,cond) variant; terminals over
 * (pc, idx) with the couple tables joined in the final minimization.
 * np_ils4: seeded kick-and-repair search that uses this window optimizer.
 * usage: np_ils4 <plan-input> <start-plan> <iters> <seed> <maxkick> <out> */
#include "rt.h"
static long rt_atol(const char *s){ long v=0; int neg=0; if(*s=='-'){neg=1;s++;} while(*s>='0'&&*s<='9') v=v*10+(*s++-'0'); return neg?-v:v; }
static char inbuf[65536];
static int COST[32][32], LAST[32], SRCL[320][5], SRCZ[320][5];
static int MINC[32];
static uint64_t RC[24];
static int base1[1600], full1[320], pat1[320]; static int CTC[160][32], CTD[160][32];
static int r1c(int i, int t){ if (full1[i] == 1) return COST[pat1[i]][t]; if (full1[i] == 2) return CTC[pat1[i]][t] == 255 ? 1000 : CTC[pat1[i]][t]; return 0; }
static int R;
static int tgt[8][320], cn[8][320], dn[8][320];
static int out[8][1600], pc[8][320], pd[8][320], pat[8][320];
static int dst_row[1600], dst_pos[1600];
static long total;
static int rowcost(int r, int i){
  if (r == 1) return 16*r1c(i, tgt[1][i]);
  if (r == R-1) return 16*(i < 64 ? LAST[pat[r][i]] : 0);
  return 16*COST[pat[r][i]][tgt[r][i]];
}
static int calc_pat(int r, int i){
  int p = 0;
  for (int P = 0; P < 5; P++){ int l = SRCL[i][P], z = SRCZ[i][P]; p |= (out[r-1][64*l+z] ^ pd[r][64*(l%5)+z]) << P; }
  return p;
}
static void set_out_row(int r, int i){
  int y = i/64, z = i%64, t = tgt[r][i];
  for (int x = 0; x < 5; x++){ int l = x+5*y; out[r][64*l+z] = ((t>>x)&1) ^ (l==0 ? (int)((RC[r]>>z)&1) : 0); }
}
static void full_eval(void){
  memcpy(out[1], base1, sizeof base1);
  for (int i = 0; i < 320; i++) if (full1[i]) set_out_row(1, i);
  total = 0;
  for (int i = 0; i < 320; i++) total += rowcost(1, i);
  for (int r = 2; r < R; r++){
    for (int x = 0; x < 5; x++) for (int z = 0; z < 64; z++){ int v = cn[r][64*x+z]; for (int y = 0; y < 5; y++) v ^= out[r-1][64*(x+5*y)+z]; pc[r][64*x+z] = v; }
    for (int x = 0; x < 5; x++) for (int z = 0; z < 64; z++){ pd[r][64*x+z] = pc[r][64*((x+4)%5)+z] ^ pc[r][64*((x+1)%5)+((z+63)&63)] ^ dn[r][64*x+z]; total += 16*(cn[r][64*x+z] + dn[r][64*x+z]); }
    for (int i = 0; i < 320; i++){ pat[r][i] = calc_pat(r, i); total += rowcost(r, i); }
    if (r < R-1) for (int i = 0; i < 320; i++) set_out_row(r, i);
  }
}
static int aff[400], naff, mark[320], stamp = 1;
static void add_aff(int i){ if (mark[i] != stamp){ mark[i] = stamp; aff[naff++] = i; } }
static void pd_flip_rows(int r, int X, int z){ for (int y = 0; y < 5; y++) add_aff(dst_row[64*(X+5*y)+z]); }
static void toggle_pd(int r, int X, int z){ pd[r][64*X+z] ^= 1; pd_flip_rows(r, X, z); }
static void toggle_pc(int r, int x, int z){ pc[r][64*x+z] ^= 1; toggle_pd(r, (x+1)%5, z); toggle_pd(r, (x+4)%5, (z+1)&63); }
static long settle(int r){
  long d = 0;
  for (int k = 0; k < naff; k++){ int i = aff[k]; int old = rowcost(r, i); pat[r][i] = calc_pat(r, i); d += rowcost(r, i) - old; }
  return d;
}
static long change_target(int r, int i, int t){
  long d = -rowcost(r, i);
  int old[5]; int y = i/64, z = i%64;
  for (int x = 0; x < 5; x++) old[x] = out[r][64*(x+5*y)+z];
  tgt[r][i] = t; d += rowcost(r, i);
  set_out_row(r, i);
  if (r+1 < R){
    stamp++; naff = 0;
    for (int x = 0; x < 5; x++){ int l = x+5*y; if (out[r][64*l+z] != old[x]){ add_aff(dst_row[64*l+z]); toggle_pc(r+1, x, z); } }
    d += settle(r+1);
  }
  return d;
}
static long flip_cn(int r, int idx){ stamp++; naff = 0; cn[r][idx] ^= 1; long d = 16*(cn[r][idx] ? 1 : -1); toggle_pc(r, idx/64, idx%64); return d + settle(r); }
static long flip_dn(int r, int idx){ stamp++; naff = 0; dn[r][idx] ^= 1; long d = 16*(dn[r][idx] ? 1 : -1); toggle_pd(r, idx/64, idx%64); return d + settle(r); }
static long descent(void){
  long imp_all = 0;
  for (int sweep = 0; sweep < 60; sweep++){ long imp = 0;
    for (int r = 1; r < R-1; r++) for (int i = 0; i < 320; i++){
      int old = tgt[r][i], bt = old; long bd = 0;
      for (int t = 0; t < 32; t++){ if (t == old) continue; long d = change_target(r, i, t); if (d < bd){ bd = d; bt = t; } change_target(r, i, old); }
      if (bt != old){ change_target(r, i, bt); imp += bd; } }
    for (int r = 2; r < R; r++) for (int i = 0; i < 320; i++){ long d = flip_cn(r, i); if (d < 0) imp += d; else flip_cn(r, i); d = flip_dn(r, i); if (d < 0) imp += d; else flip_dn(r, i); }
    imp_all += imp;
    if (!imp) break; }
  return imp_all;
}
static char planbuf[65536];
static void load_start(const char *path){
  long n = rt_read_file(path, planbuf, sizeof planbuf - 1);
  (void)n;
  int i = 0;
  while (planbuf[i]){
    int s = i; while (planbuf[i] && planbuf[i] != '\n') i++;
    int e = i;
    if (e > s){
      char k0 = planbuf[s], k1 = s+1 < e ? planbuf[s+1] : 0, k2 = s+2 < e ? planbuf[s+2] : 0;
      int isT = (k0 == 'T' && k1 == ' '), isC = (k0 == 'C' && k1 == 'N' && k2 == ' '), isDn = (k0 == 'D' && k1 == 'N' && k2 == ' '), isD = (k0 == 'D' && k1 == ' ');
      if (isT || isC || isDn || isD){
        int p = s + (isT ? 2 : 3);
        int r = 0; while (p < e && planbuf[p] >= '0' && planbuf[p] <= '9') r = r*10 + (planbuf[p++]-'0');
        while (p < e && planbuf[p] == ' ') p++;
        if (isD){
        } else if (isT){
          int want = 320; int at = 0;
          while (p < e && at < want){ tgt[r][at++] = rt_hexval(planbuf[p])*16 + rt_hexval(planbuf[p+1]); p += 2; }
          if (at != want) fail("T width");
        } else {
          int bits[320]; int at = 0;
          while (p < e && at < 320){ int byte = rt_hexval(planbuf[p])*16 + rt_hexval(planbuf[p+1]); p += 2; for (int b = 0; b < 8; b++) bits[at++] = (byte >> b) & 1; }
          if (at != 320) fail("CN/DN width");
          for (int q = 0; q < 320; q++){ if (isC) cn[r][q] = bits[q]; else dn[r][q] = bits[q]; }
        }
      }
    }
    if (planbuf[i]) i++;
  }
}
static int rcbitv(int r, int z){ return (int)((RC[r] >> z) & 1); }

/* ---------- window machinery ---------- */
static int pcbit(int r1, int x, int z){ return pc[r1][64*x+z] & 1; }
static int pdbits(int r1, int x, int z){ return pd[r1][64*x+z] & 1; }
static long ccost(int r1, int j, int p){ return (r1 == R-1) ? (j < 64 ? 16L*LAST[p] : 0) : 16L*COST[p][tgt[r1][j]]; }

/* per-window tables (all in x16 op units) */
static int b1A[5][5][2], b1B[5][5][2];
static long KC[32];
static int haveC4, c4yoA, c4xA, c4yoB, c4xB; static long C4tab[2][2];
static int ng5, g5yo[3], g5x[3], g5b[3]; static long g5tab[3][2][2];
static int ng6, g6yo[3], g6x[3], g6b[3]; static long g6tab[3][2][2];

static int nca, caY[4], caX[4];
static int ncb, cbY[4], cbX[4];

static long eval_win2(int r, int zA){
  int r1 = r+1, zB = (zA+1)&63, zC = (zA+2)&63;
  long s = 0;
  for (int yo = 0; yo < 5; yo++) s += rowcost(r, 64*yo+zA) + rowcost(r, 64*yo+zB);
  for (int j = 0; j < 320; j++){
    int has = 0;
    for (int P = 0; P < 5; P++){ int zz = SRCZ[j][P]; if (zz == zA || zz == zB || zz == zC) has = 1; }
    if (has) s += ccost(r1, j, pat[r1][j]);
  }
  for (int x = 0; x < 5; x++) s += 16L*(cn[r1][64*x+zA] + dn[r1][64*x+zA] + cn[r1][64*x+zB] + dn[r1][64*x+zB]);
  return s;
}

static void prep_win2(int r, int zA){
  int r1 = r+1, zB = (zA+1)&63, zC = (zA+2)&63;
  for (int yo = 0; yo < 5; yo++) for (int x = 0; x < 5; x++){ b1A[yo][x][0] = b1A[yo][x][1] = 0; b1B[yo][x][0] = b1B[yo][x][1] = 0; }
  for (int q = 0; q < 32; q++) KC[q] = 0;
  haveC4 = 0; ng5 = 0; ng6 = 0;
  nca = 0; ncb = 0;
  for (int j = 0; j < 320; j++){
    int pa = -1, pb = -1, pcv = -1, cnt = 0;
    for (int P = 0; P < 5; P++){ int zz = SRCZ[j][P];
      if (zz == zA){ pa = P; cnt++; } else if (zz == zB){ pb = P; cnt++; } else if (zz == zC){ pcv = P; cnt++; } }
    if (cnt == 0) continue;
    int p0 = pat[r1][j];
    if (pa >= 0 && pb < 0 && pcv < 0){
      int l = SRCL[j][pa], x = l%5, yo = l/5;
      int flip = (l == 0) ? rcbitv(r, zA) : 0;
      for (int b = 0; b < 2; b++){ int patb = (p0 & ~(1<<pa)) | (((b ^ flip)&1) << pa); b1A[yo][x][b] += (int)ccost(r1, j, patb); }
    } else if (pb >= 0 && pa < 0 && pcv < 0){
      int l = SRCL[j][pb], x = l%5, yo = l/5;
      int flip = (l == 0) ? rcbitv(r, zB) : 0;
      for (int b = 0; b < 2; b++){ int patb = (p0 & ~(1<<pb)) | (((b ^ flip)&1) << pb); b1B[yo][x][b] += (int)ccost(r1, j, patb); }
    } else if (pcv >= 0 && pa < 0 && pb < 0){
      int l = SRCL[j][pcv], x = l%5;
      int g = (int)(((out[r][64*l+zC] ^ pc[r1][64*((x+4)%5)+zC] ^ dn[r1][64*x+zC]) & 1));
      int bi = (x+1)%5;
      for (int q = 0; q < 32; q++){ int patb = (p0 & ~(1<<pcv)) | ((((q>>bi)&1) ^ g) << pcv); KC[q] += ccost(r1, j, patb); }
    } else if (pa >= 0 && pb >= 0 && pcv < 0){
      if (haveC4) fail("two AB");
      haveC4 = 1; c4yoA = SRCL[j][pa]/5; c4xA = SRCL[j][pa]%5; c4yoB = SRCL[j][pb]/5; c4xB = SRCL[j][pb]%5;
      int flipA = (SRCL[j][pa] == 0) ? rcbitv(r, zA) : 0, flipB = (SRCL[j][pb] == 0) ? rcbitv(r, zB) : 0;
      for (int ba = 0; ba < 2; ba++) for (int bb = 0; bb < 2; bb++){
        int patb = (p0 & ~(1<<pa) & ~(1<<pb)) | (((ba ^ flipA)&1) << pa) | (((bb ^ flipB)&1) << pb);
        C4tab[ba][bb] = ccost(r1, j, patb);
      }
    } else if (pb >= 0 && pcv >= 0 && pa < 0){
      if (ng5 >= 3) fail("g5 overflow");
      int lb = SRCL[j][pb], lc = SRCL[j][pcv];
      g5yo[ng5] = lb/5; g5x[ng5] = lb%5; g5b[ng5] = (lc%5+1)%5;
      int flipB = (lb == 0) ? rcbitv(r, zB) : 0;
      int g = (int)(((out[r][64*lc+zC] ^ pc[r1][64*((lc%5+4)%5)+zC] ^ dn[r1][64*(lc%5)+zC]) & 1));
      for (int bb = 0; bb < 2; bb++) for (int q = 0; q < 2; q++){
        int patb = (p0 & ~(1<<pb) & ~(1<<pcv)) | (((bb ^ flipB)&1) << pb) | (((q ^ g)&1) << pcv);
        g5tab[ng5][bb][q] = ccost(r1, j, patb);
      }
      ng5++;
    } else if (pa >= 0 && pcv >= 0 && pb < 0){
      if (ng6 >= 3) fail("g6 overflow");
      int la = SRCL[j][pa], lc = SRCL[j][pcv];
      g6yo[ng6] = la/5; g6x[ng6] = la%5; g6b[ng6] = (lc%5+1)%5;
      int flipA = (la == 0) ? rcbitv(r, zA) : 0;
      int g = (int)(((out[r][64*lc+zC] ^ pc[r1][64*((lc%5+4)%5)+zC] ^ dn[r1][64*(lc%5)+zC]) & 1));
      for (int ba = 0; ba < 2; ba++) for (int q = 0; q < 2; q++){
        int patb = (p0 & ~(1<<pa) & ~(1<<pcv)) | (((ba ^ flipA)&1) << pa) | (((q ^ g)&1) << pcv);
        g6tab[ng6][ba][q] = ccost(r1, j, patb);
      }
      ng6++;
    } else {
      fail("triple consumer");
    }
  }
  if (haveC4){ caY[0] = c4yoA; caX[0] = c4xA; nca = 1; cbY[0] = c4yoB; cbX[0] = c4xB; ncb = 1; }
  for (int i = 0; i < ng5; i++){
    int f = -1;
    for (int k = 0; k < ncb; k++) if (cbY[k] == g5yo[i] && cbX[k] == g5x[i]) f = k;
    if (f < 0){ if (ncb >= 2) fail("ncb>2"); cbY[ncb] = g5yo[i]; cbX[ncb] = g5x[i]; ncb++; }
  }
  for (int i = 0; i < ng6; i++){
    int f = -1;
    for (int k = 0; k < nca; k++) if (caY[k] == g6yo[i] && caX[k] == g6x[i]) f = k;
    if (f < 0){ if (nca >= 3) fail("nca>3"); caY[nca] = g6yo[i]; caX[nca] = g6x[i]; nca++; }
  }
}
static int slotA(int yo, int x){ for (int k = 0; k < nca; k++) if (caY[k] == yo && caX[k] == x) return k; return -1; }
static int slotB(int yo, int x){ for (int k = 0; k < ncb; k++) if (cbY[k] == yo && cbX[k] == x) return k; return -1; }

static long ownA(int r, int zA, int yo, int t){ int i = 64*yo+zA; return (r == 1) ? 16L*r1c(i, t) : 16L*COST[pat[r][i]][t]; }

static const long INF = 1000000000000L;
static long dpAv[8][32], dpBv[4][32];
static int selA[32][8][5][32], selB[32][4][5][32];
static long AM[32][32][8], BMt[32][32][4];
static int POP16[32][32];
static int Wt[32][32];
static int shiftw(int w, int sh){ int r = 0; for (int x = 0; x < 5; x++) r |= ((w >> ((x+sh)%5)) & 1) << x; return r; }

static long ownAv[5][32], ownBv[5][32];

static void run_dpA(int condA, int phiA){
  long *dp = dpAv[condA];
  for (int s = 0; s < 32; s++) dp[s] = (s == 0) ? 0 : INF;
  for (int yo = 0; yo < 5; yo++){
    static long nd[32];
    for (int s = 0; s < 32; s++) nd[s] = INF;
    for (int s = 0; s < 32; s++){
      long base = dp[s]; if (base >= INF/2) continue;
      for (int u = 0; u < 32; u++){
        int ok = 1;
        for (int k = 0; k < nca; k++) if (caY[k] == yo && (((u >> caX[k]) & 1) != ((condA >> k) & 1))){ ok = 0; break; }
        if (!ok) continue;
        long c = ownAv[yo][u ^ phiA];
        for (int x = 0; x < 5; x++) if (b1A[yo][x][0] || b1A[yo][x][1]) c += b1A[yo][x][(u >> x) & 1];
        long v = base + c; int ns = s ^ u;
        if (v < nd[ns]){ nd[ns] = v; selA[phiA][condA][yo][ns] = (s<<5)|u; }
      }
    }
    for (int s = 0; s < 32; s++) dp[s] = nd[s];
  }
}
static void run_dpB(int condB, int phiB){
  long *dp = dpBv[condB];
  for (int s = 0; s < 32; s++) dp[s] = (s == 0) ? 0 : INF;
  for (int yo = 0; yo < 5; yo++){
    static long nd[32];
    for (int s = 0; s < 32; s++) nd[s] = INF;
    for (int s = 0; s < 32; s++){
      long base = dp[s]; if (base >= INF/2) continue;
      for (int u = 0; u < 32; u++){
        int ok = 1;
        for (int k = 0; k < ncb; k++) if (cbY[k] == yo && (((u >> cbX[k]) & 1) != ((condB >> k) & 1))){ ok = 0; break; }
        if (!ok) continue;
        long c = ownBv[yo][u ^ phiB];
        for (int x = 0; x < 5; x++) if (b1B[yo][x][0] || b1B[yo][x][1]) c += b1B[yo][x][(u >> x) & 1];
        long v = base + c; int ns = s ^ u;
        if (v < nd[ns]){ nd[ns] = v; selB[phiB][condB][yo][ns] = (s<<5)|u; }
      }
    }
    for (int s = 0; s < 32; s++) dp[s] = nd[s];
  }
}

/* ---------------- exact two-column window application ---------------- */
static long win2_apply(int r, int zA){
  int r1 = r+1, rB = (zA+1)&63, rcbA = rcbitv(r, zA), rcbB = rcbitv(r, rB), zm = (zA+63)&63;
  long oldc = eval_win2(r, zA);
  prep_win2(r, zA);
  for (int yo = 0; yo < 5; yo++) for (int t = 0; t < 32; t++){ ownAv[yo][t] = ownA(r, zA, yo, t); ownBv[yo][t] = ownA(r, rB, yo, t); }
  int pcOa[5]; for (int x = 0; x < 5; x++) pcOa[x] = pcbit(r1, (x+1)%5, zm);
  int ncondA = 1 << nca, ncondB = 1 << ncb;
  for (int phiA = 0; phiA < 32; phiA++){
    for (int condA = 0; condA < ncondA; condA++){
      run_dpA(condA, phiA);
      for (int pcA = 0; pcA < 32; pcA++){
        long dnAc = 0; for (int x = 0; x < 5; x++) dnAc += 16 * (((phiA >> x) & 1) ^ ((pcA >> ((x+4)%5)) & 1) ^ pcOa[x]);
        long b = INF;
        for (int idx = 0; idx < 32; idx++){
          long d = dpAv[condA][idx]; if (d >= INF/2) continue;
          long v = d + POP16[pcA][idx ^ phiA ^ (rcbA << 0)] + dnAc;
          if (v < b) b = v;
        }
        AM[phiA][pcA][condA] = b;
      }
    }
  }
  for (int phiB = 0; phiB < 32; phiB++){
    for (int condB = 0; condB < ncondB; condB++){
      run_dpB(condB, phiB);
      for (int pcB = 0; pcB < 32; pcB++){
        long b = INF;
        for (int idx = 0; idx < 32; idx++){
          long d = dpBv[condB][idx]; if (d >= INF/2) continue;
          long v = d + POP16[pcB][idx ^ phiB ^ (rcbB << 0)];
          if (v < b) b = v;
        }
        BMt[phiB][pcB][condB] = b + KC[pcB];
      }
    }
  }
  static long gammab[8][4][32];
  for (int condA = 0; condA < ncondA; condA++) for (int condB = 0; condB < ncondB; condB++) for (int pcB = 0; pcB < 32; pcB++){
    long g = 0;
    if (haveC4) g += C4tab[(condA>>0)&1][(condB>>0)&1];
    for (int i = 0; i < ng5; i++){ int sl = slotB(g5yo[i], g5x[i]); g += g5tab[i][(condB>>sl)&1][(pcB>>g5b[i])&1]; }
    for (int i = 0; i < ng6; i++){ int sl = slotA(g6yo[i], g6x[i]); g += g6tab[i][(condA>>sl)&1][(pcB>>g6b[i])&1]; }
    gammab[condA][condB][pcB] = g;
  }
  long bestv = oldc; int bpA = 0, bphiA = 0, bcondA = 0, bpB = 0, bphiB = 0, bcondB = 0;
  for (int pcA = 0; pcA < 32; pcA++){
    for (int condA = 0; condA < ncondA; condA++){
      long bv = INF; int bphi = 0, bpcb = 0, bcdb = 0;
      for (int condB = 0; condB < ncondB; condB++){
        for (int phiB = 0; phiB < 32; phiB++){
          const int *pop = POP16[phiB];
          for (int pcB = 0; pcB < 32; pcB++){
            long v = BMt[phiB][pcB][condB] + pop[Wt[pcB][pcA]] + gammab[condA][condB][pcB];
            if (v < bv){ bv = v; bphi = phiB; bpcb = pcB; bcdb = condB; }
          }
        }
      }
      if (bv >= INF/2) continue;
      for (int phiA = 0; phiA < 32; phiA++){
        long v = AM[phiA][pcA][condA] + bv;
        if (v < bestv){ bestv = v; bpA = pcA; bphiA = phiA; bcondA = condA; bphiB = bphi; bpB = bpcb; bcondB = bcdb; }
      }
    }
  }
  if (bestv >= oldc || bestv >= INF/2) return 0;
  run_dpA(bcondA, bphiA);
  run_dpB(bcondB, bphiB);
  long dnAc = 0; for (int x = 0; x < 5; x++) dnAc += 16 * (((bphiA >> x) & 1) ^ ((bpA >> ((x+4)%5)) & 1) ^ pcOa[x]);
  int bidxA = -1, bidxB = -1; long bb = INF;
  for (int idx = 0; idx < 32; idx++){
    long d = dpAv[bcondA][idx]; if (d >= INF/2) continue;
    long v = d + POP16[bpA][idx ^ bphiA ^ (rcbA << 0)] + dnAc;
    if (v < bb){ bb = v; bidxA = idx; }
  }
  bb = INF;
  for (int idx = 0; idx < 32; idx++){
    long d = dpBv[bcondB][idx]; if (d >= INF/2) continue;
    long v = d + POP16[bpB][idx ^ bphiB ^ (rcbB << 0)];
    if (v < bb){ bb = v; bidxB = idx; }
  }
  if (bidxA < 0 || bidxB < 0) return 0;
  int uA[5], uB[5];
  int s = bidxA;
  for (int yo = 4; yo >= 0; yo--){ int rec = selA[bphiA][bcondA][yo][s]; uA[yo] = rec & 31; s = rec >> 5; }
  if (s != 0) return 0;
  s = bidxB;
  for (int yo = 4; yo >= 0; yo--){ int rec = selB[bphiB][bcondB][yo][s]; uB[yo] = rec & 31; s = rec >> 5; }
  if (s != 0) return 0;
  int idxAc = 0, idxBc = 0; for (int yo = 0; yo < 5; yo++){ idxAc ^= uA[yo]; idxBc ^= uB[yo]; }
  if (idxAc != bidxA || idxBc != bidxB) return 0;
  long rp = 0;
  for (int yo = 0; yo < 5; yo++){
    rp += ownAv[yo][uA[yo] ^ bphiA] + ownBv[yo][uB[yo] ^ bphiB];
    for (int x = 0; x < 5; x++){ rp += (long)b1A[yo][x][(uA[yo]>>x)&1] + (long)b1B[yo][x][(uB[yo]>>x)&1]; }
  }
  rp += KC[bpB];
  if (haveC4) rp += C4tab[(uA[c4yoA]>>c4xA)&1][(uB[c4yoB]>>c4xB)&1];
  for (int i = 0; i < ng5; i++) rp += g5tab[i][(uB[g5yo[i]]>>g5x[i])&1][(bpB>>g5b[i])&1];
  for (int i = 0; i < ng6; i++) rp += g6tab[i][(uA[g6yo[i]]>>g6x[i])&1][(bpB>>g6b[i])&1];
  for (int x = 0; x < 5; x++) rp += 16 * (((bpA>>x)&1) ^ ((idxAc>>x)&1) ^ ((bphiA>>x)&1) ^ ((x==0)?rcbA:0));
  for (int x = 0; x < 5; x++) rp += 16 * (((bpB>>x)&1) ^ ((idxBc>>x)&1) ^ ((bphiB>>x)&1) ^ ((x==0)?rcbB:0));
  for (int x = 0; x < 5; x++){ rp += 16*(((bphiA>>x)&1) ^ ((bpA>>((x+4)%5))&1) ^ pcOa[x]); }
  for (int x = 0; x < 5; x++){ rp += 16*(((bphiB>>x)&1) ^ ((bpB>>((x+4)%5))&1) ^ ((bpA>>((x+1)%5))&1)); }
  if (rp != bestv) return 0;
  int tA[5], tB[5], cnA[5], cnB[5], dnA[5], dnB[5], sTA[5], sTB[5];
  for (int yo = 0; yo < 5; yo++){ tA[yo] = uA[yo] ^ bphiA; tB[yo] = uB[yo] ^ bphiB; }
  for (int x = 0; x < 5; x++){ sTA[x] = ((bidxA ^ bphiA) >> x) & 1; sTB[x] = ((bidxB ^ bphiB) >> x) & 1; }
  for (int x = 0; x < 5; x++){
    cnA[x] = ((bpA>>x)&1) ^ sTA[x] ^ (x==0 ? rcbA : 0);
    cnB[x] = ((bpB>>x)&1) ^ sTB[x] ^ (x==0 ? rcbB : 0);
    dnA[x] = ((bphiA>>x)&1) ^ ((bpA>>((x+4)%5))&1) ^ pcOa[x];
    dnB[x] = ((bphiB>>x)&1) ^ ((bpB>>((x+4)%5))&1) ^ ((bpA>>((x+1)%5))&1);
  }
  int sotA[5], sotB[5], socA[5], socB[5], sodA[5], sodB[5];
  for (int yo = 0; yo < 5; yo++){ sotA[yo] = tgt[r][64*yo+zA]; sotB[yo] = tgt[r][64*yo+rB]; tgt[r][64*yo+zA] = tA[yo]; tgt[r][64*yo+rB] = tB[yo]; }
  for (int x = 0; x < 5; x++){ socA[x] = cn[r1][64*x+zA]; socB[x] = cn[r1][64*x+rB]; sodA[x] = dn[r1][64*x+zA]; sodB[x] = dn[r1][64*x+rB];
    cn[r1][64*x+zA] = cnA[x]; cn[r1][64*x+rB] = cnB[x]; dn[r1][64*x+zA] = dnA[x]; dn[r1][64*x+rB] = dnB[x]; }
  long tot0 = total;
  full_eval();
  long newc = eval_win2(r, zA);
  if (newc != bestv || tot0 - total != oldc - bestv){
    for (int yo = 0; yo < 5; yo++){ tgt[r][64*yo+zA] = sotA[yo]; tgt[r][64*yo+rB] = sotB[yo]; }
    for (int x = 0; x < 5; x++){ cn[r1][64*x+zA] = socA[x]; cn[r1][64*x+rB] = socB[x]; dn[r1][64*x+zA] = sodA[x]; dn[r1][64*x+rB] = sodB[x]; }
    full_eval();
    rt_puts("reject r"); rt_putl(r); rt_puts(" z"); rt_putl(zA); rt_puts(" newc "); rt_putl(newc); rt_puts(" pred "); rt_putl(bestv); rt_puts("\n"); rt_flush();
    return 0;
  }
  return oldc - bestv;
}

/* ---------------- repair queue ---------------- */
#define QCAP 8192
static int qr[QCAP], qz[QCAP], qh, qt_, qfull;
static int inq[5][64];
static void markq(int r, int z){
  if (r < 1 || r > 4) return;
  z &= 63;
  if (inq[r][z]) return;
  if (qt_ >= QCAP - 8){ qfull = 1; return; }
  inq[r][z] = 1; qr[qt_] = r; qz[qt_] = z; qt_++;
}
static void markblock(int r, int z){
  markq(r, z-2); markq(r, z-1); markq(r, z); markq(r, z+1);
}
static long drainq(void){
  long imp = 0;
  while (qh < qt_){
    int r = qr[qh], z = qz[qh]; qh++;
    inq[r][z] = 0;
    long g = win2_apply(r, z);
    if (g > 0){ imp += g; markblock(r, z); }
  }
  qh = qt_ = 0;
  if (qfull){ qfull = 0; for (int r = 1; r <= 4; r++) for (int z = 0; z < 64; z++) markq(r, z); qh = qt_ = 0; imp += drainq(); }
  return imp;
}

static uint64_t rs = 88172645463325252ULL;
static uint64_t rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }

static int16_t btgt2[8][320], bcn2[8][320], bdn2[8][320];

int main(int argc, char **argv){
  if (argc != 7) fail("usage: np_ils4 plan-input start-plan iters seed maxkick out");
  long iters = rt_atol(argv[3]); rs ^= (uint64_t)rt_atol(argv[4]) * 2654435761ULL; int maxkick = (int)rt_atol(argv[5]);
  rt_read_file(argv[1], inbuf, sizeof inbuf - 1); rt_p = inbuf;
  R = (int)rt_long(); if (R != 6) fail("rounds");
  for (int p = 0; p < 32; p++) for (int t = 0; t < 32; t++) COST[p][t] = (int)rt_long();
  for (int p = 0; p < 32; p++) LAST[p] = (int)rt_long();
  for (int i = 0; i < 320; i++) for (int P = 0; P < 5; P++){ SRCL[i][P] = (int)rt_long(); SRCZ[i][P] = (int)rt_long(); }
  for (int i = 0; i < 24; i++) RC[i] = rt_ulong();
  for (int i = 0; i < 1600; i++) base1[i] = (int)rt_long();
  for (int i = 0; i < 320; i++){ full1[i] = (int)rt_long(); pat1[i] = (int)rt_long(); }
  for (int ty = 0; ty < 160; ty++){ for (int t = 0; t < 32; t++) CTC[ty][t] = (int)rt_long(); for (int t = 0; t < 32; t++) CTD[ty][t] = (int)rt_long(); }
  for (int i = 0; i < 320; i++) for (int P = 0; P < 5; P++){ dst_row[64*SRCL[i][P]+SRCZ[i][P]] = i; dst_pos[64*SRCL[i][P]+SRCZ[i][P]] = P; }
  for (int p = 0; p < 32; p++){ MINC[p] = 99; for (int t = 0; t < 32; t++) if (COST[p][t] < MINC[p]) MINC[p] = COST[p][t]; }
  for (int a = 0; a < 32; a++) for (int b = 0; b < 32; b++){ int w = a^b, c = 0; while (w){ c += w & 1; w >>= 1; } POP16[a][b] = 16*c; }
  for (int pB = 0; pB < 32; pB++) for (int pA = 0; pA < 32; pA++) Wt[pB][pA] = shiftw(pB, 4) ^ shiftw(pA, 1);
  load_start(argv[2]);
  full_eval();
  long start = total;
  rt_puts("start "); rt_putl(start/16); rt_puts("\n"); rt_flush();
  for (int r = 0; r < 8; r++) for (int i = 0; i < 320; i++){ btgt2[r][i] = tgt[r][i]; bcn2[r][i] = cn[r][i]; bdn2[r][i] = dn[r][i]; }
  long best = total;
  for (int it = 0; it < (int)iters; it++){
    int k = 1 + (int)(rnd() % (unsigned)maxkick);
    if ((rnd() & 15) == 0) k += (int)(rnd() % (unsigned)(4*maxkick));
    for (int m = 0; m < k; m++){
      int kind = (int)(rnd() % 5);
      if (kind == 0){ int r = 1 + (int)(rnd() % (unsigned)(R-2)); int i = (int)(rnd() % 320); int nv = (int)(rnd() % 32); change_target(r, i, nv); markblock(r, i%64); }
      else if (kind == 1){ int r = 2 + (int)(rnd() % (unsigned)(R-2)); int i = (int)(rnd() % 320); flip_cn(r, i); markblock(r-1, i%64); }
      else if (kind == 2){ int r = 2 + (int)(rnd() % (unsigned)(R-2)); int i = (int)(rnd() % 320); flip_dn(r, i); markblock(r-1, i%64); }
      else if (kind == 3){ int r = 1 + (int)(rnd() % (unsigned)(R-2)); int z = (int)(rnd() % 64);
        for (int y = 0; y < 5; y++){ int i = 64*y + z; change_target(r, i, (int)(rnd() % 32)); } markblock(r, z); }
      else { int r = 1 + (int)(rnd() % (unsigned)(R-2)); int i = (int)(rnd() % 320); change_target(r, i, tgt[r][i] ^ (1 + (int)(rnd() % 31))); markblock(r, i%64); }
    }
    full_eval();
    drainq();
    if (total < best){
      best = total;
      for (int r = 0; r < 8; r++) for (int i = 0; i < 320; i++){ btgt2[r][i] = tgt[r][i]; bcn2[r][i] = cn[r][i]; bdn2[r][i] = dn[r][i]; }
      rt_puts("ils "); rt_putl(it); rt_puts(" best "); rt_putl(best/16); rt_puts("\n"); rt_flush();
    } else {
      for (int r = 1; r < 8; r++) for (int i = 0; i < 320; i++){ tgt[r][i] = (int)btgt2[r][i]; cn[r][i] = (int)bcn2[r][i]; dn[r][i] = (int)bdn2[r][i]; }
      full_eval();
    }
  }
  full_eval();
  rt_puts("final "); rt_putl(total/16); rt_puts("\n");
  rt_ofd = rt_create(argv[6]);
  rt_putsf("nr 6\nchained 1\n");
  rt_putsf("T 1 ");
  for (int i = 0; i < 320; i++){ int v = tgt[1][i]; rt_putc("0123456789abcdef"[v >> 4]); rt_putc("0123456789abcdef"[v & 15]); } rt_putc('\n');
  rt_putsf("D 1 ");
  for (int i = 0; i < 320; i++){ int v = full1[i] == 1 ? 0xFFFF : CTD[pat1[i]][tgt[1][i]];
    rt_putc("0123456789abcdef"[(v >> 4) & 15]); rt_putc("0123456789abcdef"[v & 15]);
    rt_putc("0123456789abcdef"[(v >> 12) & 15]); rt_putc("0123456789abcdef"[(v >> 8) & 15]); } rt_putc('\n');
  for (int r = 2; r < R-1; r++){ rt_putsf("T "); rt_putlf(r); rt_putc(' ');
    for (int i = 0; i < 320; i++){ int v = tgt[r][i]; rt_putc("0123456789abcdef"[v >> 4]); rt_putc("0123456789abcdef"[v & 15]); } rt_putc('\n'); }
  for (int r = 2; r < R; r++) for (int kind = 0; kind < 2; kind++){ rt_putsf(kind ? "DN " : "CN "); rt_putlf(r); rt_putc(' ');
    for (int byte = 0; byte < 40; byte++){ int v = 0; for (int b = 0; b < 8; b++) v |= (kind ? dn[r][8*byte+b] : cn[r][8*byte+b]) << b; rt_putc("0123456789abcdef"[v >> 4]); rt_putc("0123456789abcdef"[v & 15]); } rt_putc('\n'); }
  rt_flush();
  return 0;
}
```

### np_ils6.c

`np_ils6.c` is the `np_ils4.c` listing above with three changes: `markblock` marks the repaired window `z-3..z+2` (six columns) instead of `z-2..z+1` (four), the acceptance test is `total <= best` so equal-cost moves are kept as a plateau drift (the `ils <i> best <v>` line prints on ties and on improvements), and after the loop the state is restored to the saved plan only if the final total differs from `best`, so the written plan is the last accepted (possibly tied) state. Both sources declare the state backups `btgt2`, `bcn2` and `bdn2` as `int16_t` (their values fit 0..31 and the CN/DN copies 0..1), which keeps the process image and hence the charged peak under 2^20. Build with the command above; the recorded runs are `np_ils6 pi2.txt plan5.txt 500 7001 10 drift7001.txt` (pass 6, from the pass-5 plan) `np_ils6 pi2.txt drift7001.txt 500 7002 10 drift7002.txt` (pass 7, from the pass-6 plan) and `np_ils6 pi2.txt drift7002.txt 500 7006 10 drift7006.txt` (pass 8, from the pass-7 plan; this is the selected plan).

### np_ils7.c

`np_ils7.c` is the `np_ils6.c` listing above with one hook: the plan writer is factored into `write_plan`, and after every accepted (non-increasing) move the current state is written to `<dumpdir>/acc_<iteration>.txt` by `dump_state`; the tool takes a seventh argument (the dump directory) so recorded runs also produce the equal-cost harvest. Added declarations and functions:

```
static char dumpbuf[600]; static int dumplen; static char pbuf[700];
static void write_plan(const char *path){
  rt_ofd = rt_create(path);
  rt_putsf("nr 6\nchained 1\n");
  rt_putsf("T 1 ");
  for (int i = 0; i < 320; i++){ int v = tgt[1][i]; rt_putc("0123456789abcdef"[v >> 4]); rt_putc("0123456789abcdef"[v & 15]); } rt_putc('\n');
  rt_putsf("D 1 ");
  for (int i = 0; i < 320; i++){ int v = full1[i] == 1 ? 0xFFFF : CTD[pat1[i]][tgt[1][i]];
    rt_putc("0123456789abcdef"[(v >> 4) & 15]); rt_putc("0123456789abcdef"[v & 15]);
    rt_putc("0123456789abcdef"[(v >> 12) & 15]); rt_putc("0123456789abcdef"[(v >> 8) & 15]); } rt_putc('\n');
  for (int r = 2; r < R-1; r++){ rt_putsf("T "); rt_putlf(r); rt_putc(' ');
    for (int i = 0; i < 320; i++){ int v = tgt[r][i]; rt_putc("0123456789abcdef"[v >> 4]); rt_putc("0123456789abcdef"[v & 15]); } rt_putc('\n'); }
  for (int r = 2; r < R; r++) for (int kind = 0; kind < 2; kind++){ rt_putsf(kind ? "DN " : "CN "); rt_putlf(r); rt_putc(' ');
    for (int byte = 0; byte < 40; byte++){ int v = 0; for (int b = 0; b < 8; b++) v |= (kind ? dn[r][8*byte+b] : cn[r][8*byte+b]) << b; rt_putc("0123456789abcdef"[v >> 4]); rt_putc("0123456789abcdef"[v & 15]); } rt_putc('\n'); }
  rt_flush();
}
static void dump_state(long it){
  int n = 0; for (int i = 0; i < dumplen; i++) pbuf[n++] = dumpbuf[i];
  pbuf[n++]='/'; pbuf[n++]='a'; pbuf[n++]='c'; pbuf[n++]='c'; pbuf[n++]='_';
  char b[24]; int i = 23; b[i] = 0; unsigned long u = (unsigned long)it; do { b[--i] = (char)('0' + u % 10); u /= 10; } while (u);
  for (; b[i]; i++) pbuf[n++] = b[i];
  pbuf[n++]='.'; pbuf[n++]='t'; pbuf[n++]='x'; pbuf[n++]='t'; pbuf[n++]=0;
  write_plan(pbuf);
}
```

`main` requires `argc == 8`, copies `argv[7]` into `dumpbuf` as the directory prefix, calls `dump_state(it)` on every accepted move, and ends with `write_plan(argv[6])`. The recorded runs are `np_ils7 pi2.txt drift8105.txt 6000 9206 10 drift9206.txt dump9206` (pass 13; `drift9206.txt` SHA-256 `c179ec0c9593d0d7a4ea7d67326cafbcc2f4c1290f568caf4496f7cda5b83044`) and `np_ils7 pi2.txt drift9206.txt 4000 9406 31 drift9406.txt dump9406` (pass 14; `dump9406/acc_3273.txt` and `acc_3301.txt`, SHA-256 `0b114a32ed91c9129207a51b227e14660f1f80af3b867773284a141c544c6ae3` and `75eb45ab0d3871c3fd7bf27d5a7336d766b413aaf56af8b610d99bd3f8d5e920`), and `np_ils7 pi2.txt drift9406_3301.txt 1000 9712 31 drift9712.txt dump9712` (pass 15; the selected plan is `dump9712/acc_20.txt`, SHA-256 `c06833ea87f90cba1cbec2ec91f30f9fd35d7ed701cbef089a3cfc0369c1bdfd`). Its memory image is 815535 bytes (text 23351, data 24, bss 792160), charged 1007451 bytes (passes 13 and 15) and 1012019 bytes (pass 14) with the stack reserve and the 60,844 or 65,412 retained bytes.

### chained_table.h

Entry `CHT[32*pattern+target] = {cost, subset, tricks, selected}` of the exhaustively verified chained-chi table; `LASTC` is the generic last-round row cost per input pattern used by the planner's model. The Python emitter rebuilds the table from scratch and checks its checksum.

```c
static const unsigned char CHT[1024][4]={{15,0,0,0},{13,20,0,16},{13,9,0,1},{12,9,1,0},{13,18,0,2},{13,4,16,0},{12,18,2,0},{13,9,5,4},{13,5,0,4},{13,1,4,0},{13,1,4,3},{12,1,5,2},{12,5,4,0},{12,4,20,8},{13,18,10,8},{13,1,1,6},{13,10,0,8},{12,20,16,0},{13,2,8,0},{13,20,18,2},{13,2,8,6},{12,16,18,1},{12,2,10,4},{13,16,16,3},{12,10,8,0},{13,10,9,1},{12,8,9,16},{13,8,8,17},{13,5,20,16},{13,4,4,24},{13,2,2,12},{14,3,2,20},{14,10,1,1},{13,10,0,0},{12,8,0,1},{11,8,1,0},{13,12,0,0},{14,5,16,0},{13,12,0,2},{12,8,5,4},{12,4,0,4},{12,0,4,0},{12,0,4,3},{11,0,5,2},{11,4,4,0},{12,0,2,4},{13,0,0,7},{12,0,1,6},{13,20,0,0},{13,10,0,16},{13,8,16,17},{14,24,1,8},{13,16,2,1},{13,16,2,0},{13,3,10,4},{13,16,1,2},{13,20,0,8},{13,2,4,18},{13,0,20,19},{13,2,4,16},{12,4,20,16},{13,16,2,8},{13,6,20,1},{13,2,2,20},{14,9,1,1},{13,9,0,0},{13,20,0,0},{13,20,0,1},{12,16,0,2},{13,16,1,3},{11,16,2,0},{14,17,2,16},{13,24,0,0},{13,1,4,2},{14,3,4,3},{13,1,4,0},{13,24,0,4},{13,6,20,8},{12,16,10,8},{13,1,2,4},{12,8,0,8},{13,9,0,16},{12,0,8,0},{13,4,8,5},{12,0,8,6},{13,0,9,7},{11,0,10,4},{13,4,8,1},{11,8,8,0},{12,8,9,1},{12,0,4,8},{13,1,4,16},{13,0,0,14},{13,12,9,2},{12,0,2,12},{13,1,2,20},{13,8,1,1},{12,8,0,0},{13,10,0,1},{12,10,1,0},{13,17,0,2},{13,8,4,4},{12,17,2,0},{13,16,2,16},{13,6,0,4},{12,0,4,2},{13,2,4,3},{12,0,4,0},{12,6,4,0},{13,0,0,6},{13,4,4,1},{12,0,2,4},{12,8,17,1},{12,8,0,16},{13,1,8,0},{14,0,8,16},{13,1,8,6},{13,8,4,20},{12,1,10,4},{13,16,2,0},{12,9,8,0},{12,0,4,18},{13,1,4,8},{12,0,4,16},{13,0,17,7},{13,0,0,22},{12,4,20,1},{12,0,2,20},{14,9,4,4},{12,16,0,16},{13,18,0,0},{13,18,0,1},{13,9,0,0},{12,0,16,0},{13,9,0,2},{13,8,16,10},{12,1,0,4},{12,0,16,12},{13,1,2,6},{13,0,18,14},{11,1,4,0},{11,0,20,8},{14,3,4,1},{13,8,16,2},{13,17,0,0},{11,16,16,0},{13,2,8,4},{12,16,18,2},{14,6,8,6},{12,0,8,16},{13,2,8,0},{13,2,8,1},{13,17,0,8},{13,0,0,28},{13,12,9,16},{13,24,18,4},{12,1,20,16},{12,0,4,24},{13,2,4,8},{13,2,4,9},{13,8,4,4},{13,17,0,16},{12,8,6,4},{12,12,1,0},{12,8,0,0},{13,1,16,0},{12,8,0,2},{13,8,1,2},{11,0,0,4},{13,1,16,12},{12,0,2,6},{12,4,5,2},{10,0,4,0},{12,1,20,8},{13,2,4,1},{13,2,4,0},{12,16,0,0},{12,17,16,0},{13,16,2,2},{13,17,18,2},{13,8,16,16},{13,1,8,16},{13,8,16,18},{14,3,8,1},{12,16,0,8},{14,1,0,28},{13,2,16,5},{14,2,0,20},{11,0,20,16},{13,1,4,24},{12,2,20,1},{13,2,4,16},{13,16,2,2},{12,16,3,2},{12,16,0,0},{12,16,0,1},{13,20,0,2},{13,2,16,0},{12,20,2,0},{14,0,16,1},{13,3,0,4},{13,2,16,12},{13,16,8,8},{13,16,8,9},{12,3,4,0},{12,2,20,8},{13,1,4,1},{13,1,4,0},{13,12,0,8},{12,18,16,0},{12,0,8,4},{12,0,8,5},{13,4,8,6},{13,2,8,16},{12,0,8,0},{12,0,8,1},{12,12,8,0},{13,0,3,14},{13,0,0,12},{13,0,0,13},{13,8,8,2},{12,8,9,2},{12,0,4,8},{12,0,4,9},{13,8,7,4},{13,12,0,0},{13,17,0,0},{13,17,0,1},{13,10,0,0},{14,8,0,2},{13,10,0,2},{14,8,0,0},{12,2,0,4},{13,4,4,2},{12,16,24,1},{13,0,0,4},{11,2,4,0},{13,3,20,8},{12,0,4,1},{12,0,4,0},{12,8,23,4},{13,12,0,16},{13,1,8,4},{13,1,8,5},{12,8,17,2},{14,8,0,18},{13,1,8,0},{13,1,8,1},{12,0,19,6},{13,4,4,18},{12,0,16,5},{13,0,0,20},{12,2,20,16},{13,9,9,2},{11,0,20,1},{12,0,4,16},{14,3,1,1},{13,3,0,0},{12,1,0,1},{11,1,1,0},{13,5,0,0},{13,4,16,8},{13,5,0,2},{12,1,5,4},{13,18,0,0},{14,9,4,0},{12,0,1,0},{12,0,16,1},{13,18,0,4},{13,4,16,0},{13,16,1,20},{13,4,16,2},{12,2,0,8},{13,3,0,16},{12,0,1,24},{13,0,0,25},{13,2,4,12},{13,24,18,1},{13,0,5,28},{13,17,5,8},{11,2,8,0},{12,2,9,1},{11,0,9,16},{12,0,8,17},{14,6,8,2},{13,4,8,16},{13,16,1,4},{13,4,8,18},{13,2,1,1},{12,2,0,0},{11,0,0,1},{10,0,1,0},{12,4,0,0},{13,2,4,4},{12,4,0,2},{11,0,5,4},{13,12,0,4},{13,8,4,0},{13,1,1,0},{12,8,5,2},{12,12,4,0},{13,8,2,4},{14,8,0,7},{13,8,1,6},{12,2,17,1},{12,2,0,16},{12,0,16,17},{13,16,1,8},{13,4,16,16},{13,2,4,20},{13,4,16,18},{12,16,5,8},{12,3,8,0},{13,2,8,16},{12,1,9,16},{13,1,8,17},{13,12,20,16},{14,5,8,16},{14,16,0,5},{13,16,1,4},{13,1,1,1},{12,1,0,0},{13,3,0,1},{12,3,1,0},{12,16,12,8},{13,1,4,4},{12,24,2,0},{13,3,5,4},{12,16,0,0},{13,16,1,1},{13,2,1,0},{13,2,16,1},{12,16,0,4},{13,16,1,5},{13,16,2,4},{14,6,16,2},{11,0,0,8},{12,1,0,16},{13,2,1,24},{14,2,0,25},{12,0,4,12},{13,1,4,20},{12,8,10,4},{14,4,0,9},{10,0,8,0},{11,0,9,1},{12,2,9,16},{13,2,8,17},{13,4,8,2},{12,4,9,2},{13,4,8,0},{13,4,8,1},{12,0,1,1},{11,0,0,0},{12,2,0,1},{11,2,1,0},{12,16,29,1},{12,0,4,4},{13,6,0,2},{12,2,5,4},{13,17,0,0},{13,8,4,2},{14,3,1,0},{13,8,4,0},{13,17,0,4},{14,8,0,6},{14,12,4,1},{13,8,2,4},{11,0,17,1},{11,0,0,16},{13,2,16,17},{14,18,1,8},{12,4,17,2},{12,0,4,20},{13,4,16,1},{13,0,6,20},{11,1,8,0},{12,0,8,16},{13,3,9,16},{13,8,4,16},{13,4,25,2},{13,5,9,2},{13,12,20,1},{13,8,2,20},{13,1,4,4},{13,24,0,16},{12,1,6,4},{12,5,1,0},{12,1,0,0},{12,0,16,8},{12,1,0,2},{12,0,16,10},{13,9,0,4},{13,8,16,12},{13,4,1,0},{13,4,16,1},{12,9,4,0},{12,0,16,0},{14,0,1,2},{12,0,16,2},{13,6,0,8},{12,24,16,0},{13,4,1,24},{13,0,6,28},{13,1,16,16},{13,0,0,24},{13,1,16,18},{13,0,0,26},{12,6,8,0},{13,16,16,4},{12,4,9,16},{12,16,18,4},{13,2,8,2},{12,0,8,16},{13,2,8,0},{12,0,8,18},{12,0,4,4},{13,6,0,0},{11,0,6,4},{11,4,1,0},{11,0,0,0},{13,1,16,8},{11,0,0,2},{12,0,1,2},{12,8,0,4},{14,9,16,12},{13,8,2,6},{13,12,5,2},{11,8,4,0},{13,1,16,0},{14,10,4,1},{13,1,16,2},{12,2,23,4},{13,6,0,16},{12,16,6,8},{13,16,7,8},{12,0,16,16},{14,1,0,24},{12,0,16,18},{13,20,5,8},{13,24,0,8},{14,6,8,16},{13,16,2,4},{13,17,18,4},{12,8,20,16},{13,1,8,16},{13,0,24,18},{13,1,8,18},{13,1,7,4},{12,16,15,8},{13,24,0,0},{13,24,0,1},{13,3,0,0},{13,2,16,8},{13,3,0,2},{13,2,16,10},{13,20,0,0},{12,16,3,4},{14,16,0,4},{14,16,0,5},{13,20,0,4},{13,2,16,0},{14,16,0,0},{13,2,16,2},{12,4,0,8},{12,0,7,12},{13,8,8,4},{13,8,8,5},{12,1,17,2},{12,0,1,10},{13,0,0,8},{13,0,0,9},{11,4,8,0},{12,4,9,1},{13,6,9,16},{13,18,18,4},{12,0,8,2},{11,0,9,2},{12,0,8,0},{12,0,8,1},{12,0,7,4},{12,4,0,0},{12,2,6,4},{12,6,1,0},{12,2,0,0},{13,0,0,2},{12,2,0,2},{13,0,0,0},{13,10,0,4},{13,17,3,4},{13,24,24,1},{14,8,0,4},{12,10,4,0},{14,3,16,0},{13,8,4,1},{13,8,4,0},{11,0,23,4},{12,4,0,16},{13,0,20,5},{14,0,4,20},{11,0,17,2},{13,0,0,18},{12,0,16,1},{13,0,0,16},{12,5,8,0},{13,4,8,16},{13,8,16,5},{14,8,0,20},{12,0,25,2},{12,1,9,2},{12,8,20,1},{13,1,8,1},{14,5,16,16},{12,4,0,16},{13,6,0,0},{13,6,0,1},{12,2,0,2},{12,0,2,17},{11,2,2,0},{13,0,0,19},{13,10,0,0},{13,4,8,24},{13,8,1,16},{13,17,5,2},{13,10,0,4},{13,0,10,25},{12,2,10,8},{13,3,10,16},{13,5,0,0},{11,4,16,0},{14,5,2,2},{12,4,18,2},{12,0,2,0},{11,0,18,1},{12,0,1,2},{12,0,16,3},{13,5,0,8},{14,12,16,4},{13,8,1,0},{13,8,16,1},{13,1,2,9},{13,1,2,8},{13,8,1,4},{13,1,1,10},{13,4,16,16},{13,5,0,16},{13,24,0,1},{12,24,1,0},{13,3,0,2},{13,1,2,17},{12,3,2,0},{13,2,2,16},{12,4,24,16},{13,16,4,0},{13,16,4,3},{12,16,5,2},{12,20,4,0},{13,2,8,18},{13,0,24,19},{12,2,10,16},{12,4,0,0},{12,5,16,0},{13,4,2,2},{13,8,1,8},{12,0,2,1},{12,0,2,0},{13,0,0,3},{12,0,1,2},{12,4,0,8},{14,0,4,8},{13,4,2,10},{13,8,1,0},{12,0,2,9},{12,0,2,8},{13,0,0,11},{12,0,1,10},{13,4,2,2},{12,4,3,2},{12,4,0,0},{12,4,0,1},{11,0,0,2},{12,0,1,3},{10,0,2,0},{13,1,2,16},{12,8,0,0},{13,8,1,1},{13,4,8,8},{13,4,8,9},{12,8,0,4},{13,1,8,18},{11,0,10,8},{12,1,10,16},{13,24,0,8},{12,6,16,0},{13,16,8,0},{13,4,16,1},{13,2,2,0},{12,2,18,1},{12,16,10,4},{13,1,2,0},{12,24,8,0},{13,24,9,1},{13,16,4,8},{14,10,16,1},{14,16,0,14},{14,1,0,10},{13,16,2,12},{13,1,2,8},{13,4,19,2},{13,24,0,0},{13,5,0,0},{13,5,0,1},{12,1,0,2},{12,8,12,16},{11,1,2,0},{12,0,2,16},{12,4,27,2},{13,16,4,2},{12,4,24,1},{13,4,8,16},{12,0,25,3},{12,0,8,18},{12,1,10,8},{11,0,10,16},{13,6,0,0},{13,24,0,16},{14,4,0,1},{14,4,0,0},{13,2,2,1},{13,0,0,2},{13,17,10,4},{12,0,2,0},{13,6,0,8},{13,16,4,18},{14,4,0,9},{13,16,4,16},{13,2,2,9},{13,0,0,10},{13,20,20,1},{12,0,2,8},{13,1,16,16},{11,0,0,16},{12,2,0,0},{12,2,0,1},{13,6,0,2},{13,4,2,17},{12,6,2,0},{14,4,0,19},{12,1,24,16},{12,0,8,24},{13,2,8,8},{13,2,8,9},{12,17,4,0},{12,16,20,8},{13,6,10,8},{14,8,0,18},{12,1,0,0},{10,0,16,0},{13,1,2,2},{11,0,18,2},{13,4,2,0},{12,4,18,1},{13,4,1,2},{13,4,16,3},{12,1,0,8},{13,8,16,4},{13,1,2,10},{12,8,18,4},{13,1,4,8},{13,8,16,0},{14,12,1,4},{13,8,16,2},{12,0,16,16},{12,1,0,16},{12,8,30,16},{13,3,0,1},{13,24,0,0},{14,5,2,17},{13,24,0,2},{14,6,2,16},{11,0,24,16},{13,1,8,24},{12,2,24,1},{13,2,8,16},{11,16,4,0},{13,17,20,8},{13,2,28,1},{13,6,10,16},{11,0,0,0},{11,1,16,0},{12,0,2,2},{12,1,18,2},{13,4,2,1},{13,4,2,0},{14,4,0,3},{13,4,1,2},{11,0,0,8},{14,9,16,4},{12,0,2,10},{13,0,3,10},{12,0,4,8},{13,4,2,8},{13,18,20,1},{13,4,1,10},{12,0,2,2},{11,0,3,2},{11,0,0,0},{11,0,0,1},{12,4,0,2},{13,4,1,3},{11,4,2,0},{14,5,2,16},{12,1,27,2},{12,8,3,4},{12,0,8,8},{12,0,8,9},{13,12,0,4},{13,8,1,2},{12,4,10,8},{13,0,12,9},{13,3,0,0},{11,2,16,0},{13,16,8,4},{12,0,16,1},{14,6,2,0},{13,6,18,1},{13,16,8,0},{13,16,8,1},{13,3,0,8},{13,8,19,4},{14,1,0,9},{13,10,18,4},{14,3,4,8},{13,24,9,2},{13,16,4,8},{13,16,4,9},{12,0,19,2},{12,1,3,2},{12,1,0,0},{12,1,0,1},{13,5,0,2},{13,12,12,16},{12,5,2,0},{13,4,2,16},{11,0,27,2},{13,0,10,18},{11,0,24,1},{12,0,8,16},{12,18,4,0},{13,4,8,18},{12,0,28,1},{12,4,10,16},{12,2,0,0},{12,3,16,0},{13,0,0,1},{13,0,0,0},{13,24,17,2},{14,4,0,2},{14,17,8,0},{13,4,2,0},{12,2,0,8},{14,0,2,10},{13,0,0,9},{13,0,0,8},{13,2,4,8},{14,4,0,10},{12,16,20,1},{13,4,2,8},{13,2,8,8},{13,12,0,16},{13,17,0,1},{12,17,1,0},{12,2,12,8},{13,8,2,17},{12,10,2,0},{13,0,12,25},{12,2,0,0},{13,2,1,1},{12,0,1,16},{13,0,0,17},{12,2,0,4},{13,2,1,5},{12,0,1,20},{13,0,0,21},{13,18,0,8},{12,12,16,0},{13,16,1,24},{13,1,1,8},{13,8,2,0},{12,8,18,1},{13,1,4,9},{12,1,5,8},{12,18,8,0},{13,4,16,4},{12,0,1,0},{12,0,16,1},{14,0,2,4},{13,4,16,0},{12,0,1,4},{12,0,16,5},{13,2,25,1},{13,18,0,0},{12,16,0,1},{11,16,1,0},{12,2,29,1},{12,2,12,16},{12,0,28,17},{12,16,5,4},{13,3,0,0},{14,2,0,16},{13,1,1,16},{13,24,5,2},{13,3,0,4},{14,2,0,20},{13,1,1,20},{13,10,10,16},{13,12,0,0},{13,18,0,16},{12,4,6,8},{12,0,1,8},{13,8,2,1},{13,2,4,8},{12,0,4,9},{11,0,5,8},{13,12,0,8},{14,2,0,0},{13,0,0,1},{12,0,1,0},{13,8,2,9},{13,8,2,8},{13,0,0,5},{12,0,1,4},{12,0,8,8},{12,4,15,8},{13,12,0,0},{13,12,0,1},{11,0,12,8},{12,1,12,16},{11,8,2,0},{13,1,14,16},{11,0,0,0},{12,0,1,1},{13,2,1,16},{14,2,0,17},{11,0,0,4},{12,0,1,5},{12,0,2,4},{13,9,10,16},{12,16,0,8},{13,17,0,16},{14,18,1,24},{14,3,1,8},{13,16,4,12},{13,1,4,8},{13,24,10,4},{13,3,5,8},{11,16,8,0},{12,16,9,1},{13,2,1,0},{13,2,16,1},{14,20,8,2},{13,0,17,5},{13,2,1,4},{13,2,16,5},{12,0,25,1},{12,16,0,0},{13,18,0,1},{12,18,1,0},{11,0,29,1},{11,0,12,16},{12,9,2,0},{12,0,14,16},{12,1,0,0},{13,0,0,16},{13,12,24,1},{14,12,8,16},{12,1,0,4},{13,0,0,20},{13,1,2,4},{12,8,10,16},{12,16,17,1},{12,16,0,16},{13,6,6,8},{13,2,1,8},{13,0,5,9},{12,0,4,8},{13,2,4,9},{12,2,5,8},{12,17,8,0},{13,0,0,0},{14,2,0,1},{13,2,1,0},{14,0,1,5},{13,0,0,4},{14,2,0,5},{13,2,1,4},{13,1,28,16},{12,8,0,16},{12,1,30,16},{12,0,14,24},{13,17,0,0},{13,16,16,8},{13,17,0,2},{13,16,16,10},{13,6,0,0},{12,2,3,4},{13,4,1,16},{12,0,2,20},{13,6,0,4},{13,0,0,16},{13,4,1,20},{13,0,0,18},{13,9,0,0},{11,8,16,0},{12,1,6,8},{12,8,18,2},{14,1,0,8},{13,12,18,1},{14,1,0,10},{13,5,5,8},{13,9,0,8},{12,0,16,4},{13,1,2,4},{11,0,18,4},{14,1,0,0},{12,0,16,0},{13,4,1,4},{12,0,16,2},{12,0,28,16},{13,9,0,16},{11,0,30,16},{12,20,1,0},{12,16,0,0},{13,6,12,16},{12,16,0,2},{13,16,1,2},{12,8,24,16},{13,3,3,4},{13,0,18,20},{13,1,2,20},{12,24,4,0},{14,1,0,16},{14,0,16,18},{14,1,0,18},{12,8,0,0},{12,9,16,0},{11,0,6,8},{12,0,7,8},{13,0,0,8},{14,6,4,8},{13,0,0,10},{12,4,5,8},{12,8,0,8},{13,1,16,4},{12,0,2,4},{12,1,18,4},{13,0,0,0},{13,1,16,0},{13,0,0,2},{13,1,16,2},{12,0,14,8},{11,0,15,8},{12,8,0,0},{12,8,0,1},{12,4,12,8},{13,0,9,10},{12,12,2,0},{14,0,8,9},{12,4,0,0},{11,0,3,4},{13,0,0,4},{13,0,0,5},{12,4,0,4},{12,0,1,2},{13,0,0,0},{13,0,0,1},{13,20,0,8},{12,10,16,0},{13,3,6,8},{13,8,16,1},{13,17,17,2},{13,16,1,10},{14,16,0,8},{14,16,0,9},{12,20,8,0},{12,0,19,4},{14,3,2,4},{12,2,18,4},{13,16,8,2},{12,16,9,2},{13,16,8,0},{13,2,16,2},{11,0,15,16},{12,0,14,16},{12,0,28,1},{13,9,0,1},{12,0,25,2},{12,4,12,16},{13,18,0,2},{13,4,14,16},{12,0,19,4},{12,1,3,4},{12,8,24,1},{13,8,8,16},{13,5,0,4},{13,1,1,2},{13,8,28,1},{13,12,10,16},{12,0,7,8},{13,20,0,16},{12,2,6,8},{13,2,7,8},{12,16,17,2},{13,4,4,8},{13,16,16,1},{13,6,5,8},{13,10,0,8},{13,1,19,4},{13,2,2,4},{13,3,18,4},{13,16,25,2},{13,17,9,2},{13,24,20,1},{14,3,16,2}};
static const int LASTC[32]={10,9,9,9,9,8,10,9,9,8,9,8,10,9,10,9,9,10,8,9,8,9,9,10,9,9,9,9,9,10,10,10};
```

### np_ctl.c

```c
/* Bounded emission of the assembled native8 controller (code and literal pool, link register 1931) and the 15-OR
 * prefilter.  The controller bytes are the fixed program text of the attack (charged as code memory); this phase only
 * writes them.  usage: np_ctl <controller-out> <prefilter-out> */
#include "rt.h"
static const unsigned char CTL[8512]={155,227,1,0,0,0,0,0,82,227,1,0,0,128,0,0,82,228,1,0,0,0,0,0,50,227,1,0,0,0,0,0,18,229,1,0,0,0,0,0,195,227,41,15,0,0,0,0,82,67,0,0,0,0,0,0,20,0,26,66,121,0,0,0,20,0,26,66,249,0,0,0,20,0,26,66,121,1,0,0,20,0,26,66,249,1,0,0,20,0,26,66,121,2,0,0,20,0,26,66,249,2,0,0,20,0,26,66,121,3,0,0,20,0,26,66,249,3,0,0,75,67,26,2,0,4,0,0,17,66,26,2,0,212,36,0,22,0,16,2,128,3,0,0,18,64,0,0,0,0,0,0,196,66,28,15,16,0,0,0,77,66,0,2,0,64,0,0,20,0,0,146,16,212,36,0,153,228,1,0,0,14,1,0,11,64,0,2,128,0,0,0,17,66,0,2,0,128,0,0,22,0,16,2,128,9,0,0,153,228,1,0,0,29,1,0,56,0,0,0,128,0,0,0,8,66,32,255,120,0,0,0,22,0,16,2,128,5,1,0,75,228,35,15,128,0,0,0,49,66,34,15,0,1,0,0,22,0,16,2,0,17,0,0,29,0,0,0,0,5,0,0,2,65,34,33,9,0,0,0,2,65,8,50,9,0,0,0,2,65,8,66,9,0,0,0,2,65,8,82,9,0,0,0,2,65,8,98,9,0,0,0,2,65,8,114,9,0,0,0,2,65,8,130,9,0,0,0,2,65,8,146,9,0,0,0,2,65,8,162,9,0,0,0,2,65,8,178,9,0,0,0,2,65,8,194,9,0,0,0,2,65,8,210,9,0,0,0,2,65,8,226,9,0,0,0,2,65,8,242,9,0,0,0,2,65,8,2,10,0,0,0,2,65,8,18,10,0,0,0,2,65,8,34,10,0,0,0,2,65,8,50,10,0,0,0,2,65,8,66,10,0,0,0,2,65,8,82,10,0,0,0,2,65,8,98,10,0,0,0,2,65,8,114,10,0,0,0,2,65,8,130,10,0,0,0,2,65,8,146,10,0,0,0,2,65,8,162,10,0,0,0,2,65,8,178,10,0,0,0,2,65,8,194,10,0,0,0,2,65,8,210,10,0,0,0,2,65,8,226,10,0,0,0,2,65,8,242,10,0,0,0,2,65,8,2,11,0,0,0,2,65,8,18,11,0,0,0,2,65,8,34,11,0,0,0,2,65,8,50,11,0,0,0,2,65,8,66,11,0,0,0,2,65,8,82,11,0,0,0,2,65,8,98,11,0,0,0,2,65,8,114,11,0,0,0,2,65,8,130,11,0,0,0,2,65,8,146,11,0,0,0,2,65,8,162,11,0,0,0,2,65,8,178,11,0,0,0,2,65,8,194,11,0,0,0,2,65,8,210,11,0,0,0,2,65,8,226,11,0,0,0,2,65,8,242,11,0,0,0,2,65,8,2,12,0,0,0,2,65,8,18,12,0,0,0,2,65,8,34,12,0,0,0,2,65,8,50,12,0,0,0,2,65,8,66,12,0,0,0,2,65,8,82,12,0,0,0,2,65,8,98,12,0,0,0,2,65,8,114,12,0,0,0,2,65,8,130,12,0,0,0,2,65,8,146,12,0,0,0,2,65,8,162,12,0,0,0,2,65,8,178,12,0,0,0,2,65,8,194,12,0,0,0,2,65,8,210,12,0,0,0,2,65,8,226,12,0,0,0,2,65,8,242,12,0,0,0,2,65,8,2,13,0,0,0,2,65,8,18,13,0,0,0,2,65,8,34,13,0,0,0,2,65,8,50,13,0,0,0,2,65,8,66,13,0,0,0,2,65,8,82,13,0,0,0,2,65,8,98,13,0,0,0,2,65,8,114,13,0,0,0,2,65,8,130,13,0,0,0,2,65,8,146,13,0,0,0,2,65,8,162,13,0,0,0,2,65,8,178,13,0,0,0,2,65,8,194,13,0,0,0,2,65,8,210,13,0,0,0,2,65,8,226,13,0,0,0,2,65,8,242,13,0,0,0,2,65,8,2,14,0,0,0,2,65,8,18,14,0,0,0,2,65,8,34,14,0,0,0,2,65,8,50,14,0,0,0,2,65,8,66,14,0,0,0,2,65,8,82,14,0,0,0,2,65,8,98,14,0,0,0,2,65,8,114,14,0,0,0,2,65,8,130,14,0,0,0,2,65,8,146,14,0,0,0,2,65,8,162,14,0,0,0,2,65,8,178,14,0,0,0,2,65,8,194,14,0,0,0,2,65,8,210,14,0,0,0,2,65,8,226,14,0,0,0,2,65,8,242,14,0,0,0,66,64,32,79,16,0,0,0,67,64,2,2,0,0,0,0,67,66,32,1,0,0,0,0,129,66,2,146,16,0,0,0,65,64,2,2,9,0,0,0,67,66,30,1,0,0,0,0,65,64,2,146,16,0,0,0,67,66,28,1,0,0,0,0,65,66,2,146,16,0,0,0,130,66,20,146,16,0,0,0,65,64,2,226,8,0,0,0,67,66,26,1,0,0,0,0,65,66,2,146,16,0,0,0,130,66,20,146,16,0,0,0,65,64,2,210,8,0,0,0,67,66,24,1,0,0,0,0,65,64,2,146,16,0,0,0,67,66,22,1,0,0,0,0,65,64,2,146,16,0,0,0,67,66,20,1,0,0,0,0,65,66,2,146,16,0,0,0,130,66,20,146,16,0,0,0,74,64,20,2,0,0,0,0,178,64,0,0,0,0,0,0,133,64,4,194,120,0,0,0,139,64,4,2,128,0,0,0,16,66,2,2,0,0,0,0,22,0,16,2,128,5,1,0,20,0,40,15,0,84,36,0,20,0,40,31,128,84,36,0,20,0,40,47,0,85,36,0,20,0,40,63,128,85,36,0,20,0,40,79,0,86,36,0,20,0,40,95,128,86,36,0,20,0,40,111,0,87,36,0,20,0,40,127,128,87,36,0,20,0,40,143,0,88,36,0,20,0,40,159,128,88,36,0,20,0,40,175,0,89,36,0,20,0,40,191,128,89,36,0,20,0,40,207,0,90,36,0,20,0,40,223,128,90,36,0,20,0,40,239,0,91,36,0,20,0,40,255,128,91,36,0,20,0,40,15,1,92,36,0,20,0,40,31,129,92,36,0,20,0,40,47,1,93,36,0,20,0,40,63,129,93,36,0,20,0,40,79,1,94,36,0,20,0,40,95,129,94,36,0,20,0,40,111,1,95,36,0,20,0,40,127,129,95,36,0,20,0,40,143,1,96,36,0,20,0,40,159,129,96,36,0,20,0,40,175,1,97,36,0,20,0,40,191,129,97,36,0,20,0,40,207,1,98,36,0,20,0,40,223,129,98,36,0,20,0,40,239,1,99,36,0,20,0,40,255,129,99,36,0,20,0,40,15,2,100,36,0,20,0,40,31,130,100,36,0,20,0,40,47,2,101,36,0,20,0,40,63,130,101,36,0,20,0,40,79,2,102,36,0,20,0,40,95,130,102,36,0,20,0,40,111,2,103,36,0,20,0,40,127,130,103,36,0,20,0,40,143,2,104,36,0,20,0,40,159,130,104,36,0,20,0,40,175,2,105,36,0,20,0,40,191,130,105,36,0,20,0,40,207,2,106,36,0,20,0,40,223,130,106,36,0,20,0,40,239,2,107,36,0,20,0,40,255,130,107,36,0,20,0,40,15,3,108,36,0,20,0,40,31,131,108,36,0,20,0,40,47,3,109,36,0,20,0,40,63,131,109,36,0,20,0,40,79,3,110,36,0,20,0,40,95,131,110,36,0,20,0,40,111,3,111,36,0,20,0,40,127,131,111,36,0,20,0,40,143,3,112,36,0,20,0,40,159,131,112,36,0,20,0,40,175,3,113,36,0,20,0,40,191,131,113,36,0,20,0,40,207,3,114,36,0,20,0,40,223,131,114,36,0,20,0,40,239,3,115,36,0,20,0,40,255,131,115,36,0,20,0,40,15,4,116,36,0,20,0,40,31,132,116,36,0,20,0,40,47,4,117,36,0,20,0,40,63,132,117,36,0,20,0,40,79,4,118,36,0,20,0,40,95,132,118,36,0,20,0,40,111,4,119,36,0,20,0,40,127,132,119,36,0,20,0,40,143,4,120,36,0,20,0,40,159,132,120,36,0,20,0,40,175,4,121,36,0,20,0,40,191,132,121,36,0,20,0,40,207,4,122,36,0,20,0,40,223,132,122,36,0,20,0,40,239,4,123,36,0,20,0,40,255,132,123,36,0,20,0,40,15,5,124,36,0,20,0,40,31,133,124,36,0,20,0,40,47,5,125,36,0,20,0,40,63,133,125,36,0,20,0,40,79,5,126,36,0,20,0,40,95,133,126,36,0,20,0,40,111,5,127,36,0,20,0,40,127,133,127,36,0,20,0,40,143,5,128,36,0,20,0,40,159,133,128,36,0,20,0,40,175,5,129,36,0,20,0,40,191,133,129,36,0,20,0,40,207,5,130,36,0,20,0,40,223,133,130,36,0,20,0,40,239,5,131,36,0,20,0,40,255,133,131,36,0,20,0,40,15,6,132,36,0,20,0,40,31,134,132,36,0,20,0,40,47,6,133,36,0,20,0,40,63,134,133,36,0,20,0,40,79,6,134,36,0,20,0,40,95,134,134,36,0,20,0,40,111,6,135,36,0,20,0,40,127,134,135,36,0,20,0,40,143,6,136,36,0,20,0,40,159,134,136,36,0,20,0,40,175,6,137,36,0,20,0,40,191,134,137,36,0,20,0,40,207,6,138,36,0,20,0,40,223,134,138,36,0,20,0,40,239,6,139,36,0,20,0,40,255,134,139,36,0,20,0,40,15,7,140,36,0,20,0,40,31,135,140,36,0,20,0,40,47,7,141,36,0,20,0,40,63,135,141,36,0,20,0,40,79,7,142,36,0,20,0,40,95,135,142,36,0,20,0,40,111,7,143,36,0,20,0,40,127,135,143,36,0,20,0,40,143,7,144,36,0,20,0,40,159,135,144,36,0,20,0,40,175,7,145,36,0,20,0,40,191,135,145,36,0,20,0,40,207,7,146,36,0,20,0,40,223,135,146,36,0,20,0,40,239,7,147,36,0,20,0,40,255,135,147,36,0,20,0,40,15,8,148,36,0,20,0,40,31,136,148,36,0,20,0,40,47,8,149,36,0,20,0,40,63,136,149,36,0,20,0,40,79,8,150,36,0,20,0,40,95,136,150,36,0,20,0,40,111,8,151,36,0,20,0,40,127,136,151,36,0,20,0,40,143,8,152,36,0,20,0,40,159,136,152,36,0,20,0,40,175,8,153,36,0,20,0,40,191,136,153,36,0,20,0,40,207,8,154,36,0,20,0,40,223,136,154,36,0,20,0,40,239,8,155,36,0,20,0,40,255,136,155,36,0,20,0,40,15,9,156,36,0,20,0,40,31,137,156,36,0,20,0,40,47,9,157,36,0,20,0,40,63,137,157,36,0,20,0,40,79,9,158,36,0,20,0,40,95,137,158,36,0,20,0,40,111,9,159,36,0,20,0,40,127,137,159,36,0,20,0,40,143,9,160,36,0,20,0,40,159,137,160,36,0,20,0,40,175,9,161,36,0,20,0,40,191,137,161,36,0,20,0,40,207,9,162,36,0,20,0,40,223,137,162,36,0,20,0,40,239,9,163,36,0,20,0,40,255,137,163,36,0,20,0,40,15,10,164,36,0,20,0,40,31,138,164,36,0,20,0,40,47,10,165,36,0,20,0,40,63,138,165,36,0,20,0,40,79,10,166,36,0,20,0,40,95,138,166,36,0,20,0,40,111,10,167,36,0,20,0,40,127,138,167,36,0,20,0,40,143,10,168,36,0,20,0,40,159,138,168,36,0,20,0,40,175,10,169,36,0,20,0,40,191,138,169,36,0,20,0,40,207,10,170,36,0,20,0,40,223,138,170,36,0,20,0,40,239,10,171,36,0,20,0,40,255,138,171,36,0,20,0,40,15,11,172,36,0,20,0,40,31,139,172,36,0,20,0,40,47,11,173,36,0,20,0,40,63,139,173,36,0,20,0,40,79,11,174,36,0,20,0,40,95,139,174,36,0,20,0,40,111,11,175,36,0,20,0,40,127,139,175,36,0,20,0,40,143,11,176,36,0,20,0,40,159,139,176,36,0,20,0,40,175,11,177,36,0,20,0,40,191,139,177,36,0,20,0,40,207,11,178,36,0,20,0,40,223,139,178,36,0,20,0,40,239,11,179,36,0,20,0,40,255,139,179,36,0,20,0,40,15,12,180,36,0,20,0,40,31,140,180,36,0,20,0,40,47,12,181,36,0,20,0,40,63,140,181,36,0,20,0,40,79,12,182,36,0,20,0,40,95,140,182,36,0,20,0,40,111,12,183,36,0,20,0,40,127,140,183,36,0,20,0,40,143,12,184,36,0,20,0,40,159,140,184,36,0,20,0,40,175,12,185,36,0,20,0,40,191,140,185,36,0,20,0,40,207,12,186,36,0,20,0,40,223,140,186,36,0,20,0,40,239,12,187,36,0,20,0,40,255,140,187,36,0,20,0,40,15,13,188,36,0,20,0,40,31,141,188,36,0,20,0,40,47,13,189,36,0,20,0,40,63,141,189,36,0,20,0,40,79,13,190,36,0,20,0,40,95,141,190,36,0,20,0,40,111,13,191,36,0,20,0,40,127,141,191,36,0,20,0,40,143,13,192,36,0,20,0,40,159,141,192,36,0,20,0,40,175,13,193,36,0,20,0,40,191,141,193,36,0,20,0,40,207,13,194,36,0,20,0,40,223,141,194,36,0,20,0,40,239,13,195,36,0,20,0,40,255,141,195,36,0,20,0,40,15,14,196,36,0,20,0,40,31,142,196,36,0,20,0,40,47,14,197,36,0,20,0,40,63,142,197,36,0,20,0,40,79,14,198,36,0,20,0,40,95,142,198,36,0,20,0,40,111,14,199,36,0,20,0,40,127,142,199,36,0,20,0,40,143,14,200,36,0,20,0,40,159,142,200,36,0,20,0,40,175,14,201,36,0,20,0,40,191,142,201,36,0,20,0,40,207,14,202,36,0,20,0,40,223,142,202,36,0,20,0,40,239,14,203,36,0,20,0,40,255,142,203,36,0,20,0,40,15,15,204,36,0,20,0,40,31,143,204,36,0,20,0,40,47,15,205,36,0,20,0,40,63,143,205,36,0,20,0,40,79,15,206,36,0,20,0,40,95,143,206,36,0,20,0,40,111,15,207,36,0,20,0,40,127,143,207,36,0,20,0,40,143,15,208,36,0,20,0,40,159,143,208,36,0,20,0,40,175,15,209,36,0,20,0,40,191,143,209,36,0,20,0,40,207,15,210,36,0,20,0,40,223,143,210,36,0,20,0,40,239,15,211,36,0,20,0,40,255,143,211,36,0,16,66,2,2,0,0,0,0,22,0,16,2,0,5,1,0,18,64,0,0,0,0,0,0,74,66,2,2,0,0,0,0,175,66,18,2,128,1,0,0,16,66,20,2,0,0,0,0,23,0,16,2,128,210,0,0,78,66,18,2,0,64,0,0,11,64,0,2,0,64,0,0,175,66,18,2,0,2,0,0,16,66,20,2,0,0,0,0,23,0,16,2,0,213,0,0,78,66,18,2,0,32,0,0,11,64,0,2,0,32,0,0,175,66,18,2,128,2,0,0,16,66,20,2,0,0,0,0,23,0,16,2,128,215,0,0,78,66,18,2,0,16,0,0,11,64,0,2,0,16,0,0,143,66,18,2,128,255,127,0,16,66,20,2,0,0,0,0,23,0,16,2,0,218,0,0,78,66,18,2,0,8,0,0,11,64,0,2,0,8,0,0,143,66,18,2,128,127,0,0,16,66,20,2,0,0,0,0,23,0,16,2,128,220,0,0,78,66,18,2,0,4,0,0,11,64,0,2,0,4,0,0,143,66,18,2,128,7,0,0,16,66,20,2,0,0,0,0,23,0,16,2,0,223,0,0,78,66,18,2,0,2,0,0,11,64,0,2,0,2,0,0,143,66,18,2,128,1,0,0,16,66,20,2,0,0,0,0,23,0,16,2,128,225,0,0,78,66,18,2,0,1,0,0,11,64,0,2,0,1,0,0,143,66,18,2,128,0,0,0,16,66,20,2,0,0,0,0,23,0,16,2,0,228,0,0,78,66,18,2,128,0,0,0,11,64,0,2,128,0,0,0,140,66,2,2,128,0,0,0,65,64,2,162,16,0,0,0,153,228,1,0,128,22,1,0,111,65,6,2,0,3,0,0,77,65,10,2,128,0,0,0,75,65,10,2,128,0,0,0,10,68,10,2,0,0,0,0,77,66,10,2,128,25,0,0,2,68,32,146,16,0,0,0,77,66,10,2,0,51,0,0,2,68,32,146,16,0,0,0,77,66,10,2,128,76,0,0,2,68,32,146,16,0,0,0,77,66,10,2,0,102,0,0,2,68,32,146,16,0,0,0,146,65,0,0,0,0,0,0,211,65,12,2,0,0,0,0,192,65,14,2,17,0,0,0,111,66,14,2,128,3,0,0,16,66,18,2,0,0,0,0,22,0,16,2,128,253,0,0,142,66,14,2,128,25,0,0,111,66,20,2,128,3,0,0,16,66,18,2,0,0,0,0,22,0,16,2,0,255,0,0,142,66,14,2,0,51,0,0,111,66,20,2,128,3,0,0,16,66,18,2,0,0,0,0,22,0,16,2,128,0,1,0,142,66,14,2,128,76,0,0,111,66,20,2,128,3,0,0,16,66,18,2,0,0,0,0,22,0,16,2,0,2,1,0,142,66,14,2,0,102,0,0,111,66,20,2,128,3,0,0,16,66,18,2,0,0,0,0,22,0,16,2,128,3,1,0,139,65,12,2,128,0,0,0,16,66,12,2,0,84,36,0,23,0,16,2,0,236,0,0,211,67,0,2,0,212,36,0,206,67,30,2,0,64,0,0,143,65,30,2,128,255,63,0,142,66,30,2,128,7,0,0,70,66,10,162,16,0,0,0,211,65,12,2,0,0,0,0,194,65,14,146,16,0,0,0,20,0,12,114,16,0,0,0,10,65,4,2,0,0,0,0,217,228,1,0,0,7,1,0,24,0,0,0,0,206,0,0,82,66,0,0,0,0,0,0,66,66,18,98,16,0,0,0,24,0,0,0,0,197,1,0,82,66,0,0,0,0,192,12,66,66,18,98,16,0,0,0,24,0,0,0,0,197,1,0,82,66,0,0,0,0,128,25,66,66,18,98,16,0,0,0,24,0,0,0,0,197,1,0,82,66,0,0,0,0,64,38,66,66,18,98,16,0,0,0,24,0,0,0,0,197,1,0,82,66,0,0,0,0,0,51,66,66,18,98,16,0,0,0,24,0,0,0,0,197,1,0,153,228,1,0,0,29,1,0,12,227,25,15,128,0,0,0,54,0,24,15,128,0,0,0,29,0,0,0,0,6,0,0,16,66,26,15,0,0,192,63,23,0,16,2,128,8,1,0,29,0,0,0,128,5,0,0,77,66,26,15,0,64,0,0,66,66,18,66,16,0,0,0,20,0,0,146,16,212,36,0,196,66,28,223,120,0,0,0,75,227,27,15,128,0,0,0,79,66,26,15,128,255,63,0,16,66,18,2,0,84,36,0,23,0,16,2,0,13,1,0,75,227,27,15,0,172,155,12,153,228,1,0,0,14,1,0,26,0,38,15,0,0,0,0,82,68,0,0,128,0,0,0,70,68,34,2,16,0,0,0,3,67,34,2,0,0,0,0,85,67,0,0,0,84,36,0,146,67,0,0,0,0,0,0,83,66,26,2,0,0,0,0,65,66,18,194,16,0,0,0,135,66,22,226,16,0,0,0,143,66,20,2,128,0,0,0,134,66,20,2,16,0,0,0,66,66,18,162,16,0,0,0,20,0,26,146,16,0,0,0,75,67,26,2,128,0,0,0,139,67,28,2,128,0,0,0,16,66,28,2,0,128,0,0,23,0,16,2,128,16,1,0,26,0,36,15,0,0,0,0,210,64,0,0,0,0,0,0,85,67,0,0,0,84,36,0,146,67,0,0,0,0,0,0,83,66,26,2,0,0,0,0,71,66,18,2,16,0,0,0,79,66,18,2,128,0,0,0,70,66,18,226,16,0,0,0,194,64,6,146,16,0,0,0,75,67,26,2,128,0,0,0,139,67,28,2,128,0,0,0,16,66,28,2,0,128,0,0,23,0,16,2,0,24,1,0,26,0,36,15,0,0,0,0,19,0,40,15,0,84,36,0,83,0,40,15,128,84,36,0,147,0,40,15,0,85,36,0,211,0,40,15,128,85,36,0,19,1,40,15,0,86,36,0,83,1,40,15,128,86,36,0,147,1,40,15,0,87,36,0,211,1,40,15,128,87,36,0,19,2,40,15,0,88,36,0,83,2,40,15,128,88,36,0,147,2,40,15,0,89,36,0,211,2,40,15,128,89,36,0,19,3,40,15,0,90,36,0,83,3,40,15,128,90,36,0,147,3,40,15,0,91,36,0,211,3,40,15,128,91,36,0,19,4,40,15,0,92,36,0,83,4,40,15,128,92,36,0,147,4,40,15,0,93,36,0,211,4,40,15,128,93,36,0,19,5,40,15,0,94,36,0,83,5,40,15,128,94,36,0,147,5,40,15,0,95,36,0,211,5,40,15,128,95,36,0,19,6,40,15,0,96,36,0,83,6,40,15,128,96,36,0,147,6,40,15,0,97,36,0,211,6,40,15,128,97,36,0,19,7,40,15,0,98,36,0,83,7,40,15,128,98,36,0,147,7,40,15,0,99,36,0,211,7,40,15,128,99,36,0,19,8,40,15,0,100,36,0,83,8,40,15,128,100,36,0,147,8,40,15,0,101,36,0,211,8,40,15,128,101,36,0,19,9,40,15,0,102,36,0,83,9,40,15,128,102,36,0,147,9,40,15,0,103,36,0,211,9,40,15,128,103,36,0,19,10,40,15,0,104,36,0,83,10,40,15,128,104,36,0,147,10,40,15,0,105,36,0,211,10,40,15,128,105,36,0,19,11,40,15,0,106,36,0,83,11,40,15,128,106,36,0,147,11,40,15,0,107,36,0,211,11,40,15,128,107,36,0,19,12,40,15,0,108,36,0,83,12,40,15,128,108,36,0,147,12,40,15,0,109,36,0,211,12,40,15,128,109,36,0,19,13,40,15,0,110,36,0,83,13,40,15,128,110,36,0,147,13,40,15,0,111,36,0,211,13,40,15,128,111,36,0,19,14,40,15,0,112,36,0,83,14,40,15,128,112,36,0,147,14,40,15,0,113,36,0,211,14,40,15,128,113,36,0,19,15,40,15,0,114,36,0,83,15,40,15,128,114,36,0,147,15,40,15,0,115,36,0,211,15,40,15,128,115,36,0,19,16,40,15,0,116,36,0,83,16,40,15,128,116,36,0,147,16,40,15,0,117,36,0,211,16,40,15,128,117,36,0,19,17,40,15,0,118,36,0,83,17,40,15,128,118,36,0,147,17,40,15,0,119,36,0,211,17,40,15,128,119,36,0,19,18,40,15,0,120,36,0,83,18,40,15,128,120,36,0,147,18,40,15,0,121,36,0,211,18,40,15,128,121,36,0,19,19,40,15,0,122,36,0,83,19,40,15,128,122,36,0,147,19,40,15,0,123,36,0,211,19,40,15,128,123,36,0,19,20,40,15,0,124,36,0,83,20,40,15,128,124,36,0,147,20,40,15,0,125,36,0,211,20,40,15,128,125,36,0,19,21,40,15,0,126,36,0,83,21,40,15,128,126,36,0,147,21,40,15,0,127,36,0,211,21,40,15,128,127,36,0,19,22,40,15,0,128,36,0,83,22,40,15,128,128,36,0,147,22,40,15,0,129,36,0,211,22,40,15,128,129,36,0,19,23,40,15,0,130,36,0,83,23,40,15,128,130,36,0,147,23,40,15,0,131,36,0,211,23,40,15,128,131,36,0,19,24,40,15,0,132,36,0,83,24,40,15,128,132,36,0,147,24,40,15,0,133,36,0,211,24,40,15,128,133,36,0,19,25,40,15,0,134,36,0,83,25,40,15,128,134,36,0,147,25,40,15,0,135,36,0,211,25,40,15,128,135,36,0,19,26,40,15,0,136,36,0,83,26,40,15,128,136,36,0,147,26,40,15,0,137,36,0,211,26,40,15,128,137,36,0,19,27,40,15,0,138,36,0,83,27,40,15,128,138,36,0,147,27,40,15,0,139,36,0,211,27,40,15,128,139,36,0,19,28,40,15,0,140,36,0,83,28,40,15,128,140,36,0,147,28,40,15,0,141,36,0,211,28,40,15,128,141,36,0,19,29,40,15,0,142,36,0,83,29,40,15,128,142,36,0,147,29,40,15,0,143,36,0,211,29,40,15,128,143,36,0,19,30,40,15,0,144,36,0,83,30,40,15,128,144,36,0,147,30,40,15,0,145,36,0,211,30,40,15,128,145,36,0,19,31,40,15,0,146,36,0,83,31,40,15,128,146,36,0,147,31,40,15,0,147,36,0,211,31,40,15,128,147,36,0,19,32,40,15,0,148,36,0,83,32,40,15,128,148,36,0,147,32,40,15,0,149,36,0,211,32,40,15,128,149,36,0,19,33,40,15,0,150,36,0,83,33,40,15,128,150,36,0,147,33,40,15,0,151,36,0,211,33,40,15,128,151,36,0,19,34,40,15,0,152,36,0,83,34,40,15,128,152,36,0,147,34,40,15,0,153,36,0,211,34,40,15,128,153,36,0,19,35,40,15,0,154,36,0,83,35,40,15,128,154,36,0,147,35,40,15,0,155,36,0,211,35,40,15,128,155,36,0,19,36,40,15,0,156,36,0,83,36,40,15,128,156,36,0,147,36,40,15,0,157,36,0,211,36,40,15,128,157,36,0,19,37,40,15,0,158,36,0,83,37,40,15,128,158,36,0,147,37,40,15,0,159,36,0,211,37,40,15,128,159,36,0,19,38,40,15,0,160,36,0,83,38,40,15,128,160,36,0,147,38,40,15,0,161,36,0,211,38,40,15,128,161,36,0,19,39,40,15,0,162,36,0,83,39,40,15,128,162,36,0,147,39,40,15,0,163,36,0,211,39,40,15,128,163,36,0,19,40,40,15,0,164,36,0,83,40,40,15,128,164,36,0,147,40,40,15,0,165,36,0,211,40,40,15,128,165,36,0,19,41,40,15,0,166,36,0,83,41,40,15,128,166,36,0,147,41,40,15,0,167,36,0,211,41,40,15,128,167,36,0,19,42,40,15,0,168,36,0,83,42,40,15,128,168,36,0,147,42,40,15,0,169,36,0,211,42,40,15,128,169,36,0,19,43,40,15,0,170,36,0,83,43,40,15,128,170,36,0,147,43,40,15,0,171,36,0,211,43,40,15,128,171,36,0,19,44,40,15,0,172,36,0,83,44,40,15,128,172,36,0,147,44,40,15,0,173,36,0,211,44,40,15,128,173,36,0,19,45,40,15,0,174,36,0,83,45,40,15,128,174,36,0,147,45,40,15,0,175,36,0,211,45,40,15,128,175,36,0,19,46,40,15,0,176,36,0,83,46,40,15,128,176,36,0,147,46,40,15,0,177,36,0,211,46,40,15,128,177,36,0,19,47,40,15,0,178,36,0,83,47,40,15,128,178,36,0,147,47,40,15,0,179,36,0,211,47,40,15,128,179,36,0,19,48,40,15,0,180,36,0,83,48,40,15,128,180,36,0,147,48,40,15,0,181,36,0,211,48,40,15,128,181,36,0,19,49,40,15,0,182,36,0,83,49,40,15,128,182,36,0,147,49,40,15,0,183,36,0,211,49,40,15,128,183,36,0,19,50,40,15,0,184,36,0,83,50,40,15,128,184,36,0,147,50,40,15,0,185,36,0,211,50,40,15,128,185,36,0,19,51,40,15,0,186,36,0,83,51,40,15,128,186,36,0,147,51,40,15,0,187,36,0,211,51,40,15,128,187,36,0,19,52,40,15,0,188,36,0,83,52,40,15,128,188,36,0,147,52,40,15,0,189,36,0,211,52,40,15,128,189,36,0,19,53,40,15,0,190,36,0,83,53,40,15,128,190,36,0,147,53,40,15,0,191,36,0,211,53,40,15,128,191,36,0,19,54,40,15,0,192,36,0,83,54,40,15,128,192,36,0,147,54,40,15,0,193,36,0,211,54,40,15,128,193,36,0,19,55,40,15,0,194,36,0,83,55,40,15,128,194,36,0,147,55,40,15,0,195,36,0,211,55,40,15,128,195,36,0,19,56,40,15,0,196,36,0,83,56,40,15,128,196,36,0,147,56,40,15,0,197,36,0,211,56,40,15,128,197,36,0,19,57,40,15,0,198,36,0,83,57,40,15,128,198,36,0,147,57,40,15,0,199,36,0,211,57,40,15,128,199,36,0,19,58,40,15,0,200,36,0,83,58,40,15,128,200,36,0,147,58,40,15,0,201,36,0,211,58,40,15,128,201,36,0,19,59,40,15,0,202,36,0,83,59,40,15,128,202,36,0,147,59,40,15,0,203,36,0,211,59,40,15,128,203,36,0,19,60,40,15,0,204,36,0,83,60,40,15,128,204,36,0,147,60,40,15,0,205,36,0,211,60,40,15,128,205,36,0,19,61,40,15,0,206,36,0,83,61,40,15,128,206,36,0,147,61,40,15,0,207,36,0,211,61,40,15,128,207,36,0,19,62,40,15,0,208,36,0,83,62,40,15,128,208,36,0,147,62,40,15,0,209,36,0,211,62,40,15,128,209,36,0,19,63,40,15,0,210,36,0,83,63,40,15,128,210,36,0,147,63,40,15,0,211,36,0,211,63,40,15,128,211,36,0,26,0,36,15,0,0,0,0,19,75,40,15,0,84,37,0,83,75,40,15,128,84,37,0,147,75,40,15,0,85,37,0,211,75,40,15,128,85,37,0,19,76,40,15,0,86,37,0,83,76,40,15,128,86,37,0,147,76,40,15,0,87,37,0,0,75,88,226,17,0,0,0,175,72,60,2,0,2,0,0,206,72,60,2,0,32,0,0,239,72,70,2,0,2,0,0,14,73,60,2,0,64,0,0,47,73,72,2,0,2,0,0,78,73,60,2,0,96,0,0,141,73,68,2,0,14,0,0,142,72,68,2,0,18,0,0,130,72,68,98,18,0,0,0,141,73,70,2,128,17,0,0,206,72,70,2,128,14,0,0,194,72,70,98,18,0,0,0,141,73,72,2,0,2,0,0,14,73,72,2,0,30,0,0,2,73,72,98,18,0,0,0,141,73,74,2,0,25,0,0,78,73,74,2,0,7,0,0,66,73,74,98,18,0,0,0,128,72,68,50,18,0,0,0,128,72,68,66,18,0,0,0,128,72,68,82,18,0,0,0,175,72,68,2,0,2,0,0,64,75,90,34,18,0,0,0,141,73,60,2,0,64,0,0,128,75,92,98,18,0,0,0,142,73,60,2,0,64,0,0,192,75,94,98,18,0,0,0,141,73,68,2,0,64,0,0,192,75,94,98,18,0,0,0,28,0,88,2,0,0,0,0,83,72,40,15,128,87,37,0,192,71,88,18,18,0,0,0,26,0,38,15,0,0,0,0,19,75,40,15,0,84,37,0,83,75,40,15,128,84,37,0,147,75,40,15,0,85,37,0,211,75,40,15,128,85,37,0,19,76,40,15,0,86,37,0,83,76,40,15,128,86,37,0,147,76,40,15,0,87,37,0,0,75,88,226,17,0,0,0,175,72,60,2,0,2,0,0,206,72,60,2,0,32,0,0,239,72,70,2,0,2,0,0,14,73,60,2,0,64,0,0,47,73,72,2,0,2,0,0,78,73,60,2,0,96,0,0,141,73,68,2,0,14,0,0,142,72,68,2,0,18,0,0,130,72,68,98,18,0,0,0,141,73,70,2,128,17,0,0,206,72,70,2,128,14,0,0,194,72,70,98,18,0,0,0,141,73,72,2,0,2,0,0,14,73,72,2,0,30,0,0,2,73,72,98,18,0,0,0,141,73,74,2,0,25,0,0,78,73,74,2,0,7,0,0,66,73,74,98,18,0,0,0,128,72,68,50,18,0,0,0,128,72,68,66,18,0,0,0,128,72,68,82,18,0,0,0,175,72,68,2,0,2,0,0,64,75,90,34,18,0,0,0,141,73,60,2,0,64,0,0,128,75,92,98,18,0,0,0,142,73,60,2,0,64,0,0,192,75,94,98,18,0,0,0,141,73,68,2,0,64,0,0,192,75,94,98,18,0,0,0,26,0,38,15,0,0,0,0,83,71,0,2,0,212,36,0,142,66,58,2,0,64,0,0,111,71,58,2,128,1,0,0,69,71,4,210,17,0,0,0,49,66,58,2,0,4,0,0,23,0,16,2,128,251,1,0,4,70,28,159,16,0,0,0,68,70,28,175,16,0,0,0,138,71,48,2,0,0,0,0,18,71,0,0,0,0,0,0,82,67,0,0,0,0,0,0,146,68,0,0,0,0,0,0,8,66,56,34,17,0,0,0,23,0,16,2,128,205,1,0,20,0,26,226,17,0,0,0,75,67,26,2,128,0,0,0,171,68,36,2,128,4,0,0,217,228,1,0,128,157,1,0,11,71,56,2,128,0,0,0,49,66,62,2,0,5,0,0,22,0,16,2,128,209,1,0,49,66,56,2,128,5,0,0,23,0,16,2,128,251,1,0,138,71,62,2,0,0,0,0,24,0,0,0,0,203,1,0,9,66,56,210,17,0,0,0,22,0,16,2,128,221,1,0,133,70,56,210,17,0,0,0,210,68,0,0,0,0,0,0,82,69,0,0,0,0,0,0,171,73,38,2,128,4,0,0,9,66,52,98,18,0,0,0,22,0,16,2,0,215,1,0,202,68,76,2,0,0,0,0,75,69,42,2,128,0,0,0,24,0,0,0,0,212,1,0,19,70,42,2,0,0,0,0,75,69,42,2,128,0,0,0,43,69,38,2,128,4,0,0,133,70,52,50,17,0,0,0,16,66,52,2,0,0,0,0,22,0,16,2,128,220,1,0,138,71,48,2,0,0,0,0,217,228,1,0,128,157,1,0,10,70,62,2,0,0,0,0,140,70,52,2,128,0,0,0,24,0,0,0,0,217,1,0,197,68,56,210,17,0,0,0,24,0,0,0,0,227,1,0,133,70,58,194,17,0,0,0,210,68,0,0,0,0,0,0,50,69,0,0,128,4,0,0,82,69,0,0,128,0,0,0,16,66,52,2,0,0,0,0,22,0,16,2,0,227,1,0,138,71,50,2,0,0,0,0,217,228,1,0,128,157,1,0,74,70,62,2,0,0,0,0,140,70,52,2,128,0,0,0,24,0,0,0,128,223,1,0,8,66,48,146,17,0,0,0,22,0,16,2,128,251,1,0,9,66,40,194,17,0,0,0,23,0,16,2,0,238,1,0,197,69,40,50,17,0,0,0,138,70,46,2,0,0,0,0,138,69,50,2,0,0,0,0,138,71,44,2,0,0,0,0,217,228,1,0,128,157,1,0,138,69,62,2,0,0,0,0,140,70,52,2,128,0,0,0,16,66,52,2,0,0,0,0,23,0,16,2,128,230,1,0,147,73,42,2,0,0,0,0,8,66,76,98,17,0,0,0,22,0,16,2,128,238,1,0,10,70,76,2,0,0,0,0,74,70,44,2,0,0,0,0,202,68,40,2,0,0,0,0,43,69,40,2,128,4,0,0,75,69,42,2,128,0,0,0,24,0,0,0,0,228,1,0,197,69,56,50,17,0,0,0,16,66,46,2,0,0,0,0,22,0,16,2,128,251,1,0,138,71,48,2,0,0,0,0,217,228,1,0,128,157,1,0,10,72,62,2,0,0,0,0,138,71,50,2,0,0,0,0,217,228,1,0,128,157,1,0,8,66,64,242,17,0,0,0,22,0,16,2,0,245,1,0,10,70,64,2,0,0,0,0,74,70,62,2,0,0,0,0,204,69,46,2,128,0,0,0,24,0,0,0,128,238,1,0,138,71,48,2,0,0,0,0,217,228,1,0,0,178,1,0,20,0,40,207,18,88,37,0,20,0,40,223,146,88,37,0,20,0,40,239,18,89,37,0,20,0,40,255,146,89,37,0,138,71,50,2,0,0,0,0,217,228,1,0,0,178,1,0,20,0,40,207,18,90,37,0,20,0,40,223,146,90,37,0,20,0,40,239,18,91,37,0,20,0,40,255,146,91,37,0,29,0,0,0,128,0,0,0,29,0,0,0,128,6,0,0,0,0,0,0,0,0,0,0,0,0,0,24,203,94,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,128,177,236,13,219,78,140,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,255,255,255,255,255,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,255,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,255,255,255,255,255,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,255,255,255,255,255,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,240,140,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,136,229,196,201,251,125,169,170,7,245,154,26,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,100,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,240,140,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
static const unsigned char PF[49]={130,60,60,226,97,200,203,195,144,159,135,33,79,15,67,190,30,134,188,61,12,249,123,24,242,248,48,228,243,97,200,235,195,144,223,135,33,207,15,67,190,31,134,188,63,12,249,127,0};
int main(int argc, char **argv) {
  if (argc != 3) fail("usage");
  rt_ofd = rt_create(argv[1]); for (unsigned i = 0; i < sizeof CTL; i++) rt_putc(CTL[i]); rt_flush(); rt_sys3(3, rt_ofd, 0, 0);
  rt_ofd = rt_create(argv[2]); for (unsigned i = 0; i < sizeof PF; i++) rt_putc(PF[i]); rt_flush();
  return 0;
}
```

## Appendix C. Measured construction record

```json
{
 "address_space_limit": 1048576,
 "peak_bytes": 1012019,
 "phases": [
  {
   "args": [
    "constants0.txt"
   ],
   "binary": "np_consts",
   "charged_peak_bytes": 174368,
   "image": {
    "bss": 39968,
    "data": 48,
    "image": 42871,
    "text": 2855
   },
   "name": "lane constants (incumbent row-0 rule)",
   "outputs": {
    "constants0.txt": "4ef3a563babaec32308727a7efe7598da959a3f054aebc8ef99384c6c5f37d88"
   },
   "retained_input_output_bytes": 425,
   "seconds": 0.0,
   "stack_reserve": 131072,
   "stdout": "",
   "vmhwm_bytes": 49152,
   "wrapper_maxrss_bytes": 1978368
  },
  {
   "args": [
    "spec_zero.txt",
    "plan_input.txt"
   ],
   "binary": "np_emit",
   "charged_peak_bytes": 891208,
   "image": {
    "bss": 685152,
    "data": 16,
    "image": 708007,
    "text": 22839
   },
   "name": "round-1 record and one-constant row table",
   "outputs": {
    "plan_input.txt": "f7215edc414a6f7bdc4bd3820b650dee42cd18b51c946a1f2d3afceacfffb00e"
   },
   "retained_input_output_bytes": 52129,
   "seconds": 0.4,
   "stack_reserve": 131072,
   "stdout": "",
   "vmhwm_bytes": 401408,
   "wrapper_maxrss_bytes": 1978368
  },
  {
   "args": [
    "spec_zero.txt",
    "kmap.txt"
   ],
   "binary": "np_emit",
   "charged_peak_bytes": 914681,
   "image": {
    "bss": 685152,
    "data": 16,
    "image": 708007,
    "text": 22839
   },
   "name": "row-0 polarity map",
   "outputs": {
    "kmap.txt": "a7cdb9331663599610e4d4ad23656e3d965166404e667d5ce96755557449a2b9"
   },
   "retained_input_output_bytes": 75602,
   "seconds": 0.14,
   "stack_reserve": 131072,
   "stdout": "",
   "vmhwm_bytes": 335872,
   "wrapper_maxrss_bytes": 1974272
  },
  {
   "args": [
    "plan_input.txt",
    "90000000",
    "2",
    "34",
    "6",
    "plan1.txt",
    "K:kmap.txt"
   ],
   "binary": "np_plank",
   "charged_peak_bytes": 953472,
   "image": {
    "bss": 678208,
    "data": 32,
    "image": 690951,
    "text": 12711
   },
   "name": "polarity planner with row-0 moves, pass 1",
   "outputs": {
    "plan1.txt": "5c7e73ab0f1b52a9c0e67cc83ef7a3ab730a67eb99ed711c264e8f35db54b0dd"
   },
   "retained_input_output_bytes": 131449,
   "seconds": 260.32,
   "stack_reserve": 131072,
   "stdout": "stage 1 exact-total 13520\nstage 2 exact-total 13368\nstage 3 exact-total 12830\nstage 4 exact-total 12766\nstage 5 exact-total 12766\nfinal 12766\nKX 01000101111010101110110101100001001000111110000100000000000011101000110010111111010101110110100110010111001100010001110111000100010101100000010111100101001111100110111000110111010101110111110011100111110110111001101010111101011100011011100011001101010001010000101100000110001001110100110000110010100101101000100101110111",
   "vmhwm_bytes": 544768,
   "wrapper_maxrss_bytes": 1974272
  },
  {
   "args": [
    "consts.txt",
    "p_plank.out"
   ],
   "binary": "np_consts",
   "charged_peak_bytes": 175259,
   "image": {
    "bss": 39968,
    "data": 48,
    "image": 42871,
    "text": 2855
   },
   "name": "lane constants (planned row-0 polarity)",
   "outputs": {
    "consts.txt": "02a1023b65a6f997ad9326fc82536e244fe7c1dacb4a33adadcb7b776f38bd5f"
   },
   "retained_input_output_bytes": 1316,
   "seconds": 0.0,
   "stack_reserve": 131072,
   "stdout": "",
   "vmhwm_bytes": 45056,
   "wrapper_maxrss_bytes": 1978368
  },
  {
   "args": [
    "spec1.txt",
    "pi2.txt"
   ],
   "binary": "np_emit",
   "charged_peak_bytes": 895780,
   "image": {
    "bss": 685152,
    "data": 16,
    "image": 708007,
    "text": 22839
   },
   "name": "round-1 record under the pass-1 plan",
   "outputs": {
    "pi2.txt": "852499c9b301decd5b0cf6acbbffa370d493598830e3a60f5c197c1e722a4fc3"
   },
   "retained_input_output_bytes": 56701,
   "seconds": 0.34,
   "stack_reserve": 131072,
   "stdout": "",
   "vmhwm_bytes": 401408,
   "wrapper_maxrss_bytes": 1765376
  },
  {
   "args": [
    "pi2.txt",
    "200000000",
    "2",
    "19",
    "6",
    "plan2.txt",
    "plan1.txt"
   ],
   "binary": "np_plan",
   "charged_peak_bytes": 513371,
   "image": {
    "bss": 310144,
    "data": 32,
    "image": 321455,
    "text": 11279
   },
   "name": "polarity planner, pass 2 (rounds 2-5, round 1 fixed)",
   "outputs": {
    "plan2.txt": "a4b197ffdefacaa19b175bfea968f20c5c95cb07bb0bb0f2410c0ff2d4a04b7c"
   },
   "retained_input_output_bytes": 60844,
   "seconds": 446.62,
   "stack_reserve": 131072,
   "stdout": "stage 1 exact-total 11255\nstage 2 exact-total 11193\nstage 3 exact-total 10682\nstage 4 exact-total 10609\nstage 5 exact-total 10609\nfinal 10609",
   "vmhwm_bytes": 294912,
   "wrapper_maxrss_bytes": 1761280
  },
  {
   "args": [
    "pi2.txt",
    "plan2.txt",
    "6000",
    "51",
    "3",
    "plan3.txt"
   ],
   "binary": "np_ils2",
   "charged_peak_bytes": 574718,
   "image": {
    "bss": 371584,
    "data": 24,
    "image": 382802,
    "text": 11194
   },
   "name": "joint ILS over round-1 targets and the pass-2 plan",
   "outputs": {
    "plan3.txt": "7c3ea42cc24ae1698a25d672ff818c9848d852241eabd71147d04e449e7260c6"
   },
   "retained_input_output_bytes": 60844,
   "seconds": 342.63,
   "stack_reserve": 131072,
   "stdout": "start 12762\nfinal 12762",
   "vmhwm_bytes": 303104,
   "wrapper_maxrss_bytes": 1978368
  },
  {
   "args": [
    "pi2.txt",
    "plan3.txt",
    "s1",
    "plan4.txt"
   ],
   "binary": "np_pair",
   "charged_peak_bytes": 544553,
   "image": {
    "bss": 340864,
    "data": 16,
    "image": 352637,
    "text": 11757
   },
   "name": "exhaustive round-1 target-pair polish",
   "outputs": {
    "plan4.txt": "7c3ea42cc24ae1698a25d672ff818c9848d852241eabd71147d04e449e7260c6"
   },
   "retained_input_output_bytes": 60844,
   "seconds": 33.97,
   "stack_reserve": 131072,
   "stdout": "start 12762\nfinal 12762",
   "vmhwm_bytes": 270336,
   "wrapper_maxrss_bytes": 1974272
  },
  {
   "args": [
    "pi2.txt",
    "plan4.txt",
    "75",
    "4001",
    "10",
    "plan5.txt"
   ],
   "binary": "np_ils4",
   "charged_peak_bytes": 1005579,
   "image": {
    "bss": 790848,
    "data": 24,
    "image": 813663,
    "text": 22791
   },
   "name": "joint two-column local search (pass 5)",
   "outputs": {
    "plan5.txt": "0ac906c912451ecbd85244feeb18ed2769d667dfa0644025dcd0082c1670103b"
   },
   "retained_input_output_bytes": 60844,
   "seconds": 32.59,
   "stack_reserve": 131072,
   "stdout": "start 12762\nils 1 best 12761\nils 7 best 12760\nils 11 best 12759\nfinal 12759",
   "vmhwm_bytes": 675840,
   "wrapper_maxrss_bytes": 1978368
  },
  {
   "args": [
    "pi2.txt",
    "plan5.txt",
    "500",
    "7001",
    "10",
    "drift7001.txt"
   ],
   "binary": "np_ils6",
   "charged_peak_bytes": 1005803,
   "image": {
    "bss": 790848,
    "data": 24,
    "image": 813887,
    "text": 23015
   },
   "name": "plateau-drift two-column local search (pass 6)",
   "outputs": {
    "drift7001.txt": "5c855ef2fb1bbbe1870c5fde7991c9f867b65e6751ecb183dd7c4ee129ecb866"
   },
   "retained_input_output_bytes": 60844,
   "seconds": 288.39,
   "stack_reserve": 131072,
   "stdout": "start 12759\nils 0 best 12759\nils 1 best 12759\nils 2 best 12759\nils 4 best 12759\nils 7 best 12759\nils 8 best 12759\nils 9 best 12759\nils 10 best 12759\nils 11 best 12759\nils 13 best 12759\nils 14 best 12759\nils 15 best 12759\nils 17 best 12759\nils 18 best 12759\nils 19 best 12759\nils 21 best 12759\nils 22 best 12759\nils 23 best 12759\nils 24 best 12759\nils 25 best 12759\nils 26 best 12759\nils 27 best 12759\nils 29 best 12759\nils 30 best 12759\nils 31 best 12759\nils 34 best 12759\nils 35 best 12759\nils 36 best 12759\nils 37 best 12759\nils 38 best 12759\nils 40 best 12759\nils 41 best 12759\nils 42 best 12759\nils 44 best 12759\nils 45 best 12759\nils 46 best 12759\nils 47 best 12759\nils 49 best 12759\nils 52 best 12759\nils 53 best 12759\nils 54 best 12759\nils 55 best 12759\nils 56 best 12759\nils 57 best 12759\nils 58 best 12759\nils 59 best 12759\nils 60 best 12759\nils 62 best 12759\nils 63 best 12759\nils 65 best 12759\nils 66 best 12759\nils 67 best 12759\nils 68 best 12759\nils 69 best 12759\nils 70 best 12759\nils 71 best 12759\nils 72 best 12759\nils 73 best 12759\nils 74 best 12759\nils 75 best 12759\nils 76 best 12759\nils 77 best 12759\nils 79 best 12759\nils 80 best 12759\nils 81 best 12759\nils 83 best 12759\nils 84 best 12759\nils 85 best 12759\nils 86 best 12759\nils 88 best 12759\nils 89 best 12759\nils 90 best 12759\nils 91 best 12759\nils 92 best 12759\nils 93 best 12759\nils 94 best 12759\nils 95 best 12759\nils 96 best 12759\nils 97 best 12759\nils 99 best 12759\nils 101 best 12759\nils 102 best 12759\nils 103 best 12759\nils 105 best 12759\nils 106 best 12759\nils 107 best 12759\nils 109 best 12759\nils 110 best 12759\nils 111 best 12759\nils 112 best 12759\nils 113 best 12759\nils 117 best 12759\nils 118 best 12759\nils 120 best 12759\nils 122 best 12759\nils 123 best 12759\nils 124 best 12759\nils 125 best 12759\nils 126 best 12759\nils 127 best 12759\nils 128 best 12759\nils 129 best 12759\nils 130 best 12759\nils 131 best 12759\nils 132 best 12759\nils 134 best 12759\nils 135 best 12759\nils 136 best 12759\nils 137 best 12759\nils 138 best 12759\nils 139 best 12759\nils 140 best 12759\nils 141 best 12759\nils 142 best 12759\nils 143 best 12759\nils 144 best 12759\nils 145 best 12759\nils 147 best 12759\nils 148 best 12759\nils 149 best 12759\nils 150 best 12759\nils 151 best 12759\nils 153 best 12759\nils 155 best 12759\nils 156 best 12759\nils 157 best 12759\nils 158 best 12759\nils 159 best 12759\nils 160 best 12759\nils 161 best 12759\nils 162 best 12759\nils 163 best 12759\nils 164 best 12759\nils 165 best 12759\nils 166 best 12759\nils 167 best 12759\nils 168 best 12759\nils 169 best 12759\nils 170 best 12759\nils 171 best 12759\nils 172 best 12759\nils 174 best 12759\nils 176 best 12759\nils 178 best 12759\nils 179 best 12759\nils 181 best 12759\nils 183 best 12759\nils 184 best 12759\nils 185 best 12759\nils 186 best 12759\nils 190 best 12759\nils 191 best 12759\nils 193 best 12759\nils 194 best 12759\nils 195 best 12759\nils 196 best 12759\nils 197 best 12759\nils 199 best 12759\nils 200 best 12759\nils 202 best 12759\nils 203 best 12759\nils 204 best 12759\nils 205 best 12759\nils 206 best 12759\nils 207 best 12759\nils 208 best 12759\nils 210 best 12759\nils 211 best 12759\nils 213 best 12759\nils 214 best 12759\nils 216 best 12759\nils 218 best 12759\nils 219 best 12759\nils 220 best 12759\nils 221 best 12759\nils 224 best 12759\nils 225 best 12759\nils 226 best 12759\nils 228 best 12759\nils 229 best 12759\nils 230 best 12759\nils 231 best 12759\nils 232 best 12759\nils 233 best 12759\nils 234 best 12759\nils 235 best 12759\nils 236 best 12759\nils 237 best 12759\nils 239 best 12759\nils 240 best 12759\nils 241 best 12759\nils 242 best 12759\nils 245 best 12759\nils 246 best 12759\nils 248 best 12759\nils 249 best 12759\nils 250 best 12759\nils 251 best 12759\nils 253 best 12759\nils 254 best 12759\nils 255 best 12759\nils 256 best 12759\nils 257 best 12759\nils 259 best 12759\nils 260 best 12759\nils 261 best 12758\nils 262 best 12758\nils 263 best 12758\nils 264 best 12758\nils 265 best 12758\nils 266 best 12758\nils 267 best 12758\nils 268 best 12758\nils 269 best 12758\nils 270 best 12758\nils 273 best 12758\nils 274 best 12758\nils 275 best 12758\nils 276 best 12758\nils 277 best 12758\nils 279 best 12758\nils 281 best 12758\nils 282 best 12758\nils 283 best 12758\nils 284 best 12758\nils 285 best 12758\nils 286 best 12758\nils 287 best 12758\nils 291 best 12758\nils 294 best 12758\nils 295 best 12758\nils 296 best 12758\nils 297 best 12758\nils 298 best 12758\nils 299 best 12758\nils 300 best 12758\nils 301 best 12758\nils 302 best 12758\nils 303 best 12758\nils 304 best 12758\nils 305 best 12758\nils 306 best 12758\nils 307 best 12758\nils 308 best 12758\nils 309 best 12758\nils 310 best 12758\nils 311 best 12758\nils 312 best 12758\nils 314 best 12758\nils 315 best 12758\nils 316 best 12758\nils 317 best 12758\nils 318 best 12758\nils 319 best 12758\nils 320 best 12758\nils 321 best 12758\nils 323 best 12758\nils 324 best 12758\nils 325 best 12758\nils 326 best 12758\nils 327 best 12758\nils 328 best 12758\nils 329 best 12758\nils 330 best 12758\nils 331 best 12758\nils 334 best 12758\nils 335 best 12758\nils 337 best 12758\nils 338 best 12758\nils 339 best 12758\nils 340 best 12758\nils 341 best 12758\nils 342 best 12758\nils 343 best 12758\nils 344 best 12758\nils 347 best 12758\nils 348 best 12758\nils 349 best 12758\nils 350 best 12758\nils 352 best 12758\nils 353 best 12758\nils 354 best 12758\nils 355 best 12758\nils 357 best 12758\nils 358 best 12758\nils 360 best 12758\nils 361 best 12758\nils 363 best 12758\nils 364 best 12758\nils 366 best 12758\nils 368 best 12758\nils 369 best 12758\nils 370 best 12758\nils 371 best 12758\nils 372 best 12758\nils 374 best 12758\nils 375 best 12758\nils 376 best 12758\nils 377 best 12758\nils 378 best 12758\nils 379 best 12758\nils 381 best 12758\nils 382 best 12758\nils 383 best 12758\nils 384 best 12758\nils 385 best 12758\nils 386 best 12758\nils 388 best 12758\nils 389 best 12758\nils 391 best 12758\nils 392 best 12758\nils 393 best 12758\nils 394 best 12758\nils 395 best 12758\nils 397 best 12758\nils 398 best 12758\nils 399 best 12758\nils 400 best 12758\nils 401 best 12758\nils 403 best 12758\nils 404 best 12758\nils 406 best 12758\nils 407 best 12758\nils 410 best 12758\nils 411 best 12758\nils 412 best 12758\nils 414 best 12758\nils 417 best 12758\nils 418 best 12758\nils 420 best 12758\nils 421 best 12758\nils 422 best 12758\nils 424 best 12758\nils 425 best 12758\nils 429 best 12758\nils 432 best 12758\nils 434 best 12758\nils 437 best 12758\nils 438 best 12758\nils 439 best 12758\nils 440 best 12758\nils 442 best 12758\nils 443 best 12758\nils 444 best 12758\nils 445 best 12758\nils 446 best 12758\nils 447 best 12758\nils 448 best 12758\nils 449 best 12758\nils 450 best 12758\nils 454 best 12758\nils 455 best 12758\nils 456 best 12758\nils 457 best 12758\nils 458 best 12758\nils 459 best 12758\nils 460 best 12758\nils 462 best 12758\nils 463 best 12758\nils 464 best 12758\nils 465 best 12758\nils 466 best 12758\nils 467 best 12758\nils 468 best 12758\nils 471 best 12758\nils 472 best 12758\nils 473 best 12758\nils 474 best 12758\nils 475 best 12758\nils 476 best 12758\nils 478 best 12758\nils 479 best 12758\nils 481 best 12758\nils 482 best 12758\nils 483 best 12758\nils 485 best 12758\nils 486 best 12758\nils 487 best 12758\nils 488 best 12758\nils 489 best 12758\nils 490 best 12758\nils 491 best 12758\nils 493 best 12758\nils 494 best 12758\nils 495 best 12758\nils 497 best 12758\nils 498 best 12758\nils 499 best 12758\nfinal 12758",
   "vmhwm_bytes": 675840,
   "wrapper_maxrss_bytes": 1978368
  },
  {
   "args": [
    "pi2.txt",
    "drift7001.txt",
    "500",
    "7002",
    "10",
    "drift7002.txt"
   ],
   "binary": "np_ils6",
   "charged_peak_bytes": 1005803,
   "image": {
    "bss": 790848,
    "data": 24,
    "image": 813887,
    "text": 23015
   },
   "name": "plateau-drift two-column local search (pass 7)",
   "outputs": {
    "drift7002.txt": "c2447ca36a437dc5136f29d9f5991d5b475e3c92f55e4948bf0aedd66b7e8c60"
   },
   "retained_input_output_bytes": 60844,
   "seconds": 293.98,
   "stack_reserve": 131072,
   "stdout": "start 12758\nils 0 best 12758\nils 1 best 12758\nils 3 best 12758\nils 5 best 12758\nils 6 best 12758\nils 7 best 12758\nils 8 best 12758\nils 9 best 12758\nils 10 best 12758\nils 11 best 12758\nils 13 best 12758\nils 15 best 12758\nils 16 best 12758\nils 18 best 12758\nils 19 best 12758\nils 20 best 12758\nils 21 best 12758\nils 22 best 12758\nils 26 best 12758\nils 29 best 12758\nils 30 best 12758\nils 31 best 12758\nils 32 best 12758\nils 33 best 12758\nils 34 best 12758\nils 36 best 12758\nils 37 best 12758\nils 38 best 12758\nils 39 best 12758\nils 40 best 12758\nils 41 best 12758\nils 42 best 12758\nils 43 best 12758\nils 45 best 12758\nils 47 best 12758\nils 48 best 12758\nils 49 best 12758\nils 50 best 12758\nils 51 best 12758\nils 52 best 12758\nils 53 best 12758\nils 54 best 12758\nils 56 best 12757\nils 57 best 12757\nils 58 best 12757\nils 59 best 12757\nils 60 best 12757\nils 61 best 12757\nils 62 best 12757\nils 63 best 12757\nils 65 best 12757\nils 68 best 12757\nils 69 best 12757\nils 71 best 12757\nils 72 best 12756\nils 74 best 12756\nils 75 best 12756\nils 76 best 12756\nils 77 best 12756\nils 78 best 12756\nils 79 best 12756\nils 81 best 12756\nils 82 best 12756\nils 83 best 12756\nils 84 best 12756\nils 87 best 12756\nils 88 best 12756\nils 89 best 12756\nils 91 best 12756\nils 92 best 12756\nils 95 best 12756\nils 97 best 12756\nils 99 best 12756\nils 100 best 12756\nils 101 best 12756\nils 102 best 12756\nils 104 best 12756\nils 105 best 12756\nils 106 best 12756\nils 107 best 12756\nils 108 best 12756\nils 109 best 12756\nils 112 best 12756\nils 113 best 12756\nils 114 best 12756\nils 115 best 12756\nils 116 best 12756\nils 118 best 12756\nils 119 best 12756\nils 120 best 12756\nils 121 best 12756\nils 122 best 12756\nils 123 best 12756\nils 124 best 12756\nils 126 best 12756\nils 127 best 12756\nils 129 best 12756\nils 130 best 12756\nils 131 best 12756\nils 132 best 12756\nils 133 best 12756\nils 134 best 12756\nils 136 best 12756\nils 137 best 12756\nils 138 best 12756\nils 139 best 12756\nils 140 best 12756\nils 142 best 12756\nils 144 best 12756\nils 145 best 12756\nils 146 best 12756\nils 147 best 12756\nils 149 best 12756\nils 150 best 12756\nils 151 best 12756\nils 153 best 12756\nils 154 best 12756\nils 155 best 12756\nils 156 best 12756\nils 159 best 12756\nils 161 best 12756\nils 163 best 12756\nils 164 best 12756\nils 169 best 12756\nils 170 best 12756\nils 171 best 12756\nils 172 best 12756\nils 173 best 12756\nils 174 best 12756\nils 176 best 12756\nils 177 best 12756\nils 178 best 12756\nils 179 best 12756\nils 181 best 12756\nils 182 best 12756\nils 183 best 12756\nils 184 best 12756\nils 185 best 12756\nils 188 best 12756\nils 189 best 12756\nils 190 best 12756\nils 192 best 12756\nils 193 best 12756\nils 197 best 12756\nils 198 best 12756\nils 199 best 12755\nils 200 best 12755\nils 201 best 12755\nils 202 best 12755\nils 203 best 12755\nils 204 best 12755\nils 206 best 12755\nils 207 best 12755\nils 208 best 12755\nils 209 best 12755\nils 210 best 12755\nils 211 best 12755\nils 212 best 12755\nils 213 best 12755\nils 214 best 12755\nils 216 best 12755\nils 217 best 12755\nils 219 best 12755\nils 220 best 12755\nils 221 best 12755\nils 222 best 12755\nils 223 best 12755\nils 224 best 12755\nils 225 best 12755\nils 226 best 12755\nils 227 best 12755\nils 228 best 12755\nils 230 best 12755\nils 232 best 12755\nils 233 best 12755\nils 235 best 12755\nils 236 best 12755\nils 237 best 12755\nils 238 best 12755\nils 239 best 12755\nils 240 best 12755\nils 241 best 12755\nils 242 best 12755\nils 243 best 12755\nils 244 best 12755\nils 245 best 12755\nils 246 best 12755\nils 247 best 12755\nils 249 best 12755\nils 250 best 12755\nils 251 best 12755\nils 254 best 12755\nils 256 best 12755\nils 257 best 12755\nils 259 best 12755\nils 260 best 12755\nils 261 best 12755\nils 262 best 12755\nils 263 best 12755\nils 266 best 12755\nils 267 best 12755\nils 268 best 12755\nils 271 best 12755\nils 272 best 12755\nils 275 best 12755\nils 276 best 12755\nils 277 best 12755\nils 279 best 12755\nils 282 best 12755\nils 283 best 12755\nils 285 best 12755\nils 286 best 12755\nils 287 best 12755\nils 288 best 12755\nils 289 best 12755\nils 290 best 12755\nils 291 best 12755\nils 292 best 12755\nils 293 best 12755\nils 294 best 12755\nils 295 best 12755\nils 296 best 12755\nils 297 best 12755\nils 298 best 12755\nils 300 best 12755\nils 301 best 12755\nils 303 best 12755\nils 304 best 12755\nils 305 best 12755\nils 306 best 12755\nils 307 best 12755\nils 308 best 12755\nils 310 best 12755\nils 311 best 12755\nils 312 best 12755\nils 313 best 12755\nils 314 best 12755\nils 315 best 12755\nils 317 best 12755\nils 318 best 12755\nils 319 best 12755\nils 320 best 12755\nils 321 best 12755\nils 322 best 12755\nils 323 best 12755\nils 325 best 12755\nils 326 best 12755\nils 327 best 12755\nils 329 best 12755\nils 330 best 12755\nils 331 best 12755\nils 332 best 12755\nils 333 best 12755\nils 334 best 12755\nils 335 best 12755\nils 336 best 12755\nils 337 best 12755\nils 339 best 12755\nils 340 best 12755\nils 341 best 12755\nils 342 best 12755\nils 343 best 12755\nils 344 best 12755\nils 346 best 12755\nils 347 best 12755\nils 348 best 12755\nils 349 best 12755\nils 352 best 12755\nils 353 best 12755\nils 354 best 12755\nils 357 best 12755\nils 361 best 12755\nils 362 best 12755\nils 363 best 12755\nils 364 best 12755\nils 365 best 12755\nils 367 best 12755\nils 368 best 12755\nils 369 best 12755\nils 370 best 12755\nils 371 best 12755\nils 372 best 12755\nils 373 best 12755\nils 375 best 12755\nils 376 best 12755\nils 377 best 12755\nils 378 best 12755\nils 380 best 12755\nils 382 best 12755\nils 383 best 12755\nils 385 best 12755\nils 387 best 12755\nils 388 best 12755\nils 389 best 12755\nils 391 best 12755\nils 393 best 12755\nils 394 best 12755\nils 395 best 12755\nils 396 best 12755\nils 397 best 12755\nils 399 best 12755\nils 400 best 12755\nils 401 best 12755\nils 402 best 12755\nils 403 best 12755\nils 404 best 12755\nils 405 best 12755\nils 406 best 12755\nils 407 best 12755\nils 410 best 12755\nils 411 best 12755\nils 412 best 12755\nils 413 best 12755\nils 414 best 12755\nils 416 best 12755\nils 417 best 12755\nils 420 best 12755\nils 423 best 12755\nils 424 best 12755\nils 425 best 12755\nils 426 best 12755\nils 427 best 12755\nils 429 best 12755\nils 432 best 12755\nils 433 best 12755\nils 435 best 12755\nils 436 best 12755\nils 438 best 12755\nils 439 best 12755\nils 440 best 12755\nils 441 best 12755\nils 442 best 12755\nils 444 best 12755\nils 446 best 12755\nils 448 best 12755\nils 449 best 12755\nils 450 best 12755\nils 451 best 12755\nils 453 best 12755\nils 454 best 12755\nils 455 best 12755\nils 458 best 12755\nils 459 best 12755\nils 460 best 12755\nils 461 best 12755\nils 462 best 12755\nils 463 best 12755\nils 464 best 12755\nils 465 best 12755\nils 467 best 12755\nils 470 best 12755\nils 472 best 12755\nils 475 best 12755\nils 478 best 12755\nils 480 best 12755\nils 482 best 12755\nils 483 best 12755\nils 484 best 12755\nils 485 best 12755\nils 487 best 12755\nils 488 best 12755\nils 489 best 12755\nils 490 best 12755\nils 491 best 12755\nils 492 best 12755\nils 493 best 12755\nils 496 best 12755\nils 497 best 12755\nils 498 best 12755\nfinal 12755",
   "vmhwm_bytes": 675840,
   "wrapper_maxrss_bytes": 1978368
  },
  {
   "args": [
    "pi2.txt",
    "drift7002.txt",
    "500",
    "7006",
    "10",
    "drift7006.txt"
   ],
   "binary": "np_ils6",
   "charged_peak_bytes": 1005803,
   "image": {
    "bss": 790848,
    "data": 24,
    "image": 813887,
    "text": 23015
   },
   "name": "plateau-drift two-column local search (pass 8)",
   "outputs": {
    "drift7006.txt": "3394c9007d1e267b5a1ff0961847380dbfbbad5d6c80198812d5d1cc60f18e63"
   },
   "retained_input_output_bytes": 60844,
   "seconds": 284.3,
   "stack_reserve": 131072,
   "stdout": "start 12755\nils 1 best 12755\nils 2 best 12755\nils 4 best 12755\nils 5 best 12755\nils 6 best 12755\nils 8 best 12755\nils 12 best 12755\nils 13 best 12755\nils 14 best 12755\nils 15 best 12755\nils 16 best 12755\nils 17 best 12755\nils 20 best 12755\nils 21 best 12755\nils 22 best 12755\nils 23 best 12755\nils 24 best 12755\nils 25 best 12755\nils 26 best 12755\nils 27 best 12755\nils 28 best 12755\nils 29 best 12755\nils 30 best 12755\nils 31 best 12755\nils 32 best 12755\nils 34 best 12755\nils 35 best 12755\nils 37 best 12755\nils 38 best 12755\nils 39 best 12755\nils 40 best 12755\nils 41 best 12755\nils 42 best 12755\nils 43 best 12755\nils 44 best 12755\nils 45 best 12755\nils 46 best 12755\nils 49 best 12755\nils 50 best 12755\nils 51 best 12755\nils 52 best 12755\nils 53 best 12755\nils 54 best 12755\nils 55 best 12755\nils 57 best 12755\nils 58 best 12755\nils 59 best 12755\nils 60 best 12755\nils 62 best 12755\nils 63 best 12755\nils 64 best 12755\nils 65 best 12755\nils 68 best 12755\nils 69 best 12755\nils 70 best 12755\nils 71 best 12755\nils 72 best 12755\nils 73 best 12755\nils 74 best 12755\nils 76 best 12755\nils 78 best 12755\nils 80 best 12755\nils 82 best 12755\nils 83 best 12755\nils 84 best 12755\nils 85 best 12755\nils 86 best 12755\nils 88 best 12755\nils 90 best 12755\nils 91 best 12755\nils 92 best 12755\nils 94 best 12755\nils 95 best 12755\nils 96 best 12755\nils 97 best 12755\nils 98 best 12755\nils 100 best 12755\nils 101 best 12755\nils 102 best 12755\nils 103 best 12755\nils 104 best 12755\nils 107 best 12755\nils 109 best 12755\nils 110 best 12755\nils 111 best 12755\nils 113 best 12755\nils 115 best 12755\nils 117 best 12755\nils 118 best 12755\nils 119 best 12755\nils 120 best 12755\nils 121 best 12755\nils 122 best 12755\nils 123 best 12755\nils 124 best 12755\nils 125 best 12755\nils 126 best 12755\nils 127 best 12755\nils 128 best 12755\nils 129 best 12755\nils 130 best 12755\nils 131 best 12755\nils 133 best 12755\nils 134 best 12755\nils 135 best 12755\nils 136 best 12755\nils 137 best 12755\nils 138 best 12755\nils 140 best 12755\nils 141 best 12755\nils 142 best 12755\nils 143 best 12755\nils 144 best 12755\nils 145 best 12755\nils 146 best 12755\nils 147 best 12755\nils 148 best 12755\nils 149 best 12755\nils 150 best 12755\nils 151 best 12755\nils 152 best 12755\nils 153 best 12755\nils 154 best 12755\nils 155 best 12755\nils 157 best 12755\nils 158 best 12755\nils 161 best 12755\nils 162 best 12755\nils 163 best 12755\nils 164 best 12755\nils 165 best 12755\nils 166 best 12755\nils 167 best 12755\nils 168 best 12755\nils 169 best 12755\nils 170 best 12755\nils 171 best 12755\nils 172 best 12755\nils 173 best 12755\nils 174 best 12755\nils 175 best 12755\nils 177 best 12755\nils 178 best 12755\nils 179 best 12755\nils 180 best 12755\nils 181 best 12755\nils 183 best 12755\nils 184 best 12755\nils 185 best 12755\nils 186 best 12755\nils 187 best 12755\nils 188 best 12755\nils 189 best 12755\nils 190 best 12755\nils 191 best 12755\nils 192 best 12755\nils 193 best 12755\nils 194 best 12755\nils 195 best 12755\nils 196 best 12755\nils 197 best 12755\nils 198 best 12755\nils 199 best 12755\nils 200 best 12755\nils 203 best 12755\nils 205 best 12755\nils 206 best 12755\nils 207 best 12755\nils 208 best 12755\nils 210 best 12755\nils 212 best 12755\nils 213 best 12755\nils 214 best 12755\nils 215 best 12755\nils 216 best 12755\nils 218 best 12755\nils 219 best 12755\nils 220 best 12755\nils 221 best 12755\nils 222 best 12755\nils 223 best 12754\nils 224 best 12754\nils 225 best 12754\nils 228 best 12754\nils 230 best 12754\nils 231 best 12754\nils 232 best 12754\nils 233 best 12754\nils 234 best 12754\nils 235 best 12754\nils 236 best 12754\nils 237 best 12754\nils 239 best 12754\nils 240 best 12754\nils 241 best 12754\nils 242 best 12754\nils 243 best 12754\nils 246 best 12754\nils 247 best 12754\nils 248 best 12754\nils 249 best 12754\nils 250 best 12754\nils 251 best 12754\nils 252 best 12754\nils 253 best 12754\nils 254 best 12754\nils 255 best 12754\nils 256 best 12754\nils 257 best 12754\nils 260 best 12753\nils 261 best 12753\nils 262 best 12753\nils 263 best 12753\nils 265 best 12753\nils 267 best 12753\nils 268 best 12753\nils 270 best 12753\nils 271 best 12753\nils 274 best 12753\nils 275 best 12753\nils 276 best 12753\nils 277 best 12753\nils 278 best 12753\nils 279 best 12753\nils 280 best 12753\nils 281 best 12753\nils 282 best 12753\nils 283 best 12753\nils 286 best 12753\nils 287 best 12753\nils 288 best 12753\nils 289 best 12753\nils 290 best 12753\nils 293 best 12753\nils 294 best 12753\nils 295 best 12753\nils 296 best 12753\nils 297 best 12753\nils 298 best 12753\nils 299 best 12753\nils 301 best 12753\nils 303 best 12753\nils 304 best 12753\nils 306 best 12753\nils 307 best 12753\nils 308 best 12753\nils 309 best 12753\nils 312 best 12753\nils 313 best 12753\nils 314 best 12753\nils 315 best 12753\nils 317 best 12753\nils 318 best 12753\nils 320 best 12753\nils 322 best 12753\nils 323 best 12753\nils 324 best 12753\nils 325 best 12753\nils 329 best 12753\nils 330 best 12753\nils 331 best 12753\nils 332 best 12753\nils 333 best 12753\nils 334 best 12753\nils 336 best 12753\nils 337 best 12753\nils 338 best 12753\nils 339 best 12753\nils 340 best 12753\nils 341 best 12753\nils 342 best 12753\nils 343 best 12753\nils 344 best 12753\nils 347 best 12753\nils 349 best 12753\nils 350 best 12753\nils 352 best 12753\nils 353 best 12753\nils 354 best 12753\nils 355 best 12753\nils 359 best 12753\nils 360 best 12753\nils 361 best 12753\nils 362 best 12753\nils 363 best 12753\nils 364 best 12753\nils 365 best 12753\nils 366 best 12753\nils 367 best 12753\nils 368 best 12753\nils 370 best 12753\nils 371 best 12753\nils 372 best 12753\nils 374 best 12753\nils 375 best 12753\nils 376 best 12753\nils 377 best 12753\nils 378 best 12753\nils 379 best 12753\nils 380 best 12753\nils 382 best 12753\nils 384 best 12753\nils 387 best 12753\nils 388 best 12753\nils 390 best 12753\nils 391 best 12753\nils 392 best 12753\nils 393 best 12753\nils 395 best 12753\nils 396 best 12753\nils 397 best 12753\nils 399 best 12753\nils 400 best 12753\nils 401 best 12753\nils 402 best 12753\nils 404 best 12753\nils 405 best 12753\nils 406 best 12753\nils 407 best 12753\nils 408 best 12753\nils 409 best 12753\nils 412 best 12753\nils 413 best 12753\nils 414 best 12753\nils 416 best 12753\nils 418 best 12753\nils 420 best 12753\nils 421 best 12753\nils 422 best 12753\nils 423 best 12753\nils 424 best 12753\nils 425 best 12753\nils 426 best 12753\nils 427 best 12753\nils 429 best 12753\nils 430 best 12753\nils 431 best 12753\nils 432 best 12753\nils 433 best 12753\nils 434 best 12753\nils 435 best 12753\nils 436 best 12753\nils 437 best 12753\nils 438 best 12753\nils 439 best 12753\nils 440 best 12753\nils 441 best 12753\nils 442 best 12753\nils 443 best 12753\nils 445 best 12753\nils 446 best 12753\nils 447 best 12753\nils 448 best 12753\nils 450 best 12753\nils 451 best 12753\nils 453 best 12753\nils 456 best 12753\nils 457 best 12753\nils 458 best 12753\nils 459 best 12753\nils 460 best 12753\nils 461 best 12753\nils 462 best 12753\nils 463 best 12753\nils 464 best 12753\nils 465 best 12753\nils 466 best 12753\nils 467 best 12753\nils 468 best 12753\nils 469 best 12753\nils 470 best 12753\nils 471 best 12753\nils 472 best 12753\nils 475 best 12753\nils 476 best 12753\nils 478 best 12753\nils 479 best 12753\nils 480 best 12753\nils 482 best 12753\nils 483 best 12753\nils 486 best 12753\nils 487 best 12753\nils 489 best 12753\nils 490 best 12753\nils 491 best 12753\nils 492 best 12753\nils 493 best 12753\nils 494 best 12753\nils 495 best 12753\nils 497 best 12753\nils 498 best 12753\nils 499 best 12753\nfinal 12753",
   "vmhwm_bytes": 675840,
   "wrapper_maxrss_bytes": 1978368
  },
  {
   "args": [
    "pi2.txt",
    "drift7006.txt",
    "500",
    "8002",
    "10",
    "drift8002.txt"
   ],
   "binary": "np_ils6",
   "charged_peak_bytes": 1005803,
   "image": {
    "bss": 790848,
    "data": 24,
    "image": 813887,
    "text": 23015
   },
   "name": "plateau-drift two-column local search (pass 9)",
   "outputs": {
    "drift8002.txt": "c0b99119e295962e489db2db76fb8c1fc76c37a1c56a569ee48e165399836570"
   },
   "retained_input_output_bytes": 60844,
   "seconds": 265.48,
   "stack_reserve": 131072,
   "stdout": "start 12753\nils 0 best 12753\nils 1 best 12753\nils 2 best 12753\nils 3 best 12753\nils 4 best 12753\nils 5 best 12753\nils 7 best 12753\nils 9 best 12753\nils 11 best 12753\nils 12 best 12753\nils 14 best 12753\nils 15 best 12753\nils 16 best 12753\nils 17 best 12753\nils 18 best 12753\nils 19 best 12753\nils 21 best 12753\nils 22 best 12753\nils 23 best 12753\nils 26 best 12753\nils 27 best 12753\nils 28 best 12753\nils 29 best 12753\nils 30 best 12753\nils 31 best 12753\nils 33 best 12753\nils 34 best 12753\nils 35 best 12753\nils 37 best 12753\nils 38 best 12753\nils 40 best 12753\nils 41 best 12753\nils 42 best 12753\nils 43 best 12753\nils 44 best 12753\nils 45 best 12753\nils 48 best 12753\nils 49 best 12753\nils 50 best 12753\nils 51 best 12753\nils 53 best 12753\nils 55 best 12753\nils 56 best 12753\nils 57 best 12753\nils 58 best 12753\nils 59 best 12753\nils 60 best 12753\nils 63 best 12753\nils 64 best 12753\nils 65 best 12753\nils 66 best 12753\nils 67 best 12753\nils 68 best 12753\nils 69 best 12753\nils 70 best 12753\nils 71 best 12753\nils 72 best 12753\nils 73 best 12753\nils 74 best 12753\nils 75 best 12753\nils 77 best 12753\nils 78 best 12753\nils 79 best 12753\nils 80 best 12753\nils 81 best 12753\nils 82 best 12753\nils 83 best 12753\nils 84 best 12753\nils 85 best 12753\nils 86 best 12753\nils 87 best 12753\nils 88 best 12753\nils 89 best 12753\nils 90 best 12753\nils 91 best 12753\nils 92 best 12753\nils 93 best 12753\nils 94 best 12753\nils 95 best 12753\nils 96 best 12753\nils 98 best 12753\nils 100 best 12753\nils 101 best 12753\nils 102 best 12753\nils 104 best 12753\nils 106 best 12753\nils 109 best 12753\nils 110 best 12753\nils 111 best 12753\nils 113 best 12753\nils 116 best 12753\nils 117 best 12753\nils 119 best 12753\nils 121 best 12753\nils 126 best 12753\nils 128 best 12753\nils 129 best 12753\nils 130 best 12753\nils 132 best 12753\nils 133 best 12753\nils 135 best 12753\nils 137 best 12753\nils 139 best 12753\nils 140 best 12753\nils 141 best 12753\nils 142 best 12753\nils 143 best 12753\nils 144 best 12753\nils 145 best 12753\nils 146 best 12753\nils 147 best 12753\nils 149 best 12753\nils 150 best 12753\nils 151 best 12753\nils 152 best 12753\nils 153 best 12753\nils 155 best 12753\nils 157 best 12753\nils 158 best 12753\nils 159 best 12753\nils 160 best 12753\nils 161 best 12753\nils 162 best 12753\nils 163 best 12753\nils 164 best 12753\nils 165 best 12753\nils 166 best 12753\nils 169 best 12753\nils 172 best 12753\nils 173 best 12753\nils 175 best 12753\nils 176 best 12753\nils 177 best 12753\nils 178 best 12753\nils 179 best 12753\nils 181 best 12753\nils 182 best 12753\nils 184 best 12753\nils 185 best 12753\nils 187 best 12753\nils 188 best 12753\nils 189 best 12753\nils 190 best 12753\nils 191 best 12753\nils 192 best 12753\nils 193 best 12753\nils 194 best 12753\nils 196 best 12753\nils 197 best 12753\nils 198 best 12753\nils 199 best 12753\nils 201 best 12753\nils 202 best 12753\nils 203 best 12753\nils 204 best 12753\nils 205 best 12753\nils 206 best 12753\nils 207 best 12753\nils 208 best 12753\nils 210 best 12753\nils 211 best 12753\nils 212 best 12753\nils 214 best 12753\nils 215 best 12753\nils 217 best 12753\nils 218 best 12753\nils 219 best 12753\nils 220 best 12753\nils 221 best 12753\nils 222 best 12753\nils 223 best 12753\nils 224 best 12753\nils 225 best 12753\nils 226 best 12753\nils 227 best 12753\nils 229 best 12753\nils 230 best 12753\nils 231 best 12753\nils 232 best 12753\nils 233 best 12753\nils 234 best 12753\nils 235 best 12753\nils 237 best 12753\nils 238 best 12753\nils 241 best 12753\nils 242 best 12753\nils 244 best 12753\nils 245 best 12753\nils 246 best 12753\nils 247 best 12753\nils 248 best 12753\nils 249 best 12753\nils 250 best 12753\nils 251 best 12753\nils 253 best 12753\nils 255 best 12753\nils 257 best 12753\nils 263 best 12753\nils 264 best 12753\nils 265 best 12753\nils 267 best 12753\nils 268 best 12753\nils 272 best 12753\nils 273 best 12753\nils 274 best 12753\nils 275 best 12753\nils 276 best 12753\nils 277 best 12753\nils 278 best 12753\nils 279 best 12753\nils 280 best 12753\nils 281 best 12753\nils 283 best 12753\nils 285 best 12753\nils 286 best 12753\nils 287 best 12753\nils 288 best 12753\nils 289 best 12753\nils 290 best 12753\nils 291 best 12753\nils 293 best 12753\nils 294 best 12753\nils 295 best 12753\nils 296 best 12753\nils 297 best 12753\nils 298 best 12753\nils 299 best 12753\nils 300 best 12753\nils 301 best 12753\nils 302 best 12753\nils 304 best 12753\nils 305 best 12753\nils 306 best 12753\nils 308 best 12753\nils 310 best 12753\nils 311 best 12753\nils 312 best 12753\nils 313 best 12753\nils 314 best 12753\nils 315 best 12753\nils 317 best 12753\nils 318 best 12753\nils 319 best 12753\nils 320 best 12753\nils 321 best 12753\nils 323 best 12753\nils 325 best 12753\nils 326 best 12753\nils 327 best 12753\nils 328 best 12753\nils 329 best 12753\nils 330 best 12753\nils 332 best 12753\nils 333 best 12753\nils 334 best 12753\nils 335 best 12753\nils 336 best 12753\nils 337 best 12753\nils 341 best 12753\nils 342 best 12753\nils 343 best 12753\nils 344 best 12753\nils 345 best 12753\nils 346 best 12753\nils 347 best 12753\nils 348 best 12753\nils 349 best 12753\nils 350 best 12753\nils 351 best 12753\nils 352 best 12753\nils 354 best 12753\nils 355 best 12753\nils 356 best 12753\nils 357 best 12753\nils 359 best 12753\nils 360 best 12753\nils 363 best 12753\nils 364 best 12753\nils 365 best 12753\nils 368 best 12753\nils 369 best 12753\nils 371 best 12753\nils 372 best 12753\nils 373 best 12753\nils 374 best 12753\nils 376 best 12753\nils 378 best 12753\nils 380 best 12753\nils 382 best 12753\nils 385 best 12753\nils 386 best 12753\nils 388 best 12753\nils 389 best 12753\nils 391 best 12753\nils 393 best 12753\nils 394 best 12753\nils 395 best 12753\nils 397 best 12753\nils 398 best 12753\nils 399 best 12753\nils 400 best 12753\nils 401 best 12753\nils 402 best 12753\nils 403 best 12753\nils 405 best 12753\nils 406 best 12753\nils 409 best 12753\nils 410 best 12753\nils 411 best 12753\nils 412 best 12753\nils 413 best 12753\nils 414 best 12753\nils 415 best 12753\nils 416 best 12753\nils 417 best 12753\nils 419 best 12753\nils 421 best 12753\nils 423 best 12753\nils 424 best 12753\nils 425 best 12753\nils 426 best 12753\nils 427 best 12753\nils 428 best 12753\nils 429 best 12753\nils 430 best 12753\nils 431 best 12753\nils 434 best 12753\nils 436 best 12753\nils 439 best 12753\nils 440 best 12753\nils 441 best 12753\nils 442 best 12753\nils 444 best 12753\nils 445 best 12753\nils 446 best 12753\nils 447 best 12753\nils 448 best 12753\nils 449 best 12753\nils 450 best 12753\nils 451 best 12753\nils 452 best 12753\nils 453 best 12753\nils 454 best 12753\nils 455 best 12753\nils 457 best 12753\nils 460 best 12753\nils 462 best 12753\nils 463 best 12753\nils 465 best 12753\nils 467 best 12753\nils 468 best 12753\nils 469 best 12753\nils 470 best 12753\nils 471 best 12753\nils 472 best 12753\nils 473 best 12753\nils 474 best 12753\nils 475 best 12753\nils 476 best 12753\nils 477 best 12753\nils 480 best 12753\nils 481 best 12753\nils 482 best 12753\nils 483 best 12753\nils 484 best 12753\nils 485 best 12753\nils 487 best 12753\nils 488 best 12753\nils 489 best 12753\nils 490 best 12753\nils 491 best 12753\nils 492 best 12753\nils 493 best 12753\nils 494 best 12753\nils 495 best 12753\nils 496 best 12753\nils 497 best 12753\nils 498 best 12753\nils 499 best 12753\nfinal 12753",
   "vmhwm_bytes": 679936,
   "wrapper_maxrss_bytes": 1978368
  },
  {
   "args": [
    "pi2.txt",
    "drift8002.txt",
    "500",
    "8007",
    "10",
    "drift8007.txt"
   ],
   "binary": "np_ils6",
   "charged_peak_bytes": 1005803,
   "image": {
    "bss": 790848,
    "data": 24,
    "image": 813887,
    "text": 23015
   },
   "name": "plateau-drift two-column local search (pass 10)",
   "outputs": {
    "drift8007.txt": "f03f82e1c62afb6c39b1a54fded635ecfd1b2266ca508fa5ae849eb577e66118"
   },
   "retained_input_output_bytes": 60844,
   "seconds": 303.47,
   "stack_reserve": 131072,
   "stdout": "start 12753\nils 0 best 12753\nils 2 best 12753\nils 3 best 12753\nils 5 best 12753\nils 6 best 12753\nils 7 best 12753\nils 8 best 12753\nils 9 best 12753\nils 10 best 12753\nils 12 best 12753\nils 13 best 12753\nils 14 best 12753\nils 15 best 12753\nils 16 best 12753\nils 19 best 12753\nils 21 best 12753\nils 22 best 12753\nils 24 best 12753\nils 25 best 12752\nils 26 best 12752\nils 28 best 12752\nils 29 best 12752\nils 30 best 12752\nils 32 best 12752\nils 35 best 12752\nils 36 best 12752\nils 37 best 12752\nils 38 best 12752\nils 40 best 12752\nils 42 best 12752\nils 46 best 12752\nils 47 best 12752\nils 49 best 12752\nils 50 best 12752\nils 51 best 12752\nils 52 best 12752\nils 54 best 12752\nils 56 best 12752\nils 57 best 12752\nils 60 best 12752\nils 61 best 12752\nils 62 best 12752\nils 64 best 12752\nils 65 best 12752\nils 66 best 12752\nils 67 best 12752\nils 68 best 12752\nils 69 best 12752\nils 72 best 12752\nils 74 best 12752\nils 76 best 12752\nils 78 best 12752\nils 79 best 12752\nils 81 best 12752\nils 84 best 12752\nils 85 best 12752\nils 86 best 12752\nils 87 best 12752\nils 88 best 12752\nils 90 best 12752\nils 91 best 12752\nils 92 best 12752\nils 93 best 12752\nils 94 best 12752\nils 96 best 12752\nils 97 best 12752\nils 100 best 12752\nils 101 best 12752\nils 102 best 12752\nils 103 best 12752\nils 104 best 12752\nils 105 best 12752\nils 106 best 12752\nils 107 best 12752\nils 108 best 12752\nils 109 best 12752\nils 110 best 12752\nils 111 best 12752\nils 113 best 12752\nils 114 best 12752\nils 115 best 12752\nils 116 best 12752\nils 117 best 12752\nils 118 best 12752\nils 119 best 12752\nils 120 best 12752\nils 121 best 12752\nils 122 best 12752\nils 123 best 12752\nils 124 best 12752\nils 125 best 12752\nils 126 best 12752\nils 128 best 12752\nils 129 best 12752\nils 130 best 12752\nils 131 best 12752\nils 132 best 12752\nils 134 best 12752\nils 135 best 12752\nils 137 best 12752\nils 138 best 12752\nils 139 best 12752\nils 141 best 12752\nils 143 best 12752\nils 145 best 12752\nils 146 best 12752\nils 147 best 12752\nils 149 best 12752\nils 150 best 12752\nils 151 best 12752\nils 152 best 12752\nils 153 best 12752\nils 154 best 12752\nils 155 best 12752\nils 156 best 12752\nils 157 best 12752\nils 158 best 12752\nils 159 best 12752\nils 160 best 12752\nils 162 best 12752\nils 163 best 12752\nils 164 best 12752\nils 166 best 12752\nils 168 best 12752\nils 169 best 12752\nils 171 best 12752\nils 173 best 12752\nils 174 best 12752\nils 175 best 12752\nils 176 best 12752\nils 177 best 12752\nils 178 best 12752\nils 179 best 12752\nils 180 best 12752\nils 181 best 12752\nils 184 best 12752\nils 185 best 12752\nils 187 best 12752\nils 188 best 12752\nils 189 best 12752\nils 190 best 12752\nils 191 best 12752\nils 192 best 12752\nils 195 best 12752\nils 197 best 12752\nils 198 best 12752\nils 200 best 12752\nils 201 best 12752\nils 203 best 12752\nils 204 best 12752\nils 205 best 12752\nils 206 best 12752\nils 207 best 12752\nils 208 best 12752\nils 209 best 12752\nils 210 best 12752\nils 211 best 12752\nils 212 best 12752\nils 213 best 12752\nils 214 best 12752\nils 215 best 12752\nils 216 best 12752\nils 219 best 12752\nils 220 best 12752\nils 222 best 12752\nils 224 best 12752\nils 226 best 12752\nils 227 best 12752\nils 228 best 12752\nils 229 best 12752\nils 230 best 12752\nils 231 best 12752\nils 232 best 12752\nils 234 best 12752\nils 235 best 12752\nils 238 best 12752\nils 241 best 12752\nils 242 best 12752\nils 243 best 12752\nils 244 best 12752\nils 246 best 12752\nils 247 best 12752\nils 248 best 12752\nils 249 best 12752\nils 250 best 12752\nils 252 best 12752\nils 253 best 12752\nils 255 best 12752\nils 256 best 12752\nils 258 best 12752\nils 259 best 12752\nils 260 best 12752\nils 263 best 12752\nils 264 best 12752\nils 265 best 12752\nils 266 best 12752\nils 267 best 12752\nils 270 best 12752\nils 271 best 12752\nils 272 best 12752\nils 273 best 12752\nils 274 best 12752\nils 277 best 12752\nils 278 best 12752\nils 279 best 12752\nils 280 best 12752\nils 281 best 12752\nils 282 best 12752\nils 284 best 12752\nils 285 best 12752\nils 286 best 12752\nils 289 best 12752\nils 294 best 12752\nils 296 best 12752\nils 298 best 12752\nils 299 best 12752\nils 300 best 12752\nils 301 best 12752\nils 302 best 12752\nils 304 best 12752\nils 305 best 12752\nils 306 best 12752\nils 307 best 12752\nils 311 best 12752\nils 312 best 12752\nils 314 best 12752\nils 315 best 12752\nils 316 best 12752\nils 317 best 12752\nils 318 best 12752\nils 319 best 12752\nils 320 best 12752\nils 321 best 12752\nils 322 best 12752\nils 324 best 12752\nils 325 best 12752\nils 326 best 12752\nils 327 best 12752\nils 334 best 12752\nils 335 best 12752\nils 336 best 12752\nils 337 best 12752\nils 338 best 12752\nils 339 best 12752\nils 340 best 12752\nils 341 best 12752\nils 342 best 12752\nils 343 best 12752\nils 344 best 12752\nils 345 best 12752\nils 348 best 12752\nils 349 best 12752\nils 350 best 12752\nils 351 best 12752\nils 354 best 12752\nils 356 best 12752\nils 357 best 12752\nils 358 best 12752\nils 360 best 12752\nils 361 best 12752\nils 362 best 12752\nils 366 best 12752\nils 367 best 12752\nils 370 best 12752\nils 373 best 12752\nils 374 best 12752\nils 375 best 12752\nils 376 best 12752\nils 377 best 12752\nils 378 best 12752\nils 379 best 12752\nils 381 best 12752\nils 383 best 12752\nils 384 best 12752\nils 385 best 12752\nils 388 best 12752\nils 393 best 12752\nils 396 best 12752\nils 401 best 12752\nils 402 best 12752\nils 403 best 12752\nils 404 best 12752\nils 405 best 12752\nils 406 best 12752\nils 408 best 12752\nils 409 best 12752\nils 410 best 12752\nils 411 best 12752\nils 412 best 12752\nils 413 best 12752\nils 414 best 12752\nils 415 best 12752\nils 416 best 12752\nils 417 best 12752\nils 418 best 12752\nils 419 best 12752\nils 422 best 12752\nils 423 best 12752\nils 424 best 12752\nils 426 best 12752\nils 427 best 12752\nils 428 best 12752\nils 429 best 12752\nils 431 best 12752\nils 432 best 12752\nils 434 best 12752\nils 435 best 12752\nils 436 best 12752\nils 438 best 12752\nils 439 best 12752\nils 441 best 12752\nils 443 best 12752\nils 446 best 12752\nils 447 best 12752\nils 448 best 12752\nils 449 best 12752\nils 450 best 12752\nils 452 best 12752\nils 453 best 12752\nils 454 best 12752\nils 455 best 12752\nils 459 best 12752\nils 460 best 12752\nils 463 best 12752\nils 464 best 12752\nils 465 best 12752\nils 466 best 12752\nils 468 best 12752\nils 470 best 12752\nils 472 best 12752\nils 475 best 12752\nils 476 best 12752\nils 477 best 12752\nils 480 best 12752\nils 481 best 12752\nils 483 best 12752\nils 485 best 12752\nils 487 best 12752\nils 488 best 12752\nils 490 best 12752\nils 491 best 12752\nils 492 best 12752\nils 496 best 12752\nils 497 best 12752\nils 498 best 12752\nils 499 best 12752\nfinal 12752",
   "vmhwm_bytes": 675840,
   "wrapper_maxrss_bytes": 1974272
  },
  {
   "args": [
    "pi2.txt",
    "drift8007.txt",
    "6000",
    "57",
    "3",
    "drift0057.txt"
   ],
   "binary": "np_ils2",
   "charged_peak_bytes": 574718,
   "image": {
    "bss": 371584,
    "data": 24,
    "image": 382802,
    "text": 11194
   },
   "name": "second joint ILS over round-1 targets and the pass-10 plan",
   "outputs": {
    "drift0057.txt": "8b050381bb8e5079cc89ab825463a7901f5ded95b432ce97988fdcf2cf873088"
   },
   "retained_input_output_bytes": 60844,
   "seconds": 334.19,
   "stack_reserve": 131072,
   "stdout": "start 12752\nfinal 12752",
   "vmhwm_bytes": 307200,
   "wrapper_maxrss_bytes": 1978368
  },
  {
   "args": [
    "pi2.txt",
    "drift8007.txt",
    "108",
    "8105",
    "10",
    "drift8105.txt"
   ],
   "binary": "np_ils6",
   "charged_peak_bytes": 1005803,
   "image": {
    "bss": 790848,
    "data": 24,
    "image": 813887,
    "text": 23015
   },
   "name": "narrow plateau-drift stop (pass 12)",
   "outputs": {
    "drift8105.txt": "5d4a5898b423c2099f84be358f5493429323ba8152f4a0333bb25a0527bf68b5"
   },
   "retained_input_output_bytes": 60844,
   "seconds": 64.29,
   "stack_reserve": 131072,
   "stdout": "start 12752\nils 0 best 12752\nils 1 best 12752\nils 2 best 12752\nils 5 best 12752\nils 8 best 12752\nils 10 best 12752\nils 11 best 12752\nils 13 best 12752\nils 14 best 12752\nils 15 best 12752\nils 16 best 12752\nils 17 best 12752\nils 18 best 12752\nils 19 best 12752\nils 21 best 12752\nils 22 best 12752\nils 25 best 12752\nils 26 best 12752\nils 27 best 12752\nils 28 best 12752\nils 29 best 12752\nils 30 best 12752\nils 31 best 12752\nils 32 best 12752\nils 33 best 12752\nils 34 best 12752\nils 35 best 12752\nils 36 best 12752\nils 37 best 12752\nils 38 best 12752\nils 39 best 12752\nils 40 best 12752\nils 41 best 12752\nils 43 best 12752\nils 44 best 12752\nils 45 best 12752\nils 47 best 12752\nils 49 best 12752\nils 50 best 12752\nils 52 best 12752\nils 53 best 12752\nils 54 best 12752\nils 56 best 12752\nils 58 best 12752\nils 60 best 12752\nils 61 best 12752\nils 62 best 12752\nils 64 best 12752\nils 65 best 12752\nils 67 best 12752\nils 69 best 12752\nils 71 best 12752\nils 72 best 12752\nils 73 best 12752\nils 74 best 12752\nils 76 best 12752\nils 77 best 12752\nils 79 best 12752\nils 82 best 12752\nils 84 best 12752\nils 86 best 12752\nils 87 best 12752\nils 88 best 12752\nils 89 best 12752\nils 90 best 12752\nils 91 best 12752\nils 92 best 12752\nils 93 best 12752\nils 94 best 12752\nils 95 best 12752\nils 96 best 12752\nils 97 best 12752\nils 98 best 12752\nils 99 best 12752\nils 101 best 12752\nils 102 best 12752\nils 104 best 12752\nils 105 best 12752\nils 106 best 12752\nils 107 best 12752\nfinal 12752",
   "vmhwm_bytes": 675840,
   "wrapper_maxrss_bytes": 1982464
  },
  {
   "args": [
    "pi2.txt",
    "drift8105.txt",
    "6000",
    "9206",
    "10",
    "drift9206.txt",
    "dump9206"
   ],
   "binary": "np_ils7",
   "charged_peak_bytes": 1007451,
   "image": {
    "bss": 792160,
    "data": 24,
    "image": 815535,
    "text": 23351
   },
   "name": "long plateau drift (pass 13)",
   "outputs": {
    "drift9206.txt": "c179ec0c9593d0d7a4ea7d67326cafbcc2f4c1290f568caf4496f7cda5b83044"
   },
   "retained_input_output_bytes": 60844,
   "seconds": 3633.87,
   "stack_reserve": 131072,
   "stdout": "start 12752\nils 0 best 12752\nils 1 best 12752\nils 2 best 12752\nils 4 best 12752\nils 5 best 12752\nils 6 best 12752\nils 7 best 12752\nils 8 best 12752\nils 10 best 12752\nils 12 best 12752\nils 13 best 12752\nils 14 best 12752\nils 15 best 12752\nils 16 best 12752\nils 17 best 12752\nils 18 best 12752\nils 19 best 12752\nils 20 best 12752\nils 21 best 12752\nils 22 best 12752\nils 25 best 12752\nils 28 best 12752\nils 29 best 12752\nils 32 best 12752\nils 33 best 12752\nils 34 best 12752\nils 35 best 12752\nils 36 best 12752\nils 37 best 12752\nils 38 best 12752\nils 39 best 12752\nils 41 best 12752\nils 42 best 12752\nils 43 best 12752\nils 45 best 12752\nils 46 best 12752\nils 47 best 12752\nils 48 best 12752\nils 50 best 12752\nils 51 best 12752\nils 52 best 12752\nils 53 best 12752\nils 54 best 12752\nils 55 best 12752\nils 56 best 12752\nils 57 best 12752\nils 58 best 12752\nils 59 best 12752\nils 61 best 12752\nils 62 best 12752\nils 63 best 12752\nils 64 best 12752\nils 65 best 12752\nils 67 best 12752\nils 68 best 12752\nils 70 best 12752\nils 71 best 12752\nils 72 best 12752\nils 73 best 12752\nils 74 best 12752\nils 76 best 12752\nils 77 best 12752\nils 79 best 12752\nils 80 best 12752\nils 81 best 12752\nils 82 best 12752\nils 83 best 12752\nils 84 best 12752\nils 85 best 12752\nils 86 best 12752\nils 87 best 12752\nils 88 best 12752\nils 90 best 12752\nils 91 best 12752\nils 92 best 12752\nils 93 best 12752\nils 94 best 12752\nils 95 best 12752\nils 97 best 12752\nils 98 best 12752\nils 99 best 12752\nils 102 best 12752\nils 103 best 12752\nils 104 best 12752\nils 105 best 12752\nils 106 best 12752\nils 109 best 12752\nils 110 best 12752\nils 111 best 12752\nils 112 best 12752\nils 113 best 12752\nils 114 best 12752\nils 115 best 12752\nils 116 best 12752\nils 117 best 12752\nils 118 best 12752\nils 120 best 12752\nils 121 best 12752\nils 124 best 12752\nils 125 best 12752\nils 126 best 12752\nils 127 best 12752\nils 128 best 12752\nils 130 best 12752\nils 133 best 12752\nils 134 best 12752\nils 135 best 12752\nils 136 best 12752\nils 137 best 12752\nils 138 best 12752\nils 139 best 12752\nils 140 best 12752\nils 141 best 12752\nils 142 best 12752\nils 143 best 12752\nils 144 best 12752\nils 145 best 12752\nils 146 best 12752\nils 147 best 12752\nils 148 best 12752\nils 149 best 12752\nils 150 best 12752\nils 151 best 12752\nils 152 best 12752\nils 153 best 12752\nils 154 best 12752\nils 155 best 12752\nils 156 best 12752\nils 157 best 12752\nils 158 best 12752\nils 160 best 12752\nils 161 best 12752\nils 163 best 12752\nils 164 best 12752\nils 165 best 12752\nils 166 best 12752\nils 167 best 12752\nils 168 best 12752\nils 170 best 12752\nils 171 best 12752\nils 172 best 12752\nils 173 best 12752\nils 174 best 12752\nils 175 best 12752\nils 176 best 12752\nils 178 best 12752\nils 179 best 12752\nils 180 best 12752\nils 181 best 12752\nils 182 best 12752\nils 184 best 12752\nils 185 best 12752\nils 186 best 12752\nils 187 best 12752\nils 188 best 12752\nils 189 best 12752\nils 190 best 12752\nils 192 best 12752\nils 193 best 12752\nils 194 best 12752\nils 195 best 12752\nils 196 best 12752\nils 197 best 12752\nils 198 best 12752\nils 203 best 12752\nils 204 best 12752\nils 206 best 12752\nils 207 best 12752\nils 208 best 12752\nils 209 best 12752\nils 210 best 12752\nils 213 best 12752\nils 214 best 12752\nils 215 best 12752\nils 216 best 12752\nils 217 best 12752\nils 218 best 12752\nils 220 best 12752\nils 223 best 12752\nils 224 best 12752\nils 225 best 12752\nils 227 best 12752\nils 228 best 12752\nils 231 best 12752\nils 232 best 12752\nils 234 best 12752\nils 236 best 12752\nils 239 best 12752\nils 240 best 12752\nils 241 best 12752\nils 242 best 12752\nils 243 best 12752\nils 244 best 12752\nils 245 best 12752\nils 246 best 12752\nils 247 best 12752\nils 248 best 12752\nils 249 best 12752\nils 250 best 12752\nils 252 best 12752\nils 254 best 12752\nils 255 best 12752\nils 257 best 12752\nils 259 best 12752\nils 260 best 12752\nils 261 best 12752\nils 264 best 12752\nils 265 best 12752\nils 268 best 12752\nils 269 best 12752\nils 271 best 12752\nils 272 best 12752\nils 273 best 12752\nils 276 best 12752\nils 279 best 12752\nils 280 best 12752\nils 283 best 12752\nils 284 best 12752\nils 285 best 12752\nils 286 best 12752\nils 287 best 12752\nils 289 best 12752\nils 290 best 12752\nils 291 best 12752\nils 292 best 12752\nils 293 best 12752\nils 294 best 12752\nils 295 best 12752\nils 296 best 12752\nils 298 best 12752\nils 300 best 12752\nils 301 best 12752\nils 303 best 12752\nils 304 best 12752\nils 306 best 12752\nils 307 best 12752\nils 310 best 12752\nils 311 best 12752\nils 313 best 12752\nils 314 best 12752\nils 316 best 12752\nils 317 best 12752\nils 318 best 12752\nils 319 best 12752\nils 320 best 12752\nils 321 best 12752\nils 322 best 12752\nils 324 best 12752\nils 325 best 12752\nils 327 best 12752\nils 328 best 12752\nils 329 best 12752\nils 330 best 12752\nils 331 best 12752\nils 333 best 12752\nils 335 best 12752\nils 336 best 12752\nils 338 best 12752\nils 340 best 12752\nils 341 best 12752\nils 342 best 12752\nils 343 best 12752\nils 345 best 12752\nils 346 best 12752\nils 348 best 12752\nils 349 best 12752\nils 352 best 12752\nils 353 best 12752\nils 355 best 12752\nils 357 best 12752\nils 358 best 12752\nils 359 best 12752\nils 360 best 12752\nils 361 best 12752\nils 362 best 12752\nils 363 best 12752\nils 364 best 12752\nils 365 best 12752\nils 366 best 12752\nils 367 best 12752\nils 368 best 12752\nils 369 best 12752\nils 370 best 12752\nils 371 best 12752\nils 373 best 12752\nils 375 best 12752\nils 376 best 12752\nils 377 best 12752\nils 378 best 12752\nils 379 best 12752\nils 382 best 12752\nils 383 best 12752\nils 384 best 12752\nils 386 best 12752\nils 387 best 12752\nils 390 best 12752\nils 391 best 12752\nils 394 best 12752\nils 396 best 12752\nils 398 best 12752\nils 399 best 12752\nils 400 best 12752\nils 401 best 12752\nils 403 best 12752\nils 404 best 12752\nils 406 best 12752\nils 407 best 12752\nils 408 best 12752\nils 409 best 12752\nils 410 best 12752\nils 412 best 12752\nils 413 best 12752\nils 414 best 12752\nils 417 best 12752\nils 418 best 12752\nils 420 best 12752\nils 422 best 12752\nils 424 best 12752\nils 425 best 12752\nils 426 best 12752\nils 427 best 12752\nils 429 best 12752\nils 430 best 12752\nils 432 best 12752\nils 433 best 12752\nils 434 best 12752\nils 439 best 12752\nils 440 best 12752\nils 441 best 12752\nils 442 best 12752\nils 444 best 12752\nils 446 best 12752\nils 447 best 12752\nils 448 best 12752\nils 449 best 12752\nils 452 best 12752\nils 454 best 12752\nils 456 best 12752\nils 457 best 12752\nils 458 best 12752\nils 459 best 12752\nils 460 best 12752\nils 461 best 12752\nils 464 best 12752\nils 467 best 12752\nils 469 best 12752\nils 470 best 12752\nils 471 best 12752\nils 472 best 12752\nils 473 best 12752\nils 474 best 12752\nils 475 best 12752\nils 476 best 12752\nils 477 best 12752\nils 478 best 12752\nils 479 best 12752\nils 480 best 12752\nils 481 best 12752\nils 482 best 12752\nils 483 best 12752\nils 484 best 12752\nils 485 best 12752\nils 486 best 12752\nils 487 best 12752\nils 488 best 12752\nils 489 best 12752\nils 490 best 12752\nils 491 best 12752\nils 492 best 12752\nils 493 best 12752\nils 494 best 12752\nils 496 best 12752\nils 497 best 12752\nils 498 best 12752\nils 499 best 12752\nils 500 best 12752\nils 501 best 12752\nils 502 best 12752\nils 503 best 12752\nils 504 best 12752\nils 506 best 12752\nils 507 best 12752\nils 508 best 12752\nils 510 best 12752\nils 511 best 12752\nils 512 best 12752\nils 513 best 12752\nils 514 best 12752\nils 515 best 12752\nils 517 best 12752\nils 518 best 12752\nils 519 best 12752\nils 520 best 12752\nils 522 best 12752\nils 523 best 12752\nils 525 best 12752\nils 526 best 12752\nils 528 best 12752\nils 529 best 12752\nils 531 best 12752\nils 532 best 12752\nils 533 best 12752\nils 534 best 12752\nils 535 best 12752\nils 536 best 12752\nils 537 best 12752\nils 538 best 12752\nils 539 best 12752\nils 540 best 12752\nils 542 best 12752\nils 543 best 12752\nils 544 best 12752\nils 545 best 12752\nils 546 best 12752\nils 547 best 12752\nils 548 best 12752\nils 549 best 12752\nils 550 best 12752\nils 552 best 12752\nils 554 best 12752\nils 555 best 12752\nils 558 best 12752\nils 559 best 12752\nils 561 best 12752\nils 562 best 12752\nils 563 best 12752\nils 564 best 12752\nils 566 best 12752\nils 568 best 12752\nils 569 best 12752\nils 571 best 12752\nils 572 best 12752\nils 573 best 12752\nils 576 best 12752\nils 577 best 12752\nils 578 best 12752\nils 579 best 12752\nils 580 best 12752\nils 581 best 12752\nils 582 best 12752\nils 583 best 12752\nils 585 best 12752\nils 586 best 12752\nils 587 best 12752\nils 588 best 12752\nils 589 best 12752\nils 590 best 12752\nils 591 best 12752\nils 594 best 12752\nils 595 best 12752\nils 598 best 12752\nils 599 best 12752\nils 600 best 12752\nils 601 best 12752\nils 602 best 12752\nils 603 best 12752\nils 604 best 12752\nils 605 best 12752\nils 606 best 12752\nils 607 best 12752\nils 608 best 12752\nils 609 best 12752\nils 610 best 12752\nils 611 best 12752\nils 612 best 12752\nils 613 best 12752\nils 614 best 12752\nils 615 best 12752\nils 616 best 12752\nils 617 best 12752\nils 618 best 12752\nils 619 best 12752\nils 620 best 12752\nils 625 best 12752\nils 626 best 12752\nils 629 best 12752\nils 630 best 12752\nils 631 best 12752\nils 633 best 12752\nils 635 best 12752\nils 636 best 12752\nils 637 best 12752\nils 639 best 12752\nils 640 best 12752\nils 642 best 12752\nils 643 best 12752\nils 644 best 12752\nils 645 best 12752\nils 646 best 12752\nils 649 best 12752\nils 651 best 12752\nils 652 best 12752\nils 653 best 12752\nils 655 best 12752\nils 656 best 12752\nils 657 best 12752\nils 659 best 12752\nils 661 best 12752\nils 662 best 12752\nils 663 best 12752\nils 664 best 12752\nils 665 best 12752\nils 666 best 12752\nils 667 best 12752\nils 668 best 12752\nils 671 best 12752\nils 672 best 12752\nils 673 best 12752\nils 675 best 12752\nils 676 best 12752\nils 677 best 12752\nils 680 best 12752\nils 681 best 12752\nils 682 best 12752\nils 683 best 12752\nils 684 best 12752\nils 685 best 12752\nils 686 best 12752\nils 687 best 12752\nils 688 best 12752\nils 689 best 12752\nils 690 best 12752\nils 691 best 12752\nils 692 best 12752\nils 693 best 12752\nils 697 best 12752\nils 698 best 12752\nils 699 best 12752\nils 700 best 12752\nils 701 best 12752\nils 703 best 12752\nils 704 best 12752\nils 705 best 12752\nils 707 best 12752\nils 709 best 12752\nils 710 best 12752\nils 711 best 12752\nils 712 best 12752\nils 713 best 12752\nils 714 best 12752\nils 715 best 12752\nils 716 best 12752\nils 717 best 12752\nils 718 best 12752\nils 720 best 12752\nils 721 best 12752\nils 723 best 12752\nils 724 best 12752\nils 725 best 12752\nils 726 best 12752\nils 728 best 12752\nils 729 best 12752\nils 730 best 12752\nils 733 best 12752\nils 735 best 12752\nils 736 best 12752\nils 739 best 12752\nils 740 best 12752\nils 741 best 12752\nils 742 best 12752\nils 743 best 12752\nils 744 best 12752\nils 746 best 12752\nils 747 best 12752\nils 748 best 12752\nils 749 best 12752\nils 750 best 12752\nils 751 best 12752\nils 752 best 12752\nils 753 best 12752\nils 754 best 12752\nils 755 best 12752\nils 756 best 12752\nils 758 best 12752\nils 759 best 12752\nils 760 best 12752\nils 761 best 12752\nils 762 best 12752\nils 763 best 12752\nils 764 best 12752\nils 766 best 12752\nils 767 best 12752\nils 768 best 12752\nils 770 best 12752\nils 772 best 12752\nils 773 best 12752\nils 774 best 12752\nils 775 best 12752\nils 776 best 12752\nils 778 best 12752\nils 779 best 12752\nils 780 best 12752\nils 781 best 12752\nils 783 best 12752\nils 787 best 12752\nils 789 best 12752\nils 790 best 12752\nils 791 best 12752\nils 792 best 12752\nils 793 best 12752\nils 794 best 12752\nils 795 best 12752\nils 796 best 12752\nils 797 best 12752\nils 798 best 12752\nils 799 best 12752\nils 801 best 12752\nils 802 best 12752\nils 803 best 12752\nils 804 best 12752\nils 805 best 12752\nils 806 best 12752\nils 807 best 12752\nils 808 best 12752\nils 809 best 12752\nils 810 best 12752\nils 811 best 12752\nils 812 best 12752\nils 813 best 12752\nils 815 best 12752\nils 816 best 12752\nils 818 best 12752\nils 819 best 12752\nils 821 best 12752\nils 822 best 12752\nils 823 best 12752\nils 825 best 12752\nils 826 best 12752\nils 827 best 12752\nils 828 best 12752\nils 829 best 12752\nils 830 best 12752\nils 831 best 12752\nils 832 best 12752\nils 833 best 12752\nils 834 best 12752\nils 835 best 12752\nils 836 best 12752\nils 838 best 12752\nils 839 best 12752\nils 840 best 12752\nils 841 best 12752\nils 842 best 12752\nils 843 best 12752\nils 846 best 12752\nils 848 best 12752\nils 849 best 12752\nils 850 best 12752\nils 851 best 12752\nils 853 best 12752\nils 855 best 12752\nils 859 best 12752\nils 860 best 12752\nils 861 best 12752\nils 862 best 12752\nils 863 best 12752\nils 864 best 12752\nils 865 best 12752\nils 868 best 12752\nils 870 best 12752\nils 871 best 12752\nils 872 best 12752\nils 874 best 12752\nils 875 best 12752\nils 878 best 12752\nils 879 best 12752\nils 880 best 12752\nils 881 best 12752\nils 882 best 12752\nils 884 best 12752\nils 887 best 12752\nils 888 best 12752\nils 889 best 12752\nils 892 best 12752\nils 893 best 12752\nils 895 best 12752\nils 896 best 12752\nils 897 best 12752\nils 898 best 12752\nils 899 best 12752\nils 900 best 12752\nils 901 best 12752\nils 902 best 12752\nils 903 best 12752\nils 904 best 12752\nils 907 best 12752\nils 909 best 12752\nils 910 best 12752\nils 911 best 12752\nils 912 best 12752\nils 913 best 12752\nils 914 best 12752\nils 915 best 12752\nils 916 best 12752\nils 919 best 12752\nils 920 best 12752\nils 921 best 12752\nils 923 best 12752\nils 925 best 12752\nils 928 best 12752\nils 929 best 12752\nils 930 best 12752\nils 931 best 12752\nils 932 best 12752\nils 933 best 12752\nils 934 best 12752\nils 935 best 12752\nils 936 best 12752\nils 937 best 12752\nils 938 best 12752\nils 940 best 12752\nils 941 best 12752\nils 942 best 12752\nils 943 best 12752\nils 944 best 12752\nils 945 best 12752\nils 946 best 12752\nils 948 best 12752\nils 949 best 12752\nils 951 best 12752\nils 953 best 12752\nils 955 best 12752\nils 956 best 12752\nils 959 best 12752\nils 960 best 12752\nils 962 best 12752\nils 963 best 12752\nils 965 best 12752\nils 967 best 12752\nils 968 best 12752\nils 969 best 12752\nils 970 best 12752\nils 971 best 12752\nils 972 best 12752\nils 973 best 12752\nils 974 best 12752\nils 975 best 12752\nils 976 best 12752\nils 980 best 12752\nils 982 best 12752\nils 983 best 12752\nils 984 best 12752\nils 985 best 12752\nils 986 best 12752\nils 987 best 12752\nils 988 best 12752\nils 989 best 12752\nils 990 best 12752\nils 991 best 12752\nils 992 best 12752\nils 994 best 12752\nils 995 best 12752\nils 998 best 12752\nils 999 best 12752\nils 1000 best 12752\nils 1002 best 12752\nils 1005 best 12752\nils 1007 best 12752\nils 1008 best 12752\nils 1010 best 12752\nils 1011 best 12752\nils 1012 best 12752\nils 1013 best 12752\nils 1014 best 12752\nils 1015 best 12752\nils 1016 best 12752\nils 1017 best 12752\nils 1018 best 12752\nils 1020 best 12752\nils 1021 best 12752\nils 1024 best 12752\nils 1026 best 12752\nils 1027 best 12752\nils 1029 best 12752\nils 1032 best 12752\nils 1033 best 12752\nils 1035 best 12752\nils 1038 best 12752\nils 1039 best 12752\nils 1040 best 12752\nils 1041 best 12752\nils 1042 best 12752\nils 1043 best 12752\nils 1045 best 12752\nils 1046 best 12752\nils 1047 best 12752\nils 1048 best 12752\nils 1052 best 12752\nils 1053 best 12752\nils 1055 best 12752\nils 1056 best 12752\nils 1057 best 12752\nils 1058 best 12752\nils 1059 best 12752\nils 1061 best 12752\nils 1062 best 12752\nils 1065 best 12752\nils 1066 best 12752\nils 1067 best 12752\nils 1069 best 12752\nils 1073 best 12752\nils 1074 best 12752\nils 1075 best 12752\nils 1076 best 12752\nils 1077 best 12752\nils 1079 best 12752\nils 1081 best 12752\nils 1082 best 12752\nils 1083 best 12752\nils 1084 best 12752\nils 1086 best 12752\nils 1087 best 12752\nils 1089 best 12752\nils 1090 best 12752\nils 1091 best 12752\nils 1092 best 12752\nils 1094 best 12752\nils 1097 best 12752\nils 1098 best 12752\nils 1101 best 12752\nils 1102 best 12752\nils 1103 best 12752\nils 1104 best 12752\nils 1105 best 12752\nils 1106 best 12752\nils 1107 best 12752\nils 1108 best 12752\nils 1109 best 12752\nils 1110 best 12752\nils 1111 best 12752\nils 1112 best 12752\nils 1113 best 12752\nils 1114 best 12752\nils 1115 best 12752\nils 1116 best 12752\nils 1117 best 12752\nils 1118 best 12752\nils 1119 best 12752\nils 1120 best 12752\nils 1121 best 12752\nils 1122 best 12752\nils 1123 best 12752\nils 1125 best 12752\nils 1126 best 12752\nils 1127 best 12752\nils 1128 best 12752\nils 1129 best 12752\nils 1130 best 12752\nils 1131 best 12752\nils 1132 best 12752\nils 1135 best 12752\nils 1136 best 12752\nils 1137 best 12752\nils 1138 best 12752\nils 1139 best 12752\nils 1140 best 12752\nils 1141 best 12752\nils 1145 best 12752\nils 1146 best 12752\nils 1147 best 12752\nils 1148 best 12752\nils 1149 best 12752\nils 1150 best 12752\nils 1151 best 12752\nils 1152 best 12752\nils 1154 best 12752\nils 1155 best 12752\nils 1156 best 12752\nils 1157 best 12752\nils 1158 best 12752\nils 1159 best 12752\nils 1160 best 12752\nils 1161 best 12752\nils 1162 best 12752\nils 1164 best 12752\nils 1165 best 12752\nils 1166 best 12752\nils 1167 best 12752\nils 1168 best 12752\nils 1170 best 12752\nils 1171 best 12752\nils 1172 best 12752\nils 1173 best 12752\nils 1177 best 12752\nils 1179 best 12752\nils 1180 best 12752\nils 1181 best 12752\nils 1182 best 12752\nils 1183 best 12752\nils 1184 best 12752\nils 1185 best 12752\nils 1189 best 12752\nils 1190 best 12752\nils 1191 best 12752\nils 1192 best 12752\nils 1195 best 12752\nils 1197 best 12752\nils 1198 best 12752\nils 1199 best 12752\nils 1200 best 12752\nils 1202 best 12752\nils 1203 best 12752\nils 1204 best 12752\nils 1205 best 12752\nils 1206 best 12752\nils 1207 best 12752\nils 1208 best 12752\nils 1209 best 12752\nils 1210 best 12752\nils 1211 best 12752\nils 1213 best 12752\nils 1215 best 12752\nils 1217 best 12752\nils 1218 best 12752\nils 1219 best 12752\nils 1220 best 12752\nils 1224 best 12752\nils 1225 best 12752\nils 1226 best 12752\nils 1227 best 12752\nils 1229 best 12752\nils 1234 best 12752\nils 1236 best 12752\nils 1238 best 12752\nils 1239 best 12752\nils 1241 best 12752\nils 1242 best 12752\nils 1243 best 12752\nils 1244 best 12752\nils 1245 best 12752\nils 1248 best 12752\nils 1251 best 12752\nils 1252 best 12752\nils 1254 best 12752\nils 1255 best 12752\nils 1257 best 12752\nils 1258 best 12752\nils 1260 best 12752\nils 1261 best 12752\nils 1262 best 12752\nils 1264 best 12752\nils 1265 best 12752\nils 1267 best 12752\nils 1269 best 12752\nils 1270 best 12752\nils 1272 best 12752\nils 1274 best 12752\nils 1275 best 12752\nils 1276 best 12752\nils 1277 best 12752\nils 1278 best 12752\nils 1279 best 12752\nils 1281 best 12752\nils 1282 best 12752\nils 1283 best 12752\nils 1284 best 12752\nils 1285 best 12752\nils 1287 best 12752\nils 1288 best 12752\nils 1289 best 12752\nils 1290 best 12752\nils 1291 best 12752\nils 1292 best 12752\nils 1293 best 12752\nils 1294 best 12752\nils 1295 best 12752\nils 1296 best 12752\nils 1297 best 12752\nils 1298 best 12752\nils 1300 best 12752\nils 1302 best 12752\nils 1305 best 12752\nils 1307 best 12752\nils 1308 best 12752\nils 1309 best 12752\nils 1310 best 12752\nils 1311 best 12752\nils 1312 best 12752\nils 1314 best 12752\nils 1315 best 12752\nils 1316 best 12752\nils 1317 best 12752\nils 1318 best 12752\nils 1319 best 12752\nils 1320 best 12752\nils 1321 best 12752\nils 1322 best 12752\nils 1323 best 12752\nils 1324 best 12752\nils 1325 best 12752\nils 1326 best 12752\nils 1327 best 12752\nils 1328 best 12752\nils 1330 best 12752\nils 1331 best 12752\nils 1332 best 12752\nils 1333 best 12752\nils 1334 best 12752\nils 1336 best 12752\nils 1338 best 12752\nils 1339 best 12752\nils 1340 best 12752\nils 1342 best 12752\nils 1343 best 12752\nils 1345 best 12752\nils 1347 best 12752\nils 1348 best 12752\nils 1349 best 12752\nils 1350 best 12752\nils 1352 best 12752\nils 1353 best 12752\nils 1354 best 12752\nils 1355 best 12752\nils 1356 best 12752\nils 1357 best 12752\nils 1358 best 12752\nils 1359 best 12752\nils 1360 best 12752\nils 1362 best 12752\nils 1363 best 12752\nils 1364 best 12752\nils 1366 best 12752\nils 1367 best 12752\nils 1368 best 12752\nils 1369 best 12752\nils 1370 best 12752\nils 1371 best 12752\nils 1374 best 12752\nils 1376 best 12752\nils 1377 best 12752\nils 1378 best 12752\nils 1379 best 12752\nils 1381 best 12752\nils 1383 best 12752\nils 1385 best 12752\nils 1387 best 12752\nils 1388 best 12752\nils 1389 best 12752\nils 1391 best 12752\nils 1392 best 12752\nils 1393 best 12752\nils 1395 best 12752\nils 1396 best 12752\nils 1397 best 12752\nils 1399 best 12752\nils 1400 best 12752\nils 1401 best 12752\nils 1402 best 12752\nils 1403 best 12752\nils 1404 best 12752\nils 1405 best 12752\nils 1406 best 12752\nils 1407 best 12752\nils 1408 best 12752\nils 1409 best 12752\nils 1410 best 12752\nils 1411 best 12752\nils 1412 best 12752\nils 1414 best 12752\nils 1415 best 12752\nils 1416 best 12752\nils 1418 best 12752\nils 1419 best 12752\nils 1420 best 12752\nils 1423 best 12752\nils 1424 best 12752\nils 1426 best 12752\nils 1428 best 12752\nils 1429 best 12752\nils 1431 best 12752\nils 1432 best 12752\nils 1437 best 12752\nils 1438 best 12752\nils 1439 best 12752\nils 1440 best 12752\nils 1441 best 12752\nils 1444 best 12752\nils 1446 best 12752\nils 1447 best 12752\nils 1448 best 12752\nils 1449 best 12752\nils 1450 best 12752\nils 1452 best 12752\nils 1454 best 12752\nils 1456 best 12752\nils 1457 best 12752\nils 1459 best 12752\nils 1460 best 12752\nils 1461 best 12752\nils 1462 best 12752\nils 1463 best 12752\nils 1464 best 12752\nils 1465 best 12752\nils 1466 best 12752\nils 1467 best 12752\nils 1468 best 12752\nils 1469 best 12752\nils 1470 best 12752\nils 1472 best 12752\nils 1473 best 12752\nils 1475 best 12752\nils 1476 best 12752\nils 1477 best 12752\nils 1478 best 12752\nils 1479 best 12752\nils 1480 best 12752\nils 1481 best 12752\nils 1482 best 12752\nils 1483 best 12752\nils 1485 best 12752\nils 1486 best 12752\nils 1489 best 12752\nils 1490 best 12752\nils 1491 best 12752\nils 1493 best 12752\nils 1496 best 12752\nils 1498 best 12752\nils 1499 best 12752\nils 1500 best 12752\nils 1501 best 12752\nils 1502 best 12752\nils 1504 best 12752\nils 1505 best 12752\nils 1506 best 12752\nils 1507 best 12752\nils 1509 best 12752\nils 1510 best 12752\nils 1512 best 12752\nils 1513 best 12752\nils 1514 best 12752\nils 1515 best 12752\nils 1516 best 12752\nils 1518 best 12752\nils 1519 best 12752\nils 1522 best 12752\nils 1523 best 12752\nils 1524 best 12752\nils 1525 best 12752\nils 1526 best 12752\nils 1527 best 12752\nils 1528 best 12752\nils 1529 best 12752\nils 1530 best 12752\nils 1531 best 12752\nils 1532 best 12752\nils 1533 best 12752\nils 1534 best 12752\nils 1536 best 12752\nils 1537 best 12752\nils 1538 best 12752\nils 1539 best 12752\nils 1540 best 12752\nils 1541 best 12752\nils 1542 best 12752\nils 1543 best 12752\nils 1544 best 12752\nils 1545 best 12752\nils 1546 best 12752\nils 1547 best 12752\nils 1548 best 12752\nils 1551 best 12752\nils 1552 best 12752\nils 1554 best 12752\nils 1555 best 12752\nils 1557 best 12752\nils 1559 best 12752\nils 1561 best 12752\nils 1562 best 12752\nils 1565 best 12752\nils 1566 best 12752\nils 1567 best 12752\nils 1568 best 12752\nils 1569 best 12752\nils 1571 best 12752\nils 1572 best 12752\nils 1573 best 12752\nils 1575 best 12752\nils 1576 best 12752\nils 1577 best 12752\nils 1578 best 12752\nils 1579 best 12752\nils 1580 best 12752\nils 1581 best 12752\nils 1582 best 12752\nils 1584 best 12752\nils 1585 best 12752\nils 1586 best 12752\nils 1587 best 12752\nils 1589 best 12752\nils 1591 best 12752\nils 1593 best 12752\nils 1594 best 12752\nils 1595 best 12752\nils 1596 best 12752\nils 1599 best 12752\nils 1600 best 12752\nils 1602 best 12752\nils 1604 best 12752\nils 1605 best 12752\nils 1606 best 12752\nils 1608 best 12752\nils 1609 best 12752\nils 1611 best 12752\nils 1612 best 12752\nils 1613 best 12752\nils 1614 best 12752\nils 1615 best 12752\nils 1616 best 12752\nils 1618 best 12752\nils 1619 best 12752\nils 1620 best 12752\nils 1621 best 12752\nils 1622 best 12752\nils 1623 best 12752\nils 1624 best 12752\nils 1625 best 12752\nils 1628 best 12752\nils 1629 best 12752\nils 1630 best 12752\nils 1632 best 12752\nils 1633 best 12752\nils 1634 best 12752\nils 1635 best 12752\nils 1636 best 12752\nils 1637 best 12752\nils 1638 best 12752\nils 1639 best 12752\nils 1640 best 12752\nils 1641 best 12752\nils 1642 best 12752\nils 1643 best 12752\nils 1645 best 12752\nils 1647 best 12752\nils 1648 best 12752\nils 1649 best 12752\nils 1651 best 12752\nils 1652 best 12752\nils 1653 best 12752\nils 1655 best 12752\nils 1656 best 12752\nils 1657 best 12752\nils 1658 best 12752\nils 1659 best 12752\nils 1660 best 12752\nils 1661 best 12752\nils 1662 best 12752\nils 1663 best 12752\nils 1665 best 12752\nils 1666 best 12752\nils 1667 best 12752\nils 1669 best 12752\nils 1670 best 12752\nils 1671 best 12752\nils 1672 best 12752\nils 1673 best 12752\nils 1674 best 12752\nils 1676 best 12752\nils 1677 best 12752\nils 1678 best 12752\nils 1681 best 12752\nils 1682 best 12752\nils 1683 best 12752\nils 1684 best 12752\nils 1686 best 12752\nils 1687 best 12752\nils 1688 best 12752\nils 1689 best 12752\nils 1690 best 12752\nils 1691 best 12752\nils 1692 best 12752\nils 1693 best 12752\nils 1695 best 12752\nils 1696 best 12752\nils 1698 best 12752\nils 1699 best 12752\nils 1700 best 12752\nils 1701 best 12752\nils 1702 best 12752\nils 1703 best 12752\nils 1705 best 12752\nils 1706 best 12752\nils 1707 best 12752\nils 1708 best 12752\nils 1711 best 12752\nils 1712 best 12752\nils 1713 best 12752\nils 1714 best 12752\nils 1715 best 12752\nils 1717 best 12752\nils 1719 best 12752\nils 1720 best 12752\nils 1722 best 12752\nils 1724 best 12752\nils 1725 best 12752\nils 1726 best 12752\nils 1727 best 12752\nils 1728 best 12752\nils 1730 best 12752\nils 1736 best 12752\nils 1737 best 12752\nils 1739 best 12752\nils 1740 best 12752\nils 1741 best 12752\nils 1742 best 12752\nils 1743 best 12752\nils 1745 best 12752\nils 1746 best 12752\nils 1747 best 12752\nils 1748 best 12752\nils 1749 best 12752\nils 1750 best 12752\nils 1751 best 12752\nils 1752 best 12752\nils 1754 best 12752\nils 1755 best 12752\nils 1756 best 12752\nils 1757 best 12752\nils 1759 best 12752\nils 1760 best 12752\nils 1761 best 12752\nils 1763 best 12752\nils 1766 best 12752\nils 1767 best 12752\nils 1770 best 12752\nils 1771 best 12752\nils 1773 best 12752\nils 1774 best 12752\nils 1775 best 12752\nils 1776 best 12752\nils 1777 best 12752\nils 1778 best 12752\nils 1779 best 12752\nils 1780 best 12752\nils 1782 best 12752\nils 1783 best 12752\nils 1784 best 12752\nils 1785 best 12752\nils 1786 best 12752\nils 1787 best 12752\nils 1788 best 12752\nils 1789 best 12752\nils 1790 best 12752\nils 1792 best 12752\nils 1793 best 12752\nils 1794 best 12752\nils 1795 best 12752\nils 1796 best 12752\nils 1800 best 12752\nils 1801 best 12752\nils 1802 best 12752\nils 1803 best 12752\nils 1807 best 12752\nils 1808 best 12752\nils 1809 best 12752\nils 1810 best 12752\nils 1811 best 12752\nils 1812 best 12752\nils 1813 best 12752\nils 1814 best 12752\nils 1815 best 12752\nils 1816 best 12752\nils 1821 best 12752\nils 1823 best 12752\nils 1824 best 12752\nils 1826 best 12752\nils 1827 best 12752\nils 1829 best 12752\nils 1830 best 12752\nils 1831 best 12752\nils 1832 best 12752\nils 1834 best 12752\nils 1835 best 12752\nils 1836 best 12752\nils 1837 best 12752\nils 1839 best 12752\nils 1840 best 12752\nils 1841 best 12752\nils 1842 best 12752\nils 1845 best 12752\nils 1846 best 12752\nils 1847 best 12752\nils 1848 best 12752\nils 1851 best 12752\nils 1852 best 12752\nils 1853 best 12752\nils 1854 best 12752\nils 1855 best 12752\nils 1856 best 12752\nils 1857 best 12752\nils 1858 best 12752\nils 1859 best 12752\nils 1861 best 12752\nils 1862 best 12752\nils 1863 best 12752\nils 1864 best 12752\nils 1865 best 12752\nils 1866 best 12752\nils 1868 best 12752\nils 1869 best 12752\nils 1870 best 12752\nils 1871 best 12752\nils 1872 best 12752\nils 1873 best 12752\nils 1874 best 12752\nils 1875 best 12752\nils 1876 best 12752\nils 1877 best 12752\nils 1878 best 12752\nils 1881 best 12752\nils 1883 best 12752\nils 1884 best 12752\nils 1885 best 12752\nils 1886 best 12752\nils 1887 best 12752\nils 1888 best 12752\nils 1889 best 12752\nils 1890 best 12752\nils 1891 best 12752\nils 1892 best 12752\nils 1893 best 12752\nils 1894 best 12752\nils 1895 best 12752\nils 1896 best 12752\nils 1897 best 12752\nils 1898 best 12752\nils 1900 best 12752\nils 1901 best 12752\nils 1902 best 12752\nils 1904 best 12752\nils 1905 best 12752\nils 1907 best 12752\nils 1908 best 12752\nils 1910 best 12752\nils 1911 best 12752\nils 1912 best 12752\nils 1913 best 12752\nils 1914 best 12752\nils 1915 best 12752\nils 1917 best 12752\nils 1918 best 12752\nils 1919 best 12752\nils 1921 best 12752\nils 1924 best 12752\nils 1927 best 12752\nils 1930 best 12752\nils 1931 best 12752\nils 1932 best 12752\nils 1934 best 12752\nils 1935 best 12752\nils 1937 best 12752\nils 1939 best 12752\nils 1940 best 12752\nils 1941 best 12752\nils 1942 best 12752\nils 1943 best 12752\nils 1944 best 12752\nils 1945 best 12752\nils 1946 best 12752\nils 1947 best 12752\nils 1948 best 12752\nils 1949 best 12752\nils 1950 best 12752\nils 1951 best 12752\nils 1952 best 12752\nils 1954 best 12752\nils 1955 best 12752\nils 1956 best 12752\nils 1957 best 12752\nils 1959 best 12752\nils 1960 best 12752\nils 1964 best 12752\nils 1966 best 12752\nils 1968 best 12752\nils 1969 best 12752\nils 1971 best 12752\nils 1972 best 12752\nils 1975 best 12752\nils 1976 best 12752\nils 1977 best 12752\nils 1978 best 12752\nils 1979 best 12752\nils 1980 best 12752\nils 1982 best 12752\nils 1983 best 12752\nils 1984 best 12752\nils 1987 best 12752\nils 1989 best 12752\nils 1991 best 12752\nils 1995 best 12752\nils 1996 best 12752\nils 1997 best 12752\nils 1999 best 12752\nils 2000 best 12752\nils 2001 best 12752\nils 2002 best 12752\nils 2003 best 12752\nils 2004 best 12752\nils 2005 best 12752\nils 2006 best 12752\nils 2007 best 12752\nils 2009 best 12752\nils 2010 best 12752\nils 2011 best 12752\nils 2012 best 12752\nils 2013 best 12752\nils 2014 best 12752\nils 2016 best 12752\nils 2017 best 12752\nils 2018 best 12752\nils 2020 best 12752\nils 2021 best 12752\nils 2022 best 12752\nils 2023 best 12752\nils 2024 best 12752\nils 2026 best 12752\nils 2027 best 12752\nils 2030 best 12752\nils 2032 best 12752\nils 2033 best 12752\nils 2034 best 12752\nils 2036 best 12752\nils 2037 best 12752\nils 2038 best 12752\nils 2039 best 12752\nils 2040 best 12752\nils 2041 best 12752\nils 2042 best 12752\nils 2045 best 12752\nils 2046 best 12752\nils 2048 best 12752\nils 2049 best 12752\nils 2050 best 12752\nils 2054 best 12752\nils 2055 best 12752\nils 2056 best 12752\nils 2057 best 12752\nils 2058 best 12752\nils 2059 best 12752\nils 2060 best 12752\nils 2061 best 12752\nils 2062 best 12752\nils 2063 best 12752\nils 2065 best 12752\nils 2072 best 12752\nils 2073 best 12752\nils 2074 best 12752\nils 2075 best 12752\nils 2076 best 12752\nils 2077 best 12752\nils 2078 best 12752\nils 2079 best 12752\nils 2080 best 12752\nils 2082 best 12752\nils 2083 best 12752\nils 2087 best 12752\nils 2088 best 12752\nils 2090 best 12752\nils 2091 best 12752\nils 2092 best 12752\nils 2095 best 12752\nils 2098 best 12752\nils 2099 best 12752\nils 2100 best 12752\nils 2102 best 12752\nils 2103 best 12752\nils 2104 best 12752\nils 2105 best 12752\nils 2106 best 12752\nils 2107 best 12752\nils 2108 best 12752\nils 2109 best 12752\nils 2110 best 12752\nils 2111 best 12752\nils 2112 best 12752\nils 2113 best 12752\nils 2114 best 12752\nils 2115 best 12752\nils 2116 best 12752\nils 2117 best 12752\nils 2118 best 12752\nils 2119 best 12752\nils 2120 best 12752\nils 2121 best 12752\nils 2123 best 12752\nils 2124 best 12752\nils 2125 best 12752\nils 2126 best 12752\nils 2127 best 12752\nils 2128 best 12752\nils 2130 best 12752\nils 2131 best 12752\nils 2133 best 12752\nils 2135 best 12752\nils 2136 best 12752\nils 2137 best 12752\nils 2138 best 12752\nils 2139 best 12752\nils 2140 best 12752\nils 2141 best 12752\nils 2143 best 12752\nils 2144 best 12752\nils 2146 best 12752\nils 2147 best 12752\nils 2148 best 12752\nils 2149 best 12752\nils 2151 best 12752\nils 2152 best 12752\nils 2153 best 12752\nils 2154 best 12752\nils 2155 best 12752\nils 2156 best 12752\nils 2157 best 12752\nils 2158 best 12752\nils 2163 best 12752\nils 2167 best 12752\nils 2171 best 12752\nils 2172 best 12752\nils 2173 best 12752\nils 2174 best 12752\nils 2175 best 12752\nils 2176 best 12752\nils 2177 best 12752\nils 2178 best 12752\nils 2179 best 12752\nils 2180 best 12752\nils 2181 best 12752\nils 2183 best 12752\nils 2184 best 12752\nils 2187 best 12752\nils 2188 best 12752\nils 2189 best 12752\nils 2190 best 12752\nils 2192 best 12752\nils 2194 best 12752\nils 2195 best 12752\nils 2196 best 12752\nils 2197 best 12752\nils 2198 best 12752\nils 2199 best 12752\nils 2201 best 12752\nils 2202 best 12752\nils 2203 best 12752\nils 2204 best 12752\nils 2206 best 12752\nils 2207 best 12752\nils 2208 best 12752\nils 2209 best 12752\nils 2210 best 12752\nils 2211 best 12752\nils 2213 best 12752\nils 2214 best 12752\nils 2215 best 12752\nils 2216 best 12752\nils 2218 best 12752\nils 2222 best 12752\nils 2224 best 12752\nils 2225 best 12752\nils 2226 best 12752\nils 2227 best 12752\nils 2230 best 12752\nils 2232 best 12752\nils 2233 best 12752\nils 2234 best 12752\nils 2235 best 12752\nils 2236 best 12752\nils 2239 best 12752\nils 2241 best 12752\nils 2243 best 12752\nils 2244 best 12752\nils 2245 best 12752\nils 2246 best 12752\nils 2247 best 12752\nils 2248 best 12752\nils 2249 best 12752\nils 2250 best 12752\nils 2251 best 12752\nils 2252 best 12752\nils 2253 best 12752\nils 2254 best 12752\nils 2255 best 12752\nils 2256 best 12752\nils 2257 best 12752\nils 2258 best 12752\nils 2259 best 12752\nils 2260 best 12752\nils 2261 best 12752\nils 2262 best 12752\nils 2263 best 12752\nils 2264 best 12752\nils 2265 best 12752\nils 2268 best 12752\nils 2269 best 12752\nils 2270 best 12752\nils 2272 best 12752\nils 2274 best 12752\nils 2275 best 12752\nils 2276 best 12752\nils 2277 best 12752\nils 2278 best 12752\nils 2279 best 12752\nils 2280 best 12752\nils 2281 best 12752\nils 2282 best 12752\nils 2285 best 12752\nils 2286 best 12752\nils 2287 best 12752\nils 2288 best 12752\nils 2289 best 12752\nils 2290 best 12752\nils 2291 best 12752\nils 2292 best 12752\nils 2293 best 12752\nils 2295 best 12752\nils 2296 best 12752\nils 2298 best 12752\nils 2299 best 12752\nils 2301 best 12752\nils 2304 best 12752\nils 2305 best 12752\nils 2307 best 12752\nils 2308 best 12752\nils 2309 best 12752\nils 2310 best 12752\nils 2311 best 12752\nils 2313 best 12752\nils 2314 best 12752\nils 2315 best 12752\nils 2317 best 12752\nils 2318 best 12752\nils 2319 best 12752\nils 2320 best 12752\nils 2321 best 12752\nils 2322 best 12752\nils 2324 best 12752\nils 2325 best 12752\nils 2326 best 12752\nils 2327 best 12752\nils 2328 best 12752\nils 2329 best 12752\nils 2330 best 12752\nils 2332 best 12752\nils 2333 best 12752\nils 2334 best 12752\nils 2335 best 12752\nils 2336 best 12752\nils 2337 best 12752\nils 2340 best 12752\nils 2341 best 12752\nils 2342 best 12752\nils 2343 best 12752\nils 2344 best 12752\nils 2345 best 12752\nils 2346 best 12752\nils 2348 best 12752\nils 2349 best 12752\nils 2350 best 12752\nils 2351 best 12752\nils 2352 best 12752\nils 2353 best 12752\nils 2354 best 12752\nils 2355 best 12752\nils 2357 best 12752\nils 2358 best 12752\nils 2359 best 12752\nils 2360 best 12752\nils 2361 best 12752\nils 2362 best 12752\nils 2363 best 12752\nils 2364 best 12752\nils 2367 best 12752\nils 2368 best 12752\nils 2369 best 12752\nils 2372 best 12752\nils 2373 best 12752\nils 2374 best 12752\nils 2375 best 12752\nils 2376 best 12752\nils 2377 best 12752\nils 2378 best 12752\nils 2379 best 12752\nils 2380 best 12752\nils 2381 best 12752\nils 2382 best 12752\nils 2383 best 12752\nils 2384 best 12752\nils 2386 best 12752\nils 2388 best 12752\nils 2389 best 12752\nils 2390 best 12752\nils 2391 best 12752\nils 2392 best 12752\nils 2393 best 12752\nils 2394 best 12752\nils 2395 best 12752\nils 2396 best 12752\nils 2398 best 12752\nils 2400 best 12752\nils 2401 best 12752\nils 2402 best 12752\nils 2403 best 12752\nils 2404 best 12752\nils 2405 best 12752\nils 2406 best 12752\nils 2408 best 12752\nils 2409 best 12752\nils 2410 best 12752\nils 2412 best 12752\nils 2413 best 12752\nils 2414 best 12752\nils 2415 best 12752\nils 2416 best 12752\nils 2417 best 12752\nils 2418 best 12752\nils 2421 best 12752\nils 2423 best 12752\nils 2424 best 12752\nils 2425 best 12752\nils 2426 best 12752\nils 2427 best 12752\nils 2430 best 12752\nils 2432 best 12752\nils 2433 best 12752\nils 2434 best 12752\nils 2436 best 12752\nils 2437 best 12752\nils 2438 best 12752\nils 2439 best 12752\nils 2440 best 12752\nils 2441 best 12752\nils 2442 best 12752\nils 2444 best 12752\nils 2446 best 12752\nils 2448 best 12752\nils 2449 best 12752\nils 2450 best 12752\nils 2451 best 12752\nils 2452 best 12752\nils 2453 best 12752\nils 2454 best 12752\nils 2455 best 12752\nils 2456 best 12752\nils 2457 best 12752\nils 2458 best 12752\nils 2459 best 12752\nils 2460 best 12752\nils 2461 best 12752\nils 2462 best 12752\nils 2463 best 12752\nils 2464 best 12752\nils 2465 best 12752\nils 2466 best 12752\nils 2468 best 12752\nils 2469 best 12752\nils 2471 best 12752\nils 2472 best 12752\nils 2473 best 12752\nils 2475 best 12752\nils 2477 best 12752\nils 2478 best 12752\nils 2480 best 12752\nils 2481 best 12752\nils 2486 best 12752\nils 2487 best 12752\nils 2488 best 12752\nils 2490 best 12752\nils 2491 best 12752\nils 2492 best 12752\nils 2493 best 12752\nils 2494 best 12752\nils 2495 best 12752\nils 2498 best 12752\nils 2499 best 12752\nils 2500 best 12752\nils 2501 best 12752\nils 2502 best 12752\nils 2503 best 12752\nils 2505 best 12752\nils 2506 best 12752\nils 2508 best 12752\nils 2509 best 12752\nils 2510 best 12752\nils 2511 best 12752\nils 2512 best 12752\nils 2513 best 12752\nils 2514 best 12752\nils 2515 best 12752\nils 2517 best 12752\nils 2519 best 12752\nils 2523 best 12752\nils 2524 best 12752\nils 2525 best 12752\nils 2526 best 12752\nils 2527 best 12752\nils 2528 best 12752\nils 2529 best 12752\nils 2530 best 12752\nils 2531 best 12752\nils 2532 best 12752\nils 2533 best 12752\nils 2534 best 12752\nils 2535 best 12752\nils 2536 best 12752\nils 2537 best 12752\nils 2542 best 12752\nils 2543 best 12752\nils 2544 best 12752\nils 2545 best 12752\nils 2547 best 12752\nils 2548 best 12752\nils 2549 best 12752\nils 2550 best 12752\nils 2551 best 12752\nils 2553 best 12752\nils 2555 best 12752\nils 2556 best 12752\nils 2557 best 12752\nils 2558 best 12752\nils 2559 best 12752\nils 2560 best 12752\nils 2561 best 12752\nils 2564 best 12752\nils 2565 best 12752\nils 2566 best 12752\nils 2570 best 12752\nils 2571 best 12752\nils 2572 best 12752\nils 2574 best 12752\nils 2575 best 12752\nils 2576 best 12752\nils 2577 best 12752\nils 2578 best 12752\nils 2579 best 12752\nils 2580 best 12752\nils 2581 best 12752\nils 2583 best 12752\nils 2584 best 12752\nils 2585 best 12752\nils 2586 best 12752\nils 2587 best 12752\nils 2589 best 12752\nils 2591 best 12752\nils 2592 best 12752\nils 2595 best 12752\nils 2596 best 12752\nils 2597 best 12752\nils 2598 best 12752\nils 2600 best 12752\nils 2602 best 12752\nils 2603 best 12752\nils 2604 best 12752\nils 2605 best 12752\nils 2606 best 12752\nils 2608 best 12752\nils 2612 best 12752\nils 2613 best 12752\nils 2614 best 12752\nils 2615 best 12752\nils 2616 best 12752\nils 2617 best 12752\nils 2618 best 12752\nils 2619 best 12752\nils 2621 best 12752\nils 2624 best 12752\nils 2625 best 12752\nils 2626 best 12752\nils 2627 best 12752\nils 2628 best 12752\nils 2629 best 12752\nils 2630 best 12752\nils 2631 best 12752\nils 2632 best 12752\nils 2634 best 12752\nils 2636 best 12752\nils 2637 best 12752\nils 2638 best 12752\nils 2639 best 12752\nils 2640 best 12752\nils 2643 best 12752\nils 2644 best 12752\nils 2646 best 12752\nils 2648 best 12752\nils 2649 best 12752\nils 2652 best 12752\nils 2653 best 12752\nils 2654 best 12752\nils 2655 best 12752\nils 2656 best 12752\nils 2657 best 12752\nils 2660 best 12752\nils 2661 best 12752\nils 2662 best 12752\nils 2664 best 12752\nils 2665 best 12752\nils 2667 best 12752\nils 2669 best 12752\nils 2670 best 12752\nils 2671 best 12752\nils 2672 best 12752\nils 2673 best 12752\nils 2674 best 12752\nils 2675 best 12752\nils 2677 best 12752\nils 2678 best 12752\nils 2680 best 12752\nils 2682 best 12752\nils 2684 best 12752\nils 2685 best 12752\nils 2686 best 12752\nils 2687 best 12752\nils 2688 best 12752\nils 2689 best 12752\nils 2690 best 12752\nils 2691 best 12752\nils 2696 best 12752\nils 2697 best 12752\nils 2700 best 12752\nils 2701 best 12752\nils 2702 best 12752\nils 2703 best 12752\nils 2704 best 12752\nils 2705 best 12752\nils 2706 best 12752\nils 2708 best 12752\nils 2710 best 12752\nils 2711 best 12752\nils 2712 best 12752\nils 2713 best 12752\nils 2714 best 12752\nils 2715 best 12752\nils 2716 best 12752\nils 2717 best 12752\nils 2718 best 12752\nils 2719 best 12752\nils 2721 best 12752\nils 2722 best 12752\nils 2723 best 12752\nils 2726 best 12752\nils 2727 best 12752\nils 2728 best 12752\nils 2729 best 12752\nils 2730 best 12752\nils 2732 best 12752\nils 2733 best 12752\nils 2734 best 12752\nils 2736 best 12752\nils 2737 best 12752\nils 2740 best 12752\nils 2742 best 12752\nils 2743 best 12752\nils 2744 best 12752\nils 2745 best 12752\nils 2747 best 12752\nils 2748 best 12752\nils 2749 best 12752\nils 2751 best 12752\nils 2752 best 12752\nils 2753 best 12752\nils 2756 best 12752\nils 2757 best 12752\nils 2758 best 12752\nils 2759 best 12752\nils 2760 best 12752\nils 2762 best 12752\nils 2763 best 12752\nils 2764 best 12752\nils 2765 best 12752\nils 2766 best 12752\nils 2767 best 12752\nils 2769 best 12752\nils 2770 best 12752\nils 2771 best 12752\nils 2774 best 12752\nils 2775 best 12752\nils 2776 best 12752\nils 2777 best 12752\nils 2778 best 12752\nils 2780 best 12752\nils 2781 best 12752\nils 2782 best 12752\nils 2783 best 12752\nils 2784 best 12752\nils 2785 best 12752\nils 2787 best 12752\nils 2788 best 12752\nils 2789 best 12752\nils 2790 best 12752\nils 2792 best 12752\nils 2793 best 12752\nils 2794 best 12752\nils 2795 best 12752\nils 2796 best 12752\nils 2797 best 12752\nils 2798 best 12752\nils 2799 best 12752\nils 2801 best 12752\nils 2803 best 12752\nils 2804 best 12752\nils 2808 best 12752\nils 2810 best 12752\nils 2811 best 12752\nils 2814 best 12752\nils 2815 best 12752\nils 2816 best 12752\nils 2817 best 12752\nils 2818 best 12752\nils 2819 best 12752\nils 2821 best 12752\nils 2822 best 12752\nils 2823 best 12752\nils 2824 best 12752\nils 2825 best 12752\nils 2826 best 12752\nils 2827 best 12752\nils 2828 best 12752\nils 2829 best 12752\nils 2830 best 12752\nils 2831 best 12752\nils 2832 best 12752\nils 2833 best 12752\nils 2834 best 12752\nils 2835 best 12752\nils 2836 best 12752\nils 2838 best 12752\nils 2839 best 12752\nils 2840 best 12752\nils 2841 best 12752\nils 2842 best 12752\nils 2843 best 12752\nils 2844 best 12752\nils 2846 best 12752\nils 2847 best 12752\nils 2848 best 12752\nils 2850 best 12752\nils 2851 best 12752\nils 2852 best 12752\nils 2855 best 12752\nils 2856 best 12752\nils 2857 best 12752\nils 2858 best 12752\nils 2859 best 12752\nils 2860 best 12752\nils 2861 best 12752\nils 2862 best 12752\nils 2863 best 12752\nils 2864 best 12752\nils 2865 best 12752\nils 2866 best 12752\nils 2867 best 12752\nils 2868 best 12752\nils 2869 best 12752\nils 2871 best 12752\nils 2872 best 12752\nils 2873 best 12752\nils 2874 best 12752\nils 2875 best 12752\nils 2878 best 12752\nils 2879 best 12752\nils 2882 best 12752\nils 2885 best 12752\nils 2886 best 12752\nils 2887 best 12752\nils 2890 best 12752\nils 2892 best 12752\nils 2893 best 12752\nils 2894 best 12752\nils 2895 best 12752\nils 2896 best 12752\nils 2898 best 12752\nils 2899 best 12752\nils 2901 best 12752\nils 2902 best 12752\nils 2903 best 12752\nils 2905 best 12752\nils 2906 best 12752\nils 2907 best 12752\nils 2908 best 12752\nils 2909 best 12752\nils 2911 best 12752\nils 2912 best 12752\nils 2913 best 12752\nils 2914 best 12752\nils 2917 best 12752\nils 2918 best 12752\nils 2920 best 12752\nils 2921 best 12752\nils 2922 best 12752\nils 2923 best 12752\nils 2925 best 12752\nils 2926 best 12752\nils 2927 best 12752\nils 2928 best 12752\nils 2929 best 12752\nils 2930 best 12752\nils 2931 best 12752\nils 2933 best 12752\nils 2934 best 12752\nils 2935 best 12752\nils 2936 best 12752\nils 2937 best 12752\nils 2938 best 12752\nils 2940 best 12752\nils 2942 best 12752\nils 2944 best 12752\nils 2945 best 12752\nils 2946 best 12752\nils 2948 best 12752\nils 2949 best 12752\nils 2953 best 12752\nils 2955 best 12752\nils 2956 best 12752\nils 2962 best 12752\nils 2963 best 12752\nils 2964 best 12752\nils 2965 best 12752\nils 2966 best 12752\nils 2967 best 12752\nils 2968 best 12752\nils 2969 best 12752\nils 2971 best 12752\nils 2972 best 12752\nils 2975 best 12752\nils 2976 best 12752\nils 2977 best 12752\nils 2979 best 12752\nils 2980 best 12752\nils 2981 best 12752\nils 2982 best 12752\nils 2983 best 12752\nils 2984 best 12752\nils 2987 best 12752\nils 2988 best 12752\nils 2989 best 12752\nils 2990 best 12752\nils 2991 best 12752\nils 2992 best 12752\nils 2995 best 12752\nils 2996 best 12752\nils 2997 best 12752\nils 3000 best 12752\nils 3004 best 12752\nils 3005 best 12752\nils 3006 best 12752\nils 3008 best 12752\nils 3011 best 12752\nils 3012 best 12752\nils 3013 best 12752\nils 3015 best 12752\nils 3016 best 12752\nils 3017 best 12752\nils 3018 best 12752\nils 3020 best 12752\nils 3021 best 12752\nils 3022 best 12752\nils 3023 best 12752\nils 3024 best 12752\nils 3025 best 12752\nils 3026 best 12752\nils 3027 best 12752\nils 3028 best 12752\nils 3029 best 12752\nils 3030 best 12752\nils 3034 best 12752\nils 3035 best 12752\nils 3036 best 12752\nils 3037 best 12752\nils 3038 best 12752\nils 3039 best 12752\nils 3040 best 12752\nils 3041 best 12752\nils 3043 best 12752\nils 3045 best 12752\nils 3046 best 12752\nils 3048 best 12752\nils 3050 best 12752\nils 3051 best 12752\nils 3052 best 12752\nils 3053 best 12752\nils 3054 best 12752\nils 3055 best 12752\nils 3056 best 12752\nils 3057 best 12752\nils 3058 best 12752\nils 3060 best 12752\nils 3061 best 12752\nils 3062 best 12752\nils 3063 best 12752\nils 3065 best 12752\nils 3066 best 12752\nils 3067 best 12752\nils 3068 best 12752\nils 3069 best 12752\nils 3071 best 12752\nils 3072 best 12752\nils 3073 best 12752\nils 3074 best 12752\nils 3075 best 12752\nils 3076 best 12752\nils 3077 best 12752\nils 3078 best 12752\nils 3081 best 12752\nils 3083 best 12752\nils 3084 best 12752\nils 3085 best 12752\nils 3086 best 12752\nils 3090 best 12752\nils 3092 best 12752\nils 3093 best 12752\nils 3094 best 12752\nils 3095 best 12752\nils 3096 best 12752\nils 3097 best 12752\nils 3098 best 12752\nils 3099 best 12752\nils 3101 best 12752\nils 3102 best 12752\nils 3103 best 12752\nils 3104 best 12752\nils 3105 best 12752\nils 3107 best 12752\nils 3108 best 12752\nils 3109 best 12752\nils 3113 best 12752\nils 3114 best 12752\nils 3116 best 12752\nils 3117 best 12752\nils 3118 best 12752\nils 3119 best 12752\nils 3120 best 12752\nils 3122 best 12752\nils 3123 best 12752\nils 3125 best 12752\nils 3127 best 12752\nils 3130 best 12752\nils 3131 best 12752\nils 3132 best 12752\nils 3133 best 12752\nils 3134 best 12752\nils 3135 best 12752\nils 3136 best 12752\nils 3137 best 12752\nils 3140 best 12752\nils 3141 best 12752\nils 3142 best 12752\nils 3143 best 12752\nils 3144 best 12752\nils 3145 best 12752\nils 3146 best 12752\nils 3148 best 12752\nils 3149 best 12752\nils 3150 best 12752\nils 3151 best 12752\nils 3152 best 12752\nils 3153 best 12752\nils 3154 best 12752\nils 3156 best 12752\nils 3157 best 12752\nils 3158 best 12752\nils 3160 best 12752\nils 3161 best 12752\nils 3162 best 12752\nils 3164 best 12752\nils 3166 best 12752\nils 3168 best 12752\nils 3169 best 12752\nils 3170 best 12752\nils 3171 best 12752\nils 3172 best 12752\nils 3173 best 12752\nils 3174 best 12752\nils 3175 best 12752\nils 3176 best 12752\nils 3178 best 12752\nils 3179 best 12752\nils 3180 best 12752\nils 3183 best 12752\nils 3184 best 12752\nils 3185 best 12752\nils 3187 best 12752\nils 3188 best 12752\nils 3190 best 12752\nils 3191 best 12752\nils 3193 best 12752\nils 3195 best 12752\nils 3196 best 12752\nils 3199 best 12752\nils 3200 best 12752\nils 3201 best 12752\nils 3202 best 12752\nils 3203 best 12752\nils 3204 best 12752\nils 3207 best 12752\nils 3208 best 12752\nils 3209 best 12752\nils 3210 best 12752\nils 3211 best 12752\nils 3212 best 12752\nils 3213 best 12752\nils 3215 best 12752\nils 3216 best 12752\nils 3217 best 12752\nils 3218 best 12752\nils 3219 best 12752\nils 3220 best 12752\nils 3221 best 12752\nils 3222 best 12752\nils 3223 best 12752\nils 3224 best 12752\nils 3225 best 12752\nils 3226 best 12752\nils 3227 best 12752\nils 3228 best 12752\nils 3229 best 12752\nils 3230 best 12752\nils 3231 best 12752\nils 3232 best 12752\nils 3233 best 12752\nils 3234 best 12752\nils 3235 best 12752\nils 3237 best 12752\nils 3239 best 12752\nils 3240 best 12752\nils 3241 best 12752\nils 3242 best 12752\nils 3243 best 12752\nils 3245 best 12752\nils 3247 best 12752\nils 3248 best 12752\nils 3250 best 12752\nils 3251 best 12752\nils 3253 best 12752\nils 3259 best 12752\nils 3260 best 12752\nils 3261 best 12752\nils 3263 best 12752\nils 3264 best 12752\nils 3265 best 12752\nils 3266 best 12752\nils 3267 best 12752\nils 3268 best 12752\nils 3271 best 12752\nils 3273 best 12752\nils 3275 best 12752\nils 3278 best 12752\nils 3279 best 12752\nils 3280 best 12752\nils 3282 best 12752\nils 3284 best 12752\nils 3285 best 12752\nils 3286 best 12752\nils 3287 best 12752\nils 3288 best 12752\nils 3289 best 12752\nils 3293 best 12752\nils 3294 best 12752\nils 3296 best 12752\nils 3297 best 12752\nils 3298 best 12752\nils 3299 best 12752\nils 3300 best 12752\nils 3301 best 12752\nils 3302 best 12752\nils 3303 best 12752\nils 3305 best 12752\nils 3307 best 12752\nils 3308 best 12752\nils 3309 best 12752\nils 3310 best 12752\nils 3311 best 12752\nils 3312 best 12752\nils 3315 best 12752\nils 3316 best 12752\nils 3317 best 12752\nils 3318 best 12752\nils 3319 best 12752\nils 3321 best 12752\nils 3323 best 12752\nils 3324 best 12752\nils 3325 best 12752\nils 3326 best 12752\nils 3328 best 12752\nils 3330 best 12752\nils 3331 best 12752\nils 3332 best 12752\nils 3333 best 12752\nils 3334 best 12752\nils 3335 best 12752\nils 3337 best 12752\nils 3338 best 12752\nils 3340 best 12752\nils 3342 best 12752\nils 3343 best 12752\nils 3345 best 12752\nils 3346 best 12752\nils 3348 best 12752\nils 3349 best 12752\nils 3350 best 12752\nils 3351 best 12752\nils 3352 best 12752\nils 3354 best 12752\nils 3356 best 12752\nils 3357 best 12752\nils 3358 best 12752\nils 3359 best 12752\nils 3360 best 12752\nils 3361 best 12752\nils 3362 best 12752\nils 3363 best 12752\nils 3364 best 12752\nils 3365 best 12752\nils 3366 best 12752\nils 3367 best 12752\nils 3368 best 12752\nils 3369 best 12752\nils 3370 best 12752\nils 3371 best 12752\nils 3372 best 12752\nils 3373 best 12752\nils 3374 best 12752\nils 3375 best 12752\nils 3376 best 12752\nils 3377 best 12752\nils 3378 best 12752\nils 3381 best 12752\nils 3383 best 12752\nils 3385 best 12752\nils 3386 best 12752\nils 3387 best 12752\nils 3388 best 12752\nils 3389 best 12752\nils 3390 best 12752\nils 3391 best 12752\nils 3392 best 12752\nils 3393 best 12752\nils 3394 best 12752\nils 3395 best 12752\nils 3396 best 12752\nils 3398 best 12752\nils 3399 best 12752\nils 3400 best 12752\nils 3401 best 12752\nils 3402 best 12752\nils 3404 best 12752\nils 3406 best 12752\nils 3407 best 12752\nils 3408 best 12752\nils 3409 best 12752\nils 3410 best 12752\nils 3411 best 12752\nils 3412 best 12752\nils 3415 best 12752\nils 3418 best 12752\nils 3419 best 12752\nils 3420 best 12752\nils 3421 best 12752\nils 3422 best 12752\nils 3423 best 12752\nils 3424 best 12752\nils 3425 best 12752\nils 3426 best 12752\nils 3427 best 12752\nils 3428 best 12752\nils 3429 best 12752\nils 3430 best 12752\nils 3431 best 12752\nils 3432 best 12752\nils 3433 best 12752\nils 3434 best 12752\nils 3435 best 12752\nils 3437 best 12752\nils 3438 best 12752\nils 3441 best 12752\nils 3442 best 12752\nils 3443 best 12752\nils 3444 best 12752\nils 3446 best 12752\nils 3447 best 12752\nils 3449 best 12752\nils 3450 best 12752\nils 3451 best 12752\nils 3452 best 12752\nils 3453 best 12752\nils 3454 best 12752\nils 3455 best 12752\nils 3456 best 12752\nils 3457 best 12752\nils 3458 best 12752\nils 3459 best 12752\nils 3460 best 12752\nils 3461 best 12752\nils 3462 best 12752\nils 3464 best 12752\nils 3465 best 12752\nils 3466 best 12752\nils 3467 best 12752\nils 3469 best 12752\nils 3470 best 12752\nils 3471 best 12752\nils 3472 best 12752\nils 3473 best 12752\nils 3474 best 12752\nils 3475 best 12752\nils 3476 best 12752\nils 3479 best 12752\nils 3480 best 12752\nils 3481 best 12752\nils 3483 best 12752\nils 3484 best 12752\nils 3485 best 12752\nils 3486 best 12752\nils 3487 best 12752\nils 3488 best 12752\nils 3489 best 12752\nils 3490 best 12752\nils 3491 best 12752\nils 3492 best 12752\nils 3493 best 12752\nils 3494 best 12752\nils 3495 best 12752\nils 3496 best 12752\nils 3498 best 12752\nils 3499 best 12752\nils 3500 best 12752\nils 3501 best 12752\nils 3503 best 12751\nils 3504 best 12751\nils 3505 best 12751\nils 3506 best 12751\nils 3508 best 12751\nils 3509 best 12751\nils 3510 best 12751\nils 3512 best 12751\nils 3513 best 12751\nils 3514 best 12751\nils 3515 best 12751\nils 3517 best 12751\nils 3518 best 12751\nils 3519 best 12751\nils 3522 best 12751\nils 3524 best 12751\nils 3525 best 12751\nils 3526 best 12751\nils 3527 best 12751\nils 3528 best 12751\nils 3529 best 12751\nils 3530 best 12751\nils 3531 best 12751\nils 3532 best 12751\nils 3534 best 12751\nils 3536 best 12751\nils 3537 best 12751\nils 3538 best 12751\nils 3539 best 12751\nils 3541 best 12751\nils 3543 best 12751\nils 3544 best 12751\nils 3545 best 12751\nils 3546 best 12751\nils 3547 best 12751\nils 3548 best 12751\nils 3549 best 12751\nils 3550 best 12751\nils 3551 best 12751\nils 3552 best 12751\nils 3556 best 12751\nils 3557 best 12751\nils 3558 best 12751\nils 3559 best 12751\nils 3560 best 12751\nils 3562 best 12751\nils 3563 best 12751\nils 3564 best 12751\nils 3565 best 12751\nils 3566 best 12751\nils 3567 best 12751\nils 3569 best 12751\nils 3571 best 12751\nils 3572 best 12751\nils 3573 best 12751\nils 3574 best 12751\nils 3575 best 12751\nils 3576 best 12751\nils 3577 best 12751\nils 3580 best 12751\nils 3581 best 12751\nils 3582 best 12751\nils 3583 best 12751\nils 3584 best 12751\nils 3586 best 12751\nils 3587 best 12751\nils 3590 best 12751\nils 3592 best 12751\nils 3594 best 12751\nils 3596 best 12751\nils 3603 best 12751\nils 3604 best 12751\nils 3605 best 12751\nils 3607 best 12751\nils 3608 best 12751\nils 3609 best 12751\nils 3610 best 12751\nils 3612 best 12751\nils 3614 best 12751\nils 3615 best 12751\nils 3616 best 12751\nils 3617 best 12751\nils 3618 best 12751\nils 3619 best 12751\nils 3620 best 12751\nils 3622 best 12751\nils 3623 best 12751\nils 3624 best 12751\nils 3625 best 12751\nils 3626 best 12751\nils 3627 best 12751\nils 3628 best 12751\nils 3629 best 12751\nils 3632 best 12751\nils 3633 best 12751\nils 3634 best 12751\nils 3635 best 12751\nils 3636 best 12751\nils 3637 best 12751\nils 3639 best 12751\nils 3640 best 12751\nils 3641 best 12751\nils 3642 best 12751\nils 3645 best 12751\nils 3647 best 12751\nils 3648 best 12751\nils 3650 best 12751\nils 3651 best 12751\nils 3655 best 12751\nils 3656 best 12751\nils 3659 best 12751\nils 3660 best 12751\nils 3662 best 12751\nils 3663 best 12751\nils 3664 best 12751\nils 3666 best 12751\nils 3667 best 12751\nils 3668 best 12751\nils 3669 best 12751\nils 3673 best 12751\nils 3674 best 12751\nils 3675 best 12751\nils 3676 best 12751\nils 3677 best 12751\nils 3678 best 12751\nils 3681 best 12751\nils 3682 best 12751\nils 3685 best 12751\nils 3687 best 12751\nils 3688 best 12751\nils 3689 best 12751\nils 3690 best 12751\nils 3691 best 12751\nils 3692 best 12751\nils 3693 best 12751\nils 3694 best 12751\nils 3695 best 12751\nils 3697 best 12751\nils 3698 best 12751\nils 3699 best 12751\nils 3700 best 12751\nils 3701 best 12751\nils 3702 best 12751\nils 3703 best 12751\nils 3704 best 12751\nils 3705 best 12751\nils 3706 best 12751\nils 3707 best 12751\nils 3708 best 12751\nils 3709 best 12751\nils 3710 best 12751\nils 3712 best 12751\nils 3714 best 12751\nils 3715 best 12751\nils 3718 best 12751\nils 3720 best 12751\nils 3721 best 12751\nils 3722 best 12751\nils 3723 best 12751\nils 3724 best 12751\nils 3725 best 12751\nils 3727 best 12751\nils 3729 best 12751\nils 3730 best 12751\nils 3731 best 12751\nils 3732 best 12751\nils 3733 best 12751\nils 3734 best 12751\nils 3735 best 12751\nils 3736 best 12751\nils 3737 best 12751\nils 3738 best 12751\nils 3739 best 12751\nils 3740 best 12751\nils 3741 best 12751\nils 3742 best 12751\nils 3743 best 12751\nils 3744 best 12751\nils 3746 best 12751\nils 3747 best 12751\nils 3748 best 12751\nils 3749 best 12751\nils 3750 best 12751\nils 3751 best 12751\nils 3755 best 12751\nils 3756 best 12751\nils 3757 best 12751\nils 3758 best 12751\nils 3759 best 12751\nils 3760 best 12751\nils 3761 best 12751\nils 3762 best 12751\nils 3763 best 12751\nils 3765 best 12751\nils 3770 best 12751\nils 3772 best 12751\nils 3773 best 12751\nils 3775 best 12751\nils 3776 best 12751\nils 3777 best 12751\nils 3779 best 12751\nils 3780 best 12751\nils 3781 best 12751\nils 3782 best 12751\nils 3783 best 12751\nils 3784 best 12751\nils 3785 best 12751\nils 3788 best 12751\nils 3791 best 12751\nils 3793 best 12751\nils 3794 best 12751\nils 3795 best 12751\nils 3796 best 12751\nils 3798 best 12751\nils 3799 best 12751\nils 3800 best 12751\nils 3801 best 12751\nils 3802 best 12751\nils 3803 best 12751\nils 3804 best 12751\nils 3807 best 12751\nils 3808 best 12751\nils 3810 best 12751\nils 3812 best 12751\nils 3813 best 12751\nils 3814 best 12751\nils 3815 best 12751\nils 3817 best 12751\nils 3819 best 12751\nils 3820 best 12751\nils 3822 best 12751\nils 3824 best 12751\nils 3825 best 12751\nils 3827 best 12751\nils 3828 best 12751\nils 3830 best 12751\nils 3831 best 12751\nils 3832 best 12751\nils 3835 best 12751\nils 3836 best 12751\nils 3837 best 12751\nils 3838 best 12751\nils 3839 best 12751\nils 3841 best 12751\nils 3842 best 12751\nils 3843 best 12751\nils 3844 best 12751\nils 3845 best 12751\nils 3846 best 12751\nils 3847 best 12751\nils 3848 best 12751\nils 3850 best 12751\nils 3851 best 12751\nils 3852 best 12751\nils 3853 best 12751\nils 3855 best 12751\nils 3856 best 12751\nils 3857 best 12751\nils 3858 best 12751\nils 3859 best 12751\nils 3860 best 12751\nils 3862 best 12751\nils 3863 best 12751\nils 3864 best 12751\nils 3865 best 12751\nils 3866 best 12751\nils 3867 best 12751\nils 3868 best 12751\nils 3869 best 12751\nils 3870 best 12751\nils 3871 best 12751\nils 3873 best 12751\nils 3874 best 12751\nils 3875 best 12751\nils 3876 best 12751\nils 3877 best 12751\nils 3878 best 12751\nils 3879 best 12751\nils 3882 best 12751\nils 3884 best 12751\nils 3885 best 12751\nils 3887 best 12751\nils 3888 best 12751\nils 3889 best 12751\nils 3890 best 12751\nils 3892 best 12751\nils 3893 best 12751\nils 3894 best 12751\nils 3895 best 12751\nils 3897 best 12751\nils 3898 best 12751\nils 3899 best 12751\nils 3900 best 12751\nils 3901 best 12751\nils 3902 best 12751\nils 3905 best 12751\nils 3906 best 12751\nils 3907 best 12751\nils 3909 best 12751\nils 3910 best 12751\nils 3911 best 12751\nils 3912 best 12751\nils 3913 best 12751\nils 3914 best 12751\nils 3915 best 12751\nils 3916 best 12751\nils 3918 best 12751\nils 3919 best 12751\nils 3921 best 12751\nils 3922 best 12751\nils 3923 best 12751\nils 3924 best 12751\nils 3925 best 12751\nils 3926 best 12751\nils 3928 best 12751\nils 3929 best 12751\nils 3930 best 12751\nils 3931 best 12751\nils 3933 best 12751\nils 3935 best 12751\nils 3936 best 12751\nils 3937 best 12751\nils 3938 best 12751\nils 3939 best 12751\nils 3940 best 12751\nils 3941 best 12751\nils 3942 best 12751\nils 3943 best 12751\nils 3944 best 12751\nils 3945 best 12751\nils 3946 best 12751\nils 3947 best 12751\nils 3948 best 12751\nils 3949 best 12751\nils 3950 best 12751\nils 3951 best 12751\nils 3952 best 12751\nils 3953 best 12751\nils 3955 best 12751\nils 3956 best 12751\nils 3957 best 12751\nils 3959 best 12751\nils 3960 best 12751\nils 3962 best 12751\nils 3966 best 12751\nils 3967 best 12751\nils 3968 best 12751\nils 3972 best 12751\nils 3973 best 12751\nils 3975 best 12751\nils 3976 best 12751\nils 3977 best 12751\nils 3978 best 12751\nils 3980 best 12751\nils 3981 best 12751\nils 3982 best 12751\nils 3984 best 12751\nils 3985 best 12751\nils 3987 best 12751\nils 3989 best 12751\nils 3990 best 12751\nils 3991 best 12751\nils 3992 best 12751\nils 3993 best 12751\nils 3994 best 12751\nils 3995 best 12751\nils 3996 best 12751\nils 3998 best 12751\nils 3999 best 12751\nils 4000 best 12751\nils 4001 best 12751\nils 4003 best 12751\nils 4004 best 12751\nils 4005 best 12751\nils 4006 best 12751\nils 4007 best 12751\nils 4008 best 12751\nils 4010 best 12751\nils 4013 best 12751\nils 4014 best 12751\nils 4015 best 12751\nils 4016 best 12751\nils 4017 best 12751\nils 4018 best 12751\nils 4019 best 12751\nils 4020 best 12751\nils 4024 best 12751\nils 4025 best 12751\nils 4027 best 12751\nils 4029 best 12751\nils 4030 best 12751\nils 4031 best 12751\nils 4032 best 12751\nils 4033 best 12751\nils 4034 best 12751\nils 4035 best 12751\nils 4036 best 12751\nils 4037 best 12751\nils 4038 best 12751\nils 4040 best 12751\nils 4042 best 12751\nils 4043 best 12751\nils 4045 best 12751\nils 4046 best 12751\nils 4047 best 12751\nils 4048 best 12751\nils 4049 best 12751\nils 4050 best 12751\nils 4051 best 12751\nils 4052 best 12751\nils 4053 best 12751\nils 4054 best 12751\nils 4055 best 12751\nils 4056 best 12751\nils 4058 best 12751\nils 4060 best 12751\nils 4061 best 12751\nils 4063 best 12751\nils 4064 best 12751\nils 4065 best 12751\nils 4066 best 12751\nils 4067 best 12751\nils 4068 best 12751\nils 4069 best 12751\nils 4071 best 12751\nils 4072 best 12751\nils 4073 best 12751\nils 4074 best 12751\nils 4075 best 12751\nils 4076 best 12751\nils 4077 best 12751\nils 4078 best 12751\nils 4079 best 12751\nils 4080 best 12751\nils 4081 best 12751\nils 4082 best 12751\nils 4083 best 12751\nils 4085 best 12751\nils 4087 best 12751\nils 4088 best 12751\nils 4091 best 12751\nils 4093 best 12751\nils 4095 best 12751\nils 4096 best 12751\nils 4097 best 12751\nils 4101 best 12751\nils 4103 best 12751\nils 4104 best 12751\nils 4105 best 12751\nils 4106 best 12751\nils 4107 best 12751\nils 4108 best 12751\nils 4109 best 12751\nils 4110 best 12751\nils 4111 best 12751\nils 4112 best 12751\nils 4113 best 12751\nils 4114 best 12751\nils 4115 best 12751\nils 4117 best 12751\nils 4118 best 12751\nils 4119 best 12751\nils 4121 best 12751\nils 4122 best 12751\nils 4123 best 12751\nils 4124 best 12751\nils 4125 best 12751\nils 4126 best 12751\nils 4131 best 12751\nils 4132 best 12751\nils 4133 best 12751\nils 4135 best 12751\nils 4137 best 12751\nils 4138 best 12751\nils 4139 best 12751\nils 4140 best 12751\nils 4141 best 12751\nils 4142 best 12751\nils 4143 best 12751\nils 4144 best 12751\nils 4145 best 12751\nils 4148 best 12751\nils 4150 best 12751\nils 4152 best 12751\nils 4153 best 12751\nils 4154 best 12751\nils 4158 best 12751\nils 4159 best 12751\nils 4160 best 12751\nils 4161 best 12751\nils 4162 best 12751\nils 4163 best 12751\nils 4165 best 12751\nils 4170 best 12751\nils 4173 best 12751\nils 4174 best 12751\nils 4175 best 12751\nils 4176 best 12751\nils 4177 best 12751\nils 4178 best 12751\nils 4179 best 12751\nils 4181 best 12751\nils 4182 best 12751\nils 4183 best 12751\nils 4184 best 12751\nils 4185 best 12751\nils 4186 best 12751\nils 4187 best 12751\nils 4188 best 12751\nils 4189 best 12751\nils 4190 best 12751\nils 4191 best 12751\nils 4192 best 12751\nils 4193 best 12751\nils 4194 best 12751\nils 4195 best 12751\nils 4199 best 12751\nils 4200 best 12751\nils 4203 best 12751\nils 4204 best 12751\nils 4205 best 12751\nils 4206 best 12751\nils 4207 best 12751\nils 4208 best 12751\nils 4209 best 12751\nils 4210 best 12751\nils 4213 best 12751\nils 4214 best 12751\nils 4215 best 12751\nils 4216 best 12751\nils 4217 best 12751\nils 4218 best 12751\nils 4219 best 12751\nils 4220 best 12751\nils 4222 best 12751\nils 4223 best 12751\nils 4224 best 12751\nils 4225 best 12751\nils 4226 best 12751\nils 4227 best 12751\nils 4230 best 12751\nils 4231 best 12751\nils 4232 best 12751\nils 4234 best 12751\nils 4235 best 12751\nils 4236 best 12751\nils 4237 best 12751\nils 4238 best 12751\nils 4240 best 12751\nils 4241 best 12751\nils 4242 best 12751\nils 4243 best 12751\nils 4244 best 12751\nils 4245 best 12751\nils 4246 best 12751\nils 4248 best 12751\nils 4249 best 12751\nils 4251 best 12751\nils 4252 best 12751\nils 4253 best 12751\nils 4256 best 12751\nils 4257 best 12751\nils 4258 best 12751\nils 4259 best 12751\nils 4260 best 12751\nils 4263 best 12751\nils 4264 best 12751\nils 4266 best 12751\nils 4267 best 12751\nils 4268 best 12751\nils 4269 best 12751\nils 4270 best 12751\nils 4271 best 12751\nils 4272 best 12751\nils 4274 best 12751\nils 4275 best 12751\nils 4276 best 12751\nils 4277 best 12751\nils 4279 best 12751\nils 4281 best 12751\nils 4283 best 12751\nils 4286 best 12751\nils 4287 best 12751\nils 4288 best 12751\nils 4290 best 12751\nils 4293 best 12751\nils 4296 best 12751\nils 4297 best 12751\nils 4298 best 12751\nils 4299 best 12751\nils 4301 best 12751\nils 4302 best 12751\nils 4303 best 12751\nils 4304 best 12751\nils 4306 best 12751\nils 4307 best 12751\nils 4308 best 12751\nils 4309 best 12751\nils 4312 best 12751\nils 4313 best 12751\nils 4314 best 12751\nils 4315 best 12751\nils 4316 best 12751\nils 4318 best 12751\nils 4319 best 12751\nils 4320 best 12751\nils 4321 best 12751\nils 4322 best 12751\nils 4324 best 12751\nils 4325 best 12751\nils 4326 best 12751\nils 4327 best 12751\nils 4328 best 12751\nils 4329 best 12751\nils 4330 best 12751\nils 4331 best 12751\nils 4332 best 12751\nils 4333 best 12751\nils 4336 best 12751\nils 4338 best 12751\nils 4339 best 12751\nils 4340 best 12751\nils 4341 best 12751\nils 4342 best 12751\nils 4343 best 12751\nils 4344 best 12751\nils 4346 best 12751\nils 4347 best 12751\nils 4348 best 12751\nils 4349 best 12751\nils 4350 best 12751\nils 4351 best 12751\nils 4352 best 12751\nils 4353 best 12751\nils 4354 best 12751\nils 4355 best 12751\nils 4356 best 12751\nils 4357 best 12751\nils 4358 best 12751\nils 4360 best 12751\nils 4361 best 12751\nils 4363 best 12751\nils 4365 best 12751\nils 4366 best 12751\nils 4367 best 12751\nils 4369 best 12751\nils 4370 best 12751\nils 4371 best 12751\nils 4373 best 12751\nils 4374 best 12751\nils 4377 best 12751\nils 4378 best 12751\nils 4379 best 12751\nils 4380 best 12751\nils 4381 best 12751\nils 4382 best 12751\nils 4383 best 12751\nils 4384 best 12751\nils 4385 best 12751\nils 4386 best 12751\nils 4387 best 12751\nils 4388 best 12751\nils 4389 best 12751\nils 4390 best 12751\nils 4392 best 12751\nils 4393 best 12751\nils 4396 best 12751\nils 4397 best 12751\nils 4400 best 12751\nils 4401 best 12751\nils 4403 best 12751\nils 4406 best 12751\nils 4407 best 12751\nils 4408 best 12751\nils 4410 best 12751\nils 4411 best 12751\nils 4412 best 12751\nils 4413 best 12751\nils 4414 best 12751\nils 4415 best 12751\nils 4416 best 12751\nils 4417 best 12751\nils 4418 best 12751\nils 4419 best 12751\nils 4420 best 12751\nils 4421 best 12751\nils 4422 best 12751\nils 4423 best 12751\nils 4425 best 12751\nils 4426 best 12751\nils 4427 best 12751\nils 4428 best 12751\nils 4429 best 12751\nils 4430 best 12751\nils 4431 best 12751\nils 4432 best 12751\nils 4433 best 12751\nils 4434 best 12751\nils 4435 best 12751\nils 4436 best 12751\nils 4438 best 12751\nils 4439 best 12751\nils 4440 best 12751\nils 4441 best 12751\nils 4444 best 12751\nils 4445 best 12751\nils 4446 best 12751\nils 4447 best 12751\nils 4449 best 12751\nils 4450 best 12751\nils 4451 best 12751\nils 4452 best 12751\nils 4453 best 12751\nils 4454 best 12751\nils 4455 best 12751\nils 4457 best 12751\nils 4458 best 12751\nils 4459 best 12751\nils 4461 best 12751\nils 4462 best 12751\nils 4463 best 12751\nils 4464 best 12751\nils 4465 best 12751\nils 4469 best 12751\nils 4470 best 12751\nils 4471 best 12751\nils 4473 best 12751\nils 4474 best 12751\nils 4475 best 12751\nils 4477 best 12751\nils 4478 best 12751\nils 4479 best 12751\nils 4482 best 12751\nils 4486 best 12751\nils 4487 best 12751\nils 4488 best 12751\nils 4489 best 12751\nils 4490 best 12751\nils 4491 best 12751\nils 4492 best 12751\nils 4493 best 12751\nils 4494 best 12751\nils 4495 best 12751\nils 4496 best 12751\nils 4499 best 12751\nils 4500 best 12751\nils 4501 best 12751\nils 4503 best 12751\nils 4504 best 12751\nils 4505 best 12751\nils 4506 best 12751\nils 4508 best 12751\nils 4509 best 12751\nils 4511 best 12751\nils 4512 best 12751\nils 4513 best 12751\nils 4514 best 12751\nils 4515 best 12751\nils 4516 best 12751\nils 4518 best 12751\nils 4519 best 12751\nils 4520 best 12751\nils 4521 best 12751\nils 4522 best 12751\nils 4523 best 12751\nils 4524 best 12751\nils 4525 best 12751\nils 4526 best 12751\nils 4527 best 12751\nils 4529 best 12751\nils 4531 best 12751\nils 4533 best 12751\nils 4534 best 12751\nils 4535 best 12751\nils 4536 best 12751\nils 4537 best 12751\nils 4539 best 12751\nils 4540 best 12751\nils 4542 best 12751\nils 4543 best 12751\nils 4544 best 12751\nils 4546 best 12751\nils 4547 best 12751\nils 4548 best 12751\nils 4549 best 12751\nils 4551 best 12751\nils 4552 best 12751\nils 4553 best 12751\nils 4554 best 12751\nils 4556 best 12751\nils 4558 best 12751\nils 4559 best 12751\nils 4560 best 12751\nils 4561 best 12751\nils 4562 best 12751\nils 4563 best 12751\nils 4564 best 12751\nils 4565 best 12751\nils 4568 best 12751\nils 4569 best 12751\nils 4572 best 12751\nils 4574 best 12751\nils 4575 best 12751\nils 4577 best 12751\nils 4578 best 12751\nils 4579 best 12751\nils 4580 best 12751\nils 4581 best 12751\nils 4582 best 12751\nils 4584 best 12751\nils 4585 best 12751\nils 4588 best 12751\nils 4589 best 12751\nils 4590 best 12751\nils 4593 best 12751\nils 4594 best 12751\nils 4595 best 12751\nils 4596 best 12751\nils 4597 best 12751\nils 4598 best 12751\nils 4599 best 12751\nils 4602 best 12751\nils 4604 best 12751\nils 4606 best 12751\nils 4607 best 12751\nils 4608 best 12751\nils 4609 best 12751\nils 4610 best 12751\nils 4613 best 12751\nils 4614 best 12751\nils 4616 best 12751\nils 4617 best 12751\nils 4618 best 12751\nils 4620 best 12751\nils 4621 best 12751\nils 4622 best 12751\nils 4623 best 12751\nils 4624 best 12751\nils 4625 best 12751\nils 4627 best 12751\nils 4628 best 12751\nils 4630 best 12751\nils 4631 best 12751\nils 4632 best 12751\nils 4633 best 12751\nils 4634 best 12751\nils 4636 best 12751\nils 4638 best 12751\nils 4639 best 12751\nils 4640 best 12751\nils 4641 best 12751\nils 4642 best 12751\nils 4643 best 12751\nils 4644 best 12751\nils 4645 best 12751\nils 4646 best 12751\nils 4648 best 12751\nils 4649 best 12751\nils 4651 best 12751\nils 4652 best 12751\nils 4653 best 12751\nils 4654 best 12751\nils 4656 best 12751\nils 4657 best 12751\nils 4658 best 12751\nils 4660 best 12751\nils 4661 best 12751\nils 4662 best 12751\nils 4664 best 12751\nils 4667 best 12751\nils 4668 best 12751\nils 4669 best 12751\nils 4670 best 12751\nils 4671 best 12751\nils 4673 best 12751\nils 4675 best 12751\nils 4676 best 12751\nils 4677 best 12751\nils 4678 best 12751\nils 4679 best 12751\nils 4680 best 12751\nils 4681 best 12751\nils 4682 best 12751\nils 4683 best 12751\nils 4684 best 12751\nils 4685 best 12751\nils 4687 best 12751\nils 4688 best 12751\nils 4689 best 12751\nils 4692 best 12751\nils 4693 best 12751\nils 4694 best 12751\nils 4695 best 12751\nils 4696 best 12751\nils 4697 best 12751\nils 4699 best 12751\nils 4700 best 12751\nils 4701 best 12751\nils 4702 best 12751\nils 4704 best 12751\nils 4705 best 12751\nils 4706 best 12751\nils 4707 best 12751\nils 4708 best 12751\nils 4709 best 12751\nils 4710 best 12751\nils 4712 best 12751\nils 4713 best 12751\nils 4714 best 12751\nils 4716 best 12751\nils 4717 best 12751\nils 4718 best 12751\nils 4719 best 12751\nils 4720 best 12751\nils 4721 best 12751\nils 4722 best 12751\nils 4723 best 12751\nils 4724 best 12751\nils 4725 best 12751\nils 4726 best 12751\nils 4727 best 12751\nils 4731 best 12751\nils 4734 best 12751\nils 4735 best 12751\nils 4736 best 12751\nils 4738 best 12751\nils 4739 best 12751\nils 4741 best 12751\nils 4743 best 12751\nils 4744 best 12751\nils 4747 best 12751\nils 4750 best 12751\nils 4751 best 12751\nils 4752 best 12751\nils 4753 best 12751\nils 4755 best 12751\nils 4757 best 12751\nils 4758 best 12751\nils 4759 best 12751\nils 4761 best 12751\nils 4763 best 12751\nils 4765 best 12751\nils 4767 best 12751\nils 4768 best 12751\nils 4769 best 12751\nils 4770 best 12751\nils 4771 best 12751\nils 4773 best 12751\nils 4774 best 12751\nils 4775 best 12751\nils 4776 best 12751\nils 4777 best 12751\nils 4778 best 12751\nils 4779 best 12751\nils 4780 best 12751\nils 4781 best 12751\nils 4782 best 12751\nils 4783 best 12751\nils 4784 best 12751\nils 4786 best 12751\nils 4787 best 12751\nils 4788 best 12751\nils 4791 best 12751\nils 4792 best 12751\nils 4795 best 12751\nils 4796 best 12751\nils 4798 best 12751\nils 4799 best 12751\nils 4800 best 12751\nils 4801 best 12751\nils 4802 best 12751\nils 4804 best 12751\nils 4805 best 12751\nils 4806 best 12751\nils 4809 best 12751\nils 4810 best 12751\nils 4813 best 12751\nils 4814 best 12751\nils 4815 best 12751\nils 4817 best 12751\nils 4820 best 12751\nils 4821 best 12751\nils 4822 best 12751\nils 4825 best 12751\nils 4826 best 12751\nils 4828 best 12751\nils 4829 best 12751\nils 4830 best 12751\nils 4831 best 12751\nils 4833 best 12751\nils 4834 best 12751\nils 4835 best 12751\nils 4836 best 12751\nils 4837 best 12751\nils 4840 best 12751\nils 4841 best 12751\nils 4842 best 12751\nils 4843 best 12751\nils 4844 best 12751\nils 4845 best 12751\nils 4846 best 12751\nils 4847 best 12751\nils 4848 best 12751\nils 4849 best 12751\nils 4851 best 12751\nils 4853 best 12751\nils 4855 best 12751\nils 4856 best 12751\nils 4857 best 12751\nils 4858 best 12751\nils 4860 best 12751\nils 4862 best 12751\nils 4864 best 12751\nils 4865 best 12751\nils 4866 best 12751\nils 4867 best 12751\nils 4869 best 12751\nils 4871 best 12751\nils 4872 best 12751\nils 4873 best 12751\nils 4874 best 12751\nils 4877 best 12751\nils 4878 best 12751\nils 4879 best 12751\nils 4880 best 12751\nils 4882 best 12751\nils 4883 best 12751\nils 4884 best 12751\nils 4887 best 12751\nils 4889 best 12751\nils 4890 best 12751\nils 4892 best 12751\nils 4893 best 12751\nils 4894 best 12751\nils 4895 best 12751\nils 4896 best 12751\nils 4898 best 12751\nils 4900 best 12751\nils 4901 best 12751\nils 4902 best 12751\nils 4905 best 12751\nils 4906 best 12751\nils 4907 best 12751\nils 4908 best 12751\nils 4909 best 12751\nils 4911 best 12751\nils 4912 best 12751\nils 4913 best 12751\nils 4914 best 12751\nils 4915 best 12751\nils 4916 best 12751\nils 4917 best 12751\nils 4918 best 12751\nils 4919 best 12751\nils 4920 best 12751\nils 4921 best 12751\nils 4922 best 12751\nils 4923 best 12751\nils 4925 best 12751\nils 4926 best 12751\nils 4927 best 12751\nils 4929 best 12751\nils 4932 best 12751\nils 4933 best 12751\nils 4935 best 12751\nils 4936 best 12751\nils 4937 best 12751\nils 4938 best 12751\nils 4939 best 12751\nils 4941 best 12751\nils 4942 best 12751\nils 4944 best 12751\nils 4946 best 12751\nils 4947 best 12751\nils 4948 best 12751\nils 4949 best 12751\nils 4951 best 12751\nils 4952 best 12751\nils 4953 best 12751\nils 4954 best 12751\nils 4956 best 12751\nils 4957 best 12751\nils 4958 best 12751\nils 4960 best 12751\nils 4961 best 12751\nils 4962 best 12751\nils 4963 best 12751\nils 4964 best 12751\nils 4965 best 12751\nils 4967 best 12751\nils 4968 best 12751\nils 4969 best 12751\nils 4970 best 12751\nils 4974 best 12751\nils 4975 best 12751\nils 4976 best 12751\nils 4977 best 12751\nils 4978 best 12751\nils 4979 best 12751\nils 4980 best 12751\nils 4982 best 12751\nils 4983 best 12751\nils 4984 best 12751\nils 4985 best 12751\nils 4986 best 12751\nils 4987 best 12751\nils 4988 best 12751\nils 4990 best 12751\nils 4991 best 12751\nils 4992 best 12751\nils 4994 best 12751\nils 4996 best 12751\nils 4998 best 12751\nils 4999 best 12751\nils 5000 best 12751\nils 5002 best 12751\nils 5003 best 12751\nils 5004 best 12751\nils 5005 best 12751\nils 5006 best 12751\nils 5007 best 12751\nils 5009 best 12751\nils 5010 best 12751\nils 5011 best 12751\nils 5014 best 12751\nils 5015 best 12751\nils 5016 best 12751\nils 5017 best 12751\nils 5019 best 12751\nils 5020 best 12751\nils 5021 best 12751\nils 5022 best 12751\nils 5023 best 12751\nils 5025 best 12751\nils 5027 best 12751\nils 5028 best 12751\nils 5029 best 12751\nils 5030 best 12751\nils 5032 best 12751\nils 5033 best 12751\nils 5035 best 12751\nils 5036 best 12751\nils 5038 best 12751\nils 5039 best 12751\nils 5040 best 12751\nils 5041 best 12751\nils 5042 best 12751\nils 5044 best 12751\nils 5046 best 12751\nils 5047 best 12751\nils 5048 best 12751\nils 5049 best 12751\nils 5050 best 12751\nils 5051 best 12751\nils 5052 best 12751\nils 5053 best 12751\nils 5054 best 12751\nils 5055 best 12751\nils 5056 best 12751\nils 5057 best 12751\nils 5058 best 12751\nils 5059 best 12751\nils 5060 best 12751\nils 5061 best 12751\nils 5062 best 12751\nils 5063 best 12751\nils 5066 best 12751\nils 5067 best 12751\nils 5070 best 12751\nils 5071 best 12751\nils 5073 best 12751\nils 5074 best 12751\nils 5075 best 12751\nils 5076 best 12751\nils 5078 best 12751\nils 5079 best 12751\nils 5080 best 12751\nils 5081 best 12751\nils 5082 best 12751\nils 5083 best 12751\nils 5084 best 12751\nils 5085 best 12751\nils 5086 best 12751\nils 5090 best 12751\nils 5091 best 12751\nils 5092 best 12751\nils 5093 best 12751\nils 5094 best 12751\nils 5095 best 12751\nils 5096 best 12751\nils 5097 best 12751\nils 5098 best 12751\nils 5099 best 12751\nils 5101 best 12751\nils 5102 best 12751\nils 5103 best 12751\nils 5104 best 12751\nils 5105 best 12751\nils 5106 best 12751\nils 5107 best 12751\nils 5108 best 12751\nils 5111 best 12751\nils 5112 best 12751\nils 5113 best 12751\nils 5114 best 12751\nils 5116 best 12751\nils 5117 best 12751\nils 5118 best 12751\nils 5119 best 12751\nils 5120 best 12751\nils 5121 best 12751\nils 5122 best 12751\nils 5123 best 12751\nils 5124 best 12751\nils 5125 best 12751\nils 5126 best 12751\nils 5127 best 12751\nils 5128 best 12751\nils 5129 best 12751\nils 5130 best 12751\nils 5131 best 12751\nils 5132 best 12751\nils 5133 best 12751\nils 5134 best 12751\nils 5135 best 12751\nils 5136 best 12751\nils 5138 best 12751\nils 5139 best 12751\nils 5140 best 12751\nils 5142 best 12751\nils 5143 best 12751\nils 5144 best 12751\nils 5146 best 12751\nils 5147 best 12751\nils 5148 best 12751\nils 5150 best 12751\nils 5152 best 12751\nils 5154 best 12751\nils 5156 best 12751\nils 5157 best 12751\nils 5159 best 12751\nils 5160 best 12751\nils 5162 best 12751\nils 5164 best 12751\nils 5165 best 12751\nils 5167 best 12751\nils 5169 best 12751\nils 5170 best 12751\nils 5171 best 12751\nils 5173 best 12751\nils 5177 best 12751\nils 5178 best 12751\nils 5179 best 12751\nils 5181 best 12751\nils 5184 best 12751\nils 5185 best 12751\nils 5186 best 12751\nils 5188 best 12751\nils 5189 best 12751\nils 5190 best 12751\nils 5192 best 12751\nils 5194 best 12751\nils 5195 best 12751\nils 5197 best 12751\nils 5198 best 12751\nils 5199 best 12751\nils 5201 best 12751\nils 5202 best 12751\nils 5203 best 12751\nils 5204 best 12751\nils 5206 best 12751\nils 5207 best 12751\nils 5208 best 12751\nils 5209 best 12751\nils 5210 best 12751\nils 5212 best 12751\nils 5213 best 12751\nils 5215 best 12751\nils 5216 best 12751\nils 5217 best 12751\nils 5218 best 12751\nils 5219 best 12751\nils 5221 best 12751\nils 5222 best 12751\nils 5223 best 12751\nils 5224 best 12751\nils 5226 best 12751\nils 5227 best 12751\nils 5229 best 12751\nils 5230 best 12751\nils 5231 best 12751\nils 5232 best 12751\nils 5233 best 12751\nils 5234 best 12751\nils 5235 best 12751\nils 5236 best 12751\nils 5237 best 12751\nils 5238 best 12751\nils 5240 best 12751\nils 5241 best 12751\nils 5242 best 12751\nils 5245 best 12751\nils 5248 best 12751\nils 5250 best 12751\nils 5251 best 12751\nils 5252 best 12751\nils 5253 best 12751\nils 5254 best 12751\nils 5255 best 12751\nils 5257 best 12751\nils 5258 best 12751\nils 5260 best 12751\nils 5261 best 12751\nils 5262 best 12751\nils 5265 best 12751\nils 5267 best 12751\nils 5268 best 12751\nils 5269 best 12751\nils 5272 best 12751\nils 5273 best 12751\nils 5274 best 12751\nils 5275 best 12751\nils 5276 best 12751\nils 5277 best 12751\nils 5278 best 12751\nils 5285 best 12751\nils 5286 best 12751\nils 5287 best 12751\nils 5289 best 12751\nils 5290 best 12751\nils 5291 best 12751\nils 5293 best 12751\nils 5294 best 12751\nils 5295 best 12751\nils 5297 best 12751\nils 5298 best 12751\nils 5300 best 12751\nils 5302 best 12751\nils 5304 best 12751\nils 5305 best 12751\nils 5306 best 12751\nils 5307 best 12751\nils 5308 best 12751\nils 5309 best 12751\nils 5310 best 12751\nils 5311 best 12751\nils 5312 best 12751\nils 5313 best 12751\nils 5314 best 12751\nils 5315 best 12751\nils 5316 best 12751\nils 5317 best 12751\nils 5318 best 12751\nils 5319 best 12751\nils 5320 best 12751\nils 5321 best 12751\nils 5322 best 12751\nils 5323 best 12751\nils 5324 best 12751\nils 5325 best 12751\nils 5326 best 12751\nils 5328 best 12751\nils 5329 best 12751\nils 5332 best 12751\nils 5333 best 12751\nils 5334 best 12751\nils 5335 best 12751\nils 5336 best 12751\nils 5337 best 12751\nils 5338 best 12751\nils 5340 best 12751\nils 5341 best 12751\nils 5342 best 12751\nils 5343 best 12751\nils 5345 best 12751\nils 5346 best 12751\nils 5347 best 12751\nils 5348 best 12751\nils 5349 best 12751\nils 5352 best 12751\nils 5353 best 12751\nils 5354 best 12751\nils 5355 best 12751\nils 5356 best 12751\nils 5357 best 12751\nils 5358 best 12751\nils 5359 best 12751\nils 5360 best 12751\nils 5361 best 12751\nils 5362 best 12751\nils 5363 best 12751\nils 5364 best 12751\nils 5365 best 12751\nils 5367 best 12751\nils 5368 best 12751\nils 5369 best 12751\nils 5370 best 12751\nils 5371 best 12751\nils 5372 best 12751\nils 5373 best 12751\nils 5375 best 12751\nils 5376 best 12751\nils 5377 best 12751\nils 5379 best 12751\nils 5380 best 12751\nils 5381 best 12751\nils 5383 best 12751\nils 5385 best 12751\nils 5386 best 12751\nils 5387 best 12751\nils 5389 best 12751\nils 5391 best 12751\nils 5392 best 12751\nils 5394 best 12751\nils 5395 best 12751\nils 5396 best 12751\nils 5397 best 12751\nils 5399 best 12751\nils 5401 best 12751\nils 5403 best 12751\nils 5404 best 12751\nils 5405 best 12751\nils 5406 best 12751\nils 5407 best 12751\nils 5409 best 12751\nils 5411 best 12751\nils 5412 best 12751\nils 5413 best 12751\nils 5414 best 12751\nils 5415 best 12751\nils 5416 best 12751\nils 5420 best 12751\nils 5421 best 12751\nils 5422 best 12751\nils 5423 best 12751\nils 5424 best 12751\nils 5425 best 12751\nils 5426 best 12751\nils 5428 best 12751\nils 5430 best 12751\nils 5432 best 12751\nils 5433 best 12751\nils 5434 best 12751\nils 5435 best 12751\nils 5438 best 12751\nils 5440 best 12751\nils 5441 best 12751\nils 5443 best 12751\nils 5444 best 12751\nils 5445 best 12751\nils 5447 best 12751\nils 5448 best 12751\nils 5451 best 12751\nils 5452 best 12751\nils 5453 best 12751\nils 5455 best 12751\nils 5456 best 12751\nils 5459 best 12751\nils 5460 best 12751\nils 5461 best 12751\nils 5462 best 12751\nils 5463 best 12751\nils 5464 best 12751\nils 5465 best 12751\nils 5466 best 12751\nils 5468 best 12751\nils 5469 best 12751\nils 5471 best 12751\nils 5474 best 12751\nils 5475 best 12751\nils 5476 best 12751\nils 5478 best 12751\nils 5480 best 12751\nils 5481 best 12751\nils 5482 best 12751\nils 5483 best 12751\nils 5484 best 12751\nils 5485 best 12751\nils 5486 best 12751\nils 5487 best 12751\nils 5488 best 12751\nils 5489 best 12751\nils 5490 best 12751\nils 5492 best 12751\nils 5493 best 12751\nils 5494 best 12751\nils 5497 best 12751\nils 5498 best 12751\nils 5499 best 12751\nils 5500 best 12751\nils 5502 best 12751\nils 5503 best 12751\nils 5504 best 12751\nils 5505 best 12751\nils 5507 best 12751\nils 5508 best 12751\nils 5509 best 12751\nils 5510 best 12751\nils 5511 best 12751\nils 5512 best 12751\nils 5513 best 12751\nils 5514 best 12751\nils 5517 best 12751\nils 5519 best 12751\nils 5521 best 12751\nils 5522 best 12751\nils 5523 best 12751\nils 5524 best 12751\nils 5527 best 12751\nils 5529 best 12751\nils 5530 best 12751\nils 5533 best 12751\nils 5534 best 12751\nils 5536 best 12751\nils 5537 best 12751\nils 5539 best 12751\nils 5540 best 12751\nils 5541 best 12751\nils 5542 best 12751\nils 5546 best 12751\nils 5547 best 12751\nils 5549 best 12751\nils 5550 best 12751\nils 5551 best 12751\nils 5552 best 12751\nils 5554 best 12751\nils 5557 best 12751\nils 5561 best 12751\nils 5562 best 12751\nils 5563 best 12751\nils 5564 best 12751\nils 5565 best 12751\nils 5566 best 12751\nils 5567 best 12751\nils 5568 best 12751\nils 5570 best 12751\nils 5572 best 12751\nils 5573 best 12751\nils 5574 best 12751\nils 5575 best 12751\nils 5577 best 12751\nils 5578 best 12751\nils 5579 best 12751\nils 5580 best 12751\nils 5582 best 12751\nils 5583 best 12751\nils 5584 best 12751\nils 5586 best 12751\nils 5587 best 12751\nils 5588 best 12751\nils 5589 best 12751\nils 5590 best 12751\nils 5591 best 12751\nils 5592 best 12751\nils 5593 best 12751\nils 5594 best 12751\nils 5595 best 12751\nils 5596 best 12751\nils 5598 best 12751\nils 5599 best 12751\nils 5600 best 12751\nils 5601 best 12751\nils 5602 best 12751\nils 5603 best 12751\nils 5605 best 12751\nils 5606 best 12751\nils 5607 best 12751\nils 5608 best 12751\nils 5609 best 12751\nils 5610 best 12751\nils 5611 best 12751\nils 5612 best 12751\nils 5613 best 12751\nils 5614 best 12751\nils 5616 best 12751\nils 5617 best 12751\nils 5618 best 12751\nils 5619 best 12751\nils 5620 best 12751\nils 5621 best 12751\nils 5622 best 12751\nils 5623 best 12751\nils 5624 best 12751\nils 5626 best 12751\nils 5627 best 12751\nils 5628 best 12751\nils 5629 best 12751\nils 5630 best 12751\nils 5631 best 12751\nils 5632 best 12751\nils 5633 best 12751\nils 5634 best 12751\nils 5635 best 12751\nils 5636 best 12751\nils 5637 best 12751\nils 5638 best 12751\nils 5640 best 12751\nils 5642 best 12751\nils 5645 best 12751\nils 5646 best 12751\nils 5647 best 12751\nils 5648 best 12751\nils 5649 best 12751\nils 5650 best 12751\nils 5652 best 12751\nils 5653 best 12751\nils 5654 best 12751\nils 5655 best 12751\nils 5656 best 12751\nils 5657 best 12751\nils 5658 best 12751\nils 5659 best 12751\nils 5660 best 12751\nils 5661 best 12751\nils 5663 best 12751\nils 5664 best 12751\nils 5666 best 12751\nils 5667 best 12751\nils 5668 best 12751\nils 5669 best 12751\nils 5670 best 12751\nils 5671 best 12751\nils 5672 best 12751\nils 5673 best 12751\nils 5674 best 12751\nils 5675 best 12751\nils 5676 best 12751\nils 5678 best 12751\nils 5679 best 12751\nils 5680 best 12751\nils 5681 best 12751\nils 5682 best 12751\nils 5683 best 12751\nils 5684 best 12751\nils 5685 best 12751\nils 5686 best 12751\nils 5687 best 12751\nils 5688 best 12751\nils 5689 best 12751\nils 5691 best 12751\nils 5693 best 12751\nils 5694 best 12751\nils 5695 best 12751\nils 5696 best 12751\nils 5697 best 12751\nils 5698 best 12751\nils 5699 best 12751\nils 5700 best 12751\nils 5702 best 12751\nils 5704 best 12751\nils 5705 best 12751\nils 5706 best 12751\nils 5707 best 12751\nils 5708 best 12751\nils 5709 best 12751\nils 5710 best 12751\nils 5711 best 12751\nils 5715 best 12751\nils 5716 best 12751\nils 5717 best 12751\nils 5719 best 12751\nils 5721 best 12751\nils 5722 best 12751\nils 5724 best 12751\nils 5725 best 12751\nils 5726 best 12751\nils 5727 best 12751\nils 5728 best 12751\nils 5729 best 12751\nils 5730 best 12751\nils 5731 best 12751\nils 5732 best 12751\nils 5733 best 12751\nils 5734 best 12751\nils 5735 best 12751\nils 5736 best 12751\nils 5737 best 12751\nils 5738 best 12751\nils 5739 best 12751\nils 5741 best 12751\nils 5742 best 12751\nils 5744 best 12751\nils 5745 best 12751\nils 5747 best 12751\nils 5748 best 12751\nils 5749 best 12751\nils 5750 best 12751\nils 5751 best 12751\nils 5752 best 12751\nils 5754 best 12751\nils 5755 best 12751\nils 5756 best 12751\nils 5758 best 12751\nils 5759 best 12751\nils 5761 best 12751\nils 5762 best 12751\nils 5763 best 12751\nils 5764 best 12751\nils 5765 best 12751\nils 5766 best 12751\nils 5767 best 12751\nils 5768 best 12751\nils 5769 best 12751\nils 5772 best 12751\nils 5773 best 12751\nils 5774 best 12751\nils 5775 best 12751\nils 5776 best 12751\nils 5777 best 12751\nils 5778 best 12751\nils 5780 best 12751\nils 5781 best 12751\nils 5783 best 12751\nils 5784 best 12751\nils 5785 best 12751\nils 5786 best 12751\nils 5787 best 12751\nils 5788 best 12751\nils 5790 best 12751\nils 5791 best 12751\nils 5793 best 12751\nils 5794 best 12751\nils 5795 best 12751\nils 5798 best 12751\nils 5799 best 12751\nils 5800 best 12751\nils 5802 best 12751\nils 5803 best 12751\nils 5804 best 12751\nils 5805 best 12751\nils 5807 best 12751\nils 5808 best 12751\nils 5809 best 12751\nils 5812 best 12751\nils 5813 best 12751\nils 5816 best 12751\nils 5818 best 12751\nils 5819 best 12751\nils 5820 best 12751\nils 5822 best 12751\nils 5823 best 12751\nils 5824 best 12751\nils 5826 best 12751\nils 5827 best 12751\nils 5828 best 12751\nils 5829 best 12751\nils 5830 best 12751\nils 5831 best 12751\nils 5832 best 12751\nils 5833 best 12751\nils 5834 best 12751\nils 5836 best 12751\nils 5837 best 12751\nils 5840 best 12751\nils 5841 best 12751\nils 5842 best 12751\nils 5845 best 12751\nils 5846 best 12751\nils 5848 best 12751\nils 5849 best 12751\nils 5850 best 12751\nils 5852 best 12751\nils 5854 best 12751\nils 5855 best 12751\nils 5857 best 12751\nils 5858 best 12751\nils 5860 best 12751\nils 5861 best 12751\nils 5862 best 12751\nils 5863 best 12751\nils 5864 best 12751\nils 5866 best 12751\nils 5867 best 12751\nils 5868 best 12751\nils 5869 best 12751\nils 5871 best 12751\nils 5872 best 12751\nils 5876 best 12751\nils 5877 best 12751\nils 5878 best 12751\nils 5879 best 12751\nils 5880 best 12751\nils 5881 best 12751\nils 5882 best 12751\nils 5883 best 12751\nils 5884 best 12751\nils 5885 best 12751\nils 5886 best 12751\nils 5889 best 12751\nils 5890 best 12751\nils 5891 best 12751\nils 5893 best 12751\nils 5894 best 12751\nils 5896 best 12751\nils 5897 best 12751\nils 5898 best 12751\nils 5899 best 12751\nils 5900 best 12751\nils 5902 best 12751\nils 5904 best 12751\nils 5905 best 12751\nils 5906 best 12751\nils 5907 best 12751\nils 5908 best 12751\nils 5910 best 12751\nils 5911 best 12751\nils 5912 best 12751\nils 5913 best 12751\nils 5914 best 12751\nils 5916 best 12751\nils 5917 best 12751\nils 5918 best 12751\nils 5920 best 12751\nils 5923 best 12751\nils 5925 best 12751\nils 5927 best 12751\nils 5928 best 12751\nils 5929 best 12751\nils 5931 best 12751\nils 5933 best 12751\nils 5934 best 12751\nils 5936 best 12751\nils 5937 best 12751\nils 5938 best 12751\nils 5940 best 12751\nils 5942 best 12751\nils 5943 best 12751\nils 5944 best 12751\nils 5945 best 12751\nils 5946 best 12751\nils 5947 best 12751\nils 5948 best 12751\nils 5949 best 12751\nils 5950 best 12751\nils 5952 best 12751\nils 5954 best 12751\nils 5955 best 12751\nils 5956 best 12751\nils 5957 best 12751\nils 5958 best 12751\nils 5960 best 12751\nils 5965 best 12751\nils 5966 best 12751\nils 5967 best 12751\nils 5969 best 12751\nils 5970 best 12751\nils 5971 best 12751\nils 5973 best 12751\nils 5974 best 12751\nils 5976 best 12751\nils 5977 best 12751\nils 5978 best 12751\nils 5979 best 12751\nils 5981 best 12751\nils 5983 best 12751\nils 5984 best 12751\nils 5985 best 12751\nils 5986 best 12751\nils 5987 best 12751\nils 5988 best 12751\nils 5989 best 12751\nils 5990 best 12751\nils 5993 best 12751\nils 5996 best 12751\nils 5997 best 12751\nils 5998 best 12751\nils 5999 best 12751\nfinal 12751",
   "vmhwm_bytes": 675840
  },
  {
   "args": [
    "pi2.txt",
    "drift9206.txt",
    "4000",
    "9406",
    "31",
    "drift9406.txt",
    "dump9406"
   ],
   "binary": "np_ils7",
   "charged_peak_bytes": 1012019,
   "image": {
    "bss": 792160,
    "data": 24,
    "image": 815535,
    "text": 23351
   },
   "name": "long plateau drift (pass 14)",
   "outputs": {
    "dump9406/acc_3273.txt": "0b114a32ed91c9129207a51b227e14660f1f80af3b867773284a141c544c6ae3",
    "dump9406/acc_3301.txt": "75eb45ab0d3871c3fd7bf27d5a7336d766b413aaf56af8b610d99bd3f8d5e920"
   },
   "retained_input_output_bytes": 65412,
   "seconds": 6089.75,
   "stack_reserve": 131072,
   "stdout": "start 12751\nils 0 best 12751\nils 1 best 12751\nils 4 best 12751\nils 7 best 12751\nils 10 best 12751\nils 16 best 12751\nils 18 best 12751\nils 20 best 12751\nils 22 best 12751\nils 23 best 12751\nils 24 best 12751\nils 29 best 12751\nils 31 best 12751\nils 32 best 12751\nils 33 best 12751\nils 34 best 12751\nils 37 best 12751\nils 41 best 12751\nils 43 best 12751\nils 46 best 12751\nils 49 best 12751\nils 51 best 12751\nils 60 best 12751\nils 63 best 12751\nils 64 best 12751\nils 66 best 12751\nils 67 best 12751\nils 68 best 12751\nils 73 best 12751\nils 77 best 12751\nils 78 best 12751\nils 80 best 12751\nils 83 best 12751\nils 84 best 12751\nils 87 best 12751\nils 90 best 12751\nils 91 best 12751\nils 97 best 12751\nils 99 best 12751\nils 102 best 12751\nils 106 best 12751\nils 107 best 12751\nils 108 best 12751\nils 113 best 12751\nils 114 best 12751\nils 118 best 12751\nils 119 best 12751\nils 120 best 12751\nils 127 best 12751\nils 133 best 12751\nils 135 best 12751\nils 137 best 12751\nils 138 best 12751\nils 139 best 12751\nils 141 best 12751\nils 143 best 12751\nils 147 best 12751\nils 148 best 12751\nils 149 best 12751\nils 151 best 12751\nils 152 best 12751\nils 156 best 12751\nils 157 best 12751\nils 161 best 12751\nils 163 best 12751\nils 166 best 12751\nils 170 best 12751\nils 171 best 12751\nils 172 best 12751\nils 182 best 12751\nils 188 best 12751\nils 189 best 12751\nils 190 best 12751\nils 191 best 12751\nils 192 best 12751\nils 195 best 12751\nils 197 best 12751\nils 198 best 12751\nils 200 best 12751\nils 203 best 12751\nils 204 best 12751\nils 205 best 12751\nils 210 best 12751\nils 221 best 12751\nils 225 best 12751\nils 226 best 12751\nils 236 best 12751\nils 243 best 12751\nils 246 best 12751\nils 248 best 12751\nils 249 best 12751\nils 252 best 12751\nils 254 best 12751\nils 255 best 12751\nils 257 best 12751\nils 259 best 12751\nils 265 best 12751\nils 267 best 12751\nils 271 best 12751\nils 273 best 12751\nils 274 best 12751\nils 275 best 12751\nils 276 best 12751\nils 277 best 12751\nils 284 best 12751\nils 286 best 12751\nils 288 best 12751\nils 290 best 12751\nils 291 best 12751\nils 292 best 12751\nils 293 best 12751\nils 295 best 12751\nils 297 best 12751\nils 299 best 12751\nils 301 best 12751\nils 304 best 12751\nils 305 best 12751\nils 308 best 12751\nils 313 best 12751\nils 316 best 12751\nils 317 best 12751\nils 321 best 12751\nils 326 best 12751\nils 329 best 12751\nils 330 best 12751\nils 334 best 12751\nils 336 best 12751\nils 338 best 12751\nils 339 best 12751\nils 342 best 12751\nils 346 best 12751\nils 347 best 12751\nils 351 best 12751\nils 352 best 12751\nils 355 best 12751\nils 357 best 12751\nils 358 best 12751\nils 364 best 12751\nils 371 best 12751\nils 373 best 12751\nils 374 best 12751\nils 387 best 12751\nils 388 best 12751\nils 391 best 12751\nils 395 best 12751\nils 396 best 12751\nils 401 best 12751\nils 402 best 12751\nils 404 best 12751\nils 405 best 12751\nils 407 best 12751\nils 411 best 12751\nils 418 best 12751\nils 419 best 12751\nils 425 best 12751\nils 427 best 12751\nils 428 best 12751\nils 430 best 12751\nils 432 best 12751\nils 434 best 12751\nils 437 best 12751\nils 438 best 12751\nils 440 best 12751\nils 442 best 12751\nils 443 best 12751\nils 446 best 12751\nils 447 best 12751\nils 452 best 12751\nils 453 best 12751\nils 454 best 12751\nils 458 best 12751\nils 460 best 12751\nils 462 best 12751\nils 464 best 12751\nils 465 best 12751\nils 472 best 12751\nils 474 best 12751\nils 475 best 12751\nils 479 best 12751\nils 484 best 12751\nils 486 best 12751\nils 497 best 12751\nils 499 best 12751\nils 502 best 12751\nils 504 best 12751\nils 505 best 12751\nils 511 best 12751\nils 512 best 12751\nils 514 best 12751\nils 518 best 12751\nils 519 best 12751\nils 522 best 12751\nils 523 best 12751\nils 524 best 12751\nils 527 best 12751\nils 529 best 12751\nils 530 best 12751\nils 532 best 12751\nils 533 best 12751\nils 541 best 12751\nils 542 best 12751\nils 553 best 12751\nils 555 best 12751\nils 557 best 12751\nils 558 best 12751\nils 560 best 12751\nils 563 best 12751\nils 564 best 12751\nils 566 best 12751\nils 567 best 12751\nils 568 best 12751\nils 569 best 12751\nils 570 best 12751\nils 574 best 12751\nils 578 best 12751\nils 580 best 12751\nils 581 best 12751\nils 582 best 12751\nils 583 best 12751\nils 584 best 12751\nils 585 best 12751\nils 586 best 12751\nils 588 best 12751\nils 591 best 12751\nils 592 best 12751\nils 600 best 12751\nils 602 best 12751\nils 603 best 12751\nils 606 best 12751\nils 607 best 12751\nils 613 best 12751\nils 614 best 12751\nils 615 best 12751\nils 616 best 12751\nils 619 best 12751\nils 620 best 12751\nils 628 best 12751\nils 629 best 12751\nils 631 best 12751\nils 634 best 12751\nils 638 best 12751\nils 639 best 12751\nils 640 best 12751\nils 642 best 12751\nils 643 best 12751\nils 645 best 12751\nils 649 best 12751\nils 650 best 12751\nils 653 best 12751\nils 654 best 12751\nils 662 best 12751\nils 663 best 12751\nils 664 best 12751\nils 668 best 12751\nils 674 best 12751\nils 676 best 12751\nils 681 best 12751\nils 683 best 12751\nils 684 best 12751\nils 685 best 12751\nils 686 best 12751\nils 687 best 12750\nils 689 best 12750\nils 697 best 12750\nils 698 best 12750\nils 702 best 12750\nils 703 best 12750\nils 712 best 12750\nils 714 best 12750\nils 717 best 12750\nils 718 best 12750\nils 720 best 12750\nils 727 best 12750\nils 728 best 12750\nils 734 best 12750\nils 736 best 12750\nils 739 best 12750\nils 746 best 12750\nils 747 best 12750\nils 749 best 12750\nils 750 best 12750\nils 755 best 12750\nils 757 best 12750\nils 763 best 12750\nils 765 best 12750\nils 767 best 12750\nils 769 best 12750\nils 771 best 12750\nils 779 best 12750\nils 784 best 12750\nils 785 best 12750\nils 788 best 12750\nils 790 best 12750\nils 791 best 12750\nils 797 best 12750\nils 805 best 12750\nils 808 best 12750\nils 809 best 12750\nils 811 best 12750\nils 814 best 12750\nils 816 best 12750\nils 817 best 12750\nils 818 best 12750\nils 819 best 12750\nils 828 best 12750\nils 829 best 12750\nils 834 best 12750\nils 835 best 12750\nils 838 best 12750\nils 839 best 12750\nils 840 best 12750\nils 842 best 12750\nils 844 best 12750\nils 845 best 12750\nils 848 best 12750\nils 849 best 12750\nils 850 best 12750\nils 851 best 12750\nils 852 best 12750\nils 853 best 12750\nils 858 best 12750\nils 861 best 12750\nils 863 best 12750\nils 864 best 12750\nils 866 best 12750\nils 869 best 12750\nils 872 best 12750\nils 880 best 12750\nils 882 best 12750\nils 885 best 12750\nils 890 best 12750\nils 899 best 12750\nils 900 best 12750\nils 903 best 12750\nils 906 best 12750\nils 907 best 12750\nils 908 best 12750\nils 911 best 12750\nils 912 best 12750\nils 913 best 12750\nils 918 best 12750\nils 919 best 12750\nils 920 best 12750\nils 921 best 12750\nils 922 best 12750\nils 925 best 12750\nils 926 best 12750\nils 927 best 12750\nils 938 best 12750\nils 940 best 12750\nils 943 best 12750\nils 947 best 12750\nils 948 best 12750\nils 949 best 12750\nils 952 best 12750\nils 953 best 12750\nils 954 best 12750\nils 957 best 12750\nils 958 best 12750\nils 959 best 12750\nils 960 best 12750\nils 961 best 12750\nils 962 best 12750\nils 965 best 12750\nils 966 best 12750\nils 967 best 12750\nils 971 best 12750\nils 974 best 12750\nils 976 best 12750\nils 984 best 12750\nils 985 best 12750\nils 987 best 12750\nils 988 best 12750\nils 990 best 12750\nils 991 best 12750\nils 992 best 12750\nils 995 best 12750\nils 999 best 12750\nils 1002 best 12750\nils 1003 best 12750\nils 1005 best 12750\nils 1007 best 12750\nils 1016 best 12750\nils 1017 best 12750\nils 1022 best 12750\nils 1024 best 12750\nils 1026 best 12750\nils 1029 best 12750\nils 1030 best 12750\nils 1031 best 12750\nils 1034 best 12750\nils 1037 best 12750\nils 1039 best 12750\nils 1042 best 12750\nils 1046 best 12750\nils 1061 best 12750\nils 1062 best 12750\nils 1064 best 12750\nils 1065 best 12750\nils 1066 best 12750\nils 1070 best 12750\nils 1080 best 12750\nils 1081 best 12750\nils 1089 best 12750\nils 1090 best 12750\nils 1094 best 12750\nils 1097 best 12750\nils 1098 best 12750\nils 1104 best 12750\nils 1107 best 12750\nils 1109 best 12750\nils 1112 best 12750\nils 1113 best 12750\nils 1115 best 12750\nils 1116 best 12750\nils 1118 best 12750\nils 1124 best 12750\nils 1125 best 12750\nils 1127 best 12750\nils 1131 best 12750\nils 1134 best 12750\nils 1136 best 12750\nils 1141 best 12750\nils 1142 best 12750\nils 1148 best 12750\nils 1155 best 12750\nils 1156 best 12750\nils 1162 best 12750\nils 1165 best 12750\nils 1166 best 12750\nils 1167 best 12750\nils 1170 best 12750\nils 1172 best 12750\nils 1173 best 12750\nils 1178 best 12750\nils 1179 best 12750\nils 1182 best 12750\nils 1190 best 12750\nils 1195 best 12750\nils 1196 best 12750\nils 1199 best 12750\nils 1200 best 12750\nils 1205 best 12750\nils 1207 best 12750\nils 1208 best 12750\nils 1210 best 12750\nils 1213 best 12750\nils 1214 best 12750\nils 1216 best 12750\nils 1219 best 12750\nils 1220 best 12750\nils 1221 best 12750\nils 1225 best 12750\nils 1226 best 12750\nils 1227 best 12750\nils 1232 best 12750\nils 1234 best 12750\nils 1236 best 12750\nils 1242 best 12750\nils 1243 best 12750\nils 1244 best 12750\nils 1246 best 12750\nils 1248 best 12750\nils 1249 best 12750\nils 1252 best 12750\nils 1255 best 12750\nils 1260 best 12750\nils 1261 best 12750\nils 1262 best 12750\nils 1271 best 12750\nils 1274 best 12750\nils 1275 best 12750\nils 1277 best 12750\nils 1282 best 12750\nils 1285 best 12750\nils 1287 best 12750\nils 1288 best 12750\nils 1289 best 12750\nils 1290 best 12750\nils 1293 best 12750\nils 1297 best 12750\nils 1298 best 12750\nils 1302 best 12750\nils 1305 best 12750\nils 1308 best 12750\nils 1311 best 12750\nils 1313 best 12750\nils 1320 best 12750\nils 1322 best 12750\nils 1323 best 12750\nils 1325 best 12750\nils 1331 best 12750\nils 1333 best 12750\nils 1336 best 12750\nils 1342 best 12750\nils 1344 best 12750\nils 1346 best 12750\nils 1353 best 12750\nils 1356 best 12750\nils 1357 best 12750\nils 1358 best 12750\nils 1359 best 12750\nils 1361 best 12750\nils 1362 best 12750\nils 1363 best 12750\nils 1367 best 12750\nils 1369 best 12750\nils 1371 best 12750\nils 1375 best 12750\nils 1378 best 12750\nils 1382 best 12750\nils 1384 best 12750\nils 1385 best 12750\nils 1393 best 12750\nils 1394 best 12750\nils 1397 best 12750\nils 1400 best 12750\nils 1404 best 12750\nils 1407 best 12750\nils 1410 best 12750\nils 1411 best 12750\nils 1412 best 12750\nils 1413 best 12750\nils 1414 best 12750\nils 1418 best 12750\nils 1421 best 12750\nils 1424 best 12750\nils 1428 best 12750\nils 1432 best 12750\nils 1435 best 12750\nils 1442 best 12750\nils 1447 best 12750\nils 1448 best 12750\nils 1449 best 12750\nils 1450 best 12750\nils 1456 best 12750\nils 1464 best 12750\nils 1465 best 12750\nils 1466 best 12750\nils 1469 best 12750\nils 1470 best 12750\nils 1475 best 12750\nils 1477 best 12750\nils 1480 best 12750\nils 1483 best 12750\nils 1484 best 12750\nils 1485 best 12750\nils 1486 best 12750\nils 1492 best 12750\nils 1493 best 12750\nils 1494 best 12750\nils 1496 best 12750\nils 1499 best 12750\nils 1502 best 12750\nils 1505 best 12750\nils 1508 best 12750\nils 1511 best 12750\nils 1514 best 12750\nils 1517 best 12750\nils 1526 best 12750\nils 1536 best 12750\nils 1537 best 12750\nils 1542 best 12750\nils 1543 best 12750\nils 1550 best 12750\nils 1552 best 12750\nils 1555 best 12750\nils 1557 best 12750\nils 1558 best 12750\nils 1559 best 12750\nils 1569 best 12750\nils 1571 best 12750\nils 1574 best 12750\nils 1576 best 12750\nils 1577 best 12750\nils 1580 best 12750\nils 1583 best 12750\nils 1585 best 12750\nils 1588 best 12750\nils 1592 best 12750\nils 1595 best 12750\nils 1597 best 12750\nils 1602 best 12750\nils 1603 best 12750\nils 1604 best 12750\nils 1608 best 12750\nils 1609 best 12750\nils 1610 best 12750\nils 1613 best 12750\nils 1614 best 12750\nils 1615 best 12750\nils 1616 best 12750\nils 1620 best 12750\nils 1622 best 12750\nils 1623 best 12750\nils 1627 best 12750\nils 1628 best 12750\nils 1629 best 12750\nils 1630 best 12750\nils 1631 best 12750\nils 1633 best 12750\nils 1636 best 12750\nils 1639 best 12750\nils 1641 best 12750\nils 1644 best 12750\nils 1649 best 12750\nils 1650 best 12750\nils 1653 best 12750\nils 1655 best 12750\nils 1656 best 12750\nils 1660 best 12750\nils 1663 best 12750\nils 1664 best 12750\nils 1665 best 12750\nils 1669 best 12750\nils 1673 best 12750\nils 1674 best 12750\nils 1675 best 12750\nils 1684 best 12750\nils 1685 best 12750\nils 1686 best 12750\nils 1687 best 12750\nils 1690 best 12750\nils 1691 best 12750\nils 1695 best 12750\nils 1696 best 12750\nils 1700 best 12750\nils 1702 best 12750\nils 1707 best 12750\nils 1711 best 12750\nils 1715 best 12750\nils 1718 best 12750\nils 1719 best 12750\nils 1726 best 12750\nils 1734 best 12750\nils 1735 best 12750\nils 1738 best 12750\nils 1739 best 12750\nils 1740 best 12750\nils 1745 best 12750\nils 1747 best 12750\nils 1748 best 12750\nils 1753 best 12750\nils 1757 best 12750\nils 1758 best 12750\nils 1759 best 12750\nils 1762 best 12750\nils 1763 best 12750\nils 1765 best 12750\nils 1769 best 12750\nils 1771 best 12750\nils 1772 best 12750\nils 1777 best 12750\nils 1778 best 12750\nils 1782 best 12750\nils 1786 best 12750\nils 1789 best 12750\nils 1792 best 12750\nils 1795 best 12750\nils 1796 best 12750\nils 1800 best 12750\nils 1802 best 12750\nils 1803 best 12750\nils 1810 best 12750\nils 1814 best 12750\nils 1823 best 12750\nils 1824 best 12750\nils 1826 best 12750\nils 1827 best 12750\nils 1831 best 12750\nils 1832 best 12750\nils 1833 best 12750\nils 1834 best 12750\nils 1836 best 12750\nils 1838 best 12750\nils 1839 best 12750\nils 1841 best 12750\nils 1842 best 12750\nils 1845 best 12750\nils 1847 best 12750\nils 1849 best 12750\nils 1851 best 12750\nils 1852 best 12750\nils 1853 best 12750\nils 1857 best 12750\nils 1858 best 12750\nils 1861 best 12750\nils 1862 best 12750\nils 1864 best 12750\nils 1865 best 12750\nils 1866 best 12750\nils 1870 best 12750\nils 1876 best 12750\nils 1878 best 12750\nils 1888 best 12750\nils 1893 best 12750\nils 1894 best 12750\nils 1896 best 12750\nils 1899 best 12750\nils 1900 best 12750\nils 1901 best 12750\nils 1902 best 12750\nils 1906 best 12750\nils 1907 best 12750\nils 1908 best 12750\nils 1909 best 12750\nils 1911 best 12750\nils 1915 best 12750\nils 1916 best 12750\nils 1917 best 12750\nils 1918 best 12750\nils 1919 best 12750\nils 1923 best 12750\nils 1924 best 12750\nils 1925 best 12750\nils 1926 best 12750\nils 1931 best 12750\nils 1932 best 12750\nils 1937 best 12750\nils 1938 best 12750\nils 1939 best 12750\nils 1940 best 12750\nils 1949 best 12750\nils 1954 best 12750\nils 1956 best 12750\nils 1958 best 12750\nils 1960 best 12750\nils 1962 best 12750\nils 1965 best 12750\nils 1966 best 12750\nils 1967 best 12750\nils 1968 best 12750\nils 1972 best 12750\nils 1974 best 12750\nils 1975 best 12750\nils 1977 best 12750\nils 1980 best 12750\nils 1981 best 12750\nils 1986 best 12750\nils 1987 best 12750\nils 1990 best 12750\nils 1992 best 12750\nils 1993 best 12750\nils 1994 best 12750\nils 1998 best 12750\nils 1999 best 12750\nils 2000 best 12750\nils 2001 best 12750\nils 2002 best 12750\nils 2004 best 12750\nils 2005 best 12750\nils 2010 best 12750\nils 2013 best 12750\nils 2016 best 12750\nils 2022 best 12750\nils 2024 best 12750\nils 2027 best 12750\nils 2033 best 12750\nils 2034 best 12750\nils 2037 best 12750\nils 2046 best 12750\nils 2050 best 12750\nils 2051 best 12750\nils 2054 best 12750\nils 2059 best 12750\nils 2068 best 12750\nils 2073 best 12750\nils 2074 best 12750\nils 2076 best 12750\nils 2083 best 12750\nils 2084 best 12750\nils 2090 best 12750\nils 2091 best 12750\nils 2099 best 12750\nils 2100 best 12750\nils 2102 best 12750\nils 2106 best 12750\nils 2108 best 12750\nils 2109 best 12750\nils 2110 best 12750\nils 2111 best 12750\nils 2114 best 12750\nils 2122 best 12750\nils 2123 best 12750\nils 2128 best 12750\nils 2129 best 12750\nils 2130 best 12750\nils 2131 best 12750\nils 2133 best 12750\nils 2134 best 12750\nils 2136 best 12750\nils 2137 best 12750\nils 2138 best 12750\nils 2143 best 12750\nils 2149 best 12750\nils 2150 best 12750\nils 2151 best 12750\nils 2152 best 12750\nils 2154 best 12750\nils 2156 best 12750\nils 2157 best 12750\nils 2159 best 12750\nils 2166 best 12750\nils 2167 best 12750\nils 2168 best 12750\nils 2179 best 12750\nils 2189 best 12750\nils 2190 best 12750\nils 2192 best 12750\nils 2196 best 12750\nils 2199 best 12750\nils 2202 best 12750\nils 2203 best 12750\nils 2213 best 12750\nils 2214 best 12750\nils 2223 best 12750\nils 2234 best 12750\nils 2237 best 12750\nils 2242 best 12750\nils 2243 best 12750\nils 2245 best 12750\nils 2247 best 12750\nils 2249 best 12750\nils 2250 best 12750\nils 2254 best 12750\nils 2257 best 12750\nils 2264 best 12750\nils 2271 best 12750\nils 2272 best 12750\nils 2273 best 12750\nils 2274 best 12750\nils 2276 best 12750\nils 2278 best 12750\nils 2279 best 12750\nils 2280 best 12750\nils 2281 best 12750\nils 2282 best 12750\nils 2286 best 12750\nils 2292 best 12750\nils 2293 best 12750\nils 2300 best 12750\nils 2303 best 12750\nils 2307 best 12750\nils 2309 best 12750\nils 2319 best 12750\nils 2320 best 12750\nils 2323 best 12750\nils 2325 best 12750\nils 2326 best 12750\nils 2328 best 12750\nils 2334 best 12750\nils 2335 best 12750\nils 2336 best 12750\nils 2337 best 12750\nils 2338 best 12750\nils 2341 best 12750\nils 2342 best 12750\nils 2345 best 12750\nils 2346 best 12750\nils 2348 best 12750\nils 2349 best 12750\nils 2352 best 12750\nils 2355 best 12750\nils 2356 best 12750\nils 2358 best 12750\nils 2359 best 12750\nils 2363 best 12750\nils 2364 best 12750\nils 2365 best 12750\nils 2368 best 12750\nils 2370 best 12750\nils 2372 best 12750\nils 2373 best 12750\nils 2374 best 12750\nils 2376 best 12750\nils 2377 best 12750\nils 2380 best 12750\nils 2387 best 12750\nils 2388 best 12750\nils 2389 best 12750\nils 2393 best 12750\nils 2394 best 12750\nils 2396 best 12750\nils 2397 best 12750\nils 2401 best 12750\nils 2407 best 12750\nils 2408 best 12750\nils 2414 best 12750\nils 2423 best 12750\nils 2425 best 12750\nils 2427 best 12750\nils 2429 best 12750\nils 2431 best 12750\nils 2433 best 12750\nils 2434 best 12750\nils 2437 best 12750\nils 2439 best 12750\nils 2441 best 12750\nils 2442 best 12750\nils 2449 best 12750\nils 2451 best 12750\nils 2452 best 12750\nils 2458 best 12750\nils 2459 best 12750\nils 2463 best 12750\nils 2464 best 12750\nils 2466 best 12750\nils 2468 best 12750\nils 2469 best 12750\nils 2470 best 12750\nils 2471 best 12750\nils 2472 best 12750\nils 2474 best 12750\nils 2479 best 12750\nils 2480 best 12750\nils 2481 best 12750\nils 2484 best 12750\nils 2486 best 12750\nils 2487 best 12750\nils 2489 best 12750\nils 2490 best 12750\nils 2492 best 12750\nils 2494 best 12750\nils 2498 best 12750\nils 2499 best 12750\nils 2501 best 12750\nils 2502 best 12750\nils 2503 best 12750\nils 2505 best 12750\nils 2506 best 12750\nils 2510 best 12750\nils 2512 best 12750\nils 2515 best 12750\nils 2516 best 12750\nils 2520 best 12750\nils 2524 best 12750\nils 2525 best 12750\nils 2526 best 12750\nils 2527 best 12750\nils 2534 best 12750\nils 2537 best 12750\nils 2541 best 12750\nils 2543 best 12750\nils 2545 best 12750\nils 2547 best 12750\nils 2549 best 12750\nils 2552 best 12750\nils 2554 best 12750\nils 2555 best 12750\nils 2556 best 12750\nils 2558 best 12750\nils 2559 best 12750\nils 2563 best 12750\nils 2567 best 12750\nils 2569 best 12750\nils 2575 best 12750\nils 2577 best 12750\nils 2578 best 12750\nils 2579 best 12750\nils 2581 best 12750\nils 2591 best 12750\nils 2592 best 12750\nils 2594 best 12750\nils 2596 best 12750\nils 2600 best 12750\nils 2602 best 12750\nils 2605 best 12750\nils 2606 best 12750\nils 2609 best 12750\nils 2615 best 12750\nils 2617 best 12750\nils 2618 best 12750\nils 2620 best 12750\nils 2627 best 12750\nils 2628 best 12750\nils 2629 best 12750\nils 2630 best 12750\nils 2634 best 12750\nils 2635 best 12750\nils 2642 best 12750\nils 2643 best 12750\nils 2645 best 12750\nils 2647 best 12750\nils 2648 best 12750\nils 2649 best 12750\nils 2655 best 12750\nils 2661 best 12750\nils 2664 best 12750\nils 2671 best 12750\nils 2673 best 12750\nils 2675 best 12750\nils 2676 best 12750\nils 2681 best 12750\nils 2682 best 12750\nils 2690 best 12750\nils 2696 best 12750\nils 2700 best 12750\nils 2705 best 12750\nils 2706 best 12750\nils 2709 best 12750\nils 2710 best 12750\nils 2716 best 12750\nils 2717 best 12750\nils 2718 best 12750\nils 2719 best 12750\nils 2723 best 12750\nils 2724 best 12750\nils 2725 best 12750\nils 2726 best 12750\nils 2727 best 12750\nils 2734 best 12750\nils 2737 best 12750\nils 2738 best 12750\nils 2743 best 12750\nils 2748 best 12750\nils 2752 best 12750\nils 2754 best 12750\nils 2756 best 12750\nils 2761 best 12750\nils 2763 best 12750\nils 2767 best 12750\nils 2768 best 12750\nils 2769 best 12750\nils 2770 best 12750\nils 2774 best 12750\nils 2775 best 12750\nils 2778 best 12750\nils 2779 best 12750\nils 2783 best 12750\nils 2785 best 12750\nils 2787 best 12750\nils 2792 best 12750\nils 2794 best 12750\nils 2795 best 12750\nils 2799 best 12750\nils 2802 best 12750\nils 2804 best 12750\nils 2808 best 12750\nils 2815 best 12750\nils 2818 best 12750\nils 2823 best 12750\nils 2827 best 12750\nils 2830 best 12750\nils 2832 best 12750\nils 2833 best 12750\nils 2835 best 12750\nils 2837 best 12750\nils 2841 best 12750\nils 2842 best 12750\nils 2843 best 12750\nils 2846 best 12750\nils 2849 best 12750\nils 2858 best 12750\nils 2860 best 12750\nils 2863 best 12750\nils 2866 best 12750\nils 2868 best 12750\nils 2880 best 12750\nils 2881 best 12750\nils 2882 best 12750\nils 2885 best 12750\nils 2887 best 12750\nils 2889 best 12750\nils 2892 best 12750\nils 2895 best 12750\nils 2899 best 12750\nils 2900 best 12750\nils 2902 best 12750\nils 2903 best 12750\nils 2908 best 12750\nils 2910 best 12750\nils 2911 best 12750\nils 2914 best 12750\nils 2924 best 12750\nils 2929 best 12750\nils 2935 best 12750\nils 2936 best 12750\nils 2942 best 12750\nils 2948 best 12750\nils 2950 best 12750\nils 2955 best 12750\nils 2956 best 12750\nils 2957 best 12750\nils 2958 best 12750\nils 2961 best 12750\nils 2969 best 12750\nils 2971 best 12750\nils 2979 best 12750\nils 2981 best 12750\nils 2987 best 12750\nils 2988 best 12750\nils 2989 best 12750\nils 2993 best 12750\nils 2994 best 12750\nils 2996 best 12750\nils 2997 best 12750\nils 3001 best 12750\nils 3002 best 12750\nils 3015 best 12750\nils 3020 best 12750\nils 3025 best 12750\nils 3028 best 12750\nils 3029 best 12750\nils 3032 best 12750\nils 3034 best 12750\nils 3037 best 12750\nils 3039 best 12750\nils 3040 best 12750\nils 3041 best 12750\nils 3042 best 12750\nils 3043 best 12750\nils 3046 best 12750\nils 3048 best 12750\nils 3049 best 12750\nils 3050 best 12750\nils 3051 best 12750\nils 3052 best 12750\nils 3054 best 12750\nils 3056 best 12750\nils 3059 best 12750\nils 3060 best 12750\nils 3061 best 12750\nils 3062 best 12750\nils 3063 best 12750\nils 3065 best 12750\nils 3067 best 12750\nils 3068 best 12750\nils 3072 best 12750\nils 3074 best 12750\nils 3079 best 12750\nils 3080 best 12750\nils 3081 best 12750\nils 3086 best 12750\nils 3087 best 12750\nils 3088 best 12750\nils 3091 best 12750\nils 3096 best 12750\nils 3099 best 12750\nils 3104 best 12750\nils 3106 best 12750\nils 3108 best 12750\nils 3111 best 12750\nils 3115 best 12750\nils 3116 best 12750\nils 3117 best 12750\nils 3118 best 12750\nils 3119 best 12750\nils 3122 best 12750\nils 3123 best 12750\nils 3127 best 12750\nils 3130 best 12750\nils 3143 best 12750\nils 3144 best 12750\nils 3150 best 12750\nils 3151 best 12750\nils 3152 best 12750\nils 3157 best 12750\nils 3158 best 12750\nils 3159 best 12750\nils 3161 best 12750\nils 3167 best 12750\nils 3173 best 12750\nils 3174 best 12750\nils 3175 best 12750\nils 3179 best 12750\nils 3183 best 12750\nils 3185 best 12750\nils 3187 best 12750\nils 3189 best 12750\nils 3190 best 12750\nils 3196 best 12750\nils 3198 best 12750\nils 3200 best 12750\nils 3202 best 12750\nils 3206 best 12750\nils 3208 best 12750\nils 3215 best 12750\nils 3216 best 12750\nils 3219 best 12750\nils 3220 best 12750\nils 3226 best 12750\nils 3227 best 12750\nils 3233 best 12750\nils 3236 best 12750\nils 3237 best 12750\nils 3239 best 12750\nils 3241 best 12750\nils 3243 best 12750\nils 3248 best 12750\nils 3252 best 12750\nils 3256 best 12750\nils 3263 best 12750\nils 3268 best 12750\nils 3269 best 12750\nils 3273 best 12750\nils 3274 best 12750\nils 3276 best 12750\nils 3277 best 12750\nils 3288 best 12750\nils 3290 best 12750\nils 3300 best 12750\nils 3301 best 12750\nils 3303 best 12750\nils 3304 best 12750\nils 3305 best 12750\nils 3307 best 12750\nils 3310 best 12750\nils 3317 best 12750\nils 3320 best 12750\nils 3321 best 12750\nils 3323 best 12750\nils 3324 best 12750\nils 3325 best 12750\nils 3328 best 12750\nils 3329 best 12750\nils 3330 best 12750\nils 3333 best 12750\nils 3338 best 12750\nils 3341 best 12750\nils 3344 best 12750\nils 3347 best 12750\nils 3349 best 12750\nils 3353 best 12750\nils 3356 best 12750\nils 3357 best 12750\nils 3358 best 12750\nils 3360 best 12750\nils 3368 best 12750\nils 3371 best 12750\nils 3372 best 12750\nils 3373 best 12750\nils 3379 best 12750\nils 3380 best 12750\nils 3381 best 12750\nils 3384 best 12750\nils 3387 best 12750\nils 3389 best 12750\nils 3390 best 12750\nils 3392 best 12750\nils 3394 best 12750\nils 3396 best 12750\nils 3400 best 12750\nils 3405 best 12750\nils 3407 best 12750\nils 3409 best 12750\nils 3413 best 12750\nils 3414 best 12750\nils 3420 best 12750\nils 3421 best 12750\nils 3432 best 12750\nils 3434 best 12750\nils 3435 best 12750\nils 3436 best 12750\nils 3440 best 12750\nils 3444 best 12750\nils 3446 best 12750\nils 3449 best 12750\nils 3451 best 12750\nils 3454 best 12750\nils 3455 best 12750\nils 3457 best 12750\nils 3459 best 12750\nils 3462 best 12750\nils 3467 best 12750\nils 3469 best 12750\nils 3470 best 12750\nils 3472 best 12750\nils 3473 best 12750\nils 3474 best 12750\nils 3477 best 12750\nils 3478 best 12750\nils 3483 best 12750\nils 3489 best 12750\nils 3495 best 12750\nils 3496 best 12750\nils 3498 best 12750\nils 3500 best 12750\nils 3502 best 12750\nils 3503 best 12750\nils 3504 best 12750\nils 3509 best 12750\nils 3511 best 12750\nils 3512 best 12750\nils 3513 best 12750\nils 3514 best 12750\nils 3521 best 12750\nils 3524 best 12750\nils 3526 best 12750\nils 3528 best 12750\nils 3531 best 12750\nils 3535 best 12750\nils 3537 best 12750\nils 3539 best 12750\nils 3540 best 12750\nils 3543 best 12750\nils 3546 best 12750\nils 3555 best 12750\nils 3559 best 12750\nils 3563 best 12750\nils 3565 best 12750\nils 3568 best 12750\nils 3573 best 12750\nils 3576 best 12750\nils 3580 best 12750\nils 3581 best 12750\nils 3582 best 12750\nils 3583 best 12750\nils 3584 best 12750\nils 3585 best 12750\nils 3590 best 12750\nils 3592 best 12750\nils 3594 best 12750\nils 3595 best 12750\nils 3598 best 12750\nils 3599 best 12750\nils 3601 best 12750\nils 3605 best 12750\nils 3606 best 12750\nils 3607 best 12750\nils 3609 best 12750\nils 3611 best 12750\nils 3616 best 12750\nils 3618 best 12750\nils 3620 best 12750\nils 3626 best 12750\nils 3630 best 12750\nils 3632 best 12750\nils 3634 best 12750\nils 3645 best 12750\nils 3650 best 12750\nils 3652 best 12750\nils 3654 best 12750\nils 3657 best 12750\nils 3659 best 12750\nils 3660 best 12750\nils 3667 best 12750\nils 3671 best 12750\nils 3674 best 12750\nils 3675 best 12750\nils 3681 best 12750\nils 3682 best 12750\nils 3683 best 12750\nils 3686 best 12750\nils 3687 best 12750\nils 3690 best 12750\nils 3692 best 12750\nils 3693 best 12750\nils 3696 best 12750\nils 3699 best 12750\nils 3704 best 12750\nils 3706 best 12750\nils 3713 best 12750\nils 3715 best 12750\nils 3716 best 12750\nils 3717 best 12750\nils 3718 best 12750\nils 3720 best 12750\nils 3722 best 12750\nils 3727 best 12750\nils 3728 best 12750\nils 3729 best 12750\nils 3731 best 12750\nils 3736 best 12750\nils 3739 best 12750\nils 3740 best 12750\nils 3744 best 12750\nils 3745 best 12750\nils 3747 best 12750\nils 3752 best 12750\nils 3757 best 12750\nils 3760 best 12750\nils 3762 best 12750\nils 3763 best 12750\nils 3765 best 12750\nils 3771 best 12750\nils 3773 best 12750\nils 3781 best 12750\nils 3782 best 12750\nils 3783 best 12750\nils 3788 best 12750\nils 3796 best 12750\nils 3800 best 12750\nils 3801 best 12750\nils 3802 best 12750\nils 3804 best 12750\nils 3810 best 12750\nils 3812 best 12750\nils 3816 best 12750\nils 3818 best 12750\nils 3820 best 12750\nils 3823 best 12750\nils 3824 best 12750\nils 3828 best 12750\nils 3829 best 12750\nils 3830 best 12750\nils 3834 best 12750\nils 3836 best 12750\nils 3837 best 12750\nils 3840 best 12750\nils 3841 best 12750\nils 3845 best 12750\nils 3847 best 12750\nils 3850 best 12750\nils 3860 best 12750\nils 3861 best 12750\nils 3862 best 12750\nils 3865 best 12750\nils 3867 best 12750\nils 3873 best 12750\nils 3876 best 12750\nils 3878 best 12750\nils 3879 best 12750\nils 3880 best 12750\nils 3888 best 12750\nils 3889 best 12750\nils 3894 best 12750\nils 3895 best 12750\nils 3898 best 12750\nils 3899 best 12750\nils 3901 best 12750\nils 3903 best 12750\nils 3905 best 12750\nils 3906 best 12750\nils 3908 best 12750\nils 3912 best 12750\nils 3916 best 12750\nils 3919 best 12750\nils 3923 best 12750\nils 3928 best 12750\nils 3929 best 12750\nils 3930 best 12750\nils 3932 best 12750\nils 3933 best 12750\nils 3935 best 12750\nils 3938 best 12750\nils 3940 best 12750\nils 3941 best 12750\nils 3946 best 12750\nils 3947 best 12750\nils 3951 best 12750\nils 3957 best 12750\nils 3964 best 12750\nils 3967 best 12750\nils 3971 best 12750\nils 3972 best 12750\nils 3977 best 12750\nils 3978 best 12750\nils 3979 best 12750\nils 3981 best 12750\nils 3986 best 12750\nils 3988 best 12750\nils 3989 best 12750\nils 3991 best 12750\nils 3992 best 12750\nils 3993 best 12750\nils 3994 best 12750\nfinal 12750",
   "vmhwm_bytes": 684032
  },
  {
   "args": [
    "pi2.txt",
    "drift9406_3301.txt",
    "1000",
    "9712",
    "31",
    "drift9712.txt",
    "dump9712"
   ],
   "binary": "np_ils7",
   "charged_peak_bytes": 1007451,
   "image": {
    "bss": 792160,
    "data": 24,
    "image": 815535,
    "text": 23351
   },
   "name": "long plateau drift (pass 15)",
   "outputs": {
    "dump9712/acc_20.txt": "c06833ea87f90cba1cbec2ec91f30f9fd35d7ed701cbef089a3cfc0369c1bdfd"
   },
   "retained_input_output_bytes": 60844,
   "seconds": 1631.2,
   "stack_reserve": 131072,
   "stdout": "start 12750\nils 2 best 12750\nils 4 best 12750\nils 5 best 12750\nils 8 best 12750\nils 11 best 12750\nils 14 best 12750\nils 15 best 12750\nils 19 best 12750\nils 20 best 12750\nils 21 best 12750\nils 22 best 12750\nils 24 best 12750\nils 27 best 12750\nils 30 best 12750\nils 34 best 12750\nils 36 best 12750\nils 37 best 12750\nils 39 best 12750\nils 43 best 12750\nils 46 best 12750\nils 49 best 12750\nils 52 best 12750\nils 53 best 12750\nils 54 best 12750\nils 55 best 12750\nils 57 best 12750\nils 59 best 12750\nils 60 best 12750\nils 64 best 12750\nils 65 best 12750\nils 66 best 12750\nils 68 best 12750\nils 70 best 12750\nils 72 best 12750\nils 74 best 12750\nils 75 best 12750\nils 76 best 12750\nils 79 best 12750\nils 81 best 12750\nils 83 best 12750\nils 85 best 12750\nils 87 best 12750\nils 90 best 12750\nils 92 best 12750\nils 96 best 12750\nils 97 best 12750\nils 98 best 12750\nils 102 best 12750\nils 106 best 12750\nils 108 best 12750\nils 114 best 12750\nils 124 best 12750\nils 125 best 12750\nils 129 best 12750\nils 130 best 12750\nils 132 best 12750\nils 134 best 12750\nils 138 best 12750\nils 143 best 12750\nils 146 best 12750\nils 147 best 12750\nils 149 best 12750\nils 150 best 12750\nils 151 best 12750\nils 152 best 12750\nils 153 best 12750\nils 156 best 12750\nils 158 best 12750\nils 160 best 12750\nils 168 best 12750\nils 169 best 12750\nils 175 best 12750\nils 176 best 12750\nils 177 best 12750\nils 179 best 12750\nils 182 best 12750\nils 191 best 12750\nils 197 best 12750\nils 198 best 12750\nils 201 best 12750\nils 202 best 12750\nils 203 best 12750\nils 208 best 12750\nils 213 best 12750\nils 215 best 12750\nils 216 best 12750\nils 217 best 12750\nils 219 best 12750\nils 221 best 12750\nils 224 best 12750\nils 225 best 12750\nils 228 best 12750\nils 231 best 12750\nils 237 best 12750\nils 240 best 12750\nils 242 best 12750\nils 244 best 12750\nils 248 best 12750\nils 249 best 12750\nils 250 best 12750\nils 252 best 12750\nils 255 best 12750\nils 256 best 12750\nils 257 best 12750\nils 258 best 12750\nils 260 best 12750\nils 264 best 12750\nils 265 best 12750\nils 267 best 12750\nils 268 best 12750\nils 270 best 12750\nils 271 best 12750\nils 274 best 12750\nils 275 best 12750\nils 283 best 12750\nils 288 best 12750\nils 291 best 12750\nils 298 best 12750\nils 305 best 12750\nils 308 best 12750\nils 313 best 12750\nils 316 best 12750\nils 318 best 12750\nils 322 best 12750\nils 324 best 12750\nils 325 best 12750\nils 328 best 12750\nils 331 best 12750\nils 335 best 12750\nils 336 best 12750\nils 339 best 12750\nils 341 best 12750\nils 343 best 12750\nils 344 best 12750\nils 356 best 12750\nils 359 best 12750\nils 365 best 12750\nils 370 best 12750\nils 372 best 12750\nils 374 best 12750\nils 378 best 12750\nils 379 best 12750\nils 380 best 12750\nils 381 best 12750\nils 382 best 12750\nils 385 best 12750\nils 388 best 12750\nils 389 best 12750\nils 398 best 12750\nils 400 best 12750\nils 401 best 12750\nils 402 best 12750\nils 404 best 12750\nils 408 best 12750\nils 410 best 12750\nils 413 best 12750\nils 422 best 12750\nils 423 best 12750\nils 425 best 12750\nils 426 best 12750\nils 429 best 12750\nils 434 best 12750\nils 437 best 12750\nils 440 best 12750\nils 452 best 12750\nils 460 best 12750\nils 465 best 12750\nils 470 best 12750\nils 472 best 12750\nils 477 best 12750\nils 478 best 12750\nils 479 best 12750\nils 482 best 12750\nils 483 best 12750\nils 484 best 12750\nils 485 best 12750\nils 486 best 12750\nils 489 best 12750\nils 491 best 12750\nils 492 best 12750\nils 497 best 12750\nils 498 best 12750\nils 500 best 12750\nils 504 best 12750\nils 505 best 12750\nils 506 best 12750\nils 507 best 12750\nils 509 best 12750\nils 515 best 12750\nils 516 best 12750\nils 517 best 12750\nils 522 best 12750\nils 526 best 12750\nils 527 best 12750\nils 529 best 12750\nils 535 best 12750\nils 538 best 12750\nils 539 best 12750\nils 542 best 12750\nils 544 best 12750\nils 547 best 12750\nils 548 best 12750\nils 551 best 12750\nils 553 best 12750\nils 561 best 12750\nils 564 best 12750\nils 567 best 12750\nils 568 best 12750\nils 570 best 12750\nils 571 best 12750\nils 575 best 12750\nils 579 best 12750\nils 580 best 12750\nils 589 best 12750\nils 590 best 12750\nils 592 best 12750\nils 604 best 12750\nils 605 best 12750\nils 610 best 12750\nils 615 best 12750\nils 625 best 12750\nils 627 best 12750\nils 628 best 12750\nils 629 best 12750\nils 630 best 12750\nils 632 best 12750\nils 633 best 12750\nils 635 best 12750\nils 636 best 12750\nils 638 best 12750\nils 640 best 12750\nils 643 best 12750\nils 645 best 12750\nils 649 best 12750\nils 651 best 12750\nils 657 best 12750\nils 666 best 12750\nils 667 best 12750\nils 670 best 12750\nils 671 best 12750\nils 673 best 12750\nils 676 best 12750\nils 680 best 12750\nils 682 best 12750\nils 685 best 12750\nils 695 best 12750\nils 696 best 12750\nils 698 best 12750\nils 705 best 12750\nils 712 best 12750\nils 713 best 12750\nils 714 best 12750\nils 715 best 12750\nils 716 best 12750\nils 718 best 12750\nils 719 best 12750\nils 724 best 12750\nils 727 best 12750\nils 728 best 12750\nils 729 best 12750\nils 731 best 12750\nils 734 best 12750\nils 735 best 12750\nils 738 best 12750\nils 740 best 12750\nils 742 best 12750\nils 744 best 12750\nils 745 best 12750\nils 746 best 12750\nils 747 best 12750\nils 749 best 12750\nils 750 best 12750\nils 752 best 12750\nils 753 best 12750\nils 756 best 12750\nils 761 best 12750\nils 764 best 12750\nils 766 best 12750\nils 770 best 12750\nils 771 best 12750\nils 774 best 12750\nils 785 best 12750\nils 791 best 12750\nils 792 best 12750\nils 794 best 12750\nils 796 best 12750\nils 804 best 12750\nils 809 best 12750\nils 811 best 12750\nils 816 best 12750\nils 818 best 12750\nils 821 best 12750\nils 823 best 12750\nils 826 best 12750\nils 827 best 12750\nils 829 best 12750\nils 830 best 12750\nils 834 best 12750\nils 837 best 12750\nils 839 best 12750\nils 843 best 12750\nils 847 best 12750\nils 853 best 12750\nils 854 best 12750\nils 856 best 12750\nils 863 best 12750\nils 865 best 12750\nils 872 best 12750\nils 874 best 12750\nils 882 best 12750\nils 884 best 12750\nils 890 best 12750\nils 892 best 12750\nils 897 best 12750\nils 898 best 12750\nils 899 best 12750\nils 903 best 12750\nils 909 best 12750\nils 910 best 12750\nils 913 best 12750\nils 922 best 12750\nils 926 best 12750\nils 930 best 12750\nils 931 best 12750\nils 932 best 12750\nils 933 best 12750\nils 937 best 12750\nils 939 best 12750\nils 946 best 12750\nils 949 best 12750\nils 950 best 12750\nils 951 best 12750\nils 953 best 12750\nils 959 best 12750\nils 961 best 12750\nils 965 best 12750\nils 967 best 12750\nils 968 best 12750\nils 985 best 12750\nils 996 best 12750\nils 997 best 12750\nils 998 best 12750\nfinal 12750",
   "vmhwm_bytes": 684032,
   "wrapper_maxrss_bytes": 1982464
  },
  {
   "args": [
    "specF.txt",
    "step.bin"
   ],
   "binary": "np_emit",
   "charged_peak_bytes": 934966,
   "image": {
    "bss": 685152,
    "data": 16,
    "image": 708007,
    "text": 22839
   },
   "name": "step emission",
   "outputs": {
    "step.bin": "879dbcc6d6c7bddd7db69e2039a0faf8cdb867234d64b234107b94aa41b81340"
   },
   "retained_input_output_bytes": 95887,
   "seconds": 0.01,
   "stack_reserve": 131072,
   "stdout": "operations 25367 bytes 90894 peak 1926 mix 18726 3119 2905 617 ",
   "vmhwm_bytes": 663552,
   "wrapper_maxrss_bytes": 1982464
  },
  {
   "args": [
    "controller.bin",
    "prefilter.bin"
   ],
   "binary": "np_ctl",
   "charged_peak_bytes": 170288,
   "image": {
    "bss": 20512,
    "data": 8,
    "image": 30655,
    "text": 10135
   },
   "name": "controller and prefilter emission",
   "outputs": {
    "controller.bin": "c656b0c5f89238d20788f98274790cf0f755a6ff7ce11addd55bb08ec762fb5e",
    "prefilter.bin": "88ad15d4b5a89d38385fdb42179b15636e53cafe9cc5ed670c5a56b5bb849543"
   },
   "retained_input_output_bytes": 8561,
   "seconds": 0.0,
   "stack_reserve": 131072,
   "stdout": "",
   "vmhwm_bytes": 45056,
   "wrapper_maxrss_bytes": 1978368
  }
 ]
}
```

## Appendix D. Plan

```
nr 6
chained 1
T 1 0605011d081e1a120d0418050308061811180f121d06080c03180c061c0c00010c18131d101206031f0603081d11040800031811030e0c14041103031b0c150c160c0e030c11110a100e0c1a011a1e0410090c0e0b0317180c0c11000a181a030309060c18170c18120e0c10060a1a0f0a1701010f0f011d040c11000b050c1202140b09060f020418031e1711111e1e020e0611061e0e1a0b180603041909061906111e1d0502040c03180c1f03100e08060c030c1f03091102040c02051c110c081b18081a060805140314180c1b0614080806080f18081a100c0d0b101008050306120211081d0c1418101011171b061806031511031706030c110c0b010606060c1805021c0311000f021b06021401010f18150c011815120617050618171e14031817060c180711111501161818021803180f0c06111111020f1203010c
D 1 0000002200000002000400062041020100020200000104222200000001000001050202010004010100020200000410002000000102000300040000002007004102001001202000022006020100002100000501002000020004020002000001002007300000010002200000000000024201000002200021002000000000060000200880008004200000100800120028000000800490002000001040102010000008008000880080048000000440000400880084000200e0102800040020002000200060104400800004004000800004000004800480000000400020004010800020004000040008000008800000000010000082000400f010a0080000880000040100000080008000100080000000010010010200000180200002000200010001000000000100000200000201000080200841010100001000000000128000100000120000000201010020002208000000800000000001ffff8040000000000000004300008000804181008040804182000a020100802180000000804181420002000004002000000000002000410002000002200a000440040200200a00064000200a020002004000000000040000040020000008200a2108200802000000000004022000000800000006000200002008040040040000000000000002440020004100080040002000480600022400000e0008ffff0000ffffffff200800004000500040009000000100080000000901000000c02180000020002048000100480000000000810000018020800000000401400000114000802000084000000180200010500000000001400040008000002000000000c02080200000000105010001c01000011000000181008000400000000100080001008000c020010000008000
T 2 030b0f03031812180303110c03060c1e1818111d0c04061c13000c04180c110c1411050c180c1006180002061111121803031818030c060c11101813030610110103111111100c04001118030304030c110c030218110c140c180a18090301030311180603110304030c0c110603060c031106110c06030603181703030a091806181103061106090c16030f10180c040618051118031818110b1106110c11100c141f110c0c180606040c111803110618060618060306171118061806000c06031818090c101b110b021818180811030604181818061802010c0c1a181111060000110118180c06080611180c060c0818040f0c14060c0203111806180c1818101803060617010c111103060b0b0c04110303060c17061510180d0a06180208110318031f110303110500030603110218101800060c0611030111180c1d0f0c
T 3 0318180c031103161108030301060c030a13180c180d0c190403030c160c0c11180c110601100116001105111818020c040c181818030318060c06090c060c1518060618080606180d0c03110c0c18110306061108060303001b0d1816110c11110c0c1703180c0c111803181515081106050c110318180c060c11110c1110011603040c0318111102060c03060a140603180c1103110306180503030f060311081803110c131d110811181106060806181410020c021018110609060306060c0f0c06181405061111110603181317060611181c110c0b180501040c0c00011a0103180c0306151118010103110c0317060f06030c1803060c1e180c03181b060c0311061b110c041106110c001d06111e110c030c03141818050d100603010306060c03101e110c0608081a060b0a0c0f0c180c0003061118030803070c110d
T 4 0c180011110c03030c1806080b03181818111109031b030c06180c11030301030611030c03111f0c000c0618031f110806060603030318111003030206120c0c0a08081b1111180606020303060c18040003030c1814020303030303180c12060c110603031410060c110f0c0c1d180c03060c1403061103020c1818180303060300030c030a061e0611040c04110a111e03060c1818180416060603181110030c111a031811111809181d0306030a03060318031a18030c0606060c090f12170603121106120310060c0c1811110c060310110c061d110c17081e11001811060c11061b03110606061103061611110c060c17181d11031806180c060c0c061106000c0c0610010c0304180618030c180618050611110c010c03180a0c03180c060305011118031118111103111b180c060303180f0d0c04150c110f0c110311
CN 2 00000000000000000000000000000000002000000000000000000000000000008000000000001802
DN 2 00000000000000000000000000000000000000000000008000000800000000030000000000000000
CN 3 00000000000000000000000000080000000000000000000000000000000000000000100000000000
DN 3 00000000000000002020040000000000000000000000000000000000000000000100000000002000
CN 4 00000000000000800000000000000000000000000008000000000000000000000000200000000000
DN 4 00080000000000000000000000000000000000080000000000000000000000000000000000000000
CN 5 00000000000000000000000000000000000000080000000000000000100000000000000000000000
DN 5 00000000000000000000000000000000000004000000000000000000000000000000000000000000
```

SHA-256 `c06833ea87f90cba1cbec2ec91f30f9fd35d7ed701cbef089a3cfc0369c1bdfd`.
