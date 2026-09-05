# HashSmash AI judge

This package reviews the [paired frontier lanes](../docs/JUDGE_LANES.md) through
OpenRouter Chat Completions or Amazon Bedrock Converse/Responses. Four independent
roles inspect evaluability, cryptanalysis, cost and experiments. A proposed fatal
finding triggers defender and adjudicator reviews. One evidence package produces
both lane decisions; only the selected lane can emit a score.

Exploratory qualification is `plausible_not_refuted`; rigorous qualification is
`ai_rigor_qualified`. Other outcomes include `refuted`, `not_evaluable`,
`not_qualified` and `infra_failed`. These are AI review outcomes, not mathematical
proof or human acceptance. Relevant heuristic support, explicit scope and
resource accounting are required; model confidence never replaces an obligation.

The importable high-level calls are:

```python
from judge import OpenRouterClient, OpenRouterConfig
from judge import run_paired_review, select_lane_aggregate

dossier = run_paired_review(evidence, OpenRouterClient(OpenRouterConfig.from_env()))
aggregate = select_lane_aggregate(dossier, "exploratory")

from judge import BedrockClient, BedrockConfig

bedrock_dossier = run_paired_review(evidence, BedrockClient(BedrockConfig.from_env()))
```

The runner expects a trusted evidence envelope containing the normalized claim,
line-numbered proof, selected target, cost model, nominal reference, certificate
reports and any bound experiment results. Participant content is serialized as
untrusted evidence, never inserted into system instructions. Judge calls never
execute participant code. The dossier retains review records, provider provenance,
bindings, unresolved obligations and both decisions.

## Provider backends

Set `HASHSMASH_JUDGE_PROVIDER` to `openrouter` or `bedrock`; the default is `openrouter`.
The library and pipeline do not load `.env` themselves. Local wrapper scripts load it
without printing it.

OpenRouter reads `OPENROUTER_API_KEY`, defaults to `openai/gpt-5.6-sol`, and accepts a
model override through `HASHSMASH_JUDGE_MODEL`. Zero-data-retention routing is requested
by default and may be disabled explicitly with `HASHSMASH_OPENROUTER_ZDR=false`.
Disabling it sends the complete evidence envelope under the selected endpoint's non-ZDR
retention policy and therefore requires an explicit data-handling decision.

Amazon Bedrock reads the API key from AWS's standard `AWS_BEARER_TOKEN_BEDROCK` variable
and calls the regional Bedrock Runtime Converse endpoint directly over HTTPS. It defaults
to the US inference profile `us.anthropic.claude-opus-4-6-v1` in `us-east-1`. Override
these with `HASHSMASH_BEDROCK_MODEL` and `HASHSMASH_BEDROCK_REGION`. No AWS SDK is needed.
The Bedrock request uses JSON-Schema structured output and Claude 4.6 adaptive thinking.
Unsupported wire-schema constraints are removed only from the provider request; the full
organizer-owned schema is always enforced locally on the result.

### GPT-5.6 Sol on Bedrock

Set `HASHSMASH_BEDROCK_MODEL=us.openai.gpt-5.6-sol` to select Sol with US cross-region
inference; `global.openai.gpt-5.6-sol` is also supported when global processing is
explicitly intended. The adapter automatically uses
`https://bedrock-runtime.<region>.amazonaws.com/openai/v1/responses`, with native
`reasoning.effort` (default `high`), `max_output_tokens`, and `store=false`. It never
sends Claude thinking parameters, enables tools, or changes providers on failure.
The short `openai.gpt-5.6-sol` ID belongs to the Mantle route and is rejected here.
This integration does not require an OpenAI key or any new dependency.

AWS currently lists structured outputs as unsupported for Sol on Bedrock Runtime.
The organizer-owned `prompts/bedrock-sol-json-v1.md` instructions therefore include the
stage-specific schema. The response must complete with exactly one assistant JSON
review; refusals, tool calls, truncated responses, fenced JSON, duplicate keys, schema
violations, and semantic inconsistencies fail closed. Only stage-inapplicable null/empty
fields are supplied by normalization; claims and verdicts are never repaired. Effective
prompt hashes, API route, actual returned model, request IDs, and token usage are recorded.

`store=false` disables Responses conversation storage; it is not a claim of account-wide
zero retention or disabled AWS abuse monitoring. Confirm the account's data-retention,
logging, model-access, and quota policy before accepting private participant proofs.
The IAM principal behind the existing Bedrock API key needs `bedrock:InvokeModel` on
the inference target and the default project
`arn:aws:bedrock:<region>:<account-id>:project/default`. This adapter does not change IAM.

Run the complete local pipeline for a ready, explicitly selected candidate with:

```sh
HASHSMASH_JUDGE_PROVIDER=bedrock \
HASHSMASH_BEDROCK_MODEL=us.openai.gpt-5.6-sol \
HASHSMASH_BEDROCK_REGION=us-east-1 \
bash scripts/run-local-track.sh sha256-r31-exploratory
```

The wrapper runs deterministic setup before loading `.env`. Direct pipeline calls
require credentials already configured in the trusted shell; they do not load
`.env`. See the [qualification sequence](../docs/CANDIDATE_QUALIFICATION.md) for
separate intake, review and score commands.

For GitHub Actions, the paired workflow uses repository variables
`HASHSMASH_JUDGE_PROVIDER=bedrock`, `HASHSMASH_BEDROCK_MODEL=us.openai.gpt-5.6-sol`
and `HASHSMASH_BEDROCK_REGION=us-east-1`, retaining the `AWS_BEARER_TOKEN_BEDROCK`
secret only in the review job. Each configured role independently selects its
provider API route; live qualification is not implied by a connectivity test.

Sources for the existing adapter design: [AWS Sol model card](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-56-sol.html),
[AWS Responses API](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-mantle.html),
and [OpenAI Bedrock guidance](https://developers.openai.com/api/docs/guides/amazon-bedrock).

## Prompt strategies and role committees

Both adapters use `formal-proof-v1` and high reasoning effort by default. Override
these with `HASHSMASH_JUDGE_STRATEGY` and `HASHSMASH_REASONING_EFFORT`.
The organizer-owned strategies in `judge/strategies/` are:

- `balanced-v1`: neutral review against the rubric;
- `formal-proof-v1`: theorem, lemma and dependency checking;
- `adversarial-v1`: counterexample and hidden-assumption search;
- `cost-skeptic-v1`: resource accounting and model consistency.

Set `HASHSMASH_JUDGE_MODE=committee` to configure each role independently using
`judge/committees/paired-roles-v1.json`. `HASHSMASH_ROLE_COMMITTEE_PATH` may select
another organizer configuration directly in that directory. All six roles must
be configured; credentials and provider selection cannot be overridden by a role.
The default profile applies these strategies to the configured provider/model:

| Role | Strategy |
| --- | --- |
| Evaluability | `balanced-v1` |
| Cryptanalysis | `formal-proof-v1` |
| Cost | `cost-skeptic-v1` |
| Experiments | `adversarial-v1` |
| Defender | `balanced-v1` |
| Adjudicator | `formal-proof-v1` |

Individual roles may override model, strategy, reasoning effort and output budget.
The default `single` mode uses independent calls to one client. Both modes use the
same proof obligations and adjudication rules; neither uses majority voting.
The dossier records effective models, prompt hashes and role configuration.

## Diagnostics and tests

Run deterministic tests before any live diagnostic:

```sh
bash .yukon/setup.sh
python3 scripts/hashsmash_pipeline.py intake --track sha256-r31-exploratory
```

A ready candidate and successful intake are required for these one-stage provider
diagnostics. Select the same track and a paired role explicitly:

```sh
bash scripts/run-openrouter-smoke.sh \
  --track sha256-r31-exploratory \
  --stage lane_evaluability \
  --model openai/gpt-5.6-sol \
  --strategy formal-proof-v1 \
  --reasoning-effort high \
  --max-attempts 1

bash scripts/run-bedrock-smoke.sh \
  --track sha256-r31-exploratory \
  --stage lane_evaluability \
  --model us.openai.gpt-5.6-sol \
  --region us-east-1 \
  --strategy formal-proof-v1 \
  --reasoning-effort high \
  --max-attempts 1
```

The bounded [paired calibration](../docs/FRONTIER_LANES.md#executable-heuristic-evidence)
uses organizer toy cases and preserves both policy outcomes without scoring any
challenge candidates. Use the [participant heuristic test](../docs/PARTICIPANT_HEURISTIC_TEST.md)
to exercise the isolated source-to-evidence path. These diagnostics establish
integration behavior, not cryptanalytic accuracy or qualified research baselines.
