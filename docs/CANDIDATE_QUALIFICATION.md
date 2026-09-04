# Qualifying the existing candidate packages

This handoff concerns the sixteen existing research lanes. It does not introduce a
diagnostic benchmark or activate the twelve undefined slots.

`submission_state: ready` means that a complete package is submitted for review.
It does not mean the package has qualified or can seed a successful Yukon import.
Exploratory qualification is `plausible_not_refuted`; rigorous qualification is
`ai_rigor_qualified`. Both are AI review outcomes, not human acceptance or proof.

## Assignment for the candidate agent

Prepare complete, reviewable baseline candidates for these target pairs:

| Targets | Exploratory directories | Rigorous directories |
| --- | --- | --- |
| `md5-s63`, `md5-s64` | `lanes/exploratory/candidates/<target>/` | `lanes/rigorous/candidates/<target>/` |
| `sha1-r79`, `sha1-r80` | `lanes/exploratory/candidates/<target>/` | `lanes/rigorous/candidates/<target>/` |
| `sha256-r31`, `sha256-r32` | `lanes/exploratory/candidates/<target>/` | `lanes/rigorous/candidates/<target>/` |
| `sha3-256-r5`, `sha3-256-r6` | `lanes/exploratory/candidates/<target>/` | `lanes/rigorous/candidates/<target>/` |

Assign explicit candidate directories to each worker; a solver edits only its
assigned directory. Use a separate worktree and feature branch, then open a PR,
so candidate work does not interfere with the harness branch. Do not change target
profiles, cost models, schemas, manifests, judge prompts, validators, workflows,
or generated scores to get a candidate accepted. Do not invent definitions for
BLAKE3, Keccak[800], or Poseidon. Keep all sixteen packages
independent even when they adapt the same underlying argument.

Read `AGENTS.md`, `docs/FRONTIER_LANES.md`, `docs/JUDGE_LANES.md`,
`docs/HEURISTIC_EXPERIMENTS.md`, `schemas/claim-frontier-v3.schema.json`,
`cost-models/collision-frontier-v3.json`, the assigned `tracks/<track>/TASK.md`,
and that track's exact target profile. The internal track ID includes the lane,
for example `sha256-r31-exploratory`.

## What must replace each scaffold

1. **A concrete algorithm and proof in `proof.md`.** Specify its messages, complete
   hash computation, data structures, stopping rule, collision check, and success
   event. Justify its correctness and success bound, stating any heuristic
   assumptions explicitly, for distinct messages with equal full digests under
   the fixed IV, prefix rounds, padding and feed-forward/sponge rules of this exact
   profile. A compression-only, free-start, truncated-output, or different-round
   result is not a substitute. The judge does not fetch external links: include
   the argument needed to assess cited results in the package.
2. **A justified resource ledger in `claim.json` and the proof.** Replace the
   nominal placeholder numbers with upper bounds justified under the 256-bit
   word-RAM cost model. Charge preprocessing, message construction, all trials
   including failures, randomness, sorting/lookups, verification and restarts.
   Peak memory includes code, advice, retained messages, tables and working state.
   Explain the data and advice fields and the units of every bound. The emitted
   score is `time_log2 + memory_log2_bytes`; a birthday exponent is not a complete
   time-memory implementation ledger.
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
python3 scripts/local_tracks.py show sha256-r31-exploratory
python3 scripts/local_tracks.py check sha256-r31-exploratory
bash .yukon/setup.sh
```

Keep `submission_state` as `draft` while writing. Once the package above is complete,
set only that candidate's state to `ready`, preserving its target and lane. Re-run
the mechanical check. In a credential-free shell, prepare any required runtime
and create evidence through the organizer pipeline:

```sh
python3 scripts/prepare_experiment_image.py --track sha256-r31-exploratory
python3 scripts/hashsmash_pipeline.py intake --track sha256-r31-exploratory
```

Image preparation does not execute candidate code. Intake executes declared Python
only in the bounded, networkless Docker executor. No experiment manifest is needed
for a self-contained analytic argument that does not rely on experiments.

A trusted operator can then review that frozen evidence in a separate shell with
the Bedrock credential available securely. Match the current Actions profile:

```sh
HASHSMASH_JUDGE_PROVIDER=bedrock \
HASHSMASH_BEDROCK_MODEL=us.openai.gpt-5.6-sol \
HASHSMASH_BEDROCK_REGION=us-east-1 \
HASHSMASH_JUDGE_MODE=committee \
HASHSMASH_REASONING_EFFORT=high \
python3 scripts/hashsmash_pipeline.py judge --track sha256-r31-exploratory
```

Run the deterministic score phase only after the selected lane qualifies:

```sh
python3 scripts/hashsmash_pipeline.py score --track sha256-r31-exploratory
```

Inspect the complete dossier and unresolved obligations, not only the exit code.
Fix substantive findings in the candidate; changed input requires fresh intake
and review. Preserve all review attempts instead of selecting a favorable run.
Keep live reviews bounded and never print, commit, copy, or upload `.env` or keys.
An exploratory result cannot be copied into a rigorous score: each selected lane
requires its own correctly bound package, review, and score.

For this example, the dossier and aggregate are under
`lanes/exploratory/.yukon/reports/tracks/sha256-r31-exploratory/`; the trusted score,
if emitted, is `lanes/exploratory/.yukon/scores/sha256-r31-exploratory.json`.

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
