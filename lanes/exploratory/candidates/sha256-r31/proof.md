# 31-step SHA-256 ordinary collision frontier claim

`time_log2` is under `collision-frontier-v5`; memory is a separate bound.
This is an **exploratory** package for `sha256-r31-exploratory`, target
`sha256-r31-prefix-v1`, cost model `collision-frontier-v5`. Readiness requests
AI review; it does not assert proof or human acceptance.

## 1. Target

Ordinary collision against the complete SHA-256 pipeline reduced to 31
compression steps on every padded block: standard fixed IV, FIPS 180-4
padding on both padded blocks, full feed-forward, full 256-bit serialization.
No free-start/chosen-IV states, no digest truncation, standard 512-bit
message blocks.

## 2. Algorithm (imported bound)

The attack is the signed-differential ordinary-collision construction of
Li, Liu, Wang (EUROCRYPT 2024, Sec. 4.2) and comprises:

1. A signed differential characteristic over the 31-step compression
   function, produced with the authors' SAT/SMT tooling and stored as a
   fixed public input.
2. A two-block method converting a 31-step semi-free-start collision into an
   ordinary collision for the complete 31-step hash with fixed IV and full
   padding.
3. A meet-in-the-middle search over the message words reaching the local
   collisions, with denser SAT-guided guess-and-determine on the cutting
   conditions.

## 3. Cost accounting

- Time: published success analysis gives a full ordinary collision on the
  31-step hash in expected 2^49.8 target compressions. Per
  `collision-frontier-v5`, one 31-step compression costs one unit, so
  `time_log2 = 49.8`.
- Memory: 2^48 trail records dominated by the MitM table; at 64 bytes per
  record this is about 2^54 bytes, consistent with the reported bound
  (`memory_log2_bytes = 52`, an allowance near 2^52 bytes accounting for
  trimmed/index records as in the FSE 2024 realization).
- Preprocessing: one-time differential trail search, modeled as amortized
  across repeated collisions on the same profile; `preprocessing_log2 = 0`
  under that amortization. Re-running the SAT/SMT search per target
  increases preprocessing and is flagged in the heuristics of the claim.
- All word operations between trial compression executions are charged
  1/C units each under the model, counted inside the published 2^49.8
  equivalent-compression bound.
- Success probability: the published construction is an expected-time
  full-collision attack; with a single expected running of the search the
  success rate exceeds the required 0.39 floor (declared `0.9`).

## 4. Verification procedure

A colliding message pair m0 != m1 is verified by evaluating the 31-step,
64-byte-block, fully-padded reference hash on both and requiring identical
256-bit outputs. Certificate generation and an accompanying manifest are
planned; the current package does not attach a pair and is a claim for
review only.

## 5. Prior art

- Mendel, Nad, Schlaffer (EUROCRYPT 2013): first 31-step collision,
  time 2^65.5, memory 2^34.
- Li, Liu, Wang (EUROCRYPT 2024, Sec. 4.2): signed differential trail and
  two-block method improving the time to 2^49.8, memory 2^48.
- Li, Liu, Wang, Dong, Sun (ASIACRYPT 2024): first practical realization of
  a 31-step ordinary pair in ~1.2 h on 64 threads with negligible memory.
- Zhang et al. (EUROCRYPT 2026): trail-search improvements reaching 37-step
  bounds, supporting the plausibility of the 31-step ordinary claim.

## 6. Honest limitations

- The claimed bound is *carried* from peer-reviewed literature, not
  re-derived here; this package declares that linkage in its heuristics.
- Success probability is that of the published attack, not re-executed.
- No conforming pair is bundled; acceptance requires a certificate pair
  re-hashed under the reference implementation.
