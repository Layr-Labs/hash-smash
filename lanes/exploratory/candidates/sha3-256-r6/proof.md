# sha3-256-r6: bitsliced generic birthday search with an exact, executed ledger (time_log2 = 125.88)

## Claim

| field | value |
|---|---|
| target | `sha3-256-r6-prefix-v1` (SHA3-256 with prefix rounds 0–5), ordinary collision of the complete 256-bit digest |
| time_log2 | **125.88** (computed bound 125.8306; the claim also covers 12.58 uncounted operations per message) |
| success_probability | 0.39 (proved lower bound 0.39347, no heuristic) |
| memory_log2_bytes | 136 (computed 135.81) |
| preprocessing_log2 | 40 (one-time program construction; included in time) |
| nonuniform_advice_log2_bytes | 0 |
| heuristics | none |

No cryptanalytic weakness of the target is used. This is the birthday attack. The hash is not called as a unit-cost permutation. Every message is hashed by a charged bitsliced program that evaluates 256 messages per 256-bit word. That program is the file `experiments/keccak_bitslice.py`: the instruction list it executes is the one charged below.

## 1. Cost model and machine

`collision-frontier-v5`: one 6-round Keccak-f[1600] call costs one unit, and every other primitive 256-bit word-RAM operation costs 1/C with C = 1626. This package makes **no** permutation call. All work is primitive operations at 1/1626 each.

The machine is a 256-bit word RAM with 16 general registers, the size of the AVX2 register file:
- An ALU instruction (XOR, AND, OR, NOT, shift by a constant) reads registers and writes a register. It costs 1. As in any RAM instruction set, an instruction may carry a constant operand: a shift amount, or the 1 in a pointer increment.
- Every memory access is an explicit load or store. It costs 1.
- The hash program uses 15 registers. The 16th holds the write pointer for the keys.
- Fixed scratch areas (input planes, constants, spill slots) use direct (absolute) addresses written in the program text.
- Any address that depends on the batch or record index is formed by a charged ADD.
- Each independent uniform random 256-bit word costs 1.
- Comparisons and conditional branches cost 1 each.
- Program text is memory, not time.

## 2. Messages and batches

The attack hashes q = 2^128 messages in 2^120 batches of 256.

For batch b, draw 512 independent uniform words P_0, …, P_511. Message l (0 ≤ l < 256) is the 64-byte string whose bit i is bit l of P_i, for i < 512. Bit i means bit (i mod 8) of byte ⌊i/8⌋, which is the standard Keccak little-endian lane order. The 2^128 messages are therefore i.i.d. uniform over 64-byte strings.

A 64-byte message is a single SHA3-256 block (64 < 136). State bits 0–511 hold the message. Bits 513 and 514 are 1 (suffix byte 0x06 at byte 64). Bit 1087 is 1 (0x80 at byte 135). All other bits are 0. The digest is state bits 0–255 after rounds 0–5.

## 3. The bitsliced program

Word k of the program state holds state bit k of all 256 messages of a batch. The program is compiled once and is the same for every batch.

**Constants.** The 1,088 bits outside the message are equal in all 256 messages. Their words are 0 or all-ones, so the compiler folds them and never materialises them. Folding is exact: the folded program computes the same function, which the checks in Section 7 confirm.

**Complement flags.** For each word, the compiler records at compile time whether the stored word is the true value or its complement. XOR with an all-ones constant (padding bits, ι round-constant bits) flips the flag and emits nothing. XOR of two words XORs their flags.

**θ.**
- A column parity C[x][z] costs 4 XORs. It is accumulated as the χ outputs of the previous round leave registers.
- D[x][z] = C[x−1][z] ⊕ C[x+1][z−1] costs one XOR.
- Each state bit then costs one XOR with its D.

**ρ and π.** These only choose which word feeds which χ row, so they emit no instruction.

**χ.** For a row a_0..a_4, out_i = a_i ⊕ (¬a_{i+1} ∧ a_{i+2}). Using the flags, the term ¬b ∧ c costs:
- one AND when b is stored complemented and c is not;
- one OR when c is stored complemented and b is not, because b ∨ ¬c = ¬(¬b ∧ c), so the result is flagged;
- one AND or OR plus a NOT when the flags are equal.

A NOT of one element serves both terms that use it. A row is a 5-cycle, so it needs at least one NOT. For each row, the compiler picks the set of NOTs that minimises new instructions. It averages about 1.74 NOTs per full row. The XOR into a_i costs one more instruction.

**ι.** ι only flips the flags of lane (0,0) bits: zero instructions.

**Last round.** Only lanes (0..3, 0) form the digest, so only those four χ outputs of row y = 0 are computed. Their inputs are the θ outputs of lanes (x, x). D still needs every column parity.

**Sharing.** Identical subexpressions are shared, and anything that does not reach the digest is removed.

**Keys.** The 256 digest-bit words are transposed as a 256×256 bit matrix with the standard 8-stage butterfly. Each stage costs 6 ALU operations per word pair: SHR, XOR, AND with a mask, XOR, SHL, XOR.
- The stages commute, because stage s exchanges word-index bit s with bit-position bit s. They therefore run in three sweeps that fit in registers: stages 1, 2, 4 as each block of 8 digest words leaves the last round, then stages 8, 16, 32, then stages 64, 128.
- Flags are not undone. Key bit j of message l equals digest bit j ⊕ f_j for a fixed compile-time vector f. The key is therefore the digest XOR a constant: equal keys ⇔ equal digests.

**Register allocation.** Belady's rule on the straight-line program over 15 registers: evict the value whose next use is furthest. A value with a future use that has no memory copy is stored to a spill slot. Every reload is a load. Inputs are loaded from the scratch area IN, masks from the constant area, and each key is stored once.

**Counts per 256-message batch.** These are the exact instruction counts of the executed program. Each round's row covers its θ application, χ, ι and the parities for the next round.

| part | ALU instructions |
|---|---:|
| round 0 (including the first parities) | 6,074 |
| round 1 | 6,952 |
| round 2 | 6,963 |
| round 3 | 6,964 |
| round 4 | 6,939 |
| round 5 (four output lanes only) | 1,230 |
| transpose to keys | 6,144 |
| **ALU total** (XOR 27,072; AND 5,347; OR 3,933; NOT 2,866; SHL 1,024; SHR 1,024) | **41,266** |
| loads (inputs, masks, reloads) | 18,290 |
| stores (spills and the 256 keys) | 11,216 |
| **program total** | **70,772** |

That is 70,772 / 256 = **276.453125 operations per message** for the complete 6-round hash and its key. The unit-cost permutation would cost 1626.

Reproduce with `python3 experiments/keccak_bitslice.py --report`: stdlib only, under one second. It prints these counts. It also checks a 256-message batch against an independent scalar SHA3-256-r6 reference written in the same file (0 mismatches). We also compared 1,024 messages (4 batches) against the organizer's `verifier/keccak.py:sha3_256(…, rounds=6)` locally, with 0 mismatches. The organizer experiment (Section 7) re-hashes returned messages with the official function.

**Why the program is the target function, for every input.** Four links:
1. **Transcription.** `compile_keccak` is the FIPS 202 round function written over symbolic bits: the absorb layout, padding bits 513, 514 and 1087, prefix rounds 0–5 with θ, ρ, π, χ and ι, and digest bits 0–255. It mirrors the scalar reference `reference_sha3_256_r6` in the same file, which agrees with the organizer's `verifier/keccak.py`. This link is ordinary source reading, the same standard as for any reference implementation.
2. **Rewrite rules.** Every simplification goes through two functions, `bxor` and `andn`, and they branch only on: operands constant or not, operands the same node or not, the two flags, and the NOT choice. `check_rewrites` covers every such case with operands drawn from {0, 1, X, ¬X, Y, ¬Y}. It checks each result against its Boolean definition on all four assignments: 432 cases, 0 failures. `chi_row` only picks the NOT choice, ι is `bxor` with a constant, and the transpose uses no rules. So the graph computes exactly what link 1 writes down.
3. **Register program = graph.** `check_translation` runs the 70,772-instruction program on node names instead of values.
   - Every load must read a cell written earlier.
   - Every ALU instruction must rebuild exactly the graph node defined by its operand nodes.
   - At the end, OUT[l] must hold key node l, for all l.

   The program is straight-line, so this proves that it computes the key nodes for every input.
4. **Transpose.** A butterfly (j, s) swaps bit i+s of word j with bit i of word j+s, for every i with bit s of i clear. This is a one-bit identity, also checked. `check_transpose` applies the logged butterflies, in program order, to (plane, lane) labels at all 65,536 positions. It confirms that key l bit j is plane j bit l, with 0 failures.

Together these give key = digest ⊕ f for every 64-byte message. All four checks run in `--report` and in trial 0 of every experiment. They are deterministic and use no sampling.

## 4. The algorithm (fixed work on every tape)

Arrays:
- ARCH: 2^129 words, the input planes kept so that messages can be rebuilt.
- RK: 2^128 keys in generation order.
- K1, I1, K2, I2: key and index arrays, stored as separate arrays.
- CNT_1, CNT_2, CNT_3: counter arrays of 2^86, 2^85 and 2^85 entries, one per digit.

The digits of a key are bits 0–85, 86–170 and 171–255.

1. **Generate.** For b = 0 … 2^120 − 1:
   - (a) for i = 0 … 511, draw P_i, store it at IN[i], form ARCH + 512b + i, and store it there;
   - (b) run the program;
   - (c) store key l at RK + 256b + l;
   - (d) advance two base registers and the loop counter.
2. **Histogram.** Zero the three counter arrays. In one pass over RK, extract all three digits of each key and increment the three counters.
3. **Prefix sums.** Take an exclusive prefix sum over each counter array.
4. **Scatter** (LSD radix sort, stable):
   - pass 1 reads RK in order with index = position, and writes (K, index) to K1/I1 at CNT_1[digit 1]++;
   - pass 2 moves K1/I1 to K2/I2 by digit 2;
   - pass 3 moves K2/I2 to K1/I1 by digit 3.

   LSD radix sort with stable scatters sorts any key multiset. Precomputing all three histograms is valid because a histogram does not depend on record order.
5. **Scan.** Find the first i with K1[i] = K1[i−1].
   - If one exists, load I1[i] and I1[i−1] and rebuild both messages from ARCH. Output them if they differ, and report failure otherwise.
   - If none exists, report failure.

No loop bound depends on the data. The single data-dependent exit is charged in the fixed final term.

## 5. Ledger

Per message:

| step | operations | per message |
|---|---|---:|
| random planes | 512 RAND per batch | 2 |
| planes to IN | 512 ST per batch | 2 |
| planes to ARCH | 512 × (ADD address, ST) per batch | 4 |
| bitsliced program (Section 3) | 70,772 per batch | 276.453125 |
| key store addresses | one ADD per key advancing the 16th register (the store is inside the program count; the executed program writes the same store to the fixed slot OUT[l], and an OUT-to-RK copy would instead cost LD, ADD and ST, 2 more per message, inside the margin) | 1 |
| batch loop | 2 base ADDs, plus ADD/CMP/BR, per batch | 5/256 |
| histogram pass | ADD ptr, LD K; per digit SHR, AND, ADD addr, LD, ADD 1, ST (6 × 3); CMP, BR | 22 |
| scatter pass 1 | ADD ptr, LD K, ADD index; SHR, AND; ADD addr, LD, ADD 1, ST; ADD dst, ST K, ADD dst, ST index; CMP, BR | 15 |
| scatter passes 2, 3 | ADD ptr, LD K, ADD ptr, LD index; SHR, AND; ADD addr, LD, ADD 1, ST; ADD dst, ST K, ADD dst, ST index; CMP, BR | 2 × 16 |
| scan | ADD ptr, LD K, CMP, BR, register transfer, CMP, BR | 7 |
| **total** | | **92,537/256 = 361.47265625** |

The loops keep their pointers, bounds, masks, counter bases and the constant 1 in registers. Every loop needs at most 13 live registers, which fits in 16. The AND on the top digit is unnecessary but charged.

Fixed terms:
- **Counters.** Zeroing costs ST, ADD, CMP and BR per counter. The prefix sum costs LD, ADD, ST, ADD, CMP and BR per counter. That is at most 10 × (2^86 + 2^85 + 2^85) = 10 × 2^87 < 2^91.
- **Final step.** Rebuilding two messages takes 512 × 6 operations each. With the comparisons and output, it is below 2^16.
- **Set-up.** Writing the 9 constant words and initialising registers is below 2^8.
- **Program construction.** The straight-line program is generated once by the compiler in the experiment file: graph construction, sharing, dead-code removal and register allocation over fewer than 2^17 nodes. This one-time work is input-independent. We charge it generously at below 2^40 operations and declare it as preprocessing_log2 = 40.

Total charged time:

    T = 2^128 · (92,537/256) / 1626 + 2^91 + 2^40 + 2^16
      = 2^128 · 0.2223079… + 2^91 + 2^40 + 2^16
      = 2^125.8306.

The claim 125.88 bounds 2^128 · 374.05 / 1626. It therefore leaves 12.58 operations per message (3.5 %) for any line that a reviewer prices more strictly.

## 6. Success probability (proved, for this fixed function)

Let H be the fixed target. The digests H(M_i) of the q i.i.d. uniform messages are i.i.d. with some distribution p on N = 2^256 values.
- The probability that q i.i.d. draws from p are pairwise distinct is a Schur-concave symmetric function of p. It is therefore maximised by the uniform distribution (Munford 1977, "A note on the uniformity assumption in the birthday problem").
- For uniform p it is ∏_(i<q)(1 − i/N) ≤ exp(−q(q−1)/(2N)), and q(q−1)/(2N) = 1/2 − 2^−129.
- So Pr[some H(M_i) = H(M_j), i ≠ j] ≥ 1 − exp(−1/2 + 2^−129) ≥ 0.393469.

Keys are digest ⊕ f, so they collide exactly when digests collide. After sorting, equal keys are adjacent, so the scan finds an adjacent equal pair (i−1, i) whenever any equal pair exists.

Failure then needs M_{I1[i]} = M_{I1[i−1]}. That implies two equal messages among the q, which has probability at most q²/2^513 = 2^−257.

So Pr[success] ≥ 0.393469 − 2^−257 > 0.3934 ≥ 0.39. No assumption about H is used.

## 7. Organizer-executable experiments

**What the official runner can check.** The runner (`experiments/runner.py`, origin/main) has two trusted predicates for `python-message-pairs-v1`:
- a full collision;
- `digest-xor-mask`: for each returned pair (a, b), it recomputes both official digests and checks (H(a) ⊕ H(b)) ∧ mask = expected.

It has no predicate that compares a participant-supplied digest with the official one. A trusted check of absolute digest values is therefore not available, only XOR relations between two official digests. That relation is what the attack uses: it needs key(a) = key(b) ⇔ H(a) = H(b), not the digest values themselves.

**The sixteen experiments.** We use the strongest available form: sixteen experiments, `digest-slice-00` … `digest-slice-15`.
- Experiment k masks digest bits 16k … 16k+15 (bytes 2k and 2k+1) with expected 0. Together the trusted predicates cover all 256 digest bits.
- In each experiment, the program keys at least 32 batches (at least 8,192 messages) with the charged register program. The planes are expanded from the organizer seeds with SHAKE-256.
- For each trial, it returns two distinct messages whose program keys agree on slice k.
- The organizer recomputes both official digests and checks the slice.

**What this establishes.**
- Trusted fact: for 16 × 256 = 4,096 returned pairs, the official digests agree on the slice wherever the program keys agree.
- It does not establish anything about messages that were not returned, an error rate, or any extrapolation. The runner makes no probability inference and neither do we.
- The program's correctness for all inputs rests on the exact checks in Section 3, not on these trials. The experiments corroborate them on the official function.

**Untrusted observations** in trial 0 of every experiment:
- the full 256-bit comparison of one 256-message batch with the scalar reference (0 mismatches);
- the full-digest check of each returned pair (0);
- the results of the four exact checks in Section 3.

**Local runs.** Before submission we ran the organizer runner with its real Docker sandbox (the pinned python:3.12.12-slim-bookworm image, 1 CPU, 128 MiB) on all sixteen experiments, with the default 256 trials:
- status completed;
- 4,096/4,096 successes (256/256 in each experiment), with no repeated pair;
- a byte-identical replay for every experiment;
- 0 in every exact check and in every untrusted full-digest comparison;
- 41 s for all 32 container runs.

The bounded judge view was 97,622 bytes.

## 8. Memory

| item | bytes |
|---|---:|
| ARCH | 2^129 words |
| RK | 2^128 words |
| K1, I1, K2, I2 | 4 · 2^128 words |
| counters | 2^87 words |
| program, constants, spills, scratch | below 2^30 bytes |

At 32 bytes per word, the total is about 2^135.81 bytes. Memory is reported only; it is not scored.

Layout:
- All regions are disjoint fixed ranges of one address space of fewer than 2^133 words, so every address fits in a 256-bit word.
- Counters are zeroed before use.
- A spill slot is read only after the allocator has stored to it.
- IN and the constant area are written before the program runs.
- No uninitialised word is ever read.

## 9. What changed from our previous package

- Our earlier generic package (time_log2 128.17) charged one permutation unit (1626 operation-equivalents) per message. Here the hash costs 276.45 operations per message, executed and checked.
- Records (K, A, B) with a 4-pass sort became an input-plane archive plus (K, index) records. The sort now has 3 passes on 86-bit digits, with the histograms fused into one pass. The sort and scan cost 76 operations per message instead of 121.
- The fixed-work structure and the success proof are unchanged.

## 10. Prior work and credit

- **Bitslicing.** Biham, "A fast new DES implementation in software", FSE 1997.
- **Fewer NOTs in χ.** Bertoni, Daemen, Peeters, Van Assche and Van Keer describe the lane-complementing transform in "Keccak implementation overview". Our per-word complement flags with a per-row NOT choice are a compile-time variant of the same idea.
- **Bit-matrix transpose.** The butterfly is textbook; see, for example, Warren, *Hacker's Delight*, "Transposing a bit matrix".
- **Birthday bound for non-uniform functions.** Munford 1977.
- **On this track.** may93182 introduced bit-plane (bitsliced) Keccak evaluation in a generic package. jaazinn, tekkac and winglock published further refinements. Their public notes showed us the direction. The design, code, ledger and text here are our own; no text or code was copied.

## 11. Scope and limitations

- **Not cryptanalysis.** The attack is generic and says nothing about the strength of the target.
- **Machine assumptions.** The count assumes 16 registers, constant operands in instructions, and direct addressing for fixed scratch areas. Address arithmetic for anything that moves with the batch or record is charged. A model that also charged instruction fetch would cost more; the 12.58-operation margin covers modest stricter pricing, not that.
- **Transcription.** The equivalence argument in Section 3 is exact except for link 1, the transcription of FIPS 202 into `compile_keccak`, which is source-level. The organizer-checked slices and the reference comparisons corroborate it.
- **Randomness.** The experiment derives its planes from organizer seeds for reproducibility. The attack itself uses the model's independent random words.
- **No certificate.** A collision at this cost is infeasible, so none is supplied.
