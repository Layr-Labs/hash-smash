#!/usr/bin/env python3
"""Validate the two Yukon leaf manifests and list unresolved research slots."""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from verifier.frontier_tracks import LANES, frontier_tracks, get_frontier_track, planned_slots
from verifier.errors import VerificationError
from verifier.io import load_json_bytes


def manifest_for(lane):
    tracks = [track for track in frontier_tracks() if track.lane == lane]
    return {
        "schemaVersion": 2, "name": f"hashsmash-{lane}",
        "tracks": [{
            "name": track.target_id,
            "description": f"{track.target_id} ordinary collisions; {lane} AI review. Minimize log2(time * memory bytes). Pass means {track.accepted_status}.",
            "category": "cryptanalysis", "direction": "-",
            "editablePaths": [f"candidates/{track.target_id}"],
            "setupCommand": ["bash", "../../.yukon/setup.sh"],
            "benchmarkCommand": ["python3", "../../scripts/hashsmash_pipeline.py", "all", "--track", track.id],
            "scorePath": f".yukon/scores/{track.id}.json",
            "maxSubmissionBytes": 4194304,
            "runner": {"provider": "github-actions", "workflow": f"{track.id}.yml", "maxConcurrentWorkflows": 2},
        } for track in tracks],
    }


def validate_configuration(*, require_complete=False):
    tracks = frontier_tracks()
    if require_complete and len(tracks) != 28:
        raise VerificationError("the requested roster still has unresolved target/round definitions")
    candidate_paths, score_paths = set(), set()
    for lane in LANES:
        path = ROOT / "lanes" / lane / "benchmark.json"
        manifest = load_json_bytes(path.read_bytes(), str(path))
        if manifest != manifest_for(lane):
            raise VerificationError(f"{lane} manifest is stale or inconsistent with the organizer catalog")
        if not 1 <= len(manifest["tracks"]) <= 20:
            raise VerificationError("Yukon supports at most 20 tracks in one challenge")
    for track in tracks:
        track.benchmark()
        candidate_path = track.candidate
        score_path = track.state_root / "scores" / f"{track.id}.json"
        if candidate_path in candidate_paths or score_path in score_paths:
            raise VerificationError("paired lanes must have independent candidates and score paths")
        candidate_paths.add(candidate_path)
        score_paths.add(score_path)
        workflow = ROOT / ".github" / "workflows" / f"{track.id}.yml"
        text = workflow.read_text()
        if f"track: {track.id}\n" not in text or f"lane: {track.lane}\n" not in text:
            raise VerificationError("workflow must route the literal organizer-selected track and lane")
    return {"planned_tracks": len(planned_slots()), "runnable_tracks": len(tracks),
            "pending_tracks": 28 - len(tracks), "yukon_challenges": 2,
            "qualified_baselines": 0, "deployed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--track")
    parser.add_argument("--lane", choices=tuple(LANES))
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    result = validate_configuration(require_complete=args.require_complete)
    if args.track:
        track = get_frontier_track(args.track)
        if args.lane and track.lane != args.lane:
            raise VerificationError("workflow selected a mismatched lane")
        result["selected_track"] = track.id
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (VerificationError, OSError) as error:
        print(f"frontier configuration failed: {error}", file=sys.stderr)
        raise SystemExit(2)
