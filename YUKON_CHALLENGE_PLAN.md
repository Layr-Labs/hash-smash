# HashSmash Yukon Challenge Plan

Status: local MVP and nine experimental tracks implemented; qualification calibration remains open, 2026-09-03

Scope: first Yukon deployment for Markdown-described collision attacks  
Latest Yukon documentation/source revision reviewed: `d9471fe70a431a3c424758c3eb58d51d38e73d67`

## Implementation update

The local MVP now implements the pilot described below plus the experiment roster in
`LOCAL_TRACKS.md`:

- a schema-v1 Yukon manifest and pinned GitHub Actions workflow;
- strict participant intake limited to `candidate/` (legacy) or one `candidates/<track>/`;
- typed collision witnesses with trusted MD5/SHA-1/SHA-256 prefix-round checkers;
- a three-stage judge with OpenRouter/Sol and Amazon Bedrock/Opus or Sol backends;
- four versioned prompt strategies and a configurable three-model committee;
- deterministic, fail-closed aggregation and trusted score emission; and
- 136 credential-free tests, plus historical targeted live provider calibration;
- nine isolated local tracks with nominal references, draft gates and archived runs.

The workflow remains intentionally single-judge by default while committees are
calibrated. Repository variable `HASHSMASH_JUDGE_PROVIDER=bedrock` selects Bedrock without
exposing the OpenRouter secret to that workflow step. Committee mode is implemented and
locally selectable through strict provider-specific JSON profiles. Production remains
gated on cryptographer ratification, selected-provider validation, dev App access to the
existing GitHub repository, and an allowlisted Yukon dev importer
credential. See `MVP_VALIDATION.md` for the current evidence and exact blockers.

The policy decision is now resolved: no additional unproved cryptanalytic assumptions
are allowed. `unconditional-v1` is trusted, versioned judge policy; reported unproved
premises block aggregation regardless of positive votes. The older heuristic candidate
is not exempt and is currently a negative control, not a qualified baseline. A
distribution-free birthday argument for a randomized replacement is documented in
`UNCONDITIONAL_BASELINE.md`; its new program/resource ledger remains to be implemented.

Yukon natively supports schema-v2 independently scored tracks on one shared branch.
`YUKON_MULTITRACK_PLAN.md` records the current 20-track limit, workflow routing, and
per-primitive/per-round profile layout. Local tracks are now implemented, but the active
Yukon manifest is still v1. The user chose the scalar time-memory objective for the local
experiment, not Pareto-frontier promotion. Nominal reference values are not qualified
baselines and do not waive Yukon's import requirement.

Bedrock Sol uses the Responses API with a versioned prompt-supplied JSON schema and the
same strict local validation, while Claude retains Converse structured output. Select
Sol explicitly with `HASHSMASH_BEDROCK_MODEL=us.openai.gpt-5.6-sol`; the default model and
existing committee profiles remain unchanged. The Responses request disables stored
conversation state (`store=false`) and enables no tools. This does not replace a review
of the account's AWS data-retention and abuse-monitoring settings.

## Executive recommendation

Build the first HashSmash deployment as a deliberately narrow, hybrid-reviewed Yukon
track. Do not launch all targets, round counts, and cost tradeoffs as one benchmark.

The recommended pilot is one fixed target profile, attack class, and round count—for
example, ordinary full-round SHA-1 collisions—with a lower-is-better scalar cost score.
A submission consists of a machine-readable claim, a Markdown proof, and optional typed
certificates. Deterministic checks validate the package and any certificates. Independent
LLM reviews then audit correctness and complexity. A passing LLM result means only
`ai_qualified`; a qualified human cryptanalyst must still accept the result before it is
represented as a verified HashSmash result.

This boundary is important. An LLM can find gaps, reconstruct arguments, and produce an
excellent review dossier, but it cannot turn an informal Markdown argument into a formal
proof. Yukon normally assumes a trusted objective verifier. HashSmash initially has an
evidence-review process instead. The product and repository must say so everywhere the
result is displayed.

The pilot should be considered successful when it can process an organizer-authored
account of a known attack (the Wang et al. SHA-1 attack is the proposed end-to-end test),
reject seeded technical errors and prompt-injection attempts, produce useful citations and
author questions, keep the API credential isolated, and route the surviving claim to a
human without calling it accepted prematurely.

## What Yukon provides and what HashSmash must provide

Yukon turns a GitHub repository into an optimization benchmark. For the GitHub Actions
execution path:

- The repository defines `benchmark.json`, the editable surface, local setup/run commands,
  score direction, score path, and production workflow.
- Yukon accepts a tarball containing replacements for only `editablePaths`, creates a
  `submissions/<submissionId>` candidate branch and PR, and dispatches the configured
  workflow on that exact candidate.
- The workflow must be `workflow_dispatch`-driven, run from a clean checkout, and upload
  an artifact containing the exact score path.
- The score must be finite and numeric. A failed correctness or verification gate should
  exit nonzero rather than emit a placeholder score.
- Yukon compares the score with the current best and manages the promotion candidate.
  Only the scored content, or a content-identical editable-path graft on a newer trusted
  tip, is eligible for promotion.
- Yukon enforces the editable surface server-side, but the workflow should recheck the
  effective diff before processing untrusted content.

HashSmash must define the parts that are objective in earlier Yukon benchmarks:

- the canonical target profile and collision notion;
- the exact cost model and success-probability convention;
- a submission schema;
- deterministic certificate checkers where possible;
- the LLM review protocol and calibration corpus;
- the meaning of an AI pass;
- the human acceptance, appeal, correction, and retraction process; and
- how a multi-dimensional Pareto frontier is mapped onto Yukon's scalar, per-track model.

## Why one global HashSmash track would be wrong

The HashSmash objective compares at least:

- target and target-profile version;
- collision class;
- rounds or steps attacked;
- online time;
- peak memory;
- data or oracle queries;
- preprocessing and nonuniform advice;
- success probability; and
- restrictions and assumptions.

Yukon schema v1 and each schema-v2 track have one direction and one finite scalar score.
Neither LLM confidence nor a weighted mixture of unrelated cryptanalytic claims is a
scientifically meaningful global score. A lexicographic encoding such as “rounds times a
large constant minus cost” would also destroy the intended Pareto semantics.

Therefore:

1. The pilot should use one fixed target profile, collision class, and round count.
2. Within that fixed profile, use one published scalar cost definition. If the pilot follows
   the current short HashSmash definition, the score can be
   `log2(time × memory) = time_log2 + memory_log2_bytes`, with lower being better.
3. Keep time, memory, data, preprocessing, probability, and restrictions separately in
   `metrics`; never erase them merely because one scalar is needed for Yukon.
4. After the pilot, create separate schema-v2 tracks only for combinations whose target
   profile and scoring convention are stable. Track editable paths must be disjoint.
5. Maintain the real cross-track Pareto frontier in a trusted HashSmash index outside the
   solver-editable surface. Do not infer it from one Yukon leaderboard column.

The exact pilot target is a setter decision. Full-round SHA-1 is attractive because
HashSmash already proposes reconstructing the famous published attack as a test, but its
baseline cost vector and attack-class definition must be ratified by a cryptographer before
they enter the repository.

## What “verified” should mean

Use four visibly different states:

| State | Meaning |
| --- | --- |
| `mechanically_valid` | The package, claim schema, target identifier, hashes, and any declared certificates passed deterministic checks. |
| `ai_qualified` | The calibrated review harness found no unresolved technical blocker. This is a review result, not a proof. |
| `human_accepted` | A qualified human cryptanalyst reviewed the original package and dossier and accepted the exact claim. |
| `formally_verified` | An organizer-controlled proof checker established the exact theorem and cost claim. This state is reserved for a later proof-carrying track. |

The initial Yukon workflow may produce only `ai_qualified`. It must not label that state
`verified`, `correct`, or `accepted` in `score.json`, PR comments, job summaries, or the
frontend.

Before production import, confirm with the Yukon team whether an improving PR can remain
unpromoted pending human review. If promotion is automatic or cannot be held reliably,
use one of these alternatives:

- Treat the Yukon repository and leaderboard explicitly as an AI-screened provisional
  queue, while a separate maintainer-controlled accepted-results index records human
  decisions; or
- Keep the pilot private and non-production until the platform supports a manual promotion
  hold.

Do not add a long-running GitHub environment approval gate without first confirming Yukon
workflow timeouts and cancellation behavior.

## Submission contract

### Editable package

For a schema-v1 pilot, expose one directory such as `candidate/`:

```text
candidate/
  claim.yaml
  proof.md
  certificates/
    manifest.json
    ... optional typed certificate data ...
```

Only `candidate/` belongs in `editablePaths`. The target definitions, cost model, frontier,
prompts, judge schemas, checkers, workflow, and score path remain trusted and non-editable.

Start with Markdown only. Reject PDF, HTML, notebooks, archives inside the submission, and
submitted executables during the pilot. Markdown should be normalized to UTF-8/LF, limited
to a calibrated size, and treated as inert text. External links are citations, not content
that the ranked judge follows.

### Required claim fields

The claim manifest should use an organizer-owned JSON Schema and contain at least:

```yaml
schema_version: 1
target_profile: sha1-fips180-4-v1
attack_class: ordinary-collision
rounds: 80
claim:
  time_log2: 69.0
  time_unit: sha1-compressions
  memory_log2_bytes: 0.0
  data_log2: 0.0
  preprocessing_log2: 0.0
  success_probability: 0.5
  nonuniform_advice_log2_bytes: 0.0
restrictions: []
baseline_improved: organizer-result-id
certificate_manifest: certificates/manifest.json
```

The example values are illustrative, not a ratified Wang-attack baseline. The target
profile must define padding, feed-forward, initialization, message constraints, round
numbering, output comparison, and the precise ordinary-collision relation. The cost model
must define every unit, which costs are online versus reusable, how success is amplified,
and what memory quantity is scored.

Require the proof to have stable headings so reviewers and humans can navigate it:

1. Claim and target profile
2. Preconditions and restrictions
3. Attack algorithm
4. Correctness argument
5. Probability argument
6. Time, memory, data, and preprocessing analysis
7. Connection between certificates and lemmas
8. Prior work and claimed improvement
9. Known gaps or unverified assumptions

The ingestion step should add canonical line numbers to a review-only copy. LLM citations
must point to those line numbers and claim-manifest paths.

## Are numerical certificates likely to be needed?

Yes, but as heterogeneous, claim-specific evidence—not as one universal numeric file and
not as a substitute for the proof.

HashSmash admits attacks that are far too expensive to execute at full scale. For such an
attack, no feasible workflow can simply run the algorithm and observe a collision. The
central correctness and asymptotic-complexity claims remain mathematical arguments. A
small experiment may expose an error but cannot validate the extrapolation.

The repository should nevertheless support these certificate classes from the start:

| Certificate | When to require it | What an organizer checker can establish | What it does not establish |
| --- | --- | --- | --- |
| Concrete collision witness | Required when the target profile says the claimed regime is practically executable, or whenever the submission claims an actual produced collision. | The messages differ and hash to the same value under the canonical target implementation. | The claimed expected cost, general algorithm, or novelty. |
| Reduced-parameter execution record | Optional initially; required when an argument relies on experimental behavior at reduced scale. | The pinned implementation produces stated reduced-instance outputs and measurements. | Full-scale correctness or asymptotic extrapolation. |
| Differential/trail certificate | Conditional when the attack depends on an explicit trail and an organizer checker exists. | Local transition compatibility, bit conditions, weights, and exact bookkeeping encoded by the checker. | Independence assumptions, global probability, or completeness unless those are also certified. |
| SAT/SMT/MILP certificate | Conditional when a central lemma is solver-derived and has an approved proof-producing checker. | The precise encoded instance has the certified property. | That the encoding matches the paper or canonical primitive unless separately checked. |
| Exact arithmetic/probability worksheet | Required as structured claim data; optionally strengthened with exact rational or symbolic certificates. | Arithmetic consistency and recomputation from stated premises. | Whether the premises and probabilistic model are justified. |
| Lean theorem/certificate | Optional in the informal pilot; required only in a separate formal track. | The exact theorem type, allowed imports/axioms, and kernel-checked proof. | Relevance to the intended informal claim unless the theorem template and target model are canonical. |

The launch rule should be: require a concrete witness where feasibility makes that honest;
otherwise accept Markdown without a universal certificate, but require authors to declare
which central steps are only argued informally. Add typed certificate requirements one
target and technique family at a time as sound checkers become available.

Long term, the proof-carrying proposal in `HashSmash.md` should be a separate Yukon track,
not a silent tightening of the informal track. Its objective verifier would pin Lean,
canonical primitive definitions, theorem templates, cost/probability semantics, allowed
axioms/imports, and bounded checking resources.

## Verification and judging pipeline

The production workflow should separate deterministic processing, untrusted execution,
and secret-bearing model calls into different jobs. Never run participant code in the job
that has the model-provider credential.

### Job 1: trusted intake, no secrets

1. Check out exactly `${{ github.sha }}` with persisted Git credentials disabled.
2. For `submissions/*`, recheck that the effective candidate delta changes only the
   declared editable directory. Reject symlinks, special files, executable bits, nested
   archives, path tricks, and unexpected file types.
3. Enforce Yukon's expanded `maxSubmissionBytes` plus tighter per-file and Markdown limits.
4. Validate `claim.yaml` against the pinned schema with unknown fields rejected.
5. Verify the selected target, class, and round count equal the track constants.
6. Normalize and line-number `proof.md` without modifying the submitted artifact.
7. Hash every submitted file and emit `intake-report.json`.
8. Reject a dominated or malformed scalar claim mechanically where that can be decided
   without judging correctness.

This job handles untrusted data but executes no participant-provided code.

### Job 2: certificate checking, no secrets and no network

1. Select checkers only from an organizer-owned allowlist keyed by certificate type and
   version. A submission never supplies a command to run.
2. Run each checker in a bounded sandbox with no credentials, no network, a read-only
   root where practical, explicit CPU/memory/time/file limits, and a fresh workspace.
3. Recompute concrete collisions with the canonical implementation.
4. Treat reduced-instance runs as experiments and label them accordingly.
5. Emit structured results listing the exact input hashes, checker versions, commands,
   resource use, and verified subclaims.
6. Upload only sanitized reports to the judge job. Do not pass arbitrary logs directly
   into prompts.

If future submissions include source code or reproducers, execute them only here or in a
still more isolated job. Terminate that environment before starting any secret-bearing job.

### Job 3: LLM triage, provider secret present

The judge receives only:

- the canonical target profile and cost model;
- the current trusted frontier entry for this fixed track;
- the validated claim manifest;
- the inert, line-numbered Markdown proof; and
- sanitized deterministic certificate reports.

It receives no repository tools, shell, web access, GitHub token, unrelated files, or
private reviewer material. Submission text is serialized as a quoted data field and is
explicitly designated untrusted evidence. Prompt injection is still possible; delimiting
text is a mitigation, not a proof of isolation.

Triage decides only:

- `pass_to_specialists`;
- `author_clarification_needed`; or
- `out_of_scope` / a directly demonstrated fatal intake error.

Novel or unfamiliar methods pass with questions. Triage must not decide technical
correctness or novelty from model memory.

### Job 4: independent specialist reviews

Run at least these reviews without showing them one another's output:

1. Correctness reviewer A reconstructs preconditions, algorithm, and postcondition, checks
   each nontrivial inference, and attempts counterexamples.
2. Correctness reviewer B performs the same task independently, preferably with a
   different model family or provider.
3. Complexity reviewer recomputes every cost and probability dimension under the pinned
   cost model, including amplification, preprocessing, memory hierarchy, data, advice,
   parallelism, and hidden verification cost.

Two calls to the same model and prompt are replications, not genuinely independent expert
evidence. Label them honestly. Model diversity is useful for error discovery but never
turns agreement into proof.

Every review uses a strict JSON Schema. Required fields include:

- verdict: `supported`, `unsupported`, or `unclear`;
- explicit claim reconstruction;
- verified steps and exact evidence citations;
- fatal blockers versus missing explanations;
- assumptions and their effect on the claim;
- attempted counterexamples;
- submitted and recomputed cost vectors;
- certificate-to-lemma mapping;
- questions for the author; and
- confidence as metadata only.

Schema conformance does not imply semantic correctness. Trusted aggregation code must
reject contradictions such as `supported` alongside an unresolved fatal blocker.

### Job 5: adversarial review and synthesis

An adversarial reviewer sees the original evidence and independent structured reviews. It
tries to turn disagreements into concrete counterexamples, failed conditions, or cost
recalculations. A separate synthesis pass preserves disagreements and creates a finite
human-review checklist.

The trusted aggregator, not an LLM, maps the structured records to one of:

- `ai_qualified`: no surviving fatal blocker, required specialists agree on the exact claim
  and normalized cost, and all deterministic gates passed;
- `clarification_required`: any material ambiguity or reviewer disagreement;
- `technical_blocker`: a cited error invalidates the claim as stated; or
- `judge_infra_failed`: no valid verdict exists because the provider, timeout, or parser
  failed.

Only `ai_qualified` writes a score. Clarification and technical-blocker runs exit nonzero
and publish a useful review summary. Infrastructure failure exits nonzero with a distinct,
re-dispatchable reason and must never be reported as rejection.

### Job 6: score and dossier publication

Trusted code calculates the score from the validated claim; an LLM never supplies the
leaderboard number. A pilot score file could be:

```json
{
  "score": 103.0,
  "metrics": {
    "reviewStatus": "ai_qualified",
    "targetProfile": "sha1-fips180-4-v1",
    "attackClass": "ordinary-collision",
    "rounds": 80,
    "timeLog2": 69.0,
    "memoryLog2Bytes": 34.0,
    "timeMemoryLog2": 103.0,
    "successProbability": 0.5,
    "inputPackageSha256": "...",
    "judgeConfigSha256": "...",
    "dossierSha256": "..."
  }
}
```

Again, these numbers are illustrative. Upload the exact non-editable `scorePath` in a
small score artifact. Upload the structured dossier separately for diagnostics, with raw
provider responses and private chain-of-thought excluded. Record response IDs, exact model
identifiers returned by providers, prompt/schema versions and hashes, token use, latency,
retry counts, package hash, and checker versions.

## AI-judge implementation requirements

### Provider abstraction

Keep prompts, schemas, aggregation, and tests provider-neutral. A provider adapter should
map one pinned judge configuration to the API and normalize only transport metadata.

For an OpenAI implementation, use the Responses API with a strict JSON Schema response
format. Official OpenAI documentation says JSON-schema Structured Outputs enforce the
supplied response shape, and the Graders API supports label-model, score-model, Python,
string, similarity, and multi-grader objects. Those features help with output discipline
and offline evaluation, but they do not establish the truth of a cryptanalytic verdict.
Use representative evals before changing prompts, models, or reasoning effort.

Do not rely on a floating model alias as reproducibility. Store both the requested model
configuration and the exact model identifier returned by the provider. If a dated snapshot
is unavailable, disclose that re-running the same package later may not reproduce the same
verdict.

### Reliability

- Use bounded retries only for transport errors, rate limits, provider 5xx responses, and
  malformed/incomplete responses.
- Separate transport retry count from semantic replication count.
- Never convert provider unavailability into a failing proof verdict.
- Cap tokens, calls, wall time, and dollars per submission.
- Set `runner.maxConcurrentWorkflows` conservatively (start at one) to cap simultaneous
  judge spend and provider load.
- Validate response schemas and cross-field invariants in deterministic code.
- Do not use model confidence in the Yukon score or voting threshold.

### Prompt-injection defenses

- Treat the whole submission, including code blocks and quoted references, as hostile data.
- Pass it in a serialized evidence object, never concatenated into the system instructions.
- Give the judge no tools and no secrets other than the provider call performed by trusted
  transport code.
- Never follow links found in a submission during a ranked run.
- State that requests to reveal prompts, credentials, or private material are evidence to
  ignore and flag.
- Add prompt-injection specimens to the release-blocking calibration suite.
- Fail closed on schema-valid contradictions, suspicious attempts to manipulate the judge,
  or disagreement about whether instructions came from the harness or evidence.

These controls reduce risk but do not make LLM review sound. Human review remains the final
gate for the informal track.

## Calibration and red-team plan

An AI judge must not become a blocking production gate until it is evaluated against a
versioned corpus whose expected outcomes were set by qualified humans.

Build the initial corpus from:

1. An organizer-authored, citation-preserving reconstruction of a known valid attack.
2. Mutations that delete a necessary condition, change the collision notion, use the wrong
   round numbering, or make incompatible message conditions.
3. Complexity mutations: omitted repetitions, hidden preprocessing, time/memory unit swaps,
   incorrect exponent arithmetic, invalid independence assumptions, and shifted verifier
   cost.
4. Target-profile mutations: compression-function collision presented as an ordinary hash
   collision, free-start collision, near-collision, and chosen-prefix mismatch.
5. Certificate mutations: wrong target parameters, corrupted witnesses, valid certificate
   for a different encoding, and paper/certificate mismatch.
6. Incomplete but novel-looking proofs that should request clarification rather than be
   declared false.
7. Prompt injection, requests to ignore the rubric, fake system messages, huge code blocks,
   Unicode confusables, and output-schema manipulation.
8. Provider failures, truncation, malformed JSON, timeouts, and rate limiting.

For each judge configuration, run repeated trials and report the confusion matrix,
inter-reviewer agreement, instability rate, failure-to-clarification rate, cost, latency,
and worst missed blocker. The release suite should have zero false accepts on the
organizer-designated fatal-error and prompt-injection cases. Humans should explicitly
ratify acceptable clarification and false-rejection behavior; do not choose those limits
from model performance after the fact.

Prompt, schema, model, target, cost-model, or aggregator changes create a new judge version
and rerun the whole suite. Preserve old results and version history.

## Proposed repository layout

```text
benchmark.json
README.md
TASK.md
AGENTS.md

candidate/                         # only solver-editable path in the pilot
  claim.yaml
  proof.md
  certificates/
    manifest.json

target-profiles/
  sha1-fips180-4-v1.yaml
cost-models/
  collision-cost-v1.yaml
frontier/
  sha1-full-collision-v1.json

schemas/
  claim-v1.schema.json
  certificate-manifest-v1.schema.json
  review-v1.schema.json
  score-v1.schema.json

verifier/
  intake.py
  check_surface.sh
  check_claim.py
  check_certificates.py
  compute_score.py
  aggregate_reviews.py
  checkers/

judge/
  run_review.py
  provider_adapter.py
  prompts/
    common-v1.md
    triage-v1.md
    correctness-v1.md
    complexity-v1.md
    adversarial-v1.md
    synthesis-v1.md

tests/
  fixtures/
    valid/
    invalid/
    clarification/
    prompt-injection/
  test_claim_schema.py
  test_score.py
  test_aggregation.py
  test_certificate_routing.py

.github/workflows/
  benchmark.yml

.yukon/score.json                 # generated, never editable
```

The implementation language can be chosen later. Python is a reasonable orchestration
choice, but every dependency must be pinned and installed by the trusted setup path.

## Initial `benchmark.json` shape

The first track should use schema v1. The values below are placeholders until the target,
cost model, limits, and workflow are tested:

```json
{
  "schemaVersion": 1,
  "name": "hashsmash-sha1-full-collision-pilot",
  "description": "Submit a Markdown proof of an improved full-round SHA-1 ordinary-collision attack for AI-assisted and human review.",
  "category": "cryptanalysis",
  "direction": "-",
  "editablePaths": ["candidate"],
  "setupCommand": ["bash", "-lc", ".yukon/setup.sh"],
  "benchmarkCommand": ["bash", "-lc", ".yukon/run.sh"],
  "scorePath": ".yukon/score.json",
  "maxSubmissionBytes": 4194304,
  "runner": {
    "provider": "github-actions",
    "workflow": "benchmark.yml",
    "maxConcurrentWorkflows": 1
  }
}
```

Do not set `minScoreImprovementBips` until the score's behavior near zero and the desired
minimum scientific improvement are specified. The current HashSmash notes suggest
quantizing improvements eventually; that policy should be explicit rather than inherited
from a convenient percentage.

For later schema-v2 use, each track needs a unique name and disjoint editable directory,
for example `candidate/sha1-full`, `candidate/sha256-39-round`, and so on. Shared target,
judge, and verifier files remain outside every editable path.

## GitHub Actions requirements

The workflow should:

- trigger only on `workflow_dispatch` for ranked validation;
- use minimal permissions (`contents: read`, `actions: read`, plus only a specifically
  justified permission such as OIDC if an external verifier needs it);
- check out the dispatched SHA, not a PR merge ref, with `persist-credentials: false`;
- pin third-party actions by immutable commit SHA;
- run from a clean checkout;
- use explicit `Setup` and `Benchmark` step names for Yukon failure classification;
- enforce the editable surface again before parsing the submission;
- put the provider key only in the judge job/environment;
- distinguish verification failure from infrastructure failure in the job summary;
- write no score unless every required gate reaches `ai_qualified`;
- upload the exact `.yukon/score.json` path; and
- keep the score artifact below Yukon's 50 MiB compressed and expanded limits.

Do not add a `pull_request` trigger to the ranked workflow; Yukon already creates a PR and
dispatches the workflow, so a PR trigger would duplicate evaluation and cost.

For a competitive pilot, prefer a private repository and a small collaborator cohort.
The Yukon guide says private repositories require the GitHub Actions path, the Yukon GitHub
App, and read access for participating solvers. Move public only after the disclosure,
appeal, review-transcript, and prompt-injection policies are settled.

## Human review, appeal, and scientific record

An `ai_qualified` result should produce a dossier for a named human judge containing the
immutable package hash, target/cost-model versions, independent reviews, disagreements,
certificate results, and a finite checklist. The human records `accept`, `revision`,
`reject`, or `external_review_needed` with a rationale.

Material changes to the algorithm, target, rounds, probability, restrictions, or cost
create a new submission version and rerun affected stages. Do not let private comments
silently mutate the public claim.

Accepted claims need an append-only record. Corrections and retractions remain visible.
An appeal must identify a concrete review error or new evidence. A rejected participant
should receive cited technical reasons and the smallest narrower claim the evidence might
support, without the judge rewriting the claim on the author's behalf.

Full-round breaks of modern targets may need a responsible-disclosure path before public
PRs, logs, or model-provider transmission. Decide that policy before those targets open.

## Implementation phases

### Phase 0: ratify the scientific contract

- Choose the pilot target profile, collision class, and fixed round count.
- Ratify the cost vector, scalar score, probability normalization, and minimum meaningful
  improvement.
- Ratify one baseline result and an organizer-authored proof package.
- Decide whether the pilot leaderboard is provisional or promotion requires human approval.
- Choose provider(s), model configuration, per-submission budget, and data-retention policy.
- Decide private-versus-public repository and responsible-disclosure rules.

Exit: a cryptographer signs off on target, claim schema, score, baseline, and status words.

### Phase 1: deterministic skeleton

- Create the repository structure, manifest, setup/run scripts, workflow, schemas, target,
  cost model, and candidate template.
- Implement surface, file, schema, hash, target, and arithmetic checks.
- Add concrete collision-witness checking and certificate routing.
- Produce a valid score artifact from a hard-coded organizer fixture only.

Exit: local run and GitHub Actions baseline validation agree; malformed packages never
write a score.

### Phase 2: AI review harness

- Implement provider adapter, strict output schemas, specialist prompts, aggregation, retry
  classification, provenance capture, and sanitized dossier generation.
- Ensure the secret-bearing job executes no participant code.
- Add author-facing failure summaries and separate infrastructure diagnostics.

Exit: the known-valid fixture qualifies, obvious flawed fixtures fail or request
clarification, and provider failure never looks like technical rejection.

### Phase 3: calibration and adversarial testing

- Build and human-label the mutation corpus.
- Run repeated trials across candidate judge configurations.
- Red-team prompt injection, output contradictions, oversized inputs, cost denial of
service, certificate/paper mismatch, and model drift.
- Freeze judge v1 prompts, schemas, models, budgets, and release metrics.

Exit: zero false accepts on the fatal release suite, with human-ratified operating metrics.

### Phase 4: private canary

- Install the correct Yukon GitHub App and import the private repository.
- Validate the baseline and run invited submissions.
- Exercise clarification, appeal, re-dispatch, and human-review flows.
- Confirm exact promotion behavior with Yukon before any result is called accepted.

Exit: an end-to-end candidate has a durable PR, trusted score artifact, review dossier,
human decision, and auditable status transition.

### Phase 5: production and expansion

- Publish participant guidance and status definitions.
- Open the pilot and monitor cost, latency, disagreement, appeals, and missed issues.
- Add typed certificate checkers only with soundness tests and versioned contracts.
- Add new schema-v2 tracks one stable target/profile/round combination at a time.
- Develop a separate formally verified, proof-carrying track after the canonical Lean and
cost-semantics experiment succeeds.

## Decisions still required

1. Which exact target profile and round count is the pilot?
2. Is `time × memory` the official scalar for the pilot, and how are zero/small memory,
   preprocessing, data, and success amplification handled?
3. What minimum improvement is scientifically meaningful?
4. Does Yukon currently support holding an improving PR for human approval, and who invokes
   promotion?
5. Is the Yukon leaderboard explicitly provisional, or must a human approve before a score
   becomes promotable?
6. Which model providers/configurations and data-retention terms are acceptable for
   unpublished cryptanalysis?
7. Which model outputs and dossiers are public, private to judges, or redacted?
8. What makes a concrete collision “practically executable” and therefore witness-required?
9. Which prior-art corpus is authoritative, versioned, and legally distributable to the
   judge?
10. Who can provide human sign-off, what is the conflict-of-interest rule, and what is the
    appeal SLA?
11. What is the responsible-disclosure process for a credible modern full-round break?

## Sources reviewed

- [`HashSmash.md`](./HashSmash.md), especially the scope, required submission package,
  multi-stage LLM harness, reproduction guidance, and proof-carrying notes.
- [Yukon GitHub Actions Benchmark Author Guide](https://github.com/Layr-Labs/yukon/blob/master/docs/github-actions-benchmark-author-guide.md), reviewed at commit
  `ae0ecd5650dcc394769c4c4810237647d29f078b`.
- [Yukon Overview](https://github.com/Layr-Labs/yukon/blob/master/OVERVIEW.md), reviewed at the
  same commit.
- Current public Yukon examples, including
  [Proximity Prize](https://github.com/proximity-prize/proximity-prize),
  [quantum_ecc_add](https://github.com/Layr-Labs/quantum_ecc_add), and
  [mlxfast-challenge](https://github.com/Layr-Labs/mlxfast-challenge). These informed the
  workflow, proof-checking, editable-surface, AI-gate, retry, and infrastructure-failure
  recommendations; the pinned Yukon author guide remains authoritative for platform fields.
- [Introducing Yukon](https://www.eigenlabs.org/blog/introducing-yukon/) and
  [yukon.org](https://www.yukon.org/) for the current public product framing.
- Official OpenAI documentation for the
  [Responses API](https://developers.openai.com/api/reference/resources/responses/methods/create),
  [Graders API](https://developers.openai.com/api/reference/resources/graders), and
  [current model guidance](https://developers.openai.com/api/docs/guides/latest-model).
