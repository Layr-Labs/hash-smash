"""Trusted deterministic Yukon score construction."""

from __future__ import annotations

import math
import os
from pathlib import Path
from typing import Any, Mapping

from .certificates import verify_certificates
from .constants import SCHEMA_VERSION
from .errors import VerificationError
from .intake import validate_candidate
from .io import atomic_write_json, canonical_json_bytes, ensure_output_outside_root, sha256_bytes
from .schema_validation import require_sha256
from .frontier_tracks import LaneTrack


def build_score(
    candidate_root: str | os.PathLike[str],
    aggregate: Mapping[str, Any],
    output_path: str | os.PathLike[str] | None = None,
    *, track: LaneTrack,
) -> dict[str, Any]:
    """Build a score only for an explicitly AI-qualified judge aggregate.

    The leaderboard value is recomputed from the validated claim.  It is never accepted
    from the model or aggregate.  The caller may attach hashes of the judge configuration
    and dossier; other aggregate content is deliberately ignored.
    """

    if not isinstance(aggregate, Mapping):
        raise VerificationError("judge aggregate: must be an object")
    accepted_status = track.accepted_status
    if aggregate.get("status") != accepted_status:
        raise VerificationError(f"judge aggregate: top-level status must equal '{accepted_status}'")
    if aggregate.get("lane") != track.lane or aggregate.get("policy_id") != "paired-lanes-v1":
        raise VerificationError("judge aggregate: wrong lane or qualification policy")

    judge_config_sha256: str | None = None
    dossier_sha256: str | None = None
    if "judge_config_sha256" in aggregate:
        judge_config_sha256 = require_sha256(
            aggregate["judge_config_sha256"], "$.judge_config_sha256"
        )
    if "dossier_sha256" in aggregate:
        dossier_sha256 = require_sha256(aggregate["dossier_sha256"], "$.dossier_sha256")

    intake = validate_candidate(candidate_root, track=track)
    if intake["submission_state"] != "ready":
        raise VerificationError("draft templates cannot be scored")
    if aggregate.get("input_package_sha256") != intake["package_sha256"]:
        raise VerificationError("judge aggregate: stale or mismatched candidate package")
    if aggregate.get("target_config_sha256") != track.config_sha256():
        raise VerificationError("judge aggregate: stale or mismatched target configuration")
    aggregate_claim = aggregate.get("claim")
    if not isinstance(aggregate_claim, Mapping):
        raise VerificationError("judge aggregate: AI-qualified result must include a claim object")
    submitted_claim = intake["claim"]
    if canonical_json_bytes(aggregate_claim) != canonical_json_bytes(submitted_claim):
        raise VerificationError("paired judge aggregate must bind the entire submitted claim")
    certificate_report = verify_certificates(candidate_root, track=track)
    if certificate_report["package_sha256"] != intake["package_sha256"]:
        raise VerificationError("candidate package changed between deterministic gates")
    costs = intake["claim"]["claim"]
    time_log2 = float(costs["time_log2"])
    memory_log2_bytes = float(costs["memory_log2_bytes"])
    time_memory_log2 = time_log2 + memory_log2_bytes
    if not math.isfinite(time_memory_log2):
        raise VerificationError("time-memory score must be finite")

    metrics: dict[str, Any] = {
        "reviewStatus": accepted_status,
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
        "trackId": track.id,
        "targetConfigSha256": track.config_sha256(),
        "timeUnit": "target-compressions",
        "nominalReferenceScore": track.nominal_score,
        "improvesNominalReference": time_memory_log2 < track.nominal_score,
        "referenceIsQualifiedBaseline": False,
        "lane": track.lane,
        "qualificationPolicy": "paired-lanes-v1",
        "targetId": track.target_id,
        "unresolvedObligations": aggregate.get("reasons", []),
        "humanAccepted": False,
        "formallyVerified": False,
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
