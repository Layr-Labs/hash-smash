# Direct OpenAI judge

The opt-in `openai` provider uses the standard library to call
`https://api.openai.com/v1/responses`. It requires `OPENAI_API_KEY` and an explicit
`HASHSMASH_OPENAI_MODEL`. The reviewed model contract is `gpt-5.6-sol`, with
`HASHSMASH_REASONING_EFFORT=high`; there is no implicit model migration or provider
fallback. Other explicit model IDs require organizer verification of the same
Responses, schema and reasoning capabilities. Returned model IDs must exactly
match the configured ID.

## Operator selection

For the reusable paired workflow, separately provision the Actions secret
`OPENAI_API_KEY` and repository variables `HASHSMASH_JUDGE_PROVIDER=openai` and
`HASHSMASH_OPENAI_MODEL=gpt-5.6-sol`. This source change does not set them.
The workflow selects committee mode and high reasoning. Only the selected judge
step receives its provider secret. Intake/experiments and score jobs receive none
of the three provider keys. Every literal caller forwards the optional secret.

An absent provider setting retains OpenRouter; explicit `bedrock` retains Bedrock.
Unknown providers fail before any provider step. Do not put an OpenAI key in
`OPENROUTER_API_KEY` or `AWS_BEARER_TOKEN_BEDROCK`.

The library and pipeline read environment variables, never dotenv files. Run
credential-free setup and intake separately, following the existing
[qualification sequence](CANDIDATE_QUALIFICATION.md), before credentialed review.
The judge handles participant files as inert evidence and never executes them.
The participant diagnostic preparation wrapper scrubs `OPENAI_API_KEY` along with
existing provider/cloud credentials. Both organizer diagnostic CLIs accept
`--provider openai`; their `--model` override is rejected for OpenAI so the required
`HASHSMASH_OPENAI_MODEL` remains explicit. Existing-provider overrides are unchanged.

## Request, validation and provenance

The adapter sends `store:false`, no tools, no temperature, and
`text.format={type:json_schema,name,strict:true,schema}`. All seven stage schemas
have an object root, `additionalProperties:false` and every property required.
Only optional, ignored `cost_reconstruction.data_log2` is removed from the OpenAI
wire schema. Constraints such as `minLength`, `minimum` and array bounds remain.
The full original local schema, evidence/context and heuristic coverage checks
remain authoritative. The harness supplies only existing bookkeeping fields.

Only one completed assistant JSON review is accepted. Refusals, incomplete or
error responses, tool output, ambiguous messages, wrong model IDs, missing IDs,
duplicate JSON keys and nonfinite values fail closed. HTTP redirects are refused
before a key can be forwarded. Keys containing whitespace, controls or non-ASCII
characters fail locally with a fixed message that does not echo the key.

Provenance records the actual request and response model, API route, bounded
redacted response/request IDs, allowlisted numeric token usage, source fingerprint,
wire-schema hash, base contract hash and the successful attempt's instructions and
request-body hashes. Per-attempt hashes include trusted validation-repair feedback.
Committee/configuration fingerprints bind each effective role prompt and schema.
No reasoning content, raw HTTP body, headers or arbitrary transport exceptions are
recorded in diagnostics. HTTP error fields are allowlisted, redacted and bounded;
error envelopes larger than 64 KiB supply no body fields.

## Finite budgets and testing limits

Defaults are 32,768 output tokens, high reasoning, a 300-second request timeout
and three total attempts per role. Config validation caps output at 128,000,
timeout at 300 seconds and attempts at three. Transport failures and HTTP
408/429/5xx retry with 60/120-second backoff and bounded jitter. Numeric/date
`Retry-After` hints are capped at 120 seconds. Invalid JSON/reviews use short
0.5/8-second backoff. All failure types share one attempt budget; terminal attempts
do not sleep. Valid negative verdicts do not trigger a retry. An exhausted required
role makes both lanes `infra_failed`; the existing score gate withholds output.

The committee still calls four initial roles serially and may call defender and
adjudicator. These request limits do not guarantee that worst-case retries finish
within the workflow's 60-minute job limit, or establish provider throughput.
`store:false` disables response application storage; it does not establish
account-wide zero retention or disable abuse monitoring.

Run `bash .yukon/setup.sh` and `python3 scripts/validate_frontier_config.py` before
an independently authorized live test. The direct adapter, pipeline and workflow
tests use organizer fixtures and fake transports. A live connectivity fixture is
not a qualified candidate, benchmark, capacity measurement or score. No SDK is
required. Existing provider request bytes, prompt/config fingerprints, scoring
policy and historical dossier verification are preserved by this opt-in addition.

Official API contract reviewed on 2026-10-05:
[Sol model](https://developers.openai.com/api/docs/models/gpt-5.6-sol),
[Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs),
[Responses](https://developers.openai.com/api/reference/resources/responses/methods/create),
[data controls](https://developers.openai.com/api/docs/guides/your-data).
