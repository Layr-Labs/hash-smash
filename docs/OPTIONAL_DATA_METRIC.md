# Retiring the data metric without a reorg

HashSmash's current objective remains `time_log2` under `collision-frontier-v5`.
`data_log2` is optional legacy metadata, not a separately reviewed resource bound. Claims using
schema version 3 remain valid with or without it; a supplied value must still be
a finite, nonnegative number. New organizer templates omit it.

New cost reviews can omit `data_log2`, even when the submitted claim contains it.
The reviewer no longer compares or justifies that bound. The existing obligation
ID `data_preprocessing_advice` remains for compatibility, but covers preprocessing
and nonuniform advice only. Those costs, message generation/processing, and peak
storage must still be accounted for under the existing cost model.

Score output preserves `metrics.dataLog2` when a submitted claim supplies it and
omits it otherwise. Absence does not mean zero. The score formula, success budget,
lane criteria for the remaining obligations, and candidate package bindings are
unchanged.

## Rollout

Apply this update through the normal human-reviewed harness PR process. Do not
trigger a Yukon reorg, reimport the challenge, replay historical submissions, or
edit existing candidate packages or published results as part of this change.
Existing scores and review records remain historical results under their original
configuration. New evaluations use the updated optional-field contract.

The earlier simplified-judgment reorg is complete. Its 25 plan entries are
preserved unchanged in
[the archived plan](../reorg/history/completed-simple-judgments-plan.json), while
`reorg/plan.json` is empty. This prevents an explicit future evaluation of those
packages from selecting obsolete configuration pins. Existing artifact references
and published results are retained; clearing the plan starts no reviews or reorg.

Exact configuration/evidence fingerprints remain enforced. This update accepts
legacy candidate inputs; it does not make an old frozen review reusable under a
new harness configuration. Do not patch old hashes or dossiers to bypass this
check. If work is already running, let it finish under its existing revision
before rollout. A separately requested reconsideration of historical outcomes is
outside this migration.

## Handoff to the Yukon builder agent

Update the HashSmash UI to retire the derived Data metric without a reorg or a
database migration. The harness accepts `claim.claim.data_log2` as optional legacy
metadata and exports optional `score.metrics.dataLog2` only when supplied. Neither
field affects the numeric objective. Both older and newer records must render.

Start in the Yukon repository at:

- `apps/challenges-ui/challenges/hashsmash/lib/manifest-view-model.ts`
- `apps/challenges-ui/challenges/hashsmash/lib/manifest-view-model.test.ts`

In `deriveManifestView`, remove the `data_log2` entry from the derived resource
metrics list. It currently renders the label "Data" and assumes the unit
"complete message evaluations"; historical claims do not consistently use that
unit. Hide this derived metric for both old and new submissions, including when
its value is present. Do not replace it with "Not specified", zero, or an empty
row. Check the consuming layout for fixed column counts or assumptions about the
number of resource cards.

Search the rest of the HashSmash presentation and parsing code for `data_log2`,
`dataLog2`, and Data labels. Any typed parser should accept the field being absent.
Remove any derived cards, columns, sorting, filtering, or missing-field warnings
that depend on it. Scope this work to HashSmash; do not remove unrelated metrics
from other challenges or alter generic storage of arbitrary score metadata.

Preserve raw manifests, downloadable JSON, existing score/review records, proofs,
and submission archives exactly as supplied. Raw views may still show a historical
data field. Keep total time, peak memory, preprocessing, advice, success probability,
and current time-only score arithmetic unchanged. Preserve historical score displays
according to their recorded cost model; do not relabel old time-plus-memory scores.
Do not change rankings or qualification labels, initiate reorg/replay, or rewrite
historical records.

Add regression coverage for otherwise identical manifests with and without
`data_log2`: both should have the same visible resource metrics and score arithmetic,
no derived Data row, and no missing-data warning. Assert that a legacy field remains
intact in the raw manifest and that deriving the view does not mutate its input.
If score metrics are separately parsed, cover both presence and absence of
`metrics.dataLog2` there too. Inspect the resulting resource layout and run the
relevant HashSmash UI tests.

Deliver the UI change as a separate PR. It can be deployed before the harness
update because it handles both record shapes. Do not start a reorg.
