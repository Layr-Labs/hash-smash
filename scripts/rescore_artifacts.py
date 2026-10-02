#!/usr/bin/env python3
"""Select and verify prior Actions review artifacts; never execute their contents."""

import argparse
import os
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from judge import rescore
from scripts.hashsmash_pipeline import RunPaths
from verifier.errors import VerificationError
from verifier.frontier_tracks import get_frontier_track
from verifier.intake import validate_candidate
from verifier.io import atomic_write_json, load_json_bytes
from verifier.schema_validation import require_sha256

ARTIFACTS = rescore.ROOT / "reorg/artifacts.json"


def selection(paths):
    intake = validate_candidate(paths.candidate, track=paths.track)
    return rescore.find_source(paths.track, intake["package_sha256"])


def artifact_reference(entry):
    references = load_json_bytes(ARTIFACTS.read_bytes(), str(ARTIFACTS))
    if not isinstance(references, dict):
        raise VerificationError("rescore artifacts must map packet hashes to workflow artifact IDs")
    for source, reference in references.items():
        require_sha256(source, "artifact.source")
        if (not isinstance(reference, dict) or set(reference) != {"run_id", "artifact_id"}
                or any(type(value) is not int or value <= 0 for value in reference.values())):
            raise VerificationError("invalid prior workflow artifact reference")
    if entry["source"] not in references:
        raise VerificationError("no workflow artifact pinned for this prior judgment")
    return references[entry["source"]]


def read_packet_file(path, *, limit=4 * 1024 * 1024):
    if path.is_symlink() or not path.is_file() or path.stat().st_size > limit:
        raise VerificationError("missing or oversized prior review artifact file")
    return load_json_bytes(path.read_bytes(), str(path))


def restore(paths, downloaded):
    entry = selection(paths)
    if entry is None:
        return
    # Old artifacts retain evidence in their per-command snapshots. Choose it by
    # the pinned packet hash, never by a mutable timestamp or a 'latest' filename.
    dossier = read_packet_file(downloaded / "judge-dossier.json")
    candidates = list(downloaded.glob("runs/*/judge-evidence.json"))
    if not candidates or len(candidates) > 32:
        raise VerificationError("prior review artifact has no bounded evidence history")
    packet = None
    for path in candidates:
        candidate = {"evidence": read_packet_file(path), "dossier": dossier}
        if rescore.digest(candidate) == entry["source"]:
            packet = candidate
            break
    if packet is None:
        raise VerificationError("downloaded judgment does not match the pinned packet checksum")
    history_path = downloaded / "rescore-history.json"
    history = read_packet_file(history_path, limit=16 * 1024 * 1024) if history_path.exists() else {}
    if not isinstance(history, dict) or len(history) > 31:
        raise VerificationError("invalid prior review history")
    # Validate the complete downloaded chain in isolation before admitting any
    # packet to this run's cache. An expired ancestor needs no separate download.
    with tempfile.TemporaryDirectory(prefix="hashsmash-review-") as temporary:
        cache = Path(temporary)
        for source, ancestor in history.items():
            require_sha256(source, "history.source")
            if rescore.digest(ancestor) != source:
                raise VerificationError("prior review history checksum mismatch")
            atomic_write_json(cache / (source + ".json"), ancestor)
        atomic_write_json(cache / (entry["source"] + ".json"), packet)
        packets = rescore.history_packets(entry["source"], cache)
        previous = packet["evidence"]
        if (previous["benchmark"]["track_id"] != entry["track_id"]
                or previous["submission"]["intake_report"]["package_sha256"] != entry["package_sha256"]
                or previous["submission"]["intake_report"]["target_config_sha256"] != entry["source_config_sha256"]):
            raise VerificationError("prior workflow judgment does not match the authorized submission")
        for source, retained in packets.items():
            atomic_write_json(paths.rescore_archives / (source + ".json"), retained)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("select", "restore"))
    parser.add_argument("--track", required=True)
    parser.add_argument("--downloaded", type=Path)
    args = parser.parse_args()
    paths = RunPaths.for_track(get_frontier_track(args.track))
    try:
        if args.command == "restore":
            if args.downloaded is None:
                parser.error("restore requires --downloaded")
            restore(paths, args.downloaded)
        else:
            entry = selection(paths)
            if entry is not None:
                reference = artifact_reference(entry)
                with open(os.environ["GITHUB_OUTPUT"], "a") as output:
                    output.write(f"run_id={reference['run_id']}\nartifact_id={reference['artifact_id']}\n")
    except (VerificationError, OSError) as error:
        print(f"prior judgment unavailable: {error}; no reorg review was started", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
