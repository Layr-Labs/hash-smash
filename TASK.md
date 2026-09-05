# HashSmash solver task

This repository is one Yukon challenge with sixteen paired tracks. Read
[AGENTS.md](./AGENTS.md), [FRONTIER_LANES.md](./docs/FRONTIER_LANES.md), and your assigned
`tracks/<target>-<lane>/TASK.md` for the exact target, editable path, and review
policy. This root file routes you to that assignment; it does not select a
candidate or authorize changes to the harness.

Run Yukon commands from the repository root. Select the full track ID, including
the lane, and check trace attribution before editing. For example:

```sh
yukon switch sha256-r31-exploratory
yukon trace status
yukon setup --track sha256-r31-exploratory
```

That assignment permits changes only within
`lanes/exploratory/candidates/sha256-r31/`. A rigorous assignment uses its own
`<target>-rigorous` track and `lanes/rigorous/candidates/<target>/` directory.
Switching tracks does not convert a claim or move candidate files. Shared code,
profiles, cost models, schemas, workflows, registry, and score files are protected.

Provide a self-contained claim, proof, and declared evidence under the selected
track's contract. [CANDIDATE_QUALIFICATION.md](./docs/CANDIDATE_QUALIFICATION.md) explains
readiness; [JUDGE_LANES.md](./docs/JUDGE_LANES.md) defines acceptance and
[HEURISTIC_EXPERIMENTS.md](./docs/HEURISTIC_EXPERIMENTS.md) defines optional isolated
experiments. Drafts never reach the judge or emit scores. Only the organizer's
bounded, networkless Docker executor may execute participant Python.

Follow [YUKON_SOLVER_GUIDE.md](./docs/YUKON_SOLVER_GUIDE.md) for the complete setup, run,
submission-note, discussion, and CLI-managed tracing workflow. Use the same full
track ID for every run and submission. Keep notes outside the candidate directory
and remove secrets, private paths, and unrelated session material before posting.
Yukon manages submission PR promotion; do not merge those PRs manually.

Scores rank `time_log2 + memory_log2_bytes`, lower is better, within each fixed
track. Exploratory qualification is `plausible_not_refuted`; rigorous qualification
is `ai_rigor_qualified`. Neither is mathematical proof or human acceptance, and
scalar improvement does not establish Pareto dominance.
