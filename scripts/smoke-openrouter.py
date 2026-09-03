#!/usr/bin/env python3
"""Run one live structured judge stage without scoring."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import replace
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from judge.provider_adapter import JudgeInfraError, OpenRouterClient, OpenRouterConfig


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("triage", "correctness", "complexity"), default="triage")
    parser.add_argument("--model")
    parser.add_argument("--strategy")
    parser.add_argument("--reasoning-effort")
    parser.add_argument("--max-tokens", type=int)
    parser.add_argument("--max-attempts", type=int)
    parser.add_argument("--timeout-seconds", type=float)
    args = parser.parse_args()
    evidence_path = REPO_ROOT / ".yukon" / "work" / "judge-evidence.json"
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    config = OpenRouterConfig.from_env()
    overrides = {
        field: value
        for field, value in {
            "model": args.model,
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
        result = OpenRouterClient(config).review(args.stage, evidence)
    except JudgeInfraError as error:
        print(json.dumps({"status": "judge_infra_failed", "reason": str(error)}))
        return 3
    print(
        json.dumps(
            {
                "status": "ok",
                "stage": result.review["stage"],
                "decision": result.review["decision"],
                "verdict": result.review["verdict"],
                "issues": len(result.review["issues"]),
                "requested_model": result.provenance["requested_model"],
                "returned_model": result.provenance["returned_model"],
                "attempts": result.provenance["attempts"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
