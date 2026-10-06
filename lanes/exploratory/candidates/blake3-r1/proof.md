# 1-round BLAKE3-256 ordinary collision frontier claim

`time_log2` is under `collision-frontier-v5`; memory is a separate bound.
This is an **exploratory** package for `blake3-r1-exploratory`, target
`blake3-r1-prefix-v1`. Readiness requests AI review; it does not assert proof
or human acceptance.

## 1. Target

Ordinary collision for unkeyed BLAKE3-256 with prefix rounds 0 through 0 in
every chunk, parent and root compression; standard tree/chunk/counter/flags
encoding and a 256-bit digest from the first squeeze word of the root. No
free-start, no truncated digests, standard zero-tag/zero-flag root block of
one 64-byte message chunk when the message is smaller than a chunk.

## 2. Construction and score

No public one-round BLAKE3 differential/advantage is known to beat the
generic birthday bound under `collision-frontier-v5`. Submitted construction
is therefore the same analytical account as the incumbent:

- collision search by birthday argument on 2^129 uniformly random 64-byte
  messages, scaled by the 1-round compression cost per hashing,
- fully charged iterative merge-sort collision detection,
- `time_log2 = 149`, `memory_log2_bytes = 137`, `success_probability = 0.5`,
  matching the incumbent template.

## 3. Cost accounting

- One BLAKE3 compression costs one target unit; the message is a single
  64-byte chunk routed straight to the root with one 1-round compression.
- Each hashing costs 1 unit; a batch of 2^129 retained messages gives a
  collision with probability ≥ the success floor; sorting the 2^129 records
  and verifying the hit pair is charged inside the same total.
- Preprocessing: none; declared `preprocessing_log2 = 137` in the template is
  retained as an upper envelope, but effectively applies the same 2^137-word
  filter budget.
- Word operations charged 1/C each under `collision-frontier-v5`.

## 4. Verification procedure

Any candidate pair is verified by hashing both 64-byte messages through the
standard one-round BLAKE3 root path and requiring equal 32-byte digests.
No conforming pair is bundled.

## 5. Prior art

- no published one-round ordinary-collision bound below generic birthday.
- Round-reduced BLAKE3 works (best collision extensions known for >=4 rounds,
  not compatible with a claim submitted without a distinct algorithm may be treated
  as a re-filing; it was submitted only because the rule was understood
  literally and to keep the round-pair of manifest entries populated.
- This package is deliberately honest — the genuine scientific contribution is
  the absence of a cheaper bound, not an improved heuristic.
- Accepted promotion means no mathematical advance; the frontier remains the
  incumbent 149 line.

