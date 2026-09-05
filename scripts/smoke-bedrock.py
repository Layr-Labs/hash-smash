#!/usr/bin/env python3
"""Run one live Bedrock structured judge stage without scoring."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import replace
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from judge.bedrock_adapter import BedrockClient, BedrockConfig
from judge.provider_adapter import JudgeInfraError

from judge.lanes import INITIAL_STAGES, POLICY_ID
from judge.paired_review import evidence_binding
from scripts.hashsmash_pipeline import RunPaths, _check_current_evidence, _load_json
from verifier.frontier_tracks import get_frontier_track


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--track", required=True, help="paired frontier track with current ready intake evidence")
    parser.add_argument("--stage", choices=INITIAL_STAGES, default="lane_evaluability")
    parser.add_argument("--model")
    parser.add_argument("--region")
    parser.add_argument("--strategy")
    parser.add_argument("--reasoning-effort")
    parser.add_argument("--max-tokens", type=int)
    parser.add_argument("--max-attempts", type=int)
    parser.add_argument("--timeout-seconds", type=float)
    args = parser.parse_args()
    paths = RunPaths.for_track(get_frontier_track(args.track))
    evidence = _load_json(paths.evidence)
    _check_current_evidence(paths, evidence)
    evidence["review_context"] = {"policy_id": POLICY_ID, "binding": evidence_binding(evidence)}
    config = BedrockConfig.from_env()
    overrides = {
        field: value
        for field, value in {
            "model": args.model,
            "region": args.region,
            "strategy": args.strategy,
            "reasoning_effort": args.reasoning_effort,
            "max_tokens": args.max_tokens,
            "max_attempts": args.max_attempts,
            "timeout_seconds": args.timeout_seconds,
        }.items()
        if value is not None
    }
    if overrides:
        config = replace(config, **overrides)
    try:
        result = BedrockClient(config).review(args.stage, evidence)
    except JudgeInfraError as error:
        print(json.dumps({"status": "judge_infra_failed", "reason": str(error)}))
        return 3
    print(
        json.dumps(
            {
                "status": "ok",
                "stage": result.review["stage"],
                "findings": len(result.review["findings"]),
                "obligations": len(result.review["obligations"]),
                "requested_model": result.provenance["requested_model"],
                "returned_model": result.provenance["returned_model"],
                "region": result.provenance["region"],
                "attempts": result.provenance["attempts"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
