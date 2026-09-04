# HashSmash AI judge

This package runs three independent provider reviews—triage, correctness, and
complexity—through OpenRouter Chat Completions or Amazon Bedrock Converse/Responses. It maps
their strict structured records to one of:

- `ai_qualified`
- `clarification_required`
- `technical_blocker`
- `judge_infra_failed`

`ai_qualified` is an AI screening result, not mathematical verification or human
acceptance.

Local multi-track evidence contains a selected target profile, common cost model and
an explicitly unqualified nominal reference. `prompts/local-tracks-v1.md` instructs the
reviewer not to treat that reference as a proved baseline or a premise. The active
unconditional policy still vetoes unproved cryptanalytic assumptions, including at
committee aggregation. Complexity must reconstruct the actual submitted cost vector.
See [LOCAL_TRACKS.md](../LOCAL_TRACKS.md) for per-track runners and experiment boundaries.

The importable high-level calls are:

```python
from judge import OpenRouterClient, OpenRouterConfig, run_mvp

dossier = run_mvp(evidence, OpenRouterClient(OpenRouterConfig.from_env()))
status = dossier["aggregate"]["status"]

from judge import BedrockClient, BedrockConfig

bedrock_dossier = run_mvp(evidence, BedrockClient(BedrockConfig.from_env()))
```

The runner expects a trusted JSON evidence object containing the normalized claim,
line-numbered Markdown proof, target profile, cost model, frontier, and sanitized
certificate reports. The entire object is JSON-serialized and labeled untrusted before
it is sent to the model. No participant text is placed in the system prompt.

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

Run the complete local single-panel pipeline with:

```sh
bash .yukon/setup.sh
bash scripts/run-local-bedrock.sh --model us.openai.gpt-5.6-sol --region us-east-1
```

For a one-stage smoke test, first prepare evidence with
`python3 scripts/hashsmash_pipeline.py intake`, then use `scripts/run-bedrock-smoke.sh`
with `--model us.openai.gpt-5.6-sol --reasoning-effort high --max-attempts 1`.
The full local runner accepts `--model` and `--region` after loading `.env`; the smoke
runner additionally accepts `--max-attempts`, `--max-tokens`, and `--timeout-seconds`.

For GitHub Actions, use repository variables `HASHSMASH_JUDGE_PROVIDER=bedrock`,
`HASHSMASH_BEDROCK_MODEL=us.openai.gpt-5.6-sol`, and
`HASHSMASH_BEDROCK_REGION=us-east-1`, retaining the `AWS_BEARER_TOKEN_BEDROCK` secret.
The default Claude model and existing committee profiles are unchanged. An explicitly
selected committee can mix Sol and Claude model IDs; each member independently selects
its API route. No live committee qualification is implied by a single-panel test.

Sources: [AWS Sol model card](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-56-sol.html),
[AWS Responses API](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-mantle.html),
and [OpenAI Bedrock guidance](https://developers.openai.com/api/docs/guides/amazon-bedrock).

Both backends use `formal-proof-v1` and high reasoning effort by default. Override them
with `HASHSMASH_JUDGE_STRATEGY` and `HASHSMASH_REASONING_EFFORT`.

```sh
python3 -m judge \
  --provider bedrock \
  --evidence build/judge-evidence.json \
  --output build/judge-dossier.json
```

Exit status is 0 only for `ai_qualified`, 2 for a clarification or technical blocker,
and 3 for judge infrastructure failure. Provider errors never become proof verdicts.

## Prompt strategies

Strategies are organizer-owned overlays in `judge/strategies/`. Four versioned options
are checked in:

- `balanced-v1`: neutral review against the common rubric;
- `formal-proof-v1`: theorem/lemma and dependency-oriented checking;
- `adversarial-v1`: active counterexample and hidden-assumption search; and
- `cost-skeptic-v1`: resource accounting and model-consistency scrutiny.

The strategy name and prompt hashes are retained in judge provenance. Participant text is
always serialized in the untrusted user evidence envelope and never interpolated into a
system prompt.

## Judge committees

Set `HASHSMASH_JUDGE_MODE=committee` to run a committee. The optional
`HASHSMASH_COMMITTEE_PATH` selects a strict JSON configuration. The OpenRouter production
profile is `judge/committees/committee-v1.json`:

| Member | Model | Strategy | Reasoning |
| --- | --- | --- | --- |
| `sol-formal` | `openai/gpt-5.6-sol` | `formal-proof-v1` | high |
| `opus-adversarial` | `anthropic/claude-opus-4.6` | `adversarial-v1` | high |
| `gemini-cost` | `google/gemini-2.5-flash` | `cost-skeptic-v1` | provider default |

Members run concurrently, but each member's triage, correctness, and complexity reviews
remain sequential. Members receive only the trusted evidence envelope, not other judges'
reviews. The v1 policy requires all three members to complete and qualify the same claim;
any technical blocker or clarification is a veto. Infrastructure failures cannot become a
proof verdict or score.

For local calibration, `bash scripts/run-local-committee.sh` selects
`committee-calibration-v1.json`, which uses one attempt per stage to bound cost and time.
With `HASHSMASH_JUDGE_PROVIDER=bedrock`, the same script selects
`committee-bedrock-calibration-v1.json`: three Opus 4.6 panels with formal-proof,
adversarial, and cost-skeptic prompts. Its retry-enabled production counterpart is
`committee-bedrock-v1.json`. The ordinary local runners remain single-model so committee
use is always explicit.

For a one-stage connectivity and schema smoke test after deterministic setup:

```sh
bash scripts/run-openrouter-smoke.sh \
  --stage triage \
  --model openai/gpt-5.6-sol \
  --strategy formal-proof-v1 \
  --reasoning-effort high \
  --max-attempts 1
```

The equivalent Bedrock smoke test is:

```sh
bash scripts/run-bedrock-smoke.sh \
  --stage triage \
  --model us.anthropic.claude-opus-4-6-v1 \
  --region us-east-1 \
  --strategy formal-proof-v1 \
  --reasoning-effort high \
  --max-attempts 1
```

Run the fake-transport unit suite without credentials or network access:

```sh
python3 -m unittest discover -s judge/tests -v
```
