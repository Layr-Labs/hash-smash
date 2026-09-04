from __future__ import annotations

from copy import deepcopy
from contextlib import redirect_stdout
import io
import json
from unittest.mock import patch
import unittest

from judge.bedrock_adapter import BedrockConfig
from judge.lanes import OBLIGATIONS
from judge.paired_review import evidence_binding, run_paired_review
from judge.provider_adapter import ReviewResult
from scripts import calibrate_paired_judges as calibration


class OfflineCalibrationClient:
    """Synthetic review records exercise wiring, not model quality."""

    def __init__(self, config=None, *, false_proof=False):
        self.config = config
        self.false_proof = false_proof
        self.calls = []

    def review(self, stage, evidence):
        self.calls.append(stage)
        review = {
            "schema_version": "review-lanes-v1", "stage": stage,
            "binding": deepcopy(evidence["review_context"]["binding"]),
            "summary": "Offline organizer transport fixture.",
            "obligations": [{"id": key, "status": "supported", "explanation": "Organizer fixture checks this step.",
                             "evidence": ["proof.md:L1"]} for key in OBLIGATIONS[stage]],
            "heuristics": [], "findings": [], "cost_reconstruction": None,
            "challenge_resolutions": [], "prompt_injection_detected": False,
        }
        if stage == "lane_cost":
            cost = deepcopy(evidence["submission"]["intake_report"]["claim"]["claim"])
            cost.update(normalized_score_log2=cost["time_log2"] + cost["memory_log2_bytes"],
                        calculation_trace=["Sum the two submitted exponents."])
            review["cost_reconstruction"] = cost
        if self.false_proof and stage == "lane_cryptanalysis":
            review["obligations"][0]["status"] = "fatal"
            review["findings"] = [{
                "id": "low-bit", "severity": "fatal", "category": "counterexample",
                "statement": "The two messages hash to distinct values 0 and 1.",
                "obligation_ids": ["collision_correctness"], "heuristic_ids": [], "evidence": ["proof.md:L9-L12"],
            }]
        for finding_id in evidence["review_context"].get("fatal_findings", {}):
            review["challenge_resolutions"].append({
                "finding_id": finding_id, "result": "confirmed", "explanation": "0 & 15 != 1 & 15.",
                "evidence": ["proof.md:L9-L12"], "obligations_discharged": [],
            })
        return ReviewResult(review, {"provider": "offline-organizer-fixture"})


class PairedCalibrationTests(unittest.TestCase):
    def test_positive_is_an_exact_distinct_message_collision(self):
        first, second = bytes((0, 0)), bytes((16, 0))
        self.assertNotEqual(first, second)
        self.assertEqual(calibration.toy_projection(first), calibration.toy_projection(second))
        evidence = calibration.build_case("positive")
        self.assertIn("b=(16,0)", evidence["submission"]["proof_markdown_line_numbered"])
        client = OfflineCalibrationClient()
        dossier = run_paired_review(evidence, client)
        self.assertTrue(calibration.classify("positive", dossier)["all_expected"])
        self.assertEqual(len(client.calls), 4)

    def test_false_fixture_pair_is_objectively_not_a_collision(self):
        self.assertEqual(calibration.toy_projection(bytes((0, 0))), 0)
        self.assertEqual(calibration.toy_projection(bytes((1, 0))), 1)
        evidence = calibration.build_case("false-proof")
        self.assertIn("b=(1,0)", evidence["submission"]["proof_markdown_line_numbered"])
        client = OfflineCalibrationClient(false_proof=True)
        dossier = run_paired_review(evidence, client)
        self.assertTrue(calibration.classify("false-proof", dossier)["all_expected"])
        self.assertEqual(len(client.calls), 6)

    def test_all_targets_are_explicitly_synthetic_and_evidence_bound(self):
        bindings = []
        for case in calibration.CASES:
            evidence = calibration.build_case(case)
            profile = evidence["benchmark"]["target_profile"]
            self.assertTrue(profile["id"].startswith("toy-"))
            self.assertTrue(evidence["benchmark"]["calibration_only"])
            intake = evidence["submission"]["intake_report"]
            for name in ("certificate_report", "experiment_report"):
                report = evidence["submission"][name]
                self.assertEqual(report["package_sha256"], intake["package_sha256"])
                self.assertEqual(report["target_config_sha256"], intake["target_config_sha256"])
            bindings.append(evidence_binding(evidence)["evidence_sha256"])
        self.assertEqual(len(set(bindings)), 3)

    def test_reference_labels_are_not_leaked_into_judge_evidence(self):
        positive = calibration.build_case("positive")["submission"]["proof_markdown_line_numbered"]
        false = calibration.build_case("false-proof")["submission"]["proof_markdown_line_numbered"]
        self.assertEqual(positive.splitlines()[0], false.splitlines()[0])
        self.assertNotIn("false projection", false)
        self.assertNotIn("reference evaluation in the evidence", positive)

    def test_heuristic_observations_reproduce_and_check_every_witness(self):
        report = calibration.heuristic_experiment()
        self.assertEqual(report, calibration.heuristic_experiment())
        self.assertEqual(report["successes"], 17)
        self.assertEqual(report["trial_count"], 32)
        self.assertLess(report["interval"]["lower"], 0.5)
        self.assertGreater(report["interval"]["upper"], 0.5)
        for trial in report["trials"]:
            messages = [bytes.fromhex(value) for value in trial["messages_hex"]]
            self.assertEqual([calibration.toy_prefix10(message) for message in messages], trial["outputs"])
            actual = any(messages[i] != messages[j] and trial["outputs"][i] == trial["outputs"][j]
                         for i in range(32) for j in range(i + 1, 32))
            self.assertEqual(trial["success"], actual)
            if actual:
                i, j = trial["witness_indices"]
                self.assertNotEqual(messages[i], messages[j])
                self.assertEqual(trial["outputs"][i], trial["outputs"][j])

    def test_heuristic_case_discloses_unresolved_probability_and_runner_type(self):
        evidence = calibration.build_case("heuristic")
        submission = evidence["submission"]
        claim = submission["intake_report"]["claim"]
        self.assertEqual(claim["claim"]["success_probability"], 0.5)
        self.assertEqual(claim["heuristics"][0]["id"], "H1")
        self.assertIn("experiment_manifest", claim)
        report = submission["experiment_report"]
        self.assertEqual(report["status"], "passed")
        self.assertFalse(report["execution"]["sandboxed_participant_execution"])
        self.assertIn("do not establish the lower bound 0.5", submission["proof_markdown_line_numbered"])

    def test_dry_run_uses_no_credentials_and_writes_only_diagnostic_reports(self):
        written = []
        with patch.object(calibration.BedrockConfig, "from_env") as bedrock_env, \
                patch.object(calibration.OpenRouterConfig, "from_env") as openrouter_env, \
                patch.object(calibration, "atomic_write_json", side_effect=lambda path, data: written.append((path, data))), \
                redirect_stdout(io.StringIO()):
            self.assertEqual(calibration.main(["--dry-run", "--case", "all"]), 0)
        bedrock_env.assert_not_called()
        openrouter_env.assert_not_called()
        self.assertEqual(len(written), 3)
        for destination, report in written:
            self.assertEqual(destination.parent, calibration.REPORT_DIR)
            self.assertNotEqual(destination.name, "score.json")
            self.assertTrue(report["no_score_emitted"])
            self.assertFalse(report["is_qualified_baseline"])
            self.assertNotIn("dossier", report)

    def test_mocked_live_cli_has_bounded_calls_and_never_publishes_key(self):
        secret = "calibration-fixture-credential-never-publish"
        config = BedrockConfig(api_key=secret)
        clients, written = [], []
        def factory(effective):
            client = OfflineCalibrationClient(effective)
            clients.append(client)
            return client
        captured = io.StringIO()
        with patch.object(calibration.BedrockConfig, "from_env", return_value=config), \
                patch.object(calibration, "BedrockClient", side_effect=factory), \
                patch.object(calibration, "atomic_write_json", side_effect=lambda path, data: written.append((path, data))), \
                redirect_stdout(captured):
            result = calibration.main(["--provider", "bedrock", "--mode", "single", "--case", "positive"])
        self.assertEqual(result, 0)
        self.assertEqual(len(clients[0].calls), 4)
        self.assertEqual(clients[0].config.max_attempts, 1)
        self.assertEqual(len(written), 1)
        self.assertNotIn(secret, json.dumps(written[0][1]))
        self.assertNotIn(secret, captured.getvalue())

    def test_classification_marks_disagreement_without_claiming_error_rates(self):
        dossier = {"lanes": {"exploratory": {"status": "plausible_not_refuted"},
                             "rigorous": {"status": "ai_rigor_qualified"}}}
        classification = calibration.classify("heuristic", dossier)
        self.assertFalse(classification["all_expected"])
        self.assertIn("no statistical FP/FN estimate", classification["interpretation"])

    def test_unknown_case_rejected(self):
        with self.assertRaises(ValueError):
            calibration.build_case("../../candidate/proof")


if __name__ == "__main__":
    unittest.main()
