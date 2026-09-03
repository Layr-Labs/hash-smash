from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from verifier.errors import VerificationError
from verifier.score import build_score

from verifier.tests.common import add_manifest, make_candidate


class ScoreTests(unittest.TestCase):
    @staticmethod
    def qualified_aggregate(**extra):
        value = {
            "status": "ai_qualified",
            "claim": {
                "target_profile": "sha1-fips180-4-v1",
                "attack_class": "ordinary-collision",
                "rounds": 80,
                "restrictions": [],
            },
        }
        value.update(extra)
        return value

    def test_ai_qualified_score_is_recomputed_from_claim(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            candidate = make_candidate(root)
            output = root / "score.json"
            aggregate = self.qualified_aggregate(
                score=-999,
                judge_config_sha256="a" * 64,
                dossier_sha256="b" * 64,
            )
            score = build_score(candidate, aggregate, output)
            self.assertEqual(score["score"], 166.0)
            self.assertEqual(score["metrics"]["timeLog2"], 81.0)
            self.assertEqual(score["metrics"]["memoryLog2Bytes"], 85.0)
            self.assertEqual(score["metrics"]["judgeConfigSha256"], "a" * 64)
            self.assertEqual(json.loads(output.read_text()), score)

    def test_nonqualified_aggregate_never_emits_score(self):
        statuses = ["clarification_required", "technical_blocker", "judge_infra_failed", None]
        for status in statuses:
            with self.subTest(status=status), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                candidate = make_candidate(root)
                output = root / "score.json"
                aggregate = {} if status is None else {"status": status}
                with self.assertRaisesRegex(VerificationError, "ai_qualified"):
                    build_score(candidate, aggregate, output)
                self.assertFalse(output.exists())

    def test_invalid_optional_aggregate_hash_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = make_candidate(Path(directory))
            with self.assertRaisesRegex(VerificationError, "64 lowercase"):
                build_score(
                    candidate,
                    self.qualified_aggregate(dossier_sha256="not-a-hash"),
                )

    def test_reconstructed_claim_must_match_submission(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = make_candidate(Path(directory))
            aggregate = self.qualified_aggregate()
            aggregate["claim"]["rounds"] = 79
            with self.assertRaisesRegex(VerificationError, "differs.*rounds"):
                build_score(candidate, aggregate)

    def test_failed_certificate_gate_does_not_emit_score(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            candidate = make_candidate(root)
            add_manifest(
                candidate,
                [
                    {
                        "id": "not-a-collision",
                        "type": "sha1-collision-witness-v1",
                        "message_a": "certificates/a.bin",
                        "message_b": "certificates/b.bin",
                        "expected_digest": "0" * 40,
                    }
                ],
            )
            (candidate / "certificates" / "a.bin").write_bytes(b"a")
            (candidate / "certificates" / "b.bin").write_bytes(b"b")
            output = root / "score.json"
            with self.assertRaisesRegex(VerificationError, "does not match expected"):
                build_score(candidate, self.qualified_aggregate(), output)
            self.assertFalse(output.exists())

    def test_cli_end_to_end_and_failure_exit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            candidate = make_candidate(root)
            artifacts = root / "intake"
            intake = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "verifier",
                    "intake",
                    "--candidate",
                    str(candidate),
                    "--output-dir",
                    str(artifacts),
                ],
                cwd=Path(__file__).parents[2],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(intake.returncode, 0, intake.stderr)
            self.assertEqual(json.loads(intake.stdout)["status"], "mechanically_valid")

            aggregate = root / "aggregate.json"
            aggregate.write_text(json.dumps({"status": "technical_blocker"}))
            output = root / "score.json"
            score = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "verifier",
                    "score",
                    "--candidate",
                    str(candidate),
                    "--aggregate",
                    str(aggregate),
                    "--output",
                    str(output),
                ],
                cwd=Path(__file__).parents[2],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(score.returncode, 2)
            self.assertIn("ai_qualified", score.stderr)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
