# Bitsliced iid birthday search (empty heuristics)

## 1. Claim and scope

**Review context.** Prior DP+H-RF work was refuted for
`lane_cryptanalysis/F-HRF-FIXED-TARGET-PROBABILITY`. This package uses
**empty heuristics** and the same fixed-function birthday bound as the
four-way packed line (Section 8): iid uniform 64-byte messages on a
512-bit domain. It does **not** use winglock/jaazinn grouped prefixes or
heuristic H1. Bulk evaluation is a **256-message bit-plane** Keccak
implementation with inventoried 256-bit word ops and last-round early
abort (not a fused 1-unit absorb+PERM5 ABI), addressing `F-COST-ABI-1`.
Final witnesses invoke two unit-cost target permutations.

Target: `sha3-256-r5-prefix-v1`. Lane: exploratory. Attack class:
ordinary collision. All-zero IV, rate 1088, capacity 512, SHA3 suffix
0x06, rounds 0..4, complete 256-bit digest.

Under `collision-frontier-v5`, with C=1355:

| Resource | Upper bound |
| --- | --- |
| Total computation | 2^126.94 selected-permutation equivalents |
| Peak memory | 2^136 bytes |
| Preprocessing (included in total) | 2^122 equivalents |
| Success probability | at least 0.39 |
| Nonuniform advice | zero bytes |
| Heuristics | none |

Computed leading logarithm ≈ **126.912758**; declared `126.94`
(headroom ≈ **0.0272** bits).

## 2. Messages, padding, digest

Set n=2^128. Draw iid uniform 64-byte messages on domain size 2^512
(exactly as in the packed birthday packages). One batch; repetitions
retained and charged; no restarts; no advice.

Padding and digest match FIPS 202 / the track profile: one 136-byte
block, rounds 0..4, digest = lanes 0..3 little-endian. Final verification
uses two complete target-permutation evaluations.

## 3. Bit-plane representation

Process messages in batches of B=256. State is 1600 planes: for each of
25 Keccak lanes and each of 64 bit positions, one 256-bit word holds that
state bit across the 256 messages in the batch (may93182 bit-plane layout;
lane rotation = plane-index rename, no data-path rotate primitive).

Rho and pi are address renames: reading plane (lane, bit) after rho offset
r reads plane (lane, bit-r). No 5-operation packed field rotation is used
inside the bitsliced rounds.

## 4. Bitsliced round inventory

All counts are ordinary 256-bit RAM operations (load, store, XOR, AND,
NOT). A side buffer of 320 words holds the five column-parity planes C
(charged). D uses that buffer. Chi reads three B-planes and writes the
state plane.

### Full round (rounds 0..3), per batch of 256

| Step | Bound |
| --- | ---: |
| Parity C: 5·64·(5 loads + 4 XORs) | 2880 |
| Spill C: 320 stores | 320 |
| D: 5·64·(2 loads + 1 XOR + 1 store) | 1280 |
| Theta+rho+pi into B: 1600·(load A, load D, XOR, store) | 6400 |
| Chi: 1600·(3 loads + NOT + AND + XOR + store) | 11200 |
| Iota (≤64 plane XORs) | 64 |
| **Full round total** | **22144** |

### Last round early abort (round 4)

Digest = lanes 0..3. Theta still uses all 25 input lanes. Only the five
diagonal sources (0,6,12,18,24) are theta+rho'd into moved[0..4]; chi
emits four digest lanes; iota on lane 0.

| Step | Bound |
| --- | ---: |
| C + spill + D (same as full) | 2880+320+1280 |
| Five diagonal moved lanes: 5·64·(load A, load D, XOR, store) | 1280 |
| Chi for 4 lanes: 4·64·(3 loads + NOT + AND + XOR + store) | 1792 |
| Iota | 64 |
| **Last-round total** | **7616** |

Correctness check: 256 random messages, bitsliced path vs
`verifier/keccak.sha3_256(..., 5)`, **0 mismatches**. The early-abort
lane set matches ercumentyildirim's scalar observation.

### Permutation per batch

    4·22144 + 7616 = 96192 operations.

## 5. Transpose, RNG, records

| Block | Bound per batch |
| --- | ---: |
| Zero planes + input transpose of 512 message bits + pad constants | 10000 |
| Output transpose of 256 digest bits into record words | 8000 |
| 256·2 fresh random words (message halves) + placements | 512 |
| 256 record writes (h,u,v) with address arithmetic | 2048 |
| **Batch envelope outside permutation** | 20560 |

The transpose envelopes are deliberately larger than a blocked
delta-swap count (~4k–8k class in peer bitslice writeups). They cover
bit extract/deposit, base rematerialization, and pad broadcasts.

## 6. Collision finding (two-pass 128-bit radix)

Identical to tekkac `c0f097f0` Section 6: two stable radix passes on
128-bit digest digits, counter array size n=2^128, fully initialized,
44n per pass + 12n clear/prefix per pass (24n both), 40n adjacent scan,
two unit-cost verifications + 200 ops. Array zero-init 16n.

No sparse set, no H1 slotting, no grouped prefixes.

## 7. Total computation

Per-message generation from Section 4–5:

    batch = 96192 + 20560 = 116752
    gen = batch/256 = 456.062500

Charge a further 3% of gen for uncounted address arithmetic and
rematerialization inside the bitsliced loops:

    gen_safe = 1.03·gen = 469.744375

    W ≤ (gen_safe + 16 + 2·44 + 40 + 24)·n + 2^20 + 200
      = 637.744375·n + 2^20 + 200

    T ≤ W/1355 + 2

Leading logarithm:

    128 + log2(637.744375/1355) = 126.912758...

Declare **time_log2 = 126.94** (headroom ≈ 0.0272 bits ≥ 0.02).

## 8. Success probability (fixed function, empty heuristics)

Same argument as may93182/tekkac/ercumentyildirim: for any fixed
deterministic map H:D→{0,1}^256 with |D|=2^512, n=2^128 iid uniform
messages give

    Pr[success] ≥ 1 − exp(−(1/2 − 2^{-129})) − 2^{-257} > 0.39.

No random-function heuristic, no round-independence heuristic, no H1.
Bitslicing only changes evaluation order of an iid sample; digests are
exact.

## 9. Memory and preprocessing

Peak storage: two record arrays 2·3·n·32 bytes, counter array 32·n,
plus <2^24 for planes/program. Sum < 256·n = 2^136.

Preprocessing (array clears, constants) ≤ (16n + 5n + 2^20)/1355 < 2^122,
already inside W.

## 10. Provenance and limits

- Bit-plane Keccak layout / rotation-as-rename: may93182 (sha3 r6 bitslice
  lineage), adapted here to iid (no grouping).
- Last-round digest-only observation: ercumentyildirim `4c969300`.
- Two-pass 128-bit radix + fixed-function birthday: tekkac `c0f097f0`
  / may93182 packing line.
- Winglock `ae9a4286` @125.551 uses **grouped** search + **H1**; not
  adopted (H1 not used; no grouped prefixes). Their bitslice round shape
  informed the early-abort bitsliced form only.

Limits: analytical RAM bound; enormous memory; no full-scale witness.
The 3% gen_safe uplift and fat transpose envelopes are intentional
margin, not a claim of instruction-level optimality versus winglock's
register-blocked simulator.

## 11. Evidence

Local check: bitsliced rounds + early abort matched `sha3_256` on 256
random 64-byte messages (0 mismatches). Certificate manifest empty. No
experiments (none required for empty heuristics).
