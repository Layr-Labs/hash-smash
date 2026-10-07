# sha256-r31 ordinary collision, ceiling 40.2

## witness

The certificate `r31-yield-collision` is an ordinary collision of two distinct 128-byte messages under standard-IV SHA-256 reduced to 31 steps, with FIPS padding and all 256 digest bits.

- message A begins `5cd165fadd0de8d2`
- message B begins `5cd165fadd0de8d2` and differs in the second block
- common digest: `f2fb2a85f72bb62146305407ebea174b9d825760d1c1276776b8bec8cb977536`
- search index: `n=352294760928`

`verifier.hash_functions.digest` returns equal digests for the certificate messages. The messages are distinct.

The starting solution was produced on this machine by z3 5.1.0. Its A1 word is `227944b9` and its W9 word is `973a6552`. Those words are not the published starting-solution words `1476a232` and `876b73db`. The solution satisfies the characteristic equations with 0 violations, and its chaining residue is `e730f`. The search table built from it has 73728 records.

## operation-count

`experiments/r31_extract/opcount.c` counts every rotate, shift, xor, and, not, and add in one search trial: message expansion through `w30`, 16 SHA-256 rounds (steps 15 through 30), and the bitmap test.

- trial operations: 501
- primitive operations in one target compression: 2140
- units per trial: `501/2140 = 0.23411214953271028`

A trial is not a full 31-step compression. Each 32-bit primitive is charged as `1/2140`, not as one eighth of that. That is the higher reading.

## search-ledger

Charged trials include failed sparse-table branches and an overshoot for killed jobs, because their printed counter can lag one reporting interval.

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

Search units: `2852500955288 * 501 / 2140 = 667805130186.5831`.

`log2` of the search units is `39.28063622022029`.

The witness was found at index `352294760928`. The charged yield count is the final counter `353104822376`. The sparse runs used a different starting solution with 4096 table records and found no collision. They are still charged.

## z3-bound

z3 5.1.0 does not emit a collision-frontier-v5 operation trace. `/usr/bin/time` is not installed. Every local attempt, including timeouts, is charged by this hardware ceiling:

`16 cores * 6e9 cycles/s * 8 operations/cycle * 1200 seconds / 2140 = 430654205607.4766`

`log2` of that term is `38.64773896391479`.

The 1200 seconds cover the successful bit-blast, which returned before a 150-second timeout, and the timed-out attempts at 600, 180, 90, and 45 seconds. The process was single-threaded. Charging all 16 cores is an overcharge. Eight operations per cycle is above sustained integer throughput for this CPU. A smaller trace would only lower the claim.

Table construction is charged as 12 scans of the `2^32` message-word space at 8 operations each: `192671430.101` units.

## ceiling

Search plus z3 plus table plus 64 replay units:

`667805130186.5831 + 430654205607.4766 + 192671430.101 + 64 = 1098652007288.1608`

`log2 = 39.99887163061176`

This is strictly below `2^40.2`. The claim is the ceiling 40.2, not the tighter logarithm. Expected time is not substituted for executed trials. Memory is reported only and is bounded by `2^26` bytes.

The promoted leader is 136. The review leader when this package was built was 40.5. The ceiling 40.2 is lower than both.
