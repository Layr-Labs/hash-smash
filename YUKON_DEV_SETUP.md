# HashSmash Yukon dev setup

This is the operator runbook for the existing paired research candidates. It
retargets the reusable Yukon challenge setup instructions to HashSmash. There is
no separate diagnostic benchmark. Do not import the repository root unless the
legacy SHA-1 pilot is deliberately the intended target.

## Contract and current scope

| Contract | Exploratory | Rigorous |
| --- | --- | --- |
| Challenge manifest name | `hashsmash-exploratory` | `hashsmash-rigorous` |
| Import `rootDir` | `lanes/exploratory` | `lanes/rigorous` |
| Schema | 2 | 2 |
| Current tracks per import | 8 | 8 |
| Required review outcome | `plausible_not_refuted` | `ai_rigor_qualified` |
| Editable path, relative to the leaf | `candidates/<target>` | `candidates/<target>` |
| Score path, relative to the leaf | `.yukon/scores/<target>-exploratory.json` | `.yukon/scores/<target>-rigorous.json` |

Each track has a literal `<target>-<lane>.yml` workflow. All workflows check out
the dispatched commit and run on GitHub-hosted `ubuntu-24.04`. The submission cap
is 4,194,304 expanded bytes per track. Lower `time_log2 + memory_log2_bytes` wins.
The target, cost, and acceptance definitions remain in `FRONTIER_LANES.md`,
`JUDGE_LANES.md`, and their linked trusted profiles; this runbook does not change
them. MD5/SHA-1 endpoints are explicitly controls.

The twelve pending BLAKE3, Keccak[800], and Poseidon slots are excluded from both
manifests. Resolving them is not a prerequisite for deploying the current sixteen
lanes. Do not manufacture boundaries or scores to make `--require-complete` pass.

HashSmash needs neither Willow's M3 Max runner group and JIT App nor its Rust
toolchain, Seatbelt bridge, private leaf tarball, or wall-time attack score.
`.yukon/setup.sh` and the Python pipeline are the operator entry points already
declared in the manifests. Do not rename them to match another challenge.

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
these challenges. A draft rejection is an expected negative test, not a successful
end-to-end baseline.

## Import through Yukon dev

Ask the deployment operator to confirm that dev supports schema v2 and leaf roots,
and that the importing account's **email** is in `YUKON_BENCHMARK_IMPORTER_EMAILS`.
Create its importer key in the dev setter UI's API keys view. Keep the key in a
private file outside this repository (`chmod 600`), or supply `YUKON_API_KEY` in
the calling process environment. Never paste it into notes or commit it.

Inspect both requests without credentials or network access:

```sh
python3 scripts/import_yukon_dev.py --lane exploratory
python3 scripts/import_yukon_dev.py --lane rigorous
```

Each request uses the fixed `https://yukon-api-dev.fly.dev` API, repository
`https://github.com/Layr-Labs/hash-smash`, source branch `main`, and its explicit
leaf `rootDir`. Each import queues eight baseline workflows. The checked upstream
`bun run import-benchmark` helper does not expose `rootDir`; a bare repository URL
selects the root schema-v1 legacy pilot. The local helper sends the supported
`POST /api/benchmarks` JSON body directly.

After baseline readiness and credential setup, run the real import:

```sh
python3 scripts/import_yukon_dev.py --lane exploratory --submit --wait
python3 scripts/import_yukon_dev.py --lane rigorous --submit --wait
```

Those commands use `YUKON_API_KEY`/`YUKON_API_TOKEN`; alternatively add
`--api-key-file /absolute/path/to/private-key-file`. The helper does not load
`.env`, print the key, follow redirects, or retry an uncertain import request.
It refuses imports while local candidates are drafts. `--source-branch` selects
an explicitly intended existing branch; do not create a parallel ranked branch
per track. If a setter slug has been agreed, `--name setter/challenge` can set it;
otherwise record the actual names returned by Yukon rather than guessing that
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
must contain the leaf-relative `scorePath`, not only its basename. The workflows
stage only the validated selected score under a fresh artifact root; hidden-file
upload preserves `.yukon`. Failure must leave no successful score artifact.

After every required baseline qualifies, the organizer can explicitly open the
dev challenges and run the solver loop described in `YUKON_SOLVER_GUIDE.md`.
Test a legitimate candidate change, a non-editable-path rejection through Yukon,
and promotion. Confirm that a promotion preserves both sibling tracks and the
other leaf challenge's candidates and harness. Save the before/after commit and
path hashes; local surface-check tests alone do not establish this platform result.

Humans review and merge harness PRs. Humans must **not** merge Yukon submission
PRs; Yukon promotes the content it scored. Use the `yukon-unsafe` label on harness
PRs that invalidate pending scores, so Yukon blocks promotion of stale scored
submissions after that PR merges. Avoid the label for unrelated safe documentation
changes. Changing the label, workflow, or score packaging does not authorize
changing scientific acceptance thresholds.
