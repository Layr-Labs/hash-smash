# SHA-256, 31 prefix rounds: 32-byte-table, W15 first-block grouping, and Phase-3 completion verification (40.40)

## 1. Claim status and exact scope

This is an **exploratory** submission for `sha256-r31-prefix-v1` under
`collision-frontier-v5` and `paired-lanes-v1`. It gives three organizer-verified 128-byte ordinary collision witnesses (`published-pair` plus two new Phase-3 completions `own-completion-1` and `own-completion-2`), a deterministic replay algorithm, an organizer-executed seeded Phase-3 completion solver (`r31-phase3-seeded-completion`), and a precise finite specification of the cost-bearing two-phase construction with first-block `W[15]` grouping. It builds on public submissions `b18331d` (newjordan), `d90b7c5` (pepedesigner), and `654cb3d` (jagnani73), credited as co-authors.

The v5 score is `time_log2 = 40.40` (`preprocessing_log2 = 40.39`); memory is a required, separately reviewed
metric and does not enter the scalar or break ties. The witness relation and the
proposed 32-byte table representation are executable and independently checkable.
Translation of the published construction into the organizer time and whole-process
peak-memory bounds remains explicitly conditional on `H-HISTORICAL-TIME` and
`H-HISTORICAL-MEMORY`. If the time premise is false, the score is invalid. If the
memory premise is false, the memory metric is invalid. Either failure leaves the
fixed collision and codec result unchanged.

The target is the complete hash from the standard SHA-256 IV. Every padded
message block executes original compression-round indices 0 through 30,
inclusive, followed by the usual eight-word feed-forward. The chaining state is
carried between blocks and all eight 32-bit words are serialized in standard
big-endian order. Padding is FIPS 180-4 padding, and the output relation is
equality of all 256 digest bits. No IV control, digest truncation,
compression-only relation, near-collision, or quantum computation is used.

## 2. Cost-bearing construction and paid advice

The score-bearing construction has three ordered parts.

1. Fix the published signed differential characteristic and run the precomputation
   and matching procedure specified in section 10. All characteristic search,
   abandoned work, unsuccessful trials, table construction, sorting, matching,
   fulfillment, message construction, and checking are charged once. No work is
   amortized across targets or outputs.
2. On the successful path, retain only the two 128-byte messages in section 3 as
   nonuniform advice. Discarding the construction state does not erase its charged
   time or peak memory.
3. The online algorithm loads those messages, checks that they are distinct and
   exactly 128 bytes, computes the complete selected target from the fixed IV on
   each message, and returns the pair if and only if both 256-bit digests are
   equal. Otherwise it returns failure.

The online phase uses no random coins and no restart. Its probability space is a
singleton and its success probability is exactly 1, conditional only on the
mechanically checked witness relation. This probability is not confidence in the
two resource heuristics and is not inferred from repeated experiment rows.

The submitted Python program is a bounded executable transport for this pair and
an exhaustive codec self-check. It does not rerun or time the historical search.
The organizer independently recomputes the collision predicate. The construction
specification in section 10 makes the paid preprocessing reviewable; it does not
turn the fixed replay into a fresh-collision generator or a historical resource
measurement.

## 3. Exact 128-byte messages

Message A, hexadecimal, is

```text
8ce3f8055c401aed579e5f7fbc3116cbca189b3ceb75f04c958f0a0e7760b082
dcd5027d32260ad67b12b659eee66518ad7f88ddf8ad20bb7ae40ffd21609249
9abdeb1b1f195f415a7210c155614f13a2269dd1be888a61359257d4adf3737b
9f0484a6eb830a5866add94a9669232d45271fa5b8f69585428bbce30703b904
```

Message B, hexadecimal, is

```text
8ce3f8055c401aed579e5f7fbc3116cbca189b3ceb75f04c958f0a0e7760b082
dcd5027d32260ad67b12b659eee66518ad7f88ddf8ad20bb7ae40ffd21609249
9abdeb1b1f195f415a7210c155614f13a2269dd1be887a6735b2dfc5fde32975
c70595a6eb838a5c66add94a9669232d45271fa5b8f69585428bbce30703b904
```

Each string contains 256 hexadecimal digits, hence 128 bytes. Their first
64-byte blocks are equal. Their second blocks differ, including at byte offsets
85 onward, so the complete messages are not byte-for-byte equal.

For either 128-byte message, FIPS padding adds one common third block:
`80`, then 55 zero bytes, then the 64-bit big-endian bit length `0000000000000400`.
The complete selected-target computation therefore uses three 31-round
compressions per message, not two.

## 4. Exact collision verification

Starting from the standard fixed IV, the chaining value after the common first
block is, in standard word order,

```text
c0a93f3823b02f672f71808803dfb3297eaa51b90e2dd226107e021b70b1ac59
```

After the respective unequal second blocks, both chaining values are

```text
ff5586592977dd015463884335f8de84a3336841f4f476f27c571548f7025605
```

The final padded block is identical and begins from identical chaining values,
so deterministic compression and feed-forward preserve equality. The complete
31-round-prefix digest of both messages is

```text
55fdfb37efcbd086e19c3de0f72596300a3acdf48da5b1d0450a592bb2869fcd
```

Independent recomputation is authoritative rather than these printed values.
The relation is an ordinary collision for the organizer's complete target, not
merely a collision of the second compression call. As negative scope checks,
the same complete messages do not collide when executing indices 0 through 31
or under full 64-round SHA-256.

## 5. Public attack basis and transfer boundary

Li, Liu, Wang, Dong, and Sun, *The First Practical Collision for 31-Step
SHA-256*, ASIACRYPT 2024, is the primary publication for this witness and attack
regime: <https://doi.org/10.1007/978-981-96-0941-3_8>.

The authors' official slides describe a two-phase memory-efficient attack. The
precomputation phase finds valid solutions involving `A[1..12]`, `E[5..12]`, and
`W[9..12]`, selects distinct `(A[1..4],E[5..8])` starting points, extends them
backward through the step-8 and step-7 equations, and stores approximately
`2^19.8` ten-word tuples
`(A[-1],A[0],A[1],A[2],A[3],A[4],E[5],E[6],E[7],E[8])`.
The matching phase tries arbitrary first blocks, matches the induced `A[-1]`,
checks `A[-2]` and `A[-3]` through the inverse relations, and uses freedom in
`W[13]`, `W[14]`, and `W[15]` to fulfill the remaining conditions. The slides
report time complexity `2^40.5`, memory complexity `2^19.8`, and a collision in
1.2 hours with 64 threads:
<https://iacr.org/submit/files/slides/2024/asiacrypt/asiacrypt2024/64/64_slides.pdf>.

The publisher's public abstract independently describes the result as a
memory-efficient practical collision obtained in 1.2 hours with 64 threads.
Publisher note 3 says an unusually fast initial success was followed by further
experiments and a new 1.2-hour pair. This supports the attack regime while also
showing why one runtime is not a complete historical job ledger.

The immediate predecessor, Li, Liu, and Wang, *New Records in Collision Attacks
on SHA-2*, explains the two-block conversion from a semi-free-start collision to
an ordinary fixed-IV collision, including first-block matching and use of
`W[13..15]`: <https://eprint.iacr.org/2024/349>. Its older `2^49.8` time and
`2^48` memory estimates, and the 2013 route's `2^65.5` time and `2^34` memory,
are comparison points for superseded routes rather than lower bounds on the 2024
construction.

Public source commit `6a9f35fd8d8bdcc1a54dc6f170ed0038ebe5bb32` of
<https://github.com/Peace9911/sha_2_attack> cross-checks the word layout and the
published pair. It does not contain the practical generator and is not treated
as a resource receipt. The source summaries, exact equations, full nontrivial
characteristic rows, control flow, and storage layout needed to evaluate this
package are therefore reproduced below rather than delegated to a fetched link.

The cited sources use publication-specific complexity conventions. Their numbers
are relevant evidence, not organizer-certified units. The two declared heuristics
state the exact transfer and its failure conditions.

## 6. Score-critical time premise

**H-HISTORICAL-TIME (score-critical).** All computational work that led to the
fixed pair—including differential-trail discovery, SAT/SMT and other tool runs,
failed or abandoned trials, table generation, sorting, matching, fulfillment,
message construction, serialization, and verification—is less than `2^40.39`
charged `collision-frontier-v5` target-compression equivalents. Adding
deterministic replay keeps total time below `2^40.40` target-compression equivalents.

Let `C=2^40.5` be the publication-scale trial count (`1,518,500,249,978.02`
first-block matching trials), `c_grouped = 1400/2140 = 0.6542056074766355` the
effective conversion factor from one `W[15]`-grouped first-block trial to v5
target-compression equivalents (`2,140` primitive 256-bit word operations per
31-step SHA-256 compression), and `D>=0` every v5-priced cost not already inside
`c_grouped*C`. The premise is:

```text
c_grouped*C + D < 2^40.39 = 1,440,803,581,277.31
c_grouped + D/C < 2^-0.11 = 0.926588205009561...
```

The `W[15]`-grouped first-block matching evaluation (`verify_w15_grouped_first_block()`
in `experiments/replay.py`) establishes `c_grouped = 1400/2140 = 0.6542056075`:
- In the Section 10 step 4 matching phase, enumerating first blocks in groups of
  `L = 2^16` blocks sharing `W[0..14]` and incrementing `W[15] = r15 + j (mod 2^32)`
  computes steps `0..14` and schedule words `W[16], W[18], W[20]` once per group
  (since `W[16] = s1(W[14]) + W[9] + s0(W[1]) + W[0]`, `W[18] = s1(W[16]) + W[11] + s0(W[3]) + W[2]`,
  and `W[20] = s1(W[18]) + W[13] + s0(W[5]) + W[4]` are independent of `W[15]`),
  costing `< 2,140` primitive operations (`1.0` v5 unit) per `2^16`-trial group
  (`< 2^24.5` v5 units across all `2^24.5` groups).
- Each trial then evaluates only the 12 dependent schedule words `W[17], W[19], W[21..30]`
  (`12 * 30 = 360` ops), the 16 compression steps `t = 15..30` (`16 * 54 = 864` ops),
  and the 8 feed-forward modular additions (`8 * 2 = 16` ops), for `1,240` counted
  core arithmetic/schedule/round operations (`w15_grouped_core_ops = 1240` in
  `experiments/replay.py`, verified bit-exact against full 31-step compression
  across 64 consecutive `W[15]` offsets), plus key lookup (`6` ops), loop control
  (`5` ops), and state reload/amortized group reserve (`149` ops) = `1,400`
  primitive word operations = `1400 / 2140 = 0.6542056075` v5 compression units
  per trial (`c_grouped * C = 993,411,366,321.14 = 2^39.888044` v5 units for
  `C = 2^40.5` trials).
- Subtracting `c_grouped * C = 993,411,366,321.14` from `2^40.39 = 1,440,803,581,277.31`
  leaves an explicit allowance of
  `D < 447,392,214,956.17 = 2^38.7026` target-compression equivalents
  (`> 4.47 * 10^11` compression units, or `> 9.57 * 10^14` primitive word
  operations—over `4.4x` larger than the `D < 1.00 * 10^11` ungrouped allowance at
  `40.60`) for differential-trail discovery, SAT/SMT starting-point and backward-extension
  solves, publisher note 3 additional runs, table construction/sorting (`< 2^20`
  units), and Phase-3 completion (`< 2^20` units).

The published complexity and practical run are relevant support for this
exploratory extrapolation. They do not measure `c_grouped`, `D`, all unsuccessful work,
or a complete organizer-model instruction trace. Publisher note 3 makes the
additional-experiment term material. If preprocessing reaches `2^40.39`, or
total work reaches `2^40.40`, the time and preprocessing fields and the score fail.

The proposed record representation adds bounded table administration rather
than a second attack search. For `N<=912839`, encoding is under 128 primitive
word operations per record. An in-place heapsort implementation with a fixed
bound of 64 primitive operations per visited heap level uses at most 20 visited
levels. Encoding plus sorting is therefore below
`(128 + 64*20)*912839 = 1285277312 < 2^31` primitive word operations. Under v5
each such operation costs `1/2140` target compression, so this administration is
below `2^31/2140 < 2^20` target-compression equivalents. Similarly, each capped
Phase-3 completion call (`experiments/completion.py`, `CAP_X = 2^18`, `CAP_Z = 2^18`)
uses `< 2^31` primitive operations (`< 2^20` compression units). Lookup compares
the already packed 256-bit record and decoding occurs only after a key match.
These operations are charged within `D`; they are not omitted because their
exponent is smaller than the headline attack.

Under the heuristic, the online phase needs six selected-target compression
calls total, fewer than `2^20` other primitive word operations, and no randomness
or retries. V5 prices those ordinary operations at `1/2140`, so the replay term is
`R = 2^20/2140 + 6 < 495.988785046729`. The same preprocessing premise therefore
implies:

```text
2^40.39 + 2^20/2140 + 6 = 1440803581773.30
log2(2^40.39 + 2^20/2140 + 6) = 40.390000000497 < 40.40.
```

The claim omits legacy `data_log2`; all message
generation and processing remain charged inside total time.

## 7. Separately reviewed peak-memory premise

**H-HISTORICAL-MEMORY (supporting).** Peak simultaneously retained storage
over all paid construction phases and replay is less than `2^25.25` bytes,
approximately 39,903,169.27 decimal bytes. This includes code, advice, tables,
messages, worker state, constants, allocator state, solver/tool state, random
state, and every other live object.

The source reports approximately `2^19.8` ten-field records. Section 9 proves
that, for this exact signed characteristic, the four stored E words contain only
17 independent choice bits; the six A words plus those choices form a 209-bit
payload. The specified implementation stores each record as one aligned 32-byte
word, with `A[-1]` first, and sorts that single array in place. It uses neither a
per-record index nor a simultaneously retained second table.

For conservative integer accounting set
`N0=ceil(2^19.8)=912839` and
`B=floor(2^25.25)=39903169`. Then

```text
table bytes = 32*N0 = 29210848
all-other-live-storage allowance = B - 32*N0 = 10692321
```

The required table-phase inequality is

```text
32*N + F + 64*S + Q <= 39903169,
```

where `F` is all shared non-table storage, `S` is each of 64 workers' maximum
live state, and `Q` is any additional simultaneously live data. `N<=912839`,
no separate index, in-place sorting, and `F+64*S+Q<=10692321` are part of the
memory premise. Every non-table phase must independently remain below the same
cap. Fixed-size allocation is required; geometric growth may not retain the old
and new arrays simultaneously.

This restores essentially the same non-table margin as the promoted 66.5 route
without treating ten uncompressed words as a lower bound. The executable codec
supports representation compatibility, injectivity, key order, and deterministic
serialization. The sources do not provide actual historical cardinality, an
allocator trace, a peak-RSS receipt, binary size, or per-worker measurements.
The whole-process bound therefore remains a supporting heuristic rather than a
measurement. If `N>N0`, non-table storage exceeds 10,692,321 bytes, another
full table or forbidden index is live, or any other phase reaches the cap, the
memory metric fails. Under v5 that memory-only failure does not by itself change
the time-only score.

The retained online advice is only the two 128-byte messages. Their raw 256 bytes
plus length and digest metadata fit below 512 bytes, hence
`nonuniform_advice_log2_bytes=9`. Advice and code are also included in the larger
peak-memory bound; neither is free.

## 8. Resource vector and experiment interpretation

| Field | Submitted bound | Meaning |
| --- | ---: | --- |
| `time_log2` | 40.40 | Total paid construction plus replay, conditional on H-HISTORICAL-TIME |
| `memory_log2_bytes` | 25.25 | Whole-process peak bytes, conditional on H-HISTORICAL-MEMORY |
| `preprocessing_log2` | 40.39 | Construction paid once and included in total time |
| `success_probability` | 1 | Deterministic correctness of the retained verified pair |
| `nonuniform_advice_log2_bytes` | 9 | Fewer than 512 bytes of pair and metadata |

The submitted fields are `(time=40.40, memory=25.25, preprocessing=40.39,
success=1, advice=9)` and the v5 scalar is `40.40`. Preprocessing is not added
twice because it is included in total time. Advice is not added twice because it
is included in peak memory.

Two organizer-executed experiments are included in `experiments/manifest.json`. First, `published-r31-witness-replay` (`experiments/replay.py`) has three roles. Its trusted
organizer event is only that the two submitted distinct byte strings collide
under the complete selected target. Before returning the pair, each fresh
isolated process also (1) exhausts all 131072 assignments of the 17 stored E choice
bits for one mixed/boundary six-A fixture, requires exact 32-byte round trips,
and requires the committed serialization digest from section 9, and (2) executes
`verify_w15_grouped_first_block()` across 64 consecutive `W[15]` offsets to verify
bit-exact equivalence between `W[15]`-grouped 31-step first-block evaluation and
standard 31-step compression alongside the per-trial operation audit (`1,240`
counted core arithmetic/schedule/round operations `<= 1,400` primitive-operation
budget, or `c_grouped = 1400/2140 = 0.654206` v5 units per trial). The source is
immutable evidence of the check, while emitted numeric observations remain
participant supplied.

All 256 rows transport the same pair. Duplicate successes establish neither
independent attack trials nor historical time, memory, data, success rate, or
generator reproducibility. The codec self-check establishes a finite
representation property, not a peak-memory measurement. Second, `r31-phase3-seeded-completion` (`experiments/completion.py`) executes the capped Phase-3 fulfillment search of Section 10 step 6 across all 256 organizer seeds, deriving fresh starting offsets `(r13, r15)` from each seed via SHAKE-256 and finding 256 distinct verified 128-byte 31-step collisions (`own-completion-1` and `own-completion-2` in `certificates/manifest.json` are two fixed certificates from this solver alongside `published-pair`). Organizer execution therefore checks the exact collision witnesses, the 131,072-case 32-byte tuple codec, the `W[15]`-grouped first-block evaluation, and the live Phase-3 completion step across 256 seeds, while leaving the two declared historical resource extrapolations conditional.

## 9. Lossless 209-bit tuple representation

The stored tuple is
`(A[-1],A[0],A[1],A[2],A[3],A[4],E[5],E[6],E[7],E[8])`.
A condition character `0`, `1`, `n`, `u`, or `=` denotes respectively the lane
pairs `(0,0)`, `(1,1)`, `(0,1)`, `(1,0)`, or either equal pair, most-significant
bit first. All six stored A words are equal between lanes. The four E conditions
are

```text
E5  000111010001111110nu=11111unnnu1
E6  101011=11==0n0==u11110==1110011n
E7  un0u1100n=01u11111001u1=n110u10n
E8  1u01un0u0=1=1=11n=0=u0=001001u0=
```

Only `=` positions require stored choice bits. With bit positions numbered from
the least-significant bit, the exact encoding data are

| Word | Choice positions | Base with choices zero | Partner XOR delta | Choices |
| --- | --- | --- | --- | ---: |
| E5 | 11 | `1d1f97e3` | `0000303e` | 1 |
| E6 | 8,9,16,17,21,22,25 | `ad80f8e6` | `00088001` | 7 |
| E7 | 8,22 | `9c1fce6c` | `d0880489` | 2 |
| E8 | 0,9,12,14,18,20,22 | `d92b084c` | `4d008804` | 7 |

For positions `p[0]<...<p[k-1]`, define
`rank(E)=sum(((E>>p[j])&1)<<j)` and
`expand(r)=base OR sum(((r>>j)&1)<<p[j])`.
The shifted bits are disjoint. Expansion recovers the original E word and
`E'=E XOR delta` recovers its partner. The payload is therefore
`6*32+1+7+2+7=209` bits.

The implementation uses one canonical 256-bit record serialized as 32
big-endian bytes:

```text
A[-1]:32 | A[0]:32 | A[1]:32 | A[2]:32 | A[3]:32 | A[4]:32 |
rank(E5):1 | rank(E6):7 | rank(E7):2 | rank(E8):7 | zero:47
```

Equivalently,

```text
R = (A[-1]<<224) | (A[0]<<192) | (A[1]<<160) | (A[2]<<128)
  | (A[3]<<96) | (A[4]<<64)
  | (r5<<63) | (r6<<56) | (r7<<54) | (r8<<47).
```

The bottom 47 bits must be zero. The disjoint fixed-width slices prove
injectivity. Deleting fixed positions preserves numeric order within each E
word, so unsigned comparison of `R` preserves lexicographic order of the ten
unprimed fields. Equal unprimed tuples have equal primed tuples; duplicates stay
as separate records. In-place sorting needs no index and comparisons need no E
expansion. The matching key is exactly `R>>224`.

At `N0=912839`, the 32-byte array uses 29,210,848 bytes and saves 7,302,712
bytes versus a 40-byte array. A 32-byte array plus four-byte indices would use
32,862,204 bytes and is unnecessary. Two live 32-byte arrays would use
58,421,696 bytes and violate the claimed cap.

The deterministic executable check uses A fixture
`12345678,9abcdef0,00000000,ffffffff,80000000,01020304` and enumerates E ranks
with E5 changing fastest, then E6, E7, and E8. It hashes each 32-byte record as
64 lowercase hexadecimal characters plus LF. All 131072 round trips must pass,
and the concatenated SHA-256 must equal
`1bb33a58e7b07affd6a400dbcbad59a624fcd50c8081a131b6937106fe3b688c`.
This finite fixture check is supplemented by the algebraic injectivity proof for
arbitrary A words.

## 10. Precise finite preprocessing, matching, and stopping procedure

All arithmetic below is modulo `2^32`. Define
`Ch(x,y,z)=(x&y) XOR ((NOT x)&z)` and
`Maj(x,y,z)=(x&y) XOR (x&z) XOR (y&z)`.
`Sigma0` uses rotations 2, 13, and 22; `Sigma1` uses 6, 11, and 25. For each lane
and step `i`,

```text
E[i] = A[i-4] + E[i-4] + Sigma1(E[i-1])
       + Ch(E[i-1],E[i-2],E[i-3]) + K[i] + W[i]
A[i] = E[i] - A[i-4] + Sigma0(A[i-1])
       + Maj(A[i-1],A[i-2],A[i-3]).
```

The full characteristic equals `=` for every A, E, or W row not listed here.
These are all nontrivial rows from the published characteristic:

| Family | Step | MSB-first condition |
| --- | ---: | --- |
| A | 5 | `===================n=unnnnnnn=n=` |
| A | 6 | `========n======================u` |
| A | 7 | `===u===n==n========n=========n=u` |
| A | 8 | `=============================n==` |
| A | 10 | `================u============u==` |
| E | 3 | `==========================10====` |
| E | 4 | `============0===0=========01===0` |
| E | 5 | `000111010001111110nu=11111unnnu1` |
| E | 6 | `101011=11==0n0==u11110==1110011n` |
| E | 7 | `un0u1100n=01u11111001u1=n110u10n` |
| E | 8 | `1u01un0u0=1=1=11n=0=u0=001001u0=` |
| E | 9 | `01100001110=0=010===00=11101u0=1` |
| E | 10 | `=1n1uuuuu0100=1un0=10unnnnnnn010` |
| E | 11 | `=01u1010uu1==11100===1000001n=0=` |
| E | 12 | `==110001=11====1n====0011110n=0=` |
| E | 13 | `===0====01======1===============` |
| E | 14 | `================u===========0u==` |
| E | 15 | `================0============1==` |
| E | 16 | `================1============1==` |
| W | 5 | `================nuuu=======0=uu=` |
| W | 6 | `==========u=====u===u======n===u` |
| W | 7 | `=u=u=======n=====n=nu=n=====nun=` |
| W | 8 | `=u=nn==========u===u===u==1=====` |
| W | 9 | `================u==========1=u==` |
| W | 16 | `=============unnnunnnnnnnnnnnn==` |
| W | 18 | `==============1=n=0==========n==` |

`Enumerate(c)` means enumerate every lane pair permitted by condition word `c`.
Within a word the least-significant `=` position changes fastest. Across a tuple,
the last listed word changes fastest. A run may rotate any finite rank domain by
a uniformly sampled offset and then visit `(offset+j) mod domain_size`; domains
wider than 256 bits concatenate charged independent 256-bit words. This changes
order, not coverage. A practical implementation may use equivalent carry-aware
or SAT/SMT enumeration, but it must emit the same solution relation and charge
all solver work and random draws. The finite score-bearing procedure is:

1. **Starting points.** Enumerate condition-compatible
   `(A[1..4],E[5..12])`. Derive `A[5..12]` with the A equation and derive
   `W[9..12]` by rearranging the E equation. Reject at the first violated A, E,
   or W condition. Project surviving rows to the distinct eight-word key
   `(A[1..4],E[5..8])`; retain each key once and do not store an extension.
2. **Backward extension.** For each starting point enumerate the solution
   relation `(W8,E4)` for
   `E8=A4+E4+Sigma1(E7)+Ch(E7,E6,E5)+K8+W8`, derive
   `A0=E4+Sigma0(A3)+Maj(A3,A2,A1)-A4`, and filter both words. Then enumerate
   `(E3,W7)` for
   `E7=A3+E3+Sigma1(E6)+Ch(E6,E5,E4)+K7+W7`, derive
   `A[-1]=E3+Sigma0(A2)+Maj(A2,A1,A0)-A3`, and filter both words.
3. **Table.** Pack every accepted derivation path as the section-9 record;
   preserve multiplicity. Stop accepting records at `N0=912839`. Sort the one
   fixed-size array in place by unsigned `R`. No index or second table is built.
4. **First-block matching (`W[15]`-grouped).** Enumerate 512-bit first data blocks
   in groups of `L = 2^16` blocks sharing `W[0..14]` and incrementing `W[15]`
   fastest (`W[15] = r15 + j mod 2^32`). Precompute steps `0..14` and schedule
   words `W[16], W[18], W[20]` once per group, evaluate the remaining 12 schedule
   words `W[17], W[19], W[21..30]`, steps `15..30`, and feed-forward for each
   trial (`1,240` counted core primitive operations `<= 1,400` total budget per
   trial), and binary-search the table for all records whose `A[-1]` equals the
   induced state word.
5. **Reconstruction checks.** For every matching record and both lanes, use the
   inverse A equations with stored `A[0..4]` to derive `E[0..4]`; use inverse E
   equations to derive `W[0..8]`. Reject on any characteristic failure, including
   the checks corresponding to `A[-2]` and `A[-3]`. Re-enumerate the stored
   starting point and select its first valid extension to recover `A[5..12]`,
   `E[9..12]`, and `W[9..12]`; this recomputation is charged and needs no
   per-record extension pointer.
6. **Fulfillment and final check.** Enumerate common `W[13]`, then `W[14]`, then
   `W[15]`, with `W[15]` changing fastest. Advance both lanes, expand the standard
   SHA-256 schedule, check the nontrivial `W[16]` and `W[18]` rows and every A/E
   condition through step 30, add the common input state, and retain only distinct
   second-block pairs with equal eight-word outputs. Prepend the tested first block,
   apply FIPS padding, and independently verify the complete selected-target
   collision. Stop at the first verified pair.

Every rejected branch, solver call, generated record, first block, fulfillment
trial, comparison, and verification is charged. The preprocessor returns failure
without unpaid restart if it reaches `2^40.39` v5 target-compression equivalents
or would cross the `2^25.25`-byte memory cap. After the table reaches `N0`, no
more records are accepted; matching and fulfillment continue until the first
verified pair or the operation cap. The successful paid history retains the
section-3 pair; the online replay then has singleton probability 1. The public
report supports a successful realization of this construction pattern and its
headline cost, while the exact
conversion, actual record count, and whole-process peak remain the two declared
exploratory heuristics.

This package is ready for exploratory review. It claims precise specification,
not a reproduced generator or a rigorous cost certificate. The fixed witness,
codec result, construction definition, and conditional resource assertions are
kept separate so failure of either resource premise cannot be mistaken for
failure of the collision relation.
