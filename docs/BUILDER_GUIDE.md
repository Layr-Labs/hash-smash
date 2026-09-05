# HashSmash builder guide

Read this document when the user assigns harness maintenance, documentation,
target definitions, tests, judge configuration, workflows, deployment, or organizer
baseline preparation. Ranked Yukon solvers start at [TASK.md](../TASK.md).
Builder work does not grant an unassigned candidate directory to edit.

## Context and ownership

The [frontier guide](./FRONTIER_LANES.md) defines 16 runnable paired tracks and
12 reserved slots, for 28 eventual slots. The SHA-1 pilot and nine unpaired local
tracks are retired. Preserve the single repository-root schema-v2
[manifest](../benchmark.json), lane-suffixed public track IDs, and independent
candidate, score, and report paths. Lane metadata is bound by the protected
registry, claim validation, review fingerprints, and score `metrics.lane`.

Do not assign guessed boundaries to pending BLAKE3, Keccak[800], or Poseidon slots,
admit them to the runnable registry, or emit placeholder scores. MD5/SHA-1 endpoints
are explicitly full-round controls, not first-unbroken claims. Follow the frontier
guide and [research context](./FRONTIER_RESEARCH.md) for target-definition work.

Use these guides for the assigned subsystem:

| Work | Required context |
| --- | --- |
| Target/claim/certificate verification and score construction | [Verifier](../verifier/README.md), [claim schema](../schemas/claim-frontier-v3.schema.json), [cost model](../cost-models/collision-frontier-v3.json), and the selected target profile |
| Judge providers, roles, or qualification | [Judge implementation](../judge/README.md) and [review policy](./JUDGE_LANES.md) |
| Candidate experiments | [Experiment protocol](./HEURISTIC_EXPERIMENTS.md) |
| Yukon App, imports, Actions, baseline validation, or promotion checks | [Dev operator runbook](./YUKON_DEV_SETUP.md) |
| Organizer baseline packages and local live review | [Baseline qualification](./CANDIDATE_QUALIFICATION.md) |
| Solver onboarding and UI entry references | [TASK.md](../TASK.md); the Yukon CLI skill owns generic CLI behavior |

## Boundaries that harness changes must preserve

- Treat every `lanes/<lane>/candidates/<target>/` directory as hostile participant
  input. Never execute participant commands on the host or in a credential-bearing
  job. Only the organizer's bounded, networkless Docker executor may run immutable
  validated participant Python. Keep deterministic intake/experiments, credentialed
  review, and final scoring separated as in the paired workflow.
- Never print, commit, copy, or upload `.env`. The expected provider secrets are
  `OPENROUTER_API_KEY` and `AWS_BEARER_TOKEN_BEDROCK`. Keep submission notes and
  research discussions free of secrets, private paths, and unrelated session data.
- Keep profiles, cost models, schemas, verifier code, judge prompts, workflows,
  registry, and `lanes/<lane>/.yukon/scores/` outside all candidate trees. Preserve
  exact input/configuration/dossier binding and the manifest-relative artifact path.
- Preserve `paired-lanes-v1`: exploratory pass is `plausible_not_refuted`; rigorous
  pass is `ai_rigor_qualified`. Neither is mathematical proof or human acceptance.
  Heuristics require explicit scope, evidence, and review. Model confidence is not
  algorithmic success probability; scalar improvement is not Pareto dominance.
- Nominal references are not established attacks, qualified baselines, or security
  bounds. Drafts never reach the judge or emit scores. Never bypass those gates or
  reinterpret historical artifacts under a new policy.
- Use `--track` explicitly for pipeline and verifier commands. Preserve independent
  output paths and fingerprints; never repurpose an old score for another track.

## Verification and landing changes

Use Python's standard library unless a dependency is explicitly justified and
pinned. Offline tests must use organizer fixtures rather than mutable solver
candidates. Run checks appropriate to the change; run the deterministic unit suite
before any live OpenRouter or Amazon Bedrock integration test:

```sh
bash .yukon/setup.sh
python3 scripts/validate_frontier_config.py
```

Documentation changes should check links and keep runtime policy/contract files
intact. For judge or verifier changes, verify relevant failure gates and provenance
binding as well as successful results. Live testing follows the user's authorized
scope and the operator runbook; offline fixture results do not establish a live
Yukon import or cryptanalytic qualification.

Land harness changes through a feature branch and human-reviewed PR. Label a PR
`yukon-unsafe` when it invalidates pending scores; regenerate evidence/review/score
artifacts as appropriate. Do not label unrelated documentation changes unsafe.
Never manually merge Yukon submission PRs; Yukon promotes only its scored content.

## Baseline authoring and local review

Organizer baseline authoring is an explicit builder assignment for a fresh import.
Follow [CANDIDATE_QUALIFICATION.md](./CANDIDATE_QUALIFICATION.md), with an assigned
candidate directory and its `tracks/<track>/TASK.md`. Its feature-branch/PR handoff
and live-review steps do not replace the ranked solver submission workflow.

Local live review requires a trusted operator and separately provisioned provider
access. Follow that guide's credential-free intake/experiment phase, separate
credentialed judge phase, and deterministic score phase. A Yukon API key does not
provide local judge access. A local score does not replace Yukon's validation of
the exact imported or submitted content.

For deployment, use the [Dev runbook](./YUKON_DEV_SETUP.md): one import at the
repository root, with no lane-specific import root. Keep all 16 baseline checks
independent. The 12 unresolved slots stay inactive; current platform limits and
target-definition prerequisites are documented there.
