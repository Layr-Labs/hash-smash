"""Organizer-owned deterministic certificate checkers."""

from __future__ import annotations

import hashlib
import os
import stat
from pathlib import Path
from typing import Any

from .constants import MAX_CERTIFICATE_FILE_BYTES, SCHEMA_VERSION
from .errors import VerificationError
from .intake import validate_candidate
from .io import atomic_write_json, ensure_output_outside_root, sha256_bytes
from .hash_functions import digest
from .tracks import Track


def _read_certificate_file(candidate: Path, relative: str) -> bytes:
    # Intake already established the path shape and regular-file invariant.  O_NOFOLLOW
    # repeats the most important check at checker use time.
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(candidate / relative, flags)
    except OSError as error:
        raise VerificationError(f"{relative}: could not safely open certificate data: {error}") from error
    try:
        opened_stat = os.fstat(descriptor)
        if not stat.S_ISREG(opened_stat.st_mode):
            raise VerificationError(f"{relative}: certificate data must be a regular file")
        data = b""
        while len(data) <= MAX_CERTIFICATE_FILE_BYTES:
            chunk = os.read(descriptor, min(64 * 1024, MAX_CERTIFICATE_FILE_BYTES + 1 - len(data)))
            if not chunk:
                break
            data += chunk
        if len(data) > MAX_CERTIFICATE_FILE_BYTES:
            raise VerificationError(f"{relative}: exceeds certificate file limit")
        return data
    finally:
        os.close(descriptor)


def verify_certificates(candidate_root: str | os.PathLike[str], output_path: str | os.PathLike[str] | None = None, *, track: Track | None = None) -> dict[str, Any]:
    """Verify every declared certificate, or succeed with an empty result if absent."""

    candidate = Path(candidate_root)
    intake = validate_candidate(candidate, track=track)
    intake_files = {item["path"]: item for item in intake["files"]}
    manifest = intake["certificate_manifest"]
    results: list[dict[str, Any]] = []
    if manifest is not None:
        for certificate in manifest["certificates"]:
            message_a = _read_certificate_file(candidate, certificate["message_a"])
            message_b = _read_certificate_file(candidate, certificate["message_b"])
            for relative, data in (
                (certificate["message_a"], message_a),
                (certificate["message_b"], message_b),
            ):
                if sha256_bytes(data) != intake_files[relative]["sha256"]:
                    raise VerificationError(f"{relative}: changed after intake")
            if message_a == message_b:
                raise VerificationError(
                    f"certificate {certificate['id']}: ordinary collision messages must differ"
                )
            if track:
                digest_a = digest(message_a, track.algorithm, track.rounds).hex()
                digest_b = digest(message_b, track.algorithm, track.rounds).hex()
            else:
                digest_a = hashlib.sha1(message_a, usedforsecurity=False).hexdigest()
                digest_b = hashlib.sha1(message_b, usedforsecurity=False).hexdigest()
            expected = certificate["expected_digest"]
            if digest_a != expected:
                raise VerificationError(
                    f"certificate {certificate['id']}: message_a digest {digest_a} does not match expected {expected}"
                )
            if digest_b != expected:
                raise VerificationError(
                    f"certificate {certificate['id']}: message_b digest {digest_b} does not match expected {expected}"
                )
            results.append(
                {
                    "id": certificate["id"],
                    "type": certificate["type"],
                    "status": "verified",
                    "message_a": {
                        "path": certificate["message_a"],
                        "size_bytes": len(message_a),
                        "sha256": sha256_bytes(message_a),
                    },
                    "message_b": {
                        "path": certificate["message_b"],
                        "size_bytes": len(message_b),
                        "sha256": sha256_bytes(message_b),
                    },
                    "digest" if track else "sha1_digest": expected,
                }
            )

    report = {
        "schema_version": SCHEMA_VERSION,
        "status": "passed",
        "checker": f"hashsmash-{track.profile_id}" if track else "hashsmash-sha1-collision-v1",
        "package_sha256": intake["package_sha256"],
        "certificates": results,
    }
    if track:
        report["target_profile"] = track.profile_id
        report["target_config_sha256"] = track.config_sha256()
    if output_path is not None:
        destination = Path(output_path)
        ensure_output_outside_root(candidate, destination)
        atomic_write_json(destination, report)
    return report
