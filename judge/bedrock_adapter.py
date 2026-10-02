"""Amazon Bedrock Converse/Responses adapter for strict HashSmash reviews.

This uses Bedrock API-key bearer authentication directly over HTTPS so the judge keeps
its standard-library-only runtime.  Local validation remains authoritative even when
Bedrock structured output is enabled.
"""

from __future__ import annotations

import json
import math
import os
import random
import re
import time
import urllib.parse
from copy import deepcopy
from dataclasses import dataclass, field
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Callable, Mapping

from .prompts import DEFAULT_STRATEGY, build_messages, load_strategy_prompt, load_system_prompt
from .provider_adapter import (
    HttpResponse,
    JudgeInfraError,
    ReviewResult,
    Transport,
    TransportError,
    UrllibTransport,
    _schema_for_stage,
)
from .schema_validation import review_schema_for_stage, validate_review
from .output import complete_review, validate_response, validation_detail, retry_body


DEFAULT_BEDROCK_MODEL = "us.anthropic.claude-opus-4-6-v1"
DEFAULT_BEDROCK_REGION = "us-east-1"
BEDROCK_SOL_MODELS = {"us.openai.gpt-5.6-sol", "global.openai.gpt-5.6-sol"}
SOL_OUTPUT_CONTRACT = Path(__file__).resolve().with_name("prompts") / "bedrock-sol-json-v1.md"
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


def _bedrock_schema_for_stage(stage: str) -> dict[str, Any]:
    schema = deepcopy(_schema_for_stage(stage))

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


def _retry_after(headers: Mapping[str, str], maximum: float, now: float) -> float | None:
    value = _header(headers, "Retry-After")
    if not isinstance(value, str) or len(value) > 128:
        return None
    try:
        seconds = float(value)
    except ValueError:
        try:
            date = parsedate_to_datetime(value)
            if date.tzinfo is None:
                return None
            seconds = max(0.0, date.timestamp() - now)
        except (ValueError, TypeError, OverflowError):
            return None
    if not math.isfinite(seconds) or seconds < 0:
        return None
    return min(seconds, maximum)


def _safe_error_text(value: Any, api_key: str, limit: int) -> str | None:
    """Redact before bounding; never retain terminal/control characters."""
    if not isinstance(value, (str, int)) or isinstance(value, bool):
        return None
    text = str(value)
    for secret in (api_key, urllib.parse.quote(api_key, safe="")):
        text = text.replace(secret, "[REDACTED]")
    # Provider messages sometimes echo authentication other than the configured key.
    text = re.sub(r"(?i)\b(?:bearer|basic)\s+[a-z0-9._~+/=-]+", "[REDACTED]", text)
    text = re.sub(
        r"""(?ix)\b(?:authorization|(?:x[-_])?api[-_]?key|(?:access[-_]|secret[-_])?token|
        password|secret|aws_bearer_token_bedrock|aws_secret_access_key|x-amz-security-token)
        ["']?\s*[:=]\s*(?:"[^"]*"|'[^']*'|[^\s,;]+)""",
        "[REDACTED]", text,
    )
    text = " ".join("".join(char if char.isprintable() else " " for char in text).split())
    return text[:limit] or None


def _request_id(headers: Mapping[str, str], api_key: str) -> str | None:
    value = (_header(headers, "x-amzn-requestid")
             or _header(headers, "x-amzn-request-id")
             or _header(headers, "x-amz-request-id"))
    return _safe_error_text(value, api_key, 128)


def _safe_bedrock_error(response: HttpResponse, api_key: str) -> dict[str, Any]:
    """Allowlist structured fields, never raw bodies, headers or reasoning."""
    detail: dict[str, Any] = {"request_id": _request_id(response.headers, api_key)}
    code = _header(response.headers, "x-amzn-errortype")
    message = None
    try:
        # Refuse oversized/ambiguous error envelopes rather than publishing a fragment.
        payload = _strict_json(response.body.decode("utf-8")) if len(response.body) <= 65536 else None
        if isinstance(payload, dict):
            if isinstance(payload.get("error"), dict):
                payload = payload["error"]
            code = next((payload[key] for key in ("code", "__type", "type")
                         if isinstance(payload.get(key), (str, int))
                         and not isinstance(payload[key], bool)), code)
            message = next((payload[key] for key in ("message", "Message")
                            if isinstance(payload.get(key), str)), None)
    except (UnicodeDecodeError, ValueError, RecursionError):
        pass
    for key, value, limit in (("error_code", code, 120), ("message", message, 300)):
        safe = _safe_error_text(value, api_key, limit)
        if safe is not None:
            detail[key] = safe
    return detail


def _strict_json(text: str) -> Any:
    """Reject ambiguous JSON rather than repairing unconstrained model output."""

    def object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON property")
            result[key] = value
        return result

    def invalid_constant(_: str) -> None:
        raise ValueError("non-finite JSON constant")

    return json.loads(text, object_pairs_hook=object_pairs, parse_constant=invalid_constant)


def bedrock_system_prompt(config: "BedrockConfig", stage: str) -> str:
    """Include the Sol JSON contract in the actual prompt and its provenance hash."""
    prompt = load_system_prompt(stage, config.strategy)
    if config.api == "responses":
        schema = _schema_for_stage(stage)
        prompt += "\n\n" + SOL_OUTPUT_CONTRACT.read_text(encoding="utf-8").strip()
        prompt += "\n\n" + json.dumps(schema, ensure_ascii=True, sort_keys=True)
    return prompt


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
    # One total request budget; validation and transient failures only differ in wait time.
    max_attempts: int = 3
    base_retry_seconds: float = 0.5
    max_retry_seconds: float = 8.0
    transient_base_retry_seconds: float = 60.0
    transient_max_retry_seconds: float = 120.0
    temperature: float | None = None
    reasoning_effort: str | None = "high"
    strategy: str = DEFAULT_STRATEGY
    app_title: str = "HashSmash AI Judge"

    def __post_init__(self) -> None:
        if not self.api_key:
            raise ValueError("Amazon Bedrock API key is required")
        if not self.model or len(self.model) > 2048 or any(char.isspace() for char in self.model):
            raise ValueError("Amazon Bedrock model ID is invalid")
        if "openai.gpt-5.6" in self.model and self.model not in BEDROCK_SOL_MODELS:
            raise ValueError(
                "Bedrock Sol requires us.openai.gpt-5.6-sol or global.openai.gpt-5.6-sol"
            )
        if not REGION_RE.fullmatch(self.region):
            raise ValueError("Amazon Bedrock region is invalid")
        if type(self.max_attempts) is not int or self.max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        for base, maximum in (
            (self.base_retry_seconds, self.max_retry_seconds),
            (self.transient_base_retry_seconds, self.transient_max_retry_seconds),
        ):
            if not (math.isfinite(base) and math.isfinite(maximum) and 0 < base <= maximum):
                raise ValueError("retry delays must be finite, positive and base <= maximum")
        if self.max_tokens < 1:
            raise ValueError("max_tokens must be at least 1")
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if self.temperature is not None and not 0 <= self.temperature <= 1:
            raise ValueError("temperature must be between 0 and 1")
        if (
            self.reasoning_effort is not None
            and self.reasoning_effort not in (
                BEDROCK_REASONING_EFFORTS | ({"none"} if self.api == "responses" else set())
            )
        ):
            raise ValueError("Bedrock reasoning_effort is not supported")
        if self.api == "responses" and self.temperature is not None:
            raise ValueError("Bedrock Sol temperature must be unset; use reasoning_effort")
        load_strategy_prompt(self.strategy)

    @property
    def api(self) -> str:
        return "responses" if self.model in BEDROCK_SOL_MODELS else "converse"

    @property
    def endpoint(self) -> str:
        if self.api == "responses":
            return f"https://bedrock-runtime.{self.region}.amazonaws.com/openai/v1/responses"
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
            effort = "high" if "anthropic.claude" in model or model in BEDROCK_SOL_MODELS else None
        elif effort.strip().lower() in {"", "none-disabled", "off"}:
            effort = None
        else:
            effort = effort.strip().lower()
            if effort == "none" and model not in BEDROCK_SOL_MODELS:
                effort = None
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
        wall_clock: Callable[[], float] = time.time,
        random_source: Callable[[], float] = random.random,
    ) -> None:
        self.config = config
        self.transport = transport or UrllibTransport()
        self.sleeper = sleeper
        self.clock = clock
        self.wall_clock = wall_clock
        self.random_source = random_source

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "hashsmash-ai-judge/1",
        }

    def _request_body(self, stage: str, evidence: Mapping[str, Any]) -> bytes:
        messages = build_messages(stage, evidence, self.config.strategy)
        if self.config.api == "responses":
            # Bedrock runtime does not advertise Sol structured outputs. Supply the
            # schema as trusted instructions; the full local validator is mandatory.
            body: dict[str, Any] = {
                "model": self.config.model,
                "instructions": bedrock_system_prompt(self.config, stage),
                "input": [messages[1]],
                "max_output_tokens": self.config.max_tokens,
                "store": False,
            }
            if self.config.reasoning_effort is not None:
                body["reasoning"] = {"effort": self.config.reasoning_effort}
            return json.dumps(body, ensure_ascii=True, separators=(",", ":")).encode("utf-8")
        response_schema = _bedrock_schema_for_stage(stage)
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
        if self.config.reasoning_effort is not None and "anthropic.claude" in self.config.model:
            body["additionalModelRequestFields"] = {
                "thinking": {"type": "adaptive"},
                "output_config": {"effort": self.config.reasoning_effort},
            }
        return json.dumps(body, ensure_ascii=True, separators=(",", ":")).encode("utf-8")

    def _retry_delay(
        self, attempt: int, headers: Mapping[str, str] | None = None, *, transient: bool = False,
    ) -> float:
        base = self.config.transient_base_retry_seconds if transient else self.config.base_retry_seconds
        maximum = self.config.transient_max_retry_seconds if transient else self.config.max_retry_seconds
        exponential = min(maximum, base * (2.0 ** min(attempt - 1, 1023)))
        delay = min(maximum, exponential * (0.75 + 0.5 * self.random_source()))
        if headers is not None:
            retry_after = _retry_after(headers, maximum, self.wall_clock())
            if retry_after is not None:
                delay = max(delay, retry_after)
        return delay

    def _parse_response(self, response: HttpResponse, stage: str, evidence=None) -> ReviewResult:
        if self.config.api == "responses":
            return self._parse_sol_response(response, stage, evidence)
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
            review = complete_review(json.loads(text_blocks[0]), stage, evidence or {})
            validate_response(review, stage, evidence or {})
            usage = payload.get("usage", {})
            metrics = payload.get("metrics", {})
            if not isinstance(usage, dict):
                raise ValueError("usage is not an object")
            if not isinstance(metrics, dict):
                raise ValueError("metrics is not an object")
        except (KeyError, TypeError, ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise JudgeInfraError("Amazon Bedrock returned an invalid review",
                                  diagnostics=[validation_detail(exc)]) from exc

        return ReviewResult(
            review=review,
            provenance={
                "provider": "amazon-bedrock",
                "api": "converse",
                "output_validation": "provider-json-schema-and-local",
                "requested_model": self.config.model,
                "returned_model": self.config.model,
                "response_id": _request_id(response.headers, self.config.api_key),
                "region": self.config.region,
                "usage": usage,
                "metrics": metrics,
                "strategy": self.config.strategy,
                "reasoning_effort": self.config.reasoning_effort,
            },
        )

    def _parse_sol_response(self, response: HttpResponse, stage: str, evidence=None) -> ReviewResult:
        try:
            payload = _strict_json(response.body.decode("utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("root is not an object")
            if payload.get("status") != "completed":
                raise ValueError("response did not complete")
            if payload.get("error") is not None or payload.get("incomplete_details") is not None:
                raise ValueError("response reports an error or incomplete output")
            returned_model = payload.get("model")
            if returned_model not in BEDROCK_SOL_MODELS | {"openai.gpt-5.6-sol", "gpt-5.6-sol"}:
                raise ValueError("response model does not match Sol")
            response_id = payload.get("id")
            if not isinstance(response_id, str) or not response_id:
                raise ValueError("response ID is missing")
            output = payload.get("output")
            if not isinstance(output, list):
                raise ValueError("output is not an array")
            texts: list[str] = []
            for item in output:
                if not isinstance(item, dict):
                    raise ValueError("invalid output item")
                if item.get("type") == "reasoning":
                    continue  # Never publish internal reasoning or encrypted content.
                if (
                    item.get("type") != "message"
                    or item.get("role") != "assistant"
                    or item.get("status") != "completed"
                ):
                    raise ValueError("unexpected tool, role, or incomplete message")
                content = item.get("content")
                if not isinstance(content, list) or len(content) != 1:
                    raise ValueError("expected one message content block")
                block = content[0]
                if (
                    not isinstance(block, dict)
                    or block.get("type") != "output_text"
                    or not isinstance(block.get("text"), str)
                ):
                    raise ValueError("refused or non-text response")
                texts.append(block["text"])
            if len(texts) != 1:
                raise ValueError("expected exactly one JSON review")
            review = complete_review(_strict_json(texts[0]), stage, evidence or {})
            validate_response(review, stage, evidence or {})
            usage = payload.get("usage", {})
            if not isinstance(usage, dict):
                raise ValueError("usage is not an object")
        except (KeyError, TypeError, ValueError, UnicodeDecodeError) as exc:
            raise JudgeInfraError("Amazon Bedrock returned an invalid Sol response",
                                  diagnostics=[validation_detail(exc)]) from exc

        return ReviewResult(
            review=review,
            provenance={
                "provider": "amazon-bedrock",
                "api": "responses",
                "output_validation": "prompt-json-schema-and-local",
                "requested_model": self.config.model,
                "returned_model": returned_model,
                "response_id": response_id,
                "aws_request_id": _request_id(response.headers, self.config.api_key),
                "region": self.config.region,
                "usage": usage,
                "strategy": self.config.strategy,
                "reasoning_effort": self.config.reasoning_effort,
                "store": False,
            },
        )

    def review(self, stage: str, evidence: Mapping[str, Any]) -> ReviewResult:
        body = self._request_body(stage, evidence)
        original_body = body
        headers = self._headers()
        started = self.clock()
        attempt_latencies: list[int] = []
        last_error: JudgeInfraError | None = None
        diagnostics = []

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
            except TransportError:
                attempt_latencies.append(round((self.clock() - attempt_started) * 1000))
                last_error = JudgeInfraError("Amazon Bedrock HTTP transport failed")
                diagnostics.append({"category": "transport", "attempt": attempt, "stage": stage,
                                    "latency_ms": attempt_latencies[-1]})
                if attempt == self.config.max_attempts:
                    break
                self.sleeper(self._retry_delay(attempt, transient=True))
                continue

            if response.status < 200 or response.status > 299:
                detail = _safe_bedrock_error(response, self.config.api_key)
                diagnostics.append({"category": "http", "status": response.status,
                                    "attempt": attempt, "stage": stage,
                                    "latency_ms": attempt_latencies[-1], **detail})
                retryable = response.status in {408, 429} or 500 <= response.status <= 599
                label = "retryable" if retryable else "non-retryable"
                last_error = JudgeInfraError(
                    f"Amazon Bedrock {label} HTTP status {response.status}: "
                    + json.dumps(detail, ensure_ascii=True, sort_keys=True),
                )
                if not retryable or attempt == self.config.max_attempts:
                    break
                self.sleeper(self._retry_delay(attempt, response.headers, transient=True))
                continue

            try:
                result = self._parse_response(response, stage, evidence)
            except JudgeInfraError as exc:
                last_error = exc
                for detail in exc.diagnostics:
                    diagnostics.append({**detail, "attempt": attempt, "stage": stage,
                                        "latency_ms": attempt_latencies[-1],
                                        "request_id": _request_id(response.headers, self.config.api_key)})
                if exc.diagnostics:
                    body = retry_body(original_body, exc.diagnostics[-1])
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
                    "retry_diagnostics": diagnostics,
                }
            )
            return ReviewResult(review=result.review, provenance=provenance)

        message = str(last_error) if last_error else "Amazon Bedrock did not produce a response"
        raise JudgeInfraError(message, attempts=attempt, diagnostics=diagnostics)
