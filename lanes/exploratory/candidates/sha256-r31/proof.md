# SHA-256 through step 30: published collision with a charged construction

## 1. Result and scope

This package gives an ordinary collision for `sha256-r31-prefix-v1` and a
conditional upper bound of `time_log2 = 41.500001` under
`collision-frontier-v5`. It uses the two-block collision published by Yingxin
Li, Fukang Liu, Gaoli Wang, Xiaoyang Dong, and Siwei Sun at ASIACRYPT 2024.
The public construction is charged once; the published messages are not treated
as free advice.

The claim has two different kinds of support:

1. A `hash-collision-witness-v2` certificate establishes the exact complete-hash
   relation without a heuristic.
2. The historical time and peak-memory translations are declared premises
   `H-HISTORICAL-TIME` and `H-HISTORICAL-MEMORY`. The sources report the attack,
   its complexity, its table size, and an actual run, but not a v5 instruction
   trace or a whole-process memory trace.

The target starts from the standard SHA-256 IV, executes original round indices
0 through 30 on every padded block, performs the standard eight-word
feed-forward after every compression, carries the state between blocks, and
returns all eight words in standard big-endian order. The messages use FIPS
padding. No chosen IV, free start, output truncation, near-collision, or
full-SHA-256 claim is involved.

## 2. Published witness

The first 128-byte message is

```text
8ce3f8055c401aed579e5f7fbc3116cbca189b3ceb75f04c958f0a0e7760b082
dcd5027d32260ad67b12b659eee66518ad7f88ddf8ad20bb7ae40ffd21609249
9abdeb1b1f195f415a7210c155614f13a2269dd1be888a61359257d4adf3737b
9f0484a6eb830a5866add94a9669232d45271fa5b8f69585428bbce30703b904
```

The second 128-byte message is

```text
8ce3f8055c401aed579e5f7fbc3116cbca189b3ceb75f04c958f0a0e7760b082
dcd5027d32260ad67b12b659eee66518ad7f88ddf8ad20bb7ae40ffd21609249
9abdeb1b1f195f415a7210c155614f13a2269dd1be887a6735b2dfc5fde32975
c70595a6eb838a5c66add94a9669232d45271fa5b8f69585428bbce30703b904
```

The first 64-byte blocks are identical. The second blocks are different, so
the complete messages are distinct. A 128-byte message receives a third,
common block consisting of byte `80`, 55 zero bytes, and the big-endian
64-bit length `0000000000000400`. Each complete evaluation therefore makes
three selected-target compression calls.

Independent evaluation with the organizer implementation gives the common
state after the first data block

```text
c0a93f3823b02f672f71808803dfb3297eaa51b90e2dd226107e021b70b1ac59
```

and the common state after the two different second blocks

```text
ff5586592977dd015463884335f8de84a3336841f4f476f27c571548f7025605
```

After the padding block, both complete digests are

```text
55fdfb37efcbd086e19c3de0f72596300a3acdf48da5b1d0450a592bb2869fcd
```

The certificate files contain exactly these two byte strings. The organizer
checker recomputes both complete hashes and checks distinctness. The pair does
not collide when round index 31 is also executed, and it does not collide under
the full 64-round SHA-256; those negative checks only delimit this claim.

## 3. Primary-source construction evidence

The primary sources are the authors' ASIACRYPT 2024 slides and the publisher's
page for *The First Practical Collision for 31-Step SHA-256*:

- <https://iacr.org/submit/files/slides/2024/asiacrypt/asiacrypt2024/64/64_slides.pdf>
- <https://doi.org/10.1007/978-981-96-0941-3_8>

Slides 9 through 14 describe a two-phase construction. Its preprocessing
finds solutions satisfying the middle differential conditions, extends them
backward, and stores approximately `2^19.8` tuples containing
`(A[-1], A[0], A[1], A[2], A[3], A[4], E[5], E[6], E[7], E[8])`. Its matching
phase tries arbitrary common first blocks under 31-step SHA-256, matches the
resulting chaining state on `A[-1]`, checks `A[-2]` and `A[-3]`, and uses the
freedom in `W[13]`, `W[14]`, and `W[15]` to fulfill the remaining conditions.
The final output is verified as a two-block collision.

Slide 14 reports all three of the quantitative facts used here: time complexity
`2^40.5`, memory complexity `2^19.8`, and a practical collision found in 1.2
hours with 64 threads. Slide 15 prints the two-block pair above and the common
state after its second data block. The publisher abstract independently says
that the memory-efficient attack produced a colliding pair in 1.2 hours with 64
threads and negligible memory.

The publisher page also exposes three qualifications from the paper's notes.
The analysis first omits some factors affecting overall complexity; the paper's
per-unit auxiliary term is described as usually very small; and an initial
seconds-long success was considered atypical, after which the authors ran more
experiments and obtained another pair in 1.2 hours. These statements are why
the submitted cost is not the bare `2^40.5` headline.

The authors' public verification repository, commit
`6a9f35fd8d8bdcc1a54dc6f170ed0038ebe5bb32`, prints the same block words:
<https://github.com/Peace9911/sha_2_attack/blob/6a9f35fd8d8bdcc1a54dc6f170ed0038ebe5bb32/verify_result/sha256_31_Collision.txt>.
It corroborates the transcription but is not used as a cost receipt or as an
end-to-end generator.

The source facts establish that this is a practical standard-IV two-block
collision construction for the selected 31-step compression. They do not
establish an exact translation from the authors' complexity convention to the
organizer's 256-bit word RAM, the number and cost of every additional run, or
the cost of the research that selected the characteristic. Those transfers
are confined to the two premises below.

## 4. Charged algorithm and probability space

The abstract algorithm consists of paid construction followed by deterministic
replay.

1. Execute the published preprocessing, first-block matching, condition
   checking, message-word fulfillment, and final verification that produced
   the retained pair. Charge differential and message construction, auxiliary
   solver work, unsuccessful branches and trials, table creation and lookup,
   randomness, serialization, and verification. This one-time work is `P` in
   section 5. It is neither amortized nor divided by the number of threads.
2. Retain the two 128-byte messages as nonuniform advice. Load them, check
   their lengths and inequality, evaluate the complete selected target on both,
   compare all 256 output bits, and return the pair only on equality.

The replay uses no coins and has a singleton probability space. Because the
certificate verifies its retained advice, it returns a collision with
probability 1. This success statement is about replay after fully charged
construction; it is not a probability estimate for a fresh capped execution of
the historical search. Repeated replay is not used as statistical evidence.

## 5. Historical time premise and v5 arithmetic

**H-HISTORICAL-TIME.** All one-time computation needed to construct the exact
retained witness is less than `2^41.5` target-compression equivalents under
`collision-frontier-v5`. It includes every item listed in step 1 above and all
work needed to make the retained pair available to replay.

Let `Q = 2^40.5` denote the authors' reported complexity, let `c` translate one
unit of that accounting into v5 target-compression equivalents, and let `D`
contain every included cost not already represented by `c Q`. The premise is

```text
P = c Q + D < 2 Q = 2^41.5,
or equivalently c + D/Q < 2.
```

The construction description supports treating its dominant first-block work
as selected 31-step compressions. The reported run corroborates practicality,
and the publisher note describes the omitted per-unit term as small. The
factor-two envelope leaves one full headline-sized allowance for unit
translation, preprocessing, administration, failures, auxiliary tools, and the
additional work disclosed by the publisher.

This is still an extrapolation. No public source gives `c`, `D`, a raw attempt
ledger, or a v5 trace, and the number and aggregate cost of the additional
experiments are not reported. If `c + D/Q` reaches 2, the time and
preprocessing claims fail. The source therefore supports the premise only at
the exploratory level.

The tighter historical premise `P < 2^40.75` would require
`c + D/Q < 2^0.25`, approximately 1.1893. The primary sources do not bound the
omitted terms or conversion that tightly. This package consequently does not
use the `40.750001` accounting route.

The opaque historical quantity is not divided by 2140. Under v5, that divisor
applies only to separately counted ordinary word operations. The replay makes
six selected-target calls. A direct fixed-size wrapper has the following core
operation budget; the compression internals are not counted again.

| Replay wrapper work | Ordinary operations |
| --- | ---: |
| Advice and length loads | 10 |
| Length checks and branches | 4 |
| Four-word distinctness check | 9 |
| Padding construction and checks | 16 |
| State/block transfers and control around six calls | 30 |
| Full-digest comparisons and branches | 4 |
| Output serialization | 11 |
| Indexing, setup, and return slack | 44 |
| Total | at most 128 |

The ledger nevertheless allows fewer than `2^20` ordinary operations for the
same fixed 256-byte input, covering instruction fetch, representation changes,
and any additional fixed setup. Hence

```text
T < 2^41.5 + 6 + 2^20/2140.
```

The additive replay is less than 497 target units. Raising the exponent from
41.5 to 41.500001 adds more than 2,155,000 target units, so

```text
T < 2^41.500001.
```

This proves the submitted scalar conditional on H-HISTORICAL-TIME. The whole
historical construction is `preprocessing_log2 = 41.5` and is already included
once in total time.

## 6. Peak memory and advice

**H-HISTORICAL-MEMORY.** Peak simultaneously retained storage over all
construction and replay phases is less than `2^40` bytes, including tables,
indices, code, constants, messages, worker and allocator state, solver state,
randomness retained in memory, and nonuniform advice.

The slides report approximately `2^19.8` stored ten-word tuples. At 40 raw
bytes per tuple their payload occupies approximately

```text
40 * 2^19.8 = 2^25.121928... bytes.
```

The submitted bound is therefore more than `2^14.8` times the raw table
payload. The publisher describes the practical run's memory as negligible,
and the run used 64 threads. Those primary-source observations make the much
looser `2^40` whole-process ceiling plausible, but they are not a peak-memory
measurement. If any construction phase reaches one tebibyte, the required
memory claim fails; the time scalar is unaffected because v5 does not score
memory.

The two retained messages occupy 256 bytes. Allowing fewer than another 256
bytes for their lengths and the expected digest gives an advice bound below 512
bytes, reported as `nonuniform_advice_log2_bytes = 9`. The advice's historical
construction is already charged in `P`; the small stored representation does
not make the collision free.

## 7. Evidence boundaries and resource vector

The certificate proves only distinct-message equality for the exact complete
target. It does not prove historical work, peak memory, novelty, or a fresh
generator's success distribution. The primary sources support the two-phase
method, pair, headline complexity, table cardinality, and reported execution.
H-HISTORICAL-TIME transfers those observations to an all-work v5 bound;
H-HISTORICAL-MEMORY transfers them to a deliberately broad byte ceiling.

The submitted resource vector is:

| Field | Bound | Basis |
| --- | ---: | --- |
| `time_log2` | 41.500001 | `P` plus replay, conditional on H-HISTORICAL-TIME |
| `memory_log2_bytes` | 40 | Whole-process peak, conditional on H-HISTORICAL-MEMORY |
| `preprocessing_log2` | 41.5 | The paid historical construction `P`, included in total time |
| `success_probability` | 1 | Deterministic replay of the verified pair |
| `nonuniform_advice_log2_bytes` | 9 | Pair plus fixed metadata below 512 bytes |

No experiment manifest is declared. There is no inference from CPU time to
RAM operations, no division of total work by 64 threads, no success
amplification, and no claim that the same bounds qualify a rigorous lane.
