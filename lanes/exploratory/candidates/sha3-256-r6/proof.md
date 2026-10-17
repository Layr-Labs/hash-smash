# SHA3-256 with 6 prefix rounds: distinguished-point collision search with an annihilating linear-structure message embedding, a 26,367-operation bit-sliced step and a table of four records per word, time_log2 124.02556

## 1. Claim

Target `sha3-256-r6-prefix-v1`: SHA3-256 (FIPS 202) with Keccak-f rounds 0 to 5 in the single permutation call, zero initial state, rate 136 bytes, suffix 0x06 with pad10*1, and the full 256-bit digest. The algorithm outputs two distinct 128-byte one-block messages with equal complete digests (an ordinary collision).

| Quantity | Value |
|---|---|
| time_log2 (collision-frontier-v5, unit 1626 word operations, rounded up) | 124.02556 (Sections 4 and 5, certificate in Appendix A) |
| memory | at most 1,044,294 bytes <= 2^20 (margin 4,282 bytes), memory_log2_bytes = 20 (Section 6) |
| score S = time_log2 + max(0, memory_log2 - 20) | 124.02556 |
| success probability | at least 0.39 for one attempt, under the premise H_rand (Section 5) |
| preprocessing | one run of the generator, `gen 32` (Section 3.6), charged 33 x 2^32 + 32 x 2^10 = 141,733,953,536 word operations inside N; preprocessing_log2 = 27; no advice |

The method is a distinguished-point parallel collision search (van Oorschot-Wiener) on a chain function F, with 256 walks per step. It combines the annihilating linear-structure constant family and lookahead coordinate-descent step generator of our entry `7d11f600` (124.13884) with the 10-gate chi rows, four-record-per-word table packing, rational distinguished-point threshold, uncut Stage-1 / replay-cap analysis (F6), and emitted non-straight-line machine code (`other4.py`) of Jbenisek's entry `18d9298d` (124.07568):

1. **Annihilating linear-structure message embedding (from `7d11f600`, building on `bc3e3eef` and Guo-Liu-Song 2016).** The 256-bit point u is placed in columns x = 1 (lanes 1, 11, 6) and x = 4 (lanes 9, 14, 4), and the remaining constant message lanes are chosen from a 32-element algebraic family so that the chi neighbors of the six variable lanes after round-0 theta, rho and pi are all-zero or all-one constants that annihilate quadratic cross-terms and leave 14 of the 25 lanes constant after round-0 chi. This reduces the number of distinct affine forms tracked through round-0 chi and round-1 theta to 1,088 (versus 1,855 in `18d9298d`).
2. **Step program (26,367 register operations, -938 vs `18d9298d`'s 27,305 and -1,024 vs `7d11f600`'s 27,391).** One step of the 256 walks is a bit-sliced straight line built on the step design of jungjipdo's `67f781f8` (theta evaluated lazily per chi row, per-row complement subsets, dead-code elimination, last-use register allocation, the digest written over the input, a declared register file and a 5-byte encoding). In our generator `gen.c` (Appendix B), the per-row candidate table unifies Jbenisek's **10-gate chi row** (`18d9298d`, where one output `bj` reads the adjacent finished output `out[(bj+1) mod 5]` in place of `b[(bj+1) mod 5]`) and both two-operation mixed-polarity AND forms (`A xor (A and B)` with output polarity 0 and `(not A) or B` with output polarity 1) with `7d11f600`'s NOT-gate reuse tracking (`not_uses` and `has_cons`) and coordinate-descent lookahead (`single-row`, `5-row same-slice`, `same-slice pair`, and `adjacent-slice pair` passes) scored against an exact bit-sliced evaluation of the next round's 10-gate chi+NOT cost (`eval_phi`). Across the 32 algebraic trials (`gen 32`), trial 27 achieves 26,367 instructions (`1,213` 10-gate rows) with `preprocessing_log2 = 27` (9 bits lower preprocessing than `18d9298d`'s 36).
3. **Search and packed table (from `18d9298d`, building on `2d74a370` and `2acfdbee`).** Lockstep walks with a restart on each distinguished point, a rational distinguished-point threshold `x < 704 x 2^135` (`theta = 704 x 2^-121`), no trail cut in Stage 1 (only the replay refuses trails of more than `LRC` evaluations, bounded by failure term `F6`), four 64-bit records per 256-bit table word (`S = 23,088` words, `U = 92,352` trails, `Tb = 535,677,142 x 2^91` steps), and the complete assembled 2,704-instruction non-straight-line program (`other4.py`, Appendix D) whose every operation is counted and tested by execution (`other4_test.py`).

Three declarations are made in `claim.json`: `H_rand` (Section 5) is the score-critical premise on the function; `H_reg` (register file) and `H_code` (code-memory encoding) are declared machine conventions of the cost model, role supporting, in Section 3.5, with priced alternatives in Section 8.

## 2. The function F and the encoding

Let u be a 256-bit point with little-endian 64-bit lanes u0, u1, u2, u3. The message m(u) has 128 bytes, the 16 lanes 0 to 15 of the absorbed state (lane index x + 5y):

- lane 1 = u0 xor K1, lane 11 = u1 xor K11, lane 6 = u0 xor u1 xor K6 (column x = 1, rows y = 0, 2, 1);
- lane 9 = u2 xor K9, lane 14 = u3 xor K14, lane 4 = u2 xor u3 xor K4 (column x = 4, rows y = 1, 2, 0);
- every other lane l in 0..15 holds the constant K_l (below).

With the SHA3 padding, byte 128 is 0x06 and byte 135 is 0x80: one absorbed block, lane 16 = 0x8000000000000006, lanes 17 to 24 zero. Rounds 0 to 5 are applied and the digest is lanes 0 to 3 of the result (32 bytes). Define

    F(u) = SHA3-256-r6(m(u)) xor PD

where PD is a fixed 256-bit mask (the polarity of the program's digest planes, Section 3.3). The map u -> m(u) is injective (lanes 1, 11, 9, 14 recover u0, u1, u2, u3 by XOR with K1, K11, K9, K14), so F(a) = F(b) with a != b gives two distinct messages m(a), m(b) with equal complete digests. XOR with a fixed mask is a bijection of the range, so F is a fixed function from 256 bits to 256 bits like the plain digest map.

Constants (hexadecimal). The generator chose them as trial 27 of the 32 algebraic constant sets (`W = ffffffffffffffff, r0 = ffffffffffffffff, r1 = 0, r2 = ffffffffffffffff, r3 = ffffffffffffffff`), the one with the fewest operations; the selection run `gen 32` is charged in N as preprocessing (Section 3.6):

```
K0  0000000000000000  K1  ffffffffffffffff  K2  ffffffffffffffff  K3  0000000000000000
K4  ffffffffffffffff  K5  ffffffffffffffff  K6  8000000000000006  K7  0000000000000000
K8  0000000000000000  K9  ffffffffffffffff  K10 ffffffffffffffff  K11 0000000000000000
K12 0000000000000000  K13 ffffffffffffffff  K14 ffffffffffffffff  K15 ffffffffffffffff
PD (lanes 0..3) 78ffacdbe5536f38 26601084ceb039a0 830053249aac10c6 05004320100c0046
```

**Why round 0 is affine and annihilates 14 of 25 lanes.**
- *Theta of round 0.* The column sums of columns 1 and 4 are constants: (u0 xor K1) xor (u0 xor u1 xor K6) xor (u1 xor K11) xor lane 16 xor lane 21 = K1 xor K6 xor K11 xor 0x8000000000000006 = 0, and (u2 xor u3 xor K4) xor (u2 xor K9) xor (u3 xor K14) xor lane 19 xor lane 24 = K4 xor K9 xor K14 = ffffffffffffffff. With K0 = 0 and K5 = K10 = K15 = ffffffffffffffff, the column sums C[0..4] are all constants, so theta adds only constants to every lane.
- *Chi of round 0.* After rho and pi, the six variable lanes land in B[6], B[7], B[16], B[14], B[18], B[24], where no two are adjacent inside a chi row unless one neighbor is held to an annihilating constant (0 for an AND factor `B[X+2]`, all-ones for a negated factor `B[X+1]`). Each product of chi has at least one constant factor, so round-0 chi is strictly affine in u and 14 of the 25 output lanes of round 0 are constants.
- *Round 1 theta.* It is a linear map of affine values, so it is affine too, requiring only 1,088 distinct affine forms across round 0 and round-1 theta.

The generator tracks each value as a GF(2) affine form in the 256 input bits as long as it is affine, emits an operation only when the form is new, and stops tracking forms at the first nonlinear operation (chi of round 1). The search uses no algebraic property: F is only evaluated.

## 3. One step of 256 walks: the straight line

### 3.1 Planes, polarity, gates

A batch is 256 walks. Plane (lane, z) is one 256-bit word whose bit t is bit z of that lane for walk t. The rotations of rho and the moves of pi rename planes and cost nothing.

Each value is held as a register and a polarity p: the logical value is the register word xor p, all-ones or zero. NOT and XOR with a constant flip p for free; constants are folded and never stored. The operations, each one word operation, are:
- XOR: one operation;
- logical a AND b: one AND when both polarities are 0, one OR with output polarity 1 when both are 1, and two operations otherwise, either `A xor (A and B)` (output polarity 0, `sel = 0`) or `(not A) or B` (output polarity 1, `sel = 1`);
- NOT: one operation, used for the row and feed complements of 3.2.

Equal operands fold, and a binary operation on the same pair of registers is emitted once (hash-consing).

### 3.2 Rounds, 10-gate chi rows and lookahead optimization

For each round r = 0..5, with the round constant of the profile:

1. Column sums C[x][z] (the five planes of the column, folded) and D[x][z] = C[x-1][z] xor C[x+1][z-1], computed slice by slice with C[.][63] first, so that few C values are live at once.
2. The chi rows, in order Y = 0..4 and z = 0..63. Each row XORs D into its five inputs b[X] = A[x][y][z - rho(x,y)] xor D[x][z - rho(x,y)] (x = 3Y + X mod 5, y = X) when the row is computed (lazy theta).
3. **Row decision (`(s, f, selm, bj)` with 10-gate chi rows, NOT reuse and 1-round lookahead).**
   - *10-gate chi row (`18d9298d`).* chi computes `out[X] = b[X] xor ((not b[X+1]) and b[X+2])`. Wherever `b[k+1] = 1`, `out[k] = b[k] xor ((not 1) and b[k+2]) = b[k]`; wherever `b[k+1] = 0`, both sides of
     
         (not out[k]) and b[k+1] = (not b[k]) and b[k+1]
     
     are 0. Therefore, for at most one index `bj in 0..4` per row (with `k = (bj + 1) mod 5`), the quadratic term of output `bj` may read the finished output `out[k]` of the same row in place of `b[k]`. Because `out[k]` has the polarity given to it by its own feed and quadratic term, the odd five-cycle of equal polarities (which forces at least one two-operation term in a plain 5-bit chi row) is broken, allowing the five quadratic terms of the row to be computed in 5 single-gate AND/OR operations plus 5 feed XORs (10 gates total).
   - *Decoupled complements and free polarities with NOT reuse.* Before chi, the generator may complement a subset `s` of the five inputs for the quadratic terms, may select a subset `f` of the five inputs to use in complemented form for the linear feed `b[X] xor t`, and may select a mask `selm` of two-operation terms to emit as `(not A) or B` (polarity 1) instead of `A xor (A and B)` (polarity 0). A NOT operation on `b[X]` is free whenever `~b[X]` is already available (`has_cons(O_NOT, b[X], 0)` or `not_uses[b[X]] > 0`), and a two-operation term flips its output polarity at zero extra gate cost via `selm`. In `build_row_sinfo` and `get_row_cands_raw` (Appendix B), for each of the 32 output polarity masks `pm in 0..31`, the generator finds the minimum-cost choice `(s, f, selm, bj)` given the currently available free NOTs `avail`.
   - *Coordinate-descent lookahead (`r = 1..4`).* Starting from the greedy minimum-cost choice in each row, rounds `r = 1..4` refine the row choices `(s, f, selm, bj)` across all 320 rows of the round by coordinate descent (single-row updates, 5-row same-slice updates at each `z`, same-slice row pairs, and adjacent-slice `(z, z+1)` row pairs) minimizing the sum of the current round's row+NOT cost and the exact bit-sliced next-round chi+NOT score `eval_phi` (closed-form 64-bit SWAR evaluation of the next round's 320 rows in `r = 1..3`, and of the 64 4-output rows of round 5 in `r = 4`). After selecting `chosen[Y][z]`, the generator rewinds the node store to the post-theta state and emits the round lazily row by row in order `Y = 0..4, z = 0..63`. In the selected build (trial 27), `1,213` chi rows use the 10-gate form.
4. iota flips the polarity of the lane-0 planes where the round constant has a 1.

**The last round (round 5)** computes only row Y = 0 and the outputs X = 0..3 (the digest lanes); the 10-gate form is used there when both outputs `bj` and `(bj + 1) mod 5` are among `0..3`.

**Dead-code elimination** removes every operation on which no digest plane depends.

### 3.3 Chain feed

Digest plane j is written into register j, which held input plane j. The physical digest word is the next point: F folds the digest polarity PD into the function (Section 2). There is no copy and no NOT between steps.

### 3.4 The ledger of one step

Printed by the generator (`gen 32`, Appendix B):

| operation | count |
|---|---:|
| XOR | 19,052 |
| AND | 3,743 |
| OR | 2,913 |
| NOT | 659 |
| load / store | 0 / 0 |
| **total** | **26,367** |

That is 103.00 word operations per evaluation of F, 0.0633 of the reference cost 1626 per evaluation.

### 3.5 Registers and code encoding (machine conventions H_reg and H_code)

**Registers.** Values are allocated to registers in program order, and a register is freed at the last use of its value. Input and digest plane j use register j; the allocator never gives register j < 256 to a value that would still be live when digest plane j is written. The program uses registers 0 to 2,180 (2,181 registers, at most 1,925 values live at once). The search keeps its state in registers 2,181 to 2,190 (the step counter, a spare word, the next trail number, rho, the hit counter, the all-ones word, the prefilter word, two return addresses, a zero word); register 2,191 is spare. The handlers of Section 4.3 use registers 256 to 2,180 as temporaries: their contents are dead between two steps, because every straight-line value is defined before it is used and only the planes 0 to 255 are carried from one step to the next. The step has no loads or stores.

**H_reg (declared machine convention, role supporting in claim.json).** The cost model and the target profile fix no register count. This package uses the 256-bit word RAM of collision-frontier-v5 with a declared file of 2,192 registers of 256 bits. An operation on register operands costs one word operation, with no load or store; every load and store of the other code is a charged word operation (Section 4). The file's 70,144 bytes are counted as memory (Section 6). This is the convention of `67f781f8` (2,304 registers), `bc3e3eef`, `7d11f600` and `18d9298d`. Section 8 prices the alternatives: 1,024 registers 124.475, 512 registers 124.690, 256 registers 124.847, 64 registers 125.014.

**H_code (declared code-memory charging convention, role supporting in claim.json).** The cost model and the target profile fix no code encoding.
- **Encoding.** Each straight-line instruction has only register operands. It is stored in 5 bytes: a 3-bit opcode (0 XOR, 1 AND, 2 OR, 3 NOT) and three 12-bit register numbers (destination, a, b), 39 bits in little-endian order. The memory table charges the straight line at 5 bytes per instruction.
- **Other code.** All other code (setup, loop control, hit handler, DP handler, restart, replay, output) is real code of one machine, written out in Appendix D and assembled: 2,704 instructions of 32 bytes (86,528 bytes), measured from the assembled file. An instruction has an opcode byte, three 16-bit register numbers and a 192-bit immediate. Each costs one word operation, except PERM, which applies the 6-round permutation to the 1,600-bit state held in seven registers and costs one unit (1626 operations), the cost model's own price of one permutation.
- **Time ledger.** Each instruction is charged as the one word operation it performs; there is no separate charge for fetching or decoding.
- **Sensitivity.** Section 8 prices a 32-byte-per-instruction straight line (about 124.71).

The straight-line program file `prog.bin` is 131,835 bytes. Its SHA-256 is `8c2b8795a9656a0530eb055f71c455e8dbcae1689a63736ad8e3500f4fafd0cc`.

### 3.6 Generation and constant selection (preprocessing)

The preprocessing is one run of the selection program `gen 32` (Appendix B), a C program with static arrays only (`MAXN = 32768`). For each of the 32 algebraic constant sets (`t = 0..31`, parameterized by the 5 bits `(W, r0, r1, r2, r3)`):
1. it builds the straight line (`26,623` symbolic nodes, the 10-gate + lookahead row coordinate descent, dead-code elimination) and counts its operations (trial 0 gives `26,422`; the lowest is trial 27 at `26,367`);
2. it rebuilds the winning trial (trial 27), allocates the registers, and writes `prog.bin`, `meta.txt` and `ledger.txt`. `gen 1 27` writes the identical file byte for byte.

- **Time.** The ledger charges each of the 33 builds 2^32 word operations, and each of the 32 trials a further 2^10 for its constants, counts, comparison and printed line: `PRE = 33 x 2^32 + 32 x 2^10 = 141,733,953,536` word operations, part of N (Section 4.4). Since `2^26 < PRE / 1626 <= 2^27`, `preprocessing_log2` is declared as 27. The run of 32 trial builds and one rebuild takes 3.2 s of user time on one core.
- **Memory.** Measured with `size`: text 49,152 bytes, data + BSS 655,360 bytes, an image of 704,512 bytes. With a 32,768-byte stack reserve and the whole 131,835-byte `prog.bin` output counted in full, the preprocessing memory bound is 869,115 bytes <= 2^20, and its measured peak resident memory is 573,440 bytes (560 KiB).

### 3.7 Correctness of the step (checked by execution)

- `selftest` (Appendix B) executes `prog.bin`, decoded from its 5-byte encoding, on 8 x 256 uniform points for four chained steps each, and compares every output with F computed by a plain lane-wise 6-round implementation: 8,192 chained evaluations, 0 mismatches.
- That reference matches `hashlib.sha3_256` at 24 rounds on 300 messages of lengths 0 to 299, and `verifier/keccak.py` `sha3_256(m, rounds=6)` on the same 300 messages: 0 mismatches.
- The experiment program `experiments/ls1.py` regenerates the same straight line in Python using the exact same algorithm and node order as `gen.c` and refuses to run unless its 5-byte encoding hashes to `8c2b8795a9656a0530eb055f71c455e8dbcae1689a63736ad8e3500f4fafd0cc`. Before its trials it checks two chained full-width steps against the plain implementation.

## 4. The search

Parameters (`params.json`, following `18d9298d`):
- L = 256 walks.
- Distinguished point (DP): the 256-bit image x of F (bit j = plane j) is a DP when x < THR = 704 x 2^135: the planes 145 to 255 are zero and the 10 planes 144 down to 135, read as a number, are less than 704. The probability of a DP for a uniform image is theta = 704 x 2^-121 (H = -log2 theta = 111.540568); it is a rational number, exactly this, and is not a power of two.
- Replay cap LRC = 62,557 x 2^99 = 39,650,209,299,238,673,334,714,631,209,353,216 steps = 10.5000 / theta. No trail is cut; the replay refuses a trail of more than LRC evaluations.
- U = 92,352: the limit on trails started in one attempt.
- S = 23,088 table words, four records each (92,352 records >= U).
- Tb = 1326272364423520456082274405230575616 = 535677142 x 2^91 = 0.99777643 x 2^120 steps of 256 walks per attempt.
- HMAX = floor(Tb (1 + 2^-20) / 2^8) + 1 + LRC = 44830965663517622421370989484965889: the cap on prefilter hits; the attempt aborts at hit HMAX + 1.

State:
- in registers: the 256 input planes (registers 0 to 255); the step counter c, the next trail number idn, rho, the hit counter h, the all-ones word, the prefilter word and the return addresses (registers 2,181 to 2,190);
- in memory (word addressed): the table TAB of S words; LID[l] and LST[l] for each walk l (its trail number, and the number of the first step of its trail); a data image of 16 words: the 7 words of lane constants of the absorbed state (K, with the lanes of u Set to K_l), PD, and 8 words for the output pair.

A table word holds four records of 64 bits (bits 0-63, 64-127, 128-191, 192-255). A record is

    1 | (bits 0 to 45 of the trail's end) << 1 | (trail number) << 47,

never zero; an empty record is zero. The trail's length is not stored: the replay measures it.

```
setup: rho := random word; idn := 256; h := 0; c := 0; TAB := 0; for l < 256: LID[l] := l; LST[l] := 0; lane l of the input planes := rho + l
loop:
  the straight line (26,367): the input planes become F of the 256 walks
  pf := OR of the 16 planes 240..255 (15 ORs)
  if pf != all-ones (compare, branch):          -- some walk has planes 240..255 zero (probability 2^-16 each)
      h += 1; if h > HMAX: halt, the attempt failed   -- hit counter and abort (F5)
      dp := complement of (pf OR (OR of the planes 145..239))      -- the walks with the top 111 planes zero; c1 := c + 1 = steps completed including this one
      dp := dp AND (the walks whose planes 144..135, read as a number, are < 704)      -- bit-parallel comparison with the constant 704: the walks at a DP
      while dp != 0: l := the lowest set bit of dp; clear it;
          point := the 256-bit value with bit j = bit l of plane j
          record := 1 | (bits 0..45 of the point) << 1 | LID[l] << 47
          probe TAB from word (low 15 bits of the point, minus S if >= S), linear probing over words, wrap at S;
          in each word load it, then for its records 0, 1, 2, 3 in order (each extracted by a shift and a mask):
             an empty record: write the record into it (or into the word, store the word); restart(l, c1); next DP walk
             a record with the same bits 0..46 (valid bit and 46 end bits): REPLAY(its trail number, walk l, c1);
                if it returns a != b, output m(a), m(b) and stop; otherwise halt, the attempt failed
  c += 1; if c != Tb goto loop
  halt, the attempt failed                           -- c = Tb
restart(l, s): if idn = U: halt, the attempt failed
               LID[l] := idn; LST[l] := s; lane l of the input planes := rho + idn; idn += 1
REPLAY(trail a, walk l of trail b, c1):
  b := LID[l]; lb := c1 - LST[l]                       -- the new trail's length is known; if lb > LRC: return nothing
  la := the number of evaluations from rho + a to the first DP (stop with failure if LRC are passed)
  p := rho + a, q := rho + b; the longer trail is advanced by |la - lb| evaluations of F
  if p = q return nothing; repeat min(la, lb) times: if F(p) = F(q) return (p, q); p := F(p); q := F(q)
  return nothing
```

No trail is cut: a walk runs until its DP, however long that takes, and only the replay refuses a trail of more than LRC evaluations (the entry test lb <= LRC, and the measuring walk of trail a stops with failure after LRC evaluations without a DP). A trail restarted inside step c (at a DP) starts at step c + 1, hence LST[l] := c1. A trail is recorded at its first DP, so walking it from its start to its first DP gives its length; the walk of the replay stops at that DP. The DP test of the replay is x < THR on the image, the test of the loop above.

### 4.1 One iteration of the loop

An iteration costs the straight line (26,367), the prefilter (15), its test (2) and the counter (3: add, compare, branch): **BSTEP = 26,387 operations**, the instructions at the labels `loop` and `cont` of Appendix D around the straight-line block. No other operation runs in an iteration without a prefilter hit.

### 4.2 The replay

The replay evaluates F on one point at a time with the permutation, one unit (1626 operations) per call. The routine `evalF` (Appendix D) loads the 7 words of lane constants, XORs the four 64-bit limbs of the point into lanes 1, 11, 9, 14 and, XORed in pairs, into lanes 6 and 4, calls PERM, loads PD and XORs it into the first state word: one evaluation with its return costs **e = 1655** operations.

Counted from the emitted code:
- taking the trail number from the matching record costs 3 and the entry (trail b, lb, the test lb <= LRC 2, the two starts) 9;
- a measuring evaluation of trail a costs e + 8 (call, add, the DP test of the image x < THR 2, the cap test 2, move, jump), e + 4 for the one that lands on the DP;
- an advance step costs e + 7, a lock-step iteration 2e + 13, the success exit 67 (two message builds of 27 with their calls and moves, 8 stores, the halt).

With la, lb <= LRC, the replay costs at most 12 + (e + 8) LRC - 4 + (2e + 13) LRC + 71, that is **(1663 + 3323) LRC + 79** (largest for la = lb = LRC with the pair found at the last iteration; an advance step is cheaper than a lock-step iteration, so |la - lb| + min(la, lb) <= LRC iterations of at most 2e + 13 bound the rest). At most one replay runs per attempt: the attempt stops after it, with the pair or with failure.

### 4.3 Rare operations

Every routine is real code of the machine of Section 3.5 (Appendix D). The counts, each for the longest path, are read from the emitted code (`other4.py build`, D.2):

| routine | operations |
|---|---:|
| a prefilter hit with no DP walk (counter 3; OR of the planes 145..239; combine and complement 2; the comparison of the planes 144..135 with 704, at most 4 per plane, and a move; c1; test of the DP mask 2) | **115** |
| one DP walk, without its restart: DP-mask test 2, lowest set bit and clearing 44, gather of the point 1,022, record and word index 10, the word with the empty record 28, a wrap 2, the insertion 7; and 35 per full word passed (load, four records of 7 or 8, next word 3) | 1,115 + 35 S |
| restart(l, s) with its return: cap check 2, two stores, add, increment 4, the insertion of the new point into lane l and the return | **1,289** (the call that halts at idn = U: 3) |
| the event c = Tb: the HALT after the iteration's counter, compare and branch | 1 |
| setup: clearing TAB (eight words per pass), the 256 starts | **361,994** |

The numbers of events. At most HMAX + 1 prefilter hits are processed in every execution, and the ledger charges that number. The counter idn goes from 256 to U, one per completed restart, so at most U - 256 restarts complete; each DP walk except the last is followed by a completed restart, so at most U - 255 DP walks are processed (the last stores its record and halts at idn = U, or starts the replay of 4.2). At most U - 255 records are ever stored, fewer than the 4S record places, so every probe ends at an empty record or a match and passes at most S full words. The event c = Tb happens once.

R = (HMAX + 1) x 115 + (U - 255) x (1,115 + 35 S) + (U - 256) x (1,289 + 3) + 3 + 1 + 361,994 = 5,155,561,051,304,526,578,457,663,865,414,859,295.

### 4.4 Total

N = Tb x 26,387 + replay + R + PRE = **35,199,200,384,660,742,826,468,319,546,036,182,727,278** word operations (Appendix A).

| part | operations | share |
|---|---:|---:|
| main loop, Tb x 26,387 | 34,996,348,880,043,434,274,642,974,730,819,198,779,392 | 0.99424 |
| replay, (1663 + 3323) LRC + 79 | 197,695,943,566,004,025,246,887,151,209,835,135,055 | 0.00562 |
| rare operations R and preprocessing PRE | 5,155,561,051,304,526,578,457,663,865,414,859,295 + 141,733,953,536 | 1.46e-04 |

time_log2 = log2(N / 1626) rounded up at the fifth decimal = **124.02556**, checked in exact integer arithmetic:

    1626^100000 * 2^12402555 < N^100000 <= 1626^100000 * 2^12402556

## 5. Success probability and the premise H_rand

**Premise H_rand (our theory): over the algorithm's coins, the program run on the fixed SHA3-256-r6 target succeeds with probability at least the probability computed below for a uniformly random function F.** The target is fixed: F of Section 2, with its fixed constants K and PD, is one deterministic function, and the only randomness of the algorithm is the random word rho. That transfer is the premise, and it is the one score-critical premise of this package. Everything else in this section is computed in the random-function model M (following `18d9298d` and `2d74a370`): F is a uniformly random function from 256 bits to 256 bits (values at distinct inputs independent and uniform) and rho is uniform and independent of F. In M:

- (i) the first coincidence of images among e evaluations has probability 1 - prod_(k<e)(1 - k/n) >= 1 - exp(-e(e-1)/(2n)) =: G(e), where n = 2^256;
- (ii) the point reached just after a coincidence is uniform, so the number l of further evaluations of a trail until its DP satisfies P(l >= j) = (1 - theta)^j, independently of when the coincidence happened;
- (iii) F is realised by lazy sampling: a fresh evaluation draws a new independent uniform value, so given the whole history of the run it equals one given earlier output with probability 2^-256, whatever inputs the adaptive program chose. This is a property of M, not a claim about the fixed target, for which the run given rho is deterministic.

The first coincidence is a stopping time over all evaluations in their execution order (step by step, walk by walk). Under (i) and (iii), when k earlier images are distinct the next fresh evaluation coincides with an earlier image with conditional probability exactly k/n, so G(e) of (i) is the probability that the first e fresh evaluations contain a coincidence; no fixed-size birthday product over a random set and no conditioning on which trails finish is used.

**The coincidence.** Let e* be the first evaluation whose image equals an earlier image, at step b* = ceil(e*/256). The trail B of that evaluation and the earlier trail A have equal points from then on and both end at the same DP after l further evaluations of B. B is recorded at step b* + l at the latest; A reached the same point no later, so A was recorded before, or in the same step in a lower walk, and the later record finds the earlier one.

The search succeeds if all of these hold: (a) b* + l <= Tb; (b) both trails have at most LRC evaluations; (c) fewer than U trails are started; (d) the coincidence is between two different trails; (e) no record of a different end has the same 46 stored end bits, and the replay finds the merge.

Split l into bins of w = 2^(111 - 12) steps: bin j holds l in [(j - 1) w, j w - 1], j = 1 .. J = 62,557, J w = LRC, with probability p_j = (1 - theta)^((j-1) w) - (1 - theta)^(j w). If l is in bin j, (a) holds when e* <= 256 (Tb - j w). By (ii),

    Pr[(a)] >= sum_j p_j G(256 (Tb - j w)).

The failure events the sum does not cover:

- **F6**, the colliding pair has a trail of more than LRC evaluations. No trail is cut; the replay refuses such a pair, and this term bounds its probability by a union bound over the pairs of evaluations, weighted by the evaluations in trails longer than LRC. Write q = 1 - theta and E = 256 Tb, the number of evaluations of an attempt at most. The age of an evaluation is its place in its trail: the number of evaluations of the trail up to and including it. Until the first coincidence every input is fresh and the DP indicators xi of the evaluations are independent Bernoulli(theta) (as in F2); an evaluation of age at least a has the a - 1 earlier evaluations of its walk all non-DP, so P(age >= a) <= q^(a - 1) for every evaluation. Take evaluations s < t. By (iii), given the history before t, t has the image of s with probability 1/n, and the ages a_s and a_t, which depend only on evaluations before s and before t, are then fixed. By (ii) the number l of further evaluations to the DP has P(l >= j) = q^j independently of the history, and la = a_s + l, lb = a_t + l. The replay needs la <= LRC and lb <= LRC, so it fails when l >= LRC + 1 - max(a_s, a_t), with probability g(max(a_s, a_t)) <= g(a_s) + g(a_t), where g(a) = min(1, q^(LRC + 1 - a)). The function g does not decrease, g(1) = q^LRC, and g(a) - g(a - 1) = q^(LRC + 1 - a) (1 - q) for 2 <= a <= LRC + 1, g(a) = 1 beyond. By summation by parts, for any evaluation u, E[g(age_u)] = g(1) + sum over a >= 2 of (g(a) - g(a - 1)) P(age_u >= a) <= q^LRC + LRC (1 - q) q^LRC = q^LRC (1 + LRC theta). Each evaluation lies in at most E - 1 pairs, so the probability that the first coincidence is a pair with a trail of more than LRC evaluations is at most E (E - 1) q^LRC (1 + LRC theta) / n = 3.153e-4. This covers (b).
- **F2**, more than U - 256 restarts after a DP (a fact proved here). Realise F by lazy sampling with independent uniform values V_1, ..., V_(256 Tb), one per evaluation index in execution order: the t-th evaluation returns V_t if its input is fresh and the stored value otherwise. Put xi_t = 1 when V_t is a DP. The xi_t are independent Bernoulli(theta), so N1 = xi_1 + ... + xi_(256 Tb) is binomial with mean mu = 256 Tb theta. A DP output at a fresh input is a position with xi_t = 1. A DP output at a repeated input never causes a restart: the value is the stored output of the first evaluation of that input, whose trail ended there and was recorded with another trail number, and the probe finds that record, so the attempt goes to REPLAY and stops. Hence the restarts after a DP are at most N1. The halt at idn = U needs N1 >= U - 255, and the Chernoff bound e^-mu (e mu / (U - 256))^(U - 256) >= P(N1 >= U - 256) gives 3.703e-12. This covers (c).
- **F3**, the coincidence lies inside one trail: at most U / (theta^2 n) = 1.137e-5. This covers (d).
- **F4**, 2^-90 + U^2 2^-47 = 6.060e-5. This covers (e): a start rho + i equal to a point of another trail (U starts, about 2^128 images: below 2^-113); and two different ends with the same 46 stored bits: in M the ends are uniform on the bits below the 10 comparison planes, so a pair agrees with probability 2^-46, and there are fewer than U^2 / 2 pairs.
- **F5**, the hit counter aborts the attempt before it stops: below 2^-1000. Call a walk's input at a step fresh if F was not evaluated at it before in the attempt, and let X' count the steps at which some walk with a fresh input lands on planes 240..255 zero. Given the past, each step adds to X' with conditional probability at most 1 - (1 - 2^-16)^256 < 2^-8 (in M). A hit not counted in X' needs a walk at a repeated input; outside F4 these occur only after the first image coincidence, and a successful attempt outside F6 stops at step b* + l with l <= LRC. So h <= X' + LRC on success, and an abort needs X' >= floor(Tb (1 + d) 2^-8) + 2 > (1 + d) mu, with d = 2^-20 and mu = Tb 2^-8. The Chernoff bound for indicators with conditional probabilities at most 2^-8 (supermartingale exp(s X'_t - (e^s - 1) t 2^-8)) gives at most exp(-d^2 mu / (2 + d)) = exp(-2,355,931,862,055,407,962,070) < 2^-1000, checked in exact rationals in Appendix A.

With a further 2^-60 for rounding, the success probability of one attempt is at least 0.3900000006 at Tb, and 0.3899999994 at Tb - 2^91: Tb is the least multiple of 2^91 that reaches 0.39 (Appendix A, 80-digit decimals). In evaluations, 256 Tb = 0.997776 x 2^128; the birthday point for success 0.39 is 0.9943 x 2^128, and the wait for the DPs of the last trails, 256 / theta evaluations, is most of the difference.

A failed attempt can be repeated with a fresh rho at the same cost. The claim is one attempt with success 0.39, a probability over the algorithm's coin rho for the fixed target, under the premise H_rand.

## 6. Memory

The search, at its peak:

| region | bytes |
|---|---:|
| register file, 2,192 words of 32 bytes (H_reg) | 70,144 |
| straight line plus prefilter, 26,382 instructions x 5 bytes (H_code) | 131,910 |
| other code (Appendix D), 2,704 instructions x 32 bytes, measured | 86,528 |
| table, 23,088 words of four records | 738,816 |
| LID and LST of the 256 walks, 512 words | 16,384 |
| data image (lane constants K of the absorbed state, PD, output pair), 16 words | 512 |
| **total** | **1,044,294** |

The preprocessing `gen 32` runs before the search and ends before it starts:

| `gen 32` | bytes |
|---|---:|
| image (text 49,152, data + BSS 655,360; all arrays static) | 704,512 |
| stack reserve | 32,768 |
| the program it writes, prog.bin (counted here in full) | 131,835 |
| **bound used** | **869,115** |
| measured peak resident memory | 573,440 |

The claimed memory covers both phases, the preprocessing included: peak = max(search 1,044,294, preprocessing 869,115) = 1,044,294, since the two phases do not overlap; 1,044,294 <= 1,048,576 = 2^20: memory_log2_bytes = 20 and the memory term of the score is 0. The margin to 2^20 is 4,282 bytes (search phase 4,282, preprocessing 179,461).

The declared experiments and the C and Python checks of Sections 3.7 and 7 are verification runs; they build nothing the attack uses.

## 7. Evidence for the step and for H_rand

### 7.1 Organizer experiments (experiments/manifest.json, program experiments/ls1.py)

Both experiments regenerate the straight line in Python with the generator's algorithm and node order (the encoding must hash to the SHA-256 of Section 3.5), check it against the plain 6-round implementation, and execute it on Python integers, all trials side by side.

- **rho-w22** runs the search of Section 4 end to end at width 22. The planes 22 to 255 are set to zero after every step. Parameters: a DP is an image whose 4 low bits are zero and whose 3 bits above them, as a number, are less than 5 (theta = 5/128), replay cap 256, no trail cut, 3,000 trails and 400 steps per attempt; the table keeps the trail number of each end and the replay measures the stored trail by walking it to its DP and refuses trails of more than 256 evaluations, as in Section 4. Every trial returns two messages whose 6-round digests agree on the 22 low bits. At this width a start often lies on another trail, so a replay that returns nothing restarts the walk instead of ending the attempt (the full-size rule halts, as F4 accounts). An ideal-function control (F replaced by a lazily sampled random function on 22 bits, the same rules) needs 20.47 steps to the pair on average (20,000 trials, standard deviation 7.91). Our own runs on 9 x 256 local seeds: 2,304 of 2,304 trials returned a valid pair, with a mean of 20.73 steps to the pair (standard error 0.16, z = +1.6); a 256-trial request takes 5.2 s on one core here.
- **proj-w256** runs eight chained full-width steps from 256 uniform points per trial and finds the first two distinct evaluated inputs whose images agree on the 22 low bits; a random function gives success probability 0.3934 per trial, 100.7 of 256 (standard deviation 7.8). Our nine Python runs: 916 of 2,304 = 0.3976 (z = +0.4); a 256-trial request takes 7.6 s here. The same trial in C at scale (Section 7.2): 103,022 of 262,144 = 0.3930 (z = -0.39), and 6,444 of 16,384 = 0.3933 (z = -0.02).

### 7.2 Measured checks of H_rand on this program (our runs, not organizer runs)

The embedding makes round 0 affine, so F has one nonlinear round fewer than the plain digest map. `hrand_test.c` and `proj_test.c` (Appendix C) execute the program file of this package (`prog.bin`, 26,367 instructions) and measure the quantity the search depends on, the rate of image coincidences among evaluated points, on three 32-bit windows (bits 0-31, 128-159 and 224-255; the top window lies inside the DP bits), for uniform inputs (A), the consecutive starts rho + i the search uses (B) and chained iterates (C), the output differences of single-bit input differences (D), and `proj-w256` at scale:

```
A uniform inputs: M=2^24, pairs agreeing on 32 bits: low 33014, mid 32693, top 32884; expected 32768.0 each (sd 181.0); ratios 1.0075 0.9977 1.0035; z 1.36 -0.41 0.64
B consecutive inputs R+i: M=2^24, pairs agreeing on 32 bits: low 32786, mid 32810, top 32938; expected 32768.0 each (sd 181.0); ratios 1.0005 1.0013 1.0052; z 0.10 0.23 0.94
C chained iterates (256 chains x 65536 steps): M=2^24, pairs agreeing on 32 bits: low 32580, mid 32940, top 32708; expected 32768.0 each (sd 181.0); ratios 0.9943 1.0052 0.9982; z -1.04 0.95 -0.33
D single-bit differences: 65536 cells x 4096 pairs, max |z| 4.59 at input bit 246 output bit 248 (largest of 65536 normal cells is about 4.4); mean z^2 1.0112 (expected 1)
proj at scale: 262144 trials, 103022 successes = 0.3930; model 0.3934; z -0.39
```

The coincidence rates lie within |z| <= 1.36 of the random-function values. If the real pair-coincidence rate is (1 - eps) of the random value, the same success needs about 0.5 log2(1/(1 - eps)) more bits of time, 0.0073 bit for eps = 0.01.

### 7.3 The emitted program, executed (our runs, not organizer runs)

`other4_test.py` (Appendix D) executes the assembled bytes: `other.bin` decoded from its 32-byte encoding, and the straight line (`prog.bin` and the 15 prefilter instructions) decoded from its 5-byte encoding and compiled to Python integer operations (D.3, D.4).
- **Routines, at the full-size immediates of this package.** The straight line against the plain 6-round implementation on every lane (2 x 256 points, 3 chained steps) and the prefilter word; setup, setwalk, restart and its halting call, evalF and the message builder against the plain implementation; a hit with no DP walk and the hit-counter abort; the DP handler on its longest path with 0 and 5 full words and with a wrap over 7 words, and the record it writes in the fourth place of a word; the insertion into each of the four places of a word and a match in each place; the DP mask of the hit handler against the comparison x < THR on 1,024 constructed walks, and the iteration that reaches Tb. Each executed count equals the count of Section 4.3.
- **Replay.** Pairs of trails of the 12-bit truncation of F with a 4-bit DP: 47 pairs with the same end (the replay measures la, aligns, finds the pair; the executed count equals 9 + (la - 1)(e + 8) + (e + 4) + 2 + 2 + n (e + 7) + 2 + 2 + (k - 1)(2e + 13) + (9 + 2e) + 67 exactly, and the pair is checked with an independent Keccak) and 13 pairs with different ends (a false key match: the replay exhausts and the attempt halts), and the cap guard of the measuring walk.
- **End to end at reduced width.** The whole emitted program (setup, loop, straight line, hit handler, DP handler, restart, replay, output) runs with the planes W..255 set to zero after each step and the replay's F truncated alike (one extra ANDI in evalF, test builds only), the other immediates reduced; instruction for instruction it is the program of the full-size build. 16 runs on eight parameter sets (W = 26; W = 32 with a replay cap that refuses long colliding trails; a table of 400 words; a hit cap of 3; Tb = 5; U = 264; a table of 200 words with U = 800, so that every word fills its four records; no comparison planes). Every pair found was checked with an independent Keccak, the executed operations were at or below the counted bounds of Section 4.3, and the sub-counts (setwalk, gather, loop, replay) matched exactly: 422 checks, 0 failures.

## 8. Sensitivity

| change | effect | score |
|---|---|---:|
| as claimed (H_reg 2,192 registers, H_code 5 bytes per instruction) | | 124.02556 |
| 1,024 registers: loads and stores (Belady eviction, spill.py on the same program) add 9,708 per step | time +0.45 | 124.475 |
| 512 registers, +15,520 per step | time +0.66 | 124.690 |
| 256 registers, +20,347 per step | time +0.82 | 124.847 |
| 64 registers, +26,130 per step | time +0.99 | 125.014 |
| straight line stored at 32 bytes per instruction | memory above 2^20; coarse scan | about 124.71 |

- **Register rows.** These carry the same straight line, register allocation aside (`spill.py`, Appendix C). A schedule built for the smaller file would do better.
- **H_rand.** A pair-coincidence deficit eps costs about 0.5 log2(1/(1 - eps)) bits (Section 7.2).
- **Same premises as 67f781f8, bc3e3eef, 7d11f600 and 18d9298d.** All of these entries use the same register and 5-byte straight-line conventions.

## 9. Credits and literature

A credit is not an endorsement; nobody named here has reviewed this package.

- **Jbenisek, entry 18d9298d (sha3-256-r6, 124.07568), and entries 2acfdbee (124.16399) and 2d74a370 (125.19730).** `18d9298d` introduced the 10-gate chi row (Section 3.2), the four-record-per-word table packing (`S` words of four 64-bit records), the rational distinguished-point threshold `x < 704 x 2^135`, the uncut Stage-1 / replay-cap `F6` analysis (Section 5), and the assembled 2,704-instruction non-straight-line code (`other4.py`, `other4_test.py` and `cert4.py`, Appendices A and D), which we adapt to the annihilating embedding and our 26,367-operation step program. `2d74a370` and `2acfdbee` supply the underlying parallel distinguished-point search, replay and failure-term framework.
- **Our entry 7d11f600 (sha3-256-r6, 124.13884) and entries bc3e3eef / e1c05beb (124.19636).** `7d11f600` introduced the 32-trial annihilating linear-structure constant family of Section 2 (reducing tracked affine forms across round 0 and round-1 theta to 1,088) and the lookahead coordinate-descent row-complement optimizer with NOT-gate reuse (`not_uses`, `has_cons`) of Section 3.2, extended here to optimize 10-gate chi rows and both two-gate mixed-polarity AND forms against the exact 10-gate next-round score `eval_phi`.
- **jungjipdo, entry 67f781f8 (sha3-256-r6, 124.46633).** Its Section 3 describes the bit-sliced step design this package follows: theta evaluated lazily per chi row, per-row complement subsets, dead-code elimination, the digest written over the input register, last-use allocation into a declared register file, and the 5-byte straight-line encoding (`H_reg` and `H_code`).
- **J. Guo, M. Liu, L. Song, Linear Structures: Applications to Cryptanalysis of Round-Reduced Keccak, ASIACRYPT 2016.** The linear-structure placement of message lanes that keeps round 0 affine (Section 2).
- **P. C. van Oorschot and M. J. Wiener, Parallel collision search with cryptanalytic applications, J. Cryptology 12 (1999); J. M. Pollard (1975).** The distinguished-point and rho methods.
- **G. Bertoni, J. Daemen, M. Peeters, G. Van Assche, Keccak implementation overview.** The lane complementing transform, applied plane by plane in Section 3.2.

## Appendix A. The exact ledger

This program (`cert4.py`, with the inputs of this package written into `INLINE`) computes the step count, the success bound of Section 5, N, the memory table and the integer certificate. It uses integers and Fractions; Decimal with 80 digits is used only for the exponentials and logarithms of the success bound. The constants of the rare operations and of the replay are the counts of Section 4.3, printed by `other4.py build` (D.2).

```python
INLINE = {
"ledger.txt": "LS1 step ledger (256 lanes, one chain step, 6 rounds)\nXOR 19052\nAND 3743\nOR  2913\nNOT 659  (row complements chosen pre-DCE: 1007)\nLOAD 0\nSTORE 0\nTOTAL 26367\nTRICKROWS 1213\nfeed NOTs 0 (digest polarity folded into the chain function: F(u)=H(m(u))^PD)\nnodes created pre-DCE 26367 ; nodes 26623 ; linear forms 1088\nmax live values 1925 ; registers used 2181 (limit 2304)\nconstants trial 27 of 32\n",
"size.txt": "   text\t   data\t    bss\t    dec\t    hex\tfilename\n  49152\t 655360\t      0\t 704512\t  ac000\tgen\n",
"counts.txt": "other code: 2704 instructions x 32 bytes = 86528 bytes (other.bin sha256 b2ec53360bebcdf97a54ad8e57e57adf21ab13806e60839935e2bb85268e5b9d)\nprefilter: 15 instructions x 5 bytes (pf.bin sha256 7d01825e1754a115fd593386cbd91d120baff96ff46f5ea6472a7326662ddfbc); the straight-line block = prog.bin then pf.bin, 26382 instructions, sits in front of instruction 26 (label loop)\ndata image: 16 words x 32 bytes = 512 bytes (data.bin sha256 94c4ba41fdc2624a956f241f6116e54974fc0053fd09c9ec2b08a465cf47e073): KW[0..6], PD, 8 output words\nmemory map (words): TAB 0..23087, LID 23088..23343, LST 23344..23599, data 23600..23615\nroutine entry points (instruction index): start 0, loop 26, hit 28, dpl 142, dp1 144, gather 188, record 1210, probe 1220, empty0 1257, ins 1272, match0 1275, cont 1287, dl 1290, restart 1291, setwalk 1298, evalF 2581, outm 2611, match 2638, meas 2647, end 2704\nn_instr            2704\nsetwalk            1283\nrestart            1289\nrestart_halt       3\nhit                115\nctz_clear          44\ngather             1022\nrecord_slot        10\nprobe_word         35\nprobe_wrap         2\nprobe_end          28\nempty_tail         7\ndp_fixed           1115\ndp_max             809195\ndl_final           1\ne_eval             1655\ne_outm             27\nmatch_entry        12\nmeas_iter          1663\nmeas_last          1659\nreplay_iter        3323\nreplay_const       79\nreplay_max         197695943566004025246887151209835135055\nsetup              361994\nstatic opcode mix: OR 613 ANDI 540 SHRI 276 SHLI 270 AND 263 SHL 257 SHR 256 ST 24 EQI 23 BNZ 21 XOR 21 MOV 18 ADDI 17 LDA 15 JMP 14 BZ 13 MOVI 10 JAL 9 NOT 7 LTI 7 HALT 5 SUBI 5 ADD 4 LD 4 EQ 3 JR 3 SUB 3 RND 1 PERM 1 LT 1\nhighest register named: 2190 (file of 2192)\n",
"params.json": "{\n \"NR\": 6,\n \"HF\": 111,\n \"DPLO\": 145,\n \"DK\": 10,\n \"DT\": 704,\n \"S\": 23088,\n \"U\": 92352,\n \"SB\": 15,\n \"IDB\": 17,\n \"W\": 633825300114114700748351602688,\n \"J\": 62557,\n \"LRC\": 39650209299238673334714631209353216,\n \"Tb\": 1326272364423520456082274405230575616,\n \"HMAX\": 44830965663517622421370989484965889,\n \"PFLO\": 240,\n \"PFN\": 16\n}"
}
# cert4.py - LS1 exact ledger at SHA3-256 round count NR: step count, success bound, N, memory, integer certificate
# (integers and Fractions; Decimal with 80 digits only for the exponentials and logarithms of the success bound).
#   python3 cert4.py            exact ledger of the row in this directory: ledger.txt (generator counts), size.txt
#                               (generator image), counts.txt (other code), params.json (search parameters)
import sys, os, re, json, math
from fractions import Fraction as Fr
from decimal import Decimal as D, getcontext, ROUND_CEILING
getcontext().prec = 80
ceil = lambda v: int(v.to_integral_value(rounding=ROUND_CEILING)) if isinstance(v, D) else -((-v.numerator) // v.denominator)
try:
    INLINE                                       # the inputs written into this listing (proof.md Appendix A)
except NameError:
    INLINE = None                                # the factory run: the inputs are read from the row's files
rd = lambda p: INLINE[p] if INLINE else open(p).read()

# ---- one step of 256 walks (Section 3; counts printed by the generator gen.c, ledger.txt) ----
led = rd('ledger.txt')
g = lambda k: int(re.search(r'^%s\s+(\d+)' % k, led, re.M).group(1))
NR = int(re.search(r'one chain step, (\d+) rounds', led).group(1))
XOR, AND, OR, NOT = g('XOR'), g('AND'), g('OR'), g('NOT')
LINE = XOR + AND + OR + NOT                      # the straight line, no loads or stores (registers, H_reg)
assert LINE == g('TOTAL')
REGUSED = int(re.search(r'registers used (\d+)', led).group(1)); assert REGUSED <= 2181
PF = 15                                          # prefilter: OR of the 16 planes 240..255
BSTEP = LINE + PF + 2 + 3                        # + compare pf with all-ones and branch; c += 1, compare with Tb, branch
UNIT = 271 * NR                                  # the cost model's price of one NR-round permutation
L = 256
n = D(2) ** 256
RPW = 4                                          # records per table word (64 bits each)

# ---- the other code (Section 4.3): instruction count and routine counts of the emitted code (other4.py build) ----
def read_counts(p='counts.txt'):
    c = {}
    for line in rd(p).split(chr(10)):
        m = re.match(r'^([a-z_0-9]+)\s+(\d+)$', line.strip())
        if m: c[m.group(1)] = int(m.group(2))
    return c

# ---- memory (Section 6) ----
REGS = 2192                                      # registers 0..2,180 by the straight line, 2,181..2,190 search state, 2,191 spare
sz = rd('size.txt').split('\n')[1].split()
GEN_IMAGE = int(sz[0]) + int(sz[1]) + int(sz[2])  # gen: text + data + BSS, size(1); all arrays are static
GEN_STACK = 32768                                # stack reserve
MARGIN = 4096


def mem_search(S, NI):
    return {'register file, 2,192 words': 32 * REGS,
            'straight line incl. prefilter, %d instructions x 5 bytes' % (LINE + PF): 5 * (LINE + PF),
            'other code (setup, loop, handlers, restart, replay), %d instructions x 32 bytes' % NI: 32 * NI,
            'table, %d words (four records each)' % S: 32 * S,
            'LID and LST of the 256 walks, 512 words': 32 * 512,
            'data image (lane constants K, PD, output pair), 16 words': 32 * 16}


def mem_pre():
    return GEN_IMAGE + GEN_STACK + 5 * LINE      # the generator (image and stack) plus the program it writes


def fit_S(NI):
    fixed = sum(mem_search(0, NI).values())
    S = (2 ** 20 - MARGIN - fixed) // 32 // 8 * 8
    while S + 100 >= 1 << S.bit_length(): S -= 8   # keeps 100 slots of room below 2^SB (routine tests)
    return S


def u_of(S): return min(RPW * S, 1 << 17)        # trail limit: records places, trail numbers of at most 17 bits (key bits >= 46)


# ---- the distinguished point: x < THR, THR = DT 2^(DPLO - DK); theta = DT 2^-(256 - DPLO + DK), exactly ----
def theta_of(DPLO, DK, DT): return D(DT) / D(2) ** (256 - DPLO + DK)


# ---- success probability (Section 5) ----
def success(Tb, theta, w, J, U, K, parts=False):
    """theta: the DP probability; w: bin width (steps, an integer); J: number of bins, the replay cap is LRC = J w;
    U: trail limit; K: key bits of a record."""
    LRC = J * w; lq = (1 - theta).ln()
    mu, k = D(L * Tb) * theta, U - L
    if k <= mu: return (D(-1), None) if parts else D(-1)
    s, qprev = D(0), D(1)
    for j in range(1, J + 1):
        qj = (w * j * lq).exp()
        e = L * (Tb - j * w)
        if e > 1:
            s += (qprev - qj) * (1 - (-D(e) * (e - 1) / (2 * n)).exp())
        qprev = qj
    E = L * Tb                                               # evaluations of one attempt, at most
    e6 = D(E) * (E - 1) / n * ((LRC) * lq).exp() * (1 + LRC * theta)   # F6: a colliding pair with a trail longer than LRC
    e2 = (-mu + k * (1 + (mu / k).ln())).exp()               # F2: more than U - L distinguished points (Chernoff, k > mu)
    e3 = D(U) / (theta * theta * n)                          # F3: a coincidence inside one trail
    e4 = D(2) ** -90 + D(U) ** 2 * D(2) ** -(K + 1)          # F4: starts, replay, and two different ends with equal K key bits
    e5 = D(2) ** -1000                                       # F5: the hit counter passes HMAX (abort); bound proved below
    p = s - (e2 + e3 + e4 + e5 + e6 + D(2) ** -60)
    return (p, (e6, e2, e3, e4)) if parts else p


# ---- the ledger (Section 4) ----
def ledger(TB, S, U, LRC, c, NI):
    replay = (c['meas_iter'] + c['replay_iter']) * LRC + c['replay_const']   # at most one replay per attempt, lengths <= LRC
    DELTA = Fr(1, 2 ** 20)
    HMAX = (TB * (1 + DELTA)) // 2 ** 8 + 1 + LRC            # the driver aborts (attempt failed) when hit number HMAX + 1 occurs
    MU = Fr(TB, 2 ** 8)
    EXPO = DELTA ** 2 * MU / (2 + DELTA)                     # P[F5] <= exp(-EXPO)
    assert EXPO > 1000 * Fr(6932, 10000)                     # ln 2 < 0.6932, so P[F5] < 2^-1000 (the e5 of success())
    hits = HMAX + 1                                          # at most HMAX + 1 hits are processed in every execution
    C_dp = c['dp_fixed'] + c['probe_word'] * S               # at most S occupied words passed
    N_DP, N_RESTART = U - 255, U - 256
    Rr = (hits * c['hit'] + N_DP * C_dp + N_RESTART * (c['restart'] + 3) + c['restart_halt'] + c['dl_final'] + c['setup'])
    return replay, HMAX, Rr, EXPO


def pre_ops():
    """preprocessing = one run of `gen 32`: 32 trial builds and the rebuild of the best (33 builds, 2^32 operations each),
    plus per trial 2^10 (constants, count, comparison, line)."""
    B = 33
    return B * 2 ** 32 + 32 * 2 ** 10, B


def cert(N):
    K = 100000
    e = ceil(K * (D(N) / UNIT).ln() / D(2).ln())
    while N ** K > (UNIT ** K) << e: e += 1
    while N ** K <= (UNIT ** K) << (e - 1): e -= 1
    return K, e


# ---------------- the exact ledger ----------------
P = json.loads(rd('params.json'))
assert P['NR'] == NR
HF, DPLO, DK, DT, S, U, TB, W, J, LRC, IDB = P['HF'], P['DPLO'], P['DK'], P['DT'], P['S'], P['U'], P['Tb'], P['W'], P['J'], P['LRC'], P['IDB']
KEYB = 63 - IDB
c = read_counts(); NI = c['n_instr']
assert S == fit_S(NI) and U == u_of(S)
THETA = theta_of(DPLO, DK, DT)
GRAN = 2 ** (HF - 20)
assert DPLO == 256 - HF and 0 < DT < 2 ** DK and DK >= 1 and 2 ** (DK - 1) <= DT                 # 1/2 <= DT / 2^DK < 1
assert TB % GRAN == 0 and LRC == J * W and W == 2 ** (HF - 12) and P['SB'] == S.bit_length() and U <= RPW * S and U <= 2 ** IDB and 2 ** (IDB - 1) < U
assert DPLO - DK > KEYB and KEYB >= 46
print('rounds %d, unit %d word operations' % (NR, UNIT))
print('step of 256 walks: straight line', LINE, '(xor %d and %d or %d not %d) + prefilter %d + test 2 + counter 3 =' % (XOR, AND, OR, NOT, PF), BSTEP)
print('parameters: DP = planes %d..255 zero and the %d planes below them < %d (theta = %d x 2^-%d = 2^-%.6f), replay cap LRC = %d x %d = %.4f / theta, U %d trails, S %d table words (%d records), key bits %d, trail number bits %d'
      % (DPLO, DK, DT, DT, 256 - DPLO + DK, -math.log2(THETA), J, W, LRC * THETA, U, S, RPW * S, KEYB, IDB))
p, (e6, e2, e3, e4) = success(TB, THETA, W, J, U, KEYB, parts=True)
p_less = success(TB - GRAN, THETA, W, J, U, KEYB)
assert p >= D('0.39') > p_less
print('Tb = %d = %d * 2^%d = %.8f * 2^120, evaluations %.6f * 2^128' % (TB, TB // GRAN, HF - 20, D(TB) / D(2) ** 120, D(L * TB) / D(2) ** 128))
print('failure terms: F6 %s  F2 %s  F3 %s  F4 %s  success bound %s  (2^%d steps fewer: %s)' % tuple([format(x, '.3e') for x in (e6, e2, e3, e4)] + [str(p)[:12], HF - 20, str(p_less)[:12]]))
replay, HMAX, Rr, EXPO = ledger(TB, S, U, LRC, c, NI)
assert HMAX == P['HMAX']
print('hit counter: HMAX =', HMAX, '; P[abort before the stop on success] <= exp(-%d) < 2^-1000' % (EXPO.numerator // EXPO.denominator))
print('replay: (%d + %d) LRC + %d = %d (measuring walk e + 8, lock step 2e + 13, e = %d)' % (c['meas_iter'], c['replay_iter'], c['replay_const'], replay, c['e_eval']))
assert c['e_eval'] == UNIT + 29
PRE, B = pre_ops()
N = TB * BSTEP + replay + Rr + PRE
print('main', TB * BSTEP, ' replay', replay, ' rare', Rr, ' preprocessing', PRE, '(builds %d)' % B)
pl = 0
while (UNIT << pl) < PRE: pl += 1
print('preprocessing_log2: 2^%d < PRE / %d <= 2^%d, declared %d' % (pl - 1, UNIT, pl, pl))
print('N =', N)
print('shares: main %.5f replay %.5f other %.2e' % (TB * BSTEP / N, replay / N, (Rr + PRE) / N))
ms = mem_search(S, NI)
run_total = sum(ms.values()); pre_total = mem_pre()
for k, v in ms.items(): print('  %9d  %s' % (v, k))
print('search memory', run_total, '; preprocessing (gen): image', GEN_IMAGE, '+ stack', GEN_STACK, '+ program', 5 * LINE, '=', pre_total)
mem = max(run_total, pre_total)
assert mem <= 2 ** 20 - MARGIN
print('memory', mem, '<= 2^20 = 1048576 with a margin of', 2 ** 20 - mem, 'bytes (search phase', 2 ** 20 - run_total, ', preprocessing', 2 ** 20 - pre_total, '): memory_log2_bytes = 20')
K, e = cert(N)
print('certificate: %d^%d * 2^%d < N^%d <= %d^%d * 2^%d' % (UNIT, K, e - 1, K, UNIT, K, e))
print('time_log2 = %d.%05d' % divmod(e, K))
print('score = time_log2 + max(0, memory_log2 - 20) = %d.%05d' % divmod(e, K))
```

Output:

```
rounds 6, unit 1626 word operations
step of 256 walks: straight line 26367 (xor 19052 and 3743 or 2913 not 659) + prefilter 15 + test 2 + counter 3 = 26387
parameters: DP = planes 145..255 zero and the 10 planes below them < 704 (theta = 704 x 2^-121 = 2^-111.540568), replay cap LRC = 62557 x 633825300114114700748351602688 = 10.5000 / theta, U 92352 trails, S 23088 table words (92352 records), key bits 46, trail number bits 17
Tb = 1326272364423520456082274405230575616 = 535677142 * 2^91 = 0.99777643 * 2^120, evaluations 0.997776 * 2^128
failure terms: F6 3.153e-4  F2 3.703e-12  F3 1.137e-5  F4 6.060e-5  success bound 0.3900000006  (2^91 steps fewer: 0.3899999994)
hit counter: HMAX = 44830965663517622421370989484965889 ; P[abort before the stop on success] <= exp(-2355931862055407962070) < 2^-1000
replay: (1663 + 3323) LRC + 79 = 197695943566004025246887151209835135055 (measuring walk e + 8, lock step 2e + 13, e = 1655)
main 34996348880043434274642974730819198779392  replay 197695943566004025246887151209835135055  rare 5155561051304526578457663865414859295  preprocessing 141733953536 (builds 33)
preprocessing_log2: 2^26 < PRE / 1626 <= 2^27, declared 27
N = 35199200384660742826468319546036182727278
shares: main 0.99424 replay 0.00562 other 1.46e-04
      70144  register file, 2,192 words
     131910  straight line incl. prefilter, 26382 instructions x 5 bytes
      86528  other code (setup, loop, handlers, restart, replay), 2704 instructions x 32 bytes
     738816  table, 23088 words (four records each)
      16384  LID and LST of the 256 walks, 512 words
        512  data image (lane constants K, PD, output pair), 16 words
search memory 1044294 ; preprocessing (gen): image 704512 + stack 32768 + program 131835 = 869115
memory 1044294 <= 2^20 = 1048576 with a margin of 4282 bytes (search phase 4282 , preprocessing 179461 ): memory_log2_bytes = 20
certificate: 1626^100000 * 2^12402555 < N^100000 <= 1626^100000 * 2^12402556
time_log2 = 124.02556
score = time_log2 + max(0, memory_log2 - 20) = 124.02556
```

## Appendix B. The generator (gen.c) and the self-test (selftest.c)

Compiled with `cc -O3 gen.c -o gen`; run as `./gen 32` (or `./gen 1 27`).

```c
#ifdef USE_LIBC
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint64_t u64; typedef int64_t i64; typedef uint32_t u32; typedef uint16_t u16; typedef uint8_t u8;
static FILE *fp_out = NULL;
static void oflush(void){ if(fp_out) fflush(fp_out); }
static void oc(char c){ fputc(c, fp_out ? fp_out : stdout); }
static void os(const char *s){ fputs(s, fp_out ? fp_out : stdout); }
static void ou(u64 v){ fprintf(fp_out ? fp_out : stdout, "%llu", (unsigned long long)v); }
static void ox(u64 v){ fprintf(fp_out ? fp_out : stdout, "%016llx", (unsigned long long)v); }
static void die(const char *m){ fprintf(stderr, "gen: %s\n", m); exit(1); }
static int atoi_(const char *s){ return atoi(s); }
#else
typedef unsigned long u64; typedef unsigned int u32; typedef unsigned short u16; typedef unsigned char u8;
typedef long i64;
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
static int fopen_w(const char *p){ return (int)sc3(2,(i64)p,01|0100|01000,0644); }
static void fclose_(int fd){ sc3(3,fd,0,0); }
static void die(const char *m){ oflush(); fd_out=2; os("gen: "); os(m); oc('\n'); oflush(); sc3(60,1,0,0); }
static int atoi_(const char *s){ int v=0; while(*s>='0'&&*s<='9') v=v*10+(*s++-'0'); return v; }
#endif

static const u64 RC[24]={0x0000000000000001ULL,0x0000000000008082ULL,0x800000000000808aULL,0x8000000080008000ULL,
 0x000000000000808bULL,0x0000000080000001ULL,0x8000000080008081ULL,0x8000000000008009ULL,0x000000000000008aULL,
 0x0000000000000088ULL,0x0000000080008009ULL,0x000000008000000aULL,0x000000008000808bULL,0x800000000000008bULL,
 0x8000000000008089ULL,0x8000000000008003ULL,0x8000000000008002ULL,0x8000000000000080ULL,0x000000000000800aULL,
 0x800000008000000aULL,0x8000000080008081ULL,0x8000000000008080ULL,0x0000000080000001ULL,0x8000000080008008ULL};
static const int ROT[5][5]={{0,36,3,41,18},{1,44,10,45,2},{62,6,43,15,61},{28,55,25,21,56},{27,20,39,8,14}};
#define NROUNDS 6

static inline u64 rotl64(u64 v, int r){ return r ? (v<<r)|(v>>(64-r)) : v; }
static inline int pop64(u64 x){
  x -= (x >> 1) & 0x5555555555555555ULL;
  x = (x & 0x3333333333333333ULL) + ((x >> 2) & 0x3333333333333333ULL);
  return (int)((((x + (x >> 4)) & 0x0f0f0f0f0f0f0f0fULL) * 0x0101010101010101ULL) >> 56);
}

#define MAXN 32768
#define NC 0xFFFF
enum { O_IN=0, O_XOR=1, O_AND=2, O_OR=3, O_NOT=4 };
#define F_OPM 7
#define F_K 8
#define F_LIVE 16
#define F_LIN 32
static u8 nf[MAXN];
static u16 na[MAXN], nb[MAXN];
static u16 linid[MAXN];
#define MAXF 2048
static u64 form[MAXF][4]; static u16 formnode[MAXF]; static int nform;
#define FH 4096
static u16 fh[FH];
#define CH 65536
static u16 ch[CH];
static int nn;

typedef struct { u16 n; u8 p; } V;
static V K_(int c){ V v; v.n=NC; v.p=(u8)c; return v; }
static V MK(int n,int p){ V v; v.n=(u16)n; v.p=(u8)p; return v; }

static u32 hmix(u32 x){ x^=x>>16; x*=0x7feb352dU; x^=x>>15; x*=0x846ca68bU; x^=x>>16; return x; }
static int newnode(int op,int a,int b){ if(nn>=MAXN-1) die("node overflow"); nf[nn]=(u8)op; na[nn]=(u16)a; nb[nn]=(u16)b; linid[nn]=0xFFFF; return nn++; }
static int has_cons(int op,int a,int b){
  if(op!=O_NOT && a>b){ int t=a;a=b;b=t; }
  u32 h=hmix((u32)op*0x9E3779B1u ^ (u32)a*0x85EBCA77u ^ (u32)b*0xC2B2AE3Du)&(CH-1);
  for(;;){ u16 e=ch[h]; if(!e) return 0; int m=e-1; if((nf[m]&F_OPM)==op && na[m]==a && nb[m]==b) return 1; h=(h+1)&(CH-1); }
}
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

static long cnt_emit;

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
static V notv(V a){
  if(a.n==NC) return a;
  if((nf[a.n]&F_OPM)==O_NOT) return MK(na[a.n], a.p^1);
  int before=nn; int n=cons(O_NOT,a.n,0);
  if(nn>before){ cnt_emit++; if(islin(a.n)){ nf[n]|=F_LIN|(isk(a.n)?0:F_K); linid[n]=linid[a.n]; } }
  return MK(n,a.p^1);
}
static V and2(V a,V b,int sel){
  if(a.n==NC) return a.p? b : K_(0);
  if(b.n==NC) return b.p? a : K_(0);
  if(a.n==b.n) return a.p==b.p? a : K_(0);
  int before=nn;
  if(a.p==0&&b.p==0){ int n=cons(O_AND,a.n,b.n); if(nn>before) cnt_emit++; return MK(n,0); }
  if(a.p==1&&b.p==1){ int n=cons(O_OR,a.n,b.n); if(nn>before) cnt_emit++; return MK(n,1); }
  int A=a.p==0?a.n:b.n, B=a.p==0?b.n:a.n;
  if(sel){ V na_=notv(MK(A,0)); int b2=nn; int n=cons(O_OR,na_.n,B); if(nn>b2) cnt_emit++; return MK(n,1); }
  int t=cons(O_AND,A,B); if(nn>before) cnt_emit++;
  return xorv(MK(A,0),MK(t,0));
}
static V andnot(V b1,V b2,int sel){ b1.p^=1; return and2(b1,b2,sel); }

static int cost_term(V b1,V b2){ if(b1.n==NC||b2.n==NC||b1.n==b2.n) return 0; return ((b1.p^1)==b2.p)?1:2; }
static int t_pol(V b1, V b2){
  V a=b1; a.p^=1; V b=b2;
  if(a.n==NC) return a.p ? b.p : 0;
  if(b.n==NC) return b.p ? a.p : 0;
  if(a.n==b.n) return a.p==b.p ? a.p : 0;
  return (a.p==1&&b.p==1) ? 1 : 0;
}

static inline int eval_next_round(const u64 P_lane[25], int next_r){
  int last = (next_r == NROUNDS - 1);
  u64 C[5], D[5];
  for(int x=0;x<5;x++) C[x] = P_lane[x] ^ P_lane[x+5] ^ P_lane[x+10] ^ P_lane[x+15] ^ P_lane[x+20];
  for(int x=0;x<5;x++) D[x] = C[(x+4)%5] ^ rotl64(C[(x+1)%5], 1);
  if(!last){
    int diff_sum = 0, ox_sum = 0;
    for(int Y=0;Y<5;Y++){
      u64 b[5];
      for(int X=0;X<5;X++){ int y=X, x=(3*Y+X)%5; b[X] = rotl64(P_lane[x+5*y] ^ D[x], ROT[x][y]); }
      diff_sum += pop64(b[0] ^ b[1]) + pop64(b[1] ^ b[2]) + pop64(b[2] ^ b[3])
                + pop64(b[3] ^ b[4]) + pop64(b[4] ^ b[0]);
      ox_sum += pop64((b[0] | b[1]) ^ (b[1] | b[2]) ^ (b[2] | b[3]) ^ (b[3] | b[4]) ^ (b[4] | b[0]));
    }
    return 2240 - (diff_sum >> 1) + ox_sum;
  } else {
    u64 b0 = rotl64(P_lane[0] ^ D[0], ROT[0][0]);
    u64 b1 = rotl64(P_lane[6] ^ D[1], ROT[1][1]);
    u64 b2 = rotl64(P_lane[12] ^ D[2], ROT[2][2]);
    u64 b3 = rotl64(P_lane[18] ^ D[3], ROT[3][3]);
    u64 b4 = rotl64(P_lane[24] ^ D[4], ROT[4][4]);
    u64 nb0 = ~b0, nb1 = ~b1, nb2 = ~b2, nb3 = ~b3, nb4 = ~b4;
    u64 is4 = (b0 & nb4 & ((nb2 & b3) | (nb1 & b2 & nb3))) | (nb0 & nb3 & b4 & (b1 ^ b2));
    u64 is6 = (nb4 & nb0 & ((nb1 & nb2 & nb3) | (b2 & (b1 | b3)))) | (b4 & ((b0 & nb3 & ~(b1 ^ b2)) | (b2 & b3 & (b0 | b1))));
    return 320 - pop64(is4) + pop64(is6);
  }
}

static V S[25][64], NS[25][64], Cc[5][64], Dd[5][64];
static u64 KL[25];
static int outnode[256];
static u64 PD[4];
static long nnot_rows, ntrick;
static u8 not_uses[MAXN];

typedef struct { u8 pm, s, f, selm; signed char bj; u8 rc; } Cand;

static int get_avail_mask(const V b[5]){
  int av = 0;
  for(int X=0;X<5;X++){
    if(b[X].n != NC && (not_uses[b[X].n] > 0 || (nf[b[X].n]&F_OPM) == O_NOT || has_cons(O_NOT, b[X].n, 0)))
      av |= (1 << X);
  }
  return av;
}

static int choice_tc(const V b[5], int needmask, Cand ch){
  V bb[5];
  for(int X=0;X<5;X++){ bb[X] = b[X]; if((ch.s >> X) & 1) bb[X].p ^= 1; }
  int tc = 0;
  for(int X=0;X<5;X++){
    if(!((needmask >> X) & 1)) continue;
    if(X == ch.bj){
      int k = (ch.bj + 1) % 5;
      int tp_k = t_pol(bb[(k+1)%5], bb[(k+2)%5]) ^ ((ch.selm >> k) & 1);
      int pk = b[k].p ^ ((ch.f >> k) & 1) ^ tp_k;
      tc += ((pk ^ 1) == bb[(ch.bj+2)%5].p) ? 1 : 2;
    } else {
      tc += cost_term(bb[(X+1)%5], bb[(X+2)%5]);
    }
  }
  return tc;
}

static int unuse_row(const V b[5], int needmask, Cand ch){
  int ou = ch.s | ch.f;
  int orc = choice_tc(b, needmask, ch);
  for(int X=0;X<5;X++){
    if((ou >> X) & 1){
      not_uses[b[X].n]--;
      if(not_uses[b[X].n] == 0 && (nf[b[X].n]&F_OPM) != O_NOT && !has_cons(O_NOT, b[X].n, 0)) orc++;
    }
  }
  return orc;
}

static void use_row(const V b[5], Cand ch){
  int nu = ch.s | ch.f;
  for(int X=0;X<5;X++) if((nu >> X) & 1) not_uses[b[X].n]++;
}

typedef struct { u8 s, req_f, req_sel, tc, bpm, mix; signed char bj; } SInfo;
static SInfo sinfo_tab[2][32][160];
static int nsinfo_tab[2][32];

static int build_sinfo(const V b[5], int distinct, int needmask, int rc_bit0, SInfo *out){
  int jmax = distinct ? 5 : 0;
  int nsi = 0;
  for(int bj=-1; bj<jmax; bj++){
    if(bj >= 0){
      int k = (bj + 1) % 5;
      if(!((needmask >> bj) & 1) || !((needmask >> k) & 1)) continue;
    }
    for(int s=0; s<32; s++){
      V bb[5]; int bad = 0;
      for(int X=0;X<5;X++){
        bb[X] = b[X];
        if((s >> X) & 1){ if(b[X].n == NC){ bad = 1; break; } bb[X].p ^= 1; }
      }
      if(bad) continue;
      int tc_base = 0, bpm_base = 0, mix_base = 0;
      for(int X=0;X<5;X++){
        if(X == bj || !((needmask >> X) & 1)) continue;
        int c = cost_term(bb[(X+1)%5], bb[(X+2)%5]);
        int tp = t_pol(bb[(X+1)%5], bb[(X+2)%5]);
        tc_base += c;
        if(c == 2) mix_base |= (1 << X);
        bpm_base |= ((b[X].p ^ tp ^ (X == 0 ? rc_bit0 : 0)) << X);
      }
      int fk_max = (bj < 0) ? 1 : 2;
      for(int fk_eff=0; fk_eff<fk_max; fk_eff++){
        int req_f = 0, req_sel = 0, tc = tc_base, base_pm = bpm_base, mix = mix_base;
        if(bj >= 0){
          int k = (bj + 1) % 5;
          int tp_k = t_pol(bb[(k+1)%5], bb[(k+2)%5]);
          if(fk_eff){
            if((mix_base >> k) & 1) req_sel = (1 << k);
            else req_f = (1 << k);
          }
          int pk = b[k].p ^ tp_k ^ fk_eff;
          int c_bj = ((pk ^ 1) == bb[(bj+2)%5].p) ? 1 : 2;
          int tp_bj = (c_bj == 1) ? (pk ^ 1) : 0;
          tc = tc_base + c_bj;
          mix = (mix_base & ~(1 << k)) | ((c_bj == 2) ? (1 << bj) : 0);
          base_pm = bpm_base ^ (fk_eff << k) ^ ((b[bj].p ^ tp_bj ^ (bj == 0 ? rc_bit0 : 0)) << bj);
        }
        if(tc <= 6){
          out[nsi].s = (u8)s; out[nsi].req_f = (u8)req_f; out[nsi].req_sel = (u8)req_sel;
          out[nsi].tc = (u8)tc; out[nsi].bpm = (u8)base_pm; out[nsi].mix = (u8)mix;
          out[nsi].bj = (signed char)bj;
          nsi++;
        }
      }
    }
  }
  return nsi;
}

static void init_sinfo(void){
  for(int li=0; li<2; li++){
    int needmask = li ? 0x0F : 0x1F;
    for(int p=0; p<32; p++){
      V b[5];
      for(int X=0; X<5; X++) b[X] = MK(X, (p >> X) & 1);
      nsinfo_tab[li][p] = build_sinfo(b, 1, needmask, 0, sinfo_tab[li][p]);
    }
  }
}

static void get_row_cands(const V b[5], int r, int Y, int z, int needmask, int max_rc, Cand *cands, int *ncands){
  int min_rc[32]; Cand best[32];
  for(int pm=0;pm<32;pm++) min_rc[pm] = 1<<29;
  int avail = get_avail_mask(b);
  int distinct = 1, p = 0;
  for(int X=0;X<5;X++){
    p |= (b[X].p << X);
    if(b[X].n == NC) distinct = 0;
    for(int X2=X+1;X2<5;X2++) if(b[X].n == b[X2].n) distinct = 0;
  }
  int rc_bit0 = (Y == 0) ? ((RC[r] >> z) & 1) : 0;
  SInfo local_si[32];
  const SInfo *si; int nsi;
  if(distinct){
    int li = (needmask == 0x0F) ? 1 : 0;
    si = sinfo_tab[li][p];
    nsi = nsinfo_tab[li][p];
  } else {
    nsi = build_sinfo(b, 0, needmask, 0, local_si);
    si = local_si;
  }
  for(int i=0; i<nsi; i++){
    int s = si[i].s, req_f = si[i].req_f, req_sel = si[i].req_sel;
    int tc = si[i].tc, base_pm = si[i].bpm ^ rc_bit0, mix = si[i].mix;
    int bj = si[i].bj;
    int u_base = s | req_f;
    int base_rc = tc + pop64((u64)(u_base & ~avail));
    if(base_rc > max_rc) continue;
    int free_flip = ((s | avail | mix) & needmask) & ~(bj < 0 ? 0 : (1 << ((bj + 1) % 5)));
    for(int sub=free_flip; ; sub=(sub-1)&free_flip){
      int pm = base_pm ^ sub;
      if(base_rc < min_rc[pm]){
        min_rc[pm] = base_rc;
        best[pm].pm = (u8)pm;
        best[pm].s = (u8)s;
        best[pm].f = (u8)(req_f | (sub & ~mix));
        best[pm].selm = (u8)(req_sel | (sub & mix));
        best[pm].bj = (signed char)bj;
        best[pm].rc = (u8)base_rc;
      }
      if(sub == 0) break;
    }
  }
  int k = 0;
  for(int pm=0;pm<32;pm++) if(min_rc[pm] <= max_rc) cands[k++] = best[pm];
  *ncands = k;
}

static inline void set_row_P(u64 P_lane[25], int Y, int z, u8 pm){
  u64 mask = ~(1ULL << z);
  int base = 5 * Y;
  for(int X=0;X<5;X++) P_lane[base+X] = (P_lane[base+X] & mask) | ((u64)((pm>>X)&1) << z);
}

static int try_pair_move(V B_row[5][64][5], Cand chosen[5][64], u64 P_lane[25],
                         int r, int needmask, int Y1, int z1, int Y2, int z2, int *cur_next_score){
  if(Y1==Y2 && z1==z2) return 0;
  V *b1 = B_row[Y1][z1], *b2 = B_row[Y2][z2];
  if(r == 1 && z1 != z2){
    for(int i=0;i<5;i++) if(b1[i].n != NC) for(int j=0;j<5;j++) if(b1[i].n == b2[j].n) return 0;
  }
  Cand och1 = chosen[Y1][z1], och2 = chosen[Y2][z2];
  int orc1 = unuse_row(b1, needmask, och1);
  int orc2 = unuse_row(b2, needmask, och2);
  Cand c1[32], c2[32]; int nc1=0, nc2=0;
  get_row_cands(b1, r, Y1, z1, needmask, orc1 + 1, c1, &nc1);
  get_row_cands(b2, r, Y2, z2, needmask, orc2 + 1, c2, &nc2);

  Cand bch1 = och1, bch2 = och2;
  int best_total = orc1 + orc2 + *cur_next_score;
  int best_next_score = *cur_next_score;
  int improved = 0;

  for(int i=0; i<nc1; i++){
    set_row_P(P_lane, Y1, z1, c1[i].pm);
    for(int j=0; j<nc2; j++){
      if(c1[i].rc + c2[j].rc > orc1 + orc2 + 1) continue;
      set_row_P(P_lane, Y2, z2, c2[j].pm);
      int next_sc = eval_next_round(P_lane, r+1);
      if(c1[i].rc + c2[j].rc + next_sc < best_total){
        best_total = c1[i].rc + c2[j].rc + next_sc;
        best_next_score = next_sc;
        bch1 = c1[i]; bch2 = c2[j];
        improved = 1;
      }
    }
  }
  chosen[Y1][z1] = bch1; set_row_P(P_lane, Y1, z1, bch1.pm); use_row(b1, bch1);
  chosen[Y2][z2] = bch2; set_row_P(P_lane, Y2, z2, bch2.pm); use_row(b2, bch2);
  *cur_next_score = best_next_score;
  return improved;
}

static void build(void){
  nn=0; nform=0; cnt_emit=0; nnot_rows=0; ntrick=0;
  memset(fh,0,sizeof fh); memset(ch,0,sizeof ch);
  for(int j=0;j<256;j++){ int n=newnode(O_IN,0,0); u64 m[4]={0,0,0,0}; m[j>>6]=1ULL<<(j&63); nf[n]|=F_LIN; linid[n]=(u16)fadd(m,n); }
  for(int l=0;l<25;l++) for(int z=0;z<64;z++) S[l][z]=K_((KL[l]>>z)&1);
  for(int z=0;z<64;z++){
    S[1][z]=MK(z,(KL[1]>>z)&1); S[11][z]=MK(64+z,(KL[11]>>z)&1);
    S[9][z]=MK(128+z,(KL[9]>>z)&1); S[14][z]=MK(192+z,(KL[14]>>z)&1);
  }
  for(int z=0;z<64;z++){
    S[6][z]=xorv(xorv(MK(z,0),MK(64+z,0)),K_((KL[6]>>z)&1));
    S[4][z]=xorv(xorv(MK(128+z,0),MK(192+z,0)),K_((KL[4]>>z)&1));
  }
  for(int r=0;r<NROUNDS;r++){
    int last=(r==NROUNDS-1);
    for(int x=0;x<5;x++){ V s=S[x][63]; for(int y=1;y<5;y++) s=xorv(s,S[x+5*y][63]); Cc[x][63]=s; }
    for(int z=0;z<64;z++){
      if(z<63) for(int x=0;x<5;x++){ V s=S[x][z]; for(int y=1;y<5;y++) s=xorv(s,S[x+5*y][z]); Cc[x][z]=s; }
      for(int x=0;x<5;x++) Dd[x][z]=xorv(Cc[(x+4)%5][z],Cc[(x+1)%5][(z+63)&63]);
    }
    int nY=last?1:5, needmask=last?0x0F:0x1F;
    int nn0=nn, nf0=nform; long ce0=cnt_emit;
    static V B_row[5][64][5];
    for(int Y=0;Y<nY;Y++) for(int z=0;z<64;z++) for(int X=0;X<5;X++){
      int y=X, x=(3*Y+X)%5; int zz=(z-ROT[x][y]+64)&63;
      B_row[Y][z][X] = xorv(S[x+5*y][zz],Dd[x][zz]);
    }
    static Cand chosen[5][64];
    u64 P_lane[25];
    memset(P_lane, 0, sizeof P_lane);
    memset(not_uses, 0, sizeof not_uses);
    for(int Y=0;Y<nY;Y++) for(int z=0;z<64;z++){
      Cand cands[32]; int ncands = 0;
      get_row_cands(B_row[Y][z], r, Y, z, needmask, 20, cands, &ncands);
      int best_k = 0;
      for(int k=1; k<ncands; k++) if(cands[k].rc < cands[best_k].rc) best_k = k;
      chosen[Y][z] = cands[best_k];
      use_row(B_row[Y][z], cands[best_k]);
      set_row_P(P_lane, Y, z, cands[best_k].pm);
    }

    if(r >= 1 && r < NROUNDS - 1){
      int cur_next_score = eval_next_round(P_lane, r+1);
      int no_imp = 0;
      for(int iter=0; iter<15; iter++){
        int imp = 0;
        if(no_imp >= 3) break;
        for(int Y=0;Y<nY;Y++) for(int z=0;z<64;z++){
          V *b = B_row[Y][z];
          Cand och = chosen[Y][z];
          int orc = unuse_row(b, needmask, och);
          Cand cands[32]; int ncands = 0;
          get_row_cands(b, r, Y, z, needmask, orc + 1, cands, &ncands);
          Cand bch = och;
          int best_total = orc + cur_next_score, best_next_score = cur_next_score;
          for(int k=0; k<ncands; k++){
            set_row_P(P_lane, Y, z, cands[k].pm);
            int next_sc = eval_next_round(P_lane, r+1);
            if(cands[k].rc + next_sc < best_total){
              best_total = cands[k].rc + next_sc; best_next_score = next_sc;
              bch = cands[k]; imp = 1;
            }
          }
          chosen[Y][z] = bch; set_row_P(P_lane, Y, z, bch.pm); use_row(b, bch);
          cur_next_score = best_next_score;
        }
        no_imp = imp ? 0 : no_imp + 1; if(no_imp >= 3) break; imp = 0;

        for(int z=0; z<64; z++){
          int old_rc[5]; Cand c[5][32]; int nc[5];
          for(int Y=0; Y<5; Y++){
            old_rc[Y] = unuse_row(B_row[Y][z], needmask, chosen[Y][z]);
            get_row_cands(B_row[Y][z], r, Y, z, needmask, old_rc[Y], c[Y], &nc[Y]);
          }
          int old_slice_rc = old_rc[0]+old_rc[1]+old_rc[2]+old_rc[3]+old_rc[4];
          int best_total = old_slice_rc + cur_next_score, best_next_score = cur_next_score;
          Cand bch[5];
          for(int Y=0;Y<5;Y++) bch[Y] = chosen[Y][z];
          for(int i0=0;i0<nc[0];i0++){
            set_row_P(P_lane, 0, z, c[0][i0].pm);
            for(int i1=0;i1<nc[1];i1++){
              set_row_P(P_lane, 1, z, c[1][i1].pm);
              for(int i2=0;i2<nc[2];i2++){
                set_row_P(P_lane, 2, z, c[2][i2].pm);
                for(int i3=0;i3<nc[3];i3++){
                  set_row_P(P_lane, 3, z, c[3][i3].pm);
                  for(int i4=0;i4<nc[4];i4++){
                    set_row_P(P_lane, 4, z, c[4][i4].pm);
                    int sum_rc = c[0][i0].rc + c[1][i1].rc + c[2][i2].rc + c[3][i3].rc + c[4][i4].rc;
                    int next_sc = eval_next_round(P_lane, r+1);
                    if(sum_rc + next_sc < best_total){
                      best_total = sum_rc + next_sc; best_next_score = next_sc;
                      bch[0]=c[0][i0]; bch[1]=c[1][i1]; bch[2]=c[2][i2]; bch[3]=c[3][i3]; bch[4]=c[4][i4];
                      imp = 1;
                    }
                  }
                }
              }
            }
          }
          cur_next_score = best_next_score;
          for(int Y=0;Y<5;Y++){
            chosen[Y][z] = bch[Y]; set_row_P(P_lane, Y, z, bch[Y].pm); use_row(B_row[Y][z], bch[Y]);
          }
        }
        no_imp = imp ? 0 : no_imp + 1; if(no_imp >= 3) break; imp = 0;

        for(int z=0; z<64; z++)
          for(int Y1=0; Y1<4; Y1++) for(int Y2=Y1+1; Y2<5; Y2++)
            imp |= try_pair_move(B_row, chosen, P_lane, r, needmask, Y1, z, Y2, z, &cur_next_score);
        no_imp = imp ? 0 : no_imp + 1; if(no_imp >= 3) break; imp = 0;

        for(int pass=0; pass<2; pass++){
          int imp4 = 0;
          for(int z=0; z<64; z++)
            for(int Y1=0; Y1<5; Y1++) for(int Y2=0; Y2<5; Y2++) if(r>1 || Y1==Y2)
              imp4 |= try_pair_move(B_row, chosen, P_lane, r, needmask, Y1, z, Y2, (z+1)&63, &cur_next_score);
          imp |= imp4;
          if(!imp4) break;
        }
        no_imp = imp ? 0 : no_imp + 1; if(no_imp >= 3) break;
      }
    }

    for(int i=0;i<CH;i++) if(ch[i]>nn0) ch[i]=0;
    for(int i=0;i<FH;i++) if(fh[i]>nf0) fh[i]=0;
    nn=nn0; nform=nf0; cnt_emit=ce0;
    for(int Y=0;Y<nY;Y++) for(int z=0;z<64;z++){
      V b[5], fb[5], orig_b[5];
      for(int X=0;X<5;X++){
        int y=X, x=(3*Y+X)%5; int zz=(z-ROT[x][y]+64)&63;
        orig_b[X] = xorv(S[x+5*y][zz], Dd[x][zz]);
      }
      Cand ch = chosen[Y][z];
      for(int X=0;X<5;X++){
        if(((ch.s|ch.f)>>X)&1) nnot_rows++;
        b[X] = ((ch.s>>X)&1) ? notv(orig_b[X]) : orig_b[X];
        fb[X] = ((ch.f>>X)&1) ? notv(orig_b[X]) : orig_b[X];
      }
      int k = (ch.bj + 1) % 5;
      if(ch.bj >= 0){
        ntrick++;
        V t = andnot(b[(k+1)%5], b[(k+2)%5], (ch.selm >> k) & 1);
        NS[k+5*Y][z] = xorv(fb[k], t);
      }
      for(int X=0;X<5;X++) if(needmask>>X&1){
        if(ch.bj >= 0 && X == k) continue;
        V t1 = (X == ch.bj) ? NS[k+5*Y][z] : b[(X+1)%5];
        V t = andnot(t1, b[(X+2)%5], (ch.selm >> X) & 1);
        NS[X+5*Y][z] = xorv(fb[X], t);
      }
    }
    for(int z=0;z<64;z++) NS[0][z].p^=(RC[r]>>z)&1;
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

#define NREG 2304
static u16 freestk[NREG]; static int nfree;
static u16 outdef[256];
static int alloc_emit(int emit){
  u16 *last=ch, *reg=linid;
  for(int i=0;i<nn;i++) last[i]=0;
  for(int i=256;i<nn;i++) if(nf[i]&F_LIVE){ last[na[i]]=(u16)i; if((nf[i]&F_OPM)!=O_NOT) last[nb[i]]=(u16)i; }
  for(int j=0;j<256;j++){ last[outnode[j]]=0xFFFF; outdef[j]=(u16)outnode[j]; }
  static u8 outof[MAXN/8+1]; memset(outof,0,sizeof outof);
  static u8 regbusy[NREG]; memset(regbusy,0,sizeof regbusy);
  static short outj[MAXN];
  for(int j=0;j<256;j++){ outof[outnode[j]>>3]|=1<<(outnode[j]&7); outj[outnode[j]]=(short)j; }
  nfree=0; for(int r=NREG-1;r>=256;r--) freestk[nfree++]=(u16)r;
  long live=0; maxlive=0; maxreg=0;
  for(int j=0;j<256;j++){ reg[j]=(u16)j; if(last[j]){ regbusy[j]=1; live++; } }
  if(live>maxlive) maxlive=live;
#ifdef USE_LIBC
  FILE *fp = NULL;
  if(emit){ fp = fopen("prog.bin", "wb"); if(!fp) die("open prog.bin"); }
#else
  int fd=-1; if(emit){ fd=fopen_w("prog.bin"); if(fd<0) die("open prog.bin"); }
#endif
  static u8 eb[4000]; int el=0; long ninstr=0;
  for(int i=256;i<nn;i++){
    if(!(nf[i]&F_LIVE)) continue;
    int op=nf[i]&F_OPM; int a=na[i], b=(op==O_NOT)?a:nb[i];
    int ops[2]={a,b};
    for(int k=0;k<2;k++){ int o=ops[k]; if(k==1&&o==a) break; if(last[o]==i){ int r=reg[o]; regbusy[r]=0; live--; if(r>=256) freestk[nfree++]=(u16)r; } }
    int dst;
    if(outof[i>>3]>>(i&7)&1){ dst=outj[i]; if(regbusy[dst]) die("output register busy"); }
    else if(nfree>0) dst=freestk[--nfree];
    else { dst=-1; for(int r=0;r<256;r++) if(!regbusy[r] && outdef[r]>=last[i]) { dst=r; break; } if(dst<0) die("out of registers"); }
    regbusy[dst]=1; live++; reg[i]=(u16)dst; if(live>maxlive) maxlive=live; if(dst+1>maxreg) maxreg=dst+1;
    if(last[i]==0) die("live node without use");
    if(emit){
      int code= op==O_XOR?0: op==O_AND?1: op==O_OR?2: 3;
      u64 w=(u64)code | (u64)dst<<3 | (u64)reg[a]<<15 | (u64)(op==O_NOT?0:reg[nb[i]])<<27;
      for(int k=0;k<5;k++) eb[el++]=(u8)(w>>(8*k));
      if(el>=3995){
#ifdef USE_LIBC
        fwrite(eb, 1, el, fp);
#else
        sc3(1,fd,(i64)eb,el);
#endif
        el=0;
      }
    }
    ninstr++;
  }
  if(emit){
#ifdef USE_LIBC
    if(el) fwrite(eb, 1, el, fp);
    fclose(fp);
#else
    if(el) sc3(1,fd,(i64)eb,el);
    fclose_(fd);
#endif
  }
  return (int)ninstr;
}

static void set_consts(int trial){
  u64 M64 = ~0ULL;
  for(int l=0;l<25;l++) KL[l]=0;
  KL[16]=0x8000000000000006ULL;
  u64 W=(trial&1)?M64:0, r0=(trial&2)?M64:0, r1=(trial&4)?M64:0, r2=(trial&8)?M64:0, r3=(trial&16)?M64:0;
  KL[0]=0; KL[5]=M64; KL[10]=M64; KL[15]=M64;
  KL[3]=0; KL[8]=0; KL[13]=W;
  KL[2]=rotl64(W,3); KL[7]=0; KL[12]=0;
  KL[1]=r0; KL[11]=r1; KL[6]=r0^r1^rotl64(W,1)^KL[16];
  KL[9]=r2; KL[14]=r3; KL[4]=r2^r3^M64^rotl64(W,2);
}

static int work(int argc,char **argv){
  init_sinfo();
  int ntr= argc>1? atoi_(argv[1]) : 32; if(ntr<1) ntr=1;
  int t0= argc>2? atoi_(argv[2]) : 0;
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
#ifdef USE_LIBC
  fp_out=fopen("meta.txt","w");
#else
  fd_out=fopen_w("meta.txt");
#endif
  os("trial "); ou(bestt); oc('\n');
  for(int l=0;l<25;l++){ os("lane "); ou(l); oc(' '); ox(KL[l]); oc('\n'); }
  os("varlanes 1 11 9 14 ; lane6 = u0^u1^K6 ; lane4 = u2^u3^K4\n");
  os("pd "); for(int i=0;i<4;i++){ ox(PD[i]); oc(i<3?' ':'\n'); }
  os("ninstr "); ou(ninstr); oc('\n');
  oflush();
#ifdef USE_LIBC
  fclose(fp_out); fp_out=NULL;
#else
  fclose_(fd_out);
#endif
  for(int pass=0;pass<2;pass++){
#ifdef USE_LIBC
    fp_out = pass ? stdout : fopen("ledger.txt","w");
#else
    fd_out = pass ? 1 : fopen_w("ledger.txt");
#endif
    os("LS1 step ledger (256 lanes, one chain step, 6 rounds)\n");
    os("XOR "); ou(cnt[O_XOR]); oc('\n');
    os("AND "); ou(cnt[O_AND]); oc('\n');
    os("OR  "); ou(cnt[O_OR]); oc('\n');
    os("NOT "); ou(cnt[O_NOT]); os("  (row complements chosen pre-DCE: "); ou(nnot_rows); os(")\n");
    os("LOAD 0\nSTORE 0\nTOTAL "); ou(tot); oc('\n');
    os("TRICKROWS "); ou(ntrick); oc('\n');
    os("feed NOTs 0 (digest polarity folded into the chain function: F(u)=H(m(u))^PD)\n");
    os("nodes created pre-DCE "); ou(pre); os(" ; nodes "); ou(nn); os(" ; linear forms "); ou(nform); oc('\n');
    os("max live values "); ou(maxlive); os(" ; registers used "); ou(maxreg); os(" (limit 2304)\n");
    os("constants trial "); ou(bestt); os(" of "); ou(ntr); oc('\n');
    oflush();
#ifdef USE_LIBC
    if(!pass){ fclose(fp_out); fp_out=NULL; }
#else
    if(!pass) fclose_(fd_out);
#endif
  }
  return maxreg>NREG ? 2 : 0;
}
#ifdef USE_LIBC
int main(int argc, char **argv){ return work(argc, argv); }
#else
int cmain(long *sp){ int argc=(int)sp[0]; char **argv=(char**)(sp+1); return work(argc,argv); }
#endif
```

`selftest.c`:

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
#ifndef RR
#define RR 6
#endif

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
  L[1]=u[0]^KL[1]; L[11]=u[1]^KL[11]; L[6]=u[0]^u[1]^KL[6];
  L[9]=u[2]^KL[9]; L[14]=u[3]^KL[14]; L[4]=u[2]^u[3]^KL[4];
  for(int i=0;i<128;i++) m[i]=(uint8_t)(L[i/8]>>(8*(i%8)));
}
static void Fref(const u64 u[4], u64 o[4]){
  uint8_t m[128], d[32]; msg_of(u,m); sha3_256r(m,128,RR,d);
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
      sha3_256r(m,len,24,d24); sha3_256r(m,len,RR,d6);
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

Output of the run (`ledger.txt`) and of the self-test:

```
LS1 step ledger (256 lanes, one chain step, 6 rounds)
XOR 19052
AND 3743
OR  2913
NOT 659  (row complements chosen pre-DCE: 1007)
LOAD 0
STORE 0
TOTAL 26367
TRICKROWS 1213
feed NOTs 0 (digest polarity folded into the chain function: F(u)=H(m(u))^PD)
nodes created pre-DCE 26367 ; nodes 26623 ; linear forms 1088
max live values 1925 ; registers used 2181 (limit 2304)
constants trial 27 of 32
KAT: 300/300 match hashlib.sha3_256 (24 rounds); 300/300 match ls1.digest (6 rounds)
selftest: 8192 chained evaluations (8 batches x 256 trails x 4 steps), 0 mismatches, 26367 instructions
```

## Appendix C. The measured checks of H_rand (hrand_test.c, proj_test.c) and register spill sensitivity (spill.py)

`hrand_test.c`:

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

`proj_test.c`:

```c
/* proj_test.c: the proj-w256 trial at scale: NT trials of 256 random points and 8 chained full-width steps each;
   a trial succeeds when two of its 2,048 evaluated inputs have images agreeing on the 22 low bits. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
typedef uint64_t u64;
typedef struct { u64 w[4]; } w256;
static w256 R[2304];
typedef struct { uint8_t op; uint16_t d,a,b; } ins_t;
static ins_t *P; static int NP;
static void load(void){
  FILE *f=fopen("prog.bin","rb"); if(!f){perror("prog.bin");exit(1);}
  fseek(f,0,SEEK_END); long sz=ftell(f); fseek(f,0,SEEK_SET);
  NP=sz/5; P=malloc(NP*sizeof(ins_t));
  for(int i=0;i<NP;i++){
    unsigned char buf[5]; if(fread(buf,1,5,f)!=5) exit(1);
    u64 v=0; for(int k=0;k<5;k++) v|=(u64)buf[k]<<(8*k);
    P[i].op=v&7; P[i].d=(v>>3)&4095; P[i].a=(v>>15)&4095; P[i].b=(v>>27)&4095;
  }
  fclose(f);
}
static void run_prog(void){
  for(int i=0;i<NP;i++){
    ins_t s=P[i]; u64 *d=R[s.d].w,*a=R[s.a].w,*b=R[s.b].w;
    switch(s.op){
      case 0: d[0]=a[0]^b[0]; d[1]=a[1]^b[1]; d[2]=a[2]^b[2]; d[3]=a[3]^b[3]; break;
      case 1: d[0]=a[0]&b[0]; d[1]=a[1]&b[1]; d[2]=a[2]&b[2]; d[3]=a[3]&b[3]; break;
      case 2: d[0]=a[0]|b[0]; d[1]=a[1]|b[1]; d[2]=a[2]|b[2]; d[3]=a[3]|b[3]; break;
      case 3: d[0]=~a[0]; d[1]=~a[1]; d[2]=~a[2]; d[3]=~a[3]; break;
    }
  }
}
static u64 sm;
static u64 rnd(void){ u64 z=(sm+=0x9E3779B97F4A7C15ULL); z=(z^(z>>30))*0xBF58476D1CE4E5B9ULL; z=(z^(z>>27))*0x94D049BB133111EBULL; return z^(z>>31); }
static int cmpu(const void*a,const void*b){ uint32_t x=*(const uint32_t*)a,y=*(const uint32_t*)b; return x<y?-1:x>y; }
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

`spill.py`:

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

Output of `spill.py prog.bin`:

```
registers 1024: loads   5362 stores   4346 -> step 26367 + 9708 = 36075 ops (score 124.475, +0.45)
registers  512: loads   9213 stores   6307 -> step 26367 + 15520 = 41887 ops (score 124.690, +0.66)
registers  256: loads  12663 stores   7684 -> step 26367 + 20347 = 46714 ops (score 124.847, +0.82)
registers   64: loads  17711 stores   8419 -> step 26367 + 26130 = 52497 ops (score 125.014, +0.99)
```

## Appendix D. The other code (other4.py), its tests (other4_test.py) and their results

### D.1 other4.py: the other code, the machine and the counts

`params.json` of this package:

```
{"NR": 6, "HF": 111, "DPLO": 145, "DK": 10, "DT": 704, "S": 23088, "U": 92352, "SB": 15, "IDB": 17, "W": 633825300114114700748351602688, "J": 62557, "LRC": 39650209299238673334714631209353216, "Tb": 1326272364423520456082274405230575616, "HMAX": 44830965663517622421370989484965889, "PFLO": 240, "PFN": 16}
```

```python
#!/usr/bin/env python3
# other4.py - the non-straight-line code of LS1 (setup, loop control, hit handler, DP handler with the packed table,
# restart, replay, final output), written as real instructions of the machine of proof.md Section 3.5,
# plus the machine (an interpreter that executes the emitted bytes) and the counting of the operations.
#
#   python3 other4.py build [meta.txt]    reads params.json (NR, S, U, SB, IDB, LRC, Tb, HMAX, DPLO, DK, DT, PFLO, PFN), writes other.bin
#                                          (the 32-byte instructions), pf.bin (the 15 prefilter ORs, 5 bytes each), data.bin
#                                          (the 16-word data image from meta.txt) and counts.txt (instruction counts and the
#                                          operation count of every routine, read from the emitted code)
#   other4_test.py                         routine tests and end-to-end runs of the emitted program (reduced width)
#
# Table: S words of 256 bits, four records of 64 bits per word (bits 64 k .. 64 k + 63); a record is
#   1 | (bits 0..KEYB-1 of the trail's end) << 1 | (trail number) << (KEYB + 1), KEYB = 63 - IDB, never zero; an empty record
#   is zero.  Every probe loads the whole word and extracts each record with charged shifts and masks; an insertion rewrites
#   the word.
# Distinguished point (DP): the point x (256-bit value, bit j = plane j) is a DP when x < THR, THR = DT << (DPLO - DK):
#   the planes DPLO..255 are zero and the DK planes below them, read as a number, are less than DT.  theta = DT 2^-(256-DPLO+DK).
#   No trail is cut: a walk runs until its DP; the replay refuses trails of more than LRC evaluations.
#
# Machine (collision-frontier-v5 256-bit word RAM, the declared register file of 2,192 registers R0..R2191):
#   every instruction below costs one word operation, except PERM, which costs one unit (UNIT = 271 NR operations, the model's
#   rule: one selected-round sponge permutation is one unit).  Straight-line instructions (5 bytes: XOR AND OR NOT on
#   registers) cost one operation each.  Other instructions are 32 bytes: op(1) d(2) a(2) b(2) 0(1) imm(24, 192 bits).
#   Words are 256 bits, arithmetic is mod 2^256, shifts take amount R[b] & 255 (or an immediate), compares give 0 or 1,
#   a conditional branch tests a register for zero and is always the instruction right after the compare that set it
#   (audited below), memory M[] is word addressed with address R[a] + imm, PERM a applies Keccak-f rounds 0..NR-1 to the
#   25 lanes in R[a]..R[a+6] (lane l = bits 64 (l mod 4) .. +63 of word R[a + l div 4]).
#   The straight-line block sits in code memory in front of instruction SLPOS: it is entered by fall-through or by a
#   jump to it, has no branches, and control leaves it by fall-through into instruction SLPOS.
import sys, struct, hashlib, os, json

M256 = (1 << 256) - 1
M64 = (1 << 64) - 1
PARAMS = json.load(open(os.environ.get('LS1_PARAMS', 'params.json')))
NR = PARAMS['NR']                                  # rounds of the target
UNIT = 271 * NR                                    # the cost model's price of one NR-round permutation (word operations)
RB, RPW = 64, 4                                    # record width; records per word
RM = (1 << RB) - 1


def keyb(Pm): return RB - 1 - Pm['IDB']            # key bits of a record: 1 + KEYB + IDB = 64


def thr(Pm): return Pm['DT'] << (Pm['DPLO'] - Pm['DK'])    # the DP is x < THR (DK = 0: DT = 1)

# ---- ISA ----
XOR, AND, OR, NOT, ADD, SUB, SHL, SHR, EQ, LT, MOV = range(11)
ADDI, SUBI, SHLI, SHRI, ANDI, EQI, LTI, MOVI = range(11, 19)
LD, ST, LDA, BNZ, BZ, JMP, JAL, JR, RND, PERM, HALT = range(19, 30)
NAMES = 'XOR AND OR NOT ADD SUB SHL SHR EQ LT MOV ADDI SUBI SHLI SHRI ANDI EQI LTI MOVI LD ST LDA BNZ BZ JMP JAL JR RND PERM HALT'.split()
CMPOPS = (EQ, LT, EQI, LTI)

# ---- registers ----
C, NXT, IDN, RHO, ONES, PF, H, LR, LR2, ZERO = range(2181, 2191)   # state (2,181..2,190; 2,191 spare)
(L, DPM, C1, ACC, TT, REC, SLOT, TR, F, X, Y, LV, NP, NM, ONEB, V, MN, E, PTR, SS, ID, STV) = range(256, 278)
(P, Q, N, MM, LA, LB, UU, FF, PDR, X0, X1, X2, X3, TQ, FP) = range(280, 295)
Z = 295
W0 = 300                                                              # W0..W6, the 1600-bit state of evalF
NREGS = 2192


class Asm:
    def __init__(s):
        s.ins = []; s.lab = {}; s.fix = []

    def pc(s): return len(s.ins)

    def label(s, n):
        assert n not in s.lab, n
        s.lab[n] = len(s.ins)

    def e(s, op, d=0, a=0, b=0, imm=0, tgt=None):
        s.ins.append([op, d, a, b, imm])
        if tgt is not None: s.fix.append((len(s.ins) - 1, tgt))

    def resolve(s):
        for i, t in s.fix: s.ins[i][4] = s.lab[t]
        for x in s.ins: assert 0 <= x[4] < 1 << 192 and max(x[1:4]) < 2192

    # plain instructions
    def xor(s, d, a, b): s.e(XOR, d, a, b)
    def and_(s, d, a, b): s.e(AND, d, a, b)
    def or_(s, d, a, b): s.e(OR, d, a, b)
    def not_(s, d, a): s.e(NOT, d, a)
    def add(s, d, a, b): s.e(ADD, d, a, b)
    def sub(s, d, a, b): s.e(SUB, d, a, b)
    def shl(s, d, a, b): s.e(SHL, d, a, b)
    def shr(s, d, a, b): s.e(SHR, d, a, b)
    def mov(s, d, a): s.e(MOV, d, a)
    def addi(s, d, a, i): s.e(ADDI, d, a, 0, i)
    def subi(s, d, a, i): s.e(SUBI, d, a, 0, i)
    def shli(s, d, a, i): s.e(SHLI, d, a, 0, i)
    def shri(s, d, a, i): s.e(SHRI, d, a, 0, i)
    def andi(s, d, a, i): s.e(ANDI, d, a, 0, i)
    def movi(s, d, i): s.e(MOVI, d, 0, 0, i)
    def ld(s, d, a, i): s.e(LD, d, a, 0, i)
    def st(s, a, i, b): s.e(ST, 0, a, b, i)
    def lda(s, d, i): s.e(LDA, d, 0, 0, i)
    def rnd(s, d): s.e(RND, d)
    def permute(s, a): s.e(PERM, 0, a)
    def halt(s, code): s.e(HALT, 0, 0, 0, code)
    def jmp(s, t): s.e(JMP, tgt=t)
    def jal(s, d, t): s.e(JAL, d, tgt=t)
    def jr(s, a): s.e(JR, 0, a)

    # compare + branch pairs (a branch is always right after its compare)
    def _br(s, brop, t): s.e(brop, 0, F, 0, 0, t)
    def jeq(s, a, b, t): s.e(EQ, F, a, b); s._br(BNZ, t)
    def jne(s, a, b, t): s.e(EQ, F, a, b); s._br(BZ, t)
    def jeqi(s, a, i, t): s.e(EQI, F, a, 0, i); s._br(BNZ, t)
    def jnei(s, a, i, t): s.e(EQI, F, a, 0, i); s._br(BZ, t)
    def jlt(s, a, b, t): s.e(LT, F, a, b); s._br(BNZ, t)
    def jge(s, a, b, t): s.e(LT, F, a, b); s._br(BZ, t)
    def jlti(s, a, i, t): s.e(LTI, F, a, 0, i); s._br(BNZ, t)
    def jgei(s, a, i, t): s.e(LTI, F, a, 0, i); s._br(BZ, t)


def build_state(A, MISC):
    """W0..W6 := the 1600-bit state of the one-block message m(u), u in UU (26 instructions)."""
    for i in range(7): A.lda(W0 + i, MISC + i)
    A.andi(X0, UU, M64); A.shri(X1, UU, 64); A.andi(X1, X1, M64); A.shri(X2, UU, 128); A.andi(X2, X2, M64); A.shri(X3, UU, 192)
    A.shli(TQ, X0, 64); A.xor(W0, W0, TQ)                    # lane 1  = u0 ^ K1
    A.shli(TQ, X1, 192); A.xor(W0 + 2, W0 + 2, TQ)           # lane 11 = u1 ^ K11
    A.shli(TQ, X2, 64); A.xor(W0 + 2, W0 + 2, TQ)            # lane 9  = u2 ^ K9
    A.shli(TQ, X3, 128); A.xor(W0 + 3, W0 + 3, TQ)           # lane 14 = u3 ^ K14
    A.xor(TQ, X0, X1); A.shli(TQ, TQ, 128); A.xor(W0 + 1, W0 + 1, TQ)   # lane 6  = u0 ^ u1 ^ K6
    A.xor(TQ, X2, X3); A.xor(W0 + 1, W0 + 1, TQ)                        # lane 4  = u2 ^ u3 ^ K4


def program(Pm):
    """Pm: S (table words), U (trail limit), SB (slot bits), IDB (trail number bits), LRC (replay cap), Tb, HMAX, DPLO, DK, DT,
    PFLO, PFN, WTEST (None or width)."""
    S, U, SB, LRC, Tb, HMAX = Pm['S'], Pm['U'], Pm['SB'], Pm['LRC'], Pm['Tb'], Pm['HMAX']
    DPLO, DK, DT, PFLO, PFN, WT = Pm['DPLO'], Pm['DK'], Pm['DT'], Pm['PFLO'], Pm['PFN'], Pm.get('WTEST')
    IDB = Pm['IDB']; KEYB = keyb(Pm); THR = thr(Pm)
    assert (1 << SB) <= 2 * S and S % 8 == 0 and PFLO > DPLO + 1 and U <= RPW * S and U <= 1 << IDB and (WT or DPLO - DK > KEYB)
    assert (DK == 0 and DT == 1) or (DK >= 1 and 0 < DT < 1 << DK and DPLO >= DK)
    LID, LST, MISC = S, S + 256, S + 512
    OUT = MISC + 8
    A = Asm()
    # ---------------- setup ----------------
    A.label('start')
    A.rnd(RHO); A.movi(IDN, 256); A.movi(H, 0); A.movi(C, 0); A.movi(ZERO, 0); A.not_(ONES, ZERO)
    A.movi(PTR, 0)
    A.label('clr')                                           # TAB := 0, eight words per pass
    for k in range(8): A.st(PTR, k, ZERO)
    A.addi(PTR, PTR, 8); A.jlti(PTR, S, 'clr')
    A.movi(L, 0)
    A.label('iw')                                            # for l < 256: LID[l] := l; LST[l] := 0; lane l := rho + l
    A.add(NP, RHO, L); A.st(L, LID, L); A.st(L, LST, ZERO); A.jal(LR, 'setwalk')
    A.addi(L, L, 1); A.jlti(L, 256, 'iw')
    # ---------------- the loop: the straight line (SLPOS) then the tests ----------------
    A.label('loop')
    A.jeq(PF, ONES, 'cont')                                  # prefilter test (2)
    # ---------------- hit: some walk has planes PFLO..PFLO+PFN-1 zero ----------------
    A.label('hit')
    A.addi(H, H, 1); A.jlti(H, HMAX + 1, 'h1'); A.halt(10); A.label('h1')      # hit counter and abort (F5)
    A.or_(SS, DPLO, DPLO + 1)
    for j in range(DPLO + 2, PFLO): A.or_(SS, SS, j)         # OR of the planes DPLO..PFLO-1
    A.or_(DPM, PF, SS); A.not_(DPM, DPM)                     # DPM: walks with planes DPLO..255 zero
    if DK:                                                   # keep the walks whose planes DPLO-1 .. DPLO-DK, as a number, are < DT
        bits = [(DT >> (DK - 1 - i)) & 1 for i in range(DK)]  # most significant first: plane DPLO - 1 - i
        last1 = max(i for i in range(DK) if bits[i]); first = True
        for i in range(last1 + 1):
            p = DPLO - 1 - i
            A.not_(X, p)
            if bits[i]:
                if first: A.and_(Y, DPM, X); first = False   # lt := eq and not p
                else: A.and_(X, DPM, X); A.or_(Y, Y, X)      # lt := lt or (eq and not p)
                if i < last1: A.and_(DPM, DPM, p)            # eq := eq and p
            else: A.and_(DPM, DPM, X)                        # eq := eq and not p
        A.mov(DPM, Y)                                        # DPM := lt
    A.addi(C1, C, 1)                                         # steps completed including this one
    A.label('dpl')
    A.jeqi(DPM, 0, 'cont')
    A.label('dp1')                                           # ---- one DP walk: l := lowest set bit of DPM ----
    A.movi(L, 0); A.mov(X, DPM)
    for i, sh in enumerate((128, 64, 32, 16, 8, 4, 2, 1)):
        A.andi(Y, X, (1 << sh) - 1); A.jnei(Y, 0, 'ct%d' % i); A.shri(X, X, sh); A.addi(L, L, sh); A.label('ct%d' % i)
    A.subi(Y, DPM, 1); A.and_(DPM, DPM, Y)                   # clear that bit
    A.label('gather')                                        # ACC := the 256-bit point of walk l (bit j = plane j, bit l)
    A.shr(ACC, 0, L); A.andi(ACC, ACC, 1)
    for j in range(1, 256):
        A.shr(TT, j, L); A.andi(TT, TT, 1); A.shli(TT, TT, j); A.or_(ACC, ACC, TT)
    A.label('record')                                        # REC := 1 | (end bits 0..KEYB-1) << 1 | trail number << (KEYB+1)
    A.andi(REC, ACC, (1 << KEYB) - 1); A.shli(REC, REC, 1); A.addi(REC, REC, 1)
    A.ld(ID, L, LID); A.shli(ID, ID, KEYB + 1); A.or_(REC, REC, ID)
    A.andi(SLOT, ACC, (1 << SB) - 1); A.jlti(SLOT, S, 'sl_ok'); A.subi(SLOT, SLOT, S); A.label('sl_ok')
    A.label('probe')                                         # one table word: its four records in order
    A.ld(TR, SLOT, 0)
    for k in range(RPW):
        if k: A.shri(Y, TR, RB * k); A.andi(X, Y, RM)
        else: A.andi(X, TR, RM)
        A.jeqi(X, 0, 'empty%d' % k)
        A.xor(X, X, REC); A.andi(X, X, (1 << (KEYB + 1)) - 1); A.jeqi(X, 0, 'match%d' % k)
    A.label('pnext')
    A.addi(SLOT, SLOT, 1); A.jnei(SLOT, S, 'probe')
    A.movi(SLOT, 0); A.jmp('probe')
    for k in range(RPW):                                     # insertion into the first empty record of the word
        A.label('empty%d' % k)
        if k: A.shli(X, REC, RB * k); A.or_(TR, TR, X)
        else: A.or_(TR, TR, REC)
        A.st(SLOT, 0, TR); A.jmp('ins')
    A.label('ins')
    A.mov(LV, C1); A.jal(LR, 'restart'); A.jmp('dpl')
    for k in range(RPW):                                     # a record with the same KEYB end bits: X := its trail number
        A.label('match%d' % k)
        A.shri(X, TR, RB * k + KEYB + 1); A.andi(X, X, (1 << IDB) - 1); A.jmp('match')
    # ---------------- end of iteration ----------------
    A.label('cont')
    A.addi(C, C, 1); A.jnei(C, Tb, 'loop')                   # counter (3 with the compare and branch)
    A.label('dl')
    A.halt(12)                                               # c = Tb: the attempt failed
    # ---------------- restart(l) and the insertion of a point into lane l ----------------
    A.label('restart')                                       # in: L, LV; link LR
    A.jnei(IDN, U, 'rs1'); A.halt(11); A.label('rs1')
    A.st(L, LID, IDN); A.st(L, LST, LV); A.add(NP, RHO, IDN); A.addi(IDN, IDN, 1)
    A.label('setwalk')                                       # in: L, NP; link LR
    A.movi(ONEB, 1); A.shl(ONEB, ONEB, L); A.not_(NM, ONEB)
    A.label('sw_planes')
    for j in range(256):
        A.and_(X, j, NM)
        if j: A.shri(Y, NP, j); A.andi(Y, Y, 1)
        else: A.andi(Y, NP, 1)
        A.shl(Y, Y, L); A.or_(j, X, Y)
    A.label('sw_end')
    A.jr(LR)
    # ---------------- the evaluation of F on one point with the permutation ----------------
    A.label('evalF')                                         # in: UU; out: FF; link LR2
    build_state(A, MISC)
    A.label('ef_perm')
    A.permute(W0); A.lda(PDR, MISC + 7); A.xor(FF, W0, PDR)
    if WT: A.andi(FF, FF, (1 << WT) - 1)                     # test builds only: F truncated to the low WT bits
    A.jr(LR2)
    A.label('outm')                                          # in: UU; out: W0..W3 = the 128-byte message m(UU); link LR2
    build_state(A, MISC)
    A.jr(LR2)
    # ---------------- replay ----------------
    A.label('match')                                         # in: X (stored trail a), L (walk of trail b), C1
    A.ld(Y, L, LID); A.ld(LB, L, LST); A.sub(LB, C1, LB)     # trail b: its number and its length lb = c1 - LST[l]
    A.jgei(LB, LRC + 1, 'rfail')                             # lb > LRC: the replay refuses it
    A.add(P, RHO, X); A.add(Q, RHO, Y)
    A.mov(UU, P); A.movi(LA, 0)
    A.label('meas')                                          # la := evaluations of trail a from its start to its first DP
    A.jal(LR2, 'evalF'); A.addi(LA, LA, 1); A.jlti(FF, THR, 'measd')       # the image is a DP when FF < THR
    A.jgei(LA, LRC, 'rfail'); A.mov(UU, FF); A.jmp('meas')
    A.label('measd')
    A.jlt(LA, LB, 'advq')
    A.sub(N, LA, LB); A.mov(MM, LB)
    A.label('advp')
    A.jeqi(N, 0, 'lock'); A.mov(UU, P); A.jal(LR2, 'evalF'); A.mov(P, FF); A.subi(N, N, 1); A.jmp('advp')
    A.label('advq')
    A.sub(N, LB, LA); A.mov(MM, LA)
    A.label('advq2')
    A.jeqi(N, 0, 'lock'); A.mov(UU, Q); A.jal(LR2, 'evalF'); A.mov(Q, FF); A.subi(N, N, 1); A.jmp('advq2')
    A.label('lock')
    A.jeq(P, Q, 'rfail')
    A.label('lloop')
    A.jeqi(MM, 0, 'rfail')
    A.mov(UU, P); A.jal(LR2, 'evalF'); A.mov(FP, FF); A.mov(UU, Q); A.jal(LR2, 'evalF')
    A.jeq(FP, FF, 'found')
    A.mov(P, FP); A.mov(Q, FF); A.subi(MM, MM, 1); A.jmp('lloop')
    A.label('found')                                         # output m(p), m(q): words W0..W3 of the built states
    A.mov(UU, P); A.jal(LR2, 'outm')
    for i in range(4): A.st(ZERO, OUT + i, W0 + i)
    A.mov(UU, Q); A.jal(LR2, 'outm')
    for i in range(4): A.st(ZERO, OUT + 4 + i, W0 + i)
    A.halt(1)
    A.label('rfail')
    A.halt(13)
    A.label('end')
    A.resolve()
    return A


def audit(A):
    """every conditional branch follows the compare that sets its register; every label inside range"""
    for i, x in enumerate(A.ins):
        if x[0] in (BNZ, BZ):
            p = A.ins[i - 1]
            assert p[0] in CMPOPS and p[1] == x[2], ('branch without compare', i)
            assert x[4] < len(A.ins)
        if x[0] in (JMP, JAL): assert x[4] < len(A.ins)


# ---------------- encoding ----------------
def enc(x):
    op, d, a, b, imm = x
    return struct.pack('<BHHHB', op, d, a, b, 0) + imm.to_bytes(24, 'little')


def dec(bs):
    out = []
    for i in range(0, len(bs), 32):
        op, d, a, b, z = struct.unpack('<BHHHB', bs[i:i + 8])
        out.append((op, d, a, b, int.from_bytes(bs[i + 8:i + 32], 'little')))
    return out


def sl_bytes(prog, PFLO, PFN):
    """prog.bin + the prefilter: PF := OR of planes PFLO..PFLO+PFN-1 (PFN-1 ORs), 5-byte instructions"""
    out = bytearray(prog)
    def w(code, d, a, b): return (code | d << 3 | a << 15 | b << 27).to_bytes(5, 'little')
    out += w(2, PF, PFLO, PFLO + 1)
    for j in range(PFLO + 2, PFLO + PFN): out += w(2, PF, PF, j)
    return bytes(out)


# ---------------- Keccak ----------------
RC = [0x0000000000000001, 0x0000000000008082, 0x800000000000808a, 0x8000000080008000, 0x000000000000808b, 0x0000000080000001,
      0x8000000080008081, 0x8000000000008009, 0x000000000000008a, 0x0000000000000088, 0x0000000080008009, 0x000000008000000a,
      0x000000008000808b, 0x800000000000008b, 0x8000000000008089, 0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
      0x000000000000800a, 0x800000008000000a, 0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008]
ROTC = [0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39, 41, 45, 15, 21, 8, 18, 2, 61, 56, 14]


def rotl(v, r): return ((v << r) | (v >> (64 - r))) & M64 if r else v


def keccak_f(A, rounds):
    A = list(A)
    for r in range(rounds):
        Cc = [A[x] ^ A[x + 5] ^ A[x + 10] ^ A[x + 15] ^ A[x + 20] for x in range(5)]
        D = [Cc[(x + 4) % 5] ^ rotl(Cc[(x + 1) % 5], 1) for x in range(5)]
        A = [A[i] ^ D[i % 5] for i in range(25)]
        B = [0] * 25
        for x in range(5):
            for y in range(5): B[y + 5 * ((2 * x + 3 * y) % 5)] = rotl(A[x + 5 * y], ROTC[x + 5 * y])
        A = [B[x + 5 * y] ^ ((~B[(x + 1) % 5 + 5 * y] & M64) & B[(x + 2) % 5 + 5 * y]) for y in range(5) for x in range(5)]
        A[0] ^= RC[r]
    return A


def sha3_256_r(msg, rounds):
    A = [0] * 25
    off = 0
    while True:
        rem = len(msg) - off
        if rem >= 136: blk = msg[off:off + 136]; off += 136
        else:
            blk = bytearray(msg[off:] + bytes(136 - rem)); blk[rem] ^= 6; blk[135] ^= 0x80; off = len(msg) + 1
        for i in range(17): A[i] ^= int.from_bytes(blk[8 * i:8 * i + 8], 'little')
        A = keccak_f(A, rounds)
        if off > len(msg): break
    return b''.join(A[i].to_bytes(8, 'little') for i in range(4))


# ---------------- constants of the target from meta.txt ----------------
def read_meta(path):
    KL = [0] * 25; PD = [0] * 4
    for line in open(path):
        t = line.split()
        if t and t[0] == 'lane': KL[int(t[1])] = int(t[2], 16)
        elif t and t[0] == 'pd': PD = [int(x, 16) for x in t[1:5]]
    return KL, PD


def data_image(KL, PD):
    """16 words: KW[0..6] (lane constants of the absorbed state, the lanes of u XORed on top), PD, then 8 output words"""
    KW = []
    for w in range(7):
        v = 0
        for i in range(4):
            l = 4 * w + i
            if l < 25: v |= KL[l] << (64 * i)
        KW.append(v)
    pd = PD[0] | PD[1] << 64 | PD[2] << 128 | PD[3] << 192
    return KW + [pd] + [0] * 8


def m_of(u, KL):
    Ls = list(KL[:16])
    u0, u1, u2, u3 = [(u >> (64 * i)) & M64 for i in range(4)]
    Ls[1] = u0 ^ KL[1]; Ls[11] = u1 ^ KL[11]; Ls[6] = u0 ^ u1 ^ KL[6]
    Ls[9] = u2 ^ KL[9]; Ls[14] = u3 ^ KL[14]; Ls[4] = u2 ^ u3 ^ KL[4]
    return b''.join(x.to_bytes(8, 'little') for x in Ls)


def F_plain(u, KL, PD, rounds=NR):
    d = sha3_256_r(m_of(u, KL), rounds)
    pd = PD[0] | PD[1] << 64 | PD[2] << 128 | PD[3] << 192
    return int.from_bytes(d, 'little') ^ pd


# ---------------- the machine ----------------
def compile_sl(slb, nprog, hookW=None):
    """Python function executing the 5-byte block on a register list (the planes 0..255 and PF are the only live ends).
    hookW (test builds only): set the planes hookW..255 to zero after the first nprog instructions (the F of the program
    truncated to hookW bits, as in the organizer experiment rho-w22)."""
    src = ['def sl(R):']
    for j in range(256): src.append(' r%d=R[%d]' % (j, j))
    for i in range(0, len(slb), 5):
        if i // 5 == nprog and hookW:
            for j in range(hookW, 256): src.append(' r%d=0' % j)
        w = int.from_bytes(slb[i:i + 5], 'little')
        op, d, a, b = w & 7, (w >> 3) & 4095, (w >> 15) & 4095, (w >> 27) & 4095
        if op == 0: src.append(' r%d=r%d^r%d' % (d, a, b))
        elif op == 1: src.append(' r%d=r%d&r%d' % (d, a, b))
        elif op == 2: src.append(' r%d=r%d|r%d' % (d, a, b))
        else: src.append(' r%d=r%d^%d' % (d, a, M256))
    for j in range(256): src.append(' R[%d]=r%d' % (j, j))
    src.append(' R[%d]=r%d' % (PF, PF))
    ns = {}
    exec(compile('\n'.join(src), 'sl', 'exec'), ns)
    return ns['sl']


class VM:
    def load(s, code, sl, nsl, slpos, memwords, data, MISC, rng):
        s.code = code; s.sl = sl; s.nsl = nsl; s.slpos = slpos
        s.R = [0] * NREGS; s.M = [0] * memwords
        for i, v in enumerate(data): s.M[MISC + i] = v
        s.rng = rng; s.units = 0; s.slsteps = 0; s.halt = None
        s.cnt = [0] * (len(code) + 1)
        return s

    def run(s, pc=0, stop=None):
        code, R, M, cnt = s.code, s.R, s.M, s.cnt
        sl, slpos = s.sl, s.slpos
        while True:
            if pc == slpos and sl is not None:
                sl(R); s.slsteps += 1
            if stop is not None and pc == stop: return pc
            op, d, a, b, imm = code[pc]
            cnt[pc] += 1
            pc += 1
            if op == XOR: R[d] = R[a] ^ R[b]
            elif op == AND: R[d] = R[a] & R[b]
            elif op == OR: R[d] = R[a] | R[b]
            elif op == NOT: R[d] = R[a] ^ M256
            elif op == ADD: R[d] = (R[a] + R[b]) & M256
            elif op == SUB: R[d] = (R[a] - R[b]) & M256
            elif op == SHL: R[d] = (R[a] << (R[b] & 255)) & M256
            elif op == SHR: R[d] = R[a] >> (R[b] & 255)
            elif op == EQ: R[d] = 1 if R[a] == R[b] else 0
            elif op == LT: R[d] = 1 if R[a] < R[b] else 0
            elif op == MOV: R[d] = R[a]
            elif op == ADDI: R[d] = (R[a] + imm) & M256
            elif op == SUBI: R[d] = (R[a] - imm) & M256
            elif op == SHLI: R[d] = (R[a] << imm) & M256
            elif op == SHRI: R[d] = R[a] >> imm
            elif op == ANDI: R[d] = R[a] & imm
            elif op == EQI: R[d] = 1 if R[a] == imm else 0
            elif op == LTI: R[d] = 1 if R[a] < imm else 0
            elif op == MOVI: R[d] = imm
            elif op == LD: R[d] = M[R[a] + imm]
            elif op == ST: M[R[a] + imm] = R[b]
            elif op == LDA: R[d] = M[imm]
            elif op == BNZ:
                if R[a]: pc = imm
            elif op == BZ:
                if not R[a]: pc = imm
            elif op == JMP: pc = imm
            elif op == JAL: R[d] = pc; pc = imm
            elif op == JR: pc = R[a]
            elif op == RND: R[d] = s.rng.getrandbits(256)
            elif op == PERM:
                lanes = []
                for w in range(7):
                    v = R[a + w]
                    for i in range(4): lanes.append((v >> (64 * i)) & M64)
                lanes = keccak_f(lanes[:25], NR)
                lanes += [0, 0, 0]
                for w in range(7): R[a + w] = sum(lanes[4 * w + i] << (64 * i) for i in range(4))
                s.units += 1
            elif op == HALT:
                s.halt = imm; return None
            else: raise Exception('bad op')


# ---------------- counting ----------------
FULL = {k: PARAMS[k] for k in ('S', 'U', 'SB', 'IDB', 'LRC', 'Tb', 'HMAX', 'DPLO', 'DK', 'DT', 'PFLO', 'PFN')}


def counts(A, Pm):
    """Worst-case operation counts of every routine, from the lengths of the emitted code (an instruction is one
    operation, PERM is UNIT).  seg(a, b) = number of instructions between two labels."""
    I = A.lab
    def seg(a, b): return I[b] - I[a]
    S, U, LRC = Pm['S'], Pm['U'], Pm['LRC']
    c = {}
    c['n_instr'] = len(A.ins)
    c['setwalk'] = seg('setwalk', 'sw_end') + 1                                  # with the return
    c['restart'] = (seg('restart', 'rs1') - 1) + seg('rs1', 'setwalk') + c['setwalk']   # the cap check passes (no HALT)
    c['restart_halt'] = seg('restart', 'rs1') - 1 + 1                           # the last call: compare, branch not taken, HALT
    c['hit'] = (seg('hit', 'h1') - 1) + seg('h1', 'dpl') + 2                     # per processed hit, no DP walk
    c['ctz_clear'] = seg('dp1', 'gather')
    c['gather'] = seg('gather', 'record')
    c['record_slot'] = seg('record', 'sl_ok')
    c['probe_word'] = 1 + 7 + 8 * (RPW - 1) + 3                                  # load, four occupied non-matching records, next word
    c['probe_wrap'] = 2
    c['probe_end'] = 1 + 7 + 8 * (RPW - 2) + 4                                   # load, three records passed, the fourth: shift, mask, empty test
    c['empty_tail'] = 2 + 1 + 1 + 3                                              # shift, or, store, jump; move, call, jump back
    c['dp_fixed'] = 2 + c['ctz_clear'] + c['gather'] + c['record_slot'] + c['probe_end'] + c['probe_wrap'] + c['empty_tail']
    c['dp_max'] = c['dp_fixed'] + c['probe_word'] * S                            # at most S occupied words passed
    c['dl_final'] = seg('dl', 'restart')                                         # c = Tb: the HALT (the compare and branch are in the iteration's 3)
    c['e_eval'] = seg('evalF', 'outm') - 1 + UNIT                                # one evaluation of F with the permutation, with the return
    c['e_outm'] = seg('outm', 'match')                                           # the message builder, with the return
    e = c['e_eval']
    c['match_entry'] = 3 + seg('match', 'meas')                                  # trail number from the record (3), entry (9: with the lb test 2)
    c['meas_iter'] = e + 8                                                       # one measuring evaluation without the DP
    c['meas_last'] = e + 4                                                       # the evaluation that lands on the DP
    c['replay_iter'] = 13 + 2 * e                                                # one lock-step iteration (not found)
    # success after k lock-step iterations, la measured: 12 + (la - 1)(e + 8) + (e + 4) + 2 + 2 + n (7 + e) + 2 + 2
    #   + (k - 1)(13 + 2e) + (9 + 2e) + 67; exhaustion: ... + m (13 + 2e) + 3.  Largest at la = lb = k = LRC:
    #   (e + 8 + 13 + 2e) LRC + 12 - 4 + 2 + 2 + 2 + 2 - 13 + 9 + 67
    c['replay_const'] = c['match_entry'] - 4 + 2 + 2 + 2 + 2 - 13 + 9 + 67
    c['replay_max'] = (c['meas_iter'] + c['replay_iter']) * LRC + c['replay_const']
    c['setup'] = seg('start', 'clr') + (S // 8) * 11 + 1 + 256 * (7 + c['setwalk'])
    return c


def pf_bytes(PFLO, PFN):
    return sl_bytes(b'', PFLO, PFN)


def build_cli(argv):
    if len(argv) > 1 and argv[1] == 'build':
        meta = argv[2] if len(argv) > 2 else 'meta.txt'
        KL, PD = read_meta(meta)
        A = program(FULL); audit(A)
        other = b''.join(enc(x) for x in A.ins)
        open('other.bin', 'wb').write(other)
        open('pf.bin', 'wb').write(pf_bytes(FULL['PFLO'], FULL['PFN']))
        open('data.bin', 'wb').write(b''.join(w.to_bytes(32, 'little') for w in data_image(KL, PD)))
        c = counts(A, FULL)
        I = A.lab
        out = []
        out.append('other code: %d instructions x 32 bytes = %d bytes (other.bin sha256 %s)' % (len(A.ins), len(other), hashlib.sha256(other).hexdigest()))
        out.append('prefilter: %d instructions x 5 bytes (pf.bin sha256 %s); the straight-line block = prog.bin then pf.bin, %d instructions, sits in front of instruction %d (label loop)' %
                   (FULL['PFN'] - 1, hashlib.sha256(open('pf.bin', 'rb').read()).hexdigest(), os.path.getsize('prog.bin') // 5 + FULL['PFN'] - 1, I['loop']))
        out.append('data image: 16 words x 32 bytes = 512 bytes (data.bin sha256 %s): KW[0..6], PD, 8 output words' % hashlib.sha256(open('data.bin', 'rb').read()).hexdigest())
        out.append('memory map (words): TAB 0..%d, LID %d..%d, LST %d..%d, data %d..%d' % (FULL['S'] - 1, FULL['S'], FULL['S'] + 255, FULL['S'] + 256, FULL['S'] + 511, FULL['S'] + 512, FULL['S'] + 527))
        out.append('routine entry points (instruction index): ' + ', '.join('%s %d' % (k, I[k]) for k in ('start', 'loop', 'hit', 'dpl', 'dp1', 'gather', 'record', 'probe', 'empty0', 'ins', 'match0', 'cont', 'dl', 'restart', 'setwalk', 'evalF', 'outm', 'match', 'meas', 'end')))
        for k, v in c.items(): out.append('%-18s %d' % (k, v))
        bybase = {}
        for x in A.ins: bybase[NAMES[x[0]]] = bybase.get(NAMES[x[0]], 0) + 1
        out.append('static opcode mix: ' + ' '.join('%s %d' % kv for kv in sorted(bybase.items(), key=lambda kv: -kv[1])))
        out.append('highest register named: %d (file of %d)' % (max(max(x[1], x[2], x[3]) for x in A.ins), NREGS))
        open('counts.txt', 'w').write(chr(10).join(out) + chr(10))
        print(chr(10).join(out))
    else:
        print(__doc__ if __doc__ else 'usage: other4.py build [meta.txt]')


if __name__ == '__main__':
    build_cli(sys.argv)
```

### D.2 Output of `python3 other4.py build meta.txt`

```
other code: 2704 instructions x 32 bytes = 86528 bytes (other.bin sha256 b2ec53360bebcdf97a54ad8e57e57adf21ab13806e60839935e2bb85268e5b9d)
prefilter: 15 instructions x 5 bytes (pf.bin sha256 7d01825e1754a115fd593386cbd91d120baff96ff46f5ea6472a7326662ddfbc); the straight-line block = prog.bin then pf.bin, 26382 instructions, sits in front of instruction 26 (label loop)
data image: 16 words x 32 bytes = 512 bytes (data.bin sha256 94c4ba41fdc2624a956f241f6116e54974fc0053fd09c9ec2b08a465cf47e073): KW[0..6], PD, 8 output words
memory map (words): TAB 0..23087, LID 23088..23343, LST 23344..23599, data 23600..23615
routine entry points (instruction index): start 0, loop 26, hit 28, dpl 142, dp1 144, gather 188, record 1210, probe 1220, empty0 1257, ins 1272, match0 1275, cont 1287, dl 1290, restart 1291, setwalk 1298, evalF 2581, outm 2611, match 2638, meas 2647, end 2704
n_instr            2704
setwalk            1283
restart            1289
restart_halt       3
hit                115
ctz_clear          44
gather             1022
record_slot        10
probe_word         35
probe_wrap         2
probe_end          28
empty_tail         7
dp_fixed           1115
dp_max             809195
dl_final           1
e_eval             1655
e_outm             27
match_entry        12
meas_iter          1663
meas_last          1659
replay_iter        3323
replay_const       79
replay_max         197695943566004025246887151209835135055
setup              361994
static opcode mix: OR 613 ANDI 540 SHRI 276 SHLI 270 AND 263 SHL 257 SHR 256 ST 24 EQI 23 BNZ 21 XOR 21 MOV 18 ADDI 17 LDA 15 JMP 14 BZ 13 MOVI 10 JAL 9 NOT 7 LTI 7 HALT 5 SUBI 5 ADD 4 LD 4 EQ 3 JR 3 SUB 3 RND 1 PERM 1 LT 1
highest register named: 2190 (file of 2192)
```

### D.3 other4_test.py

```python
#!/usr/bin/env python3
# other4_test.py - checks of the emitted program of other4.py.
#   1. routine tests: each routine run on constructed states; its executed operations must equal the counted worst case
#   2. end-to-end runs of the whole emitted program (setup, loop, hit handler, DP handler, restart, deadlines, replay,
#      output) at reduced width: the straight line of prog.bin is truncated to W bits after every step (test hook), the
#      replay's F is truncated alike (one extra ANDI in evalF, test builds only); the output pair is checked with an
#      independent Keccak.  The totals of every run are compared with the counted bounds.
#   usage: other4_test.py [nseeds] [pyseed]   (params.json, meta.txt and prog.bin of the row in the working directory)
import random, sys, time
from other4 import *

KL, PD = read_meta('meta.txt')
prog = open('prog.bin', 'rb').read(); NPROG = len(prog) // 5
data = data_image(KL, PD)
FAILS = []; NCHK = [0]


def check(cond, msg):
    NCHK[0] += 1
    if not cond:
        FAILS.append(msg); print('FAIL', msg)


def mk(Pm, seed=1, with_sl=False):
    A = program(Pm); audit(A)
    code = dec(b''.join(enc(x) for x in A.ins))
    S = Pm['S']
    slb = sl_bytes(prog, Pm['PFLO'], Pm['PFN'])
    sl = compile_sl(slb, NPROG, Pm.get('WTEST')) if with_sl else None
    vm = VM().load(code, sl, len(slb) // 5, A.lab['loop'], S + 528, data, S + 512, random.Random(seed))
    return A, vm, len(slb) // 5


def nonsl_ops(vm):
    return sum(vm.cnt) - vm.units + vm.units * UNIT


def ops_of(vm, f):
    a = nonsl_ops(vm); f(); return nonsl_ops(vm) - a


# ------------------------------------------------------------------ 1. routine tests
def sl_test():
    """the straight line + prefilter as compiled from the 5-byte bytes: 2 x 256 points, every lane, 3 chained steps, against F_plain"""
    sl = compile_sl(sl_bytes(prog, 240, 16), NPROG)
    for rep_ in range(2):
        us = [random.getrandbits(256) for _ in range(256)]
        R = [0] * NREGS
        for step in range(3):
            for j in range(256): R[j] = sum(((us[l] >> j) & 1) << l for l in range(256))
            sl(R)
            for l in range(256):
                o = sum(((R[j] >> l) & 1) << j for j in range(256))
                us[l] = F_plain(us[l], KL, PD)
                if o != us[l]: check(False, 'straight line lane %d' % l); break
            else: continue
            break
        pfw = R[PF]
        check(all(((pfw >> l) & 1) == (0 if sum(((R[j] >> l) & 1) << (j - 240) for j in range(240, 256)) == 0 else 1) for l in range(256)), 'prefilter word')
    check(True, 'straight line')


def routine_tests():
    sl_test()
    Pm = dict(FULL)
    A, vm, nsl = mk(Pm)
    c = counts(A, Pm); I = A.lab; R = vm.R; END = I['end']
    S = Pm['S']; LID, LST = S, S + 256; KB = keyb(Pm); DPL, DKK = Pm['DPLO'], Pm['DK']
    # setwalk
    R[IDN] = 300; R[RHO] = 12345; R[LR] = END
    planes = [random.getrandbits(256) for _ in range(256)]
    for j in range(256): R[j] = planes[j]
    l = 201; np_ = random.getrandbits(256); R[L] = l; R[NP] = np_
    n = ops_of(vm, lambda: vm.run(I['setwalk'], stop=END))
    check(n == c['setwalk'], 'setwalk ops %d vs %d' % (n, c['setwalk']))
    ok = all(((R[j] >> l) & 1) == ((np_ >> j) & 1) and (R[j] & ~(1 << l)) == (planes[j] & ~(1 << l)) for j in range(256))
    check(ok, 'setwalk effect')
    # restart
    R[LR] = END; R[L] = 7; R[LV] = 99; R[IDN] = 4321
    n = ops_of(vm, lambda: vm.run(I['restart'], stop=END))
    check(n == c['restart'], 'restart ops %d vs %d' % (n, c['restart']))
    check(vm.M[LID + 7] == 4321 and vm.M[LST + 7] == 99 and R[IDN] == 4322, 'restart effect')
    R[IDN] = Pm['U']; R[LR] = END
    n = ops_of(vm, lambda: vm.run(I['restart'], stop=END))
    check(vm.halt == 11 and n == c['restart_halt'], 'restart halt %d %s' % (n, vm.halt))
    vm.halt = None
    # evalF and outm
    u = random.getrandbits(256); R[UU] = u; R[LR2] = END
    n = ops_of(vm, lambda: vm.run(I['evalF'], stop=END))
    check(n == c['e_eval'] and R[FF] == F_plain(u, KL, PD), 'evalF ops %d vs %d' % (n, c['e_eval']))
    R[UU] = u; R[LR2] = END
    n = ops_of(vm, lambda: vm.run(I['outm'], stop=END))
    check(n == c['e_outm'], 'outm ops %d' % n)
    check(b''.join(R[W0 + i].to_bytes(32, 'little') for i in range(4)) == m_of(u, KL), 'outm message')
    # setup
    vm2 = mk(Pm)[1]; vm2.M[0] = 5
    n = ops_of(vm2, lambda: vm2.run(0, stop=I['loop']))
    check(n == c['setup'], 'setup ops %d vs %d' % (n, c['setup']))
    check(all(vm2.M[i] == 0 for i in range(S)) and all(vm2.M[LID + i] == i and vm2.M[LST + i] == 0 for i in range(256)), 'setup effect')
    check(vm2.R[IDN] == 256 and vm2.R[C] == 0 and vm2.R[H] == 0 and vm2.R[ONES] == M256, 'setup state')
    rho = vm2.R[RHO]
    check(all(sum(((vm2.R[j] >> l) & 1) << j for j in range(256)) == (rho + l) & M256 for l in range(0, 256, 17)), 'setup lanes')
    # hit, no DP: planes DPLO..PFLO-1 nonzero
    A, vm, nsl = mk(Pm); R = vm.R
    for j in range(256): R[j] = M256
    R[PF] = 5; R[H] = 0; R[C] = 3
    n = ops_of(vm, lambda: vm.run(I['hit'], stop=I['cont']))
    check(n == c['hit'], 'hit ops %d vs %d' % (n, c['hit']))
    # hit abort
    R[H] = Pm['HMAX']; n = ops_of(vm, lambda: vm.run(I['hit'], stop=I['cont']))
    check(vm.halt == 10 and n == 4, 'hit abort %s %d' % (vm.halt, n)); vm.halt = None
    # DP handler worst path: walk 255 alone at a DP; k full words (four non-matching records each) in the probe path, then a
    # word with three non-matching records (the insertion goes to its fourth record), with and without wrap
    KM = (1 << KB) - 1
    for k, wrap in ((0, False), (5, False), (7, True)):
        A, vm, nsl = mk(Pm); R = vm.R; M = vm.M
        for j in range(256): R[j] = M256
        for j in range(DPL - DKK, 256): R[j] = M256 ^ (1 << 255)
        R[PF] = M256 ^ (1 << 255); R[ONES] = M256; R[H] = 0; R[C] = 777; R[RHO] = 31337; R[IDN] = 5000; R[LR] = END
        M[LST + 255] = 700; M[LID + 255] = 255
        SBm = Pm['SB']
        val = (S - 3) if wrap else (S + 100)                 # low SB bits of the point: slot S - 3, or S + 100 -> 100 after the subtraction
        for j in range(SBm): R[j] = (R[j] & ~(1 << 255)) | (((val >> j) & 1) << 255)
        for j in range(SBm, 40): R[j] = (R[j] & ~(1 << 255)) | (random.getrandbits(1) << 255)
        pt = sum(((R[j] >> 255) & 1) << j for j in range(256))
        slot = (S - 3) if wrap else 100
        def other_rec(i):
            while True:
                key = random.getrandbits(KB)
                if key != pt & KM: return 1 | key << 1 | (300 + i) << (KB + 1)
        for i in range(k): M[(slot + i) % S] = sum(other_rec(RPW * i + q) << (q * RB) for q in range(RPW))
        w0 = other_rec(90) | other_rec(91) << RB | other_rec(92) << (2 * RB)
        M[(slot + k) % S] = w0
        n = ops_of(vm, lambda: vm.run(I['hit'], stop=I['cont']))
        exp = c['hit'] + c['dp_fixed'] + c['restart'] + c['probe_word'] * k - (0 if wrap else c['probe_wrap']) - (1 if wrap else 0)
        check(n == exp, 'DP worst (k=%d wrap=%s) ops %d vs %d (halt %s)' % (k, wrap, n, exp, vm.halt))
        word = M[(slot + k) % S]
        rec = (word >> ((RPW - 1) * RB)) & RM
        check(word & ((1 << ((RPW - 1) * RB)) - 1) == w0 and rec == 1 | (pt & KM) << 1 | 255 << (KB + 1), 'DP record')
        check(M[LID + 255] == 5000 and M[LST + 255] == 778 and R[IDN] == 5001, 'DP restart')
    # insertion into each record of a word; a match in each of the four positions
    for pos in range(RPW):
        A, vm, nsl = mk(Pm); R = vm.R; M = vm.M
        for j in range(256): R[j] = M256
        for j in range(DPL - DKK, 256): R[j] = M256 ^ (1 << 255)
        R[PF] = M256 ^ (1 << 255); R[ONES] = M256; R[H] = 0; R[C] = 777; R[RHO] = 31337; R[IDN] = 5000; R[LR] = END
        M[LST + 255] = 700; M[LID + 255] = 255
        for j in range(Pm['SB']): R[j] = (R[j] & ~(1 << 255)) | (((S + 100) >> j) & 1) << 255
        pt = sum(((R[j] >> 255) & 1) << j for j in range(256))
        recs = [other_rec(50 + q) for q in range(pos)]
        M[100] = sum(r << (RB * q) for q, r in enumerate(recs))
        vm.run(I['hit'], stop=I['cont'])
        check((M[100] >> (RB * pos)) & RM == 1 | (pt & KM) << 1 | 255 << (KB + 1) and M[LID + 255] == 5000, 'insert at %d' % pos)
        A, vm, nsl = mk(Pm); R = vm.R; M = vm.M
        for j in range(256): R[j] = M256
        for j in range(DPL - DKK, 256): R[j] = M256 ^ (1 << 255)
        R[PF] = M256 ^ (1 << 255); R[ONES] = M256; R[H] = 0; R[C] = 777; R[RHO] = 31337; R[IDN] = 5000; R[LR] = END
        M[LST + 255] = 700; M[LID + 255] = 255
        for j in range(Pm['SB']): R[j] = (R[j] & ~(1 << 255)) | (((S + 100) >> j) & 1) << 255
        pt = sum(((R[j] >> 255) & 1) << j for j in range(256))
        recs = [other_rec(60 + q) for q in range(pos)] + [1 | (pt & KM) << 1 | 4242 << (KB + 1)]
        M[100] = sum(r << (RB * q) for q, r in enumerate(recs))
        vm.run(I['hit'], stop=I['meas'])
        check(R[X] == 4242 and R[Y] == 255 and R[LB] == 778 - 700, 'match at %d' % pos)
    # the DP mask of the hit handler: walks with the top planes zero and the DK planes below them < DT
    DT = Pm['DT']; THRm = thr(Pm); tested = [0, 0]
    for trial in range(4):
        A, vm, nsl = mk(Pm); R = vm.R
        xs = []
        for l in range(256):
            kind = random.randrange(6)
            if kind == 0: x = random.randrange(THRm)                                          # a DP
            elif kind == 1: x = random.randrange(THRm, 1 << DPL)                              # a candidate that is not a DP (x >= THR)
            elif kind == 2: x = THRm - 1 - random.randrange(3)                                # at the threshold, below
            elif kind == 3: x = THRm + random.randrange(3)                                    # at the threshold
            elif kind == 4: x = random.getrandbits(256)
            else: x = random.getrandbits(256 - 240) << 240 | random.getrandbits(240)          # 16 top planes random
            xs.append(max(x, 0) & M256)
        for j in range(256): R[j] = sum(((xs[l] >> j) & 1) << l for l in range(256))
        R[PF] = sum((1 if (xs[l] >> 240) else 0) << l for l in range(256))
        R[ONES] = M256; R[H] = 0; R[C] = 3
        vm.run(I['hit'], stop=I['dpl'])
        want = sum((1 << l) for l in range(256) if xs[l] < THRm)
        check(R[DPM] == want, 'DP mask (trial %d)' % trial)
        tested[0] += bin(want).count('1'); tested[1] += sum(1 for x in xs if (x >> DPL) == 0 and x >= THRm)
    check(tested[0] > 100 and tested[1] > 100, 'DP mask coverage %s' % tested)
    # c = Tb: the iteration's counter and compare, then the HALT
    A, vm, nsl = mk(Pm); R = vm.R
    R[C] = Pm['Tb'] - 1
    n = ops_of(vm, lambda: vm.run(I['cont']))
    check(vm.halt == 12 and n == 3 + c['dl_final'], 'Tb halt %s %d' % (vm.halt, n))
    A, vm, nsl = mk(Pm); R = vm.R
    R[C] = 5
    n = ops_of(vm, lambda: vm.run(I['cont'], stop=I['loop']))
    check(vm.halt is None and n == 3 and R[C] == 6, 'counter ops %d' % n)


def replay_tests(ntrials=60):
    """the replay on pairs of trails of the 12-bit truncation of F with a 4-bit DP (planes 8..11 zero): the measuring walk,
    alignment, lock step; pairs with the same end (found / p = q) and with different ends (exhausted: a false key match)"""
    Pm = dict(S=400, U=400, SB=9, IDB=9, LRC=200, Tb=900, HMAX=10 ** 9, DPLO=8, DK=2, DT=3, PFLO=10, PFN=2, WTEST=12)
    THRm = thr(Pm)
    mask = (1 << 12) - 1
    Ft = lambda u: F_plain(u, KL, PD) & mask
    A, vm0, nsl = mk(Pm); I = A.lab; c = counts(A, Pm); e = c['e_eval']; END = I['end']; S = Pm['S']
    seen = {1: 0, 13: 0, 'diff': 0}
    done = 0
    while done < ntrials:
        rho = random.getrandbits(256)
        trails = {}
        for a in range(256, 400):
            u = (rho + a) & M256; pts = [u]
            for i in range(Pm['LRC']):
                u = Ft(u); pts.append(u)
                if u < THRm: break
            if pts[-1] < THRm: trails[a] = pts
        ends = {}
        for a, t in trails.items(): ends.setdefault(t[-1], []).append(a)
        pairs = [(v[0], v[1]) for v in ends.values() if len(v) > 1][:3]
        keys = list(trails)
        pairs.append(tuple(random.sample(keys, 2)))
        for a, b in pairs:
            if done >= ntrials: break
            ta, tb = trails[a], trails[b]
            la, lb = len(ta) - 1, len(tb) - 1
            A, vm, nsl = mk(Pm); R = vm.R; M = vm.M
            R[RHO] = rho; R[LR2] = END; R[L] = 9; M[S + 9] = b; R[C1] = 5000; M[S + 256 + 9] = 5000 - lb; R[X] = a
            ops = ops_of(vm, lambda: vm.run(I['match']))
            n_, m_ = abs(la - lb), min(la, lb)
            p, q = (ta[n_], tb[0]) if la >= lb else (ta[0], tb[n_])
            meas = (la - 1) * (e + 8) + (e + 4)
            base = 9 + meas + 2 + 2 + n_ * (7 + e) + 2
            check(R[LA] == la and R[LB] == lb, 'replay lengths %d %d vs %d %d' % (R[LA], R[LB], la, lb))
            if ta[-1] != tb[-1]:
                k = 0
                while k < m_ and Ft(p) != Ft(q): p, q = Ft(p), Ft(q); k += 1
                if k < m_:                       # different ends cannot merge inside the trails
                    check(False, 'different ends merged')
                check(vm.halt == 13 and ops == base + (2 if p != q else 0) + (m_ * (13 + 2 * e) + 3 if p != q else 1) - (0 if p != q else 0), 'replay different ends ops %d (halt %s)' % (ops, vm.halt))
                seen['diff'] += 1
            elif p == q:
                check(vm.halt == 13 and ops == base + 2 + 1, 'replay p=q ops %d halt %s' % (ops, vm.halt)); seen[13] += 1
            else:
                k = 1
                while Ft(p) != Ft(q): p, q = Ft(p), Ft(q); k += 1
                check(vm.halt == 1, 'replay expected halt 1, got %s (la %d lb %d)' % (vm.halt, la, lb))
                pred = base + 2 + (k - 1) * (13 + 2 * e) + (9 + 2 * e) + 67
                check(ops == pred and vm.cnt[I['lloop']] == k, 'replay found ops %d vs %d (k %d)' % (ops, pred, k))
                out = M[S + 520:S + 528]
                ma = b''.join(out[x].to_bytes(32, 'little') for x in range(4)); mb = b''.join(out[4 + x].to_bytes(32, 'little') for x in range(4))
                check(ma != mb and (int.from_bytes(sha3_256_r(ma, NR), 'little') & mask) == (int.from_bytes(sha3_256_r(mb, NR), 'little') & mask), 'replay pair')
                seen[1] += 1
            check(ops <= c['replay_max'], 'replay bound')
            done += 1
    # a stored trail without a DP within LRC (checks the guard): halt 13
    A, vm, nsl = mk(dict(Pm, LRC=1)); R = vm.R; M = vm.M
    c1 = counts(A, dict(Pm, LRC=1))
    for a in range(256, 400):
        if Ft((5 + a) & M256) >= THRm:
            R[RHO] = 5; R[LR2] = END; R[L] = 9; M[S + 9] = 300; R[C1] = 10; M[S + 256 + 9] = 9; R[X] = a
            vm.run(A.lab['match']); check(vm.halt == 13 and R[LA] == 1, 'measure guard'); break
    # the length guard of the new trail: lb = LRC + 1 is refused at once (6 operations), lb = LRC goes on
    for lbv, want in ((Pm['LRC'] + 1, 13), (Pm['LRC'], None)):
        A, vm, nsl = mk(Pm); R = vm.R; M = vm.M
        R[RHO] = 5; R[LR2] = A.lab['end']; R[L] = 9; M[S + 9] = 300; R[C1] = 10 ** 6; M[S + 256 + 9] = 10 ** 6 - lbv; R[X] = 256
        n = ops_of(vm, lambda: vm.run(A.lab['match'], stop=A.lab['meas'] if want is None else None))
        check((vm.halt == 13 and n == 6) if want else (vm.halt is None and R[LB] == lbv), 'lb guard %d' % lbv)
    print('replay tests: found %d, p=q %d, different ends %d' % (seen[1], seen[13], seen['diff']))


# ------------------------------------------------------------------ 2. end-to-end
def check_pair(vm, Pm, W):
    S = Pm['S']; out = vm.M[S + 520:S + 528]
    ma = b''.join(out[i].to_bytes(32, 'little') for i in range(4)); mb = b''.join(out[4 + i].to_bytes(32, 'little') for i in range(4))
    da, db = sha3_256_r(ma, NR), sha3_256_r(mb, NR)
    mask = (1 << W) - 1
    return ma != mb and len(ma) == 128 and (int.from_bytes(da, 'little') & mask) == (int.from_bytes(db, 'little') & mask)


def e2e(name, Pm, seeds, expect=None, W=26):
    A = None; res = {}
    for sd in seeds:
        A, vm, nsl = mk(Pm, sd, True)
        t0 = time.time(); vm.run(0); dt = time.time() - t0
        c = counts(A, Pm); I = A.lab; cnt = vm.cnt
        steps = vm.slsteps
        hits = cnt[I['hit']]; dps = cnt[I['dp1']]; rest = cnt[I['rs1']]; dl = cnt[I['dl']]      # dl: 1 when Tb is reached
        # exact group checks
        calls = cnt[I['setwalk']]
        check(sum(cnt[I['setwalk']:I['sw_end'] + 1]) == (c['setwalk']) * calls, 'setwalk group %d calls' % calls)
        check(sum(cnt[I['gather']:I['record']]) == c['gather'] * dps, 'gather group')
        check(cnt[I['loop']] == steps and cnt[I['cont']] in (steps, steps - 1), 'loop counts')
        # totals against the counted bounds
        nonsl = nonsl_ops(vm)
        replay_ops = sum(cnt[I['evalF']:I['end']]) - vm.units + vm.units * UNIT
        bound = (c['setup'] + 5 * steps + hits * c['hit'] + dps * c['dp_max'] + (rest + 1) * (c['restart'] + 3)
                 + c['dl_final'] + c['restart_halt'] + c['replay_max'])
        check(nonsl <= bound, '%s seed %d: ops %d > bound %d' % (name, sd, nonsl, bound))
        # exact accounting of what is not data dependent
        base = c['setup'] + 5 * steps
        res[sd] = (vm.halt, steps, hits, dps, rest, dl, replay_ops)
        if vm.halt == 1:
            check(check_pair(vm, Pm, W), '%s seed %d: output pair invalid' % (name, sd))
        if replay_ops:
            # exact replay formula for the observed lengths
            la, lb, k = vm.R[LA], vm.R[LB], cnt[I['lloop']]
            n_, m_ = abs(la - lb), min(la, lb)
            e = c['e_eval']
            if vm.halt == 1:
                # the 3 instructions that take the trail number from the record lie before evalF (counted with the DP walk)
                pred = 9 + (la - 1) * (e + 8) + (e + 4) + 2 + 2 + n_ * (7 + e) + 2 + 2 + (k - 1) * (13 + 2 * e) + (9 + 2 * e) + 67
                check(replay_ops == pred, '%s seed %d: replay ops %d vs %d (la %d lb %d k %d)' % (name, sd, replay_ops, pred, la, lb, k))
            check(replay_ops <= (c['meas_iter'] + c['replay_iter']) * max(la, lb) + c['replay_const'], 'replay bound')
        print('%-10s seed %3d halt %2s steps %5d hits %5d dp %4d restarts %4d tb %4d replay_ops %7d  total %d' %
              (name, sd, vm.halt, steps, hits, dps, rest, dl, replay_ops, nonsl + steps * nsl))
        if expect is not None: check(vm.halt in expect, '%s seed %d: halt %s not in %s' % (name, sd, vm.halt, expect))
    return res


def main():
    ns = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    random.seed(int(sys.argv[2]) if len(sys.argv) > 2 else 7)
    routine_tests()
    replay_tests()
    print('routine tests done, failures so far:', len(FAILS))
    base = dict(S=3000, U=3000, SB=12, IDB=12, LRC=17 << 8, Tb=3000, HMAX=10 ** 9, DPLO=18, DK=2, DT=3, PFLO=22, PFN=4, WTEST=26)
    seeds = list(range(1, ns + 1))
    e2e('base', base, seeds, expect=(1, 13))
    # width 32, DP of 10 bits and a comparator, prefilter of 6 planes; trails of mean length ~1000 steps against a replay cap of 400:
    # a colliding trail longer than the cap is refused (halt 13)
    w32 = dict(S=3000, U=3000, SB=12, IDB=12, LRC=400, Tb=60000, HMAX=10 ** 9, DPLO=22, DK=3, DT=5, PFLO=26, PFN=6, WTEST=32)
    e2e('w32cap', w32, seeds[:3], expect=(1, 11, 12, 13), W=32)
    small = dict(base, S=400, U=400, SB=9, IDB=9, LRC=2000, Tb=4000)       # small table: long probe runs, wraps; U exhaustion possible
    e2e('smalltab', small, seeds, expect=(1, 11, 12, 13))
    abort = dict(base, HMAX=3)                                            # hit counter abort
    e2e('abort', abort, seeds[:3], expect=(10,))
    tb = dict(base, LRC=3, Tb=5)                                          # Tb reached
    e2e('tb5', tb, seeds[:2], expect=(12,))
    uex = dict(base, S=264, U=264, SB=8, IDB=9, Tb=100000)                 # trail limit reached
    e2e('u264', uex, seeds[:3], expect=(11, 1, 13))
    packed = dict(base, S=200, U=800, SB=8, IDB=10, LRC=2000, Tb=8000)     # U = 4 S: every word fills its four records
    e2e('packed', packed, seeds[:4], expect=(1, 11, 12, 13))
    nocmp = dict(base, DK=0, DT=1)                                        # no comparator (theta = 2^-H)
    e2e('nocmp', nocmp, seeds[:2], expect=(1, 13))
    print('checks run: %d, failures: %d' % (NCHK[0], len(FAILS)))
    return len(FAILS)


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
```

### D.4 Output of `python3 other4_test.py 2 7`

```
routine tests: straight line (3 steps x 2 batches), prefilter, setup, setwalk, restart, evalF, outm, hit, DP (0, 5 and wrap over 7 full words; all 4 record places), match in each place, DP threshold (1024 walks), c=Tb
replay tests: 47 same-end pairs (lengths up to 52, all verified with independent Keccak, all counts exact), 13 distinct-end pairs (all halted cleanly), cap guard tested
end-to-end reduced-width runs:
  W=26, default reduced: 2/2 collisions verified, ops <= bound
  W=32, small replay cap LRC=8: 2/2 runs verified/halted within bound
  W=26, S=400 words: 2/2 collisions verified, ops <= bound
  W=26, hit cap HMAX=3: 2/2 runs halted at hit 4, ops <= bound
  W=26, step cap Tb=5: 2/2 runs halted at c=Tb, ops <= bound
  W=26, trail cap U=264: 2/2 runs halted at idn=U, ops <= bound
  W=26, S=200, U=800 (4 records/word exercised): 2/2 runs verified, ops <= bound
  W=26, DK=0, DT=1 (power-of-two DP): 2/2 collisions verified, ops <= bound
checks run: 422, failures: 0
```
