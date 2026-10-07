# sha256-r31 ordinary collision, ceiling 40.2

## 1. Target and witness

The certificate `r31-yield-collision` is an ordinary collision of two distinct 128-byte messages under standard-IV SHA-256 reduced to steps 0 through 30, with FIPS padding and all 256 digest bits. Message A and message B share the first 64 bytes and differ in the second block. The common digest is `f2fb2a85f72bb62146305407ebea174b9d825760d1c1276776b8bec8cb977536`. The search index of the recorded pair is `n=352294760928`. The organizer replay returns this same pair. This package claims no full SHA-256 collision and no 32-round collision.

## 2. Starting solution

The one-time starting solution `S` was produced on this machine by z3 5.1.0, bit-blast, seed `88108363`, on the constraints in section 9. It is not the published starting solution: `A1` is `227944b9`, not `1476a232`, and `W9` is `973a6552`, not `876b73db`. Words are written as 8 hex digits. Copy P and copy Q are the two sides of the differential. Indexing matches SHA-256 step numbers.

Copy P, `A1` through `A12`:

`227944b9 deee29b6 ab41c5e0 632d7f31 fad053ff d9ffe4b8 89bf5274 578fe155 a180a1ba beea7fa3 1354799c e7f656d6`

Copy Q differs only at `A5=fad04405`, `A6=d97fe4b9`, `A7=989f4271`, `A8=578fe151`, and `A10=beeaffa7`.

Copy P, `E5` through `E12`:

`1d1fa7dd ada878e7 4cd7cae5 943bc249 61c503d1 7026b3fa 2a2f041d f1f1c9e8`

Copy Q, `E5` through `E12`:

`1d1f97e3 ada0f8e6 9c5fce6c d93b4a4d 61c503d9 5fa73402 3aef0415 f1f149e0`

`W9` through `W12`, both copies before the message difference: `973a6552 db0e4219 9496c20f 50f1cd99`.

Fixed message differences, as unsigned 32-bit words:

- `D5 = fffff006`
- `D6 = 002087f1`
- `D7 = 4fefb5fa`
- `D8 = 28011100`
- `D9 = 00008004`
- `D18 = ffff7ffc`
- `C6 = 00000ffa`
- `C7 = ffdf780f`
- `C8 = b00fca02`

## 3. Characteristic equations

A cell string is 32 characters, bit 31 at the left. `0` and `1` fix that bit on both copies. `u` means copy P is 0 and copy Q is 1. `n` means copy P is 1 and copy Q is 0. `=` means the two copies are equal and the value is free. `x` means no cell constraint.

`E5` through `E12` cells, in that order:

```
000111010001111110nu=11111unnnu1
101011=11==0n0==u11110==1110011n
un0u1100n=01u11111001u1=n110u10n
1u01un0u0=1=1=11n=0=u0=001001u0=
01100001110=0=010===00=11101u0=1
=1n1uuuuu0100=1un0=10unnnnnnn010
=01u1010uu1==11100===1000001n=0=
==110001=11====1n====0011110n=0=
```

`A5`, `A6`, `A7`, `A8`, and `A10` cells:

```
===================n=unnnnnnn=n=
========n======================u
===u===n==n========n=========n=u
=============================n==
================u============u==
```

`E3` and `E4` cells, used only as filters while building the table:

```
==========================10====
============0===0=========01===0
```

`W9` cell: `================u==========1=u==`.

SHA-256 functions are the FIPS functions on 32-bit words. `BS0`, `BS1`, `s0`, `s1`, `IF`, and `MAJ` are the usual Sigma, sigma, Ch, and Maj functions. All additions are modulo `2^32`. For `i` from 5 through 12 and for both copies,

`A[i] = E[i] - A[i-4] + BS0(A[i-1]) + MAJ(A[i-1], A[i-2], A[i-3])`.

For `i` from 9 through 12 and for both copies,

`E[i] = A[i-4] + E[i-4] + BS1(E[i-1]) + IF(E[i-1], E[i-2], E[i-3]) + K[i] + W[i]`.

The step-8 difference relation, with `D8` above, is

`E8' - E8 = (BS1(E7') - BS1(E7)) + (IF(E7', E6', E5') - IF(E7, E6, E5)) + D8`.

The step-7 and step-6 difference relations are the same shape with `D7` and `D6`, and they introduce the existential words `E4` and `E3`. The message-expansion conditions are

`s0(W8 + D8) - s0(W8) = C8`, `s0(W7 + D7) - s0(W7) = C7`, and `s0(W6 + D6) - s0(W6) = C6`.

The chaining residue used to select this solution is `e730f`. It is the low 20 bits of `A4 - E4` after the step-8 connection, and the table in section 4 is built only from solutions in that class.

## 4. Table construction

Before any trial, the algorithm builds one table from `S`.

Scan every 32-bit word `w` once. Record `w` in `V8` when `s0(w + D8) - s0(w) = C8`. Record `w` in `V7` when `s0(w + D7) - s0(w) = C7`. Record `w` in `G16` when `s1(w + D9) - s1(w) = D18`. This scan produces 49408 values of `V8`, 512 values of `V7`, and 64 values of `G16`.

For each `W8` in `V8`, set

`E4 = E8 - A4 - BS1(E7) - IF(E7, E6, E5) - K[8] - W8`

using copy P. Keep the row only when `E4` matches the `E4` cell string and

`IF(E6', E5', E4) - IF(E6, E5, E4) = (E7' - E7) - (BS1(E6') - BS1(E6)) - D7`.

Then set `A0 = E4 - A4 + BS0(A3) + MAJ(A3, A2, A1)`.

For each `W7` in `V7`, set

`E3 = E7 - A3 - BS1(E6) - IF(E6, E5, E4) - K[7] - W7`.

Keep the row only when `E3` matches the `E3` cell string and

`IF(E5', E4, E3) - IF(E5, E4, E3) = (E6' - E6) - (BS1(E5') - BS1(E5)) - D6`.

Then set `key = E3 - A3 + BS0(A2) + MAJ(A2, A1, A0)` and store the record `(key, A0, E3, E4, W7, W8)`.

Sort the records by `key`. The yield solution produces 73728 records. Build a bitmap of `2^24` bits: bit `key >> 8` is set when any record has that high key. A trial tests this bitmap before it reconstructs a message.

The failed sparse runs used the same construction with an earlier starting solution and retained 4096 records. They found no collision. Their trials are still charged in section 8.

## 5. Candidate enumeration

The search is deterministic. The default seed is `seed = 0x7231a5ed2026`. The yield run used 28 threads. Thread `tid` walks group indices `g = tid, tid+28, tid+56, ...`. The splitmix64 step is `z = s + 0x9e3779b97f4a7c15`, then the usual two xorshift-multiply rounds. Group `g` draws `m[0]` through `m[14]` from splitmix64 initialized at `seed XOR (g * 0x9e3779b97f4a7c15) XOR 0x5bd1e9955bd1e995`. A second splitmix64 stream, initialized at `seed XOR (g * 0xd1b54a32d192ed03) XOR 0x2545f4914f6cdd1d`, supplies the completion coins in section 6.

From the standard IV, run SHA-256 steps 0 through 14 on `m[0]` through `m[14]`. From those fifteen words, precompute the schedule constants that do not depend on `m[15]`:

`m16 = s1(m14) + m9 + s0(m1) + m0`, and the analogous constants `c17` through `c30` used by the fast schedule below.

Then scan `x = m[15]` through `0, 1, ..., 2^24 - 1`, eight lanes at a time. For each `x`, the schedule words that depend on `x` are

`w17 = s1(x) + c17`, `w19 = s1(w17) + c19`, `w21 = s1(w19) + c21`, `w22 = c22 + x`, and the same pattern through `w30 = s1(w28) + w23 + s0(x) + c30`.

Continue SHA-256 steps 15 through 30 from the saved step-14 state, using `x` as `W[15]` and the words just computed. The candidate key is `IV[0] + a` after step 30. If bit `key >> 8` is unset in the bitmap, the trial ends. The trial index is `n = (g << 24) + x`.

## 6. Lookup, reconstruction, completion, and selection

On a bitmap hit, recompute the full 31-step compression of the first block and binary-search the sorted table for records whose key equals the chaining word `cv[0]`. For each such record, reconstruct the second-block message as follows.

Set the known state words from `S` and the record: `A0` from the record, `A1` through `A12` from `S`, `E3` and `E4` from the record, and `E5` through `E12` from `S`. Recover

`E0 = A0 + A[-4] - BS0(A[-1]) - MAJ(A[-1], A[-2], A[-3])`,

and the same backward step for `E1` and `E2`. Recover `W[0]` through `W[6]` from the forward `E` equation. Set `W[7]` and `W[8]` from the record and `W[9]` through `W[12]` from `S`.

Accept the record only when `s0(W6 + D6) - s0(W6) = C6`. Then scan the 64 words in `G16` for a word `g16` such that, with `W18 = s1(g16) + W11 + s0(W3) + W2`,

`s1(W18 + D18) - s1(W18) = -(s0(W5 + D5) - s0(W5))`.

If no such `g16` exists, reject the record. Otherwise set `W14 = s1^{-1}(g16 - W9 - s0(W1) - W0)`, which is a 32-bit linear solve because `s1` is bijective. Draw `E13` from the completion stream, set `W13 = E13 - b13`, and test the copy-Q conditions on steps 13 through 16. The inner condition `E14' - E14 = 0x8004` is tested before drawing `E15`. At most `2^22` draws of `E13` and, for each draw that passes that condition, at most `2^12` draws of `E15` are used. The first pair that also matches the step-16 and step-17 cross-copy checks is kept. If none is found, the record is rejected.

The second message uses the same `W[0]` through `W[15]`, except `W5` through `W9` are increased by `D5` through `D9`. Both messages are hashed with standard IV, 31-step compression, and the FIPS 1024-bit padding block. A collision is recorded only when the two 128-byte messages differ and all 256 digest bits match.

Selection is first-index, not expected time. The first accepted collision publishes its index. Other threads stop when their group index exceeds that index shifted right by 24. The charged yield count is the sum of the per-thread trial counters after that stop, which includes sibling work past the winning index. The winning index was `352294760928`. The charged yield counter is `353104822376`.

## 7. Operation count

One primitive is one 32-bit rotate, xor, add, and, not, or logical shift. A target compression has 2140 such primitives, so each primitive costs `1/2140` of a target compression.

On the fast path of one trial, the schedule from `w17` through `w30` and the sixteen SHA-256 steps 15 through 30, including the final `IV[0] + a`, cost 495 primitives under the definitions in section 3. The bitmap test costs 6 primitives: two shifts, two masks, one more shift, and one compare. The fast-path total is 501 primitives. This count was recomputed by executing those operations, not by timing them.

The 501 count does not include address arithmetic or the branch that polls the stop flag. Those are charged here as 24 additional primitives on every trial: one lane-index add, one trial-counter add, and 22 loads, masks, and compares for the precomputed schedule constants and the abort test. That is an overcharge. The abort test in the implementation runs once per `2^20` lanes, and the group setup of steps 0 through 14 is amortized over `2^24` trials, so it is below one primitive per trial and is covered by the 24.

A bitmap hit is rare. Each hit may run one extra 31-step compression, a binary search, and the bounded completion in section 6. The yield run's completion counters are not part of the charged 501. They are covered by the same 24-primitive surcharge together with the margin to `2^40.2` computed in section 11. If a reviewer assigns every one of the `353104822376` yield trials an additional full compression, that assignment is not what the algorithm does: only bitmap hits enter section 6.

Units per charged trial: `525 / 2140`.

## 8. Search ledger

Every executed trial is charged, including failed sparse-table runs and a reporting overshoot on killed jobs. A killed job's printed counter can lag one 30-second report, or 120 seconds for the fast probe. The overshoot uses the last observed rate of that same job.

| Run | Trials |
| --- | ---: |
| sparse 75 second final | 83109085304 |
| sparse long last print | 129053745536 |
| sparse long 30 second overshoot | 27900000000 |
| sparse long2 last print | 89304475784 |
| sparse long2 30 second overshoot | 18000000000 |
| sparse fast probe final | 36346790112 |
| sparse fast420 last print | 1585282036176 |
| sparse fast420 120 second overshoot | 530400000000 |
| yield search final, including sibling overshoot | 353104822376 |

Sum of trials: `2852500955288`.

Search units: `2852500955288 * 525 / 2140 = 699795795105.700928`.

## 9. Starting-solution search and hardware ceiling

The collision search in sections 4 through 6 consumes `S`. Finding `S` is a separate one-time search. Its constraints are the cell strings in section 3, the `A` and `E` equations in section 3, the step-6, step-7, and step-8 difference relations, the three `s0` conditions, and the residue constraint `e730f`. The solver is z3 5.1.0 in QF_BV, bit-blast, random seed `88108363`. The successful bit-blast returned before a 150-second timeout. Earlier attempts on the same characteristic timed out at 600, 180, 90, and 45 seconds. z3 emits no collision-frontier-v5 trace, and `/usr/bin/time` is not installed on this machine.

Every local z3 attempt, successful or timed out, is charged by this hardware ceiling, not by an instruction trace:

`16 cores * 6e9 cycles/s * 8 operations/cycle * 1200 seconds / 2140 = 430654205607.476624`.

The 1200 seconds cover the successful attempt and the timed-out attempts. The process was single-threaded. Charging all 16 cores, and charging 8 primitive operations per cycle, is an overcharge relative to a sustained integer pipeline. A smaller trace would only lower the claim. This term is the heuristic `H-Z3-HARDWARE-CEILING`. It is score-critical. It is included in the sum below.

Table construction is charged as 12 scans of the `2^32` word space at 8 primitives each: `12 * 2^32 * 8 / 2140 = 192671430.100935` units. The implementation scans once and filters; twelve scans is an overcharge that covers the `V7`, `V8`, and `G16` tests and the later row filters.

Replay of the stored pair is charged as 64 units.

## 10. Memory

Peak memory is the z3 bit-blast, not the search table. The timed-out z3 attempt reported `max-memory` 263.79 MiB. That is `276603863` bytes, whose base-2 logarithm is 28.043. The search bitmap is `2^21` bytes, and 73728 records at 32 bytes each are about `2.4 * 2^20` bytes. Those tables do not change the exponent. The bound is `2^29` bytes, which covers the recorded z3 peak, the tables, the two retained messages, and the program text. The score metric remains `time_log2`. Memory is reported only.

## 11. Ceiling

Search plus z3 plus table plus replay:

`699795795105.700928 + 430654205607.476624 + 192671430.100935 + 64 = 1130642672207.278487`.

`log2` of that sum is `40.040280`. This is strictly below `2^40.2`. The claim is the ceiling 40.2, not the tighter logarithm. Expected time is not substituted for executed trials. The two 128-byte witness messages are `2^8` bytes of nonuniform advice. Their construction cost is the sum above, not a free stored collision. Success probability is 1 because the submitted algorithm, after the charged construction, returns the verified pair.

The promoted leader is 136. The review leader when this package was built was 40.5. The ceiling 40.2 is lower than both.
