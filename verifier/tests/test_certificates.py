from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from verifier.certificates import verify_certificates
from verifier.errors import VerificationError

from verifier.tests.common import add_manifest, make_candidate


class _Digest:
    def __init__(self, value: str):
        self.value = value

    def hexdigest(self) -> str:
        return self.value


class CertificateTests(unittest.TestCase):
    def test_absent_manifest_is_a_valid_empty_certificate_set(self):
        with tempfile.TemporaryDirectory() as directory:
            report = verify_certificates(make_candidate(Path(directory)))
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
                        "type": "sha1-collision-witness-v1",
                        "message_a": "certificates/a.bin",
                        "message_b": "certificates/b.bin",
                        "expected_digest": expected,
                    }
                ],
            )
            (candidate / "certificates" / "a.bin").write_bytes(b"message a")
            (candidate / "certificates" / "b.bin").write_bytes(b"message b")
            output = root / "certificate-report.json"
            with patch("verifier.certificates.hashlib.sha1", return_value=_Digest(expected)) as sha1:
                report = verify_certificates(candidate, output)

            self.assertEqual(sha1.call_count, 2)
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
                        "type": "sha1-collision-witness-v1",
                        "message_a": "certificates/a.bin",
                        "message_b": "certificates/b.bin",
                        "expected_digest": "0" * 40,
                    }
                ],
            )
            (candidate / "certificates" / "a.bin").write_bytes(b"same")
            (candidate / "certificates" / "b.bin").write_bytes(b"same")
            with self.assertRaisesRegex(VerificationError, "messages must differ"):
                verify_certificates(candidate)

    def test_expected_digest_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = make_candidate(Path(directory))
            add_manifest(
                candidate,
                [
                    {
                        "id": "bad",
                        "type": "sha1-collision-witness-v1",
                        "message_a": "certificates/a.bin",
                        "message_b": "certificates/b.bin",
                        "expected_digest": "0" * 40,
                    }
                ],
            )
            (candidate / "certificates" / "a.bin").write_bytes(b"a")
            (candidate / "certificates" / "b.bin").write_bytes(b"b")
            with self.assertRaisesRegex(VerificationError, "does not match expected"):
                verify_certificates(candidate)


if __name__ == "__main__":
    unittest.main()
