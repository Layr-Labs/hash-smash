# Yukon multi-problem and round-count support

Status: nine local tracks are implemented; the Yukon migration below is **not activated**.
See [LOCAL_TRACKS.md](./LOCAL_TRACKS.md) for the selected MD5/SHA-1/SHA-256 roster,
registry, deterministic checkers and isolated local runner. Our active `benchmark.json`
is still schema v1 with one full-round SHA-1 benchmark. Nominal local reference scores
are not qualified baselines and do not satisfy Yukon's baseline import gate.

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

## HashSmash mapping

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

## Solver experience after migration

For schema v2, the documented commands are:

```sh
yukon clone <setter>/hashsmash
yukon switch sha1-r40
yukon setup --track sha1-r40
yukon run --track sha1-r40
yukon submit --track sha1-r40
```

The first track is default. Switching changes local Yukon selection, not the Git branch
or worktree. These are future v2 instructions, not commands for our current v1 manifest.

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

## Migration work

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
certificate checkers, disjoint candidate directories and isolated reports/scores. Remote
workflow wrappers, a v2 manifest activation, baseline import handling and dev deployment
remain future work. No repositories, branches, deployments or Pareto promotion rules
were created; see LOCAL_TRACKS.md for the actual local configuration.
