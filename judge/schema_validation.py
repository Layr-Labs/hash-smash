"""Small, strict validator for the checked-in review schema.

This intentionally implements only the JSON Schema vocabulary used by
``schemas/review-lanes-v1.schema.json``.  It is not a general JSON Schema engine.
Keeping the supported vocabulary explicit makes the no-dependency benchmark
runtime auditable and fail-closed.
"""

from __future__ import annotations

import math
from typing import Any, Mapping


class ReviewValidationError(ValueError):
    """The model response is not a valid, internally consistent review."""


def review_schema_for_stage(stage: str) -> dict[str, Any]:
    """Load the organizer schema for a supported paired-review stage."""
    from .lanes import LANE_STAGES, load_lane_schema

    if stage not in LANE_STAGES:
        raise ValueError(f"unknown paired review stage: {stage!r}")
    return load_lane_schema()


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
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            raise ReviewValidationError(f"{path}: exceeds maximum item count")
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


def validate_review(
    review: Any,
    *,
    expected_stage: str | None = None,
    schema: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate schema and semantic invariants, returning ``review`` unchanged."""

    from .lanes import validate_lane_review

    return validate_lane_review(review, expected_stage=expected_stage, schema=schema)
