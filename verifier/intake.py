"""Deterministic submission intake and filesystem validation."""

from __future__ import annotations

import os
import stat
from pathlib import Path
from typing import Any

from .constants import (
    ATTACK_CLASS,
    CLAIM_PATH,
    MANIFEST_PATH,
    MAX_CERTIFICATE_FILE_BYTES,
    MAX_CLAIM_BYTES,
    MAX_MANIFEST_BYTES,
    MAX_PROOF_BYTES,
    MAX_TOTAL_BYTES,
    PROOF_PATH,
    ROUNDS,
    SCHEMA_VERSION,
    TARGET_PROFILE,
)
from .errors import VerificationError
from .io import (
    atomic_write_bytes,
    atomic_write_json,
    canonical_json_bytes,
    ensure_output_outside_root,
    load_json_bytes,
    sha256_bytes,
)
from .schema_validation import validate_claim, validate_manifest
from .tracks import Track


def _scan_candidate(candidate: Path, *, allow_experiments: bool = False) -> dict[str, os.stat_result]:
    """Return every candidate file after rejecting ambiguous filesystem objects."""

    try:
        root_stat = candidate.lstat()
    except FileNotFoundError as error:
        raise VerificationError(f"candidate root does not exist: {candidate}") from error
    if stat.S_ISLNK(root_stat.st_mode) or not stat.S_ISDIR(root_stat.st_mode):
        raise VerificationError("candidate root must be a real directory, not a symlink")

    files: dict[str, os.stat_result] = {}
    with os.scandir(candidate) as root_entries:
        for entry in root_entries:
            relative = entry.name
            entry_stat = entry.stat(follow_symlinks=False)
            if stat.S_ISLNK(entry_stat.st_mode):
                raise VerificationError(f"{relative}: symlinks are not allowed")
            if stat.S_ISREG(entry_stat.st_mode):
                files[relative] = entry_stat
                continue
            if stat.S_ISDIR(entry_stat.st_mode) and (relative == "certificates" or allow_experiments and relative == "experiments"):
                with os.scandir(entry.path) as certificate_entries:
                    for certificate_entry in certificate_entries:
                        certificate_relative = f"{relative}/{certificate_entry.name}"
                        certificate_stat = certificate_entry.stat(follow_symlinks=False)
                        if stat.S_ISLNK(certificate_stat.st_mode):
                            raise VerificationError(f"{certificate_relative}: symlinks are not allowed")
                        if not stat.S_ISREG(certificate_stat.st_mode):
                            raise VerificationError(
                                f"{certificate_relative}: only direct regular files are allowed"
                            )
                        files[certificate_relative] = certificate_stat
                continue
            if stat.S_ISDIR(entry_stat.st_mode):
                raise VerificationError(f"{relative}: unexpected directory")
            raise VerificationError(f"{relative}: only regular files are allowed")
    return files


def _read_regular_file(path: Path, expected_stat: os.stat_result, limit: int, relative: str) -> bytes:
    if expected_stat.st_mode & 0o111:
        raise VerificationError(f"{relative}: executable files are not allowed")
    if expected_stat.st_size > limit:
        raise VerificationError(f"{relative}: exceeds its {limit}-byte limit")

    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise VerificationError(f"{relative}: could not safely open regular file: {error}") from error
    try:
        opened_stat = os.fstat(descriptor)
        if not stat.S_ISREG(opened_stat.st_mode):
            raise VerificationError(f"{relative}: changed to a non-regular file during intake")
        if (opened_stat.st_dev, opened_stat.st_ino) != (expected_stat.st_dev, expected_stat.st_ino):
            raise VerificationError(f"{relative}: changed during intake")
        if opened_stat.st_size > limit:
            raise VerificationError(f"{relative}: exceeds its {limit}-byte limit")
        chunks: list[bytes] = []
        remaining = limit + 1
        while remaining:
            chunk = os.read(descriptor, min(64 * 1024, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        data = b"".join(chunks)
        if len(data) > limit:
            raise VerificationError(f"{relative}: exceeds its {limit}-byte limit")
        final_stat = os.fstat(descriptor)
        if (final_stat.st_size, final_stat.st_mtime_ns) != (
            opened_stat.st_size,
            opened_stat.st_mtime_ns,
        ):
            raise VerificationError(f"{relative}: changed while being read")
        return data
    finally:
        os.close(descriptor)


def _number_proof(data: bytes) -> tuple[bytes, int]:
    if b"\x00" in data:
        raise VerificationError(f"{PROOF_PATH}: NUL bytes are not allowed")
    if b"\r" in data:
        raise VerificationError(f"{PROOF_PATH}: must use LF line endings")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise VerificationError(f"{PROOF_PATH}: must be UTF-8") from error
    if not text.strip():
        raise VerificationError(f"{PROOF_PATH}: must not be empty")

    lines = text.splitlines(keepends=True)
    numbered = "".join(f"{index:06d} | {line}" for index, line in enumerate(lines, 1))
    return numbered.encode("utf-8"), len(lines)


def _file_limit(relative: str) -> int:
    if relative == CLAIM_PATH:
        return MAX_CLAIM_BYTES
    if relative == PROOF_PATH:
        return MAX_PROOF_BYTES
    if relative == MANIFEST_PATH:
        return MAX_MANIFEST_BYTES
    return MAX_CERTIFICATE_FILE_BYTES


def validate_candidate(candidate_root: str | os.PathLike[str], output_dir: str | os.PathLike[str] | None = None, *, track: Track | None = None) -> dict[str, Any]:
    """Validate a candidate and optionally write the trusted intake artifacts.

    The candidate is never modified.  If ``output_dir`` is provided, the function
    writes ``intake-report.json`` and ``proof-numbered.md`` only after every gate passes.
    """

    candidate = Path(candidate_root)
    paired = bool(getattr(track, "lane", None))
    file_stats = _scan_candidate(candidate, allow_experiments=paired)
    missing = {CLAIM_PATH, PROOF_PATH} - set(file_stats)
    if missing:
        raise VerificationError(f"candidate: missing required file(s): {', '.join(sorted(missing))}")

    total_size = sum(item.st_size for item in file_stats.values())
    if total_size > MAX_TOTAL_BYTES:
        raise VerificationError(f"candidate: exceeds total {MAX_TOTAL_BYTES}-byte limit")

    contents = {
        relative: _read_regular_file(candidate / relative, info, _file_limit(relative), relative)
        for relative, info in sorted(file_stats.items())
    }
    claim = validate_claim(load_json_bytes(contents[CLAIM_PATH], CLAIM_PATH), track=track)

    manifest_present = MANIFEST_PATH in contents
    manifest_declared = "certificate_manifest" in claim
    if manifest_present != manifest_declared:
        if manifest_present:
            raise VerificationError(
                f"{MANIFEST_PATH}: exists but {CLAIM_PATH} does not declare certificate_manifest"
            )
        raise VerificationError(f"{MANIFEST_PATH}: declared by {CLAIM_PATH} but missing")

    manifest: dict[str, Any] | None = None
    declared_certificate_files: set[str] = set()
    if manifest_present:
        manifest = validate_manifest(load_json_bytes(contents[MANIFEST_PATH], MANIFEST_PATH), track=track)
        for certificate in manifest["certificates"]:
            declared_certificate_files.add(certificate["message_a"])
            declared_certificate_files.add(certificate["message_b"])

    allowed = {CLAIM_PATH, PROOF_PATH}
    if manifest_present:
        allowed.add(MANIFEST_PATH)
    allowed.update(declared_certificate_files)
    experiment_manifest = None
    experiment_path = "experiments/manifest.json"
    if paired and (experiment_path in contents or "experiment_manifest" in claim):
        if experiment_path not in contents or "experiment_manifest" not in claim:
            raise VerificationError("experiment manifest must exist and be explicitly declared by the claim")
        from experiments import declared_files, validate_manifest as validate_experiments
        try:
            experiment_manifest = validate_experiments(load_json_bytes(contents[experiment_path], experiment_path))
            experiment_files = declared_files(experiment_manifest)
        except ValueError as error:
            raise VerificationError(f"invalid experiment manifest: {error}") from error
        if sum(len(contents.get(name, b"")) for name in experiment_files) > 65536:
            raise VerificationError("experiment source texts exceed the total 64 KiB review budget")
        allowed.add(experiment_path)
        allowed.update(experiment_files)
        declared_certificate_files.update(experiment_files)
    unexpected = set(contents) - allowed
    absent = declared_certificate_files - set(contents)
    if unexpected:
        raise VerificationError(f"candidate: unexpected file(s): {', '.join(sorted(unexpected))}")
    if absent:
        raise VerificationError(f"candidate: declared certificate file(s) missing: {', '.join(sorted(absent))}")

    numbered_proof, line_count = _number_proof(contents[PROOF_PATH])
    if paired:
        experiment_ids = {item["id"] for item in experiment_manifest["experiments"]} if experiment_manifest else set()
        for heuristic in claim["heuristics"]:
            for ref in heuristic["evidence_ids"]:
                kind, value = ref.split(":", 1)
                if kind == "experiment" and value not in experiment_ids:
                    raise VerificationError(f"heuristic {heuristic['id']}: unknown experiment {value}")
                if kind == "proof":
                    ends = [int(part) for part in value.split("-")]
                    if ends[0] > ends[-1] or ends[-1] > line_count:
                        raise VerificationError(f"heuristic {heuristic['id']}: proof reference outside document")
    files = [
        {
            "path": relative,
            "size_bytes": len(contents[relative]),
            "sha256": sha256_bytes(contents[relative]),
        }
        for relative in sorted(contents)
    ]
    package_sha256 = sha256_bytes(canonical_json_bytes(files))
    report: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "status": "mechanically_valid",
        "track": {
            "target_profile": track.profile_id if track else TARGET_PROFILE,
            "attack_class": ATTACK_CLASS,
            "rounds": track.rounds if track else ROUNDS,
        },
        "claim": claim,
        "certificate_manifest": manifest,
        "files": files,
        "proof": {
            "path": PROOF_PATH,
            "sha256": sha256_bytes(contents[PROOF_PATH]),
            "line_count": line_count,
            "line_numbered_sha256": sha256_bytes(numbered_proof),
        },
        "package_sha256": package_sha256,
    }
    if track:
        report["track"]["id"] = track.id
        report["target_config_sha256"] = track.config_sha256()
        report["submission_state"] = claim["submission_state"]
    if paired:
        report["lane"] = track.lane
        report["experiment_manifest"] = experiment_manifest

    if output_dir is not None:
        destination = Path(output_dir)
        # Reject writing reports into the untrusted candidate tree.
        ensure_output_outside_root(candidate, destination)
        atomic_write_bytes(destination / "proof-numbered.md", numbered_proof)
        atomic_write_json(destination / "intake-report.json", report)
    return report
