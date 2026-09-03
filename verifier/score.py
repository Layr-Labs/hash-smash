"""Trusted deterministic Yukon score construction."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Mapping

from .certificates import verify_certificates
from .constants import SCHEMA_VERSION
from .errors import VerificationError
from .intake import validate_candidate
from .io import atomic_write_json, canonical_json_bytes, ensure_output_outside_root, sha256_bytes
from .schema_validation import require_sha256


def build_score(
    candidate_root: str | os.PathLike[str],
    aggregate: Mapping[str, Any],
    output_path: str | os.PathLike[str] | None = None,
) -> dict[str, Any]:
    """Build a score only for an explicitly AI-qualified judge aggregate.

    The leaderboard value is recomputed from the validated claim.  It is never accepted
    from the model or aggregate.  The caller may attach hashes of the judge configuration
    and dossier; other aggregate content is deliberately ignored.
    """

    if not isinstance(aggregate, Mapping):
        raise VerificationError("judge aggregate: must be an object")
    if aggregate.get("status") != "ai_qualified":
        raise VerificationError("judge aggregate: top-level status must equal 'ai_qualified'")

    judge_config_sha256: str | None = None
    dossier_sha256: str | None = None
    if "judge_config_sha256" in aggregate:
        judge_config_sha256 = require_sha256(
            aggregate["judge_config_sha256"], "$.judge_config_sha256"
        )
    if "dossier_sha256" in aggregate:
        dossier_sha256 = require_sha256(aggregate["dossier_sha256"], "$.dossier_sha256")

    intake = validate_candidate(candidate_root)
    aggregate_claim = aggregate.get("claim")
    if not isinstance(aggregate_claim, Mapping):
        raise VerificationError("judge aggregate: AI-qualified result must include a claim object")
    submitted_claim = intake["claim"]
    for field in ("target_profile", "attack_class", "rounds", "restrictions"):
        if aggregate_claim.get(field) != submitted_claim[field]:
            raise VerificationError(
                f"judge aggregate: reconstructed claim differs from submission at {field}"
            )
    certificate_report = verify_certificates(candidate_root)
    if certificate_report["package_sha256"] != intake["package_sha256"]:
        raise VerificationError("candidate package changed between deterministic gates")
    costs = intake["claim"]["claim"]
    time_log2 = float(costs["time_log2"])
    memory_log2_bytes = float(costs["memory_log2_bytes"])
    time_memory_log2 = time_log2 + memory_log2_bytes

    metrics: dict[str, Any] = {
        "reviewStatus": "ai_qualified",
        "targetProfile": intake["track"]["target_profile"],
        "attackClass": intake["track"]["attack_class"],
        "rounds": intake["track"]["rounds"],
        "timeLog2": time_log2,
        "memoryLog2Bytes": memory_log2_bytes,
        "timeMemoryLog2": time_memory_log2,
        "dataLog2": float(costs["data_log2"]),
        "preprocessingLog2": float(costs["preprocessing_log2"]),
        "nonuniformAdviceLog2Bytes": float(costs["nonuniform_advice_log2_bytes"]),
        "successProbability": float(costs["success_probability"]),
        "inputPackageSha256": intake["package_sha256"],
        "certificateReportSha256": sha256_bytes(canonical_json_bytes(certificate_report)),
    }
    if judge_config_sha256 is not None:
        metrics["judgeConfigSha256"] = judge_config_sha256
    if dossier_sha256 is not None:
        metrics["dossierSha256"] = dossier_sha256

    score = {
        "schema_version": SCHEMA_VERSION,
        "score": time_memory_log2,
        "metrics": metrics,
    }
    if output_path is not None:
        destination = Path(output_path)
        ensure_output_outside_root(Path(candidate_root), destination)
        atomic_write_json(destination, score)
    return score
