# HashSmash MVP validation record

Date: 2026-09-03

## Result

The Yukon-compatible MVP passes its complete offline suite. It has interchangeable
OpenRouter and Amazon Bedrock provider backends behind the same judge, aggregation, and
score interface. Live OpenRouter calibration established that Sol can perform the full
three-stage review and that each proposed OpenRouter committee member can produce valid
structured reviews for the current public fixture. Bedrock is fully tested with fake HTTP
transports but has not been exercised live because no `AWS_BEARER_TOKEN_BEDROCK` is present
in the local `.env`.

The checked-in deterministic radix-sort fixture is mechanically valid and claims the
lower-is-better score `179.0` (`log2(time) = 92`, `log2(memory bytes) = 87`). This is an
organizer plumbing and calibration fixture, not a new SHA-1 attack. These results validate
the workflow contracts; they do not formally verify the proof or turn `ai_qualified` into
human acceptance.

## Offline tests

`bash .yukon/setup.sh` passes 70 credential-free tests:

- 19 deterministic verifier tests;
- 45 judge, schema, fake-provider, and committee tests; and
- 6 repository-level Yukon and pipeline tests.

The verifier tests cover closed schemas, filesystem and size restrictions, line-numbered
proof intake, optional certificate checking, and the exact AI-qualification score gate.
The judge tests cover prompt isolation, versioned strategies, stage-specific schemas,
malformed responses, bounded provider retries, semantic invariants, canonical claim
aggregation, committee unanimity and veto rules, independent panel execution, and
infrastructure-failure handling. Bedrock coverage additionally checks bearer
authentication, regional endpoint construction, Converse request and response shapes,
wire-schema adaptation, adaptive reasoning configuration, retry behavior, bounded error
reporting, provider selection, and a complete mocked three-stage aggregation.

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

The next live check is deliberately only a one-stage smoke test:

```sh
bash scripts/run-bedrock-smoke.sh --stage triage --max-attempts 1
```

It is blocked only on adding a valid `AWS_BEARER_TOKEN_BEDROCK` to `.env` and having model
access in the configured AWS region.

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
- Select the production provider. For OpenRouter, enable a ZDR-compatible route; for
  Bedrock, complete the live smoke/panel calibration and confirm model access, region, data
  governance, quotas, and cost.
- Configure only the selected GitHub Actions provider secret and repository permissions.
- Complete the combined post-fix committee run and retain its calibration dossier.
- Create the GitHub repository, install the Yukon dev GitHub App, obtain an allowlisted dev
  importer API key, and run a non-ranking canary submission.

The Yukon integration follows the
[GitHub Actions benchmark author guide](https://github.com/Layr-Labs/yukon/blob/master/docs/github-actions-benchmark-author-guide.md)
and [Yukon overview](https://github.com/Layr-Labs/yukon/blob/master/OVERVIEW.md).
