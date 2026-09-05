from __future__ import annotations

import json
from pathlib import Path


from verifier.frontier_tracks import get_frontier_track

TRACK = get_frontier_track("sha1-r80-rigorous")


def valid_claim(**overrides):
    value = TRACK.draft_claim()
    value.pop("certificate_manifest")
    value["submission_state"] = "ready"
    value["claim"].update(time_log2=81, memory_log2_bytes=85)
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
        {"schema_version": 2, "certificates": certificates},
    )
