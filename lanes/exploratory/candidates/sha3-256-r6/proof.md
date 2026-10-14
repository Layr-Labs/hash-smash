# sha3-256-r6: bit-sliced distinguished-point collision search, time_log2 124.46633, memory below 2^20 bytes

## 1. Claim

- Target: sha3-256-r6-prefix-v1, an ordinary collision of the complete 256-bit digest (zero state, rate 136 bytes, suffix 0x06 with pad10*1, Keccak-f[1600] rounds 0 to 5 in the single permutation call).
- Output: two distinct 32-byte messages with equal digests.
- Time: at most N = 47,776,754,250,108,289,885,528,736,753,876,813,425,013 word operations, that is N / 1626 target compressions, time_log2 = 124.46633 (Section 6, integer certificate in 6.3).
- Memory: at most 1,048,576 bytes including code, registers, the table and all working state, memory_log2_bytes = 20 (Section 4.3).
- Score under hashsmash-scalar-tm-v1: 124.46633 + max(0, 20 - 20) = 124.46633.
- Success probability: at least 0.3905 for one attempt, over the algorithm's fresh coins, under the declared premise H_rand (Section 7). No amplification, no preprocessing beyond the generation of the code (Section 6), no advice.
- Machine convention: a 256-bit word RAM with a declared file of 2,304 registers, whose bytes are counted as memory (premise H_reg, Section 4.1). Smaller files are priced in Section 10.
- The required `baseline_improved` identifier names the organizer's nominal entry sha3-256-r6-nominal-v2. It is a nominal reference, not an established attack or baseline; nothing here depends on it.

## 2. Messages and the chain function

- A point is a 256-bit value x. Its message is m(x) = LE32(x), the 32 little-endian bytes of x, zero bytes included. m is injective, every message has bit length 256 < 2^64, and two different points give two different messages.
- With SHA3 padding the padded input is m(x) || 06 || 00 (102 times) || 80, exactly one 136-byte rate block. The sponge absorbs it into the all-zero state and applies one permutation (rounds 0 to 5); the digest is the first 32 bytes of the state, since 32 < 136.
- Lanes after absorption (lane index x + 5y, little-endian 64-bit lanes): A[0..3] are the four 64-bit words of x, A[4] = 0x06, A[16] = 2^63, all other lanes are 0.
- The chain function is f(x) = the digest of m(x), read as a little-endian 256-bit value. The digest is the first four lanes after the permutation, so digest bit j is bit j mod 64 of lane j div 64.
- If x != x' and f(x) = f(x'), then m(x) and m(x') are distinct messages with equal complete digests: an ordinary collision of the target.

## 3. The bit-sliced chain step

### 3.1 Representation

- A batch is 256 trails. Plane (lane, z) is one 256-bit word whose bit t is bit z of that lane for trail t. The 256 input planes are bits 0..255 of the current points; the 256 digest planes are the next points.
- A rotation of a lane renames planes and costs nothing. A plane that is the same constant for every trail is folded and never stored.
- NOT is folded into a polarity: every plane is held physically as its logical value XOR a known bit p (p = 1 means complemented). XOR with a constant flips p; a NOT flips p.

### 3.2 Gates

The program has four operations on registers, each one word operation: XOR, AND, OR, NOT. For logical a = A xor pa and b = B xor pb (A, B the physical words):

- a XOR b = (A XOR B) xor (pa xor pb): one XOR.
- a AND b: one AND if pa = pb = 0; one OR with output polarity 1 if pa = pb = 1 (NOT A AND NOT B = NOT (A OR B)); two operations otherwise (A AND NOT B = A XOR (A AND B)).
- Constants are folded: a AND 0 = 0, a AND 1 = a, a XOR c flips the polarity; equal operands are folded (a XOR a = 0, a AND a = a, a AND NOT a = 0).
- Every binary operation on the same pair of physical words is emitted once.

### 3.3 Rounds

For each of the six rounds, with the round constants of the profile:

1. theta parity: for each column x and bit z, the parity of the five planes of the column (folded constants, otherwise XOR).
2. D[x][z] = parity[x-1][z] XOR parity[x+1][z-1].
3. rho and pi are renaming. Each chi row (five planes of one row y and one bit z after pi) takes its five inputs A[i][z'] XOR D[i mod 5][z'] at the moment the row is computed, so a theta output exists only while its row is open.
4. chi: out[x] = b[x] XOR ((NOT b[x+1]) AND b[x+2]). The term (NOT b[x+1]) AND b[x+2] costs one operation when the two polarities differ and two when they are equal. Before a row is computed, the generator may complement some of its five planes (one NOT each); it takes the subset of the 32 that minimizes NOTs plus two-operation terms, and the empty subset on ties. This is the lane complementing transform of the Keccak reference code applied plane by plane: a row costs 5 XOR + 5 AND/OR + at least one extra operation, since in a five-cycle the number of equal adjacent polarities is odd.
5. iota flips the polarity of the planes of lane 0 whose round-constant bit is 1 (free).

In the last round only the four digest lanes are needed: only row y = 0 and only outputs x = 0..3 are computed. Instructions that no digest plane depends on are removed (dead-code elimination).

### 3.4 Chain feed and input polarity

The digest planes become the input planes of the next step with no copy: digest plane j is written into register j, which held input plane j. The program is generated for one fixed input polarity P (one bit per input plane). If a digest plane's polarity differs from P[j], one NOT writes it into register j. P is chosen as the cheapest of eight candidates P0 = 0, P(k+1) = digest polarity of the program generated for Pk; the program is deterministic.

### 3.5 Registers

Input plane j and digest plane j live in register j (j < 256). The remaining values are allocated to registers 256 to 2,303 in program order: a register is freed after the last use of its value. The allocation never exceeds 2,304 registers (the generator stops otherwise); the peak is exactly 2,304. The main loop has no loads or stores.

### 3.6 Ledger of one step

The generator is the program experiments/sha3r6_rho.py (`--ledger`). One step of 256 trails is:

| operation | count |
| --- | ---: |
| XOR | 25,074 |
| AND | 4,953 |
| OR | 3,303 |
| NOT | 1,257 |
| **total** | **34,587** |

That is 135.11 word operations per evaluation of f, against the reference cost 1626 of one permutation: 0.08310 target compressions per evaluation.

### 3.7 Correctness of the step

- `--selftest 512` executes the generated straight line on 512 uniform messages and four chained steps each, against an independent plain implementation of the six rounds in the same file, which matches the organizer reference verifier/keccak.py sha3_256(m, rounds=6) on random messages. Result: 0 differences in 2,048 chained evaluations.
- The organizer experiment proj-w256 (Section 9) runs the same straight line at full width for eight chained steps from random planes; every returned pair is recomputed by the organizer's trusted digest, so a wrong step would show as failed pairs.

## 4. Machine convention and memory

### 4.1 Machine (premise H_reg)

The machine is the cost model's 256-bit word RAM: every load, store, add, subtract, AND, OR, XOR, NOT, shift, compare, branch and random word is one operation, and the selected-round permutation is one unit (1626 operations). This entry declares a register file of 2,304 registers of 256 bits; register operands cost nothing beyond the operation, and the file's 73,728 bytes are counted as memory. The profile and cost model fix no register count; this is a declared convention, priced for 1,024 and 256 registers in Section 10.

### 4.2 Code encoding

The straight line has only register operations without immediates. One instruction is stored in 5 bytes: a 3-bit opcode (XOR, AND, OR, NOT) and three 12-bit register numbers (39 bits). All other code (loop, tests, handlers, cap scan, recovery and the one-walk permutation used by the recovery) is charged 40 bytes per instruction, for at most 4,096 instructions.

### 4.3 Memory map

| region | bytes |
| --- | ---: |
| straight line, 34,587 instructions of 5 bytes | 172,935 |
| other code, at most 4,096 instructions of 40 bytes | 163,840 |
| register file, 2,304 words | 73,728 |
| per lane: start index (8 bytes) and start batch (16 bytes), 256 lanes | 6,144 |
| R, the batch counter, the next index, the stage-1 counter, the entry count, B and constants | 256 |
| handler scratch (one copy of 256 planes) | 8,192 |
| recovery state (two lane-states of 25 words and two points) | 2,048 |
| table, 19,000 entries of 32 bytes | 608,000 |
| **total** | **1,035,143** |

1,035,143 <= 1,048,576 = 2^20, so memory_log2_bytes = 20 and the memory term of the score is 0.

## 5. The search

Parameters: d = 114 (a point is distinguished when its physical planes 0 to 113 are all zero in its lane, probability 2^-114 for a uniform point), L = 2^114, cap = 9L, K = 2^64, table capacity E = 19,000, B = 1,361,665,816,212,535,654,038,673,833,664,431,347 batches (about 2^120.0348), Q = 256 B = 348,586,448,950,409,127,433,900,501,418,094,424,832 evaluations.

A distinguished point is defined on physical planes: the condition is that the logical bits 0 to 113 equal the fixed polarity pattern P[0..113]. It is a fixed set of points of density 2^-114, which is all the analysis uses.

### 5.1 Setup (phase 0)

1. Draw one random word R (the cost model's independent uniform random 256-bit word).
2. Trail i starts at s_i = R + i mod 2^256. Lanes 0 to 255 get starts 0 to 255: the 256 x 256 bits are written into the planes with the polarity P (at most 196,608 + 256 operations), and the next index is 256.
3. Every lane stores its start index and its start batch 0.

### 5.2 Main loop (one batch)

1. The straight line (34,587 operations) replaces the 256 points by their images.
2. Stage-1 test: w = OR of planes 0 to 31 (31 operations); compare w with the all-ones word and branch (2). Lane t has bit t of w equal to 0 exactly when its planes 0 to 31 are zero.
3. Loop: add one to the batch counter b, compare with B, branch (3). At b = B the attempt halts with failure.

A batch is 34,623 operations.

### 5.3 Stage-1 handler (when w is not all ones)

v = OR of planes 32 to 113 (81 operations), z = w OR v, compare z with all ones and branch: 84 operations. If z is all ones no lane is distinguished and the loop continues. The attempt halts with failure if the stage-1 handler runs more than S1 = 2 floor(B / 2^24) + 2^20 times (expected about B 2^-24; Section 7.4).

### 5.4 Distinguished-point handler

For each lane t with bit t of z equal to 0 (a scan of 256 bit positions, 768 operations):

1. The key is the 64 physical bits 114 to 177 of the lane (256 operations).
2. The table is scanned linearly for the key (3 operations per stored entry, at most 57,000).
3. If the key is present: recovery (5.6) with that entry and the current trail (start index, length b - start batch). After the recovery the attempt stops: it outputs the pair if the recovery found one and fails otherwise.
4. If the table holds E entries the attempt halts with failure. Otherwise the entry (key, start index, length) is appended (4 stores).
5. Restart: the lane gets the next index i and the point R + i, written into its 256 planes (about 1,310 operations), and start batch b.

A distinguished-point event costs at most 58,570 operations; there are at most E of them.

### 5.5 Cap scan

Every K = 2^64 batches every lane whose age b - start batch exceeds cap is restarted as in 5.4.5 (at most 336,384 operations per scan). A trail is therefore cut after at most cap + K < 10L evaluations.

### 5.6 Recovery

Given two trails (start s_a, length l_a) and (s_b, l_b) that end at points with the same key, with l_a >= l_b: compute f^(l_a - l_b)(s_a), then step both values together until their images are equal; the two values with equal images are returned. Each step is one call of the selected-round permutation (one unit) plus at most 64 operations (splitting x and writing the 25 input lanes, reading and joining the four digest lanes, the comparison and the loop, with margin). At most 2(cap + K) steps.

If the two trails reach the same distinguished point and the first trail is not a suffix of the second (the second start is not a point of the first trail), the first equal images occur at two distinct values: the merge point of the trails. They are a collision of f.

## 6. Time

### 6.1 Ledger

| part | bound | word operations |
| --- | --- | ---: |
| main loop | B batches x 34,623 | 47,144,955,554,726,621,949,781,004,142,963,606,527,181 |
| stage-1 handler | S1 = 162,323,214,556,281,048,540,911,987,990 runs x 84 | 13,635,150,022,727,608,077,436,606,991,160 |
| distinguished-point events | E x (768 + 58,570) | 1,127,422,000 |
| cap scans | (floor(B / 2^64) + 1) x 336,384 | 24,830,538,770,993,391,576,576 |
| recovery, permutation calls | 2(cap + K) = 373,845,373,814,507,626,147,683,883,122,950,144 calls x 1626 | 607,872,577,822,389,400,116,133,993,957,916,934,144 |
| recovery, other operations | 2(cap + K) x 64 | 23,926,103,924,128,488,073,451,768,519,868,809,216 |
| generation of the straight line (preprocessing) | charged 2^32 | 4,294,967,296 |
| setup | 256 x 256 x 3 + 256 + 512 + 64 | 197,440 |
| **N** | | **47,776,754,250,108,289,885,528,736,753,876,813,425,013** |

The main loop is 98.68 percent of N, the recovery 1.32 percent; everything else is below 10^-9.

### 6.2 Preprocessing

The straight line is produced by the generator in experiments/sha3r6_rho.py from the round constants and rotation offsets. Its work (eight generations of about 40,000 symbolic gates, the row subset search, dead-code elimination and allocation) is well below 2^32 word operations, charged in N; preprocessing_log2 = 32 - log2(1626) < 22 target compressions is declared as 22.

### 6.3 Certificate

time_log2 = log2(N / 1626). The claim 124.46633 is log2(N / 1626) rounded up at the fifth decimal: 2^124.46632 * 1626 <= N < 2^124.46633 * 1626, checked in exact integer arithmetic as 1626^100000 * 2^12446632 <= N^100000 < 1626^100000 * 2^12446633 (Python big integers, true). The claim is 124.46633.

## 7. Success probability

### 7.1 Premise H_rand

H_rand: over the algorithm's fresh coins (the word R), the values of f on the points the search evaluates behave as those of a uniformly random function from 256-bit values to 256-bit values. Concretely, conditioned on the history of the attempt, every newly evaluated image at a point not evaluated before is uniform and independent of the earlier ones.

### 7.2 Finished trails

A trail is finished when it has reached a distinguished point and its entry was stored or looked up before the halt. Let S be the set of points evaluated on finished trails. If two distinct points x, x' of S have f(x) = f(x'), let A be the trail evaluated later at the merge. From f(x) on, A follows the path of the trail of x' (B), so both stop at the first distinguished point after f(x) = f(x'). B stored that point before A reached it (B passed f(x') earlier), so A's lookup finds B's key and the recovery runs. A finished trail has no repeated point (it would cycle without a distinguished point and could not finish), so A != B. The recovery returns (x, x') unless the start of A is a point of B's path, the Robin Hood case of 7.4.

### 7.3 Lemma: points outside S

Points outside S lie on the at most 256 trails unfinished at the halt or on cut trails.

- Unfinished trails. Under H_rand every image is distinguished with probability 2^-114 independently, so the age of the trail in a lane at the halt is dominated by a geometric variable of mean L, independently across lanes. Their sum exceeds 360 L with probability at most P(Gamma(256, L) > 360 L) = P(Poisson(360) <= 255) = 3.25e-9.
- Cut trails. A trail reaches 9L evaluations without a distinguished point with probability (1 - 2^-114)^(9L) < e^-9. At most E + 256 = 19,256 trails exist, so the number of cut trails exceeds 12 with probability at most P(Poisson(19,256 e^-9) >= 13) = 1.38e-6. Each cut trail holds fewer than 10 L points.

So |S| >= M = Q - 480 L = 338,617,238,982,022,258,387,121,948,465,991,840,512 except with probability below 1.39e-6.

### 7.4 Bound

Under H_rand, the images of the points of S are uniform and independent until the first repeat. Conditioning on the distinguished-point indicators (a function of the low 114 bits of each image) only raises the probability that two images are equal (two distinguished images agree on those bits; two others agree with probability 1/(2^114 - 1) instead of 2^-114). Hence the probability that S contains no pair of distinct points with equal images is at most prod_{i < M} (1 - i / 2^256) <= exp(-M(M - 1) / 2^257) = 0.609499.

Further failure terms:

| event | bound |
| --- | --- |
| more than 360 L points on unfinished trails | 3.25e-9 |
| more than 12 cut trails | 1.38e-6 |
| more than E distinguished points (Poisson mean below 16,800 against 19,000) | below 1e-30 |
| a key match between different distinguished points (64-bit keys, fewer than 2^15 entries and lookups) | below 2^-36 |
| Robin Hood: an image equal to a start point R + i (fewer than 2^15 starts, Q images) | below 2^-100 |
| the stage-1 handler runs more than S1 times (Chernoff, mean at most B 2^-24) | below 1e-30 |

The success probability is at least 1 - 0.6094986 - 0.0000014 = 0.3905 >= 0.39 (B is the least batch count for which the bound reaches 0.3905).

The bound is computed in the reproduction script with Decimal arithmetic (80 digits).

## 8. Heuristic premises and their evidence

- H_rand (score-critical) is a premise about one fixed function; it cannot be tested at width 256. If the real pair-collision rate among the evaluated images is (1 - eps) of the random-function rate, the margin 0.3905 - 0.39 covers eps up to 0.0016; a larger eps costs 0.5 log2(1 / (1 - eps)) more bits of time (0.0073 for eps = 0.01). Evidence: the experiments of Section 9 and the step checks of 3.7.
- H_reg (supporting, cost convention) is the register file of Section 4.1. Its effect is priced in Section 10.

## 9. Experiments

Both experiments are declared in experiments/manifest.json and run the shipped program experiments/sha3r6_rho.py, which regenerates the straight line of Section 3 (the same generator and allocation) and executes it on 256 trails per batch. The organizer recomputes every returned pair with its trusted digest.

### 9.1 rho-w22

Per trial, one attempt of the search of Section 5 at width 22: points are 22-bit values, the message of a point is its 32 little-endian bytes (upper bits zero), planes 22 to 255 are reset to logical 0 after every step, a point is distinguished when its physical planes 0 and 1 are zero, cap 36, 14 batches (3,584 evaluations), starts R + i from one random word, a dictionary table and the recovery of 5.6 with the reference implementation. The trial returns the pair the recovery finds, or two nulls.

- Event: digest-xor-mask on the 22 low digest bits (mask ffff3f followed by 29 zero bytes, expected zero).
- Ideal-function control (our run, not organizer-executed): the same search with the image replaced by an independent uniform 22-bit value per new point succeeds in 2,139 of 4,000 attempts, 0.535 (95 percent interval 0.519 to 0.550).
- Expectation if H_rand holds at this width: about 136.9 of 256 successes, standard deviation 8.0.
- Our runs on random seeds: 132 of 256 (target) and 141 of 256 (ideal control) in one run.
- Scope: a reduced-width search with the claimed program and control flow; it tests the program end to end and the rate of detected merges at 22 bits. It does not test 256-bit collision rates or full-scale trail lengths.

### 9.2 proj-w256

Per trial: 256 random planes as starting points (uniform points), eight chained full-width steps of the straight line, and the first pair, in step-major order, of distinct evaluated inputs whose images agree on the 22 low digest bits. The pair's inputs are recomputed from the trial's random planes with the plain implementation and returned.

- Event: digest-xor-mask on the 22 low digest bits.
- If the images of the 2,048 distinct evaluated inputs are uniform on 22 bits, a trial succeeds with probability 1 - prod_{i < 2048} (1 - i/2^22) = 0.39337: expectation 100.7 of 256, standard deviation 7.8. Our run: 98 of 256.
- Scope: iterates of the full-width chain, a 22-bit projection, 2,048 points per trial. A success is a partial match, not a collision.

## 10. Sensitivity

- Register file (H_reg). With the same straight line and Belady allocation (furthest next use), loads and stores add 12,893 operations per batch for 1,024 registers (+0.4567 bit) and 26,750 for 256 registers (+0.8259 bit); the memory stays below 2^20 with the smaller file and table. Scores 124.92303 and 125.29223.
- Code encoding. Charging 32 bytes per straight-line instruction instead of 5 would add 933,849 bytes. With a table of 9,000 entries (d = 115) the memory would be 1,648,992 bytes (2^20.65, a score penalty of 0.65) and the time about 0.05 bit higher, so the 5-byte encoding of Section 4.2 is score-relevant; it stores exactly the information the straight line needs (opcode and three register numbers).
- H_rand deficit: Section 8.

## 11. Relation to other entries, credits and literature

- Jbenisek's sha3-256-r6 entry 2d74a370 (10-12, time_log2 125.19730, memory 2^20.0801, passed review, not promoted because the scalar was then time-only) is the first low-memory distinguished-point search on this target, with 64 registers and every load and store counted. This entry was built independently (its program, ledger and proof are ours). It differs in the step program (theta evaluated lazily per chi row, per-row complement subsets) and in the machine: 34,587 register operations per step under the declared 2,304-register file, against 54,009 operations with every load and store on 64 registers in 2d74a370; with 256 registers this entry's step is 61,373 operations (Section 10). The declared register file follows the convention of Jbenisek's pareto blake3 entry 0a9640ed (1,024 registers counted as memory). Credit for both.
- Distinguished-point parallel collision search: P. C. van Oorschot and M. J. Wiener, Parallel collision search with cryptanalytic applications, Journal of Cryptology 12 (1999). Rho method: J. M. Pollard (1975). The argument needed here is given in Section 7.
- Lane complementing and bit-sliced Keccak: G. Bertoni, J. Daemen, M. Peeters, G. Van Assche, Keccak implementation overview (version 3.2). Section 3.3 states the variant used.

## 12. Reproduction

- `python3 experiments/sha3r6_rho.py --ledger` prints the instruction counts by operation, the register peak (2,304) and the input polarity weight.
- `python3 experiments/sha3r6_rho.py --selftest 512` checks the straight line against the plain six-round implementation.
- `python3 experiments/sha3r6_rho.py --stats 256` runs both experiments locally on random seeds and the ideal-function control.
- The integers of Sections 5 to 7 are produced by a separate reproduction script (claim_numbers.py, in the author's workspace, Decimal arithmetic) from the constants listed in Sections 5 and 6.
