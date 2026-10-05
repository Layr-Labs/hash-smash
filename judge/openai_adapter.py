"""Direct OpenAI Responses reviews, with native schema and full local validation."""

from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
import random
import re
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping

from .bedrock_adapter import _header, _retry_after, _safe_error_text, _strict_json
from .output import complete_review, retry_body, validate_response, validation_detail
from .prompts import DEFAULT_STRATEGY, build_messages, load_strategy_prompt, load_system_prompt
from .provider_adapter import (
    HttpResponse, JudgeInfraError, ReviewResult, Transport, TransportError,
    UrllibTransport, _schema_for_stage,
)

OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
OPENAI_REASONING_EFFORTS = {"none", "low", "medium", "high", "xhigh", "max"}
OUTPUT_CONTRACT = Path(__file__).resolve().with_name("prompts") / "openai-responses-json-v1.md"


def openai_schema_for_stage(stage: str) -> dict[str, Any]:
    """Keep substantive constraints; omit optional, ignored legacy cost metadata.

    Responses strict schemas require every property to be required. The local full
    schema continues to accept old records containing data_log2 without scoring it.
    """
    schema = _schema_for_stage(stage)
    if stage == "lane_cost":
        schema["properties"]["cost_reconstruction"]["properties"].pop("data_log2", None)
    return schema


def openai_system_prompt(config: "OpenAIConfig", stage: str) -> str:
    return (load_system_prompt(stage, config.strategy) + "\n\n"
            + OUTPUT_CONTRACT.read_text(encoding="utf-8").strip())


def openai_contract_provenance(config: "OpenAIConfig", stage: str) -> dict[str, str]:
    """Fingerprint the effective contract, including the adapter and shared helpers."""
    source_names = (
        "openai_adapter.py", "provider_adapter.py", "bedrock_adapter.py",
        "output.py", "prompts.py", "schema_validation.py",
    )
    source = {name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
              for name in source_names}
    schema = json.dumps(openai_schema_for_stage(stage), ensure_ascii=True,
                        sort_keys=True, separators=(",", ":")).encode()
    return {
        "system_prompt_sha256": hashlib.sha256(openai_system_prompt(config, stage).encode()).hexdigest(),
        "request_schema_sha256": hashlib.sha256(schema).hexdigest(),
        "adapter_source_sha256": hashlib.sha256(
            json.dumps(source, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
    }


@dataclass(frozen=True)
class OpenAIConfig:
    api_key: str = field(repr=False)
    model: str  # Explicit API model ID; no implicit model or alternate-provider fallback.
    max_tokens: int = 32768
    timeout_seconds: float = 300.0
    max_attempts: int = 3
    base_retry_seconds: float = 0.5
    max_retry_seconds: float = 8.0
    transient_base_retry_seconds: float = 60.0
    transient_max_retry_seconds: float = 120.0
    reasoning_effort: str = "high"
    strategy: str = DEFAULT_STRATEGY

    def __post_init__(self) -> None:
        if not isinstance(self.api_key, str) or not self.api_key.strip():
            raise ValueError("OPENAI_API_KEY is required")
        if any(not 33 <= ord(char) <= 126 for char in self.api_key):
            raise ValueError("OPENAI_API_KEY must contain only printable ASCII without whitespace")
        if not isinstance(self.model, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,199}", self.model):
            raise ValueError("HASHSMASH_OPENAI_MODEL must be an explicit OpenAI model ID")
        if type(self.max_tokens) is not int or not 1 <= self.max_tokens <= 128000:
            raise ValueError("max_tokens must be between 1 and 128000")
        if type(self.max_attempts) is not int or not 1 <= self.max_attempts <= 3:
            raise ValueError("max_attempts must be between 1 and 3")
        if not math.isfinite(self.timeout_seconds) or not 0 < self.timeout_seconds <= 300:
            raise ValueError("timeout_seconds must be finite and between 0 and 300")
        for base, maximum in (
            (self.base_retry_seconds, self.max_retry_seconds),
            (self.transient_base_retry_seconds, self.transient_max_retry_seconds),
        ):
            if not (math.isfinite(base) and math.isfinite(maximum) and 0 < base <= maximum <= 120):
                raise ValueError("retry delays must be finite, positive and base <= maximum <= 120")
        if self.reasoning_effort not in OPENAI_REASONING_EFFORTS:
            raise ValueError("OpenAI reasoning_effort is not supported")
        load_strategy_prompt(self.strategy)

    @property
    def endpoint(self) -> str:
        return OPENAI_RESPONSES_URL

    @classmethod
    def from_env(cls) -> "OpenAIConfig":
        return cls(
            api_key=os.environ.get("OPENAI_API_KEY", ""),
            model=os.environ.get("HASHSMASH_OPENAI_MODEL", ""),
            reasoning_effort=os.environ.get("HASHSMASH_REASONING_EFFORT", "high").strip().lower(),
            strategy=os.environ.get("HASHSMASH_JUDGE_STRATEGY", DEFAULT_STRATEGY),
        )


def _request_id(response: HttpResponse, key: str) -> str | None:
    return _safe_error_text(_header(response.headers, "x-request-id"), key, 128)


def _safe_error(response: HttpResponse, key: str) -> dict[str, Any]:
    detail: dict[str, Any] = {"request_id": _request_id(response, key)}
    try:
        payload = _strict_json(response.body.decode()) if len(response.body) <= 65536 else None
        error = payload.get("error") if isinstance(payload, dict) else None
        if isinstance(error, dict):
            for name, limit in (("code", 120), ("type", 120), ("message", 300)):
                value = _safe_error_text(error.get(name), key, limit)
                if value is not None:
                    detail[name] = value
    except (UnicodeDecodeError, ValueError, RecursionError):
        pass
    return detail


def _usage(value: Any) -> dict[str, Any]:
    """Retain only numeric token counters, never arbitrary provider metadata."""
    if not isinstance(value, dict):
        raise ValueError("usage is not an object")
    result = {name: value[name] for name in ("input_tokens", "output_tokens", "total_tokens")
              if type(value.get(name)) is int and value[name] >= 0}
    for name, field_name in (("input_tokens_details", "cached_tokens"),
                             ("output_tokens_details", "reasoning_tokens")):
        nested = value.get(name)
        if isinstance(nested, dict) and type(nested.get(field_name)) is int and nested[field_name] >= 0:
            result[name] = {field_name: nested[field_name]}
    return result


class OpenAIClient:
    def __init__(
        self, config: OpenAIConfig, *, transport: Transport | None = None,
        sleeper: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
        wall_clock: Callable[[], float] = time.time,
        random_source: Callable[[], float] = random.random,
    ) -> None:
        self.config = config
        # A redirect must never send this provider's bearer key to another host.
        self.transport = transport or UrllibTransport(follow_redirects=False)
        self.sleeper, self.clock = sleeper, clock
        self.wall_clock, self.random_source = wall_clock, random_source

    def _request_body(self, stage: str, evidence: Mapping[str, Any]) -> bytes:
        messages = build_messages(stage, evidence, self.config.strategy)
        return json.dumps({
            "model": self.config.model,
            "instructions": openai_system_prompt(self.config, stage),
            "input": [messages[1]],
            "max_output_tokens": self.config.max_tokens,
            "reasoning": {"effort": self.config.reasoning_effort},
            "store": False,
            "text": {"format": {
                "type": "json_schema", "name": f"hashsmash_{stage}_review_v1",
                "strict": True, "schema": openai_schema_for_stage(stage),
            }},
        }, ensure_ascii=True, separators=(",", ":")).encode()

    def _retry_delay(self, attempt: int, headers=None, *, transient=False) -> float:
        base = self.config.transient_base_retry_seconds if transient else self.config.base_retry_seconds
        maximum = self.config.transient_max_retry_seconds if transient else self.config.max_retry_seconds
        delay = min(maximum, base * 2 ** (attempt - 1) * (0.75 + 0.5 * self.random_source()))
        after = _retry_after(headers or {}, maximum, self.wall_clock())
        return max(delay, after) if after is not None else delay

    def _parse_response(self, response: HttpResponse, stage: str, evidence) -> ReviewResult:
        try:
            payload = _strict_json(response.body.decode())
            if not isinstance(payload, dict):
                raise ValueError("root is not an object")
            if payload.get("status") != "completed":
                raise ValueError("response did not complete")
            if payload.get("error") is not None or payload.get("incomplete_details") is not None:
                raise ValueError("response reports an error or incomplete output")
            if payload.get("model") != self.config.model:
                raise ValueError("response model does not match requested model")
            response_id = payload.get("id")
            if not isinstance(response_id, str) or not response_id:
                raise ValueError("response ID is missing")
            output = payload.get("output")
            if not isinstance(output, list):
                raise ValueError("output is not an array")
            texts = []
            for item in output:
                if not isinstance(item, dict):
                    raise ValueError("invalid output item")
                if item.get("type") == "reasoning":
                    continue  # Internal reasoning/encrypted content is never retained.
                if (item.get("type") != "message" or item.get("role") != "assistant"
                        or item.get("status") != "completed"):
                    raise ValueError("unexpected tool, role, or incomplete message")
                content = item.get("content")
                if not isinstance(content, list) or len(content) != 1:
                    raise ValueError("expected one message content block")
                block = content[0]
                if (not isinstance(block, dict) or block.get("type") != "output_text"
                        or not isinstance(block.get("text"), str)):
                    raise ValueError("refused or non-text response")
                texts.append(block["text"])
            if len(texts) != 1:
                raise ValueError("expected exactly one JSON review")
            review = complete_review(_strict_json(texts[0]), stage, evidence)
            validate_response(review, stage, evidence)
            usage = _usage(payload.get("usage", {}))
        except (KeyError, TypeError, ValueError, UnicodeDecodeError, RecursionError) as exc:
            detail = validation_detail(exc)
            detail = {key: _safe_error_text(value, self.config.api_key, 400)
                      if isinstance(value, str) else value for key, value in detail.items()}
            raise JudgeInfraError("OpenAI returned an invalid review", diagnostics=[detail]) from exc
        return ReviewResult(review=review, provenance={
            "provider": "openai", "api": "responses", "endpoint": self.config.endpoint,
            "output_validation": "provider-json-schema-and-local",
            "requested_model": self.config.model, "returned_model": self.config.model,
            "response_id": _safe_error_text(response_id, self.config.api_key, 128),
            "request_id": _request_id(response, self.config.api_key),
            "usage": usage, "strategy": self.config.strategy,
            "reasoning_effort": self.config.reasoning_effort, "store": False,
            **openai_contract_provenance(self.config, stage),
        })

    def review(self, stage: str, evidence: Mapping[str, Any]) -> ReviewResult:
        body = original = self._request_body(stage, evidence)
        headers = {"Authorization": f"Bearer {self.config.api_key}",
                   "Content-Type": "application/json", "Accept": "application/json",
                   "User-Agent": "hashsmash-ai-judge/1"}
        started = self.clock()
        latencies, diagnostics = [], []
        request_hashes, prompt_hashes = [], []
        last_error = "OpenAI did not produce a response"
        for attempt in range(1, self.config.max_attempts + 1):
            request_hashes.append(hashlib.sha256(body).hexdigest())
            prompt_hashes.append(hashlib.sha256(json.loads(body)["instructions"].encode()).hexdigest())
            attempt_started = self.clock()
            try:
                response = self.transport.request(self.config.endpoint, headers=headers, body=body,
                                                  timeout_seconds=self.config.timeout_seconds)
            except TransportError:
                latencies.append(round((self.clock() - attempt_started) * 1000))
                last_error = "OpenAI HTTP transport failed"
                diagnostics.append({"category": "transport", "attempt": attempt, "stage": stage,
                                    "latency_ms": latencies[-1]})
                if attempt < self.config.max_attempts:
                    self.sleeper(self._retry_delay(attempt, transient=True))
                continue
            latencies.append(round((self.clock() - attempt_started) * 1000))
            if not 200 <= response.status <= 299:
                detail = _safe_error(response, self.config.api_key)
                diagnostics.append({"category": "http", "status": response.status,
                                    "attempt": attempt, "stage": stage,
                                    "latency_ms": latencies[-1], **detail})
                last_error = f"OpenAI HTTP status {response.status}"
                retryable = response.status in {408, 429} or 500 <= response.status <= 599
                if not retryable or attempt == self.config.max_attempts:
                    break
                self.sleeper(self._retry_delay(attempt, response.headers, transient=True))
                continue
            try:
                result = self._parse_response(response, stage, evidence)
            except JudgeInfraError as exc:
                last_error = str(exc)
                diagnostics.extend({**detail, "attempt": attempt, "stage": stage,
                                    "latency_ms": latencies[-1],
                                    "request_id": _request_id(response, self.config.api_key)}
                                   for detail in exc.diagnostics)
                if attempt == self.config.max_attempts:
                    break
                body = retry_body(original, exc.diagnostics[-1])
                self.sleeper(self._retry_delay(attempt))
                continue
            return ReviewResult(review=result.review, provenance={
                **result.provenance, "attempts": attempt,
                "base_system_prompt_sha256": result.provenance["system_prompt_sha256"],
                "system_prompt_sha256": prompt_hashes[-1],
                "request_body_sha256": request_hashes[-1],
                "attempt_request_sha256": request_hashes,
                "attempt_system_prompt_sha256": prompt_hashes,
                "latency_ms": round((self.clock() - started) * 1000),
                "attempt_latencies_ms": latencies, "retry_diagnostics": diagnostics,
            })
        raise JudgeInfraError(last_error, attempts=attempt, diagnostics=diagnostics)
