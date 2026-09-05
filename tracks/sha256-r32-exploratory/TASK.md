# sha256-r32-exploratory

Read the repository-root [solver task](../../TASK.md) first. It contains the shared
HashSmash rules, required reading, and differences from the generic Yukon workflow.
This file supplies only the assigned target and lane contract.

| Field | Assignment |
| --- | --- |
| Yukon and organizer track ID | `sha256-r32-exploratory` |
| Editable directory | `lanes/exploratory/candidates/sha256-r32/` |
| Exact target profile | [sha256-r32-prefix-v1](../../target-profiles/sha256-r32-prefix-v1.json) |
| Review lane | `exploratory` |
| Qualifying AI review status | `plausible_not_refuted` |
| Nominal reference | 128; not an established attack, qualified baseline, or security bound |

Use `python3 scripts/local_tracks.py show sha256-r32-exploratory` from the repository
root to inspect the trusted profile, cost model, and reference. Keep the selected
track ID and candidate lane consistent; the sibling lane has its own package.

Follow [TASK.md's evaluation guidance](../../TASK.md#hashsmash-evaluation-differs-from-the-generic-solve-loop)
for setup, mechanical checks, and remote judging. Ranked solvers submit through
Yukon. Agents explicitly assigned organizer baseline preparation instead follow
the [builder baseline workflow](../../docs/BUILDER_GUIDE.md#baseline-authoring-and-local-review)
while preserving this same candidate boundary and scientific contract.
