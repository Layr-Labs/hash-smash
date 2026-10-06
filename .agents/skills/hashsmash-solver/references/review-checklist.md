# Candidate review checklist

Use this when a candidate is ready for critique or a review identified a defect.
The current target profile, claim schema, cost model and review policy remain
authoritative. These questions supplement them with recurring failure cases.

## Target and construction

- Do the two messages meet the domain, differ, and collide on the complete
  selected hash and all required digest bits?
- Does a paper use the same IV, padding, rounds, capacity, digest length and
  message constraints? State the missing conversion instead of assuming it.
- Can a reviewer reconstruct the algorithm from the package alone? Cited
  external pages are not fetched by the judge.
- Do proof, pseudocode and experiment agree on masks, sorting keys, joins, loop
  bounds and failure handling? After a code correction, search the proof for
  the old description.

## Probability and heuristic support

- What is the algorithm's exact random experiment, success event and stopping
  rule? Are dependence assumptions and seed expansion disclosed?
- Are preprocessing, failed trials and repetitions included in the claimed
  success budget? A successful sampled run is not an expected-cost proof.
- Does each score-critical heuristic identify supporting evidence, scope,
  extrapolation and limitations? A local differential count does not justify
  multiplying probabilities across dependent rounds.
- Is a partial output-mask event being distinguished from a full collision?
  Missing evidence and a concrete counterexample require different conclusions.
- Does an unsuccessful search establish only the tested restriction? Do not
  generalize it into an impossibility theorem or invent odds for future success.

## Cost and storage

- Recompute the total in the selected cost units, including randomness,
  initialization, sorting, lookup, failures, recovery, preprocessing and advice.
  Do all terms listed in prose actually appear in the total?
- Are complete compressions and their individual operations counted only once?
  Are partial computations priced by their actual operations?
- Does claimed time count all processors' computation rather than elapsed time?
- Are table regions disjoint, addresses representable, and indexing operations
  charged? Include scratch buffers, code, constants and retained randomness in
  memory. Uninitialized storage needs an explicit valid access argument.
- Does the final logarithmic bound round conservatively and justify the stated
  success probability? A nominal exponent is not the current promoted score.

## Package and feedback

- Are manifest references valid, including an explicitly declared empty
  certificate manifest when present? Are proof-line references still correct?
- Are experiments declared in the approved format? Never run candidate source
  directly, including a copied version or a mock runner on the host.
- Run the mechanical checker after edits. Freeze a snapshot for critique;
  changed bytes require a new review packet.
- Missing local experiment results mean the critic has incomplete evidence.
  Official remote intake may still execute the declared experiment; do not
  report an invented pass, probability or failure in its place.
- For each critique, either fix the argument or explain the disagreement using
  exact evidence. Avoid asking successive critics until one agrees.
- A private preflight and a remote qualification can disagree. Preserve the
  distinction between advisory feedback, official AI review, human acceptance
  and successful promotion.
