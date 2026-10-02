# Paired collision-frontier lanes

Roster update: 2026-09-25. The root Yukon manifest selects **six exploratory
tracks**: SHA-256 31/32, SHA3-256 5/6, and BLAKE3 1/2. The challenge will add two
Poseidon targets after their parameters and round pair are defined. The historical
local catalog below retains **24 runnable lanes and 4 deferred Poseidon slots**
for research and compatibility; it is not the active Yukon roster. Reconciliation
archives the fourteen omitted registrations while preserving the six retained
track identities and results. Editing the manifest alone does not change Yukon.
See [FRONTIER_VALIDATION.md](./FRONTIER_VALIDATION.md) for test evidence and limits.

## Roster and selection limits

Every concrete target below has an independent `exploratory` and `rigorous` lane.

| Mockup family | Concrete target / settings | Lane count | Selection status |
| --- | --- | --- | --- |
| MD5 | `md5-s63`, `md5-s64` | 4 | Penultimate/full-round controls; full MD5 is broken |
| SHA-1 | `sha1-r79`, `sha1-r80` | 4 | Penultimate/full-round controls; full SHA-1 is broken |
| SHA-256 | `sha256-r31`, `sha256-r32` | 4 | User-selected classical ordinary-collision frontier pair |
| Keccak[1600] | `sha3-256-r5`, `sha3-256-r6` | 4 | Selected SHA3-256 instance; rate 1088, capacity 512, output 256 |
| BLAKE3 | `blake3-r1`, `blake3-r2` | 4 local / 2 imported | Organizer-selected unkeyed BLAKE3-256 exploration pair; boundary unverified |
| Keccak[800] r544/c256 | `keccak800-r5`, `keccak800-r6` | 4 local / 2 imported | Organizer-selected exploration pair; output 256, legacy pad10*1, prefix rounds; boundary unverified |
| Poseidon | Not yet assigned | 4 reserved | Field, width, mode, constants, output and reduction schedule unresolved |

The user approved deferring undefined round pairs. The MD5/SHA-1 control exception
and precise SHA3-256 instantiation are explicit organizer choices to confirm before
publication. There is no first-unbroken standard round for MD5 or SHA-1; rounds
65/81 must not be invented to manufacture one. The mockup's plotted records are
synthetic, not cryptanalytic evidence. See [FRONTIER_RESEARCH.md](./FRONTIER_RESEARCH.md)
for primary sources, exact problem distinctions, and unresolved choices.

The selected boundaries reflect dated classical collision literature, not proofs
of security and not yet independently normalized best-known computation scores.
For every implementation, execute the **first** `r` rounds in every compression
or sponge permutation, with the fixed initialization, padding, full output and
serialization in its trusted target profile. SHA3-256 uses the SHA-3 domain suffix,
not legacy Keccak padding. This is prefix reduction, not Keccak-p's last-round
convention. Free-start, compression-only, quantum, and truncated-output attacks
do not solve these ordinary complete-message hash targets.

## Lanes and scoring

[JUDGE_LANES.md](./JUDGE_LANES.md) is the review contract. Four independent roles
inspect evaluability, cryptanalysis, resources and experiments. A proposed fatal
error goes through a defender and adjudicator. A single evidence package produces
both decisions; only the selected lane can emit a score.

- Exploratory pass: `plausible_not_refuted`. Relevant support exists and no fatal
  flaw has survived adjudication. Material uncertainties remain visible.
- Rigorous pass: `ai_rigor_qualified`. Material obligations and heuristic claims
  meet ordinary cryptanalytic standards for the claimed regime.
- Missing evidence, infrastructure errors, drafts and refuted claims never score.
  An exploratory success is not automatically a rigorous baseline.

These are AI judgments, not formal proofs, human acceptance, or measured error
rates. The committee supports different models and prompting strategies per role
via `judge/committees/paired-roles-v1.json`. All roles default to the configured
provider/model, with different strategies. No majority vote or numerical model
confidence threshold substitutes for proof obligations. Success probability in a
claim means algorithmic success, not confidence that the judge is right.

The fixed `collision-frontier-v5` cost model ranks
`log2(total charged time)`, lower is better, with success
probability at least 0.39. Preprocessing, failed trials, verification, advice and
code storage count in the resource ledger. Memory is required and reviewed, but
does not affect the scalar or break ties. Time sums work across all processors.
This shared policy applies to all 28 planned slots, including those whose target
definitions are still pending; it does not activate unresolved slots. A trusted selected-target compression/permutation costs one
unit; other 256-bit RAM operations are charged as specified in the model.

The display reference is nominal collision-security exponent: 64 for MD5, 80 for
SHA-1, 128 for these 256-bit targets. It is **not** a measured attack, an executable
baseline, or a proved total-computation bound. A birthday exponent alone does not account
for implementation constants. Actual submissions must still report memory bytes.
Profiles, policies and scores are isolated by lane; historical artifacts are never
reinterpreted under the paired policy.
Nominal references cannot satisfy Yukon's successful-baseline import requirement.

## Local use

From the repository root:

```sh
bash .yukon/setup.sh
python3 scripts/local_tracks.py list
python3 scripts/local_tracks.py catalog
python3 scripts/validate_frontier_config.py
python3 scripts/local_tracks.py show sha256-r31-exploratory
python3 scripts/local_tracks.py check sha256-r31-exploratory
```

For that example, a solver may edit only
`lanes/exploratory/candidates/sha256-r31/`. New templates start as `draft`; inspect
the selected package for its current state. Once a substantive claim/proof and
optional evidence are ready, set its state to `ready`; this enables review, not
automatic acceptance.

```sh
python3 scripts/hashsmash_pipeline.py intake --track sha256-r31-exploratory
```

Then, in a trusted shell with provider credentials configured, run `judge` and
`score` using the same explicit track, or `all` for a complete local run. Bedrock
settings remain `HASHSMASH_JUDGE_PROVIDER=bedrock`,
`HASHSMASH_BEDROCK_MODEL=us.openai.gpt-5.6-sol`, and
`HASHSMASH_BEDROCK_REGION=us-east-1`; select `HASHSMASH_JUDGE_MODE=committee`
for per-role prompt/model overrides. No commands from the candidate are run on
the host. Credentials are never passed into the experiment container.

Scores: `lanes/<lane>/.yukon/scores/<target>-<lane>.json`.
Reports and immutable run archives: `lanes/<lane>/.yukon/reports/tracks/<target>-<lane>/`.
Evidence: the parallel `.yukon/work/tracks/` tree. These outputs are ignored by Git.
Target, claim, source, evidence, policy and review-configuration fingerprints bind
the run; changed inputs require fresh intake/review. Pipeline and verifier commands
require `--track`; select the complete organizer ID including its lane.

## Executable heuristic evidence

[HEURISTIC_EXPERIMENTS.md](./HEURISTIC_EXPERIMENTS.md) documents the manifest and
source protocol. Claims disclose each heuristic's role, evidence, scope,
extrapolation and limitations. References point to proof lines or declared
experiment IDs. Experiments are required when declared; an analytic proof need
not include a meaningless empirical program.

The MVP supports exact/sampled modular-addition differential checks and submitted
Python message-pair generators. Python runs in a digest-pinned, networkless,
non-root Docker sandbox with no credentials, a read-only filesystem, resource and
output caps, fixed seeds, and a repeatability check. Organizer code independently
recomputes selected-target collisions or declared output-mask events. Source is
included as inert, untrusted judge evidence. Undeclared files are rejected.

Docker must be running and the pinned image available for Python experiments:

```sh
python3 scripts/prepare_experiment_image.py --track sha256-r31-exploratory
HASHSMASH_TEST_DOCKER=1 python3 -m unittest tests.test_experiments
```

Image preparation reads the selected ready manifest and pulls only the organizer's
pinned image. It does not execute the submission. Without Docker/image availability,
Python experiments stop as a development setup failure, not a rejected mathematical
claim. Exact/sampled organizer evaluators need no Docker. There is no unsafe host fallback.

Measured internal values, reported costs and execution wall time are not trusted
attack costs. A finite run does not establish expected time; small-word experiments
do not establish independence across full-size rounds. Fixed-seed reproducibility
does not establish ideal randomness. The runner records these limitations explicitly.
`HASHSMASH_EXPERIMENT_HOLDOUT_NONCE` allows organizer-selected fresh holdout seeds
after freezing a submission; the nonce and full result are recorded for replay.

For a finite live judge diagnostic using organizer toy examples only:

```sh
bash scripts/run-paired-calibration.sh --provider bedrock --model us.openai.gpt-5.6-sol --mode committee --case all
```

The wrapper runs the offline suite, then loads local `.env` without printing it.
Three toy cases cover an exact valid proof, a concrete false proof and an explicitly
uncertain empirical heuristic. Each case is bounded to four to six stage calls,
one transport attempt per stage, and fixed output/time caps. No challenge candidates
are read or scored. Reports go to `.yukon/reports/paired-calibration/`; unexpected
verdicts require inspection, especially the heuristic case whose truth is not a
ground-truth label. See its organizer [fixture notes](../tests/fixtures/paired-calibration/README.md).

This initial harness does not mechanically validate every possible internal
differential condition. Such measurements remain source-reviewed observations
until a new organizer-owned typed evaluator is added with tests and a versioned
fingerprint. Do not generalize a checked output predicate to unmeasured heuristics.

## Yukon manifest and deployment gates

Import the repository root once as `hashsmash`. The root schema-v2
[`benchmark.json`](../benchmark.json) contains six exploratory SHA-256, SHA3-256,
and BLAKE3 tracks. Other lanes remain local with independent review decisions.
Every track uses its full
`<target>-<lane>` ID, such as `sha256-r31-exploratory` or
`sha256-r31-rigorous`, in both Yukon and organizer commands. No `rootDir`
override or separate lane import is needed.

The protected track registry stores each lane. Claim validation and review
fingerprints bind a package to that lane, and generated scores retain it in
`metrics.lane`. Yukon's strict manifest schema has no arbitrary metadata field;
track names and descriptions expose the distinction using supported fields.
The lane directories retain their separate candidate, score and report paths.

The literal per-track `workflow_dispatch` wrappers call one reusable workflow.
No participant-controlled track input is needed. Editable paths, commands and
score paths in the manifest are repository-relative. For example, the exploratory
SHA-256 r31 track edits `lanes/exploratory/candidates/sha256-r31` and uploads only
`lanes/exploratory/.yukon/scores/sha256-r31-exploratory.json` at that exact path.

Yukon permits at most 20 active tracks. Use manifest reconciliation to retire
the fourteen omitted registrations, preserving their history and all retained
track records. Reorg remains a separate operation for configuration changes.
Keep the retained names, including their lane suffixes: a rename creates a new
identity. Poseidon requires exact definitions and qualified baselines before its
two exploratory targets can be added. Do not split the repository into lane imports.

Workflow separation is intentional: a credential-free job validates and executes
experiments, a fresh secret-bearing job reviews immutable same-run artifacts
without executing participant code, and a fresh credential-free job deterministically
reaggregates and scores. Only that run's selected score is uploaded. Artifact origin,
not just a self-reported hash, is part of the trust boundary. Local generated
artifacts must likewise remain organizer-controlled.

For dev setup and exact import commands, use [YUKON_DEV_SETUP.md](./YUKON_DEV_SETUP.md).
Candidate authors should follow [CANDIDATE_QUALIFICATION.md](./CANDIDATE_QUALIFICATION.md).

Before activating the imported exploratory lanes:

1. Preserve the selected SHA-256, SHA3-256, and BLAKE3 target definitions.
2. Keep the undefined Poseidon slots deferred. To add two exploratory targets later,
   establish exact definitions and defensible or explicitly provisional round pairs, then
   update catalog, profiles, templates, schemas, manifest, wrappers and checker
   tests. `--require-complete` checks that eventual full roster only.
3. Establish an admissible baseline separately for each activated lane, or obtain a
   supported Yukon change allowing an initially empty frontier. Drafts/nominal
   references cannot be passed off as successful baselines.
4. Arrange the Yukon dev GitHub App/importer access and confirm the deployment supports
   schema v2 and reconciliation. A fresh import queues six baseline workflows;
   reconciliation queues baselines only for new or eligible retried tracks. Run an end-to-end dev import, submission and
   promotion test, including preservation of sibling tracks across both lanes.
5. Calibrate both lane policies on labeled real cryptanalysis, with human review of
   false positives, false negatives and disagreements. Toy/fake-provider tests establish
   integration behavior, not real-world judge quality.
