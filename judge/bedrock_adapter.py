"""Amazon Bedrock Converse adapter for strict HashSmash reviews.

This uses Bedrock API-key bearer authentication directly over HTTPS so the judge keeps
its standard-library-only runtime.  Local validation remains authoritative even when
Bedrock structured output is enabled.
"""

from __future__ import annotations

import json
import os
import random
import re
import time
import urllib.parse
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping

from .prompts import DEFAULT_STRATEGY, build_messages, load_strategy_prompt
from .provider_adapter import (
    HttpResponse,
    JudgeInfraError,
    ReviewResult,
    Transport,
    TransportError,
    UrllibTransport,
    _schema_for_stage,
)
from .schema_validation import load_review_schema, validate_review


DEFAULT_BEDROCK_MODEL = "us.anthropic.claude-opus-4-6-v1"
DEFAULT_BEDROCK_REGION = "us-east-1"
BEDROCK_REASONING_EFFORTS = {"low", "medium", "high", "xhigh", "max"}
REGION_RE = re.compile(r"[a-z]{2}(?:-gov)?-[a-z]+-\d+\Z")

# Bedrock structured output accepts a documented subset of JSON Schema Draft 2020-12.
# These constraints are retained in the organizer-owned schema and enforced locally after
# inference, but must be omitted from the wire schema to avoid a Bedrock 400 response.
UNSUPPORTED_WIRE_SCHEMA_KEYS = {
    "exclusiveMaximum",
    "exclusiveMinimum",
    "maxItems",
    "maxLength",
    "maxProperties",
    "maximum",
    "minLength",
    "minProperties",
    "minimum",
    "multipleOf",
    "pattern",
    "uniqueItems",
}


def _bedrock_schema_for_stage(base_schema: Mapping[str, Any], stage: str) -> dict[str, Any]:
    schema = deepcopy(_schema_for_stage(base_schema, stage))

    def sanitize(value: Any) -> None:
        if isinstance(value, dict):
            for key in list(value):
                if key in UNSUPPORTED_WIRE_SCHEMA_KEYS:
                    value.pop(key)
                elif key == "minItems" and value[key] not in {0, 1}:
                    value.pop(key)
                else:
                    sanitize(value[key])
        elif isinstance(value, list):
            for item in value:
                sanitize(item)

    sanitize(schema)
    return schema


def _header(headers: Mapping[str, str], name: str) -> str | None:
    wanted = name.lower()
    for key, value in headers.items():
        if key.lower() == wanted:
            return value
    return None


def _retry_after(headers: Mapping[str, str], maximum: float) -> float | None:
    value = _header(headers, "Retry-After")
    if value is None:
        return None
    try:
        seconds = float(value)
    except ValueError:
        return None
    if seconds < 0:
        return None
    return min(seconds, maximum)


def _safe_bedrock_error(response: HttpResponse) -> str:
    """Extract only bounded AWS error identifiers and messages."""

    try:
        payload = json.loads(response.body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return ""
    if not isinstance(payload, dict):
        return ""
    error_type = payload.get("__type") or payload.get("code")
    message = payload.get("message") or payload.get("Message")
    parts: list[str] = []
    if isinstance(error_type, (str, int)) and not isinstance(error_type, bool):
        parts.append(f"type={str(error_type)[:120]}")
    if isinstance(message, str):
        normalized = " ".join(message.split())
        if normalized:
            parts.append(f"message={normalized[:300]}")
    return f" ({'; '.join(parts)})" if parts else ""


@dataclass(frozen=True)
class BedrockConfig:
    api_key: str = field(repr=False)
    model: str = DEFAULT_BEDROCK_MODEL
    region: str = DEFAULT_BEDROCK_REGION
    # Adaptive-thinking tokens count against this total.  The larger cap prevents the
    # substantive JSON review from being crowded out by reasoning; billing is based on
    # actual use, not the cap.
    max_tokens: int = 32768
    # First-use structured-output schema compilation can take several minutes.
    timeout_seconds: float = 300.0
    max_attempts: int = 3
    base_retry_seconds: float = 0.5
    max_retry_seconds: float = 8.0
    temperature: float | None = None
    reasoning_effort: str | None = "high"
    strategy: str = DEFAULT_STRATEGY
    app_title: str = "HashSmash AI Judge"

    def __post_init__(self) -> None:
        if not self.api_key:
            raise ValueError("Amazon Bedrock API key is required")
        if not self.model or len(self.model) > 2048 or any(char.isspace() for char in self.model):
            raise ValueError("Amazon Bedrock model ID is invalid")
        if not REGION_RE.fullmatch(self.region):
            raise ValueError("Amazon Bedrock region is invalid")
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        if self.max_tokens < 1:
            raise ValueError("max_tokens must be at least 1")
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if self.temperature is not None and not 0 <= self.temperature <= 1:
            raise ValueError("temperature must be between 0 and 1")
        if (
            self.reasoning_effort is not None
            and self.reasoning_effort not in BEDROCK_REASONING_EFFORTS
        ):
            raise ValueError("Bedrock reasoning_effort is not supported")
        load_strategy_prompt(self.strategy)

    @property
    def endpoint(self) -> str:
        model_path = urllib.parse.quote(self.model, safe="")
        return (
            f"https://bedrock-runtime.{self.region}.amazonaws.com/"
            f"model/{model_path}/converse"
        )

    @classmethod
    def from_env(cls) -> "BedrockConfig":
        api_key = os.environ.get("AWS_BEARER_TOKEN_BEDROCK", "")
        model = os.environ.get("HASHSMASH_BEDROCK_MODEL") or DEFAULT_BEDROCK_MODEL
        effort = os.environ.get("HASHSMASH_REASONING_EFFORT")
        if effort is None:
            effort = "high" if "anthropic.claude" in model else None
        elif effort.strip().lower() in {"", "none", "none-disabled", "off"}:
            effort = None
        else:
            effort = effort.strip().lower()
        return cls(
            api_key=api_key,
            model=model,
            region=(
                os.environ.get("HASHSMASH_BEDROCK_REGION")
                or os.environ.get("AWS_REGION")
                or os.environ.get("AWS_DEFAULT_REGION")
                or DEFAULT_BEDROCK_REGION
            ),
            reasoning_effort=effort,
            strategy=os.environ.get("HASHSMASH_JUDGE_STRATEGY", DEFAULT_STRATEGY),
        )


class BedrockClient:
    def __init__(
        self,
        config: BedrockConfig,
        *,
        transport: Transport | None = None,
        sleeper: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
        random_source: Callable[[], float] = random.random,
    ) -> None:
        self.config = config
        self.transport = transport or UrllibTransport()
        self.sleeper = sleeper
        self.clock = clock
        self.random_source = random_source
        self.schema = load_review_schema()

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "hashsmash-ai-judge/1",
        }

    def _request_body(self, stage: str, evidence: Mapping[str, Any]) -> bytes:
        messages = build_messages(stage, evidence, self.config.strategy)
        response_schema = _bedrock_schema_for_stage(self.schema, stage)
        body: dict[str, Any] = {
            "system": [{"text": messages[0]["content"]}],
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": messages[1]["content"]}],
                }
            ],
            "inferenceConfig": {"maxTokens": self.config.max_tokens},
            "outputConfig": {
                "textFormat": {
                    "type": "json_schema",
                    "structure": {
                        "jsonSchema": {
                            "schema": json.dumps(
                                response_schema,
                                ensure_ascii=True,
                                sort_keys=True,
                                separators=(",", ":"),
                            ),
                            "name": f"hashsmash_{stage}_review_v1",
                            "description": f"HashSmash {stage} review record",
                        }
                    },
                }
            },
        }
        if self.config.temperature is not None:
            body["inferenceConfig"]["temperature"] = self.config.temperature
        if self.config.reasoning_effort is not None:
            body["additionalModelRequestFields"] = {
                "thinking": {"type": "adaptive"},
                "output_config": {"effort": self.config.reasoning_effort},
            }
        return json.dumps(body, ensure_ascii=True, separators=(",", ":")).encode("utf-8")

    def _retry_delay(self, attempt: int, headers: Mapping[str, str] | None = None) -> float:
        if headers is not None:
            retry_after = _retry_after(headers, self.config.max_retry_seconds)
            if retry_after is not None:
                return retry_after
        exponential = min(
            self.config.max_retry_seconds,
            self.config.base_retry_seconds * (2 ** (attempt - 1)),
        )
        return exponential * (0.75 + 0.5 * self.random_source())

    def _parse_response(self, response: HttpResponse, stage: str) -> ReviewResult:
        try:
            payload = json.loads(response.body.decode("utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("root is not an object")
            if payload.get("stopReason") != "end_turn":
                raise ValueError("completion did not finish with end_turn")
            content = payload["output"]["message"]["content"]
            if not isinstance(content, list):
                raise ValueError("message content is not an array")
            text_blocks = [
                block["text"]
                for block in content
                if isinstance(block, dict) and isinstance(block.get("text"), str)
            ]
            if len(text_blocks) != 1:
                raise ValueError("expected exactly one structured text block")
            review = json.loads(text_blocks[0])
            if isinstance(review, dict):
                review.setdefault("decision", None)
                review.setdefault("verdict", None)
                review.setdefault("submitted_cost", None)
                review.setdefault("recomputed_cost", None)
                review.setdefault("calculation_trace", [])
            validate_review(review, expected_stage=stage, schema=self.schema)
            usage = payload.get("usage", {})
            metrics = payload.get("metrics", {})
            if not isinstance(usage, dict):
                raise ValueError("usage is not an object")
            if not isinstance(metrics, dict):
                raise ValueError("metrics is not an object")
        except (KeyError, TypeError, ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise JudgeInfraError(
                f"Amazon Bedrock returned an invalid structured response: {exc}"
            ) from exc

        return ReviewResult(
            review=review,
            provenance={
                "provider": "amazon-bedrock",
                "requested_model": self.config.model,
                "returned_model": self.config.model,
                "response_id": _header(response.headers, "x-amzn-requestid"),
                "region": self.config.region,
                "usage": usage,
                "metrics": metrics,
                "strategy": self.config.strategy,
                "reasoning_effort": self.config.reasoning_effort,
            },
        )

    def review(self, stage: str, evidence: Mapping[str, Any]) -> ReviewResult:
        body = self._request_body(stage, evidence)
        headers = self._headers()
        started = self.clock()
        attempt_latencies: list[int] = []
        last_error: JudgeInfraError | None = None

        for attempt in range(1, self.config.max_attempts + 1):
            attempt_started = self.clock()
            try:
                response = self.transport.request(
                    self.config.endpoint,
                    headers=headers,
                    body=body,
                    timeout_seconds=self.config.timeout_seconds,
                )
                attempt_latencies.append(round((self.clock() - attempt_started) * 1000))
            except TransportError as exc:
                attempt_latencies.append(round((self.clock() - attempt_started) * 1000))
                last_error = exc
                if attempt == self.config.max_attempts:
                    break
                self.sleeper(self._retry_delay(attempt))
                continue

            if response.status in {408, 429} or 500 <= response.status <= 599:
                last_error = JudgeInfraError(
                    f"Amazon Bedrock retryable HTTP status {response.status}",
                    attempts=attempt,
                )
                if attempt == self.config.max_attempts:
                    break
                self.sleeper(self._retry_delay(attempt, response.headers))
                continue
            if response.status < 200 or response.status > 299:
                raise JudgeInfraError(
                    f"Amazon Bedrock non-retryable HTTP status {response.status}"
                    f"{_safe_bedrock_error(response)}",
                    attempts=attempt,
                )

            try:
                result = self._parse_response(response, stage)
            except JudgeInfraError as exc:
                last_error = exc
                if attempt == self.config.max_attempts:
                    break
                self.sleeper(self._retry_delay(attempt))
                continue

            provenance = dict(result.provenance)
            provenance.update(
                {
                    "attempts": attempt,
                    "latency_ms": round((self.clock() - started) * 1000),
                    "attempt_latencies_ms": attempt_latencies,
                }
            )
            return ReviewResult(review=result.review, provenance=provenance)

        message = str(last_error) if last_error else "Amazon Bedrock did not produce a response"
        raise JudgeInfraError(message, attempts=self.config.max_attempts)
