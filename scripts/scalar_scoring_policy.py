"""Explicit scalar policy transforms and the pinned original-challenge policy."""

from __future__ import annotations

import math
from pathlib import Path
import re
from typing import Any, Mapping

from scripts.scalar_score_resources import read_v5_score_resources
from verifier.errors import VerificationError
from verifier.io import canonical_json_bytes, load_json_bytes, sha256_bytes

FORMULA = "timeLog2 + log2(memoryUnits)"
SCORE_METRIC = "normalizedTimeMemoryLog2"
ACTIVE_POLICY_ID = "hashsmash-scalar-tm-v1"
ACTIVE_POLICY_SHA256 = "65f6bd3eb8260395d5a9520ebe14be10f68efba6bf4625d9cebef2221b832c2d"
ACTIVE_POLICY_PATH = Path(__file__).resolve().parents[1] / "scoring-policies" / f"{ACTIVE_POLICY_ID}.json"


def validate_policy(policy: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the complete scalar-time-memory-v1 policy definition.

    Numeric policy parameters must use JSON integer spelling, keeping the
    canonical definition identical across Python and JavaScript consumers.
    """
    fields = {
        "id", "version", "formula", "sourceCostModelId", "timeUnit",
        "memoryUnitBytes", "minimumMemoryUnits",
    }
    if not isinstance(policy, Mapping) or set(policy) != fields:
        raise VerificationError("scalar policy requires exactly the documented definition fields")
    identifier = policy["id"]
    if not isinstance(identifier, str) or re.fullmatch(r"[a-z][a-z0-9-]{0,95}", identifier) is None:
        raise VerificationError("scalar policy id must be a lowercase identifier of at most 96 characters")
    if type(policy["version"]) is not int or policy["version"] != 1:
        raise VerificationError("unsupported scalar policy version")
    if policy["formula"] != FORMULA:
        raise VerificationError("unsupported scalar policy formula")
    if policy["sourceCostModelId"] != "collision-frontier-v5":
        raise VerificationError("scalar policy requires collision-frontier-v5 resources")
    if policy["timeUnit"] != "target-compressions":
        raise VerificationError("scalar policy requires target-compressions")
    unit = policy["memoryUnitBytes"]
    if type(unit) is not int or not 1 <= unit <= 9007199254740991:
        raise VerificationError("scalar policy memoryUnitBytes must be a positive safe JSON integer")
    floor = policy["minimumMemoryUnits"]
    if floor is not None and (type(floor) is not int or floor != 1):
        raise VerificationError("scalar policy minimumMemoryUnits must be 1 or null")
    return dict(policy)


def scoring_policy_metadata(policy: Mapping[str, Any]) -> dict[str, str]:
    """Return the three scoring fields, separate from historical judge metadata."""
    definition = validate_policy(policy)
    return {
        "scoringPolicyId": definition["id"],
        "scoringPolicySha256": sha256_bytes(canonical_json_bytes(definition)),
        "scoreMetric": SCORE_METRIC,
    }


def active_scalar_policy() -> dict[str, Any]:
    """Load the immutable approved definition; a changed ID or hash fails closed."""
    definition = validate_policy(load_json_bytes(ACTIVE_POLICY_PATH.read_bytes(), str(ACTIVE_POLICY_PATH)))
    marker = scoring_policy_metadata(definition)
    if (marker["scoringPolicyId"] != ACTIVE_POLICY_ID
            or marker["scoringPolicySha256"] != ACTIVE_POLICY_SHA256):
        raise VerificationError("active scalar policy does not match its pinned ID and definition hash")
    return definition


def scalar_score(metrics: Mapping[str, Any], policy: Mapping[str, Any]) -> float:
    """Transform existing official bounds without exponentiating large costs.

    memoryUnits = memoryBytes / memoryUnitBytes; a non-null minimum floors
    memoryUnits at one. No rounding, time normalization, weighting, or default
    unit is implicit. The caller retains the original metrics and judgment
    provenance and separately attaches scoring_policy_metadata(policy).
    """
    definition = validate_policy(policy)
    time_log2, memory_log2_bytes = read_v5_score_resources(metrics)
    memory_log2_units = memory_log2_bytes - math.log2(definition["memoryUnitBytes"])
    if definition["minimumMemoryUnits"] is not None:
        memory_log2_units = max(0.0, memory_log2_units)
    score = time_log2 + memory_log2_units
    if not math.isfinite(score):
        raise VerificationError("scalar policy result must be finite")
    return score
