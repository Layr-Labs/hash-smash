# Generic birthday collision search with an explicit word-RAM ledger

## 1. Claim, target, and assumptions

This is the provisional organizer baseline for `sha1-fips180-4-v1`: an ordinary
collision search against all 80 rounds of SHA-1. It claims no cryptanalytic improvement.
The submitted upper bounds remain time `2^92`, peak memory `2^87` bytes, data
`2^80` distinct chosen messages, and one-run success probability at least `0.39`.
There is no target-specific preprocessing or nonuniform advice. The pilot score remains
`92 + 87 = 179`; the tighter intermediate bounds below are not new submitted scores.

The probability claim explicitly assumes that standard SHA-1 on this fixed message
family behaves as independent uniform 160-bit outputs. This random-function heuristic
is not a theorem about concrete SHA-1. All correctness and resource statements below
are conditional only on the stated machine model, not on successful sampling.

Use the organizer's abstract 128-bit word RAM with a flat `2^128`-word address space.
One complete one-block SHA-1 evaluation costs one time unit; every other word-RAM
primitive also costs one unit. This intentionally overcharges ordinary operations.
There is no parallelism, network communication, external dataset, or special hardware
assumption beyond this abstract machine. These buffers cannot fit on present hardware.

## 2. Representation and instruction semantics

Let `n = 2^80`. Message `m(i)`, for `0 <= i < n`, is the 22-byte ASCII string
`HashSmash birthday v1:` followed by the 12-byte big-endian encoding of `i`.
It has exactly 34 bytes (272 bits). Standard SHA-1 padding adds `0x80`, 21 zero bytes,
and the 8-byte big-endian length 272, producing exactly one 64-byte block. SHA-1 uses
the standard IV, all 80 rounds, feed-forward, and the full 160-bit output, as specified
in FIPS 180-4 sections 5.1.1 and 6.1. There is no chosen-IV or reduced-round substitution.

Every record is two 16-byte words: word 0 contains digest bytes 0..15, and word 1
contains digest bytes 16..19 in its most significant 32 bits followed by the 96-bit
nonce. Words and digest bytes are interpreted big-endian. No pointers or per-record
metadata are stored. Two disjoint arrays `A` and `B` each reserve `2n` words.

The literal aliases in the program are:

- `N = n`.
- `K0 = int_be(ASCII("HashSmash birthday v1:")[0:16])`.
- `K1 = int_be(ASCII("HashSmash birthday v1:")[16:22]) << 80`.
- `MASK96 = 2^96 - 1`.

They are fixed public literal operands (substituted into instructions), not results of
runtime parsing or preprocessing. The fixed public program is resident initially, as
usual for a word-RAM algorithm; its storage, constants, and machine state are charged
in section 6. There is no separate runtime compiler, loader, or target-dependent table.
Only `A` and `B` are dynamically allocated; every initialization they need appears below.

Each non-label line below is exactly one charged instruction:

- `SET d x` copies a word. `ADD/SUB/SHL/SHR/AND/OR d x y` performs the indicated
  unsigned 128-bit operation, storing its result in `d`; shifts are logical.
- `LT/EQ d x y` sets `d` to 0 or 1. `BZ x label` branches if `x == 0`.
  `JMP label` and `HALT` each cost one unit. Comparison and branch are separate.
- `LD d a` and `ST a x` read/write one 128-bit word at word address `a`.
  Address arithmetic is explicit; a register result write is part of its instruction.
- `ALLOC d size` reserves a contiguous, uninitialized interval of `size` words,
  returns its base address in `d`, and uses the model's one-word descriptor with
  no hidden allocator arena. The two descriptors are also explicitly stored below.
- `SHA hi lo base` is the model's complete one-block SHA-1 evaluation: hash the
  first 34 bytes of the three words beginning at `base`; return digest bytes 0..15
  as `hi = int_be(digest[0:16])` and bytes 16..19 as
  `lo = int_be(digest[16:20])`. The entire 128-bit `lo` result is overwritten:
  its upper 96 bits are zero, i.e. the 32-bit suffix is canonically zero-extended.
  The same rule applies to the result registers `l0` and `l1` during rehashing.
  Padding and the SHA-1 computation are included in this one hash unit, not an
  extra SHA compression.
  Construction of those three words and subsequent result storage are separate.
  The last 14 bytes of the three-word message slot are zero and are not hashed.

All arithmetic operands, addresses, counters, and shifts fit the machine. In particular,
`i < 2^80`, counts/positions are at most `n`, `2n = 2^81`, digest halves fit their
specified fields, and the largest allocated exclusive address is `4096 + 4n < 2^128`.
The byte-selection shifts range from 0 to 120. Nonces remain below `2^96`.
No overflow affects a meaningful arithmetic result.

## 3. Complete instruction schedule

The program has 149 instructions. Labels are free control-flow names, not operations.
Fixed memory addresses are allocated in section 6. The initial allocation frontier is
word 4096; `ALLOC` reserves `A` and then `B` above that frontier.

The byte-position loop runs `j = 19, 18, ..., 0`: least significant digest byte first.
For byte `j`, `q = j >> 4` selects record word 0 or 1 and
`s = 8 * (15 - (j & 15))` selects that byte. The lower 96 nonce bits of word 1
are never sorting keys.

```text
start:
SHL size N 1
ALLOC A size
ALLOC B size
ST 672 A
ST 673 B
fill_init:
SET i 0
SET p A
fill_test:
LT c i N
BZ c sort_init
fill_body:
ST 0 K0
SHR t i 16
OR t K1 t
ST 1 t
AND t i 65535
SHL t t 112
ST 2 t
SHA hi lo 0
SHL t lo 96
OR t t i
ST p hi
ADD a p 1
ST a t
ADD p p 2
ADD i i 1
JMP fill_test
sort_init:
SET src A
SET dst B
SET j 20
pass_test:
LT c 0 j
BZ c scan_init
pass_setup:
SUB j j 1
SHR q j 4
AND r j 15
SUB s 15 r
SHL s s 3
zero_init:
SET k 0
zero_test:
LT c k 256
BZ c hist_init
zero_body:
ADD a 16 k
ST a 0
ADD k k 1
JMP zero_test
hist_init:
SET p src
SET i 0
hist_test:
LT c i N
BZ c prefix_init
hist_body:
ADD a p q
LD w a
SHR b w s
AND b b 255
ADD a 16 b
LD t a
ADD t t 1
ST a t
ADD p p 2
ADD i i 1
JMP hist_test
prefix_init:
SET k 0
SET total 0
prefix_test:
LT c k 256
BZ c scatter_init
prefix_body:
ADD a 16 k
LD t a
ADD a 272 k
ST a total
ADD total total t
ADD k k 1
JMP prefix_test
scatter_init:
SET p src
SET i 0
scatter_test:
LT c i N
BZ c pass_end
scatter_body:
ADD a p q
LD w a
SHR b w s
AND b b 255
ADD a 272 b
LD pos a
ADD t pos 1
ST a t
SHL a pos 1
ADD a dst a
LD x p
ADD nextp p 1
LD y nextp
ST a x
ADD a a 1
ST a y
ADD p p 2
ADD i i 1
JMP scatter_test
pass_end:
SET t src
SET src dst
SET dst t
JMP pass_test
scan_init:
SET i 1
ADD p src 2
scan_test:
LT c i N
BZ c fail
scan_body:
SUB a p 2
LD x0 a
ADD a a 1
LD x1 a
LD y0 p
ADD a p 1
LD y1 a
EQ c x0 y0
BZ c scan_next
SHR u x1 96
SHR v y1 96
EQ c u v
BZ c scan_next
scan_hit:
AND nonce0 x1 MASK96
AND nonce1 y1 MASK96
JMP verify
scan_next:
ADD p p 2
ADD i i 1
JMP scan_test
verify:
EQ c nonce0 nonce1
BZ c verify_build
JMP fail
verify_build:
ST 528 K0
SHR t nonce0 16
OR t K1 t
ST 529 t
AND t nonce0 65535
SHL t t 112
ST 530 t
ST 531 K0
SHR t nonce1 16
OR t K1 t
ST 532 t
AND t nonce1 65535
SHL t t 112
ST 533 t
SHA h0 l0 528
SHA h1 l1 531
EQ u h0 h1
EQ v l0 l1
AND c u v
BZ c fail
success:
ST 534 1
ST 535 34
ST 536 34
HALT
fail:
ST 534 0
ST 535 0
ST 536 0
HALT
```

On success, words 528..530 and 531..533 contain the two messages (first 34 bytes
of each slot), word 534 is 1, and words 535 and 536 contain their byte lengths, 34.
On failure, word 534 and both lengths are zero; the message slots must not be read.
These fixed output slots are the return interface: no uncharged serialization, stdout,
disk write, or external communication is part of the algorithm.

## 4. Correctness and probability

Generation writes each of the `n` distinct nonces once and stores its complete digest.
The 34-byte encoding is injective in the nonce. Histogram counters `C[b]` (base 16)
start at zero. At the end of histogramming, `C[b]` is exactly the number of source
records whose current digest byte is `b`.

The prefix loop writes `P[b] = sum_{a < b} C[a]` (base 272). Each scatter consumes
source records in their existing order and increments `P[b]` after placing one record.
Thus every destination index 0..n-1 is written exactly once, bucket intervals are
disjoint, and relative order within a bucket is preserved. Both record words, including
the nonce, move together. Inductively, after processing byte `j`, records are sorted
by digest suffix `j..19`. After byte 0, they are sorted by all 20 digest bytes.
The source/destination swap after every pass always leaves `src` pointing at the
completed output. In particular, the final 20th pass returns to `A`.

The adjacent scan compares word 0 and the upper 32 bits of word 1, ignoring nonces.
Equal complete digests are contiguous, so it finds a pair if and only if one exists.
Their nonces are distinct because scatter is a permutation of the original records.
The program nevertheless checks distinctness and recomputes standard SHA-1 of both
reconstructed messages before returning success. In this deterministic computation
those rehashes equal their stored digests; a successful return is a genuine ordinary
SHA-1 collision, not merely a match of a truncated digest. If there is no sampled
collision, the program terminates with failure. It performs no retries.

Under the declared random-function heuristic, with `R = 2^160`, the failure
probability on these distinct messages is
`product_{i=0}^{n-1} (1 - i/R) <= exp(-n(n-1)/(2R))`.
For `n = 2^80`, let `x = n(n-1)/(2R) = 1/2 - 2^-81 > 499/1000`.
The positive exponential series gives the exact rational comparison

```text
exp(x) > 1 + 499/1000 + (499/1000)^2/2 + (499/1000)^3/6
       = 9865254499/6000000000 > 100/61.
```

Therefore `exp(-x) < 61/100` and success probability is strictly greater than
`39/100 = 0.39`. This finite-n calculation, not a limiting approximation, meets the
threshold in one run. Its approximate value is near `1 - exp(-1/2) = 0.393469`;
that approximation is not used to prove the threshold. No claim of randomness of
actual SHA-1 is established by this calculation or by a model review.

## 5. Complete time ledger

The following counts refer to the labeled program above. Loop tests include the final
failed test. Allocation has no element-initialization cost; all reads of dynamic
storage follow explicit writes. The public code/literals are already resident, not
computed by an omitted setup stage.

| Portion | Charged operations |
| --- | ---: |
| Allocation and descriptor stores (`start`) | 5 |
| Fill initialization | 2 |
| Fill tests | `2(n+1)` |
| Fill bodies, including one hash each | `16n` |
| Sort initialization and pass tests | `3 + 2(20+1) = 45` |
| Byte-selection setup, per pass | 5 |
| Zero counters, per pass | `1 + 2(256+1) + 4*256 = 1539` |
| Histogram, per pass | `2 + 2(n+1) + 11n = 13n+4` |
| Prefix positions, per pass | `2 + 2(256+1) + 7*256 = 2308` |
| Scatter, per pass | `2 + 2(n+1) + 19n = 21n+4` |
| Swap and jump, per pass | 4 |
| Adjacent scan including setup/termination | at most `18(n-1)+4` |
| Final verification and return, or failure return | at most 32 |

For the scan, each of at most `n-1` iterations has 2 test instructions, at most
13 comparison/body instructions, and either 3 advance instructions or 3 hit instructions.
Its initialization uses 2 instructions, with at most 2 additional terminating-test
instructions. The short branch on unequal word 0 only reduces the count.

After a hit, the normal distinctness check uses 2 instructions, construction of the two
messages uses 14, their two full hashes use 2, comparison/branch uses 4, and output
metadata plus halt uses 4: 26 total. The invalid-nonce and unequal-rehash failure paths
are no longer. A no-hit failure return uses 4. The separate allowance 32 bounds every
case, including the final two hashes and the return itself.

Thus fill costs `18n+4`, and all 20 sorting passes cost exactly

```text
45 + 20 * (5 + 1539 + (13n+4) + 2308 + (21n+4) + 4)
= 680n + 77325.
```

Total time is at most

```text
5 + (18n+4) + (680n+77325) + (18(n-1)+4) + 32
= 716n + 77352
< 2^90 + 2^17
< 2^91
< 2^92, for n = 2^80.
```

The last bound is deliberately looser than this schedule requires. There is no
unaccounted numerical search, certificate checking, preprocessing, repetition, or
amortized setup. Hash calls number exactly `n` without a hit and `n+2` with a hit;
those calls are already included in the ledger, not added again.

## 6. Peak memory and remaining resources

Reserve exactly 4096 fixed 16-byte words, including all unused padding, plus the two
dynamic arrays. Inclusive fixed word-address ranges are:

| Word addresses | Purpose | Words |
| --- | --- | ---: |
| 0..2 | Current 34-byte message in a 48-byte slot | 3 |
| 3..15 | Reserved alignment/padding | 13 |
| 16..271 | 256 histogram counters | 256 |
| 272..527 | 256 prefix/scatter positions | 256 |
| 528..543 | Two output slots, success flag, two lengths, spare words | 16 |
| 544..671 | SHA-1 working storage, reused for every hash | 128 |
| 672..673 | Array descriptors | 2 |
| 674..737 | Registers and machine control state | 64 |
| 738..769 | Public constant pool reservation | 32 |
| 770..1023 | Reserved padding | 254 |
| 1024..2047 | Fixed code: 256 instruction slots, four words each | 1024 |
| 2048..4095 | Reserved padding | 2048 |
| **Total fixed** | **Every reserved word is charged** | **4096** |

The SHA-1 reservation is sufficient even with deliberately wasteful 128-bit slots for
each 32-bit value: 80 message-schedule words, 5 chaining words, 5 working words,
4 round constants, 4 words for the padded 64-byte block, 16 temporaries, and 14 spare
words sum to 128. Hashes are sequential and share this workspace. Digest outputs reside
in the charged registers or record buffers; there is no live digest list elsewhere.

The program uses fewer than 48 named word registers. The 64-word state reservation also
covers the program counter, allocation frontier, instruction/opcode and three operand
latches, and control flags; no stack or recursion is used. Each of the 149 instructions
fits one opcode plus at most three 128-bit operands, including literal or label operands.
The reservation for 256 such instructions is larger than the complete program.
The constant pool is additionally charged even though literal operands can be encoded
in those code slots. The output area uses six words for messages and three for metadata;
all seven spare words are charged as well.

`A` occupies words `[4096, 4096+2n)`; `B` occupies
`[4096+2n, 4096+4n)`. Abstract allocation adds no hidden metadata beyond the two
descriptors and allocation frontier already counted. Neither source nor destination
has padding between records. Counting both arrays and all fixed state simultaneously,

```text
peak bytes <= (2n + 2n + 4096) * 16
           = 64n + 65536
           = 2^86 + 2^16
           < 2^87.
```

Data is measured as the number of **distinct chosen messages**, namely `n = 2^80`,
not bytes or hash invocations. Their total generated length is `34n` bytes, but these
messages are generated sequentially and not retained as a message array. Final
verification reuses two already-chosen messages, so it adds no distinct data. The
success output consists of two 34-byte messages plus the already-counted status/length
metadata. No external samples or oracle transcript are required.

There is no target-specific preprocessing, reusable table, nonuniform advice, or
amortization across attacks. The zero log2 fields in the manifest are conservative
unit upper bounds for these absent resources, not logarithms of literal zero.
The fully specified public program and domain string are fixed uniform algorithm
description/state, not target-dependent advice; their live storage is nevertheless
included above.

## 7. Certificates and limitations

No concrete SHA-1 collision witness or executable numerical certificate accompanies
this generic baseline: executing `2^80` hashes and storing these buffers is infeasible.
The empty certificate manifest is intentional. If the attack itself succeeds, its
two rehashed output messages are the collision witness; that is different from claiming
that this submission has already run it or supplied such a witness.

All accounting and the finite-n probability inequality are explicit above and require
no participant program execution to review. Small-scale organizer tests can check the
instruction counts and sorting implementation but cannot certify behavior at this
physical scale, prove the random-function heuristic, or exhibit a full-size sampled
collision. A favorable AI verdict remains `ai_qualified`, not mathematical proof or
human acceptance. This is an integration baseline, not an improving submission.
