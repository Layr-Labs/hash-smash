# Yukon multi-track contract and historical design

2026-09-04 update: HashSmash now uses one repository-root schema-v2
[`benchmark.json`](./benchmark.json) named `hashsmash`, with sixteen uniquely named
`<target>-<lane>` tracks. See [FRONTIER_LANES.md](./FRONTIER_LANES.md) for the current
roster and [YUKON_DEV_SETUP.md](./YUKON_DEV_SETUP.md) for import instructions. The
previous two-leaf import plan is superseded: Yukon source-repository exclusivity
requires a single challenge for the fresh deployment.

Both lanes retain disjoint candidate and generated-state directories. The protected
registry and validated claim bind the lane, while score `metrics.lane` stores it
with the result. Yukon manifests reject arbitrary metadata fields, so the lane
also appears in each supported track name and description. Sixteen tracks fit the
current 20-track limit. The twelve undefined slots remain inactive; eventually
activating all 28 would require an upstream track-limit increase.

One import queues a baseline for every declared track. All sixteen must qualify
before opening. The schema-v1 pilot and nine local tracks are historical code
pending separate cleanup; they are not part of the root Yukon import. The rest
of this document records the earlier design investigation and alternatives, not
additional active challenges or instructions for the current deployment.

Source checked through authenticated GitHub: Yukon master
`d9471fe70a431a3c424758c3eb58d51d38e73d67`. The older local Yukon checkout was not changed.
Source support does not establish which revision is running in a Yukon dev deployment.

## Native schema-v2 tracks

Yukon supports one challenge with independently scored tracks in one repository,
one manifest, and one shared source branch. Each track declares its name, editable
paths, commands, score path, direction, and workflow. Import creates tracks atomically
and queues one baseline per track. Promotion grafts only the winning track's editable
paths onto the latest shared branch, preserving sibling-track work.

The current parser allows **1 to 20 tracks**. Track editable paths must be pairwise
disjoint, including ancestor overlap. V2 rejects unknown fields: there is no per-track
branch or arbitrary `rounds` field. Round semantics belong in trusted external profiles.

- [Author guide: multiple tracks](https://github.com/Layr-Labs/yukon/blob/d9471fe70a431a3c424758c3eb58d51d38e73d67/docs/github-actions-benchmark-author-guide.md#multiple-tracks-on-one-branch-schema-v2)
- [Manifest parser and track limit](https://github.com/Layr-Labs/yukon/blob/d9471fe70a431a3c424758c3eb58d51d38e73d67/src/benchmark/manifest.ts#L111)
- [Overview](https://github.com/Layr-Labs/yukon/blob/d9471fe70a431a3c424758c3eb58d51d38e73d67/OVERVIEW.md)

## Historical HashSmash mapping

Use one track per fixed `(primitive, round semantics, attack class, cost model,
success criterion)`. These names and round counts are illustrative, not a chosen roster:

| Example track | Editable directory | Trusted profile | Score file |
| --- | --- | --- | --- |
| `sha1-r40` | `candidates/sha1-r40/` | `target-profiles/sha1-r40-v1.json` | `.yukon/scores/sha1-r40.json` |
| `sha1-r60` | `candidates/sha1-r60/` | `target-profiles/sha1-r60-v1.json` | `.yukon/scores/sha1-r60.json` |
| `sha1-r80` | `candidates/sha1-r80/` | `target-profiles/sha1-fips180-4-v1.json` | `.yukon/scores/sha1-r80.json` |

A shared editable `candidate/` for all tracks is invalid. Shared verifier, judge, policy,
frontier, profiles, and workflow code stay outside every editable surface. A submitted
round count must match the selected profile; participant text cannot choose the target.

Reduced-round profiles must specify which rounds execute, schedule, IV, padding,
feed-forward, output encoding/width, and collision relation. Reduced-round full-hash,
compression, and free-start collisions are not interchangeable. Each profile needs its
own baseline and reference tests. Different round counts are different problems, not
entries on the same dominance frontier.

## Workflow routing

Current Yukon dispatches repository, workflow filename, and ref, but **no track input**:
[dispatch code](https://github.com/Layr-Labs/yukon/blob/d9471fe70a431a3c424758c3eb58d51d38e73d67/src/integrations/github.ts#L1033).

Give each track a thin `workflow_dispatch` wrapper, e.g. `sha1-r40.yml`, containing a
literal track ID. Have wrappers call the same reusable trusted workflow. Select an
allowlisted registry entry and run intake/review/score only for that track. Do not rely
on a dispatch input Yukon does not supply, infer identity from solver files, or run
every track's AI judge on each submission.

Use track-specific work/report/score paths, artifact names, and concurrency groups.
Upload only the selected score. A shared workflow can produce all tracks' scores, but
the guide's shared-workflow example does not imply automatic track-input routing.
Preserve provider-specific credentials and the intake/judge/score trust boundary.

## Current solver experience

For schema v2, the documented commands are:

```sh
yukon clone <setter>/hashsmash
cd hashsmash
yukon switch sha1-r80-rigorous
yukon trace status
yukon setup --track sha1-r80-rigorous
yukon run --track sha1-r80-rigorous
yukon submit --track sha1-r80-rigorous --note-file submission-note.md \
  --model "<actual exact model version and variant>" \
  --harness "<actual coding agent or harness name>"
```

The first track is default. Switching changes local Yukon selection, not the Git branch
or worktree. Run from the cloned repository root and select the intended full track ID
before editing so trace attribution follows that track. See
[YUKON_SOLVER_GUIDE.md](./YUKON_SOLVER_GUIDE.md) for submission notes and tracing details.

## Scalar promotion is not Pareto promotion

Yukon accepts a finite numeric `score` and optional stored JSON `metrics`. Its comparator
uses that scalar, `direction`, and an optional improvement threshold; it does not
perform componentwise dominance over metrics or maintain a nondominated frontier:
[score comparator](https://github.com/Layr-Labs/yukon/blob/d9471fe70a431a3c424758c3eb58d51d38e73d67/src/benchmark/score.ts#L129).

Our current `log2(time) + log2(memory)` is likewise scalar: a smaller value can improve
time while worsening memory. Assumption-free qualification makes claims comparable,
but does not turn scalar improvement into Pareto dominance.

The user selected the scalar time-memory objective for the local experiment. The other
options below are historical alternatives, not planned work for this setup:

- Retain a clearly stated scalar objective within each fixed track.
- Add common resource-budget tracks, such as minimizing time at a fixed memory cap,
  recognizing the 20-track limit.
- Implement organizer-owned vector/frontier validation and promotion coordination, or
  extend Yukon for true Pareto support. Merely putting vectors in `metrics` is insufficient.
  Concurrent promotions require incumbent-frontier freshness checks, not just evaluation
  against a stale snapshot. Human acceptance remains a separate promotion gate.

## Historical migration work

1. Select the primitive/round roster and fully specify each target. The historical
   heuristic fixture cannot serve as a qualified baseline under `unconditional-v1`.
2. Replace hard-coded target/round constants and candidate/profile/frontier paths with
   an organizer-owned track registry used by validation, evidence, judges, and scoring.
   Add cross-track rejection tests; never infer the target from participant prose.
3. Extend certificate verification for reduced rounds using trusted reference code;
   `hashlib.sha1` verifies only full-round SHA-1, not arbitrary reduced-round profiles.
4. Create disjoint candidate directories and track-scoped generated state. Update
   editable-surface checks, local commands, and workflow wrappers.
5. Validate the v2 manifest against Yukon, test score isolation, and qualify one baseline
   per track. Then coordinate the actual dev import and confirm deployed v2 support.

The local runner now implements registry-based target selection, new reduced-round
certificate checkers, disjoint candidate directories and isolated reports/scores.
The current paired-lane implementation also supplies the remote workflow wrappers,
a root schema-v2 manifest, and a dev import helper. A fresh deployment must validate
that complete contract through Yukon; local tests cannot establish remote promotion
behavior. No Pareto promotion rules were introduced. See FRONTIER_LANES.md for the
current configuration.
