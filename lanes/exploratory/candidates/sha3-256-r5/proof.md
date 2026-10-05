# Five-round SHA3-256 collision via conditional internal differentials, time_log2 = 106.5

## 1. Claim and scope

Target `sha3-256-r5-prefix-v1`, lane exploratory, attack class ordinary collision.
The selected hash is the complete FIPS 202 SHA3-256 sponge: all-zero 1600-bit IV,
rate 1088, capacity 512, suffix 0x06 then pad10*1, the first five Keccak-f[1600]
rounds (0..4) in every permutation, full 256-bit digest. No round-convention or
domain change.

This is a DISCONTINUOUS claim: instead of a constant-factor birthday improvement
it reports the published dedicated five-round collision attack, which costs far
below the 2^128 birthday bound. Under `collision-frontier-v5` (C = 1355, one
five-round sponge permutation = one unit):

| Resource | Upper bound |
| --- | --- |
| Total computation | 2^106.5 selected-permutation equivalents |
| Peak memory | 2^112 bytes (reported only) |
| Preprocessing (connector), inside total | 2^80 |
| Success probability | >= 0.5 |
| Nonuniform advice | 0 bytes |

This is an analytic complexity bound (no witness pair is exhibited); the full
construction is restated below so the judge needs no external link.

## 2. The published result

Five-round SHA3-256 (Keccak[r=1088, c=512], n=256) has three independent dedicated
CLASSICAL full-collision results for exactly these parameters (not near-collision,
not free-start, not reduced capacity):

- 2^105 (theoretical) -- Zhang, Hou, Liu, EUROCRYPT 2023, "Conditional Internal
  Differentials." Table 5: d in [256,320] -> "106 - 1 = 105"; Table 6:
  "SHA3-224/SHA3-256/SHAKE128, 5 rounds, 106 - 1 = 105"; Table 1 lists the SHA3-256
  5-round row as 2^105 (this work) and 2^115 (ref [9]).
- 2^115 (theoretical) -- Dinur, Dunkelman, Shamir, FSE 2013 (ref [9]); the 2023
  survey classifies it as a 5-round SHA3-256 full collision.
- Practical (real pair exhibited) -- Guo et al., J. Cryptology 2020; confirmed by
  Guo et al., ASIACRYPT 2022 ("the 5-round collision attacks on SHA3-256 ... by
  Guo et al. at JoC 2020").

So the true finding cost is at most practical, far below 2^105, itself far below
2^106.5. We charge 2^106.5 as a conservative upper bound established three ways.

## 3. The attack construction

Internal differential cryptanalysis (Peyrin; generalized by DDS) tracks the
self-difference of a single near-symmetric state under Keccak-f's 2-fold symmetry.
The EUROCRYPT 2023 attack on nr rounds has three stages:

- Stage 1, connector (improved TIDA). Solve, over GF(2), the linear systems from
  the differential transition conditions of the first two rounds, giving an affine
  space of initial messages. Five-round attacks use 2-block messages: M0 makes the
  system consistent (~2^25 first-block trials, each yielding ~2^21 solutions), M1
  ranges over the solution space. Cost is one-time Gaussian elimination.
- Stage 2, characteristic filter. For each candidate compute the internal
  difference after (nr - 1.5) = 3.5 rounds; conforming states go into disjoint
  collision subsets, non-conforming are discarded. This oversampling and rejection
  are already inside the paper's reported complexity (Section 4).
- Stage 3, variant birthday over disjoint subsets. Search each subset
  independently (store final-round outputs, stop at first collision). The
  variant-birthday relation (paper Eqs. 2-5) gives input count N and the collision
  probability.

For d = 256 the collision is placed on the first 5 lanes (320 bits) before the last
chi (paper: "For 256 <= d <= 320, find collisions on the first 5 lanes before the
last chi"); by bijectivity of chi on that row it propagates to equal first-320
output bits, containing the full 256-bit digest. Hence a true ordinary collision of
the complete hash, not a near-collision.

## 4. Parameters and the all-in figure (d = 256)

From EUROCRYPT 2023 Table 6 / Section 6.3: nr = 5 on rounds 0..4 with the original
round constants; 3.5-round characteristic (Characteristic 3) with transition
condition numbers (k2,k3,k4) = (21,18,16), which the paper states applies
identically to SHA3-256; degrees of freedom >= 540.

Table 5 gives the all-in total time complexity 2^{106-1} = 2^105 for d in [256,320].
This is the value of the Section 6.3 formula 2^{A + (m+16)/2}, verified against the
paper's worked d = 384 case (2^{18+(224+16)/2} = 2^138, matching Table 5). The
leading A already prices the connector oversampling and the Stage-2 rejection; the
(m+16)/2 term is the variant-birthday subset search. So 2^105 is the all-in EXPECTED
cost of generation, filtering, connector, and search combined, not a post-filter
count.

## 5. Mapping to the selected target

- Attack class: full fixed-IV collision of the complete SHA3-256 digest =
  ordinary-collision. Not a distinguisher, free-start, near-collision, or c=160
  contest instance.
- Domain/padding: standard SHA3-256; suffix 0x06 + pad10*1 are fixed bits absorbed
  within the 2-block message (DF >= 540 leaves ample freedom). The reference
  `_sponge` absorbs multiple rate blocks, each with the five-round permutation, so
  the 2-block message is hashed exactly as required.
- Rounds: prefix rounds 0..4 with original constants, per block. Matches the profile.
- Unit: one five-round sponge permutation = 1 unit; other 256-bit word ops = 1/C,
  C = 1355. The paper's figure is in reduced-round evaluations (its "bit operations"
  footnote applies only to the SHA3-512 polynomial-method row), so 2^105 maps to
  time_log2 ~ 105.

## 6. Cost accounting (refutation-class coverage)

Charging convention (F-COST-1, F-SUCCESS-SPACE): the model charges expected total
computation for success >= 0.39, counting all trials/failures. The paper's d = 256
figure 2^105 is exactly such an expected all-in total (Section 4); every trial and
failure is already inside it.

- Main search (F-TIME-CHAIN): each evaluated state is one five-round permutation
  from the connector state (the 3.5-round check is a prefix of it). We charge the
  paper's all-in 2^105 and conservatively double it to 2^106 as a full-pool /
  no-early-stop convention.
- Sorting/lookup (F-TIME-CHAIN): up to ~2^106 outputs stored/compared at 1/C each,
  < 2^103.
- Connector (F-COST-1): Gaussian elimination on systems of dimension <= 1600
  (< 2^33 bit ops each) with ~2^25 first-block trials; inputs enumerated from the
  affine description for free. Bounded by 2^80 (preprocessing_log2 = 80), already
  inside the total; added again as slack.
- Total (F-COST-1): 2^106 + 2^103 + 2^80 < 2^106.01; claim time_log2 = 106.5
  (> 0.49 bit margin), a strict upper bound on the published cost.
- Success (F-SUCCESS-SPACE): the variant-birthday argument returns a collision with
  probability close to 1 for the designed number of subsets, >= 0.5 at the charged
  budget. success_probability = 0.5 (>= 0.39). This is the algorithmic success
  event; it is separate from the heuristic's epistemic status.
- Memory (F-MEM-1): peak = one subset's hash table + affine descriptions; reported
  over-estimate 2^112 bytes (reported-only, no scalar weight).
- Experiments (F-EVAL-01): no experiment manifest is declared; the gate "does not
  require full-scale execution of an infeasible attack," and the one heuristic is
  supported by the cited peer-reviewed literature (Section 7).

## 7. Declared heuristic

One score-critical heuristic: the 3.5-round conditional internal-differential
characteristic partitions the constructed inputs into disjoint collision subsets on
which the map through the final rounds behaves as a random function, so the
variant-birthday count holds. This is the standard working premise of
internal-differential collision cryptanalysis. Evidence: the peer-reviewed
EUROCRYPT 2023 analysis (which additionally reports that its three-round instance's
observed colliding-subset count matched theory), DDS FSE 2013 (2^115), and the real
five-round SHA3-256 collision of J. Cryptology 2020. Declared in claim.json with
role score-critical, scope (5-round SHA3-256, c=512, n=256, rounds 0..4,
characteristic (21,18,16), d=256), extrapolation from the verified 3/4-round
instances, and the limitation that the 5-round figure is a theoretical estimate not
re-run at full scale here.

## 8. Evidence, provenance, limitations

Primary source reconstructed above: Zhang-Hou-Liu, EUROCRYPT 2023 (Tables 1/5/6,
Section 6.3). Corroboration: DDS FSE 2013 (2^115); Guo et al. J. Cryptology 2020
(real pair); Guo et al. ASIACRYPT 2022. This is an analytic upper bound with large
memory and infeasible work; no pair is exhibited (a witness would be rejected and
the claim is deliberately analytic). It rests on the declared internal-differential
heuristic and concerns only the five-round prefix variant, not full SHA3-256.

Model: Claude Opus 4.8. Harness: Claude Code.
