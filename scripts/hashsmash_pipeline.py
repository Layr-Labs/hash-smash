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
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from judge.bedrock_adapter import BedrockClient, BedrockConfig, bedrock_system_prompt  # noqa: E402
from judge.committee import (  # noqa: E402
    DEFAULT_BEDROCK_COMMITTEE_PATH,
    DEFAULT_COMMITTEE_PATH,
    load_committee,
    member_client_config,
    run_committee,
)
from judge.prompts import (  # noqa: E402
    QUALIFICATION_POLICY_ID, load_qualification_policy, load_system_prompt,
)
from judge.provider_adapter import OpenRouterClient, OpenRouterConfig  # noqa: E402
from judge.run_review import run_mvp  # noqa: E402
from judge.paired_review import run_paired_review, select_lane_aggregate  # noqa: E402
from judge.lanes import LANE_STAGES, POLICY_ID as PAIRED_POLICY_ID  # noqa: E402
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
from verifier.tracks import Track, get_track  # noqa: E402
from verifier.experiment_evidence import execute as execute_experiments, validate_stored as validate_experiment_evidence  # noqa: E402
from experiments import ExperimentError, ExperimentSetupError, judge_view  # noqa: E402
from scripts.local_state import TrackBusyError, track_session  # noqa: E402


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


@dataclass(frozen=True)
class RunPaths:
    candidate: Path
    work: Path
    reports: Path
    score: Path
    evidence: Path
    dossier: Path
    aggregate: Path
    track: Track | None = None

    @property
    def generated(self) -> tuple[Path, ...]:
        return (self.score, self.work / "intake-report.json", self.work / "proof-numbered.md",
                self.work / "certificate-report.json", self.evidence, self.dossier, self.aggregate,
                *((self.work / "experiment-report.json",) if getattr(self.track, "lane", None) else ()))

    @classmethod
    def for_track(cls, track: Track, *, state_root: Path | None = None, candidate: Path | None = None) -> "RunPaths":
        root = state_root if state_root is not None else getattr(track, "state_root", REPO_ROOT / ".yukon")
        work, reports = root / "work" / "tracks" / track.id, root / "reports" / "tracks" / track.id
        return cls(candidate if candidate is not None else track.candidate,
                   work, reports, root / "scores" / f"{track.id}.json",
                   work / "judge-evidence.json", reports / "judge-dossier.json",
                   reports / "aggregate.json", track)


def _paths(paths: RunPaths | None) -> RunPaths:
    # Legacy default remains unchanged for the existing single-track Yukon workflow.
    return paths or RunPaths(CANDIDATE_ROOT, WORK_ROOT, REPORT_ROOT, SCORE_PATH,
                             EVIDENCE_PATH, DOSSIER_PATH, AGGREGATE_PATH)


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = load_json_bytes(path.read_bytes(), _display_path(path))
    except OSError as error:
        raise VerificationError(f"could not read {_display_path(path)}: {error}") from error
    if not isinstance(value, dict):
        raise VerificationError(f"{_display_path(path)}: JSON root must be an object")
    return value


def _remove_known_outputs(paths: Sequence[Path]) -> None:
    """Remove only enumerated generated files so a failed run cannot reuse stale state."""

    for path in paths:
        path.unlink(missing_ok=True)


def _build_evidence(
    intake_report: Mapping[str, Any], certificate_report: Mapping[str, Any], paths: RunPaths | None = None,
) -> dict[str, Any]:
    p = _paths(paths)
    try:
        numbered_proof = (p.work / "proof-numbered.md").read_text(encoding="utf-8")
    except OSError as error:
        raise VerificationError(f"could not read numbered proof: {error}") from error
    if sha256_bytes(numbered_proof.encode()) != intake_report["proof"]["line_numbered_sha256"]:
        raise VerificationError("numbered proof does not match current intake")
    if intake_report["package_sha256"] != certificate_report["package_sha256"]:
        raise VerificationError("candidate changed between intake and certificate verification")
    evidence = {
        "schema_version": "hashsmash-evidence-v1",
        "submission": {
            "intake_report": dict(intake_report),
            "proof_markdown_line_numbered": numbered_proof,
            "certificate_report": dict(certificate_report),
        },
        "benchmark": p.track.benchmark() if p.track else {
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
    if getattr(p.track, "lane", None):
        report = _load_json(p.work / "experiment-report.json")
        if intake_report["submission_state"] == "ready":
            validate_experiment_evidence(report, p.candidate, intake_report, p.track)
        if report["execution"] is not None:
            report = {**report, "execution": judge_view(report["execution"])}
        evidence["submission"]["experiment_report"] = report
    if len(canonical_json_bytes(evidence)) > 512 * 1024:
        raise VerificationError("judge evidence exceeds the 512 KiB review budget")
    return evidence


def run_intake(paths: RunPaths | None = None) -> int:
    p = _paths(paths)
    _remove_known_outputs(p.generated)
    intake_report = validate_candidate(p.candidate, p.work, track=p.track)
    certificate_report = verify_certificates(
        p.candidate, p.work / "certificate-report.json", track=p.track,
    )
    if getattr(p.track, "lane", None):
        experiment_report = execute_experiments(p.candidate, intake_report, p.track,
                                               holdout_nonce=os.environ.get("HASHSMASH_EXPERIMENT_HOLDOUT_NONCE"))
        atomic_write_json(p.work / "experiment-report.json", experiment_report)
    evidence = _build_evidence(intake_report, certificate_report, p)
    atomic_write_json(p.evidence, evidence)
    draft = p.track is not None and intake_report["submission_state"] == "draft"
    print(
        json.dumps(
            {
                "status": "draft_not_submitted" if draft else "mechanically_valid",
                "package_sha256": intake_report["package_sha256"],
                "certificates_verified": len(certificate_report["certificates"]),
                "evidence": _display_path(p.evidence),
            },
            sort_keys=True,
        )
    )
    return 2 if draft else 0


def _safe_config(config: Any, *, paired: bool = False) -> dict[str, Any]:
    value = asdict(config)
    value.pop("api_key", None)
    value["qualification_policy_id"] = PAIRED_POLICY_ID if paired else QUALIFICATION_POLICY_ID
    value["qualification_policy_sha256"] = sha256_bytes(
        (REPO_ROOT / "judge" / "policies" / "paired-lanes-v1.md").read_bytes() if paired else load_qualification_policy().encode("utf-8")
    )
    value["prompt_sha256"] = {
        stage: sha256_bytes(
            (bedrock_system_prompt(config, stage) if isinstance(config, BedrockConfig)
             else load_system_prompt(stage, config.strategy)).encode("utf-8")
        )
        for stage in (LANE_STAGES if paired else ("triage", "correctness", "complexity"))
    }
    if isinstance(config, BedrockConfig):
        value["api"] = config.api
        value["endpoint"] = config.endpoint
    value["review_schema_sha256"] = sha256_bytes(
        (REPO_ROOT / "schemas" / ("review-lanes-v1.schema.json" if paired else "review-v1.schema.json")).read_bytes()
    )
    if paired:
        value["aggregation_sha256"] = sha256_bytes(canonical_json_bytes({
            name: sha256_bytes((REPO_ROOT / "judge" / name).read_bytes())
            for name in ("lanes.py", "paired_review.py", "schema_validation.py")
        }))
    return value


def _provider_from_env() -> tuple[str, Any, Any]:
    provider = os.environ.get("HASHSMASH_JUDGE_PROVIDER", "openrouter").strip().lower()
    if provider == "openrouter":
        return provider, OpenRouterConfig.from_env(), OpenRouterClient
    if provider == "bedrock":
        return provider, BedrockConfig.from_env(), BedrockClient
    raise ValueError("HASHSMASH_JUDGE_PROVIDER must be 'openrouter' or 'bedrock'")


def _write_infrastructure_failure(reason: str, paths: RunPaths | None = None) -> None:
    p = _paths(paths)
    aggregate = {
        "status": "judge_infra_failed",
        "reasons": [reason],
        "claim": None,
        "recomputed_cost": None,
    }
    atomic_write_json(p.aggregate, aggregate)
    atomic_write_json(
        p.dossier,
        {
            "schema_version": "judge-dossier-v1",
            "aggregate": aggregate,
            "reviews": {},
            "provenance": {},
            "infrastructure_failures": {"configuration": reason},
        },
    )


def _check_current_evidence(p: RunPaths, evidence: Mapping[str, Any]) -> None:
    if p.track is None:
        return
    intake = validate_candidate(p.candidate, track=p.track)
    if intake["submission_state"] != "ready":
        raise VerificationError("draft templates are not submitted to the judge")
    certificates = verify_certificates(p.candidate, track=p.track)
    current = _build_evidence(intake, certificates, p)
    if canonical_json_bytes(current) != canonical_json_bytes(evidence):
        raise VerificationError("stale or mismatched evidence: rerun intake for this track")


def run_judge(paths: RunPaths | None = None) -> int:
    p = _paths(paths)
    _remove_known_outputs((p.score, p.dossier, p.aggregate))
    evidence = _load_json(p.evidence)
    _check_current_evidence(p, evidence)
    try:
        provider, base_config, client_factory = _provider_from_env()
        mode = os.environ.get("HASHSMASH_JUDGE_MODE", "single").strip().lower()
        paired = bool(getattr(p.track, "lane", None))
        if paired:
            from judge.role_committee import build_role_clients
            role_clients, committee_record = build_role_clients(base_config, client_factory, mode=mode)
            safe_config = {"mode": mode, "provider": provider,
                           "judge": _safe_config(base_config, paired=True),
                           "role_committee": committee_record}
            dossier = run_paired_review(evidence, client_factory(base_config), role_clients=role_clients)
            dossier["aggregate"] = select_lane_aggregate(dossier, p.track.lane)
            judge_label = f"paired:{provider}:{base_config.model}"
        elif mode == "single":
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
        _write_infrastructure_failure(reason, p)
        print(json.dumps({"status": "judge_infra_failed", "reason": reason}, sort_keys=True))
        return 3

    aggregate = dict(dossier["aggregate"])
    if p.track:
        safe_config["track_id"] = p.track.id
        safe_config["target_config_sha256"] = p.track.config_sha256()
        claim_schema = "claim-frontier-v3.schema.json" if paired else "claim-local-v2.schema.json"
        safe_config["claim_schema_sha256"] = sha256_bytes((REPO_ROOT / "schemas" / claim_schema).read_bytes())
        safe_config["certificate_schema_sha256"] = sha256_bytes((REPO_ROOT / "schemas" / "certificate-manifest-local-v2.schema.json").read_bytes())
        aggregate["input_package_sha256"] = evidence["submission"]["intake_report"]["package_sha256"]
        aggregate["target_config_sha256"] = p.track.config_sha256()
        aggregate["judge_evidence_sha256"] = sha256_bytes(canonical_json_bytes(evidence))
    config_hash = sha256_bytes(canonical_json_bytes(safe_config))
    dossier_core = {key: value for key, value in dossier.items() if key != "aggregate"}
    dossier_core["judge_configuration_sha256"] = config_hash
    aggregate["judge_config_sha256"] = config_hash
    aggregate["dossier_sha256"] = sha256_bytes(canonical_json_bytes(dossier_core))
    dossier["aggregate"] = aggregate
    dossier["judge_configuration"] = safe_config

    atomic_write_json(p.dossier, dossier)
    atomic_write_json(p.aggregate, aggregate)
    status = aggregate["status"]
    print(
        json.dumps(
            {
                "status": status,
                "judge": judge_label,
                "dossier": _display_path(p.dossier),
            },
            sort_keys=True,
        )
    )
    if status in ("ai_qualified", "plausible_not_refuted", "ai_rigor_qualified"):
        return 0
    if status in ("judge_infra_failed", "infra_failed"):
        return 3
    return 2


def run_score(paths: RunPaths | None = None) -> int:
    p = _paths(paths)
    p.score.unlink(missing_ok=True)
    aggregate = _load_json(p.aggregate)
    if p.track:
        evidence = _load_json(p.evidence)
        _check_current_evidence(p, evidence)
        if aggregate.get("judge_evidence_sha256") != sha256_bytes(canonical_json_bytes(evidence)):
            raise VerificationError("judge aggregate does not bind this evidence")
        if getattr(p.track, "lane", None):
            from judge.paired_review import aggregate_paired_reviews, evidence_binding
            dossier = _load_json(p.dossier)
            binding = evidence_binding(evidence)
            if dossier.get("binding") != binding or dossier.get("claim") != evidence["submission"]["intake_report"]["claim"]:
                raise VerificationError("paired dossier does not bind this exact evidence and claim")
            config_hash = sha256_bytes(canonical_json_bytes(dossier["judge_configuration"]))
            core = {key: value for key, value in dossier.items() if key not in ("aggregate", "judge_configuration")}
            core["judge_configuration_sha256"] = config_hash
            if (aggregate.get("judge_config_sha256") != config_hash
                    or aggregate.get("dossier_sha256") != sha256_bytes(canonical_json_bytes(core))
                    or dossier.get("aggregate") != aggregate):
                raise VerificationError("paired dossier/configuration integrity mismatch")
            outcomes = aggregate_paired_reviews(dossier["reviews"], binding=binding,
                claim=evidence["submission"]["intake_report"]["claim"],
                infrastructure_failures=dossier.get("infrastructure_failures"))
            if outcomes != dossier["lanes"]:
                raise VerificationError("stored paired decisions differ from deterministic aggregation")
            selected = select_lane_aggregate(dossier, p.track.lane)
            if any(aggregate.get(key) != value for key, value in selected.items()):
                raise VerificationError("score aggregate differs from selected lane dossier")
    score = build_score(p.candidate, aggregate, p.score, track=p.track)
    print(
        json.dumps(
            {
                "status": "scored",
                "score": score["score"],
                "output": _display_path(p.score),
            },
            sort_keys=True,
        )
    )
    return 0


def render_summary(paths: RunPaths | None = None) -> str:
    p = _paths(paths)
    aggregate = _load_json(p.aggregate)
    lines = ["## HashSmash review", "", f"Status: `{aggregate['status']}`"]
    if p.score.exists():
        score = _load_json(p.score)
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


def run_all(paths: RunPaths | None = None) -> int:
    p = _paths(paths)
    intake_status = run_intake(p)
    if intake_status:
        return intake_status
    judge_status = run_judge(p)
    if judge_status:
        print(render_summary(p), end="")
        return judge_status
    score_status = run_score(p)
    print(render_summary(p), end="")
    return score_status


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the HashSmash Yukon MVP")
    parser.add_argument("command", choices=("intake", "judge", "score", "summary", "all"))
    parser.add_argument("--track", help="explicit local track; omission keeps the legacy Yukon pilot")
    return parser.parse_args(argv)


def _execute(command: str, p: RunPaths, record: dict | None = None) -> int:
    try:
        if command == "intake":
            return run_intake(p)
        if command == "judge":
            return run_judge(p)
        if command == "score":
            return run_score(p)
        if command == "summary":
            print(render_summary(p), end="")
            return 0
        return run_all(p)
    except ExperimentSetupError as error:
        p.score.unlink(missing_ok=True)
        if record is not None:
            record.update(error_category="experiment_setup_failed", error=str(error))
        print(f"experiment dev setup unavailable: {error}", file=sys.stderr)
        return 3
    except (VerificationError, ExperimentError) as error:
        p.score.unlink(missing_ok=True)
        if record is not None:
            record.update(error_category="verification_failed", error=str(error))
        print(f"verification failed: {error}", file=sys.stderr)
        return 2
    except OSError as error:
        p.score.unlink(missing_ok=True)
        if record is not None:
            record.update(error_category="infrastructure_failed", error=str(error))
        print(f"pipeline infrastructure error: {error}", file=sys.stderr)
        return 3


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        p = RunPaths.for_track(get_track(args.track)) if args.track else _paths(None)
        with track_session(p, args.command) as record:
            result = _execute(args.command, p, record)
            record["exit_code"] = result
            return result
    except (TrackBusyError, VerificationError, OSError) as error:
        # Unknown tracks and lock failures must not erase another run's score.
        print(f"local run unavailable: {error}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
