"""OpenRouter Chat Completions adapter for strict HashSmash reviews."""

from __future__ import annotations

import json
import os
import random
import time
import urllib.error
import urllib.request
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Protocol

from .prompts import DEFAULT_STRATEGY, build_messages, load_strategy_prompt
from .schema_validation import load_review_schema, validate_review


OPENROUTER_CHAT_COMPLETIONS_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "openai/gpt-5.6-sol"
REASONING_EFFORTS = {"none", "minimal", "low", "medium", "high", "xhigh", "max"}


class JudgeInfraError(RuntimeError):
    """No valid review was produced because the judge infrastructure failed."""

    def __init__(self, message: str, *, attempts: int = 0) -> None:
        super().__init__(message)
        self.attempts = attempts


class TransportError(JudgeInfraError):
    """The HTTP request did not produce a response."""


@dataclass(frozen=True)
class HttpResponse:
    status: int
    headers: Mapping[str, str]
    body: bytes


class Transport(Protocol):
    def request(
        self,
        url: str,
        *,
        headers: Mapping[str, str],
        body: bytes,
        timeout_seconds: float,
    ) -> HttpResponse: ...


class UrllibTransport:
    """Minimal stdlib HTTP transport; it deliberately performs no logging."""

    def request(
        self,
        url: str,
        *,
        headers: Mapping[str, str],
        body: bytes,
        timeout_seconds: float,
    ) -> HttpResponse:
        request = urllib.request.Request(url, data=body, headers=dict(headers), method="POST")
        try:
            with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
                return HttpResponse(
                    status=response.status,
                    headers=dict(response.headers.items()),
                    body=response.read(),
                )
        except urllib.error.HTTPError as exc:
            # HTTP errors are responses. Return the body only to the parser; callers never
            # include it in exception messages because it may contain provider internals.
            return HttpResponse(
                status=exc.code,
                headers=dict(exc.headers.items()) if exc.headers else {},
                body=exc.read(),
            )
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise TransportError(f"Judge HTTP transport failed: {type(exc).__name__}") from exc


@dataclass(frozen=True)
class OpenRouterConfig:
    api_key: str = field(repr=False)
    model: str = DEFAULT_MODEL
    endpoint: str = OPENROUTER_CHAT_COMPLETIONS_URL
    max_tokens: int = 16384
    timeout_seconds: float = 120.0
    max_attempts: int = 3
    base_retry_seconds: float = 0.5
    max_retry_seconds: float = 8.0
    require_parameters: bool = True
    data_collection: str = "deny"
    zdr: bool = True
    temperature: float | None = None
    reasoning_effort: str | None = "high"
    strategy: str = DEFAULT_STRATEGY
    app_url: str | None = None
    app_title: str = "HashSmash AI Judge"

    def __post_init__(self) -> None:
        if not self.api_key:
            raise ValueError("OpenRouter API key is required")
        if not self.model:
            raise ValueError("OpenRouter model is required")
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        if self.max_tokens < 1:
            raise ValueError("max_tokens must be at least 1")
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if self.data_collection not in {"allow", "deny"}:
            raise ValueError("data_collection must be 'allow' or 'deny'")
        if self.reasoning_effort is not None and self.reasoning_effort not in REASONING_EFFORTS:
            raise ValueError("reasoning_effort is not supported")
        load_strategy_prompt(self.strategy)

    @classmethod
    def from_env(cls) -> "OpenRouterConfig":
        """Create config from process environment; this does not read a .env file."""

        api_key = os.environ.get("OPENROUTER_API_KEY", "")
        model = (
            os.environ.get("HASHSMASH_JUDGE_MODEL")
            or os.environ.get("OPENROUTER_MODEL")
            or DEFAULT_MODEL
        )
        effort = os.environ.get("HASHSMASH_REASONING_EFFORT")
        if effort is None:
            effort = "high" if model.startswith("openai/gpt-5.6") else None
        elif effort.strip().lower() in {"", "none-disabled", "off"}:
            effort = None
        else:
            effort = effort.strip().lower()
        zdr_text = os.environ.get("HASHSMASH_OPENROUTER_ZDR", "true").strip().lower()
        if zdr_text not in {"true", "false", "1", "0", "yes", "no"}:
            raise ValueError("HASHSMASH_OPENROUTER_ZDR must be true or false")
        return cls(
            api_key=api_key,
            model=model,
            zdr=zdr_text in {"true", "1", "yes"},
            reasoning_effort=effort,
            strategy=os.environ.get("HASHSMASH_JUDGE_STRATEGY", DEFAULT_STRATEGY),
            app_url=os.environ.get("HASHSMASH_APP_URL") or None,
        )


@dataclass(frozen=True)
class ReviewResult:
    review: dict[str, Any]
    provenance: dict[str, Any]


def _schema_for_stage(base_schema: Mapping[str, Any], stage: str) -> dict[str, Any]:
    """Specialize the wire schema so the provider cannot fill in forbidden fields."""

    schema = deepcopy(dict(base_schema))
    # Provider structured-output implementations accept the validation schema, but
    # some reject draft/document annotations that are useful only to local tooling.
    for annotation in ("$schema", "$id", "title"):
        schema.pop(annotation, None)
    properties = schema["properties"]
    properties["stage"] = {"type": "string", "enum": [stage]}

    def remove_wire_fields(*fields: str) -> None:
        for field in fields:
            properties.pop(field, None)
        schema["required"] = [field for field in schema["required"] if field not in fields]

    if stage == "triage":
        properties["decision"] = {
            "type": "string",
            "enum": ["pass_to_review", "clarification_needed", "out_of_scope"],
        }
        remove_wire_fields("verdict")
    else:
        remove_wire_fields("decision")
        verdicts = {
            "correctness": ["supported", "unsupported", "unclear"],
            "complexity": ["supported", "unsupported", "unclear"],
            "adversarial": [
                "no_known_blocker",
                "author_response_required",
                "major_blocker",
            ],
            "synthesis": ["advance", "request_revision", "seek_specialist", "reject"],
        }
        try:
            properties["verdict"] = {"type": "string", "enum": verdicts[stage]}
        except KeyError as exc:
            raise ValueError(f"unknown review stage: {stage!r}") from exc

    if stage == "complexity":
        for field in ("submitted_cost", "recomputed_cost"):
            properties[field]["type"] = "object"
        properties["calculation_trace"]["minItems"] = 1
    else:
        remove_wire_fields("submitted_cost", "recomputed_cost", "calculation_trace")
    return schema


def _header(headers: Mapping[str, str], name: str) -> str | None:
    wanted = name.lower()
    for key, value in headers.items():
        if key.lower() == wanted:
            return value
    return None


def _safe_retry_after(headers: Mapping[str, str], maximum: float) -> float | None:
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


def _safe_provider_error(response: HttpResponse) -> str:
    """Extract a bounded OpenRouter error code/message without echoing arbitrary bodies."""

    try:
        payload = json.loads(response.body.decode("utf-8"))
        error = payload.get("error") if isinstance(payload, dict) else None
        if not isinstance(error, dict):
            return ""
        code = error.get("code")
        message = error.get("message")
        parts: list[str] = []
        if isinstance(code, (str, int)) and not isinstance(code, bool):
            parts.append(f"code={str(code)[:80]}")
        if isinstance(message, str):
            normalized = " ".join(message.split())
            if normalized:
                parts.append(f"message={normalized[:300]}")
        return f" ({'; '.join(parts)})" if parts else ""
    except (UnicodeDecodeError, json.JSONDecodeError, AttributeError):
        return ""


class OpenRouterClient:
    def __init__(
        self,
        config: OpenRouterConfig,
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
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "hashsmash-ai-judge/1",
            "X-OpenRouter-Title": self.config.app_title,
            "X-OpenRouter-Metadata": "enabled",
        }
        if self.config.app_url:
            headers["HTTP-Referer"] = self.config.app_url
        return headers

    def _request_body(self, stage: str, evidence: Mapping[str, Any]) -> bytes:
        response_schema = _schema_for_stage(self.schema, stage)
        body: dict[str, Any] = {
            "model": self.config.model,
            "messages": build_messages(stage, evidence, self.config.strategy),
            "max_tokens": self.config.max_tokens,
            "stream": False,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": f"hashsmash_{stage}_review_v1",
                    "strict": True,
                    "schema": response_schema,
                },
            },
            "provider": {
                "require_parameters": self.config.require_parameters,
                "data_collection": self.config.data_collection,
                "zdr": self.config.zdr,
            },
        }
        if self.config.temperature is not None:
            body["temperature"] = self.config.temperature
        if self.config.reasoning_effort is not None:
            body["reasoning"] = {
                "effort": self.config.reasoning_effort,
                "exclude": True,
            }
        return json.dumps(body, ensure_ascii=True, separators=(",", ":")).encode("utf-8")

    def _retry_delay(self, attempt: int, headers: Mapping[str, str] | None = None) -> float:
        if headers is not None:
            retry_after = _safe_retry_after(headers, self.config.max_retry_seconds)
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
            choices = payload["choices"]
            if not isinstance(choices, list) or len(choices) != 1:
                raise ValueError("expected exactly one choice")
            choice = choices[0]
            if not isinstance(choice, dict) or choice.get("finish_reason") != "stop":
                raise ValueError("completion did not finish with stop")
            message = choice["message"]
            if not isinstance(message, dict) or not isinstance(message.get("content"), str):
                raise ValueError("missing string message content")
            review = json.loads(message["content"])
            if isinstance(review, dict):
                # The provider-facing schema omits stage-inapplicable null/empty fields.
                # Restore the canonical review record before strict local validation.
                review.setdefault("decision", None)
                review.setdefault("verdict", None)
                review.setdefault("submitted_cost", None)
                review.setdefault("recomputed_cost", None)
                review.setdefault("calculation_trace", [])
            validate_review(review, expected_stage=stage, schema=self.schema)
            response_id = payload["id"]
            returned_model = payload["model"]
            if not isinstance(response_id, str) or not response_id:
                raise ValueError("missing response id")
            if not isinstance(returned_model, str) or not returned_model:
                raise ValueError("missing returned model")
            usage = payload.get("usage", {})
            if not isinstance(usage, dict):
                raise ValueError("usage is not an object")
            metadata = payload.get("openrouter_metadata", {})
            if not isinstance(metadata, dict):
                raise ValueError("openrouter_metadata is not an object")
        except (KeyError, TypeError, ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise JudgeInfraError(f"OpenRouter returned an invalid structured response: {exc}") from exc

        provenance = {
            "provider": "openrouter",
            "requested_model": self.config.model,
            "returned_model": returned_model,
            "response_id": response_id,
            "created": payload.get("created"),
            "service_tier": payload.get("service_tier"),
            "usage": usage,
            "openrouter_metadata": metadata,
            "data_collection": self.config.data_collection,
            "zdr_requested": self.config.zdr,
            "strategy": self.config.strategy,
            "reasoning_effort": self.config.reasoning_effort,
        }
        return ReviewResult(review=review, provenance=provenance)

    def review(self, stage: str, evidence: Mapping[str, Any]) -> ReviewResult:
        """Run one independent review with bounded infrastructure retries."""

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

            if response.status == 429 or 500 <= response.status <= 599:
                last_error = JudgeInfraError(
                    f"OpenRouter retryable HTTP status {response.status}", attempts=attempt
                )
                if attempt == self.config.max_attempts:
                    break
                self.sleeper(self._retry_delay(attempt, response.headers))
                continue
            if response.status < 200 or response.status > 299:
                raise JudgeInfraError(
                    f"OpenRouter non-retryable HTTP status {response.status}"
                    f"{_safe_provider_error(response)}",
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

        message = str(last_error) if last_error else "OpenRouter did not produce a response"
        raise JudgeInfraError(message, attempts=self.config.max_attempts)
