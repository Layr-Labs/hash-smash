#!/usr/bin/env python3
"""List, inspect and validate local tracks without loading credentials or calling AI."""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verifier.certificates import verify_certificates
from verifier.errors import VerificationError
from verifier.intake import validate_candidate
from verifier.io import load_json_bytes
from verifier.tracks import all_tracks, get_track


def status(track) -> dict:
    current = validate_candidate(track.candidate, track=track)
    report_root = ROOT / ".yukon" / "reports" / "tracks" / track.id
    scored = []
    run_count = 0
    # Score only successful score/all invocations, bound to this exact current model.
    # Historical candidates can be best-known results but are clearly not current input.
    for path in sorted((report_root / "runs").glob("*/run.json")):
        run_count += 1
        run = load_json_bytes(path.read_bytes(), str(path))
        score_path = path.parent / "score.json"
        if run.get("exit_code") != 0 or run.get("command") not in ("all", "score") or not score_path.is_file():
            continue
        score = load_json_bytes(score_path.read_bytes(), str(score_path))
        metrics = score.get("metrics", {})
        if (metrics.get("trackId") != track.id or metrics.get("reviewStatus") != "ai_qualified"
                or metrics.get("targetConfigSha256") != track.config_sha256()):
            continue
        scored.append({"score": score["score"], "run_id": run["run_id"],
                       "current_candidate": metrics.get("inputPackageSha256") == current["package_sha256"]})
    return {"track": track.id, "submission_state": current["submission_state"],
            "nominal_reference_score": track.digest_bits, "qualified_baseline": None,
            "archived_runs": run_count, "best_ai_reviewed": min(scored, key=lambda r: r["score"]) if scored else None}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("list", "show", "check", "status"))
    parser.add_argument("track", nargs="?")
    args = parser.parse_args(argv)
    try:
        selected = (get_track(args.track),) if args.track else all_tracks()
        if args.command == "show" and not args.track:
            parser.error("show requires a track ID")
        if args.command == "list":
            print("TRACK         FUNCTION  STEPS/ROUNDS  DIFFICULTY       NOMINAL LOG2(T*M)")
            for track in selected:
                print(f"{track.id:13} {track.algorithm:8} {track.rounds:12}  {track.difficulty:16} {track.digest_bits}")
        elif args.command == "show":
            track = selected[0]
            print(json.dumps({"purpose": track.purpose, "candidate": str(track.candidate),
                              **track.benchmark()}, indent=2))
        elif args.command == "status":
            results = []
            failed = False
            for track in selected:
                try:
                    results.append(status(track))
                except (VerificationError, OSError) as error:
                    results.append({"track": track.id, "status": "invalid_candidate_or_report", "error": str(error)})
                    failed = True
            print(json.dumps(results, indent=2))
            return 2 if failed else 0
        else:
            results = []
            for track in selected:
                report = validate_candidate(track.candidate, track=track)
                certificates = verify_certificates(track.candidate, track=track)
                results.append({"track": track.id, "status": "mechanically_valid",
                                "submission_state": report["submission_state"],
                                "certificates_verified": len(certificates["certificates"]),
                                "qualified": False})
            print(json.dumps(results, indent=2))
        return 0
    except (VerificationError, OSError) as error:
        print(f"track validation failed: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
