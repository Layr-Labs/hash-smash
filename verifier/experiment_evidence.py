"""Bind isolated experiment outputs to the exact candidate and trusted target."""

from pathlib import Path
from typing import Any

from experiments import declared_files, run_experiments, verify_report_integrity
from .certificates import _read_certificate_file
from .errors import VerificationError
from .hash_functions import digest
from .io import canonical_json_bytes, sha256_bytes


def source_snapshot(candidate: Path, intake: dict) -> dict[str, bytes]:
    manifest = intake.get("experiment_manifest")
    if manifest is None:
        return {}
    indexed = {item["path"]: item for item in intake["files"]}
    sources = {}
    for name in sorted(declared_files(manifest)):
        data = _read_certificate_file(candidate, name)
        if name not in indexed or sha256_bytes(data) != indexed[name]["sha256"]:
            raise VerificationError("experiment source changed after intake")
        sources[name] = data
    return sources


def execute(candidate: Path, intake: dict, track, *, holdout_nonce: str | None = None) -> dict:
    """Call only before judge credentials are used; candidate Python stays isolated."""
    ready = intake["submission_state"] == "ready"
    manifest = intake.get("experiment_manifest")
    report: dict[str, Any] = {
        "status": "passed" if ready and manifest is not None else "not_requested" if ready else "draft_not_submitted",
        "package_sha256": intake["package_sha256"],
        "target_config_sha256": track.config_sha256(),
        "execution": None,
    }
    if ready and manifest is not None:
        report["execution"] = run_experiments(
            manifest, source_snapshot(candidate, intake), target_profile=track.profile_id,
            target_config_sha256=track.config_sha256(), holdout_nonce=holdout_nonce,
            digest_fn=lambda message: digest(message, track.algorithm, track.rounds),
        )
    return report


def validate_stored(report: Any, candidate: Path, intake: dict, track) -> dict:
    """Validate bindings without executing participant code in the judge job.

    Workflow artifact provenance supplies authenticity. Hashes detect stale inputs
    and accidental corruption; a hash alone is not a signature by the executor.
    """
    if not isinstance(report, dict) or set(report) != {
        "status", "package_sha256", "target_config_sha256", "execution",
    }:
        raise VerificationError("invalid experiment evidence envelope")
    if (report["package_sha256"] != intake["package_sha256"]
            or report["target_config_sha256"] != track.config_sha256()):
        raise VerificationError("stale experiment evidence package or target")
    manifest = intake.get("experiment_manifest")
    if manifest is None:
        if report["status"] != "not_requested" or report["execution"] is not None:
            raise VerificationError("unexpected experiment report for a claim without experiments")
        return report
    if report["status"] != "passed":
        raise VerificationError("required experiments did not complete")
    try:
        execution = verify_report_integrity(report["execution"])
    except (ValueError, TypeError, KeyError) as error:
        raise VerificationError(f"invalid experiment evidence: {error}") from error
    if (execution["target_profile"] != track.profile_id
            or execution["target_config_sha256"] != track.config_sha256()
            or canonical_json_bytes(execution["manifest"]) != canonical_json_bytes(manifest)):
        raise VerificationError("experiment execution does not bind this target and manifest")
    expected = source_snapshot(candidate, intake)
    # Validate exact source bytes against the independently snapshotted intake.
    recorded = execution["sources"]
    if isinstance(recorded, list):
        if len({item["path"] for item in recorded}) != len(recorded):
            raise VerificationError("duplicate experiment report source")
        recorded = {item["path"]: item for item in recorded}
    if set(recorded) != set(expected):
        raise VerificationError("experiment report source inventory mismatch")
    for name, content in expected.items():
        item = recorded[name]
        if (item["sha256"] != sha256_bytes(content)
                or item["untrusted_source_text"].encode("utf-8") != content):
            raise VerificationError("experiment report source differs from candidate")
    return report
