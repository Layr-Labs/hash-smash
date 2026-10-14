"""Approved golden vectors and explicit artificial-policy arithmetic tests."""

from copy import deepcopy
import json
from pathlib import Path
import unittest
import tempfile
from unittest.mock import patch

from scripts.scalar_scoring_policy import (ACTIVE_POLICY_PATH, active_scalar_policy,
                                          scalar_score, scoring_policy_metadata, validate_policy)
from verifier.errors import VerificationError
from verifier.io import canonical_json_bytes


class ScalarScoringPolicyTests(unittest.TestCase):
    def setUp(self):
        self.policy = json.loads((Path(__file__).parent / "fixtures/scalar-scoring/policy.json").read_text())
        self.metrics = {
            "costModelId": "collision-frontier-v5", "timeUnit": "target-compressions",
            "timeLog2": 70, "memoryLog2Bytes": 20,
            "targetConfigSha256": "a" * 64, "dossierSha256": "b" * 64,
            "inputPackageSha256": "c" * 64, "judgeConfigSha256": "d" * 64,
        }

    def test_approved_policy_matches_shared_golden_vectors_and_pinned_hash(self):
        vectors = json.loads((Path(__file__).parent / "fixtures/scalar-scoring/approved-policy-vectors.json").read_text())
        policy = active_scalar_policy()
        self.assertEqual(policy, vectors["policy"])
        self.assertEqual(scoring_policy_metadata(policy), vectors["metadata"])
        for case in vectors["cases"]:
            with self.subTest(metrics=case["metrics"]):
                self.assertEqual(scalar_score(case["metrics"], policy), case["score"])

    def test_active_policy_rejects_relabelled_or_changed_definition(self):
        for field, value in (("id", "different-policy"), ("minimumMemoryUnits", None),
                             ("memoryUnitBytes", 1000000)):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                definition = {**active_scalar_policy(), field: value}
                path = Path(directory) / "policy.json"
                path.write_text(json.dumps(definition))
                with patch("scripts.scalar_scoring_policy.ACTIVE_POLICY_PATH", path):
                    with self.assertRaisesRegex(VerificationError, "pinned ID and definition hash"):
                        active_scalar_policy()

    def test_future_fingerprint_binds_effective_helpers_and_policy_bytes(self):
        from verifier.frontier_tracks import ROOT, get_frontier_track
        track = get_frontier_track("sha256-r37-exploratory")
        before = track.config_sha256()
        original = Path.read_bytes
        for target in (ROOT / "scripts/scalar_scoring_policy.py",
                       ROOT / "scripts/scalar_score_resources.py", ACTIVE_POLICY_PATH):
            def changed_bytes(path):
                data = original(path)
                return data + b"\n" if path == target else data
            with self.subTest(path=target), patch.object(Path, "read_bytes", changed_bytes):
                self.assertNotEqual(track.config_sha256(), before)

    def test_fixture_floor_below_at_and_above_unit(self):
        for memory, expected in ((0, 70), (9, 70), (10, 70), (20, 80)):
            with self.subTest(memory=memory):
                self.assertEqual(scalar_score({**self.metrics, "memoryLog2Bytes": memory}, self.policy), expected)

    def test_explicit_fractional_units_allow_negative_scalar(self):
        policy = {**self.policy, "minimumMemoryUnits": None}
        self.assertEqual(scalar_score({**self.metrics, "memoryLog2Bytes": 9}, policy), 69)
        self.assertEqual(scalar_score({**self.metrics, "timeLog2": 0, "memoryLog2Bytes": 0}, policy), -10)

    def test_unit_is_explicit_and_large_costs_do_not_need_exponentiation(self):
        policy = {**self.policy, "memoryUnitBytes": 1000}
        self.assertAlmostEqual(scalar_score(self.metrics, policy), 80.03421571533791, places=12)
        self.assertEqual(scalar_score({**self.metrics, "memoryLog2Bytes": 2000}, self.policy), 2060)

    def test_overflow_is_rejected(self):
        with self.assertRaisesRegex(VerificationError, "result must be finite"):
            scalar_score({**self.metrics, "timeLog2": 1e308, "memoryLog2Bytes": 1e308}, self.policy)

    def test_projection_changes_only_separate_metadata_and_preserves_inputs(self):
        original = deepcopy((self.metrics, self.policy))
        score = scalar_score(self.metrics, self.policy)
        marker = scoring_policy_metadata(self.policy)
        self.assertEqual(score, 80)
        self.assertEqual(set(marker), {"scoringPolicyId", "scoringPolicySha256", "scoreMetric"})
        self.assertEqual(marker["scoringPolicyId"], self.policy["id"])
        self.assertEqual(marker["scoreMetric"], "normalizedTimeMemoryLog2")
        self.assertEqual((self.metrics, self.policy), original)

    def test_definition_identity_is_order_independent_but_binds_each_parameter(self):
        marker = scoring_policy_metadata(self.policy)
        self.assertEqual(marker["scoringPolicySha256"],
                         "62618c3da17486edc0e4f84dc6a5e2bb4fe0e2d3c660befa55f58993f8f623fa")
        reordered = dict(reversed(list(self.policy.items())))
        self.assertEqual(scoring_policy_metadata(reordered), marker)
        for field, value in (("id", "another-fixture-v1"), ("memoryUnitBytes", 1000),
                             ("minimumMemoryUnits", None)):
            with self.subTest(field=field):
                self.assertNotEqual(scoring_policy_metadata({**self.policy, field: value})["scoringPolicySha256"],
                                    marker["scoringPolicySha256"])

    def test_no_default_policy_or_missing_parameters(self):
        for policy in (None, {}, {**self.policy, "extra": "field"}):
            with self.subTest(policy=policy), self.assertRaises(VerificationError):
                scalar_score(self.metrics, policy)
        for field in self.policy:
            policy = dict(self.policy)
            del policy[field]
            with self.subTest(field=field), self.assertRaises(VerificationError):
                validate_policy(policy)

    def test_refuses_unknown_semantics_and_noncanonical_numbers(self):
        for field, values in (
            ("id", ("", "UPPERCASE", "bad\nid", "x" * 97, None)),
            ("version", (True, 1.0, 2)),
            ("formula", ("timeLog2", "")),
            ("sourceCostModelId", ("collision-frontier-v4", "orchard-field-ram-v2")),
            ("timeUnit", ("seconds",)),
            ("memoryUnitBytes", (True, 0, -1, 1024.0, "1024", 2 ** 53, float("nan"))),
            ("minimumMemoryUnits", (True, False, 0, 1.0, 2, "1")),
        ):
            for value in values:
                with self.subTest(field=field, value=value), self.assertRaises(VerificationError):
                    validate_policy({**self.policy, field: value})

    def test_canonical_definition_has_only_ascii_and_integer_parameters(self):
        # Shared serialization contract for the Yukon maintenance implementation.
        self.assertEqual(canonical_json_bytes(validate_policy(self.policy)), (
            b'{"formula":"timeLog2 + log2(memoryUnits)","id":"organizer-fixture-scalar-v1",'
            b'"memoryUnitBytes":1024,"minimumMemoryUnits":1,"sourceCostModelId":"collision-frontier-v5",'
            b'"timeUnit":"target-compressions","version":1}\n'
        ))


if __name__ == "__main__":
    unittest.main()
