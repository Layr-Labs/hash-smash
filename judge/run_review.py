"""CLI and library entry point for the three-review HashSmash MVP."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from dataclasses import replace
from pathlib import Path
from typing import Any, Mapping, Protocol, Sequence

from .aggregate import REQUIRED_STAGES, aggregate_reviews
from .provider_adapter import JudgeInfraError, OpenRouterClient, OpenRouterConfig, ReviewResult


class ReviewClient(Protocol):
    def review(self, stage: str, evidence: Mapping[str, Any]) -> ReviewResult: ...


def run_independent_reviews(
    evidence: Mapping[str, Any],
    client: ReviewClient,
    *,
    stages: Sequence[str] = REQUIRED_STAGES,
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], dict[str, str]]:
    """Run stages independently; no specialist receives another stage's output."""

    reviews: dict[str, dict[str, Any]] = {}
    provenance: dict[str, dict[str, Any]] = {}
    failures: dict[str, str] = {}
    for stage in stages:
        try:
            result: ReviewResult = client.review(stage, evidence)
        except JudgeInfraError as exc:
            failures[stage] = f"{exc} (attempts={exc.attempts})"
            continue
        reviews[stage] = result.review
        provenance[stage] = result.provenance
    return reviews, provenance, failures


def run_mvp(
    evidence: Mapping[str, Any], client: ReviewClient
) -> dict[str, Any]:
    """Run triage/correctness/complexity independently and aggregate them.

    This is the importable high-level MVP API. The returned dossier's authoritative
    outcome is ``dossier["aggregate"]["status"]``.
    """
    reviews, provenance, failures = run_independent_reviews(evidence, client)
    expected_claim = None
    try:
        candidate_claim = evidence["submission"]["intake_report"]["claim"]
        if isinstance(candidate_claim, Mapping):
            expected_claim = candidate_claim
    except (KeyError, TypeError):
        pass
    aggregate = aggregate_reviews(
        reviews,
        infrastructure_failures=failures,
        expected_claim=expected_claim,
    )
    return {
        "schema_version": "judge-dossier-v1",
        "aggregate": aggregate,
        "reviews": reviews,
        "provenance": provenance,
        "infrastructure_failures": failures,
    }


def _atomic_json_write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the HashSmash AI judge")
    parser.add_argument("--evidence", type=Path, required=True, help="trusted JSON evidence envelope")
    parser.add_argument("--output", type=Path, required=True, help="judge dossier JSON path")
    parser.add_argument("--model", help="provider model override")
    parser.add_argument(
        "--provider",
        choices=("openrouter", "bedrock"),
        default=os.environ.get("HASHSMASH_JUDGE_PROVIDER", "openrouter"),
    )
    parser.add_argument("--max-attempts", type=int, help="bounded attempts per review")
    parser.add_argument("--timeout-seconds", type=float, help="HTTP timeout per attempt")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    with args.evidence.open("r", encoding="utf-8") as handle:
        evidence = json.load(handle)
    if not isinstance(evidence, dict):
        raise SystemExit("evidence JSON root must be an object")

    if args.provider == "bedrock":
        from .bedrock_adapter import BedrockClient, BedrockConfig

        config = BedrockConfig.from_env()
        client_factory = BedrockClient
    else:
        config = OpenRouterConfig.from_env()
        client_factory = OpenRouterClient
    overrides: dict[str, Any] = {}
    if args.model:
        overrides["model"] = args.model
    if args.max_attempts is not None:
        overrides["max_attempts"] = args.max_attempts
    if args.timeout_seconds is not None:
        overrides["timeout_seconds"] = args.timeout_seconds
    if overrides:
        config = replace(config, **overrides)

    dossier = run_mvp(evidence, client_factory(config))
    _atomic_json_write(args.output, dossier)
    status = dossier["aggregate"]["status"]
    print(json.dumps({"status": status, "output": str(args.output)}))
    if status == "ai_qualified":
        return 0
    if status == "judge_infra_failed":
        return 3
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
