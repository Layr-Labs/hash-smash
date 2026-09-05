# Solver workflow for the HashSmash Yukon challenge

Use this guide after the organizer has imported and opened the single dev challenge.
Read `AGENTS.md`, `FRONTIER_LANES.md`, and your assigned
`tracks/<target>-<lane>/TASK.md` before editing. Only the assigned candidate
directory is editable; shared code and judge configuration are protected.

Use the actual setter/challenge name returned by import. In these examples,
replace `SETTER` with that confirmed namespace:

```sh
YUKON_API_URL=https://yukon-api-dev.fly.dev yukon clone SETTER/hashsmash
cd hashsmash
YUKON_API_URL=https://yukon-api-dev.fly.dev yukon tracks
YUKON_API_URL=https://yukon-api-dev.fly.dev yukon switch sha256-r31-exploratory
YUKON_API_URL=https://yukon-api-dev.fly.dev yukon trace status
```

The CLI prints the repository root as the benchmark work directory after cloning.
Stay at that root for Yukon commands. Public Yukon and organizer Python track
names are identical: `sha256-r31-exploratory` includes the selected lane. Its
editable directory is `lanes/exploratory/candidates/sha256-r31`. The manifest,
trusted registry, setup and benchmark commands all bind that same selection.

`yukon switch` changes local Yukon selection only, preserving your Git branch,
HEAD, index and worktree. It does not convert an exploratory claim into a rigorous
one or overwrite sibling work. To work on the rigorous track, select
`yukon switch sha256-r31-rigorous` in the same clone before starting that work;
its editable directory is `lanes/rigorous/candidates/sha256-r31`. The lane is also
recorded in the validated claim binding and generated score `metrics.lane`.

The current Yukon CLI supplies agent/session tracing integrations. Use the current
organizer-supported CLI and inspect `yukon trace status` in the selected challenge
before editing. If capture is disabled, enable it with `yukon trace on`, then
verify that the intended agent's session is being captured. Run the coding agent
inside the cloned repository. Do not add unrelated per-challenge hook files or
edit protected agent configuration to bypass trace requirements. Report capture
failures to the organizer; a passing score is not evidence that tracing worked.

After completing the package and setting its state to `ready`, run:

```sh
YUKON_API_URL=https://yukon-api-dev.fly.dev yukon setup --track sha256-r31-exploratory
YUKON_API_URL=https://yukon-api-dev.fly.dev yukon run --track sha256-r31-exploratory
YUKON_API_URL=https://yukon-api-dev.fly.dev yukon submit --track sha256-r31-exploratory --note-file submission-note.md
```

Keep `submission-note.md` outside the editable candidate directory; it is CLI
submission metadata, not part of the proof package. Submission notes must explain
the change, algorithm, resource accounting, commands, evidence, limitations, and
what the agent actually did. Remove credentials, `.env` content, private data,
private machine paths, and unrelated session material before posting. The judge
does not fetch external links: include necessary mathematical support in the
candidate package itself.

Local live review requires provider access in the trusted environment; solvers
without that access should follow the organizer's remote submission procedure.
Do not put a provider key into the candidate or request untrusted host execution.
Only the organizer's bounded Docker executor may run declared Python experiments.

For partial research, use `yukon discussion create` and its CLI help after the
organizer enables the `Research Notes` category and App Discussions permission.
Standalone Notes are retired. Research threads and submission notes are visible
to repository collaborators; private repository visibility does not make them an
appropriate place for secrets. Do not claim that AI qualification is proof or
human acceptance, or that scalar improvement establishes Pareto dominance.

Yukon opens and manages submission PRs. Do not merge them using GitHub's merge,
squash, or rebase buttons. Let Yukon promote the scored content; an improving
submission must also preserve every sibling track, including those in the other lane.
