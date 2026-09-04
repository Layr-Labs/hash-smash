#!/usr/bin/env python3
"""Pull the pinned runtime in the credential-free intake job when Python is used."""

import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments import DEFAULT_DOCKER_IMAGE
from verifier.frontier_tracks import get_frontier_track
from verifier.intake import validate_candidate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--track", required=True)
    args = parser.parse_args()
    track = get_frontier_track(args.track)
    intake = validate_candidate(track.candidate, track=track)
    if intake["submission_state"] != "ready":
        print("Draft candidate: no experiment runtime preparation")
        return 2
    manifest = intake.get("experiment_manifest")
    if manifest and any(item["kind"] == "python-message-pairs-v1" for item in manifest["experiments"]):
        subprocess.run(["docker", "pull", "--platform", "linux/amd64", DEFAULT_DOCKER_IMAGE], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
