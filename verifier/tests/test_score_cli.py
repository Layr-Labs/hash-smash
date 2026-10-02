from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import PropertyMock, patch

from verifier.errors import VerificationError
from verifier.score import build_score
from verifier.intake import validate_candidate

from verifier.tests.common import TRACK, add_manifest, make_candidate


class ScoreTests(unittest.TestCase):
    @staticmethod
    def qualified_aggregate(candidate, **extra):
        intake = validate_candidate(candidate, track=TRACK)
        value = {
            "status": TRACK.accepted_status,
            "lane": TRACK.lane,
            "policy_id": "paired-lanes-v1",
            "claim": intake["claim"],
            "input_package_sha256": intake["package_sha256"],
            "target_config_sha256": TRACK.config_sha256(),
        }
        value.update(extra)
        return value

    def test_ai_rigor_qualified_score_is_recomputed_from_claim(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            candidate = make_candidate(root)
            output = root / "score.json"
            aggregate = self.qualified_aggregate(
                candidate,
                score=-999,
                judge_config_sha256="a" * 64,
                dossier_sha256="b" * 64,
            )
            score = build_score(candidate, aggregate, output, track=TRACK)
            self.assertEqual(score["score"], 81.0)
            self.assertEqual(score["metrics"]["timeLog2"], 81.0)
            self.assertEqual(score["metrics"]["memoryLog2Bytes"], 85.0)
            self.assertEqual(score["metrics"]["scoreMetric"], "timeLog2")
            self.assertEqual(score["metrics"]["costModelId"], "collision-frontier-v5")
            self.assertNotIn("timeMemoryLog2", score["metrics"])
            self.assertEqual(score["metrics"]["judgeConfigSha256"], "a" * 64)
            self.assertEqual(json.loads(output.read_text()), score)

    def test_memory_is_reported_but_never_changes_ranking_or_breaks_ties(self):
        results = []
        # The faster algorithm wins even with a much larger memory bound.
        # Equal-time algorithms tie, including when the former sum would overflow.
        for time, memory in ((79, 1), (79, 1000), (80, 0), (1e308, 1e308)):
            with self.subTest(time=time, memory=memory), tempfile.TemporaryDirectory() as directory:
                candidate = make_candidate(Path(directory))
                path = candidate / "claim.json"
                claim = json.loads(path.read_text())
                claim["claim"].update(time_log2=time, memory_log2_bytes=memory)
                path.write_text(json.dumps(claim))
                result = build_score(candidate, self.qualified_aggregate(candidate), track=TRACK)
                self.assertEqual(result["score"], time)
                self.assertEqual(result["metrics"]["memoryLog2Bytes"], memory)
                self.assertEqual(result["metrics"]["improvesNominalReference"], time < 80)
                results.append(result["score"])
        self.assertEqual(results[0], results[1])
        self.assertLess(results[1], results[2])

    def test_review_bound_to_former_cost_model_cannot_be_reused(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = make_candidate(Path(directory))
            with patch.object(type(TRACK), "cost_path", new_callable=PropertyMock) as cost_path:
                cost_path.return_value = TRACK.profile_path.parents[1] / "cost-models/collision-frontier-v3.json"
                with self.assertRaisesRegex(VerificationError, "unexpected frontier cost model"):
                    TRACK.benchmark()
            aggregate = self.qualified_aggregate(candidate, target_config_sha256="0" * 64)
            with self.assertRaisesRegex(VerificationError, "stale or mismatched target configuration"):
                build_score(candidate, aggregate, track=TRACK)

    def test_nonqualified_aggregate_never_emits_score(self):
        statuses = ["clarification_required", "technical_blocker", "judge_infra_failed", None]
        for status in statuses:
            with self.subTest(status=status), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                candidate = make_candidate(root)
                output = root / "score.json"
                aggregate = {} if status is None else {"status": status}
                with self.assertRaisesRegex(VerificationError, "ai_rigor_qualified"):
                    build_score(candidate, aggregate, output, track=TRACK)
                self.assertFalse(output.exists())

    def test_invalid_optional_aggregate_hash_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = make_candidate(Path(directory))
            with self.assertRaisesRegex(VerificationError, "64 lowercase"):
                build_score(
                    candidate,
                    self.qualified_aggregate(candidate, dossier_sha256="not-a-hash"),
                    track=TRACK,
                )

    def test_reconstructed_claim_must_match_submission(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = make_candidate(Path(directory))
            aggregate = self.qualified_aggregate(candidate)
            aggregate["claim"]["rounds"] = 79
            with self.assertRaisesRegex(VerificationError, "entire submitted claim"):
                build_score(candidate, aggregate, track=TRACK)

    def test_failed_certificate_gate_does_not_emit_score(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            candidate = make_candidate(root)
            add_manifest(
                candidate,
                [
                    {
                        "id": "not-a-collision",
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
            output = root / "score.json"
            with self.assertRaisesRegex(VerificationError, "does not match expected"):
                build_score(candidate, self.qualified_aggregate(candidate), output, track=TRACK)
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
                    "--track",
                    TRACK.id,
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
                    "--track",
                    TRACK.id,
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
            self.assertIn("ai_rigor_qualified", score.stderr)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
