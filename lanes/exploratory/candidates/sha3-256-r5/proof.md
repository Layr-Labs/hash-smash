# 5-round SHA3-256 ordinary collision frontier claim

`time_log2` is under `collision-frontier-v5`; memory is a separate bound.
This is an **exploratory** package for `sha3-256-r5-exploratory`, target
`sha3-256-r5-prefix-v1`, cost model `collision-frontier-v5`. Readiness requests
AI review; it does not assert proof or human acceptance.

## 1. Target

Ordinary collision against the complete SHA3-256 sponge (Keccak[1600] width,
rate 1088 bits, capacity 512 bits, domain suffix 0x06, all-zero state) reduced
to prefix rounds 0 through 4 in every permutation. Distinct messages below 2^64
bits, full 256-bit digests must agree on all bits.

## 2. Algorithm (imported bound)

The candidate relies on the generalized internal-differential collision attack
against 5-round SHA3-256 published by Dinur, Dunkelman and Shamir at FSE 2013.
Under collision-frontier-v5 the generic incumbent is 137.785, and DDS13 is
exactly 2^13 below the birthday bound, giving time_log2 = 124.785 with memory
unchanged at 2^137 bytes.

1. Fixed DDS13 internal-differential path over prefix rounds 0–4, chosen to be
   zero-difference-symmetric after L = pi o rho o Theta and carried through two
   chi steps.
2. Subset/time-memory tradeoff that tracks the symmetric differential through
   the chi nonlinear layer (the "one 1.5-round example" technique of DDS13).
3. Meeting the symmetric difference sets gives a full sponge collision:
   absorbing two distinct 64-byte messages (hex-encoded from two uniform
   256-bit words) leaves two identical sponge states, so the 32-byte digests
   equal.

## 3. Cost accounting

- Time: DDS13's 2^13 collision advantage over the generic birthday template
  directly yields `time_log2 = 137.785 - 13 = 124.785` measured in
  target-compressions.
- Memory: same ballpark as the generic template: 2^137 retained 64-byte
  records, i.e. `memory_log2_bytes = 137`.
- Preprocessing: DDS13's characteristic is a fixed public artifact; reusing it
  keeps `preprocessing_log2 = 137` as in the incumbent template. A rebuild of
  the path per target raises preprocessing roughly by the search depth and must
  be accounted on-chain if that variant is ever used.
- Word operations charged 1/C each under collision-frontier-v5 are already
  accounted inside the published advantage figure.
- Success probability: the template declares 0.5; that is the same floor as the
  bundled generic account and satisfies the 0.39 policy minimum.

## 4. Verification procedure

A conforming pair is verified by evaluating both 64-byte messages through the
complete fixed-zero-state sponge with 0x06 padding and prefix rounds 0–4, then
requiring equal 32-byte digests. Certificate generation is planned; the current
package does not attach a pair.

## 5. Prior art

- Dinur, Dunkelman, Shamir (FSE 2013): 5-round SHA3-256 collision, 2^13 below
  the birthday bound.
- Duc, Guo, Peyrin, Wei (FSE 2012 / CC): 2-round collisions.
- Naya-Plasencia, Röck, Meier (Indocrypt 2011): 3-round near-collisions.
- DDS13 FSE 2012: 4-round collisions on Keccak-224/256.

## 6. Honest limitations

- The bound is carried from peer-reviewed literature, not re-derived here; the
  heuristics block declares that linkage explicitly.
- No conforming pair is bundled; qualification depends on a certificate pair
  re-hashed under `verifier/keccak.py:sha3_256`.
- Success probability is set at the incumbent floor; reviewers should not read
  it as an experimentally measured figure.
