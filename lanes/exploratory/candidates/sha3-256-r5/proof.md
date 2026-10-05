# Generic five-round SHA3-256 collision by two-pass radix sorting

The scalar in this package is `time_log2` under `collision-frontier-v5`.
Memory is reported separately. The construction uses one batch of `n=2^128`
independent 64-byte messages, evaluates the exact selected hash once per sample,
and sorts the 256-bit outputs with two stable radix passes whose digits are 128
bits wide. Its charged time is below `2^128.222` target-permutation units, peak
memory is below `2^136` bytes, and success probability is greater than `0.39`.

This is a generic finite-function argument. It assumes no statistical property
of SHA3, its rounds, or its output. The only randomness is the word RAM's stated
primitive for fresh independent uniform 256-bit words. There is no random-oracle,
differential, round-independence, or empirical premise, so `heuristics` is empty.

## 1. Exact complete hash

Each sampled message is exactly 64 bytes. Two independently sampled 256-bit
words `u,v` encode

    m = LE32(u) || LE32(v),

where `LE32` emits all 32 little-endian bytes, including leading or trailing
zero bytes. This is a bijection between pairs `(u,v)` and a domain `D` of
`2^512` distinct byte strings.

For each message, initialize the 1600-bit Keccak state to zero. Append SHA3's
delimited suffix byte `0x06`, then zero bytes, then the final `0x80` byte, making
the single 136-byte rate block

    m || 0x06 || (70 zero bytes) || 0x80.

XOR the block into the 1088-bit rate in standard little-endian Keccak lane and
bit order. Capacity bits remain zero. Apply, in order, original Keccak-f rounds
0, 1, 2, 3, and 4. Each round applies theta, rho, pi, chi, and iota; chi reads
all of its right-hand side from a temporary row. The five round constants are

    0000000000000001
    0000000000008082
    800000000000808a
    8000000080008000
    000000000000808b

The output `H(m)` is the first 32 squeeze bytes after round 4. This is the full
256-bit digest. Since 32 bytes are less than the 136-byte rate, no further
permutation is needed. Every complete hash therefore uses exactly one selected
five-round target permutation. The state is fixed-IV and the result is neither
free-start, compression-only, truncated, nor a raw-permutation collision.

## 2. Algorithm

Let `n=B=2^128`. Use seven arrays of 256-bit words:

- source arrays `Hs,Us,Vs`, each of length `n`;
- destination arrays `Hd,Ud,Vd`, each of length `n`; and
- a count/position table `P`, of length `B`.

The six record arrays form two structure-of-arrays representations of triples
`(h,u,v)`. A digest is held in one 256-bit word using the target's byte order.
The table index and every address fit in a 256-bit word.

1. For each `i` from 0 through `n-1`, draw fresh independent uniform words
   `u,v`, build the exact padded state from Section 1, call the selected target
   permutation once, and store the triple `(H(m),u,v)` in the source arrays.
   Repeated messages are retained. There is no resampling.
2. Stably sort by the low 128 digest bits. Clear every `P[d]`; count each digit;
   replace the counts by exclusive starting positions; then scan the source in
   order, copy each complete triple to the next destination position for its
   digit, and increment that position. Swap source and destination array roles.
3. Repeat the same stable pass using the high 128 digest bits, and swap roles
   again. Stable least-significant-digit radix sorting makes the resulting
   sequence nondecreasing by the complete 256-bit digest.
4. Scan adjacent records. When two full digests agree and their `(u,v)` pairs
   differ, reconstruct both 64-byte messages, recompute both complete hashes,
   verify message inequality and all 256 output bits, and return the pair.
   If no such adjacent pair exists, halt with failure.

There is one batch and no restart. At most two extra target permutations are
used for final verification. Every execution halts within the same worst-case
budget, whether or not it returns a collision.

The radix invariant is standard but included explicitly. At the beginning of a
pass, `P[d]` is the number of preceding records with digit `d`. Scanning the
source in its existing order and incrementing `P[d]` places records of each
digit contiguously while preserving their previous relative order. The first
pass orders low digits; the stable second pass orders high digits and preserves
low-digit order within each equal high digit. Thus it orders all 256 digest bits.
Copying all three array components at the same destination index preserves each
digest's associated message.

After sorting, every equal digest occupies one contiguous interval. If such an
interval contains two different messages, at least one adjacent pair differs;
otherwise equality of every adjacent message would make the whole interval one
repeated message. The scan therefore finds a distinct-message collision whenever
the sample contains one. The final recomputation checks the exact target relation.

## 3. Success probability for every fixed target

Fix the selected deterministic function `H`. The messages `M_1,...,M_n` are iid
uniform on `D`. Let `Q=2^256`, and for each possible output `y` set

    p_y = |{m in D : H(m)=y}| / 2^512.

No uniformity of this probability vector is assumed. If `e_n(p)` is the nth
elementary symmetric polynomial, independence gives

    Pr[all H(M_i) are distinct] = n! e_n(p).

For completeness, uniform `p` maximizes `e_n` on the probability simplex. Take
a maximizer with minimum sum of squared coordinates. If two coordinates `a,b`
differ, hold the other coordinates `r` fixed and average `a,b`. The identity

    e_n(p) = ab e_(n-2)(r) + (a+b)e_(n-1)(r) + e_n(r)

shows that averaging cannot decrease `e_n`, while it strictly decreases the
sum of squares. This contradicts the choice of maximizer. Hence

    Pr[all outputs distinct]
      <= product_(j=0,...,n-1) (1-j/Q)
      <= exp(-n(n-1)/(2Q))
       = exp(-(1/2 - 2^-129))
       < exp(-0.499).

The middle inequality uses `1-x <= exp(-x)`. The last inequality follows from
`1/2-2^-129 > 0.499`.

Let `E` be the event that two sampled input messages are equal. A union bound,
which needs no independence among the pair events, gives

    Pr[E] <= n(n-1)/(2|D|) < 2^-257.

If outputs collide and `E` does not occur, the sorted scan succeeds. Therefore

    Pr[success] > 1 - exp(-0.499) - 2^-257.

This exceeds `0.39` using only rational checks. The first five terms of the
positive Taylor series give

    exp(0.499)
      > sum_(k=0,...,4) (499/1000)^k/k!
       = 39523019494001/24000000000000
       > 125/76.

Thus `exp(-0.499)<76/125=0.608`, while `2^-257<1/500=0.002`.
Consequently the displayed success probability is greater than
`1-0.608-0.002=0.39`. This is algorithmic success probability over fresh RAM
coins, not confidence in a proof or review.

## 4. Charged operation ledger

Under `collision-frontier-v5`, one selected target permutation costs one unit
and every other primitive 256-bit word operation costs `1/1355` units. The
following bounds include all required initialization, randomness, message setup,
all memory traffic, sorting, a failed full scan, and final verification.

Reserving RAM address ranges does not promise zero-filled memory. Every source
record is written during generation before being read; each destination slot
is written exactly once in a pass before becoming a source. Therefore the six
record arrays need no separate clearing. The table P is explicitly cleared
before each pass. All data-memory loads and stores are counted; as usual for
the specified RAM primitive model, executing a primitive instruction is not
recursively charged for fetching an implementation of that instruction.

The permutation interface uses 25 consecutive RAM words, each holding one
64-bit Keccak lane in its low bits, at lane index `x+5y`. It reads and replaces
these 25 lanes as the selected target-permutation primitive, charged once;
its internal operations are not charged a second time. The wrapper overwrites
every lane before each call. Because the IV is zero, the absorbed block can be
written directly without a separate XOR with zero.

Use a fixed finite set of RAM registers for pointers, counters, temporaries,
and constants; all register arithmetic and assignments are counted. No
unbounded register array or implicit memory access is used. The generation
loop terminates by comparing its H-array pointer with the precomputed end,
so it needs no separate index increment. Fixed short loops below are unrolled.

| One generated record, outside the permutation | Ordinary operations |
| --- | ---: |
| Draw `u,v` | 2 |
| Store `u,v` in source arrays | 2 |
| Reset state pointer and copy two extraction temporaries | 3 |
| Extract/write eight message lanes: eight masks/stores/pointer increments plus six shifts | 30 |
| Write lanes 8 through 24, one store and pointer increment each | 34 |
| Pack four output lanes: pointer reset, four loads/masks, three shifts/ORs/pointer increments | 18 |
| Store the packed digest | 1 |
| Advance three record-array pointers | 3 |
| Compare H pointer with end and branch | 2 |
| Total | 95 |

The lane constants are lane 8 = `0x06`, lanes 9 through 15 = zero,
lane 16 = `0x8000000000000000`, and capacity lanes 17 through 24 = zero.
The four output lanes are packed with shifts 0, 64, 128, and 192, matching
Section 1's little-endian digest. Thus the declared 96-operation envelope
includes state initialization, padding, randomness, message retention, output
packing, and control without assuming a whole-hash oracle.

Each radix pass has the following per-entry envelopes. Loop setup is constant
and is included in the fixed reserve below.

| Phase in one pass | Ordinary operations |
| --- | ---: |
| Clear `P` (store, increment, compare, branch) | `4B` |
| Count digits | `12n` |
| Convert counts to exclusive positions | `8B` |
| Stable scatter of all three record words | `24n` |

Since `B=n`, this is at most `48n` operations per pass. The count envelope
includes a digest load, at most two shift/mask operations, computation of the
table address, table load/add/store, and loop control. In detail, count uses
at most 12 operations: digest load (1), digit extraction (at most 2), table
address shift/add (2), load/increment/store (3), pointer advance (1),
compare/branch (2), with one spare operation. For scatter the exact envelope
is 22: three source loads (3), digit extraction (2), table address shift/add
(2), position load (1), destination offset shift (1), three base additions
(3), three record stores (3), position increment/store (2), three source
pointer advances (3), and end comparison/branch (2). Array bases and end
pointers are fixed registers set in the constant setup allowance. The
exclusive-prefix bound
includes loading the count, storing the running sum, addition, and loop control.

The adjacent scan uses at most `32n` ordinary operations even in the worst case
where every digest comparison is equal and both message words must be tested.
This covers all digest/message loads, XOR/OR or comparisons, branches, pointer
increments, and termination checks.

Fixed code, public constants, state scratch, counters, final output, and all
other workspace use less than `2^24` bytes. Initializing them costs at most
`2^24` ordinary operations. Two final one-block wrappers, full comparisons,
serialization, and all fixed residual work keep the combined nonlinear-size
allowance below `2^25` ordinary operations. No table or code contains target-
dependent advice or a precomputed collision.

Writing `H_calls` for selected permutations and `W` for ordinary operations,

    H_calls <= n + 2
    W <= (96 + 2*48 + 32)n + 2^25
      = 224n + 2^25.

Hence total charged time is

    T = H_calls + W/1355
      <= (1579/1355)n + 2 + 2^25/1355.

For `n=2^128`, this is strictly below `(29133/25000)n`: after clearing
denominators, the leading-coefficient margin is

    29133*1355 - 1579*25000 = 215,

and `25000*(2^25+2710) < 215*2^128` covers the fixed terms. Finally,

    29133/25000 < 2^(111/500) = 2^0.222,

which is the exact integer inequality

    29133^500 < 2^111 * 25000^500.

Therefore `T < 2^128.222`. For orientation only, direct high-precision
evaluation of the preceding exact bound is about `2^128.220718319619`.
The claimed 128.222 rounds upward and includes failed outcomes; it is not merely
a birthday exponent, expected time, or cost conditional on success.

## 5. Memory, preprocessing, and advice

Each 256-bit word occupies 32 bytes. The six record arrays use `6n` words and
the count table uses `n` words. Including all fixed storage,

    peak bytes < 7n*32 + 2^24
               = 224n + 2^24
               < 256n
               = 2^136.

Both copies are retained because each stable pass reads one complete set and
writes the other. This bound also includes every sampled message, every digest,
the radix table, state scratch, code, constants, counters, and output. It is an
abstract RAM bound and makes no claim of physical feasibility.

`preprocessing_log2=14` bounds fixed setup: `2^24/1355 < 2^14` target units.
Bulk generation and every table clear/prefix/scatter are part of the main run
and already included in `T`, rather than hidden as preprocessing. The algorithm
evaluates `n+2 < 2^129` message instances. No external data is supplied.

`nonuniform_advice_log2_bytes=0` means at most one byte under the schema's
nonnegative logarithmic field; actual nonuniform advice is zero. The public
algorithm and target constants are charged as fixed code and storage.

## 6. Evidence, limits, and provenance

The evidence is the complete algorithm, universal probability proof, and explicit
RAM ledger above. There is no full-scale execution, observed collision pair,
measured success rate, certificate, or participant experiment. The certificate
manifest is valid and empty. The claim is a generic analytical upper bound and
does not assert a new SHA3 cryptanalytic weakness.

The required `baseline_improved` value `sha3-256-r5-nominal-v2` identifies the
organizer's nominal display reference. Its field name does not itself establish
an improvement over the nominal 128-bit exponent. This package's bound 128.222
is above that nominal reference, though it improves the previously promoted
generic SHA3-256 r5 package at commit
`fe799147566520c8b54c75180b400dec075ed137`.

This revision was constructed independently from that promoted package's exact
target definition and universal birthday argument. It changes the sample count,
sorting algorithm, success bound, and resource ledger. It incorporates no
unpromoted participant candidate, code, proof, experiment, or proprietary data.

`submission_state=ready` means the package is complete for exploratory review.
It does not claim review qualification, an official score, human acceptance, or
promotion. Any such outcome must come from the correctly bound Yukon workflow.
