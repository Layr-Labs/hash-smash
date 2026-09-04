# Baseline-construction agent prompt

Copy the single prompt below and replace `{{TARGET}}` once with an algorithm/round
ID, **without a lane suffix**. Give each target to one worker in its own worktree.
The worker is assigned both lane candidates, with separate qualification required.

Currently supported targets: `md5-s63`, `md5-s64`, `sha1-r79`, `sha1-r80`,
`sha256-r31`, `sha256-r32`, `sha3-256-r5`, `sha3-256-r6`.

Defaults inside the prompt: six hours, two local CPU workers, 2 GiB of experiment
memory, and at most two live review panels per lane. A panel includes multiple
role calls and the configured adapter retries; this is not a dollar cap.
Creating this document does not launch workers, authorize a deployment, or run a judge.

```text
TARGET="{{TARGET}}"

Construct launch-baseline candidates for this HashSmash algorithm/round target.
Work autonomously in your assigned repository worktree, producing actual proofs
and packages rather than stopping at a plan. Aim to qualify a conservative common
construction in BOTH lanes: ${TARGET}-rigorous and ${TARGET}-exploratory.

The priority is an honest, auditable, accepted starting point—not a novel attack
or a record. A baseline may score worse than the nominal display reference; the
current local score gate does not require improvement over that reference.

Assignment and authority

- Record the starting commit and verify both IDs in the trusted registry before
  editing. If the target is absent or undefined, report that blocker; do not invent
  rounds, profiles, or a test-only substitute. Use your current worktree, not the
  shared original checkout, and preserve existing work.
- Your assigned candidate directories are exactly
  lanes/rigorous/candidates/${TARGET}/ and
  lanes/exploratory/candidates/${TARGET}/. You may also keep your own scratch
  calculations under .yukon/work/baseline-research/${TARGET}/ and write a handoff
  at baseline-research/${TARGET}/BASELINE_REPORT.md, outside the candidates.
- All other candidates and trusted profiles, models, schemas, registries,
  manifests, prompts, verifier code and workflows are read-only. Generated
  evidence/review/score artifacts may be written only by the trusted pipeline.
  Do not relax a gate, fabricate a score, copy a review across lanes, or turn a
  nominal reference into an allegedly qualified baseline.
- Default limits: six elapsed hours, two local CPU workers and 2 GiB of experiment
  memory. No extra agents, paid compute beyond the bounded judge runs below,
  dependency installation, scheduling, deployment, merge, push, or PR creation.
  You may commit your own assigned candidate changes and handoff on your worktree
  branch. Do not commit unrelated changes or generated raw reports/scores.

Read the contract

Read AGENTS.md, FRONTIER_LANES.md, JUDGE_LANES.md, HEURISTIC_EXPERIMENTS.md,
schemas/claim-frontier-v3.schema.json, cost-models/collision-frontier-v3.json,
both assigned tracks' TASK.md files, and the exact selected target profile.
Use python3 scripts/local_tracks.py show "${TARGET}-rigorous" and the equivalent
exploratory command to resolve the organizer definitions and paths.
Read PARTICIPANT_HEURISTIC_TEST.md for the live calibration's cost-accounting
and evidence limitations. The paired-lanes policy applies; the old unconditional
policy is not a blanket prohibition on properly supported heuristics here.

Construction strategy

Start with the simplest credible rigorous construction. Investigate a fully
accounted generic collision algorithm before attempting new cryptanalysis.
UNCONDITIONAL_BASELINE.md offers a distribution-free birthday argument as a
possible starting point, NOT a finished or qualified baseline. Recheck and adapt
its proof, domain, sampling, word size and ledger to this exact v3 target; its
legacy SHA-1 parameters cannot be copied into a 256-bit-output target unchanged.
A slower, fully justified fallback is preferable to an unsupported low score.

Research primary sources when useful, credit prior work, and explain how each
result matches this exact profile. The judge does not browse your citations:
include the necessary argument in proof.md. Do not execute an astronomically
large attack merely to qualify a baseline; use a substantive analytical argument
and feasible checks with precisely stated scope. Do not present a stored published
collision as a cheap algorithm while omitting its construction/preprocessing cost.

Required mathematical package

1. Specify the actual algorithm, messages, data structures, random coins (if any),
   stopping rule, failure handling and final distinct-message/full-digest check.
   Match the fixed IV, prefix rounds on every block/permutation, padding, domain
   suffix, feed-forward/sponge semantics and full output of the selected profile.
   A free-start, compression-only, truncated-output, different-padding or
   different-round result is not a solution to this target.
2. Establish success probability at least 0.39 for the stated algorithm. Separate
   repeated inputs from collisions between distinct inputs. Justify input-domain
   size, sampling distribution, dependencies and any restart/amplification costs.
   The model provides charged independent uniform 256-bit random words; a fixed
   PRNG is not automatically an equivalent probability space. Algorithmic success
   probability is not confidence in a heuristic or in the judge.
3. Provide explicit operation and peak-memory ledgers under collision-frontier-v3.
   Account for every selected-target compression/permutation, all other primitive
   operations, random-word generation, construction, sorting/lookups, failed
   trials, verification, preprocessing and restarts. Specify record layouts,
   comparisons, loop bounds, scratch reuse, code/constants, tables, stored messages
   and advice in bytes. Include complete loop-level pseudocode and enough counts
   to audit the constants. Avoid unexplained large allowances for an unspecified
   implementation; conservative bounds still need justification.
4. Derive every claim.json field, including data, preprocessing and advice, from
   that ledger. The scalar is time_log2 + memory_log2_bytes, not Pareto dominance.
   Keep the organizer's baseline_improved identifier while explaining that its
   nominal entry is only a reference. Do not reuse draft placeholder costs.
5. Explicitly list any heuristics with IDs, roles, scope, extrapolation, limitations
   and valid proof/experiment evidence references. Prefer avoiding unnecessary
   assumptions, but do not conceal necessary ones. Rigorous qualification can
   admit heuristics established to ordinary cryptanalytic standards; exploratory
   qualification requires relevant support and absence of a confirmed fatal flaw.

Experiments and packaging

Use experiments only where they strengthen a material claim. Preserve all trials
and failures; specify sampling, stopping, dependence, selection effects and what
is extrapolated. Finite successes, toy counts, seeded replay and observed runtime
do not automatically prove population probability or attack cost. Use only the
existing typed experiment interface. If it cannot check an essential internal
predicate, document the limitation rather than pretending it verified that fact.

Participant Python runs ONLY through the organizer's isolated executor. Do not
import, run, evaluate, or copy candidate code elsewhere for host execution, and
never run it in a credential-bearing process. Scratch arithmetic may check lemmas
and ledgers; it is not an alternative execution route for submitted programs.
Never supply a participant-generated report as trusted organizer evidence.

Produce substantive proof.md, schema-valid claim.json, a valid certificate manifest
(empty when appropriate), and only declared optional evidence files. Keep notes
and handoff material outside candidate trees. Keep incomplete work draft; set
ready only when the package is complete enough for substantive review. Write the
proof as an argument, not instructions telling reviewers what verdict to return.

Qualification and iteration

For each lane, set TRACK to "${TARGET}-rigorous" or "${TARGET}-exploratory" in
the shell running that phase. Use the explicit full ID and independent outputs:

  python3 scripts/local_tracks.py check "$TRACK"
  bash .yukon/setup.sh
  python3 scripts/prepare_experiment_image.py --track "$TRACK"  # only if needed
  python3 scripts/hashsmash_pipeline.py intake --track "$TRACK"

Run these preparation steps in a credential-free shell. Missing Docker or image
access is a setup blocker; there is no host fallback. An analytic package without
declared experiments need not use Docker. Freeze and commit the candidate before
live review; changed package bytes require new intake and review.

For at most TWO live review panels per lane, I authorize sending these assigned
baseline packages—their Markdown, declared Python and certificate/experiment
evidence—to AWS Bedrock for review using the existing local credential. No other
private files are authorized for upload. In a SEPARATE trusted child shell, load
/Users/robert/eig/hash-smash/.env for authentication only, with shell tracing
disabled and without printing, copying,
committing, or exposing its contents to a model. If that file or access is missing,
finish the offline work and report the blocker; do not change infrastructure.

After loading credentials, explicitly select the current deployment settings:
HASHSMASH_JUDGE_PROVIDER=bedrock
HASHSMASH_BEDROCK_MODEL=us.openai.gpt-5.6-sol
HASHSMASH_BEDROCK_REGION=us-east-1
HASHSMASH_JUDGE_MODE=committee
HASHSMASH_REASONING_EFFORT=high

Then run only:
  python3 scripts/hashsmash_pipeline.py judge --track "$TRACK"

Use the repository's role-committee configuration unchanged. Do not use the all
command or run-local-track.sh wrapper in the credential-bearing shell: preparation
and participant execution must remain separate from inference. After that shell
exits, use the secret-free deterministic score phase for a qualifying lane:
  python3 scripts/hashsmash_pipeline.py score --track "$TRACK"

Inspect all findings and both outcomes, not only an exit code. A second panel is
for a substantive candidate correction, not a lottery on unchanged inputs. Retain
every attempt and report adapter retries; ask before exceeding the panel budget.
Diagnose protocol or judge defects without modifying trusted code or concealing
unfavorable reviews. If only exploratory qualifies, preserve that partial result
and state exactly what still prevents a rigorous baseline.

Completion and handoff

Success requires an honest package, real selected-lane qualification and a trusted
score bound to the current package/configuration for EACH lane. Rigorous requires
ai_rigor_qualified; exploratory requires plausible_not_refuted. A rigorous result
in an exploratory dossier does not create the rigorous lane's score: submit and
review the correctly bound package in each lane separately.

Commit the assigned packages and BASELINE_REPORT.md. Report the construction,
sources, probability argument, complete cost vector, scalar, substantive remaining
assumptions, exact tests, per-lane verdicts, candidate commit/package hashes, and
archived run IDs/paths. Distinguish ready, mechanically valid, AI-qualified, scored,
and actually validated as a Yukon launch baseline. Local qualification is a handoff
for organizers to re-run the real workflow/import on merged content, not a claim
that deployment or human acceptance has occurred.

Stop when both baselines qualify and the handoff is complete; do not spend the
remaining budget optimizing. If time/review limits or a genuine blocker intervene,
deliver the best honest partial result, with incomplete packages left draft and
precise remaining obligations. Do not fabricate acceptance to finish the task.
```

The explicit outcome, authority and evidence boundaries follow
[official OpenAI prompting guidance](https://developers.openai.com/api/docs/guides/prompt-engineering).
This is prompt-structure guidance, not a model change or a launch authorization.
