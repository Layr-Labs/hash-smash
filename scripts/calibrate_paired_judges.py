#!/usr/bin/env python3
"""Finite organizer toy-target calibration for real paired judge providers.

Credentials come only from the inherited process environment. Every case is an
organizer fixture; no participant source or challenge candidate is loaded. Output
is diagnostic evidence/dossiers only, and never a score or qualified baseline.
"""

from __future__ import annotations

import argparse
from dataclasses import replace
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import random
import sys
from typing import Any, Mapping
import uuid

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from judge.bedrock_adapter import BedrockClient, BedrockConfig
from judge.lanes import LANE_STAGES
from judge.paired_review import run_paired_review
from judge.provider_adapter import OpenRouterClient, OpenRouterConfig
from judge.role_committee import build_role_clients
from verifier.io import atomic_write_json, canonical_json_bytes

FIXTURE_DIR = REPO_ROOT / "tests/fixtures/paired-calibration"
REPORT_DIR = REPO_ROOT / ".yukon/reports/paired-calibration"
CASES = ("positive", "false-proof", "heuristic")
EXPECTED = {
    "positive": {"exploratory": ["plausible_not_refuted"], "rigorous": ["ai_rigor_qualified"]},
    "false-proof": {"exploratory": ["refuted"], "rigorous": ["refuted"]},
    "heuristic": {"exploratory": ["plausible_not_refuted"], "rigorous": ["not_qualified"]},
}


def _digest(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def toy_projection(message: bytes) -> int:
    if len(message) != 2:
        raise ValueError("projection fixture requires exactly two bytes")
    return message[0] & 15


def toy_prefix10(message: bytes) -> int:
    if len(message) != 3:
        raise ValueError("prefix fixture requires exactly three bytes")
    return int.from_bytes(hashlib.sha256(message).digest()[:2], "big") >> 6


def heuristic_experiment() -> dict[str, Any]:
    """Small trusted organizer computation; never executes submitted source."""
    rng = random.Random(2026)
    trials = []
    for index in range(32):
        messages = [rng.randrange(1 << 24).to_bytes(3, "big") for _ in range(32)]
        outputs = [toy_prefix10(message) for message in messages]
        collisions = [(i, j) for i in range(32) for j in range(i + 1, 32)
                      if messages[i] != messages[j] and outputs[i] == outputs[j]]
        trials.append({
            "trial_index": index, "messages_hex": [message.hex() for message in messages],
            "outputs": outputs, "success": bool(collisions),
            "witness_indices": list(collisions[0]) if collisions else [],
        })
    successes, count = sum(item["success"] for item in trials), len(trials)
    frequency, z = successes / count, 1.959963984540054
    denominator = 1 + z * z / count
    center = (frequency + z * z / (2 * count)) / denominator
    half_width = z * math.sqrt(frequency * (1 - frequency) / count + z * z / (4 * count * count)) / denominator
    return {
        "producer": "trusted-organizer-toy-reference", "sandboxed_participant_execution": False,
        "target": "toy-prefix10-v1", "seed": 2026,
        "prng": "Python random.Random; fixed-seed pseudorandom samples are not a mathematical uniformity certificate",
        "batch_size": 32, "trial_count": count, "successes": successes,
        "observed_frequency": frequency,
        "interval": {"method": "Wilson two-sided, descriptive only", "level": 0.95,
                     "lower": center - half_width, "upper": center + half_width},
        "trials": trials,
        "reference_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }


def build_case(case: str) -> dict[str, Any]:
    if case not in CASES:
        raise ValueError("unknown organizer calibration case")
    proof = (FIXTURE_DIR / f"{case}.md").read_text(encoding="utf-8")
    heuristic = case == "heuristic"
    profile = {
        "id": "toy-prefix10-v1" if heuristic else "toy-projection4-v1",
        "purpose": "organizer synthetic calibration only; not a registered challenge target",
        "rounds": 1, "round_semantics": "one application of the complete toy map; not a cryptographic round count",
        "input_bytes": 3 if heuristic else 2, "output_bits": 10 if heuristic else 4,
        "definition": "int.from_bytes(hashlib.sha256(message).digest()[:2], 'big') >> 6" if heuristic else "message[0] & 15",
    }
    cost_model = {
        "id": "toy-operations-v1", "time_unit": "toy-operations",
        "one_unit": "one fixed-width byte/int primitive, uniform input draw, comparison, output, or complete toy hash call",
        "memory": "all logical byte storage including inputs, outputs, counters, and scratch; Python interpreter excluded",
        "score": "log2(time * memory_bytes)", "note": "diagnostic metadata; no score is emitted",
    }
    heuristics = [{
        "id": "H1", "statement": "The specified 32-message batch succeeds with probability at least 0.5.",
        "role": "score-critical success probability", "evidence_ids": ["organizer-trials-2026"],
        "scope": "exact toy-prefix10 map; uniform 24-bit messages; batch size 32",
        "extrapolation": "finite observed batches to underlying population probability",
        "limitations": "32 pseudorandom batches; confidence interval lower endpoint below claimed bound; no exact count",
    }] if heuristic else []
    exponent = 12 if heuristic else 4
    claim = {
        "schema_version": 3, "submission_state": "ready", "lane": "exploratory",
        "target_profile": profile["id"], "attack_class": "ordinary-collision", "rounds": 1,
        "claim": {
            "time_log2": exponent, "time_unit": "toy-operations", "memory_log2_bytes": exponent,
            "data_log2": 0, "preprocessing_log2": 0, "success_probability": 0.5 if heuristic else 1.0,
            "nonuniform_advice_log2_bytes": 0,
        },
        "restrictions": [], "baseline_improved": "none-organizer-calibration-only", "heuristics": heuristics,
    }
    if heuristic:
        claim["experiment_manifest"] = "experiments/manifest.json"
    package_hash = _digest({"case": case, "claim": claim, "proof_markdown": proof})
    config_hash = _digest({"target_profile": profile, "cost_model": cost_model, "policy_id": "paired-lanes-v1"})
    numbered = "\n".join(f"L{index}\t{line}" for index, line in enumerate(proof.splitlines(), 1)) + "\n"
    intake = {
        "status": "mechanically_valid", "submission_state": "ready", "claim": claim,
        "track": {"target_profile": profile["id"], "attack_class": "ordinary-collision", "rounds": 1},
        "package_sha256": package_hash, "target_config_sha256": config_hash,
        "source": "organizer calibration fixture; not verifier approval of a challenge candidate",
    }
    certificate = {
        "status": "passed", "package_sha256": package_hash, "target_config_sha256": config_hash,
        "certificates": [], "scope": "no participant certificates supplied; this does not certify proof statements",
    }
    experiment = {
        "status": "passed" if heuristic else "not_requested", "package_sha256": package_hash,
        "target_config_sha256": config_hash,
        "execution": heuristic_experiment() if heuristic else None,
    }
    return {
        "schema_version": "hashsmash-evidence-v1",
        "submission": {"intake_report": intake, "certificate_report": certificate,
                       "proof_markdown_line_numbered": numbered, "experiment_report": experiment},
        "benchmark": {"target_profile": profile, "cost_model": cost_model,
                      "qualification_policy": "paired-lanes-v1", "calibration_only": True},
    }


def classify(case: str, dossier: Mapping[str, Any]) -> dict[str, Any]:
    actual = {lane: dossier["lanes"][lane]["status"] for lane in ("exploratory", "rigorous")}
    matches = {lane: status in EXPECTED[case][lane] for lane, status in actual.items()}
    return {"expected": EXPECTED[case], "actual": actual, "matches_expected": matches,
            "all_expected": all(matches.values()),
            "interpretation": "rubric diagnostic; investigate unexpected reasoning; no statistical FP/FN estimate"}


def _safe_config(config: Any) -> dict[str, Any]:
    return {key: getattr(config, key) for key in (
        "model", "strategy", "reasoning_effort", "max_tokens", "timeout_seconds", "max_attempts",
    )} | ({"region": config.region} if isinstance(config, BedrockConfig) else {})


def main(argv: list[str] | None = None) -> int:
    import os

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=(*CASES, "all"), default="positive")
    parser.add_argument("--provider", choices=("bedrock", "openrouter"),
                        default=os.environ.get("HASHSMASH_JUDGE_PROVIDER", "bedrock"))
    parser.add_argument("--mode", choices=("single", "committee"),
                        default=os.environ.get("HASHSMASH_JUDGE_MODE", "single"))
    parser.add_argument("--model")
    parser.add_argument("--max-tokens", type=int, default=16384)
    parser.add_argument("--timeout-seconds", type=float, default=180.0)
    parser.add_argument("--dry-run", action="store_true", help="construct evidence only; no credentials or provider calls")
    args = parser.parse_args(argv)
    if not 1024 <= args.max_tokens <= 32768 or not 1 <= args.timeout_seconds <= 300:
        parser.error("max-tokens must be 1024..32768 and timeout-seconds 1..300")
    cases = CASES if args.case == "all" else (args.case,)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    client, role_clients, config_record, committee_record = None, {}, {}, {}
    if not args.dry_run:
        try:
            config = BedrockConfig.from_env() if args.provider == "bedrock" else OpenRouterConfig.from_env()
            factory = BedrockClient if args.provider == "bedrock" else OpenRouterClient
            overrides = {"max_attempts": 1, "max_tokens": args.max_tokens, "timeout_seconds": args.timeout_seconds}
            if args.model:
                overrides["model"] = args.model
            config = replace(config, **overrides)
            client = factory(config)
            role_clients, committee_record = build_role_clients(config, factory, mode=args.mode)
            # Preserve role models/strategies while respecting this finite run's
            # explicit per-request output cap and single transport attempt.
            for stage, role_client in list(role_clients.items()):
                if role_client.config.max_tokens > args.max_tokens:
                    role_clients[stage] = factory(replace(role_client.config, max_tokens=args.max_tokens))
                    committee_record["roles"][stage]["max_tokens"] = args.max_tokens
            if any(role_client.config.max_attempts != 1 for role_client in role_clients.values()):
                raise ValueError("calibration role attempts must stay bounded at one")
            config_record = _safe_config(config)
        except (ValueError, OSError) as error:
            print(json.dumps({"status": "configuration_failed", "error_type": type(error).__name__}))
            return 3
    summaries = []
    for case in cases:
        evidence = build_case(case)
        record = {
            "schema_version": "paired-calibration-report-v1", "run_id": run_id, "case": case,
            "calibration_only": True, "is_qualified_baseline": False,
            "no_score_emitted": True, "provider": args.provider, "config": config_record,
            "committee": committee_record, "max_stage_calls": len(LANE_STAGES),
            "max_transport_attempts_per_stage": 1, "evidence": evidence,
        }
        if args.dry_run:
            record["status"] = "evidence_only"
            summary = {"case": case, "status": "evidence_only"}
        else:
            dossier = run_paired_review(evidence, client, role_clients=role_clients)
            record.update(status="reviewed", dossier=dossier, classification=classify(case, dossier))
            summary = {"case": case, **record["classification"]}
        destination = REPORT_DIR / f"{run_id}-{case}.json"
        atomic_write_json(destination, record)
        summary["report"] = str(destination)
        summaries.append(summary)
        print(json.dumps(summary, sort_keys=True), flush=True)
    if any("infra_failed" in item.get("actual", {}).values() for item in summaries):
        return 3
    return 0 if args.dry_run or all(item["all_expected"] for item in summaries) else 2


if __name__ == "__main__":
    raise SystemExit(main())
