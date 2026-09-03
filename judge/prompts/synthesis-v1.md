Create a concise human-review dossier from the original untrusted evidence,
independent reviews, adversarial review, and any author response. Preserve
disagreements; do not vote, average confidence, or turn agreement into proof. For each
material claim record the evidence, strongest objection, resolution status, unknowns,
and the exact human decision needed.

Set `decision` to null and `verdict` to `advance`, `request_revision`,
`seek_specialist`, or `reject`. Both cost vectors must be null and the calculation trace
empty. `reject` requires at least one specifically cited fatal issue. The recommendation
is nonbinding; an AI result never represents human acceptance or formal verification.
