#!/usr/bin/env python3
"""Real participant-Python pipeline calibration, with separate trust phases.

Prepare runs only the immutable organizer fixture through production intake and
Docker. Review never executes participant code and makes at most six provider
calls, each with one transport attempt. No registered target/baseline is changed.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from dataclasses import replace
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import shutil
import sys
from typing import Any
import uuid

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from experiments import ExperimentError, ExperimentSetupError
from judge.bedrock_adapter import BedrockClient, BedrockConfig
from judge.lanes import LANE_STAGES
from judge.provider_adapter import JudgeInfraError, OpenRouterClient, OpenRouterConfig
from scripts import hashsmash_pipeline as pipeline
from verifier.errors import VerificationError
from verifier.frontier_tracks import LaneTrack
from verifier.intake import validate_candidate
from verifier.io import atomic_write_json, canonical_json_bytes, load_json_bytes, sha256_bytes

FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "participant-heuristic"
REPORT_ROOT = REPO_ROOT / ".yukon" / "reports" / "participant-heuristic"
TRACK_ID = "calibration-md5-s8-exploratory"
TARGET_PROFILE = "md5-s8-prefix-v1"
FIXTURE_ID = "participant-birthday-heuristic-v1"
EXPERIMENT_ID = "birthday-batches"
PREPARE_FILENAME = "prepared-run.json"
RESULT_FILENAME = "result.json"
CREDENTIAL_NAMES = (
    "OPENROUTER_API_KEY", "AWS_BEARER_TOKEN_BEDROCK",
    "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN",
    "AWS_SECURITY_TOKEN", "AWS_PROFILE", "AWS_DEFAULT_PROFILE",
    "AWS_WEB_IDENTITY_TOKEN_FILE", "AWS_CONTAINER_CREDENTIALS_RELATIVE_URI",
    "AWS_CONTAINER_CREDENTIALS_FULL_URI", "AWS_CONTAINER_AUTHORIZATION_TOKEN",
    "AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE", "GITHUB_TOKEN", "GH_TOKEN",
)


def _json(path: Path) -> dict[str, Any]:
    value = load_json_bytes(path.read_bytes(), str(path))
    if not isinstance(value, dict):
        raise VerificationError("calibration artifact must be a JSON object")
    return value


def instantiated_claim_schema() -> dict[str, Any]:
    """Explicit organizer test instance: change only the allowed target enum."""
    schema = _json(REPO_ROOT / "schemas" / "claim-frontier-v3.schema.json")
    schema["properties"]["target_profile"]["enum"] = [TARGET_PROFILE]
    return schema


def fixture_hashes() -> dict[str, str]:
    return {str(path.relative_to(FIXTURE_ROOT)): sha256_bytes(path.read_bytes())
            for path in sorted(FIXTURE_ROOT.rglob("*")) if path.is_file()}


class CalibrationTrack(LaneTrack):
    """Never registered: exact existing hash, paired policy, isolated score path."""

    def benchmark(self) -> dict[str, Any]:
        benchmark = super().benchmark()
        schema_path = REPO_ROOT / "schemas" / "claim-frontier-v3.schema.json"
        benchmark["calibration"] = {
            "id": FIXTURE_ID,
            "calibration_only": True,
            "registered_frontier_track": False,
            "is_qualified_baseline": False,
            "meaning": "Noncompetitive integration fixture; any score is diagnostic only.",
            "claim_schema": {
                "base_path": "schemas/claim-frontier-v3.schema.json",
                "base_sha256": sha256_bytes(schema_path.read_bytes()),
                "change": "Only properties.target_profile.enum is instantiated as [md5-s8-prefix-v1].",
                "instantiated_sha256": sha256_bytes(canonical_json_bytes(instantiated_claim_schema())),
                "production_validator": "verifier.schema_validation.validate_claim with organizer-selected exact track; unchanged",
            },
            "driver_sha256": sha256_bytes(Path(__file__).read_bytes()),
            "fixture_sha256": fixture_hashes(),
        }
        return benchmark


def calibration_track() -> CalibrationTrack:
    return CalibrationTrack(
        id=TRACK_ID, algorithm="md5", rounds=8, difficulty="calibration-only",
        purpose="Full participant-Python heuristic pipeline integration; not competitive research.",
        lane="exploratory", target_id="md5-s8", output_bits=128,
        nominal_security_bits=64, selection_status="calibration-only",
        boundary_role="not-a-frontier-boundary",
    )


def paths_for(run_directory: Path) -> pipeline.RunPaths:
    # These paths can never be the active/legacy output paths, even if callers
    # select a directory in the repository. The registry rejects TRACK_ID.
    return pipeline.RunPaths.for_track(calibration_track(),
        state_root=run_directory / "calibration-state",
        candidate=run_directory / "participant-package")


def require_credential_free() -> None:
    if any(os.environ.get(name) for name in CREDENTIAL_NAMES):
        raise VerificationError("prepare refuses a credential-bearing environment; start a separate secret-free process")


def _fresh_directory(path: Path | None) -> Path:
    if path is None:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        path = REPORT_ROOT / f"{stamp}-{uuid.uuid4().hex[:8]}"
    path = path.expanduser().absolute()
    if path.exists() or path.is_symlink():
        raise VerificationError("prepare requires a fresh nonexistent run directory")
    path.mkdir(parents=True, exist_ok=False)
    return path.resolve()


def _load_prepared(run_directory: Path) -> tuple[dict[str, Any], pipeline.RunPaths]:
    run_directory = run_directory.resolve(strict=True)
    prepared = _json(run_directory / PREPARE_FILENAME)
    paths = paths_for(run_directory)
    if (prepared.get("schema_version") != "participant-heuristic-prepared-v1"
            or prepared.get("fixture_id") != FIXTURE_ID
            or prepared.get("status") != "prepared"
            or prepared.get("track_id") != TRACK_ID
            or prepared.get("target_config_sha256") != paths.track.config_sha256()
            or prepared.get("fixture_sha256") != fixture_hashes()):
        raise VerificationError("prepared run does not match the current frozen fixture/configuration")
    schema = _json(run_directory / "claim-test-instance.schema.json")
    if canonical_json_bytes(schema) != canonical_json_bytes(instantiated_claim_schema()):
        raise VerificationError("test-only schema instance changed after preparation")
    current = validate_candidate(paths.candidate, track=paths.track)
    if current["package_sha256"] != prepared.get("package_sha256"):
        raise VerificationError("participant package changed after preparation")
    if sha256_bytes(paths.evidence.read_bytes()) != prepared.get("evidence_file_sha256"):
        raise VerificationError("trusted judge evidence changed after preparation")
    # This rebuilds current intake/certificates and validates stored full
    # experiments. It never runs a submitted program.
    pipeline._check_current_evidence(paths, _json(paths.evidence))
    return prepared, paths


def prepare_run(run_directory: Path | None = None) -> dict[str, Any]:
    require_credential_free()
    if "HASHSMASH_EXPERIMENT_HOLDOUT_NONCE" in os.environ:
        raise VerificationError("this frozen public-seed fixture does not accept a holdout override")
    run_directory = _fresh_directory(run_directory)
    paths = paths_for(run_directory)
    shutil.copytree(FIXTURE_ROOT / "candidate", paths.candidate)
    atomic_write_json(run_directory / "claim-test-instance.schema.json", instantiated_claim_schema())
    # Commit the package/configuration before the first sample is executed.
    intake = validate_candidate(paths.candidate, track=paths.track)
    prepared = {
        "schema_version": "participant-heuristic-prepared-v1", "fixture_id": FIXTURE_ID,
        "status": "committed_before_execution", "track_id": TRACK_ID,
        "calibration_only": True, "is_qualified_baseline": False,
        "package_sha256": intake["package_sha256"],
        "target_config_sha256": paths.track.config_sha256(), "fixture_sha256": fixture_hashes(),
        "sample_protocol": "Frozen batch256, trials256, production public seed; no seed search or holdout claim.",
        "max_stage_calls": 6, "max_transport_attempts_per_stage": 1,
    }
    atomic_write_json(run_directory / PREPARE_FILENAME, prepared)
    result = pipeline.run_intake(paths)
    if result != 0:
        raise VerificationError("fixture failed genuine production intake")
    report = _json(paths.work / "experiment-report.json")["execution"]
    measured = report["experiments"][0]
    if report["target_profile"] != TARGET_PROFILE or measured["id"] != EXPERIMENT_ID:
        raise VerificationError("experiment target or ID mismatch")
    if measured["trials"] != 256 or len(measured["checked_trials"]) != 256:
        raise VerificationError("the frozen protocol requires every one of 256 trials")
    if measured["event"] != {"kind": "full-collision"}:
        raise VerificationError("fixture must check full collisions, not output masks")
    prepared.update(status="prepared", evidence_file_sha256=sha256_bytes(paths.evidence.read_bytes()),
                    experiment_report_sha256=report["report_sha256"])
    atomic_write_json(run_directory / PREPARE_FILENAME, prepared)
    return inspect_run(run_directory)


@contextmanager
def forbid_participant_execution():
    """Fail-safe in addition to the production judge/score no-execution design."""
    from experiments import runner
    from verifier import experiment_evidence

    def refuse(*_args, **_kwargs):
        raise VerificationError("participant execution is forbidden during credential-bearing review")

    slots = ((pipeline, "execute_experiments"), (experiment_evidence, "run_experiments"), (runner, "_run_docker"))
    saved = [(module, name, getattr(module, name)) for module, name in slots]
    try:
        for module, name, _ in saved:
            setattr(module, name, refuse)
        yield
    finally:
        for module, name, original in saved:
            setattr(module, name, original)


@contextmanager
def _provider_selection(provider: str, config: Any, client_factory: Any):
    """Inject only trusted provider dependencies, never mechanical validators."""
    saved_provider = pipeline._provider_from_env
    saved_mode = os.environ.get("HASHSMASH_JUDGE_MODE")
    count = {"calls": 0, "stages": []}

    class BoundedClient:
        def __init__(self, actual_config):
            self.client = client_factory(actual_config)

        def review(self, stage, evidence):
            if count["calls"] >= 6 or stage not in LANE_STAGES or stage in count["stages"]:
                raise JudgeInfraError("finite calibration stage budget exceeded")
            count["calls"] += 1
            count["stages"].append(stage)
            return self.client.review(stage, evidence)

    try:
        pipeline._provider_from_env = lambda: (provider, config, BoundedClient)
        os.environ["HASHSMASH_JUDGE_MODE"] = "single"
        yield count
    finally:
        pipeline._provider_from_env = saved_provider
        if saved_mode is None:
            os.environ.pop("HASHSMASH_JUDGE_MODE", None)
        else:
            os.environ["HASHSMASH_JUDGE_MODE"] = saved_mode


def review_run(run_directory: Path, *, provider: str = "bedrock", model: str | None = None,
               max_tokens: int = 16384, timeout_seconds: float = 180.0,
               config: Any = None, client_factory: Any = None) -> dict[str, Any]:
    """Real adapters by default; explicit config/factory injection for offline tests."""
    if provider not in {"bedrock", "openrouter"}:
        raise ValueError("unsupported calibration provider")
    if not 1024 <= max_tokens <= 32768 or not 1 <= timeout_seconds <= 300:
        raise ValueError("provider limits outside finite calibration budget")
    run_directory = run_directory.resolve(strict=True)
    with forbid_participant_execution():
        prepared, paths = _load_prepared(run_directory)
        # Preserve every diagnostic result, including failures. Repeating a live
        # test requires a separate explicitly chosen run; no quiet overwrite.
        if (run_directory / "review-started.json").exists() or paths.dossier.exists():
            raise VerificationError("review already attempted; use a new run directory for an explicit repeat")
        factory = client_factory or (BedrockClient if provider == "bedrock" else OpenRouterClient)
        if config is None:
            config = BedrockConfig.from_env() if provider == "bedrock" else OpenRouterConfig.from_env()
        updates = {"max_attempts": 1, "max_tokens": max_tokens, "timeout_seconds": timeout_seconds}
        if model:
            updates["model"] = model
        config = replace(config, **updates)
        record = {
            "schema_version": "participant-heuristic-result-v1", "fixture_id": FIXTURE_ID,
            "calibration_only": True, "is_qualified_baseline": False,
            "provider": provider, "model": config.model, "max_stage_calls": 6,
            "max_transport_attempts_per_stage": 1, "package_sha256": prepared["package_sha256"],
            "experiment_report_sha256": prepared["experiment_report_sha256"],
            "interpretation": "One diagnostic, not a measured false-positive/false-negative rate. No target or baseline promotion.",
        }
        atomic_write_json(run_directory / "review-started.json", record)
        with _provider_selection(provider, config, factory) as count:
            judge_status = pipeline.run_judge(paths)
            # Invoke the real score gate even on a withheld verdict: it must
            # refuse rather than leave a stale diagnostic score behind.
            score_status = pipeline._execute("score", paths)
        dossier = _json(paths.dossier)
        outcomes = {lane: item["status"] for lane, item in dossier.get("lanes", {}).items()}
        record.update(judge_exit_code=judge_status, score_exit_code=score_status,
                      actual_stage_calls=count["calls"], stages=count["stages"],
                      outcomes=outcomes, diagnostic_score_emitted=paths.score.exists(),
                      diagnostic_score_path=str(paths.score) if paths.score.exists() else None,
                      expected_policy_diagnostic={"exploratory": "plausible_not_refuted", "rigorous": "not_qualified"},
                      outcome_matches_expected=outcomes == {"exploratory": "plausible_not_refuted", "rigorous": "not_qualified"})
        atomic_write_json(run_directory / RESULT_FILENAME, record)
    return inspect_run(run_directory)


def inspect_run(run_directory: Path) -> dict[str, Any]:
    prepared, paths = _load_prepared(run_directory)
    report = _json(paths.work / "experiment-report.json")["execution"]
    measured = report["experiments"][0]
    summary = {
        "run_directory": str(run_directory.resolve()), "fixture_id": FIXTURE_ID,
        "status": "prepared", "calibration_only": True, "registered_frontier_track": False,
        "target_profile": report["target_profile"], "trials": measured["trials"],
        "full_collisions": measured["successes"],
        "no_pair_returned": sum(row.get("reason") == "no_pair_returned" for row in measured["checked_trials"]),
        "observed_fraction": measured["successes"] / measured["trials"],
        "iid_model_probability_not_a_verified_target_probability": -math.expm1(sum(math.log1p(-j / 65536) for j in range(256))),
        "reproducibility": measured["reproducibility"],
        "package_sha256": prepared["package_sha256"],
        "experiment_report_sha256": report["report_sha256"],
        "evidence": str(paths.evidence), "full_experiment_report": str(paths.work / "experiment-report.json"),
    }
    if (run_directory / RESULT_FILENAME).exists():
        summary.update(status="reviewed", review=_json(run_directory / RESULT_FILENAME))
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "review", "inspect"))
    parser.add_argument("--run-directory", type=Path)
    parser.add_argument("--provider", choices=("bedrock", "openrouter"), default="bedrock")
    parser.add_argument("--model")
    parser.add_argument("--max-tokens", type=int, default=16384)
    parser.add_argument("--timeout-seconds", type=float, default=180.0)
    args = parser.parse_args(argv)
    if args.command != "prepare" and args.run_directory is None:
        parser.error("review/inspect require --run-directory")
    try:
        if args.command == "prepare":
            summary = prepare_run(args.run_directory)
        elif args.command == "review":
            summary = review_run(args.run_directory, provider=args.provider, model=args.model,
                                 max_tokens=args.max_tokens, timeout_seconds=args.timeout_seconds)
        else:
            summary = inspect_run(args.run_directory)
        print(json.dumps(summary, sort_keys=True), flush=True)
        if summary.get("review", {}).get("judge_exit_code") == 3:
            return 3
        return 0
    except ExperimentSetupError:
        print(json.dumps({"status": "experiment_setup_failed", "action": "Configure Docker and the pinned image in a secret-free process."}))
        return 3
    except (VerificationError, ExperimentError, ValueError, OSError) as error:
        # Exception text may come from an adapter; never echo credential values.
        print(json.dumps({"status": "calibration_failed", "error_type": type(error).__name__}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
