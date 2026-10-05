# SHA-256 r32: repaired-subtable ordinary-collision search

## Claim and exact target

This package specifies a finite classical probabilistic search for an ordinary
collision on `sha256-r32-prefix-v1`. The target starts once from the standard
SHA-256 IV, applies rounds 0 through 31 with their original constants and
message schedule on every padded block, performs feed-forward after each block,
and returns all 256 digest bits. The search uses 128-byte messages. If `B0` is a
common 64-byte first block and `B1`, `B1'` are the two distinct second blocks,
the complete messages are

```text
B0 || B1 || 0x80 || 55 zero bytes || BE64(1024)
B0 || B1'|| 0x80 || 55 zero bytes || BE64(1024).
```

The submitted resource bounds are `time_log2=56.091`, peak memory
`2^40` bytes, preprocessing at most `2^55`
target-compression equivalents, nonuniform advice at most
`2^20` bytes, and algorithmic success probability at least 0.39.
No concrete standard-IV C32 collision was found. The probability and resource
bounds depend on the explicitly declared premises in this proof and
`claim.json`.

## Source construction and the r32 boundary

The starting point is the 35-step SHA-256 construction of Li, Liu, Wang and
Shi, *Pushing the Limit of Memory-Efficient Collision Attack Framework for
SHA-2*, ePrint 2026/1080, Section 4, Figure 6 and Table 3. The source reports
about `2^29.1824` prefix-table rows, bridge density `2^-20.92`, `2^17.585`
candidate `(W14,W15)` pairs per bridge, 45 residual conditions, Step-1 work
about `2^34.3`, and overall bridge-search work about `2^48.335` in its own
units.

Independent replay gives

```text
C35(IV,M0) = c4369610 c91f70a7 87e430e6 a5e58128
             d29cb97b 9ab268d1 8788f401 629f6cb2
C32(IV,M0) = 6a9f7255 39f4063e a684176a b5efb469
             57ccf218 f7ab3896 562fcb55 c67d5c37.
```

The published second blocks have equal reduced-compression outputs from the
C35 chaining value after every round count 23 through 35, but not from the C32
chaining value. Thus the published complete messages are a C35 collision, not
a collision for this target. This algorithm retains the second-block
construction but searches for a fresh common first block using C32 itself.

Four printed relation symbols are read as corrections because the printed
forms exclude the source's own Table 3 witness: the A14, A15 and W20 relations
are inequalities, and the E7 component relation is equality. Two earlier
transcriptions were also corrected directly from the Figure 6 image:
`E18[2]=E18[16]` and `A14[9]=A14[20]`. These choices are part of the algorithm,
not silent edits. The Table 3 state, tail and collision replay pass them. The
source-faithful A14 reading and the earlier redundant cross-state test generate
the same ordered 196,608-element tail set for this construction.

## State-consistent repair and the frozen table

The initial expanded-table attempt varied E5, E6 and E7 while retaining
A1 through A13. That violates the SHA-256 state recurrence except at Table 3.
For each Figure 6 E5/E6/E7 triple, the repaired construction retains A4 through
A13 and reconstructs the lower A words backwards:

```text
A3 = E7 + Sigma0(A6) + Maj(A6,A5,A4) - A7
A2 = E6 + Sigma0(A5) + Maj(A5,A4,A3) - A6
A1 = E5 + Sigma0(A4) + Maj(A4,A3,A2) - A5
```

All operations are modulo `2^32`, separately in the two branches. Retain a
variant only if the derived A words agree where Figure 6 requires equality,
all A cross-relations hold in both branches, the known-state round recurrences
hold, and derived W9 through W13 satisfy their rows. Of 1,048,576 row-and-
relation E5/E6/E7 triples, 1,048,576 survive A3 equality, 32,768 survive A2
equality, and 10,240 survive A1 equality and every remaining prefix check.

The exact count-only expansion of those 10,240 variants has 1,848 nonempty
variants and 1,396,774,912 records. This is about 2.293 times, not equal to,
the paper's approximate `2^29.1824` rows. The earlier roughly 95-fold
projection came from variants that failed the A-state recurrence and is not
used here.

The attack freezes a smaller table selected before its record counts were
known: seed 2026100505 selected 64 variants uniformly without replacement from
the 10,239 non-Table-3 survivors and then added Table 3. The complete selected
table has:

| Quantity | Exact result |
| --- | ---: |
| Selected variants | 65 |
| Nonempty selected variants | 14 |
| Records | 8,025,600 |
| Distinct A(-1) keys | 4,088,007 |
| Maximum records at one key | 16 |
| Packed seven-word stream | 224,716,816 bytes |

For each variant, enumerate every allowed W8 pair, derive E4 and A0 in both
branches, and retain the row-, relation- and equality-valid results. For each
survivor enumerate every allowed W7 pair, derive E3 and A(-1), and retain equal
A(-1). A stored record is `(A(-1), variant_id, W7, W8, E3, E4, A0)` and is
sorted lexicographically in that order. Table 3 reproduces the independently
known 593,920 records and its exact multiplicity histogram. Representative
records from all 14 nonempty selected variants replay the complete eight-word
state through round 13 in both branches. A copied-artifact control with one W7
bit changed fails by name at round 7.

## Bridge lookup and tail sweep

For a fresh uniform 64-byte `B0`, compute `CV=C32(IV,B0)` and interpret its
eight words as the common incoming A and E halves. Use `CV.A(-1)` to locate its
record group. Scan at most 16 records in sorted order. For each record,
reconstruct both branches' early state and W0 through W6, then test W0 through
W3 equality and every W4, W5 and W6 row and relation. The first passing record
is canonical. A trial with no passing record is rejected.

The high prefix state A4 through A13 and E8 through E13 is the same in all 65
variants, so one exact source-faithful list of 196,608 `(W14,W15)` pairs serves
every bridge. W9 through W13 and W0 through W8 remain record- and bridge-
specific. For each canonical accepted bridge, form both complete second blocks
for every tail in fixed list order and compute both C32 outputs from the actual
CV. A second-block equality is retained. Since the W4 row makes the blocks
different, the two messages are distinct. A common padding block preserves an
equal second-block chaining state. Before return, independently hash both
complete 128-byte messages from the standard IV and require all 256 digest bits
to agree.

This direct C32 comparison makes collision soundness independent of the
differential heuristic. The differential and its measurements are used only
to lower-bound the chance that the finite search reaches an equality.

## Finite algorithm and caps

Preprocessing reconstructs the fixed characteristic and starting point,
derives the frozen 65 variants, enumerates and sorts the exact table, builds a
direct `2^32`-entry read-only key-to-span index, and enumerates the tail list.
All choices are fixed before the fresh first-block coins.

The online run uses the following caps:

```text
q >= 2^-25                     accepted bridge probability premise
pi >= 2^-30                   average successful-sweep premise
N = 2^55                      first-block trials
B = 2^29                      canonical accepted bridges swept
L = 196608                    tails per sweep
R = 2^48                      total records examined
d = 16                        exact per-key record cap
mu <= 2^-8                    mean records examined per trial premise
P <= 2^55                     all preprocessing in target equivalents
```

The run examines at most N first blocks, stops before record examination R+1,
and sweeps at most the first B canonical accepted bridges. It may retain the
first verified collision but continues no work beyond the fixed caps. If a cap
is reached without a verified pair, it returns failure. The cost bound is
therefore deterministic for every choice of coins.

### Exact search, failure handling, and stopping rule

All additions and subtractions below are modulo `2^32`. `ROTR`, `Sigma0`,
`Sigma1`, `sigma0`, `sigma1`, `Ch`, and `Maj` are the FIPS SHA-256 functions;
the first 32 FIPS round constants are used. A row is a 32-character string from
MSB to LSB. `=` means an equal free bit, `0` and `1` fix both branches, `u`
means left 0/right 1, and `n` means left 1/right 0. Relation indices count from
the least significant bit. Appendix A gives every score-bearing prefix and tail
row, published word input, and frozen variant state as inert JSON. Appendix B
gives the complete dependency closure for the variant constructor, table
builder, bridge sampler, tail engine, and ledger used to instantiate the finite
algorithm. It also includes two independent scalar checkers; their historical
pilot streams are diagnostic inputs, not inputs to the charged online
construction.

Preprocessing performs these deterministic steps in order:

1. Enumerate all Figure 6 E5/E6/E7 row-and-relation triples in lexicographic
   Cartesian order. Derive A3, A2, A1 with the three backward equations above;
   reject immediately on a required branch equality, A relation, state
   recurrence, or W9--W13 row failure. Assign the Cartesian index as
   `variant_id`.
2. List the 10,239 non-Table-3 survivors in increasing Cartesian-index order.
   Apply CPython's `random.Random(2026100505).sample(list, 64)` to that list,
   add the Table-3 variant, then sort the 65 IDs numerically. The constructor
   source records this procedure, and Appendix A freezes the resulting 65 IDs,
   so those IDs rather than a Python-version-dependent replay are normative.
   This selection precedes record counting.
3. For each selected variant, enumerate the W8 row domain in integer assignment
   order, derive both E4 and A0 values, and reject on the E4 row, E4 relation,
   or A0 branch inequality. For each survivor enumerate W7 the same way, derive
   E3 and A(-1), and retain equal A(-1). Emit the seven-word record
   `(A(-1),variant_id,W7,W8,E3,E4,A0)`. Sort all records lexicographically and
   reject duplicate or malformed records.
4. Allocate `2^32` direct-address entries of 16 bytes each. Scan the sorted
   table once, writing the exact `(start,count)` span for every present
   A(-1) key and `(0,0)` for every absent key. Abort preprocessing if any count
   exceeds 16 or if a stored span does not reproduce exactly the contiguous
   sorted records for its key.
5. Enumerate E14, then E15, in integer assignment order. Derive the two W14/A14
   and W15/A15 branches and retain exactly the corrected rows and relations.
   The result must have 196,608 ordered pairs and the ordered big-endian
   `(W14,W15)` byte stream must hash to
   `33217b7b360c05deb16661fb5dcc25655704824f5070c976288874866195de37`.
   Any mismatch aborts preprocessing.

The online algorithm then executes exactly:

```text
accepted = 0; examined = 0; saved = none
for trial = 0,...,N-1:
    draw 512 fresh independent random bits; serialize them as B0
    CV = C32(standard_IV, B0)
    read (start,count) from direct_index[CV[0]]
    if count > 16: return failure
    take the count records beginning at start as the sorted record span
    canonical = none
    for record in that span, in stored order:
        if examined == R: return failure
        examined += 1
        load the record's variant state
        derive E2,E1,E0 and W0,...,W6 in both branches
        if W0,...,W3 are unequal: continue
        if any W4,W5,W6 row or relation fails: continue
        canonical = record; break
    if canonical is none: continue
    if accepted == B: return saved after final verification, else failure
    accepted += 1
    replay both prefixes through round 13; mismatch means failure
    for (W14,W15) in the fixed 196608-element list:
        form both distinct 16-word second blocks
        left  = C32(CV, left_block)
        right = C32(CV, right_block)
        if left == right and saved is none: save (B0,left_block,right_block)
after the loop:
    if saved is none: return failure
    hash both complete 128-byte messages plus the common padding block
    return them only if they differ and all 256 digest bits agree; otherwise fail
```

If a collision is saved before a cap, the loops may stop immediately because
the charged ledger is an upper bound. The pseudocode above instead permits
continuation to the fixed caps; either rule has the same returned-pair check
and cannot exceed the ledger. Malformed data, a state replay mismatch, an
unexpected tail commitment, a cap that would be exceeded, or a failed final
digest comparison returns failure and never a candidate pair.

## Measured bridge rate and load

The repaired-table stream was fixed at seed 2026100519 and `2^33` trials before
its 4,096-trial prefix smoke and conditional pilot. It generated every first
block with SplitMix64-seeded xoshiro256**, computed C32 from the standard IV,
and retained all counts and accepted inputs without adaptive stopping. The
complete result is:

| Quantity | Result |
| --- | ---: |
| First-block C32 trials | 8,589,934,592 |
| Key-hit trials | 8,171,516 |
| Records in hit groups | 16,043,766 |
| Canonical records examined | 16,043,350 |
| Accepted canonical bridges | 351 |
| Observed q | 4.0861777961e-8 = 2^-24.54467 |
| Nominal iid Wilson 99.9% diagnostic | [3.4287633500e-8, 4.8696416919e-8] |
| Mean examined records per trial | 0.0018676917534 = 2^-9.06453 |

The cumulative record-filter vector is 16,043,350; 8,020,187; 1,003,371;
62,898; 7,893; 2,907; and 351 for W0--W3 equality, W4 row, W4 relations,
W5 row, W5 relations, W6 row and W6 relations. An independent auditor checked
the complete packed table and state mapping, reconstructed every recorded RNG
block and C32 CV, replayed both prefixes for all 351 accepts, and verified that
each stored record is the canonical first valid record. A disposable changed-W7
record fails by name at `accepted_record_not_canonical_first_valid`.

The measured sampler located each key with a top-16-bit directory followed by
binary search inside that directory. It read the same sorted contiguous span
and applied the same stored order and canonical first-valid-record rule as the
charged direct-address index. The lookup representation therefore cannot
change the observed q or record-load counts; only its lookup work differs, and
the selected ledger separately charges the direct-index lookup.

The point q is 1.371 times 2^-25, and even the nominal 99.9% diagnostic lower
endpoint is 1.150 times 2^-25. The mean-load premise 2^-8 is 2.092 times the
observed mean. These are relevant margins, not calibrated guarantees: the
entire stream is deterministic once its seed is fixed, and no PRNG observation
proves the mathematical fresh-coin population bounds.

The exact table bound gives `0<=C<=16` for the record examinations C on one
trial. Under the declared actual-C32 mean premise `E[C]<=2^-8`, independent
first-block coins make the C values independent even though C can be correlated
with acceptance. Since `C^2<=16C`,

```text
Var(sum C) <= N * 16 * E[C].
```

With the selected R, Chebyshev gives the overflow bound used below.

## Tail evidence and its conditioning limit

The source's 45 residual conditions and `2^17.585` tails give the central model
`2^-27.415` for one full sweep. The corrected scalar oracle reproduces the
published Table 3 tail and exact C32 equality from its published C35 chaining
value. It also reproduces the 196,608-tail domain with two independent schedule
implementations and rejects changed E20 and schedule-index artifacts by name.

The first complete direct measurement swept all 196,608 tails for each of 27
canonical bridges from a precommitted standard-IV C32 stream, 5,308,416 tails
in total. Sequential survivors were 34,427 at the E16 row, 218 after E16
relations, six at the E17 row, and zero at E18 and later stages. This zero is
expected at the target event scale and is not used as a rate estimate.

The rare-event estimator was piloted first on 31 abstract accepted A halves.
Seed 2026100505 gave five successes in 1,000,000 proposals, each K=1. After
freezing the extended schema and independently replaying those five outcomes,
seed 2026100518 made 100,000,000 proposals on all 27 standard-IV accepted
A-half/record pairs. It produced this sequential residual vector after the
forced E16--E18 proposal conditions:

| Stage | Survivors |
| --- | ---: |
| E19 row | 50,001,341 |
| E20 row | 25,005,183 |
| W20 row | 390,738 |
| W20 relations | 6,026 |
| W22 row | 3,054 |
| W22 relations | 385 |
| Complete named path and exact C32 equality | 209 |

All 209 complete outcomes have K=1. The inverse-multiplicity estimate is
`3.0615234375e-9`, about `2^-28.28`, with Monte Carlo standard error
`2.11770e-10`. This is a deterministic seeded measurement, so the standard
error describes dispersion under the proposal calculation but no calibrated
confidence interval is claimed. Every base contributed between 3 and 15
successes; no base had zero. All 209 outcomes independently replay through the
pinned repository compressor with equal complete C32 feed-forward outputs.
Every one of the 100,000,000 reconstructed
E halves retains all W4--W6 bridge conditions. A separate seed checked 1,024
uniform E halves for each base (27,648 total) and reproduced the same invariant
W4--W6 words.

The importance proposal chooses E16, E17, E18 and E19 from exact row domains
with 18, 27, 25 and 31 free bits, respectively. For a fixed A half, variant,
record and tail, it inverts the message schedule triangularly to W0 through W3
and then the round equations to the initial E half. The target/proposal weight
for a uniform 128-bit E half is `2^(101-128)=2^-27`. If K is the number of
path-conforming successful tails for the reconstructed CV, inverse-
multiplicity weighting estimates the full-sweep union probability under that
uniform-E law:

```text
pi_uniform = L * E_proposal[2^-27 * I(selected tail succeeds) / K].
```

Every recorded success was replayed with the pinned target compressor and its
K was obtained by a complete 196,608-tail sweep.

This estimator changes the incoming E half after drawing an accepted A half and
record. For fixed A and record, however, E2, E1 and E0 follow from the A
recurrence while E3 and E4 are in the record. W4 through W6 therefore do not
depend on the incoming E half; the same holds for every record in the key group,
so the canonical first-valid record is invariant. A 10,000-proposal regression
rechecked all six W4--W6 stages and every proposal passed. The estimate is thus
the path-conforming full-sweep yield under uniform E for the empirical accepted
A-half/record cohort. The reconstructed CVs still lack standard-IV first-block
preimages. The declared tail premise transfers this uniform-E result to the
actual C32 E-half law within accepted bridges. The threshold slack and remaining
limitations are stated with that premise; no calibrated confidence interval is
claimed.

The variant-aware oracle loads all 65 repaired states independently from both
the JSON map and binary sidecar and requires exact equality. It reproduces the
Table-3 prefix, every named late predicate, and the exact C32 output. It also
replays conditional-pilot trial 1458 for non-Table-3 variant 640554 through
round 13 and all W4--W6 bridge predicates. Both variants generate the same
ordered 196,608-tail stream with SHA-256
`33217b7b360c05deb16661fb5dcc25655704824f5070c976288874866195de37`.
Changing W9 bit 0 in either copied variant fails by name. Sixty-four E19 inverse
cases for each variant type reproduce their four targets and weight `2^-27`.

The variant-aware C++ Table-3 sweep exactly matches the fixed implementation's
complete stage vector. Complete sweeps on all 351 independently audited
standard-IV accepts cover 69,009,408 tails. Sequential survivors were 554,399
at the E16 row, 4,293 after its relations, 135 at E17, seven at E18, two after
the E18 relations, and zero at E19. This complete sweep records the observable
stages but supplies no terminal rare-event rate estimate.

The repaired-cohort importance run was fixed at seed 2026100522 and 20,000,000
proposals after the 351-bridge audit and before evaluating that proposal stream.
It uses the same exact `2^-27` likelihood ratio and inverse-multiplicity event.
Its residual sequential counts were 10,001,757 at E19, 5,000,373 at E20,
78,161 at the W20 row, 1,297 after W20 relations, 671 at the W22 row, 82 after
W22 relations, and 43 exact C32 path successes. Every success had `K=1`, so the
empirical repaired-cohort estimate is `3.1494140625e-9`, about `2^-28.24`, with
Monte Carlo standard error `4.80281e-10` and no calibrated interval. All 43
outcomes independently replay through the pinned compressor, and all 20 million
reconstructed proposals retain the six W4--W6 predicates. This measurement
directly covers the empirical repaired-variant cohort. The score-bearing
`pi>=2^-30` still transfers the uniform reconstructed-E result to the actual
accepted C32 E-half law; the reconstructed halves have no first-block preimages.
A fixed deterministic empirical 351-row cohort does not prove the
accepted-bridge population mean. These are distinct limitations: one concerns
extrapolation from the measured cohort to the accepted-bridge population, and
the other concerns transfer from uniform reconstructed E halves to the actual
accepted C32 E-half law. Fixed seeds and the post-pilot threshold choice provide
no calibrated coverage for either step.

## Success probability

Let X be the number of canonical accepted bridges in the first N trials of an
unbounded reference run. Under q and fresh independent first-block coins,
`X~Binomial(N,q)`. With the selected parameters `E[X]>=2^30=2B` and a
multiplicative Chernoff bound gives

```text
Pr[X < B] <= exp(-2^27).
```

Accepted bridges in order are iid from the single-trial distribution
conditioned on canonical acceptance. A complete tail sweep is a deterministic
indicator of its bridge; the premise says its conditional mean is at least pi.
Therefore

```text
Pr[first B sweeps all miss | X>=B]
  <= (1-pi)^B
  <= exp(-B*pi)
  <= exp(-1/2).
```

The record budget overflows with probability at most `2^-43`. A union
bound gives

```text
Pr[success] >= 1 - exp(-1/2) - exp(-2^27) - 2^-43
            > 0.39.
```

The submitted 0.39 is this algorithmic lower bound conditional on the declared
q, pi and load premises. It is not confidence in those premises.

## Charged work

Under `collision-frontier-v5`, one C32 call costs one target-compression unit
and each other primitive 256-bit word operation costs 1/2224. The ledger uses

```text
H = N + 2*B*L + 6
W = 256*N + 2048*R + 8192*B + 512*B*L
T = H + W/2224 + P.
```

The N term is one first-block C32 call per trial. Each tail uses two C32 calls,
one per second block. The final six calls independently hash two three-block
messages. Padding is computed only for a retained second-block equality; six
calls already cover final replay even if no earlier padding shortcut is used.

The selected per-unit ceilings are itemized as follows; the final appendix
recomputes them from the stated primitives.

| Unit | Word-operation ceiling | Included work |
| --- | ---: | --- |
| First-block trial outside C32 | 256 | two uniform 256-bit words; message serialization; packed dense-index address, load, mask and shift; empty-group check; counters, branches, retained-result control and spare wrapper traffic. The C32 call is in H. |
| Examined table record | 2,048 | record and variant-state loads; both-branch E2/E1/E0 and W0--W6 inversion; W0--W3 equality; all W4--W6 rows and relations; canonical-loop control and stores. |
| Accepted bridge setup | 8,192 | load the variant state, reconstruct and replay both prefixes through round 13, form the two second-block templates, and initialize sweep/verification state. |
| One tail outside C32 | 512 | load W14/W15, update both block templates, invoke two separately charged C32 calls, compare eight output words, and update counters/retained candidate state. |

The first-block lookup uses a direct `2^32`-entry index with 16 bytes per entry,
`2^36` bytes total. Each entry holds the start offset and 0--16 count. This
deliberately loose representation avoids hiding a search over the
8,025,600-record array; a packed four-byte representation is possible but is
not needed for the submitted memory bound. The 2,048-record allowance retains
the much larger earlier itemized ceiling. C32 schedule/round/feed-forward work
is charged only through H and is not duplicated in W.

For the selected integer caps, the exact ledger is

```text
H = 36239903251496966
W = 9853880382733156352
P = 2^55
T = 170579469784238273568 / 2224
log2(T) = 56.09006484552054
```

The claim rounds this upward to `time_log2=56.091`. Failed trials, table
construction, sorting, indexing, randomness, lookup, record filtering, every
tail, final verification and all historical discovery work are included.

## Preprocessing, memory and advice

The source reports Step-1 work about `2^34.3` but does not give a v5 conversion
or a numeric total for the preceding four-stage characteristic search. The
claim therefore declares the aggregate historical-and-finite preprocessing
ceiling `P<=2^55` as a score-critical premise. It includes characteristic
discovery, starting-solution search, failed searches, repair enumeration,
table construction, sorting, indexing, tail construction and validation. The
finite construction is directly countable and is far below P; the unmeasured
historical search controls the premise.

Online table records can be padded to one 32-byte RAM word, using less than
`8,025,600*32 < 2^28` bytes. The `2^36`-byte direct index, variant map, 1.6 MB
tail list, two table images during bottom-up sorting, messages, code and scratch
keep the finite construction below `2^37` bytes. The submitted
`2^40` peak also covers the historical search under a separately
declared memory premise. The paper reports a 378 GB server capacity; this is
relevant capacity evidence, not a peak trace.

Retained nonuniform advice consists of the source characteristic, Table 3
starting blocks/state, 65 selected variant inputs, Figure 6 rows and relations,
constants, labels and lengths. Its itemized encoding is below
`2^20` bytes. The generated table and tail list are preprocessing
data whose construction is charged in P and whose retained bytes are charged
to memory; they are not free stored advice.

## Declared premises and limitations

The claim declares five premises:

1. `repaired-subtable-c32-bridge-density` supplies the stated lower bound q for
   the exact frozen table and canonical rule. Its actual-standard-IV seeded
   measurement is directly relevant, but deterministic seed expansion and the
   selected threshold do not prove a fresh-coin population bound.
2. `repaired-subtable-record-load` bounds the actual-C32 mean examined records
   by 2^-8. Exact d=16 and the measured mean support the abort analysis;
   transfer from the seeded stream remains unresolved.
3. `accepted-bridge-tail-yield` states pi at least 2^-30 for the repaired
   accepted-bridge distribution. The exact path control, direct stage sweeps
   and a measured uniform-E mean about 2^-28.28 support the threshold. The
   fixed deterministic empirical 351-row cohort does not prove the
   accepted-bridge population mean. Separately, uniform reconstructed E halves
   still must transfer to the actual accepted C32 E-half law, and those halves
   have no standard-IV first-block preimages. Fixed seeds and the post-pilot
   threshold choice provide no calibrated coverage.
4. `historical-preprocessing-resource-bound` charges at most 2^55 v5
   equivalents for every historical and finite construction phase. The source
   reports Step-1 work about 2^34.3 and overall bridge-search work about
   2^48.335, while the finite table work is counted directly. The source gives
   neither a v5 conversion nor a numeric characteristic-search total.
5. `historical-peak-memory-bound` states that all phases fit in 2^40 bytes.
   The finite online and table-build layout is below 2^37 bytes and the source
   reports a 378 GB server. That capacity figure is not a measured peak.

The first four premises affect the score or success proof. The fifth affects
the separately reviewed memory field. No unlisted ideal-hash, independent-tail,
or free-preprocessing assumption is used.

All computational observations in this package are participant-produced inert
evidence. There is no organizer experiment manifest or execution report. The
fixed seeds make the streams reproducible but do not turn their outputs into
fresh ideal coins or calibrated statistical confidence. No full-scale attack
or standard-IV C32 collision is claimed.

## Embedded evidence

Appendices A--C are assembled from the immutable completed artifacts. Their
content is inert: there is no organizer experiment manifest or certificate.

## Appendix A: exact inert inputs

### Figure 6 prefix conditions

Embedded JSON SHA-256: `717520fd21cbb2b0da95ed1d885b839131122943fb97fb1af8198e614cb86d39`.

```json
{
  "bit_convention": {
    "bit_zero": "least significant bit",
    "row_leftmost_bit": 31,
    "symbols": {
      "0": "both bits fixed to 0",
      "1": "both bits fixed to 1",
      "=": "same free bit in both branches",
      "n": "1 to 0",
      "u": "0 to 1"
    }
  },
  "corrections_verified_on_table3_witness": [
    "A14[18,8] != A14[6,17]",
    "A15[29] != A6[29]",
    "W20[4,31] != W20[6,22]",
    "E7[21,10] = E7[3,15] (authorized fourth correction; printed inequality excludes Table 3)"
  ],
  "relations": {
    "A14": {
      "same_as_state_bits": [
        [
          20,
          4,
          9
        ]
      ],
      "unequal_state_bits": [
        [
          15,
          13,
          15
        ]
      ],
      "unequal_vectors": [
        [
          [
            18,
            8
          ],
          [
            6,
            17
          ]
        ]
      ],
      "xor_mask": "0000000020000000"
    },
    "A15": {
      "equal_branches": true,
      "unequal_state_bits": [
        [
          29,
          6,
          29
        ],
        [
          29,
          13,
          29
        ]
      ]
    },
    "E4": {
      "unequal_bit_pairs": [
        [
          10,
          15
        ]
      ]
    },
    "W20": {
      "unequal_vectors": [
        [
          [
            4,
            31
          ],
          [
            6,
            22
          ]
        ]
      ]
    },
    "W4": {
      "equal_vectors": [
        [
          [
            18
          ],
          [
            14
          ]
        ]
      ],
      "unequal_vectors": [
        [
          [
            1,
            8
          ],
          [
            12,
            25
          ]
        ]
      ]
    },
    "W5": {
      "equal_vectors": [
        [
          [
            0,
            1,
            30
          ],
          [
            28,
            18,
            9
          ]
        ]
      ]
    },
    "W6": {
      "equal_vectors": [
        [
          [
            1,
            8
          ],
          [
            12,
            25
          ]
        ]
      ],
      "unequal_vectors": [
        [
          [
            18
          ],
          [
            14
          ]
        ]
      ]
    },
    "W7": {
      "equal_vectors": [
        [
          [
            11,
            14,
            20
          ],
          [
            22,
            31,
            31
          ]
        ]
      ],
      "unequal_vectors": [
        [
          [
            22,
            13,
            23
          ],
          [
            18,
            9,
            8
          ]
        ]
      ]
    },
    "W8": {
      "equal_vectors": [
        [
          [
            0,
            14,
            21
          ],
          [
            28,
            25,
            6
          ]
        ]
      ],
      "unequal_vectors": [
        [
          [
            31,
            23,
            30,
            15,
            22,
            8
          ],
          [
            27,
            2,
            15,
            26,
            7,
            4
          ]
        ]
      ]
    }
  },
  "rows": {
    "A14": "==u=============================",
    "A15": "================================",
    "E14": "=0=100110000000=101=0000=110===0",
    "E15": "=1====0011===u10001=011===0n===1",
    "E3": "=====1=====011======0======0====",
    "E4": "==n0=0=1===100=0==0=1===0==1=0=1",
    "W4": "==n=============================",
    "W5": "=====u===u==========n===========",
    "W6": "==n=============================",
    "W7": "=======n=======u===u====u=1=u=u=",
    "W8": "============u=======uu=========="
  },
  "source": {
    "citation": "Yingxin Li, Fukang Liu, Gaoli Wang, Jiali Shi, Pushing the Limit of Memory-efficient Collision Attack Framework for SHA-2, Cryptology ePrint Archive, Paper 2026/1080, Section 4, Figure 6 and Table 3.",
    "figure6_location": "Published pagination pp. 302-303; Figure 6.",
    "table3_location": "Published pagination p. 307; Table 3.",
    "transcribed_for": "sha256-r32-prefix-v1 fixed-slice reconstruction"
  }
}
```

### Figure 6 tail conditions

Embedded JSON SHA-256: `acbe8688d8c417c0a642c39b445a9206b4cde197ce5ac738d03934282e48cb2b`.

```json
{
  "authorized_corrections": [
    "A14[18,8] != A14[6,17]",
    "A15[29] != A6[29]",
    "W20[4,31] != W20[6,22]",
    "E7[21,10] = E7[3,15]"
  ],
  "relations": {
    "A14": {
      "equal": [
        [
          9,
          20
        ]
      ],
      "equal_A13": [
        [
          30,
          30
        ],
        [
          25,
          25
        ],
        [
          23,
          23
        ]
      ],
      "unequal": [
        [
          18,
          6
        ],
        [
          8,
          17
        ]
      ],
      "unequal_A13": [
        [
          15,
          15
        ]
      ]
    },
    "A15": {
      "unequal_A13": [
        [
          29,
          29
        ]
      ],
      "unequal_A6": [
        [
          29,
          29
        ]
      ]
    },
    "E16": {
      "equal": [
        [
          28,
          1
        ],
        [
          20,
          7
        ],
        [
          20,
          2
        ],
        [
          6,
          11
        ]
      ],
      "unequal": [
        [
          30,
          12
        ],
        [
          28,
          10
        ],
        [
          10,
          29
        ]
      ]
    },
    "E18": {
      "equal": [
        [
          2,
          16
        ]
      ],
      "unequal": [
        [
          24,
          11
        ]
      ]
    },
    "W20": {
      "unequal": [
        [
          4,
          6
        ],
        [
          31,
          22
        ],
        [
          31,
          1
        ],
        [
          30,
          0
        ],
        [
          25,
          16
        ],
        [
          21,
          14
        ]
      ]
    },
    "W22": {
      "equal": [
        [
          4,
          6
        ],
        [
          31,
          22
        ]
      ],
      "unequal": [
        [
          27,
          20
        ]
      ]
    }
  },
  "rows": {
    "A14": "==u=============================",
    "A15": "================================",
    "A16": "================================",
    "E14": "=0=100110000000=101=0000=110===0",
    "E15": "=1====0011===u10001=011===0n===1",
    "E16": "======u=n====1==n=====0===01====",
    "E17": "======0=0====1==0==========1====",
    "E18": "==u===1=0=======1====1==========",
    "E19": "==0=============================",
    "E20": "==1=============================",
    "W20": "=====0=nn=====0=u=1=============",
    "W22": "==n============================="
  },
  "source": "Li et al., ePrint 2026/1080, Figure 6; rows transcribed MSB-to-LSB, relation indices are LSB=0",
  "symbols": {
    "0": "both zero",
    "1": "both one",
    "=": "equal free bit",
    "n": "unprimed one, primed zero",
    "u": "unprimed zero, primed one"
  }
}
```

### Published Table 3 words

Embedded JSON SHA-256: `ebee813e9a69fb6b9abcef86d0acbad59490eb97cb71e532404f2fd1333e2af8`.

```json
{
  "M0_words": "a8850273 c0f4a504 5d3ad7b5 6e5f5026 535cc256 e92ef7a5 436f70df 7d7e236a cadc14e8 d59ac191 6874f1ba 6b83960d f6dfe9de 6a013df2 f856b739 237894e8",
  "M1_prime_words": "c0008214 ae65f3bf e93c006a 5f195aa9 84d6cd0f 25c114ec ca897317 da9fd6ef 6ec97e18 5100da8a 0912e57b a96b2054 41b22a2c 6d12f88a d2701ecc 140976d1",
  "M1_words": "c0008214 ae65f3bf e93c006a 5f195aa9 a4d6cd0f 21811cec ea897317 db9ec665 6ec17218 5100da8a 0912e57b a96b2054 45f2222c 4d12f88a d2701ecc 140976d1",
  "reported_C32_IV_M0": "6a9f7255 39f4063e a684176a b5efb469 57ccf218 f7ab3896 562fcb55 c67d5c37",
  "reported_C32_second_block_collision_from_C35_cv": true,
  "reported_C35_IV_M0": "c4369610 c91f70a7 87e430e6 a5e58128 d29cb97b 9ab268d1 8788f401 629f6cb2",
  "reported_C35_second_block_collision": true,
  "source": "Li et al., ePrint 2026/1080, Section 4, Table 3, published pagination p. 307.",
  "word_encoding": "16 big-endian 32-bit SHA-256 message words per block; hex text in word order."
}
```

### Frozen repaired-variant mapping

Embedded JSON SHA-256: `e47c9a2ee02cc553f22796e6c04b46d91ba6e03ceb0f0ba2fdc9a261309ea234`.

```json
{
  "common_fixed_state": {
    "A4_A13": {
      "left": [
        "b8560dbb",
        "677e1e2a",
        "9bcf7bbe",
        "f8677ad6",
        "4a299906",
        "44d24ab4",
        "39781650",
        "6c206d58",
        "35c5c2b8",
        "0508c8f0"
      ],
      "right": [
        "98560dbb",
        "633b16ba",
        "9bcf7bbe",
        "f8677ad6",
        "4a299906",
        "44f24ab5",
        "39781650",
        "6422edc8",
        "574542b8",
        "0508c8f0"
      ]
    },
    "E8_E13": {
      "left": [
        "11cae594",
        "d504bf23",
        "7f27d24c",
        "bf893f69",
        "2300f189",
        "fcc08ef5"
      ],
      "right": [
        "f1cae594",
        "d0e1b7b4",
        "bf27d74c",
        "b78bbfd9",
        "3fffd0f9",
        "bf81c0f4"
      ]
    }
  },
  "experiment": "immutable mapping for the 65-variant repaired subtable",
  "selection": {
    "binary_format": "BWR1, big-endian uint32 count, then count records of (cartesian_id,E5,E5p,E6,E6p,E7,E7p)",
    "binary_path": "backward-sample-variants.bin",
    "binary_sha256": "1d50ca93bd78c137dd893b03533e623895c49e37c934c81881a098f78d68feb0",
    "cartesian_ids": [
      16934,
      17170,
      17190,
      26274,
      26546,
      50106,
      50994,
      58274,
      59014,
      59306,
      90810,
      123410,
      133054,
      148146,
      180894,
      180922,
      181134,
      190214,
      213814,
      214802,
      223118,
      255654,
      263070,
      279090,
      287670,
      296714,
      296886,
      313146,
      320158,
      320178,
      320438,
      321302,
      377738,
      385574,
      393994,
      427926,
      444314,
      452134,
      508458,
      516666,
      542262,
      550530,
      557714,
      574134,
      640554,
      648114,
      656898,
      680478,
      706362,
      713634,
      770710,
      804666,
      819866,
      836226,
      837274,
      845714,
      870330,
      901894,
      919338,
      967426,
      976526,
      1008266,
      1032838,
      1041178,
      1042230
    ],
    "non_table3_size": 64,
    "sample_size": 65,
    "seed": 2026100505,
    "selection_rule": "64 uniform variants without replacement from the 10,239 non-Table-3 survivors, plus the Table 3 control",
    "table3_controls": 1
  },
  "variants": [
    {
      "A1_A3": {
        "left": [
          "65c43574",
          "587a1bf8",
          "9131b01f"
        ],
        "right": [
          "65c43574",
          "587a1bf8",
          "9131b01f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d18aa4",
          "b1df6594",
          "87511040"
        ],
        "right": [
          "5c8d82b4",
          "a1cf4d01",
          "a7501040"
        ]
      },
      "W9_W13": {
        "left": [
          "5924e292",
          "1084a27b",
          "a95d2174",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5924e292",
          "1084a27b",
          "a95d2174",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 16934
    },
    {
      "A1_A3": {
        "left": [
          "65c42974",
          "587a0cf8",
          "9121e11f"
        ],
        "right": [
          "65c42974",
          "587a0cf8",
          "9121e11f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d18aa4",
          "b1df6594",
          "87414140"
        ],
        "right": [
          "5c8d82b4",
          "a1cf4d01",
          "a7404140"
        ]
      },
      "W9_W13": {
        "left": [
          "5924a192",
          "1094627b",
          "a96cf074",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5924a192",
          "1094627b",
          "a96cf074",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 17170
    },
    {
      "A1_A3": {
        "left": [
          "65c43974",
          "587a1cf8",
          "9131b11f"
        ],
        "right": [
          "65c43974",
          "587a1cf8",
          "9131b11f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d18aa4",
          "b1df6594",
          "87511140"
        ],
        "right": [
          "5c8d82b4",
          "a1cf4d01",
          "a7501140"
        ]
      },
      "W9_W13": {
        "left": [
          "5924e192",
          "1084a27b",
          "a95d2074",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5924e192",
          "1084a27b",
          "a95d2074",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 17190
    },
    {
      "A1_A3": {
        "left": [
          "65643974",
          "589a1df8",
          "9121b23f"
        ],
        "right": [
          "65643974",
          "589a1df8",
          "9121b23f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d18aa4",
          "b1ff6594",
          "87411260"
        ],
        "right": [
          "5c8d82b4",
          "a1ef4d01",
          "a7401260"
        ]
      },
      "W9_W13": {
        "left": [
          "5904e292",
          "1074a27b",
          "a96d1f54",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5904e292",
          "1074a27b",
          "a96d1f54",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 26274
    },
    {
      "A1_A3": {
        "left": [
          "65643b74",
          "589a1ef8",
          "9121f33f"
        ],
        "right": [
          "65643b74",
          "589a1ef8",
          "9121f33f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d18aa4",
          "b1ff6594",
          "87415360"
        ],
        "right": [
          "5c8d82b4",
          "a1ef4d01",
          "a7405360"
        ]
      },
      "W9_W13": {
        "left": [
          "5904a192",
          "1074627b",
          "a96cde54",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5904a192",
          "1074627b",
          "a96cde54",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 26546
    },
    {
      "A1_A3": {
        "left": [
          "65c43ad4",
          "587a1f00",
          "9123f31f"
        ],
        "right": [
          "65c43ad4",
          "587a1f00",
          "9123f31f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d18aa4",
          "b1df659c",
          "87435340"
        ],
        "right": [
          "5c8d82b4",
          "a1cf4d09",
          "a7425340"
        ]
      },
      "W9_W13": {
        "left": [
          "5922a18a",
          "10926273",
          "a96ade74",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5922a18a",
          "10926273",
          "a96ade74",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 50106
    },
    {
      "A1_A3": {
        "left": [
          "65c438f4",
          "587a1d00",
          "9121f13f"
        ],
        "right": [
          "65c438f4",
          "587a1d00",
          "9121f13f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d18aa4",
          "b1df659c",
          "87415160"
        ],
        "right": [
          "5c8d82b4",
          "a1cf4d09",
          "a7405160"
        ]
      },
      "W9_W13": {
        "left": [
          "5924a18a",
          "10946273",
          "a96ce054",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5924a18a",
          "10946273",
          "a96ce054",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 50994
    },
    {
      "A1_A3": {
        "left": [
          "65643ad4",
          "589a1f00",
          "9121b31f"
        ],
        "right": [
          "65643ad4",
          "589a1f00",
          "9121b31f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d18aa4",
          "b1ff659c",
          "87411340"
        ],
        "right": [
          "5c8d82b4",
          "a1ef4d09",
          "a7401340"
        ]
      },
      "W9_W13": {
        "left": [
          "5904e18a",
          "1074a273",
          "a96d1e74",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5904e18a",
          "1074a273",
          "a96d1e74",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 58274
    },
    {
      "A1_A3": {
        "left": [
          "656429f4",
          "589a0e00",
          "9131a23f"
        ],
        "right": [
          "656429f4",
          "589a0e00",
          "9131a23f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d18aa4",
          "b1ff659c",
          "87510260"
        ],
        "right": [
          "5c8d82b4",
          "a1ef4d09",
          "a7500260"
        ]
      },
      "W9_W13": {
        "left": [
          "5904e28a",
          "1064a273",
          "a95d2f54",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5904e28a",
          "1064a273",
          "a95d2f54",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 59014
    },
    {
      "A1_A3": {
        "left": [
          "65643af4",
          "589a1f00",
          "9123b33f"
        ],
        "right": [
          "65643af4",
          "589a1f00",
          "9123b33f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d18aa4",
          "b1ff659c",
          "87431360"
        ],
        "right": [
          "5c8d82b4",
          "a1ef4d09",
          "a7421360"
        ]
      },
      "W9_W13": {
        "left": [
          "5902e18a",
          "1072a273",
          "a96b1e54",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5902e18a",
          "1072a273",
          "a96b1e54",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 59306
    },
    {
      "A1_A3": {
        "left": [
          "6564b9f4",
          "5a9a9e3a",
          "9123f21f"
        ],
        "right": [
          "6564b9f4",
          "5a9a9e3a",
          "9123f21f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d18aa4",
          "b3ffe5d6",
          "87435240"
        ],
        "right": [
          "5c8d82b4",
          "a3efcd43",
          "a7425240"
        ]
      },
      "W9_W13": {
        "left": [
          "5702a250",
          "0e71e239",
          "a96adf74",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5702a250",
          "0e71e239",
          "a96adf74",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 90810
    },
    {
      "A1_A3": {
        "left": [
          "6564a7d4",
          "5a9a8c42",
          "9121e01f"
        ],
        "right": [
          "6564a7d4",
          "5a9a8c42",
          "9121e01f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d18aa4",
          "b3ffe5de",
          "87414040"
        ],
        "right": [
          "5c8d82b4",
          "a3efcd4b",
          "a7404040"
        ]
      },
      "W9_W13": {
        "left": [
          "5704a248",
          "0e73e231",
          "a96cf174",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5704a248",
          "0e73e231",
          "a96cf174",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 123410
    },
    {
      "A1_A3": {
        "left": [
          "66c7f774",
          "5ff9dbf8",
          "9133f33f"
        ],
        "right": [
          "66c7f774",
          "5ff9dbf8",
          "9133f33f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d38aa4",
          "b95f2294",
          "87535360"
        ],
        "right": [
          "5c8f82b4",
          "a94f0a01",
          "a7525360"
        ]
      },
      "W9_W13": {
        "left": [
          "51209f92",
          "0902a57b",
          "a95ade54",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "51209f92",
          "0902a57b",
          "a95ade54",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 133054
    },
    {
      "A1_A3": {
        "left": [
          "65c63974",
          "587a1df8",
          "9121f21f"
        ],
        "right": [
          "65c63974",
          "587a1df8",
          "9121f21f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d38aa4",
          "b1df6594",
          "87415240"
        ],
        "right": [
          "5c8f82b4",
          "a1cf4d01",
          "a7405240"
        ]
      },
      "W9_W13": {
        "left": [
          "5922a292",
          "1094627b",
          "a96cdf74",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5922a292",
          "1094627b",
          "a96cdf74",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 148146
    },
    {
      "A1_A3": {
        "left": [
          "65c629d4",
          "587a0e00",
          "9133e21f"
        ],
        "right": [
          "65c629d4",
          "587a0e00",
          "9133e21f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d38aa4",
          "b1df659c",
          "87534240"
        ],
        "right": [
          "5c8f82b4",
          "a1cf4d09",
          "a7524240"
        ]
      },
      "W9_W13": {
        "left": [
          "5920a28a",
          "10826273",
          "a95aef74",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5920a28a",
          "10826273",
          "a95aef74",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 180894
    },
    {
      "A1_A3": {
        "left": [
          "65c639d4",
          "587a1e00",
          "9123f21f"
        ],
        "right": [
          "65c639d4",
          "587a1e00",
          "9123f21f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d38aa4",
          "b1df659c",
          "87435240"
        ],
        "right": [
          "5c8f82b4",
          "a1cf4d09",
          "a7425240"
        ]
      },
      "W9_W13": {
        "left": [
          "5920a28a",
          "10926273",
          "a96adf74",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5920a28a",
          "10926273",
          "a96adf74",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 180922
    },
    {
      "A1_A3": {
        "left": [
          "65c62ad4",
          "587a0f00",
          "9133a31f"
        ],
        "right": [
          "65c62ad4",
          "587a0f00",
          "9133a31f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d38aa4",
          "b1df659c",
          "87530340"
        ],
        "right": [
          "5c8f82b4",
          "a1cf4d09",
          "a7520340"
        ]
      },
      "W9_W13": {
        "left": [
          "5920e18a",
          "1082a273",
          "a95b2e74",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5920e18a",
          "1082a273",
          "a95b2e74",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 181134
    },
    {
      "A1_A3": {
        "left": [
          "656628f4",
          "589a0d00",
          "9131a13f"
        ],
        "right": [
          "656628f4",
          "589a0d00",
          "9131a13f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d38aa4",
          "b1ff659c",
          "87510160"
        ],
        "right": [
          "5c8f82b4",
          "a1ef4d09",
          "a7500160"
        ]
      },
      "W9_W13": {
        "left": [
          "5902e18a",
          "1064a273",
          "a95d3054",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5902e18a",
          "1064a273",
          "a95d3054",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 190214
    },
    {
      "A1_A3": {
        "left": [
          "65c6b8f4",
          "5a7a9d3a",
          "9131f11f"
        ],
        "right": [
          "65c6b8f4",
          "5a7a9d3a",
          "9131f11f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d38aa4",
          "b3dfe5d6",
          "87515140"
        ],
        "right": [
          "5c8f82b4",
          "a3cfcd43",
          "a7505140"
        ]
      },
      "W9_W13": {
        "left": [
          "5722a150",
          "0e83e239",
          "a95ce074",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5722a150",
          "0e83e239",
          "a95ce074",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 213814
    },
    {
      "A1_A3": {
        "left": [
          "65c6a8f4",
          "5a7a8d3a",
          "9121e13f"
        ],
        "right": [
          "65c6a8f4",
          "5a7a8d3a",
          "9121e13f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d38aa4",
          "b3dfe5d6",
          "87414160"
        ],
        "right": [
          "5c8f82b4",
          "a3cfcd43",
          "a7404160"
        ]
      },
      "W9_W13": {
        "left": [
          "5722a150",
          "0e93e239",
          "a96cf054",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5722a150",
          "0e93e239",
          "a96cf054",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 214802
    },
    {
      "A1_A3": {
        "left": [
          "6566aaf4",
          "5a9a8f3a",
          "9133a33f"
        ],
        "right": [
          "6566aaf4",
          "5a9a8f3a",
          "9133a33f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d38aa4",
          "b3ffe5d6",
          "87530360"
        ],
        "right": [
          "5c8f82b4",
          "a3efcd43",
          "a7520360"
        ]
      },
      "W9_W13": {
        "left": [
          "5700e150",
          "0e622239",
          "a95b2e54",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5700e150",
          "0e622239",
          "a95b2e54",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 223118
    },
    {
      "A1_A3": {
        "left": [
          "6566b9f4",
          "5a9a9e42",
          "9131b23f"
        ],
        "right": [
          "6566b9f4",
          "5a9a9e42",
          "9131b23f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d38aa4",
          "b3ffe5de",
          "87511260"
        ],
        "right": [
          "5c8f82b4",
          "a3efcd4b",
          "a7501260"
        ]
      },
      "W9_W13": {
        "left": [
          "5702e248",
          "0e642231",
          "a95d1f54",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5702e248",
          "0e642231",
          "a95d1f54",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 255654
    },
    {
      "A1_A3": {
        "left": [
          "66c5eb74",
          "5ff9cbf8",
          "9133e31f"
        ],
        "right": [
          "66c5eb74",
          "5ff9cbf8",
          "9133e31f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d18ea4",
          "b95f2294",
          "87534340"
        ],
        "right": [
          "5c8d86b4",
          "a94f0a01",
          "a7524340"
        ]
      },
      "W9_W13": {
        "left": [
          "51229b92",
          "0902a57b",
          "a95aee74",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "51229b92",
          "0902a57b",
          "a95aee74",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 263070
    },
    {
      "A1_A3": {
        "left": [
          "65c43974",
          "587a1bf8",
          "9121f01f"
        ],
        "right": [
          "65c43974",
          "587a1bf8",
          "9121f01f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d18ea4",
          "b1df6594",
          "87415040"
        ],
        "right": [
          "5c8d86b4",
          "a1cf4d01",
          "a7405040"
        ]
      },
      "W9_W13": {
        "left": [
          "59249e92",
          "1094627b",
          "a96ce174",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "59249e92",
          "1094627b",
          "a96ce174",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 279090
    },
    {
      "A1_A3": {
        "left": [
          "65643f74",
          "589a1ef8",
          "9131f31f"
        ],
        "right": [
          "65643f74",
          "589a1ef8",
          "9131f31f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d18ea4",
          "b1ff6594",
          "87515340"
        ],
        "right": [
          "5c8d86b4",
          "a1ef4d01",
          "a7505340"
        ]
      },
      "W9_W13": {
        "left": [
          "59049d92",
          "1064627b",
          "a95cde74",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "59049d92",
          "1064627b",
          "a95cde74",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 287670
    },
    {
      "A1_A3": {
        "left": [
          "66c5a8f4",
          "5ff9ca00",
          "9123a13f"
        ],
        "right": [
          "66c5a8f4",
          "5ff9ca00",
          "9123a13f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d18ea4",
          "b95f229c",
          "87430160"
        ],
        "right": [
          "5c8d86b4",
          "a94f0a09",
          "a7420160"
        ]
      },
      "W9_W13": {
        "left": [
          "5122db8a",
          "0912e573",
          "a96b3054",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5122db8a",
          "0912e573",
          "a96b3054",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 296714
    },
    {
      "A1_A3": {
        "left": [
          "66c3fcf4",
          "5ff9dc00",
          "9131f33f"
        ],
        "right": [
          "66c3fcf4",
          "5ff9dc00",
          "9131f33f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d18ea4",
          "b95f229c",
          "87515360"
        ],
        "right": [
          "5c8d86b4",
          "a94f0a09",
          "a7505360"
        ]
      },
      "W9_W13": {
        "left": [
          "51249b8a",
          "0904a573",
          "a95cde54",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "51249b8a",
          "0904a573",
          "a95cde54",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 296886
    },
    {
      "A1_A3": {
        "left": [
          "65c43cf4",
          "587a1d00",
          "9123f13f"
        ],
        "right": [
          "65c43cf4",
          "587a1d00",
          "9123f13f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d18ea4",
          "b1df659c",
          "87435160"
        ],
        "right": [
          "5c8d86b4",
          "a1cf4d09",
          "a7425160"
        ]
      },
      "W9_W13": {
        "left": [
          "59229d8a",
          "10926273",
          "a96ae054",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "59229d8a",
          "10926273",
          "a96ae054",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 313146
    },
    {
      "A1_A3": {
        "left": [
          "65642dd4",
          "589a0e00",
          "9133e21f"
        ],
        "right": [
          "65642dd4",
          "589a0e00",
          "9133e21f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d18ea4",
          "b1ff659c",
          "87534240"
        ],
        "right": [
          "5c8d86b4",
          "a1ef4d09",
          "a7524240"
        ]
      },
      "W9_W13": {
        "left": [
          "59029e8a",
          "10626273",
          "a95aef74",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "59029e8a",
          "10626273",
          "a95aef74",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 320158
    },
    {
      "A1_A3": {
        "left": [
          "65643dd4",
          "589a1e00",
          "9121f21f"
        ],
        "right": [
          "65643dd4",
          "589a1e00",
          "9121f21f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d18ea4",
          "b1ff659c",
          "87415240"
        ],
        "right": [
          "5c8d86b4",
          "a1ef4d09",
          "a7405240"
        ]
      },
      "W9_W13": {
        "left": [
          "59049e8a",
          "10746273",
          "a96cdf74",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "59049e8a",
          "10746273",
          "a96cdf74",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 320178
    },
    {
      "A1_A3": {
        "left": [
          "65643ed4",
          "589a1f00",
          "9131f31f"
        ],
        "right": [
          "65643ed4",
          "589a1f00",
          "9131f31f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d18ea4",
          "b1ff659c",
          "87515340"
        ],
        "right": [
          "5c8d86b4",
          "a1ef4d09",
          "a7505340"
        ]
      },
      "W9_W13": {
        "left": [
          "59049d8a",
          "10646273",
          "a95cde74",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "59049d8a",
          "10646273",
          "a95cde74",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 320438
    },
    {
      "A1_A3": {
        "left": [
          "65642cf4",
          "589a0d00",
          "9131e13f"
        ],
        "right": [
          "65642cf4",
          "589a0d00",
          "9131e13f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d18ea4",
          "b1ff659c",
          "87514160"
        ],
        "right": [
          "5c8d86b4",
          "a1ef4d09",
          "a7504160"
        ]
      },
      "W9_W13": {
        "left": [
          "59049d8a",
          "10646273",
          "a95cf054",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "59049d8a",
          "10646273",
          "a95cf054",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 321302
    },
    {
      "A1_A3": {
        "left": [
          "65c4aed4",
          "5a7a8f42",
          "9123a31f"
        ],
        "right": [
          "65c4aed4",
          "5a7a8f42",
          "9123a31f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d18ea4",
          "b3dfe5de",
          "87430340"
        ],
        "right": [
          "5c8d86b4",
          "a3cfcd4b",
          "a7420340"
        ]
      },
      "W9_W13": {
        "left": [
          "5722dd48",
          "0e922231",
          "a96b2e74",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5722dd48",
          "0e922231",
          "a96b2e74",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 377738
    },
    {
      "A1_A3": {
        "left": [
          "6564bbd4",
          "5a9a9c42",
          "9131b01f"
        ],
        "right": [
          "6564bbd4",
          "5a9a9c42",
          "9131b01f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d18ea4",
          "b3ffe5de",
          "87511040"
        ],
        "right": [
          "5c8d86b4",
          "a3efcd4b",
          "a7501040"
        ]
      },
      "W9_W13": {
        "left": [
          "5704de48",
          "0e642231",
          "a95d2174",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5704de48",
          "0e642231",
          "a95d2174",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 385574
    },
    {
      "A1_A3": {
        "left": [
          "66c7a974",
          "5ff9c9f8",
          "9123a11f"
        ],
        "right": [
          "66c7a974",
          "5ff9c9f8",
          "9123a11f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d38ea4",
          "b95f2294",
          "87430140"
        ],
        "right": [
          "5c8f86b4",
          "a94f0a01",
          "a7420140"
        ]
      },
      "W9_W13": {
        "left": [
          "5120db92",
          "0912e57b",
          "a96b3074",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5120db92",
          "0912e57b",
          "a96b3074",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 393994
    },
    {
      "A1_A3": {
        "left": [
          "66c5ecf4",
          "5ff9cc00",
          "9131e33f"
        ],
        "right": [
          "66c5ecf4",
          "5ff9cc00",
          "9131e33f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d38ea4",
          "b95f229c",
          "87514360"
        ],
        "right": [
          "5c8f86b4",
          "a94f0a09",
          "a7504360"
        ]
      },
      "W9_W13": {
        "left": [
          "51229b8a",
          "0904a573",
          "a95cee54",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "51229b8a",
          "0904a573",
          "a95cee54",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 427926
    },
    {
      "A1_A3": {
        "left": [
          "65c62ef4",
          "587a0f00",
          "9123e33f"
        ],
        "right": [
          "65c62ef4",
          "587a0f00",
          "9123e33f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d38ea4",
          "b1df659c",
          "87434360"
        ],
        "right": [
          "5c8f86b4",
          "a1cf4d09",
          "a7424360"
        ]
      },
      "W9_W13": {
        "left": [
          "59209d8a",
          "10926273",
          "a96aee54",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "59209d8a",
          "10926273",
          "a96aee54",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 444314
    },
    {
      "A1_A3": {
        "left": [
          "65663bf4",
          "589a1c00",
          "9131b03f"
        ],
        "right": [
          "65663bf4",
          "589a1c00",
          "9131b03f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d38ea4",
          "b1ff659c",
          "87511060"
        ],
        "right": [
          "5c8f86b4",
          "a1ef4d09",
          "a7501060"
        ]
      },
      "W9_W13": {
        "left": [
          "5902de8a",
          "1064a273",
          "a95d2154",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5902de8a",
          "1064a273",
          "a95d2154",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 452134
    },
    {
      "A1_A3": {
        "left": [
          "65c6bbd4",
          "5a7a9c42",
          "9123b01f"
        ],
        "right": [
          "65c6bbd4",
          "5a7a9c42",
          "9123b01f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d38ea4",
          "b3dfe5de",
          "87431040"
        ],
        "right": [
          "5c8f86b4",
          "a3cfcd4b",
          "a7421040"
        ]
      },
      "W9_W13": {
        "left": [
          "5720de48",
          "0e922231",
          "a96b2174",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5720de48",
          "0e922231",
          "a96b2174",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 508458
    },
    {
      "A1_A3": {
        "left": [
          "6566bbd4",
          "5a9a9c42",
          "9123f01f"
        ],
        "right": [
          "6566bbd4",
          "5a9a9c42",
          "9123f01f"
        ]
      },
      "E5_E7": {
        "left": [
          "58d38ea4",
          "b3ffe5de",
          "87435040"
        ],
        "right": [
          "5c8f86b4",
          "a3efcd4b",
          "a7425040"
        ]
      },
      "W9_W13": {
        "left": [
          "57009e48",
          "0e71e231",
          "a96ae174",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "57009e48",
          "0e71e231",
          "a96ae174",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 516666
    },
    {
      "A1_A3": {
        "left": [
          "65e4367c",
          "587a1bf8",
          "9131f03f"
        ],
        "right": [
          "65e4367c",
          "587a1bf8",
          "9131f03f"
        ]
      },
      "E5_E7": {
        "left": [
          "58f18bac",
          "b1df6594",
          "87515060"
        ],
        "right": [
          "5cad83bc",
          "a1cf4d01",
          "a7505060"
        ]
      },
      "W9_W13": {
        "left": [
          "5904a18a",
          "1084627b",
          "a95ce154",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5904a18a",
          "1084627b",
          "a95ce154",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 542262
    },
    {
      "A1_A3": {
        "left": [
          "65842a7c",
          "589a0df8",
          "9121a23f"
        ],
        "right": [
          "65842a7c",
          "589a0df8",
          "9121a23f"
        ]
      },
      "E5_E7": {
        "left": [
          "58f18bac",
          "b1ff6594",
          "87410260"
        ],
        "right": [
          "5cad83bc",
          "a1ef4d01",
          "a7400260"
        ]
      },
      "W9_W13": {
        "left": [
          "58e4e18a",
          "1074a27b",
          "a96d2f54",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "58e4e18a",
          "1074a27b",
          "a96d2f54",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 550530
    },
    {
      "A1_A3": {
        "left": [
          "66e3e7dc",
          "5ff9cb00",
          "9121e21f"
        ],
        "right": [
          "66e3e7dc",
          "5ff9cb00",
          "9121e21f"
        ]
      },
      "E5_E7": {
        "left": [
          "58f18bac",
          "b95f229c",
          "87414240"
        ],
        "right": [
          "5cad83bc",
          "a94f0a09",
          "a7404240"
        ]
      },
      "W9_W13": {
        "left": [
          "51049f82",
          "0914a573",
          "a96cef74",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "51049f82",
          "0914a573",
          "a96cef74",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 557714
    },
    {
      "A1_A3": {
        "left": [
          "65e43adc",
          "587a1e00",
          "9131f21f"
        ],
        "right": [
          "65e43adc",
          "587a1e00",
          "9131f21f"
        ]
      },
      "E5_E7": {
        "left": [
          "58f18bac",
          "b1df659c",
          "87515240"
        ],
        "right": [
          "5cad83bc",
          "a1cf4d09",
          "a7505240"
        ]
      },
      "W9_W13": {
        "left": [
          "5904a182",
          "10846273",
          "a95cdf74",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5904a182",
          "10846273",
          "a95cdf74",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 574134
    },
    {
      "A1_A3": {
        "left": [
          "65e4b8fc",
          "5a7a9c42",
          "9123b03f"
        ],
        "right": [
          "65e4b8fc",
          "5a7a9c42",
          "9123b03f"
        ]
      },
      "E5_E7": {
        "left": [
          "58f18bac",
          "b3dfe5de",
          "87431060"
        ],
        "right": [
          "5cad83bc",
          "a3cfcd4b",
          "a7421060"
        ]
      },
      "W9_W13": {
        "left": [
          "5702e140",
          "0e922231",
          "a96b2154",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5702e140",
          "0e922231",
          "a96b2154",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 640554
    },
    {
      "A1_A3": {
        "left": [
          "6584bbdc",
          "5a9a9f42",
          "9121f31f"
        ],
        "right": [
          "6584bbdc",
          "5a9a9f42",
          "9121f31f"
        ]
      },
      "E5_E7": {
        "left": [
          "58f18bac",
          "b3ffe5de",
          "87415340"
        ],
        "right": [
          "5cad83bc",
          "a3efcd4b",
          "a7405340"
        ]
      },
      "W9_W13": {
        "left": [
          "56e4a040",
          "0e73e231",
          "a96cde74",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "56e4a040",
          "0e73e231",
          "a96cde74",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 648114
    },
    {
      "A1_A3": {
        "left": [
          "66e5a57c",
          "5ff9c8f8",
          "9121a03f"
        ],
        "right": [
          "66e5a57c",
          "5ff9c8f8",
          "9121a03f"
        ]
      },
      "E5_E7": {
        "left": [
          "58f38bac",
          "b95f2294",
          "87410060"
        ],
        "right": [
          "5caf83bc",
          "a94f0a01",
          "a7400060"
        ]
      },
      "W9_W13": {
        "left": [
          "5102df8a",
          "0914e57b",
          "a96d3154",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5102df8a",
          "0914e57b",
          "a96d3154",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 656898
    },
    {
      "A1_A3": {
        "left": [
          "6586267c",
          "589a0bf8",
          "9133e01f"
        ],
        "right": [
          "6586267c",
          "589a0bf8",
          "9133e01f"
        ]
      },
      "E5_E7": {
        "left": [
          "58f38bac",
          "b1ff6594",
          "87534040"
        ],
        "right": [
          "5caf83bc",
          "a1ef4d01",
          "a7524040"
        ]
      },
      "W9_W13": {
        "left": [
          "58e0a18a",
          "1062627b",
          "a95af174",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "58e0a18a",
          "1062627b",
          "a95af174",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 680478
    },
    {
      "A1_A3": {
        "left": [
          "65e639fc",
          "587a1d00",
          "9123f13f"
        ],
        "right": [
          "65e639fc",
          "587a1d00",
          "9123f13f"
        ]
      },
      "E5_E7": {
        "left": [
          "58f38bac",
          "b1df659c",
          "87435160"
        ],
        "right": [
          "5caf83bc",
          "a1cf4d09",
          "a7425160"
        ]
      },
      "W9_W13": {
        "left": [
          "5900a082",
          "10926273",
          "a96ae054",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5900a082",
          "10926273",
          "a96ae054",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 706362
    },
    {
      "A1_A3": {
        "left": [
          "65863bdc",
          "589a1f00",
          "9121b31f"
        ],
        "right": [
          "65863bdc",
          "589a1f00",
          "9121b31f"
        ]
      },
      "E5_E7": {
        "left": [
          "58f38bac",
          "b1ff659c",
          "87411340"
        ],
        "right": [
          "5caf83bc",
          "a1ef4d09",
          "a7401340"
        ]
      },
      "W9_W13": {
        "left": [
          "58e2e082",
          "1074a273",
          "a96d1e74",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "58e2e082",
          "1074a273",
          "a96d1e74",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 713634
    },
    {
      "A1_A3": {
        "left": [
          "65e6aadc",
          "5a7a8e42",
          "9131e21f"
        ],
        "right": [
          "65e6aadc",
          "5a7a8e42",
          "9131e21f"
        ]
      },
      "E5_E7": {
        "left": [
          "58f38bac",
          "b3dfe5de",
          "87514240"
        ],
        "right": [
          "5caf83bc",
          "a3cfcd4b",
          "a7504240"
        ]
      },
      "W9_W13": {
        "left": [
          "5702a140",
          "0e83e231",
          "a95cef74",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5702a140",
          "0e83e231",
          "a95cef74",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 770710
    },
    {
      "A1_A3": {
        "left": [
          "65e43e7c",
          "587a1cf8",
          "9123f13f"
        ],
        "right": [
          "65e43e7c",
          "587a1cf8",
          "9123f13f"
        ]
      },
      "E5_E7": {
        "left": [
          "58f18fac",
          "b1df6594",
          "87435160"
        ],
        "right": [
          "5cad87bc",
          "a1cf4d01",
          "a7425160"
        ]
      },
      "W9_W13": {
        "left": [
          "59029c8a",
          "1092627b",
          "a96ae054",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "59029c8a",
          "1092627b",
          "a96ae054",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 804666
    },
    {
      "A1_A3": {
        "left": [
          "66e5ebdc",
          "5ff9cb00",
          "9123e21f"
        ],
        "right": [
          "66e5ebdc",
          "5ff9cb00",
          "9123e21f"
        ]
      },
      "E5_E7": {
        "left": [
          "58f18fac",
          "b95f229c",
          "87434240"
        ],
        "right": [
          "5cad87bc",
          "a94f0a09",
          "a7424240"
        ]
      },
      "W9_W13": {
        "left": [
          "51029b82",
          "0912a573",
          "a96aef74",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "51029b82",
          "0912a573",
          "a96aef74",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 819866
    },
    {
      "A1_A3": {
        "left": [
          "65e42edc",
          "587a0e00",
          "9121a21f"
        ],
        "right": [
          "65e42edc",
          "587a0e00",
          "9121a21f"
        ]
      },
      "E5_E7": {
        "left": [
          "58f18fac",
          "b1df659c",
          "87410240"
        ],
        "right": [
          "5cad87bc",
          "a1cf4d09",
          "a7400240"
        ]
      },
      "W9_W13": {
        "left": [
          "5904dd82",
          "1094a273",
          "a96d2f74",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5904dd82",
          "1094a273",
          "a96d2f74",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 836226
    },
    {
      "A1_A3": {
        "left": [
          "65e42efc",
          "587a0e00",
          "9123e23f"
        ],
        "right": [
          "65e42efc",
          "587a0e00",
          "9123e23f"
        ]
      },
      "E5_E7": {
        "left": [
          "58f18fac",
          "b1df659c",
          "87434260"
        ],
        "right": [
          "5cad87bc",
          "a1cf4d09",
          "a7424260"
        ]
      },
      "W9_W13": {
        "left": [
          "59029d82",
          "10926273",
          "a96aef54",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "59029d82",
          "10926273",
          "a96aef54",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 837274
    },
    {
      "A1_A3": {
        "left": [
          "65842ffc",
          "589a0f00",
          "9121e33f"
        ],
        "right": [
          "65842ffc",
          "589a0f00",
          "9121e33f"
        ]
      },
      "E5_E7": {
        "left": [
          "58f18fac",
          "b1ff659c",
          "87414360"
        ],
        "right": [
          "5cad87bc",
          "a1ef4d09",
          "a7404360"
        ]
      },
      "W9_W13": {
        "left": [
          "58e49c82",
          "10746273",
          "a96cee54",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "58e49c82",
          "10746273",
          "a96cee54",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 845714
    },
    {
      "A1_A3": {
        "left": [
          "65e4bffc",
          "5a7a9f3a",
          "9123f33f"
        ],
        "right": [
          "65e4bffc",
          "5a7a9f3a",
          "9123f33f"
        ]
      },
      "E5_E7": {
        "left": [
          "58f18fac",
          "b3dfe5d6",
          "87435360"
        ],
        "right": [
          "5cad87bc",
          "a3cfcd43",
          "a7425360"
        ]
      },
      "W9_W13": {
        "left": [
          "57029c48",
          "0e91e239",
          "a96ade54",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "57029c48",
          "0e91e239",
          "a96ade54",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 870330
    },
    {
      "A1_A3": {
        "left": [
          "65e4addc",
          "5a7a8d42",
          "9131a11f"
        ],
        "right": [
          "65e4addc",
          "5a7a8d42",
          "9131a11f"
        ]
      },
      "E5_E7": {
        "left": [
          "58f18fac",
          "b3dfe5de",
          "87510140"
        ],
        "right": [
          "5cad87bc",
          "a3cfcd4b",
          "a7500140"
        ]
      },
      "W9_W13": {
        "left": [
          "5704dc40",
          "0e842231",
          "a95d3074",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5704dc40",
          "0e842231",
          "a95d3074",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 901894
    },
    {
      "A1_A3": {
        "left": [
          "66e7ba7c",
          "5ff9d9f8",
          "9123b13f"
        ],
        "right": [
          "66e7ba7c",
          "5ff9d9f8",
          "9123b13f"
        ]
      },
      "E5_E7": {
        "left": [
          "58f38fac",
          "b95f2294",
          "87431160"
        ],
        "right": [
          "5caf87bc",
          "a94f0a01",
          "a7421160"
        ]
      },
      "W9_W13": {
        "left": [
          "5100da8a",
          "0912e57b",
          "a96b2054",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5100da8a",
          "0912e57b",
          "a96b2054",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": true,
      "variant_id": 919338
    },
    {
      "A1_A3": {
        "left": [
          "65e62ddc",
          "587a0d00",
          "9121a11f"
        ],
        "right": [
          "65e62ddc",
          "587a0d00",
          "9121a11f"
        ]
      },
      "E5_E7": {
        "left": [
          "58f38fac",
          "b1df659c",
          "87410140"
        ],
        "right": [
          "5caf87bc",
          "a1cf4d09",
          "a7400140"
        ]
      },
      "W9_W13": {
        "left": [
          "5902dc82",
          "1094a273",
          "a96d3074",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5902dc82",
          "1094a273",
          "a96d3074",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 967426
    },
    {
      "A1_A3": {
        "left": [
          "65862efc",
          "589a0e00",
          "9133a23f"
        ],
        "right": [
          "65862efc",
          "589a0e00",
          "9133a23f"
        ]
      },
      "E5_E7": {
        "left": [
          "58f38fac",
          "b1ff659c",
          "87530260"
        ],
        "right": [
          "5caf87bc",
          "a1ef4d09",
          "a7520260"
        ]
      },
      "W9_W13": {
        "left": [
          "58e0dd82",
          "1062a273",
          "a95b2f54",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "58e0dd82",
          "1062a273",
          "a95b2f54",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 976526
    },
    {
      "A1_A3": {
        "left": [
          "6586aefc",
          "5a9a8e3a",
          "9123a21f"
        ],
        "right": [
          "6586aefc",
          "5a9a8e3a",
          "9123a21f"
        ]
      },
      "E5_E7": {
        "left": [
          "58f38fac",
          "b3ffe5d6",
          "87430240"
        ],
        "right": [
          "5caf87bc",
          "a3efcd43",
          "a7420240"
        ]
      },
      "W9_W13": {
        "left": [
          "56e0dd48",
          "0e722239",
          "a96b2f74",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "56e0dd48",
          "0e722239",
          "a96b2f74",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 1008266
    },
    {
      "A1_A3": {
        "left": [
          "65e6aedc",
          "5a7a8e42",
          "9131a21f"
        ],
        "right": [
          "65e6aedc",
          "5a7a8e42",
          "9131a21f"
        ]
      },
      "E5_E7": {
        "left": [
          "58f38fac",
          "b3dfe5de",
          "87510240"
        ],
        "right": [
          "5caf87bc",
          "a3cfcd4b",
          "a7500240"
        ]
      },
      "W9_W13": {
        "left": [
          "5702dd40",
          "0e842231",
          "a95d2f74",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "5702dd40",
          "0e842231",
          "a95d2f74",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 1032838
    },
    {
      "A1_A3": {
        "left": [
          "6586addc",
          "5a9a8d42",
          "9123e11f"
        ],
        "right": [
          "6586addc",
          "5a9a8d42",
          "9123e11f"
        ]
      },
      "E5_E7": {
        "left": [
          "58f38fac",
          "b3ffe5de",
          "87434140"
        ],
        "right": [
          "5caf87bc",
          "a3efcd4b",
          "a7424140"
        ]
      },
      "W9_W13": {
        "left": [
          "56e09c40",
          "0e71e231",
          "a96af074",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "56e09c40",
          "0e71e231",
          "a96af074",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 1041178
    },
    {
      "A1_A3": {
        "left": [
          "6586bdfc",
          "5a9a9d42",
          "9131f13f"
        ],
        "right": [
          "6586bdfc",
          "5a9a9d42",
          "9131f13f"
        ]
      },
      "E5_E7": {
        "left": [
          "58f38fac",
          "b3ffe5de",
          "87515160"
        ],
        "right": [
          "5caf87bc",
          "a3efcd4b",
          "a7505160"
        ]
      },
      "W9_W13": {
        "left": [
          "56e29c40",
          "0e63e231",
          "a95ce054",
          "45f2222c",
          "4d12f88a"
        ],
        "right": [
          "56e29c40",
          "0e63e231",
          "a95ce054",
          "41b22a2c",
          "6d12f88a"
        ]
      },
      "is_table3": false,
      "variant_id": 1042230
    }
  ]
}
```

## Appendix B: score-bearing construction and selected audit sources

The construction programs' local source dependencies are included in this appendix. Appendix A supplies their score-bearing JSON inputs. The scalar oracles are retained as audit sources; their historical pilot streams are not part of the charged finite algorithm. Each source block reports the digest of the displayed fence body and the digest of the exact source-file bytes. Every embedded source file has one final LF, which the fence uses as its delimiter; the appendix checker restores that LF and verifies both digests. Thus the bridge-stream audit and the repaired-cohort precommit identify the exact embedded source files even though their displayed-body digests differ. The fixed-slice 100-million precommit names the separate fixed-slice measurement source embedded below, not the repaired-cohort program.

### Backward reconstruction primitives

Embedded source SHA-256: `44240d0c44275d8c8cfb8afb709cb6fc7561cedea442045675c95292c83ace4b`.

Source-file SHA-256 after restoring the single final LF: `a8b0de41843bb320074375b5bb5e7ac0e66352b5da7b7fe2e2d7dc187fc5416a`.

```python
#!/usr/bin/env python3
"""Self-contained SHA-256 primitives for backward variant reconstruction.

This module contains exactly the constants, Figure 6 domains, and recurrence
functions consumed by backward_repair.py. It has no external filesystem input.
"""

from __future__ import annotations


MASK = 0xFFFFFFFF

K = (
    0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5,
    0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
    0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3,
    0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
    0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC,
    0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
    0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7,
    0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
    0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13,
    0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85,
    0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3,
    0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
    0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5,
    0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3,
    0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208,
    0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2,
)

A = tuple(int(value, 16) for value in """
66e7ba7c 5ff9d9f8 9123b13f b8560dbb 677e1e2a 9bcf7bbe f8677ad6
4a299906 44d24ab4 39781650 6c206d58 35c5c2b8 0508c8f0
""".split())
A_PRIME = tuple(int(value, 16) for value in """
66e7ba7c 5ff9d9f8 9123b13f 98560dbb 633b16ba 9bcf7bbe f8677ad6
4a299906 44f24ab5 39781650 6422edc8 574542b8 0508c8f0
""".split())
E = tuple(int(value, 16) for value in """
58f38fac b95f2294 87431160 11cae594 d504bf23 7f27d24c bf893f69
2300f189 fcc08ef5
""".split())
E_PRIME = tuple(int(value, 16) for value in """
5caf87bc a94f0a01 a7421160 f1cae594 d0e1b7b4 bf27d74c b78bbfd9
3fffd0f9 bf81c0f4
""".split())
W9 = tuple(int(value, 16) for value in
           "5100da8a 0912e57b a96b2054 45f2222c 4d12f88a".split())
W9_PRIME = tuple(int(value, 16) for value in
                 "5100da8a 0912e57b a96b2054 41b22a2c 6d12f88a".split())

# Backward-compatible names used by backward_repair.py.
AP = A_PRIME
EP = E_PRIME
W9P = W9_PRIME

EXPANSION_ROWS = {
    5: "01011u001n=nuu=11000n=1=101u=100",
    6: "101n=0=1=1=n1111==n0u===n=0n=n=u",
    7: "10u0=1=101==00=n==0=0===0==0=0=0",
}


def rotr(value: int, shift: int) -> int:
    return ((value >> shift) | (value << (32 - shift))) & MASK


def big0(value: int) -> int:
    return rotr(value, 2) ^ rotr(value, 13) ^ rotr(value, 22)


def big1(value: int) -> int:
    return rotr(value, 6) ^ rotr(value, 11) ^ rotr(value, 25)


def ch(x: int, y: int, z: int) -> int:
    return (x & y) ^ ((~x) & z)


def maj(x: int, y: int, z: int) -> int:
    return (x & y) ^ (x & z) ^ (y & z)


def bit(value: int, index: int) -> int:
    return (value >> index) & 1


def row_pair(row: str, assignment: int) -> tuple[int, int]:
    left = right = free_index = 0
    for offset, symbol in enumerate(row):
        index = 31 - offset
        if symbol == "=":
            value = (assignment >> free_index) & 1
            free_index += 1
            left |= value << index
            right |= value << index
        elif symbol == "1":
            left |= 1 << index
            right |= 1 << index
        elif symbol == "n":
            left |= 1 << index
        elif symbol == "u":
            right |= 1 << index
        elif symbol != "0":
            raise ValueError(f"invalid row symbol {symbol!r}")
    if assignment >= 1 << free_index:
        raise ValueError("assignment exceeds row freedom")
    return left, right


def row_values(row: str):
    for assignment in range(1 << row.count("=")):
        yield row_pair(row, assignment)


def row_ok(row: str, left: int, right: int) -> bool:
    for offset, symbol in enumerate(row):
        left_bit = bit(left, 31 - offset)
        right_bit = bit(right, 31 - offset)
        if symbol == "=" and left_bit != right_bit:
            return False
        if symbol == "0" and (left_bit != 0 or right_bit != 0):
            return False
        if symbol == "1" and (left_bit != 1 or right_bit != 1):
            return False
        if symbol == "n" and (left_bit != 1 or right_bit != 0):
            return False
        if symbol == "u" and (left_bit != 0 or right_bit != 1):
            return False
    return True


def e_relation(round_index: int, value: int, reading: str) -> bool:
    if round_index == 5:
        return bit(value, 3) == bit(value, 8) == bit(value, 21)
    if round_index == 6:
        unequal = zip((9, 27, 9, 8), (23, 14, 14, 27))
        equal = zip((1, 1, 23, 6), (6, 15, 10, 25))
        return (all(bit(value, a) != bit(value, b) for a, b in unequal) and
                all(bit(value, a) == bit(value, b) for a, b in equal))
    if round_index == 7:
        comparisons = tuple((bit(value, a), bit(value, b))
                            for a, b in zip((21, 10), (3, 15)))
        if reading == "equality":
            return all(left == right for left, right in comparisons)
        if reading == "printed_inequality":
            return all(left != right for left, right in comparisons)
    raise ValueError((round_index, reading))


def relation_values(reading: str) -> dict[int, tuple[tuple[int, int], ...]]:
    return {
        index: tuple(pair for pair in row_values(EXPANSION_ROWS[index])
                     if e_relation(index, pair[0], reading))
        for index in (5, 6, 7)
    }


def state_arrays(combo=None):
    left_e = {index: E[index - 5] for index in range(5, 14)}
    right_e = {index: E_PRIME[index - 5] for index in range(5, 14)}
    if combo is not None:
        for index, pair in zip((5, 6, 7), combo):
            left_e[index], right_e[index] = pair
    left_a = {index: A[index - 1] for index in range(1, 14)}
    right_a = {index: A_PRIME[index - 1] for index in range(1, 14)}
    return left_a, right_a, left_e, right_e


def predicted_a(index: int, a: dict[int, int], e: dict[int, int]) -> int:
    return (e[index] - a[index - 4] + big0(a[index - 1]) +
            maj(a[index - 1], a[index - 2], a[index - 3])) & MASK
```

### Backward state-consistent variant reconstruction

Embedded source SHA-256: `e2009fa626dcff6a567af61a3254aa27474a6b2d442fe3e6d625a9285e604c93`.

Source-file SHA-256 after restoring the single final LF: `2094808e63d16fa060bc9cc6007c2888267aad084d54e4ed779ab35ac8df9c28`.

```python
#!/usr/bin/env python3
"""Count and validate the backward A1..A3 repair of the Figure 6 table.

The E5/E6/E7 domain comes from the literal Figure 6 rows and the explicitly
selected E7 equality. A4..A13 and E8..E13 remain fixed to the
Table 3 trace.  For each branch, A3, A2, and A1 are derived backwards from
rounds 7, 6, and 5, respectively, and then checked by the forward recurrence.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
import shutil
import struct
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

import audit_table as source

HERE = Path(__file__).resolve().parent
MASK = 0xFFFFFFFF


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def previous_a(i: int, aa: dict[int, int], ee: dict[int, int]) -> int:
    """Return A_(i-4) from the A_i round identity."""
    return (ee[i] + source.big0(aa[i - 1])
            + source.maj(aa[i - 1], aa[i - 2], aa[i - 3])
            - aa[i]) & MASK


def derive_a1_a3(combo):
    aa, aap, ee, eep = source.state_arrays(combo)
    for i in (7, 6, 5):
        aa[i - 4] = previous_a(i, aa, ee)
        aap[i - 4] = previous_a(i, aap, eep)
    return aa, aap, ee, eep


def cross_state_failures(aa: dict[int, int]) -> list[str]:
    failures = []
    if source.bit(aa[3], 29) != source.bit(aa[2], 29):
        failures.append("A3[29]=A2[29]")
    if source.bit(aa[3], 29) == source.bit(aa[5], 29):
        failures.append("A3[29]!=A5[29]")
    for bit_index in (26, 4):
        if source.bit(aa[3], bit_index) != source.bit(aa[4], bit_index):
            failures.append(f"A3[{bit_index}]=A4[{bit_index}]")
    for bit_index in (22, 18, 16, 11, 7):
        if source.bit(aa[3], bit_index) == source.bit(aa[4], bit_index):
            failures.append(f"A3[{bit_index}]!=A4[{bit_index}]")
    return failures


def derive_w9_13(aa, aap, ee, eep):
    words, wordsp = [], []
    for i in range(9, 14):
        words.append((ee[i] - aa[i - 4] - ee[i - 4]
                      - source.big1(ee[i - 1])
                      - source.ch(ee[i - 1], ee[i - 2], ee[i - 3])
                      - source.K[i]) & MASK)
        wordsp.append((eep[i] - aap[i - 4] - eep[i - 4]
                       - source.big1(eep[i - 1])
                       - source.ch(eep[i - 1], eep[i - 2], eep[i - 3])
                       - source.K[i]) & MASK)
    return tuple(words), tuple(wordsp)


def differential_row(left: int, right: int) -> str:
    symbols = []
    for bit_index in range(31, -1, -1):
        left_bit = source.bit(left, bit_index)
        right_bit = source.bit(right, bit_index)
        symbols.append("=" if left_bit == right_bit
                       else ("n" if left_bit else "u"))
    return "".join(symbols)


W_ROWS = tuple(differential_row(left, right)
               for left, right in zip(source.W9, source.W9P))


def recurrence_failures(aa, aap, ee, eep, words, wordsp):
    failures = []
    for branch, branch_a, branch_e in (
            ("left", aa, ee), ("right", aap, eep)):
        for i in range(5, 14):
            if source.predicted_a(i, branch_a, branch_e) != branch_a[i]:
                failures.append(f"A_identity_{branch}_round_{i}")
    for branch, branch_a, branch_e, branch_words in (
            ("left", aa, ee, words),
            ("right", aap, eep, wordsp)):
        for i in range(9, 14):
            predicted_e = (branch_a[i - 4] + branch_e[i - 4]
                           + source.big1(branch_e[i - 1])
                           + source.ch(branch_e[i - 1], branch_e[i - 2],
                                       branch_e[i - 3])
                           + source.K[i] + branch_words[i - 9]) & MASK
            if predicted_e != branch_e[i]:
                failures.append(f"E_identity_{branch}_round_{i}")
    return failures


def full_variant_failures(combo, overridden_a3: int | None = None):
    aa, aap, ee, eep = derive_a1_a3(combo)
    if overridden_a3 is not None:
        aa[3] = overridden_a3
    failures = []
    for index in (1, 2, 3):
        if aa[index] != aap[index]:
            failures.append(f"A{index}_branch_equality")
    failures.extend(f"left_{item}" for item in cross_state_failures(aa))
    failures.extend(f"right_{item}" for item in cross_state_failures(aap))
    words, wordsp = derive_w9_13(aa, aap, ee, eep)
    for i, (left, right, row) in enumerate(zip(words, wordsp, W_ROWS), 9):
        if not source.row_ok(row, left, right):
            failures.append(f"W{i}_Figure6_row")
    failures.extend(recurrence_failures(aa, aap, ee, eep, words, wordsp))
    return failures


def describe_variant(cartesian_id, combo, aa, aap, words, wordsp):
    return {
        "cartesian_id": cartesian_id,
        "is_table3": combo == tuple(zip(source.E[:3], source.EP[:3])),
        "E5_E6_E7": [f"{left:08x}/{right:08x}" for left, right in combo],
        "derived_A1_A2_A3": [
            f"{aa[i]:08x}/{aap[i]:08x}" for i in (1, 2, 3)
        ],
        "W9_W13": [f"{value:08x}" for value in words],
        "W9p_W13p": [f"{value:08x}" for value in wordsp],
    }


def enumerate_backward_repair():
    values = source.relation_values("equality")
    stages = Counter()
    survivors = []
    first_cross_state_reject = None
    table3_combo = tuple(zip(source.E[:3], source.EP[:3]))

    for cartesian_id, combo in enumerate(
            itertools.product(values[5], values[6], values[7])):
        stages["E5_E6_E7_row_relation_cartesian"] += 1
        aa, aap, ee, eep = derive_a1_a3(combo)
        stages["A3_derived_both_branches"] += 1
        if aa[3] != aap[3]:
            continue
        stages["A3_branch_equality"] += 1
        if aa[2] != aap[2]:
            continue
        stages["A2_branch_equality"] += 1
        if aa[1] != aap[1]:
            continue
        stages["A1_branch_equality"] += 1

        left_cross = cross_state_failures(aa)
        right_cross = cross_state_failures(aap)
        if left_cross or right_cross:
            if first_cross_state_reject is None:
                words, wordsp = derive_w9_13(aa, aap, ee, eep)
                first_cross_state_reject = {
                    **describe_variant(cartesian_id, combo, aa, aap,
                                       words, wordsp),
                    "left_failures": left_cross,
                    "right_failures": right_cross,
                }
            continue
        stages["all_A3_A2_A4_A5_cross_state_relations_both_branches"] += 1

        words, wordsp = derive_w9_13(aa, aap, ee, eep)
        w_ok = True
        for i, (left, right, row) in enumerate(
                zip(words, wordsp, W_ROWS), 9):
            if not source.row_ok(row, left, right):
                w_ok = False
                break
            stages[f"W{i}_Figure6_row"] += 1
        if not w_ok:
            continue

        failures = recurrence_failures(aa, aap, ee, eep, words, wordsp)
        if failures:
            raise AssertionError(
                f"backward survivor {cartesian_id} failed recurrence: {failures}")
        stages["full_known_state_recurrence_both_branches"] += 1
        survivors.append(describe_variant(
            cartesian_id, combo, aa, aap, words, wordsp))

    if not any(item["is_table3"] for item in survivors):
        raise AssertionError("Table 3 is not a backward-repair survivor")
    return {
        "construction": (
            "retain A4..A13 and E8..E13; enumerate corrected-E7 "
            "E5/E6/E7; derive A3/A2/A1 backwards from rounds 7/6/5"
        ),
        "source_domain_sizes": {
            str(i): len(values[i]) for i in (5, 6, 7)
        },
        "cumulative_stage_counts": dict(stages),
        "eligible_variants": len(survivors),
        "table3_survivors": sum(item["is_table3"] for item in survivors),
        "non_table3_survivors": sum(not item["is_table3"]
                                    for item in survivors),
        "survivors": survivors,
        "first_branch_equal_but_cross_state_rejected": first_cross_state_reject,
    }


def run_named_control() -> int:
    combo = tuple(zip(source.E[:3], source.EP[:3]))
    aa, _, _, _ = derive_a1_a3(combo)
    failures = full_variant_failures(combo, overridden_a3=aa[3] ^ 1)
    name = "flip_derived_left_A3_bit0"
    expected = "A_identity_left_round_7"
    print(json.dumps({
        "control": name,
        "injected_change": "flip bit 0 of derived left-branch A3",
        "expected_failure": expected,
        "observed_failures": failures,
        "passed": expected in failures,
    }, sort_keys=True))
    return 23 if expected in failures else 1


def disposable_control():
    with tempfile.TemporaryDirectory(prefix="backward-repair-control-") as tmp:
        copied = Path(tmp)
        shutil.copy2(__file__, copied / Path(__file__).name)
        shutil.copy2(HERE / "audit_table.py", copied / "audit_table.py")
        result = subprocess.run(
            [sys.executable, str(copied / Path(__file__).name),
             "--named-control"],
            cwd=copied, text=True, capture_output=True, check=False)
    if result.returncode != 23:
        raise AssertionError(
            "named failing control did not fail as expected: "
            f"status={result.returncode} stdout={result.stdout!r} "
            f"stderr={result.stderr!r}")
    record = json.loads(result.stdout)
    if not record["passed"]:
        raise AssertionError(f"named control was not detected: {record}")
    record["disposable_copy_exit_status"] = result.returncode
    return record


def write_deterministic_sample(backward, path: Path):
    seed = 2026100505
    table3 = [item for item in backward["survivors"] if item["is_table3"]]
    non_table3 = [item for item in backward["survivors"]
                  if not item["is_table3"]]
    selected = random.Random(seed).sample(non_table3, 64) + table3
    selected.sort(key=lambda item: item["cartesian_id"])
    with path.open("wb") as stream:
        stream.write(b"BWR1")
        stream.write(struct.pack(">I", len(selected)))
        for item in selected:
            values = [item["cartesian_id"]]
            for pair in item["E5_E6_E7"]:
                values.extend(int(word, 16) for word in pair.split("/"))
            stream.write(struct.pack(">7I", *values))
    return {
        "seed": seed,
        "selection_rule": (
            "64 uniform variants without replacement from the 10,239 "
            "non-Table-3 survivors, plus the Table 3 control"
        ),
        "sample_size": len(selected),
        "non_table3_size": len(selected) - len(table3),
        "table3_controls": len(table3),
        "cartesian_ids": [item["cartesian_id"] for item in selected],
        "binary_path": path.name,
        "binary_sha256": sha256_file(path),
        "binary_format": (
            "BWR1, big-endian uint32 count, then count records of "
            "(cartesian_id,E5,E5p,E6,E6p,E7,E7p)"
        ),
    }


def write_all_survivors(backward, path: Path):
    selected = sorted(backward["survivors"],
                      key=lambda item: item["cartesian_id"])
    with path.open("wb") as stream:
        stream.write(b"BWR1")
        stream.write(struct.pack(">I", len(selected)))
        for item in selected:
            values = [item["cartesian_id"]]
            for pair in item["E5_E6_E7"]:
                values.extend(int(word, 16) for word in pair.split("/"))
            stream.write(struct.pack(">7I", *values))
    return {
        "variant_count": len(selected),
        "binary_path": path.name,
        "binary_sha256": sha256_file(path),
        "binary_format": (
            "BWR1, big-endian uint32 count, then count records of "
            "(cartesian_id,E5,E5p,E6,E6p,E7,E7p)"
        ),
    }


def write_sample_states(backward, sample, path: Path):
    wanted = set(sample["cartesian_ids"])
    selected = [item for item in backward["survivors"]
                if item["cartesian_id"] in wanted]
    selected.sort(key=lambda item: item["cartesian_id"])
    if len(selected) != sample["sample_size"]:
        raise AssertionError("sample state mapping cardinality mismatch")
    with path.open("wb") as stream:
        stream.write(b"RVS1")
        stream.write(struct.pack(">I", len(selected)))
        for item in selected:
            combo = tuple(tuple(int(word, 16) for word in pair.split("/"))
                          for pair in item["E5_E6_E7"])
            aa, aap, ee, eep = derive_a1_a3(combo)
            words, wordsp = derive_w9_13(aa, aap, ee, eep)
            values = ([item["cartesian_id"]]
                      + [aa[i] for i in range(1, 4)]
                      + [aap[i] for i in range(1, 4)]
                      + [ee[i] for i in range(5, 8)]
                      + [eep[i] for i in range(5, 8)]
                      + list(words) + list(wordsp))
            if len(values) != 23:
                raise AssertionError("variant state record must have 23 words")
            stream.write(struct.pack(">23I", *values))
    return {
        "variant_count": len(selected),
        "binary_path": path.name,
        "binary_sha256": sha256_file(path),
        "binary_format": (
            "RVS1, big-endian uint32 count, then 23 uint32 words per variant: "
            "variant_id; A1..A3 left/right; E5..E7 left/right; "
            "W9..W13 left/right"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=HERE / "backward-repair-measurements.json")
    parser.add_argument("--sample-binary", type=Path,
                        default=HERE / "backward-sample-variants.bin")
    parser.add_argument("--all-binary", type=Path,
                        default=HERE / "backward-all-variants.bin")
    parser.add_argument("--sample-states-binary", type=Path,
                        default=HERE / "repaired-variant-states.bin")
    parser.add_argument("--named-control", action="store_true")
    args = parser.parse_args()
    if args.named_control:
        raise SystemExit(run_named_control())

    backward = enumerate_backward_repair()
    sample = write_deterministic_sample(backward, args.sample_binary)
    all_survivors = write_all_survivors(backward, args.all_binary)
    sample_states = write_sample_states(
        backward, sample, args.sample_states_binary)
    result = {
        "experiment": "backward A1..A3 repaired Figure 6 table",
        "source": {
            "script_sha256": sha256_file(Path(__file__)),
            "construction_primitives_sha256":
                sha256_file(HERE / "audit_table.py"),
        },
        "equation": (
            "A_(i-4)=E_i+Sigma0(A_(i-1))"
            "+Maj(A_(i-1),A_(i-2),A_(i-3))-A_i mod 2^32"
        ),
        "figure6_constraints": {
            "A1_A2_A3_rows": "branch equality",
            "cross_state": [
                "A3[29]=A2[29]", "A3[29]!=A5[29]",
                "A3[26,4]=A4[26,4]",
                "A3[22,18,16,11,7]!=A4[22,18,16,11,7]",
            ],
            "enforced_on": "both branches",
        },
        "backward_repair": backward,
        "deterministic_shard_sample": sample,
        "all_survivors_binary": all_survivors,
        "sample_states_binary": sample_states,
        "checker_control": disposable_control(),
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "output": str(args.output),
        "eligible_variants": result["backward_repair"]["eligible_variants"],
        "non_table3_survivors":
            result["backward_repair"]["non_table3_survivors"],
        "control": result["checker_control"]["control"],
    }, indent=2))


if __name__ == "__main__":
    main()
```

### Repaired table enumeration

Embedded source SHA-256: `b92ad1d8a616d00da27f1cbf1e09a8ef1a2984c48912a1a9ca94c5339df94a64`.

Source-file SHA-256 after restoring the single final LF: `9c1c68c92399ee62c207fda429fa70d297d2ddf703446d301c6532ae602b52b8`.

```cpp
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>

using U = uint32_t;

static constexpr U K[14] = {
    0x428a2f98u, 0x71374491u, 0xb5c0fbcfu, 0xe9b5dba5u,
    0x3956c25bu, 0x59f111f1u, 0x923f82a4u, 0xab1c5ed5u,
    0xd807aa98u, 0x12835b01u, 0x243185beu, 0x550c7dc3u,
    0x72be5d74u, 0x80deb1feu};

static constexpr U A_FIXED[14] = {
    0, 0x66e7ba7cu, 0x5ff9d9f8u, 0x9123b13fu, 0xb8560dbbu,
    0x677e1e2au, 0x9bcf7bbeu, 0xf8677ad6u, 0x4a299906u,
    0x44d24ab4u, 0x39781650u, 0x6c206d58u, 0x35c5c2b8u,
    0x0508c8f0u};
static constexpr U AP_FIXED[14] = {
    0, 0x66e7ba7cu, 0x5ff9d9f8u, 0x9123b13fu, 0x98560dbbu,
    0x633b16bau, 0x9bcf7bbeu, 0xf8677ad6u, 0x4a299906u,
    0x44f24ab5u, 0x39781650u, 0x6422edc8u, 0x574542b8u,
    0x0508c8f0u};
static constexpr U E_FIXED[14] = {
    0, 0, 0, 0, 0, 0x58f38facu, 0xb95f2294u, 0x87431160u,
    0x11cae594u, 0xd504bf23u, 0x7f27d24cu, 0xbf893f69u,
    0x2300f189u, 0xfcc08ef5u};
static constexpr U EP_FIXED[14] = {
    0, 0, 0, 0, 0, 0x5caf87bcu, 0xa94f0a01u, 0xa7421160u,
    0xf1cae594u, 0xd0e1b7b4u, 0xbf27d74cu, 0xb78bbfd9u,
    0x3fffd0f9u, 0xbf81c0f4u};

static const std::string ROW_E5 = "01011u001n=nuu=11000n=1=101u=100";
static const std::string ROW_E6 = "101n=0=1=1=n1111==n0u===n=0n=n=u";
static const std::string ROW_E7 = "10u0=1=101==00=n==0=0===0==0=0=0";
static const std::string ROW_E4 = "==n0=0=1===100=0==0=1===0==1=0=1";
static const std::string ROW_E3 = "=====1=====011======0======0====";
static const std::string ROW_W7 = "=======n=======u===u====u=1=u=u=";
static const std::string ROW_W8 = "============u=======uu==========";
static const std::array<std::string, 5> ROW_W9_13 = {
    "================================", "================================",
    "================================", "=====n===n==========u===========",
    "==u============================="};

struct Pair { U x, y; };
struct Input { U cartesian_id; Pair e5, e6, e7; };
struct State {
  U a[14]{}, ap[14]{}, e[14]{}, ep[14]{};
  U w[14]{}, wp[14]{};
};
struct Record { U key, w7, w8, e3, e4, a0; };
struct PackedRecord { U key, variant_id, w7, w8, e3, e4, a0; };

static inline U rotr(U x, unsigned n) {
  return (x >> n) | (x << (32 - n));
}
static inline U S0(U x) { return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22); }
static inline U S1(U x) { return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25); }
static inline U Ch(U x, U y, U z) { return (x & y) ^ (~x & z); }
static inline U Maj(U x, U y, U z) {
  return (x & y) ^ (x & z) ^ (y & z);
}
static inline unsigned bit(U x, unsigned i) { return (x >> i) & 1u; }

static bool row_ok(const std::string &row, U x, U y) {
  if (row.size() != 32) return false;
  for (unsigned off = 0; off < 32; ++off) {
    const unsigned b = 31 - off, xb = bit(x, b), yb = bit(y, b);
    const char symbol = row[off];
    if (symbol == '=' && xb != yb) return false;
    if (symbol == '0' && (xb || yb)) return false;
    if (symbol == '1' && (!xb || !yb)) return false;
    if (symbol == 'n' && (xb != 1 || yb != 0)) return false;
    if (symbol == 'u' && (xb != 0 || yb != 1)) return false;
  }
  return true;
}

static bool rel_e5(U x) {
  return bit(x, 3) == bit(x, 8) && bit(x, 21) == bit(x, 8);
}
static bool rel_e6(U x) {
  return bit(x, 9) != bit(x, 23) && bit(x, 27) != bit(x, 14) &&
         bit(x, 9) != bit(x, 14) && bit(x, 8) != bit(x, 27) &&
         bit(x, 1) == bit(x, 6) && bit(x, 1) == bit(x, 15) &&
         bit(x, 23) == bit(x, 10) && bit(x, 6) == bit(x, 25);
}
static bool rel_e7(U x) {
  return bit(x, 21) == bit(x, 3) && bit(x, 10) == bit(x, 15);
}
static bool rel_e4(U x) { return bit(x, 10) != bit(x, 15); }
static bool rel_w7(U x) {
  return bit(x, 22) != bit(x, 18) && bit(x, 13) != bit(x, 9) &&
         bit(x, 23) != bit(x, 8) && bit(x, 11) == bit(x, 22) &&
         bit(x, 14) == bit(x, 31) && bit(x, 20) == bit(x, 31);
}
static bool rel_w8(U x) {
  return bit(x, 0) == bit(x, 28) && bit(x, 14) == bit(x, 25) &&
         bit(x, 21) == bit(x, 6) && bit(x, 31) != bit(x, 27) &&
         bit(x, 23) != bit(x, 2) && bit(x, 30) != bit(x, 15) &&
         bit(x, 15) != bit(x, 26) && bit(x, 22) != bit(x, 7) &&
         bit(x, 8) != bit(x, 4);
}

static std::vector<Pair> row_values(const std::string &row,
                                    bool (*relation)(U)) {
  std::vector<unsigned> free_bits;
  U left = 0, right = 0;
  for (unsigned off = 0; off < 32; ++off) {
    const unsigned b = 31 - off;
    const char symbol = row[off];
    if (symbol == '=') free_bits.push_back(b);
    else if (symbol == '1') left |= 1u << b, right |= 1u << b;
    else if (symbol == 'n') left |= 1u << b;
    else if (symbol == 'u') right |= 1u << b;
    else if (symbol != '0') throw std::runtime_error("bad row symbol");
  }
  std::vector<Pair> result;
  const uint64_t limit = 1ull << free_bits.size();
  for (uint64_t assignment = 0; assignment < limit; ++assignment) {
    U x = left, y = right;
    for (size_t j = 0; j < free_bits.size(); ++j) {
      if ((assignment >> j) & 1ull) {
        x |= 1u << free_bits[j];
        y |= 1u << free_bits[j];
      }
    }
    if (relation(x)) result.push_back({x, y});
  }
  return result;
}

static U read_u32(std::istream &stream) {
  unsigned char bytes[4];
  if (!stream.read(reinterpret_cast<char *>(bytes), 4))
    throw std::runtime_error("short input");
  return (U(bytes[0]) << 24) | (U(bytes[1]) << 16) |
         (U(bytes[2]) << 8) | U(bytes[3]);
}

static void write_u32(std::ostream &stream, U value) {
  const unsigned char bytes[4] = {
      static_cast<unsigned char>(value >> 24),
      static_cast<unsigned char>(value >> 16),
      static_cast<unsigned char>(value >> 8),
      static_cast<unsigned char>(value)};
  stream.write(reinterpret_cast<const char *>(bytes), 4);
}

static void write_u64(std::ostream &stream, uint64_t value) {
  write_u32(stream, static_cast<U>(value >> 32));
  write_u32(stream, static_cast<U>(value));
}

static std::vector<Input> read_inputs(const char *path) {
  std::ifstream stream(path, std::ios::binary);
  if (!stream) throw std::runtime_error("cannot open input");
  char magic[4];
  if (!stream.read(magic, 4) || std::string(magic, 4) != "BWR1")
    throw std::runtime_error("bad input magic");
  const U count = read_u32(stream);
  std::vector<Input> result;
  result.reserve(count);
  for (U i = 0; i < count; ++i) {
    Input item{};
    item.cartesian_id = read_u32(stream);
    item.e5 = {read_u32(stream), read_u32(stream)};
    item.e6 = {read_u32(stream), read_u32(stream)};
    item.e7 = {read_u32(stream), read_u32(stream)};
    result.push_back(item);
  }
  if (stream.peek() != EOF) throw std::runtime_error("trailing input bytes");
  return result;
}

static U previous_a(int i, const U *a, const U *e) {
  return e[i] + S0(a[i - 1]) + Maj(a[i - 1], a[i - 2], a[i - 3]) - a[i];
}

static State derive_state(const Input &input) {
  State state;
  for (int i = 4; i < 14; ++i) {
    state.a[i] = A_FIXED[i]; state.ap[i] = AP_FIXED[i];
  }
  for (int i = 8; i < 14; ++i) {
    state.e[i] = E_FIXED[i]; state.ep[i] = EP_FIXED[i];
  }
  state.e[5] = input.e5.x; state.ep[5] = input.e5.y;
  state.e[6] = input.e6.x; state.ep[6] = input.e6.y;
  state.e[7] = input.e7.x; state.ep[7] = input.e7.y;
  for (int i : {7, 6, 5}) {
    state.a[i - 4] = previous_a(i, state.a, state.e);
    state.ap[i - 4] = previous_a(i, state.ap, state.ep);
  }
  for (int i = 9; i < 14; ++i) {
    state.w[i] = state.e[i] - state.a[i - 4] - state.e[i - 4]
        - S1(state.e[i - 1])
        - Ch(state.e[i - 1], state.e[i - 2], state.e[i - 3]) - K[i];
    state.wp[i] = state.ep[i] - state.ap[i - 4] - state.ep[i - 4]
        - S1(state.ep[i - 1])
        - Ch(state.ep[i - 1], state.ep[i - 2], state.ep[i - 3]) - K[i];
  }
  return state;
}

static bool cross_ok(const U *a) {
  if (bit(a[3], 29) != bit(a[2], 29)) return false;
  if (bit(a[3], 29) == bit(a[5], 29)) return false;
  for (unsigned b : {26u, 4u})
    if (bit(a[3], b) != bit(a[4], b)) return false;
  for (unsigned b : {22u, 18u, 16u, 11u, 7u})
    if (bit(a[3], b) == bit(a[4], b)) return false;
  return true;
}

static std::string validate_state(const Input &input, const State &state) {
  if (!row_ok(ROW_E5, input.e5.x, input.e5.y) || !rel_e5(input.e5.x))
    return "E5_source_domain";
  if (!row_ok(ROW_E6, input.e6.x, input.e6.y) || !rel_e6(input.e6.x))
    return "E6_source_domain";
  if (!row_ok(ROW_E7, input.e7.x, input.e7.y) || !rel_e7(input.e7.x))
    return "E7_source_domain";
  for (int i = 1; i <= 3; ++i)
    if (state.a[i] != state.ap[i]) return "A1_A3_branch_equality";
  if (!cross_ok(state.a) || !cross_ok(state.ap))
    return "A3_cross_state_relations";
  for (int i = 5; i < 14; ++i) {
    U got = state.e[i] - state.a[i - 4] + S0(state.a[i - 1])
          + Maj(state.a[i - 1], state.a[i - 2], state.a[i - 3]);
    U gotp = state.ep[i] - state.ap[i - 4] + S0(state.ap[i - 1])
           + Maj(state.ap[i - 1], state.ap[i - 2], state.ap[i - 3]);
    if (got != state.a[i]) return "A_identity_left_round_" + std::to_string(i);
    if (gotp != state.ap[i]) return "A_identity_right_round_" + std::to_string(i);
  }
  for (int i = 9; i < 14; ++i) {
    if (!row_ok(ROW_W9_13[i - 9], state.w[i], state.wp[i]))
      return "W_Figure6_row_" + std::to_string(i);
    U got = state.a[i - 4] + state.e[i - 4] + S1(state.e[i - 1])
          + Ch(state.e[i - 1], state.e[i - 2], state.e[i - 3])
          + K[i] + state.w[i];
    U gotp = state.ap[i - 4] + state.ep[i - 4] + S1(state.ep[i - 1])
           + Ch(state.ep[i - 1], state.ep[i - 2], state.ep[i - 3])
           + K[i] + state.wp[i];
    if (got != state.e[i]) return "E_identity_left_round_" + std::to_string(i);
    if (gotp != state.ep[i]) return "E_identity_right_round_" + std::to_string(i);
  }
  return "";
}

static void emit_hex(U value) {
  static const char digits[] = "0123456789abcdef";
  char out[9];
  for (int i = 0; i < 8; ++i)
    out[i] = digits[(value >> (28 - 4 * i)) & 15];
  out[8] = 0;
  std::cout << '"' << out << '"';
}

static void emit_histogram(const std::map<uint64_t, uint64_t> &histogram) {
  std::cout << '{';
  bool first = true;
  for (const auto &[multiplicity, keys] : histogram) {
    if (!first) std::cout << ',';
    std::cout << '"' << multiplicity << "\":" << keys;
    first = false;
  }
  std::cout << '}';
}

static std::map<uint64_t, uint64_t>
multiplicity_histogram(std::vector<U> &keys, uint64_t &distinct,
                       uint64_t &maximum) {
  std::sort(keys.begin(), keys.end());
  std::map<uint64_t, uint64_t> histogram;
  distinct = maximum = 0;
  for (size_t begin = 0; begin < keys.size();) {
    size_t end = begin + 1;
    while (end < keys.size() && keys[end] == keys[begin]) ++end;
    const uint64_t count = end - begin;
    ++distinct;
    ++histogram[count];
    maximum = std::max(maximum, count);
    begin = end;
  }
  return histogram;
}

static int named_control() {
  Input table3{919338u,
      {E_FIXED[5], EP_FIXED[5]}, {E_FIXED[6], EP_FIXED[6]},
      {E_FIXED[7], EP_FIXED[7]}};
  State state = derive_state(table3);
  state.a[3] ^= 1u;
  const std::string failure = validate_state(table3, state);
  const bool passed = failure == "A1_A3_branch_equality";
  std::cout << "{\"control\":\"flip_derived_left_A3_bit0\","
            << "\"expected_failure\":\"A1_A3_branch_equality\","
            << "\"observed_failure\":\"" << failure << "\","
            << "\"passed\":" << (passed ? "true" : "false") << "}\n";
  return passed ? 23 : 1;
}

int main(int argc, char **argv) {
  if (argc == 2 && std::string(argv[1]) == "--named-control")
    return named_control();
  const bool count_only = argc == 3 && std::string(argv[1]) == "--count-only";
  const bool pack_mode = argc == 4 && std::string(argv[1]) == "--pack";
  if ((!count_only && !pack_mode && argc != 2) ||
      (count_only && argc != 3) || (pack_mode && argc != 4)) {
    std::cerr << "usage: repaired_table_sample [--count-only] variants.bin\n"
              << "       repaired_table_sample --pack output.bin variants.bin\n";
    return 2;
  }
  try {
    const auto inputs = read_inputs(argv[count_only ? 2 : (pack_mode ? 3 : 1)]);
    const auto w7s = row_values(ROW_W7, rel_w7);
    const auto w8s = row_values(ROW_W8, rel_w8);
    if (w7s.size() != 524288 || w8s.size() != 1048576)
      throw std::runtime_error("W7/W8 source cardinality mismatch");

    std::vector<U> all_keys;
    std::vector<PackedRecord> packed_records;
    uint64_t total_records = 0, nonzero = 0, table3_records = 0;
    for (const Input &input : inputs) {
      const State state = derive_state(input);
      const std::string failure = validate_state(input, state);
      if (!failure.empty()) throw std::runtime_error(
          "variant " + std::to_string(input.cartesian_id) + ": " + failure);

      uint64_t e4_row = 0, e4_relation = 0, a0_equal = 0;
      uint64_t w7_examined = 0, e3_row = 0, key_equal = 0;
      std::vector<Record> records;
      Record representative{};
      bool have_representative = false;
      for (const Pair &p8 : w8s) {
        U e4 = state.e[8] - state.a[4] - S1(state.e[7])
              - Ch(state.e[7], state.e[6], state.e[5]) - K[8] - p8.x;
        U e4p = state.ep[8] - state.ap[4] - S1(state.ep[7])
               - Ch(state.ep[7], state.ep[6], state.ep[5]) - K[8] - p8.y;
        if (!row_ok(ROW_E4, e4, e4p)) continue;
        ++e4_row;
        if (!rel_e4(e4)) continue;
        ++e4_relation;
        U a0 = e4 + S0(state.a[3])
               + Maj(state.a[3], state.a[2], state.a[1]) - state.a[4];
        U a0p = e4p + S0(state.ap[3])
                + Maj(state.ap[3], state.ap[2], state.ap[1]) - state.ap[4];
        if (a0 != a0p) continue;
        ++a0_equal;
        for (const Pair &p7 : w7s) {
          ++w7_examined;
          U e3 = state.e[7] - state.a[3] - S1(state.e[6])
                 - Ch(state.e[6], state.e[5], e4) - K[7] - p7.x;
          U e3p = state.ep[7] - state.ap[3] - S1(state.ep[6])
                  - Ch(state.ep[6], state.ep[5], e4p) - K[7] - p7.y;
          if (!row_ok(ROW_E3, e3, e3p)) continue;
          ++e3_row;
          U key = e3 + S0(state.a[2])
                  + Maj(state.a[2], state.a[1], a0) - state.a[3];
          U keyp = e3p + S0(state.ap[2])
                   + Maj(state.ap[2], state.ap[1], a0p) - state.ap[3];
          if (key != keyp) continue;
          ++key_equal;
          Record record{key, p7.x, p8.x, e3, e4, a0};
          if (!have_representative) {
            representative = record;
            have_representative = true;
          }
          if (!count_only) {
            records.push_back(record);
            if (!pack_mode) all_keys.push_back(key);
          }
        }
      }
      std::vector<U> variant_keys;
      uint64_t distinct = 0, maximum = 0;
      std::map<uint64_t, uint64_t> histogram;
      if (!count_only) {
        std::sort(records.begin(), records.end(), [](const Record &x,
                                                      const Record &y) {
          return std::tie(x.key, x.w7, x.w8, x.e3, x.e4, x.a0) <
                 std::tie(y.key, y.w7, y.w8, y.e3, y.e4, y.a0);
        });
        variant_keys.reserve(records.size());
        for (const Record &record : records) variant_keys.push_back(record.key);
        histogram = multiplicity_histogram(variant_keys, distinct, maximum);
        if (!records.empty()) representative = records.front();
        if (pack_mode) {
          packed_records.reserve(packed_records.size() + records.size());
          for (const Record &record : records) {
            packed_records.push_back({record.key, input.cartesian_id,
                                      record.w7, record.w8, record.e3,
                                      record.e4, record.a0});
          }
        }
      }
      total_records += key_equal;
      if (key_equal) ++nonzero;
      if (input.cartesian_id == 919338u) table3_records = key_equal;

      std::cout << "{\"type\":\"variant\",\"cartesian_id\":"
                << input.cartesian_id << ",\"A1_A2_A3\":[";
      for (int i = 1; i <= 3; ++i) {
        if (i != 1) std::cout << ',';
        emit_hex(state.a[i]);
      }
      std::cout << "],\"E5_E6_E7\":[";
      for (int i = 5; i <= 7; ++i) {
        if (i != 5) std::cout << ',';
        emit_hex(state.e[i]);
      }
      std::cout << "],\"W9_W13\":[";
      for (int i = 9; i <= 13; ++i) {
        if (i != 9) std::cout << ',';
        emit_hex(state.w[i]);
      }
      std::cout << "],\"W8_scan_candidates\":" << w8s.size()
                << ",\"E4_row\":" << e4_row
                << ",\"E4_relation\":" << e4_relation
                << ",\"A0_equal\":" << a0_equal
                << ",\"W7_scan_candidates\":" << w7_examined
                << ",\"E3_row\":" << e3_row
                << ",\"Aminus1_equal\":" << key_equal
                << ",\"records\":" << key_equal
                << ",\"distinct_keys\":";
      if (count_only) std::cout << "null"; else std::cout << distinct;
      std::cout << ",\"max_multiplicity\":";
      if (count_only) std::cout << "null"; else std::cout << maximum;
      std::cout << ",\"multiplicity_histogram\":";
      if (count_only) std::cout << "null"; else emit_histogram(histogram);
      std::cout << ",\"representative_record\":";
      if (!have_representative) {
        std::cout << "null";
      } else {
        const Record &record = representative;
        std::cout << '[';
        const U values[] = {record.key, record.w7, record.w8, record.e3,
                            record.e4, record.a0};
        for (int i = 0; i < 6; ++i) {
          if (i) std::cout << ',';
          emit_hex(values[i]);
        }
        std::cout << ']';
      }
      std::cout << "}\n";
    }

    uint64_t distinct = 0, maximum = 0;
    std::map<uint64_t, uint64_t> histogram;
    if (!count_only && !pack_mode)
      histogram = multiplicity_histogram(all_keys, distinct, maximum);
    if (pack_mode) {
      std::sort(packed_records.begin(), packed_records.end(),
                [](const PackedRecord &x, const PackedRecord &y) {
        return std::tie(x.key, x.variant_id, x.w7, x.w8, x.e3, x.e4, x.a0) <
               std::tie(y.key, y.variant_id, y.w7, y.w8, y.e3, y.e4, y.a0);
      });
      std::ofstream stream(argv[2], std::ios::binary);
      if (!stream) throw std::runtime_error("cannot create packed output");
      stream.write("RPT1", 4);
      write_u32(stream, 28);
      write_u64(stream, packed_records.size());
      U prior = 0;
      uint64_t current = 0;
      bool have_prior = false;
      for (const PackedRecord &record : packed_records) {
        if (!have_prior || record.key != prior) {
          if (have_prior) {
            ++histogram[current];
            maximum = std::max(maximum, current);
          }
          ++distinct;
          prior = record.key;
          current = 0;
          have_prior = true;
        }
        ++current;
        for (U value : {record.key, record.variant_id, record.w7, record.w8,
                        record.e3, record.e4, record.a0})
          write_u32(stream, value);
      }
      if (have_prior) {
        ++histogram[current];
        maximum = std::max(maximum, current);
      }
      stream.close();
      if (!stream) throw std::runtime_error("packed output write failed");
    }
    std::cout << "{\"type\":\"summary\",\"sample_variants\":"
              << inputs.size() << ",\"nonzero_variants\":" << nonzero
              << ",\"records\":" << total_records
              << ",\"count_only\":" << (count_only ? "true" : "false")
              << ",\"pack_mode\":" << (pack_mode ? "true" : "false")
              << ",\"distinct_keys_across_sample\":";
    if (count_only) std::cout << "null"; else std::cout << distinct;
    std::cout << ",\"max_multiplicity_across_sample\":";
    if (count_only) std::cout << "null"; else std::cout << maximum;
    std::cout
              << ",\"multiplicity_histogram_across_sample\":";
    if (count_only) std::cout << "null"; else emit_histogram(histogram);
    std::cout << ",\"table3_records\":" << table3_records;
    if (pack_mode)
      std::cout << ",\"packed_record_file\":\"" << argv[2]
                << "\",\"packed_record_bytes\":"
                << (16ull + packed_records.size() * 28ull);
    std::cout << "}\n";
  } catch (const std::exception &error) {
    std::cerr << "ERROR: " << error.what() << '\n';
    return 1;
  }
  return 0;
}
```

### Canonical repaired bridge sampler

Embedded source SHA-256: `20a8a98c3df6c5ba65dcf408910ada643549076b03d9b16d3f89c9bf466f8303`.

Source-file SHA-256 after restoring the single final LF: `915cf93ba9080c6366e0743b12228b65c8378516180a134eacad9bfd30abe01b`.

```cpp
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_map>
#include <vector>

using U = uint32_t;
using Q = uint64_t;

static constexpr U K[32] = {
    0x428a2f98u, 0x71374491u, 0xb5c0fbcfu, 0xe9b5dba5u,
    0x3956c25bu, 0x59f111f1u, 0x923f82a4u, 0xab1c5ed5u,
    0xd807aa98u, 0x12835b01u, 0x243185beu, 0x550c7dc3u,
    0x72be5d74u, 0x80deb1feu, 0x9bdc06a7u, 0xc19bf174u,
    0xe49b69c1u, 0xefbe4786u, 0x0fc19dc6u, 0x240ca1ccu,
    0x2de92c6fu, 0x4a7484aau, 0x5cb0a9dcu, 0x76f988dau,
    0x983e5152u, 0xa831c66du, 0xb00327c8u, 0xbf597fc7u,
    0xc6e00bf3u, 0xd5a79147u, 0x06ca6351u, 0x14292967u};

static constexpr U IV[8] = {
    0x6a09e667u, 0xbb67ae85u, 0x3c6ef372u, 0xa54ff53au,
    0x510e527fu, 0x9b05688cu, 0x1f83d9abu, 0x5be0cd19u};

// A4..A13 and E8..E13 are common to every repaired variant.
static constexpr U A_COMMON[2][10] = {
    {0xb8560dbbu, 0x677e1e2au, 0x9bcf7bbeu, 0xf8677ad6u,
     0x4a299906u, 0x44d24ab4u, 0x39781650u, 0x6c206d58u,
     0x35c5c2b8u, 0x0508c8f0u},
    {0x98560dbbu, 0x633b16bau, 0x9bcf7bbeu, 0xf8677ad6u,
     0x4a299906u, 0x44f24ab5u, 0x39781650u, 0x6422edc8u,
     0x574542b8u, 0x0508c8f0u}};
static constexpr U E_COMMON[2][6] = {
    {0x11cae594u, 0xd504bf23u, 0x7f27d24cu,
     0xbf893f69u, 0x2300f189u, 0xfcc08ef5u},
    {0xf1cae594u, 0xd0e1b7b4u, 0xbf27d74cu,
     0xb78bbfd9u, 0x3fffd0f9u, 0xbf81c0f4u}};

static inline U rr(U x, unsigned n) { return (x >> n) | (x << (32 - n)); }
static inline U s0(U x) { return rr(x, 2) ^ rr(x, 13) ^ rr(x, 22); }
static inline U s1(U x) { return rr(x, 6) ^ rr(x, 11) ^ rr(x, 25); }
static inline U l0(U x) { return rr(x, 7) ^ rr(x, 18) ^ (x >> 3); }
static inline U l1(U x) { return rr(x, 17) ^ rr(x, 19) ^ (x >> 10); }
static inline U ch(U x, U y, U z) { return z ^ (x & (y ^ z)); }
static inline U maj(U x, U y, U z) { return (x & y) | (z & (x | y)); }
static inline unsigned bit(U x, unsigned b) { return (x >> b) & 1u; }

static U read_u32(std::istream &stream) {
  unsigned char bytes[4];
  if (!stream.read(reinterpret_cast<char *>(bytes), 4))
    throw std::runtime_error("short input");
  return (U(bytes[0]) << 24) | (U(bytes[1]) << 16) |
         (U(bytes[2]) << 8) | U(bytes[3]);
}

static Q read_u64(std::istream &stream) {
  return (Q(read_u32(stream)) << 32) | read_u32(stream);
}

static void c32(const U *input, const U *block, U *cv) {
  U w[32];
  std::copy(block, block + 16, w);
  for (unsigned i = 16; i < 32; ++i)
    w[i] = l1(w[i - 2]) + w[i - 7] + l0(w[i - 15]) + w[i - 16];
  U a = input[0], b = input[1], c = input[2], d = input[3];
  U e = input[4], f = input[5], g = input[6], h = input[7];
  for (unsigned i = 0; i < 32; ++i) {
    U t1 = h + s1(e) + ch(e, f, g) + K[i] + w[i];
    U t2 = s0(a) + maj(a, b, c);
    h = g; g = f; f = e; e = d + t1;
    d = c; c = b; b = a; a = t1 + t2;
  }
  const U result[8] = {a, b, c, d, e, f, g, h};
  for (unsigned i = 0; i < 8; ++i) cv[i] = input[i] + result[i];
}

struct Record {
  U key, variant_id, w7, w8, e3, e4, a0;
};

struct Variant {
  U id;
  U a[2][3];
  U e[2][3];
  U w[2][5];
};

static Q rotl(Q x, unsigned k) { return (x << k) | (x >> (64 - k)); }

struct RNG {
  Q state[4];
  explicit RNG(Q seed) {
    for (Q &word : state) {
      seed += 0x9e3779b97f4a7c15ULL;
      Q z = seed;
      z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
      z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
      word = z ^ (z >> 31);
    }
  }
  Q next() {
    Q result = rotl(state[1] * 5, 7) * 9;
    Q temporary = state[1] << 17;
    state[2] ^= state[0]; state[3] ^= state[1];
    state[1] ^= state[2]; state[0] ^= state[3];
    state[2] ^= temporary; state[3] = rotl(state[3], 45);
    return result;
  }
  Q below(Q n) {
    Q value, threshold = -n % n;
    do value = next(); while (value < threshold);
    return value % n;
  }
};

static bool row(U x, U y, U xor_mask, U ones, U zeros) {
  return (x ^ y) == xor_mask && (x & ones) == ones && !(x & zeros);
}

static bool bridge(const U *cv, const Record &record, const Variant &variant,
                   Q *stages) {
  U words[2][7];
  for (unsigned branch = 0; branch < 2; ++branch) {
    U a_buffer[18]{}, e_buffer[18]{};
    U *a = a_buffer + 4, *e = e_buffer + 4;
    for (int i = -4; i < 0; ++i) {
      a[i] = cv[-1 - i];
      e[i] = cv[3 - i];
    }
    std::copy(variant.a[branch], variant.a[branch] + 3, a + 1);
    std::copy(A_COMMON[branch], A_COMMON[branch] + 10, a + 4);
    std::copy(variant.e[branch], variant.e[branch] + 3, e + 5);
    std::copy(E_COMMON[branch], E_COMMON[branch] + 6, e + 8);
    a[0] = record.a0;
    e[3] = record.e3;
    e[4] = record.e4 ^ (branch ? 0x20000000u : 0u);
    e[2] = a[2] + a[-2] - s0(a[1]) - maj(a[1], a[0], a[-1]);
    e[1] = a[1] + a[-3] - s0(a[0]) - maj(a[0], a[-1], a[-2]);
    e[0] = a[0] + a[-4] - s0(a[-1]) - maj(a[-1], a[-2], a[-3]);
    for (unsigned i = 0; i < 7; ++i) {
      int j = static_cast<int>(i);
      words[branch][i] = e[j] - a[j - 4] - e[j - 4]
          - s1(e[j - 1]) - ch(e[j - 1], e[j - 2], e[j - 3]) - K[i];
    }
  }
  for (unsigned i = 0; i < 4; ++i)
    if (words[0][i] != words[1][i]) return false;
  ++stages[0];
  U x = words[0][4];
  if (!row(x, words[1][4], 0x20000000u, 0x20000000u, 0u)) return false;
  ++stages[1];
  if (bit(x, 1) == bit(x, 12) || bit(x, 8) == bit(x, 25) ||
      bit(x, 18) != bit(x, 14)) return false;
  ++stages[2];
  x = words[0][5];
  if (!row(x, words[1][5], 0x04400800u, 0x00000800u, 0x04400000u))
    return false;
  ++stages[3];
  if (bit(x, 0) != bit(x, 28) || bit(x, 1) != bit(x, 18) ||
      bit(x, 30) != bit(x, 9)) return false;
  ++stages[4];
  x = words[0][6];
  if (!row(x, words[1][6], 0x20000000u, 0x20000000u, 0u)) return false;
  ++stages[5];
  if (bit(x, 1) != bit(x, 12) || bit(x, 8) != bit(x, 25) ||
      bit(x, 18) == bit(x, 14)) return false;
  ++stages[6];
  return true;
}

static std::vector<Variant> read_variants(const char *path) {
  std::ifstream stream(path, std::ios::binary);
  if (!stream) throw std::runtime_error("cannot open variant state file");
  char magic[4];
  if (!stream.read(magic, 4) || std::string(magic, 4) != "RVS1")
    throw std::runtime_error("bad variant state magic");
  const U count = read_u32(stream);
  std::vector<Variant> variants;
  variants.reserve(count);
  for (U index = 0; index < count; ++index) {
    Variant variant{};
    variant.id = read_u32(stream);
    for (unsigned branch = 0; branch < 2; ++branch)
      for (U &word : variant.a[branch]) word = read_u32(stream);
    for (unsigned branch = 0; branch < 2; ++branch)
      for (U &word : variant.e[branch]) word = read_u32(stream);
    for (unsigned branch = 0; branch < 2; ++branch)
      for (U &word : variant.w[branch]) word = read_u32(stream);
    if (!variants.empty() && variants.back().id >= variant.id)
      throw std::runtime_error("variant states not strictly ordered");
    variants.push_back(variant);
  }
  if (stream.peek() != EOF) throw std::runtime_error("trailing variant bytes");
  return variants;
}

static std::vector<Record> read_records(const char *path, Q &declared_count) {
  std::ifstream stream(path, std::ios::binary);
  if (!stream) throw std::runtime_error("cannot open repaired table");
  char magic[4];
  if (!stream.read(magic, 4) || std::string(magic, 4) != "RPT1")
    throw std::runtime_error("bad repaired table magic");
  if (read_u32(stream) != 28) throw std::runtime_error("bad record size");
  declared_count = read_u64(stream);
  std::vector<Record> records;
  records.reserve(declared_count);
  for (Q index = 0; index < declared_count; ++index) {
    Record record{};
    record.key = read_u32(stream); record.variant_id = read_u32(stream);
    record.w7 = read_u32(stream); record.w8 = read_u32(stream);
    record.e3 = read_u32(stream); record.e4 = read_u32(stream);
    record.a0 = read_u32(stream);
    if (!records.empty()) {
      const Record &prior = records.back();
      if (std::tie(record.key, record.variant_id, record.w7, record.w8,
                   record.e3, record.e4, record.a0) <=
          std::tie(prior.key, prior.variant_id, prior.w7, prior.w8,
                   prior.e3, prior.e4, prior.a0))
        throw std::runtime_error("repaired table not strictly canonical");
    }
    records.push_back(record);
  }
  if (stream.peek() != EOF) throw std::runtime_error("trailing table bytes");
  return records;
}

static void hex_words(const U *words, size_t count) {
  std::cout << '"';
  for (size_t i = 0; i < count; ++i)
    std::cout << std::hex << std::setw(8) << std::setfill('0') << words[i];
  std::cout << '"' << std::dec;
}

int main(int argc, char **argv) {
  if (argc != 6) {
    std::cerr << "usage: repaired_bridge_sample table.bin states.bin trials seed c32|conditional\n";
    return 2;
  }
  try {
    Q declared_count = 0;
    std::vector<Record> table = read_records(argv[1], declared_count);
    std::vector<Variant> variants = read_variants(argv[2]);
    std::unordered_map<U, size_t> variant_index;
    for (size_t index = 0; index < variants.size(); ++index)
      variant_index.emplace(variants[index].id, index);
    for (const Record &record : table)
      if (!variant_index.count(record.variant_id))
        throw std::runtime_error("table record has missing variant state");

    std::vector<size_t> index(65537), key_offsets;
    std::vector<U> keys;
    size_t offset = 0;
    for (unsigned high = 0; high <= 65536; ++high) {
      while (offset < table.size() && Q(table[offset].key) < (Q(high) << 16))
        ++offset;
      index[high] = offset;
    }
    for (size_t i = 0; i < table.size(); ++i) {
      if (i == 0 || table[i - 1].key != table[i].key) {
        keys.push_back(table[i].key);
        key_offsets.push_back(i);
      }
    }

    const Q trials = std::strtoull(argv[3], nullptr, 0);
    const Q seed = std::strtoull(argv[4], nullptr, 0);
    const std::string mode = argv[5];
    if (mode != "c32" && mode != "conditional") return 5;
    RNG rng(seed);
    Q key_hit_trials = 0, group_records = 0, examined = 0, accepted = 0;
    Q stages[7]{};
    std::cout << "{\"kind\":\"start\",\"trials\":" << trials
              << ",\"seed\":" << seed << ",\"mode\":\"" << mode
              << "\",\"records\":" << table.size()
              << ",\"declared_records\":" << declared_count
              << ",\"keys\":" << keys.size()
              << ",\"variants\":" << variants.size()
              << ",\"canonical_order\":\"key,variant_id,W7,W8,E3,E4,A0\"}\n"
              << std::flush;

    for (Q trial = 0; trial < trials; ++trial) {
      U block[16]{}, cv[8];
      if (mode == "c32") {
        for (unsigned i = 0; i < 8; ++i) {
          Q value = rng.next();
          block[2 * i] = U(value >> 32);
          block[2 * i + 1] = U(value);
        }
        c32(IV, block, cv);
      } else {
        cv[0] = keys[rng.below(keys.size())];
        for (unsigned i = 1; i < 8; ++i) cv[i] = U(rng.next());
      }
      if (trial < 4) {
        std::cout << "{\"kind\":\"control\",\"trial\":" << trial
                  << ",\"cv\":";
        hex_words(cv, 8);
        if (mode == "c32") {
          std::cout << ",\"block\":";
          hex_words(block, 16);
        }
        std::cout << "}\n";
      }

      const U high = cv[0] >> 16;
      auto begin = table.begin() + index[high];
      auto end = table.begin() + index[high + 1];
      auto current = std::lower_bound(
          begin, end, cv[0], [](const Record &record, U key) {
            return record.key < key;
          });
      if (current != end && current->key == cv[0]) {
        ++key_hit_trials;
        auto group_end = current;
        while (group_end != end && group_end->key == cv[0]) ++group_end;
        group_records += static_cast<Q>(group_end - current);
        for (; current != group_end; ++current) {
          ++examined;
          const Variant &variant = variants[variant_index.at(current->variant_id)];
          if (bridge(cv, *current, variant, stages)) {
            ++accepted;
            std::cout << "{\"kind\":\"accepted\",\"trial\":" << trial
                      << ",\"cv\":";
            hex_words(cv, 8);
            std::cout << ",\"variant_id\":" << current->variant_id
                      << ",\"record\":";
            const U record_words[6] = {current->key, current->w7, current->w8,
                                       current->e3, current->e4, current->a0};
            hex_words(record_words, 6);
            if (mode == "c32") {
              std::cout << ",\"block\":";
              hex_words(block, 16);
            }
            std::cout << "}\n" << std::flush;
            break;
          }
        }
      }
      if ((trial + 1) % 16777216 == 0 || trial + 1 == trials) {
        std::cout << "{\"kind\":\"counts\",\"trials\":" << trial + 1
                  << ",\"key_hit_trials\":" << key_hit_trials
                  << ",\"group_records\":" << group_records
                  << ",\"examined\":" << examined
                  << ",\"accepted\":" << accepted
                  << ",\"stages\":[";
        for (unsigned i = 0; i < 7; ++i)
          std::cout << (i ? "," : "") << stages[i];
        std::cout << "]}\n" << std::flush;
      }
    }
  } catch (const std::exception &error) {
    std::cerr << "ERROR: " << error.what() << '\n';
    return 1;
  }
  return 0;
}
```

### Fixed-slice tail sweep and importance sampler

Embedded source SHA-256: `75c81bf52207cbc5c97c5bae298ba7baf858d4ff856c81509d41b2a6dffa7503`.

Source-file SHA-256 after restoring the single final LF: `151c50786972c551d03560e5c6f25f6efecbcc0fbac85e1a4e36edfae503ce97`.

```cpp
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using U = uint32_t;
using Q = uint64_t;
static constexpr U MASK = 0xffffffffU;
static constexpr U K[32] = {
    0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
    0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
    0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
    0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967
};
static constexpr U AF[2][13] = {
 {0x66e7ba7c,0x5ff9d9f8,0x9123b13f,0xb8560dbb,0x677e1e2a,0x9bcf7bbe,0xf8677ad6,0x4a299906,0x44d24ab4,0x39781650,0x6c206d58,0x35c5c2b8,0x0508c8f0},
 {0x66e7ba7c,0x5ff9d9f8,0x9123b13f,0x98560dbb,0x633b16ba,0x9bcf7bbe,0xf8677ad6,0x4a299906,0x44f24ab5,0x39781650,0x6422edc8,0x574542b8,0x0508c8f0}
};
static constexpr U EF[2][9] = {
 {0x58f38fac,0xb95f2294,0x87431160,0x11cae594,0xd504bf23,0x7f27d24c,0xbf893f69,0x2300f189,0xfcc08ef5},
 {0x5caf87bc,0xa94f0a01,0xa7421160,0xf1cae594,0xd0e1b7b4,0xbf27d74c,0xb78bbfd9,0x3fffd0f9,0xbf81c0f4}
};
static constexpr U WF[2][5] = {
 {0x5100da8a,0x0912e57b,0xa96b2054,0x45f2222c,0x4d12f88a},
 {0x5100da8a,0x0912e57b,0xa96b2054,0x41b22a2c,0x6d12f88a}
};

static const std::string R_E14 = "=0=100110000000=101=0000=110===0";
static const std::string R_E15 = "=1====0011===u10001=011===0n===1";
static const std::string R_A14 = "==u=============================";
static const std::string R_A16 = "================================";
static const std::string R_E16 = "======u=n====1==n=====0===01====";
static const std::string R_E17 = "======0=0====1==0==========1====";
static const std::string R_E18 = "==u===1=0=======1====1==========";
static const std::string R_E19 = "==0=============================";
static const std::string R_E20 = "==1=============================";
static const std::string R_W20 = "=====0=nn=====0=u=1=============";
static const std::string R_W22 = "==n=============================";

static inline U rr(U x,unsigned n){return (x>>n)|(x<<(32-n));}
static inline U B0(U x){return rr(x,2)^rr(x,13)^rr(x,22);}
static inline U B1(U x){return rr(x,6)^rr(x,11)^rr(x,25);}
static inline U S0(U x){return rr(x,7)^rr(x,18)^(x>>3);}
static inline U S1(U x){return rr(x,17)^rr(x,19)^(x>>10);}
static inline U Ch(U x,U y,U z){return z^(x&(y^z));}
static inline U Maj(U x,U y,U z){return (x&y)|(z&(x|y));}
static inline unsigned bit(U x,unsigned b){return (x>>b)&1U;}

static U row_delta(const std::string& r){
 U d=0; for(unsigned j=0;j<32;j++)if(r[j]=='u'||r[j]=='n')d|=U(1)<<(31-j); return d;
}
static bool row_ok(const std::string&r,U x,U y){
 if(r.size()!=32)return false;
 for(unsigned j=0;j<32;j++){
  unsigned a=bit(x,31-j),b=bit(y,31-j);char c=r[j];
  if(c=='='&&a!=b)return false;
  if(c=='0'&&(a||b))return false;
  if(c=='1'&&(!a||!b))return false;
  if(c=='u'&&(a||!b))return false;
  if(c=='n'&&(!a||b))return false;
 }
 return true;
}
static std::vector<std::pair<U,U>> row_values(const std::string&r){
 U base=0,delta=0;std::vector<unsigned> pos;
 for(unsigned j=0;j<32;j++){
  if(r[j]=='=')pos.push_back(31-j);
  else if(r[j]=='1'||r[j]=='n')base|=U(1)<<(31-j);
  if(r[j]=='u'||r[j]=='n')delta|=U(1)<<(31-j);
 }
 if(pos.size()>=32)throw std::runtime_error("row domain too large to enumerate");
 std::vector<std::pair<U,U>> out;out.reserve(Q(1)<<pos.size());
 for(Q q=0;q<(Q(1)<<pos.size());q++){
  U x=base;for(unsigned j=0;j<pos.size();j++)x|=U((q>>j)&1)<<pos[j];out.push_back({x,x^delta});
 }
 return out;
}

struct RNG{
 Q s[4];
 static Q rotl(Q x,unsigned k){return (x<<k)|(x>>(64-k));}
 explicit RNG(Q seed){for(auto &x:s){seed+=0x9e3779b97f4a7c15ULL;Q z=seed;z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL;z=(z^(z>>27))*0x94d049bb133111ebULL;x=z^(z>>31);}}
 Q next(){Q r=rotl(s[1]*5,7)*9,t=s[1]<<17;s[2]^=s[0];s[3]^=s[1];s[1]^=s[2];s[0]^=s[3];s[2]^=t;s[3]=rotl(s[3],45);return r;}
 U word(){return U(next());}
 Q below(Q n){Q x,t=-n%n;do{x=next();}while(x<t);return x%n;}
};

struct Domain{
 int parent[32],xr[32],fixed[32];
 std::string row;
 std::vector<int> roots;
 int free_bits=0;
 Domain(const std::string&r,const std::vector<std::array<int,3>>&edges):row(r){
  for(int i=0;i<32;i++){parent[i]=i;xr[i]=0;fixed[i]=-1;}
  for(auto e:edges)unite(e[0],e[1],e[2]);
  for(int j=0;j<32;j++)if(r[j]!='='){
   int b=31-j,v=(r[j]=='1'||r[j]=='n');auto q=find(b);int want=v^q.second;
   if(fixed[q.first]>=0&&fixed[q.first]!=want)throw std::runtime_error("inconsistent domain");fixed[q.first]=want;
  }
  for(int i=0;i<32;i++)if(find(i).first==i){roots.push_back(i);if(fixed[i]<0)free_bits++;}
 }
 std::pair<int,int> find(int x){
  if(parent[x]==x)return {x,0};auto q=find(parent[x]);int v=xr[x]^q.second;parent[x]=q.first;xr[x]=v;return {parent[x],xr[x]};
 }
 void unite(int a,int b,int parity){
  auto x=find(a),y=find(b);if(x.first==y.first){if((x.second^y.second)!=parity)throw std::runtime_error("bad parity graph");return;}
  parent[x.first]=y.first;xr[x.first]=x.second^y.second^parity;
 }
 U sample(RNG&rng){
  int rv[32];for(int i=0;i<32;i++)rv[i]=-1;
  Q pool=0;int left=0;
  for(int root:roots){
   if(fixed[root]>=0)rv[root]=fixed[root];
   else{if(!left){pool=rng.next();left=64;}rv[root]=pool&1;pool>>=1;left--;}
  }
  U x=0;for(int i=0;i<32;i++){auto q=find(i);x|=U(rv[q.first]^q.second)<<i;}return x;
 }
};

struct Record{U key,w7,w8,e3,e4,a0;};
struct InputBridge{
 std::array<U,8> cv{};Record r{};std::array<U,16> block{};bool has_block=false;Q trial=0;std::string raw_cv,raw_record,raw_block;
};
struct Branch{
 U aa[40]{},ee[40]{},w[32]{};
 U&a(int i){return aa[i+4];} U&e(int i){return ee[i+4];}
 const U&a(int i)const{return aa[i+4];} const U&e(int i)const{return ee[i+4];}
};
struct Tail{U w14,w15;};
struct EarlyStats{Q e14=0,w14eq=0,a14row=0,a14rel=0,e15=0,w15eq=0,a15row=0,a15rel=0;};

static std::array<Branch,2> derive(const std::array<U,8>&cv,const Record&r){
 if(cv[0]!=r.key)throw std::runtime_error("CV/record key mismatch");std::array<Branch,2> z;
 const std::string rw7="=======n=======u===u====u=1=u=u=",rw8="============u=======uu==========";
 U d7=row_delta(rw7),d8=row_delta(rw8);
 for(int p=0;p<2;p++){
  Branch&b=z[p];for(int i=-4;i<0;i++){b.a(i)=cv[-1-i];b.e(i)=cv[3-i];}
  for(int i=1;i<=13;i++)b.a(i)=AF[p][i-1];for(int i=5;i<=13;i++)b.e(i)=EF[p][i-5];
  b.a(0)=r.a0;b.e(3)=r.e3;b.e(4)=r.e4^(p?0x20000000U:0);
  b.e(2)=b.a(2)+b.a(-2)-B0(b.a(1))-Maj(b.a(1),b.a(0),b.a(-1));
  b.e(1)=b.a(1)+b.a(-3)-B0(b.a(0))-Maj(b.a(0),b.a(-1),b.a(-2));
  b.e(0)=b.a(0)+b.a(-4)-B0(b.a(-1))-Maj(b.a(-1),b.a(-2),b.a(-3));
  for(int i=0;i<7;i++)b.w[i]=b.e(i)-b.a(i-4)-b.e(i-4)-B1(b.e(i-1))-Ch(b.e(i-1),b.e(i-2),b.e(i-3))-K[i];
  b.w[7]=r.w7^(p?d7:0);b.w[8]=r.w8^(p?d8:0);for(int i=9;i<=13;i++)b.w[i]=WF[p][i-9];
 }
 for(int i=0;i<4;i++)if(z[0].w[i]!=z[1].w[i])throw std::runtime_error("bridge W0..W3 mismatch");
 return z;
}

static bool a14_rel(U x,U a13){
 return bit(x,18)!=bit(x,6)&&bit(x,8)!=bit(x,17)&&bit(x,9)==bit(x,20)&&
        bit(x,30)==bit(a13,30)&&bit(x,25)==bit(a13,25)&&bit(x,23)==bit(a13,23)&&bit(x,15)!=bit(a13,15);
}
static bool a15_rel(U x,U a13,U a6){return bit(x,29)!=bit(a13,29)&&bit(x,29)!=bit(a6,29);}
static bool e16_rel(U x){return bit(x,28)==bit(x,1)&&bit(x,20)==bit(x,7)&&bit(x,20)==bit(x,2)&&bit(x,6)==bit(x,11)&&bit(x,30)!=bit(x,12)&&bit(x,28)!=bit(x,10)&&bit(x,10)!=bit(x,29);}
static bool e18_rel(U x){return bit(x,24)!=bit(x,11)&&bit(x,2)==bit(x,16);}
static bool w4_rel(U x){return bit(x,1)!=bit(x,12)&&bit(x,8)!=bit(x,25)&&bit(x,18)==bit(x,14);}
static bool w5_rel(U x){return bit(x,0)==bit(x,28)&&bit(x,1)==bit(x,18)&&bit(x,30)==bit(x,9);}
static bool w6_rel(U x){return bit(x,1)==bit(x,12)&&bit(x,8)==bit(x,25)&&bit(x,18)!=bit(x,14);}
static bool w20_rel(U x){return bit(x,4)!=bit(x,6)&&bit(x,31)!=bit(x,22)&&bit(x,31)!=bit(x,1)&&bit(x,30)!=bit(x,0)&&bit(x,25)!=bit(x,16)&&bit(x,21)!=bit(x,14);}
static bool w22_rel(U x){return bit(x,4)==bit(x,6)&&bit(x,31)==bit(x,22)&&bit(x,27)!=bit(x,20);}

static std::vector<Tail> candidates(const std::array<Branch,2>&b,EarlyStats*st=nullptr){
 std::vector<Tail> out;auto e14s=row_values(R_E14),e15s=row_values(R_E15);out.reserve(196608);
 for(auto q:e14s){
  if(st)st->e14++;U e14=q.first,e14p=q.second;
  U a14=e14-b[0].a(10)+B0(b[0].a(13))+Maj(b[0].a(13),b[0].a(12),b[0].a(11));
  U a14p=e14p-b[1].a(10)+B0(b[1].a(13))+Maj(b[1].a(13),b[1].a(12),b[1].a(11));
  U w14=e14-b[0].a(10)-b[0].e(10)-B1(b[0].e(13))-Ch(b[0].e(13),b[0].e(12),b[0].e(11))-K[14];
  U w14p=e14p-b[1].a(10)-b[1].e(10)-B1(b[1].e(13))-Ch(b[1].e(13),b[1].e(12),b[1].e(11))-K[14];
  if(w14!=w14p)continue;if(st)st->w14eq++;
  if(!row_ok(R_A14,a14,a14p))continue;if(st)st->a14row++;
  if(!a14_rel(a14,b[0].a(13)))continue;if(st)st->a14rel++;
  for(auto v:e15s){
   if(st)st->e15++;U e15=v.first,e15p=v.second;
   U a15=e15-b[0].a(11)+B0(a14)+Maj(a14,b[0].a(13),b[0].a(12));
   U a15p=e15p-b[1].a(11)+B0(a14p)+Maj(a14p,b[1].a(13),b[1].a(12));
   U w15=e15-b[0].a(11)-b[0].e(11)-B1(e14)-Ch(e14,b[0].e(13),b[0].e(12))-K[15];
   U w15p=e15p-b[1].a(11)-b[1].e(11)-B1(e14p)-Ch(e14p,b[1].e(13),b[1].e(12))-K[15];
   if(w15!=w15p)continue;if(st)st->w15eq++;
   if(a15!=a15p)continue;if(st)st->a15row++;
   if(!a15_rel(a15,b[0].a(13),b[0].a(6)))continue;if(st)st->a15rel++;
   out.push_back({w14,w15});
  }
 }
 return out;
}

static constexpr int NS=13;
static const char* SN[NS]={"A16_row","E16_row","E16_relations","E17_row","E18_row","E18_relations","E19_row","E20_row","W20_row","W20_relations","W22_row","W22_relations","C32_collision"};
struct Test{bool ok[NS]{};std::array<U,8> out{},outp{};};

static constexpr int NBS=6;
static const char* BSN[NBS]={"W4_row","W4_relations","W5_row","W5_relations","W6_row","W6_relations"};
struct BridgeTest{bool ok[NBS]{};};
static BridgeTest test_bridge(const std::array<Branch,2>&b){
 BridgeTest z;
 z.ok[0]=row_ok("==n=============================",b[0].w[4],b[1].w[4]);z.ok[1]=w4_rel(b[0].w[4]);
 z.ok[2]=row_ok("=====u===u==========n===========",b[0].w[5],b[1].w[5]);z.ok[3]=w5_rel(b[0].w[5]);
 z.ok[4]=row_ok("==n=============================",b[0].w[6],b[1].w[6]);z.ok[5]=w6_rel(b[0].w[6]);
 return z;
}
static bool bridge_success(const BridgeTest&t){for(bool q:t.ok)if(!q)return false;return true;}

static Test test_tail(const std::array<U,8>&cv,const std::array<Branch,2>&base,const Tail&t){
 Branch b[2]={base[0],base[1]};
 for(int p=0;p<2;p++){
  b[p].w[14]=t.w14;b[p].w[15]=t.w15;
  for(int i=14;i<32;i++){
   if(i>=16)b[p].w[i]=S1(b[p].w[i-2])+b[p].w[i-7]+S0(b[p].w[i-15])+b[p].w[i-16];
   b[p].e(i)=b[p].a(i-4)+b[p].e(i-4)+B1(b[p].e(i-1))+Ch(b[p].e(i-1),b[p].e(i-2),b[p].e(i-3))+K[i]+b[p].w[i];
   b[p].a(i)=b[p].e(i)-b[p].a(i-4)+B0(b[p].a(i-1))+Maj(b[p].a(i-1),b[p].a(i-2),b[p].a(i-3));
  }
 }
 Test z;
 z.ok[0]=row_ok(R_A16,b[0].a(16),b[1].a(16));
 z.ok[1]=row_ok(R_E16,b[0].e(16),b[1].e(16));z.ok[2]=e16_rel(b[0].e(16));
 z.ok[3]=row_ok(R_E17,b[0].e(17),b[1].e(17));z.ok[4]=row_ok(R_E18,b[0].e(18),b[1].e(18));z.ok[5]=e18_rel(b[0].e(18));
 z.ok[6]=row_ok(R_E19,b[0].e(19),b[1].e(19));z.ok[7]=row_ok(R_E20,b[0].e(20),b[1].e(20));
 z.ok[8]=row_ok(R_W20,b[0].w[20],b[1].w[20]);z.ok[9]=w20_rel(b[0].w[20]);
 z.ok[10]=row_ok(R_W22,b[0].w[22],b[1].w[22]);z.ok[11]=w22_rel(b[0].w[22]);
 for(int p=0;p<2;p++)for(int j=0;j<8;j++){
  U v=j<4?b[p].a(31-j):b[p].e(35-j);(p?z.outp:z.out)[j]=cv[j]+v;
 }
 z.ok[12]=z.out==z.outp;return z;
}
static bool success(const Test&t){for(bool q:t.ok)if(!q)return false;return true;}

static std::string field(const std::string&s,const std::string&name){
 std::string key="\""+name+"\":\"";auto p=s.find(key);if(p==std::string::npos)return {};p+=key.size();auto e=s.find('"',p);return s.substr(p,e-p);
}
static Q number_field(const std::string&s,const std::string&name){
 std::string key="\""+name+"\":";auto p=s.find(key);if(p==std::string::npos)return 0;p+=key.size();return std::strtoull(s.c_str()+p,nullptr,10);
}
static std::vector<U> hex_words(const std::string&s){
 if(s.size()%8)throw std::runtime_error("bad hex word field");std::vector<U> v;
 for(size_t i=0;i<s.size();i+=8)v.push_back(U(std::stoul(s.substr(i,8),nullptr,16)));return v;
}
static std::vector<InputBridge> load_bridges(const std::string&path){
 std::ifstream f(path);if(!f)throw std::runtime_error("cannot read bridge input");std::vector<InputBridge> v;std::string line;
 while(std::getline(f,line))if(line.find("\"kind\":\"accepted\"")!=std::string::npos){
  InputBridge b;b.raw_cv=field(line,"cv");b.raw_record=field(line,"record");b.raw_block=field(line,"block");b.trial=number_field(line,"trial");
  auto cv=hex_words(b.raw_cv),r=hex_words(b.raw_record);if(cv.size()!=8||r.size()!=6)throw std::runtime_error("bad accepted record");
  std::copy(cv.begin(),cv.end(),b.cv.begin());b.r={r[0],r[1],r[2],r[3],r[4],r[5]};
  if(!b.raw_block.empty()){auto x=hex_words(b.raw_block);if(x.size()!=16)throw std::runtime_error("bad block");std::copy(x.begin(),x.end(),b.block.begin());b.has_block=true;}
  v.push_back(b);
 }
 if(v.empty())throw std::runtime_error("no accepted records");return v;
}
static std::string hx(U x){std::ostringstream o;o<<std::hex<<std::setw(8)<<std::setfill('0')<<x;return o.str();}
static std::string cvhex(const std::array<U,8>&x){std::string s;for(U q:x)s+=hx(q);return s;}
static Q tail_hash(const std::vector<Tail>&v){Q h=1469598103934665603ULL;for(auto t:v)for(U x:{t.w14,t.w15})for(int k=3;k>=0;k--){h^=(x>>(8*k))&255;h*=1099511628211ULL;}return h;}

struct Counts{Q tested[NS]{},pass[NS]{},marginal[NS]{};};
struct BridgeCounts{Q tested[NBS]{},pass[NBS]{},marginal[NBS]{};};
static Counts sweep_one(const InputBridge&in,std::vector<Tail>*kept=nullptr,EarlyStats*early=nullptr){
 auto b=derive(in.cv,in.r);EarlyStats st;auto tails=candidates(b,&st);if(early)*early=st;if(kept)*kept=tails;
 Counts c;for(auto t:tails){auto z=test_tail(in.cv,b,t);bool live=true;for(int i=0;i<NS;i++){if(z.ok[i])c.marginal[i]++;if(live){c.tested[i]++;if(z.ok[i])c.pass[i]++;else live=false;}}}return c;
}
static void add(Counts&a,const Counts&b){for(int i=0;i<NS;i++){a.tested[i]+=b.tested[i];a.pass[i]+=b.pass[i];a.marginal[i]+=b.marginal[i];}}
static void add(BridgeCounts&a,const BridgeCounts&b){for(int i=0;i<NBS;i++){a.tested[i]+=b.tested[i];a.pass[i]+=b.pass[i];a.marginal[i]+=b.marginal[i];}}
static void print_counts(std::ostream&o,const Counts&c){
 o<<"[";for(int i=0;i<NS;i++){if(i)o<<",";o<<"{\"name\":\""<<SN[i]<<"\",\"denominator\":"<<c.tested[i]<<",\"pass\":"<<c.pass[i]<<",\"fail\":"<<(c.tested[i]-c.pass[i])<<",\"marginal_pass\":"<<c.marginal[i]<<"}";}o<<"]";
}
static void print_counts(std::ostream&o,const BridgeCounts&c){
 o<<"[";for(int i=0;i<NBS;i++){if(i)o<<",";o<<"{\"name\":\""<<BSN[i]<<"\",\"denominator\":"<<c.tested[i]<<",\"pass\":"<<c.pass[i]<<",\"fail\":"<<(c.tested[i]-c.pass[i])<<",\"marginal_pass\":"<<c.marginal[i]<<"}";}o<<"]";
}
static void update(BridgeCounts&c,const BridgeTest&t){bool live=true;for(int i=0;i<NBS;i++){if(t.ok[i])c.marginal[i]++;if(live){c.tested[i]++;if(t.ok[i])c.pass[i]++;else live=false;}}}
static void update(Counts&c,const Test&t){bool live=true;for(int i=0;i<NS;i++){if(t.ok[i])c.marginal[i]++;if(live){c.tested[i]++;if(t.ok[i])c.pass[i]++;else live=false;}}}
static void print_early(std::ostream&o,const EarlyStats&s,Q n){
 o<<"{\"E14_domain\":"<<s.e14<<",\"W14_equal\":"<<s.w14eq<<",\"A14_row\":"<<s.a14row<<",\"A14_relations\":"<<s.a14rel<<",\"E15_domain\":"<<s.e15<<",\"W15_equal\":"<<s.w15eq<<",\"A15_row\":"<<s.a15row<<",\"A15_relations\":"<<s.a15rel<<",\"candidates\":"<<n<<"}";
}

static int run_sweep(const std::string&input,const std::string&label,const std::string&output){
 auto ins=load_bridges(input);std::ofstream f(output);if(!f)return 3;Counts total;Q expected_hash=0;size_t expected_n=0;
 f<<"{\n  \"schema\":\"tail-stage-sweep-v1\",\n  \"ensemble\":\""<<label<<"\",\n  \"input\":\""<<input<<"\",\n  \"bridge_count\":"<<ins.size()<<",\n  \"bridges\":[\n";
 for(size_t j=0;j<ins.size();j++){
  std::vector<Tail> tails;EarlyStats early;Counts c=sweep_one(ins[j],&tails,&early);add(total,c);Q h=tail_hash(tails);
  if(j==0){expected_hash=h;expected_n=tails.size();}else if(h!=expected_hash||tails.size()!=expected_n)throw std::runtime_error("bridge-specific candidate set changed unexpectedly");
  f<<"    {\"index\":"<<j<<",\"trial\":"<<ins[j].trial<<",\"cv\":\""<<ins[j].raw_cv<<"\",\"record\":\""<<ins[j].raw_record<<"\"";
  if(ins[j].has_block)f<<",\"block\":\""<<ins[j].raw_block<<"\"";f<<",\"candidate_build\":";print_early(f,early,tails.size());f<<",\"stages\":";print_counts(f,c);f<<"}"<<(j+1==ins.size()?"\n":",\n");
 }
 f<<"  ],\n  \"candidate_count_per_bridge\":"<<expected_n<<",\n  \"candidate_fnv1a64\":\""<<std::hex<<std::setw(16)<<std::setfill('0')<<expected_hash<<std::dec<<"\",\n  \"aggregate_stages\":";print_counts(f,total);f<<"\n}\n";return 0;
}

struct Recon{std::array<U,8> cv{};std::array<U,4>w03{};};
static Recon reconstruct(const InputBridge&base,const Branch&b,const Tail&t,U e16,U e17,U e18,U e19){
 U e14=b.a(10)+b.e(10)+B1(b.e(13))+Ch(b.e(13),b.e(12),b.e(11))+K[14]+t.w14;
 U a14=e14-b.a(10)+B0(b.a(13))+Maj(b.a(13),b.a(12),b.a(11));
 U e15=b.a(11)+b.e(11)+B1(e14)+Ch(e14,b.e(13),b.e(12))+K[15]+t.w15;
 U a15=e15-b.a(11)+B0(a14)+Maj(a14,b.a(13),b.a(12));
 U w16=e16-b.a(12)-b.e(12)-B1(e15)-Ch(e15,e14,b.e(13))-K[16];
 U w17=e17-b.a(13)-b.e(13)-B1(e16)-Ch(e16,e15,e14)-K[17];
 U w18=e18-a14-e14-B1(e17)-Ch(e17,e16,e15)-K[18];
 U w19=e19-a15-e15-B1(e18)-Ch(e18,e17,e16)-K[19];
 U w3=w19-S1(w17)-b.w[12]-S0(b.w[4]);
 U w2=w18-S1(w16)-b.w[11]-S0(w3);
 U w1=w17-S1(t.w15)-b.w[10]-S0(w2);
 U w0=w16-S1(t.w14)-b.w[9]-S0(w1);
 U em1=b.e(3)-b.a(-1)-B1(b.e(2))-Ch(b.e(2),b.e(1),b.e(0))-K[3]-w3;
 U em2=b.e(2)-b.a(-2)-B1(b.e(1))-Ch(b.e(1),b.e(0),em1)-K[2]-w2;
 U em3=b.e(1)-b.a(-3)-B1(b.e(0))-Ch(b.e(0),em1,em2)-K[1]-w1;
 U em4=b.e(0)-b.a(-4)-B1(em1)-Ch(em1,em2,em3)-K[0]-w0;
 Recon z;for(int i=0;i<4;i++)z.cv[i]=base.cv[i];z.cv[4]=em1;z.cv[5]=em2;z.cv[6]=em3;z.cv[7]=em4;z.w03={w0,w1,w2,w3};return z;
}
static Q count_k(const std::array<U,8>&cv,const Record&r,const std::vector<Tail>&tails){
 auto b=derive(cv,r);Q k=0;for(auto t:tails)if(success(test_tail(cv,b,t)))k++;return k;
}

static int run_importance(const std::string&input,Q trials,Q seed,const std::string&label,const std::string&output){
 auto ins=load_bridges(input);std::vector<std::array<Branch,2>> bases;std::vector<Tail> tails;Q th=0;
 for(size_t i=0;i<ins.size();i++){
  auto b=derive(ins[i].cv,ins[i].r);EarlyStats st;auto t=candidates(b,&st);Q h=tail_hash(t);
  if(i==0){tails=t;th=h;}else if(h!=th||t.size()!=tails.size())throw std::runtime_error("non-common tail set");bases.push_back(b);
 }
 Domain d16(R_E16,{{28,1,0},{20,7,0},{20,2,0},{6,11,0},{30,12,1},{28,10,1},{10,29,1}});
 Domain d17(R_E17,{}),d18(R_E18,{{24,11,1},{2,16,0}}),d19(R_E19,{});
 int proposal_log2=d16.free_bits+d17.free_bits+d18.free_bits+d19.free_bits;
 if(proposal_log2!=101)throw std::runtime_error("proposal domain cardinality mismatch");
 RNG rng(seed);Counts stages,late_given_bridge;BridgeCounts bridge_stages;std::array<Q,NS> joint_bridge_late{};
 Q recon_ok=0,chosen_success=0,bridge_full=0,chosen_success_bridge=0;long double sum_inv_k=0,sum_inv_k2=0,sum_inv_k_bridge=0,sum_inv_k2_bridge=0;
 std::vector<Counts> base_stages(ins.size()),base_late_given_bridge(ins.size());std::vector<BridgeCounts> base_bridge_stages(ins.size());std::vector<std::array<Q,NS>> base_joint_bridge_late(ins.size());
 std::vector<Q> base_proposals(ins.size()),base_recon(ins.size()),base_successes(ins.size()),base_bridge_full(ins.size()),base_successes_bridge(ins.size());
 std::vector<long double> base_sum_inv_k(ins.size()),base_sum_inv_k_bridge(ins.size());std::vector<std::vector<Q>> base_k_values(ins.size());
 struct Hit{Q trial;size_t base,tail;Recon rec;U e16,e17,e18,e19;Q k;bool bridge;};std::vector<Hit> hits;
 for(Q q=0;q<trials;q++){
  size_t bi=rng.below(ins.size()),ti=rng.below(tails.size());base_proposals[bi]++;U e16=d16.sample(rng),e17=d17.sample(rng),e18=d18.sample(rng),e19=d19.sample(rng);
  Recon z=reconstruct(ins[bi],bases[bi][0],tails[ti],e16,e17,e18,e19);auto nb=derive(z.cv,ins[bi].r);
  bool exact=true;for(int k=0;k<4;k++)exact&=nb[0].w[k]==z.w03[k];if(!exact)throw std::runtime_error("proposal reconstruction failed");recon_ok++;base_recon[bi]++;
  BridgeTest bridge_test=test_bridge(nb);update(bridge_stages,bridge_test);update(base_bridge_stages[bi],bridge_test);bool bridge_ok=bridge_success(bridge_test);
  Test test=test_tail(z.cv,nb,tails[ti]);update(stages,test);update(base_stages[bi],test);
  if(bridge_ok){bridge_full++;base_bridge_full[bi]++;update(late_given_bridge,test);update(base_late_given_bridge[bi],test);for(int i=0;i<NS;i++)if(test.ok[i]){joint_bridge_late[i]++;base_joint_bridge_late[bi][i]++;}}
  if(success(test)){
   Q kval=count_k(z.cv,ins[bi].r,tails);if(!kval)throw std::runtime_error("successful selected tail has K=0");chosen_success++;base_successes[bi]++;base_k_values[bi].push_back(kval);long double x=1.0L/kval;sum_inv_k+=x;sum_inv_k2+=x*x;base_sum_inv_k[bi]+=x;
   if(bridge_ok){chosen_success_bridge++;base_successes_bridge[bi]++;sum_inv_k_bridge+=x;sum_inv_k2_bridge+=x*x;base_sum_inv_k_bridge[bi]+=x;}
   hits.push_back({q,bi,ti,z,e16,e17,e18,e19,kval,bridge_ok});
  }
 }
 long double weight=std::ldexp(1.0L,proposal_log2-128);long double factor=tails.size()*weight;
 long double pi=factor*sum_inv_k/trials;long double second=factor*factor*sum_inv_k2/trials;long double var=trials>1?(second-pi*pi)*trials/(trials-1):0;long double se=std::sqrt(std::max((long double)0,var)/trials);
 long double pi_bridge=factor*sum_inv_k_bridge/trials;long double second_bridge=factor*factor*sum_inv_k2_bridge/trials;long double var_bridge=trials>1?(second_bridge-pi_bridge*pi_bridge)*trials/(trials-1):0;long double se_bridge=std::sqrt(std::max((long double)0,var_bridge)/trials);
 std::ofstream f(output);if(!f)return 3;f<<std::setprecision(18);
 f<<"{\n  \"schema\":\"tail-importance-v1\",\n  \"ensemble\":\""<<label<<"\",\n  \"input\":\""<<input<<"\",\n  \"seed\":"<<seed<<",\n  \"trials\":"<<trials<<",\n  \"bridge_count\":"<<ins.size()<<",\n";
 f<<"  \"tail_count\":"<<tails.size()<<",\n  \"tail_fnv1a64\":\""<<std::hex<<std::setw(16)<<std::setfill('0')<<th<<std::dec<<"\",\n";
 f<<"  \"reconstructed_E_halves\":\"abstract; no standard-IV first-block preimage is known\",\n";
 f<<"  \"proposal\":{\"dimensions\":[\"E16_with_relations\",\"E17\",\"E18_with_relations\",\"E19\"],\"domain_log2\":["<<d16.free_bits<<","<<d17.free_bits<<","<<d18.free_bits<<","<<d19.free_bits<<"],\"joint_domain_log2\":"<<proposal_log2<<",\"likelihood_ratio\":"<<double(weight)<<",\"likelihood_ratio_power2\":-27},\n";
 f<<"  \"reconstruction_pass\":"<<recon_ok<<",\n  \"bridge_filter_scope\":\"exact Figure 6 W4-W6 rows and relations; W0-W3 equality is guaranteed by each selected A half and checked by derive\",\n";
 f<<"  \"bridge_stage_counts\":";print_counts(f,bridge_stages);f<<",\n  \"full_bridge_pass_under_proposal\":"<<bridge_full<<",\n";
 f<<"  \"stage_counts\":";print_counts(f,stages);f<<",\n  \"late_stage_counts_given_full_bridge_under_proposal\":";print_counts(f,late_given_bridge);f<<",\n";
 f<<"  \"bridge_and_late_marginal\":[";for(int i=0;i<NS;i++){if(i)f<<",";f<<"{\"name\":\""<<SN[i]<<"\",\"denominator\":"<<trials<<",\"bridge_pass\":"<<bridge_full<<",\"late_pass\":"<<stages.marginal[i]<<",\"joint_pass\":"<<joint_bridge_late[i]<<"}";}f<<"],\n  \"chosen_tail_successes\":"<<chosen_success<<",\n";
 f<<"  \"sum_inverse_K\":"<<double(sum_inv_k)<<",\n  \"pi_uniform_estimate\":"<<double(pi)<<",\n  \"monte_carlo_standard_error\":"<<double(se)<<",\n";
 f<<"  \"chosen_tail_successes_with_full_bridge\":"<<chosen_success_bridge<<",\n  \"sum_inverse_K_with_full_bridge\":"<<double(sum_inv_k_bridge)<<",\n";
 f<<"  \"uniform_E_probability_mass_estimate_bridge_and_path_union\":"<<double(pi_bridge)<<",\n  \"bridge_and_path_monte_carlo_standard_error\":"<<double(se_bridge)<<",\n";
 f<<"  \"calibrated_confidence_interval\":null,\n  \"per_base\":[\n";
 for(size_t i=0;i<ins.size();i++){
  f<<"    {\"base_bridge_index\":"<<i<<",\"base_trial\":"<<ins[i].trial<<",\"source_cv\":\""<<ins[i].raw_cv<<"\",\"record\":\""<<ins[i].raw_record<<"\",\"proposal_count\":"<<base_proposals[i]<<",\"reconstruction_pass\":"<<base_recon[i]<<",\"bridge_stage_counts\":";print_counts(f,base_bridge_stages[i]);
  f<<",\"full_bridge_pass_under_proposal\":"<<base_bridge_full[i]<<",\"stage_counts\":";print_counts(f,base_stages[i]);f<<",\"late_stage_counts_given_full_bridge_under_proposal\":";print_counts(f,base_late_given_bridge[i]);
  f<<",\"bridge_and_late_marginal\":[";for(int k=0;k<NS;k++){if(k)f<<",";f<<"{\"name\":\""<<SN[k]<<"\",\"joint_pass\":"<<base_joint_bridge_late[i][k]<<"}";}f<<"],\"chosen_tail_successes\":"<<base_successes[i]<<",\"sum_inverse_K\":"<<double(base_sum_inv_k[i])<<",\"chosen_tail_successes_with_full_bridge\":"<<base_successes_bridge[i]<<",\"sum_inverse_K_with_full_bridge\":"<<double(base_sum_inv_k_bridge[i])<<",\"K_values\":[";for(size_t j=0;j<base_k_values[i].size();j++){if(j)f<<",";f<<base_k_values[i][j];}f<<"]}"<<(i+1==ins.size()?"\n":",\n");
 }
 f<<"  ],\n  \"successes\":[\n";
 for(size_t i=0;i<hits.size();i++){auto&h=hits[i];f<<"    {\"trial\":"<<h.trial<<",\"base_bridge_index\":"<<h.base<<",\"base_trial\":"<<ins[h.base].trial<<",\"cv\":\""<<cvhex(h.rec.cv)<<"\",\"record\":\""<<ins[h.base].raw_record<<"\",\"tail_index\":"<<h.tail<<",\"tail\":\""<<hx(tails[h.tail].w14)<<hx(tails[h.tail].w15)<<"\",\"E16\":\""<<hx(h.e16)<<"\",\"E17\":\""<<hx(h.e17)<<"\",\"E18\":\""<<hx(h.e18)<<"\",\"E19\":\""<<hx(h.e19)<<"\",\"full_bridge\":"<<(h.bridge?"true":"false")<<",\"K\":"<<h.k<<"}"<<(i+1==hits.size()?"\n":",\n");}
 f<<"  ]\n}\n";return 0;
}

int main(int argc,char**argv){
 try{
  if(argc<2)throw std::runtime_error("usage: tail_measure sweep INPUT LABEL OUTPUT | importance INPUT TRIALS SEED LABEL OUTPUT");
  std::string mode=argv[1];
  if(mode=="sweep"&&argc==5)return run_sweep(argv[2],argv[3],argv[4]);
  if(mode=="importance"&&argc==7)return run_importance(argv[2],std::strtoull(argv[3],nullptr,0),std::strtoull(argv[4],nullptr,0),argv[5],argv[6]);
  throw std::runtime_error("bad arguments");
 }catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 2;}
}
```

### Variant-aware tail sweep and importance sampler

Embedded source SHA-256: `4ed2e8ae7eaec4b471f8276f9d366e11af3cd33e6127408638192f658789b216`.

Source-file SHA-256 after restoring the single final LF: `b1fc414eb1e72eca133c3674523c461cf4b1ed57d2ee0c210f7ef9224ab2378c`.

```cpp
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

using U = uint32_t;
using Q = uint64_t;
static constexpr U MASK = 0xffffffffU;
static constexpr U K[32] = {
    0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
    0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
    0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
    0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967
};
static constexpr U AF[2][13] = {
 {0x66e7ba7c,0x5ff9d9f8,0x9123b13f,0xb8560dbb,0x677e1e2a,0x9bcf7bbe,0xf8677ad6,0x4a299906,0x44d24ab4,0x39781650,0x6c206d58,0x35c5c2b8,0x0508c8f0},
 {0x66e7ba7c,0x5ff9d9f8,0x9123b13f,0x98560dbb,0x633b16ba,0x9bcf7bbe,0xf8677ad6,0x4a299906,0x44f24ab5,0x39781650,0x6422edc8,0x574542b8,0x0508c8f0}
};
static constexpr U EF[2][9] = {
 {0x58f38fac,0xb95f2294,0x87431160,0x11cae594,0xd504bf23,0x7f27d24c,0xbf893f69,0x2300f189,0xfcc08ef5},
 {0x5caf87bc,0xa94f0a01,0xa7421160,0xf1cae594,0xd0e1b7b4,0xbf27d74c,0xb78bbfd9,0x3fffd0f9,0xbf81c0f4}
};
static constexpr U WF[2][5] = {
 {0x5100da8a,0x0912e57b,0xa96b2054,0x45f2222c,0x4d12f88a},
 {0x5100da8a,0x0912e57b,0xa96b2054,0x41b22a2c,0x6d12f88a}
};

static const std::string R_E14 = "=0=100110000000=101=0000=110===0";
static const std::string R_E15 = "=1====0011===u10001=011===0n===1";
static const std::string R_A14 = "==u=============================";
static const std::string R_A16 = "================================";
static const std::string R_E16 = "======u=n====1==n=====0===01====";
static const std::string R_E17 = "======0=0====1==0==========1====";
static const std::string R_E18 = "==u===1=0=======1====1==========";
static const std::string R_E19 = "==0=============================";
static const std::string R_E20 = "==1=============================";
static const std::string R_W20 = "=====0=nn=====0=u=1=============";
static const std::string R_W22 = "==n=============================";

static inline U rr(U x,unsigned n){return (x>>n)|(x<<(32-n));}
static inline U B0(U x){return rr(x,2)^rr(x,13)^rr(x,22);}
static inline U B1(U x){return rr(x,6)^rr(x,11)^rr(x,25);}
static inline U S0(U x){return rr(x,7)^rr(x,18)^(x>>3);}
static inline U S1(U x){return rr(x,17)^rr(x,19)^(x>>10);}
static inline U Ch(U x,U y,U z){return z^(x&(y^z));}
static inline U Maj(U x,U y,U z){return (x&y)|(z&(x|y));}
static inline unsigned bit(U x,unsigned b){return (x>>b)&1U;}

static U row_delta(const std::string& r){
 U d=0; for(unsigned j=0;j<32;j++)if(r[j]=='u'||r[j]=='n')d|=U(1)<<(31-j); return d;
}
static bool row_ok(const std::string&r,U x,U y){
 if(r.size()!=32)return false;
 for(unsigned j=0;j<32;j++){
  unsigned a=bit(x,31-j),b=bit(y,31-j);char c=r[j];
  if(c=='='&&a!=b)return false;
  if(c=='0'&&(a||b))return false;
  if(c=='1'&&(!a||!b))return false;
  if(c=='u'&&(a||!b))return false;
  if(c=='n'&&(!a||b))return false;
 }
 return true;
}
static std::vector<std::pair<U,U>> row_values(const std::string&r){
 U base=0,delta=0;std::vector<unsigned> pos;
 for(unsigned j=0;j<32;j++){
  if(r[j]=='=')pos.push_back(31-j);
  else if(r[j]=='1'||r[j]=='n')base|=U(1)<<(31-j);
  if(r[j]=='u'||r[j]=='n')delta|=U(1)<<(31-j);
 }
 if(pos.size()>=32)throw std::runtime_error("row domain too large to enumerate");
 std::vector<std::pair<U,U>> out;out.reserve(Q(1)<<pos.size());
 for(Q q=0;q<(Q(1)<<pos.size());q++){
  U x=base;for(unsigned j=0;j<pos.size();j++)x|=U((q>>j)&1)<<pos[j];out.push_back({x,x^delta});
 }
 return out;
}

struct RNG{
 Q s[4];
 static Q rotl(Q x,unsigned k){return (x<<k)|(x>>(64-k));}
 explicit RNG(Q seed){for(auto &x:s){seed+=0x9e3779b97f4a7c15ULL;Q z=seed;z=(z^(z>>30))*0xbf58476d1ce4e5b9ULL;z=(z^(z>>27))*0x94d049bb133111ebULL;x=z^(z>>31);}}
 Q next(){Q r=rotl(s[1]*5,7)*9,t=s[1]<<17;s[2]^=s[0];s[3]^=s[1];s[1]^=s[2];s[0]^=s[3];s[2]^=t;s[3]=rotl(s[3],45);return r;}
 U word(){return U(next());}
 Q below(Q n){Q x,t=-n%n;do{x=next();}while(x<t);return x%n;}
};

struct Domain{
 int parent[32],xr[32],fixed[32];
 std::string row;
 std::vector<int> roots;
 int free_bits=0;
 Domain(const std::string&r,const std::vector<std::array<int,3>>&edges):row(r){
  for(int i=0;i<32;i++){parent[i]=i;xr[i]=0;fixed[i]=-1;}
  for(auto e:edges)unite(e[0],e[1],e[2]);
  for(int j=0;j<32;j++)if(r[j]!='='){
   int b=31-j,v=(r[j]=='1'||r[j]=='n');auto q=find(b);int want=v^q.second;
   if(fixed[q.first]>=0&&fixed[q.first]!=want)throw std::runtime_error("inconsistent domain");fixed[q.first]=want;
  }
  for(int i=0;i<32;i++)if(find(i).first==i){roots.push_back(i);if(fixed[i]<0)free_bits++;}
 }
 std::pair<int,int> find(int x){
  if(parent[x]==x)return {x,0};auto q=find(parent[x]);int v=xr[x]^q.second;parent[x]=q.first;xr[x]=v;return {parent[x],xr[x]};
 }
 void unite(int a,int b,int parity){
  auto x=find(a),y=find(b);if(x.first==y.first){if((x.second^y.second)!=parity)throw std::runtime_error("bad parity graph");return;}
  parent[x.first]=y.first;xr[x.first]=x.second^y.second^parity;
 }
 U sample(RNG&rng){
  int rv[32];for(int i=0;i<32;i++)rv[i]=-1;
  Q pool=0;int left=0;
  for(int root:roots){
   if(fixed[root]>=0)rv[root]=fixed[root];
   else{if(!left){pool=rng.next();left=64;}rv[root]=pool&1;pool>>=1;left--;}
  }
  U x=0;for(int i=0;i<32;i++){auto q=find(i);x|=U(rv[q.first]^q.second)<<i;}return x;
 }
};

struct Record{U key,w7,w8,e3,e4,a0;};
struct Variant{U id;U a[2][3],e[2][3],w[2][5];};
static std::vector<Variant> VARIANTS;
static std::unordered_map<U,size_t> VARIANT_INDEX;
struct InputBridge{
 std::array<U,8> cv{};Record r{};U variant_id=0;std::array<U,16> block{};bool has_block=false;Q trial=0;std::string raw_cv,raw_record,raw_block;
};
struct Branch{
 U aa[40]{},ee[40]{},w[32]{};
 U&a(int i){return aa[i+4];} U&e(int i){return ee[i+4];}
 const U&a(int i)const{return aa[i+4];} const U&e(int i)const{return ee[i+4];}
};
struct Tail{U w14,w15;};
struct EarlyStats{Q e14=0,w14eq=0,a14row=0,a14rel=0,e15=0,w15eq=0,a15row=0,a15rel=0;};

static const Variant& variant_for(U id){
 auto found=VARIANT_INDEX.find(id);if(found==VARIANT_INDEX.end())throw std::runtime_error("missing variant state");return VARIANTS[found->second];
}

static std::array<Branch,2> derive(const std::array<U,8>&cv,const Record&r,U variant_id){
 if(cv[0]!=r.key)throw std::runtime_error("CV/record key mismatch");std::array<Branch,2> z;
 const Variant&v=variant_for(variant_id);
 const std::string rw7="=======n=======u===u====u=1=u=u=",rw8="============u=======uu==========";
 U d7=row_delta(rw7),d8=row_delta(rw8);
 for(int p=0;p<2;p++){
  Branch&b=z[p];for(int i=-4;i<0;i++){b.a(i)=cv[-1-i];b.e(i)=cv[3-i];}
  for(int i=1;i<=3;i++)b.a(i)=v.a[p][i-1];for(int i=4;i<=13;i++)b.a(i)=AF[p][i-1];
  for(int i=5;i<=7;i++)b.e(i)=v.e[p][i-5];for(int i=8;i<=13;i++)b.e(i)=EF[p][i-5];
  b.a(0)=r.a0;b.e(3)=r.e3;b.e(4)=r.e4^(p?0x20000000U:0);
  b.e(2)=b.a(2)+b.a(-2)-B0(b.a(1))-Maj(b.a(1),b.a(0),b.a(-1));
  b.e(1)=b.a(1)+b.a(-3)-B0(b.a(0))-Maj(b.a(0),b.a(-1),b.a(-2));
  b.e(0)=b.a(0)+b.a(-4)-B0(b.a(-1))-Maj(b.a(-1),b.a(-2),b.a(-3));
  for(int i=0;i<7;i++)b.w[i]=b.e(i)-b.a(i-4)-b.e(i-4)-B1(b.e(i-1))-Ch(b.e(i-1),b.e(i-2),b.e(i-3))-K[i];
  b.w[7]=r.w7^(p?d7:0);b.w[8]=r.w8^(p?d8:0);for(int i=9;i<=13;i++)b.w[i]=v.w[p][i-9];
 }
 for(int i=0;i<4;i++)if(z[0].w[i]!=z[1].w[i])throw std::runtime_error("bridge W0..W3 mismatch");
 return z;
}

static bool a14_rel(U x,U a13){
 return bit(x,18)!=bit(x,6)&&bit(x,8)!=bit(x,17)&&bit(x,9)==bit(x,20)&&
        bit(x,30)==bit(a13,30)&&bit(x,25)==bit(a13,25)&&bit(x,23)==bit(a13,23)&&bit(x,15)!=bit(a13,15);
}
static bool a15_rel(U x,U a13,U a6){return bit(x,29)!=bit(a13,29)&&bit(x,29)!=bit(a6,29);}
static bool e16_rel(U x){return bit(x,28)==bit(x,1)&&bit(x,20)==bit(x,7)&&bit(x,20)==bit(x,2)&&bit(x,6)==bit(x,11)&&bit(x,30)!=bit(x,12)&&bit(x,28)!=bit(x,10)&&bit(x,10)!=bit(x,29);}
static bool e18_rel(U x){return bit(x,24)!=bit(x,11)&&bit(x,2)==bit(x,16);}
static bool w4_rel(U x){return bit(x,1)!=bit(x,12)&&bit(x,8)!=bit(x,25)&&bit(x,18)==bit(x,14);}
static bool w5_rel(U x){return bit(x,0)==bit(x,28)&&bit(x,1)==bit(x,18)&&bit(x,30)==bit(x,9);}
static bool w6_rel(U x){return bit(x,1)==bit(x,12)&&bit(x,8)==bit(x,25)&&bit(x,18)!=bit(x,14);}
static bool w20_rel(U x){return bit(x,4)!=bit(x,6)&&bit(x,31)!=bit(x,22)&&bit(x,31)!=bit(x,1)&&bit(x,30)!=bit(x,0)&&bit(x,25)!=bit(x,16)&&bit(x,21)!=bit(x,14);}
static bool w22_rel(U x){return bit(x,4)==bit(x,6)&&bit(x,31)==bit(x,22)&&bit(x,27)!=bit(x,20);}

static std::vector<Tail> candidates(const std::array<Branch,2>&b,EarlyStats*st=nullptr){
 std::vector<Tail> out;auto e14s=row_values(R_E14),e15s=row_values(R_E15);out.reserve(196608);
 for(auto q:e14s){
  if(st)st->e14++;U e14=q.first,e14p=q.second;
  U a14=e14-b[0].a(10)+B0(b[0].a(13))+Maj(b[0].a(13),b[0].a(12),b[0].a(11));
  U a14p=e14p-b[1].a(10)+B0(b[1].a(13))+Maj(b[1].a(13),b[1].a(12),b[1].a(11));
  U w14=e14-b[0].a(10)-b[0].e(10)-B1(b[0].e(13))-Ch(b[0].e(13),b[0].e(12),b[0].e(11))-K[14];
  U w14p=e14p-b[1].a(10)-b[1].e(10)-B1(b[1].e(13))-Ch(b[1].e(13),b[1].e(12),b[1].e(11))-K[14];
  if(w14!=w14p)continue;if(st)st->w14eq++;
  if(!row_ok(R_A14,a14,a14p))continue;if(st)st->a14row++;
  if(!a14_rel(a14,b[0].a(13)))continue;if(st)st->a14rel++;
  for(auto v:e15s){
   if(st)st->e15++;U e15=v.first,e15p=v.second;
   U a15=e15-b[0].a(11)+B0(a14)+Maj(a14,b[0].a(13),b[0].a(12));
   U a15p=e15p-b[1].a(11)+B0(a14p)+Maj(a14p,b[1].a(13),b[1].a(12));
   U w15=e15-b[0].a(11)-b[0].e(11)-B1(e14)-Ch(e14,b[0].e(13),b[0].e(12))-K[15];
   U w15p=e15p-b[1].a(11)-b[1].e(11)-B1(e14p)-Ch(e14p,b[1].e(13),b[1].e(12))-K[15];
   if(w15!=w15p)continue;if(st)st->w15eq++;
   if(a15!=a15p)continue;if(st)st->a15row++;
   if(!a15_rel(a15,b[0].a(13),b[0].a(6)))continue;if(st)st->a15rel++;
   out.push_back({w14,w15});
  }
 }
 return out;
}

static constexpr int NS=13;
static const char* SN[NS]={"A16_row","E16_row","E16_relations","E17_row","E18_row","E18_relations","E19_row","E20_row","W20_row","W20_relations","W22_row","W22_relations","C32_collision"};
struct Test{bool ok[NS]{};std::array<U,8> out{},outp{};};

static constexpr int NBS=6;
static const char* BSN[NBS]={"W4_row","W4_relations","W5_row","W5_relations","W6_row","W6_relations"};
struct BridgeTest{bool ok[NBS]{};};
static BridgeTest test_bridge(const std::array<Branch,2>&b){
 BridgeTest z;
 z.ok[0]=row_ok("==n=============================",b[0].w[4],b[1].w[4]);z.ok[1]=w4_rel(b[0].w[4]);
 z.ok[2]=row_ok("=====u===u==========n===========",b[0].w[5],b[1].w[5]);z.ok[3]=w5_rel(b[0].w[5]);
 z.ok[4]=row_ok("==n=============================",b[0].w[6],b[1].w[6]);z.ok[5]=w6_rel(b[0].w[6]);
 return z;
}
static bool bridge_success(const BridgeTest&t){for(bool q:t.ok)if(!q)return false;return true;}

static Test test_tail(const std::array<U,8>&cv,const std::array<Branch,2>&base,const Tail&t){
 Branch b[2]={base[0],base[1]};
 for(int p=0;p<2;p++){
  b[p].w[14]=t.w14;b[p].w[15]=t.w15;
  for(int i=14;i<32;i++){
   if(i>=16)b[p].w[i]=S1(b[p].w[i-2])+b[p].w[i-7]+S0(b[p].w[i-15])+b[p].w[i-16];
   b[p].e(i)=b[p].a(i-4)+b[p].e(i-4)+B1(b[p].e(i-1))+Ch(b[p].e(i-1),b[p].e(i-2),b[p].e(i-3))+K[i]+b[p].w[i];
   b[p].a(i)=b[p].e(i)-b[p].a(i-4)+B0(b[p].a(i-1))+Maj(b[p].a(i-1),b[p].a(i-2),b[p].a(i-3));
  }
 }
 Test z;
 z.ok[0]=row_ok(R_A16,b[0].a(16),b[1].a(16));
 z.ok[1]=row_ok(R_E16,b[0].e(16),b[1].e(16));z.ok[2]=e16_rel(b[0].e(16));
 z.ok[3]=row_ok(R_E17,b[0].e(17),b[1].e(17));z.ok[4]=row_ok(R_E18,b[0].e(18),b[1].e(18));z.ok[5]=e18_rel(b[0].e(18));
 z.ok[6]=row_ok(R_E19,b[0].e(19),b[1].e(19));z.ok[7]=row_ok(R_E20,b[0].e(20),b[1].e(20));
 z.ok[8]=row_ok(R_W20,b[0].w[20],b[1].w[20]);z.ok[9]=w20_rel(b[0].w[20]);
 z.ok[10]=row_ok(R_W22,b[0].w[22],b[1].w[22]);z.ok[11]=w22_rel(b[0].w[22]);
 for(int p=0;p<2;p++)for(int j=0;j<8;j++){
  U v=j<4?b[p].a(31-j):b[p].e(35-j);(p?z.outp:z.out)[j]=cv[j]+v;
 }
 z.ok[12]=z.out==z.outp;return z;
}
static bool success(const Test&t){for(bool q:t.ok)if(!q)return false;return true;}

static std::string field(const std::string&s,const std::string&name){
 std::string key="\""+name+"\":\"";auto p=s.find(key);if(p==std::string::npos)return {};p+=key.size();auto e=s.find('"',p);return s.substr(p,e-p);
}
static Q number_field(const std::string&s,const std::string&name){
 std::string key="\""+name+"\":";auto p=s.find(key);if(p==std::string::npos)return 0;p+=key.size();return std::strtoull(s.c_str()+p,nullptr,10);
}
static U read_u32(std::istream&f){unsigned char b[4];if(!f.read(reinterpret_cast<char*>(b),4))throw std::runtime_error("short variant state input");return (U(b[0])<<24)|(U(b[1])<<16)|(U(b[2])<<8)|U(b[3]);}
static void load_variants(const std::string&path){
 std::ifstream f(path,std::ios::binary);if(!f)throw std::runtime_error("cannot read variant states");char magic[4];
 if(!f.read(magic,4)||std::string(magic,4)!="RVS1")throw std::runtime_error("bad variant state magic");U count=read_u32(f);VARIANTS.clear();VARIANT_INDEX.clear();VARIANTS.reserve(count);
 for(U i=0;i<count;i++){Variant v{};v.id=read_u32(f);for(int p=0;p<2;p++)for(U&x:v.a[p])x=read_u32(f);for(int p=0;p<2;p++)for(U&x:v.e[p])x=read_u32(f);for(int p=0;p<2;p++)for(U&x:v.w[p])x=read_u32(f);if(!VARIANTS.empty()&&VARIANTS.back().id>=v.id)throw std::runtime_error("variant states not strictly ordered");VARIANT_INDEX.emplace(v.id,VARIANTS.size());VARIANTS.push_back(v);}
 if(f.peek()!=EOF)throw std::runtime_error("trailing variant state bytes");
}
static std::vector<U> hex_words(const std::string&s){
 if(s.size()%8)throw std::runtime_error("bad hex word field");std::vector<U> v;
 for(size_t i=0;i<s.size();i+=8)v.push_back(U(std::stoul(s.substr(i,8),nullptr,16)));return v;
}
static std::vector<InputBridge> load_bridges(const std::string&path){
 std::ifstream f(path);if(!f)throw std::runtime_error("cannot read bridge input");std::vector<InputBridge> v;std::string line;
 while(std::getline(f,line))if(line.find("\"kind\":\"accepted\"")!=std::string::npos){
  InputBridge b;b.raw_cv=field(line,"cv");b.raw_record=field(line,"record");b.raw_block=field(line,"block");b.trial=number_field(line,"trial");b.variant_id=U(number_field(line,"variant_id"));
  auto cv=hex_words(b.raw_cv),r=hex_words(b.raw_record);if(cv.size()!=8||r.size()!=6)throw std::runtime_error("bad accepted record");
  std::copy(cv.begin(),cv.end(),b.cv.begin());b.r={r[0],r[1],r[2],r[3],r[4],r[5]};
  (void)variant_for(b.variant_id);
  if(!b.raw_block.empty()){auto x=hex_words(b.raw_block);if(x.size()!=16)throw std::runtime_error("bad block");std::copy(x.begin(),x.end(),b.block.begin());b.has_block=true;}
  v.push_back(b);
 }
 if(v.empty())throw std::runtime_error("no accepted records");return v;
}
static std::string hx(U x){std::ostringstream o;o<<std::hex<<std::setw(8)<<std::setfill('0')<<x;return o.str();}
static std::string cvhex(const std::array<U,8>&x){std::string s;for(U q:x)s+=hx(q);return s;}
static Q tail_hash(const std::vector<Tail>&v){Q h=1469598103934665603ULL;for(auto t:v)for(U x:{t.w14,t.w15})for(int k=3;k>=0;k--){h^=(x>>(8*k))&255;h*=1099511628211ULL;}return h;}

struct Counts{Q tested[NS]{},pass[NS]{},marginal[NS]{};};
struct BridgeCounts{Q tested[NBS]{},pass[NBS]{},marginal[NBS]{};};
static Counts sweep_one(const InputBridge&in,std::vector<Tail>*kept=nullptr,EarlyStats*early=nullptr){
 auto b=derive(in.cv,in.r,in.variant_id);EarlyStats st;auto tails=candidates(b,&st);if(early)*early=st;if(kept)*kept=tails;
 Counts c;for(auto t:tails){auto z=test_tail(in.cv,b,t);bool live=true;for(int i=0;i<NS;i++){if(z.ok[i])c.marginal[i]++;if(live){c.tested[i]++;if(z.ok[i])c.pass[i]++;else live=false;}}}return c;
}
static void add(Counts&a,const Counts&b){for(int i=0;i<NS;i++){a.tested[i]+=b.tested[i];a.pass[i]+=b.pass[i];a.marginal[i]+=b.marginal[i];}}
static void add(BridgeCounts&a,const BridgeCounts&b){for(int i=0;i<NBS;i++){a.tested[i]+=b.tested[i];a.pass[i]+=b.pass[i];a.marginal[i]+=b.marginal[i];}}
static void print_counts(std::ostream&o,const Counts&c){
 o<<"[";for(int i=0;i<NS;i++){if(i)o<<",";o<<"{\"name\":\""<<SN[i]<<"\",\"denominator\":"<<c.tested[i]<<",\"pass\":"<<c.pass[i]<<",\"fail\":"<<(c.tested[i]-c.pass[i])<<",\"marginal_pass\":"<<c.marginal[i]<<"}";}o<<"]";
}
static void print_counts(std::ostream&o,const BridgeCounts&c){
 o<<"[";for(int i=0;i<NBS;i++){if(i)o<<",";o<<"{\"name\":\""<<BSN[i]<<"\",\"denominator\":"<<c.tested[i]<<",\"pass\":"<<c.pass[i]<<",\"fail\":"<<(c.tested[i]-c.pass[i])<<",\"marginal_pass\":"<<c.marginal[i]<<"}";}o<<"]";
}
static void update(BridgeCounts&c,const BridgeTest&t){bool live=true;for(int i=0;i<NBS;i++){if(t.ok[i])c.marginal[i]++;if(live){c.tested[i]++;if(t.ok[i])c.pass[i]++;else live=false;}}}
static void update(Counts&c,const Test&t){bool live=true;for(int i=0;i<NS;i++){if(t.ok[i])c.marginal[i]++;if(live){c.tested[i]++;if(t.ok[i])c.pass[i]++;else live=false;}}}
static void print_early(std::ostream&o,const EarlyStats&s,Q n){
 o<<"{\"E14_domain\":"<<s.e14<<",\"W14_equal\":"<<s.w14eq<<",\"A14_row\":"<<s.a14row<<",\"A14_relations\":"<<s.a14rel<<",\"E15_domain\":"<<s.e15<<",\"W15_equal\":"<<s.w15eq<<",\"A15_row\":"<<s.a15row<<",\"A15_relations\":"<<s.a15rel<<",\"candidates\":"<<n<<"}";
}

static int run_sweep(const std::string&states,const std::string&input,const std::string&label,const std::string&output){
 auto ins=load_bridges(input);std::ofstream f(output);if(!f)return 3;Counts total;Q expected_hash=0;size_t expected_n=0;
 f<<"{\n  \"schema\":\"variant-tail-stage-sweep-v1\",\n  \"ensemble\":\""<<label<<"\",\n  \"input\":\""<<input<<"\",\n  \"variant_states\":\""<<states<<"\",\n  \"variant_count\":"<<VARIANTS.size()<<",\n  \"bridge_count\":"<<ins.size()<<",\n  \"bridges\":[\n";
 for(size_t j=0;j<ins.size();j++){
  std::vector<Tail> tails;EarlyStats early;Counts c=sweep_one(ins[j],&tails,&early);add(total,c);Q h=tail_hash(tails);
  if(j==0){expected_hash=h;expected_n=tails.size();}else if(h!=expected_hash||tails.size()!=expected_n)throw std::runtime_error("bridge-specific candidate set changed unexpectedly");
  f<<"    {\"index\":"<<j<<",\"trial\":"<<ins[j].trial<<",\"variant_id\":"<<ins[j].variant_id<<",\"cv\":\""<<ins[j].raw_cv<<"\",\"record\":\""<<ins[j].raw_record<<"\"";
  if(ins[j].has_block)f<<",\"block\":\""<<ins[j].raw_block<<"\"";f<<",\"candidate_build\":";print_early(f,early,tails.size());f<<",\"stages\":";print_counts(f,c);f<<"}"<<(j+1==ins.size()?"\n":",\n");
 }
 f<<"  ],\n  \"candidate_count_per_bridge\":"<<expected_n<<",\n  \"candidate_fnv1a64\":\""<<std::hex<<std::setw(16)<<std::setfill('0')<<expected_hash<<std::dec<<"\",\n  \"aggregate_stages\":";print_counts(f,total);f<<"\n}\n";return 0;
}

struct Recon{std::array<U,8> cv{};std::array<U,4>w03{};};
static Recon reconstruct(const InputBridge&base,const Branch&b,const Tail&t,U e16,U e17,U e18,U e19){
 U e14=b.a(10)+b.e(10)+B1(b.e(13))+Ch(b.e(13),b.e(12),b.e(11))+K[14]+t.w14;
 U a14=e14-b.a(10)+B0(b.a(13))+Maj(b.a(13),b.a(12),b.a(11));
 U e15=b.a(11)+b.e(11)+B1(e14)+Ch(e14,b.e(13),b.e(12))+K[15]+t.w15;
 U a15=e15-b.a(11)+B0(a14)+Maj(a14,b.a(13),b.a(12));
 U w16=e16-b.a(12)-b.e(12)-B1(e15)-Ch(e15,e14,b.e(13))-K[16];
 U w17=e17-b.a(13)-b.e(13)-B1(e16)-Ch(e16,e15,e14)-K[17];
 U w18=e18-a14-e14-B1(e17)-Ch(e17,e16,e15)-K[18];
 U w19=e19-a15-e15-B1(e18)-Ch(e18,e17,e16)-K[19];
 U w3=w19-S1(w17)-b.w[12]-S0(b.w[4]);
 U w2=w18-S1(w16)-b.w[11]-S0(w3);
 U w1=w17-S1(t.w15)-b.w[10]-S0(w2);
 U w0=w16-S1(t.w14)-b.w[9]-S0(w1);
 U em1=b.e(3)-b.a(-1)-B1(b.e(2))-Ch(b.e(2),b.e(1),b.e(0))-K[3]-w3;
 U em2=b.e(2)-b.a(-2)-B1(b.e(1))-Ch(b.e(1),b.e(0),em1)-K[2]-w2;
 U em3=b.e(1)-b.a(-3)-B1(b.e(0))-Ch(b.e(0),em1,em2)-K[1]-w1;
 U em4=b.e(0)-b.a(-4)-B1(em1)-Ch(em1,em2,em3)-K[0]-w0;
 Recon z;for(int i=0;i<4;i++)z.cv[i]=base.cv[i];z.cv[4]=em1;z.cv[5]=em2;z.cv[6]=em3;z.cv[7]=em4;z.w03={w0,w1,w2,w3};return z;
}
static Q count_k(const std::array<U,8>&cv,const Record&r,U variant_id,const std::vector<Tail>&tails){
 auto b=derive(cv,r,variant_id);Q k=0;for(auto t:tails)if(success(test_tail(cv,b,t)))k++;return k;
}

static int run_importance(const std::string&states,const std::string&input,Q trials,Q seed,const std::string&label,const std::string&output){
 auto ins=load_bridges(input);std::vector<std::array<Branch,2>> bases;std::vector<Tail> tails;Q th=0;
 for(size_t i=0;i<ins.size();i++){
  auto b=derive(ins[i].cv,ins[i].r,ins[i].variant_id);EarlyStats st;auto t=candidates(b,&st);Q h=tail_hash(t);
  if(i==0){tails=t;th=h;}else if(h!=th||t.size()!=tails.size())throw std::runtime_error("non-common tail set");bases.push_back(b);
 }
 Domain d16(R_E16,{{28,1,0},{20,7,0},{20,2,0},{6,11,0},{30,12,1},{28,10,1},{10,29,1}});
 Domain d17(R_E17,{}),d18(R_E18,{{24,11,1},{2,16,0}}),d19(R_E19,{});
 int proposal_log2=d16.free_bits+d17.free_bits+d18.free_bits+d19.free_bits;
 if(proposal_log2!=101)throw std::runtime_error("proposal domain cardinality mismatch");
 RNG rng(seed);Counts stages,late_given_bridge;BridgeCounts bridge_stages;std::array<Q,NS> joint_bridge_late{};
 Q recon_ok=0,chosen_success=0,bridge_full=0,chosen_success_bridge=0;long double sum_inv_k=0,sum_inv_k2=0,sum_inv_k_bridge=0,sum_inv_k2_bridge=0;
 std::vector<Counts> base_stages(ins.size()),base_late_given_bridge(ins.size());std::vector<BridgeCounts> base_bridge_stages(ins.size());std::vector<std::array<Q,NS>> base_joint_bridge_late(ins.size());
 std::vector<Q> base_proposals(ins.size()),base_recon(ins.size()),base_successes(ins.size()),base_bridge_full(ins.size()),base_successes_bridge(ins.size());
 std::vector<long double> base_sum_inv_k(ins.size()),base_sum_inv_k_bridge(ins.size());std::vector<std::vector<Q>> base_k_values(ins.size());
 struct Hit{Q trial;size_t base,tail;Recon rec;U e16,e17,e18,e19;Q k;bool bridge;};std::vector<Hit> hits;
 for(Q q=0;q<trials;q++){
  size_t bi=rng.below(ins.size()),ti=rng.below(tails.size());base_proposals[bi]++;U e16=d16.sample(rng),e17=d17.sample(rng),e18=d18.sample(rng),e19=d19.sample(rng);
  Recon z=reconstruct(ins[bi],bases[bi][0],tails[ti],e16,e17,e18,e19);auto nb=derive(z.cv,ins[bi].r,ins[bi].variant_id);
  bool exact=true;for(int k=0;k<4;k++)exact&=nb[0].w[k]==z.w03[k];if(!exact)throw std::runtime_error("proposal reconstruction failed");recon_ok++;base_recon[bi]++;
  BridgeTest bridge_test=test_bridge(nb);update(bridge_stages,bridge_test);update(base_bridge_stages[bi],bridge_test);bool bridge_ok=bridge_success(bridge_test);
  Test test=test_tail(z.cv,nb,tails[ti]);update(stages,test);update(base_stages[bi],test);
  if(bridge_ok){bridge_full++;base_bridge_full[bi]++;update(late_given_bridge,test);update(base_late_given_bridge[bi],test);for(int i=0;i<NS;i++)if(test.ok[i]){joint_bridge_late[i]++;base_joint_bridge_late[bi][i]++;}}
  if(success(test)){
   Q kval=count_k(z.cv,ins[bi].r,ins[bi].variant_id,tails);if(!kval)throw std::runtime_error("successful selected tail has K=0");chosen_success++;base_successes[bi]++;base_k_values[bi].push_back(kval);long double x=1.0L/kval;sum_inv_k+=x;sum_inv_k2+=x*x;base_sum_inv_k[bi]+=x;
   if(bridge_ok){chosen_success_bridge++;base_successes_bridge[bi]++;sum_inv_k_bridge+=x;sum_inv_k2_bridge+=x*x;base_sum_inv_k_bridge[bi]+=x;}
   hits.push_back({q,bi,ti,z,e16,e17,e18,e19,kval,bridge_ok});
  }
 }
 long double weight=std::ldexp(1.0L,proposal_log2-128);long double factor=tails.size()*weight;
 long double pi=factor*sum_inv_k/trials;long double second=factor*factor*sum_inv_k2/trials;long double var=trials>1?(second-pi*pi)*trials/(trials-1):0;long double se=std::sqrt(std::max((long double)0,var)/trials);
 long double pi_bridge=factor*sum_inv_k_bridge/trials;long double second_bridge=factor*factor*sum_inv_k2_bridge/trials;long double var_bridge=trials>1?(second_bridge-pi_bridge*pi_bridge)*trials/(trials-1):0;long double se_bridge=std::sqrt(std::max((long double)0,var_bridge)/trials);
 std::ofstream f(output);if(!f)return 3;f<<std::setprecision(18);
 f<<"{\n  \"schema\":\"variant-tail-importance-v1\",\n  \"ensemble\":\""<<label<<"\",\n  \"input\":\""<<input<<"\",\n  \"variant_states\":\""<<states<<"\",\n  \"variant_count\":"<<VARIANTS.size()<<",\n  \"seed\":"<<seed<<",\n  \"trials\":"<<trials<<",\n  \"bridge_count\":"<<ins.size()<<",\n";
 f<<"  \"tail_count\":"<<tails.size()<<",\n  \"tail_fnv1a64\":\""<<std::hex<<std::setw(16)<<std::setfill('0')<<th<<std::dec<<"\",\n";
 f<<"  \"reconstructed_E_halves\":\"abstract; no standard-IV first-block preimage is known\",\n";
 f<<"  \"proposal\":{\"dimensions\":[\"E16_with_relations\",\"E17\",\"E18_with_relations\",\"E19\"],\"domain_log2\":["<<d16.free_bits<<","<<d17.free_bits<<","<<d18.free_bits<<","<<d19.free_bits<<"],\"joint_domain_log2\":"<<proposal_log2<<",\"likelihood_ratio\":"<<double(weight)<<",\"likelihood_ratio_power2\":-27},\n";
 f<<"  \"reconstruction_pass\":"<<recon_ok<<",\n  \"bridge_filter_scope\":\"exact Figure 6 W4-W6 rows and relations; W0-W3 equality is guaranteed by each selected A half and checked by derive\",\n";
 f<<"  \"bridge_stage_counts\":";print_counts(f,bridge_stages);f<<",\n  \"full_bridge_pass_under_proposal\":"<<bridge_full<<",\n";
 f<<"  \"stage_counts\":";print_counts(f,stages);f<<",\n  \"late_stage_counts_given_full_bridge_under_proposal\":";print_counts(f,late_given_bridge);f<<",\n";
 f<<"  \"bridge_and_late_marginal\":[";for(int i=0;i<NS;i++){if(i)f<<",";f<<"{\"name\":\""<<SN[i]<<"\",\"denominator\":"<<trials<<",\"bridge_pass\":"<<bridge_full<<",\"late_pass\":"<<stages.marginal[i]<<",\"joint_pass\":"<<joint_bridge_late[i]<<"}";}f<<"],\n  \"chosen_tail_successes\":"<<chosen_success<<",\n";
 f<<"  \"sum_inverse_K\":"<<double(sum_inv_k)<<",\n  \"pi_uniform_estimate\":"<<double(pi)<<",\n  \"monte_carlo_standard_error\":"<<double(se)<<",\n";
 f<<"  \"chosen_tail_successes_with_full_bridge\":"<<chosen_success_bridge<<",\n  \"sum_inverse_K_with_full_bridge\":"<<double(sum_inv_k_bridge)<<",\n";
 f<<"  \"uniform_E_probability_mass_estimate_bridge_and_path_union\":"<<double(pi_bridge)<<",\n  \"bridge_and_path_monte_carlo_standard_error\":"<<double(se_bridge)<<",\n";
 f<<"  \"calibrated_confidence_interval\":null,\n  \"per_base\":[\n";
 for(size_t i=0;i<ins.size();i++){
  f<<"    {\"base_bridge_index\":"<<i<<",\"base_trial\":"<<ins[i].trial<<",\"variant_id\":"<<ins[i].variant_id<<",\"source_cv\":\""<<ins[i].raw_cv<<"\",\"record\":\""<<ins[i].raw_record<<"\",\"proposal_count\":"<<base_proposals[i]<<",\"reconstruction_pass\":"<<base_recon[i]<<",\"bridge_stage_counts\":";print_counts(f,base_bridge_stages[i]);
  f<<",\"full_bridge_pass_under_proposal\":"<<base_bridge_full[i]<<",\"stage_counts\":";print_counts(f,base_stages[i]);f<<",\"late_stage_counts_given_full_bridge_under_proposal\":";print_counts(f,base_late_given_bridge[i]);
  f<<",\"bridge_and_late_marginal\":[";for(int k=0;k<NS;k++){if(k)f<<",";f<<"{\"name\":\""<<SN[k]<<"\",\"joint_pass\":"<<base_joint_bridge_late[i][k]<<"}";}f<<"],\"chosen_tail_successes\":"<<base_successes[i]<<",\"sum_inverse_K\":"<<double(base_sum_inv_k[i])<<",\"chosen_tail_successes_with_full_bridge\":"<<base_successes_bridge[i]<<",\"sum_inverse_K_with_full_bridge\":"<<double(base_sum_inv_k_bridge[i])<<",\"K_values\":[";for(size_t j=0;j<base_k_values[i].size();j++){if(j)f<<",";f<<base_k_values[i][j];}f<<"]}"<<(i+1==ins.size()?"\n":",\n");
 }
 f<<"  ],\n  \"successes\":[\n";
 for(size_t i=0;i<hits.size();i++){auto&h=hits[i];f<<"    {\"trial\":"<<h.trial<<",\"base_bridge_index\":"<<h.base<<",\"base_trial\":"<<ins[h.base].trial<<",\"variant_id\":"<<ins[h.base].variant_id<<",\"cv\":\""<<cvhex(h.rec.cv)<<"\",\"record\":\""<<ins[h.base].raw_record<<"\",\"tail_index\":"<<h.tail<<",\"tail\":\""<<hx(tails[h.tail].w14)<<hx(tails[h.tail].w15)<<"\",\"E16\":\""<<hx(h.e16)<<"\",\"E17\":\""<<hx(h.e17)<<"\",\"E18\":\""<<hx(h.e18)<<"\",\"E19\":\""<<hx(h.e19)<<"\",\"full_bridge\":"<<(h.bridge?"true":"false")<<",\"K\":"<<h.k<<"}"<<(i+1==hits.size()?"\n":",\n");}
 f<<"  ]\n}\n";return 0;
}

int main(int argc,char**argv){
 try{
  if(argc<3)throw std::runtime_error("usage: variant_tail_measure sweep STATES INPUT LABEL OUTPUT | importance STATES INPUT TRIALS SEED LABEL OUTPUT");
  std::string mode=argv[1];load_variants(argv[2]);
  if(mode=="sweep"&&argc==6)return run_sweep(argv[2],argv[3],argv[4],argv[5]);
  if(mode=="importance"&&argc==8)return run_importance(argv[2],argv[3],std::strtoull(argv[4],nullptr,0),std::strtoull(argv[5],nullptr,0),argv[6],argv[7]);
  throw std::runtime_error("bad arguments");
 }catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 2;}
}
```

### Fixed-slice scalar oracle dependency

Embedded source SHA-256: `b25fc1b2a98afdae956486bdfe9a49d1582e2206a093f3f84d8b8c1ddaf5258a`.

Source-file SHA-256 after restoring the single final LF: `0c864b703d0f5d1d9f3d37642e445dc802d9d457c01f433269afd4badfb66f73`.

```python
#!/usr/bin/env python3
"""Independent scalar oracle for the corrected Figure 6 SHA-256 tail.

The state convention is the paper's: after round i, the two state words that
receive new values are A_i and E_i.  Before round zero the chaining words are
(A_-1,A_-2,A_-3,A_-4,E_-1,E_-2,E_-3,E_-4).
"""

from __future__ import annotations

import argparse
import json
import random
import struct
from pathlib import Path

MASK = 0xFFFFFFFF
HERE = Path(__file__).resolve().parent
COND = json.loads((HERE / "figure6-tail.json").read_text())
ROWS = COND["rows"]

IV = (
    0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
    0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19,
)
K = (
    0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5,
    0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
    0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3,
    0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
    0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC,
    0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
    0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7,
    0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
    0x27B70A85, 0x2E1B2138, 0x4D2C6DFC,
)

A_FIXED = (
    tuple(int(x, 16) for x in "66e7ba7c 5ff9d9f8 9123b13f b8560dbb 677e1e2a 9bcf7bbe f8677ad6 4a299906 44d24ab4 39781650 6c206d58 35c5c2b8 0508c8f0".split()),
    tuple(int(x, 16) for x in "66e7ba7c 5ff9d9f8 9123b13f 98560dbb 633b16ba 9bcf7bbe f8677ad6 4a299906 44f24ab5 39781650 6422edc8 574542b8 0508c8f0".split()),
)
E_FIXED = (
    tuple(int(x, 16) for x in "58f38fac b95f2294 87431160 11cae594 d504bf23 7f27d24c bf893f69 2300f189 fcc08ef5".split()),
    tuple(int(x, 16) for x in "5caf87bc a94f0a01 a7421160 f1cae594 d0e1b7b4 bf27d74c b78bbfd9 3fffd0f9 bf81c0f4".split()),
)
W_FIXED = (
    tuple(int(x, 16) for x in "5100da8a 0912e57b a96b2054 45f2222c 4d12f88a".split()),
    tuple(int(x, 16) for x in "5100da8a 0912e57b a96b2054 41b22a2c 6d12f88a".split()),
)


def ror(x: int, n: int) -> int:
    return ((x >> n) | (x << (32 - n))) & MASK


def big0(x: int) -> int:
    return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)


def big1(x: int) -> int:
    return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)


def small0(x: int) -> int:
    return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)


def small1(x: int) -> int:
    return ror(x, 17) ^ ror(x, 19) ^ (x >> 10)


def ch(x: int, y: int, z: int) -> int:
    return z ^ (x & (y ^ z))


def maj(x: int, y: int, z: int) -> int:
    return (x & y) | (z & (x | y))


def bit(x: int, i: int) -> int:
    return (x >> i) & 1


def row_pair(row: str, x: int) -> tuple[int, int]:
    delta = sum(1 << (31 - j) for j, c in enumerate(row) if c in "un")
    return x, x ^ delta


def row_ok(row: str, x: int, xp: int) -> bool:
    for j, c in enumerate(row):
        b, bp = bit(x, 31 - j), bit(xp, 31 - j)
        if c == "=" and b != bp:
            return False
        if c == "0" and (b or bp):
            return False
        if c == "1" and (not b or not bp):
            return False
        if c == "u" and (b or not bp):
            return False
        if c == "n" and (not b or bp):
            return False
    return True


def row_values(row: str):
    positions = [31 - j for j, c in enumerate(row) if c == "="]
    base = sum(1 << (31 - j) for j, c in enumerate(row) if c in "1n")
    delta = sum(1 << (31 - j) for j, c in enumerate(row) if c in "un")
    for assignment in range(1 << len(positions)):
        x = base
        for j, pos in enumerate(positions):
            x |= ((assignment >> j) & 1) << pos
        yield x, x ^ delta


def relations_ok(name: str, x: int) -> bool:
    rel = COND["relations"].get(name, {})
    return (all(bit(x, a) == bit(x, b) for a, b in rel.get("equal", ())) and
            all(bit(x, a) != bit(x, b) for a, b in rel.get("unequal", ())))


def expand(words: list[int], rounds: int) -> list[int]:
    w = list(words)
    for i in range(16, rounds):
        w.append((small1(w[i - 2]) + w[i - 7] + small0(w[i - 15]) + w[i - 16]) & MASK)
    return w


def trace(cv: tuple[int, ...], words: list[int] | tuple[int, ...], rounds: int = 32):
    """Return paper-indexed A/E dictionaries, expanded W, and feed-forward CV."""
    w = expand(list(words), rounds)
    a = {i: cv[-1 - i] for i in range(-4, 0)}
    e = {i: cv[3 - i] for i in range(-4, 0)}
    for i in range(rounds):
        e[i] = (a[i - 4] + e[i - 4] + big1(e[i - 1]) +
                ch(e[i - 1], e[i - 2], e[i - 3]) + K[i] + w[i]) & MASK
        a[i] = (e[i] - a[i - 4] + big0(a[i - 1]) +
                maj(a[i - 1], a[i - 2], a[i - 3])) & MASK
    out = tuple((cv[j] + (a[rounds - 1 - j] if j < 4 else e[rounds + 3 - j])) & MASK
                for j in range(8))
    return a, e, w, out


def parse_words(value: str) -> tuple[int, ...]:
    value = value.strip().replace(" ", "")
    if len(value) % 8:
        raise ValueError("word string length is not divisible by 8")
    return tuple(int(value[i:i + 8], 16) for i in range(0, len(value), 8))


def derive_bridge(cv: tuple[int, ...], record: tuple[int, ...]):
    """Rebuild W0..W13 and the fixed states from an explicit CV+record."""
    key, w7, w8, e3, e4, a0 = record
    if key != cv[0]:
        raise ValueError("record key differs from CV A_-1")
    branches = []
    for p in range(2):
        a = {i: cv[-1 - i] for i in range(-4, 0)}
        e = {i: cv[3 - i] for i in range(-4, 0)}
        a.update({i: x for i, x in enumerate(A_FIXED[p], 1)})
        e.update({i: x for i, x in enumerate(E_FIXED[p], 5)})
        a[0] = a0
        e[3] = e3
        e[4] = e4 ^ (0x20000000 if p else 0)
        e[2] = (a[2] + a[-2] - big0(a[1]) - maj(a[1], a[0], a[-1])) & MASK
        e[1] = (a[1] + a[-3] - big0(a[0]) - maj(a[0], a[-1], a[-2])) & MASK
        e[0] = (a[0] + a[-4] - big0(a[-1]) - maj(a[-1], a[-2], a[-3])) & MASK
        w = []
        for i in range(7):
            w.append((e[i] - a[i - 4] - e[i - 4] - big1(e[i - 1]) -
                      ch(e[i - 1], e[i - 2], e[i - 3]) - K[i]) & MASK)
        w.extend((row_pair("=======n=======u===u====u=1=u=u=", w7)[p],
                  row_pair("============u=======uu==========", w8)[p]))
        w.extend(W_FIXED[p])
        branches.append((a, e, w))
    if branches[0][2][:4] != branches[1][2][:4]:
        raise ValueError("bridge fails W0..W3 equality")
    return branches


def _a14_ok(a14: int, a13: int) -> bool:
    rel = COND["relations"]["A14"]
    return (relations_ok("A14", a14) and
            all(bit(a14, dst) == bit(a13, src) for src, dst in rel["equal_A13"]) and
            all(bit(a14, dst) != bit(a13, src) for src, dst in rel["unequal_A13"]))


def _a15_ok(a15: int, a13: int, a6: int) -> bool:
    rel = COND["relations"]["A15"]
    return (all(bit(a15, dst) != bit(a13, src) for src, dst in rel["unequal_A13"]) and
            all(bit(a15, dst) != bit(a6, src) for src, dst in rel["unequal_A6"]))


def candidate_tails(branches):
    """Enumerate the corrected, bridge-local W14/W15 choices."""
    (a, e, _), (ap, ep, _) = branches
    out = []
    stages = {name: 0 for name in (
        "E14_domain", "W14_equal", "A14_row", "A14_relations",
        "E15_domain", "W15_equal", "A15_row", "A15_relations", "candidates")}
    e15_domain = tuple(row_values(ROWS["E15"]))
    for e14, e14p in row_values(ROWS["E14"]):
        stages["E14_domain"] += 1
        a14 = (e14 - a[10] + big0(a[13]) + maj(a[13], a[12], a[11])) & MASK
        a14p = (e14p - ap[10] + big0(ap[13]) + maj(ap[13], ap[12], ap[11])) & MASK
        w14 = (e14 - a[10] - e[10] - big1(e[13]) - ch(e[13], e[12], e[11]) - K[14]) & MASK
        w14p = (e14p - ap[10] - ep[10] - big1(ep[13]) - ch(ep[13], ep[12], ep[11]) - K[14]) & MASK
        if w14 != w14p:
            continue
        stages["W14_equal"] += 1
        if not row_ok(ROWS["A14"], a14, a14p):
            continue
        stages["A14_row"] += 1
        if not _a14_ok(a14, a[13]):
            continue
        stages["A14_relations"] += 1
        for e15, e15p in e15_domain:
            stages["E15_domain"] += 1
            a15 = (e15 - a[11] + big0(a14) + maj(a14, a[13], a[12])) & MASK
            a15p = (e15p - ap[11] + big0(a14p) + maj(a14p, ap[13], ap[12])) & MASK
            w15 = (e15 - a[11] - e[11] - big1(e14) - ch(e14, e[13], e[12]) - K[15]) & MASK
            w15p = (e15p - ap[11] - ep[11] - big1(e14p) - ch(e14p, ep[13], ep[12]) - K[15]) & MASK
            if w15 != w15p:
                continue
            stages["W15_equal"] += 1
            if not row_ok(ROWS["A15"], a15, a15p):
                continue
            stages["A15_row"] += 1
            if not _a15_ok(a15, a[13], a[6]):
                continue
            stages["A15_relations"] += 1
            out.append((w14, w15))
    stages["candidates"] = len(out)
    return out, stages


STAGE_NAMES = (
    "A16_row", "E16_row", "E16_relations", "E17_row", "E18_row",
    "E18_relations", "E19_row", "E20_row", "W20_row", "W20_relations",
    "W22_row", "W22_relations", "C32_collision",
)


def late_stage_results(cv: tuple[int, ...], words: tuple[int, ...], wordsp: tuple[int, ...]):
    a, e, w, out = trace(cv, words, 32)
    ap, ep, wp, outp = trace(cv, wordsp, 32)
    values = {
        "A16_row": row_ok(ROWS["A16"], a[16], ap[16]),
        "E16_row": row_ok(ROWS["E16"], e[16], ep[16]),
        "E16_relations": relations_ok("E16", e[16]),
        "E17_row": row_ok(ROWS["E17"], e[17], ep[17]),
        "E18_row": row_ok(ROWS["E18"], e[18], ep[18]),
        "E18_relations": relations_ok("E18", e[18]),
        "E19_row": row_ok(ROWS["E19"], e[19], ep[19]),
        "E20_row": row_ok(ROWS["E20"], e[20], ep[20]),
        "W20_row": row_ok(ROWS["W20"], w[20], wp[20]),
        "W20_relations": relations_ok("W20", w[20]),
        "W22_row": row_ok(ROWS["W22"], w[22], wp[22]),
        "W22_relations": relations_ok("W22", w[22]),
        "C32_collision": out == outp,
    }
    return values, (a, e, w, out), (ap, ep, wp, outp)


def reconstruct_cv_for_proposal(a_half: tuple[int, ...], branch, tail,
                                e16: int, e17: int, e18: int, w3: int,
                                wrong_w18_index: bool = False):
    """Invert (E16,E17,E18,W3) to W0..W3 and then the four CV E words."""
    a, e, wprefix = branch
    w14, w15 = tail
    e14 = (a[10] + e[10] + big1(e[13]) + ch(e[13], e[12], e[11]) + K[14] + w14) & MASK
    a14 = (e14 - a[10] + big0(a[13]) + maj(a[13], a[12], a[11])) & MASK
    e15 = (a[11] + e[11] + big1(e14) + ch(e14, e[13], e[12]) + K[15] + w15) & MASK
    a15 = (e15 - a[11] + big0(a14) + maj(a14, a[13], a[12])) & MASK
    w16 = (e16 - a[12] - e[12] - big1(e15) - ch(e15, e14, e[13]) - K[16]) & MASK
    a16 = (e16 - a[12] + big0(a15) + maj(a15, a14, a[13])) & MASK
    w17 = (e17 - a[13] - e[13] - big1(e16) - ch(e16, e15, e14) - K[17]) & MASK
    w18 = (e18 - a14 - e14 - big1(e17) - ch(e17, e16, e15) - K[18]) & MASK
    w2 = (w18 - small1(w16) - (wprefix[10] if wrong_w18_index else wprefix[11]) - small0(w3)) & MASK
    w1 = (w17 - small1(w15) - wprefix[10] - small0(w2)) & MASK
    w0 = (w16 - small1(w14) - wprefix[9] - small0(w1)) & MASK

    # A0..A3 and E0..E3 are fixed by the table record and the accepted A half.
    em1 = (e[3] - a[-1] - big1(e[2]) - ch(e[2], e[1], e[0]) - K[3] - w3) & MASK
    em2 = (e[2] - a[-2] - big1(e[1]) - ch(e[1], e[0], em1) - K[2] - w2) & MASK
    em3 = (e[1] - a[-3] - big1(e[0]) - ch(e[0], em1, em2) - K[1] - w1) & MASK
    em4 = (e[0] - a[-4] - big1(em1) - ch(em1, em2, em3) - K[0] - w0) & MASK
    cv = tuple(a_half) + (em1, em2, em3, em4)
    return cv, (w0, w1, w2, w3), (w16, w17, w18), (a14, a15, a16, e14, e15)


def paper_fixture():
    data = json.loads((HERE / "inputs" / "sha256-r32-paper-inputs.json").read_text())
    m0 = parse_words(data["M0_words"])
    m1 = parse_words(data["M1_words"])
    m1p = parse_words(data["M1_prime_words"])
    _, _, _, cv35 = trace(IV, m0, 35)
    return m0, m1, m1p, cv35


def self_test(seed: int = 2026100504):
    m0, m1, m1p, cv = paper_fixture()
    stages, left, right = late_stage_results(cv, m1, m1p)
    a, e, _, _ = left
    record = (cv[0], m1[7], m1[8], e[3], e[4], a[0])
    branches = derive_bridge(cv, record)
    assert tuple(branches[0][2]) == m1[:14], "Table3_unprimed_prefix_replay"
    assert tuple(branches[1][2]) == m1p[:14], "Table3_primed_prefix_replay"
    tails, early = candidate_tails(branches)
    table_tail = (m1[14], m1[15])
    assert table_tail in tails, "Table3_tail_in_candidate_set"
    for stage_name, passed in stages.items():
        assert passed, f"Table3_{stage_name}"

    # Disposable condition perturbation: Table 3 has E20 bit 29 = 1.
    perturbed = list(ROWS["E20"])
    perturbed[2] = "0"
    perturb_name = "control_perturbed_E20_bit29_zero"
    perturb_pass = row_ok("".join(perturbed), left[1][20], right[1][20])
    assert not perturb_pass, perturb_name

    # Audit both directions of the triangular map on unconstrained random words.
    rng = random.Random(seed)
    bijection_cases = 128
    for _ in range(bijection_cases):
        target = tuple(rng.getrandbits(32) for _ in range(3))
        w3 = rng.getrandbits(32)
        new_cv, w03, _, _ = reconstruct_cv_for_proposal(cv[:4], branches[0], table_tail, *target, w3)
        rebuilt = derive_bridge(new_cv, record)
        words = tuple(rebuilt[0][2]) + table_tail
        _, et, wt, _ = trace(new_cv, words, 19)
        assert tuple(et[i] for i in range(16, 19)) == target, "bijection_forward_backward_E16_E18"
        assert tuple(wt[:4]) == w03, "bijection_forward_backward_W0_W3"

    target = tuple(rng.getrandbits(32) for _ in range(3))
    w3 = rng.getrandbits(32)
    bad_cv, _, _, _ = reconstruct_cv_for_proposal(
        cv[:4], branches[0], table_tail, *target, w3, wrong_w18_index=True)
    bad_branch = derive_bridge(bad_cv, record)[0]
    _, bad_e, _, _ = trace(bad_cv, tuple(bad_branch[2]) + table_tail, 19)
    wrong_control = tuple(bad_e[i] for i in range(16, 19)) == target
    assert not wrong_control, "control_wrong_schedule_W18_uses_W10"

    return {
        "oracle": "tail_oracle.py",
        "table3": {
            "cv35": "".join(f"{x:08x}" for x in cv),
            "record": "".join(f"{x:08x}" for x in record),
            "tail": "".join(f"{x:08x}" for x in table_tail),
            "stage_results": stages,
            "c32_output": "".join(f"{x:08x}" for x in left[3]),
            "candidate_count": len(tails),
            "candidate_stages": early,
        },
        "controls": {
            perturb_name: perturb_pass,
            "control_wrong_schedule_W18_uses_W10": wrong_control,
        },
        "bijection_random_cases": bijection_cases,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = self_test()
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
```

### Independent variant-aware scalar oracle

Embedded source SHA-256: `9ca91afd4ba3d57e06bb10e5b6ab07db953087955a57db37a4c96e747a589d7f`.

Source-file SHA-256 after restoring the single final LF: `2251751e0ae00636a90e78c0f1a316033558f26d1ff422170f0b95fddae23ed8`.

```python
#!/usr/bin/env python3
"""Scalar variant-aware oracle for the repaired SHA-256 Figure 6 tail."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import struct
from pathlib import Path

import tail_oracle as fixed


HERE = Path(__file__).resolve().parent
DEFAULT_MAPPING = HERE / "variant_inputs" / "repaired-variant-mapping.json"
DEFAULT_STATES = HERE / "variant_inputs" / "repaired-variant-states.bin"
DEFAULT_PILOT = HERE / "variant_inputs" / "repaired-sampler-conditional-pilot.jsonl"
MASK = 0xFFFFFFFF


def _words(values):
    return tuple(int(value, 16) for value in values)


def load_mapping(path: Path):
    raw = json.loads(path.read_text())
    common = raw["common_fixed_state"]
    variants = {}
    for item in raw["variants"]:
        variant_id = item["variant_id"]
        assert variant_id not in variants, "variant_mapping_duplicate_id"
        variants[variant_id] = {
            "is_table3": item["is_table3"],
            "a": tuple(_words(item["A1_A3"][side]) for side in ("left", "right")),
            "e": tuple(_words(item["E5_E7"][side]) for side in ("left", "right")),
            "w": tuple(_words(item["W9_W13"][side]) for side in ("left", "right")),
        }
    common_state = {
        "a": tuple(_words(common["A4_A13"][side]) for side in ("left", "right")),
        "e": tuple(_words(common["E8_E13"][side]) for side in ("left", "right")),
    }
    return raw, variants, common_state


def load_binary_states(path: Path):
    data = path.read_bytes()
    assert data[:4] == b"RVS1", "variant_binary_magic"
    count = struct.unpack_from(">I", data, 4)[0]
    offset = 8
    variants = {}
    for _ in range(count):
        words = struct.unpack_from(">23I", data, offset)
        offset += 23 * 4
        variant_id = words[0]
        assert variant_id not in variants, "variant_binary_duplicate_id"
        variants[variant_id] = {
            "a": (tuple(words[1:4]), tuple(words[4:7])),
            "e": (tuple(words[7:10]), tuple(words[10:13])),
            "w": (tuple(words[13:18]), tuple(words[18:23])),
        }
    assert offset == len(data), "variant_binary_trailing_bytes"
    assert list(variants) == sorted(variants), "variant_binary_id_order"
    return variants


def load_pilot_accepts(path: Path):
    accepts = []
    for line in path.read_text().splitlines():
        row = json.loads(line)
        if row.get("kind") == "accepted":
            accepts.append(row)
    assert accepts, "conditional_pilot_has_accept"
    return accepts


def derive_bridge(cv, record, variant, common):
    """Rebuild W0..W13 for one repaired variant and explicit CV+record."""
    key, w7, w8, e3, e4, a0 = record
    if key != cv[0]:
        raise ValueError("record key differs from CV A_-1")
    branches = []
    for branch in range(2):
        a = {index: cv[-1 - index] for index in range(-4, 0)}
        e = {index: cv[3 - index] for index in range(-4, 0)}
        a.update({index: value for index, value in enumerate(variant["a"][branch], 1)})
        a.update({index: value for index, value in enumerate(common["a"][branch], 4)})
        e.update({index: value for index, value in enumerate(variant["e"][branch], 5)})
        e.update({index: value for index, value in enumerate(common["e"][branch], 8)})
        a[0] = a0
        e[3] = e3
        e[4] = e4 ^ (0x20000000 if branch else 0)
        e[2] = (a[2] + a[-2] - fixed.big0(a[1]) - fixed.maj(a[1], a[0], a[-1])) & MASK
        e[1] = (a[1] + a[-3] - fixed.big0(a[0]) - fixed.maj(a[0], a[-1], a[-2])) & MASK
        e[0] = (a[0] + a[-4] - fixed.big0(a[-1]) - fixed.maj(a[-1], a[-2], a[-3])) & MASK
        words = []
        for index in range(7):
            words.append((e[index] - a[index - 4] - e[index - 4]
                          - fixed.big1(e[index - 1])
                          - fixed.ch(e[index - 1], e[index - 2], e[index - 3])
                          - fixed.K[index]) & MASK)
        words.extend((fixed.row_pair("=======n=======u===u====u=1=u=u=", w7)[branch],
                      fixed.row_pair("============u=======uu==========", w8)[branch]))
        words.extend(variant["w"][branch])
        branches.append((a, e, words))
    assert branches[0][2][:4] == branches[1][2][:4], "variant_bridge_W0_W3_equality"
    return branches


def bridge_stage_results(branches):
    left, right = branches
    words, wordsp = left[2], right[2]
    return {
        "W4_row": fixed.row_ok("==n=============================", words[4], wordsp[4]),
        "W4_relations": (fixed.bit(words[4], 1) != fixed.bit(words[4], 12)
                         and fixed.bit(words[4], 8) != fixed.bit(words[4], 25)
                         and fixed.bit(words[4], 18) == fixed.bit(words[4], 14)),
        "W5_row": fixed.row_ok("=====u===u==========n===========", words[5], wordsp[5]),
        "W5_relations": (fixed.bit(words[5], 0) == fixed.bit(words[5], 28)
                         and fixed.bit(words[5], 1) == fixed.bit(words[5], 18)
                         and fixed.bit(words[5], 30) == fixed.bit(words[5], 9)),
        "W6_row": fixed.row_ok("==n=============================", words[6], wordsp[6]),
        "W6_relations": (fixed.bit(words[6], 1) == fixed.bit(words[6], 12)
                         and fixed.bit(words[6], 8) == fixed.bit(words[6], 25)
                         and fixed.bit(words[6], 18) != fixed.bit(words[6], 14)),
    }


def reconstruct_e19(a_half, branch, tail, e16, e17, e18, e19):
    """Invert E16..E19 to W0..W3, then to the incoming E half."""
    a, e, words = branch
    w14, w15 = tail
    e14 = (a[10] + e[10] + fixed.big1(e[13])
           + fixed.ch(e[13], e[12], e[11]) + fixed.K[14] + w14) & MASK
    a14 = (e14 - a[10] + fixed.big0(a[13])
           + fixed.maj(a[13], a[12], a[11])) & MASK
    e15 = (a[11] + e[11] + fixed.big1(e14)
           + fixed.ch(e14, e[13], e[12]) + fixed.K[15] + w15) & MASK
    a15 = (e15 - a[11] + fixed.big0(a14)
           + fixed.maj(a14, a[13], a[12])) & MASK
    w16 = (e16 - a[12] - e[12] - fixed.big1(e15)
           - fixed.ch(e15, e14, e[13]) - fixed.K[16]) & MASK
    w17 = (e17 - a[13] - e[13] - fixed.big1(e16)
           - fixed.ch(e16, e15, e14) - fixed.K[17]) & MASK
    w18 = (e18 - a14 - e14 - fixed.big1(e17)
           - fixed.ch(e17, e16, e15) - fixed.K[18]) & MASK
    w19 = (e19 - a15 - e15 - fixed.big1(e18)
           - fixed.ch(e18, e17, e16) - fixed.K[19]) & MASK
    w3 = (w19 - fixed.small1(w17) - words[12] - fixed.small0(words[4])) & MASK
    w2 = (w18 - fixed.small1(w16) - words[11] - fixed.small0(w3)) & MASK
    w1 = (w17 - fixed.small1(w15) - words[10] - fixed.small0(w2)) & MASK
    w0 = (w16 - fixed.small1(w14) - words[9] - fixed.small0(w1)) & MASK
    em1 = (e[3] - a[-1] - fixed.big1(e[2]) - fixed.ch(e[2], e[1], e[0])
           - fixed.K[3] - w3) & MASK
    em2 = (e[2] - a[-2] - fixed.big1(e[1]) - fixed.ch(e[1], e[0], em1)
           - fixed.K[2] - w2) & MASK
    em3 = (e[1] - a[-3] - fixed.big1(e[0]) - fixed.ch(e[0], em1, em2)
           - fixed.K[1] - w1) & MASK
    em4 = (e[0] - a[-4] - fixed.big1(em1) - fixed.ch(em1, em2, em3)
           - fixed.K[0] - w0) & MASK
    return tuple(a_half) + (em1, em2, em3, em4), (w0, w1, w2, w3)


def _hex_words(value):
    return fixed.parse_words(value)


def _tail_sha256(tails):
    digest = hashlib.sha256()
    for tail in tails:
        digest.update(struct.pack(">II", *tail))
    return digest.hexdigest()


def _prefix_replay(cv, branches, variant, common, label):
    for branch, (a_expected, e_expected, words) in enumerate(branches):
        a, e, expanded, _ = fixed.trace(cv, words, 14)
        assert tuple(expanded[:14]) == tuple(words), f"{label}_schedule_prefix"
        expected_a = variant["a"][branch] + common["a"][branch]
        expected_e = variant["e"][branch] + common["e"][branch]
        assert tuple(a[index] for index in range(1, 14)) == expected_a, f"{label}_A1_A13"
        assert tuple(e[index] for index in range(5, 14)) == expected_e, f"{label}_E5_E13"


def self_test(mapping_path: Path, states_path: Path, pilot_path: Path,
              seed: int = 2026100520):
    raw_mapping, variants, common = load_mapping(mapping_path)
    binary_variants = load_binary_states(states_path)
    assert len(variants) == 65, "variant_mapping_count"
    table3_ids = [variant_id for variant_id, item in variants.items() if item["is_table3"]]
    assert len(table3_ids) == 1, "variant_mapping_single_Table3"
    table3_id = table3_ids[0]

    m0, m1, m1p, cv35 = fixed.paper_fixture()
    del m0
    # Record fields are key,W7,W8,E3,E4,A0.
    traced_a, traced_e, _, _ = fixed.trace(cv35, m1, 14)
    table_record = (cv35[0], m1[7], m1[8], traced_e[3], traced_e[4], traced_a[0])
    table_branches = derive_bridge(cv35, table_record, variants[table3_id], common)
    assert tuple(table_branches[0][2]) == m1[:14], "Table3_variant_prefix_replay_unprimed"
    assert tuple(table_branches[1][2]) == m1p[:14], "Table3_variant_prefix_replay_primed"
    _prefix_replay(cv35, table_branches, variants[table3_id], common, "Table3_variant_prefix")
    table_bridge = bridge_stage_results(table_branches)
    assert all(table_bridge.values()), "Table3_variant_bridge_stages"
    table_tails, table_build = fixed.candidate_tails(table_branches)
    table_tail = (m1[14], m1[15])
    assert len(table_tails) == 196608, "Table3_variant_tail_count"
    assert table_tail in table_tails, "Table3_variant_tail_present"
    table_stages, table_left, table_right = fixed.late_stage_results(cv35, m1, m1p)
    assert all(table_stages.values()), "Table3_variant_full_C32_collision"

    accepts = load_pilot_accepts(pilot_path)
    pilot = next(row for row in accepts if row["variant_id"] != table3_id)
    pilot_id = pilot["variant_id"]
    pilot_cv = _hex_words(pilot["cv"])
    pilot_record = _hex_words(pilot["record"])
    assert len(pilot_record) == 6, "non_Table3_record_word_count"
    pilot_branches = derive_bridge(pilot_cv, pilot_record, variants[pilot_id], common)
    _prefix_replay(pilot_cv, pilot_branches, variants[pilot_id], common,
                   "non_Table3_conditional_pilot_prefix")
    pilot_bridge = bridge_stage_results(pilot_branches)
    assert all(pilot_bridge.values()), "non_Table3_conditional_pilot_bridge_stages"
    pilot_tails, pilot_build = fixed.candidate_tails(pilot_branches)
    assert pilot_tails == table_tails, "variant_common_ordered_tail_domain"

    rng = random.Random(seed)
    inverse_cases = []
    for label, cv, record, variant, branches in (
            ("Table3", cv35, table_record, variants[table3_id], table_branches),
            ("non_Table3", pilot_cv, pilot_record, variants[pilot_id], pilot_branches)):
        for _ in range(64):
            target = tuple(rng.getrandbits(32) for _ in range(4))
            tail = table_tails[rng.randrange(len(table_tails))]
            new_cv, w03 = reconstruct_e19(cv[:4], branches[0], tail, *target)
            rebuilt = derive_bridge(new_cv, record, variant, common)
            words = tuple(rebuilt[0][2]) + tail
            _, e, expanded, _ = fixed.trace(new_cv, words, 20)
            assert tuple(expanded[:4]) == w03, f"{label}_E19_inverse_W0_W3"
            assert tuple(e[index] for index in range(16, 20)) == target, f"{label}_E19_inverse_targets"
        inverse_cases.append({"label": label, "cases": 64})

    assert set(binary_variants) == set(variants), "variant_binary_json_id_set"
    for variant_id, variant in variants.items():
        binary = binary_variants[variant_id]
        assert binary["a"] == variant["a"], "variant_binary_json_A1_A3"
        assert binary["e"] == variant["e"], "variant_binary_json_E5_E7"
        assert binary["w"] == variant["w"], "variant_binary_json_W9_W13"

    return {
        "schema": "variant-tail-oracle-self-test-v1",
        "inputs": {
            "mapping": mapping_path.name,
            "mapping_sha256": hashlib.sha256(mapping_path.read_bytes()).hexdigest(),
            "states": states_path.name,
            "states_sha256": hashlib.sha256(states_path.read_bytes()).hexdigest(),
            "conditional_pilot": pilot_path.name,
            "conditional_pilot_sha256": hashlib.sha256(pilot_path.read_bytes()).hexdigest(),
        },
        "variant_count": len(variants),
        "binary_json_equal": True,
        "table3": {
            "variant_id": table3_id,
            "cv35": "".join(f"{word:08x}" for word in cv35),
            "record": "".join(f"{word:08x}" for word in table_record),
            "bridge_stages": table_bridge,
            "late_stages": table_stages,
            "c32_output": "".join(f"{word:08x}" for word in table_left[3]),
        },
        "non_table3_conditional_pilot": {
            "trial": pilot["trial"],
            "variant_id": pilot_id,
            "cv": pilot["cv"],
            "record": pilot["record"],
            "bridge_stages": pilot_bridge,
            "prefix_replayed_through_round": 13,
        },
        "tail_domain": {
            "count": len(table_tails),
            "ordered_sha256": _tail_sha256(table_tails),
            "identical_for_table3_and_non_table3": True,
            "table3_build": table_build,
            "non_table3_build": pilot_build,
        },
        "E19_inverse": {
            "cases": inverse_cases,
            "proposal_domain_log2": [18, 27, 25, 31],
            "joint_domain_log2": 101,
            "uniform_target_log2": 128,
            "likelihood_ratio_power2": -27,
        },
        "mapping_selection": raw_mapping["selection"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mapping", type=Path, default=DEFAULT_MAPPING)
    parser.add_argument("--states", type=Path, default=DEFAULT_STATES)
    parser.add_argument("--pilot", type=Path, default=DEFAULT_PILOT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = self_test(args.mapping, args.states, args.pilot)
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
```

### Finite resource ledger

Embedded source SHA-256: `9d39d5947efdd89a2cf72b1eaeedd7688c4ccfc723453a18669017da74efeb3c`.

Source-file SHA-256 after restoring the single final LF: `fccdc4788b0be3ef489cb53c85974c411e1fc05e980c7dff001f37170cbf9fd1`.

```python
#!/usr/bin/env python3
"""Compute and check the finite SHA-256 r32 search ledgers."""

from __future__ import annotations

import argparse
import json
import math
from decimal import Decimal, getcontext
from pathlib import Path


def build():
    getcontext().prec = 80
    operation_caps = {
        "a_first_block_wrapper_and_index_miss": {
            "ceiling": 256,
            "items": {
                "two_uniform_256_bit_random_words": 2,
                "split_mask_and_store_sixteen_32_bit_block_words": 48,
                "C32_call_wrapper_input_output_and_dispatch": 48,
                "trial_cap_counters_and_control": 24,
                "direct_key_index_extraction_address_load_and_empty_check": 32,
                "spare": 102
            },
            "note": "C32 internals are charged once in H. A direct-address 2^32 span index with 16-byte entries is at most 2^36 bytes and fits the declared 2^40-byte peak; this avoids an unsupported lookup-time maximum."
        },
        "b_examined_record": {
            "ceiling": 2048,
            "items": {
                "record_variant_and_pointer_loads": 64,
                "reconstruct_and_mask_two_branch_A_E_state": 384,
                "derive_and_mask_two_branch_W0_through_W8": 640,
                "W0_W6_row_relation_and_equality_tests": 256,
                "canonical_scan_counters_and_control": 128,
                "spare": 576
            }
        },
        "c_accepted_bridge_setup": {
            "ceiling": 8192,
            "items": {
                "copy_fixed_and_variant_high_prefix_state": 256,
                "prepare_two_W0_through_W13_prefixes": 512,
                "tail_list_state_and_accepted_bridge_bookkeeping": 256,
                "at_most_once_final_message_build_compare_and_serialization": 4096,
                "spare": 3072
            },
            "note": "The final ordinary work occurs at most once and is covered by one bridge allowance because B>=1. Its six C32 calls are separate in H."
        },
        "d_each_tail_outside_two_C32_calls": {
            "ceiling": 512,
            "items": {
                "tail_loads_loop_counter_and_cap_check": 32,
                "write_tail_words_into_two_prepared_blocks": 32,
                "two_C32_call_wrappers_input_output_and_dispatch": 160,
                "compare_two_eight_word_outputs": 64,
                "candidate_bookkeeping_and_control": 32,
                "spare": 192
            },
            "note": "The two C32 internals are charged in H, not again here. The attack needs only exact output equality; diagnostic differential-stage tests are not online work."
        }
    }
    for name, value in operation_caps.items():
        if sum(value["items"].values()) != value["ceiling"]:
            raise AssertionError(name + "_itemization")

    common = {
        "B": 2**29,
        "L": 196608,
        "pi_premise": 2.0**-30,
        "P": 2**55,
        "peak_memory_bytes": 2**40,
        "advice_bytes": 2**20,
        "word_operation_divisor": 2224,
        "operation_ceilings": {"a": 256, "b": 2048, "c": 8192, "d_tail": 512}
    }
    cases = (
        ("repaired_65_variant", 2**-25, 2**55, 2**48, 16, 2.0**-8),
        ("repaired_65_variant_conservative", 2**-26, 2**56, 2**49, 16, 2.0**-8),
        ("fixed_table3_slice", 2**-30, 2**60, 2**51, 4, 2.0**-10),
    )
    ledgers = {}
    for name, q, n, r, record_cap, mu in cases:
        b, l, p = common["B"], common["L"], common["P"]
        a = common["operation_ceilings"]["a"]
        brec = common["operation_ceilings"]["b"]
        c = common["operation_ceilings"]["c"]
        dtail = common["operation_ceilings"]["d_tail"]
        h = n + 2 * b * l + 6
        w_terms = {"aN": a*n, "bR": brec*r, "cB": c*b, "dBL": dtail*b*l}
        w = sum(w_terms.values())
        divisor = common["word_operation_divisor"]
        t_num = (h + p) * divisor + w
        t_den = divisor
        log2_t = math.log2(t_num) - math.log2(t_den)
        expected_bridges = n * q
        delta = expected_bridges / b - 1
        shortfall_exponent = b * delta * delta / (2 * (1 + delta))
        max_mean = n * mu
        gap = r - max_mean
        variance_bound = n * record_cap * mu
        overflow = variance_bound / (gap * gap)
        overflow_power = int(math.log2(overflow))
        conservative_success = (Decimal(1) - (Decimal(-1) / 2).exp() -
                                (Decimal(2) ** overflow_power) - Decimal(2) ** -100)
        ledgers[name] = {
            "premises": {"q": q, "q_power2": int(math.log2(q)), "N": n,
                         "R": r, "record_cap": record_cap, "mean_load": mu,
                         "mean_load_power2": int(math.log2(mu))},
            "expected_bridges": int(expected_bridges),
            "B": b,
            "delta": delta,
            "shortfall_bound": f"exp(-{int(shortfall_exponent)})",
            "shortfall_exponent": shortfall_exponent,
            "record_variance_bound": int(variance_bound),
            "record_budget_gap": int(gap),
            "record_overflow_bound": overflow,
            "record_overflow_power2": overflow_power,
            "tail_miss_bound": "exp(-1/2)",
            "success_lower_bound_symbolic": f"1 - exp(-1/2) - exp(-{int(shortfall_exponent)}) - 2^{overflow_power}",
            "shortfall_bound_used_for_decimal": "exp(-2^27) < 2^-100",
            "conservative_success_lower_bound_decimal": str(conservative_success),
            "success_exceeds_0_39": conservative_success > Decimal("0.39"),
            "H": h,
            "W_terms": w_terms,
            "W": w,
            "P": p,
            "T_exact": {"numerator": t_num, "denominator": t_den},
            "T_decimal": t_num / t_den,
            "log2_T": log2_t,
            "log2_T_rounded_up_0_001": math.ceil(log2_t * 1000) / 1000,
        }
    return {
        "schema": "sha256-r32-finite-ledger-audit-v1",
        "cost_model": "collision-frontier-v5",
        "common": common,
        "operation_ceiling_audit": operation_caps,
        "ledgers": ledgers,
        "implementation_notes": [
            "The audited first-block wrapper ceiling is a=256.",
            "The q>=2^-25, N=2^55, R=2^48 repaired 65-variant case is the selected ledger; q>=2^-26 and the fixed Table-3 case are sensitivity/fallback ledgers.",
            "The finite algorithm uses two C32 calls per tail, one for each second block. Six additional C32 calls cover the single final complete-message replay."
        ]
    }


def check(path: Path):
    observed = json.loads(path.read_text())
    expected = build()
    for case in expected["ledgers"]:
        for field in ("H", "W", "P", "T_exact", "log2_T_rounded_up_0_001"):
            if observed["ledgers"][case][field] != expected["ledgers"][case][field]:
                raise AssertionError(f"{case}_{field}")
    if observed["operation_ceiling_audit"] != expected["operation_ceiling_audit"]:
        raise AssertionError("operation_ceiling_itemization")
    return observed


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--output", type=Path)
    group.add_argument("--check", type=Path)
    args = parser.parse_args()
    if args.output:
        value = build()
        args.output.write_text(json.dumps(value, indent=2) + "\n")
        print(json.dumps({case: {"log2_T": row["log2_T"],
                                 "success": row["conservative_success_lower_bound_decimal"]}
                          for case, row in value["ledgers"].items()}))
    else:
        check(args.check)
        print(json.dumps({"status": "pass", "artifact": str(args.check)}))


if __name__ == "__main__":
    main()
```

## Appendix C: compact completed evidence

### Conditional repaired-sampler audit

Embedded JSON SHA-256: `79492656bc9b78a3f658fea558c5027490086ca06b9ca691db1c2560672cf4f7`.

```json
{
  "checker_control": {
    "control": "mutate_first_accepted_W7_bit0",
    "disposable_copy_exit_status": 23,
    "expected_failure": "accepted_record_not_canonical_first_valid",
    "observed_failure": "accepted_record_not_canonical_first_valid",
    "passed": true
  },
  "experiment": "independent repaired-subtable sampler audit",
  "packed_table_audit": {
    "canonical_order_checked_for_every_record": true,
    "distinct_keys": 4088007,
    "maximum_multiplicity": 16,
    "multiplicity_histogram": {
      "1": 1939953,
      "10": 144,
      "12": 13824,
      "16": 2816,
      "2": 1511289,
      "3": 132387,
      "4": 344937,
      "5": 956,
      "6": 32306,
      "8": 109395
    },
    "nonempty_variants": 14,
    "per_variant_counts": {
      "26274": 552960,
      "287670": 487168,
      "313146": 294912,
      "320438": 227584,
      "385574": 524288,
      "452134": 145408,
      "508458": 786432,
      "59306": 1545728,
      "640554": 1245184,
      "706362": 540672,
      "804666": 294912,
      "870330": 262144,
      "90810": 524288,
      "919338": 593920
    },
    "records": 8025600,
    "variant_state_present_for_every_record": true
  },
  "replay_summary": {
    "accepted_prefixes_both_branches_checked": 22,
    "canonical_first_valid_records_checked": 11,
    "failures": 0
  },
  "sampler_source_audit": {
    "canonical_record_order": "key,variant_id,W7,W8,E3,E4,A0",
    "first_32_constants_match_pinned_reference": true,
    "relation_edges_derived_from_Figure6": {
      "W4": [
        [
          1,
          12,
          1
        ],
        [
          8,
          25,
          1
        ],
        [
          18,
          14,
          0
        ]
      ],
      "W5": [
        [
          0,
          28,
          0
        ],
        [
          1,
          18,
          0
        ],
        [
          30,
          9,
          0
        ]
      ],
      "W6": [
        [
          1,
          12,
          0
        ],
        [
          8,
          25,
          0
        ],
        [
          18,
          14,
          1
        ]
      ]
    },
    "relation_predicates_match": true,
    "row_masks_derived_from_Figure6": {
      "W4": [
        "20000000",
        "20000000",
        "00000000"
      ],
      "W5": [
        "04400800",
        "00000800",
        "04400000"
      ],
      "W6": [
        "20000000",
        "20000000",
        "00000000"
      ]
    },
    "row_masks_in_sampler": {
      "W4": [
        "20000000",
        "20000000",
        "00000000"
      ],
      "W5": [
        "04400800",
        "00000800",
        "04400000"
      ],
      "W6": [
        "20000000",
        "20000000",
        "00000000"
      ]
    },
    "row_masks_match": true,
    "serialization": "xoshiro256** uint64 high uint32 then low uint32",
    "standard_IV_matches_pinned_reference": true
  },
  "selection": {
    "binary_format": "BWR1, big-endian uint32 count, then count records of (cartesian_id,E5,E5p,E6,E6p,E7,E7p)",
    "binary_path": "backward-sample-variants.bin",
    "binary_sha256": "1d50ca93bd78c137dd893b03533e623895c49e37c934c81881a098f78d68feb0",
    "cartesian_ids": [
      16934,
      17170,
      17190,
      26274,
      26546,
      50106,
      50994,
      58274,
      59014,
      59306,
      90810,
      123410,
      133054,
      148146,
      180894,
      180922,
      181134,
      190214,
      213814,
      214802,
      223118,
      255654,
      263070,
      279090,
      287670,
      296714,
      296886,
      313146,
      320158,
      320178,
      320438,
      321302,
      377738,
      385574,
      393994,
      427926,
      444314,
      452134,
      508458,
      516666,
      542262,
      550530,
      557714,
      574134,
      640554,
      648114,
      656898,
      680478,
      706362,
      713634,
      770710,
      804666,
      819866,
      836226,
      837274,
      845714,
      870330,
      901894,
      919338,
      967426,
      976526,
      1008266,
      1032838,
      1041178,
      1042230
    ],
    "non_table3_size": 64,
    "sample_size": 65,
    "seed": 2026100505,
    "selection_rule": "64 uniform variants without replacement from the 10,239 non-Table-3 survivors, plus the Table 3 control",
    "table3_controls": 1
  },
  "stream_integrity": {
    "accepted_rows": 11,
    "conditional_stream_exactly_recomputed": {
      "accepted": 11,
      "examined": 514833,
      "group_records": 514845,
      "key_hit_trials": 262144,
      "stages": [
        514833,
        257654,
        32346,
        1986,
        239,
        96,
        11
      ]
    },
    "control_rows": 4,
    "count_checkpoints": 1,
    "final_counts": {
      "accepted": 11,
      "examined": 514833,
      "group_records": 514845,
      "key_hit_trials": 262144,
      "kind": "counts",
      "stages": [
        514833,
        257654,
        32346,
        1986,
        239,
        96,
        11
      ],
      "trials": 262144
    },
    "mode": "conditional",
    "monotone_and_complete": true,
    "seed": 2026100519,
    "trials": 262144
  },
  "variant_state_mapping": {
    "binary_equals_json": true,
    "common_state_loaded_from_mapping": true,
    "variants": 65
  }
}
```

### Completed repaired standard-IV stream audit

Embedded JSON SHA-256: `1c2017a98df41d3c7cfcea2946bc5f317d006aab57380c468120ba24f4849205`.

```json
{
  "checker_control": {
    "control": "mutate_first_accepted_W7_bit0",
    "disposable_copy_exit_status": 23,
    "expected_failure": "accepted_record_not_canonical_first_valid",
    "observed_failure": "accepted_record_not_canonical_first_valid",
    "passed": true
  },
  "experiment": "independent repaired-subtable sampler audit",
  "packed_table_audit": {
    "canonical_order_checked_for_every_record": true,
    "distinct_keys": 4088007,
    "maximum_multiplicity": 16,
    "multiplicity_histogram": {
      "1": 1939953,
      "10": 144,
      "12": 13824,
      "16": 2816,
      "2": 1511289,
      "3": 132387,
      "4": 344937,
      "5": 956,
      "6": 32306,
      "8": 109395
    },
    "nonempty_variants": 14,
    "per_variant_counts": {
      "26274": 552960,
      "287670": 487168,
      "313146": 294912,
      "320438": 227584,
      "385574": 524288,
      "452134": 145408,
      "508458": 786432,
      "59306": 1545728,
      "640554": 1245184,
      "706362": 540672,
      "804666": 294912,
      "870330": 262144,
      "90810": 524288,
      "919338": 593920
    },
    "records": 8025600,
    "variant_state_present_for_every_record": true
  },
  "replay_summary": {
    "C32_controls_and_accepts_checked": 355,
    "accepted_prefixes_both_branches_checked": 702,
    "canonical_first_valid_records_checked": 351,
    "failures": 0
  },
  "sampler_source_audit": {
    "canonical_record_order": "key,variant_id,W7,W8,E3,E4,A0",
    "first_32_constants_match_pinned_reference": true,
    "relation_edges_derived_from_Figure6": {
      "W4": [
        [
          1,
          12,
          1
        ],
        [
          8,
          25,
          1
        ],
        [
          18,
          14,
          0
        ]
      ],
      "W5": [
        [
          0,
          28,
          0
        ],
        [
          1,
          18,
          0
        ],
        [
          30,
          9,
          0
        ]
      ],
      "W6": [
        [
          1,
          12,
          0
        ],
        [
          8,
          25,
          0
        ],
        [
          18,
          14,
          1
        ]
      ]
    },
    "relation_predicates_match": true,
    "row_masks_derived_from_Figure6": {
      "W4": [
        "20000000",
        "20000000",
        "00000000"
      ],
      "W5": [
        "04400800",
        "00000800",
        "04400000"
      ],
      "W6": [
        "20000000",
        "20000000",
        "00000000"
      ]
    },
    "row_masks_in_sampler": {
      "W4": [
        "20000000",
        "20000000",
        "00000000"
      ],
      "W5": [
        "04400800",
        "00000800",
        "04400000"
      ],
      "W6": [
        "20000000",
        "20000000",
        "00000000"
      ]
    },
    "row_masks_match": true,
    "serialization": "xoshiro256** uint64 high uint32 then low uint32",
    "standard_IV_matches_pinned_reference": true
  },
  "source": {
    "packed_table": "repaired-subtable-65.bin",
    "packed_table_sha256": "bbc1c4b94fa822e1176c2046aa36ea2f077b0590f37420995cfbf769f473eeff",
    "pinned_reference_sha256": "514fa8ab8a461e4a41080efa27b4ba2a3b499eeedf0a2d2346e6562835d040f5",
    "repository_commit": "8a0f02675cdcd58ebfc16119af02a094c3e1dd16",
    "sampler_source": "repaired_bridge_sample.cpp",
    "sampler_source_sha256": "915cf93ba9080c6366e0743b12228b65c8378516180a134eacad9bfd30abe01b",
    "stream": "repaired-c32-seed-2026100519-N33.jsonl",
    "stream_sha256": "ccd81c657ad941374ce2c80584824322287bb9b0432d7fe3f4588e3fd6ba0198",
    "validator_sha256": "b59c43acb88603e0788bf7df65aba640e81ca4d2e898f8a64b6ec4e53994eec2",
    "variant_mapping": "repaired-variant-mapping.json",
    "variant_mapping_sha256": "47841a38e8ee86f0d6243b1233ea4ff78b2aa5f5057a93cdcbd7605e6bdfcfbf",
    "variant_states": "repaired-variant-states.bin",
    "variant_states_sha256": "cc96a713059ceb66f2813116a482f7bc77024d89ebf8411f89ee58ba0ee7d3ab"
  },
  "statistics": {
    "actual_standard_IV_C32": {
      "accepted": 351,
      "nominal_iid_Wilson_95_interval": [
        3.6804775766592096e-08,
        4.536598478406502e-08
      ],
      "nominal_iid_Wilson_99_9_interval": [
        3.4287633499545444e-08,
        4.869641691872201e-08
      ],
      "q_hat": 4.086177796125412e-08,
      "q_hat_log2": -24.54467277969544,
      "trials": 8589934592
    },
    "diagnostic_scope": "Wilson intervals and the bounded-load standard-error bound are nominal iid diagnostics. The seeded xoshiro256** stream is deterministic; these are not coverage guarantees, and the PRNG does not prove mathematical independence.",
    "filter_stages": {
      "conditional_pass_rates": [
        0.49990725129103336,
        0.1251056864384833,
        0.06268668319096327,
        0.12548888676905465,
        0.36830102622576966,
        0.12074303405572756
      ],
      "cumulative_counts": [
        16043350,
        8020187,
        1003371,
        62898,
        7893,
        2907,
        351
      ]
    },
    "table_load": {
      "bounded_load_standard_error_upper_bound_if_iid": 1.86516674450009e-06,
      "exact_table_key_fraction": 0.0009518133010715246,
      "group_records": 16043766,
      "hit_rate": 0.0009512896649539471,
      "key_hit_trials": 8171516,
      "maximum_records_per_key": 16,
      "mean_group_records_per_trial": 0.0018677401822060347,
      "mean_records_examined_per_key_hit": 1.9633260217565505,
      "mean_records_examined_per_trial": 0.0018676917534321547,
      "mean_records_examined_per_trial_log2": -9.064527914459388,
      "records_examined": 16043350
    }
  },
  "stream_integrity": {
    "accepted_rows": 351,
    "conditional_stream_exactly_recomputed": null,
    "control_rows": 4,
    "count_checkpoints": 512,
    "final_counts": {
      "accepted": 351,
      "examined": 16043350,
      "group_records": 16043766,
      "key_hit_trials": 8171516,
      "kind": "counts",
      "stages": [
        16043350,
        8020187,
        1003371,
        62898,
        7893,
        2907,
        351
      ],
      "trials": 8589934592
    },
    "mode": "c32",
    "monotone_and_complete": true,
    "seed": 2026100519,
    "trials": 8589934592
  },
  "variant_state_mapping": {
    "binary_equals_json": true,
    "common_state_loaded_from_mapping": true,
    "variants": 65
  }
}
```

### Fixed-oracle Table 3 self-test

Embedded JSON SHA-256: `496fca54620f8c41dc9eb4b4ee0ac969f3906e0885d3bfd350818ecc57bc3551`.

```json
{
  "bijection_random_cases": 128,
  "controls": {
    "control_perturbed_E20_bit29_zero": false,
    "control_wrong_schedule_W18_uses_W10": false
  },
  "oracle": "tail_oracle.py",
  "table3": {
    "c32_output": "22b419939458056ce7f8a711998eb4c0544191e8b7a599b191dcfc3a0d403a72",
    "candidate_count": 196608,
    "candidate_stages": {
      "A14_relations": 12,
      "A14_row": 128,
      "A15_relations": 196608,
      "A15_row": 393216,
      "E14_domain": 256,
      "E15_domain": 393216,
      "W14_equal": 256,
      "W15_equal": 393216,
      "candidates": 196608
    },
    "cv35": "c4369610c91f70a787e430e6a5e58128d29cb97b9ab268d18788f401629f6cb2",
    "record": "c4369610db9ec6656ec17218a70d43082932d839ac311f10",
    "stage_results": {
      "A16_row": true,
      "C32_collision": true,
      "E16_relations": true,
      "E16_row": true,
      "E17_row": true,
      "E18_relations": true,
      "E18_row": true,
      "E19_row": true,
      "E20_row": true,
      "W20_relations": true,
      "W20_row": true,
      "W22_relations": true,
      "W22_row": true
    },
    "tail": "d2701ecc140976d1"
  }
}
```

### Fixed-oracle disposable controls

Embedded JSON SHA-256: `d3816c05406c7dab1004c31cbf4e0e94bed03c11f864d2e7aa8a6326fd7e09e0`.

```json
{
  "controls": [
    {
      "expected": "pass",
      "name": "baseline",
      "observed": "pass",
      "returncode": 0
    },
    {
      "expected": "Table3_E20_row",
      "mutation": "E20 position 2: 1 -> 0",
      "name": "perturbed_Table3_E20_bit29",
      "observed": "named_failure",
      "returncode": 1
    },
    {
      "expected": "bijection_forward_backward_E16_E18",
      "mutation": "W18 inversion subtracts W10 instead of W11",
      "name": "wrong_schedule_index_W18_uses_W10",
      "observed": "named_failure",
      "returncode": 1
    }
  ],
  "schema": "tail-mutation-controls-v1"
}
```

### Fixed standard-IV stage sweep

Embedded JSON SHA-256: `cf65a2cf2b6a3aee5c35e21f768cec2552afe146221e9ae57d31d9a64d13d160`.

```json
{
  "aggregate_stages": [
    {
      "denominator": 5308416,
      "fail": 0,
      "marginal_pass": 5308416,
      "name": "A16_row",
      "pass": 5308416
    },
    {
      "denominator": 5308416,
      "fail": 5273989,
      "marginal_pass": 34427,
      "name": "E16_row",
      "pass": 34427
    },
    {
      "denominator": 34427,
      "fail": 34209,
      "marginal_pass": 41627,
      "name": "E16_relations",
      "pass": 218
    },
    {
      "denominator": 218,
      "fail": 212,
      "marginal_pass": 6,
      "name": "E17_row",
      "pass": 6
    },
    {
      "denominator": 6,
      "fail": 6,
      "marginal_pass": 0,
      "name": "E18_row",
      "pass": 0
    },
    {
      "denominator": 0,
      "fail": 0,
      "marginal_pass": 1326626,
      "name": "E18_relations",
      "pass": 0
    },
    {
      "denominator": 0,
      "fail": 0,
      "marginal_pass": 0,
      "name": "E19_row",
      "pass": 0
    },
    {
      "denominator": 0,
      "fail": 0,
      "marginal_pass": 0,
      "name": "E20_row",
      "pass": 0
    },
    {
      "denominator": 0,
      "fail": 0,
      "marginal_pass": 65536,
      "name": "W20_row",
      "pass": 0
    },
    {
      "denominator": 0,
      "fail": 0,
      "marginal_pass": 98304,
      "name": "W20_relations",
      "pass": 0
    },
    {
      "denominator": 0,
      "fail": 0,
      "marginal_pass": 0,
      "name": "W22_row",
      "pass": 0
    },
    {
      "denominator": 0,
      "fail": 0,
      "marginal_pass": 663552,
      "name": "W22_relations",
      "pass": 0
    },
    {
      "denominator": 0,
      "fail": 0,
      "marginal_pass": 0,
      "name": "C32_collision",
      "pass": 0
    }
  ],
  "bridge_count": 27,
  "candidate_count_per_bridge": 196608,
  "candidate_fnv1a64": "21821011d57a5203",
  "ensemble": "standard_iv_c32_bridges",
  "schema": "tail-stage-sweep-v1"
}
```

### Precommitted 100-million importance specification

Embedded JSON SHA-256: `119ed84a7229ab1bbe607a2c4773bd0502d8ef64801c0f5ea18e273367c9b96f`.

```json
{
  "A_half_cohort": "all 27 accepted standard-IV first-block bridges from the completed 2^33 seed-2026100503 stream",
  "E_half_law": "abstract reconstruction from the E16/E17/E18/E19 proposal; no standard-IV first-block preimage is known",
  "additional_recording": "exact W4-W6 bridge stages, bridge/late marginal and joint counts, per-base counts, every K, and whether each selected success passes the full bridge",
  "binary_sha256": "d4bed134c8810257efaecedc598c458ceff153d864e34270226281f4d3c8f03a",
  "chronology": "Fixed after the 1,000,000-proposal abstract pilot and its five successes, after independent replay, and before reading any seed-2026100518 result.",
  "command": "tools/localrun.sh -t 600 -n 1 ./tail_measure importance inputs/c32-sample-33-final.jsonl 100000000 2026100518 standard_iv_A_halves_abstract_E_reconstruction importance-standard-iv-100m.json",
  "created_utc": "2026-10-05T12:52:01Z",
  "figure6_conditions_sha256": "664bfffc35c216cfe3e39f7d806ae0341593dc51ac4431736813748cd5a0bad6",
  "input": "inputs/c32-sample-33-final.jsonl",
  "input_sha256": "7839ada8af04a42759ff965b410a3989a284ac0520ac7ef438ece84b9b2afe74",
  "likelihood_ratio_power2": -27,
  "multiplicity": "K counts the same selected event over all 196,608 tails for every selected success",
  "output": "importance-standard-iv-100m.json",
  "proposal_domain_log2": [
    18,
    27,
    25,
    31
  ],
  "reporting": "Retain and report the raw result even if its success rate is below the pilot. No calibrated confidence interval will be claimed.",
  "resource_estimate": {
    "cores": 1,
    "cpu_and_wall_bound": "600 seconds; a 100,000-proposal no-hit probe took 0.13 seconds, so proposal-only extrapolation is about 130 seconds, with the remainder reserved for exhaustive K scans",
    "output_disk": "under 5 MiB expected",
    "peak_memory": "under 0.1 GiB; one 196,608-tail vector plus 27 bridge states and counters"
  },
  "schema": "tail-importance-precommit-v1",
  "seed": 2026100518,
  "selected_event": "all named A16-through-W22 path conditions and exact C32 feed-forward equality",
  "source_sha256": "151c50786972c551d03560e5c6f25f6efecbcc0fbac85e1a4e36edfae503ce97",
  "tail_count": 196608,
  "timeout_seconds": 600,
  "trials": 100000000
}
```

### 100-million importance result

Embedded JSON SHA-256: `285faa719d4cac3f66afab776cfccca5d9de3486dbe49ef307fbac3f7fa55d2e`.

```json
{
  "bridge_count": 27,
  "bridge_stage_counts": [
    {
      "denominator": 100000000,
      "fail": 0,
      "marginal_pass": 100000000,
      "name": "W4_row",
      "pass": 100000000
    },
    {
      "denominator": 100000000,
      "fail": 0,
      "marginal_pass": 100000000,
      "name": "W4_relations",
      "pass": 100000000
    },
    {
      "denominator": 100000000,
      "fail": 0,
      "marginal_pass": 100000000,
      "name": "W5_row",
      "pass": 100000000
    },
    {
      "denominator": 100000000,
      "fail": 0,
      "marginal_pass": 100000000,
      "name": "W5_relations",
      "pass": 100000000
    },
    {
      "denominator": 100000000,
      "fail": 0,
      "marginal_pass": 100000000,
      "name": "W6_row",
      "pass": 100000000
    },
    {
      "denominator": 100000000,
      "fail": 0,
      "marginal_pass": 100000000,
      "name": "W6_relations",
      "pass": 100000000
    }
  ],
  "calibrated_confidence_interval": null,
  "chosen_tail_successes": 209,
  "ensemble": "standard_iv_A_halves_abstract_E_reconstruction",
  "monte_carlo_standard_error": 2.1176978407745222e-10,
  "per_base": [
    {
      "K_values": [
        1,
        1,
        1,
        1,
        1,
        1
      ],
      "base_bridge_index": 0,
      "base_trial": 297904080,
      "chosen_tail_successes": 6,
      "proposal_count": 3703255
    },
    {
      "K_values": [
        1,
        1,
        1
      ],
      "base_bridge_index": 1,
      "base_trial": 541886044,
      "chosen_tail_successes": 3,
      "proposal_count": 3704417
    },
    {
      "K_values": [
        1,
        1,
        1,
        1,
        1
      ],
      "base_bridge_index": 2,
      "base_trial": 821627414,
      "chosen_tail_successes": 5,
      "proposal_count": 3703652
    },
    {
      "K_values": [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1
      ],
      "base_bridge_index": 3,
      "base_trial": 835318145,
      "chosen_tail_successes": 10,
      "proposal_count": 3703527
    },
    {
      "K_values": [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1
      ],
      "base_bridge_index": 4,
      "base_trial": 1735749845,
      "chosen_tail_successes": 9,
      "proposal_count": 3702182
    },
    {
      "K_values": [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1
      ],
      "base_bridge_index": 5,
      "base_trial": 2080444017,
      "chosen_tail_successes": 12,
      "proposal_count": 3701663
    },
    {
      "K_values": [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1
      ],
      "base_bridge_index": 6,
      "base_trial": 2113439127,
      "chosen_tail_successes": 8,
      "proposal_count": 3701989
    },
    {
      "K_values": [
        1,
        1,
        1,
        1,
        1,
        1,
        1
      ],
      "base_bridge_index": 7,
      "base_trial": 2423612657,
      "chosen_tail_successes": 7,
      "proposal_count": 3708158
    },
    {
      "K_values": [
        1,
        1,
        1,
        1,
        1,
        1,
        1
      ],
      "base_bridge_index": 8,
      "base_trial": 2603006510,
      "chosen_tail_successes": 7,
      "proposal_count": 3704086
    },
    {
      "K_values": [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1
      ],
      "base_bridge_index": 9,
      "base_trial": 2932328028,
      "chosen_tail_successes": 11,
      "proposal_count": 3704589
    },
    {
      "K_values": [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1
      ],
      "base_bridge_index": 10,
      "base_trial": 2933228829,
      "chosen_tail_successes": 9,
      "proposal_count": 3708082
    },
    {
      "K_values": [
        1,
        1,
        1,
        1,
        1,
        1
      ],
      "base_bridge_index": 11,
      "base_trial": 3594161641,
      "chosen_tail_successes": 6,
      "proposal_count": 3704512
    },
    {
      "K_values": [
        1,
        1,
        1
      ],
      "base_bridge_index": 12,
      "base_trial": 4203051109,
      "chosen_tail_successes": 3,
      "proposal_count": 3703185
    },
    {
      "K_values": [
        1,
        1,
        1,
        1,
        1,
        1
      ],
      "base_bridge_index": 13,
      "base_trial": 4367132904,
      "chosen_tail_successes": 6,
      "proposal_count": 3700706
    },
    {
      "K_values": [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1
      ],
      "base_bridge_index": 14,
      "base_trial": 4603829108,
      "chosen_tail_successes": 8,
      "proposal_count": 3703769
    },
    {
      "K_values": [
        1,
        1,
        1
      ],
      "base_bridge_index": 15,
      "base_trial": 4933792032,
      "chosen_tail_successes": 3,
      "proposal_count": 3705039
    },
    {
      "K_values": [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1
      ],
      "base_bridge_index": 16,
      "base_trial": 4994674326,
      "chosen_tail_successes": 12,
      "proposal_count": 3703861
    },
    {
      "K_values": [
        1,
        1,
        1,
        1,
        1,
        1,
        1
      ],
      "base_bridge_index": 17,
      "base_trial": 5245356954,
      "chosen_tail_successes": 7,
      "proposal_count": 3702034
    },
    {
      "K_values": [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1
      ],
      "base_bridge_index": 18,
      "base_trial": 5402628384,
      "chosen_tail_successes": 8,
      "proposal_count": 3703939
    },
    {
      "K_values": [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1
      ],
      "base_bridge_index": 19,
      "base_trial": 6240147173,
      "chosen_tail_successes": 15,
      "proposal_count": 3699952
    },
    {
      "K_values": [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1
      ],
      "base_bridge_index": 20,
      "base_trial": 6445990344,
      "chosen_tail_successes": 12,
      "proposal_count": 3703031
    },
    {
      "K_values": [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1
      ],
      "base_bridge_index": 21,
      "base_trial": 6629437200,
      "chosen_tail_successes": 8,
      "proposal_count": 3702152
    },
    {
      "K_values": [
        1,
        1,
        1,
        1,
        1
      ],
      "base_bridge_index": 22,
      "base_trial": 6673359959,
      "chosen_tail_successes": 5,
      "proposal_count": 3705257
    },
    {
      "K_values": [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1
      ],
      "base_bridge_index": 23,
      "base_trial": 6775561396,
      "chosen_tail_successes": 8,
      "proposal_count": 3702238
    },
    {
      "K_values": [
        1,
        1,
        1,
        1,
        1,
        1
      ],
      "base_bridge_index": 24,
      "base_trial": 8142616327,
      "chosen_tail_successes": 6,
      "proposal_count": 3704135
    },
    {
      "K_values": [
        1,
        1,
        1,
        1,
        1,
        1
      ],
      "base_bridge_index": 25,
      "base_trial": 8205734139,
      "chosen_tail_successes": 6,
      "proposal_count": 3704887
    },
    {
      "K_values": [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1
      ],
      "base_bridge_index": 26,
      "base_trial": 8292494325,
      "chosen_tail_successes": 9,
      "proposal_count": 3705703
    }
  ],
  "pi_uniform_estimate": 3.0615234375e-09,
  "proposal": {
    "dimensions": [
      "E16_with_relations",
      "E17",
      "E18_with_relations",
      "E19"
    ],
    "domain_log2": [
      18,
      27,
      25,
      31
    ],
    "joint_domain_log2": 101,
    "likelihood_ratio": 7.450580596923828e-09,
    "likelihood_ratio_power2": -27
  },
  "reconstruction_pass": 100000000,
  "schema": "tail-importance-v1",
  "seed": 2026100518,
  "stage_counts": [
    {
      "denominator": 100000000,
      "fail": 0,
      "marginal_pass": 100000000,
      "name": "A16_row",
      "pass": 100000000
    },
    {
      "denominator": 100000000,
      "fail": 0,
      "marginal_pass": 100000000,
      "name": "E16_row",
      "pass": 100000000
    },
    {
      "denominator": 100000000,
      "fail": 0,
      "marginal_pass": 100000000,
      "name": "E16_relations",
      "pass": 100000000
    },
    {
      "denominator": 100000000,
      "fail": 0,
      "marginal_pass": 100000000,
      "name": "E17_row",
      "pass": 100000000
    },
    {
      "denominator": 100000000,
      "fail": 0,
      "marginal_pass": 100000000,
      "name": "E18_row",
      "pass": 100000000
    },
    {
      "denominator": 100000000,
      "fail": 0,
      "marginal_pass": 100000000,
      "name": "E18_relations",
      "pass": 100000000
    },
    {
      "denominator": 100000000,
      "fail": 49998659,
      "marginal_pass": 50001341,
      "name": "E19_row",
      "pass": 50001341
    },
    {
      "denominator": 50001341,
      "fail": 24996158,
      "marginal_pass": 25005183,
      "name": "E20_row",
      "pass": 25005183
    },
    {
      "denominator": 25005183,
      "fail": 24614445,
      "marginal_pass": 1563222,
      "name": "W20_row",
      "pass": 390738
    },
    {
      "denominator": 390738,
      "fail": 384712,
      "marginal_pass": 1564458,
      "name": "W20_relations",
      "pass": 6026
    },
    {
      "denominator": 6026,
      "fail": 2972,
      "marginal_pass": 52595,
      "name": "W22_row",
      "pass": 3054
    },
    {
      "denominator": 3054,
      "fail": 2669,
      "marginal_pass": 12502113,
      "name": "W22_relations",
      "pass": 385
    },
    {
      "denominator": 385,
      "fail": 176,
      "marginal_pass": 864,
      "name": "C32_collision",
      "pass": 209
    }
  ],
  "sum_inverse_K": 209,
  "tail_count": 196608,
  "trials": 100000000
}
```

### Pinned replay of 209 importance outcomes

Embedded JSON SHA-256: `fdd7a6b0692d243cfdd56cba01b5b292e654ab0b920c0cfde096bf39663d6bbb`.

```json
{
  "K_distribution": {
    "1": 209
  },
  "all_bridge_stages_pass": true,
  "all_late_stages_pass": true,
  "all_pinned_C32_equal": true,
  "measurement_sha256": "c56094ac631d5549d8f39f0a11da1454e75224b0e4f4bbb6c9dbefc38fb45d79",
  "pinned_reference_sha256": "514fa8ab8a461e4a41080efa27b4ba2a3b499eeedf0a2d2346e6562835d040f5",
  "pinned_repository_commit": "8a0f02675cdcd58ebfc16119af02a094c3e1dd16",
  "recomputed_pi_uniform_estimate": 3.0615234375e-09,
  "recomputed_sum_inverse_K": 209.0,
  "schema": "large-measurement-validation-v1",
  "successes_replayed": 209
}
```

### Variant-aware scalar controls

Embedded JSON SHA-256: `ebfb4eb2d9e5d4a8954057eab1230d538ba6b21c939454c32bc19e9efa47a037`.

```json
{
  "E19_inverse": {
    "cases": [
      {
        "cases": 64,
        "label": "Table3"
      },
      {
        "cases": 64,
        "label": "non_Table3"
      }
    ],
    "joint_domain_log2": 101,
    "likelihood_ratio_power2": -27,
    "proposal_domain_log2": [
      18,
      27,
      25,
      31
    ],
    "uniform_target_log2": 128
  },
  "binary_json_equal": true,
  "inputs": {
    "conditional_pilot": "repaired-sampler-conditional-pilot.jsonl",
    "conditional_pilot_sha256": "e0b35a01758c59e23569a2f4176cfc2b02bd19020dd2cc3c11965af5b2d6cd41",
    "mapping": "repaired-variant-mapping.json",
    "mapping_sha256": "47841a38e8ee86f0d6243b1233ea4ff78b2aa5f5057a93cdcbd7605e6bdfcfbf",
    "states": "repaired-variant-states.bin",
    "states_sha256": "cc96a713059ceb66f2813116a482f7bc77024d89ebf8411f89ee58ba0ee7d3ab"
  },
  "mapping_selection": {
    "binary_format": "BWR1, big-endian uint32 count, then count records of (cartesian_id,E5,E5p,E6,E6p,E7,E7p)",
    "binary_path": "backward-sample-variants.bin",
    "binary_sha256": "1d50ca93bd78c137dd893b03533e623895c49e37c934c81881a098f78d68feb0",
    "cartesian_ids": [
      16934,
      17170,
      17190,
      26274,
      26546,
      50106,
      50994,
      58274,
      59014,
      59306,
      90810,
      123410,
      133054,
      148146,
      180894,
      180922,
      181134,
      190214,
      213814,
      214802,
      223118,
      255654,
      263070,
      279090,
      287670,
      296714,
      296886,
      313146,
      320158,
      320178,
      320438,
      321302,
      377738,
      385574,
      393994,
      427926,
      444314,
      452134,
      508458,
      516666,
      542262,
      550530,
      557714,
      574134,
      640554,
      648114,
      656898,
      680478,
      706362,
      713634,
      770710,
      804666,
      819866,
      836226,
      837274,
      845714,
      870330,
      901894,
      919338,
      967426,
      976526,
      1008266,
      1032838,
      1041178,
      1042230
    ],
    "non_table3_size": 64,
    "sample_size": 65,
    "seed": 2026100505,
    "selection_rule": "64 uniform variants without replacement from the 10,239 non-Table-3 survivors, plus the Table 3 control",
    "table3_controls": 1
  },
  "non_table3_conditional_pilot": {
    "bridge_stages": {
      "W4_relations": true,
      "W4_row": true,
      "W5_relations": true,
      "W5_row": true,
      "W6_relations": true,
      "W6_row": true
    },
    "cv": "ebb987029abec68b3cb649752184e8f214434bc78024ad6bbbfb1440b5659fc7",
    "prefix_replayed_through_round": 13,
    "record": "ebb98702935869654ca301c26fed21282950cb53add2116c",
    "trial": 1458,
    "variant_id": 640554
  },
  "schema": "variant-tail-oracle-self-test-v1",
  "table3": {
    "bridge_stages": {
      "W4_relations": true,
      "W4_row": true,
      "W5_relations": true,
      "W5_row": true,
      "W6_relations": true,
      "W6_row": true
    },
    "c32_output": "22b419939458056ce7f8a711998eb4c0544191e8b7a599b191dcfc3a0d403a72",
    "cv35": "c4369610c91f70a787e430e6a5e58128d29cb97b9ab268d18788f401629f6cb2",
    "late_stages": {
      "A16_row": true,
      "C32_collision": true,
      "E16_relations": true,
      "E16_row": true,
      "E17_row": true,
      "E18_relations": true,
      "E18_row": true,
      "E19_row": true,
      "E20_row": true,
      "W20_relations": true,
      "W20_row": true,
      "W22_relations": true,
      "W22_row": true
    },
    "record": "c4369610db9ec6656ec17218a70d43082932d839ac311f10",
    "variant_id": 919338
  },
  "tail_domain": {
    "count": 196608,
    "identical_for_table3_and_non_table3": true,
    "non_table3_build": {
      "A14_relations": 12,
      "A14_row": 128,
      "A15_relations": 196608,
      "A15_row": 393216,
      "E14_domain": 256,
      "E15_domain": 393216,
      "W14_equal": 256,
      "W15_equal": 393216,
      "candidates": 196608
    },
    "ordered_sha256": "33217b7b360c05deb16661fb5dcc25655704824f5070c976288874866195de37",
    "table3_build": {
      "A14_relations": 12,
      "A14_row": 128,
      "A15_relations": 196608,
      "A15_row": 393216,
      "E14_domain": 256,
      "E15_domain": 393216,
      "W14_equal": 256,
      "W15_equal": 393216,
      "candidates": 196608
    }
  },
  "variant_count": 65
}
```

### Variant-aware disposable controls

Embedded JSON SHA-256: `8e0946c55935900f9d4af611a53576abcfefb010c9e6bdabbeddc5d5d3120cd9`.

```json
{
  "controls": [
    {
      "expected": "pass",
      "name": "baseline",
      "observed": "pass",
      "returncode": 0
    },
    {
      "expected": "Table3_variant_prefix_replay_unprimed",
      "name": "perturbed_Table3_variant_W9_bit0",
      "observed": "named_failure",
      "returncode": 1
    },
    {
      "expected": "non_Table3_conditional_pilot_prefix_A1_A13",
      "name": "perturbed_non_Table3_variant_W9_bit0",
      "observed": "named_failure",
      "returncode": 1
    }
  ],
  "schema": "variant-tail-mutation-controls-v1"
}
```

### Conditional-pilot variant tail sweep

Embedded JSON SHA-256: `d08415fe219355a822473324c52fec2aa0c7efd1037ff5f93859284417fe5420`.

```json
{
  "aggregate_stages": [
    {
      "denominator": 2162688,
      "fail": 0,
      "marginal_pass": 2162688,
      "name": "A16_row",
      "pass": 2162688
    },
    {
      "denominator": 2162688,
      "fail": 2142062,
      "marginal_pass": 20626,
      "name": "E16_row",
      "pass": 20626
    },
    {
      "denominator": 20626,
      "fail": 20452,
      "marginal_pass": 18147,
      "name": "E16_relations",
      "pass": 174
    },
    {
      "denominator": 174,
      "fail": 169,
      "marginal_pass": 6,
      "name": "E17_row",
      "pass": 5
    },
    {
      "denominator": 5,
      "fail": 5,
      "marginal_pass": 0,
      "name": "E18_row",
      "pass": 0
    },
    {
      "denominator": 0,
      "fail": 0,
      "marginal_pass": 541428,
      "name": "E18_relations",
      "pass": 0
    },
    {
      "denominator": 0,
      "fail": 0,
      "marginal_pass": 0,
      "name": "E19_row",
      "pass": 0
    },
    {
      "denominator": 0,
      "fail": 0,
      "marginal_pass": 0,
      "name": "E20_row",
      "pass": 0
    },
    {
      "denominator": 0,
      "fail": 0,
      "marginal_pass": 32768,
      "name": "W20_row",
      "pass": 0
    },
    {
      "denominator": 0,
      "fail": 0,
      "marginal_pass": 49152,
      "name": "W20_relations",
      "pass": 0
    },
    {
      "denominator": 0,
      "fail": 0,
      "marginal_pass": 0,
      "name": "W22_row",
      "pass": 0
    },
    {
      "denominator": 0,
      "fail": 0,
      "marginal_pass": 270336,
      "name": "W22_relations",
      "pass": 0
    },
    {
      "denominator": 0,
      "fail": 0,
      "marginal_pass": 0,
      "name": "C32_collision",
      "pass": 0
    }
  ],
  "bridge_count": 11,
  "candidate_count_per_bridge": 196608,
  "candidate_fnv1a64": "21821011d57a5203",
  "ensemble": "repaired-conditional-pilot",
  "schema": "variant-tail-stage-sweep-v1"
}
```

### Repaired standard-IV cohort tail sweep

Embedded JSON SHA-256: `63fc85f7324679bcac976c3ea268c891db77b937022e0fe488ba0cfaa8831428`.

```json
{
  "aggregate_stages": [
    {
      "denominator": 69009408,
      "fail": 0,
      "marginal_pass": 69009408,
      "name": "A16_row",
      "pass": 69009408
    },
    {
      "denominator": 69009408,
      "fail": 68455009,
      "marginal_pass": 554399,
      "name": "E16_row",
      "pass": 554399
    },
    {
      "denominator": 554399,
      "fail": 550106,
      "marginal_pass": 540046,
      "name": "E16_relations",
      "pass": 4293
    },
    {
      "denominator": 4293,
      "fail": 4158,
      "marginal_pass": 148,
      "name": "E17_row",
      "pass": 135
    },
    {
      "denominator": 135,
      "fail": 128,
      "marginal_pass": 7,
      "name": "E18_row",
      "pass": 7
    },
    {
      "denominator": 7,
      "fail": 5,
      "marginal_pass": 17248924,
      "name": "E18_relations",
      "pass": 2
    },
    {
      "denominator": 2,
      "fail": 2,
      "marginal_pass": 0,
      "name": "E19_row",
      "pass": 0
    },
    {
      "denominator": 0,
      "fail": 0,
      "marginal_pass": 0,
      "name": "E20_row",
      "pass": 0
    },
    {
      "denominator": 0,
      "fail": 0,
      "marginal_pass": 1048576,
      "name": "W20_row",
      "pass": 0
    },
    {
      "denominator": 0,
      "fail": 0,
      "marginal_pass": 1146880,
      "name": "W20_relations",
      "pass": 0
    },
    {
      "denominator": 0,
      "fail": 0,
      "marginal_pass": 23040,
      "name": "W22_row",
      "pass": 0
    },
    {
      "denominator": 0,
      "fail": 0,
      "marginal_pass": 8626176,
      "name": "W22_relations",
      "pass": 0
    },
    {
      "denominator": 0,
      "fail": 0,
      "marginal_pass": 0,
      "name": "C32_collision",
      "pass": 0
    }
  ],
  "bridge_count": 351,
  "candidate_count_per_bridge": 196608,
  "candidate_fnv1a64": "21821011d57a5203",
  "ensemble": "repaired-standard-iv",
  "schema": "variant-tail-stage-sweep-v1"
}
```

### Variant schema-outcome pinned replay

Embedded JSON SHA-256: `44755ea2c152be6e069018cd16110966e3e30b8c9290971c7b3a6590e841fa35`.

```json
{
  "K_distribution": {
    "1": 1
  },
  "all_bridge_stages_pass": true,
  "all_late_stages_pass": true,
  "all_pinned_C32_equal": true,
  "bases_sha256": "e0b35a01758c59e23569a2f4176cfc2b02bd19020dd2cc3c11965af5b2d6cd41",
  "mapping_sha256": "47841a38e8ee86f0d6243b1233ea4ff78b2aa5f5057a93cdcbd7605e6bdfcfbf",
  "measurement_sha256": "6b7520358d43282ab00a19545bec48b3d1da47d07ededcbe0fe582d2b18838bc",
  "pinned_reference_sha256": "514fa8ab8a461e4a41080efa27b4ba2a3b499eeedf0a2d2346e6562835d040f5",
  "pinned_repository_commit": "8a0f02675cdcd58ebfc16119af02a094c3e1dd16",
  "recomputed_pi_uniform_estimate": 1.46484375e-07,
  "recomputed_sum_inverse_K": 1.0,
  "replays": [
    {
      "K": 1,
      "base_bridge_index": 1,
      "cv": "4575efc95e9c7893e29f686b7f32cc08c8b8afd68390f8045c92bf0a232213b4",
      "pinned_C32_output": "af02e1aed615b41d9a8c3e6527053972ba87ec2a0aa8a5c67c044d82f5213206",
      "tail_index": 73275,
      "trial": 5071,
      "variant_id": 26274
    }
  ],
  "schema": "variant-importance-validation-v1",
  "states_sha256": "cc96a713059ceb66f2813116a482f7bc77024d89ebf8411f89ee58ba0ee7d3ab",
  "successes_replayed": 1
}
```

### Precommitted repaired-cohort importance specification

Embedded JSON SHA-256: `340fffd6989e093b55f1337a4e4fb32bf62c2e9287823a79ea97ebe5f3472240`.

```json
{
  "A_half_cohort": "all 351 audited canonical accepts from the precommitted standard-IV C32 seed-2026100519 N=2^33 stream",
  "E_half_law": "abstract reconstruction from the E16/E17/E18/E19 proposal; no standard-IV first-block preimage is known",
  "base_sampling": "uniform over the 351 empirical accepted bridge/variant/record rows",
  "binary_sha256": "0fb174a3d95583f844e979a3b7ccf49b349983177f3324c8168c33b1836bb05e",
  "chronology": "Fixed after the repaired seed-2026100519 N=2^33 stream completed and its independent audit passed, after the fixed-variant 100-million result, and before any seed-2026100522 proposal was evaluated.",
  "command": "tools/localrun.sh -t 600 -n 1 ./variant_tail_measure importance variant_inputs/repaired-variant-states.bin variant_inputs/repaired-c32-seed-2026100519-N33.jsonl 20000000 2026100522 repaired_standard_iv_A_halves_abstract_E_reconstruction variant-importance-repaired-20m.json",
  "created_utc": "2026-10-05T14:04:15Z",
  "figure6_conditions_sha256": "664bfffc35c216cfe3e39f7d806ae0341593dc51ac4431736813748cd5a0bad6",
  "input": "variant_inputs/repaired-c32-seed-2026100519-N33.jsonl",
  "input_audit": "variant_inputs/repaired-c32-seed-2026100519-validation.json",
  "input_audit_sha256": "5468df95122ac055061936e7419fc3610d65902356e5b52c8780831deca9ab26",
  "input_sha256": "ccd81c657ad941374ce2c80584824322287bb9b0432d7fe3f4588e3fd6ba0198",
  "likelihood_ratio_power2": -27,
  "multiplicity": "K counts the same selected event over all 196,608 tails for every selected success",
  "proposal_domain_log2": [
    18,
    27,
    25,
    31
  ],
  "reporting": "Retain per-base counts, every K, exact W4-W6 stages, all successes, and the raw result even if below the fixed-variant estimate. No calibrated confidence interval is claimed.",
  "resource_estimate": {
    "cores": 1,
    "cpu_and_wall_bound": "600 seconds; the completed fixed-variant 100-million run and variant schema regression put the expected run below three minutes including K sweeps",
    "output_disk": "under 5 MiB expected",
    "peak_memory": "under 0.1 GiB; one 196,608-tail vector plus 351 bridge states and counters"
  },
  "schema": "variant-tail-importance-precommit-v1",
  "seed": 2026100522,
  "selected_event": "all named A16-through-W22 path conditions and exact C32 feed-forward equality",
  "source_sha256": "b1fc414eb1e72eca133c3674523c461cf4b1ed57d2ee0c210f7ef9224ab2378c",
  "tail_count": 196608,
  "timeout_seconds": 600,
  "trials": 20000000,
  "variant_mapping_sha256": "47841a38e8ee86f0d6243b1233ea4ff78b2aa5f5057a93cdcbd7605e6bdfcfbf",
  "variant_states": "variant_inputs/repaired-variant-states.bin",
  "variant_states_sha256": "cc96a713059ceb66f2813116a482f7bc77024d89ebf8411f89ee58ba0ee7d3ab"
}
```

### Repaired-cohort 20-million importance result

Embedded JSON SHA-256: `3f77e46b50d152550b7e8794b0ac175c34819a852549fabad93ded38ef1976d3`.

```json
{
  "bridge_count": 351,
  "bridge_stage_counts": [
    {
      "denominator": 20000000,
      "fail": 0,
      "marginal_pass": 20000000,
      "name": "W4_row",
      "pass": 20000000
    },
    {
      "denominator": 20000000,
      "fail": 0,
      "marginal_pass": 20000000,
      "name": "W4_relations",
      "pass": 20000000
    },
    {
      "denominator": 20000000,
      "fail": 0,
      "marginal_pass": 20000000,
      "name": "W5_row",
      "pass": 20000000
    },
    {
      "denominator": 20000000,
      "fail": 0,
      "marginal_pass": 20000000,
      "name": "W5_relations",
      "pass": 20000000
    },
    {
      "denominator": 20000000,
      "fail": 0,
      "marginal_pass": 20000000,
      "name": "W6_row",
      "pass": 20000000
    },
    {
      "denominator": 20000000,
      "fail": 0,
      "marginal_pass": 20000000,
      "name": "W6_relations",
      "pass": 20000000
    }
  ],
  "calibrated_confidence_interval": null,
  "chosen_tail_successes": 43,
  "ensemble": "repaired_standard_iv_A_halves_abstract_E_reconstruction",
  "monte_carlo_standard_error": 4.802806376211615e-10,
  "per_base": [
    {
      "K_values": [],
      "base_bridge_index": 0,
      "base_trial": 17918261,
      "chosen_tail_successes": 0,
      "proposal_count": 57100
    },
    {
      "K_values": [],
      "base_bridge_index": 1,
      "base_trial": 58171330,
      "chosen_tail_successes": 0,
      "proposal_count": 57565
    },
    {
      "K_values": [],
      "base_bridge_index": 2,
      "base_trial": 176484505,
      "chosen_tail_successes": 0,
      "proposal_count": 56781
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 3,
      "base_trial": 176571214,
      "chosen_tail_successes": 1,
      "proposal_count": 56978
    },
    {
      "K_values": [],
      "base_bridge_index": 4,
      "base_trial": 180847483,
      "chosen_tail_successes": 0,
      "proposal_count": 56850
    },
    {
      "K_values": [],
      "base_bridge_index": 5,
      "base_trial": 211521508,
      "chosen_tail_successes": 0,
      "proposal_count": 57004
    },
    {
      "K_values": [],
      "base_bridge_index": 6,
      "base_trial": 234361822,
      "chosen_tail_successes": 0,
      "proposal_count": 56998
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 7,
      "base_trial": 242737276,
      "chosen_tail_successes": 1,
      "proposal_count": 56727
    },
    {
      "K_values": [],
      "base_bridge_index": 8,
      "base_trial": 356734454,
      "chosen_tail_successes": 0,
      "proposal_count": 57054
    },
    {
      "K_values": [],
      "base_bridge_index": 9,
      "base_trial": 374421478,
      "chosen_tail_successes": 0,
      "proposal_count": 56687
    },
    {
      "K_values": [],
      "base_bridge_index": 10,
      "base_trial": 458004772,
      "chosen_tail_successes": 0,
      "proposal_count": 56856
    },
    {
      "K_values": [],
      "base_bridge_index": 11,
      "base_trial": 467563822,
      "chosen_tail_successes": 0,
      "proposal_count": 57112
    },
    {
      "K_values": [],
      "base_bridge_index": 12,
      "base_trial": 532875338,
      "chosen_tail_successes": 0,
      "proposal_count": 56786
    },
    {
      "K_values": [],
      "base_bridge_index": 13,
      "base_trial": 551427412,
      "chosen_tail_successes": 0,
      "proposal_count": 57050
    },
    {
      "K_values": [],
      "base_bridge_index": 14,
      "base_trial": 566600227,
      "chosen_tail_successes": 0,
      "proposal_count": 57021
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 15,
      "base_trial": 569685119,
      "chosen_tail_successes": 1,
      "proposal_count": 57168
    },
    {
      "K_values": [],
      "base_bridge_index": 16,
      "base_trial": 574689321,
      "chosen_tail_successes": 0,
      "proposal_count": 57151
    },
    {
      "K_values": [],
      "base_bridge_index": 17,
      "base_trial": 576855655,
      "chosen_tail_successes": 0,
      "proposal_count": 57375
    },
    {
      "K_values": [],
      "base_bridge_index": 18,
      "base_trial": 625451630,
      "chosen_tail_successes": 0,
      "proposal_count": 56895
    },
    {
      "K_values": [],
      "base_bridge_index": 19,
      "base_trial": 645899945,
      "chosen_tail_successes": 0,
      "proposal_count": 56727
    },
    {
      "K_values": [],
      "base_bridge_index": 20,
      "base_trial": 653652258,
      "chosen_tail_successes": 0,
      "proposal_count": 57122
    },
    {
      "K_values": [],
      "base_bridge_index": 21,
      "base_trial": 725630919,
      "chosen_tail_successes": 0,
      "proposal_count": 56725
    },
    {
      "K_values": [],
      "base_bridge_index": 22,
      "base_trial": 732304285,
      "chosen_tail_successes": 0,
      "proposal_count": 57210
    },
    {
      "K_values": [],
      "base_bridge_index": 23,
      "base_trial": 798373369,
      "chosen_tail_successes": 0,
      "proposal_count": 57028
    },
    {
      "K_values": [],
      "base_bridge_index": 24,
      "base_trial": 812287011,
      "chosen_tail_successes": 0,
      "proposal_count": 56840
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 25,
      "base_trial": 829693419,
      "chosen_tail_successes": 1,
      "proposal_count": 57008
    },
    {
      "K_values": [],
      "base_bridge_index": 26,
      "base_trial": 833032947,
      "chosen_tail_successes": 0,
      "proposal_count": 57300
    },
    {
      "K_values": [],
      "base_bridge_index": 27,
      "base_trial": 897499227,
      "chosen_tail_successes": 0,
      "proposal_count": 57111
    },
    {
      "K_values": [],
      "base_bridge_index": 28,
      "base_trial": 899151807,
      "chosen_tail_successes": 0,
      "proposal_count": 56948
    },
    {
      "K_values": [],
      "base_bridge_index": 29,
      "base_trial": 908178391,
      "chosen_tail_successes": 0,
      "proposal_count": 56650
    },
    {
      "K_values": [],
      "base_bridge_index": 30,
      "base_trial": 926050390,
      "chosen_tail_successes": 0,
      "proposal_count": 56826
    },
    {
      "K_values": [],
      "base_bridge_index": 31,
      "base_trial": 956031028,
      "chosen_tail_successes": 0,
      "proposal_count": 57091
    },
    {
      "K_values": [],
      "base_bridge_index": 32,
      "base_trial": 1001950028,
      "chosen_tail_successes": 0,
      "proposal_count": 56690
    },
    {
      "K_values": [],
      "base_bridge_index": 33,
      "base_trial": 1027402391,
      "chosen_tail_successes": 0,
      "proposal_count": 56719
    },
    {
      "K_values": [],
      "base_bridge_index": 34,
      "base_trial": 1037506219,
      "chosen_tail_successes": 0,
      "proposal_count": 57302
    },
    {
      "K_values": [],
      "base_bridge_index": 35,
      "base_trial": 1049631527,
      "chosen_tail_successes": 0,
      "proposal_count": 56782
    },
    {
      "K_values": [],
      "base_bridge_index": 36,
      "base_trial": 1094935644,
      "chosen_tail_successes": 0,
      "proposal_count": 57036
    },
    {
      "K_values": [],
      "base_bridge_index": 37,
      "base_trial": 1109485953,
      "chosen_tail_successes": 0,
      "proposal_count": 57215
    },
    {
      "K_values": [],
      "base_bridge_index": 38,
      "base_trial": 1240292925,
      "chosen_tail_successes": 0,
      "proposal_count": 56853
    },
    {
      "K_values": [],
      "base_bridge_index": 39,
      "base_trial": 1259690315,
      "chosen_tail_successes": 0,
      "proposal_count": 57138
    },
    {
      "K_values": [],
      "base_bridge_index": 40,
      "base_trial": 1300174125,
      "chosen_tail_successes": 0,
      "proposal_count": 57284
    },
    {
      "K_values": [],
      "base_bridge_index": 41,
      "base_trial": 1349990332,
      "chosen_tail_successes": 0,
      "proposal_count": 56857
    },
    {
      "K_values": [],
      "base_bridge_index": 42,
      "base_trial": 1375663983,
      "chosen_tail_successes": 0,
      "proposal_count": 56722
    },
    {
      "K_values": [],
      "base_bridge_index": 43,
      "base_trial": 1381853267,
      "chosen_tail_successes": 0,
      "proposal_count": 57153
    },
    {
      "K_values": [],
      "base_bridge_index": 44,
      "base_trial": 1399889232,
      "chosen_tail_successes": 0,
      "proposal_count": 57130
    },
    {
      "K_values": [],
      "base_bridge_index": 45,
      "base_trial": 1449664408,
      "chosen_tail_successes": 0,
      "proposal_count": 57315
    },
    {
      "K_values": [],
      "base_bridge_index": 46,
      "base_trial": 1469959780,
      "chosen_tail_successes": 0,
      "proposal_count": 56806
    },
    {
      "K_values": [],
      "base_bridge_index": 47,
      "base_trial": 1518730530,
      "chosen_tail_successes": 0,
      "proposal_count": 57048
    },
    {
      "K_values": [],
      "base_bridge_index": 48,
      "base_trial": 1524627504,
      "chosen_tail_successes": 0,
      "proposal_count": 56886
    },
    {
      "K_values": [],
      "base_bridge_index": 49,
      "base_trial": 1533809422,
      "chosen_tail_successes": 0,
      "proposal_count": 56513
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 50,
      "base_trial": 1536029950,
      "chosen_tail_successes": 1,
      "proposal_count": 56835
    },
    {
      "K_values": [],
      "base_bridge_index": 51,
      "base_trial": 1569105786,
      "chosen_tail_successes": 0,
      "proposal_count": 57348
    },
    {
      "K_values": [],
      "base_bridge_index": 52,
      "base_trial": 1582094747,
      "chosen_tail_successes": 0,
      "proposal_count": 56815
    },
    {
      "K_values": [],
      "base_bridge_index": 53,
      "base_trial": 1645423137,
      "chosen_tail_successes": 0,
      "proposal_count": 56864
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 54,
      "base_trial": 1650921687,
      "chosen_tail_successes": 1,
      "proposal_count": 56901
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 55,
      "base_trial": 1656734836,
      "chosen_tail_successes": 1,
      "proposal_count": 56764
    },
    {
      "K_values": [],
      "base_bridge_index": 56,
      "base_trial": 1681163707,
      "chosen_tail_successes": 0,
      "proposal_count": 57212
    },
    {
      "K_values": [],
      "base_bridge_index": 57,
      "base_trial": 1691945925,
      "chosen_tail_successes": 0,
      "proposal_count": 57279
    },
    {
      "K_values": [],
      "base_bridge_index": 58,
      "base_trial": 1723843173,
      "chosen_tail_successes": 0,
      "proposal_count": 56761
    },
    {
      "K_values": [],
      "base_bridge_index": 59,
      "base_trial": 1770879447,
      "chosen_tail_successes": 0,
      "proposal_count": 57129
    },
    {
      "K_values": [],
      "base_bridge_index": 60,
      "base_trial": 1779238857,
      "chosen_tail_successes": 0,
      "proposal_count": 57106
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 61,
      "base_trial": 1793633921,
      "chosen_tail_successes": 1,
      "proposal_count": 57422
    },
    {
      "K_values": [],
      "base_bridge_index": 62,
      "base_trial": 1798975733,
      "chosen_tail_successes": 0,
      "proposal_count": 56690
    },
    {
      "K_values": [],
      "base_bridge_index": 63,
      "base_trial": 1803095058,
      "chosen_tail_successes": 0,
      "proposal_count": 56964
    },
    {
      "K_values": [],
      "base_bridge_index": 64,
      "base_trial": 1861540286,
      "chosen_tail_successes": 0,
      "proposal_count": 56725
    },
    {
      "K_values": [],
      "base_bridge_index": 65,
      "base_trial": 1866148264,
      "chosen_tail_successes": 0,
      "proposal_count": 56971
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 66,
      "base_trial": 1899658917,
      "chosen_tail_successes": 1,
      "proposal_count": 56834
    },
    {
      "K_values": [],
      "base_bridge_index": 67,
      "base_trial": 1905104905,
      "chosen_tail_successes": 0,
      "proposal_count": 57377
    },
    {
      "K_values": [],
      "base_bridge_index": 68,
      "base_trial": 1928272132,
      "chosen_tail_successes": 0,
      "proposal_count": 56996
    },
    {
      "K_values": [],
      "base_bridge_index": 69,
      "base_trial": 1963884083,
      "chosen_tail_successes": 0,
      "proposal_count": 56553
    },
    {
      "K_values": [],
      "base_bridge_index": 70,
      "base_trial": 2019361165,
      "chosen_tail_successes": 0,
      "proposal_count": 56917
    },
    {
      "K_values": [],
      "base_bridge_index": 71,
      "base_trial": 2054523445,
      "chosen_tail_successes": 0,
      "proposal_count": 57041
    },
    {
      "K_values": [],
      "base_bridge_index": 72,
      "base_trial": 2078151027,
      "chosen_tail_successes": 0,
      "proposal_count": 56970
    },
    {
      "K_values": [],
      "base_bridge_index": 73,
      "base_trial": 2079822372,
      "chosen_tail_successes": 0,
      "proposal_count": 57053
    },
    {
      "K_values": [],
      "base_bridge_index": 74,
      "base_trial": 2190635372,
      "chosen_tail_successes": 0,
      "proposal_count": 57219
    },
    {
      "K_values": [],
      "base_bridge_index": 75,
      "base_trial": 2220429085,
      "chosen_tail_successes": 0,
      "proposal_count": 56840
    },
    {
      "K_values": [],
      "base_bridge_index": 76,
      "base_trial": 2228588909,
      "chosen_tail_successes": 0,
      "proposal_count": 57058
    },
    {
      "K_values": [
        1,
        1
      ],
      "base_bridge_index": 77,
      "base_trial": 2256237956,
      "chosen_tail_successes": 2,
      "proposal_count": 56768
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 78,
      "base_trial": 2266803914,
      "chosen_tail_successes": 1,
      "proposal_count": 56632
    },
    {
      "K_values": [],
      "base_bridge_index": 79,
      "base_trial": 2312760225,
      "chosen_tail_successes": 0,
      "proposal_count": 56835
    },
    {
      "K_values": [],
      "base_bridge_index": 80,
      "base_trial": 2315156034,
      "chosen_tail_successes": 0,
      "proposal_count": 56346
    },
    {
      "K_values": [],
      "base_bridge_index": 81,
      "base_trial": 2465430827,
      "chosen_tail_successes": 0,
      "proposal_count": 57070
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 82,
      "base_trial": 2475422852,
      "chosen_tail_successes": 1,
      "proposal_count": 57001
    },
    {
      "K_values": [],
      "base_bridge_index": 83,
      "base_trial": 2495979999,
      "chosen_tail_successes": 0,
      "proposal_count": 56714
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 84,
      "base_trial": 2509822694,
      "chosen_tail_successes": 1,
      "proposal_count": 56529
    },
    {
      "K_values": [],
      "base_bridge_index": 85,
      "base_trial": 2527247714,
      "chosen_tail_successes": 0,
      "proposal_count": 57729
    },
    {
      "K_values": [],
      "base_bridge_index": 86,
      "base_trial": 2539787952,
      "chosen_tail_successes": 0,
      "proposal_count": 57160
    },
    {
      "K_values": [],
      "base_bridge_index": 87,
      "base_trial": 2582284596,
      "chosen_tail_successes": 0,
      "proposal_count": 56566
    },
    {
      "K_values": [],
      "base_bridge_index": 88,
      "base_trial": 2655924392,
      "chosen_tail_successes": 0,
      "proposal_count": 56798
    },
    {
      "K_values": [],
      "base_bridge_index": 89,
      "base_trial": 2701254389,
      "chosen_tail_successes": 0,
      "proposal_count": 56766
    },
    {
      "K_values": [],
      "base_bridge_index": 90,
      "base_trial": 2718023585,
      "chosen_tail_successes": 0,
      "proposal_count": 57296
    },
    {
      "K_values": [],
      "base_bridge_index": 91,
      "base_trial": 2751745380,
      "chosen_tail_successes": 0,
      "proposal_count": 56814
    },
    {
      "K_values": [],
      "base_bridge_index": 92,
      "base_trial": 2762053470,
      "chosen_tail_successes": 0,
      "proposal_count": 57345
    },
    {
      "K_values": [],
      "base_bridge_index": 93,
      "base_trial": 2777842042,
      "chosen_tail_successes": 0,
      "proposal_count": 56927
    },
    {
      "K_values": [],
      "base_bridge_index": 94,
      "base_trial": 2787158155,
      "chosen_tail_successes": 0,
      "proposal_count": 57205
    },
    {
      "K_values": [],
      "base_bridge_index": 95,
      "base_trial": 2793375959,
      "chosen_tail_successes": 0,
      "proposal_count": 57135
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 96,
      "base_trial": 2812452456,
      "chosen_tail_successes": 1,
      "proposal_count": 56959
    },
    {
      "K_values": [],
      "base_bridge_index": 97,
      "base_trial": 2873961830,
      "chosen_tail_successes": 0,
      "proposal_count": 57157
    },
    {
      "K_values": [],
      "base_bridge_index": 98,
      "base_trial": 2890183596,
      "chosen_tail_successes": 0,
      "proposal_count": 56883
    },
    {
      "K_values": [],
      "base_bridge_index": 99,
      "base_trial": 2920785542,
      "chosen_tail_successes": 0,
      "proposal_count": 56985
    },
    {
      "K_values": [],
      "base_bridge_index": 100,
      "base_trial": 2936861214,
      "chosen_tail_successes": 0,
      "proposal_count": 57199
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 101,
      "base_trial": 3035033518,
      "chosen_tail_successes": 1,
      "proposal_count": 56803
    },
    {
      "K_values": [],
      "base_bridge_index": 102,
      "base_trial": 3039037891,
      "chosen_tail_successes": 0,
      "proposal_count": 57227
    },
    {
      "K_values": [],
      "base_bridge_index": 103,
      "base_trial": 3072422221,
      "chosen_tail_successes": 0,
      "proposal_count": 57488
    },
    {
      "K_values": [],
      "base_bridge_index": 104,
      "base_trial": 3120123029,
      "chosen_tail_successes": 0,
      "proposal_count": 57596
    },
    {
      "K_values": [],
      "base_bridge_index": 105,
      "base_trial": 3170542454,
      "chosen_tail_successes": 0,
      "proposal_count": 57144
    },
    {
      "K_values": [],
      "base_bridge_index": 106,
      "base_trial": 3189108471,
      "chosen_tail_successes": 0,
      "proposal_count": 56793
    },
    {
      "K_values": [],
      "base_bridge_index": 107,
      "base_trial": 3200283645,
      "chosen_tail_successes": 0,
      "proposal_count": 56874
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 108,
      "base_trial": 3207227824,
      "chosen_tail_successes": 1,
      "proposal_count": 56984
    },
    {
      "K_values": [],
      "base_bridge_index": 109,
      "base_trial": 3221533102,
      "chosen_tail_successes": 0,
      "proposal_count": 56792
    },
    {
      "K_values": [
        1,
        1
      ],
      "base_bridge_index": 110,
      "base_trial": 3230645753,
      "chosen_tail_successes": 2,
      "proposal_count": 57026
    },
    {
      "K_values": [],
      "base_bridge_index": 111,
      "base_trial": 3234619894,
      "chosen_tail_successes": 0,
      "proposal_count": 56673
    },
    {
      "K_values": [],
      "base_bridge_index": 112,
      "base_trial": 3269571455,
      "chosen_tail_successes": 0,
      "proposal_count": 56883
    },
    {
      "K_values": [],
      "base_bridge_index": 113,
      "base_trial": 3271828414,
      "chosen_tail_successes": 0,
      "proposal_count": 56936
    },
    {
      "K_values": [],
      "base_bridge_index": 114,
      "base_trial": 3341553603,
      "chosen_tail_successes": 0,
      "proposal_count": 57208
    },
    {
      "K_values": [],
      "base_bridge_index": 115,
      "base_trial": 3401200615,
      "chosen_tail_successes": 0,
      "proposal_count": 56749
    },
    {
      "K_values": [],
      "base_bridge_index": 116,
      "base_trial": 3402597156,
      "chosen_tail_successes": 0,
      "proposal_count": 57211
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 117,
      "base_trial": 3412427434,
      "chosen_tail_successes": 1,
      "proposal_count": 57094
    },
    {
      "K_values": [],
      "base_bridge_index": 118,
      "base_trial": 3418641620,
      "chosen_tail_successes": 0,
      "proposal_count": 56661
    },
    {
      "K_values": [],
      "base_bridge_index": 119,
      "base_trial": 3438862636,
      "chosen_tail_successes": 0,
      "proposal_count": 56913
    },
    {
      "K_values": [],
      "base_bridge_index": 120,
      "base_trial": 3440805650,
      "chosen_tail_successes": 0,
      "proposal_count": 57120
    },
    {
      "K_values": [],
      "base_bridge_index": 121,
      "base_trial": 3474897441,
      "chosen_tail_successes": 0,
      "proposal_count": 57022
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 122,
      "base_trial": 3535055328,
      "chosen_tail_successes": 1,
      "proposal_count": 56830
    },
    {
      "K_values": [],
      "base_bridge_index": 123,
      "base_trial": 3541534546,
      "chosen_tail_successes": 0,
      "proposal_count": 56691
    },
    {
      "K_values": [],
      "base_bridge_index": 124,
      "base_trial": 3564056213,
      "chosen_tail_successes": 0,
      "proposal_count": 57239
    },
    {
      "K_values": [],
      "base_bridge_index": 125,
      "base_trial": 3570024152,
      "chosen_tail_successes": 0,
      "proposal_count": 56464
    },
    {
      "K_values": [],
      "base_bridge_index": 126,
      "base_trial": 3580041632,
      "chosen_tail_successes": 0,
      "proposal_count": 56995
    },
    {
      "K_values": [],
      "base_bridge_index": 127,
      "base_trial": 3581942504,
      "chosen_tail_successes": 0,
      "proposal_count": 57307
    },
    {
      "K_values": [],
      "base_bridge_index": 128,
      "base_trial": 3583612532,
      "chosen_tail_successes": 0,
      "proposal_count": 56988
    },
    {
      "K_values": [],
      "base_bridge_index": 129,
      "base_trial": 3610731986,
      "chosen_tail_successes": 0,
      "proposal_count": 56947
    },
    {
      "K_values": [],
      "base_bridge_index": 130,
      "base_trial": 3623699258,
      "chosen_tail_successes": 0,
      "proposal_count": 57448
    },
    {
      "K_values": [],
      "base_bridge_index": 131,
      "base_trial": 3641293677,
      "chosen_tail_successes": 0,
      "proposal_count": 56487
    },
    {
      "K_values": [],
      "base_bridge_index": 132,
      "base_trial": 3656378447,
      "chosen_tail_successes": 0,
      "proposal_count": 57124
    },
    {
      "K_values": [],
      "base_bridge_index": 133,
      "base_trial": 3712556344,
      "chosen_tail_successes": 0,
      "proposal_count": 57188
    },
    {
      "K_values": [],
      "base_bridge_index": 134,
      "base_trial": 3722082478,
      "chosen_tail_successes": 0,
      "proposal_count": 56724
    },
    {
      "K_values": [],
      "base_bridge_index": 135,
      "base_trial": 3742342207,
      "chosen_tail_successes": 0,
      "proposal_count": 56968
    },
    {
      "K_values": [],
      "base_bridge_index": 136,
      "base_trial": 3747501459,
      "chosen_tail_successes": 0,
      "proposal_count": 56811
    },
    {
      "K_values": [],
      "base_bridge_index": 137,
      "base_trial": 3837293419,
      "chosen_tail_successes": 0,
      "proposal_count": 57342
    },
    {
      "K_values": [],
      "base_bridge_index": 138,
      "base_trial": 3919360579,
      "chosen_tail_successes": 0,
      "proposal_count": 56994
    },
    {
      "K_values": [],
      "base_bridge_index": 139,
      "base_trial": 3925405711,
      "chosen_tail_successes": 0,
      "proposal_count": 56827
    },
    {
      "K_values": [],
      "base_bridge_index": 140,
      "base_trial": 3926820994,
      "chosen_tail_successes": 0,
      "proposal_count": 57059
    },
    {
      "K_values": [],
      "base_bridge_index": 141,
      "base_trial": 3929084595,
      "chosen_tail_successes": 0,
      "proposal_count": 56930
    },
    {
      "K_values": [],
      "base_bridge_index": 142,
      "base_trial": 3943673105,
      "chosen_tail_successes": 0,
      "proposal_count": 56799
    },
    {
      "K_values": [],
      "base_bridge_index": 143,
      "base_trial": 3991348442,
      "chosen_tail_successes": 0,
      "proposal_count": 57119
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 144,
      "base_trial": 3991375129,
      "chosen_tail_successes": 1,
      "proposal_count": 56855
    },
    {
      "K_values": [],
      "base_bridge_index": 145,
      "base_trial": 3994386385,
      "chosen_tail_successes": 0,
      "proposal_count": 57204
    },
    {
      "K_values": [],
      "base_bridge_index": 146,
      "base_trial": 4011730510,
      "chosen_tail_successes": 0,
      "proposal_count": 57279
    },
    {
      "K_values": [],
      "base_bridge_index": 147,
      "base_trial": 4021246364,
      "chosen_tail_successes": 0,
      "proposal_count": 57273
    },
    {
      "K_values": [],
      "base_bridge_index": 148,
      "base_trial": 4102221293,
      "chosen_tail_successes": 0,
      "proposal_count": 56782
    },
    {
      "K_values": [],
      "base_bridge_index": 149,
      "base_trial": 4134000870,
      "chosen_tail_successes": 0,
      "proposal_count": 56706
    },
    {
      "K_values": [],
      "base_bridge_index": 150,
      "base_trial": 4159386436,
      "chosen_tail_successes": 0,
      "proposal_count": 56704
    },
    {
      "K_values": [],
      "base_bridge_index": 151,
      "base_trial": 4170629027,
      "chosen_tail_successes": 0,
      "proposal_count": 56628
    },
    {
      "K_values": [],
      "base_bridge_index": 152,
      "base_trial": 4208264472,
      "chosen_tail_successes": 0,
      "proposal_count": 56898
    },
    {
      "K_values": [],
      "base_bridge_index": 153,
      "base_trial": 4221118422,
      "chosen_tail_successes": 0,
      "proposal_count": 57092
    },
    {
      "K_values": [],
      "base_bridge_index": 154,
      "base_trial": 4224463269,
      "chosen_tail_successes": 0,
      "proposal_count": 57036
    },
    {
      "K_values": [],
      "base_bridge_index": 155,
      "base_trial": 4268249297,
      "chosen_tail_successes": 0,
      "proposal_count": 57042
    },
    {
      "K_values": [],
      "base_bridge_index": 156,
      "base_trial": 4295963325,
      "chosen_tail_successes": 0,
      "proposal_count": 57286
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 157,
      "base_trial": 4296228071,
      "chosen_tail_successes": 1,
      "proposal_count": 56742
    },
    {
      "K_values": [],
      "base_bridge_index": 158,
      "base_trial": 4323530517,
      "chosen_tail_successes": 0,
      "proposal_count": 57075
    },
    {
      "K_values": [],
      "base_bridge_index": 159,
      "base_trial": 4337876831,
      "chosen_tail_successes": 0,
      "proposal_count": 57704
    },
    {
      "K_values": [],
      "base_bridge_index": 160,
      "base_trial": 4341333359,
      "chosen_tail_successes": 0,
      "proposal_count": 57468
    },
    {
      "K_values": [],
      "base_bridge_index": 161,
      "base_trial": 4350642310,
      "chosen_tail_successes": 0,
      "proposal_count": 56464
    },
    {
      "K_values": [],
      "base_bridge_index": 162,
      "base_trial": 4425306164,
      "chosen_tail_successes": 0,
      "proposal_count": 57204
    },
    {
      "K_values": [],
      "base_bridge_index": 163,
      "base_trial": 4431978134,
      "chosen_tail_successes": 0,
      "proposal_count": 57094
    },
    {
      "K_values": [],
      "base_bridge_index": 164,
      "base_trial": 4448065696,
      "chosen_tail_successes": 0,
      "proposal_count": 57043
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 165,
      "base_trial": 4506959748,
      "chosen_tail_successes": 1,
      "proposal_count": 56873
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 166,
      "base_trial": 4511461196,
      "chosen_tail_successes": 1,
      "proposal_count": 57235
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 167,
      "base_trial": 4513635963,
      "chosen_tail_successes": 1,
      "proposal_count": 56948
    },
    {
      "K_values": [],
      "base_bridge_index": 168,
      "base_trial": 4558337258,
      "chosen_tail_successes": 0,
      "proposal_count": 56814
    },
    {
      "K_values": [],
      "base_bridge_index": 169,
      "base_trial": 4584344386,
      "chosen_tail_successes": 0,
      "proposal_count": 57530
    },
    {
      "K_values": [],
      "base_bridge_index": 170,
      "base_trial": 4602385768,
      "chosen_tail_successes": 0,
      "proposal_count": 57188
    },
    {
      "K_values": [],
      "base_bridge_index": 171,
      "base_trial": 4603802380,
      "chosen_tail_successes": 0,
      "proposal_count": 56895
    },
    {
      "K_values": [],
      "base_bridge_index": 172,
      "base_trial": 4623116153,
      "chosen_tail_successes": 0,
      "proposal_count": 56489
    },
    {
      "K_values": [],
      "base_bridge_index": 173,
      "base_trial": 4633260251,
      "chosen_tail_successes": 0,
      "proposal_count": 56952
    },
    {
      "K_values": [],
      "base_bridge_index": 174,
      "base_trial": 4645743701,
      "chosen_tail_successes": 0,
      "proposal_count": 57078
    },
    {
      "K_values": [],
      "base_bridge_index": 175,
      "base_trial": 4663073782,
      "chosen_tail_successes": 0,
      "proposal_count": 57114
    },
    {
      "K_values": [],
      "base_bridge_index": 176,
      "base_trial": 4664292545,
      "chosen_tail_successes": 0,
      "proposal_count": 57128
    },
    {
      "K_values": [],
      "base_bridge_index": 177,
      "base_trial": 4731760534,
      "chosen_tail_successes": 0,
      "proposal_count": 56622
    },
    {
      "K_values": [],
      "base_bridge_index": 178,
      "base_trial": 4786198809,
      "chosen_tail_successes": 0,
      "proposal_count": 56698
    },
    {
      "K_values": [],
      "base_bridge_index": 179,
      "base_trial": 4789031057,
      "chosen_tail_successes": 0,
      "proposal_count": 57117
    },
    {
      "K_values": [],
      "base_bridge_index": 180,
      "base_trial": 4825631097,
      "chosen_tail_successes": 0,
      "proposal_count": 56795
    },
    {
      "K_values": [],
      "base_bridge_index": 181,
      "base_trial": 4825944230,
      "chosen_tail_successes": 0,
      "proposal_count": 56808
    },
    {
      "K_values": [],
      "base_bridge_index": 182,
      "base_trial": 4831916289,
      "chosen_tail_successes": 0,
      "proposal_count": 57274
    },
    {
      "K_values": [],
      "base_bridge_index": 183,
      "base_trial": 4897547518,
      "chosen_tail_successes": 0,
      "proposal_count": 56939
    },
    {
      "K_values": [],
      "base_bridge_index": 184,
      "base_trial": 4906341245,
      "chosen_tail_successes": 0,
      "proposal_count": 56898
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 185,
      "base_trial": 4920084861,
      "chosen_tail_successes": 1,
      "proposal_count": 56922
    },
    {
      "K_values": [],
      "base_bridge_index": 186,
      "base_trial": 4931549186,
      "chosen_tail_successes": 0,
      "proposal_count": 57392
    },
    {
      "K_values": [],
      "base_bridge_index": 187,
      "base_trial": 4961498883,
      "chosen_tail_successes": 0,
      "proposal_count": 57182
    },
    {
      "K_values": [],
      "base_bridge_index": 188,
      "base_trial": 4986810986,
      "chosen_tail_successes": 0,
      "proposal_count": 57279
    },
    {
      "K_values": [],
      "base_bridge_index": 189,
      "base_trial": 5032695316,
      "chosen_tail_successes": 0,
      "proposal_count": 57134
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 190,
      "base_trial": 5047961576,
      "chosen_tail_successes": 1,
      "proposal_count": 56866
    },
    {
      "K_values": [],
      "base_bridge_index": 191,
      "base_trial": 5134087340,
      "chosen_tail_successes": 0,
      "proposal_count": 56684
    },
    {
      "K_values": [],
      "base_bridge_index": 192,
      "base_trial": 5137028660,
      "chosen_tail_successes": 0,
      "proposal_count": 56623
    },
    {
      "K_values": [],
      "base_bridge_index": 193,
      "base_trial": 5145369362,
      "chosen_tail_successes": 0,
      "proposal_count": 56886
    },
    {
      "K_values": [],
      "base_bridge_index": 194,
      "base_trial": 5163730141,
      "chosen_tail_successes": 0,
      "proposal_count": 57045
    },
    {
      "K_values": [],
      "base_bridge_index": 195,
      "base_trial": 5168706797,
      "chosen_tail_successes": 0,
      "proposal_count": 56924
    },
    {
      "K_values": [],
      "base_bridge_index": 196,
      "base_trial": 5201956621,
      "chosen_tail_successes": 0,
      "proposal_count": 57042
    },
    {
      "K_values": [],
      "base_bridge_index": 197,
      "base_trial": 5285323916,
      "chosen_tail_successes": 0,
      "proposal_count": 57023
    },
    {
      "K_values": [],
      "base_bridge_index": 198,
      "base_trial": 5344536769,
      "chosen_tail_successes": 0,
      "proposal_count": 56952
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 199,
      "base_trial": 5344768182,
      "chosen_tail_successes": 1,
      "proposal_count": 56965
    },
    {
      "K_values": [],
      "base_bridge_index": 200,
      "base_trial": 5369885597,
      "chosen_tail_successes": 0,
      "proposal_count": 56607
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 201,
      "base_trial": 5382803788,
      "chosen_tail_successes": 1,
      "proposal_count": 57099
    },
    {
      "K_values": [],
      "base_bridge_index": 202,
      "base_trial": 5383292772,
      "chosen_tail_successes": 0,
      "proposal_count": 57384
    },
    {
      "K_values": [],
      "base_bridge_index": 203,
      "base_trial": 5411426812,
      "chosen_tail_successes": 0,
      "proposal_count": 56846
    },
    {
      "K_values": [],
      "base_bridge_index": 204,
      "base_trial": 5421342576,
      "chosen_tail_successes": 0,
      "proposal_count": 57364
    },
    {
      "K_values": [],
      "base_bridge_index": 205,
      "base_trial": 5430106471,
      "chosen_tail_successes": 0,
      "proposal_count": 56907
    },
    {
      "K_values": [],
      "base_bridge_index": 206,
      "base_trial": 5445411146,
      "chosen_tail_successes": 0,
      "proposal_count": 57071
    },
    {
      "K_values": [],
      "base_bridge_index": 207,
      "base_trial": 5494229096,
      "chosen_tail_successes": 0,
      "proposal_count": 57252
    },
    {
      "K_values": [],
      "base_bridge_index": 208,
      "base_trial": 5523842774,
      "chosen_tail_successes": 0,
      "proposal_count": 56791
    },
    {
      "K_values": [],
      "base_bridge_index": 209,
      "base_trial": 5547305233,
      "chosen_tail_successes": 0,
      "proposal_count": 57108
    },
    {
      "K_values": [],
      "base_bridge_index": 210,
      "base_trial": 5550261902,
      "chosen_tail_successes": 0,
      "proposal_count": 57194
    },
    {
      "K_values": [],
      "base_bridge_index": 211,
      "base_trial": 5559338256,
      "chosen_tail_successes": 0,
      "proposal_count": 57403
    },
    {
      "K_values": [],
      "base_bridge_index": 212,
      "base_trial": 5565631893,
      "chosen_tail_successes": 0,
      "proposal_count": 57143
    },
    {
      "K_values": [],
      "base_bridge_index": 213,
      "base_trial": 5570113404,
      "chosen_tail_successes": 0,
      "proposal_count": 56878
    },
    {
      "K_values": [],
      "base_bridge_index": 214,
      "base_trial": 5605752319,
      "chosen_tail_successes": 0,
      "proposal_count": 56785
    },
    {
      "K_values": [],
      "base_bridge_index": 215,
      "base_trial": 5608026028,
      "chosen_tail_successes": 0,
      "proposal_count": 57090
    },
    {
      "K_values": [],
      "base_bridge_index": 216,
      "base_trial": 5621357057,
      "chosen_tail_successes": 0,
      "proposal_count": 56926
    },
    {
      "K_values": [],
      "base_bridge_index": 217,
      "base_trial": 5641939140,
      "chosen_tail_successes": 0,
      "proposal_count": 56736
    },
    {
      "K_values": [],
      "base_bridge_index": 218,
      "base_trial": 5657413702,
      "chosen_tail_successes": 0,
      "proposal_count": 56769
    },
    {
      "K_values": [],
      "base_bridge_index": 219,
      "base_trial": 5671278149,
      "chosen_tail_successes": 0,
      "proposal_count": 57062
    },
    {
      "K_values": [],
      "base_bridge_index": 220,
      "base_trial": 5709905767,
      "chosen_tail_successes": 0,
      "proposal_count": 56648
    },
    {
      "K_values": [],
      "base_bridge_index": 221,
      "base_trial": 5715672783,
      "chosen_tail_successes": 0,
      "proposal_count": 56753
    },
    {
      "K_values": [],
      "base_bridge_index": 222,
      "base_trial": 5744118167,
      "chosen_tail_successes": 0,
      "proposal_count": 56968
    },
    {
      "K_values": [],
      "base_bridge_index": 223,
      "base_trial": 5754318305,
      "chosen_tail_successes": 0,
      "proposal_count": 56895
    },
    {
      "K_values": [],
      "base_bridge_index": 224,
      "base_trial": 5767037210,
      "chosen_tail_successes": 0,
      "proposal_count": 56759
    },
    {
      "K_values": [],
      "base_bridge_index": 225,
      "base_trial": 5834780951,
      "chosen_tail_successes": 0,
      "proposal_count": 56661
    },
    {
      "K_values": [],
      "base_bridge_index": 226,
      "base_trial": 5835634791,
      "chosen_tail_successes": 0,
      "proposal_count": 56673
    },
    {
      "K_values": [],
      "base_bridge_index": 227,
      "base_trial": 5849549140,
      "chosen_tail_successes": 0,
      "proposal_count": 56838
    },
    {
      "K_values": [],
      "base_bridge_index": 228,
      "base_trial": 5877606839,
      "chosen_tail_successes": 0,
      "proposal_count": 56780
    },
    {
      "K_values": [],
      "base_bridge_index": 229,
      "base_trial": 5884468264,
      "chosen_tail_successes": 0,
      "proposal_count": 57041
    },
    {
      "K_values": [],
      "base_bridge_index": 230,
      "base_trial": 5901145278,
      "chosen_tail_successes": 0,
      "proposal_count": 57088
    },
    {
      "K_values": [],
      "base_bridge_index": 231,
      "base_trial": 5923082135,
      "chosen_tail_successes": 0,
      "proposal_count": 57070
    },
    {
      "K_values": [],
      "base_bridge_index": 232,
      "base_trial": 5929811841,
      "chosen_tail_successes": 0,
      "proposal_count": 56781
    },
    {
      "K_values": [],
      "base_bridge_index": 233,
      "base_trial": 5955278585,
      "chosen_tail_successes": 0,
      "proposal_count": 57409
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 234,
      "base_trial": 5969543452,
      "chosen_tail_successes": 1,
      "proposal_count": 57080
    },
    {
      "K_values": [],
      "base_bridge_index": 235,
      "base_trial": 5975978024,
      "chosen_tail_successes": 0,
      "proposal_count": 56774
    },
    {
      "K_values": [],
      "base_bridge_index": 236,
      "base_trial": 5991598506,
      "chosen_tail_successes": 0,
      "proposal_count": 56882
    },
    {
      "K_values": [],
      "base_bridge_index": 237,
      "base_trial": 6006256450,
      "chosen_tail_successes": 0,
      "proposal_count": 57091
    },
    {
      "K_values": [],
      "base_bridge_index": 238,
      "base_trial": 6017240897,
      "chosen_tail_successes": 0,
      "proposal_count": 57199
    },
    {
      "K_values": [],
      "base_bridge_index": 239,
      "base_trial": 6045822586,
      "chosen_tail_successes": 0,
      "proposal_count": 56861
    },
    {
      "K_values": [],
      "base_bridge_index": 240,
      "base_trial": 6090234471,
      "chosen_tail_successes": 0,
      "proposal_count": 57469
    },
    {
      "K_values": [],
      "base_bridge_index": 241,
      "base_trial": 6093678444,
      "chosen_tail_successes": 0,
      "proposal_count": 56935
    },
    {
      "K_values": [],
      "base_bridge_index": 242,
      "base_trial": 6162988136,
      "chosen_tail_successes": 0,
      "proposal_count": 57614
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 243,
      "base_trial": 6165336792,
      "chosen_tail_successes": 1,
      "proposal_count": 56841
    },
    {
      "K_values": [],
      "base_bridge_index": 244,
      "base_trial": 6185755351,
      "chosen_tail_successes": 0,
      "proposal_count": 56791
    },
    {
      "K_values": [],
      "base_bridge_index": 245,
      "base_trial": 6210832266,
      "chosen_tail_successes": 0,
      "proposal_count": 57080
    },
    {
      "K_values": [],
      "base_bridge_index": 246,
      "base_trial": 6217055846,
      "chosen_tail_successes": 0,
      "proposal_count": 57057
    },
    {
      "K_values": [],
      "base_bridge_index": 247,
      "base_trial": 6226885705,
      "chosen_tail_successes": 0,
      "proposal_count": 57518
    },
    {
      "K_values": [],
      "base_bridge_index": 248,
      "base_trial": 6246271270,
      "chosen_tail_successes": 0,
      "proposal_count": 56827
    },
    {
      "K_values": [],
      "base_bridge_index": 249,
      "base_trial": 6246861211,
      "chosen_tail_successes": 0,
      "proposal_count": 56951
    },
    {
      "K_values": [],
      "base_bridge_index": 250,
      "base_trial": 6293960876,
      "chosen_tail_successes": 0,
      "proposal_count": 56933
    },
    {
      "K_values": [],
      "base_bridge_index": 251,
      "base_trial": 6336304565,
      "chosen_tail_successes": 0,
      "proposal_count": 57110
    },
    {
      "K_values": [],
      "base_bridge_index": 252,
      "base_trial": 6336954817,
      "chosen_tail_successes": 0,
      "proposal_count": 56866
    },
    {
      "K_values": [],
      "base_bridge_index": 253,
      "base_trial": 6373300667,
      "chosen_tail_successes": 0,
      "proposal_count": 56818
    },
    {
      "K_values": [],
      "base_bridge_index": 254,
      "base_trial": 6375401129,
      "chosen_tail_successes": 0,
      "proposal_count": 56974
    },
    {
      "K_values": [],
      "base_bridge_index": 255,
      "base_trial": 6394572667,
      "chosen_tail_successes": 0,
      "proposal_count": 57048
    },
    {
      "K_values": [],
      "base_bridge_index": 256,
      "base_trial": 6394711508,
      "chosen_tail_successes": 0,
      "proposal_count": 57384
    },
    {
      "K_values": [],
      "base_bridge_index": 257,
      "base_trial": 6442767461,
      "chosen_tail_successes": 0,
      "proposal_count": 56877
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 258,
      "base_trial": 6449730767,
      "chosen_tail_successes": 1,
      "proposal_count": 56896
    },
    {
      "K_values": [],
      "base_bridge_index": 259,
      "base_trial": 6456593903,
      "chosen_tail_successes": 0,
      "proposal_count": 57366
    },
    {
      "K_values": [],
      "base_bridge_index": 260,
      "base_trial": 6477949151,
      "chosen_tail_successes": 0,
      "proposal_count": 57081
    },
    {
      "K_values": [],
      "base_bridge_index": 261,
      "base_trial": 6479976413,
      "chosen_tail_successes": 0,
      "proposal_count": 57034
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 262,
      "base_trial": 6486758621,
      "chosen_tail_successes": 1,
      "proposal_count": 57453
    },
    {
      "K_values": [],
      "base_bridge_index": 263,
      "base_trial": 6509915228,
      "chosen_tail_successes": 0,
      "proposal_count": 57360
    },
    {
      "K_values": [],
      "base_bridge_index": 264,
      "base_trial": 6572882004,
      "chosen_tail_successes": 0,
      "proposal_count": 56778
    },
    {
      "K_values": [],
      "base_bridge_index": 265,
      "base_trial": 6579945969,
      "chosen_tail_successes": 0,
      "proposal_count": 56716
    },
    {
      "K_values": [],
      "base_bridge_index": 266,
      "base_trial": 6622423105,
      "chosen_tail_successes": 0,
      "proposal_count": 57039
    },
    {
      "K_values": [],
      "base_bridge_index": 267,
      "base_trial": 6643460885,
      "chosen_tail_successes": 0,
      "proposal_count": 57038
    },
    {
      "K_values": [],
      "base_bridge_index": 268,
      "base_trial": 6653624312,
      "chosen_tail_successes": 0,
      "proposal_count": 56647
    },
    {
      "K_values": [],
      "base_bridge_index": 269,
      "base_trial": 6654819135,
      "chosen_tail_successes": 0,
      "proposal_count": 57101
    },
    {
      "K_values": [],
      "base_bridge_index": 270,
      "base_trial": 6662530716,
      "chosen_tail_successes": 0,
      "proposal_count": 56871
    },
    {
      "K_values": [],
      "base_bridge_index": 271,
      "base_trial": 6686669610,
      "chosen_tail_successes": 0,
      "proposal_count": 56833
    },
    {
      "K_values": [],
      "base_bridge_index": 272,
      "base_trial": 6749891543,
      "chosen_tail_successes": 0,
      "proposal_count": 56933
    },
    {
      "K_values": [
        1,
        1
      ],
      "base_bridge_index": 273,
      "base_trial": 6780169865,
      "chosen_tail_successes": 2,
      "proposal_count": 57105
    },
    {
      "K_values": [],
      "base_bridge_index": 274,
      "base_trial": 6792208361,
      "chosen_tail_successes": 0,
      "proposal_count": 57278
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 275,
      "base_trial": 6809960270,
      "chosen_tail_successes": 1,
      "proposal_count": 57057
    },
    {
      "K_values": [],
      "base_bridge_index": 276,
      "base_trial": 6829329218,
      "chosen_tail_successes": 0,
      "proposal_count": 57093
    },
    {
      "K_values": [],
      "base_bridge_index": 277,
      "base_trial": 6861752273,
      "chosen_tail_successes": 0,
      "proposal_count": 57090
    },
    {
      "K_values": [],
      "base_bridge_index": 278,
      "base_trial": 6896150822,
      "chosen_tail_successes": 0,
      "proposal_count": 57323
    },
    {
      "K_values": [],
      "base_bridge_index": 279,
      "base_trial": 6897794761,
      "chosen_tail_successes": 0,
      "proposal_count": 56696
    },
    {
      "K_values": [],
      "base_bridge_index": 280,
      "base_trial": 6898487902,
      "chosen_tail_successes": 0,
      "proposal_count": 57021
    },
    {
      "K_values": [],
      "base_bridge_index": 281,
      "base_trial": 6987430412,
      "chosen_tail_successes": 0,
      "proposal_count": 56942
    },
    {
      "K_values": [],
      "base_bridge_index": 282,
      "base_trial": 6990858687,
      "chosen_tail_successes": 0,
      "proposal_count": 57042
    },
    {
      "K_values": [],
      "base_bridge_index": 283,
      "base_trial": 7038964774,
      "chosen_tail_successes": 0,
      "proposal_count": 57363
    },
    {
      "K_values": [],
      "base_bridge_index": 284,
      "base_trial": 7043449762,
      "chosen_tail_successes": 0,
      "proposal_count": 56735
    },
    {
      "K_values": [],
      "base_bridge_index": 285,
      "base_trial": 7092844181,
      "chosen_tail_successes": 0,
      "proposal_count": 56991
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 286,
      "base_trial": 7099823441,
      "chosen_tail_successes": 1,
      "proposal_count": 56936
    },
    {
      "K_values": [],
      "base_bridge_index": 287,
      "base_trial": 7129424377,
      "chosen_tail_successes": 0,
      "proposal_count": 56885
    },
    {
      "K_values": [],
      "base_bridge_index": 288,
      "base_trial": 7161152705,
      "chosen_tail_successes": 0,
      "proposal_count": 57046
    },
    {
      "K_values": [],
      "base_bridge_index": 289,
      "base_trial": 7221960449,
      "chosen_tail_successes": 0,
      "proposal_count": 56564
    },
    {
      "K_values": [],
      "base_bridge_index": 290,
      "base_trial": 7239340091,
      "chosen_tail_successes": 0,
      "proposal_count": 56815
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 291,
      "base_trial": 7257857987,
      "chosen_tail_successes": 1,
      "proposal_count": 57161
    },
    {
      "K_values": [],
      "base_bridge_index": 292,
      "base_trial": 7262317304,
      "chosen_tail_successes": 0,
      "proposal_count": 56643
    },
    {
      "K_values": [],
      "base_bridge_index": 293,
      "base_trial": 7266161005,
      "chosen_tail_successes": 0,
      "proposal_count": 56989
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 294,
      "base_trial": 7279865028,
      "chosen_tail_successes": 1,
      "proposal_count": 57141
    },
    {
      "K_values": [],
      "base_bridge_index": 295,
      "base_trial": 7289864765,
      "chosen_tail_successes": 0,
      "proposal_count": 57467
    },
    {
      "K_values": [],
      "base_bridge_index": 296,
      "base_trial": 7319591991,
      "chosen_tail_successes": 0,
      "proposal_count": 57114
    },
    {
      "K_values": [],
      "base_bridge_index": 297,
      "base_trial": 7388743200,
      "chosen_tail_successes": 0,
      "proposal_count": 57133
    },
    {
      "K_values": [],
      "base_bridge_index": 298,
      "base_trial": 7419061651,
      "chosen_tail_successes": 0,
      "proposal_count": 56930
    },
    {
      "K_values": [],
      "base_bridge_index": 299,
      "base_trial": 7514107653,
      "chosen_tail_successes": 0,
      "proposal_count": 56953
    },
    {
      "K_values": [],
      "base_bridge_index": 300,
      "base_trial": 7514776900,
      "chosen_tail_successes": 0,
      "proposal_count": 57128
    },
    {
      "K_values": [],
      "base_bridge_index": 301,
      "base_trial": 7565202039,
      "chosen_tail_successes": 0,
      "proposal_count": 57048
    },
    {
      "K_values": [],
      "base_bridge_index": 302,
      "base_trial": 7569538220,
      "chosen_tail_successes": 0,
      "proposal_count": 56550
    },
    {
      "K_values": [],
      "base_bridge_index": 303,
      "base_trial": 7577570600,
      "chosen_tail_successes": 0,
      "proposal_count": 56816
    },
    {
      "K_values": [],
      "base_bridge_index": 304,
      "base_trial": 7577889555,
      "chosen_tail_successes": 0,
      "proposal_count": 57169
    },
    {
      "K_values": [],
      "base_bridge_index": 305,
      "base_trial": 7598642088,
      "chosen_tail_successes": 0,
      "proposal_count": 57614
    },
    {
      "K_values": [],
      "base_bridge_index": 306,
      "base_trial": 7636261821,
      "chosen_tail_successes": 0,
      "proposal_count": 56594
    },
    {
      "K_values": [],
      "base_bridge_index": 307,
      "base_trial": 7660942051,
      "chosen_tail_successes": 0,
      "proposal_count": 57245
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 308,
      "base_trial": 7765014619,
      "chosen_tail_successes": 1,
      "proposal_count": 56917
    },
    {
      "K_values": [],
      "base_bridge_index": 309,
      "base_trial": 7863015743,
      "chosen_tail_successes": 0,
      "proposal_count": 56828
    },
    {
      "K_values": [],
      "base_bridge_index": 310,
      "base_trial": 7872515046,
      "chosen_tail_successes": 0,
      "proposal_count": 57106
    },
    {
      "K_values": [],
      "base_bridge_index": 311,
      "base_trial": 7886060661,
      "chosen_tail_successes": 0,
      "proposal_count": 56885
    },
    {
      "K_values": [],
      "base_bridge_index": 312,
      "base_trial": 7886304525,
      "chosen_tail_successes": 0,
      "proposal_count": 56630
    },
    {
      "K_values": [],
      "base_bridge_index": 313,
      "base_trial": 7916657959,
      "chosen_tail_successes": 0,
      "proposal_count": 56903
    },
    {
      "K_values": [],
      "base_bridge_index": 314,
      "base_trial": 7958195565,
      "chosen_tail_successes": 0,
      "proposal_count": 56314
    },
    {
      "K_values": [],
      "base_bridge_index": 315,
      "base_trial": 7973861272,
      "chosen_tail_successes": 0,
      "proposal_count": 56868
    },
    {
      "K_values": [],
      "base_bridge_index": 316,
      "base_trial": 7995685758,
      "chosen_tail_successes": 0,
      "proposal_count": 57178
    },
    {
      "K_values": [],
      "base_bridge_index": 317,
      "base_trial": 8012397782,
      "chosen_tail_successes": 0,
      "proposal_count": 57004
    },
    {
      "K_values": [],
      "base_bridge_index": 318,
      "base_trial": 8023444845,
      "chosen_tail_successes": 0,
      "proposal_count": 57028
    },
    {
      "K_values": [],
      "base_bridge_index": 319,
      "base_trial": 8029404993,
      "chosen_tail_successes": 0,
      "proposal_count": 56872
    },
    {
      "K_values": [],
      "base_bridge_index": 320,
      "base_trial": 8049723774,
      "chosen_tail_successes": 0,
      "proposal_count": 56451
    },
    {
      "K_values": [],
      "base_bridge_index": 321,
      "base_trial": 8055926287,
      "chosen_tail_successes": 0,
      "proposal_count": 56952
    },
    {
      "K_values": [],
      "base_bridge_index": 322,
      "base_trial": 8071991647,
      "chosen_tail_successes": 0,
      "proposal_count": 57008
    },
    {
      "K_values": [],
      "base_bridge_index": 323,
      "base_trial": 8075250451,
      "chosen_tail_successes": 0,
      "proposal_count": 56806
    },
    {
      "K_values": [],
      "base_bridge_index": 324,
      "base_trial": 8081923034,
      "chosen_tail_successes": 0,
      "proposal_count": 56851
    },
    {
      "K_values": [],
      "base_bridge_index": 325,
      "base_trial": 8084343181,
      "chosen_tail_successes": 0,
      "proposal_count": 56832
    },
    {
      "K_values": [],
      "base_bridge_index": 326,
      "base_trial": 8087895317,
      "chosen_tail_successes": 0,
      "proposal_count": 56702
    },
    {
      "K_values": [],
      "base_bridge_index": 327,
      "base_trial": 8094633666,
      "chosen_tail_successes": 0,
      "proposal_count": 56887
    },
    {
      "K_values": [],
      "base_bridge_index": 328,
      "base_trial": 8121901899,
      "chosen_tail_successes": 0,
      "proposal_count": 57220
    },
    {
      "K_values": [],
      "base_bridge_index": 329,
      "base_trial": 8133956595,
      "chosen_tail_successes": 0,
      "proposal_count": 56956
    },
    {
      "K_values": [],
      "base_bridge_index": 330,
      "base_trial": 8147070679,
      "chosen_tail_successes": 0,
      "proposal_count": 56884
    },
    {
      "K_values": [],
      "base_bridge_index": 331,
      "base_trial": 8150117148,
      "chosen_tail_successes": 0,
      "proposal_count": 56807
    },
    {
      "K_values": [],
      "base_bridge_index": 332,
      "base_trial": 8154012733,
      "chosen_tail_successes": 0,
      "proposal_count": 56609
    },
    {
      "K_values": [],
      "base_bridge_index": 333,
      "base_trial": 8178142168,
      "chosen_tail_successes": 0,
      "proposal_count": 57361
    },
    {
      "K_values": [],
      "base_bridge_index": 334,
      "base_trial": 8224471169,
      "chosen_tail_successes": 0,
      "proposal_count": 56661
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 335,
      "base_trial": 8232241952,
      "chosen_tail_successes": 1,
      "proposal_count": 56725
    },
    {
      "K_values": [],
      "base_bridge_index": 336,
      "base_trial": 8239888670,
      "chosen_tail_successes": 0,
      "proposal_count": 56747
    },
    {
      "K_values": [],
      "base_bridge_index": 337,
      "base_trial": 8252591303,
      "chosen_tail_successes": 0,
      "proposal_count": 56926
    },
    {
      "K_values": [
        1
      ],
      "base_bridge_index": 338,
      "base_trial": 8256576231,
      "chosen_tail_successes": 1,
      "proposal_count": 57096
    },
    {
      "K_values": [],
      "base_bridge_index": 339,
      "base_trial": 8319317445,
      "chosen_tail_successes": 0,
      "proposal_count": 56749
    },
    {
      "K_values": [],
      "base_bridge_index": 340,
      "base_trial": 8323971416,
      "chosen_tail_successes": 0,
      "proposal_count": 57487
    },
    {
      "K_values": [],
      "base_bridge_index": 341,
      "base_trial": 8357396792,
      "chosen_tail_successes": 0,
      "proposal_count": 56716
    },
    {
      "K_values": [],
      "base_bridge_index": 342,
      "base_trial": 8421702749,
      "chosen_tail_successes": 0,
      "proposal_count": 57044
    },
    {
      "K_values": [],
      "base_bridge_index": 343,
      "base_trial": 8447840477,
      "chosen_tail_successes": 0,
      "proposal_count": 57038
    },
    {
      "K_values": [],
      "base_bridge_index": 344,
      "base_trial": 8508220377,
      "chosen_tail_successes": 0,
      "proposal_count": 57204
    },
    {
      "K_values": [],
      "base_bridge_index": 345,
      "base_trial": 8508338669,
      "chosen_tail_successes": 0,
      "proposal_count": 56577
    },
    {
      "K_values": [],
      "base_bridge_index": 346,
      "base_trial": 8519915286,
      "chosen_tail_successes": 0,
      "proposal_count": 56825
    },
    {
      "K_values": [],
      "base_bridge_index": 347,
      "base_trial": 8533069907,
      "chosen_tail_successes": 0,
      "proposal_count": 56883
    },
    {
      "K_values": [],
      "base_bridge_index": 348,
      "base_trial": 8533468635,
      "chosen_tail_successes": 0,
      "proposal_count": 56708
    },
    {
      "K_values": [],
      "base_bridge_index": 349,
      "base_trial": 8555120162,
      "chosen_tail_successes": 0,
      "proposal_count": 57240
    },
    {
      "K_values": [],
      "base_bridge_index": 350,
      "base_trial": 8577355228,
      "chosen_tail_successes": 0,
      "proposal_count": 56906
    }
  ],
  "pi_uniform_estimate": 3.1494140625e-09,
  "proposal": {
    "dimensions": [
      "E16_with_relations",
      "E17",
      "E18_with_relations",
      "E19"
    ],
    "domain_log2": [
      18,
      27,
      25,
      31
    ],
    "joint_domain_log2": 101,
    "likelihood_ratio": 7.450580596923828e-09,
    "likelihood_ratio_power2": -27
  },
  "reconstruction_pass": 20000000,
  "schema": "variant-tail-importance-v1",
  "seed": 2026100522,
  "stage_counts": [
    {
      "denominator": 20000000,
      "fail": 0,
      "marginal_pass": 20000000,
      "name": "A16_row",
      "pass": 20000000
    },
    {
      "denominator": 20000000,
      "fail": 0,
      "marginal_pass": 20000000,
      "name": "E16_row",
      "pass": 20000000
    },
    {
      "denominator": 20000000,
      "fail": 0,
      "marginal_pass": 20000000,
      "name": "E16_relations",
      "pass": 20000000
    },
    {
      "denominator": 20000000,
      "fail": 0,
      "marginal_pass": 20000000,
      "name": "E17_row",
      "pass": 20000000
    },
    {
      "denominator": 20000000,
      "fail": 0,
      "marginal_pass": 20000000,
      "name": "E18_row",
      "pass": 20000000
    },
    {
      "denominator": 20000000,
      "fail": 0,
      "marginal_pass": 20000000,
      "name": "E18_relations",
      "pass": 20000000
    },
    {
      "denominator": 20000000,
      "fail": 9998243,
      "marginal_pass": 10001757,
      "name": "E19_row",
      "pass": 10001757
    },
    {
      "denominator": 10001757,
      "fail": 5001384,
      "marginal_pass": 5000373,
      "name": "E20_row",
      "pass": 5000373
    },
    {
      "denominator": 5000373,
      "fail": 4922212,
      "marginal_pass": 312125,
      "name": "W20_row",
      "pass": 78161
    },
    {
      "denominator": 78161,
      "fail": 76864,
      "marginal_pass": 312831,
      "name": "W20_relations",
      "pass": 1297
    },
    {
      "denominator": 1297,
      "fail": 626,
      "marginal_pass": 10722,
      "name": "W22_row",
      "pass": 671
    },
    {
      "denominator": 671,
      "fail": 589,
      "marginal_pass": 2500200,
      "name": "W22_relations",
      "pass": 82
    },
    {
      "denominator": 82,
      "fail": 39,
      "marginal_pass": 177,
      "name": "C32_collision",
      "pass": 43
    }
  ],
  "sum_inverse_K": 43,
  "tail_count": 196608,
  "trials": 20000000
}
```

### Pinned replay of 43 repaired-cohort outcomes

Embedded JSON SHA-256: `db121f610e8f1534f285630f027d3d1100e76d0d9ae5ae771b27546cf0d61525`.

```json
{
  "K_distribution": {
    "1": 43
  },
  "all_bridge_stages_pass": true,
  "all_late_stages_pass": true,
  "all_pinned_C32_equal": true,
  "bases_sha256": "ccd81c657ad941374ce2c80584824322287bb9b0432d7fe3f4588e3fd6ba0198",
  "mapping_sha256": "47841a38e8ee86f0d6243b1233ea4ff78b2aa5f5057a93cdcbd7605e6bdfcfbf",
  "measurement_sha256": "9ed40d820d9f01c97b0fbbe0b36aaa40ebba92a1fdf05d4f6b909d150ec4ffde",
  "pinned_reference_sha256": "514fa8ab8a461e4a41080efa27b4ba2a3b499eeedf0a2d2346e6562835d040f5",
  "pinned_repository_commit": "8a0f02675cdcd58ebfc16119af02a094c3e1dd16",
  "recomputed_pi_uniform_estimate": 3.1494140625e-09,
  "recomputed_sum_inverse_K": 43.0,
  "replays": [
    {
      "K": 1,
      "base_bridge_index": 77,
      "cv": "103f95c0fcabeae40224b5a7e08d0b673a5c699593f0f8b9edcfa214e91b1e89",
      "pinned_C32_output": "08ff365cb855d3dc3b508c00a6ca0cdd8f9a218b63206905ba61b42fc50af09a",
      "tail_index": 175241,
      "trial": 168855,
      "variant_id": 706362
    },
    {
      "K": 1,
      "base_bridge_index": 77,
      "cv": "103f95c0fcabeae40224b5a7e08d0b67a9960a9f9e2e9abaf786c8992d5cc05a",
      "pinned_C32_output": "c2328c7581e73f8016a82ea0c91d74a07c5b5bfbc080e43128129f36948751dc",
      "tail_index": 131167,
      "trial": 646423,
      "variant_id": 706362
    },
    {
      "K": 1,
      "base_bridge_index": 157,
      "cv": "063ff67f77c701496d09beef3f7affc842d763cda66979ff4514cb5a31b1a154",
      "pinned_C32_output": "2c07cb39bb62a4874e02d6868d1715a9f1c12443329177b0483c9ffd39e488e3",
      "tail_index": 194172,
      "trial": 758756,
      "variant_id": 706362
    },
    {
      "K": 1,
      "base_bridge_index": 199,
      "cv": "3c28e2d10880ef5abdb18fad2a2970a6fd5bc6f09e380eef33fdc09bc2784ffa",
      "pinned_C32_output": "7827347b1a57f9a187041361b65710026a36eec3afe21d61c75c78da7bbf1eed",
      "tail_index": 53838,
      "trial": 1155761,
      "variant_id": 804666
    },
    {
      "K": 1,
      "base_bridge_index": 84,
      "cv": "b9bd2d869ad0ee24facb9f96790ad7e11288ac3ef4be77791d11a4ca0947298f",
      "pinned_C32_output": "9e373a57e9c154a01a8e148f689073e38474bee2f2dbadca3544b797f2196e31",
      "tail_index": 94161,
      "trial": 1837215,
      "variant_id": 640554
    },
    {
      "K": 1,
      "base_bridge_index": 234,
      "cv": "304004cb20c3e54b109de45a4fff6d5451d6bafdedb28016dc734306d98aec16",
      "pinned_C32_output": "124ae90c4512b88502689e3182472d53bdfb9d9908d1bc155e4ef6857edc83ea",
      "tail_index": 169588,
      "trial": 1985278,
      "variant_id": 706362
    },
    {
      "K": 1,
      "base_bridge_index": 101,
      "cv": "ca192b05ec732c6b721e02dc4fca0e6242a34d874dff98d92a42fd2d806b3736",
      "pinned_C32_output": "b0dbf3fa04fc9e6a64b96eaca591aa0c7c616b4d8db22840ec1f45638039f247",
      "tail_index": 145246,
      "trial": 2644683,
      "variant_id": 640554
    },
    {
      "K": 1,
      "base_bridge_index": 185,
      "cv": "0fc014c6d52631d8a91f6aef5dbb10953347358b99b0eeae536d7bedab9132d3",
      "pinned_C32_output": "840858f033d30a923900ddc14bde759541f5511e8deddae3613d76913235fb05",
      "tail_index": 97109,
      "trial": 2738453,
      "variant_id": 706362
    },
    {
      "K": 1,
      "base_bridge_index": 144,
      "cv": "df570fd6bae7003d3494985bd9d5b2a773b3c4b36c115f17bf721b255ba36139",
      "pinned_C32_output": "af7950b69b49fd1d73d5e9bbf265a4d38e7cd2bb702911d195e3044231053e0c",
      "tail_index": 100698,
      "trial": 3527542,
      "variant_id": 59306
    },
    {
      "K": 1,
      "base_bridge_index": 122,
      "cv": "44e2820a5691c36309ef7b5fd215e34b02bf143d1ce78cad338ab2e567673497",
      "pinned_C32_output": "197876e86b88e313a8abd1bc4c93900a238a211aa86aecd401bcfab2a5d5c72e",
      "tail_index": 79889,
      "trial": 4001498,
      "variant_id": 287670
    },
    {
      "K": 1,
      "base_bridge_index": 273,
      "cv": "026005807264ae29804a9767bd699ec569abc3888b875d9f21801f597830157d",
      "pinned_C32_output": "f1bb43157fa614a06a7bc96b914bb0a136369635416ee58cb2024d7020c64daf",
      "tail_index": 76083,
      "trial": 4186320,
      "variant_id": 706362
    },
    {
      "K": 1,
      "base_bridge_index": 294,
      "cv": "c139a60af28dcc20a2be8cc34b5750a60a1224588068fc72efb1411346342ada",
      "pinned_C32_output": "ac2b81910725e5ec72e1be1a93f932d2291f8b453ca6829a56ac380764707673",
      "tail_index": 146245,
      "trial": 5003505,
      "variant_id": 640554
    },
    {
      "K": 1,
      "base_bridge_index": 15,
      "cv": "0cf855a86df997de16b06bbac66c3bddf87f03d70d9b23e86421e9700ff1e646",
      "pinned_C32_output": "0d9071929f75435b935e363fffafe5fff71385ff9aeec4839cee279f620f2418",
      "tail_index": 62285,
      "trial": 5330699,
      "variant_id": 26274
    },
    {
      "K": 1,
      "base_bridge_index": 82,
      "cv": "3b07452b4bb9af49a8077b2d43d51c50758ece29d148a20d2c1587e04c9dc59d",
      "pinned_C32_output": "345dc50d343c799a3cf0c1ef8fd977ab81d22da07220a2c0c94bbcb2b720e710",
      "tail_index": 39822,
      "trial": 5475736,
      "variant_id": 804666
    },
    {
      "K": 1,
      "base_bridge_index": 165,
      "cv": "f85b3d410270cb7418dbcb704b2a73ce9482cd4605f81cf79093059c3a73e3ec",
      "pinned_C32_output": "8b217b8ca0914201c110897ea7512b3e72c0ef2489e1a68d51f1a7cfbfaf78b2",
      "tail_index": 185944,
      "trial": 5511870,
      "variant_id": 640554
    },
    {
      "K": 1,
      "base_bridge_index": 166,
      "cv": "3a07589153e95be8cf48e9a8e330e0666f035c6bec6a9e34a13ba8a8c0af1d5d",
      "pinned_C32_output": "61f6ad653142de76e5183b5dabb02810be70e8b0fd2367cea335cea2ad65880b",
      "tail_index": 111842,
      "trial": 6028688,
      "variant_id": 804666
    },
    {
      "K": 1,
      "base_bridge_index": 54,
      "cv": "ee41658728aec3ab715926c8bbcffab4af3c8b15f362f02dc592e1bfbc1b3c9f",
      "pinned_C32_output": "118537e593e0172a610372f0f1a4a64a50dbba2233cfe2c339e49cc2b3e7f66d",
      "tail_index": 177441,
      "trial": 6192636,
      "variant_id": 706362
    },
    {
      "K": 1,
      "base_bridge_index": 110,
      "cv": "7bdb1c45d2394fcde48989c84876840525428643c04eadb301807ad0c46a091a",
      "pinned_C32_output": "0cb020fbeb3057a12bac790ffc1603ef52255939043951a4a12a6cb1b0d6f72a",
      "tail_index": 112783,
      "trial": 6473658,
      "variant_id": 640554
    },
    {
      "K": 1,
      "base_bridge_index": 275,
      "cv": "722963d41bd647477ab10954c97978156a3a0b6f4199f37f7ce68fbfa27dcb28",
      "pinned_C32_output": "b6f24b0b62651ac2bf37ad685a4444e4ed836369024a957229a8e7acf389c5a0",
      "tail_index": 144854,
      "trial": 6750235,
      "variant_id": 804666
    },
    {
      "K": 1,
      "base_bridge_index": 243,
      "cv": "a39b1b8608a58e074be3458a916bbc52022bc441a13a200ddc9bb346db2af0e3",
      "pinned_C32_output": "3e5eb8fc7215259f868c610c92d992a6d55cd9bb8bf28df931550f385171ca33",
      "tail_index": 44191,
      "trial": 6820399,
      "variant_id": 640554
    },
    {
      "K": 1,
      "base_bridge_index": 117,
      "cv": "0b36eac10e6fab647d19ddd9e03923343030ec18bc4e30ca2f55099fb9282acf",
      "pinned_C32_output": "8d8b6be91be75803bae05679340cc6899d4ea52f3e97e856589b2e322c20788c",
      "tail_index": 128697,
      "trial": 7201249,
      "variant_id": 59306
    },
    {
      "K": 1,
      "base_bridge_index": 108,
      "cv": "3c7864a7b5e07a9f44821af18562bc3ce799ae73766cfd8a69b8affd65c9f22c",
      "pinned_C32_output": "68bd94b2147d870318e947ad3ff9a64b236ac5560f8d37c8394559afa709307a",
      "tail_index": 174660,
      "trial": 7526055,
      "variant_id": 26274
    },
    {
      "K": 1,
      "base_bridge_index": 201,
      "cv": "e28edaf5861734fa4f01ca94bda1b218c5c5ff8c0c469f07abcb077397a277e3",
      "pinned_C32_output": "f873dff5a46e9a6e627a556de2772cfa0df3445fea641a5b7cf1097c5e6fdc10",
      "tail_index": 54648,
      "trial": 8021723,
      "variant_id": 90810
    },
    {
      "K": 1,
      "base_bridge_index": 258,
      "cv": "a23bad4978c219a97396adffb674cf25d22f7bcc789dbb323601b1ba78ce2b9a",
      "pinned_C32_output": "c8041eb8941b1c43d03222509432165cf31ffa4edc43273fa52484ae6b4bc18a",
      "tail_index": 37434,
      "trial": 8791366,
      "variant_id": 640554
    },
    {
      "K": 1,
      "base_bridge_index": 78,
      "cv": "bb5d3a465de6731503b5f79993135607c58a14bd8baa53814973832a0c0b0b3a",
      "pinned_C32_output": "c1fd15670eefc1d2197f74bdb88a1ebb91ba67ba5da5cbbd3aa0a6110d6842a9",
      "tail_index": 13196,
      "trial": 8868188,
      "variant_id": 640554
    },
    {
      "K": 1,
      "base_bridge_index": 338,
      "cv": "f0b4f1941a650e886c1f57f05a00e1e1fd6c7ab476323ace21f80b3902c2135b",
      "pinned_C32_output": "754736f7b240f6d83f0698a467a9dcb71c1b95899e442967ee59134bf595a8cd",
      "tail_index": 122576,
      "trial": 10075424,
      "variant_id": 59306
    },
    {
      "K": 1,
      "base_bridge_index": 291,
      "cv": "18b79fd833931fcb23f29733e361195ae3b511fd236468642489a963594d6f24",
      "pinned_C32_output": "f4b0470679ccc88e7b0cd2ed95df95d745bdf7f511588b34f18df288a7d2eae6",
      "tail_index": 80998,
      "trial": 10128812,
      "variant_id": 59306
    },
    {
      "K": 1,
      "base_bridge_index": 190,
      "cv": "40c18a8cec1dacbe536a8dc93865b3814e03816b3476c753abbb2cfb0dc2d123",
      "pinned_C32_output": "66e6a322e5eac932371fea24d24183b479f1901dcfe5424944b39fc873615c02",
      "tail_index": 41124,
      "trial": 10470706,
      "variant_id": 706362
    },
    {
      "K": 1,
      "base_bridge_index": 286,
      "cv": "d2f7fec4b2ca7b1b5b7aed744acd568113aa0279bbbb68791441c6a3fc63b836",
      "pinned_C32_output": "e421d8e07a27cd6068cb8ede134d01261d88ad7463ab48bdbbc4e41c7daf2a34",
      "tail_index": 59989,
      "trial": 10721585,
      "variant_id": 26274
    },
    {
      "K": 1,
      "base_bridge_index": 167,
      "cv": "47c2048beff1f23c84502500db78ebe0321cc09c4dbbdb794940884f9c112ff5",
      "pinned_C32_output": "ecd5ce55e6601b6bee9924523a75522aa35000fa89a4de7f7178785bbb7f4222",
      "tail_index": 36864,
      "trial": 10799337,
      "variant_id": 706362
    },
    {
      "K": 1,
      "base_bridge_index": 61,
      "cv": "18b70f93b8d826883d9722426b3f986d0743a0bdc0b1379b61d3899bf7280422",
      "pinned_C32_output": "fbd42436fa4b8f9b8b182b05525ea25b8a033314cf3201120f825f4a545a5e60",
      "tail_index": 48587,
      "trial": 11447503,
      "variant_id": 59306
    },
    {
      "K": 1,
      "base_bridge_index": 66,
      "cv": "eab87aacbe09501dd105f11548e6763be913d9d7a768dd7e48f5075cc8bc89bf",
      "pinned_C32_output": "6ee3bf887475ceba03d6de34624ae1658edb4830c848acaa29c0f64f255c0f09",
      "tail_index": 19538,
      "trial": 11495810,
      "variant_id": 919338
    },
    {
      "K": 1,
      "base_bridge_index": 55,
      "cv": "227660c8cc5b3d59becdcc2785a6728597d33396ee7a78722251ffd8cef11025",
      "pinned_C32_output": "a047fa02afe98815c206c3ef08a5041db8852c587a4fd53b85c3f2d4453b18cf",
      "tail_index": 54117,
      "trial": 12668889,
      "variant_id": 26274
    },
    {
      "K": 1,
      "base_bridge_index": 110,
      "cv": "7bdb1c45d2394fcde48989c848768405a68d48d75d35343be113fd8978e9cfcf",
      "pinned_C32_output": "95346e5d7d103c48fc626d9f0f91c40f752afdfeb3048c27f23317a2da77b48a",
      "tail_index": 110156,
      "trial": 12706422,
      "variant_id": 640554
    },
    {
      "K": 1,
      "base_bridge_index": 3,
      "cv": "d259b344bf60bddeb8f265738786f7021d8f10b842606c1eac2234c78ac249c6",
      "pinned_C32_output": "5edbfaad5761ccc7e0327e3cc32da239651882d5cc1a20b9ca0f4cbd17dc9160",
      "tail_index": 42457,
      "trial": 13508868,
      "variant_id": 508458
    },
    {
      "K": 1,
      "base_bridge_index": 25,
      "cv": "d0b771d8ed370d3106e82d7d2ce3f111cf172e6635b55793509c6c8978a3da85",
      "pinned_C32_output": "f5ccd8167d396a26abc382a2e96df75faeed16e601ec98a78c950e3686309ebe",
      "tail_index": 44785,
      "trial": 15963764,
      "variant_id": 59306
    },
    {
      "K": 1,
      "base_bridge_index": 7,
      "cv": "8b25c42918747f0eefeea306fd93b95923afe473c22e4c7654515449c77a53bc",
      "pinned_C32_output": "c7eb4a7f602732f87fb1601b269b213f83e2aa2b9f7e1b4a65434d11c234afa4",
      "tail_index": 153142,
      "trial": 16316796,
      "variant_id": 287670
    },
    {
      "K": 1,
      "base_bridge_index": 50,
      "cv": "8b1b1c43370ca463698858e1a8fcc7cedb53b8114bc92cf176a6afe62657115c",
      "pinned_C32_output": "47a90f4f6fbaa4b6e5cf1d5ed5a481b79fef7d0dcaf6af0d068e1a5ec118e7d1",
      "tail_index": 125193,
      "trial": 17430311,
      "variant_id": 640554
    },
    {
      "K": 1,
      "base_bridge_index": 335,
      "cv": "fcb989c194d5dba65b12461607858632f6273ed9530c93e4eea8e087a8bb3c45",
      "pinned_C32_output": "6c036a2db99fe1d3ed9b6df15411dc3cdc3079f9905c6e2efda18f847aee6632",
      "tail_index": 33336,
      "trial": 17457026,
      "variant_id": 59306
    },
    {
      "K": 1,
      "base_bridge_index": 308,
      "cv": "d4591f10b810a5cfdf0a11255e70437fb55982deeaacf8799ebf558eef6f9610",
      "pinned_C32_output": "be1e53e242ff16587069214bd03cf3bb340a92feb09810f552982450e7583276",
      "tail_index": 32958,
      "trial": 18632844,
      "variant_id": 508458
    },
    {
      "K": 1,
      "base_bridge_index": 96,
      "cv": "d10ee5e23b184b3ac608c2f52556d7c67a6b60d2a985fd7ba1d6c372a0ee2b72",
      "pinned_C32_output": "2a9d3695bf2968b026420b25535a32918774ae87d07b1a38e2cca5c48e2df450",
      "tail_index": 194562,
      "trial": 19020564,
      "variant_id": 90810
    },
    {
      "K": 1,
      "base_bridge_index": 262,
      "cv": "cad900150c8f3af26013b0413d8e5b6b92fdc68a0d424031ab95b934589c19ae",
      "pinned_C32_output": "ca43a2214b7d773044117fd599ffec1dc1637b7c4ad524abd0f5e93c764c3fd8",
      "tail_index": 91093,
      "trial": 19381946,
      "variant_id": 508458
    },
    {
      "K": 1,
      "base_bridge_index": 273,
      "cv": "026005807264ae29804a9767bd699ec5b61325996ac5ebc8d7119718669aff52",
      "pinned_C32_output": "0c828993374908d49e5faa13bea7106bd951114ec7a748e651b4af0597090c43",
      "tail_index": 143826,
      "trial": 19648636,
      "variant_id": 706362
    }
  ],
  "schema": "variant-importance-validation-v1",
  "states_sha256": "cc96a713059ceb66f2813116a482f7bc77024d89ebf8411f89ee58ba0ee7d3ab",
  "successes_replayed": 43
}
```

### Finite ledgers

Embedded JSON SHA-256: `05a7374709c7b35453b8eddfc76becb5d4ffd93dc459c066a671c480f8486bb4`.

```json
{
  "common": {
    "B": 536870912,
    "L": 196608,
    "P": 36028797018963968,
    "advice_bytes": 1048576,
    "operation_ceilings": {
      "a": 256,
      "b": 2048,
      "c": 8192,
      "d_tail": 512
    },
    "peak_memory_bytes": 1099511627776,
    "pi_premise": 9.313225746154785e-10,
    "word_operation_divisor": 2224
  },
  "cost_model": "collision-frontier-v5",
  "ledgers": {
    "fixed_table3_slice": {
      "B": 536870912,
      "H": 1153132610839379974,
      "P": 36028797018963968,
      "T_decimal": 1.323969698681795e+18,
      "T_exact": {
        "denominator": 2224,
        "numerator": 2944508609868312097824
      },
      "W": 299813638791355170816,
      "W_terms": {
        "aN": 295147905179352825856,
        "bR": 4611686018427387904,
        "cB": 4398046511104,
        "dBL": 54043195528445952
      },
      "conservative_success_lower_bound_decimal": "0.39346934028736302368252166450710133003152296208240131575182505503527027415114256",
      "delta": 1.0,
      "expected_bridges": 1073741824,
      "log2_T": 60.19957581194412,
      "log2_T_rounded_up_0_001": 60.2,
      "premises": {
        "N": 1152921504606846976,
        "R": 2251799813685248,
        "mean_load": 0.0009765625,
        "mean_load_power2": -10,
        "q": 9.313225746154785e-10,
        "q_power2": -30,
        "record_cap": 4
      },
      "record_budget_gap": 1125899906842624,
      "record_overflow_bound": 3.552713678800501e-15,
      "record_overflow_power2": -48,
      "record_variance_bound": 4503599627370496,
      "shortfall_bound": "exp(-134217728)",
      "shortfall_bound_used_for_decimal": "exp(-2^27) < 2^-100",
      "shortfall_exponent": 134217728.0,
      "success_exceeds_0_39": true,
      "success_lower_bound_symbolic": "1 - exp(-1/2) - exp(-134217728) - 2^-48",
      "tail_miss_bound": "exp(-1/2)"
    },
    "repaired_65_variant": {
      "B": 536870912,
      "H": 36239903251496966,
      "P": 36028797018963968,
      "T_decimal": 7.66994018814021e+16,
      "T_exact": {
        "denominator": 2224,
        "numerator": 170579469784238273568
      },
      "W": 9853880382733156352,
      "W_terms": {
        "aN": 9223372036854775808,
        "bR": 576460752303423488,
        "cB": 4398046511104,
        "dBL": 54043195528445952
      },
      "conservative_success_lower_bound_decimal": "0.39346934028725288955847884897829130577004835270740131575182505503527027415114256",
      "delta": 1.0,
      "expected_bridges": 1073741824,
      "log2_T": 56.09006484552054,
      "log2_T_rounded_up_0_001": 56.091,
      "premises": {
        "N": 36028797018963968,
        "R": 281474976710656,
        "mean_load": 0.00390625,
        "mean_load_power2": -8,
        "q": 2.9802322387695312e-08,
        "q_power2": -25,
        "record_cap": 16
      },
      "record_budget_gap": 140737488355328,
      "record_overflow_bound": 1.1368683772161603e-13,
      "record_overflow_power2": -43,
      "record_variance_bound": 2251799813685248,
      "shortfall_bound": "exp(-134217728)",
      "shortfall_bound_used_for_decimal": "exp(-2^27) < 2^-100",
      "shortfall_exponent": 134217728.0,
      "success_exceeds_0_39": true,
      "success_lower_bound_symbolic": "1 - exp(-1/2) - exp(-134217728) - 2^-43",
      "tail_miss_bound": "exp(-1/2)"
    },
    "repaired_65_variant_conservative": {
      "B": 536870912,
      "H": 72268700270460934,
      "P": 36028797018963968,
      "T_decimal": 1.1713459853577893e+17,
      "T_exact": {
        "denominator": 2224,
        "numerator": 260507347143572337696
      },
      "W": 19653713171891355648,
      "W_terms": {
        "aN": 18446744073709551616,
        "bR": 1152921504606846976,
        "cB": 4398046511104,
        "dBL": 54043195528445952
      },
      "conservative_success_lower_bound_decimal": "0.39346934028730973297733965699316099571145460270740131575182505503527027415114256",
      "delta": 1.0,
      "expected_bridges": 1073741824,
      "log2_T": 56.70094488673336,
      "log2_T_rounded_up_0_001": 56.701,
      "premises": {
        "N": 72057594037927936,
        "R": 562949953421312,
        "mean_load": 0.00390625,
        "mean_load_power2": -8,
        "q": 1.4901161193847656e-08,
        "q_power2": -26,
        "record_cap": 16
      },
      "record_budget_gap": 281474976710656,
      "record_overflow_bound": 5.684341886080802e-14,
      "record_overflow_power2": -44,
      "record_variance_bound": 4503599627370496,
      "shortfall_bound": "exp(-134217728)",
      "shortfall_bound_used_for_decimal": "exp(-2^27) < 2^-100",
      "shortfall_exponent": 134217728.0,
      "success_exceeds_0_39": true,
      "success_lower_bound_symbolic": "1 - exp(-1/2) - exp(-134217728) - 2^-44",
      "tail_miss_bound": "exp(-1/2)"
    }
  },
  "operation_ceiling_audit": {
    "a_first_block_wrapper_and_index_miss": {
      "ceiling": 256,
      "items": {
        "C32_call_wrapper_input_output_and_dispatch": 48,
        "direct_key_index_extraction_address_load_and_empty_check": 32,
        "spare": 102,
        "split_mask_and_store_sixteen_32_bit_block_words": 48,
        "trial_cap_counters_and_control": 24,
        "two_uniform_256_bit_random_words": 2
      },
      "note": "C32 internals are charged once in H. A direct-address 2^32 span index with 16-byte entries is at most 2^36 bytes and fits the declared 2^40-byte peak; this avoids an unsupported lookup-time maximum."
    },
    "b_examined_record": {
      "ceiling": 2048,
      "items": {
        "W0_W6_row_relation_and_equality_tests": 256,
        "canonical_scan_counters_and_control": 128,
        "derive_and_mask_two_branch_W0_through_W8": 640,
        "reconstruct_and_mask_two_branch_A_E_state": 384,
        "record_variant_and_pointer_loads": 64,
        "spare": 576
      }
    },
    "c_accepted_bridge_setup": {
      "ceiling": 8192,
      "items": {
        "at_most_once_final_message_build_compare_and_serialization": 4096,
        "copy_fixed_and_variant_high_prefix_state": 256,
        "prepare_two_W0_through_W13_prefixes": 512,
        "spare": 3072,
        "tail_list_state_and_accepted_bridge_bookkeeping": 256
      },
      "note": "The final ordinary work occurs at most once and is covered by one bridge allowance because B>=1. Its six C32 calls are separate in H."
    },
    "d_each_tail_outside_two_C32_calls": {
      "ceiling": 512,
      "items": {
        "candidate_bookkeeping_and_control": 32,
        "compare_two_eight_word_outputs": 64,
        "spare": 192,
        "tail_loads_loop_counter_and_cap_check": 32,
        "two_C32_call_wrappers_input_output_and_dispatch": 160,
        "write_tail_words_into_two_prepared_blocks": 32
      },
      "note": "The two C32 internals are charged in H, not again here. The attack needs only exact output equality; diagnostic differential-stage tests are not online work."
    }
  },
  "schema": "sha256-r32-finite-ledger-audit-v1"
}
```

### Finite-ledger disposable control

Embedded JSON SHA-256: `be59de01c13802b8820277d6316b4c446fbd3ec6007aeff31c53bf8b8c1dca24`.

```json
{
  "controls": [
    {
      "name": "baseline",
      "observed": "pass",
      "returncode": 0
    },
    {
      "expected": "repaired_65_variant_H",
      "mutation": "repaired H += 1",
      "name": "mutated_repaired_H_plus_one",
      "observed": "named_failure",
      "returncode": 1
    }
  ],
  "schema": "finite-ledger-mutation-control-v1"
}
```
