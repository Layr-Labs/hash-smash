# HashSmash Yukon production setup

Start with the [builder guide](./BUILDER_GUIDE.md). Production uses the existing
private `Layr-Labs/hash-smash` repository and its `main` branch. Preserve its
ancestry and the separate `mooselumph/hash-smash` dev challenge and history.
The [dev runbook](./YUKON_DEV_SETUP.md) and `scripts/import_yukon_dev.py` remain
specific to dev. This guide does not authorize launch or change the
[scientific review contract](./JUDGE_LANES.md).

## Release and access readiness

Land one signed, human-reviewed harness snapshot through a feature-branch PR.
Record its production parent, reviewed donor revision, final tree and resulting
commit. Keep inherited signature requirements and default-branch protections;
verify the production App and promotion actor can satisfy the approved rules.
App installation and any required actor eligibility remain explicit checks.
Humans review harness PRs; Yukon alone promotes the scored content of submission
PRs. Apply `yukon-unsafe` to harness changes that invalidate pending scores.

Configure the production **yukon-autoresearch** GitHub App for this repository;
verify its approved contents, Actions, pull-request and Discussions permissions.
The dev App `yukon-eigen` does not establish production access. Give private-repo
solvers clone/read access through their own GitHub identities; Yukon does not
provide private clone tokens. Keep repository visibility unchanged pending an
explicit owner decision.

Provision importer and provider credentials separately through approved secret
channels. Never copy a dev `.env`, commit credentials, or include private local
paths in submission or release notes. The repository already has the Actions
secret name `AWS_BEARER_TOKEN_BEDROCK` and these variables:

- `HASHSMASH_JUDGE_PROVIDER=bedrock`
- `HASHSMASH_BEDROCK_MODEL=us.openai.gpt-5.6-sol`
- `HASHSMASH_BEDROCK_REGION=us-east-1`

Their presence does not verify usable provider access or baseline qualification.
Only the judge step receives the provider credential; preserve isolated intake,
experiments and scoring as implemented in the workflow. The importer needs its
own production-authorized `YUKON_API_KEY` or `YUKON_API_TOKEN` in the process
environment. Confirm importer account eligibility with the production operator.

Verify Discussions and an Announcement-format category named exactly
`Research Notes`, plus the App's Discussions access. Enabling Discussions alone
does not create that category or establish App eligibility.

## Six fresh baselines

Import repository-root `benchmark.json` with no `rootDir` override. The six
exploratory track names and submitted `time_log2` bounds are:

| Track | Declared bound | Accounting |
| --- | ---: | --- |
| `sha256-r31-exploratory` | 136 | Existing algorithm, v5 costs with C=2140 |
| `sha256-r32-exploratory` | 136 | Existing algorithm, v5 costs with C=2224 |
| `sha3-256-r5-exploratory` | 137.785 | Existing algorithm, v5 costs with C=1355 |
| `sha3-256-r6-exploratory` | 137.4 | Existing algorithm, v5 costs with C=1626 |
| `blake3-r1-exploratory` | 149 | Unchanged declaration |
| `blake3-r2-exploratory` | 140 | Unchanged declaration |

The four SHA packages refine the declarations in production base
`0455d2b52f4f920fe5c3a6af8c71592a824e6a57` (tree
`fc77941c70bde24a95105147a816cea4e6f50513`), whose donor was
`94a9c97fc047bf8f00ed892f0e5c51e69d6c7e1a`. Each proof separates target
compression/permutation calls H from ordinary word operations W and justifies
`log2(H + W/C)` under [v5 accounting](./RESCORING.md). Targets, algorithms,
success lower bounds and memory bounds are unchanged; these are replacement
claims with self-contained derivations, not new cryptanalytic algorithms.

These declarations are not newly qualified production scores. They match the
four historical dev policy-change rescores, but ordinary judging checks the
submitted bound and must review these changed packages afresh. Historical
exploratory `plausible_not_refuted` judgments with `humanAccepted: false` do not
qualify the replacement packages. All six exact-source production qualifications
remain pending. A fresh import does not inherit dev IDs, submission histories
or manual-review backlog. The active reorg plan remains empty; historical
artifact mappings are not current qualification evidence.
Retain the dev challenge and its outstanding reviews. Poseidon, rigorous, MD5,
SHA-1 and Keccak[800] tracks remain outside this six-track import.

Before import, review the exact merged source and all six packages under
[CANDIDATE_QUALIFICATION.md](./CANDIDATE_QUALIFICATION.md). Bind intake evidence,
review and score to those immutable inputs and current configuration. Reuse the
existing donor offline audit for unchanged source: all 257 tests passed (252
original passes plus five Docker fixture follow-up passes), along with configuration
validation and six mechanical intake passes. The fixture tests use fake reviewers;
these results do not establish live provider access or production baseline
qualification. Changed packages or evaluation configuration require fresh evidence
and review; deployment-only documentation does not tighten any submitted bound.

## Stage the production import without opening

Use an inspected Yukon checkout. The importer command was verified at Yukon
`5f79ad1009291f155f6664e895efefa9b72de340`; its package alias is
`import-benchmark`. From that repository, with the importer credential already
provisioned in the process environment, run:

```sh
bun run scripts/import-benchmark.ts https://github.com/Layr-Labs/hash-smash --prod
```

This command creates a production import and waits for baselines. Omit `--open`.
The optional timestamp on `--open` is a closing time, not a scheduled launch.
Inspect the command's resolved production API and intended setter/challenge name
before use; add `--name` only for an explicitly agreed namespace. The inspected
importer has no source-branch flag: verify `main` is the repository default and
that the resolved import commit is the exact reviewed release. Check for an
existing production registration before creating a fresh one. A timeout does not
cancel the import; inspect returned IDs before retrying an uncertain request.

Record all six production track IDs, resolved source commit, baseline job IDs,
GitHub run URLs, App actor, evidence/review fingerprints, review labels and scores.
Verify the artifact's exact repository-relative score path under
`lanes/exploratory/.yukon/scores/`, successful qualification for all six tracks,
and no successful score artifact on failure. Keep the ready challenge unopened.

Read back `promotionMode: manual` on every production registration. A qualifying
improvement must enter owner review without changing the promoted best; the owner
accepts the inspected candidate SHA through Yukon before Yukon queues promotion.
Before launch, verify legitimate improvement, protected-path rejection and
sibling preservation through the real production lifecycle. Do not manufacture
improvement claims or manually merge a submission PR to test this sequence.

Final launch time, visibility, rewards, production UI references and human signoffs
remain separate owner decisions. Open submissions only after explicit launch
approval and completion of the production verification gates.
