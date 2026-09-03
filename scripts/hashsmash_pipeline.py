#!/usr/bin/env python3
"""End-to-end HashSmash MVP pipeline used locally and by Yukon.

The participant package is treated as untrusted throughout.  Only deterministic
organizer-owned code can create the final Yukon score.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from judge.bedrock_adapter import BedrockClient, BedrockConfig  # noqa: E402
from judge.committee import (  # noqa: E402
    DEFAULT_BEDROCK_COMMITTEE_PATH,
    DEFAULT_COMMITTEE_PATH,
    load_committee,
    member_client_config,
    run_committee,
)
from judge.prompts import load_system_prompt  # noqa: E402
from judge.provider_adapter import OpenRouterClient, OpenRouterConfig  # noqa: E402
from judge.run_review import run_mvp  # noqa: E402
from verifier.certificates import verify_certificates  # noqa: E402
from verifier.errors import VerificationError  # noqa: E402
from verifier.intake import validate_candidate  # noqa: E402
from verifier.io import (  # noqa: E402
    atomic_write_json,
    canonical_json_bytes,
    load_json_bytes,
    sha256_bytes,
)
from verifier.score import build_score  # noqa: E402


CANDIDATE_ROOT = REPO_ROOT / "candidate"
WORK_ROOT = REPO_ROOT / ".yukon" / "work"
REPORT_ROOT = REPO_ROOT / ".yukon" / "reports"
SCORE_PATH = REPO_ROOT / ".yukon" / "score.json"
EVIDENCE_PATH = WORK_ROOT / "judge-evidence.json"
DOSSIER_PATH = REPORT_ROOT / "judge-dossier.json"
AGGREGATE_PATH = REPORT_ROOT / "aggregate.json"

GENERATED_FILES = (
    SCORE_PATH,
    WORK_ROOT / "intake-report.json",
    WORK_ROOT / "proof-numbered.md",
    WORK_ROOT / "certificate-report.json",
    EVIDENCE_PATH,
    DOSSIER_PATH,
    AGGREGATE_PATH,
)


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = load_json_bytes(path.read_bytes(), str(path.relative_to(REPO_ROOT)))
    except OSError as error:
        raise VerificationError(f"could not read {path.relative_to(REPO_ROOT)}: {error}") from error
    if not isinstance(value, dict):
        raise VerificationError(f"{path.relative_to(REPO_ROOT)}: JSON root must be an object")
    return value


def _remove_known_outputs(paths: Sequence[Path]) -> None:
    """Remove only enumerated generated files so a failed run cannot reuse stale state."""

    for path in paths:
        path.unlink(missing_ok=True)


def _build_evidence(
    intake_report: Mapping[str, Any], certificate_report: Mapping[str, Any]
) -> dict[str, Any]:
    try:
        numbered_proof = (WORK_ROOT / "proof-numbered.md").read_text(encoding="utf-8")
    except OSError as error:
        raise VerificationError(f"could not read numbered proof: {error}") from error
    return {
        "schema_version": "hashsmash-evidence-v1",
        "submission": {
            "intake_report": dict(intake_report),
            "proof_markdown_line_numbered": numbered_proof,
            "certificate_report": dict(certificate_report),
        },
        "benchmark": {
            "target_profile": _load_json(
                REPO_ROOT / "target-profiles" / "sha1-fips180-4-v1.json"
            ),
            "cost_model": _load_json(
                REPO_ROOT / "cost-models" / "collision-cost-v1.json"
            ),
            "frontier": _load_json(
                REPO_ROOT / "frontier" / "sha1-full-collision-v1.json"
            ),
        },
    }


def run_intake() -> int:
    _remove_known_outputs(GENERATED_FILES)
    intake_report = validate_candidate(CANDIDATE_ROOT, WORK_ROOT)
    certificate_report = verify_certificates(
        CANDIDATE_ROOT, WORK_ROOT / "certificate-report.json"
    )
    evidence = _build_evidence(intake_report, certificate_report)
    atomic_write_json(EVIDENCE_PATH, evidence)
    print(
        json.dumps(
            {
                "status": "mechanically_valid",
                "package_sha256": intake_report["package_sha256"],
                "certificates_verified": len(certificate_report["certificates"]),
                "evidence": _display_path(EVIDENCE_PATH),
            },
            sort_keys=True,
        )
    )
    return 0


def _safe_config(config: Any) -> dict[str, Any]:
    value = asdict(config)
    value.pop("api_key", None)
    value["prompt_sha256"] = {
        stage: sha256_bytes(load_system_prompt(stage, config.strategy).encode("utf-8"))
        for stage in ("triage", "correctness", "complexity")
    }
    value["review_schema_sha256"] = sha256_bytes(
        (REPO_ROOT / "schemas" / "review-v1.schema.json").read_bytes()
    )
    return value


def _provider_from_env() -> tuple[str, Any, Any]:
    provider = os.environ.get("HASHSMASH_JUDGE_PROVIDER", "openrouter").strip().lower()
    if provider == "openrouter":
        return provider, OpenRouterConfig.from_env(), OpenRouterClient
    if provider == "bedrock":
        return provider, BedrockConfig.from_env(), BedrockClient
    raise ValueError("HASHSMASH_JUDGE_PROVIDER must be 'openrouter' or 'bedrock'")


def _write_infrastructure_failure(reason: str) -> None:
    aggregate = {
        "status": "judge_infra_failed",
        "reasons": [reason],
        "claim": None,
        "recomputed_cost": None,
    }
    atomic_write_json(AGGREGATE_PATH, aggregate)
    atomic_write_json(
        DOSSIER_PATH,
        {
            "schema_version": "judge-dossier-v1",
            "aggregate": aggregate,
            "reviews": {},
            "provenance": {},
            "infrastructure_failures": {"configuration": reason},
        },
    )


def run_judge() -> int:
    _remove_known_outputs((SCORE_PATH, DOSSIER_PATH, AGGREGATE_PATH))
    evidence = _load_json(EVIDENCE_PATH)
    try:
        provider, base_config, client_factory = _provider_from_env()
        mode = os.environ.get("HASHSMASH_JUDGE_MODE", "single").strip().lower()
        if mode == "single":
            safe_config: dict[str, Any] = {
                "mode": "single",
                "provider": provider,
                "judge": _safe_config(base_config),
            }
            dossier = run_mvp(evidence, client_factory(base_config))
            judge_label = f"{provider}:{base_config.model}"
        elif mode == "committee":
            default_committee_path = (
                DEFAULT_BEDROCK_COMMITTEE_PATH
                if provider == "bedrock"
                else DEFAULT_COMMITTEE_PATH
            )
            committee_path = Path(
                os.environ.get("HASHSMASH_COMMITTEE_PATH", str(default_committee_path))
            )
            committee = load_committee(committee_path)
            safe_config = {
                "mode": "committee",
                "provider": provider,
                "committee": asdict(committee),
                "members": {
                    member.id: _safe_config(member_client_config(base_config, member))
                    for member in committee.members
                },
            }
            def report_progress(member_id: str, member_status: str) -> None:
                print(
                    json.dumps(
                        {"committee_member": member_id, "status": member_status},
                        sort_keys=True,
                    ),
                    flush=True,
                )

            dossier = run_committee(
                evidence,
                committee,
                base_config,
                client_factory=client_factory,
                progress=report_progress,
            )
            judge_label = f"committee:{provider}:{committee.committee_id}"
        else:
            raise ValueError("HASHSMASH_JUDGE_MODE must be 'single' or 'committee'")
    except (OSError, ValueError) as error:
        reason = f"judge configuration failed: {type(error).__name__}: {error}"
        _write_infrastructure_failure(reason)
        print(json.dumps({"status": "judge_infra_failed", "reason": reason}, sort_keys=True))
        return 3

    aggregate = dict(dossier["aggregate"])
    config_hash = sha256_bytes(canonical_json_bytes(safe_config))
    dossier_core = {key: value for key, value in dossier.items() if key != "aggregate"}
    dossier_core["judge_configuration_sha256"] = config_hash
    aggregate["judge_config_sha256"] = config_hash
    aggregate["dossier_sha256"] = sha256_bytes(canonical_json_bytes(dossier_core))
    dossier["aggregate"] = aggregate
    dossier["judge_configuration"] = safe_config

    atomic_write_json(DOSSIER_PATH, dossier)
    atomic_write_json(AGGREGATE_PATH, aggregate)
    status = aggregate["status"]
    print(
        json.dumps(
            {
                "status": status,
                "judge": judge_label,
                "dossier": _display_path(DOSSIER_PATH),
            },
            sort_keys=True,
        )
    )
    if status == "ai_qualified":
        return 0
    if status == "judge_infra_failed":
        return 3
    return 2


def run_score() -> int:
    SCORE_PATH.unlink(missing_ok=True)
    aggregate = _load_json(AGGREGATE_PATH)
    score = build_score(CANDIDATE_ROOT, aggregate, SCORE_PATH)
    print(
        json.dumps(
            {
                "status": "scored",
                "score": score["score"],
                "output": _display_path(SCORE_PATH),
            },
            sort_keys=True,
        )
    )
    return 0


def render_summary() -> str:
    aggregate = _load_json(AGGREGATE_PATH)
    lines = ["## HashSmash review", "", f"Status: `{aggregate['status']}`"]
    if SCORE_PATH.exists():
        score = _load_json(SCORE_PATH)
        lines.extend(("", f"Yukon score: `{score['score']}` (lower is better)"))
    reasons = aggregate.get("reasons")
    if isinstance(reasons, list) and reasons:
        lines.extend(("", "Reasons:"))
        lines.extend(f"- {reason}" for reason in reasons)
    lines.extend(
        (
            "",
            "This is an AI screening result, not formal verification or human acceptance.",
        )
    )
    return "\n".join(lines) + "\n"


def run_all() -> int:
    intake_status = run_intake()
    if intake_status:
        return intake_status
    judge_status = run_judge()
    if judge_status:
        print(render_summary(), end="")
        return judge_status
    score_status = run_score()
    print(render_summary(), end="")
    return score_status


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the HashSmash Yukon MVP")
    parser.add_argument("command", choices=("intake", "judge", "score", "summary", "all"))
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        if args.command == "intake":
            return run_intake()
        if args.command == "judge":
            return run_judge()
        if args.command == "score":
            return run_score()
        if args.command == "summary":
            print(render_summary(), end="")
            return 0
        return run_all()
    except VerificationError as error:
        SCORE_PATH.unlink(missing_ok=True)
        print(f"verification failed: {error}", file=sys.stderr)
        return 2
    except OSError as error:
        SCORE_PATH.unlink(missing_ok=True)
        print(f"pipeline infrastructure error: {error}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
