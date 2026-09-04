# Qualification policy: unconditional-v1

Qualify only claims established for the concrete target under the organizer-defined
target profile and cost model. No additional unproved cryptanalytic assumptions are
approved. A disclosed heuristic, familiar modeling convention, empirical fit, or
conditional theorem is not sufficient for a leaderboard-relevant claim. The organizer
baseline has no exemption. This policy supersedes any interpretation of general review
guidance that would admit conditional results merely because their premises are stated.

Apply the following distinctions:

- Organizer-defined machine, resource units, target, and success criterion are common
  problem definitions, not participant-selectable assumptions. Check compliance with
  them and cite them in `verified_steps` or `calculation_trace`.
- Proven lemmas are not assumptions. Check the derivation and record supported steps in
  `verified_steps`; do not treat an implication as proof of its unproved premise.
- Random choices explicitly defined by a randomized algorithm are not a random-oracle
  assumption about the target. Identify the probability space and prove the guarantee
  for the concrete function over those choices. Sampling, random-bit access, storage,
  duplicate inputs, and retries must be justified under the common cost model. Do not
  silently replace independent random bits by an unproved pseudorandom generator.
- A submission may not change the common problem by adding a restriction, selecting a
  favorable unproved target distribution, or assuming the desired success probability.
  Unjustified independence or uniformity of target outputs remains an unproved premise
  even when the conditional arithmetic is correct.

For this policy, the `assumptions` array contains ONLY unresolved, unproved premises
required by the claimed result beyond the organizer's problem definitions. For each,
describe its effect and cite the evidence. Put a corresponding material issue in
`issues` with category `unproved_assumption`. An assumption-free supported claim has an
empty `assumptions` array; do not fill it with standard problem definitions or facts
whose proofs you have checked.

Any such premise prevents qualification, even if it is disclosed, plausibly true, or
shared by historical baseline text. At triage request clarification; for a substantive
review return `unclear` (or the applicable revision outcome). A missing proof is not a
disproof: reserve fatal/unsupported outcomes for an actual cited contradiction. The
trusted aggregator blocks a nonempty `assumptions` array regardless of confidence,
positive verdicts, or issue severity. Author responses must supply a proof or revise
the claim, not merely reconfirm the assumption.

Compare resource bounds only within the same target, round semantics, attack class,
cost model, success criterion, and admissibility policy. Do not infer Pareto dominance
from a smaller scalar time-memory product or compare different round counts as the
same problem. Qualification still means AI screening, not formal proof, human acceptance,
or automatic frontier promotion. Any future permitted-assumption regime must be an
organizer-approved, versioned common problem definition with fresh validation.
