from __future__ import annotations

import json
from pathlib import Path


def valid_claim(**overrides):
    value = {
        "schema_version": 1,
        "target_profile": "sha1-fips180-4-v1",
        "attack_class": "ordinary-collision",
        "rounds": 80,
        "claim": {
            "time_log2": 81,
            "time_unit": "sha1-compressions",
            "memory_log2_bytes": 85,
            "data_log2": 80,
            "preprocessing_log2": 0,
            "success_probability": 0.39,
            "nonuniform_advice_log2_bytes": 0,
        },
        "restrictions": [],
        "baseline_improved": "sha1-known-result-v1",
    }
    value.update(overrides)
    return value


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def make_candidate(root: Path, claim=None, proof: str = "# Claim\n\nArgument.\n") -> Path:
    candidate = root / "candidate"
    candidate.mkdir()
    write_json(candidate / "claim.json", valid_claim() if claim is None else claim)
    (candidate / "proof.md").write_text(proof, encoding="utf-8", newline="\n")
    return candidate


def add_manifest(candidate: Path, certificates) -> None:
    claim_path = candidate / "claim.json"
    claim = json.loads(claim_path.read_text(encoding="utf-8"))
    claim["certificate_manifest"] = "certificates/manifest.json"
    write_json(claim_path, claim)
    write_json(
        candidate / "certificates" / "manifest.json",
        {"schema_version": 1, "certificates": certificates},
    )
