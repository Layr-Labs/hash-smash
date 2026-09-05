# HashSmash Yukon dev setup

This is the operator runbook for the existing paired research candidates. It
retargets the reusable Yukon challenge setup instructions to HashSmash. There is
one schema-v2 challenge imported from the repository root. Its sixteen tracks
include both review lanes; do not create a second import for the other lane.

## Contract and current scope

| Contract | Value |
| --- | --- |
| Challenge manifest name | `hashsmash` |
| Manifest / import root | Repository-root `benchmark.json`; omit `rootDir` |
| Schema / current tracks | 2 / 16 (eight exploratory, eight rigorous) |
| Yukon and organizer track ID | `<target>-<lane>`, such as `sha1-r80-rigorous` |
| Required exploratory / rigorous outcome | `plausible_not_refuted` / `ai_rigor_qualified` |
| Editable path, relative to repository root | `lanes/<lane>/candidates/<target>` |
| Score path, relative to repository root | `lanes/<lane>/.yukon/scores/<target>-<lane>.json` |

The protected registry records the lane, claim validation binds each package to
it, and successful scores include `metrics.lane`. Track names and descriptions
also identify the lane. Yukon's strict manifest schema does not accept an arbitrary
`metadata` field; do not add one. Lane directories remain isolated storage for
candidates and generated state, and no longer contain import manifests.

Each track has a literal `<target>-<lane>.yml` workflow. All workflows check out
the dispatched commit and run on GitHub-hosted `ubuntu-24.04`. The submission cap
is 4,194,304 expanded bytes per track. Lower `time_log2 + memory_log2_bytes` wins.
The target, cost, and acceptance definitions remain in `FRONTIER_LANES.md`,
`JUDGE_LANES.md`, and their linked trusted profiles; this runbook does not change
them. MD5/SHA-1 endpoints are explicitly controls.

The twelve pending BLAKE3, Keccak[800], and Poseidon slots are excluded from the
manifest. Resolving them is not a prerequisite for deploying the current sixteen
tracks. Yukon's present limit is 20 tracks per challenge; activating all 28 slots
would first require an upstream limit increase as well as exact target definitions.
Do not manufacture boundaries or scores to make `--require-complete` pass.

HashSmash needs neither Willow's M3 Max runner group and JIT App nor its Rust
toolchain, Seatbelt bridge, private leaf tarball, or wall-time attack score.
`.yukon/setup.sh` and the Python pipeline are the operator entry points already
declared in the root manifest. Do not rename them to match another challenge.

## GitHub and provider access

The operator repository is the existing private `Layr-Labs/hash-smash` repository.
Use feature branches and human-reviewed harness PRs; never recreate the repository
or push harness changes directly to `main`.

Install or configure the [Yukon dev App](https://github.com/apps/yukon-eigen/installations/new)
for `Layr-Labs/hash-smash`. Its execution access includes contents write, Actions
read/write, and pull requests write. Verify the selected repository and any pending
permission approval in GitHub's repository/organization GitHub Apps settings.
`GET /repos/Layr-Labs/hash-smash/installation` requires an App JWT; an ordinary
`gh` login's JWT/401 error is not evidence that the App is absent. A successful
Yukon-driven baseline run verifies the service's actual access. A direct
`gh workflow run` only verifies that user's Actions access.

Current Actions configuration uses secret `AWS_BEARER_TOKEN_BEDROCK` and variables
`HASHSMASH_JUDGE_PROVIDER=bedrock`,
`HASHSMASH_BEDROCK_MODEL=us.openai.gpt-5.6-sol`, and
`HASHSMASH_BEDROCK_REGION=us-east-1`. The paired workflow selects committee mode
and high reasoning effort. Only the judge step receives the provider key;
experiments and final scoring run in separate jobs. Check these settings before
the official run; do not commit or print keys or `.env`.

Give invited solvers repository read access using their own GitHub identities.
Yukon does not mint private-repository clone tokens. For research threads, enable
Discussions and create an Announcement-format category named exactly
`Research Notes`; the dev App needs approved Discussions read/write access.

## Real baseline readiness

Follow [CANDIDATE_QUALIFICATION.md](./CANDIDATE_QUALIFICATION.md). Every imported
track needs a substantive `ready` package and a qualifying review/score under
that lane's policy. Complete the offline suite before live provider review.
Neither draft values, nominal reference scores, nor local calibration scores
are research baselines. An exploratory pass does not qualify a rigorous lane.

Before importing, merge the intended candidate and harness PRs, use a clean
checkout of that source branch, and obtain trusted workflow results on the exact
content. Changes to a package require fresh evidence/review. The importer helper's
local readiness check is not a remote-branch attestation or a proof of qualification;
Yukon dispatches baseline validation against the source it actually resolves.

The [local participant heuristic test](./PARTICIPANT_HEURISTIC_TEST.md) can help
diagnose the harness, but it is outside the production registry and cannot seed
this challenge. A draft rejection is an expected negative test, not a successful
end-to-end baseline.

## Import through Yukon dev

Confirm that the dev deployment supports schema v2 and that the importing account's
**email** is in `YUKON_BENCHMARK_IMPORTER_EMAILS`. Close and archive the prior lane
deployments in the setter UI before this fresh repository import; Yukon does not
allow concurrent open challenges for the same source repository.

Create the account's importer key in the dev setter UI's API keys view. Keep the key in a
private file outside this repository (`chmod 600`), or supply `YUKON_API_KEY` in
the calling process environment. Never paste it into notes or commit it.

Inspect the one import request without credentials or network access:

```sh
python3 scripts/import_yukon_dev.py --source-branch main
```

The request uses the fixed `https://yukon-api-dev.fly.dev` API, repository
`https://github.com/Layr-Labs/hash-smash`, and source branch `main`. It omits
`rootDir`, so Yukon reads the sixteen-track schema-v2 manifest at the repository
root. The helper sends the supported `POST /api/benchmarks` JSON body directly.
If using the setter UI instead, choose the same repository and branch, leave its
root-directory field empty, and use the challenge name `hashsmash`.

Submitting that import activates validation: Yukon queues sixteen baseline
workflows against the resolved source commit. There is no separate per-lane
activation step. All sixteen baselines must qualify for the challenge to become
ready; an exploratory success does not substitute for its rigorous sibling.

After baseline readiness and credential setup, run the real import:

```sh
python3 scripts/import_yukon_dev.py --source-branch main --submit --wait
```

That command uses `YUKON_API_KEY`/`YUKON_API_TOKEN`; alternatively add
`--api-key-file /absolute/path/to/private-key-file`. The helper does not load
`.env`, print the key, follow redirects, or retry an uncertain import request.
It refuses imports while local candidates are drafts. `--source-branch` selects
an explicitly intended existing branch; do not create a parallel ranked branch
per track. If a setter slug has been agreed, `--name setter/challenge` can set it;
otherwise record the actual name returned by Yukon rather than guessing that
the GitHub organization equals the setter namespace.

There is deliberately no production or opening option. Successful baselines
remain `ready`, with submissions unopened. The helper reports track IDs and job
URLs; `--wait` reports transitions and returns nonzero on failed baselines or a
wait timeout. A timeout does not cancel or recreate the import. Inspect the saved
IDs in dev before retrying after a network error or interruption. To retry a failed
baseline, archive/delete that failed import in the setter UI, fix the actual
cause, and import again; never delete/recreate the GitHub repository.

## Yukon verification before opening

For each track, record the source commit, Yukon baseline job ID, GitHub workflow
run URL, App actor, exact score ZIP entry, review label and scalar. The score ZIP
must contain the repository-relative `scorePath`, not only its basename. The workflows
stage only the validated selected score under a fresh artifact root; hidden-file
upload preserves `.yukon`. Failure must leave no successful score artifact.

After every required baseline qualifies, the organizer can explicitly open the
dev challenge and run the solver loop described in `YUKON_SOLVER_GUIDE.md`.
Test a legitimate candidate change, a non-editable-path rejection through Yukon,
and promotion. Confirm that a promotion preserves all sibling tracks, including
the other lane's candidates, and the harness. Save the before/after commit and
path hashes; local surface-check tests alone do not establish this platform result.

Humans review and merge harness PRs. Humans must **not** merge Yukon submission
PRs; Yukon promotes the content it scored. Use the `yukon-unsafe` label on harness
PRs that invalidate pending scores, so Yukon blocks promotion of stale scored
submissions after that PR merges. Avoid the label for unrelated safe documentation
changes. Changing the label, workflow, or score packaging does not authorize
changing scientific acceptance thresholds.
