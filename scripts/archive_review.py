#!/usr/bin/env python3
"""Preserve a trusted review packet and print its proposed reorg plan entry.

Run on organizer-downloaded workflow artifacts, never participant-supplied packets.
The printed entry does not activate anything; review it into reorg/plan.json.
"""

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from judge import rescore
from verifier.frontier_tracks import get_frontier_track
from verifier.io import atomic_write_json, canonical_json_bytes, load_json_bytes
from verifier.schema_validation import require_sha256


def archive(evidence_path, dossier_path, archive_root):
    packet = {
        "evidence": load_json_bytes(evidence_path.read_bytes(), str(evidence_path)),
        "dossier": load_json_bytes(dossier_path.read_bytes(), str(dossier_path)),
    }
    history_path = dossier_path.parent / "rescore-history.json"
    if history_path.exists():
        from scripts.rescore_artifacts import read_packet_file
        history = read_packet_file(history_path, limit=16 * 1024 * 1024)
        if not isinstance(history, dict) or len(history) > 31:
            raise ValueError("invalid archived review history")
        for source, ancestor in history.items():
            require_sha256(source, "history.source")
            if rescore.digest(ancestor) != source:
                raise ValueError("archived review history checksum mismatch")
            atomic_write_json(archive_root / (source + ".json"), ancestor)
    rescore.verify_packet(packet, archive_root)
    source = rescore.digest(packet)
    destination = archive_root / (source + ".json")
    if destination.exists() and destination.read_bytes() != canonical_json_bytes(packet):
        raise ValueError("refusing to replace an existing archive")
    atomic_write_json(destination, packet)
    evidence = packet["evidence"]
    track = get_frontier_track(evidence["benchmark"]["track_id"])
    intake = evidence["submission"]["intake_report"]
    return {
        "track_id": track.id, "package_sha256": intake["package_sha256"], "source": source,
        "source_config_sha256": intake["target_config_sha256"],
        "destination_config_sha256": track.config_sha256(),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", required=True, type=Path)
    parser.add_argument("--dossier", required=True, type=Path)
    parser.add_argument("--archive-root", type=Path, default=rescore.ARCHIVES)
    args = parser.parse_args()
    entry = archive(args.evidence, args.dossier, args.archive_root)
    sys.stdout.buffer.write(canonical_json_bytes(entry))
