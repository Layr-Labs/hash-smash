# SHA-256 r32 ordinary-collision search

## Claim and target

This package specifies a finite-budget, classical ordinary-collision search for
sha256-r32-prefix-v1. Define C32 once as the profile's 32-round SHA-256
compression, including feed-forward. Every padded block uses round indices 0
through 31. The complete target uses the standard IV once, FIPS 180-4 padding,
and all 256 digest bits.

The algorithm searches messages B0 || M1 and B0 || M1-prime. B0 is one 64-byte
block shared by both messages; M1 and M1-prime are distinct 64-byte second
blocks. Each message has length 128 bytes before padding and therefore receives
the same third padding block. A returned pair is checked as two complete
messages from the standard IV, with equal full digests. No free-start,
compression-only, near-collision, or truncated-output result is claimed. No
complete r32 collision was found in the bounded participant computations, and
no collision certificate is supplied.

The construction adapts the practical 35-step SHA-256 result of Li, Liu, Wang,
and Shi, ePrint 2026/1080, Section 4, Figure 6, and Table 3. Its Table 3 pair
is not an r32 collision when started from the standard IV. The package searches
a new first block under C32.

## Evidence and provenance

| Evidence class | Quantity or input | Package record | What it establishes |
|---|---|---|---|
| Paper-reported | Table 3 blocks and the 35-step construction; Step 1 work about 2^34.3; 45 residual conditions against 2^17.585 W14/W15 choices; 378 GB historical server capacity | Cited-source transcription below; Li et al., Section 4, pp. 302–305, Figure 6, and Table 3, p. 307 | Reported source inputs, not this candidate's r32 rate or resource upper bounds |
| Exact participant derivation | C35 starting chaining value; fixed A/E state words; Figure 6 witness checks; finite prefix table, key multiplicity, and tail count | Embedded Table 3 source-audit program/output and primary sample program/output | Results recomputed for the transcribed inputs and pinned reference implementation |
| Sampled participant observations | 127 accepts in 2^22 conditional uniform-CV proposals; 0 equalities in 4,096 sampled C32 tail checks | Embedded seeded sample inputs and raw JSON output | Reproducible observations for the stated stream only; not an organizer report or a full-scale probability measurement |
| Extrapolated premises | C32 bridge density, accepted-bridge tail yield, two search-cost bounds, and full peak memory | claim.json heuristic IDs and the unresolved-premise list below | Five unresolved premises retained for exploratory evaluation |

The source snapshot, target-profile snapshot, Table 3 words, Figure 6 condition
transcription, programs, and raw JSON outputs are embedded as named appendix
blocks at the end of this proof. Their hashes are printed by the replay
programs. The compression-source and profile hashes match challenge commit
fc56c3fa38ac40043d8291649c78148bc4872995. The source-audit program derives the
fixed A/E states from the transcribed Table 3 blocks and checks the listed
Figure 6 rows and relations on the witness. Candidate intake computes a content
hash over claim.json and this proof; the participant-side program/output hashes
bind the finite measurements to their code and inputs. These are content
commitments, not organizer execution provenance.

## Published starting point and r32 boundary

The exact Table 3 input words and source citation are recorded in
verification/sha256-r32-paper-inputs.json and sources/li-et-al-source-data.md.
The three blocks are M0, M1, and M1-prime. Independent replay in
verification/sha256-r32-source-audit.py gives:

~~~text
C35(IV, M0) = c4369610 c91f70a7 87e430e6 a5e58128
             d29cb97b 9ab268d1 8788f401 629f6cb2
C32(IV, M0) = 6a9f7255 39f4063e a684176a b5efb469
             57ccf218 f7ab3896 562fcb55 c67d5c37
~~~

From the C35 chaining value, M1 and M1-prime have equal second-block C32 and
C35 chaining values, and their complete padded messages collide at 35 rounds.
From the standard-IV C32 chaining value, the complete messages do not collide.
The full trace therefore supports the stated r32 boundary and the need to
search a fresh first block. The blocks differ at W4, so the source pair's
messages are distinct.

Replaying M1 and M1-prime from C35(IV,M0) through the relevant rounds derives:

~~~text
A1..A13 =
66e7ba7c 5ff9d9f8 9123b13f b8560dbb 677e1e2a 9bcf7bbe f8677ad6
4a299906 44d24ab4 39781650 6c206d58 35c5c2b8 0508c8f0
A1'..A13' =
66e7ba7c 5ff9d9f8 9123b13f 98560dbb 633b16ba 9bcf7bbe f8677ad6
4a299906 44f24ab5 39781650 6422edc8 574542b8 0508c8f0
E5..E13 =
58f38fac b95f2294 87431160 11cae594 d504bf23 7f27d24c bf893f69
2300f189 fcc08ef5
E5'..E13' =
5caf87bc a94f0a01 a7421160 f1cae594 d0e1b7b4 bf27d74c b78bbfd9
3fffd0f9 bf81c0f4
W9..W13  = 5100da8a 0912e57b a96b2054 45f2222c 4d12f88a
W9'..W13'= 5100da8a 0912e57b a96b2054 41b22a2c 6d12f88a
~~~

These values are derived from the transcribed Table 3 blocks by the included
source-audit program. It also checks each row and bit relation in the packaged
Figure 6 transcription on that witness, including the three inequality
readings A14[18,8] != A14[6,17], A15[29] != A6[29], and
W20[4,31] != W20[6,22]. The audit output records all listed checks as passing.
This is a check of the transcribed input and replay; it is not independent
authentication of the source transcription.

## Fixed prefix table

Bit 0 is least significant; the leftmost row character denotes bit 31. The
symbols =, 0, 1, u, and n mean equal free bits, fixed 0, fixed 1, 0-to-1,
and 1-to-0. The machine-readable rows and relations are in
verification/figure6-conditions.json.

Enumerate admissible path-one W8 values. For each, derive E4 and A0 in both
branches from the round equations and retain those passing the E4 row,
E4[10] != E4[15], and A0=A0-prime. For each retained W8 pair, enumerate
admissible W7 values, derive E3 and A(-1) in both branches, then retain those
passing the E3 row and A(-1)=A(-1)-prime. Sort by key and record tuple. All
arithmetic is modulo 2^32.

The exact enumeration, conditional on the transcription, gives:

| Quantity | Result |
|---|---:|
| Admissible W8 values | 1,048,576 |
| W8 survivors after E4/A0 checks | 44 |
| Admissible W7 values per survivor | 524,288 |
| Table records | 593,920 |
| Distinct A(-1) keys | 408,576 |
| Maximum records per key | 4 |
| Packed table bytes | 14,254,080 = 593,920 × 24 |
| SHA-256 of sorted packed table | 3cd961f8e0efe18027ec7192b4f0fa9f449659fdae14a5969fe3f6b821c8ebc7 |

The six packed words per record are A(-1), W7, W8, E3, E4, and A0. Primed
values follow from the fixed differential path. The regenerated table contains
both the Table 3 record (c4369610, db9ec665, 6ec17218, a70d4308, 2932d839,
ac311f10) and the separate C32 bridge regression record
(f3b8f7ae, ab9c6465, 6e417236, d68fa526, 29b2d81b, acb11ef2). The latter is a
synthetic chaining-value regression input; no first-block preimage is claimed.

## Matching a first block and making a collision

For each fresh 64-byte B0, compute CV=C32(IV,B0) and interpret its eight words
as (A(-1), A(-2), A(-3), A(-4), E(-1), E(-2), E(-3), E(-4)). Direct-index the
table by A(-1); at most four records can match. Scan them in sorted order and
select the first record whose recovered W0..W6 pass the W4, W5, and W6 rows and
relations. If none pass, this B0 is rejected.

For an accepted bridge, the record determines both branches' W7, W8, E3, E4,
and A0; W9..W13 are fixed. Recover W0..W6 by inverting the E updates and
replay both 14-round prefixes from CV. The code checks the replayed state
against the derived state before sweeping the tail set.

The tail set comes from the E14 and E15 rows and the A14/A15 conditions in the
packaged Figure 6 transcription. There are 2^8 E14 row values; 12 W14 values
survive the W14/A14 checks. For each, there are 2^15 E15 row values and 16,384
W15 pairs survive the W15/A15 checks, giving exactly 12 × 16,384 = 196,608
(W14,W15) tails. The list commitment from the exact C32 regression and each of
the 16 sampled accepted bridges is
ec59bb6beaab8473f3ce54e8a8a121f043ca2097e7e952e7946dff35975b8b1d.

For every tail, form both 64-byte second blocks and compare their complete C32
chaining values. Charge four C32 calls per tail: both second blocks and both
common padding blocks, even when the second-block states differ. If the full
outputs agree, retain the first candidate pair. Since W4 differs, the messages
are distinct. After the fixed search budget, independently hash each retained
128-byte message from the standard IV through all three padded blocks and
return a pair only when the two complete 256-bit digests agree.

The full finite procedure is:

~~~text
Preprocess:
  Obtain the fixed 35-step starting point and characteristic.
  Derive the table constants by replaying the Table 3 source input.
  Enumerate and sort the prefix table; build a 2^32-entry four-byte index.
  Enumerate the fixed 196,608-element tail list.

Search:
  accepted = 0; saved_pair = none
  For t = 0,...,2^65-1:
    Draw two independent uniform 256-bit words and serialize B0.
    CV = C32(IV, B0); scan all table records for CV.A(-1), at most four.
    If no record passes the exact bridge filter: continue.
    If accepted < 2^33:
      accepted += 1
      Recover and replay both prefixes through round 13.
      Sweep every tail in list order; test both complete second-block C32 values.
      When equal, test both common padding blocks; save the first distinct pair.
  If saved_pair is absent: output failure.
  Independently hash saved_pair as two complete messages from the standard IV.
  Output it only if the full 256-bit digests agree and the messages differ.
~~~

The trial loop has a fixed budget. It continues after the first witness if one is
found and performs no more than 2^33 complete tail sweeps. No record examination
cap is used for success: the exact measured table multiplicity four is charged
as a worst case for every first-block trial.

## The five unresolved premises and the conditional formulas

The claim preserves these five premises as unresolved. They are stated here in
the same scope as their claim.json heuristic IDs.

1. fixed-slice-c32-bridge-density: a fresh uniform 64-byte B0 produces an
   accepted C32(IV,B0) bridge with probability q at least 2^-31.
2. fixed-slice-average-tail-yield: over the accepted-bridge distribution, the
   average probability that a complete deterministic 196,608-tail sweep finds
   a second-block equality is pi at least 2^-34.
3. starting-point-search-resource-bound: the Step 1 search for the fixed
   starting point fits within 2^35 target-compression equivalents, including
   the unresolved conversion from the paper's generic 2^34.3 work figure.
4. characteristic-search-resource-bound: the four-stage characteristic search
   fits within the remaining aggregate preprocessing ceiling. The paper gives
   no numeric cost bound for this search.
5. peak-memory-capacity-bound: full preprocessing and online peak storage fits
   within 2^39 bytes. For comparison, this dossier interprets the paper's 378 GB
   label as decimal 378,000,000,000-byte host capacity; the paper does not
   specify a binary unit. It is capacity, not peak use. The claimed 2^39-byte
   ceiling is 549,755,813,888 bytes (549.756 decimal GB), about 1.454 times the
   decimal interpretation, so the capacity number does not establish this
   ceiling.

Conditional success and time formulas use q, pi, the two search ceilings, and
the finite setup count immediately above. Let N=2^65 and m=2^33. Under the
first two premises and fresh independent B0 values:

~~~text
P(success) >= 1 - 2^-32 - exp(-m*pi)
            >= 1 - 2^-32 - exp(-1/2)
            = 0.3934693400545... > 0.39.
~~~

The claimed success probability is 0.39, only 0.00346934 above the required
0.39 threshold. It is an algorithmic probability conditional on the stated
premises, not a confidence level for those premises.

The cost formula under collision-frontier-v5 is:

~~~text
T = H + W/2224 + T_preprocessing
T_preprocessing <= 2^36 target-compression equivalents
H = 2^65 + 4(2^33)(196608) + 16
W = 2048(2^65) + 4(2048)(2^65) + 4096(2^33)(196608) + 2(2224)(2^33)
log2(T) = 67.486607283276...; claim.time_log2 = 67.487 (upward rounded)
~~~

The time score is conditional on premises 3 and 4. Peak memory is reported and
reviewed separately; it is not part of the scalar time score.

## Bridge-density evidence and its limit

The fixed table has exactly 408,576 of 2^32 keys. The primary conditional sample
selects one table key uniformly and draws the other seven chaining words from
the seeded Python PRNG for 2^22 proposals. Seed 20261004 produced 127 bridge
filter accepts. The raw output gives the observed conditional frequency
127/4,194,304 = 3.0279159546e-5 and a nominal one-sided 99.9% Clopper-Pearson
lower diagnostic of 2.2650315802e-5. Multiplication by the exact key fraction
408,576/2^32 gives 2.1547021878e-9, above 2^-31 = 4.6566128731e-10.

That interval has its stated binomial coverage only if proposals are iid uniform.
This run is a fixed seeded PRNG stream; it does not establish iid sampling or
calibrated coverage. The seed was inherited from the prior participant run.
Whether it was selected before exploratory results, or whether other seeds or
slices were tried, is not recorded. The 2^20 sizing output uses the same seed
and proposal order, so it is exactly the first 2^20 proposals of the 2^22
stream, not an independent sample; the 33 accepts are not pooled or counted as
corroboration.

The measured model samples abstract uniform chaining values conditioned on a
table-key hit. It does not generate first-block preimages. Thus it supports only
the finite uniform-state filter calculation under its sampling model; transfer
to actual standard-IV C32 outputs remains premise 1. A structural bias correlated
with the exact table predicate could reduce q.

## Tail-yield evidence and its limit

The source paper's Step 3 model has 45 residual bit conditions and
2^17.585 W14/W15 choices. The subtraction 45 - 17.585 = 27.415 gives the
paper's heuristic full-sweep exponent under that condition-count model. The
claimed pi=2^-34 takes 6.585 bits of slack from that model. The paper reports
the 35-step construction, not this candidate's C32 fixed-slice accepted-bridge
average.

The bounded exact diagnostic sampled the first 16 accepted abstract bridge
states from the 2^22 stream, then sampled 256 tail indexes without replacement
per bridge using seed 920260928. Both prefixes replayed through step 13. Each
bridge regenerated 196,608 tails with the same list hash; 4,096 exact C32
second-block comparisons produced zero equalities. The published Table 3 tail
is in the regression candidate set, but it does not collide from the recorded
synthetic C32 regression chaining value. These finite checks validate code paths
and predicates; they are too small to estimate a full-sweep event around 2^-34.
Premise 2 remains unresolved.

There is no organizer execution report for these internal-state computations.
The current experiment protocol supports local addition/XOR events and
organizer-checked target message-pair outputs, not arbitrary C32 internal-state
bridge sampling. No experiment manifest is declared. The code and raw participant
outputs are supplied as auditable input; they are not attributed to the
organizer's deterministic runner.

## Success derivation

For independent first-block trials, X, the count of accepted bridges, is
Binomial(N,q). Under q>=2^-31, E[X]>=2^34 and Var(X)<=E[X]. Since m=2^33 is at
most E[X]/2, Chebyshev gives:

~~~text
P(X < m) <= P(|X-E[X]| >= E[X]/2)
          <= 4 Var(X)/E[X]^2
          <= 4/E[X]
          <= 2^-32.
~~~

Each sweep is a deterministic predicate of its accepted B0 and selected
first-valid record. With independent trial coins, the first m accepted bridges
are iid from the single-trial bridge distribution conditioned on acceptance:
for any ordered accepted outcomes, independence factors the probability into
the same conditional single-acceptance law; summing over the possible trial
indices of those acceptances preserves that product law. This is the usual
rejection-sampling argument. Fresh B0 coins alone would not justify treating
tails attached to one B0 as independent, and the algorithm makes no such claim.

Let p(Y) be the deterministic full-sweep result for accepted bridge Y, equal to
one on a successful bridge and zero otherwise. Premise 2 states E[p(Y)]>=pi.
The first m accepted bridges are iid, so, conditional on having at least m,

~~~text
P(all first m sweeps miss) = (1-E[p(Y)])^m
                           <= (1-pi)^m
                           <= exp(-m*pi)
                           <= exp(-1/2).
~~~

Union-bound this event with X<m to obtain the success formula above. The exact
numerical lower bound is 0.3934693400545..., so the submitted lower bound is
0.39. No experiment is used as a proof of q, pi, or the accepted-sequence
independence argument.

## Charged work

The cost model is collision-frontier-v5. For sha256-r32, one C32 call costs one
target-compression equivalent; every other primitive 256-bit word operation,
including a random 256-bit word, costs 1/2224. All work over all processors is
charged.

For N=2^65 trials, at most four table records per trial, and at most m=2^33
full sweeps, the compression counts are:

- First blocks: N calls, one C32(IV,B0) for every trial.
- Tail tests: four calls per tail, covering both second blocks and both common
  padding blocks even when the second-block states differ. This is
  4m×196,608 = 3×2^51 calls.
- Prefix replays: each accepted bridge has two 14-round branch replays. Each is
  conservatively charged as one full compression equivalent, converted to
  2×2224 word operations per accepted bridge. This is the final term in W.
- Final validation: two complete messages each have three padded blocks, so six
  exact C32 calls suffice. H_replay=16 is the explicit ceiling rounded upward
  from six calls; the other ten units are deliberately unused conservative
  headroom, not additional operations attributed to the algorithm.

The online word-operation ceilings are itemized as follows. Each value is a
256-bit word-RAM operation; a 32-bit arithmetic, bit, or comparison operation
is charged at least one word operation.

| Work unit | Per-unit ceiling | Counted operations in the unit |
|---|---:|---|
| First-block trial, outside table-record loops | 2,048 | two uniform random words (2); sixteen B0 word stores (16); eight chaining-word reads (8); direct-index address/read and empty check (4); trial/accept counters and branches (32); state and message buffer handling (64); result retention amortized over N trials (64); endian conversion and remaining fixed loop/address handling (192). These listed operations total at most 382; 1,666 operations per trial remain charged as explicit overhead allowance. No per-record recovery or per-tail work is hidden here. |
| One examined table record | 2,048 | at most ten record/key reads; six E2/E1/E0 inversions (two branches × three words, each bounded by 21 primitive operations); fourteen W0..W6 recoveries (two branches × seven words, each bounded by 19); four W0..W3 equality checks; W4..W6 row-bit checks bounded by 384 operations; relation checks bounded by 64; record-loop control and state loads/stores bounded by 256. This subtotal is below 1,200 operations; 2,048 is the charged ceiling. |
| One returned tail candidate | 4,096 | at most two raw E15-row candidates per returned tail, each with both-branch A15/W15 derivations and checks bounded by 256 operations (512 total); two-branch schedule/block handling bounded by 768; output comparison, padding control, counters, and writes bounded by 512. These items total at most 1,792 operations; the remaining 2,304 are charged headroom. C32 calls are charged separately in H. |

For the finite setup loops, the per-candidate caps are also itemized. W8 uses at
most 48 operations for both-branch E4 arithmetic, 160 for the 32-position E4
row scan, 8 for E4 relations, 32 for both A0 derivations/comparison, and 8 for
loads and loop state, totaling 256. W7 uses at most 48 for both-branch E3
arithmetic, 160 for the E3 row scan, 32 for both A(-1) derivations, 4 for the
key comparison, and 268 for record loads/stores and loop state, totaling 512.
For each E14 or E15 row candidate, both-branch word derivation and equality
checks use at most 128 operations, a 32-bit row scan at most 160, relation bits
and comparisons at most 32, and loop, pointer, and state traffic at most 192,
totaling 512.

The recorded operation-count inputs and expanded subtotals are in
verification/sha256-r32-revision-ledger.json. The exact finite preprocessing
ceiling is derived below. Its operation count is 21,251,109,920, below the
charged 2^40 word operations:

| Finite setup phase | Count | Maximum operations per item | Upper operations |
|---|---:|---:|---:|
| W8 derivation and checks | 2^20 | 256 | 268,435,456 |
| W7 derivation after 44 W8 survivors | 44×2^19 | 512 | 11,811,160,064 |
| Stable merge sort and pack, 20 levels | 593,920 records | 32 per record per level | 380,108,800 |
| Dense four-byte index initialization and fill | 2^32 slots | 2 | 8,589,934,592 |
| E14 values and 12×2^15 raw E15 candidates | 256 E14; 393,216 E15 | 512 per item | 201,457,664 |
| Source-state replay | at most six C32-equivalent calls | 2,224 word operations per equivalent | 13,344 |

The table sort can use bottom-up merge sort; at most 20 merge levels suffice for
593,920 records. Each six-word record comparison/copy fits 32 operations per
level: twelve word loads/stores, six word comparisons, and fourteen for merge
indices, bounds, branches, and control. A direct index has 2^32 four-byte offsets, including empty-key
sentinels. The setup charge of 2^40 word operations is about
494,384,724.719 target-compression equivalents.

The Step 1 charge is 2^35 target-compression equivalents, rounded above the
paper's approximate 2^34.3 generic work figure under premise 3. After that
charge and finite setup, the characteristic search receives the residual
2^36 - 2^35 - (2^40/2224) = 33,865,353,643.280575 target-compression equivalents under
premise 4. The exact residual is recorded in the revision ledger. The source
provides no numeric upper bound for the characteristic search, and the generic
work-unit conversion for Step 1 is unresolved. The aggregate
preprocessing_log2 is 36 only under these two premises; neither search is free.

With C=2224, the online and total cost are:

~~~text
H = 2^65 + 3×2^51 + 16
W = 2^76 + 2^78 + 3×2^61 + 4448×2^33
T = H + W/2224 + 2^36
log2(T) = 67.486607283276...; claim.time_log2 = 67.487
~~~

The 2^36 preprocessing term includes both searches and the finite setup ceiling
2^40/2224. The ledger program recomputes the formula from the measured table
multiplicity and writes the full numerical result and inputs to
verification/sha256-r32-revision-ledger.json.

## Memory and nonuniform advice

The online index, packed table, and tail array use 2^34 + 14,254,080 +
1,572,864 = 17,195,696,128 bytes. This subtotal excludes executable code,
runtime memory, and scratch space; it is not a complete online peak bound.

The claim reports memory_log2_bytes=39 for the full preprocessing and online
peak. The historical search phases and complete online high-water lack a
measured peak trace or an algorithmic peak bound; the full 2^39-byte ceiling
remains premise 5. The cited 378 GB capacity is smaller than the claimed
549.756 GB decimal ceiling and does not establish it.

The retained nonuniform advice inventory is:

| Item | Bytes |
|---|---:|
| Three Table 3 blocks | 192 |
| C35 chaining value | 32 |
| 54 fixed A/E/W words | 216 |
| Eleven 32-symbol Figure 6 rows | 352 |
| Figure 6 relation indices and masks | 80 |
| Labels, lengths, and alignment | 64 |
| Inventory sum | 936 |

The inventory rounds up to 1,024 bytes. The claim's nonuniform_advice_log2_bytes=16
is a 65,536-byte ceiling. The regenerated table and tail list are charged
preprocessing data, not free advice. No solver logs, binaries, or search
artifacts are retained; their discovery cost remains in the preprocessing
premises.

## Heuristics and remaining obligations

The five heuristic IDs in claim.json remain unresolved:

- fixed-slice-c32-bridge-density: the uniform-CV count and seeded conditional
  sample support plausibility; transfer to actual standard-IV C32 outputs is
  unproved. The seed-selection history and any multiple-seed or slice search
  are unknown.
- fixed-slice-average-tail-yield: the paper's 45-condition model and the
  explicit 6.585-bit haircut support plausibility; neither source results nor
  the zero-hit sample establish the candidate's conditional average pi.
- starting-point-search-resource-bound: 2^34.3 is source-reported generic work;
  the conversion and 2^35 target-compression ceiling remain unresolved.
- characteristic-search-resource-bound: no numeric source work bound is
  available; fitting within the 33.865-billion-equivalent residual remains
  unresolved.
- peak-memory-capacity-bound: the 2^39-byte full peak ceiling is not supported
  by a peak trace; 378 GB is server capacity and is smaller than the claim.

No organizer experiment report, full-scale run, or standard-IV r32 witness is
claimed. The finite outputs and scripts establish only the recorded
transcriptions, deterministic enumerations, seeded sample results, and
conditional arithmetic. A reviewer may reject any of the five premises; the
0.39 probability and 67.487 score depend on them as specified.

## Embedded source, code, inputs, and raw outputs

The intake format accepts only claim.json, proof.md, and the declared certificate/experiment files. Accordingly, the complete reproducibility files are embedded below as named blocks in this proof. To rerun, create a scratch directory with the displayed relative paths, copy each block verbatim, and use Python 3.13.5 with the challenge source at commit fc56c3fa38ac40043d8291649c78148bc4872995. The code blocks are UTF-8 source; the JSON blocks are the recorded input or output bytes. The source-audit and sample outputs include source/profile/program hashes.

From the scratch directory, run python3 verification/sha256-r32-source-audit.py --repo /path/to/repo, python3 verification/sha256-r32-tail-sample.py --repo /path/to/repo, python3 verification/sha256-r32-bridge-probe-size.py --repo /path/to/repo, then python3 verification/sha256-r32-revision-ledger.py. The sizing probe is the first 2^20 proposals of the 2^22 primary stream, not an independent sample.

### Embedded file: sources/li-et-al-source-data.md

~~~text
# Cited source data

**Reference.** Yingxin Li, Fukang Liu, Gaoli Wang, and Jiali Shi, *Pushing the Limit of Memory-efficient Collision Attack Framework for SHA-2*, Cryptology ePrint Archive, Paper 2026/1080 (2026), Section 4, Figure 6, and Table 3. Public record: https://eprint.iacr.org/2026/1080.

The following source-reported quantities are used in the proof:

- Section 4 describes a four-stage characteristic optimization and a SAT/SMT-based search. It reports a Step 1 valid-solution search of approximately 2^34.3 work. The paper does not state a conversion to collision-frontier-v5 units or a numeric upper bound for the characteristic search.
- The 35-step SHA-256 construction has 45 residual bit conditions in its Step 3 analysis and 2^17.585 W14/W15 choices. The dossier's subtraction 45 - 17.585 = 27.415 is arithmetic on those reported inputs. It is a probability model, not a measured rate for the candidate's C32 accepted-bridge distribution.
- The reported experimental machine has 378 GB of RAM capacity. The dossier treats this as decimal 378,000,000,000 bytes when comparing units. It is a capacity report, not a measured peak.
- Table 3 gives the three 64-byte blocks transcribed in the proof appendix block named verification/sha256-r32-paper-inputs.json. The finite replay in verification/sha256-r32-source-audit.py derives the C35 starting chaining value and all fixed A/E words from those blocks.

verification/figure6-conditions.json contains the row and bit-relation transcription used by the enumeration. The source-audit program replays the Table 3 witness, checks the listed relations, and records its pass/fail result. The proof appendix includes the raw source words, condition transcription, derived-state output, challenge-source snapshot, and target-profile snapshot. Neither those participant-side checks nor this transcription authenticate an organizer experiment report.
~~~

### Embedded file: sources/sha256-r32-prefix-v1.json

~~~json
{
  "id": "sha256-r32-prefix-v1",
  "status": "frontier-experiment",
  "algorithm": "sha256",
  "primitive": "SHA-256",
  "specification": "FIPS 180-4",
  "specification_url": "https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf",
  "rounds": 32,
  "full_rounds": 64,
  "round_count_unit": "compression rounds",
  "round_selection": "Execute indices 0 through 31, inclusive, on every padded block.",
  "digest_bits": 256,
  "attack_class": "ordinary-collision",
  "message_domain": "All finite byte strings with bit length less than 2^64; no chosen IV, free-start state, or digest truncation.",
  "block_bits": 512,
  "word_bits": 32,
  "padding": "FIPS 180-4: append 0x80, zero bytes to 56 modulo 64, then 64-bit BIG-endian original bit length.",
  "initialization": "Use the standard fixed IV from the specification once at the start of the complete message.",
  "schedule": "Use the standard message-word selection/expansion and constants at their original indices; do not renumber phases.",
  "feed_forward": "After each reduced compression, add every working state word to the incoming chaining state modulo 2^32. Preserve the full standard state and serialize in standard order.",
  "digest_encoding": "Big-endian standard chaining-state order; all digest words.",
  "reference_implementation": "verifier/hash_functions.py:digest",
  "relation": {
    "preconditions": [
      "m0 and m1 satisfy the message domain",
      "m0 is not byte-for-byte equal to m1"
    ],
    "postcondition": "The two complete sha256-r32 hashes are byte-for-byte equal."
  },
  "out_of_scope": [
    "compression-only or free-start collisions",
    "near-collisions or output truncation",
    "changing the IV, padding, round range, or output width",
    "implementation/side-channel attacks"
  ]
}
~~~

### Embedded file: sources/hash_functions_snapshot.py

~~~python
"""Organizer-owned reduced-round, full-message hash definitions.

MD5: RFC 1321. SHA-1/SHA-256: FIPS 180-4. Reduced variants execute the
first r compression steps on EVERY padded block, retaining IV and feed-forward.
This is a reference checker, not an attack or a participant-code executor.
"""

import struct

MASK = 0xffffffff
FULL_ROUNDS = {"md5": 64, "sha1": 80, "sha256": 64}
MD5_K = (
    0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
    0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
    0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
    0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
    0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05, 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
    0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391,
)
SHA256_K = (
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
)
IV = {
    "md5": (0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476),
    "sha1": (0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0),
    "sha256": (0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
               0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19),
}


def _rol(value: int, count: int) -> int:
    value &= MASK
    return ((value << count) | (value >> (32-count))) & MASK


def _ror(value: int, count: int) -> int:
    return _rol(value, 32-count)


def _compress(algorithm: str, state: tuple[int, ...], block: bytes, rounds: int) -> tuple[int, ...]:
    words = list(struct.unpack("<16I" if algorithm == "md5" else ">16I", block))
    if algorithm == "md5":
        a, b, c, d = state
        rotations = ((7, 12, 17, 22), (5, 9, 14, 20), (4, 11, 16, 23), (6, 10, 15, 21))
        for i in range(rounds):
            if i < 16:
                f, g = (b & c) | (~b & d), i
            elif i < 32:
                f, g = (d & b) | (~d & c), (5*i+1) % 16
            elif i < 48:
                f, g = b ^ c ^ d, (3*i+5) % 16
            else:
                f, g = c ^ (b | ~d), (7*i) % 16
            a, b, c, d = d, (b + _rol(a+f+MD5_K[i]+words[g], rotations[i//16][i%4])) & MASK, b, c
        working = (a, b, c, d)
    elif algorithm == "sha1":
        for i in range(16, rounds):
            words.append(_rol(words[i-3] ^ words[i-8] ^ words[i-14] ^ words[i-16], 1))
        a, b, c, d, e = state
        for i in range(rounds):
            if i < 20:
                f, k = (b & c) | (~b & d), 0x5a827999
            elif i < 40:
                f, k = b ^ c ^ d, 0x6ed9eba1
            elif i < 60:
                f, k = (b & c) | (b & d) | (c & d), 0x8f1bbcdc
            else:
                f, k = b ^ c ^ d, 0xca62c1d6
            a, b, c, d, e = (_rol(a, 5)+f+e+k+words[i]) & MASK, a, _rol(b, 30), c, d
        working = (a, b, c, d, e)
    else:
        for i in range(16, rounds):
            x, y = words[i-15], words[i-2]
            s0 = _ror(x, 7) ^ _ror(x, 18) ^ (x >> 3)
            s1 = _ror(y, 17) ^ _ror(y, 19) ^ (y >> 10)
            words.append((words[i-16]+s0+words[i-7]+s1) & MASK)
        a, b, c, d, e, f, g, h = state
        for i in range(rounds):
            s1 = _ror(e, 6) ^ _ror(e, 11) ^ _ror(e, 25)
            t1 = (h+s1+((e & f) ^ (~e & g))+SHA256_K[i]+words[i]) & MASK
            s0 = _ror(a, 2) ^ _ror(a, 13) ^ _ror(a, 22)
            t2 = (s0+((a & b) ^ (a & c) ^ (b & c))) & MASK
            a, b, c, d, e, f, g, h = (t1+t2) & MASK, a, b, c, (d+t1) & MASK, e, f, g
        working = (a, b, c, d, e, f, g, h)
    return tuple((old+new) & MASK for old, new in zip(state, working))


def digest(data: bytes, algorithm: str, rounds: int) -> bytes:
    """Hash bytes with the pinned prefix-step/full-message semantics."""
    if algorithm == "blake3":
        from .blake3 import blake3
        return blake3(data, rounds)
    if algorithm in ("sha3_256", "keccak800"):
        from .keccak import sha3_256, keccak800
        return {"sha3_256": sha3_256, "keccak800": keccak800}[algorithm](data, rounds)
    if algorithm not in FULL_ROUNDS or type(rounds) is not int or not 1 <= rounds <= FULL_ROUNDS[algorithm]:
        raise ValueError("unsupported algorithm or round count")
    if not isinstance(data, bytes) or len(data) >= 1 << 61:
        raise ValueError("requires bytes with bit length less than 2^64")
    endian = "little" if algorithm == "md5" else "big"
    padded = data + b"\x80" + bytes((55-len(data)) % 64) + (8*len(data)).to_bytes(8, endian)
    state = IV[algorithm]
    for offset in range(0, len(padded), 64):
        state = _compress(algorithm, state, padded[offset:offset+64], rounds)
    return b"".join(word.to_bytes(4, endian) for word in state)
~~~

### Embedded file: verification/sha256-r32-paper-inputs.json

~~~json
{
  "source": "Li et al., ePrint 2026/1080, Section 4, Table 3, published pagination p. 307.",
  "word_encoding": "16 big-endian 32-bit SHA-256 message words per block; hex text in word order.",
  "M0_words": "a8850273 c0f4a504 5d3ad7b5 6e5f5026 535cc256 e92ef7a5 436f70df 7d7e236a cadc14e8 d59ac191 6874f1ba 6b83960d f6dfe9de 6a013df2 f856b739 237894e8",
  "M1_words": "c0008214 ae65f3bf e93c006a 5f195aa9 a4d6cd0f 21811cec ea897317 db9ec665 6ec17218 5100da8a 0912e57b a96b2054 45f2222c 4d12f88a d2701ecc 140976d1",
  "M1_prime_words": "c0008214 ae65f3bf e93c006a 5f195aa9 84d6cd0f 25c114ec ca897317 da9fd6ef 6ec97e18 5100da8a 0912e57b a96b2054 41b22a2c 6d12f88a d2701ecc 140976d1",
  "reported_C35_IV_M0": "c4369610 c91f70a7 87e430e6 a5e58128 d29cb97b 9ab268d1 8788f401 629f6cb2",
  "reported_C32_IV_M0": "6a9f7255 39f4063e a684176a b5efb469 57ccf218 f7ab3896 562fcb55 c67d5c37",
  "reported_C35_second_block_collision": true,
  "reported_C32_second_block_collision_from_C35_cv": true
}
~~~

### Embedded file: verification/figure6-conditions.json

~~~json
{
  "source": {
    "citation": "Yingxin Li, Fukang Liu, Gaoli Wang, Jiali Shi, Pushing the Limit of Memory-efficient Collision Attack Framework for SHA-2, Cryptology ePrint Archive, Paper 2026/1080, Section 4, Figure 6 and Table 3.",
    "figure6_location": "Published pagination pp. 302-303; Figure 6.",
    "table3_location": "Published pagination p. 307; Table 3.",
    "transcribed_for": "sha256-r32-prefix-v1 fixed-slice reconstruction"
  },
  "bit_convention": {
    "bit_zero": "least significant bit",
    "row_leftmost_bit": 31,
    "symbols": {
      "=": "same free bit in both branches",
      "0": "both bits fixed to 0",
      "1": "both bits fixed to 1",
      "u": "0 to 1",
      "n": "1 to 0"
    }
  },
  "rows": {
    "E3": "=====1=====011======0======0====",
    "E4": "==n0=0=1===100=0==0=1===0==1=0=1",
    "W7": "=======n=======u===u====u=1=u=u=",
    "W8": "============u=======uu==========",
    "W4": "==n=============================",
    "W5": "=====u===u==========n===========",
    "W6": "==n=============================",
    "E14": "=0=100110000000=101=0000=110===0",
    "E15": "=1====0011===u10001=011===0n===1",
    "A14": "==u=============================",
    "A15": "================================"
  },
  "relations": {
    "E4": {"unequal_bit_pairs": [[10, 15]]},
    "W7": {
      "unequal_vectors": [[[22, 13, 23], [18, 9, 8]]],
      "equal_vectors": [[[11, 14, 20], [22, 31, 31]]]
    },
    "W8": {
      "equal_vectors": [[[0, 14, 21], [28, 25, 6]]],
      "unequal_vectors": [[[31, 23, 30, 15, 22, 8], [27, 2, 15, 26, 7, 4]]]
    },
    "W4": {
      "unequal_vectors": [[[1, 8], [12, 25]]],
      "equal_vectors": [[[18], [14]]]
    },
    "W5": {"equal_vectors": [[[0, 1, 30], [28, 18, 9]]]},
    "W6": {
      "equal_vectors": [[[1, 8], [12, 25]]],
      "unequal_vectors": [[[18], [14]]]
    },
    "A14": {
      "xor_mask": "0000000020000000",
      "unequal_vectors": [[[18, 8], [6, 17]]],
      "same_as_state_bits": [[20, 4, 9]],
      "unequal_state_bits": [[15, 13, 15]]
    },
    "A15": {
      "equal_branches": true,
      "unequal_state_bits": [[29, 6, 29], [29, 13, 29]]
    },
    "W20": {"unequal_vectors": [[[4, 31], [6, 22]]]}
  },
  "corrections_verified_on_table3_witness": [
    "A14[18,8] != A14[6,17]",
    "A15[29] != A6[29]",
    "W20[4,31] != W20[6,22]"
  ]
}
~~~

### Embedded file: verification/sha256-r32-source-audit.py

~~~python
#!/usr/bin/env python3
"""Replay the published Table 3 pair and bind its constants to the transcript."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import platform
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CANDIDATE = HERE.parent
SOURCES = CANDIDATE / "sources"
sys.path.insert(0, str(SOURCES))
from hash_functions_snapshot import IV, SHA256_K, _compress, digest  # noqa: E402

with (HERE / "sha256-r32-paper-inputs.json").open(encoding="utf-8") as handle:
    INPUTS = json.load(handle)
with (HERE / "figure6-conditions.json").open(encoding="utf-8") as handle:
    FIGURE6 = json.load(handle)

MASK = 0xFFFFFFFF


def parse_words(field: str) -> tuple[int, ...]:
    words = tuple(int(item, 16) for item in INPUTS[field].split())
    if len(words) != 16:
        raise AssertionError(f"{field} must contain 16 words")
    return words


def pack(words: tuple[int, ...]) -> bytes:
    return struct.pack(">16I", *words)


def ror(value: int, bits: int) -> int:
    return ((value >> bits) | (value << (32 - bits))) & MASK


def sigma0(value: int) -> int:
    return ror(value, 7) ^ ror(value, 18) ^ (value >> 3)


def sigma1(value: int) -> int:
    return ror(value, 17) ^ ror(value, 19) ^ (value >> 10)


def expand(words16: tuple[int, ...], limit: int = 32) -> list[int]:
    words = list(words16)
    for index in range(16, limit):
        words.append((words[index - 16] + sigma0(words[index - 15]) +
                      words[index - 7] + sigma1(words[index - 2])) & MASK)
    return words


def trace(state: tuple[int, ...], message: tuple[int, ...], rounds: int = 35):
    """Return round-indexed a/e working words plus expanded schedule."""
    words = expand(message, rounds)
    a, b, c, d, e, f, g, h = state
    av, ev = {}, {}
    for index in range(rounds):
        t1 = (h + (ror(e, 6) ^ ror(e, 11) ^ ror(e, 25)) +
              ((e & f) ^ (~e & g)) + SHA256_K[index] + words[index]) & MASK
        t2 = ((ror(a, 2) ^ ror(a, 13) ^ ror(a, 22)) +
              ((a & b) ^ (a & c) ^ (b & c))) & MASK
        a, b, c, d, e, f, g, h = (t1 + t2) & MASK, a, b, c, (d + t1) & MASK, e, f, g
        av[index] = a
        ev[index] = e
    return av, ev, words


def row_ok(row: str, first: int, second: int) -> bool:
    for offset, symbol in enumerate(row):
        bit = 31 - offset
        x, y = (first >> bit) & 1, (second >> bit) & 1
        if symbol == "=" and x != y:
            return False
        if symbol == "0" and (x != 0 or y != 0):
            return False
        if symbol == "1" and (x != 1 or y != 1):
            return False
        if symbol == "n" and (x != 1 or y != 0):
            return False
        if symbol == "u" and (x != 0 or y != 1):
            return False
    return True


def relation_edges(name: str):
    relation = FIGURE6["relations"].get(name, {})
    edges = [(a, b, 1) for a, b in relation.get("unequal_bit_pairs", [])]
    for left, right in relation.get("equal_vectors", []):
        edges.extend((a, b, 0) for a, b in zip(left, right))
    for left, right in relation.get("unequal_vectors", []):
        edges.extend((a, b, 1) for a, b in zip(left, right))
    return edges


def relations_ok(word: int, edges) -> bool:
    return all((((word >> a) ^ (word >> b)) & 1) == parity for a, b, parity in edges)


def bit(word: int, index: int) -> int:
    return (word >> index) & 1


def hexwords(words) -> list[str]:
    return [f"{word:08x}" for word in words]


def find_repo(repo_arg: str | None):
    candidates = [Path(repo_arg).resolve()] if repo_arg else []
    for parent in Path(__file__).resolve().parents:
        candidates.extend((parent, parent / "repo"))
    return next((root for root in candidates
                 if (root / "verifier" / "hash_functions.py").is_file()), None)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", help="optional challenge source root for byte-for-byte snapshot comparison")
    args = parser.parse_args()

    m0 = parse_words("M0_words")
    m1 = parse_words("M1_words")
    m1p = parse_words("M1_prime_words")
    source_code = (SOURCES / "hash_functions_snapshot.py").read_bytes()
    profile_bytes = (SOURCES / "sha256-r32-prefix-v1.json").read_bytes()
    figure_bytes = (HERE / "figure6-conditions.json").read_bytes()
    input_bytes = (HERE / "sha256-r32-paper-inputs.json").read_bytes()

    cv35 = _compress("sha256", IV["sha256"], pack(m0), 35)
    cv32 = _compress("sha256", IV["sha256"], pack(m0), 32)
    a, e, w = trace(cv35, m1)
    ap, ep, wp = trace(cv35, m1p)

    expected_a = tuple(int(word, 16) for word in
                       "66e7ba7c 5ff9d9f8 9123b13f b8560dbb 677e1e2a 9bcf7bbe f8677ad6 4a299906 44d24ab4 39781650 6c206d58 35c5c2b8 0508c8f0".split())
    expected_ap = tuple(int(word, 16) for word in
                        "66e7ba7c 5ff9d9f8 9123b13f 98560dbb 633b16ba 9bcf7bbe f8677ad6 4a299906 44f24ab5 39781650 6422edc8 574542b8 0508c8f0".split())
    expected_e = tuple(int(word, 16) for word in
                       "58f38fac b95f2294 87431160 11cae594 d504bf23 7f27d24c bf893f69 2300f189 fcc08ef5".split())
    expected_ep = tuple(int(word, 16) for word in
                        "5caf87bc a94f0a01 a7421160 f1cae594 d0e1b7b4 bf27d74c b78bbfd9 3fffd0f9 bf81c0f4".split())

    assert cv35 == tuple(int(word, 16) for word in INPUTS["reported_C35_IV_M0"].split())
    assert cv32 == tuple(int(word, 16) for word in INPUTS["reported_C32_IV_M0"].split())
    assert tuple(a[index] for index in range(1, 14)) == expected_a
    assert tuple(ap[index] for index in range(1, 14)) == expected_ap
    assert tuple(e[index] for index in range(5, 14)) == expected_e
    assert tuple(ep[index] for index in range(5, 14)) == expected_ep

    conditions = []
    for name, index in (("E3", 3), ("E4", 4), ("W7", 7), ("W8", 8),
                        ("W4", 4), ("W5", 5), ("W6", 6),
                        ("E14", 14), ("E15", 15), ("A14", 14), ("A15", 15)):
        left = {"E3": e, "E4": e, "W7": w, "W8": w, "W4": w, "W5": w,
                "W6": w, "E14": e, "E15": e, "A14": a, "A15": a}[name][index]
        right = {"E3": ep, "E4": ep, "W7": wp, "W8": wp, "W4": wp, "W5": wp,
                 "W6": wp, "E14": ep, "E15": ep, "A14": ap, "A15": ap}[name][index]
        conditions.append({"name": name, "passes": row_ok(FIGURE6["rows"][name], left, right)})

    for name, index in (("E4", 4), ("W7", 7), ("W8", 8), ("W4", 4), ("W5", 5), ("W6", 6), ("A14", 14), ("W20", 20)):
        edges = relation_edges(name)
        if name == "W20":
            words_to_check = (w[index],)
        elif name == "A14":
            words_to_check = (a[index],)
        elif name == "E4":
            words_to_check = (e[index],)
        elif name == "W7":
            words_to_check = (w[index],)
        elif name == "W8":
            words_to_check = (w[index],)
        elif name == "W4":
            words_to_check = (w[index],)
        elif name == "W5":
            words_to_check = (w[index],)
        else:
            words_to_check = (w[index],)
        # Relation entries are within-word relations; row checks cover branch pairs.
        for checked in words_to_check:
            conditions.append({"name": f"{name}-bit-relations", "passes": relations_ok(checked, edges)})

    conditions.extend([
        {"name": "A14 xor difference is exactly 2^29", "passes": (a[14] ^ ap[14]) == (1 << 29)},
        {"name": "A15 branches are equal", "passes": a[15] == ap[15]},
        {"name": "A14[20]=A4[9]", "passes": bit(a[14], 20) == bit(a[4], 9)},
        {"name": "A14[15]!=A13[15]", "passes": bit(a[14], 15) != bit(a[13], 15)},
        {"name": "A15[29]!=A6[29]", "passes": bit(a[15], 29) != bit(a[6], 29)},
        {"name": "A15[29]!=A13[29]", "passes": bit(a[15], 29) != bit(a[13], 29)},
    ])

    second32 = (_compress("sha256", cv35, pack(m1), 32) ==
                _compress("sha256", cv35, pack(m1p), 32))
    second35 = (_compress("sha256", cv35, pack(m1), 35) ==
                _compress("sha256", cv35, pack(m1p), 35))
    full32 = digest(pack(m0) + pack(m1), "sha256", 32) == digest(pack(m0) + pack(m1p), "sha256", 32)
    full35 = digest(pack(m0) + pack(m1), "sha256", 35) == digest(pack(m0) + pack(m1p), "sha256", 35)
    assert second32 is bool(INPUTS["reported_C32_second_block_collision_from_C35_cv"])
    assert second35 is bool(INPUTS["reported_C35_second_block_collision"])
    assert full32 is False and full35 is True
    assert pack(m1) != pack(m1p)

    repo = find_repo(args.repo)
    source_match = None
    profile_match = None
    repo_commit = "unavailable"
    if repo is not None:
        source_match = source_code == (repo / "verifier" / "hash_functions.py").read_bytes()
        profile_match = profile_bytes == (repo / "target-profiles" / "sha256-r32-prefix-v1.json").read_bytes()
        if (repo / ".git").exists():
            import subprocess
            repo_commit = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                                         check=True, capture_output=True, text=True).stdout.strip()

    out = {
        "target_profile": "sha256-r32-prefix-v1",
        "source_repo_commit": repo_commit,
        "source_matches_repo": source_match,
        "profile_matches_repo": profile_match,
        "source_hashes": {
            "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "bundled_hash_functions_sha256": hashlib.sha256(source_code).hexdigest(),
            "bundled_profile_sha256": hashlib.sha256(profile_bytes).hexdigest(),
            "figure6_transcription_sha256": hashlib.sha256(figure_bytes).hexdigest(),
            "paper_inputs_sha256": hashlib.sha256(input_bytes).hexdigest(),
        },
        "published_table3_replay": {
            "M0_words": hexwords(m0),
            "M1_words": hexwords(m1),
            "M1_prime_words": hexwords(m1p),
            "C35_IV_M0": hexwords(cv35),
            "C32_IV_M0": hexwords(cv32),
            "derived_A1_A13": hexwords(a[index] for index in range(1, 14)),
            "derived_A1_prime_A13_prime": hexwords(ap[index] for index in range(1, 14)),
            "derived_E5_E13": hexwords(e[index] for index in range(5, 14)),
            "derived_E5_prime_E13_prime": hexwords(ep[index] for index in range(5, 14)),
            "C32_second_block_equal_from_C35_cv": second32,
            "C35_second_block_equal_from_C35_cv": second35,
            "complete_standard_iv_C32_messages_equal": full32,
            "complete_standard_iv_C35_messages_equal": full35,
            "messages_distinct": pack(m1) != pack(m1p),
        },
        "figure6_witness_conditions": conditions,
        "all_reported_conditions_pass": all(item["passes"] for item in conditions),
        "limitation": "This verifies the packaged Table 3 input and Figure 6 transcription against replayed finite state; it does not authenticate the transcription's source or prove any heuristic rate.",
        "python": sys.version,
        "platform": platform.platform(),
    }
    output = HERE / "sha256-r32-source-audit.json"
    output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
~~~

### Embedded file: verification/sha256-r32-source-audit.json

~~~json
{
  "target_profile": "sha256-r32-prefix-v1",
  "source_repo_commit": "fc56c3fa38ac40043d8291649c78148bc4872995",
  "source_matches_repo": true,
  "profile_matches_repo": true,
  "source_hashes": {
    "program_sha256": "a038f829410d5ac0a088052e6cb59731c8fad6b1c25f1bef2f08942642281164",
    "bundled_hash_functions_sha256": "514fa8ab8a461e4a41080efa27b4ba2a3b499eeedf0a2d2346e6562835d040f5",
    "bundled_profile_sha256": "93d2e5d9ca93540633798d58cbab2d6d8447916db2b127e9abe71f45d14f6835",
    "figure6_transcription_sha256": "a8f9ed4cc356804f87bb8ce4986f751baf8ea4666f1a5dc3e468127eff6fc64e",
    "paper_inputs_sha256": "b30b7090712cb2b3c95990a4400abf45d3dfe620ffa4cea1fe89b5a523c19509"
  },
  "published_table3_replay": {
    "M0_words": [
      "a8850273",
      "c0f4a504",
      "5d3ad7b5",
      "6e5f5026",
      "535cc256",
      "e92ef7a5",
      "436f70df",
      "7d7e236a",
      "cadc14e8",
      "d59ac191",
      "6874f1ba",
      "6b83960d",
      "f6dfe9de",
      "6a013df2",
      "f856b739",
      "237894e8"
    ],
    "M1_words": [
      "c0008214",
      "ae65f3bf",
      "e93c006a",
      "5f195aa9",
      "a4d6cd0f",
      "21811cec",
      "ea897317",
      "db9ec665",
      "6ec17218",
      "5100da8a",
      "0912e57b",
      "a96b2054",
      "45f2222c",
      "4d12f88a",
      "d2701ecc",
      "140976d1"
    ],
    "M1_prime_words": [
      "c0008214",
      "ae65f3bf",
      "e93c006a",
      "5f195aa9",
      "84d6cd0f",
      "25c114ec",
      "ca897317",
      "da9fd6ef",
      "6ec97e18",
      "5100da8a",
      "0912e57b",
      "a96b2054",
      "41b22a2c",
      "6d12f88a",
      "d2701ecc",
      "140976d1"
    ],
    "C35_IV_M0": [
      "c4369610",
      "c91f70a7",
      "87e430e6",
      "a5e58128",
      "d29cb97b",
      "9ab268d1",
      "8788f401",
      "629f6cb2"
    ],
    "C32_IV_M0": [
      "6a9f7255",
      "39f4063e",
      "a684176a",
      "b5efb469",
      "57ccf218",
      "f7ab3896",
      "562fcb55",
      "c67d5c37"
    ],
    "derived_A1_A13": [
      "66e7ba7c",
      "5ff9d9f8",
      "9123b13f",
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
    "derived_A1_prime_A13_prime": [
      "66e7ba7c",
      "5ff9d9f8",
      "9123b13f",
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
    ],
    "derived_E5_E13": [
      "58f38fac",
      "b95f2294",
      "87431160",
      "11cae594",
      "d504bf23",
      "7f27d24c",
      "bf893f69",
      "2300f189",
      "fcc08ef5"
    ],
    "derived_E5_prime_E13_prime": [
      "5caf87bc",
      "a94f0a01",
      "a7421160",
      "f1cae594",
      "d0e1b7b4",
      "bf27d74c",
      "b78bbfd9",
      "3fffd0f9",
      "bf81c0f4"
    ],
    "C32_second_block_equal_from_C35_cv": true,
    "C35_second_block_equal_from_C35_cv": true,
    "complete_standard_iv_C32_messages_equal": false,
    "complete_standard_iv_C35_messages_equal": true,
    "messages_distinct": true
  },
  "figure6_witness_conditions": [
    {
      "name": "E3",
      "passes": true
    },
    {
      "name": "E4",
      "passes": true
    },
    {
      "name": "W7",
      "passes": true
    },
    {
      "name": "W8",
      "passes": true
    },
    {
      "name": "W4",
      "passes": true
    },
    {
      "name": "W5",
      "passes": true
    },
    {
      "name": "W6",
      "passes": true
    },
    {
      "name": "E14",
      "passes": true
    },
    {
      "name": "E15",
      "passes": true
    },
    {
      "name": "A14",
      "passes": true
    },
    {
      "name": "A15",
      "passes": true
    },
    {
      "name": "E4-bit-relations",
      "passes": true
    },
    {
      "name": "W7-bit-relations",
      "passes": true
    },
    {
      "name": "W8-bit-relations",
      "passes": true
    },
    {
      "name": "W4-bit-relations",
      "passes": true
    },
    {
      "name": "W5-bit-relations",
      "passes": true
    },
    {
      "name": "W6-bit-relations",
      "passes": true
    },
    {
      "name": "A14-bit-relations",
      "passes": true
    },
    {
      "name": "W20-bit-relations",
      "passes": true
    },
    {
      "name": "A14 xor difference is exactly 2^29",
      "passes": true
    },
    {
      "name": "A15 branches are equal",
      "passes": true
    },
    {
      "name": "A14[20]=A4[9]",
      "passes": true
    },
    {
      "name": "A14[15]!=A13[15]",
      "passes": true
    },
    {
      "name": "A15[29]!=A6[29]",
      "passes": true
    },
    {
      "name": "A15[29]!=A13[29]",
      "passes": true
    }
  ],
  "all_reported_conditions_pass": true,
  "limitation": "This verifies the packaged Table 3 input and Figure 6 transcription against replayed finite state; it does not authenticate the transcription's source or prove any heuristic rate.",
  "python": "3.13.5 | packaged by Anaconda, Inc. | (main, Jun 12 2025, 11:23:37) [Clang 14.0.6 ]",
  "platform": "macOS-27.0-arm64-arm-64bit-Mach-O"
}
~~~

### Embedded file: verification/sha256-r32-tail-sample.py

~~~python
#!/usr/bin/env python3
"""Reproduce a bounded conditional bridge/tail sample for sha256-r32.

The sample draws abstract chaining values from the idealized uniform-CV model,
conditions them on the exact fixed-slice table and bridge filters, then runs a
per-bridge tail construction and a deterministic sample of exact C32 checks.
It deliberately does not claim that these abstract states were produced by
SHA256_r32(IV, B0); that distribution transfer remains a separate heuristic.
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import random
import struct
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = None
IV = None
SHA256_K = None
_compress = None


def configure_repo(repo_arg: str | None = None):
    """Load the pinned reference implementation from an explicit repo root."""
    global ROOT, IV, SHA256_K, _compress
    roots = [Path(repo_arg).resolve()] if repo_arg else []
    for parent in Path(__file__).resolve().parents:
        roots.extend((parent, parent / "repo"))
    ROOT = next((root for root in roots if (root / "verifier" / "hash_functions.py").is_file()), None)
    if ROOT is None:
        raise SystemExit("pass --repo PATH to the challenge source root")
    sys.path.insert(0, str(ROOT))
    from verifier.hash_functions import IV as source_iv, SHA256_K as source_k, _compress as source_compress
    IV, SHA256_K, _compress = source_iv, source_k, source_compress


def source_metadata(program_path: Path | None = None):
    """Return hashes binding the run to source, target profile, and program."""
    reference = ROOT / "verifier" / "hash_functions.py"
    profile = ROOT / "target-profiles" / "sha256-r32-prefix-v1.json"
    try:
        commit = subprocess.run(
            ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
            check=True, capture_output=True, text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        commit = "unavailable"
    return {
        "challenge_commit": commit,
        "target_profile": "sha256-r32-prefix-v1",
        "target_profile_sha256": hashlib.sha256(profile.read_bytes()).hexdigest(),
        "reference_hash_functions_sha256": hashlib.sha256(reference.read_bytes()).hexdigest(),
        "program_sha256": hashlib.sha256((program_path or Path(__file__)).read_bytes()).hexdigest(),
        "bridge_sampler_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "figure6_conditions_sha256": hashlib.sha256(FIGURE6_PATH.read_bytes()).hexdigest(),
        "paper_inputs_sha256": hashlib.sha256(PAPER_INPUTS_PATH.read_bytes()).hexdigest(),
        "python": sys.version,
        "platform": platform.platform(),
    }

MASK = 0xFFFFFFFF
FIGURE6_PATH = HERE / "figure6-conditions.json"
PAPER_INPUTS_PATH = HERE / "sha256-r32-paper-inputs.json"
FIGURE6 = json.loads(FIGURE6_PATH.read_text())
ROWS = FIGURE6["rows"]

A1 = tuple(map(lambda x: int(x, 16), """
66e7ba7c 5ff9d9f8 9123b13f b8560dbb 677e1e2a 9bcf7bbe f8677ad6
4a299906 44d24ab4 39781650 6c206d58 35c5c2b8 0508c8f0
""".split()))
A1P = tuple(map(lambda x: int(x, 16), """
66e7ba7c 5ff9d9f8 9123b13f 98560dbb 633b16ba 9bcf7bbe f8677ad6
4a299906 44f24ab5 39781650 6422edc8 574542b8 0508c8f0
""".split()))
E5 = tuple(map(lambda x: int(x, 16), """
58f38fac b95f2294 87431160 11cae594 d504bf23 7f27d24c bf893f69
2300f189 fcc08ef5
""".split()))
E5P = tuple(map(lambda x: int(x, 16), """
5caf87bc a94f0a01 a7421160 f1cae594 d0e1b7b4 bf27d74c b78bbfd9
3fffd0f9 bf81c0f4
""".split())
)
W9 = tuple(map(lambda x: int(x, 16), "5100da8a 0912e57b a96b2054 45f2222c 4d12f88a".split()))
W9P = tuple(map(lambda x: int(x, 16), "5100da8a 0912e57b a96b2054 41b22a2c 6d12f88a".split()))

def row_pair(row: str, x: int) -> tuple[int, int]:
    y = x
    for j, char in enumerate(row):
        if char in "nu":
            y ^= 1 << (31 - j)
    return x, y


def row_ok(row: str, x: int, y: int) -> bool:
    for j, char in enumerate(row):
        a, b = (x >> (31 - j)) & 1, (y >> (31 - j)) & 1
        if char == "=" and a != b:
            return False
        if char == "0" and (a != 0 or b != 0):
            return False
        if char == "1" and (a != 1 or b != 1):
            return False
        if char == "n" and (a != 1 or b != 0):
            return False
        if char == "u" and (a != 0 or b != 1):
            return False
    return True


def relations_ok(x: int, edges: tuple[tuple[int, int, int], ...]) -> bool:
    return all((((x >> a) ^ (x >> b)) & 1) == parity for a, b, parity in edges)


def equal_vectors(left: tuple[int, ...], right: tuple[int, ...]):
    return tuple((a, b, 0) for a, b in zip(left, right))


def unequal_vectors(left: tuple[int, ...], right: tuple[int, ...]):
    return tuple((a, b, 1) for a, b in zip(left, right))


def relation_edges(name: str):
    """Expand the packaged Figure 6 transcription into LSB-indexed edges."""
    relation = FIGURE6["relations"].get(name, {})
    edges = list((a, b, 1) for a, b in relation.get("unequal_bit_pairs", []))
    for left, right in relation.get("equal_vectors", []):
        edges.extend(equal_vectors(tuple(left), tuple(right)))
    for left, right in relation.get("unequal_vectors", []):
        edges.extend(unequal_vectors(tuple(left), tuple(right)))
    return tuple(edges)


def row_values(row: str, edges=()):
    """Yield every pair satisfying a row and LSB-indexed bit relations."""
    fixed = {31 - j: int(c in "1n") for j, c in enumerate(row) if c != "="}
    graph = {i: [] for i in range(32)}
    for a, b, parity in edges:
        graph[a].append((b, parity))
        graph[b].append((a, parity))

    components = []
    seen = set()
    for root in range(32):
        if root in seen:
            continue
        offsets = {root: 0}
        stack = [root]
        seen.add(root)
        while stack:
            a = stack.pop()
            for b, parity in graph[a]:
                if b in offsets:
                    if offsets[b] != (offsets[a] ^ parity):
                        return
                else:
                    offsets[b] = offsets[a] ^ parity
                    stack.append(b)
                    seen.add(b)
        roots = {fixed[b] ^ offset for b, offset in offsets.items() if b in fixed}
        if len(roots) > 1:
            return
        components.append((offsets, next(iter(roots)) if roots else None))

    free = [i for i, (_, root_value) in enumerate(components) if root_value is None]
    flips = sum(1 << (31 - j) for j, c in enumerate(row) if c in "nu")
    for assignment in range(1 << len(free)):
        choices = {component: ((assignment >> j) & 1) for j, component in enumerate(free)}
        x = 0
        for i, (offsets, root_value) in enumerate(components):
            bit0 = choices[i] if root_value is None else root_value
            for bit, offset in offsets.items():
                x |= (bit0 ^ offset) << bit
        yield x, x ^ flips


def ror(x: int, n: int) -> int:
    return ((x >> n) | (x << (32 - n))) & MASK


def s0(x: int) -> int:
    return ror(x, 2) ^ ror(x, 13) ^ ror(x, 22)


def s1(x: int) -> int:
    return ror(x, 6) ^ ror(x, 11) ^ ror(x, 25)


def ssig0(x: int) -> int:
    return ror(x, 7) ^ ror(x, 18) ^ (x >> 3)


def ch(x: int, y: int, z: int) -> int:
    return (x & y) ^ (~x & z)


def maj(x: int, y: int, z: int) -> int:
    return (x & y) ^ (x & z) ^ (y & z)


def bit_edges_for_w7():
    return relation_edges("W7")


def bit_edges_for_w8():
    return relation_edges("W8")


def build_table():
    """Regenerate the finite fixed-slice table from the repository dossier."""
    e4_edges = relation_edges("E4")
    w8_survivors = []
    debug_known_w8 = {}
    w8_count = 0
    for w8, w8p in row_values(ROWS["W8"], bit_edges_for_w8()):
        w8_count += 1
        e4 = (E5[3] - A1[3] - s1(E5[2]) - ch(E5[2], E5[1], E5[0]) - SHA256_K[8] - w8) & MASK
        e4p = (E5P[3] - A1P[3] - s1(E5P[2]) - ch(E5P[2], E5P[1], E5P[0]) - SHA256_K[8] - w8p) & MASK
        if not row_ok(ROWS["E4"], e4, e4p) or not relations_ok(e4, e4_edges):
            continue
        a0 = (e4 + s0(A1[2]) + maj(A1[2], A1[1], A1[0]) - A1[3]) & MASK
        a0p = (e4p + s0(A1P[2]) + maj(A1P[2], A1P[1], A1P[0]) - A1P[3]) & MASK
        if a0 == a0p:
            w8_survivors.append((w8, w8p, e4, e4p, a0))
            if w8 in (0x6ec17218, 0x6e417236):
                debug_known_w8[f"{w8:08x}"] = [f"{x:08x}" for x in (w8, w8p, e4, e4p, a0)]

    w7_values = list(row_values(ROWS["W7"], bit_edges_for_w7()))
    debug_known_pairs = []
    table = defaultdict(list)
    for w8, w8p, e4, e4p, a0 in w8_survivors:
        for w7, w7p in w7_values:
            e3 = (E5[2] - A1[2] - s1(E5[1]) - ch(E5[1], E5[0], e4) - SHA256_K[7] - w7) & MASK
            e3p = (E5P[2] - A1P[2] - s1(E5P[1]) - ch(E5P[1], E5P[0], e4p) - SHA256_K[7] - w7p) & MASK
            if not row_ok(ROWS["E3"], e3, e3p):
                continue
            key = (e3 + s0(A1[1]) + maj(A1[1], A1[0], a0) - A1[2]) & MASK
            a0p = a0
            keyp = (e3p + s0(A1P[1]) + maj(A1P[1], A1P[0], a0p) - A1P[2]) & MASK
            if key != keyp:
                continue
            table[key].append((w7, w7p, w8, w8p, e3, e3p, e4, e4p, a0))
    for records in table.values():
        records.sort()
    flat = []
    for key in sorted(table):
        for record in table[key]:
            flat.extend((key, record[0], record[2], record[4], record[6], record[8]))
    packed = struct.pack(">" + "I" * len(flat), *flat)
    wanted = (
        (0xc4369610, 0xdb9ec665, 0x6ec17218, 0xa70d4308, 0x2932d839, 0xac311f10),
        (0xf3b8f7ae, 0xab9c6465, 0x6e417236, 0xd68fa526, 0x29b2d81b, 0xacb11ef2),
    )
    actual_rows = {
        (key, record[0], record[2], record[4], record[6], record[8])
        for key, records in table.items() for record in records
    }
    return table, {
        "w8_admissible": w8_count,
        "w8_state_survivors": len(w8_survivors),
        "w7_admissible": len(w7_values),
        "table_records": sum(map(len, table.values())),
        "distinct_keys": len(table),
        "max_records_per_key": max(map(len, table.values())),
        "table_bytes": len(packed),
        "table_sha256": hashlib.sha256(packed).hexdigest(),
        "published_and_c32_regression_records_present": [list(row) in [list(x) for x in actual_rows] for row in wanted],
    }


def derive_bridge(cv: tuple[int, ...], record: tuple[int, ...]):
    """Recover W0..W6 for both branches and return full W0..W13 pairs."""
    key, r = cv[0], record
    w7, w7p, w8, w8p, e3, e3p, e4, e4p, a0 = r
    branches = []
    for prime in (False, True):
        # CV[0:4] are A(-1)..A(-4), in reverse index order.
        aa = {i: cv[-1 - i] for i in range(-4, 0)}
        # CV[4:8] are E(-1)..E(-4), in reverse index order.
        ee = {i: cv[3 - i] for i in range(-4, 0)}
        fixed_a = A1P if prime else A1
        fixed_e = E5P if prime else E5
        fixed_w = W9P if prime else W9
        for i, value in enumerate(fixed_a, 1):
            aa[i] = value
        aa[0] = a0
        ee.update({i: value for i, value in enumerate(fixed_e, 5)})
        ee[3] = e3p if prime else e3
        ee[4] = e4p if prime else e4
        ee[2] = (aa[2] + aa[-2] - s0(aa[1]) - maj(aa[1], aa[0], aa[-1])) & MASK
        ee[1] = (aa[1] + aa[-3] - s0(aa[0]) - maj(aa[0], aa[-1], aa[-2])) & MASK
        ee[0] = (aa[0] + aa[-4] - s0(aa[-1]) - maj(aa[-1], aa[-2], aa[-3])) & MASK
        ww = []
        for i in range(7):
            ww.append((ee[i] - aa[i - 4] - ee[i - 4] - s1(ee[i - 1]) -
                       ch(ee[i - 1], ee[i - 2], ee[i - 3]) - SHA256_K[i]) & MASK)
        ww.extend((w7p if prime else w7, w8p if prime else w8))
        ww.extend(fixed_w)
        branches.append((aa, ee, ww))
    (a, e, w), (ap, ep, wp) = branches
    if w[:4] != wp[:4]:
        return None
    if not row_ok(ROWS["W4"], w[4], wp[4]) or not row_ok(ROWS["W5"], w[5], wp[5]) or not row_ok(ROWS["W6"], w[6], wp[6]):
        return None
    if not relations_ok(w[4], relation_edges("W4")):
        return None
    if not relations_ok(w[5], relation_edges("W5")):
        return None
    if not relations_ok(w[6], relation_edges("W6")):
        return None
    return branches


def candidate_tails(branches, stats: dict | None = None):
    """Enumerate W14/W15 choices meeting the bridge-local Figure 6 conditions."""
    (a, e, _), (ap, ep, _) = branches
    tails = []
    e14_values = tuple(row_values(ROWS["E14"]))
    e15_values = tuple(row_values(ROWS["E15"]))
    w14_tail_counts = []
    for e14, e14p in e14_values:
        a14 = (e14 - a[10] + s0(a[13]) + maj(a[13], a[12], a[11])) & MASK
        a14p = (e14p - ap[10] + s0(ap[13]) + maj(ap[13], ap[12], ap[11])) & MASK
        w14 = (e14 - a[10] - e[10] - s1(e[13]) - ch(e[13], e[12], e[11]) - SHA256_K[14]) & MASK
        w14p = (e14p - ap[10] - ep[10] - s1(ep[13]) - ch(ep[13], ep[12], ep[11]) - SHA256_K[14]) & MASK
        if w14 != w14p or not row_ok(ROWS["A14"], a14, a14p):
            continue
        if not relations_ok(a14, relation_edges("A14")):
            continue
        if any(((a14 >> bit) & 1) != ((a[state_i] >> state_bit) & 1)
               for bit, state_i, state_bit in FIGURE6["relations"]["A14"]["same_as_state_bits"]):
            continue
        if any(((a14 >> bit) & 1) == ((a[state_i] >> state_bit) & 1)
               for bit, state_i, state_bit in FIGURE6["relations"]["A14"]["unequal_state_bits"]):
            continue
        tails_before = len(tails)
        for e15, e15p in e15_values:
            a15 = (e15 - a[11] + s0(a14) + maj(a14, a[13], a[12])) & MASK
            a15p = (e15p - ap[11] + s0(a14p) + maj(a14p, ap[13], ap[12])) & MASK
            w15 = (e15 - a[11] - e[11] - s1(e14) - ch(e14, e[13], e[12]) - SHA256_K[15]) & MASK
            w15p = (e15p - ap[11] - ep[11] - s1(e14p) - ch(e14p, ep[13], ep[12]) - SHA256_K[15]) & MASK
            if w15 != w15p or not row_ok(ROWS["A15"], a15, a15p):
                continue
            if any(((a15 >> bit) & 1) == ((a[state_i] >> state_bit) & 1)
                   for bit, state_i, state_bit in FIGURE6["relations"]["A15"]["unequal_state_bits"]):
                continue
            tails.append((w14, w15))
        w14_tail_counts.append(len(tails) - tails_before)
    if stats is not None:
        stats.update({
            "e14_row_values": len(e14_values),
            "e15_row_values_per_w14": len(e15_values),
            "w14_values_passing_all_a14_conditions": len(w14_tail_counts),
            "tails_per_passing_w14": w14_tail_counts,
        })
    return tails


def trace_from_block(cv, block_words):
    aa = {i: cv[-1 - i] for i in range(-4, 0)}
    ee = {i: cv[3 - i] for i in range(-4, 0)}
    ww = list(block_words)
    for i in range(16):
        ee[i] = (aa[i - 4] + ee[i - 4] + s1(ee[i - 1]) +
                 ch(ee[i - 1], ee[i - 2], ee[i - 3]) + SHA256_K[i] + ww[i]) & MASK
        aa[i] = (ee[i] - aa[i - 4] + s0(aa[i - 1]) +
                 maj(aa[i - 1], aa[i - 2], aa[i - 3])) & MASK
    return aa, ee, ww


def pack_words(words):
    return struct.pack(">16I", *words)


def digest_collision(cv, words, wp):
    return _compress("sha256", cv, pack_words(words), 32) == _compress("sha256", cv, pack_words(wp), 32)


def prefix_replays(cv, branches):
    for aa_expected, ee_expected, ww in branches:
        aa = {i: cv[-1 - i] for i in range(-4, 0)}
        ee = {i: cv[3 - i] for i in range(-4, 0)}
        for i in range(14):
            ee[i] = (aa[i - 4] + ee[i - 4] + s1(ee[i - 1]) +
                     ch(ee[i - 1], ee[i - 2], ee[i - 3]) + SHA256_K[i] + ww[i]) & MASK
            aa[i] = (ee[i] - aa[i - 4] + s0(aa[i - 1]) +
                     maj(aa[i - 1], aa[i - 2], aa[i - 3])) & MASK
        if any(aa[i] != aa_expected[i] for i in range(14)):
            return False
        if any(ee[i] != ee_expected[i] for i in range(14)):
            return False
    return True


def sample_bridges(table, wanted: int, seed: int):
    """Sample ideal uniform-CV states, conditioned on a table-key hit."""
    rng = random.Random(seed)
    keys = sorted(table)
    accepted = []
    accept_count = 0
    proposals = 1 << 22
    for _ in range(proposals):
        key = keys[rng.randrange(len(keys))]
        cv = (key, *(rng.getrandbits(32) for _ in range(7)))
        for record in table[key]:
            branches = derive_bridge(cv, record)
            if branches is not None:
                accept_count += 1
                if len(accepted) < wanted:
                    accepted.append((cv, record, branches))
                break
    return accepted, proposals, accept_count


def binomial_lower_one_sided(n: int, k: int, alpha: float) -> float:
    """Clopper-Pearson lower bound, via a stable binomial upper tail."""
    if k == 0:
        return 0.0

    def upper_tail(p: float) -> float:
        j = k
        log_term = (math.lgamma(n + 1) - math.lgamma(j + 1) -
                    math.lgamma(n - j + 1) + j * math.log(p) +
                    (n - j) * math.log1p(-p))
        term = math.exp(log_term)
        total = term
        while j < n:
            term *= ((n - j) / (j + 1)) * (p / (1.0 - p))
            j += 1
            total += term
            if term <= total * 1e-16:
                break
        return total

    lo, hi = 0.0, k / n
    for _ in range(80):
        mid = (lo + hi) / 2
        if upper_tail(mid) > alpha:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def reference_regression():
    cv = tuple(int(x, 16) for x in
               "f3b8f7ae 23d7ad68 c61d47d1 deda8ba2 8b60fb6e 96529cbd 3907ddc0 de6affc9".split())
    record = (0xab9c6465, 0xaa9d74ef, 0x6e417236, 0x6e497e36,
              0xd68fa526, 0xd68fa526, 0x29b2d81b, 0x09b2d81b, 0xacb11ef2)
    branches = derive_bridge(cv, record)
    if branches is None:
        raise AssertionError("repository C32 bridge regression does not pass the reproduced filter")
    tail_stats = {}
    tails = candidate_tails(branches, tail_stats)
    known_tail = (0xd2701ecc, 0x140976d1)
    words = branches[0][2][:14] + list(known_tail)
    words_p = branches[1][2][:14] + list(known_tail)
    return {
        "cv_words": [f"{x:08x}" for x in cv],
        "record": [f"{x:08x}" for x in record],
        "bridge_filter_passes": True,
        "candidate_tail_count": len(tails),
        "tail_enumeration": tail_stats,
        "candidate_tail_sha256": hashlib.sha256(
            b"".join(struct.pack(">II", *tail) for tail in tails)
        ).hexdigest(),
        "published_table3_tail_is_in_candidate_set": known_tail in set(tails),
        "published_table3_tail_c32_second_block_equal_from_this_cv": digest_collision(cv, words, words_p),
    }


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", help="challenge repository root; inferred when run inside repo")
    args = parser.parse_args()
    configure_repo(args.repo)
    started = time.perf_counter()
    table, table_stats = build_table()
    accepted, cv_draws, accept_count = sample_bridges(table, wanted=16, seed=20261004)
    tail_rng = random.Random(920260928)
    per_bridge = []
    for bridge_id, (cv, record, branches) in enumerate(accepted):
        start = time.perf_counter()
        tail_stats = {}
        tails = candidate_tails(branches, tail_stats)
        # A uniform-without-replacement sample from this bridge's complete
        # local candidate set. The size is capped to keep exact C32 checks cheap.
        sample_n = min(256, len(tails))
        indexes = sorted(tail_rng.sample(range(len(tails)), sample_n))
        hits = 0
        for idx in indexes:
            w14, w15 = tails[idx]
            words = branches[0][2][:14] + [w14, w15]
            words_p = branches[1][2][:14] + [w14, w15]
            hits += int(digest_collision(cv, words, words_p))
        per_bridge.append({
            "id": bridge_id,
            "cv_words": [f"{x:08x}" for x in cv],
            "table_key": f"{cv[0]:08x}",
            "record": [f"{x:08x}" for x in record],
            "candidate_tail_count": len(tails),
            "tail_enumeration": tail_stats,
            "candidate_tail_sha256": hashlib.sha256(
                b"".join(struct.pack(">II", *tail) for tail in tails)
            ).hexdigest(),
            "sample_size": sample_n,
            "sample_indexes": indexes,
            "sampled_c32_collisions": hits,
            "both_prefixes_replay_through_step_13": prefix_replays(cv, branches),
            "tail_build_and_sample_seconds": time.perf_counter() - start,
        })
    out = {
        "experiment": "per-bridge fixed-slice tail sample",
        "target": "sha256-r32-prefix-v1",
        "source": source_metadata(),
        "model": "CV is drawn uniformly from 256-bit states conditional on the fixed-slice key/filter; no first-block preimage is asserted",
        "sample_seeds": {"bridge_state": 20261004, "tail_index": 920260928},
        "seed_selection_record": "Seeds were inherited from the prior participant run. Whether they were fixed before any exploratory results or whether other seeds/slices were tried is not recorded; the sample is not a blinded holdout.",
        "table": table_stats,
        "conditional_acceptance_sample": {
            "seed": 20261004,
            "proposals": cv_draws,
            "accepted": accept_count,
            "accepted_rate": accept_count / cv_draws,
            "nominal_iid_one_sided_confidence": 0.999,
            "nominal_iid_conditional_rate_lower_99_9_percent": binomial_lower_one_sided(cv_draws, accept_count, 0.001),
            "key_fraction": table_stats["distinct_keys"] / (1 << 32),
            "nominal_iid_uniform_CV_q_lower_99_9_percent": (table_stats["distinct_keys"] / (1 << 32)) *
                                               binomial_lower_one_sided(cv_draws, accept_count, 0.001),
            "coverage_limit": "The interval is a nominal iid-uniform binomial diagnostic. The fixed seeded PRNG run does not establish iid sampling or calibrated coverage; its seed-selection chronology is not recorded.",
        },
        "known_c32_regression": reference_regression(),
        "sample": {
            "accepted_abstract_bridges_sampled_for_tail_checks": len(accepted),
            "conditional_cv_draws": cv_draws,
            "conditional_accepted_total": accept_count,
            "sampled_c32_second_block_checks": sum(x["sample_size"] for x in per_bridge),
            "sampled_c32_equalities": sum(x["sampled_c32_collisions"] for x in per_bridge),
            "prefix_replay_count": sum(bool(x["both_prefixes_replay_through_step_13"]) for x in per_bridge),
            "per_bridge": per_bridge,
        },
        "runtime_seconds": time.perf_counter() - started,
        "interpretation_limit": "This sample checks exact predicates for a reproducible conditional ideal-state sample. It does not estimate the 2^-27 to 2^-34 full-sweep event and does not prove the C32 chaining-value distribution."
    }
    output = HERE / "sha256-r32-tail-sample.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
~~~

### Embedded file: verification/sha256-r32-tail-sample.json

~~~json
{
  "experiment": "per-bridge fixed-slice tail sample",
  "target": "sha256-r32-prefix-v1",
  "source": {
    "challenge_commit": "fc56c3fa38ac40043d8291649c78148bc4872995",
    "target_profile": "sha256-r32-prefix-v1",
    "target_profile_sha256": "93d2e5d9ca93540633798d58cbab2d6d8447916db2b127e9abe71f45d14f6835",
    "reference_hash_functions_sha256": "514fa8ab8a461e4a41080efa27b4ba2a3b499eeedf0a2d2346e6562835d040f5",
    "program_sha256": "2fc6357e9aaaa078fc078ed42b34bdce4f1fe65a9fb9f37aac6bff00d7e5bce2",
    "bridge_sampler_sha256": "2fc6357e9aaaa078fc078ed42b34bdce4f1fe65a9fb9f37aac6bff00d7e5bce2",
    "figure6_conditions_sha256": "a8f9ed4cc356804f87bb8ce4986f751baf8ea4666f1a5dc3e468127eff6fc64e",
    "paper_inputs_sha256": "b30b7090712cb2b3c95990a4400abf45d3dfe620ffa4cea1fe89b5a523c19509",
    "python": "3.13.5 | packaged by Anaconda, Inc. | (main, Jun 12 2025, 11:23:37) [Clang 14.0.6 ]",
    "platform": "macOS-27.0-arm64-arm-64bit-Mach-O"
  },
  "model": "CV is drawn uniformly from 256-bit states conditional on the fixed-slice key/filter; no first-block preimage is asserted",
  "sample_seeds": {
    "bridge_state": 20261004,
    "tail_index": 920260928
  },
  "seed_selection_record": "Seeds were inherited from the prior participant run. Whether they were fixed before any exploratory results or whether other seeds/slices were tried is not recorded; the sample is not a blinded holdout.",
  "table": {
    "w8_admissible": 1048576,
    "w8_state_survivors": 44,
    "w7_admissible": 524288,
    "table_records": 593920,
    "distinct_keys": 408576,
    "max_records_per_key": 4,
    "table_bytes": 14254080,
    "table_sha256": "3cd961f8e0efe18027ec7192b4f0fa9f449659fdae14a5969fe3f6b821c8ebc7",
    "published_and_c32_regression_records_present": [
      true,
      true
    ]
  },
  "conditional_acceptance_sample": {
    "seed": 20261004,
    "proposals": 4194304,
    "accepted": 127,
    "accepted_rate": 3.0279159545898438e-05,
    "nominal_iid_one_sided_confidence": 0.999,
    "nominal_iid_conditional_rate_lower_99_9_percent": 2.2650315801907697e-05,
    "key_fraction": 9.512901306152344e-05,
    "nominal_iid_uniform_CV_q_lower_99_9_percent": 2.154702187767308e-09,
    "coverage_limit": "The interval is a nominal iid-uniform binomial diagnostic. The fixed seeded PRNG run does not establish iid sampling or calibrated coverage; its seed-selection chronology is not recorded."
  },
  "known_c32_regression": {
    "cv_words": [
      "f3b8f7ae",
      "23d7ad68",
      "c61d47d1",
      "deda8ba2",
      "8b60fb6e",
      "96529cbd",
      "3907ddc0",
      "de6affc9"
    ],
    "record": [
      "ab9c6465",
      "aa9d74ef",
      "6e417236",
      "6e497e36",
      "d68fa526",
      "d68fa526",
      "29b2d81b",
      "09b2d81b",
      "acb11ef2"
    ],
    "bridge_filter_passes": true,
    "candidate_tail_count": 196608,
    "tail_enumeration": {
      "e14_row_values": 256,
      "e15_row_values_per_w14": 32768,
      "w14_values_passing_all_a14_conditions": 12,
      "tails_per_passing_w14": [
        16384,
        16384,
        16384,
        16384,
        16384,
        16384,
        16384,
        16384,
        16384,
        16384,
        16384,
        16384
      ]
    },
    "candidate_tail_sha256": "ec59bb6beaab8473f3ce54e8a8a121f043ca2097e7e952e7946dff35975b8b1d",
    "published_table3_tail_is_in_candidate_set": true,
    "published_table3_tail_c32_second_block_equal_from_this_cv": false
  },
  "sample": {
    "accepted_abstract_bridges_sampled_for_tail_checks": 16,
    "conditional_cv_draws": 4194304,
    "conditional_accepted_total": 127,
    "sampled_c32_second_block_checks": 4096,
    "sampled_c32_equalities": 0,
    "prefix_replay_count": 16,
    "per_bridge": [
      {
        "id": 0,
        "cv_words": [
          "ba371553",
          "f7d4bb46",
          "c4a803f2",
          "8457c3bd",
          "f96b49c1",
          "e26e85ac",
          "cd20f7f6",
          "23824d01"
        ],
        "table_key": "ba371553",
        "record": [
          "e51e6520",
          "e41f75aa",
          "6e417016",
          "6e497c16",
          "9d0da44b",
          "9d0da44b",
          "29b2da3b",
          "09b2da3b",
          "acb12112"
        ],
        "candidate_tail_count": 196608,
        "tail_enumeration": {
          "e14_row_values": 256,
          "e15_row_values_per_w14": 32768,
          "w14_values_passing_all_a14_conditions": 12,
          "tails_per_passing_w14": [
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384
          ]
        },
        "candidate_tail_sha256": "ec59bb6beaab8473f3ce54e8a8a121f043ca2097e7e952e7946dff35975b8b1d",
        "sample_size": 256,
        "sample_indexes": [
          706,
          771,
          1371,
          1828,
          2877,
          3931,
          4800,
          4961,
          7932,
          8224,
          8442,
          9125,
          10143,
          10443,
          13404,
          13411,
          14257,
          15551,
          16472,
          16604,
          19868,
          20638,
          20815,
          22596,
          23787,
          24012,
          25128,
          25294,
          25517,
          27387,
          27504,
          27540,
          29184,
          29279,
          29735,
          30110,
          30215,
          30767,
          31022,
          31069,
          31375,
          31681,
          31884,
          32023,
          32127,
          32219,
          32655,
          33711,
          34891,
          35015,
          35341,
          35527,
          35582,
          36066,
          36297,
          36348,
          36873,
          38316,
          39730,
          40664,
          41462,
          41896,
          42295,
          43014,
          43183,
          44507,
          44668,
          45996,
          46984,
          47009,
          47129,
          47333,
          47914,
          48329,
          49279,
          49832,
          50445,
          50632,
          51455,
          52558,
          53256,
          53428,
          54115,
          54698,
          55120,
          55453,
          56142,
          56174,
          56340,
          56896,
          57190,
          58229,
          59383,
          59645,
          63413,
          65448,
          65768,
          66155,
          66910,
          66964,
          68895,
          70505,
          70615,
          70811,
          71512,
          72817,
          73071,
          74698,
          76151,
          76448,
          78810,
          78918,
          79002,
          82407,
          83377,
          83862,
          84613,
          84755,
          86124,
          88947,
          89135,
          89733,
          90243,
          90557,
          91204,
          91605,
          91992,
          92170,
          93208,
          94672,
          94833,
          95625,
          96514,
          96610,
          97377,
          97470,
          97632,
          100258,
          100674,
          100753,
          103207,
          103891,
          104421,
          105247,
          106063,
          106724,
          107136,
          107969,
          108305,
          108521,
          109095,
          109787,
          110595,
          110785,
          111358,
          111829,
          112180,
          112564,
          114430,
          115145,
          118084,
          118580,
          119308,
          121182,
          122745,
          123116,
          124083,
          124163,
          124223,
          124522,
          125229,
          126014,
          126228,
          126385,
          131081,
          131861,
          131894,
          135263,
          136496,
          136688,
          137389,
          137404,
          138277,
          138314,
          139903,
          140084,
          140298,
          140908,
          141700,
          142376,
          142639,
          143117,
          143230,
          143526,
          143547,
          144055,
          144378,
          144883,
          145177,
          145923,
          146481,
          149408,
          149717,
          150841,
          152832,
          152907,
          153426,
          153542,
          154918,
          156156,
          157870,
          158892,
          159250,
          162025,
          163392,
          163828,
          164754,
          164917,
          164957,
          165093,
          165774,
          166052,
          166387,
          166635,
          167662,
          167709,
          169148,
          169677,
          170114,
          171621,
          171655,
          172717,
          173102,
          173751,
          174166,
          174699,
          175745,
          179090,
          180385,
          180725,
          180748,
          181038,
          182735,
          184319,
          184772,
          185883,
          187834,
          189390,
          192045,
          192261,
          192475,
          193251,
          195557,
          195637,
          195943,
          196422
        ],
        "sampled_c32_collisions": 0,
        "both_prefixes_replay_through_step_13": true,
        "tail_build_and_sample_seconds": 1.9755291671026498
      },
      {
        "id": 1,
        "cv_words": [
          "0cd694ac",
          "0394f771",
          "d0f5b380",
          "5eb992eb",
          "f42b15a5",
          "6f4437e2",
          "7a2b2429",
          "d673f1bc"
        ],
        "table_key": "0cd694ac",
        "record": [
          "931ec771",
          "921fd7fb",
          "6ee17140",
          "6ee97d40",
          "efad4124",
          "efad4124",
          "2912d911",
          "0912d911",
          "ac111fe8"
        ],
        "candidate_tail_count": 196608,
        "tail_enumeration": {
          "e14_row_values": 256,
          "e15_row_values_per_w14": 32768,
          "w14_values_passing_all_a14_conditions": 12,
          "tails_per_passing_w14": [
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384
          ]
        },
        "candidate_tail_sha256": "ec59bb6beaab8473f3ce54e8a8a121f043ca2097e7e952e7946dff35975b8b1d",
        "sample_size": 256,
        "sample_indexes": [
          796,
          1714,
          2227,
          2344,
          2864,
          3134,
          3156,
          4836,
          6053,
          6971,
          7158,
          7388,
          7783,
          8371,
          8699,
          9609,
          11567,
          12332,
          12602,
          13495,
          14503,
          15479,
          16639,
          16664,
          18769,
          22554,
          24413,
          24643,
          24897,
          26933,
          27043,
          27897,
          29563,
          29977,
          30866,
          30897,
          31070,
          32221,
          33388,
          33485,
          34306,
          34538,
          35927,
          35933,
          36855,
          36938,
          38385,
          38617,
          39381,
          40138,
          41369,
          41560,
          42183,
          43338,
          43746,
          44681,
          46762,
          46920,
          47012,
          48161,
          48313,
          48578,
          48791,
          49297,
          49630,
          50378,
          52171,
          52859,
          53059,
          53568,
          53587,
          55017,
          55391,
          55499,
          55971,
          56333,
          56447,
          57765,
          57787,
          58546,
          59129,
          59687,
          61065,
          62084,
          65075,
          65655,
          65852,
          66072,
          67450,
          67492,
          68608,
          69403,
          69576,
          69952,
          70021,
          71360,
          71488,
          71584,
          72556,
          72660,
          73943,
          74046,
          74377,
          74894,
          75878,
          78275,
          78844,
          78933,
          81141,
          83704,
          83761,
          83796,
          83913,
          84632,
          84656,
          85115,
          85626,
          86459,
          86722,
          86922,
          89031,
          89358,
          89699,
          90555,
          90666,
          90922,
          91101,
          91404,
          92195,
          93462,
          93786,
          95253,
          96662,
          97371,
          97942,
          100493,
          101292,
          104004,
          104460,
          104683,
          105097,
          105195,
          105257,
          105550,
          107364,
          108038,
          109618,
          110203,
          111427,
          112061,
          112372,
          112981,
          113185,
          113485,
          113574,
          114759,
          115171,
          115785,
          115934,
          117488,
          119406,
          119503,
          121088,
          121710,
          122093,
          122705,
          123063,
          125011,
          125022,
          125104,
          126453,
          127720,
          128309,
          128891,
          129131,
          129838,
          129924,
          132428,
          132461,
          133258,
          133335,
          133739,
          134114,
          134753,
          136209,
          137152,
          137171,
          137545,
          138236,
          138486,
          138875,
          138907,
          138926,
          139004,
          139024,
          140040,
          140553,
          146138,
          146553,
          147052,
          148460,
          149014,
          149104,
          149210,
          149438,
          149980,
          153937,
          154850,
          154875,
          156575,
          160091,
          160209,
          160448,
          160462,
          161810,
          161998,
          162223,
          163169,
          163994,
          164973,
          166383,
          166446,
          166494,
          167404,
          167504,
          168960,
          169118,
          169309,
          169333,
          169465,
          170080,
          170822,
          172820,
          173309,
          174410,
          176710,
          176861,
          178355,
          178410,
          179740,
          181068,
          182467,
          183766,
          185172,
          185321,
          187903,
          188981,
          189615,
          190313,
          191496,
          192454,
          192463,
          193131,
          193767,
          194755,
          195726
        ],
        "sampled_c32_collisions": 0,
        "both_prefixes_replay_through_step_13": true,
        "tail_build_and_sample_seconds": 1.9645245000720024
      },
      {
        "id": 2,
        "cv_words": [
          "0ab714a9",
          "5f21dd89",
          "0b7deb9f",
          "d3b774dc",
          "c5c84fd2",
          "3f3215f9",
          "76ca5e6b",
          "f8de9c98"
        ],
        "table_key": "0ab714a9",
        "record": [
          "953e4774",
          "943f57fe",
          "6ee17140",
          "6ee97d40",
          "ed8dc121",
          "ed8dc121",
          "2912d911",
          "0912d911",
          "ac111fe8"
        ],
        "candidate_tail_count": 196608,
        "tail_enumeration": {
          "e14_row_values": 256,
          "e15_row_values_per_w14": 32768,
          "w14_values_passing_all_a14_conditions": 12,
          "tails_per_passing_w14": [
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384
          ]
        },
        "candidate_tail_sha256": "ec59bb6beaab8473f3ce54e8a8a121f043ca2097e7e952e7946dff35975b8b1d",
        "sample_size": 256,
        "sample_indexes": [
          145,
          4255,
          5580,
          9112,
          9425,
          10841,
          11138,
          11258,
          14234,
          14771,
          15282,
          15634,
          16139,
          16652,
          17040,
          18109,
          19753,
          20531,
          20662,
          21986,
          22048,
          22981,
          23049,
          24989,
          25691,
          26706,
          27803,
          29362,
          29812,
          31539,
          31584,
          31939,
          32846,
          34741,
          35257,
          36009,
          37622,
          38158,
          38477,
          40722,
          41077,
          41455,
          45694,
          46840,
          47297,
          47542,
          47827,
          48184,
          49386,
          49711,
          51734,
          51770,
          52101,
          52335,
          52789,
          54232,
          54761,
          55054,
          55252,
          57786,
          60136,
          63125,
          63843,
          64356,
          64979,
          64994,
          68482,
          68858,
          69573,
          70505,
          72520,
          73883,
          75082,
          75359,
          75460,
          75561,
          75640,
          76399,
          76514,
          76617,
          77676,
          78381,
          78444,
          78603,
          78830,
          79237,
          79395,
          80455,
          81520,
          81795,
          82947,
          83436,
          83882,
          85274,
          85540,
          86112,
          86366,
          87147,
          88238,
          88791,
          89774,
          90378,
          90766,
          91025,
          91734,
          92229,
          92637,
          93432,
          93565,
          93568,
          93917,
          95002,
          95113,
          95135,
          95726,
          96478,
          97120,
          97498,
          97554,
          97632,
          97700,
          98314,
          98599,
          100709,
          100782,
          100792,
          100926,
          103228,
          104217,
          104429,
          107849,
          109455,
          109508,
          111031,
          111489,
          111522,
          112936,
          112954,
          113881,
          114483,
          114630,
          116471,
          116681,
          117195,
          117395,
          117489,
          117603,
          118487,
          118841,
          119841,
          119925,
          120147,
          120453,
          122879,
          123190,
          123901,
          123902,
          124231,
          126782,
          126839,
          127083,
          128543,
          128689,
          129013,
          129199,
          129568,
          130454,
          130723,
          130901,
          130924,
          131726,
          132429,
          132943,
          135396,
          135481,
          136474,
          138666,
          139284,
          139664,
          139939,
          143339,
          143398,
          145329,
          145631,
          145690,
          146185,
          146591,
          147322,
          147582,
          148294,
          148579,
          150122,
          150949,
          152853,
          155506,
          156378,
          156814,
          158000,
          159177,
          161651,
          161851,
          161998,
          162232,
          162359,
          163266,
          163711,
          164597,
          164783,
          164786,
          164834,
          166584,
          168362,
          168949,
          171096,
          171622,
          171848,
          172189,
          172426,
          172648,
          173123,
          173222,
          173671,
          173773,
          173964,
          174599,
          174610,
          174855,
          176324,
          177130,
          177230,
          177612,
          178015,
          178028,
          179083,
          179480,
          180237,
          180346,
          181483,
          183429,
          183959,
          184179,
          184769,
          185537,
          186351,
          187958,
          188480,
          190925,
          191359,
          192517,
          192681,
          193743,
          193998,
          194013,
          194356,
          195293,
          195767
        ],
        "sampled_c32_collisions": 0,
        "both_prefixes_replay_through_step_13": true,
        "tail_build_and_sample_seconds": 2.089294208213687
      },
      {
        "id": 3,
        "cv_words": [
          "cc38b24d",
          "922dbfda",
          "90049b0a",
          "6b21d04b",
          "1c4e47e2",
          "08a76f43",
          "1951bd7e",
          "bb499314"
        ],
        "table_key": "cc38b24d",
        "record": [
          "d39cc630",
          "d29dd6ba",
          "6ec17120",
          "6ec97d20",
          "af0f4245",
          "af0f4245",
          "2932d931",
          "0932d931",
          "ac312008"
        ],
        "candidate_tail_count": 196608,
        "tail_enumeration": {
          "e14_row_values": 256,
          "e15_row_values_per_w14": 32768,
          "w14_values_passing_all_a14_conditions": 12,
          "tails_per_passing_w14": [
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384
          ]
        },
        "candidate_tail_sha256": "ec59bb6beaab8473f3ce54e8a8a121f043ca2097e7e952e7946dff35975b8b1d",
        "sample_size": 256,
        "sample_indexes": [
          129,
          494,
          1138,
          2123,
          2329,
          4269,
          5789,
          6183,
          6622,
          7217,
          7415,
          7726,
          8140,
          8258,
          8644,
          8773,
          9409,
          10269,
          11861,
          14707,
          17042,
          17103,
          18745,
          19446,
          19626,
          20979,
          24241,
          25228,
          26392,
          27150,
          27522,
          28430,
          28528,
          31595,
          32993,
          33112,
          34196,
          34315,
          34824,
          35288,
          35867,
          36271,
          37267,
          37285,
          38790,
          40854,
          41551,
          41728,
          41773,
          43479,
          45331,
          45408,
          45937,
          47096,
          47765,
          48889,
          48904,
          50945,
          50955,
          51086,
          51536,
          51764,
          52755,
          53393,
          54218,
          55037,
          55375,
          55563,
          55819,
          56896,
          57936,
          57962,
          59391,
          60226,
          61938,
          61988,
          62638,
          63416,
          63419,
          63662,
          63991,
          65272,
          65439,
          65519,
          66854,
          66919,
          67973,
          69586,
          70955,
          71402,
          71719,
          72018,
          72376,
          73570,
          73723,
          74130,
          74423,
          75265,
          75326,
          75402,
          76557,
          76783,
          77034,
          77922,
          78485,
          78531,
          78723,
          78873,
          79839,
          80336,
          80424,
          80854,
          81325,
          82652,
          83654,
          83772,
          84070,
          86196,
          86495,
          87612,
          88235,
          88519,
          88587,
          89176,
          89524,
          90590,
          92044,
          92230,
          92751,
          92802,
          93158,
          93252,
          93410,
          93626,
          95725,
          96044,
          96686,
          97328,
          97849,
          98942,
          99549,
          101099,
          102843,
          103150,
          103560,
          105572,
          109390,
          111340,
          111473,
          111668,
          111889,
          112648,
          112977,
          113584,
          114033,
          115016,
          116721,
          117220,
          117385,
          118552,
          119401,
          120646,
          121127,
          121537,
          122462,
          123506,
          123583,
          125102,
          127008,
          128197,
          128970,
          130461,
          133039,
          134558,
          134969,
          135814,
          136004,
          138042,
          138278,
          139487,
          142668,
          143221,
          145239,
          145901,
          145953,
          145984,
          146897,
          147084,
          147218,
          147440,
          147782,
          148145,
          148540,
          150655,
          151157,
          151216,
          151520,
          151961,
          153362,
          154403,
          156086,
          156142,
          159426,
          159472,
          159713,
          159991,
          160171,
          160648,
          160951,
          161874,
          161895,
          162066,
          163634,
          163803,
          165653,
          166593,
          166902,
          167039,
          167575,
          167622,
          168493,
          170506,
          170639,
          171374,
          172654,
          175586,
          175649,
          175736,
          176423,
          177682,
          178512,
          178898,
          179098,
          179424,
          180097,
          181430,
          183222,
          183881,
          183938,
          184404,
          185482,
          185698,
          188733,
          189208,
          190313,
          190944,
          191286,
          191857,
          191946,
          192497,
          192972,
          193126,
          193381,
          193428,
          195266,
          196224
        ],
        "sampled_c32_collisions": 0,
        "both_prefixes_replay_through_step_13": true,
        "tail_build_and_sample_seconds": 1.9809896249789745
      },
      {
        "id": 4,
        "cv_words": [
          "a3b699b7",
          "a6fcd990",
          "759e2bab",
          "91291e34",
          "f70ee394",
          "2bbd9698",
          "2eaf09d1",
          "c171c3b8"
        ],
        "table_key": "a3b699b7",
        "record": [
          "fb9ec264",
          "fa9fd2ee",
          "6e41723e",
          "6e497e3e",
          "868d472f",
          "868d472f",
          "29b2d813",
          "09b2d813",
          "acb11eea"
        ],
        "candidate_tail_count": 196608,
        "tail_enumeration": {
          "e14_row_values": 256,
          "e15_row_values_per_w14": 32768,
          "w14_values_passing_all_a14_conditions": 12,
          "tails_per_passing_w14": [
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384
          ]
        },
        "candidate_tail_sha256": "ec59bb6beaab8473f3ce54e8a8a121f043ca2097e7e952e7946dff35975b8b1d",
        "sample_size": 256,
        "sample_indexes": [
          65,
          1210,
          2043,
          4641,
          5719,
          7154,
          8539,
          8703,
          11177,
          11567,
          13303,
          13953,
          15048,
          15452,
          15762,
          16184,
          18072,
          18276,
          21271,
          21745,
          21966,
          23080,
          28357,
          29950,
          31047,
          31222,
          31583,
          31727,
          32646,
          33123,
          33578,
          34952,
          38469,
          39777,
          40585,
          41141,
          41629,
          42017,
          42195,
          42276,
          44103,
          45021,
          45189,
          45761,
          45853,
          47220,
          49848,
          49894,
          50183,
          50584,
          51011,
          52203,
          53794,
          54114,
          55192,
          55643,
          55957,
          58311,
          58666,
          58845,
          59009,
          59931,
          60446,
          60727,
          60884,
          61316,
          61599,
          61854,
          62261,
          62578,
          62947,
          63328,
          63375,
          64097,
          64177,
          65637,
          66097,
          66513,
          66972,
          67272,
          67980,
          69218,
          69609,
          69715,
          70291,
          71714,
          74887,
          75035,
          75094,
          77618,
          77654,
          77743,
          78770,
          79720,
          80487,
          83465,
          84807,
          85086,
          85249,
          85898,
          85918,
          86664,
          87241,
          87579,
          88000,
          89007,
          89514,
          89983,
          91218,
          91889,
          92257,
          92385,
          94136,
          94624,
          96176,
          96529,
          96967,
          97278,
          97510,
          97551,
          98058,
          100411,
          100912,
          101108,
          102773,
          104849,
          105714,
          106490,
          106635,
          107293,
          108609,
          108622,
          108925,
          110395,
          110823,
          110921,
          111036,
          111863,
          112720,
          112979,
          113296,
          113481,
          114210,
          114971,
          115243,
          115670,
          115776,
          116301,
          116325,
          116571,
          117322,
          117334,
          117393,
          119103,
          120057,
          120353,
          120479,
          120524,
          121210,
          121819,
          123015,
          123127,
          124596,
          125202,
          125252,
          126166,
          127942,
          128118,
          128139,
          130174,
          131895,
          133901,
          134230,
          134267,
          134709,
          134973,
          135144,
          135184,
          136121,
          136259,
          137715,
          139572,
          142266,
          142415,
          142808,
          142915,
          143204,
          143649,
          145824,
          145928,
          146816,
          147008,
          147065,
          147591,
          149634,
          149710,
          150801,
          151515,
          151925,
          154239,
          154475,
          155528,
          155752,
          156353,
          156462,
          158151,
          159644,
          160464,
          160556,
          161703,
          161963,
          162242,
          162281,
          162375,
          163135,
          164328,
          168514,
          170117,
          170382,
          170482,
          170685,
          171009,
          171775,
          173215,
          173506,
          174036,
          174311,
          174534,
          176816,
          176929,
          177626,
          177758,
          178265,
          178747,
          179463,
          179484,
          179753,
          181095,
          183684,
          184885,
          185022,
          185358,
          185376,
          185858,
          186033,
          186678,
          187507,
          188270,
          188423,
          188765,
          188967,
          189649,
          191036,
          191565,
          192059,
          194120
        ],
        "sampled_c32_collisions": 0,
        "both_prefixes_replay_through_step_13": true,
        "tail_build_and_sample_seconds": 1.9878508751280606
      },
      {
        "id": 5,
        "cv_words": [
          "ea34f70b",
          "f8f1c0ed",
          "e814a889",
          "6c08606f",
          "341e1fcb",
          "ec287be9",
          "b1f88b1b",
          "c2fc58d0"
        ],
        "table_key": "ea34f70b",
        "record": [
          "b51e6570",
          "b41f75fa",
          "6e43721e",
          "6e4b7e1e",
          "cd0da403",
          "cd0da403",
          "29b0d833",
          "09b0d833",
          "acaf1f0a"
        ],
        "candidate_tail_count": 196608,
        "tail_enumeration": {
          "e14_row_values": 256,
          "e15_row_values_per_w14": 32768,
          "w14_values_passing_all_a14_conditions": 12,
          "tails_per_passing_w14": [
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384
          ]
        },
        "candidate_tail_sha256": "ec59bb6beaab8473f3ce54e8a8a121f043ca2097e7e952e7946dff35975b8b1d",
        "sample_size": 256,
        "sample_indexes": [
          1362,
          1910,
          2797,
          3136,
          3427,
          3482,
          3675,
          3984,
          4108,
          4692,
          5280,
          6104,
          7244,
          7477,
          8494,
          8776,
          9266,
          9749,
          10107,
          10757,
          10979,
          11348,
          12054,
          14390,
          14467,
          15264,
          16454,
          17356,
          17428,
          17814,
          19324,
          19743,
          20131,
          24171,
          27800,
          27984,
          29778,
          30479,
          30812,
          32174,
          32371,
          32479,
          32537,
          32638,
          32784,
          32901,
          33077,
          33767,
          34109,
          34488,
          35254,
          36301,
          36832,
          42152,
          43976,
          43982,
          44077,
          44501,
          44833,
          45189,
          46110,
          46651,
          46938,
          47734,
          47854,
          48144,
          49356,
          50122,
          50890,
          51162,
          51431,
          54000,
          56262,
          57800,
          58079,
          59059,
          59937,
          60819,
          61867,
          62569,
          63766,
          64646,
          65263,
          66985,
          66986,
          67823,
          69153,
          69197,
          71755,
          71877,
          71969,
          74115,
          74891,
          76308,
          76699,
          79914,
          80053,
          80327,
          81091,
          81394,
          81431,
          82932,
          84660,
          86946,
          88494,
          88609,
          89042,
          90406,
          91261,
          91341,
          92400,
          93252,
          94529,
          96194,
          98033,
          99036,
          99455,
          99606,
          100878,
          102095,
          102761,
          103365,
          103563,
          103574,
          104039,
          104722,
          105650,
          105975,
          106833,
          107114,
          107516,
          108412,
          108530,
          109188,
          109489,
          110712,
          110857,
          111686,
          111720,
          112334,
          113537,
          114771,
          117257,
          117400,
          117763,
          118321,
          119869,
          120556,
          120710,
          122566,
          122812,
          124010,
          124277,
          126300,
          126453,
          127507,
          128361,
          128767,
          129092,
          130188,
          130197,
          130894,
          131523,
          131851,
          132746,
          132826,
          132964,
          133589,
          134671,
          134837,
          135655,
          135751,
          137677,
          137738,
          138707,
          139151,
          139373,
          139633,
          139718,
          139886,
          140249,
          140277,
          140554,
          140614,
          141818,
          142453,
          142586,
          143095,
          145917,
          146113,
          146891,
          148205,
          148530,
          148681,
          151117,
          153656,
          154214,
          155289,
          155446,
          155671,
          155781,
          156942,
          157921,
          158289,
          158348,
          158390,
          159056,
          160071,
          160740,
          160746,
          161272,
          162004,
          162855,
          163522,
          165287,
          165535,
          168243,
          168558,
          168641,
          169260,
          169847,
          170061,
          171108,
          172022,
          172023,
          172662,
          172792,
          172880,
          173145,
          173166,
          173186,
          175700,
          176251,
          176657,
          178186,
          178276,
          179741,
          180401,
          180623,
          181380,
          181828,
          182268,
          186035,
          186083,
          186669,
          187309,
          188057,
          189065,
          189704,
          190214,
          190337,
          190487,
          190889,
          191011,
          191662,
          193834
        ],
        "sampled_c32_collisions": 0,
        "both_prefixes_replay_through_step_13": true,
        "tail_build_and_sample_seconds": 1.9665111671201885
      },
      {
        "id": 6,
        "cv_words": [
          "1435150a",
          "ce83d26f",
          "a4fff75c",
          "ef7b1e75",
          "eb0fa17a",
          "7dfefd4e",
          "2b66dacc",
          "c91cdcfd"
        ],
        "table_key": "1435150a",
        "record": [
          "8b1e4771",
          "8a1f57fb",
          "6e43721e",
          "6e4b7e1e",
          "f70dc202",
          "f70dc202",
          "29b0d833",
          "09b0d833",
          "acaf1f0a"
        ],
        "candidate_tail_count": 196608,
        "tail_enumeration": {
          "e14_row_values": 256,
          "e15_row_values_per_w14": 32768,
          "w14_values_passing_all_a14_conditions": 12,
          "tails_per_passing_w14": [
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384
          ]
        },
        "candidate_tail_sha256": "ec59bb6beaab8473f3ce54e8a8a121f043ca2097e7e952e7946dff35975b8b1d",
        "sample_size": 256,
        "sample_indexes": [
          1194,
          2025,
          2149,
          3041,
          3956,
          4690,
          5181,
          7116,
          7336,
          7575,
          7637,
          8051,
          8931,
          9111,
          9727,
          9924,
          10496,
          11793,
          12335,
          13641,
          16133,
          16964,
          17586,
          17824,
          18397,
          18451,
          18935,
          20462,
          21659,
          21954,
          21967,
          22492,
          24125,
          24351,
          25346,
          25626,
          25936,
          26357,
          27507,
          28191,
          29284,
          29760,
          30137,
          30990,
          32240,
          32696,
          32818,
          32966,
          33352,
          34548,
          34844,
          34845,
          36819,
          36889,
          37136,
          37544,
          38345,
          38683,
          38714,
          39637,
          40224,
          41648,
          41983,
          41991,
          42217,
          42249,
          42370,
          43379,
          43811,
          43831,
          44787,
          45167,
          46163,
          47865,
          49445,
          50396,
          50735,
          51420,
          51661,
          53876,
          55603,
          59882,
          60028,
          60152,
          60999,
          61032,
          61552,
          61852,
          62002,
          62535,
          63986,
          66305,
          67113,
          68076,
          68807,
          69815,
          70264,
          70368,
          72315,
          72554,
          73242,
          74740,
          75436,
          75813,
          79912,
          79950,
          84321,
          84333,
          84853,
          85231,
          85254,
          85700,
          85768,
          86850,
          87661,
          87842,
          88430,
          89400,
          89665,
          90427,
          90732,
          91452,
          92501,
          92750,
          93383,
          93515,
          93560,
          93695,
          94764,
          95329,
          96004,
          97104,
          98079,
          99175,
          99955,
          99963,
          100139,
          100687,
          101634,
          101647,
          102048,
          102296,
          102776,
          102889,
          104736,
          105545,
          107410,
          107864,
          108622,
          110025,
          110503,
          111116,
          111735,
          111916,
          113699,
          113838,
          114032,
          114564,
          116285,
          117358,
          117612,
          118203,
          119351,
          119501,
          121367,
          121742,
          122177,
          122557,
          122631,
          123765,
          124261,
          126299,
          127996,
          128540,
          128757,
          132301,
          132356,
          132944,
          133135,
          133762,
          135379,
          135647,
          137503,
          138512,
          140072,
          140157,
          140388,
          140707,
          140899,
          141132,
          141161,
          142750,
          142979,
          143349,
          145804,
          146317,
          146651,
          147817,
          148137,
          150798,
          151278,
          151371,
          152053,
          152383,
          152550,
          156604,
          156983,
          157671,
          157845,
          157948,
          158265,
          161179,
          161446,
          163688,
          163733,
          164241,
          164402,
          164975,
          165417,
          167520,
          168034,
          168153,
          169259,
          170781,
          171450,
          172169,
          172321,
          173078,
          173339,
          173512,
          174911,
          174992,
          175154,
          178003,
          178073,
          178515,
          178960,
          179488,
          179536,
          180072,
          180529,
          181864,
          182337,
          183768,
          184385,
          186394,
          186529,
          186537,
          188365,
          188522,
          188759,
          190001,
          192378,
          193216,
          194924,
          196231
        ],
        "sampled_c32_collisions": 0,
        "both_prefixes_replay_through_step_13": true,
        "tail_build_and_sample_seconds": 1.9807563750073314
      },
      {
        "id": 7,
        "cv_words": [
          "fc3714ae",
          "e3dee77f",
          "ab372335",
          "466f007a",
          "55bcf0c8",
          "e62c9050",
          "ba202138",
          "1c4f13f9"
        ],
        "table_key": "fc3714ae",
        "record": [
          "a31c4765",
          "a21d57ef",
          "6e437236",
          "6e4b7e36",
          "df0fc226",
          "df0fc226",
          "29b0d81b",
          "09b0d81b",
          "acaf1ef2"
        ],
        "candidate_tail_count": 196608,
        "tail_enumeration": {
          "e14_row_values": 256,
          "e15_row_values_per_w14": 32768,
          "w14_values_passing_all_a14_conditions": 12,
          "tails_per_passing_w14": [
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384
          ]
        },
        "candidate_tail_sha256": "ec59bb6beaab8473f3ce54e8a8a121f043ca2097e7e952e7946dff35975b8b1d",
        "sample_size": 256,
        "sample_indexes": [
          958,
          2120,
          2721,
          3261,
          3337,
          3746,
          5126,
          5607,
          6398,
          6819,
          6866,
          7210,
          7614,
          7658,
          9560,
          10619,
          11182,
          11986,
          12115,
          12974,
          14492,
          14556,
          15112,
          15216,
          16958,
          17536,
          18700,
          19380,
          19542,
          19748,
          19765,
          20430,
          21565,
          23614,
          24214,
          25303,
          25308,
          26323,
          26463,
          27571,
          28441,
          29257,
          29337,
          31010,
          32409,
          34972,
          35073,
          35393,
          38076,
          38822,
          39667,
          40897,
          41251,
          41371,
          41605,
          42613,
          42723,
          43226,
          43437,
          45448,
          45673,
          45764,
          47078,
          48164,
          48764,
          48981,
          50061,
          50482,
          50557,
          50723,
          51543,
          52441,
          53584,
          54108,
          54483,
          54657,
          55741,
          57330,
          58213,
          60549,
          60689,
          61412,
          61889,
          62861,
          63003,
          63006,
          64659,
          66174,
          66896,
          69873,
          70164,
          70510,
          70900,
          70919,
          72865,
          73761,
          73856,
          77951,
          78113,
          79265,
          79748,
          82026,
          82243,
          82410,
          82483,
          83019,
          84109,
          84638,
          85045,
          85671,
          87154,
          88224,
          89070,
          90304,
          90747,
          91712,
          92042,
          92371,
          92804,
          94521,
          94571,
          94948,
          95692,
          96005,
          96337,
          96576,
          96738,
          97626,
          98268,
          98489,
          102739,
          104517,
          107264,
          107434,
          107499,
          107914,
          110452,
          110900,
          111170,
          112700,
          113118,
          113551,
          114549,
          114675,
          115764,
          116897,
          119221,
          119523,
          120759,
          120959,
          122133,
          122376,
          122752,
          123315,
          123447,
          123952,
          124170,
          124420,
          125631,
          126421,
          126542,
          126719,
          127530,
          127936,
          129158,
          129161,
          129296,
          129466,
          129943,
          130410,
          130728,
          132516,
          133179,
          133502,
          133882,
          134395,
          135572,
          136421,
          136963,
          137040,
          139270,
          139917,
          142698,
          142869,
          144732,
          144926,
          145283,
          145585,
          145759,
          145818,
          146097,
          146141,
          146242,
          146667,
          147448,
          147613,
          147943,
          148719,
          150406,
          153437,
          153593,
          154361,
          154605,
          157553,
          157995,
          158678,
          159376,
          159712,
          160065,
          160750,
          161873,
          161895,
          162958,
          163105,
          165168,
          165455,
          166443,
          167001,
          168983,
          170842,
          171136,
          171486,
          172638,
          172971,
          173710,
          174950,
          176157,
          177773,
          177913,
          179763,
          179804,
          179847,
          180349,
          181381,
          182739,
          183325,
          183482,
          183882,
          184068,
          186025,
          186395,
          186433,
          186952,
          187144,
          187349,
          187757,
          189348,
          190870,
          190982,
          191102,
          192277,
          193304,
          194976,
          195539,
          196022,
          196597
        ],
        "sampled_c32_collisions": 0,
        "both_prefixes_replay_through_step_13": true,
        "tail_build_and_sample_seconds": 1.9679149589501321
      },
      {
        "id": 8,
        "cv_words": [
          "fab6b2f5",
          "a84cfe83",
          "da3642a8",
          "27f159f2",
          "4865c2e5",
          "b5bcda0c",
          "7e3eb57e",
          "275118f0"
        ],
        "table_key": "fab6b2f5",
        "record": [
          "a51ec720",
          "a41fd7aa",
          "6ec17038",
          "6ec97c38",
          "dd8d426d",
          "dd8d426d",
          "2932da19",
          "0932da19",
          "ac3120f0"
        ],
        "candidate_tail_count": 196608,
        "tail_enumeration": {
          "e14_row_values": 256,
          "e15_row_values_per_w14": 32768,
          "w14_values_passing_all_a14_conditions": 12,
          "tails_per_passing_w14": [
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384
          ]
        },
        "candidate_tail_sha256": "ec59bb6beaab8473f3ce54e8a8a121f043ca2097e7e952e7946dff35975b8b1d",
        "sample_size": 256,
        "sample_indexes": [
          56,
          945,
          1868,
          3885,
          4959,
          5277,
          6554,
          8518,
          9397,
          11814,
          12324,
          12462,
          13474,
          16725,
          17951,
          17971,
          19304,
          19497,
          22443,
          22504,
          23208,
          24478,
          25719,
          25817,
          29078,
          29178,
          31115,
          32013,
          32114,
          33218,
          33974,
          34462,
          35746,
          36003,
          36187,
          36553,
          36643,
          36669,
          37188,
          37751,
          39758,
          39832,
          40075,
          40346,
          40449,
          40609,
          42269,
          42392,
          42467,
          42546,
          42772,
          44113,
          44671,
          44710,
          46138,
          47205,
          48735,
          49305,
          49427,
          49521,
          50210,
          50500,
          52265,
          52922,
          53204,
          53314,
          53412,
          53706,
          54653,
          56106,
          57266,
          57641,
          57722,
          58038,
          58061,
          58752,
          59785,
          59835,
          60020,
          61608,
          63166,
          63768,
          63913,
          65143,
          65774,
          67231,
          67237,
          67328,
          67593,
          67626,
          67631,
          67912,
          68647,
          69805,
          71815,
          71910,
          71933,
          72231,
          72694,
          72781,
          75134,
          75786,
          75989,
          78138,
          78701,
          78703,
          78885,
          79230,
          80379,
          82344,
          84825,
          87072,
          87163,
          87677,
          88895,
          89469,
          89700,
          89950,
          90640,
          91192,
          91963,
          92598,
          92696,
          96834,
          96918,
          97221,
          97250,
          97660,
          99093,
          100170,
          101289,
          102573,
          103308,
          104739,
          106743,
          107300,
          107411,
          107506,
          107820,
          108182,
          110690,
          112202,
          112741,
          112748,
          113187,
          113466,
          113526,
          113657,
          114289,
          114676,
          114693,
          115391,
          115862,
          115956,
          117048,
          119036,
          119525,
          119681,
          120633,
          121129,
          124144,
          124266,
          125177,
          125929,
          126747,
          126803,
          126885,
          127060,
          127760,
          127963,
          130322,
          131722,
          131756,
          132548,
          133001,
          133764,
          135559,
          136045,
          137151,
          137792,
          138396,
          139558,
          139936,
          140079,
          141447,
          142338,
          142911,
          143020,
          144842,
          146014,
          146995,
          147662,
          148102,
          148136,
          148224,
          148918,
          149490,
          150052,
          150914,
          151126,
          151269,
          151769,
          154882,
          155668,
          156174,
          157509,
          157794,
          157869,
          159696,
          159906,
          162216,
          162372,
          163871,
          164125,
          164212,
          164374,
          165192,
          165670,
          166494,
          167644,
          167674,
          168011,
          168245,
          168330,
          169810,
          172759,
          174153,
          174293,
          174349,
          176009,
          176349,
          177235,
          177266,
          177630,
          177698,
          178298,
          178431,
          178935,
          180295,
          180485,
          180672,
          180685,
          181357,
          184676,
          185163,
          185806,
          186486,
          187534,
          187805,
          189585,
          191400,
          192531,
          192611,
          194526,
          195207,
          196205
        ],
        "sampled_c32_collisions": 0,
        "both_prefixes_replay_through_step_13": true,
        "tail_build_and_sample_seconds": 1.9664708748459816
      },
      {
        "id": 9,
        "cv_words": [
          "1ad698a8",
          "90b290b9",
          "844e9a8b",
          "0121db69",
          "d4b198b2",
          "f44f3365",
          "9ba3de0f",
          "c405e2c8"
        ],
        "table_key": "1ad698a8",
        "record": [
          "851cc375",
          "841dd3ff",
          "6ee37140",
          "6eeb7d40",
          "fdaf4520",
          "fdaf4520",
          "2910d911",
          "0910d911",
          "ac0f1fe8"
        ],
        "candidate_tail_count": 196608,
        "tail_enumeration": {
          "e14_row_values": 256,
          "e15_row_values_per_w14": 32768,
          "w14_values_passing_all_a14_conditions": 12,
          "tails_per_passing_w14": [
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384
          ]
        },
        "candidate_tail_sha256": "ec59bb6beaab8473f3ce54e8a8a121f043ca2097e7e952e7946dff35975b8b1d",
        "sample_size": 256,
        "sample_indexes": [
          612,
          1498,
          1886,
          3623,
          4885,
          5292,
          5770,
          5910,
          6002,
          6194,
          6896,
          8862,
          9550,
          9771,
          10339,
          11625,
          11670,
          12153,
          13229,
          15683,
          15816,
          16279,
          16297,
          17115,
          17324,
          17647,
          20099,
          22173,
          23209,
          25089,
          25486,
          25579,
          26286,
          26912,
          28583,
          29684,
          30132,
          30481,
          34648,
          35227,
          35271,
          37850,
          41959,
          42450,
          42467,
          44309,
          44952,
          45105,
          45910,
          46790,
          47032,
          47141,
          47461,
          47652,
          47893,
          47908,
          48595,
          48615,
          48645,
          48835,
          49279,
          49325,
          49415,
          49717,
          50466,
          50988,
          52946,
          53450,
          54964,
          55279,
          55316,
          55342,
          57381,
          59632,
          61559,
          62056,
          62968,
          64996,
          65822,
          66175,
          66199,
          66538,
          66855,
          66862,
          68422,
          69489,
          69976,
          71697,
          71752,
          71923,
          71981,
          72021,
          72402,
          73476,
          74278,
          74691,
          76255,
          76630,
          76635,
          76969,
          77154,
          78695,
          78708,
          79356,
          79427,
          79490,
          79569,
          79826,
          83366,
          83557,
          84108,
          84343,
          84386,
          84628,
          85495,
          87743,
          88554,
          88901,
          89187,
          90120,
          90219,
          92445,
          92979,
          93270,
          94176,
          95304,
          95763,
          95815,
          96299,
          96589,
          96771,
          97025,
          98794,
          99447,
          99891,
          100978,
          101186,
          102035,
          102055,
          103004,
          103848,
          105636,
          105885,
          106859,
          107168,
          108474,
          109829,
          110685,
          111359,
          111497,
          113672,
          114311,
          114821,
          115366,
          115803,
          116162,
          116310,
          116699,
          117519,
          118002,
          118451,
          118496,
          120675,
          121008,
          121042,
          121428,
          123655,
          124730,
          125718,
          126564,
          127322,
          127443,
          128652,
          128981,
          129889,
          130260,
          131301,
          132364,
          132982,
          134608,
          136846,
          137559,
          138773,
          142020,
          143866,
          145945,
          146034,
          146829,
          147357,
          147507,
          148205,
          148255,
          148900,
          151220,
          153128,
          153242,
          155627,
          156919,
          157418,
          157565,
          158141,
          159407,
          160949,
          161575,
          162154,
          164142,
          165024,
          165629,
          166220,
          167139,
          168314,
          169194,
          171304,
          172224,
          175986,
          177026,
          178294,
          178599,
          179246,
          179949,
          180183,
          180310,
          180807,
          181697,
          182146,
          182280,
          182344,
          182374,
          182833,
          182994,
          183164,
          183748,
          184387,
          184482,
          184491,
          184860,
          185112,
          185620,
          186819,
          188477,
          188906,
          188945,
          188961,
          189259,
          189305,
          189408,
          190184,
          190420,
          191055,
          193128,
          194582,
          194683,
          194994,
          195786,
          196039,
          196418
        ],
        "sampled_c32_collisions": 0,
        "both_prefixes_replay_through_step_13": true,
        "tail_build_and_sample_seconds": 1.9678697078488767
      },
      {
        "id": 10,
        "cv_words": [
          "cc353814",
          "420f0bbb",
          "be4b0ed0",
          "cdc6397f",
          "4de8d2cf",
          "8a059633",
          "d9d74639",
          "855bf39f"
        ],
        "table_key": "cc353814",
        "record": [
          "d39e4261",
          "d29f52eb",
          "6ec37018",
          "6ecb7c18",
          "af0dc70c",
          "af0dc70c",
          "2930da39",
          "0930da39",
          "ac2f2110"
        ],
        "candidate_tail_count": 196608,
        "tail_enumeration": {
          "e14_row_values": 256,
          "e15_row_values_per_w14": 32768,
          "w14_values_passing_all_a14_conditions": 12,
          "tails_per_passing_w14": [
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384
          ]
        },
        "candidate_tail_sha256": "ec59bb6beaab8473f3ce54e8a8a121f043ca2097e7e952e7946dff35975b8b1d",
        "sample_size": 256,
        "sample_indexes": [
          419,
          1745,
          3961,
          4207,
          4816,
          4901,
          5824,
          6412,
          9992,
          13521,
          14298,
          14771,
          15365,
          15482,
          16169,
          18520,
          19899,
          20064,
          23034,
          23731,
          27645,
          29297,
          29979,
          32116,
          35785,
          35881,
          36464,
          37125,
          37331,
          37795,
          37940,
          38352,
          38961,
          40775,
          40843,
          42621,
          43636,
          44285,
          44348,
          45293,
          45801,
          45996,
          46583,
          48663,
          48918,
          49486,
          49699,
          50022,
          50171,
          51415,
          51685,
          54093,
          54491,
          54875,
          55803,
          56580,
          56989,
          57441,
          58090,
          58607,
          58834,
          59485,
          59720,
          59943,
          60065,
          60076,
          60088,
          60938,
          61562,
          62890,
          62916,
          63434,
          65708,
          65738,
          65739,
          66038,
          66400,
          68115,
          68657,
          69245,
          69863,
          70227,
          70940,
          72264,
          72575,
          75288,
          75725,
          76442,
          76448,
          76898,
          77432,
          77901,
          77984,
          78071,
          79040,
          80066,
          80318,
          80965,
          81311,
          81716,
          83005,
          83351,
          84148,
          84318,
          84896,
          85606,
          86568,
          87640,
          88360,
          88395,
          90232,
          91576,
          92162,
          92966,
          93868,
          94159,
          94483,
          94574,
          94580,
          95468,
          97968,
          99453,
          99929,
          100164,
          103052,
          103141,
          104006,
          104254,
          104631,
          104946,
          104953,
          105188,
          105732,
          106179,
          106962,
          107155,
          109756,
          110252,
          111149,
          111796,
          111861,
          112146,
          112706,
          113825,
          114331,
          114369,
          115974,
          116122,
          117418,
          119006,
          120224,
          120427,
          121498,
          123144,
          124766,
          127709,
          128359,
          129318,
          129733,
          130122,
          130535,
          130997,
          132308,
          132721,
          133656,
          133789,
          135294,
          136003,
          136064,
          136674,
          137002,
          137134,
          137224,
          137832,
          140968,
          141414,
          141655,
          141764,
          141939,
          143243,
          144822,
          146263,
          146484,
          146768,
          148326,
          148514,
          149036,
          149212,
          151685,
          151849,
          152240,
          152282,
          153286,
          153616,
          154597,
          154779,
          155325,
          155554,
          155784,
          155918,
          158375,
          158602,
          159317,
          160328,
          161416,
          162020,
          162178,
          162293,
          162937,
          163217,
          164162,
          164680,
          165299,
          165399,
          165876,
          165883,
          167101,
          167487,
          167495,
          168680,
          169179,
          169330,
          169457,
          170268,
          170725,
          171915,
          172658,
          172809,
          173793,
          174177,
          174683,
          175123,
          175563,
          175811,
          176556,
          177138,
          180860,
          181015,
          182275,
          182888,
          183993,
          185295,
          185803,
          187110,
          187374,
          187660,
          188368,
          188552,
          188859,
          189007,
          190635,
          190857,
          191137,
          191145,
          194548,
          195256
        ],
        "sampled_c32_collisions": 0,
        "both_prefixes_replay_through_step_13": true,
        "tail_build_and_sample_seconds": 1.9638075840193778
      },
      {
        "id": 11,
        "cv_words": [
          "fcb73315",
          "6d38f311",
          "62b4e6aa",
          "7f00cd51",
          "558219cc",
          "94e1bed4",
          "fa4e3779",
          "60cd8fd8"
        ],
        "table_key": "fcb73315",
        "record": [
          "a31e4760",
          "a21f57ea",
          "6ec17018",
          "6ec97c18",
          "df8dc20d",
          "df8dc20d",
          "2932da39",
          "0932da39",
          "ac312110"
        ],
        "candidate_tail_count": 196608,
        "tail_enumeration": {
          "e14_row_values": 256,
          "e15_row_values_per_w14": 32768,
          "w14_values_passing_all_a14_conditions": 12,
          "tails_per_passing_w14": [
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384
          ]
        },
        "candidate_tail_sha256": "ec59bb6beaab8473f3ce54e8a8a121f043ca2097e7e952e7946dff35975b8b1d",
        "sample_size": 256,
        "sample_indexes": [
          64,
          253,
          520,
          1364,
          1524,
          2580,
          3403,
          5242,
          5727,
          6081,
          6276,
          6494,
          7297,
          7831,
          8709,
          9649,
          10230,
          10912,
          11957,
          12233,
          12258,
          12457,
          13573,
          14849,
          15474,
          16257,
          16517,
          16844,
          16856,
          19052,
          19500,
          20610,
          20690,
          22478,
          27385,
          28008,
          28935,
          29572,
          31595,
          32316,
          32796,
          32879,
          33456,
          33975,
          34289,
          35523,
          37531,
          37613,
          38597,
          38760,
          39560,
          42822,
          43365,
          44924,
          45299,
          45407,
          45536,
          46421,
          46642,
          46797,
          48136,
          48915,
          52791,
          52860,
          52896,
          53528,
          55613,
          56316,
          57558,
          57667,
          59988,
          60444,
          60621,
          60779,
          61220,
          61552,
          62107,
          63640,
          63761,
          64755,
          64930,
          65137,
          65403,
          66832,
          68130,
          68985,
          69454,
          70972,
          71531,
          71679,
          71952,
          72517,
          72729,
          73947,
          74035,
          75461,
          75758,
          75906,
          77080,
          77361,
          79464,
          80898,
          81118,
          81330,
          82368,
          82703,
          83753,
          83784,
          84526,
          84596,
          84995,
          87125,
          87544,
          88478,
          90411,
          91443,
          92175,
          92178,
          93986,
          94283,
          95185,
          96199,
          98321,
          98823,
          99709,
          102991,
          103019,
          103053,
          105880,
          105901,
          106415,
          108504,
          108618,
          108689,
          109577,
          110366,
          110657,
          112558,
          112888,
          115051,
          116332,
          117130,
          117477,
          118532,
          118791,
          118832,
          119748,
          124764,
          125999,
          126639,
          126910,
          127020,
          127188,
          127282,
          128183,
          128905,
          129173,
          130275,
          130496,
          130617,
          130659,
          131649,
          131717,
          131813,
          131899,
          131966,
          133125,
          134056,
          135589,
          136166,
          136858,
          137366,
          138754,
          139271,
          140043,
          140704,
          140714,
          140734,
          141809,
          142745,
          143932,
          145447,
          145512,
          146834,
          148376,
          148698,
          149593,
          151099,
          151116,
          153287,
          154058,
          154099,
          156941,
          157757,
          157768,
          157838,
          159003,
          159551,
          160023,
          160250,
          161204,
          161248,
          161340,
          161604,
          161631,
          161918,
          162733,
          163705,
          163729,
          164283,
          164318,
          164367,
          164475,
          165039,
          166149,
          166532,
          166914,
          167580,
          167785,
          168330,
          168452,
          168764,
          169249,
          171217,
          172217,
          173109,
          173126,
          173253,
          173991,
          174380,
          175608,
          175927,
          176582,
          176744,
          177833,
          178947,
          180479,
          181106,
          182873,
          182993,
          183427,
          183477,
          183576,
          184427,
          186327,
          186485,
          187697,
          189002,
          189792,
          190630,
          192031,
          192559,
          192620,
          193027,
          193933,
          194336
        ],
        "sampled_c32_collisions": 0,
        "both_prefixes_replay_through_step_13": true,
        "tail_build_and_sample_seconds": 1.96679504099302
      },
      {
        "id": 12,
        "cv_words": [
          "e3b733ea",
          "2a8db5e2",
          "0b8cad74",
          "44bf0ce2",
          "a73d9036",
          "5cdee4a0",
          "f00fb7e6",
          "93900645"
        ],
        "table_key": "e3b733ea",
        "record": [
          "bb9e4631",
          "ba9f56bb",
          "6e41703e",
          "6e497c3e",
          "c68dc362",
          "c68dc362",
          "29b2da13",
          "09b2da13",
          "acb120ea"
        ],
        "candidate_tail_count": 196608,
        "tail_enumeration": {
          "e14_row_values": 256,
          "e15_row_values_per_w14": 32768,
          "w14_values_passing_all_a14_conditions": 12,
          "tails_per_passing_w14": [
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384
          ]
        },
        "candidate_tail_sha256": "ec59bb6beaab8473f3ce54e8a8a121f043ca2097e7e952e7946dff35975b8b1d",
        "sample_size": 256,
        "sample_indexes": [
          715,
          1066,
          1281,
          3807,
          6827,
          6913,
          6996,
          8651,
          11462,
          11723,
          12316,
          14382,
          14589,
          14723,
          14829,
          15289,
          16577,
          17260,
          18606,
          20041,
          20884,
          21700,
          21710,
          22497,
          23023,
          24354,
          24413,
          25274,
          25813,
          27404,
          27613,
          27940,
          28035,
          28294,
          28487,
          28749,
          29199,
          29484,
          30068,
          30258,
          32215,
          33325,
          33508,
          34354,
          34605,
          35234,
          35416,
          36417,
          36595,
          37083,
          37285,
          37694,
          38012,
          38418,
          38797,
          39750,
          41732,
          42352,
          43336,
          44287,
          45044,
          45395,
          46021,
          48198,
          48624,
          49313,
          50137,
          51585,
          52475,
          52633,
          52959,
          53691,
          53828,
          53887,
          54467,
          54594,
          56225,
          58128,
          58198,
          58220,
          58431,
          58702,
          60028,
          60145,
          61220,
          61302,
          62478,
          62571,
          63312,
          63641,
          63719,
          64387,
          64708,
          64949,
          65858,
          66907,
          67243,
          67438,
          67470,
          67627,
          67639,
          68154,
          71127,
          71494,
          72637,
          73043,
          73048,
          74873,
          77809,
          77839,
          78368,
          80214,
          81325,
          81549,
          81687,
          82366,
          82819,
          83439,
          83845,
          84028,
          84338,
          85857,
          86640,
          88199,
          88647,
          89541,
          89660,
          92586,
          93234,
          94265,
          94347,
          95844,
          96187,
          97208,
          98110,
          98117,
          98130,
          98382,
          99849,
          100190,
          102594,
          102823,
          102869,
          104052,
          104752,
          105081,
          106117,
          107610,
          108276,
          108280,
          108496,
          108708,
          108787,
          110065,
          110427,
          110786,
          111274,
          111391,
          111900,
          112676,
          113699,
          113927,
          114873,
          118083,
          121180,
          121191,
          121539,
          122330,
          122888,
          123108,
          123136,
          123816,
          125077,
          125310,
          126133,
          126556,
          127187,
          127533,
          130649,
          130818,
          132571,
          132619,
          133135,
          133402,
          135089,
          135727,
          135843,
          136772,
          137349,
          141127,
          142246,
          142616,
          143279,
          143668,
          143714,
          144388,
          145469,
          146297,
          146848,
          148807,
          149301,
          149661,
          150461,
          150506,
          150562,
          150617,
          152285,
          153601,
          153954,
          154038,
          157838,
          159214,
          160018,
          160580,
          160693,
          160874,
          161979,
          162055,
          163082,
          165435,
          166237,
          167217,
          167522,
          168146,
          168871,
          169328,
          170160,
          170321,
          173738,
          173987,
          174840,
          175408,
          176754,
          177399,
          177637,
          177713,
          178406,
          180488,
          180571,
          180897,
          183368,
          183541,
          183745,
          184409,
          184611,
          186076,
          186145,
          187291,
          188414,
          190159,
          190916,
          191034,
          192813,
          193304,
          193436,
          194727
        ],
        "sampled_c32_collisions": 0,
        "both_prefixes_replay_through_step_13": true,
        "tail_build_and_sample_seconds": 1.9588920411188155
      },
      {
        "id": 13,
        "cv_words": [
          "d4b714f4",
          "8f63dbb7",
          "ace48e6b",
          "22554d34",
          "4185d6d1",
          "b99eec85",
          "ddbd3c2f",
          "90c6db69"
        ],
        "table_key": "d4b714f4",
        "record": [
          "cb1c6521",
          "ca1d75ab",
          "6ec37038",
          "6ecb7c38",
          "b78fa46c",
          "b78fa46c",
          "2930da19",
          "0930da19",
          "ac2f20f0"
        ],
        "candidate_tail_count": 196608,
        "tail_enumeration": {
          "e14_row_values": 256,
          "e15_row_values_per_w14": 32768,
          "w14_values_passing_all_a14_conditions": 12,
          "tails_per_passing_w14": [
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384
          ]
        },
        "candidate_tail_sha256": "ec59bb6beaab8473f3ce54e8a8a121f043ca2097e7e952e7946dff35975b8b1d",
        "sample_size": 256,
        "sample_indexes": [
          120,
          286,
          425,
          1843,
          2285,
          4449,
          5126,
          6370,
          7156,
          8108,
          8734,
          9280,
          9376,
          9954,
          10705,
          10920,
          12525,
          12977,
          13416,
          13954,
          14239,
          14572,
          15102,
          15163,
          15427,
          16222,
          16365,
          19356,
          19909,
          20479,
          20513,
          20545,
          20717,
          20767,
          20876,
          22665,
          22692,
          22916,
          23078,
          23354,
          24019,
          24712,
          26096,
          26239,
          27198,
          28093,
          28343,
          29565,
          30199,
          31444,
          31499,
          32384,
          32647,
          33474,
          33570,
          36041,
          36408,
          37498,
          37645,
          37759,
          38260,
          38839,
          39428,
          39532,
          39691,
          39897,
          40625,
          41741,
          42759,
          43722,
          43866,
          44015,
          44805,
          45255,
          45544,
          46492,
          47657,
          49906,
          50241,
          50963,
          51139,
          52989,
          53593,
          54336,
          54638,
          55289,
          55829,
          58669,
          60862,
          61876,
          62019,
          62261,
          62390,
          63142,
          63181,
          63271,
          63507,
          64726,
          66415,
          67594,
          67667,
          68657,
          69546,
          69709,
          70278,
          71527,
          71671,
          71675,
          72410,
          74512,
          75304,
          75334,
          75787,
          76033,
          76307,
          77048,
          78019,
          78232,
          79204,
          80838,
          80955,
          82299,
          84433,
          85069,
          85746,
          86618,
          87523,
          88129,
          88633,
          88644,
          89134,
          91443,
          92357,
          94390,
          94833,
          95731,
          96391,
          97572,
          97909,
          98304,
          98436,
          102169,
          102449,
          103795,
          104596,
          104666,
          104733,
          105381,
          106135,
          106495,
          107781,
          108117,
          108798,
          109598,
          110476,
          110778,
          111116,
          111287,
          111745,
          111829,
          113077,
          113593,
          114930,
          117274,
          118410,
          119541,
          121608,
          121688,
          121758,
          124073,
          124275,
          124966,
          126853,
          128603,
          128762,
          128886,
          130115,
          130724,
          131778,
          132790,
          132904,
          133205,
          134681,
          135761,
          135790,
          137613,
          138603,
          138958,
          139578,
          141745,
          142760,
          142818,
          143421,
          144473,
          145465,
          147993,
          148059,
          149184,
          150463,
          151010,
          151219,
          152554,
          152642,
          153267,
          154737,
          155242,
          155431,
          155934,
          156437,
          156671,
          157492,
          157780,
          158083,
          159600,
          160091,
          161784,
          162800,
          163068,
          163291,
          163954,
          164585,
          165141,
          165967,
          166223,
          166713,
          166902,
          167415,
          167517,
          168257,
          169563,
          169887,
          171410,
          171785,
          171803,
          172371,
          172425,
          173208,
          175936,
          176017,
          177948,
          178872,
          179893,
          182823,
          183631,
          187802,
          189103,
          189189,
          189418,
          190533,
          191984,
          193069,
          194184,
          194836,
          195554,
          196089,
          196596
        ],
        "sampled_c32_collisions": 0,
        "both_prefixes_replay_through_step_13": true,
        "tail_build_and_sample_seconds": 1.9979778330307454
      },
      {
        "id": 14,
        "cv_words": [
          "abb91616",
          "e80fa0cf",
          "c03150a1",
          "1ec424ae",
          "1ed62f54",
          "e9c3e8a9",
          "d070ec37",
          "dd13d6ed"
        ],
        "table_key": "abb91616",
        "record": [
          "f39c6465",
          "f29d74ef",
          "6e41701e",
          "6e497c1e",
          "8e8fa50e",
          "8e8fa50e",
          "29b2da33",
          "09b2da33",
          "acb1210a"
        ],
        "candidate_tail_count": 196608,
        "tail_enumeration": {
          "e14_row_values": 256,
          "e15_row_values_per_w14": 32768,
          "w14_values_passing_all_a14_conditions": 12,
          "tails_per_passing_w14": [
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384
          ]
        },
        "candidate_tail_sha256": "ec59bb6beaab8473f3ce54e8a8a121f043ca2097e7e952e7946dff35975b8b1d",
        "sample_size": 256,
        "sample_indexes": [
          1263,
          3660,
          3900,
          3964,
          4071,
          4210,
          4640,
          4693,
          6824,
          7224,
          7531,
          10435,
          11396,
          12315,
          12520,
          13952,
          14487,
          14918,
          15810,
          16608,
          17386,
          18117,
          19121,
          19261,
          19682,
          19817,
          21193,
          21430,
          22066,
          24238,
          24406,
          24636,
          26739,
          26789,
          29012,
          31244,
          31935,
          35162,
          35535,
          36645,
          37020,
          37181,
          37576,
          38807,
          39150,
          39187,
          40658,
          41796,
          42476,
          43098,
          44094,
          45359,
          45449,
          46655,
          47035,
          47340,
          47670,
          48334,
          48470,
          49109,
          50305,
          50733,
          51271,
          51675,
          51709,
          52606,
          52761,
          52794,
          52862,
          53649,
          54379,
          54628,
          55033,
          55695,
          55857,
          56573,
          57918,
          60079,
          61307,
          61583,
          61692,
          61757,
          65697,
          65740,
          66263,
          66842,
          67126,
          67484,
          68002,
          69359,
          71915,
          73117,
          73355,
          73432,
          73664,
          75074,
          75403,
          75539,
          76074,
          77010,
          77315,
          77694,
          79446,
          81062,
          81105,
          81875,
          82409,
          83189,
          83712,
          84011,
          84180,
          85798,
          87819,
          89333,
          89585,
          89994,
          91037,
          94042,
          95652,
          98298,
          98414,
          98995,
          99092,
          99173,
          99341,
          100960,
          103285,
          104560,
          107218,
          107406,
          109020,
          110428,
          110724,
          112995,
          113056,
          113104,
          113278,
          113823,
          113994,
          114734,
          115783,
          115847,
          116453,
          118623,
          119251,
          120513,
          121222,
          125025,
          126033,
          126268,
          126647,
          127388,
          127877,
          129999,
          130702,
          130941,
          131703,
          131813,
          131989,
          132649,
          133829,
          134251,
          134548,
          135929,
          137126,
          138068,
          139239,
          139638,
          140501,
          140877,
          141612,
          142929,
          143831,
          145637,
          145656,
          146082,
          146427,
          146763,
          147289,
          147902,
          148008,
          148578,
          148656,
          148658,
          150238,
          151953,
          152538,
          152933,
          153408,
          154458,
          154623,
          154632,
          155060,
          156634,
          156739,
          157238,
          157530,
          158746,
          158805,
          158950,
          159144,
          160746,
          161595,
          162293,
          163778,
          164447,
          165107,
          165965,
          167831,
          168388,
          168451,
          170681,
          171616,
          172621,
          173132,
          173137,
          173491,
          173520,
          174373,
          174528,
          174610,
          175370,
          175825,
          178019,
          178536,
          179797,
          180051,
          180533,
          180738,
          181812,
          182453,
          183198,
          183373,
          183528,
          183643,
          184021,
          184357,
          184728,
          186195,
          186759,
          187136,
          187317,
          188247,
          188641,
          188656,
          189516,
          189845,
          191046,
          191661,
          192533,
          192751,
          192891,
          193509,
          194822,
          195959,
          196129
        ],
        "sampled_c32_collisions": 0,
        "both_prefixes_replay_through_step_13": true,
        "tail_build_and_sample_seconds": 2.059073750162497
      },
      {
        "id": 15,
        "cv_words": [
          "c43719b1",
          "fe18dc59",
          "6a38ac9a",
          "bdb4a33d",
          "64e38bf1",
          "12f42053",
          "62225622",
          "a47aabc4"
        ],
        "table_key": "c43719b1",
        "record": [
          "db9e4264",
          "da9f52ee",
          "6ec17238",
          "6ec97e38",
          "a70dc729",
          "a70dc729",
          "2932d819",
          "0932d819",
          "ac311ef0"
        ],
        "candidate_tail_count": 196608,
        "tail_enumeration": {
          "e14_row_values": 256,
          "e15_row_values_per_w14": 32768,
          "w14_values_passing_all_a14_conditions": 12,
          "tails_per_passing_w14": [
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384,
            16384
          ]
        },
        "candidate_tail_sha256": "ec59bb6beaab8473f3ce54e8a8a121f043ca2097e7e952e7946dff35975b8b1d",
        "sample_size": 256,
        "sample_indexes": [
          873,
          1426,
          1861,
          7824,
          8751,
          9512,
          11783,
          13898,
          13904,
          14619,
          15059,
          15422,
          16328,
          19171,
          19365,
          19699,
          21507,
          21613,
          21871,
          22559,
          22851,
          22930,
          25243,
          27008,
          27346,
          28772,
          29309,
          29923,
          30287,
          30414,
          30782,
          30992,
          32740,
          34573,
          35100,
          37469,
          37725,
          38669,
          38921,
          39247,
          39750,
          40329,
          41945,
          42631,
          43544,
          44687,
          45079,
          46288,
          47078,
          47279,
          47938,
          49075,
          50124,
          50482,
          50645,
          50817,
          51043,
          51233,
          52912,
          53492,
          54591,
          55273,
          55809,
          56127,
          56673,
          56759,
          56918,
          57094,
          57224,
          57757,
          58389,
          58647,
          59652,
          59755,
          60931,
          61127,
          61754,
          61778,
          63527,
          63606,
          64879,
          66532,
          67324,
          67635,
          69646,
          70281,
          70336,
          70796,
          71774,
          72373,
          72799,
          73292,
          73789,
          73949,
          74023,
          76132,
          77300,
          78055,
          79206,
          79302,
          80208,
          82036,
          84822,
          85391,
          85459,
          85759,
          86723,
          87024,
          87135,
          89607,
          90100,
          90287,
          90528,
          92072,
          93910,
          95103,
          96832,
          97726,
          97836,
          98248,
          99134,
          99447,
          99702,
          99930,
          104056,
          104271,
          104499,
          104962,
          105841,
          107451,
          108089,
          108753,
          108835,
          109392,
          109755,
          109988,
          110581,
          112209,
          112449,
          113336,
          113506,
          113813,
          116591,
          116690,
          117042,
          117065,
          117237,
          117423,
          117661,
          118124,
          118741,
          120269,
          120358,
          121018,
          121306,
          122093,
          123122,
          123568,
          124459,
          125970,
          128365,
          128375,
          128500,
          128992,
          129552,
          130120,
          131259,
          132402,
          133207,
          133403,
          134067,
          134150,
          135151,
          135616,
          135690,
          135786,
          136956,
          137600,
          137756,
          138146,
          138276,
          138333,
          140307,
          140462,
          141123,
          141913,
          142746,
          142854,
          144437,
          145637,
          147597,
          147969,
          148010,
          148411,
          148498,
          149205,
          150882,
          151239,
          153898,
          153934,
          155284,
          155986,
          157181,
          157821,
          157828,
          159128,
          160500,
          162925,
          163669,
          163849,
          164675,
          164741,
          165328,
          165942,
          166031,
          166116,
          166586,
          166876,
          167837,
          168434,
          170031,
          170432,
          170986,
          171071,
          171587,
          172250,
          172729,
          173236,
          173910,
          174439,
          176125,
          176451,
          176899,
          177443,
          177837,
          179390,
          181217,
          182681,
          182982,
          183772,
          184993,
          186572,
          186852,
          187354,
          188284,
          188342,
          189313,
          190421,
          190847,
          191564,
          192451,
          193627,
          195845,
          196274,
          196436,
          196449
        ],
        "sampled_c32_collisions": 0,
        "both_prefixes_replay_through_step_13": true,
        "tail_build_and_sample_seconds": 1.9951727918814868
      }
    ]
  },
  "runtime_seconds": 169.43808966688812,
  "interpretation_limit": "This sample checks exact predicates for a reproducible conditional ideal-state sample. It does not estimate the 2^-27 to 2^-34 full-sweep event and does not prove the C32 chaining-value distribution."
}
~~~

### Embedded file: verification/sha256-r32-bridge-probe-size.py

~~~python
#!/usr/bin/env python3
"""Measure a one-million-state conditional bridge probe for protocol sizing."""

import importlib.util
import argparse
import json
import random
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("tail_sample", HERE / "sha256-r32-tail-sample.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

parser = argparse.ArgumentParser()
parser.add_argument("--repo", help="challenge repository root; inferred when run inside repo")
args = parser.parse_args()
module.configure_repo(args.repo)

started = time.perf_counter()
table, table_stats = module.build_table()
rng = random.Random(20261004)
keys = sorted(table)
proposals = 1 << 20
accepted = 0
for _ in range(proposals):
    key = keys[rng.randrange(len(keys))]
    cv = (key, *(rng.getrandbits(32) for _ in range(7)))
    for record in table[key]:
        if module.derive_bridge(cv, record) is not None:
            accepted += 1
            break

conditional_lower = module.binomial_lower_one_sided(proposals, accepted, 0.001)
out = {
    "source": module.source_metadata(Path(__file__)),
    "seed": 20261004,
    "conditional_proposals": proposals,
    "conditional_acceptances": accepted,
    "conditional_acceptance_rate": accepted / proposals,
    "nominal_iid_one_sided_confidence": 0.999,
    "nominal_iid_conditional_rate_lower_99_9_percent": conditional_lower,
    "table_key_fraction": table_stats["distinct_keys"] / (1 << 32),
    "nominal_iid_uniform_cv_q_lower_99_9_percent": conditional_lower * table_stats["distinct_keys"] / (1 << 32),
    "table_sha256": table_stats["table_sha256"],
    "relationship_to_primary_sample": "Same seed and proposal order as the 2^22 run; this is its first 2^20 proposals, not an independent sample.",
    "coverage_limit": "The interval is a nominal iid-uniform binomial diagnostic. The fixed seeded PRNG run does not establish iid sampling or calibrated coverage.",
    "runtime_seconds": time.perf_counter() - started,
}
path = HERE / "sha256-r32-bridge-probe-size.json"
path.write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
~~~

### Embedded file: verification/sha256-r32-bridge-probe-size.json

~~~json
{
  "source": {
    "challenge_commit": "fc56c3fa38ac40043d8291649c78148bc4872995",
    "target_profile": "sha256-r32-prefix-v1",
    "target_profile_sha256": "93d2e5d9ca93540633798d58cbab2d6d8447916db2b127e9abe71f45d14f6835",
    "reference_hash_functions_sha256": "514fa8ab8a461e4a41080efa27b4ba2a3b499eeedf0a2d2346e6562835d040f5",
    "program_sha256": "e1aa67d9362718f422d71e259e250118286fb4e7647f6e1bd520ef9f3dc6c356",
    "bridge_sampler_sha256": "2fc6357e9aaaa078fc078ed42b34bdce4f1fe65a9fb9f37aac6bff00d7e5bce2",
    "figure6_conditions_sha256": "a8f9ed4cc356804f87bb8ce4986f751baf8ea4666f1a5dc3e468127eff6fc64e",
    "paper_inputs_sha256": "b30b7090712cb2b3c95990a4400abf45d3dfe620ffa4cea1fe89b5a523c19509",
    "python": "3.13.5 | packaged by Anaconda, Inc. | (main, Jun 12 2025, 11:23:37) [Clang 14.0.6 ]",
    "platform": "macOS-27.0-arm64-arm-64bit-Mach-O"
  },
  "seed": 20261004,
  "conditional_proposals": 1048576,
  "conditional_acceptances": 33,
  "conditional_acceptance_rate": 3.147125244140625e-05,
  "nominal_iid_one_sided_confidence": 0.999,
  "nominal_iid_conditional_rate_lower_99_9_percent": 1.7210416240318613e-05,
  "table_key_fraction": 9.512901306152344e-05,
  "nominal_iid_uniform_cv_q_lower_99_9_percent": 1.6372099113195245e-09,
  "table_sha256": "3cd961f8e0efe18027ec7192b4f0fa9f449659fdae14a5969fe3f6b821c8ebc7",
  "relationship_to_primary_sample": "Same seed and proposal order as the 2^22 run; this is its first 2^20 proposals, not an independent sample.",
  "coverage_limit": "The interval is a nominal iid-uniform binomial diagnostic. The fixed seeded PRNG run does not establish iid sampling or calibrated coverage.",
  "runtime_seconds": 69.71359466691501
}
~~~

### Embedded file: verification/sha256-r32-revision-ledger.py

~~~python
#!/usr/bin/env python3
"""Recompute the success and collision-frontier-v5 cost ledger."""

import json
import math
import platform
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sample = json.loads((HERE / "sha256-r32-tail-sample.json").read_text())
source_audit = json.loads((HERE / "sha256-r32-source-audit.json").read_text())

C = 2224
N = 1 << 65
M = 1 << 33
TAILS = 196608
MAX_RECORDS = sample["table"]["max_records_per_key"]
TRIAL_WORD_OPS = 2048
RECORD_WORD_OPS = 2048
TAIL_WORD_OPS = 4096
PREFIX_REPLAY_CEILING_COMPRESSIONS = 2
TABLE_SETUP_WORD_OPS = 1 << 40
PREPROCESSING_CEILING = 1 << 36
STARTING_SEARCH_CEILING = 1 << 35

assert sample["target"] == "sha256-r32-prefix-v1"
assert sample["source"]["challenge_commit"] == "fc56c3fa38ac40043d8291649c78148bc4872995"
assert sample["table"]["table_records"] == 593920
assert sample["table"]["distinct_keys"] == 408576
assert MAX_RECORDS == 4
assert source_audit["all_reported_conditions_pass"]

table_setup_ce = TABLE_SETUP_WORD_OPS / C
characteristic_residual_ce = PREPROCESSING_CEILING - STARTING_SEARCH_CEILING - table_setup_ce

H = {
    "first_block_C32_calls": N,
    "second_block_and_padding_calls_all_tails": 4 * M * TAILS,
    "final_validation_ceiling": 16,
}
W = {
    "trial_generation_lookup_and_control": TRIAL_WORD_OPS * N,
    "worst_case_four_record_examinations": MAX_RECORDS * RECORD_WORD_OPS * N,
    "per_tail_construction_checks_and_comparison": TAIL_WORD_OPS * M * TAILS,
    "two_prefix_replays_per_accepted_bridge": PREFIX_REPLAY_CEILING_COMPRESSIONS * C * M,
}

online_units = sum(H.values()) + sum(W.values()) / C
total_units = online_units + PREPROCESSING_CEILING
success_tail_failure = math.exp(-M * 2.0 ** -34)
success_lower = 1.0 - 2.0 ** -32 - success_tail_failure

preprocess_components = {
    "source_constant_replay": {
        "compression_equivalent_ceiling": 6,
        "word_ops": 6 * C,
    },
    "W8_enumeration": {
        "candidate_count": 1 << 20,
        "maximum_word_ops_each": 256,
        "word_ops": (1 << 20) * 256,
    },
    "W7_enumeration_after_44_W8_survivors": {
        "candidate_count": 44 * (1 << 19),
        "maximum_word_ops_each": 512,
        "word_ops": 44 * (1 << 19) * 512,
    },
    "stable_merge_sort_and_pack": {
        "records": 593920,
        "merge_levels_ceiling": 20,
        "maximum_word_ops_per_record_per_level": 32,
        "word_ops": 593920 * 20 * 32,
    },
    "direct_index_initialize_and_fill": {
        "entries": 1 << 32,
        "maximum_word_ops_per_entry": 2,
        "word_ops": 2 * (1 << 32),
    },
    "tail_rows_and_tail_set": {
        "E14_row_values": 1 << 8,
        "maximum_word_ops_per_E14_value": 512,
        "E14_word_ops": (1 << 8) * 512,
        "surviving_W14_values": 12,
        "E15_row_values_per_W14": 1 << 15,
        "raw_E15_pairs": 12 * (1 << 15),
        "maximum_word_ops_per_raw_pair": 512,
        "E15_word_ops": 12 * (1 << 15) * 512,
        "word_ops": ((1 << 8) * 512) + 12 * (1 << 15) * 512,
    },
}
table_setup_counted_word_ops = sum(item["word_ops"] for item in preprocess_components.values())
assert table_setup_counted_word_ops < TABLE_SETUP_WORD_OPS
assert STARTING_SEARCH_CEILING + characteristic_residual_ce + table_setup_ce == PREPROCESSING_CEILING

out = {
    "cost_model": "collision-frontier-v5",
    "target": "sha256-r32-prefix-v1",
    "source_repo_commit": sample["source"]["challenge_commit"],
    "source_measurement_sha256": sample["source"]["program_sha256"],
    "table_input": {
        "records": sample["table"]["table_records"],
        "distinct_keys": sample["table"]["distinct_keys"],
        "maximum_records_per_key": MAX_RECORDS,
        "packed_table_bytes": sample["table"]["table_bytes"],
        "packed_table_sha256": sample["table"]["table_sha256"],
    },
    "parameters": {
        "C": C,
        "first_block_trials_N": N,
        "accepted_bridges_swept_M": M,
        "tails_per_sweep": TAILS,
        "q_lower_premise": 2.0 ** -31,
        "pi_average_lower_premise": 2.0 ** -34,
        "first_m_accepted_bridges_are_iid_under_fresh_independent_trials": True,
    },
    "H_C32_compression_equivalents": H | {"online_total": sum(H.values())},
    "W_256_bit_word_operations": W | {"online_total": sum(W.values())},
    "online_target_compression_equivalents": online_units,
    "preprocessing": {
        "finite_table_tail_setup_ceiling_word_ops": TABLE_SETUP_WORD_OPS,
        "finite_table_tail_setup_ceiling_target_compressions": table_setup_ce,
        "finite_table_tail_counted_upper_bound_word_ops": table_setup_counted_word_ops,
        "finite_table_tail_operation_breakdown": preprocess_components,
        "step1_reported_work_exponent": 34.3,
        "step1_charged_target_compression_ceiling": STARTING_SEARCH_CEILING,
        "starting_search_units_conversion": "unresolved premise; the paper's generic work unit is not defined as a collision-frontier-v5 target-compression unit",
        "characteristic_search_residual_ceiling_target_compressions": characteristic_residual_ce,
        "characteristic_search_numeric_source_bound": None,
        "characteristic_search_ceiling_status": "unresolved premise; source reports a four-stage search and a result, but not a numeric upper bound",
        "aggregate_preprocessing_ceiling_target_compressions": PREPROCESSING_CEILING,
    },
    "success_given_declared_premises": {
        "expected_accepted_bridge_count_lower": N * 2.0 ** -31,
        "accepted_count_failure_probability_upper": 2.0 ** -32,
        "conditional_all_miss_probability_for_first_M_accepted_bridges_upper": success_tail_failure,
        "combined_success_probability_lower": success_lower,
        "claim_probability_rounded_down": 0.39,
        "slack_above_0.39": success_lower - 0.39,
        "derivation": [
            "For independent trials X is Binomial(N,q), E[X]>=2^34 and Var(X)<=E[X].",
            "Chebyshev at distance E[X]/2 gives P[X<M]<=4/E[X]<=2^-32.",
            "Conditional on at least M acceptances, the first M accepted bridges are iid from a single-trial bridge distribution conditioned on acceptance (rejection sampling).",
            "A complete tail sweep is a deterministic predicate of each accepted bridge. If its conditional mean success is at least pi=2^-34, iid accepted bridges give all-miss probability (1-E[p_i])^M<=exp(-M*pi)=exp(-1/2).",
            "Union bound gives 1-2^-32-exp(-1/2)=0.3934693400545...; the claim is 0.39."
        ],
    },
    "memory": {
        "direct_index_bytes": 1 << 34,
        "packed_table_bytes": sample["table"]["table_bytes"],
        "tail_array_bytes": TAILS * 8,
        "known_online_data_structure_bytes": (1 << 34) + sample["table"]["table_bytes"] + TAILS * 8,
        "code_runtime_and_search_peak_upper_bound_bytes": None,
        "claimed_full_peak_bytes": 1 << 39,
        "reported_historical_server_capacity_decimal_bytes": 378000000000,
        "claimed_ceiling_over_historical_capacity_ratio": (1 << 39) / 378000000000,
        "full_peak_status": "unresolved premise; historical capacity is not a measured peak or an upper bound for either search",
    },
    "advice": {
        "inventory_source": "byte inventory table in proof.md",
        "claimed_ceiling_bytes": 1 << 16,
        "inventory_upper_bound_bytes": 1024,
        "solver_artifacts_retained": 0,
        "precomputed_table_is_generated_and_charged_instead_of_supplied_as_advice": True,
    },
    "total_target_compression_equivalents": total_units,
    "total_time_log2": math.log2(total_units),
    "claim_time_log2_rounded_up_to_three_decimals": math.ceil(math.log2(total_units) * 1000) / 1000,
    "fixed_inputs_and_ceiling_sources": {
        "N": "2^65",
        "M": "2^33",
        "tails_per_sweep": "196608 from exact table/tail enumeration",
        "trial_word_ops": "2048 per trial; explicit budget in proof.md",
        "record_word_ops": "2048 per examined record; explicit budget in proof.md",
        "tail_word_ops": "4096 per swept tail; includes at most two raw W15 row candidates per output tail",
        "final_validation": "16 C32-compression ceiling; six exact calls for two 3-block messages, rounded upward",
        "finite_setup_word_ops": "2^40 ceiling above explicit enumeration, sorting, indexing and tail count",
        "prefix_replays": "two 14-round branch replays per accepted bridge, each charged as one full C32 equivalent and converted to 2224 word operations",
    },
    "participant_measurement_is_not_organizer_experiment": True,
    "python": sys.version,
    "platform": platform.platform(),
}
(HERE / "sha256-r32-revision-ledger.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
~~~

### Embedded file: verification/sha256-r32-revision-ledger.json

~~~json
{
  "cost_model": "collision-frontier-v5",
  "target": "sha256-r32-prefix-v1",
  "source_repo_commit": "fc56c3fa38ac40043d8291649c78148bc4872995",
  "source_measurement_sha256": "2fc6357e9aaaa078fc078ed42b34bdce4f1fe65a9fb9f37aac6bff00d7e5bce2",
  "table_input": {
    "records": 593920,
    "distinct_keys": 408576,
    "maximum_records_per_key": 4,
    "packed_table_bytes": 14254080,
    "packed_table_sha256": "3cd961f8e0efe18027ec7192b4f0fa9f449659fdae14a5969fe3f6b821c8ebc7"
  },
  "parameters": {
    "C": 2224,
    "first_block_trials_N": 36893488147419103232,
    "accepted_bridges_swept_M": 8589934592,
    "tails_per_sweep": 196608,
    "q_lower_premise": 4.656612873077393e-10,
    "pi_average_lower_premise": 5.820766091346741e-11,
    "first_m_accepted_bridges_are_iid_under_fresh_independent_trials": true
  },
  "H_C32_compression_equivalents": {
    "first_block_C32_calls": 36893488147419103232,
    "second_block_and_padding_calls_all_tails": 6755399441055744,
    "final_validation_ceiling": 16,
    "online_total": 36900243546860158992
  },
  "W_256_bit_word_operations": {
    "trial_generation_lookup_and_control": 75557863725914323419136,
    "worst_case_four_record_examinations": 302231454903657293676544,
    "per_tail_construction_checks_and_comparison": 6917529027641081856,
    "two_prefix_replays_per_accepted_bridge": 38208029065216,
    "online_total": 377796236196807287242752
  },
  "online_target_compression_equivalents": 2.0677265190873393e+20,
  "preprocessing": {
    "finite_table_tail_setup_ceiling_word_ops": 1099511627776,
    "finite_table_tail_setup_ceiling_target_compressions": 494384724.7194245,
    "finite_table_tail_counted_upper_bound_word_ops": 21251109920,
    "finite_table_tail_operation_breakdown": {
      "source_constant_replay": {
        "compression_equivalent_ceiling": 6,
        "word_ops": 13344
      },
      "W8_enumeration": {
        "candidate_count": 1048576,
        "maximum_word_ops_each": 256,
        "word_ops": 268435456
      },
      "W7_enumeration_after_44_W8_survivors": {
        "candidate_count": 23068672,
        "maximum_word_ops_each": 512,
        "word_ops": 11811160064
      },
      "stable_merge_sort_and_pack": {
        "records": 593920,
        "merge_levels_ceiling": 20,
        "maximum_word_ops_per_record_per_level": 32,
        "word_ops": 380108800
      },
      "direct_index_initialize_and_fill": {
        "entries": 4294967296,
        "maximum_word_ops_per_entry": 2,
        "word_ops": 8589934592
      },
      "tail_rows_and_tail_set": {
        "E14_row_values": 256,
        "maximum_word_ops_per_E14_value": 512,
        "E14_word_ops": 131072,
        "surviving_W14_values": 12,
        "E15_row_values_per_W14": 32768,
        "raw_E15_pairs": 393216,
        "maximum_word_ops_per_raw_pair": 512,
        "E15_word_ops": 201326592,
        "word_ops": 201457664
      }
    },
    "step1_reported_work_exponent": 34.3,
    "step1_charged_target_compression_ceiling": 34359738368,
    "starting_search_units_conversion": "unresolved premise; the paper's generic work unit is not defined as a collision-frontier-v5 target-compression unit",
    "characteristic_search_residual_ceiling_target_compressions": 33865353643.280575,
    "characteristic_search_numeric_source_bound": null,
    "characteristic_search_ceiling_status": "unresolved premise; source reports a four-stage search and a result, but not a numeric upper bound",
    "aggregate_preprocessing_ceiling_target_compressions": 68719476736
  },
  "success_given_declared_premises": {
    "expected_accepted_bridge_count_lower": 17179869184.0,
    "accepted_count_failure_probability_upper": 2.3283064365386963e-10,
    "conditional_all_miss_probability_for_first_M_accepted_bridges_upper": 0.6065306597126334,
    "combined_success_probability_lower": 0.39346934005453593,
    "claim_probability_rounded_down": 0.39,
    "slack_above_0.39": 0.0034693400545359188,
    "derivation": [
      "For independent trials X is Binomial(N,q), E[X]>=2^34 and Var(X)<=E[X].",
      "Chebyshev at distance E[X]/2 gives P[X<M]<=4/E[X]<=2^-32.",
      "Conditional on at least M acceptances, the first M accepted bridges are iid from a single-trial bridge distribution conditioned on acceptance (rejection sampling).",
      "A complete tail sweep is a deterministic predicate of each accepted bridge. If its conditional mean success is at least pi=2^-34, iid accepted bridges give all-miss probability (1-E[p_i])^M<=exp(-M*pi)=exp(-1/2).",
      "Union bound gives 1-2^-32-exp(-1/2)=0.3934693400545...; the claim is 0.39."
    ]
  },
  "memory": {
    "direct_index_bytes": 17179869184,
    "packed_table_bytes": 14254080,
    "tail_array_bytes": 1572864,
    "known_online_data_structure_bytes": 17195696128,
    "code_runtime_and_search_peak_upper_bound_bytes": null,
    "claimed_full_peak_bytes": 549755813888,
    "reported_historical_server_capacity_decimal_bytes": 378000000000,
    "claimed_ceiling_over_historical_capacity_ratio": 1.454380460021164,
    "full_peak_status": "unresolved premise; historical capacity is not a measured peak or an upper bound for either search"
  },
  "advice": {
    "inventory_source": "byte inventory table in proof.md",
    "claimed_ceiling_bytes": 65536,
    "inventory_upper_bound_bytes": 1024,
    "solver_artifacts_retained": 0,
    "precomputed_table_is_generated_and_charged_instead_of_supplied_as_advice": true
  },
  "total_target_compression_equivalents": 2.067726519774534e+20,
  "total_time_log2": 67.48660728327647,
  "claim_time_log2_rounded_up_to_three_decimals": 67.487,
  "fixed_inputs_and_ceiling_sources": {
    "N": "2^65",
    "M": "2^33",
    "tails_per_sweep": "196608 from exact table/tail enumeration",
    "trial_word_ops": "2048 per trial; explicit budget in proof.md",
    "record_word_ops": "2048 per examined record; explicit budget in proof.md",
    "tail_word_ops": "4096 per swept tail; includes at most two raw W15 row candidates per output tail",
    "final_validation": "16 C32-compression ceiling; six exact calls for two 3-block messages, rounded upward",
    "finite_setup_word_ops": "2^40 ceiling above explicit enumeration, sorting, indexing and tail count",
    "prefix_replays": "two 14-round branch replays per accepted bridge, each charged as one full C32 equivalent and converted to 2224 word operations"
  },
  "participant_measurement_is_not_organizer_experiment": true,
  "python": "3.13.5 | packaged by Anaconda, Inc. | (main, Jun 12 2025, 11:23:37) [Clang 14.0.6 ]",
  "platform": "macOS-27.0-arm64-arm-64bit-Mach-O"
}
~~~
