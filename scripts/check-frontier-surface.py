#!/usr/bin/env python3
"""Check the selected lane overlay against trusted main before processing it."""

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from verifier.frontier_tracks import get_frontier_track


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--track", required=True)
    args = parser.parse_args()
    track = get_frontier_track(args.track)
    prefix = str(track.candidate.relative_to(ROOT)) + "/"
    if not os.environ.get("GITHUB_REF", "").startswith("refs/heads/submissions/"):
        return 0
    command = ["git", "-c", "core.hooksPath=/dev/null", "-c", "core.fsmonitor=false",
               "-c", "core.pager=cat"]
    sha = os.environ.get("GITHUB_SHA", "")
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ValueError("invalid dispatched commit")
    subprocess.run([*command, "rev-parse", "--verify", "refs/remotes/origin/main"], cwd=ROOT,
                   check=True, stdout=subprocess.DEVNULL)
    # Yukon creates one commit whose parent is the frozen benchmark base. A
    # sibling promotion may advance main while this run queues; diffing moving
    # main would then falsely attribute the sibling delta to this submission.
    parents = subprocess.check_output([*command, "rev-list", "--parents", "-n", "1", sha], cwd=ROOT).decode().split()
    if len(parents) != 2 or parents[0] != sha:
        raise ValueError("submission must be a single-parent overlay")
    parent = parents[1]
    subprocess.run([*command, "merge-base", "--is-ancestor", parent, "refs/remotes/origin/main"],
                   cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    diff = subprocess.check_output([*command, "diff", "--no-ext-diff", "--no-renames", "--name-only", "-z",
                                    parent, sha], cwd=ROOT)
    for path in diff.split(b"\0"):
        if path and not path.decode("utf-8").startswith(prefix):
            # Do not reflect attacker-controlled filenames into Actions command syntax.
            raise ValueError("submission changed a path outside the selected lane candidate")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, subprocess.SubprocessError):
        print("Selected-lane editable surface verification failed", file=sys.stderr)
        raise SystemExit(2)
