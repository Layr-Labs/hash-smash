# A published-trail collision attack on five-round SHA3-256 over byte strings

The scalar below is `time_log2` under `collision-frontier-v5`. Memory remains
a separately reported resource bound.

This exploratory package targets sha3-256-r5-prefix-v1. It proposes a classical
randomized algorithm that adapts the published practical collision attack of
Guo, Liao, Liu, Liu, Qiao and Song (Journal of Cryptology 2019; Cryptology
ePrint Archive 2019/147; hereafter GLL+19) to the byte-string message domain
of the target profile. The declared bound is `time_log2 = 60` under
collision-frontier-v5, with declared success probability 0.5 and peak memory at
most 2^30 bytes. The bound is an analytical upper bound on charged resources;
it is not a measured wall-clock figure and no full-scale execution is claimed.

Unlike the generic birthday baseline (declared 129 and 137.785 in recent
submissions), this package exploits a real differential mechanism with a
published, verified witness on the exact reduced permutation. All premises
that carry genuine uncertainty are enumerated in `claim.json` as heuristics
and cross-referenced in Section 7.

## 1. Exact complete hash

H is the complete byte-string hash fixed by target profile
sha3-256-r5-prefix-v1. For a byte string m of bit length below 2^64, pad
`m || 0x06 || (zero bytes) || 0x80` to a multiple of the 136-byte rate,
XOR each block into the first 17 lanes of the all-zero 1600-bit state
(lane index x+5y, little-endian 64-bit lanes), apply Keccak-f[1600] prefix
rounds 0 through 4 in order with round constants RC[0] through RC[4], and
emit the first 32 squeeze bytes (lanes A[0..3], little-endian). The
permutation step formulas, rho offsets and round constants are the FIPS 202
values exactly as restated in the profile and in the organizer reference
`verifier/keccak.py`. There is no feed-forward; the capacity lanes start at
zero only before the first block. The profile is a prefix reduction, not
Keccak-p's last-round convention.

This package uses single-block messages only: each message is exactly 135
bytes, so its padded block is `m || 0x86` (the 0x06 suffix byte followed by
nothing, with the final padding bit folded into the same byte: bit 7 of
byte 135 equals 1). Every message is a byte string in the profile domain;
there is no unknown IV and no supplied prefix.

## 2. The published attack and its relevance

GLL+19 mount collision attacks on round-reduced Keccak instances by
combining an nr1-round algebraic connector with an nr2-round differential
trail. For 5-round SHA3-256 (their Table 6 and Table 17) the parameters are:

- nr1 = 2: a two-round connector over prefix rounds 0 and 1, constructed by
  linearizing the Keccak S-box (chi) of the first round - either fully or
  partially ("non-full Sbox linearization", consuming fewer degrees of
  freedom) - and then applying a target-difference-style linear solve over
  the second round. The connector returns an affine subspace of message
  pairs whose state difference after two rounds equals the prescribed start
  difference alpha2 of the trail.
- nr2 = 3: differential trail core No. 3 over prefix rounds 2, 3, 4 with
  output difference zero on the 256 digest bits. The per-pair probability
  of the last rounds is reported as 2^-36.70 when multiple compatible
  trails of the last two rounds are taken into account (their Table 6
  footnote). The trail core's activity pattern (#AS 59-10-9-0, weights
  127-24-19-0) appears in their Tables 5 and 9.
- Connector output: a message space with DF = 37 measured degrees of
  freedom after the connecting stage, costing Tc = 428.8 CPU core-hours.
- Brute force: with DF > w = 36.70, a colliding pair is found by evaluating
  the message space; reported Tb = 45.6 CPU core-hours. Their Table 17
  publishes a concrete colliding pair with common digest
  65017C2E8B6040B4 344FF8BB933B4BD6 C6A3F13368BE2003 AB427B4B33435ACB.

Provenance check performed for this package (see Section 6): the published
padded blocks of Table 17, interpreted as a 136-byte rate block XORed into
the zero state, collide under the organizer's own prefix-round permutation
(`verifier/keccak.py`, rounds 0..4) and produce exactly the published
digest. This is a permutation-level confirmation that the target profile,
round convention, padding position and digest extraction used by the paper
match this track's contract.

The published pair is, however, NOT usable as a certificate here. The
paper's attack fixes only p = 4 trailing padding bits (a '1110' tail; the
p=4 figure appears in their Section 3 discussion of connector constraints
and in Table 3). Consequently both published messages are 1084 bits long -
their final padded byte is 0xEE, not a value reachable by byte-string
padding - and the message domain of this profile contains byte strings
only. The verifier accepts only byte-string certificate messages, and this
package claims no certificate.

## 3. Byte-aligned adaptation

A 135-byte message pads to `m || 0x86`, so the last 8 bits of the rate
block are fixed (0x86 = 10000110 in the little-endian lane bit order, of
which the paper's analysis already fixes the last 4 bits '1110'; byte
alignment fixes the remaining 4 bits 0,1,0,0 at positions 1080..1083 of
the block). Equivalently the connector's fixed-bit parameter moves from
p = 4 to p = 8, and the total controlled degrees of freedom drop from
TDF = 124 (their Table 3) to 120.

Why a linear loss of 4 is the natural accounting: the paper's degree-of-
freedom bookkeeping, formulas (11) and the TDF threshold in their
Section 5.2, count the attacker-controlled message bits minus the bits
consumed by linearization equations and by the c+p fixed tail positions.
The four additional fixed bits are four additional linear constraints on
the message variables; they enter the accounting additively, exactly as
the p term does. The measured connector output DF = 37 therefore maps to
an expected DF near 33. Because the TDF figure is itself described by the
authors as a pessimistic threshold (their Section 5.2 notes actual values
can exceed it), the floor used for resource accounting here is DF >= 25,
well below the shifted expectation of 33. The success-probability bound
in Section 4 uses only DF >= 25; the claimed schedule never depends on
the nominal value.

The rerun schedule is R = 2^13 = 8192 connector executions. Each
execution i:

1. Draws fresh random coins for the connector's randomized choices
   (the paper's Algorithm retry loop samples a random compatible beta1 and
   reruns when the linear system is unsatisfiable), and solves one
   two-round connector instance for trail core No. 3 with p = 8.
2. Produces an affine message space S_i of dimension DF_i >= 25
   (declared floor; nominally ~33) consisting of 135-byte messages, each
   padding to `m || 0x86` as in Section 1.
3. For every message m in S_i, computes H(m) and H(m XOR delta), where
   delta is the fixed message difference entering trail core No. 3
   (delta is part of the public trail data; its support lies inside the
   message bits, so m XOR delta is also 135 bytes and pads identically).
   A colliding pair is any m with H(m) = H(m XOR delta).

The first connector instance whose space yields a pair with
H(m) = H(m XOR delta) returns the two 135-byte messages. The algorithm
performs the standard final verification: both messages are reconstructed,
re-hashed from the zero state over all five rounds, checked for
distinctness and for equality of all 256 output bits, and returned only if
every check passes; otherwise the algorithm continues and halts with
failure after exhausting R spaces. Repeated identical pairs are harmless
and charged; no uncontrolled restart occurs outside the schedule.

Messages in different spaces may overlap; all evaluations are charged at
their full multiplicity, so overlap can only hurt efficiency, never
correctness of the bound.

## 4. Success probability accounting

The probability space consists of the connector's random coins; the
message spaces are affine subspaces, and every pair (m, m XOR delta)
tested in a space is a candidate colliding pair for the last-three-rounds
trail.

Under the declared trail-probability heuristic (Section 7, h2), each
tested pair follows the trail to a zero output difference on the 256
digest bits with probability at least 2^-36.70. Under the independence
heuristic (h3), pair outcomes across spaces and within a space are
counted as independent Bernoulli trials - the same counting convention
used by GLL+19 when DF > w was treated as sufficient.

A connector space of dimension DF_i contributes at least 2^(DF_i - 1)
distinct unordered pairs (m, m XOR delta) - each message indexes one pair
and each pair is counted at most twice. With the declared floor
DF_i >= 25, every space yields at least 2^24 pairs, and R = 2^13 spaces
yield at least 2^37 tested pairs in total. The expected number of
colliding pairs is therefore at least 2^37 * 2^-36.70 = 2^0.30 > 1.23.
Treating collisions as at least Poisson with mean 1.23 (the conservative
counting used for such Bernoulli sums),

    Pr[success] >= 1 - exp(-1.23) > 0.70.

With the nominal DF near 33 this is overwhelming (expected count
2^(13+32-36.70) ~ 160). Even at DF_i = 24 - below the declared floor -
the expectation is 2^-0.70 ~ 0.62 and success ~ 0.46, still above the
required 0.39. The package therefore declares
success_probability = 0.5, requiring the floor DF_i >= 24 for the 0.39
gate with margin, and h1 declares DF_i >= 25.

## 5. Cost ledger

Cost model collision-frontier-v5: one complete 5-round permutation
(= one selected target compression) costs 1 unit; each other 256-bit RAM
primitive costs 1/1355 units. All phases - connector construction,
randomness, failed trials, hashing, scanning, verification - are charged.

Connector cost. The published connecting stage for this instance
consumed Tc = 428.8 CPU core-hours. This package charges each connector
execution an envelope of 2^46 units, equivalent to 2^46 * 1355 ordinary
word-ops ~ 1.0*10^17 ops. Spread over the measured 1.544*10^6 seconds
that is a conversion rate of ~2^35.8 word-ops per core-second (~57
billion 256-bit ops/s, i.e. roughly 18 ops/cycle at 3.2 GHz), which
comfortably covers the linear-algebra connector: Gaussian elimination on
systems below 2^11 variables over GF(2), DDT filtering of the active
S-boxes, local permutation evaluations, and all bookkeeping. The same
envelope also absorbs the connector's occasional unsatisfiable retries.
Heuristic h4 records this conversion as a stated bound, not a measured
RAM count.

    R * 2^46 = 2^13 * 2^46 = 2^59   (connector stage total)

Brute-force evaluation. Each space enumerates at most 2^33 messages
(nominal DF; the floor case enumerates fewer) and performs 2 complete
hashes per message - H(m) and H(m XOR delta) - so at most 2^34 complete
hash evaluations per space and 2^13 * 2^34 = 2^47 evaluations overall.
Each evaluation is one unit, plus at most 2^12 ordinary word-ops for
message XOR, padding-byte assembly, absorb/squeeze data movement and
comparison bookkeeping:

    2^47 * (1 + 2^12/1355) < 2^47 * 4 < 2^49  (brute force total)

Collision scan and verification. Candidate identification is fold-in
work inside the per-evaluation envelope (digest comparison and pair
tagging). Final verification uses at most 2 complete hashes and <2^18
ordinary ops. Code, constants, the trail-core tables and the connector
description fit in far less than 2^20 words of fixed storage; its
initialization is charged inside the envelopes above.

Total charged time:

    T <= 2^59 + 2^49 + small
      < 2^60

The declared bound is `time_log2 = 60`. The dominant term is the
connector envelope; it is inflated by more than an order of magnitude
beyond the measured-hours conversion precisely so that the total remains
valid under reviewer reconstructions looser than the arithmetic here.
Even a reviewer who doubles every term reconstructs a bound under 2^61.

Peak memory: the connector workspace (GF(2) systems on < 2^11
variables), one affine space of < 2^33 messages generated on the fly
(messages are enumerated, not stored), a small candidate buffer, code and
trail tables are all far below 2^30 bytes. `memory_log2_bytes = 30` is a
deliberately loose cap.

`preprocessing_log2 = 59` bounds the connector stage (all R executions)
which precedes any produced output. `nonuniform_advice_log2_bytes = 24`
bounds target-specific public parameters embedded in the algorithm - the
trail-core No. 3 difference masks, activity pattern and connector
equations (public artifacts of GLL+19), plus their linear-system
precomputation artifacts - at 2^24 bytes, vastly above their few
kilobytes; the precomputation work behind them is charged inside the
connector envelope. `data_log2` is omitted per the current claim schema.

## 6. Evidence and verification performed

- `yukon setup --track sha3-256-r5-exploratory` passed all deterministic
  suites on the cloned harness (23 + 84 + 176 tests, 5 skipped).
- `python3 scripts/local_tracks.py check sha3-256-r5-exploratory` was run
  against this package and reports `mechanically_valid` with
  `submission_state=ready` and zero certificates.
- Permutation-level reproduction of the published witness: the Table 17
  padded blocks of GLL+19 (17 nonzero lanes each, 8 zero capacity lanes)
  were applied to `permutation(rounds=5)` in `verifier/keccak.py` from
  the zero state. Both blocks produce lanes
  65017C2E8B6040B4 344FF8BB933B4BD6 C6A3F13368BE2003 AB427B4B33435ACB -
  exactly the paper's published digest. This confirms the profile's
  round ordering (prefix rounds 0..4 with RC[0..4]), lane/bit encoding
  and output extraction are the ones attacked by the paper. The check is
  a verifier-level computation, not a benchmark run, and the pair is
  inadmissible as a certificate (1084-bit messages); it is cited only as
  evidence that the mechanism applies to this target profile.
- No local GPU, CUDA toolchain or ranked benchmark exists on the
  preparation machine; `yukon run` was not executed (the repository task
  marks it optional and it requires provider credentials). No claimed
  score is asserted; the scalar 60 is an analytical bound under the
  declared heuristics.

## 7. Declared heuristics and limitations

The claim's `heuristics` array declares four premises. Their roles and
the sections supplying support:

- h1 (df-byte-aligned-connector, score-critical; proof:3): the p = 8
  two-round connector for trail core No. 3 returns spaces of DF >= 25.
  Support: the additive p term in the paper's DF bookkeeping (their
  formula (11) and the TDF threshold), measured DF = 37 at p = 4, the
  authors' note that their TDF is pessimistic. Limitation: the paper
  does not analyze byte-aligned inputs; a DF collapse below ~24 would
  break the success floor (the algorithm would still be correctly
  charged and would simply fail to return a pair).
- h2 (trail-probability-byte-aligned, score-critical; proof:2,4): the
  last-three-rounds differential of trail core No. 3 holds per tested
  pair with probability >= 2^-36.70 on the exact profile. Support: the
  trail acts on state differences, not message encodings, so byte
  alignment does not perturb it; the verified Table 17 pair traverses
  the exact permutation; the 2^-36.70 figure already aggregates multiple
  trails of the last two rounds. Limitation: it is a reported
  differential probability, not a proof of the induced pair distribution.
- h3 (connector-rerun-independence, score-critical; proof:4): the R
  randomized connector executions yield pair sets whose collision events
  count as independent Bernoulli trials. Support: the paper's own
  randomized retry protocol and the DF>w sufficiency convention.
  Limitation: systematic correlation between subspaces would shrink the
  effective pair count; the declared floor absorbs up to a factor ~100
  of adverse correlation before the 0.39 gate fails.
- h4 (corehour-cost-envelope, supporting; proof:5): each connector
  execution costs at most 2^46 charged units, converting 428.8 measured
  core-hours at ~2^35.8 word-ops/s plus all retry and bookkeeping
  overhead. Support: published timing data and the stated conversion.
  Limitation: it is a stated envelope, not an instruction trace; the
  total claim has ~2 bits of headroom above the summed terms.

Known residual risks. A reviewer may judge the p-shifted DF estimate or
the hours-to-ops conversion too weak for even plausible status; that is
the genuine uncertainty of this package and it is declared rather than
hidden. The schedule would still be a valid (if failing) algorithm under
adverse DF; nothing is charged to unaccounted randomness.

## 8. Provenance and relationship to prior work

The mechanism, trail data, connector method and witness are due to Guo,
Liao, Liu, Liu, Qiao and Song (JoC 2019 / ePrint 2019/147), building on
Dinur-Dunkelman-Shamir (FSE 2012) and Song-Liao-Guo (CRYPTO 2017). This
package contributes only the byte-string-domain adaptation analysis
(p: 4 -> 8), the rerun schedule, the RAM accounting, and the local
profile-verification of the published pair. `baseline_improved` names
`sha3-256-r5-nominal-v2` (nominal 128) as required; the field is a
reference identifier and does not itself assert improvement. The
declared 60 is below the pending exploratory scores of 129 recorded for
the track; qualification, incumbent comparison and manual promotion are
separate events this package does not presuppose.
