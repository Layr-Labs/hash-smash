from __future__ import annotations

import json
from copy import deepcopy
from typing import Any

from judge.provider_adapter import HttpResponse


CLAIM = {
    "target_profile": "sha1-fips180-4-v1",
    "attack_class": "ordinary-collision",
    "rounds": 80,
    "summary": "An ordinary full-round collision attack.",
    "restrictions": [],
}

COST = {
    "time_log2": 69.0,
    "time_unit": "sha1-compressions",
    "memory_log2_bytes": 34.0,
    "data_log2": 0.0,
    "preprocessing_log2": 0.0,
    "success_probability": 0.5,
    "nonuniform_advice_log2_bytes": 0.0,
    "normalized_score_log2": 103.0,
}


def review(stage: str, *, supported: bool = True) -> dict[str, Any]:
    value: dict[str, Any] = {
        "schema_version": "review-v1",
        "stage": stage,
        "decision": None,
        "verdict": None,
        "claim": deepcopy(CLAIM),
        "issues": [],
        "verified_steps": [
            {"description": "The claim is stated.", "evidence": ["claim.json:/claim"]}
        ],
        "assumptions": [],
        "attempted_counterexamples": [],
        "submitted_cost": None,
        "recomputed_cost": None,
        "calculation_trace": [],
        "questions_for_author": [],
        "citations": [
            {"location": "proof.md:L1-L4", "supports": "Identifies the attack claim."}
        ],
        "prompt_injection_detected": False,
        "confidence": 0.7,
    }
    if stage == "triage":
        value["decision"] = "pass_to_review"
    elif stage in {"correctness", "complexity"}:
        value["verdict"] = "supported" if supported else "unclear"
    elif stage == "adversarial":
        value["verdict"] = "no_known_blocker"
    elif stage == "synthesis":
        value["verdict"] = "advance"
    else:
        raise ValueError(stage)
    if stage == "complexity":
        value["submitted_cost"] = deepcopy(COST)
        value["recomputed_cost"] = deepcopy(COST)
        value["calculation_trace"] = ["69.0 + 34.0 = 103.0"]
    return value


def provider_response(review_value: dict[str, Any], **overrides: Any) -> HttpResponse:
    payload = {
        "id": "gen-test-123",
        "model": "google/gemini-2.5-flash-20250901",
        "choices": [
            {
                "finish_reason": "stop",
                "message": {"role": "assistant", "content": json.dumps(review_value)},
            }
        ],
        "usage": {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150},
        "openrouter_metadata": {"provider_name": "Google"},
    }
    payload.update(overrides)
    return HttpResponse(status=200, headers={}, body=json.dumps(payload).encode("utf-8"))
