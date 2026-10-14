"""Preparation for scalar policy changes using only organizer-owned fixtures."""

from copy import deepcopy
from pathlib import Path
import tempfile
import unittest

from scripts.scalar_score_resources import read_v5_score_resources
from tests.helpers import candidate_fixture
from verifier.errors import VerificationError
from verifier.frontier_tracks import get_frontier_track
from verifier.intake import validate_candidate
from verifier.io import atomic_write_json, canonical_json_bytes, load_json_bytes
from verifier.score import build_score


class ScalarScoreResourceTests(unittest.TestCase):
    def metrics(self, **changes):
        return {
            "costModelId": "collision-frontier-v5",
            "timeUnit": "target-compressions",
            "timeLog2": 128.0,
            "memoryLog2Bytes": 17.25,
            "scoreMetric": "timeLog2",
            **changes,
        }

    def test_preserves_original_metrics_and_evidence_identifiers(self):
        metrics = self.metrics(
            targetConfigSha256="a" * 64, inputPackageSha256="b" * 64,
            judgeConfigSha256="c" * 64, dossierSha256="d" * 64,
            unresolvedObligations=["historical fixture"],
        )
        before = canonical_json_bytes(metrics)
        self.assertEqual(read_v5_score_resources(metrics), (128, 17.25))
        self.assertEqual(canonical_json_bytes(metrics), before)

    def test_uses_official_resources_not_declared_bound_or_display_scalar(self):
        metrics = self.metrics(timeLog2=110, declaredTimeLog2=128, score=999,
                               normalized_score_log2=777, timeMemoryLog2=888)
        self.assertEqual(read_v5_score_resources(metrics), (110, 17.25))

    def test_does_not_combine_exponents_or_invent_a_normalization(self):
        self.assertEqual(read_v5_score_resources(self.metrics(
            timeLog2=1e308, memoryLog2Bytes=1e308)), (1e308, 1e308))
        self.assertEqual(read_v5_score_resources(self.metrics(
            timeLog2=0, memoryLog2Bytes=0)), (0, 0))

    def test_requires_both_resource_bounds(self):
        for field in ("timeLog2", "memoryLog2Bytes"):
            with self.subTest(field=field):
                metrics = self.metrics()
                del metrics[field]
                with self.assertRaisesRegex(VerificationError, field):
                    read_v5_score_resources(metrics)

    def test_rejects_invalid_or_nonfinite_resource_bounds(self):
        invalid = (None, True, False, "12", [], {}, -1, float("inf"),
                   float("-inf"), float("nan"), 10 ** 1000)
        for field in ("timeLog2", "memoryLog2Bytes"):
            for index, value in enumerate(invalid):
                with self.subTest(field=field, case=index):
                    with self.assertRaisesRegex(VerificationError, field):
                        read_v5_score_resources(self.metrics(**{field: value}))

    def test_requires_explicit_compatible_resource_model_and_units(self):
        for field, values in (
            ("costModelId", (None, "collision-frontier-v3", "collision-frontier-v4",
                             "orchard-field-ram-v2", "unknown")),
            ("timeUnit", (None, "word-operations", "seconds", "target-compression")),
        ):
            for value in values:
                with self.subTest(field=field, value=value):
                    with self.assertRaises(VerificationError):
                        read_v5_score_resources(self.metrics(**{field: value}))
            metrics = self.metrics()
            del metrics[field]
            with self.assertRaises(VerificationError):
                read_v5_score_resources(metrics)

    def test_rejects_missing_or_nonobject_metrics(self):
        for value in (None, [], 1, "metrics"):
            with self.subTest(value=value), self.assertRaisesRegex(VerificationError, "object"):
                read_v5_score_resources(value)

    def test_generated_scores_retain_original_and_reviewed_time_bounds(self):
        track = get_frontier_track("sha256-r37-exploratory")
        with tempfile.TemporaryDirectory() as directory:
            candidate = candidate_fixture(Path(directory), track)
            claim_path = candidate / "claim.json"
            claim = load_json_bytes(claim_path.read_bytes(), str(claim_path))
            claim["claim"]["memory_log2_bytes"] = 17.25
            atomic_write_json(claim_path, claim)
            original_claim = claim_path.read_bytes()
            intake = validate_candidate(candidate, track=track)
            aggregate = {
                "status": track.accepted_status, "lane": track.lane,
                "policy_id": "paired-lanes-v1", "claim": intake["claim"],
                "input_package_sha256": intake["package_sha256"],
                "target_config_sha256": track.config_sha256(),
            }
            before = deepcopy(aggregate)
            ordinary = build_score(candidate, aggregate, track=track)
            reviewed = build_score(candidate, aggregate, track=track, rescore_result={
                "source": "e" * 64, "time_log2": 110, "previous_score": 128,
                "score_policy_changed": True, "declared_cost_model": track.benchmark()["cost_model"],
            })
            self.assertEqual(read_v5_score_resources(ordinary["metrics"]), (128, 17.25))
            self.assertEqual(read_v5_score_resources(reviewed["metrics"]), (110, 17.25))
            self.assertEqual(reviewed["metrics"]["declaredTimeLog2"], 128)
            self.assertEqual(ordinary["score"], 128)
            self.assertEqual(reviewed["score"], 110)
            self.assertEqual(aggregate, before)
            self.assertEqual(claim_path.read_bytes(), original_claim)


if __name__ == "__main__":
    unittest.main()
