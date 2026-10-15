# SHA3-256 with 6 prefix rounds: distinguished-point collision search with a linear-structure message embedding and a 28,543-operation bit-sliced step, time_log2 124.19636

## 1. Claim

Target `sha3-256-r6-prefix-v1`. This is SHA3-256 (FIPS 202) with Keccak-f rounds 0 to 5 in the single permutation call, zero initial state, rate 136 bytes, suffix 0x06 with pad10*1, and the full 256-bit digest. The algorithm outputs two distinct 128-byte one-block messages with equal complete digests (an ordinary collision).

| Quantity | Value |
|---|---|
| time_log2 (collision-frontier-v5, unit 1626 word operations, rounded up) | 124.19636 (Sections 4 and 5, certificate in Appendix A) |
| memory | at most 1,042,630 bytes <= 2^20, memory_log2_bytes = 20 (Section 6) |
| score S = time_log2 + max(0, memory_log2 - 20) | 124.19636 |
| success probability | at least 0.39 for one attempt, under the premise H_rand (Section 5) |
| preprocessing | the constant-selection run `gen 512` (512 constant sets, the best rebuilt), charged 513 x 2^32 + 512 x 2^10 operations; preprocessing_log2 = 31 (Section 3.6); no advice |

The method is a generic distinguished-point search (van Oorschot-Wiener) on a chain function F with 256 walks per step. It is the method of our earlier entry 2d74a370, with the same table, restart rule, deadlines, replay and success bound. Two things are new.

1. **The message embedding.** The 256-bit point is placed in six message lanes so that round 0 of the permutation and the theta step of round 1 are linear in the point. This is a one-round linear structure in the sense of Guo, Liu and Song (2016). With constants folded, those steps cost a few hundred word operations instead of several thousand.
2. **The step program.** It is a bit-sliced straight line of 28,543 register operations, built by a generator written for this entry (Appendix B). It follows the step design of jungjipdo's entry 67f781f8: theta evaluated lazily per chi row, a per-row complement subset, dead-code elimination, last-use register allocation, the digest written in place of the input, and a declared register file. We read 67f781f8's text as a description and wrote everything here ourselves; none of its code is used.

Three declarations are made in claim.json. H_rand (Section 5) is the score-critical premise on the function. H_reg (register file) and H_code (code-memory encoding) are machine conventions of the cost model, role supporting, in Section 3.5. Both conventions move the score, and Section 8 prices each one.

## 2. The function F and the encoding

Let u be a 256-bit point with little-endian 64-bit lanes u0, u1, u2, u3. The message m(u) has 128 bytes, the 16 lanes 0 to 15 of the absorbed state (lane index x + 5y):

- lane 1 = u0, lane 6 = u1, lane 11 = u0 xor u1 xor K11 (column x = 1, rows y = 0, 1, 2);
- lane 4 = u2, lane 9 = u3, lane 14 = u2 xor u3 xor K14 (column x = 4, rows y = 0, 1, 2);
- every other lane l in 0..15 holds the constant K_l (the table below).

With the SHA3 padding, byte 128 is 0x06 and byte 135 is 0x80. So the message is one absorbed block, lane 16 = 0x8000000000000006, and lanes 17 to 24 are zero. Rounds 0 to 5 are applied, and the digest is lanes 0 to 3 of the result (32 bytes). Define

    F(u) = SHA3-256-r6(m(u)) xor PD

where PD is a fixed 256-bit mask (the polarity of the program's digest planes, below). The map u -> m(u) is injective (lanes 1, 6, 4, 9 are u). Hence F(a) = F(b) with a != b gives two distinct messages m(a), m(b) with equal complete digests. XOR with a fixed mask is a bijection of the range, so F is a fixed function from 256 bits to 256 bits like the plain digest map.

Constants (hexadecimal, lane: value). They were chosen by the generator as trial 192 of 512 pseudo-random constant sets, the one with the fewest operations:

```
K0  c9a9d386ab38e13a  K2  9be65c0f48819e78  K3  a42df10543300344  K5  9d9a486de15a3242
K7  62628f16871056a6  K8  8d7196f55bc91f8b  K10 793ea2677e200f74  K11 7e8d7d4cce830045
K12 fe58db5a1de5126a  K13 1b571a79774b02ce  K14 8a2d82f8f9dcb705  K15 f01a6a80f9aae74b
PD (lanes 0..3) bc67dc6bab8bcb17 3820000300821020 2220094600040088 422009c4d01014c0
```

**Why round 0 is linear.**
- *Theta of round 0.* The column sums of columns 1 and 4 are constants: u0 xor u1 xor (u0 xor u1 xor K11) xor lane 16 xor lane 21 = K11 xor 0x8000000000000006, and u2 xor u3 xor (u2 xor u3 xor K14) xor lane 19 xor lane 24 = K14. So theta adds only constants to every lane.
- *Chi of round 0.* After rho and pi, the six message lanes land in positions where no two are adjacent inside a chi row. Each product of chi has at least one constant factor, so chi of round 0 is affine in u.
- *Round 1 theta.* It is a linear map of affine values, so it is affine too.

The generator tracks each value as a GF(2) affine form in the 256 input bits as long as it is affine. It emits an operation only when the form is new, so it reuses a form computed once. It stops tracking forms at the first nonlinear operation (chi of round 1). This choice is credited to Guo-Liu-Song's linear structures. The search uses no algebraic property: F is only evaluated.

## 3. One step of 256 walks: the straight line

### 3.1 Planes, polarity, gates

A batch is 256 walks. Plane (lane, z) is one 256-bit word whose bit t is bit z of that lane for walk t. Rotations of rho and the moves of pi rename planes and cost nothing.

Each value is held as a register and a polarity p: the logical value is the register word xor p, all-ones or zero. NOT and XOR with a constant flip p for free. Constant values are folded and never stored.

The operations, each one word operation, are:
- XOR: one operation;
- logical a AND b: one AND when both polarities are 0, one OR with output polarity 1 when both are 1, and two operations (A xor (A and B)) otherwise;
- NOT: one operation, used only for the row complements of 3.2.

Equal operands fold. A binary operation on the same pair of registers is emitted once (hash-consing).

### 3.2 Rounds

For each round r = 0..5 with the round constant of the profile:

1. Column sums C[x][z] (the five planes of the column, folded) and D[x][z] = C[x-1][z] xor C[x+1][z-1]. These are computed slice by slice, with C[.][63] first, so that few C values are live at once.
2. The chi rows, in order Y = 0..4 and z = 0..63. Each row XORs D into its five inputs b[X] = A[x][y][z - rho(x,y)] xor D[x][z - rho(x,y)] (x = 3Y + X mod 5, y = X) only when the row is computed (lazy theta).
3. **Row complement subset.** Before chi, the generator may NOT some of the five inputs. Over the 32 subsets it takes the first one that minimises NOTs plus the number of chi terms that need two operations. In a five-cycle the number of equal adjacent polarities is odd, so at least one extra operation per row remains.
4. chi: out[X] = b[X] xor ((not b[X+1]) and b[X+2]). iota flips the polarity of the lane-0 planes where the round constant has a 1.

**Round 5** computes only row Y = 0 and the outputs X = 0..3 (the digest lanes).

**Dead-code elimination** then removes every operation that no digest plane depends on.

### 3.3 Chain feed

Digest plane j is written into register j, which held input plane j. The physical digest word is the next point: F folds the digest polarity PD into the function (Section 2). There is no copy and no NOT between steps.

### 3.4 The ledger of one step

Printed by the generator (`gen 512`, Appendix B):

| operation | count |
|---|---:|
| XOR | 20,955 |
| AND | 3,985 |
| OR | 2,671 |
| NOT | 932 |
| load / store | 0 / 0 |
| **total** | **28,543** |

That is 111.50 word operations per evaluation of F, 0.0686 of the reference cost 1626 per evaluation.

The linear part is round 0 plus the theta of round 1, with 1,709 distinct affine forms tracked. A generic round of this program costs about 6,700 operations.

### 3.5 Registers and code encoding (machine conventions H_reg and H_code)

**Registers.** The values are allocated to registers in program order. A register is freed at the last use of its value. Input and digest plane j use register j; the allocator never gives register j < 256 to a value that would still be live when digest plane j is written. The program uses registers 0 to 2,180 (2,181 registers, at most 1,925 values live at once). The search keeps its own state in 11 further registers, 2,181 to 2,191. The step has no loads or stores.

**H_reg (declared machine convention, role supporting in claim.json).** The cost model and the target profile fix no register count. This package uses the 256-bit word RAM of collision-frontier-v5 with a declared file of 2,192 registers of 256 bits. An operation on register operands costs one word operation, with no load or store. All transfers are charged as stated: the step has no loads or stores, and every load and store of the other code is a charged word operation in Section 4. The file's 70,144 bytes are counted as memory (Section 6). This is the same convention as 67f781f8 (a declared file of 2,304 registers), which is a declared dependency of this package, and as our blake3 entry 0a9640ed. Section 8 prices the alternatives: 1,024 registers 124.608, 512 registers 124.810, 256 registers 124.966, 64 registers 125.119.

**H_code (declared code-memory charging convention, role supporting in claim.json).** The cost model and the target profile fix no code encoding.
- **Encoding.** Each straight-line instruction has only register operands and no immediate. It is stored in 5 bytes: a 3-bit opcode (0 XOR, 1 AND, 2 OR, 3 NOT) and three 12-bit register numbers (destination, a, b), 39 bits in little-endian order. The memory table charges the straight line at 5 bytes per instruction (Section 6).
- **Other code.** All other code (loop, handlers, replay, the one-walk permutation used by the replay) is charged 32 bytes per instruction.
- **Time ledger.** Each straight-line instruction is charged as the one word operation it performs (Sections 3.4 and 4.1). The ledger has no separate line for fetching or decoding instructions.
- **Sensitivity.** Section 8 prices a 32-byte-per-instruction straight line (about 124.82).

Both conventions move the score (Section 8). The role "supporting" in claim.json is the role of a declared convention and is not a statement that the premise is small. The checks of Section 3.7 and the organizer experiments validate the function of the program, decoded from its 5-byte encoding in software, with this allocation. They do not measure the cost of register access or of instruction execution, and no claim rests on such a measurement.

The program file is 142,715 bytes. Its SHA-256 is 016bc4cd3465a74680fa0b1844e750dcff72945c0f10be80fde95c5b26cbec88.

### 3.6 Generation and constant selection (preprocessing)

The preprocessing is one run of the selection program `gen 512` (Appendix B), a freestanding C program without libc. For each of 512 constant sets (trial 0: all constants zero; trial t > 0: xorshift constants from seed t) it builds the straight line (about 28,800 symbolic nodes, the row subset search, dead-code elimination) and counts its operations. It keeps the trial with the fewest operations (trial 192, 28,543; trial 0 gives 28,769), rebuilds it, allocates the registers and writes prog.bin, meta.txt and ledger.txt. `gen 1 192` writes the identical file (checked byte for byte). The attack runs `gen 512`, and that run is charged.

- **Time.** The run of 512 trial builds and one rebuild took 0.56 s of user time on one core of an AMD Ryzen 9 7900X (at most 5.6 GHz): at most 3.2 x 10^9 cycles and, at most 8 retired instructions per cycle, below 2^35 machine instructions. The ledger charges each of the 513 builds 2^32 word operations, and each trial a further 2^10 for its constants, the sum of the four counts, the comparison, the update of the best and its printed line: PRE = 513 x 2^32 + 512 x 2^10 = 2,203,318,747,136 word operations, part of N (Section 4.4). Since 2^30 < PRE / 1626 <= 2^31, preprocessing_log2 is declared as 31.
- **Memory.** The program is static and freestanding, and all its arrays are static (Appendix B, `MAXN = 32768`). Measured with `size`: text 17,985 bytes and data plus BSS 777,924 bytes, an image of 795,909 bytes.
  - `gen 512` was run under `nice -n 10 prlimit --as=1048576`, an address-space limit of 2^20 bytes. It completes, and prog.bin (SHA-256 016bc4cd... as above), meta.txt, the 512 trial lines and the ledger are identical to the output of the build with `MAXN = 65535` used in the earlier filings of this package. That build declared 1,076,900 bytes of data plus BSS and runs only with an address-space limit of at least 1,241,088 bytes. The value of `MAXN` is the only difference between the two sources.
  - The smallest address-space limit under which the new `gen 512` completes is 942,080 bytes (binary search in 4,096-byte steps). It also completes with the stack limited to 16,384 bytes.
  - The peak resident memory, measured by the program itself from /proc/self/status VmHWM, is at most 561,152 bytes (earlier runs 561,152 and 557,056; six runs of the new build, 548,864 to 557,056). The work runs in a forked child; getrusage of that child, read by the parent through wait4, gives 393,216 bytes.

### 3.7 Correctness of the step (checked by execution)

- `selftest` (our C program) executes the program file, decoded from its 5-byte encoding, on 2 x 256 uniform points for four chained steps each. It compares every output with F computed by a plain lane-wise six-round implementation. Result: 2,048 chained evaluations, 0 mismatches.
- That reference matches hashlib.sha3_256 at 24 rounds on 300 messages of lengths 0 to 299, and the organizer's verifier/keccak.py sha3_256(m, rounds=6) on the same messages: 0 mismatches.
- The experiment program regenerates the same straight line in Python and refuses to run unless its encoding hashes to the SHA-256 above. Before its trials it checks two chained full-width steps against the plain implementation.
- The organizer experiments then recompute every returned pair with the trusted digest (Section 7).

## 4. The search

Parameters:
- L = 256 walks.
- Distinguished point (DP): the planes 142 to 255 of F are zero (H = 114 bits, theta = 2^-114).
- Trail cap Lc = 17 x 2^114 steps.
- U = 21,000: the limit on trails started in one attempt, and the number of table words S.
- Tb = 1,344,468,483,582,484,789,411,976,361,654,878,208 = 67,878,312 x 2^94 = 1.01146567 x 2^120 steps of 256 walks per attempt.
- HMAX = floor(Tb (1 + 2^-20) / 2^8) + 1 + Lc = 358,328,021,402,897,758,426,346,050,933,489,665: the cap on prefilter hits. The attempt aborts at hit HMAX + 1.

State:
- in registers: the 256 input planes (registers 0 to 255); the step counter c, the next deadline nxt and the next trail number idn;
- in memory: LID[l] and LST[l] for each walk l (its trail number and the step at which it started); the table TAB of S words; rho; the hit counter h and HMAX; the constants.

A table word holds a record:
- bits 0 to 121: bits 0 to 121 of the trail's end (122 of the 142 bits a DP leaves free);
- bits 122 to 136: the trail number (15 bits);
- bits 137 to 255: the length (119 bits; Lc < 2^119).

A record is nonzero; an empty slot is zero.

```
rho := random word; idn := 256; h := 0; TAB := 0; for l < 256: LID[l] := l; LST[l] := 0; lane l of the input planes := rho + l
c := 0; nxt := min(Tb, Lc)
loop:
  the straight line (28,543): the input planes become F of the 256 walks
  pf := OR of the 16 planes 240..255 (15 ORs)
  if pf != all-ones (compare, branch):          -- some walk has planes 240..255 zero (probability 2^-16 each)
      h += 1; if h > HMAX: halt, the attempt failed   -- hit counter and abort (F5)
      slow test: OR of planes 142..239 -> the walks l at a DP
      for each such walk l, in increasing order:
          record := (bits 0..121 of the point of walk l) | LID[l] << 122 | (c - LST[l]) << 137
          probe TAB from slot (low 15 bits of the point, minus S if >= S), linear probing, wrap at S:
             empty slot: store the record
             a record with the same 122 end bits and a different trail number: REPLAY(that record, this record);
                if it returns a != b, output m(a), m(b) and stop; otherwise halt, the attempt failed
          restart(l)
  c += 1; if c != nxt goto loop (compare, branch)
  if c = Tb: halt, the attempt failed
  for each walk l with c - LST[l] = Lc: restart(l)        -- no DP within Lc steps
  nxt := min(Tb, min over l of LST[l] + Lc); goto loop
restart(l): if idn = U: halt, the attempt failed
            LID[l] := idn; LST[l] := c; lane l of the input planes := rho + idn; idn += 1
REPLAY(trail a of length la, trail b of length lb, the same end):
  p := rho + a, q := rho + b; the longer trail is advanced by |la - lb| evaluations of F
  if p = q return nothing; repeat min(la, lb) times: if F(p) = F(q) return (p, q); p := F(p); q := F(q)
  return nothing
```

### 4.1 One iteration of the loop

An iteration costs:
- the straight line, 28,543;
- the prefilter, 15;
- its test, 2;
- the counter, 3 (add, compare, branch).

**BSTEP = 28,563 operations.** No other operation runs in an iteration without a prefilter hit or a deadline.

### 4.2 The replay

The replay evaluates F on one point at a time with the selected-round permutation. Each call of the permutation is one unit (1626 operations). One evaluation costs at most E1 = 1626 + 35 operations: building the 25 input lanes (lanes 11 and 14 take two XORs each, the other lanes are moves of u or of constants; 29), the XOR with PD on the four digest lanes (4), and 2 spare.

The costs per evaluation:
- an advance step costs E1 + 7 (4 moves, add, compare, branch);
- a lock-step iteration costs 2 E1 + 19 (two evaluations, the equality test of four lanes with 4 XOR, 3 OR and a branch, 8 moves, the loop counter 3).

With both lengths at most Lc, the replay costs at most (E1 + 7)(max - min) + (2 E1 + 19) min <= (2 E1 + 19) Lc. At most one replay runs per attempt: the attempt stops after it, with the pair or (if the replay returns nothing, an event inside F4) with failure.

### 4.3 Rare operations

Each routine is straight-line code or a counted loop. Its count is an upper bound on what it executes.

- **A prefilter hit: 116.** The hit counter is 6 (load h, add, store, load HMAX, compare, branch). The slow test is 110: the OR of planes 142..239 (98), combine, compare, branch, call and return. The driver aborts at hit HMAX + 1, so every execution processes at most HMAX + 1 hits, and the ledger charges that number. The abort enters the success bound as F5 (Section 5).
- **A walk at a DP: 1,030 + 4 + (10 S + 20) + 6 + 2,460 + 1,100.** In order, these are:
  - gathering the walk's 256-bit point from the 256 planes (shift, mask, shift, OR per plane);
  - forming the record;
  - the probe, at most 10 per slot over at most S slots;
  - the store;
  - the restart (a 256-bit add, then for each of the 256 planes the new bit set into bit l);
  - the next deadline (a loop over the 256 LST words).

  It runs at most U + 1 times: every restart uses a trail number, plus one last DP.
- **Deadline scans: 1,300**, at most U + 1 times.
- **Setup and final bookkeeping: 704,000.**

R = (HMAX + 1) x 116 + (U + 1)(C_dp + 1,300) + 704,000 = 41,566,050,482,736,139,977,456,141,912,820,041,176.

### 4.4 Total

N = Tb x 28,563 + (2 E1 + 19) Lc + R + PRE = **39,623,246,885,746,059,599,222,323,362,107,280,213,464** word operations (Appendix A).

| part | operations | share |
|---|---:|---:|
| main loop, Tb x 28,563 | 38,402,053,296,566,513,039,974,280,817,948,286,255,104 | 0.96918 |
| replay, (2 E1 + 19) Lc | 1,179,627,538,696,810,419,270,586,400,042,855,170,048 | 0.02977 |
| rare operations R | 41,566,050,482,736,139,977,456,141,912,820,041,176 | 1.05e-3 |
| selection run `gen 512` (preprocessing), PRE | 2,203,318,747,136 | 6e-29 |

time_log2 = log2(N / 1626) rounded up at the fifth decimal = **124.19636**, checked in exact integer arithmetic:

    1626^100000 * 2^12419635 < N^100000 <= 1626^100000 * 2^12419636

## 5. Success probability and the premise H_rand

This section is the analysis of 2d74a370 (Section 6 there) with the parameters of Section 4.

**Premise H_rand.** F behaves as a uniformly random function from 256 bits to 256 bits: the values of F at distinct inputs are independent and uniform, and the random word rho is uniform. Two consequences are used, both for evaluations at distinct inputs:

- (i) the first coincidence of images among e evaluations has probability 1 - prod_{k<e}(1 - k/n) >= 1 - exp(-e(e-1)/(2n)) =: G(e), where n = 2^256;
- (ii) the point reached just after a coincidence is uniform, so the number l of further evaluations of a trail until its DP satisfies P(l >= j) = (1 - theta)^j, independently of when the coincidence happened.

**The coincidence.** Evaluations are numbered step by step and, inside a step, by walk. Let e* be the first evaluation whose image equals an earlier image, at step b* = ceil(e*/256). The trail B of that evaluation and the earlier trail A have equal points from then on, and both end at the same DP after l further evaluations of B. B is recorded at step b* + l at the latest. A reached the same point no later, so A was recorded before, or in the same step in a lower walk; the later record finds the earlier one.

The search succeeds if all of these hold:
- (a) b* + l <= Tb;
- (b) both trails have at most Lc evaluations;
- (c) fewer than U trails are started;
- (d) the coincidence is between two different trails;
- (e) the 122 stored end bits are those of the real ends, and the replay finds the merge.

Split l into bins of w = 2^102 steps: bin j holds l in [(j - 1) w, j w - 1], for j = 1 .. Lc / w = 17 x 2^12, with probability p_j = (1 - theta)^((j-1) w) - (1 - theta)^(j w). If l is in bin j, (a) holds when e* <= 256 (Tb - j w). By (ii),

    Pr[(a)] >= sum_j p_j G(256 (Tb - j w)).

The failure events that the sum does not cover:

- **F1**, some trail of the attempt has no DP within Lc steps: at most U (1 - theta)^Lc <= U e^-17 = 8.694e-04. This covers (b).
- **F2**, more than U - 256 DPs among the 256 Tb evaluations: the number is binomial with mean mu = 256 Tb theta = 16,571.9. The Chernoff bound e^-mu (e mu / (U - 256))^(U - 256) gives 9.0e-212. This covers (c).
- **F3**, the coincidence lies inside one trail: at most U 2^(2H) / n = 7.823e-05. This covers (d).
- **F4**, 2^-90. This covers (e). It includes:
  - a start rho + i equal to a point of another trail (U starts, about 2^128 images: below 2^-113);
  - two different ends with the same 122 stored bits (below U^2 2^-123 < 2^-94).
- **F5**, the hit counter aborts the attempt before it stops: below 2^-1000. Call a walk's input at a step fresh if F was not evaluated at it before in the attempt, and let X' count the steps at which some walk with a fresh input lands on planes 240..255 zero. Given the past, the images of the fresh inputs are independent and uniform (H_rand), so each step adds to X' with conditional probability at most 1 - (1 - 2^-16)^256 < 2^-8. A hit not counted in X' needs a walk at a repeated input. Outside F4 no start is a point of a trail, so repeated inputs occur only after the first image coincidence (step b*), and a successful attempt outside F1 stops at step b* + l with l <= Lc. On success, therefore, h <= X' + Lc, and an abort needs X' >= floor(Tb (1 + d) 2^-8) + 2 > (1 + d) mu, with d = 2^-20 and mu = Tb 2^-8. The Chernoff bound for indicators with conditional probabilities at most 2^-8 (supermartingale exp(s X'_t - (e^s - 1) t 2^-8)) gives probability at most exp(-d^2 mu / (2 + d)) = exp(-2.39 x 10^21) < 2^-1000. cert.py checks the exponent in exact rationals and subtracts 2^-1000 from the success bound. This is not sampled.

With a further 2^-60 for rounding, the success probability of one attempt, with the abort, is at least 0.3900000000 at Tb. It is 0.3899999910 at Tb - 2^94, so Tb is the least multiple of 2^94 that reaches 0.39. Appendix A computes both with 80-digit decimals.

In evaluations, 256 Tb = 1.011466 x 2^128. Most of this is the birthday point for success 0.39, which is 0.9943 x 2^128. The wait for the DPs of the last trails, 256 x 2^114 = 2^122 evaluations, is the main reason the count is above it.

A failed attempt (probability up to 0.61 under the premise) can be repeated with a fresh rho at the same cost. The claim is one attempt with success 0.39.

## 6. Memory

The search, at its peak:

| region | bytes |
|---|---:|
| register file, 2,192 words of 32 bytes (H_reg) | 70,144 |
| straight line plus prefilter, 28,558 instructions x 5 bytes (H_code) | 142,790 |
| other code (loop, slow test, DP handler, restart, deadline scan, replay, one-walk permutation), at most 4,096 instructions x 32 bytes | 131,072 |
| table, 21,000 words | 672,000 |
| LID and LST of the 256 walks, 512 words | 16,384 |
| scratch (one copy of the 256 planes) | 8,192 |
| constants K and PD, rho, counters, replay state, 64 words | 2,048 |
| **total** | **1,042,630** |

**Preprocessing.** The selection run `gen 512` runs before the search and ends before it starts (Section 3.6).

| `gen 512` | bytes |
|---|---:|
| text | 17,985 |
| static arrays, data plus BSS (`MAXN = 32768`) | 777,924 |
| image (text, data, BSS) | 795,909 |
| stack reserve (the run completes with a 16,384-byte stack limit) | 32,768 |
| the program it writes, prog.bin (streamed through a 4,000-byte buffer, counted here in full) | 142,715 |
| **bound used** | **971,392** |
| measured peak resident memory (VmHWM), at most | 561,152 |
| smallest address-space limit under which it completes | 942,080 |

The working memory of the generator is released before the table is filled.

**Total.** The two phases do not overlap, so the peak is the larger of the two, 1,042,630 <= 1,048,576 = 2^20. So memory_log2_bytes = 20 and the memory term of the score is 0. If the generator's measured peak is added to the search's instead (Section 8), the total is about 2^20.61; with its image and stack instead, about 2^20.84. Peak = max(search 1,042,630; preprocessing 971,392) = 1,042,630.

**The declared experiments are not the attack.** They run in Python at reduced width (rho-w22) or on 2,048 points per trial (proj-w256), as evidence of correctness and of the function's behaviour. Their memory is the Python interpreter's and is not part of the attack's memory. Measured peak resident memory of one organizer-shaped request of 256 trials (GNU time, Python 3, WSL):

| run | peak memory |
|---|---:|
| rho-w22 | 71,904 KiB |
| proj-w256 | 50,192 KiB |

Each takes about 4 seconds on one core. The C programs used for the checks of Sections 3.7 and 7.3 are also not part of the attack.

## 7. Evidence for the step and for H_rand

### 7.1 Organizer experiments (declared in experiments/manifest.json, program experiments/ls1.py)

Both experiments regenerate the straight line in Python with the generator's algorithm and node order (the encoding must hash to the SHA-256 of Section 3.5), check it against the plain six-round implementation, and execute it on Python integers, all trials side by side.

- **rho-w22** runs the search of Section 4 end to end at width 22. The planes 22 to 255 are set to zero after every step. The parameters are a DP of 4 low image bits zero, cap 128, 3,000 trails and 400 steps per attempt. Every trial returns two messages whose six-round digests agree on the 22 low bits.
  - At this width a start often lies on another trail, so a replay that returns nothing restarts the walk instead of ending the attempt. The full-size rule of Section 4 halts, as the failure term F4 accounts.
  - Our own runs on 9 x 256 local seeds: 2,304 of 2,304 trials returned a valid pair, with a mean of 18.01 steps to the pair. Our ideal-function control runs the same search with F replaced by a lazily sampled random function on 22 bits: 17.94 steps (20,000 trials, standard deviation 7.05; standard error of the 2,304-trial mean 0.15, z = +0.5).
- **proj-w256** runs eight chained full-width steps from 256 uniform points per trial and finds the first two distinct evaluated inputs whose images agree on the 22 low bits. The model gives success probability 0.3934 per trial, 100.7 of 256.
  - Our nine Python runs: 859 of 2,304 = 0.373 (z = -2.0).
  - The same trial in C at scale (Section 7.2): 0.3936 in 262,144 trials (z = +0.2), and 0.3882 in a first 16,384 (z = -1.4).
  - We read the Python shortfall as a fluctuation, since the large run sits on the model. The organizer run is one more sample of 256.

### 7.2 Our measured checks of H_rand under the linear round 0 (not organizer runs)

The linear embedding makes round 0 affine, so F has one fewer nonlinear round than the plain digest map. We measured whether that shows in the quantity the search depends on: the rate of image coincidences among the points it evaluates. hrand_test.c and proj_test.c (Appendix C) execute the program file itself. Results (AMD Ryzen 9 7900X, seeds in the sources):

```
A uniform inputs: M=2^24, pairs agreeing on 32 bits: low 32639, mid 32766, top 32877; expected 32768.0 each (sd 181.0); ratios 0.9961 0.9999 1.0033; z -0.71 -0.01 0.60
B consecutive inputs R+i: M=2^24, pairs agreeing on 32 bits: low 32764, mid 32644, top 32966; expected 32768.0 each (sd 181.0); ratios 0.9999 0.9962 1.0060; z -0.02 -0.68 1.09
C chained iterates (256 chains x 65536 steps): M=2^24, pairs agreeing on 32 bits: low 32679, mid 32837, top 32712; expected 32768.0 each (sd 181.0); ratios 0.9973 1.0021 0.9983; z -0.49 0.38 -0.31
D single-bit differences: 65536 cells x 4096 pairs, max |z| 4.09 at input bit 0 output bit 0 (largest of 65536 normal cells is about 4.4); mean z^2 0.9994 (expected 1)
proj at scale: 262144 trials, 103170 successes = 0.3936; model 0.3934; z 0.20
```

What these show:
- **Windows A to C.** The windows are bits 0-31, 128-159 and 224-255. The top window lies inside the bits that define a distinguished point. In each window, pair-coincidence rates among 2^24 images match the random-function value within 0.6 percent (one standard deviation is 0.55 percent). This holds for uniform inputs (A), for the consecutive starts rho + i the search uses (B), and for the chained iterates a walk evaluates (C).
- **Single-bit differences (D).** The output difference of single-bit input differences shows no bias: the largest |z| over 65,536 cells is 4.09, in line with independent cells, and the mean z^2 is 0.9994.

What they do not show: a deficit of a fraction of a percent, or any effect that appears only for 256-bit coincidences. The premise remains a premise.

If the real pair-coincidence rate is (1 - eps) of the random value, the same success needs about 0.5 log2(1/(1 - eps)) more bits of time. That is 0.0073 bit for eps = 0.01.

## 8. Sensitivity

| change | effect | score |
|---|---|---:|
| as claimed (H_reg 2,192 registers, H_code 5 bytes per instruction) | | 124.19636 |
| 1,024 registers: loads and stores (Belady eviction, spill.py on the same program) add 9,718 per step | time +0.41 | 124.608 |
| 512 registers, +15,625 per step | time +0.61 | 124.810 |
| 256 registers, +20,763 per step | time +0.77 | 124.966 |
| 64 registers, +26,412 per step | time +0.92 | 125.119 |
| straight line stored at 32 bytes per instruction | memory at least 1,141,696 bytes with no table; best found H = 117, table 3,600 words: time about 124.56, memory 2^20.26 | about 124.82 |
| generator peak added to the search's memory instead of the larger of the two | table 3,600 words, H = 117 fits 2^20: time about 124.56 (coarse bins) | about 124.56 |

- **Register rows.** These carry the same straight line, register allocation aside. A schedule built for the smaller file would do better.
- **Approximate rows.** The 32-byte-code and summed-memory rows come from the parameter scan with coarse bins of the success bound (opt_params.py); they are not certified.
- **H_rand.** A pair-coincidence deficit eps costs about 0.5 log2(1/(1 - eps)) bits (Section 7.2).
- **Same premises as 67f781f8.** Entry 67f781f8 uses the same register and 5-byte conventions. Under each row above it moves in the same direction; by its own Section 10, it is at 124.923 for 1,024 registers.

## 9. Relation to other entries, credits and literature

A credit is not an endorsement; nobody named here has reviewed this package.

- **jungjipdo, entry 67f781f8 (sha3-256-r6, 124.46633).** Its Section 3 describes the step design this package follows:
  - theta evaluated lazily per chi row and the per-row complement subsets;
  - dead-code elimination and the digest written over the input register;
  - last-use allocation into a declared register file;
  - the 5-byte straight-line encoding.

  We read its proof as a description. The generator, the self-test, the ledger, the search code and this text are our own, and none of its code was run, imported or compiled. This package is declared as derived from 67f781f8 (dependency) and uses the same register-file convention.
- **Our entry 2d74a370 (sha3-256-r6, 125.19730).** It supplies the search: the lockstep distinguished-point walks with restart on a DP, the table, deadlines, the replay, the success bound of Section 5 and the rare-operation accounting. Those are reused here with new parameters.
- **J. Guo, M. Liu, L. Song, Linear Structures: Applications to Cryptanalysis of Round-Reduced Keccak, ASIACRYPT 2016.** This is the linear-structure placement of message lanes that keeps round 0 linear, used in Section 2 as an embedding of the chain's points.
- **P. C. van Oorschot and M. J. Wiener, Parallel collision search with cryptanalytic applications, J. Cryptology 12 (1999); J. M. Pollard (1975).** These are the distinguished-point and rho methods.
- **G. Bertoni, J. Daemen, M. Peeters, G. Van Assche, Keccak implementation overview.** This is the source of the lane complementing transform, applied plane by plane in Section 3.2.

## 10. Limits

- **H_rand.** The premise is not tested at 256 bits; no run reaches 2^128 and no full collision is claimed. The checks of Section 7 work at 22 and 32 bits.
- **H_reg and H_code.** These are declared machine conventions, role supporting in claim.json (Section 3.5). The cost model fixes no register count and no code encoding. Both move the score, and Section 8 prices the alternatives.
- **What is executed, and what is bounded.**
  - The straight line is executed and compared with the plain permutation.
  - The search runs at width 22 in the experiment.
  - The routines of Section 4.3 are counted by stated bounds, not generated; their total is below 2^-9 of N.
  - The 4,096-instruction size of the other code is a declared bound, not a measured size.
- **Replay cost.** The replay is charged one unit per permutation call, plus the stated per-call operations.

## 11. The review of the earlier filing 3ff7e687

The review of the earlier filing of this package (submission 3ff7e687, status not_evaluable) listed eight finding ids. All eight have severity material and none is fatal. Each is answered here by id. The claim is unchanged: time_log2 124.19636, memory_log2_bytes 20, preprocessing_log2 31, success 0.39, the same prog.bin (SHA-256 016bc4cd...cbec88) and the same ledger. This version changes the role and the wording of H_reg and H_code and the memory statement of the generator.

| id | lane | answer in this version |
|---|---|---|
| F-MACHINE-CONVENTIONS | cryptanalysis | H_reg and H_code are stated as machine conventions. The cost model fixes neither a register count nor a code encoding (Section 3.5; claim.json heuristics H_reg and H_code, role supporting). Each is priced in Section 8: 1,024 registers 124.608, 512 124.810, 256 124.966, 64 125.119, and 32-byte code about 124.82. H_reg is the convention of 67f781f8 (2,304 registers), a declared dependency. |
| F-HREG-MODEL | evaluability | The package does not claim that the cost model supplies 2,192 registers. It declares the file as a convention, counts its 70,144 bytes as memory and charges every load and store of the other code. The other file sizes are priced in Section 8. |
| F-HCODE-MODEL | evaluability | The 5-byte encoding is stated as a code-memory charging rule (Sections 3.5 and 6). The time ledger counts one word operation per straight-line instruction and has no separate fetch or decode line. The 32-byte alternative is priced (about 124.82). The checks decode the encoding in software and validate function; no claim rests on a measurement of execution cost. |
| EXP-03 | experiments | No organizer experiment validates H_reg or H_code, and none is claimed to. The experiments validate the function of the program (Sections 3.7 and 7.1). The effect of the conventions is priced, not measured (Section 8). |
| F_cost_aux_unverified | cost | The routine counts of Section 4.3 are upper bounds for straight-line routines and counted loops. They are not generated code, and the 4,096-instruction size of the other code is a declared bound, not a measured size. Their weight: the rare operations R are 1.05e-3 of N, so doubling R would raise time_log2 by 0.0015. The other code is charged 131,072 bytes, and the memory margin to 2^20 is 5,946 bytes, 185 instructions of 32 bytes. With 8,192 instructions the total would be 1,173,702 bytes (2^20.163), a score of about 124.359 before any re-tuning of the table. |
| F-HRAND-EXTRAPOLATION | cryptanalysis, evaluability | H_rand is unchanged and remains the score-critical premise. It is extrapolated from 22- and 32-bit projections to 256-bit coincidences at about 2^128 evaluations and is not tested there (Sections 5, 7.2 and 10). A pair-coincidence deficit eps costs about 0.5 log2(1/(1 - eps)) bits (Section 7.2). |
| EXP-01 | experiments | No full collision and no 256-bit coincidence is observed or claimed. The organizer experiments are evidence at 22 bits and for the function of the straight line (Section 7.1). The bound 0.39 is derived from H_rand in Section 5, not from the experiments. |
| EXP-02 | experiments | No success probability is inferred from the organizer runs. They serve as an exact-digest check of the returned pairs and as a functional check of the program. The seeds are public and there is no holdout nonce. rho-w22 returned some repeated pairs, which are reported as they are, and no rate or independence of trials is inferred from them. The larger measurements of Section 7.2 are our own runs, labelled as such, and are not organizer-executed. They bound a pair-coincidence deficit at about half a percent and nothing finer. |

## Appendix A. The exact ledger

This program (cert.py) computes the step count, the success bound of Section 5, N, the memory table and the integer certificate. It uses integers and Fractions; Decimal with 80 digits is used only for the exponentials and logarithms of the success bound. It runs in about 20 seconds. Tb was found with `cert.py --search 67700000 67890000`, and the run below re-checks that Tb is the least multiple of 2^94 with success at least 0.39.

```python
# LS1 exact ledger: step count, success bound, N, memory, integer certificate (integers and Fractions; Decimal with 80
# digits only for the exponentials and logarithms of the success bound).
import sys
from fractions import Fraction as Fr
from decimal import Decimal as D, getcontext, ROUND_CEILING
getcontext().prec = 80
ceil = lambda v: int(v.to_integral_value(rounding=ROUND_CEILING)) if isinstance(v, D) else -((-v.numerator) // v.denominator)

# ---- one step of 256 walks (Section 3; counts printed by the generator gen.c, ledger.txt) ----
XOR, AND, OR, NOT = 20955, 3985, 2671, 932
LINE = XOR + AND + OR + NOT                      # the straight line, no loads or stores (registers, H_reg)
assert LINE == 28543
PF = 15                                          # prefilter: OR of the 16 planes 240..255
BSTEP = LINE + PF + 2 + 3                        # + compare pf with all-ones and branch; c += 1, compare with nxt, branch
print('step of 256 walks: straight line', LINE, '(xor %d and %d or %d not %d) + prefilter %d + test 2 + counter 3 =' % (XOR, AND, OR, NOT, PF), BSTEP)

# ---- parameters of the search (Section 4) ----
L, H, U = 256, 114, 21000                        # walks; distinguished point: planes 142..255 zero (theta = 2^-H); trail limit
S = U                                            # table words
KAPPA = 17
Lc = KAPPA * 2 ** H                              # cap on the length of a trail, in steps
n = D(2) ** 256
theta = D(2) ** -H
BINS = 12                                        # bins of w = 2^(H-12) steps for the remaining trail length
w = 2 ** (H - BINS)
J = Lc // w
lq = (1 - theta).ln()


def success(Tb):
    """Lower bound on the success probability of one attempt of Tb steps (Section 5)."""
    s, qprev = D(0), D(1)
    for j in range(1, J + 1):
        qj = (w * j * lq).exp()
        e = L * (Tb - j * w)
        if e > 1:
            s += (qprev - qj) * (1 - (-D(e) * (e - 1) / (2 * n)).exp())
        qprev = qj
    e1 = U * (-D(Lc) * theta).exp()                          # F1: some trail has no distinguished point within Lc steps
    mu, k = D(L * Tb) * theta, U - L
    e2 = (-mu + k * (1 + (mu / k).ln())).exp()               # F2: more than U - L distinguished points (Chernoff, k > mu)
    assert k > mu
    e3 = D(U) * D(2) ** (2 * H) / n                          # F3: a coincidence inside one trail
    e4 = D(2) ** -90                                         # F4: starts, end-key matches, replay
    e5 = D(2) ** -1000                                       # F5: the hit counter passes HMAX (abort); bound proved below
    return s - (e1 + e2 + e3 + e4 + e5 + D(2) ** -60), (e1, e2, e3, e4)


GRAN = 2 ** (H - 20)
if len(sys.argv) > 1 and sys.argv[1] == '--search':
    lo, hi = int(sys.argv[2]) * GRAN, int(sys.argv[3]) * GRAN
    assert success(hi)[0] >= D('0.39') > success(lo)[0]
    while hi - lo > GRAN:
        mid = (lo + hi) // 2 // GRAN * GRAN
        if success(mid)[0] >= D('0.39'): hi = mid
        else: lo = mid
    print('TB = %d * 2^%d' % (hi // GRAN, H - 20)); sys.exit()

TB = 67878312 * GRAN                                          # least multiple of 2^94 with success >= 0.39 (checked below)
p, (e1, e2, e3, e4) = success(TB)
p_less, _ = success(TB - GRAN)
assert p >= D('0.39') > p_less
print('Tb = %d = %.8f * 2^120, evaluations %.6f * 2^128' % (TB, D(TB) / D(2) ** 120, D(L * TB) / D(2) ** 128))
print('failure terms: F1 %.3e  F2 %.3e  F3 %.3e  F4 %.3e  success bound %s  (2^94 steps fewer: %s)' % (e1, e2, e3, e4, str(p)[:12], str(p_less)[:12]))

# ---- replay (Section 4.4): one evaluation = permutation (one unit, 1626) + 35 (state build 29, xor PD 4, margin 2) ----
E1 = 1626 + 35
replay = (2 * E1 + 19) * Lc                                  # advance (E1 + 7) per step, lock step (2 E1 + 19); at most (2 E1 + 19) Lc

# ---- prefilter hit counter and abort (Sections 4 and 5, F5) ----
DELTA = Fr(1, 2 ** 20)
HMAX = (TB * (1 + DELTA)) // 2 ** 8 + 1 + Lc                 # the driver aborts (attempt failed) when hit number HMAX + 1 occurs
# F5: abort => X' > (1 + DELTA) Tb 2^-8, X' = steps with a hit among walks at fresh inputs (conditional prob. <= 2^-8 each,
# H_rand); steps with a walk at a repeated input lie after the first coincidence and number at most Lc before the stop.
# Chernoff for adapted indicators: P[X' >= (1 + d) mu] <= exp(-d^2 mu / (2 + d)), mu = Tb 2^-8.
MU = Fr(TB, 2 ** 8)
EXPO = DELTA ** 2 * MU / (2 + DELTA)                         # P[F5] <= exp(-EXPO)
assert EXPO > 1000 * Fr(6932, 10000)                         # ln 2 < 0.6932, so P[F5] < 2^-1000 (the e5 of success())
print('hit counter: HMAX =', HMAX, '; P[abort before the stop on success] <= exp(-%d) < 2^-1000' % (EXPO.numerator // EXPO.denominator))

# ---- rare operations (Section 4.3) ----
hits = HMAX + 1                                              # at most HMAX + 1 hits are processed in every execution
C_hit = 110 + 6                                              # slow test (OR of planes 142..239 (98), compare, branch, call, return)
                                                             # + counter: load h, add, store, load HMAX, compare, branch
C_dp = 1030 + 4 + (10 * S + 20) + 6 + 2460 + 1100            # gather the point, record, probe, store, restart, next deadline
R = hits * C_hit + (U + 1) * C_dp + (U + 1) * 1300 + 704000
PRE = 513 * 2 ** 32 + 512 * 2 ** 10                          # preprocessing = the selection run `gen 512`: 512 trial builds and the
                                                             # rebuild of the best, 2^32 each, + per trial at most 2^10 for the
                                                             # constants, the total, the comparison, the best update and the line
N = TB * BSTEP + replay + R + PRE
print('main', TB * BSTEP, ' replay', replay, ' rare', R, ' preprocessing', PRE)
pl = 31
assert (1626 << (pl - 1)) < PRE <= (1626 << pl)
print('preprocessing_log2: 2^%d < PRE / 1626 <= 2^%d, declared %d' % (pl - 1, pl, pl))
print('N =', N)
print('shares: main %.5f replay %.5f other %.2e' % (TB * BSTEP / N, replay / N, (R + PRE) / N))

# ---- memory (Section 6) ----
REGS = 2192                                                  # 2,181 used by the straight line + 11 for the loop and search state
mem_run = {
    'register file, 2,192 words': 32 * REGS,
    'straight line incl. prefilter, 28,558 instructions x 5 bytes': 5 * (LINE + PF),
    'other code (driver, handlers, replay, one-walk permutation), at most 4,096 instructions x 32 bytes': 32 * 4096,
    'table, %d words' % S: 32 * S,
    'LID and LST of the 256 walks, 512 words': 32 * 512,
    'scratch (one copy of the 256 planes)': 32 * 256,
    'constants (K, PD), rho, counters, replay state, 64 words': 32 * 64,
}
run_total = sum(mem_run.values())
GEN_PEAK = 561152                                            # bound on the measured VmHWM of `gen 512` (resident; 6 runs 548,864 to 557,056)
GEN_IMAGE = 17985 + 777924                                   # gen (MAXN = 32768): text + data + BSS, size(1); all arrays are static
GEN_STACK = 32768                                            # stack reserve; `gen 512` completes with the stack limited to 16,384 bytes
pre_total = max(GEN_PEAK, GEN_IMAGE + GEN_STACK) + 5 * LINE  # generator (declared image and stack) plus the program it writes
for k, v in mem_run.items(): print('  %9d  %s' % (v, k))
print('search memory', run_total, '; preprocessing (gen 512): image', GEN_IMAGE, '+ stack', GEN_STACK, '+ program', 5 * LINE, '=', pre_total, '(measured resident peak %d)' % GEN_PEAK)
mem = max(run_total, pre_total)
assert mem <= 2 ** 20
print('memory', mem, '<= 2^20 = 1048576: memory_log2_bytes = 20')

K = 100000
e = ceil(K * (D(N) / 1626).ln() / D(2).ln())
while N ** K > (1626 ** K) << e: e += 1
while N ** K <= (1626 ** K) << (e - 1): e -= 1
print('certificate: 1626^%d * 2^%d < N^%d <= 1626^%d * 2^%d' % (K, e - 1, K, K, e))
print('time_log2 = %d.%05d' % divmod(e, K))
print('score = time_log2 + max(0, memory_log2 - 20) = %d.%05d' % divmod(e, K))
```

Output:

```
step of 256 walks: straight line 28543 (xor 20955 and 3985 or 2671 not 932) + prefilter 15 + test 2 + counter 3 = 28563
Tb = 1344468483582484789411976361654878208 = 1.01146567 * 2^120, evaluations 1.011466 * 2^128
failure terms: F1 8.694e-04  F2 9.034e-212  F3 7.823e-05  F4 8.078e-28  success bound 0.3900000000  (2^94 steps fewer: 0.3899999910)
hit counter: HMAX = 358328021402897758426346050933489665 ; P[abort before the stop on success] <= exp(-2388254647361271098429) < 2^-1000
main 38402053296566513039974280817948286255104  replay 1179627538696810419270586400042855170048  rare 41566050482736139977456141912820041176  preprocessing 2203318747136
preprocessing_log2: 2^30 < PRE / 1626 <= 2^31, declared 31
N = 39623246885746059599222323362107280213464
shares: main 0.96918 replay 0.02977 other 1.05e-03
      70144  register file, 2,192 words
     142790  straight line incl. prefilter, 28,558 instructions x 5 bytes
     131072  other code (driver, handlers, replay, one-walk permutation), at most 4,096 instructions x 32 bytes
     672000  table, 21000 words
      16384  LID and LST of the 256 walks, 512 words
       8192  scratch (one copy of the 256 planes)
       2048  constants (K, PD), rho, counters, replay state, 64 words
search memory 1042630 ; preprocessing (gen 512): image 795909 + stack 32768 + program 142715 = 971392 (measured resident peak 561152)
memory 1042630 <= 2^20 = 1048576: memory_log2_bytes = 20
certificate: 1626^100000 * 2^12419635 < N^100000 <= 1626^100000 * 2^12419636
time_log2 = 124.19636
score = time_log2 + max(0, memory_log2 - 20) = 124.19636
```

so N = 39623246885746059599222323362107280213464 word operations and time_log2 = 124.19636.

## Appendix B. The generator (gen.c) and the self-test (selftest.c)

Build: `gcc -O2 -static -nostdlib -ffreestanding -fno-builtin -fno-tree-loop-distribute-patterns -fno-stack-protector -fno-pie -no-pie -o gen gen.c`; run `gen 512` (writes prog.bin, meta.txt, ledger.txt; `gen 1 192` writes the same files; `MAXN` 32768 or 65535 gives the same files). `selftest run 2` checks prog.bin as in Section 3.7; `selftest kat` prints the reference digests compared with hashlib and the organizer reference.

```c
/* gen.c - LS1 step generator for sha3-256-r6 (6 prefix rounds of Keccak-f[1600]).
 * Freestanding (no libc) so the measured peak RSS is the generator's own working set.
 *
 * Chain function on physical 256-bit points u (4 lanes u0..u3):
 *   message m(u) = 128 bytes = lanes 0..15 of the absorbed state:
 *     lane 1 = u0, lane 6 = u1, lane 11 = u0^u1^K[11]   (column x=1, rows 0,1,2)
 *     lane 4 = u2, lane 9 = u3, lane 14 = u2^u3^K[14]   (column x=4, rows 0,1,2)
 *     other lanes 0..15 = constants K[l]; lane 16 = 0x8000000000000006 (SHA3 pad);
 *   F(u) = SHA3-256-r6(m(u)) XOR PD   (PD = fixed digest polarity mask of the program).
 * Column parities of the message lanes are constant, so round-0 theta adds only
 * constants; no two message lanes are chi-adjacent after rho/pi, so round 0 is
 * linear in u and round-1 theta stays linear (Guo-Liu-Song 2016 linear structure).
 *
 * Representation: plane (lane,z) is one 256-bit word (bit t = trail t). A value is
 * (node, polarity): logical = physical(node) XOR p. Constants folded. Linear nodes
 * carry their GF(2) form over the 256 input bits, deduplicated by form.
 * Lazy theta: C, D per round; each chi row XORs D into its five planes when computed.
 * Per-row complement subset (32 candidates) minimizing NOTs + two-op terms.
 * Dead-code elimination, last-use register allocation; digest plane j written to
 * register j (= input register j of the next step: free chain feed).
 * Outputs: prog.bin (5 bytes/instr: 3-bit op, 12-bit dst, a, b), meta.txt, ledger.txt.
 * Usage: gen [ntrials] [first]  (trial 0: all constants 0; trial t>0: xorshift constants seed t).
 * The preprocessing of the attack is the selection run "gen 512": 512 trial builds, the best (trial 192) rebuilt and written.
 */
typedef unsigned long u64; typedef unsigned int u32; typedef unsigned short u16; typedef unsigned char u8;
typedef long i64;

/* ---------- freestanding runtime ---------- */
__asm__(".global _start\n_start:\n xor %rbp,%rbp\n mov %rsp,%rdi\n and $-16,%rsp\n call cmain\n mov %rax,%rdi\n mov $60,%rax\n syscall\n");
static i64 sc3(i64 n, i64 a, i64 b, i64 c){ i64 r; __asm__ volatile("syscall":"=a"(r):"a"(n),"D"(a),"S"(b),"d"(c):"rcx","r11","memory"); return r; }
void *memset(void *d, int c, unsigned long n){ u8 *p=d; while(n--) *p++=(u8)c; return d; }
void *memcpy(void *d, const void *s, unsigned long n){ u8 *p=d; const u8 *q=s; while(n--) *p++=*q++; return d; }
static int fd_out = 1;
static char obuf[4096]; static int olen;
static void oflush(void){ if(olen){ sc3(1,fd_out,(i64)obuf,olen); olen=0; } }
static void oc(char c){ if(olen==4096) oflush(); obuf[olen++]=c; }
static void os(const char *s){ while(*s) oc(*s++); }
static void ou(u64 v){ char t[24]; int n=0; do{ t[n++]='0'+v%10; v/=10; }while(v); while(n) oc(t[--n]); }
static void ox(u64 v){ for(int i=60;i>=0;i-=4) oc("0123456789abcdef"[(v>>i)&15]); }
static int fopen_w(const char *p){ return (int)sc3(2,(i64)p,01|0100|01000,0644); } /* O_WRONLY|O_CREAT|O_TRUNC */
static void fclose_(int fd){ sc3(3,fd,0,0); }
static void die(const char *m){ oflush(); fd_out=2; os("gen: "); os(m); oc('\n'); oflush(); sc3(60,1,0,0); }
static int atoi_(const char *s){ int v=0; while(*s>='0'&&*s<='9') v=v*10+(*s++-'0'); return v; }

/* ---------- Keccak constants ---------- */
static const u64 RC[24]={0x0000000000000001UL,0x0000000000008082UL,0x800000000000808aUL,0x8000000080008000UL,
 0x000000000000808bUL,0x0000000080000001UL,0x8000000080008081UL,0x8000000000008009UL,0x000000000000008aUL,
 0x0000000000000088UL,0x0000000080008009UL,0x000000008000000aUL,0x000000008000808bUL,0x800000000000008bUL,
 0x8000000000008089UL,0x8000000000008003UL,0x8000000000008002UL,0x8000000000000080UL,0x000000000000800aUL,
 0x800000008000000aUL,0x8000000080008081UL,0x8000000000008080UL,0x0000000080000001UL,0x8000000080008008UL};
static const int ROT[5][5]={{0,36,3,41,18},{1,44,10,45,2},{62,6,43,15,61},{28,55,25,21,56},{27,20,39,8,14}}; /* ROT[x][y] */
#define NROUNDS 6

/* ---------- node store ---------- */
#define MAXN 32768           /* the selected build uses 28,799 nodes; 32768 keeps the declared static arrays under 2^20 bytes */
#define NC 0xFFFF            /* constant marker */
enum { O_IN=0, O_XOR=1, O_AND=2, O_OR=3, O_NOT=4 };
#define F_OPM 7
#define F_K 8                /* physical constant of a linear node */
#define F_LIVE 16
#define F_LIN 32
static u8 nf[MAXN];          /* op | flags */
static u16 na[MAXN], nb[MAXN];
static u16 linid[MAXN];      /* form index for linear nodes; reused as reg[] */
#define MAXF 8192
static u64 form[MAXF][4]; static u16 formnode[MAXF]; static int nform;
#define FH 16384
static u16 fh[FH];           /* form hash: form index+1 */
#define CH 65536
static u16 ch[CH];           /* cons hash: node+1; reused as lastuse[] */
static int nn;

typedef struct { u16 n; u8 p; } V;
static V K_(int c){ V v; v.n=NC; v.p=(u8)c; return v; }
static V MK(int n,int p){ V v; v.n=(u16)n; v.p=(u8)p; return v; }

static u32 hmix(u32 x){ x^=x>>16; x*=0x7feb352dU; x^=x>>15; x*=0x846ca68bU; x^=x>>16; return x; }
static int newnode(int op,int a,int b){ if(nn>=MAXN-1) die("node overflow"); nf[nn]=(u8)op; na[nn]=(u16)a; nb[nn]=(u16)b; linid[nn]=0xFFFF; return nn++; }
static int cons(int op,int a,int b){
  if(op!=O_NOT && a>b){ int t=a;a=b;b=t; }
  u32 h=hmix((u32)op*0x9E3779B1u ^ (u32)a*0x85EBCA77u ^ (u32)b*0xC2B2AE3Du)&(CH-1);
  for(;;){ u16 e=ch[h]; if(!e) break; int m=e-1; if((nf[m]&F_OPM)==op && na[m]==a && nb[m]==b) return m; h=(h+1)&(CH-1); }
  int m=newnode(op,a,b); ch[h]=(u16)(m+1); return m;
}
static int isk(int n){ return (nf[n]&F_K)?1:0; }
static int islin(int n){ return (nf[n]&F_LIN)?1:0; }
static u32 fhash(const u64 *m){ return hmix((u32)(m[0]^m[0]>>32^m[1]*3^m[2]*5^m[3]*7^(m[1]>>29)^(m[3]>>31))); }
static int flookup(const u64 *m){ u32 h=fhash(m)&(FH-1); for(;;){ u16 e=fh[h]; if(!e) return -1; int f=e-1; if(form[f][0]==m[0]&&form[f][1]==m[1]&&form[f][2]==m[2]&&form[f][3]==m[3]) return f; h=(h+1)&(FH-1);} }
static int fadd(const u64 *m,int node){ if(nform>=MAXF) die("form overflow"); int f=nform++; for(int i=0;i<4;i++) form[f][i]=m[i]; formnode[f]=(u16)node;
  u32 h=fhash(m)&(FH-1); while(fh[h]) h=(h+1)&(FH-1); fh[h]=(u16)(f+1); return f; }

static long cnt_emit; /* ops created (pre-DCE) */

static V xorv(V a,V b){
  if(a.n==NC) return MK(b.n==NC?NC:b.n, b.p^a.p);
  if(b.n==NC) return MK(a.n, a.p^b.p);
  if(a.n==b.n) return K_(a.p^b.p);
  if(islin(a.n)&&islin(b.n)){
    const u64 *fa=form[linid[a.n]], *fb=form[linid[b.n]]; u64 m[4];
    for(int i=0;i<4;i++) m[i]=fa[i]^fb[i];
    int kk=isk(a.n)^isk(b.n);
    if(!(m[0]|m[1]|m[2]|m[3])) return K_(kk^a.p^b.p);
    int f=flookup(m);
    if(f>=0){ int n3=formnode[f]; return MK(n3, kk^a.p^b.p^isk(n3)); }
    int n=newnode(O_XOR,a.n<b.n?a.n:b.n,a.n<b.n?b.n:a.n); nf[n]|=F_LIN|(kk?F_K:0);
    linid[n]=(u16)fadd(m,n); cnt_emit++; return MK(n,a.p^b.p);
  }
  int before=nn; int n=cons(O_XOR,a.n,b.n); if(nn>before) cnt_emit++;
  return MK(n,a.p^b.p);
}
static V notv(V a){ /* physical complement, logical value unchanged */
  if(a.n==NC) return a;
  int before=nn; int n=cons(O_NOT,a.n,0);
  if(nn>before){ cnt_emit++; if(islin(a.n)){ nf[n]|=F_LIN|(isk(a.n)?0:F_K); linid[n]=linid[a.n]; } }
  return MK(n,a.p^1);
}
static V and2(V a,V b){ /* logical a AND b */
  if(a.n==NC) return a.p? b : K_(0);
  if(b.n==NC) return b.p? a : K_(0);
  if(a.n==b.n) return a.p==b.p? a : K_(0);
  int before=nn;
  if(a.p==0&&b.p==0){ int n=cons(O_AND,a.n,b.n); if(nn>before) cnt_emit++; return MK(n,0); }
  if(a.p==1&&b.p==1){ int n=cons(O_OR,a.n,b.n); if(nn>before) cnt_emit++; return MK(n,1); }
  /* A & ~B with A the pol-0 operand: A ^ (A & B) */
  int A=a.p==0?a.n:b.n, B=a.p==0?b.n:a.n;
  int t=cons(O_AND,A,B); if(nn>before) cnt_emit++;
  return xorv(MK(A,0),MK(t,0));
}
static V andnot(V b1,V b2){ b1.p^=1; return and2(b1,b2); } /* (~b1) & b2 */

/* cost estimate of (~b1)&b2 given polarities */
static int cost_term(V b1,V b2){ if(b1.n==NC||b2.n==NC||b1.n==b2.n) return 0; return ((b1.p^1)==b2.p)?1:2; }

/* ---------- the step ---------- */
static V S[25][64], NS[25][64], Cc[5][64], Dd[5][64];
static u64 KL[25];          /* lane constants of the absorbed state (var lanes: offset) */
static int outnode[256];
static u64 PD[4];
static long nnot_rows;

static void build(void){
  nn=0; nform=0; cnt_emit=0; nnot_rows=0;
  memset(fh,0,sizeof fh); memset(ch,0,sizeof ch);
  for(int j=0;j<256;j++){ int n=newnode(O_IN,0,0); u64 m[4]={0,0,0,0}; m[j>>6]=1UL<<(j&63); nf[n]|=F_LIN; linid[n]=(u16)fadd(m,n); }
  for(int l=0;l<25;l++) for(int z=0;z<64;z++) S[l][z]=K_((KL[l]>>z)&1);
  for(int z=0;z<64;z++){
    S[1][z]=MK(z,(KL[1]>>z)&1); S[6][z]=MK(64+z,(KL[6]>>z)&1);
    S[4][z]=MK(128+z,(KL[4]>>z)&1); S[9][z]=MK(192+z,(KL[9]>>z)&1);
  }
  for(int z=0;z<64;z++){
    S[11][z]=xorv(xorv(MK(z,0),MK(64+z,0)),K_((KL[11]>>z)&1));
    S[14][z]=xorv(xorv(MK(128+z,0),MK(192+z,0)),K_((KL[14]>>z)&1));
  }
  for(int r=0;r<NROUNDS;r++){
    int last=(r==NROUNDS-1);
    /* theta: C[.][63] first, then per z: C[.][z], D[.][z] (keeps few C live) */
    for(int x=0;x<5;x++){ V s=S[x][63]; for(int y=1;y<5;y++) s=xorv(s,S[x+5*y][63]); Cc[x][63]=s; }
    for(int z=0;z<64;z++){
      if(z<63) for(int x=0;x<5;x++){ V s=S[x][z]; for(int y=1;y<5;y++) s=xorv(s,S[x+5*y][z]); Cc[x][z]=s; }
      for(int x=0;x<5;x++) Dd[x][z]=xorv(Cc[(x+4)%5][z],Cc[(x+1)%5][(z+63)&63]);
    }
    int nY=last?1:5, needmask=last?0x0F:0x1F;
    for(int Y=0;Y<nY;Y++) for(int z=0;z<64;z++){
      V b[5];
      for(int X=0;X<5;X++){ int y=X, x=(3*Y+X)%5; int zz=(z-ROT[x][y]+64)&63; b[X]=xorv(S[x+5*y][zz],Dd[x][zz]); }
      /* complement subset */
      int best=-1,bc=1<<30;
      for(int s=0;s<32;s++){
        int c=0; V bb[5];
        for(int X=0;X<5;X++){ bb[X]=b[X]; if(s>>X&1){ if(b[X].n==NC){ c=1<<29; } else { bb[X].p^=1; c++; } } }
        for(int X=0;X<5;X++) if(needmask>>X&1) c+=cost_term(bb[(X+1)%5],bb[(X+2)%5]);
        if(c<bc){ bc=c; best=s; }
      }
      for(int X=0;X<5;X++) if(best>>X&1){ b[X]=notv(b[X]); nnot_rows++; }
      for(int X=0;X<5;X++) if(needmask>>X&1){
        V t=andnot(b[(X+1)%5],b[(X+2)%5]);
        NS[X+5*Y][z]=xorv(b[X],t);
      }
    }
    for(int z=0;z<64;z++) NS[0][z].p^=(RC[r]>>z)&1;   /* iota */
    for(int l=0;l<25;l++) for(int z=0;z<64;z++) S[l][z]=NS[l][z];
  }
  PD[0]=PD[1]=PD[2]=PD[3]=0;
  for(int j=0;j<256;j++){ V v=S[j>>6][j&63]; if(v.n==NC||v.n<256) die("digest plane constant or input"); outnode[j]=v.n; PD[j>>6]|=(u64)v.p<<(j&63); }
  for(int j=0;j<256;j++) for(int k=j+1;k<256;k++) if(outnode[j]==outnode[k]) die("shared digest node");
}

static long cnt[5], nlive, maxlive, maxreg;
static void dce(void){
  for(int i=0;i<nn;i++) nf[i]&=~F_LIVE;
  for(int j=0;j<256;j++) nf[outnode[j]]|=F_LIVE;
  for(int i=nn-1;i>=256;i--) if(nf[i]&F_LIVE){ int op=nf[i]&F_OPM; nf[na[i]]|=F_LIVE; if(op!=O_NOT) nf[nb[i]]|=F_LIVE; }
  for(int k=0;k<5;k++) cnt[k]=0; nlive=0;
  for(int i=256;i<nn;i++) if(nf[i]&F_LIVE){ cnt[nf[i]&F_OPM]++; nlive++; }
}

/* register allocation; writes prog.bin when emit */
#define NREG 2304
static u16 freestk[NREG]; static int nfree;
static u16 outdef[256];
static int alloc_emit(int emit){
  u16 *last=ch, *reg=linid;     /* reuse */
  for(int i=0;i<nn;i++) last[i]=0;
  for(int i=256;i<nn;i++) if(nf[i]&F_LIVE){ last[na[i]]=(u16)i; if((nf[i]&F_OPM)!=O_NOT) last[nb[i]]=(u16)i; }
  for(int j=0;j<256;j++){ last[outnode[j]]=0xFFFF; outdef[j]=(u16)outnode[j]; }
  static u8 outof[MAXN/8+1]; memset(outof,0,sizeof outof);
  static u8 regbusy[NREG]; memset(regbusy,0,sizeof regbusy);
  static short outj[MAXN];  /* only touched for out nodes */
  for(int j=0;j<256;j++){ outof[outnode[j]>>3]|=1<<(outnode[j]&7); outj[outnode[j]]=(short)j; }
  nfree=0; for(int r=NREG-1;r>=256;r--) freestk[nfree++]=(u16)r;
  long live=0; maxlive=0; maxreg=0;
  for(int j=0;j<256;j++){ reg[j]=(u16)j; if(last[j]){ regbusy[j]=1; live++; } }
  if(live>maxlive) maxlive=live;
  int fd=-1; if(emit){ fd=fopen_w("prog.bin"); if(fd<0) die("open prog.bin"); }
  static u8 eb[4000]; int el=0; long ninstr=0;
  for(int i=256;i<nn;i++){
    if(!(nf[i]&F_LIVE)) continue;
    int op=nf[i]&F_OPM; int a=na[i], b=(op==O_NOT)?a:nb[i];
    /* free operands whose last use is here */
    int ops[2]={a,b};
    for(int k=0;k<2;k++){ int o=ops[k]; if(k==1&&o==a) break; if(last[o]==i){ int r=reg[o]; regbusy[r]=0; live--; if(r>=256) freestk[nfree++]=(u16)r; } }
    int dst;
    if(outof[i>>3]>>(i&7)&1){ dst=outj[i]; if(regbusy[dst]) die("output register busy"); }
    else if(nfree>0) dst=freestk[--nfree];
    else { dst=-1; for(int r=0;r<256;r++) if(!regbusy[r] && outdef[r]>=last[i]) { dst=r; break; } if(dst<0) die("out of registers"); }
    regbusy[dst]=1; live++; reg[i]=(u16)dst; if(live>maxlive) maxlive=live; if(dst+1>maxreg) maxreg=dst+1;
    if(last[i]==0){ /* dead value (cannot happen after DCE) */ die("live node without use"); }
    if(emit){
      int code= op==O_XOR?0: op==O_AND?1: op==O_OR?2: 3;
      u64 w=(u64)code | (u64)dst<<3 | (u64)reg[a]<<15 | (u64)(op==O_NOT?0:reg[nb[i]])<<27;
      for(int k=0;k<5;k++) eb[el++]=(u8)(w>>(8*k));
      if(el>=3995){ sc3(1,fd,(i64)eb,el); el=0; }
    }
    ninstr++;
  }
  if(emit){ if(el) sc3(1,fd,(i64)eb,el); fclose_(fd); }
  return (int)ninstr;
}

static u64 rs;
static u64 xs(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
static void set_consts(int trial){
  for(int l=0;l<25;l++) KL[l]=0;
  KL[16]=0x8000000000000006UL;
  if(trial>0){ rs=0x9E3779B97F4A7C15UL*(u64)trial+1; for(int i=0;i<10;i++) xs();
    static const int fl[12]={0,2,3,5,7,8,10,12,13,15,11,14};
    for(int i=0;i<12;i++) KL[fl[i]]=xs(); }
}

static int work(int argc,char **argv);
/* The work runs in a forked child: its own signal struct starts with ru_maxrss 0, so the
   parent's wait4 rusage gives the worker's peak RSS without the high-water mark that Linux
   carries over from the shell across fork+execve. */
int cmain(long *sp){
  int argc=(int)sp[0]; char **argv=(char**)(sp+1);
  i64 pid=sc3(57,0,0,0);
  if(pid==0){ int rc=work(argc,argv); oflush(); sc3(60,rc,0,0); }
  if(pid<0) die("fork");
  struct { long ut[2], st[2]; long maxrss, rest[14]; } ru; int status=0;
  { i64 r; register i64 r10 __asm__("r10")=(i64)&ru; __asm__ volatile("syscall":"=a"(r):"a"(61L),"D"(pid),"S"((i64)&status),"d"(0L),"r"(r10):"rcx","r11","memory"); }
  int fd=(int)sc3(2,(i64)"ledger.txt",01|02000,0);
  for(int pass=0;pass<2;pass++){ fd_out= pass?1:fd;
    os("worker peak RSS (getrusage via wait4, worker forked from the 1-page parent) "); ou(ru.maxrss); os(" KiB = "); ou(ru.maxrss*1024); os(" bytes (limit 1048576)\n"); oflush(); }
  fclose_(fd);
  return ((status>>8)&255);
}
static int work(int argc,char **argv){
  int ntr= argc>1? atoi_(argv[1]) : 1; if(ntr<1) ntr=1;
  int t0= argc>2? atoi_(argv[2]) : 0;   /* gen <ntrials> [first trial]; the attack runs "gen 512" */
  int bestt=t0; long bestc=1L<<60;
  for(int t=t0;t<t0+ntr;t++){ set_consts(t); build(); dce(); long tot=cnt[1]+cnt[2]+cnt[3]+cnt[4];
    if(ntr>1){ os("trial "); ou(t); os(" ops "); ou(tot); oc('\n'); }
    if(tot<bestc){ bestc=tot; bestt=t; } }
  oflush();
  set_consts(bestt); build(); dce();
  long pre=cnt_emit;
  int ninstr=alloc_emit(1);
  long tot=cnt[1]+cnt[2]+cnt[3]+cnt[4];
  if(ninstr!=tot) die("instr count mismatch");
  struct { long ut[2], st[2]; long maxrss, ixrss, idrss, isrss, minflt, majflt, nswap, inblock, oublock, msgsnd, msgrcv, nsignals, nvcsw, nivcsw; } ru;
  sc3(98,0,(i64)&ru,0);
  /* VmHWM from /proc/self/status: peak RSS of this process image only (ru_maxrss on Linux
     can carry over the parent's high-water mark across fork+execve) */
  long hwm=-1; { static char st[4096]; int fd=(int)sc3(2,(i64)"/proc/self/status",0,0);
    if(fd>=0){ long n=sc3(0,fd,(i64)st,sizeof st-1); fclose_(fd); if(n>0){ st[n]=0;
      for(long i=0;i+6<n;i++) if(st[i]=='V'&&st[i+1]=='m'&&st[i+2]=='H'&&st[i+3]=='W'&&st[i+4]=='M'){ long j=i+6,v=0; while(st[j]==' '||st[j]=='	') j++; while(st[j]>='0'&&st[j]<='9') v=v*10+(st[j++]-'0'); hwm=v; break; } } } }
  /* meta.txt */
  fd_out=fopen_w("meta.txt");
  os("trial "); ou(bestt); oc('\n');
  for(int l=0;l<25;l++){ os("lane "); ou(l); oc(' '); ox(KL[l]); oc('\n'); }
  os("varlanes 1 6 4 9 ; lane11 = u0^u1^K11 ; lane14 = u2^u3^K14\n");
  os("pd "); for(int i=0;i<4;i++){ ox(PD[i]); oc(i<3?' ':'\n'); }
  os("ninstr "); ou(ninstr); oc('\n');
  oflush(); fclose_(fd_out);
  /* ledger.txt + stdout */
  for(int pass=0;pass<2;pass++){
    fd_out= pass? 1 : fopen_w("ledger.txt");
    os("LS1 step ledger (256 lanes, one chain step, 6 rounds)\n");
    os("XOR "); ou(cnt[O_XOR]); oc('\n');
    os("AND "); ou(cnt[O_AND]); oc('\n');
    os("OR  "); ou(cnt[O_OR]); oc('\n');
    os("NOT "); ou(cnt[O_NOT]); os("  (row complements chosen pre-DCE: "); ou(nnot_rows); os(")\n");
    os("LOAD 0\nSTORE 0\nTOTAL "); ou(tot); oc('\n');
    os("feed NOTs 0 (digest polarity folded into the chain function: F(u)=H(m(u))^PD)\n");
    os("nodes created pre-DCE "); ou(pre); os(" ; nodes "); ou(nn); os(" ; linear forms "); ou(nform); oc('\n');
    os("max live values "); ou(maxlive); os(" ; registers used "); ou(maxreg); os(" (limit 2304)\n");
    os("constants trial "); ou(bestt); os(" of "); ou(ntr); oc('\n');
    os("generator peak RSS (VmHWM, this process image) "); ou(hwm); os(" KiB = "); ou(hwm*1024); os(" bytes (limit 1048576)\n");
    os("getrusage ru_maxrss "); ou(ru.maxrss); os(" KiB (Linux carries the parent's high-water mark across fork+execve)\n");
    oflush(); if(!pass) fclose_(fd_out);
  }
  if(maxreg>NREG) return 2;
  return 0;
}
```

```c
/* selftest.c - checks the emitted LS1 straight line (prog.bin + meta.txt) against a plain
 * lane-wise Keccak reference written here (rounds 0..R-1, SHA3 padding, 136-byte rate).
 *   selftest kat            : prints "hexmsg digest24 digest6" for 300 deterministic messages
 *                             (lengths 0..299) for comparison with hashlib / the organizer reference
 *   selftest run [nbatch]   : nbatch x 256 random points, 4 chained steps each; counts mismatches
 *                             of the program output against F(u) = SHA3-256-r6(m(u)) ^ PD.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint64_t u64;

static const u64 RC[24]={0x0000000000000001ULL,0x0000000000008082ULL,0x800000000000808aULL,0x8000000080008000ULL,
 0x000000000000808bULL,0x0000000080000001ULL,0x8000000080008081ULL,0x8000000000008009ULL,0x000000000000008aULL,
 0x0000000000000088ULL,0x0000000080008009ULL,0x000000008000000aULL,0x000000008000808bULL,0x800000000000008bULL,
 0x8000000000008089ULL,0x8000000000008003ULL,0x8000000000008002ULL,0x8000000000000080ULL,0x000000000000800aULL,
 0x800000008000000aULL,0x8000000080008081ULL,0x8000000000008080ULL,0x0000000080000001ULL,0x8000000080008008ULL};
static const int RHO[25]={0,1,62,28,27, 36,44,6,55,20, 3,10,43,25,39, 41,45,15,21,8, 18,2,61,56,14}; /* index x+5y */
static u64 rotl(u64 v,int r){ return r? (v<<r)|(v>>(64-r)) : v; }

static void keccakf(u64 A[25], int rounds){
  for(int r=0;r<rounds;r++){
    u64 C[5],D[5],B[25];
    for(int x=0;x<5;x++) C[x]=A[x]^A[x+5]^A[x+10]^A[x+15]^A[x+20];
    for(int x=0;x<5;x++) D[x]=C[(x+4)%5]^rotl(C[(x+1)%5],1);
    for(int i=0;i<25;i++) A[i]^=D[i%5];
    for(int x=0;x<5;x++) for(int y=0;y<5;y++) B[y+5*((2*x+3*y)%5)]=rotl(A[x+5*y],RHO[x+5*y]);
    for(int y=0;y<5;y++) for(int x=0;x<5;x++) A[x+5*y]=B[x+5*y]^((~B[(x+1)%5+5*y])&B[(x+2)%5+5*y]);
    A[0]^=RC[r];
  }
}
static void sha3_256r(const uint8_t *m, size_t len, int rounds, uint8_t out[32]){
  u64 A[25]; memset(A,0,sizeof A);
  uint8_t blk[136]; size_t off=0;
  for(;;){
    size_t rem=len-off;
    if(rem>=136){ memcpy(blk,m+off,136); off+=136; }
    else { memset(blk,0,136); memcpy(blk,m+off,rem); blk[rem]^=0x06; blk[135]^=0x80; off=len+1; }
    for(int i=0;i<17;i++){ u64 w=0; for(int k=0;k<8;k++) w|=(u64)blk[8*i+k]<<(8*k); A[i]^=w; }
    keccakf(A,rounds);
    if(off>len) break;
  }
  for(int i=0;i<32;i++) out[i]=(uint8_t)(A[i/8]>>(8*(i%8)));
}

static u64 KL[25], PD[4]; static long ninstr;
static uint8_t *prog;
static void load(void){
  FILE *f=fopen("meta.txt","r"); if(!f){ perror("meta.txt"); exit(2); }
  char line[512];
  while(fgets(line,sizeof line,f)){
    int l; unsigned long long v,a,b,c,d;
    if(sscanf(line,"lane %d %llx",&l,&v)==2) KL[l]=v;
    else if(sscanf(line,"pd %llx %llx %llx %llx",&a,&b,&c,&d)==4){ PD[0]=a;PD[1]=b;PD[2]=c;PD[3]=d; }
    else if(sscanf(line,"ninstr %ld",&ninstr)==1){}
  }
  fclose(f);
  f=fopen("prog.bin","rb"); if(!f){ perror("prog.bin"); exit(2); }
  prog=malloc(ninstr*5); if(fread(prog,5,ninstr,f)!=(size_t)ninstr){ fprintf(stderr,"short prog\n"); exit(2); } fclose(f);
}
/* message m(u): 128 bytes = lanes 0..15 */
static void msg_of(const u64 u[4], uint8_t m[128]){
  u64 L[16]; for(int i=0;i<16;i++) L[i]=KL[i];
  L[1]=u[0]; L[6]=u[1]; L[11]=u[0]^u[1]^KL[11];
  L[4]=u[2]; L[9]=u[3]; L[14]=u[2]^u[3]^KL[14];
  for(int i=0;i<128;i++) m[i]=(uint8_t)(L[i/8]>>(8*(i%8)));
}
static void Fref(const u64 u[4], u64 o[4]){
  uint8_t m[128], d[32]; msg_of(u,m); sha3_256r(m,128,6,d);
  for(int i=0;i<4;i++){ u64 w=0; for(int k=0;k<8;k++) w|=(u64)d[8*i+k]<<(8*k); o[i]=w^PD[i]; }
}
typedef struct { u64 w[4]; } W256;
static W256 R[2304];
static void run_prog(void){
  const uint8_t *p=prog;
  for(long i=0;i<ninstr;i++,p+=5){
    u64 w=(u64)p[0]|(u64)p[1]<<8|(u64)p[2]<<16|(u64)p[3]<<24|(u64)p[4]<<32;
    int op=w&7, d=(w>>3)&4095, a=(w>>15)&4095, b=(w>>27)&4095; W256 t;
    for(int k=0;k<4;k++){ u64 x=R[a].w[k], y=R[b].w[k];
      t.w[k]= op==0? x^y : op==1? x&y : op==2? x|y : ~x; }
    if(op>3 || d>=2304){ fprintf(stderr,"bad instr %ld\n",i); exit(3); }
    R[d]=t;
  }
}
static u64 rs=0x0123456789abcdefULL;
static u64 xr(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }

int main(int argc,char **argv){
  if(argc>1 && !strcmp(argv[1],"kat")){
    for(int len=0;len<300;len++){
      uint8_t m[300],d24[32],d6[32]; for(int i=0;i<len;i++) m[i]=(uint8_t)xr();
      sha3_256r(m,len,24,d24); sha3_256r(m,len,6,d6);
      for(int i=0;i<len;i++) printf("%02x",m[i]); printf(" ");
      for(int i=0;i<32;i++) printf("%02x",d24[i]); printf(" ");
      for(int i=0;i<32;i++) printf("%02x",d6[i]); printf("\n");
    }
    return 0;
  }
  int nb= argc>2? atoi(argv[2]) : 2;
  if(argc>3) rs=strtoull(argv[3],0,0);
  load();
  long mism=0, evals=0;
  for(int bt=0;bt<nb;bt++){
    static u64 U[256][4];
    for(int t=0;t<256;t++) for(int i=0;i<4;i++) U[t][i]=xr();
    for(int j=0;j<256;j++) for(int k=0;k<4;k++){ u64 w=0; for(int b=0;b<64;b++){ int t=64*k+b; w|=((U[t][j>>6]>>(j&63))&1)<<b; } R[j].w[k]=w; }
    for(int step=0;step<4;step++){
      run_prog();
      for(int t=0;t<256;t++){
        u64 o[4], g[4]={0,0,0,0}; Fref(U[t],o);
        for(int j=0;j<256;j++) g[j>>6]|=((R[j].w[t>>6]>>(t&63))&1)<<(j&63);
        if(memcmp(o,g,32)) { if(mism<5) fprintf(stderr,"mismatch batch %d step %d trail %d\n",bt,step,t); mism++; }
        evals++;
        memcpy(U[t],o,32);   /* chain on the reference value */
      }
    }
  }
  printf("selftest: %ld chained evaluations (%d batches x 256 trails x 4 steps), %ld mismatches, %ld instructions\n",evals,nb,mism,ninstr);
  return mism?1:0;
}
```

## Appendix C. Programs of the measured checks (Sections 7 and 8)

hrand_test.c (Section 7.2, tests A to D), proj_test.c (the proj-w256 trial at scale; it shares the loader and executor of hrand_test.c, of which only main differs and is shown), ideal_rho.py (the ideal-function control of rho-w22), spill.py (the register rows of Section 8).

```c
/* hrand_test.c - measured checks of the premise H_rand for the LS1 chain function F (prog.bin + meta.txt).
 * Executes the emitted straight line (256 lanes per step) and counts, among M = 2^24 evaluations,
 * the pairs of images that agree on a 32-bit window (low bits 0..31, bits 128..159, top bits 224..255):
 *   A: uniform random inputs (independent images expected: C(M,2)/2^32 pairs, Poisson)
 *   B: structured inputs R + i, i < M (the start pattern of the search: consecutive integers)
 *   C: iterates: 256 chains of 65,536 chained steps from random starts (the points a walk evaluates)
 * and D: single-bit input differences: for each of the 256 input bits j, 4,096 random u, the count of output bit k
 *   flipping in F(u) ^ F(u ^ e_j), for all 65,536 (j,k) cells; reports the largest |z| (binomial 4096, 1/2).
 * Usage: hrand_test [seed]   (reads prog.bin and meta.txt from the current directory) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
typedef uint64_t u64;
static long ninstr; static uint8_t *prog;
typedef struct { u64 w[4]; } W256;
static W256 R[2304];
static void load(void){
  FILE *f=fopen("meta.txt","r"); char line[512];
  while(fgets(line,sizeof line,f)) sscanf(line,"ninstr %ld",&ninstr);
  fclose(f); f=fopen("prog.bin","rb"); prog=malloc(ninstr*5);
  if(fread(prog,5,ninstr,f)!=(size_t)ninstr) exit(2); fclose(f);
}
static void run_prog(void){
  const uint8_t *p=prog;
  for(long i=0;i<ninstr;i++,p+=5){
    u64 w=(u64)p[0]|(u64)p[1]<<8|(u64)p[2]<<16|(u64)p[3]<<24|(u64)p[4]<<32;
    int op=w&7, d=(w>>3)&4095, a=(w>>15)&4095, b=(w>>27)&4095;
    W256 *x=&R[a],*y=&R[b],t;
    switch(op){ case 0: for(int k=0;k<4;k++) t.w[k]=x->w[k]^y->w[k]; break;
                case 1: for(int k=0;k<4;k++) t.w[k]=x->w[k]&y->w[k]; break;
                case 2: for(int k=0;k<4;k++) t.w[k]=x->w[k]|y->w[k]; break;
                default: for(int k=0;k<4;k++) t.w[k]=~x->w[k]; }
    R[d]=t;
  }
}
static u64 sm;
static u64 rnd(void){ u64 z=(sm+=0x9E3779B97F4A7C15ULL); z=(z^(z>>30))*0xBF58476D1CE4E5B9ULL; z=(z^(z>>27))*0x94D049BB133111EBULL; return z^(z>>31); }
/* set lane t (0..255) of the 256 input planes to point u[4] */
static void set_point(int t,const u64 u[4]){ for(int j=0;j<256;j++){ u64 bit=(u[j>>6]>>(j&63))&1; u64 m=1ULL<<(t&63); R[j].w[t>>6]=(R[j].w[t>>6]&~m)|(bit<<(t&63)); } }
static void get_point(int t,u64 o[4]){ o[0]=o[1]=o[2]=o[3]=0; for(int j=0;j<256;j++) o[j>>6]|=((R[j].w[t>>6]>>(t&63))&1)<<(j&63); }
static uint32_t window(int t,int lo){ uint32_t v=0; for(int j=0;j<32;j++) v|=(uint32_t)((R[lo+j].w[t>>6]>>(t&63))&1)<<j; return v; }
static int cmpu(const void*a,const void*b){ uint32_t x=*(const uint32_t*)a,y=*(const uint32_t*)b; return x<y?-1:x>y; }
static double pairs(uint32_t *k,long M){ qsort(k,M,4,cmpu); double p=0; long i=0; while(i<M){ long j=i; while(j<M&&k[j]==k[i]) j++; double c=j-i; p+=c*(c-1)/2; i=j; } return p; }
#define LM 24
static uint32_t *K0,*K1,*K2;
static void report(const char *name,long M){
  double E=(double)M*(M-1)/2/4294967296.0;
  double p0=pairs(K0,M),p1=pairs(K1,M),p2=pairs(K2,M);
  printf("%s: M=2^%d, pairs agreeing on 32 bits: low %.0f, mid %.0f, top %.0f; expected %.1f each (sd %.1f); ratios %.4f %.4f %.4f; z %.2f %.2f %.2f\n",
    name,LM,p0,p1,p2,E,sqrt(E),p0/E,p1/E,p2/E,(p0-E)/sqrt(E),(p1-E)/sqrt(E),(p2-E)/sqrt(E));
}
int main(int argc,char**argv){
  sm= argc>1? strtoull(argv[1],0,0) : 0x15c0ffee;
  load();
  long M=1L<<LM, S=M/256;
  K0=malloc(M*4); K1=malloc(M*4); K2=malloc(M*4);
  /* A: uniform random inputs */
  for(long s=0;s<S;s++){
    for(int j=0;j<256;j++) for(int k=0;k<4;k++) R[j].w[k]=rnd();
    run_prog();
    for(int t=0;t<256;t++){ long e=s*256+t; K0[e]=window(t,0); K1[e]=window(t,128); K2[e]=window(t,224); }
  }
  report("A uniform inputs",M);
  /* B: consecutive inputs R0 + i */
  u64 R0[4]={rnd(),rnd(),rnd(),rnd()};
  for(long s=0;s<S;s++){
    for(int t=0;t<256;t++){ u64 i=(u64)(s*256+t), u[4]; u[0]=R0[0]+i; u64 c=u[0]<R0[0]; for(int k=1;k<4;k++){ u[k]=R0[k]+c; c=c&&u[k]==0; } set_point(t,u); }
    run_prog();
    for(int t=0;t<256;t++){ long e=s*256+t; K0[e]=window(t,0); K1[e]=window(t,128); K2[e]=window(t,224); }
  }
  report("B consecutive inputs R+i",M);
  /* C: iterates of 256 chains */
  for(int j=0;j<256;j++) for(int k=0;k<4;k++) R[j].w[k]=rnd();
  for(long s=0;s<S;s++){
    run_prog();
    for(int t=0;t<256;t++){ long e=s*256+t; K0[e]=window(t,0); K1[e]=window(t,128); K2[e]=window(t,224); }
  }
  report("C chained iterates (256 chains x 65536 steps)",M);
  /* D: single-bit input differences */
  static uint32_t cnt[256][256]; memset(cnt,0,sizeof cnt);
  int NS=4096;
  for(int j=0;j<256;j++){
    for(int s=0;s<NS/128;s++){
      u64 u[128][4];
      for(int t=0;t<128;t++){ for(int k=0;k<4;k++) u[t][k]=rnd(); u64 v[4]; memcpy(v,u[t],32); set_point(t,v); v[j>>6]^=1ULL<<(j&63); set_point(128+t,v); }
      run_prog();
      for(int t=0;t<128;t++){ u64 a[4],b[4]; get_point(t,a); get_point(128+t,b); for(int k=0;k<256;k++) cnt[j][k]+=((a[k>>6]^b[k>>6])>>(k&63))&1; }
    }
  }
  double zmax=0; int jm=0,km=0; double sum=0;
  for(int j=0;j<256;j++) for(int k=0;k<256;k++){ double z=(cnt[j][k]-NS/2.0)/sqrt(NS/4.0); sum+=z*z; if(fabs(z)>zmax){ zmax=fabs(z); jm=j; km=k; } }
  printf("D single-bit differences: 65536 cells x %d pairs, max |z| %.2f at input bit %d output bit %d (largest of 65536 normal cells is about 4.4); mean z^2 %.4f (expected 1)\n",NS,zmax,jm,km,sum/65536);
  return 0;
}
```

```c
/* proj_test: the proj-w256 trial at scale: NT trials of 256 random points and 8 chained full-width steps each;
   a trial succeeds when two of its 2,048 evaluated inputs have images agreeing on the 22 low bits. */
int main(int argc,char**argv){
  sm= argc>1? strtoull(argv[1],0,0) : 0x9e1f;
  long NT= argc>2? atol(argv[2]) : 16384;
  load();
  static uint32_t key[2048]; long succ=0;
  for(long tr=0;tr<NT;tr++){
    for(int j=0;j<256;j++) for(int k=0;k<4;k++) R[j].w[k]=rnd();
    for(int s=0;s<8;s++){ run_prog(); for(int t=0;t<256;t++){ uint32_t v=0; for(int j=0;j<22;j++) v|=(uint32_t)((R[j].w[t>>6]>>(t&63))&1)<<j; key[s*256+t]=v; } }
    qsort(key,2048,4,cmpu); int hit=0; for(int i=1;i<2048;i++) if(key[i]==key[i-1]){ hit=1; break; }
    succ+=hit;
  }
  double p=0.39337; /* 1-prod_{i<2048}(1-i/2^22) */
  printf("proj at scale: %ld trials, %ld successes = %.4f; model %.4f; z %.2f\n",NT,succ,(double)succ/NT,p,(succ-NT*p)/sqrt(NT*p*(1-p)));
  return 0;
}
```

```python
# Ideal-function control for rho-w22 (our own run, not organizer): the search of ls1.py rho_w with the same parameters
# (W=22, H=4, LC=128, U=3000, TB=400, 256 walks, starts rho+i, restarts, same event order), f replaced by a lazily
# sampled uniform random function on 22 bits. Prints the mean and quantiles of the steps to the first replayed pair.
import random, sys
W, H, LC, U, TB = 22, 4, 128, 3000, 400
mask = (1 << W) - 1


def trial(rng):
    fmap = {}
    def f(x):
        v = fmap.get(x)
        if v is None: v = fmap[x] = rng.getrandbits(W)
        return v
    c0 = 0
    while True:                                  # attempts
        rho = rng.getrandbits(W)
        pts = [(rho + l) & mask for l in range(256)]
        lid = list(range(256)); lst = [c0] * 256; nid = 256; table = {}
        c = c0
        while c - c0 < TB:
            c += 1
            pts = [f(x) for x in pts]
            events = sorted([(l, 1) for l in range(256) if pts[l] & ((1 << H) - 1) == 0] +
                            [(l, 2) for l in range(256) if c - lst[l] == LC and pts[l] & ((1 << H) - 1) != 0])
            for l, kind in events:
                if kind == 1:
                    x, ln = pts[l], c - lst[l]
                    if x in table:
                        ida, la = table[x]
                        if ida != lid[l]:
                            a, b = (rho + ida) & mask, (rho + lid[l]) & mask
                            for _ in range(abs(la - ln)):
                                if la > ln: a = f(a)
                                else: b = f(b)
                            if a != b:
                                for _ in range(min(la, ln) + 1):
                                    if f(a) == f(b): return c
                                    a, b = f(a), f(b)
                    else:
                        table[x] = (lid[l], ln)
                if nid >= U: break
                lid[l] = nid; lst[l] = c; pts[l] = (rho + nid) & mask; nid += 1
            if nid >= U: break
        c0 = c


rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 7)
n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
st = sorted(trial(rng) for _ in range(n))
m = sum(st) / n; sd = (sum((v - m) ** 2 for v in st) / (n - 1)) ** 0.5
print("ideal-function control: %d trials, mean steps %.3f (sd %.2f), median %d, 90%% %d, max %d" % (n, m, sd, st[n // 2], st[9 * n // 10], st[-1]))
```

```python
# Register-file sensitivity: the same straight line (prog.bin) executed on a machine with only Rk registers.
# Values live in memory when evicted; Belady (furthest next use) eviction; a store is charged only when an evicted
# value is used again later (a dead value is dropped), a load when an operand is not in a register.
# The 256 input planes start in memory and the 256 digest planes must end in memory (stored at the end if resident).
import sys, heapq
data = open(sys.argv[1] if len(sys.argv) > 1 else "prog.bin", "rb").read()
P = []
for i in range(0, len(data), 5):
    w = int.from_bytes(data[i:i + 5], "little")
    c, d, a, b = w & 7, (w >> 3) & 4095, (w >> 15) & 4095, (w >> 27) & 4095
    P.append((c, d, (a,) if c == 3 else (a, b)))
n = len(P)
# value ids: (register, version); version increases each time the register is written
ver = [0] * 4096
uses = []                 # per instruction: operand value ids
defs = []
for c, d, srcs in P:
    uses.append(tuple((r, ver[r]) for r in srcs))
    ver[d] += 1
    defs.append((d, ver[d]))
outs = {(j, ver[j]) for j in range(256)}
INF = 10 ** 9
nextuse = {}
nu_list = [None] * n
for i in range(n - 1, -1, -1):
    d = defs[i]
    nu_list[i] = [nextuse.get(v, INF) for v in uses[i]] , nextuse.get(d, INF)
    nextuse.pop(d, None)
    for v in uses[i]:
        nextuse[v] = i
first_use = dict(nextuse)  # inputs (version 0)

def run(Rk):
    resident = {}         # value -> next use
    heap = []
    inmem = set((j, 0) for j in range(256))
    loads = stores = 0
    def evict(protect):
        nonlocal stores
        aside = []
        while True:
            nu, v = heapq.heappop(heap)
            nu = -nu
            if v not in resident or resident[v] != nu:
                continue                      # stale heap entry
            if v in protect:
                aside.append((-nu, v)); continue
            del resident[v]
            if (nu < INF or v in outs) and v not in inmem:
                stores += 1; inmem.add(v)
            for x in aside: heapq.heappush(heap, x)
            return
    for i in range(n):
        (unu, dnu) = nu_list[i]
        ops = uses[i]
        for v, nu in zip(ops, unu):
            if v not in resident:
                if len(resident) >= Rk: evict(set(ops))
                loads += 1
                resident[v] = nu; heapq.heappush(heap, (-nu, v))
            else:
                resident[v] = nu; heapq.heappush(heap, (-nu, v))
        for v, nu in zip(ops, unu):
            if nu == INF and v not in outs and v in resident:
                del resident[v]
        d = defs[i]
        if len(resident) >= Rk: evict(set())
        resident[d] = dnu; heapq.heappush(heap, (-dnu, d))
    for v in outs:
        if v in resident and v not in inmem: stores += 1
    return loads, stores

for Rk in [int(x) for x in sys.argv[2:]] or [1024, 512, 256, 64]:
    l, s = run(Rk)
    print("registers %4d: loads %6d stores %6d -> step %d + %d = %d ops" % (Rk, l, s, n, l + s, n + l + s))
```
