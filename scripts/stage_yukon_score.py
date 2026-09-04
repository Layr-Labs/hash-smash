#!/usr/bin/env python3
"""Stage one validated score at its exact manifest-relative artifact path."""

import argparse
import json
import math
from pathlib import Path, PurePosixPath


def read_score(data):
    def reject_constant(value):
        raise ValueError(f"nonfinite JSON number: {value}")

    score = json.loads(data, parse_constant=reject_constant)
    value = score.get("score") if isinstance(score, dict) else None
    if type(value) not in (int, float):
        raise ValueError("score must be a finite numeric JSON field")
    try:
        finite = math.isfinite(value)
    except OverflowError:
        finite = False
    if not finite:
        raise ValueError("score must be finite")
    return score


def stage_score(benchmark_root, score_path, destination):
    root = Path(benchmark_root).resolve(strict=True)
    relative = PurePosixPath(score_path)
    if (relative.is_absolute() or str(relative) != score_path
            or any(part in (".", "..") for part in relative.parts)
            or "\\" in score_path or not relative.parts):
        raise ValueError("score path must be a normalized relative POSIX path")
    manifest = json.loads((root / "benchmark.json").read_bytes())
    tracks = manifest["tracks"] if manifest["schemaVersion"] == 2 else [manifest]
    if score_path not in {track["scorePath"] for track in tracks}:
        raise ValueError("score path is not declared in this benchmark manifest")
    source = root
    for part in relative.parts:
        source = source / part
        if source.is_symlink():
            raise ValueError("score source must not traverse symlinks")
    data = source.read_bytes()
    read_score(data)
    destination = Path(destination).absolute()
    for track in tracks:
        for editable in track["editablePaths"]:
            if source.is_relative_to(root / editable) or destination.resolve().is_relative_to(root / editable):
                raise ValueError("score artifacts must stay outside editable paths")
    # Never reuse a staging directory: a leftover score or unrelated file must
    # not enter this run's artifact. GitHub RUNNER_TEMP is fresh for each job.
    destination.mkdir(parents=True, exist_ok=False)
    output = destination.joinpath(*relative.parts)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark-root", required=True)
    parser.add_argument("--score-path", required=True)
    parser.add_argument("--destination", required=True)
    args = parser.parse_args()
    try:
        stage_score(args.benchmark_root, args.score_path, args.destination)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(2, f"Score artifact staging failed: {error}\n")
    print(f"Staged exact artifact entry: {args.score_path}")


if __name__ == "__main__":
    main()
