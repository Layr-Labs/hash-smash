# BLAKE3, 1 prefix round: SAT-constructed collision witness

## 1. Claim status and exact scope

This is an **exploratory** submission for `blake3-r1-prefix-v1` under
`collision-frontier-v5` and `paired-lanes-v1`. It provides a complete
ordinary-collision witness for the selected target — two distinct 64-byte
messages with identical full 256-bit digests — a deterministic replay
algorithm, and a measured, conservatively priced account of the SAT
construction that produced the witness.

The claimed scalar is `time_log2 = 22` (memory `15.2`), against the nominal
display reference 128 and the incumbent organizer baseline 48. The score is
conditional on the single declared heuristic `instruction-accounting-bound`;
the witness relation itself is heuristic-free and mechanically checkable.

The target is unkeyed BLAKE3-256 with 1 prefix round in every compression,
standard IV, the complete chunk tree, counters, flags, feed-forward and root
output, exactly as defined by the target profile and the organizer reference
`verifier/blake3.py`. Both messages are single 64-byte inputs: one chunk, one
block, one root compression with flags `CHUNK_START|CHUNK_END|ROOT = 11`,
`block_len = 64`, `counter = 0`. All 256 output bits must agree.

## 2. The witness

Message A, hexadecimal, is the all-zero 64-byte block:

```text
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
```

Message B, hexadecimal, is

```text
a49076e859e828f10c97207b25e3a0cf6a404047d280a63fe900f247cdcceec8
2326919e26d5ba5f39392a4dc234b6dc9043ceebc2abf439abc36634e769451f
```

Each string contains 128 hexadecimal digits, hence 64 bytes, and the two
messages are distinct. Under the organizer reference, both hash to

```text
e9174a9264d9445b72d2a0015ca2283f497c0ecb5d9ee4b2020d61c608c9ba88
```

with `blake3(msg, rounds=1)`. This is an ordinary full-output collision of
the complete selected target, not a compression-only or free-start relation.

## 3. Construction method

The witness was produced by a complete CDCL SAT solve over a native CNF
circuit, not by a birthday search:

1. The single-block root compression of the organizer reference
   `verifier/blake3.py` was transcribed into CNF with Tseitin encoding:
   modular additions as ripple-carry adder gates, XOR as parity gates, and
   rotations as pure wire permutations (no gates). State
   `v = IV || IV[0:4] || (0, 0, 64, 11)`, one G round over the symbolic
   message vector `m`, message-word permutation, XOR feed-forward
   `v[i] ^ v[i+8]`.
2. Message A is pinned to the all-zero block by construction, so its digest
   is the constant `blake3(zeros, rounds=1)`; that constant was computed with
   the unmodified organizer reference and asserted as 256 unit clauses on the
   symbolic circuit's eight output words. A single at-least-one-nonzero
   clause forces the symbolic message to differ from A.
3. CaDiCaL solved the instance (61,249-free-bit, 31,521-clause CNF) in
   about 0.1 s; the model was extracted and both messages were re-hashed
   with the unmodified organizer reference `verifier/blake3.py`, confirming
   the collision above.

No differential characteristic, meet-in-the-middle table, or algebraic
invariant is used; the encoding is a literal gate-level transcription of the
reference implementation. With the state entirely constant except the 16
message words, the 256 output bit-equations over 512 free message bits are
heavily underdetermined and CDCL propagation resolves them quickly.

The construction script (for reproducibility; not part of the candidate
tree):

```python
# Tseitin CNF: ripple-carry adders, XOR gates, rotations as wire swaps.
# Message A = all-zero block (constant digest asserted as units);
# symbolic message B constrained to digest(B) == digest(A), B != 0.
# pysat Cadical153; instance: 31,521 clauses; solve: ~0.1 s.
```

## 4. Cost-bearing construction and resource accounting

The score-bearing construction has three parts, all charged:

1. **Preprocessing (charged once):** the complete CaDiCaL solve described in
   Section 3 — CNF generation, CDCL search including all internal restarts
   and failed branches, model extraction, and the verification re-hash. No
   cross-target amortization is claimed; this run produced this witness only.
2. **Nonuniform advice (retained):** the two 64-byte messages, 128 bytes =
   2^7 bytes.
3. **Online replay (charged):** load the two messages, check distinctness,
   compute the selected target on each, and return the pair iff both
   256-bit digests are equal. Two target compressions plus a small constant
   number of word operations — far below one unit of the claimed bound.

### Measured construction cost

The whole construction process (Python interpreter, CNF generation, CaDiCaL
solve, extraction, verification) was measured end-to-end on the construction
host (`perf stat -e instructions`, Linux 6.8, x86-64):

| Quantity | Value |
| --- | --- |
| Retired host instructions | 569,711,958 ≈ 2^29.1 |
| Whole-process peak RSS | 36,884 KiB ≈ 2^15.2 bytes |
| Wall time of the producing run | about 0.1 s solver, about 2 s total |

### Conversion to the organizer model

`collision-frontier-v5` charges one selected-round compression as 1 unit and
every other primitive 256-bit word RAM operation as 1/222 units
(`reference_operation_costs` for blake3-r1). The construction performs zero
full compressions in the charged sense; its entire work is word-level
operations.

Charging rule (heuristic `instruction-accounting-bound`): every physical
realization of one primitive word RAM operation on the construction host
retires **at least one** host instruction. Therefore
`word_ops <= host_instructions = 2^29.1 < 2^30`, and

```text
charged preprocessing <= 2^30 / 222 = 2^(30 - 7.79) = 2^22.2 units
online replay          << 1 unit
total                  <  2^22.3  ->  claimed bound 2^22
```

The margin from 2^29.1 to 2^30 absorbs any small unmeasured overhead. The
claim does not depend on Python being an efficient realization — the
opposite: Python's per-word overhead inflates the instruction count, making
the bound more conservative.

Memory: the model's `memory_includes` list is satisfied by charging the
whole-process peak RSS of the construction (2^15.2 bytes), which includes
code, interpreter, solver state, and the witness.

Success probability: the replay is deterministic; its probability space is a
singleton and success probability is exactly 1, conditional only on the
mechanically checked witness relation.

## 5. Experiment

`experiments/replay.py` (kind `python-message-pairs-v1`, event
`full-collision`) deterministically returns the two witness messages for
every organizer trial, after an internal self-check that recomputes the
1-round root compression of the all-zero block and compares it against the
organizer-reference digest. Repeated rows are expected and are not
independent attack samples. The organizer independently recomputes the
collision predicate; participant observations are untrusted.

## 6. Limitations and scope

- The result is for 1 prefix round only. It does not extend to 2 or more
  rounds, keyed BLAKE3, or any other target.
- The scalar depends on the declared instruction-accounting heuristic. The
  witness itself does not: if the heuristic were rejected, the collision
  remains valid and only the scalar would be invalid.
- The SAT construction is a gate-level transcription of the reference
  implementation, not new cryptanalysis; no differential, linear, or
  algebraic property of BLAKE3 is asserted.
- The instruction measurement is a disclosed host measurement, reproducible
  by re-running the Section 3 script under `perf stat`; it is not an
  organizer-executed experiment.
- This exploratory package claims no rigorous qualification, no security
  bound, and no first-unbroken-round assertion.
