# A charged replay of the published SHA-256 31-round collision

## 1. Claim and scope

This package claims `time_log2 = 41.500001` for an ordinary collision on
`sha256-r31-prefix-v1`. The offline construction is described below as a
finite two-phase search, and its full cost is charged once. The online output
algorithm then replays the two fixed messages in section 2 and checks the
complete selected target. It is not a fresh-collision service.

The target uses the standard SHA-256 IV, rounds 0 through 30 on every padded
block, the standard feed-forward, FIPS padding, and all 256 digest bits. The
published messages are distinct and 128 bytes each. No free-start state,
chosen IV, truncation, near-collision, or full-SHA-256 result is claimed.

There are two uncertain resource premises, stated separately in section 7:
`H-HISTORICAL-TIME` and `H-HISTORICAL-MEMORY`. The certificate establishes the
retained pair's collision relation. It does not measure the historical search.

## 2. Fixed witness

Message A is

```text
8ce3f8055c401aed579e5f7fbc3116cbca189b3ceb75f04c958f0a0e7760b082
dcd5027d32260ad67b12b659eee66518ad7f88ddf8ad20bb7ae40ffd21609249
9abdeb1b1f195f415a7210c155614f13a2269dd1be888a61359257d4adf3737b
9f0484a6eb830a5866add94a9669232d45271fa5b8f69585428bbce30703b904
```

Message B is

```text
8ce3f8055c401aed579e5f7fbc3116cbca189b3ceb75f04c958f0a0e7760b082
dcd5027d32260ad67b12b659eee66518ad7f88ddf8ad20bb7ae40ffd21609249
9abdeb1b1f195f415a7210c155614f13a2269dd1be887a6735b2dfc5fde32975
c70595a6eb838a5c66add94a9669232d45271fa5b8f69585428bbce30703b904
```

The first 64-byte blocks agree; the second blocks differ. A 128-byte message
has three padded blocks: the two data blocks and a common block containing
`80`, 55 zero bytes, and the 64-bit big-endian length `0000000000000400`.
The independently recomputed chaining state after the common first block is

```text
c0a93f3823b02f672f71808803dfb3297eaa51b90e2dd226107e021b70b1ac59
```

After the two different second blocks both states are

```text
ff5586592977dd015463884335f8de84a3336841f4f476f27c571548f7025605
```

The complete padded 31-round digests are both
`55fdfb37efcbd086e19c3de0f72596300a3acdf48da5b1d0450a592bb2869fcd`.
The certificate manifest points to the exact binary messages; the organizer
checker recomputes the complete target relation.

## 3. SHA-256 equations and characteristic notation

All state and message words are 32-bit unsigned values. Arithmetic in these
equations is modulo `2^32`:

```text
Ch(x,y,z)  = (x AND y) XOR ((NOT x) AND z)
Maj(x,y,z) = (x AND y) XOR (x AND z) XOR (y AND z)
S0(x)      = ROTR(x,2) XOR ROTR(x,13) XOR ROTR(x,22)
S1(x)      = ROTR(x,6) XOR ROTR(x,11) XOR ROTR(x,25)

E[i] = A[i-4] + E[i-4] + S1(E[i-1])
       + Ch(E[i-1],E[i-2],E[i-3]) + K[i] + W[i]
A[i] = E[i] - A[i-4] + S0(A[i-1])
       + Maj(A[i-1],A[i-2],A[i-3])
```

For `i >= 16`, the message schedule is

```text
W[i] = sigma1(W[i-2]) + W[i-7] + sigma0(W[i-15]) + W[i-16]
sigma0(x) = ROTR(x,7) XOR ROTR(x,18) XOR (x >> 3)
sigma1(x) = ROTR(x,17) XOR ROTR(x,19) XOR (x >> 10)
```

The table uses a pair of bits `(left,right)` for the two second-block lanes.
Rows are printed most-significant bit first. `=` means equal and free; `0`
means `(0,0)`; `1` means `(1,1)`; `n` means `(1,0)`; and `u` means
`(0,1)`. For a word condition, each `=` position can therefore be either
`(0,0)` or `(1,1)`. This defines every bit condition used below; all
unlisted A, E, and W words have the equal condition.

The nontrivial rows printed on slide 14 are reproduced here in full:

| Word | Index | 32-bit condition |
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

Every row not listed has the equal condition `=` at all 32 positions. The
slide's table plus equations above defines every condition used by the search;
no unspecified “published differential characteristic” is needed to interpret
the procedure.

## 4. Solver and source boundary

Li, Liu, Wang, Dong, and Sun report the collision in *The First Practical
Collision for 31-Step SHA-256*, ASIACRYPT 2024, LNCS 15490, pp. 237–266
([paper](https://doi.org/10.1007/978-981-96-0941-3_8)). The authors' slides
give the construction sequence on slides 10–14 and the pair on slide 15
([slides PDF](https://iacr.org/submit/files/slides/2024/asiacrypt/asiacrypt2024/64/64_slides.pdf)).

The public author repository at commit
[`6a9f35fd8d8bdcc1a54dc6f170ed0038ebe5bb32`](https://github.com/Peace9911/sha_2_attack/tree/6a9f35fd8d8bdcc1a54dc6f170ed0038ebe5bb32)
contains differential-search code in addition to the result verifier. The
`find_dc_model_31_256.py` setup uses `start_step=5`, `end_step=19`, a 31-word
message bound, initial weight 60, and message-difference indices
`[5,6,7,8,9,16,18]`. Its operation flags are `op0=op1=op3=op4=[1]*31`,
`op2=[0]*15+[1]*16`, `op5=[0]*11+[1]*20`, and `op6=op7=op8=[0]*31`.
Its model expands SHA additions, XOR, IF, MAJ, and the
schedule as bit-vector constraints using `unit_function_256.py` and
`constrain_condition.py`. It tries objective weights 60 down to 0, writes the
STP query, invokes `stp ... --cryptominisat --threads 26`, treats the exact
response `Valid.\n` as unsatisfiable, saves other successful responses, and
stops at the first unsatisfiable objective. A nonzero solver exit aborts via
`check_output`. The source locations are
[`find_dc_model_31_256.py`](https://github.com/Peace9911/sha_2_attack/blob/6a9f35fd8d8bdcc1a54dc6f170ed0038ebe5bb32/find_dc/find_dc_model_31_256.py#L167-L217),
[`correct_dc_model_31_256.py`](https://github.com/Peace9911/sha_2_attack/blob/6a9f35fd8d8bdcc1a54dc6f170ed0038ebe5bb32/find_dc/correct_dc_model_31_256.py#L99-L220),
[`unit_function_256.py`](https://github.com/Peace9911/sha_2_attack/blob/6a9f35fd8d8bdcc1a54dc6f170ed0038ebe5bb32/find_dc/configuration/unit_function_256.py#L99-L121),
and [`constrain_condition.py`](https://github.com/Peace9911/sha_2_attack/blob/6a9f35fd8d8bdcc1a54dc6f170ed0038ebe5bb32/find_dc/configuration/constrain_condition.py#L1-L58).

The final characteristic used below is the slide-14 table, checked against
the printed collision. The repository's `correct_dc_model_31_256.py` adds
intermediate A/E constraints to a differential model; those constraint arrays
are not a complete final condition table. The slide is the source for the
table reproduced here. The repository's `verify_result` program checks
candidate compression results; it does not implement the practical
precomputation-and-matching generator. This proof therefore supplies the
generator's control flow and all condition tables rather than saying to run a
repository attack executable.

The operational rules below resolve choices left at “arbitrary” or
“exhausted” in the presentation. They are specified so a reader can identify
the charged search. They are not claimed to reproduce undocumented random
seeds, thread scheduling, or the authors' private implementation.

## 5. Precise construction procedure

Let `Allowed(C)` enumerate all two-lane 32-bit word pairs matching condition
row `C`. If the `=` positions, numbered from the least-significant bit, are
`p[0] < ... < p[m-1]`, rank `r` from 0 to `2^m-1` sets both bits at `p[j]`
to `(r >> j) AND 1`. Fixed characters use the pair definitions above. Uniform
sampling from `Allowed(C)` draws `m` independent bits; this gives each
permitted pair equal probability. For rows sampled together, words are
processed in the displayed order and the last word's bits change fastest.
An implementation consumes independent uniform 256-bit words and uses their
bits in that order, taking `ceil(m/256)` words for `m` free bits and discarding
unused tail bits; each draw is charged.

The ten-word table record is exactly

```text
(A[-1], A[0], A[1], A[2], A[3], A[4], E[5], E[6], E[7], E[8])
```

Each word is 32 bits. Encode each record as the concatenation of ten
big-endian 32-bit words, exactly 40 bytes. The exact target capacity used here
is `N = ceil(2^19.8) = 912839` records, based on the slide's approximate
`2^19.8` count. Sort this fixed-size byte array in place with ascending
heapsort and lexicographic record comparison; fixed-width big-endian encoding
preserves the ten-word unsigned tuple order. Retain duplicate records. Binary
search returns the complete range sharing the first word `A[-1]`. The set of
accepted eight-word starting keys uses one 32-byte key per distinct point;
there are at most N such keys, and their storage is included in the memory
premise.

### Preprocessing

1. **Trail model.** Select the fixed characteristic table above. The paid
   historical trail-selection stage is the differential-search work; the
   public STP bit-vector model and its settings are described in section 4.
   Charge every generated query, solver invocation, returned model,
   failed/abandoned solver branch, and parsing operation. The final table used
   by the search is the slide-14 table checked here. The public model code is
   not claimed to reproduce that final table by itself; equivalence between
   its result and the published table remains unverified.
2. **Forward starting points.** Draw a candidate pair for
   `(A[1],A[2],A[3],A[4],E[5],...,E[12])` from the corresponding rows of the
   table. `A[1..4]` have only equal conditions. Calculate `A[5]` through
   `A[12]` in increasing index with the A equation. For each lane, calculate
   `W[9]` through `W[12]` by rearranging the E equation:

   ```text
   W[i] = E[i] - A[i-4] - E[i-4] - S1(E[i-1])
          - Ch(E[i-1],E[i-2],E[i-3]) - K[i]    (mod 2^32)
   ```

   Reject the draw on the first A, E, or W bit that violates its row. A valid
   draw defines a starting key `(A[1..4],E[5..8])`; ignore a key already
   accepted. Keep the accepted keys in a set; at most one key is retained per
   distinct starting point. Continue drawing until new starting keys have
   yielded at least one table record and the table reaches `N`, or the v5
   budget in section 6 is exhausted.
3. **Backward extension and records.** For each new valid starting key, first
   enumerate `E[4]` over `Allowed(E[4])`. Derive `W[8]` from the E equation
   at step 8 and reject if either E[4] or W[8] violates its row. Then derive
   `A[0] = E[4] + S0(A[3]) + Maj(A[3],A[2],A[1]) - A[4]` and reject a
   violation of its equal condition. For every remaining `(E[4],W[8],A[0])`,
   enumerate `E[3]` over `Allowed(E[3])`, derive `W[7]` from the E equation
   at step 7, and reject a violation of E[3], W[7], or A[-1], where

   ```text
   A[-1] = E[3] + S0(A[2]) + Maj(A[2],A[1],A[0]) - A[3]  (mod 2^32).
   ```

   Append each surviving ten-word tuple in enumeration order. Stop appending
   when the array has `N` records. If all permitted extensions for a starting
   key fail, discard that key and draw another. Every attempted pair and
   rejected extension is charged.
4. **Table preparation.** Sort the fixed-size array in place by the tuple
   order above. No separate index or second table is kept. Construction
   returns failure if the v5 budget is exhausted before `N` records are
   present. The source reports the table's approximate size but no exact
   cardinality or allocator trace; `N` is the operational threshold for this
   specification.

### Matching, message modification, and fulfillment

For each match attempt, use fresh independent uniform bits as specified here:

1. Draw two independent uniform 256-bit words, concatenate them into a
   uniform 512-bit first block `M0`, and sample with replacement. Execute one
   31-round compression from the standard IV, including feed-forward. Map that chaining state to
   `(A[-4],A[-3],A[-2],A[-1],E[-4],E[-3],E[-2],E[-1])` as
   `(d,c,b,a,h,g,f,e)` in ordinary SHA register order. Binary-search the
   sorted table for every record whose first word `A[-1]` equals this state
   word. A miss advances to the next sampled `M0`.
2. For each matching record in tuple order, recover its start key from
   `A[1..4],E[5..8]`. Re-enumerate the backward extensions in the same rank
   order and retain the first one whose `(A[-1],A[0])` equals the record.
   If no extension reproduces the record, reject it. Re-enumerate allowed
   `(E[9],...,E[12])` tuples in the defined order; calculate `A[5..12]` and
   `W[9..12]` as in preprocessing and use the first tuple satisfying all
   A/E/W rows. If no such tuple exists, reject the record. This recomputation
   avoids storing E[3..4], W[7..12], or an extension pointer in every table
   row; all recomputation work is charged.
3. Reconstruct the missing early values independently in both lanes. For
   `i=0,1,2`, invert the A equation to calculate

   ```text
   E[i] = A[i] + A[i-4] - S0(A[i-1])
          - Maj(A[i-1],A[i-2],A[i-3])                         (mod 2^32).
   ```

   With the reconstructed `E[3]` and `E[4]`, invert the E equation to obtain
   `W[0..8]` from the known IV1 words and the record's A/E values. Reject the
   record if any row for `E[0..8]` or `W[0..9]` fails. This is the slide's
   A[-2]/A[-3] check: those two words come from the sampled common first-block
   state; only values that make the stored A[0..4] and E[5..8] consistent
   with them survive. In particular, calculate `E[0..2]`, then the required
   `W[4..6]` from their E equations and test every bit of those words against
   the W[4..6] rows. Check distinctness of the two reconstructed second
   blocks.
4. **Message modification.** Draw one independent uniform 256-bit word `U`;
   use its top 96 bits, in order, as `(W[13],W[14],W[15])` and use the same
   three words in both lanes. Expand
   the standard schedule through W[30]. Execute both 31-round second-block
   compressions. Check every A/E/W condition from the table and require
   equality of all eight feed-forward output words. If any test fails, discard
   this trial and move to the next record or first block; the triple is not
   reused. `W[13..15]` are the free common words used to fulfill the remaining
   late conditions shown on slide 14.
5. **Complete-hash check and stop.** Prepend `M0`, apply FIPS padding, and
   recompute both complete target digests from the standard IV. Return the
   pair only if the messages are distinct and the full 256-bit digests agree.
   Otherwise continue with the next fresh draw. Stop on the first verified
   pair. All random draws, table misses, matching candidates, failed message
   modifications, hash checks, restarts, and serialization are charged.
   There is no silent restart or success amplification outside this loop.

Solver errors/nonzero exits abort construction. Failed condition checks reject
the current candidate and advance in the stated enumeration order. If the
global v5 budget is exhausted before the first full collision, construction
returns failure. There is no claimed algorithmic success rate for a fresh
bounded construction. The package's `success_probability = 1` is for replay
after a successful construction has been fully paid and the certificate has
verified the retained pair.

The presentation does not publish the authors' random seeds, exact
starting-point draw count, exact table count, or a construction executable.
Uniform draws and the tie-breaking orders above make those otherwise open
choices definite; they are explicit operationalization choices, not claims
about undocumented source code. The certificate in this package verifies the
published pair; no part of this package runs the 2^40-scale search.

## 6. v5 cost ledger

The v5 unit for this target is one 31-round SHA-256 compression. A target
compression costs 1; each other primitive 256-bit word operation, including
random-word generation, costs `1/2140`. The full cost of each construction
phase is included once:

| Phase | Charged work | Source location |
| --- | --- | --- |
| Trail selection | Every STP query, solver invocation, model parse, abandoned objective, and trial; no v5 trace is published, so its translation is inside the historical `cQ+D` premise. | Author `find_dc_model_31_256.py`, lines 167–217; bit models in `unit_function_256.py` and `constrain_condition.py`. |
| Starting-point search | All random bits, A/E recurrences, W[9..12] inversions, tests, duplicates, and rejected samples; each ordinary operation is priced at `1/2140`. | Slides 10–11 give A/E/W solution relations; the precise sampling and rejection sequence is specified above. |
| Backward extension and table build | All E[4]/E[3] enumeration, W[8]/W[7] inversions, A[0]/A[-1] calculations, rejects, 40-byte stores, and repeats to N. | Slide 11; table tuple and reported approximate count on slide 14. |
| Sorting and lookup | In-place sort comparisons/swaps, lower/upper-bound searches, and every matching key comparison are ordinary word operations at `1/2140`. | Slides 12–14 specify the `A[-1]` table match; sort and binary-search order are fixed here. |
| State checks and fulfillment | All reconstruction of E[0..4], W[0..12], schedule work, two second-block compression calls per candidate, W[13..15] draws, condition rejects, and retries. | Slides 12–14 give the A[-1]/A[-2]/A[-3] checks and W[13..15] freedom; equations and sampling rules are above. |
| Final verification and serialization | Every full-hash check is 6 target compressions for two 128-byte messages, plus wrapper word operations at `1/2140`. Failed checks remain charged. | Slide 15 prints the pair and common second-block state; complete padding/hash behavior is defined by the target profile. |
| Deterministic online replay | 6 target compressions plus fewer than `2^20` ordinary word operations for fixed advice loads, length/distinctness checks, comparison, and output. | Exact pair and digest in section 2; replay is also checked by the certificate. |

For each counted phase `j`, let `H_j` be its selected-target compression calls
and `O_j` its other primitive word operations; the v5 price is exactly
`H_j + O_j/2140`. The full historical total is the sum over trail selection,
candidate generation, extensions, table administration, matching, fulfillment,
rejected work, final checking, and serialization. STP's non-word-RAM work has no
published v5 trace; its translation is part of the unknown `c` and `D`, not a
free stage or an inferred discount.

Let `Q=2^40.5` be the paper's time estimate and let `P` be total historical
work in v5 units, including trail selection, table construction and
administration, all failures/restarts, fulfillment, verification, and
serialization. No per-phase counts or v5 trace are available. The declared
premise is

```text
H-HISTORICAL-TIME: P = cQ + D < 2Q = 2^41.5,
                    equivalently c + D/Q < 2.
```

Here `c` is the unknown conversion of the paper's dominant estimate into v5
units. `D` is every included cost not represented by `cQ`. Neither `P` nor
its components are divided by 2140: that price applies only to individually
counted ordinary word operations. The reported 1.2 hours on 64 threads is
wall time and is not divided by 64 in the ledger.

The fixed online wrapper uses at most 128 ordinary word operations by this
inventory: 10 advice/length loads, 4 length checks and branches, 9 operations
for distinctness, 16 for padding construction/checks, 30 state/block transfers
and control around the six calls, 4 digest comparisons/branches, 11 output
serialization operations, and 44 indexing/setup/return operations. The ledger
uses the looser cap of fewer than `2^20` ordinary operations for the fixed
input, including representation work and instruction fetch.

The online replay's total is bounded by

```text
T < 2^41.5 + 6 + 2^20/2140
  = 2^41.5 + 495.988785046729
  < 2^41.500001.
```

The exponent increase from 41.5 to 41.500001 allows 2,155,611.1953125
additional target-compression units, which exceeds the replay term. Therefore
`preprocessing_log2 = 41.5` and `time_log2 = 41.500001` follow if
H-HISTORICAL-TIME holds. Preprocessing is already included in total work.

The table's reported count is approximately `2^19.8`. At N=912839 and ten
32-bit words per record, the raw array is 36,513,560 bytes (about
`2^25.12` bytes). The distinct-start-key set has at most N 32-byte keys,
29,210,848 raw bytes; together these two explicit arrays use 65,724,408 bytes
before allocator and worker overhead. This is evidence for
H-HISTORICAL-MEMORY, not a full peak measurement. The retained messages are
256 bytes; fewer than 256 additional bytes for lengths and digest metadata
keeps advice below 512 bytes, so `nonuniform_advice_log2_bytes = 9`.

## 7. Resource bounds, premises, and open obligations

| Claim field | Bound | Basis |
| --- | ---: | --- |
| `time_log2` | 41.500001 | H-HISTORICAL-TIME plus six-call replay bound |
| `preprocessing_log2` | 41.5 | Same one-time construction premise |
| `memory_log2_bytes` | 40 | H-HISTORICAL-MEMORY, peak below 1 TiB |
| `success_probability` | 1 | Deterministic replay of certified advice |
| `nonuniform_advice_log2_bytes` | 9 | Fewer than 512 retained bytes |

**H-HISTORICAL-TIME (score-critical).** The exact successful historical
construction described above, including all trail search, solver work,
samples, table work, failed candidates, matching, fulfillment, retries,
checks, and the work that made the fixed messages available, costs less than
`2^41.5` v5 units. The source reports `2^40.5` complexity for the same
two-phase 31-step attack and a successful 1.2-hour run with 64 threads. A
factor-two allowance covers unit translation and work omitted from the
headline. This is plausible exploratory evidence; no source supplies `c`,
`D`, an attempt ledger, or a v5 trace. The number and total cost of the
additional runs disclosed by the publisher are also unknown. If `P` reaches
`2^41.5`, both the preprocessing and total-time claims fail.

**H-HISTORICAL-MEMORY (supporting).** Peak simultaneously retained storage for
all search, solver, table, thread, allocator, code, randomness, advice, and
replay phases is below `2^40` bytes. The slide reports about `2^19.8`
ten-word records; their raw payload is 36,513,560 bytes at the operational
capacity. The additional distinct-start-key set is at most 29,210,848 raw
bytes. Together they use 65,724,408 bytes (`2^25.969926`), leaving about
`2^14.030074` multiplicative headroom under the cap for remaining storage.
Neither value is a whole-process peak measurement. No allocator, worker, or
solver peak trace is published. Any phase reaching `2^40` bytes invalidates
this bound.

Open obligations are: (1) H-HISTORICAL-TIME's v5 conversion, aggregate failed
work, and solver/auxiliary-run cost are unmeasured; (2) H-HISTORICAL-MEMORY's
whole-process peak is unmeasured; (3) the fixed witness and deterministic
replay do not reproduce the historical large search, its random sequence, or
its success distribution. This claim uses no fresh-generator success probability,
novelty claim, or rigorous-qualification claim. The deterministic replay
probability is not evidence for either historical resource premise.

## 8. Experiments

No experiment manifest is declared. The claim does not rely on empirical
search success, expected search time, or measured whole-process memory. The
submitted resource bounds rely only on the two explicit historical premises
in section 7.

## 9. Primary sources

1. Yingxin Li, Fukang Liu, Gaoli Wang, Xiaoyang Dong, and Siwei Sun, *The
   First Practical Collision for 31-Step SHA-256*, ASIACRYPT 2024, LNCS 15490,
   pp. 237–266, [DOI](https://doi.org/10.1007/978-981-96-0941-3_8).
2. Authors' ASIACRYPT 2024 slides, especially slides 10–15:
   [PDF](https://iacr.org/submit/files/slides/2024/asiacrypt/asiacrypt2024/64/64_slides.pdf).
3. Authors' public implementation, commit
   [`6a9f35fd8d8bdcc1a54dc6f170ed0038ebe5bb32`](https://github.com/Peace9911/sha_2_attack/tree/6a9f35fd8d8bdcc1a54dc6f170ed0038ebe5bb32).
