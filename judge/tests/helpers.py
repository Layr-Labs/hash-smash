from __future__ import annotations

import json
from copy import deepcopy
from typing import Any

from judge.lanes import OBLIGATIONS
from judge.paired_review import evidence_binding
from judge.provider_adapter import HttpResponse, ReviewResult


def fixture_evidence() -> dict:
    """Organizer-owned analytic fixture: never read a mutable solver candidate."""
    claim = {
        "schema_version": 3, "submission_state": "ready", "lane": "exploratory",
        "target_profile": "organizer-fixture-v1", "attack_class": "ordinary-collision", "rounds": 2,
        "claim": {
            "time_log2": 10.0, "time_unit": "target-compressions", "memory_log2_bytes": 8.0,
            "data_log2": 0.0, "preprocessing_log2": 0.0, "success_probability": 0.5,
            "nonuniform_advice_log2_bytes": 0.0,
        },
        "restrictions": [], "heuristics": [], "baseline_improved": "organizer-fixture-reference",
    }
    return {
        "schema_version": "hashsmash-evidence-v1",
        "submission": {
            "intake_report": {
                "status": "mechanically_valid", "submission_state": "ready", "claim": claim,
                "track": {"target_profile": "organizer-fixture-v1", "attack_class": "ordinary-collision", "rounds": 2},
                "package_sha256": "a" * 64, "target_config_sha256": "b" * 64,
            },
            "certificate_report": {"status": "passed", "package_sha256": "a" * 64, "target_config_sha256": "b" * 64},
            "proof_markdown_line_numbered": "L1\tAn organizer analytic fixture, not a real attack claim.",
        },
        "benchmark": {"target_profile": {"id": "organizer-fixture-v1"}},
    }


def fixture_review(stage: str, evidence: dict) -> dict:
    binding = evidence.get("review_context", {}).get("binding") or evidence_binding(evidence)
    result = {
        "schema_version": "review-lanes-v1", "stage": stage, "binding": deepcopy(binding),
        "summary": "Organizer synthetic decision fixture.",
        "obligations": [
            {"id": key, "status": "supported", "explanation": "Discharged by fixture.", "evidence": ["proof.md:L1"]}
            for key in OBLIGATIONS[stage]
        ],
        "heuristics": [], "findings": [], "cost_reconstruction": None,
        "challenge_resolutions": [], "prompt_injection_detected": False,
    }
    if stage == "lane_cost":
        cost = deepcopy(evidence["submission"]["intake_report"]["claim"]["claim"])
        cost.update(normalized_score_log2=cost["time_log2"] + cost["memory_log2_bytes"], calculation_trace=["10 + 8 = 18"])
        result["cost_reconstruction"] = cost
    for finding_id in evidence.get("review_context", {}).get("fatal_findings", {}):
        result["challenge_resolutions"].append({
            "finding_id": finding_id, "result": "unresolved", "explanation": "Fixture leaves objection unresolved.",
            "evidence": ["proof.md:L1"], "obligations_discharged": [],
        })
    return result


def add_fatal(review: dict) -> None:
    review["obligations"][0]["status"] = "fatal"
    review["findings"].append({
        "id": "collision-error", "severity": "fatal", "category": "counterexample",
        "statement": "A fixture critic alleges a concrete counterexample.",
        "obligation_ids": [review["obligations"][0]["id"]], "heuristic_ids": [], "evidence": ["proof.md:L1"],
    })


class FixtureClient:
    def __init__(self, mutate=None):
        self.mutate = mutate
        self.calls = []

    def review(self, stage, evidence):
        self.calls.append((stage, deepcopy(evidence)))
        review = fixture_review(stage, evidence)
        if self.mutate:
            self.mutate(stage, review, evidence)
        return ReviewResult(review, {"provider": "offline-organizer-fixture", "requested_model": "fixture"})


def review(stage: str) -> dict[str, Any]:
    return fixture_review(stage, fixture_evidence())


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
