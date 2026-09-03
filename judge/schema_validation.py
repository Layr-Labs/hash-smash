"""Small, strict validator for the checked-in review schema.

This intentionally implements only the JSON Schema vocabulary used by
``schemas/review-v1.schema.json``.  It is not a general JSON Schema engine.
Keeping the supported vocabulary explicit makes the no-dependency benchmark
runtime auditable and fail-closed.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Mapping


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA_PATH = REPO_ROOT / "schemas" / "review-v1.schema.json"


class ReviewValidationError(ValueError):
    """The model response is not a valid, internally consistent review."""


def load_review_schema(path: Path | str = DEFAULT_SCHEMA_PATH) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        schema = json.load(handle)
    if not isinstance(schema, dict):
        raise ReviewValidationError("review schema root must be an object")
    return schema


def _join(path: str, component: str | int) -> str:
    if isinstance(component, int):
        return f"{path}[{component}]"
    return f"{path}.{component}" if path != "$" else f"$.{component}"


def _type_matches(instance: Any, type_name: str) -> bool:
    if type_name == "null":
        return instance is None
    if type_name == "boolean":
        return isinstance(instance, bool)
    if type_name == "object":
        return isinstance(instance, dict)
    if type_name == "array":
        return isinstance(instance, list)
    if type_name == "string":
        return isinstance(instance, str)
    if type_name == "integer":
        return isinstance(instance, int) and not isinstance(instance, bool)
    if type_name == "number":
        return isinstance(instance, (int, float)) and not isinstance(instance, bool)
    raise ReviewValidationError(f"unsupported schema type: {type_name!r}")


def _validate(instance: Any, schema: Mapping[str, Any], path: str) -> None:
    declared = schema.get("type")
    if declared is not None:
        types = [declared] if isinstance(declared, str) else declared
        if not isinstance(types, list) or not all(isinstance(item, str) for item in types):
            raise ReviewValidationError(f"invalid type declaration in schema at {path}")
        if not any(_type_matches(instance, type_name) for type_name in types):
            expected = " or ".join(types)
            raise ReviewValidationError(f"{path}: expected {expected}")

    if "enum" in schema and instance not in schema["enum"]:
        raise ReviewValidationError(f"{path}: value is not in the allowed enum")

    if isinstance(instance, dict):
        properties = schema.get("properties", {})
        if not isinstance(properties, dict):
            raise ReviewValidationError(f"invalid properties declaration in schema at {path}")
        required = schema.get("required", [])
        missing = [key for key in required if key not in instance]
        if missing:
            raise ReviewValidationError(f"{path}: missing required properties: {', '.join(missing)}")
        if schema.get("additionalProperties") is False:
            extras = sorted(set(instance) - set(properties))
            if extras:
                raise ReviewValidationError(f"{path}: unknown properties: {', '.join(extras)}")
        for key, value in instance.items():
            if key in properties:
                _validate(value, properties[key], _join(path, key))

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            raise ReviewValidationError(f"{path}: requires at least {schema['minItems']} items")
        item_schema = schema.get("items")
        if item_schema is not None:
            for index, item in enumerate(instance):
                _validate(item, item_schema, _join(path, index))

    if isinstance(instance, str) and "minLength" in schema:
        if len(instance) < schema["minLength"]:
            raise ReviewValidationError(f"{path}: string is too short")

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        numeric = float(instance)
        if not math.isfinite(numeric):
            raise ReviewValidationError(f"{path}: number must be finite")
        if "minimum" in schema and numeric < schema["minimum"]:
            raise ReviewValidationError(f"{path}: number is below minimum")
        if "exclusiveMinimum" in schema and numeric <= schema["exclusiveMinimum"]:
            raise ReviewValidationError(f"{path}: number is below exclusive minimum")
        if "maximum" in schema and numeric > schema["maximum"]:
            raise ReviewValidationError(f"{path}: number is above maximum")


def _assert_stage_invariants(review: Mapping[str, Any]) -> None:
    stage = review["stage"]
    decision = review["decision"]
    verdict = review["verdict"]

    stage_verdicts = {
        "correctness": {"supported", "unsupported", "unclear"},
        "complexity": {"supported", "unsupported", "unclear"},
        "adversarial": {"no_known_blocker", "author_response_required", "major_blocker"},
        "synthesis": {"advance", "request_revision", "seek_specialist", "reject"},
    }
    if stage == "triage":
        if decision not in {"pass_to_review", "clarification_needed", "out_of_scope"}:
            raise ReviewValidationError("$.decision: triage requires a triage decision")
        if verdict is not None:
            raise ReviewValidationError("$.verdict: triage verdict must be null")
        if review["submitted_cost"] is not None or review["recomputed_cost"] is not None:
            raise ReviewValidationError("triage cost vectors must be null")
    else:
        if decision is not None:
            raise ReviewValidationError(f"$.decision: {stage} decision must be null")
        if verdict not in stage_verdicts[stage]:
            raise ReviewValidationError(f"$.verdict: invalid verdict for {stage}")

    if stage != "complexity":
        if review["submitted_cost"] is not None or review["recomputed_cost"] is not None:
            raise ReviewValidationError(f"{stage} cost vectors must be null")
        if review["calculation_trace"]:
            raise ReviewValidationError(f"{stage} calculation_trace must be empty")
    else:
        if review["submitted_cost"] is None or review["recomputed_cost"] is None:
            raise ReviewValidationError("complexity requires submitted and recomputed costs")
        if not review["calculation_trace"]:
            raise ReviewValidationError("complexity requires a non-empty calculation trace")
        for field in ("submitted_cost", "recomputed_cost"):
            vector = review[field]
            expected = vector["time_log2"] + vector["memory_log2_bytes"]
            if not math.isclose(vector["normalized_score_log2"], expected, abs_tol=1e-6):
                raise ReviewValidationError(
                    f"$.{field}.normalized_score_log2 must equal time_log2 + memory_log2_bytes"
                )
        if verdict == "supported":
            submitted = review["submitted_cost"]
            recomputed = review["recomputed_cost"]
            if submitted["time_unit"] != recomputed["time_unit"]:
                raise ReviewValidationError(
                    "supported complexity verdict contradicts cost discrepancy at time_unit"
                )
            upper_bound_fields = (
                "time_log2",
                "memory_log2_bytes",
                "data_log2",
                "preprocessing_log2",
                "nonuniform_advice_log2_bytes",
                "normalized_score_log2",
            )
            for key in upper_bound_fields:
                if recomputed[key] > submitted[key] + 1e-6:
                    raise ReviewValidationError(
                        f"supported complexity verdict contradicts cost discrepancy at {key}"
                    )
            if recomputed["success_probability"] + 1e-6 < submitted["success_probability"]:
                raise ReviewValidationError(
                    "supported complexity verdict contradicts cost discrepancy at success_probability"
                )

    fatal_issues = [issue for issue in review["issues"] if issue["severity"] == "fatal"]
    material_issues = [issue for issue in review["issues"] if issue["severity"] == "material"]
    survived = [
        counterexample
        for counterexample in review["attempted_counterexamples"]
        if counterexample["result"] == "survives"
    ]
    if stage == "triage":
        if decision == "pass_to_review" and (fatal_issues or survived):
            raise ReviewValidationError(
                "pass_to_review contradicts a fatal issue or surviving counterexample"
            )
        if decision == "out_of_scope" and not fatal_issues:
            raise ReviewValidationError("out_of_scope requires a cited fatal issue")
        if decision == "clarification_needed":
            if not (fatal_issues or material_issues or review["questions_for_author"]):
                raise ReviewValidationError(
                    "clarification_needed requires an issue or author question"
                )
    positive = verdict in {"supported", "no_known_blocker", "advance"}
    if positive and (fatal_issues or survived):
        raise ReviewValidationError("positive verdict contradicts a fatal issue or surviving counterexample")
    if verdict in {"unsupported", "major_blocker", "reject"} and not fatal_issues:
        raise ReviewValidationError("negative technical verdict requires a cited fatal issue")
    if verdict in {"unclear", "author_response_required", "request_revision", "seek_specialist"}:
        if not (fatal_issues or material_issues or review["questions_for_author"]):
            raise ReviewValidationError("unclear/revision verdict requires an issue or author question")

    if review["prompt_injection_detected"]:
        injection_issues = [
            issue
            for issue in review["issues"]
            if issue["category"] == "prompt_injection" and issue["severity"] in {"fatal", "material"}
        ]
        if not injection_issues:
            raise ReviewValidationError(
                "prompt_injection_detected requires a material or fatal prompt_injection issue"
            )


def validate_review(
    review: Any,
    *,
    expected_stage: str | None = None,
    schema: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate schema and semantic invariants, returning ``review`` unchanged."""

    active_schema = schema if schema is not None else load_review_schema()
    _validate(review, active_schema, "$")
    if not isinstance(review, dict):  # Narrow the type after the schema check.
        raise ReviewValidationError("review root must be an object")
    if expected_stage is not None and review.get("stage") != expected_stage:
        raise ReviewValidationError(
            f"$.stage: expected {expected_stage!r}, got {review.get('stage')!r}"
        )
    _assert_stage_invariants(review)
    return review
