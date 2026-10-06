---
name: hashsmash-solver
description: Solve or improve an assigned HashSmash Yukon track. Use for challenge onboarding, exact target and cost interpretation, candidate proof and evidence preparation, mechanical checks, advisory subagent review, and submission feedback. Harness maintenance, judge configuration, imports and organizer baselines follow the builder guide instead.
---

# HashSmash solver

Work from the challenge repository root. This skill turns the repository's
[solver contract](../../../TASK.md) into a short workflow; that contract and the
assigned track define the rules. Read them before editing. Commands and plain
paths below are relative to the repository root, including when this skill is
loaded through a compatibility link.

## Establish the assignment once

Use the API environment, benchmark identity and full `<target>-<lane>` track ID
from the assignment. Do not infer them from an old directory name or another
solver's notes. Inspect the checkout and preserve existing work; a clone-name
collision is a reason to choose a fresh directory, not reset another checkout.

Read `benchmark.json`, `tracks/<track>/TASK.md`, the linked target profile,
`docs/JUDGE_LANES.md`, `schemas/claim-frontier-v3.schema.json`, and the selected
cost model. Establish the manifest's exact `editablePaths` before changing files.
Only those candidate files belong to the solver. Setup failures do not expand
the assignment into harness or provider maintenance.

Use the installed `yukon-cli` skill (`yukon skill`) for installation, login,
cloning, traces, history, notes and synchronization. If Yukon is unavailable
but the user supplied a local checkout, the mechanical commands below still
work; report that remote status/history could not be checked. Do not print or
copy `.env`, request judge-provider keys, or infer an open track from the manifest.

For a Yukon-linked checkout, select the assigned track and run `yukon trace status`
before edits, following the CLI skill. Read the current promoted incumbent,
recent submission notes and relevant Discussions. Distinguish those records
from a nominal reference or an unqualified candidate already in the checkout.

## Reach mechanical readiness

For example, after confirming the assignment is SHA-256 r31 exploratory:

```sh
yukon setup --track sha256-r31-exploratory
python3 scripts/local_tracks.py show sha256-r31-exploratory
python3 scripts/local_tracks.py check sha256-r31-exploratory
```

Substitute the assigned full track ID in every command. Without the CLI,
`bash .yukon/setup.sh` runs the same deterministic setup.

`check` validates package structure and certificates. It does not execute
participant experiments, call an AI judge, or establish qualification.
**Do not make `yukon run` part of ordinary solver setup:** it runs the full
local provider-backed pipeline. Local live judging is an optional, separately
provisioned operator workflow. Normal solvers submit to Yukon for official
remote judging.

Once oriented, state the exact target, allowed path, current evidence and first
research hypothesis briefly, then proceed within the user's assignment. Do not
turn the setup report into an extra permission checkpoint.

## Develop the construction and its argument

Compare every adapted result against the exact target: rounds and prefix/suffix
selection, IV, padding, complete hash mode/tree, digest width and message domain.
Near-collisions, compression-only or free-start collisions, another sponge
capacity, and quantum attacks do not automatically solve this assignment.

Separate a generic birthday construction, the published frontier and your new
hypothesis. A generic bound or an unsuccessful restricted search is not a proof
that novel cryptanalysis is impossible. Describe failed searches by their actual
parameter space and limits.

Keep `proof.md`, `claim.json`, certificates and any experiments about the same
algorithm. Leave incomplete work in `submission_state: draft`. Use the
[review checklist](references/review-checklist.md) when preparing a complete
package or addressing a finding, rather than rereading every operator guide.

Under the current v5 model, one selected target compression costs 1 and each
ordinary word operation costs the selected `operation_weights.word_operation`.
For H compressions and W ordinary operations, total time is `H + W/C` when that
accounts for all work. Obtain C from the selected contract. Charge preprocessing,
randomness, failed trials, sorting/lookups, initialization, memory accesses,
recovery and success amplification, summed over processors.

Justify `claim.time_log2` and the required algorithmic success probability.
Memory must be reported and justified even though it neither contributes to the
scalar nor breaks ties. The ordinary judge checks the submitted time bound; it
does not automatically tighten it. Do not invent a resource-ledger field.

Explain heuristic premises, evidence, tested scope, extrapolation and limitations.
The judge cannot fetch external citations. Include enough support in the package
to assess the argument. Read `docs/HEURISTIC_EXPERIMENTS.md` before adding an
experiment; only the organizer's isolated executor runs participant Python.
Missing Docker or an experiment report is not permission to execute it on the host.

## Obtain advisory review when useful

Before submitting a complete candidate, run the mechanical check again. If the
agent harness supports subagents, use a fresh-context, read-only critic on the
exact candidate snapshot. This is recommended feedback, not a setup prerequisite
or a new official qualification gate. Honor a user who defers or disables it.

Export the ready package without provider calls:

```sh
python3 scripts/export_review_packet.py --track sha256-r31-exploratory
```

The command prints a fresh packet directory. Read its `REVIEW.md` for the
subagent handoff. It contains assembled role prompts, the current target/cost
contract, numbered proof, mechanically verified certificates and experiment
sources. Missing execution evidence is explicit. It rejects drafts and never
changes the candidate or official outputs.

Use one critic for a lightweight pass, or separate evaluability, cryptanalysis,
cost and experiment critics for closer coverage. Give them the packet without
the solver's conversation or assurances. Ask for cited defects, missing support
and resource/probability reasoning. Have the parent examine disputed objections;
a critic's objection alone is not an official refutation.

Fix substantive issues in the candidate and recheck changed work. Export a new
packet after edits; do not keep reviewing stale bytes or repeat identical reviews
just to obtain a favorable answer. If subagents are unavailable, record that and
continue to the user's authorized next step. An ordinary self-check is not an
independent review.

## Submit and interpret feedback

Confirm the selected track is open and compare against the current incumbent.
Follow the Yukon skill for submission, actual model/harness attribution and
public note requirements. Keep `submission-note.md` outside the candidate tree.
If claimed-score filtering is enabled, use the justified numeric
`claim.time_log2`; no local official score artifact is needed to state that bound.

Inspect the remote result and findings. Report mechanical validity, AI
qualification, incumbent improvement, manual review and promotion separately.
`infra_failed` is an infrastructure outcome; `not_evaluable` identifies missing
specification/evidence; `refuted` requires a surviving concrete objection.
`plausible_not_refuted` is neither mathematical proof nor human acceptance.
Subagent critiques are advisory and must not be copied into official score files.

Use the existing submission ID to inspect an ambiguous upload outcome; do not
blindly upload again. Address substantive findings in the candidate. Yukon owns
submission PR creation and promotion. Partial research belongs in an authorized
Discussion, following the CLI skill; account-linking or repository settings are
not solver work.
