# SHA3-256 round 6: row-pair embedding, affine round-0/round-1 front and compact checkpoint search

## 1. Claim and resources

This package prices an ordinary distinguished-point birthday search for two distinct 128-byte one-block messages with the same `sha3-256-r6-prefix-v1` digest. It claims no weakness in full SHA3-256 and no reduction in the number of digest evaluations: it is the generic parallel collision search of van Oorschot and Wiener over a fixed injective message family, with a cheaper exact bit-sliced evaluation of the 6-round digest. Under the single score-critical premise H1 in Section 6, one bounded attempt succeeds with probability at least 0.39.

The exact ledger has N = 33893102225923899353969877205805498318795 word operations. One target compression costs C = 1626, so `log2(N/C) = 123.9710039457481967973092371163651576865089929597114901377397100743382423973987753684733361840233804866642436689165073750855771697283025423369631517875330216199490080587094799844572793248880883238523605083010370159276824` and the upward-rounded claim is **123.97101**. Peak memory is 935025 bytes, below 2^20, so `memory_log2_bytes = 20` and the scalar memory term is zero. Preprocessing is 1153085472499881472 word operations (an explicit upper bound, Section 5), i.e. 2^49.33309 target compressions, declared upward as `preprocessing_log2 = 50`. There is no nonuniform advice. Every `*_log2` field in claim.json uses the target-compression unit.

Relative to the current incumbent (the six-lane package, 26521 straight-line operations, claim 124.03079) the only changes in the attack are the message embedding, the straight-line program that evaluates it and the two scalar message-formation routines of the controller (Section 4): the rest of the search controller, table, distinguished-point rule, batch bound Tb, trail capacity U, replay procedure and the whole success certificate are unchanged. The straight line now has 25439 operations, so BSTEP falls from 26540 to 25458 and the claim falls by 0.05978.

## 2. Target and chain function

Write the 256-bit point as four little-endian 64-bit lanes u0..u3 and define the pivot lane

`P(u) = rotl(u0,28) xor rotl(u1,35) xor rotl(u2,4) xor rotl(u3,50)`  (64-bit left rotations).

The one-block message m(u) has 16 lanes in standard Keccak lane order (lane index x+5y). Lanes 0..3 are `K_x xor u_x`, lane 4 is `K_4 xor P(u)`, lanes 10..13 are `K_(10+x) xor u_x`, lane 14 is `K_14 xor P(u)`, and lanes 5..9 and 15 are the constants K_5..K_9, K_15. SHA3 padding of a 128-byte message gives absorbed lane 16 = `8000000000000006`; lanes 17..24 are the zero capacity. The map u -> m(u) is injective because lanes 0..3 return u. Define `g(u) = SHA3-256-r6(m(u)) xor PD`. Equal values of g at different points are equal digests of different messages because the common constant PD cancels.

The 25 absorbed lane constants (lanes 16..24 are padding and capacity) are:

`91b7584a2265b1f5 cd613e30d8f16adf 1027c4d1c386bbc4 1e2feb89414c343c c2ce6f447ed4d57b fffffffffffffffe 7ffffffffffffff9 ffffffffffffffff ffffffffffffffff ffffffffffffffff a3dbc36cebd7dd6e 04d352abfe38d8b3 36ee76bd58a07275 8509223b2dd712f5 ae55498dccb84e5c 0000000000000001 8000000000000006 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000 0000000000000000`

PD is `dddc2cc7fafec3fc 90c3e68829261d02 2223d33885013c02 2220113084012000`; it is the polarity of the emitted digest planes, and both normative emitters derive it again and reject a mismatch.

### 2.1 Why rounds 0 and 1 are cheap

The linear part of the message lives only in rows y=0 and y=2, with lane (x,2) equal to lane (x,0) up to a constant. Write `L_x` for the linear part of lane (x,0) (so `L_4 = P`).

1. **Round-0 theta is constant.** Every column x contains the two variable lanes (x,0) and (x,2) with identical linear parts, so every column parity is constant and theta adds only constants.
2. **Round-0 chi is affine.** pi moves lane (x,y) to row 2x+3y, position y. Lane (x,0) therefore lands at position 0 of row 2x and lane (x,2) at position 2 of row 2x+1 (mod 5). Every chi row has non-constant inputs only at positions 0 and 2. chi multiplies only the pairs of positions (X+1, X+2), and {0,2} is not such a pair, so every round-0 chi output is an affine function of u.
3. **Constants.** Row-1 lanes are set so that position 1 of every round-0 chi row is the constant 0; then output position 0 is `a0 xor a2` and output position 4 is constant. Positions 3 and 4 come from lane 15, the padding lane and the capacity, shifted by the round-0 theta effect D0 of the constants. The constants are solved (Appendix B, `np_consts.c`) so that `D0 = (~1, ~PAD, ~0, ~0, ~0)`; this target has even total parity, as every theta effect must. It makes every position-3 input equal to one and every position-4 input equal to one except at four (row, bit) positions (one bit of row 2 and the three set bits of PAD in row 4). Output position 1 is then a complemented copy of position 2, output position 2 equals position 2, output position 4 is constant, and output position 3 is constant except at those four positions, where it is a complemented copy of position 0 (`1 xor a0`).
4. **Round-1 theta is half constant.** The round-1 column parity of column 2 is `C1[2](w) = xor_x L_x[w - r(x,2)]` plus a constant, with rotation offsets r(x,2) = 3, 10, 43, 25, 39. The pivot lane `L_4 = P` is exactly the solution of `C1[2] = const` (it sets `L_4[z] = xor_(x<4) L_x[z + 39 - r(x,2)]`), so C1[2] is constant, and C1[1] (the complemented copies) is constant as well. Column 0 carries `a0 xor a2` and its parity C1[0] is non-constant. Column 3 has non-constant parity only at the four exceptional bits. Consequently the round-1 theta effects D1[0] and D1[3] are constant, D1[2] is constant except at those few bits, D1[1] = C1[0] and D1[4] = C1[3] xor rotl(C1[0],1) are non-constant, and after round-1 theta column 3 is constant except at four bits. pi maps column 3 to one position of every round-1 chi row, so almost every round-1 row has a constant input and needs at most three AND/OR gates instead of five. The four exceptional bits fall in four distinct rows (row 2 bit 43 and row 3 bits 57, 59, 60 of the round-1 chi layer), which keep five gates: `316*3 + 4*5 = 968`.

The emitted round-0/round-1 segment has 968 AND/OR gates (a 39.5% cut, not a halving) (the six-lane incumbent has 1600) and 3293 operations in total (incumbent 4280). These structural statements are explanatory only: the emitter tracks every affine form exactly (Section 3), and the executed checks of Section 7 compare the emitted program bit for bit with scalar SHA3-256-r6 of m(u).

## 3. Bit-sliced register step

One 256-bit register word carries one bit plane for 256 walks. Inputs are the 256 planes of u in registers 0..255; outputs are the 256 digest planes in the same registers.

**Front segment (rounds 0 and 1).** The emitter starts from 256 affine input planes and builds the 64 pivot planes as three XORs each. Every value is a pair (node, polarity); an XOR of two affine nodes is first looked up by its exact 256-bit linear form, so identical forms are shared and constant results fold away. A complemented copy costs nothing because only the polarity bit changes. Round-0 chi uses the generic exact row builder (`_row_choice`): every round-0 row is affine and costs only the XORs its linear terms need.

**Chained-chi rows and the polarity plan.** Rounds 1 to 4 build every row whose five inputs are distinct non-constant nodes with the exhaustively verified 1024-entry chained-chi table (checksum c8fa4bd9170966dc): for an input polarity pattern p and a chosen output polarity target t it gives the cheapest complement subset, chaining order and mixed-term selection, with 10 to 15 operations. Round-1 rows with exactly one constant input (316 of the 320 rows, Section 2.1) are built from a second exhaustive table: for each of the 160 row types (constant position, constant value, polarities of the four variable inputs) and each of the 32 output-polarity targets, the cheapest chained-row decision (complement subset, chaining order, mixed-term selection), found by emitting all 15872 decisions of each type on a scratch graph and counting live operations (np_emit record mode; ties broken as in the chained table). The plan stores the chosen decision of each such row explicitly (line `D 1`), so the Python emitter needs no table. Round 0 and any remaining row use the generic exact row builder. The plan also fixes the target t of every full row in rounds 1..4 and optional complement bits on the theta column parities (CN) and theta effects (DN) of rounds 2..5. It was found by the bounded staged simulated-annealing planner `np_plan.c` (seed 22, next-round weight 6/16, T0 = 2; pass 1 with 100000000 moves per stage over all rounds, pass 2 with 250000000 moves per stage over rounds 2..5; each pass ends with exact coordinate descent). Pass 1 plans round-1 targets with the table costs; because a linear output of a round-1 row may coincide with an affine form that already exists in the graph with a different constant, its realized polarity can differ from the scratch-graph target, so pass 2 re-records the actual round-1 output polarities under the pass-1 decisions and re-plans rounds 2..5 with round 1 fixed. The pass-2 model cost (its final printed value, 10626) counts the full rows of rounds 2..4 (table cost), the 64 last-round rows (generic last-round row cost) and the CN/DN NOTs; adding the fixed theta XORs of rounds 2..5 (`3*3200 + 1920`) and the emitted round-0/1 segment gives exactly the emitted 25439 operations. The plan text is in Appendix D, SHA-256 `2d719b3d3276fafa6af44671e6203d98ba2c66a97310bd9c2f9a3d58781f3641`.

**Last round.** Only the four digest lanes of row 0 are formed.

| segment | XOR | AND | OR | NOT | total |
|---|---:|---:|---:|---:|---:|
| rounds 0-1 (front) | 2122 | 483 | 485 | 203 | 3293 |
| round 2 | 4810 | 798 | 802 | 162 | 6572 |
| round 3 | 4810 | 810 | 790 | 175 | 6585 |
| round 4 | 4806 | 801 | 799 | 150 | 6556 |
| round 5 (four digest lanes) | 2176 | 139 | 117 | 1 | 2433 |
| **straight line** | 18724 | 3031 | 2993 | 691 | **25439** |

The emitted straight-line register program has 25439 operations. Lowest-free last-use allocation names registers 0..1931 (peak 1932). It contains 343 14-bit, 16346 25-bit and 8750 36-bit encoded records, 16341 with destination equal to the first operand. Its stored size is 91057 bytes and SHA-256 is `c2d52e3ed730f2bc8e7acdaa80fd05fd246ff5aadc20de6faeb9939450a38847`.

### 3.1 Registers and code encoding (machine conventions H_reg and H_code)

These conventions are unchanged from the incumbent package; only the measured numbers differ.

**Registers.** Input and digest plane j use register j. Each other value receives the lowest free register allowed by its last use. Values in registers above 255 are dead between steps and may be reused by handlers. The straight line uses registers 0 through 1931; persistent search state begins at register 1932. The declared file has 1943 words, or 62176 bytes, all included in Section 5.

**H_reg (declared machine convention, role supporting in claim.json).** The cost model and target profile fix no register count. This package uses the 256-bit word RAM of collision-frontier-v5 with the declared register file above. An operation on register operands costs one word operation, with no load or store. Every load and store in the assembled other code is an explicit charged word operation. H_reg affects the time and memory ledgers, not the success bound.

**Sensitivity of H_reg (quantified).** Every emitted straight-line and prefilter record reads at most two register operands and writes one. Every non-PERM controller word has at most two semantic register reads and one write; PERM reads and rewrites seven packed state words, 14 accesses, below 3C. Charging each register access as a separate load or store makes every ordinary instruction cost at most 4 word operations and every PERM at most 4C. Applying the same factor to preprocessing gives `N_RAM <= 4N`, hence `time_log2_RAM <= 125.9710039457481967973092371163651576865089929597114901377397100743382423973987753684733361840233804866642436689165073750855771697283025423369631517875330216199490080587094799844572793248880883238523605083010370159276824`, exactly 2 above the claimed model, with memory unchanged.

**H_code (declared code-memory charging convention, role supporting in claim.json).** Each straight-line instruction has register operands only. Bits 0..1 give XOR, AND, OR or NOT and bit 2 flags destination equal to the first operand. With that flag, NOT carries one 11-bit register and a binary operation carries two; without it, NOT carries destination and source while a binary operation carries destination and two sources. Commutative operations swap operands when the destination equals the second. Records are packed without padding in a little-endian bit stream: 91057 bytes. The separate prefilter is a 15-OR chain from digest planes 240..255 into register 1936 (49 bytes, SHA-256 `88ad15d4b5a89d38385fdb42179b15636e53cafe9cc5ed670c5a56b5bb849543`). The other code (setup, loop control, handlers, restart, replay and output) is 1016 fixed 8-byte instruction words followed by 12 32-byte literal words, 8512 bytes, SHA-256 `c656b0c5f89238d20788f98274790cf0f755a6ff7ce11addd55bb08ec762fb5e`. A word has a 5-bit opcode, one literal flag, three 11-bit register fields and a 25-bit immediate or literal index. Each assembled operation is charged as the word operation it performs, except PERM at C.

## 4. Search, table, and controller

The search is the incumbent's compact checkpoint search, byte for byte except the two scalar message-formation routines. The attempt starts 256 walks from `rho + trail_number`. It advances all walks through the step, applies the 15-OR prefilter, and handles exact distinguished points with probability `712 * 2^-121`. The table has 18600 256-bit words and 93000 slots; each word has five 51-bit slots (written bit and 50 endpoint bits) and the word and slot position encode the trail number. The 256 live walks use one packed word apiece: low 128 bits are the start step and high 128 bits are the positional trail number.

On a prefilter hit the 125-operation hit handler forms the exact distinguished-point mask and continues the batch loop when it is zero. Only when it is nonzero do 256 stores copy the carried planes to a scratch matrix, charged indexed loops gather or replace one lane per distinguished point, and 256 fixed loads restore the planes; that cost is part of the 2893-operation per-DP handler. A matching endpoint starts the final replay. Replay measures the stored trail while keeping every `G = ceil(LRC/(S-1)) = 2107889139913890569390211303440`-th point in the now-free table, advances the other trail to alignment, locates the merge segment by checkpoints, then lock-steps only that segment.

**Scalar evaluation.** Replay evaluates g with the scalar routine `eval_f`: seven loads of the constant state words, then `state0 ^= u` (lanes 0..3), extraction of u0..u3 (six operations), the pivot `P` by four rotations of three operations each, three XORs and one 64-bit mask, `state1 ^= P` (lane 4), `state2 ^= u << 128` (lanes 10, 11), `state3 ^= u >> 128` (lanes 12, 13) and `state3 ^= P << 128` (lane 14), then PERM, a load of PD and one XOR. Its charged cost is `e = C + 40 = 1666` (the incumbent's six-lane routine cost C + 29). `output_message` is the same message formation plus a return (38 operations).

With `e = 1666`, at most one replay costs `(2e+17)LRC + (3e+20)G + 17*nck + e + 93 = 131306883637006639297473720649711215510` operations, where LRC = 39204630113258450700088540032663552 and nck = S-1 = 18599.

The controller permits at most HMAX = 44384159803516906822519431956004865 prefilter hits and aborts on hit 44384159803516906822519431956004866; that abort value is a checked controller literal and the input to F5 below. Setup initializes `remaining = Tb = 1325958336173754933667940744388673536`. Every continuation path executes `remaining -= 1`, branches to the step only while the result is nonzero, and otherwise reaches HALT. The exact-byte experiment starts `remaining` at three, supplies only no-DP prefilter results, requires exactly two back-edges, and then requires the charged-limit HALT.

## 5. Exact operation and memory ledgers

`BSTEP = 25439 + 15 + 2 + 2 = 25458`: the straight line, the prefilter ORs, its compare and branch, and the count-down subtract and conditional back-edge.

| term | word operations |
|---|---:|
| main work `Tb * BSTEP` | 33756247322311453101318435470646850879488 |
| one replay (Section 4) | 131306883637006639297473720649711215510 |
| hit, DP, probe, restart, setup, cap and final-halt paths | 5548019975439613352814929036436342325 |
| preprocessing (upper bound, below) | 1153085472499881472 |
| **N** | **33893102225923899353969877205805498318795** |

The path term is the incumbent's carried bound for these paths, `5548019975439613352814929036434245173`, plus an explicit allowance of `2^21`. The carried bound decomposes as `125*HIT_ABORT + 92744*(2893 + 2835 + 24*18600) + 1477691`: at most HIT_ABORT = 44384159803516906822519431956004866 hits at 125 operations each (the hit handler), at most U-256 = 92744 handled distinguished points each charged the per-DP handler (2893: save, ctz, gather, record, insert, restore), one restart (2835) and a full linear probe of all 18600 table words (24 operations per word), and a remainder of 1477691 covering setup (750162) and the final match, halt and output paths. All of these paths are byte-identical to the incumbent's controller; the only one that touches message formation is the final output, which calls `output_message` twice and therefore costs 22 more operations than before, far below the allowance.

**Preprocessing.** The attack's construction consists exactly of the five bounded freestanding C phases of Appendix B, run alone and sequentially under an address-space cap of 1048576 bytes; their inputs are the closed-form rules of Section 2.1 (the D0 target, the fixed row-0 constants) and their own outputs. Their measured running time is 1404.2 s in total, essentially all of it the two planner passes. The ledger charges `2^60` word operations for these phases: a deliberately generous bound (a 2^36 operations-per-second rate would need more than 2^24 seconds). Design-time experiments that led to choosing the embedding rule are analysis, not phases of the attack: none of their outputs is an input to it, since the constants follow from the stated rule via `np_consts` and the plan from `np_plan`. The ledger also keeps the incumbent's inherited campaign charge `163967893034496`, which covers the construction of the chained-chi table and the controller design used here (that campaign ran under the same 1 MiB cap). Total `1153085472499881472` word operations, `log2(prep/C) = 49.333094`, declared as `preprocessing_log2 = 50`. This bound changes N only in its twenty-third significant digit.

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
| step program (H_code) | 91057 |
| table | 595200 |
| transpose scratch | 8192 |
| **search total** | **773890** |

The online controller uses link registers and zero stack. Replay checkpoints alias the table after a match, when the ordinary endpoint table is no longer needed.

**Construction memory.** Each phase ran alone under `prlimit --as=1048576 --stack=131072`. The charged peak is `max(VmHWM, image + stack reserve) + retained input/output bytes`, with VmHWM read by the program itself from `/proc/self/status` at exit. Appendix C also lists `wrapper_maxrss_bytes`, the peak of the measuring wrapper (`/usr/bin/time` around `prlimit`, before `exec`); it is outside the charged process and is not part of the attack.

| sequential construction phase | image bytes | stack reserve | measured VmHWM | retained input/output | charged peak | seconds |
|---|---:|---:|---:|---:|---:|---:|
| lane constants | 38799 | 131072 | 36864 | 425 | 170296 | 0.00 |
| round-1 record and one-constant row table | 707903 | 131072 | 397312 | 55412 | 894387 | 0.37 |
| polarity planner, pass 1 (all rounds) | 322307 | 131072 | 294912 | 56272 | 509651 | 463.41 |
| round-1 record under the pass-1 plan | 707903 | 131072 | 397312 | 56697 | 895672 | 0.37 |
| polarity planner, pass 2 (rounds 2-5, round 1 fixed) | 322307 | 131072 | 294912 | 60840 | 514219 | 940.07 |
| step emission | 707903 | 131072 | 655360 | 96050 | 935025 | 0.02 |
| controller and prefilter emission | 30903 | 131072 | 40960 | 8561 | 170536 | 0.00 |

Construction peaks at 935025 bytes and search at 773890 bytes. The claimed peak is their maximum, **935025 bytes**, below 2^20.

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

As reduced-scale evidence (not an organizer experiment), the scalar chain g of this package was evaluated on 2^20 inputs in each of three families, counting colliding pairs in three 32-bit output windows (bits 0..31, 112..143, 224..255; 128 pairs expected per window): uniform random u: 130, 120, 119 pairs; u varying only in u0: 126, 120, 132; distinct weight-3 points: 122, 121, 119. Every count is within one standard deviation of a random function, including for points that vary only in u0 and for distinct weight-3 points, where an affine front would be most likely to show structure. This tests consistency only; it does not reach birthday scale.

## 7. Organizer experiments

`experiments/compact.py` contains compressed source text, not prebuilt program bytes. It runs the normative Python step emitter (an independent implementation of the same construction as `np_emit.c`; both produce the SHA-256 above) on the stated constants and plan, checks operation count, register peak, byte length and hash, and checks that the step's register peak does not reach the controller's persistent registers. It re-derives the 1024-entry chained-chi table with its exhaustive 32-input truth check and checksum. It parses the exact emitted stream and executes two chained bit-sliced steps on eight lanes against scalar SHA3-256-r6 of m(u) (`message_for` in the support module implements Section 2 independently of the emitter). It assembles the controller, checks its size, hash and literal pool, runs `eval_f` against the scalar chain on four full-width points, and exercises gather/setwalk, restart packing, every slot probe position, replay success, replay refusal and the all-no-DP charged-limit halt, plus every field boundary of both encodings. The `success-certificate` experiment additionally recomputes Appendix A at 200-digit precision and checks the plan binding. Each response row returns the projected 12-bit pair derived from the first request seed when one exists among 68 points, otherwise the failed-trial null pair.

Local runs of both experiment ids and `--self-test` passed; both bounded C emitters reproduce the same step bytes as the Python emitter.

## 8. Credit

This package builds directly on the promoted incumbent `f9b654c6-23d2-4df5-9e7b-803c46b43553` (0xplemonade): its search controller, table layout, replay procedure, success certificate and Section 6 analysis are reused unchanged, and its lineage credits `20eb70ca-366a-4fbd-9594-4fa85f158a0b` (one-round-lookahead generator, lowest-free allocation, two-address encoding, positional five-slot table, one-word walk, checkpoint replay), `d258ba65-054d-4098-bbac-0b974fee36c8` (chained-chi identity and table), `3509abf0-ecab-457b-8d5d-ea8aec5d5e8c` and `911bffce-8e7a-4502-90ab-c69a473fff48`. New here: the row-pair embedding with the C1[2] pivot lane (Section 2.1), the staged polarity planner, and the bounded freestanding construction of Appendix B. No participant executable was used; all programs in Appendix B were written for this package. Credit is not endorsement.

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
 "plan_sha256": "2d719b3d3276fafa6af44671e6203d98ba2c66a97310bd9c2f9a3d58781f3641",
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

Build: `gcc -O2 -mpopcnt -static -nostdlib -ffreestanding -fno-stack-protector -fno-builtin -fno-pie -no-pie`. Phases: `np_consts constants.txt`; `np_emit record spec_zero.txt plan_input.txt` (constants plus an all-zero plan; also builds the one-constant row table); `np_plan plan_input.txt 100000000 2 22 6 plan1.txt`; `np_emit record spec1.txt plan_input2.txt` (constants plus the pass-1 plan); `np_plan plan_input2.txt 250000000 2 22 6 plan.txt plan1.txt` (pass 2, copying the round-1 lines of the pass-1 plan); `np_emit emit spec.txt step.bin` (constants plus the final plan); `np_ctl controller.bin prefilter.bin`.

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
 * complete the column parities C0 that produce D0.  usage: np_consts <out> */
#include "rt.h"
static const uint64_t PAD = 0x8000000000000006UL;
static const uint64_t K0[5] = {0x91b7584a2265b1f5UL, 0xcd613e30d8f16adfUL, 0x1027c4d1c386bbc4UL, 0x1e2feb89414c343cUL, 0xc2ce6f447ed4d57bUL};
typedef struct { uint64_t m[5]; int v; int used; } Row;
static Row piv[320];
static int top(const uint64_t m[5]) { for (int w = 4; w >= 0; w--) if (m[w]) return 64 * w + 63 - __builtin_clzl(m[w]); return -1; }
static uint64_t rotl(uint64_t v, int k) { k &= 63; return k ? (v << k) | (v >> (64 - k)) : v; }
int main(int argc, char **argv) {
  if (argc != 2) fail("usage");
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
static int scratch_mode; static uint16_t touched[256]; static int ntouched;
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
static int record_mode;
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
  if (argc != 4) fail("usage: np_emit record|emit spec out");
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
 "peak_bytes": 935025,
 "phases": [
  {
   "args": [
    "constants.txt"
   ],
   "binary": "np_consts",
   "charged_peak_bytes": 170296,
   "image": {
    "bss": 35872,
    "data": 8,
    "image": 38799,
    "text": 2919
   },
   "name": "lane constants",
   "outputs": {
    "constants.txt": "4ef3a563babaec32308727a7efe7598da959a3f054aebc8ef99384c6c5f37d88"
   },
   "retained_input_output_bytes": 425,
   "seconds": 0.0,
   "stack_reserve": 131072,
   "stdout": "",
   "vmhwm_bytes": 36864,
   "wrapper_maxrss_bytes": 2252800
  },
  {
   "args": [
    "record",
    "spec_zero.txt",
    "plan_input.txt"
   ],
   "binary": "np_emit",
   "charged_peak_bytes": 894387,
   "image": {
    "bss": 684544,
    "data": 16,
    "image": 707903,
    "text": 23343
   },
   "name": "round-1 record and one-constant row table",
   "outputs": {
    "plan_input.txt": "f7215edc414a6f7bdc4bd3820b650dee42cd18b51c946a1f2d3afceacfffb00e"
   },
   "retained_input_output_bytes": 55412,
   "seconds": 0.37,
   "stack_reserve": 131072,
   "stdout": "",
   "vmhwm_bytes": 397312,
   "wrapper_maxrss_bytes": 2170880
  },
  {
   "args": [
    "plan_input.txt",
    "100000000",
    "2",
    "22",
    "6",
    "plan1.txt"
   ],
   "binary": "np_plan",
   "charged_peak_bytes": 509651,
   "image": {
    "bss": 310144,
    "data": 32,
    "image": 322307,
    "text": 12131
   },
   "name": "polarity planner, pass 1 (all rounds)",
   "outputs": {
    "plan1.txt": "3d0cda6b1a925cbe64b4153a175d17128e1d5183f2220805353d98d3d265503c"
   },
   "retained_input_output_bytes": 56272,
   "seconds": 463.41,
   "stack_reserve": 131072,
   "stdout": "stage 1 exact-total 13551\nstage 2 exact-total 13424\nstage 3 exact-total 12880\nstage 4 exact-total 12812\nstage 5 exact-total 12812\nfinal 12812",
   "vmhwm_bytes": 294912,
   "wrapper_maxrss_bytes": 2252800
  },
  {
   "args": [
    "record",
    "spec1.txt",
    "plan_input2.txt"
   ],
   "binary": "np_emit",
   "charged_peak_bytes": 895672,
   "image": {
    "bss": 684544,
    "data": 16,
    "image": 707903,
    "text": 23343
   },
   "name": "round-1 record under the pass-1 plan",
   "outputs": {
    "plan_input2.txt": "2a121aaa398dcdf7349ddc1f02c5413248c523fa439ea91ab47144c03169340b"
   },
   "retained_input_output_bytes": 56697,
   "seconds": 0.37,
   "stack_reserve": 131072,
   "stdout": "",
   "vmhwm_bytes": 397312,
   "wrapper_maxrss_bytes": 2252800
  },
  {
   "args": [
    "plan_input2.txt",
    "250000000",
    "2",
    "22",
    "6",
    "plan.txt",
    "plan1.txt"
   ],
   "binary": "np_plan",
   "charged_peak_bytes": 514219,
   "image": {
    "bss": 310144,
    "data": 32,
    "image": 322307,
    "text": 12131
   },
   "name": "polarity planner, pass 2 (rounds 2-5, round 1 fixed)",
   "outputs": {
    "plan.txt": "2d719b3d3276fafa6af44671e6203d98ba2c66a97310bd9c2f9a3d58781f3641"
   },
   "retained_input_output_bytes": 60840,
   "seconds": 940.07,
   "stack_reserve": 131072,
   "stdout": "stage 1 exact-total 11124\nstage 2 exact-total 11210\nstage 3 exact-total 10699\nstage 4 exact-total 10626\nstage 5 exact-total 10626\nfinal 10626",
   "vmhwm_bytes": 294912,
   "wrapper_maxrss_bytes": 2252800
  },
  {
   "args": [
    "emit",
    "spec.txt",
    "step.bin"
   ],
   "binary": "np_emit",
   "charged_peak_bytes": 935025,
   "image": {
    "bss": 684544,
    "data": 16,
    "image": 707903,
    "text": 23343
   },
   "name": "step emission",
   "outputs": {
    "step.bin": "c2d52e3ed730f2bc8e7acdaa80fd05fd246ff5aadc20de6faeb9939450a38847"
   },
   "retained_input_output_bytes": 96050,
   "seconds": 0.02,
   "stack_reserve": 131072,
   "stdout": "operations 25439 bytes 91057 peak 1932 mix 18724 3031 2993 691",
   "vmhwm_bytes": 655360,
   "wrapper_maxrss_bytes": 2252800
  },
  {
   "args": [
    "controller.bin",
    "prefilter.bin"
   ],
   "binary": "np_ctl",
   "charged_peak_bytes": 170536,
   "image": {
    "bss": 20512,
    "data": 8,
    "image": 30903,
    "text": 10383
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
   "vmhwm_bytes": 40960,
   "wrapper_maxrss_bytes": 2170880
  }
 ]
}
```

## Appendix D. Plan

```
nr 6
chained 1
T 1 0b11041806110f03110c160c1f1d11040c110c060e06030c1e061219100612130f00030a180a160c061a100306150206120e00161d01061d1211080c1317030f0110011011170a060a0301180911180a1b0a1113091b031b16060601011f0a0d1105020c0f0613010b17170f1b1818111417181118181e03010b18040f031f1804091e0606090d031a09150b18030a03110f091e1809181e0c030a1816180f041117181112040a001e18180903111d06181a0903070b1708160d091e09061103120c031e0c11100c1814180b0c111e10180c040c11001511060f171405010b1e031b03180b031c0516181b05030301061b16061714030b060c110b021418000c0c110f18110f0f1b110d111301121410110c0c070116181803171103091b111101061403090911110d0603121b0f120214060c1a03170f030217100910180214
D 1 00000102000000010000000200412200000200000001010000050102000210000000000204000400000001002100000000060000000120052006010002012020000420072000204001010007000114000000204120060004010000000000040002010000200700060402000000000002010104020000000020200005210000416008000060080800040040002800400028002000000010006010000060102400401020000400000080084010240040104010500044000000001020102400200800000400c01082000008440000000000a0084000200880004010040000000000400440000800020000000000201000040000a0086010000080000004201000000200800002010100000080008022824100418000000000410001000000400000000280008100000108018200080100109000110000100001001102010041000010028020000110020011000000108043000101010801ffff010000020002010000010000800000008010004100400043000100028000100180000000080200000000020000040008200a02020200200a0200200a08000006200a04020006000804000800000000000002600a400608024200000a4000200a020208400006000828002000200008000006000400000002000004002400000220002000000040002400000041000004200a2800000640000800ffff2008ffffffff0800600a200a8100c02040101001c02088009000401008004010000000000000c0204000000000008400800000000000000108010001040040000100000080084010c020000000000008400000008008800808000800401040000000c02040100008001114004800410081000100000080208000010000008020000080000000080100005000
T 2 1803080c111118180305030311110c0618021f06060b0411060c13110c11100608181803180c0c1106180c08050c041011171117060c0c001c0c1118061a181118041803030c0a19030611161718030a180c111e06181a060304180605181111061808120c1d07180813060318180c0311060c1d0c1103060c060600080c03180606110c0c06181118150f171400110811110003180601180c0c010c0c180c110c031818061111080c03060c06031804100c0603110c080c1e060a180c040101110c0f11180c18060018110600180c180403090c181703111d0806060c06030c0c0310180c000c180f06180c1106111e0c0c120c010c060c060c0618110617031806111409061a180206180810180c0203180c06011e03150406030c0c030c111114180203011a081812180c180c11040a111d0306100c0b110c1e180c0c0303
T 3 110b061918030610041801110c06000618031011061a03060601010315111108061118060e0106040404091106180218061818051e180d1103181106100c1117171b18180c0c0c0318030c1503030c181403060c06030c180c040c18151818030118111811030c1b09091111051803060811180c11110c1f030303010f18060c0d0c060c06060c180301180c1a0312180f1e181711110c06180c181b1114011711060017181006010c18100306030c03030c060d081f1106181118041403111101060c080c08110c030606180a03030f031b0204110f1d1e03181d0c18170c02060306180206110c07110c1801180c03180f0217031818031814001809031d0301000c03061818180b111806030a0611181103110c1811110603030c0c18060c061706010d0c0c180603090311180611150603110c0c1c030c110c0306181111
T 4 030c110c040906030608030c18111803031801030c051106090311061e11060f11170c0c06181b0605060c180c16100c0111061503060c0303181118060310110d11000c1803181811180c11060618060c0318011e1812061801061a030c030c0804110c060c06030206110c061d040c061b0617180310110c1f031811031818110c030c060308030c06181101020c110906180618060c0f0c05120c1003120c03060610040a0606180c0c1106041803111d03050a0c08110c031108181811060516060603110c181d0c0c0411030311061111041806031e0c01111e060a0c181012030214181b020306110c111103061806030c10030b0c01031803030c04101108060c03060c18111117031806030408111818010c06040c10001e0c0c110617060c1111181818180c060c0c0c1118181d12060c1114181d030c1e15180606
CN 2 00000000000000000000000000000000000000000010000000000000000000000000000000000000
DN 2 00000000000000000000002000000000000000000000000000000000000000000000400000000000
CN 3 00000000000000000000000000000000100000000000000000000000000000000000000000000000
DN 3 00000000000000000000000000000000000000000000000000000000000000000000000000000000
CN 4 20000000000000000000000020000000000000800000000000000000000000000000000000000000
DN 4 80000000000000008000000000000400000000000000000000000000000000000000000000000000
CN 5 00000000000000000000000000000000000000000000000000000000000000000000000000000000
DN 5 00000000000000000000000000000000000000000000000000000000000000000000000000000000
```
