"""Versioned paired-lane review schema, semantics, and organizer prompt loading."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Mapping

POLICY_ID = "paired-lanes-v1"
INITIAL_STAGES = ("lane_evaluability", "lane_cryptanalysis", "lane_cost", "lane_experiments")
CHALLENGE_STAGES = ("lane_defender", "lane_adjudicator")
LANE_STAGES = INITIAL_STAGES + CHALLENGE_STAGES
SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas/review-lanes-v1.schema.json"
PROMPT_DIR = Path(__file__).resolve().with_name("prompts")
OBLIGATIONS = {
    "lane_evaluability": (
        "target_defined", "algorithm_defined", "resources_defined", "probability_space_defined",
        "heuristics_disclosed", "evidence_relevant",
    ),
    "lane_cryptanalysis": ("collision_correctness", "probability_analysis", "heuristic_justification"),
    "lane_cost": ("time_bound", "memory_bound", "data_preprocessing_advice", "success_budget", "score_arithmetic"),
    "lane_experiments": ("experiment_relevance", "experiment_reproducibility", "statistics", "extrapolation"),
    "lane_defender": (),
    "lane_adjudicator": (),
}


def load_lane_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def load_lane_prompt(stage: str, strategy: str) -> str:
    # Reuse the established role strategies, but never import the legacy
    # unconditional policy into this explicitly different acceptance regime.
    from .prompts import load_strategy_prompt

    if stage not in LANE_STAGES:
        raise ValueError(f"unknown paired review stage: {stage!r}")
    common = (PROMPT_DIR / "paired-common-v1.md").read_text(encoding="utf-8").strip()
    rubric = (PROMPT_DIR / f"{stage.replace('_', '-')}-v1.md").read_text(encoding="utf-8").strip()
    strategy_prompt = load_strategy_prompt(strategy).replace("SHA-1", "target")
    return (
        f"{common}\n\nREVIEW STRATEGY: {strategy}\n{strategy_prompt}"
        f"\n\nREVIEW STAGE: {stage}\n{rubric}"
        f"\n\nRequired obligation IDs: {json.dumps(OBLIGATIONS[stage])}"
    )


def validate_lane_review(
    review: Any, *, expected_stage: str | None = None, schema: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    from .schema_validation import ReviewValidationError, _validate

    _validate(review, schema if schema is not None else load_lane_schema(), "$")
    stage = review["stage"]
    if expected_stage is not None and stage != expected_stage:
        raise ReviewValidationError("paired review stage does not match requested stage")
    for field, value in review["binding"].items():
        if len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
            raise ReviewValidationError(f"binding.{field} must be a lowercase SHA-256 digest")
    obligations = review["obligations"]
    ids = [item["id"] for item in obligations]
    if len(ids) != len(set(ids)) or set(ids) != set(OBLIGATIONS[stage]):
        raise ReviewValidationError("paired review must cover exactly the requested obligation IDs")
    findings = review["findings"]
    finding_ids = [item["id"] for item in findings]
    if len(finding_ids) != len(set(finding_ids)):
        raise ReviewValidationError("finding IDs must be unique within a review")
    for item in findings:
        if "/" in item["id"]:
            raise ReviewValidationError("local finding IDs cannot contain slash")
        if not set(item["obligation_ids"]) <= set(ids):
            raise ReviewValidationError("finding references an unknown obligation")
    fatal = [item for item in findings if item["severity"] == "fatal"]
    for item in obligations:
        if item["status"] == "fatal" and not any(item["id"] in f["obligation_ids"] for f in fatal):
            raise ReviewValidationError("fatal obligation requires a linked, cited fatal finding")
        if stage == "lane_evaluability" and item["status"] == "not_applicable":
            raise ReviewValidationError("evaluability obligations cannot be not_applicable")
        if item["status"] == "not_applicable" and item["id"] not in {
            "heuristic_justification", *OBLIGATIONS["lane_experiments"],
        }:
            raise ReviewValidationError("required mathematical/cost obligation cannot be not_applicable")
    heuristic_ids = [item["id"] for item in review["heuristics"]]
    if len(heuristic_ids) != len(set(heuristic_ids)):
        raise ReviewValidationError("heuristic IDs must be unique within a review")
    for item in findings:
        if not set(item["heuristic_ids"]) <= set(heuristic_ids):
            raise ReviewValidationError("finding references an unknown heuristic")
    for item in review["heuristics"]:
        if item["status"] == "refuted" and not any(item["id"] in finding["heuristic_ids"] for finding in fatal):
            raise ReviewValidationError("refuted heuristic requires its own linked, cited fatal finding")
    if review["prompt_injection_detected"] and not any(
        item["category"] == "prompt_injection" for item in findings
    ):
        raise ReviewValidationError("prompt injection flag requires a cited finding")
    challenges = review["challenge_resolutions"]
    if stage not in CHALLENGE_STAGES and challenges:
        raise ReviewValidationError("only defender/adjudicator may resolve challenges")
    if stage in CHALLENGE_STAGES and (findings or review["heuristics"]):
        raise ReviewValidationError("challenge reviews resolve supplied findings without introducing new ones")
    challenge_ids = [item["finding_id"] for item in challenges]
    if len(challenge_ids) != len(set(challenge_ids)):
        raise ReviewValidationError("challenge finding IDs must be unique")
    for item in challenges:
        if item["obligations_discharged"] and (stage != "lane_adjudicator" or item["result"] != "refuted"):
            raise ReviewValidationError("only a refuting adjudicator may discharge challenged obligations")
    cost = review["cost_reconstruction"]
    if stage != "lane_cost" and cost is not None:
        raise ReviewValidationError("cost reconstruction belongs only to lane_cost")
    if stage == "lane_cost":
        if cost is None:
            raise ReviewValidationError("lane_cost must reconstruct the resource claim")
        if not math.isclose(cost["normalized_score_log2"], cost["time_log2"] + cost["memory_log2_bytes"], abs_tol=1e-6):
            raise ReviewValidationError("reconstructed score must equal time_log2 + memory_log2_bytes")
    return review
