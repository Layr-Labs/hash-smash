# HashSmash MVP validation record

Date: 2026-09-03

## Result

The Yukon-compatible MVP passes its complete offline suite. It has interchangeable
OpenRouter and Amazon Bedrock provider backends behind the same judge, aggregation, and
score interface. Live OpenRouter calibration established that Sol can perform the full
three-stage review and that each proposed OpenRouter committee member can produce valid
structured reviews for the current public fixture. Bedrock Sol now also passes its live
smoke test and full three-stage pipeline, returning `ai_qualified` and generating the
Yukon score `179.0`. All three calls succeeded on their first attempts. The earlier
Bedrock Opus run completed its three reviews but correctly withheld a score because
triage misspelled the canonical target-profile identifier; that historical result is
retained below rather than reclassified as a pass.

The checked-in deterministic radix-sort fixture is mechanically valid and claims the
lower-is-better score `179.0` (`log2(time) = 92`, `log2(memory bytes) = 87`). This is an
organizer plumbing and calibration fixture, not a new SHA-1 attack. These results validate
the workflow contracts; they do not formally verify the proof or turn `ai_qualified` into
human acceptance.

## Offline tests

`bash .yukon/setup.sh` passes 88 credential-free tests:

- 19 deterministic verifier tests;
- 61 judge, schema, fake-provider, and committee tests; and
- 8 repository-level Yukon and pipeline tests.

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

The optional `sha1-collision-witness-v1` checker was also exercised outside the repository
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
