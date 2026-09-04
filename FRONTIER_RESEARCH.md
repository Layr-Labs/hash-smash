# Collision-frontier roster research

Research date: 2026-09-04. This is an organizer research note, not a qualified
baseline, proof of security, or substitute for a frozen target profile.

## What the mockup establishes

The [mockup data](https://zooko.github.io/hashsmash-webdesigns/hashsmash-data.js)
names seven families: MD5, SHA-1, SHA-256, BLAKE3, Keccak[1600],
Keccak[800] with rate 544/capacity 256, and an explicitly provisional Poseidon
profile. The file explicitly identifies all its records as synthetic UI data.
Consequently its illustrated costs and last attacked rounds cannot establish
the challenge roster. Its Poseidon field, width, and round schedule are marked
TBD; its Keccak[1600] row does not specify rate, capacity, padding, or output
length. Its linked [Lean SHA-3 paper](https://eprint.iacr.org/2024/1880) is an
implementation paper, not a collision-frontier source.

Seven families × two round settings × two judging lanes = 28 lane slots. A slot
can be reserved without claiming that its target or frontier has been established.

## Recommended selections and unresolved entries

| Family | Recommended pair | Status and precise interpretation |
| --- | --- | --- |
| MD5 | 63 / 64 steps | Explicit full-round-control exception. Full 64-step MD5 is collision-broken; there is no first unbroken round within the standard algorithm. |
| SHA-1 | 79 / 80 steps | Explicit full-round-control exception for the same reason. |
| SHA-256 | 31 / 32 steps | User-selected pair, consistent with the classical ordinary-collision literature inspected. Freeze standard IV, first `r` steps in every compression call, full 256-bit output, and normal message padding. |
| Keccak[1600] | 5 / 6 rounds of SHA3-256 | Recommended concrete instance: width 1600, rate 1088, capacity 512, output 256, SHA-3 domain suffix `01`, first `r` rounds. Actual 5-round collisions exist; the inspected literature does not provide a classical ordinary-collision attack on 6-round SHA3-256. |
| BLAKE3 | Unresolved | The inspected sources do not establish an exact ordinary-collision boundary. Reserve both round slots pending a matching result; do not infer it from compression-function or keyed-permutation attacks. |
| Keccak[800], r544/c256 | Unresolved | Preserve these requested rate/capacity values. The common 800-bit Crunchy result is instead r640/c160 and cannot establish this boundary. Output length and padding also need freezing. |
| Poseidon | Unresolved | A concrete parameter set, mode, output, and full/partial round reduction rule are needed before a meaningful boundary can be named. |

The MD5/SHA-1 exception requires organizer acknowledgment because it changes the
selection criterion, although it preserves the requested two settings per family.
Do not create nonstandard MD5 step 65 or SHA-1 step 81 to manufacture an
unbroken setting. Even a known full-round collision does not automatically prove
that the same pair collides after removing the last step.

For the unresolved rows, using a convenient pair as a local exploration target
is possible, but its status must be `provisional` or `boundary_unverified`.
There is no evidence-based way to describe all 28 slots as verified frontier
lanes from the material reviewed here.

## Evidence for the usable pairs

### MD5 and SHA-1

The original [MD5 collision report](https://eprint.iacr.org/2004/199) establishes
full MD5 collisions. [SHA-1 is a Shambles](https://eprint.iacr.org/2020/014)
reports both ordinary identical-prefix and chosen-prefix collision methods
against full SHA-1, including an executed chosen-prefix result. These are good
positive controls for judging established cryptanalysis. Published operation
figures are not automatically this repository's time-memory scores.

### SHA-256

[New Records in Collision Attacks on SHA-2](https://eprint.iacr.org/2024/349)
distinguishes ordinary collisions from semi-free-start and free-start results.
The latter reach higher step counts but grant control over the chaining value
and are not ordinary collisions from the standard IV.
[The First Practical Collision for 31-Step SHA-256](https://doi.org/10.1007/978-981-96-0941-3_8)
provides a direct primary publication for the lower setting. The 31/32 pair is
therefore sensible. Absence of a located 32-step result is a literature status,
not a lower-bound theorem. Padding and multiple-block composition must agree
with the profile before importing any witness or cost argument.

### Keccak[1600]: prefer SHA3-256 5/6

[Practical Collision Attacks against Round-Reduced SHA-3](https://eprint.iacr.org/2019/147)
reports actual collisions for 5-round SHA3-256, SHA3-224, and SHAKE128, while
its 6-round practical result concerns the lower-capacity Crunchy instance.
[Exploring SAT for Cryptanalysis](https://eprint.iacr.org/2022/184) gives a
classical 6-round SHAKE128 attack with reported time `2^123.5`, but explicitly
distinguishes its 6-round SHA3-256 result as quantum. The latter is ineligible
in a classical track. The [Keccak designers' current cryptanalysis list](https://keccak.team/third_party.html)
and [2024 probabilistic-linearization paper](https://eprint.iacr.org/2024/1136)
do not establish a later classical 6-round SHA3-256 attack. This supports 5/6
as a dated literature selection for SHA3-256.

SHA3-256 is only one possible instantiation of the mockup's Keccak[1600] row.
Selecting SHAKE128 with rate 1344/capacity 256/output 256 instead gives a
time-based literature pair of 6/7. Its 6-round result is close enough to the
nominal 128-bit threshold that exact memory and cost accounting are material;
do not silently copy `123.5` as `log2(T*M)`. Selecting legacy Keccak padding
instead of SHAKE padding also requires a matching attack/transfer argument.

## Why the remaining boundaries are unresolved

### BLAKE3

The [official BLAKE3 specification and analysis](https://github.com/BLAKE3-team/BLAKE3-specs/blob/master/blake3.tex)
separate keyed permutations, compression functions, and the ordinary hash.
Their differential-trail table is not a table of collision attacks. A trail
with nonzero output difference, or one requiring an attacker-selected chaining
value, is insufficient for the requested task. The ordinary-hash row considers
up to two rounds and does not establish an ordinary-collision frontier.

[New Boomerang Attacks on BLAKE](https://eprint.iacr.org/2023/299) attacks the
keyed permutation of full seven-round BLAKE3 at reported complexity `2^180`.
This neither breaks the 128-bit ordinary-collision claim nor supplies a lower
ordinary-collision boundary. BLAKE/BLAKE2 results cannot be inherited without
checking changes in initialization, flags, schedule, and output formation.

A concrete BLAKE3 profile is straightforward: unkeyed BLAKE3, standard IV,
256-bit output, prefix round reduction in every compression invocation, and
unchanged tree/chunk/counter/flag/output semantics. Choosing two numerical
rounds remains an organizer exploration choice until a matching attack is
located or established. A fixed-length one-block simplification is a distinct
target and must be named as such.

### Keccak[800], r544/c256

The [Crunchy contest](https://keccak.team/crunchy_contest.html) fixes capacity
160 and collision output 160 across all widths. Its 800-bit instance therefore
has rate 640. It permits any consecutive round subsequence, not necessarily
the first rounds. Its 5-round solution does not establish a result for
rate 544/capacity 256/output 256 with prefix round reduction.

[New Collision Attacks on Round-Reduced Keccak](https://eprint.iacr.org/2017/128)
likewise specifies the actual 800-bit target as `[640,160,160]`; the paper's
round and capacity assumptions are explicit. No inspected primary result
established a 5/6 or 6/7 boundary for the requested `[544,256,256]` instance.

Recommended concrete definition if retaining the requested family: width 800,
32-bit lanes, rate 544, capacity 256, output 256, zero initialization,
`pad10*1`, no extra domain suffix, first `r` rounds, and ordinary sponge
messages. This is an organizer-defined Keccak instance, not SHA3-256 or
SHAKE128. Its full permutation has 22 rounds. Fixing that definition makes
implementation possible but does not supply the missing frontier evidence.

### Poseidon

The [original Poseidon paper](https://eprint.iacr.org/2019/458)
defines a family parameterized by field, width, power map, linear layer,
constants, and full/partial round counts. The paper's design security margins
are not observed ordinary-collision boundaries. Reducing a scalar total round
count without specifying which full or partial rounds are removed changes the
problem ambiguously.

A currently well-documented starting point is the [EF Poseidon initiative](https://www.poseidon-initiative.info/home)
and its [verifier repository](https://github.com/khovratovich/poseidon-tools):
Poseidon1 over KoalaBear `p=2130706433`, width 16, power map `x^3`. Its collision
challenge uses fixed-domain compression on fifteen input field elements and
compares the first `q` output elements. Its CICO challenges are a different
problem. Neither provides a first-unbroken ordinary sponge-collision boundary.

If adopting this set, pin an exact verifier/parameter commit, MDS matrix,
constants, domain element, output count, canonical field encoding, full-round
count, partial-round count, and reduction schedule. A collision target with
`q` output elements has output space at most `p^q`; its generic output-size
exponent is `q*log2(p)/2`, not automatically 128. For a sponge, capacity imposes
an additional limitation. A guessed 30/31 pair from the mockup has no authority.

## Cost and round conventions required before publication

The literature commonly compares time against the nominal birthday exponent
`n/2`. This repository ranks `log2(T*M)` in explicit time and memory units.
A table birthday search has approximately `T=2^(n/2)` and
`M=2^(n/2)` entries, hence product exponent near `n`, before overheads. A
constant-memory cycle search has a different analysis and can have a different
product. Consequently a nominal 128-bit display reference must not be
presented as the measured score of a particular table algorithm. Preserve both
the conventional nominal collision-security exponent and the cost-model
reference, and label which criterion selected the rounds.

For SHAKE128's reported `2^123.5` time, even a few additional memory bits in
the exponent can change whether the attack beats a literal `T*M < 2^128`
threshold. That audit is necessary if 6/7 is chosen instead of SHA3-256 5/6.
For the latter, the practical 5-round result has a much larger margin, but a
qualified score still needs the ordinary resource review.

The [Keccak specification summary](https://keccak.team/keccak_specs_summary.html)
defines lane layout, round constants, padding, and standardized domain
suffixes. Prefix round reduction uses constants numbered from zero. This is
different from standardized Keccak-p reduced-round permutations, which retain
the last rounds of Keccak-f. Record the start index explicitly and never
substitute one for the other when verifying a published collision.

Every imported record should carry the exact target fingerprint, attack class,
classical/quantum setting, round start/count, output size, reported time and
memory with units, heuristic qualifications, source version, and the organizer's
translation into the challenge cost model. A nominal reference or unlocated
attack is not a qualified baseline in either judging lane.
