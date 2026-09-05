from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from verifier.constants import MAX_PROOF_BYTES
from verifier.errors import VerificationError
from verifier.intake import validate_candidate

from verifier.tests.common import TRACK, add_manifest, make_candidate, valid_claim, write_json


class IntakeTests(unittest.TestCase):
    def test_valid_candidate_writes_hashed_line_numbered_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            candidate = make_candidate(root, proof="# Claim\nsecond line\n")
            output = root / "artifacts"
            report = validate_candidate(candidate, output, track=TRACK)

            self.assertEqual(report["status"], "mechanically_valid")
            self.assertEqual(report["track"]["target_profile"], "sha1-r80-prefix-v1")
            self.assertEqual(report["proof"]["line_count"], 2)
            self.assertEqual(
                (output / "proof-numbered.md").read_text(encoding="utf-8"),
                "000001 | # Claim\n000002 | second line\n",
            )
            saved_report = json.loads((output / "intake-report.json").read_text())
            self.assertEqual(saved_report["package_sha256"], report["package_sha256"])
            self.assertRegex(report["package_sha256"], r"^[0-9a-f]{64}$")

    def test_unknown_claim_fields_rejected_at_each_object_level(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            top = valid_claim(extra=True)
            with self.assertRaisesRegex(VerificationError, "unknown field.*extra"):
                validate_candidate(make_candidate(root, top), track=TRACK)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            nested = valid_claim()
            nested["claim"]["hidden_cost"] = 1
            with self.assertRaisesRegex(VerificationError, "unknown field.*hidden_cost"):
                validate_candidate(make_candidate(root, nested), track=TRACK)

    def test_fixed_track_and_finite_numeric_constraints(self):
        cases = []
        wrong_target = valid_claim(target_profile="sha256-fips180-4-v1")
        cases.append((wrong_target, "target_profile"))
        wrong_rounds = valid_claim(rounds=79)
        cases.append((wrong_rounds, "rounds"))
        low_probability = valid_claim()
        low_probability["claim"]["success_probability"] = 0.389
        cases.append((low_probability, "at least 0.39"))
        bool_number = valid_claim()
        bool_number["claim"]["time_log2"] = True
        cases.append((bool_number, "must be a number"))

        for claim, message in cases:
            with self.subTest(message=message), tempfile.TemporaryDirectory() as directory:
                with self.assertRaisesRegex(VerificationError, message):
                    validate_candidate(make_candidate(Path(directory), claim), track=TRACK)

        with tempfile.TemporaryDirectory() as directory:
            candidate = make_candidate(Path(directory))
            claim = valid_claim()
            claim["claim"]["time_log2"] = float("nan")
            write_json(candidate / "claim.json", claim)
            with self.assertRaisesRegex(VerificationError, "invalid JSON"):
                validate_candidate(candidate, track=TRACK)

    def test_proof_must_be_nonempty_utf8_lf_text_within_limit(self):
        invalid_proofs = [
            (b"", "must not be empty"),
            (b"\xff", "must be UTF-8"),
            (b"line\r\n", "LF line endings"),
            (b"line\x00text", "NUL bytes"),
            (b"x" * (MAX_PROOF_BYTES + 1), "exceeds"),
        ]
        for proof, message in invalid_proofs:
            with self.subTest(message=message), tempfile.TemporaryDirectory() as directory:
                candidate = make_candidate(Path(directory))
                (candidate / "proof.md").write_bytes(proof)
                with self.assertRaisesRegex(VerificationError, message):
                    validate_candidate(candidate, track=TRACK)

    def test_unexpected_missing_and_executable_files_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = make_candidate(Path(directory))
            (candidate / "extra.txt").write_text("no")
            with self.assertRaisesRegex(VerificationError, "unexpected file.*extra.txt"):
                validate_candidate(candidate, track=TRACK)

        with tempfile.TemporaryDirectory() as directory:
            candidate = make_candidate(Path(directory))
            (candidate / "proof.md").unlink()
            with self.assertRaisesRegex(VerificationError, "missing required file.*proof.md"):
                validate_candidate(candidate, track=TRACK)

        with tempfile.TemporaryDirectory() as directory:
            candidate = make_candidate(Path(directory))
            os.chmod(candidate / "proof.md", 0o755)
            with self.assertRaisesRegex(VerificationError, "executable files"):
                validate_candidate(candidate, track=TRACK)

    def test_symlinks_and_nested_directories_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            candidate = make_candidate(root)
            linked_root = root / "linked-candidate"
            linked_root.symlink_to(candidate, target_is_directory=True)
            with self.assertRaisesRegex(VerificationError, "candidate root.*symlink"):
                validate_candidate(linked_root, track=TRACK)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            candidate = make_candidate(root)
            (candidate / "proof.md").unlink()
            (candidate / "proof.md").symlink_to(root / "outside.md")
            with self.assertRaisesRegex(VerificationError, "symlinks are not allowed"):
                validate_candidate(candidate, track=TRACK)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            candidate = make_candidate(root)
            (candidate / "unexpected").mkdir()
            with self.assertRaisesRegex(VerificationError, "unexpected directory"):
                validate_candidate(candidate, track=TRACK)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            candidate = make_candidate(root)
            (candidate / "certificates" / "nested").mkdir(parents=True)
            with self.assertRaisesRegex(VerificationError, "only direct regular files"):
                validate_candidate(candidate, track=TRACK)

        if hasattr(os, "mkfifo"):
            with tempfile.TemporaryDirectory() as directory:
                candidate = make_candidate(Path(directory))
                os.mkfifo(candidate / "pipe")
                with self.assertRaisesRegex(VerificationError, "only regular files"):
                    validate_candidate(candidate, track=TRACK)

    def test_manifest_declaration_and_declared_file_set_are_exact(self):
        certificate = {
            "id": "witness-1",
            "type": "hash-collision-witness-v2",
            "target_profile": TRACK.profile_id,
            "message_a": "certificates/a.bin",
            "message_b": "certificates/b.bin",
            "expected_digest": "0" * 40,
        }
        with tempfile.TemporaryDirectory() as directory:
            candidate = make_candidate(Path(directory))
            add_manifest(candidate, [certificate])
            (candidate / "certificates" / "a.bin").write_bytes(b"a")
            with self.assertRaisesRegex(VerificationError, "declared certificate file.*b.bin"):
                validate_candidate(candidate, track=TRACK)

        with tempfile.TemporaryDirectory() as directory:
            candidate = make_candidate(Path(directory))
            add_manifest(candidate, [])
            (candidate / "certificates" / "undeclared.bin").write_bytes(b"x")
            with self.assertRaisesRegex(VerificationError, "unexpected file.*undeclared.bin"):
                validate_candidate(candidate, track=TRACK)

        with tempfile.TemporaryDirectory() as directory:
            candidate = make_candidate(Path(directory))
            (candidate / "certificates").mkdir()
            write_json(
                candidate / "certificates" / "manifest.json",
                {"schema_version": 1, "certificates": []},
            )
            with self.assertRaisesRegex(VerificationError, "does not declare"):
                validate_candidate(candidate, track=TRACK)

    def test_manifest_rejects_unknown_fields_unsafe_paths_and_duplicate_ids(self):
        base = {
            "id": "witness-1",
            "type": "hash-collision-witness-v2",
            "target_profile": TRACK.profile_id,
            "message_a": "certificates/a.bin",
            "message_b": "certificates/b.bin",
            "expected_digest": "0" * 40,
        }
        invalid_items = []
        unknown = dict(base, command="run me")
        invalid_items.append(([unknown], "unknown field.*command"))
        traversal = dict(base, message_a="certificates/../claim.json")
        invalid_items.append(([traversal], "safe file path"))
        uppercase = dict(base, expected_digest="A" * 40)
        invalid_items.append(([uppercase], "lowercase hexadecimal"))
        invalid_items.append(([base, dict(base)], "must be unique"))

        for certificates, message in invalid_items:
            with self.subTest(message=message), tempfile.TemporaryDirectory() as directory:
                candidate = make_candidate(Path(directory))
                add_manifest(candidate, certificates)
                with self.assertRaisesRegex(VerificationError, message):
                    validate_candidate(candidate, track=TRACK)

        with tempfile.TemporaryDirectory() as directory:
            candidate = make_candidate(Path(directory))
            add_manifest(candidate, [])
            manifest_path = candidate / "certificates" / "manifest.json"
            write_json(
                manifest_path,
                {"schema_version": 1, "certificates": [], "extra": True},
            )
            with self.assertRaisesRegex(VerificationError, "unknown field.*extra"):
                validate_candidate(candidate, track=TRACK)

    def test_output_directory_cannot_be_inside_candidate(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = make_candidate(Path(directory))
            with self.assertRaisesRegex(VerificationError, "outside the candidate"):
                validate_candidate(candidate, candidate / "reports", track=TRACK)


if __name__ == "__main__":
    unittest.main()
