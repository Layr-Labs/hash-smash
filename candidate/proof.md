# Generic birthday collision search with deterministic radix sorting

## 1. Claim and target profile

This submission is the provisional organizer baseline for `sha1-fips180-4-v1`: an
ordinary collision search against all 80 rounds of SHA-1. It is not a cryptanalytic
break and claims no improvement over prior work.

The one-run bounds are strictly less than `2^92` time units, strictly less than `2^87`
bytes of peak live memory, `2^80` chosen messages, no preprocessing or nonuniform advice,
and success probability greater than `0.39` under the random-function heuristic.

The organizer cost model is an abstract 128-bit word RAM with a flat `2^128`-word
address space. One complete one-block SHA-1 evaluation
costs one time unit. Every other 128-bit word-RAM primitive operation is also charged as
one full time unit, deliberately overcharging ordinary instructions relative to SHA-1.
Contiguous-array allocation creates a one-word descriptor and reserves the requested
address interval; it has no hidden arena or per-element allocator metadata. This is a
complexity-accounting machine, not a claim that the buffers fit on present hardware.

## 2. Preconditions and restrictions

Treat SHA-1 on the fixed message family below as a random function into 160-bit strings.
This is a heuristic assumption, not a theorem about concrete SHA-1.

Each message is the ASCII domain separator `HashSmash birthday v1:` followed by a
distinct 12-byte nonce. Choose the first `n = 2^80` nonce values in big-endian order.
Every message is shorter than 56 bytes and therefore uses exactly one SHA-1 compression
after standard padding.

## 3. Attack algorithm

Allocate two contiguous buffers `A` and `B`, each containing exactly `n` packed 32-byte
records. A record consists of a 20-byte complete SHA-1 digest followed by its 12-byte
nonce. Fill `A` by hashing every selected message once. `B` is initially scratch space.

Sort the records lexicographically by their complete 20-byte digest using stable least-
significant-digit radix sort. Perform exactly 20 byte-position passes. Each pass first
counts the 256 possible byte values, computes 256 prefix positions, then stably scatters
all records from the source buffer to the destination buffer. Swap the source and
destination roles after each pass.

Scan adjacent records in the final sorted buffer. If two adjacent records have equal
20-byte digests, return the messages reconstructed from their two nonces. Otherwise
report that this run found no collision.

## 4. Correctness argument

Radix sorting orders records by all 20 digest bytes, so every set of equal complete
digests is contiguous. The final scan therefore finds an equal-digest pair if and only
if the sampled set contains one. The nonces in two different records are distinct, so
their encoded messages differ byte-for-byte.

Each digest is standard SHA-1 with the specified IV, padding, all 80 rounds,
feed-forward, and 160-bit output. Any returned pair therefore satisfies the exact
ordinary-collision relation in the target profile. The algorithm can return no pair;
the next section bounds that event under the stated heuristic.

## 5. Probability argument

For `n` distinct inputs mapped independently and uniformly into `N = 2^160` outputs,
the probability of no collision is

```text
product from i = 0 to n - 1 of (1 - i/N).
```

Using `1 - x <= exp(-x)`, this is at most
`exp(-n(n-1)/(2N))`. For `n = 2^80`, the exponent is
`-1/2 + 2^-81`. Hence the collision probability is greater than `0.39`; its limiting
value is `1 - exp(-1/2)`, approximately `0.393469`. No independence statement is made
outside the explicit random-function heuristic.

## 6. Time accounting

Filling `A` performs exactly `n = 2^80` one-block SHA-1 evaluations. Message construction,
loop control, and record writes are charged separately below rather than hidden in that
count.

All indices, positions, and counters fit in one 128-bit word. In the histogram phase for
one record, two record-word loads, byte selection, one counter load/add/store, index
increment, and loop control use fewer than 16 charged operations. In the scatter phase,
the same byte selection, one position load/add/store, two record-word loads, two record-
word stores, index increment, and loop control use fewer than 32 charged operations.
Thus both phases together use fewer than 48, and therefore fewer than 64, operations per
record per radix position. The complete radix sort uses fewer than

```text
20 * 64 * 2^80 < 2^11 * 2^80 = 2^91
```

time units. Initial message construction, nonce increment, and the two-word record write
use fewer than 64 operations per record, hence less than `2^86`. The adjacent scan uses
fewer than 32 operations per record, hence less than `2^85`. All 20 prefix computations
touch only 256 counters, and setup touches only fixed state. Their sum is less than
`2^87`, and therefore certainly less than `2^90`. Consequently the total is less than
`2^91 + 2^90 + 2^80`, which is strictly below `2^92` time units.

## 7. Memory, data, and preprocessing accounting

Each packed record is exactly 32 bytes. Each of `A` and `B` holds `2^80` records and thus
uses exactly `2^85` bytes; together they use exactly `2^86` bytes. Both buffers remain
live during sorting.

The two buffers occupy valid, disjoint intervals well inside the model's `2^128`-word
address space. Each has one 16-byte descriptor. The two 256-entry 128-bit
counter/position arrays, current messages, returned messages, loop variables, SHA-1
state, and all other fixed state use less than `2^20` bytes. Thus
peak simultaneously live memory is less than

```text
2^86 + 2^20 < 2^87 bytes.
```

The attack hashes `2^80` chosen messages, performs no target-specific preprocessing, and
uses no reusable or nonuniform advice. The scalar pilot score is therefore
`92 + 87 = 179`.

## 8. Certificates, prior work, and known limitations

No concrete collision witness is supplied because this generic computation is infeasible
to execute in the MVP. The deterministic checker establishes package consistency only;
it cannot establish the random-function heuristic or the existence of a sampled collision.

This is an organizer integration baseline, not an improving participant submission. Its
central limitation is the heuristic treatment of concrete SHA-1 as a random function on
the selected family. Its intentionally loose time and memory bounds favor auditability
over competitiveness.
