# Paired exploratory and rigorous judge policy v1

Both lanes review the same exact target, rounds, submitted cost vector, heuristic
disclosures, and organizer evidence. The initial roles independently evaluate
minimum evaluability, cryptanalysis, resource accounting, and experiments.

Exploratory qualification is `plausible_not_refuted`: the submission is concrete,
has relevant supporting evidence, and has no concrete fatal finding confirmed
after a defender and adjudicator examine it. Plausible or unresolved material
obligations remain visible in the dossier. Heuristics without relevant supporting
evidence fail the shared minimum evaluability gate. A cited additional heuristic
discovered by a reviewer remains visible and must be covered by both substantive
roles before rigorous qualification.

Rigorous qualification is `ai_rigor_qualified`: every material obligation is
discharged to ordinary cryptanalytic standards; every score-critical heuristic
has adequate support for its exact claimed regime; the reconstructed resource
bounds support the submitted claim. This can admit established heuristics. It is
neither formal verification nor human acceptance.

All declared heuristic IDs must be reviewed by both cryptanalytic and experiment
roles. Algorithmic success probability never encodes confidence in a reviewer or
heuristic. No numerical model confidence or majority threshold controls a lane.
Evidence-sensitive failure rates require a labeled calibration corpus and human
evaluation; they are objectives, not measured guarantees of this initial policy.

Only a cited fatal finding confirmed by the adjudicator after a defender review
produces `refuted`. Missing details produce `not_evaluable`; unresolved material
obligations produce `not_qualified` in the rigorous lane. Provider, schema, missing
stage, binding, or challenge-coverage failures produce `infra_failed` in both lanes
and never produce a score. Drafts never reach inference.

A supported reconstruction that contradicts the submitted cost or success bound
must include a cited fatal finding linked to the affected cost obligation. Without
one, the review is internally inconsistent and fails closed. An explicitly
unresolved reconstruction can remain exploratory. A declared experiment requires
a passed execution report; not_requested cannot satisfy a declared manifest.

Every refuted heuristic must link to its own fatal finding. Dismissing that finding
changes its effective status to pending_reassessment, while preserving the critic's
original record. This can restore exploratory eligibility, but a new substantive
assessment is needed before treating the heuristic as established for rigorous
qualification.

The paired policy applies only to explicitly selected paired tracks. Archived
unconditional-v1 tracks retain their original semantics and fingerprints.
