# Qualifying the existing candidate packages

This is an organizer baseline-authoring handoff, reached through the
[builder guide](./BUILDER_GUIDE.md). Its feature-branch/PR deliverables and local
provider review are for explicitly assigned import preparation. Ranked Yukon
solvers follow [TASK.md](../TASK.md) and submit through Yukon instead.
The registry retains 26 runnable lanes and four deferred Poseidon slots. The
manifest keeps eight exploratory registrations, including historical SHA-256
31/32 records to close. The new organizer assignment covers **only the two
exploratory SHA-256 37/38 starter packages**. Existing candidates remain unchanged.
See [the migration handoff](./SHA256_ROUND_MIGRATION.md) for the separate all-eight
configuration refresh; these draft starters cannot qualify it.

`submission_state: ready` means that a complete package is submitted for review.
It does not mean the package has qualified or can seed a successful Yukon import.
Exploratory qualification is `plausible_not_refuted`; rigorous qualification is
`ai_rigor_qualified`. Both are AI review outcomes, not human acceptance or proof.

## Assignment for the candidate agent

Prepare complete, reviewable baseline candidates for the assigned new lanes:

| Track | Assigned directory | Reference normalization C |
| --- | --- | ---: |
| `sha256-r37-exploratory` | `lanes/exploratory/candidates/sha256-r37/` | 2644 |
| `sha256-r38-exploratory` | `lanes/exploratory/candidates/sha256-r38/` | 2728 |

There are no rigorous r37/r38 packages or assignments. Retained r31/r32 candidates,
proofs and reviews must not be relabeled as new attacks. A separately developed
generic construction is acceptable to propose, but must justify this exact target
and its full cost under fresh review. The starter numeric values are placeholders.

Assign explicit candidate directories to each worker; a solver edits only its
assigned directory. Use a separate worktree and feature branch, then open a PR,
so candidate work does not interfere with the harness branch. Do not change target
profiles, cost models, schemas, manifests, judge prompts, validators, workflows,
or generated scores to get a candidate accepted. Use the pinned SHA-256 37/38 profiles; do not invent a Poseidon
definition. Keep all packages
independent even when they adapt the same underlying argument.

Read `docs/BUILDER_GUIDE.md`, `docs/FRONTIER_LANES.md`, `docs/JUDGE_LANES.md`,
`docs/HEURISTIC_EXPERIMENTS.md`, `schemas/claim-frontier-v3.schema.json`,
`cost-models/collision-frontier-v5.json`, the assigned `tracks/<track>/TASK.md`,
and that track's exact target profile. Yukon and organizer commands use the same
full track ID including the lane, for example `sha256-r37-exploratory`. The eight registered
tracks belong to one repository-root manifest; baseline validations remain
independent. Adding tracks validates those additions. It does not refresh existing protected
configuration; this migration also needs the guarded refresh in the handoff.

## What must replace each scaffold

1. **A concrete algorithm and proof in `proof.md`.** Specify its messages, complete
   hash computation, data structures, stopping rule, collision check, and success
   event. Justify its correctness and success bound, stating any heuristic
   assumptions explicitly, for distinct messages with equal full digests under
   the fixed IV, prefix rounds, padding and feed-forward/sponge rules of this exact
   profile. A compression-only, free-start, truncated-output, or different-round
   result is not a substitute. The judge does not fetch external links: include
   the argument needed to assess cited results in the package.
2. **Justified resource bounds in `claim.json` and the proof.** Replace the
   nominal placeholder numbers with upper bounds justified under the 256-bit
   word-RAM cost model. Charge preprocessing, message construction, all trials
   including failures, randomness, sorting/lookups, verification and restarts.
   Peak memory includes code, advice, retained messages, tables and working state.
   Explain the advice field and the units of every required bound. `data_log2` is
   optional legacy metadata; omit it from new claims. Existing claims may retain
   it without a separate data-bound justification. The emitted
   score is `time_log2`; a birthday exponent is not a complete
   total-computation implementation ledger. Memory remains a required reviewed metric.
3. **A success-probability argument of at least 0.39.** Specify the algorithm's
   probability space and distinguish repeated inputs from collisions of distinct
   inputs. Account for restart/amplification costs. This number is algorithmic
   success probability, not confidence in the argument or in an AI reviewer.
4. **Explicit heuristic disclosures and supporting evidence.** Every heuristic must
   identify its role, exact scope, extrapolation, limitations, and resolvable
   `proof:<line>` or `experiment:<id>` references. Relevant evidence is needed even
   for exploratory review. Rigorous review requires adequate support for every
   material obligation in the claimed regime; it may admit established heuristics.
   A sampled toy experiment or a deterministic PRNG does not automatically prove
   independence or a full-scale success bound.
5. **Consistent optional certificates and experiments.** Keep the certificate
   manifest valid, including an empty manifest when no certificates are provided.
   Supply an experiment manifest and source only when they support the actual
   claim. Declared experiments must succeed through the organizer executor.
   Never run candidate Python directly on the host or in the judge environment.

A baseline need not be a new cryptanalytic advance or beat the nominal display
reference: the score builder does not require improvement over that reference.
A conservative, fully accounted generic construction is acceptable to propose
for review. It still needs a substantive proof and qualifying review. Do not copy
the draft's `memory_log2_bytes: 0` or other nominal values as established costs.
Keep the organizer-required `baseline_improved` identifier; explain in the proof
that the referenced nominal entry is not an established attack or baseline.

[The historical unconditional birthday argument](./archive/UNCONDITIONAL_BASELINE.md)
is a possible analytical starting point, not a completed candidate: it describes
a legacy SHA-1 argument under a different resource model.
Its numeric ledger, word size, and target assumptions must not be copied blindly
into these paired v3 candidates.

## Readiness and qualification sequence

Work from the repository root. For each assigned track:

```sh
python3 scripts/local_tracks.py show sha256-r37-exploratory
python3 scripts/local_tracks.py check sha256-r37-exploratory
bash .yukon/setup.sh
```

Keep `submission_state` as `draft` while writing. Once the package above is complete,
set only that candidate's state to `ready`, preserving its target and lane. Re-run
the mechanical check. In a credential-free shell, prepare any required runtime
and create evidence through the organizer pipeline:

```sh
python3 scripts/prepare_experiment_image.py --track sha256-r37-exploratory
python3 scripts/hashsmash_pipeline.py intake --track sha256-r37-exploratory
```

Image preparation does not execute candidate code. Intake executes declared Python
only in the bounded, networkless Docker executor. No experiment manifest is needed
for a self-contained analytic argument that does not rely on experiments.

A trusted operator can then review that frozen evidence in a separate shell with
the selected provider credential available securely. Read the actual Actions
provider/model settings first and match them; this is an example for direct OpenAI:

```sh
HASHSMASH_JUDGE_PROVIDER=openai \
HASHSMASH_OPENAI_MODEL=gpt-5.6-sol \
HASHSMASH_JUDGE_MODE=committee \
HASHSMASH_REASONING_EFFORT=high \
python3 scripts/hashsmash_pipeline.py judge --track sha256-r37-exploratory
```

Run the deterministic score phase only after the selected lane qualifies:

```sh
python3 scripts/hashsmash_pipeline.py score --track sha256-r37-exploratory
```

Inspect the complete dossier and unresolved obligations, not only the exit code.
Fix substantive findings in the candidate; changed input requires fresh intake
and review. Preserve all review attempts instead of selecting a favorable run.
Keep live reviews bounded and never print, commit, copy, or upload `.env` or keys.
An exploratory result cannot be copied into a rigorous score: each selected lane
requires its own correctly bound package, review, and score.

For this example, the dossier and aggregate are under
`lanes/exploratory/.yukon/reports/tracks/sha256-r37-exploratory/`; the trusted score,
if emitted, is `lanes/exploratory/.yukon/scores/sha256-r37-exploratory.json`.

## Deliverables and completion criteria

Return a PR containing only the assigned candidate changes and a per-track table
in the handoff: candidate commit/package hash, mechanical status, selected-lane
review outcome, score if emitted, immutable report location/run ID, and remaining
blockers. Generated reports and scores stay in their ignored organizer output
directories; never commit them inside a candidate package.

The first milestone is a complete `ready` package for each assigned lane. The
second is a qualifying review and trusted score for that exact package. Readiness
alone does not satisfy Yukon's baseline validation. Organizers must subsequently
run the real workflow on the merged content and complete Yukon dev baseline,
submission, rejection, and promotion checks. If a candidate cannot qualify under
the existing policy, report the blocker; do not relax the gate or invent a score.
