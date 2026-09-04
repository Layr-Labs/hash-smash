# HashSmash Yukon MVP

This repository is an initial Yukon-compatible benchmark for AI-assisted review of
Markdown cryptanalytic proofs. The current setup has **16 runnable paired lanes**:
exploratory and rigorous review for two settings each of MD5, SHA-1, SHA-256 and
SHA3-256. Twelve additional slots are reserved for BLAKE3, Keccak[800] and Poseidon,
whose exact frontier definitions remain open. Start with [FRONTIER_LANES.md](./FRONTIER_LANES.md)
for the roster, commands, two Yukon leaf manifests and deployment gates.
[JUDGE_LANES.md](./JUDGE_LANES.md) defines the shared review dossier and lane policies;
[HEURISTIC_EXPERIMENTS.md](./HEURISTIC_EXPERIMENTS.md) defines isolated executable evidence.
No qualified baselines, new deployments, or overnight workers are created by this setup.

The previous nine local tracks remain available with `--collection legacy`;
[LOCAL_TRACKS.md](./LOCAL_TRACKS.md) documents their unchanged policy and score conventions.
The sections below describe the legacy pilot unless stated otherwise.

The existing Yukon manifest and GitHub deployment remain the legacy pilot:

- target: full-round SHA-1 (`sha1-fips180-4-v1`);
- attack class: ordinary collisions;
- rounds: 80; and
- score: `log2(time in SHA-1 compressions) + log2(peak memory bytes)`, lower is better.

The MVP is deliberately conservative. Deterministic code validates the submission and
optional concrete collision witnesses. Independent provider calls review scope,
correctness, and complexity. OpenRouter and Amazon Bedrock are supported through the same
validated review interface. OpenRouter defaults to `openai/gpt-5.6-sol`; Bedrock defaults
to Claude Opus 4.6. Both use the `formal-proof-v1` strategy and high reasoning effort. An
optional committee can run several models or prompting strategies without sharing one
member's output with another. Trusted aggregation may label a submission `ai_qualified`;
that label is not human acceptance or formal verification.

The legacy policy is [`unconditional-v1`](./judge/policies/unconditional-v1.md): no
unproved cryptanalytic assumptions are admitted. The historical heuristic candidate is
retained as a negative control and cannot currently serve as a qualified baseline.
See [the unconditional birthday argument](./UNCONDITIONAL_BASELINE.md) for the proposed
replacement and [the multi-track plan](./YUKON_MULTITRACK_PLAN.md) for verified Yukon
schema-v2 support. The unconditional birthday replacement is not implemented; the nine
legacy local tracks are not an activated Yukon multi-track deployment. The scalar
time-memory objective is intentional and is not a Pareto-frontier implementation.

## Repository contract

For the legacy pilot, only [`candidate/`](./candidate) is participant-editable. A local
solver instead edits only its assigned `candidates/<track>/`, or
`lanes/<lane>/candidates/<target>/` for the new lanes. Each contains a strict JSON claim,
a Markdown proof, and optional certificate data. Everything that interprets or scores the
submission is outside that directory.

The generated Yukon score is `.yukon/score.json`. Verification failures exit nonzero and
do not write a placeholder score. Local scores are isolated at `.yukon/scores/<track>.json`;
paired-lane scores are under `lanes/<lane>/.yukon/scores/<track>.json`.
Nominal references and unsubmitted drafts never create these files.

## Local setup and tests

```bash
bash .yukon/setup.sh
```

This uses only Python's standard library and runs all deterministic and mocked-provider
tests. It does not contact either provider.

## Local live integration

For OpenRouter, place `OPENROUTER_API_KEY` in `.env`, then run:

```bash
bash scripts/run-local-live.sh
```

For Amazon Bedrock, place the API key in AWS's standard
`AWS_BEARER_TOKEN_BEDROCK` variable in `.env`, then run:

```bash
bash scripts/run-local-bedrock.sh
```

For GPT-5.6 Sol on Bedrock (the override wins over `.env` model settings):

```bash
bash .yukon/setup.sh
bash scripts/run-local-bedrock.sh --model us.openai.gpt-5.6-sol --region us-east-1
```

This selects Bedrock Runtime's Responses API. Claude continues to use Converse.
The existing Bedrock key must have Sol inference-profile and default-project access.

The scripts load `.env` without printing it, validate `candidate/`, send the inert proof
evidence to the selected provider, aggregate the structured reviews, and write a score
only if the result is `ai_qualified`. Reports are written under `.yukon/reports/` and are
ignored by Git.

For the bounded three-member calibration committee, run:

```bash
HASHSMASH_JUDGE_PROVIDER=bedrock bash scripts/run-local-committee.sh
```

The Bedrock committee runs three independent Opus 4.6 panels using formal-proof,
adversarial, and cost-skeptic strategies. Omitting the provider variable selects the
OpenRouter committee combining Sol, Opus, and Gemini. Both require unanimous qualification
and give technical-blocker and clarification results veto power. The script selects the
appropriate one-attempt calibration profile; production profiles allow bounded retries.

Provider choice, model IDs, regions, and privacy or routing settings are controlled through
environment variables documented in [`judge/README.md`](./judge/README.md). OpenRouter and
Bedrock Claude use provider JSON-schema output. Bedrock Sol receives the schema in trusted
instructions because this route does not advertise constrained structured outputs. Every
route enforces the same strict local schema and semantic validation; Sol output is never
repaired or accepted merely because it parses. OpenRouter
requests Zero Data Retention by default. Do not disable it unless the proof package is
approved for OpenRouter's non-ZDR retention policy.

## Yukon

[`benchmark.json`](./benchmark.json) is a schema-v1 GitHub Actions benchmark manifest.
The ranked workflow is [`.github/workflows/benchmark.yml`](./.github/workflows/benchmark.yml).
It separates deterministic intake from the secret-bearing judge job and uploads the exact
score path expected by Yukon.

The workflow has not been imported into Yukon as part of this MVP. Before production:

1. Select OpenRouter or Bedrock. Configure either an OpenRouter ZDR-compatible route and
   `OPENROUTER_API_KEY`, or a Bedrock API key and the desired model access. Evaluate AWS
   temporary credentials or role-based authentication before production hardening.
2. Decide whether improving PRs can be held for human review.
3. Replace the provisional generic baseline with a cryptographer-ratified frontier entry.
4. Create the GitHub repository, install the appropriate Yukon GitHub App, and obtain a
   Yukon dev importer API key from the allowlisted deployment operator.

See [`YUKON_CHALLENGE_PLAN.md`](./YUKON_CHALLENGE_PLAN.md) for the full design and rollout
plan. See [`MVP_VALIDATION.md`](./MVP_VALIDATION.md) for the offline and live provider test
record, certificate decision, and remaining production gates.
