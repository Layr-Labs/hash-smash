from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from verifier.certificates import verify_certificates
from verifier.errors import VerificationError

from verifier.tests.common import TRACK, add_manifest, make_candidate


class CertificateTests(unittest.TestCase):
    def test_absent_manifest_is_a_valid_empty_certificate_set(self):
        with tempfile.TemporaryDirectory() as directory:
            report = verify_certificates(make_candidate(Path(directory)), track=TRACK)
            self.assertEqual(report["status"], "passed")
            self.assertEqual(report["certificates"], [])

    def test_two_distinct_messages_with_expected_equal_sha1_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            candidate = make_candidate(root)
            expected = "a" * 40
            add_manifest(
                candidate,
                [
                    {
                        "id": "witness-1",
                        "type": "hash-collision-witness-v2",
                        "target_profile": TRACK.profile_id,
                        "message_a": "certificates/a.bin",
                        "message_b": "certificates/b.bin",
                        "expected_digest": expected,
                    }
                ],
            )
            (candidate / "certificates" / "a.bin").write_bytes(b"message a")
            (candidate / "certificates" / "b.bin").write_bytes(b"message b")
            output = root / "certificate-report.json"
            with patch("verifier.certificates.digest", return_value=bytes.fromhex(expected)) as checker:
                report = verify_certificates(candidate, output, track=TRACK)

            self.assertEqual(checker.call_count, 2)
            checker.assert_any_call(b"message a", TRACK.algorithm, TRACK.rounds)
            checker.assert_any_call(b"message b", TRACK.algorithm, TRACK.rounds)
            self.assertEqual(report["certificates"][0]["status"], "verified")
            self.assertTrue(output.is_file())
            self.assertNotEqual(
                report["certificates"][0]["message_a"]["sha256"],
                report["certificates"][0]["message_b"]["sha256"],
            )

    def test_identical_messages_rejected_before_hash_comparison(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = make_candidate(Path(directory))
            add_manifest(
                candidate,
                [
                    {
                        "id": "same",
                        "type": "hash-collision-witness-v2",
                        "target_profile": TRACK.profile_id,
                        "message_a": "certificates/a.bin",
                        "message_b": "certificates/b.bin",
                        "expected_digest": "0" * 40,
                    }
                ],
            )
            (candidate / "certificates" / "a.bin").write_bytes(b"same")
            (candidate / "certificates" / "b.bin").write_bytes(b"same")
            with self.assertRaisesRegex(VerificationError, "messages must differ"):
                verify_certificates(candidate, track=TRACK)

    def test_expected_digest_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = make_candidate(Path(directory))
            add_manifest(
                candidate,
                [
                    {
                        "id": "bad",
                        "type": "hash-collision-witness-v2",
                        "target_profile": TRACK.profile_id,
                        "message_a": "certificates/a.bin",
                        "message_b": "certificates/b.bin",
                        "expected_digest": "0" * 40,
                    }
                ],
            )
            (candidate / "certificates" / "a.bin").write_bytes(b"a")
            (candidate / "certificates" / "b.bin").write_bytes(b"b")
            with self.assertRaisesRegex(VerificationError, "does not match expected"):
                verify_certificates(candidate, track=TRACK)


if __name__ == "__main__":
    unittest.main()
