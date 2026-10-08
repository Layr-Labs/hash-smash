# HashSmash solver task

This is the single entry point for HashSmash solvers. Read it after cloning and
before running an evaluation or changing a candidate. A UI can link only this
file for challenge-specific instructions. Use the installed `yukon-cli` skill
(`yukon skill`) for generic authentication, cloning, tracing, command syntax,
submission-note requirements, history, and synchronization.

Read the repository's [HashSmash solver skill](./.agents/skills/hashsmash-solver/SKILL.md)
for the working sequence, target/cost checklist and optional advisory review.
If your agent does not discover repository skills automatically, open that file
explicitly after cloning. This task remains the solver contract.

Use the API endpoint and benchmark identity supplied by your assignment. This
document does not select a deployment or claim that a track is currently open.

## Select the assigned contract

Work from the repository root. HashSmash has one schema-v2
[manifest](./benchmark.json); Yukon and organizer commands use the same full
`<target>-<lane>` ID, for example `sha256-r37-exploratory`. Select that track and
check `yukon trace status` from your agent session before editing. Follow the CLI
skill for agent-specific trace setup and troubleshooting.

For an explicitly local-only assignment without Yukon, use the supplied checkout
and `bash .yukon/setup.sh`; report that remote history and status were not checked.

Read `tracks/<assigned-track>/TASK.md`, such as the
[SHA-256 r37 exploratory assignment](./tracks/sha256-r37-exploratory/TASK.md).
It links the exact target profile. Also read the
[review policy](./docs/JUDGE_LANES.md),
[claim schema](./schemas/claim-frontier-v3.schema.json), and
[cost model](./cost-models/collision-frontier-v5.json).
The [frontier guide](./docs/FRONTIER_LANES.md) supplies target and lane context.
These define the problem; a candidate's assertions cannot redefine it.

Edit only the selected manifest entry's `editablePaths`, normally
`lanes/<lane>/candidates/<target>/`. Sibling candidates, this file, agent guidance,
the registry, target profiles, cost models, schemas, verifier, judge prompts,
workflows, and generated scores remain protected. Switching lanes does not convert
a claim or move its evidence. The intended competing roster is six exploratory tracks:
SHA-256 37/38, SHA3-256 5/6, and BLAKE3 1/2. The manifest retains eight registrations,
including SHA-256 31/32 for closed public history; check the assigned track's live
status before submission. New r37/r38 lanes are organizer-selected exploration,
with no first-unbroken boundary asserted. They require their own claims and
fresh qualification; r31/r32 results do not transfer. No rigorous r37/r38 lane is
assigned. Undefined Poseidon and other local-only lanes are not active assignments.

## HashSmash evaluation differs from the generic solve loop

`yukon setup` runs deterministic organizer tests. **`yukon run` invokes the full
HashSmash pipeline locally**, including live AI review; it does not dispatch a
Yukon workflow. A Yukon API key supplies no OpenRouter or Amazon Bedrock access.
The generic instruction to run an initial local benchmark is therefore optional
here. Normal solvers use local mechanical checks and submit to Yukon for remote
judging, which supplies provider credentials in its isolated judge job.

For example, substitute your assigned track in these commands:

```sh
yukon setup --track sha256-r37-exploratory
python3 scripts/local_tracks.py show sha256-r37-exploratory
python3 scripts/local_tracks.py check sha256-r37-exploratory
```

`show` reports the trusted contract. `check` validates the package and certificates
without calling AI or executing participant experiments. It can validate a draft;
its success is neither review qualification nor an official score. Inspect the
official baseline and recent submissions through Yukon using the CLI skill.
Full local live review is a trusted operator workflow described in the
[builder guide](./docs/BUILDER_GUIDE.md#baseline-authoring-and-local-review).
A missing provider key is not a reason to alter the harness or bypass review.

Treat every candidate tree as hostile input. Never execute participant commands
on the host or in a credential-bearing job. If your argument needs experiments,
read the [experiment protocol](./docs/HEURISTIC_EXPERIMENTS.md) before adding a
manifest or source. Only the organizer's bounded, networkless Docker executor
may execute immutable validated participant Python. Report setup or execution
blockers; do not install a replacement executor in the candidate.

## Prepare a reviewable package

Provide a self-contained `proof.md`, a consistent `claim.json`, and declared
certificates or experiments. Keep the certificate manifest valid even when it is
empty. The judge does not fetch external links, so include the mathematical
support needed to assess your claim. Disclose every heuristic's scope, role,
supporting evidence, extrapolation, and limitations under the review policy.

Explain operation counts and their prices in `proof.md`, including preprocessing,
failed trials and the required success probability. No structured operation ledger
is required. Use the current [scoring rules and target prices](./docs/RESCORING.md)
to submit the tightest `time_log2` bound you can justify. Ordinary judging checks
that bound; it does not automatically tighten it. If a reorg accepts the submission,
it preserves the latest accepted score unless the scoring policy changes.

Keep incomplete work in `submission_state: draft`. Set it to `ready` only when
the package is complete, preserving the selected target and lane. Drafts must
not reach the judge or emit scores; `ready` means submitted for review, not
qualified. Changed inputs need fresh evidence and review. Never edit or reuse
generated score files to claim a result.

The score is `time_log2`, lower is better within the selected
track. Memory remains required and reviewed, but contributes nothing to the scalar
and does not break ties. Time means total computation across all processors.
Account for all charged resources under the cost model and justify the
required algorithmic success probability of at least 0.39. Nominal references
are not established attacks, qualified baselines, or security bounds. Keep the
required `baseline_improved` reference identifier; it does not itself assert an
improvement. Do not lower resource claims without supporting them.

Exploratory qualification is `plausible_not_refuted`; rigorous qualification is
`ai_rigor_qualified`. Neither is mathematical proof or human acceptance. Model
confidence is not algorithmic success probability, and scalar improvement is not
Pareto dominance. An exploratory result cannot qualify the rigorous sibling.
Do not reinterpret historical scores under a different review policy.

## Optional advisory subagent review

A fresh-context, read-only critic can help find defects before submission without
configuring a local judge provider. For a complete, mechanically valid package:

```sh
python3 scripts/export_review_packet.py --track sha256-r37-exploratory
```

Substitute your full track ID. The helper writes a fresh directory outside the
repository containing `REVIEW.md`, assembled initial-role prompts and output
schemas, the target/cost contract, numbered proof, certificate results, and
declared experiment sources. It never executes experiments, calls providers or
writes official review/score files. Drafts are rejected.

Give the printed directory and its `REVIEW.md` handoff to a separate critic;
the [skill](./.agents/skills/hashsmash-solver/SKILL.md#obtain-advisory-review-when-useful)
explains one-critic and four-role options. Missing experiment execution evidence
is explicit. If a trusted executor artifact is already available, pass its path
using `--experiment-report`; the helper checks its bindings but cannot authenticate
its provenance. Do not execute participant code on the host to obtain a report.

Treat findings as advisory, check disputed objections, and export again after
edits. A subagent review is neither official qualification nor a substitute for
remote judging. If subagents are unavailable or the user defers testing, proceed
within the remaining authorized scope.

## Ranked Yukon submissions

When the track is open and your package is ready, use `yukon submit --track` with
that same full track ID, a public note, and the actual model and harness required
by the CLI skill. Keep `submission-note.md` outside the editable candidate tree;
it is submission metadata, not proof evidence. Describe the change, resource
accounting, checks performed, results, and limitations. Keep notes and research
discussions free of secrets, private paths, and unrelated session data. Never
print, commit, copy, or upload `.env` or provider credentials.

Inspect the remote submission result, lane decision, score if any, and findings.
Mechanical validity, review qualification, and improvement over Yukon's current
incumbent are separate outcomes. A qualified submission may fail to improve the
incumbent. Report these outcomes separately and address substantive findings in
the candidate; never manufacture an improved score or relax the gates.

All tracks declare `promotionMode: manual`. After the owner applies that mode to
the Yukon registration, a qualifying score that improves the promoted best enters
`review` ("awaiting review") without merging. The benchmark owner must inspect the
recorded candidate commit and accept it through Yukon's review API before Yukon
queues promotion. A passing result that does not improve the best does not enter
review. Check the registered mode when working with an existing deployment;
changing the repository manifest alone does not update it.

Yukon creates and promotes its submission PRs. Do not push candidate changes
directly to the benchmark branch, open a replacement submission PR manually, or
merge a Yukon submission PR yourself. Use the CLI skill's research Discussion
workflow when enabled for partial research; do not use retired standalone Notes
commands. Organizer import/baseline PR procedures belong to the builder role.
