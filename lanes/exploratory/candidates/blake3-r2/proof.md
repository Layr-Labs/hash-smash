# blake3-r2: bitsliced generic birthday search with an exact, executed ledger (time_log2 = 127.10)

## Claim

| field | value |
|---|---|
| target | `blake3-r2-prefix-v1` (BLAKE3-256 with prefix rounds 0–1), ordinary collision of the complete 256-bit digest |
| time_log2 | **127.10** (computed bound 127.0506; the claim also covers 7.76 uncounted operations per message) |
| success_probability | 0.39 (proved lower bound 0.39347, no heuristic) |
| memory_log2_bytes | 136 (computed 135.81) |
| preprocessing_log2 | 40 (one-time program construction; included in time) |
| nonuniform_advice_log2_bytes | 0 |
| heuristics | none |

No cryptanalytic weakness of the target is used. This is the birthday attack. The hash is not called as a unit-cost compression. Every message is hashed by a charged bitsliced program that evaluates 256 messages per 256-bit word. That program is the file `experiments/blake3_bitslice.py`: the instruction list it executes is the one charged below.

## 1. Cost model and machine

`collision-frontier-v5`: one 2-round BLAKE3 compression costs one unit, and every other primitive 256-bit word-RAM operation costs 1/C with C = 430. This package makes **no** compression call. All work is primitive operations at 1/430 each.

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

For batch b, draw 512 independent uniform words P_0, …, P_511. Message l (0 ≤ l < 256) is the 64-byte string whose bit i is bit l of P_i, for i < 512. Bit i means bit (i mod 8) of byte ⌊i/8⌋. The 2^128 messages are therefore i.i.d. uniform over 64-byte strings.

A 64-byte message is one chunk of one block. Its hash is a single root compression with:
- chaining value IV;
- counter 0;
- block length 64;
- flags CHUNK_START | CHUNK_END | ROOT = 11;
- rounds 0 and 1, with the standard message permutation between them.

Message word m_j is little-endian bytes 4j..4j+3, so bit t of m_j is message bit 32j + t. The digest is the eight words h_i = v_i ⊕ v_{i+8}, serialised little-endian, so digest bit j is bit (j mod 32) of h_{⌊j/32⌋}.

## 3. The bitsliced program

Word k of the program holds one bit of one 32-bit variable for all 256 messages. A 32-bit variable is therefore 32 words. The program is compiled once and is the same for every batch.

**Constants.** The initial state v_0..v_15 is IV, IV_0..IV_3, 0, 0, 64 and 11, the same for all messages. Its bits are compile-time constants (words 0 or all-ones) and are never materialised. Any gate with a constant input is folded. Folding is exact; Section 7 checks it.

**Complement flags.** For each word, the compiler records at compile time whether the stored word is the value or its complement. XOR with all-ones flips the flag for free. AND and OR of two words with equal flags cost one instruction, by De Morgan.

**Rotations.** Rotations by 16, 12, 8 and 7 are renamings of bit positions, so they emit no instruction. A 32-bit XOR costs 32 XORs.

**Addition mod 2^32.** Each addition is a ripple-carry chain of full adders on bit words:
- bit 0 has no carry in, so it is a half adder;
- bit 31 has no carry out, so it costs 2 XORs;
- bits 1–30 cost 5 instructions each: sum p ⊕ q ⊕ r, carry ((q ⊕ p) ∧ (r ⊕ p)) ⊕ p.

For the carry, the compiler picks as pivot p one of the three inputs whose two partners have equal flags. One always exists among three flags. So the AND never needs a NOT, and the program has no NOT instruction at all. A full addition costs 154 instructions, and a + b + m is two additions. With a constant operand, the bit costs at most 2: sum p ⊕ q, carry p ∧ q or p ∨ q, or the same through p ⊕ q when the flags differ.

**Sharing.** Identical subexpressions are shared, and anything that does not reach the digest is removed.

**Keys.** The 256 digest-bit words (with their flags) are transposed as a 256×256 bit matrix with the standard 8-stage butterfly. Each stage costs 6 ALU operations per word pair: SHR, XOR, AND with a mask, XOR, SHL, XOR.
- The stages commute, so they run in three sweeps that fit in registers: stages 1, 2, 4 as each block of 8 digest words is formed, then stages 8, 16, 32, then stages 64, 128.
- Key bit j of message l equals digest bit j ⊕ f_j for a fixed compile-time vector f. The key is therefore the digest XOR a constant: equal keys ⇔ equal digests.

**Register allocation.** Belady's rule on the straight-line program over 15 registers: evict the value whose next use is furthest. A value with a future use that has no memory copy is stored to a spill slot. Every reload is a load. Inputs are loaded from the scratch area IN, masks from the constant area, and each key is stored once.

**Counts per 256-message batch.** These are the exact instruction counts of the executed program.

| part | ALU instructions |
|---|---:|
| round 0 (48 additions, many with constant operands, plus XORs) | 6,794 |
| round 1 (48 additions × 154, plus 32 word XORs × 32) | 8,416 |
| digest h_i = v_i ⊕ v_{i+8} | 256 |
| transpose to keys | 6,144 |
| **ALU total** (XOR 15,697; AND 2,121; OR 1,744; SHL 1,024; SHR 1,024; NOT 0) | **21,610** |
| loads (inputs, masks, reloads) | 8,502 |
| stores (spills and the 256 keys) | 5,127 |
| **program total** | **35,239** |

That is 35,239 / 256 = **137.65234375 operations per message** for the complete 2-round hash and its key. The unit-cost compression would cost 430.

Reproduce with `python3 experiments/blake3_bitslice.py --report`: stdlib only, under one second. It prints these counts and checks a 256-message batch against an independent scalar BLAKE3-r2 reference in the same file (0 mismatches). We also compared 1,024 messages (4 batches) against the organizer's `verifier/hash_functions.py:digest(…, "blake3", 2)` locally:
- 0 key mismatches;
- 0 mismatches between our scalar reference and the official one.

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
| bitsliced program (Section 3) | 35,239 per batch | 137.65234375 |
| key store addresses | one ADD per key advancing the 16th register (the store is inside the program count) | 1 |
| batch loop | 2 base ADDs, plus ADD/CMP/BR, per batch | 5/256 |
| histogram pass | ADD ptr, LD K; per digit SHR, AND, ADD addr, LD, ADD 1, ST (6 × 3); CMP, BR | 22 |
| scatter pass 1 | ADD ptr, LD K, ADD index; SHR, AND; ADD addr, LD, ADD 1, ST; ADD dst, ST K, ADD dst, ST index; CMP, BR | 15 |
| scatter passes 2, 3 | ADD ptr, LD K, ADD ptr, LD index; SHR, AND; ADD addr, LD, ADD 1, ST; ADD dst, ST K, ADD dst, ST index; CMP, BR | 2 × 16 |
| scan | ADD ptr, LD K, CMP, BR, register transfer, CMP, BR | 7 |
| **total** | | **57,004/256 = 222.671875** |

The loops keep their pointers, bounds, masks, counter bases and the constant 1 in registers. Every loop needs at most 13 live registers, which fits in 16. The AND on the top digit is unnecessary but charged.

Fixed terms:
- **Counters.** Zeroing costs ST, ADD, CMP and BR per counter. The prefix sum costs LD, ADD, ST, ADD, CMP and BR per counter. That is at most 10 × (2^86 + 2^85 + 2^85) = 10 × 2^87 < 2^91.
- **Final step.** Rebuilding two messages takes 512 × 6 operations each. With the comparisons and output, it is below 2^16.
- **Set-up.** Writing the 9 constant words and initialising registers is below 2^8.
- **Program construction.** The straight-line program is generated once by the compiler in the experiment file: graph construction, sharing, dead-code removal and register allocation over fewer than 2^17 nodes. This one-time work is input-independent. We charge it generously at below 2^40 operations and declare it as preprocessing_log2 = 40.

Total charged time:

    T = 2^128 · (57,004/256) / 430 + 2^91 + 2^40 + 2^16
      = 2^128 · 0.5178415… + 2^91 + 2^40 + 2^16
      = 2^127.0506.

The claim 127.10 bounds 2^128 · 230.43 / 430. It therefore leaves 7.76 operations per message (3.5 %) for any line that a reviewer prices more strictly.

## 6. Success probability (proved, for this fixed function)

Let H be the fixed target. The digests H(M_i) of the q i.i.d. uniform messages are i.i.d. with some distribution p on N = 2^256 values.
- The probability that q i.i.d. draws from p are pairwise distinct is a Schur-concave symmetric function of p. It is therefore maximised by the uniform distribution (Munford 1977, "A note on the uniformity assumption in the birthday problem").
- For uniform p it is ∏_(i<q)(1 − i/N) ≤ exp(−q(q−1)/(2N)), and q(q−1)/(2N) = 1/2 − 2^−129.
- So Pr[some H(M_i) = H(M_j), i ≠ j] ≥ 1 − exp(−1/2 + 2^−129) ≥ 0.393469.

Keys are digest ⊕ f, so they collide exactly when digests collide. After sorting, equal keys are adjacent, so the scan finds an adjacent equal pair whenever any equal pair exists.

Failure then needs the two indexed messages to be equal. That implies two equal messages among the q, which has probability at most q²/2^513 = 2^−257.

So Pr[success] ≥ 0.393469 − 2^−257 > 0.3934 ≥ 0.39. No assumption about H is used.

## 7. Organizer-executable experiment

`experiments/manifest.json` declares one `python-message-pairs-v1` experiment that runs `experiments/blake3_bitslice.py`, the same program file whose counts are charged here. For each organizer seed, it does the following:
- It expands 512 plane words with SHAKE-256 and runs the 35,239-instruction register program on the simulated 16-register machine.
- It returns two distinct messages whose bitsliced keys agree on 8 digest bits: bits 0 and 7 of digest bytes 0, 8, 16 and 24, the declared `digest-xor-mask` event.
- With more than 512 trials, it reuses batches for further disjoint pairs.
- Trial 0 also reports, as untrusted observations, the instruction counts and a full 256-message comparison with the scalar reference.

The organizer re-hashes every returned pair with the official function. A wrong program would pass each trial with probability about 2^−8.

Before submission we ran the organizer runner (`experiments/runner.py` of origin/main) in two ways. The official intake executes the declared experiment itself, and its report, not ours, is the evidence.
- **Real Docker sandbox** (the pinned python:3.12.12-slim-bookworm image, 1 CPU, 128 MiB), default 256 trials: status completed, 256/256 successes and a byte-identical replay, 3.9 s for both runs together.
- **Docker replaced** by a local Python 3.12 subprocess, with the official BLAKE3 digest as the digest callback: 256 trials gave 256/256 with no repeated pair (under 1 s per run); 4,096 trials gave 4,096/4,096 (about 2 s per run).

The experiment shows that the charged program computes the target on the sampled messages. It does not measure attack cost, and the ledger does not rely on it for anything except that the counted program is the correct function.

## 8. Memory

| item | size |
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

- Our earlier generic package (time_log2 128.55) charged one compression unit (430 operation-equivalents) per message. Here the hash costs 137.65 operations per message, executed and checked.
- The sort became a 3-pass sort on (K, index) records, with the histograms fused into one pass. It costs 76 operations per message instead of 121.
- The fixed-work structure and the success proof are unchanged.

## 10. Prior work and credit

- **Bitslicing.** Biham, "A fast new DES implementation in software", FSE 1997.
- **Bitsliced ripple-carry addition.** The 5-gate full adder is textbook. Our pivot choice is a compile-time bookkeeping step that lets every carry use one AND without a NOT.
- **Bit-matrix transpose.** The butterfly is textbook; see, for example, Warren, *Hacker's Delight*, "Transposing a bit matrix".
- **Birthday bound for non-uniform functions.** Munford 1977.
- **On this track.** tekkac introduced packed-lane (SWAR) BLAKE3 evaluation with 36-bit lanes. On the SHA3 tracks, may93182 introduced bit-plane evaluation, and jaazinn and winglock published further refinements of these generic searches. Their public notes showed us that hashing below the compression unit was the direction. We use full bitslicing rather than packed lanes. The design, code, ledger and text here are our own; no text or code was copied.

## 11. Scope and limitations

- **Not cryptanalysis.** The attack is generic and says nothing about the strength of the target.
- **Machine assumptions.** The count assumes 16 registers, constant operands in instructions, and direct addressing for fixed scratch areas. Address arithmetic for anything that moves with the batch or record is charged. A model that also charged instruction fetch would cost more; the 7.76-operation margin covers modest stricter pricing, not that.
- **Randomness.** The experiment derives its planes from organizer seeds for reproducibility. The attack itself uses the model's independent random words.
- **No certificate.** A collision at this cost is infeasible, so none is supplied.
