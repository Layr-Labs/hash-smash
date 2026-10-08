# HashSmash Yukon production setup

Start with the [builder guide](./BUILDER_GUIDE.md). Production uses
`Layr-Labs/hash-smash` and `main`. Preserve its ancestry and the separate
`mooselumph/hash-smash` dev challenge and history. The
[dev runbook](./YUKON_DEV_SETUP.md) and `scripts/import_yukon_dev.py` remain
specific to dev. This guide does not authorize live operations or change the
[scientific review contract](./JUDGE_LANES.md).

## Current round migration

Follow [SHA256_ROUND_MIGRATION.md](./SHA256_ROUND_MIGRATION.md) for the concrete
r31/r32 to r37/r38 rollout. The manifest preserves eight exploratory registrations:
six existing entries plus two new SHA-256 lanes. The intended competing roster
is six after r31/r32 are closed through Yukon. Keep those two registrations and
their public results; do not archive, rename or reimport them.

The new r37/r38 packages are organizer drafts. Nominal numbers do not qualify a
baseline, and historical r31/r32 declarations or attacks are not r37/r38 evidence.
All existing candidate files and definitions are preserved. Every existing lane's
configuration fingerprint changes because of the shared registry/schema/cost
inputs, even though old prices, hash cores and judging rules are unchanged.
A human-reviewed harness PR needs `yukon-unsafe`; qualification and guarded
all-eight refresh are separate live work before admission is restored.

## Release and access readiness

Use a signed, human-reviewed feature-branch PR. Record the production parent,
reviewed tree and resulting commit. Preserve signature requirements and branch
protections. Verify the production **yukon-autoresearch** App and promotion actor
can satisfy them; dev App access is not production access. Humans review harness
PRs; Yukon alone promotes the scored content of submission PRs.

Inspect the actual production provider/model variables and secret names without
printing values. Do not infer current settings from an old runbook or change
providers as part of a round migration. The paired workflow supports OpenRouter,
Amazon Bedrock and direct OpenAI; see [judge/README.md](../judge/README.md) and
[OPENAI_JUDGE.md](./OPENAI_JUDGE.md). Only the selected judge step receives its key;
intake/experiments and final scoring remain in separate credential-free jobs.
The importer needs separate production authorization, not a judge key. Never
copy a dev `.env` or place credentials in notes, source, candidates or artifacts.

Verify repository read access, production App permissions, Discussions and the
Announcement-format `Research Notes` category as applicable. Do not change
repository visibility or permissions implicitly during this migration.

## Existing registrations and qualification

Use the actual production challenge reference and IDs. Reconciliation preview
must retain six records, add r37/r38, and archive none. Record and resolve the
pending job/review inventory as described in the handoff. Changed target
configuration requires fresh bound evidence/review; successful addition workflows
do not refresh retained sibling records. Reorg includes all nonarchived tracks,
including closed r31/r32, and must preserve their closed state.

Each required qualification records the exact source, candidate/package hash,
target/configuration hash, baseline job, workflow run/attempt, artifact IDs/digests,
review outcome and score if emitted. Inspect unresolved obligations. Only a
qualifying selected-lane review can emit the exact manifest-relative score path.
Do not bypass strict gates or reuse an old configuration hash to keep history green.
Historical results remain historical; a fresh review is a separate record.

Run the required offline suite before any separately authorized live judging:

```sh
bash .yukon/setup.sh
python3 scripts/validate_frontier_config.py
```

The tests use organizer fixtures and fake reviewers. Their success proves harness
behavior, not cryptanalytic qualification, production registration, UI readiness
or a successful live migration. New drafts must continue to fail readiness gates.

## A separately intended fresh registration

Do not use a new import to update the existing production challenge: it creates
new identities without transferring history. Only when a separate registration
is explicitly intended, inspect the installed Yukon importer and resolved API,
repository, default branch, source commit and setter namespace. Import the root
`benchmark.json` with no `rootDir`; eight baselines must qualify. Keep admission
unopened and close the two historical SHA registrations explicitly. Never retry
an uncertain import without inspecting its returned records.

This repository's helper has no production option. Use the current supported
production owner/importer workflow from an inspected Yukon checkout. Do not infer
an `--open` timestamp is a scheduled launch; confirm its meaning on that version.

## Restore admission only after verification

Verify `promotionMode: manual`, exact IDs/settings and protected-path rejection.
A qualifying improvement enters owner review without changing the promoted best;
the owner accepts the inspected candidate SHA through Yukon before promotion.
Preserve accepted submissions, manual decisions, workflow provenance and all
sibling candidates. Never manufacture an improvement or manually merge a Yukon
submission PR to test the lifecycle.

The separate Yukon UI change must preserve old result URLs and display the new
rounds using their actual IDs. Final opening/resumption of the intended six,
UI release, reward decisions and human signoffs require the rollout's explicit
operator authorization. r31/r32 must remain closed.
