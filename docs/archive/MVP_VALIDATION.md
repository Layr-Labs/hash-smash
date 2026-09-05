# HashSmash MVP validation record

> Historical record: the legacy SHA-1 pilot and nine local tracks described here
> have been retired. Commands, paths, test counts and deployment plans below
> describe that earlier system. Use the [current documentation](../README.md)
> and [paired-lane guide](../FRONTIER_LANES.md) for supported workflows.

Date: 2026-09-03

## Result

At the recorded revision, the repository included nine local MD5/SHA-1/SHA-256
tracks and passed 136 offline tests. The now-retired `LOCAL_TRACKS.md` guide
documented that workflow. Each new track started with
an unsubmitted draft and a nominal reference, not a qualified baseline. No new live
provider reviews, overnight agents, pushes, or deployments were performed for this setup.

The pilot enforces `unconditional-v1`: no additional
unproved cryptanalytic assumptions are admitted. The earlier policy ambiguity is
resolved; the heuristic organizer candidate must not qualify. Historical mixed results
are retained below, not promoted under the new policy. A distribution-free probability
argument for a randomized replacement has been derived and tested with exact arithmetic;
the replacement algorithm and resource ledger remain to be implemented.

The MVP has interchangeable OpenRouter and Amazon Bedrock provider backends behind the
same judge, aggregation, and score interface. Earlier live provider successes and
failures are retained below as historical results, not substituted for the latest batch.

The checked-in deterministic radix-sort fixture remains mechanically valid and claims
score `179.0`, but its unproved heuristic makes it a negative calibration fixture under
the active policy, not an admissible baseline. This distinction matters for Yukon import,
which requires a qualifying baseline. No mathematical or human acceptance is claimed.

## Offline tests

`bash .yukon/setup.sh` passes 136 credential-free tests:

- 19 deterministic verifier tests;
- 68 judge, schema, fake-provider, policy, and committee tests;
- 8 repository-level Yukon and pipeline tests;
- 21 organizer baseline instruction, sorting, resource, and probability tests; and
- 20 local-track, reference-hash, witness, isolation, history, and integration tests.

The verifier tests cover closed schemas, filesystem and size restrictions, line-numbered
proof intake, optional certificate checking, and the exact AI-qualification score gate.
The judge tests cover prompt isolation, versioned strategies, stage-specific schemas,
malformed responses, bounded provider retries, semantic invariants, canonical claim
aggregation, committee unanimity and veto rules, independent panel execution, and
infrastructure-failure handling. Bedrock coverage additionally checks bearer
authentication, regional endpoint construction, Converse request and response shapes,
wire-schema adaptation, adaptive reasoning configuration, retry behavior, bounded error
reporting, provider selection, and a complete mocked three-stage aggregation.
Sol coverage adds Responses request/response handling, prompt-supplied schemas, refusal
and truncation rejection, strict JSON parsing, returned-model checks, no stored
conversation state, effective prompt hashing, removal of stale scores after failure,
and an independent mixed Sol/Claude committee with three prompting strategies.

### Nine-track local setup validation

The new registry selects MD5 at 8/24/64 steps, SHA-1 at 8/40/80 rounds, and SHA-256 at
8/24/64 rounds. Exact profile definitions retain standard full-message padding, IV,
feed-forward and output width, reducing every compression block to its prefix steps.
The shared local v2 cost model standardizes 256-bit machine words and charged random
coins. Existing legacy target/model/candidate/workflow semantics were not migrated.

Validation includes:

- Full reference hashes agree with independent `hashlib` implementations on 15 message
  lengths per function, including one/two-block padding boundaries.
- Reduced SHA-1 (8/40) and SHA-256 (8/24) agree with published NIST intermediate-state
  examples plus the defined feed-forward. Reduced MD5 (8/24) agrees with an independent
  direct-register implementation of RFC 1321's update order.
- Small full-message collision fixtures verify on each 8-step/round control, including
  multi-block inputs, but not on the corresponding full-round target. Witness relabeling,
  identical messages, wrong digests, incorrect round counts and cross-track claims fail.
- Every track completes intake, three-stage **fake Bedrock transport**, aggregation and
  score construction in temporary test directories. This validates plumbing only; the
  mock provider's deliberate positive votes do not qualify any real submission.
- Drafts cannot reach the provider or emit a score. Nominal references cannot substitute
  for a review. Submitted cost reconstruction must match deterministic intake.
- Concurrent track intakes have isolated state; per-track CLI locks reject overlapping
  same-track runs. Archives contain only enumerated generated files, preserving failed
  runs without copying credentials. Stale input/configuration scores fail closed.
- Historical status excludes failed or wrong-configuration scores and distinguishes an
  old best AI-reviewed candidate from the current input. Tests use organizer-owned
  temporary fixtures so solver edits do not invalidate the deterministic suite.
- Credential-free `local_tracks.py check` validates all nine real draft folders, and
  `status` reports no AI-reviewed result or qualified baseline for any new track.

The nominal scalars 128/160/256 are coarse output-width-derived starting references, not
measured security, established birthday-attack ledgers or hidden approved assumptions.
No score artifact was installed for a draft, and no full attack was attempted. Live
positive/negative judge calibration on actual future submissions remains experiment work.

The optional legacy `sha1-collision-witness-v1` checker was also exercised outside the repository
against the published SHAttered PDF pair. It accepted the distinct files with their common
SHA-1 digest. The files were temporary and are not included here.

## Live OpenRouter calibration

The original Gemini-only pipeline was exercised end to end before the fixture was
strengthened. It returned `ai_qualified`, created the Yukon score artifact, and confirmed
that the secret-bearing job, strict schemas, trusted aggregation, and score gate work
together.

After switching the default to `openai/gpt-5.6-sol`, a full Sol review was run against the
current fixture. Sol first identified real weaknesses in the generic baseline: unsupported
constant factors, memory accounting at the exact bound, a 64-bit address-space mismatch,
and ambiguous restrictions. The fixture and cost model were made explicit rather than
loosening the judge. With an abstract 128-bit word-RAM model, explicit array allocation,
radix-sort operation counts, and canonical restriction aggregation, Sol's triage passed
and both substantive reviews returned `supported`; trusted aggregation returned
`ai_qualified`.

Committee calibration then exercised the three intended perspectives:

| Member | Observed result on the current fixture |
| --- | --- |
| Sol / formal proof | Full three-stage panel `ai_qualified` |
| Opus / adversarial | Triage passed; correctness and complexity supported |
| Gemini / cost skeptic | Full three-stage panel `ai_qualified` in the first bounded committee run |

The first bounded committee run exposed an ambiguous counterexample-result convention and
an 8K output cap that truncated Opus's complexity review. The common rubric now explicitly
defines `refuted`, `survives`, and `inconclusive`, rejects positive verdicts paired with a
surviving fatal counterexample, and gives Opus 16K output tokens. Isolated Opus retests of
all three stages then passed on their first attempts.

The final post-fix combined run was interrupted before producing a dossier. A subsequent
retry from the restricted local runner correctly failed as infrastructure-only before any
model responded. Retrying outside the network sandbox with Zero Data Retention disabled
was not authorized because it would change the retention policy for the complete proof
evidence. No combined committee qualification is claimed yet.

## Zero Data Retention check

A production-safe one-stage smoke request used:

```sh
HASHSMASH_OPENROUTER_ZDR=true bash scripts/run-openrouter-smoke.sh \
  --stage triage \
  --model openai/gpt-5.6-sol \
  --strategy formal-proof-v1 \
  --reasoning-effort high \
  --max-tokens 2048 \
  --max-attempts 1
```

OpenRouter returned a non-retryable HTTP 404 before inference: `No endpoints found
matching your data policy (Zero data retention)`. This is recorded as
`judge_infra_failed`, never as a proof failure. The workflow still sets ZDR to true and
therefore fails closed until the OpenRouter account privacy or routing configuration
provides an eligible Sol endpoint. A non-ZDR run is technically known to work, but must
not be used for participant submissions without an explicit retention decision.

Generated dossiers retain requested and returned model IDs, usage, latency, bounded
routing metadata, prompt and schema hashes, and a dossier hash. The API key is removed from
every configuration snapshot.

## Amazon Bedrock backend

The Bedrock backend uses only Python's standard library and calls:

```text
POST https://bedrock-runtime.{region}.amazonaws.com/model/{model-id}/converse
Authorization: Bearer ${AWS_BEARER_TOKEN_BEDROCK}
```

It defaults to `us.anthropic.claude-opus-4-6-v1`, high-effort adaptive thinking, and the
same strict stage schemas and local semantic validation used for OpenRouter. The request
uses Bedrock's `outputConfig.textFormat` JSON-Schema mode. Constraints unsupported by
Bedrock's wire-schema subset are omitted from the request but retained in the authoritative
local schema, so provider acceptance never weakens the score gate.

The GitHub Actions judge job selects Bedrock when repository variable
`HASHSMASH_JUDGE_PROVIDER` equals `bedrock`. OpenRouter and Bedrock are separate conditional
steps, so only the chosen provider secret is exposed. Bedrock committee profiles run Opus
4.6 independently with formal-proof, adversarial, and cost-skeptic strategies.

The live smoke test succeeded on its first attempt:

```sh
bash scripts/run-bedrock-smoke.sh --stage triage --max-attempts 1
```

It returned a schema-valid `pass_to_review`. The subsequent full local run used
`bash scripts/run-local-bedrock.sh` with the checked-in fixture, the US Opus 4.6 inference
profile, `us-east-1`, formal-proof prompting, and high reasoning effort:

| Stage | Result | Attempts | Client latency | Total tokens |
| --- | --- | ---: | ---: | ---: |
| Triage | `pass_to_review` | 1 | 58.2 s | 9,507 |
| Correctness | `supported` | 1 | 144.3 s | 13,809 |
| Complexity | `supported` | 1 | 234.4 s | 19,841 |

The full panel consumed 43,157 reported tokens and approximately 7 minutes 17 seconds of
client request time. These figures exclude the separate smoke call. There were no provider,
authentication, schema, truncation, or retry failures in the full panel, and all recorded
issues were minor.

The triage review transcribed the target as `sha1-fip180-4-v1`, omitting the `s` in
`sha1-fips180-4-v1`. The other reviews and deterministic intake used the correct identifier.
Aggregation therefore returned `clarification_required`, and `.yukon/score.json` was not
created. The response was not silently corrected and the proof was not changed to obtain a
pass. This is a judge-output reliability issue to address during calibration, not a
Bedrock access or transport blocker.

The complexity reviewer proposed tighter resource bounds, but they were not promoted to a
score. The original claim remains time exponent 92, memory exponent 87, and score 179.
The complete validated reviews, AWS request IDs, token usage, and timing remain in ignored
local artifacts under `.yukon/reports/`. A post-run credential scan found no configured API
key outside `.env`.

The initial sandbox-only request failed before reaching AWS. It also exposed a misleading
OpenRouter-specific label in the shared HTTP transport; that label is now provider-neutral
and covered by a credential-redaction regression test.

## Live Bedrock Sol integration

After the deterministic suite passed, the one-stage smoke used
`us.openai.gpt-5.6-sol`, `us-east-1`, formal-proof prompting, high reasoning, and one
attempt. It returned a locally schema-valid `pass_to_review` on its first attempt.
The complete local pipeline then ran with:

```sh
bash scripts/run-local-bedrock.sh --model us.openai.gpt-5.6-sol --region us-east-1
```

| Stage | Result | Attempts | Client latency | Total tokens |
| --- | --- | ---: | ---: | ---: |
| Triage | `pass_to_review` | 1 | 47.1 s | 9,476 |
| Correctness | `supported` | 1 | 42.1 s | 8,281 |
| Complexity | `supported` | 1 | 99.6 s | 13,859 |

The panel used 31,616 reported tokens (15,220 input, 16,396 output) and approximately
3 minutes 9 seconds of client request time, excluding the separate smoke call. The
actual returned model was `us.openai.gpt-5.6-sol` in all three stages. There were no
retries, infrastructure failures, refusals, truncations, or local validation failures.
Triage recorded two minor evidence/accounting notes; both specialists reported no issues.

The adapter uses Bedrock Runtime's Responses API with `store=false`, no tools, and a
versioned prompt-supplied schema. AWS does not advertise constrained structured outputs
for this route; local JSON/schema/semantic checks remain mandatory. No claim identifiers,
proof text, substantive verdicts, or score-gate rules were altered to obtain this result.

Aggregation returned `ai_qualified`, and `.yukon/score.json` was emitted with the original
submitted score **179.0**. The reviewer's tighter estimated resource bounds were recorded
but did not replace the submitted score. This remains an explicitly heuristic generic
birthday-search calibration fixture, not a novel attack or mathematically verified proof.

The validated dossier is `.yukon/reports/judge-dossier.json`; the earlier Opus dossier was
preserved in an ignored `previous-run.*` subdirectory before regenerating the standard
outputs. This test used the local key only. No GitHub variables, secrets, deployments,
workflow defaults, or existing committee profiles were changed. The mixed Sol/Claude
committee was tested with mocked provider calls, not as a live committee calibration.

## Baseline accounting revision after GitHub Actions

The first GitHub Actions run on commit `baa8740` completed intake and all three
Bedrock Sol calls, but returned `clarification_required`: triage passed and correctness
was supported, while complexity was unclear. This differed from the earlier local pass
on identical evidence and effective judge configuration. The run was a substantive
review disagreement, not a development-setup failure:
[Actions run 33807847289](https://github.com/Layr-Labs/hash-smash/actions/runs/33807847289).
Its complete intake/review artifacts remain under
`.yukon/reports/github-actions-33807847289/`.

The complexity objections were actionable: informal per-record operation ceilings and
an unitemized fixed-memory allowance. The organizer baseline now contains a complete
149-instruction word-RAM program, exact loop/setup counts, explicit rehash/output costs,
and a fixed-memory layout that charges every reserved byte. Its bounds are
`716n + 77352` time units and `64n + 65536` bytes, for `n = 2^80`. The submitted
time exponent 92, memory exponent 87, probability 0.39, and score 179 are unchanged.
The target, cost model, prompts, provider implementation, schemas, workflow, aggregation,
and score gates were not modified.

The proof also specifies the 22-byte domain prefix, 34-byte messages, all 20 LSD radix
positions, stable-scatter invariants, finite-n rational probability inequality, data
units, output interface, and absence of required numerical certificates. It remains
explicitly conditional on the SHA-1 random-function heuristic.

The trusted small-n interpreter in `calibration/birthday_wordram.py` runs only its
organizer-owned literal program. A read-only comparison confirmed that the revised
proof documents exactly that program. Offline tests check real SHA-1 record encoding,
every digest-byte sorting position, stable permutations, forced synthetic collisions,
reverification failure, exact operation counts, fixed-state/address bounds, and the
probability threshold using exact rational arithmetic. The full-size checks are symbolic;
the interpreter refuses more than 4096 records. Synthetic digests are testing fixtures,
not certificates. The tests neither execute candidate input nor require future
participant submissions to retain this organizer proof.

Before any revised live calls, all 102 deterministic tests passed. Repeatability testing
uses three predeclared independent Sol panels on one unchanged evidence package, with
one attempt per stage, high reasoning, `formal-proof-v1`, `us-east-1`, and the existing
strict acceptance rules. Each panel's dossier and score (only if qualified) are retained
separately; the test is not a retry-until-pass loop. Historical standard outputs were
preserved in `.yukon/reports/before-wordram-gz4ohde0/`.

The first revised batch returned `ai_qualified`, `clarification_required`, and
`ai_qualified`, with score 179 for each qualified trial. All six substantive specialists
returned `supported`. In trial 2, triage identified an ambiguity in the full-word result
of the SHA instruction: the digest suffix was described as occupying the low 32 bits,
without explicitly defining the upper 96 bits. That matters when rehash results are
compared as full words. The trusted reference already zero-extended this value; the
proof now specifies that behavior explicitly for every SHA result, and a fifteenth
baseline test pins it. No instruction or resource count changed. Trial 2's complexity
review also labeled the already-disclosed random-function assumption as material despite
returning `supported`; this separate rubric inconsistency was not suppressed or
reclassified. All first-batch results and their original evidence are preserved in
`.yukon/reports/baseline-wordram-1x_hfq70/`.

After the zero-extension clarification, all **103** offline tests passed. A final,
predeclared three-panel batch ran concurrently with independent clients, identical
evidence and configuration, and no cross-reviewer context. No further revision or
retry-until-pass was performed. All triages returned `pass_to_review`, and all six
correctness/complexity reviews returned `supported`:

| Final trial | Aggregate | Score emitted | Reported tokens | Summed request time |
| --- | --- | ---: | ---: | ---: |
| 1 | `clarification_required` | No | 47,165 | 261.670 s |
| 2 | `ai_qualified` | 179.0 | 50,494 | 339.196 s |
| 3 | `clarification_required` | No | 48,520 | 276.142 s |

All nine calls succeeded on their first attempts with the requested/returned model
`us.openai.gpt-5.6-sol`, no infrastructure or schema failures, and 146,179 total reported
tokens. Request times are summed client latencies, not the concurrent batch's wall time.
Trial 1's triage and complexity reviewers, and trial 3's complexity reviewer, classified
the explicitly declared random-function assumption as material. Trial 2 did not. Those
material flags correctly vetoed qualification despite the positive specialist verdicts.
There were no material instruction-semantics or resource-accounting objections in the
final batch. Minor comments about deliberately loose resource bounds were not promoted
to lower scores.

Final evidence package SHA-256:
`5f2a884a71af7d66a8c89a70584b3b0dfad4be4eeb0f5fba6d2a5d196f4e2454`.
Both batches used judge configuration SHA-256
`dcd9cc120d73d266f45cec749337be80563291f9e1aa10fcf5b82e29a43c8d2d`.
The final evidence, all dossiers, and summary are under
`.yukon/reports/baseline-wordram-zeroextended-yr893j86/`.
All six panels were independently revalidated, reaggregated, and checked against their
configuration/dossier hashes and score-presence rules after completion. The standard
report paths now reflect final trial 3, not the selected passing trial; consequently
`.yukon/score.json` remains absent. The passing trial's score is retained in its own
directory. No `.env` content or API key was included in changed files or generated
artifacts. These revisions and tests are local; they have not been pushed or rerun in
GitHub Actions or a Yukon dev deployment.

**Historical decision point (resolved by the policy update below):** explicitly decide whether
this particular random-function heuristic is an allowed, disclosed condition for
`ai_qualified`, or require a baseline that does not depend on it. Merely declaring an
arbitrary assumption must not exempt a participant from review. The current proof cannot
establish that concrete SHA-1 satisfies the heuristic, and this revision does not claim
otherwise. Any approved-assumption policy should be organizer-owned, narrowly scoped,
versioned, and tested with disallowed-assumption negative controls before changing the
judge rubric. Broad multi-model/strategy committee calibration is still outstanding.

## Unconditional policy and multi-track follow-up

The user chose not to admit conditional cryptanalytic results. The active versioned
policy is `judge/policies/unconditional-v1.md`, loaded into the trusted prompt for every
stage and strategy and hashed in the judge configuration. It excludes unproved premises
about the target, while distinguishing common problem definitions, proved lemmas, and
explicit algorithmic randomness. A nonempty `assumptions` array now blocks qualification
deterministically; an explicit `unproved_assumption` issue also blocks even if mislabeled
minor. The committee also applies a mandatory premise veto even with relaxed voting
thresholds, including a valid premise finding from a partially failed panel. The schema's
array shape is unchanged, but the versioned policy narrows its meaning
to unresolved premises. This is an intentional tightening, not a waiver for the baseline.

Seven new policy regression tests cover those gates, trusted-policy placement, all
strategies/stages, evidence injection isolation, and effective policy hashing. Six new
mathematical tests cover finite output distributions, exhaustive toy input sampling,
repeated-input false collisions, and exact rational bounds. All 115 then-current tests
passed before live validation; the final suite of 116 passed after the additional committee
veto regression. The strict rule still depends on AI review to detect missing premises;
it is not a formal proof checker and needs continued positive/negative calibration.

### Live negative control

The existing heuristic fixture was reviewed with Bedrock `us.openai.gpt-5.6-sol`,
`us-east-1`, high reasoning, and `formal-proof-v1`, under the new trusted policy.
Triage returned `clarification_needed` and correctness returned `unclear`; both identified
the same single required, unproved uniform/independent-output premise. Complexity's first
call ended with `ConnectionResetError`, so that original panel correctly remains
`judge_infra_failed`. No score was emitted.

Exactly one isolated complexity retry completed successfully, returning `unclear` and
the same unproved premise. It took 82,495 ms and used 10,342 input plus 7,462 output tokens
(17,804 total). This is not a fresh full-panel pass or a replacement of the failed panel.
All three completed stage reviews identified the intended negative control; this narrow
test does not establish false-positive/false-negative rates or qualify a new baseline.

Ignored local artifacts are retained separately:

- Original: `.yukon/reports/unconditional-policy-negative-z_4sjzw0/judge-dossier.json`.
- Evidence: `.yukon/reports/unconditional-policy-negative-z_4sjzw0/judge-evidence.json`.
- Retry: `.yukon/reports/unconditional-policy-negative-z_4sjzw0/complexity-retry.json`.
- Original configuration SHA-256:
  `60e1e2fb05bde643638eeb7cf51afedd3e2a736c6b5bcd374a7d2e7adc029548`.
- Original dossier SHA-256:
  `2254c2a02b50791af2d719fdc4f3a7fcc17e866395acc2a94ee7fb0dd257ae8c`.

### Replacement baseline and track plan

`docs/archive/UNCONDITIONAL_BASELINE.md` proves a conservative probability lower bound for iid
sampling of 192-bit nonces against any fixed 160-bit-output function. It subtracts
duplicate-input probability explicitly and exceeds 0.39 at `2^80` draws without a
random-oracle assumption. It is a proposed replacement, not a changed candidate or a
new score: common random-bit accounting, three-word records, and the instruction ledger
must still be implemented and validated.

`docs/archive/YUKON_MULTITRACK_PLAN.md` records verified schema-v2 support at Yukon commit
`d9471fe70a431a3c424758c3eb58d51d38e73d67`, including the 20-track limit, disjoint editable
paths, shared branch, and lack of track inputs in workflow dispatch. The active manifest
remains v1, and no actual dev deployment was inspected or changed. Native promotion is
scalar; storing a cost vector in metrics does not implement Pareto dominance.

## Certificate conclusion

Numerical certificates should remain optional for the proof-first v1 challenge. A
submission's central claim is a complexity and correctness argument about a potentially
infeasible attack; no generally useful executable certificate can prove that argument.
Requiring a concrete full SHA-1 collision would also exclude legitimate theoretical
improvements that cannot be run at benchmark scale.

The MVP therefore requires a strict numerical claim record and accepts optional, typed
certificates when they establish a narrow lemma. The first supported type checks a concrete
ordinary SHA-1 collision witness. Such a witness strengthens a submission but cannot prove
its method, complexity accounting, success probability, or novelty. Future tracks may add
deterministic checkers for reduced-round traces, SAT or SMT witnesses, or experiment tables
when a proposed proof makes those artifacts meaningful.

## Fail-closed behavior observed

Live attempts revealed several integration conditions and rejected them as judge
infrastructure failures rather than proof failures:

- network access unavailable inside the local sandbox;
- no ZDR-eligible Sol endpoint under the current OpenRouter account policy;
- a model filling stage-inapplicable fields despite textual null instructions; and
- a completion reaching its output-token limit.

These led to stage-specific provider schemas that structurally omit irrelevant fields,
trusted normalization and full local validation, bounded retries, explicit counterexample
semantics, and model-specific committee budgets. Conservative resource upper bounds and
success-probability lower bounds are handled explicitly.

## Remaining production gates

- Implement the unconditional randomized baseline, standardize its random-bit accounting,
  and repeat qualification calibration under `unconditional-v1`.
- Ratify the target profile, cost model, generic frontier, and public calibration fixture
  with a cryptographer.
- Decide how an improving AI-qualified entry is held for mandatory human review.
- Calibrate false-positive and false-negative rates on known-good, flawed, ambiguous, and
  prompt-injection fixtures before opening the challenge.
- Select the production provider/model. For OpenRouter, enable a ZDR-compatible route;
  for Bedrock, broaden Sol/Opus panel calibration and confirm production region, data
  governance, quotas, and cost. One Sol fixture pass is not a reliability measurement.
- Configure only the selected GitHub Actions provider secret and repository permissions.
- Complete the combined post-fix committee run and retain its calibration dossier.
- Grant the Yukon dev GitHub App access to the existing repository, obtain an allowlisted
  dev importer API key, and run a non-ranking canary submission.

The Yukon integration follows the
[GitHub Actions benchmark author guide](https://github.com/Layr-Labs/yukon/blob/master/docs/github-actions-benchmark-author-guide.md)
and [Yukon overview](https://github.com/Layr-Labs/yukon/blob/master/OVERVIEW.md).
