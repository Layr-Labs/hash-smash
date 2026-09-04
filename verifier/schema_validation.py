"""Small, explicit JSON validators for the pinned v1 schemas.

The project deliberately avoids a runtime JSON Schema dependency.  The JSON Schema
documents remain the public contract, while these functions implement the same closed
objects and constraints in Python's standard library.
"""

from __future__ import annotations

import math
import re
from typing import Any, NoReturn

from .constants import (
    ATTACK_CLASS,
    MANIFEST_PATH,
    MAX_CERTIFICATES,
    MINIMUM_SUCCESS_PROBABILITY,
    ROUNDS,
    SCHEMA_VERSION,
    TARGET_PROFILE,
)
from .errors import VerificationError
from .tracks import Track

_CERTIFICATE_PATH_RE = re.compile(r"certificates/[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
_CERTIFICATE_ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}\Z")
_SHA1_RE = re.compile(r"[0-9a-f]{40}\Z")
_SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")


def _fail(path: str, message: str) -> NoReturn:
    raise VerificationError(f"{path}: {message}")


def _object(value: Any, path: str, required: set[str], optional: set[str] = frozenset()) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail(path, "must be an object")
    if not all(isinstance(key, str) for key in value):
        _fail(path, "all field names must be strings")
    keys = set(value)
    missing = required - keys
    unknown = keys - required - optional
    if missing:
        _fail(path, f"missing required field(s): {', '.join(sorted(missing))}")
    if unknown:
        _fail(path, f"unknown field(s): {', '.join(sorted(unknown))}")
    return value


def _string(value: Any, path: str, *, nonempty: bool = True) -> str:
    if not isinstance(value, str):
        _fail(path, "must be a string")
    if nonempty and not value:
        _fail(path, "must not be empty")
    return value


def _number(value: Any, path: str, *, minimum: float | None = None, maximum: float | None = None) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        _fail(path, "must be a number")
    result = float(value)
    if not math.isfinite(result):
        _fail(path, "must be finite")
    if minimum is not None and result < minimum:
        _fail(path, f"must be at least {minimum}")
    if maximum is not None and result > maximum:
        _fail(path, f"must be at most {maximum}")
    return result


def _exact_integer(value: Any, expected: int, path: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value != expected:
        _fail(path, f"must equal {expected}")


def _exact_string(value: Any, expected: str, path: str) -> None:
    if not isinstance(value, str) or value != expected:
        _fail(path, f"must equal {expected!r}")


def validate_claim(value: Any, *, track: Track | None = None) -> dict[str, Any]:
    """Validate and return a claim conforming to claim-v1.schema.json."""

    claim = _object(
        value,
        "$",
        {
            "schema_version",
            "target_profile",
            "attack_class",
            "rounds",
            "claim",
            "restrictions",
            "baseline_improved",
        } | ({"submission_state"} if track else set()),
        {"certificate_manifest"},
    )
    _exact_integer(claim["schema_version"], 2 if track else SCHEMA_VERSION, "$.schema_version")
    _exact_string(claim["target_profile"], track.profile_id if track else TARGET_PROFILE, "$.target_profile")
    _exact_string(claim["attack_class"], ATTACK_CLASS, "$.attack_class")
    _exact_integer(claim["rounds"], track.rounds if track else ROUNDS, "$.rounds")
    if track and claim["submission_state"] not in ("draft", "ready"):
        _fail("$.submission_state", "must equal draft or ready")

    costs = _object(
        claim["claim"],
        "$.claim",
        {
            "time_log2",
            "time_unit",
            "memory_log2_bytes",
            "data_log2",
            "preprocessing_log2",
            "success_probability",
            "nonuniform_advice_log2_bytes",
        },
    )
    _number(costs["time_log2"], "$.claim.time_log2", minimum=0)
    _exact_string(costs["time_unit"], "target-compressions" if track else "sha1-compressions", "$.claim.time_unit")
    _number(costs["memory_log2_bytes"], "$.claim.memory_log2_bytes", minimum=0)
    _number(costs["data_log2"], "$.claim.data_log2", minimum=0)
    _number(costs["preprocessing_log2"], "$.claim.preprocessing_log2", minimum=0)
    _number(
        costs["success_probability"],
        "$.claim.success_probability",
        minimum=MINIMUM_SUCCESS_PROBABILITY,
        maximum=1,
    )
    _number(
        costs["nonuniform_advice_log2_bytes"],
        "$.claim.nonuniform_advice_log2_bytes",
        minimum=0,
    )

    restrictions = claim["restrictions"]
    if not isinstance(restrictions, list):
        _fail("$.restrictions", "must be an array")
    if len(restrictions) > 64:
        _fail("$.restrictions", "must contain no more than 64 items")
    for index, restriction in enumerate(restrictions):
        text = _string(restriction, f"$.restrictions[{index}]")
        if len(text) > 1024:
            _fail(f"$.restrictions[{index}]", "must contain no more than 1024 characters")
    baseline = _string(claim["baseline_improved"], "$.baseline_improved")
    if len(baseline) > 256:
        _fail("$.baseline_improved", "must contain no more than 256 characters")
    if track:
        _exact_string(baseline, track.reference_id, "$.baseline_improved")

    if "certificate_manifest" in claim:
        _exact_string(claim["certificate_manifest"], MANIFEST_PATH, "$.certificate_manifest")
    return claim


def validate_manifest(value: Any, *, track: Track | None = None) -> dict[str, Any]:
    """Validate and return a certificate manifest."""

    manifest = _object(value, "$", {"schema_version", "certificates"})
    _exact_integer(manifest["schema_version"], 2 if track else SCHEMA_VERSION, "$.schema_version")
    certificates = manifest["certificates"]
    if not isinstance(certificates, list):
        _fail("$.certificates", "must be an array")
    if len(certificates) > MAX_CERTIFICATES:
        _fail("$.certificates", f"must contain no more than {MAX_CERTIFICATES} items")

    ids: set[str] = set()
    for index, item in enumerate(certificates):
        path = f"$.certificates[{index}]"
        certificate = _object(
            item,
            path,
            {"id", "type", "message_a", "message_b", "expected_digest"} | ({"target_profile"} if track else set()),
        )
        certificate_id = _string(certificate["id"], f"{path}.id")
        if not _CERTIFICATE_ID_RE.fullmatch(certificate_id):
            _fail(f"{path}.id", "contains unsupported characters or is too long")
        if certificate_id in ids:
            _fail(f"{path}.id", "must be unique")
        ids.add(certificate_id)
        _exact_string(
            certificate["type"],
            "hash-collision-witness-v2" if track else "sha1-collision-witness-v1",
            f"{path}.type",
        )
        if track:
            _exact_string(certificate["target_profile"], track.profile_id, f"{path}.target_profile")
        for field in ("message_a", "message_b"):
            certificate_path = _string(certificate[field], f"{path}.{field}")
            if not _CERTIFICATE_PATH_RE.fullmatch(certificate_path):
                _fail(
                    f"{path}.{field}",
                    "must be a direct, safe file path under certificates/",
                )
            if certificate_path == MANIFEST_PATH:
                _fail(f"{path}.{field}", "must not refer to the manifest")
        digest = _string(certificate["expected_digest"], f"{path}.expected_digest")
        digest_length = track.digest_bits // 4 if track else 40
        if not re.fullmatch(r"[0-9a-f]{%d}" % digest_length, digest):
            _fail(f"{path}.expected_digest", f"must be {digest_length} lowercase hexadecimal characters")
    return manifest


def require_sha256(value: Any, path: str) -> str:
    text = _string(value, path)
    if not _SHA256_RE.fullmatch(text):
        _fail(path, "must be 64 lowercase hexadecimal characters")
    return text
